---
type: work
id: WORK-006
title: "실험 앱 공정성(B-1) · case3 Jev 재귀 탐색 — 전달 보장 · intent · 기록 검증 · 재실행(SPEC-006 v2)"
status: todo
product: procedure-hub
feature: phub-recommend
work_type: change
owner: "backend 워커(clinic_chat)"
roles:
  pm: "코디네이터"
  design: ""
  fe: ""
  be: "backend 워커"
  qa: "reviewer_code 워커 · 코디(재실행 발주 · 확인 시험 승인)"
  ops: ""
progress: 0
created_at: 2026-11-01
updated_at: 2026-11-01
depends_on:
  - "WORK-004(실험 앱 · 완료) · WORK-005(허브 v3 · 완료)"
  - "SPEC-005 v3.2(peek · expand · 도구 meta · intent 설명 — 코디가 v3.2 발주 보충 2 로 전달 · WP-3 · WP-1 ③ 전제)"
tags:
  - product/procedure-hub
  - feature/phub-recommend
  - doc/work
  - status/todo
links:
  spec: "orchestration/work/phub-recommend/SPEC-006.md (0.3.1 · §2-5 · §3-4~§3-7 · §4-2 · §4-4 · §7-6 · §7-7)"
  decisions:
    - "orchestration/work/phub-recommend/_RESUME.md §2 (11-01 「2차 분류 결과 → A+B 스펙 발주」 · 「case3 를 Jev 재귀 탐색으로 교체」)"
    - "orchestration/work/phub-recommend/phub-recommend-jev-walk-addendum.md"
  evals:
    - "reference/2026-10-30-hub-evals/build-out/fail-triage2.md · runs/batches/b202610311552-d39a4d.json(rerun-v3 · 비교 기준)"
---

# 실험 앱 공정성 · case3 교체

SPEC-006 **0.3.1(v2.1)** 의 바뀐 조항만 구현한다. 계약은 SPEC-006(앱) · SPEC-005 v3.2(허브 peek/expand · 도구 meta)가 갖고, 이 문서는 순서 · 파일 · 시험 · 끝 조건 · 검증 명령만 갖는다. 둘이 다르면 SPEC 을 따른다.

**비목표**: 허브 코드(SPEC-005 — 도구 meta · peek/expand 는 v3.2 쪽 WORK) · 프롬프트 공통부 · 채점 기준 · 질문 세트 · 화면 재설계(걸음 흔적 표시만) · push(코디 승인 뒤) · 배포.

## Meta

- 레포: `/Users/kknaks/orca/workspaces/clinic_chat/hub-evals`(브랜치 `kknaksss/hub-evals` · 공개 레포 `kknaks/clinic_chat`) — 여기서만 · 로컬 커밋 · **push 는 코디 승인 뒤**
- 허브 18005: **사용자 · 실험이 쓰는 중** — 띄우지도 끄지도 않는다 · 읽기 호출(GET · 조회 POST · MCP tools/call)은 허용 · 새 허브 빌드(v3.2) 재시작은 코디
- **실물 CLI 호출은 코디 승인 뒤**(구독 사용량) — WP-0 확인 시험 1회씩 · 그 밖은 모의(`tests/fake_hub` · 모의 CLI 이벤트 재생)
- 키 · 원장 · 기록 · `.env` 는 레포에 넣지 않는다(`test_repo_rules.py`) · 자식 env 키 지움 유지 · 기록에 키 · env 값 없음
- 사용자 포트 · 프로세스(3700 · 3800 · 8700 · 8800 · 54329 · `procedure-*`) 금지 · 실험 서버 18210
- WP 마다 **그 WP 시험만** · 전체 시험 · ruff 는 WP-4 끝에 한 번 · 재실행(WP-5)은 코디 발주
- 코드 표면은 **grep 전부**: `grep -rn "output_bytes\|tool_calls\|cap_text\|tool_result_max_bytes\|input_cap_bytes\|intent\|hub_path\|plan_path\|--tools\|mcp_servers\|MAX_MCP\|ttft_kind" clinic_chat tests web prompts` 결과 파일이 전부 아래 표에 있어야 한다(WP-4 검증 · 11-01 실행 결과 29 파일 — 표와 1:1)

## Work Summary

| Field | Value |
|---|---|
| Goal | case2(두 CLI)가 허브 응답 전체를 받고(잘림 0) · 허브 호출의 95% 이상에 `intent` 를 넘기고 · 격리 밖 도구 0 · case3 가 Jev 재귀 탐색으로 돌며 걸음마다 기록되고 · 검증 스크립트가 결정론으로 세며 · 182문항 재실행 전후 보고가 나온다 |
| Non-goal | 위 비목표 · 통과율 목표 숫자(사용자 보고 뒤 · W-4) |
| 완료 판정 | §Done Criteria |

## Scope · Code Surface

| 파일 | 새/고침 | SPEC-006 v2 |
|---|---|---|
| `clinic_chat/config.py` · `.env.example` · `README.md` | 고침 — `MCP_RESULT_MAX_CHARS` · `WALK_MAX_STEPS` · `WALK_BYTE_BUDGET` · `WALK_ENOUGH_MIN` · `TOOL_RESULT_MAX_BYTES` 기본 0 · 설명 | §2-5 · §3-4 · §3-5 |
| `clinic_chat/llm/cli_process.py` | 고침 — 자식 env 에 `MAX_MCP_OUTPUT_TOKENS`(키 지움은 그대로) | §3-5 |
| `clinic_chat/llm/cli.py` | 고침 — Claude `--disallowedTools Bash,Read,Grep,Glob,Edit,Write`(W-6) · Codex `-c tool_output_token_limit` · 도구별 `output_token_limit` · 도구 결과 마커 판정 → `truncated` · `delivered_bytes`(`output_bytes` 호환) · `intent_passed` · `stray`(허브 MCP 접두 밖 도구) · `trace.intent_ratio` · `trace.stray_tools` · `system/init.tools` 기록 | §3-5 · §3-6 · §4-2 |
| `clinic_chat/cases/loop.py` | 고침 — SDK 판 `cap_text` 상한 0 = 없음 · `delivered_bytes` · `intent_passed` 같은 칸 | §2-5 · §3-7 |
| `prompts/case2.md` | 고침 — intent 한 줄 + 의도 표 12(SPEC-005 §5-1 의도 열) | §3-6 |
| `clinic_chat/clients/hub_rest.py` | 고침 — `peek(node, intent)` · `expand(node, sections\|neighbor_ids, intent)` 두 함수(SPEC-005 v3.2 계약 · 안이 바뀌어도 case3 그대로) | §3-4-2 |
| `clinic_chat/cases/case3.py` | **교체** — 걸음 루프(§3-4-1) · Jev Choice「펼칠 것」+ Noul「충분」(2단 · seed · confidence) · 멈춤 4종 · 예산(통째로 뺌) · 되돌아가기(v1 경로 = 지금 `plan_path` · `run` 을 `fallback_*` 로 이름만 바꿔 보존) · `trace.walk` · 단계 이름 | §3-4 |
| `clinic_chat/cases/case1.py` · `case2.py` | 고침 — 기록 칸만(`delivered_bytes` · `intent_passed`) | §4-2 |
| `clinic_chat/runner.py` · `runs.py` · `timing.py` | 고침 — `settings` 새 칸 · `versions` · `trace.walk` 저장 · 단계 이름 `hub_peek#k` · `jev#k` · `hub_expand#k` | §4-2 · §3-4-4 |
| `clinic_chat/report.py` · `rerun_report`(보고서 생성기) | 고침 — 「intent 전달 비율」 · 「잘린 호출」 · 「격리 밖 도구」 · case3 `walk` 열(걸음 · bytes_total · 되돌아감 · Jev 호출 · 시간) | §3-6 · §4-4 · §7-6 |
| `clinic_chat/verify_runs.py`(새) | 새 — §4-4 검증(마커 · 허브 재호출 `hub_bytes` · intent 비율 · stray · walk · 공정성 바이트 · 두 번 같음) · 출력 레포 밖 | §4-4 |
| `clinic_chat/server.py` · `web/app.js` · `index.html` | 고침 — case3 흔적 「걸음 k · 노드 · 고른 것 · 신뢰도 · 바이트」 접기 · 되돌아감 표시 · `intent` · 잘림 표시 | §6 |
| `clinic_chat/deps.py` | 고침 — `intent_tools` · `section_tools` 에 peek · expand 등록 · 걸음 경로 `sections=none` 꼴 | §3-4 |
| `clinic_chat/batch.py` · `clinic_chat/rerun_report.py` · `clinic_chat/quality/judge.py` | 고침 — 배치 settings 새 칸 · 전후 보고 열(intent · 잘림 · stray · walk · C 비율) / judge 는 **영향 없음 — 확인만**(`tool_calls` 이름만 겹침) | §4-4 · §7-6 |
| `web/state.js` | 고침 — 걸음 흔적 · 잘림 · intent 상태 | §6 |
| **새 시험 폴더 `tests/phase8/`**: `test_cli_ingest.py`(새) · `test_case3_walk.py`(새) · `test_verify_runs.py`(새) · `test_prompts.py`(새 — 프롬프트 시험은 지금 없음) | 새 | §7-6 |
| 기존 시험(고침): `tests/phase3/test_case3.py` → **되돌아가기 경로 시험으로 이름 · 대상 바꿈**(`test_case3_fallback.py` · v1 흐름 = `fallback_*`) · `tests/phase2/test_loop.py`(`cap_text` 0 = 없음) · `tests/phase4/test_timing_runs.py`(단계 이름 · settings 칸) · `tests/phase7/test_mock_e2e.py`(case3 걸음 모의) · `tests/cli/test_cli.py` · `test_runner_cli.py` · `test_rerun_report.py` · `test_report.py`(새 칸 · 열) · `tests/phase1/test_repo_rules.py`(상수 · env 이름) | 고침 | §7-6 |
| 모의 · 보조(고침): `tests/fake_hub/__init__.py` · `fake_hub/gold.py`(peek · expand 모의) · `tests/fake_jev.py`(Choice「펼칠 것」· Noul「충분」 모의) · `tests/mock_server.py` · `tests/estimate_cost.py`(walk 단계 비용) / `tests/phase5/test_quality.py` · `tests/phase6/test_screen.py` 는 **영향 없음 — 확인만** | 고침 · 확인 | — |
| `build-out/work006-report.md`(레포 밖 · 프로필 `reference/2026-10-30-hub-evals/build-out/`) | 새 — WP 출력 원문 · 확인 시험 원문 · SPEC 과 다른 점 | — |

손대지 않는 것: 허브 레포 · 프롬프트 공통부 · 채점 프롬프트 · `quality/*` · 질문 세트 · 기록 파일(`runs/`) · `.env`.

## Execution

### WP-0 — 조사 확인 시험(코디 승인 뒤 실물 1회씩)

전제: 코디가 SPEC-005 v3.2 planner 쪽에 **허브 MCP 도구 12 `_meta["anthropic/maxResultSizeChars"]`** 가 들어간 빌드를 18005 에 띄움(없으면 Claude 쪽 시험은 「meta 없이」 한 번 더 돌려 두 결과를 나란히 적는다 — 그래야 (a) 채택 근거가 선다).

1. `system/init` 의 `tools` 칸을 기록해 `--tools ""` 때 남는 내장 도구 목록 확인(W-6) · `--disallowedTools` 추가 뒤 다시 확인
2. **Claude**: 큰 결과 도구 2(check_conditions `family:M8` · procedure_card `sections=all`)를 자식 env `MAX_MCP_OUTPUT_TOKENS=200000` + 허브 meta 로 1회 — `tool_result` 내용에 마커 없음 · `delivered_bytes == hub_bytes`(같은 입력 REST 재호출) · 경고 문구가 있으면 원문 기록
3. **Codex**: 같은 두 호출을 `-c tool_output_token_limit=200000`(+ 도구별)로 1회 — 마커 없음 · 바이트 같음 · 0.166 실물 마커 문자열(한도를 일부러 작게 한 호출 1회로 받아 둠 — 판정 규칙에 쓸 원문)
4. **마커 확정 절차**: Claude 는 한도를 일부러 작게(`MAX_MCP_OUTPUT_TOKENS=1000` · meta 없음) 한 호출 1회로 실제 마커 원문을 받고, Codex 는 `tool_output_token_limit=500` 호출 1회로 받는다 — SPEC §3-5 표의 **Claude 4 + 변형 3 · Codex 실물 후보 5**(「Warning: truncated output (original token count:」 · 「<truncated omitted_approx_tokens=」 · 「omitted_due_to_size_limit (overage_bytes=」 · 「 bytes omitted ...」 · 「 tokens truncated」 · 구조 칸 `_codex_executed_tool_call_truncated`) 중 **실제로 나온 것**을 `TRUNCATION_MARKERS` 상수로 고정 · 안 나온 후보는 상수에서 뺀다(없는 문자열로 판정하지 않음 · F-3)
5. 결과 표(provider × 도구 × 설정 × hub_bytes × delivered_bytes × 마커 × **문턱 실측값**(저장 · 잘림이 시작되는 글자 · 토큰 — W-3)) → `work006-report.md` · **잘림 0 이 아니면 escalation**(자동으로 (b) 프록시로 가지 않음 — SPEC §3-5)

완료 조건: 표 원문 · `TRUNCATION_MARKERS` 실물 고정(provider 별 원문) · 문턱 실측값 · 내장 도구 목록 · 설정값 확정(W-5)

### WP-1 — 전달 보장 구현

1. `config.py` · `cli_process.py` · `cli.py`: 설정 · env · Codex 플래그 · `--disallowedTools` · `TRUNCATION_MARKERS`(WP-0 고정값 · provider 별) 로 마커 판정(`truncated` · 마커 없음 + 바이트 작음 → `"unknown"`) · `delivered_bytes` · `stray` · `intent_passed`(값 ∈ I-01~I-12 일 때만 true · `none` 은 false) · `trace.intent_ratio` · `trace.stray_tools` · `intent_values{}`
2. `loop.py`: SDK 판 상한 0 = 없음(기본) · 같은 칸
3. ③ 허브 meta · `intent` 설명은 허브 몫(SPEC-005 v3.2) — 앱은 `system/init.mcp_servers` · `tools/list` 로 meta 가 있는지 **기동 확인 줄**에 「도구 meta 12/12」 를 낸다(없으면 경고 · 실험은 막지 않음)

시험(`tests/phase8/test_cli_ingest.py` — 모의 JSONL 재생): `TRUNCATION_MARKERS` 의 Claude 문자열(4 + 변형 3) · Codex 문자열(WP-0 고정분) 각각 → `truncated` true · `intent: "none"` → `intent_passed` false · 마커 없음 + 바이트 작음 → `"unknown"` · `stray`(mcp__hub 밖 이름) · `intent_passed` 셋 · env 에 `MAX_MCP_OUTPUT_TOKENS` 있고 키 없음 · Codex 인자에 `tool_output_token_limit` · Claude 인자에 `--disallowedTools` · SDK `cap_text` 0 이면 그대로

검증: `uv run pytest tests/phase8/test_cli_ingest.py tests/phase2/test_loop.py tests/cli/test_cli.py -q`

### WP-2 — intent

1. `prompts/case2.md` 한 줄 + 의도 표(판 sha 바뀜 → 기록 `versions.prompts.case2`) · Codex 판 같은 파일
2. 보고서 열 「intent 전달 비율」(케이스 · provider · 도구별) · 화면 호출 흔적에 `intent`

시험(`tests/phase8/test_prompts.py` — **새** · 프롬프트 시험은 지금 없음): 프롬프트에 I-01~I-12 12줄이 있고 SPEC-005 §5-1 의도 이름과 같음(표 fixture) · `tests/cli/test_report.py` · `test_rerun_report.py`: 모의 기록에서 `intent_ratio` · C 비율 열

검증: `uv run pytest tests/phase8/test_prompts.py tests/cli/test_report.py tests/cli/test_rerun_report.py -q`

### WP-3 — case3 Jev 재귀 탐색(교체) — SPEC-005 v3.2 peek/expand 가 모의로라도 있어야 시작

1. `hub_rest.py` `peek` · `expand`(v3.2 계약 · 모의 허브에 같은 꼴)
2. `case3.py` 교체: ① resolve ② Jev#0(의도 + 시작 노드 · 후보 없으면 vocab 에서) ③ 걸음 루프(peek → Choice「펼칠 것」+ Noul「충분」 → expand · 멈춤 4종 · 예산은 통째로 뺌 · 걸음당 이웃 ≤ 3 · 2단 Choice) ④ Sonnet 1회 입력(걸음 순서 · 안전 요약 노드당 1 · claude_contract 합집합) · 되돌아가기(v1 경로 보존 · `fallback_reason`)
3. `trace.walk` · 단계 이름 · 화면 흔적

시험(`tests/phase8/test_case3_walk.py` — 모의 Jev `tests/fake_jev.py` · 모의 허브 `tests/fake_hub/` · v1 시험은 `tests/phase3/test_case3_fallback.py` 로 옮겨 되돌아가기 경로만 검사): 멈춤 4종 각각 · 예산 넘는 expand 는 뺌(`budget_hit`) · 되돌아가기 3 사유 · 걸음 N 소진 · 이웃 2단 Choice(255 넘김) · seed 재현 · `walk` 칸 전부 · 단계 합 = total · Jev 오류 → 그 열만 오류 · 되돌아간 판은 `trace.hub` 있음 · 걸음 판은 `intent` 넘기되 `sections=none` 꼴(의도 묶음 · 동봉 안 붙음)

검증: `uv run pytest tests/phase8/test_case3_walk.py tests/phase3 tests/phase7 -q` · (키 있고 코디 승인 시) 실물 1질문 Jev 걸음 — 걸음 수 · 바이트 · ms 원문

### WP-4 — 기록 검증 스크립트 · 전체 검증

1. `verify_runs.py`(§4-4): 배치 · run_id 입력 · 마커(`TRUNCATION_MARKERS`) · 허브 재호출 `hub_bytes`(빌드 해시 같을 때만) · intent 비율(값 규칙) · stray · walk · 공정성 바이트 · **C 비율**(fail-triage2 §2 셈) · 두 번 같음 · 시험 `tests/phase8/test_verify_runs.py`
2. rerun-v3 배치(`b202610311552-d39a4d`)로 한 번 돌려 **기준선**: 잘린 호출 100 · intent 14/662(유효 12 · `none` 2) · bash 10 · C 18 이 그대로 나와야 함(fail-triage2 와 같은 숫자 — 다르면 스크립트 오류)
3. 전체 시험 · ruff · `tests/phase1/test_repo_rules.py` · 표면 grep(Meta) 결과 파일 ⊆ §Scope 표(누락 0)

검증:
```bash
uv run pytest -q && uv run ruff check .
uv run python -m clinic_chat.verify_runs --batch b202610311552-d39a4d --out <레포 밖>
```

완료 조건: 기준선 표 원문(fail-triage2 §5 와 일치) · 전체 시험 통과

### WP-5 — 재실행 · 비교 보고(코디 발주 · 사용자 구독 사용량)

1. **case2 182문항**(rerun-v3 와 같은 문항 · 같은 채점 · claude-cli) → `verify_runs` → 잘림 0 · intent ≥ 95% · stray 0 · `rerun_report` 전후(case2 열)
2. (Codex 판은 사용자 결정 뒤 — 10-30 「전체 실험은 나중에」)
3. **case3 걸음 182문항**(허브 v3.2 peek/expand 발행 · 코디 재시작 뒤) → `rerun_report` 전후(rerun-v3 case3 기준 · 되돌아간 판 따로) → 사용자 보고(W-4)

완료 조건: 두 보고서 · 검증 표 원문

## Done Criteria

- [ ] WP-0 확인 시험 표(Claude · Codex 각 실물 1회 · `TRUNCATION_MARKERS` 실물 고정 · 문턱 실측값 · 내장 도구 목록) · 잘림 0 또는 escalation 기록
- [ ] WP-1~3 시험 통과 원문 · 기동 확인 줄에 「도구 meta 12/12」
- [ ] `verify_runs` 기준선 = fail-triage2 §2 · §5 숫자(잘림 100 · intent 14 · bash 10 · C 18) · 두 번 바이트 같음
- [ ] 재실행 case2 182: 잘린 호출 0 · 대조 불가 0 · intent ≥ 95% · stray 0 · 전후 보고
- [ ] 재실행 case3 걸음 182: 전후 보고(통과율 · 「정보 없음」류 · C 비율 · 첫 글자 · bytes_total 중앙 · 되돌아감 · Jev 호출 · 시간) — 기준은 사용자(W-4)
- [ ] 전체 시험 · ruff · 레포 규칙 시험 통과 · 표면 grep 누락 0
- [ ] SPEC-006 v2 와 다르게 구현한 곳 0 — 있으면 목록 + `ask` 근거
- [ ] 로컬 커밋 · push 는 코디 승인 뒤 · `git status --short` 원문

## Rollback

로컬 커밋을 되돌린다. case3 v1 경로는 `fallback_*` 로 코드에 남아 있어 `WALK_MAX_STEPS=0` 이면 v1 경로만으로 돈다(되돌림 스위치). 허브는 건드리지 않음.

## Open Issues

- SPEC-006 §7-7 W-1~W-6 — W-1 · W-2 는 SPEC-005 v3.2 · W-3 · W-4 사용자 · W-5 · W-6 은 WP-0 결과로 닫음
- Codex 판 전체 재실행 여부는 사용자(10-30)

## Related

- SPEC-006 0.3.1 · SPEC-006.v1.md(보관) · review-spec006-v2-report.md · SPEC-005 v3.1(현행) · v3.2(작성 중) · WORK-004 · WORK-005 · `fail-triage2.md` · `cli-research.md` · `phub-recommend-jev-walk-addendum.md`
