# @mediness-be — 도구 및 제한

## 사용 가능한 도구
- Read, Edit, Write, Glob, Grep, Bash
- mediness 레포의 SKILLs (있다면)

## 작업 디렉토리
- 실제 작업 위치와 base는 dispatch brief의 `작업 워크트리`·`base 브랜치`가 SSOT다.
- 문서 SSOT는 brief §1에 적힌 경로만 read-only로 참조한다.
- **첫 액션**: brief의 작업 워크트리에서
  - `git branch --show-current`와 brief의 base/branch 관계 확인
  - `back/pyproject.toml` (의존성, 스크립트)
  - `back/app/` 디렉토리 구조 Glob 으로 파악
  - 컨벤션·규칙은 brief의 문서 SSOT에 있는 `AGENTS.md`, `rules/`를 read-only로 참조

## 탐색 경로 (mediness-app 레포 루트 기준, 실 디렉토리는 Glob 으로 확인)
```
back/app/router/     # FastAPI 라우터
back/app/service/    # 비즈니스 로직
back/app/schema/     # Pydantic
back/app/model/      # SQLAlchemy 모델
back/app/client/     # 외부 클라이언트
back/app/core/       # 설정, 보안, DI 등
back/app/middleware/ # 미들웨어
back/alembic/        # DB 마이그레이션
back/tests/          # pytest
```

## 오케스트레이션 계약
- 태스크·allowed_paths·검증·완료 보고는 dispatch brief와 preamble만 따른다.
- legacy 태스크 큐·리포트 디렉토리·`.processed`를 읽거나 갱신하지 않는다.

## Bash 자주 쓰는 명령
- `uv run pytest tests/...`
- `uv run alembic ...`
- `uv run ruff check .` (설정 있으면)

## 금지 사항
- `front/` 수정 금지 (FE 담당)
- 문서 레포 `mediness-mediness/` 는 read-only — `rules/`, `context/`, `docs/`, `templates/`, `products/` 수정 금지 (planning 담당)
- **★ `mediness-mediness/mediness-app/` 는 repo split 잔재 — 절대 접근 금지.** 코드는 `harness_works/mediness-app/` 만 사용
- 마이그레이션·API 변경 메모는 리포트 "다른 팀 영향" 에 명시
- git push, 직접 배포 금지
