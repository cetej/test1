"""
Block Attention Residuals (Block AttnRes)

Based on: "Attention Residuals" by Kimi Team (Moonshot AI), arXiv:2603.15031

Replaces fixed-weight residual accumulation (PreNorm dilution) with learned,
input-dependent depth-wise softmax attention over block-level representations.

Standard residual:  h_l = h_{l-1} + f_l(h_{l-1})
AttnRes:            h_l = sum_i alpha_{i->l} * v_i
Block AttnRes:      Partition layers into blocks; within blocks use standard
                    residuals, between blocks use depth-wise softmax attention.

This implementation operates at block boundaries: groups of transformer layers
form blocks with standard residuals internally. At each boundary, depth-wise
attention aggregates all previous block outputs to produce the hidden state
for the next block.
"""

import torch
import torch.nn as nn
from typing import List

from .modeling_normalization import RMSNorm


class BlockAttentionResidual(nn.Module):
    """
    Block Attention Residual module for depth-wise attention aggregation.

    Transformer layers are grouped into blocks (e.g. 4 layers per block).
    Within each block, standard residual connections are used. At block
    boundaries, all previous block outputs are aggregated via learned
    depth-wise softmax attention to produce the input for the next block.

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
        self.layers_per_block = block_size // 2

        # Number of block boundaries during the forward pass
        self.num_boundaries = (num_layers + self.layers_per_block - 1) // self.layers_per_block

        # Per-boundary pseudo-query projection: projects normalized block
        # outputs to scalar logits for depth-wise attention.
        self.query_projs = nn.ModuleList([
            nn.Linear(dim, 1, bias=False) for _ in range(self.num_boundaries)
        ])

        # RMSNorm applied to stacked block representations before projection
        self.depth_norm = RMSNorm(dim, eps=eps, elementwise_affine=False)

        # Initialize all pseudo-query vectors to zero (ensures uniform
        # attention at start of training, reducing to equal-weight average)
        self._init_weights()

    def _init_weights(self):
        for proj in self.query_projs:
            nn.init.zeros_(proj.weight)

    def depth_attention(
        self,
        block_outputs: List[torch.Tensor],
        boundary_idx: int,
    ) -> torch.Tensor:
        """
        Compute softmax attention over block-level representations.

        Args:
            block_outputs: List of N block outputs, each [B, T, D].
            boundary_idx: Index of the current boundary for selecting query proj.

        Returns:
            Aggregated hidden state [B, T, D].
        """
        if len(block_outputs) == 1:
            return block_outputs[0]

        # Stack block outputs: [N, B, T, D]
        V = torch.stack(block_outputs, dim=0)

        # Normalize for computing attention logits
        K = self.depth_norm(V)  # [N, B, T, D]

        # Compute scalar logits per block using pseudo-query projection
        proj = self.query_projs[boundary_idx]
        logits = proj(K).squeeze(-1)  # [N, B, T]

        # Softmax over depth dimension (dim=0)
        alpha = torch.softmax(logits, dim=0)  # [N, B, T]

        # Weighted aggregation: [N, B, T] x [N, B, T, D] -> [B, T, D]
        return torch.einsum('n b t, n b t d -> b t d', alpha, V)
