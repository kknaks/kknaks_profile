---
type: work
id: WORK-005
title: "허브 응답 설계 수정(SPEC-005 v3) — 의도 동봉 · 섹션 기본 묶음 · 쌍 evidence · fact 재부착 · checks 펼침 · 재인용 측정"
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
  qa: "reviewer_code 워커 · 코디(재실행 · 18005 재시작)"
  ops: ""
progress: 0
created_at: 2026-10-31
updated_at: 2026-10-31
depends_on:
  - "WORK-003(골드 · 도구 9 · 완료)"
tags:
  - product/procedure-hub
  - feature/phub-recommend
  - doc/work
  - status/todo
links:
  spec: "orchestration/work/phub-recommend/SPEC-005.md (0.3.1 · §4-3 F-A~F-E · §5-0 · §5-13~§5-15 · §6-5)"
  decisions:
    - "orchestration/work/phub-recommend/_RESUME.md §2 (10-31 「고칠 순서 1 허브 응답 설계」)"
  evals:
    - "reference/2026-10-30-hub-evals/build-out/fail-triage.md · .json · fail-triage-scripts/"
---

# 허브 응답 설계 수정 — 전달 문제 B 239건 + 오류 15건

SPEC-005 **0.3.1(v3.1 · 검수 반영)** 의 바뀐 조항만 구현한다. 계약은 SPEC 이 갖고, 이 문서는 순서 · 파일 · 시험 · 끝 조건 · 검증 명령만 갖는다. 둘이 다르면 SPEC 을 따른다. 검수 PASS 뒤 구현 발주는 코디가 한다.

**비목표**: 실버 · 시맨틱 · 브론즈 수정(A 61 은 9단계) · 앱(clinic_chat · SPEC-006) 수정 · Jev 규칙 · 프롬프트 · 채점 · 원장 MCP · push · 배포. 정해진 결정(허브 LLM 없음 · 결정론 · slim · G13 · 충돌 하나)을 다시 열지 않는다.

## Meta

- 코드: `/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-recommend`(브랜치 `kknaksss/phub-recommend` · 로컬 전용 · **push 금지**) · 명령은 `backend/` 에서 · 기준점 = WORK-003 마지막 커밋(`b6b2127` 뒤 짧은 카드 · 실물 실험 수정 커밋 포함 — Phase 0 에서 `git log -1` 로 적는다)
- 입력 `$W` = `orchestration/work/phub-recommend`(실버 · 시맨틱 **읽기만**) · 평가 `$E` = `reference/2026-10-30-hub-evals`(`build-out/fail-triage.json` · `fail-triage-scripts/replay.py` · `triage.py` · `runs/runs.jsonl` — **읽기만** · 새 파일은 `build-out/recheck/` 와 `fail-triage-scripts/recheck.py` 만)
- 로컬: DB `phub-graph-postgres`(55434) · 허브 18005 는 **사용자 · 실험이 쓰는 중 — 워커는 띄우지도 끄지도 않는다**(측정은 `--gold inprocess` · D-7). **읽기 호출(GET · 조회 POST)은 허용**(WP-0 기준선 · W-5). 새 빌드 발행 뒤 18005 재시작은 코디가(WP-7 끝)
- 사용자 포트 · 프로세스(3700 · 3800 · 8700 · 8800 · 54329 · `procedure-*`) 금지 · 외부 호출 없음
- 원장 인용 본문을 시험 · 문서에 옮기지 않는다 — fact id · 경로만(공개 레포). 시험 기대값은 실물 빌드에서 뽑는다(가상 문장 없음)
- WP 마다 **그 WP 시험만** 돌린다. 전체 시험 · ruff · 품질 · 재인용 측정은 WP-7 에서 한 번

## Work Summary

| Field | Value |
|---|---|
| Goal | B 239 중 카드 도구 호출이 있던 205 행 가운데 조항이 닿는 186 행의 90% 이상(168+)을 허브 응답에 싣고(재인용률 · SPEC §6-5 · 205 · 239 기준은 보고) · checks 400 15건을 200 으로 · 응답 크기 중앙값 ≤ 현 ×2 · 품질 6/6 · 106/106 유지 |
| Non-goal | 위 비목표 · 허브를 안 부른 17건 · resolve 만 17건(V-1) · 「닫지 않는 행」 19(§6-5 표) · A · C · 미분류 |
| 완료 판정 | §Done Criteria 전부 |

## Scope · Code Surface

| 파일 | 새/고침 | SPEC v3 |
|---|---|---|
| `app/modules/gold/facts.py` | 고침 — `attached_to` 칸 · 잎 fact 헬퍼(엣지 · 노드 속성 잎 → fact id 규칙) | §4-3 F-C · F-D |
| `app/modules/gold/build.py` | 고침 — F-A step8_notes 앵커(where ①~⑤) · F-B attrs 앵커 · F-C 엣지 속성 잎 fact · F-D 노드 속성 잎 fact · `family:None` 바로잡기 · `counts.v3_facts` · 가드 | §4-3 F-A~F-E · §3-5 |
| `app/model/gold.py` · `alembic/versions/<새 리비전>_gold_fact_attached.py` | 새 리비전 — `gold_fact.attached_to jsonb` + 인덱스(GIN) · 다른 테이블 그대로 | §4-2 · §4-3 |
| `app/modules/gold/repository.py` · `memory.py` | 고침 — `attached_to` 적재 · `facts_by_attach[(node, section)]` 색인 · 1-hop 동봉 dict(시술마다 C1~C14 재료 · 빌드 때 모아 둠 S4) | §5-13 |
| `app/modules/gold/service.py` | 고침 — `GoldToolService.resolve · procedure_card · check_conditions · compare · vocab` 명시 인자에 `intent` · `GoldState.load` facts cols 7 → 8(`attached_to`) | §5-0 · §4-3(F-7) |
| `app/modules/gold/application.py`(export cols) · `scripts/gold_export.py` | 고침 — export fact cols 에 `attached_to`(없으면 `gold-export.json` 에 안 나가 recheck · gold_match 가 못 읽음) | §4-3 · §6-5(F-7) |
| `tests/test_gold_api.py`(`procedures 1개 → 400` 기대) · `tests/test_gold_pairs.py` | 고침 — PAIR_MIN 1 에 맞춰 기대값 바꿈(1개 = `relations[]`) | §5-5(F-7) |
| `scripts/gold_e2e.py` · `tests/test_public_api_contract.py` | 고침 — sections 호출에 `intent_used` · `sections_used` 검증 · section 응답 계약 시험 영향 확인 | §5-0(F-7) |
| `app/modules/gold/tools.py` | 고침 — `intent` 공통 입력 · 기본 의도 · `Shape` 에 의도 기본 묶음 ∪ 요청 · `none` · `sections_used` · `intent_used` · 공통 section 매핑 함수(시술 노드 단위 · 도구 9) · 계열 카드 `by_unit` · `companion{}`(§5-13 표 · 상한) · pair_check 1개 입력 `relations[]` · `self_pair[]` · claims 원문 기본 · compare `overview · method` rows · `source_comparisons[].members[].attrs_text` · `relations[]` · check_conditions 계열 · 제품 펼침 + `by_unit` · combos 짧은 카드 `price` · `effect` · pih 요약 `C12` · `INTENTS` 와 1:1 상수 | §5-0 · §5-3~§5-9 · §5-13~§5-15 |
| `app/router/gold.py` · `app/schema/gold.py` · `app/swagger_docs/gold.py` · `app/modules/gold/mcp_server.py` | 고침 — `intent` 입력(REST query · body · MCP tool 인자 · 설명 문구 같게) · pair_check 최소 1 · check_conditions id 종류에 family | §5-0 · §5-5 · §5-6 |
| `app/modules/gold/config.py` · `envs/gold.env.example` | 고침 — `GOLD_EXPAND_MAX_UNITS=20` · `GOLD_CARD_BY_UNIT_MAX=12` · `GOLD_SECTION_FACTS_MAX=8` · 동봉 상한(§5-13 표 값) | §5-13 · §5-14 |
| `scripts/gold_quality_eval.py` | 고침 — 문항 의도를 `intent` 로 넘김(어댑터 · 채점 식 그대로) | §6-1 |
| `tests/test_gold_build.py` · `test_gold_guards.py` · `test_gold_tools.py` · `test_gold_api.py` · `test_gold_mcp.py` · `tests/test_gold_v3_*.py`(새) | 새 · 고침 | §6-4 v3 행 |
| `$E/fail-triage-scripts/recheck.py`(새) · `$E/build-out/recheck/recheck-report.{md,json}`(새) | 새 — 재실행 · 대조 · 크기 · 리포트(결정론) | §6-5 |
| `backend/build-out/work005-report.md` | 새 — WP 출력 원문 · SPEC 과 다른 점 | — |
| `docs/gold-local.md` | 고침 — `intent` · `sections=none` · 재빌드 · 발행 · 재시작 순서 한 단락 | — |

손대지 않는 것: `$W` 전부 · `$E/build-out/fail-triage.*` · `triage.py` · `replay.py`(읽기만 · import 하지 않음 · 판정 식은 recheck.py 에 같은 식으로) · `runs/` · `app/modules/raw/` · 기존 앱 · v1 graph · 사용자 env · clinic_chat.

## Execution

### WP-0 — 기준점 · 측정 스크립트(끝 조건 도구를 먼저)

1. 기준점: `git status --short` 깨끗한지 · `git log -1` sha 를 report 머리에. 더러우면 escalation
2. `recheck.py`(SPEC §6-5): 입력 = `fail-triage.json`(rows cls B 239 · `jev_intent` · `tools_called` · 원장 경로 · 인용) + `replay.py` 의 호출 묶음(전체 755 중 실패 174문항분 · 같은 입력) + `runs/runs.jsonl`(현 크기 기준 · 셈 규칙 §6-5) + **gold-export 두 벌**(옛 e9d30ace · 새 v3 빌드 — 해시 둘 다 리포트 머리에) · 대상 서버 `--base-url`(18005 · 읽기 호출만) 또는 `--inprocess`(새 빌드 TestClient) · 호출마다 `intent` = 행 `jev_intent`(「?」면 없이) · **판정 규칙은 recheck.py 안에 같은 식으로 적는다**(`norm` = 소문자 · 공백 · 기호 제거 · 양방향 포함 · 골드 쪽 8자 이상 · fact id 일치 — `triage.py` 는 모듈 수준에서 파일을 읽고 쓰므로 import · 수정하지 않음 · F-6) · 행마다 **새 export 로 `gold_match` 를 다시 돌려 gold_hits 를 갱신**한 뒤 fact id · 인용 대조(F-3) · 분모 = 카드 도구(T2~T8) 호출이 있던 B 205 · 「닫지 않는 행」 19 는 §6-5 표 그대로 따로 셈 · 출력 = `recheck-report.json`(행마다 닫힘 여부 · 어느 호출 · 어느 fact id · 옛/새 gold_hits) · `.md`(묶음 ①~⑧ · 의도별 · 도구별 크기 중앙 · 오류 · 비율 = 조항이 닿는 186 기준 / 205 기준 / 239 기준) · 시간 칸은 `.json` 머리 하나에만
3. `replay.json` 은 WP-7 발행 · 재시작 전에 18005(e9d30ace) 읽기 재호출로 먼저 만든다(`replay.py` 와 같은 호출 묶음 · `$E/build-out/recheck/replay.json`) — W-1
4. **지금 허브(18005 · 빌드 e9d30ace · 읽기 호출)로 한 번 돌려 기준선**을 만든다 — B 닫힘 0 에 가까운지(fail-triage 와 같은 결과여야 함 · 다르면 스크립트 오류) · 도구별 크기 중앙이 SPEC §6-5 표와 같은 자리인지

시험(`$E/fail-triage-scripts/test_recheck.py` · pytest · 읽기만): `recheck.py` 두 번 → `.json` 바이트 같음(시간 칸 뺀 비교) · **판정 동일성**: recheck 의 규칙으로 `fail-triage.json` 320행을 옛 export 로 재분류 → cls · sub 가 320/320 같음(F-6) · 크기 셈이 §6-5 표(662 · 201 · 도구별 중앙)와 같음

완료 조건: `recheck-report.baseline.{md,json}` · 기준선 재인용률(기대 ≈ 0%) · 320/320 재분류 동일 · 18005 는 읽기 호출만

### WP-1 — fact 재부착 · 새 fact(빌드 · F-A ~ F-E 의 빌드 쪽)

1. 리비전: `gold_fact.attached_to jsonb`(기본 `[]`) · GIN 인덱스 · 이름 명시
2. `facts.py`: `attached_to` · 잎 fact 헬퍼 `leaf_facts(owner, section, path_prefix, value)`(F-C · F-D 공통 · id `{owner}#{section}#{칸 경로}`)
3. `build.py`
   - F-A: `step8_notes[]` 245 → `where` 규칙 ①~⑤(SPEC §4-3 표) → `attached_to`(단위 시술 · combo · 고민) · meta `{where, kind, cc}` · 미해결이면 `scope:all` 유지하되 **셈 0 이어야 함**(가드)
   - F-B: 8단계 `attrs[]` 56 → `source_index` 규칙 → `attached_to`
   - F-C: `site_caution` 엣지 `spec` 잎 · `vessels[].danger` · `clinical_pearls[]` · `safe_injection_depth` → fact(owner 엣지 · attached 계열 · 부위 · `units_affected`) / 비교 조합 `members[].attrs_text` 잎 · `anchor.subtitle` → fact(attached 멤버 단위 시술 + combo) / `product_family.row.basis` → fact(제품 · overview) / treats `row.evidence.role` → fact(section evidence · attached to_units)
   - F-D: 단위 시술 `pih[]` 잎 · `sources[].detail` · 조합 `effect.*` · `price` · `evidence_notes` · `caveats` · `rationale` · `sessions` · `maintenance` · `subtitle` · `follow_up` · `avoid_text` · `annual_focus` · 계열 `definition` → fact(section 은 SPEC 표)
   - `family:None` owner 40행 → `taxonomy_products[].product` 정본 id
   - `counts.v3_facts{step8_notes_by_anchor{①..⑤}, attrs_attached, site_caution_leaves, compare_member_leaves, combo_leaves, pih_leaves, family_none}` · 가드(F-A 미해결 0 · F-B owner 없음 0 · `family:None` 0)
4. 빌드 두 번 → 해시 같음 · 발행은 WP-7 에서(코디 재시작과 묶음)

시험(`tests/test_gold_v3_facts.py`): 앵커 ①~⑤ 셈 = 13 · 152 · 44 · 28 · 8 · 미해결 0 / attrs 56 전부 노드 1+ / SC 22엣지 spec 잎 fact / 비교 조합 9 members 잎 / 조합 79 effect·price / `family:None` 0 / 두 번 빌드 해시 같음 / 일부러 `where` 를 깬 입력(시험 안 복사본) → 가드 실패

검증:
```bash
DATABASE_URL=sqlite+aiosqlite:///:memory: uv run pytest tests/test_gold_v3_facts.py tests/test_gold_build.py tests/test_gold_guards.py -q
uv run python scripts/gold_build.py --dry-run   # 셈 · 가드 · 해시(발행 안 함)
```

완료 조건: 시험 통과 원문 · `counts.v3_facts` 원문 · 새 빌드 해시(발행 전)

### WP-2 — 섹션 매핑 구멍(② 16) · 공통 매핑 함수

1. `tools.py`: `section_facts_for(node, section, product?)` 를 **도구 9 공통**으로 — 지금 `_section_facts` 를 확장: owner ∪ `facts_by_attach` · 계열 · 제품 카드의 단위 시술 수준 section 은 `by_unit{unit: [fact]}`(상한 `GOLD_CARD_BY_UNIT_MAX` · `truncated` · `units_total`) · `site_caution` = owner(계열) ∪ SC 엣지 fact(단위는 부위 일치 · 계열은 전부) ∪ `family_text` critical
2. `Shape` 의 `sections` 를 **응답에 나온 시술 노드 전부**에 적용(T2 카드 · T4 쌍 양끝 · T5 · T6 비교 시술 · T7 구성 · T8 이웃) — 응답 `sections[s]` 또는 노드별 `sections` 칸(도구마다 자리는 지금 꼴 유지 · 새 자리는 `node_sections{node id: {section: [fact]}}`)
3. compare rows 에 `overview` · `method`

시험(`tests/test_gold_v3_sections.py`): fail-triage ② 16건의 fact id(SPEC §4-3 F-E 열거)가 같은 입력 + 요청 section 으로 응답 `facts[].id` 에 있음(실물 id · 원문 복사 없음) · 계열 카드 `by_unit` 상한 · T5 `sections=emergency` · T2 `sections=checks` 적용

검증: `uv run pytest tests/test_gold_v3_sections.py tests/test_gold_tools.py -q`

완료 조건: 16/16 fact id 응답에 있음

### WP-3 — `intent` 입력 · 의도 → 섹션 기본 묶음(① 53)

1. `intent?` 공통 입력(REST · MCP · 코어 같은 이름 · 검증 · 오류 문구) · 없으면 도구 기본 의도 · `INTENTS` 상수에 기본 묶음 · 동봉 묶음 열 추가(SPEC §5-13 · §5-14 표와 1:1)
2. `Shape(sections, intent, tool)` → `want` = 기본 묶음 ∪ 요청 · `none` 끔 · `all` 전부 · 응답 머리 `intent_used` · `sections_used[]`
3. section 안 fact 수 상한 `GOLD_SECTION_FACTS_MAX`(넘으면 id 만 + `more`)
4. `gold_quality_eval.py` 가 문항 의도를 `intent` 로 넘김

시험(`tests/test_gold_v3_intent.py`): 12 의도 × 해당 도구 → `sections_used` = 표 값 · 요청과 합집합 · `none` · 모르는 값 4xx · REST ↔ MCP 같은 JSON · `intent` 없음 = 기본 의도 · 상수 ↔ 표 행 수 같음(표는 시험 안 fixture 로 — 원문 아님)

검증: `uv run pytest tests/test_gold_v3_intent.py tests/test_gold_api.py tests/test_gold_mcp.py -q`

완료 조건: 시험 통과 · case3 ① 18건(Jev 상위 4 밖 8 · noul < 0.5 10)의 빠진 section 이 **18/18** 그 의도 기본 묶음에 들어 있음을 표로(SPEC §5-14 v3.1)

### WP-4 — 의도별 고정 동봉(⑤ 90 · ⑦ 20 · ⑥ 18)

1. `memory.py`: 시술 노드마다 동봉 재료 dict(빌드 적재 때 · S4) — SC 엣지(부위 트리 상위 · `units_affected`) · requires_check 전부 · 금기류 relation 요약 · 제품 · 계열 definition fact · 합병증 · 조합(combo_component in · 추천 패키지 먼저) · 패키지(contains in) · 타임라인 · pih 잎 · not_condition · evidence refs(F-A · F-B attached)
2. `tools.py`: `companion(node, intent)` → `{C1..C14 중 해당}`(SPEC §5-13 의도 × 동봉 표 · 상한 · 원문은 상한 안 fact 만 `shape.refs` 에) · 카드 · 쌍 · 비교 · 조합 구성 · 이웃 시술 노드에 붙임 · `more` 셈 유지
3. §5-15 승격: 짧은 조합 카드 `price` · `effect.*` fact id(+ expectedResult 원문 ≤ 2) · 안전 요약 `pih` → `{pih_risk, pih_rate, note}`
4. 상한 설정값(env · 기본 = §5-13 표)

시험(`tests/test_gold_v3_companion.py`): 의도 12 × 도구 → `companion` 칸 집합 = 표 · 상한(SC 3 · relations 6 · products 10/5 · combos 5 · claims 4/쌍 · evidence refs 5) · fail-triage ⑤ 1-hop 42건의 owner 노드 id 가 같은 입력 + `intent` 응답에 있음(표본 — 전수는 WP-7 recheck) · 원문 없는 요약 칸에 `text` 키 없음

검증: `uv run pytest tests/test_gold_v3_companion.py tests/test_gold_tools.py -q`

완료 조건: 시험 통과 · 도구별 기본 응답 크기(in-process · 실물 입력 10 — work003-report 「짧은 카드」 표와 같은 입력) 표 · SPEC §6-5 상한 안

### WP-5 — 쌍 · 비교(④ 27)

1. `pair_check`: `procedures` 1~6 · 1개 = `relations[]`(금기류 먼저 · 상한 6 · `other` 후보) · 계열 하나 · 같은 계열 펼침 → `self_pair[]`(4엣지) · claims **원문 기본**(상한 4/쌍 · 금기류 먼저 · conditional 은 id + 표시로 늘) · 묶음(D-9)은 claims 까지 같을 때만
2. `compare`: `relations[]`(종류 무관) · `source_comparisons[].members[]` 비교 대상 멤버의 attrs_text fact(F-C) 원문 · rows `overview` · `method`(WP-2)

시험(`tests/test_gold_v3_pairs.py`): 1개 입력 → `relations` · 2개 최소 제약 없어짐 · 계열 M2 하나 → `self_pair` E8-0059 값 · ④ 27건의 `procedure_relation` id(부록)가 같은 입력(계열 · 제품 포함) 응답 `edges` · `relations` · `claims` 에 있음(Q114 `none` · 호출 없던 Q130 · Q205 제외 · 그 사유를 표로) · conditional 주장 id 표시

검증: `uv run pytest tests/test_gold_v3_pairs.py -q`

완료 조건: 시험 통과 · 27건 처리표(닫힘 / 호출 없음 / 데이터 없음)

### WP-6 — check_conditions 계열 · 제품 펼침(오류 15)

1. `check_conditions` id 종류에 `family` · `product` 펼침 = `expand_units` 와 같은 규칙 · 상한 `GOLD_EXPAND_MAX_UNITS`(20 · `truncated` · `units_total`) · 조건마다 가장 엄격 등급 하나 + `by_unit{condition: {grade3: [unit]}}` · `expanded{input, kind, units}` · product 키 행은 제품 자체 행 그대로
2. REST path · MCP 설명에 받는 종류 갱신

시험(`tests/test_gold_v3_checks.py`): 계열 6종(M8 · M15 · M4 · M9 · M11 · M12) 200 · `by_unit` 등급 갈림이 접히지 않음(실물에서 갈리는 조건 1개 이상 골라 고정) · 제품 id · 상한 · 없는 id 4xx 그대로 · REST ↔ MCP 같음

검증: `uv run pytest tests/test_gold_v3_checks.py tests/test_gold_api.py -q`

완료 조건: 15건 입력(Q008 · Q021 · Q070 · Q074 · Q096 · Q099 · Q108 · Q120 · Q138 · Q141 · Q150 · Q161 · Q168 · Q169 · Q202 의 `family:M*`)이 in-process 에서 200

### WP-7 — 빌드 발행 · 재인용 측정 · 크기 · 품질 · 전체 검증

1. 로컬 커밋(WP 단위) → 새 빌드 발행(`gold_build.py` · `gold_publish.py`) → `gold_export.py`(새 `gold-export.json` — recheck 가 읽음) → **코디에게 heartbeat 「발행 완료 · 18005 재시작 요청」** · 코디 재시작 전까지는 `--inprocess` 로 잰다
2. `recheck.py --inprocess`(그리고 코디 재시작 뒤 `--base-url http://127.0.0.1:18005` 로 한 번 더 — 둘이 같아야 함): B 재인용률(조항이 닿는 186 기준 · 205 · 239) · 「닫지 않는 행」 19 · 묶음 · 의도 · 오류 15 → 0 · 도구별 기본 응답 크기 중앙 vs §6-5 표 · 두 번 바이트 같음
3. 품질: `gold_quality_eval.py --gold inprocess`(intent 포함) → 6/6 · 106/106 · Q106 · Q108~110 · 회귀 0 · 두 번 같음
4. 전체 검증 한 번: `uv run pytest -q` · ruff · 기존 앱 시험 회귀 0 · **표면 전수 grep(F-7)**: `grep -rn "sections" app scripts tests` · `grep -rn "PAIR_MIN" app tests` · facts cols `grep -rn '"source")' app scripts` 의 결과 파일이 전부 §Scope 표에 있고 `intent` · `attached_to` 가 빠진 곳 0
5. `work005-report.md`: WP 출력 원문 · 재인용률 표 · 크기 표 · SPEC 과 다르게 한 곳(있으면 `ask` 근거) · 남은 것

완료 조건: Done Criteria

## Done Criteria

- [ ] WP-0~6 완료 조건 전부(출력 원문을 report 에)
- [ ] `recheck-report` — B 재인용률: 조항이 닿는 186 행 기준 ≥ 90%(168+) · 205 기준 · 239 기준 값 보고 · 옛/새 export 해시 · 묶음 ①~⑧ · 의도별 표 · 「닫지 않는 행」 19 = §6-5 표와 같음 · 그 밖 닫히지 않은 행 전부 사유(데이터 없음 / 상한 밖)
- [ ] checks 400 15건 → 200 · 재실행 오류 0
- [ ] 도구별 기본 응답 크기 중앙값 ≤ 2 × 현(§6-5 표) · recommend ≤ 14.4KB · p95 보고
- [ ] `quality-report-gold` 6/6 · 106/106 · Q106 · Q108 · Q109 · Q110 맞음 · 회귀 0 · 두 번 같음
- [ ] REST ↔ MCP 같은 JSON(`intent` 포함 9 도구) · 모든 응답에 `claude_contract` · `intent_used` · `sections_used`
- [ ] 새 빌드 해시 · 입력 해시 11 · `counts.v3_facts` · 발행 빌드 id 를 report 머리에 · 18005 재시작은 코디(워커가 하지 않았음을 적음)
- [ ] ruff · 전체 시험 통과 · `git status --short` 원문 · push 0
- [ ] SPEC v3.1 과 다르게 구현한 곳 0 — 있으면 목록 + `ask` 로 합의한 근거 · 표면 grep 누락 0(WP-7 4)
- [ ] `$W` · `$E` 기존 파일 변경 0(`git status` 로 확인 · recheck.py · test_recheck.py · build-out/recheck/ 만 새 파일)

## Rollback

push · 배포 없음. WP-0 기준점 커밋으로 코드를 되돌린다. `attached_to` 리비전은 `alembic downgrade` 로 그 리비전만. 발행은 `gold_publication` 포인터를 이전 빌드(e9d30ace)로 되돌리고 재시작(코디). 지난 빌드 행은 지우지 않는다.

## Open Issues

- SPEC-005 §7 V-1 ~ V-7(사용자 · SPEC-006) — 본문 추천 기본값으로 진행 · 측정 뒤 V-3 상한 숫자 · V-6 문턱 조정 · V-7 끝 조건 분모는 사용자 확인
- 허브를 안 부른 B 17건 · resolve 만 17건 · 「닫지 않는 행」 19 · A 61 · C 6 · 미분류 14 는 이 작업 밖(측정 리포트에는 셈)

## Related

- SPEC-005 0.3.1 · SPEC-005.v2.md(보관) · review-spec005-v3-report.md · WORK-003 · `_RESUME.md` §2 · `fail-triage.md` · `work003-report.md`
