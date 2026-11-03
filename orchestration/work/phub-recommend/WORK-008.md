---
type: work
id: WORK-008
title: "expand 를 걷기용으로 — fact 한 줄 목록 · peek bytes = 실제 · 이웃 n_facts · 크기 표 = 측정값(SPEC-005 v3.3)"
status: todo
product: procedure-hub
feature: phub-recommend
work_type: change
owner: "backend 워커"
roles:
  pm: "코디네이터"
  design: ""
  fe: ""
  be: "backend 워커"
  qa: "reviewer_code 워커 · 코디(18005 재시작 · rerun-v5 재실행)"
  ops: ""
progress: 0
created_at: 2026-11-01
updated_at: 2026-11-01
depends_on:
  - "WORK-007(v3.2 · 완료 · 코드 cc637a2 · 빌드 b031371c)"
  - "WORK-009(앱 · clinic_chat — 이 작업의 WP-1 · WP-2 뒤(peek bytes · n_facts 는 WP-2)에 시작 · heartbeat 「v3.3 꼴 확정」 · 아래 §순서 의존)"
tags:
  - product/procedure-hub
  - feature/phub-recommend
  - doc/work
  - status/todo
links:
  spec: "orchestration/work/phub-recommend/SPEC-005.md (0.3.4 · §3-0 W7-D · §5-0 · §5-0-1 표 · §5-13 C′ · §5-14′ · §5-16 · §6-4 v3.3 행 · §6-5 · §6-7 · §7 V-14~V-18 · §8)"
  decisions:
    - "orchestration/work/phub-recommend/phub-recommend-walk-fix-context.md (11-01 사용자 승인 「발주하자」)"
    - "orchestration/work/phub-recommend/phub-recommend-spec005-v33-brief.md"
  evals:
    - "orchestration/work/phub-recommend/spec005-v33-measure.py · .json (설계 측정 — 이 작업이 실물 코드로 다시 잰다)"
    - "reference/2026-10-30-hub-evals/runs/runs.jsonl (batch b202611011148-c6ed3a · rerun-v4 · case3 trace.walk)"
    - "backend/build-out/work007-report.md"
---

# expand 를 걷기용으로(허브 · SPEC-005 v3.3)

SPEC-005 **0.3.4(v3.3)** 의 바뀐 조항만 구현한다. 계약은 SPEC 이 갖고, 이 문서는 순서 · 파일 · 시험 · 끝 조건 · 검증 명령만 갖는다. 둘이 다르면 SPEC 을 따른다. 검수 PASS 뒤 구현 발주는 코디가 한다.

**하는 것**: T11 expand 기본 꼴 = fact 한 줄 목록(`facts[]{id, line, section, owner?, cut?, flags?, gap?}` · 1쪽 12줄 · `more` 셈 · `full` · `page` · `fact_ids` 원문 · `claude_contract{allowed: "facts_uncut", must_show_flags}`) · T10 peek `sections[].bytes` = 그 section 의 실제 expand 기본 꼴 REST 본문 바이트 · peek 이웃 줄 `n_facts` · `GOLD_SIZE_CAPS` = §5-0-1 v3.3 표(측정값) · W7-D1~D13 은 이미 코드에 있음(본문만 따라옴 — 코드 변경 없음 · 시험 기대값만 v3.3 표에 맞춤).

**비목표**: case2 도구 T1~T9 응답 꼴 · 동봉 · 다이어트 손잡이 변경(V-14 · §6-7 (g) 바이트 같음이 끝 조건) · 실버 · 시맨틱 · 브론즈 수정 · 앱(clinic_chat — 걸음 · 예산 · cut 줄 받기 · 바이트 셈 · 1쪽 · Jev 고름 = WORK-009 · V-15 · V-17 · V-18 은 코디 결정으로 닫힘 · V-16 열림) · Jev 규칙 · 프롬프트 · 채점 · 182문항 재실행(코디) · push · 배포. 정해진 결정(허브 LLM 없음 · 결정론 · 요약문 생성 없음 · 「답이 많은 곳」 추측 표시 없음)을 다시 열지 않는다. 18005 는 띄우지도 끄지도 않는다(측정은 `--inprocess` · 읽기 호출은 허용).

## 순서 의존 — WORK-009(앱 · clinic_chat)

| 이 작업 | 먼저/뒤 | WORK-009 | 왜 |
|---|---|---|---|
| WP-1 expand 꼴 · WP-2 peek `bytes` · `n_facts` 확정 + 공개 계약 시험 | **먼저** | 걸음 코드가 읽는 칸(`facts[].line` · `cut` · `more` · `page` · `full` · `fact_ids` · `claude_contract.allowed` · peek `bytes` · `n_facts`) | 앱은 SPEC-005 §5-16 대응표를 따른다 — 꼴이 서기 전엔 앱 시험이 고정할 것이 없다 |
| WP-4 발행 → **코디 18005 재시작** | **먼저** | 실물 걸음 · 재실행(rerun-v5) | 새 꼴이 서버에 있어야 앱 실물 확인 |
| — | 뒤 | V-15(닫힘 — cut 원문 받되 예산 포함) · V-16(고름 · 열림) · V-17(닫힘 — 앱도 허브와 같은 직렬화) · V-18(닫힘 — 걸음은 1쪽) | 허브는 칸만 낸다 — 정책 구현은 앱 |

→ 발주 순서(코디): WORK-008 WP-0~3 → WP-1 · WP-2 끝나면 heartbeat 「v3.3 꼴 확정」(WORK-009 착수 가능) → WP-4 발행 · 재시작 → WORK-009 → 코디 rerun-v5.

## Meta

- 코드: `/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-recommend`(브랜치 `kknaksss/phub-recommend` · 로컬 전용 · **push 금지**) · 명령은 `backend/` 에서 · 기준점 = `cc637a2`(WORK-007) — Phase 0 에서 `git log -1` · `git status --short` 깨끗 확인
- 입력 `$W` = `orchestration/work/phub-recommend`(읽기만 · `spec005-v33-measure.py` 는 **읽고 같은 셈을 실물 코드로 다시 적는다** — import 하지 않음) · 평가 `$E` = `reference/2026-10-30-hub-evals`(`runs/runs.jsonl` · `build-out/rerun-v4-vs-v3.json` · `build-out/recheck2/*` — **읽기만** · 새 파일은 `build-out/walk3/` · `fail-triage-scripts/walk3.py` · `test_walk3.py` 만 · `recheck2.py` 는 (b) 쪽 넘김 한 곳만 고침 — 아래 WP-3)
- 로컬 DB `phub-graph-postgres`(55434) · 사용자 포트 · 프로세스(3700 · 3800 · 8700 · 8800 · 54329 · `procedure-*`) 금지 · 외부 호출 없음
- 원장 인용 본문을 시험 · 문서에 옮기지 않는다 — fact id · 경로 · 바이트만. 시험 기대값은 실물 빌드에서 뽑는다(가상 문장 없음)
- WP 마다 **그 WP 시험만** 돌린다. 전체 시험 · ruff · 품질 · 재실행 측정은 WP-5 에서 한 번
- 숫자 손잡이는 전부 설정(`config.py` · `envs/gold.env.example`) — 새 손잡이 `GOLD_EXPAND_LINE_CHARS=40` · `GOLD_PEEK_ITEMS_PER_KIND=4` 유지 · `GOLD_EXPAND_SECTION_MAX=12` 는 뜻이 「1쪽 줄 수」로 바뀜 · 코드 상수로 박지 않는다

## Work Summary

| Field | Value |
|---|---|
| Goal | SPEC-005 §6-7 (a)~(h): expand 기본 꼴 section 1 중앙 ≤ 2,000 · p95 ≤ 5,000 · `full` ≤ 4,000/8,000 · peek bytes 차 0(6,140/6,140) · peek ≤ 2,500/8,000 · 걸음 재생 평균 ≥ 3.0 · 이웃 도달 ≥ 85% · 「자료에 없다」 case3 68 중 ≥ 5 · case2 도구 바이트 같음 · 품질 6/6 · 106/106 · 회귀 0 · 결정론 · 시험 |
| Non-goal | 위 비목표 · V-14 · V-16(열림) · V-15 · V-17 · V-18 정책 구현(앱) |
| 완료 판정 | §Done Criteria 전부 |

## Scope · Code Surface

표면 전수(WP-0 에서 아래 grep 으로 다시 세고 빠진 파일은 이 표에 더한다 — 「목록 N개」가 아니라 「쓰는 곳 전부」). 작성 때(cc637a2) 센 결과:

```bash
grep -rln "def peek\|def expand\b\|\.peek(\|\.expand(\|/peek\|/expand\|\"peek\"\|\"expand\"\|'peek'\|'expand'" app scripts tests docs envs
grep -rn "GOLD_PEEK_\|GOLD_EXPAND_\(SECTION\|NEIGHBORS\|PICK\|FACT_IDS\|LINE\)\|sections_bytes\|warm_sections\|section_ids" app scripts tests docs envs | cut -d: -f1 | sort | uniq -c
grep -rn "ExpandRequest\|PeekResponse\|INTENT_DESC_WALK\|GOLD_SIZE_CAPS\|GOLD_SIZE_GATE\|size_caps\|case3_path" app scripts tests envs | cut -d: -f1 | sort | uniq -c
grep -ln "expand\|peek" "$E"/fail-triage-scripts/*.py
```

| 파일 | 새/고침 | SPEC v3.3 |
|---|---|---|
| `app/modules/gold/tools.py`(knob 19곳 · `peek` · `expand` · `warm_sections` · `_node_fact_ids`) | 고침 — `expand` 기본 꼴(줄 · `owner` 생략 · `cut` · `flags` · `gap` · 쪽 · `more` · `by_unit{unit: n}` · `claude_contract{allowed, must_show_flags}` · `build{build_hash}` · `request` null 빼기 · `priority`/`use_first`/`sections{}`/`source.meta`/`sections_used` 없음) · `full` · `page` · `fact_ids` 원문 행 · `peek` items `n_facts` · `warm_sections` 가 **실제 expand 기본 꼴 바이트**를 노드 × section 마다 잼(`g.sections_bytes` 뜻 바뀜 · 공식 아님) · peek `claude_contract.rule` 유지 | §5-16 |
| `app/modules/gold/memory.py`(2곳) | 고침 — `sections_bytes` 주석 · 뜻(원문 합 → expand 바이트) | §5-16 |
| `app/modules/gold/config.py`(8곳) · `envs/gold.env.example`(7곳) | 고침 — `GOLD_EXPAND_LINE_CHARS=40`(새) · `GOLD_EXPAND_SECTION_MAX=12`(1쪽 줄 수) · `GOLD_SIZE_CAPS` = §5-0-1 v3.3 표 — 실물 키 이름(`config.py:80` · `envs/gold.env.example:63`) 그대로: `recommend` 29,000/43,000 · `procedure_card:unit` 12,000/24,000 · `procedure_card:family` 11,000/13,000 · `pair_check` 19,000/27,000 · `check_conditions` 17,000/24,000 · `compare` 33,000/43,000 · `combos` 22,000/26,000 · `neighbors` 10,000/25,000 · `resolve` 2,000/4,000 · `vocab` 8,000/16,000 · `peek` 2,500/8,000 · **`expand` 2,000/5,000 · `expand_full`(새 키) 4,000/8,000** · `case3_path` 키 삭제 | §5-0-1 · §5-16 |
| `app/schema/gold.py`(4곳 · `ExpandRequest`) · `app/router/gold.py`(3곳) · `app/modules/gold/mcp_server.py`(2곳) · `app/modules/gold/service.py`(1곳) · `app/swagger_docs/gold.py` | 고침 — `ExpandRequest` 에 `full: bool = False` · `page: int = 1(≥ 1)` · REST · MCP · service 인자 · 설명 문구(「한 줄 목록 · 원문은 full · fact_ids」) · `page` < 1 · `full` 아닌 값 4xx | §5-16 |
| `scripts/gold_e2e.py` | 고침 — expand 기본 · `full` · `fact_ids` · `page=2` 각 1회 · peek `bytes` == expand 본문 길이 1건 · REST ↔ MCP 같음 | §6-2 · §5-16 |
| `docs/gold-local.md` | 고침 — expand 꼴 한 단락(줄 · cut · 쪽 · full) · peek bytes 뜻 | — |
| `tests/test_gold_v32_walk.py`(knob 9곳) | 고침 — v3.2 꼴 기대값(`sections{s: {facts, more_ids}}` · `bytes` = 원문 합) → v3.3 | §6-4 |
| `tests/test_gold_tools.py`(286행 `GOLD_SIZE_CAPS` 주석 · `size_caps()["recommend"]` · `GOLD_SIZE_GATE=1` 판정) | 고침 — 기대값 · 주석을 v3.3 표로(recommend 29,000) | §5-0-1 |
| `tests/test_gold_v32_diet.py`(39행 `caps` · 154행 expand 표본) | 고침 — `GOLD_SIZE_CAPS` 기대값 = v3.3 표 · `case3_path` 없음 · expand 표본 꼴 | §6-4 |
| `tests/test_gold_v32_b186.py`((b) 추가 호출에 `expand` 를 쓰는 행) | 고침 — (b) 판정이 새 꼴에서도 닿게(쪽 넘김 포함 · 같은 section 은 1 추가 호출로 셈) · 145/155 유지 · strict xfail 10 그대로 | §6-5 (i) · §6-7 (g) |
| `tests/test_gold_mcp.py` · `tests/test_gold_v32_mcp_meta.py` · `tests/test_public_api_contract.py` | 고침 — expand 입력 스키마 `full` · `page` · 응답 칸 | §5-16 |
| **`tests/test_gold_v33_expand.py`(새)** | 새 — §6-4 v3.3 행 전부 | §6-4 |
| `$E/fail-triage-scripts/recheck2.py` | 고침(한 곳) — `reach_one_call` 의 `expand` (b) 를 쪽 넘김 포함으로(`more` 가 있으면 `page` 2… 같은 section) · 판정 식 · 나머지 그대로 · 고친 줄을 report 에 원문으로 | §6-7 (g) |
| `$E/fail-triage-scripts/walk3.py`(새) · `test_walk3.py`(새) · `$E/build-out/walk3/{walk3-report.{md,json}, sizes.json}`(새) | 새 — §6-7 (a)~(f) 를 **실물 코드**로(`spec005-v33-measure.py` 의 셈 · 재생 규칙 · 「자료에 없다」 식 · 사유 분류를 그대로 다시 적음 · import 안 함) | §6-7 |
| `backend/build-out/work008-report.md`(새) | 새 — WP 출력 원문 · §6-7 표 1:1 · SPEC 과 다른 점(있으면 ask 근거) | — |
| 영향 없음(작성 때 grep) | `$E/fail-triage-scripts/reach.py`(peek/expand 는 설명 문장만 · 그래프 BFS — 코드 경로 아님) · v1 `app/modules/graph/*` · raw 도구 · case2 도구 코드 경로(T1~T9) | — |

손대지 않는 것: `$W` 전부 · `$E/runs/` · `$E/build-out/` 기존 파일(recheck2 산출물 포함 — 새 산출은 `walk3/` · `recheck2` 재실행 산출은 `recheck2-report.v33.{md,json}` 새 이름으로) · `fail-triage*-scripts/` 의 다른 파일 · 기존 앱 · clinic_chat · 사용자 env.

## Execution

### WP-0 — 기준점 · 표면 전수 · 측정 스크립트(끝 조건 도구를 먼저)

1. `git log -1`(cc637a2 여야 함) · `git status --short` 깨끗 — 아니면 escalation
2. 표면 grep(위 4줄) 원문을 report 에 · Scope 표 밖 파일이 나오면 표에 더한다
3. `walk3.py`(SPEC §6-7): 입력 = 발행본(in-process `GoldClient.inprocess()` 또는 `RECHECK2_FRESH_BUILD` 꼴 메모리 빌드 — 발행 · 18005 손대지 않음) · `runs.jsonl` b202611011148-c6ed3a · `rerun-v4-vs-v3.json` · gold-export(새 빌드). 셈: (a) 6,140 쌍 · 476 걸음 호출(이웃 없는 것 따로) · 676 이 닿은 쌍 (b) `full` (c) peek bytes 차 (d) peek 1,071 (e) 걸음 재생(§6-7 규칙 1~5 · 앱 셈 바이트 `json.dumps(d, ensure_ascii=False)`) (f) 68행 · 사유 분류(방문 · section 안 고름 / 1쪽 밖 / n홉 / 연결 없음 · 시작 노드에서 홉 · 정책 B) · 시간 칸 분리
4. **기준선**: 지금 코드(cc637a2)로 walk3 한 번 → `walk3-report.baseline.{md,json}` — (a) 옛 꼴 = 6,733 / 20,863 · 476 기록 바이트 재계산이 기록과 475/476 같음(설계 측정과 대조) · (e) 옛 꼴 재생 평균 1.84 · 이웃 53.4%

시험(`test_walk3.py`): 두 번 바이트 같음(시간 칸 분리) · 기준선 476 재계산 = 기록 바이트(차 1건 이하 · 사유 = 정수/실수 직렬화) · 재생 규칙 고정 입력(걸음 2개짜리 기록 1판)으로 걸음 · 멈춤 · 큐 순서 · 68 = 식으로 뽑은 행 수

완료 조건: 기준선 리포트 · 시험 통과 · 표면 grep 원문

### WP-1 — T11 expand 걷기 꼴(§5-16)

1. `config.py` · env 예시: `GOLD_EXPAND_LINE_CHARS=40` · `GOLD_EXPAND_SECTION_MAX` 설명 = 1쪽 줄 수
2. `expand`: 기본 꼴(줄 규칙 · `owner` 생략 · `cut` · `flags` · `gap` · 쪽 · `more` · 계열 · 제품 단위 수준 section `by_unit{unit: n}` ≤ 4 + `units_more_n` · 봉투 `build{build_hash}` · `request` null 빼기 · `intent_used: null` · `claude_contract{allowed: "facts_uncut", must_show_flags}`) · `full=true`(`text` · `source{file, path}`) · `fact_ids`(그 노드 fact ∪ 계열 · 제품이면 펼친 단위 fact — `_node_fact_ids` · 원문 행 · 요청 순서 · 끝에 · 요청 section 의 줄과 겹치는 id 는 줄을 빼고 원문 행 하나만) · 이웃 줄 v3.2 그대로
3. 스키마 · REST · MCP · service · swagger: `full` · `page`(≥ 1 · 아니면 4xx) · 설명 문구
4. 줄 순서 = peek `n_facts` 의 순서(`g.section_ids` · A1-5) — 두 경로가 같은 목록을 읽는다

시험(`test_gold_v33_expand.py` 일부): 기본 꼴 칸 · 없는 칸(`priority` · `use_first` · `sections` · `source.meta` · `sections_used`) · fact id 응답 안 1회 · 줄 규칙(40 이하 원문 그대로 · 41자 fact 는 39 + 「…」 + `cut` — 실물 fact 에서 뽑은 id) · `owner` 생략/있음 실물 1건씩 · `gap` 실물 1건 · `page=2` = 13~24번째 · `more` · `full` · `fact_ids` 그 노드(∪ 펼친 단위) 아님 4xx · `sections` + `fact_ids` 겹침 = 원문 행 하나(id 한 번) · 65개 4xx · `page=0` 4xx · `intent=I-03` 넘겨도 `request` 빼고 같음 · REST ↔ MCP 같음 · 두 번 같음

검증: `DATABASE_URL=sqlite+aiosqlite:///:memory: uv run pytest tests/test_gold_v33_expand.py tests/test_gold_v32_walk.py -q`

완료 조건: 시험 통과 · 실물 응답 1건(꼴 확인용 · 원장 인용 본문 없이 칸 이름 · 바이트만) report 에

### WP-2 — T10 peek bytes · n_facts(§5-16)

1. `warm_sections`: 노드 × section 마다 **실제 T11 기본 꼴(1쪽 · `request{id, sections}` · intent 없이)을 만들어 REST 본문 바이트**(`json.dumps(…, ensure_ascii=False, separators=(",", ":"))` = FastAPI `JSONResponse` 와 같은 바이트 — 시험으로 확인)를 `g.sections_bytes` 에 · 적재 시간 측정(설계 0.1s · 1s 넘으면 report)
2. peek items `n_facts` = 그 이웃의 17 section fact 수 합 · 앞 4 유지 · 「답이 많은 곳」 표시 없음
3. REST · MCP 응답이 같은 바이트인지(MCP 는 텍스트 결과 · REST 본문과 같은 문자열) 확인

시험(`test_gold_v33_expand.py` 나머지): **전 6,140 쌍 `peek.sections[s].bytes == len(TestClient POST /expand 본문)` 차 0** · `n_facts` = 이웃 section 합(실물 3건) · peek 1,071 바이트 분포(중앙 ≤ 2,500 · p95 ≤ 8,000) · REST ↔ MCP 같음

검증: `uv run pytest tests/test_gold_v33_expand.py tests/test_gold_api.py tests/test_gold_mcp.py tests/test_public_api_contract.py -q`

완료 조건: 시험 통과 · peek 분포 · 적재 시간 · **heartbeat 「v3.3 꼴 확정」(WORK-009 착수 가능)**(§5-16 대응표가 실물과 1:1 임을 report 에)

### WP-3 — 크기 표 · 기존 시험 · recheck2 (b) 쪽 넘김

1. `GOLD_SIZE_CAPS` = §5-0-1 v3.3 표(위 Scope 값 · `case3_path` 삭제)
2. `test_gold_tools.py` · `test_gold_v32_diet.py` caps 기대값 · `test_gold_v32_walk.py` 꼴 기대값 · `test_gold_v32_b186.py` (b) 판정(쪽 넘김) · `test_gold_mcp.py` · `test_public_api_contract.py` 스키마
3. `recheck2.py reach_one_call` (b): 새 expand 꼴에서 fact 가 1쪽 밖이면 `more` 를 보고 `page` 를 올려 같은 section 을 다 본다(같은 section = 1 추가 호출로 셈 · 결정론 · 캐시) — 고친 줄 원문을 report 에

시험: 위 4 파일 · `test_recheck2.py`(5 · 그대로 통과)

검증: `uv run pytest tests/test_gold_tools.py tests/test_gold_v32_diet.py tests/test_gold_v32_walk.py tests/test_gold_v32_b186.py tests/test_gold_mcp.py tests/test_public_api_contract.py -q` · `$E` 에서 `python -m pytest fail-triage-scripts/test_recheck2.py -q`

완료 조건: 시험 통과 · b186 145/155 유지(strict xfail 10 그대로)

### WP-4 — 발행 · 측정 · 품질

1. 로컬 커밋(WP 단위) → 새 빌드(`gold_build.py` — 빌드 내용이 안 바뀌면 해시 b031371c 그대로일 수 있음 · 그대로면 발행은 코드만 바뀐 것 · report 에 사실대로) → 발행 → `gold_export.py` → heartbeat 「발행 완료 · 18005 재시작 요청」 · 재시작 전엔 `--inprocess`
2. `walk3.py --inprocess` 두 번(바이트 같음): §6-7 (a)~(f) — 설계 측정과 어긋나면 행마다 사유
3. `recheck2.py rerun --inprocess` → `recheck2-report.v33.{md,json}`: (g) T1~T9 응답 바이트가 WORK-007 `rerun-responses.inprocess.json` 과 같음(빌드 · 시간 칸 빼고 · 다르면 호출 목록) · (i) ≥ 145/155
4. 품질: `gold_quality_eval.py --gold inprocess` → 6/6 · 106/106 · Q106 · Q108~110 · 회귀 0 · 두 번 같음
5. 코디 재시작 뒤 `walk3.py --base-url http://127.0.0.1:18005`(읽기 호출) 1회 — in-process 와 같아야 함 · `gold_e2e.py --gold http://127.0.0.1:18005`

완료 조건: 리포트 3(walk3 · recheck2 v33 · quality) · 빌드 해시 · 18005 재시작은 코디(워커가 하지 않았음을 적음)

### WP-5 — 전체 검증 · 보고

1. `uv run pytest -q --ignore=tests/integration` · `ruff check .` · 기존 앱 시험 회귀 0
2. 표면 grep 다시(WP-0 그대로) — 결과 파일이 전부 Scope 표에 있고 · expand 응답에 `priority` · `use_first` · `source.meta` 잔존 0 · `case3_path` 잔존 0 · peek `bytes` 를 원문 합으로 쓰는 코드 0
3. `work008-report.md`: WP 출력 원문 · §6-7 표 1:1 · 설계 측정 대비 차 · SPEC 과 다르게 한 곳(있으면 `ask` 근거) · 남은 것(V-14 · V-16)

## Done Criteria

- [ ] WP-0~4 완료 조건 전부(출력 원문을 report 에) · 표면 grep 누락 0
- [ ] (a) expand 기본 꼴 section 1 — 6,140 쌍 · rerun-v4 이웃 없는 걸음 호출 둘 다 중앙 ≤ 2,000 · p95 ≤ 5,000 · 이웃 포함 · 676 쌍 보고
- [ ] (b) `full=true` 중앙 ≤ 4,000 · p95 ≤ 8,000
- [ ] (c) peek `sections[].bytes` = 실제 expand 본문 바이트 **6,140/6,140 차 0**
- [ ] (d) peek 1,071 중앙 ≤ 2,500 · p95 ≤ 8,000 · `n_facts` 있음 · 앞 4
- [ ] (e) 걸음 재생 평균 걸음 ≥ 3.0 · 이웃 노드 도달 ≥ 85% · 분포 · 멈춤 사유
- [ ] (f) 「자료에 없다」 case3 68 중 새 꼴 줄로 닿음 ≥ 5 · 사유 표(SPEC §6-7 (f) 와 같은 분류) · 행 목록
- [ ] (g) case2 도구 T1~T9 응답 바이트 = WORK-007 재실행과 같음 · recheck2 (i) ≥ 145/155((b) 쪽 넘김 포함)
- [ ] (h) 품질 6/6 · 106/106 · Q106 · Q108 · Q109 · Q110 · 회귀 0 · walk3 · recheck2 · 품질 두 번 바이트 같음 · ruff · 전체 시험
- [ ] REST ↔ MCP 같은 JSON(11 도구 + expand 새 인자) · `intent` 받되 무시(`intent_used: null`) 유지
- [ ] `git status --short` 원문 · push 0 · `$W` 변경 0 · `$E` 기존 파일 변경 = `recheck2.py` 한 곳(diff 원문)
- [ ] SPEC v3.3 과 다르게 구현한 곳 0 — 있으면 목록 + `ask` 합의 근거

## Rollback

push · 배포 없음. WP-0 기준점(cc637a2)으로 코드를 되돌리고 재시작(코디). 빌드 내용이 같으면 발행 포인터는 그대로 · 바뀌었으면 b031371c 로 되돌린다. 새 alembic 리비전 없음.

## Open Issues

- SPEC-005 §7 V-14(case2 더 줄이기 · 사용자) · V-16(Jev 고름 · 23행은 9단계) — 열림. V-15(cut 원문 받되 예산 포함) · V-17(앱도 허브와 같은 직렬화) · V-18(걸음은 1쪽)은 코디 11-01 결정으로 닫힘 · 구현은 앱(WORK-009)
- 「자료에 없다」 68 중 허브 꼴로 닿을 수 있는 몫은 설계 측정 5 — 나머지 32 는 고름 · 23 은 골드 fact 없음 · 6 은 되돌아감(§6-7 (f))
- rerun-v5(새 허브 + WORK-009 앱 · 182 문항)는 코디

## Related

- **WORK-009(앱)는 이 작업의 WP-1 · WP-2 뒤**(§순서 의존) · SPEC-005 0.3.4 · SPEC-005.v3.2.1.md(보관) · WORK-007 · work007-report.md · spec005-v33-measure.py/.json · phub-recommend-walk-fix-context.md · SPEC-006 v2 §3-4 · `_RESUME.md` §2
