# @centurion-backend — 기술 스택

- Python 3.13 · FastAPI · Pydantic v2 · uv(`backend/uv.lock`, `--frozen`)
- SQLAlchemy async · PostgreSQL · Alembic(서비스별 chain — `alembic.crm.ini`)
- Redis · RabbitMQ/TaskIQ(Linky worker) — crm 이 쓰는지는 브리프·코드로 확인
- pytest · ruff(`backend/ruff.toml`)
- 관리 화면은 `backend/admin`(Jinja + HTMX + Tailwind) — 브리프가 지정할 때만
