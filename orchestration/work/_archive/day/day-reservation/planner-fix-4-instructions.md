# [planner] SPEC-006 고침 4 — 사용자 결정 R29 ~ R33 + 4차 WARN 3 · 사용자 리뷰 판

맥락이 없으면 먼저 읽어라: 원 브리프 `/Users/kknaks/orca/workspaces/kknaks_profile/day-ext/orchestration/work/day-reservation/day-reservation-spec-brief.md` · 고침 1 ~ 3 지시서(`/Users/kknaks/orca/workspaces/kknaks_profile/day-ext/orchestration/work/day-reservation/planner-fix-{1,2,3}-instructions.md`) · **결정 파일(갱신 — 맨 아래 「SPEC 4차 검수 뒤 결정」 R29 ~ R33)** `/Users/kknaks/orca/workspaces/kknaks_profile/day-ext/reference/2026-11-23-reservation/reservation-board-decisions.md` · 4차 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day-ext/orchestration/work/day-reservation/review-doc-4-report.md`

작업 워크트리: `/Users/kknaks/orca/workspaces/mediness-mediness/day-reservation-spec` (네 미커밋 변경 위에서)

## 고칠 것
1. **R29 (가장 큼)** — 갱신 = 중앙 한 번 최신화 · PC 는 DB 만. 화면 요청이 「보는 중인 날짜」 표시(만료 있음)를 남기고 서버 쪽 주기 작업이 보는 중인 날짜만 병원 · 날짜당 한 번 최신화(R26 범위 · C1 ~ C3 그대로) · PC 는 DB 사본만 주기적으로 다시 읽음 · 첫 열기는 즉시 최신화(R17 · C4). 오늘 = 지금 10초 회차. §3 조회 흐름 · API · 케이스 · Rule 을 이것으로. OQ-R10 · OQ-R22 닫음. 남는 것(주기 · 만료 시간 · 갱신 전달 폴링 / SSE · 보는 중 표시를 어디 둘지)은 새 OQ(기본안 표시 · 결정 아님). 함수 · 저장소 설계는 하지 않는다(WORK 몫) — 「보는 중 표시」가 담아야 할 정보(병원 · 날짜 · 만료)와 지킬 조건만
2. R30 · R31 · R32 · R33 — 해당 OQ 닫음(R33 의 R06 예외 · R03 ⓑ 주의). 닫은 OQ 는 OQ 표에서 「닫힘 → R 번호」로 옮기고 본문 「OQ-…」 자리를 결정으로 바꾼다
3. 4차 W4-1(R30 으로 정리 — C2 는 「중간 상태 안 보임」 · 실패 화면 = R30 이전 사본) · W4-2(오늘 화면에 C1 이 걸리는지 — 사실 + OQ, R29 와 맞춰) · W4-3(C1 범위 = 구매 · 시술권 · 선불카드 · 화면이 읽는 칸)
4. SPEC 머리에 「남은 OQ」 요약이 사용자 리뷰에서 바로 보이게 — 남은 OQ 는 결정 아님 · 구현 전에 닫을 것과 2루프로 미룬 것을 나눠 표시
5. `20-spec.md` · `10-decision.md` · `log.md` 개정 표기 · §8 검증 → §9 완료 보고
