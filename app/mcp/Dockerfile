# 채팅용 MCP 서버 — back chat-tool API 의 얇은 래퍼.
#
# 이 컨테이너는 **원장을 마운트하지 않는다.** 파일을 만질 일이 없다 — 데이터는 전부
# back HTTP 로 온다(DEC-027 D5). codex 워커도 마찬가지로 마운트가 없다.

FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

COPY pyproject.toml uv.lock* ./
RUN uv sync --no-dev || (uv lock && uv sync --no-dev)

COPY app ./app

EXPOSE 28081

CMD ["uv", "run", "uvicorn", "app.server:asgi", "--host", "0.0.0.0", "--port", "28081"]
