# [planner] 스펙 4차 — 검수 3차 잔재 2줄

같은 워크트리 · 같은 범위 · 같은 제약. `review-doc-3-report.md`(`/Users/kknaks/orca/workspaces/kknaks_profile/day-mobile-v2/orchestration/work/day-mobile-v2/`)의
- **N-1** SPEC-005 :458 OQ-N16 행 「줄마다 취소하면 알림은 취소 횟수만큼 온다」 → 취소선 + OQ-N17(완전히 닫힐 때만 · 일부 취소 = 알림 없음)로
- **N-2** SPEC-005 :473 §5 모델 대조 「호출 취소 알림을 쓰지 않음 · migration 없음」 → 취소선 + SPEC-000 enum migration(`doctor_call_cancel`)으로
- **N-3** 사슬로 여러 호출이 함께 닫힐 때 알림 행 `doctor_call_id` — 지금 코드 사실(한 호출만 닫힘)을 한 줄로 적고 넘어간다

이 셋만. lint `--strict` products/day ERROR 0. 리포트 `spec-4-report.md`(같은 폴더). 커밋 · PR · Issue 수정 금지. 완료 보고는 dispatch preamble 의 worker_done 그대로.
