# @sc-ax-be — 기술 스택

## 언어 및 프레임워크
- Python 3.12 + FastAPI + Uvicorn
- SQLAlchemy 2.0 + psycopg 3 (PostgreSQL 16, 확장 없음) — Alembic 은 아직 없다(운영 스키마 변경은 별도 gate)
- Pydantic 2 · MCP(`mcp[cli]`) · pytest 8 · uv (`pyproject.toml`·`uv.lock`, hatchling)
- 문서 파서: pypdf · python-docx · openpyxl · python-pptx · 한국어 분석 kiwipiepy

## 구조 (backend/src/ax_workspace/)
- `modules/<도메인>/` — organization_access · work · reports · meetings · ax_execution · actions · jobs · datasets.
  `domain.py`(순수 도메인) · `application.py`(operation) · 그 외 하위 관심사 파일
- `platform/` — persistence · durable_jobs · conversations · materials · soniox · codex_cli 등 어댑터
- `entrypoints/` — http · http_auth · mcp · *_worker · reset_demo · dataset
- `bootstrap/` — application(조립) · settings · seed · reset · schema_sync · dataset_import

## 도메인 지식
- 도메인 사실의 SSOT 는 spec 리포 `products/sc-ax/`(baseline·SPEC·ERD). 이 파일에 요약을 복사하지 않는다 — 낡는다
- 구현 대조는 `docs/domain-model.md`. README 의 「로그인과 세션」「권한」「업무」「판단 통합」이 현재 동작 설명

## 핵심 원칙
- TDD: RED → GREEN → REFACTOR
- 최소 변경 · 기존 컨벤션 우선 — 작업 전 같은 모듈의 기존 파일 패턴 확인
- 실행 경로는 하나(`make local-stack`). demo mode 를 따로 만들지 않는다 — production 경로를 `DeveloperAuthAdapter`+seed 로 지나간다
