# Analýza: OS-Themis – A Scalable Critic Framework for Generalist GUI Rewards

**arXiv:** [2603.19191](https://arxiv.org/abs/2603.19191v1)
**GitHub:** [OS-Copilot/OS-Themis](https://github.com/OS-Copilot/OS-Themis)
**Datum publikace:** 19. března 2026
**Autoři:** Zehao Li, Zhenyu Wu, Yibo Zhao, Bowen Yang, Jingjing Xie et al. (USTC, Shanghai AI Lab, CUHK MMLab, HKUST, NUS)
**Licence:** Apache 2.0

## 1. Problém

Reinforcement Learning (RL) může zlepšit robustnost GUI agentů ve stochastických prostředích, ale trénink je extrémně citlivý na kvalitu reward funkce. Existující přístupy mají tři hlavní omezení:

1. **Rule-based rewards** – spoléhají na manuální heuristiky, mají vysokou přesnost, ale špatně škálují a jsou náchylné k reward hackingu
2. **Training-based critics** – vyžadují drahá anotovaná data a špatně generalizují na out-of-distribution prostředí
3. **LLM-as-a-judge** – flexibilní, ale trpí halucinacemi a povrchním hodnocením při zpracování celé trajektorie najednou

## 2. Řešení: Multi-agentní architektura

OS-Themis dekompozuje hodnocení trajektorií na 4 specializované agenty:

| Agent | Role |
|-------|------|
| **Selector** | Identifikuje nejdůležitější kroky v trajektorii (milestone extraction) |
| **Verifier** | Vizuálně ověřuje vybrané kroky pomocí screenshotů |
| **Reviewer** | Hledá rizikové body – chybějící save/submit akce, skryté selhání maskované triviálními úspěchy |
| **Judge** | Finální verdikt (completed / not_completed) na základě celého řetězce důkazů |

### Dvoustupňový proces

1. **Milestone Verification Module** (Selector + Verifier) – granulární ověřování klíčových milníků, izolace relevantních signálů od šumu
2. **Verdict Calibration Module** (Reviewer + Judge) – audit důkazního řetězce, korekce příliš optimistických hodnocení

### Konfigurace

- Backbone model: Qwen3-VL-235B (stejný model pro všechny 4 role)
- Selector rounds: 6, Reviewer rounds: 2
- Temperature: 0, max tokens: 8192

## 3. Benchmark: OmniGUIRewardBench (OGRBench)

Cross-platform benchmark pokrývající 5 GUI platforem: Ubuntu, Mobile, Windows, macOS, Web.

| Model | Accuracy | Precision | Recall |
|-------|----------|-----------|--------|
| **Qwen3-VL-235B** | **88.0 %** | 92.8 % | 82.3 % |
| Gemini-3-Flash | 86.2 % | 93.2 % | 78.0 % |
| GPT-5 | 82.9 % | 93.4 % | 70.6 % |
| Qwen3-VL-235B-Thinking | 85.2 % | 89.3 % | 79.9 % |

Průměr přes všechny testované modely: 81.6 % accuracy, 90.9 % precision, 70.4 % recall.

## 4. Klíčové experimentální výsledky (AndroidWorld)

- **+10.3 %** zlepšení při online RL tréninku (pilotní studie s Qwen3-VL-4B, GRPO algoritmus, 1024 trénovacích úloh, 4 trajektorie na úlohu, KL regularizace kl_coef = 0.005)
- **+6.9 %** zlepšení při filtrování trajektorií v self-training smyčce
- Všechny testované modely dosahují svého nejlepšího výkonu právě pod OS-Themis

## 5. Použitelné nápady pro naše projekty

### Pro Pyramid Flow (video generování)

| Nápad | Obtížnost | Dopad | Priorita |
|-------|-----------|-------|----------|
| Multi-agent video quality eval | Střední | Vysoký | **1** |
| RL fine-tuning s critic reward | Vysoká | Velmi vysoký | **2** |
| Self-training data filtering | Nízká | Střední | **3** |
| Milestone keyframe evaluation | Nízká | Střední | **4** |

#### Multi-agentní hodnocení kvality videa
Místo jedné metriky (FVD, FID) nasadit pipeline agentů: jeden hodnotí vizuální kvalitu klíčových snímků, druhý plynulost pohybu, třetí soulad s promptem, čtvrtý dává finální verdikt. Reviewer agent odhaluje false positives (video vypadá dobře, ale má artefakty v pohybu nebo nesoulad s textem).

#### Milestone-based evaluace pro autoregresivní generování
Pyramid Flow generuje video autoregresivně po pyramidálních úrovních. Evaluovat kvalitu na klíčových snímcích (keyframes) mezi rozlišovacími úrovněmi místo hodnocení všech framů.

#### RL fine-tuning s lepším reward modelem
Multi-agentní critic jako reward model pro RLHF/GRPO fine-tuning. Místo binárního "dobré/špatné" → granulární reward na úrovni jednotlivých aspektů (text alignment, motion quality, visual fidelity). GRPO setup z paperu (4 trajektorie na úlohu, KL regularizace) je přímo aplikovatelný.

#### Self-training filtrování dat
Multi-agentní evaluace k filtrování syntetických/generovaných trénovacích dat. Automatické vyřazení nekvalitních vzorků při škálování tréninku na větší datasety.

### Pro Seznam.cz kontext

- **Kvalita vyhledávání** – multi-agentní hodnocení relevance výsledků (relevance, čerstvost, lokální kontext, kalibrace)
- **AI content moderation** – dekomponovaná evaluace pro automatický fact-checking zpráv (navazuje na fact-checking iniciativu s Demagog.cz)

---

*Zpracováno: březen 2026*
