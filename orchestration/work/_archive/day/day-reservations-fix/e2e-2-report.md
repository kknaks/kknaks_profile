# e2e-2 — KOS 문진 제출 500 원인 · 제출 id 위치 · 시험 문진 지우기

2026-11-28 · 스택(11340) · 워크트리 코드 안 건드림 · 스크래치 스크립트만(DAY 어댑터 · 스키마 import). KOS 호출은 서버 공유 시스템 토큰(Redis) — 새 로그인 없음. id 앞 8자.

## 1. 제출 1회 — 응답 모양
- 대상: 고객 `f68fd438`(KOS `6b081f36` · 생년월일 · 성별 FEMALE 이 KOS 에 있음 · 그 전 legacy 읽기 400 · qa 방문 고객 아님).
- 페이로드 = DAY 와 같은 생성: `day.js` `answersBody`/`submit` 꼴(보기 원본 `...a.raw` + `parentQuestionId` · `parentQuestionTitle` · `id` · `title` · `inputType` · `inputText ""` · `subText ""`) → `PublicQuestionnaireSubmit.model_validate(...).model_dump(exclude_unset, mode="json")`(라우터와 같음) → `language` 뺌(`questionnaire_public._save`) → `{**payload, "visitorId"}`(`identity.submit_questionnaire`) → 공개 `visitor/open/v1/commands/submit-visitor-questionnaire`(DAY 지금 경로 그대로) **1회 · 재시도 없음**.
- 응답: **HTTP 200** · `application/json` · 본문 = `{"questionnaireId": "6b0a73fd…"}`(최상위 키 하나 · 24자 ObjectId) — 06:26:05Z.

## 2. 제출 id 위치
- **최상위 `questionnaireId`**. KOS OpenAPI(`ax-clinic-project/para/archive/inbox_archive/2026-09-18-kos-openapi.yaml:15241-15249` `SubmitVisitorQuestionnaireCommandResponse` — required `questionnaireId` · object-id)와 같다. KOS 웹 고객 페이지의 **내부** 제출(`…/visitor/questionnaire/visitor/v1/commands/submit-questionnaire/legacy` · HAR `설문내용.har`)도 200 `{"questionnaireId": str}`.
- 내부 legacy 읽기(`get-questionnaire-submit/legacy`) `id` = `6b0a73fd…` · `createdDateTimeUtc` 06:26:05Z · 답 14 — **제출 응답 id = 읽기 id**(앞 8자 · 제출 시각 같음 · D46 ② 확인. 전체 24자 대조는 스크립트가 응답 id 를 저장하지 않아 앞 8자 + 시각으로 판정).
- 코드 `emr/kos/identity.py` `submit_questionnaire` = `questionnaireId` 최상위 먼저 → 없으면 `data.questionnaireId` — **맞음**(최상위에서 읽힘 · `data` 갈래는 안 쓰임).

## 3. e2e-1 의 500 원인(후보 · 한 줄씩)
OpenAPI 설명(`:4209`): 「설문 응답을 **저장하고**, 설문 응답 내용을 기반으로 **내원객의 기본 정보 일부를 갱신**합니다」 — 저장 뒤 고객 갱신 단계가 있다. e2e-1 은 응답 저장(읽기 200 `6b0a712a`)은 됐고 고객 값은 안 바뀜(1b9a7c0c 지금도 생년월일 없음 · `GENDER_UNSPECIFIED`) → **저장 뒤 고객 갱신 단계에서 실패**로 읽힌다.
| 차이 | e2e-1(500) | e2e-2(200) | 판정 |
|---|---|---|---|
| 휴대폰 `phone.countryCode` | **빈 글자**(KOS 고객 미리 채움이 비어 그대로) | 있음(KOS 값) | **가장 유력** — 고객 갱신이 휴대폰을 파싱(OpenAPI 400 예: `countryCode` NotAvailable · 빈 값은 그 예외 밖에서 500 이 났을 수 있음) |
| 생년월일 | 시험 값 `19900101`(KOS 고객 값 없음) | KOS 값 그대로 | 후보 — 갱신 단계 값 충돌 가능 |
| 성별 | FEMALE(KOS 는 `GENDER_UNSPECIFIED`) | FEMALE(KOS 값과 같음) | 후보(약함) |
| 답 한 줄 키 | 7키(`answerId` · `isSubText` · `translsMap` 없음 · 스크립트가 원본을 안 펼침) | 10키(웹 화면과 같음) | 약함 — 응답 저장은 이 꼴로도 됐음(읽기 답 14) |
| 첫 보기 · INPUT_BOX 1문항 건너뜀 · 약관 | 같음 | 같음 | 원인 아님(둘 다 같음) |
| `subText` | 빈 글자 | 빈 글자 | 원인 아님 |
- 한 번만 내라는 조건이라 갈라 보지 못함 — 「휴대폰 국가번호 빈 값 → 고객 갱신 500」이 가장 유력(확정 아님). DAY 고객 웹은 국가번호를 미리 채움 그대로 보낼 수 있다(`day.js:6540` `countryCode: st.cc.trim()` · 서버 스키마 `SubmitPhone` 은 빈 값 허용).

## 4. 시험 문진 지우기 — **경로 없음 · 안 지움**
- KOS OpenAPI 경로 중 문진은 `submit-visitor-questionnaire` · `get-questionnaire-agreements` · `get-questionnaire-submit` · `get-visitor-questionnaire` 4개뿐(`:4203` · `:4375` · `:4397` · `:4504`) — 지우기 없음(지우기 경로는 상품 2개뿐 `:941` · `:988`).
- HAR(`~/Downloads/*.har` 전부) 의 문진 경로 = `issue-questionnaire-link` · `get-questionnaire-submit/legacy` · `visitor/v1/commands/submit-questionnaire/legacy` — 지우기 · 취소 호출 없음.
- DAY · cc-prototype 코드에도 문진 지우기 경로 없음. 경로를 지어 부르지 않았다.
- 남은 시험 제출(KOS DEMO): `6b0a712a`(고객 `1b9a7c0c` · KOS `6b083e1b` · e2e-1) · `6b0a73fd`(고객 `f68fd438` · KOS `6b081f36` · e2e-2). 지우려면 KOS 웹 화면에서 지우는 동작의 HAR 를 떠야 한다(사람 · KOS 쪽 문의).
- 부수 효과 확인: e2e-2 제출이 고객 갱신을 했어도 값은 KOS 원래 값 그대로라 바뀐 것 없음(생년월일 있음 · FEMALE 그대로 · 주소는 원래 비어 있음). e2e-1 고객(1b9a7c0c)도 안 바뀜.

## 5. 코드 제안(안 고침)
- ⓐ `backend/day/services/questionnaire_kos.py:105` — `error = f"{type(exc).__name__}:{status}" if status else type(exc).__name__` → `name = getattr(exc, "name", "")` 를 붙여 `f"{type(exc).__name__}:{status}:{name}"`(`KosError.name` = 응답 `className` 꼬리 60자 · 값 · 개인정보 없음 · `client.py:156-166`) — 500 의 KOS 예외 이름이 `crm_error` 와 경고 로그에 남는다.
- ⓑ 500 인데 KOS 에 저장된 경우 [다시 보내기] 이중 제출 막기 — `questionnaire_kos.py` `send`(:85-130) 안, `adapter.submit_questionnaire` 실패(`EmrError` · `status >= 500` 또는 시간 초과) 직후 **같은 어댑터로 내부 legacy 읽기 1회**(`adapter.read_questionnaire(visitor)` — 이미 있는 내부 경로 · 공개 호출 아님): 읽은 제출의 `submitted_at` ≥ 이 행 `submitted_at`(DAY 저장 시각) 이면 KOS 가 받은 것으로 보고 `result = SENT` · `crm_error = None` · `_remember_submit(..., read.external_id)`. 같은 검사를 `resend`(:187-) 가 행을 잡기 전에도 1번(이미 KOS 에 있으면 409 대신 sent 로 맞추고 신호). 비교 기준은 「KOS 제출 시각 ≥ DAY 행 저장 시각」(KOS 는 고객당 마지막 1건만 줌 — 그 뒤 다른 경로로 낸 제출도 같은 고객이면 이 행의 것으로 보게 되는 빈틈은 알고 감).
- ⓒ (원인 후보 대응) 고객 웹 제출 검사에서 `phone.phoneNumber` 가 있는데 `countryCode` 가 비면 400(또는 화면에서 국가번호 필수) — `schemas/public_questionnaire.py` `SubmitPhone` · `day.js:6540`. SPEC 글자 · 결정이 필요하면 코디 판단.

## 6. KOS 로그인
- 이번 단계에서 테스트 계정 로그인 안 함 · 시스템 계정은 서버 공유 토큰 사용 → 해제할 내 로그인 없음. 테스트 계정 활성 로그인 2개(06:18:02 · 06:18:39)는 내 것 아님(그대로 둠).
