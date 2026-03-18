# Shared Memory — Learnings

Accumulated knowledge from all tasks. Used by all skills/agents to improve over time.

## Patterns

### Budget-First Orchestration
- **Context**: When orchestrating any multi-step task
- **Pattern**: Assign complexity tier BEFORE scouting. Start with lowest viable tier. Upgrade only if scout reveals higher complexity. Always tell the user when upgrading.
- **Example**: Task "fix typo in README" → light tier (0 agents, 1 critic). Task "add authentication module" → standard/deep.
- **Source**: Self-assessment task, 2026-03-18

### Proportional Critic Usage
- **Context**: When deciding how many review rounds to run
- **Pattern**: Light tier = once at end. Standard = after key subtasks. Deep = after each subtask. Last allowed round = focus on high-severity only.
- **Source**: Self-assessment task, 2026-03-18

### Tool Least Privilege
- **Context**: When creating or reviewing skills
- **Pattern**: Only grant tools the skill actually needs. Bash and Agent are expensive — remove if not essential. skill-generator doesn't need Bash or Agent.
- **Source**: Self-assessment task, 2026-03-18

## Anti-patterns

### Mandatory Full Orchestration
- **Context**: When tempted to always use all phases for every task
- **Problem**: Over-orchestration wastes tokens. A trivial edit doesn't need scout→plan→execute→critic→scribe.
- **Instead**: Assign a light tier and do simple things directly. Only orchestrate fully for standard/deep tasks.
- **Source**: Self-assessment task, 2026-03-18

### Infinite Critic Loop
- **Context**: When critic returns FAIL and you re-execute and re-review
- **Problem**: Without a limit, critic→fix→critic→fix can loop indefinitely, burning tokens.
- **Instead**: Max 2 FAIL verdicts on same target, then circuit breaker → escalate to user.
- **Source**: Self-assessment task, 2026-03-18

### Unbounded Agent Spawning
- **Context**: When orchestrator or scout spawn explore agents
- **Problem**: Each agent has its own context window = significant token cost. Without limits, costs explode.
- **Instead**: Tier-based limits. Light=0-1, Standard=2-4, Deep=5-8. Never exceed without user approval.
- **Source**: Self-assessment task, 2026-03-18

## Skill Gaps

<!-- Tasks where no suitable skill existed — candidates for /skill-generator -->
