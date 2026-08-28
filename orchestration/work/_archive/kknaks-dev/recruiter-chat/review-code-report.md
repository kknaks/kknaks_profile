# reviewer_code — 채용담당자 채팅 BE+FE 검수 (WORK-023 · WORK-024)

- 검수자: `@kknaks-reviewer` (read-only — 코드 미수정 · 테스트 미실행)
- 검수 대상: 워크트리 `recruiter-chat` 의 **미커밋 변경 전부**
  (tracked 27 파일 + untracked 53 파일)
- 기준 SSOT: SPEC-017 v0.0.4 · WORK-023 · WORK-024 · DEC-027(D1~D6)
- 작성: 2026-08-28

---

## 총평 — **WARN** (머지 가능, 착지 전 확인 2건)

FAIL 없음. 결정(DEC-027)의 골격 — 전용 큐 · MCP 하나로 좁힌 표면 · `chat_exposed`
옵트인 · 이벤트 폴딩 — 이 **구조로** 서 있고, 지시가 아니라 코드가 경계를 갖는다.
allowed_paths 위반 0건, 기존 파이프라인(`service/ai_service.py` · `worker` compose
서비스 · `queue=default`) 변경 0줄. 테스트 105/19 는 실재한다(수식으로 검증 — §4).

착지 전 결정이 필요한 것 둘:

1. **세션 쿠키가 실제로는 sliding 이 아니다** — spec §4 · S-5 3항 미충족. (W1)
2. **동시 요청 경합에서 409 가 500 으로 샌다** — Case Matrix 의 `CONVERSATION_BUSY`
   경로가 한 갈래 새어 있다. (W2)

나머지 8건은 low/info 다.

---

## 1. 축별 판정

| # | 축 | 판정 | 근거 |
|---|---|---|---|
| 1 | allowed_paths | **PASS** | 변경 전부 `app/back/`·`app/mcp/`·`app/front/` 안. `para/`·`orchestration/`·`resume/`·`agents.md` 오염 0 |
| 2 | 기존 파이프라인 무변경 | **PASS** | `service/ai_service.py` diff 없음. compose 의 `worker`·`redis`·`back` 블록 무변경(추가만) |
| 3 | spec 계약 | **WARN** | API 4+1·에러 `{"detail":"<CODE>"}`·합성 slug 404 동일성·tool 11종·steps/sources shape·폴링 계약 전부 일치. **쿠키 sliding(W1)·409 경합(W2)** 이 어긋난다 |
| 4 | 경계(보안) | **PASS**(주의 1) | shell/web_search/apps off + `sandbox=read-only` 실재 · 매 호출 `chat_exposed` 판정 · 남의 세션 404 동일. 토큰 로그 마스킹은 **죽은 코드**(W3) |
| 5 | 계층 규약 | **PASS** | router→service→repository 준수, ORM 이 repository 를 넘지 않음, 아래층 HTTP 무지(`core/exceptions` 만 던짐) |
| 6 | 소비자 멱등 | **PASS**(주의 1) | `tool_use_id` upsert · 재생 초기화 · 완료 메시지 재수신 무시 · timeout/실패 마감 경로 전부 있음. 재생+스트림 소멸 조합에서 부분 텍스트가 날아간다(W10) |
| 7 | FE | **PASS** | 폴링 `pending` 동안만·`done/failed` 중단·cleanup 확실 · 컴포저 잠금 · mock 스위치 1곳 · 토큰 밖 색 사실상 0(W7 1건) |
| 8 | 테스트 실재 | **PASS** | BE 105 · MCP 19 가 파일·케이스로 실재. 핵심 시나리오(쿠키 발급 시점·409·404 동일성·멱등) 전부 커버 |

---

## 2. 축별 근거 (통과 사유)

### 축 1 — allowed_paths

`git status` 기준 미커밋 변경 80건 전부가 `app/` 아래다. `git diff origin/main` 에
`para/`·`resume/`·`.agents/` 가 보이는 것은 **브랜치가 main 보다 1커밋 뒤라서**
생긴 역방향 표시일 뿐, 이 작업의 산출물이 아니다(W8 참조).

### 축 2 — 기존 파이프라인 무변경

- `app/back/service/ai_service.py` — 변경 없음. `submission.py:6-10` 이 그 이유를
  명시적으로 적어 두었다(익명 입력에 `danger-full-access` + `/ledger` 를 재사용할 수 없다).
- `docker-compose.yml` — `worker` 서비스 블록에 손대지 않고 `mcp` · `chat-worker`
  **두 서비스를 추가**만 했다. 볼륨도 `chat-codex-sessions` 신규(`codex-sessions` 무변경).
- `chat-worker` 에 **`/ledger` 마운트가 없다**(`docker-compose.yml` 추가분) — DEC-027
  Context ② 가 지목한 사고 축이 구조적으로 닫혔다.
- `career_repo.py:27` · `problem_repo.py:27` · `project_repo.py:29` 는 `chat_exposed` 를
  **DTO 로 흘려보내기만** 하고 조회 필터에 섞지 않는다 — 공개·어드민 표면 계약 무변경.

### 축 3 — spec 계약 (일치한 부분)

| 계약 | 구현 | 위치 |
|---|---|---|
| API 4+1 경로 | 전부 일치 | `api/chat_router.py:71,85,109,123,145` |
| 목록 봉투 `{conversations:[…]}` | 일치 | `schemas/chat.py:95-98` |
| `POST` 201 + `{conversation, messages}` | 일치 | `chat_router.py:85-106` |
| 에러 `{"detail":"<CODE>"}` | 일치 | `core/exceptions.py:40-43` + `schemas/chat.py:24-27` |
| 422 코드 구분(EMPTY/TOO_LONG) | pydantic 이 아니라 서비스가 판정 | `service/chat/chat_service.py:47-54` |
| 쿠키 httpOnly·Lax·Secure·30일 | 속성 일치 (sliding 만 W1) | `chat_router.py:55-68` · `config.py` chat_cookie_* |
| 쿠키 값 해시 저장 | sha256, 원문 미저장 | `service/chat/session_service.py:30-32` |
| 발급 시점 = 채팅 첫 사용 | `resolve` 는 만들지 않음 | `session_service.py:44-59` |
| 합성 slug 404 동일성 | 파싱 실패·미존재·미노출·접두사 불일치 전부 `NOT_FOUND` | `service/chat/tool_service.py:98-109` |
| tool 11종 이름 | allowlist ≡ spec §4 표 | `service/chat/submission.py:61-73` · `mcp/app/server.py` |
| `steps` 네 필드만 노출 | `toolUseId`·`status` 제거 | `schemas/chat.py:145-155` |
| `sources` = 실제 읽은 것 | 문서 계열 tool_result 의 `structured.item` 에서만 | `service/chat/consumer.py:81,176-203` |
| `source.url` nullable · career/problem → `/career` | 일치 | `core/chat_slugs.py:40-47` |
| 2초 폴링 · done/failed 중단 | 일치 | `lib/chat-types.ts:80` · `lib/chat.ts:148-166` |
| 모델 `gpt-5.6-terra` · `queue=chat` · timeout 180 | 일치 | `config.py` chat_model/chat_queue/chat_timeout_sec |

### 축 4 — 경계(보안)

- **손을 MCP 하나로**: `submission.py:112-116` 이 `features.shell_tool=false` ·
  `web_search="disabled"` · `features.apps=false` 를, `submission.py:53,166` 이
  `sandbox="read-only"` 를 신규·resume **공통**으로 싣는다. 툴별
  `approval_mode="approve"` 는 allowlist 전 항목에 개별로 걸린다(`:108-111`) —
  서버 기본이 아니라 툴별이라 tool 이 늘어도 자동으로 열리지 않는다.
- **turn 토큰**: 해시만 저장(`turn_token.py:55-68`), 마감 시 해시 NULL 이 폐기
  (`consumer.py:305-318`), 검증은 만료까지 본다(`chat_repo.py:195-211`).
  MCP 는 **헤더 없음만** 막고 유효성은 back 이 본다(`mcp/app/server.py:215-242`) —
  게이트가 두 곳에 살지 않는다.
- **매 호출 노출 판정**: `chat_tool_repo.py:172-178,206-210,242-248` 의 `_*_stmt()` 가
  쿼리마다 `chat_exposed.is_(True)` 를 건다. 캐시·export 없음 → 어드민 토글 즉시 반영.
  `test_chat_tool_api.py:179` 가 career/project/problem 3종 전부 확인.
- **경로 이탈 차단**: `core/chat_detail.py:30-46` 이 `resolve()` 로 심링크·`..` 을 편 뒤
  유형별 허용 루트와 비교한다. `para/projects/company/` 는 루트에서 빠져 있다.
- **남의 세션 404**: `chat_service.py:73-80` 한 곳에서만 소유권을 판정하고 「없음」과
  구분하지 않는다.
- **어드민 표면 보호**: `chat_router.py:44-48` 이 `require_admin` 을 라우터 레벨로 건다.
- 주의 1건 = W3(로그 마스킹 죽은 코드).

### 축 5 — 계층 규약

- router 는 서비스만 부른다. ORM 객체는 `repository/chat_repo.py`·`chat_tool_repo.py`
  밖으로 안 나간다 — `get_project`/`get_note` 는 ORM 대신 `(dto, detail_path)` 튜플을
  돌려주고 파일 읽기는 service 가 한다(`chat_tool_repo.py:228-239`).
- 아래층은 HTTP 를 모른다: 서비스는 `core.exceptions` 만 던지고, 쿠키 속성은
  라우터가 소유한다(`session_service.py:61-75` 가 「새 토큰」만 돌려준다).
- 트랜잭션 경계: 제출은 요청 커밋 뒤 `BackgroundTasks` 로 밀린다(`chat_router.py:161-165`
  · `runtime.py:121-157`) — 워커가 안 보이는 row 를 찾는 사고가 구조적으로 없다.

### 축 6 — 소비자 멱등

| 요구 | 구현 | 테스트 |
|---|---|---|
| 재생 시 text 초기화 | `consumer.py:226-231` | `test_chat_consumer.py:77` |
| `tool_use_id` 멱등 upsert | `consumer.py:249-271` | `:114` |
| 중복 tool_result 가 첫 duration 유지 | `consumer.py:333-343` | `:151` |
| 재생에서는 duration 미기록 | `consumer.py:338` | `:167` |
| 이미 끝난 메시지의 완료 이벤트 무시 | `consumer.py:399-402,447-449` | `:365` |
| 소비자 1개 보장 | `_running` 집합 `consumer.py:369-372` | — |
| timeout 마감(`AI_TIMEOUT`) | `consumer.py:380-382` · `_close_from_task:459` | `:346` |
| 실패 마감(`AI_FAILED`) | `consumer.py:383-385` · `runtime.py:169-181` | `:354`, `test_chat_submission.py:287` |
| 기동 스윕 2단 복구 | `consumer.py:479-498` | `:383`, `:398` |
| idle 상한을 바깥에서 | `asyncio.wait_for` `consumer.py:375-379` | — |

### 축 7 — FE

- 폴링: `active=pending` 일 때만 인터벌을 걸고, `done/failed` 로 바뀌면 `pending` 이
  false 가 되어 effect cleanup 이 `clearInterval` + `cancelled=true`
  (`lib/chat.ts:148-165`). 대화 전환·언마운트에서도 같은 cleanup 이 돈다.
- 컴포저 잠금: `chat-view.tsx:274-279` — `disabled={pending}` +
  placeholder 「답변을 기다리는 중…」(spec U-6 문구 그대로). 잠금이 새더라도 409 를
  받으면 상태를 다시 읽는다(`:87-97`).
- mock 스위치: `lib/chat.ts:34,108` 한 곳. 화면 코드는 `chatApi` 만 본다.
- 색: `globals.css` 추가분 514줄에 raw hex/rgb/hsl **0건**(전부 `var(--*)`).
  신규 커스텀 프로퍼티는 `--nav-h: 61px` 하나(색 아님). 예외 1건은 W7.
- spec 문구 일치: 히어로 헤더/서브/placeholder/하단 문구(`chat-intro.tsx:23-40`),
  실패 문구·`다시 시도`(`chat-thread.tsx:63-68`), tool 박스 헤더·뱃지
  (`tool-steps.tsx:33-38`), 사이드바 4요소(`conversation-sidebar.tsx`).
- 네비: `00 Ask` 가 첫 항목이고 번호는 `0{idx}` 로 재계산돼 기존 01~06 이 유지된다
  (`topnav.tsx` diff). `/chat` 활성 시에만 액센트 색.
- `scroll ↓` 앵커 `#about` 은 `landing-preview.tsx:125` 에 실재한다.

### 축 8 — 테스트 실재

| 파일 | `def test_` | parametrize 확장 | 계 |
|---|---|---|---|
| `tests/test_chat_api.py` | 14 | +2 | 16 |
| `tests/test_chat_tool_api.py` | 20 | +2+2+2 | 26 |
| `tests/test_chat_submission.py` | 27 | +2 | 29 |
| `tests/test_chat_consumer.py` | 27 | — | 27 |
| `tests/test_chat_detail_guard.py` | 7 | — | 7 |
| **BE 합계** | **95** | **+10** | **105** ✓ |
| `app/mcp/tests/test_server.py` | 17 | +2 | **19** ✓ |

핵심 시나리오 커버 확인:

- 쿠키 발급 시점 — `test_list_without_cookie_creates_no_session:23`(세션 row 0 검증) ·
  `test_create_conversation_issues_cookie:33` · `test_second_request_reuses_session:55`
- 409 — `test_message_while_pending_is_409:120` · DB 방어선 `:154`
- 404 동일성 — `test_other_session_conversation_is_404:81` ·
  `test_unknown_conversation_is_404:94` · `test_bad_career_slug_is_always_404:254`
  (파싱 실패 / 없는 id / 접두사 불일치 3케이스)
- 멱등 — 위 축 6 표
- 토큰 게이트 — 무토큰 401 · 폐기 401 · 만료 401(`test_chat_tool_api.py:114,128,140`)
- 경로 이탈 — `test_chat_detail_guard.py` 7종 + `test_project_body_is_absent_outside_public_root:334`

---

## 3. 위반 · 우려 목록

### W1 — 세션 쿠키가 실제로는 sliding 이 아니다 · **심각도 medium** · spec §4 · S-5 3항

- **파일**: `app/back/api/chat_router.py:99-104` · `app/back/repository/chat_repo.py:53-58,66-74`
- **근거 규칙**: SPEC-017 §4 「Max-Age 30일 … 사용(요청)마다 만료 연장」 · §3 S-5 3항
  「세션 만료는 사용 시마다 연장(sliding)된다」 · DEC-026 D1
- **사실**: `Set-Cookie` 는 `resolve_or_create` 가 **새 토큰을 낸 경우에만** 나간다
  (`chat_router.py:103-104`). 이미 세션이 있는 요청에서는 쿠키를 다시 굽지 않으므로
  브라우저의 만료는 **최초 발급 +30일 고정**이다. 서버는 `last_seen_at` 을 밀지만
  (`chat_repo.py:66-74`) 그 값을 읽는 코드가 어디에도 없다 — `get_session_id` 는
  `token_hash` 만 본다(`:53-58`).
- **결과 둘**: ① 31일 이상 연속 사용한 방문자도 대화를 잃는다(계약 위반).
  ② 서버 세션 row 는 **영원히 유효**하다 — 만료 판정도 청소도 없다.
- **판단**: 코드 한 곳(응답마다 `_set_session_cookie`) + `resolve` 의 만료 컷 하나면
  닫힌다. 어느 쪽을 정본으로 둘지는 코디 결정 사항.

### W2 — 동시 요청 경합에서 409 가 500 으로 샌다 · **심각도 medium-low** · spec §4 Case Matrix

- **파일**: `app/back/service/chat/chat_service.py:107-109` · `app/back/models/chat.py:129-136`
- **근거 규칙**: SPEC-017 §4 Case Matrix `CONVERSATION_BUSY` = 409 · §5 직렬화
- **사실**: 앱 검사(`pending_count > 0`)를 두 요청이 동시에 통과하면 두 번째 commit 이
  partial unique index 에 걸려 `IntegrityError` 가 난다. 이를 409 로 접는 핸들러가
  `core/exceptions.py` 에도 라우터에도 없다 → **500**.
- **테스트 상태**: `tests/test_chat_api.py:154-171` 은 「IntegrityError 가 난다」까지만
  확인하고 HTTP 응답은 보지 않는다. 즉 이 갈래는 **의도적으로 열려 있는 것이 아니라
  검증되지 않은 것**이다.
- **판단**: 코드 주석(`chat_service.py:8-12`)은 DB 를 「최종 방어선」이라 부르는데,
  방어선이 뚫린 요청에 어떤 코드를 줄지가 정해져 있지 않다. spec 은 409 를 요구한다.

### W3 — turn 토큰 redaction 이 죽은 코드다 · **심각도 low** · WORK-023 Pre-deploy 3항

- **파일**: `app/back/service/chat/submission.py:179-184` · `app/back/service/chat/runtime.py:147-155`
- **근거 규칙**: WORK-023 Pre-deploy 「turn 토큰이 로그에 원문으로 남지 않음」 ·
  DEC-027 D5
- **사실**: `redact_config_overrides` 를 부르는 프로덕션 코드가 **없다**
  (호출처는 `tests/test_chat_submission.py:212` 뿐). `runtime.py:154` 의 로그는
  `mask(None)` 이라 **항상 `<none>`** 이다 — 마스킹이 아니라 아무것도 안 찍는 것이다.
- **현재 위험**: back 자체는 overrides 를 로그로 내지 않으므로 누출 경로가 없다.
  다만 ① `runtime.py:143` 의 `logger.exception` 이 잡는 예외가 제출 인자(=Bearer 포함
  `-c` 목록)를 문자열에 담고 있으면 그대로 찍힌다, ② open-kknaks/codex 쪽 로깅은
  back 의 redaction 이 관여하지 못한다.
- **판단**: Pre-deploy 항목은 **back 한정으로만** 참이다. 워커/브로커 로그를 확인하지
  않으면 체크박스를 채울 수 없다 → §5 질문 Q3.

### W4 — problem 합성 slug 의 왕복 검증이 career 와 다르다 · **심각도 low** · spec §4 slug 규약

- **파일**: `app/back/service/chat/tool_service.py:111-118` (career 는 `:105-108`)
- **사실**: career 는 복원한 행의 정본 slug 와 요청 slug 가 다르면 404 로 접는다.
  problem 에는 같은 검사가 없어 `problem-007` 이 200 을 받고, 응답·근거 카드의 slug 는
  `problem-7` 로 돌아온다.
- **영향**: 존재 여부는 새지 않는다(404 동일성은 유지). 다만 「손잡이를 하나로 둔다」는
  같은 파일의 규약(`:105-107` 주석)이 두 유형에서 갈린다.

### W5 — MCP 가 모델이 준 slug 를 URL 인코딩 없이 경로에 붙인다 · **심각도 low** · DEC-027 D3

- **파일**: `app/mcp/app/server.py:123,145,166,188` → `app/mcp/app/back_client.py:31`
- **근거 규칙**: DEC-027 D3 「AI 가 파일 경로를 직접 넘기는 일이 없다」 · 경계는 지시가
  아니라 구조
- **사실**: `f"/api/chat-tool/careers/{slug}"` 를 그대로 `httpx` 에 넘긴다. httpx 는
  base_url 의 raw_path 에 **단순 연결**하며 dot-segment 정규화를 하지 않고, FastAPI 의
  `{slug}` 는 `/` 를 매칭하지 않으므로 **현재는 전부 404 로 끝난다** — 실제 이탈 경로는
  확인되지 않았다.
- **판단**: 지금은 뚫리지 않지만, 모델이 제어하는 문자열이 URL 문법으로 흐르는 자리가
  남아 있다. `urllib.parse.quote(slug, safe="")` 한 줄이 이 축을 구조로 닫는다.

### W6 — 「다시 시도」가 질문 줄을 하나 더 만든다 · **심각도 low** · spec §3 S-8 3항

- **파일**: `app/front/components/chat/chat-view.tsx:152-164`
- **근거 규칙**: SPEC-017 §3 S-8 3항 「같은 질문을 **새 assistant 메시지**로 재제출한다」
- **사실**: 재시도가 `continueConversation` → `POST …/messages` 를 부르므로 BE 가
  user + assistant **한 쌍**을 새로 만든다. 스레드에 같은 질문이 두 번 보인다.
- **판단**: BE 에 재시도 전용 경로가 없어 FE 만으로는 못 고친다. spec 환류(재시도의
  정의를 「질문 재전송」으로 열거나, BE 에 재제출 엔드포인트 추가) 결정이 필요하다.

### W7 — 토큰 밖 색 1건 · **심각도 low** · WORK-024 「globals.css 토큰만 사용」

- **파일**: `app/front/components/admin/chat-exposure-toggle.tsx:66`
- **사실**: `color: var(--danger, #e5534b)` — `--danger` 는
  `app/front/app/globals.css:41` 에 이미 정의돼 있어 fallback hex 는 도달하지 않는
  죽은 값이다. 그래도 토큰 규약 밖의 색 리터럴이다.
- 참고: 신규 CSS 514줄 본문에는 raw 색 0건 — 이 한 곳만 인라인 스타일에 있다.

### W8 — 브랜치가 `origin/main` 보다 1커밋 뒤다 · **심각도 info**

- **사실**: `HEAD ecb689e` 는 `origin/main 2d07629` 의 **조상**이다
  (`git log origin/main..HEAD` 비어 있음). main 이 앞서 갖고 있는 커밋은
  `app/back/main.py`(2줄) · `service/persona_service.py` · `api/persona_router.py` ·
  `seed/seed_profile.py` · `.agents/` · `para/` · `resume/` 를 건드린다.
- **주의**: 이 작업도 `app/back/main.py` 를 고친다(라우터 등록 · 기동 스윕). 서로 다른
  자리라 자동 머지될 확률이 높지만, 머지·리베이스 전에 확인할 유일한 겹침이다.
- 이 역방향 diff 때문에 `git diff origin/main` 만 보면 `para/`·`resume/` 오염처럼
  보인다 — **오염 아니다.**

### W9 — chat-tool 응답만 `schemas/` 층을 쓰지 않는다 · **심각도 info** · 레포 계층 규약

- **파일**: `app/back/api/chat_tool_router.py:46-60`
- **사실**: `asdict(dto)` 로 dict 를 직접 조립하고 pydantic 스키마를 거치지 않는다.
  레포 규약상 계약 표면은 `schemas/` 인데 이 표면만 예외다.
- **판단**: front 계약이 아니라 MCP 계약이고 소비자가 하나(우리 MCP 서버)라 실해는
  없다. 다만 「계약은 schemas 가 갖는다」가 예외를 하나 갖게 된다.

### W10 — 재생 복구 + 스트림 소멸 조합에서 부분 텍스트가 사라진다 · **심각도 low**

- **파일**: `app/back/service/chat/consumer.py:226-231`(reset) → `:445-463`(마감)
- **사실**: 기동 스윕이 `replay=True` 로 붙으면 먼저 `content=""` 를 커밋한다.
  스트림이 이미 만료돼 이벤트가 하나도 안 오면 `_close_from_task` 가
  `result_text=None` 으로 마감하므로 최종 content 는 **빈 문자열**이 된다.
- **모순**: `finalize` 의 docstring(`consumer.py:299-303`)은 「실패 마감에서는 부분
  텍스트를 지우지 않는다 — 방문자가 이미 읽은 글자를 사후에 뺏지 않는다」인데, 재생
  경로에서는 마감 **전에** 이미 지워져 있다.
- **사용자 영향**: FE 는 `failed` 에서 content 를 그리지 않고 실패 문구만 보이므로
  화면상 차이는 없다. DB 기록과 명시된 불변식이 어긋나는 문제다.
- **테스트 공백**: `test_replay_resets_text_before_reaccumulating:77` 은 재적재가
  되는 경우만 본다. 「재생했는데 스트림이 죽어 있다」 케이스가 없다.

---

## 4. 확인했으나 문제 없던 것 (되짚기 방지)

- `chat-worker`·`mcp` 컨테이너 **원장 마운트 없음** — compose 추가분에서 확인.
- `CODEX_HOME=/root/.codex-chat` 분리 + `chat-codex-sessions` 별도 볼륨 — 파이프라인
  세션 resume 사고 축 제거(D5).
- `skip_git_repo_check` 가 신규·resume 공통으로 실린다(`submission.py:167`).
- `resume` 있으면 지난 기록을 **싣지 않는다**(`runtime.py:105-107`) — D2 의
  「같은 것을 두 번 싣지 않는다」 준수. 테스트 `test_chat_submission.py:343,370`.
- 시스템 프롬프트의 커리어 개요도 `chat_exposed` 를 통과한 것만이다
  (`runtime.py:99-103` → `chat_tool_repo.list_careers`) — 프롬프트가 경계를 우회하지 않는다.
- `alembic` 리비전 체인 정상: `b7d3e1f04a92 ← f1c0a9b2d3e4` (헤드 분기 없음).
  downgrade 는 신규 표 3 + 컬럼 3 을 되돌린다(WORK-023 Rollback 그대로).
- `.env` 실값 커밋 없음 — `app/mcp/.env.example` 은 예시뿐이고, `app/back` 에는
  추적되는 env 파일 자체가 없다.
- MCP `stateless_http=True` + Mount lifespan 명시(`server.py:248-254`) — 알려진
  「Task group is not initialized」 함정을 피했다.
- FE 죽은 타입 `HeroTerminalLine`(`lib/types.ts:28,505`)이 남아 있으나 컴포넌트 제거와
  무관한 site config 계약이라 그대로 두는 것이 맞다.

---

## 5. 코디가 물어야 할 질문

**Q1 (W1 — 결정 필요).** 세션 sliding 을 어디서 실현할 것인가?
① 매 응답마다 쿠키를 다시 굽는다(브라우저 만료 연장), ② `resolve` 가 `last_seen_at`
기준 30일 컷을 적용한다(서버 만료), ③ 둘 다. spec §4 문구는 ①을, DEC-026 D1 의
「sliding」은 ③을 읽게 한다. **현재는 어느 쪽도 없다** — 착지 전 정할 것.

**Q2 (W2 — 결정 필요).** partial unique index 위반(`IntegrityError`)을 409
`CONVERSATION_BUSY` 로 접을 것인가, 500 을 수용할 것인가? spec Case Matrix 는 409 를
요구한다. 접는다면 예외 핸들러 자리(`core/exceptions.py` vs 서비스)도 함께.

**Q3 (W3 — 확인 필요).** open-kknaks/codex 워커가 제출 인자(`-c` 목록)를 로그에
남기는가? 남긴다면 back 의 `redact_config_overrides` 로는 못 막으므로 WORK-023
Pre-deploy 3항을 「back 로그 한정」으로 좁혀 적거나, 워커 로그 레벨을 조정해야 한다.

**Q4 (W6 — spec 환류).** 「다시 시도」가 질문을 다시 만드는 것을 수용할 것인가
(S-8 3항 문구 완화), 아니면 BE 에 재제출 전용 경로를 추가할 것인가?
WORK-023 「SPEC 환류」 규칙상 임의 결정 금지 항목이다.

**Q5 (W8 — 절차).** 머지 전에 `origin/main`(2d07629) 을 먼저 받을 것인가?
겹치는 파일은 `app/back/main.py` 하나다.

**Q6 (미검증 축 — 범위 밖 고지).** 이 검수는 정적 검토다. 다음 셋은 **코드로 확인할 수
없어 판정하지 않았다** — 코디의 통합 검증에 남긴다:
① codex 가 `-c` 오버라이드를 실제로 먹고 MCP 에 붙는가,
② `chat_mcp_url` 기본값(`http://mcp:28081/mcp`)이 compose 네트워크에서 닿는가
(compose 는 `back` 에 `CHAT_MCP_URL` 을 주지 않고 기본값에 의존한다),
③ 180초 timeout 이 실제 응답 지연에 충분한가(DEC-027 OQ-2 실측).
