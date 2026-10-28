# WORK-007 WP-KOS 결과 보고 — 예약 현황 KOS 데모 실호출 확인

## 상태: done

- 시험일: 2026-10-26 (KST) 20:13 ~ 20:19(호출 시각) · backend 워커 (task_25be3dc3526c) · **코드 변경 0 · 커밋 0**
- 기준: WORK-007 WP-KOS 행(K1 ~ K10) · SPEC-005(r1 검수 중 본문) §3.3 · §4.2 · §5.6 · §8 「미확인」 줄 · §10 OQ-728 · OQ-739 · OQ-753 ~ OQ-756. SPEC 문구가 아니라 **KOS 가 실제로 무엇을 받는지**를 적었다
- 테넌트 확인(스크립트 `assert` · 매 실행 처음): procedure `.env` 테넌트 = 앞 판 데모 HAR(`예약.har`)의 유일한 테넌트 · 공개 키 = `KOS_API_tenent_dev` · 공개 키 ≠ 운영 키 `KOS_API_tenent`. **운영 키 사용 0건**
- 방법: scratchpad 일회성 스크립트(back `KosClient` 를 import · 토큰은 별도 scratch DB) — 코드 레포에 남긴 파일 0. 사용자 스택(3700 · 8700)과 사용자 프로세스는 건드리지 않았다
- 쓰기 가드: 허가 경로 목록 밖 command 를 막았다. 쓰기 키마다 **1회만** 보냈다(두 번째 실행은 막힘 — 실제로 한 번 막혔고, 그때 다시 나간 쓰기는 0). 실패한 쓰기 1건(K9b)은 **다시 보내지 않았다**
- 원본 응답은 scratchpad 에만 있다. 이 리포트에는 KOS id · 키 · 토큰 · 실명 · 실제 고객 값을 적지 않았다. 시험 고객의 값은 **지어낸 값**이다
- 표기: 「같음 / 다름」 = SPEC-005 와 비교한 결과 · **확인** = 이번에 데모로 보낸 것 · 본 것

---

## 0. 판정 (한 줄씩)

| 항목 | 판정 | 한 줄 |
|---|---|---|
| 신규 생성 (`find-duplicated-visitor` → `create-visitor`) | **받음** | 동의 플래그 없이 200 `{data:{id}}`. KOS 기본값으로 저장됨: 개인정보 · 광고 동의 = false, **정보성 알림 동의 = true** (OQ-753) |
| 전 칸 예약 (`reserve`) | **받음** | `doctors` · `counselor` · `funnel` · `reservationMemo` · `sedationRequired` · `consultationRequired` · `desiredDischargeDateTimeUtc` 7칸 모두 일정 상세에 그대로 보였다 |
| 내부 이동 (`update-reservation` `items`) | **받음** | 묶음 id · 지정 의사 · 메모 · 유입 · 상담사 · 수면 · 상담 필요 · 귀가 희망 모두 남았다. 바뀐 칸은 시각 · 그룹뿐이다 |
| 진행 경로 (`update-reservation{consultationRequired}` 단독) | **받음** | `consultationRequired` 만 바뀌었고 다른 칸은 남았다 (OQ-755) |
| 상담사 (`update-reservation{counselor}` 단독) | **받음** | `counselor` 만 바뀌었고 다른 칸은 남았다 (OQ-755) |
| 메모 (공개 `change-reservation-memo`) | **받음** | `reservationMemo` 가 보낸 값으로 통째로 바뀌었다. 다른 칸은 그대로다 |
| 고객 수정 (`update-visitor-personal-information`) | **받음** | `dateOfBirth` = `yyyy-MM-dd 00:00:00.000Z`, `passportExpiryDate` = `yyyy-MM-dd` 둘 다 받았고, 같은 꼴로 다시 읽혔다. 시스템 계정 권한으로 됐다. 고치지 않은 칸은 남았다 (OQ-739) |
| 바로 시술 (접수 묶음 끝 단계 `PROCEDURE_WAITING`) | **받음** — 읽는 쪽 주의 1 | 4단계가 모두 200 이었다. 주의: 「방 없음」 작업은 `room` 키가 **없는 게 아니라 `room:{id:"", title:"", …}`(빈 값 객체)** 로 온다 → 「방 없음」 판정은 `room.id` 가 빈 값인지로 해야 한다 (OQ-756) |
| 귀가 (공개 `changeFlowStep(COMPLETED)`) | **받음** | `PROCEDURE_DONE` → `COMPLETED` 200. `reservation.status` 도 `COMPLETED` 가 됐다 (OQ-728) |
| 귀가 거절 (수납 필요 작업이 남은 일정) | **KOS 가 거절함** | 공개 `changeFlowStep(COMPLETED)` → **HTTP 400 `InvalidRequestException`** · 단계는 `PROCEDURE_DONE` 그대로. 다만 거절 이유가 「수납 필요」인지 「시작 안 한 시술」인지는 가르지 못했다(§3 K9b) (OQ-728) |

**「안 받음」 0건.** 모양이 다르거나 주의할 점은 아래 5개다(BE1 · BE2 · BE4 가 따라야 함).

1. **K1 문진 제출본** — 응답이 `data` 로 감싸여 있지 않고 **최상위 객체**다(`{id, visitorId, …, answers[], createdDateTimeUtc, agreements[]}`). SPEC §4.2 의 `data{createdDateTimeUtc, answers[…]}` 와 **다르다**
2. **K1 문진 제출본 없음** — HTTP 400 · `className` = `InvalidRequestException` · `errorProperties:[{key:"visitorId", reason:"NotFound"}]`. 지금 `KosError` 는 `className` 만 남긴다(「HTTP 400 InvalidRequestException」). 그래서 「아직 입력되지 않았어요」를 고르려면 BE 가 **`errorProperties` 를 따로 읽어야 한다**
3. **K8 「방 없음」** — `room` 은 늘 객체다. 방이 없으면 `room.id = ""` 다(위 표)
4. **K8 반영 지연** — `change-tasks-room` 결과가 바로(0초) 읽히지 않고 약 1초 뒤에 보였다. 앞 판 RT§1 은 「바로 보임」이었다. 묶음 1 · 3 · 6 단계도 1초 첫 번째 다시 읽기에서 보였다(1초 × 5 규칙 안)
5. **시각 꼴** — 보낼 때는 `…:00.000Z` 를 받는다. 읽을 때 `occupiedResources[].reservationTime` 은 `…:00Z`(밀리초 없음)로 온다. `desiredDischargeDateTimeUtc` 는 `.000Z` 그대로다. 비교는 파싱한 뒤에 해야 한다

### `funnel` 요청 모양 — 확정 (OQ-754)

```text
reserve / update-reservation 의
funnel: {
  funnel: <get-codes{category:"FUNNEL"} 의 data[] 항목 그대로 — {id, category:"FUNNEL", name, order, closed, default}>,
  funnelDetail: "<자유 글 — 없으면 빈 문자열>"
  // funnelCategory: <같은 Code 꼴> — 선택. 데모 지점은 get-codes{FUNNEL_CATEGORY} = 0건이라 보내지 않았다
}
```

- 근거 1 — KOS 웹 JS(`reservation-client_v0.0.541` · HAR 에 실린 청크)
  - 내부 `reserveV2` · `updateReservationV2` 의 요청 계약 `funnel` = `{funnel: Code, funnelDetail: string, funnelCategory: Code}` 다
  - `Code` 의 protobuf 필드는 `{id, category, name, order, closed, color?, default?}` 다
  - 화면 모델 → 계약 변환기(모듈 34496)는 HAR 청크에 없어서 읽지 못했다
- 근거 2 — 데모 실호출(K2)
  - 위 꼴로 보냈더니 200 이었다
  - 일정 상세(내부 `get-schedule-detail` · 하루 목록 `get-schedules-for-reservation` · 공개 `get-schedule-detail` 셋 다)에 `funnel{funnel{id, category, name, order, closed, default}, funnelDetail}` 로 **보낸 그대로** 보였다. K3 ~ K6 뒤에도 남았다
- **`{funnel:{id}}` 만 보내는 꼴은 시험하지 않았다.** BE 는 `funnel_code` 사본 행 전체를 넣는다(코드 표 1시간 사본의 열 = `id · category · name · order · closed · default` · SPEC §3.3 과 같음)
- 유입을 넣지 않은 일정의 `funnel` 은 `{funnelDetail:""}` 만 온다(K9b 일정 · 지금 데모 일정들)

---

## 1. K1 — 읽기 모양 (모두 200 · 제출본 없음 400 은 정상 응답)

| 호출 | 종류 · 경로 | 본문 키 | HTTP | 응답 키(모양) | SPEC-005 와 |
|---|---|---|---|---|---|
| 예약 그룹 | 내부 `schedule/group/v1/queries/get-reservation-groups` | `deleted · zoneIds` | 200 | `data[{id, title, memo, startDate, intervalMinutes, intervalCapacities[{enabled, intervalCapacity, zoneId}], isDefault, sameDayCloseBufferMinutes, operationTimetable{monday…sunday{enabled, startTime, endTime, breaktime}}, order}]` · 13그룹 | **같음**(§3.3 칸 모두 있음 · `memo` · `startDate` · `isDefault` 는 더 있음) |
| 하루 예약 | 내부 `schedule/v2/queries/get-schedules-for-reservation` | `baseDateUtc · reservationGroupIds · zoneIds` | 200 | `data[]` 일정(7건): `id · flowStep · flowStepUpdatedDateTimeUtc · receptionDateTimeUtc · updatedDateTimeUtc · zone{id,title} · visitor{id, name, phoneticName, gender, nationality, isNew, chartNumber, …} · reservation{status, consultationRequired, sedationRequired, counselor{id,name}, doctor{id,name}, reservationAssignee{id,name}, reservationMemo, funnel, connectedChannel, reservationGroupId, startDateTime, endDateTime, zoneId, requestedProcedures, desiredDischargeDateTimeUtc*} · occupiedResources[{id, type, reservationTime{startDateTimeUtc,endDateTimeUtc}, reservationGroup{reservationGroupId, zoneId, doctors[]}}] · purchaseIds[] · prescriptionIds[] · tasks[{type, sequence, title, status, paymentRequired, room{id, zoneId, title, order}, roomAssignedDateTimeUtc, …}]` | **같음**. `*` `desiredDischargeDateTimeUtc` 는 **값이 있을 때만 키가 온다**(K2 일정에서 확인) · `room` 은 늘 객체(주의 3) |
| 칸 정원 | 공개 `schedule/open/v2/queries/get-reservation-slots-by-groups` | `reservationGroupIds · startDateTimeUtc · endDateTimeUtc` | 200 | `data[{reservationGroupId, zoneId, slots[{reservationGroupId, zone{id,name}, startDateTimeUtc, endDateTimeUtc, capacity, reservationCount}]}]` | **같음** |
| 공지 | 내부 `meta/notice/v1/queries/get-notices` | `startDateTimeUtc · endDateTimeUtc · deleted` | 200 | 그 날짜 0건. 넓은 기간(9 ~ 12월)으로 한 번 더 읽음 → 1건 `{id, content, releaseDateTimeUtc, deleted}` | **같음** |
| 유입 코드 | 내부 `meta/codes/v1/queries/get-codes` | `category:"FUNNEL"` | 200 | `data[{id, category, name, order, closed, default}]` · 13건 | **같음** |
| (유입 분류) | 같은 경로 | `category:"FUNNEL_CATEGORY"` | 200 | `data[]` 0건 | — (§0 `funnel` 참고) |
| 기타 작업 | 내부 `schedule/etcetera-tasks/v1/queries/get-etcetera-tasks` | `{}` | 200 | `data[{id, title, deleted, translsMap}]` · 「방 배정」 있음 | **같음** |
| 직원 | 공개 `account/open/v1/queries/get-accounts` | `{}` | 200 | `data[{id, name, email, roleTags[], activate}]` · `COUNSELOR` 태그가 있는 활성 계정이 있다 | 같음(SPEC-003 사본) |
| 고객 검색 | 내부 `visitor/v2/queries/get-visitors` | `indexOfPage · countInPage · visitorName · phoneNumber · chartNumber · sort` | 200 | `{data[고객 전체 모양], count}` | 같음 |
| 고객 | 내부 `visitor/v2/queries/get-visitor` | `id` | 200 | `data{id, name, phoneticName, phoneNumber?, dateOfBirth, gender, nationality, language, passportNumber, passportSurname?, passportGivenNames?, passportExpiryDate?, address{…}, memo, visitorFunnel{…}, 동의 3, isNew, …}` — **빈 칸은 키 자체가 없다**(`?`) | 같음(U§2 그대로) |
| 문진 양식 | 공개 `visitor/open/v1/queries/get-visitor-questionnaire` | `visitorId` | 200 | 최상위 `{name, phoneNumber, address, addressDetail, dateOfBirth, gender, phone, agreements, pages[{id, title, questions[{questionId, title, sequence, answers[{answerId, title, inputType, isSubText, subText, translsMap}], translsMap}], translsMap}]}` | **같음**(최상위 · `pages[]`) |
| 문진 제출본 | 공개 `visitor/open/v1/queries/get-questionnaire-submit` | `visitorId` | 200 · 400 | 있음: **최상위** `{id, visitorId, visitorName, phoneNumber, phone, phoneticName, address, addressDetail, dateOfBirth, gender, createdDateTimeUtc, answers[{seq, questionId, questionTitle, answerId, answerTitle, memo}], agreements[…]}` / 없음: 400 `InvalidRequestException` + `errorProperties[{key:"visitorId", reason:"NotFound"}]` | **다름** — 주의 1 · 2 |
| 이전 방문 | 공개 `schedule/open/v1/queries/get-schedules-by-visitor` | `visitorId` | 200 | `data[]` 일정(하루 예약과 같은 모양) | 같음 |
| 일정 상세 | 내부 `schedule/v1/queries/get-schedule-detail` | `scheduleId` | 200 | `data{}` = 하루 예약 일정과 같은 모양 | 같음 |

---

## 2. K2 ~ K7 — 쓰기 (각 1회 · 2.5초 뒤 다시 읽어 전후 비교)

전후 비교는 일정 상세 전체(또는 고객 전체) JSON 을 키마다 비교했다. 「바뀐 칸」 밖은 모두 같았다.

| # | 종류 · 경로 | 본문 키 | HTTP · 응답 | 거절 이름 | 전 → 후 (바뀐 칸) |
|---|---|---|---|---|---|
| K2-1 | 내부 `visitor/v1/queries/find-duplicated-visitor` | `name · birthDateUtc` | 200 `{}` | — | 일치 없음 = 빈 객체(SPEC §8 그대로) |
| K2-2 | 내부 `v1/visitor/commands/create-visitor` | `name · phoneticName · gender · dateOfBirth("yyyy-MM-dd 00:00:00.000Z") · nationality` — **동의 플래그 없음** | 200 `{data:{id}}` | — | 새 고객: `isNew` true · 국적 · 생년월일 · 성별 · 발음은 보낸 그대로 · `aggrementPersonalInformation` false · `aggrementAdvertisements` false · `agreementInformationalNotification` **true**(보내지 않았는데 참) |
| K2-3 | 내부 `schedule/reservation/v2/commands/reserve` | `visitorId · zoneId · occupiedResources[{id(새 uuid4), type, reservationTime, reservationGroup{reservationGroupId, zoneId, doctors[{id,name}]}}] · reservationAssignee{id,name} · consultationRequired(true) · sedationRequired(true) · counselor{id,name} · reservationMemo · desiredDischargeDateTimeUtc · funnel{funnel, funnelDetail}` | 200 `{scheduleId}` | — | 새 일정 `RESERVED` · `RESERVED`. **7칸 모두 보낸 그대로**: `occupiedResources[0].reservationGroup.doctors` = 보낸 원장 1명 · `occupiedResources[0].id` = 보낸 uuid · `counselor` · `reservationMemo` · `consultationRequired` · `sedationRequired` · `desiredDischargeDateTimeUtc` · `funnel`. 담당자 = 시스템 계정(`get-user-account` id · `getAccounts` 에 있는 id). `reservation.doctor` 는 `{id:"", name:""}` 그대로(지정 의사는 `occupiedResources…doctors` 쪽에만 보인다) |
| K3 | 내부 `schedule/reservation/v2/commands/update-reservation` | `scheduleId · occupiedResources{items:[{id 그대로, type, reservationTime 새 값, reservationGroup{다른 그룹, zoneId, doctors 그대로}}]}` | 200 `{}` | — | 바뀐 칸: `occupiedResources[0].reservationGroup.reservationGroupId` · `…reservationTime.start/end` · `reservation.reservationGroupId` · `reservation.startDateTime/endDateTime` · `updatedDateTimeUtc`. **남음**: 묶음 id · 지정 의사 · 메모 · 유입 · 상담사 · 수면 · 상담 필요 · 귀가 희망 · 담당자 |
| K4 | 같은 경로 | `scheduleId · consultationRequired(false)` | 200 `{}` | — | 바뀐 칸: `reservation.consultationRequired` · `updatedDateTimeUtc` 뿐 |
| K5 | 같은 경로 | `scheduleId · counselor{id,name}`(다른 상담사) | 200 `{}` | — | 바뀐 칸: `reservation.counselor.id/name` · `updatedDateTimeUtc` 뿐 |
| K6 | 공개 `schedule/open/v1/commands/change-reservation-memo` | `scheduleId · memo` | 200 `{}` | — | 바뀐 칸: `reservation.reservationMemo`(보낸 글로 통째로) · `updatedDateTimeUtc` 뿐 |
| K7 | 내부 `visitor/v2/commands/update-visitor-personal-information` | `id · name · phoneticName · dateOfBirth · gender · registrationNumber · foreignRegistrationNumber · passportNumber · passportSurname · passportGivenNames · passportExpiryDate · address · nationality · language · snsInfo` — 직전 `get-visitor` 에 있던 칸 + 바꾼 칸(여권 성 · 여권 이름 · 여권번호 · 만료일 · 국적 · 생년월일). `get-visitor` 에 키가 없던 `phoneNumber` · `additionalPhoneNumber` · `email` 은 보내지 않음 | 200 `{}` | — | 바뀐 칸: `dateOfBirth`(→ `yyyy-MM-dd 00:00:00.000Z` 그대로) · `nationality` · `passportNumber` · `passportSurname`(키 생김) · `passportGivenNames`(키 생김) · `passportExpiryDate`(키 생김 · `yyyy-MM-dd`) · `updatedDateTimeUtc`. **남음**: 이름 · 발음 · 성별 · 언어 · 주소 · 메모 · 유입 · 동의 3 · `isNew`. 일정의 `visitor` 에도 새 생년월일 · 국적이 보였다 |

- K7 은 「읽은 묶음 전체 + 바꾼 칸」(SPEC §8 그대로)만 시험했다. 바꾼 칸만 보내는 부분 수정은 시험하지 않았다
- K3 ~ K6 은 모두 `RESERVED` 단계에서 보냈다. 접수 뒤 단계에서의 내부 `update-reservation{counselor}`(실장 호출은 `CONSULTATION_WAITING` · `CONSULTATION` 에서 보낸다)는 **시험하지 않았다**. 앞 판 MC§2.1 에서는 이동이 `RECEPTION` 에서 받아졌다

---

## 3. K8 · K9 — 접수 묶음(바로 시술) · 귀가

### K8 — 접수 묶음, 끝 단계 `PROCEDURE_WAITING` (K2 일정 · K4 로 상담 필요 = false)

| 순서 | 종류 · 경로 | 본문 키 | HTTP | 다시 읽기(1초 간격) |
|---|---|---|---|---|
| 0 | 내부 `get-schedule-detail` | `scheduleId` | 200 | `RESERVED` · `RESERVED` · 작업 0 |
| 1 | 내부 `schedule/v1/commands/recept` | `scheduleId` | 200 `{}` | 1번째(1초): `RECEPTION` · `IN_PROGRESS` · 접수 시각 있음 |
| 2 | 내부 `schedule/v1/commands/add-flow-tasks` | `scheduleId · tasks[{type:"ETCETERA", title:"방 배정", etceteraConfiguration{etceteraTaskId, name, translsMap}, translsMap}]` | 200 `{}` | 1번째(1초): `ETCETERA · seq 1 · 「방 배정」 · NOT_STARTED · room{id:""…}`(주의 3) |
| 3 | 내부 `schedule/flow/v1/commands/change-tasks-room` | `scheduleId · sequences:[1] · roomId` | 200 `{}` | 0초: 아직 방 빈 값 → 다음 읽기(약 1초)에서 `READY` · 방 A-레이저실 · `roomAssignedDateTimeUtc` 있음 (주의 4) |
| 4 | 내부 `schedule/v1/commands/change-flow-step` | `id · step:"PROCEDURE_WAITING"` | 200 `{}` | 1번째(1초): **`PROCEDURE_WAITING`** · `IN_PROGRESS` · 「방 배정」 `READY` + 방 · `paymentRequired` false |

- 방은 오늘 4층 일정 중 진행 단계(`RECEPTION` ~ `PROCEDURE`)에서 `CANCELED` 가 아닌 작업에 붙은 방(5개)을 빼고 `order` → `title` 순으로 첫 번째를 골랐다(SPEC §5.7 규칙)
- ⚠ 스크립트 기록: 2단계 뒤 「방 없는 「방 배정」」을 `room` 키가 없는 것으로 찾다가 못 찾고 멈췄다. 그 뒤 **쓰기는 다시 보내지 않고** 3단계부터 이어서 했다(그 사이 KOS 상태는 그대로였다). 이것이 주의 3 의 근거다

### K9 — 귀가 (K8 일정)

| 순서 | 종류 · 경로 | 본문 키 | HTTP | 전 → 후 |
|---|---|---|---|---|
| 1 | 공개 `schedule/open/v1/commands/change-flow-step` | `scheduleId · step:"PROCEDURE"` | 200 `{}` | `PROCEDURE_WAITING` → `PROCEDURE` |
| 2 | 내부 `schedule/v1/commands/cancel-flow-tasks` | `scheduleId · sequences:[「방 배정」] · reason:"CANCEL"` | 200 `{}` | 「방 배정」 `READY` → `CANCELED`(방은 남음) |
| 3 | 공개 `change-flow-step` | `scheduleId · step:"PROCEDURE_DONE"` | 200 `{}` | `PROCEDURE` → `PROCEDURE_DONE` · `IN_PROGRESS` |
| 4 | 공개 `change-flow-step` | `scheduleId · step:"COMPLETED"` | **200 `{}`** | `PROCEDURE_DONE` → **`COMPLETED`** · `reservation.status` **`COMPLETED`**. 공개 `get-schedule-detail` 도 같았다 |

- 「작업 완료」 단계: 이 일정의 작업은 「방 배정」 하나라서, 시술 현황 [귀가 대기]와 같은 순서로 「방 배정」을 취소하고 `PROCEDURE_DONE` 으로 갔다

### K9b — 귀가 거절: 수납 필요 작업이 남은 일정 (시험용으로 만든 두 번째 일정)

| 순서 | 종류 · 경로 | 본문 키 | HTTP | 결과 |
|---|---|---|---|---|
| 1 | 내부 `reserve` | 최소 모양(`visitorId` = K2 고객 · 그룹 「기타」 · 담당자 · 상담 필요 false · 수면 false · 메모) | 200 | `RESERVED` |
| 2 | 내부 `recept` | `scheduleId` | 200 | `RECEPTION` |
| 3 | 내부 `add-flow-tasks` | `수납필요 추가.har` 의 두 번째 `add-flow-tasks` 본문(`PROCEDURE` · `productOptionConfiguration` + `medicalServiceConfiguration`, **시술권 없음**) — `scheduleId` 만 바꿈 | 200 | 작업 1개 `PROCEDURE · NOT_STARTED · 방 없음 · paymentRequired: true` |
| 4 | 공개 `change-flow-step` | `step:"PROCEDURE_DONE"` | **200** | `RECEPTION` → `PROCEDURE_DONE`(KOS 는 시술 단계를 건너뛰는 것도, 시작 안 한 시술이 남은 것도 막지 않았다) |
| 5 | 공개 `change-flow-step` | `step:"COMPLETED"` | **400** | **`InvalidRequestException`** · 단계 `PROCEDURE_DONE` 그대로 · 작업 그대로 |

- **KOS 는 이 상태에서 `COMPLETED` 를 거절한다.** 응답 HTTP 상태 · `className` 만 기록됐다. `errorProperties`(무엇 때문인지)는 지금 `KosClient` 가 버려서 남지 않았고, 「재시도 금지」 규칙 때문에 다시 보내지 않았다
- 그래서 거절 이유가 **수납 필요(`paymentRequired`) 때문인지, 끝나지 않은(`NOT_STARTED`) 시술 때문인지는 가르지 못했다**. 두 조건이 한 작업에 같이 있었다
- SPEC §5.10 과의 관계
  - ccc 는 수납 필요 ≥ 1 이면 아예 보내지 않는다(409 `payment_required`)
  - 수납 필요 0 인데 끝나지 않은 시술이 남은 경우, KOS 가 400 으로 거절하면 → 409 `kos_rejected` 토스트가 된다
  - 지금 기본값(남은 작업을 ccc 가 취소하지 않음 · 거절은 토스트)과 **맞다**

---

## 4. 호출 기록

| 구분 | 경로 | 횟수 | 결과 |
|---|---|---|---|
| 쓰기 · 내부 | `v1/visitor/commands/create-visitor` | 1 | 200 |
| | `schedule/reservation/v2/commands/reserve` | 2 (K2 · K9b) | 200 |
| | `schedule/reservation/v2/commands/update-reservation` | 3 (K3 · K4 · K5) | 200 |
| | `visitor/v2/commands/update-visitor-personal-information` | 1 | 200 |
| | `schedule/v1/commands/recept` | 2 (K8 · K9b) | 200 |
| | `schedule/v1/commands/add-flow-tasks` | 2 (K8 · K9b) | 200 |
| | `schedule/flow/v1/commands/change-tasks-room` | 1 | 200 |
| | `schedule/v1/commands/change-flow-step` | 1 | 200 |
| | `schedule/v1/commands/cancel-flow-tasks` | 1 | 200 |
| 쓰기 · 공개 | `schedule/open/v1/commands/change-reservation-memo` | 1 | 200 |
| | `schedule/open/v1/commands/change-flow-step` | 5 | 200 × 4 · **400 × 1**(K9b `COMPLETED`) |
| 조회 | 내부 · 공개 queries | 58 | 200 × 56 · 400 × 2(문진 제출본 없음 — 정상 응답) |
| 인증 | 공개 `exchange-token` · 내부 `sign-in` · `get-user-account` | 실행마다 | 모두 200(호출 로그 밖) |

- **쓰기 20건**(200 × 19 · 400 × 1). 쓰기 키마다 1회씩이다. 재시도 0 · 허가 목록 밖 쓰기 0 · **운영 키 0**
- 사용자 스택(3700 · 8700) · 사용자 프로세스는 건드리지 않았다. 떠 있는 back 이 KOS 를 폴링하므로, K8 끝 ~ K9 귀가 사이(약 30초) 시술 현황판에 시험 카드가 잠깐 보였을 수 있다

---

## 5. 남긴 데모 데이터 (K10 — 지우지 않음 · 지울지는 사용자)

모두 **데모 지점 · 4층 · 2026-10-26** 에 「시험용으로 만듦」이다.

| # | 무엇 | 지금 상태 | 시술 현황판 |
|---|---|---|---|
| 1 | **시험 고객 1명**(신규) — 이름 `WPKOS Probe` · 국적 US · 여권 성 `PROBE`(모두 지어낸 값) · 연락처 · 이메일 없음 | `isNew` true | — |
| 2 | **일정 1**(K2 ~ K9) — 19:00 KST · 그룹 「영미권」(K3 로 「일본」 19:30 에서 옮김) · 지정 의사 1 · 상담사 · 유입 「인스타그램」 · 메모 · 귀가 희망 | **`COMPLETED`**(귀가 완료) · 「방 배정」 `CANCELED`(A-레이저실) | 안 보임(`COMPLETED`) |
| 3 | **일정 2**(K9b) — 17:00 KST · 그룹 「기타」 · 같은 고객 | **`PROCEDURE_DONE`**(귀가 대기) · 시술 작업 1개 `NOT_STARTED` · **수납 필요** · 방 없음 | **안 보임**(방 없음 — SPEC-003 §5.1 조건 3). 예약 현황 E2E 에서는 「귀가 대기 · 수납 필요 1건」 일정으로 보인다 |

- 일정 2 는 `COMPLETED` 가 거절되어 끝내지 못했다. 끝내려면 KOS 화면에서 그 시술 작업을 취소하거나 수납한 뒤 귀가 처리하면 된다(사용자 · 코디 판단)
- 시술 대기(`PROCEDURE_WAITING`)로 남긴 일정은 0이다

---

## 6. 계약 대조 · 코디가 확인할 것

| SPEC-005 줄 | 판정 | 고칠 곳(제안 · 결정은 코디 · planner) |
|---|---|---|
| §8 신규 고객 `create-visitor`(동의 플래그 없음) | 받음 | OQ-753 닫아도 됨. KOS 기본값이 정보성 알림 동의 = true 로 남는다는 사실은 사용자에게 알릴 거리 |
| §8 `reserve` 전 칸 · OQ-754 `funnel` | 받음 · 모양 확정 | §8 본문 `funnel?` → `funnel?:{funnel:<FUNNEL 코드 행 전체>, funnelDetail}` 으로 적기 |
| §8 이동 · 진행 경로 · [실장 호출] `update-reservation` 부분 수정 · OQ-714 · OQ-755 | 받음 | OQ-755 닫아도 됨(단 실장 호출의 접수 뒤 단계는 미시험 — E2E #17 에서 확인) |
| §8 메모 `change-reservation-memo` | 받음 | 「미확인」 → 데모 확인 |
| §8 고객 정보 · OQ-739 | 받음 | 날짜 꼴 · 권한 확정. `get-visitor` 에 없는 키는 「읽은 묶음」에 없으니 보내지 않는다(빈 문자열로 채우지 않음) |
| §8 바로 시술 · OQ-756 | 받음 | §5.6 3 · 4단계 「방 없는」 = `room.id` 빈 값으로 적기(주의 3) |
| §8 [귀가 완료] · OQ-728 | 받음 + 거절 확인 | 기본값 그대로. 거절 이름은 `InvalidRequestException` — 토스트 문구에 쓸 알려진 이름이 아니다 |
| §4.2 문진 제출본 | **다름** | 응답 = 최상위 객체(`data` 없음) · 없음 = 400 `InvalidRequestException` + `errorProperties[visitorId NotFound]` → BE2 는 `KosError` 의 이름만으로 가르지 못한다(주의 1 · 2) |
| §4.3 · §5.6 반영 지연 | 같음 | 모든 다시 읽기가 1초 첫 번째에서 보였다. `change-tasks-room` 도 0초에는 안 보일 수 있다(주의 4) |
