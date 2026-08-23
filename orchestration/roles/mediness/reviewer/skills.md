# @mediness-reviewer — 기술 스택 (검수 대상 이해용)

리뷰어는 구현하지 않지만, 검수 대상의 스택을 읽을 줄 알아야 한다.

## 문서 리포 (mediness-mediness)
- 문서 파이프라인: `20-spec/`(계약) → `30-work/`(WP) → `30-work.md`(WP List·Status Board·Spec Coverage)
- 규칙 원본: 리포 루트 `rules/document-pipeline.md`, 린트: `scripts/lint-pipeline.py`
- ID 체계: `MEDINESS-SPEC-NNN` / `MEDINESS-WP-NNN` — 매달린 참조는 린트가 잡는다

## 백엔드 (mediness-app/back)
- Python 3.12 + FastAPI + SQLAlchemy 2.0 (+ Alembic) + Pydantic 2
- 계층: `app/routers/` → `app/services/` → `app/repositories/` → `app/models/`, 경계 `app/schemas/`
- 부속: `app/core/`(설정·보안·DI), `app/clients/`(외부), `app/policies/`, `app/commands/`, `app/seeds/`
- 테스트: pytest (`back/tests/`)

## 프론트엔드 (mediness-app/front)
- Next.js (App Router) + TypeScript + Tailwind
- 구조: `app/`(라우트·페이지) · `components/`(도메인별 공용 컴포넌트) · `lib/`(훅·유틸·API)
- 테스트: vitest (`__tests__/`)

## 검수 기법
- diff 산정: `git diff --stat <base>...HEAD` + `git status --porcelain` (untracked 포함)
- 재사용 위반 탐지: 신규 함수/컴포넌트 이름·역할로 기존 코드 Grep — 유사물이 이미 있으면 위반 후보
- 계층 위반 탐지: `grep -n "session.execute\|select(" back/app/routers/ back/app/services/` 류의 위치 기반 검색
- 근거 수집: 위반마다 기존의 "올바른 예" 파일을 하나 찾아 대조 근거로 제시
