FROM python:3.13-slim

# git — jobs/inputs.py의 git_log_today 호출에 필요 (spec-03 §2.2)
# build deps — pydantic-core 등 일부 패키지가 컴파일 필요할 수 있음
RUN apt-get update \
    && apt-get install -y --no-install-recommends git build-essential \
    && rm -rf /var/lib/apt/lists/*

# uv — 의존성 매니저 (back/pyproject.toml과 일관)
RUN pip install --no-cache-dir uv

WORKDIR /app

# 의존성 먼저 (Docker layer caching — pyproject 안 바뀌면 재install 안 함)
COPY pyproject.toml ./
RUN uv sync --no-install-project

# 코드 복사
COPY . .

ENV PYTHONUNBUFFERED=1 \
    PERSONA_DIR=/persona \
    PYTHONPATH=/app

EXPOSE 48000

# single-worker 강제 (spec-03 §1.2 — APScheduler 다중 발동 차단)
CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "48000", "--workers", "1"]
