# 예약 등록 모달 — KOS 예약 생성(기존 고객 · 신규 고객)

- 조사일: 2026-10-26 (KST) · 조사자: cc-prototype researcher (task_dacee03f38c8)
- 앞 판에서 이어진다: `reservation-visitor-update-report.md`(`U§`) · `reservation-questionnaire-report.md`(`Q§`) · `reservation-read-report.md`(`R§`)
- 원천
  - `reference/2026-10-23-cc-overall-board/har/예약.har` (gitignore · 항목 187개 · 04:11:13Z ~ 04:11:47Z)
  - KOS 웹앱 정적 JS: 예약 화면 `core-cf.kos-solution.com/reservation/…reservation-client_v0.0.540.js` 묶음 69개, 고객 화면 `visitor-information_v0.0.157` 묶음(앞 판에서 받은 것)
  - 공개 스펙 openapi.yaml 1.0.1(2026-10-26)
  - 시안 `design-analysis-report.md` §3.5(`D§`)
- 표기
  - **확인**: HAR 에 찍혔거나 데모에서 조회해서 본 것
  - **JS**: 웹앱 코드의 요청을 만드는 부분에 있는 것(호출은 안 했다)
  - **스펙**: openapi.yaml 에 적힌 것
  - **추정**: 해석
- **KOS 쓰기 0건.** `reserve` · `create-visitor` · `reserveV2` 등은 HAR 과 JS 로만 읽었다
- 리포트에 id · 토큰 · 이름 · 연락처 · 생년월일 · 차트번호 값은 적지 않았다

---

## 0. 요약

- **HAR 에는 예약 두 건이 있다.** ① 기존 고객(#87), ② 신규 고객(#147 고객 생성 → #174 예약)
  - 두 예약의 본문은 **최소 모양**이다: `visitorId · zoneId · occupiedResources[1] · reservationAssignee`
  - 사용자가 메모 · 상담 · 희망 시술 · 유입을 넣지 않았다
  - 넣을 수 있는 필드 전체는 JS 에서 읽었다: `visitorId · zoneId · occupiedResources · reservationAssignee · consultationRequired · sedationRequired · counselor · reservationMemo · desiredDischargeDateTimeUtc · funnel · requestedProcedures · connectedChannel`
  - **「당일 지정 의사」는 `occupiedResources[].reservationGroup.doctors[]` 다**(JS)
- **신규 고객은 두 단계다**: `find-duplicated-visitor`(이름 + 생년월일 → `{}`) → `v1/visitor/commands/create-visitor` → `{data:{id}}`
  - **「고객을 구분할 수 있는 정보가 부족합니다」는 화면 검사다**(JS `isIdentifiable`)
    - 조건 = 메인 연락처(국가 + 번호) · 여권번호 · 생년월일 · SNS(종류 + ID) · 이메일 중 하나
    - 서버 오류로 오는 것은 HAR 에서도 JS 에서도 보지 못했다
  - 「고객 수가 유형」 필수도 화면 검사다. 기본 유형이면 본문에서 **빠진다**(JS · HAR 본문에 `visitorType` 없음)
- **공개 짝**
  - 기존 고객: `reserveByVisitorIdV2`
  - 신규 고객: `reserveV2`(중복 검색 + 고객 생성 + 예약을 한 번에)
  - 슬롯 기반: `reserveByTimeSlot(WithVisitorId)`
  - 공개 v2 에는 내부 필드 중 **`counselor` · `desiredDischargeDateTimeUtc` · `connectedChannel` · `funnel`(코드)이 없다.** 공개 v2 의 유입은 `funnelDetail` 자유 텍스트뿐이다
  - 지정 의사(`reservationGroup.doctor`)는 스펙에 칸이 있지만 **「현재 공개 예약 생성·수정 요청에서는 이 값을 사용하지 않습니다」**라고 적혀 있다
  - `reserveV2` 로 신규 고객을 만들 때 **성별 · 한글 발음 칸이 없다**(`reserveByTimeSlot` 에는 `visitorGender` 가 있다)
- **고객 검색**
  - 공개 `searchVisitors` 는 차트번호 · 생년월일 · 연락처로 찾는다(데모 확인)
  - **이름만으로는 400** 이다. 이름(`partOfVisitorName`)은 연락처 · 차트번호 · 생년월일 중 하나와 함께 줄 때만 조건이 된다(스펙 · 데모 확인)
  - 내부 `visitor/v2/queries/get-visitors` 는 이름 하나로도 찾는다(HAR #149)
- **슬롯 · 정원**
  - 칸 머리의 「N명 / 30분」 = 예약 그룹의 `intervalCapacities[{zoneId, enabled, intervalCapacity}]` + `intervalMinutes` 다(데모: 정원 3 · 30분)
  - 칸마다의 지금 예약 수는 공개 `getReservationSlotsByGroupsV2.slots[]{capacity, reservationCount}` 로 온다(확인: 예약 ②가 그 칸의 `reservationCount` 에 들어 있었다)
  - 정원 초과(`ReservationCapacityExceeded`)와 같은 고객의 시간 겹침은 **서버가 거른다**(스펙 오류 예시)
  - 휴무 · 운영 시간 밖을 서버가 거르는지는 스펙에 없다
  - KOS 직원 화면은 슬롯을 `ignoreReservationPolicy: true` 로 부른다(HAR)
- 정할 것은 **13개**다(Q-50 ~ Q-62)

---

## 1. HAR 인벤토리

항목 187개 = KOS API 108 + KOS OPTIONS 21 + KOS 정적(js 16 · svg 2) + Datadog 31 + Amplitude 9.

KOS API 108건은 모두 POST · `api.kos-solution.com/tenants/{tenantId}/…` 이고 `Authorization` 헤더는 내보낼 때 빠졌다. 아래는 108건 **전부**다. 같은 경로 · 같은 본문 모양이 한 단계 안에서 이어지면 `#번호` 를 한 칸에 모았다. 칸마다의 # 개수를 합치면 108 이다(§1.13).

### 1.1 A · 예약 화면 진입 (04:11:13 ~ 15, 18건)

| # | 경로 | 본문 키 | 응답 모양 (건수) | 용도 |
|---|---|---|---|---|
| 1 | `role/v2/queries/get-roles` | — | `data[]` (15) | 역할 |
| 4 | `account/v2/queries/get-accounts-last-update-date-time-utc` | — | `data: "<UTC>"` | 직원 목록 캐시 |
| 5 | `account/v2/queries/get-accounts` | `{}` | `data[]` (79) | 직원 전체(예약 담당자 선택지) |
| 6 | `meta/codes/v1/queries/get-codes` | `category:FUNNEL_CATEGORY` | (0) | 유입 분류 |
| 7 | `meta/codes/v1/queries/get-codes` | `category:FUNNEL` | `data[{id,category,name,order,closed,default}]` (13) | 유입 채널 |
| 8 · 21 | `schedule/default-operation-time/v1/queries/get-default-reservation-policy` | `{}` | `data{}` (비어 있음) | 병원 기본 예약 정책 |
| 10 | `schedule/reservation-rule/v1/queries/get-reservation-rule-summaries` | `{}` | `data[{id,title,isActive,isDefault,lastModifiedBy,…}]` (2) | 예약 규칙 목록(활성 · 기본 1개) |
| 13 | `schedule/reservation-time-slot/v1/queries/get-reservation-time-slots` | `dateTimeRangeUtc · reservationRuleId · visitorCategoryIds[] · requestedProcedureOptionIds[] · requestedProcedureTicketIds[] · ignoreReservationPolicy:true · ignoreOfferingPeriod:true` | `data[{dateTimeRangeUtc, available, reservationPolicyViolated, offeringPeriodViolated}]` (113) + `timeSlotIntervalMinutes: 30` | 6일치 예약 가능 시각 — §4 |
| 15 | `schedule/reservation-rule/v1/queries/get-reservation-rule` | `id` | `data{id,title,isActive,isDefault,ruleSet{title, occupancyPolicy, zoneOccupancyPolicy, components[{rule{title, occupancyTarget{zoneIds[], reservationGroup{id}}}}]}, events[12]}` | 활성 규칙의 내용 — §4 |
| 17 · 20 | `schedule/default-operation-time/v1/queries/get-default-operation-timetable` | `{}` | 요일별 운영 시간 | |
| 18 | `schedule/occupied-time/v2/queries/get-occupied-times` | 날짜 범위 · `deleted` | (0) | 시간 점유 |
| 19 · 24 | `schedule/default-operation-time/v1/queries/get-default-days-off` | 날짜 범위 | (0) | 휴무 |
| 22 | `schedule/v2/queries/get-schedules-for-reservation` | `baseDateUtc · reservationGroupIds[] · zoneIds[]` | `data[일정]` | 그날 일정(R§1) |
| 23 | `schedule/group/v1/queries/get-reservation-group-days-offs` | 그룹 id 목록 · 날짜 범위 | (0) | 그룹 휴무 |
| 25 | `schedule/reservation-time-slot/v1/queries/get-occupied-resources-by-reservation-time-slot` | #13 과 같은 키 + 슬롯 하나의 `dateTimeRangeUtc` · `ignore…:false` | `data[{type:RESERVATION_GROUP, dateTimeRangeUtc, reservationGroup{reservationGroupId, zoneId, doctors[]}}]` (1) | **슬롯을 고르면 어느 예약 그룹 · 구역을 차지할지** 정한다 — 이 결과가 `reserve.occupiedResources` 로 간다 |

### 1.2 B · 고객 목록 (04:11:17.5, 1건)

| # | 경로 | 본문 키 | 응답 | 용도 |
|---|---|---|---|---|
| 33 | `visitor/v2/queries/get-visitors` | `indexOfPage · countInPage:20 · visitorName · phoneNumber · chartNumber`(모두 빈칸) · `sort{by:lastVisitedDateTimeUtc, order:DESC}` | `data[고객 상세 모양]` (20) + `count` | 예약 창의 고객 검색(빈 조건 = 최근 방문 순). JS 의 검색 조건: `visitorName · phoneNumber · chartNumber · dateOfBirth · doctorId · counselorId` |

### 1.3 C · 기존 고객 고르기 → 고객 요약 (04:11:19.6 ~ 20.0, 20건 · 같은 묶음이 두 번 나간다)

| # | 경로 | 본문 키 | 응답 | 용도 |
|---|---|---|---|---|
| 35 · 77 | `visitor/v2/queries/get-visitor` | `id` | `data{고객}` | 고른 고객 |
| 37 · 78 | `schedule/v1/queries/get-payment-required-tasks` | `visitorId` | (0) | 수납이 필요한 작업 |
| 39 | `consultation/v1/queries/get-consultations-by-visitor-id` | `visitorId` | `data[]` | 상담 기록 |
| 41 · 83 | `schedule/reservation-time-slot/v1/queries/get-reservation-time-slots` | #13 과 같음 | (113) | 고객을 고른 뒤 슬롯을 다시 부른다 |
| 42 | `schedule/v1/queries/get-schedule-summaries` | `visitorId · sort` | `data[]` | 지난 일정 |
| 44 · 84 | `ticket/v1/queries/get-ticket-bundles` | `visitorId · sort` | `data[]` | 보유 시술권(희망 시술 TICKET 선택지) |
| 61 · 80 | `visitor/questionnaire/v1/queries/get-questionnaire-submit/legacy` | `visitorId` | 400 `NotFound` | 문진 제출 여부 |
| 62 · 81 | `meta/codes/v1/queries/get-codes` | `FUNNEL` | (13) | |
| 64 · 82 | `meta/codes/v1/queries/get-codes` | `FUNNEL_CATEGORY` | (0) | |
| 65 | `purchase/prepaid-card/v1/queries/get-prepaid-card-summaries` | `visitorId · available` | (0) | |
| 66 | `purchase/prepaid-card/v1/queries/get-visitor-prepaid-card-balance` | `visitorId` | `data{remainingBalance, remainingPoint}` | |
| 69 | `procedure-menu/currency-settings/queries/get-currency-settings` | — | `data{currency:"KRW"}` | 통화 |
| 70 | `security/v2/queries/check-message-permission` | `message` | `data{available}` | 권한(U§7: 판단 근거로 쓸 수 없다) |

### 1.4 D · **예약 ① 기존 고객** (04:11:21.1)

| # | 경로 | 본문 | 응답 |
|---|---|---|---|
| 87 | **`schedule/reservation/v2/commands/reserve`** (쓰기) | §2 | `{scheduleId}`(uuid) |

### 1.5 E · 예약 ① 뒤 화면 갱신 (04:11:21.3 ~ 21.9, 11건)

| # | 경로 | 본문 키 | 응답 | 용도 |
|---|---|---|---|---|
| 89 | `get-default-days-off` | 날짜 범위 | (0) | |
| 90 | `get-accounts-last-update-date-time-utc` | — | 문자열 | |
| 91 · 100 · 104 | `schedule/group/v1/queries/get-reservation-group` | `id` | `data{예약 그룹 하나}` — `intervalMinutes:30 · intervalCapacities[{enabled, intervalCapacity:3, zoneId}] · isDefault · sameDayCloseBufferMinutes:30 · operationTimetable · order` | 만든 예약의 그룹 |
| 93 · 94 | `get-codes` | `FUNNEL_CATEGORY` / `FUNNEL` | (0) / (13) | |
| 95 | `procedure-menu/visitors/queries/get-visitors` | `sort` | (0) | 고객 유형(U§1 #37 과 같다) |
| 96 | `get-currency-settings` | — | | |
| 97 | `schedule/v1/queries/get-schedule-summaries` | `visitorId · sort` | `data[]` (+1) | |
| 102 | `schedule/v1/queries/get-schedule-detail` | `scheduleId` | `data{일정}` | 만든 예약 상세 — §2.3 |

### 1.6 F · 다시 예약 화면 (04:11:26.3 ~ 26.5, 16건)

A 와 같은 묶음이다: #108(`get-accounts-last-update…`) · #109 · #110(`get-codes` ×2) · #111 · #119(`get-default-reservation-policy`) · #112(`get-reservation-rule-summaries`) · #113(`get-reservation-time-slots`) · #114(`get-reservation-rule`) · #115 · #118(`get-default-operation-timetable`) · #116(`get-occupied-times`) · #117 · #122(`get-default-days-off`) · #120(`get-schedules-for-reservation`, 예약 ①이 들어 있다) · #121(`get-reservation-group-days-offs`) · #124(`get-occupied-resources-by-reservation-time-slot`, 다음 칸).

### 1.7 G · 신규 고객 창 열기 (04:11:28.7 ~ 28.8, 10건)

| # | 경로 | 본문 키 | 응답 | 용도 |
|---|---|---|---|---|
| 129 | `procedure-menu/target-countries/v1/queries/get-target-countries` | — | (4) | 타겟 국가(U§5: 국적 목록이 아니다) |
| 130 · 131 | `get-codes` | `FUNNEL` / `FUNNEL_CATEGORY` | (13) / (0) | |
| 132 | `meta/connect/v1/queries/get-connect-apps` | `{}` | (0) | |
| 133 · 134 · 135 | `account/v2/queries/get-accounts` | `DOCTOR` / `COUNSELOR` / `{}` | (13) / (22) / (79) | 담당 의사 · 상담사 · 추천인 |
| 136 | `procedure-menu/visitors/queries/get-visitors` | `sort` | (0) | 고객 유형 |
| 137 | `visitor/v1/queries/get-custom-attribute-definitions` | `{}` | (0) | 커스텀 속성 |
| 138 | `get-codes` | `VISITOR_CATEGORY` | (7) | 고객 분류 |

### 1.8 H · **신규 고객 만들기** (04:11:42.7, 2건)

| # | 경로 | 본문 키 | 응답 |
|---|---|---|---|
| 145 | `visitor/v1/queries/find-duplicated-visitor` | `name · birthDateUtc` | `{}`(일치 없음) |
| 147 | **`v1/visitor/commands/create-visitor`** (쓰기) | §3 | `{data:{id}}` |

### 1.9 I · 만든 고객 검색 (04:11:43.0, 1건)

| # | 경로 | 본문 키 | 응답 |
|---|---|---|---|
| 149 | `visitor/v2/queries/get-visitors` | `indexOfPage · countInPage · visitorName · sort` | (1) + `count` — **이름 하나로 찾았다**. 새 고객에게 **차트번호가 이미 붙어 있다**(KOS 가 만든다) |

### 1.10 J · 신규 고객 고르기 → 요약 (04:11:45.8 ~ 46.2, 18건)

C 와 같은 묶음이다: #151 · #164(`get-visitor`) · #152 · #165(`get-payment-required-tasks`) · #153(`get-consultations-by-visitor-id`) · #154 · #166(`get-questionnaire-submit/legacy`, 400) · #155 · #156 · #167 · #168(`get-codes` ×4) · #157 · #158(선불카드 2) · #159 · #169(`get-reservation-time-slots`) · #160(`get-schedule-summaries`, 0) · #161 · #170(`get-ticket-bundles`, 비어 있음).

### 1.11 K · **예약 ② 신규 고객** (04:11:47.0)

| # | 경로 | 본문 | 응답 |
|---|---|---|---|
| 174 | **`schedule/reservation/v2/commands/reserve`** (쓰기) | §2 · `visitorId` = #147 이 만든 고객(확인) | `{scheduleId}` |

### 1.12 L · 예약 ② 뒤 갱신 (04:11:47.1 ~ 47.5, 9건)

#175(`get-default-days-off`) · #176(`get-accounts-last-update…`) · #177 · #184(`get-reservation-group`) · #178 · #179(`get-codes` ×2) · #180(`procedure-menu/visitors/…/get-visitors`) · #181(`get-schedule-summaries`) · #183(`get-schedule-detail`).

### 1.13 합계

A 18 + B 1 + C 20 + D 1 + E 11 + F 16 + G 10 + H 2 + I 1 + J 18 + K 1 + L 9 = **108** 이다. HAR 의 KOS API 108건과 맞는다. 쓰기는 3건(#87 · #147 · #174)이다.

---

## 2. 내부 `reserve` 해부 (`schedule/reservation/v2/commands/reserve`)

### 2.1 HAR 두 건(#87 ①기존 · #174 ②신규)

```text
{
  visitorId,                                   ← 고객 id(24자)
  zoneId,                                      ← 접수 구역(= reservationGroup.zoneId 와 같았다)
  occupiedResources: [{
     id,                                       ← uuid. 화면이 만든 값으로 보인다(추정, 슬롯 조회 응답에는 id 가 없다)
     type: "RESERVATION_GROUP",
     reservationTime: {startDateTimeUtc, endDateTimeUtc},   ← "…T04:30:00.000Z" 꼴, 30분
     reservationGroup: {reservationGroupId, zoneId}         ← #25 · #124 슬롯→그룹 결과 그대로
  }],
  reservationAssignee: {id, name}              ← 예약 담당자(직원). 두 건이 같은 계정이다
}
→ 200 {"scheduleId": "<uuid>"}
```

①과 ②의 본문 키는 같다. 차이는 고객 id · 시각(30분 뒤 칸)뿐이다.

### 2.2 넣을 수 있는 필드 전체 (JS `reserveV2` 의 요청 만드는 부분)

| 필드 | 형식(JS) | HAR 에 | 메모 |
|---|---|---|---|
| `visitorId` | 문자열 | ✔ | 기존 · 신규 모두 **고객 id 가 먼저 있어야 한다**(신규는 `create-visitor` 를 먼저 부른다) |
| `zoneId` | 화면 이름 `receptionZoneId` | ✔ | 접수 구역 |
| `occupiedResources[]` | `{id, type, reservationTime, reservationGroup{reservationGroupId, zoneId, doctors[{id,name}]}}` | ✔(`doctors` 없음) | **`doctors` = 「당일 지정 의사」**. 일정 응답의 `occupiedResources[].reservationGroup.doctors[]` 로 다시 보인다 |
| `reservationAssignee` | `{id, name}` | ✔ | |
| `consultationRequired` | bool | ✗ | 상담 필요 |
| `sedationRequired` | bool | ✗ | 수면 마취 |
| `counselor` | `{id, name}` | ✗ | **희망 상담사** |
| `reservationMemo` | 문자열 | ✗ | |
| `desiredDischargeDateTimeUtc` | 문자열 | ✗ | 귀가 희망 시각 |
| `funnel` | 변환기를 거친다 → 일정의 `funnel{funnel{…}, funnelCategory{…}, funnelDetail}` 모양(R§3.1 16행) | ✗ | 유입 채널(코드 · 분류 · 상세) |
| `requestedProcedures[]` | `{type: OPTION, optionConfiguration{optionId, optionTitle, …}}` 또는 `{type: TICKET, ticketConfiguration{ticketId, ticketTitle, …}}` | ✗ | 희망 시술 = 상품 옵션 또는 보유 시술권 |
| `connectedChannel` | enum(`HOMEPAGE · GANGNAMUNNI · KOS_CONNECT · …`) | ✗ | |
| (`visitorRequest`) | 화면에서 뺀다(`omit`) | — | 고객 요청사항은 직원 화면에서 넣지 않는다 |

JS 의 서버 오류 처리(`reserveV2` 실패를 화면 문구로 바꾸는 부분)

| 서버 오류 `errorProperties` | 화면 코드 |
|---|---|
| `startDateTime` NotAvailable | `ALREADY_RESERVED`(같은 고객 시간 겹침, 스펙 예시와 같다) |
| `occupiedResources` Required | `OCCUPIED_RESOURCES_EMPTY` |
| `occupiedResources[n].id` Required / Duplicated | id 빠짐 / 중복 |
| `occupiedResources[n].startDateTimeUtc` NotAvailable | `DIFFERENT_DATE_IN_OCCUPIED_RESOURCES` |
| `visitorId` NotFound · `zoneId` NotFound · `occupiedResources[n].zoneId` NotFound | 고객 없음 · 구역 없음 · 구역이 그룹에 없음 |

**정원 초과 오류를 처리하는 코드는 JS 의 이 목록에 없다.** 내부 `reserve` 가 정원을 거르는지는 알 수 없다(추정: 직원 화면은 정책을 무시한다, §4) → Q-55

같은 묶음에 다른 예약 쓰기도 있다(JS, 이번 범위 밖): `reservation/v2/commands/update-reservation` · `v1/commands/cancel-reservation` · `revoke-canceled-reservation` · `replace-reservation-requested-procedures` · `change-visitor-location` · `issue-reception-token`.

### 2.3 만든 예약이 어떻게 보이나 — 공개 `getScheduleDetail` (데모 조회)

| | ① 기존 | ② 신규 |
|---|---|---|
| `flowStep` / `reservation.status` | `RESERVED` / `RESERVED` | 같음 |
| `visitor.isNew` | false | **true** |
| `consultationRequired` · `sedationRequired` | false · false | 같음 |
| `reservationMemo` · `counselor` · `requestedProcedures` | 빈칸 · 없음 · 0 | 같음 |
| `reservationAssignee` | 있음 | 있음 |
| `funnel` / `connectedChannel` | `{funnelDetail:""}` / `Channel_UNSPEICIFED` | 같음 |
| `zone.title` | 「4층」 | 같음 |
| `occupiedResources[0].reservationGroup.doctors` | `[]` | `[]` |

내부로 만든 예약이 공개 조회에서 그대로 보인다(확인).

---

## 3. 내부 `create-visitor` 해부 (`v1/visitor/commands/create-visitor`)

### 3.1 HAR #147 본문

`name · dateOfBirth("yyyy-MM-dd 00:00:00.000Z" 꼴) · address{address, detailedAddress, zipCode}(빈칸) · gender(MALE) · language("ko") · aggrementPersonalInformation(true) · agreementInformationalNotification(true) · passportSurname · passportGivenNames · passportExpiryDate(빈칸) · phoneticName(3자)` → `{"data":{"id":"<24자>"}}`

- 연락처 · 이메일 · 여권번호 · SNS 는 넣지 않았다. **구분 정보 = 생년월일 하나**로 만들어졌다
- `nationality` 키가 없다. 만든 고객은 `nationality: "KR"` 로 조회됐다(#149) → 기본값이 KR 이거나 화면 기본값이 빠진 것이다(추정)

### 3.2 넣을 수 있는 필드 전체 (JS `toCreateVisitorCommand`)

`name · phoneticName · phoneNumber{countryCode, phoneNumber} · visitorType(기본 유형이면 빠짐) · dateOfBirth · registrationNumber · address{zipCode, address, detailedAddress} · gender · nationality · language · doctor · counselor · funnel(funnelId) · recommenderName · aggrementPersonalInformation · aggrementAdvertisements · memo · additionalPhoneNumber · snsInfo{snsType, accountId} · foreignRegistrationNumber · passportNumber · detailedFunnel · agreementInformationalNotification · email · visitorFunnel · visitorCategories[] · passportSurname · passportGivenNames · passportExpiryDate(yyyy-MM-dd) · referrer · lineInformation[] · unniInformation[] · customAttributes[]`

앞 판 `update-visitor-personal-information`(U§2.1)과 비교

| 구분 | 필드 |
|---|---|
| 두 작업에 모두 있음 | 개인 정보 전부(이름 · 발음 · 연락처 2 · 이메일 · 생년월일 · 성별 · 주민번호 · 외국인등록번호 · 여권 4 · 주소 · 국적 · 언어 · SNS) |
| 생성에만 있음 | 관리 정보(`memo · doctor · counselor · funnel/visitorFunnel/detailedFunnel · referrer/recommenderName · visitorType · visitorCategories · 동의 3 · customAttributes · lineInformation · unniInformation`). 수정할 때는 관리 정보 작업(U§2.3)이 따로 있다 |

### 3.3 검사는 화면에서 한다

JS 고객 저장 함수: 생성은 `xt() && jt()` 를 모두 통과해야 `createVisitor` 를 부른다.

| 검사 | 내용 | 어디서 |
|---|---|---|
| `requiredName` | 이름 없음 | 화면 |
| `invalidPhoneticNameIncludeHiragana` | 발음에 히라가나 → 「가타카나로」 | 화면 |
| **`notIdentifiable`** | `isIdentifiable` = (연락처 국가 + 번호) ∨ 여권번호 ∨ 생년월일 ∨ (SNS 종류 + ID) ∨ 이메일. 없으면 모달 「고객을 구분할 수 있는 정보가 부족합니다」 + 다섯 항목 목록 | **화면**. 이 조건의 서버 오류 처리는 JS 에 없다 |
| 연락처 · 주민번호 · 외국인등록번호 · 이메일 형식 · 여권 영문 대문자 | 형식 검사 | 화면 |
| `requiredVisitorType` | 「고객 수가 유형을 선택해주세요」 | 화면. 기본 유형은 본문에서 빠진다 |
| `requiredFunnel` · `…Category` · `…Detail` | 지점 설정에 따라 유입 필수 | 화면(설정이 켜졌을 때만) |

서버가 구분 정보 없이 고객을 만들게 두는지는 확인하지 못했다(쓰기 금지) → Q-52.

공개 쪽은 이렇다
- `reserveByTimeSlot`: 스펙 설명에 「`visitorPhone · visitorSnsInfo · visitorEmail · visitorPassportNumber · visitorBirthDayUtc` 중 하나 이상을 **반드시** 전달」이라고 적혀 있다. 사용자가 정한 규칙(이름 + 다섯 중 하나)과 같다
- `reserveV2`: 같은 문구는 없다. 다섯 필드가 「중복 검색과 새 내원객 생성에 사용」된다고만 적혀 있다

---

## 4. 슬롯 · 정원 · 검증

| 무엇 | KOS 에서 | 근거 |
|---|---|---|
| 칸(열) | 예약 그룹. 데모 13개(R§3.3) | 확인 |
| 칸 간격 | 그룹 `intervalMinutes`(데모 15/30/60) · 슬롯 조회 `timeSlotIntervalMinutes: 30` | 확인 |
| **정원 「N명 / 30분」** | 그룹 `intervalCapacities[{zoneId, enabled, intervalCapacity}]` — 구역마다 따로 있다. 데모 「국내」: 4층 3 · 다른 구역 1(enabled false) | 확인(R §1 #9 · 이번 #91) |
| 칸마다의 예약 수 | **공개 `getReservationSlotsByGroupsV2`** → `data[{reservationGroupId, zoneId, slots[{startDateTimeUtc, endDateTimeUtc, capacity, reservationCount, zone{id,name}}]}]` | 데모 오늘: 14묶음(그룹 × 구역). 예약 ②의 칸이 `capacity 3 · reservationCount 1` 이었다(확인) |
| 예약 가능 시각 | **예약 규칙**(활성 · 기본 1개)이 정한다. 규칙 `ruleSet{occupancyPolicy: ALL_MATCHED_SEQUENTIAL, zoneOccupancyPolicy: SINGLE_ZONE_ONLY, components[1]{rule{occupancyTarget{reservationGroup}}}}` — 데모 규칙은 **예약 그룹 1개(국내)만** 가리킨다 | 확인(#15). 공개 `getReservationTimeSlots`(규칙 생략 = 기본 규칙) · `getReservationRuleSummaries`(2) 도 200 |
| 슬롯 → 그룹 | 내부 `get-occupied-resources-by-reservation-time-slot` 이 슬롯 하나를 「어느 그룹 · 구역을 차지할지」로 바꾼다. 공개는 `reserveByTimeSlot(WithVisitorId)` 가 서버에서 같은 일을 하는 것으로 보인다(스펙: 「조회한 슬롯 범위를 전달」, 추정) | 확인 · 스펙 |
| 운영 시간 · 휴무 · 점유 | 그룹 `operationTimetable` · `sameDayCloseBufferMinutes:30`, 병원 `get-default-operation-timetable` · `get-default-days-off`, 그룹 `get-reservation-group-days-offs`, `get-occupied-times` — 모두 내부 조회(R§2) | 확인 |
| 정책 무시 | KOS 직원 화면은 슬롯을 **`ignoreReservationPolicy: true · ignoreOfferingPeriod: true`** 로 부른다. 113슬롯 중 1개가 `reservationPolicyViolated: true` 인데도 `available: true` 였다 | 확인 |
| 서버가 거르는 것 | 공개 `reserveV2` · `reserveByVisitorIdV2` 의 400 예시: **슬롯 정원 초과 `ReservationCapacityExceeded`** · **같은 고객의 시간 겹침**(`startDateTime` NotAvailable) · 날짜가 다른 일정 · 구역이 그룹에 없음 · 그룹 없음 · 담당자 없음/비활성 · 전화번호. `reserveByTimeSlot` 은 「해당 시간이 예약 불가능한 경우」 | 스펙 |
| 서버가 거르는지 모르는 것 | 휴무일 · 운영 시간 밖 · 시간 점유 칸에 예약하는 것(`reserveV2` 오류 예시에 없다). 내부 `reserve` 의 정원 초과(JS 처리 목록에 없다) | → Q-55 |

시안과 비교
- 「칸 [+]」(D§3.1): 칸 = 그룹 · 시각이 이미 정해져 있다. 그래서 KOS 의 「규칙 → 슬롯 → 그룹」 순서가 아니라 **그룹 · 시각을 직접 고르는 `reserveByVisitorIdV2`(occupiedResources 에 그룹 지정)** 꼴과 맞는다. 데모의 기본 규칙은 그룹 1개만 다루므로, 규칙 기반 슬롯 조회로는 다른 12개 칸의 가능 시각이 나오지 않는다(추정) → Q-54
- 드래그 이동(R Q-13): 공개 `updateReservationV2{scheduleId, zoneId, occupiedResources}` · 내부 `reservation/v2/commands/update-reservation` 이 있다(쓰기 · 이번 범위 밖). 정원 · 겹침 검사는 생성과 같은 오류를 쓰는 것으로 보인다(JS 의 `updateReservationV2` 오류 처리가 같은 목록이다)

---

## 5. 공개 짝 · 차이

| 내부 | 공개 | 필드 차이 |
|---|---|---|
| `reservation/v2/commands/reserve`(기존 고객 id) | **`reserveByVisitorIdV2`** `{visitorId*, zoneId*, occupiedResources*[{startDateTimeUtc*, endDateTimeUtc*, reservationGroup*{reservationGroupId*, zoneId*, doctor}}], reservationAssigneeId, consultationRequired, sedationRequired, reservationMemo, requestedProcedures[], funnelDetail}` | 공개에 **없는 것**: `counselor` · `desiredDischargeDateTimeUtc` · `connectedChannel` · `funnel`(코드 · 분류). 유입은 `funnelDetail` 자유 텍스트만 있다. 지정 의사 `reservationGroup.doctor` 는 「현재 사용하지 않음」(스펙) — 내부는 `doctors[]`(배열). 담당자는 내부 `{id,name}` / 공개 `reservationAssigneeId`. `occupiedResources.id · type` 은 공개에서 받지 않는다 |
| `create-visitor` → `reserve` (두 번) | **`reserveV2`** — 중복 검색(`visitorName · visitorPhone · visitorEmail · visitorPassportNumber · visitorSnsInfo · visitorBirthDayUtc · visitorConnectedInformation`) → 있으면 그 고객, 없으면 새로 만들어 예약 | 새 고객에 넣을 수 있는 것: 이름 · 연락처 · 이메일 · 여권번호 · 여권 성/이름 · 국적 · 언어 · SNS · 생년월일. **성별 · 한글 발음 · 주소 · 주민번호 · 메모는 없다.** 고객 id 를 미리 알 수 없다(응답은 `scheduleId` 뿐이다, 스펙) |
| (슬롯 기반) | `reserveByTimeSlot` · `reserveByTimeSlotWithVisitorId` `{reservationDateTimeRange*, reservationRuleId, visitorName* …, visitorGender, visitorIsNew, visitorCategoryIds, visitorLanguageCode, funnel, visitorRequest, …}` | 그룹을 고르지 않는다(규칙이 정한다). `reserveByTimeSlot` 에는 **성별 · `funnel`(전체)** 이 있다 |
| `visitor/v2/queries/get-visitors`(이름 하나로도 됨) | **`searchVisitors`** `{offset*, limit*, chartNumber, dateOfBirth, phone, email, partOfVisitorName}` → `data[{id, chartNumber, name, phoneNumber, dateOfBirth, gender, nationality, passportSurname?, passportGivenNames?}]` | 이름(`partOfVisitorName`)과 이메일은 **보조 조건**이다. 연락처 · 차트번호 · 생년월일 중 하나가 있어야 한다 |
| `visitor/v1/queries/find-duplicated-visitor` | `findDuplicatedVisitorId` | U§4 와 같다. HAR #145 본문(이름 + 생년월일)으로 지금 부르면 신규 고객이 나온다(확인) |

**공개 `searchVisitors` 데모 조회**(HAR 에 나온 두 고객으로)

| 보낸 조건 | 결과 |
|---|---|
| 이름만(`partOfVisitorName`) | **400** `BAD_REQUEST` |
| 차트번호(신규 고객) | 200 · 1건 · 그 고객 |
| 차트번호(기존 고객) | 200 · 1건 · 그 고객 |
| 생년월일(신규 고객) | 200 · 1건 |
| 생년월일 + 이름 | 200 · 1건 |
| 차트번호(기존) + 이름(신규) | 200 · 0건(두 조건을 함께 건다) |
| 연락처(기존 고객의 번호) | 200 · 20건(한도). **데모에서는 같은 번호를 가진 고객이 20명 넘게 있었다** — 그 고객은 첫 20건 안에 없었다 |

응답 키: 여권 이름이 있는 고객만 `passportSurname · passportGivenNames` 키가 붙는다(빈 값은 키가 빠진다).

---

## 6. 모달 필드 대조표 (D§3.5 「예약 등록」)

| # | 시안 | 공개 | 내부 (HAR · JS) | 없음 · 메모 |
|---|---|---|---|---|
| C1 | 고객 검색 · 이름 | `searchVisitors.partOfVisitorName`(보조만) | `get-visitors.visitorName`(단독 가능) | 공개로는 이름만으로 검색할 수 없다 → Q-50 |
| C2 | 고객 검색 · 연락처 | `searchVisitors.phone{countryCode, phoneNumber}` | `get-visitors.phoneNumber` | |
| C3 | 고객 검색 · 생년월일 | `searchVisitors.dateOfBirth`(ISO 또는 `yyyy-MM-dd HH:mm:ss.SSS'Z'`) | `get-visitors.dateOfBirth` | |
| C4 | 고객 검색 · 차트번호 | `searchVisitors.chartNumber`(일치) | `get-visitors.chartNumber` | 차트번호는 KOS 가 고객을 만들 때 붙인다(#149) |
| C5 | 결과 표 · 차트번호 · 이름 (발음) · 생년월일 · 국적 | `searchVisitors` 응답에 **발음(`phoneticName`)이 없다** | `get-visitors` 응답에 모두 있다 | → Q-50 |
| C6 | 페이지 나눔 | `offset · limit` | `indexOfPage · countInPage` + `count`(전체 수) | 공개에는 전체 수가 없다 |
| C7 | 「이름이 같은 기존 고객이 있어요」 | 이름만으로는 `findDuplicatedVisitorId` · `searchVisitors` 둘 다 안 된다 | `get-visitors(visitorName)` 은 된다. 이름이 포함되는지(부분) 일치인지는 미확인 | KOS 중복 기준(이름 + 다섯 중 하나)과 시안 경고 기준이 다르다 → Q-51 (U Q-43) |
| C8 | 예약 초안 Badge 「신규 고객 / 기존 고객 · No.N」 | 기존: `searchVisitors.chartNumber` | 같음 | 신규는 만들기 전에 차트번호가 없다 |
| F1 | 예약일 · 시간 | `occupiedResources[].startDateTimeUtc · endDateTimeUtc` | `occupiedResources[].reservationTime` | 모든 일정은 같은 날이어야 한다 |
| F2 | 권역 | `occupiedResources[].reservationGroup.reservationGroupId`(+ `zoneId`) | 같음 | 권역 = 예약 그룹(사용자 결정) |
| F3 | 유입 채널 | `funnelDetail`(자유 텍스트)만. `reserveByTimeSlot` 에는 `funnel` 이 있다 | `funnel{funnel 코드, funnelCategory, funnelDetail}` · `connectedChannel` | 시안 선택지 6개 ↔ 지점 코드 13개(R Q-11) → Q-56 |
| F4 | 이름 (여권) | 신규: `reserveV2.visitorName` + `visitorPassportSurname · GivenNames` | 신규: `create-visitor.name · passportSurname · passportGivenNames` | 기존 고객의 여권 이름 수정은 U§2(내부) |
| F5 | 한글 발음 | **없음**(`reserveV2` 에 칸 없음 · 문진 `phoneticName` 은 Q§M2) | `create-visitor.phoneticName` | → Q-53 |
| F6 | 생년월일 | 신규: `reserveV2.visitorBirthDayUtc`(ISO) | `create-visitor.dateOfBirth`(`yyyy-MM-dd 00:00:00.000Z`) | 날짜 기준이 서로 다르다(U Q-41) |
| F7 | 국적 | 신규: `reserveV2.visitorNationality`(ISO alpha-2) | `create-visitor.nationality` | 넣지 않으면 KR 로 보였다(§3.1) |
| F8 | 성별 | **`reserveV2` 에 없음**(`reserveByTimeSlot.visitorGender` 에는 있음) | `create-visitor.gender` | → Q-53 |
| F9 | **통역** | **KOS 예약에 없음** | 없음 | KOS 에서 통역이 있는 곳은 문진 「상담 시 통역이 필요하신가요?」(Q§M21) · 지난 예약 그룹 이름 「통역」(R§3.3) · 메모뿐이다 → Q-57 |
| F10 | **원장 상담** | `consultationRequired`(bool, 「상담 필요 여부」) · 지정 의사 `reservationGroup.doctor` 는 **사용하지 않음**(스펙) | `consultationRequired` · **`occupiedResources[].reservationGroup.doctors[]`(당일 지정 의사)** · `counselor`(희망 상담사) | 「상담 필요」가 실장 상담인지 원장 상담인지 KOS 문서에 없다. 원장 지정은 내부에서만 된다 → Q-58 |
| F11 | **희망 시술 / 예산** | 희망 시술: `requestedProcedures[]`(OPTION `optionId · optionTitle · price` / TICKET `ticketId · ticketTitle`). 예산: **없음** | 같음(시술권 선택지는 `get-ticket-bundles`) | KOS 희망 시술은 **상품 옵션 · 시술권 id** 여야 한다. 시안의 자유 글자(「써마지 FLX …」)와 다르다. 예산은 문진 「대략적인 시술 예산」에만 있다 → Q-59 |
| F12 | 예약 메모 | `reservationMemo` | 같음 | 시안의 자동 조합(「YY.M.D/본사/시술/통역/원장」)은 화면이 만든다 |
| F13 | (시안 밖) 예약 담당자 · 수면 마취 · 귀가 희망 · 상담사 | `reservationAssigneeId` · `sedationRequired` / 귀가 희망 · 상담사 **없음** | `reservationAssignee` · `sedationRequired` · `desiredDischargeDateTimeUtc` · `counselor` | 시안에는 칸이 없다. 담당자를 누구로 넣을지 → Q-60 |
| E1 | [예약 등록] 켜짐 조건 | 시안: 이름이 비면 꺼짐. KOS: 신규 = 이름 + 구분 정보 하나(화면 검사, `reserveByTimeSlot` 은 서버 필수) · 칸 = 그룹 + 시각 · 구역 | 화면 검사 `isIdentifiable` · `requiredVisitorType` | → Q-52 |
| E2 | 정원 · 겹침 | 서버 400(정원 초과 · 같은 고객 겹침) | 정원 처리가 JS 에 없다 | → Q-55 |

---

## 7. 정할 것 (결정하지 않음) — 13개

| # | 자리 | 왜 정해야 하나 | 앞 판 |
|---|---|---|---|
| Q-50 | 고객 검색을 공개로 할지 내부로 할지 | 공개 `searchVisitors` 는 이름만으로 못 찾고, 발음 · 전체 수를 주지 않는다. 내부 `get-visitors` 는 이름 하나로도 되고 시안 결과 표의 값을 모두 준다 | — |
| Q-51 | 「이름이 같은 기존 고객」 경고 기준 | KOS 중복 기준(이름 + 연락처/생년월일 등)과 다르다. 이름만으로 경고할지(내부 검색), KOS 기준을 따를지 | U Q-43 |
| Q-52 | 신규 고객 구분 규칙을 누가 검사하나 | KOS 에서는 화면이 검사한다(서버 검사는 미확인). ccc 화면이 같은 규칙(이름 + 다섯 중 하나)을 검사할지. 공개 `reserveByTimeSlot` 은 서버가 필수로 본다 | 사용자 결정(2026-10-26) |
| Q-53 | 신규 고객을 `reserveV2` 한 번으로 만들지, 내부 `create-visitor` → 예약 두 번으로 만들지 | `reserveV2` 는 성별 · 한글 발음 · 주소 · 메모를 받지 않는다. 만든 고객 id 도 응답에 없다. 만든 뒤 내부 고객 수정(U§2)으로 채울지도 포함한다 | U Q-39 |
| Q-54 | 칸 [+] → 예약을 그룹 지정 방식(`reserveByVisitorIdV2`)으로 할지, 규칙 · 슬롯 방식(`reserveByTimeSlot`)으로 할지 | 시안 칸은 그룹 · 시각이 정해져 있다. 데모 기본 규칙은 그룹 1개만 가리킨다 | R Q-4 · Q-5 |
| Q-55 | 정원 · 휴무 · 운영 시간 · 점유 검사 | 공개는 정원 · 겹침을 서버가 거른다. 휴무 · 운영 시간 밖 · 점유는 스펙에 없다. KOS 직원 화면은 정책을 무시한다. ccc 가 칸 [+] 을 막을지, 서버 오류만 보일지 | R Q-13 |
| Q-56 | 유입 채널 | 공개 v2 는 자유 텍스트(`funnelDetail`)만, 내부 · `reserveByTimeSlot` 은 코드를 받는다. 시안 6개 선택지를 KOS 코드에 대응시킬지 | R Q-11 |
| Q-57 | 통역을 어디에 둘지 | KOS 예약 필드가 없다. 문진 답 · 예약 메모 · ccc 중 어디에 둘지 | Q-38 |
| Q-58 | 「원장 상담」 | `consultationRequired`(상담 필요) · 당일 지정 의사(`reservationGroup.doctors[]`, 내부만) · 희망 상담사(`counselor`, 내부만) 중 무엇과 맞출지. 「상담 필요」의 정의(실장/원장)를 KOS 에 확인할지 | — |
| Q-59 | 희망 시술 / 예산 | KOS 는 상품 옵션 · 시술권 id 만 받는다. 시안 자유 글자를 옵션으로 고르게 할지, 메모로 둘지. 예산은 KOS 예약에 없다(문진에만) | Q-38 |
| Q-60 | 예약 담당자 | KOS 는 직원 계정을 넣는다(HAR 은 화면을 쓴 계정). ccc 가 시스템 계정 · 직원 매핑 · 비움 중 무엇으로 넣을지(공개는 활성 직원만) | U Q-49 |
| Q-61 | 「신규 고객 · 기존 고객 · No.N」 표시 시점 | 신규 고객은 만들기 전에 차트번호가 없다(KOS 가 붙인다). `reserveV2` 는 고객 id · 차트번호를 돌려주지 않는다. 차트번호 정본은 지금 KOS(사용자 결정) | 사용자 결정 |
| Q-62 | 내부 `reserve` 의 `occupiedResources[].id` | 화면이 uuid 를 만들어 넣는 것으로 보인다(중복이면 오류). 내부로 보낼 때 ccc 가 만들지. 공개는 받지 않는다 | — |

---

## 8. 호출 기록 · 빠진 행 점검

**호출**(2026-10-26, 데모 테넌트, 조회만)
- 공개(데모 키): `exchange-token` 1 + 조회 13
  - `searchVisitors` 7(200 ×6 · 400 ×1)
  - `findDuplicatedVisitorId` 1 · `getScheduleDetail` 2 · `getReservationSlotsByGroupsV2` 1 · `getReservationTimeSlots` 1 · `getReservationRuleSummaries` 1 — 모두 200
- 내부: 이번 판에서는 부르지 않았다(HAR 과 JS 로 충분했다)
- 정적 파일: 예약 화면 JS `remoteEntry` + 묶음 68개(GET)
- **쓰기 0건**, 운영 키 0건

**빠진 행**
- HAR: 항목 187 = KOS API 108 + OPTIONS 21 + 정적 18 + Datadog 31 + Amplitude 9. 인벤토리 §1.1~§1.12 의 # 를 모두 합치면 108(§1.13)
- 두 흐름: ① 기존 = B → C → D(#87) → E, ② 신규 = G → H(#145 · #147) → I → J → K(#174) → L
- 모달 대조 25행
  - 고객 검색 · 결과 · 경고 · Badge: C1~C8
  - 예약 초안 12필드 + 메모: F1~F12, 시안 밖 필드: F13
  - 켜짐 조건 · 검사: E1 · E2
  - 브리프가 짚은 통역 · 원장 상담 · 희망 시술/예산은 F9 · F10 · F11 이다
- 정할 것 13개(Q-50 ~ Q-62)
