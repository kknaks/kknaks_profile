# @centurion-backend — 도구 및 구조

## 작업 위치
- 워크트리 · base 는 브리프가 SSOT. 첫 액션: `git branch --show-current` → 레포 `AGENTS.md` → 브리프 §1 계약 문서 통독.

## 레이아웃
```
backend/crm/__init__.py      모듈 경계 설명
backend/crm/public.py        공개 면 — 밖은 이것만 import
backend/crm/{config,db,models,dtos,enums,errors}.py
backend/crm/connection.py    병원별 CRM 연결
backend/crm/kos_client.py    KOS 클라이언트
backend/crm/catalog_source.py  catalog 동기화 공급원
backend/crm/emr/             업체별 어댑터(base · factory · kos)
backend/migrations/crm/      Alembic revision
backend/tests/crm/           (없으면 만든다 — 브리프 allowed_paths 안)
```

## 명령 (`backend/` 에서)
- `uv sync --frozen` (private index 권한 필요 — 실패하면 설치를 우회하지 말고 보고)
- `uv run --frozen pytest -q <만든·고친 테스트만>`
- `uv run --frozen ruff check <만진 파일>`
- `scripts/test.sh` 에는 crm 전용 suite 가 없다(sso · admin · common · linky · integration · all).

## 금지
- allowed_paths 밖 수정 · 커밋 · push · PR · migration 적용 · 사용자 포트/프로세스 종료.
