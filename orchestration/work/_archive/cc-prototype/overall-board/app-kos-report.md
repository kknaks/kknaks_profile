# 앱 KOS 확인 — 국적 · 언어 · 여권번호 수정 · 문진 언어 · 공개 문진 제출

- 조사일: 2026-10-27 (KST) · 조사자: cc-prototype researcher (task_1fb354020521)
- 앞 판: `reservation-visitor-update-report.md`(아래 `V§`), `reservation-questionnaire-report.md`(아래 `Q§`)에서 이어진다
- 원천
  - `reference/2026-10-23-cc-overall-board/har/국적_언어_여권번호변경.har` (gitignore · 항목 22개 · 10:21:36Z ~ 10:21:45Z)
  - KOS 웹앱 JS — 앞 판이 받아 둔 정적 파일(`visitor-information-client_v0.0.157` · `reservation-client_v0.0.541` · `purchase-client_v0.0.263`, 2026-10-26 받음). 이번에 다시 받지 않았다. 지금 배포본과 버전이 다를 수 있다
  - 공개 스펙 `https://developers.kos-solution.com/openapi.yaml` 1.0.1(2026-10-26 받은 사본)
  - 데모 실호출(2026-10-27, 데모 테넌트) — §7
- 표기
  - **확인**: HAR 에 찍혔거나 데모에서 호출해서 본 것
  - **JS**: 웹앱 코드에 적힌 것(호출해 보지 않음)
  - **스펙**: openapi.yaml 에 적힌 것
  - **추정**: 해석
- **KOS 쓰기는 2건이다**(브리프가 허가한 것만): 내부 `update-visitor-personal-information` 1 · 공개 `submitVisitorQuestionnaire` 1. 대상은 둘 다 앞 판이 만든 시험 고객 1명이다
- 리포트에는 테넌트 · 고객 · 설문 id, 토큰, 이름 · 연락처 · 여권번호 · 주소 · 생년월일 값을 적지 않았다. 모양 · 필드 이름 · 타입 · 코드 값(국적 · 언어 코드)만 적는다

---

## 0. 요약

- **KOS 고객에 언어 칸이 있다.** 이름은 `language`, 값은 문자열 코드 하나(`"ko"` · `"zh-CN"` 꼴)이고 비어 있으면 `""` 다. HAR 에서 사용자가 이 칸을 `""` → `"ko"` 로 바꿨고, 데모에서 `""` → `"zh-CN"` 으로 바꾼 것도 반영됐다(확인)
  - `_RESUME` 10-27 줄의 「KOS 고객 정보에 언어 칸 없음」은 **고쳐야 한다.** 칸은 있다. 다만 문진 「사용 가능한 언어」 답이 이 칸으로 가지 않는 것은 맞다(Q§4.2, 이번 공개 제출에서도 확인)
  - 값 목록(JS enum, 17개): `ko · ja · en · zh-CN · zh-yue · es · th · ru · id · ms · vi · mn · uz · nl · de · pt · etc`. 스펙 `reserveV2.visitorLanguage` 의 「지원 목록」과 같다
- **언어 칸이 보이는 곳은 내부 `get-visitor` 하나뿐이다.** 공개 `getVisitor`, 공개 일정(`getSchedulesByVisitor` · `getScheduleDetail`)의 `visitor`, ccc 가 쓰는 내부 예약 조회(`get-schedules-for-reservation`)의 `visitor` 에는 **언어 키가 없다.** 국적(`nationality`)은 모두에 있다(확인)
- **문진 양식의 번역 언어는 6개다**: `ko · ja · zh-Hans · zh-Hant · en · id`. 고객 `language` 와 **코드 꼴이 다르다**(`zh-CN` ↔ `zh-Hans`, `zh-yue` ↔ `zh-Hant`). KOS 웹앱에 이 둘을 잇는 변환이 있다(`zh-CN → zh-Hans` · `zh-yue → zh-Hant`, JS)
- **KOS 웹앱에 이미 「국적 → 언어」 규칙이 있다**(JS · 영수증 · 예약 문서용). `resolveDefault` = ① 고객 `language` → ② 고객 국적 대응표 → ③ 병원 국적 대응표 → ④ `en`. 국적 대응표는 18개 나라(§3.3). 결정 재료로만 적는다
- **`update-visitor-personal-information` 은 HAR 대로 보내면 원하는 칸만 바뀐다**(데모 확인). 보낸 13개 키 중 바꾼 3개(국적 · 언어 · 여권번호)만 바뀌었고, 나머지 개인 · 관리 정보 34개 키는 그대로였다. 응답은 `{}`(200). 여권번호는 보낸 값 그대로 저장되고 **내부 조회에만** 보인다
  - 본문에 넣지 않은 `snsInfo`(`{snsType:"etc", accountId:""}`)가 HAR · 데모 둘 다에서 그대로 남았다. **「빠진 필드 = 지움」이 아니라는 약한 근거**다(accountId 가 빈 값이라 결정적이지 않다 → Q-145)
- **공개 `submitVisitorQuestionnaire` 1회 — 200**, `getQuestionnaireSubmit` 로 16줄 답이 순서 · 값 그대로 확인됐다. **고객 정보가 바뀌는 칸은 legacy 경로(Q§4.2)보다 많다**(§5.3)
  - 바뀜: 성별 · 휴대폰(맨 앞 0 빠짐) · 주소(비어 있던 주소에도) · **생년월일**(앞 판에서 판단 못 함 → 이번에 반영 확인) · **한글 발음** · **개인정보 동의**(false → true)
  - 안 바뀜: 이름 · 언어 · 국적 · 여권 · 이메일 · SNS · `updatedDateTimeUtc`
- 정할 것은 **9개**다(Q-145 ~ Q-153)

---

## 1. HAR 인벤토리 — `국적_언어_여권번호변경.har`

항목 22개 = KOS API 9(+ OPTIONS 2) + KOS 정적 svg 9 + Datadog 4. 테넌트는 `.env` 의 데모 테넌트와 같다(확인 · §7). `kos-client-uri` 는 모두 `…/reservation/schedule/?visitorId={id}&tab=reservation&historyMenu=reservationHistory` 꼴이다 — **KOS 예약 화면에서 고객 상세를 연 상태**다. `Authorization` 헤더는 내보낼 때 빠졌다(앞 판과 같다). 고객은 앞 판(이동 단계 시험)이 만든 `[ccc 시험]` 고객 중 하나다.

| # | 시각(Z) | 경로 (`api.kos-solution.com/tenants/{tenantId}/…`) | 요청 본문 키 | 응답 | 용도 |
|---|---|---|---|---|---|
| 0 | 10:21:36.770 | `role/v2/queries/get-roles` | — | 200 | 화면 열기 |
| 1 | 36.771 | `schedule/v1/queries/get-schedule-summaries` | `visitorId · sort` | 200 | 고객 일정 이력 |
| 2–10 | 36.799 | `core-cf…/visitor-information/*.svg` | — | 200/304 | 정적 아이콘 9 |
| 13 | 45.649 | `visitor/v1/queries/find-duplicated-visitor` | `name · passportNumber · birthDateUtc` | 200 `data{고객 전체}` | **[저장] 직전 중복 확인.** 새 여권번호를 넣어 불렀다. 이름 + 생년월일로 **자기 자신**이 걸렸다(응답 id = 수정 대상 id). 응답이 저장 **전** 고객 상태라 아래 비교의 「전」으로 쓴다 |
| 14 | 45.650 | OPTIONS #13 | — | — | CORS |
| 15 | 45.726 | **`visitor/v2/commands/update-visitor-personal-information`** | §2.1 의 13개 키 | 200 `{}` | **저장(쓰기)** |
| 16 | 45.727 | OPTIONS #15 | — | — | CORS |
| 17 | 45.870 | `visitor/v2/queries/get-visitor` | `id` | 200 `data{고객}` | **수정 후** |
| 18 · 20 | 45.870 · 45.942 | `ticket/v1/queries/get-ticket-bundles` | `visitorId · sort` | 200 `{}` | 다시 그리기 |
| 11 · 12 · 19 · 21 | — | Datadog RUM | — | — | — |

**합계**: KOS API 9건(쓰기 1 · 조회 6 · OPTIONS 2) + 정적 9 + Datadog 4 = 22. 수정 **전** `get-visitor` 는 HAR 에 없다(수정 창은 이미 열려 있었다). #13 의 응답이 전 상태 역할을 한다.

- 중복 확인에서 **자기 자신이 걸려도 웹앱은 그대로 저장했다**(#13 → #15, 76ms 뒤). 웹앱은 걸린 고객이 수정 대상과 같으면 넘어가는 것으로 보인다(추정)
- `birthDateUtc` 는 KST 0시의 UTC(`전날T15:00:00.000Z`), 저장 `dateOfBirth` 는 `yyyy-MM-dd 00:00:00.000Z` — V§4 · Q-41 과 같다

---

## 2. `update-visitor-personal-information` 해부

### 2.1 HAR #15 본문 — 13개 키

| 필드 | 형식 | HAR 에서 | 메모 |
|---|---|---|---|
| `id` | 24자 id | 그대로 | |
| `name` | 문자열 | 원래 값 그대로 | |
| `phoneticName` | 문자열 | `""` | |
| `dateOfBirth` | `yyyy-MM-dd 00:00:00.000Z` | 원래 값 그대로 | |
| `gender` | `GENDER_UNSPECIFIED · MALE · FEMALE` | 그대로 | |
| `registrationNumber` | 문자열 | `""` | |
| `foreignRegistrationNumber` | 문자열 | `""` | |
| `passportNumber` | 문자열(이번 값 7자) | **`""` → 값** | 여권번호 |
| `passportSurname` · `passportGivenNames` | 문자열 | `""` | 여권 영문 성 · 이름. 이번에는 안 넣었다 |
| `address` | `{address, detailedAddress, zipCode}` | 모두 `""` | |
| `nationality` | ISO 3166-1 alpha-2 | **`KR` → `JP`** | |
| `language` | 언어 코드 문자열 | **`""` → `ko`** | §3 |
| 본문에 없음 | — | `phoneNumber · additionalPhoneNumber · email · passportExpiryDate · snsInfo` | JS 는 값이 있을 때만 넣는다(V§2.1). 이 고객은 휴대폰 · 이메일 · 만료일이 없고, `snsInfo` 는 `{snsType:"etc", accountId:""}` 였다 |
| 응답 | `{}` (200) | | |

V§2.1 의 JS 필드 목록과 같다. 새 필드는 없다.

### 2.2 전 ↔ 후 (HAR #13 응답 ↔ #17, 내부 고객 키 37개)

| 키 | 전 → 후 | 본문 값과 |
|---|---|---|
| `nationality` | `KR` → `JP` | 같다 |
| `language` | `""` → `ko` | 같다 |
| `passportNumber` | `""` → 값 | 같다 |
| `passportSurname` · `passportGivenNames` · `phoneticName` | 키 없음 → `""` | 같다 |
| `updatedDateTimeUtc` | 바뀜 | — |
| 그 밖 30개(`name · dateOfBirth · gender · address · registrationNumber · foreignRegistrationNumber · snsInfo · memo · funnel · visitorFunnel · 동의 3개 · doctor · counselor · customAttributes …`) | 그대로 | — |

- **본문에 없던 `snsInfo` 가 그대로 남았다.** `snsType` 에 값(`etc`)이 있었으니 「빠진 필드를 지운다」면 지워졌어야 한다. 다만 `accountId` 가 빈 값이라 서버가 「빈 SNS」로 보고 손대지 않았을 가능성도 있다 → Q-145
- 「키 없음」 → `""` 로 바뀌는 것은 V§3.1 과 같다

### 2.3 데모에서 같은 명령 1회 — 결과

§6.1. 요약하면 HAR 과 같다: 바꾼 3칸만 바뀌고 다른 키는 그대로였다.

---

## 3. 언어 칸

### 3.1 어디에 보이나 (데모 조회 · HAR 고객과 시험 고객 둘 다)

| 조회 | 언어 키 | 국적 키 |
|---|---|---|
| 내부 `visitor/v2/queries/get-visitor` | **`language`** | `nationality` |
| 내부 `v1/visitor/queries/get-visitor`(옛 경로) | **`language`** | `nationality` |
| 공개 `getVisitor`(`{id}`) | 없음(키 7~9개: `id · chartNumber · name · phoneNumber · dateOfBirth · gender · nationality` + 여권 성 · 이름이 있으면) | 있음 |
| 공개 `getSchedulesByVisitor` · `getScheduleDetail` 의 `visitor` | 없음(키 12개: `categories · chartNumber · dateOfBirth · gender · id · isNew · memo · name · nationality · phoneticName · snsInfo · visitorType`) | 있음 |
| 내부 `schedule/v2/queries/get-schedules-for-reservation`(ccc 예약 현황이 10초마다 부름)의 `visitor` | 없음(위와 같은 12개) | 있음 |
| 내부 `schedule/v1/queries/get-schedule-summaries` | 없음(고객 객체 없음) | 없음 |

→ ccc 가 고객 언어를 쓰려면 **고객마다 내부 `get-visitor` 를 한 번 더** 불러야 한다. 국적은 지금 받는 일정 응답에 이미 있다.

- 웹앱 예약 · 영수증 코드는 `visitor.registeredLanguage` 라는 이름으로 언어를 읽는다(JS). 어느 응답이 이 이름을 주는지는 이번에 찾지 못했다(위 6개 응답에는 없다)
- 공개 스펙에서 고객 언어를 받는 곳: `reserveV2.visitorLanguage`(「새 내원객을 생성할 때 저장」), `reserveByTimeSlot.visitorLanguageCode` · `getReservationTimeSlots.visitorLanguageCode`(「locale code」). **기존 고객의 언어를 고치는 공개 작업은 없다**(V§0 과 같다)

### 3.2 값 목록 (JS)

`visitor-information-client` · `reservation-client` 에 같은 enum 이 있다.

```text
ko · ja · en · zh-CN · zh-yue · es · th · ru · id · ms · vi · mn · uz · nl · de · pt · etc   (17)
```

- 스펙 `reserveV2.visitorLanguage` 설명의 「지원 목록: ko, ja, en, zh-CN, zh-yue, es, th, ru, id, ms, vi, mn, uz, nl, de, pt 등」과 같다(`etc` 만 스펙에 없다)
- 비어 있으면 `""` 다(데모 시험 고객 10명 중 HAR 고객 · 이번 시험 고객 외에는 모두 `""`, 확인)
- `zh-yue` 는 이름은 광둥어 태그지만 KOS 는 번체(`zh-Hant`)로 바꿔 쓴다(§3.3)

### 3.3 KOS 웹앱의 언어 결정 규칙 (JS · `reservation-client` · `purchase-client`)

문서(영수증 · 예약 안내) 언어를 고르는 코드다. 문진 화면 코드는 아니다.

```text
문서 언어 enum (17): ko · ja · zh-Hans · zh-Hant · en · th · es · ru · fr · id · ms · vi · mn · uz · nl · de · pt
normalize(고객 language): zh-CN → zh-Hans, zh-yue → zh-Hant, 그 밖은 그대로. enum 에 없으면(etc 등) 없음
fromNationality(국적):
  KR→ko · JP→ja · CN→zh-Hans · TW/HK/MO→zh-Hant · TH→th · ID→id · ES→es · RU→ru · FR→fr · DE→de · PT/BR→pt · US/GB/AU/NZ→en
  (그 밖 나라 → 없음)
resolveDefault = normalize(고객 language) ?? fromNationality(고객 국적) ?? fromNationality(병원 국적) ?? "en"
```

- 화면에서 직원이 고른 언어(`selectedLanguage`)가 있으면 그것이 먼저다(JS)
- **국적 대응표는 KOS 것이 이미 있다.** 대만 · 홍콩 · 마카오 = 번체, 중국 = 간체로 `_RESUME` 10-27 줄의 예시와 같다. 베트남 · 몽골 · 우즈베키스탄 · 말레이시아 등은 언어 enum 에는 있지만 국적 대응표에는 없다

### 3.4 문진 양식 언어와 맞추기

| | 고객 `language` | 문서 언어 enum | 문진 양식 번역 | 동의 약관 번역 |
|---|---|---|---|---|
| 한국어 | `ko` | `ko` | `ko` | (원문) |
| 일본어 | `ja` | `ja` | `ja` | `ja` |
| 영어 | `en` | `en` | `en` | `en` |
| 중국어 간체 | `zh-CN` | `zh-Hans` | `zh-Hans` | `zh` |
| 중국어 번체 | `zh-yue` | `zh-Hant` | `zh-Hant` | `zh` |
| 인도네시아어 | `id` | `id` | `id` | — |
| 태국어 · 스페인어 · 러시아어 · 말레이 · 베트남어 · 몽골어 · 우즈베크어 · 네덜란드어 · 독일어 · 포르투갈어 | 있음 | 있음 | **없음** | 없음 |
| 기타 | `etc` | 없음 | 없음 | 없음 |

- 문진 양식 코드 꼴은 **문서 언어 enum 과 같다**(`zh-Hans · zh-Hant`). 고객 `language` 는 `zh-CN · zh-yue` 꼴이라 한 번 바꿔야 한다. KOS 웹앱의 `normalize` 가 그 변환이다
- 고객 언어 17개 중 양식이 번역을 가진 것은 6개다. 나머지 고객 언어(예: `th`)와 국적 대응표에만 있는 언어(`th · es · ru · fr · de · pt`)는 양식에 번역이 없다 → Q-147
- **동의 약관 번역은 키가 다르다**(`ja · en · zh` — 간체 · 번체 구분 없음 · 확인). 양식 질문과 같은 코드로 고를 수 없다 → Q-148

---

## 4. 문진 양식 언어 — 데모 조회 (공개 `getVisitorQuestionnaire`)

- 응답은 `data` 로 감싸지 않은 객체다: `{name, phoneNumber, address, addressDetail, dateOfBirth, gender, pages[], agreements[]}`(확인). 스펙은 `data{…}` 로 적었다 — 스펙과 다르다. 미리 채워진 고객 값은 Q§1.3 과 같다
- 4쪽 · 15질문 · 답 70개(`CHECK_BOX` 54 · `SELECT_BOX` 15 · `INPUT_BOX` 1). Q§3.1 과 같다
- `agreements` 는 이번 응답에서 **빈 배열**이었다. 약관은 따로 `getQuestionnaireAgreements` 로 받는다(1건 · `PERSONAL_INFORMATION` · 필수)

번역 필드 모양

```text
pages[]                .translsMap.title.translation        {ko, ja, zh-Hans, zh-Hant, en, id}     4
pages[].questions[]    .translsMap.title.translation        {같은 6개}                              15
           .answers[]  .translsMap.title.translation        {같은 6개}                              69
           .answers[]  .translsMap.subText.translation      {같은 6개}  (isSubText:true 인 답)       12
           .answers[]  .translsMap = {}                     (이메일 INPUT_BOX 답 · title 도 "")      1
```

- 모든 번역 칸이 **6개 언어 모두 채워져 있다**(빈 번역 0개, 확인). 원문(`title` · `subText`)은 한국어다
- 번역은 **보여 주는 글자만** 바꾼다. 제출할 때 `answers[].title` · `parentQuestionTitle` 에는 원문(한국어)을 넣었다(이번 제출 · Q§3.1 의 legacy 제출 둘 다) — 고객이 본 언어는 제출에 남지 않는다 → Q-149
- 고객 설문 페이지 안내 문구(`get-intro/legacy`)도 같은 6개 언어다(Q§1.3)
- 6개 언어가 KOS 고정인지, 지점이 양식을 고쳐 늘릴 수 있는지는 **문서에 없음** · 확인 못 함

---

## 5. 공개 `submitVisitorQuestionnaire` — 데모 1회

### 5.1 보낸 것 (모양)

| 필드 | 보낸 값의 모양 | 왜 |
|---|---|---|
| `visitorId` | 시험 고객 id | |
| `name` | 고객 이름 + 「 문진」(고객 이름과 **다르게**) | 이름이 고객 정보로 가는지 보려고 |
| `dateOfBirth` | `yyyyMMdd` · 고객 값과 **다른** 날짜 | 앞 판에서 판단 못 한 생년월일 반영(Q§M4) |
| `gender` | `FEMALE`(고객은 `GENDER_UNSPECIFIED`) | |
| `phone` | `{countryCode:"82", phoneNumber: 11자리 시험 번호}` | 고객은 휴대폰 없음 |
| `address` · `addressDetail` | `[ccc 시험]` 문구 | 고객 주소는 비어 있었다 |
| `phoneticName` | 시험 문구 | 스펙 「고객 정보에도 반영」 |
| `registrationNumber` | **보내지 않음** | 가짜 주민번호가 형식 검사에 걸려 1회 시험을 날릴 위험이 있어 뺐다 |
| `agreements[]` | `getQuestionnaireAgreements` 1건 그대로 + `agreed:true` | 고객 개인정보 동의는 `false` 였다 |
| `answers[]` | 16줄(15질문마다 1개 + 언어 질문 「기타」 1개). 키 7개(Q§3.2). 이메일 `INPUT_BOX` 는 시험 주소, 「사용 가능한 언어」는 `일본어` + `기타`(`subText` 시험 문구), 예/아니오는 `아니오`, 나머지는 첫 선택지 | 언어 답이 고객 `language` 로 가는지 보려고 고객 언어(`zh-CN`)와 다른 `일본어` 를 골랐다 |

응답: **200 `{questionnaireId}`**(`data` 로 감싸지 않음 · 162ms).

### 5.2 `getQuestionnaireSubmit` 로 확인

- 200 · `data{id, visitorId, visitorName, phoneNumber, address, addressDetail, dateOfBirth, gender, phone{countryCode, phoneNumber}, phoneticName, createdDateTimeUtc, agreements[{…, agreed}], answers[16]{seq, questionId, questionTitle, answerId, answerTitle, memo}}`
- 16줄 모두 **보낸 순서 그대로** · `questionId` = `parentQuestionId` · `answerId` = `id` · `answerTitle` = `title` · `memo` = `INPUT_BOX` 면 `inputText`, 아니면 `subText`(확인). Q§4.1 과 같다. `seq` 는 모두 `""`
- `visitorName` · `dateOfBirth` · `gender` · `phoneticName` · `address` 는 **보낸 값**이다. `phone.phoneNumber` 는 보낸 11자리 그대로, 문자열 `phoneNumber` 는 `""`(공개 본문에는 문자열 휴대폰 칸이 없다)
- `agreements` 는 약관 1건 + `agreed:true`

### 5.3 고객 정보 — 제출 전 ↔ 뒤 (내부 `get-visitor` 키 전부)

| 필드 | 공개 제출(이번) | legacy 제출(Q§4.2) | 스펙 |
|---|---|---|---|
| `gender` | **바뀜**(보낸 값) | 바뀜 | 언급 없음 |
| `phoneNumber{countryCode, phoneNumber}` | **생김**(11자리 → **10자리**, 맨 앞 0 빠짐) | 같음 | 「갱신」 |
| `address{address, detailedAddress, zipCode}` | **비어 있다가 채워짐**(`zipCode` 는 `""`) | 같음 | 「기존 주소가 있을 때만」 — **스펙과 다르다(공개도)** |
| `dateOfBirth` | **바뀜**(보낸 날짜 · `yyyy-MM-dd 00:00:00.000Z` 로 저장) | 판단 못 함 | 언급 없음 — **스펙에 없는 반영** |
| `phoneticName` | **바뀜**(보낸 값) | legacy 에는 칸 없음 | 「반영」 — 스펙과 같다 |
| `aggrementPersonalInformation` | **false → true** | 판단 못 함 | 「type 이 있으면 동의 정보에 반영」 — 스펙과 같다. 관리 정보 묶음 칸인데 제출로 바뀐다 |
| `name` | **그대로**(제출 이름 ≠ 고객 이름) | 그대로 | 「설문에 저장할 이름」 |
| `language` | **그대로**(언어 답 `일본어` 와 다르다) | 그대로 | — |
| `nationality` · `passportNumber` · `snsInfo` · `memo` · `registrationNumber` | 그대로 | 그대로 | — |
| 이메일 | 고객 키 없음(답 `memo` 로만) | 같음 | — |
| `updatedDateTimeUtc` | **그대로** | 그대로 | — |

- 공개 `getVisitor` · 공개 일정 `visitor` 에도 바뀐 성별 · 생년월일 · 한글 발음이 보였다(확인). 이름은 그대로였다
- **정리**: 공개 경로는 legacy 와 같은 칸(성별 · 휴대폰 · 주소)을 바꾸고, 생년월일 · 한글 발음 · 동의를 **더** 바꾼다. 이름 · 언어 · 국적 · 여권은 바꾸지 않는다. 바꿔도 수정 시각은 남지 않는다 → Q-150 · Q-151

---

## 6. 데모 쓰기 ⓐ — 시험 고객 1명

### 6.1 `update-visitor-personal-information` 1회

| 단계 | 내용 |
|---|---|
| 대상 | 앞 판 시험 고객(`[ccc 시험] 이동 NN` 중 하나 · HAR 고객과 다른 사람). 쓰기 직전 다시 읽어 스냅샷과 같은지 확인했다 |
| 본문 | HAR #15 와 **같은 13개 키**. 읽은 값 그대로 + `nationality: KR → CN` · `language: "" → zh-CN` · `passportNumber: "" → 시험 문자열(9자, 실제 여권번호 아님)`. `snsInfo` 는 HAR 처럼 넣지 않았다(이 고객도 `{snsType:"etc", accountId:""}`) |
| 응답 | **200 `{}`** · 82ms |

다시 읽어 비교(필드마다)

| 조회 | 키 수 전 → 후 | 바뀐 키 |
|---|---|---|
| 내부 v2 `get-visitor` | 34 → 37 | `nationality`(=본문) · `language`(=본문) · `passportNumber`(=본문, 보낸 값 그대로) · `passportSurname` · `passportGivenNames` · `phoneticName`(키 없음 → `""`) · `updatedDateTimeUtc`. **그 밖 30개 그대로**(`snsInfo` 포함) |
| 내부 v1 `get-visitor` | 34 → 37 | v2 와 같다 |
| 공개 `getVisitor` | 7 → 9 | `nationality` · `passportSurname` · `passportGivenNames`(`""`). 여권번호 · 언어 키는 없다 |
| 공개 일정 `visitor` | 12 → 12 | `nationality` 만 |

- 시스템 계정으로 내부 고객 수정이 **실제로 된다**(V Q-47 의 답: 권한 있음)
- HAR 과 같은 결과다. 「읽은 묶음 전체 + 바꿀 칸만」으로 보내면 다른 칸은 안전하다(확인). 묶음에서 키를 **빼고** 보냈을 때 지워지는지는 시험하지 않았다(1회 허가) → Q-145

---

## 7. 호출 기록 · 데모 확인 · 흔적

**데모 테넌트 확인**(값은 출력하지 않고 같은지만 비교)
- `.env` 의 공개 키 = ax-clinic-project `KOS_API_tenent_dev` → **같다**, 운영 `KOS_API_tenent` → **다르다**
- `.env` 테넌트 id = 새 HAR 의 테넌트 id → **같다**
- 시스템 계정 sign-in 의 `tenantIds`(1개)에 그 테넌트가 있다

**호출**(2026-10-27, 데모 테넌트, 합계 72)
- 공개(데모 키): `exchange-token` 12(스크립트마다 새로 받음) · `getVisitor` 8(200 ×5 · 400 ×3 = 본문 키를 `visitorId` 로 잘못 보냄, 스펙은 `id`) · `getSchedulesByVisitor` 5 · `getScheduleDetail` 2 · `getVisitorQuestionnaire` 4 · `getQuestionnaireAgreements` 1 · `getQuestionnaireSubmit` 12(400 ×11 = 제출 전 「없음」 확인 · 200 ×1 = 제출 뒤) · **`submitVisitorQuestionnaire` 1(쓰기)**
- 내부(시스템 계정 Bearer): sign-in 9 · `get-visitors` 2 · v2 `get-visitor` 7 · v1 `get-visitor` 4 · `get-schedule-summaries` 2 · `get-reservation-groups` 1 · `get-schedules-for-reservation` 1 · **`update-visitor-personal-information` 1(쓰기)**
- **쓰기 2건**, 운영 키 0건. KOS 웹앱 JS 는 새로 받지 않았다(앞 판 사본)

**남긴 데모 흔적 — 되돌리지 않았다**(시험 고객 1명 · 브리프에 되돌리기 지시 없음)
1. 고객 개인 정보: 국적 `KR → CN` · 언어 `"" → zh-CN` · 여권번호 `"" → 시험 문자열` · 여권 성 · 이름 키가 `""` 로 생김
2. 문진 제출 1건(이 고객의 첫 제출 · `getQuestionnaireSubmit` 200)
3. 문진 제출이 바꾼 고객 정보: 성별 `GENDER_UNSPECIFIED → FEMALE` · 생년월일(시험 고객의 가상 날짜 → 다른 가상 날짜) · 휴대폰(시험 번호, 없던 칸) · 주소(`[ccc 시험]` 문구) · 한글 발음(시험 문구) · 개인정보 동의 `false → true`. 이름은 그대로
- 되돌리는 길: 1 · 3 의 개인 정보 칸은 같은 `update-visitor-personal-information` 으로(휴대폰을 빈 값으로 지울 수 있는지는 모름), 동의는 관리 정보 `update-visitor-management-information`, 문진 제출은 내부 `delete-questionnaire-submit`(JS 에만 있음 · 부르지 않음)
- HAR 쪽(사용자가 KOS 웹에서 한 것): 다른 시험 고객 1명의 국적 `KR → JP` · 언어 `"" → ko` · 여권번호 값 — 이번 조사가 만든 것이 아니다

**빠진 행**
- HAR: 22 = KOS API 9 + OPTIONS 2 … 인벤토리 §1 은 KOS 9 + OPTIONS 2 + 정적 9 + Datadog 4 를 모두 적었다
- 브리프 할 일 1(본문 · 언어 칸 · 여권 · 묶음 · 응답 · 세 조회 표면) → §2 · §3.1 / 2(값 목록 · 번역 꼴 대조) → §3.2 ~ §3.4 / 3(양식 언어 · 번역 필드) → §4 / 4ⓐ → §6 / 4ⓑ → §5 / 5 → §8

---

## 8. 정할 것 (결정하지 않음) — 9개

| # | 자리 | 왜 정해야 하나 | 앞 판 |
|---|---|---|---|
| Q-145 | 스캐너가 고객을 고칠 때 본문을 어떻게 만들지 | 「내부 `get-visitor` 로 읽고 → 13개 키 전부 + 바꿀 칸」은 안전함을 확인했다. 키를 빼고 보낼 때 지워지는지는 모른다(`snsInfo` 가 남은 것은 약한 근거). 휴대폰 · 이메일 · 만료일 · SNS 가 **있는** 고객이면 웹앱처럼 그 키도 함께 보낼지. 읽기와 쓰기 사이에 다른 사람이 고친 값은 덮인다 | V Q-39 · Q-40 |
| Q-146 | `_RESUME` 10-27 「KOS 고객 정보에 언어 칸 없음」 고치기와 문진 표시 언어의 원천 | KOS 고객 `language` 칸은 있다(직원이 KOS 웹에서 고침 · 새 고객 예약 때 `visitorLanguage`). 사용자 결정은 「국적」이다. ① 국적만 ② KOS 언어 칸 먼저, 없으면 국적(KOS 웹앱 `resolveDefault` 와 같은 순서) ③ 그 밖 — 사용자에게 다시 보일지. 언어 칸은 내부 `get-visitor` 에만 있어 고객마다 호출이 하나 더 든다 | `_RESUME` 10-27 |
| Q-147 | 양식 번역이 없는 언어 · 국적 | 양식은 6개 언어뿐이다. 국적 대응표(KOS 18개 나라)에서 태국 · 스페인 · 러시아 · 프랑스 · 독일 · 포르투갈 · 브라질은 양식 번역이 없다. 표에 없는 나라(베트남 등)도 있다. 그때 영어 · 한국어 중 무엇으로 보일지(KOS 웹앱 문서는 마지막에 `en`) | — |
| Q-148 | 국적 → 언어 대응표를 어디서 가져올지 | KOS 웹앱 JS 의 표(대만 · 홍콩 · 마카오 = 번체 등)를 그대로 옮길지, ccc 가 따로 정할지. JS 는 공식 계약이 아니고 버전마다 바뀔 수 있다. 동의 약관 번역은 `ja · en · zh` 로 키가 달라 같은 코드로 고를 수 없다 | `_RESUME` 10-27 |
| Q-149 | 고객이 본 언어를 남길지 | 제출 답의 `title` · `parentQuestionTitle` 은 원문(한국어)이고 KOS 는 표시 언어를 저장하지 않는다. 방문별 문진 이력(ccc)에 표시 언어를 함께 둘지 | Q-27 · Q-36 |
| Q-150 | 공개 문진 제출이 고객 정보를 바꾸는 것 | 생년월일 · 성별 · 휴대폰 · 주소 · 한글 발음 · 개인정보 동의가 **고객이 입력한 값으로 바뀐다.** 스캐너로 고친 생년월일을 고객이 문진에서 다르게 넣으면 덮인다. 문진 화면에서 이 칸을 고객에게 보일지 · 잠글지 · 미리 채울지(KOS 양식 응답에 미리 채운 값이 있다) | Q-30 |
| Q-151 | 스캐너 ↔ 문진 순서 | 둘 다 같은 고객 칸(생년월일 · 성별)을 쓴다. 나중에 한 쪽이 이긴다. 수정 시각은 문진 쪽에서 남지 않는다 | — |
| Q-152 | 주민번호를 공개 문진으로 넣을지 | 스펙은 `registrationNumber` 「고객 정보에도 반영」. 이번 시험에서 보내지 않았다(가짜 값 위험). 촬영 가이드 마스킹 결정(뒷자리 가림)과 이어진다 — 문진으로 받을지, 스캐너 내부 경로(`registrationNumber`)로 넣을지, 안 넣을지 | Q§M5 · `_RESUME` 10-27 |
| Q-153 | 데모 흔적 되돌리기 | 시험 고객 1명의 국적 · 언어 · 여권 · 성별 · 생년월일 · 휴대폰 · 주소 · 발음 · 동의 · 문진 1건이 남았다(§7). 그대로 둘지, 되돌릴지(문진 삭제는 내부 JS 경로뿐) | — |
