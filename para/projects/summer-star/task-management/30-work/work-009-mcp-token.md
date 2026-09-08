---
type: work
id: WORK-009
title: "회의록 AI — MCP 서버 · 회의별 단명 토큰 · codex allow list"
status: done
product: "task-management"
work_type: new-feature
owner: ""
roles:
  pm: ""
  design: ""
  fe: ""
  be: ""
  qa: ""
  ops: ""
progress: 100
created_at: 2026-09-07
updated_at: 2026-09-07
tags:
  - product/task-management
  - doc/work
  - status/done
links:
  baselines: [BASE-003]
  decisions: [DEC-003, DEC-001]
  specs: [SPEC-007]
  works: [WORK-002, WORK-006, WORK-007]
  releases: []
  related: [SPEC-001, SPEC-006, SPEC-008, WORK-010, WORK-011, WORK-012]
---

# 회의록 AI — MCP 서버 · 회의별 단명 토큰 · codex allow list

**AI 가 우리 데이터를 읽는 유일한 길을 세운다.** 지금 코드는 안건·업무·유형을 프롬프트에 실어 보낸다(옛 설계). 이 work 가 끝나면 codex 는 **별도 컨테이너의 MCP 도구 7개**로 우리 REST 를 부르고, 그 호출은 **회의별 단명 토큰**(`auth_session` 행)으로 인증되며, 셸·웹·이미지·내장 앱은 **codex 설정 allow list** 가 막는다. **WORK-010(회의 시작) · 011(회의 중) · 012(회의 종료)가 전부 이것에 기댄다** — 이게 없으면 배치가 컨텍스트를 못 얻는다.

> 1 파일 = 1 work = **빌드 계획**. dev 가 이 문서만 보고 PR 분리 / 일정 / 작업 시작이 가능해야 한다.
> SPEC 의 외부 계약 본문은 복제하지 않고 frontmatter `links.specs` 와 index 에서 연결한다.
> **결정 원본은 `reference/2026-09-06-task-management-app/Meeting flow.md`** — MF-2 · 3 · 4 · 51 · 55 · 68 · 69. 계약과 부딪히면 그쪽이 이긴다.

## Meta

- Baseline: BASE-003 §Raw L36~L38(AI 가 안건·업무를 볼 수 있어야 한다 — 전달 방식은 MF-50 이 도구로 정했다)
- Covers spec: **SPEC-007 §4 「AI 도구 7개」 표 · 「웜스타트」 표의 도구·토큰 행 · §5 「실행 옵션은 한 빌더에서만」 · §6 AC 「codex 설정에 `enabled_tools` 7개 …」**. 이 work 는 **도구 · 토큰 · 설정**만 세운다 — 웜스타트 프롬프트(WORK-010) · 배치 입력(WORK-011) · 최종 호출(WORK-012)은 이것을 **쓴다**
- Depends on work: **WORK-002**(`auth_session` · `security.py` · `require_account`) · **WORK-006**(`meeting` 도메인 · `/start`) · **WORK-007**(`integrations/agent.py` 옵션 빌더 · compose `worker` · `meeting_batch_service`)
- Parallel work: 없음 — **코드 워커는 한 번에 하나**
- Follow-up work: WORK-010(회의 시작) → 011 → 012 → 013(편집) · WORK-014(목록·상세 UI 는 독립)
- **External dependency**
  - **코드 레포는 별도다** — `github.com/kknaks/task_management`, 워크트리 `/Users/kknaks/orca/workspaces/task_management/docs-v1`. 이 문서 레포에 코드를 만들지 않는다
  - **open-kknaks 2.1.2**(back 핀 = worker 이미지 핀). `provider_options["config"]` 에 문자열 목록을 주면 `codex exec -c <k>=<v>` 로 하나씩 나간다(`worker/codex_adapter.py` `repeated_flags`). **resume 에서도 `config` 는 살아남는다**(`CODEX_RESUME_UNSUPPORTED_OPTIONS` 에 없다). `sandbox` 는 resume 에서 버려지므로 **새 세션(웜스타트) 때 걸린 값을 세션이 물려받는다**. open-kknaks 자체는 고치지 않는다(PyPI 별도 제품)
  - **codex 0.147.0 실측 표**(`system/README.md` §codex 설정) — allow list 뿐이고 deny list 는 없다. `enabled_tools` 에 서버 id 접두를 붙이면 조용히 「툴 0개」. `approval_policy="never"` 는 «user cancelled» 로 죽는다 — 툴별 `approval_mode="approve"` 가 맞다

## Work Summary

| Field | Value |
|---|---|
| Type | new-feature |
| Owner |  |
| Status | done |
| Progress | 100% |
| Branch/PR | `kknaksss/docs-v1` |
| Blocker | 없음 — Open Issues #1 닫힘(회의당 하나 · 원문 컬럼) |
| Next | 없음 — WORK-010 으로 |

## Role Assignment

| Role | Assignee | Responsibility | Status |
|---|---|---|---|
| PM |  | 범위 확정 · SPEC-007 §6 AC 해당 3항목 대조 | todo |
| Design |  | 해당 없음 — 화면 없음 | — |
| FE |  | 해당 없음 | — |
| BE |  | Phase 1~4 전부 — 리비전 · 토큰 · `app/mcp/` · 옵션 빌더 · compose | todo |
| QA |  | 도구 밖 호출 0건 · 남의 회의 404 · 토큰 ≠ 세션 JWT · 폐기 = 행 삭제 · 워커 로그 실측 | todo |
| Ops |  | **신규 env 3개**(`MCP_BASE_URL` · `MCP_SERVER_URL` · `MEETING_TOKEN_TTL_MIN`) · compose 서비스 1개(`mcp`) · `.env.example` | todo |

## Scope

포함:

- **`auth_session` 확장** — `kind ∈ {refresh, meeting}` · `meeting_id`(부분 인덱스 `WHERE kind='meeting'`) · **`meeting_token`(원문 · meeting 행만)** 리비전 `0007`. 발급(`/start` · 회의당 하나 · 원문 컬럼) · 검증(REST 가 그 행으로 계정 · 회의 범위) · 폐기(행 DELETE · best-effort)
- **REST 인증의 두 번째 갈래** — `require_account` 가 Bearer 를 받아 **JWT 면 지금처럼, 아니면 `auth_session(kind='meeting')` 원문 조회**. 회의 토큰으로 온 요청은 `account_id` + `meeting_id` 를 갖고, **그 회의 밖의 회의 리소스는 404**. 사용자 세션 JWT 와 회의 토큰이 서로 대신하지 못한다
- **MCP 서버 `app/mcp/`** — 별도 컨테이너. 도구 7개 = `get_meeting` · `get_account` · `list_agendas` · `get_agenda` · `list_tasks` · `get_task` · `list_work_types`. **전부 조회 · 우리 REST 의 얇은 래퍼**. 받은 `Authorization` 헤더를 그대로 back 으로 넘긴다. DB 를 모른다. back 을 import 하지 않는다
- **codex 실행 옵션 빌더 확장** — `build_codex_options()` 가 allow list(내장 스위치 off · `enabled_tools` 7 · 툴별 `approval_mode`) + MCP 서버 주소 + 헤더 토큰을 `provider_options["config"]` 로 만든다. **옵션을 만드는 곳은 여전히 이 함수 하나**
- **compose** — `mcp` 서비스 신설(back · worker · mcp 셋). worker 가 mcp 를, mcp 가 api 를 본다
- 테스트 — 리비전 왕복 · 토큰 발급/검증/폐기 · 회의 범위 404 · 옵션 빌더 출력(allow list 7 · 헤더) · MCP 도구 7개 ↔ REST 대응(대역 back)

제외:

- **웜스타트 프롬프트 · 컨텍스트 제거 · `/start` 의 commit 제거** → WORK-010. 이 work 는 `/start` 안에서 **토큰 행 INSERT 한 줄**만 더한다
- **배치 입력을 발화 하나로 · AI 트랙 전량 교체** → WORK-011
- **종료 파이프라인 · ② 종결 시 토큰 폐기 호출 자리** → WORK-012 가 `finalize_service` 에서 부른다. 이 work 는 **폐기 함수만** 만든다
- 프론트 전부 · MCP 도구의 **쓰기** 도구(없다 — DEC-003 §8) · MCP 서버의 자체 권한 판정(백엔드가 진다 — MF-4)

## Code Surface

- Repo / module: `github.com/kknaks/task_management` — `app/back`(BE) · **`app/mcp`(신규 · BE 워커)** · `docker-compose.local.yml` · `.env.example`
- 경로는 `backend/README.md` §4 · `system/README.md` §codex 를 따른다

| 경로 | 신규 / 수정 / 폐기 | 설명 |
|---|---|---|
| `app/back/models/account.py` | 수정 | `AuthSession` 에 `kind`(`String CHECK refresh\|meeting`, 기본 `refresh`) · `meeting_id`(`BigInteger FK meeting.id NULL`) · **`meeting_token`(`String(255) NULL` — 원문, meeting 행만)**. `refresh_token_hash` 는 **NULL 허용**으로(meeting 행은 NULL — UNIQUE 는 NULL 을 여러 개 허용). 부분 인덱스 `(meeting_id) WHERE kind='meeting'`(**비유니크** — 회의당 하나는 `start()` 의 상태 게이트가 지킨다 · D-6) · CHECK `kind='meeting' ⇔ (meeting_id IS NOT NULL AND meeting_token IS NOT NULL)` |
| `app/back/alembic/versions/0007_auth_session_meeting_token.py` | **신규** | 위 컬럼 · 인덱스 · CHECK · `refresh_token_hash` NULL 허용. 기존 행은 `kind='refresh'`. `downgrade` 는 meeting 행 DELETE 뒤 컬럼 제거 |
| `app/back/dto/account.py` | 수정 | `AuthSessionDTO` 에 `kind` · `meeting_id`. **`AccountContextDTO`(신규)** — `account_id` · `meeting_id: int \| None`(회의 토큰이면 값) |
| `app/back/core/security.py` | 수정 | `generate_meeting_token()` — refresh 와 같은 생성기(랜덤 32바이트 urlsafe). **해시 함수 없음** — 원문 저장. TTL 은 `settings.meeting_token_ttl_min` |
| `app/back/repository/auth_session_repository.py` | 수정 | `create_meeting_token(session, account_id, meeting_id, token, expires_at)` · `find_meeting_token(token)`(원문 일치 · 만료 제외) · `get_meeting_token(meeting_id)`(제출부가 원문을 읽는다) · `delete_meeting_tokens(meeting_id)` |
| `app/back/service/auth_service.py` | 수정 | `issue_meeting_token(session, account_id, meeting_id) -> str`(원문 INSERT · 반환) · `get_meeting_token(session, meeting_id) -> str \| None`(제출부가 읽는다 — 없거나 만료면 `None`) · `revoke_meeting_token(session, meeting_id)`(행 DELETE · 없으면 조용히 0건) · `resolve_bearer(session, token) -> AccountContextDTO`(JWT 시도 → 실패면 회의 토큰 원문 조회 → 둘 다 아니면 `token_expired`) |
| `app/back/api/deps.py` | 수정 | `require_account` 가 `resolve_bearer` 를 지난다. 반환은 지금처럼 `account_id`(int)를 유지하고, **`require_context`(신규)** 가 `AccountContextDTO` 를 준다 — 회의 라우터가 회의 범위를 봐야 할 때 쓴다. **JWT 경로는 DB 를 안 본다**(지금 그대로) — 회의 토큰만 조회 |
| `app/back/api/meeting_router.py` | 수정 | `GET /api/meetings/{id}` · 안건·줄 조회 표면에 **회의 토큰 범위 검사** — `ctx.meeting_id` 가 있고 `≠ id` 면 `NotFoundError`. 쓰기 표면은 회의 토큰으로 **전부 404**(도구는 조회뿐). **회의 토큰 전용 표면 둘 신설** — `GET /api/meetings/current`(토큰의 회의 상세) · `GET /api/meetings/current/tasks?projectId=`(기간 없음 · 삭제 제외 · 생략 = 회의 프로젝트/무소속 · `none` = 무소속 · **사후 검사 M-15 와 같은 repository 조회**). JWT 로는 둘 다 404 |
| `app/back/api/task_router.py` · `setting_router.py` | 수정(최소) | 회의 토큰으로 **쓰기 표면은 404**, 조회(`GET /api/tasks` · `/{id}` · `/api/work-types` · `/api/profile`)는 계정 범위 그대로 |
| `app/back/service/meeting_service.py` | 수정(한 줄) | `start()` 안 — 전이와 **같은 트랜잭션**에서 `auth_service.issue_meeting_token()`. 회의당 하나 |
| `app/back/integrations/agent.py` | 수정 | `build_codex_options(*, session_id, output_schema, timeout_sec, meeting_token)` — `provider_options["config"]` 에 아래 목록. `sandbox="read-only"` 는 `provider_options["sandbox"]`(새 세션에만 유효 — resume 은 상속). `AgentGateway.run()` 시그니처에 `meeting_token` 추가. **옵션을 만드는 곳은 이 함수 하나**(정적 검사 유지) |
| `app/back/config.py` | 수정 | `mcp_server_url: str`(codex 가 부를 MCP 주소 — compose 안 `http://mcp:8010/mcp`) · `meeting_token_ttl_min: int = 330`(회의 상한 300분 + 여유. 실측 후 조정) · **`mcp_base_url` 은 back 이 아니라 mcp 의 env** |
| `app/mcp/pyproject.toml` · `uv.lock` | **신규** | `mcp`(python SDK) · `httpx`. back 을 의존하지 않는다 |
| `app/mcp/server.py` | **신규** | Streamable HTTP MCP 서버. 도구 7개 등록. 요청의 `Authorization` 을 그대로 `MCP_BASE_URL` 로 전달. back 이 401/404 를 주면 도구 결과로 그 사실을 돌려준다(삼키지 않는다) |
| `app/mcp/tools.py` | **신규** | 도구 7개 ↔ REST 대응표(아래 §Internal Interface). 응답을 **그대로** 돌려준다 — 가공·필터 없음(권한 판정은 back) |
| `app/mcp/Dockerfile` | **신규** | uv 이미지 · `MCP_BASE_URL` · `MCP_PORT` env |
| `docker-compose.local.yml` | 수정 | `mcp` 서비스(`build: ./app/mcp` · `MCP_BASE_URL=http://api:8000` · `depends_on: api`) · `worker` 에 `MCP_SERVER_URL` 은 불필요(옵션은 back 이 만든다) · `api` 에 `MCP_SERVER_URL=http://mcp:8010/mcp` |
| `.env.example` | 수정 | `MCP_SERVER_URL` · `MEETING_TOKEN_TTL_MIN` 두 줄 + 주석 |
| `app/back/tests/test_meeting_token.py` · `test_agent_options.py` · `app/mcp/tests/test_tools.py` | **신규** | §Execution 검증 항목 |
| `app/back/service/meeting_batch_service.py` · `meeting_finalize_service.py` | 수정(호출부만) | `gateway.run(..., meeting_token=…)` 인자 추가. **프롬프트 · 입력은 건드리지 않는다**(WORK-010 · 011 · 012) |

- Domain / schema note: 리비전 **1건**(`0007`). `meeting` 쪽 스키마 변경 없음

## Domain / Schema

| Entity | 역할 |
|---|---|
| `auth_session` | `kind='meeting'` 행 = 회의별 단명 토큰. **원문 컬럼** · 회의당 하나 · 회전 없음 · `revoked_at` 안 찍음 · 폐기 = DELETE |
| `meeting` | 읽기만 — `start()` 가 토큰 행을 만들 때 `meeting_id` 로 참조 |

- 상태 / invariant: `account.md` **A-13**(발급 · 원문 컬럼 · 검증 · 폐기 = 행 삭제 · 왜 무상태 JWT 가 아닌가) · **A-7 은 `refresh` 행에만** · `database/README.md` §1 `meeting ||--o| auth_session` · §4 인덱스 · `system/README.md` **불변식 13 · 14**(AI 는 MCP 로만 · 권한은 백엔드) · **SYS-12 · SYS-15 · SYS-16**
- Migration 필요 여부: **있음** — `0007_auth_session_meeting_token`(`down_revision = "0006_job"`)
- SPEC 에 환류해야 하는 변경: 없음. 도구 표 · 토큰 규칙은 SPEC-007 §4 · DEC-003 §8 · A-13 이 이미 정본

## Dependency

| Consumer | Interface | 설명 |
|---|---|---|
| **WORK-010 회의 시작** | `auth_service.issue_meeting_token()` · `build_codex_options(meeting_token=)` | 웜스타트 제출이 토큰 헤더와 allow list 를 얹어 나간다 |
| **WORK-011 회의 중** | 같은 빌더 · `resume` | 배치 제출도 같은 옵션. AI 가 `list_agendas` · `get_agenda` · `list_tasks` · `get_task` · `list_work_types` 를 부른다 |
| **WORK-012 회의 종료** | `auth_service.revoke_meeting_token()` | ② 종결 뒤 best-effort 폐기(행 DELETE) |
| **open-kknaks worker** | `provider_options["config"]` · `["sandbox"]` | 우리 코드가 아니다. 넘기는 값만 정한다 |

## Internal Interface Contract

외부 계약(도구 7개의 뜻 · 토큰 규칙)은 **SPEC-007 §4 · DEC-003 §8 · `account.md` A-13 · `system/README.md` §codex** 가 정본이다. 여기는 Phase 사이가 의존하는 내부 접점만 고정한다.

| 접점 | 계약 |
|---|---|
| **회의 토큰 원문** | refresh 와 같은 생성기(랜덤 32바이트 · urlsafe). **`auth_session.meeting_token` 에 원문으로 저장**(회의당 하나 · 사용자 확정). 제출부(웜스타트 · 배치 · 최종)가 `get_meeting_token(meeting_id)` 로 읽어 옵션 빌더에 넘기고 `-c mcp_servers.tm.http_headers={Authorization="Bearer <원문>"}` 에 실린다. **로그 · 응답 · `MeetingDetail` 에는 나오지 않는다**(정적 검사) |
| **`resolve_bearer(token)`** | ① `decode_access_token` 성공 → `AccountContextDTO(account_id, meeting_id=None)` ② 실패 → `find_meeting_token(token)`(원문 일치 · 만료 제외) → 있으면 `(account_id, meeting_id)` ③ 둘 다 없으면 `UnauthorizedError("token_expired")` — **응답은 지금과 하나**(거부 사유를 흘리지 않는다) |
| **회의 범위 — allowlist**(2026-09-07 검수 F-1 · D-7 코디 확정) | 회의 토큰(`ctx.meeting_id` 있음)으로 200 이 되는 표면은 **여섯뿐** — `GET /api/meetings/current` · `GET /api/meetings/current/tasks` · `GET /api/meetings/{meeting_id}`(토큰의 회의만) · `GET /api/tasks/{task_id}` · `GET /api/work-types` · `GET /api/auth/session`. **그 밖은 메서드 불문 404**(목록 · jobs · 쓰기 · 문서함 · 캘린더 · 하위 조회 전부). 판정은 `deps.py require_context` **한 곳**, 허용 표면은 (method, path) 상수 목록 하나. `detail` 은 리소스 무언급 「찾을 수 없습니다」 · `code=not_found` |
| **`build_codex_options()` 출력** | `provider_options["config"]` = 아래 목록(순서 고정 · 테스트가 문자열로 비교). `provider_options["sandbox"]="read-only"`(새 세션). 다른 어디서도 `-c` 를 만들지 않는다 |
| **MCP 서버 키** | `mcp_servers.tm` — 키 이름 `tm` 하나. `enabled_tools` 는 접두 없이 도구 이름만 |
| **MCP 도구 ↔ REST** | `get_meeting` → `GET /api/meetings/{meeting_id}`(토큰의 회의) · `get_account` → `GET /api/profile` · `list_agendas` → 상세의 `agendas.human` + `agendas.ai` 를 `{id, title, state, track, sourceAgendaId}` 로 · `get_agenda(id)` → 상세에서 그 안건 + `lines[]`(`kind` · `content` · `detail` · `taskId`) · `list_tasks(projectId?)` → `GET /api/tasks?projectId=`(무소속은 `none`) · `get_task(id)` → `GET /api/tasks/{id}` · `list_work_types` → `GET /api/work-types`(`description` 포함). **MCP 가 회의 id 를 인자로 받지 않는다** — 토큰이 회의를 안다(back 이 `ctx.meeting_id` 로 판정). `get_meeting` 이 부르는 `{meeting_id}` 는 **back 이 토큰으로 채우는 전용 표면 `GET /api/meetings/current`** 하나를 더한다(회의 토큰 전용 · JWT 로는 404) |
| **폐기** | `revoke_meeting_token(meeting_id)` = `DELETE … WHERE kind='meeting' AND meeting_id=?`. 0건이어도 예외 없음(best-effort). 호출 자리는 WORK-012 |

`config` 목록(테스트가 이 순서 그대로 비교한다 — **문자열 하나라도 다르면 실패**):

```text
features.shell_tool=false
web_search="disabled"
features.image_generation=false
features.apps=false
mcp_servers.tm.url="<MCP_SERVER_URL>"
mcp_servers.tm.http_headers={Authorization="Bearer <token>"}
mcp_servers.tm.enabled_tools=["get_meeting","get_account","list_agendas","get_agenda","list_tasks","get_task","list_work_types"]
mcp_servers.tm.tools.get_meeting.approval_mode="approve"
… (7개 전부)
```

## Execution

### Phase 1 — `auth_session(kind='meeting')` · 발급 · 검증 · 폐기 (백엔드)

- **Status**: DONE
- **설명**: 토큰의 실체를 만든다. 이게 서야 MCP 서버가 부를 REST 가 「누구의 어느 회의」를 안다.
- **작업**:
  - [ ] 리비전 `0007` — `kind` · `meeting_id` · 부분 인덱스 · CHECK. `downgrade`
  - [ ] `security.py` 생성기 · `config.py` `meeting_token_ttl_min`
  - [ ] `auth_session_repository` 4함수 · `auth_service` 4함수 · `AccountContextDTO`
  - [ ] `deps.py` — `require_account` 가 `resolve_bearer` 경유(JWT 는 DB 안 봄) · `require_context`
  - [ ] 회의 라우터 범위 검사 · `GET /api/meetings/current` · 쓰기 표면 404 · 업무·설정 조회는 그대로
  - [ ] `tests/test_meeting_token.py`
- **검증**:
  - [ ] `alembic upgrade head` → `downgrade -1` → `upgrade` 왕복. 기존 refresh 행이 `kind='refresh'` 로 남는다
  - [ ] `issue_meeting_token` 이 돌려준 원문으로 `GET /api/meetings/current` → 200 그 회의. 다른 회의 `GET /api/meetings/{other}` → **404**. `POST /api/meetings/{id}/lines` → **404**. `GET /api/tasks` → 200(계정 범위)
  - [ ] 그 토큰이 `decode_access_token` 에서 실패하고, 세션 JWT 는 `find_meeting_token` 에 없다 — **서로 대신 못 한다**. `get_meeting_token(meeting_id)` 가 `/start` 뒤 같은 원문을 돌려준다(두 번째 제출이 이걸 쓴다)
  - [ ] 만료 지난 행 · `revoke` 뒤 → `401 token_expired`(응답 하나)
  - [ ] `revoke_meeting_token` 두 번 → 예외 없음. A-7 재사용 감지가 회의 토큰에 **안 걸린다**(refresh 세션이 끊기지 않는다)
  - [ ] **정적 검사**: 토큰 원문이 `MeetingDetail` · 로그 포맷 문자열 · 응답 스키마에 0건(grep 결과를 완료 증거에)
  - [ ] `pytest` 전체 통과(`make test` — 순서 의존 없음) · 남의 회의 토큰으로 어느 표면이든 404
- **완료 증거**: `orchestration/work/docs-v1/work009-phase4-evidence.md`(워커 JSONL 발췌 · 도구 밖 0건 · 토큰 대조 · allowlist 200/404 · revoke 뒤 401) · 검수 `work009-review-report.md`(FAIL 1 · WARN 7 → 전부 수정 `work009-review-fixes.md`) · `make test` 564 passed · `app/mcp` 40 · compose 5 healthy

### Phase 2 — `app/mcp/` 서버 · 도구 7개 · compose (백엔드)

- **Status**: DONE
- **설명**: codex 가 우리 데이터를 읽는 유일한 길. **얇아야 한다** — 판정 · 가공 · 캐시가 여기 있으면 두 번째 게이트가 된다(MF-4 위반).
- **작업**:
  - [ ] `app/mcp/` 패키지 — `pyproject` · `server.py`(Streamable HTTP) · `tools.py`(7개) · `Dockerfile`
  - [ ] 헤더 전달 — 요청의 `Authorization` 을 그대로 back 으로. 없으면 back 의 401 을 그대로 돌려준다
  - [ ] compose `mcp` 서비스 · `api` 에 `MCP_SERVER_URL` · `.env.example`
  - [ ] `app/mcp/tests/test_tools.py` — 대역 back(httpx `MockTransport`)으로 도구 7개 ↔ REST 경로·쿼리 대응
- **검증**:
  - [ ] `docker compose up` 에 `db · redis · api · worker · mcp` 다섯이 뜬다. `mcp` 헬스가 `api` 를 기다린다
  - [ ] Phase 1 토큰으로 MCP `list_agendas` 호출(curl 또는 MCP 클라이언트) → 사람 안건 + AI 안건 둘 다 · `track` 필드 있음. `get_agenda(id)` → `lines[]` 에 `kind` · `content` · `detail` · `taskId`. `list_work_types` → `description` 있음
  - [ ] 남의 회의 토큰 · 만료 토큰 → 도구 결과에 401/404 가 **그대로** 드러난다(빈 배열로 대체하지 않는다)
  - [ ] **정적 검사**: `app/mcp/` 가 `app/back` 을 import 하지 않는다 · DB 드라이버 의존 0건 · 쓰기 HTTP 메서드(POST/PATCH/DELETE) 호출 0건(grep)
  - [ ] 도구 이름 7개가 `system/README.md` §Components 표와 글자 그대로 같다
- **완료 증거**: `orchestration/work/docs-v1/work009-phase4-evidence.md`(워커 JSONL 발췌 · 도구 밖 0건 · 토큰 대조 · allowlist 200/404 · revoke 뒤 401) · 검수 `work009-review-report.md`(FAIL 1 · WARN 7 → 전부 수정 `work009-review-fixes.md`) · `make test` 564 passed · `app/mcp` 40 · compose 5 healthy

### Phase 3 — codex 옵션 빌더 · allow list · 헤더 토큰 (백엔드)

- **Status**: DONE
- **설명**: MF-3 · 4 가 코드가 되는 자리. **한 함수**가 새 세션과 resume 양쪽의 옵션을 만든다.
- **작업**:
  - [ ] `build_codex_options(meeting_token=)` — `config` 목록(§Internal Interface 순서 그대로) · `sandbox="read-only"` · `resume` 유지
  - [ ] `AgentGateway.run(meeting_token=)` · 대역 게이트웨이 시그니처
  - [ ] `meeting_batch_service` · `meeting_finalize_service` 호출부 — `auth_service.get_meeting_token(meeting_id)` 로 읽어 전달. `None`(없음 · 만료)이면 제출하지 않는다(세션 없음과 같은 취급 — MF-70). **프롬프트 · 입력은 건드리지 않는다**
  - [ ] `tests/test_agent_options.py`
- **검증**:
  - [ ] 새 세션 옵션에 `config` **14 줄**(내장 4 + url + headers + enabled_tools + 툴별 approval 7)이 **정확한 문자열 · 순서**로 있고 `sandbox="read-only"` 가 있다. resume 옵션에도 같은 `config` 가 있고 `sandbox` 는 없다
  - [ ] `enabled_tools` 에 `tm.` 접두가 없다 · `approval_policy` 키가 어디에도 없다(«user cancelled» 함정)
  - [ ] **정적 검사**: `provider_options` · `"config"` · `mcp_servers` 문자열을 만드는 곳이 `build_codex_options` **한 함수**뿐(grep)
  - [ ] `pytest` 전체 통과. 기존 `test_meeting_batch` 가 옵션 인자 추가로만 바뀌고 동작은 그대로
- **완료 증거**: `orchestration/work/docs-v1/work009-phase4-evidence.md`(워커 JSONL 발췌 · 도구 밖 0건 · 토큰 대조 · allowlist 200/404 · revoke 뒤 401) · 검수 `work009-review-report.md`(FAIL 1 · WARN 7 → 전부 수정 `work009-review-fixes.md`) · `make test` 564 passed · `app/mcp` 40 · compose 5 healthy

### Phase 4 — 실물 통합 확인 (백엔드 · 앱 창 없이 curl + 워커 로그)

- **Status**: DONE
- **설명**: 워커 로그로 **도구 밖 호출 0건**과 **도구가 실제로 불린다**를 본다. 프롬프트는 옛것이라도 토큰 · allow list · MCP 경로는 여기서 검증된다.
- **작업**:
  - [ ] 회의 하나 생성 → `/start` → 웜스타트 제출이 나가고 워커 로그에 `-c mcp_servers.tm.*` 가 보인다
  - [ ] 워커에서 codex 에게 「list_agendas 를 불러라」 수준의 확인 프롬프트를 한 번 던져(임시 · 커밋 안 함) 도구 호출 이벤트(`mcp_tool_call`)가 로그에 남는다
- **검증**:
  - [ ] 워커 로그의 도구 호출이 **우리 7개 밖 0건**(`command_execution` · `web_search` 0건)
  - [ ] 도구 호출 헤더의 토큰이 `auth_session(kind='meeting').meeting_token` 과 같고 **사용자 세션 JWT 와 다르다**(DB 로 확인)
  - [ ] `revoke_meeting_token` 뒤 같은 토큰으로 도구 호출 → 401 이 도구 결과에 드러난다
  - [ ] SPEC-007 §6 AC 「codex 설정에 `enabled_tools` 7개 · `features.apps=false` · `sandbox="read-only"` · 도구별 `approval_mode="approve"` 가 있고, 워커 로그에 우리 도구 밖의 도구 호출이 0건이다. 도구 호출 헤더의 토큰이 사용자 세션 토큰과 다르다」 — **이 항목이 이 work 의 Done 이다**
- **완료 증거**: `orchestration/work/docs-v1/work009-phase4-evidence.md`(워커 JSONL 발췌 · 도구 밖 0건 · 토큰 대조 · allowlist 200/404 · revoke 뒤 401) · 검수 `work009-review-report.md`(FAIL 1 · WARN 7 → 전부 수정 `work009-review-fixes.md`) · `make test` 564 passed · `app/mcp` 40 · compose 5 healthy

## Pre-deploy Check

- [ ] `.env` 에 `MCP_SERVER_URL` · `MEETING_TOKEN_TTL_MIN` — 없으면 기동 실패(비밀값은 아니지만 compose 안 주소라 기본값을 두지 않는다)
- [ ] compose 다섯 서비스 기동 순서 — `api` → `mcp` → `worker`
- [ ] 리비전 `0007` 적용 뒤 기존 refresh 로그인이 그대로 된다(A-7 회귀 없음)
- [ ] 토큰 원문이 **back 로그** · 응답에 없다(워커 JSONL 에는 `-c` 문자열로 남는다 — 설계상 그렇다. Phase 4 실측이 그걸 본다)
- [ ] codex 를 올릴 때 새로 붙은 내장 도구를 확인한다(deny list 가 없다 — `system/README.md` §codex)

## Rollback

- **스키마**: `alembic downgrade -1` — `kind='meeting'` 행이 먼저 지워진다(downgrade 가 DELETE 한다). refresh 행은 영향 없음
- **백엔드**: `deps.py` 의 회의 토큰 갈래와 `GET /api/meetings/current` 를 걷어내면 MCP 가 전부 401 이 된다 — 배치는 도구 없이 돌아 **컨텍스트가 빈다**(WORK-011 전이면 옛 프롬프트라 아직 동작한다)
- **compose**: `mcp` 서비스 제거. `api` 의 `MCP_SERVER_URL` 을 비우면 옵션 빌더가 기동 실패로 알린다
- 부분 revert 시: Phase 3 만 되돌리면 도구 · 토큰은 있되 codex 가 안 부른다(무해). **Phase 1 은 단독으로 되돌리지 않는다** — 2 · 3 이 전제한다

## Done Criteria

- [x] 모든 Phase 가 `DONE` 또는 `SUPERSEDED` 다
- [ ] **SPEC-007 §6 AC 의 codex 설정 항목 1개 + 「도구 호출 헤더의 토큰 ≠ 세션 토큰」이 실측 캡처로 완료 증거에 있다**
- [ ] 정적 검사 4종(토큰 원문 노출 0 · 옵션 빌더 단일 · `app/mcp` 의 back import 0 · 쓰기 메서드 0) 결과가 붙어 있다
- [ ] 남의 회의 · 만료 · 폐기 토큰이 어느 표면에서든 401/404 라는 테스트가 있다
- [ ] `make test` 전체 통과 · `Errors` 줄 0
- [ ] `30-work/README.md` 갱신

## Open Issues

- ~~#1 토큰 발급 단위~~ → **닫힘(2026-09-07 저녁 사용자 확정): 회의당 하나 · 원문을 `auth_session.meeting_token` 컬럼에 둔다.** 제출마다 발급하는 것은 오버헤드. 해시만 두던 규칙은 refresh 행에만 남는다(A-13 · ERD 갱신)
- **워커 질문 2건(2026-09-07 · 코디 답)** — ① `get_account` 는 **`GET /api/auth/session`**(`AccountSummary`)을 부른다. `/api/profile` 은 SPEC-010 미구현 — 그 work 가 열리면 대응을 바꾼다 ② `list_work_types` 는 `/api/work-types` 응답을 **그대로 통과**시킨다. `description` 은 WORK-013 이 컬럼을 더하면 자동으로 실린다(MCP 가 필드를 고르지 않는다)
- **워커 질문 3(2026-09-07 · 코디 답)** — `list_tasks` 는 화면용 `GET /api/tasks`(오늘 기본값 · `projectId` int)를 쓰지 않는다. **회의 토큰 전용 `GET /api/meetings/current/tasks?projectId=`** 를 더 연다 — 기간 없음 · 삭제 제외 · 생략 = 회의 프로젝트(무소속이면 무소속) · `none` = 무소속 · **사후 검사(M-15)와 같은 repository 조회**(AI 가 보는 목록 = 서버가 검사하는 목록). JWT 로는 404. SPEC-007 §4 도구 표에 코디가 환류한다
- MCP 서버 포트 `8010` · 키 `tm` · TTL 330분은 이 work 가 정한 값이다. 계약이 아니라 설정이고 env 로 바뀐다
- `GET /api/meetings/current` 는 이 work 가 여는 **회의 토큰 전용 표면**이다 — SPEC 에 없다. 도구가 회의 id 를 모르는 설계(토큰이 안다)에서 나온 것이라 SPEC-007 §4 도구 표에 한 줄 환류가 필요하면 코디가 한다

## Related

- SPEC: SPEC-007 §4 · §5 · §6 (frontmatter `links.specs`) · DEC-003 §2 · §8 · DEC-001 §4
- Architecture: `system/README.md` §codex 설정 · 불변식 13~15 · `backend/README.md` §4 · §5-2 · §9 · §11 · `database/domains/account.md` A-13
- Work: WORK-002 · 006 · 007(선행) · WORK-010 · 011 · 012(소비)
