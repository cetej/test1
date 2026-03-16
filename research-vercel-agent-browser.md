# Vercel Agent Browser vs Playwright — Research

## What is agent-browser?

- **Package**: `agent-browser` (npm), **Repo**: `vercel-labs/agent-browser`
- CLI tool for browser automation designed specifically for AI coding agents (Claude Code, Cursor, Codex, Gemini CLI)
- Released around January 2026 (currently v0.4.x)
- Architecture: Rust CLI + Node.js daemon using Playwright under the hood

## How it works

```bash
agent-browser open <url>          # navigate to a page
agent-browser snapshot -i         # compact list of interactive elements (@e1, @e2...)
agent-browser click @e1           # interact by ref
agent-browser fill @e2 "text"     # fill input by ref
```

## Key advantage: Token/context efficiency

- **82-93% less context usage** than Playwright MCP on the same tasks
- 6 tests: ~5.5K chars (agent-browser) vs ~31K chars (Playwright MCP) — 5.7x more efficient
- Successful click returns "Done" (6 chars) vs full page state in Playwright MCP
- Typical page snapshot: 200-400 tokens vs thousands with Playwright MCP

## Comparison

| Aspect | agent-browser | Playwright |
|---|---|---|
| Purpose | AI agent browser control | General browser automation & testing |
| Interface | CLI commands | API / MCP protocol |
| Token efficiency | Very high (82-93% less) | Lower (full accessibility trees) |
| Element selection | Semantic refs (@e1, @e2) | CSS selectors, XPath, ARIA |
| Cross-browser | Chrome only | Chrome, Firefox, WebKit, Edge |
| Network interception | No | Yes |
| Multi-tab | Limited | Yes |
| PDF generation | No | Yes |
| Trace/video recording | Basic | Full support |
| Test script generation | No | Yes |
| Maturity | Early (v0.4.x) | Mature |
| Windows support | Broken | Full |

## Scaling & practical cost analysis

### Token cost savings at scale

| Scale | Playwright MCP cost | agent-browser cost | Savings |
|-------|--------------------|--------------------|---------|
| 100 tasks/day | ~$2.34/day | ~$0.42/day | ~$1.92/day |
| 1,000 tasks/day | ~$23.40/day | ~$4.20/day | ~$19.20/day |
| 10,000 tasks/day | ~$234/day | ~$42/day | ~$192/day |

The real win is not dollars — it is **context window space**. A single screenshot = 15,000+ tokens. In multi-step browser tasks, Playwright MCP can exhaust the context window in a few steps. agent-browser keeps long autonomous sessions viable.

### Scaling readiness (as of March 2026)

- **154 open issues**, project is ~2 months old
- **Parallel execution is undocumented** — DIY infrastructure required
- **Windows support is broken**
- **CI/CD**: Works headless-first, auto-detects Docker/K8s, but no dedicated CI docs
- **Cloud scaling path**: Connect to Browserbase, Browserless, or Vercel Sandbox (beta)

### Best use cases

- AI coding agent verification loops (build → check in browser → fix → repeat)
- Smoke testing during development
- Form filling and basic interaction testing (~90s for 30 fields)

### Poor fit for

- Production E2E test suites (no test runner, assertions, or reporting)
- Web scraping (4.3x slower, 7.4x more memory than traditional scrapers)
- Cross-browser testing (Chrome only)

### Alternatives for scaled production

| Tool | Best for | Maturity |
|------|---------|----------|
| **Stagehand + Browserbase** | Production AI automation | Most production-ready |
| **Browser Use** | Python ecosystem, autonomous agents | Mature (50K+ stars) |
| **agent-browser** | Dev-loop verification, token savings | Young (~2 months) |
| **Playwright MCP** | Full E2E testing, debugging | Most mature |

### Verdict

For "AI agent verifies its own work in browser" — **yes, worth it, token savings are real**. For scaling to thousands of production tests — **not ready yet**. Stagehand + Browserbase is the safer bet today. Emerging consensus: use Playwright for 80% of predictable steps, AI tools for the 20% requiring adaptability.

## Conclusion

**agent-browser is NOT a Playwright replacement.** It is a complementary tool optimized for AI coding agents that need to verify UI with minimal context window consumption. For full E2E testing, cross-browser support, and production test suites, Playwright remains the better choice.

## Sources

- https://github.com/vercel-labs/agent-browser
- https://www.npmjs.com/package/agent-browser
- https://pub.towardsai.net/vercel-just-solved-browser-automation-for-ai-agents-b3414ebdb4d7
- https://dev.to/chen_zhang_bac430bc7f6b95/why-vercels-agent-browser-is-winning-the-token-efficiency-war-for-ai-browser-automation-4p87
