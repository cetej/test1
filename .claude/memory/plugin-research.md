# Plugin System Research

**Date**: 2026-03-18
**Status**: Complete

## Findings

Claude Code has a mature plugin system. Skills in `.claude/skills/` can be packaged as distributable plugins.

### Plugin Structure
```
.claude-plugin/
├── plugin.json    (metadata)
├── commands/      (slash commands)
├── agents/        (subagents)
├── skills/        (agent skills)
├── hooks/         (event handlers)
└── .mcp.json      (optional MCP config)
```

### Distribution
- Install: `/plugin install {name}@{marketplace}`
- Host: git repo, GitHub, or URL with `marketplace.json`
- Official marketplace: `anthropics/claude-plugins-official`

### Decision
Our orchestration skills CAN be packaged as a plugin for sharing across projects (test1, NG-ROBOT, etc.). This would be cleaner than copying `.claude/skills/` between repos.

### Next Step
Consider creating a `.claude-plugin/` package for the orchestration system when stabilized. Low priority — current per-repo approach works fine.
