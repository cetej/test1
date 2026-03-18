# CLAUDE.md

## Project Overview

**Pyramid Flow** is an autoregressive video generation model based on Flow Matching. It generates high-quality videos (up to 10s at 768p, 24 FPS) by interpolating between latents of different resolutions and noise levels using a single DiT (Diffusion Transformer). Licensed under MIT.

- **Paper**: https://arxiv.org/abs/2410.05954
- **Model**: https://huggingface.co/rain1011/pyramid-flow-sd3
- **Language**: Python 3.8.10
- **Framework**: PyTorch 2.1.2

## Repository Structure

```
├── pyramid_dit/              # Core DiT model
│   ├── __init__.py           # Exports PyramidDiffusionMMDiT, PyramidDiTForVideoGeneration, SD3TextEncoderWithMask
│   ├── pyramid_dit_for_video_gen_pipeline.py  # Main generation pipeline (text-to-video, image-to-video)
│   ├── modeling_pyramid_mmdit.py              # MM-DiT architecture
│   ├── modeling_mmdit_block.py                # Transformer block components
│   ├── modeling_embedding.py                  # Positional/patch embeddings
│   ├── modeling_normalization.py              # Normalization layers
│   └── modeling_text_encoder.py               # SD3 text encoder with mask support
├── video_vae/                # Causal Video VAE for encoding/decoding
│   ├── __init__.py           # Exports CausalVideoVAE, LPIPSWithDiscriminator
│   ├── modeling_causal_vae.py                 # Main VAE model
│   ├── modeling_enc_dec.py                    # Encoder/decoder architecture
│   ├── modeling_causal_conv.py                # Causal convolution layers
│   ├── modeling_block.py                      # VAE building blocks
│   ├── modeling_resnet.py                     # ResNet blocks
│   ├── modeling_loss.py                       # LPIPS + discriminator losses
│   ├── modeling_lpips.py                      # Perceptual loss
│   ├── modeling_discriminator.py              # Discriminator for VAE training
│   └── context_parallel_ops.py                # Context parallelism operations
├── diffusion_schedulers/     # Noise scheduling
│   ├── scheduling_flow_matching.py            # Pyramid flow matching (Euler discrete)
│   └── scheduling_cosine_ddpm.py              # Cosine DDPM scheduler
├── trainer_misc/             # Training & distributed utilities
│   ├── utils.py              # Optimizer creation, distributed init, LR schedulers
│   ├── sp_utils.py           # Sequence parallelism group management
│   └── communicate.py        # All-to-all communication ops
├── scripts/                  # Multi-GPU inference scripts
│   ├── inference_multigpu.sh                  # CLI for multi-GPU inference
│   ├── app_multigpu_engine.py                 # Multi-GPU Gradio engine
│   └── app_multigpu_engine.sh                 # Launcher for multi-GPU Gradio
├── assets/                   # Example images for demos
├── app.py                    # Single-GPU Gradio web UI
├── app_multigpu.py           # Multi-GPU Gradio launcher
├── inference_multigpu.py     # Multi-GPU inference entry point
├── utils.py                  # General utility functions
├── video_generation_demo.ipynb  # Jupyter notebook demo
├── requirements.txt          # Python dependencies
└── LICENSE                   # MIT License
```

## Setup

```bash
conda create -n pyramid python==3.8.10
conda activate pyramid
pip install -r requirements.txt
```

Download model checkpoint:
```python
from huggingface_hub import snapshot_download
snapshot_download("rain1011/pyramid-flow-sd3", local_dir="PATH", local_dir_use_symlinks=False, repo_type='model')
```

## Key Entry Points

| Task | Command / File |
|------|---------------|
| Gradio demo (single GPU) | `python app.py` |
| Multi-GPU inference | `CUDA_VISIBLE_DEVICES=0,1 sh scripts/inference_multigpu.sh` |
| Multi-GPU Gradio | `sh scripts/app_multigpu_engine.sh` |
| Notebook demo | `video_generation_demo.ipynb` |

## Architecture & Key Concepts

- **PyramidDiTForVideoGeneration** (`pyramid_dit/pyramid_dit_for_video_gen_pipeline.py`): Main pipeline class. Orchestrates text encoding, DiT denoising, and VAE decoding. Exposes `generate()` for text-to-video and `generate_i2v()` for image-to-video.
- **PyramidDiffusionMMDiT** (`pyramid_dit/modeling_pyramid_mmdit.py`): The core multi-modal DiT model that processes text and visual tokens jointly.
- **CausalVideoVAE** (`video_vae/modeling_causal_vae.py`): Causal video autoencoder. Supports `enable_tiling()` for memory-efficient decoding.
- **Flow Matching Scheduler** (`diffusion_schedulers/scheduling_flow_matching.py`): Implements the pyramid flow matching strategy with Euler discrete steps.
- **Sequence Parallelism** (`trainer_misc/sp_utils.py`): Distributes sequence dimension across GPUs for multi-GPU inference. Supports 2 or 4 GPUs.

## Model Variants

| Variant | Resolution | Max Duration | Config Directory |
|---------|-----------|-------------|-----------------|
| 768p | 1280x768 | 10s (temp=31) | `diffusion_transformer_768p` |
| 384p | 640x384 | 5s (temp=16) | `diffusion_transformer_384p` |

## Important Parameters

- `guidance_scale`: Controls visual quality (7-9 for 768p, 7 for 384p)
- `video_guidance_scale`: Controls motion dynamics (higher = more motion)
- `temp`: Controls video duration (16 = ~5s, 31 = ~10s at 768p)
- `model_dtype`: Only `bf16` is fully supported; `fp16` is not supported
- `save_memory=True`: Enables memory-efficient VAE decoding
- `cpu_offloading=True`: Enables CPU offloading (<12GB VRAM)
- `model.enable_sequential_cpu_offload()`: Even lower VRAM usage (<8GB)

## Orchestration System

This project includes a multi-agent orchestration system in `.claude/skills/` with shared memory in `.claude/memory/`.

### When to use orchestration automatically

- **Use `/orchestrate`** when the task has 3+ steps, touches multiple files/modules, has unknown scope, or requires research before implementation
- **Work directly** when the task is a single-step edit, a simple question, or a clearly scoped change to 1-2 files

When in doubt, prefer orchestration — the overhead is small but the quality improvement is significant.

### Available skills

| Skill | Role | When to use |
|-------|------|-------------|
| `/orchestrate` | Conductor — decomposes, delegates, coordinates | Complex or multi-step tasks |
| `/scout` | Explorer — maps codebase context | Before implementing changes in unfamiliar code |
| `/critic` | Reviewer — evaluates quality | After implementation, before finalizing |
| `/scribe` | Recorder — maintains shared memory | After decisions or task completion |
| `/skill-generator` | Creator — builds new skills | When a repeatable pattern has no skill yet |
| `/budget` | Cost controller — tracks and limits resource usage | Before expensive operations, or to check status |
| `/watch` | News scanner — tracks updates in AI/ML ecosystem | Weekly, or when asking "what's new" |

### Cost control

Every orchestrated task is assigned a **complexity tier** (light / standard / deep) that sets hard limits on agent spawns, critic iterations, and scout depth. The budget is tracked in `.claude/memory/budget.md`.

| Tier | Agent spawns | Critic rounds | When |
|------|-------------|---------------|------|
| light | 0-1 | 1 | Single file, known pattern |
| standard | 2-4 | 2 | Multi-file, some exploration |
| deep | 5-8 | 3 | Cross-cutting, major feature |

**Default to light tier.** Upgrade only when scouting reveals higher complexity. Circuit breakers stop execution if limits are hit — the user decides whether to extend.

### Shared memory

Always check `.claude/memory/learnings.md` before starting work — it contains accumulated patterns and anti-patterns from previous tasks. After completing work, record learnings and decisions via `/scribe`.

## Code Conventions

- **Naming**: Modules follow `modeling_*.py` pattern for model components, `scheduling_*.py` for schedulers
- **No test suite**: The project has no automated tests
- **No linter config**: No `.flake8`, `pyproject.toml`, or similar linting configuration
- **No CI/CD**: No GitHub Actions or similar pipelines configured
- **Dtype**: Always use `torch.bfloat16`; fp16 is not supported
- **Device management**: Use `torch.cuda.set_device()` before inference; CPU offloading is handled by the pipeline
- **Imports**: Core classes are re-exported through `__init__.py` in each package

## Dependencies (Key)

- `torch==2.1.2`, `torchvision==0.16.2`
- `transformers==4.39.3` (Hugging Face)
- `diffusers>=0.30.1` (for `export_to_video` and scheduler base classes)
- `accelerate==0.30.0` (for device management and offloading)
- `einops`, `timm==0.6.12` (tensor operations and vision models)
- `gradio` (web UI, installed separately)
