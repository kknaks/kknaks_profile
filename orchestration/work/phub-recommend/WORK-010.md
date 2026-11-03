---
type: work
id: WORK-010
title: "실버 9단계(설명 사실)를 골드에 — step9 입력 · G19~G22 · section safety.management · 값 사전 globals(SPEC-005 v3.4)"
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
  qa: "reviewer_code 워커 · 코디(18005 재시작 · 재실행)"
  ops: ""
progress: 0
created_at: 2026-11-01
updated_at: 2026-11-01
depends_on:
  - "WORK-008(v3.3 · 완료 · 코드 2ca8094 · 빌드 b031371c)"
  - "실버 9단계(step9-explanations.json step9-v1 · 5d394f87dca53602) · semantic.json 11-01 판(inputs 12 · 6c43231e82939a44)"
  - "**짝 의존 — SPEC-006 0.3.6(I-04 고정 섹션에 safety.management 추가 · 앱 clinic_chat config.py:80 같이 · 코디)** — v3.4 발행(18005 재시작)과 같은 묶음으로만 나간다(검수 F-1 · 아래 §순서 의존)"
tags:
  - product/procedure-hub
  - feature/phub-recommend
  - doc/work
  - status/todo
links:
  spec: "orchestration/work/phub-recommend/SPEC-005.md (0.3.5 · §2-1 · §2-2 v3.4 · §3-1 G19~G22 · §3-5 · §4-3 v3.4 · §5-0-1 v3.4 영향 · §5-14 I-04 · §5-16 v3.4 · §6-4 v3.4 행 · §6-8 · §7 V-19~V-21 · §8 N-9단계)"
  decisions:
    - "orchestration/work/phub-recommend/step9-decisions.json (D9-1~D9-9 · 사용자 11-01 「추천으로 데이터 결정하자」)"
    - "orchestration/work/phub-recommend/phub-recommend-spec005-v34-brief.md"
  evals:
    - "orchestration/work/phub-recommend/step9-effect.json · .md (A 행 닫힘 셈 — 같은 식을 새 export 로)"
    - "reference/2026-10-30-hub-evals/fail-triage-scripts/walk3.py · recheck2.py"
---

# 실버 9단계 → 골드(허브 · SPEC-005 v3.4)

SPEC-005 **0.3.5(v3.4)** 의 바뀐 조항만 구현한다. 계약은 SPEC 이 갖고, 이 문서는 순서 · 파일 · 시험 · 끝 조건 · 검증 명령만 갖는다. 둘이 다르면 SPEC 을 따른다. 검수 PASS 뒤 구현 발주는 코디가 한다.

**하는 것**: 입력에 `step9-explanations.json`(해시 가드 12) · G19 9단계 fact(G9-1 id · 원문 그대로 · 정본 노드만) · G20 8단계 합병증 · 부작용 칸 section(CX management · prevention 54 → `safety.management` · SE 잎 205 새 fact) · G21 값 사전 8 → globals + 전역 fact · G22 ② resolved 하나(alternatives 는 id 메타) · section 18(`safety.management`) · I-04 기본 묶음 · peek/expand 18 section · `global_facts`.

**비목표**: 실버 · 시맨틱 · 9단계 원장 수정(9단계 값이 틀려 보이면 보고 — V-19) · 9단계 충돌 처분 다시 하기(골드는 접지 · 고르지 않는다) · 다이어트 손잡이 · 크기 표 숫자 변경(넘으면 보고 — V-20) · 앱 코드(clinic_chat — SPEC-006 0.3.6 · config 는 코디가 짝으로 발주 · 이 작업은 §6-8 (k) 로 영향만 잰다) · Jev · 채점 · 182 재실행(코디) · push · 배포. 18005 는 띄우지도 끄지도 않는다.

## 순서 의존 — SPEC-006 0.3.6(짝 · 검수 F-1)

| 이 작업 | 먼저/뒤 | 짝 | 왜 |
|---|---|---|---|
| WP-2 · WP-3(G20 CX 54 이동 · SE 75 · I-04 묶음) | 먼저 | SPEC-006 0.3.6 §3-4-1-1 I-04 고정 섹션 + `safety.management` · 앱 `config.py:80` | 006 이 그대로면 case3 I-04 첫 걸음이 관리 · 예방 54 를 잃고 75 를 못 받는다(SPEC-005 §5-16 v3.4 영향) |
| WP-4 §6-8 (k) ① ② ③ 셈 | 발행 전 | 006 0.3.6 꼴(S + safety.management) | ② 감소 · ③ ≥ ① 을 숫자로 — 코디가 짝 발행 판단 |
| WP-4 발행 · **18005 재시작 요청** | 006 0.3.6 앱 config 와 **같은 묶음** | 코디 | 한쪽만 나가면 case3 I-04 회귀 |

→ 발주 순서(코디): WORK-010 WP-0~3 → heartbeat 「v3.4 section · step9 fact 확정」 → 006 0.3.6 개정 · 앱 config(코디) → WORK-010 WP-4 (k) 셈 → 발행 + 앱 config 같이 → 재시작 → WP-5.

## Meta

- 코드: `/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-recommend`(브랜치 `kknaksss/phub-recommend` · 로컬 · **push 금지**) · 명령은 `backend/` 에서 · 기준점 = `2ca8094`(WORK-008) — Phase 0 에서 `git log -1` · `git status --short` 깨끗 확인
- 입력 `$W` = `orchestration/work/phub-recommend`(읽기만 — `GOLD_INPUT_DIR` · 입력 13 = semantic + 12) · 평가 `$E` = `reference/2026-10-30-hub-evals`(읽기만 · 새 파일은 `build-out/step9-gold/` · `fail-triage-scripts/step9_gold.py` · `test_step9_gold.py` 만)
- 로컬 DB `phub-graph-postgres`(55434) · 사용자 포트 · 프로세스 금지 · 외부 호출 없음
- 원장 인용 본문을 시험 · 문서에 옮기지 않는다 — fact id · 경로 · 바이트 · 셈만. 기대값은 실물 빌드에서 뽑는다
- WP 마다 그 WP 시험만 · 전체 시험 · 품질 · 재실행 · walk3 는 WP-5 에서 한 번
- 새 alembic 리비전 없음(fact · global 행 추가 · 스키마 같음 — `gold_fact.section` String(32)(`safety.management` 17자) · id String(400)(9단계 fact id 최대 133자) · 메타는 기존 fact 와 같이 `gold_fact.source` jsonb 의 `meta` 에)

## Scope · Code Surface

표면 전수(WP-0 에서 아래 grep 을 다시 돌려 빠진 파일은 표에 더한다). 작성 때(2ca8094) 결과:

```bash
grep -rl 'INPUT_FILES\|hash_guard\|read_dir' app scripts tests
grep -rl 'FACT_SECTIONS\|facts import SECTIONS\|SECTIONS =' app scripts tests
grep -rl 'safety\.complications\|safety\.side_effects' app scripts tests
grep -rl 'INTENT_SECTIONS\|"I-04"' app scripts tests
grep -rl 'globals\|gold_global' app scripts tests
grep -rl 'v3_facts\|counts\[' app scripts tests
grep -rl 'sections_index\|warm_sections' app scripts tests
grep -rl 'overview.*method.*recovery' app scripts tests     # section 이름을 문장으로 나열한 설명 · 시험
```

| 파일 | 새/고침 | SPEC v3.4 |
|---|---|---|
| `app/modules/gold/inputs.py` | 고침 — `INPUT_FILES` 에 `step9-explanations.json`(13) · 해시 가드 = semantic inputs 12 | §2-1 |
| `app/modules/gold/build.py` | 고침 — G19(node_slots → fact · ids.map · 정본 없음 셈) · G20(CX section 이동 · SE 잎 fact) · G21(globals kind value_dictionary · 전역 fact) · G22(alternatives 메타) · 가드 `counts.v34_facts` · step9 `summary.open ≠ 0` 이면 실패 | §3-1 · §3-5 · §4-3 |
| `app/modules/gold/facts.py` | 고침 — `SECTIONS` 에 `safety.management`(18) · section 매핑(관리 · 예방) | §4-3 |
| `app/modules/gold/memory.py` · `repository.py` · `application.py` | 고침 — 새 global kind · fact 메타(`source.meta` 안 qualifiers · class · multi_source · same_as · alternatives · resolved_by) 적재 · 읽기 · `app/model/gold.py` 는 확인만(칸 그대로) | §3-1 · §4-3 |
| `app/modules/gold/tools.py` | 고침 — `INTENT_SECTIONS["I-04"]` 에 `safety.management` · `node_section_facts` 매핑 · `sections_index` 18 · peek `global` 에 값 사전 · expand `global_facts`(timeline · safety.complications) · C6′ 셈(section 무관 · 그대로인지 확인) · `warm_sections` 다시 잼 | §5-14 · §5-16 |
| `app/modules/gold/mcp_server.py` · `service.py` · `app/router/gold.py` · `app/schema/gold.py` · `app/swagger_docs/gold.py` | 고침 — section 이름을 나열한 설명 · 검증(모르는 section 4xx 집합)에 `safety.management` | §5-16 |
| `app/modules/gold/config.py` | 확인 — 새 손잡이 없음(`GOLD_COMPANION_GLOBAL_MAX` 재사용) | §5-16 |
| `scripts/gold_ingest.py` · `gold_build.py` · `gold_export.py` | 확인 · 고침 — 입력 13 · export 에 새 메타 · global kind | §2-1 |
| `scripts/gold_quality_eval.py` · `scripts/gold_e2e.py` | 고침 — 채점 식 그대로 · e2e 에 `safety.management` expand 1회 · `#step9[` fact 1건 · 값 사전 global 1건 | §6-2 |
| `docs/gold-local.md` | 고침 — 9단계 입력 · section 18 한 단락 | — |
| `tests/gold_support.py` · `test_gold_ingest.py` · `test_gold_build.py` · `test_gold_guards.py` · `test_gold_v3_facts.py` | 고침 — 입력 13 · 가드 · 셈 | §6-4 |
| `tests/test_gold_tools.py` · `test_gold_v3_intent.py` · `test_gold_v3_sections.py` · `test_gold_v3_companion.py` · `test_gold_v32_diet.py`(17 → 18 · INTENT 표) · `test_gold_v32_walk.py` · `test_gold_v33_expand.py`(section 집합 · peek bytes 차 0 다시) · `test_gold_v32_b186.py` · `test_gold_mcp.py` · `test_public_api_contract.py` | 고침 — section 18 · I-04 · 기대값(실물에서) | §6-4 |
| **`tests/test_gold_v34_step9.py`(새)** | 새 — §6-4 v3.4 행 전부 | §6-4 |
| `$E/fail-triage-scripts/step9_gold.py` · `test_step9_gold.py` · `$E/build-out/step9-gold/{step9-gold-report.{md,json}}`(새) | 새 — §6-8 (b) (c) (d) (e) 셈(`step9-effect.py` 의 판정 식을 다시 적음 · import 안 함 · 9단계 레코드 대신 새 export fact 원문) | §6-8 |
| `backend/build-out/work010-report.md`(새) | 새 — WP 출력 원문 · §6-8 표 1:1 | — |
| 영향 없음(작성 때 grep) | `app/modules/graph/*`(`validation.py` 포함) · `app/modules/retrieval/*` · `scripts/graph_*` · `tests/test_graph_*` · `tests/graph_support.py` · `tests/integration/*`(v1 그래프 · `counts[` · `read_dir` 가 다른 뜻 — 검수 W-5) | — |

손대지 않는 것: `$W` 전부 · `$E` 기존 파일(`walk3.py` · `recheck2.py` 는 실행만) · clinic_chat · 사용자 env.

## Execution

### WP-0 — 기준점 · 표면 · 셈 스크립트(끝 조건 도구 먼저)

1. `git log -1`(2ca8094) · `git status --short` 깨끗
2. 표면 grep 원문 → report · 표 밖 파일은 표에 더함 · `gold_fact.source.meta` 에 메타를 싣는 기존 길 확인
3. `step9_gold.py`: 입력 = 새 export · 옛 export(b031371c) · `step9-explanations.json` · `step9-effect.json`(행 목록) · `fail-triage2.json` · runs(v5a) — (b) id 집합 · 원문 바이트 (c) section 별 차 (d) ② 칸 (e) A 행 닫힘(2차 54 · v5a 30 · 판정 = 인용 ⊂ fact 원문 · 사유 분류는 step9-effect 와 같은 이름)
4. 기준선: 옛 export 로 한 번 → `step9-gold-report.baseline.*`(9단계 fact 0 · 2차 A 닫힘 0)

시험(`test_step9_gold.py`): 두 번 바이트 같음 · 기준선 셈 · 판정 식 고정 입력

### WP-1 — 입력 · section(§2-1 · §4-3)

1. `INPUT_FILES` 13 · 해시 가드 12 · step9 `summary.open` · `human_check` ≠ 0 → 빌드 실패
2. `SECTIONS` 18 · 검증 집합 · 설명 문구

시험: 입력 13 · 낡힌 step9 사본(sha 다름) → 가드 실패 · open ≠ 0 사본 → 실패 · section 18

검증: `DATABASE_URL=sqlite+aiosqlite:///:memory: uv run pytest tests/test_gold_ingest.py tests/test_gold_guards.py -q`

### WP-2 — 빌드 규칙 G19~G22(§3-1)

1. G19 node_slots → fact(ids.map · 정본 노드 없음 = 셈 · id = G9-1 · 원문 = 레코드 text · 메타)
2. G20 CX `#management` · `#prevention` section 이동(id 그대로) · SE 잎 새 fact(**section_map 행마다 하나** — step8 칸을 직접 훑으면 206 · SE-M16-06 「-」 · owner 계열 · 단위 시술 펼침은 G9 길)
3. G21 globals kind `value_dictionary` 8 · 전역 fact 8
4. G22 ② alternatives 메타(id · 원천 경로) · 원문 fact 0 · 가드는 9단계 숫자 정의(`step9-decisions conflict_resolution` numset)로 — `\d` 금지(resolved 원문 숫자 없는 ② 5칸)
5. 가드 `counts.v34_facts`(입력에서 센 값과 대조)

시험(`test_gold_v34_step9.py` 빌드 부분): fact 수 = 정본 노드 쪽 emit 합 · 안 실음 = 나머지 · 합 = facts_out · id 유일 · 원문 바이트 = 레코드 · CX 이동 54 · SE 205 · globals 8 · ② resolved ∈ emit · alternatives ∉ emit · 나머지 emit numset 빈 것 · alternatives 원문 0 · 두 번 빌드 해시 같음

검증: `uv run pytest tests/test_gold_v34_step9.py tests/test_gold_build.py tests/test_gold_v3_facts.py -q`

### WP-3 — 도구(§5-14 · §5-16)

1. `INTENT_SECTIONS["I-04"]` · `sections_index` 18 · `node_section_facts` 매핑
2. peek `global` 값 사전 · expand `global_facts`(timeline · safety.complications · ≤ 4) · `warm_sections` 다시 · peek bytes 차 0
3. REST · MCP · schema · swagger 설명 · 모르는 section 4xx 집합

시험(`test_gold_v34_step9.py` 도구 부분 + 기존 고침): I-04 카드에 safety.management 원문 · expand(sections=[safety.management]) 200 · peek sections 에 있음 · `global_facts` · REST ↔ MCP 같음 · 전 노드 × section peek bytes 차 0

검증: `uv run pytest tests/test_gold_v34_step9.py tests/test_gold_v3_intent.py tests/test_gold_v3_sections.py tests/test_gold_v32_diet.py tests/test_gold_v33_expand.py tests/test_gold_mcp.py tests/test_public_api_contract.py -q`

완료 조건: 시험 통과 · heartbeat 「v3.4 section · step9 fact 확정」(코디 — SPEC-006 §3-4-1-1 I-04 고정 섹션 판단 자리)

### WP-4 — 발행 · 측정

1. 로컬 커밋(WP 단위) → `gold_build.py`(새 빌드 해시 · 가드 전부) → 발행 → `gold_export.py` → heartbeat 「발행 완료 · 18005 재시작 요청」
2. `step9_gold.py` 두 번(바이트 같음) — §6-8 (b) (c) (d) (e)
3. `recheck2.py rerun --inprocess` → 크기(§6-8 (f)) · (i) 145/155 · T1~T9 응답 변화 목록(9단계 fact 로 바뀌는 것이 정상 — 도구 · 바이트 차 보고)
4. `walk3.py --inprocess` 두 번 — §6-8 (h) · report 에 「walk3 SECTIONS 상수 17 그대로 · 영향 없음」 한 줄(검수 W-4)
4-1. **§6-8 (k)** case3 I-04 경로 세 판(① b031371c · ② v3.4 · 지금 S · ③ v3.4 · S + safety.management) — `step9_gold.py` 에 함수 하나 · 판 · 노드별 표 · ③ ≥ ① 이 아니면 발행 요청 전에 `ask`
5. 품질 `gold_quality_eval.py --gold inprocess` 두 번 — §6-8 (g)
6. 코디 재시작 뒤 `--base-url` 읽기 1회(in-process 와 같아야 함) · `gold_e2e.py`

### WP-5 — 전체 검증 · 보고

1. `uv run pytest -q --ignore=tests/integration` · `ruff check .`
2. 표면 grep 다시 — section 17 을 가정한 코드 · 시험 잔존 0 · 입력 12 를 가정한 코드 0
3. `work010-report.md`: WP 출력 원문 · §6-8 표 1:1 · 설계 셈 대비 차 · SPEC 과 다르게 한 곳(있으면 `ask` 근거) · 남은 것(V-19~V-21)

## Done Criteria

- [ ] §6-8 (a)~(k) 전부(설계 셈 · 실물 · 판정 표)
- [ ] (b) 새 export 9단계 fact = 정본 노드 쪽 emit(설계 5,273) · 안 실음 = 비활성 제품 노드만(설계 39) · 원문 바이트 같음
- [ ] (c) section 별 차 = 설계 셈(overview +3,735 · recovery +902 · method +634 · disclosure +2 · safety.management +129 · safety.side_effects +130 · safety.complications −54 +4 · timeline +4)
- [ ] (e) 2차 A 54 중 골드 fact 로 닫힘 ≥ 51 · v5a A 30 중 ≥ 25 · 나머지 사유
- [ ] (f) 크기 표 안 또는 넘는 도구 보고 · expand section 1 중앙 ≤ 2,000 · p95 ≤ 5,000 · peek bytes 차 0
- [ ] (g) 품질 6/6 · 106/106 · 회귀 0 · (h) walk3 평균 걸음 ≥ 3.0 · 이웃 도달 ≥ 85% · 새로 닿음 ≥ 5 · (i) ≥ 145/155
- [ ] (k) case3 I-04 경로 ③ ≥ ① · ② 감소 보고 · 발행은 SPEC-006 0.3.6 앱 config 와 같은 묶음(코디)
- [ ] 새 빌드 해시 · 입력 해시 12 · `counts.v34_facts` · 발행 빌드 id 를 report 머리에 · 18005 재시작은 코디
- [ ] ruff · 전체 시험 · `git status --short` 원문 · push 0 · `$W` 변경 0 · `$E` 기존 파일 변경 0
- [ ] SPEC v3.4 와 다르게 구현한 곳 0 — 있으면 목록 + `ask` 합의 근거

## Rollback

push · 배포 없음. 기준점(2ca8094)으로 코드를 되돌리고 발행 포인터를 b031371c 로 · 재시작(코디). 새 alembic 리비전 없음.

## Open Issues

- SPEC-005 §7 V-19(비활성 제품 39 fact) · V-20(크기 표) · V-21(전역 값 사전 내는 자리) — 본문 추천값으로 진행 · 측정 뒤 사용자
- SPEC-006 0.3.6(I-04 고정 섹션 + `safety.management` · 앱 config) — **짝 의존**(코디 발주 · 같은 묶음 발행)

## Related

- SPEC-005 0.3.5 · SPEC-005.v3.3.md(보관) · WORK-008 · work008-report.md · step9-* · 로그 2026-11-01-silver-step9-explanations · 점검 스킬 procedure-hub-explanation-check
