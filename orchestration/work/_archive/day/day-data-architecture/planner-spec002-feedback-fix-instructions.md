# [planner] SPEC-002 개정 ⑥ 검수 반영 — W1 ~ W4 · OQ-09 · OQ-21 (+ SPEC-000)

너는 day planner 다. 미커밋 · 커밋 금지. 읽을 것: `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/review-spec002-feedback-report.md` W1 ~ W4 · OQ 판정 · 「같이 정리할 것」 · 원천 `/Users/kknaks/orca/workspaces/kknaks_profile/day/reference/2026-11-03-cc-day/screen/procedure-board-decisions.md`(코디가 바로잡음: cc 토큰 근거 · 방배정.har · 「결정 — 코디」 OQ-21 · 「결정 — 다시 호출」에 OQ-09 · 카드 메모).
- **W1** 새 flow-step 값(내부 경로) = 「데모 지점 실물 확인 전 미확인 · 확인 전 운영 병원엔 열지 않음」 · 방배정.har 근거 삭제.
- **W2** 「cc 와 같음」 → 「KOS 는 대리 수락을 받는다(cc D-27 실호출)」.
- **W3 · W4** 리뷰어 방향대로.
- **OQ-09 닫음**: 다시 호출 · 재호출도 KOS `call-tasks-doctors` 다시 보냄(cc · 사용자) · 실물 확인 뒤 운영.
- **OQ-21 닫음**: `external_outbox.sender_staff_id`(토큰 고르기 전용 · KOS 떼면 같이 지움) — SPEC-000 표 · 규칙 24.
- F8 결론: 카드 = 오더 메모만(상담 메모 안 보임) · `procedure_order_note ← orderMemo`(일정 단위) 표 확인.
log · lint. 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/planner-spec002-feedback-fix-report.md`. 완료는 preamble 의 worker_done 절차대로(둘 다).
