# api-swagger-docs backend 결과 보고

## 상태: done (커밋 · push · PR 없음 — 워크트리에 변경만)

워크트리 `/Users/kknaks/orca/workspaces/cc-prototype/api-swagger-docs` · 브랜치 `kknaksss/api-swagger-docs` · base `77173cf`.
옆 파일: `openapi-before.json`(77173cf 그대로) · `openapi-after.json`(작업 뒤) — 둘 다 `create_app(Settings(...)).openapi()` 덤프(서버 안 띄움).

## 1. 변경 파일 (전부 `procedure/back/` 안)

| 파일 | 내용 |
|---|---|
| `app/main.py` | `FastAPI(title="CCC procedure API", version="0.1.0"(그대로), description=…, openapi_tags=…, docs_url="/api/docs", redoc_url="/api/redoc", openapi_url="/api/openapi.json", swagger_ui_oauth2_redirect_url="/api/docs/oauth2-redirect")` · health 에 tags · summary · description · 끝에 `decorate(app)` |
| `app/openapi_docs.py` (신규) | app description(공통 규칙 · 통역 WS 프로토콜) · 태그 12개 설명 · `decorate()` = `app.openapi` 감싸 스키마 dict 만 고침(securitySchemes · operation security · 422 제거) |
| `app/api/docs.py` (신규) | 문서용 `ErrorResponse`/`ErrorDetail`/`DuplicateCandidate` 모델 · `errors(...)`(→ `responses=`) · `binary(...)` · 태그 이름 상수 · 공통 오류 항목(INVALID · UNAUTHORIZED · FAKE_BOARD · KOS_*) |
| `app/api/{actions,auth,board,chat,devices,display,notifications,photos,public_questionnaire,reservations}.py` | 라우트마다 summary · description · responses(오류 전수) · 한국어 tags · 경로/쿼리/헤더 파라미터 description · multipart 는 `openapi_extra` requestBody · 바이너리는 `binary()` |
| `app/schemas/{actions,board,chat,reservations}.py` | 모든 모델 docstring · 모든 필드 `Field(description=…)` |
| `tests/test_openapi_docs.py` (신규) | 문서 경로 · 설명 빠진 곳 0 · 422 없음 · Bearer 표시 = require_login 과 일치 · 401 모양 그대로 (7개) |

`app/api/interpret.py` · `deps.py` · service · domain · repository · front · infra · compose · env · 정적 `api-reference.html` 무수정.
태그: 인증 · 현황판 · 조작 · 예약 · 고객 · 알림 · 기기 · 표시 요청 · 공개 문진 · 신분증 사진 · 채팅 · 상태(12). `GET /api/devices/targets` 는 기기 + 표시 요청 두 태그 · `/api/customers/*`(검색 · personal · remark · identity · funnel) = 고객 · `passport-scan` = 신분증 사진.

## 2. 수치 (기준선 → 이후)

| | 기준선(77173cf) | 이후 |
|---|---|---|
| `uv run pytest -q` | 536 passed | **543 passed** (+7 = 새 `test_openapi_docs.py` · 기존 536 그대로 통과) |
| `uv run ruff check .` | All checks passed | All checks passed |

기능 폴더 밖 import 없음(새 import 는 `app.*` · `fastapi.*` · `pydantic` 만). 서버 · 포트 · 프로세스 안 건드림(TestClient · `app.openapi()` 만).

## 3. before / after OpenAPI 구조 비교 — 구조 변화 0

비교 스크립트: 양쪽 `$ref` 를 풀고 `description` · `examples` · `example` 키만 뺀 뒤(필드 이름은 지우지 않음) operation 집합 · operationId · parameters · requestBody · 200 `application/json` 스키마 · 기존 components 스키마 전부를 같게 비교.

```
operations before=70 after=70
schemas before=168 after=169 · added(문서용)=['DuplicateCandidate', 'ErrorDetail', 'ErrorResponse']
removed: ['HTTPValidationError', 'ValidationError'] (FastAPI 기본 422 용)
NOTE ('GET', '/api/board/stream'): 200 content 문서 추가 ['text/event-stream']
NOTE ('GET', '/api/chat/photos/{photo_id}'): 200 content 문서 추가 ['image/jpeg']
NOTE ('GET', '/api/chat/videos/{video_id}'): 200 content 문서 추가 ['video/mp4']
NOTE ('GET', '/api/chat/videos/{video_id}/thumbnail'): 200 content 문서 추가 ['image/jpeg']
NOTE ('GET', '/api/id-photos/{photo_id}'): 200 content 문서 추가 ['image/jpeg']
NOTE ('POST', '/api/chat/photos'): requestBody 문서 추가(전엔 없음 · request.form() 수동 파싱) — ['multipart/form-data']
NOTE ('POST', '/api/chat/videos'): requestBody 문서 추가(전엔 없음 · request.form() 수동 파싱) — ['multipart/form-data']
NOTE ('POST', '/api/customers/{customer_id}/passport-scan'): requestBody 문서 추가(전엔 없음 · request.form() 수동 파싱) — ['multipart/form-data']
PROBLEMS: 0
```

- 경로 64 · operation 70 · 파라미터(이름 · 위치 · 필수 · 타입 · 기본값) · 요청 본문 필드 이름 · 타입 · 필수 · 기본값 · 200 응답 스키마 · 기존 166개 스키마 = **전부 같다**.
- 늘어난 것: 설명 · tags · security · 문서용 오류 모델 3개 · 4xx/5xx `responses` · 바이너리/SSE 200 content · multipart requestBody 문서 3개(코드는 `request.form()` 수동 파싱 그대로 — `File/Form` 파라미터 안 넣음 · `openapi_extra` 만).
- 줄어든 것: **FastAPI 기본 `422` 응답 표기와 `HTTPValidationError`/`ValidationError` 스키마** — 이 서버는 422 를 내지 않는다(main 의 처리기가 400 `invalid_request` 로 바꿈). 틀린 문서라 문서에서만 뺐다(동작 무관). 코디가 원치 않으면 `openapi_docs._patch` 의 두 블록을 지우면 된다.
- 코드 수준 추가 확인(AST): 10개 라우터 · 4개 스키마 파일의 **함수 본문(docstring 제외) · 인자 이름 · 클래스 필드 타입 주석 · 클래스 대입문**을 HEAD 와 비교 → 차이 2 = `main.create_app`(이번 변경) · `CreateCallRequest.target` 의 `Field(discriminator="kind")` 에 `description=` 추가뿐.
- `chat.py` 는 `tests/test_chat_r3.py::test_chat_route_handlers_async`(데코레이터 다음 줄이 `async def` 여야 함) 때문에 summary · description · responses 를 모듈 dict(`_D_<NAME>`)로 빼고 `@router.get(..., **_D_X)` 한 줄로 실었다 — 같은 kwargs.
- 문서 경로: `/docs` · `/redoc` · `/openapi.json` · `/docs/oauth2-redirect` 는 이제 back 에서 404(`not_found`) — 운영에선 원래 front 로 가던 경로라 영향 없음.

## 4. 커버리지 (openapi-after.json 기준 · 시험으로 고정)

| 항목 | before | after |
|---|---|---|
| operation | 70 | 70 |
| summary 있음 | 70 (함수 이름) | **70 / 70** (한국어) |
| description 있음 | 27 | **70 / 70** |
| responses 오류 표(4xx/5xx) 있음 | 0 | 로그인 · 검증이 있는 곳 전부(코드에서 raise 되는 DomainError 를 따라가 셈) |
| 파라미터 description | 0 / 62 | **62 / 62** |
| schema property(components + paths 안 inline · multipart 칸 포함) description | 0 / 664 | **683 / 683** |
| security(Bearer) 표시 | 0 | 65 (= 70 − login · health · stream · 공개 문진 2) |

`tests/test_openapi_docs.py` 가 summary · description · tags · 파라미터 · 모든 property description 이 비면 실패한다.
(브리프의 「엔드포인트 71개」는 정적 레퍼런스 기준 — 지금 OpenAPI 는 70 operation · 통역 WS 는 OpenAPI 밖이라 app description 에 적음.)

## 5. securitySchemes — 방법과 동작 불변 근거

- 방법: `app/openapi_docs.decorate(app)` 가 `app.openapi` 를 감싼다. 처음 만들 때 FastAPI 원래 `openapi()` 결과 dict 에
  `components.securitySchemes.BearerAuth = {type: http, scheme: bearer}` 를 넣고, `require_login` 을 (라우터 dependencies 포함) 의존성 트리에 가진 operation 에만 `security: [{BearerAuth: []}]` 를 붙인다. 라우트를 펴는 길은 FastAPI 0.156 이 OpenAPI 를 만들 때 쓰는 그것(`fastapi.routing.iter_route_contexts` + `fastapi.openapi.utils._get_api_route_for_openapi`) — 0.15x 는 `include_router` 를 `_IncludedRouter` 로 감싸 두어 `app.routes` 에 APIRoute 가 직접 없다.
- 근거: 라우트 · 의존성 · 예외 처리기 · 미들웨어는 하나도 안 바꿨다 — `HTTPBearer`/`Security` 의존성을 넣지 않았으므로 요청 처리 경로에 새 코드가 없다. 바뀌는 건 `/api/openapi.json` 이 내는 JSON 뿐. 시험 `test_security_is_docs_only`: `GET /api/auth/me` 무토큰 = 401 `{"error":{"code":"unauthorized","message":"로그인이 필요해요"}}` 그대로 · `WWW-Authenticate` 헤더 없음 · `/api/health` 200. `test_bearer_security_matches_require_login`: 모든 operation 의 security 유무 = require_login 유무 · 65개.
- 주의: `_get_api_route_for_openapi` 는 FastAPI 비공개 함수 — FastAPI 를 올리면 바뀔 수 있다. 바뀌면 위 시험이 깨져 알려 준다(조용히 security 0 이 되지 않게 개수까지 고정).
- 문서는 인증 없이 열린다(데모 · 운영 같은 동작 · 환경 분기 없음). CORS 무변경.

## 6. 확인 못 한 것 (코드로 뜻을 못 정해 설명에 짓지 않음 — 중립 서술만)

- KOS 값을 그대로 넘기는 칸의 값 집합: `gender` · `nationality`(형식 · `KR` 비교만 확실) · `language` · `currency` · `PrevProcedure.status` · `connectedChannel` · 문진 `QuestionnairePrefill.gender` / `PublicQuestionnaireSubmit.gender` 가 받는 값.
- `isNew`(예약) — KOS `isNew` 그대로라고만 적음. `sedationRequired` — 이름 이상 근거 없음.
- 고객 검색 조건의 매칭 방식(부분 일치 등) — KOS 가 정한다.
- KOS 객체를 그대로 넘기는 칸의 안쪽 구조: `Room.order`(현황판) · 문진 `pages` · `agreements`.
- 채팅 사진 · 동영상 `width` / `height` 의 단위 — 서버는 앱이 준 값을 검사 없이 저장(픽셀이라 쓰지 않음).
- `ReadResponse.lastViewedAt` 은 nullable 타입이지만 null 이 되는 코드 경로를 찾지 못함.
- 운영의 `PROC_SESSION_HOURS` 실제 값 — 문서엔 「env · 기본 12시간 · 정확한 만료는 `expiresAt`」으로 적음.

## 7. SPEC ↔ 코드 차이 · 발견한 버그 (고치지 않음 · 문서는 코드대로)

SPEC ↔ 코드
- 검증 오류: SPEC-005 는 모르는 요청 필드에 422 — 코드는 400 `invalid_request`(전 API 공통).
- 예약 API 역할: SPEC-005 §7.1 · 라우터 docstring 은 「네 역할」 — 코드는 로그인만 봄(counselor 포함 다섯 모두).
- SPEC-005 의 `closedDay`(예약판) · `defaultRoute`(상세) — 코드에 없음. `PUT /api/customers/{id}/funnel` 은 SPEC §7.5 표에 없음. `not_consultation_addable` 문구가 SPEC 과 다름.
- `not_movable`: SPEC 과 `RESV_CONFLICT_CODES` 에 있으나 모든 상태가 옮길 수 있어 실제로는 안 남 — 옮기기 응답 표에서 뺐다.
- 채팅 수정: SPEC-007 §5 = 남의 메시지(시스템 줄 포함) 403 `chat_not_yours` 먼저 — 코드는 남이 만든 시스템 줄에 400 `chat_not_editable`.
- 공개 문진 오류 `requestId`: 브리프 · 일부 설명은 410/409 에 `requestId` 가 실린다고 봤으나 코드는 응답 전에 지운다(`QuestionnaireService._target_or_deny` · `tests/test_app_qweb.py:123`) — 문서에서 뺐다.
- 가짜 모드(`PROC_FAKE_BOARD`) 예약 조회가 실 경로와 다름: 폼의 없는 `groupId` 에 400 안 남 · 검색이 `phone` 무시 · `birth` 형식 검사 없음 · 상세에 `displays` · `funnelCodes` · `customer.funnel` 없음.

보다가 본 버그 · 주의점
- `POST /api/display-requests` 에 `fake_board` 검사가 없음(가짜 모드에서도 됨) · 그 `deviceId` 는 남의 기기도 됨(`pending` · `claim` 만 자기 기기 검사).
- `POST /api/display-requests/claim` · `/{id}/close` 는 소유를 보지 않음 — 로그인한 아무 계정이나 아무 요청을 닫거나 스캔 토큰을 claim 할 수 있음.
- `POST /api/visits/{id}/anesthesia/end` 가 귀가 대기 카드에서도 됨(스냅샷 `canEnd` 는 false).
- `POST /api/notifications/read` 를 조건 없이 부르면 오늘 것만이 아니라 **안 읽은 전부**를 읽음 처리(목록은 오늘만).
- KOS env 가 비면 쌓인 KOS op 를 보내지 않고 계속 쌓기만 함.
- multipart 한도 초과(파일 2개 이상 · 칸 10개 초과 · 사진 아닌 칸 1MB 초과)는 Starlette 가 `400 http_error` 로 냄(`invalid_request` 아님) — 응답 표에 그대로 적음.
- 예약 생성: 새 고객 만들기는 성공하고 예약 호출이 실패하면 KOS 에 고객만 남음.
- `GET /api/reservations/{id}`(조회)가 DB 를 씀 — 문진 이력 행 추가 · 오래된 띄우기 요청 expired 처리.
- 예약에 고객이 없으면 `customer.customerId` 가 null 이 아니라 `0`. `ReceptionResponse.flowStep` 은 nullable 타입이나 null 이 안 됨.
- 취소 · 귀가는 사본 상태로 검사 — 사본이 갱신되기 전 다시 누르면 KOS 에 한 번 더 보냄.
- 채팅 `clientId` 는 계정 전체에서 유일(`UNIQUE(account_id, client_id)`) — 방 A 에 쓴 `clientId` 로 방 B 에 보내면 방 A 의 옛 메시지를 200 으로 돌려줌(설명에 주의로 적음). `Room.lastMessageAt` 은 멤버 입장 경계로 거르지 않아 `lastMessage` 가 null 인데 값이 있을 수 있음. 메시지에 안 붙은 업로드 사진 · 동영상은 지워지지 않음.
- 스키마 이름: `schemas/actions.py` 에 쓰이지 않는 `ErrorBody`/`ErrorResponse` 가 있고, `schemas/board`·`chat`·`reservations` 에 같은 이름(`Room` · `SyncInfo`)이 있어 OpenAPI 에 `app__schemas__board__Room` 같은 긴 이름이 나옴(77173cf 부터 그랬음 · 이름 안 바꿈). 문서용 오류 모델은 충돌을 피해 `ErrorDetail` 로 지었다.

## 운영 확인 (코디)
배포 뒤 `https://ccc.medisolveai.xyz/api/docs` · `/api/openapi.json` 이 열리는지 — ingress `/api` → back 이라 인프라 변경은 필요 없다고 보지만, 실제 운영에서 열어 보진 않았다(pending · 이번 범위 밖).

## 수정 1판 — 리뷰 WARN 34건 문구 수정 (2026-11-11)

상태: done. 리뷰 근거(파일:줄)를 하나씩 열어 확인했고 **34건 모두 리뷰어가 맞음 → 34건 고침 · 안 고친 것 0**. 바뀐 것은 description · summary · `responses=` 표 · `Field(description=…)` 문구 · 시험뿐(동작 · §7 버그 무수정).

변경 파일(1판 위에 덧고침): `app/api/{actions,board,chat,devices,display,photos,public_questionnaire,reservations,docs}.py` · `app/schemas/{actions,board,chat,reservations}.py` · `tests/test_openapi_docs.py`.

### W 번호별 처리

| W | 처리 | 요약 (근거) |
|---|---|---|
| **W-R2** (우선) | 고침 | 예약 등록 설명 맨 위 굵은 **주의**: 「일정 id · 고객 id 없음」 502 는 KOS reserve · create-visitor 쓰기가 **끝난 뒤** 남 → 재시도하면 중복될 수 있으니 먼저 조회로 확인. 502 표 · 「멱등 아님」 줄에도 (service/reservations.py:837-839,938-940) |
| **W-C3** (우선) | 고침 | 메시지 목록 굵은 **주의**: `since` 의 `+` 는 `%2B` 로 URL 인코딩 — 안 하면 공백으로 읽혀 400 invalid_request. `since` 쿼리 설명 · 400 표에도 (clock.py:43-51 · service/chat.py:356-362) |
| **W-C2** (우선) | 고침 | 굵은 **주의**: 지운 메시지 = `deletedAt` 에 지운 시각 · text · photo · video 만 null — `deletedAt == null` 로 거르면 놓침 (service/chat.py:107-120) |
| **W-R1** (우선) | 고침 | 접수 · 상담 추가 굵은 **주의**: 5초 유지는 상세 GET 단건 재조회만 — ~3초 뒤 배경 재읽기 · 판 일괄 재읽기는 KOS 값으로 덮음 (service/reservations.py:756-763 · reception.py:73 · reservation_sync.py:301) |
| W-R3 | 고침 | event_log 는 KOS 호출이 실패할 때만 — KOS 설정 없음 · 응답 형식 502 는 행 없음 |
| W-R4 | 고침 | form `date` = 형식 검사 + 재읽을 날 · 정원 판정은 `start` 의 KST 날 사본 → 다르면 묵은 값 가능 |
| W-R5 | 고침 | 캐시 비움 = 1~4단계 중 실패(409 · 502)만 · 0단계 읽기 · not_receivable · room_task_missing · room_locked · room_busy · 400 · 404 는 안 비움 (reception.py:168-171) |
| W-R6 | 고침 | 공지: get-notices 읽기는 늘 먼저(실패 = event_log + 409/502) · 「쓰기 호출 없음(읽기만)」 · 재읽기에서 못 찾으면 `notice: null` |
| W-R7 | 고침 | 생성 검사 순서 = 유입 → 담당자 → 상담사 (service/reservations.py:787-803) |
| W-R8 | 고침 | `web_manual` = PUT identity(둘 다) + 사진 삭제 자동 unconfirmed · `device` = app_scan · app_manual 둘 다 |
| W-R9 a–e | 고침 | (a) `date.fromisoformat` 기준 — `20240101` 도 통과 · 검색 birth 는 받은 글자 그대로 KOS 로 (b) `desiredDischargeTime` = 「정수:정수」 꼴만 · 범위 검사 없음 (c) 「마지막 저장 이력 시각과 다르면」 (d) 방 없으면 `상담 대기` (e) `isNew` · `sedationRequired` 괄호 풀이 지우고 「KOS 값 그대로」 |
| W-C1 | 고침 | 시스템 줄 예시에서 「」 제거(초대 · 나가기 줄 둘 다) (service/chat.py:188-190,318) |
| W-C4 | 고침 | `since` = 최근 `limit`(≤50)개만 · `before` 와 같이 못 씀 · `hasMore=true` 면 처음 꼴 + `before` 로 다시 불러오기 |
| W-C5 | 고침 | 같은 방 재등장 = 앞 결과가 **성공**일 때만 재사용 · 실패면 다시 처리 (service/chat.py:536) |
| W-C6 | 고침 | FORM_400 에 「파일 아닌 칸 1MB 초과」 추가 (starlette formparsers.py:86-94) |
| W-C7 | 고침 | `ftyp` = 5~8번째 바이트(0부터 4~7) · 「가나다 순」 → 「코드포인트 순(라틴 < 한글 · 대문자 < 소문자)」 |
| **W-D1** | 고침(표에서 뺌) | `DELETE /api/devices/{token}` 400 invalid_request 제거 — 응답 표 = 200 · 401 |
| W-D2 | 고침 | 만료 반영 = pending · claim · close · 예약 상세 · 공개 문진만 · create 에선 기한 지난 pending 이 canceled 로 닫힘 |
| W-P1 | 고침 | q_canceled · q_submitted 는 직원 close · 여권 스캔 `displayRequestId` done 에서도 같은 코드 |
| W-P2 | 고침 | 고정 1분 아님 — 미끄러지는 60초 창 · 10 밑이면 바로 풀림 |
| W-P3 | 고침 | `qweb_denied` reason 나열 · not_found · rate 외엔 `requestId` 도 남김 |
| **W-P4** | 고침(표에서 뺌) | 공개 문진 GET 의 invalid_request 제거 — 400 표엔 서비스가 내는 `q_token_missing` 만 |
| W-P5 | 고침 | 정의 밖 키 400 은 최상위만 · `answers[]` · `agreements[]` 안 키는 검사 없이 KOS 로 |
| W-PH1 | 고침 | passport-scan 검사 순서를 실제대로 (photos.py:103-105 · passport_scan.py:56) |
| W-PH2 | 고침 | `reservationId` 존재 검사 없음 · KOS 일정 붙이기는 로컬 저장 + 예약 + kos_id 있을 때만 |
| W-PH3 | 고침 | `failed` 사진도 KOS 를 불러 409/502 가능 · 고객 행 없으면 KOS 단계 조용히 건너뜀 |
| W-PH4 | 고침 | done 은 `displayRequestId` 를 보낼 때만 · 종류 · 예약 검사 없이 닫음 (photos · display close 두 곳) |
| W-Q1 | 고침 | translsMap · 「답 값 없음」 단정 삭제 → 「`pages` 중 객체 항목만 그대로」 · 약관 응답이 비면 양식의 `agreements` 로 대체 명시 |
| W-A1 | 고침 | 수락 · 알림 읽음: 조건을 다 생략해도 본문 `{}` 는 필수 · 본문 없으면 400 |
| W-A2 | 고침 | 길이는 공백 지우기 전에 잼 · 공백만 = 빈 문자열 저장(기본 이름 안 붙고 기존 이름도 빈 값으로) · `installId` 공백만 = 생략 |
| W-A3 | 고침 | `KosFailure.error` 실제 문구 나열(HTTP · network · sign-in 실패 · 「KOS 값이 바뀌지 않음」 · BLOCKED · 예외 클래스 이름) |
| W-A4 | 고침 | 주기 발행 아님 — 마지막 발행 뒤 `KOS_POLL_SCHEDULE_SEC` 조용할 때만(1초마다 확인) 폴백 (container.py:91) |
| W-A5 | 고침 | 방 못 찾으면 글자 그대로 「방」 · N = 호출의 시술 수 전체(뒤에 안 바뀜) |
| W-A6 | 고침 | 401 사유에 「계정 삭제」 · 「서버에 `PROC_SESSION_SECRET` 없으면 늘 401」 추가 (service/auth.py:86,99) |

### 「조용히 통과」 2 — 오류 표 회귀 시험 추가
`tests/test_openapi_docs.py::test_error_tables_match_dependencies` — 모든 operation 에서 **양방향**으로 고정:
`require_login` 의존성 보유 ⇔ 401 표에 `unauthorized` · `require_real_board` 보유 ⇔ 403 표에 `fake_board`.
예외는 코드에 이름으로 박음: `GET /api/board/stream`(?token= 직접 검증 → 401) · `POST /api/public/questionnaire`(라우트 안 fake_board 검사).
실측: 401 unauthorized 표 66개(Bearer 65 + stream) · fake_board 표 28개 — 빈 집합으로 통과하는 시험이 아님을 확인.

### 수치
| | 1판 | 수정 1판 |
|---|---|---|
| `uv run pytest -q` | 543 passed | **544 passed** (+1 오류 표 시험) |
| `uv run ruff check .` | All checks passed | All checks passed |
| summary / description | 70 / 70 | 70 / 70 |
| property description | 683 / 683 | 683 / 683 |
| security(Bearer) | 65 | 65 |

### 구조 비교 (openapi-after.json 다시 덤프 · 1판과 같은 스크립트)
```
operations before=70 after=70
schemas before=168 after=169 · added(문서용)=['DuplicateCandidate', 'ErrorDetail', 'ErrorResponse']
removed: ['HTTPValidationError', 'ValidationError'] (FastAPI 기본 422 용)
NOTE ('GET', '/api/board/stream'): 200 content 문서 추가 ['text/event-stream']
NOTE ('GET', '/api/chat/photos/{photo_id}'): 200 content 문서 추가 ['image/jpeg']
NOTE ('GET', '/api/chat/videos/{video_id}'): 200 content 문서 추가 ['video/mp4']
NOTE ('GET', '/api/chat/videos/{video_id}/thumbnail'): 200 content 문서 추가 ['image/jpeg']
NOTE ('GET', '/api/id-photos/{photo_id}'): 200 content 문서 추가 ['image/jpeg']
NOTE ('POST', '/api/chat/photos'): requestBody 문서 추가(전엔 없음 · request.form() 수동 파싱) — ['multipart/form-data']
NOTE ('POST', '/api/chat/videos'): requestBody 문서 추가(전엔 없음 · request.form() 수동 파싱) — ['multipart/form-data']
NOTE ('POST', '/api/customers/{customer_id}/passport-scan'): requestBody 문서 추가(전엔 없음 · request.form() 수동 파싱) — ['multipart/form-data']
PROBLEMS: 0
```
AST 비교(함수 본문 · 인자 이름 · 필드 타입 주석): 차이 = 1판과 같은 `CreateCallRequest.target` 의 `Field(discriminator="kind")` + description 뿐(+ main.create_app 은 1판 변경 그대로) → 동작 불변.

### 새로 본 것 (고치지 않음)
- 기기 등록 이름에 공백만 보내면 **기존 이름이 빈 문자열로 덮인다**(service/devices.py:33) — W-A2 문구에 사실대로 적음 · 동작은 그대로.

## 수정 2판 — 재검수 N1 (2026-11-11)

- 고침: `app/api/reservations.py` 접수(`POST /api/reservations/{reservation_id}/reception`) 부작용 문구 — event_log `reception` 은
  「1 ~ 4단계 진행 중 실패하고 **이미 보낸 단계가 있으면** 끝 단계 null 로 1줄 · 첫 단계에서 실패하면 행 없음」.
  근거 확인: `service/reception.py:168-171`(실패 시 `_log_reception(..., None, done)`) · `:201-203`(`if not steps and end_step is None: return`).
- 같은 문구 복사본: grep(`끝 단계 null` · `단계 중 실패` · event_log `reception`) — 다른 곳 없음(상담 추가는 `consultation_add` 로 다른 문구).
- 검증: `uv run pytest -q tests/test_openapi_docs.py` 8 passed · `uv run ruff check .` All checks passed · `openapi-after.json` 다시 덤프 → 구조 비교 PROBLEMS 0.
- 동작 · 시험 · 다른 파일 무변경.
