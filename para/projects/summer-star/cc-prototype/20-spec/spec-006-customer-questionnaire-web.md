---
type: spec
id: SPEC-006
title: "고객 문진 웹 — 고객 자기 폰 · 로그인 없는 토큰 링크 · KOS 문진 제출(지금) · ccc 저장(나중) · QR 은 데스크 웹 · 직원 앱이 보여 줌"
version: 0.1.0
status: draft
product: cc-prototype
feature: procedure
created_at: 2026-10-28
updated_at: 2026-10-28
tags:
  - product/cc-prototype
  - feature/procedure
  - doc/spec
  - status/draft
links:
  baselines:
    - "[[baseline-009-reservation-board|BASE-009]]"
  decisions:
    - "[[decision-008-customer-questionnaire-web|DEC-008]]"
    - "[[decision-007-app-v2|DEC-007]]"
    - "[[decision-006-reservation-board|DEC-006]]"
  specs:
    - "[[spec-004-procedure-app|SPEC-004]]"
    - "[[spec-005-reservation-board|SPEC-005]]"
  works:
    - "[[work-010-customer-questionnaire-web|WORK-010]]"
  releases: []
  related: []
sources:
  - "orchestration/work/overall-board/_RESUME.md §2 — 10-27 「문진 = 고객이 웹에서 한다」 · 10-28 「문진 다시 하기 착수」 · 10-27 「문진 언어 원천」 · 10-26 「문진 방문별 이력」 · §1 「문진 다시 하기」 · 「법적 검토(나중)」"
  - "para/projects/summer-star/cc-prototype/20-spec/spec-004-procedure-app.md 0.4.1 (§5-3 · §6.15 · §6.17 · §7.3 · §7.4 — 이 문서가 문진 몫을 가져온다)"
  - "para/projects/summer-star/cc-prototype/20-spec/spec-005-reservation-board.md 0.4.0 (§5.11 · §6.6 · §6.8 #10)"
  - "orchestration/work/overall-board/app-spec-followups.md (#1 · #2 · #5)"
  - "orchestration/work/overall-board/app-kos-report.md §3 · §4 · §5 (언어 · 양식 번역 6개 · 공개 제출)"
  - "orchestration/work/overall-board/reservation-questionnaire-report.md"
  - "cc-prototype procedure/ main affac41 (back service/questionnaire.py · api/questionnaire.py · service/display.py · domain/languages.py · app lib/screens/questionnaire_screen.dart · lib/l10n/questionnaire_text.dart · front components/reservations/Display.tsx — 읽기만)"
---

# 고객 문진 웹 계약

> 문진을 **고객이 자기 폰으로 ccc 고객용 웹 페이지에서** 한다(DEC-008). 직원 기기(데스크 웹 · 직원 앱)는 **QR 만 보여 준다**.
> 이 문서가 문진의 정본이다 — SPEC-004 §6.15(앱 문진 화면)는 이 문서로 옮겨지고 빠진다(SPEC-004 0.4.2). 띄우기 요청(SPEC-004 §5-3)은 그대로 쓰고, 문진 종류(`kind:"questionnaire"`)에서 달라지는 것만 여기 적는다.
>
> SSOT 순서(이기는 순): ① DEC-008 · `_RESUME` §2 문진 줄 ② 이 문서 ③ SPEC-004 0.4.2 §5-3 · SPEC-005 0.4.1 ④ 지금 구현(`affac41` — BE4 문진 서비스 · 언어 표). 화면 시안은 없다 → **DS 기본값**(medikit · 모바일 웹)으로 그리고 E2E 에서 고친다.
>
> 근거 표기: `D8-nn` = DEC-008 · `D7-nn` = DEC-007 · `S4§` = SPEC-004 0.4.1 절 · `S5§` = SPEC-005 0.4.0 절 · `AK§` = `app-kos-report.md` 절 · `F#n` = `app-spec-followups.md` 줄 · `코드` = `affac41` 구현 · **`기본값`** = 결정에 없어 이 문서가 고른 값(§12 OQ 에 같이 올림).
>
> **이 레포는 public** — 키 · 토큰 값 · 비밀번호 · 실명 · 연락처 · KOS id 값을 쓰지 않는다. env 는 이름만.

## 1. 범위

### 1.1 In

| 무엇 | 근거 |
|---|---|
| **고객 문진 웹 페이지** — front 의 로그인 없는 공개 페이지(§2) · 고객 자기 폰 브라우저 | D8-01 · D8-02 |
| **토큰 링크** — 띄우기 요청 1행 = 링크 1개 · 만들기 · 유효 시간 · 한 번 제출 · 다시 열기 · 만료 화면(§3) | D8-03 |
| 화면 — 언어 칩 · KOS 양식 그대로 · 미리 채움 · 동의 · 제출 · 끝 · 오류 화면(§4 · §5) | D8-06 · D7-14 ~ D7-16 · D7-46 |
| **공개 back API** 2개 — 로그인 대신 토큰 · BE4 문진 서비스 재사용(§6) | D8-04 |
| 보안 — 다른 고객 정보 0 · 속도 제한 · 로그 · 직원 세션 안 씀(§7) | D8-03 · 기본값 |
| **QR 이 뜨는 곳** — 데스크 웹 예약 상세 QR 상자 · 직원 앱(폰 · 태블릿)이 띄우기 요청을 받아 QR 화면(§8) | D8-03 |
| KOS 제출(지금) · ccc 방문별 이력(§6.3 · §6.4) | D8-04 · D7-14 · D7-47 |
| **나중에 KOS 없이** — 문항 · 답을 ccc 에 두도록 바꿀 자리(§9 — 이번 판은 자리만) | D8-04 |
| 법적 검토 주석 자리(§7.6) | D8-07 |
| E2E — 고객 폰 실물(§10) | D8-02 |

### 1.2 Out

| 무엇 | 근거 |
|---|---|
| 앱 문진 화면(APP5) · 문진 잠금 · `[직원]` 길게 누르기 · 잠금 해제 API | D8-05 · OQ-802 |
| 코디 폰 [QR 읽기]로 문진 열기 — 문진 QR 은 이제 브라우저 주소라 고객 폰 카메라로 연다. [QR 읽기]는 **스캔(`kind:"scan"`)만** | D8-03 |
| [링크 복사] · [메신저 전송] · 문자 · 카카오 발송 | D7-44 그대로 · OQ-808 |
| KOS 고객 설문 링크(30일) | D7-13 그대로 |
| 주민번호 칸 | D7-16(Q-152) |
| 문진 이력 화면 | D7-47 그대로 |
| ccc 자체 문항 · 답 저장으로 바꾸기(실제 구현) | D8-04 — 나중 |
| 고객 로그인 · 고객 계정 · 본인 인증 | 기본값(토큰만) |

## 2. 경로 · 페이지

| 항목 | 계약 |
|---|---|
| 주소 | **`{PROC_FRONT_ORIGIN}/q#<토큰>`** — 토큰은 **주소의 `#` 뒤(fragment)** 에 둔다. fragment 는 브라우저가 서버로 보내지 않으므로 front · ingress · back 접근 로그와 다른 사이트 `Referer` 에 토큰이 남지 않는다 — 기본값(OQ-801 · 브리프 예시 `/q/<토큰>` 의 대안) |
| 주소 바탕 | back env `PROC_FRONT_ORIGIN`(지금 CORS 에 쓰는 front 주소 · 운영 `https://ccc.medisolveai.xyz`)을 그대로 쓴다 — 새 env 없음 · 기본값(OQ-813) |
| front 페이지 | `procedure/front/app/q/page.tsx`(새) — **`(main)` 묶음 밖**(공통 헤더 · 로그인 확인 없음). 클라이언트 컴포넌트가 `location.hash` 에서 토큰을 읽는다. 루트 `app/page.tsx` 의 로그인 이동은 `/q` 에 닿지 않는다 |
| 직원 세션과 분리 | 이 페이지는 `lib/session.ts` 를 읽지 않고 `lib/api.ts` 를 쓰지 않는다 — **새 `lib/publicApi.ts`**(back 호출은 lib 에서만 · 규칙 그대로)가 `Authorization` 없이 토큰 헤더(§6.1)만 싣는다. 직원 폰에서 열려도 직원 토큰이 실리지 않는다 |
| 메타 | `<meta name="robots" content="noindex,nofollow">` · `<meta name="referrer" content="no-referrer">` · 제목 = 「Céramique」(고객 이름 없음) · `viewport` 모바일 · 외부 스크립트 · 분석 태그 0 |
| 토큰 꼴 | base64url 43자(§3.1). `#` 뒤가 비었거나 꼴이 틀리면 back 을 부르지 않고 「링크가 올바르지 않아요」 화면(§5) |

## 3. 토큰

### 3.1 만들기

| 항목 | 계약 |
|---|---|
| 1행 = 1링크 | 띄우기 요청 `POST /api/display-requests {reservationId, kind:"questionnaire", deviceId?}`(S4§5-3) 한 번이 링크 하나를 만든다. 문진 전용 표는 없다 |
| 값 | **`token = base64url(HMAC-SHA256(PROC_SESSION_SECRET, "q|{requestId}|{qr_nonce}"))`**(43자 · 256비트). `qr_nonce` = 무작위 16바이트(새 열 · §6.5) · DB 에는 `qr_nonce` 와 **`qr_token_hash = sha256(token)`** 만 둔다(토큰 원문 0). 같은 행에서 로그인한 직원 화면이 링크를 **다시 그릴 수 있게** 하려는 것(데스크 웹 새로고침 · 직원 앱이 나중에 받기 — §8) · 기본값(OQ-801) |
| 스캔 종류 | `kind:"scan"` 은 지금 그대로(무작위 32바이트 · 해시만 · `ccc://display?t=` · claim — S4§5-3) |
| 비밀 값 바뀜 | `PROC_SESSION_SECRET` 이 바뀌면 열려 있던 링크가 모두 「링크가 만료됐어요」가 된다(직원 로그인도 같이 끊긴다 — 지금 그대로) |

### 3.2 상태 · 유효 시간 (문진 종류만)

| 상태 | 뜻 | 바뀌는 때 |
|---|---|---|
| `pending` | QR 이 보이는 중 · 고객이 아직 안 엶 | 만들 때 |
| `opened` | **고객이 페이지를 처음 엶**(공개 `GET` 첫 200) · `opened_at` | 첫 `GET` |
| `done` | 제출 성공 | 공개 `POST` 성공 |
| `canceled` | 데스크 [닫기] · 같은 예약 새 요청 | 직원 |
| `expired` | 아래 시간 지남 | 읽을 때마다(`expire_displays`) |

- **여는 시한** = `expires_at` = 만들 때 + `PROC_DISPLAY_TTL_MIN`(10분 · D7-44 그대로). `pending` 인 채 지나면 `expired`
- **쓰는 시한** = `opened_at` + **`PROC_QWEB_FILL_MIN`(새 env · 기본 60분)**. `opened` 인 채 지나면 `expired` — 기본값(OQ-803). 지금 `expire_displays` 는 `opened` 를 건드리지 않는다(코드) → **문진 종류의 `opened` 만** 이 규칙을 더한다(스캔 종류는 그대로)
- 공개 응답 `fillUntil` = 쓰는 시한(첫 `GET` 뒤 값) — 화면에 남은 시간은 보이지 않는다(기본값). 시한이 지나 제출하면 410 → 만료 화면

### 3.3 한 번 제출 · 다시 열기 · 새 링크

| 경우 | 계약 |
|---|---|
| 새로고침 · 같은 링크 다시 열기 | `opened` 이고 쓰는 시한 안이면 **다시 연다**(같은 `GET` · `opened_at` 그대로). 쓰던 답은 남지 않는다(브라우저 저장 안 함 — 기본값 · OQ-806) |
| 제출 뒤 다시 열기 | 409 `q_submitted` → 「이미 제출했어요」 화면 |
| 한 번 제출 | 공개 `POST` 성공 = `done` · 그 링크로 두 번째 `POST` = 409 `q_submitted`. 같은 링크로 두 `POST` 가 겹치면 뒤엣것 = 409 `q_submitting`(요청 id 별 잠금 — back 메모리 · §6.2) |
| 다른 폰이 같은 링크 | 막지 않는다 — 먼저 제출한 쪽이 이기고 나머지는 「이미 제출했어요」 · 기본값(OQ-805) |
| 직원이 다시 띄움 | 같은 예약 · `questionnaire` 의 **`pending` · `opened` 를 `canceled` 로 닫고** 새로 만든다(지금 코드는 `pending` 만 닫음 → `opened` 도 닫게 바꿈). 옛 링크 = 410 `q_canceled` → 「새 QR 을 받아 주세요」 화면 |
| 오늘 이미 제출 | 그래도 새 링크를 만든다(D7-47 그대로). KOS 는 덮어쓰고 ccc 이력은 줄이 하나 더 생긴다. 직원 쪽 상자에 「오늘 이미 제출함 · HH:MM」 안내만(§8.1) |

## 4. 화면 (고객 폰 · 시안 없음 → DS 기본값)

모바일 세로 한 열 · 폭 100%(최대 560px 가운데) · 글자 16px 이상(iOS 확대 막기) · 단계마다 한 화면 · 위에 진행 막대(「n / N」). 화면 틀 글자(버튼 · 안내 · 오류)는 **6개 언어 고정 문구 한 파일**(`procedure/front/lib/q/text.ts` — 앱 `lib/l10n/questionnaire_text.dart` 에서 옮김 · 그 파일은 앱에서 지운다). KOS 양식 · 약관 글자는 응답의 번역을 쓴다.

| 단계 | 계약 |
|---|---|
| ① 불러오기 | 공개 `GET`(§6.1) · 도는 동안 빈 틀 + 스피너 |
| ② 첫 화면 | 위 **언어 칩 6개**(`ko · ja · zh-Hans · zh-Hant · en · id` · 이름은 자기 말 — 「한국어 · 日本語 · 简体中文 · 繁體中文 · English · Bahasa Indonesia」) — back 이 정한 언어가 고른 채(§4.1) · 고객이 바꿀 수 있음(받은 번역 안에서 바꾼다 · 다시 부르지 않음 · D7-46) · 「{고객 이름} 님」(언어별 꼴 — 앱 문구 그대로) · 안내 한 줄 · [시작] |
| ③ 기본 정보 | **미리 채움**(이름 · 생년월일 · 성별 · 휴대폰(국가 번호 + 번호) · 주소 · 상세 주소 — `prefill` · KOS 값 · 스캔이 먼저였으면 스캔으로 고친 값) · **고객이 고칠 수 있음**(D7-16 Q-150 · Q-151). 생년월일 = 날짜 입력(보낼 때 `yyyyMMdd` · F#2) · 휴대폰 = `{countryCode, phoneNumber}`(F#5). **주민번호 칸 없음 · 한글 발음 칸 없음**(D7-16 Q-152 · 발음은 보내면 400 — §6.2) |
| ④ 양식 | KOS 양식 `pages[]` 차례(데모 4쪽) · 쪽마다 한 화면 · [이전] · [다음]. 질문 · 답 글자 = `translsMap.title.translation[언어]`(없으면 원문) · `subText` 도 같은 규칙. `CHECK_BOX`(여러 개) · `SELECT_BOX`(하나) · `INPUT_BOX`(글자) **KOS 그대로** · 필수 표시는 KOS 값 · 필수를 안 채우면 [다음] 꺼짐 · `isSubText:true` 답을 고르면 그 아래 글자칸 |
| ⑤ 동의 | `agreements[]` — 약관 글자 = 번역 키 `ja · en · zh`(`zh-Hans` · `zh-Hant` 둘 다 `zh`) · 그 밖 원문(한국어) · 필수 동의 안 하면 [제출] 꺼짐(`languages.AGREEMENT_KEY` 와 같은 표를 front 한 곳에) |
| ⑥ 제출 | [제출] → 공개 `POST`(§6.2) · 도는 동안 버튼 꺼짐 · 실패 = 「제출하지 못했어요 · 직원에게 알려 주세요」 + [다시 제출](입력값 유지) |
| ⑦ 끝 | 「감사합니다 · 이 창을 닫으셔도 돼요」(그 언어) · 되돌아갈 버튼 없음 · 뒤로 가기로 돌아와도 다시 `GET` → 「이미 제출했어요」 |

- 답 `title` · `parentQuestionTitle` 은 **원문(한국어)** 으로 보낸다(KOS 와 같게 · AK§4) — 고객이 본 언어는 ccc 이력에만(§6.4)
- 자동 완성 끄기 없음(고객 폰 기본) · 붙여 넣기 막지 않음

### 4.1 언어 고르기

**back 이 정한다**(D7-15 · D8-06 · 지금 `domain/languages.py` 그대로): KOS 고객 `language`(내부 `get-visitor`) → normalize(`zh-CN → zh-Hans` · `zh-yue → zh-Hant` · 그 밖 그대로 · `etc` · 빈 값 = 없음) → 없으면 **국적 대응표**(KOS 웹앱 표 — 출처 `app-kos-report.md` §3.3 · 주석 그대로) → 없으면 `en` → 그 값이 양식 번역 6개에 없으면 `en`. 응답 `language = {code, source:"kos_language"|"nationality"|"default", options:[6]}`.

| 경우 | 화면 언어 |
|---|---|
| 정상 | `language.code` · 고객이 칩으로 바꾸면 그 값(제출 본문 `language` · ccc 이력에 남음 · KOS 고객 `language` 는 바꾸지 않음 — D7-46) |
| `?lang=` | 공개 `GET` 에 `lang`(6개 중 하나)을 주면 그 값이 먼저(지금 BE4 그대로 · 화면은 보통 안 씀) |
| 응답 전 오류 화면(토큰 꼴 틀림 · 404 · 410 · 409 · 429) | 고객 언어를 모르므로 **브라우저 언어**(`navigator.languages` 첫 매치: `ko*`→ko · `ja*`→ja · `zh-TW`·`zh-HK`·`zh-MO`·`zh-Hant*`→zh-Hant · 그 밖 `zh*`→zh-Hans · `id*`·`in*`→id · 나머지 en) — 이 경우만 · 기본값 |

## 5. 오류 · 끝 화면

| 받은 것 | 화면(6개 언어) | 버튼 |
|---|---|---|
| 토큰 꼴 틀림 · 404 `q_not_found` | 「링크가 올바르지 않아요 · 직원에게 새 QR 을 요청해 주세요」 | 없음 |
| 410 `q_expired` | 「QR 유효 시간이 지났어요 · 직원에게 새 QR 을 요청해 주세요」 | 없음 |
| 410 `q_canceled` | 「새 QR 이 만들어졌어요 · 직원에게 새 QR 을 받아 주세요」 | 없음 |
| 409 `q_submitted` | 「이미 제출했어요 · 감사합니다」 | 없음 |
| 409 `q_submitting` | 「제출 중이에요 · 잠시 뒤 다시 열어 주세요」 | [다시 열기] |
| 429 `too_many_requests` | 「잠시 뒤 다시 시도해 주세요」 | [다시 시도] |
| 400 `questionnaire_field` · 409 `questionnaire_rejected` · 502 `kos_unavailable` · 네트워크 | 「제출하지 못했어요 · 직원에게 알려 주세요」(제출 때) / 「불러오지 못했어요 · 직원에게 알려 주세요」(불러올 때) | [다시 제출] / [다시 시도] |
| 403 `fake_board` | 「지금은 제출할 수 없어요 · 직원에게 알려 주세요」 | 없음 |

- 오류 화면에 고객 이름 · 예약 정보 · 오류 코드 · 영어 원문 메시지를 보이지 않는다(코드는 `data-code` 속성으로만 — E2E 확인용)

## 6. back

### 6.1 공개 API — 로그인 대신 토큰

| 항목 | 계약 |
|---|---|
| 경로 | **`GET /api/public/questionnaire?lang=`** · **`POST /api/public/questionnaire`** — router `api/public_questionnaire.py`(새) · prefix `/api/public` |
| 토큰 | 헤더 **`X-Questionnaire-Token: <token>`** — 경로 · 쿼리에 싣지 않는다(접근 로그에 남지 않게 · §7.3). 없으면 400 `q_token_missing` |
| 인증 | `Authorization` 을 **보지 않는다**(있어도 무시 — 직원 권한으로 바뀌지 않음). `deps.Actor` 를 쓰지 않는다 |
| 찾기 | `sha256(token)` → `display_request.qr_token_hash` · `kind = "questionnaire"` 인 행만(스캔 행 · 없는 해시 = 404 `q_not_found`). 찾은 뒤 `hmac.compare_digest` 로 §3.1 식을 다시 계산해 맞는지 한 번 더 |
| 상태 판정 | `expire_displays`(§3.2) 먼저 커밋 → `expired` = 410 `q_expired` · `canceled` = 410 `q_canceled` · `done` = 409 `q_submitted` · `pending`/`opened` = 계속 |
| `GET` 응답 | `{customerName, language:{code, source, options}, form:{pages[]}, agreements[], prefill:{name, phone:{countryCode, phoneNumber}, address, addressDetail, dateOfBirth, gender}, fillUntil}` — **지금 BE4 `load()` 응답에서 `reservationId` · `todaySubmitted` 를 뺀 것 + `fillUntil`**. 첫 성공이면 `pending → opened`(`opened_at`) |
| `POST` 본문 | `{language, name, dateOfBirth:"yyyyMMdd", gender, phone:{countryCode, phoneNumber}, address, addressDetail, agreements[{…, agreed}], answers[{parentQuestionId, parentQuestionTitle, id, title, inputText?, subText?}]}` — 지금 BE4 `QuestionnaireSubmit` 에서 **`deviceId` · `displayRequestId` 를 뺀 것**(요청 행은 토큰이 정한다 · 보내면 400 `invalid_request`) |
| `POST` 응답 | `{ok:true}` |
| 가짜 판 | `PROC_FAKE_BOARD` 켜짐 = `POST` 403 `fake_board`(지금 `require_real_board` 와 같은 뜻 · 로그인 없이 검사) |
| 캐시 | 두 응답 모두 `Cache-Control: no-store` |
| CORS | 운영은 front · back 이 같은 주소(`/api`)라 상관없다. 로컬(3700 ↔ 8700)은 CORS `allow_headers` 에 `X-Questionnaire-Token` 을 더한다 |

### 6.2 BE4 재사용 — 바뀌는 곳

지금 `service/questionnaire.py` `QuestionnaireService` 를 그대로 쓰고 **「누가」만 바꾼다**.

| 지금(`affac41`) | 바뀜 |
|---|---|
| `load(actor, reservation_id, lang, device_id)` · `submit(actor, reservation_id, body, sent)` | 앞 단계 = **`public_target(token)`**(§6.1 찾기 · 상태 판정 → `DisplayRequest`) → `load_for(request, lang)` · `submit_for(request, body, sent)`. 예약 · 고객은 요청 행의 `reservation_id` · `customer_id` 로만 찾는다(본문 · 쿼리의 id 를 받지 않는다) |
| `self.devices.check(actor, device_id)` | 없앰(고객 폰은 기기 행이 없다) |
| 제출 금지 칸 `registrationNumber` · `phoneticName` → 400 `questionnaire_field` | **그대로** |
| KOS 공개 `submitVisitorQuestionnaire` + `visitorId` · 실패 400 → 409 `questionnaire_rejected` · 그 밖 502 · `event_log(kos_rejected)` | **그대로**(actor = `customer` — §7.4) |
| 제출 뒤 `getQuestionnaireSubmit` 다시 읽어 `put_app_questionnaire` | 이름 · 값만 바꿈 — `source = "web_submit"`(§6.4) |
| `self.display.finish(tx, actor, displayRequestId)` | 토큰의 요청 행을 `done`(같은 트랜잭션) |
| 겹친 제출 | 요청 id 별 `asyncio.Lock`(back 메모리 · 한 파드) — 잠겨 있으면 409 `q_submitting` · 기본값(OQ-804) |
| 직원 경로 `GET` · `POST /api/questionnaires/{reservationId}` | **없앰**(앱 문진 화면이 빠져 부르는 곳이 없다 · D8-05) — 서비스 몸통은 위처럼 재사용 |
| `POST /api/auth/unlock`(문진 잠금 해제 · D7-71) | **없앰**(잠금이 없어짐) — 기본값(OQ-802) |

### 6.3 KOS 제출 (지금)

- 원천 = SPEC-004 §8.0 #16 ~ #20(내부 `get-visitor` 언어 · 공개 `getVisitorQuestionnaire` · `getQuestionnaireAgreements` · `submitVisitorQuestionnaire` · `getQuestionnaireSubmit`) — **그대로**
- **KOS 고객 값이 바뀐다**: 제출이 KOS 고객의 성별 · 생년월일 · 주소 · 휴대폰 · 개인정보 동의를 바꾼다(AK§5.3). 고객이 미리 채운 값을 고치면 KOS 고객 값도 그 값이 된다. 이름 · 언어 · 국적 · 여권은 바뀌지 않는다
- **휴대폰은 KOS 가 맨 앞 0 을 뺀다**(11자리 → 10자리) — ccc 는 고치지 않고 다음 미리 채움도 KOS 값 그대로(S4§6.15 ⑥ 그대로 · 시험은 앞 0 빠진 값을 맞는 값으로)
- 데스크 웹 상세 「건강 정보」는 지금처럼 KOS 최신 제출본을 읽는다(S5§5.11 — 바뀌지 않음) · 다음 5초 폴링에 채워진다
- 데모 지점에만 쓴다(D7-12)

### 6.4 ccc 방문별 이력

- `questionnaire_history` 에 `source` 값 **`web_submit`** 을 더한다(있던 `read` · `app_submit` 은 그대로 둠). 열: `language`(고객이 본 언어) · `device_id = null` · `display_request_id`(토큰의 요청) · `reservation_id` · `answers`(KOS 제출본 `answers[]` 그대로) — D7-14 · D7-47 · D8-06
- **같은 제출본 `read` 행이 먼저 있으면 그 행을 고친다**(웹 상세 5초 폴링이 먼저 읽은 경우 · `UNIQUE(customer_id, kos_submitted_at)` · 지금 `put_app_questionnaire` 규칙 그대로) — 새 행 · 버림 없음. 읽기 쪽은 `INSERT OR IGNORE` 그대로라 `web_submit` 행을 덮지 않는다
- 제출 확인(`getQuestionnaireSubmit`)이 실패하면 이력만 못 쓴다(제출은 됐다 · 지금 그대로)

### 6.5 표 · 열

| 표 · 열 | 바뀜 | 근거 |
|---|---|---|
| `display_request.qr_nonce` | 새 열(TEXT · null 가능 — 스캔 행 · 옛 행 null) | §3.1 |
| `display_request` 상태 규칙 | 문진 종류 `opened` 도 쓰는 시한으로 `expired`(§3.2) · 새 요청이 `opened` 도 `canceled` 로(§3.3) | §3 |
| `questionnaire_history.source` | 값 더함 `web_submit` | §6.4 |
| `event_log.type` | 더함 `qweb_open` · `qweb_denied` — §7.4 | §7.4 |
| 마이그레이션 | `MIGRATIONS` 에 `ADD COLUMN qr_nonce` 한 줄 · 멱등(S5§3.2 방식) | — |

### 6.6 띄우기 요청 응답에 링크 (직원 쪽 · 로그인 필요)

토큰을 다시 계산할 수 있으므로(§3.1) **로그인한 직원 응답에만** 링크를 싣는다.

| 자리 | 더하는 것 |
|---|---|
| `POST /api/display-requests` 응답 | `qrUrl`(문진 종류만 · `{PROC_FRONT_ORIGIN}/q#<token>`) — `qrToken` 은 스캔 종류만 채우고 문진 종류는 `null`(웹 · 앱이 `ccc://` 를 그리지 않게) |
| SSE `event: display` | `qrUrl`(문진 종류 · 그 기기 스트림에만 — S4§5-3 그대로) |
| `GET /api/display-requests/pending` 항목(F#1) | `qrUrl`(문진 종류 · `status = pending` 일 때만 · 그 밖 null). **문진 종류는 돌려줄 때 `opened` 로 바꾸지 않는다**(`opened` = 고객이 엶 — §3.2) · 스캔 종류는 지금 그대로 |
| 상세 `displays[]`(S4§5-3 「닫기」 · S5§7.3) | `qrUrl`(문진 종류 · `pending` 일 때만) · `openedAt` 더함 — 데스크 웹이 새로고침해도 QR 을 다시 그리고 「입력 중 · HH:MM」을 쓴다 |
| `POST /api/display-requests/claim` | 문진 종류 해시 = 404 `display_not_found`(문진 QR 은 claim 길이 아니다) |
| 띄우기 푸시 payload | **바꾸지 않음**(`{kind:"display", requestId}` — 링크 · 토큰을 Apple 쪽으로 보내지 않는다). 앱은 누르면 `pending` 을 읽어 `qrUrl` 을 받는다 |

### 6.7 경로 수

지금 코드 `test_route_count_50`(HTTP 49 + WS 1) → **− 3**(`GET` · `POST /api/questionnaires/{reservationId}` · `POST /api/auth/unlock`) **+ 2**(`GET` · `POST /api/public/questionnaire`) = **49 = HTTP 48 + WS 1** · 시험 **`test_route_count_49`**. OQ-802 가 unlock 을 남기면 50. 이 판 사이 다른 판이 경로를 더하면 그 수 위에서 −3 +2 로 다시 센다.

## 7. 보안

### 7.1 다른 고객 정보 0

- 공개 `GET` 은 **토큰의 요청 행 한 고객**의 이름 · 미리 채움 · 그 고객 양식만 돌려준다. `reservationId` · `customerId` · KOS id · 차트 번호 · 예약 시각 · 지점 · 직원 이름 · 다른 예약을 싣지 않는다
- 공개 경로는 예약 · 고객 id 를 입력으로 받지 않는다(§6.2) — id 를 바꿔 넣어 남의 것을 여는 길이 없다
- 공개 응답 스키마는 **허용 키 목록**(pydantic 모델 · `extra` 금지)으로 내보낸다 — KOS 응답을 통째로 흘리지 않는다(양식 `pages[]` · 약관 `agreements[]` 는 KOS 그대로 · 고객 값 칸 없음)

### 7.2 토큰

256비트 · DB 엔 해시 · 여는 시한 10분 · 쓰는 시한 60분 · 한 번 제출 · 새 요청이 옛것을 닫음(§3). **링크를 가진 사람은 그 고객의 미리 채운 값(이름 · 생년월일 · 성별 · 휴대폰 · 주소)을 볼 수 있다** — QR 을 남이 찍는 위험은 짧은 시한 · 한 번 제출로만 줄인다(PoC · OQ-807 · 법적 검토 §7.6).

### 7.3 속도 제한 (back 메모리 · 한 파드 — 기본값 OQ-804)

| 대상 | 한도 | 넘으면 |
|---|---|---|
| 같은 클라이언트 IP — 공개 `GET` | 1분 30회 | 429 `too_many_requests` · 1분 |
| 같은 IP — 공개 `POST` | 1분 5회 | 같음 |
| 같은 IP — 404 · 410 응답(틀린 · 지난 토큰) | 1분 10회 | 같음(토큰 맞히기 막기) |
| 같은 토큰 — `POST` | 1분 3회 | 같음 |

- IP = ingress 가 넘긴 클라이언트 주소(cloudflared · nginx 헤더 — 어느 헤더를 믿을지 WP-BE 가 운영 ingress 에서 확인해 한 곳에 적는다 · 없으면 소켓 주소). IP 는 메모리 카운터에만 · DB · 로그에 남기지 않는다
- 직원 API 에는 걸지 않는다

### 7.4 로그

| 무엇 | 남김 | 남기지 않음 |
|---|---|---|
| `event_log` `qweb_open` | `{requestId, reservationId, language, first}`(첫 열기 · 다시 열기) · actor = `customer` | 토큰 · IP · 고객 값 |
| `event_log` `qweb_denied` | `{requestId?, reason}`(`not_found` · `expired` · `canceled` · `submitted` · `submitting` · `rate`) — `not_found` 는 `requestId` 없음 · 같은 IP 같은 이유는 1분에 1행만 | 토큰 · IP |
| `event_log` `questionnaire_submit` | `{reservationId, customerId, language, historyId, displayRequestId, channel:"web"}` · actor = `customer` | 답 · 고객 값 |
| `event_log` `kos_rejected` | 지금 그대로(`op` · `httpStatus` · `kosError`) · actor = `customer` | — |
| 앱 로그(파이썬 `logging`) | 상태 코드 · 요청 id | 토큰 · `qrUrl` · 헤더 값 · 본문 |
| 접근 로그 | 경로 `/api/public/questionnaire`(토큰은 헤더 · fragment 라 안 남음) | — |

### 7.5 그 밖

- 공개 응답 · 페이지에 직원 세션 쿠키 · 토큰을 쓰지 않는다(§2) · `Referrer-Policy: no-referrer`
- 직원 화면 응답의 `qrUrl` 은 로그인 응답에만(§6.6) · 푸시 · 이벤트 로그 · 리포트 · 스크린샷 파일 이름에 토큰을 쓰지 않는다
- E2E 스크린샷에 QR · 주소창이 찍히면 토큰이 보인다 — 레포 · 리포트에 올리기 전에 가리거나, 이미 닫힌 요청의 것만 올린다

### 7.6 법적 검토 주석 (D8-07 — PoC 동안 SPEC · 코드 주석으로만)

주석 문구: **「법적 검토 필요: 고객 공개 웹 문진 — 개인정보(이름 · 생년월일 · 성별 · 휴대폰 · 주소 · 건강 답) 수집 · 동의 · 보관 · 링크 노출」**. 자리 3곳:

1. back `api/public_questionnaire.py` 머리
2. front `app/q/page.tsx` 머리
3. back `questionnaire_history` 정의(`repository/db.py`) — `web_submit` 줄 옆(보관 기간 미정)

## 8. QR 이 뜨는 곳

### 8.1 데스크 웹 — 예약 상세 「고객 기본 정보」 머리 (S4§6.17 자리를 바꿈)

| 항목 | 계약 |
|---|---|
| 버튼 | **[QR로 고객 입력 요청]** 그대로 → `POST /api/display-requests {kind:"questionnaire"}` → QR 상자 |
| QR 내용 | **`qrUrl`**(§6.6 — `https://…/q#<token>`) · 지금 `ccc://display?t=` 대신. QR 아래 「고객 휴대폰 카메라로 찍어 주세요」 · 남은 시간 mm:ss(여는 시한 · `pending` 동안) |
| [태블릿에 띄우기] | 그대로 — 기기 목록(`targets`) → 고르면 그 기기가 **같은 QR** 을 보여 준다(§8.2) · 「{기기}에 표시 중」 |
| 단계(5초 폴링 `displays[]`) | `pending` = QR · 남은 시간 → `opened` = 「고객이 입력 중 · HH:MM」(QR 숨김) → `done` = 「제출됨 · HH:MM」 → `expired` = 「시간이 지났어요」 + [다시 만들기] · `canceled` = 상자 닫힘 |
| 새로고침 | 상세 `displays[]` 의 `qrUrl` 로 다시 그린다(§6.6) |
| [닫기] | 요청 `canceled`(지금 그대로) → 고객 폰 링크 = 「새 QR …」 화면 |
| 오늘 이미 제출 | 상자 위 「오늘 이미 제출함 · HH:MM」(상세 `displays[]` 중 오늘 `done` · 지금 앱 시트의 안내를 웹에도) |
| 없음 | [링크 복사] · [메신저 전송](D7-44 · OQ-808) |

### 8.2 직원 앱 — 띄우기 요청 `kind:"questionnaire"` = QR 보여 주기 (S4§5-3 「열기」 · §6.11 을 바꿈)

| 항목 | 계약 |
|---|---|
| 받기 | 지금 길 그대로(SSE `display` · 띄우기 푸시 → `pending` · 앱이 앞으로 올 때 `pending`) — 문진 종류는 **`qrUrl` 을 받아 QR 화면**을 연다(문진 화면 · 잠금 없음) |
| QR 화면(새 · DS 기본값) | 흰 바탕 전체 화면 · 가운데 큰 QR(짧은 변의 60%) · 「휴대폰 카메라로 QR 을 찍어 주세요」 + 영어 한 줄 「Scan with your phone camera」 — 기본값(OQ-809) · 남은 시간 mm:ss · 오른쪽 위 [닫기]. 고객 이름 · 예약 정보 없음. 화면이 켜진 동안 꺼짐 막기(`wakelock`) |
| 닫힘 | 5초마다 `GET /api/reservations/{id}` 의 `displays[]` 에서 그 요청 상태를 본다 — `pending` 이 아니면(`opened` · `done` · `canceled` · `expired`) 「고객 폰에서 열렸어요」 등 한 줄 1.5초 뒤 저절로 닫힘. [닫기]는 **화면만** 닫는다(요청은 그대로 · 데스크 웹 QR 은 계속 됨) — 기본값 |
| 문진 종류 `pending` 항목 | `status = pending` 인 것만 QR 화면을 연다(`opened` 는 열지 않음) · 같은 `requestId` 는 한 번만(지금 규칙) · 다른 QR · 스캔 화면이 떠 있으면 끝날 때까지 기다림(OQ-621 그대로) |
| 앱 예약 상세 | **[태블릿에 띄우기](문진)** 그대로(다른 기기로) · **[이 기기에서 열기] → [이 기기에 QR 보이기]** = `POST /api/display-requests {kind:"questionnaire"}`(`deviceId` 없이) → 응답 `qrUrl` 로 같은 QR 화면 |
| [QR 읽기](예약 현황 머리) | **스캔 종류만**(`ccc://display?t=`) — 문진 QR(https)을 찍으면 「고객 폰으로 찍는 QR 이에요」 토스트 |
| 지움 | `screens/questionnaire_screen.dart` · `lib/l10n/questionnaire_text.dart`(→ front 로 옮김) · `model/questionnaire.dart` · 잠금 · `[직원]` · unlock 호출 · 문진 API 호출 · 그 시험 — 기본값(OQ-802 · OQ-812) |

## 9. 나중에 KOS 없이 — 바꿀 자리 (이번 판은 자리만 · 구현 없음)

D8-04 「나중에 KOS 안 쓰는 상황 고려 — 답 원천은 지금 KOS 제출 · 나중에 ccc 가 SoT 로 바꿀 수 있게」.

| 층 | 지금(KOS) | 나중(ccc) | 바뀌지 않는 것 |
|---|---|---|---|
| 문항 원천 | `QuestionnaireService` 가 KOS 공개 양식 · 약관을 읽음 | ccc 표 `questionnaire_form`(판 번호 · `pages` json · `agreements` json · 켜짐) — **KOS 양식 모양 그대로**(`translsMap` 6언어 · `CHECK_BOX` 등) | front 페이지 · 공개 API 응답 모양 |
| 미리 채움 | 내부 `get-visitor` | ccc 고객 사본 + 스캔 값 | `prefill` 모양 |
| 답 저장 | KOS `submitVisitorQuestionnaire` + ccc 이력 사본 | **ccc `questionnaire_history` 가 SoT**(지금 `answers` 는 KOS 제출본 모양 — 그대로 씀) + 동의 · 기본 정보 열 더함 · KOS 제출은 켜고 끌 수 있게 | 공개 `POST` 본문 |
| 읽는 곳 | 데스크 상세 「건강 정보」 = KOS 최신 제출본(S5§5.11) | ccc 최신 `web_submit` 행 | 화면 |
| 고객 값 바뀜 | KOS 제출이 KOS 고객의 성별 · 생년월일 · 휴대폰 · 주소 · 동의를 바꿈 | 어디에 둘지 미정(OQ-811) | — |

- 코드 자리: `QuestionnaireService` 안에서 **양식 읽기 · 미리 채움 · 제출을 세 함수로 나눠 둔다**(이번 판 WP-BE — 이름만 · 갈래 없음). 원천을 고르는 env · 표는 바꿀 때 만든다(지금 만들지 않는다)
- 지금 판이 지킬 것: ① 공개 API · front 는 KOS 이름(`visitorId` · `translsMap` 밖 KOS 전용 키)을 모른다 — 응답은 §6.1 모양만 ② 이력 `answers` 는 KOS 제출본 그대로 넣어 두어 나중에 원천이 될 수 있게

## 10. 검증

### 10.1 back 단위 시험 (pytest · KOS 가짜)

| 묶음 | 확인 |
|---|---|
| 토큰 | 문진 요청 만들기 → `qrUrl` 꼴 · `qrToken = null` · DB 에 원문 0(`qr_nonce` · 해시만) · 같은 행 다시 계산 = 같은 토큰 · 스캔 요청은 지금 그대로 |
| 공개 `GET` | 헤더 없음 400 · 틀린 토큰 404 · 스캔 토큰 404 · 첫 `GET` → `opened` · 두 번째 `GET` 200(`opened_at` 그대로) · 10분 지난 `pending` 410 `q_expired` · 60분 지난 `opened` 410 · `canceled` 410 `q_canceled` · `done` 409 · 응답 키 = 허용 목록뿐(`reservationId` · `customerId` · KOS id 없음) · `Authorization` 을 넣어도 결과 같음 · 언어 표(지금 `languages` 시험 그대로) |
| 공개 `POST` | 성공 → KOS 본문 = 받은 값 + `visitorId`(`deviceId` · `displayRequestId` 없음) · 요청 `done` · 이력 `web_submit` 1행(`language` · `display_request_id` · `device_id` null) · 같은 제출본 `read` 행 고침 · 두 번째 409 · 겹친 두 `POST` = 하나 409 `q_submitting` · 주민번호 · 발음 400 · `deviceId` 보냄 400 · KOS 400 → 409 + `kos_rejected` · 가짜 판 403 |
| 다시 띄우기 | 같은 예약 새 요청 → 옛 `pending` · `opened` 둘 다 `canceled` |
| pending · 상세 | 문진 `pending` 항목 = `qrUrl` 있음 · 돌려줘도 `pending` 그대로 · 상세 `displays[]` `qrUrl` · `openedAt` · claim 에 문진 토큰 404 |
| 속도 제한 | 각 한도 +1 = 429 · 1분 뒤 풀림(가짜 시계) · 직원 API 는 안 걸림 |
| 로그 | `event_log` · 앱 로그 캡처에 토큰 문자열 0 |
| 경로 | `test_route_count_49`(§6.7) · 없앤 3개 404 |

### 10.2 front · 앱 시험

- front: `npx tsc --noEmit` · `npm run lint` · `npm run build` · 로컬 브라우저(모바일 폭)에서 단계 ①~⑦ · 오류 화면 7가지 · 언어 칩 6 · 브라우저 언어 오류 화면 스크린샷(토큰 · QR 가림)
- 앱: `flutter analyze` 0 · `flutter test`(문진 화면 시험 지움 · QR 화면 — `qrUrl` 로 그림 · `pending` 아닐 때 닫힘 · [QR 읽기] 가 https 를 거절) · 시뮬레이터 스크린샷(폰 · 패드 QR 화면)

### 10.3 E2E — 고객 폰 실물 (완료 조건 · 배포 주소)

고객 폰이 front 에 닿아야 하므로 **배포(`https://ccc.medisolveai.xyz`) 뒤** 한다. 데모 지점 · `[ccc 시험]` 시험 고객만 · 직원 본인 폰을 「고객 폰」으로 쓴다(로그인 안 한 브라우저).

| # | 무엇 | 기대 |
|---|---|---|
| Q1 | 데스크 웹 [QR로 고객 입력 요청] → 아이폰 기본 카메라로 찍기 → Safari | 문진 첫 화면 · KOS `language` 가 있는 시험 고객 = 그 언어 · 칩으로 바꾸기 · 기본 정보 미리 채움 · 4쪽 · 동의 · 제출 · 「감사합니다」 → 웹 상자 「고객이 입력 중」 → 「제출됨」 · 「건강 정보」 채워짐(5초 안) · ccc 이력 `web_submit` 1행 |
| Q2 | 같은 링크 다시 열기 · 뒤로 가기 | 「이미 제출했어요」 |
| Q3 | 언어 원천 셋 — `language` 없음 + 국적 표에 있음 / 둘 다 없음 | 국적 언어 / English |
| Q4 | [태블릿에 띄우기] → 아이패드 앱(앞 · 뒤 둘 다) | QR 화면 → 고객 폰으로 찍으면 아이패드 화면 저절로 닫힘 · 데스크 웹도 「입력 중」 |
| Q5 | 직원 폰 앱 예약 상세 [이 기기에 QR 보이기] | 같은 흐름 1회 |
| Q6 | 10분 동안 안 찍기 · 새 QR 만든 뒤 옛 QR 찍기 · [닫기] 뒤 찍기 | 만료 화면 · 「새 QR …」 화면 · 「새 QR …」 화면 |
| Q7 | 입력 중 새로고침 | 다시 열림(답은 처음부터 — OQ-806) |
| Q8 | 안드로이드 폰 크롬(있으면) | Q1 과 같음 — 기본값(OQ-810) |

- 제출이 KOS 시험 고객 값(성별 · 생년월일 · 휴대폰 · 주소 · 동의)을 바꾼다 — 데모 흔적으로 둔다(D7-16 Q-153) · 휴대폰은 앞 0 빠진 값
- 스크린샷 · 리포트에 토큰 · QR · 실제 이름 · 번호 0(§7.5)

## 11. env

| 이름 | 쓰는 곳 | 기본 |
|---|---|---|
| `PROC_FRONT_ORIGIN` | QR 주소 바탕(이미 있음 · CORS) | 지금 값 |
| `PROC_SESSION_SECRET` | 토큰 HMAC(이미 있음 · 직원 토큰) | 지금 값 |
| `PROC_DISPLAY_TTL_MIN` | 여는 시한(이미 있음) | 10 |
| **`PROC_QWEB_FILL_MIN`** | 쓰는 시한(새) — `.env.example` 이름 한 줄 · 운영 값은 기본 그대로 | 60 |

## 12. 열린 것

| # | 무엇 | 기본값(제안) | 상태 |
|---|---|---|---|
| OQ-801 | 토큰을 어디에 싣나 · 어떻게 만드나 | 주소 fragment `/q#<token>` + API 헤더 `X-Questionnaire-Token` · HMAC(`PROC_SESSION_SECRET`, 요청 id · nonce) · DB 엔 nonce · 해시(§2 · §3.1). 대안 = 경로 `/q/<token>`(접근 로그에 남음) | 새로 · planner 기본값 |
| OQ-802 | 앱 문진 잠금 · `POST /api/auth/unlock` | 함께 없앤다(잠금이 없으면 부르는 곳 0 · 경로 49). 남기면 경로 50 | 새로 · planner 기본값 |
| OQ-803 | 시한 | 여는 시한 10분(D7-44 그대로) · 쓰는 시한 60분(`PROC_QWEB_FILL_MIN`) · 화면에 남은 시간 안 보임 | 새로 · planner 기본값 |
| OQ-804 | 속도 제한 · 겹친 제출 잠금을 back 메모리로 | 한 파드 전제로 메모리(§7.3) · 파드를 늘리면 DB 로 옮김 | 새로 · planner 기본값 |
| OQ-805 | 같은 링크를 다른 폰이 열기 | 막지 않음 · 먼저 제출이 이김 | 새로 · planner 기본값 |
| OQ-806 | 입력 중 새로고침 때 답 남기기 | 남기지 않음(브라우저 저장 0 — 고객 폰에 개인정보를 두지 않음) | 새로 · planner 기본값 |
| OQ-807 | 링크만 있으면 미리 채운 개인정보가 보임 | PoC = 보임(Q-150 미리 채움 결정 그대로) · 짧은 시한 · 한 번 제출 · 법적 검토 주석 | 새로 · 법적 검토(나중) |
| OQ-808 | [링크 복사] · [메신저 전송] — 주소가 이제 https 라 만들 수는 있음 | 없음(D7-44 그대로) | 새로 · 사용자 |
| OQ-809 | 직원 앱 QR 화면 안내 언어 | 한국어 + 영어 두 줄 | 새로 · planner 기본값 |
| OQ-810 | 고객 폰 E2E 기기 | 아이폰 Safari 필수 · 안드로이드 크롬은 있으면 | 새로 · 사용자 |
| OQ-811 | KOS 없이 갈 때 고객 기본 값(성별 · 생년월일 · 휴대폰 · 주소 · 동의)의 원천 · 바꾸는 시점 | 이번 판 밖 — 바꿀 때 정한다(§9) | 열림 · 사용자 |
| OQ-812 | 옛 TestFlight 빌드(앱 문진 화면 있음) | 다음 빌드로 바꿈 · 옛 빌드의 문진은 배포 뒤 404(받아들임) | 새로 · planner 기본값 |
| OQ-813 | QR 주소 바탕 env | `PROC_FRONT_ORIGIN` 재사용(새 env 없음) | 새로 · planner 기본값 |
| OQ-814 | 고객 화면 디자인 | 시안 없음 → DS 기본값(모바일) · E2E 에서 고침 | 새로 · planner 기본값 |

## 부록 A. DEC-008 대응표

| D8 | 절 |
|---|---|
| D-01 문진 = 고객이 웹에서 | 머리말 · §1.1 · §4 |
| D-02 방식 = ccc 고객용 웹 페이지(KOS 설문 링크 아님) | §1.1 · §1.2 · §2 |
| D-03 흐름 — QR = 데스크 웹 · 직원 앱 · 고객 폰으로 찍음 · 로그인 없는 토큰 링크 | §2 · §3 · §8 |
| D-04 제출 = 지금 KOS(BE4 재사용) · 나중에 ccc | §6.2 · §6.3 · §9 |
| D-05 앱 APP5 문진 화면 뺌 | §1.2 · §6.2 · §8.2 |
| D-06 이어 가는 문진 결정(언어 원천 · 칩 · 미리 채움 · 주민번호 · 매 방문 · 이력 · 다시 띄우기) | §3.3 · §4 · §4.1 · §6.4 |
| D-07 법적 검토 = 주석으로만 | §7.6 · OQ-807 |
| D-08 순서 = 앱 판 끝낸 뒤 · 문서부터 | WORK-010 Meta |
