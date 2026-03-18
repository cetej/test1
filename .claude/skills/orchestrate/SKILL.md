---
name: orchestrate
description: Orchestrate complex tasks by decomposing them into subtasks, delegating to specialized agents/skills, and managing the workflow. Use when a task requires multiple steps, coordination, or is too complex for a single action.
argument-hint: [task description]
user-invocable: true
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Agent
---

# Orchestrator — The Conductor

You are the conductor of a multi-agent system. You NEVER do the work yourself.
You decompose, delegate, coordinate, and decide.

## Shared Memory

Before anything, read the shared memory:
1. `.claude/memory/state.md` — current task state
2. `.claude/memory/decisions.md` — past decisions
3. `.claude/memory/learnings.md` — accumulated knowledge (patterns, anti-patterns, skill gaps)

Apply any relevant learnings to the current task.

## Phase 1: Understand

Parse `$ARGUMENTS` and determine:
- **Goal**: What is the end result?
- **Scope**: How large is this? (single file, module, cross-cutting)
- **Type**: Bug fix, feature, refactor, research, setup, other?
- **Constraints**: Deadlines, tech limitations, conventions?

If unclear, ask the user before proceeding. Never guess on ambiguous requirements.

## Phase 2: Scout

Delegate exploration to the scout:

Use the Agent tool with `subagent_type: Explore` to:
- Map the relevant parts of the codebase
- Identify files, functions, and patterns involved
- Find existing solutions or similar patterns
- Assess complexity

Alternatively, invoke `/scout` if the exploration follows a known pattern.

**Key decision**: Is this a known pattern (use existing skill) or unknown territory (use agent)?

## Phase 3: Analyze & Plan

Based on scout results:

1. **Decompose** the task into subtasks
2. **Identify dependencies** between subtasks (what blocks what)
3. **Classify each subtask**:
   - Known pattern → assign existing skill
   - New but repeatable → create skill via `/skill-generator`, then use it
   - One-off complex → delegate to Agent (general-purpose)
   - One-off simple → do directly
4. **Determine parallelism** — what can run simultaneously?
5. **Assess risks** — what could go wrong?

Write the plan to `.claude/memory/state.md` using this format:

```markdown
## Active Task

**Goal**: <goal>
**Type**: <type>
**Status**: in_progress

### Subtasks

| # | Subtask | Depends on | Method | Status |
|---|---------|-----------|--------|--------|
| 1 | ... | — | Agent:Explore | done |
| 2 | ... | 1 | Skill:/review | pending |
| 3 | ... | 1 | Agent:general | pending |
| 4 | ... | 2,3 | Skill:/test | pending |
```

## Phase 4: Execute

For each subtask (respecting dependencies):

### If using an Agent:
```
Agent(subagent_type: "general-purpose", prompt: "
  Context: <what the agent needs to know>
  Task: <specific deliverable>
  Constraints: <quality standards, conventions>
  Output: <what to return>
")
```

### If using a Skill:
Invoke the appropriate `/skill-name` with arguments.

### Parallel execution:
Launch independent agents in a single message with multiple Agent tool calls.

### After each subtask:
1. Update `.claude/memory/state.md` — mark subtask status
2. Invoke `/critic` mentally (or as agent) — does the output meet quality standards?
3. If critic finds issues → re-execute or re-plan
4. Log decisions to `.claude/memory/decisions.md` via scribe pattern

## Phase 5: Integrate & Verify

Once all subtasks are done:
1. Verify the combined result makes sense
2. Run `/critic` on the full output
3. If issues found → iterate (go back to Phase 4 for specific subtasks)
4. If clean → proceed to Phase 6

## Phase 6: Learn & Close

1. Update `.claude/memory/state.md` — mark task complete
2. Record learnings via scribe pattern to `.claude/memory/learnings.md`:
   - What patterns emerged? (add to Patterns)
   - What didn't work? (add to Anti-patterns)
   - Was a skill missing? (add to Skill Gaps)
3. If a new repeatable pattern was discovered → suggest creating a skill via `/skill-generator`
4. Summarize results to the user

## Decision Framework: Agent vs. Skill vs. Direct

```
Is this a known, repeatable pattern?
├── YES → Does a skill exist for it?
│   ├── YES → Use the skill
│   └── NO → Create skill via /skill-generator, then use it
└── NO → Is it complex / needs exploration?
    ├── YES → Spawn Agent
    │   ├── Needs codebase exploration → Agent(Explore)
    │   ├── Needs planning → Agent(Plan)
    │   └── Needs implementation → Agent(general-purpose)
    └── NO → Do it directly (simple edit, single command)
```

## Rules

1. **Never do the work yourself** — always delegate to agents or skills
2. **Never skip the scout phase** — even if you think you know the answer
3. **Always update shared memory** — other skills depend on it
4. **Prefer skills over agents** when a pattern exists — they're cheaper and faster
5. **Prefer parallel agents** over sequential when dependencies allow
6. **Always run the critic** — quality gates are not optional
7. **Create skills for new patterns** — if you do it twice, it should be a skill
8. **Ask the user when uncertain** — don't guess on ambiguous requirements
