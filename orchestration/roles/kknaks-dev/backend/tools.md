# @kknaks-be — 도구 및 구조

## 작업 디렉토리
- 실제 작업 위치·base 는 dispatch brief 의 `작업 워크트리`·`base 브랜치`가 SSOT
- **첫 액션**: 워크트리에서 `git branch --show-current` 확인 → `app/back/pyproject.toml` →
  `app/back/` 구조를 Glob 으로 파악

## 탐색 경로 (레포 루트 기준)
```
app/back/api/          # FastAPI 라우터 (*_router.py)
app/back/service/      # 비즈니스 로직
app/back/repository/   # DB 접근 (ORM 은 여기까지)
app/back/models/       # SQLAlchemy 모델
app/back/schemas/      # front 계약 (Pydantic)
app/back/dto/          # 계층 간 내부 운반
app/back/core/         # db·security·예외
app/back/alembic/      # 마이그레이션
app/back/tests/        # pytest
app/back/ai_schemas/   # codex output schema (기존 파이프라인)
app/mcp/               # (신설) 채팅 MCP 서버
```

## 자주 쓰는 명령
- `cd app/back && uv run pytest -q tests/<파일>`
- `cd app/back && uv run alembic revision --autogenerate -m "..."`

## 금지 사항
- `app/front/` 수정 금지 (FE 담당) · `para/`·`orchestration/` 수정 금지 (코디네이터)
- git commit·push·PR 금지 — 워크트리에 변경만 남긴다
