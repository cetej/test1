# Knihovna 300 promptů (zdroj: CyrilXBT)

## Checkpoint z mobilní session 2026-03-25

### Kontext
- Uživatel sdílel kolekci 300 šablonových promptů od @cyrilXBT
- Projekt: Pyramid Flow (autoregressive video generation, PyTorch, Gradio, multi-GPU)
- Cíl: mít prompty k dispozici jako referenci pro budoucí práci na projektech

---

## Doporučení pro další session

### Ihned použitelné pro Pyramid Flow:

1. **Code Review (#1)** — Provést review `app.py`, `inference_multigpu.py`, `utils.py`
2. **Write Unit Tests (#4)** — Projekt nemá žádné testy, vytvořit základní test suite
3. **Optimize Performance (#5)** — Profilovat inference pipeline, hledat bottlenecky
4. **Write Documentation (#10)** — Zdokumentovat API parametry a konfiguraci modelu
5. **Security Audit (#11)** — Audit Gradio endpointů (app.py je veřejně přístupný)
6. **Code Architecture Review (#17)** — Review DiT pipeline architektury
7. **CI/CD Pipeline (#29)** — Vytvořit GitHub Actions (linting, testy)
8. **AI Monitoring (#68)** — Sledování kvality generovaného videa a GPU paměti
9. **Health Check Endpoint (#43)** — Monitoring stavu modelu a GPU

### Prioritní pořadí:
1. Unit testy (projekt je bez testů)
2. CI/CD pipeline
3. Code review + security audit
4. Dokumentace

---

## Přehled všech 6 kategorií

### Kategorie 1: Coding & Debugging (1–50)
Code review, debugging, refactoring, unit testy, API endpointy, DB optimalizace,
dokumentace, security audit, CLI nástroje, async konverze, DB schéma, regex,
web scraping, architektura, error handling, cron joby, překlad mezi jazyky,
webhooky, rate limiting, middleware, caching, migrace, auth systémy, mock data,
paginace, CI/CD, microservices, retry logika, state machine, queue systémy,
SDK tvorba, React optimalizace, integrační testy, search, notifikace, parsery,
event systémy, file upload, konfigurace, health check, feature flagy, logging,
reporty, validace, plugin systémy, load testing, dashboard backend.

### Kategorie 2: AI Workflows (51–100)
AI agenti, prompt chaining, system prompty, evaluace promptů, RAG systémy,
klasifikace, extrakce dat, multi-agent systémy, evaluační frameworky,
sumarizace, content moderace, Q&A systémy, data enrichment, writing assistant,
feedback loop, document processing, personalizace, AI monitoring, prompt šablony,
human-in-the-loop, knowledge grafy, customer service AI, code review AI,
research assistant, competitive intelligence, meeting intelligence,
contract analysis, sentiment analysis, lead scoring, content recommendation,
anomaly detection, překlady, proposal generation, risk assessment, voice AI,
trend detection, compliance checking, AI onboarding, predictive maintenance,
inventory management, finanční analýza, social media monitoring, tech support,
price optimization, fraud detection, scheduling, quality control, news aggregation,
personalized learning, supply chain intelligence.

### Kategorie 3: Research & Analysis (101–150)
Deep research, competitive analysis, market sizing, steel-manning argumentů,
investiční teze, SWOT, first principles, historické vzory, interpretace dat,
risk analysis, scenario planning, literature review, policy analysis,
technology assessment, business model analysis, causal chains, expert synthesis,
trend analysis, decision frameworks, gap analysis, root cause analysis,
stakeholder analysis, generování hypotéz, analogické uvažování,
mapování předpokladů, second-order effects, benchmarking, customer research,
regulatorní landscape, technology roadmap, mentální modely, pre-mortem,
value chain, network effects, jobs to be done, moat analysis, demografie,
supply & demand, inovace, pricing power, distribuce, brand analysis,
churn analysis, partnership strategy, go-to-market, operations, talent,
platform vs product, seasonalita, exit strategy.

### Kategorie 4: Automation (151–200)
Mapování manuálních procesů, Zapier workflow, email automatizace,
data pipeline, automatizace reportů, lead qualification bot,
social media posting, customer onboarding, invoice processing,
monitoring & alerting, support triage, content publishing,
competitive monitoring, CRM automatizace, contract generation,
inventory reorder, employee onboarding, feedback collection,
finanční reconciliace, knowledge base update, meeting follow-up,
price monitoring, job posting & screening, compliance monitoring,
customer win-back, partner integrace, performance reviews,
document approval, customer health scoring, webhook processing,
sales forecasting, content moderace, IT ticket routing,
subscription management, market research, A/B testing,
expense management, user lifecycle, QA testing, data quality,
partner reporting, customer communication, product analytics,
security scanning, vendor management, LMS, social listening,
release management, grant management, crisis communication.

### Kategorie 5: Content Creation (201–250)
Twitter thready, long-form články, newsletter, YouTube scripty,
LinkedIn posty, email kampaně, product descriptions, case studies,
press release, landing page copy, podcast outline, social media kalendář,
white paper, video ad script, webinář, SEO články, sales emaily,
bio & about page, srovnávací články, how-to guidy, interview otázky,
book summary, opinion piece, FAQ, onboarding emaily, annual report,
thought leadership, event pozvánky, testimonial request, product launch email,
explainer content, community post, pitch deck, awards submission,
research report summary, product update, evergreen content, controversy take,
brand story, re-engagement kampaň, workshop curriculum, investor update,
partnership proposal, referral program, community guidelines, job description,
grant proposal, crisis communication, product roadmap, year in review.

### Kategorie 6: Productivity Systems (251–300)
Daily planning, weekly review, goal setting, meeting effectiveness,
decision making, email management, knowledge management, project management,
habit building, deep work, delegace, content creation systém, osobní finance,
learning systém, networking, reading & notes, morning routine, energy management,
feedback systém, idea management, client management, hiring, sales process,
customer success, team communication, performance management, productivity audit,
quarterly planning, research & synthesis, product development, budget management,
conflict resolution, innovation, vendor selection, crisis management,
training & development, OKR, retrospektivy, dokumentace, offboarding,
content kalendář, partnership management, procurement, risk management,
customer feedback, data governance, brand management, strategic planning,
personal board of directors, life design.
