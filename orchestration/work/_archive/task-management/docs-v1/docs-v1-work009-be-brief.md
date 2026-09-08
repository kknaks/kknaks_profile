# [backend] WORK-009 Phase 1~4 — MCP 서버 · 회의별 단명 토큰 · codex allow list

너는 **task-management `backend` 워커**다.
역할 문서: `/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/orchestration/roles/task-management/backend/role.md`

## 0. 어디서 무엇을 보나

**코드 워크트리** — `/Users/kknaks/orca/workspaces/task_management/docs-v1` (브랜치 `kknaksss/docs-v1`, HEAD `aa98518`).
**코드 워커는 한 번에 하나만 돈다.** WORK-001~008 이 전부 들어와 있다. 미커밋 변경은 `tauri.conf.json` 하나뿐 — 건드리지 마라.

문서는 전부 **코디 워크트리 절대경로 · 읽기 전용**이다.

```
/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/para/projects/summer-star/task-management/
  30-work/work-009-mcp-token.md                ← 네 빌드 계획. Phase 1~4 전부. Code Surface 표 · Internal Interface Contract 가 구현 규격
  20-spec/spec-007-meeting-live.md §4          ← 「AI 도구 7개」 표 · 「웜스타트」 표의 도구·토큰 행 · §6 AC codex 설정 항목
  10-decision/decision-003-meeting-notes.md    ← §2 AI 데이터 접근 · §8 「AI 도구 연결」(배치 · 토큰 행)
  40-architecture/system/README.md             ← §codex 설정(allow list 실측 표 · 함정) · Components MCP 행 · 흐름 ③ · 불변식 13~15
  40-architecture/backend/README.md            ← §4 디렉토리(app/mcp) · §5-2 · §9 · §11 env
  40-architecture/database/domains/account.md  ← A-7(refresh 만) · **A-13**(회의 토큰 규칙 넷)
  40-architecture/database/README.md           ← §1 ERD auth_session · §4 인덱스
/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/reference/2026-09-06-task-management-app/Meeting flow.md
                                               ← 결정 원본. §1-4 MF-2·3·4 · §1-5 MF-68·69(원문 컬럼)·70. 계약과 부딪히면 이게 이긴다
```

## 1. 범위 — Phase 1 · 2 · 3 · 4 전부

```
Phase 1  auth_session(kind='meeting') 리비전 0007 · 발급/조회/검증/폐기 · require_account 두 번째 갈래 · 회의 범위 404 · GET /api/meetings/current
Phase 2  app/mcp/ 별도 패키지 — Streamable HTTP MCP 서버 · 도구 7개(REST 얇은 래퍼 · 헤더 전달) · Dockerfile · compose `mcp` 서비스
Phase 3  build_codex_options(meeting_token=) — provider_options["config"] 에 -c 목록 · sandbox=read-only · 호출부 3곳 토큰 전달
Phase 4  실물 — compose 다섯 서비스 기동 · 워커 로그로 도구 밖 호출 0건 · 헤더 토큰 ≠ 세션 JWT
```

**프론트 · 웜스타트 프롬프트 · 배치 입력 · 종료 파이프라인은 이 work 가 아니다**(WORK-010 · 011 · 012). 옵션 빌더 호출부에 인자 하나 더하는 것 외에 `meeting_batch_service` · `meeting_finalize_service` 의 프롬프트·입력·검증 코드를 건드리지 마라.

## ⛔ 2. 이미 있는 것 — 다시 만들지 마라

```
core/security.py         generate_refresh_token() 이 있다. 회의 토큰 생성기는 같은 방식(secrets.token_urlsafe(32))으로 하나 더한다.
                         **해시 함수는 만들지 않는다** — 회의 토큰은 원문 저장(A-13 · MF-69 보강)
api/deps.py              require_account 가 JWT 만 본다. **JWT 경로는 그대로 두고**(DB 안 봄) 실패했을 때만 회의 토큰 원문 조회를 더한다.
                         응답은 지금처럼 401 token_expired 하나 — 거부 사유를 흘리지 않는다
repository/auth_session_repository.py   create · find_by_token_hash · revoke · revoke_all_for_account 가 있다. 회의 토큰용 4함수를 더한다.
                         **revoke 계열을 회의 토큰에 쓰지 마라** — 회의 토큰 폐기는 행 DELETE 이고 revoked_at 을 찍지 않는다
integrations/agent.py    build_codex_options() 가 **옵션을 만드는 유일한 함수**다. 여기에만 -c 목록을 더한다. 다른 곳에서 provider_options 를 만들면 반려
service/meeting_service.py start()   L515~. 지금은 load_warm_start_context → commit → warm_start 순서다(옛 설계 · WORK-010 이 고친다).
                         **이 work 는 전이 UPDATE 와 같은 트랜잭션 안에 issue_meeting_token() 한 줄만 더한다.** 나머지 순서를 건드리지 마라
docker-compose.local.yml db · redis · api · worker 넷. mcp 를 더한다. worker 의 마운트·PATH 를 바꾸지 마라
open-kknaks 2.1.2        app/back/.venv/.../open_kknaks/worker/codex_adapter.py — provider_options["config"] 가 list[str] 이면 -c 로 하나씩 나간다.
                         **resume 에서도 config 는 살아남고 sandbox 는 버려진다**(CODEX_RESUME_UNSUPPORTED_OPTIONS). open-kknaks 는 고치지 않는다
```

## 3. 계약 — 이대로 제공한다

- **도구 7개 이름** — `get_meeting` · `get_account` · `list_agendas` · `get_agenda` · `list_tasks` · `get_task` · `list_work_types`. 글자 그대로. SPEC-007 §4 표가 각 도구가 **주는 필드**를 정한다 — 그 필드만.
- **도구 ↔ REST 대응** — WP §Internal Interface Contract 표. `get_meeting` 은 **회의 토큰 전용 표면 `GET /api/meetings/current`** 를 부른다(이 work 가 연다 · JWT 로는 404). MCP 는 회의 id 를 인자로 받지 않는다 — 토큰이 회의를 안다.
- **토큰** — `auth_session(kind='meeting')` 행 · **회의당 하나** · **원문을 `meeting_token` 컬럼에** · `/start` 때 INSERT · 제출부는 `get_meeting_token(meeting_id)` 로 읽는다 · 폐기 = 행 DELETE(함수만 만든다 — 호출은 WORK-012). `refresh_token_hash` 는 meeting 행에서 NULL.
- **회의 범위** — 회의 토큰으로 온 요청은 `AccountContextDTO(account_id, meeting_id)`. 회의 라우터의 `{id}` 가 다르면 404. **쓰기 표면은 회의 토큰으로 전부 404.** 업무 · 유형 · 프로필 조회는 계정 범위 그대로.
- **`config` 목록** — WP §Internal Interface Contract 의 문자열 · 순서 그대로. 테스트가 문자열로 비교한다. 키는 `mcp_servers.tm`. `enabled_tools` 에 접두 없음. `approval_policy` 키 금지.
- **env** — `MCP_SERVER_URL`(api 가 옵션에 싣는 mcp 주소 · 기본값 없음) · `MEETING_TOKEN_TTL_MIN`(기본 330) · mcp 컨테이너의 `MCP_BASE_URL`(api 주소) · `MCP_PORT`(8010).

## 4. 먼저 읽을 핵심 파일

```
app/back/models/account.py L74~95         AuthSession
app/back/core/security.py                 토큰 생성기 · decode_access_token
app/back/api/deps.py                      require_account
app/back/service/auth_service.py          _issue_tokens · refresh · logout — 같은 결로
app/back/repository/auth_session_repository.py
app/back/integrations/agent.py            build_codex_options · OpenKknaksGateway.run
app/back/service/meeting_service.py L515~ start()
app/back/service/meeting_batch_service.py  gateway.run 호출부(warm_start · _run_once · _run_final_once)
app/back/service/meeting_finalize_service.py  gateway.run 호출부(_attempt_integration)
app/back/alembic/versions/0006_job.py      리비전 형식 · down_revision
app/back/tests/conftest.py · test_auth.py  대역 · 픽스처 방식
docker-compose.local.yml · app/back/Dockerfile.worker · .env.example
app/back/.venv/lib/python3.12/site-packages/open_kknaks/worker/codex_adapter.py   config/sandbox 처리(읽기만)
```

## 5. allowed_paths — 이 밖은 건드리지 마라

```
app/back/                  (ORM · 리비전 · service · repository · api · integrations · tests · config)
app/mcp/                   (신규 패키지 전체)
docker-compose.local.yml
.env.example
```

문서 경로(`para/` · `orchestration/`) · `app/front/` · `tauri.conf.json` · open-kknaks 패키지는 **금지**.

## 6. 구현 단계

WP §Execution Phase 1 → 2 → 3 → 4 순서 그대로. Phase 마다 그 Phase 의 검증 항목을 통과시킨 뒤 다음으로.

- Phase 1 끝 — `alembic upgrade head` 왕복 · 회의 토큰으로 `GET /api/meetings/current` 200 · 다른 회의 404 · 쓰기 404 · 세션 JWT 와 서로 대신 못 함 · 만료/폐기 → 401
- Phase 2 끝 — `docker compose up` 에 다섯 서비스 · Phase 1 토큰으로 MCP 도구 7개 호출 결과가 REST 응답과 같다 · `app/mcp` 의 back import 0 · 쓰기 메서드 0
- Phase 3 끝 — 옵션 빌더 테스트(문자열 · 순서 고정) · resume 에 `sandbox` 없음 · `provider_options` 만드는 곳 한 함수
- Phase 4 끝 — 워커 로그에 `-c mcp_servers.tm.*` · `mcp_tool_call` 이벤트 · 우리 도구 밖 호출 0 · 헤더 토큰 = `auth_session.meeting_token` ≠ 세션 JWT

## 7. 범위 제약 — 하지 말 것

- **프롬프트 · 배치 입력 · 종료 파이프라인을 고치지 않는다.** 옛 설계 그대로 둔다 — WORK-010 · 011 · 012 몫
- **MCP 서버에 판정 · 가공 · 캐시를 두지 않는다.** REST 응답을 그대로 돌려준다. 401/404 도 그대로 드러낸다(빈 배열로 대체 금지)
- **쓰기 도구를 만들지 않는다.** 7개 전부 조회
- **회의 토큰을 해시하지 않는다.** 원문 컬럼. refresh 는 지금처럼 해시
- **`revoked_at` 을 회의 토큰에 찍지 않는다.** 폐기 = DELETE
- **`approval_policy` 를 쓰지 않는다.** 툴별 `approval_mode="approve"`
- `except Exception` · 임의 재시도 · 조용한 기본값 금지. 설계 밖 예외는 전파
- 커밋 · push · PR 금지. **문서를 고치지 않는다** — 틀렸으면 보고

## 8. 검증

```bash
cd app/back && uv run alembic upgrade head && uv run alembic downgrade -1 && uv run alembic upgrade head
cd app/back && make test            # 전체 스위트 — 순서 의존 없음 · Errors 줄 0
cd app/mcp  && uv run pytest -q
docker compose -f docker-compose.local.yml up -d && docker compose -f docker-compose.local.yml ps   # db redis api worker mcp
```

정적 검사 4종(grep 결과를 보고에 붙여라):
1. 토큰 원문이 로그 포맷 문자열 · 응답 스키마 · `MeetingDetail` 에 0건
2. `provider_options` · `"config"` · `mcp_servers` 를 만드는 곳이 `build_codex_options` 한 함수
3. `app/mcp/` 에서 `from app.back` · `import models` · DB 드라이버 0건
4. `app/mcp/` 에서 POST/PATCH/DELETE 호출 0건

막히면 30분 넘기지 말고 §9 (2) 방식으로 물어라. 특히 **codex 0.147 이 `-c mcp_servers.tm.url` 로 Streamable HTTP MCP 를 붙이는지** 실물에서 안 되면 바로 보고 — 그건 결정이지 네가 고칠 게 아니다.

---

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다. preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.

- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_98a33032-2134-4bf9-ac48-e9df737f9b8f --from term_fd9fc1ce-619d-4f87-b218-10dfaefaa275 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "backend 완료: WORK-009 Phase 1~4" \
  --body "변경 파일 목록 / Phase 별 구현 요약 / 검증 결과(수치 · 정적 검사 4종 grep) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_98a33032-2134-4bf9-ac48-e9df737f9b8f \
  --text "[worker_done] backend 완료 — WORK-009 MCP · 토큰 · allow list. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_98a33032-2134-4bf9-ac48-e9df737f9b8f --text "[질문] backend: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
