# 온톨로지 데모 — **이미지 하나로 API 와 MCP 도구 서버 둘 다** 띄운다.
#
# 두 프로세스가 같은 코드(`service/`)를 지나고 같은 DB 를 읽는다. 이미지를 갈라 두면
# 도구와 API 가 서로 다른 커밋으로 뜨는 날이 오고, 그때 「같은 함수를 지난다」로
# 성립시킨 SPEC-003 AC-5(오차 0)가 조용히 깨진다. 커맨드만 다르게 준다:
#
#   API : uv run --no-sync uvicorn main:app       --host 0.0.0.0 --port 28080
#   MCP : uv run --no-sync uvicorn tools.server:asgi --host 0.0.0.0 --port 28081
#
# **DB 는 이미지에 굽지 않는다.** 원천도 산출 DB 도 PII 라 레포 밖 볼륨으로 붙인다
# (compose `ontology-data`). 이미지에 구우면 PII 가 이미지 레이어에 박힌다.
#
# 원천 데이터도 마운트하지 않는다 — 서빙 컨테이너는 **빌드된 DB 만** 읽는다.
# 빌드(`python -m build all`)는 사람이 원천이 있는 자리에서 돌리고 산출 DB만 올린다.

FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

WORKDIR /app

# 의존성 레이어 — 코드가 바뀌어도 lock 이 같으면 캐시된다.
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project

COPY . .

# 호스트 볼륨에 쓰는 것이 없다(DB 는 읽기 전용). 그래도 root 로 돌리지 않는다 —
# 채팅 저장소만 쓰기가 필요해서 그 디렉토리 소유만 넘긴다.
RUN useradd -m -u 1000 -s /usr/sbin/nologin app \
    && mkdir -p /data \
    && chown -R app:app /app /data

ENV HOME=/home/app \
    UV_CACHE_DIR=/home/app/.cache/uv

USER app

EXPOSE 28080 28081

CMD ["uv", "run", "--no-sync", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "28080"]
