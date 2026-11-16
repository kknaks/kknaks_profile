# 예약 이동 · 취소 · 부도 · 취소 되돌리기 — HAR 5개 + 데모 쓰기 시험

- 조사 · 시험일: 2026-10-26 (KST) · 조사자: cc-prototype researcher (task_dacee03f38c8)
- 앞 판 `reservation-memo-test-report.md` 에서 이어진다
- 원천
  - `reference/2026-10-23-cc-overall-board/har/` 의 `예약이동.har`(12) · `예약상세_수정.har`(34) · `예약취소.har`(33) · `예약부도.har`(11) · `예약취소_되돌리기.har`(15) — gitignore
  - KOS 예약 화면 JS `reservation-client_v0.0.540`
  - 공개 스펙 openapi.yaml 1.0.1
- 데모 쓰기 허가: 지시서 §3-6. 테넌트 · 키는 스크립트 `assert` 로 확인했다(테넌트 = 데모, 키 = `KOS_API_tenent_dev` ≠ 운영 키)
  - 이번 실행의 허가 경로는 공개 `update-reservation(v2)` · 공개 `cancel-reservation` · 내부 `revoke-canceled-reservation` **셋으로 좁혔다**
- 표기
  - **확인**: HAR · 데모로 본 것
  - **JS**: 웹앱 코드
  - **스펙**: openapi.yaml
  - **추정**: 해석
- 리포트에 id · 이름 · 토큰 값은 적지 않았다

---

## 0. 결론

| 조작 | KOS 쓰기 | 공개 짝 | 데모 시험(1회씩) |
|---|---|---|---|
| **이동**(시각 · 그룹) | 내부 `schedule/reservation/v2/commands/update-reservation{scheduleId, occupiedResources{items[…]}}` | **`updateReservationV2{scheduleId*, zoneId*, occupiedResources*[…]}`** | 공개로 보냄 → 200. 바뀐 것은 시각 · 그룹 · 일정 묶음뿐이고 메모 · 유입 · 담당 · 상담은 그대로 |
| **취소** | 내부 `schedule/reservation/v1/commands/cancel-reservation{scheduleId, reason:"CANCELED"}` | **`cancelReservation{scheduleId*, reason*}`** | 공개로 보냄 → 200. `reservation.status RESERVED → CANCELED`, **flowStep 은 `RESERVED` 그대로** |
| **부도** | 같은 작업 · `reason:"NO_SHOW"` | 같은 `cancelReservation` | 공개로 보냄 → 200. `status → NO_SHOW`, flowStep 그대로 |
| **취소 되돌리기** | 내부 `schedule/reservation/v1/commands/revoke-canceled-reservation{scheduleId}` | **공개 없음** | 내부로 보냄 → 200. `CANCELED → RESERVED`, 수정 시각 말고는 취소 전과 같다 |

- **취소와 부도는 `reason` 하나로 갈린다**(`CANCELED` / `NO_SHOW`)
- **이동은 부분 수정이다.** 내부 · 공개 모두 일정 묶음(`occupiedResources`)만 보낸다. 다른 예약 필드는 지워지지 않았다(HAR 과 시험 둘 다 확인)
- **접수된(`RECEPTION`) 일정도 이동된다**(HAR: 사용자가 앞 판 시험 B 일정을 옮겼다)
- 내부 상세 수정은 30분 칸이 아닌 **55분(09:35 ~ 10:30)** 으로도 저장됐다(확인)
- 정할 것은 **9개**다(Q-83 ~ Q-91)

---

## 1. HAR 인벤토리

5개 파일의 항목 105개 = KOS API 69 + KOS 정적(js 1) + OPTIONS 2 + Datadog 25 + Amplitude 8. 아래는 **KOS API 69건 전부**다. 모두 POST · `api.kos-solution.com/tenants/{tenantId}/…` 이다.

### 1.1 `예약이동.har` — KOS API 5건 (05:49:19 ~ 22.7)

화면: 예약 현황 판(`/reservation`)의 이동 버튼.

| # | 경로 | 본문 키 | 응답 |
|---|---|---|---|
| 0 | `role/v2/queries/get-roles` | — | (15) |
| 1 | `visitor/v2/queries/get-visitor` | `id` | `data{고객}` |
| 4 | `schedule/group/v1/queries/get-reservation-group` | `id` | 이동 전 그룹(「국내」) |
| **7** | **`schedule/reservation/v2/commands/update-reservation`** | `scheduleId · occupiedResources{items:[{id, type:RESERVATION_GROUP, reservationTime{startDateTimeUtc, endDateTimeUtc}, reservationGroup{reservationGroupId, zoneId}}]}` | `{}` |
| 9 | `get-reservation-group` | `id` | 이동 뒤 그룹(「중화권」) |

대상은 앞 판 시험 B 일정(접수 상태)이다. 「국내」 → 「중화권」, 시각은 같은 칸(17:30 ~ 18:00 KST)이다.

### 1.2 `예약상세_수정.har` — KOS API 22건 (05:49:39 ~ 52.2)

화면: 예약 현황 → 고객 상세(`/reservation/schedule/?visitorId&scheduleId`) → 예약 탭에서 저장.

| # | 경로 | 본문 키 | 응답 |
|---|---|---|---|
| 0 · 1 · 3 | `get-roles` · `get-visitor` ×2 | | |
| 4 | `schedule/v1/queries/get-payment-required-tasks` | `visitorId` | (0) |
| 5 | `schedule/v1/queries/get-schedule-detail` | `scheduleId` | `data{일정}` — **수정 전: `RECEPTION` · `IN_PROGRESS`** |
| 6 | `get-accounts-last-update…` | | |
| 7 | `get-reservation-group` | `id` | 「중화권」 |
| 8 · 15 | `get-codes FUNNEL_CATEGORY` | | (0) |
| 9 · 14 | `get-codes FUNNEL` | | (13) |
| 10 | `procedure-menu/visitors/queries/get-visitors` | `sort` | (0) |
| 11 | `get-codes CONSULTATION_RESULT` | | (8) |
| 12 | `consultation/v1/queries/get-consultations-by-visitor-id` | `visitorId` | (0) |
| 13 | `visitor/questionnaire/v1/queries/get-questionnaire-submit/legacy` | `visitorId` | **200**(이 고객은 앞 판에서 문진을 제출했다) |
| 16 · 17 | 선불카드 2 | `visitorId` | |
| 18 | `get-schedule-summaries` | `visitorId · sort` | (5) |
| 19 | `ticket/v1/queries/get-ticket-bundles` | `visitorId · sort` | `{}` |
| **29** | **`schedule/reservation/v2/commands/update-reservation`** | #7 과 같은 키 · 같은 `occupiedResources[].id` | `{}` |
| 30 | `get-reservation-group` | `id` | 「중화권」 |
| 31 | `get-accounts-last-update…` | | |

대상은 같은 시험 B 일정이다. 그룹은 그대로 두고 시각을 **09:35 ~ 10:30Z(55분)** 로 바꿨다.

### 1.3 `예약취소.har` — KOS API 22건 (05:50:46 ~ 51.1)

화면: 고객 상세 → [예약 취소] → 「고객 의사 취소」.

| # | 경로 | 본문 키 | 응답 |
|---|---|---|---|
| 1 · 3 · 5 | `get-roles` · `get-visitor` ×2 | | |
| 6 | `get-payment-required-tasks` | | (0) |
| 7 | `get-schedule-detail` | `scheduleId` | **취소 전: `RESERVED` · `RESERVED`** |
| 8 · 29 | `get-accounts-last-update…` | | |
| 9 · 28 · 31 | `get-reservation-group` | `id` | |
| 10 · 16 | `get-codes FUNNEL_CATEGORY` | | |
| 11 · 15 | `get-codes FUNNEL` | | |
| 12 | `procedure-menu/visitors/…/get-visitors` | | |
| 13 | `get-consultations-by-visitor-id` | | |
| 14 | `get-questionnaire-submit/legacy` | | 400 |
| 17 · 18 | 선불카드 2 | | |
| 19 | `get-schedule-summaries` | | (2) |
| 20 | `get-ticket-bundles` | | |
| **26** | **`schedule/reservation/v1/commands/cancel-reservation`** | `scheduleId · reason:"CANCELED"` | `{}` |

대상은 앞 판 신규 고객(`예약.har` #147)이 따로 가진 오늘 18:30 KST 일정이다(사용자가 만든 것으로 보인다).

### 1.4 `예약취소_되돌리기.har` — KOS API 12건 (05:51:08.7 ~ 12.8)

| # | 경로 | 본문 키 | 응답 |
|---|---|---|---|
| 0 · 1 · 2 · 3 | `get-roles` · `get-reservation-group` · `procedure-menu/visitors/…` · `get-schedule-summaries` | | #3: 대상 일정 **`RESERVED` · `RESERVED`** |
| **5** | **`cancel-reservation`** | `scheduleId · reason:"CANCELED"` | `{}` |
| 6 · 8 | `get-reservation-group` | | |
| 7 | `get-accounts-last-update…` | | |
| **10** | **`schedule/reservation/v1/commands/revoke-canceled-reservation`** | `scheduleId` | `{}` |
| 11 · 14 | `get-reservation-group` | | |
| 12 | `get-accounts-last-update…` | | |

1.3 과 같은 일정이다. 1.3 에서 취소된 일정이 이 파일 #3 에서는 다시 `RESERVED` 였다. 두 HAR 사이(05:50:54 ~ 05:51:08)에 한 번 더 되돌리기가 있었던 것으로 보인다(HAR 에 없음, 추정).

### 1.5 `예약부도.har` — KOS API 8건 (05:51:23.7 ~ 25.7)

| # | 경로 | 본문 키 | 응답 |
|---|---|---|---|
| 0 · 1 · 2 · 3 | `get-roles` · `get-reservation-group` · `procedure-menu/visitors/…` · `get-schedule-summaries` | | #3: 대상 `RESERVED` · `RESERVED` |
| **6** | **`cancel-reservation`** | `scheduleId · reason:"NO_SHOW"` | `{}` |
| 7 · 9 | `get-reservation-group` | | |
| 8 | `get-accounts-last-update…` | | |

1.3 · 1.4 와 같은 일정이다. 지금 데모에서 조회하면 `RESERVED` · **`NO_SHOW`** 다(확인).

**합계**: 5 + 22 + 22 + 12 + 8 = **69** — KOS API 69건과 같다. 쓰기는 6건이다(#7 · #29 · #26 · #5 · #10 · #6).

---

## 2. `update-reservation` 해부 (이동)

### 2.1 내부 두 건 비교

| | 이동 버튼(`예약이동` #7) | 상세 수정(`예약상세_수정` #29) |
|---|---|---|
| 본문 키 | `scheduleId · occupiedResources{items[1]}` | **같다** |
| `items[0].id` | 기존 일정 묶음 id | 같은 id(그대로 둔다) |
| 바꾼 것 | 그룹(국내 → 중화권) | 시각(30분 → 55분, 09:35 ~ 10:30Z) |
| `zoneId` · 메모 · 담당 · 상담 · 유입 · 지정 의사 | **보내지 않음** | 보내지 않음 |
| 단계 | `RECEPTION` 에서 받았다 | `RECEPTION` 에서 받았다 |

- JS(`updateReservationV2`)에서 보낼 수 있는 필드: `scheduleId · zoneId · occupiedResources{items} · reservationAssignee · consultationRequired · sedationRequired · counselor · funnel · reservationMemo · desiredDischargeDateTimeUtc · connectedChannel`. `scheduleId` 말고는 모두 선택이다(JS zod `.optional()`)
- **빠진 필드는 지워지지 않았다**(확인): 시험 B 일정의 `예약상세_수정` #5(수정 전) ↔ 지금 조회를 비교했다. 바뀐 것은 `occupiedResources` · `reservation.startDateTime` · `endDateTime` · `updatedDateTimeUtc` 뿐이다. 담당자 · 메모 · 상담 · 유입은 그대로였다
- 내부 묶음 꼴은 `occupiedResources: {items: [...]}`(객체 안 배열)이다. 공개는 `occupiedResources: [...]`(배열)이다

### 2.2 거절 조건

| 출처 | 오류 |
|---|---|
| 공개 `updateReservationV2` 400 예시(스펙) | `NotFoundSchedule` · `OccupiedResourcesEmpty` · `DifferentDateInOccupiedResources` · `NotFoundZone` · `ZoneNotInReservationGroup` · `MissingOccupiedResourceConfiguration` · **`ReservationNotAllowedByPolicy`(변경 정책)** · **`ReservationCapacityExceeded`(정원 초과)** · **같은 고객 시간 겹침**(`startDateTime` NotAvailable) |
| 내부 JS 오류 처리(`oF`) | `ALREADY_RESERVED`(`startDateTime` NotAvailable) · `OCCUPIED_RESOURCES_EMPTY` · `OCCUPIED_RESOURCE_ID_EMPTY/DUPLICATED` · `DIFFERENT_DATE…` · `ZONE_NOT_IN_RESERVATION_GROUP` · `SCHEDULE_NOT_FOUND` — **정원 초과 처리는 없다**(C§2.2 와 같다) |
| 휴무 · 운영 시간 밖 | 스펙 · JS 모두 언급이 없다 |

### 2.3 데모 시험 — 공개 `updateReservationV2` 1회

- 대상: 오늘 이후 4층의 `RESERVED` 일정 중 가장 이른 것(11/1 10:00 KST · 「국내」 · 작업 없음 · 메모 있음 · 유입 「홈페이지」). 시험 A · B 는 뺐다
- 옮길 칸: 공개 `getReservationSlotsByGroupsV2` 로 미리 봤다. 「중화권」 11:00 · 정원 3 · 예약 0

| 순서 | 호출 | 본문(모양) | 결과 |
|---|---|---|---|
| M1 | 공개 `POST /schedule/open/v2/commands/update-reservation` | `{scheduleId, zoneId(4층), occupiedResources:[{startDateTimeUtc(+1시간), endDateTimeUtc(+30분), reservationGroup{「중화권」 id, zoneId}}]}` | **200** `{}` |

전후 비교(공개 `getScheduleDetail` 전체 필드)
- 바뀐 것: `occupiedResources` · `reservation.startDateTime` · `reservation.endDateTime` · `reservation.reservationGroupId`(국내 → 중화권) · `updatedDateTimeUtc`
- 그대로: `flowStep RESERVED` · `status RESERVED` · 메모 · 유입 · 담당 · 상담 · 수면 · 고객
- ⚠ 공개 v2 로 바꾸면 **일정 묶음 id(`occupiedResources[].id`)가 새로 바뀐다**(확인). 내부 상세 수정은 같은 id 를 넣어서 그대로였다
- 지정 의사(`reservationGroup.doctors`)는 전후 모두 빈칸이었다. 공개 v2 는 의사 값을 쓰지 않는다(C§5)

---

## 3. `cancel-reservation` 해부 (취소 · 부도)

| 항목 | 내용 |
|---|---|
| 내부 | `schedule/reservation/v1/commands/cancel-reservation{scheduleId, reason}` → `{}`. `reason` = `CANCELED`(고객 의사 취소) · `NO_SHOW`(부도) |
| 공개 | `cancelReservation{scheduleId*, reason*}`. `reason` enum `CANCELED · NO_SHOW`(+ 기본값 `UNSPECIFIED` 은 쓰지 않음). 400: `scheduleId NotFound` · **`status NotAvailable`(취소할 수 없는 상태)** · **`ReservationNotAllowedByPolicy`(취소 정책)** · 사유가 기본값 |
| 바뀌는 것 | `reservation.status` 만(`CANCELED` / `NO_SHOW`) + `updatedDateTimeUtc`. **`flowStep` 은 `RESERVED` 그대로**(R§3.2 와 같다) |
| 취소된 일정이 보이는 곳 | `getSchedulesByFlowStep(RESERVED)` 에 **그대로 나온다**(확인). 화면이 `reservation.status` 로 걸러야 한다 |
| 접수된 뒤에도 되나 | 이번에 시험하지 않았다(HAR 의 세 건 모두 `RESERVED` 일정). 공개 스펙의 「취소할 수 없는 상태」(`status NotAvailable`)가 무엇인지는 적혀 있지 않다 → Q-86 |

데모 시험(1회씩)

| 순서 | 대상 | 호출 | 결과 | 바뀐 필드 |
|---|---|---|---|---|
| C1 | 11/2 10:00 KST `RESERVED` 일정 | 공개 `cancelReservation{scheduleId, reason:"CANCELED"}` | **200** | `reservation.status RESERVED → CANCELED` · `updatedDateTimeUtc`. flowStep 그대로 |
| R1 | 같은 일정 | 내부 `revoke-canceled-reservation{scheduleId}` | **200** | `CANCELED → RESERVED` · `updatedDateTimeUtc`. **취소 전과 비교하면 `updatedDateTimeUtc` 말고 모두 같다** |
| N1 | 11/3 10:00 KST `RESERVED` 일정 | 공개 `cancelReservation{scheduleId, reason:"NO_SHOW"}` | **200** | `status RESERVED → NO_SHOW` · `updatedDateTimeUtc`. flowStep 그대로. **되돌리지 않았다** |

반영 지연: 세 건 모두 3초 뒤 첫 조회에서 이미 반영돼 있었다.

---

## 4. `revoke-canceled-reservation` (되돌리기)

- 내부 `schedule/reservation/v1/commands/revoke-canceled-reservation{scheduleId}` → `{}`
- 결과: `CANCELED → RESERVED`(시험 R1). flowStep 은 처음부터 `RESERVED` 였다
- JS 오류 처리: `scheduleId NotFound` → `notFound` · **`status NotAvailable` → `notAvailable`**. 되돌릴 수 없는 상태가 있다는 뜻이다
- **부도(`NO_SHOW`)도 되돌릴 수 있는지는 시험하지 않았다**(허가: 부도는 되돌리지 않음). 작업 이름이 「canceled reservation」이라서 부도는 `status NotAvailable` 로 거절될 수도 있다(추정) → Q-87
- **공개 짝: 없음.** 스펙 75개에 revoke · restore 류 작업이 없다(grep)

---

## 5. 공개 짝 정리

| 조작 | 내부 | 공개 | 차이 |
|---|---|---|---|
| 이동(시각 · 그룹) | `reservation/v2/commands/update-reservation` | `updateReservationV2` | 공개는 `zoneId` 필수 · 배열 꼴 · 묶음 id 를 새로 만든다. 공개 v2 는 메모 · 상담 · 담당 · 유입을 받지 않는다(그 칸들은 deprecated v1 `updateReservation` 이나 `changeReservationMemo` 에 있다) |
| 이동(슬롯 기반) | — | `rescheduleByTimeSlot{scheduleId, reservationDateTimeRange}` + `getReschedulableTimeSlots` | 그룹을 고르지 않는다(규칙이 정한다) |
| 취소 · 부도 | `reservation/v1/commands/cancel-reservation` | `cancelReservation` | 같은 본문 |
| 취소 되돌리기 | `reservation/v1/commands/revoke-canceled-reservation` | **없음** | |

---

## 6. 시안과 비교

| 시안 | KOS | 메모 |
|---|---|---|
| 카드 **드래그 → 칸에 놓기** = 권역 · 시각 이동. 놓으면 바로 · 확인 없음(D§6 · Q-13) | KOS 는 버튼으로 이동한다(사용자). 같은 `update-reservation` 이다. 공개 `updateReservationV2` 로도 된다(시험 M1) | 정원 초과 · 겹침 · 정책 거절은 서버가 400 으로 돌려준다(스펙). 놓은 뒤 거절되면 카드를 어떻게 되돌릴지 → Q-83 |
| 칸 = 30분 줄 | KOS 상세 수정은 55분 같은 임의 길이도 받았다 | 드래그가 길이를 유지할지 → Q-84 |
| [예약 취소] — 접수 전만 · 상태 「취소」 | KOS `cancel-reservation(CANCELED)`. 접수 뒤에도 되는지는 미확인 | → Q-86 |
| 범례 「취소」(R§3.2 S7) · 2계층 「부도」 | `reservation.status CANCELED` / `NO_SHOW` — flowStep 은 `RESERVED` 그대로. 2계층(예약 상태 · 내원 단계)과 그대로 맞는다 | 시안 [예약 취소] 버튼 하나 ↔ KOS 사유 둘(취소 · 부도) → Q-85 |
| 취소 되돌리기 | 시안에 없다. KOS 는 내부로만 된다 | → Q-88 |
| 고객 상세 「이전 방문」 Badge 「노쇼」 | `NO_SHOW` | R Q-23 |

---

## 7. 호출 기록

| 구분 | 경로 | 횟수 | 결과 |
|---|---|---|---|
| **쓰기 · 공개** | `schedule/open/v2/commands/update-reservation` | 1 | 200 |
| | `schedule/open/v1/commands/cancel-reservation`(CANCELED 1 · NO_SHOW 1) | 2 | 200 |
| **쓰기 · 내부** | `schedule/reservation/v1/commands/revoke-canceled-reservation` | 1 | 200 |
| 조회 · 공개 | `get-schedule-detail` 10 · `get-schedules-by-flow-step` 5 · `get-reservation-slots-by-groups` 1 | 16 | 200 |
| 인증 | 공개 `exchange-token` 4 · 내부 sign-in 1 | 5 | 200 |

- 쓰기 4건(각 1회) · 허가 밖 쓰기 0 · 운영 키 0. 합계 25회(스크립트 로그)
- 시술 대기로 둔 일정은 없다

**남긴 상태**(되돌리지 않음)

| 일정 | 상태 |
|---|---|
| 11/1 일정 | 11:00 KST · 「중화권」 · `RESERVED` |
| 11/2 일정 | `RESERVED`(취소 → 되돌림) |
| 11/3 10:00 일정 | `NO_SHOW` |

모두 원래 있던 데모 예약이다. 시험용으로 새로 만든 일정은 없다.

---

## 8. 정할 것 (결정하지 않음) — 9개

| # | 자리 | 왜 정해야 하나 | 앞 판 |
|---|---|---|---|
| Q-83 | 드래그를 놓았는데 KOS 가 거절할 때 | 정원 초과 · 같은 고객 겹침 · 변경 정책은 서버 400. 카드를 원래 자리로 되돌릴지 · 미리 막을지(슬롯 조회) · 확인 창을 둘지 | R Q-13 · C Q-55 |
| Q-84 | 드래그가 예약 길이를 유지하나 | KOS 는 임의 길이(55분)도 받는다. 칸 하나로 맞출지 · 원래 길이를 유지할지 | — |
| Q-85 | [예약 취소] 버튼과 사유 | KOS 는 `CANCELED` · `NO_SHOW` 두 사유다. 시안 버튼 하나에서 사유를 고르게 할지, 부도를 다른 곳(예: 시간이 지난 예약)에서 할지 | — |
| Q-86 | 접수 뒤 취소 | KOS 가 받는지 미확인. 공개 스펙에 「취소할 수 없는 상태」가 있다. 시안은 접수 전만 버튼이 있다 | — |
| Q-87 | 부도 되돌리기 | `revoke-canceled-reservation` 이 부도도 되돌리는지 미확인(시험 허가 밖) | — |
| Q-88 | 취소 되돌리기를 ccc 에 넣을지 | 공개가 없고 내부만 있다. 시안에도 없다 | — |
| Q-89 | 이동을 공개 v2 로 할지 내부로 할지 | 공개는 묶음 id 를 새로 만들고 `zoneId` 가 필수다. 내부는 id 를 유지한다. 묶음 id 를 ccc 가 참조한다면 공개 이동 뒤 다시 읽어야 한다 | C Q-62 |
| Q-90 | 취소 · 부도 일정을 판에 보일지 | `getSchedulesByFlowStep(RESERVED)` 에 섞여 온다. 칸 머리 건수에서 뺄지(R Q-3), 흐리게 보일지(시안 취소 = 불투명 0.5) | R Q-2 · Q-3 |
| Q-91 | 시험이 남긴 데모 상태 | 11/1 일정 이동 · 11/3 부도는 원래 데모 예약을 바꾼 것이다. 데모를 쓰는 다른 작업(E2E 등)에 알릴지 | — |
