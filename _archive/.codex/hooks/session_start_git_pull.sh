#!/usr/bin/env bash
set -euo pipefail

repo_root="$(git rev-parse --show-toplevel 2>/dev/null || true)"
if [[ -z "$repo_root" ]]; then
  echo "codex session git pull: skip, not inside a git repo"
  exit 0
fi

cd "$repo_root"

branch="$(git branch --show-current)"
if [[ -z "$branch" ]]; then
  echo "codex session git pull: skip, detached HEAD"
  exit 0
fi

upstream="$(git rev-parse --abbrev-ref --symbolic-full-name '@{u}' 2>/dev/null || true)"
if [[ -z "$upstream" ]]; then
  echo "codex session git pull: skip, no upstream for $branch"
  exit 0
fi

if [[ -n "$(git status --porcelain)" ]]; then
  echo "codex session git pull: skip, working tree has local changes"
  exit 0
fi

git pull --ff-only
