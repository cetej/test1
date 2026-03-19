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
BlockAttentionResidualDualStream = attn_res_mod.BlockAttentionResidualDualStream


class TestBlockAttentionResidual:

    def setup_method(self):
        self.dim = 64
        self.num_layers = 6
        self.block_size = 4
        self.batch_size = 2
        self.seq_len = 16

    def _make_module(self, **kwargs):
        defaults = dict(dim=self.dim, num_layers=self.num_layers, block_size=self.block_size)
        defaults.update(kwargs)
        return BlockAttentionResidual(**defaults)

    def test_init_shapes(self):
        module = self._make_module()
        total_steps = self.num_layers * 2
        assert len(module.query_projs) == total_steps
        assert module.num_blocks == 3  # 12 / 4

    def test_zero_init(self):
        module = self._make_module()
        for proj in module.query_projs:
            assert torch.all(proj.weight == 0)

    def test_uniform_attention_at_init(self):
        module = self._make_module()
        b1 = torch.randn(self.batch_size, self.seq_len, self.dim)
        b2 = torch.randn(self.batch_size, self.seq_len, self.dim)
        result = module._depth_attention([b1, b2], step_idx=0)
        expected = (b1 + b2) / 2.0
        torch.testing.assert_close(result, expected, atol=1e-5, rtol=1e-5)

    def test_single_block_passthrough(self):
        module = self._make_module()
        b = torch.randn(self.batch_size, self.seq_len, self.dim)
        result = module._depth_attention([b], step_idx=0)
        torch.testing.assert_close(result, b)

    def test_block_boundary_tracking(self):
        module = self._make_module(block_size=4)
        hidden = torch.randn(self.batch_size, self.seq_len, self.dim)
        block_outputs = []
        partial = torch.zeros_like(hidden)
        step_count = 0

        for step in range(4):
            out = torch.randn_like(hidden)
            hidden, block_outputs, partial, step_count = module(
                hidden, out, step, block_outputs, partial, step_count
            )

        assert len(block_outputs) == 1
        assert step_count == 0

    def test_full_forward(self):
        module = self._make_module()
        hidden = torch.randn(self.batch_size, self.seq_len, self.dim)
        block_outputs = []
        partial = torch.zeros_like(hidden)
        step_count = 0
        total = self.num_layers * 2

        for step in range(total):
            out = torch.randn_like(hidden)
            hidden, block_outputs, partial, step_count = module(
                hidden, out, step, block_outputs, partial, step_count
            )

        assert hidden.shape == (self.batch_size, self.seq_len, self.dim)
        assert len(block_outputs) == module.num_blocks

    def test_gradient_flow(self):
        module = self._make_module()
        hidden = torch.randn(self.batch_size, self.seq_len, self.dim, requires_grad=True)
        block_outputs = []
        partial = torch.zeros_like(hidden)
        step_count = 0
        total = self.num_layers * 2

        current = hidden
        for step in range(total):
            sublayer_out = current * 0.1
            current, block_outputs, partial, step_count = module(
                current, sublayer_out, step, block_outputs, partial, step_count
            )

        current.sum().backward()
        assert hidden.grad is not None
        assert not torch.all(hidden.grad == 0)

    def test_different_block_sizes(self):
        for bs in [2, 4, 6, 8, 12]:
            module = self._make_module(block_size=bs)
            hidden = torch.randn(self.batch_size, self.seq_len, self.dim)
            block_outputs = []
            partial = torch.zeros_like(hidden)
            step_count = 0

            for step in range(self.num_layers * 2):
                out = torch.randn_like(hidden)
                hidden, block_outputs, partial, step_count = module(
                    hidden, out, step, block_outputs, partial, step_count
                )

            assert hidden.shape == (self.batch_size, self.seq_len, self.dim)

    def test_three_blocks_attention(self):
        """With 3 completed blocks at init, attention should produce equal-weight average."""
        module = self._make_module()
        blocks = [torch.randn(self.batch_size, self.seq_len, self.dim) for _ in range(3)]
        result = module._depth_attention(blocks, step_idx=0)
        expected = sum(blocks) / 3.0
        torch.testing.assert_close(result, expected, atol=1e-5, rtol=1e-5)


class TestDualStream:

    def setup_method(self):
        self.dim = 64
        self.num_layers = 4
        self.block_size = 4
        self.bs = 2
        self.seq = 16
        self.enc = 8

    def test_init_state(self):
        module = BlockAttentionResidualDualStream(
            dim=self.dim, num_layers=self.num_layers, block_size=self.block_size
        )
        h = torch.randn(self.bs, self.seq, self.dim)
        e = torch.randn(self.bs, self.enc, self.dim)
        state = module.init_state(h, e)
        assert state['step_idx'] == 0

    def test_step(self):
        module = BlockAttentionResidualDualStream(
            dim=self.dim, num_layers=self.num_layers, block_size=self.block_size
        )
        h = torch.randn(self.bs, self.seq, self.dim)
        e = torch.randn(self.bs, self.enc, self.dim)
        state = module.init_state(h, e)

        sh = torch.randn_like(h)
        se = torch.randn_like(e)
        new_h, new_e = module.step(state, h, sh, e, se)
        assert state['step_idx'] == 1
        assert new_h.shape == h.shape
        assert new_e.shape == e.shape


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
