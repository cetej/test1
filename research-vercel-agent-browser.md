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

## Conclusion

**agent-browser is NOT a Playwright replacement.** It is a complementary tool optimized for AI coding agents that need to verify UI with minimal context window consumption. For full E2E testing, cross-browser support, and production test suites, Playwright remains the better choice.

## Sources

- https://github.com/vercel-labs/agent-browser
- https://www.npmjs.com/package/agent-browser
- https://pub.towardsai.net/vercel-just-solved-browser-automation-for-ai-agents-b3414ebdb4d7
- https://dev.to/chen_zhang_bac430bc7f6b95/why-vercels-agent-browser-is-winning-the-token-efficiency-war-for-ai-browser-automation-4p87
