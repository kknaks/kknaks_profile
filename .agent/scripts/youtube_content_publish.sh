#!/usr/bin/env bash
# Commit a pending content stub and push to origin/main.
#
# Usage: youtube_content_publish.sh persona/contents/C-019-pending.md
#
# Flow:
#   1) git add <stub>
#   2) git commit            (pre-commit hook rebuilds + stages persona/_map.md
#                             and runs persona validation — do NOT pass --no-verify)
#   3) fetch + rebase + push, retried up to 3x for concurrent server pushes.
#
# Conflict guard: the enrich server pushes to the same branch, so a rebase can
# collide on the auto-generated persona/_map.md. That single file we resolve by
# rebuilding it. ANY other unmerged path means a real conflict (e.g. an id
# collision on the stub itself) — we abort the rebase and stop WITHOUT pushing.

set -euo pipefail

STUB="${1:?usage: youtube_content_publish.sh <stub-path>}"
REPO="$(git rev-parse --show-toplevel)"
cd "$REPO"

if [ ! -f "$STUB" ]; then
  echo "stub not found: $STUB" >&2
  exit 1
fi

CONTENT_ID="$(grep -m1 '^id:' "$STUB" | awk '{print $2}')"
YOUTUBE_ID="$(grep -m1 '^youtubeId:' "$STUB" | awk '{print $2}')"
MSG="chore: content ${CONTENT_ID} pending (youtubeId ${YOUTUBE_ID})"

build_map() {
  uv run --quiet --with python-frontmatter --with pyyaml \
    python3 app/scripts/build_persona_map.py >/dev/null
}

git add "$STUB"
git commit -m "$MSG"

for attempt in 1 2 3; do
  git fetch origin

  if ! git rebase origin/main; then
    unmerged="$(git diff --name-only --diff-filter=U)"
    if [ "$unmerged" = "persona/_map.md" ]; then
      build_map
      git add persona/_map.md
      git -c core.editor=true rebase --continue
    else
      git rebase --abort
      echo "rebase conflict in: ${unmerged:-<none>} — aborted, not pushing" >&2
      exit 1
    fi
  fi

  if git push origin main; then
    echo "pushed: $STUB ($MSG)"
    exit 0
  fi

  echo "push rejected (attempt ${attempt}/3) — remote advanced, retrying" >&2
  sleep $((attempt * 2))
done

echo "push failed after 3 attempts" >&2
exit 1
