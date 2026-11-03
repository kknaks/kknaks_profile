# 05 시술 현황 (작업)

2026-11-03 사용자와 정함. 공통 규칙은 [README.md](README.md). 검토표: https://claude.ai/artifact/7NurJfkmN59QEeRgca7zcf

## 정한 것

- **시술 현황 = 작업(`visit_task`)** — cc 의 `procedure` 테이블을 이름만 바꾼 것(KOS 「시술(진료 행위)」과 헷갈리지 않게).
  작업은 수납에서 생긴 시술권(또는 추후 수납이면 상품 옵션 · 기타 작업)에서 꺼내 만든다 — 03 「시술 개념 셋」.
- **1차는 스냅샷만**(cc 방식 · 04-1 보류): 옵션 · 진료항목 이름 · 단위 · 약물 · 시술권 회차 · 기타 작업 이름을 KOS 작업 응답에서 받아 적는다.
- **cc 가 읽지 않던 KOS 칸도 넣는다**(사용자 2026-11-03): 마취 종류 · 시술메모 · 담당자/의사 메모 · 준비 시각 · 방 배정 시각 · 회차 등.
  KOS 오더지와 같은 수준으로 보여 준다. 동기화 때 같은 응답에서 받는다(따로 호출 없음).
- 작업 ↔ 직원(담당자 · 집도의 · 호출된 의사)은 `visit_task_staff` 연결 테이블 — cc 의 JSON 목록을 쓰지 않는다.
- KOS 작업은 id 가 없다 — 외부 id = KOS 스케줄 id + 작업 순번(`external_ref`), KOS 에 쓸 때 `sequence` 로 가리킨다.
- DAY 만의 기록: 의사 호출 · 호출 작업 · 수락 · 마취 시간 · 카드 순서 · 동작 기록.
- KOS 를 떼면 지우는 것: `external_outbox`(외부 쓰기 큐 — cc `kos_op`).
- cc 테이블 9개가 어디로 갔는지: `procedure` → `visit_task` · `visit_task_staff` / `doctor_call` · `doctor_call_item` · `call_accept` →
  `doctor_call` · `doctor_call_task` · `doctor_call_accept` / `anesthesia` → `visit_anesthesia` / `board_order` → `board_card_order` /
  `event_log` → `event_log` / `kos_op` → `external_outbox` / `kos_token` · `sync_state` → `external_session` · `external_ref` · 서버 상태.

## `visit_task`

| 묶음 | 필드 | 타입 | 필수 | 설명 | 외부(KOS) |
|---|---|---|---|---|---|
| 식별 | `id` | uuid PK | ✓ | 작업 1개 = 시술 현황 카드 안의 한 줄. 외부 id = KOS 스케줄 id + 작업 순번(external_ref) |  |
|  | `visit_id` | uuid FK → visit | ✓ | 방문 1 : 작업 N |  |
|  | `kind` | enum procedure · etc | ✓ | 시술(시술권 · 상품) / 기타 작업(방 배정 · 마취 · 시트팩 …) (cc: procedure.kind) | type · etceteraConfiguration |
|  | `sequence` | int | ✓ | KOS 작업 순번 — KOS 에 쓸 때 이걸로 가리킨다(KOS 작업은 id 가 없다) (cc: procedure.kos_sequence) | sequence |
|  | `sort_order` | int | ✓ | 작업 순서 — 오더지 인쇄 순서 (cc: procedure.kos_order) | order |
|  | `status` | enum not_started · waiting · ready · done · canceled | ✓ | 작업 상태 (cc: procedure.kos_status) | status (FLOW_TASK_STATUS) |
| 스냅샷 (1차 — 메뉴 테이블 없음) | `title` | varchar | ✓ | 카드에 보이는 이름 (cc: procedure.title) | title |
|  | `option_title` | varchar |  | 상품 옵션 이름 (cc 에 없던 새 칸) | productOptionConfiguration.optionTitle |
|  | `medical_service_title` | varchar |  | 진료항목 이름 (cc 에 없던 새 칸) | medicalServiceConfiguration.title |
|  | `unit_type · unit_value` | enum · numeric |  | 단위 · 용량 (cc · unit · shot …) (cc 에 없던 새 칸) | medicalServiceConfiguration.unit |
|  | `ticket_round_current · ticket_round_total` | int |  | 시술권 회차 — 3 / 10 (cc 에 없던 새 칸) | ticketConfiguration.round |
|  | `etc_task_title` | varchar |  | 기타 작업 이름 (방 배정 등) (cc: etc_task_def) | etceteraConfiguration.name |
|  | `medicines` | varchar[] |  | 쓰는 약물 이름 — 스냅샷 (cc 에 없던 새 칸) | medicalServiceConfiguration.medicines[] |
| 진행 | `payment_required` | bool | ✓ | 수납 필요 — 추후 수납으로 넣은 시술 (cc: procedure.payment_required) | paymentRequired |
|  | `anesthesia_type` | enum sedation · spray · cream · dental · gas · ice · cream_dental |  | 마취 종류 (cc 에 없던 새 칸) | anesthesiaType |
|  | `procedure_note` | text |  | 시술메모 (부위 · 요청사항 · 용량) (cc 에 없던 새 칸) | memo |
|  | `assignee_note · doctor_note` | text |  | 담당자 메모 · 의사 메모 (cc 에 없던 새 칸) | assigneeMemo · doctorMemo |
|  | `room_id` | uuid FK |  | 이 작업이 들어간 방 (cc: procedure.room_kos_id → room(6번)) | room.id |
|  | `room_assigned_at` | timestamptz |  | 방 배정 시각 (cc 에 없던 새 칸) | roomAssignedDateTimeUtc |
|  | `ready_at` | timestamptz |  | 준비 완료 시각 (cc 에 없던 새 칸) | readyDateTimeUtc |
|  | `doctor_called_at` | timestamptz |  | 의사 호출 시각 (cc: procedure.doctor_call_at) | doctorCallDateTime |
|  | `doctor_assigned_at` | timestamptz |  | 집도의 배정 시각 (cc: procedure.doctor_assigned_at) |  |
|  | `started_at` | timestamptz |  | 시술 시작 — DAY 에서 누름(KOS 에 없는 칸) (cc: procedure.started_at) |  |
|  | `completed_at` | timestamptz |  | 시술 완료 (cc: procedure.completed_at) | completedDateTimeUtc |
|  | `created_at · updated_at · deleted_at` | timestamptz | ✓ | 동기화 칸(synced · present)은 external_ref |  |

## `visit_task_staff`

| 필드 | 타입 | 필수 | 설명 | 외부(KOS) |
|---|---|---|---|---|
| `task_id · staff_id · role` | uuid · uuid · enum · PK | ✓ | role = assignee(담당자) · doctor(집도의) · called_doctor(호출된 의사) (cc: procedure.assignee_staff_ids · doctor_staff_ids) | assignees[] · doctors[] · calledDoctors[] |
| `created_at · updated_at · deleted_at` | timestamptz | ✓ |  |  |

## `doctor_call`

| 필드 | 타입 | 필수 | 설명 | 외부(KOS) |
|---|---|---|---|---|
| `id` | uuid PK | ✓ | 시술실에서 의사를 부른 1회 |  |
| `visit_id` | uuid FK → visit | ✓ |  |  |
| `kind` | enum one · all | ✓ | 특정 의사 호출 / 전체 호출 (cc: doctor_call.kind) |  |
| `target_staff_id` | uuid FK → staff |  | 특정 의사 — kind = one 일 때 (cc: doctor_call.target_staff_id) |  |
| `called_by_staff_id` | uuid FK → staff | ✓ | 부른 직원 (cc 에 없던 새 칸) |  |
| `reassigned_from_call_id` | uuid FK → doctor_call |  | 다른 의사로 다시 부른 경우 원래 호출 (cc: doctor_call.reassigned_from_call_id) |  |
| `created_at · updated_at · deleted_at` | timestamptz | ✓ | created_at = 호출 시각 |  |

## `doctor_call_task`

| 필드 | 타입 | 필수 | 설명 | 외부(KOS) |
|---|---|---|---|---|
| `call_id · task_id` | uuid FK · PK | ✓ | 한 번 호출에 작업 여러 개 (cc: doctor_call_item) |  |
| `created_at · updated_at · deleted_at` | timestamptz | ✓ |  |  |

## `doctor_call_accept`

| 필드 | 타입 | 필수 | 설명 | 외부(KOS) |
|---|---|---|---|---|
| `id` | uuid PK | ✓ |  |  |
| `call_id · task_id` | uuid FK | ✓ | 어느 호출의 어느 작업을 (cc: call_accept) |  |
| `doctor_staff_id` | uuid FK → staff | ✓ | 수락한 의사 — 집도의가 된다 (cc: call_accept.doctor_staff_id) |  |
| `accepted_at` | timestamptz | ✓ | (cc: call_accept.accepted_at) |  |
| `created_at · updated_at · deleted_at` | timestamptz | ✓ |  |  |

## `visit_anesthesia`

| 필드 | 타입 | 필수 | 설명 | 외부(KOS) |
|---|---|---|---|---|
| `id` | uuid PK | ✓ |  |  |
| `visit_id` | uuid FK → visit | ✓ | 방문 1 : 마취 N (cc: anesthesia) |  |
| `started_at · ended_at` | timestamptz |  | 마취 시작 · 끝 — 현황판 타이머 (cc: anesthesia) |  |
| `started_by · ended_by` | uuid FK → staff |  | 누른 직원 (cc: start_event_id · end_event_id) |  |
| `created_at · updated_at · deleted_at` | timestamptz | ✓ |  |  |

## `board_card_order`

| 필드 | 타입 | 필수 | 설명 | 외부(KOS) |
|---|---|---|---|---|
| `hospital_id · board_date · visit_id` | uuid · date · uuid · PK | ✓ | 하루 · 병원별 카드 드래그 순서 — cc 의 visit_ids JSON 한 줄 대신 카드마다 한 행 (cc: board_order) |  |
| `position` | int | ✓ | 위에서부터 순서 (cc: board_order.visit_ids) |  |
| `updated_by_staff_id` | uuid FK → staff |  | 마지막으로 옮긴 직원 (cc: board_order.updated_by) |  |
| `created_at · updated_at · deleted_at` | timestamptz | ✓ |  |  |

## `event_log`

| 필드 | 타입 | 필수 | 설명 | 외부(KOS) |
|---|---|---|---|---|
| `id` | uuid PK | ✓ |  |  |
| `hospital_id` | uuid FK | ✓ |  |  |
| `occurred_at` | timestamptz | ✓ | (cc: event_log.at) |  |
| `actor_staff_id` | uuid FK → staff |  | 누가 — 시스템이면 비어 있음 (cc: event_log.actor) |  |
| `type` | varchar | ✓ | 무슨 동작 (예: task.start · call.create · room.assign) (cc: event_log.type) |  |
| `visit_id` | uuid FK → visit |  | (cc: event_log.visit_id) |  |
| `payload` | jsonb |  | 동작 내용 (cc: event_log.payload) |  |
| `created_at` | timestamptz | ✓ | 쌓기만 — 고치거나 지우지 않는다 |  |

## `external_outbox`

| 필드 | 타입 | 필수 | 설명 | 외부(KOS) |
|---|---|---|---|---|
| `id` | uuid PK | ✓ | DAY 에서 고친 것을 KOS 에 보내는 큐 (cc: kos_op) |  |
| `hospital_id · vendor` | uuid · enum | ✓ |  |  |
| `visit_id · seq` | uuid · int | ✓ | 방문별 보낼 순서 (cc: kos_op.visit_id · seq) |  |
| `event_id` | uuid FK → event_log |  | 어느 동작에서 생겼나 (cc: kos_op.event_id) |  |
| `api · path · body` | varchar · varchar · jsonb | ✓ | 보낼 호출 (cc: kos_op) |  |
| `expect` | jsonb | ✓ | 보낸 뒤 조회에서 확인할 값 (cc: kos_op.expect) |  |
| `status` | enum pending · sent · confirmed · failed | ✓ | (cc: kos_op.status) |  |
| `attempts · checks` | int | ✓ | 보낸 횟수 · 확인 실패 횟수(2 면 다시 보냄) (cc: kos_op) |  |
| `last_error` | text |  | (cc: kos_op.last_error) |  |
| `created_at · updated_at` | timestamptz | ✓ |  |  |

## 다른 곳으로

| 필드 | 타입 | 필수 | 설명 | 외부(KOS) |
|---|---|---|---|---|
| 시술권 id (ticketId) | | | KOS 시술권 — 데스크 몫. 1차는 회차 스냅샷만 → 두지 않음 (1차) | ticketConfiguration.ticketId |
| 상품 옵션 · 진료항목 id | | | 메뉴 테이블이 1차에 없음 — 스냅샷 이름만 → 두지 않음 (1차 · 04-1) | optionId · medicalServiceConfiguration.id |
| taskTimers · etceteraWorks | | | 작업 타이머 · 기타 업무 — cc 는 쓰지 않음 → 확인 필요 | taskTimers[] · etceteraWorks[] |
| kos_token · sync_state | | | KOS 토큰 · 동기화 상태 — external_session · external_ref 와 서버 상태로 → cc kos_token · sync_state |  |

## 확인할 것

- KOS `taskTimers`(작업 타이머) · `etceteraWorks`(기타 업무) — cc 는 쓰지 않았다. 시술 현황에 필요한지.
