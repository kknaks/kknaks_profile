# back (FastAPI) — uv 기반. inbox.md Step 7: compose 는 back·db·redis 셋.
# git 포함 — /ledger 착지 커밋용(케이스 승인 착지). 원장은 이미지에 굽지 않는다.

FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    # 브라우저를 /root 밖에 둔다 — 아래에서 런타임을 비-root 로 내리는데
    # /root 는 0700 이라 그대로 두면 chromium 을 못 읽는다.
    PLAYWRIGHT_BROWSERS_PATH=/opt/ms-playwright

# 의존성 레이어 — 코드가 바뀌어도 lock 이 같으면 캐시된다.
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project

# chromium — 웹 캡처 3단계의 동적 렌더(fetch_service). back 이 크롤링 주체라
# 여기 굽는다(사용자 승인 — 이미지 커지는 것 감수). --with-deps 가 apt 런타임
# 라이브러리까지 깐다. 코드 COPY 앞 — 코드가 바뀌어도 이 레이어는 캐시된다.
RUN uv run --no-sync playwright install --with-deps chromium \
    && rm -rf /var/lib/apt/lists/*

COPY . .

# 착지는 /ledger(호스트 bind, rw)에 md 를 쓰고 커밋한다. root 로 쓰면 호스트에
# root 소유 파일이 쌓이고, deploy.sh 가 SSH 사용자(kknaks, uid 1000)로 도는
# `git reset --hard` 가 그 파일들을 못 지워 배포가 통째로 실패한다
# (2026-08-28 실사고 — 89개가 걸렸다). 호스트 사용자와 같은 uid 로 내린다.
#
# 여기까지는 root 여야 한다 — apt(--with-deps)와 chown 이 필요하다.
RUN useradd -m -u 1000 -s /usr/sbin/nologin app \
    && chmod -R a+rX /opt/ms-playwright \
    && chown -R app:app /app

ENV HOME=/home/app \
    UV_CACHE_DIR=/home/app/.cache/uv

USER app

EXPOSE 8000

CMD ["uv", "run", "--no-sync", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
