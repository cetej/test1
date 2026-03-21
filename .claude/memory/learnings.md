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

### Cost Estimation for User Decisions
- **Context**: When proposing options with different cost profiles to the user
- **Pattern**: Always estimate cost in tokens AND real currency (USD + local). Users can't judge "50k tokens" but understand "$0.15/week". Present as comparison table with previews.
- **Example**: /watch source tier selection — presented 3 options with token counts, USD, CZK estimates
- **Source**: /watch creation task, 2026-03-18

## Cross-Repo Setup

### User's Desktop Environment
- **Context**: User (cetej) works on desktop with repo `ng-robot` (https://github.com/cetej/NG-ROBOT)
- **Key fact**: `test1` repo exists ONLY on Claude Code web — it does NOT exist on user's desktop
- **Orchestration sync**: `.claude/skills/` and `.claude/memory/` are developed here in test1, then synced to ng-robot via `scripts/sync-orchestration.sh` or manual `git checkout` from test1 remote
- **CLAUDE.md**: Each repo has its own project-specific CLAUDE.md — do NOT sync between repos
- **Sync workflow**: User added test1 as remote in ng-robot (`git remote add test1 https://github.com/cetej/test1.git`), then cherry-picks files from test1 branches
- **Common confusion**: User may say "I did git pull but nothing changed" — likely pulled in ng-robot while changes are in test1. Always clarify which repo.
- **Source**: Session 2026-03-18

## Skill Gaps

### ~~Dependency Upgrade Planner~~ RESOLVED
- Created `/dependency-audit` skill (2026-03-18)

### Agent Teams Integration
- **Situation**: Claude Code now supports native Agent Teams (since Feb 2026)
- **What was needed**: /orchestrate Phase 4 could use Agent Teams for parallel subtask execution instead of manual Agent() spawning
- **Workaround used**: Current system uses individual Agent() calls
- **Priority**: medium
