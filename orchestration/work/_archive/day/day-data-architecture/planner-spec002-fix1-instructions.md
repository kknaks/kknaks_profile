# [planner] DAY-SPEC-002 검수 WARN 반영(fix1)

너는 SPEC-002 를 쓴 day planner 다. 같은 mediness 워크트리 · 미커밋 그대로. 커밋 금지.
읽을 것: 검수 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/review-spec002-report.md` — WARN W1 ~ W11 · 「사용자 결정 OQ 8건 판정」 · 「cc 와 다른 곳」.

## 고칠 것 (리뷰어 고칠 방향대로 — 코디 결정)

1. **W1 ~ W11 전부** 리뷰어 「고칠 방향」대로. 특히 W5(재호출 대상 · 기본 선택은 OQ-04 가 닫힐 때까지 본문 U-5 · S-3 · API 에 「OQ-04 대기」) · W6(「반영 중」은 cc 대로 그리지 않음 — 스냅샷 `reflecting` 값만 둠) · W7(outbox → `event_id` → `event_log.actor_staff_id` → 그 직원의 만료 안 된 `external_session` · 없으면 `pending` 유지 · `attempts` 안 올림 — 이 한 줄을 규칙으로).
2. **답이 있는 OQ 닫기**(리뷰어 판정 그대로 · 근거 링크): OQ-02(제안 키를 기본값으로 · 코드에서 정함) · OQ-03(묶지 않음 — HAR 요청 쪽으로 옮김) · OQ-04 시간(ⓐ 열린 호출 `created_at` 부터) · OQ-05(① 수락한 의사 토큰 — 결과: DAY 에 로그인한 적 없는 의사를 대리 수락하면 KOS 에는 「반영 중」에 머문다 · 한 줄 명시) · OQ-06(① 시스템 계정) · OQ-07 표시(② 안 그림) · OQ-11(`staff.is_system_account` 로 — 새 칸 없음).
3. 남는 사용자 OQ 는 **OQ-01 · OQ-04(대상 · 기본 선택) · OQ-07(실패 복구)** 세 개 — 리뷰어가 짚은 반대 근거(OQ-01 의 AGENTS.md `routers/` · `routers/api/` 구분)를 선택지에 같이 적는다.
4. 「cc 와 다른 곳」 두 줄(수락된 시술은 원장을 바꿀 길 없음 · 수락 창 기본 선택)을 SPEC 에 사실로 적는다(결정 아님 — 기본 선택은 OQ-04 와 같이 열어 둠).
5. log 한 줄 · lint `--strict` 1회.

리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/planner-spec002-fix1-report.md` — W 별 고친 줄 · 닫은 OQ · 남은 OQ 3. 완료는 preamble 의 worker_done 절차대로(`orca orchestration send` 와 `orca terminal send` 둘 다).
