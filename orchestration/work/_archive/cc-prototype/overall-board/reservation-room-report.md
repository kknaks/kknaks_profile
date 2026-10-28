# 접수 · 방 배정 — KOS 에서 실제로 일어나는 순서

- 조사일: 2026-10-26 (KST) · 조사자: cc-prototype researcher (task_dacee03f38c8)
- 앞 판 `reservation-create-report.md`(`C§`)에서 이어진다
- 원천
  - `reference/2026-10-23-cc-overall-board/har/방배정.har` (gitignore · 항목 123개 · 05:09:33.9Z ~ 05:10:05.3Z)
  - KOS 예약 화면 정적 JS(`reservation-client_v0.0.540`, 앞 판에서 받은 것)
  - 공개 스펙 openapi.yaml 1.0.1
  - `workflow-v2.md` 「1. 시작 상태」 · 「KOS 반영 표」 · `_RESUME.md` §2(2026-10-23 · 10-25 「방 배정」 줄)
- 대상 일정: 앞 판 HAR `예약.har` #174 에서 **신규 고객으로 만든 예약**이다. 일정 id 가 같았다(확인, 값은 적지 않음)
- 표기
  - **확인**: HAR 이나 데모 조회로 본 것
  - **JS**: 웹앱 코드에 적힌 것
  - **스펙**: openapi.yaml 에 적힌 것
  - **추정**: 해석
- **KOS 쓰기 0건.** 리포트에 id · 이름 · 토큰 값은 적지 않았다

---

## 0. 요약

- **KOS 의 접수 → 방 배정은 쓰기 5번이다.** 브리프의 「6건」 중 `get-etcetera-tasks` 는 조회다. KOS 화면 세 곳(고객 상세의 예약 · 수납 · 상담 탭, 시술 진행판)을 오간다

  | 순서 | 쓰기 | 본문 | 결과 | 누른 곳(`kos-client-uri`) |
  |---|---|---|---|---|
  | ① | `schedule/v1/commands/recept` | `{scheduleId}` | `RESERVED` → **`RECEPTION`**(추정) · `receptionDateTimeUtc` 기록 · 예약 상태 `RESERVED` → `IN_PROGRESS` | 고객 상세 · **예약** 탭 |
  | ② | `schedule/v1/commands/add-flow-tasks` | `{scheduleId, tasks:[{type:ETCETERA, title:"방 배정", etceteraConfiguration{etceteraTaskId, name, translsMap}, translsMap}]}` | 작업 1개 추가(seq 1 · `NOT_STARTED` · 방 없음) | 고객 상세 · **수납** 탭 |
  | ③ | `schedule/v1/commands/change-flow-step` | `{id, step:"PROCEDURE_WAITING"}` | 단계 → **시술 대기** | 고객 상세 · **상담** 탭 |
  | ④ | `schedule/flow/v1/commands/change-tasks-room` | `{scheduleId, sequences:[1], roomId}` | 「방 배정」 작업에 방이 붙는다. 작업 `NOT_STARTED` → **`READY`** · `roomAssignedDateTimeUtc` · `readyDateTimeUtc` 기록 | **시술 진행판**(`/reservation/procedure`) |
  | ⑤ | `schedule/v1/commands/change-flow-step` | `{id, step:"CONSULTATION_WAITING"}` | 단계 → **상담 대기**(시술 대기에서 거꾸로 갔다) | 고객 상세 · **시술** 탭 |

- **방은 일정에 붙지 않는다. 작업에 붙는다.** KOS 의 「방 배정」 = 기타 작업(ETCETERA) 「방 배정」을 동선에 더하고, 그 작업에 방을 넣는 것이다. 기타 작업 목록(`get-etcetera-tasks`, 데모 10개) 중 첫 번째가 「방 배정」이다. workflow-v2 「1. 시작 상태」 · `_RESUME` 10-25 줄과 같은 구조다
- **공개 짝은 ③ · ⑤(`changeFlowStep`)뿐이다.** ① 접수 · ② 작업 추가 · ④ 방 지정은 공개 API 가 없다
  - ①을 공개 `changeFlowStep(RECEPTION)` 으로 대신할 수 있는지는 미확인이다(접수 시각 · 예약 상태가 같이 바뀌는지 스펙에 없다)
- **스펙과 다른 점**: 공개 스펙은 「시술 대기로 바꿀 때 시술 목록이 없으면 `procedures NotFound`」라고 한다. 그런데 내부 ③은 **시술(PROCEDURE) 작업 없이, 「방 배정」 기타 작업 하나만 있는 상태에서 200** 이었다
- **최종 상태**(지금 데모 조회): 단계 `CONSULTATION_WAITING` · 예약 상태 `IN_PROGRESS` · 접수 시각 있음 · 작업 1개(「방 배정」 · `READY` · 방 「A-룸9」 모양 · 배정 시각 있음). 공개 `getScheduleDetail` 과 내부 `get-schedules-grouped-by-zone` 이 같은 상태를 보였다
- 시안의 [접수 완료] 한 번 = KOS 의 ① + ② + ④(+ 단계 바꾸기)다. 순서와 중간 상태는 §5
- 정할 것은 **10개**다(Q-63 ~ Q-72)

---

## 1. HAR 인벤토리

항목 123개 = KOS API 54 + KOS OPTIONS 18 + KOS 정적(js 21 · css 1) + Datadog 23 + Amplitude 6(OPTIONS 1 포함).

KOS API 54건은 모두 POST · `api.kos-solution.com/tenants/{tenantId}/…` 이고 `Authorization` 은 HAR 에 없다. 아래 표는 **순서대로 54건 전부**다(같은 묶음은 한 칸에 #로 모았다). 「누른 곳」은 요청의 `kos-client-uri` 와 시각 간격을 보고 짐작한 것이다.

| 단계 | 시각(Z) | # | 경로 | 본문 키 | 응답 모양 (건수) | 누른 곳 · 용도 |
|---|---|---|---|---|---|---|
| P0 | 09:33.9 | 0 | `role/v2/queries/get-roles` | — | (15) | 고객 상세(예약 탭) 열림 |
| | | 1 | `schedule/group/v1/queries/get-reservation-group` | `id` | `data{그룹}` | 예약의 그룹 |
| | | 2 | `procedure-menu/visitors/queries/get-visitors` | `sort` | (0) | 고객 유형 |
| | | 4 | `schedule/v1/queries/get-schedule-summaries` | `visitorId · sort` | `data[1]` — **`RESERVED` · 예약 상태 `RESERVED` · `tasks[]` 0개** | **접수 전 상태** |
| **W1** | 09:34.0 | **6** | **`schedule/v1/commands/recept`** | `scheduleId` | `{}` | **[접수]** — 예약 탭 |
| P1 | 09:34.4 ~ 34.9 | 8 | `meta/codes/v1/queries/get-codes` | `category:CONSULTATION_RESULT` | (8) | 접수 뒤 화면이 상담 결과 코드를 받는다 |
| | | 10 | `account/v2/queries/get-accounts-last-update-date-time-utc` | — | 문자열 | |
| | | 21 · 29 · 30 | `get-reservation-group` | `id` | `data{그룹}` | |
| | | 22 | `purchase/tax-refund-settings/v1/queries/get-tax-refund-settings` | `{}` | **400** `id NotFound` | 세금 환급 설정(데모에 없음) |
| | | 24 | `procedure-menu/vat-settings/queries/get-vat-settings` | — | `data{includeVATInPrice, vatRate}` | 부가세 |
| P2 | 09:37.3 | 35 | `v1/visitor/queries/get-visitor` | `id` | `data{고객}` | **수납 탭** 열기 |
| | | 36 | `purchase/payment-settings/v1/queries/get-payment-settings` | — | `data{결제 수단 설정 …}` | 결제 설정 |
| P3 | 09:39.9 ~ 41.5 | 39 | `ticket/v1/queries/get-ticket-bundles` | `visitorId · sort` | `{}` | 보유 시술권(없음) |
| | | 43 | `procedure-menu/product-options/v2/queries/search-product-option-summaries` | `searchText(빈칸) · size:25 · deleted · optionTypes[SINGLE, GROUP] · baseDateTimeUtc · closed` | `data[25]{id, title, type, price{amount, suppliedAmount, taxFreeAmount, vatAmount, taxation}, productConfiguration, medicalService{…}}` + `nextCursor` | 수납 탭에서 상품 옵션을 고르는 창 |
| | | 52 | `procedure-menu/target-countries/v1/queries/get-target-countries` | `sort` | (4) | |
| | | 54 | `procedure-menu/visitors/queries/get-visitors` | `sort` | (0) | |
| P4 | 09:42.5 | 58 | `schedule/etcetera-tasks/v1/queries/get-etcetera-tasks` | `{}` | `data[{id, title, deleted, translsMap}]` (10) | **기타 작업 고르기 창**. 데모 목록: 방 배정 · 마취시간 · 드레싱 · 수면 가능 여부 조회 · 모델링팩 (10분) · 채혈 30cc · 수면 경과 확인 · 채혈 120cc · 원장 상담 · 수면 후 회복 |
| **W2** | 09:44.4 | **60** | **`schedule/v1/commands/add-flow-tasks`** | §2.2 | `{}` | **「방 배정」 작업 추가** — 수납 탭 |
| P5 | 09:44.6 ~ 44.9 | 65 · 68 | `get-reservation-group` | `id` | | 갱신 |
| | | 66 | `get-accounts-last-update…` | — | | |
| **W3** | 09:48.0 | **72** | **`schedule/v1/commands/change-flow-step`** | `id · step:PROCEDURE_WAITING` | `{}` | **단계 → 시술 대기** — 상담 탭 |
| P6 | 09:48.1 ~ 48.3 | 74 · 77 | `get-reservation-group` | `id` | | 갱신 |
| | | 75 | `get-accounts-last-update…` | — | | |
| P7 | 09:50.7 ~ 51.1 | 80 | `get-accounts-last-update…` | — | | **시술 진행판**으로 이동 |
| | | 81 | `schedule/zone/room/v1/queries/get-rooms` | `zoneId` | (28) | 방 목록 |
| | | 83 | `schedule/v2/queries/get-schedules-grouped-by-zone` | `zoneIds[2] · startDateTimeUtc · endDateTimeUtc` | `data[{zoneId, schedules[일정]}]` (구역 1 · 일정 4) | 진행판 데이터(시술 현황이 쓰는 그 작업, workflow-v2 D-08). **이 일정: `PROCEDURE_WAITING` · 접수 시각 있음 · 작업 「방 배정」 `NOT_STARTED` · 방 없음** |
| | | 86 | `meta/notice/v1/queries/get-notices` | 날짜 범위 · `deleted` | (0) | 공지 |
| P8 | 09:56.5 | 90 | `get-accounts-last-update…` | — | | 방 고르기 창 |
| | | 91 | `get-rooms` | `zoneId` | (28) | |
| **W4** | 10:00.1 | **93** | **`schedule/flow/v1/commands/change-tasks-room`** | `scheduleId · sequences:[1] · roomId` | `{}` | **방 지정** — 진행판 |
| P9 | 10:02.3 ~ 02.7 | 96 | `visitor/v2/queries/get-visitor` | `id` | | 고객 상세 다시 열기 |
| | | 97 | `schedule/v1/queries/get-payment-required-tasks` | `visitorId` | (0) | 수납 필요 작업 없음(「방 배정」은 `paymentRequired:false`) |
| | | 98 | `schedule/v1/queries/get-schedule-detail` | `scheduleId` | `data{일정}` — **`PROCEDURE_WAITING` · `IN_PROGRESS` · 작업 「방 배정」 `READY` · 방 있음 · `roomAssignedDateTimeUtc`** | **방 배정 뒤 상태** |
| | | 99 | `get-accounts-last-update…` | — | | |
| | | 100 | `get-reservation-group` | `id` | | |
| | | 101 · 108 | `get-codes` | `FUNNEL_CATEGORY` | (0) | |
| | | 102 · 107 | `get-codes` | `FUNNEL` | (13) | |
| | | 104 | `get-codes` | `CONSULTATION_RESULT` | (8) | |
| | | 103 | `procedure-menu/visitors/queries/get-visitors` | `sort` | (0) | |
| | | 105 | `consultation/v1/queries/get-consultations-by-visitor-id` | `visitorId` | (0) | |
| | | 106 | `visitor/questionnaire/v1/queries/get-questionnaire-submit/legacy` | `visitorId` | 400 `NotFound` | |
| | | 109 · 110 | 선불카드 요약 · 잔액 | `visitorId` | (0) / `data{…}` | |
| | | 111 | `get-schedule-summaries` | `visitorId · sort` | `data[1]` — `PROCEDURE_WAITING` · 작업 1 | |
| | | 112 | `get-ticket-bundles` | `visitorId · sort` | `{}` | |
| **W5** | 10:05.0 | **118** | **`schedule/v1/commands/change-flow-step`** | `id · step:CONSULTATION_WAITING` | `{}` | **단계 → 상담 대기** — 시술 탭 |
| P10 | 10:05.3 | 119 | `get-accounts-last-update…` | — | | 갱신 |
| | | 120 | `get-reservation-group` | `id` | | |

**합계**: P0 4 + W1 1 + P1 7 + P2 2 + P3 4 + P4 1 + W2 1 + P5 3 + W3 1 + P6 3 + P7 4 + P8 2 + W4 1 + P9 17 + W5 1 + P10 2 = **54** 로, HAR 의 KOS API 54건과 같다. 쓰기는 5건이다.

---

## 2. 쓰기 5건 해부 (순서대로)

### 2.1 ① `recept` — `POST …/schedule/v1/commands/recept`

- 본문: **`{scheduleId}` 하나**(JS `recept(e){… {scheduleId:e} …}` 와 같다) → `{}`
- 바뀐 것(#4 접수 전 ↔ #83 · #98 뒤)

  | 필드 | 전 | 뒤 | 메모 |
  |---|---|---|---|
  | `receptionDateTimeUtc` | (요약 응답에 없음) | **recept 를 부른 시각**(같은 초) | 확인 |
  | `reservation.status` | `RESERVED` | **`IN_PROGRESS`** | 확인 |
  | `flowStep` | `RESERVED` | 다음에 읽었을 때는 이미 ③ 뒤라 `PROCEDURE_WAITING` 이었다 | `RECEPTION` 이 되었다고 보인다(추정). recept 직후 상태는 HAR 에 없다 |
  | `zone` · `visitorLocation.zoneId` | 예약의 구역 | 그대로(「4층」) | 접수 구역은 본문에 없다. 예약 때 정한 `zoneId` 를 쓴다 |
  | 접수 직원 | — | **일정 응답에 접수한 직원 필드가 없다** | R§3.1 21행과 같다 |

- 짝을 이루는 내부 작업: `schedule/v1/commands/cancel-reception{scheduleId}`(접수 취소, JS)
- **공개 짝**: 전용 작업은 없다. 공개 `changeFlowStep{scheduleId, step:RECEPTION}` 이 가장 가깝다. 이것이 `receptionDateTimeUtc` · 예약 상태까지 바꾸는지는 스펙에 없다 → Q-63

### 2.2 ② `add-flow-tasks` — `POST …/schedule/v1/commands/add-flow-tasks`

```text
{ scheduleId,
  tasks: [ { type: "ETCETERA",
             title: "방 배정",
             etceteraConfiguration: { etceteraTaskId,  ← get-etcetera-tasks 목록의 「방 배정」 id(확인)
                                      name: "방 배정", translsMap{name{}} },
             translsMap: { title{} } } ] }      → {}
```

- 결과(#83): 작업 `type ETCETERA · sequence 1 · title 「방 배정」 · status NOT_STARTED · room 없음 · paymentRequired false`
- **시술(PROCEDURE) 작업 · 상품 옵션은 이번에 더하지 않았다.** 사용자는 수납 탭에서 상품 옵션 창(#43)을 열었지만, 고른 것은 기타 작업 「방 배정」 하나였다. JS 상 같은 묶음에 `add-etcetera-works` · `cancel-flow-tasks` · `revoke-cancel-procedure-tasks` 도 있다. 시술 작업을 더할 때도 `add-flow-tasks` 를 쓰는지는 이번 HAR 로는 모른다 → Q-66
- 화면: 고객 상세 **수납** 탭(`tab=purchase`)에서 보냈다. KOS 는 수납 탭에서 동선(작업)을 꾸린다(추정)
- **공개 짝: 없음**(R§ · KDA§5 「시술 작업 추가 — 스펙에 없음」과 같다)

### 2.3 ③ `change-flow-step` → `PROCEDURE_WAITING` — `POST …/schedule/v1/commands/change-flow-step`

- 본문 `{id, step}`. 키 이름이 `scheduleId` 가 아니라 **`id`** 다(JS `{step:t, id:e}`) → `{}`
- 결과: `flowStep PROCEDURE_WAITING` · `flowStepUpdatedDateTimeUtc` = 이 시각(확인 #98)
- 화면: 고객 상세 **상담** 탭
- **공개 짝**: `changeFlowStep{scheduleId, step}`(키 이름이 다르다)
  - 스펙의 400 예시에 「시술 대기 · 진행 단계로 바꿀 때 시술 목록이 없으면 `procedures NotFound`」가 있다
  - 이번 내부 호출은 **PROCEDURE 작업이 0개(ETCETERA 1개만)인데 200** 이었다 → 내부와 공개의 검사가 다르거나, ETCETERA 도 「시술 목록」으로 친다(미확인) → Q-67

### 2.4 ④ `change-tasks-room` — `POST …/schedule/flow/v1/commands/change-tasks-room`

- 본문 `{scheduleId, sequences:[1], roomId}` → `{}`
  - `sequences` = 「방 배정」 작업의 sequence
  - `roomId` = `get-rooms`(#81 · #91) 목록 중 하나
- 결과(#98)

  | 작업 필드 | 전(#83) | 뒤(#98) |
  |---|---|---|
  | `status` | `NOT_STARTED` | **`READY`** |
  | `room{id, zoneId, title, order}` | 없음 | 「A-룸9」 모양 |
  | `roomAssignedDateTimeUtc` | 없음 | 호출 시각 |
  | `readyDateTimeUtc` | 없음 | 같은 시각 |
  | `assignees` | 0 | 0 |

- 화면: **시술 진행판**(`/reservation/procedure`)에서 보냈다. 고객 상세가 아니다
- workflow-v2 「KOS 반영 표」의 `change-tasks-room {scheduleId, sequences[], roomId}`(의사 호출 전 방 넣기)와 같은 작업 · 같은 본문이다
- **공개 짝: 없음**(KDA§5 「방 배정 · 이동 — 스펙에 없음」)

### 2.5 ⑤ `change-flow-step` → `CONSULTATION_WAITING`

- 본문 `{id, step:"CONSULTATION_WAITING"}` → `{}`. 화면: 고객 상세 **시술** 탭
- 결과(지금 조회): `flowStep CONSULTATION_WAITING` · 「방 배정」 작업과 방은 그대로 남았다
- **시술 대기 → 상담 대기, 즉 거꾸로 가는 변경도 받는다**(확인). 상담 대기는 공개 스펙 400 예시(상담 진행 · 시술 대기 · 귀가)에 걸리지 않는 단계다
- 사용자가 왜 마지막에 상담 대기로 돌렸는지는 HAR 로 알 수 없다(「상담 필요」 고객의 실제 순서일 수도 있다 — 추정) → Q-68
- **공개 짝**: `changeFlowStep`

---

## 3. 단계마다의 상태

| 시점 | 근거 | `flowStep` | 예약 상태 | 접수 시각 | 작업 |
|---|---|---|---|---|---|
| 접수 전 | #4 | `RESERVED` | `RESERVED` | (없음) | 0개 |
| ① 접수 뒤 | (HAR 에 조회 없음) | `RECEPTION` (추정) | `IN_PROGRESS` (추정) | 기록 | 0개 |
| ② 작업 추가 뒤 | (조회 없음) | | | | 「방 배정」 `NOT_STARTED` |
| ③ 시술 대기 뒤 | #83 | `PROCEDURE_WAITING` | `IN_PROGRESS` | 있음 | 「방 배정」 `NOT_STARTED` · 방 없음 |
| ④ 방 지정 뒤 | #98 · #111 | `PROCEDURE_WAITING` | `IN_PROGRESS` | 있음 | 「방 배정」 **`READY` · 방 · 배정 시각** |
| ⑤ 상담 대기 뒤 · **지금** | 공개 `getScheduleDetail` · 공개 `getSchedulesByFlowStep(CONSULTATION_WAITING)` · 내부 `get-schedules-grouped-by-zone`(데모 조회) | `CONSULTATION_WAITING` | `IN_PROGRESS` | 있음 | 「방 배정」 `READY` · 방 · 배정 시각 |

- **시술 현황 판정과의 관계**(workflow-v2 「카드가 생기는 때」 · `_RESUME` 10-25)
  - 지금 이 고객은 방이 있지만 단계가 `CONSULTATION_WAITING` 이다
  - 시술 현황 카드는 `PROCEDURE_WAITING` 부터 생기므로 **지금 카드에 나오지 않는다**(추정, workflow-v2 기준)
  - ④ 직후(시술 대기 + 방)에는 카드 조건에 맞았다
  - 「방 배정」 작업 = 방 붙은 ETCETERA 이면서 ccc 가 호출한 적 없는 작업 → 화면에서 숨기는 줄(10-25)과 같은 모양이다

---

## 4. 공개 짝 정리

| KOS 쓰기 | 내부 경로 | 공개 |
|---|---|---|
| ① 접수 | `schedule/v1/commands/recept{scheduleId}` | **공개 없음**(전용). 비슷한 것: `changeFlowStep(RECEPTION)` — 접수 시각 · 예약 상태가 바뀌는지 미확인 |
| ② 작업(「방 배정」) 추가 | `schedule/v1/commands/add-flow-tasks{scheduleId, tasks[]}` | **공개 없음** |
| ③ 단계 → 시술 대기 | `schedule/v1/commands/change-flow-step{id, step}` | `changeFlowStep{scheduleId, step}` |
| ④ 작업에 방 지정 | `schedule/flow/v1/commands/change-tasks-room{scheduleId, sequences[], roomId}` | **공개 없음**. 방 목록 조회도 공개에는 없다(R§2) |
| ⑤ 단계 → 상담 대기 | `change-flow-step` | `changeFlowStep` |
| (참고) 접수 취소 | `schedule/v1/commands/cancel-reception{scheduleId}`(JS) | 공개 없음 |
| (참고) 작업 취소 | `schedule/v1/commands/cancel-flow-tasks`(workflow-v2 · JS) | 공개 없음 |

---

## 5. 시안과 비교 — 「시술실 선택 → [접수 완료]」 한 번

시안(D§3.4 바닥 줄)
- [시술실 선택](A-룸1~10) → 「방 선택 + 신분 필드 모두 입력」이면 [접수 완료]가 켜진다
- 누르면 상태 「접수」 + 방 배정 + 흐름 시작 시각
- 내원 현황 첫 줄에 「접수 완료 · {방} 배정 · 데스크 {직원}」이 뜬다

KOS 는 **쓰기 3~4번 + 조회 1~2번**이고, 화면 세 곳에 나뉘어 있다. [접수 완료] 한 번으로 KOS 와 같은 결과를 내려면 KOS 순서는 이렇다(HAR 에서 본 순서 그대로 · 결정 아님)

| 순서 | 호출 | 미리 필요한 것 | 실패하면 남는 것(추정) |
|---|---|---|---|
| 0 | (조회) `get-etcetera-tasks` → 「방 배정」 기타 작업 id · (조회) `get-rooms` → 방 id | 지점마다 「방 배정」 기타 작업이 등록되어 있어야 한다(데모: 목록 10개 중 하나) | — |
| 1 | `recept{scheduleId}` | 일정이 `RESERVED` | — |
| 2 | `add-flow-tasks{scheduleId, tasks:[ETCETERA 「방 배정」]}` | 1 성공 | 실패하면 **접수만 된 상태**(접수 시각 · `IN_PROGRESS`, 작업 0개)가 남는다. 되돌리려면 `cancel-reception` |
| 3 | `change-tasks-room{scheduleId, sequences:[새 작업의 sequence], roomId}` | **새 작업의 sequence 를 알아야 한다** — `add-flow-tasks` 응답이 `{}` 라서 일정을 다시 조회해야 한다(HAR 에서도 #83 을 읽은 뒤 방을 넣었다) | 실패하면 **방 없는 「방 배정」 작업**이 남는다(`NOT_STARTED`). 되돌리려면 `cancel-flow-tasks` |
| (4) | `change-flow-step{id, step}` | 어느 단계로 보낼지(HAR 에서는 시술 대기 → 상담 대기) | 실패하면 단계만 앞 상태로 남는다 |

- HAR 의 실제 순서는 「단계 변경(③)이 방 지정(④)보다 앞」이었다. 방 지정이 단계에 따라 막히는지는 모른다 → Q-64
- KOS 에는 「방 선택 + 신분 필드 모두 입력」 같은 접수 조건이 없다. `recept` 본문은 일정 id 하나다. 신분 확인 조건은 ccc 쪽 규칙이다
- 「데스크 {직원}」: KOS 접수에는 직원 필드가 없다. 기록은 시스템 계정 이름으로 남는다(U Q-49) → Q-69
- 시안 방 목록 「A구역 A-룸1~10」 ↔ KOS `get-rooms` 28개(A-룸1~9 · A-레이저실 · A-트윈 · A-시술실 · A-회복실 · B-룸 · B-트윈). R Q-16 · 디자인 Q-19 와 같다 → Q-70
- 시안의 [시술실 선택] 팝오버 「사용 중」 표시: KOS 에는 방 사용 여부 필드가 없다. 진행판(`get-schedules-grouped-by-zone`)의 작업 `room` 을 모아야 한다(R Q-16)

---

## 6. 정할 것 (결정하지 않음) — 10개

| # | 자리 | 왜 정해야 하나 | 앞 판 |
|---|---|---|---|
| Q-63 | 접수를 내부 `recept` 로 할지 공개 `changeFlowStep(RECEPTION)` 으로 할지 | `recept` 는 공개가 아니다. 공개 단계 변경이 접수 시각 · 예약 상태(`IN_PROGRESS`)까지 바꾸는지 모른다. 데모에서 한 번 시험할지(쓰기 허가 필요) | — |
| Q-64 | [접수 완료] 한 번에 보낼 호출과 순서 | KOS 는 접수 → 작업 추가 → (다시 조회) → 방 지정 → 단계 변경. HAR 은 단계 변경이 방 지정보다 앞이었다. 순서가 바뀌어도 되는지 모른다 | — |
| Q-65 | 중간에 실패했을 때 | 접수만 된 상태 · 방 없는 「방 배정」 작업이 남을 수 있다. 되돌리기(`cancel-reception` · `cancel-flow-tasks`)를 할지, 남겨 두고 재시도할지 | — |
| Q-66 | 시술 작업 · 상품 옵션도 접수 때 넣을지 | KOS 는 수납 탭에서 동선을 꾸린다. 이번 HAR 은 「방 배정」 하나만 더했다. 시술 작업을 넣는 경로(`add-flow-tasks` 의 PROCEDURE?)는 미확인 | — |
| Q-67 | 시술 대기로 바꿀 때 시술 목록 검사 | 공개 스펙은 시술 목록이 없으면 거절한다고 하고, 내부는 ETCETERA 하나로도 받았다. 공개로 바꿀 때 막힐 수 있다 | — |
| Q-68 | 접수 · 방 배정 뒤 어느 단계로 둘지 | HAR 은 시술 대기 → 상담 대기로 끝났다. 시안의 「진행 경로 · 상담 필요 / 바로 시술」(D§3.4)이 KOS 의 상담 대기 / 시술 대기와 맞는지. 시술 현황 카드는 시술 대기부터 생긴다 | R Q-1 |
| Q-69 | 「데스크 {직원}」 | KOS 접수에 직원 필드가 없다. ccc 에만 남길지 | U Q-49 |
| Q-70 | 방 목록 · 범위 | 시안 A-룸1~10 ↔ KOS 28개. 어느 방을 고르게 할지 · 「사용 중」을 무엇으로 볼지 | R Q-16 |
| Q-71 | 「방 배정」 기타 작업이 없는 지점 | KOS 방 배정은 지점에 「방 배정」 기타 작업이 등록되어 있어야 한다. 이름으로 찾을지 · id 를 설정으로 둘지 | — |
| Q-72 | 방을 「방 배정」 작업에 넣을지, 첫 시술 작업에 넣을지 | `change-tasks-room` 은 어느 작업이든 받는다(시술 현황은 호출 전에 시술 작업에 방을 넣는다). 시술 현황의 「방 배정」 판정(방 붙은 ETCETERA · ccc 호출 없음)과 맞아야 한다 | `_RESUME` 10-25 |

---

## 7. 호출 기록 · 빠진 행 점검

**호출**(2026-10-26, 데모 테넌트, 조회만)
- 공개(데모 키): `exchange-token` 1 + `getScheduleDetail` 1 · `getSchedulesByFlowStep` 1 — 모두 200
- 내부(시스템 계정 Bearer): sign-in 1 + `get-schedules-grouped-by-zone` 1(HAR #83 본문) · `get-etcetera-tasks` 1 — 모두 200
- **쓰기 0건**, 운영 키 0건

**빠진 행**
- HAR: 항목 123 = KOS API 54 + OPTIONS 18 + 정적 22 + Datadog 23 + Amplitude 6. 인벤토리의 # 를 모두 합치면 54(§1 합계)
- 쓰기: 브리프 목록의 #6 · #60 · #72 · #93 · #118 = 5건. #58 `get-etcetera-tasks` 는 조회라 §1 에 넣었다
- 할 일 1~6: §1 · §2 · §3 · §4 · §5 · §6
- 정할 것 10개(Q-63 ~ Q-72)
