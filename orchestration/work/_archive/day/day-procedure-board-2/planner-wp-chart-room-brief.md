# [planner] WP — 차트 작성 · 방 이동 Delivery 발행

같은 스펙 워크트리(PR #920 · 마지막 커밋 4490876e · 미머지). `start-delivery` 규칙. 파일 수정 · 커밋 금지 — Issue 만.

## 할 것
CENTURION_DAY 에 Delivery Issue — **새 Issue 하나**(새 key 예 `day/board-chart-room` · target DAY-SPEC-002 개정 ⑯ · DAY-SPEC-000) 를 권함. #236 에 붙이는 것이 레포 규칙상 맞다면 그 이유를 보고하고 그렇게 해도 된다(#236 은 이미 승인된 v3 — 붙이면 재승인 필요).
- 결과 계약 = 개정 ⑯ 전부: U-14 차트 · U-15 방 이동 · U-12 「시술 완료」 탭 원래 방 묶음 · 「방 배정」 판정 = `room_assign_etc_task_id`(e2e F10 — 지금 기타 작업 전부가 숨겨지는 버그 고침 · 기타 작업도 [종료]해야 [귀가 대기]) · 데이터 `visit_task.started_room_id` · `visit_task.is_room_assign` · 새 `visit_task_chart_log`(migration) · 데모 연결 설정 값 넣기(로컬 · dev 데이터 — 방법은 Execution 에)
- Acceptance 항목별(화면 · API · infra 테스트 · **데모 실물**: 점유 이동 · 복귀 · 이동 KOS 반영 · 「방 배정」 새로 만들기 · 차트 메모 · 집도의 KOS 반영 · KOS 웹 수정 → DAY 반영 · 진행 중 작업 이동 — 스펙 OQ-38 · 39 확인 안 됨 묶음)
- Non-Goals: SPEC-002 「이번에 안 하는 것」 표(일괄 적용 · 작성자 여러 명 · 지난 방문 차트 · 침대 수 · 관리실 기록 창 · 날짜 이동 등) · 토스트 글자 정리(별도) · 10초 판 전체 다시 그리기(OQ-37)
- Execution: 코드 레포 `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-procedure-board-2`(PR #238 브랜치 · 커밋 caa72435 위 + **미커밋 F9 시술 완료 카드 머리 수정** 있음) · phase(backend 데이터 · migration / 차트 서비스 · KOS op · 동기화 guard · 이력 / 방 이동 서비스 · KOS op / 화면 / 검증 · 데모 실물) · rollback
- baseline pending. L2/L3 면 `delivery-plan:review` 에서 **멈춘다**(승인 대행 금지)

## 완료 보고
Issue 번호 · URL · risk · plan_digest · 라벨 · Target Delta/Acceptance 요약. 코디 핸들 `term_28f2b422-a0ae-490a-bbed-aeb19fbd7fdd`(worker_done + terminal send).
