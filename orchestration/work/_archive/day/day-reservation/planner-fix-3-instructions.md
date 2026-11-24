# [planner] SPEC-006 고침 3 — 3차 검수 FAIL 2 · WARN 3

맥락이 없으면 먼저 읽어라: 원 브리프 `/Users/kknaks/orca/workspaces/kknaks_profile/day-ext/orchestration/work/day-reservation/day-reservation-spec-brief.md` · `planner-fix-1-instructions.md` · `planner-fix-2-instructions.md` · 결정 파일 `/Users/kknaks/orca/workspaces/kknaks_profile/day-ext/reference/2026-11-23-reservation/reservation-board-decisions.md` · **3차 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day-ext/orchestration/work/day-reservation/review-doc-3-report.md`** (경로 앞부분 = `/Users/kknaks/orca/workspaces/kknaks_profile/day-ext/orchestration/work/day-reservation/`)

작업 워크트리: `/Users/kknaks/orca/workspaces/mediness-mediness/day-reservation-spec` (네 미커밋 변경 위에서)

## 코디 방향 — SPEC 은 「요구 조건」을 적고 함수 설계는 하지 않는다

지금 함수(`run_schedules` · `emr_kos_keys.apply_isolated` · `sync_sales_hospital`)는 「오늘」 전제(같은 병원 잠금 · 못 잡으면 조용히 건너뜀 · 단계마다 따로 commit · 발행 시각 순서)로 짜여 있다. 다른 날짜에 그대로 부르면 R20 · R26 · R27 을 못 지킨다. SPEC 에는 **날짜 최신화가 지켜야 할 조건**을 계약으로 적고, 지금 함수가 그 조건을 어디서 못 지키는지를 사실(파일:줄)로 적는다. 어떻게 고칠지(함수 · 잠금 키 · transaction 설계)는 WORK 몫 — SPEC 에서 설계하지 않는다.

조건(이대로 계약에 넣는다):
- C1 **완성된 상태만 보인다**: 그 날짜의 일정 · KOS 키 보충(그룹 칸) · 구매(결제 포함)가 모두 반영된 상태만 화면 읽기에 보인다. 일정만 반영되고 그룹 칸이 빈 중간 상태를 읽는 순서가 없다(F3-2 · R20 · R27)
- C2 **조용히 건너뛰지 않는다**: 날짜 최신화는 오늘 10초 회차의 잠금 때문에 단계를 건너뛰지 않는다. 못 하면 실패로 끝나고 이전 사본을 그린다(F3-1)
- C3 **구매 단계도 그 날짜 것**: 구매 회차의 「오늘」 가정(발행 시각 순서 · 병원 잠금)에 걸려 그 날짜 메시지가 버려지지 않는다(W3-1 — 사실은 적고 조건으로)
- C4 **그리는 시점(OQ-R28 기본안 변경)**: 세 단계를 다 받은 뒤 그린다. KOS 실패 · 시간 초과면 이전 사본을 그린다. 결정이 아니라 기본안 — 「사용자 확인」 표시(W3-2 의 충돌은 이 기본안으로 사라지는지 확인해 적는다)

## 고칠 것
1. F3-1 · F3-2 · W3-1 · W3-2 — 위 C1 ~ C4 로. S6:L278 · L311 「오늘 회차와 서로 막지 않음」 문장 · L268 「순서 그대로」(오늘 태스크는 구매 발행 :98-110 이 키 보충 :111 보다 먼저) 바로잡기
2. W3-3 — `10-decision.md` 결정 범위 표기
3. `20-spec.md` · `10-decision.md` · `log.md` 개정 표기
4. §8 검증 → §9 완료 보고
