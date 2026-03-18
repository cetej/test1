# Research Findings

**Date**: 2026-03-18

## 1. Transition Matching Distillation (TMD)

**Source**: arXiv 2601.09881 (NVIDIA Research)
**Verdict**: HIGH potential speedup (3-5x), but requires FULL RETRAINING

- Hierarchical approach: few outer transition steps + multiple inner flow refinement steps
- Requires teacher-student distillation training (not inference-only)
- Architecture surgery: split DiT into main backbone + flow head
- Only practical if retraining is planned anyway
- **Recommendation**: WATCH — revisit when compute is available for retraining

## 2. Modular Diffusers

**Source**: HuggingFace blog, diffusers v0.37.0+
**Verdict**: Interesting but NOT URGENT

- New composable pipeline framework (ModularPipeline, blocks, visual debugging)
- Introduced in diffusers 0.37.0 (experimental)
- Migration effort: 2-4 weeks full, 1 week hybrid
- Pyramid's multi-GPU sequence parallelism would need major refactoring
- **Recommendation**: HYBRID approach — keep current pipeline, optionally create modular version later
- **Note**: We pinned diffusers at 0.35.2, so Modular Diffusers is not available yet

## 3. Self-Flow Paper

**Status**: Pending (agent still running)

## 4. Plugin System

**Verdict**: Available and mature

- Claude Code supports distributable plugins via `.claude-plugin/` structure
- Skills can be packaged as plugins for cross-project sharing
- Official marketplace: anthropics/claude-plugins-official
- **Recommendation**: LOW priority — current per-repo approach works fine
