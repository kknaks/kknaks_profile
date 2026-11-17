# [planner] spec-5 — 마감 전 문서 정리 (작은 판)

너는 앞 맥락이 없다. 원 브리프 `/Users/kknaks/orca/workspaces/kknaks_profile/day-fix-feedback/orchestration/work/fix-feedback/fix-feedback-spec-brief.md`(역할 · allowed_paths `products/day/` · 검증)를 따른다. 작업 워크트리 `/Users/kknaks/orca/workspaces/mediness-mediness/fix-feedback-spec`(미커밋 위에). 커밋 · push 금지.

검수 `…/fix-feedback/review-doc-3-report.md` 의 아래만 고친다:
- **F1** `spec-005-notifications.md:444` 「모델 대조」의 「호출 취소 알림 = notification_kind enum migration 1개」 문장 → 취소선 + 「→ 이번엔 호출 취소 알림을 쓰지 않음 · migration 없음(사용자 2026-11-17 · 다음 스펙)」.
- **W1** `spec-005:34` 「`document.hidden` 일 때만」 → 취소선 + 「→ 늘(2차 개정 E5)」.
- **W2** `spec-003:70` ② OQ-62 구절 → 취소선 + 「→ ⑦」.
- **W4** spec-002 규칙 38 끝에 「원래 원장 호출 알림 행 · 앱 푸시는 그대로 — 그걸로 수락하면 기존 규칙(남은 줄 없으면 `call_closed` · 있으면 남은 줄만)」 한 줄.
- 그리고 2루프 코드 사실 한 줄: SPEC-002 스냅샷 `systemDoctor` 는 **진행중 · 완료 줄에서만 참**(be-3 · N1 — `board_rules.py` `system_doctor`).

`python3 scripts/lint-pipeline.py --strict` products/day ERROR 0. 리포트 `…/fix-feedback/spec-5-report.md`(짧게). 완료 보고는 preamble 의 worker_done.
