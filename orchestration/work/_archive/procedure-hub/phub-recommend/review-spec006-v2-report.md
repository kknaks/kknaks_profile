# 검수 보고서 — SPEC-006 v2(0.3.0) · WORK-006

작성 2026-11-01 · 검수자 reviewer 워커(읽기 전용 · 스펙 · 코드 수정 없음 · 실물 CLI 호출 없음) · 발주서 `phub-recommend-review-spec006-v2-brief.md`
(같은 이름의 10-30 판 `review-spec006-v2-report.md`(WORK-004 재검수 · PASS)는 이 파일로 덮음 — 그 판 결론은 `_RESUME.md` §2 10-30 에 남아 있음)
대상 `SPEC-006.md`(0.3.0 · 11-01) · `WORK-006.md` · `phub-recommend-jev-walk-addendum.md` · 대조 = 앱 코드 `clinic_chat/hub-evals`(HEAD 18561a4 · case3.py · llm/cli.py · cli_process.py · config.py · loop.py · clients · tests) · `fail-triage2.md` · `.json` · `runs/runs.jsonl`(rerun-v3 182) · Claude CLI 2.1.284 바이너리 문자열 · Codex CLI 0.166.0 바이너리 문자열 · `mcp` 2.3 `MCPServer.tool` 시그니처 · `_RESUME.md` §2

## 판정 — **FAIL** (FAIL 3 · WARN 5)

한 줄: 스펙 본문(§2-5 · §3-4 · §3-5 · §3-6 · §3-7 · §4 · §7-6 · §7-7)은 앱 실물 이름 · 기록 칸 · Jev 호출 꼴 · fail-triage2 숫자 · 보충 항목 · 결정표와 전부 맞는다. FAIL 은 WORK-006 의 시험 경로가 레포 구조와 다르고(F-1), 자기 규칙인 「grep 결과 파일 전부 표에」 를 지금 상태에서 못 지키며(F-2), §3-5 전달 보장 정의에 적은 Codex 마커 문자열이 0.166 바이너리에 없다(F-3)는 세 가지다.

| 기준 | 판정 | 요지 |
|---|---|---|
| 1 실물 대조 | **FAIL(경미)** | 도구 · 기록 칸 · 격리 플래그 · Jev 꼴 · 단계 이름 전부 코드와 같음(부록 A). 전달 보장 (a) 근거: Claude `MAX_MCP_OUTPUT_TOKENS`(기본 25,000) · `anthropic/maxResultSizeChars` · 마커 3종 · `mcp` 2.3 `tool(meta=)` · Codex `tool_output_token_limit` · `output_token_limit` 전부 바이너리 · 시그니처에서 확인. **Codex 마커 2종은 0.166 에 없음**(F-3) · Claude 마커는 3종 외 변형 3 더 있음(W-4) |
| 2 fail-triage2 대조 | PASS | 잘림 100/614(규칙 `rec_bytes < hub_bytes − 8` · 1,700~2,300B 뭉침 93) · intent 14/662(값 I-01 9 · I-05 2 · I-03 1 · `none` 2) · C 18 · case3 중앙 46,539 · p95 170,989 · 최대 280,705 · bash 10(Q078 · Q105 · Q150 · Q161 · Q165 · Q166 · Q170 · Q171 · Q174 · Q202) 전부 `runs.jsonl` 재계산과 같음. 끝 조건 · 기록 칸 대응: 잘림 → `truncated` · `delivered_bytes` · `hub_bytes` · 0 / intent → `intent_passed` · `intent_ratio` ≥ 95% / 격리 → `stray` 0 / 크기 → `walk.bytes_total` · 공정성 바이트 보고. **C 비율 자체는 끝 조건 · 보고 열에 없음**(W-2 · 허브 A-1 몫이긴 함) |
| 3 보충 대조 | PASS | 걸음 ≤ 4(`WALK_MAX_STEPS`) · peek ≤ 2KB(§3-4-2) · 예산 20KB(`WALK_BYTE_BUDGET`) · 「충분」 Noul(`WALK_ENOUGH_MIN`) · 멈춤 4종(`walk.stop`) · 되돌아가기 = 의도 묶음 1회(§3-4-3 · `fallback_reason` 3 사유) · 걸음마다 기록(노드 · 섹션 · 신뢰도 · 바이트 · ms) · `trace.walk` · 첫 글자 영향(`claude` 시작 − `t0`) · Jev 호출 수 · 시간(`jev_calls` · `jev_ms_total`) · 비교 기준 182(`b202610311552-d39a4d` · 같은 채점) · 허브 쪽 세 줄은 W-1 로 v3.2 에 넘김 — 빠진 항목 0 |
| 4 결정표 충돌 | PASS | 허브 LLM 없음(peek · expand 결정론 명시) · Jev 는 앱(§3-4 · §3-7) · CLI 판 입력 상한 없음(§2-5 · §3-7 · `input_cap_bytes: null` — SDK 판 0 은 공정성 정리 · 실험 밖) · 채점 열마다 절대(`judge.mode: "absolute"` 유지) — 어긋남 0 |
| 5 WORK-006 | **FAIL** | WP 순서(0 확인 → 1 전달 → 2 intent → 3 걸음 → 4 검증 → 5 재실행) · WP 마다 시험 · 끝 조건 ↔ §7-6 1:1 · v3.2 의존(depends_on · WP-0 전제 · WP-1 ③ · WP-3 「모의로라도」) 명시됨. 단 **시험 경로 4개가 레포에 없음**(F-1) · **Meta 의 grep 규칙을 지금 레포에 돌리면 표 밖 파일 14** (F-2) |
| 6 추측 자리(W 밖) | WARN | Codex 「기본 10KiB/256줄 하드컷에서 바뀜」 · Claude 「50,000 자」 숫자는 바이너리에서 특정 못 함(문서 인용 — W-3 · WP-0 실측으로 닫힘) · `intent` 값 `none` 처리(W-5) |

## FAIL

### F-1 · WORK-006 WP-1 · WP-2 · Meta — 시험 파일 경로가 레포 구조와 다름(기준 5)

근거(`tests/` 실물): `tests/{cli,phase1..7}/` 아래에만 시험이 있다 — `tests/phase2/test_loop.py` · `tests/cli/test_report.py` · `tests/phase1/test_repo_rules.py` · `tests/phase3/test_case3.py`. WORK-006 이 적은 `tests/test_loop.py` · `tests/test_report.py` · `tests/test_repo_rules.py` 는 없고 `tests/test_prompts.py` 는 어디에도 없다(프롬프트 시험 자체가 없음). WP-1 검증 `uv run pytest tests/test_cli_ingest.py tests/test_loop.py -q` · WP-2 `tests/test_prompts.py tests/test_report.py` 는 그대로 치면 「file not found」.
방향: 기존 경로로 고치고(`tests/phase2/test_loop.py` · `tests/cli/test_report.py` · `tests/phase1/test_repo_rules.py`) 새 시험은 한 폴더(예 `tests/phase8/`)로 두며 `test_prompts.py` 는 「새」 로 표시.

### F-2 · WORK-006 Meta 「코드 표면 grep 전부」 ↔ §Scope 표 — 표 밖 파일 14(기준 5)

근거: Meta 의 grep 을 레포에 그대로 돌리면 28 파일. 표에 없는 것 —
- `clinic_chat/deps.py`(`intent_tools` · `section_tools` — 걸음 경로 `sections=none` · peek/expand 도구 등록 자리) · `clinic_chat/batch.py` · `clinic_chat/quality/judge.py`
- **`tests/phase3/test_case3.py`**(v1 case3 흐름 시험 — 교체로 깨짐 · `fallback_*` 로 옮겨야 함) · `tests/phase7/test_mock_e2e.py` · `tests/phase2/test_loop.py`(`cap_text` 0) · `tests/phase4/test_timing_runs.py` · `tests/cli/test_cli.py` · `test_runner_cli.py` · `test_rerun_report.py` · `tests/fake_jev.py`(새 Choice 이름 「펼칠 것」 · Noul 「충분」 모의) · `tests/mock_server.py` · `tests/estimate_cost.py`
- `web/state.js`
WP-4 3 「표면 grep 누락 0」 이 끝 조건인데 발주 시점에 이미 14 누락 — 구현 워커가 표만 보고 가면 v1 시험이 깨진 채로 WP-4 에서 발견된다.
방향: 위 14 를 표에 더하고(「고침」 또는 「영향 없음 — 확인만」) `test_case3.py` 는 「되돌아가기 경로 시험으로 이름 · 대상 바꿈」 으로 적는다.

### F-3 · SPEC-006 §3-5 「전달 보장 정의」 — Codex 마커 문자열이 0.166 실물에 없음(기준 1 · 6)

근거: Codex 0.166.0 바이너리(`codex-darwin-arm64/.../bin/codex`) 문자열에 「[... output truncated to fit」 · 「[... omitted k of n lines」 꼴은 없다(「[... omitted … frame」 은 Rust panic 메시지). 실물 잘림 문자열 후보 = 「Warning: truncated output (original token count:」 · 「<truncated omitted_approx_tokens=」 · 「omitted_due_to_size_limit (overage_bytes=」 · 「 bytes omitted ...」 · 「 tokens truncated」 · 구조 칸 `_codex_executed_tool_call_truncated{original_bytes, max_bytes, omitted_calls}`. 스펙은 표에서 「0.166 실물 마커는 WP-0 에서 적음」 이라 하면서도 **정의 문단**에는 옛 꼴 두 줄을 「마커 문자열」 로 적어 두었다 — `truncated` 판정 구현이 그 두 줄을 따르면 Codex 잘림을 0 으로 잘못 센다.
방향: 정의 문단에서 Codex 두 줄을 빼고 「마커 목록 = WP-0 실물로 고정한 설정 상수(`TRUNCATION_MARKERS`)」 로 쓰며, 위 실물 후보를 WP-0 2 · 3 의 「찾을 문자열」 로 넣는다. Claude 쪽 변형(W-4)도 같은 상수에.

## WARN

| id | 조항 | 내용 · 방향 |
|---|---|---|
| W-1 | WORK-006 depends_on · SPEC-006 §7-7 W-1 · W-2 | SPEC-005 v3.2 발주서(`phub-recommend-spec005-v32-brief.md`)에는 peek · expand · 도구 `_meta` · `intent` 설명 문구가 **없다**(A-1 다이어트 · A-2 · D-1~D-14 만). 보충 addendum 은 peek/expand 만 다룬다. `_RESUME` 11-01 「보충 2 로 전달」 이 문서로 안 보이므로 코디가 v3.2 planner 에 세 줄(peek/expand 꼴 · meta 12 · intent 「반드시」)이 닿았는지 확인 |
| W-2 | SPEC-006 §7-6 case3 교체 비교 · §4-4 | 교체의 동기가 「C 10% · 46KB」 인데 비교 보고 항목에 C(허브가 줬는데 놓침) 건수 · 비율 열이 없다. `rerun_report` 에 fail-triage2 §2 와 같은 C 셈(응답 facts 원문 ∋ 인용) 한 열 추가 권고 — 판정은 결정론이라 앱 몫 |
| W-3 | SPEC-006 §3-5 표 | Claude 「약 50,000 자 파일 저장」 · 「250,000 자까지」 · Codex 「기본 10KiB/256줄」 은 문서 · 이슈 인용이고 바이너리에서 숫자를 특정하지 못했다(확인된 것: `MAX_MCP_OUTPUT_TOKENS` 기본 `P=25000` · `maxResultSizeChars` · `persistenceThresholdCeiling` 칸 · `tool-results/mcp-<name>-blob-…` 저장 경로). WP-0 실측 표에 「문턱 실측값」 열을 두어 닫는다(이미 WP-0 범위 — 적기만) |
| W-4 | SPEC-006 §3-5 Claude 마커 | 3종 외 변형: 「Output truncated (… KB total). The full output could not all be saved to」 · 「(… KB total): later output was discarded because **this session writes no files**」 · 「Output exceeded the persist limit; only the first … were saved to」. 둘째는 앱이 쓰는 `--no-session-persistence` 와 직결 — 저장 자체가 안 될 수 있어 (c) 폐기 근거가 더 강해지고, 마커 판정엔 이 문자열도 넣어야 한다(F-3 상수에 같이) |
| W-5 | SPEC-006 §3-6 · §4-4 | rerun-v3 의 intent 14 중 2 는 값 `"none"`(허브 v3 는 모르는 값 4xx — SPEC-005 §5-0). `intent_passed` 를 「칸 있음」 으로만 재면 틀린 값도 통과로 센다 — 「값 ∈ I-01~I-12 일 때만 true」 한 줄 |

## 부록 A — 실물 대조표(기준 1)

| 스펙 | 실물(코드 · 기록) | 결과 |
|---|---|---|
| §2-5 Claude 격리 플래그(`--setting-sources ""` · `--tools ""` · `--allowedTools mcp__hub` · `--strict-mcp-config` · `--disable-slash-commands` · `--no-session-persistence` · `--system-prompt` · `--permission-mode bypassPermissions` · `--max-budget-usd`) | `cli.py claude_args` 같음 · stdin 프롬프트 | ○ |
| §2-5 Codex 격리(`CODEX_HOME` · `--ignore-user-config` · `--ignore-rules` · `--ephemeral` · read-only · shell/exec/web/plugins/skills 끔 · `model_instructions_file` · `project_doc_max_bytes=0` · `shell_environment_policy.inherit="none"` · `mcp_servers.hub.url/required/approval/tool_timeout_sec`) | `cli.py codex_args` 같음 | ○ |
| §2-5 자식 env 키 지움 | `cli_process.SCRUB_ENV` 13 — `MAX_MCP_OUTPUT_TOKENS` 는 아직 없음(WP-1) | ○ |
| §3-5 설정 이름 `MCP_RESULT_MAX_CHARS` · `WALK_*` · `TOOL_RESULT_MAX_BYTES=0` | `config.py` 에 `tool_result_max_bytes=20_000` 만(새 이름은 WP-1) · `.env.example` 35행 | ○(새 칸) |
| §3-3 · §4-2 `tool_calls[]{tool, input, output_bytes, node_ids, ms, is_error}` | `cli.py` `_assistant` · `_user` · `CodexIngest._item` 같음 · rerun-v3 기록 키 6 같음 | ○ |
| §4-2 `trace.cli{rate_limits, api_retries, session_tools, mcp_servers, observed_model, api_key_source, num_turns, cli_ttft_ms}` · `timing.ttft_kind · cli_boot_ms · thinking_ms · ttft_ms_ex_boot · total_ms_ex_boot` · `cost.billed · usd_estimate` · `judge.mode` · `settings.input_cap_bytes: null` | rerun-v3 Q001 기록 전부 있음 | ○ |
| §3-4 Jev 꼴(`system_one(state, questions)` · `Choice(instructions, criteria)` · `Noul` · 255 · confidence · p_max · 1·2위 비 · seed) | `jev_client.py`(`CHOICE_MAX=255` · `choice_stats`) · `case3.py build_jev_questions` · `_shuffled` | ○ |
| §3-4-5 v1 경로(`hub_resolve` · `jev` · `hub_path` · `claude` · `hub_list: "cache"` · `trace.hub{resolve, path, tool, input, node_ids}` · `result_bytes`) | `case3.py run` 같음(`plan_path` · `two_procs` · `deps.intent_tools` · `section_tools`) | ○ |
| §3-4-2 `hub_rest.py` `peek` · `expand` 두 함수 | 아직 없음(`call` 9 도구만) — WP-3 | ○(새) |
| §3-5 (a) 근거 — Claude | 2.1.284 바이너리: `MAX_MCP_OUTPUT_TOKENS` env · 기본 `P=25000` · `_meta` 키 `anthropic/maxResultSizeChars` · 마커 「Output too large (」 「). Full output saved to:」 「exceeds maximum allowed tokens. Output has been saved to」 「Preview (first」 · `--disallowedTools` 있음 | ○ |
| §3-5 (a) 근거 — 허브 쪽 meta | `mcp` 2.3 `MCPServer.tool(name, title, description, annotations, icons, meta, structured_output)` — `meta` 인자 있음 | ○ |
| §3-5 (a) 근거 — Codex | 0.166.0 바이너리: `tool_output_token_limit` · `output_token_limit`(MCP 도구별) 키 있음 · 마커는 F-3 | △ |
| §3-6 `prompts/case2.md` intent 한 줄 | 지금 파일에 intent 언급 0(WP-2) · `deps.intent_tools` 는 case3 만 씀 | ○(새) |
| §4-1 단계 이름(`hub_resolve` · `jev#k` · `hub_peek#k` · `hub_expand#k` · `claude`) | `timing.stage(name)` 임의 이름 — 새 이름 추가 가능 · `web/app.js` 흔적 표시 자리 | ○ |

## 부록 B — fail-triage2 재계산(기준 2)

| 항목 | 스펙 · fail-triage2 | 재계산(`runs.jsonl` rerun-v3 182 · `fail-triage2.json`) |
|---|---|---|
| case2 도구 호출 | 662(허브) / 614(200) | 672 전체 = 허브 662 + bash 10 · 200 응답 614 |
| 잘림 | 100/614 | `case2_truncated_calls` 100(규칙 `rec_bytes < hub_bytes − 8`) · 1,700~2,300B 뭉침 93(check_conditions 47 · procedure_card 23 · resolve 17 · recommend 6) · `output_bytes` 중앙 1,775 |
| intent | 14/662 | 14 = I-01 9 · I-05 2 · I-03 1 · `none` 2 · case3 159/182 |
| C | 18 | `c_rows` 18(C1 10 · C3 8) |
| case3 크기 | 중앙 46,539 · p95 170,989 · 최대 280,705 | 같음 |
| bash | 10 문항 | Q078 · Q105 · Q150 · Q161 · Q165 · Q166 · Q170 · Q171 · Q174 · Q202 같음 |

## 부록 C — 보충(addendum) ↔ SPEC-006 v2 대응(기준 3)

| 보충 항목 | SPEC-006 조항 |
|---|---|
| peek ≤ 2KB → Jev Choice(섹션 · 이웃 ≤ 255) + 「충분」 → expand 고른 것만 | §3-4-1 흐름 · §3-4-2 |
| 걸음 상한 N(4) · 바이트 예산 B(20KB) | `WALK_MAX_STEPS` · `WALK_BYTE_BUDGET` · 예산 = expand 합 · 통째로 뺌 `budget_hit` |
| 「충분」 신뢰도 문턱 | `WALK_ENOUGH_MIN`(0.5 · W-3) |
| 못 찾으면 되돌아가기 = 의도 묶음 1회 | §3-4-3(3 사유 · `fallback_reason`) |
| 걸음마다 기록(노드 · 섹션 · 신뢰도 · 바이트 · ms) | §3-4-4 `trace.walk.steps[]` |
| 첫 글자 영향 측정 | §3-4-4 `claude` 시작 − `t0` |
| 비교 기준 = rerun-v3 182 · 같은 채점 | §3-4-4 · §7-6 |
| Jev 호출 수 · 시간 trace | `jev_calls` · `jev_ms_total` |
| case3 는 의도 묶음 · 동봉 자동 첨부 안 씀 | §3-4-1 「의도」 행(`sections=none` 꼴) |
| 허브 쪽(peek/expand 꼴 · A-1 · 끝 조건 도달 비율) | §7-7 W-1 · W-2 → SPEC-005 v3.2(W-1 경고) |
