# WP-KOS — 되돌리기 KOS 실호출 확인 (backend · 코드 변경 없음)

정본: `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/para/projects/summer-star/cc-prototype/30-work/work-006-overall-board-undo.md` **WP-KOS 행 그대로**(K1 ~ K6 · 완료 조건 · public 규칙) + SPEC-003 0.5.0 §5.13 · §8 · OQ-528 · OQ-529 · OQ-530.

- 리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/orchestration/work/overall-board/kos-undo-probe-report.md`
- env: `/Users/kknaks/orca/workspaces/cc-prototype/overall-board/procedure/.env`(데모 테넌트 · 값 출력 금지). 운영 명동점 키 금지.
- 스크립트는 scratchpad 에 · 코드 레포에 남기지 않는다. 사용자 스택(3700 · 8700)은 건드리지 않는다(떠 있는 back 이 KOS 를 폴링하니 데모 일정 변화가 화면에도 보인다 — 정상).
- **대상 일정**: 오늘(KST) 데모 4층 일정 중 방 있는 것. 방 없는 ETCETERA(시트팩 등)가 붙은 일정이 없으면 K1 ~ K4 는 PROCEDURE 로 먼저 하고, **K5 직전에 멈춰 질문 채널로 「ETCETERA 작업 붙은 일정 필요」라고 물어라**(사용자가 KOS 화면에서 붙인다). 오늘 일정이 아예 없으면 바로 물어라 — 데모 환자 생성 스크립트를 마음대로 돌리지 마라.
- 끝에 OQ-528 · OQ-529 · OQ-530 각각 「받음 / 안 받음」 한 줄 판정 + K2 뒤 실제 작업 status.
- 보고는 §9 두 채널.
