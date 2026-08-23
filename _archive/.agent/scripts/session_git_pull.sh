#!/usr/bin/env bash
# SessionStart hook: keep the main branch in sync with the remote.
# Only pulls when the current branch is main, so starting a session on a
# feature branch never triggers an unexpected rebase. --autostash keeps any
# in-progress work safe.
#
# Always prints exactly one deterministic status line so the session start
# log confirms the pull ran — even when already up to date. (Plain `git pull`
# can emit empty stdout when there is nothing to do, which looked like the
# hook never ran.)
set -uo pipefail

branch=$(git rev-parse --abbrev-ref HEAD 2>/dev/null) || {
  echo "🔄 git-pull: not a git repo — skipped"
  exit 0
}

if [ "$branch" != "main" ]; then
  echo "🔄 git-pull: on '$branch' (not main) — skipped"
  exit 0
fi

before=$(git rev-parse --short HEAD 2>/dev/null)
out=$(git pull --rebase --autostash origin main 2>&1)
status=$?
after=$(git rev-parse --short HEAD 2>/dev/null)

if [ "$status" -ne 0 ]; then
  echo "❌ git-pull: FAILED on main — resolve manually:"
  echo "$out"
  exit 0
fi

if [ "$before" = "$after" ]; then
  echo "✅ git-pull: main already up to date (${after})"
else
  count=$(git rev-list --count "${before}..${after}" 2>/dev/null || echo "?")
  echo "✅ git-pull: main updated (${before} → ${after}, +${count} commits)"
fi

exit 0
