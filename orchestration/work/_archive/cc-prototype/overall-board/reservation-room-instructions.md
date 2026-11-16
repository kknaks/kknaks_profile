# [researcher] 추가 지시 — 접수 · 방 배정 KOS 순서 (read-only 조사)

앞 판 `reservation-create-report.md` 에 이어지는 판이다. 역할 · 금지는 `reservation-read-research-instructions.md` §5 와 같다.
**⚠ 코디 핸들이 바뀌었다 — 완료 보고 · 질문은 `term_fa2737b7-e69a-40e1-9fac-019199b9dad3` 으로**(앞 판 §7 의 명령에서 핸들만 바꿔 쓴다). 옛 `term_e84a7eea…` 로 보내지 마라.

## 1. 무엇을 하나

사용자: 「지금은 방 배정이 엄청 복잡해 — 일단 순서로 보여 줄게」. 사용자가 KOS 데모에서 **한 고객을 접수하고 방을 배정한** 과정을 HAR 로 떴다. **KOS 에서 접수 → 방 배정이 실제로 어떤 순서 · 어떤 호출로 일어나는지**를 그대로 적는다. 시안의 「시술실 선택 → [접수 완료]」(design-analysis-report §3.4 바닥 줄 · 「접수 완료 · {방} 배정 · 데스크 {직원}」)와 비교한다.

## 2. 읽을 것

- `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/reference/2026-10-23-cc-overall-board/har/방배정.har` (gitignore · 123항목). 코디가 본 쓰기 순서(항목 번호):
  - #6 `schedule/v1/commands/recept` → #58 `schedule/etcetera-tasks/v1/queries/get-etcetera-tasks` → #60 `schedule/v1/commands/add-flow-tasks` → #72 `schedule/v1/commands/change-flow-step` → (#81 `get-rooms` · #83 `get-schedules-grouped-by-zone`) → #93 `schedule/flow/v1/commands/change-tasks-room` → #118 `schedule/v1/commands/change-flow-step`
  - 그 사이 조회: `search-product-option-summaries` · `get-ticket-bundles` · `get-vat-settings` · `get-payment-settings` · `get-tax-refund-settings`(400) 등
  - **이 목록으로 끝내지 말고 KOS 요청(OPTIONS · js · svg 제외)을 전부 세어** 인벤토리를 만든다
- 시술 현황이 이미 아는 것: `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/reference/2026-10-12-cc-prototype/workflow-v2.md` 「1. 시작 상태」(「방 배정」 ETCETERA 작업으로 방을 준다) · 「KOS 반영 표」(`change-tasks-room` · `cancel-flow-tasks`) · `orchestration/work/overall-board/_RESUME.md` §2 2026-10-25 「방 배정」 줄들
- 공개 스펙: `changeFlowStep` 등 접수 · 작업 관련 공개 작업

## 3. 할 일

1. **HAR 인벤토리**: KOS 요청 전부 — 순서대로, 메서드 · 경로 · 본문 키 · 응답 모양 · 화면에서 무엇을 눌렀을 때로 보이는지.
2. **쓰기 6건 해부**(순서대로): 본문 전체(값은 모양만). 특히
   - `recept`: 접수가 무엇을 바꾸나(flowStep · 접수 시각 · 구역 「접수: 4층」 · 접수 직원?) · 공개 `changeFlowStep(RECEPTION)` 과 차이
   - `add-flow-tasks`: 어떤 작업을 더하나(type · title 「방 배정」? · `get-etcetera-tasks` 의 기타 작업 목록과 관계) · 시술 작업 · 상품 옵션도 여기서 더하나
   - `change-flow-step` 2번: 각각 어느 단계에서 어느 단계로
   - `change-tasks-room`: 어느 작업(sequence)에 어느 방 · 방 배정 시각
3. **전후 상태**: HAR 의 `get-schedule-summaries` · `get-schedules-grouped-by-zone` · `get-schedule-detail` 응답으로 일정의 flowStep · tasks[](type · title · status · room · roomAssignedDateTimeUtc) · receptionDateTimeUtc 가 단계마다 어떻게 바뀌나. 지금 데모에서 같은 일정을 **조회**해 최종 상태 확인
4. **공개 짝**: 각 쓰기에 공개 API 가 있나(없으면 「공개 없음」)
5. **시안 비교**: 시안은 「방 선택 + 신분 필드 모두 입력 → [접수 완료] 한 번」. KOS 는 몇 단계인가 · ccc 가 [접수 완료] 한 번으로 묶으려면 어떤 호출을 어떤 순서로 보내야 하나(**결정하지 말고 KOS 순서만**) · 실패하면 중간 상태가 남나
6. 「정할 것」: 결정하지 마라. Q-63 부터

## 4. allowed_paths

- `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/orchestration/work/overall-board/reservation-room-report.md` — 리포트 1개

## 5. 하지 말 것

- **KOS 쓰기 0건** — HAR 에 찍힌 것만 해석
- 리포트에 id · 토큰 · 이름 등 값 금지(모양만)
