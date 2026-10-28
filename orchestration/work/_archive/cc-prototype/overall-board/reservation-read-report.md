# 예약 현황 조회 — HAR 내부 API ↔ KOS 공개 API 대조

- 조사일: 2026-10-26 (KST) · 조사자: cc-prototype researcher (task_dacee03f38c8)
- 범위: 시안 「현황 › 예약 현황」 화면에 보이는 값을 **조회로** KOS 에서 가져올 수 있는지만 본다. 쓰기(등록 · 이동 · 취소 · 접수 · 방 배정)는 이번 판에서 다루지 않는다
- 원천
  - HAR: `reference/2026-10-23-cc-overall-board/har/예약현황_조회.har` (gitignore). 2026-10-26T00:50Z 에 데모 테넌트에서 뜬 것이다. HAR 의 테넌트 · 구역 id 가 procedure `.env` 의 데모 값과 같은지 비교했고, 같았다(값은 적지 않는다)
  - 시안 필드: `orchestration/work/overall-board/design-analysis-report.md` §3 · §7.2 (아래 `D§`)
  - 공개 API: `https://developers.kos-solution.com/openapi.yaml` 을 2026-10-26 에 받았다. `info.version` **1.0.1** · 작업 75개. 10-20 조사(`kos-demo-api.md`)의 개수와 같다. 문서 위치는 `스펙 <스키마 이름>.<필드>` 로 적는다. 웹 문서는 `https://developers.kos-solution.com/docs/openapi/<태그>#<operationId>` 다
  - 이미 아는 것: `reference/2026-10-12-cc-prototype/kos-demo-api.md` (`KDA§`) · `workflow-v2.md` 「KOS 반영 표」 · 「인증 · 계정」 · `workflow-v1.md` 1 · 2절
- 표기
  - **확인** = 이번에 데모에서 실제로 불러서 본 것
  - **스펙** = openapi.yaml 에 적힌 것
  - **추정** = 해석. 결정 근거로 쓰지 않는다
  - **계산** = KOS 값 하나에서 정해진 규칙으로 바로 나오는 값(예: 생년월일 → 만 나이). 다른 필드로 짐작해 채우는 것과 다르다. 그래도 화면이 계산해야 하므로 「정할 것」에 올렸다
- public 레포다. 실명 · 연락처 · KOS id · 키 · 토큰 값은 적지 않았다. 응답은 모양 · 건수 · enum 만 적는다

---

## 0. 요약

- **HAR 의 KOS 요청은 14건이다.** 브리프에는 15건이라고 되어 있었다. HAR 항목은 모두 18개다: KOS 14 · Datadog RUM 3 · Amplitude 1. KOS 요청의 경로는 **11종**이고, 브리프 목록과 같다. 중복 호출은 3건이다(`get-accounts` 는 roleTag 만 다르고, `get-reservation-group-days-offs` · `get-schedules-for-reservation` 은 본문까지 같다)
- **카드 한 장을 그리는 데 필요한 값은 공개 API 만으로 조회된다.** 예약 시각 · 상태 · 이름 · 성별 · 국적 코드 · 초진/재진 · 차트번호 · 권역 그룹 id 다. 원천은 `getSchedulesByFlowStep` 이다. 다만 **하루 전체를 받으려면 flowStep 마다 한 번씩, 8번 불러야 한다.** 내부 `get-schedules-for-reservation` 은 1번이면 된다. 2026-08-25 하루로 맞대 봤다: 공개 8회 합집합 34건 = 내부 34건 = `getScheduleStatistics` 34건. id 집합이 같았다. 일정 한 건의 필드 모양도 공개와 내부가 같았다
- **권역 = KOS 「예약 그룹」의 `title` 이다.** 데모의 예약 그룹 13개 중 5개 이름이 시안의 5칸과 글자까지 같다(국내 · 중화권 · 영미권 · 일본 · 기타). 나머지 8개는 시술 이름이다(리프팅 · 레이저 · 필러 · 스킨부스터 · 보톡스 · 후관리 · 수액/체형 · 제모). 08-25 일정 34건 중 **22건이 시술 그룹에 들어 있다.** 시안 5칸에 넣을 자리가 없다 → 정할 것
- **공개 API 에 없어서 내부 API 로만 볼 수 있는 것**: 방 목록(`get-rooms`) · 공지(`get-notices`) · 기본 운영 시간과 휴무(`get-default-operation-timetable` · `get-default-days-off`) · 그룹 휴무(`get-reservation-group-days-offs`) · 시간 점유(`get-occupied-times`) · 역할 이름(`get-roles`)
- **KOS 에 아예 없는 것**: 주민등록번호 · 여권번호, 신분증 확인과 스캔, 고객 입력 링크 · QR, 여정 리포트, 후납 금액, 처방전 내용(공개 API 기준), 본사 예약 요청과 원문, 상담사의 「지금 상태」, 접수한 직원, 국가명 · 국기
- 실호출은 모두 200 이었다. 예외는 `getQuestionnaireSubmit` 하나다. 데모 내원객에게 401회 불렀더니(같은 사람이 겹친 경우 포함) 전부 400 `visitorId NotFound` 였다. 제출된 문진이 데모에 없다. 그래서 **건강 문진의 답이 실제로 어떻게 오는지는 확인하지 못했다**
- 정할 것은 **24개**다(§6)

---

## 1. HAR 인벤토리 — KOS 요청 14건

호스트는 모두 `api.kos-solution.com`, 경로는 모두 `/tenants/{tenantId}/…`, 메서드는 모두 POST 다. 「#」는 HAR `entries` 의 순번(0부터)이다. 13 · 14 · 17 은 Datadog, 16 은 Amplitude 라서 뺐다.

HAR 요청 헤더에는 `Authorization` 이 없다. 내보낼 때 빠진 것으로 보인다(추정). 남은 헤더는 `kos-client-uri` · `origin` · `referer` · Datadog 추적 헤더다. 실호출은 workflow-v2 「인증 · 계정」 방식(Bearer)으로 했고, 200 이 왔다(§5).

「화면 용도」는 HAR 만으로는 알 수 없다. 경로 이름과 본문을 보고 짐작한 것이라 모두 **추정**이다.

| # | 경로 (`/tenants/{tenantId}` 뒤) | 요청 본문 키 | 응답 최상위 (HAR 건수) | 화면 용도(추정) |
|---|---|---|---|---|
| 0 | `/role/v2/queries/get-roles` | (본문 없음) | `data[{id, name, roleTags[int]}]` (15) | 직원 역할 이름 · 태그 |
| 1 | `/schedule/zone/room/v1/queries/get-rooms` | `zoneId` | `data[{id, zoneId, title, order}]` (28) | 구역의 방 목록(A-룸1… · B-트윈… 모양) |
| 2 | `/schedule/default-operation-time/v1/queries/get-default-days-off` | `startDateTime · endDateTime` (그날 KST 0시~24시를 UTC 로) | `data[]` (0) | 병원 기본 휴무일 |
| 3 | `/schedule/default-operation-time/v1/queries/get-default-operation-timetable` | `{}` | `data{monday…sunday{enabled, startTime, endTime, breaktime{startTime,endTime}}}` | 요일별 기본 운영 시간. 캘린더 시간축으로 쓰는 것으로 보인다 |
| 4 | `/schedule/group/v1/queries/get-reservation-group-days-offs` | `reservationGroupIds[13] · startDateTime · endDateTime` | `data[]` (0) | 예약 그룹별 휴무 |
| 5 | `/schedule/occupied-time/v2/queries/get-occupied-times` | `dateTimeRange{startDateTimeUtc, endDateTimeUtc} · deleted:false` | `data[]` (0) | 막아 둔 시간(시간 점유) |
| 6 | `/account/v2/queries/get-accounts-last-update-date-time-utc` | (본문 없음) | `data: "<UTC 시각>"` | 직원 목록이 언제 바뀌었는지(캐시 갱신 판단) |
| 7 | `/account/v2/queries/get-accounts` | `roleTag: "DOCTOR"` | `data[{id, userId, email, name, roleId, activate, createdAt, roleName, realName, updatedDateTimeUtc, mfaMethods[], role{id,name,roleTags[]}}]` (13) | 원장 목록 |
| 8 | `/account/v2/queries/get-accounts` | `roleTag: "COUNSELOR"` | 위와 같은 모양 (22) | 상담사 목록 |
| 9 | `/schedule/group/v1/queries/get-reservation-groups` | `deleted:false · zoneIds[1]` | `data[{id, title, memo, startDate, intervalMinutes, intervalCapacities[{enabled, intervalCapacity, zoneId}], isDefault, sameDayCloseBufferMinutes, operationTimetable{…}, order}]` (13) | **캘린더의 열 = 예약 그룹** |
| 10 | `/schedule/v2/queries/get-schedules-for-reservation` | `baseDateUtc · reservationGroupIds[13] · zoneIds[2]` | `data[일정]` (1) — 모양은 §1.1 | **그날의 예약 카드** |
| 11 | `/schedule/group/v1/queries/get-reservation-group-days-offs` | #4 와 본문까지 같음 | `data[]` (0) | #4 를 다시 부른 것 |
| 12 | `/schedule/v2/queries/get-schedules-for-reservation` | #10 과 본문까지 같음 | #10 과 응답까지 같음(`diff` 로 비교) | #10 을 다시 부른 것 |
| 15 | `/meta/notice/v1/queries/get-notices` | `startDateTimeUtc · endDateTimeUtc · deleted:false` | `data[]` (0). 범위를 넓혀 실호출하니 `data[{id, content, releaseDateTimeUtc, deleted}]` (1) | 공지 |

**합계**: 14행 = HAR 의 KOS 요청 14건. 경로는 11종이다.

### 1.1 `get-schedules-for-reservation` 일정 한 건의 모양 (HAR #10)

`KDA§3.3` 의 공개 일정 모양과 **키가 같다.** HAR #10 의 1건과, 같은 날 공개 `getSchedulesByFlowStep(PROCEDURE)` · `getScheduleDetail` 이 돌려준 같은 일정을 키 단위로 비교했다. 빠진 키도 더 있는 키도 없었다.

```text
data[{ id, flowStep, flowStepUpdatedDateTimeUtc, createdDateTimeUtc, updatedDateTimeUtc, receptionDateTimeUtc, deleted,
  visitor{id, name, phone{countryCode, phoneNumber}, chartNumber, gender, dateOfBirth, nationality, memo,
          visitorType{id,name}, isNew, categories[{id,name,order,color}], snsInfo{snsType, accountId}, phoneticName},
  reservation{reservationGroupId, startDateTime, endDateTime, consultationRequired, sedationRequired,
              counselor{id,name}, doctor{id,name}, funnel{funnelDetail, …}, reservationMemo, zoneId,
              reservationAssignee{id,name}, status, requestedProcedures[], connectedChannel},
  consultation{counselor, doctor, consultationMemo}, consultations[],
  tasks[{type, sequence, title, status, paymentRequired, room{id,zoneId,title,order}, roomAssignedDateTimeUtc, …}],
  purchaseIds[], purchases[](deprecated), prescriptionIds[], etceteraWorks[], taskTimers[], reactions[],
  zone{id,title}, visitorLocation{zoneId}, orderMemo,
  occupiedResources[{id, type, reservationTime{startDateTimeUtc,endDateTimeUtc}, reservationGroup{reservationGroupId, zoneId, doctors[]}}] }]
```

스펙과 실제 응답이 다른 곳이 두 군데 있다.
- 스펙 `protos.schedule.OccupiedResource` 에는 `type · id · reservationTime` 만 있다. 그런데 실제 공개 응답에는 **`reservationGroup{reservationGroupId, zoneId, doctors}` 가 붙어 온다(확인).** 문서에 없는 필드다
- 스펙 `ScheduleDetailReservationContract` 는 `reservationGroupId` · `zoneId` · `doctor` 를 **Deprecated** 로 표시한다. 08-25 일정 34건에서는 `reservation.reservationGroupId` 와 `occupiedResources[0].reservationGroup.reservationGroupId` 가 모두 같았다(확인)
- 스펙에만 있고 응답에 없던 키도 있다: `receptionNumber`(접수 번호) · `visitorRequest`(내원객 요청사항) · `reservation.desiredDischargeDateTimeUtc`(귀가 희망 일시). 데모 응답에는 없거나 null 이었다

---

## 2. 내부 API ↔ 공개 API 짝

| 내부 (HAR #) | 공개 짝 | 차이 |
|---|---|---|
| `get-schedules-for-reservation` (#10 · #12) | **`getSchedulesByFlowStep`** (`/schedule/open/v1/queries/get-schedules-by-flow-step`) · 보조로 `getScheduleDetail` · `getScheduleStatistics` | ① 요청 방식. 내부는 날짜 하루 + 그룹 · 구역 필터로 **한 번**에 받는다. 공개는 **flowStep 이 필수**라서 8번 불러야 하고, 그룹 · 구역 필터가 없다(스펙 `GetSchedulesByFlowStepQuery` = `flowStep · reservationStartDateTimeUtcFrom · …To`). ② 결과. 08-25 하루로 비교하니 공개 합집합 · 내부 · 통계 모두 34건이고 id 집합이 같았다(확인). 취소 · 노쇼 건도 양쪽에 다 나온다(§3.1 상태). ③ 일정 한 건의 모양은 같다(§1.1). ④ `getScheduleStatistics` 는 날짜 범위로 **한 번**에 받는다. 대신 모양이 평평하다: `reservationGroupTitle` · `zoneTitle` · `reservationStatus` · `isFirstProcedureSchedule` · `visitorGender` · `visitorNationality` · `optionItemTotalPriceV2` · `paymentTotalAmountV2` 등. **flowStep · 이름 · 발음 · 차트 외 visitor 필드는 없다.** `visitorChartNumber` 는 있다 |
| `get-reservation-groups` (#9) | **`getReservationGroups`** | 응답 키가 같다(확인. 13건, id 집합도 같다). 내부는 `zoneIds · deleted` 로 거를 수 있고, 공개는 필터가 없다. 공개 스펙에는 `reservationPolicy` 가 더 있다 |
| `get-accounts` (#7 · #8) | **`getAccounts`** (`/account/open/v1/queries/get-accounts`) | 공개 필드는 `id · name · email · roleTags[문자열] · activate` 다. 내부에는 `userId · roleId · roleName · realName · createdAt · updatedDateTimeUtc · mfaMethods · role{}` 가 더 있다. 둘 다 `roleTag` 로 거를 수 있다(스펙 `roleTag · activate`). 데모 공개 79건(10-20 에는 77건) |
| `get-accounts-last-update-date-time-utc` (#6) | 공개 API 없음 | — |
| `get-roles` (#0) | 공개 API 없음 | 공개는 `getAccounts.roleTags`(태그 문자열)뿐이다. 역할 **이름**(「상담실장」 등)은 없다 |
| `get-rooms` (#1) | 공개 API 없음 | `KDA§2.1` 과 같다. 방은 일정의 `tasks[].room` 으로만 나온다 |
| `get-default-operation-timetable` (#3) | 공개 API 없음 | 같은 모양의 `operationTimetable` 이 공개 `getReservationGroups.data[].operationTimetable`(그룹별)에 있다. 병원 기본값 그 자체는 아니다 |
| `get-default-days-off` (#2) | 공개 API 없음 | — |
| `get-reservation-group-days-offs` (#4 · #11) | 공개 API 없음 | — |
| `get-occupied-times` (#5) | 공개 API 없음(조회) | 공개에는 쓰기 `createOccupiedTime` 만 있다. 슬롯 조회(`getReservationSlotsByGroupsV2` 등)는 「남은 자리」를 주는 것이라 다른 정보다 |
| `get-notices` (#15) | 공개 API 없음 | 스펙 75개 중 notice 를 포함한 작업은 0개다(grep) |

---

## 3. 시안 필드 대조표

칸 설명
- **공개**: 공개 API 작업 · 필드 경로
- **내부**: HAR 경로(# 번호) · 필드 경로
- **없음**: `KOS 에 없음`
- **모양 차이**: KOS 값과 시안 값의 차이
- 일정 필드 경로는 `getSchedulesByFlowStep` · `getScheduleDetail` · 내부 `get-schedules-for-reservation` 셋에서 같다(§1.1). 표에서는 `일정.` 으로 줄인다

### 3.1 §7.2 예약 현황 — 32행

| # | 시안 필드 (D§7.2) | 공개 | 내부 | 모양 차이 · 메모 |
|---|---|---|---|---|
| 1 | 날짜 · 요일 | — (조회 조건) | — | 화면이 정하는 값이다. KOS 쪽 조건은 그날 KST 0시~24시를 UTC 로 바꾼 범위다. HAR 은 `baseDateUtc = <전날>T15:00Z` 꼴로 보낸다 |
| 2 | 총 예약 수 · 상태별 수 | `getSchedulesByFlowStep` 8회의 건수 · `getScheduleStatistics.totalCount` | #10 `data[]` 건수 | **KOS 에 「건수」 필드는 없다.** 받은 목록을 세야 한다. 시안의 「총」은 취소를 빼는지 정의가 없다(칸 머리 N 은 취소를 뺀다, D§3.1) → Q-3 |
| 3 | 권역 · 권역별 수 | `일정.reservation.reservationGroupId`(Deprecated) · `일정.occupiedResources[].reservationGroup.reservationGroupId`(스펙에 없음, 실제로 옴) → `getReservationGroups.data[].title` · 또는 `getScheduleStatistics.reservationGroupTitle` | #10 `occupiedResources[].reservationGroup.reservationGroupId` → #9 `title` | **권역 = 예약 그룹.** 아래 §3.3. 그룹은 13개이고 시안은 5칸이다 |
| 4 | 예약 시각(30분) | `일정.reservation.startDateTime · endDateTime` (UTC `Z`) · `occupiedResources[].reservationTime` | 같음 | 08-25 일정 34건 모두 30분이었다. 그런데 그룹의 `intervalMinutes` 는 15 · 30 · 60 이 섞여 있다(확인). 시안의 줄은 30분 고정 · 08:00–20:00 이다. KOS 기본 운영 시간은 월요일 10:00–20:00 KST 다(#3, 확인) → Q-5 |
| 5 | 예약 상태 | `일정.flowStep` + `일정.reservation.status` | 같음 | 아래 §3.2. KOS 는 flowStep 8개 + 예약 상태 6개이고, 시안은 7개다 |
| 6 | 고객 이름(영문 여권) | `일정.visitor.name` · 여권 이름은 `getVisitor` / `searchVisitors` 의 `passportSurname · passportGivenNames`(스펙) | `일정.visitor.name` | `name` 은 KOS 에 등록한 그대로다. 08-25 34건: 한글 17 · 그 밖의 문자 17(한자 · 가나로 보인다), **`SURNAME, GIVEN` 모양 0건**. 외국 국적 15명에게 `getVisitor` 를 불렀더니 여권 이름이 있는 사람은 0명이었다(응답에 키 자체가 없었다) → Q-6 |
| 7 | 한글 발음 | `일정.visitor.phoneticName` (스펙 「발음 표기 이름」) | 같음 | 필드는 있다. 데모에서는 08-25 34건 모두, 오늘 1건도 비어 있었다(확인) |
| 8 | 성별 | `일정.visitor.gender` = `MALE · FEMALE · GENDER_UNSPECIFIED` | 같음 | 시안은 ♂/♀ 두 값이다. `GENDER_UNSPECIFIED` 일 때 어떻게 보일지 정의가 없다 → Q-7 |
| 9 | 국적(코드 · 국가명 · 국기) | 코드: `일정.visitor.nationality` (ISO 3166-1 alpha-2, 스펙 설명) | 같음 | 코드만 온다. 데모 값은 `KR · CN · JP`. **국가명 · 국기 그림은 KOS 에 없음** — 코드를 이름 · 국기로 바꾸는 표가 화면 쪽에 있어야 한다 → Q-8 |
| 10 | 초진 · 재진 | `일정.visitor.isNew` (스펙 「신규 내원객 여부」) · `getScheduleStatistics.isFirstProcedureSchedule` | `일정.visitor.isNew` | true/false 두 값이다. 두 필드의 정의 차이는 workflow-v1 1절에서도 아직 미확인이다 |
| 11 | 차트번호 | `일정.visitor.chartNumber` | 같음 | 08-25 34건 모두 채워져 있었다. 시안의 `No.1415` 는 숫자 모양이다. KOS 값의 형식은 지점이 정한다(값은 적지 않음) |
| 12 | 나이 | `일정.visitor.dateOfBirth` → **계산** | 같음 | 나이 필드는 KOS 에 없다. 생년월일은 08-25 34건 중 10건만 채워져 있었다 → Q-9 |
| 13 | 고객 기본 정보 11칸 | 아래 13a–13k | | |
| 13a | 이름 | 6행과 같음 | | |
| 13b | 한글 발음 | 7행과 같음 | | |
| 13c | 성별 | 8행과 같음 | | |
| 13d | 생년월일 | `일정.visitor.dateOfBirth` · `getVisitor.data.dateOfBirth` | 같음 | 12행 참고 |
| 13e | 주민등록번호/여권번호 | **KOS 에 없음** | KOS 에 없음 | 스펙에서 passportNumber · 주민번호를 grep 했지만 없었다. 일정 · 내원객 응답에도 없다 |
| 13f | 국적 | 9행과 같음 | | |
| 13g | 휴대폰 번호 | `일정.visitor.phone{countryCode, phoneNumber}` · `getVisitor.data.phoneNumber` · `additionalPhoneNumber` | `일정.visitor.phone` | 국가번호와 번호가 따로 온다 |
| 13h | 이메일 | 일정 · `getVisitor` 응답에는 **없음.** 문진 1쪽 질문 「이메일」(`getVisitorQuestionnaire`, `INPUT_BOX`)이 있다. 답은 `getQuestionnaireSubmit.data.answers[]`(스펙) | 없음 | 공개 `getAccounts` 의 email 은 직원 것이다. 고객 이메일은 문진 답으로만 들어올 수 있고, 제출된 문진이 데모에 없어 확인하지 못했다 → Q-10 |
| 13i | SNS 종류 | `일정.visitor.snsInfo.snsType` = `etc · kakaotalk · line · instagram · whatsapp · wechat` (스펙) | 같음 | 데모 08-25: kakaotalk 9 · etc 7 · line 7 · wechat 7 · instagram 4 |
| 13j | SNS 아이디 | `일정.visitor.snsInfo.accountId` | 같음 | |
| 13k | 주소 / 주소 (자국) | `getVisitorQuestionnaire.data.address · addressDetail` · `getQuestionnaireSubmit.data.address · addressDetail`(스펙) | 없음 | KOS 주소는 칸 하나(+상세)다. 시안은 국내 「주소」 / 외국인 「주소 (자국)」으로 나눈다. 데모 오늘 1건은 비어 있었다 |
| 14 | 고객 입력 링크 · QR | **KOS 에 없음** | KOS 에 없음 | 문진 양식 조회(`getVisitorQuestionnaire`)와 제출(쓰기 `submitVisitorQuestionnaire`)은 있다. 고객에게 보낼 링크를 만들어 주는 작업은 스펙에 없다 |
| 15 | 신분증 종류 · 확인 상태 · 스캔 기기 · 시각 | **KOS 에 없음** | KOS 에 없음 | 이미지 쓰기(`registerVisitorImages`)는 있다. 조회와 신분 확인 상태는 없다 |
| 16 | 유입 채널 · 상세 | `일정.reservation.funnel{funnel{name,…}, funnelCategory{name,…}, funnelDetail}` · `일정.reservation.connectedChannel` = `GANGNAMUNNI · HOMEPAGE · KOS_CONNECT · Channel_UNSPEICIFED` · `getScheduleStatistics.reservationFunnelName · …CategoryName · …Detail` | `일정.reservation.funnel` · `connectedChannel` | 시안의 선택지 6개(본사 · 홈페이지 · 인스타그램 · 지인 소개 · 에이전시 · 기타)는 **고정 목록**이다. KOS 의 `funnel` 은 지점이 만든 코드(`CodeCategory FUNNEL`)다. 데모 08-25 34건은 `funnel.name` 이 모두 비어 있었고 `connectedChannel` 은 모두 미지정이었다 → Q-11 |
| 17 | 예약 메모 | `일정.reservation.reservationMemo` | 같음 | 원문 그대로 보여 준다(workflow-v1 메모 원칙). 쓰기는 다음 판에서(`changeReservationMemo`) |
| 18 | 건강 문진 7항목 | 질문: `getVisitorQuestionnaire.data.pages[「건강 정보」].questions[]` — **7개가 시안과 같은 이름이다**(질환 · 복용 약물 · 알레르기 · 임신/수유 · 켈로이드 · 신체 내 금속장치 · 지혈 장애, 확인). 답: `getQuestionnaireSubmit.data.answers[{questionTitle, answerTitle, memo}]`(스펙) | 없음 | `getVisitorQuestionnaire` 는 **빈 양식**(질문 + 선택지)이다. 답이 들어 있지 않다(확인). 답 조회 `getQuestionnaireSubmit` 은 데모 401회 호출 모두 400 `NotFound` 였다 → 답의 실제 모양은 **미확인**. 「문제 있는 답」(빨강) 기준도 KOS 에 없다 → Q-12 |
| 19 | 고객 공통 주의사항 | 후보: `일정.visitor.memo` (스펙 「메모」) · `getScheduleStatistics.visitorMemo` | `일정.visitor.memo` | KOS 에 「주의사항」이라는 필드는 없다. 고객 단위 메모는 `visitor.memo` 하나뿐이다. 둘이 같은 것인지는 정해야 한다 → Q-13. 데모 08-25 는 34건 모두 비어 있었다 |
| 20 | 이전 방문(날짜 · 결과 · 예약 시각 · 예약 메모 · 상담 메모 · 시술 내역 · 원장) | `getSchedulesByVisitor(visitorId, 기간)` → `data[].reservation.startDateTime · status · reservationMemo` · `consultation.consultationMemo` · `consultations[].content.text` · `tasks[].title · status · doctors[]` · `zone.title` / `getSchedulesSummarizedByTask(visitorId)` → `data[{scheduleId, startDateTimeUtc, tasks[]}]` | 없음(HAR 에 없다) | 데모 1명: 일정 4건 · 작업 묶음 4건(확인). 결과 「방문 완료 / 노쇼」 = `reservation.status` `COMPLETED / NO_SHOW` 이고 이름이 다르다. **오늘 일정도 함께 온다** — 「이전」만 남기려면 오늘을 빼야 한다. 시안의 「4층 / {권역}」 = `zone.title` / 그룹 title |
| 21 | 배정 방 · 접수 시각 · 접수 직원 | 방: `일정.tasks[type=ETCETERA, title「방 배정」].room.title` · `roomAssignedDateTimeUtc`. 접수 시각: `일정.receptionDateTimeUtc`. 접수 직원: **KOS 에 없음** | 같음 + 방 목록 #1 | 방은 일정 단위가 아니다. **작업마다** `room` 이 있다(오늘 1건은 작업 4개가 모두 같은 방이었다). `reservation.reservationAssignee` 는 「예약 담당자」라서 접수 직원이 아니다 |
| 22 | 상담사 · 상담 상태 · 시각 · 상담사의 현재 상태 | 상담사: `일정.reservation.counselor`(희망 상담사) · `일정.consultation.counselor` · `일정.consultations[].counselors[]`. 상태: `flowStep` `CONSULTATION_WAITING · CONSULTATION`. 시각: `consultations[].consultationStartedDateTimeUtc` · `flowStepUpdatedDateTimeUtc`. 상담사 목록: `getAccounts(roleTag=COUNSELOR)` | 상담사 목록: #8 | 「상담사의 지금 상태」(A-룸2 상담 중)는 **KOS 에 없음.** 다른 일정을 모아 보면 알 수 있겠지만 그건 계산이다 → Q-14 |
| 23 | 시술 단계 · 시각 | `일정.flowStep` (`PROCEDURE_WAITING · PROCEDURE · PROCEDURE_DONE`) · `flowStepUpdatedDateTimeUtc` · `tasks[].status · readyDateTimeUtc · completedDateTimeUtc` | 같음 | 시안의 단계는 「시술 대기 / 진행 중 / 완료」 · 「귀가 대기 / 귀가」다. flowStep 과 한 줄씩 맞는다. 시각은 flowStep 이 바뀐 시각 하나뿐이다. 단계마다 언제 시작했는지는 없다 |
| 24 | 전체 금액 · 결제 금액 · 후납 금액 | `getScheduleStatistics.optionItemTotalPriceV2{value,currency}` · `paymentTotalAmountV2{value,currency}` / `일정.purchaseIds` → `getPurchaseSummaries.data[].items[].price · transactions[].price · status` | `일정.purchaseIds` | 「전체」 · 「결제」에 가까운 이름의 필드는 통계에 있다. 08-01~10-26 의 500건 중 18건에 값이 있었다(확인). 두 필드가 시안의 「전체 · 결제」와 같은 뜻인지는 문서에 없다. **「후납」은 KOS 에 없음** → Q-15 |
| 25 | 처방전 유무 · 내용 | 유무: `일정.prescriptionIds[]` · 내용: **KOS 에 없음(공개)** | `prescriptionIds[]` | 처방전을 조회하는 공개 작업은 없다. 데모 08-25 는 34건 모두 비어 있었다 |
| 26 | 여정 리포트 언어 · 전송 상태 | **KOS 에 없음** | KOS 에 없음 | 언어 후보로 문진 「사용 가능한 언어」 질문은 있다(확인). 답은 미확인 |
| 27 | 진행 경로(상담 필요 / 바로 시술) | `일정.reservation.consultationRequired` (bool) | 같음 | 시안은 2값, KOS 도 bool 이다. 데모 08-25 는 34건 모두 false 였다 |
| 28 | 방 목록 · 사용 여부 · 사용자 | 목록: **공개 API 없음** | 목록: #1 `get-rooms` `data[{title, order}]` (28, 모두 order 0) | 「사용 중 · 쓰는 사람」 필드는 KOS 에 없음. 그날 일정들의 `tasks[].room` 을 모아 계산해야 한다 → Q-16. 시안은 「A구역 A-룸1~10」이다. 데모 방 이름은 A-룸1~9 · A-레이저실 · A-트윈 · B-룸 등 28개다 |
| 29 | 공지 본문 | **공개 API 없음** | #15 `get-notices` `data[{id, content, releaseDateTimeUtc, deleted}]` | 오늘 범위에서는 0건이었다. 2026 년 전체로 넓히니 1건이 나왔다(확인). KOS 공지는 게시 시각이 있는 **목록**이다. 시안은 Textarea **하나**다 → Q-17 |
| 30 | 예약 요청(이름 · 발음 · 국적 · 희망 일시 · 권역 · 수신 시각 · 상태 · 처리 시각 · 반려 사유 · 원문) | **KOS 에 없음** | KOS 에 없음 | 「본사 메시지」 · 승인/반려를 담는 객체가 없다. 비슷한 KOS 필드는 `connectedChannel`(외부 채널 이름)과 `visitorRequest`(요청사항 문자열, 스펙. 데모 응답에는 없었다) 정도다 → Q-18 |
| 31 | 요청 원문 파싱 필드 | **KOS 에 없음** | KOS 에 없음 | 30행과 같다 |
| 32 | 원내 현황 카드 상태 · 금액 | 상태: `flowStep` · 수납 필요는 `일정.tasks[].paymentRequired` · 금액: 24행 | 같음 | §3.4 |

### 3.2 범례 상태 7개 (D§3.2)

KOS 값은 두 개다. `일정.flowStep` 8개(+`FLOW_STATUS_UNSPECIFIED`)와 `일정.reservation.status` 6개(`RESERVED · CANCELED · NO_SHOW · IN_PROGRESS · COMPLETED` + `UNSPECIFIED`)다(스펙 enum).

**취소 · 노쇼 일정은 flowStep 이 `RESERVED` 그대로이고, 예약 상태만 바뀐다**(확인: CANCELED 3건 · NO_SHOW 1건의 `getScheduleDetail`. `deleted` 는 false). 이 일정들은 `getSchedulesByFlowStep(RESERVED)` 에도, 내부 #10 에도 나온다(확인).

| # | 시안 상태 | KOS 원천 | 모양 차이 |
|---|---|---|---|
| S1 | 예약 | `flowStep=RESERVED` 이고 `reservation.status=RESERVED` | 취소 · 노쇼도 flowStep 이 RESERVED 라서, 예약 상태를 같이 봐야 구분된다 |
| S2 | 접수 | `flowStep=RECEPTION` | 짝은 하나다 |
| S3 | 상담(「상담 중」) | `flowStep=CONSULTATION` | **`CONSULTATION_WAITING`(상담 대기)이 들어갈 칸이 시안에 없다.** 08-25 에 1건 있었다 → Q-1 |
| S4 | 진행(「시술 중」) | `flowStep=PROCEDURE` | **`PROCEDURE_WAITING`(시술 대기)이 들어갈 칸이 시안에 없다** → Q-1 |
| S5 | 귀가 대기 | `flowStep=PROCEDURE_DONE` | 짝은 하나다(workflow-v1 표의 이름과 같다) |
| S6 | 귀가 | `flowStep=COMPLETED` (예약 상태 `COMPLETED`) | 짝은 하나다 |
| S7 | 취소 | `reservation.status=CANCELED` | **`NO_SHOW`(노쇼)가 들어갈 칸이 시안에 없다.** 이전 방문 Badge 에는 「노쇼」가 있다 → Q-2 |

남는 KOS 값: `CONSULTATION_WAITING` · `PROCEDURE_WAITING` · `NO_SHOW` · `FLOW_STATUS_UNSPECIFIED` · `RESERVATION_STATUS_UNSPECIFIED`.

### 3.3 권역 5칸 (D§3.1 `BK_TRACKS`)

원천: 일정의 예약 그룹 id(§3.1 3행) → `getReservationGroups.data[].title`(공개) / #9 `title`(내부). 데모 그룹 13개(확인):

| # | 시안 칸 | 같은 이름의 KOS 예약 그룹 | 메모 |
|---|---|---|---|
| R1 | 국내 | 「국내」 (`isDefault: true`, order 1) | |
| R2 | 중화권 | 「중화권」 (order 2) | |
| R3 | 영미권 | 「영미권」 (order 3) | |
| R4 | 일본 | 「일본」 (order 4) | |
| R5 | 기타 | 「기타」 (order 5) | |

- **5칸에 들어가지 않는 그룹이 8개 있다**: 리프팅 · 레이저 · 필러 · 스킨부스터 · 보톡스 · 후관리 · 수액/체형 · 제모(order 6~13). 이 그룹들은 국적이 아니라 시술로 나뉜다. 08-25 일정 34건의 그룹: 중화권 7 · 기타 4 · 국내 1 · **시술 그룹 22**(후관리 6 · 스킨부스터 6 · 필러 3 · 리프팅 2 · 제모 2 · 수액/체형 2 · 레이저 1) → Q-4
- 지난 일정의 통계 `reservationGroupTitle` 에는 지금 목록에 없는 그룹 이름도 나온다. 08-01~10-26 의 500건에 「상담/중화권 · 통역 · 인모드 · 상담/국내 · 홈페이지 예약 · 써마지 · 중국 · 영어권 …」 등 29종이 있었다(확인). 그룹이 바뀌어 온 흔적으로 보인다(추정). 지난날을 볼 때 칸을 어떻게 정할지도 Q-4 에 포함했다
- 일정 하나가 그룹 여러 개를 차지할 수 있다(`occupiedResources[]` 가 배열이다). 통계 500건 중 5건이 그룹 2개 이상을 가졌다(확인) → Q-4
- 「국적 → 권역」 계산은 하지 않았다(브리프). 국적 코드는 9행에 있다
- 칸 머리의 「N건」 = 그 그룹 id 를 가진 일정 수를 세는 것이다. 취소를 빼는 규칙은 화면이 정한다(D§3.1)

### 3.4 「원내 현황」 탭 카드 (D§3.3 ④)

| # | 시안 | 공개 | 내부 | 모양 차이 |
|---|---|---|---|---|
| C1 | 필터 칸(전체 · 귀가 대기 · 시술 중 · 상담 중 · 접수 완료) | `flowStep` 으로 거른다(§3.2) | 같음 | 시안 원문에는 「6칸」이라고 적혀 있는데 이름은 5개뿐이다(D§3.3). 대기 단계 2개(상담 대기 · 시술 대기)가 들어갈 칸이 없다 → Q-1 |
| C2 | 카드 이름 · 한글 발음 · 국기 | 6 · 7 · 9행과 같음 | 같음 | |
| C3 | Badge(수납 필요 / 귀가 대기 / 시술 중 · 상담 중 / 접수 완료) | 단계: `flowStep`. 수납 필요: `일정.tasks[].paymentRequired`(작업 단위 bool) | 같음 | 「수납 필요」 필드는 **작업마다** 있다. 일정 하나에 대한 값은 없다(오늘 1건: 작업 4개 중 3개가 true). 단계 Badge 와 수납 Badge 중 무엇을 먼저 보일지 → Q-15 |
| C4 | 금액 3칸(전체 · 결제 · 후납) | 24행과 같음 | `purchaseIds` | 후납 없음 → Q-15 |

### 3.5 공지 (브리프 추가 행)

| # | 시안 | 공개 | 내부 | 모양 차이 |
|---|---|---|---|---|
| N1 | 「공지사항」 본문 · [수정하기/저장] | 공개 API 없음 | 조회: #15 `get-notices{startDateTimeUtc, endDateTimeUtc, deleted}` → `data[{id, content, releaseDateTimeUtc, deleted}]`. 저장(쓰기)은 HAR 에 없다 | 29행과 같다. 날짜 범위로 조회하는 게시 목록이다. 저장은 다음 판 · Q-17 |

---

## 4. 시술 현황과 겹치는 것

예약 현황 카드와 상세에 필요한 일정 · 작업 필드는 시술 현황이 이미 쓰는 내부 `get-schedules-grouped-by-zone`(workflow-v2 「KOS 반영 표」, D-08)과 겹친다. 이 작업은 이번 HAR 에 **없다.** 같은 모양인지는 비교하지 않았다. 방 목록 `get-rooms` 와 직원 `getAccounts` 는 시술 현황에서 이미 쓰고 있다(같은 표).

---

## 5. 데모 실호출 (2026-10-26)

- 데모 테넌트에서만 불렀다. 공개 = `ax-clinic-project/scripts/.env` 의 `KOS_API_tenent_dev` → `https://open-api.kos-solution.com` `exchange-token` → `Authorization: <token>`. 내부 = procedure `.env` 의 시스템 계정 → `/common/v1/user/commands/sign-in` → `Authorization: Bearer <token>`
- 운영 키 `KOS_API_tenent` 는 쓰지 않았다(값이 다른 것을 비교만 했다). 쓰기 호출은 0건이다. 스크립트가 경로에 `/queries/` 가 없으면 멈추게 했다. 예외는 토큰 교환과 sign-in 두 개다
- 「오늘」 = 2026-10-25T15:00Z ~ 2026-10-26T15:00Z. 오늘은 데모에 일정이 **1건**(flowStep `PROCEDURE`)뿐이었다. 그래서 상태 · 권역 · 채움 비율은 일정이 34건 있던 **2026-08-25** 로 한 번 더 봤다(표에 「08-25」로 적었다)

### 5.1 공개 API

| 작업 | 경로 | 결과 | 건수 | 확인한 필드 |
|---|---|---|---|---|
| `exchangeToken` | `/open/authorization/commands/exchange-token` | 200 ×5 | — | `token` |
| `getSchedulesByFlowStep` ×8 (오늘) | `/schedule/open/v1/queries/get-schedules-by-flow-step` | 200 ×8 | PROCEDURE 1 · 나머지 7개 단계 0 | §1.1 의 키 전부. `occupiedResources[].reservationGroup` 이 응답에 있다 |
| `getSchedulesByFlowStep` ×9 (08-25) | 같음 | 200 ×9 | 8개 단계 합집합 34. 따로 부른 RESERVED 1회에 노쇼 1건이 들어 있었다 | 내부 #10 과 id 집합이 같다 |
| `getScheduleStatistics` | `/statistics/open/v1/queries/get-schedule-statistics` | 200 ×4 | 오늘 1 · 08-25 34 · 08-01~10-26 500(`totalCount` 1117) · 같은 기간 CANCELED+NO_SHOW 48 | `reservationGroupTitle` · `reservationGroupOccupiedResources[]` · `isFirstProcedureSchedule` · `reservationStatus` · `optionItemTotalPriceV2` · `paymentTotalAmountV2` |
| `getScheduleDetail` | `/schedule/open/v1/queries/get-schedule-detail` | 200 ×5 | 오늘 1 · 노쇼 1 · 취소 3 | 취소 · 노쇼 모두 `flowStep=RESERVED` · `deleted=false` |
| `getReservationGroups` | `/schedule/open/v1/queries/get-reservation-groups` | 200 | 13 | `title · order · isDefault · intervalMinutes(15/30/60)` · 내부 #9 와 키 · id 가 같다 |
| `getZones` | `/schedule/open/zone/v1/queries/get-zones` | 200 | 2 | (10-20 과 같다) |
| `getAccounts` | `/account/open/v1/queries/get-accounts` | 200 | 79 | `id · name · email · roleTags · activate` |
| `getVisitor` | `/visitor/open/v1/queries/get-visitor` | 200 ×16 | 오늘 1명 + 외국 국적 15명 | 응답 키 `id · chartNumber · name · phoneNumber · dateOfBirth · gender · nationality`. `passportSurname/GivenNames` 는 16명 모두 응답에 없었다 |
| `getVisitorQuestionnaire` | `/visitor/open/v1/queries/get-visitor-questionnaire` | 200 | 최상위 객체(`data` 로 감싸지 않음) · pages 4 | 「건강 정보」 질문 7개가 시안과 같다. 답 값은 없다(빈 양식) |
| `getQuestionnaireSubmit` | `/visitor/open/v1/queries/get-questionnaire-submit` | **400 ×401** | — | 모두 `{"className":"InvalidRequestException","errorProperties":[{"key":"visitorId","reason":"NotFound"}]}`. 데모에 제출된 문진이 없다 |
| `getSchedulesByVisitor` | `/schedule/open/v1/queries/get-schedules-by-visitor` | 200 | 4 | 오늘 일정이 들어 있다 · `reservation.status` · `consultations[]` |
| `getSchedulesSummarizedByTask` | `/schedule/open/v1/queries/get-schedules-summarized-by-tasks` | 200 | 4 | `scheduleId · startDateTimeUtc · endDateTimeUtc · tasks[]` |
| `getPurchaseSummaries` | — | 부르지 않음 | — | 오늘 일정에 `purchaseIds` 가 없었다. 모양은 `KDA§3.4` 에 있다 |

공개 호출 수: 토큰 5 + 조회 449 = **454회**(그중 401회가 문진 제출 조회). 호출 한도는 IP 당 1분에 3,000회다(스펙 `info.description` 「호출 한도」).

### 5.2 내부 API (HAR 의 11종 전부, HAR 본문 그대로)

| HAR # | 경로 | 결과 | 건수 | 확인한 필드 |
|---|---|---|---|---|
| — | `/common/v1/user/commands/sign-in` | 200 ×2 | — | `data.token` |
| 0 | `/role/v2/queries/get-roles` | 200 | 15 | HAR 과 같은 모양 |
| 1 | `/schedule/zone/room/v1/queries/get-rooms` | 200 | 28 | `title · order` |
| 2 | `/schedule/default-operation-time/v1/queries/get-default-days-off` | 200 | 0 | |
| 3 | `/schedule/default-operation-time/v1/queries/get-default-operation-timetable` | 200 | 객체 | 월요일 `startTime/endTime` = 01:00Z/11:00Z (= 10:00–20:00 KST), 쉬는 시간 빈칸 |
| 4 (=11) | `/schedule/group/v1/queries/get-reservation-group-days-offs` | 200 | 0 | |
| 5 | `/schedule/occupied-time/v2/queries/get-occupied-times` | 200 | 0 | |
| 6 | `/account/v2/queries/get-accounts-last-update-date-time-utc` | 200 | 문자열 | |
| 7 | `/account/v2/queries/get-accounts` (DOCTOR) | 200 | 13 | §2 의 내부 필드 |
| 8 | `/account/v2/queries/get-accounts` (COUNSELOR) | 200 | 22 | |
| 9 | `/schedule/group/v1/queries/get-reservation-groups` | 200 | 13 | |
| 10 (=12) | `/schedule/v2/queries/get-schedules-for-reservation` | 200 ×2 | 오늘 1 · 08-25 34 | 08-25 의 34건: (flowStep, 예약 상태) = (CONSULTATION, IN_PROGRESS) 22 · (RECEPTION, IN_PROGRESS) 6 · (COMPLETED, COMPLETED) 4 · (RESERVED, NO_SHOW) 1 · (CONSULTATION_WAITING, IN_PROGRESS) 1 |
| 15 | `/meta/notice/v1/queries/get-notices` | 200 ×2 | 오늘 0 · 2026 년 전체 1 | `id · content · releaseDateTimeUtc · deleted` |

내부 호출 수: sign-in 2 + 조회 14 = **16회**. 모두 200 이다.

---

## 6. 정할 것 (결정하지 않음) — 24개

| # | 자리 | 왜 정해야 하나 | 근거 |
|---|---|---|---|
| Q-1 | 상태 칸에 없는 대기 단계 두 개: `CONSULTATION_WAITING` · `PROCEDURE_WAITING` | 시안 상태는 7개, KOS flowStep 은 8개다. 「상담 중」 · 「시술 중」에 합칠지, 「접수」에 둘지, 칸을 새로 만들지. 원내 현황 탭 필터(C1)도 같은 문제다 | §3.2 S3 · S4 · §3.4 C1 |
| Q-2 | 노쇼(`NO_SHOW`) | 시안 범례에 칸이 없다. 이전 방문 Badge 에는 「노쇼」가 있다 | §3.2 S7 |
| Q-3 | 「총 예약 N건」에 취소 · 노쇼를 넣는지 | 칸 머리 N 은 취소를 뺀다. 총 수의 규칙은 시안에 없다 | §3.1 2행 |
| Q-4 | 권역 칸 ↔ 예약 그룹 | 그룹 13개 중 5개만 시안 칸 이름과 같다. 시술 그룹 8개를 어디에 둘지 정해야 한다(08-25 에는 34건 중 22건). 지난날의 옛 그룹 이름, 그룹을 2개 이상 가진 일정도 같이 정한다. 칸을 KOS 그룹 목록(order 순)으로 그대로 쓸지도 포함한다 | §3.3 |
| Q-5 | 시간축 · 칸 간격 | 시안은 08:00–20:00 · 30분 고정이다. KOS 기본 운영 시간은 10:00–20:00 이고, 그룹 간격은 15/30/60분이다. 휴무(#2 · #4) · 시간 점유(#5)를 화면에 보일지도 정한다 | §3.1 4행 · §5.2 #3 |
| Q-6 | 카드 이름의 원천 | 시안은 영문 여권 이름 「SURNAME, GIVEN」이다. KOS `visitor.name` 은 등록한 그대로(한글 · 한자 등)다. 여권 이름 필드(`getVisitor.passport*`)는 데모에서 비어 있었고, 받으려면 고객마다 한 번씩 불러야 한다 | §3.1 6행 |
| Q-7 | `GENDER_UNSPECIFIED` 일 때 아이콘 | 시안에는 ♂/♀ 만 있다 | §3.1 8행 |
| Q-8 | 국가명 · 국기 | KOS 는 ISO 코드만 준다. 이름 · 국기 표를 어디에 둘지 | §3.1 9행 |
| Q-9 | 나이 | KOS 에는 생년월일만 있고, 그것도 자주 비어 있다(08-25 34건 중 10건만 있음). 생년월일이 없으면 무엇을 보일지 | §3.1 12행 |
| Q-10 | 고객 이메일 · 주소의 원천 | 일정과 내원객 응답에는 없다. 문진 제출 답으로만 들어올 수 있다. 데모에 제출 건이 없어 확인하지 못했다. 데모에 문진을 제출해서 확인할지(쓰기라 이번 판 밖이다) | §3.1 13h · 13k |
| Q-11 | 유입 채널 선택지 | 시안의 고정 6개와 KOS 지점 코드(`funnel`) · `connectedChannel` 4값이 다르다. 데모에는 값이 없었다 | §3.1 16행 |
| Q-12 | 건강 문진 답의 모양 · 「확인 필요」 기준 | 질문 7개는 KOS 양식과 같다. 답(`getQuestionnaireSubmit`)은 미확인이다. 무엇이 「문제 있는 답」인지 KOS 는 정하지 않는다 | §3.1 18행 · §5.1 |
| Q-13 | 「주의사항」 = `visitor.memo` 인가 | KOS 에 「주의사항」 필드는 없다. 고객 단위 메모는 하나뿐이다 | §3.1 19행 |
| Q-14 | 상담사의 「지금 상태」 · 접수 직원 | KOS 에 없다. 다른 일정을 모아 계산할지, ccc 가 따로 가질지, 빼둘지 | §3.1 21 · 22행 |
| Q-15 | 금액 · 수납 필요 | 「전체 · 결제」에 가까운 통계 필드(`optionItemTotalPriceV2` · `paymentTotalAmountV2`)가 같은 뜻인지 KOS 에 확인할지, 수납 원장(`getPurchaseSummaries`)에서 셀지. 「후납」은 KOS 에 없다. 작업 단위 `paymentRequired` 를 일정 단위로 어떻게 묶을지 | §3.1 24행 · §3.4 C3 · C4 |
| Q-16 | 시술실 배정 팝오버의 방 · 사용 여부 | 방 목록은 내부 `get-rooms` 에만 있다. 사용 중인지는 KOS 에 없어서 그날 일정의 `tasks[].room` 으로 계산해야 한다. 시안 「A-룸1~10」과 데모 방 28개의 이름이 다르다(디자인 Q-19 와 이어짐) | §3.1 28행 |
| Q-17 | 공지 | 공개 API 가 없어서 내부 API 를 써야 한다. KOS 공지는 게시 시각이 있는 목록이고, 시안은 Textarea 하나다. 어느 공지를 보일지(오늘 범위? 최신 1건?) · 수정은 KOS 로 갈지 ccc 에 둘지 | §3.1 29행 · §3.5 |
| Q-18 | 예약 요청(본사) 패널 | KOS 에 해당하는 객체가 없다. 원천을 어디로 할지(디자인 Q-17 과 같다) | §3.1 30 · 31행 |
| Q-19 | 고객 입력 링크 · QR · 신분 확인 · 여권번호/주민번호 · 여정 리포트 · 처방전 내용 | 모두 KOS 조회에 없다. ccc 가 따로 가질지, 이번 판에서 뺄지 | §3.1 13e · 14 · 15 · 25 · 26행 |
| Q-20 | 하루 일정을 공개로 받을지 내부로 받을지 | 공개는 flowStep 마다 8번, 그룹 · 구역 필터 없음, 「예약 그룹 id」 필드는 Deprecated 이거나 스펙 밖이다. 내부는 1번이지만 공식 계약이 아니다. 통계 API 는 1번이지만 flowStep · 고객 필드가 모자란다. 시술 현황이 쓰는 `get-schedules-grouped-by-zone` 과 합칠지도 포함한다 | §2 · §1.1 · §4 |
| Q-21 | 예약 그룹 id 를 어느 필드에서 읽을지 | `reservation.reservationGroupId` 는 스펙상 Deprecated 이고, `occupiedResources[].reservationGroup` 은 스펙에 없다. 둘 다 지금은 값이 온다 | §1.1 |
| Q-22 | 구역(층) 범위 | HAR 은 그룹을 한 구역으로 거르고, 일정은 두 구역으로 거른다. 08-25 일정은 구역 2개에 20 · 14 로 나뉘었다. 화면이 「4층」 하나만 볼지 | §1 #9 · #10 · §5.1 |
| Q-23 | 이전 방문에서 오늘 일정 빼기 · 결과 이름 | `getSchedulesByVisitor` 는 오늘 일정도 준다. 시안 「방문 완료 / 노쇼」 ↔ KOS `COMPLETED / NO_SHOW`, 그 밖의 상태(`IN_PROGRESS` 로 남은 지난 일정 — 데모 1명에 2건 있었다)를 어떻게 보일지 | §3.1 20행 |
| Q-24 | HAR 요청 수 | 브리프에는 15건이라고 되어 있는데 실제 KOS 요청은 14건이다. HAR 을 다시 뜰 필요가 있는지 | §0 · §1 |

---

## 7. 빠진 행 점검

- HAR: KOS 요청 14건 = §1 인벤토리 14행. 경로 11종 = §2 짝 표 11행. Datadog 3 · Amplitude 1 은 뺐다
- 시안 §7.2: **32행** = §3.1 의 1~32행. 13행은 「고객 기본 정보」 11칸을 13a~13k 로 나눴다
- 브리프가 더한 것: 범례 상태 7행(§3.2 S1~S7) · 권역 5행(§3.3 R1~R5) · 원내 현황 탭 카드 4행(§3.4 C1~C4) · 공지 1행(§3.5 N1)
- 대조표 합계: 32 + 7 + 5 + 4 + 1 = **49행**(13a~k 를 따로 세면 60행). 빠진 행은 없다
- 정할 것: 24개(§6)
- 보지 않은 것: §7.1(헤더) · §7.3(시술 현황) · §7.4(원내 현황 평면도)는 이번 범위 밖이라 대조하지 않았다. `getPurchaseSummaries` 는 오늘 수납 id 가 없어서 부르지 않았다
