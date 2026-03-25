# Pyramid Flow - Project Notes

## Prompt Library
- Soubor `prompts-library.md` obsahuje katalog 300 šablonových promptů (6 kategorií po 50)
- Při práci na projektu zkontroluj relevantní sekci a nabídni uživateli aplikaci vhodných promptů
- Prioritní oblasti pro tento projekt: unit testy, CI/CD, code review, security audit, dokumentace

## Project Context
- Pyramid Flow: autoregressive video generation (PyTorch, Flow Matching, DiT)
- Gradio web app (`app.py`), multi-GPU inference (`inference_multigpu.py`)
- Model: rain1011/pyramid-flow-sd3 (Hugging Face)
- Podporuje 768p/384p, 5-10s video, 24 FPS

## Known Gaps (as of 2026-03-25)
- Žádné unit testy
- Žádná CI/CD pipeline
- Security audit Gradio endpointů nebyl proveden
