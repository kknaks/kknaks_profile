# 리뷰 리포트 — api-swagger-docs / code (2026-11-11)

워크트리 `/Users/kknaks/orca/workspaces/cc-prototype/api-swagger-docs` · base `77173cf` · 미커밋 변경(diff 15 파일 + untracked 3). read-only 검수 — 리포 파일 수정 없음.

## 판정: **WARN** (FAIL 0 · WARN 34 · 동작 불변 PASS)

- **동작 불변 PASS** — 라우트 함수 본문 · 의존성 · 예외 처리기 · 미들웨어 · CORS · `response_model` · alias · 필드 타입/기본값 전부 HEAD 와 같다(AST 비교 · OpenAPI 구조 비교 둘 다 0 차이). `decorate` 는 `/api/openapi.json` 생성 때만 돈다.
- **설명 ↔ 코드 대조**: 70 operation 전수. 오류 코드 목록에 **빠진 코드 · 나지 않는 코드(실질) · 틀린 상태 · 틀린 역할 · 틀린 부수효과(KOS/SSE/푸시) 없음**. 남은 것은 문구가 코드보다 넓거나 좁은 곳(WARN). 외부 호출자가 실제로 걸릴 만한 것은 W-R2(생성 502 후 재시도 = 중복) · W-C3(`since` `+` 인코딩) · W-C2(지운 메시지 `deletedAt` 오독) · W-R1(5초 보장 오해) — **머지 전 문구 수정 권장**.
- 지어낸 설명: 단정형 창작 없음. 해석 성격의 짧은 주석 2곳(W-R9e)만.
- public 레포: 실명 · 연락처 · KOS id · 키 · 토큰 · 내부 호스트 없음(examples 자체가 0개 · 호스트는 브리프가 요구한 운영 주소뿐).

## 실행한 검증 (수치)

| 검증 | 결과 |
|---|---|
| `uv run pytest -q tests/test_openapi_docs.py` | **7 passed** |
| `create_app(settings).openapi()` 덤프 ↔ `openapi-after.json` | **완전 일치**(dict ==) |
| AST 비교(독스트링 · summary/description/responses/tags/openapi_extra · `Field()/Path()/Query()` 빈 래퍼 정규화) 10 라우터 + main + 스키마 4 | 함수 본문 차이 **0** · main 은 `FastAPI(...)` 인자 + `decorate(app)` 만 · schemas/actions 의 `discriminator="kind"` 유지 |
| OpenAPI before↔after 구조(operationId · parameters · requestBody · 200 JSON 스키마, `$ref` 해소 · 설명류 키 제거, `properties` 안 필드명은 보존) | 64 path · 70 op **차이 0** (새 multipart requestBody 3개 = before 없음 → 문서 추가) |
| 기계 대조: require_login op ↔ 401 표 · require_real_board op ↔ 403 fake_board 표 · 입력 있는 op ↔ 400 invalid_request | 불일치 0 (공개 문진 POST 의 fake_board 는 라우트 안 인라인 검사 `public_questionnaire.py:121` — 맞음) |
| `_get_api_route_for_openapi` 제거 모의 | 앱 부팅 OK · `/api/health` 200 · `/api/docs` 200 · `/api/openapi.json` **500**(조용히 틀리지 않음) |

## FAIL

없음.

## WARN — 지적 표

| # | 판정 | 파일:줄 | 설명이 말하는 것 | 코드가 하는 것 | 근거 |
|---|---|---|---|---|---|
| **W-R2** | WARN(우선) | `app/api/reservations.py:208-209` | 502 kos_unavailable 사유에 「KOS 응답에 일정 id 또는 새 고객 id 가 없음」 | 이 두 502 는 KOS `reserve` / create-visitor 가 **성공한 뒤** 응답 모양 검사에서 난다 → 호출자가 재시도하면 KOS 에 예약 · 고객이 중복 생김. 「멱등 아님」 옆에 「이 502 는 KOS 쓰기가 이미 됐을 수 있음」이 없다 | `service/reservations.py:837-842` · `:938-940` |
| **W-C3** | WARN(우선) | `app/api/chat.py:250-251` | `updatedAt` 을 그대로 `since` 로 | 값에 `+09:00` 이 있어 URL 인코딩(`%2B`) 안 하면 공백으로 바뀌어 `fromisoformat` 실패 → 400 invalid_request. 인코딩 필요를 안 적음 | `service/chat.py` since 파싱 · 쿼리 디코딩 |
| **W-C2** | WARN(우선) | `app/api/chat.py:255` | 「지운 메시지도 나온다(`deletedAt` · text · photo · video = null)」 — `deletedAt` 도 null 로 읽힘 | `deletedAt` 은 값이 있고 text · photo · video 만 null. 같은 파일 :367 은 바르게 적음 | `service/chat.py:107-120` |
| **W-R1** | WARN(우선) | `app/api/reservations.py:344` · `:409` | 접수 · 상담 추가 후 「5초 동안 KOS 의 이전 단계로 되돌리지 않음」 | 5초 유지는 상세 GET 의 단건 재조회만 지킨다. 접수 뒤 ~3초 배경 재읽기 · 판 일괄 재읽기는 KOS 값으로 덮어쓴다 | `service/reservations.py:756-763` · `reception.py:73,94-98` · `reservation_sync.py:297` |
| W-C4 | WARN | `app/api/chat.py:249` | `since` 로 새 · 수정 · 삭제를 채운다 | 최근 `limit`(≤50)건만 · `before` 와 같이 못 씀 → `hasMore=true` 면 더 옛 변경을 받을 길이 없다. 그때 할 일을 안 적음 | `repo.py:760-762` · `service/chat.py:356` |
| W-R3 | WARN | `app/api/reservations.py:44-46`(WRITE_COMMON) | 쓰기 실패마다 event_log 행 | KOS 설정 없음 · 응답 형식 502 는 `kos_write` try 밖이라 행이 안 남는다 | `service/reservations.py:837,841,1056` · `reception.py:71,183` |
| W-D2 | WARN | `app/api/display.py:27`(STATUS) | 만료는 띄우기 API 를 부를 때마다 먼저 반영 | `create()` · `targets()` 는 `_expire` 안 부름 — create 에선 기한 지난 pending 이 `expired` 가 아니라 `canceled` 로 닫힘 | `service/display.py:83-132` · `:114-116` |
| W-P1 | WARN | `app/api/public_questionnaire.py:48-50,58-59` | `410 q_canceled` = 같은 예약에 새 링크 · `409 q_submitted` = 이미 제출 | 직원이 `POST /api/display-requests/{id}/close` 로 canceled/done 닫아도 같은 코드 | `service/questionnaire.py:123-126` · `service/display.py:202-214` |
| W-P2 | WARN | `app/api/public_questionnaire.py:46` | 나쁜 토큰 10회/분이면 그 IP 를 「1분」 막음 | 슬라이딩 창 — 60초 창 안이 10 미만이 되는 순간 풀림 | `service/questionnaire.py:79-86,254` |
| W-P3 | WARN | `app/api/public_questionnaire.py:51` | `qweb_denied` 로그엔 이유만 | `not_found` 외엔 `requestId` 도 남김 | `service/questionnaire.py:279-280` |
| W-P4 | WARN | `app/api/public_questionnaire.py:78` | GET 공개 문진에 `400 invalid_request` | 입력이 `lang: str|None` · 선택 헤더 `str` 뿐 — 검증 실패 길 없음(나지 않는 코드) | `public_questionnaire.py` `load` 시그니처 |
| W-P5 | WARN | `app/api/public_questionnaire.py:98` | 정의 밖 키 → 400 | 최상위만. `answers[]` · `agreements[]` 항목은 `extra="allow"` 로 KOS 까지 넘김 | `schemas/actions.py` `_Loose` |
| W-D1 | WARN | `app/api/devices.py:42` | `DELETE /api/devices/{token}` 에 400 invalid_request | 입력이 path `str` 하나 — 검증 실패 길 없음(나지 않는 코드) | `devices.py:44` |
| W-PH1 | WARN | `app/api/photos.py:73` | passport-scan 검사 순서 = 기기 → Content-Length 413 → 사진 필수 | 실제 = Content-Length 413 → multipart 400 http_error → photo 형식 → fields → 정수 칸 → 기기 404 → 사진 크기 413 → 사진 필수 → 고객 404 → 날짜 400 | `photos.py:103-105` · `service/passport_scan.py:56` |
| W-PH2 | WARN | `app/api/photos.py:52-53` | `reservationId` 를 사진 행에 저장 · 그 예약 일정에 KOS 이미지 붙임 | id 검사 없음(FK 없음 → 없는 id 도 저장) · KOS 붙이기는 로컬 저장 + 예약 kos_id 있을 때만 | `repository/db.py:186` · `service/id_photo.py:78-80` |
| W-PH3 | WARN | `app/api/photos.py:170` | KOS 에 「올라간 적 있으면」 KOS 삭제 | `failed` 상태도 KOS get/delete 를 불러 409/502 가능 · 고객 행 없으면 KOS 단계 조용히 건너뜀 | `service/id_photo.py:156` |
| W-PH4 | WARN | `app/api/display.py:132-133` | 여권 스캔 저장 성공 = 요청 done | `displayRequestId` 를 보낼 때만 · 그 id 의 종류 · 예약 검사 없이 닫음 | `service/passport_scan.py:80` |
| W-Q1 | WARN | `app/schemas/actions.py:389-390,399` | `pages` 에 translsMap 포함 · 고객 답 값 없음 | KOS 내용에 대한 단정 — 서버는 dict 만 걸러 그대로 넘김(코드로 확인 불가 = 추정 서술) · `agreements` 는 빈 목록이면 `form.agreements` 로 대체(미기재) | `service/questionnaire.py:146-147` |
| W-R4 | WARN | `app/api/reservations.py:88-90` | 폼 `date` 는 형식 검사만 | `groupId`+`start` 일 때 재읽는 날 = `date`(기본 오늘), 슬롯 판정은 `start` 의 KST 날 — 둘이 다르면 `available` 이 묵은 값일 수 있음 | `service/reservations.py:395-397,409-410` |
| W-R5 | WARN | `app/api/reservations.py:346` | 접수 실패 때도 그 날짜 캐시를 비운다 | 단계 시퀀스 안 실패만. 0단계 읽기 · room_locked · room_busy · not_receivable · room_task_missing · 방 404 는 안 비움 | `reception.py:168-171` |
| W-R6 | WARN | `app/api/reservations.py:227` · `schemas/reservations.py:764` | 공지 표 「없음 · 빈 값 · 호출 없음」 | KOS get-notices 읽기는 늘 먼저 → 409/502 · event_log 가능(「쓰기 호출 없음」이 맞다) · `NoticeResponse.notice` 는 재읽기에서 못 찾으면 null 가능(미기재) | `service/reservations.py:977,996-1002` |
| W-R7 | WARN | `app/api/reservations.py:179` | 생성 검사 순서 상담사 → 담당자 | 코드는 유입 → 담당자 → 상담사(첫 400 문구만 달라짐) | `service/reservations.py:787-803` |
| W-R8 | WARN | `app/schemas/reservations.py:304,306` | `Identity.method` `web_manual` = 웹 확인 버튼 · `device` = 앱 스캔 | `web_manual` 은 PUT identity `unconfirmed` · 사진 삭제 자동 행도 · `device` 는 `app_manual` 에도 | `repo.py:563` · `id_photo.py:183` · `passport_scan.py:77-79` |
| W-R9 | WARN | `reservations.py` 여러 곳 | (a) 날짜 「`YYYY-MM-DD` 꼴」 (b) `desiredDischargeTime` 「HH:MM」 (c) 상세 「문진 제출본이 새로우면」 (d) 상담 호출 푸시 본문 (e) `isNew`「(신규 고객)」 · `sedationRequired`「(수면 마취 필요)」 | (a) `fromisoformat` 이 `20240101` 도 받음 — 검색은 그 값을 KOS 로 그대로 (b) `25:99` · `9:5` 도 통과 (c) 「마지막 저장본과 다르면」 (d) 방 없으면 `상담 대기` 만(미기재) (e) 이름 풀이 — 코드 근거 약함(be 리포트 §6 은 「그대로라고만 적음」이라 했으나 괄호 풀이가 붙어 있음) | `service/reservations.py:441-449,595,829` · `reservation_rules.py:84-86` · `push.py:144` |
| W-A1 | WARN | `app/api/actions.py:107` · `schemas/actions.py:77-81` · `:186` | 원장 수락 「`doctorId` 생략」 · 알림 읽음 「셋 다 없으면」 | 본문 자체는 필수(`{}` 라도) — 본문 없이 보내면 400 invalid_request. OpenAPI `requestBody.required: true` 는 맞음, 산문이 오해 소지 | `actions.py:132` · `main.py:117-121` |
| W-A2 | WARN | `app/schemas/actions.py:135-137` | 기기 이름 1~40자 · 앞뒤 공백 지움 · 없으면 iPhone/iPad | 공백만 `"   "` 은 길이 검사 통과 → 빈 문자열로 저장(기본값 안 붙음) · `installId` 공백만 = 생략 취급(미기재) | `service/devices.py:29-34` · `repo.py:346` |
| W-A3 | WARN | `app/schemas/board.py:153` | `KosFailure.error` = 「상태 · 이름」 | 한국어 문구(「KOS 값이 바뀌지 않음」 · sign-in 실패 · BLOCKED)도 들어감 | `kos/ops.py:60,105,152` |
| W-A4 | WARN | `app/api/board.py:36` | `KOS_POLL_SCHEDULE_SEC` 마다 「그와 상관없이」 board 발행 | 마지막 발행 뒤 그만큼 조용했을 때만(폴백) | `container.py:91` |
| W-A5 | WARN | `app/schemas/actions.py:170-172` | 원장 호출 알림 본문 `<방> · 시술 N건` | 방 못 찾으면 글자 그대로 `방` · N = 호출의 전체 시술 수 | `service/push.py` `message()` |
| W-A6 | WARN | `app/api/docs.py:51-52`(UNAUTHORIZED) | 401 사유 나열 | 서버 `PROC_SESSION_SECRET` 없음 · 계정 행 삭제도 401(사소) | `service/auth.py:86,99` |
| W-C1 | WARN | `app/api/chat.py:135,161,186` | 시스템 줄 `「<나>님이 …초대했습니다」` | 저장 text 엔 「」 없음 — 따옴표를 값의 일부로 오해 가능 | `service/chat.py:190,318` |
| W-C5 | WARN | `app/api/chat.py:396-397` · `schemas/chat.py:281` | 전달 대상에 같은 방이 또 오면 앞 결과 그대로 | 앞 결과가 **성공**일 때만 재사용 — 실패면 다시 처리 | `service/chat.py:536` |
| W-C6 | WARN | `app/api/chat.py:62`(FORM_400) | multipart 400 http_error 사유 | 파일 아닌 칸 1MB 초과(Starlette `max_part_size`)도 400 http_error — 미기재 | `starlette/formparsers.py:86-94` |
| W-C7 | WARN | `app/api/chat.py:527` · `:77` · `schemas/chat.py:66,131` | 「4~8번째 바이트가 ftyp」 · 「가나다 순」 | `head[4:8]` = 5~8번째 바이트 · 정렬은 코드포인트 순(라틴 < 한글 · 대문자 < 소문자) | `service/chat.py:66,135,205,709` |

## 「조용히 통과하는 자리」

1. **커버리지 시험이 「비어 있지 않음」만 본다** — `tests/test_openapi_docs.py:43-73`. 필드명 반복 · 무의미 채움을 막지 못한다. 실측: 683 필드 중 8자 미만 64개 — 대부분 `$ref` 객체 필드(`customer`「고객」)나 `ok`「늘 true」라 무의미 채움은 아님. 단 `Personal.name`「이름」 · `NewCustomer.email`「이메일」 같은 이름 되풀이가 섞여 있다(WARN 아님 · 참고). 의미 정확성은 시험으로 못 고정 — 이번 리뷰가 그 자리를 메웠다.
2. **오류 표 존재는 시험이 안 본다** — 시험은 401/403/400 표 유무를 검사하지 않는다. 이번 리뷰에서 기계 대조로 0 불일치 확인(위 표). 회귀 방지엔 시험 추가가 낫다(제안).
3. **422 제거 — 맞다(PASS)**. `RequestValidationError` → 400 `invalid_request`(`main.py:117-121`) · `StarletteHTTPException` → `not_found`/`http_error`(`main.py:123-125`) · 앱 안에 422 를 직접 내는 곳 없음(grep 0). `ResponseValidationError` 는 500. `HTTPValidationError`/`ValidationError` 스키마 제거도 다른 참조가 없을 때만(`openapi_docs.py:166-170`).
4. **비공개 FastAPI 함수** — `openapi_docs.py:132-140`. 호출은 `openapi()` 안에서 늦게 일어나 **부팅을 막지 않는다**(모의로 확인). 사라지면 `/api/openapi.json` 500(소리 남) · 의미가 바뀌어 None 만 돌려주면 security 0 이 되지만 `test_bearer_security_matches_require_login` 이 `secured == n_ops - 5` 로 잡는다. 이미지 빌드는 `uv sync --frozen`(`Dockerfile`) → fastapi 0.156.4 고정이라 운영에서 갑자기 바뀌지 않는다. PASS(주의: `pyproject` 는 `fastapi>=0.115` — lock 갱신 시 시험이 지켜 줌).

## 고객(협업자)이 실물에서 만날 자리

- 예약 생성 502 후 재시도 → KOS 중복 예약/고객(W-R2).
- 채팅 `since` 에 `updatedAt` 을 그대로 붙이면 400(W-C3).
- 지운 메시지를 `deletedAt == null` 로 거르면 다 놓침(W-C2).
- 접수 직후 판/배경 재읽기에서 단계가 잠깐 되돌아 보일 수 있음(W-R1).
- 운영 `/api/docs` 실제 열림은 미확인(be 리포트 「운영 확인」 pending — 배포 뒤 코디 확인).

## 본 범위

- **operation 설명 · 오류 표: 70/70 전수** — 라우터별로 service · domain · repository · kos 오류 매핑까지 따라감(actions 10 · board 3 · auth 2 · devices 2 · notifications 4 · health 1 · reservations 17 · chat 21 · display 4 · public 2 · photos 4).
- **필드 설명**: 응답 모델 · 요청 모델 **전부**의 enum · nullable · 시간 형식 · 정렬 · 단위 칸 전수. 그 밖 서술형 칸은 라우터별 대조 중 확인한 범위(대부분) — 미세한 산문 전수는 아님.
- multipart requestBody 3개 칸 이름 · 필수 · 타입 ↔ `request.form()` 읽는 칸: 전수 일치.
- app description(공통 규칙) 전 항목 · 통역 WS 프로토콜: 전수.
- public 레포 grep: 추가된 모든 줄(diff `+` + 신규 2 파일) · OpenAPI 의 example/examples(0개).

## 확인한 것 (PASS 근거)

- **동작 불변**: 위 AST · 구조 비교 0 차이. `decorate` 는 `app.openapi` 만 감싸 처음 생성 때 dict 를 고침(`openapi_docs.py:173-183`) — 라우트 · 의존성 · 미들웨어 · 처리기 무변경, `HTTPBearer`/`Security` 의존성 미추가 → 401 모양 그대로(`test_security_is_docs_only`). CORS 블록 무변경(`main.py:97-102`). 문서 경로 `/api/docs` · `/api/redoc` · `/api/openapi.json` 인증 없음 · 환경 분기 없음.
- **security 표시 65 = require_login 의존성 보유 op 65**(login · health · stream · 공개 문진 2 제외) — 시험 + 재확인.
- **app description 공통 규칙**(`openapi_docs.py:20-104`) 전부 코드와 일치: 로그인 본문 · `token`/`expiresAt` · `PROC_SESSION_HOURS` 기본 12(`config.py:60`) · 요청마다 DB 재검사(비활성 · 역할 · staffId 변경 → 401, `service/auth.py:83-103`) · 5회 실패 60초 429 메모리(`auth.py:36-37,59-61`) · 검증 오류 400 `<loc>: <msg>` 첫 하나 · 404 not_found · 405 http_error · `kos_rejected` 409(4xx 중 401 제외) / `kos_unavailable` 502(`kos_errors.py:35-42`) · 시각 KST `+09:00` 초 / 채팅 밀리초(`clock.py:24-36`) · 공개 문진 no-store + no-referrer(오류 포함, `main.py:104-111`) · 다운로드 `no-store` · `inline` · Bearer 헤더만 · SSE `?token=` · 통역 WS(언어 8개 · 10초 start · PCM 16k/24k · pause/resume/stop 3초 · error 코드 3개 · 알 수 없는 프레임만 연결 유지 · Origin 규칙 · 1008 · 역할 무검사 — `api/interpret.py` · `service/interpret/session.py`).
- **ErrorDetail**: `step` · `candidate` 만 추가 키 — 코드의 extra 사용처와 일치(`fields=` 를 오류에 싣는 곳 없음).
- **be 리포트 §7 버그가 문서에 사실대로**: display-requests 생성 fake_board 없음 · 남의 기기 허용 · claim/close 소유 무검사 · anesthesia/end 귀가 대기 허용 · notifications/read 무조건 = 안 읽은 전부 · KOS env 없으면 쌓기만 · multipart 한도 400 http_error · 채팅 clientId 계정 단위 · `not_movable` 제외(DRAG_MAINS 가 `state_of` 7값 전부 → 실제 안 남, `reservation_rules.py:167` · `service/reservations.py:908`) · 공개 문진 오류 `requestId` 제거(`questionnaire.py:268`) — 모두 설명이 코드대로.
- **「확인 못 한 것」 칸**(gender · nationality · language · currency · PrevProcedure.status · connectedChannel · 검색 매칭 · width/height 단위) — 「KOS 값 그대로」 · 「앱이 준 값 · 검사 없음」 중립 서술 확인. 예외는 W-R9e · W-Q1.
- **기능 독립 · allowed_paths**: 변경 전부 `procedure/back/` · 새 import 는 `app.*` · `fastapi.*` · `pydantic` 만. interpret.py · deps.py · service · domain · repository 무수정.

## 참고(기존 부채 · 범위 밖)

- be 리포트 §7 의 버그 목록 — 이번 범위 밖(동작 변경 금지). 재지적하지 않음.
- 스키마 이름 충돌(`app__schemas__board__Room` 등)은 77173cf 부터. 문서용 모델 `ErrorDetail` 로 회피 — 적절.

---

## 재검수 (수정 1판) — 2026-11-11

### 종합 판정: **PASS** (W 34/34 OK · 새 지적 1건 = 경미 WARN · 머지 비차단)

- 1판 WARN 34건 모두 코드대로 고쳐졌다. 우선 4건(W-R2 · W-C3 · W-C2 · W-R1)은 해당 엔드포인트 description 맨 위에 굵은 **주의** 단락으로 올라가, 외부 호출자가 무엇을 하면 안 되는지 · 대신 무엇을 하는지(조회로 먼저 확인 · `%2B` 인코딩 예시 · `deletedAt` 은 값 있음 · 5초는 상세 GET 만)까지 한 번에 읽힌다.
- 수정이 새로 만든 틀린 설명: 1건(N1 · 경미). 그 밖 새 사실 서술은 코드로 다시 확인해 맞음.
- 동작 불변 재확인 PASS · 새 시험은 빈 집합 통과 아님.

### 실행한 검증

| 검증 | 결과 |
|---|---|
| `uv run pytest -q tests/test_openapi_docs.py` | **8 passed** (+1 `test_error_tables_match_dependencies`) |
| 지금 `app.openapi()` 덤프 ↔ 새 `openapi-after.json` | 완전 일치 |
| 1판 덤프(리뷰 1판 때 스크래치 보관) ↔ 지금 덤프 — description · summary 밖 차이 | **1곳뿐**: `DELETE /api/devices/{token}` 의 `400` 응답 제거(W-D1 의도) · 그 밖 구조 · 파라미터 · 본문 · 스키마 무변경 |
| 바뀐 설명 전수 | 142 위치(같은 문구 반복 포함 — 401 공통 문구 · 쓰기 공통 단락 · 만료 단락 · 공개 문진 공통 단락) **전부 읽음** |
| AST 비교(1판과 같은 스크립트) | 파일별 차이 줄 수 1판과 동일(actions 38 · chat 91 · reservations 43 · main 5 …) — 함수 본문 · 의존성 · 처리기 · `response_model` · alias 무변경 |
| 새 시험 실측 | 70 op 순회 · require_login 65 · require_real_board 27 · 401 표 66(+stream) · fake_board 표 28 — 양방향 대조가 실제로 돈다 |

### W 번호별 확인

| W | 확인 | 메모(코드 근거) |
|---|---|---|
| **W-R2** | OK | `app/api/reservations.py:183-185` 주의 + `:201` 멱등 줄 + 502 표. 「이미 된 뒤 · 재시도=중복 · 먼저 조회」 — `service/reservations.py:837-842,938-940` 과 맞음 |
| **W-C3** | OK | `app/api/chat.py:247-248` 주의 + 인코딩 예시(`%3A`/`%2B` 정확) · `since` 파라미터 · 400 표 세 곳 |
| **W-C2** | OK | `app/api/chat.py:250-251` 주의 + 목록 줄 「`deletedAt` = 지운 시각」 — `service/chat.py:107-120` |
| **W-R1** | OK | 접수 `:342-344` · 상담 추가 `:424-426` 주의 + 부작용 줄 「상세 GET 단건만 5초 · 배경/일괄 재읽기는 덮음」 — `service/reservations.py:756-763` · `reception.py:73,94-98` |
| W-R3 | OK | 쓰기 공통 단락 9곳 — 설정 없음 · 응답 모양 502 는 event_log 없음 |
| W-R4 | OK | form `date` = 형식 + 재읽기 날 · 정원은 `start` KST 날 사본 — `service/reservations.py:395-397,409-410` |
| W-R5 | OK | 캐시 비움 = 1~4단계 409·502 만 — `reception.py:168-171` (같은 줄의 event_log 문구는 N1) |
| W-R6 | OK | get-notices 읽기 선행 · 「쓰기 호출 없음(읽기만)」 · `notice: null` 추가 사유 — `service/reservations.py:977,996-1002` |
| W-R7 | OK | 유입 → 담당자 → 상담사 (본문 · 400 표 둘 다) |
| W-R8 | OK | `web_manual` · `device` 범위 — `repo.py:563` · `id_photo.py:183` · `passport_scan.py:77-79` |
| W-R9 a | OK | `date.fromisoformat` 기준 · 검색 birth 는 받은 글자 그대로(`service/reservations.py:445,452`) · 생성/개인정보는 정규화(`:919` · `_kos_date :1200-1206`). 「KOS 에는 `YYYY-MM-DD` 로」는 실제로 `… 00:00:00.000Z` 꼬리가 붙지만(생년월일) 호출자에 영향 없는 KOS 쪽 세부 — OK |
| W-R9 b | OK | 「정수:정수 · 범위 검사 없음」 · `00:00 + 시×60+분` — `reservation_rules.py:82-90` |
| W-R9 c | OK | 「마지막 저장 이력 시각과 다르면 · ccc 웹 제출본을 보일 땐 추가 안 함」 — `service/reservations.py:637-640`(`not use_own` 조건) |
| W-R9 d | OK | 상담 호출 푸시 본문 방 없음 = 「상담 대기」 |
| W-R9 e | OK | `isNew` 3곳 · `sedationRequired` 괄호 풀이 삭제 → 「KOS 값 그대로」 |
| W-C1 | OK | 낫표 제거 · 「낫표 없음 · 이름 뒤 빈칸」 명시 — `service/chat.py:190,318` |
| W-C4 | OK | `since` = 최근 limit 개만 · before 불가 · `hasMore` 땐 처음 꼴 + before 로 다시 |
| W-C5 | OK | 앞 대상 성공일 때만 재사용 (본문 · `ForwardOk.message` 둘 다) — `service/chat.py:536` |
| W-C6 | OK | 사진 · 동영상 400 표에 「파일 아닌 칸 1MB 초과」 |
| W-C7 | OK | `ftyp` 5~8번째(0부터 4~7) · 「코드포인트 순(라틴 < 한글 · 대문자 < 소문자)」 4곳 |
| W-D1 | OK | 400 제거 → 응답 표 200 · 401 |
| W-D2 | OK | 만료 반영 자리 나열 · create 는 기한 지난 pending 도 canceled — `service/display.py:102-132,146-221`. (`여권 스캔 저장의 displayRequestId 닫기`(`finish → _close → _expire`)도 만료를 반영하지만 목록에 없음 — 참고, 호출자 영향 없음) |
| W-P1 | OK | q_canceled · q_submitted 원인에 직원 close · 스캔 `displayRequestId` (본문 · 409/410 표) — `service/display.py:197-214` |
| W-P2 | OK | 미끄러지는 60초 창 · 「막힌 요청은 횟수에 더하지 않는다」 — `_gate` 가 `_target_or_deny` 앞에서 막아 `rate.add(("bad",ip))` 를 안 탐 (`service/questionnaire.py:79-89,253-266`) |
| W-P3 | OK | reason 6종 · not_found · rate 외 `requestId` — `_deny` `:270-282` (rate 는 `None` 을 넘김) |
| W-P4 | OK | GET 400 표 = `q_token_missing` 만 — `service/questionnaire.py:114` |
| W-P5 | OK | 최상위만 400 · 항목 안 키는 KOS 로 |
| W-PH1 | OK | 검사 순서 전체가 코드 순서와 같음 — `photos.py:103-112` → `parse_fields` → `passport_scan.save` `:56-66` |
| W-PH2 | OK | `reservationId` 검사 없음 · KOS 일정 붙이기 조건 |
| W-PH3 | OK | `failed` 도 KOS 호출 · 고객 행 없으면 `kos`=skipped |
| W-PH4 | OK | passport-scan · display close 두 곳 — `service/passport_scan.py:80` · `display.finish` |
| W-Q1 | OK | `pages` 객체 항목만 그대로 · 약관 `data`→`agreements` 키→양식 `agreements` 대체 — `service/questionnaire.py:51-55,146-147` |
| W-A1 | OK | 수락 · 알림 읽음 「본문 `{}` 필수」 (모델 docstring · 필드 · 엔드포인트 · 400 표) |
| W-A2 | OK | 길이는 공백 지우기 전 · 공백만 = 빈 문자열 저장 · 기존 이름도 덮임 — `service/devices.py:29-35` · `repo.py:346`(`""` 는 None 아님 → extra 에 들어감). `installId` 공백만 = 생략 |
| W-A3 | OK | `HTTP <상태> <이름>` · `network <예외>` · BLOCKED 문구 — `kos/client.py:62,96` · `kos/ops.py:29,105,152` |
| W-A4 | OK | 폴백 · 1초마다 확인 — `container.py:84-93` (`check_sec=1.0`) |
| W-A5 | OK | 「방」 글자 · N = 호출 시술 수 전체 |
| W-A6 | OK | 401 공통 문구에 계정 삭제 · `PROC_SESSION_SECRET` 없음 — `service/auth.py:86,99` |

### 새 지적

| # | 판정 | 파일:줄 | 설명이 말하는 것 | 코드가 하는 것 | 근거 |
|---|---|---|---|---|---|
| N1 | WARN(경미) | `app/api/reservations.py:360` | event_log `reception` 은 「1 ~ 4단계 중 실패하면 끝 단계 null 로 1줄」 | 보낸 단계가 하나도 없으면(첫 단계 `recept` 에서 실패) 행을 남기지 않는다 — 1판 문구 「실패해도 보낸 단계가 있으면」이 맞았다. 「1 ~ 4단계 진행 중 실패하고 이미 보낸 단계가 있으면」으로 | `service/reception.py:168-171`(실패 시 `_log_reception(..., None, done)`) · `:201-203`(`if not steps and end_step is None: return`) |

참고(지적 아님): 새 시험 `test_error_tables_match_dependencies` 자체엔 「순회한 op 수」 단언이 없다 — 라우트를 하나도 못 펴면 `bad == []` 로 통과한다. 다만 같은 파일 `test_bearer_security_matches_require_login` 이 `routes 메서드 수 == operation 수` 를 단언해 그 경우를 잡으므로 실질 위험 없음.

### 본 범위
- 수정 1판에서 바뀐 description · summary · 응답 표 **전부**(1판 덤프와 지금 덤프의 차이 142 위치) + 구조 차이 전수.
- 새로 단정한 사실(위 표 메모의 코드 줄)은 하나씩 열어 확인. 1판 PASS 자리 · §7 버그 목록은 다시 보지 않음(지시대로).
