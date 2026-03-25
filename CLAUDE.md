# CLAUDE.md

## Project Overview

**Pyramid Flow** is an autoregressive video generation framework based on Flow Matching. It generates high-quality videos (up to 10s at 768p, 24 FPS) by interpolating between latents of different resolutions and noise levels using a single DiT (Diffusion Transformer). The project is a research codebase — not a library — with inference-focused code and a Gradio demo.

Paper: [Pyramidal Flow Matching for Efficient Video Generative Modeling](https://arxiv.org/abs/2410.05954)

## Repository Structure

```
├── app.py                          # Gradio web UI (single GPU)
├── app_multigpu.py                 # Gradio web UI (multi-GPU)
├── inference_multigpu.py           # Multi-GPU inference script
├── utils.py                        # Shared utilities (distributed, image processing, downloads)
├── video_generation_demo.ipynb     # Jupyter notebook demo
├── requirements.txt                # Python dependencies
│
├── pyramid_dit/                    # Core DiT model
│   ├── __init__.py                 # Exports: PyramidDiffusionMMDiT, PyramidDiTForVideoGeneration, SD3TextEncoderWithMask
│   ├── pyramid_dit_for_video_gen_pipeline.py  # Main generation pipeline (generate, generate_i2v)
│   ├── modeling_pyramid_mmdit.py   # Pyramid MM-DiT architecture
│   ├── modeling_mmdit_block.py     # MM-DiT transformer blocks
│   ├── modeling_embedding.py       # Embedding layers
│   ├── modeling_normalization.py   # Normalization layers
│   └── modeling_text_encoder.py    # Text encoder (SD3-based with mask support)
│
├── diffusion_schedulers/           # Diffusion scheduling
│   ├── scheduling_flow_matching.py # PyramidFlowMatchEulerDiscreteScheduler
│   └── scheduling_cosine_ddpm.py   # DDPMCosineScheduler
│
├── video_vae/                      # Video VAE (Causal Video VAE)
│   ├── __init__.py                 # Exports: LPIPSWithDiscriminator, CausalVideoVAE
│   ├── modeling_causal_vae.py      # Main VAE model
│   ├── modeling_enc_dec.py         # Encoder/decoder architecture
│   ├── modeling_causal_conv.py     # Causal convolution layers
│   ├── modeling_block.py           # VAE building blocks
│   ├── modeling_resnet.py          # ResNet blocks for VAE
│   ├── modeling_loss.py            # LPIPS + discriminator loss
│   ├── modeling_lpips.py           # LPIPS perceptual loss
│   ├── modeling_discriminator.py   # Discriminator model
│   └── context_parallel_ops.py     # Context parallelism operations for VAE
│
├── trainer_misc/                   # Training/distributed utilities
│   ├── utils.py                    # Optimizer creation, schedulers, distributed init
│   ├── sp_utils.py                 # Sequence parallelism utilities
│   └── communicate.py              # All-to-all communication primitives
│
├── scripts/                        # Shell/Python launch scripts
│   ├── inference_multigpu.sh       # Launch multi-GPU inference
│   ├── app_multigpu_engine.sh      # Launch multi-GPU Gradio demo
│   └── app_multigpu_engine.py      # Multi-GPU Gradio engine
│
└── assets/                         # Images for README
```

## Tech Stack & Dependencies

- **Python**: 3.8.10
- **PyTorch**: 2.1.2 (with CUDA, bfloat16 support)
- **torchvision**: 0.16.2
- **transformers**: 4.39.3 (Hugging Face, for text encoder)
- **diffusers**: >=0.30.1 (Hugging Face, for video export and utilities)
- **accelerate**: 0.30.0 (Hugging Face, for device management)
- **Gradio**: Used for the web demo (not pinned in requirements.txt)
- **timm**: 0.6.12 (for model hub utilities)
- **einops**: Tensor operations

## Key Concepts

### Model Variants
- **768p** (`diffusion_transformer_768p`): High-resolution, supports up to 10s video at 24 FPS (1280x768)
- **384p** (`diffusion_transformer_384p`): Lower-resolution, supports 5s video at 24 FPS (640x384)

### Precision
- **bf16** is the primary supported dtype. fp16 is NOT supported. fp32 is available as fallback.

### Generation Modes
- **Text-to-video**: `model.generate()` — text prompt to video frames
- **Image-to-video**: `model.generate_i2v()` — input image + text prompt to video frames

### Key Parameters
- `guidance_scale`: Controls visual quality (recommended 7-9 for 768p, 7 for 384p)
- `video_guidance_scale`: Controls motion dynamics (higher = more motion)
- `temp`: Controls video duration (16 = ~5s, 31 = ~10s)
- `num_inference_steps`: Per-stage denoising steps (list of 3 values)

### Memory Optimization
- `cpu_offloading=True` in generate(): Inference with <12GB VRAM
- `model.enable_sequential_cpu_offload()`: Inference with <8GB VRAM
- `model.vae.enable_tiling()`: Always enabled for memory efficiency

### Multi-GPU Support
- Sequence parallelism via `trainer_misc/sp_utils.py` and context parallelism via `utils.py`
- Supports 2 or 4 GPUs for inference
- Uses `torch.distributed` with NCCL backend

## Development Conventions

### Code Style
- No linter or formatter is configured (no pyproject.toml, setup.cfg, or similar)
- Naming: `modeling_*.py` for model components, `scheduling_*.py` for schedulers
- Modules use `__init__.py` to re-export key classes
- Print-based logging with `[INFO]`, `[DEBUG]`, `[WARNING]`, `[ERROR]` prefixes in app code

### Model Weights
- Downloaded from Hugging Face Hub (`rain1011/pyramid-flow-sd3`)
- Stored locally; path configured at runtime
- Not committed to the repository

### No Tests
- There is no test suite in this repository. Validation is done through the Jupyter notebook and Gradio demos.

## Common Tasks

### Running the Gradio Demo
```bash
python app.py
```

### Running Multi-GPU Inference
```bash
CUDA_VISIBLE_DEVICES=0,1 sh scripts/inference_multigpu.sh
```

### Adding a New Model Component
Follow the `modeling_*.py` naming convention and export from the package `__init__.py`.
