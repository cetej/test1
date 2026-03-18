# Shared Memory — News & Updates

Tracked findings from `/watch` scans. Only ACTION and WATCH items are recorded here.

## Last Scan

**Date**: 2026-03-18
**Mode**: full
**Sources**: 10 (9 returned, 1 empty)
**Items**: 17 (6 action, 6 watch, 5 info)

## Active Items

### Action Items

1. **Diffusers 0.37.0 requires Python >=3.10.0** — our project uses 3.8.10. Blocks all diffusers upgrades.
   - Source: [diffusers releases](https://github.com/huggingface/diffusers/releases)
   - Impact: CRITICAL for project
   - Status: open

2. **Claude Code Plugin System** — can package orchestration as distributable plugin
   - Source: [Claude Code releases](https://github.com/anthropics/claude-code/releases)
   - Impact: medium for orchestration
   - Status: open

3. **Agent Teams** — native parallel agent coordination (since Feb 2026)
   - Source: [Claude Code releases](https://github.com/anthropics/claude-code/releases)
   - Impact: high for /orchestrate Phase 4
   - Status: open

4. **Claude Code Analytics API** — real cost/usage metrics via API
   - Source: [Anthropic API docs](https://docs.anthropic.com/en/release-notes/overview)
   - Impact: high for /budget skill
   - Status: open

5. **timm 1.0.25** — our project uses 0.6.12, massive version gap
   - Source: [timm PyPI](https://pypi.org/project/timm/)
   - Impact: medium for project
   - Status: open

6. **New hook events** — TaskCompleted, TeammateIdle, HTTP hooks, updatedInput
   - Source: [Claude Code docs](https://code.claude.com/docs/en/skills)
   - Impact: medium for orchestration automation
   - Status: open

### Watch List

1. **Self-Flow** — self-supervised flow matching with Dual-Timestep Scheduling (Mar 2026)
   - Source: [arxiv/aimodels.fyi](https://www.aimodels.fyi/papers/arxiv/self-supervised-flow-matching-scalable-multi-modal)
   - Relevance: directly applicable to Pyramid Flow training

2. **Transition Matching Distillation** — few-step video gen distillation (Jan 2026)
   - Source: [emergentmind](https://www.emergentmind.com/papers/2601.09881)
   - Relevance: inference speedup technique for flow matching models

3. **Modular Diffusers** — composable pipeline blocks + Mellon visual editor
   - Source: [HuggingFace blog](https://huggingface.co/blog/modular-diffusers)
   - Relevance: alternative pipeline architecture

4. **FlexAttention + FlashAttention-4** — on Hopper/Blackwell GPUs
   - Source: [PyTorch blog](https://pytorch.org/blog/)
   - Relevance: attention speedup for DiT

5. **PyTorch 2.10.0** — our project uses 2.1.2 (8 major versions behind)
   - Source: [PyTorch releases](https://github.com/pytorch/pytorch/releases)
   - Relevance: massive performance and feature gap

6. **Wan VACE** — controllable video gen with multiple conditioning modes
   - Source: [diffusers releases](https://github.com/huggingface/diffusers/releases)
   - Relevance: competitive techniques to learn from

## Scan History

### 2026-03-18 — full — 17 items found
- First scan. 6 ACTION, 6 WATCH, 5 INFO.
- Key finding: Python 3.8.10 is becoming a critical blocker for dependency upgrades.
- Reddit returned no results (consider broadening query next time).

## Skipped Sources

<!-- Sources that consistently return nothing useful — skip in future scans -->
- Reddit (r/LocalLLaMA, r/StableDiffusion) — 0 results on first scan. Try broader query next time before skipping.
