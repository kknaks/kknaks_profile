# WP-133 서버 LLM claude → codex 핫픽스 — backend_hotfix 결과 보고

## 상태: done (Phase 1·2 코드 완료, 커밋 없음 / Phase 3 는 배포 후 코디네이터 몫)

- 워크트리: `/Users/kknaks/orca/workspaces/mediness-app/llm-codex-hotfix-hotfix` (base `origin/main` `67b6a7dc`)
- 커밋·push·PR 없음. 변경은 워크트리에만 있다.

## 변경 파일 (전부 `back/app/` 안)

| 파일 | 변경 |
|---|---|
| `back/app/services/server_llm_submission.py` (신규) | 공용 codex 조립 `build_codex_submission(effort, timeout_sec, mcp_tool_names=None)` → `ServerSubmission(provider, model, provider_options, options)`. `submit_kwargs(plan)`(model None 이면 키 제외). `log_final_prompt(path, provider, prompt, system_prompt=None, plan=None)`(바이트 로그 + `-c` redact). `compose_prompt`·`redact_config_overrides` 는 선례 `meeting_v2_submission` 것을 그대로 재사용·re-export |
| `back/app/config.py` | `server_llm_provider: str = "codex"`, `server_codex_model: str = ""`, property `server_codex_model_resolved` (= 값 or `landing_chat_model`) |
| `back/app/services/decision_gate.py` | B `_default_ai_call`: 인자 `provider` 기본 `"claude"` → `None`(= `settings.server_llm_provider`). codex/claude 분기 |
| `back/app/services/brief/synthesizer.py` | C `_synthesize_events` submit: codex/claude 분기. 모듈 상수 `_BRIEF_MCP_TOOL_NAMES`(접두어 없는 4종) |
| `back/app/services/weekly_report_pipeline.py` | D `_default_ai_call`: codex/claude 분기 |

`pipeline_ingest_consumer.py`(B′) 는 수정 없음.

## 설정 키 (Open Issues ① = ⓐ 공용 키 한 벌)

| 키 (env) | 기본값 | 의미 |
|---|---|---|
| `server_llm_provider` (`SERVER_LLM_PROVIDER`) | `codex` | B·C·D 공용 provider. `codex` 이외면 claude 분기(구 인자) |
| `server_codex_model` (`SERVER_CODEX_MODEL`) | `""` | 빈 값 → `landing_chat_model`(기본 `gpt-5.6-terra`). 해석값도 비면 `model` 키 제외 |
| MCP url / server key | (새 키 없음) | `meeting_v2_mcp_url`(`http://mcp:28081/mcp`)·`meeting_v2_mcp_server_key`(`mediness`) 를 **그대로 참조** — 같은 값 보장 |
| MCP 인증 | — | `X-Internal-Auth="<INTERNAL_AUTH_SECRET>"`(선례와 동일) |

## 지점별 전/후 제출 인자

공통 codex 모양 (`provider_options`): `sandbox="read-only"`, `skip_git_repo_check=True`, `config=[model_reasoning_effort=<e>, approval_policy="never", (MCP 줄), features.shell_tool=false, web_search="disabled", features.image_generation=false, features.apps=false]`. `prompt = compose_prompt(system, user)` = `f"{system}\n\n---\n\n{user}"`. claude 전용 키(`system_prompt`·`max_turns`·`effort`·`mcp_config`·`allowed_tools`·`disallowed_tools`·`json_schema`) 0개.

| 지점 | 전 (claude) | 후 (codex, 기본) |
|---|---|---|
| **B** `decision_gate._default_ai_call` | provider `claude`, model `meeting_llm_batch`, po `{system_prompt, max_turns(기본6/B′25), effort low, mcp_config, allowed_tools(접두 7), disallowed_tools}`, options `{timeout_sec}` | effort `low`, MCP `enabled_tools` = `gate_tools.ALLOWED_TOOL_NAMES` 7종(접두어 없음) + 툴별 `approval_mode="approve"`, options `{timeout_sec}` 그대로, queue `brief_queue` 그대로. `model` 인자가 명시되면 그 값 우선(현재 호출부 없음) |
| **B′** `pipeline_ingest_consumer` partial | `max_turns=pipeline_gate_max_turns, timeout_sec=pipeline_gate_timeout_sec` | 그대로 통과. codex 분기는 `timeout_sec` 만 소비하고 `max_turns` 는 무시(시그니처 유지) → 깨지지 않음 |
| **C** `BriefSynthesizer._synthesize_events` | provider `claude`, po `{system_prompt, max_turns 25, effort medium, mcp_config, allowed_tools(접두 4)}`, options `{timeout_sec:600}` | effort `medium`, MCP `enabled_tools=["read_file_tool","list_dir_tool","repo_search_tool","get_metadata_tool"]` + approve 4줄, options `{timeout_sec:600}`, `result(timeout=600)` 그대로 |
| **D** `weekly_report_pipeline._default_ai_call` | provider `claude`, po `{system_prompt, max_turns 1, effort low}`, options `{timeout_sec:300}` | effort `low`, `mcp_servers.*` 줄 없음, options `{timeout_sec:300}` 그대로 |

claude 분기는 세 곳 모두 구 인자 그대로 남겼다(provider 값만 `settings.server_llm_provider` 에서 온다 → `claude` 설정 시 구 인자와 동일).

결과 파싱·상태 판정(`status != "done"`)은 손대지 않았다(WP-133 결과 파싱 표 = 변경 불요).

## 되돌리는 법

- back 파드 env `SERVER_LLM_PROVIDER=claude` → 세 경로 모두 구 claude 인자로 제출. (⚠ 조직 차단 중엔 같은 실패 — 코드 회귀 대응용)
- 모델만 바꾸기: `SERVER_CODEX_MODEL=<정식 모델 ID>` (effort 허용값 짝 재확인 필요)
- 또는 핫픽스 커밋 revert. 데이터·migration 변경 없음.

## Phase 3 에서 코디가 볼 로그

back 로거 `server_llm_submission`, 제출 직전 한 줄:

```
server_llm final_prompt path=<decision_gate|brief|weekly> provider=codex bytes=<N> model=<모델> config=[... 'mcp_servers.*.http_headers=<redacted>' ...]
```

- grep 키워드: **`server_llm final_prompt`** (경로별 `path=brief` 등)
- `bytes` = compose 후 최종 프롬프트(system+템플릿+본문 합본) UTF-8 바이트 → Open Issues ②(C argv/E2BIG 한계) 실측값. claude 분기에서도 같은 줄이 `provider=claude bytes=<prompt+system>` 로 찍힌다.
- C 는 기존 `brief serialized prompt body = N bytes`(본문만) 로그도 그대로 남아 있다.
- 시크릿: `http_headers` 줄은 로그에서 `<redacted>` (실측: 로그에 secret 원문 없음 확인). C 의 에러 저장은 기존 `_redact_tokens` 를 그대로 거친다.

## 검증 (테스트는 사용자 결정으로 작성·수정·실행하지 않음)

- `python -m py_compile` 5파일 → 에러 0
- import 확인 (`uv sync --frozen` 으로 scratchpad venv 생성, 필수 env 더미값): `app.services.decision_gate, app.services.brief.synthesizer, app.services.weekly_report_pipeline, app.config, app.services.pipeline_ingest_consumer` → import-ok
- 조립 결과 대조 (ad-hoc 스크립트, 파일 생성 없음): B/C/D 모두 `provider_options` 키 = `config, sandbox, skip_git_repo_check` 뿐, 금지 키 0, `mcp__` 접두어 0, MCP 줄 수 B 10 / C 7 / D 0, model = `gpt-5.6-terra`
- `git status --short` → `back/app/` 밖 변경 0

## 미결·주의

- **기존 테스트가 깨진다(알고 둠)**: `tests/services/test_brief_synthesizer.py:541-549`, `test_decision_gate_ai.py:300-370` 등 claude 인자 단정 — 기본값이 codex 로 바뀐 탓. 후속에서 settings override 로 claude 회귀 테스트화 + codex 신규 테스트 필요.
- B 계측 `collect_stream_stats` 는 그대로 — codex 스트림에서 0/누락 가능(Open Issues ④, 추천 무영향).
- C 출력 코드펜스/머리말 오염은 lint 로 안 잡힌다(Open Issues ③) — Phase 3 에서 `markdown_body` 가 `# 📋 메디솔브 브리핑` 으로 시작하는지 확인 필요.
- Pre-deploy: 워커 컨테이너에서 `http://mcp:28081/mcp` 도달 여부(회의 v2 가 이미 쓰는 값).
