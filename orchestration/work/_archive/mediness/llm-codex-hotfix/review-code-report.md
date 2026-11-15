# 리뷰 리포트 — llm-codex-hotfix / backend 리뷰 (WP-133 B·C·D codex 전환) (2026-11-13)

## 판정: PASS

필수 위반 0건. 선례(`meeting_v2_submission`)와 글자 단위로 일치하고, claude 분기는 provider 값만 설정값으로 바뀌었으며, codex 분기에 claude 전용 키가 0개다. 판정과 무관한 참고 2건과 실물 체크포인트 5건은 아래에 정리했다.

## 검수 범위
- diff: `origin/main`(`67b6a7dc`)..HEAD = 커밋 0. 워킹트리 수정 4 + untracked 1
  - `back/app/config.py` (+19) · `back/app/services/decision_gate.py` · `back/app/services/brief/synthesizer.py` · `back/app/services/weekly_report_pipeline.py` · 신규 `back/app/services/server_llm_submission.py` (157줄)
- 실행한 검사:
  - `git status --short` · `git diff origin/main` (경로 필터 `':!back/app'` → 변경 0)
  - `python -m py_compile` 5파일 → OK
  - import 1회(더미 env, 워커가 만든 scratchpad venv): `server_llm_submission` 을 **먼저** import하고(순환 탐지 순서) decision_gate·synthesizer·weekly_report_pipeline·pipeline_ingest_consumer·`app.main` 을 이어 import → `import-ok`
  - ad-hoc 조립 대조(파일 생성 없음): B/C/D 의 `submit_kwargs`·`provider_options` 키, `-c` 줄 전문, 로그 출력에 시크릿 원문이 남는지
  - open_kknaks `worker/codex_adapter.py`(`CODEX_ALLOWED_PROVIDER_OPTIONS`·`_build_command`·에러 경로) 대조
  - pytest 미실행, 테스트 미작성은 지적하지 않음(사용자 결정)

## 위반 (FAIL 사유)
- 없음

## 경미 (WARN)
- 없음

## 참고 (판정 무관 — 잠재 위험, 코디네이터 판단)
1. `back/app/services/decision_gate.py:719-720` — codex 분기에서 `model` 인자가 명시되면 `codex_kwargs["model"] = model` 로 덮어쓴다. 현재 `model=` 을 넘기는 호출부는 0건이다(`recommend_with_ai` → `_invoke` 는 2-arg, B′ partial 은 `max_turns`·`timeout_sec` 만 넘김, `scripts/eval_decision_gate.py` 에도 없음). 그래서 지금은 무해하다. 다만 나중에 누가 claude 모델명(`meeting_llm_batch`)을 명시해 넘기면 codex 가 metadata 400 으로 실패한다. 구 시그니처의 의미(모델 override)를 보존한 선택이라 위반은 아니다.
2. `back/app/services/server_llm_submission.py:37` — 바이트 로그는 logger `server_llm_submission` 의 INFO 레벨이다. back 프로세스(`app/main.py:27` `basicConfig(level=INFO)`, 스케줄러 경유 C·D·B)에서는 찍힌다. 하지만 `scripts/brief_backfill.py` 로 C 를 수동 1회 돌릴 때는 basicConfig 가 없어 INFO 가 출력되지 않을 수 있다(Python lastResort 핸들러는 WARNING 이상만 출력). Phase 3 에서 바이트 수치를 수동 run 으로 얻으려면 정기 06:00 run 의 back 로그를 보는 편이 확실하다.

## 기존 부채 (이번 판정 제외)
- `back/app/services/brief/synthesizer.py:42-44` `_TOKEN_REDACT_RE` 는 `sk-ant-`·`xoxp-`·`ATATT3` 만 잡고 `INTERNAL_AUTH_SECRET` 은 잡지 않는다. 다만 이번 diff 가 C 에러 문자열에 시크릿을 싣는 경로는 확인되지 않았다(아래 7번). 회의 v2 선례도 같은 구조다.
- codex 제출의 `provider_options.config` 는 Redis task payload 에 평문으로 `X-Internal-Auth` 를 싣는다. 이는 선례(회의 v2) 설계와 같고 이번에 새로 생긴 것이 아니다.

## 확인한 것 (PASS 근거) — 브리프 §4 항목별

1. **선례 일치** — PASS. `_config_overrides` 를 줄 단위로 대조한 결과, 순서(effort → approval_policy → mcp url/http_headers/enabled_tools → 툴별 approval_mode → 표면 4줄)·TOML 따옴표(`'approval_policy="never"'`, `f'…url="{…}"'`, `{{X-Internal-Auth="{…}"}}`, `enabled_tools=["a", "b"]` 의 `", "` 구분)·키 경로 `mcp_servers.{server}.tools.{name}.approval_mode="approve"` 가 `meeting_v2_submission.py:82-104` 와 글자 단위로 같다. `compose_prompt`·`redact_config_overrides` 는 선례를 import 해 재사용했다(재구현 없음). `ServerSubmission` 은 `MeetingSubmission` 과 모양이 같고 metadata 만 없다. 유일한 구조 차이는 MCP 줄이 `if mcp_tool_names:` 조건부라는 점인데, D 는 MCP 를 쓰지 않으므로 WP 대응표가 요구하는 차이다. `_strip_prefix` 는 방어용 추가이고, 현재 입력은 모두 접두어 없는 이름이라 no-op 이다.
2. **claude 전용 키 0** — PASS. 실조립 결과 B/C/D 모두 `provider_options` 키 = `{config, sandbox, skip_git_repo_check}` 이고 금지 7키와의 교집합은 ∅ 이다. 셋 다 open_kknaks `CODEX_ALLOWED_PROVIDER_OPTIONS` 의 부분집합이라 «Unsupported codex provider_options» 거부가 나지 않는다. top-level kwargs = `provider, model, provider_options, options`.
3. **claude 분기 보존** — PASS. B(`decision_gate.py:727-753`)·C(`synthesizer.py:583-605`)·D(`weekly_report_pipeline.py:530-541`)의 `client.submit(...)` 인자는 `origin/main` 과 토큰이 동일하다. 달라진 것은 `provider=` 값의 출처 하나뿐이다(B `resolved_provider`, C·D `settings.server_llm_provider`). `SERVER_LLM_PROVIDER=claude` 면 `"claude"` 가 그대로 들어간다. 바뀐 동작은 claude 분기에 로그 1줄(`log_final_prompt`)이 추가된 것뿐이며 WP Phase 1 의 요구사항이다.
4. **경로별 값** — PASS.
   - B: `ALLOWED_TOOL_NAMES` 7종(read_file·repo_search·brief_search·decision_run_get·product_get·wbs_version_list·wbs_get, 접두어 없음) → `-c` 10줄 + 공통 6. effort `low`. `timeout_sec` 은 resolved 값(기본 300) 그대로.
   - C: 4종(`_BRIEF_MCP_TOOL_NAMES`, claude 분기 접두 4종과 같은 집합) · `medium` · 600. `client.result(timeout=600)` 은 그대로다.
   - D: MCP 줄 0, 공통 6줄만 · `low` · 300.
   - queue 는 셋 다 `settings.brief_queue` 그대로다.
   - 모델: `server_codex_model or landing_chat_model` → `or None`. 둘 다 빈 값이면 `model=None` 이고 `submit_kwargs` 가 키를 뺀다(실측 확인).
5. **B′ 호환** — PASS. `pipeline_ingest_consumer.py:165-169` partial 이 넘기는 `max_turns=25`·`timeout_sec=300` 은 시그니처(`max_turns: int | None`, `timeout_sec: int | None`)로 그대로 받는다. codex 분기는 `timeout_sec` 만 소비하고 `resolved_max_turns` 는 계산만 하고 쓰지 않는다. partial 이 `provider` 를 넘기지 않으므로 설정값을 따른다. 파서 `loads_json_robust` 는 그대로다.
6. **결과 처리 불변** — PASS.
   - B: `try/finally broker.close`·timings·`collect_stream_stats`·`status != "done"` → `GateCallFailed` 가 diff 밖이라 그대로다.
   - C: except → `_redact_tokens(str(exc)[:500])` → FAILED, status 검사, `lint_markdown`, `update_markdown_body` 가 그대로다. 새 코드(`build_codex_submission`·`log_final_prompt`)는 기존 `try` 안에 있어서, 예외가 나도 기존 FAILED 처리 경로를 탄다.
   - D: `try/finally` 와 이후 처리는 diff 밖이라 그대로다.
   - codex 경로의 프롬프트 변경은 `compose_prompt(system, user)` 하나뿐이다.
7. **비밀 유출** — PASS.
   - 바이트 로그는 `redact_config_overrides` 를 거친다. 실측: 로그 버퍼에 더미 시크릿 원문이 없다(`secret in log: False`).
   - claude 분기의 로그 줄에는 config 가 없다.
   - `GateCallFailed` 는 status·task_id 만 싣는다.
   - 어댑터 에러 경로를 보면 `_validate_options` 메시지는 키 이름만 담고, spawn 실패(`E2BIG` 포함)는 `str(OSError)` 라 argv 내용이 없다. 따라서 C 의 `brief_run.error` 에 시크릿이 저장되는 경로는 찾지 못했다.
8. **런타임 위험** — PASS.
   - import 순환 없음: `server_llm_submission → config, meeting_v2_submission → meeting_v2_session_tools → decision_gate_tools`(외부 import 없음)이고, 어느 것도 decision_gate·synthesizer·weekly 를 역참조하지 않는다. `server_llm_submission` 을 먼저 import 하는 순서로도 확인했다.
   - 속성명: `meeting_v2_mcp_server_key`·`meeting_v2_mcp_url`·`internal_auth_secret`·`landing_chat_model`·`server_codex_model_resolved` 가 모두 존재한다(실조립 성공).
   - async: `client.submit` 은 await 하고, 조립·로그는 동기 함수라 오용이 없다. `**submit_kwargs(plan)` 와 명시 kwarg(`prompt`·`queue`) 사이에 키 충돌도 없다.
   - `model_reasoning_effort=low` 는 엄격한 TOML 로는 bare 값이라 무효지만, 선례와 바이트 동일하고 운영 회의 v2 에서 정상 동작 중이다(codex `-c` 가 문자열로 폴백한다).
9. **범위** — PASS. `back/app/` 밖 변경 0. `action_runtime/llm/driver.py`·`mcp/`·`back/tests/`·`back/scripts/` 무수정. `pipeline_ingest_consumer.py` 도 무수정.
10. **실물 체크포인트** — 아래 절.

## 실물 체크포인트 (Phase 3 — 배포 후 첫 실호출에서 볼 것)

1. **바이트 로그**: back 로그에서 `server_llm final_prompt path=brief|decision_gate|weekly provider=codex bytes=N model=gpt-5.6-terra config=[...'mcp_servers.*.http_headers=<redacted>'...]` 를 찾는다. `provider=codex` 이고 `model` 이 의도한 핀인지 확인한다. 시크릿 원문이 보이면 즉시 중단한다.
2. **C E2BIG 근접**: Linux 는 단일 argv 문자열을 **`MAX_ARG_STRLEN` = 131072 B(128 KiB)** 로 제한한다. 이는 ARG_MAX 와 별개 한계이고, 회의 v2 는 147KB 에서 터졌다. C `bytes` 가 **~120,000 이상**이면 여유가 거의 없다. 기존 경고(`brief prompt body … exceeds ~100KB`)는 본문만 기준이라 system·템플릿 몫을 못 본다. 실패하면 `brief_run.error.llm` 에 `exit_code=127`·`Argument list too long` 계열이 남는다.
3. **C 본문 형태**: `brief_run.state=PUBLISHED` 여도 `markdown_body` 가 `# 📋 메디솔브 브리핑` 으로 **시작하는지**, 앞에 ```` ```markdown ```` 펜스나 머리말 산문이 없는지 눈으로 확인한다. `lint_markdown` 은 부분 문자열만 보므로 이를 잡지 못한다(WP Open Issues ③).
4. **MCP 실연결 (B·C)**: worker 로그나 stream 에서 `mcp_tool_call` 이벤트가 나오는지(C warmup `read_file_tool`, B 문서 조회) 확인한다. 툴 호출이 0이고 결과가 «문서를 못 읽었다» 류면 `http://mcp:28081/mcp` 도달성이나 X-Internal-Auth 를 의심한다. B 계측 `collect_stream_stats` 값이 0/누락인 것은 Open Issues ④ 로 예상된 현상이다.
5. **수동 backfill 로그 비가시**: `scripts.brief_backfill` 로 돌리면 INFO 바이트 로그가 안 보일 수 있다(참고 2). 바이트 수치는 정기 run 의 back 파드 로그로 확보한다.
