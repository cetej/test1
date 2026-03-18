# Shared Memory — Decision Log

Decisions made during task execution. Each entry captures WHAT was decided, WHY, and by WHOM.

### 2026-03-18 — Add Budget Controller to Orchestration System
- **Context**: Self-assessment revealed no cost controls. System could become a "token black hole" with unbounded agent spawns and critic loops.
- **Options considered**: (A) Simple agent counter, (B) Full budget skill with tiers + circuit breakers + history, (C) External hook-based monitoring
- **Decision**: Option B — full budget skill with 3 complexity tiers (light/standard/deep)
- **Rationale**: Most practical. Tiers give proportional control without over-engineering. Circuit breakers prevent runaway costs. History enables learning from past task costs. External hooks (C) would be fragile and hard to maintain.
- **Decided by**: orchestrator + user

### 2026-03-18 — Soften "Never Do Work Yourself" Rule
- **Context**: Original orchestrator rule "never do the work yourself" forced delegation even for trivial edits, wasting tokens.
- **Options considered**: (A) Keep strict rule, (B) Allow direct work for light tier, (C) Remove rule entirely
- **Decision**: Option B — light tier allows direct work, standard/deep still delegate
- **Rationale**: Proportional approach. A single-line fix shouldn't spawn an agent. But complex tasks still benefit from delegation to keep the orchestrator focused on coordination.
- **Decided by**: orchestrator (self-assessment)

### 2026-03-18 — Remove Bash and Agent from skill-generator
- **Context**: skill-generator had Bash and Agent in allowed-tools but doesn't need them. Violates least-privilege principle.
- **Decision**: Restricted to Read, Write, Edit, Glob, Grep
- **Rationale**: skill-generator creates files and reads existing ones. It never needs to run shell commands or spawn subagents.
- **Decided by**: orchestrator (self-assessment)
