# 예약 상세 모달 · KOS 사전 설문(문진)으로 넣을 수 있는 정보

- 조사일: 2026-10-26 (KST) · 조사자: cc-prototype researcher (task_dacee03f38c8). 앞 판 `reservation-read-report.md`(아래 `R§`)에서 이어진다
- 원천
  - `reference/2026-10-23-cc-overall-board/har/설문전송.har` · `설문내용.har` (gitignore)
  - 고객용 설문 링크(코디 스크래치에 있다. 레포에 옮기지 않았다)
  - 공개 스펙 `https://developers.kos-solution.com/openapi.yaml` (2026-10-26 받음, 1.0.1, 작업 75개)
  - 시안 `design-analysis-report.md` §3.4(아래 `D§`)
- 표기
  - **확인**: 이번에 데모에서 조회해서 본 것, 또는 HAR 에 찍힌 것
  - **스펙**: openapi.yaml 에 적힌 것
  - **추정**: 해석
- **KOS 쓰기는 0건이다.** 링크 발급 · 설문 제출 · 고객 수정은 HAR 에 찍힌 것만 읽고 해석했다
- 리포트에는 테넌트 · 고객 · 일정 · 설문 id, 토큰, 링크, 이름 · 연락처 · 주소 · 주민번호 값을 적지 않았다. 토큰은 claim 의 **키 이름**만 적는다

---

## 0. 요약

- **두 HAR 의 파일 이름과 내용은 맞다.** 「설문전송」은 직원이 KOS 예약 화면에서 고객용 설문 **링크를 발급**한 기록이고, 「설문내용」은 고객이 그 링크로 설문을 **제출**한 기록이다. 다만 「전송」 파일에 실제로 메신저 · 문자로 보낸 요청은 없다. KOS 는 URL 을 돌려줄 뿐이다
- **제출 경로는 둘이다.**
  - ① 공개 API `submitVisitorQuestionnaire`(API 키 + `visitorId`)
  - ② 고객 페이지가 쓰는 내부 `submit-questionnaire/legacy`(링크 토큰을 본문에 담는다. Authorization 헤더 없음)
  - 답(`answers[]`) 항목의 키 7개는 둘이 **똑같다.** 다른 점: 공개는 `registrationNumber`(주민번호) · `phoneticName` 을 더 받고, 내부는 `visitorId` 대신 `token` 을 받는다
- **제출하면 KOS 의 두 곳에 남는다**(데모 조회로 확인)
  - ⓐ 설문 응답 자체. 공개 `getQuestionnaireSubmit` 으로 50개 답이 그대로 나온다. 자유 입력은 `memo` 에 들어간다
  - ⓑ **고객 정보 일부가 바뀐다.** 성별 · 휴대폰 · 주소가 제출 값으로 바뀌었다. 바뀐 값은 일정 응답의 `visitor` 에도 보인다. **이름은 바뀌지 않았다.** 이메일 · 메신저 · 사용 언어 답도 고객 정보에 들어가지 않는다(설문 답으로만 남는다)
- **스펙과 실제가 다른 곳이 두 군데 있다.** 둘 다 내부 legacy 경로로 제출한 결과다. 공개 경로도 그런지는 확인하지 못했다
  - 주소: 스펙은 「기존 주소가 있을 때만 고객 정보에 반영」이라고 한다. 실제로는 **비어 있던 주소에도 들어갔다**
  - 성별: 스펙은 고객 정보에 반영된다고 적지 않았다. 실제로는 **바뀌었다**
- **링크 유효 기간은 30일**(`exp − iat` = 2,592,000초)이다. 시안의 「10분 유효」는 고객 입력 QR 이 아니라 **신분증 스캔 QR** 문구다(D§3.4 스캔 2단계). 링크 발급은 **공개 API 짝이 없다**
- **모달 필드를 넣을 곳**(§5 표)
  - 문진 제출로 넣는 것: 건강 7항목 · 이메일 · 메신저(SNS) 종류와 아이디 · 사용 언어 · 통역 · 희망 시술 · 예산
  - 문진 제출 + 고객 정보 반영: 주소 · 휴대폰 · 성별 · 주민번호(공개 경로, 스펙)
  - KOS 에 넣을 곳이 없는 것: 신분 확인 **상태** · 「주의사항」(공개 쓰기 없음) · 여권번호/국적/이메일/SNS 의 고객 정보 반영(기존 고객 기준)
  - 신규 고객이면 예약 생성 `reserveV2` 의 `visitorPassportNumber` · `visitorNationality` · `visitorEmail` · `visitorSnsInfo` · `visitorLanguage` 로 고객이 만들어질 때 들어간다(스펙)
- 정할 것은 **14개**다(Q-25 ~ Q-38). 앞 판의 Q-6 · Q-10 · Q-11 · Q-12 · Q-13 · Q-19 와 이어지는 곳은 표시했다

---

## 1. HAR 인벤토리

### 1.1 `설문전송.har` — 항목 12개

KOS 8개(POST 7 · OPTIONS 1)와 Datadog RUM 4개(#0 · #2 · #4 · #11)다. KOS 요청은 모두 `origin: app.kos-solution.com` 에서 나갔다. `kos-client-uri` 는 `https://app.kos-solution.com/{tenantId}/reservation/schedule/?visitorId={visitorId}&scheduleId=…` 꼴이다. 즉 **KOS 웹 「예약」 화면에서 일정 하나를 열어 둔 상태**다(확인). `Authorization` 헤더는 HAR 에 없다. 내보낼 때 빠진 것으로 보인다(앞 판과 같다).

| # | 메서드 · 경로 (`api.kos-solution.com/tenants/{tenantId}` 뒤) | 종류 | 요청 본문 키 | 응답 모양 | 용도 |
|---|---|---|---|---|---|
| 1 | POST `/visitor/questionnaire/v1/commands/issue-questionnaire-link` | **내부 · 쓰기** | `visitorId` | `data{url}` (URL 436자) | 고객용 설문 링크 발급(§2) |
| 3 | OPTIONS 같은 경로 | CORS 사전 요청 | — | 본문 없음 | — |
| 5 | POST `/role/v2/queries/get-roles` | 내부 · 조회 | (본문 없음) | `data[{id, name, roleTags[int]}]` (15) | 역할 목록(앞 판 #0 과 같다) |
| 6 | POST `/schedule/v1/queries/get-schedule-summaries` | 내부 · 조회 | `visitorId · sort{by:"startDateTimeUtc", order:"DESC"}` | `data[{id, flowStep, reservation{startDateTimeUtc, endDateTimeUtc, reservationAssignee, reservationMemo, status, requestedProcedures}, consultation{}, tasks[{sequence, title, doctors, doctorMemo, assigneeMemo}], deleted, consultations[]}]` (4) | 고객의 일정 이력(최신순). 공개 짝 `getSchedulesByVisitor` |
| 7 | POST `/schedule/group/v1/queries/get-reservation-group` | 내부 · 조회 | `id` | `data{예약 그룹 1개}` — 앞 판 #9 의 한 행과 같은 모양 | 예약 그룹 1건. 공개 짝은 목록 `getReservationGroups` |
| 8 | POST `/procedure-menu/visitors/queries/get-visitors` | 내부 · 조회 | `sort{by:"order", order:"ASC"}` | `data[]` (0) | 이름만 보면 시술 메뉴 쪽 「고객 분류」 목록으로 보인다(추정). 비어 있었다 |
| 9 | POST `/v1/visitor/queries/get-visitor` | 내부 · 조회 | `id` | `data{…}` 키 39개 — §4.1 | **직원용 고객 상세.** 공개 `getVisitor`(키 7~9개)보다 훨씬 많다 |
| 10 | POST `/schedule/zone/room/v1/queries/get-rooms` | 내부 · 조회 | `zoneId` | `data[{id, zoneId, title, order}]` (28) | 방 목록(앞 판 #1 과 같다) |

시각으로 보면 #1 · #3 은 01:50:26 이고, #5~#10 은 01:51:52 에 한꺼번에 나갔다. #9 는 **제출(01:52:28) 전**의 고객 상세다. 이것을 제출 뒤 조회한 값과 비교했다(§4).

### 1.2 `설문내용.har` — 항목 2개

| # | 메서드 · 경로 | 종류 | 요청 본문 키 | 응답 | 용도 |
|---|---|---|---|---|---|
| 0 | POST `visitor-api.kos-solution.com/tenants/{tenantId}/visitor/questionnaire/visitor/v1/commands/submit-questionnaire/legacy` | **내부 · 쓰기** | `name · phoneNumber · phone{countryCode, phoneNumber} · address · addressDetail · dateOfBirth · gender · answers[50] · agreements[1] · token` | `{questionnaireId}` (`data` 로 감싸지 않음) | 고객 설문 제출(§3) |
| 1 | OPTIONS 같은 경로 | CORS 사전 요청 | — | — | — |

- `origin: service.kos-solution.com`(고객용 설문 페이지)이고, `Authorization` · 쿠키는 없다. 인증은 본문의 `token`(= 링크의 token, 같은 값임을 확인)이 한다
- 제출 시각은 01:52:28.629Z 다. KOS 의 설문 `createdDateTimeUtc` 는 01:52:28.796Z 다(확인)

**합계**: HAR 항목 14개 = KOS 10(쓰기 2 · 조회 6 · OPTIONS 2) + Datadog 4. 인벤토리 행은 §1.1 8행 + §1.2 2행 = 10행으로, KOS 요청 수와 같다.

### 1.3 고객 설문 페이지가 부르는 것 (링크를 GET 해서 JS 를 읽음)

링크 페이지는 Next.js 앱(`service.kos-solution.com/questionnaire/{tenantId}/first?token=…`)이다. JS 묶음 10개를 받아 경로 문자열을 찾았다. 요청 본문은 `{token}` 이고 Authorization 은 없다. 호스트는 `visitor-api.kos-solution.com/tenants/{tenantId}/…` 다. 같은 작업이 접두사 두 가지로 들어 있다: `visitor/questionnaire/visitor/v1/…`(HAR 제출이 쓴 쪽)과 `visitor/questionnaire/v1/…`.

| 작업 (JS 이름) | 경로 꼬리 | 종류 | 이번 조회 결과 (`…/visitor/v1` / `…/v1`) |
|---|---|---|---|
| `getIntroLegacy` | `/queries/get-intro/legacy` | 조회 | 200 / 200 — 안내 문구 `information · description` + 6개 언어 번역(`ko · ja · zh-Hans · zh-Hant · en · id`) |
| `getQuestionnaireLegacy` | `/queries/get-questionnaire/legacy` | 조회 | **200** / 400 `visitorId NotFound` — 아래 |
| `getQuestionnaireAgreements` | `/queries/get-questionnaire-agreements/legacy` | 조회 | 200 / 200 — 약관 1건(`PERSONAL_INFORMATION`, 필수) |
| `getQuestionnaireIsAlreadySubmitted` | `/queries/get-questionnaire-submit/legacy` | 조회 | **200** / 400 — 200 이면 제출한 적이 있다는 뜻이다. 응답은 공개 `getQuestionnaireSubmit` 과 같은 모양이다 |
| `submitQuestionnaireLegacy` | `/commands/submit-questionnaire/legacy` | 쓰기 | **부르지 않았다** |
| `getHospital` | `v1/hospital/queries/get-hospital` | 조회 | 부르지 않았다(병원 정보, 설문과 무관) |
| `getFeatureFlags` | `/common/feature-flags/v1/queries/get-feature-flags` | 조회 | 부르지 않았다 |

`get-questionnaire/legacy` 는 응답에 **고객의 현재 KOS 정보를 미리 채워서** 준다(`name · phoneNumber · phone · address · addressDetail · dateOfBirth · gender`). 그 뒤에 질문 `pages[4]` 가 온다. 질문과 선택지마다 `translsMap` 번역이 있다. 고객은 미리 채워진 값을 보고 고친 뒤 제출하는 것으로 보인다(추정). 토큰은 제출 뒤에도 조회에 쓸 수 있었다(확인). 다시 제출할 수 있는지는 쓰기라서 확인하지 않았다.

---

## 2. 설문 링크 발급 (`issue-questionnaire-link`)

| 항목 | 내용 |
|---|---|
| 요청 | 내부 · 쓰기 · `POST api.kos-solution.com/tenants/{tenantId}/visitor/questionnaire/v1/commands/issue-questionnaire-link` `{visitorId}`. 직원 세션(Bearer, 추정 — HAR 에는 헤더가 빠져 있다)으로 부른다. **일정 id 는 받지 않는다** → 설문은 고객 단위다 |
| 응답 | `{"data":{"url": "<436자>"}}` |
| 링크 모양 | `https://service.kos-solution.com/questionnaire/{tenantId}/first?token={JWT}`. 경로의 24자 id 는 토큰의 `tid` 와 같다(확인) |
| 토큰 | JWT · 헤더 `alg: HS256 · typ: JWT` · claim 키 **`sub · jti · iat · exp · tid · vid · scope`**. `sub` 와 `vid` 는 같은 값이다(확인) |
| 유효 기간 | `exp − iat` = **2,592,000초 = 30일**. 다른 유효 기간을 정하는 요청 필드는 없다(본문 키가 `visitorId` 하나뿐) |
| 제출 때 | 이 토큰을 그대로 제출 본문의 `token` 으로 보낸다(확인). 제출한 뒤에도 같은 토큰으로 조회가 200 이었다 |
| 공개 API 짝 | **없음.** 스펙 75개 중 설문 링크 · 토큰을 발급하는 작업은 없다. 공개 쪽에는 서버가 직접 제출하는 `submitVisitorQuestionnaire` 만 있다 |

시안(D§3.4)과 비교

| 시안 | KOS |
|---|---|
| [QR로 고객 입력 요청] · QR 상자 120 | KOS 는 URL 만 준다. QR 이미지는 화면이 그려야 한다 |
| [링크 복사] | 발급된 URL 을 복사하면 된다 |
| [메신저 전송] | 보내는 작업은 **KOS 에 없다**(HAR 에도 없다) |
| [태블릿에 띄우기] | KOS 에 없다. 같은 URL 을 태블릿에서 열면 된다(추정) |
| 「링크는 10분 동안만 유효합니다」 | 이 문구는 **신분증 스캔 QR**(스캔 2단계) 쪽에 있다. KOS 설문 링크는 30일이다 |
| 링크 주소 `https://ceramique.kr/survey/…` | KOS 링크는 `service.kos-solution.com` 이다. 사용자 구상(ccc 자체 질문지)이라면 ccc 주소가 된다 → Q-25 |

---

## 3. 제출 본문 해부

### 3.1 내부 legacy 제출 (HAR `설문내용` #0)

```text
{
  name, phoneNumber, phone{countryCode, phoneNumber},   ← 기본 정보(미리 채워진 값을 고객이 고침)
  address, addressDetail,                                ← 주소 한 칸 + 상세. 우편번호 · 나라 칸 없음
  dateOfBirth  ("yyyyMMdd" 8자리),  gender ("MALE"|"FEMALE"|…),
  answers[ {id, title, subText, inputText, parentQuestionId, parentQuestionTitle, inputType} ],  ← 고른 선택지 하나마다 한 줄
  agreements[ {id, title, link, required, translsMap, type, agreed} ],
  token                                                  ← 링크 JWT
}
```

- `answers[]` 한 줄 = **고른 선택지 하나**다. `id` = 선택지 id(`answerId`), `parentQuestionId` = 질문 id, `title` · `parentQuestionTitle` = 선택지 · 질문 글자다. 질문 · 선택지 id 는 데모 양식에서 1~2자리 숫자 문자열이었다(질문 6~20, 선택지 1~69). 제출한 id 50개는 모두 양식(`getVisitorQuestionnaire`)의 id 안에 있었다(확인)
- 자유 입력은 두 가지다
  - `INPUT_BOX`(이메일 질문 1개뿐) → `inputText`
  - 선택지에 `isSubText: true` 인 것(메신저 「라인 · 위챗」, 희망 시술 · 예산 · 과거 시술력 · 질환 · 약물 · 알레르기 · 언어의 「기타」 등 12개) → `subText`
- `inputType` 은 `CHECK_BOX` · `SELECT_BOX` · `INPUT_BOX` 가 쓰였다. 스펙에는 `DISCOUNT_SELECT_BOX` 도 있다
- 데모 제출 50줄에는 같은 질문 안에서 「없음」과 다른 선택지가 함께 들어 있었다(예: 복용 약물 「없음」 + 7개). KOS 가 이 조합을 거르지 않고 그대로 저장했다(확인). 막지 않는다는 뜻인지, 이번에만 통과한 것인지는 알 수 없다
- 양식은 4쪽 15질문이다. 연락 및 방문 정보(이메일 · 사용 중인 메신저 · 방문 유형) / 시술 정보(희망 시술 · 예산 · 과거 시술력) / 건강 정보(7개) / 추가 정보(사용 가능한 언어 · 통역 필요). **국적 · 여권 · 신분증 질문은 없다**

### 3.2 공개 `submitVisitorQuestionnaire` (스펙 `protos.open.SubmitVisitorQuestionnaireCommand`)

| 필드 | 필수 | 스펙 설명 (요약) | legacy 본문에 |
|---|---|---|---|
| `visitorId` | ✔ | 설문을 제출할 내원객 | 없음(토큰의 `vid` 가 대신한다) |
| `name` | ✔ | 「설문 응답에 저장할」 이름 | 있음 |
| `dateOfBirth` | ✔ | `yyyyMMdd` | 있음 |
| `gender` | ✔ | enum | 있음 |
| `phone{countryCode, phoneNumber}` | — | 설문에 저장하고 **고객 휴대폰도 갱신** | 있음(+ `phoneNumber` 문자열) |
| `address` · `addressDetail` | — | 설문에 저장. **기존 고객 주소가 있을 때만** 고객 정보에 반영 | 있음 |
| `phoneticName` | — | 설문에 저장하고 **고객 정보에도 반영** | **없음** |
| `registrationNumber` | — | 주민등록번호. 설문에 저장하고 **고객 정보에도 반영** | **없음** |
| `agreements[]` | — | `type` 이 있으면 그 유형의 고객 동의 정보에 반영 | 있음 |
| `answers[]` | — | 키 7개(`id · title · inputText · inputType · parentQuestionId · parentQuestionTitle · subText`, 모두 필수). `INPUT_BOX` 이면 `inputText` → memo, 아니면 `subText` → memo | **같은 키 7개** |
| 응답 | | `{questionnaireId}` | 같음 |
| 오류 | | 400 `SubmitVisitorQuestionnairePhoneNotAvailableError`(번호를 해석할 수 없음) + 공통 400 | — |

**ccc 가 제출할 수 있는 길**(둘 다 쓰기라서 부르지 않았다)
- ① **공개** `submitVisitorQuestionnaire`. 서버에 API 키가 있고 `visitorId` 만 알면 된다. 공식 계약이다. 주민번호 · 발음까지 넣을 수 있다
- ② **내부** `issue-questionnaire-link`(직원 Bearer) → 토큰 → `submit-questionnaire/legacy`. 고객 페이지가 쓰는 그대로이지만 공식 계약이 아니다. 주민번호 · 발음 칸이 없다
- 두 길 모두 **KOS 양식의 질문 · 선택지 id 로 답해야 하는 것으로 보인다**(스펙의 키가 `parentQuestionId` · `id` 다). 양식에 없는 질문 · id 를 보냈을 때 KOS 가 받는지는 스펙에 적혀 있지 않고, 확인할 수도 없었다(쓰기 금지) → Q-26

---

## 4. 제출 뒤 KOS 에 무엇이 남나 — 데모 조회

제출한 고객 1명(id 는 HAR #1 본문에서 얻었다)으로 아래를 조회했다. 모두 200 이다. 값끼리 같은지만 비교하고, 값은 적지 않는다.

### 4.1 설문 응답 자체 — 공개 `getQuestionnaireSubmit`

- **200**(앞 판에서는 데모 401회가 모두 400 이었다. 이번 제출이 데모의 첫 설문이다)
- 모양: `data{id, visitorId, visitorName, phoneNumber, phone{}, address, addressDetail, dateOfBirth(yyyyMMdd), gender, phoneticName, createdDateTimeUtc, agreements[{…, agreed}], answers[50]{seq, questionId, questionTitle, answerId, answerTitle, memo}}`
- 대응 관계(50줄 모두 확인)
  - `questionId` = 제출 `parentQuestionId`
  - `answerId` = 제출 `id`
  - `answerTitle` = 제출 `title`
  - `memo` = `INPUT_BOX` 면 `inputText`, 아니면 `subText` — 스펙 설명과 같다(4건으로 확인)
  - `seq` 는 50줄 모두 **빈 문자열**이었다. 스펙에는 「뷰 노출 순서」라고 되어 있다
- `visitorName` 은 **제출한 이름**이다. 고객 정보의 이름과 다르다(아래)
- **응답은 객체 하나**(`data{}`)이고 목록이 아니다. 일정 id 도 없다 → 설문은 고객마다 1건으로 보인다. 다시 제출하면 덮어쓰는지, 이력이 남는지는 미확인 → Q-27
- 고객 페이지 `get-questionnaire-submit/legacy` 도 같은 모양 · 같은 값이었다

### 4.2 고객 정보 — 제출 전(HAR #9, 내부) ↔ 제출 뒤(내부 `get-visitor` · 공개 `getVisitor`)

내부 `get-visitor` 응답 키 39개를 하나씩 비교했다. 바뀐 키는 **3개**다.

| 필드 | 제출 전 → 뒤 | 제출 값과 같은가 | 스펙 |
|---|---|---|---|
| `gender` | 바뀜 | 같다 | 스펙에는 고객 정보 반영 언급이 **없다** → 스펙과 다르다 |
| `phoneNumber{countryCode, phoneNumber}` | 키가 **없다가 생겼다** | 국가번호는 같다. 번호는 **맨 앞 0 이 빠진** 꼴로 저장됐다(제출 11자리 → 저장 10자리) | 「갱신됩니다」와 같다 |
| `address{address, detailedAddress, zipCode}` | 비어 있다가 채워짐 | `address` · `detailedAddress` 가 제출 값과 같다. `zipCode` 는 빈칸이다 | 「기존 주소가 있을 때만 반영」과 **다르다**(비어 있었는데 반영됐다) |
| `name` | 그대로 | **다르다**(제출 이름 ≠ 고객 이름) | 「설문 응답에 저장할 이름」 — 고객 정보는 안 바꾼다는 뜻으로 읽힌다 |
| `dateOfBirth` | 그대로 | 제출 전부터 같은 값이었다 → 반영 여부는 **판단할 수 없음** | 언급 없음 |
| `snsInfo` · `language` · `memo` · `passportNumber` · `registrationNumber` · `nationality` | 그대로 | 메신저 · 언어 답은 고객 정보에 들어가지 않았다. legacy 본문에는 주민번호 칸이 없다 | — |
| 동의 플래그(`aggrementPersonalInformation` 등) | 그대로 | 제출 전부터 개인정보 동의가 true 였다 → 판단할 수 없음 | 「반영」 |
| `updatedDateTimeUtc` · `lastVisitedDateTimeUtc` | **그대로** | 필드 3개가 바뀌었는데 수정 시각은 그대로다 | — |

공개 `getVisitor` 의 키는 `id · chartNumber · name · phoneNumber · dateOfBirth · gender · nationality · passportSurname · passportGivenNames` 9개다. 여기서도 휴대폰 · 성별이 새 값으로 보였다.

**내부 `get-visitor` 에만 있는 고객 필드**(제출과 상관없이 직원 화면이 갖는 것): `registrationNumber` · `foreignRegistrationNumber` · `passportNumber` · `passportSurname` · `passportGivenNames` · `passportExpiryDate` · `address{address, detailedAddress, zipCode}` · `language` · `snsInfo` · `funnel` · `visitorFunnel{funnelCategoryId, funnelId, funnelDetail}` · `detailedFunnel` · `recommenderName` · `doctor` · `counselor` · `memo` · `migratedMemo` · 동의 플래그 3개 · `customAttributes[]` · `lineInformation[]` · `unniInformation[]` 등. **고객 이메일 필드는 내부 응답에도 없다**(확인).

### 4.3 일정 — 공개 `getSchedulesByVisitor` · `getScheduleDetail`(4건) · 내부 `get-schedule-summaries`

- 일정 4건의 `visitor` 가 모두 **새 성별 · 새 휴대폰**으로 보였다(확인). 일정 응답의 `visitor` 는 고객 정보를 그때그때 읽어 오는 것으로 보인다(추정)
- 일정 응답에는 **설문을 가리키는 필드가 없다**(키 이름에 `questionnaire` 가 없음). 건강 답을 보려면 `getQuestionnaireSubmit(visitorId)` 를 따로 불러야 한다
- KOS 웹 화면의 어느 자리에 설문 답이 보이는지는 HAR 이 없어 **미확인**이다 → Q-28

---

## 5. 예약 상세 모달 필드 대조 (D§3.4)

넣는 길
- **문진**: 문진 제출로 넣는다(질문 · 답 형식). 설문 응답에만 남는다
- **문진→고객**: 문진 제출이 고객 정보까지 바꾼다
- **고객 API**: 고객 · 예약 쓰기 작업에 칸이 있다(이름만 적는다. 부르지 않았다)
- **없음**: KOS 에 넣을 곳 없음

읽는 곳은 앞 판 R§3.1 의 해당 행이다.

| # | 모달 필드 (D§3.4) | 넣는 길 | 질문 · 형식 / 작업 | 메모 · 앞 판 |
|---|---|---|---|---|
| M1 | 이름(외국인은 「이름 (여권 영문)」) | **문진**(설문에만) · 고객 API(신규만) | 제출 `name`(필수) — 고객 정보는 안 바뀐다(확인) / `reserveV2.visitorName` · `visitorPassportSurname · GivenNames`(새 고객이 생길 때) | 기존 고객의 이름 · 여권 이름을 바꾸는 공개 쓰기는 없다 · R Q-6 → Q-29 |
| M2 | 한글 발음 | **문진→고객**(공개만, 스펙) | 공개 제출 `phoneticName` — 「고객 정보에도 반영」. legacy 본문에는 칸이 없다 | 실제로 반영되는지는 미확인(쓰기 금지) |
| M3 | 성별 | **문진→고객** | 제출 `gender`(필수) · 고객 정보 반영 확인 | 스펙에 반영 언급이 없다 → Q-30 |
| M4 | 생년월일 | **문진**(+고객 반영 미확인) | 제출 `dateOfBirth` `yyyyMMdd`(필수) / `reserveV2.visitorBirthDayUtc`(신규) | 이번 데모에서는 값이 원래 같아서 판단할 수 없었다 |
| M5 | 주민등록번호 | **문진→고객**(공개만, 스펙) | 공개 제출 `registrationNumber` — 「고객 정보에도 반영」. 내부 고객 필드 `registrationNumber` 가 있다 | legacy 고객 페이지에는 칸이 없다 · R Q-19 |
| M6 | 여권번호 | **고객 API(신규만)** · 기존 고객: **없음** | `reserveV2.visitorPassportNumber`(「중복 검색과 새 내원객 생성에 사용」). 문진에는 칸 · 질문이 없다. 내부 고객 필드 `passportNumber` · `passportExpiryDate` 가 있다(쓰기는 HAR 에 없다) | R Q-19 → Q-29 |
| M7 | 국적 | **고객 API(신규만)** · 기존: **없음** | `reserveV2.visitorNationality`(「새 내원객 생성 때 저장」). 문진에 질문이 없다 | |
| M8 | 휴대폰 번호 | **문진→고객** | 제출 `phone{countryCode, phoneNumber}` · 반영 확인(맨 앞 0 이 빠져 저장됨) · 오류 `PhoneNotAvailable` | 화면에 보일 때의 형식 → Q-31 |
| M9 | 이메일 | **문진**(질문 「이메일」 `INPUT_BOX` → `memo`) · 고객 API(신규만 `reserveV2.visitorEmail`) | 고객 정보에는 이메일 필드가 없다(공개 · 내부 모두) | R Q-10 |
| M10 | SNS 종류 | **문진**(질문 「사용 중인 메신저」 `CHECK_BOX` 복수: 없음 · 카카오톡 · 라인 · 위챗 · 왓츠앱) · 고객 API(신규만 `reserveV2.visitorSnsInfo`) | 문진 답은 고객 `snsInfo` 로 가지 않았다(확인). KOS `snsType` enum 에는 `instagram · etc` 가 더 있다. 문진에서는 **복수 선택**, 고객 정보에는 **하나**다 | → Q-32 |
| M11 | SNS 아이디 | **문진**(라인 · 위챗 선택지의 `subText` → `memo`) | 카카오톡 · 왓츠앱 선택지에는 추가 입력이 없다(`isSubText: false`) | → Q-32 |
| M12 | 주소 / 주소 (자국) | **문진→고객** | 제출 `address · addressDetail` · 반영 확인(비어 있던 주소에도 들어감) | KOS 는 주소 한 칸 + 상세 + `zipCode` 다. 국내 · 자국 구분이 없다 · R Q-10 → Q-33 |
| M13 | 고객 기본 정보 채움 글자(「n / N 입력」 · 「모두 입력됨」) | 없음 | KOS 에 「입력 완료」 상태가 없다. 제출 여부는 `getQuestionnaireSubmit` 이 200 인지 400 인지로만 알 수 있다 | → Q-34 |
| M14 | [QR로 고객 입력 요청] · 링크 · 태블릿 · 복사 · 메신저 | 내부(링크 발급만) | §2. 공개 짝 없음 · 30일 · 보내기 기능 없음 | R Q-19 → Q-25 |
| M15 | 신분 확인 {여권/신분증} Badge(확인 완료/미확인) | **없음** | 확인 **상태**를 둘 필드가 KOS 에 없다 | R Q-19 |
| M16 | 신분증 스캔 이미지 · 수신 기기 · 시각 · 「자동 입력됨」 | **고객 API**(이미지만) | `generateUploadingImageUrl`(presigned URL, 5분) → PUT → `registerVisitorImages{visitorId, scheduleId?, fileName, source(HOSPITAL·VISITOR·AGREEMENT·PEN_CHART), category, equipment, shootingDateTimeUtc, memo(≤150자), path}` | 기기 · 「자동 입력」(OCR 로 칸을 채움)은 KOS 에 없다. 이미지를 조회하는 공개 작업도 없다 → Q-35 |
| M17 | 유입 채널 · 상세 | 고객 API | `reserveV2` · `reserveByVisitorIdV2` 의 `funnelDetail`(예약 만들 때). 문진에는 질문이 없다 | 고객 단위 유입(내부 `visitorFunnel`)과 예약 단위 유입이 따로 있다 · R Q-11 |
| M18 | 예약 메모 | 고객 API | `changeReservationMemo{scheduleId, memo}`(통째로 바꾼다, KDA§5) | 문진과 상관없다 |
| M19 | 건강 정보 7항목(질환 · 복용 약물 · 알레르기 · 임신/수유 · 켈로이드 · 신체 내 금속장치 · 지혈 장애) | **문진** | 질문 12~18. 질환 · 약물 · 알레르기 · 금속장치 = `CHECK_BOX` 복수(+「기타」 `subText`). 임신 · 켈로이드 · 지혈 = `SELECT_BOX` 예/아니오. 읽기: `getQuestionnaireSubmit.answers[]` | 「확인 필요 N」 · 빨강 기준은 KOS 에 없다. 설문이 고객 단위라서 **방문마다의 건강 상태는 따로 남지 않는다** · R Q-12 → Q-36 |
| M20 | 주의사항(고객 공통 메모) | **없음**(공개 쓰기) | 후보 필드 `visitor.memo`(R Q-13)를 쓰는 공개 작업이 없다. 내부 쓰기는 HAR 에 없다 | R Q-13 → Q-37 |
| M21 | (모달 밖) 희망 시술 · 예산 · 과거 시술력 · 방문 유형 · 사용 언어 · 통역 필요 | **문진** | 질문 8 · 9 · 10 · 11 · 19 · 20 | 시안은 이 값들을 「예약 등록 · 승인」 초안(희망 시술 / 예산 · 통역)과 여정 리포트 언어 자리에 쓴다. 언어 답은 고객 `language` 로 가지 않았다(확인) → Q-38 |
| M22 | (모달 밖) 동의 약관 | **문진→고객**(스펙) | 제출 `agreements[{type, agreed}]` · 목록은 `getQuestionnaireAgreements`(데모 1건: 개인정보 필수) | 이번 데모에서는 동의 값이 원래 true 라 반영 여부를 판단할 수 없었다 |

**모달 오른쪽 아래쪽**(이전 방문 · 내원 현황 · 정산 · 시술실 배정 · 접수)은 문진과 상관없다. 앞 판 R§3.1 20~28행에 있다.

---

## 6. 정할 것 (결정하지 않음) — 14개

| # | 자리 | 왜 정해야 하나 | 앞 판 |
|---|---|---|---|
| Q-25 | 고객 입력 링크를 KOS 링크(`service.kos-solution.com`, 30일)로 쓸지, ccc 자체 페이지로 할지 | 사용자 구상은 ccc 자체 질문지다. KOS 링크는 내부 발급 API 로만 만들 수 있다. 시안의 「10분」은 스캔 QR 문구라서, 고객 입력 링크의 유효 기간은 따로 정해야 한다 | R Q-19 |
| Q-26 | ccc 질문지 ↔ KOS 양식 id 대응 | 제출 답은 KOS 양식의 `parentQuestionId` · 선택지 `id` 로 보낸다. 양식은 지점이 정하고(데모 15질문 · 선택지 70개), 양식에 없는 질문을 KOS 가 받는지는 모른다. ccc 질문을 KOS 양식에 맞출지, KOS 양식을 ccc 에 맞게 고칠지(KOS 설정), 남는 질문을 ccc 에만 둘지 | — |
| Q-27 | 설문은 고객마다 1건인가 | 응답이 목록이 아닌 객체 하나이고 일정 id 도 없다. 다시 제출할 때 덮어쓰는지 이력이 남는지 모른다. 재방문 고객의 건강 정보를 어떻게 다룰지와 이어진다 | — |
| Q-28 | KOS 직원 화면에서 설문 답이 어디에 보이나 | API 로는 확인했다. KOS 웹 화면의 자리는 HAR 이 없어 보지 못했다. 필요하면 화면 HAR 을 한 번 더 뜬다 | — |
| Q-29 | 기존 고객의 이름(여권 영문) · 여권번호 · 국적을 KOS 에 넣는 길 | 공개 쓰기는 **새 고객을 만드는 예약 생성** 때만 받는다. 기존 고객을 고치는 공개 작업은 없다. 문진에도 칸이 없다. 내부 고객 수정 API 는 HAR 에 없다 | R Q-6 · Q-19 |
| Q-30 | 제출이 성별 · 주소를 덮어쓰는 것 | 실제로는 스펙 설명보다 많이 바뀌었다(성별 · 비어 있던 주소). 고객이 잘못 고르면 KOS 고객 정보가 바뀐다. 공개 경로도 그런지 데모에서 한 번 제출해 볼지(쓰기 허가가 필요하다) | — |
| Q-31 | 휴대폰 형식 | 제출은 11자리였고 KOS 는 맨 앞 0 을 뺀 10자리로 저장했다. 화면에 보일 형식(`+82 10 …` 등)을 정해야 한다 | — |
| Q-32 | SNS: 문진 「메신저」(복수 · 5개) ↔ 고객 `snsInfo`(하나 · enum 6개) | 문진 답은 고객 정보로 가지 않는다. 시안의 「SNS 종류 · 아이디」를 어느 쪽에서 읽을지. 카카오톡 · 왓츠앱은 아이디 칸이 없다 | — |
| Q-33 | 주소 (자국) | KOS 주소는 한 칸이고 국내 · 자국 구분이 없다. 외국인 자국 주소를 같은 칸에 둘지 | R Q-10 |
| Q-34 | 「n / N 입력」 · 「접수 완료」 판단 | KOS 에는 입력 완료 상태가 없다. 무엇을 「입력됨」으로 볼지(제출 여부 · 칸별 값) | — |
| Q-35 | 신분 확인 상태 · 스캔 이미지 | 상태는 KOS 에 넣을 곳이 없다. 이미지는 `registerVisitorImages` 로 넣을 수 있지만 조회하는 공개 작업이 없다. ccc 가 상태와 이미지를 가질지, 이미지만 KOS 에 둘지 | R Q-19 |
| Q-36 | 건강 「확인 필요」 기준 · 방문별 건강 상태 | 빨강 기준은 KOS 에 없다. 설문이 고객 단위라서 방문마다의 답이 따로 남지 않는다(Q-27 과 이어진다) | R Q-12 |
| Q-37 | 주의사항을 KOS 에 둘지 | `visitor.memo` 를 쓰는 공개 작업이 없다. ccc 에만 둘지, 내부 API 를 찾을지 | R Q-13 |
| Q-38 | 문진의 다른 답(희망 시술 · 예산 · 언어 · 통역 · 방문 유형)을 예약 초안 · 여정 리포트에 쓸지 | 값은 설문에만 있다. 고객 `language` 는 바뀌지 않는다. 시안 「방문 유형(초진/재진)」 답과 KOS `isNew` 가 다를 때 어떻게 할지 | — |

---

## 7. 호출 기록 · 빠진 행 점검

**호출**(2026-10-26, 데모 테넌트, 조회만)
- 공개(데모 키 `KOS_API_tenent_dev`): `exchange-token` 1 + 조회 9 — 모두 200
  - `getQuestionnaireSubmit` · `getVisitor` · `getVisitorQuestionnaire` · `getQuestionnaireAgreements` · `getSchedulesByVisitor` · `getScheduleDetail` ×4
- 내부(시스템 계정 Bearer): sign-in 1 + 조회 2 — 모두 200
  - `v1/visitor/queries/get-visitor` · `schedule/v1/queries/get-schedule-summaries`. HAR 본문 그대로 보냈다
- 고객 페이지(링크 토큰): HTML · JS GET 11회, `visitor-api` 조회 8회 — 200 ×6 · 400 ×2(`…/v1` 접두사의 `get-questionnaire` · `get-questionnaire-submit`, `visitorId NotFound`)
- **쓰기 0건.** 운영 키는 쓰지 않았다. 링크 발급 · 제출 · 고객 수정은 부르지 않았다

**빠진 행**
- HAR: 항목 14개 = KOS 10 + Datadog 4. 인벤토리 10행(§1.1 8행 + §1.2 2행) = KOS 요청 10건
- 모달 대조 22행(M1~M22)
  - D§3.4 왼쪽 칸 필드 11개: M1~M12 중 M9~M12 는 이메일 · SNS 두 칸 · 주소
  - 그 밖: 채움 글자 · QR · 신분 확인 2개 · 유입 · 예약 메모 · 건강 · 주의사항
  - 브리프가 짚은 여권번호/주민번호 · 신분 확인 · 이메일 · 주소(자국) · SNS · 건강 7항목 · 주의사항은 모두 행이 있다
  - 모달 안이지만 문진과 상관없는 것(이전 방문 · 내원 현황 · 정산 · 바닥 줄)은 R§3.1 로 넘겼다
- 정할 것 14개(Q-25 ~ Q-38)
