# @kknaks-be — 기술 스택

- Python 3.12 + FastAPI + Uvicorn
- SQLAlchemy 2.0(async) + Alembic + PostgreSQL
- Pydantic 2 + pydantic-settings
- pytest + uv (`app/back/pyproject.toml`)
- open-kknaks 2.1.2 (AgentClient/RedisBroker — 제출·스트림 구독) + codex CLI(런타임 마운트)
- Redis (큐 브로커)
- Docker compose (`app/back/docker-compose*.yml`)

## 핵심 원칙
- 최소 변경 · 기존 컨벤션 우선 · 테스트 없이 완료 선언 금지
