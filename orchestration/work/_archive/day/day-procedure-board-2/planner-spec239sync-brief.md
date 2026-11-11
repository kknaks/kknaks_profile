# [planner] 스펙 맞추기 — #239 리뷰 반영분 (스펙만 · 커밋 금지)

스펙 워크트리(브랜치 `kknaksss/day-procedure-board-2-spec` = #921 head 987b2dc7 와 같음). 코드 반영 내용(사용자 결정 2026-11-11 · 워커 보고)을 SPEC-002 에 맞춘다:
- 동기화 표 `visit.room_id` = 「방 배정」 작업을 뺀 가장 늦게 배정된 작업의 방(설정 id 있을 때 · 다른 방 붙은 작업이 없으면 지금 값 그대로)
- KOS 쓰기 표 점유 이동(방 배정 없음) 순서 = add-flow-tasks → 확인 → ①새 「방 배정」 → 원래 방 ②나머지 → 새 방(change-tasks-room)
- 스냅샷 `cards[].canHoldMove`(이동 가능 + 지금 방 방 배정 있음 또는 설정 id 있음) · OQ-49 = 설정 비면 「점유 이동」 버튼 꺼짐 + 서버 기존 409 conflict · `room_assign_unset` 제안 삭제
- 매트릭스 「방 배정 이름 못 구함」 = 409 conflict(조용히 이동 아님)
- OQ-39 · #239 리뷰 W4: 완료 시술 집도의 변경은 KOS 상태 안 바뀜(사용자 · 차트작성3.har) — 확인됨
log.md 11-11 행 · lint --strict products/day ERROR 0. 커밋 · push · Delivery 금지. 완료 보고 두 명령(코디 핸들 `term_28f2b422-a0ae-490a-bbed-aeb19fbd7fdd`) · subject 'planner #239 반영 스펙'.
