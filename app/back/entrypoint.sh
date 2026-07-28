#!/bin/sh
# back 컨테이너 기동 — 마이그레이션 먼저, 그다음 서버 (KDEV-WORK-015).
#
# **스키마 없이 뜨면 조용히 반쯤 죽는다.** `seed_admin` 이 DB 실패를 삼키고 부팅을
# 계속하도록 돼 있어서, 사이트는 멀쩡한데 관리자 로그인과 승인 큐만 안 되는 상태가
# 된다. 에러도 안 보인다.
#
# CI 스텝이 아니라 여기서 하는 이유: 배포 워크플로 밖에서 `docker compose up` 을
# 직접 해도 누락되지 않는다. alembic 은 멱등이라 재시작마다 돌아도 무해하고,
# `--workers 1` 하드락이라 동시 실행 경합도 없다.
#
# `set -e` — 마이그레이션이 실패하면 **뜨지 않는다.** 잘못된 스키마 위에서 서비스가
# 도는 것보다 크래시 루프가 낫다. 최소한 눈에 보인다.
set -e

echo "[entrypoint] alembic upgrade head"
uv run --no-sync alembic upgrade head

echo "[entrypoint] starting uvicorn (single worker)"
# single-worker 강제 (spec-03 §1.2 — APScheduler 다중 발동 차단)
exec uv run --no-sync uvicorn main:app --host 0.0.0.0 --port 48000 --workers 1
