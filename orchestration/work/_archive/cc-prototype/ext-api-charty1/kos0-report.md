# WORK-014 KOS0 결과 보고 — 데모 KOS 조회(쓰기 0)

## 상태: done

> backend 워커 · 2026-11-16 · **데모 테넌트만**(공개 키 = ax-clinic `scripts/.env` 의 `KOS_API_tenent_dev` · 실제 지점 키 `KOS_API_tenent` 미사용). 내부 API 는 지금 `KosClient` 그대로(시스템 계정 `sign-in` 토큰 · 브라우저 UA · Origin · `kos-client-uri`).
> 조회 스크립트 · 원 응답은 워커 scratchpad 에만 있다(레포 밖). 이 리포트에는 **키 트리 · 꼴 · 건수만** 적는다 — 값 · id · 이름 · 금액 0.
> **코드 변경 0** · **KOS 쓰기 0**(`/commands/` 데이터 쓰기 0 — 인증용 `exchange-token` · `sign-in` 만).

## 판정

**「D-16 그대로」** — 내부 `get-schedule-event-logs` 가 실제로 단계 변경 이력을 주고, 처음 `CONSULTATION_WAITING` 시각을 뽑을 수 있다. 다만 SPEC 문구 두 곳을 실물에 맞춰 고쳐야 한다(아래 ① 「SPEC 고침 줄 후보」): `eventType` 은 **전체 이름**(`protos.schedule.event.FlowStepChanged`)이고 `flowStep` 은 **숫자가 아니라 문자열 enum 이름**이다.

## ① 이력 `schedule/v1/queries/get-schedule-event-logs {scheduleId}`

- 대상: 최근 8일 데모 일정 중 접수 뒤 단계(`flowStep` 이 비지 않고 `RESERVED` 아님) 88건 중 앞 40건 → 40번 호출 · 40/40 `200`
- 응답 키 트리: `{data[]}` · 원소 = `{scheduleId: str, version: int, eventType: str, payload: str(JSON), raisedDateTimeUtc: str, initiator: {type: str, id?: str}}`(1285 원소 모두 같은 6키)
- `eventType` 꼴: **전체 이름 문자열** — `protos.schedule.event.<이름>` · `protos.schedule.consultation.events.<이름>`. 27종 관측. 단계 변경은 정확히 `protos.schedule.event.FlowStepChanged`(136 원소). 짧은 이름 `FlowStepChanged` 와 같은 문자열은 **없다**
- `FlowStepChanged` 의 `payload`(JSON 문자열 · 136/136 `json.loads` 성공) 키 = `{flowStep, raisedDateTimeUtc}`
- **`flowStep` 꼴 = 문자열 enum 이름**(숫자 0건) — 관측 값 집합: `RECEPTION` 36 · `CONSULTATION_WAITING` 39 · `PROCEDURE_WAITING` 34 · `PROCEDURE` 14 · `PROCEDURE_DONE` 9 · `CONSULTATION` 3 · `COMPLETED` 1
- **`flowStep` ↔ `CONSULTATION_WAITING` 대응 근거**: 숫자 대응표가 필요 없다 — 값이 사본 `reservation.flow_step`(일정 `flowStep`)과 같은 문자열이다. 또 40/40 일정에서 **가장 늦은 `FlowStepChanged` 의 `raisedDateTimeUtc` 가 일정의 `flowStepUpdatedDateTimeUtc` 와 2ms 안에서 같다**(그 이벤트가 지금 단계로 바뀐 기록이라는 뜻). 지금 단계가 상담 대기인 일정 6건은 마지막 `FlowStepChanged.flowStep = CONSULTATION_WAITING`
- 상담 대기를 거친 일정: 40건 중 **38건**(`CONSULTATION_WAITING` 원소 1개 이상). 거치지 않은 일정 2건(접수 → 시술 대기 · 접수만)
- **같은 단계 반복 = 원소 둘로 남는다**: 상담 대기를 **두 번 거친 일정 1건**(접수 → 상담 대기 → 시술 대기 → 상담 대기)에서 `CONSULTATION_WAITING` 원소가 2개. 시술 대기 ↔ 시술 반복 일정 2건도 각 단계 원소가 따로 남음
- **원소 차례는 시각 순이 아닐 수 있다**: `version` 오름차순이 아닌 응답 12/40. 그래서 「첫 원소」가 아니라 **`raisedDateTimeUtc` 최솟값**을 골라야 한다(SPEC §6.11 4 「최솟값」 그대로 맞음)
- `raisedDateTimeUtc` 꼴(원소): UTC ISO `YYYY-MM-DDTHH:MM:SS.fffZ`(124) · 소수 2자리 `…SS.ffZ`(12) — **소수 자릿수가 고정이 아니다**(뒤 0 을 떼는 꼴로 보임). `payload` 안 `raisedDateTimeUtc` 는 나노초(7 ~ 9자리)이고 원소 값과 ≤ 2ms 차이 → **원소 값을 쓴다**
- `initiator.type` 관측: `ACCOUNT` · `HOMEPAGE` · `INTERNAL_SYSTEM`(쓰지 않음)
- 원소 수: 일정당 1 ~ 118(중앙 ~ 24) — 응답 크기는 일정마다 다르다

**SPEC 고침 줄 후보**(코디 판단):
1. §6.11 4 「부르기」 — `eventType = FlowStepChanged` → `eventType` 의 **마지막 `.` 뒤 조각이 `FlowStepChanged`**(실물은 `protos.schedule.event.FlowStepChanged`). 전체 문자열 일치로 할지 끝 조각 일치로 할지 정해 주면 그대로 한다(워커 제안: 끝 조각 일치 — 패키지 이름 변경에 덜 깨짐)
2. 같은 줄 「(숫자 enum 대응은 WORK-014 KOS0 확인 값)」 → **`flowStep` 은 문자열 `CONSULTATION_WAITING`**(숫자 아님)
3. 시각 파싱은 소수 자릿수 가변(2 ~ 3자리)을 받아야 한다 — 지금 `app/domain/clock.parse` 가 받는지 BE3 에서 시험으로 확인
4. T57 가짜 응답 = 위 원소 6키 · 전체 이름 `eventType` · 문자열 `flowStep` · `payload` JSON 문자열 · 차례 섞임

## ② 휴무 `schedule/default-operation-time/v1/queries/get-default-days-off {startDateTime, endDateTime}`

- 90일(오늘 KST 0시 ~ +91일 0시 직전 · UTC `…000Z`) → `200` · `{data: []}` — **0건**
- 원소 모양을 보려고 기간만 넓혀 2번 더 조회(지난 1년 · 그 앞 1년 · 다음 1년): 지난 1년에 **1건**, 나머지 0건
- 원소 키 트리: **`{id: str(24), startDateTime: str, endDateTime: str}` 3키뿐** — **이름(name) 칸이 없다**
- `startDateTime` · `endDateTime` 꼴: UTC ISO 초 단위 `YYYY-MM-DDTHH:MM:SSZ`(소수 없음). 관측 1건 = KST 0시 ~ 다음날 KST 0시(24시간 · 끝은 배타로 보임)
- 운영 시간(같이 확인 · `get-default-operation-timetable {}`): `{data{monday … sunday: {enabled: bool, startTime: str(20), endTime: str(20), breaktime{startTime, endTime}}}}` — SPEC §6.16 과 같음 · 쉬는 시간 없음 = 빈 문자열

**낼 칸 후보**(KOS `id` 는 빼고 — DEC-012 D-27):
- (가) `{startDate, endDate}` — KST `YYYY-MM-DD` 둘(끝 = `endDateTime` 직전 시각의 KST 날짜 · 하루 휴무면 둘이 같음). 여러 날 휴무도 한 원소로 그대로 옮김
- (나) `{start, end}` — ISO `+09:00` 초 단위 둘(KOS 값을 시각 그대로 · 하루 안 몇 시간 휴무도 손실 없음)
- (다) 날마다 한 원소 `{date}` 로 펼침 — 여러 날 휴무를 우리가 쪼갬(가공이 가장 큼)
- SPEC 예시의 `name` 칸은 KOS 에 **원천이 없다** → 넣지 않는다(지어 채우지 않음). 워커 제안: (가) — 날짜 범위 · 이름 없음. 몇 시간 휴무가 생길 수 있는지는 데모 1건으로 알 수 없다(관측은 24시간 1건뿐)

## ③ 공개 선불카드 `purchase/open/prepaid-card/v1/queries/get-prepaid-card-summaries {visitorId, available: true}`

- 데모 고객 60명에 불러 **카드가 있는 고객 1명**(카드 4장) — 나머지 59명 `{data: []}`(전부 `200`)
- 원소 키 트리: `{id: str(36), title: str, remainingBalance{balance{value: int, currency: str(3)}, total{value: int, currency: str(3)}}, remainingPoint{balance{value, currency}, total{value, currency}}, expirationDateTimeUtc: str, createdDateTimeUtc: str, ownerId: str, description: str, translsMap: {}, updatedDateTimeUtc: str}`
- **`remainingBalance` · `remainingPoint` 의 `balance` · `total` = 금액 객체 `{value, currency}` 맞음**(4/4 · `value` 는 int) → SPEC §4.4 표 · T51 그대로(고침 없음)
- 날짜 꼴: `createdDateTimeUtc` = `YYYY-MM-DDTHH:MM:SS.fffZ` · **`expirationDateTimeUtc` = `YYYY-MM-DDTHH:MMZ`(초 없음 · 17자)** — 파싱이 초 없는 꼴을 받아야 한다(BE1 에서 시험으로 확인)

## ④ 내부 시술권 `ticket/v1/queries/get-ticket-bundles {visitorId, sort: {by: "ticket.createdDateTimeUtc", order: 2}}`

- 데모 고객 25명 → 25/25 `200`. 묶음이 있는 고객 16명 · 묶음 합 86
- 묶음 키 트리: `{optionConfiguration{optionId, optionTitle, productTitle, promotionConfiguration, translsMap}, price{value: float, currency}, purchaseId, purchaseItemId, ticketSets[]{procedure, unit, tickets[]{id, status, price{value, currency}, createdDateTimeUtc}, title, ticketGroupId, medicalService, …}, title, translsMap, visitorId}` — 지금 코드가 읽는 칸(`optionConfiguration.optionId` · `.optionTitle` · `price` · `ticketSets[].tickets[].status` · `.createdDateTimeUtc`)이 모두 있다. `price.value` 는 **float**(지금 코드의 정수 변환 그대로 필요)
- **다 쓴 · 다 취소된 묶음(`AVAILABLE` · `IN_USE` 0장)을 준다**: 4명에게서 **11묶음**(86 중) — 내부 조회는 걸러 주지 않는다 → SPEC §4.3 「거르기」(우리가 거름)가 필요하다 · T50 「`USED` · `CANCELED` 만인 묶음 → 안 나옴」 가짜 응답이 실물과 맞다
- 관측 상태 값: `AVAILABLE` · `IN_USE` · `USED` · `CANCELED`(4종 · 그 밖 0)
- `IN_USE` 만 남은 묶음이 흔하다(묶음이 있는 고객 16명 중 12명은 장이 전부 `IN_USE`) — 0.4.0 행동 변화(「사용 중 장만 남은 묶음이 나온다」)가 데모에서 실제로 크게 보인다

## 호출 기록

| KOS 작업 | 종류 | 번 |
|---|---|---|
| `open/authorization/commands/exchange-token` · `common/v1/user/commands/sign-in` · `v1/account/queries/get-user-account` | 인증 | 각 1 ~ 2 |
| 공개 `get-zones` · 내부 `get-reservation-groups` | 읽기 | 1 · 1 |
| 내부 `schedule/v2/queries/get-schedules-for-reservation`(대상 일정 찾기 · 8일) | 읽기 | 8 |
| 내부 `get-schedule-event-logs` | 읽기 | 40 |
| 내부 `get-default-days-off` · `get-default-operation-timetable` | 읽기 | 4 · 1 |
| 공개 `get-prepaid-card-summaries` | 읽기 | 60 |
| 내부 `ticket/v1/queries/get-ticket-bundles` | 읽기 | 25 |

- **쓰기 0**. 토큰 · 키 · 응답 원문은 레포 · 리포트 어디에도 없다(원 응답 = 워커 scratchpad 만)

## 이슈 · 코디가 확인할 것

1. **판정 = D-16 그대로** — §6.11 4 「부르기」 줄 고침 두 개(전체 이름 `eventType` · 문자열 `flowStep`) 넣어 주면 BE3 를 그대로 간다
2. **`daysOff` 고른 칸** — (가) · (나) · (다) 중 하나. KOS 에 이름 칸이 없으니 SPEC §6.16 예시의 `name` 은 빼야 한다
3. 시각 꼴 가변(이력 소수 2 ~ 3자리 · 선불카드 만료 초 없음)은 계약이 아니라 파싱 문제라 BE1 · BE3 시험으로 덮는다
