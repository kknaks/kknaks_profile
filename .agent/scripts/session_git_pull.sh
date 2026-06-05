#!/usr/bin/env bash
# SessionStart hook: keep the main branch in sync with the remote.
# Only pulls when the current branch is main, so starting a session on a
# feature branch never triggers an unexpected rebase. --autostash keeps any
# in-progress work safe; failures are swallowed so a session never blocks.
set -uo pipefail

branch=$(git rev-parse --abbrev-ref HEAD 2>/dev/null) || exit 0

if [ "$branch" = "main" ]; then
  git pull --rebase --autostash origin main 2>&1 || echo "session_git_pull: pull skipped (see git output above)"
else
  echo "session_git_pull: on '$branch', not main — skipped"
fi

exit 0
