# @ontology-be — 기술 스택

- Python 3.12 + FastAPI + Uvicorn + uv (`app/ontology-agent/pyproject.toml`)
- SQLite (표준 라이브러리 `sqlite3` — ORM 없음. 테이블·뷰는 빌드 스크립트가 생성)
- Pydantic 2 + pydantic-settings (`config.py`)
- open-kknaks 2.1.2 (AgentClient/RedisBroker — 제출·스트림 구독) + codex CLI(런타임 마운트)
- MCP (FastMCP Streamable HTTP — `app/mcp/` 가 모범)
- pytest
- 프론트는 static 단일 페이지(순수 HTML/JS — 빌드 도구 없음). 목업 HTML 이 출발점

## 핵심 원칙
- 최소 변경 · 기존 컨벤션 우선 · 테스트 없이 완료 선언 금지
- 데이터 변환 로직은 기존 스크립트의 **이식** — 새 해석을 넣지 않는다
