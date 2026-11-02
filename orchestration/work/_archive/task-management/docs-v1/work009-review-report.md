---
type: review
work: WORK-009
title: "WORK-009 검수 — MCP 서버 · 회의별 단명 토큰 · codex allow list"
reviewer: reviewer
date: 2026-09-07
scope: "미커밋 변경 18 파일 + 신규 app/mcp · 0007 리비전 · 테스트 2 파일"
worktree: /Users/kknaks/orca/workspaces/task_management/docs-v1 (kknaksss/docs-v1 · HEAD aa98518)
verdict: "FAIL 1 · WARN 7 · 문서 공백 6"
---

# WORK-009 검수 리포트

**FAIL 1 · WARN 7 · 문서 공백 6.**
`tauri.conf.json` 은 범위 밖이라 보지 않았다. 테스트는 돌리지 않았다(코디 실측 — 557 passed · mcp 40 · compose 5 healthy).

## 0. 축별 판정 한 줄

| 축 | 판정 | 한 줄 |
|---|---|---|
| 2-1 권한 경계 — MCP 가 두 번째 게이트인가 | **PASS** | 판정·캐시·쓰기·DB·back import 0. 401/404 를 삼키는 코드 0. 가공은 WP §Internal Interface 가 지정한 사영뿐 |
| 2-2 토큰 — A-13 넷 | **FAIL 1 · WARN 1** | 원문·회의당 하나·행 DELETE·401 하나는 전부 코드가 됐다. **회의 목록 표면(`GET /api/meetings`)이 회의 토큰에 열려 있다** |
| 2-3 옵션 빌더 | **PASS** | 한 함수 · 문자열 14 줄이 WP 순서 그대로 · `tm.` 접두 없음 · `approval_policy` 0 · `sandbox` 는 새 세션만. 호출부는 토큰만 더했다 |
| 2-4 계층 · 트랜잭션 · 예외 | **PASS · WARN 1** | 새 `commit()` 0 · `except Exception` 0 · repository 는 DTO 만. `"none"` 센티널이 service 까지 내려간 것 하나 |
| 2-5 리비전 · compose · env | **PASS · WARN 1** | 0007 다섯 요소 · downgrade 순서 정확 · 5 서비스 · `mcp_server_url` 기본값 없음. `worker` 가 `mcp` 를 안 기다린다 |
| 2-6 테스트가 WP 검증을 덮나 | **WARN 3** | 24 + 14 + 40 이 대부분을 덮는다. 리비전 왕복 · 회의 목록 · Phase 4 실측 셋이 빈다 |

---

## 1. FAIL

### F-1. 회의 토큰으로 **그 회의 밖의 회의 리소스**가 나간다 — `GET /api/meetings` 목록

- **자리**: `app/back/api/deps.py:86-88` · 열린 표면은 `app/back/api/meeting_router.py:59`
- **어긋난 문서**: WP §Scope 「회의 토큰으로 온 요청은 … **그 회의 밖의 회의 리소스는 404**」 · DEC-003 §2 「도구는 **이 회의·이 계정 범위**에서만 답하고, 그 범위 판정은 **백엔드가 진다**」 · `system/README.md` 불변식 14 · SPEC-007 §4 L146
- **무엇이 일어나나**: `require_context` 의 회의 범위 검사는 **경로에 `{meeting_id}` 가 있을 때만** 돈다(`path_meeting_id is not None`). `GET /api/meetings?from=&to=` 는 경로 파라미터가 없어 그대로 통과하고, `list_meetings(account_id=…)` 가 **그 계정의 모든 회의**(제목 · 일시 · 유형 · 프로젝트 · 집계)를 돌려준다. `GET /api/meetings/{other}` 는 404 인데 목록으로는 같은 회의가 다 보인다.
- **왜 FAIL 인가**: 오늘 실제로 AI 가 이 표면을 부르지는 못한다 — `enabled_tools` allow list 에 대응 도구가 없다. 그러나 그것은 **codex 설정이 막는 것**이지 백엔드가 막는 것이 아니다. 「권한 경계는 백엔드가 진다 · MCP 는 두 번째 게이트가 아니다」(DEC-003 §2 · 불변식 14)의 방향이 뒤집힌다. 토큰 원문이 워커 로그에 실리는 설계(WP Phase 4)에서 REST 를 직접 부르는 경로가 남는 것도 같은 이유로 곤란하다.
- **성격**: 계정 밖으로는 새지 않는다(계정 범위는 지켜진다). 회의 범위만 안 걸린다.
- **고치는 자리 후보**(선택은 코드 워커/코디): `require_context` 가 「회의 라우터의 경로인데 `{meeting_id}` 도 `current` 도 아니면 404」를 더하거나, 목록 라우트에서 `ctx.meeting_id` 를 보고 404 를 내는 것. 문서에 규칙이 없으니 §4 D-7 로 함께 올린다.

---

## 2. WARN

### W-1. 404 본문 문구가 SPEC-006 §4 계약과 다르고, 업무 표면에도 회의록 문구가 나간다

- **자리**: `app/back/api/deps.py:32` `_NOT_FOUND = "없는 회의록입니다"`
- **어긋난 문서**: SPEC-006 §4 Case Matrix — `not_found` → `404 {detail:"회의록을 찾을 수 없습니다", code:"not_found"}`. 「없는 회의록입니다」는 **화면 문구**다(같은 표 오른쪽 칸 · §6 AC L697). `meeting_service.py:73` 은 계약대로 `"회의록을 찾을 수 없습니다"` 를 쓴다.
- **무엇이 일어나나**: 회의 토큰이 쓰기 표면을 치면 어디서든 이 문구가 나간다 — `POST /api/tasks` 도 `DELETE /api/work-types/{id}` 도 「없는 회의록입니다」다.
- **거부 사유 누설은 아니다**: 회의 토큰 소지자 기준으로는 「없는 회의」와 「남의 회의」와 「쓰기 금지」가 **전부 같은 본문**이라 구별되지 않는다(deps 의 주석대로다). 문제는 문구 계약과 표면 불일치뿐이다.

### W-2. `GET /api/jobs/{job_id}` 도 회의 토큰에 열려 있다

- **자리**: `app/back/api/job_router.py:19,23`
- **문서**: WP §Internal Interface 「그 밖(업무 · 유형 · 프로필 조회)은 계정 범위 그대로」 — job 은 열거에 없다.
- 대응 도구가 없는 조회 표면이다. 계정 범위이고 GET 이라 계약 문언 위반은 아니나, 「도구가 부르는 표면만 연다」는 결이 아니다. F-1 과 같은 결정에 묶어 판단하면 된다.

### W-3. `worker` 가 `mcp` 를 기다리지 않는다

- **자리**: `docker-compose.local.yml:105-137` — `worker.depends_on` 은 `redis` 하나. `mcp` 는 `api` 를 `service_healthy` 로 기다린다(83-104).
- **어긋난 문서**: WP §Pre-deploy Check 「compose 다섯 서비스 기동 순서 — `api` → `mcp` → `worker`」 · §Code Surface 「worker 가 mcp 를, mcp 가 api 를 본다」
- **왜 문제인가**: mcp 가 늦게 뜨는 동안 제출된 웜스타트/배치는 **에러가 아니라 조용히 「툴 0개」**로 돈다(`system/README.md` §codex 설정 — deny list 가 없고 틀린 MCP 주소는 침묵한다). 정확히 문서가 경계하는 실패 모양이다.

### W-4. `"none"` 센티널이 service 까지 내려가고, 같은 리터럴이 두 곳에 산다

- **자리**: `app/back/service/meeting_service.py:559,562-586`(`UNASSIGNED_PROJECT` · `project_id: str | None` · `int(project_id)`) vs `app/back/api/meeting_router.py:53,80-88`(`_UNASSIGNED` · 라우터에서 파싱해 `MeetingListFilterDTO` 로 넘긴다)
- **어긋난 문서**: `backend/README.md` §2 계층 · §3 schema/dto — 같은 라우터의 이웃 표면이 이미 「라우터가 쿼리 문자열을 풀고 service 는 타입만 받는다」로 서 있다. 새 표면 하나만 HTTP 인코딩(`"none"`)을 service 가 안다.
- 동작에는 문제가 없다(`_PROJECT_ID_PATTERN` 이 `^(none|[0-9]+)$` 로 막는다). 규약 일관성 문제다.

### W-5. 테스트 공백 — 리비전 왕복이 자동화돼 있지 않다

- `app/back/tests/conftest.py:52` 는 `command.upgrade(config, "head")` 하나뿐이다. `downgrade -1 → upgrade` 를 도는 테스트가 없다.
- **어긋난 문서**: WP Phase 1 검증 첫 항목 「`alembic upgrade head` → `downgrade -1` → `upgrade` 왕복. 기존 refresh 행이 `kind='refresh'` 로 남는다」
- 코드 자체는 읽어서 검토했고 순서에 문제를 못 찾았다 — `downgrade` 가 meeting 행 DELETE → CHECK 3 → 인덱스 → FK → `refresh_token_hash` NOT NULL 복구 → 컬럼 3 제거 순이라 NOT NULL 복구가 먼저 깨질 자리가 없다. **손으로든 테스트로든 한 번 도는 증거가 필요하다.**

### W-6. 테스트 공백 — 회의 목록 표면에 대한 회의 토큰 테스트가 없다

- `test_meeting_token.py` 의 조회 테스트는 `/current` · `/current/tasks` · `/{id}` · `/api/tasks` · `/api/work-types` · `/api/auth/session` 을 친다. `GET /api/meetings`(목록)를 치는 테스트가 없다 — F-1 이 안 잡힌 이유다.

### W-7. Phase 4 실측 증거가 없다 — 이 work 의 Done 이 아직 안 닫혔다

- WP Done Criteria 「SPEC-007 §6 AC 의 codex 설정 항목 1개 + 「도구 호출 헤더의 토큰 ≠ 세션 토큰」이 **실측 캡처**로 완료 증거에 있다」 · Phase 4 「워커 로그의 도구 호출이 우리 7개 밖 0건(`command_execution` · `web_search` 0건)」 · 「`revoke` 뒤 같은 토큰으로 도구 호출 → 401 이 도구 결과에 드러난다」
- 코디 실측은 「557 passed · mcp 40 · compose 5 healthy」까지다. **워커 로그의 `mcp_tool_call` · 도구 밖 0건 · 헤더 토큰 ≠ JWT (DB 대조)** 는 아직 없다. WP Phase 1~4 의 `Status` 와 `완료 증거` 도 `TODO` · `미작성` 그대로다.

---

## 3. PASS — 무엇을 확인했나

### 3-1. 권한 경계 (MF-4 · 불변식 13 · 14 · SYS-15)

| 검사 | 결과 |
|---|---|
| `app/mcp` 가 `app/back` 을 import | **0** (`tests/test_static.py:55` 가 같은 검사를 자동화) |
| `app/mcp` 의 DB 드라이버 의존 | **0** — `uv.lock` 47 패키지에 `sqlalchemy`·`psycopg`·`asyncpg`·`alembic` 없음 |
| `app/mcp` 의 쓰기 HTTP 메서드 | **0** — HTTP 호출 지점은 `tools.py:_get()` 하나뿐이고 `client.get` 만 부른다 |
| 401/404 를 빈 배열·기본값으로 | **0** — `BackendError(status, body)` 로 올리고 `server.py:_call` 이 `ToolError` 로 그대로 통과시킨다(설계한 실패 둘만 바꾸고 나머지는 손대지 않고 전파) |
| 캐시 | 없음 — `_client()` 가 호출마다 새 `AsyncClient` 를 연다(MF-50 「조회하면 그 순간 최신」) |
| 헤더 | `server.py:_forwarded_headers` 가 `Authorization` 을 **그대로** 넘기고, 없으면 붙이지 않는다 → back 의 401 이 도구 결과가 된다 |

**가공에 대한 판단**: `tools.py` 의 `_agenda_row` · `_line_row` · `_tracked_agendas` 는 사영이지 판정이 아니다. WP §Internal Interface 가 `list_agendas` → `{id, title, state, track, sourceAgendaId}` · `get_agenda` → 그 안건 + `lines[]`(`kind`·`content`·`detail`·`taskId`) 로 **지정한 모양**이고, SPEC-007 §4 도구 표와 같다. `merged` 를 빼는 것도 SPEC-008 이 회의 후 산출물로 정한 것이라 맞다. `list_work_types` · `list_tasks` · `get_task` · `get_account` 는 응답 그대로 통과한다(코디 답 ②대로).
`get_agenda` 가 `AgendaNotFound` 를 내는 것은 **이미 back 이 인가한 `/current` 응답 안에서의 조회 실패**라 두 번째 게이트가 아니다 — 「조용히 빈 안건을 지어내지 않는다」쪽이다.
도구 이름 7개는 `system/README.md` §Components L95 · SPEC-007 §4 표와 **글자 그대로** 같다(`tools.py:TOOL_NAMES` · `agent.py:_TOOL_NAMES` · `test_tools.py:112`).

### 3-2. 토큰 — A-13 넷

| A-13 규칙 | 코드 | 확인 |
|---|---|---|
| **원문 저장** | `core/security.py:131-139` `generate_meeting_token()` — 해시 함수 짝이 **없다**. `models/account.py` `meeting_token String(255) NULL` | A-7 회귀 0 — `hash_refresh_token` 그대로, `find_by_token_hash`·`revoke`·`revoke_all_for_account` 는 전부 `kind='refresh'` 로 좁혔다(`auth_session_repository.py:58-105`) |
| **회의당 하나** | `meeting_service.py:539-544` — 전이 UPDATE 와 **같은 트랜잭션**, `session.commit()`(546) 앞. 재발급 경로 없음 | 두 번 INSERT 되는 경로 없음 — `start()` 가 `_assert_allowed(current,"start")`(534)로 `scheduled` 에서만 지나고 상태는 한 방향이다. `get_meeting_token` 은 `one_or_none()` 이라 두 행이 생기면 조용히 하나를 고르지 않고 터진다 |
| **폐기 = 행 DELETE** | `auth_session_repository.py:171-180` `delete()` · `revoked_at` 을 **안 찍는다** · 0건이어도 예외 없음(`rowcount or 0`) | `test_meeting_token.py:288` 두 번 호출 → 1 · 0 · 이후 401. A-7 재사용 감지가 회의 토큰을 안 끊는다(`test:307` — `revoke_all_for_account` 뒤에도 행이 살고 `/current` 가 200) |
| **검증** | `auth_service.py:199-221` `resolve_bearer` — ① `decode_access_token`(DB 안 봄) ② 실패 시 `find_meeting_token`(원문 일치 · 만료 제외 · `revoked_at` 안 봄) ③ 둘 다 아니면 `UnauthorizedError("세션이 만료되었습니다", code="token_expired")` **하나** | `except UnauthorizedError` 로만 갈라진다 — `decode_access_token`(security.py:99-120)이 만료·위조·형식 오류를 전부 그 하나로 모으므로 사유가 안 샌다. 헤더 없음도 같은 401(`deps.py:80`) |

**회의 범위** — 쓰기 표면 전수: `meeting_router` 의 POST/PATCH/DELETE 16 개 · `task_router` 16 개 · `setting_router` 6 개 · `auth_router.session_router` 의 `POST /logout` 까지 **전부** `require_context` 의 `_READ_METHODS` 게이트를 지난다(`deps.py:83`). 라우터 단위 `dependencies=[Depends(require_account)]` 가 5 라우터에 다 걸려 있어(`meeting:48` · `task:40` · `setting:28` · `job:19` · `auth.session_router:30`) 빠진 쓰기 라우터가 없다. WS(`meeting_stream_router:85`)는 `decode_access_token` 을 직접 부르므로 회의 토큰으로 열리지 않는다.
읽기 쪽 회의 범위는 `{meeting_id}` 경로 파라미터 대조(`deps.py:86-88`)로 걸리고, 회의 라우터의 모든 하위 경로가 이름을 `meeting_id` 로 통일해 두어 빠지는 자리가 없다 — **F-1(경로 파라미터가 없는 목록)만 예외다.**

**원문 노출** — `schemas/` · `api/` 에 `meeting_token` **0건**. `AuthSessionDTO` 는 원문을 담지 않는다(`dto/auth.py:44-49`). 예외 메시지도 `f"회의 {meeting_id} 에 회의 토큰이 없습니다"` 로 id 만 싣는다. `test_agent_options.py:171` 이 로그 포맷 문자열까지 자동으로 검사한다.

### 3-3. 옵션 빌더 (MF-3 · BE §5-2)

- `provider_options` · `mcp_servers` 문자열을 만드는 곳: **`integrations/agent.py` 뿐**(grep — `build_mcp_config:86` 이 목록을, `build_codex_options:113` 이 조립을 맡고 앞 함수는 뒤 함수만 부른다. WP 가 말한 「한 함수」의 실질을 지킨다). `test_agent_options.py:156` 이 정적으로 고정.
- 문자열·순서: `expected_config()`(테스트가 **손으로 적은** 14 줄)와 WP §Internal Interface 목록이 완전히 일치한다 — `features.shell_tool=false` / `web_search="disabled"` / `features.image_generation=false` / `features.apps=false` / `mcp_servers.tm.url=…` / `mcp_servers.tm.http_headers={Authorization="Bearer …"}` / `enabled_tools=[7개]` / `tools.<7>.approval_mode="approve"`.
- `enabled_tools` 에 `tm.` 접두 **없음**(`agent.py:93` 이 이름만 감싼다 · `test:96`). `approval_policy` 는 소스 전체에 **0건**(주석·테스트 제외).
- `sandbox="read-only"` 는 `session_id is None` 일 때만(`agent.py:127-128` · `test:56,83`). `config` 는 양쪽에 같은 목록(`test:69`).
- 호출부: `meeting_batch_service`(270 · 413) · `meeting_finalize_service`(221) · `warm_start`(660) 가 **`meeting_token=` 인자 하나만** 더했다. 프롬프트 빌더(`build_warm_start_prompt` · `build_final_prompt` · `build_integration_prompt`)와 `_load_input` 계열은 손대지 않았다 — **WORK-010/011/012 범위 침범 없음**. `TaskContextDTO` 에 `project_name` 이 붙었지만 `_task_rows`(680-689)가 필드를 손으로 골라 실으므로 **웜스타트 프롬프트 본문은 그대로다**.
- 토큰 없음 처리: `RuntimeError` 전파(batch 262 · 402 · finalize 213) — `ai_session_id` 없음과 **같은 취급**이라 WP Phase 3 「세션 없음과 같은 취급(MF-70)」에 맞고, 새 실패 갈래를 만들지 않았다(불변식 15).

### 3-4. 계층 · 트랜잭션 · 예외

- router 가 ORM 을 만지지 않는다. `/current`(`meeting_router:117`) · `/current/tasks`(136)는 `require_context` → `meeting_service` → `task_repository`/`meeting_repository` 를 지난다.
- `/current/tasks` 가 **사후 검사(M-15)와 같은 repository 함수**를 쓴다 — `task_repository.list_meeting_context` 하나이고, 배치 화이트리스트(`meeting_batch_service:347,470,647`)와 같은 함수·같은 인자 규약(회의 프로젝트 · 무소속이면 무소속)이다. WP §Internal Interface 「AI 가 보는 목록 = 서버가 검사하는 목록」 충족.
- service 가 `fastapi` · `schemas` 를 import 하지 않는다. repository 는 DTO 만 내보낸다(`_to_dto` · `TaskContextDTO`).
- **새로 더한 `commit()` 0** — `meeting_service.start()` 의 기존 하나(546)뿐이고 토큰 INSERT 가 그 앞에 들어가 전이와 갈리지 않는다.
- `except Exception` · `except BaseException` · 임의 재시도 · 조용한 기본값 **0** (`app/back` · `app/mcp` 전수).

### 3-5. 리비전 · compose · env

- `0007_auth_session_meeting_token` (`down_revision="0006_job"`) — `kind` `server_default 'refresh'` NOT NULL ✓ · `meeting_id` BigInteger + FK `fk_auth_session_meeting_id` ✓ · `meeting_token String(255) NULL` ✓ · `refresh_token_hash` NULL 완화 ✓ · 부분 인덱스 `ix_auth_session_meeting_id (meeting_id) WHERE kind='meeting'` ✓ · CHECK 셋(`kind IN (…)` · `(kind='meeting') = (meeting_id IS NOT NULL AND meeting_token IS NOT NULL)` · `kind <> 'refresh' OR refresh_token_hash IS NOT NULL`) ✓. 모델(`models/account.py:93-131`)이 같은 이름·같은 식으로 선언돼 있다.
- `downgrade` 가 meeting 행을 먼저 DELETE 하고 컬럼을 뺀다 ✓ (순서 검토는 W-5).
- compose 다섯: `db`(15) · `redis`(31) · `api`(43) · `mcp`(83) · `worker`(105). `mcp.depends_on: api / condition: service_healthy` ✓ (그래서 `api` 에 헬스체크가 새로 붙었다). `worker` 의 마운트 4종 · `PATH` · `CODEX_HOME` · 브로커 env **변화 없음** ✓ (기동 순서는 W-3).
- `config.py:36-39` `mcp_server_url: str = Field(min_length=1)` — **기본값 없음**(비면 기동 실패) ✓ · `meeting_token_ttl_min: int = 330`(71) ✓. `.env.example` 에 `MCP_SERVER_URL` · `MEETING_TOKEN_TTL_MIN` 두 줄 + 주석 ✓ (`MCP_PORT` 가 덤으로 하나 더 — D-5).

---

## 4. 문서 공백 (지적이 아니다 — 코디가 정하거나 문서를 고칠 자리)

| # | 자리 | 무엇이 비었나 |
|---|---|---|
| **D-1** | `system/README.md` §codex 설정 L133 · `backend/README.md` §5-2 「단명 토큰의 축은 `auth_session` 행이다」 문단 | 둘 다 아직 **「(해시만 저장)」** 이라 적혀 있다. `account.md` A-13 은 2026-09-07 저녁에 **원문 컬럼**으로 확정됐고 코드는 A-13 을 따랐다. 두 문장이 정정 대상 |
| **D-2** | WP Phase 3 검증 「`config` **7+5 줄**」 | 실제 계약 목록은 **14 줄**(내장 4 + url + headers + enabled_tools + 툴별 7). 코드·테스트는 14 로 맞다 — 문서의 수식만 틀렸다 |
| **D-3** | WP §Pre-deploy 「토큰 원문이 로그 · 응답에 없다」 vs Phase 4 「워커 로그에 `-c mcp_servers.tm.*` 가 보인다」 | 헤더 토큰은 `-c` 문자열에 실려 **워커 로그에 원문으로 남는다**(설계상 그래야 Phase 4 를 볼 수 있다). 「로그」가 back 로그만인지 워커 로그까지인지 문서가 가르지 않는다 |
| **D-4** | SPEC-007 §4 도구 표 · DEC-003 §8 은 `list_tasks(projectId?)` · `get_agenda(id)` 카멜/약칭 | 실제 MCP 도구 인자는 `project_id` · `agenda_id` · `task_id`(스네이크). 도구 **인자 이름** 규약이 어느 문서에도 없다. 이름이 계약이면 못 박아야 하고, 아니면 그렇다고 적어야 한다 |
| **D-5** | `backend/README.md` §11 env 표 | `MCP_PORT` 가 없다(`MCP_BASE_URL` · `MCP_SERVER_URL` · `MEETING_TOKEN_TTL_MIN` 셋뿐). `.env.example` 과 compose 가 쓴다 |
| **D-6** | `database/README.md` §4 `auth_session` 행 | `` `UNIQUE (refresh_token_hash)`, `(account_id, expires_at)`, `(meeting_id) WHERE kind='meeting'` `` 이 세 개 다 UNIQUE 인지 첫 개만인지 문장이 가르지 않는다. 코드는 **비유니크 부분 인덱스**로 갔고 「회의당 하나」는 `start()` 의 상태 게이트가 지킨다. DB 로 못 박을지 결정 필요 |
| **D-7** | WP §Internal Interface 「회의 범위」 행 | 「`{id}` 와 다를 때 404」만 적혀 있고, **경로 파라미터가 없는 회의 표면**(목록 `GET /api/meetings`)에 대한 규칙이 없다. F-1 의 뿌리다 |

---

## 5. 2-6 — WP 검증 항목 ↔ 테스트 대응표

**있는 것**(`test_meeting_token.py` 24 · `test_agent_options.py` 14 · `app/mcp/tests` 40)

| WP 검증 항목 | 테스트 |
|---|---|
| 발급 = 전이와 같은 트랜잭션 · 회의당 하나 | `test_meeting_token.py:51` |
| 제출부가 같은 원문을 다시 읽는다 | `:73` |
| 원문이 `/start` 응답·`MeetingDetail` 에 없다 | `:87` (+ 정적 `test_agent_options.py:171`) |
| 토큰으로 `/current` 200 그 회의 | `:103` |
| **JWT 로 `/current` 404** | `:116` |
| 토큰으로 자기 회의 `/{id}` 200 | `:127` |
| **자기 계정의 다른 회의 404** | `:139` |
| **남의 회의 404** | `:158` |
| **쓰기 표면 404**(회의 5 종 + 업무) | `:190`(parametrize) · `:223` |
| 업무·유형·계정 조회는 계정 범위 | `:210` |
| **서로 대신 못 한다** | `:241` |
| **만료 토큰 401 token_expired** | `:260` · 모르는 Bearer `:278` |
| 폐기 = 행 DELETE · 두 번 예외 없음 · 이후 401 | `:288` |
| A-7 재사용 감지가 회의 토큰을 안 끊는다 | `:307` |
| `/current/tasks` 기본 = 회의 프로젝트 · `none` · 도구 표 필드 · JWT 404 | `:338` `:355` `:372` `:386` |
| **옵션 문자열·순서**(새 세션) | `test_agent_options.py:48` |
| 새 세션 `sandbox="read-only"` | `:56` |
| resume 도 같은 `config` | `:69` |
| **resume 에 `sandbox` 없음** | `:83` |
| `enabled_tools` 접두 없음 | `:96` |
| `approval_policy` 0 | `:109` |
| 툴별 `approval_mode` 7 | `:120` |
| 토큰은 헤더 문자열에만 | `:133` |
| 옵션 만드는 곳 한 곳(정적) | `:156` |
| 토큰이 로그·직렬화에 없음(정적) | `:171` |
| 도구 이름 7개 = 문서 표 | `mcp/tests/test_tools.py:112` `:125` |
| 도구 ↔ REST 대응 7 + 쿼리 통과 | `:133` `:143` `:152` `:169` `:193` `:204` `:213` `:222` |
| 회의 밖 안건을 지어내지 않는다 | `:185` |
| **헤더가 그대로 back 에 닿는다 / 없으면 안 붙인다** | `:240` · `server` 쪽 `:298` `:310` |
| 전 도구가 GET 뿐 | `:248` |
| **back 의 401/404 가 그대로 드러난다** | `:272`(parametrize) |
| `app/mcp` back import 0 · DB 0 · 쓰기 0 | `test_static.py:55` `:65` `:76` |

**빈 것**

| WP 검증 항목 | 상태 |
|---|---|
| `alembic upgrade → downgrade -1 → upgrade` 왕복 · 기존 행이 `kind='refresh'` | **자동 테스트 없음**(conftest 는 `upgrade head` 뿐) — W-5 |
| 회의 토큰으로 **회의 목록** 표면 | **테스트 없음** — F-1 이 안 잡힌 이유 · W-6 |
| Phase 2 「compose 다섯 기동 · mcp 가 api 를 기다린다」 | 코디 실측(5 healthy)으로 충족 |
| Phase 4 워커 로그 `mcp_tool_call` · 도구 밖 0건 · 헤더 토큰 ≠ JWT · revoke 후 401 | **미실측** — W-7 (이 항목이 WP 의 Done 이다) |

---

## 6. 요약

토큰 설계(A-13 넷) · 옵션 빌더(문자열 14 줄과 순서 · 함정 셋) · MCP 의 얇음(판정·캐시·쓰기·DB·import 전부 0) · 리비전 · compose 는 **문서대로 섰다.** 회귀도 안 보인다 — A-7 은 `refresh` 행으로 정확히 좁혀졌고, 프롬프트·배치 입력은 옛 설계 그대로라 WORK-010 이후 범위를 침범하지 않았다.

닫아야 할 것은 셋이다 — ① **F-1** 회의 목록 표면(백엔드가 회의 범위를 지는 자리에 구멍이 하나 남았다. 문서에도 규칙이 없어 D-7 과 함께 결정이 필요하다) ② **W-7** Phase 4 실측(이것이 이 work 의 Done 이다) ③ **W-5** 리비전 왕복 증거. 나머지 WARN 넷은 문구·기동 순서·계층 일관성이라 커밋을 막을 무게는 아니다.
