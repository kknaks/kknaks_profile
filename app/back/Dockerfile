# back (FastAPI) — uv 기반. inbox.md Step 7: compose 는 back·db·redis 셋.
# git 포함 — /ledger 착지 커밋용(케이스 승인 착지). 원장은 이미지에 굽지 않는다.

FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

# 의존성 레이어 — 코드가 바뀌어도 lock 이 같으면 캐시된다.
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project

# chromium — 웹 캡처 3단계의 동적 렌더(fetch_service). back 이 크롤링 주체라
# 여기 굽는다(사용자 승인 — 이미지 커지는 것 감수). --with-deps 가 apt 런타임
# 라이브러리까지 깐다. 코드 COPY 앞 — 코드가 바뀌어도 이 레이어는 캐시된다.
RUN uv run --no-sync playwright install --with-deps chromium \
    && rm -rf /var/lib/apt/lists/*

COPY . .

EXPOSE 8000

CMD ["uv", "run", "--no-sync", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
