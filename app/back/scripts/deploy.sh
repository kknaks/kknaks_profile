#!/usr/bin/env bash
# 백엔드 수동 배포 — 로컬에서 실행하면 홈서버에 SSH 로 들어가 배포한다.
#
#   ./app/back/scripts/deploy.sh          # origin/main 기준
#   ./app/back/scripts/deploy.sh <브랜치>  # 다른 브랜치로 배포
#
# 하는 일: 서버 clone 을 origin/<브랜치> 로 reset → app/back/.env 확인 →
#          docker compose up -d --build → /api/health 대기.
# .env 는 안 건드린다 — 서버의 app/back/.env 는 사람이 관리한다.
# 프론트는 Vercel 자체 배포라 여기서 다루지 않는다.

set -euo pipefail

SSH_HOST=home-server
REPO_DIR=/home/kknaks/kknaks_profile
BRANCH="${1:-main}"

ssh "$SSH_HOST" bash -s <<EOF
set -euo pipefail
cd "$REPO_DIR"

echo "── fetch + reset --hard origin/$BRANCH"
# 서버 working tree 는 origin 의 mirror 다. 착지 잡 커밋은 push 완료가
# 확정 조건(케이스 1)이라 reset 으로 잃을 로컬 상태가 없다.
git fetch origin "$BRANCH"
git checkout -B "$BRANCH" "origin/$BRANCH"
git reset --hard "origin/$BRANCH"

echo "── preflight: app/back/.env"
test -f app/back/.env || { echo "app/back/.env 가 없다 — 서버에 먼저 두어라"; exit 1; }

echo "── docker compose up -d --build"
cd app/back
docker compose up -d --build

echo "── /api/health 대기"
for i in \$(seq 1 90); do
  if curl -fsS -o /dev/null http://localhost:48000/api/health; then
    echo "back ready (attempt \$i)"
    exit 0
  fi
  sleep 2
done
echo "back 이 안 떴다 — 로그:"
docker compose logs --tail 50 back
exit 1
EOF
