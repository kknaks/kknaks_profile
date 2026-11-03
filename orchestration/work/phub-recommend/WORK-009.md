---
type: work
id: WORK-009
title: "case3 걷기 순서(첫 걸음 이웃 먼저 · 짧은 fact · 원문은 마지막) · stray 막기 · 비교 규칙(SPEC-006 v2.2)"
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
  qa: "reviewer_code 워커 · 코디(허브 v3.3 재시작 · 확인 시험 승인 · 재실행 2회 발주)"
  ops: ""
progress: 0
created_at: 2026-11-01
updated_at: 2026-11-01
depends_on:
  - "WORK-006(SPEC-006 v2.1 · 완료 · 앱 f8533ff · rerun-v4 b202611011148-c6ed3a)"
  - "WORK-008(SPEC-005 v3.3 · 허브 — expand 짧은 fact 꼴 · peek bytes 실제값 · 이웃 fact 수) — **꼴 확정이 먼저**(아래 §순서 의존)"
tags:
  - product/procedure-hub
  - feature/phub-recommend
  - doc/work
  - status/todo
links:
  spec: "orchestration/work/phub-recommend/SPEC-006.md (0.3.4 · §3-3 · §3-4-1~§3-4-8 · §3-5-1 · §3-6 · §3-7 · §3-8 · §4-2 · §4-4 · §4-5 · §7-8 · §7-9)"
  decisions:
    - "orchestration/work/phub-recommend/_RESUME.md §2 (11-01 「case3 걷기 살리기 발주」 · 「rerun-v4 결과」)"
    - "orchestration/work/phub-recommend/phub-recommend-walk-fix-context.md · phub-recommend-spec006-v22-brief.md"
  evals:
    - "orchestration/work/phub-recommend/spec006-v22-count.md · .py(근거 셈 · 결정론)"
    - "orchestration/work/phub-recommend/spec006-v24-recount.md · .py · .json(v2.4 — 받는 자리 정의 · 순서 표 order_v24 · 34 행 cover34 · backend venv)"
    - "orchestration/work/phub-recommend/review-spec006-v2.3-report.md(재검수)"
    - "orchestration/work/phub-recommend/review-v33-v22-report.md(검수 F-1~F-3 · W-9~W-16)"
    - "reference/2026-10-30-hub-evals/build-out/work006-report.md · verify-b202611011148-c6ed3a.md · rerun-v4-vs-v3.md"
---

# case3 걷기 순서 · stray 막기 · 비교 규칙

SPEC-006 **0.3.4(v2.4 · v2.2 · v2.3 포함)** 의 바뀐 조항만 구현한다. 계약은 SPEC-006(앱) · SPEC-005 v3.3(허브 짧은 fact 꼴 — WORK-008)이 갖고, 이 문서는 순서 · 파일 · 시험 · 끝 조건 · 검증 명령만 갖는다. 둘이 다르면 SPEC 을 따른다. 검수 PASS 뒤 구현 발주는 코디가 한다.

**비목표**: 허브 코드(WORK-008) · 프롬프트 공통부 · 채점 프롬프트 · `quality/*` 판정 · 질문 세트 · 화면 재설계(걸음 흔적 칸 추가만) · 통과율 목표 숫자(사용자 · W-4) · Codex 전체 재실행(사용자) · push(코디 승인 뒤). 정해진 결정(case3 = Jev 재귀 탐색 · 결정론 허브 · 입력 상한 없음 · 전달 보장 · intent 규칙 · 되돌아가기 v1 경로)을 다시 열지 않는다.

## 순서 의존 — WORK-008(SPEC-005 v3.3 · 허브)

| 이 작업 | 먼저/뒤 | WORK-008 | 왜 |
|---|---|---|---|
| WP-0 · WP-4 · **WP-5 의 1(비교 규칙 보고 열)** | **먼저 해도 됨** | — | 허브 꼴과 무관 · WP-5 의 2~3(verify 걸음 칸 · 전체 시험 · 표면 grep)은 WP-2 trace 칸에 기대므로 **끝에**(검수 W-13) |
| WP-1 `hub_rest.py` 짧은 꼴 · WP-2 걸음 규칙 · WP-3 Claude 넘김 꼴 | **뒤** | expand 짧은 fact 꼴 · peek `sections[].bytes` = 실제 expand 바이트 · 원문 받기 인자(`full` / `fact_ids`) 확정 | 앱 모의(`tests/fake_hub/gold.py`)가 고정할 꼴이 v3.3 이다 · 꼴이 서기 전에 쓰면 두 번 고친다 |
| T-2 예산 실측(WP-2 끝) | **뒤** | v3.3 빌드(로컬 커밋 · 허브 `--inprocess` 읽기 또는 코디가 18005 재시작) | SPEC-006 §3-4-6 표의 추정을 실물로 바꿈(§7-9 X-2) |
| WP-6 재실행 2회 | **뒤** | v3.3 발행 · 코디 18005 재시작 | 같은 허브 빌드로 2회 |

→ 발주 순서(코디): WORK-008 꼴 확정(heartbeat 「v3.3 꼴 확정」) → WORK-009 WP-0~5 → v3.3 발행 · 재시작 → WP-6.

## Meta

- 레포: `/Users/kknaks/orca/workspaces/clinic_chat/hub-evals`(브랜치 `kknaksss/hub-evals` · 기준점 `f8533ff` · 공개 레포 `kknaks/clinic_chat`) — 여기서만 · 로컬 커밋 · **push 는 코디 승인 뒤** · WP-0 에서 `git log -1` · `git status --short` 깨끗 확인
- 허브 18005: 사용자 · 실험이 쓰는 중 — 띄우지도 끄지도 않는다 · 읽기 호출만 허용 · v3.3 빌드 재시작은 코디
- **실물 CLI 호출은 코디 승인 뒤**(구독 사용량) — S-1 · S-3 확인 시험만 · 그 밖은 모의(`tests/fake_hub` · `tests/fake_jev.py` · 모의 CLI 이벤트 재생)
- 키 · 원장 · 기록 · `.env` 는 레포에 넣지 않는다(`tests/phase1/test_repo_rules.py`) · 원장 인용 본문을 시험 · 문서에 옮기지 않는다(fact id · 경로만)
- 사용자 포트 · 프로세스(3700 · 3800 · 8700 · 8800 · 54329 · `procedure-*`) 금지 · 실험 서버 18210
- WP 마다 **그 WP 시험만** · 전체 시험 · ruff 는 WP-5 끝에 한 번 · 재실행(WP-6)은 코디 발주
- **코드 표면은 grep 전부**(11-01 실행 · 31 파일 — 아래 §Scope 표와 1:1 · WP-5 에서 다시 돌려 누락 0 확인):

```bash
grep -rlE "walk|WALK_|stray|TRUNCATION_MARKERS|peek|expand\(|prompts\.load|system_for|prompts\.versions|delivered_bytes|hub_bytes|NONE_ENOUGH|neighbors_by_kind" \
  clinic_chat tests web prompts .env.example README.md | grep -v __pycache__ | sort
```

## Work Summary

| Field | Value |
|---|---|
| Goal | case3 가 첫 걸음에 의도별 이웃 종류(§3-4-6 표)를 먼저 고르고 · 짧은 fact 로 걸어 예산 20KB 안에서 걸음 3~4 · 이웃 노드에 닿고 · 마지막에 고른 fact 만 원문으로 받아 출처 노드 · use_first 순으로 Sonnet 에 넘기며 · case2 접두 없는 도구 이름 호출이 0 이 되고 · 보고서가 case1 대비 차와 2회 평균을 낸다 |
| Non-goal | 위 비목표 |
| 완료 판정 | §Done Criteria |

## Scope · Code Surface

grep 31 파일(위 명령) + grep 에 안 걸리지만 바꾸는 파일 6(`walk_order.json` · `prompts/case3.md` · `batch.py` · `README.md` · `tests/fake_jev.py` · `tests/phase8/test_walk_order.py` — 검수 W-14).

| 파일 | 새/고침 | SPEC-006 v2.2 |
|---|---|---|
| `clinic_chat/config.py` · `.env.example` | 고침 — `WALK_SECTIONS_PER_STEP` 2 · `WALK_NEIGHBORS_MAX` 3(지금 `case3.py` 상수 → 설정) · `WALK_FIRST_SECTION_MAX` 1 · `WALK_FIRST_SECTION_MAX_BY_INTENT` `I-02:2,I-03:2,I-04:2,I-05:2` · `WALK_FULL_BYTE_BUDGET` **15000** · `WALK_FULL_FACTS_MAX` 64 · `WALK_ORDER_TABLE` · `TRUNCATION_MARKERS` 는 그대로(Claude 비움) | §2-5 · §3-4-1 · §3-5-1 |
| `clinic_chat/cases/case3.py` | 고침 — **바이트 셈 `_hub` = compact(`separators=(",", ":")`) · 걸음 경로 peek · expand 에 `intent` 안 넘김 · `bytes_mismatch`(v2.3 F-1)** · 걸음 1 = 이웃 먼저(v2.4 edge kind 표 + 계열 S 는 `key_family` · 제품 S 는 `product_unit` 늘 더함으로 선택지 거름 · 계열 · 제품 S 의 섹션 expand `by_unit` unit 을 그 section 으로 대기열(Jev 섹션 고름 없이 단위 expand) · peek n > 앞 4 종류는 `expand(neighbor_kinds)` 목록(`hub_list#1-j` · 예산 밖) · 이웃 Choice + 섹션 Choice(의도별 상한) 한 요청 · 「충분」 없음 · 라벨에 `n_facts` · `bytes` · `step1_options` 기록) · 대기열 · S 로 돌아옴(peek 재사용) · 걸음당 섹션 ≤ 2 · peek bytes 로 미리 거름 · 넘으면 그 섹션만 빼고 계속 · 예산 멈춤 새 정의 · 「충분」 은 fact ≥ 1 뒤 · ⑤ 원문 받기(`hub_full#n`) · §3-4-7 넘김 꼴 · `trace.walk` 새 칸 · 되돌아가기 조건 그대로(`fallback_*` 보존) | §3-4-1 · §3-4-3 · §3-4-4 · §3-4-7 |
| `clinic_chat/cases/walk_order.json`(새 · grep 밖) | 새 — 프로필 레포에 **커밋된** `spec006-v24-recount.json` 의 `order_v24`(의도별 edge kind 순서 · `first_section_max_2` · `unit_link` · 규칙 문자열)을 그대로 복사(스크립트를 다시 돌리지 않음 — 돌리면 프로필 레포 파일을 덮어씀 · 검수 W-14) · 판 sha = `order_table_sha` | §3-4-6 |
| `clinic_chat/clients/hub_rest.py` | 고침 — 걸음용 `peek` · `expand` 는 `intent` 인자를 보내지 않음(되돌아가기 경로 함수는 그대로 보냄 · v2.3 F-1) · 섹션 호출 본문 = `{"sections":[s]}` 만(None · 기본값 칸 없음 · v2.4 W-1) · 계열 · 제품 응답의 `by_unit` · `units_more_n` 읽기 · `expand(node, neighbor_kinds=[…])` · `expand` 가 v3.3 기본 꼴(`facts[]{id, line, section, owner?, cut?}` · `more` · `claude_contract{allowed, must_show_flags}`)을 읽고 · 원문 받기(`expand(node, fact_ids=[…])` — SPEC-005 0.3.4 §5-16) · peek `sections[].bytes` = 실제 바이트 · 이웃 `n_facts` · 앞 4 | §3-4-2 |
| `clinic_chat/cases/case2.py` · `clinic_chat/prompts.py` · `prompts/case2.md` | 고침 — 프롬프트 자리표 `{tool:<이름>}` · `prompts.system_for(case, provider)` 가 provider 별로 채움(claude-cli `mcp__hub__` · sdk 짧은 이름 · codex-cli 는 S-3 전까지 짧은 이름 그대로) · 한 줄 「설명 · 응답의 짧은 이름 = 위 도구」 · `prompts.versions(provider)` = 채운 글의 sha · v3.3 확정 뒤 「expand 는 한 줄 fact · 원문은 `fact_ids`」 한 줄 | §3-3 · §3-8 |
| `prompts/case3.md`(grep 밖) | 고침 — 「`quotable: false` 줄은 인용하지 않음」 한 줄 · 「facts 는 rank 순(허브 줄 순서 = 우선순위) · source 는 출처 노드」 | §3-4-7 |
| `clinic_chat/cases/case1.py` | **확인만** — `system_for` 호출부가 provider 인자를 받게 바뀌면 같이(원장 도구 3 은 이름 자리표 대상 아님 — case1 프롬프트에 도구 이름이 없으면 고침 없음) | §3-8 |
| `clinic_chat/llm/cli.py` · `clinic_chat/cases/loop.py` | 고침 — `mark_call` 에 `stray_kind`(`bare_hub` = 허브 도구 11 짧은 이름이거나 그것으로 시작 · 그 밖 `foreign`) · `stray_fixed_next`(다음 호출이 같은 도구 접두 이름) · `trace.stray_by_kind` · **stray 호출의 CLI 원문 이벤트 한 줄을 `trace.cli.stray_events[]` 에 남김**(S-2 확인용 · 입력 꼴) | §3-8 · §4-2 |
| `clinic_chat/runner.py` | 고침 — `settings` 새 칸(`walk_*` · `order_table_sha`) · `versions.prompts` 를 provider 별 채운 글 sha 로 | §4-2 |
| `clinic_chat/verify_runs.py` | 고침 — (v2.4) 「34 행 · 1홉 몫 / 0홉 몫」(fixture = 커밋본 `spec006-v24-recount.json cover34.rows` · S 같은 행만 문턱) · `bytes_mismatch` · `list.bytes` · 이름 「이웃 fact 도달」 / 「이웃 peek 도달」 · 걸음 칸(`steps_n` 중앙 182 기준 · 멈춤 비율 · 이웃 도달 · 2홉 · `full.bytes` · `excluded` · `filtered_by_budget` · 되돌아감 사유) · `stray_kind` 별 · 잘림 판정에 근소 차이 · 기록 오류 · 대조 불가 따로(지금 구현 확인 · 이름 맞춤) | §3-5-1 · §4-4 |
| `clinic_chat/rerun_report.py` · `clinic_chat/report.py` | 고침 — 「case1 대비 차」 열 · `--batches a,b`(2회 평균 · 두 회 차 · case1 뒤집힘 비율) · case3 걸음 열 새 칸 · stray 두 열 | §4-5 · §4-4 |
| `clinic_chat/quality/judge.py` · `clinic_chat/quality/word_check.py` | **확인만** — `prompts.load("judge"/"extract")` 만 씀 · `system_for` 서명 바뀌어도 영향 없음을 확인 | — |
| `clinic_chat/quality/raw_tools.py` | **확인만** — grep 이 내부 함수 이름 `walk` 로 잡음 · 영향 없음 | — |
| `web/app.js` · `web/state.js` | 고침 — case3 흔적에 걸음 `phase`(첫 · 대기열 · 돌아옴) · 이웃 fact 도달 · 원문/한 줄 표시 · stray 두 종류 | §6 · §3-4-4 |
| `clinic_chat/batch.py`(grep 밖) | 고침 — 배치 settings 새 칸 · 같은 판 2회 배치 라벨(`--label …-r1` · `-r2`) 안내 | §4-5 |
| `README.md` | 고침 — v2.2 env · 비교 규칙 한 단락 | §8 |
| `tests/fake_hub/__init__.py` · `tests/fake_hub/gold.py` | 고침 — v3.3 짧은 꼴 모의(peek `bytes` = 모의 expand 실제 바이트 · `line` · `more` · 원문 받기) | §3-4-2 |
| `tests/fake_jev.py`(grep 밖) | 고침 — 걸음 1 두 질문(이웃 Choice · 섹션 Choice) · 「충분」 없는 요청 모의 | §3-4-1 |
| `tests/phase8/test_case3_walk.py` | 고침 — 아래 WP-2 · WP-3 시험 | §3-4 |
| `tests/phase8/test_cli_ingest.py` | 고침 — `stray_kind` · `stray_fixed_next` · `stray_events` | §3-8 |
| `tests/phase8/test_prompts.py` | 고침 — 자리표 채움 · provider 별 sha · 채운 글의 도구 이름 ⊆ 그 provider 세션 도구 목록 | §3-8 |
| `tests/phase8/test_verify_runs.py` | 고침 — 걸음 · stray 칸 · rerun-v4 기준선 | §4-4 |
| `tests/phase8/test_walk_order.py`(새 · grep 밖) | 새 — `walk_order.json` = `spec006-v22-count.py` 결과(같은 입력이면 같은 표) · 규칙 재현 | §3-4-6 |
| `tests/cli/test_report.py` · `tests/cli/test_rerun_report.py` | 고침 — case1 대비 차 · 2회 평균 열 | §4-5 |
| `tests/phase3/test_case3_fallback.py` | 고침 — 되돌아가기 사유 그대로 · 「첫 expand 초과」 · 「없음(충분)」 사유가 더는 안 나옴 | §3-4-3 |
| `tests/phase4/test_timing_runs.py` | 고침 — 단계 이름 `hub_full#n` · settings 칸 | §3-4-4 |
| `tests/phase7/test_mock_e2e.py` | 고침 — 모의 e2e 걸음 꼴 | §3-4 |
| `tests/phase6/test_screen.py` | 고침 — 흔적 칸(phase · 원문/한 줄) | §6 |

손대지 않는 것: 허브 레포 · 프롬프트 공통부 · 채점 · 이름 뽑기 프롬프트 · `quality/*` 판정 · 질문 세트 · 기록 파일(`runs/`) · `.env`.

## Execution

### WP-0 — 기준점 · 순서 표 · 기준선

1. `git log -1`(= `f8533ff`) · `git status --short` 깨끗 · 표면 grep 원문(31) 저장
2. `walk_order.json` 만들기: 프로필 레포에 커밋된 `orchestration/work/phub-recommend/spec006-v24-recount.json` 의 `order_v24` 를 그대로 복사(스크립트는 돌리지 않음 · 손으로 고치지 않음) · `order_table_sha`
3. `verify_runs` 를 rerun-v4 배치로 돌려 **기준선**: 걸음 중앙 1 · 예산 멈춤 116/182 · 이웃 도달(fact) 49/148 · peek 도달 79/148 · 되돌아감 34(no_start 11 · no_facts 23) · stray 15(새 칸이면 bare_hub 15 · foreign 0) — `spec006-v22-count.md` §A · §D 와 같은 숫자여야 함(다르면 스크립트 오류)

시험: `tests/phase8/test_walk_order.py`(`walk_order.json` == 커밋본 `order_v24` · 의도 1홉·1쪽 행 < 10 → 전체(`_all`) · `first_section_max_2` = I-02 · I-03 · I-04 · I-05 · `unit_link` = family → key_family · product → product_unit) · `tests/phase8/test_verify_runs.py`(rerun-v4 기준선 숫자는 기록 파일이 레포 밖이라 **고정 fixture 몇 판으로** 같은 셈을 검사)

검증: `uv run pytest tests/phase8/test_walk_order.py tests/phase8/test_verify_runs.py -q`

### WP-1 — 허브 짧은 꼴 소비(WORK-008 꼴 확정 뒤)

1. `hub_rest.py`: v3.3 `expand` 짧은 꼴 · 원문 받기 · peek `bytes` 실제값(SPEC-005 v3.3 칸 이름 그대로 — SPEC-006 §3-4-2 표는 최소 칸)
2. `tests/fake_hub/gold.py`: 같은 꼴 모의 · peek `bytes` 는 모의 expand 를 실제로 직렬화한 바이트(가짜 숫자 아님)

시험(v2.3 F-1 포함): **모의 허브 · 실물 허브(18005 읽기 호출 또는 inprocess) 모두 peek `sections[].bytes` == 앱 `_hub` 가 센 그 섹션 expand 바이트(차 0 · 전 섹션 · `intent` 없이)** · 앱 셈 = `json.dumps(…, ensure_ascii=False, separators=(",", ":"))` · 걸음용 `peek` · `expand` 요청에 `intent` 칸 없음(되돌아가기 경로 요청엔 있음) · `expand(neighbor_kinds)` 응답 읽기 · `line` ≤ 40자(넘으면 앞 39자 + 「…」 · `cut: true`) · `fact_ids` 원문 받기 응답에 `text` · `page` 는 걸음에서 안 부름

검증: `uv run pytest tests/phase8/test_case3_walk.py -q -k hub`

### WP-2 — 걸음 규칙(§3-4-1)

1. 걸음 1: v2.4 edge kind 표의 그 의도 종류(+ 계열 S `key_family` · 제품 S `product_unit`)만 선택지(없으면 `GOLD_PEEK_KIND_ORDER` 다음 종류) · peek n > 앞 4 인 표 종류는 `expand(neighbor_kinds)` 목록을 더함(예산 밖 · `walk.list`) · 이웃 Choice + 짝 Noul(≤ 3) + 섹션 Choice(≤ 1 · I-02 · I-03 · I-04 · I-05 는 2 · 「없음」) 한 요청 · 라벨 `n_facts` · `bytes` · 「충분」 Noul · 「없음(충분)」 없음 · expand 순서 = 이웃 slim → 섹션 · `step1_options` 기록
2. (v2.4) 계열 · 제품 S 의 섹션 expand 응답 `by_unit{section: {unit: n}}` 의 unit 을 「그 section」 으로 대기열 뒤에(`by_unit_queued`) — 그 걸음은 peek 뒤 Jev 섹션 고름 없이 `expand(unit, sections=[section])` · 걸음 상한 · 예산 안
3. 걸음 2~N: 대기열 앞 · 비면 S 로 돌아옴(peek 재사용 · `peek_reused`) · 선택지에서 남은 예산 넘는 섹션 미리 뺌(`filtered_by_budget`) · 섹션 ≤ 2 하나씩 · 실제 바이트 넘으면 그 섹션만 `excluded` 하고 다음으로 · 예산 멈춤 = 남은 예산 < 최소 섹션 바이트 그리고 이웃 선택지 없음 · 「충분」 은 걸음 2~ 이고 모은 fact ≥ 1 · 고른 이웃은 대기열 뒤
4. 되돌아가기 조건 그대로(no_start · peek_failed · no_facts)
5. **T-2 예산 실측**(v3.3 빌드 있을 때 · 허브 `--inprocess` 읽기 또는 18005 읽기 호출 · compact 셈): rerun-v4 걸음 판 148 의 기록된 (노드 · 섹션 · 이웃) 선택을 v3.3 실물로 다시 불러 섹션 호출 바이트 · 이웃 slim(1장 · 배열 · 걸음 2~ 이웃 포함) · `expand(fact_ids)` cut 받기 응답 · `neighbor_kinds` 목록 응답 바이트 · **목록 호출 수 · ms(첫 글자 영향 · W-6)** · `by_unit` 이 34 · 461 행 목표 단위를 앞 4 에 내는지(X-13 · 보고만)의 중앙 · p95 · 「4걸음 합」 표를 다시 냄 → SPEC-006 §3-4-6 표(섹션 2,037 / 2,630 · slim 250 / 1,014 · 배열 752 / 2,306 · 원문 예산 15,000 vs 재생 p95 14,376)와 다르면 **보고**(기본값 바꿈은 코디 · SPEC 개정) · Jev 호출 없음

시험(`tests/phase8/test_case3_walk.py` · 모의 Jev · 모의 허브):
- 걸음 1 이웃 선택지 ⊆ v2.4 표 edge kind(+ 단위 규칙)의 (peek items ∪ `neighbor_kinds` 목록) · n ≤ 4 종류는 목록 호출 없음 · n > 4 종류는 목록 호출 1 · 목록 바이트는 `bytes_total` 에 안 들어감 · 섹션 상한 I-02 · I-03 · I-04 · I-05 = 2 · 그 밖 1 · 계열 S 인데 표에 key_family 가 없는 의도에서도 key_family 이웃이 선택지에 있음 · by_unit unit 이 그 section 으로 대기열에 들어가고 그 걸음 Jev 요청에 섹션 Choice 가 없음 · 종류에 이웃이 없을 때 다음 종류로 채움 · 이웃 0 이면 섹션만
- **§3-4-8 재현 fixture(v2.4 정의)**: 모의 허브에 Q106 꼴(계열 S · 목표가 단위 노드 줄 1쪽 · `key_family`) · Q114 꼴(concern S · `treats` 이웃 줄 1쪽) · 앞 4 밖 이웃이 목표인 꼴을 두고 `step1_options` 에 목표 노드가 들어감 · 목표가 이웃 줄 2쪽에만 있으면 「뜸」 으로 안 셈 · 계열 S 자신의 섹션에는 단위 fact 줄이 없음(모의도 실물 꼴대로)
- 걸음 1 Jev 요청에 「충분」 · 「없음(충분)」 이 없음
- 대기열 순서 = Choice 1위 → 짝 Noul 높은 순 · 비면 S 로 돌아옴 · 돌아올 때 peek 호출 없음
- 남은 예산 넘는 섹션은 선택지에 없음 · 실제 바이트가 넘는 섹션은 빼고 다음 섹션을 담음(멈추지 않음) · 담을 것 없고 이웃 없음 → `budget`
- 「충분」 ≥ 0.5 라도 fact 0 이면 안 멈춤 · 걸음 2 에서 fact ≥ 1 · 0.5 → `enough`
- 걸음당 섹션 ≤ 2 · 이웃 ≤ 3 · 걸음 ≤ 4 · seed 재현 · 2단 Choice(255 넘김) 그대로
- 되돌아가기 3 사유 · `walk` 새 칸 전부 · 단계 합 = total

검증: `uv run pytest tests/phase8/test_case3_walk.py tests/phase3/test_case3_fallback.py tests/phase4/test_timing_runs.py -q`

### WP-3 — 원문 받기 · Claude 넘김 꼴(§3-4-7)

1. ⑤ 원문: `cut` 줄만 · rank 순(걸음 순 → expand 호출 순 → 응답 `facts[]` 순 · 중복 제거) · 출처 노드별 `expand(node, fact_ids)` 1회 · `WALK_FULL_BYTE_BUDGET` · `WALK_FULL_FACTS_MAX` · 못 받은 cut 줄 = `quotable: false`
2. 넘김 JSON = §3-4-7 꼴(`facts[]{id, text|line, section, source{id, kind, name, edge}, step, rank, cut?, quotable?}` · `neighbors` · `safety` · `claude_contract{rule, allowed_fact_ids, must_show_flags}`) · `prompts/case3.md` 두 줄

시험: 잘리지 않은 줄은 원문 받기 대상 아님(줄 = 원문) · 원문 예산 넘으면 뒤 cut 줄은 `quotable: false` 이고 `allowed_fact_ids` 에 없음 · `allowed_fact_ids` = 잘리지 않은 줄 + 받은 원문 · `source` 가 받은 걸음 노드 · `rank` = 걸음 → 호출 → 줄 순 · 원문 받기 호출 수 = cut 줄이 있는 출처 노드 수 · `rule` = peek 의 규칙 문장

검증: `uv run pytest tests/phase8/test_case3_walk.py -q -k full`

### WP-4 — stray 막기(§3-8)

1. `prompts/case2.md` 자리표 · `prompts.system_for(case, provider)` · 채운 글 sha
2. `cli.py` · `loop.py`: `stray_kind` · `stray_fixed_next` · `stray_by_kind` · `stray_events`(CLI 원문 이벤트 · 키 · env 값 없음 확인)
3. 보고서 · 화면 두 열

시험: claude-cli 로 채운 프롬프트의 도구 이름이 전부 `mcp__hub__` 11 중 하나(정규식으로 추출 → ⊆ 모의 `system/init.tools`) · sdk 는 짧은 이름 · codex 는 지금 글 그대로 · provider 별 sha 다름 · 모의 이벤트: `procedure_card`(접두 없음) → `bare_hub` · `fixed_next` true · `Bash` → `foreign` · `check_conditions_placeholder` → `bare_hub`(허브 이름으로 시작)

검증: `uv run pytest tests/phase8/test_prompts.py tests/phase8/test_cli_ingest.py -q`

**확인 시험(코디 승인 뒤 실물)**:
- **S-1**(§7-9 X-7): rerun-v4 stray 15 문항(Q031 · Q066 · Q089 · Q109 · Q115 · Q125 · Q149 · Q164 · Q167 · Q172 · Q175 · Q197 · Q234 · Q235 · Q239) × 2회 · case2 만 · 새 프롬프트 → `stray_by_kind` 합 0 이면 「프롬프트 짧은 이름」 원인 닫힘 · 0 아니면 `stray_events` 원문을 붙여 escalation(추측으로 다른 고침 안 함)
- **S-2**: S-1 에서 stray 가 나오면 `stray_events` 의 `tool_use.input` 원문으로 「빈 입력 · 배열이 문자열」 이 CLI 기록 그대로인지 확인(SPEC §3-8 사실 4 의 추정 닫기)
- **S-3**(§7-9 X-5 · 사용자가 Codex 를 열 때만): codex-cli 1질문 — 세션 도구 이름 원문 기록 → 자리표 채움 규칙 확정

### WP-5 — 비교 규칙 · 보고 · 전체 검증

1. `rerun_report`: 「case1 대비 차」(항목별) · `--batches a,b` 2회 평균 · 두 회 차 · case1 뒤집힘 비율 · 「전 1회」 표시 · case3 걸음 열(§7-8 칸)
2. `verify_runs`: §4-4 v2.2 행 · 두 번 바이트 같음
3. 전체 시험 · ruff · `tests/phase1/test_repo_rules.py` · 표면 grep 다시(결과 ⊆ §Scope 표 · 누락 0)
4. `verify_runs` 에 「34 행 · 1홉 몫 / 0홉 몫」 셈(SPEC §7-8 · §4-4 · v2.4 정의): 34 행 목록(문항 · 자리 · 목표를 1쪽에 가진 노드 · 섹션)은 프로필 레포 커밋본 `spec006-v24-recount.json` 의 `cover34.rows` 를 fixture 로 복사 · 그 판 S 가 rerun-v4 와 같은 행만 문턱 분모 · 판정 = `walk.step1_options` ∋ 그 노드(1홉) / 그 섹션(0홉) — 「받는 자리」 는 `g.section_ids` 1쪽(허브 `_node_fact_ids` 아님)

시험: 모의 배치 둘(같은 문항 · 판정 일부 다름)로 Δ · 평균 · 뒤집힘 비율 값 고정

검증:
```bash
uv run pytest -q && uv run ruff check .
uv run python -m clinic_chat.verify_runs --batch b202611011148-c6ed3a --out <레포 밖>   # WP-0 기준선 그대로
```

### WP-6 — 재실행 2회 · 보고(코디 발주 · 사용자 구독 사용량)

전제: v3.3 발행 · 코디 18005 재시작 · WP-0~5 로컬 커밋.

1. 182문항 × **2회**(같은 앱 커밋 · 허브 빌드 · 프롬프트 판 · claude-cli · 라벨 `…-r1` · `…-r2`) → `verify_runs` 각각 → `rerun_report --batches r1,r2 --before-label rerun-v4`
2. §7-8 표 칸을 채워 보고(걸음 중앙 · 예산 멈춤 · 이웃 fact 도달 · 34 행 1홉 몫 · 0홉 몫 · stray · 되돌아감 · 크기 · case1 대비 차 2회 평균 · case1 뒤집힘) → 사용자(W-4 · X-3 · X-4)

## Done Criteria

- [ ] WP-0 기준선 = `spec006-v22-count.md` 숫자(걸음 중앙 1 · 예산 116 · 이웃 fact 도달 49/148 · 되돌아감 34 · stray 15) · `walk_order.json` = 셈 결과
- [ ] WP-1~4 시험 통과 원문 · T-2 실측 표(SPEC §3-4-6 추정과 나란히 · 다르면 보고)
- [ ] S-1 확인 시험 결과(stray 0 또는 escalation + 원문)
- [ ] 전체 시험 · ruff · 레포 규칙 시험 통과 · 표면 grep 누락 0
- [ ] 재실행 2회: **걸음 중앙 ≥ 3 · 예산 멈춤 ≤ 30%(두 회 모두) · 이웃 fact 도달 ≥ 80%(X-4 추천) · 34 행 1홉 몫 = S 같은 분모 행 전부 뜸(셈 8/8) · 0홉 몫 · 합 보고(셈 4 · 12) · `bytes_mismatch` 0 · stray 0** · 되돌아감 · 크기 · case1 대비 차(2회 평균) 보고
- [ ] SPEC-006 v2.2 와 다르게 구현한 곳 0 — 있으면 목록 + `ask` 근거
- [ ] 로컬 커밋 · push 는 코디 승인 뒤 · `git status --short` 원문

## Rollback

로컬 커밋을 되돌린다. 걸음 규칙은 설정으로 v2 쪽에 가깝게 돌릴 수 있다(`WALK_FIRST_SECTION_MAX` · `WALK_SECTIONS_PER_STEP` 값) · `WALK_MAX_STEPS=0` 이면 v1 경로만(되돌림 스위치 그대로). 허브는 건드리지 않음.

## Open Issues

- SPEC-006 §7-9 X-1~X-14 — X-1 은 WORK-008 · X-2 · X-13 은 T-2 · X-5 · X-7 은 S-3 · S-1 · S-2 · X-10 · X-14 는 허브(SPEC-005 다음 판 · 코디 전달) · X-3 · X-4 · X-6 · X-8 · X-12 는 사용자 · 코디 · X-9 · X-11 닫힘

## Related

- SPEC-006 0.3.4 · SPEC-006.v2.3.md · SPEC-006.v2.2.md · SPEC-006.v2.1.md(보관) · SPEC-005 v3.3 · WORK-008(허브) · WORK-006 · `spec006-v22-count.md` · `work006-report.md` · `phub-recommend-walk-fix-context.md`
