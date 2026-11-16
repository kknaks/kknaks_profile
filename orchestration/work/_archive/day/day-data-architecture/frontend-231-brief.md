# [frontend] Delivery #231 — 시술 현황 1차 ② 화면 (DAY-SPEC-002)

너는 #229 · 웹 로그인을 만든 day frontend 워커다. 같은 워크트리 · #224 ~ #229 커밋 + **#230 백엔드 미커밋 변경이 있다(다른 워커 작업 · 지금 검수 중)** — 백엔드 파일(services · routers 의 로직 · emr · models · migrations)은 고치지 마라. 필요하면 `[질문]`.
## SSOT
- 계약 Issue #231 `gh issue view 231 -R MediSolveAIDev/CENTURION_DAY` · 검수 `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/review-delivery230-231-report.md` · `-v2-report.md`.
- **#230 이 남긴 조각 계약 표(A9)** — `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/backend-230-report.md` 의 라우트 · 조각 이름 · 넘기는 값 · SSE 이벤트(`board` · `kos_failed`) · 토스트. 자리 템플릿을 실제 화면으로 채운다.
- 화면 정본: SPEC-002 `/Users/kknaks/orca/workspaces/mediness-mediness/day-data-architecture-spec/products/day/20-spec/spec-002-procedure-board.md` 화면 구성(E 번호) · 원천 `/Users/kknaks/orca/workspaces/kknaks_profile/day/reference/2026-11-03-cc-day/screen/procedure-board-decisions.md`(의사 호출 창 · 수납 필요 · U1 ~ U12) · 시안 `/Users/kknaks/orca/workspaces/kknaks_profile/day/reference/2026-11-03-cc-day/screen/시술현황_프로토타입 (1).html`(생김새).
- **#229 매크로만**으로 조립 — 손 CSS 0 · 인라인 스크립트 · `hx-on` 0 · 동작은 `day.js`(이벤트 위임 + data-*).
## 하지 말 것
백엔드 로직 · 앱 · 방 옮기기 · 차트 작성 · KOS 쓰기 · 커밋. **compose 는 사용자가 보는 중 — down 금지**, 끝나면 `--profile app up -d --build api` 로 새 코드만.
## 검증 · 보고
계약 Acceptance · `uv run pytest -m "not infra"`(템플릿 렌더 테스트) · ruff · **브라우저 실물**: 로그인 → 시술 현황 → 카드 · 인박스 · 의사 호출 창 · 수락 · 시작 · 종료 · 마취 · D&D · 확인 필요 · 수납 필요 · SSE 갱신을 데모 지점 데이터로(데모 오늘 일정이 0건이면 그 사실과 함께 빈 상태 + 견본 데이터 화면) · 스크린샷 `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/frontend-231-shots/`. 권한: 사용자가 `DAY_ADMIN_EMAILS` 를 넣지 않았으면 권한 없음 화면이 뜬다 — 그 경우 테스트로만 확인하고 리포트에 적어라(값을 직접 넣지 마라).
리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/frontend-231-report.md` — Acceptance · E 번호 ↔ 템플릿 · 스크린샷 · 사용자가 열 URL. 완료는 preamble 의 worker_done 절차대로(둘 다).
