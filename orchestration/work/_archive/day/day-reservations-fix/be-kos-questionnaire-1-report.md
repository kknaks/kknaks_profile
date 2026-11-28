# be-kos-questionnaire-1 — KOS 문진(초진설문) 읽기 실물 확인

- 워크트리 `CENTURION_DAY/day-reservations-fix` (base `origin/dev` `65506f35`) · **레포 변경 없음 · 커밋 없음**(`git status` 깨끗 · `uv sync --frozen` 으로 만든 `.venv` 는 gitignore 대상).
- 스크립트: `/private/tmp/be-kos-questionnaire-1/live.py`(실물) · `har_shape.py`(HAR 모양). DAY `KosClient.open()` · `internal()` 그대로 사용 · 새 HTTP 코드 없음.
- KOS 값 파일: 브리프는 `deploy/local.env` 를 가리켰지만 `DAY_SEED_KOS_*` · `KOS_*_BASE` · `KOS_WEB_BASE` · `KOS_CLIENT_TAG` 는 **같은 폴더 `deploy/kos-demo.env`** 에 있다(`local.env` 엔 KOS 키 없음). 읽기만 · 출력 없음.
- 데모 확인: `check_demo_tenant` OK → 공개 `get-zones` + 내부 `get-reservation-groups` 로 `check_open_key_is_demo` OK. 그 뒤에만 고객 조회.
- **로그인 세션 해제(코디 허용 · 11-27)**: 첫 실행에서 시스템 계정 sign-in 이 5기기 한도로 401(자동 해제 꺼 둔 상태 · 그 실행은 KOS 쓰기 없음). 코디 허용 뒤 `KOS_CLIENT_TAG` 를 켜서 DAY 기본 동작(같은 태그 로그인 중 가장 오래된 1개 해제 · 1회)으로 다시 실행 — **실행 창 2026-11-27 04:09:46Z ~ 04:11:46Z (KST 13:09:46 ~ 13:11:46)**. 해제는 `KosClient` 가 INFO 로그로만 남기는데 스크립트가 INFO 를 안 찍어 **실제로 해제됐는지는 로그로 확정 못 함**(두 번째 실행은 401 없이 바로 통과 — 한도가 그새 풀렸거나 1개 해제가 일어남). 해제됐다면 이 창 안 1회 · 같은 태그(`KOS_CLIENT_TAG`) 세션만. **dev 서버 동기화가 같은 태그를 쓰면 이 시각에 끊겼을 수 있다 — 확인 필요.** 다시 실행하지 않았다(추가 sign-in · 해제 피함).
- 비밀값 · 토큰 · 고객 개인정보 · 답 원문은 출력 · 기록하지 않았다(키 · 모양 · 개수 · id 앞 8자만).

## 요약 표

| # | 확인 | 경로 | 응답 코드 | 결과 | 비고 |
|---|---|---|---|---|---|
| 1 | 문진 읽기 API | 공개 `POST visitor/open/v1/queries/get-questionnaire-submit` body `{visitorId}` (근거: KOS OpenAPI `2026-09-18-kos-openapi.yaml:4397` `getQuestionnaireSubmit` 「제출된 초진 설문지 조회」 · cc-prototype `origin/main:procedure/back/app/service/reservations.py:82 · 599` 가 이미 부름 · `ax-clinic-project/scripts/kos_collect_extra.py:14`) | 200 = 제출 있음 · 400 `InvalidRequestException` `visitorId NotFound` = 제출 없음(또는 고객 없음 — 둘이 같은 코드) | 실물 OK. 응답이 `data` 로 감싸지지 **않음**(OpenAPI 는 `data` 라 적었지만 실물은 최상위 키). 키 = `id`(제출 id · visitorId 와 다름 12/12) · `visitorId` · `visitorName` · `phoneNumber` · `phone{countryCode,phoneNumber}` · `address` · `addressDetail` · `dateOfBirth`(8자리 `yyyyMMdd`) · `gender` · `phoneticName` · `createdDateTimeUtc` · `answers[]` · `agreements[]` | **목록 API 없음** — 「목록」과 「상세」가 같은 한 번 호출(고객 1명 → 제출 1건). 내부(웹) 경로 `visitor/questionnaire/v1/queries/get-questionnaire-submit/legacy`(HAR 31건 · KOS 웹 고객 차트가 부름)도 실물 200 · **같은 id · 같은 제출 시각 · 같은 키**(감싸기 없음) |
| 2 | 제출 시각 | `createdDateTimeUtc` | — | ISO 8601 **UTC `Z`** (12/12). **고객 단위**(요청 = `visitorId` 만 · 일정 id 없음 · 응답에 일정 id 없음). **이력 안 옴 — 한 건만** | 여러 번 낸 고객이 어느 건을 받는지(마지막? 처음?) **확인 안 됨** — 두 번 제출해 보려면 KOS 쓰기라 안 함. HAR 4명 · 실물 12명 모두 1건. KOS 웹 화면도 「초진설문 n시간 전 제출」 한 줄(캡처 `:73`) |
| 3 | 문항 1:1 | 양식 `visitor/open/v1/queries/get-visitor-questionnaire`(DAY 가 이미 쓰는 경로) ↔ 제출 읽기 `answers[]` | 200 | **질문 수준 같음**: 5명 모두 양식 질문 15 · 답의 질문 id 15 · 답 질문 ⊂ 양식 15/15 · 양식에 없는 질문 0 · 안 답한 질문 0. **답 한 줄 모양은 DAY 저장분과 다름**(아래 대조 표) | DAY 는 자기 문항 정의가 **없다** — DAY 고객 문진 웹의 양식이 KOS `get-visitor-questionnaire` 를 그때그때 받아 그린다(`emr/kos/identity.py:29 · 134-145` · `services/questionnaire_public.py:229 · 276`). 그래서 「문항이 같다」는 구조상 참. 보기(답) id ↔ 양식 보기 id 대조는 **미확인**(스크립트가 양식 보기 키를 `id` 로 읽었는데 실물 키는 `answerId` — 0/15 는 스크립트 버그. 다시 돌리면 sign-in 이 또 생겨 안 돌림) |
| 4 | 바뀐 것만 가져올 길 | `get-visitors`(내부 목록) 행 · `get-visitor`(내부 상세) | 200 | **없음** — 두 응답에 문진 · 설문 관련 키 0개(`quest|survey|first|initial` 검색). 제출 읽기 API 에 날짜 거르기 없음(body = `visitorId` 하나) | OpenAPI 의 날짜 범위 거르기(`submittedDateTimeRange`)는 **만족도 조사**(`find-satisfaction-survey-answers`)뿐 — 초진설문 아님 |
| 5 | 데모 고객 중 제출자 | 공개 `get-questionnaire-submit` × 고객 400명(전체 608 · `lastVisitedDateTimeUtc` 내림차순 앞 400) | 200 × 12 · 400 × 388 | **12명** — 앞 8자: `6b00149a` `6af28880` `6adb0aaf` `6ab9c5ff` `6ae057e3` `6a8d8c49` `6a97734b` `6a8fed89` `6a8e4643` `6b07896c` `6ae147f6` `6ae0582e` | 나머지 208명은 안 봄. 12명 중 DAY 고객 문진 웹에서 내 KOS 로 간 것인지 KOS 에서 직접 낸 것인지는 구분 못 함(KOS 응답에 출처 칸 없음) |

## 문항 · 답 대조 표

DAY `questionnaire_history.answers` = 고객이 DAY 웹에서 낸 **KOS 제출 본문 그대로**(언어만 뺌 · `services/questionnaire_public.py:361` · `services/questionnaire_kos.py:52 payload_of`) — 즉 KOS **제출** 모양(`SubmitVisitorQuestionnaireCommand` · 답 = `SelectedAnswer`). KOS **읽기** 응답은 다른 모양(`GetQuestionnaireSubmitLegacyQueryResponse` · 답 = `QuestionnaireSubmitAnswer`).

### 답 한 줄

| DAY 저장(제출 모양 `SelectedAnswer`) | KOS 읽기(`QuestionnaireSubmitAnswer`) | 판정 | 비고 |
|---|---|---|---|
| `parentQuestionId` | `questionId` | 같음(이름만 다름) | 실물: 답 질문 id 가 양식 질문 id 안 15/15 |
| `parentQuestionTitle` | `questionTitle` | 같음(이름만 다름) | 값 같은지는 안 봄 |
| `id` | `answerId` | 같음(이름만 다름) · **값 대조 미확인** | |
| `title` | `answerTitle` | 같음(이름만 다름) | |
| `inputText` | `memo` | 조건부 같음 | OpenAPI: `inputType = INPUT_BOX` 일 때만 memo 로 저장(`openapi.yaml` `SelectedAnswer.inputText`). 실물 memo 채워진 줄 0 ~ 4 |
| `subText` | — | DAY 만 | KOS 읽기에 없음. DAY `health_lines` 는 `inputText` 가 비면 `subText` 를 씀(`policies/questionnaire.py` `health_lines`) |
| `inputType` | — | DAY 만 | KOS 읽기에 없음. DAY `health_lines` 가 `INPUT_BOX` 면 보기 제목을 뺀다 → KOS 읽기분은 양식(`get-visitor-questionnaire` 의 보기 `inputType`)으로 되찾거나 memo 유무로 갈라야 함 — **추정 금지 원칙상 정할 것** |
| — | `seq` | KOS 만 | 실물 12/12 모두 빈 글자 `""` — 쓸 값 없음 |

한 질문에 답 여러 줄(복수 선택) — 실물 질문 15 · 답 15 ~ 50줄. DAY 저장분도 보기마다 한 줄이라 같은 꼴.

### 머리 칸

| DAY 저장(제출 본문) | KOS 읽기 | 판정 |
|---|---|---|
| `name` | `visitorName` | 이름만 다름 |
| `dateOfBirth`(yyyyMMdd) | `dateOfBirth`(실물 8자리) | 같음 |
| `gender` | `gender` | 같음 |
| `phone{countryCode,phoneNumber}` | `phone{…}` + `phoneNumber`(폐기 예정) | 같음 |
| `address` · `addressDetail` | 같은 이름 | 같음 |
| `agreements[]` | `agreements[]`(`id,title,link,required,translsMap,type,agreed`) | 같은 모양(HAR 제출 본문과 같음) |
| `phoneticName` · `registrationNumber` | `phoneticName` 만 | DAY 는 둘 다 제출 금지(`FORBIDDEN_FIELDS`) · KOS 읽기엔 발음만 |
| — | `id`(KOS 제출 id) · `visitorId` | KOS 만 — DAY 행에 KOS 제출 id 칸 없음(`submit_questionnaire` 가 응답 `questionnaireId` 를 버림 · `emr/kos/identity.py:161-165`) |
| `submitted_at`(DAY 시각) | `createdDateTimeUtc` | 뜻 같음 · 출처 다름 |
| `visit_id` · `display_request_id` · `device_id` · `source` · `crm_*` | — | DAY 만 — KOS 읽기분은 `visit_id` 없음(고객 단위) |

**결론**: 「KOS 문진 항목이 DAY 와 완전히 같다」 = **질문(문항) 기준으로 참**(DAY 가 KOS 양식을 그대로 씀 · 실물 15/15). **저장 모양은 다름** — 키 이름 4개 바뀜 · `inputType` · `subText` 가 KOS 읽기에 없음 · `seq` 는 늘 빈 값. 동기화하려면 `emr/kos/mapper` 에 읽기 → 우리 형식 변환이 필요하고, 화면(`health_lines`)이 기대는 `inputType` 을 어떻게 채울지 정해야 한다.

## 동기화 방식 후보 (결정 아님)

KOS 에는 「바뀐 문진만」 길이 없다 → 모두 **고객 1명당 호출 1번** 꼴.

| 후보 | 방법 | 호출량 | 장단 |
|---|---|---|---|
| A. 그때 읽기 | 예약 상세 · 고객 차트를 열 때 그 고객 `get-questionnaire-submit` 1번 → 6개월 판정 | 화면 1번당 1 | 늘 최신 · 화면이 KOS 응답을 기다림(시한 필요) · 실패 시 표시 규칙 필요 |
| B. 오늘 방문 고객만 | 일정 동기화(오늘 · 예약 · 접수)가 고객을 볼 때 그 고객 문진도 읽어 저장 | 하루 방문 고객 수 | 6개월 판정이 필요한 사람만 · 화면 안 기다림 · 당일 KOS 에서 낸 것은 다음 동기화까지 늦음 |
| C. 전체 백필 + 주기 | 고객 목록(`get-visitors`) 전체를 돌며 읽기(데모 608명 = 608회 · 1초 1회면 ~10분) | 고객 수 / 주기 | 고객 차트도 다 채움 · 무거움 · 안 바뀐 것도 매번 읽음 |

### 정할 것

1. **단위**: KOS 는 고객 단위 · 한 건만 준다 — DAY 행의 `visit_id` 를 비울지(null 허용 칸 · `models/reception.py`), 6개월 판정을 고객 단위로 바꾸는 것(research-1 Q10)과 같이 정할 것.
2. **이력**: KOS 는 마지막(으로 보이는) 한 건만 — 여러 번 낸 고객의 앞 이력은 KOS 에서 못 가져온다. 어느 건을 주는지는 쓰기 금지라 미확인 → 실물로 두 번 내 보는 확인이 따로 필요한지.
3. **되돌아옴(중복)**: DAY 웹에서 낸 문진은 KOS 로 보내지므로(`crm_status = sent`) KOS 읽기에 **그 제출이 다시 나온다**. DAY 행에 KOS 제출 id 가 없어 같은 건인지 가를 키가 없다 → (a) 제출 응답 `questionnaireId` 를 저장 칸에 남기기(외부 id 는 `external_ref` 한 테이블 원칙) (b) 시각 근사 비교(추정이라 비권장) 중 선택.
4. **`source = read`**: `enums/reception.py` 에 이미 `read` 값이 있으나 쓰는 코드 없음 — KOS 에서 읽은 행에 이것을 쓸지.
5. **`inputType` · `subText` 빈자리**: 양식에서 되찾을지(양식이 바뀌면 틀릴 수 있음) · 비워 두고 화면 규칙을 memo 기준으로 바꿀지.
6. **400 의 두 뜻**: 「제출 없음」과 「고객 없음」이 같은 `visitorId NotFound` — 연결된 고객이면 「제출 없음」으로 읽어도 되는지.
7. **세션 해제 확인**: 위 실행 창(04:09:46Z ~ 04:11:46Z)에 dev 서버 KOS 동기화가 끊겼는지.

## 미확인 · 주의

- 보기 id(`answerId`) ↔ 양식 보기 id 값 대조(스크립트 키 실수 · 재실행 안 함).
- 여러 번 제출한 고객의 응답이 어느 건인지.
- 고객 208명(608 중 400만 봄)의 제출 여부.
- 세션 해제가 실제로 일어났는지(INFO 로그 안 찍음).
