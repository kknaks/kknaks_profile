# [planner] #965 스펙 맞추기 — 구현에서 정한 것 반영 (sync-1)

같은 워크트리(`/Users/kknaks/orca/workspaces/mediness-mediness/day-kos-call-notify-spec` · 브랜치 `kknaksss/day-kos-call-notify-spec` · head b3898f8d). 코드는 읽기만(`/Users/kknaks/orca/workspaces/CENTURION_DAY/day-kos-call-notify` 미커밋).

반영할 것 — 원천 = `/Users/kknaks/orca/workspaces/kknaks_profile/day-시술/orchestration/work/day-kos-call-notify/be-fix-1-report.md` 「스펙 반영 필요」 1 ~ 4 + `/Users/kknaks/orca/workspaces/kknaks_profile/day-시술/orchestration/work/day-kos-call-notify/be-impl-r1-report.md` 「_apply_tasks 를 타는 모든 커밋 경로」 표:

1. 규칙 40 ① 「바뀌었고」 → 「늦어졌고(앞으로만 · 빈 값 → 값 포함)」 · 근거 코드 검수 r1 W1.
2. 규칙 40 ①(또는 ⑧) `event_log` `call.create` payload `kosCalledAt` · 이미 만든 KOS 시각 최댓값 이하면 안 만듦 · `doctor_called_at` 저장 규칙 그대로 · 형식 틀린 행은 건너뜀(be-fix-2 I-a).
3. SPEC-005 「KOS 에서 건 호출」 받는 계정 · 규칙 40 ②: 시스템 계정 직원 호출 `kind = one` 받는 사람 = `target_staff_id` ∪ called_doctor 원장 · OQ-107 ⓒ 결과 문장 갱신.
4. 규칙 40 ② 대표 = 묶음에서 sequence 가 가장 작은 작업의 calledDoctors 첫 원장.
5. 규칙 40 머리 · SPEC-005 「언제」 ②의 「(ㄱ)(ㄴ) 두 경로」 → 코드 표 그대로(10초 일정 조회 · 예약 상세 연쇄 두 커밋 · 외부 연동 `ext_sync` `_load_date` · `_save_scoped_schedules` 커밋) · `emr_date_sync` · `emr_backfill` 은 오늘 아님이라 제외(근거 be-impl-r1-report 의 :172 · :161).
6. 개정 ㉚ 머리 요약 맞추기 · log.md 한 줄.

금지: 위 밖 계약 변경 · 코드 레포 수정 · #965 머지. lint `--strict` products/day ERROR 0 → **커밋 · PR #965 에 push**.

보고 `/Users/kknaks/orca/workspaces/kknaks_profile/day-시술/orchestration/work/day-kos-call-notify/planner-sync-1-report.md` · 완료 보고는 terminal send 한 줄(「[done] planner sync-1 …」)로.
