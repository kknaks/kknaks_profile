#!/usr/bin/env bash
# open-kknaks 워커 기동 — **호스트 직접 실행 폴백**.
#
# 기본은 compose 의 worker 서비스다 (docker-compose.yml + docker-compose.local.yml,
# 2026-08-25 전환). codex CLI 는 거기서도 이미지에 안 굽는다 — 호스트의 리눅스용
# 번들을 런타임 마운트한다. 이 스크립트는 compose 없이 호스트에서 워커를 띄워야
# 할 때(디버깅·번들 문제 우회)만 쓴다 — 호스트 codex + ~/.codex 인증을 그대로 쓰고
# compose 의 redis 노출 포트(46379)로 붙는다.
# ⚠ 폴백으로 돌릴 땐 back 의 .env AI_CWD·AI_SCHEMA_DIR 이 /ledger 기준이므로
#   호스트 경로로 덮어야 한다 (아래 AI_CWD 환경변수 참고).
#
# 사전 준비
#   1. codex CLI 설치 + 로그인          — `codex --version` 으로 확인
#   2. redis 가 떠 있음                 — docker compose 의 kknaks-redis (localhost:46379)
#   3. app/back 의존성 설치             — `uv sync` (open-kknaks 는 back 의존성에 있다)
#
# 사용법
#   bash app/back/scripts/run-worker.sh
#
#   환경변수로 덮을 수 있다:
#     REDIS_URL     기본 redis://localhost:46379/0   — back 의 REDIS_URL 과 같아야 한다
#     AI_NAMESPACE  기본 kknaks_profile              — back 의 AI_NAMESPACE 와 같아야 한다
#     AI_QUEUE      기본 default                     — back 의 AI_QUEUE 와 같아야 한다
#     AI_CWD        기본 이 레포 루트                — codex 의 읽기 전용 cwd(원장 레포).
#                                                     back 이 컨테이너여도 이 값은
#                                                     **호스트 경로**다 — back 의 AI_CWD 와
#                                                     같은 호스트 경로를 가리켜야 한다
#     CONCURRENCY   기본 1                           — codex 세션 동시 실행 수
#
# 참고
#   - 태스크의 provider=codex 는 back 이 제출할 때 정한다 — 워커는 코덱스/클로드
#     어댑터를 모두 등록하고 태스크가 고른 쪽을 실행한다
#   - output_schema 는 back 이 파일 경로(app/back/ai_schemas/*.json)로 넘긴다 —
#     이 경로도 워커(호스트) 기준이다. back 이 컨테이너면 AI_SCHEMA_DIR 로
#     호스트 경로를 넘겨야 한다
#   - open-kknaks 를 back 의존성 대신 라이브러리 체크아웃으로 돌리려면:
#     cd <open_kknaks 클론> && uv run open-kknaks worker run ... (README 참고)

set -euo pipefail

BACK_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REPO_ROOT="$(cd "$BACK_DIR/../.." && pwd)"

REDIS_URL="${REDIS_URL:-redis://localhost:46379/0}"
AI_NAMESPACE="${AI_NAMESPACE:-kknaks_profile}"
AI_QUEUE="${AI_QUEUE:-default}"
AI_CWD="${AI_CWD:-$REPO_ROOT}"
CONCURRENCY="${CONCURRENCY:-1}"

if ! command -v codex >/dev/null 2>&1; then
  echo "codex CLI 가 없다 — 호스트에 설치·로그인부터 (inbox.md Step 7)" >&2
  exit 1
fi

echo "worker: redis=$REDIS_URL ns=$AI_NAMESPACE queue=$AI_QUEUE cwd=$AI_CWD"
cd "$BACK_DIR"
exec uv run open-kknaks worker run \
  --broker "$REDIS_URL" \
  --namespace "$AI_NAMESPACE" \
  --queues "$AI_QUEUE" \
  --work-dir "$AI_CWD" \
  --concurrency "$CONCURRENCY"
