"""
Tests for Block Attention Residuals implementation.
Isolated imports to avoid heavy dependency chain.
"""

import torch
import torch.nn as nn
import pytest
import sys
import os
import importlib
import importlib.util


def _load_module(name, path):
    """Load a single module from file path without triggering package __init__."""
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


# Load normalization first (dependency of attn_residual)
_base = os.path.join(os.path.dirname(__file__), '..', 'pyramid_dit')

# Stub the diffusers dependency for normalization module
import types
diffusers_stub = types.ModuleType('diffusers')
diffusers_utils_stub = types.ModuleType('diffusers.utils')
diffusers_utils_stub.is_torch_version = lambda *a, **k: True
diffusers_stub.utils = diffusers_utils_stub
sys.modules.setdefault('diffusers', diffusers_stub)
sys.modules.setdefault('diffusers.utils', diffusers_utils_stub)

norm_mod = _load_module(
    'pyramid_dit.modeling_normalization',
    os.path.join(_base, 'modeling_normalization.py')
)

# Now load the attn_residual module
attn_res_mod = _load_module(
    'pyramid_dit.modeling_attn_residual',
    os.path.join(_base, 'modeling_attn_residual.py')
)

BlockAttentionResidual = attn_res_mod.BlockAttentionResidual


class TestBlockAttentionResidual:

    def setup_method(self):
        self.dim = 64
        self.num_layers = 12
        self.block_size = 8  # 4 layers per block
        self.batch_size = 2
        self.seq_len = 16

    def _make_module(self, **kwargs):
        defaults = dict(dim=self.dim, num_layers=self.num_layers, block_size=self.block_size)
        defaults.update(kwargs)
        return BlockAttentionResidual(**defaults)

    def test_init_shapes(self):
        module = self._make_module()
        assert module.layers_per_block == 4
        assert module.num_boundaries == 3  # 12 layers / 4 per block
        assert len(module.query_projs) == 3

    def test_zero_init(self):
        module = self._make_module()
        for proj in module.query_projs:
            assert torch.all(proj.weight == 0)

    def test_uniform_attention_at_init(self):
        """With zero-init weights, depth attention should produce equal-weight average."""
        module = self._make_module()
        b1 = torch.randn(self.batch_size, self.seq_len, self.dim)
        b2 = torch.randn(self.batch_size, self.seq_len, self.dim)
        result = module.depth_attention([b1, b2], boundary_idx=0)
        expected = (b1 + b2) / 2.0
        torch.testing.assert_close(result, expected, atol=1e-5, rtol=1e-5)

    def test_single_block_passthrough(self):
        """With only one block, depth_attention should return it unchanged."""
        module = self._make_module()
        b = torch.randn(self.batch_size, self.seq_len, self.dim)
        result = module.depth_attention([b], boundary_idx=0)
        torch.testing.assert_close(result, b)

    def test_three_blocks_attention(self):
        """With 3 blocks at init, should produce equal-weight average."""
        module = self._make_module()
        blocks = [torch.randn(self.batch_size, self.seq_len, self.dim) for _ in range(3)]
        result = module.depth_attention(blocks, boundary_idx=0)
        expected = sum(blocks) / 3.0
        torch.testing.assert_close(result, expected, atol=1e-5, rtol=1e-5)

    def test_boundary_simulation(self):
        """Simulate the orchestrator loop: run layers, aggregate at boundaries."""
        module = self._make_module()  # 12 layers, 4 per block
        hidden = torch.randn(self.batch_size, self.seq_len, self.dim)

        block_outputs = []
        layers_in_block = 0
        boundary_idx = 0

        for i_layer in range(self.num_layers):
            # Simulate a transformer layer (just add noise)
            hidden = hidden + torch.randn_like(hidden) * 0.1
            layers_in_block += 1

            is_boundary = (layers_in_block >= module.layers_per_block) or (i_layer == self.num_layers - 1)
            if is_boundary:
                block_outputs.append(hidden)
                hidden = module.depth_attention(block_outputs, boundary_idx)
                boundary_idx += 1
                layers_in_block = 0

        assert hidden.shape == (self.batch_size, self.seq_len, self.dim)
        assert len(block_outputs) == 3
        assert boundary_idx == 3

    def test_gradient_flow(self):
        """Gradients should flow through depth attention back to input."""
        module = self._make_module()
        hidden = torch.randn(self.batch_size, self.seq_len, self.dim, requires_grad=True)

        block_outputs = []
        layers_in_block = 0
        boundary_idx = 0
        current = hidden

        for i_layer in range(self.num_layers):
            current = current + current * 0.1  # differentiable "layer"
            layers_in_block += 1

            is_boundary = (layers_in_block >= module.layers_per_block) or (i_layer == self.num_layers - 1)
            if is_boundary:
                block_outputs.append(current)
                current = module.depth_attention(block_outputs, boundary_idx)
                boundary_idx += 1
                layers_in_block = 0

        current.sum().backward()
        assert hidden.grad is not None
        assert not torch.all(hidden.grad == 0)

    def test_different_block_sizes(self):
        """Module should work with various block sizes."""
        for bs in [2, 4, 6, 8, 12]:
            module = self._make_module(block_size=bs)
            layers_per_block = bs // 2
            expected_boundaries = (self.num_layers + layers_per_block - 1) // layers_per_block
            assert module.num_boundaries == expected_boundaries
            assert len(module.query_projs) == expected_boundaries

    def test_different_boundary_indices_use_different_projs(self):
        """Each boundary should use its own projection."""
        module = self._make_module()
        # Set different weight vectors for each proj so they produce different logits
        torch.manual_seed(42)
        for i, proj in enumerate(module.query_projs):
            proj.weight.data = torch.randn_like(proj.weight) * (i + 1)

        blocks = [torch.randn(1, 4, self.dim), torch.randn(1, 4, self.dim)]

        r0 = module.depth_attention(blocks, boundary_idx=0)
        r1 = module.depth_attention(blocks, boundary_idx=1)
        # Different projections -> different attention weights -> different results
        assert not torch.allclose(r0, r1)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
