"""
Block Attention Residuals (Block AttnRes)

Based on: "Attention Residuals" by Kimi Team (Moonshot AI), arXiv:2603.15031

Replaces fixed-weight residual accumulation (PreNorm dilution) with learned,
input-dependent depth-wise softmax attention over block-level representations.

Standard residual:  h_l = h_{l-1} + f_l(h_{l-1})
AttnRes:            h_l = sum_i alpha_{i->l} * v_i
Block AttnRes:      Partition layers into blocks; within blocks use standard
                    residuals, between blocks use depth-wise softmax attention.
"""

import torch
import torch.nn as nn
from typing import List, Optional, Tuple

from .modeling_normalization import RMSNorm


class BlockAttentionResidual(nn.Module):
    """
    Block Attention Residual module for depth-wise attention aggregation.

    Instead of accumulating layer outputs with fixed unit weights (standard
    residual connections), this module learns to selectively aggregate previous
    block outputs using softmax attention over depth.

    Each layer has a learned pseudo-query vector w_l (initialized to zero for
    uniform initial weights). At block boundaries, attention is computed over
    all previous block outputs to produce the aggregated hidden state.

    Args:
        dim: Hidden state dimension.
        num_layers: Total number of transformer layers.
        block_size: Number of sublayer steps per block. Each transformer layer
                    has 2 sublayers (attention + MLP), so block_size=8 means
                    4 transformer layers per block. Default: 8.
        eps: Epsilon for RMSNorm. Default: 1e-6.
    """

    def __init__(
        self,
        dim: int,
        num_layers: int,
        block_size: int = 8,
        eps: float = 1e-6,
    ):
        super().__init__()
        self.dim = dim
        self.num_layers = num_layers
        self.block_size = block_size

        # Total sublayer steps: each transformer layer has 2 (attn + mlp)
        self.total_steps = num_layers * 2
        # Number of block boundaries (transitions) during forward pass
        self.num_blocks = (self.total_steps + block_size - 1) // block_size

        # Per-layer pseudo-query projection: projects normalized block outputs
        # to scalar logits for depth-wise attention. One per sublayer step.
        self.query_projs = nn.ModuleList([
            nn.Linear(dim, 1, bias=False) for _ in range(self.total_steps)
        ])

        # RMSNorm applied to stacked block representations before projection
        self.depth_norm = RMSNorm(dim, eps=eps, elementwise_affine=False)

        # Initialize all pseudo-query vectors to zero (ensures uniform
        # attention at start of training, reducing to equal-weight average)
        self._init_weights()

    def _init_weights(self):
        for proj in self.query_projs:
            nn.init.zeros_(proj.weight)

    def forward(
        self,
        current_hidden: torch.Tensor,
        sublayer_output: torch.Tensor,
        step_idx: int,
        block_outputs: List[torch.Tensor],
        partial_block: torch.Tensor,
        block_step_count: int,
    ) -> Tuple[torch.Tensor, List[torch.Tensor], torch.Tensor, int]:
        """
        Compute Block AttnRes aggregation for one sublayer step.

        Args:
            current_hidden: Current hidden state [B, T, D] (unused in AttnRes
                           mode, kept for API compatibility).
            sublayer_output: Output of the current sublayer f_l(h) [B, T, D].
            step_idx: Current sublayer step index (0-indexed).
            block_outputs: List of completed block representations [B, T, D].
            partial_block: Running sum within current block [B, T, D].
            block_step_count: Number of steps accumulated in current block.

        Returns:
            new_hidden: The new hidden state after AttnRes aggregation [B, T, D].
            block_outputs: Updated list of block outputs.
            partial_block: Updated partial block accumulation.
            block_step_count: Updated step count within current block.
        """
        # Accumulate sublayer output into partial block (standard residual
        # within the block)
        partial_block = partial_block + sublayer_output
        block_step_count += 1

        # Check if we've reached a block boundary
        is_block_boundary = (block_step_count >= self.block_size) or \
                           (step_idx == self.total_steps - 1)

        if is_block_boundary:
            # Save the completed block output
            block_outputs.append(partial_block)

            # Compute depth-wise attention over all block outputs
            new_hidden = self._depth_attention(
                block_outputs, step_idx
            )

            # Reset partial block for next block
            partial_block = torch.zeros_like(new_hidden)
            block_step_count = 0
        else:
            # Within a block: the hidden state is the partial accumulation
            new_hidden = partial_block

        return new_hidden, block_outputs, partial_block, block_step_count

    def _depth_attention(
        self,
        block_outputs: List[torch.Tensor],
        step_idx: int,
    ) -> torch.Tensor:
        """
        Compute softmax attention over block-level representations.

        Args:
            block_outputs: List of N block outputs, each [B, T, D].
            step_idx: Current sublayer step index for selecting the query proj.

        Returns:
            Aggregated hidden state [B, T, D].
        """
        num_blocks = len(block_outputs)

        if num_blocks == 1:
            # Only one block: no attention needed, just return it
            return block_outputs[0]

        # Stack block outputs: [N, B, T, D]
        V = torch.stack(block_outputs, dim=0)

        # Normalize for computing attention logits
        K = self.depth_norm(V)  # [N, B, T, D]

        # Compute scalar logits per block using pseudo-query projection
        # logits: [N, B, T, 1] -> [N, B, T]
        proj = self.query_projs[step_idx]
        logits = proj(K).squeeze(-1)  # [N, B, T]

        # Softmax over depth dimension (dim=0)
        alpha = torch.softmax(logits, dim=0)  # [N, B, T]

        # Weighted aggregation: [N, B, T] x [N, B, T, D] -> [B, T, D]
        h = torch.einsum('n b t, n b t d -> b t d', alpha, V)

        return h


class BlockAttentionResidualDualStream(nn.Module):
    """
    Dual-stream Block AttnRes for joint transformer architectures.

    Manages separate AttnRes streams for hidden_states (video latents) and
    encoder_hidden_states (text embeddings), since they follow different
    residual paths in the MMDiT architecture.

    Args:
        dim: Hidden state dimension.
        num_layers: Total number of transformer layers.
        block_size: Sublayer steps per block (default: 8).
        eps: RMSNorm epsilon.
        apply_to_encoder: Whether to also apply AttnRes to the encoder
                         (text) stream. Default: False (encoder stream uses
                         standard residuals to preserve text conditioning).
    """

    def __init__(
        self,
        dim: int,
        num_layers: int,
        block_size: int = 8,
        eps: float = 1e-6,
        apply_to_encoder: bool = False,
    ):
        super().__init__()
        self.hidden_attn_res = BlockAttentionResidual(
            dim=dim,
            num_layers=num_layers,
            block_size=block_size,
            eps=eps,
        )
        self.apply_to_encoder = apply_to_encoder
        if apply_to_encoder:
            self.encoder_attn_res = BlockAttentionResidual(
                dim=dim,
                num_layers=num_layers,
                block_size=block_size,
                eps=eps,
            )

    def init_state(self, hidden_states: torch.Tensor, encoder_hidden_states: torch.Tensor):
        """Initialize tracking state at the start of the forward pass."""
        return {
            'hidden_block_outputs': [],
            'hidden_partial_block': torch.zeros_like(hidden_states),
            'hidden_block_step_count': 0,
            'encoder_block_outputs': [] if self.apply_to_encoder else None,
            'encoder_partial_block': torch.zeros_like(encoder_hidden_states) if self.apply_to_encoder else None,
            'encoder_block_step_count': 0 if self.apply_to_encoder else None,
            'step_idx': 0,
        }

    def step(
        self,
        state: dict,
        hidden_states: torch.Tensor,
        sublayer_hidden_output: torch.Tensor,
        encoder_hidden_states: Optional[torch.Tensor],
        sublayer_encoder_output: Optional[torch.Tensor],
    ) -> Tuple[torch.Tensor, Optional[torch.Tensor]]:
        """
        Process one sublayer step for both streams.

        Args:
            state: Mutable state dict from init_state().
            hidden_states: Current hidden state (for standard residual fallback).
            sublayer_hidden_output: Output of sublayer for hidden stream.
            encoder_hidden_states: Current encoder state (may be None for last layer).
            sublayer_encoder_output: Output of sublayer for encoder stream (may be None).

        Returns:
            new_hidden: Updated hidden state.
            new_encoder: Updated encoder state (or None).
        """
        step_idx = state['step_idx']

        # Hidden stream: always use AttnRes
        new_hidden, state['hidden_block_outputs'], state['hidden_partial_block'], \
            state['hidden_block_step_count'] = self.hidden_attn_res(
                hidden_states,
                sublayer_hidden_output,
                step_idx,
                state['hidden_block_outputs'],
                state['hidden_partial_block'],
                state['hidden_block_step_count'],
            )

        # Encoder stream: optionally use AttnRes
        new_encoder = None
        if encoder_hidden_states is not None and sublayer_encoder_output is not None:
            if self.apply_to_encoder:
                new_encoder, state['encoder_block_outputs'], state['encoder_partial_block'], \
                    state['encoder_block_step_count'] = self.encoder_attn_res(
                        encoder_hidden_states,
                        sublayer_encoder_output,
                        step_idx,
                        state['encoder_block_outputs'],
                        state['encoder_partial_block'],
                        state['encoder_block_step_count'],
                    )
            else:
                # Standard residual for encoder
                new_encoder = encoder_hidden_states + sublayer_encoder_output

        state['step_idx'] = step_idx + 1

        return new_hidden, new_encoder
