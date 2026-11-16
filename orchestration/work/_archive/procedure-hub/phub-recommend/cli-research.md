---
type: research
id: cli-research
title: "hub-evals 를 CLI(Claude Code CLI · Codex CLI)로 돌릴 수 있나"
product: procedure-hub
feature: phub-recommend
created_at: 2026-10-30
brief: orchestration/work/phub-recommend/phub-recommend-cli-research-brief.md (추가 절 두 줄 포함)
---

# hub-evals 를 CLI 로 돌릴 수 있나

> 조사만 했다. 유료 호출이나 실제 질문 실행은 하지 않았다. 근거로 쓴 것은 `--help` · `--version` · `codex debug models` · `codex features list` · 로그인 상태(계정 칸은 가림) · 공식 문서 · 참고 설계 코드(읽기만) · hub-evals 코드와 기존 실행 기록(`reference/2026-10-30-hub-evals/runs/_archive/`)이다.
> 「확인 필요」라고 적은 칸은 무료로는 확인할 수 없는 것이다. 실물 1회 호출이 있어야 닫힌다(§7 U 표).

## 0. 요약

| | claude-cli | codex-cli |
|---|---|---|
| 로컬 버전 | Claude Code `2.1.284` | codex-cli `0.165.0` |
| 로그인 | claude.ai OAuth · **구독 `max`** · `apiProvider: firstParty` · 셸 env 에 API 키 없음 | ChatGPT 로그인 · plan `prolite` · `auth.json` 에 API 키 없음 |
| case1 · case2(HTTP MCP 도구 루프) | **가능** — `--mcp-config` `type: "http"` | **가능** — `-c mcp_servers.<id>.url=…`(streamable HTTP) |
| case3(도구 없이 1회) | **가능** — `--tools ""` · MCP 안 붙임 | **가능** — 셸 · 웹검색 끄고 MCP 안 붙임 |
| ① 이름 뽑기(JSON schema) | **가능** — `--json-schema` → `structured_output` | **가능** — `--output-schema` + `-o` |
| ② 채점(도구 + JSON schema) | **가능** — 원장 도구 3 을 **로컬 stdio MCP** 로 감싸야 함 | **가능**(같은 조건) — 다만 사용자 말로는 채점은 Claude Opus 로만 함 |
| 첫 글자 시각(ttft) | **토큰 단위로 잴 수 있음** — `--include-partial-messages` → `stream_event` `text_delta` | **메시지 단위만** — `agent_message` 는 `item.completed` 때 통째로 옴(델타 없음). 「첫 메시지 완료 시각」으로 대신함 |
| 도구 시작 · 끝 · 왕복 | 됨(`tool_use` 블록 · `tool_result` · `num_turns`) | 됨(`item.started` · `item.completed` `mcp_tool_call`) · 왕복 수 칸은 없어 셈 |
| 토큰 | 됨(`usage` · `modelUsage`) | 됨(`turn.completed.usage` — input · cached_input · output · reasoning_output) |
| 비용 칸 | `total_cost_usd`(클라이언트 **추정**치 · 구독이어도 나옴 · 실제 청구 아님) | 없음 — 토큰만 |
| 한도 신호 | `rate_limit_event{rateLimitType: five_hour\|seven_day, utilization, resetsAt}` · `system/api_retry{error: rate_limit}` | 공식 JSONL 칸 없음 — 한도에 걸리면 `error` · `turn.failed` 메시지로 옴(문구는 확인 필요) |
| 모델 | Sonnet = `--model claude-sonnet-5-5`(별칭 `sonnet`) · Opus = `--model claude-opus-5-5`(별칭 `opus`) | **terra = `gpt-5.6-terra` 또는 `gpt-6.1-terra`**(로컬 목록에 둘 다 있음 · §3 정할 것) |

- **가능**: claude-cli 는 필요한 것 6 가지(case1 · case2 · case3 · ① · ② · 측정)가 다 된다. codex-cli 는 답 케이스 3 과 ① 이 되고, 측정은 ttft 만 메시지 단위로 줄어든다. ② 는 사용자 결정대로 Claude 만 쓴다
- **가장 큰 함정**: hub-evals `.env` 에 `ANTHROPIC_API_KEY` 가 있다. **`claude -p` 는 env 에 이 키가 있으면 구독 대신 무조건 키를 쓴다**(공식 authentication 「In non-interactive mode (`-p`), the key is always used when present」). 자식 프로세스 env 에서 이 키를 **빼지 않으면** CLI 로 돌려도 API 로 과금된다 — 지금 $10 이 나간 그 경로다
- `--bare` 는 못 쓴다. bare 는 OAuth · 키체인을 안 읽고 API 키만 받는다(공식 headless). 그래서 격리는 참고 설계처럼 플래그를 묶어서 한다(§5)

---

## 1. 우리 실험에 필요한 것을 CLI 가 다 하나

### 1-1. case1 · case2 — 로컬 Streamable HTTP MCP 도구 루프

**claude-cli**

```bash
claude -p --model claude-sonnet-5-5 --effort high \
  --system-prompt "<common.md + case1.md>" \
  --tools "" --strict-mcp-config --setting-sources "" --disable-slash-commands \
  --no-session-persistence --permission-mode bypassPermissions \
  --mcp-config '{"mcpServers":{"hub":{"type":"http","url":"http://127.0.0.1:18005/procedure-hub/raw-mcp/mcp"}}}' \
  --allowedTools "mcp__hub__raw_list mcp__hub__raw_get mcp__hub__raw_search" \
  --output-format stream-json --verbose --include-partial-messages \
  --max-budget-usd 1 \
  "<질문>"
```

- `type: "http"` 는 `claude mcp add --transport http`(help)와 같은 꼴이다. `url` 만 쓰고 `type` 을 빠뜨리면 그 서버는 **조용히 빠진다**(`system/init.mcp_server_errors[].type = url_missing_type`). 실행 앞에서 `system/init.mcp_servers[].status` 를 보고 `connected` 가 아니면 그 열을 오류로 해야 한다
- `-p` 에 `--mcp-config` 를 주면 첫 바퀴 전에 서버 연결을 `MCP_TIMEOUT`(기본 30초)까지 기다린다(공식 headless)
- 도구 이름은 `mcp__hub__<도구>` 꼴로 바뀐다. 기록 `trace.tool_calls[].tool` 에는 접두를 뗀 이름을 남긴다(참고 설계 `_MCP_TOOL_PREFIX` 와 같음)
- **도구 루프 상한**: 지금 앱 `CASE_TOOL_LOOP_MAX=12`(SPEC-006 R-2) 와 같은 칸이 2.1.284 `--help` 에는 없다(`--max-turns` 안 보임). 남는 장치는 `--max-budget-usd`(추정 $ 상한 → `subtype: error_max_budget_usd`) · 앱 쪽 타임아웃 · 프롬프트뿐이다. **「상한에 닿으면 tool_choice none 으로 마지막 답 1번」(SPEC §3-2)은 CLI 로 옮길 수 없다**(§7 막힘 B-2)
- 앱의 도구 결과 상한(`tool_result_max_bytes` 20,000 · `cap_text`)도 CLI 안에서는 앱이 끼어들 수 없다. 허브 MCP 가 결과를 스스로 줄이지 않으면 SDK 판과 입력 크기가 달라진다(B-3)

**codex-cli**

```bash
CODEX_HOME=<전용 홈> codex exec --json --color never --ephemeral --skip-git-repo-check \
  -C <임시 cwd> -s read-only --ignore-user-config --ignore-rules \
  -m <terra id> -c model_reasoning_effort="<값>" \
  -c model_instructions_file="<common.md + case2.md 파일>" -c project_doc_max_bytes=0 \
  -c features.shell_tool=false -c features.unified_exec=false -c web_search="disabled" -c tools.view_image=false \
  -c features.plugins=false -c features.skill_search=false -c features.skip_host_skill_discovery=true \
  -c 'shell_environment_policy.inherit="none"' \
  -c 'mcp_servers.hub.url="http://127.0.0.1:18005/procedure-hub/gold-mcp/mcp"' \
  -c mcp_servers.hub.required=true \
  -c 'mcp_servers.hub.default_tools_approval_mode="approve"' \
  -c mcp_servers.hub.tool_timeout_sec=60 \
  "<질문>"
```

- HTTP 지원: `codex mcp add --url <URL>`(help 「URL for a streamable HTTP MCP server」) · 설정 키 `mcp_servers.<id>.url`(공식 config-reference). 참고 설계는 stdio(`command` · `args`)만 썼으니 `url` 꼴은 새로 쓰는 것이다
- `required=true` 면 서버 시작에 실패할 때 실행이 멈춘다(config-reference) — 조용히 도구 없이 답하는 일을 막는다
- `enabled_tools` · `disabled_tools` 로 도구 목록을 자를 수 있다(참고 설계 `_mcp_overrides`)
- 도구 루프 상한 칸은 Codex 에도 없다. 타임아웃(앱) 하나뿐이다

### 1-2. case3 — 도구 없이 1회

- **claude-cli**: `--tools ""` 를 주고 `--mcp-config` 는 안 준다(+ `--strict-mcp-config` 로 사용자 MCP 도 막음). 입력 = 질문 + ③ 허브 결과 JSON + 슬롯 표(지금 앱 그대로)
- **codex-cli**: MCP 를 안 붙이고 셸 · 웹검색 · 이미지를 끈다. 다만 Codex 는 **도구가 0 개인 상태를 보장하는 칸이 없다** — `features.*` 를 끄고 나서도 남는 도구가 있는지는 실물 1회 JSONL(`item.*` 에 도구 항목이 나오나)로 확인해야 한다(U-4)
- 앞 단계(① hub_resolve · ② Jev · ③ hub_path)는 그대로 앱 코드다. Jev 는 API 그대로 둔다(브리프 · TypeSafe · 질문당 0.04 원 수준 — `pricing.py` `jev-1.14.0` 입력 $0.042/1M)

### 1-3. ① 이름 뽑기 · ② 채점

| | ① 이름 뽑기 | ② 채점 |
|---|---|---|
| 지금(SDK) | Opus 5.5 · effort low · `output_config.format` · 도구 없음 | Opus 5.5 · effort medium · 원장 도구 3(앱 안 함수 `quality/raw_tools.py`) 루프 → 마지막 구조화 출력 |
| claude-cli | `--model claude-opus-5-5 --effort low --tools "" --json-schema '<names 스키마>' --output-format json` → `structured_output` | `--model claude-opus-5-5 --effort medium --json-schema '<judge 스키마>' --mcp-config <원장 도구 stdio 서버>` · `--output-format stream-json`(도구 호출 · 근거 기록) |
| 구조화 출력 꼴 | `--json-schema` 는 합성 도구 `StructuredOutput` 으로 마지막 답을 받는다(참고 설계 `_STRUCTURED_OUTPUT_TOOL`). 스키마에 못 맞추면 `structured_output` 칸이 **없다**(공식 headless) → 그 칸 유무를 먼저 본다 | 같음 · 도구 루프와 한 실행 안에서 같이 된다 |

- **원장 도구 3 은 MCP 로 줘야 한다.** CLI 는 앱 안 Python 함수를 부를 수 없다. 길은 둘이다
  - (가) **앱 안 원장 도구를 감싼 로컬 stdio MCP 서버**(`clinic_chat/quality/raw_mcp.py` 꼴 · 공식 MCP Python SDK `FastMCP` · `RAW_DIR` 을 읽는 `raw_tools.py` 를 그대로 부름) → `--mcp-config '{"mcpServers":{"raw":{"type":"stdio","command":"uv","args":["run","python","-m","clinic_chat.quality.raw_mcp"],"env":{"RAW_DIR":"…"}}}}'`
  - (나) 허브 원장 MCP(`/raw-mcp/mcp`)를 그대로 붙임 — **SPEC-006 §5-2 W-3(채점 경로가 실험 대상 서버에 기대지 않게)과 부딪힌다**
  - 추천은 (가)다. SPEC 규칙이 그대로 지켜지고, 근거 인용 검사(`check_evidence`)도 같은 `raw_tools.py` 를 쓴다(정할 것 D-4)
- **사용자 결정(추가 절)**: 채점 = Claude CLI 로 Opus. Codex 답도 Opus 가 채점한다 → ② 는 claude-cli 한 길만 만들면 된다
- **가리기**(A · B · C 섞기 · `judge_order` · `judge_seed`)는 프롬프트를 앱이 만드니 그대로 된다

---

## 2. 측정이 되나

### 2-1. claude-cli `stream-json`(`--verbose --include-partial-messages`)

| 잴 것 | 어디서 | 비고 |
|---|---|---|
| 프로세스 시작 | 앱이 `Popen` 직전 `perf_counter` | 앱 시계 |
| 기동 끝(설정 · 인증 · MCP 연결) | 첫 줄 `system/init` 도착 시각 | `mcp_servers[].status` 도 같이 봄. `-p --mcp-config` 는 init 전에 서버를 기다림 |
| 첫 API 응답 | 첫 `stream_event` `message_start` | |
| **ttft** | 첫 `stream_event` 중 `event.delta.type == "text_delta"` | thinking 델타는 따로 옴 → 지금 정의(SPEC §4-1 「thinking 델타 제외」)와 같게 셀 수 있음 |
| 도구 시작 · 끝 | `assistant` 메시지의 `tool_use` 블록 → 다음 `user` 메시지의 `tool_result` | 참고 설계 `ClaudeEventIngest` 와 같음 · 결과 내용이 빈 채 올 때가 있음(참고 코드 주석 「observed live: None · ""」) |
| 왕복 수 | `result.num_turns` · 또는 `message_start` 개수 | |
| 토큰 | `result.usage`(input · output · cache_creation · cache_read) · `result.modelUsage`(모델별) | 바퀴별은 `stream_event message_delta.usage` 로 셈(확인 필요 U-2) |
| 비용 | `result.total_cost_usd` | **클라이언트 추정**(공식 headless 「client-side estimates」). 구독이면 청구되지 않는다 — 「API 였으면 얼마」로 기록 |
| 전체 | `result.duration_ms` · `duration_api_ms` | `duration_ms − duration_api_ms` ≈ CLI 쪽 시간(도구 · 기동 포함) |
| 한도 | `rate_limit_event{status, resetsAt, rateLimitType, utilization}` · `system/api_retry{error:"rate_limit"}` | 배치 멈춤 · 이어 가기에 씀(§6-4) |

### 2-2. codex-cli `--json`

| 잴 것 | 어디서 | 비고 |
|---|---|---|
| 기동 끝 | `thread.started` → `turn.started` | MCP 시작 시각을 따로 알리는 줄이 있는지는 확인 필요(U-3) |
| **ttft** | **잴 수 없음(토큰 단위)** — `agent_message` 는 `item.completed` 때 글 전체가 한 번에 옴(참고 설계 docstring 「no token deltas are fabricated」 · 공식 문서에 델타 언급 없음) | 대신 `ttft_msg_ms` = 첫 `agent_message` 완료 시각. 화면도 그때 한꺼번에 그려짐 |
| 도구 시작 · 끝 | `item.started` · `item.completed`(`item.type == "mcp_tool_call"`) | 참고 설계 `CodexEventIngest` 그대로 |
| 왕복 수 | 칸 없음 — `reasoning` · `agent_message` · 도구 항목 순서로 어림 | SDK 의 「Sonnet 호출 수」와 같은 뜻이 아님 |
| 토큰 | `turn.completed.usage{input_tokens, cached_input_tokens, output_tokens, reasoning_output_tokens}` | 턴 전체 합만 |
| 비용 | 없음 | 구독(ChatGPT plan) 사용량으로 빠짐 |

### 2-3. 공정성 — 케이스 사이 비교

- **같은 provider 안에서 case1 · 2 · 3 을 비교한다.** provider 끼리(Claude vs Codex) 속도 비교는 모델 · 기동 · 스트리밍 방식이 달라 같은 눈금이 아니다. 기록에는 둘 다 남기고 화면은 같은 provider 끼리 묶는다
- CLI 기동 오버헤드(프로세스 · 인증 · MCP 연결)는 case1 · 2 는 MCP 연결이 있고 case3 는 없다. 그래서 단계를 하나 더 둔다: `stages[]` 에 `cli_boot`(spawn → init) 를 넣고, `ttft_ms` · `total_ms` 는 **두 가지**로 남긴다 — t0 기준(사용자가 느끼는 값) · `cli_boot` 를 뺀 값(모델 + 도구 값). SDK 판의 MCP 연결은 지금 앱 시작 때 1회라서 질문 시간에 안 들어간다 — 뺀 값이 SDK 판과 더 가깝다
- case3 는 CLI 를 한 번만 띄우고(④ Sonnet 1회), 앞 단계 hub_resolve · jev · hub_path 는 앱 안에서 돈다 — `cli_boot` 는 ④ 앞에 들어간다
- 기동 시간을 따로 재는 「빈 호출」(도구 없이 아주 짧은 프롬프트)은 비용이 들어 이번엔 안 했다 — 첫 실물에서 `cli_boot` 칸으로 바로 보인다

---

## 3. 모델

### 3-1. Codex 「terra」

로컬 `codex debug models`(로컬 모델 목록 · 호출 없음)에 terra 가 둘 있다.

| slug | 이름 | 고를 수 있는 effort | 기본 effort | 속도 등급 |
|---|---|---|---|---|
| `gpt-6.1-terra` | GPT-6.1 Terra | low · medium · high · xhigh · max · ultra | low | fast |
| `gpt-5.6-terra` | GPT-5.6-Terra | low · medium · high · xhigh · max · ultra | medium | fast |

- 참고 설계(Strong_hajin `CodexCliProfile`)의 기본값은 `gpt-5.6-terra` · `service_tier="fast"` · `model_reasoning_effort="low"` 다
- 사용자 `~/.codex/config.toml` 의 기본값은 `gpt-6-sol` · effort medium 이다(terra 아님) → 실험은 `-m` 으로 꼭 박는다
- 둘 다 `-m <slug>` 로 고를 수 있다(목록 `visibility: list`). **어느 쪽을 「terra」로 할지는 사용자가 정한다**(D-1)

### 3-2. Claude

- 답: `--model claude-sonnet-5-5`(별칭 `sonnet` 도 됨 — 별칭은 「최신」을 가리켜 나중에 바뀔 수 있으니 기록 재현을 위해 **전체 id** 를 박음)
- ① · ②: `--model claude-opus-5-5`
- 실제로 돈 모델은 `system/init.model` · `result.modelUsage` 키로 기록한다(`observed_model`)
- `--fallback-model` 은 **주지 않는다**(SPEC §3-1 「폴백 쓰지 않음」)

### 3-3. thinking · effort 를 세 케이스 같게

| | claude-cli | codex-cli |
|---|---|---|
| effort | `--effort low\|medium\|high\|xhigh\|max` — 세 케이스 같은 값 하나(SDK 판 R-3 = `high`) | `-c model_reasoning_effort="…"` — 세 케이스 같은 값 하나 |
| thinking | **SDK 판 `thinking: between_tools` 를 그대로 줄 칸이 CLI 에 없다.** CLI 가 모델 기본을 쓴다 — 무엇이 나갔는지는 stream 의 thinking 블록 유무로만 보임(확인 필요 U-2) | 추론을 끌 수 없음(effort 로만 조절) · `hide_agent_reasoning` 은 출력만 가림 |
| 같게 되나 | provider 안 세 케이스는 **같은 플래그**를 쓰니 같다. SDK 판과 같지는 않다 | provider 안 세 케이스는 같다 |
| service tier | 없음 | `service_tier`(`fast` · `default`) — 세 케이스 같은 값(D-2) |

---

## 4. 비용 · 한도

### 4-1. 무엇으로 과금되나 · 지금 어느 쪽인가

| | 과금 | 로컬 지금 | 주의 |
|---|---|---|---|
| claude-cli | 구독 OAuth(`/login`) 이면 **구독 사용량** · env 에 `ANTHROPIC_API_KEY`(또는 `ANTHROPIC_AUTH_TOKEN` · `apiKeyHelper`)가 있으면 **API 과금**이 이긴다(공식 「Authentication precedence」 2·3·4 > 7) | `authMethod: claude.ai` · `subscriptionType: max` · 셸 env 에 키 없음 | **hub-evals `.env` 에 `ANTHROPIC_API_KEY` 가 있다.** `pydantic-settings` 는 os.environ 에 안 올리지만, 사용자가 `.env` 를 셸에 export 하고 띄우면 자식이 받는다 → **자식 env 를 만들 때 `ANTHROPIC_API_KEY` · `ANTHROPIC_AUTH_TOKEN` · `CLAUDE_CODE_USE_*` 를 지우는 것을 코드로 강제**하고, 실행 앞 `system/init`(`apiKeySource` 칸 확인 필요) 또는 `claude auth status --json` 의 `authMethod` 로 「구독」인지 확인한 뒤에만 돌린다 |
| codex-cli | ChatGPT 로그인이면 **plan 사용량** · `CODEX_API_KEY`(또는 auth.json 의 `OPENAI_API_KEY`)면 API 과금(공식 non-interactive 「CI Authentication」) | `auth_mode: chatgpt` · plan `prolite` · auth.json `OPENAI_API_KEY` 비어 있음 · 셸 env 에 `OPENAI_API_KEY` · `CODEX_API_KEY` 없음 | 자식 env 에서 `OPENAI_API_KEY` · `CODEX_API_KEY` 를 지움 |

### 4-2. 한 판의 양(기존 SDK 실행 기록 4건 · 캐시 0)

| | 입력 토큰 | 출력 토큰 | 왕복 | 전체 시간 |
|---|---|---|---|---|
| case1 | 51k~91k | 1.8k~2.6k | 3~4 | 16~24초 |
| case2 | 53k~70k | 1.7k~2.1k | 3 | 14~16초 |
| case3 | 8k~53k | 0.3k~1.5k | 1 | 4~14초 |
| 세 열 합 | **약 11만~21만** | 약 4k~6k | | |

- ② 채점(Opus · 도구 루프) 기록은 이 4건에 없다(채점 버튼 끔) — 사용자 말 「질문당 $2+」에서 세 열 몫(Sonnet $2/$10 기준 질문당 약 $0.3~0.5)을 빼면, **나머지 대부분은 Opus 채점 · 이름 뽑기 몫**으로 보인다(추정 · 기록 없음)
- CLI 로 바꾸면 시스템 프롬프트를 `--system-prompt` · `model_instructions_file` 로 갈아 끼워야 이 양이 비슷하다. 갈아 끼우지 않으면 CLI 기본 프롬프트(코딩 에이전트용)가 바퀴마다 붙는다

### 4-3. 밤새 일괄 실행(26 × 2) 때 한도

일괄 1회 = 질문 26 × {Claude Sonnet 세 열 · Codex terra 세 열} + 채점 52판(Opus 채점 1 + 이름 뽑기 3 씩).

| 쪽 | 쓰는 양(어림) | 한도 | 위험 |
|---|---|---|---|
| Claude 구독(max) | Sonnet 세 열 26판(약 300만~550만 입력) + Opus 채점 52판 + Opus 뽑기 156번 | **5시간 창 · 7일 창**(`rate_limit_event.rateLimitType = five_hour \| seven_day`). 정확한 한도 수치는 공식으로 공개되지 않는다 | **중간~높음**. Opus 채점이 가장 크다. 그리고 **이 구독은 코디 · 워커 Claude Code 세션과 같은 몫을 쓴다** — 밤샘 배치가 낮 작업 한도를 먹고, 낮 작업이 많으면 배치가 막힌다 |
| Codex plan(prolite) | terra 세 열 26판 | plan 의 5시간 · 주간 사용량 | 중간. 어디까지인지는 Codex 쪽 사용량 화면으로만 보임(JSONL 칸 없음) |

- 정책: 개인 구독을 자기 로컬 실험에 쓰는 것은 두 CLI 의 일반 사용 범위다. 다만 Claude 구독을 **배포된 서비스의 백엔드로** 쓰는 건 맞지 않는다 — 사용자 결정 「실험은 CLI · 배포는 SDK」가 그 선을 이미 지킨다. 한도를 피하려고 계정을 여럿 돌리는 식은 하지 않는다
- 줄이는 길(정할 것 D-6): 채점을 Opus 대신 Sonnet 으로(안 함이 기본 — 사용자 「채점 = Opus」) · 이름 뽑기를 Sonnet effort low 로 · 한 밤에 provider 하나씩

### 4-4. 예상 소요 시간(어림 · 실물 없음)

| 한 판 | 어림 |
|---|---|
| 세 열 동시(SDK 실측 14~24초) + CLI 기동(프로세스 · MCP 연결 — 확인 필요, 수 초로 봄) | 약 20~40초 |
| ① 뽑기 3번(병렬) | 약 10~20초 |
| ② Opus 채점(도구 루프 · 확인 필요) | 약 40~120초 |
| 질문 사이 간격(§6-4) | 10~30초 |
| **한 판 합** | **약 1.5~3.5분** |
| **52판(26 × 2 · 순차)** | **약 1.5~3시간** + 한도에 걸리면 창이 다시 열릴 때(최대 5시간)까지 기다림 |

---

## 5. 격리 — 공정성에 충분한가

### 5-1. 참고 설계에서 본 격리

| | 참고 설계(Strong_hajin) | 실험에 충분한가 | 더할 것 |
|---|---|---|---|
| **Codex** | 전용 `CODEX_HOME`(`.scax/codex-runtime` · `auth.json` 만 심볼릭 링크 · `AGENTS.md` · `config.toml` · skills 있으면 거부 — `prepare_isolated_codex_home`) · `--ignore-user-config` · `--ignore-rules` · `shell_environment_policy.inherit="none"` · plugins · skills 끔 · `--ephemeral` · `-s read-only` · 임시 cwd | **설정 · 규칙 · 스킬 · 플러그인은 충분**. 사용자 `config.toml` 에 `node_repl` · `pencil` MCP 와 플러그인 7 개가 켜져 있어 격리가 없으면 그대로 실린다 | **셸 · 실행 도구를 끄는 칸이 참고 설계에 없다**(read-only 샌드박스로 막을 뿐 도구 자체는 모델에 보임) → `features.shell_tool=false` · `features.unified_exec=false` · `web_search="disabled"` · `tools.view_image=false` 를 더한다. **내장 지시문**도 `model_instructions_file` 로 갈아 끼운다(참고 설계는 프롬프트 안에 정책을 넣었다). `project_doc_max_bytes=0` 으로 AGENTS.md 를 막는다 |
| **Claude** | `--setting-sources ""` · `--tools ""`(MCP 도구는 남음) · `--disable-slash-commands` · `--strict-mcp-config` · `--permission-mode bypassPermissions` · `--max-budget-usd` · 임시 cwd · 설정 폴더는 공용(키체인 인증이라 `CLAUDE_CONFIG_DIR` 를 옮기면 「Not logged in」 — 참고 코드 docstring 실측) | **도구 · 설정 · MCP 는 충분** | (1) **`--system-prompt`** 로 Claude Code 기본 시스템 프롬프트를 갈아 끼운다(참고 설계는 안 함 — 코딩 에이전트 지시가 붙으면 SDK 판 · Codex 판과 조건이 달라진다) · (2) **`--no-session-persistence`** — 참고 설계 docstring 이 「사람 세션과 기록이 섞인다」를 받아들인 자리인데, 이 플래그로 세션 파일을 안 남길 수 있다 · (3) 자식 env 에서 API 키 지움(§4-1) · (4) 자동 메모리 · 사용자 `~/.claude/CLAUDE.md` 가 `--setting-sources ""` 로 정말 안 실리는지는 첫 실물에서 확인(U-1) |

### 5-2. 사람 세션과 섞임

- Claude: 공용 설정 폴더를 쓴다 → `--no-session-persistence` 면 세션 기록은 안 남는다. **사용량(구독 한도)은 섞인다** — 막을 길 없음(§4-3)
- Codex: 전용 `CODEX_HOME` + `--ephemeral` 이면 세션 · 기록이 사람 쪽(`~/.codex/sessions`)에 안 남는다. `auth.json` 은 심볼릭 링크라 토큰 갱신이 원본에 쓰인다 — 세 열을 동시에 띄우면 갱신이 겹칠 수 있다(B-5 · 첫 실물 확인)

---

## 6. 실험 앱에 넣는 방법(추천)

### 6-1. 바꾸는 층은 「LLM 호출」 하나

SPEC-006 구조(case1 · 2 · 3 · 측정 · 기록 · 채점)는 그대로 두고, 지금 Anthropic SDK 를 직접 부르는 세 곳만 provider 뒤로 숨긴다.

| 지금 부르는 곳 | 바꾼 뒤 |
|---|---|
| `cases/loop.py` `run_tool_loop`(case1 · 2 — 앱이 도는 루프) | `provider.tool_answer(system, question, mcp_url, on_event)` — **sdk 는 지금 루프 그대로** · cli 는 CLI 가 루프를 돌고 앱은 이벤트만 받음 |
| `cases/case3.py` ④ Sonnet 1회 | `provider.answer(system, prompt, on_event)` |
| `quality/word_check.py` `extract_names` · `quality/judge.py` `judge` | `judge_provider.structured(system, prompt, schema, tools=None\|raw_mcp)` — **채점 provider 는 따로 고른다**(기본 claude-cli Opus) |

```
clinic_chat/llm/
  base.py        Provider 계약 — answer · tool_answer · structured · 정규화 이벤트(text_delta | text_done | tool_start | tool_end | usage | rate_limit | boot_done | error)
  sdk.py         지금 anthropic_client + loop 를 옮김(배포 경로 · 회귀 기준)
  claude_cli.py  claude -p stream-json 어댑터
  codex_cli.py   codex exec --json 어댑터
  cli_process.py 서브프로세스 실행(프로세스 그룹 · 줄마다 콜백 · 타임아웃 · 취소) · 자식 env 정리(키 지움)
clinic_chat/quality/raw_mcp.py   원장 도구 3 을 감싼 stdio MCP(채점용 · §1-3 가)
```

- `CaseTimer` · `stages[]` · SSE 이벤트 이름(§4-3)은 그대로 쓴다. 어댑터가 정규화 이벤트를 `timer.mark_text()` · `timer.stage("tool:…")` 로 옮긴다
- case1 · 2 의 MCP 연결: sdk 는 지금처럼 앱의 `ClientSession`, cli 는 URL 만 CLI 에 넘긴다(앱 `hub_mcp.py` 를 안 거침) — 기록 `trace.tool_calls[].output_bytes` · `node_ids` 는 cli 이벤트의 도구 결과에서 다시 셈(Claude 는 `tool_result` 내용 · Codex 는 `item.result`)

### 6-2. 참고 설계에서 가져올 것 · 버릴 것

| 가져올 것 | 버릴 것 · 바꿀 것 |
|---|---|
| provider 설정 하나로 전환 · 호출부는 어댑터를 import 하지 않음(`create_conversation_provider` · `AI_PROVIDERS`) | 대화 이어 가기(`resume` · `provider_session_ref` · `seed_references` · `recent_exchanges`) — 실험은 단건(SPEC §1) |
| `subprocess_runner` — 프로세스 그룹 · stdout 줄 콜백 · 타임아웃 · 취소 시 그룹째 종료(MCP 자식까지) | SCAX 정책 문구(`RELATIONSHIP_POLICY` 등) · `AnswerDocument` · follow-up 스키마 |
| `CodexEventIngest` · `ClaudeEventIngest` 의 이벤트 정규화 · 도구 지연은 시작과 끝을 둘 다 봤을 때만 | 「JSON 처럼 생긴 agent_message 는 숨김」 규칙 — 실험은 답 글을 그대로 보여야 함 |
| `prepare_isolated_codex_home`(auth 심볼릭 링크 · 금지 파일 검사) | Codex 의 stdio `command` · `args` · `env_vars` MCP 꼴 → `url` 꼴로 |
| Claude 격리 플래그 묶음 · `--max-budget-usd` 상한 | Claude `--output-format json`(generate) → 전부 `stream-json --include-partial-messages`(ttft 때문) |
| 실패 정규화(`ProviderUnavailable` · `ProviderRequestFailed` · `ProviderResponseInvalid` · 로그인 안 됨 판정) · 키 · 원 프롬프트를 오류에 안 넣음 | 참고 설계에 없는 것 더함: `--system-prompt` · `model_instructions_file` · 셸 도구 끔 · `--no-session-persistence` · 자식 env 키 지움 · 한도(`rate_limit_event`) 처리 |

### 6-3. 화면 · 기록 — 질문마다 provider 고르기(사용자 추가 절)

```
┌────────────────────────────────────────────────────────────────────┐
│ 질문 [                                    ] provider [claude-cli ▾] [보내기] │
│                                             · claude-cli · Sonnet 5.5     │
│                                             · codex-cli  · terra(<id>)    │
│                                             · sdk        · Sonnet 5.5 ⚠ 유료 │
├──────────────────┬──────────────────┬──────────────────────────────┤
│ case1 원장 MCP   │ case2 골드 MCP   │ case3 골드 + Jev             │
│ claude-cli·sonnet│ claude-cli·sonnet│ claude-cli·sonnet            │  ← 열 머리에 provider · 모델
│ ⏱ 기동 / 첫 글자 / 전체 (기동 뺀 값)                                 │
```

- 고른 provider 로 **세 케이스 모두** 돈다(열마다 다른 provider 를 섞지 않음 — 케이스 비교가 같은 provider 안에서만 공정)
- 채점 provider 는 따로 둔다(설정 `JUDGE_PROVIDER=claude-cli` · `JUDGE_MODEL=claude-opus-5-5`) — 화면은 「채점: claude-cli · Opus」 한 줄
- sdk 를 고르면 「유료」 표시 · `.env` 에 키가 있을 때만 선택지가 켜짐
- 기록 한 줄(`runs.jsonl`)에 더할 칸:

```json
"provider": "claude-cli",
"versions": {
  "answer_provider": "claude-cli", "answer_model": "claude-sonnet-5-5", "answer_model_observed": "…",
  "judge_provider": "claude-cli", "judge_model": "claude-opus-5-5",
  "cli_version": "2.1.284", "auth_kind": "subscription"
},
"settings": {"effort": "high", "service_tier": null, "tool_loop_max": null, "max_budget_usd": 1.0},
"cases": {"case1": {"timing": {"cli_boot_ms": 0, "ttft_ms": 0, "ttft_kind": "token|message", "ttft_ms_ex_boot": 0, "…": "…"},
                    "cost": {"usd_estimate": 0.0, "billed": "subscription"}}}
```

- 기록 표(질문 기록 목록)에 **provider · 모델 열**을 더하고, provider 로 거르는 필터를 둔다
- `ttft_kind` — Codex 는 `message` 라서 표에서 Claude 와 같은 열에 두되 표시를 달리 한다(⏱ 뒤 「(메시지)」)
- `auth_kind` — 실행 앞에 확인한 값(구독 · API 키). **구독이 아니면 CLI provider 는 실행하지 않는다**

### 6-4. 일괄 실행(배치) — 질문 리스트 전체

- 입력: `questions.md`(26) 를 서버가 읽어 목록으로 · 화면 「일괄 실행」 패널에서 **provider 여러 개 체크**(claude-cli · codex-cli) · 채점 켬/끔 · 질문 범위(전체 · 번호 골라)
- 모양: `batch_id` 하나 = `runs/batches/<batch_id>.json`(계획: 질문 × provider 칸 목록 · 상태 `todo|running|done|failed|skipped`) + 끝난 판은 지금처럼 `runs.jsonl` 한 줄(`batch_id` · `batch_item` 칸 더함)
- **순차**로 돈다(한 번에 한 판 — 한 판 안의 세 열은 지금처럼 동시). 순서는 질문 → provider 를 번갈아(Q1 claude · Q1 codex · Q2 claude …) — 한 provider 가 한도에 걸려도 다른 쪽은 계속 갈 수 있게
- **질문 사이 간격**: 설정 `BATCH_GAP_SEC`(기본 15 — 정할 것 D-7)
- **실패 재시도**: 판 하나에 최대 2번 더(간격 60초 → 180초). 재시도는 「기동 실패 · 프로세스 비정상 종료 · 시간 초과 · 서버 과부하(`api_retry error: overloaded`)」만. **모델이 답했는데 품질이 나쁜 것 · 거절(refusal) · 스키마 미달은 재시도하지 않고 그대로 기록**(실험 결과다)
- **한도에 걸렸을 때**: Claude 는 `rate_limit_event`(`utilization` 이 높음 · `status` 429) 나 `api_retry error: rate_limit` 이 오면 그 provider 칸을 `paused_until = resetsAt` 으로 두고 다른 provider 를 계속 · 둘 다 막히면 배치 전체가 `resetsAt` 까지 잠든다. Codex 는 JSONL 에 한도 칸이 없어 `turn.failed` · `error` 메시지 문구(「usage limit」 꼴 — 문구 확인 필요 U-3)로 판정하고, 다시 열리는 시각을 모르면 30분마다 한 번 다시 해 본다
- **끊겨도 이어서**: 서버가 다시 뜨면 `batches/<id>.json` 을 읽어 `done` 아닌 칸부터 · `running` 으로 남은 칸은 결과 줄이 `runs.jsonl` 에 있으면 `done`, 없으면 다시 함 · 채점만 안 된 판은 채점만 다시(`POST /api/runs/{id}/judge` 꼴)
- **진행 기록**: 화면에 `n/52 · 지금 질문 · provider · 다음 재개 시각 · 실패 목록` · 코디가 밤새 볼 수 있게 `GET /api/batches/{id}` JSON 도 냄
- 코디가 돌릴 때(사용자 추가 절): 화면 없이 `uv run python -m clinic_chat.batch --providers claude-cli,codex-cli --judge on` 같은 명령 하나로도 돌게 한다(같은 배치 파일 · 같은 이어 가기)

### 6-5. 구현 순서(제안 · 발주 단위 아님)

1. `llm/base.py` · `sdk.py` 로 지금 코드를 옮기기만(동작 같음 · 기존 시험 통과)
2. `cli_process.py`(자식 env 정리 시험 포함 — 키가 있으면 지워지는지)
3. `claude_cli.py` + 모의 stream-json 시험(기록된 줄 몇 개로) → 실물 1회(U-1 · U-2)
4. `quality/raw_mcp.py` + 채점 claude-cli → 실물 1회
5. `codex_cli.py` + 모의 JSONL 시험 → 실물 1회(U-3 · U-4)
6. 화면 provider 선택 · 기록 칸 · 기록 표 열
7. 배치(계획 파일 · 이어 가기 · 한도 멈춤) → 질문 2개 × 2 provider 로 짧게 → 밤샘 전체(사용자 · 코디)

---

## 7. 막히는 것 · 사용자가 할 일

### 7-1. 막히는 것(B)

| # | 무엇 | 영향 | 길 |
|---|---|---|---|
| B-1 | `claude -p` 는 env 에 `ANTHROPIC_API_KEY` 가 있으면 무조건 API 키로 과금 | CLI 로 돌려도 돈이 나감 | 자식 env 에서 지움 · 실행 앞 `authMethod` 확인(§4-1) |
| B-2 | 두 CLI 모두 도구 루프 상한 칸이 없다(2.1.284 help 에 `--max-turns` 없음 · Codex 도 없음) · 「상한 닿으면 tool_choice none 으로 마지막 답」을 못 함 | SPEC R-2 · `loop_capped` 를 CLI 판에서 지킬 수 없음 | CLI 판은 `--max-budget-usd` · 타임아웃으로 대신하고 기록에 `tool_loop_max: null` · 도구 호출 수를 남김(D-3) |
| B-3 | 도구 결과 상한(`cap_text` 20,000 바이트)을 CLI 안에 넣을 수 없음 | SDK 판과 입력 크기 달라짐 · 토큰 늘어남 | 허브 MCP 쪽 응답 크기 한도(SPEC-005 §5-12 크기 한도 20,000)가 실물에서 지켜지는지 확인 · 안 되면 허브에서 고침 |
| B-4 | Codex 는 글자 단위 ttft 를 못 잼 | Codex 판 ttft = 메시지 단위 | `ttft_kind` 로 구분(§6-3) |
| B-5 | Codex 전용 홈의 `auth.json` 심볼릭 링크를 세 열이 동시에 갱신할 수 있음 | 드물게 인증 꼬임 | 첫 실물에서 확인 · 문제가 나면 판 시작 전 1회 `codex login status` 로 갱신을 먼저 끝냄 |
| B-6 | Sonnet 「thinking 끔(between_tools)」을 CLI 로 그대로 줄 수 없음 | SDK 판과 thinking 조건이 다름 | provider 안 세 케이스는 같음 · 기록에 thinking 블록 유무를 남김 |
| B-7 | Claude 구독 한도를 사람 세션과 같이 씀 | 밤샘 배치 ↔ 낮 작업이 서로 막음 | 배치를 밤에 · `rate_limit_event` 로 멈춤 · 이어 가기 |

### 7-2. 정할 것(D) — 사용자

| # | 무엇 | 선택지 | 추천 |
|---|---|---|---|
| D-1 | terra 가 어느 것인가 | `gpt-6.1-terra` · `gpt-5.6-terra`(참고 설계 기본) | — (사용자 몫) |
| D-2 | Codex effort · service tier | effort low(6.1 기본)·medium(5.6 기본)·high / tier fast · default | Claude 쪽 `high` 와 맞추려면 high · tier 는 default(fast 는 사용량을 더 씀 — 공식 「fast」 등급 설명 확인 필요) |
| D-3 | CLI 판 도구 루프 상한 | 없음(타임아웃 · 예산만) · 프롬프트에 「도구 N 번까지」 | 없음 + 기록 |
| D-4 | 채점 원장 도구 | (가) 로컬 stdio MCP · (나) 허브 raw-mcp | (가) — SPEC W-3 그대로 |
| D-5 | ① 이름 뽑기 모델 | Opus(지금 R-4) · Sonnet effort low | 사용자 「채점 = Opus」라 Opus 유지 |
| D-6 | 한도 걱정이 크면 | 한 밤에 provider 하나 · 채점을 다음 날 따로 | 먼저 질문 2 × 2 짧게 돌려 한 판 양을 본 뒤 정함 |
| D-7 | 배치 간격 · 재시도 수 | 간격 10~30초 · 재시도 0~3 | 15초 · 2번 |

### 7-3. 사용자 · 코디가 할 일(U) — 실물 1회로만 닫히는 것

| # | 무엇 | 누가 | 어떻게 |
|---|---|---|---|
| U-1 | Claude 격리 확인 — 사용자 CLAUDE.md · 자동 메모리 · 스킬이 안 실리는지 · `system/init` 의 도구 목록이 MCP 도구뿐인지 | 구현 워커 실물 1회 | `system/init`(tools · mcp_servers · model · 인증 칸) 저장해 봄 |
| U-2 | Claude stream 의 바퀴별 usage · thinking 블록 · `rate_limit_event` 실제 꼴 | 같음 | 실물 1회 줄 저장 → 모의 시험 자료로 |
| U-3 | Codex JSONL 실제 꼴 — MCP 시작 줄 · 한도 걸렸을 때 메시지 · `mcp_tool_call` 결과 칸 | 같음 | 실물 1회 |
| U-4 | Codex 에서 셸 · 웹 · 이미지를 끈 뒤 남는 내장 도구가 있는지 | 같음 | 실물 1회 JSONL 의 `item.*` 종류 확인 |
| U-5 | **밤샘 실행 전 `.env` 의 `ANTHROPIC_API_KEY` 를 그대로 둘지** — CLI 만 쓸 밤엔 빼 두면 B-1 이 이중으로 막힘 | 사용자 | `.env` 에서 그 줄을 주석으로(sdk provider 는 그동안 꺼짐) |
| U-6 | Claude 구독 사용량 화면 · Codex 사용량 화면에서 밤샘 전 남은 양 확인 | 사용자 | claude.ai 설정 · ChatGPT Codex 사용량 |
| U-7 | 허브(18005)가 밤새 떠 있어야 함 | 사용자 · 코디 | 배치 시작 때 허브 헬스 확인을 앱이 먼저 함 |

## 근거

- 로컬: `claude --version` 2.1.284 · `claude --help` · `claude mcp add --help` · `claude auth status --json`(계정 칸 가림) · `codex --version` 0.165.0 · `codex exec --help` · `codex mcp add --help` · `codex debug models` · `codex features list` · `codex login status` · `~/.codex/config.toml`(값은 모델 · MCP 이름만 봄) · `~/.codex/auth.json`(`auth_mode` · plan 클레임만)
- 공식: code.claude.com/docs/en/headless(`--bare` 는 구독 안 씀 · stream-json · `--include-partial-messages` · `system/init` · `mcp_server_errors` · `system/api_retry` · `total_cost_usd` 추정) · /authentication(인증 우선순위 · `-p` 는 키가 있으면 늘 씀) · /agent-sdk/typescript(`rate_limit_event` · result 칸) · learn.chatgpt.com/docs/config-file/config-reference(`mcp_servers.<id>.url` · `required` · `enabled_tools` · `web_search` · `features.shell_tool` · `model_instructions_file` · `project_doc_max_bytes`) · /non-interactive-mode(`--json` 이벤트 · usage · `--output-schema` · `CODEX_API_KEY`)
- 참고 설계(읽기만): `Strong_hajin/backend/src/ax_workspace/platform/codex_cli.py:84-91`(profile) · `:267-334`(`_conversation_arguments` · `_mcp_overrides`) · `:524-566`(`_arguments`) · `:608-768`(`CodexEventIngest`) · `:771-796`(`prepare_isolated_codex_home`) · `platform/claude_cli.py:1-10`(격리 방침 docstring) · `:66-74`(profile) · `:238-282`(`_isolation_arguments` · `_conversation_arguments`) · `:410-566`(`ClaudeEventIngest`) · `platform/cli_process.py:83-106`(`subprocess_runner`) · `bootstrap/settings.py`(`AI_PROVIDERS` · `ai_provider`) · `bootstrap/application.py:4229-4233`(`create_conversation_provider`) · `modules/ax_execution/ai.py`(계약 · 실패 정규화)
- hub-evals: `clinic_chat/clients/anthropic_client.py`(between_tools · effort high) · `cases/loop.py`(루프 상한 · `cap_text`) · `quality/judge.py` · `quality/word_check.py` · `runner.py` · `pricing.py` · `.env` 이름 목록(값은 안 봄)
- 실행 기록: `reference/2026-10-30-hub-evals/runs/_archive/runs-2026-10-30T1450-before-reset.jsonl`(4판 토큰 · 시간)
