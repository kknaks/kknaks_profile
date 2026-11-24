# [planner] SPEC-006 → WP 나누기 · Delivery Issue 발행

너는 SPEC-006 을 쓴 planner 다. SPEC 은 사용자 승인 · 커밋됨: 브랜치 `kknaksss/day-reservation-spec` `1870f68c` · PR MediSolveAIDev/mediness#958(머지 전).
맥락이 없으면 읽어라: SPEC `products/day/20-spec/spec-006-reservation-board.md` · 결정 파일 `/Users/kknaks/orca/workspaces/kknaks_profile/day-ext/reference/2026-11-23-reservation/reservation-board-decisions.md`(R1 ~ R41) · 원 브리프 `/Users/kknaks/orca/workspaces/kknaks_profile/day-ext/orchestration/work/day-reservation/day-reservation-spec-brief.md`(§5 · §9)
Delivery 절차: `start-delivery` 스킬 · `rules/delivery-workflow.md` · `tools/harness/references/requests.md` (이 워크트리)

작업 워크트리(문서): `/Users/kknaks/orca/workspaces/mediness-mediness/day-reservation-spec`
코드 워크트리(읽기만): `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-reservation` (origin/dev `5ece25ea`) — 레포 루트 `AGENTS.md` 를 먼저 읽는다

## 할 것
1. SPEC-006 을 구현 단위(WP)로 나눈다. 축 제안(근거 있으면 바꿔도 됨 · 이유를 적는다):
   - **backend** — 조회(전체 페이지 · HTMX 조각 · 10초 다시 읽기 — DB 만) · 다른 날짜 최신화 요청 → 중앙 작업(R40 · 같은 (병원 · 날짜) 잠금 · R26 범위 일정 → 키 보충 → 구매 · 시술권 · 카드 · 조건 C1 ~ C3 — 지금 함수가 못 지키는 곳은 SPEC 사실 표) · 권한 키(R31 — DAY-SPEC-002 개정 ⑲ board 방식 기본값 행)
   - **frontend** — Jinja2 + HTMX 화면(시안 정본 · 문구 짓기 금지 · 인라인 스크립트 0 · 손 CSS 0 — CENTURION_DAY 화면 규칙)
   - BE ↔ FE 계약(조각 경로 · 넘기는 값)은 WP 에 명시 → 둘이 병렬로 갈 수 있게. 단계 의존은 실제 순서만(전부 직렬 금지)
   - 각 WP: 범위 · 완료 조건(실물 e2e 1회 — 로컬 KOS 데모 지점에서 오늘 · 다른 날짜 열기 · 같은 날짜 동시 열기) · migration 필요 여부 · 되돌리기
2. Delivery Issue 발행 — `mediness start-delivery --mediness-repo /Users/kknaks/orca/workspaces/mediness-mediness/day-reservation-spec --code-repo /Users/kknaks/orca/workspaces/CENTURION_DAY/day-reservation --github-repo MediSolveAIDev/CENTURION_DAY` `--plan` → `--apply`. baseline = SPEC PR 커밋 `1870f68c`(머지 전). harness 가 main 머지를 요구해 막히면 **우회하지 말고** 막힌 이유 · 명령 출력을 그대로 보고. **승인 receipt 는 적용하지 마라**(사용자 몫). plan / request / apply json 은 `/Users/kknaks/orca/workspaces/kknaks_profile/day-ext/orchestration/work/day-reservation/delivery/` 에 남긴다
3. `30-work.md` Spec Coverage 행을 Delivery 번호로(lint 규칙대로) · `log.md` 한 줄 — 커밋하지 마라(코디가 PR #958 에 얹는다)

## 금지
코드 수정 · 커밋 · push · PR · SPEC 본문 계약 변경(필요하면 멈추고 보고).

## 보고
`/Users/kknaks/orca/workspaces/kknaks_profile/day-ext/orchestration/work/day-reservation/delivery-1-report.md` — Issue 번호 · WP 표(범위 · 의존 · 완료 조건) · BE ↔ FE 계약 · baseline · 막힌 것. 완료 보고는 preamble 의 worker_done.
