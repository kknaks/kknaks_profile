# be-probe-1 결과 보고 — KOS 데모 지점 실물 확인 1 (예약 등록 · 새 고객 · 변경 · 취소)

## 상태: done

- 실행일: 2026-11-24 · DAY `KosClient`(`backend/day/emr/kos/client.py` `internal()` · `open()`) 그대로 사용 · 새 HTTP 코드 없음
- 데모 지점 확인(`check_open_key_is_demo` 같은 확인) **통과한 뒤에만** 썼다 — 공개 `get-zones` 기본 구역 id 가 데모 테넌트 예약 그룹 `intervalCapacities[].zoneId` 에 있음
- 레포 파일 수정 · 커밋 없음(`git status` 깨끗). `uv run` 이 워크트리에 `.venv` 를 만들었다(gitignore 대상)
- 값 · 토큰 · 개인정보 원문은 출력 · 기록하지 않았다. 아래는 키 이름 · 모양 · O/X · id 앞 8자만

## 요약 표

| 시험 | 경로 | 응답 코드 | 들어갔나 | 비고 |
|---|---|---|---|---|
| 1-a 같은 고객 찾기(없음) | 내부 `visitor/v1/queries/find-duplicated-visitor` | 200 | — | 응답 `{}`(`data` 키 없음) |
| 1-b 같은 고객 찾기(있음) | 같음 | 200 | O | `data` = 고객 상세 한 건 · 기존 데모 고객 id 와 같음 |
| 2 새 고객 만들기 | 내부 `v1/visitor/commands/create-visitor` | **400 → 200**(재시도 1회) | O(9/9 칸) | 첫 시도 400 `InvalidCommandException` = 연락처 꼴(`+82` · 앞 0). KOS 꼴(`82` · 앞 0 없음)로 바꾸니 200 |
| 3 예약 만들기 | 내부 `schedule/reservation/v2/commands/reserve` | 200 | O(전 칸) | 응답 `{scheduleId}` 하나. **담당자 · 유입은 바로 읽으면 빠지고 나중에 들어옴**(아래 §3) |
| 4ⓐ 최상위 `doctor` | 같음 | 200 | **X** | `reservation.doctor` 빈 값 · `occupiedResources[].reservationGroup.doctors` 빈 목록 |
| 4ⓑ `reservationGroup.doctors` | 같음 | 200 | **O** | `occupiedResources[0].reservationGroup.doctors[0]` 에 들어감 · `reservation.doctor` 는 빈 값 그대로 |
| 5-1 날짜 · 시간 바꾸기 | 내부 `schedule/reservation/v2/commands/update-reservation` | 200 | O | **다른 날짜로도 옮겨짐**(11-27 → 11-28) |
| 5-2 예약 그룹 바꾸기 | 같음 | 200 | O | 같은 구역 · 같은 간격(30분)의 다른 그룹 |
| 5-3 지정 의사 바꾸기 | 같음 | 200 | O | ⓑ 자리(`reservationGroup.doctors`) |
| 6 예약 취소 | 공개 `schedule/open/v1/commands/cancel-reservation` | **400 → 200**(재시도 1회) | O | 첫 시도 400 = 내가 `reason` 에 자유 글자를 넣은 잘못. enum `CANCELED` 로 200 · `reservation.status = "CANCELED"` |

- **지정 의사 결론: ⓑ**(`occupiedResources[].reservationGroup.doctors: [{id, name}]`). ⓐ 최상위 `doctor` 는 200 으로 받지만 저장하지 않는다(조용히 버림).
- **`isNew`**: `reserve` 응답에는 없다(응답은 `{scheduleId}` 뿐). 예약 상세 `visitor.isNew = true` · 고객 상세 `isNew = true`(새 고객).
- 시험 고객(남겨 둠): KOS 고객 id `6b051a9e…` · 이름 「박하늘(시험)」 · 가짜 번호
- 시험 예약(모두 취소함): main `7e2dbde9…` · 4ⓐ `d828b97b…` · 4ⓑ `b7cf07f9…` — 모두 앞날(2026-11-27 · 이동 뒤 11-28) · 시험 전에 빈 칸이었음

## 단계별

### 0. 기준 정보(읽기)

| 무엇 | 경로 | 고른 값 |
|---|---|---|
| 구역 | 공개 `schedule/open/zone/v1/queries/get-zones` | `isDefault` 구역 |
| 예약 그룹 | 내부 `schedule/group/v1/queries/get-reservation-groups {deleted:false}` | `isDefault` 그룹(30분) · 5-2 는 같은 구역 · 30분 다른 그룹 |
| 직원 | 내부 `role/v2/queries/get-roles` + `account/v2/queries/get-accounts` | 담당자 = 역할 「상담실장」 활성 · 시스템 계정 아님 / 의사 = 역할 「원장」 활성 |
| 유입 | 내부 `meta/codes/v1/queries/get-codes {category:"FUNNEL"}` | 안 닫힌 첫 코드 · 행 `{id, category, name, order, closed, default}` |
| 빈 칸 | 공개 `schedule/open/v2/queries/get-reservation-slots-by-groups` | `data[].{reservationGroupId, zoneId, slots[].{reservationGroupId, zone{id,name}, startDateTimeUtc, endDateTimeUtc, capacity, reservationCount}}` |

참고: 「원장」 중 `licenseNumber` 가 있는 계정은 전부 비활성이었고, 활성 원장 2명은 `licenseNumber` 가 비어 있다. 의사를 면허 번호로 가르면 데모 지점에서는 활성 의사가 0명이 된다.

### 1. 같은 고객 찾기

- 요청 1-a(새 이름): `{name, phone{countryCode, phoneNumber}, snsInfo{snsType, accountId}, birthDateUtc}` → 200 `{}`
  - 1-a 의 연락처는 `+82` · 앞 0 꼴이었다. 이 꼴은 2 에서 거부됐다. 「없음」 응답 모양을 보는 데는 영향 없음
- 요청 1-b(기존 데모 고객): `{name, birthDateUtc}` → 200 `{data: {고객 상세 전 칸}}`. `data.id` = 그 고객 id(O)
  - `data` 키 모양 = `visitor/v2/queries/get-visitor` 의 `data` 와 같음(`id, chartNumber, name, visitorType, dateOfBirth, gender, nationality, language, doctor, counselor, funnel, snsInfo, visitorFunnel, isNew, …`)
- 2 뒤 확인: 새 고객의 `{name, phone(KOS 꼴), snsInfo}` 로 다시 찾으니 200 · `data.id` = 새 고객 id(O)
- **「없음」= `data` 키가 없음**(null 아님 · 빈 객체). cc `_new_visitor` 의 `found.get("data")` 판정과 맞다

### 2. 새 고객 만들기

- 요청 키: `{name, phoneticName, gender, nationality, dateOfBirth, phoneNumber{countryCode, phoneNumber}, snsInfo{snsType, accountId}}`
  - 값 꼴: `gender` = `MALE|FEMALE|GENDER_UNSPECIFIED` · `nationality` = ISO 2자(`KR`) · `dateOfBirth` = `YYYY-MM-DD 00:00:00.000Z`(공백 · cc 와 같음) · `snsType` = 소문자 enum(`kakaotalk` …)
- 첫 시도 400: `className = InvalidCommandException`, 본문 키 `className, errorProperties, message, properties, status`. 연락처를 `countryCode "+82"` · 번호 앞 `0` 으로 보냈다
- 재시도(연락처만 바꿈 — `countryCode "82"` · 앞 0 없는 번호. cc 시험 고정본 · `get-visitor` 응답 꼴과 같음) → 200 `{data: {id}}`
  - 연락처만 바꿨으니 원인은 연락처 꼴이다. 다만 `countryCode` 와 앞 0 중 무엇이 막았는지는 따로 가르지 않았다(재시도 1회 제한)
- 다시 읽기 `visitor/v2/queries/get-visitor {id}`:

| 칸 | 들어갔나 |
|---|---|
| name | O |
| phoneticName | O |
| gender | O |
| nationality | O |
| dateOfBirth(앞 10자) | O |
| phoneNumber.countryCode | O |
| phoneNumber.phoneNumber | O(보낸 그대로) |
| snsInfo.snsType | O |
| snsInfo.accountId | O |
| (덤) isNew | `true` |
| (덤) chartNumber | KOS 가 매김(있음) |

- 기존 고객 상세에는 연락처가 없으면 `phoneNumber` 키 자체가 없다(null 아님)

### 3. 예약 만들기

- 요청 키(cc `create` 와 같음 · `counselor` · `desiredDischargeDateTimeUtc` 는 안 넣음):
  `{visitorId, zoneId, occupiedResources[{id(uuid4), type:"RESERVATION_GROUP", reservationTime{startDateTimeUtc, endDateTimeUtc}, reservationGroup{reservationGroupId, zoneId, doctors:[]}}], reservationAssignee{id, name}, reservationMemo, funnel{funnel{id, category, name, order, closed, default}, funnelDetail}}`
- 응답 200 `{scheduleId}` — `visitor` 같은 다른 키 없음
- 다시 읽기 내부 `schedule/v1/queries/get-schedule-detail {scheduleId}` (DAY `PATH_SCHEDULE_DETAIL` = cc `PATH_DETAIL`). 상세 모양: `{id, visitor{id, name, phone, chartNumber, gender, dateOfBirth, nationality, isNew, snsInfo, phoneticName, …}, flowStep, reservation{reservationGroupId, startDateTime, endDateTime, consultationRequired, sedationRequired, counselor, doctor, funnel{funnel?, funnelDetail}, reservationMemo, zoneId, reservationAssignee, status, requestedProcedures, connectedChannel, statusUpdatedDateTimeUtc}, consultation{…}, zone{id,title}, occupiedResources[{id, type, reservationTime, reservationGroup{reservationGroupId, zoneId, doctors}}], deleted, …}`

| 칸 | 바로 읽음(reserve 직후) | 다시 읽음(수 초 뒤) |
|---|---|---|
| visitor.id | O | O |
| zoneId | O | O |
| 시작 · 끝 | O(`reservation.startDateTime/endDateTime` + `occupiedResources[0].reservationTime`) | O |
| 예약 그룹 | O(`reservation.reservationGroupId` + `occupiedResources[0].reservationGroup`) | O |
| 담당자 `reservation.reservationAssignee` | **X** | O |
| 유입 `reservation.funnel.funnel.id` | **X** | O |
| 유입 상세 `reservation.funnel.funnelDetail` | **X** | O |
| 예약 메모 `reservation.reservationMemo` | O | O |
| 상태 | `reservation.status = RESERVED` · `flowStep = RESERVED` | 같음 |

- `connectedChannel = "Channel_UNSPEICIFED"`(KOS 철자 그대로)
- 고객 상세의 `visitorFunnel` · `funnel` · `detailedFunnel` 에는 예약 유입이 옮겨지지 않았다(예약에만 저장)
- 유입을 안 보낸 예약(4ⓐ · 4ⓑ)은 상세 `reservation.funnel` 이 `{funnelDetail: ""}` 모양이다

### 4. 지정 의사 두 자리

- ⓐ 요청 = 3 과 같은 모양(메모 · 유입 없음) + 최상위 `doctor{id, name}` → 200 · 다시 읽음: `reservation.doctor` 빈 값 · `occupiedResources[0].reservationGroup.doctors` 길이 0 · `consultation.doctor` 빈 값 → **안 들어감**
- ⓑ 요청 = `occupiedResources[0].reservationGroup.doctors: [{id, name}]` → 200 · 다시 읽음: `occupiedResources[0].reservationGroup.doctors[0].id` = 그 의사(O) · `reservation.doctor` 는 빈 값
- 결론 **ⓑ**. 상세에서 지정 의사를 읽는 자리도 `occupiedResources[].reservationGroup.doctors` 다(`reservation.doctor` 아님)

### 5. 예약 변경 (main 예약)

- 요청 키(cc `move` 와 같음): `{scheduleId, occupiedResources{items[{id(기존 자원 id), type, reservationTime{startDateTimeUtc, endDateTimeUtc}, reservationGroup{reservationGroupId, zoneId, doctors}}]}}` → 응답 200 `{}`
- 다시 읽기(2초 뒤 · 한 번에 맞음):

| 시험 | 바뀌었나 | 함께 확인 |
|---|---|---|
| 5-1 날짜 · 시간(11-27 11:00 → 11-28 15:00 KST · 길이 30분 그대로) | O(`occupiedResources` · `reservation.startDateTime` 둘 다) | 자원 id 그대로 · 담당자 · 메모 · 유입 · 유입 상세 그대로 · `RESERVED` |
| 5-2 예약 그룹(기본 → 다른 30분 그룹) | O(`occupiedResources[0].reservationGroup.reservationGroupId` · `reservation.reservationGroupId`) | 위와 같음 |
| 5-3 지정 의사(빈 → 원장 1명 · ⓑ 자리) | O(`reservationGroup.doctors[0]`) | `reservation.doctor` 는 빈 값 그대로 |

- KOS 는 다른 날짜로 옮기는 것도 받는다. cc `move` 는 「같은 날짜 안에서만」을 자체 규칙으로 막았다(KOS 제약 아님)

### 6. 예약 취소

- 요청 키: `{scheduleId, reason}`(공개 · cc `cancel`)
- 첫 시도 `reason = "(시험) …"`(자유 글자) → 400 · 본문이 JSON 객체가 아님. **내 잘못**: openapi `protos.schedule.CancelReservationCommand.reason` 은 enum `CANCELED | NO_SHOW`(`CANCEL_RESERVATION_REASON_UNSPECIFIED` 는 쓰지 않음)이다. cc 시험도 `"CANCELED"` 를 보낸다
- 재시도 `reason = "CANCELED"` → 200 `{eventId}` (세 건 모두)
- 다시 읽음(3초 뒤): `reservation.status = "CANCELED"` · `flowStep = "RESERVED"`(그대로) · `deleted = false` · `statusUpdatedDateTimeUtc` 갱신 · 상세 404 아님(그대로 읽힘)

## DAY `writes.py` 에 열 때 필요한 것 (후보 — 결정 아님)

| 동작 | api · 경로 | 값 조건 후보 | 확인 조건 후보(다시 읽기) |
|---|---|---|---|
| 같은 고객 찾기 | internal `visitor/v1/queries/find-duplicated-visitor` | 읽기지만 쓰기 직전 판정이다. 연락처는 KOS 꼴 | `data` 키 있음 = 있음 · 없음 = 새로 |
| 새 고객 | internal `v1/visitor/commands/create-visitor` | `name` 필수. `phoneNumber.countryCode` = 숫자만(`82`) · 번호 앞 0 없음 · `dateOfBirth` `YYYY-MM-DD 00:00:00.000Z` · `gender` enum · `snsType` 소문자 enum | 응답 `data.id` → `get-visitor` 칸 같음 |
| 예약 만들기 | internal `schedule/reservation/v2/commands/reserve` | `occupiedResources` 1개 · `type RESERVATION_GROUP` · 끝 = 시작 + 그룹 간격 · `reservationAssignee` 필수 · 지정 의사는 **`reservationGroup.doctors`** 에만 | 응답 `scheduleId` → 상세의 그룹 · 시작 · 구역 · 고객. **담당자 · 유입은 바로 안 보일 수 있다** — 확인을 바로 한 번으로 끝내면 거짓 불일치(재읽기 · 기다림 필요) |
| 예약 변경 | internal `schedule/reservation/v2/commands/update-reservation` | `items[].id` = 기존 자원 id · 바꾸지 않는 칸(`doctors` 포함)도 다시 실어야 한다(덮어쓰기로 보임 — 5-3 에서 빈 목록 → 1명 확인. 빈 목록으로 지우는 것은 시험 안 함) | `occupiedResources[0]` 의 시작 · 끝 · 그룹 · doctors 가 보낸 값 |
| 예약 취소 | open `schedule/open/v1/commands/cancel-reservation` | `reason ∈ {CANCELED, NO_SHOW}` | `reservation.status == "CANCELED"`(`flowStep` 는 안 바뀜) |

- 최상위 `doctor` 는 KOS 가 200 을 주고 버린다. `write_open` 에서 막을지(본문에 최상위 `doctor` 가 있으면 거부) 정해야 한다
- 취소 상태는 `reservation.status` 에만 드러난다. 방문 단계(`flowStep`)로 판정하면 취소를 못 알아챈다
- 그 밖에 시험 안 한 칸: `counselor` · `desiredDischargeDateTimeUtc` · `consultationRequired` · `sedationRequired` · 빈 `doctors` 로 의사 빼기 · `NO_SHOW` · 접수 뒤 예약 취소(정책 400 `ReservationStatusNotAvailable` 후보)

## 이슈 · 코디가 확인할 것

1. **reserve 직후 상세에서 담당자 · 유입이 빠짐**(수 초 뒤에는 들어옴). outbox `expect` 를 정할 때 이 지연을 생각해야 한다
2. 지정 의사 자리는 ⓑ. DAY 화면 · 동기화가 예약 의사를 `reservation.doctor` 에서 읽고 있다면 맞지 않는다(이번 범위 밖 · 확인 안 함)
3. 데모 지점의 활성 원장에는 `licenseNumber` 가 없다. 의사 목록을 면허로 거르면 비게 된다
4. 시험 고객 `6b051a9e…` 는 남겨 둠(지침 7). 시험 예약 3건은 취소 상태로 KOS 에 남아 있다(지우지 않음)
5. 400 이 두 번 났다(2 · 6). 둘 다 1회 재시도로 원인 칸 하나만 바꿔 통과했다. 6 은 내 본문 잘못이었고 KOS 쪽 문제는 아니다

## 시험 스크립트 (`/private/tmp/day-probe-1/`)

- `pcommon.py` — env 읽기(값 출력 안 함) · `KosClient` 조립 · 오류 칸만 남기는 transport · 모양 출력 · `where`(값 대신 경로)
- `discover.py`(0 · 읽기 · 데모 확인) · `steps12.py`(1 · 2 첫 시도) · `step2retry.py`(2 재시도) · `steps34.py`(3 · 4) · `inspect3.py`(3 다시 읽기) · `steps56.py`(5 · 6 첫 시도) · `step6retry.py`(6 재시도) · `harshape.py`(HAR 요청 모양 · 참고)
- `log.md` — 단계별 요청 · 응답 키 모양 기록 · `state.json` — 고른 id(직원 이름 · 기존 고객 정보 지움)
