# Research: MiroFish — AI Social Prediction Engine

## Overview

MiroFish is an open-source AI prediction engine built by **Guo Hangjiang** ("Baifu"), a 20-year-old senior at Beijing University of Posts and Telecommunications. He built it in 10 days using Python. The project hit #1 on GitHub's global trending list in March 2026 and accumulated 33,000+ stars.

- **GitHub:** https://github.com/666ghj/MiroFish
- **License:** AGPL (open source)
- **Investment:** 30 million yuan (~$4.1M) from Chen Tianqiao (founder of Shanda Group) within 24 hours of the first demo

## How It Works — 5-Stage Pipeline

### 1. Knowledge Graph Construction (GraphRAG)
Input document (news article, financial report, policy draft, novel) is processed by GraphRAG. The system extracts entities (people, organizations, events, concepts) and their relationships to build a structured knowledge graph.

### 2. Agent Generation
From the graph, thousands of AI agent personas are generated. Each agent gets:
- Unique personality and background
- Initial stance on the topic
- Social relationships with other agents
- Individual and group memory structures

### 3. Environment Setup
Based on the knowledge graph, simulation parameters are automatically configured. An environment-configuration agent injects parameters to initialize the virtual world.

### 4. Simulation Execution
Agents interact on two simulated platforms (Twitter-like and Reddit-like). They post, comment, debate, form opinions, and influence each other. New variables can be injected at runtime (e.g., "Fed cuts rates by 50 basis points") to observe how the digital world reorganizes.

### 5. Report Generation
A ReportAgent analyzes all simulation data and outputs a structured prediction report covering turning points in public opinion, key influencing factors, and sentiment trends.

## Technology Stack

| Component | Technology |
|-----------|-----------|
| Simulation Engine | OASIS (Open Agent Social Interaction Simulations) by CAMEL-AI — up to 1M agents, 23 social interaction types |
| Knowledge Graphs | GraphRAG |
| LLM | Any OpenAI SDK-compatible model (Qwen-plus recommended) |
| Language | Python |
| Graph Database | Neo4j (in offline fork) |
| Local LLM | Ollama (in offline fork) |

### Offline Fork
- [MiroFish-Offline](https://github.com/nikmcfly/MiroFish-Offline) — English fork with Neo4j + Ollama local stack

## Demo Cases

1. **Dream of the Red Chamber** — Fed first 80 chapters of the classic Chinese novel; agents predicted the missing ending with multiple narrative branches
2. **Federal Reserve rate simulation** — Simulated reactions of retail investors, institutions, and analysts; tracked sentiment convergence
3. **Polymarket trading bot** — One developer simulated 2,847 digital humans before every trade, reported $4,266 profit over 338 trades

## Predecessor: BettaFish
Guo's first project (end of 2025) was BettaFish, a multi-agent sentiment analyzer that also topped GitHub trending with 20,000 stars in a week.

## Limitations

- **No benchmarks** comparing predictions to real-world outcomes
- **High API costs** — running thousands of LLM agents is expensive
- **Inherited biases** from LLM training data
- **Herd behavior** — research shows LLM agents are more susceptible to herd behavior than real humans (agents polarize faster)
- **Not validated** — demonstrations show methodology, not accuracy proof

## Replication Feasibility

All components are open-source or publicly available:

1. **GraphRAG** — Microsoft has an open-source implementation
2. **OASIS** — Open-source framework from CAMEL-AI
3. **LLM** — Any OpenAI-compatible API, or local via Ollama
4. **Neo4j** — Open-source graph database
5. **MiroFish itself** — AGPL licensed, can be forked directly

The entire project can be cloned and run locally with the offline fork using Ollama for the LLM and Neo4j for the graph database.

## Sources

- [PANews — Guo Hangjiang story](https://www.panewslab.com/en/articles/019cf53a-ca7c-7159-9fbc-40859cdfa108)
- [DEV Community — MiroFish overview](https://dev.to/arshtechpro/mirofish-the-open-source-ai-engine-that-builds-digital-worlds-to-predict-the-future-ki8)
- [Judy AI Lab — MiroFish analysis](https://judyailab.com/en/posts/mirofish-multi-agent-prediction/)
- [TMTPOST — AI Product Tops GitHub](https://en.tmtpost.com/post/7905996)
- [Medium — MiroFish Swarm Intelligence](https://agentnativedev.medium.com/mirofish-swarm-intelligence-with-1m-agents-that-can-predict-everything-114296323663)
- [blocmates — What is MiroFish](https://www.blocmates.com/articles/what-is-mirofish-the-agent-engine-that-can-predict-anything-and-everything)
- [emelia.io — MiroFish AI Swarm Engine](https://emelia.io/hub/mirofish-ai-swarm-prediction)
