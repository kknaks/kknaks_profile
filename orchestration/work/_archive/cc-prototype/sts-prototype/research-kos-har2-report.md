# KOS 웹앱 내부 API — HAR 2차 분석 (DEMO, 2026-10-13)

- 조사자: cc-prototype `researcher` 워커. **HAR 파일 읽기만 했다.** 다시 보낸 요청 0, 복사 · 가공 저장 0, KOS API 호출 0. 1차 리포트 `research-kos-har-report.md` 는 고치지 않았다
- 입력: `/Users/kknaks/Downloads/app.kos-solution.com2.har` — Chrome DevTools 저장, 항목 122개, 녹화 시각 2026-10-13 15:27:46 ~ 15:29:29 KST(약 1분 43초)
- 대상: DEMO 테넌트 `<tenantId>` · 일정 `abf727cb-8c71-483e-9bad-2ce96fac47be`(시술 작업 4개, 결제 없음) + 마지막 요청 1개는 1차 일정 `dd60eae7-…`
- 공개 스펙 대조 기준: 1차와 같은 `https://developers.kos-solution.com/openapi.yaml`(작업 75개, 2026-10-13)
- 표기: **사실** = HAR · 스펙에 있는 것, **추정** = 해석. 시각은 KST

---

## 1차 + 2차 합친 동작 ↔ 내부 API 대응표

모든 내부 API 는 `POST https://api.kos-solution.com/tenants/{tenantId}/…` 이고, 응답 본문은 모두 `{}` 이다(쓰기 20건 전부).

| 화면 동작 | 내부 경로(`/tenants/{tenantId}/` 뒤) | 요청 본문 | 작업을 가리키는 값 | 공개 OpenAPI | 근거 |
|---|---|---|---|---|---|
| 단계 변경(접수 · 상담 대기 · 상담 · 시술 대기 · 시술 · 귀가 대기 · 귀가) | `schedule/v1/commands/change-flow-step` | `{id, step}` | 일정 `id` | **있음** `changeFlowStep`(필드 `scheduleId` · `step`) | 1차 3 · 2차 6 |
| **상담사 지정**(상담 기록 생성) | `consultation/v1/commands/create-consultation` | `{consultationId, visitorId, consultationStartedDateTimeUtc, scheduleId, content:{text}, counselorIds[]}` | 상담 id 를 **웹앱이 만들어 보냄** | **없음** | 2차 |
| 상담 의사 지정 | `consultation/v1/commands/change-consultation-doctors` | `{consultationId, doctorIds[]}` | 상담 id | **없음** | 2차 |
| **담당자** | `schedule/flow/v1/commands/change-tasks-assignees` | `{scheduleId, sequences[], assigneeIds[]}` | 일정 id + 작업 **`sequence` 배열** | **없음** | 2차 3 |
| **집도의** | `schedule/flow/v1/commands/change-tasks-doctors` | `{scheduleId, sequences[], doctorIds[]}` | 일정 id + `sequence` 배열 | **없음** | 2차 1 |
| **시술 완료하기** | `schedule/flow/v1/commands/change-tasks-complete` | `{scheduleId, sequences[], complete:true}` | 일정 id + `sequence` 배열 | **없음** | 2차 3 |
| 미완료 시술 취소(귀가 대기 전 일괄 취소) | `schedule/v1/commands/cancel-flow-tasks` | `{scheduleId, sequences[], reason:"CANCEL"}` | 일정 id + `sequence` 배열 | **없음** | 1차 1([1,2,3,4]) · 2차 1([4]) |
| 단건 시술 취소하기 | — | — | — | — | **HAR 에 없음**. 같은 `cancel-flow-tasks` 에 순번 1개를 보낼 것으로 추정(2차의 `[4]` 는 바로 뒤 107ms 에 `PROCEDURE_DONE` 이 이어져 일괄 취소 흐름으로 봄) |
| 방 | — | — | — | — | **HAR 에 없음** |
| 우선순위 | — | — | — | — | **HAR 에 없음** |
| 시술 추가 | — | — | — | — | **HAR 에 없음** |

**작업을 무엇으로 가리키나(사실):** 작업 쓰기 4종 모두 **`scheduleId` + `sequences`(작업 `tasks[].sequence` 정수 배열)** 이다. task id · `ticketId` 는 쓰지 않는다. 여러 작업을 한 요청으로 바꿀 수 있는 꼴이다.

**시술 완료하기 → 시술권 차감(사실 + 한계):** `change-tasks-complete` 뒤 그 작업의 `status` 가 `NOT_STARTED` → **`DONE`**, `completedDateTimeUtc` 가 채워졌다(완료 요청 뒤 약 0.1초). 다만 이 DEMO 일정의 작업 4개는 **시술권이 없는 작업**이었다(`procedureConfiguration.ticketConfiguration` = `{}`, `paymentRequired` = true, 일정 `purchaseIds` 0개, `get-ticket-bundles` 응답 비어 있음 — 완료 전후 모두). 그래서 **완료가 시술권을 차감하는지는 이 HAR 로 확인할 수 없다.**

---

## 1. 요청 목록 요약

122개 = KOS API **72** · 분석/로그 50(`browser-intake-datadoghq.com` 34 · `api2.amplitude.com` 16, 목록에서 빼고 내용 안 봄). 정적 파일 0. KOS 72개 모두 `POST`, 응답 200 이 70 · 400 이 2(`visitor/questionnaire/v1/queries/get-questionnaire-submit/legacy` — `visitorId NotFound`, 초진 설문 없음).

KOS 72 = **쓰기 16**(`/commands/`) + 조회 56.

쓰기 시각순:

| # | KST | 경로 | 요약 |
|---|---|---|---|
| 6 | 15:27:52.252 | `schedule/v1/commands/change-flow-step` | → `CONSULTATION_WAITING` |
| 9 | 15:27:54.430 | `consultation/v1/commands/create-consultation` | 상담사 1명 지정, 메모 빈 값 |
| 11 | 15:27:56.713 | `consultation/v1/commands/change-consultation-doctors` | 상담 의사 1명 |
| 12 | 15:27:57.398 | `schedule/v1/commands/change-flow-step` | → `CONSULTATION` |
| 15 | 15:28:02.756 | `schedule/v1/commands/change-flow-step` | → `PROCEDURE_WAITING` |
| 21 | 15:28:09.671 | `schedule/v1/commands/change-flow-step` | → `PROCEDURE` |
| 63 | 15:28:28.282 | `schedule/flow/v1/commands/change-tasks-assignees` | 순번 [1] 담당자 1명(⚠ 이 요청만 화면이 `reservation/schedule/?…&tab=purchase` — 고객 상세의 수납 탭) |
| 77 | 15:28:53.793 | `schedule/flow/v1/commands/change-tasks-doctors` | 순번 [1] 집도의 1명 |
| 80 | 15:28:59.079 | `schedule/flow/v1/commands/change-tasks-complete` | 순번 [1] 완료 |
| 84 | 15:29:05.164 | `schedule/flow/v1/commands/change-tasks-assignees` | 순번 [1,2] 담당자 |
| 86 | 15:29:05.917 | `schedule/flow/v1/commands/change-tasks-complete` | 순번 [2] 완료 |
| 89 | 15:29:09.092 | `schedule/flow/v1/commands/change-tasks-assignees` | 순번 [1,2,3] 담당자 |
| 90 | 15:29:09.939 | `schedule/flow/v1/commands/change-tasks-complete` | 순번 [3] 완료 |
| 93 | 15:29:13.964 | `schedule/v1/commands/cancel-flow-tasks` | 순번 [4] 취소 |
| 94 | 15:29:14.071 | `schedule/v1/commands/change-flow-step` | → `PROCEDURE_DONE` |
| 121 | 15:29:29.147 | `schedule/v1/commands/change-flow-step` | 1차 일정 `dd60eae7-…` → `COMPLETED` |

- 담당자 요청은 순번이 **누적**됐다([1] → [1,2] → [1,2,3], 같은 담당자). 웹앱이 담당자 창에서 이미 담당자가 있는 작업도 함께 보낸 것으로 보인다(추정). 서버는 같은 값으로 덮어써 결과에 문제가 없다(완료 뒤 상세: 1~3 모두 같은 담당자)
- 1차 일정은 작업을 모두 취소한 상태였고 `COMPLETED` 가 200 으로 통과했다. 공개 문서의 「완료되지 않은 시술이 남아 있으면 거절」과 어긋나지 않는다(취소된 작업은 남은 것으로 치지 않음 — 추정)

---

## 2. 쓰기 요청 상세(동작별)

HAR 2차 쓰기 요청 **16개**를 동작별로 묶었다(행마다 요청 수를 괄호에 적음).

| 동작 | 요청 # | 경로 | 본문 필드 · 값 모양 | 응답 |
|---|---|---|---|---|
| 단계 변경 | 6 · 12 · 15 · 21 · 94 · 121 (6) | `schedule/v1/commands/change-flow-step` | `id`: 일정 UUID · `step`: `CONSULTATION_WAITING` / `CONSULTATION` / `PROCEDURE_WAITING` / `PROCEDURE` / `PROCEDURE_DONE` / `COMPLETED` | 200 `{}` |
| 상담사 지정 = 상담 기록 생성 | 9 (1) | `consultation/v1/commands/create-consultation` | `consultationId`: UUID(웹앱이 만든 값 `f79b686b-…`) · `visitorId`: 24자 hex · `consultationStartedDateTimeUtc`: 요청 순간의 브라우저 시각(`2026-10-13T06:27:54.429Z`, 요청 시각과 1ms 차) · `scheduleId`: UUID · `content.text`: `""` · `counselorIds`: 24자 hex 배열 1개(DEMO 직원 남준서) | 200 `{}` |
| 상담 의사 지정 | 11 (1) | `consultation/v1/commands/change-consultation-doctors` | `consultationId`: 위와 같은 UUID · `doctorIds`: hex 배열 1개(권태윤) | 200 `{}` |
| 담당자 | 63 · 84 · 89 (3) | `schedule/flow/v1/commands/change-tasks-assignees` | `scheduleId` · `sequences`: `[1]` / `[1,2]` / `[1,2,3]` · `assigneeIds`: hex 배열 1개(방온유) | 200 `{}` |
| 집도의 | 77 (1) | `schedule/flow/v1/commands/change-tasks-doctors` | `scheduleId` · `sequences`: `[1]` · `doctorIds`: hex 배열 1개(권태윤) | 200 `{}` |
| 시술 완료하기 | 80 · 86 · 90 (3) | `schedule/flow/v1/commands/change-tasks-complete` | `scheduleId` · `sequences`: `[1]` / `[2]` / `[3]` · `complete`: `true`(불리언 — `false` 로 완료 취소도 될 것으로 추정, HAR 에 없음) | 200 `{}` |
| 미완료 시술 취소 | 93 (1) | `schedule/v1/commands/cancel-flow-tasks` | `scheduleId` · `sequences`: `[4]` · `reason`: `"CANCEL"` | 200 `{}` |

합계 6 + 1 + 1 + 3 + 1 + 3 + 1 = **16 = HAR 쓰기 16**.

### 서버에 남은 결과(사실 — `get-schedule-detail` 15:28:17(#33) ↔ 15:29:22(#98) 비교)

| 칸 | 전 | 후 |
|---|---|---|
| `flowStep` | `PROCEDURE` | `PROCEDURE_DONE` |
| 작업 1 | `NOT_STARTED` · 담당 없음 · 의사 없음 | **`DONE`** · `assignees`=[방온유] · `doctors`=[권태윤] · `doctorAssignedDateTimeUtc` = `readyDateTimeUtc` = 15:28:53.893 · `completedDateTimeUtc` 15:28:59.185 |
| 작업 2 · 3 | `NOT_STARTED` | **`DONE`** · `assignees`=[방온유] · `completedDateTimeUtc` 채워짐 · **`readyDateTimeUtc` 빈 값** |
| 작업 4 | `NOT_STARTED` | **`CANCELED`** |
| 작업 `room` · `order` · `urgencyLevel` | 빈 값 · 1~4 · UNSPECIFIED | 변화 없음 |
| `ticketConfiguration` | `{}` | `{}` |

- 사실: **집도의 지정이 `readyDateTimeUtc` 를 찍는다**(작업 1 은 의사 지정 시각 = ready 시각, 의사를 안 붙인 작업 2 · 3 은 완료돼도 ready 가 비어 있다). 운영 캡처의 「ready」 시각을 시술 시작으로 읽으면 안 된다는 단서다
- 사실: 담당자 지정만으로는 ready 가 찍히지 않는다
- 상담: `get-consultations-by-visitor-id` 응답의 상담 1건 = `consultationStartedDateTimeUtc` 15:27:54.429(웹앱이 보낸 값) · `createdDateTimeUtc` 15:27:54.545 · 상담사 남준서 · 상담 의사 권태윤. → 상담 리포트(`research-counselor-trace-report.md` §2)의 「`consultationStartedDateTimeUtc` 53건 = 생성 순간」은 이 웹앱 동작(상담사 지정 순간의 브라우저 시각)으로 설명된다. 나머지 92건(= 예약 시작 시각)이 어떤 경로로 생기는지는 HAR 에 없다

---

## 3. 단계 · 상담 시작 흐름(2차에서 처음 보임)

```text
15:27:52.252  change-flow-step            → CONSULTATION_WAITING
15:27:54.430  create-consultation         counselorIds=[남준서], content.text=""
15:27:56.713  change-consultation-doctors doctorIds=[권태윤]
15:27:57.398  change-flow-step            → CONSULTATION
```

- 상담 단계로 가기 전에 **상담 기록 생성(상담사 지정)이 먼저** 나간다(사실). 공개 문서의 「`CONSULTATION` — 상담 담당자가 지정돼 있지 않으면 거절」과 맞는 순서다
- 상담 메모 본문은 이때 빈 값이다. 메모를 쓰는 요청(공개 `updateScheduleConsultationInfo` 에 해당하는 내부 작업)은 이 HAR 에 없다

귀가 대기:

```text
15:29:13.964  cancel-flow-tasks  {sequences:[4], reason:"CANCEL"}
15:29:14.071  change-flow-step   → PROCEDURE_DONE
```

1차와 같은 꼴(취소 → 107ms 뒤 단계 변경). 이번엔 남은 작업이 1개라 `sequences` 가 `[4]` 하나다. 1차의 `[1,2,3,4]` 와 합쳐 보면 **「남은(미완료) 작업 순번 전부」를 담는다**는 해석이 맞다(추정 → 근거 2건).

---

## 4. 공개 OpenAPI 대조

공개 75개 경로 · operationId 와 대조했다(공개에 `consultation/` 쓰기는 `updateScheduleConsultationInfo` 하나, `schedule/flow/` 경로는 0개).

| 내부 쓰기 | 공개 같은 작업 |
|---|---|
| `schedule/v1/commands/change-flow-step` | **있음** `changeFlowStep` |
| `consultation/v1/commands/create-consultation` | 공개 없음 |
| `consultation/v1/commands/change-consultation-doctors` | 공개 없음 |
| `schedule/flow/v1/commands/change-tasks-assignees` | 공개 없음 |
| `schedule/flow/v1/commands/change-tasks-doctors` | 공개 없음 |
| `schedule/flow/v1/commands/change-tasks-complete` | 공개 없음 |
| `schedule/v1/commands/cancel-flow-tasks` | 공개 없음 |

---

## 5. 인증 · 호스트

1차와 같다(사실).

- `Authorization` · `Cookie` · `Set-Cookie` 헤더 **0개**, HAR `cookies` 배열 **0개**. Chrome 이 HAR 를 내보낼 때 지운다. 웹앱의 인증 방식은 이번에도 알 수 없다
- 호스트 `api.kos-solution.com`(공개 `open-api.kos-solution.com` 과 다름), 경로에 `/tenants/{tenantId}`
- 헤더 이름은 1차와 같은 종류(`kos-client-uri` · `referer` · `content-type` · `x-datadog-*` · `traceparent` · `tracestate` 등)

---

## 6. 쓸 만한 조회(2차에서 새로 보인 것)

| 내부 조회 | 요청 | 주는 것 | 공개 대응 |
|---|---|---|---|
| `schedule/v1/queries/get-schedules-grouped-by-zone` | `{zoneIds[], startDateTimeUtc, endDateTimeUtc}` | **구역별 하루 일정 전체** — 일정마다 `getScheduleDetail` 과 같은 필드(차이는 `visitorLocation` 하나). DEMO 그날 4건 | 공개 `getSchedulesByFlowStep`(단계 + 기간)이 가까움. 구역 단위 · 한 번에 상세 꼴은 없음. **현황판 원천으로 가장 가까운 조회** |
| `consultation/v1/queries/get-consultations-by-visitor-id` | `{visitorId}` | 고객의 상담 기록 전체(`counselors` · `consultationDoctors` · `consultationProcedures` · `content.text` · 시각) | 공개 없음(상담은 일정 상세 안에서만) |
| `schedule/v1/queries/get-schedule-summaries` | `{visitorId, sort}` | 고객의 일정 요약(단계 · 예약 시각 · 예약 담당 · 메모 · `tasks` · `consultations`) — DEMO 9건 | 공개 `getSchedulesByVisitor` 와 비슷 |
| `schedule/v1/queries/get-payment-required-tasks` | `{visitorId}` | 결제가 필요한 작업 목록(DEMO 빈 배열) | 공개 없음 |
| `schedule/v1/queries/get-schedule-detail` | `{scheduleId}` | 공개 `getScheduleDetail` 과 같은 필드 | 있음 |
| `schedule/zone/room/v1/queries/get-rooms` · `role/v2/queries/get-roles` | 1차와 같음 | 방 목록 · 역할 목록 | 공개 없음 |
| `meta/codes/v1/queries/get-codes` | `{category}`(`FUNNEL` 등) | 코드 목록(`id · category · name · order · closed · default`) | 공개 없음 |
| 그 밖 | `v1/visitor/queries/get-visitor` · `ticket/v1/queries/get-ticket-bundles` · 선불카드 2종 · `schedule/group/v1/queries/get-reservation-group` · `purchase/payment-settings/v1/queries/get-payment-settings` · `meta/notice/v1/queries/get-notices` · `image/visitor-image/v1/queries/get-visitor-images` · `procedure-menu/visitors/queries/get-visitors` · `account/v2/…/get-accounts-last-update-date-time-utc` | 고객 · 시술권 · 선불 · 예약 그룹 · 결제 설정 · 공지 · 이미지 | 고객 · 시술권 · 선불 · 예약 그룹은 공개에 비슷한 작업 있음 |

---

## KOS 요청서 초안 — 갱신(결정은 코디 · 사용자)

**내부 API 가 확인된 것 — 「이 경로를 OpenAPI 로 열어 달라」**

1. **시술 완료하기** `schedule/flow/v1/commands/change-tasks-complete {scheduleId, sequences[], complete}` — 요청 1순위. **시술권이 걸린 작업에서 완료하면 시술권이 차감되는지 KOS 에 같이 물을 것**(이번 HAR 는 시술권 없는 작업이라 확인 못 함)
2. **담당자** `schedule/flow/v1/commands/change-tasks-assignees {scheduleId, sequences[], assigneeIds[]}`
3. **집도의** `schedule/flow/v1/commands/change-tasks-doctors {scheduleId, sequences[], doctorIds[]}` — 이 호출이 작업 `readyDateTimeUtc` 를 찍는다는 점도 문서화 요청
4. **시술 취소** `schedule/v1/commands/cancel-flow-tasks {scheduleId, sequences[], reason}` — `reason` 값 목록도
5. **상담사 지정** `consultation/v1/commands/create-consultation` · **상담 의사** `change-consultation-doctors` — 상담 id 를 호출하는 쪽이 만든다는 점, 이미 상담 기록이 있을 때 상담사만 바꾸는 작업이 따로 있는지
6. 조회: `get-schedules-grouped-by-zone` · `get-rooms` · `get-roles` · `get-consultations-by-visitor-id`

**아직 HAR 에 없는 것** — 3차 녹화가 필요하면: **방 지정 · 이동 · 우선순위 · 시술 추가 · 단건 시술 취소하기**, 그리고 시술권이 걸린 작업에서 **시술 완료하기**(전후 `get-ticket-bundles` 비교)

---

## 검증

- **쓰기 요청 수:** HAR 2차 `/commands/` 요청 **16** = §2 동작별 표 행 합 **16**(단계 변경 6 · 상담 생성 1 · 상담 의사 1 · 담당자 3 · 집도의 1 · 완료 3 · 취소 1). 합친 대응표에 쓰기 경로 7종이 모두 있다(1차 쓰기 4건의 경로 2종 포함)
- **토큰 · 쿠키 값:** HAR 의 `Authorization` · `Cookie` · `Set-Cookie` 헤더 0개 · `cookies` 배열 0개 → 리포트에 들어갈 값 없음. 추가로 HAR 의 쿼리 문자열 값 전부와 추적 헤더 값(`x-datadog-*` · `traceparent` · `tracestate` · `dd-request-id`) 전부를 리포트와 문자열 대조 → 쿼리 값 238개 · 추적 헤더 값 466개 중 리포트에 나온 것 **0건**(값은 출력하지 않고 개수만 셈)
- **재전송:** 0(HAR 는 `json.load` 로 읽기만 함)
- **고객 이름:** 리포트에 고객 이름 없음(HAR 응답의 `visitor.name` · 고객 상세 `name` · `phoneticName` 4종과 그 부분 문자열 대조 → **0건**). 직원 이름(남준서 · 권태윤 · 방온유)은 브리프 허용
