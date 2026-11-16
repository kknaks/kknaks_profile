# 조사 3차 — 새 HAR 2개: 예약 이력 · 병원 정보

> researcher · 조사일 **2026-11-16** · 데모 테넌트만. 이번에는 KOS 를 **한 번도 부르지 않았다**(공개 · 내부 0번, 쓰기 0번). HAR 과, HAR 안에 든 KOS 웹 JS 번들, 1차에 받은 openapi.yaml 만 봤다.
> public 레포다. 키 · 토큰 · 테넌트 id · KOS id · 사람 이름 · 병원 이름 · 번호 값은 적지 않았다. 경로 · 칸 이름 · 모양 · 건수만 적었다.
> 표기: **HAR** = 이번 HAR 2개 · **JS** = HAR 안의 KOS 웹 JS 번들 · **스펙** = openapi.yaml 1.0.1(작업 81개) · **추정** = 해석(근거를 함께 적음).
> 분류(1차와 같음): **A** 지금 코드에 있음 / **B** KOS 공개 API 로 됨 / **C** 내부 API(HAR)로만 됨 / **D** CC 저장 필요 / **E** 없음 · HAR 필요.

새 HAR 2개는 둘 다 데모 테넌트에서 캡처한 것이다. 테넌트 경로 조각이 `상담대기.har` 와 같고, `예약이력.har` 의 내부 계정 응답 25명 · 17명이 모두 데모 공개 `getAccounts` id 안에 있다.

---

## 0. 요약

| # | 질문 | 한 줄 답 | 분류 | KOS 호출 수 |
|---|---|---|---|---|
| 1 | 2-3 처음 상담 대기 시각 | **`예약이력.har` 에는 이력 호출이 없다.** 이 HAR 은 일정 상세의 「예약 이력」 탭이 아니라 **예약 목록 화면**(`/reservation/list`)에서 캡처됐다. 대신 KOS 웹 JS 에 내부 `schedule/v1/queries/get-schedule-event-logs {scheduleId}` 가 있다. 이 조회는 이벤트마다 `{eventType, payload, raisedDateTimeUtc, initiator, version}` 를 주고, 단계 변경 이벤트 `FlowStepChanged` 의 payload 에는 `flowStep` 이 있다. 이것이면 「처음 `CONSULTATION_WAITING` 이 된 시각」을 뽑을 수 있다(추정). 다만 **실제 응답이 없다.** 공개 스펙에도 없다(다시 대조함) | **E**(내부 경로는 JS 로만 확인 · 상세 탭 HAR 필요). 응답이 확인되면 **C** | (추정) **일정 1건당 1번.** 여러 건을 한 번에 받는 형태는 JS 에 없다 |
| 2 | 병원 정보 | `병원정보.har` 에서 내부 `/tenants/{id}/v1/hospital/queries/get-hospital`(본문 없음)이 실제로 불렸다. 응답 `data` 의 **칸 17개가 2차 JS 추정과 이름 · 개수 모두 같다.** `addressContract{address, detailedAddress, zipCode, translsMap}` 도 맞다. 데모에서 값이 든 칸은 3개(요양기관 번호 · 병원 이름 · 국적)뿐이다. 운영 시간(`get-default-operation-timetable` 등)은 두 HAR 모두 불리지 않았다 | **C** | 1번(인자 없음) |

---

## 1. 2-3 처음 상담 대기 시각

### 1.1 `예약이력.har` 에 실제로 든 것(HAR)

엔트리 33개 중 KOS 호출은 13개이고, 나머지는 분석 · RUM 이다.

- RUM 의 화면 경로는 `/{tenant}`(7) · `/{tenant}/hospital`(15) · `/{tenant}/reservation/list`(127)였다. 일정 상세나 「예약 이력」 탭으로 보이는 경로는 없다.
- 웹소켓 엔트리는 0개다.

| 경로(`/tenants/{id}/…`) | 요청 키 | 응답 키 트리 |
|---|---|---|
| `schedule/v2/queries/get-schedule-list-items` | `{tenantId(빈 문자열), updatedDateTimeUtcFrom, updatedDateTimeUtcTo, limit}`. 범위는 24시간, `limit` 2000 | `{data[]{id(uuid), visitor{id, name, chartNumber, isNew, categories[], phoneticName}, reservationStartDateTime, reservationStatus, requestedProcedureTitles[], funnel{funnel{id, category, name, order, closed, default}, funnelDetail}, reservationMemo, reservationGroupId, occupiedReservationGroups[]{reservationGroupId, startDateTimeUtc, endDateTimeUtc, doctors[]}, zone{id, title}, createdDateTimeUtc, updatedDateTimeUtc}, totalCount}`. 5건이고, `reservationStatus` 는 모두 `IN_PROGRESS` |
| `schedule/socket/v1/commands/issue-schedule-socket-token` | `{}` | `{token}`. 사용자가 화면을 열 때 KOS 웹이 부른 것이다. 우리가 부른 것이 아니다 |
| `account/v2/queries/get-accounts` ×2 | `{roleTag}` | 2차와 같은 모양 |
| `role/v2/queries/get-roles` ×3 · `get-accounts-last-update-date-time-utc` · `meta/codes/v1/queries/get-codes` ×2 · `schedule/zone/v1/queries/get-zones` · `schedule/group/v1/queries/get-reservation-groups {deleted, zoneIds[]}` · `v1/hospital/queries/get-hospital` | — | 2차 · §2 와 같은 모양 |

- `get-schedule-list-items` 원소에는 단계(`flowStep`) · 단계 변경 시각 · 이력 칸이 **없다.** 그래서 이 HAR 로는 2-3 을 풀 수 없다.

### 1.2 KOS 웹 JS 에서 찾은 이력 조회(JS)

이번 HAR 에는 JS 번들이 없었다(캐시된 것으로 추정). 그래서 앞서 받은 HAR(`2026-10-23-cc-overall-board/har/예약그룹.har`)의 reservation 클라이언트 번들을 봤다. 10-23 시점 판이다.

- 경로: `/tenants/:currentTenantId/schedule/v1/queries/get-schedule-event-logs`
- 요청: `{scheduleId}` — **일정 하나**를 받는다
- 응답 `data[]` 원소(프로토 기본값 함수 기준): `{scheduleId, version, eventType, payload(JSON 문자열), raisedDateTimeUtc, initiator}`
- KOS 웹은 `raisedDateTimeUtc` 를 이력 시각(`createdDateTime`)으로 쓰고, `scheduleId + version` 을 원소 id 로 쓴다
- `initiator`(행위자): `{type, id}`. `type` = `ACCOUNT`(계정 id → 이름) · `GANGNAMUNNI` · `HOMEPAGE` · `INTERNAL_SYSTEM`(KOS) · `KOS_CONNECT`
- `eventType` 은 63종이 JS 에 있다. 2-3 과 관계있는 것:
  - `FlowStepChanged` — payload `{flowStep(숫자 enum), raisedDateTimeUtc}`
    - KOS 웹은 `flowStep` 을 `RECEPTION` · `CONSULTATION_WAITING` · `CONSULTATION` · `PROCEDURE_WAITING` · `PROCEDURE` · `PROCEDURE_DONE` 6개로만 바꾼다. 나머지(`COMPLETED` 포함)는 `unknown` 이 되고 **화면 목록에서 빠진다**. 응답에서 빠지는 것은 아니다
  - `ReservationStatusChanged` — payload `{status}`(`CANCELED` · `NO_SHOW` · `IN_PROGRESS` · `RESERVED` · `COMPLETED`)
  - 그 밖에 `Reservation*` · `ProcedureTask*` · `Consultation*` · `EtceteraWorks*` · `TaskTimer*` · `ScheduleOrderMemoChanged` · `ScheduleCommentAdded` · `VisitorLocationChanged` 등
- 상담 단위 이력도 따로 있다: `consultation/v1/queries/get-consultation-event-logs {consultationId}` → `{consultationId, version, eventType, payload, raisedDateTimeUtc, initiator}`(`Consultation*` 이벤트)

질문별 답(모두 **추정**이다. 근거는 JS 구조뿐이고 실제 응답은 없다):

| 질문 | 답 |
|---|---|
| 이력 원소에 단계 · 시각 · 행위자가 있나 | 있다. `payload.flowStep` · `raisedDateTimeUtc` · `initiator` |
| 같은 단계를 여러 번 거친 기록이 각각 남나 | 이벤트마다 `version` 이 붙는 이벤트 로그 구조라서 각각 남는 것으로 본다. 실제 응답으로 확인하지 못했다 |
| 「처음 `CONSULTATION_WAITING` 이 된 시각」을 뽑을 수 있나 | `eventType=FlowStepChanged` 이고 `flowStep` 이 `CONSULTATION_WAITING` 인 원소 중 `raisedDateTimeUtc` 가 가장 이른 것을 고르면 된다 |
| 일정 1건당 호출인가 | 1건당 1번이다(`{scheduleId}` 하나). 여러 건 묶음 형태는 JS 에 없다 |
| board 에 넣을 때 KOS 호출 수 | 그날 일정 N건이면 N번이다. 1차의 board 는 날짜당 3~4번이고 건수와 무관하므로, 이 조회를 넣으면 호출이 건수에 비례하게 된다 |

- 1차 계산식(「접수 시각 + 접수 체류 분」 · 공개 `getScheduleStatistics`)과 비교하지는 못했다. 이 조회의 응답이 없기 때문이다.
- 숫자 `flowStep` 과 단계 이름의 대응은 JS 의 enum 상수 이름으로만 봤다. 숫자 값은 확인하지 못했다.

### 1.3 공개 스펙 다시 대조(스펙)

- openapi.yaml 에서 `event-log` · `eventlog` · `histor` · `FlowStepChanged` · `auditlog` 를 찾으면 **0건**이다. 1차 결론(공개에 없음)이 그대로다.
- 다른 HAR 32개(10-23 · 11-09 · 11-11 · 11-16)에서도 `event-logs` 경로를 실제로 부른 엔트리는 0건이다.

---

## 2. 병원 정보

### 2.1 `병원정보.har`(HAR)

엔트리 5개: KOS `role/v2/queries/get-roles` 1개 · `v1/hospital/queries/get-hospital` 1개 · 분석 · RUM 3개. RUM 의 화면 경로는 `/{tenant}/hospital` 이다.

`POST /tenants/{id}/v1/hospital/queries/get-hospital` — 요청 본문 없음 → 200

| 응답 `data` 칸 | 모양 | 데모 값 | 2차 JS 추정 |
|---|---|---|---|
| `nursingInstitutionNumber` | 문자열(요양기관 번호) | **있음**(8자) | 같음 |
| `companyRegistrationNumber` | 문자열(사업자 번호) | 빈 값 | 같음 |
| `businessLicenseImageUrl` | 문자열 | 빈 값 | 같음 |
| `companyName` | 문자열 | 빈 값 | 같음 |
| `hospitalName` | 문자열 | **있음**(15자) | 같음 |
| `representativeName` | 문자열 | 빈 값 | 같음 |
| `hospitalPhoneNumber` | 문자열 | 빈 값 | 같음(KOS 웹이 국가 번호 82 를 붙임 · JS) |
| `addressContract` | `{address, detailedAddress, zipCode, translsMap{}}` | 모두 빈 값 | **추정이 맞았다** |
| `websiteUrl` | 문자열 | 빈 값 | 같음 |
| `taxBillEmail` | 문자열 | 빈 값 | 같음 |
| `logoImageUrl` | 문자열 | 빈 값 | 같음 |
| `representativeStampImageUrl` | 문자열 | 빈 값 | 같음 |
| `hospitalMapImageUrl` | 문자열 | 빈 값 | 같음 |
| `nationality` | 문자열 | **있음**(2자) | 같음 |
| `languages` | 배열 | 빈 배열 | 같음 |
| `qualifiedInvoiceIssuerNumber` | 문자열 | 빈 값 | 같음 |
| `translsMap` | 객체 | 빈 객체 | 같음 |

- 칸 17개가 JS 기본값 함수와 이름 · 개수 모두 같다. 빠진 칸도, 더 있는 칸도 없다.
- 빈 칸도 빠지지 않고 빈 문자열로 온다.
- `translsMap` 은 언어별 번역 맵으로 추정한다. JS 처방 · 안내문 코드에서 `translsMap.hospitalName.translation` 을 읽는다.
- 데모에서는 주소 · 전화 · 대표자가 비어 있다. 실제 지점에 값이 있는지는 이 HAR 로 알 수 없다.

### 2.2 운영 시간

- `get-default-operation-timetable` · `get-default-days-off` 는 이번 두 HAR 에서 불리지 않았다. 모양은 2차 때처럼 여전히 펼치지 못했다. `상품 수납.har` 에는 이 경로가 있다.
- `예약이력.har` 에서 내부 `get-reservation-groups {deleted, zoneIds[]}` 가 13건을 줬다. 원소 모양은 공개 `getReservationGroups` 와 같다(그룹별 `operationTimetable`).

---

## 3. 정할 것 (결정하지 않고 모음)

1. **2-3 원천을 무엇으로 할지.**
   - (가) 내부 `get-schedule-event-logs`. 일정 1건당 1번이라 board 에 넣으면 호출 수가 건수에 비례한다
   - (나) 1차의 공개 통계 계산식(단계를 오간 일정은 어긋남)
   - (다) CC 가 단계 변경을 직접 기록(**D**)
   - (라) 2-3 을 상세에서만 보이고 목록에는 넣지 않기
2. **이력 조회를 쓴다면 언제 부를지.** 상세를 열 때만 부를지, 목록 캐시와 함께 부를지. 일정마다 부른 결과를 CC 에 남길지.
3. **「처음」의 기준.** 같은 날 상담 대기로 여러 번 간 경우 처음 값을 줄지 마지막 값을 줄지. KOS 웹처럼 `COMPLETED` 같은 단계를 버릴지.
4. **병원 정보로 무엇을 내보낼지.** 17칸 전부를 줄지, 일부(이름 · 전화 · 주소 · 국적 · 언어 등)만 줄지. 이미지 URL · 세금계산서 이메일 · 사업자 번호처럼 연동처에 필요 없을 수 있는 칸을 어떻게 다룰지.
5. **빈 칸을 어떻게 다룰지.** 데모는 17칸 중 14칸이 비어 있다. 비면 CC 설정 값(**D**)으로 채울지, 빈 채로 줄지.
6. **병원 정보 캐시.** 인자 없는 1번 호출이고 값이 잘 바뀌지 않을 것으로 보인다(추정). 직원 · 방 사본처럼 주기 조회로 둘지, 요청마다 부를지.

## 4. 확인하지 못한 것

1. **`get-schedule-event-logs` 의 실제 응답.** 일정 상세의 「예약 이력」 탭을 연 HAR 이 있어야 한다. 같은 단계를 여러 번 거친 일정에서 받으면 반복 기록이 각각 남는지도 함께 볼 수 있다.
2. `flowStep` 숫자 값과 단계 이름의 대응(JS 상수 이름만 봤다).
3. 지금 KOS 웹 판에서도 이력 경로가 같은지. JS 는 10-23 판이고, 이번 HAR 에는 JS 가 없었다.
4. 운영 시간 내부 조회(`get-default-operation-timetable` · `get-default-days-off`)의 응답 모양.
5. 실제 지점의 병원 정보 값 채움 정도(데모만 봤다).

## 5. 호출 기록

- KOS 호출 0번(공개 · 내부 · 쓰기 모두). 이번에는 토큰 교환도 하지 않았다.
- 원자료(JS 번들 사본)는 스크래치패드에만 있고 레포에는 없다.
