# mediness-app 조사 — codex 워커 연결 · MCP 사용 패턴

- 조사자: research 워커 (read-only)
- 일자: 2026-09-02
- 대상: `/Users/kknaks/git/harness_works/mediness-app` (**사내 레포** — 아래에는 구조·설정 키·
  파일:줄만 옮긴다. 도메인 지식·프롬프트 본문·비밀값·데이터는 옮기지 않는다. 사내 툴 이름도
  개별로 나열하지 않고 「카탈로그 툴 N종」으로만 적는다)
- 대조: `ontology-demo/app/back/service/chat/`(우리 레포의 기존 open-kknaks 채팅) ·
  `ontology-demo/app/mcp/`(우리 FastMCP) · `ontology-demo/app/back/docker-compose.yml` ·
  `ontology-demo/app/ontology-agent/`(현 스캐폴드)
- 조사 대상 레포는 수정하지 않았고 코드를 실행하지 않았다.

## 요약 (먼저 읽을 5줄)

1. mediness 의 codex 결선은 **`open-kknaks worker run` 데몬 컨테이너 1개 + Redis 브로커 + HTTP
   MCP 서버 1개**의 3각 구조다. codex CLI 도 인증도 **이미지에 굽지 않고** 호스트 준비본을
   ro 마운트 + `PATH` 선두 + `CODEX_HOME` 볼륨으로 붙인다.
2. codex 에 MCP 를 알리는 방법이 **두 가지**이고, 대화형 경로는 **설정 파일을 안 쓴다** —
   제출 페이로드의 `provider_options.config` 에 반복 `-c` TOML 오버라이드로 서버 URL·헤더·
   `enabled_tools`·툴별 `approval_mode` 를 **매 turn** 실어 보낸다.
3. 응답 소비는 **`AgentClient.stream(task_id)` 이벤트를 DB row 로 폴딩**하는 백그라운드
   consumer 다. 타임아웃 축이 두 개(전체 상한 = 바깥 `asyncio.wait_for`, idle 상한), 종료
   마감은 `broker.get_task()` 의 최종 status·result 로 한 번 더 확정한다.
4. **우리 레포에 이 패턴이 이미 이식돼 있다** — `app/back/service/chat/` 이 mediness
   `landing_chat/` 의 축소판이고, `app/back/docker-compose.yml` 에 전용 큐 워커(`chat-worker`)
   + `mcp` 서비스가 이미 서 있다. ontology-agent 는 **새로 발명할 것이 거의 없다**.
5. 우리 쪽에서 달라져야 하는 것은 4가지뿐이다 — **큐/네임스페이스 분리(`ontology`)**,
   **MCP 서버가 back REST 래퍼가 아니라 SQLite 마스킹 뷰 직독**, **인증이 사용자 JWT 가 아니라
   turn 불투명 토큰(우리 기존 방식 유지)**, **FE 가 WS 가 아니라 2초 폴링**(SPEC-003).

---

## §1 codex 워커 기동

### 1.1 compose 서비스 정의

`mediness-app/docker-compose.yml:104-161` — `worker` 서비스 한 개가 전부다.

| 항목 | 값 | 근거 |
|---|---|---|
| 빌드 | `context: ./back` · `dockerfile: Dockerfile.worker` | `docker-compose.yml:117-119` |
| 레플리카 | **1 고정** | `docker-compose.yml:115-116` — 이유는 코드 주석에 명시: codex 세션이 **워커 로컬 파일**(`$CODEX_HOME/sessions/…`)이라 방↔세션 1:1 이 그 워커에 묶인다. 두 번째 레플리카가 같은 방의 다음 turn 을 집으면 resume 이 「세션 없음」으로 떨어지고 문맥이 조용히 초기화된다 |
| env_file | back 컨테이너와 **같은 `.env` 공유** | `docker-compose.yml:121` |
| redis | `REDIS_URL: redis://redis:6379/0` | `docker-compose.yml:123` |
| MCP URL | `MEDINESS_MCP_URL: http://mcp:28081/mcp` | `docker-compose.yml:125` |
| 큐 목록 | `OPEN_KKNAKS_QUEUE` = **쉼표 구분 4개**, 대화형 큐를 **맨 앞**에 | `docker-compose.yml:130` |
| `PATH` | CLI 마운트 경로를 선두에 | `docker-compose.yml:134`, 로컬 override `docker-compose.local.yml:9` |
| `CODEX_HOME` | `/root/.codex` (이미지 ENV 와 같은 값을 compose 에도 다시 박음 — 볼륨 경로와 눈으로 대조되게) | `docker-compose.yml:139`, 이미지 `back/Dockerfile.worker:70` |
| 볼륨 | 세션 영속 2종(claude/codex) — `mediness_codex_sessions:/root/.codex` | `docker-compose.yml:143-147`, 선언 `:283-285` |
| depends_on | `redis`(healthy) + `mcp`(started) | `docker-compose.yml:148-152` |
| healthcheck | `codex --version` | `docker-compose.yml:156-161` — 이유: codex 를 못 찾으면 태스크를 **집은 뒤에야** 실패해 사용자에겐 죽은 채팅으로 보인다. 기동 시점에 unhealthy 로 드러나는 편이 낫다 |

**큐 순서가 의미를 갖는다** — `docker-compose.yml:126-130` 주석: open-kknaks 의 dequeue 가
큐 목록을 **순서대로** 훑으므로, 대화형 큐를 배치 큐 뒤에 두면 헤드-오브-라인 지연이 생긴다.
동시 실행은 워커의 concurrency 가 잡는다.

### 1.2 이미지 — CLI 를 굽지 않는다

`back/Dockerfile.worker`:

- base `python:3.12-slim` + `ca-certificates` 만 (`:31-39`). curl 도 뺐다(`:35-36`).
- **open-kknaks 를 PyPI 로 정확 핀** — `pip install "open-kknaks==2.1.2"` (`:59`).
  back 의 `pyproject.toml:28` 이 `open-kknaks>=2.1.1` 로 짝을 이룬다. 주석(`:55-58`)이
  「back 핀과 **lockstep** — 한쪽만 올리면 broker payload 계약이 갈린다」를 못 박았다.
- **codex CLI 는 설치하지 않는다**(`:61-65`). 호스트에 정적 musl 바이너리를 준비해 두고
  `<host>/.codex-tools:/codex-tools:ro` 로 마운트한 뒤 `PATH` 선두로 잡는다. 이유는
  open-kknaks 가 CLI 를 **`shutil.which("codex")` 로만** 찾기 때문이다(전용 env 없음, `:19-20`).
  ⚠ npm 배포본(`@openai/codex`)은 쓰지 말라고 명시 — 네이티브 ELF 가 아니라 node 스크립트라
  PATH 에 node 런타임이 얽힌다(`:21-23`).
- **인증은 굽지 않는다**(`:24`, `:69`). `CODEX_HOME` 아래로 런타임 주입만 한다. 로컬 검증은
  `docker-compose.local.yml:16` 이 호스트 `~/.codex/auth.json` **파일 하나만** ro 로 얹는다
  (세션 디렉터리를 통째로 내주지 않는다 — `docker-compose.local.yml:13-14`).

### 1.3 기동 커맨드 + MCP config 생성

`back/worker-entrypoint.sh` (30줄):

```
1. umask 077 → /tmp/mcp-config.json 을 heredoc 으로 생성        (:13-26)
   { "mcpServers": { "<key>": { "type":"http", "url":"$MEDINESS_MCP_URL",
                                "headers": { "X-Internal-Auth": "$INTERNAL_AUTH_SECRET" } } } }
2. exec open-kknaks worker run --broker "$REDIS_URL" --queues "$OPEN_KKNAKS_QUEUE"   (:28-30)
```

⚠ **이 공용 config 파일은 claude 큐 전용이다.** `Dockerfile.worker:78-79` 주석이 명시:
대화형(codex) turn 은 발화별 MCP 설정을 **반복 `-c` 오버라이드**로 실어 보내므로 이 파일을
쓰지 않는다. 즉 codex 경로에서 이 entrypoint 는 사실상 데몬 기동만 한다.

### 1.4 모델 지정 위치

- **compose 에 모델이 없다.** 모델은 **제출 페이로드**(`task.model`)로 간다.
- 값의 SoT 는 back 설정 — `back/app/config.py:125` `landing_chat_model: str = "gpt-5.6-terra"`,
  짝인 `back/app/config.py:134` `landing_chat_reasoning_effort: str = "low"`.
- 주석에 실측 함정 2개가 박혀 있다(`config.py:107-138`):
  - **정식 표기만 유효**하다. 축약형·다른 계열명·서버 내부 해석명은 metadata 조회 실패로
    **400** 이고, 에러 문구가 인증 문제처럼 읽히지만 원인은 언제나 **ID 표기**다.
  - **모델과 effort 는 짝**이다. 허용 effort 목록이 CLI 가 아니라 **모델별**로 갈린다.
    `none` 은 금지(추론이 꺼지면 자연어를 MCP 툴로 연결하는 판단 자체가 죽는다는 실측),
    하한은 `low`.
- 빈 문자열이면 **아예 넘기지 않는다** — `--model` 자체가 안 붙어 CLI 기본 모델이 쓰인다
  (`submission.py:81-83`, `:213-214`). `""` 를 넘기면 `--model ""` 이 되므로 「미지정」은
  반드시 `None` 이어야 한다.

---

## §2 open-kknaks 결선

### 2.1 클라이언트 생성 — 매 호출 connect/close

`back/app/services/landing_chat/runtime.py:37-58`:

```python
from open_kknaks import AgentClient, RedisBroker        # lazy import (:39)
broker = RedisBroker(url=settings.redis_url)
await broker.connect()
try:
    client = AgentClient(broker=broker)
    return await client.submit(prompt=…, queue=…, provider=…, model=…,
                               provider_options=…, options=…, metadata=…)
finally:
    await broker.close()
```

- **lazy import** 로 의존 미설치 환경을 보호한다(`:38`).
- 취소도 같은 모양 — `AgentClient(broker).cancel(task_id)` (`runtime.py:61-87`).
- 소비 경로는 별도로 broker 를 열고 `client.stream(task_id, timeout=…)` 을 돈다
  (`consumer.py:865-869`, `:907`).

우리 레포도 같은 모양이되 **namespace 인자가 하나 더** 있다 —
`ontology-demo/app/back/service/chat/runtime.py:57` `RedisBroker(url=…, namespace=settings.ai_namespace)`.

### 2.2 제출 페이로드에 실리는 것 (계약 6항)

`back/app/services/landing_chat/submission.py:1-49` 머리 주석이 계약을 6항으로 못 박고,
같은 파일이 그 조립을 전부 갖는다.

| # | 항목 | 값 · 위치 |
|---|---|---|
| 1 | provider | `"codex"` 고정 — `submission.py:212` |
| 2 | 세션 바인딩 | 방에 세션 id 가 있으면 `options["resume"] = {"mode":"session","session_id":…}`, 없으면 키 자체를 안 실음 — `submission.py:205-207`. **방 하나 = 세션 하나** |
| 3 | reasoning + 시간 상한 | `model_reasoning_effort` 는 `-c` 로, 상한은 `options["timeout_sec"]` — `submission.py:123`, `:204`. codex 에 **turn 수 제한 키가 없어서**(실측) 상한 축이 시간 하나뿐이다 |
| 4 | sandbox | `provider_options["sandbox"] = "read-only"` — `submission.py:64`, `:163` |
| 5 | MCP allowlist | `-c` 오버라이드로 매 turn — `submission.py:121-136` |
| 6 | 시스템 프롬프트 | **프롬프트 본문 앞에 붙여서** 보냄 — `submission.py:192-196` |
| — | model | `settings.landing_chat_model or None` — `submission.py:214` |
| — | metadata | `{room_id, turn_id}` 관측용 — `submission.py:220` |
| — | git 검사 우회 | `provider_options["skip_git_repo_check"] = True` — `submission.py:165`. resume 에도 **반드시** 실어야 한다(워커 이미지에 git 이 없어 「Not inside a trusted directory」로 막힘, `:39-40`) |

**시스템 프롬프트를 provider_options 로 못 보내는 이유**(`submission.py:183-186`): codex 어댑터가
`system_prompt` provider option 을 **지원하지 않는다** — 허용 목록에 없어 `Unsupported codex
provider_options` 로 제출 자체가 거부된다. 그래서 프롬프트 본문 앞에 블록으로 붙인다. 블록
순서는 `[시스템 프롬프트] → [참조 문맥] → [사용자 발화]` 이고 구분자는 `\n\n---\n\n`
(`submission.py:192-196`). 참조가 없으면 그 자리는 **아예 비운다**(「참조 없음」 같은 문장을 넣지 않음).

### 2.3 resume 분기는 앱이 갖지 않는다

`submission.py:150-167` — 신규·resume 에 **같은 값**을 넘긴다. `codex exec resume` 이 못 받는
옵션(`--sandbox` 등)은 **open-kknaks 어댑터가 `CODEX_RESUME_UNSUPPORTED_OPTIONS` 로 제출 전에
떨궈** 준다. 앱이 한 번 더 가르면 같은 규칙이 두 곳에 산다는 것이 명시 근거(`:36-37`, `:156-157`).
`--model` 은 resume 도 받으므로 그대로 나간다(`:28-30`).

### 2.4 제출 순서 — 커밋 뒤에 제출, 제출 뒤에 소비자

`runtime.py:1-20` + `:110-132`:

1. 라우터는 **요청 트랜잭션을 커밋한 뒤** `submit_and_consume(turn_id)` 하나만 부른다.
2. 커밋보다 먼저 큐에 넣으면 워커가 즉시 집어 소비자가 **아직 보이지 않는 row** 를 찾다 실패한다.
3. 제출 성공 → **그 태스크 전용 소비자**를 `asyncio.create_task` 로 띄운다(`:131`).
4. 제출 실패 → turn 을 `failed`(`WORKER_UNAVAILABLE`)로 마감하고 소비자는 띄우지 않는다
   (`turns.py:455-457`, `:463-469`). 접수(202)는 이미 확정된 사실이라 응답을 뒤집지 않는다.
5. `asyncio.create_task` 반환을 **모듈 레벨 set 에 보관**한다 — 안 붙들면 GC 가 가져가 조용히
   사라진다(`runtime.py:16-19`, `:105-107`).

### 2.5 제출 직전에 매 turn 다시 계산하는 것

`back/app/services/landing_chat/turns.py:390-461` — 순서가 곧 계약이다:

```
시스템 프롬프트 재조립(매 turn) → tool allowlist 재계산(매 turn)
  → turn 전용 MCP 토큰 발급 → build_submission → submit
```

- allowlist 는 요청자의 capability 집합에서 계산하고(`:414-424`), **제출 시점 목록을 turn row 에
  감사 기록으로 남긴다**(`:426`) — 나중에 「왜 그 툴을 못 썼나」를 되짚는 근거.
- `qualified_tool_name`(`catalog.py:65-75`)은 **서버 id 를 앞에 붙이지 않는다** —
  `mcp_servers.<id>.enabled_tools` 는 그 서버 안에서의 툴 이름을 받고, 서버 id 는 키 경로가
  이미 담고 있다. ⚠ 표기가 틀리면 **에러가 아니라 조용히 「툴 0개」** 가 된다.

---

## §3 MCP 연동

### 3.1 codex 가 MCP 를 아는 두 경로

| 경로 | 방식 | 쓰는 곳 |
|---|---|---|
| **A. 설정 파일** | entrypoint 가 `/tmp/mcp-config.json` 을 굽고, 제출 시 `mcp_config=<path>` 로 넘겨 CLI 가 `--mcp-config` 로 읽는다 | 배치(claude) 큐 전용. `worker-entrypoint.sh:14-26`, `back/app/config.py:95-97` (`mediness_mcp_config_path`), compose `docker-compose.yml:62` |
| **B. 발화별 `-c` 오버라이드** | **태스크별 설정 파일이 없다.** 제출 페이로드 `provider_options["config"]` 에 TOML 오버라이드 문자열 리스트를 실어 보낸다 | 대화형(codex) 경로 — `submission.py:86-147`, `:166` |

**우리가 따라야 할 것은 B** 다. 이유는 `mcp_token.py:55-56` 에 있다 — turn 토큰이 **codex
프로세스 인자로만 흐르고 디스크에 남지 않는다**(발화별 설정 파일 자체가 없으므로).

### 3.2 `-c` 오버라이드 키 목록 (전부 `--strict-config` 수용 확인됨)

`submission.py:121-147`. 값은 TOML 로 파싱되므로 **문자열은 따옴표로 감싼다**.

```
model_reasoning_effort=<effort>
approval_policy="never"
mcp_servers.<key>.url="<streamable http url>"
mcp_servers.<key>.http_headers={Authorization="Bearer <turn token>"}
mcp_servers.<key>.enabled_tools=["toolA", "toolB", …]
mcp_servers.<key>.tools.<toolName>.approval_mode="approve"     # allowlist 개수만큼 1줄씩
features.shell_tool=false
web_search="disabled"
features.image_generation=false
features.apps=false
```

**Streamable HTTP URL 주입 지점**은 `mcp_servers.<key>.url` 한 줄이다. 값의 SoT 는
`back/app/config.py:144` `landing_chat_mcp_url = "http://mcp:28081/mcp"` (워커 컨테이너 기준
주소). 서버 키는 `config.py:142` `landing_chat_mcp_server_key`이며, **allowlist 계산이 훑는
서버 key 와 반드시 같아야 한다** — 갈리면 조용히 「툴 0개」다(`config.py:140-142` 주석).

**승인 축이 둘이라는 것이 이 절의 핵심 함정**(`submission.py:94-106`, `:44-48`):

- `approval_policy="never"` 는 「안 물어보고 **실패 처리**」이지 허용이 아니다. 비대화(exec)에서
  MCP 툴 호출이 「user cancelled」로 죽던 원인이 이것이다.
- 허용하는 축은 `mcp_servers.<id>.tools.<tool>.approval_mode="approve"` (codex 0.117.0+).
  우선순위는 **툴별 > 서버 기본 > auto**.
- **툴별로 거는 이유**: 서버 기본으로 걸면 나중에 카탈로그에 툴이 늘 때 그것까지 자동으로 열린다.
- 한때 쓰던 `bypass_approvals_and_sandbox=True` 는 **걷어냈다** — 승인과 sandbox 를 **함께** 꺼서
  에이전트가 컨테이너 셸을 열 수 있었다. 지금은 승인(per-tool)과 파일 접근(`sandbox=read-only`)이
  분리된 축이다.

**표면 축소**(`submission.py:108-119`, `:137-146`):

- `features.shell_tool=false` 로 shell/exec_command/write_stdin 을 통째로 뺀다.
- `features.apps=false` 가 필요한 이유가 특히 중요하다 — codex 가 **우리가 설정하지 않은** MCP
  surface 를 붙인다(실측에서 세션에 `mcp__codex_apps__` 27종). allowlist 는 우리 서버만 가리키므로
  그 밖의 surface 를 **아예 못 막는다**.
- ⚠ 안 되는 것 전수: `features.unified_exec=false` 는 shell 을 끄는 키가 **아니고**, `tools.*` 는
  범용 denylist 가 **아니며**, `apply_patch` 단독 차단 키는 **없다**(read-only sandbox 가 실효 차단).
- ⚠ `enabled_tools` 가 **빈 배열이면 그 서버 툴이 하나도 안 열린다** — 버그가 아니라 fail-closed 계약.
- ⚠ 툴 이름에 점(`.`)이 있으면 TOML quoted key(`tools."a.b"`)가 필요하다.

**로그 위생**: `submission.py:224-229` `redact_config_overrides()` 가 `http_headers` 줄을
`<redacted>` 로 바꾼다 — 그 줄에 Bearer 원문이 들어 있다.

### 3.3 MCP 서버 쪽 (수신 측)

`mediness-app/mcp/app/server.py`:

- FastMCP + **Streamable HTTP** — `mcp = FastMCP(name, transport_security=…, stateless_http=True)`
  (`:108`), ASGI 조립은 `_streamable_app = mcp.streamable_http_app()` (`:1603`) 을
  `Mount("/", …)` 로 얹는다(`:1618`). SDK 기본 경로가 `/mcp` 다.
- **`stateless_http=True` 인 이유**(`:98-107`): stateful 이면 세션이 **프로세스 인메모리**에 살고,
  배포로 pod 이 교체되면 기존 session id 의 GET/POST 가 SDK 세션 계층에서 404 를 맞는다. 이 서버의
  툴은 전부 back REST 의 얇은 래퍼라 세션에 얹을 상태가 없다.
- **lifespan 을 바깥에 명시해야 한다**(`:1599-1610`): inner Starlette 의 자체 lifespan 은
  `Mount` 로 감싸면 자동 발화하지 않아, 안 박으면 `POST /mcp` 가
  `RuntimeError("Task group is not initialized")` 로 죽는다.
- **DNS rebinding 보호** — `TransportSecuritySettings(enable_dns_rebinding_protection=True,
  allowed_hosts=…, allowed_origins=…)` (`:92-96`). compose 가 워커가 붙는 Host 를 명시로 넣는다
  (`docker-compose.yml:178`).
- **인증은 dual-auth** (`JwtContextMiddleware`, `:1521-1597`):
  1. `X-Internal-Auth` 헤더가 시크릿과 같으면 **service identity** 로 통과(배치 워커 경로).
     write 툴은 `_reject_if_service()`(`:362`)가 `service:` prefix 를 거부하므로 이 경로는 read-only.
  2. 아니면 `Authorization: Bearer <jwt>` 를 back 에 물어 검증 → ContextVar 세팅.
     실패는 401 + `WWW-Authenticate`(RFC 9728), back 호출 자체 실패는 503.
  - `/health` + well-known 2종은 인증 면제(`:1454-1462`).

### 3.4 툴 호출 결과가 응답 스트림에 나타나는 모양

`AgentClient.stream(task_id)` 이 주는 이벤트 종류 — `consumer.py:953-1058` 의 분기가 곧 목록이다:

| `event.type` | 실린 필드 | 백엔드 처리 |
|---|---|---|
| `init` | `session_id` | 세션 id 확정 · turn `pending → running` (`consumer.py:961-969`, `:245-262`) |
| `text` | `text`(**delta**) | 누적해 assistant row 갱신 (`:971-985`, `:264-268`) |
| `tool_use` | `tool_use_id` · `tool_name` · `tool_input` | 툴 row upsert + 인자 요약 (`:987-1008`) |
| `tool_result` | `tool_use_id` · `tool_result` · `tool_is_error` | 같은 row 에 결과·소요시간·출처 접기 (`:1010-1047`) |
| `progress` | `description` | usage 에 적재 + 브로드캐스트 (`:1049-1053`) |
| `cost` | `cost_usd` | **집계만**, 브로드캐스트 안 함 (`:1055-1058`) |
| `thinking` | — | **버린다** — 적재도 브로드캐스트도 없음 (`:957-959`) |

`tool_use_id` 로 use↔result 를 짝짓는다. 이 필드는 open-kknaks 2.1.0+ 에서 들어왔고 2.1.1 이
codex 어댑터에서도 채운다(`Dockerfile.worker:44-48`).

---

## §4 소비·폴딩 — 응답을 DB/API 상태로 접기

### 4.1 소비자 진입 (`consumer.py:836-861`)

```python
redis = …
if not await acquire_consumer_lock(redis, task_id):   # 중복 소비자 차단 (:87-101)
    return
try:
    await asyncio.wait_for(_consume(…), timeout=settings.landing_chat_timeout_sec)
except TimeoutError:      → _finalize_out_of_band(code="TURN_TIMEOUT")
except Exception:         → _finalize_out_of_band(code="WORKER_UNAVAILABLE")
finally:
    release_consumer_lock() · _revoke_turn_token() · _drain_after()
```

⚠ **바깥 `asyncio.wait_for` 가 유일한 안전망이다**(`:848-850`). 라이브러리의 `stream(timeout=)`
는 **이벤트가 하나도 없으면 발동하지 않는다**(deadline 검사가 `async for` 본문 안에 있다는 실측).
그래서 타임아웃 축이 둘이다 — 전체 상한 `landing_chat_timeout_sec`(`config.py:107`)와 무응답
상한 `landing_chat_idle_timeout_sec`(`config.py:148`).

### 4.2 스트림 루프 (`consumer.py:864-927`)

```python
broker = RedisBroker(url=…); await broker.connect(); client = AgentClient(broker=broker)
async with session_factory() as db:
    turn, room = await _load(db, turn_id)
    if turn.status not in (PENDING, RUNNING): return      # 완료 이벤트 재수신 무시 (:876-881)
    if replay: await folder.reset_for_replay(); await db.commit()
    async for event in client.stream(task_id, timeout=…):
        if await _is_canceled(db, turn.id): break          # 매 이벤트마다 DB 재조회 (:908-911)
        await _fold_one(db, folder, bus, event, turn=turn)
        await db.commit()                                  # 이벤트 1건 = 커밋 1회
    task = await broker.get_task(task_id)                  # 2차 안전망 (:923)
    await _close_from_task(db, folder, bus, task, turn=turn)
```

- **적재 먼저, 브로드캐스트 나중**(`:954`). 브로드캐스트 payload 는 이벤트 원본을 다시 가공하지
  않고 **적재 결과(fold)** 를 그대로 싣는다 — 스트림으로 본 화면과 재입장으로 복원한 화면이
  갈리면 그건 두 개의 진실이라는 것이 명시 근거(`:110-114`, `:127-131`, `:993-994`).
- 없는 값은 **키 자체를 싣지 않는다**(빈 문자열·빈 배열 금지) — `:1002-1006`, `:1025-1032`.
- 취소 감지는 **컬럼 하나만 스칼라로 재조회**한다(`:930-950`) — 취소는 다른 세션에서 커밋되므로
  소비자가 들고 있는 객체엔 안 보인다. 루프가 이벤트마다 커밋해 매 회 새 트랜잭션이 열린다.

### 4.3 마감 (`consumer.py:1061-1099`)

`broker.get_task(task_id)` 의 최종 상태로 확정한다:

| `task.status` | 처리 |
|---|---|
| `done` | `task.result` 로 최종 본문 확정 → turn `DONE` + `TURN_COMPLETED` |
| `cancelled` | turn `CANCELED` + `TURN_CANCELED` |
| 그 외 / `None` | `turn.error_code` = `WORKER_UNAVAILABLE` / `TURN_TIMEOUT`, turn `FAILED` + `TURN_FAILED`. `task.error` 는 **500자 잘라서** 저장 |

**최종 usage 는 여기서 덮는다**(`:1068-1071`) — 스트림의 `cost`/`progress` 는 **중간 관측치**라
마지막 값이 총계가 아니다(실측: 30툴 turn 인데 `cost_usd:0` 으로 굳음). 태스크 최종 usage 가
유일한 총계다.

마감 직전에 `turn` 을 **refresh** 하고 상태를 다시 본다(`:1063-1066`) — 그 사이 취소됐거나 이미
마감됐으면 완료 이벤트를 무시한다.

### 4.4 실패·재시도·복구

- **재시도 자동화가 없다.** 실패는 turn 상태(`FAILED` + `error_code`)로 표현하고 사용자가 다시
  보낸다. 코드는 `WORKER_UNAVAILABLE` · `TURN_TIMEOUT` 두 가지만 쓴다.
- **out-of-band 마감**(`:1102-1119`)은 **부분 텍스트를 지우지 않는다**.
- **기동 시 스윕 2단 복구**(`recover_pending_turns`, `:1157-…`, 호출 `back/app/main.py:166-168`):
  ① `task_id` 가 있으면 **재부착 재생**(소비자 재기동, `replay=True`) ② 없으면(제출 전에 죽음)
  재생할 스트림이 없으므로 **실패로 마감**.
- **재생(replay) 규율**(`:229-243`, `:162-166`): assistant 부분 텍스트만 비우고 툴 row 는
  `tool_use_id` 로 멱등 upsert 라 지우지 않는다. 재생 중엔 **latency 를 재지 않는다** — 이벤트가
  Redis Stream 에서 연달아 쏟아져 시간차가 「툴이 걸린 시간」이 아니라 「스트림을 읽은 시간」이다.
- **turn 토큰 폐기**는 best-effort(`:1122-1134`) — 실패해도 자연 만료로 흡수, turn 을 뒤집지 않는다.
- **취소 신호의 실제 효과**가 `runtime.py:61-76` 에 실측으로 정리돼 있다: dequeue 전이면 실행 자체가
  안 되고, running 이면 2.1.1 까지는 프로세스가 안 죽었다(2.1.2 가 `_watch_for_cancel` 로 고침 —
  `Dockerfile.worker:49-53`). 어느 쪽이든 소비자는 이벤트 공백 1초 지점에서 드레인하고 끝난다.

### 4.5 API 로 나가는 모양

mediness 는 **WS 브로드캐스트**(`RoomBroadcaster.emit`)로 내보낸다 — `turn.started` · `turn.text`
· `turn.tool_use` · `turn.tool_result` · `turn.progress` · `turn.completed` · `turn.failed` ·
`turn.canceled` · `room.context_reset` (`consumer.py` 전역, 이벤트 상수는 `landing_chat/events.py`).

**우리는 여기가 다르다** — SPEC-003 §4 는 **2초 폴링**이고, 우리 레포의 기존 채팅도 폴링이다
(`ontology-demo/app/back/service/chat/runtime.py:117-120` 주석: 「폴링에 재큐잉 경로가 없어…」).
폴딩 로직 자체는 동일하고 **출구만 WS → 폴링 조회**로 바뀐다.

---

## §5 `app/ontology-agent` 적용 체크리스트

### 5.0 전제 — 이미 우리 레포에 있는 것 (재발명 금지)

| 있는 것 | 위치 | 상태 |
|---|---|---|
| open-kknaks 워커 이미지 | `app/back/Dockerfile.worker` | `open-kknaks==2.1.2` 핀 · `CODEX_HOME` · `CMD` 가 `--broker/--namespace/--queues/--work-dir/--concurrency` 로 이미 파라미터화 (`:25`, `:29`, `:40`) |
| 전용 큐 채팅 워커 + MCP 서비스 | `app/back/docker-compose.yml:101-141` | `mcp` + `chat-worker`(큐 `chat`, 별도 `CODEX_HOME=/root/.codex-chat`, 별도 세션 볼륨, 원장 마운트 **없음**) |
| 제출 조립 | `app/back/service/chat/submission.py` | mediness 계약 6항이 그대로 이식됨 — sandbox/approval 축 분리, `features.apps=false` 까지 (`:52-58`, 머리 주석 `:31-45`) |
| 제출·소비자 배선 | `app/back/service/chat/runtime.py:50-67`, `:156-` | `RedisBroker(url, namespace)` + `AgentClient.submit` + `start_turn` |
| 이벤트 폴딩 소비자 | `app/back/service/chat/consumer.py` | `wait_for` 바깥 상한(`:396-410`) · `stream` 루프(`:437`) · `_close_from_task`(`:474`) · `recover_pending_turns`(`:508`) |
| turn 토큰 | `app/back/service/chat/turn_token.py` | **불투명 난수 + sha256 저장**. JWT 기계를 안 만든 이유가 머리 주석에 있다 |
| FastMCP 서버 | `app/mcp/app/server.py` | `stateless_http=True`(`:65`) · `Mount("/")`(`:301`) · lifespan 명시(`:290-`) · `TurnTokenMiddleware`(`:254-`) |
| ontology-agent 스캐폴드 | `app/ontology-agent/config.py:22-28` | `redis_url` · `ai_namespace=ontology_demo` · `ai_queue=ontology` · `ai_provider=codex` · `ai_model=gpt-5.6-terra` · `ai_timeout_sec=180` **이미 선언돼 있다** |

### 5.1 compose 추가분 (큐 = `ontology` 분리)

`app/back/docker-compose.yml` 에 서비스 2개를 더한다. **기존 `worker`·`chat-worker` 는 한 줄도
건드리지 않는다**(레포의 기존 규율 — `docker-compose.yml:99` 주석).

- `ontology-mcp` — `build: ../mcp`(별도 이미지가 필요하면 `app/ontology-agent/` 아래에 새 MCP
  패키지), `MCP_ALLOWED_HOSTS: ontology-mcp,ontology-mcp:28081`, 포트 **비노출**.
  ⚠ 우리 MCP 는 SQLite 마스킹 뷰를 읽으므로 **DB 파일 ro 마운트**가 필요하다(§5.3).
- `ontology-worker` — `dockerfile: Dockerfile.worker`, 환경:
  ```
  REDIS_URL=redis://redis:6379/0
  AI_NAMESPACE=ontology_demo        # ONTOLOGY_AI_NAMESPACE 와 같은 값
  AI_QUEUE=ontology                 # ⚠ back 의 ai_queue 와 반드시 일치
  AI_CWD=/app                       # 파일을 안 만지므로 빈 디렉토리면 된다
  CONCURRENCY=${ONTOLOGY_WORKER_CONCURRENCY:-2}
  CODEX_HOME=/root/.codex-ontology  # 채팅·파이프라인 세션과 격리
  PATH=/claude-tools/node/bin:/usr/local/bin:/usr/bin:/bin
  ```
  볼륨: node 마운트 ro · `ontology-codex-sessions:/root/.codex-ontology` ·
  `auth.json` **파일 하나만** ro. **원장(`/ledger`) 마운트 없음**.
  healthcheck `codex --version`. `depends_on: redis(healthy), ontology-mcp`.
- 볼륨 선언에 `ontology-codex-sessions:` 추가.
- ⚠ **레플리카 1 고정.** 세션이 워커 로컬 파일이라 2개 이상이면 resume 이 깨진다
  (mediness `docker-compose.yml:108-114`). 우리도 대화 resume 을 쓰면 같은 제약이다.

### 5.2 env 키 (ontology-agent `ONTOLOGY_` prefix)

`app/ontology-agent/config.py` 에 더할 것 — 이미 있는 6개(`redis_url`·`ai_namespace`·`ai_queue`·
`ai_provider`·`ai_model`·`ai_timeout_sec`) 위에:

| 키 | 기본값 제안 | 근거 |
|---|---|---|
| `ai_reasoning_effort` | `"low"` | 모델과 **짝**. `none` 금지(툴 연결 판단이 죽는다) — mediness `config.py:128-134` |
| `mcp_url` | `http://ontology-mcp:28081/mcp` | `-c mcp_servers.<key>.url` 에 그대로 박힘 |
| `mcp_server_key` | `"ontology"` | allowlist 계산이 훑는 key 와 **반드시 동일** |
| `turn_token_ttl_sec` | `900` | 우리 기존 채팅과 같은 축 |
| `ai_idle_timeout_sec` | `120` | 무응답 상한 — 전체 상한과 **별개 축** |
| `demo_password` | (없음 — 주입 전용) | SPEC-003 §4 `ONTOLOGY_DEMO_PASSWORD`. 값을 코드·문서·기본값에 넣지 않는다 |

**핀 lockstep 규칙**: `app/ontology-agent/pyproject.toml` 의 open-kknaks 핀과
`Dockerfile.worker:25` 의 `==2.1.2` 가 **같은 버전을 가리켜야 한다**. 한쪽만 올리면 broker
payload 계약이 갈린다(`back/Dockerfile.worker:55-58`).

### 5.3 MCP 서버 기동 방식

- FastMCP + Streamable HTTP, `stateless_http=True`, `Mount("/", streamable_http_app())`,
  **lifespan 명시**, `TransportSecuritySettings(allowed_hosts=…)`. 우리 `app/mcp/app/server.py`
  가 이미 그 모양이므로 **그 파일을 골격으로 복사**한다.
- 인증은 **우리 방식 유지** — `TurnTokenMiddleware`(헤더 없는 호출만 거부, 유효성은 뒤에서 확인).
  mediness 의 JWT family + dual-auth 는 **가져오지 않는다**: 저기는 툴 권한이 사람마다 갈리고
  audit `sub` 를 채워야 했지만, 우리는 **공용 비밀번호 1개 · 익명 방문자**(DEC-005 D2)라 토큰이
  답할 질문이 「지금 도는 turn 인가」 하나뿐이다.
- ⚠ **여기가 mediness 와 가장 크게 갈리는 지점**: mediness MCP 툴은 전부 **back REST 의 얇은
  래퍼**라 세션에 얹을 상태가 없다. 우리 온톨로지 도구 4종(SPEC-002)은 **SQLite 마스킹 뷰를
  직접 읽는다.** 선택지 둘:
  - (A) MCP 가 DB 파일을 ro 로 직독 — 왕복이 짧지만 DB 경로가 두 컨테이너에 걸린다.
  - (B) MCP 가 ontology-agent 의 내부 API 를 부르는 래퍼 — mediness·우리 기존 채팅과 같은 모양이고
    「화면과 도구가 같은 수치를 본다」(SPEC-003 §5)가 **구조로 강제된다**.
  → **(B) 권장.** SPEC-003 AC-5(`/api/kpi/series` = `query_kpi` 오차 0)가 (B)면 자동으로 성립한다.

### 5.4 코드로 그대로 가져올 패턴

1. `submission.py` 전체 구조 — `-c` 오버라이드 목록·sandbox·approval 축 분리·
   `features.{shell_tool,apps,image_generation}` off·`web_search="disabled"`·
   `skip_git_repo_check=True`·모델 `None` 처리·`redact_config_overrides`.
2. `runtime.py` 의 **커밋 뒤 제출 → 제출 뒤 소비자 → task 참조 set 보관** 3단.
3. `consumer.py` 의 **바깥 `wait_for` 상한 + `stream` 루프 + 이벤트별 폴딩 + `get_task` 2차 마감**.
4. `recover_pending_turns` 2단 복구(재부착 재생 / 제출 전 사망은 실패 마감)와 기동 훅.
5. **적재 먼저, 브로드캐스트(=응답 필드) 나중** + 「없는 값은 키를 싣지 않는다」 규율.
6. `turn_token.py` 의 불투명 토큰 + sha256 저장 + 마감 시 컬럼 NULL 폐기.
7. 「토큰이 닿는 값을 로그 인자로 만들지 않는다」 규율(마스킹 함수를 두지 않는다).

### 5.5 우리 상황에서 **달라져야** 하는 것

| # | 항목 | 이유 |
|---|---|---|
| 1 | **출구가 WS 가 아니라 폴링** — `steps`·부분 `content` 를 message row 에 접고, `GET /api/chat/conversations/{id}` 가 그것을 읽는다 | SPEC-003 §4 «2초 폴링», AC-8. 폴딩 로직은 동일, `RoomBroadcaster.emit` 자리만 사라진다 |
| 2 | **`steps` 기록 주체가 백엔드** — `{tool, args_summary, duration_ms, called_at}`, `args_summary` 는 서버가 만들고 길이 제한 | SPEC-003 §4 Data Contract. mediness `_summarize_tool_arguments`(`consumer.py:670`)·`_summarize`(`:553`)가 그대로 쓸 수 있는 자리 |
| 3 | **allowlist 가 정적이다** — 도구 4종(`query_kpi`·`query_layer`·`trace_ontology`·`get_definition`) 고정 튜플. capability 계산·카탈로그 DB 가 없다 | SPEC-002 §4. 우리 기존 채팅의 `TOOL_ALLOWLIST` 상수 방식(`service/chat/submission.py:60-`)과 같다 |
| 4 | **인증이 사용자 JWT 가 아니다** — turn 불투명 토큰 + 접속 게이트는 env 비번 1개 | DEC-005 D2, SPEC-003 §4. mediness 의 JWT family·rotation·revocation 캐시는 전부 불필요 |
| 5 | **답변이 자유 텍스트가 아니라 구조화 객체** — `answer`·`premise_correction`·`used_edges`·`citations`·`unknowns` | SPEC-005 §4. mediness 는 `task.result` 문자열을 그대로 본문으로 쓴다(`consumer.py:1075-1076`). 우리는 그 문자열을 **파싱·검증**하는 단계가 하나 더 필요하다 — 스키마 위반 시 처리는 SPEC-005 OQ-5 미결 |
| 6 | **세션 resume 을 쓸지 결정 필요** | SPEC-003 은 `conversation`/`message` 만 정하고 codex 세션 재사용을 정하지 않았다. 쓰면 레플리카 1 고정 + 세션 볼륨이 따라오고, 안 쓰면 매 turn 새 세션이라 이전 대화를 프롬프트에 다시 실어야 한다(우리 기존 채팅 `runtime.py:110-112` 가 「세션이 살아 있으면 같은 것을 두 번 싣지 않는다」로 처리) |
| 7 | **관계 지식을 프롬프트에 넣지 않는다** | SPEC-005 §5 · AC-보조 2. mediness 의 `SystemPromptAssembler` 는 조직 문맥을 프롬프트에 싣는 구조라 **그 부분은 가져오면 안 된다**. 시스템 프롬프트는 도구 사용 규칙 + 답변 형식만 |
| 8 | **원장 마운트 없음 · `AI_CWD` 는 빈 디렉토리** | 우리 `chat-worker` 와 같은 규율(`docker-compose.yml:132-133`). 데이터는 MCP 도구로만 온다 |

### 5.6 착수 전에 닫아야 할 것

1. **큐 이름 3곳 일치** — `ontology-agent/config.py:ai_queue` · compose `AI_QUEUE` ·
   (있다면) 워커 청취 목록. 어긋나면 태스크가 **영원히 pending** 이다(mediness `config.py:100-102`
   가 같은 함정을 「유령 큐」로 기록).
2. **`mcp_server_key` 2곳 일치** — `-c mcp_servers.<key>` 와 allowlist 표기. 어긋나면 에러가
   아니라 **조용히 툴 0개**.
3. **모델 × effort 조합 실측** — `gpt-5.6-terra` + `low` 가 레퍼런스 통과 조합.
4. **codex CLI·인증 준비물** — 홈서버에 node/codex 준비본과 `~/.codex/auth.json`(우리 compose 는
   이미 `/home/kknaks/.nvm/…/v24.19.0` 와 `/home/kknaks/.codex/auth.json` 을 쓴다). ontology 워커도
   같은 것을 쓰되 `CODEX_HOME` 만 분리한다.
5. **open-kknaks 핀 lockstep** — ontology-agent pyproject ↔ Dockerfile.worker.

---

## 조사 한계

- 코드를 실행하지 않았고 컨테이너를 띄우지 않았다. 「실측」이라 적은 것은 전부 **대상 레포의
  주석이 기록한 실측**이며, 이 조사가 재현한 것이 아니다.
- open-kknaks 패키지 소스 자체(`AgentClient`·`RedisBroker`·codex 어댑터의 `_build_command`)는
  열지 않았다 — 두 레포의 사용부와 주석에 적힌 계약만 옮겼다. `CODEX_RESUME_UNSUPPORTED_OPTIONS`
  동작·`stream(timeout=)` 의 deadline 위치는 그 주석의 진술이다.
- 사내 도메인 지식(툴 카탈로그 내용·프롬프트 본문·조직 모델·데이터)은 의도적으로 옮기지 않았다.
  필요하면 위 파일:줄로 직접 열어 보는 편이 낫다.
- mediness 의 k8s 배포본(`charts/mediness`, 별도 인프라 레포)은 이 레포에 없어 보지 못했다 —
  compose 기준 구성만 정리했다.
