---
type: work
id: WORK-007
title: "허브 응답 다이어트 · B 잔여 186 조항 · peek/expand · MCP 전달 계약(SPEC-005 v3.2)"
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
  qa: "reviewer_code 워커 · 코디(18005 재시작 · 실패 문항 재실행 · CLI 실물 확인 승인)"
  ops: ""
progress: 0
created_at: 2026-11-01
updated_at: 2026-11-01
depends_on:
  - "WORK-005(v3 · 완료 · 코드 c95b37a · 빌드 d3a1abd5)"
  - "SPEC-006 v2 §3-4-2 · §3-5 · §3-6(앱 쪽 소비자 — WORK-006 WP-0 · WP-3 가 이 작업의 WP-5 · WP-4 결과를 쓴다 · 아래 §순서 의존)"
tags:
  - product/procedure-hub
  - feature/phub-recommend
  - doc/work
  - status/todo
links:
  spec: "orchestration/work/phub-recommend/SPEC-005.md (0.3.3 · §3-0 W5-D · §4-3 F-D′ · F-F · §5-0-1 · §5-0-2 · §5-13 C1′~C14′ · §5-14′ · §5-16 · §6-4 · §6-5 · §6-6 · §8)"
  decisions:
    - "orchestration/work/phub-recommend/_RESUME.md §2 (11-01 「2차 분류 결과 → A+B 스펙 발주」 · 보충 case3 = Jev 재귀 탐색 교체)"
    - "orchestration/work/phub-recommend/phub-recommend-jev-walk-addendum.md"
  evals:
    - "reference/2026-10-30-hub-evals/build-out/fail-triage2.md · .json · rerun-report.md · runs/runs.jsonl(batch b202610311552-d39a4d)"
    - "backend/build-out/work005-report.md"
---

# 허브 응답 다이어트 · B 잔여 186 · peek/expand · MCP 전달

SPEC-005 **0.3.3(v3.2.1)** 의 바뀐 조항만 구현한다. 계약은 SPEC 이 갖고, 이 문서는 순서 · 파일 · 시험 · 끝 조건 · 검증 명령만 갖는다. 둘이 다르면 SPEC 을 따른다. 검수 PASS 뒤 구현 발주는 코디가 한다.

**비목표**: 실버 · 시맨틱 · 브론즈 수정(A 54 는 9단계) · 앱(clinic_chat · SPEC-006 v2 — 걸음 · 예산 · 되돌아가기 · 기록) 수정 · Jev 규칙 · 프롬프트 · 채점 · 실패 문항 재실행(코디) · push · 배포. 정해진 결정(허브 LLM 없음 · 결정론 · slim · G13 · 충돌 하나 · case3 교체)을 다시 열지 않는다. 18005 는 띄우지도 끄지도 않는다(측정은 `--inprocess` · 읽기 호출은 허용).

## 순서 의존 — WORK-006(SPEC-006 v2 · 실험 앱)과의 계약 · 순서(검수 F-3)

| 이 작업 | 먼저/뒤 | WORK-006 | 왜 |
|---|---|---|---|
| WP-4 peek · expand 응답 꼴 확정(SPEC §5-16 · 006 §3-4-2 최소 칸 대응표 · `intent?` 받되 무시) | **먼저** | WP-3 걸음(모의라도 `hub_rest.py` 의 `peek` · `expand` 두 함수) | 앱은 005 §5-16 꼴을 따른다(코디 11-01) — 꼴이 서기 전엔 앱 시험이 고정할 것이 없다 |
| WP-5 MCP meta · intent 문구 → 로컬 커밋 → WP-6 발행 → **코디 18005 재시작** | **먼저** | WP-0 확인 시험(Claude CLI 가 잘림 없이 받는지 — meta 빌드가 18005 에 있어야 (a) 근거가 섬) | meta 는 서버 도구 정의에 있어야 CLI 가 읽는다 |
| WP-6 5 CLI 실물 확인 | 뒤(또는 대신) | WP-0 기록 | 같은 호출 — 006 쪽 기록이 먼저 있으면 그 출처로 대신 |
| `intent?` 인자 · 이웃 꼴 `neighbors_by_kind` | 합의됨 | 006 §3-4-1 · §3-4-2 | 005 §5-16 이 정본 · 006 은 따름 |

→ 발주 순서(코디): WORK-007 WP-0~5 → 발행 · 재시작 → WORK-006 WP-0 · WP-3 → WORK-007 WP-6 측정 · WORK-006 재실행. WP-4 · WP-5 를 끝내면 heartbeat 에 「peek/expand 꼴 확정 · meta 빌드 준비」 를 적는다.

## Meta

- 코드: `/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-recommend`(브랜치 `kknaksss/phub-recommend` · 로컬 전용 · **push 금지**) · 명령은 `backend/` 에서 · 기준점 = `c95b37a`(WORK-005 마지막) — Phase 0 에서 `git log -1` · `git status --short` 깨끗 확인
- 입력 `$W` = `orchestration/work/phub-recommend`(읽기만) · 평가 `$E` = `reference/2026-10-30-hub-evals`(`build-out/fail-triage2.json` · `fail-triage2-scripts/` · `fail-triage-scripts/recheck.py` · `runs/runs.jsonl` — **읽기만** · 새 파일은 `build-out/recheck2/` · `fail-triage-scripts/recheck2.py` · `reach.py` · `test_recheck2.py` 만)
- 로컬 DB `phub-graph-postgres`(55434) · 사용자 포트 · 프로세스(3700 · 3800 · 8700 · 8800 · 54329 · `procedure-*`) 금지 · 외부 호출 없음(WP-6 CLI 실물 확인만 코디 승인 뒤 1회)
- 원장 인용 본문을 시험 · 문서에 옮기지 않는다 — fact id · 경로만. 시험 기대값은 실물 빌드에서 뽑는다(가상 문장 없음)
- WP 마다 **그 WP 시험만** 돌린다. 전체 시험 · ruff · 품질 · 재실행 측정은 WP-7 에서 한 번
- 숫자 손잡이는 전부 설정(`config.py` · `envs/gold.env.example`)이고 기본값 = SPEC §5-0-1 표 · §5-13 C′ 표. 코드 상수로 박지 않는다

## Work Summary

| Field | Value |
|---|---|
| Goal | (i) rerun-v3 실제 호출 676 재실행에서 B 186 중 조항 닿는 161 행의 ≥ 90%(145+) 를 허브 응답에 id 또는 원문으로 (ii) 도구별 기본 응답 중앙 · p95 ≤ SPEC §5-0-1 표(case3 경로 호출 중앙 ≤ 20KB · p95 ≤ 60KB) (iii) C3 fact 없는 행 5 가 기본 응답 원문 칸에 + Q003 2 는 C1′ 로 빠짐 (iv) 품질 6/6 · 106/106 · 회귀 0 · 결정론 · 시험 (v) peek ≤ 2KB · expand ≤ 8KB 중앙 (vi) 걸음 ≤ 4 도달 ≥ 90% (vii) MCP 도구 14 meta · intent 문구 |
| Non-goal | 위 비목표 · 닫지 않는 행 25(SPEC §8) · A · C1 · 미분류 · case3 걸음 실행(앱) |
| 완료 판정 | §Done Criteria 전부 |

## Scope · Code Surface

표면 전수(F-7 방식 · WP-0 에서 grep 으로 다시 세고 빠진 파일은 이 표에 더한다 — 「목록 N개」가 아니라 「쓰는 곳 전부」):

| 파일 | 새/고침 | SPEC v3.2 |
|---|---|---|
| `app/modules/gold/tools.py` | 고침 — `Shape` 예산(4/24 · 명시 12 · `budget_explicit`) · `limit_facts` 전 section `more_ids` · `node_sections` by_unit id 만 · 단위 ≤ 4 · `units_more` · 단위 → 제품 fact id · `sections_index` 17 · `_c1_site_caution` 같은 계열 · 부위 체인 · 잎 id 전부 · `_c2_checks` 전 등급 id · `question_conditions` 원문 · `edges` · `relations_of` → `relations_all`(저장 엣지 수준 · 종류 무관 · ≤ 20 · `global`) · `_c4_products` basis · `_c6_complications` 잎 id · `_c7_combos` ≤ 8 · `refs` 전부 · `index` · `_c14_evidence_refs` 계열 · 제품 = 펼친 단위 전부 · `envelope` `index{}` · `claude_contract.priority` · `use_first` · `pair_check` 쌍 상한 12 · claims 원문 2 · `reasons` id 전부 · `check_conditions` 펼침 8 · `checks[].edges` · `compare` C10′ 멤버 판정(`field == members` · 입력 펼친 단위) · 원문 ≤ 6/멤버 · `why_roles` · `recommend` `why[].role` · `n` 만 · `combos` refs 전부 · `neighbors` 이웃 동봉 없음 · **`peek` · `expand`(새 함수)** · `INTENT_CAPS` 를 표 이하로 | §5-0-1 · §5-3~§5-9 · §5-13 · §5-14′ · §5-16 |
| `app/modules/gold/memory.py` · `build.py` | 고침 — section 바이트 합(`sections_bytes[(node, section)]` · peek 용 · 빌드 때) · F-D′ 잎 fact(`combos[].consult_copy.patientExplanation` 7 · RC-RE-R1~R7 · §4-3) · `counts.v3_facts.fd2_patient_explanation` = 7 · 이웃 종류 고정 순서 표 | §4-3 F-D′ · §5-16 |
| `app/modules/gold/config.py` · `envs/gold.env.example` | 고침 — `GOLD_SECTION_FACTS_MAX=4` · `GOLD_RESPONSE_FACTS_MAX=24` · `GOLD_EXPLICIT_FACTS_MAX=12` · `GOLD_CARD_BY_UNIT_MAX=4` · `GOLD_EXPAND_MAX_UNITS=8` · `GOLD_PAIR_EXPAND_MAX=12` · `GOLD_COMPANION_*`(SC 3 · CLAIMS 2 · RELATIONS 20 · COMBOS 8 · EVIDENCE 10/1 · NOTCOND 5/2) · `GOLD_PAIR_CLAIMS_MAX=2` · `GOLD_COMPARE_MEMBER_TEXT_MAX=6` · `GOLD_EXPAND_SECTION_MAX=12` · `GOLD_EXPAND_NEIGHBORS_MAX=20` · `GOLD_PEEK_ITEMS_PER_KIND=8` · `GOLD_MCP_RESULT_MAX_CHARS=200000` · 도구별 상한 표(`GOLD_SIZE_CAPS` json — 측정 대조용) | §5-0-1 · §5-0-2 · §5-13 · §5-16 |
| `app/modules/raw/config.py` · `mcp_server.py` · `envs/*.example` | 고침 — `RAW_MCP_RESULT_MAX_CHARS=200000` · 도구 3 `meta` | §5-0-2 M-1 · §5-12 |
| `app/modules/gold/mcp_server.py` · `app/router/gold.py` · `app/schema/gold.py` · `app/swagger_docs/gold.py` · `app/modules/gold/service.py` · `container.py` | 고침 — 도구 9 `meta={"anthropic/maxResultSizeChars": …}` · `INTENT_DESC` 문구(M-2 · 상수 하나) · 서버 `instructions` 한 줄 · **T10 `GET /nodes/{id}/peek` · T11 `POST /nodes/{id}/expand` · MCP `peek` · `expand`**(`intent?` 받되 무시 · meta 있음) · `GoldToolService.peek · expand` | §5-0-2 · §5-16 |
| `scripts/gold_quality_eval.py` · `scripts/gold_e2e.py` | 고침 — 어댑터가 `index` · `sections_index` · `more_ids` 를 읽어도 채점 식 그대로 · E2E 에 peek · expand 각 1회 · `claude_contract.priority` 검증 | §6-1 · §6-2 |
| `docs/gold-local.md` | 고침 — 다이어트 손잡이 · peek/expand · meta 한 단락 | — |
| `tests/test_gold_v3_*.py`(기존 5 · 기대값 갱신) · `tests/test_gold_tools.py` · `test_gold_api.py` · `test_gold_mcp.py` · `test_public_api_contract.py` · **`tests/test_gold_v32_diet.py` · `test_gold_v32_b186.py` · `test_gold_v32_walk.py` · `test_gold_v32_mcp_meta.py`(새 4)** | 새 · 고침 | §6-4 v3.2 행 4 |
| `$E/fail-triage-scripts/recheck2.py`(새 · 판정 식은 recheck.py 와 같은 식을 다시 적음 · import 안 함) · `reach.py`(새) · `test_recheck2.py`(새) · `$E/build-out/recheck2/{replay2.json, recheck2-report.{md,json}, reach-report.{md,json}, sizes.json}`(새) | 새 | §6-5 · §6-6 |
| `backend/build-out/work007-report.md` | 새 — WP 출력 원문 · 측정 표 · SPEC 과 다른 점(있으면 ask 근거) | — |

손대지 않는 것: `$W` 전부 · `$E/build-out/fail-triage*.{md,json}` · `fail-triage-scripts/{replay,triage,recheck}.py` · `fail-triage2-scripts/` · `runs/` · `app/modules/raw/tools.py`(meta 는 mcp_server 만) · 기존 앱 · v1 graph · 사용자 env · clinic_chat.

## Execution

### WP-0 — 기준점 · 표면 전수 · 측정 스크립트(끝 조건 도구를 먼저)

1. `git log -1`(c95b37a 여야 함) · `git status --short` 깨끗 — 아니면 escalation
2. **표면 grep 전수**(결과를 report 에 · Scope 표에 없는 파일이 나오면 표에 더한다):
   ```bash
   grep -rln "sections\|intent\|companion\|more_ids\|by_unit\|claude_contract" app scripts tests docs
   grep -rn "mcp.tool(\|@mcp.tool" app
   # 골드 앱이 import 하지 않는 모듈은 「영향 없음」으로 표에 적고 meta 대상 아님(검수 W-4) — 지금 잡히는 무관 모듈: app/model/canonical_publication.py · app/modules/retrieval/{application,domain}.py · app/schema/knowledge_retrieval.py · tests/test_retrieval_domain.py · v1 app/modules/graph/mcp_server.py(도구 6 · 골드 앱 마운트 아님) → meta 대상은 골드 9 + peek · expand 2 + raw 3 = 14 로 고정
   grep -rn "GOLD_\(SECTION\|RESPONSE\|CARD\|EXPAND\|COMPANION\|PAIR\)" app scripts tests envs docs
   grep -rn "PAIR_EXPAND_MAX\|COMPARE_UNITS_MAX\|INTENT_CAPS\|INTENT_DESC" app tests
   ```
3. `recheck2.py`(SPEC §6-5): 입력 = `fail-triage2.json`(`b_rows` 186 · `c_rows` 18 · `rows` 의 `gold_hits` · `tools_called`) + `runs.jsonl` batch `b202610311552-d39a4d`(case2 `tool_calls[]` 오류 아닌 것 전부 · case3 `trace.hub` 1회 → 유일 호출 676 · `meta.replay_unique` 와 같아야 함) + gold-export(옛 d3a1abd5 사본을 먼저 `build-out/recheck2/gold-export.d3a1abd52f70afe9.json` 로 보관 · 새 v3.2 빌드) · 대상 `--inprocess` 또는 `--base-url`(읽기만). 판정 = recheck.py 와 같은 식(norm · 양방향 포함 · 8자 · fact id · **엣지 id 도**) · 행마다 새 export 로 `gold_match` 재실행 → 응답 **전체 JSON** 안의 id 집합(`facts[].id` ∪ `more_ids` ∪ 모든 칸의 fact · edge id 문자열) 또는 인용 · 분모 = 186 · 조항 닿는 행 161 = SPEC §8 표의 조항 열(스크립트 안 fixture — `b186-clauses.json` 을 §8 에서 뽑아 `build-out/recheck2/` 에) · 묶음 · 조항 · 의도 · 도구 · 케이스별 표 · 비율 161 · 186 · 273 · 크기 = 도구별 기본 응답 중앙 · p95 · 최대(「sections 없음」 · 「있음」 따로 · case3 경로 159 따로) · 기록 입력 오류 호출은 사유 열거(W5-D14)
4. `reach.py`(SPEC §6-6): 새 export 그래프 BFS · 시작 노드 = case3 `hub.resolve.candidates ∪ menu_candidates` · X0 문항은 T1 resolve 를 in-process 로 · d(f) 정의 그대로 · 분포 · 도달 불가 사유
5. **기준선**: 지금 코드(c95b37a · 옛 export)로 recheck2 · reach 한 번 → `recheck2-report.baseline.{md,json}` · `reach-report.baseline.{md,json}`(v3.2 전 값 — 보고 비교용)

시험(`test_recheck2.py`): 두 번 바이트 같음(시간 칸 분리) · 676 = `meta.replay_unique` · 판정 동일성 = recheck2 규칙으로 `fail-triage2.json rows` 320 을 옛 export 로 재분류 → cls · sub 320/320 같음 · 크기 셈이 `fail-triage2.json case3_sizes`(중앙 46,539 · p95 170,989)와 같음

완료 조건: 기준선 리포트 2 · 320/320 · 표면 grep 원문

### WP-1 — 다이어트(§5-0-1 A1-1 ~ A1-9)

1. `config.py` 손잡이 전부(표) · `INTENT_CAPS` 는 표 이하로만
2. `Shape`: section 4 · 응답 24 · 명시 12 · 묶음 밖 명시 section = id ≤ 4 · 원문 0(A1-4 · V-9) · `limit_facts` 는 모든 section `more_ids` 전부
3. `node_sections`: 계열 · 제품 `by_unit` id 만 · 단위 ≤ 4 · `units_more` · 단위 → 쓰는 제품 fact id(aftercare · side_effects) · `sections_index{17}`(단일 노드 도구만 · recommend `n`)
4. `envelope`: `index{combos, checks, relations, families}` 한 번 · 카드 동봉은 id 참조 · `claude_contract.priority` · `use_first`(정렬 규칙 A1-8 · 결정론)
5. `neighbors`: 이웃 시술 동봉 · 원문 없음(요청 노드만)
6. 도구별 기본 응답 바이트를 rerun-v3 표본(도구별 ≤ 20 호출 · 결정론으로 고른 것)으로 in-process 측정 → 표 대조(넘는 도구는 WP-2 · 3 뒤 다시)

시험(`test_gold_v32_diet.py`): 손잡이 = 표 · by_unit 원문 0 · 단위 4 · `units_more` · `sections_index` 17 · 묶음 밖 명시 section 원문 0 + id ≤ 4 · `more_ids` 전부 · `index` 한 번 · `priority` 순서 결정론(두 번 같음 · 동순위 id 순) · 표본 바이트 ≤ 표(중앙 기준은 WP-7)

검증: `DATABASE_URL=sqlite+aiosqlite:///:memory: uv run pytest tests/test_gold_v32_diet.py tests/test_gold_tools.py -q`

완료 조건: 시험 통과 · 표본 바이트 표

### WP-2 — 동봉 규칙(C1′ ~ C14′ · B 이웃 노드 51 · 메모 10 · 쌍 8 · 엣지 6)

1. C1′ 같은 계열 · 부위 체인 · 잎 id 전부(Q003 입력에서 SC-jawline-M1 이 실리프팅 카드에 **없고** 보톡스 턱 단위 카드엔 있음)
2. C2′ 전 등급 · 계열 상속 · 전역 주장 id 전부 · `edges[]` · `question_conditions` 원문 ≤ 4 · 없으면 금기 ≤ 2
3. C3′ `relations_all`(저장 엣지 수준 · 종류 무관 · ≤ 20 · claims · reasons id · `global` sequence 메모 ≤ 4) — T3 · T5 카드에도
4. C4′ basis · C6′ 잎 id 전부 · C7′ ≤ 8 · refs 전부 · 원문 1(T7 2) · C9′ 원문 2 · id 전부 · C10′ 멤버 판정 · ≤ 6/멤버 · C12′ 펼친 단위 pih 잎 · C14′ 계열 · 제품 = 펼친 단위 전부 ≤ 10
5. recommend `why[].role` · compare `why_roles` · F-D′ 잎 fact(빌드 — `combos[].consult_copy.patientExplanation` 7 · 가드 `counts.v3_facts.fd2_patient_explanation == 7` · 검수 W-5)

시험(`test_gold_v32_b186.py` 일부 · 조항별 표본): C1′ Q003 · C2′ Q002 c2(K8-0192 id) · Q021 c2(엣지 id) · C3′ Q004 c2(E8-0169 · R8-0145#reason) · Q042 c3(E8-0005) · Q134 c2(E8-0081) · Q215(sequence_rank) · C6′ Q088 c2(CX-M11-01#prevention) · C7′ Q006 c3 · Q015 c2(members 잎 id) · Q025 c2(price) · C9′ Q017 c2(R8-0154#reason) · C14′ Q147 c3(step8_notes[190]) · Q054 c2(attrs[11]) · F-D′ Q018 c3(patientExplanation) — 입력은 SPEC §8 「실제 호출」 열 그대로 · 기대 = id 가 응답 JSON 안에

검증: `uv run pytest tests/test_gold_v32_b186.py tests/test_gold_v3_companion.py tests/test_gold_v3_pairs.py tests/test_gold_v3_facts.py -q`

완료 조건: 표본 전부 통과 · F-D′ 셈 `counts.v3_facts.fd2_patient_explanation` = 7 원문

### WP-3 — 섹션 매핑(F-F 24 · §5-14′ 29)

1. F-F 표 21줄(24행)을 **행마다 같은 입력**으로 돌려 fact id 가 응답 안에 있게 — 못 닿는 원인(예산 · by_unit 상한 · 멤버 판정 · 제품 수준)을 행마다 적고 고친다(매핑 규칙은 SPEC 그대로 · 구현만)
2. §5-14′ `sections_index` 로 29행(SPEC §8 §5-14′ 열)이 id 로 닿는지
3. `check_conditions` 펼침 8 · `checks[].edges` · `not_condition` id 목록

시험(`test_gold_v32_b186.py` 나머지): F-F 24/24 · §5-14′ 29/29 · 단 Q136 · Q140 c3(U5-028 가 M8 by_unit 4 밖이면 `units_more` 에 단위 id) 는 SPEC 대로 「단위 4 안이면 id」 — 밖이면 사유 기록(§6-6 걸음으로)

검증: `uv run pytest tests/test_gold_v32_b186.py tests/test_gold_v3_sections.py tests/test_gold_v3_checks.py -q`

완료 조건: 24/24 · 29/29(또는 사유 행)

### WP-4 — peek · expand(§5-16 · T10 · T11)

1. 빌드 · 메모리: `sections_bytes` · 이웃 종류 고정 순서 · 종류별 앞 8(금기류 · 등급 · id 순)
2. `peek(id, intent?)` · `expand(id, sections, neighbors, neighbor_kinds, fact_ids, include_conditional, intent?)` — 꼴 · 상한 · 4xx(peek 밖 이웃 · 임의 fact id · 모르는 intent) · **`intent?` 받되 무시**(`intent_used: null` · 동봉 0 · 검수 F-1) · 이웃 꼴 `neighbors_by_kind` 하나 · G13 요약 유지 · 손잡이 설정 이름 전부(`GOLD_PEEK_ITEMS_PER_KIND` · `GOLD_PEEK_NAME_CHARS` · `GOLD_PEEK_KIND_ORDER` · `GOLD_EXPAND_PICK_MAX` · `GOLD_EXPAND_FACT_IDS_MAX` · `GOLD_EXPAND_SECTION_MAX` · `GOLD_EXPAND_NEIGHBORS_MAX`)
3. REST 2 · MCP 2(meta 포함) · service · e2e 1회씩 · 공개 계약 시험에 추가
4. **실물 보고 결정(V-8)**: 1,071 노드 peek 바이트 분포를 재고 새 도구 2 로 둘지 모드로 할지 report 에 근거 한 줄(응답 꼴은 같으므로 어느 쪽이든 끝 조건 동일) — 바꿀 거면 `ask`

시험(`test_gold_v32_walk.py`): 13 종류 노드 표본 peek 200 · ≤ 4,000 B · 이웃 순서 · 앞 8 · `sections[].bytes` = 원문 합 · expand section 12 · 이웃 20 · 4xx 3종 · `intent=I-03` 을 넘겨도 응답이 안 넘긴 것과 `request` 칸 빼고 같음 · `intent_used` null · REST ↔ MCP 같음 · 두 번 같음 · 전 노드 1,071 peek 바이트 중앙 ≤ 2,000 · SPEC §5-16 대응표 칸(`neighbors_by_kind[*].items[].{id,kind,label}` · `sections[].{name,n_facts,bytes}` · `facts[].{id,text,section}`)이 전부 있음

검증: `uv run pytest tests/test_gold_v32_walk.py tests/test_gold_api.py tests/test_gold_mcp.py tests/test_public_api_contract.py -q`

완료 조건: 시험 통과 · peek 분포(중앙 · p95 · 최대) · V-8 근거 · **SPEC §5-16 대응표가 실물 응답과 1:1 임을 report 에(WORK-006 WP-3 가 읽는 계약)** · heartbeat 「peek/expand 꼴 확정」

### WP-5 — MCP 전달 계약(§5-0-2 M-1 ~ M-3)

1. 골드 9 + peek · expand + raw 3 = 14 도구 `meta={"anthropic/maxResultSizeChars": 설정값}` · env 예시
2. `INTENT_DESC` 문구(M-2 · 의도 표 12 · 「반드시 넘긴다 · 없으면 기본 의도」) 상수 하나 → REST · MCP · 서버 instructions · required 아님

시험(`test_gold_v32_mcp_meta.py`): `list_tools` 14 전부 `_meta` 값 = 설정 · intent 설명 문구 9 도구 · REST 스키마 · instructions 같은 문자열 · `intent` 없는 호출 200 · peek · expand 는 `intent?` 를 받고 `intent_used` null

검증: `uv run pytest tests/test_gold_v32_mcp_meta.py tests/test_gold_mcp.py -q`

완료 조건: 시험 통과 · 로컬 커밋 → **WORK-006 WP-0 이 쓸 빌드 — WP-6 1 발행 뒤 코디에게 18005 재시작 요청**(heartbeat 「meta 빌드 준비」)

### WP-6 — 빌드 발행 · 재실행 측정 · 걸음 · 품질 · CLI 실물 확인

1. 로컬 커밋(WP 단위) → 새 빌드(`gold_build.py` · F-D′ · `sections_bytes` 로 해시 바뀜) → 발행 → `gold_export.py` → heartbeat 「발행 완료 · 18005 재시작 요청」 · 재시작 전엔 `--inprocess`
2. `recheck2.py --inprocess`(코디 재시작 뒤 `--base-url http://127.0.0.1:18005` 로 한 번 더 — 같아야 함): (i) 161 기준 ≥ 90% · 186 · 273 보고 · 조항별 · 묶음별 · 의도별 · 닫지 않는 행 25 따로 (ii) 크기 표 전부 · case3 경로 호출 중앙 ≤ 20,000 · p95 ≤ 60,000 (iii) C3 = fact 없는 행 5(Q014 c2 · Q054 c3 · Q190 c3 · Q221 c3 + Q069 c2) 의 정규화 인용이 재실행 응답의 **원문 칸**(`facts[].text` ∪ 동봉 원문 칸)에 있음 5/5 + Q003 2 반대 조건 · 두 번 바이트 같음
3. `reach.py`: (vi) 161 중 d ≤ 4 ≥ 90% · 분포 · 도달 불가 사유 · 두 번 같음
4. 품질: `gold_quality_eval.py --gold inprocess` → 6/6 · 106/106 · Q106 · Q108~110 · 회귀 0 · 두 번 같음
5. **CLI 실물 확인(코디 승인 뒤 1회 · SPEC §5-0-2)**: Claude CLI 가 허브 MCP 를 붙여 `check_conditions family:M8 sections=all`(> 50,000 자) 1회 → 모델이 받은 결과에 「Output too large」 없음. SPEC-006 v2 WP-0 확인 시험 기록이 먼저 있으면 그것으로 대신(report 에 출처)
6. 크기 · 재인용이 서로 당기면: 손잡이를 줄이는 쪽(V-3 추천) — 조항 · 표 숫자는 안 바꾼다 · 못 맞추면 `ask`

완료 조건: 리포트 4(recheck2 · reach · quality · sizes) · 빌드 해시 · 입력 해시 12 · `counts.v3_facts` · 18005 재시작은 코디(워커가 하지 않았음을 적음)

### WP-7 — 전체 검증 · 보고

1. `uv run pytest -q`(통합 제외) · ruff · 기존 앱 시험 회귀 0
2. **표면 grep 다시**(WP-0 명령 그대로) — 결과 파일이 전부 Scope 표에 있고 `meta` 빠진 도구 0 · `intent` 설명 옛 문구 0 · 옛 상한 숫자(`=12` · `=36` · `=20` · `30`) 잔존 0
3. `work007-report.md`: WP 출력 원문 · 끝 조건 표(§Done Criteria 와 1:1) · SPEC 과 다르게 한 곳(있으면 `ask` 근거) · V-8 근거 · 남은 것

## Done Criteria

- [ ] WP-0~6 완료 조건 전부(출력 원문을 report 에) · 표면 grep 누락 0
- [ ] `recheck2-report` — (i) 조항 닿는 행 161 기준 ≥ 90%(145+) · 186 · 273 기준 보고 · 옛/새 export 해시 · 조항별(C1′ 3 · C2′ 32 · C3′ 14 · C4′ 1 · C6′ 4 · C7′ 40 · C9′ 8 · C14′ 11 · §5-14′ 29 · F-F 18 · F-D′ 1) · 묶음 · 의도 · 케이스별 · 닫지 않는 행 25 = SPEC §8 와 같음 · 그 밖 닫히지 않은 행 전부 사유
- [ ] (ii) 도구별 기본 응답 중앙 · p95 ≤ SPEC §5-0-1 표 전부 · case3 경로 호출 중앙 ≤ 20,000 · p95 ≤ 60,000 · 「sections 있음」 · 최대 보고
- [ ] (iii) C3 5/5(Q014 c2 · Q054 c3 · Q069 c2 · Q190 c3 · Q221 c3 — 정규화 인용이 `facts[].text` ∪ 동봉 원문 칸 안 · 본문 아무 데나는 아님) · Q003 c2 · c3 는 SC-jawline-M1 이 실리프팅 카드에 없음 + 보톡스 턱 단위 카드에 있음 · Q203 c2 는 vocab 만이라 밖
- [ ] (iv) `quality-report-gold` 6/6 · 106/106 · Q106 · Q108 · Q109 · Q110 · 회귀 0 · 두 번 같음 · recheck2 · reach 두 번 바이트 같음
- [ ] (v) peek 1,071 노드 중앙 ≤ 2,000 · p95 ≤ 4,000 · expand(section 1) 중앙 ≤ 8,000 · p95 ≤ 16,000
- [ ] (vi) `reach-report` 161 중 d ≤ 4 ≥ 90% · 분포 · 186 기준 보고
- [ ] (vii) `list_tools` 14 도구 `_meta["anthropic/maxResultSizeChars"]` = 설정값 · intent 문구 상수 하나 · required 아님 · CLI 실물 확인 1회 잘림 없음(또는 SPEC-006 WP-0 기록 출처)
- [ ] REST ↔ MCP 같은 JSON(11 도구) · 모든 응답에 `claude_contract{allowed_fact_ids, priority, use_first, must_show_flags, rule}` · `intent_used` · `sections_used` · 단일 노드 도구에 `sections_index` · `index`
- [ ] 새 빌드 해시 · 입력 해시 12 · `counts.v3_facts`(F-D′ `fd2_patient_explanation` 7 포함) · 발행 빌드 id 를 report 머리에 · 18005 재시작은 코디
- [ ] ruff · 전체 시험 통과 · `git status --short` 원문 · push 0
- [ ] SPEC v3.2 와 다르게 구현한 곳 0 — 있으면 목록 + `ask` 합의 근거
- [ ] `$W` · `$E` 기존 파일 변경 0(새 파일은 `recheck2.py` · `reach.py` · `test_recheck2.py` · `build-out/recheck2/` 만)

## Rollback

push · 배포 없음. WP-0 기준점(c95b37a)으로 코드를 되돌린다. 발행은 `gold_publication` 포인터를 d3a1abd5 로 되돌리고 재시작(코디). 지난 빌드 행은 지우지 않는다. 새 alembic 리비전은 없다(F-D′ 는 fact 행 추가 · 스키마 같음).

## Open Issues

- SPEC-005 §7 V-3(상한 표 숫자 vs 손잡이) · V-8(새 도구 2 vs 모드 — WP-4 실물 뒤) · V-9(묶음 밖 명시 section 원문 0) · V-10(걸음 4 · 20KB 는 SPEC-006 v2 값) · V-11 · V-12(intent required) — 본문 추천값으로 진행 · 측정 뒤 사용자 확인
- 닫지 않는 행 25(X0 16 · N 9) · A 54 · C1 10 · 미분류 15 는 이 작업 밖(리포트에는 셈)
- case3 걸음 실행 · 182문항 재실행 · 첫 글자 영향은 SPEC-006 v2 · WORK-006 · 코디

## Related

- **WORK-006 WP-0 · WP-3 는 이 작업의 WP-5 · WP-4 뒤**(§순서 의존) · SPEC-005 0.3.3 · SPEC-005.v3.1.md(보관) · review-spec005-v32-report.md · WORK-005 · work005-report.md · fail-triage2.md · rerun-report.md · phub-recommend-jev-walk-addendum.md · SPEC-006 v2(§3-4 · §3-5 · §3-6 · W-2) · `_RESUME.md` §2
