# 03 예약 / 방문

2026-11-03 사용자와 정하는 중. 공통 규칙은 [README.md](README.md). 검토표: https://claude.ai/artifact/WcNUV73uvfKVN4etSjBjFn

## 정한 것

- **예약과 방문은 `visit` 한 테이블**이다 — KOS 스케줄(고객 한 명의 하루) 1건 = 1행. 취소 · 노쇼면 방문 칸이 비어 있다.
  워크인도 예약을 만들어 쓰고, 내원 현황은 고객을 바로 봐야 해서 나누지 않는다(사용자 2026-11-03). 고객 id 는 이 행 하나에만.
- 비대면 상담은 없다 — 상담에는 늘 방문이 있다(`consultation.visit_id` 필수).
- **`flow_step` 은 KOS 단계 8개 그대로**(`reserved` · `reception` · `consultation_waiting` · `consultation` · `procedure_waiting` ·
  `procedure` · `procedure_done`(귀가 대기) · `completed`(귀가 완료)). cc 의 2계층(큰 단계 + 대기 · 진행 · 완료)은 화면에서 계산한다.
  취소 · 노쇼는 단계가 아니라 `reservation_status`. 현황판 카드의 잘게 나눈 상태(방 배정 · 호출 · 시술 중)는 5번 시술에서.
- `reservation_status` — `reserved` · `canceled` · `no_show` · `received`(접수됨, KOS `IN_PROGRESS`) · `completed`.
- [귀가 대기] 시각 칸(cc `home_requested_at`)은 두지 않는다 — `procedure_done` 으로 바뀐 시각은 `visit_flow_log` 에 남는다.
- 동기화 칸(`synced_at` · 처음 받은 시각 · 외부에 있나)은 `external_ref` 에만. DAY 테이블에는 생성 · 수정 · 삭제 시각만.
- 상담사 · 상담 의사는 한 상담에 한 명.
- 이름: 오더 메모 = `procedure_order_note`, 상담 메모 = `consultation_note`.
- **유입은 고객 · 방문 둘 다 둔다**(사용자 2026-11-03) — 고객 `funnel_id` · `funnel_detail` = 최초 유입, 방문 `funnel_id` ·
  `funnel_detail` · `connected_channel` = 이번 예약이 들어온 곳. KOS 도 둘을 따로 갖는다(고객 `visitorFunnel` · 예약 `reservation.funnel`).

## `visit` — 예약 + 방문

| 묶음 | 필드 | 타입 | 필수 | 설명 | 외부(KOS) |
|---|---|---|---|---|---|
| 식별 | `id` | uuid PK | ✓ | DAY 방문 id. KOS 스케줄 1건 = 1행 — 예약 칸 + 방문 칸. 취소 · 노쇼면 방문 칸이 비어 있다 |  |
|  | `hospital_id` | uuid FK → hospital | ✓ |  |  |
|  | `customer_id` | uuid FK → customer | ✓ | 고객 — 이 행 하나에만 둔다 | visitor.id |
|  | `booked_at` | timestamptz |  | 예약이 처음 만들어진 시각 | createdDateTimeUtc |
|  | `deleted_at` | timestamptz |  | 소프트 딜리트 — 외부에서 지워지면 그 시각을 채운다. 행은 지우지 않는다 | deleted |
| 예약 | `reserved_start_at` | timestamptz | ✓ | 예약 시작 시각 | reservation.startDateTime |
|  | `reserved_end_at` | timestamptz |  | 예약 끝 시각 | reservation.endDateTime |
|  | `reservation_status` | enum reserved · canceled · no_show · received · completed | ✓ | 예약 상태 — 예약됨 · 취소 · 노쇼 · 접수됨 · 완료 (KOS IN_PROGRESS = 접수됨) | reservation.status |
|  | `reservation_group_id` | uuid FK |  | 예약 그룹 (시간표 · 정원 단위) | reservation.reservationGroupId (폐기 예정 표시) |
|  | `reservation_notes` | text |  | 예약 메모 (최대 1,000자) | reservation.reservationMemo |
|  | `reservation_assignee_id` | uuid FK |  | 예약 담당자 (예약을 잡은 직원) | reservation.reservationAssignee.id |
|  | `requested_counselor_id` | uuid FK |  | 희망 상담사 | reservation.counselor.id |
|  | `requested_doctor_id` | uuid FK |  | 희망 의사 | reservation.doctor.id |
|  | `funnel_id` | uuid FK |  | 이 예약의 유입 채널 (고객의 최초 유입과 별개) | reservation.funnel.funnel |
|  | `funnel_detail` | varchar |  | 상세 유입 채널 (자유 입력) | reservation.funnel.funnelDetail |
|  | `connected_channel` | enum gangnamunni · homepage · kos_connect |  | 예약이 들어온 외부 채널 | reservation.connectedChannel |
|  | `consultation_required` | bool | ✓ | 상담 필요 | reservation.consultationRequired |
|  | `sedation_required` | bool | ✓ | 수면(진정) 필요 | reservation.sedationRequired |
|  | `desired_discharge_at` | timestamptz |  | 희망 귀가 시각 | reservation.desiredDischargeDateTimeUtc |
| 내원 | `flow_step` | enum reserved · reception · consultation_waiting · consultation · procedure_waiting · procedure · procedure_done · completed | ✓ | 지금 단계 — KOS flowStep 8개 그대로(procedure_done = 귀가 대기, completed = 귀가 완료) | flowStep |
|  | `flow_step_at` | timestamptz |  | 지금 단계로 바뀐 시각 | flowStepUpdatedDateTimeUtc |
|  | `reception_at` | timestamptz |  | 접수 시각 | receptionDateTimeUtc |
|  | `reception_zone_id` | uuid FK |  | 접수 구역 (층) | zone.id |
|  | `current_zone_id` | uuid FK |  | 고객이 지금 있는 구역 | visitorLocation.zoneId |
|  | `is_new` | bool |  | 신환 여부 — 이 방문 기준 | visitor.isNew |
|  | `procedure_order_note` | text |  | 오더 메모 (최대 2,000자) — 오더지에 인쇄되는 메모 | orderMemo |
|  | `room_id` | uuid FK |  | 지금 배정된 방 — 현황판 카드 위치 (cc visit.room_id · reservation.room_kos_id · room_title) | 방 배정 작업의 room (내부 API) |
|  | `room_assigned_at` | timestamptz |  | 방 배정 시각 — 현황판 정렬 · 「입실」 시각 (cc visit.room_assigned_at) | roomAssignedDateTimeUtc (내부 API) |
| KOS 데스크 몫 | `purchase_ids` | — |  | 수납 연결 — 수납은 KOS 데스크가 한다. cc 는 [수납하기] 링크 · 수납 필요 표시에 썼다 | purchaseIds[] · purchases[] |
|  | `prescription_ids` | — |  | 처방전 연결 — cc 는 [처방전 출력] 링크에 썼다 | prescriptionIds[] |
|  | `reactions` | — |  | 카드에 직원이 단 반응 (반응 종류 + 누른 직원) | reactions[] |
| 동기화 | `created_at · updated_at` | timestamptz | ✓ |  |  |

## `visit_requested_procedure` — 희망 시술 (방문 1 : N)

2026-11-03 사용자 위임으로 결정 — 참고용 기록이라 **참조 + 스냅샷**만 둔다.
- 시술권을 희망한 경우(`kind = ticket`)는 시술권 id 를 두지 않는다 — 시술권은 KOS 데스크 몫이고 1차에 시술권 테이블이 없다.
  화면에는 그때 이름(`option_title`)만 보이면 된다. 시술권 id 가 필요한 곳은 작업(5번)뿐이다.
- 가격 사유(정상가 · 수가 유형가)와 진료항목 구성은 두지 않는다 — 희망 단계에서 쓰지 않는다.

| 필드 | 타입 | 필수 | 설명 | 외부(KOS) |
|---|---|---|---|---|
| `id` | uuid PK | ✓ |  |  |
| `visit_id` | uuid FK → visit | ✓ | 방문 1 : 희망 시술 N |  |
| `kind` | enum product_option · ticket | ✓ | 새로 살 상품 옵션인지, 이미 가진 시술권을 쓰겠다는 건지 | requestedProcedures[].type |
| `product_option_id` | uuid FK |  | 상품 옵션 참조 — kind = product_option 일 때. 메뉴는 소프트 딜리트라 참조가 깨지지 않는다 | optionConfiguration.optionId |
| `product_title` | varchar |  | 스냅샷 — 그때 상품 이름 | optionConfiguration.productTitle |
| `option_title` | varchar | ✓ | 스냅샷 — 그때 옵션 이름 (시술권이면 시술권 이름) | optionConfiguration.optionTitle |
| `option_type` | enum single · group · consultation |  | 스냅샷 — 옵션 종류 (group = 코스) | optionConfiguration.optionType |
| `price_amount · currency` | int · varchar |  | 스냅샷 — 그때 가격 | optionConfiguration.price |
| `sort_order` | int | ✓ | 예약에 적힌 순서 | 배열 순서 |
| `created_at · updated_at · deleted_at` | timestamptz | ✓ |  |  |

## `consultation` — 상담 (방문 1 : N)

| 묶음 | 필드 | 타입 | 필수 | 설명 | 외부(KOS) |
|---|---|---|---|---|---|
| 상담 | `id` | uuid PK | ✓ |  | consultations[].id |
|  | `visit_id` | uuid FK → visit | ✓ | 방문 1 : 상담 N. 비대면 상담은 없다 — 상담에는 늘 방문이 있다 | scheduleId |
|  | `started_at` | timestamptz |  | 상담 시작 시각 | consultationStartedDateTimeUtc |
|  | `counselor_id` | uuid FK |  | 상담사 — 한 상담에 한 명(사용자 2026-11-03) | counselors[] |
|  | `doctor_id` | uuid FK |  | 상담 의사 — 한 상담에 한 명(사용자 2026-11-03) | consultationDoctors[] |
|  | `consultation_note` | text |  | 상담 메모 (최대 5,000자) | content.text |
|  | `procedures` | — |  | 상담에서 정한 시술 | consultationProcedures[] |
|  | `created_at · updated_at` | timestamptz | ✓ | DAY 행 생성 · 수정 시각 | createdDateTimeUtc · updatedDateTimeUtc |
|  | `deleted_at` | timestamptz |  | 소프트 딜리트 |  |

## `visit_flow_log` — 단계 이력 (방문 1 : N)

| 묶음 | 필드 | 타입 | 필수 | 설명 | 외부(KOS) |
|---|---|---|---|---|---|
| 단계 이력 | `id` | uuid PK | ✓ |  |  |
|  | `visit_id` | uuid FK → visit | ✓ | 방문 1 : 이력 N |  |
|  | `flow_step` | enum (visit.flow_step 과 같음) | ✓ | 바뀐 단계 |  |
|  | `changed_at` | timestamptz | ✓ | 바뀐 시각. KOS 는 마지막 단계 시각만 주므로 DAY 가 동기화하며 쌓는다 | flowStepUpdatedDateTimeUtc |
|  | `source` | enum external · day | ✓ | 외부(KOS)에서 바뀐 걸 받았는지, DAY 에서 바꿨는지 |  |
|  | `actor_staff_id` | uuid FK |  | DAY 에서 바꾼 직원 (외부에서 온 건 비어 있음) |  |
|  | `deleted_at` | timestamptz |  | 소프트 딜리트 |  |

## 시술 개념 셋 — KOS 구조를 따른다 (사용자 2026-11-03)

흐름: 예약 때 **희망 시술** → 내원해 상담하며 **상담 시술**을 고르고 → 수납(KOS 데스크)하면 **시술권**이 생기고(1회짜리도) →
오늘 받을 것을 시술권에서 꺼내 **작업**을 만든다 → 작업이 시술 현황 카드다.

```text
visit
 ├─ visit_requested_procedure   희망 시술 (참고)        visit 1 : N      → 상품 옵션 참조 + 이름 · 가격 스냅샷
 ├─ consultation
 │    └─ consultation_procedure 상담 시술 (참고)        상담 1 : N       → 상품 옵션 | 시술권 참조 + 이름 · 가격 스냅샷
 └─ visit_task                  작업 = 시술 현황 (핵심)  visit 1 : N (5번) → 종류별로 하나를 가리킨다:
                                  · 시술권 + 회차 (잔여 시술권 / 오늘 결제한 시술)
                                  · 상품 옵션 (추후 수납 — 수납 필요)
                                  · 기타 작업 종류 (방 배정 · 마취 · 시트팩 …)
                                  + 옵션 · 진료항목 이름 스냅샷
```

- KOS 도 셋을 서로 잇지 않는다 — 각자 메뉴(상품 옵션)나 시술권을 가리킨다. DAY 도 잇지 않는다.
- 시술권(남은 회차 · 금액)과 수납은 KOS 데스크 몫 — 1차는 작업에 **시술권 id 와 회차만** 담고 시술권 · 수납 테이블은 만들지 않는다.
- 작업의 외부 id = KOS `scheduleId` + 작업 `sequence`(KOS 작업은 id 가 없고 이 둘로 가리킨다 — HAR `change-tasks-*`).
- 출처: KOS 데이터 모델 문서 · HAR `수납.har`(`initialize-purchase` → `add-pending-purchase-items` → `add-transaction` →
  `accept-purchase` → `register-purchase`) · `수납필요 추가.har` · `방배정.har`(`add-flow-tasks`) · `get-ticket-bundles`.

## 논의 중 (사용자가 더 생각하기로 함)

1. **예약 그룹(`reservation_group_id`)** — 6번(방 · 구역 · 예약 그룹)에서 정한다. KOS 는 예약 안 `reservationGroupId` 를 폐기 예정으로
   두고 점유 자원(`occupiedResources`, 종류 `RESERVATION_GROUP`)으로 옮기는 중.

보류(예약 현황 때): 수납 연결 · 처방전 연결 · 반응(`reactions`).
