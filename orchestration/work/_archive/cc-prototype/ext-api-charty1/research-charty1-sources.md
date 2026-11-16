# 조사 — charty 1차 상담: 요청 항목별 「어디서 가져오나」

> researcher · 조사일 **2026-11-16** · 데모 테넌트만 · KOS 공개 API **조회(`/queries/`)만** 불렀다.
> 쓰기(`/commands/`) 호출은 0건이다. 공개 토큰 교환(`/open/authorization/commands/exchange-token`)만 1회 불렀다(인증 · 데이터 쓰기 아님). 내부 API 토큰 발급(`sign-in`)도 `/commands/` 경로라 이번에는 부르지 않았다. 그래서 내부 API 는 **코드 · HAR 로만** 본다.
> public 레포다. 키 · 토큰 · 테넌트 id · KOS id · 사람 이름 · 연락처 · 메모 원문은 적지 않았다. 아래에는 경로 · 칸 이름 · 모양 · 건수만 있다.
> 코드 = kknaksss/cc-prototype `origin/main` `0a58aba`(`git show` 로만 읽음). 줄 번호는 모두 `procedure/back/app/` 아래 파일 기준이다.
> KOS 스펙 = `https://developers.kos-solution.com/openapi.yaml`(2026-11-16 받음 · `info.version` **1.0.1** · 작업 **81개**. 10-20 조사 때는 75개였다). 문서 URL 꼴 = `https://developers.kos-solution.com/docs/openapi/<태그>#<operationId>`.

표기: **확인** = 이번에 데모에서 불러 본 것 · **스펙** = openapi.yaml · **HAR** = 로컬 HAR(값은 옮기지 않음) · **코드** = origin/main · **추정** = 해석(근거를 함께 적음).
분류: **A** 지금 코드에 있음 / **B** KOS 공개 API 로 됨 / **C** 내부 API(HAR)로만 됨 / **D** CC 저장 필요 / **E** 없음 · HAR 필요.

---

## 0. 요약표 (항목 21개)

| # | 항목 | 분류 | 원천 한 줄 | KOS 호출 수 | 실호출 |
|---|---|---|---|---|---|
| 1-1 | 접수 목록(board) | **A** | 사본 `reservation`. 날짜 조회 = 내부 `get-schedules-for-reservation` 1 + 공개 정원 1 + 내부 공지 1 + (오늘) 공개 수납 1. 10초 캐시 | 캐시가 낡았을 때만 날짜당 3~4번. 목록 건수와 무관 | 공개 같은 원천(`getSchedulesByFlowStep`) 확인 |
| 1-2 | 예약 상세(고객 정보) | **A**(칸별 A/C) | 사본 + 내부 `get-schedule-detail` 1 + 내부 `get-visitor` 1 + 공개 문진 2 + 공개 고객 일정 1 (+ 귀가면 수납 1) | 요청 1번에 5~6번 + 날짜 조회 | 공개 부분 확인 |
| 1-3 | 고객 언어 쓰기 | **A**(C) | 내부 `get-visitor` 다시 읽기 → 내부 `update-visitor-personal-information`(개인 묶음 전체) | 2번(값이 같으면 1번) | 코드만(쓰기 금지) |
| 2-1 | 담당 상담사(목록) | **A** | 사본 `reservation.counselor` = KOS `reservation.counselor`. **스펙 이름은 「희망 상담사」**다 | 0번 추가 | 확인 |
| 2-2 | 관리실(목록) | **A** | 사본 `reservation.room_title`(작업 방 중 가장 늦게 배정된 것) | 0번 추가 | 확인 |
| 2-3 | 처음 상담 대기가 된 시각 | **E**(+B 추정 · D 후보) | 단계 이력을 그대로 주는 조회는 HAR · 스펙 어디에도 없다. 공개 `getScheduleStatistics` 의 단계별 체류 분으로 **계산만** 할 수 있다 | 통계로 하면 기간당 1번(페이지) | 확인(통계) |
| 2-4 | 접수 시각(귀가 포함) | **A** | 사본 `reservation.reception_at` = KOS `receptionDateTimeUtc`. board 카드는 귀가 고객을 빼지 않는다(원내 현황만 뺀다) | 0번 추가 | 확인 |
| 3-1 | 상담 여부(상담 · 시술만) | **A**(CC 판정) · KOS 칸은 다른 뜻 | CC 판정 = 지금 단계 · CC 접수 이벤트 · [+ 상담 추가]. KOS `consultationRequired` 는 안 읽는다 | 0번 | 확인(어긋남 106건) |
| 3-2 | customerId 로 시술권 | **B** | 사본 `customer.kos_id` → 공개 `getTicketBundlesQuery` 1 | 1번 | 확인 |
| 3-3 | 시술권 「사용 중」 장수 | **C** | 공개 묶음 조회에는 `IN_USE` 장이 안 온다. 내부 `ticket/v1/queries/get-ticket-bundles` 에는 온다 | 내부 1번 | 공개 확인 · 내부는 HAR |
| 3-4 | 시술권 만료일 · 차감 | 만료일 **E**(발행일 A) · 차감 **C** | 시술권에 만료 칸이 없다(스펙 · 공개 · HAR). 차감 = 내부 `add-flow-tasks` 작업에 `ticketConfiguration` 을 실음 | 차감 1번 | 스펙 · HAR(쓰기 안 함) |
| 3-5 | 선불카드 잔액 · 만료일 | **B** | 공개 `getPrepaidCardSummaries`(카드별 만료일 · 잔액) · `getVisitorPrepaidCardBalance`(합산) | 1~2번 | 확인 |
| 3-6 | 희망 시술 · 예산 · 동행자 · 원장 상담 · 통역 | 희망 시술 **B** · 원장 지정 **B**(희망 의사) · 나머지 **E/D** | KOS 예약에 `requestedProcedures` · `doctor`(희망 의사) · `counselor`(희망 상담사)가 있다. 예산 · 동행자 · 통역 칸은 KOS · CC 둘 다 없다 | 0번(일정 응답에 있음) | 확인 |
| 3-7 | 진단기 · 날짜 | **E** | KOS · CC 어디에도 없다 | — | 스펙 검색만 |
| 3-8 | 열람 기록 | **A**(틀만) · **D** | `ext_call` 은 연동처 · 경로 · 상태 · 결과뿐이다. 고객 · 직원 칸은 일부러 없다. 직원 행위는 `event_log.actor` | 0번 | 코드 |
| 3-9 | 지난 방문의 상담자 | **B**(코드에는 없음) | 공개 `getSchedulesByVisitor` 원소에 `consultation.counselor` · `consultations[].counselors[]` 가 온다. 지금 `previousVisits` · ext `visits` 는 안 꺼낸다 | 0번 추가(같은 호출) | 확인 |
| 4-1 | 오더 메모 등록 · 수정 | **C** · 읽기 **A/B** | 쓰기 = 내부 `schedule/v1/commands/change-order-memo {scheduleId, orderMemo}`(HAR). 읽기 = 일정 `orderMemo`(시술 현황 사본 · 공개 일정 응답) | 쓰기 1번 | HAR(쓰기 안 함) · 읽기 확인 |
| 4-2 | 차트 메모 등록 · 수정 | **C** | 작업 단위 `change-flow-tasks-assignee-memo` · `change-flow-tasks-doctor-memo {scheduleId, sequences[], …Memo}`(HAR). CC 에는 읽기 · 쓰기 다 없다 | 메모 1개당 1번 | HAR(쓰기 안 함) · 읽기 확인 |
| 4-3 | (참고) 예약 메모 | **A** · **B** | 직원 `PUT /reservations/{id}/memo` = 공개 `changeReservationMemo` | 1번 | 코드 |
| 4-4 | (참고) 고객 특이사항 | **A** · **C** | 직원 `PUT /customers/{id}/remark` = 내부 다시 읽기 + `update-visitor-management-information` | 2번 | 코드 |
| 4-5 | (참고) 상담 메모 | **B** | 공개 `updateScheduleConsultationInfo {scheduleId, consultationMemo}`. CC 쓰기 없음 | 1번 | 스펙 |

항목 수: 브리프 1-1 ~ 3-9 의 16개 + 4 오더 · 차트 2개 = **18개**. 거기에 4 와 관계를 보라고 한 기존 쓰기 3개(4-3 ~ 4-5)를 더해 **21행**이다.

---

## 1. 직원 API 를 ext 로

### 1-1 `GET /api/reservations/board` — 접수 목록

**원천(A · 코드)**
- `service/reservations.py:285-366` `board()`. 먼저 `ensure_day(day)`(`:276`)를 부르고, 나머지는 사본 `reservation` · `customer` · `reservation_slot` · `notice` 만 읽는다.
- `kos/reservation_sync.py:267-276` `ensure()`: 날짜 캐시 `kos_resv_cache_sec = 10`초(`config.py:32`)가 낡았을 때만 `fetch_day()`(`:278-320`)를 부른다. 같은 날짜는 날짜 잠금으로 한 번만 돈다.

| `fetch_day` 안 호출 | 종류 | 경로 | 비고 |
|---|---|---|---|
| 하루 예약 | 내부 | `schedule/v2/queries/get-schedules-for-reservation`(`:28` · `:290`) | `{baseDateUtc, reservationGroupIds, zoneIds}` · 두 구역 |
| 칸 정원 | 공개 | `schedule/open/v2/queries/get-reservation-slots-by-groups`(`:29` · `:333`) | |
| 공지 | 내부 | `meta/notice/v1/queries/get-notices`(`:30` · `:352`) | |
| 수납 금액(오늘만 · 원내 일정 수납이 있을 때) | 공개 | `purchase/open/v1/queries/get-purchase-summaries`(`:371`) | 메모리에만 |

- 1시간 목록 `master()`(`:177-190` · 구역 · 그룹 · 방 · 유입 코드 · 기타 작업 = 5번)은 서버 시작 때와 1시간마다 돈다. board 요청과는 무관하다.
- **KOS 호출 수**: board 1번 = 캐시가 신선하면 0번, 낡았으면 3~4번. **카드(고객) 수와 무관**하다. 고객마다 따로 부르는 호출이 없다.

**ext 로 낼 때 칸(사본에 이미 있는 것)**: 카드(`:313-320`) = `reservationId` · 시작 · 끝 · 그룹 · 구역 · 고객(`customerId` · 이름 · 발음명 · 성별 · 국적 · 신규) · 상태(`main` · `sub`) · 수납 필요 수. 원내 현황(`_clinic` · `:368-391`) = 접수 시각 `receptionAt` · 상태 · 금액. 사본 열은 `repository/db.py:110-118` `reservation` 이다(`flow_step` · `flow_step_at` · `reception_at` · `counselor` · `room_title` · `consultation_required` · `memo` · `desired_discharge_at` 등).

**데모(확인)**: 같은 원천을 공개 `getSchedulesByFlowStep`(단계 7개 × 최근 30일)으로 불렀다. 모두 200이고, 162건(접수 11 · 상담 대기 16 · 상담 2 · 시술 대기 58 · 시술 23 · 시술 완료 36 · 귀가 16), 단계당 96~254ms 였다. [문서](https://developers.kos-solution.com/docs/openapi/schedule#getSchedulesByFlowStep)

**함정**
- board 는 사본을 보고, 사본은 10초 캐시다. ext 가 board 를 자주 부르면 직원 화면과 같은 캐시를 같이 쓴다. KOS 호출은 늘지 않지만 최대 10초 늦은 값이다.
- 날짜 조회가 실패하면 board 는 사본 그대로 + `sync.lastError` 다(`:295-297`). ext 에서 이것을 오류로 볼지, 낡은 값으로 낼지는 정해야 한다.
- 카드는 **묶음(resource)당 한 장**이다(`:308`). 한 예약이 여러 장일 수 있다. 「오늘 고객」 목록으로 내려면 예약 단위로 다시 묶어야 한다.

### 1-2 `GET /api/reservations/{reservation_id}` — 고객 정보 칸별 원천

호출 순서(`service/reservations.py:484-579`): `ensure_today()` + `ensure_day(그 날짜)` → `refresh_schedule()` 내부 `schedule/v1/queries/get-schedule-detail` 1번(`:739` · 캐시 없음) → `_detail_reads()`(`:581-619`) 동시 4번(귀가 + 수납 있으면 5번).

| 칸 | 응답 위치 | 원천 | 분류 |
|---|---|---|---|
| 기본 정보(이름 · 성별 · 국적 · 신규 · 차트 번호) | `customer.*` | 사본 `customer`(`:552-555`) | A |
| 나이 · 개인 정보 묶음 | `customer.age` · `customer.personal` | **내부** `visitor/v2/queries/get-visitor`(`:593` · `personal_of` `:150-171`) | A(C) |
| **고객 언어** | `customer.personal.language` | 내부 `get-visitor` 의 `language`(`:165`). **공개 `getVisitor` 에는 language 칸이 없다**(스펙 · 확인: 응답 키 9개 `id · chartNumber · name · phoneNumber · dateOfBirth · gender · nationality · passportSurname · passportGivenNames`) | A(C) |
| 문진 | `health` | 공개 `visitor/open/v1/queries/get-visitor-questionnaire` + `get-questionnaire-submit`(`:593-594`). CC 웹 제출본이 더 새로우면 그것(`_health` `:621-643`) | A(B) |
| 이전 방문 | `previousVisits[]` | 공개 `schedule/open/v1/queries/get-schedules-by-visitor` 1번(`:594` · `previous_visits` `:192-218`) | A(B) |
| 예약 메모 | `reservation.memo` | 사본 `memo` = KOS `reservation.reservationMemo`(`reservation_sync.py:132`) | A |
| 귀가 희망 시각 | `reservation.desiredDischargeAt` | 사본 = KOS `reservation.desiredDischargeDateTimeUtc`(`:135`) | A |
| 유입 경로 | `reservation.funnel`(예약) · `customer.funnel`(고객) | 예약 = 사본 `funnel`(`:133`). 고객 = 내부 `get-visitor` 의 `visitorFunnel`(`visitor_funnel_of` `:174-181`) | A · A(C) |
| 고객 특이사항 | `customer.remark` | 내부 `get-visitor` 의 `memo`(`:557`) | A(C) |

**KOS 호출 수**: 상세 1번 = 일정 상세 1 + 고객 1 + 문진 2 + 고객 일정 1 (+ 수납 1) = **5~6번**. 여기에 오늘 · 그 날짜 사본이 낡았으면 날짜 조회(3~4번)가 붙는다.

**데모(확인)**: 공개 `getScheduleDetail` 1건 200(46ms) · 키 22개. 공개 `getSchedulesByVisitor` 5명 200 · 일정 2~13건 · 56~146ms. [getScheduleDetail](https://developers.kos-solution.com/docs/openapi/schedule#getScheduleDetail) · [getSchedulesByVisitor](https://developers.kos-solution.com/docs/openapi/schedule#getSchedulesByVisitor) · [getVisitor](https://developers.kos-solution.com/docs/openapi/visitor#getVisitor)

**함정**
- `_detail_reads` 는 하나가 실패해도 나머지를 쓴다(`personalError` 같은 칸으로 냄). ext 계약에서 부분 실패를 어떻게 보일지 정해야 한다.
- 상세는 열 때마다 KOS 를 5~6번 부른다. 직원 화면은 모달 폴링으로 이것을 반복한다. ext 로 같은 것을 열면 키당 60초 60번 제한(DEC-010 D-34) 안에서 KOS 쪽이 최대 6배로 늘어난다.
- `previousVisits[]` 에는 `reservationMemo` · `consultationMemo` · 의사 이름이 있다(`:209-213`). ext `visits` 는 DEC-011 D-03 으로 이것들을 **뺐다**. 상세를 ext 로 내면 D-03 과 부딪힌다.
- 고객 언어 · 특이사항 · 고객 유입은 **내부 API 에만** 있다. 내부 API 의존(시스템 계정 토큰 · 브라우저 UA · 2026-11-03~)이 ext 에 하나 더 붙는다.

### 1-3 `PUT /api/customers/{customer_id}/personal` — 언어만 바꿀 때

**호출 모양(코드 · 실호출 안 함)** `service/reservations.py:1056-1084`
1. 내부 `visitor/v2/queries/get-visitor {id}` — 지금 값을 다시 읽는다(`:1063`)
2. 본문 = `{id}` + 다시 읽은 값 중 `PERSONAL_KEYS` 17개(`:1167` — `name · phoneticName · phoneNumber · additionalPhoneNumber · email · dateOfBirth · gender · registrationNumber · foreignRegistrationNumber · passportNumber · passportSurname · passportGivenNames · passportExpiryDate · address · nationality · language · snsInfo`)에서 **있는 키 전부** + 바꾼 키(`language`)만 덮는다(`:1068-1075`)
3. 바뀐 값이 지금 값과 같으면 KOS 를 부르지 않는다(`:1072-1074`)
4. 내부 `visitor/v2/commands/update-visitor-personal-information`(`:89` · `:1076`)

- 요청 칸은 `PersonalIn.language`(`schemas/reservations.py:841` · 「KOS 값」). 보낸 키만 바꾼다(`model_fields_set`).
- HAR: 개인 정보 쓰기 HAR 은 없다. 위 모양은 코드에만 근거한다. 언어 값 모양은 `상담대기.har` 의 내부 `get-visitor` 응답에서 `language: str(2)` · `str(5)` 두 꼴이 보였다(값은 옮기지 않음).

**다른 칸을 같이 덮는 위험**
- KOS 쓰기는 「개인 묶음 전체 교체」다. 그래서 언어 하나만 바꿔도 다시 읽은 16칸을 같이 보낸다. 1번(읽기)과 4번(쓰기) 사이에 KOS 웹에서 다른 칸을 고치면 그 변경이 **덮인다**(경합 창 · 잠금 없음).
- 다시 읽은 응답에 없던 키는 보내지 않는다(K7 · `:1069`). 보내지 않은 키를 KOS 가 비우는지, 그대로 두는지는 **확인 안 됨**(쓰기 금지 · HAR 없음).
- 성공하면 사본 `customer` 의 이름 · 발음명 · 국적 · 성별만 맞춘다(`:1078-1082`). 언어는 사본 열이 없다.

---

## 2. 상세에만 있는 칸을 목록에

**핵심 답: 2-1 · 2-2 · 2-4 는 날짜 조회 응답에 이미 있고, 사본 `reservation` 열에 들어가 있다. 목록에 넣어도 KOS 호출은 늘지 않는다.** 2-3 만 원천이 없다.

### 2-1 담당 상담사(staffId · 이름)
- 원천(A): 사본 `reservation.counselor`(`{id, name}`) ← KOS `reservation.counselor`(`reservation_sync.py:131`). 상세는 `_staff_ref`(`reservations.py:569` · `:682-686`)로 KOS 계정 id 를 사본 `staff.id`(ccc staffId)로 바꾼다. board 도 같은 `ctx` 에서 바로 바꿀 수 있다(추가 호출 없음).
- **스펙의 뜻이 다르다.** 스펙 `getScheduleDetail` 에서 `reservation.counselor` 는 **「희망 상담사」**이고 `reservation.doctor` 는 「희망 의사」다. 실제로 상담한 사람은 `consultation.counselor`(「상담사」) · `consultations[].counselors[]` 에 있다. 우리 schema 는 `reservation.counselor` 를 「예약 담당 상담사」로 적었다(`schemas/reservations.py:380` · `:438`).
- 데모(확인 · 최근 30일 162건): 예약 상담사만 있음 6 · 상담 상담사만 있음 30 · 둘 다 있고 같음 5 · **둘 다 있고 다름 3** · 둘 다 없음 118.
- 함정: 「담당 상담사」를 예약의 희망 상담사로 낼지, 실제 상담자로 낼지에 따라 원천이 다르다(정할 것).

### 2-2 관리실
- 원천(A): 사본 `reservation.room_title`(`reservation_sync.py:138`) = 작업에 붙은 방 중 `roomAssignedDateTimeUtc` 가 가장 늦은 것(`_card_room_task` · `kos/sync.py` 에서 가져다 씀 · `reservation_sync.py:123-124`). 상세 `flow.roomTitle` 이 바로 이 값이다(`reservations.py:675`).
- 데모(확인): 작업 519개 중 방이 있는 작업 392 · 방 빈 값 127(방 없음 = `room.id` 빈 문자열).
- 함정: 방은 **작업 단위**다(DAY 조사 §2). 「관리실」 하나로 내면 「가장 늦게 배정된 작업」 규칙이 그대로 계약이 된다.

### 2-3 처음 상담 대기가 된 시각 — 이번 조사의 핵심

**지금 코드**: 상세 `_flow()`(`reservations.py:645-679`)의 상담 시각 `c_at` 은 사본 `flow_step_at` = KOS `flowStepUpdatedDateTimeUtc`(`reservation_sync.py:129`)다. 이 값은 「지금 단계가 된 시각」이라 단계가 넘어가면 바뀐다(`:665`). 상담이 끝난 뒤에는 KOS 상담 시작 시각(`consultation_started_at`)으로 바꿔 쓴다(`:667-668`).

**HAR(`2026-11-16-cc-charty1/har/상담대기.har` · 47항목 · KOS 30 · 그 밖은 Datadog RUM · Amplitude)**

| # | 요청 | 모양 |
|---|---|---|
| #1 · #2 · #4 | 내부 `visitor/v2/queries/get-visitor` | `{id}` → 고객 36키(`language` 포함) |
| #6 | 내부 `schedule/v1/queries/get-schedule-detail` | `{scheduleId}` → 22키. 단계 칸은 `flowStep` · `flowStepUpdatedDateTimeUtc` 두 개뿐이다 |
| #9 | 내부 `schedule/v1/queries/get-schedule-summaries` | `{visitorId, sort}` → 일정 요약(`flowStep` · 예약 · 작업 메모) |
| #7 | 내부 `consultation/v1/queries/get-consultations-by-visitor-id` | `{visitorId}` → `data[]` |
| **#41** | 내부 **`schedule/v1/commands/change-flow-step`** | `{id: uuid, step: CONSULTATION_WAITING}` → `{}`(사용자가 KOS 웹에서 한 쓰기 · 우리는 부르지 않음) |
| 그 밖 | 그룹 · 코드 · 계정 · 선불카드 · 시술권 · 통화 · 부가세 · 공지 조회 | — |

- **단계 변경 이력을 주는 호출은 이 HAR 에 없다.** HAR 전체(요청 · 응답 본문)에서 `histor` · `flowStepLog` · `changedDateTime` 을 찾아봤다. KOS API 응답에는 0건이었다. RUM 의 `historyMenu=reservationHistory` 는 KOS 웹 **화면 주소의 질의 값**(예약 이력 탭)일 뿐이고, 그 탭을 여는 API 호출은 HAR 에 없다.
- 스펙: 일정 응답(`getScheduleDetail` · `getSchedules` · `getSchedulesByFlowStep` · `getSchedulesByVisitor`)의 단계 칸은 `flowStep` · `flowStepUpdatedDateTimeUtc`(「내원 단계 변경 일시」) 둘뿐이다. 이력 배열은 없다. 이력 조회 작업도 81개 중 없다.

**공개 통계로 계산은 된다(B · 추정)** — [getScheduleStatistics](https://developers.kos-solution.com/docs/openapi/statistics#getScheduleStatistics)
- `statistics/open/v1/queries/get-schedule-statistics`: 예약마다 단계별 체류 분(`receptionDwellTimeMinute` · `consultationWaitingDwellTimeMinute` · `consultationDwellTimeMinute` · `procedureWaitingDwellTimeMinute` · `procedureDwellTimeMinute` · `procedureDoneDwellTimeMinute`)과 `receptionDateTimeUtc` 를 준다. → KOS 안에는 단계 이력이 있다는 뜻이다(추정). 다만 시각이 아니라 **분 단위 체류 시간**만 밖으로 나온다.
- 데모(확인): 최근 30일 1번 호출(`limit 500`) 200 · 273ms · 422행(`totalCount 422`). 위 162건과 일정 id 로 맞췄다.
  - 체류 칸은 **지나간 단계만** 생긴다. 지금 단계는 없다. 예: 지금 상담 대기 16건 중 7건은 `reception` 체류만 있다.
  - 단계가 **앞뒤로 오간다.** 지금 상담 대기인데 시술 대기 · 시술 체류가 있는 일정이 7건이다(상담 추가로 되돌아온 것으로 추정).
  - 「접수 시각 + 접수 체류 분」 ≈ 상담 대기가 된 시각인지 시험했다: 지금 상담 대기 15건의 `flowStepUpdatedDateTimeUtc − (접수 + 접수 체류)` = **1분 안 11건 · 84 ~ 358분 4건**. 1분 안인 것은 접수 → 상담 대기로 곧장 간 일정이다. 크게 어긋난 4건은 앞뒤로 오간 일정이다. 즉 이 계산은 「상담 대기를 한 번만, 접수 바로 뒤에 거쳤을 때」만 맞고, 분 단위로 버려진다.
  - 같은 단계를 두 번 거치면 체류 분이 합쳐지는지 · 따로인지는 **문서에 없음 · 확인 안 됨**.
- KOS 호출 수: 기간 · 고객 필터(`visitorIds` · 기간 · 커서)로 1번에 여러 행을 받는다. 목록 1번당 1번(+ 페이지)이다.

**CC 쪽 보조 근거(D 후보)**
- CC 접수 이벤트 `event_log` `type = reception`, `payload.endStep = CONSULTATION_WAITING`(`service/reception.py:165` · `:205`). 시각 = `event_log.at`(CC 서버 시각). 이 값은 **CC 에서 접수한 경우에만** 있다. KOS 웹에서 접수하거나 단계를 바꾸면 남지 않는다. [+ 상담 추가] 이벤트(`consultation_add` · `:263`)도 같다.
- 시술 현황 동기화(`kos/sync.py:110-111`)와 예약 사본(`reservation_sync.py:129`)은 `flow_step_at` 을 **덮어쓴다.** 이력을 쌓지 않는다. 10초 조회마다 「단계가 바뀐 것을 본 시각」을 따로 남기면 D 가 되지만, 지금은 없다.

**함정 · 결론**: 「처음 상담 대기 시각」을 KOS 에서 바로 받는 길은 이번 HAR · 스펙으로는 **없음(E)**. KOS 웹에 「예약 이력」 탭이 있으므로, 그 탭을 연 HAR 이 있으면 내부 이력 조회가 보일 수 있다(**HAR 필요**). 경로를 짐작해 만들지는 않았다.

### 2-4 접수 시각 — 귀가 마친 고객 포함
- 원천(A): 사본 `reservation.reception_at` = KOS `receptionDateTimeUtc`(`reservation_sync.py:129`). 상세 `flow.receptionAt`(`reservations.py:675`)과 원내 현황 `receptionAt`(`:388`)이 같은 열이다.
- **board 가 귀가 고객을 빼나**: 카드(`cards`)는 그날 예약을 **전부** 싣는다(`:303-325` · 상태로 거르지 않음). 원내 현황 `clinic.items` 는 `IN_CLINIC_FLOWS`(접수 ~ 시술 완료 · `domain/reservation_rules.py:34-35`)만이라 **귀가(`COMPLETED`)를 뺀다**(`:371`). 지금 카드에는 접수 시각 칸이 없다.
- 데모(확인): 접수 뒤 단계 162건 중 `receptionDateTimeUtc` 가 빈 것 4건(귀가 1 · 시술 완료 1 · 상담 1 · 상담 대기 1). 통계의 접수 시각과는 147/147 같았다.
- 함정: 접수 뒤 단계인데 접수 시각이 비는 일정이 있다(4/162). null 로 낼 수밖에 없다.

---

## 3. 없는 칸 · API

### 3-1 접수의 상담 여부(상담 · 시술만)
- CC 판정(A · `reservations.py:653-656`) — 「상담 거침」은 다음 중 하나다. ① 지금 단계가 `CONSULTATION_WAITING` · `CONSULTATION`. ② CC 접수 이벤트의 `endStep = CONSULTATION_WAITING`. ③ `consultation_add` 이벤트. 주석에 「KOS `consultationRequired` 는 안 읽는다(10-27)」라고 적혀 있다. 접수 끝 단계도 직원이 고른 경로이고, `consultationRequired` 가 아니다(`reception.py:165`). 예약 생성은 `consultationRequired` 를 보내지 않는다(`reservations.py:834` 주석 「KOS 기본 false」).
- KOS 칸: `reservation.consultationRequired`(스펙 「상담 필요 여부」). 사본 `consultation_required` 에는 저장하지만(`reservation_sync.py:130`) 판정에는 쓰지 않는다.
- 데모(확인 · 162건): `consultationRequired=false` 인데 상담을 거친 흔적(상담 단계 · 상담 기록 · 통계 상담 대기 체류)이 있는 일정 **106** · false 이고 흔적 없음 54 · true 이고 흔적 있음 2 · true 이고 흔적 없음 0. → 데모에서 이 칸은 「실제로 상담을 했나」를 거의 나타내지 않는다.
- 함정: ②③ 은 CC 에서 한 조작만 안다. KOS 웹에서 상담 대기로 보낸 일정이 지나가면 ① 도 풀린다. 그러면 CC 판정은 「상담 안 함」이 된다. KOS 의 `consultations[]` · 통계 상담 체류가 보조 원천이 될 수 있다(정할 것).

### 3-2 customerId(ccc id)로 보유 시술권
- 지금 lookup(`service/ext.py:218-236`): `find(name, email)`(내부 이름 검색 1번) → `_keep()` 으로 ccc id 를 정함 → 공개 `ticket/open/v1/queries/get-ticket-bundles {visitorId: KOS id}` 1번(`:226`).
- 시술권 호출에 필요한 값은 **KOS 고객 id 하나뿐**이다. ccc `customer.id` → `customer.kos_id`(`db.py:18-21`)를 사본에서 바로 바꾸면 이름 · 이메일 검색 없이 탈 수 있다(B). KOS 호출 = **1번**(지금 lookup 의 2번에서 이름 검색이 빠짐).
- 데모(확인): 공개 시술권 5명 200 · 49~167ms · 묶음 있음 2명(3 · 1) · 결과 없음 3명(본문 `{}` · `data` 키 없음). [문서](https://developers.kos-solution.com/docs/openapi/ticket#getTicketBundlesQuery)
- 함정: ccc id 는 사본에 있는 고객만 된다(lookup · 검색 · 날짜 조회로 사본에 들어온 고객). 이름 + 이메일을 받지 않으면 DEC-010 의 「둘 다 맞아야 고객을 연다」(열거 방지) 규칙이 이 경로에는 걸리지 않는다. ccc id 는 1부터 차례로 붙는 정수라 키만 있으면 차례로 넣어 볼 수 있다(정할 것).

### 3-3 시술권 「사용 중」 장수
- 지금 계산(`ext.py:238-252`): `remainingCount` = 묶음 안 `status == AVAILABLE` 장수 · `totalCount` = 묶음 안 장수 전부(`:250`).
- KOS 칸: 시술권 `tickets[].status` enum = `AVAILABLE · USED · CANCELED · IN_USE · TicketStatus_UNSPECIFIED`(스펙). **`IN_USE` 가 「사용 중」이다.**
- **공개 조회에는 사용 중인 장이 안 온다**(확인): 일정 작업에 시술권이 붙어 있고 그 작업이 아직 안 끝난(`NOT_STARTED` · `WAITING` · `READY`) 장이 있는 고객 2명은 공개 묶음 결과가 `{}` 였다. 붙은 시술권 id 는 공개 묶음에 0건이었다. 공개 묶음이 준 장은 전부 `AVAILABLE`(4장)이다. 스펙 요약도 「사용 가능한 시술권 묶음 목록」이다. 앞 조사(`research-purchase-snapshot.md` §179)에 따르면 묶음은 `AVAILABLE` 이 1장 이상 있을 때만 오고, 그 안의 `USED` 는 보인다. `AVAILABLE` 이 섞인 묶음 안에 `IN_USE` 장이 보이는지는 **확인 안 됨**(그런 고객을 못 찾았다).
- **내부 조회에는 온다**(HAR): `상담대기.har` #8 내부 `ticket/v1/queries/get-ticket-bundles {visitorId, sort}` → 묶음 5개 · 장 상태 `IN_USE`. 칸 모양은 공개와 같다(`optionConfiguration` · `ticketSets[].tickets[]{id, status, price, createdDateTimeUtc}`).
- 분류: **C**(내부). KOS 호출 = 내부 1번(공개 대신 바꾸면 그대로 1번).
- 함정: 지금 `totalCount` 는 공개 묶음 안 장수라 사용 중 장을 세지 않는다. 사용 중 장만 남은 묶음은 지금 lookup 응답에서 **통째로 빠진다**(「시술권 없음」으로 보임).

### 3-4 시술권 만료일 · 차감
- **만료일**: 시술권 · 세트 · 묶음 어디에도 만료 칸이 없다(스펙 `getTicketBundlesQuery` 전체 · 공개 확인 · 내부 HAR 키 전수). 만료 칸은 선불카드에만 있다(3-5). → **E**. 발행일은 있다: `tickets[].createdDateTimeUtc`, 지금 `purchasedDate`(`ext.py:243-251` · 묶음 안 가장 이른 발행일)가 이 값이다(A).
- **차감(KOS 쓰기)**: KOS 에 「시술권 차감」 작업은 따로 없다. **일정에 시술 작업을 넣으면서 시술권을 붙이는** 꼴이다(HAR · 쓰기 안 함).
  - `상품 수납.har` #68 · `고객예약접수시술.har` #117: 내부 `schedule/v1/commands/add-flow-tasks {scheduleId, tasks[{type: PROCEDURE, title, procedureConfiguration{productOptionConfiguration{…}, ticketConfiguration{ticketId, round{total, current}}, medicalServiceConfiguration{…}}, translsMap}]}` → `{}`
  - 일정 응답 작업에도 같은 `ticketConfiguration{ticketId, round}` 가 남는다(공개 확인: 작업 244개).
  - 작업 상태 ↔ 시술권 상태: 작업을 넣으면 `IN_USE`(HAR · 내부 묶음). 작업 `DONE` → `USED` · `CANCELED` → 대개 `AVAILABLE`(앞 조사 §172 · 7/7 · 4/5)이다(추정 · 이번에 다시 보지 않음).
  - 공개 스펙에 작업을 넣는 쓰기는 없다(스펙 81개 중 `add-flow-tasks` 에 해당하는 것 없음).
- 지금 CC 코드에는 작업 추가 · 시술권 차감 쓰기가 없다(`service/` grep: `add-flow-tasks` 0건).
- 분류: 차감 **C**. 호출 = 작업 1개당 내부 1번(한 요청에 `tasks[]` 여러 개를 실은 HAR 도 있다 · `상품 수납.har` #68 = 2개).
- 함정: 차감은 「시술 작업이 생긴다」는 뜻이다. 시술 현황판 · 수납 필요 수 · 원장 호출에 바로 보인다. `productOptionConfiguration` · `medicalServiceConfiguration` 본문은 메뉴 사본(`menu_*`)으로 짜야 하고, KOS 웹이 보내는 다국어 `translsMap` 까지 맞춰야 하는지는 **확인 안 됨**.

### 3-5 선불카드 잔액 · 만료일
- 공개 2개(B):
  - [getPrepaidCardSummaries](https://developers.kos-solution.com/docs/openapi/prepaidcard#getPrepaidCardSummaries) `purchase/open/prepaid-card/v1/queries/get-prepaid-card-summaries {visitorId*, available?}` → 카드별 `id · title · description · createdDateTimeUtc · expirationDateTimeUtc*(만료 일시) · ownerId · remainingBalance{balance, total} · remainingPoint{balance, total} · updatedDateTimeUtc`. `available=true` 면 「만료되지 않았고 잔액이 남은 카드만」(스펙).
  - [getVisitorPrepaidCardBalance](https://developers.kos-solution.com/docs/openapi/prepaidcard#getVisitorPrepaidCardBalance) `…/get-visitor-prepaid-card-balance {visitorId}` → 사용 가능한 카드 합산 `remainingBalance` · `remainingPoint` · 마지막 충전 시각
- 데모(확인 · 5명): 목록 200 · 카드 1장 1명 · 0장 4명 · 39~266ms. 합산 5명 200 · 키 2~3개.
- 내부(HAR): `상담대기.har` #27 · #28 도 같은 이름의 내부 경로 `purchase/prepaid-card/v1/queries/…` 를 쓴다.
- 지금 CC 코드에는 없다. KOS 호출 = 1번(목록에 만료 · 잔액이 다 있음) 또는 2번(합산까지).
- 함정: 잔액은 현금 · 포인트 두 갈래이고 각각 `balance` · `total` 이 있다. 카드마다 만료일이 다르다.

### 3-6 예약의 희망 시술 · 예산 · 동행자 · 원장 상담 지정 · 통역 필요

| 칸 | KOS | CC | 분류 |
|---|---|---|---|
| 희망 시술 | `reservation.requestedProcedures[]`(스펙 「희망 시술 목록」 · 필수 배열). 원소 `type`(`OPTION` · `TICKET`) + `optionConfiguration{optionId, optionTitle, productTitle, price, …}` 또는 `ticketConfiguration{ticketId, ticketTitle, …}`. 통계에도 `requestedOptionTitles` · `requestedProductOptionTotalPriceV2`(희망시술 옵션 총액)가 있다 | 사본에 안 담음 · 예약 생성이 보내지 않음 | **B** |
| 원장 상담 지정 | `reservation.doctor`(스펙 「희망 의사」) · 통계 `requestedDoctorName(s)` | 예약 생성은 `doctors: []` 만(`reservations.py:833`) | **B**(칸 있음 · 데모 값 0) |
| 희망 상담사 | `reservation.counselor`(스펙 「희망 상담사」) | 사본 `counselor` · 예약 생성 `counselorStaffId` | A(2-1 참고) |
| 예산 | 없음(스펙 · 응답 키 검색) | 없음 | **E/D** |
| 동행자 | 없음 | 없음 | **E/D** |
| 통역 필요 | 없음 | 없음(데모 가짜 데이터 문구에만 나옴 · `fake_board.py:14` · `fake_reservations.py:77`) | **E/D** |
| 내원객 요청사항 | `visitorRequest`(스펙 · 일정 상세 · 예약 쓰기 `reserveByTimeSlot*`) | 없음 | B(스펙 · 데모 응답에는 키가 안 옴) |

- 데모(확인 · 162건): `requestedProcedures` 가 빈 배열 159 · 원소 있음 3(`OPTION` 3 · `TICKET` 1). `reservation.doctor` 는 162건 모두 빈 값.
- 문진: 공개 문진 제출본의 답(`answers[]`)은 병원이 만든 양식 질문에 대한 답이다. 「예산 · 동행자 · 통역」 같은 질문이 양식에 있는지는 양식마다 다르고, CC 는 「건강 정보」 쪽만 읽는다(`domain/reservation_rules.py:311-317`). 이번에는 양식 질문 목록을 보지 않았다(**미확인**).
- KOS 호출 수: 희망 시술 · 희망 의사는 일정 응답 안에 있다. 날짜 조회(내부)나 고객 일정(공개)에서 같이 받으므로 0번 추가다. 다만 지금 사본은 `requestedProcedures` 를 버린다(`reservation_fields` 에 없음).

### 3-7 진단기 · 날짜(그날 피부 진단)
- KOS: 스펙에 진단 · 진단기 작업이나 칸이 없다(`diagnos` · `skin` 검색 0건 · `machine` 은 시술 기기 목록 `getMachines` 뿐). HAR 에도 없다.
- CC: 없다. → **E**. 다른 시스템(진단기 업체)에서 오는 값이라면 이 조사 범위 밖이다.

### 3-8 열람 기록(연 직원 · 고객 · 시각)
- 지금 표 `ext_call`(`repository/db.py:287-295`): `id · at · client(linky|charty|null) · endpoint("<METHOD> <경로 틀>") · status · outcome`. 설계상 **이름 · 이메일 · 키 · IP · 고객 · 예약 id 를 싣지 않는다**(같은 줄 주석 · `service/ext.py:5` · SPEC-008 §3.4 · DEC-010). 쓰기 = `ExtService.record()`(`ext.py:103-116`) → `tx.add_ext_call`(`repo.py:519-521`).
- 직원 행위 표 `event_log`(`db.py:71-74`): `id · at · actor(직원 login_id 또는 "ext:<연동처>") · type · visit_id · payload(JSON)`. `_event()`(`reservations.py:478-480`)가 쓴다. 외부 예약은 이미 `actor = "ext:charty"` 로 남는다(`ext.py:282`). 지금은 **조회(열람)는 남기지 않고 조작만** 남긴다.
- 직원 id 를 받으면 붙일 수 있는 자리(사실만): ① `ext_call` 에 열을 더한다(지금 설계 원칙과 부딪힘). ② `event_log` 에 `type` 을 새로 두고 `payload` 에 직원 · 고객을 싣는다(열 추가 없음). ③ 새 표. centurion 통합 계정의 직원 id 와 ccc `staff` · `account` 의 관계는 이번에 보지 않았다(**미확인**).
- 분류: 틀은 **A**, 내용은 **D**.

### 3-9 지난 방문의 상담자
- 원천 호출: 직원 `previousVisits[]` · ext `visits` 는 둘 다 공개 `get-schedules-by-visitor` 1번이다(`reservations.py:594` · `ext.py:351`).
- 그 응답 원소에 상담자가 **있다**(확인 · 5명 일정 27건): `consultation.counselor{id, name}` 채워짐 12/27 · `consultations[]` 원소 12개(`counselors[]{id, name}` · `consultationDoctors[]` · `consultationStartedDateTimeUtc` · `content.text` · `result`). 예약 쪽 `reservation.counselor`(희망 상담사)는 7/27.
- 지금 코드는 안 꺼낸다: `previous_visits()`(`:205-215`)는 날짜 · 결과 · 구역 · 그룹 · 예약 메모 · 상담 메모 · 시술(의사 이름)만 낸다. ext `visits()`(`ext.py:379-380`)는 날짜 · 시작 · 결과 · 시술 이름만 낸다.
- 분류: **B**. KOS 호출 0번 추가(같은 응답).
- 함정: `consultations[].content.text` 는 상담 내용 원문이다. DEC-011 D-03 「상담 메모 · 의사 이름은 내지 않는다」와 같은 판단이 상담자 이름 · 상담 의사에도 걸리는지 정해야 한다.

---

## 4. 오더 메모 · 차트 메모 등록 · 수정 (실호출 안 함)

### 4-1 오더 메모
- **쓰기(C · HAR)**: `2026-11-09-cc-day/har/고객예약접수시술.har` #127 내부 **`schedule/v1/commands/change-order-memo`** `{scheduleId: uuid, orderMemo: str}` → 200 `{}`. 일정 단위 글 하나이고 통째로 바꾼다(추정 · 칸이 하나뿐). 공개 스펙에는 오더 메모 쓰기가 **없다**(81개 중 0).
- **읽기**: 일정 `orderMemo`(스펙 「오더 메모」 · 공개 `getScheduleDetail` · `getSchedulesByFlowStep` · `getSchedulesByVisitor` · 내부 `get-schedule-detail`). 데모(확인): 162건 중 값 있음 88. CC 는 **시술 현황** 사본 `visit.order_memo` 에 이미 담는다(`kos/sync.py:106` · 내부 `get-schedules-grouped-by-zone` 10초 조회 · 오늘 · `KOS_ZONE_ID` 구역만 · `schemas/board.py:180`). 예약 사본 `reservation` 에는 오더 메모 열이 없다.
- **수정 id**: KOS 일정 id(`scheduleId`) 하나다. ccc `reservationId` → 사본 `reservation.kos_id` 로 바꾸면 된다.
- 지금 CC 쓰기: 없다.
- 호출 수: 1번.

### 4-2 차트 메모
- **쓰기(C · HAR)** — 작업(sequence) 단위 글 두 칸이다. DAY 조사 `research-har-room-chart-report.md` §3 과 같고, 이번에 `차트작성3.har` 도 확인했다.
  - 간호 · 담당자 메모: 내부 `schedule/v1/commands/change-flow-tasks-assignee-memo {scheduleId, sequences: [int], assigneeMemo: str}` → `{}`(`차트작성.har` #39 · `차트작성2.har` #5)
  - 의사 메모: 내부 `schedule/v1/commands/change-flow-tasks-doctor-memo {scheduleId, sequences: [int], doctorMemo: str}` → `{}`(`차트작성.har` #48 · `차트작성2.har` #7 · `차트작성3.har` #26 · #32)
  - 같은 화면에서 담당자 · 집도의를 따로 바꾼다: `schedule/flow/v1/commands/change-tasks-assignees {…, assigneeIds}` · `change-tasks-doctors {…, doctorIds}`(`차트작성3.har` 은 `doctorIds` 2개도 보냄 · #23). `차트작성3.har` #15 에는 `change-tasks-complete {scheduleId, sequences, complete: bool}` 도 있다.
  - 고쳐 쓰기 = 통째로 바꾸기다(두 번째 글이 첫 글로 시작 · DAY 조사 §3-1). 작성자 칸은 본문에 없다(토큰 주인).
- **읽기**: 일정 `tasks[].assigneeMemo` · `tasks[].doctorMemo`(공개 일정 응답 · 확인: 작업 519개 중 값 있음 13 · 14). 내부 `get-schedule-summaries` 에도 있다(`상담대기.har` #9).
- **수정 id**: `scheduleId` + 작업 `sequence`. sequence 는 일정 응답 `tasks[].sequence` 다. 사본 `reservation.tasks[].sequence` · 시술 현황 `procedure.kos_sequence` 에 이미 있다.
- 지금 CC 코드: 읽기 · 쓰기 다 없다(`assigneeMemo` · `doctorMemo` grep 0건).
- 호출 수: 메모 칸 1개당 1번. 담당자 · 집도의까지 함께 바꾸면 2~3번(원자 아님).
- **「차트 메모」가 무엇을 가리키는지는 하나로 정해지지 않는다.** KOS 웹 「고객 차트」 화면(`opened.visitor_chart` · `상담대기.har` Amplitude)에는 고객 단위 `memo`(= CC 「특이사항」 4-4)도 있다. charty 가 말한 「차트 메모」가 ⓐ 작업 메모(위)인지, ⓑ 고객 특이사항인지, ⓒ 상담 메모(4-5)인지 정해야 한다.

### 4-3 ~ 4-5 지금 CC 의 메모 쓰기와의 관계

| 메모 | 단위 | CC 직원 API | KOS 쓰기 | 근거 |
|---|---|---|---|---|
| 예약 메모 | 일정 | `PUT /api/reservations/{id}/memo`(`api/reservations.py:316`) | **공개** `schedule/open/v1/commands/change-reservation-memo {scheduleId, memo}` · 끝난 예약은 409 · 같은 값이면 안 부름 · `event_log resv_memo` | `service/reservations.py:997-1008` · [changeReservationMemo](https://developers.kos-solution.com/docs/openapi/schedule#changeReservationMemo) |
| 고객 특이사항 | 고객 | `PUT /api/customers/{id}/remark`(`api/reservations.py:509`) | 내부 `get-visitor` 다시 읽기 → 내부 `visitor/v2/commands/update-visitor-management-information`(관리 묶음 13키 전체 + `memo`) · `event_log visitor_remark` | `:1086-1107` · `MANAGEMENT_KEYS :1170` |
| 상담 메모 | 일정 | 없음 | **공개** `schedule/open/v1/commands/update-schedule-consultation-info {scheduleId*, consultationMemo}` | [updateScheduleConsultationInfo](https://developers.kos-solution.com/docs/openapi/schedule#updateScheduleConsultationInfo) |
| 오더 메모 | 일정 | 없음 | 내부 `change-order-memo`(4-1) | HAR |
| 작업 메모 2종 | 작업 | 없음 | 내부 `change-flow-tasks-*-memo`(4-2) | HAR |

- 오더 메모는 예약 메모와 **다른 칸**이다(`reservation.reservationMemo` ↔ 일정 `orderMemo`). 직원 API `memo` 경로를 그대로 다시 써서는 안 된다.
- 고객 특이사항은 1-3 과 같은 「다시 읽고 묶음 전체 보내기」라, 같은 경합 위험이 있다(관리 묶음 13키).

---

## 5. 묶어 보기 — 가안 다시 그리기 (결정 아님 · 사실 정리)

가안: 「기존 `lookup` 에 필드 추가 + 새 ext 5개(board · 예약 상세 · 고객 언어 · 오더 메모 · 차트 메모)」.

| 엔드포인트(가안) | 담을 칸 | 원천 | KOS 호출(요청 1번) | 이 조사로 드러난 것 |
|---|---|---|---|---|
| 기존 `POST /customers/lookup` + 칸 | 시술권(남은 · **사용 중** · 발행일) · 선불카드(잔액 · 만료) | 이름 검색(내부) 1 + 시술권 1 + 선불카드 1~2 | **2 → 3~4**. 사용 중까지 세려면 시술권을 공개 → **내부**로 바꿔야 한다(3-3) | 시술권 만료일은 KOS 에 없다(3-4). customerId 로 찾는 갈래를 더하면 이름 검색이 빠져 1~3번이 된다(3-2) |
| 새 board | 예약별 시작 · 끝 · 고객(ccc id · 이름 · 국적 · 신규) · 상태 · **접수 시각** · **담당(희망) 상담사** · **관리실** · 상담 여부(CC 판정) · (희망 시술) | 사본 `reservation`(날짜 조회) | **0번**(10초 캐시가 낡으면 날짜당 3~4번) | 2-1 · 2-2 · 2-4 는 사본 열에 이미 있다. 희망 시술은 사본이 버려서 날짜 조회 응답을 저장해야 한다. **처음 상담 대기 시각(2-3)은 원천이 없다** — 통계 계산(공개 +1번 · 분 단위 · 추정)이나 CC 저장이나 HAR 추가 중 하나 |
| 새 예약 상세 | 기본 정보 · 언어 · 문진 · 이전 방문(+상담자) · 예약 메모 · 귀가 희망 · 유입 · 희망 시술 · 희망 의사 | 사본 + 일정 상세(내부) + 고객(내부) + 문진(공개 2) + 고객 일정(공개) | **5번**(+ 날짜 조회) | 언어 · 특이사항 · 고객 유입은 **내부 전용**이다. 이전 방문의 메모 · 의사를 내면 DEC-011 D-03 과 부딪힌다. 지난 방문 상담자는 같은 응답에 있다(3-9) |
| 새 고객 언어(쓰기) | `language` 하나 | 내부 다시 읽기 + 내부 개인 묶음 쓰기 | **2번**(같은 값이면 1) | 묶음 전체를 다시 보내므로 경합 시 다른 칸을 덮는다(1-3). ext 처음 쓰기 경로 + KOS 쓰기 |
| 새 오더 메모(쓰기) | `orderMemo` 전체 | 내부 `change-order-memo` | **1번** | 공개 쓰기 없다. 읽기는 일정 응답에 있음. 예약 메모와 다른 칸 |
| 새 차트 메모(쓰기) | 작업마다 `assigneeMemo` · `doctorMemo` | 내부 `change-flow-tasks-*-memo` | **칸 1개당 1번** | id = 일정 id + 작업 sequence. 「차트 메모」가 무엇인지(작업 메모 · 고객 특이사항 · 상담 메모) 먼저 정해야 한다 |
| (가안 밖) 시술권 차감 | 작업 + `ticketConfiguration` | 내부 `add-flow-tasks` | 1번 | 「charty 가 차감할 시술권을 골라 넘긴다」를 KOS 에 반영하려면 **시술 작업 생성**이 필요하다(3-4) |
| (가안 밖) 열람 기록 | 연 직원 · 고객 · 시각 | CC 저장 | 0번 | `ext_call` 원칙(고객 id 없음)과 부딪힌다(3-8) |

내부 API 의존 정리: 지금 ext 6개 중 내부를 쓰는 것은 이름 검색 하나다. 가안을 다 넣으면 내부 의존이 일정 상세 · 고객 · 시술권(사용 중) · 개인 묶음 쓰기 · 오더 메모 쓰기 · 작업 메모 쓰기까지 늘어난다. **ext 에서 KOS 쓰기가 처음으로 3종 생긴다**(지금 ext 의 쓰기는 예약 생성뿐이다).

---

## 6. 정할 것 (결정하지 않고 모음)

1. **「처음 상담 대기 시각」의 원천**(2-3) — ⓐ KOS 「예약 이력」 탭을 연 HAR 을 받아 내부 이력 조회를 찾는다. ⓑ 공개 통계 「접수 시각 + 접수 체류 분」으로 계산한다(분 단위 · 곧장 간 경우만 맞음 · 추정). ⓒ CC 가 단계 변화를 본 시각을 따로 쌓는다(KOS 웹 조작은 최대 10초 늦음 · CC 를 켜기 전 값 없음). ⓓ 지금처럼 「지금 단계 시각」.
2. **「담당 상담사」의 뜻**(2-1) — 예약 `reservation.counselor`(KOS 「희망 상담사」 · 우리 schema 는 「담당 상담사」로 적음) vs 실제 상담 `consultation.counselor` · `consultations[].counselors[]`. 데모에서 둘이 다른 일정 3건 · 실제만 있는 일정 30건.
3. **「상담 여부」 판정**(3-1) — CC 판정(이벤트 · 지금 단계)만 쓸지, KOS `consultations[]` · 통계 상담 체류를 보탤지. KOS `consultationRequired` 는 데모에서 실제와 106/162 어긋난다.
4. **「차트 메모」가 무엇인가**(4-2) — 작업 메모(간호 · 의사) · 고객 특이사항 · 상담 메모 중 무엇인지. charty 에 되물을지.
5. **시술권 사용 중**(3-3) — 사용 중을 세려면 공개 → 내부 시술권 조회로 바꿔야 한다. 내부 의존을 늘릴지. 지금 lookup 이 「사용 중만 남은 묶음」을 통째로 빠뜨리는 것을 고칠지.
6. **시술권 만료일**(3-4) — KOS 에 없다. 발행일로 대신할지 · 칸을 비울지 · 메뉴(상품) 쪽 유효기간 규칙이 있는지 더 볼지.
7. **시술권 차감을 받을지**(3-4) — 받으면 ext 가 KOS 에 시술 작업을 만든다(시술 현황 · 수납 · 원장 호출에 바로 보임). 작업 본문(옵션 · 진료항목 · 다국어)을 메뉴 사본으로 짜야 한다.
8. **customerId 로 여는 경로의 열거 방지**(3-2) — 이름 + 이메일 없이 ccc id 만으로 시술권 · 상세를 열면 DEC-010 「둘 다 맞아야 연다」가 이 경로에 걸리지 않는다. ccc id 는 차례 정수다.
9. **이전 방문 · 상세에 메모 · 의사 · 상담자를 낼지**(1-2 · 3-9) — DEC-011 D-03(메모 · 의사 미노출)과 같은 기준을 상담자 · 상담 내용에도 걸지.
10. **열람 기록의 자리**(3-8) — `ext_call` 에 고객 · 직원을 싣지 않는 원칙을 바꿀지, `event_log` 새 type 으로 둘지, 새 표를 만들지. centurion 직원 id 와 ccc 계정을 어떻게 잇는지.
11. **예산 · 동행자 · 통역 필요**(3-6) — KOS · CC 둘 다 칸이 없다. CC 에 새로 저장할지 · 예약 메모 같은 글에 넣을지 · 문진 양식 질문으로 받을지(양식 질문 목록은 미확인).
12. **고객 언어 쓰기의 덮어쓰기 위험**(1-3) — 묶음 전체 교체 + 읽기 · 쓰기 사이 경합을 받아들일지.
13. **board 의 신선도 · 부분 실패**(1-1 · 1-2) — 10초 캐시 값 · 날짜 조회 실패 때 낡은 사본 · 상세 일부 실패를 ext 에서 어떻게 보일지.
14. **원천이 둘인 칸** — 고객 유입(예약 `funnel` vs 고객 `visitorFunnel`) · 상담사(희망 vs 실제) · 접수 시각(일정 vs 통계 · 데모에서는 147/147 같음) · 오더 메모(시술 현황 사본 = 4층 · 오늘만 vs 일정 응답).

---

## 7. 미확인 (사유)

- **내부 API 실호출 0건** — 내부 토큰 발급 `sign-in` 이 `/commands/` 경로라 브리프 §7 에 따라 부르지 않았다. 그래서 내부 시술권 조회의 `IN_USE` 칸 · 내부 고객 `language` 값 꼴은 HAR 로만 봤다.
- 단계 이력 조회 — HAR · 스펙에 없다. KOS 웹 「예약 이력」 탭 HAR 이 필요하다.
- `AVAILABLE` 이 섞인 공개 묶음 안에서 `IN_USE` 장이 보이는지 — 그런 고객을 못 찾았다.
- 통계 체류 분이 같은 단계를 두 번 거칠 때 합쳐지는지 — 문서에 없다.
- 개인 묶음 쓰기에서 보내지 않은 키를 KOS 가 비우는지 — 쓰기 금지 · HAR 없음.
- 문진 양식에 예산 · 동행 · 통역 질문이 있는지 — 양식 질문 목록을 보지 않았다.
- 시술권 작업 `CANCELED` → 시술권 상태 — 앞 조사 값(4/5)을 옮겼고, 이번에는 다시 보지 않았다.

## 8. 호출 기록

| 대상 | 수 | 비고 |
|---|---|---|
| 공개 토큰 교환 | 1 | 데모 키(`KOS_API_tenent_dev`) |
| 공개 조회 | 32 | `getSchedulesByFlowStep` 7 · `getScheduleStatistics` 2 · `getTicketBundlesQuery` 5 · `getSchedulesByVisitor` 5 · `getPrepaidCardSummaries` 5 · `getVisitorPrepaidCardBalance` 5 · `getScheduleDetail` 1 · `getVisitor` 2(1번은 본문 키 오류 400) |
| 내부 · 쓰기 | 0 | |

원 응답은 scratchpad 에만 두었다(레포 밖). 실제 지점 키 · 운영 서버 · 클러스터 · 사용자 포트에는 닿지 않았다.
