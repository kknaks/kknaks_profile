# [planner] DAY-SPEC-002 재검수 반영(fix2) — N1 · N2 (+ 사용자 OQ 답이 오면 같이)

너는 SPEC-002 planner 다. 같은 mediness 워크트리 · 미커밋. 커밋 금지. 읽을 것: `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/review-spec002-fix1-report.md` N1 · N2.

1. **N1** — 규칙 9 · 닫은 OQ-05 「결과」에 한 줄: 「그 의사가 DAY 에 로그인할 때까지 같은 방문의 뒤 KOS 쓰기(첫 시작 · 종료 · 귀가 대기)도 함께 멈춘다 — KOS 화면에서는 그 고객이 시술 대기 · 미완료로 남는다」. 규칙 24 는 바꾸지 않는다.
2. **N2 — 코디 판정(리뷰어 전제 정정)**: DAY worker 는 이미 **병원 연결 설정의 시스템 계정**(`crm_connection.config` `system_email` · `system_password`)으로 sign-in 하고 `get-user-account` 로 그 계정 id 를 얻는다(#226 · 코드 `backend/day/emr/kos/` · PR #228 `8c85233a`). #226 은 `staff.is_system_account = true` 를 **그 sign-in 계정 하나에만** 켠다(공용 · 마취용 등 다른 사람 아닌 계정은 KOS 에 표시 칸이 없어 켜지 않음 — #226 검수 W8 · 사용자 결정 대기). 그러니:
   - 규칙 25 `assigneeIds` = 「그 병원 연결의 시스템 계정(sign-in 계정 = `is_system_account` 인 직원) KOS id」 — 하나로 정해진다. 새 칸 없음.
   - 규칙 19 · OQ-11(원장 목록에서 마취용 · 공용 계정 빼기)은 **다시 연다**: 지금 `is_system_account` 는 sign-in 계정 하나뿐이라 마취용 · 공용은 빠지지 않는다. 「뺄 계정을 어디서 표시할지 = 사용자 결정(#226 W8)」 OQ 로.
3. log 한 줄 · lint `--strict` 1회.

리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/planner-spec002-fix2-report.md`. 완료는 preamble 의 worker_done 절차대로(둘 다).
