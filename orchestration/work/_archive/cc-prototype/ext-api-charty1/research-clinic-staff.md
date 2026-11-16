# 조사 2차 — 병원 정보 · 직원 목록: 어디서 가져오나

> researcher · 조사일 **2026-11-16** · 데모 테넌트만 · KOS 공개 API **조회(`/queries/`)만** 불렀다.
> 쓰기(`/commands/`) 호출은 0건이다. 공개 토큰 교환만 1회 불렀다(인증용, 데이터 쓰기 아님). 내부 API 는 1차처럼 **부르지 않았다**(내부 토큰 발급 `sign-in` 이 `/commands/` 경로라서). 내부 쪽은 HAR 과 KOS 웹 JS 번들로만 봤다.
> public 레포다. 키 · 토큰 · 테넌트 id · KOS id · 사람 이름 · 이메일 · 전화는 적지 않았다. 역할 이름은 KOS 역할 설정 값이라서 적었다(2차 브리프가 허용함). 그 밖에는 경로 · 칸 이름 · 모양 · 건수만 적었다.
> 코드 = kknaksss/cc-prototype `origin/main` `0a58aba`(`git show` 로만 읽음). 줄 번호는 모두 `procedure/back/app/` 아래 파일 기준이다.
> KOS 스펙 = openapi.yaml `info.version` 1.0.1 · 작업 81개(1차에서 받은 파일 그대로).

표기: **확인** = 이번에 데모에서 불러 본 것 · **스펙** = openapi.yaml · **HAR** = 로컬 HAR(값은 옮기지 않음) · **JS** = HAR 안에 든 KOS 웹 JS 번들 · **코드** = origin/main · **추정** = 해석(근거를 함께 적음).
분류(1차와 같음): **A** 지금 코드에 있음 / **B** KOS 공개 API 로 됨 / **C** 내부 API(HAR)로만 됨 / **D** CC 저장 필요 / **E** 없음 · HAR 필요.

---

## 0. 요약

| # | 질문 | 한 줄 답 | 분류 |
|---|---|---|---|
| 1 | 병원 정보 | 공개 스펙에는 병원 · 테넌트 · 지점 정보를 주는 조회가 **없다**. 내부 `/tenants/{id}/v1/hospital/queries/get-hospital` 이 KOS 웹 JS 에 있고, 병원 이름 · 전화 · 주소 · 대표자 · 사업자 번호 · 요양기관 번호 · 국적 · 언어 같은 칸이 보인다. 다만 **이 조회를 실제로 부른 HAR 이 없어서** 응답은 보지 못했다. 공개 API 로 받을 수 있는 병원 설정은 구역 · 예약 그룹(운영 시간표) · 타겟 국가뿐이다. CC 설정에는 병원 이름 칸이 없다 | 이름 · 주소 · 전화 **E**(내부 경로는 JS 로만 확인. HAR 필요) · 운영 설정 **B** · CC 설정 **D** |
| 2 | 직원 목록 | 공개 `getAccounts` 는 직원 1명당 `{id, name, email, activate, roleTags[]}` **5칸뿐**이다. 「CS팀(콜센터)」는 **역할 이름**이라서 공개 응답에 **안 온다**. 공개 응답에 오는 것은 역할에 붙은 태그 `CALL_COUNSELOR` 다. 그런데 이 태그는 관리자 · 코디 같은 역할에도 붙어 있어서, `roleTag=CALL_COUNSELOR` 로 거르면 21명이 나온다(CS팀은 그중 3명). 역할 이름은 내부 `account/v2/queries/get-accounts`(`roleName` · `role{id, name, roleTags}`)와 내부 `role/v2/queries/get-roles` 에만 있다. 데모 82명 중 활성 58명 · 비활성 24명 | 기본 5칸 **B** · 역할 이름(CS팀) **C** |
| 3 | 지금 CC | 직원 사본 `staff` 는 공개 `getAccounts` 를 1시간마다 통째로 덮어쓴다. **이메일은 버리고** 이름 · 태그 · 활성만 저장한다. KOS 에서 사라진 계정의 행은 지우지 않는다. `kos_exclude_account_ids` 는 사본에서 행을 빼지 않고, 원장 · 상담사 **목록에서만** 뺀다. 직원 목록을 그대로 내는 API 는 **없다**. 목적별로 거른 목록 3곳(예약 폼 · 예약 상세 상담사 · 시술 board 원장)과 메신저 상대 목록(ccc 계정 기준)만 있다. ext 에는 직원 경로가 없다 | **A**(일부) |

---

## 1. 병원 정보

### 1.1 공개 스펙(openapi 1.0.1)

- 작업 81개의 operationId · 경로 · 요약을 모두 훑었다. 병원 · 테넌트 · 지점 · 사업자를 주는 조회는 **없다**.
- 스펙 본문에 「병원」이라는 말은 설명문에만 나온다(「병원에 등록된 직원」 · 「병원 예약 취소 정책」 등). 「tenant」 · 「branch」 · 「hospital」을 이름에 단 스키마나 경로는 없다.
- `exchangeToken` 응답은 `{token}` 하나뿐이다. 테넌트를 알려 주는 칸이 없다.

공개 API 로 받을 수 있는 **병원 설정**(확인 · 데모 실호출):

| 작업 | 응답 칸(키 트리) | 데모 |
|---|---|---|
| `getZones` (`/schedule/open/zone/v1/queries/get-zones`) | `data[]{id, title, isDefault, order}` | 2건 |
| `getZone` | `data{id, title, isDefault, order}` | (부르지 않음. 스펙만) |
| `getReservationGroups` (`/schedule/open/v1/queries/get-reservation-groups`) | `data[]{id, title, color, memo, isDefault, order, startDate, intervalMinutes, sameDayCloseBufferMinutes, intervalCapacities[]{zoneId, enabled, intervalCapacity}, operationTimetable{monday … sunday: {enabled, startTime, endTime, breaktime{startTime, endTime}}}, reservationPolicy{reservation{maxAdvanceDays, minimumAdvance{…}}, cancel{allowed, minimumAdvance{…}}, reschedule{…}}}` | 13건 · 기본 그룹 1건. 실응답에는 `color` · `reservationPolicy` 가 없었다(스펙에서도 선택 칸) |
| `getTargetCountries` (`/procedure-menu/open/target-countries/queries/get-target-countries`) | `data[]{code, order, suggestingVisitorTypeId?}` | 4건 · 코드 2종(`KR` · `ETC`. 같은 코드가 2건씩) |

- 병원 전체의 운영 시간표를 주는 공개 조회는 없다. 운영 시간표는 **예약 그룹마다** 있다.

### 1.2 내부 API(HAR · JS)

HAR 은 1차 브리프의 7+1개와 `2026-10-23-cc-overall-board/har/` 23개를 봤다. **HAR 의 계정 id 는 데모 공개 `getAccounts` 와 모두 겹친다**(`상담대기.har` 82/82 · `상품 수납.har` 82/82 · `고객예약접수시술.har` 80/80 · `방이동.har` 81/81). 그래서 이 HAR 들은 데모 테넌트에서 캡처한 것이다.

실제로 불린 내부 조회 중 병원 설정에 해당하는 것(HAR):

| 경로(`/tenants/{id}/…`) | 응답 모양 | HAR |
|---|---|---|
| `meta/codes/v1/queries/get-codes {category}` | `data[]{id(uuid), category, name, order, closed, default?}`. 관찰한 category = `FUNNEL`(14) · `FUNNEL_CATEGORY`(0) · `CONSULTATION_RESULT`(8) | 상담대기 외 |
| `meta/template/v1/queries/get-hospital-text-snippets {}` | `data[]{id, title, content, createdDateTimeUtc, updatedDateTimeUtc}`. 이름은 hospital 이지만 **문구 템플릿**이다 | 상담대기 · 수납필요 확인 · 처방전상세 |
| `procedure-menu/currency-settings/queries/get-currency-settings` | `data{currency}`(`KRW`) | 상담대기 외 |
| `procedure-menu/vat-settings/queries/get-vat-settings` | `data{includeVATInPrice, vatRate}` | 상담대기 · 상품 수납 |
| `schedule/group/v1/queries/get-reservation-group {id}` | 공개 예약 그룹 원소와 같은 모양 | 상담대기 외 |
| `schedule/default-operation-time/v1/queries/get-default-operation-timetable` · `get-default-days-off` | (응답 모양은 이번에 펼치지 않았다) | 상품 수납 |
| `meta/connect/v1/queries/get-connect-apps` | (펼치지 않음) | 상품 수납 |

**병원 이름 · 주소 · 전화를 주는 조회를 실제로 부른 HAR 은 없다.** HAR 에 담긴 KOS 웹 JS 번들(`예약그룹.har` 의 reservation · notification · purchase 클라이언트)에는 다음 조회가 있다(JS):

- 경로: `/tenants/:currentTenantId/v1/hospital/queries/get-hospital` (본문 `{}`)
- JS 가 읽는 응답 `data` 칸(프로토 기본값 함수 기준): `nursingInstitutionNumber`(요양기관 번호) · `companyRegistrationNumber`(사업자 번호) · `businessLicenseImageUrl` · `companyName` · `hospitalName` · `representativeName` · `hospitalPhoneNumber` · `addressContract` · `websiteUrl` · `taxBillEmail` · `logoImageUrl` · `representativeStampImageUrl` · `hospitalMapImageUrl` · `nationality` · `languages[]` · `qualifiedInvoiceIssuerNumber` · `translsMap{}`
- `addressContract` 는 같은 번들의 `{address, detailedAddress, zipCode, translsMap}` 메시지로 **추정**한다(바로 옆 기본값 함수 기준이고, 연결 고리는 직접 확인하지 못했다). reservation 클라이언트는 `hospitalPhoneNumber` 에 국가 번호 `82` 를 붙인다.
- 같은 JS 에는 공통 경로 `/common/v1/tenant/queries/get-user-tenants` 와 `/common/v1/hospital/commands/create-hospital {code, name}` 도 있다. 둘 다 HAR 에서 불린 적은 없다.

→ 병원 이름 · 주소 · 전화는 **E**로 둔다. 내부 경로가 있다는 근거가 JS 뿐이고 실제 응답이 없기 때문이다. KOS 웹에서 이 조회를 부르는 화면(병원 설정 · 처방전 · 영수증 등 · 추정)을 HAR 로 받아야 응답을 확인할 수 있다.

### 1.3 CC 설정으로 낼 수 있는 것

`config.py:17-75` 에 있는 병원 관련 칸(코드):

- `kos_tenant_id`(`:21`) · `kos_zone_id`(`:24`, 구역 1개) · `kos_ext_reservation_group_id`(`:37`, 외부 예약 그룹 1개) · `kos_web_base`(`:30`) · `kos_poll_window`(`:28`, 조회 시간대)
- 시간대는 설정이 아니라 코드 상수다. `domain/clock.py:7` `KST = ZoneInfo("Asia/Seoul")`
- 병원 이름 · 주소 · 전화 · 대표자 칸은 **없다** → 넣으려면 **D**(CC 저장 · 설정)

---

## 2. 직원 목록

### 2.1 공개 `getAccounts` (`/account/open/v1/queries/get-accounts`)

스펙:

- 요청 `{activate?: boolean, roleTag?: enum}`. `roleTag` 는 「지정한 역할 태그가 **붙은 역할**의 직원만」 고른다. `ROLE_TAG_UNSPECIFIED` 는 조건으로 쓸 수 없다(400).
- 응답 `data[]{id*, name*, email*, activate*, roleTags[]}`. 스펙 설명문도 「ID, 이름, 이메일, 역할 태그, 활성화 여부**만** 포함」이라고 적고 있다.
- `roleTags` enum: `ADMIN`(관리자) · `DOCTOR`(의사) · `COUNSELOR`(상담사) · `NURSE`(간호사) · `SKINCARE`(스킨케어) · `CALL_COUNSELOR`(**콜 상담사**) · `COORDINATOR`(코디네이터) · `ROLE_TAG_UNSPECIFIED`
- 역할 **이름**을 담는 스키마 `protos.account.AccountRoleV2Contract{id, name, roleTags}` 는 스펙에 있다. 그러나 이 스키마는 일정의 작업 담당자(`FlowTaskAssignee.role`) · 기타 업무 담당자(`ScheduleEtceteraWorkAssignee.role`)에만 쓰이고, `getAccounts` 에는 붙지 않는다.

데모 실호출(확인):

| 호출 | 건수 |
|---|---|
| `{}` | 82 |
| `{activate: true}` | 58 |
| `{activate: false}` | 24 |
| `{roleTag: "CALL_COUNSELOR"}` | 21(활성 14 · 비활성 7) |

- 82명 모두 키가 5개로 같다. `roleTags` 는 82명 모두 배열이고, 빈 배열이 6명이다.
- 이름이 같은 직원이 1쌍 있다(이름만으로는 사람을 가를 수 없다).

`roleTags` 조합별 인원(확인 · 공개):

| roleTags 조합 | 인원 |
|---|---|
| `ADMIN` | 24 |
| 7종 전부 | 10 |
| `SKINCARE` | 8 |
| `NURSE` | 8 |
| `CALL_COUNSELOR, COUNSELOR, COORDINATOR` | 7 |
| (없음) | 6 |
| `DOCTOR` | 5 |
| `COUNSELOR, ADMIN` | 4 |
| `COUNSELOR` | 4 |
| `CALL_COUNSELOR` | 3 |
| `DOCTOR, ADMIN` | 2 |
| `ADMIN, NURSE, SKINCARE, CALL_COUNSELOR, COORDINATOR` | 1 |

태그별 활성/비활성(한 사람이 여러 태그에 세어진다): `ADMIN` 32/9 · `COUNSELOR` 15/10 · `NURSE` 14/5 · `CALL_COUNSELOR` 14/7 · `SKINCARE` 12/7 · `COORDINATOR` 12/6 · `DOCTOR` 10/7 · 태그 없음 3/3

### 2.2 「CS팀(콜센터)」는 어디서 오나

내부 `account/v2/queries/get-accounts`(HAR · `상담대기.har` #11 · 본문 `{}`) 응답 원소:

`{id, userId, email, name, realName, roleId, roleName, role{id, name, roleTags[](숫자)}, activate, createdAt, updatedDateTimeUtc, mfaMethods[], licenseNumber?}`

- `licenseNumber` 는 82명 중 37명에게만 있다. `mfaMethods` 는 82명 모두 빈 배열이다.
- `roleName` 은 82명 모두 `role.name` 과 같다.
- 내부 `role.roleTags` 는 숫자다. 스펙 enum 순서(0 = UNSPECIFIED … 7 = COORDINATOR)로 바꾸면 `상담대기.har` 에서는 82명 모두 공개 `roleTags` 와 같다. 숫자와 이름의 대응은 순서로 맞춘 **추정**이고, 82/82 일치로 뒷받침된다.
- 내부 `role/v2/queries/get-roles`(HAR · 본문 없음) = `data[]{id, name, roleTags[]}`, **15개 역할**.

역할(역할 이름 = KOS 설정 값) · 태그 · 인원(HAR · `상담대기.har` · 활성/비활성):

| 역할 이름 | roleTags | 활성 | 비활성 |
|---|---|---|---|
| 경영지원 | `ADMIN` | 14 | 2 |
| 관리자 | 7종 전부 | 6 | 4 |
| 마케팅 | `ADMIN` | 7 | 1 |
| 간호 | `NURSE` | 7 | 1 |
| 피부관리 | `SKINCARE` | 5 | 3 |
| 코디 | `CALL_COUNSELOR, COUNSELOR, COORDINATOR` | 5 | 2 |
| 원장 | `DOCTOR` | 2 | 3 |
| 상담실장 | `COUNSELOR` | 2 | 2 |
| 상담총괄실장 | `COUNSELOR, ADMIN` | 2 | 2 |
| **CS팀(콜센터)** | **`CALL_COUNSELOR`** | **2** | **1** |
| 대표원장 | `DOCTOR, ADMIN` | 2 | 0 |
| 마취과 | (없음) | 2 | 1 |
| 촬영팀 | (없음) | 1 | 2 |
| ADMIN | `ADMIN, NURSE, SKINCARE, CALL_COUNSELOR, COORDINATOR` | 1 | 0 |
| OWNER | `ADMIN, DOCTOR` | 0 | 0 |

여기서 알 수 있는 것:

- **공개 응답만으로 「CS팀(콜센터)」를 고르는 정식 방법은 없다.** `roleTag=CALL_COUNSELOR` 로 거르면 CS팀 3명 + 코디 7명 + 관리자 10명 + ADMIN 1명 = 21명이 나온다.
- 지금 데모에서는 태그가 정확히 `[CALL_COUNSELOR]` 하나인 역할이 CS팀뿐이다. 그래서 공개 응답에서 「태그 집합 = `[CALL_COUNSELOR]`」인 3명이 CS팀 3명과 겹친다(확인 · 공개 3명). 하지만 이는 **지금 설정이 우연히 그런 것**이다. 같은 태그 집합을 가진 역할이 새로 생기면 섞인다(추정).
- 같은 이유로, 태그가 없는 역할 둘(마취과 · 촬영팀, 6명)은 공개 응답에서 서로 구별되지 않는다. 경영지원 · 마케팅도 둘 다 `[ADMIN]` 이라 구별되지 않는다.
- 「외주」를 뜻하는 칸은 공개 · 내부 어느 계정 응답에도 **없다**. 외주인지 아닌지는 역할 이름(내부)으로만 짐작할 수 있다.
- 시점 차이: `고객예약접수시술.har` 3명 · `방이동.har` 3명 · `상품 수납.har` 1명은 그때의 내부 태그가 오늘의 공개 태그와 다르다. 그 사이 역할이 바뀐 것으로 **추정**한다. 또 데모 일정의 작업 담당자 `role`(확인 · 1차 `getSchedulesByFlowStep` 응답)은 `경영지원 [ADMIN]` 이었는데, 그 계정의 지금 공개 태그는 7종 전부였다. 일정에 담긴 역할은 **배정 당시 값**일 수 있다(추정).

---

## 3. 지금 CC

### 3.1 직원 사본 동기화 — `kos/sync.py`

- 경로: 공개 `account/open/v1/queries/get-accounts`(`:24`)를 본문 `{}`(필터 없음)로 부른다(`:173`). 주기는 1시간 + 서버 시작(`config.py:27` `kos_poll_master_sec=3600`). 조회 시간대(`:160`) 밖에서는 부르지 않는다.
- 저장(`:177-180`): `staff` 행 = `kos_id` · `name` · `role_tags` · `active` · `synced_at`.
  - **버리는 것: `email`.** 공개 응답 5칸 중 4칸만 저장한다.
  - 역할 이름은 처음부터 받지 않는다(공개 응답에 없음).
- 테이블(`repository/db.py:10-13`): `staff{id(정수), kos_id UNIQUE, name, role_tags(JSON), active, is_doctor, synced_at}`. 이메일 칸이 없다.
- **삭제가 없다.** upsert 만 한다. KOS 목록에서 빠진 계정의 행은 마지막 값 그대로 남는다(`repository/repo.py` 에 `DELETE FROM staff` 없음).
- 일정 동기화에서 담당자 · 집도의로 나온 계정이 직원 목록에 없으면 `role_tags=[]` · `active=False` 행을 새로 만든다(`kos/sync.py:64-73`).
- `kos_exclude_account_ids`(`config.py:25` · 쉼표 목록 → `:81-83` `exclude_account_ids`):
  - 사본에서 **행을 빼지 않는다.** 82명이 모두 저장된다.
  - 쓰이는 곳은 목록 거르기뿐이다:
    - 원장 표시 `is_doctor`: `repo.py:302-312` `set_doctor_flags` = `DOCTOR` 태그 · 활성 · 시스템 계정 아님 · 제외 목록 아님. 시스템 계정 id 를 모르면 갱신하지 않는다
    - 상담사 목록: `service/reservations.py:109-115` `_counselors` = `COUNSELOR` 태그 · 활성 · 시스템 아님 · 제외 아님
    - 예약 폼 직원 목록: `service/reservations.py:414` = 활성 · 제외 아님(태그는 보지 않는다)

### 3.2 직원 목록을 내는 API

직원 목록 **전체**를 그대로 내는 경로는 없다. 있는 것은 다음 4곳이다(코드).

| 경로 | 내는 것 | 기준 | 위치 |
|---|---|---|---|
| `GET /api/reservations/form` | `staff[]{staffId, name}` · `defaultAssigneeStaffId` · `counselors[]{staffId, name}` | `staff` = 활성 · 제외 아님 / `counselors` = `_counselors` | `api/reservations.py:82` → `service/reservations.py:394-432` |
| `GET /api/reservations/{id}` | `counselors[]{staffId, name, busyRoom}`(상담 단계가 있을 때만) | `_counselors` | `api/reservations.py:115` → `service/reservations.py:532-535` |
| `GET /api/board` | `doctors[]{id, name, busy, busyRoom}` | `is_doctor` | `api/board.py:54` → `service/board_service.py:27-31` · `domain/rules.py:44-45` |
| `GET /api/chat/people` | `{id, name, role}` | **ccc 로그인 계정** 기준(활성 + 비밀번호 있음 · 나 뺌). KOS 직원 사본이 아니다 | `api/chat.py:84` → `service/chat.py:200-205` |

- 응답에 역할 태그 · 이메일 · 활성 여부를 내는 곳은 없다.
- ext(`api/ext.py`)의 경로 6개(`/menu` · `/customers/lookup` · `/reservations` · `/availability` · `/customers/visits` · `/customers/reservations`) 중 직원 · 병원 정보를 내는 것은 없다. `service/ext.py` 에도 직원 · 병원 참조가 없다.
- 병원 정보를 내는 CC API 도 없다.

---

## 4. 정할 것 (결정하지 않고 모음)

1. **「외주 직원」을 무엇으로 가르나.**
   - (가) 역할 이름 「CS팀(콜센터)」(내부 API · **C**)
   - (나) 공개 태그 집합이 정확히 `[CALL_COUNSELOR]`(지금 데모에서는 맞지만 설정이 바뀌면 깨진다)
   - (다) `roleTag=CALL_COUNSELOR` 필터(코디 · 관리자까지 21명)
   - (라) CC 에 직접 두는 목록(**D**)
   - 외주가 CS팀 하나뿐인지, 다른 역할(예: 촬영팀)도 외주인지는 사용자 확인이 필요하다.
2. **역할 이름을 내보낼지.** 연동처에 태그(7종 enum)만 줄지, KOS 역할 이름(15개 · 지점마다 다름)까지 줄지. 역할 이름을 주려면 내부 API(`account/v2` 또는 `role/v2`)에 기대는 곳이 하나 더 생긴다.
3. **이메일을 줄지.** 공개 응답에는 오지만 CC 사본은 버린다. 1차 브리프는 「직원 정보는 centurion 통합 계정」이라고 했다. 직원 식별자를 KOS 계정 id · ccc `staff.id` · centurion 계정 중 무엇으로 할지.
4. **비활성 직원을 넣을지**(데모 82명 중 24명). 넣는다면, KOS 에서 사라졌는데 CC 사본에만 남은 행과 일정에서만 생긴 `active=False` 행(§3.1)을 어떻게 볼지.
5. **`kos_exclude_account_ids` · 시스템 계정을 직원 목록에서도 뺄지.** 지금은 원장 · 상담사 목록에서만 뺀다.
6. **병원 정보 범위와 원천.**
   - 이름 · 주소 · 전화 같은 칸이 필요하면: 내부 `get-hospital` HAR 을 받아 확인할지(**E → C**), CC 설정에 둘지(**D**)
   - 운영 시간 · 구역 · 예약 그룹 · 타겟 국가 · 통화 · 부가세 중 무엇을 「병원 정보」로 볼지
   - 운영 시간을 병원 전체 값으로 줄지(내부 `get-default-operation-timetable` · 공개 없음), 예약 그룹별로 줄지(공개)
7. **역할 변경의 시점.** 직원 목록의 역할은 지금 값이다. 일정 담당자의 `role` 은 배정 당시 값일 수 있다(§2.2 추정). 연동처가 둘 중 무엇을 기대하는지.

## 5. 확인하지 못한 것

1. 내부 `get-hospital` 의 실제 응답(HAR 없음. JS 칸 이름만 봄). `addressContract` 의 하위 칸도 추정이다.
2. 내부 `get-default-operation-timetable` · `get-default-days-off` · `get-connect-apps` 의 응답 모양(이번에 펼치지 않음).
3. 내부 API 실호출(규칙상 안 함). 내부 계정 응답은 HAR 시점(11-16 `상담대기.har`) 값이다.
4. 외주 직원이 CS팀 말고 또 있는지(데이터에 외주 표시 칸이 없다).
5. 데모 `.env` 의 `KOS_EXCLUDE_ACCOUNT_IDS` · 시스템 계정이 몇 명을 가리키는지(id 값이라 보지 않았다).

## 6. 호출 기록

- 데모 공개: 토큰 교환 1번 + 조회 7번(`getAccounts` ×4 · `getZones` · `getReservationGroups` · `getTargetCountries`). 모두 200.
- 내부 호출 0번 · 쓰기 0번. 토큰 파일은 끝난 뒤 지웠다.
- 원자료(JSON)는 스크래치패드에만 있고 레포에는 없다.
