# @mediness-be — 기술 스택

## 언어 및 프레임워크
- Python 3.12 + FastAPI (Uvicorn)
- SQLAlchemy 2.0 + Alembic + psycopg (PostgreSQL)
- Pydantic 2 + pydantic-settings
- pytest + uv (`pyproject.toml`, `uv.lock`)
- structlog / python-json-logger
- WebSocket (FastAPI 내장)
- Celery / 워커 (`Dockerfile.worker`, `worker-entrypoint.sh` 존재 시)

## 레이어 구조
- 디렉토리: `app/router/`, `app/service/`, `app/schema/`, `app/model/`, `app/client/`, `app/core/`, `app/middleware/` (실제 디렉토리는 작업 시 Glob 으로 확인)
- 4 계층 지향: Router (HTTP) → Service (비즈니스) → (Repository) → Model

## 핵심 원칙
- TDD: RED → GREEN → REFACTOR. 테스트 없이 프로덕션 코드 X
- 최소 변경: 정확히 필요한 부분만
- 기존 컨벤션 우선 — 작업 전 `app/` 구조와 기존 파일 패턴 확인
