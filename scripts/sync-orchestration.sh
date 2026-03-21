#!/bin/bash
# sync-orchestration.sh — Sync .claude/ orchestration system between repos
#
# Usage:
#   ./scripts/sync-orchestration.sh <target-repo-path>
#   ./scripts/sync-orchestration.sh ~/ng-robot
#   ./scripts/sync-orchestration.sh ~/ng-robot --dry-run
#   ./scripts/sync-orchestration.sh ~/ng-robot --commit
#
# Syncs: .claude/skills/ and .claude/memory/ (learnings only)
# Skips: CLAUDE.md (project-specific), state/checkpoint (session-specific)

set -euo pipefail

# --- Config ---
SCRIPT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
SOURCE_DIR="$SCRIPT_DIR/.claude"

# Memory files to sync (shared knowledge, not session state)
SYNC_MEMORY_FILES=(
    "learnings.md"
    "budget.md"
    "decisions.md"
    "news.md"
)

# Memory files to SKIP (session/project-specific)
# checkpoint.md, state.md, implementation-plan*.md, research-findings.md, plugin-research.md

# --- Args ---
TARGET_REPO=""
DRY_RUN=false
AUTO_COMMIT=false

for arg in "$@"; do
    case "$arg" in
        --dry-run) DRY_RUN=true ;;
        --commit) AUTO_COMMIT=true ;;
        -*) echo "Unknown option: $arg"; exit 1 ;;
        *) TARGET_REPO="$arg" ;;
    esac
done

if [ -z "$TARGET_REPO" ]; then
    echo "Usage: $0 <target-repo-path> [--dry-run] [--commit]"
    echo ""
    echo "Options:"
    echo "  --dry-run   Show what would be copied without making changes"
    echo "  --commit    Auto-commit changes in target repo after sync"
    echo ""
    echo "Example:"
    echo "  $0 ~/ng-robot"
    echo "  $0 ~/ng-robot --dry-run"
    echo "  $0 ~/ng-robot --commit"
    exit 1
fi

# Resolve to absolute path
TARGET_REPO="$(cd "$TARGET_REPO" 2>/dev/null && pwd)" || {
    echo "Error: Target directory '$1' does not exist"
    exit 1
}

TARGET_CLAUDE="$TARGET_REPO/.claude"

echo "=== Orchestration Sync ==="
echo "Source: $SOURCE_DIR"
echo "Target: $TARGET_CLAUDE"
[ "$DRY_RUN" = true ] && echo "Mode:   DRY RUN (no changes)"
echo ""

# --- Sync skills ---
echo "--- Skills ---"
mkdir -p "$TARGET_CLAUDE/skills"

changed=0
for skill_dir in "$SOURCE_DIR/skills"/*/; do
    skill_name="$(basename "$skill_dir")"
    source_file="$skill_dir/SKILL.md"
    target_file="$TARGET_CLAUDE/skills/$skill_name/SKILL.md"

    if [ ! -f "$source_file" ]; then
        continue
    fi

    if [ -f "$target_file" ]; then
        if diff -q "$source_file" "$target_file" > /dev/null 2>&1; then
            echo "  [=] $skill_name (unchanged)"
            continue
        fi
        echo "  [U] $skill_name (updated)"
    else
        echo "  [+] $skill_name (new)"
    fi

    if [ "$DRY_RUN" = false ]; then
        mkdir -p "$TARGET_CLAUDE/skills/$skill_name"
        cp "$source_file" "$target_file"
    fi
    ((changed++))
done

# --- Sync memory (selected files only) ---
echo ""
echo "--- Memory ---"
mkdir -p "$TARGET_CLAUDE/memory"

for mem_file in "${SYNC_MEMORY_FILES[@]}"; do
    source_file="$SOURCE_DIR/memory/$mem_file"
    target_file="$TARGET_CLAUDE/memory/$mem_file"

    if [ ! -f "$source_file" ]; then
        continue
    fi

    if [ -f "$target_file" ]; then
        if diff -q "$source_file" "$target_file" > /dev/null 2>&1; then
            echo "  [=] $mem_file (unchanged)"
            continue
        fi
        echo "  [U] $mem_file (updated)"
    else
        echo "  [+] $mem_file (new)"
    fi

    if [ "$DRY_RUN" = false ]; then
        cp "$source_file" "$target_file"
    fi
    ((changed++))
done

# --- Also copy this script to target ---
target_script="$TARGET_REPO/scripts/sync-orchestration.sh"
if [ "$DRY_RUN" = false ]; then
    mkdir -p "$TARGET_REPO/scripts"
    cp "$SCRIPT_DIR/scripts/sync-orchestration.sh" "$target_script" 2>/dev/null || true
    chmod +x "$target_script" 2>/dev/null || true
fi

# --- Summary ---
echo ""
if [ "$changed" -eq 0 ]; then
    echo "Everything is up to date."
else
    if [ "$DRY_RUN" = true ]; then
        echo "$changed file(s) would be updated. Run without --dry-run to apply."
    else
        echo "$changed file(s) synced."

        if [ "$AUTO_COMMIT" = true ]; then
            echo ""
            echo "--- Committing in target repo ---"
            cd "$TARGET_REPO"
            git add .claude/
            git commit -m "Sync orchestration system from upstream" || echo "Nothing to commit."
        fi
    fi
fi
