# @sc-ax-be — 도구 및 제한

## 사용 가능한 도구
- Read, Edit, Write, Glob, Grep, Bash

## 작업 디렉토리
- 실제 작업 위치와 base 는 dispatch brief 의 `작업 워크트리`·`base 브랜치`가 SSOT 다
- 문서 SSOT 는 brief §1 에 적힌 경로(spec 리포 코디 워크트리 절대경로)만 read-only 로 참조한다
- **첫 액션**: brief 의 작업 워크트리에서
  - `git branch --show-current` 와 brief 의 base/branch 관계 확인
  - `README.md` 「띄우기」「검증」, `backend/pyproject.toml`
  - `backend/src/ax_workspace/` 구조를 Glob 으로 파악 · `tests/architecture/test_architecture.py` 로 경계 규칙 확인
  - `docs/domain-model.md` 에서 이번 태스크가 닿는 표·모듈 확인

## 탐색 경로 (ax-workspace 루트 기준, 실 파일은 Glob 으로 확인)
```
backend/src/ax_workspace/modules/      # 도메인별 domain.py · application.py
backend/src/ax_workspace/platform/     # 영속·잡·외부 어댑터
backend/src/ax_workspace/entrypoints/  # http · mcp · 워커 · reset_demo
backend/src/ax_workspace/bootstrap/    # 조립 · settings · seed
backend/tests/{unit,contract,integration,architecture}/
docs/domain-model.md                   # ERD ↔ 구현 대조표
```

## 오케스트레이션 계약
- 태스크·allowed_paths·검증·완료 보고는 dispatch brief 와 preamble 만 따른다

## Bash 자주 쓰는 명령
- `cd backend && uv run pytest -q tests/unit/test_x.py` · `uv run pytest -q tests/architecture`
- `make postgres-up` · `make reset-demo`(파괴적 — 브리프가 허용할 때만) · `make api`
- 전체 스위트(`make test`·`make verify`)·`acceptance-e2e` 는 코디네이터 몫 — 워커가 돌리지 않는다

## 금지 사항
- canonical(`/Users/kknaks/git/harness_works/ax-workspace`) 수정 금지 — 워크트리에서만 작업
- `frontend/`·spec 리포 수정 금지
- git commit·push·PR 금지
