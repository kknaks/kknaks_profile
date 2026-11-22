# [backend] P2 — 앱 기기 선택 JSON · 바로 시작 JSON · 스냅샷 can* 3칸 (DAY 직원 앱 0.2.0)

같은 워크트리 `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-mobile-v2` · 브리프 `/Users/kknaks/orca/workspaces/kknaks_profile/day-mobile-v2/orchestration/work/day-mobile-v2/day-mobile-v2-be-brief.md` 의 역할 · 규칙 · 검증 · 금지 그대로(§5 allowed_paths 만 아래로 바꿈). P1 은 커밋 `a7868dc6` 로 들어갔다. ⚠ mobile 워커가 같은 워크트리 `app/` 에서 작업한다 — `app/` 건드리지 마라 · git 은 읽기만(stash · checkout · commit 금지 · 커밋은 코디). reviewer 가 P1 을 읽는 중 — `services/interpret` 등 P1 파일은 건드리지 마라.

## 정본 (PR 브랜치 스펙 · 머지 전)
- `/Users/kknaks/orca/workspaces/mediness-mediness/day-mobile-v2-spec/products/day/20-spec/spec-001-login-session.md` **개정 ⑩** 전부 — 앱 `POST /api/auth/login` 이 기기 제한이면 `choose_device`(웹 #257 service 재사용 · 앱용 JSON) · `POST /api/auth/device`(OQ-K18 기본값) · 데모 넘김(prod→dev) `adapters/environments.py` `read_success` 가 `choose_device` 를 받게 · 케이스 매트릭스 · 만료 · 잘못된 선택 · 재차 막힘 · OQ-K19 · K20
- `/Users/kknaks/orca/workspaces/mediness-mediness/day-mobile-v2-spec/products/day/20-spec/spec-002-procedure-board.md` **개정 ㉕** — 바로 시작 앱 JSON `/api/visits/{id}/quick-start`(`board.quick_start` 재사용 · 일부/전부 거절 응답 OQ-77 기본값) · 스냅샷 `canCancelCall` · `canQuickStart` · `canChangeDoctor`(판정 = 서비스 거절 규칙 · OQ-78 · 개정 ㉕ ③)
- 웹 기준 코드: `backend/day/services/auth.py`(기기 선택 · pending) · `routers/login.py` · `routers/board.py:610` quick_start · `policies/board_rules.py` · `presentation/board.py`
- 조사 지도 `/Users/kknaks/orca/workspaces/kknaks_profile/day-mobile-v2/orchestration/work/day-mobile-v2/research-current-state.md` §B · §C

## allowed_paths
- `backend/day/routers/api/` · `backend/day/schemas/` · `backend/day/services/auth.py` · `backend/day/services/board*.py`(재사용에 필요한 만큼) · `backend/day/presentation/board.py` · `backend/day/adapters/environments.py` · `backend/day/dtos/`(필요 칸만) · 관련 테스트
- 웹 라우트 · 템플릿 · static 금지(웹 동작 바뀌면 안 됨). migration 금지.
- 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day-mobile-v2/orchestration/work/day-mobile-v2/be-p2-report.md`

## 검증
- 관련 테스트 + 새 테스트 · ruff — 1회씩. **웹 동작 무변경 확인**(웹 로그인 · 웹 바로 시작 기존 테스트 그대로 통과).
- 실물: 로컬에서 KOS 데모 테넌트로 앱 로그인 JSON 1회(기기 제한이 실제로 안 걸리면 목으로 · 사용자 포트 금지). 못 하면 pending.
- 리포트: 새 경로 · 요청/응답 예시(값은 가짜) · 오류 코드 표 · 바꾼 파일 · 테스트 수치 · 스펙과 다른 곳(있으면 멈추고 질문).

완료 보고는 dispatch preamble 의 worker_done 그대로. 커밋 · push · PR 금지.
