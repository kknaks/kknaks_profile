# 기존 고객 정보 수정(여권번호 · 국적 등) — KOS 경로

- 조사일: 2026-10-26 (KST) · 조사자: cc-prototype researcher (task_dacee03f38c8)
- 앞 판: `reservation-questionnaire-report.md`(아래 `Q§`), `reservation-read-report.md`(아래 `R§`)에서 이어진다
- 원천
  - `reference/2026-10-23-cc-overall-board/har/고객정보 수정.har` (gitignore · 항목 65개 · 02:15:40Z ~ 02:16:13Z)
  - KOS 웹앱 「고객 정보」 화면 JS(`core-cf.kos-solution.com/visitor-information/…_v0.0.157.js`, 공개로 받을 수 있는 정적 파일 81개)
  - 공개 스펙 openapi.yaml 1.0.1(2026-10-26 받음)
- 표기
  - **확인**: HAR 에 찍혔거나 데모에서 조회해서 본 것
  - **JS**: 웹앱 코드에 적힌 것(요청을 만드는 코드). 실제로 호출해 보지는 않았다
  - **스펙**: openapi.yaml 에 적힌 것
  - **추정**: 해석
- **KOS 쓰기는 0건이다.** `update-visitor-personal-information` 등은 HAR 과 JS 로만 읽었다
- 리포트에는 id · 토큰 · 이름 · 연락처 · 여권번호 · 주소 · 생년월일 값을 적지 않았다. 모양만 적는다

---

## 0. 요약

- **기존 고객의 여권 · 국적을 고치는 길은 내부 API 하나다.** 경로는 `POST api.kos-solution.com/tenants/{tenantId}/visitor/v2/commands/update-visitor-personal-information` 이다
  - JS 기준으로 받는 필드: `id · name · phoneticName · phoneNumber · additionalPhoneNumber · email · dateOfBirth · gender · registrationNumber · foreignRegistrationNumber · passportNumber · passportSurname · passportGivenNames · passportExpiryDate · address{address, detailedAddress, zipCode} · nationality · language · snsInfo`
  - **스캔 값 전부가 들어갈 칸이 있다.** HAR 의 실제 수정에서 생년월일 · 여권 성이 바뀐 것을 확인했다
  - 공개 스펙을 다시 grep 했다. 쓰기 25개 중 기존 고객을 고치는 작업은 **없다.** 고객 쪽 쓰기는 `submitVisitorQuestionnaire` · `registerVisitorImages` · `disableAdvertisingAgreementToVisitors` 와 예약 생성(신규 고객)뿐이다
- **고객 수정은 두 묶음으로 나뉜다**(JS)
  - ① 개인 정보: `update-visitor-personal-information`
  - ② 관리 정보: `update-visitor-management-information` = `memo`(주의사항 후보, Q-37) · 유입 · 추천인 · 고객 유형 · 분류 · 담당 의사/상담사 · 동의 3개 · `customAttributes[]`
  - ①로 수정했을 때 ②에 속한 필드(유입 id 등, 값이 있던 것)는 **그대로 남았다**(확인)
  - **① 안에서 본문에 넣지 않은 필드가 지워지는지는 판단할 수 없었다.** HAR 본문에 없던 휴대폰 · 이메일 · 만료일 · SNS 는 수정 전에도 비어 있었다 → Q-40
- **수정 결과는 공개 API 에도 보인다.** 지금 데모에서 공개 `getVisitor` 로 같은 고객을 조회했다. 바뀐 생년월일 · 여권 성이 내부 응답과 같았다(확인). 단, 공개 `getVisitor` 에는 여권번호 · 만료일 · 국적 외 항목이 대부분 없다(키 9개)
- **중복 고객 찾기는 공개 API 에도 있다**(`findDuplicatedVisitorId`). 내부 `find-duplicated-visitor` 와 같은 조건이다
  - 조건 순서는 스펙에 적혀 있다: `name+phone` → `passportNumber` → `snsInfo` → `email` → `name+birthDateUtc`
  - 여권 성 · 이름은 조건이 아니다
  - 데모 조회 결과: 이름 + 생년월일만 일치로 나왔다. 이름만, 여권 성만, 생년월일만으로는 0건이었다
- **국적은 ISO 3166-1 alpha-2 문자열이다**(본문 `"KR"`). KOS 코드 표가 아니다. `get-codes` 의 분류(유입 · 고객 분류 · 이미지 분류 · 촬영 장비)에도 국적 · 언어는 없다
  - `get-target-countries` 는 국적 목록이 아니라 상품 가격용 「타겟 국가」다(데모 4행: `KR` 2 · `ETC` 2, 코드가 겹친다)
- **신분 확인 「상태」를 둘 정해진 칸은 없다.** 고객 커스텀 속성(`customAttributes`)이 후보다. 데모에는 정의가 **0개**이고, 정의를 만드는 것은 내부 쓰기(`create-custom-attribute-definition`)다 → Q-44
- 정할 것은 **11개**다(Q-39 ~ Q-49)

---

## 1. HAR 인벤토리

항목 65개 = KOS API 34 + KOS 정적 파일(js 8 · svg 2) + OPTIONS 6 + Datadog 12 + Amplitude 3. 아래 표는 **KOS API 34건 전부**다. 모두 POST · `api.kos-solution.com/tenants/{tenantId}/…` 이고 `Authorization` 헤더는 내보낼 때 빠졌다(앞 판과 같다). `kos-client-uri` 는 모두 `…/reservation/schedule/?visitorId={visitorId}&tab=reservation` 꼴이다. 즉 **KOS 예약 화면에서 고객 상세를 연 상태**다(확인). 「단계」는 시각을 보고 묶었다.

| # | 시각(Z) | 경로 | 요청 본문 키 | 응답 모양 (건수) | 단계 · 용도 |
|---|---|---|---|---|---|
| 0 | 02:15:40.077 | `role/v2/queries/get-roles` | — | `data[{id,name,roleTags[int]}]` (15) | A 화면 처음 열기 |
| 1 | 40.079 | `schedule/zone/room/v1/queries/get-rooms` | `zoneId` | `data[{id,zoneId,title,order}]` (28) | A |
| 3 | 40.284 | `account/v2/queries/get-accounts` | `roleTag:DOCTOR` | `data[계정]` (13) | A |
| 4 | 40.284 | `account/v2/queries/get-accounts` | `roleTag:COUNSELOR` | (22) | A |
| 7 | 46.055 | `visitor/v2/queries/get-visitors` | `indexOfPage · countInPage` | `data[고객 상세 모양]` (10) + `count` | B 고객 목록 1쪽. JS 상 검색 조건: `chartNumber · visitorName · phoneNumber · dateOfBirth · doctorId · counselorId · sort` |
| 9 | 51.008 | `role/v2/queries/get-roles` | — | (15) | C 고객 상세 열기 |
| 12 | 52.382 | `visitor/v2/queries/get-visitor` | `id` | `data{고객}` — §3 | C **수정 전 #1** |
| 13 | 52.383 | `schedule/v1/queries/get-payment-required-tasks` | `visitorId` | `data[]` (0) | C 수납이 필요한 작업 |
| 14 | 52.455 | `consultation/v1/queries/get-consultations-by-visitor-id` | `visitorId` | `data[]` (0) | C 상담 기록 |
| 15 | 52.456 | `visitor/questionnaire/v1/queries/get-questionnaire-submit/legacy` | `visitorId` | 400 `visitorId NotFound` | C **직원 화면이 고객 상세에서 문진 답을 부르는 곳**(이 고객은 제출 없음). Q§ Q-28 의 답이다 |
| 16 | 52.457 | `meta/codes/v1/queries/get-codes` | `category:FUNNEL` | `data[{id,category,name,order,closed,default}]` (13) | C 유입 코드 |
| 17 | 52.457 | `meta/codes/v1/queries/get-codes` | `category:FUNNEL_CATEGORY` | (0) | C |
| 18 | 52.460 | `purchase/prepaid-card/v1/queries/get-prepaid-card-summaries` | `visitorId · available` | (0) | C 선불카드 |
| 19 | 52.463 | `purchase/prepaid-card/v1/queries/get-visitor-prepaid-card-balance` | `visitorId` | `data{remainingBalance, remainingPoint}` | C |
| 20 | 52.465 | `ticket/v1/queries/get-ticket-bundles` | `visitorId · sort` | `{}` | C 시술권(없음) |
| 21 | 52.465 | `schedule/v1/queries/get-schedule-summaries` | `visitorId · sort` | `data[일정 요약]` (1) | C 일정 이력 |
| 29 | 56.824 | `procedure-menu/target-countries/v1/queries/get-target-countries` | — | `data[{code,order}]` (4) | D 수정 창 열기 — §5 |
| 31 | 56.825 | `meta/codes/v1/queries/get-codes` | `FUNNEL` | (13) | D |
| 32 | 56.826 | `meta/codes/v1/queries/get-codes` | `FUNNEL_CATEGORY` | (0) | D |
| 33 | 56.826 | `meta/connect/v1/queries/get-connect-apps` | `{}` | (0) | D 연결 앱(KOS Connect) |
| 34 | 56.827 | `account/v2/queries/get-accounts` | `DOCTOR` | (13) | D 담당 의사 선택지 |
| 35 | 56.828 | `account/v2/queries/get-accounts` | `COUNSELOR` | (22) | D 담당 상담사 선택지 |
| 36 | 56.828 | `account/v2/queries/get-accounts` | `{}` | (79) | D 추천인(직원) 선택지(추정) |
| 37 | 56.829 | `procedure-menu/visitors/queries/get-visitors` | `sort{by:order}` | (0) | D 고객 유형 목록으로 보인다(추정) |
| 38 | 56.829 | `visitor/v1/queries/get-custom-attribute-definitions` | `{}` | `data[]` (0) | D **커스텀 속성 정의** — 데모 0개 |
| 39 | 56.830 | `visitor/v2/queries/get-visitor` | `id` | `data{고객}` | D 수정 전 #2 |
| 47 | 56.925 | `security/v2/queries/check-message-permission` | `message: "protos.visitor.UpdateVisitorPersonalInformationCommand"` | `data{available:true}` | D 수정 권한 확인 — §7 |
| 49 | 57.018 | `meta/codes/v1/queries/get-codes` | `category:VISITOR_CATEGORY` | `data[{…,color}]` (7) | D 고객 분류 |
| 50 | 57.111 | `visitor/v2/queries/get-visitor` | `id` | `data{고객}` | D 수정 전 #3(#12 · #39 와 같다) |
| 56 | 02:16:13.518 | `visitor/v1/queries/find-duplicated-visitor` | `name · birthDateUtc · passportSurname` | `{}`(일치 없음) | E [저장] 직전 중복 확인 — §4 |
| 58 | 13.579 | **`visitor/v2/commands/update-visitor-personal-information`** | §2 | `{}` | E **저장(쓰기)** |
| 61 | 13.718 | `visitor/v2/queries/get-visitor` | `id` | `data{고객}` | E **수정 후** |
| 62 | 13.719 | `ticket/v1/queries/get-ticket-bundles` | `visitorId · sort` | `{}` | E 다시 그리기 |
| 63 | 13.787 | `ticket/v1/queries/get-ticket-bundles` | 같음 | `{}` | E |

**합계**: 34행 = HAR 의 KOS API 34건. 쓰기는 #58 하나다. 경로로는 21종이다.

웹앱 JS 에 있는 고객 관련 내부 작업 전부(`visitor-information` 묶음, 경로 문자열 grep)
- 조회: `visitor/v2/queries/get-visitor · get-visitors · get-visitors-by-ids · search-visitors` · `visitor/v1/queries/find-duplicated-visitor · get-custom-attribute-definitions` · `v1/visitor/queries/find-visitor` · `visitor/files/v1/queries/get-visitor-files` · `visitor/questionnaire/v1/queries/get-questionnaire-submit` · `schedule/v2/queries/get-schedules-by-visitor` 등
- 쓰기: **`visitor/v2/commands/update-visitor-personal-information`** · **`visitor/v2/commands/update-visitor-management-information`** · `v1/visitor/commands/update-visitor`(옛 경로, 같은 묶음 안에 남아 있다) · `v1/visitor/commands/create-visitor` · `visitor/v1/commands/create · update · delete-custom-attribute-definition` · `visitor/files/v1/commands/generate-presigned-file-url · create-visitor-file · change-visitor-file-name · delete-visitor-files · generate-signed-file-urls · register-visitor-file-download-reason` · `visitor/questionnaire/v1/commands/issue-questionnaire-link · delete-questionnaire-submit` · `visitor/v1/commands/issue-link-line-information-token · unlink-line-information` · `delete-visitor-processor/v1/commands/delete-visitor` · `ticket/v1/commands/generate-arbitrary-ticket`

---

## 2. `update-visitor-personal-information` 해부

### 2.1 필드 (HAR #58 본문 + 웹앱 JS 의 요청 만드는 코드)

| 필드 | HAR 본문에 | 형식(모양) | JS 에서 | 메모 |
|---|---|---|---|---|
| `id` | ✔ | 24자 id | 그대로 | 고객 id |
| `name` | ✔ | 문자열 | 그대로 | 표시 이름. 이번에는 수정 전과 같은 값을 보냈다 |
| `phoneticName` | ✔(빈 문자열) | 문자열 | 그대로 | 한글 발음 |
| `phoneNumber` | ✗ | — | 그대로 | 휴대폰. 오류 `phoneNumber NotAvailable` · `countryCode NotAvailable` 처리 코드가 있다(JS) |
| `additionalPhoneNumber` | ✗ | — | 그대로 | 추가 번호 |
| `email` | ✗ | — | 그대로 | **고객 이메일 칸이 여기 있다.** 다만 `get-visitor` 응답에는 비어 있으면 키가 보이지 않는다 |
| `dateOfBirth` | ✔ | `yyyy-MM-dd 00:00:00.000Z`(JS: `format(…, "yyyy-MM-dd 00:00:00.000'Z'")`) | 날짜가 있을 때만 | 날짜를 **UTC 0시**로 보낸다 |
| `gender` | ✔ | `GENDER_UNSPECIFIED · MALE · FEMALE` | 있을 때만 | |
| `registrationNumber` | ✔(빈 문자열) | 문자열 | 그대로 | 주민등록번호 |
| `foreignRegistrationNumber` | ✔(빈 문자열) | 문자열 | 그대로 | 외국인등록번호 |
| `passportNumber` | ✔(빈 문자열) | 문자열 | 그대로 | **여권번호** |
| `passportSurname` | ✔ | 영문 대문자(3자 모양) | 그대로 | **여권 성.** 이번 수정으로 들어갔다(확인) |
| `passportGivenNames` | ✔(빈 문자열) | 문자열 | 그대로 | 여권 이름 |
| `passportExpiryDate` | ✗ | `yyyy-MM-dd`(JS) | 날짜가 있을 때만 | **여권 만료일** |
| `address` | ✔ | `{address, detailedAddress, zipCode}` | 그대로 | |
| `nationality` | ✔ | `"KR"` 모양 — ISO alpha-2 | 그대로 | **국적** |
| `language` | ✔(빈 문자열) | 문자열(데모의 다른 고객은 `zh-CN` 꼴) | 그대로 | 언어. 스펙 `reserveV2.visitorLanguage` 의 목록(`ko, ja, en, zh-CN, zh-yue, …`)과 같은 꼴로 보인다(추정) |
| `snsInfo` | ✗ | `{snsType, accountId}` | 있을 때만 | |
| 응답 | | `{}` (200) | | |

- **「필수」 여부는 알 수 없다.** 공개 스펙이 아니라서 required 표시가 없다. JS 는 `id` 를 늘 넣는다
- `memo` 는 **이 작업에 없다.** 관리 정보 쪽 `update-visitor-management-information` 에 있다(§2.3)

### 2.2 부분 수정인가, 통째로 덮어쓰기인가

| 근거 | 무엇을 보았나 | 판단 |
|---|---|---|
| 관리 정보 필드 | 본문에 없던 `visitorFunnel.funnelId` · `funnel`(값 있음), 동의 3개(값 있음)가 수정 뒤에도 그대로였다(#50 ↔ #61, 확인) | **관리 묶음은 건드리지 않는다** |
| 개인 정보 묶음 안 | 본문에 없던 `phoneNumber · additionalPhoneNumber · email · passportExpiryDate · snsInfo` 는 수정 **전에도 비어 있었다**. 수정 뒤에도 비어 있다 | **판단할 수 없음.** 빠진 필드를 「그대로 둔다」로 읽는지 「지운다」로 읽는지 HAR 로 가를 수 없다 → Q-40 |
| 웹앱의 보내는 방식 | JS 는 수정 창의 개인 정보 칸을 **모두** 모아 보낸다. 빈 칸은 빈 문자열로 보내고, 값이 없는 날짜 · 성별 · SNS 는 넣지 않는다 | 웹앱은 「읽고 → 고치고 → 묶음 전체를 다시 보낸다」. 서버가 빈 문자열을 「지움」으로 받는다면 묶음 단위 덮어쓰기다(추정) |

### 2.3 함께 있는 관리 정보 작업 (JS, HAR 에는 없음)

`POST …/visitor/v2/commands/update-visitor-management-information`
- 필드: `{id, memo, visitorFunnel, referrer, visitorType, visitorCategories[], doctor, counselor, aggrementPersonalInformation, aggrementAdvertisements, agreementInformationalNotification, customAttributes[]}`
- `customAttributes` 는 배열을 **통째로** 보낸다(`.map(…)`)
- `memo`(주의사항 후보) · 커스텀 속성을 바꾸려면 이 작업을 써야 한다. 이때 유입 · 분류 · 담당 · 동의 값도 함께 보내야 하는 것으로 보인다(추정) → Q-46

---

## 3. 수정 전후 비교

### 3.1 HAR 안에서 (#50 수정 전 ↔ #61 수정 후, 내부 `get-visitor` 키 전부)

| 키 | 전 → 후 | 본문 값과 |
|---|---|---|
| `dateOfBirth` | 빈칸 → `yyyy-MM-dd 00:00:00.000Z` | 같다 |
| `passportSurname` | 키 없음 → 값 | 같다 |
| `passportGivenNames` | 키 없음 → 빈 문자열 | 같다 |
| `phoneticName` | 키 없음 → 빈 문자열 | 같다 |
| `updatedDateTimeUtc` | **바뀜**(저장 시각) | — |
| 그 밖(`name · gender · nationality · registrationNumber · passportNumber · address · language · memo · snsInfo · funnel · 동의 …`) | 그대로 | `name · nationality` 는 원래 값을 그대로 보냈다 |

- 빈 값이 든 필드는 응답에서 키가 빠지는 경우가 있다(`passportSurname` 등은 「키 없음」 → 「빈 문자열」로 바뀌었다). 「키 없음」과 「빈 값」을 같은 것으로 다뤄야 한다(추정)
- 앞 판의 문진 제출은 `updatedDateTimeUtc` 를 바꾸지 않았다(Q§4.2). 이 작업은 바꾼다

### 3.2 지금 데모에서 같은 고객을 조회

| 조회 | 결과 |
|---|---|
| 내부 `visitor/v2/queries/get-visitor` | 200. HAR #61 과 **키 · 값이 모두 같다**(확인). 그 뒤로 바뀐 것은 없다 |
| 공개 `getVisitor` | 200. 키 `id · chartNumber · name · phoneNumber · dateOfBirth · gender · nationality · passportSurname · passportGivenNames`. **바뀐 생년월일 · 여권 성이 내부와 같은 값으로 보였다**(확인). 여권번호 · 만료일 · 주민번호 · 외국인등록번호 · 주소 · 언어 · SNS · 이메일 키는 공개 응답에 **없다** |

---

## 4. 중복 고객 찾기

| | 내부 `visitor/v1/queries/find-duplicated-visitor` | 공개 `findDuplicatedVisitorId` (`/visitor/open/v1/queries/find-duplicated-visitor-id`) |
|---|---|---|
| 요청 | JS: `name · phone · passportNumber · birthDateUtc(ISO, toISOString) · passportSurname · passportGivenNames · snsInfo(accountId 가 있을 때만) · email`. 빈 값은 넣지 않는다 | 같은 키 8개(스펙) |
| 조건 | 문서 없음 | 스펙: **`name+phone` → `passportNumber` → `snsInfo`(type+id) → `email` → `name+birthDateUtc` 순서.** `passportSurname · passportGivenNames` 는 「중복 조회 조건으로 사용되지 않는다」 |
| 응답 | 일치하면 `data{고객 전체 모양}`, 없으면 `{}` | 일치하면 `data: "<고객 id>"`, 없으면 `{}` |
| HAR #56 | `name · birthDateUtc · passportSurname` → `{}`. 저장 **전**이라 고객의 생년월일이 아직 비어 있었다 | — |

데모 조회(HAR #56 의 값을 써서, 조회만)

| 보낸 키 | 내부 | 공개 |
|---|---|---|
| HAR #56 그대로(이름 + 생년월일 + 여권 성) | 200 · 그 고객이 나옴 | 200 · 그 고객 id |
| 이름 + 생년월일 | 200 · 나옴 | 200 · 나옴 |
| 여권 성만 | 200 · `{}` | 200 · `{}` |
| 이름만 · 생년월일만 · 이름 + 여권 성 · 여권 성 + 생년월일 | 200 · `{}` | (부르지 않음) |
| 빈 본문 | 400 `InvalidCommandException` | — |
| 이름 + 생년월일을 ISO 가 아닌 `yyyy-MM-dd HH:mm:ss.SSSZ` 꼴로 | **500** `RuntimeException`(`Unknown Internal Service`) | — |

- `birthDateUtc` 는 **KST 0시를 UTC 로 바꾼 값**(`전날T15:00:00.000Z`)이다. 저장할 때 `dateOfBirth` 는 **UTC 0시**(`yyyy-MM-dd 00:00:00.000Z`)로 보낸다. 서로 기준이 다른데도 이번에는 일치했다 → Q-41
- 여권번호로 찾는 경우는 확인하지 못했다. 데모 고객 중 여권번호가 있는 사람을 찾지 않았다
- 시안 「예약 등록」(D§3.5)과 비교
  - 시안 고객 검색의 입력 4개(이름 · 연락처 · 생년월일 · 차트번호)는 내부 `get-visitors` 의 검색 조건(`visitorName · phoneNumber · dateOfBirth · chartNumber`)과 같다(JS)
  - 「이름이 같은 기존 고객이 있어요」 경고는 **이름만으로는 KOS 중복 확인에 걸리지 않는다.** 이름 + 생년월일, 또는 이름 + 휴대폰이어야 한다 → Q-43
  - 스캔 값(여권번호 · 이름 · 생년월일)으로 기존 고객을 찾는 데는 공개 `findDuplicatedVisitorId` 를 쓸 수 있다(스펙과 데모 확인)

---

## 5. 코드 표

| 조회 | 데모 결과 | 국적과의 관계 |
|---|---|---|
| `meta/codes/v1/queries/get-codes` `FUNNEL` | 13 · `{id(uuid), category, name, order, closed, default}` | 유입 |
| 〃 `FUNNEL_CATEGORY` | 0 | 유입 분류 |
| 〃 `VISITOR_CATEGORY` | 7 · `{…, color}` | 고객 분류(VIP 등) |
| 〃 `IMAGE_CATEGORY` · `IMAGE_EQUIPMENT` (이번에 더 불렀다) | 2 · 5 | 이미지 분류 · 촬영 장비. `registerVisitorImages` 의 `category · equipment` 에 넣는 값이다 |
| 〃 `ACCOUNT_STATUS` | 0 | — |
| 내부 `procedure-menu/target-countries/v1/queries/get-target-countries` = 공개 `getTargetCountries` | 4 · `{code, order}` · 코드는 `KR` 2 · `ETC` 2 | **국적 목록이 아니다.** 상품 가격용 「타겟 국가」다(스펙: 그 밖의 나라는 `ETC`) |

- 스펙 `CodeCategory` enum(`FUNNEL · EXPOSURE_CHANNEL · ETCETRA_PRODUCT_CATEGORY · IMAGE_EQUIPMENT · CALL_CONSULTATION_RESULT · IMAGE_CATEGORY · FUNNEL_CATEGORY · VISITOR_CATEGORY · ACCOUNT_STATUS · CONSULTATION_RESULT`)에 **국적 · 언어는 없다**
- **국적 값은 ISO 3166-1 alpha-2**다. 근거: 수정 본문 · 일정 응답의 `"KR · CN · JP"` 와 스펙 필드 설명. 화면의 국가 선택 목록은 KOS API 로 오지 않는다. 웹앱이 자체로 가진 것으로 보인다(추정) → Q-48

---

## 6. 스캔 값 대조표

넣는 길
- **공개**: 공개 작업
- **내부**: 내부 `update-visitor-personal-information`(P) 또는 `update-visitor-management-information`(M)
- **없음**: KOS 에 넣을 곳 없음

| # | 스캔 · 데스크 값 | 공개 (기존 고객) | 내부 | 보이는 곳(조회) | 앞 판 |
|---|---|---|---|---|---|
| S1 | 여권 영문 성 | 없음(신규 고객만 `reserveV2.visitorPassportSurname`) | **P `passportSurname`** — HAR 로 반영 확인 | 공개 `getVisitor` · 내부 `get-visitor` | Q§M1 · R Q-6 |
| S2 | 여권 영문 이름 | 없음(신규만 `…GivenNames`) | **P `passportGivenNames`** | 같음 | Q§M1 |
| S3 | 표시 이름(한글 · 원어) | 없음 | P `name` | 일정 `visitor.name` 등 | Q§M1 |
| S4 | 여권번호 | 없음(신규만 `visitorPassportNumber`) | **P `passportNumber`** — 칸은 HAR 본문에 있다(빈값). 실제로 값을 넣어 반영되는지는 미확인 | 내부 `get-visitor` 만. 공개 `getVisitor` 에는 키가 없다 | Q§M6 |
| S5 | 여권 만료일 | 없음 | **P `passportExpiryDate`**(`yyyy-MM-dd`, JS) | 내부만 | — |
| S6 | 국적 | 없음(신규만 `visitorNationality`) | **P `nationality`**(ISO alpha-2) | 공개 `getVisitor` · 일정 `visitor.nationality` | Q§M7 · R 9행 |
| S7 | 생년월일 | 문진 제출 `dateOfBirth`(반영 여부 미확인, Q§M4) | **P `dateOfBirth`** — HAR 로 반영 확인 | 공개 · 내부 · 일정 | R 12행 |
| S8 | 성별 | 문진 제출 `gender`(반영 확인, Q§M3) | P `gender` | 공개 · 내부 · 일정 | — |
| S9 | 주민등록번호 | 문진 제출 `registrationNumber`(스펙) | P `registrationNumber` | 내부만 | Q§M5 |
| S10 | 외국인등록번호 | 없음 | P `foreignRegistrationNumber` | 내부만 | — |
| S11 | 주소 | 문진 제출 `address`(반영 확인) | P `address{address, detailedAddress, zipCode}` | 내부만 | Q§M12 |
| S12 | 한글 발음 | 문진 제출 `phoneticName`(스펙) | P `phoneticName` | 일정 `visitor.phoneticName` | R 7행 |
| S13 | 휴대폰 · 추가 번호 | 문진 제출 `phone` | P `phoneNumber` · `additionalPhoneNumber` | 공개 · 일정 | Q§M8 |
| S14 | 이메일 | 없음(문진 답 · 신규만) | **P `email`** | 응답에 키가 보인 적이 없다(비어 있어서로 보인다, 추정) | Q§M9 |
| S15 | SNS · 언어 | 없음(신규만) | P `snsInfo` · `language` | 일정 `visitor.snsInfo` / 내부 `language` | Q§M10 · M21 |
| S16 | 신분증 · 여권 **이미지** | **`generateUploadingImageUrl` → PUT → `registerVisitorImages`**(source · category · equipment) | `visitor/files/v1/commands/generate-presigned-file-url → create-visitor-file`(고객 파일) | 공개 조회 없음 · 내부 `get-visitor-files` | Q§M16 · Q-35 |
| S17 | 신분 확인 **상태**(확인 완료/미확인) | **없음** | 정해진 칸 없음. 후보는 M `customAttributes[]` — 데모 정의 0개, 정의를 만드는 것은 내부 쓰기 | 내부 `get-visitor.customAttributes` | Q§M15 · Q-35 → Q-44 |
| S18 | 스캔 기기 · 시각 · 「자동 입력됨」 | **없음** | 없음(커스텀 속성 후보) | — | Q§M16 |
| S19 | 주의사항(고객 공통 메모) | 없음 | **M `memo`** | 일정 `visitor.memo` · 내부 | R Q-13 · Q-37 → Q-46 |

---

## 7. 권한 확인 · 계정

- 웹앱은 저장 전에 `security/v2/queries/check-message-permission{message: "<명령 이름>"}` 을 부른다(HAR #47)
- 우리 시스템 계정으로 같은 조회를 해 봤다. 개인 정보 · 관리 정보 명령 모두 `available: true` 였다
  - 그런데 **없는 명령 이름 두 개를 넣어도 `true`** 였다(확인)
  - 이 조회로는 시스템 계정이 실제로 고객 수정 권한을 가졌는지 **판단할 수 없다** → Q-47
- 내부 쓰기는 시스템 계정 이름으로 남는다. 누가 스캔 · 수정했는지는 ccc 에만 남는다(workflow-v2 「인증 · 계정」과 같은 구조) → Q-49

---

## 8. 정할 것 (결정하지 않음) — 11개

| # | 자리 | 왜 정해야 하나 | 앞 판 |
|---|---|---|---|
| Q-39 | 기존 고객의 여권 · 국적 · 생년월일을 내부 `update-visitor-personal-information` 으로 넣을지 | 공개 API 로는 길이 없다. 내부 API 는 공식 계약이 아니다. 공개 API 추가를 KOS 에 요청할지도 포함한다 | Q-29 |
| Q-40 | 개인 정보 묶음 안에서 본문에 넣지 않은 필드가 지워지는가 | HAR 로는 가를 수 없다(빠진 필드가 원래 비어 있었다). 웹앱처럼 「get-visitor 로 읽고 → 고치고 → 묶음 전체를 보낼지」. 아니면 데모에서 쓰기 시험을 한 번 허가할지 | — |
| Q-41 | 날짜 기준 | 저장은 `yyyy-MM-dd 00:00:00.000Z`(UTC 0시), 중복 확인은 KST 0시의 ISO, 만료일은 `yyyy-MM-dd` 다. 스캔한 날짜를 어느 꼴로 바꿀지. ISO 가 아닌 꼴을 보내면 500 이 났다 | — |
| Q-42 | 스캔 이름을 어디에 넣을지 | `name`(표시 이름)과 `passportSurname/GivenNames` 가 따로 있다. 스캔한 영문 이름으로 `name` 까지 바꿀지(한글 · 원어 이름이 덮인다). 카드 이름(R Q-6)을 무엇으로 보일지와 이어진다 | R Q-6 |
| Q-43 | 중복 고객 확인 | 스캔 뒤 공개 `findDuplicatedVisitorId` 로 찾을지, 어떤 키(여권번호 · 이름 + 생년월일 · 이름 + 휴대폰)로 찾을지. 시안의 「이름이 같은 고객」 경고는 KOS 조건과 다르다(이름만으로는 안 걸린다) | — |
| Q-44 | 신분 확인 상태 · 스캔 기기 · 시각을 둘 자리 | KOS 에 정해진 칸이 없다. 커스텀 속성 정의를 만들지(KOS 설정 쓰기 · 지점마다), ccc 에만 둘지 | Q-35 |
| Q-45 | 신분증 이미지 저장 | 공개 `registerVisitorImages`(조회 API 없음) / 내부 고객 파일(`visitor/files`) / ccc. 신분증 이미지를 KOS 에 남겨도 되는지(개인정보)도 포함한다 | Q-35 |
| Q-46 | 주의사항 = 관리 정보 `memo` 를 내부로 쓸지 | 관리 묶음은 유입 · 분류 · 담당 · 동의 · 커스텀 속성을 함께 보내는 것으로 보인다. 덮어쓰기 위험이 Q-40 과 같다 | Q-37 |
| Q-47 | 시스템 계정의 고객 수정 권한 | 권한 확인 조회가 아무 이름에나 true 를 준다. 실제 쓰기 한 번으로만 알 수 있다 | — |
| Q-48 | 국적 선택 목록 | KOS 코드 표에 국적이 없다. ISO 목록을 ccc 가 가질지. 스캔 결과(여권 MRZ 의 ISO alpha-3)를 alpha-2 로 바꿔야 한다 | R Q-8 |
| Q-49 | 수정 이력 | KOS 에는 `updatedDateTimeUtc` 만 남고 수정자는 시스템 계정이다. 누가 무엇을 스캔 · 수정했는지를 ccc 에 남길지 | — |

---

## 9. 호출 기록 · 빠진 행 점검

**호출**(2026-10-26, 데모 테넌트, 조회만)
- 공개(데모 키): `exchange-token` 2 + `getVisitor` 1 · `getTargetCountries` 1 · `findDuplicatedVisitorId` 3 — 모두 200
- 내부(시스템 계정 Bearer): sign-in 4 + 조회 25
  - `visitor/v2/queries/get-visitor` 1 · `get-custom-attribute-definitions` 1 · `get-target-countries` 1 · `get-codes` 6 — 모두 200
  - `find-duplicated-visitor` 9 — 200 ×7 · 400 ×1 · 500 ×1
  - `check-message-permission` 7 — 모두 200
- 정적 파일: KOS 웹앱 앱 껍데기 1 · `visitor-information` JS 81개(GET, 공개 정적 파일)
- **쓰기 0건**, 운영 키 0건

**빠진 행**
- HAR: 항목 65개 = KOS API 34 + 정적 10 + OPTIONS 6 + Datadog 12 + Amplitude 3. 인벤토리 34행 = KOS API 34건
- 브리프 §3-2 에서 짚은 필드
  - `passportNumber · passportExpiryDate · passportSurname/GivenNames · nationality · dateOfBirth · gender · registrationNumber · phoneticName · language · email · snsInfo` → §2.1 에 모두 있다
  - `memo` → §2.3
- 스캔 값 대조표 19행(S1~S19). 브리프가 짚은 신분 확인 상태 · 커스텀 속성은 S17 이다
- 정할 것 11개(Q-39 ~ Q-49)
