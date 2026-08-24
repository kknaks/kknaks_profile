#!/usr/bin/env bash
# 로컬 dev 일괄 실행 — postgres(도커) + 백엔드(uv) + 프론트(npm).
# Ctrl-C 로 백/프론트가 같이 죽는다. postgres 는 컨테이너라 살아 있다
# (내리려면: docker compose -f back/docker-compose.yml down).

set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"

# 1. postgres — healthy 까지 기다린다
docker compose -f "$ROOT/back/docker-compose.yml" up -d --wait postgres

# 2. 백엔드 — :48000 (프론트 NEXT_PUBLIC_API_BASE 기본값)
(cd "$ROOT/back" && uv run uvicorn main:app --reload --port 48000) &
BACK_PID=$!

# 3. 프론트 — :3000
(cd "$ROOT/front" && npm run dev) &
FRONT_PID=$!

trap 'kill "$BACK_PID" "$FRONT_PID" 2>/dev/null' INT TERM EXIT
wait
