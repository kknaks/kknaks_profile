---
type: spec
id: SPEC-005
title: "허브 골드 그래프 · 결정론 도구 — 실버 · 시맨틱 → 골드 빌드 · 저장 · REST/MCP 도구 9 · 골드 E2E"
status: draft
product: procedure-hub
feature: phub-recommend
version: 0.1.0
created_at: 2026-10-30
updated_at: 2026-10-30
replaces:
  - "SPEC-004"
tags:
  - product/procedure-hub
  - feature/phub-recommend
  - doc/spec
  - status/draft
links:
  decisions:
    - "orchestration/work/phub-recommend/_RESUME.md §2 (10-26 경계 · 10-27 W-1 · 10-29 reading_contract · 10-30 전 행)"
  sources:
    - "orchestration/work/phub-recommend/semantic.json"
    - "orchestration/work/phub-recommend/step1-products.json ~ step8-relations.json"
    - "orchestration/work/phub-recommend/gold-research.md · gold-research.json"
    - "orchestration/work/phub-recommend/quality-eval.py · quality-eval-set.json · quality-report.md"
  work:
    - "orchestration/work/phub-recommend/WORK-003.md"
---

# SPEC-005 — 허브 골드 그래프 · 결정론 도구

> 검수 반영 2026-10-30(F-1 ~ F-5 · W-1 ~ W-9) — `review-spec005-report.md`
> 보강 2026-10-30(raw-mcp · O-1~O-4) — `_RESUME.md` §2 10-30 「원장도 MCP 로」 · 「SPEC-005 열린 것 O-1~O-4 추천대로」

SPEC-004 · WORK-002 를 대체한다. 옛 스펙 · 그래프 v2 와 대조하지 않고 새로 쓴다(_RESUME §2 10-29 「처음부터」).
근거는 아래 정본만이다. 결정을 다시 논의하지 않고, 열린 것은 §7 에만 둔다.

| 정본 | 무엇 | 이 스펙에서 |
|---|---|---|
| `_RESUME.md` §2 | 결정표 | 경계 · 기본 응답 · 충돌 · 품질 목표 · 골드 판단 ①~⑤ · D-01~D-14 |
| `semantic.json` | 노드 13 · 엣지 21 · 사전 2,053 · resolve_rules · id 대응 1,071 · 상속 9 · 표시 12 · gate 3값 | 골드 빌드의 뜻 · id · 읽는 규칙 |
| `step1` ~ `step8` json | 실버 | 골드 빌드 입력(§2) |
| `gold-research.md` · `.json` | 골드 규칙 G1~G17 · 의도 12 · 도구 9 · 경로 11 · 패널 · 속도 장치 | §3 · §5 의 뼈대(정정 3곳 — §3-0) |
| `quality-eval.py` · `quality-eval-set.json` · `quality-report.md` | 품질 3차 · 문항 111 | 골드 E2E 의 정답 세트(§6) |

## 0. 요약

- 허브 = **골드 그래프 + 결정론 조회 도구 9**(REST · MCP 같은 코어). LLM 없음
- 골드 = 실버 · 시맨틱에 규칙 18(gold-research G1~G17 정정 반영 + G18 메뉴 라벨)을 적용해 **빌드 때 단위 시술 수준으로 펼친 그래프**(D-01). 요청 때는 메모리 조회만
- 앱이 읽는 시술 쌍 값 · 확인 조건 등급 · 대기 기간은 8단계 `resolved` 하나뿐(10-30 충돌 하나로). 원문 주장은 근거 · alternatives 로만
- 안전 묶음(부작용 · 합병증 · 확인 조건 · 위험지대 · 금기류 관계 · 피함 · 응급 징후 · 필수 고지 · gap 상태)은 시술이 응답에 나오면 거르기와 무관하게 늘 동봉(10-26)
- 완료 조건: 품질 측정을 **골드 도구 위에서** 다시 돌려 목표 6/6 유지 + 지금 남은 틀림 4문항(Q106 · Q108 · Q109 · Q110)도 맞음 · 로컬 서버 실물 호출 · 속도 측정(§6)

| 절 | 내용 |
|---|---|
| §1 | 범위 · 경계 |
| §2 | 입력 계약(파일 · 해시 · 칸 경로 — 실물 대조) |
| §3 | 골드 빌드(G1~G18 · G1~G17 정정 반영 · 펼치기 · 거르기 · 안전 동봉 · resolved · gap · 결정론) |
| §4 | 저장(스키마 · 적재 방식) |
| §5 | 도구 9(입력 · 출력 · 후보 여럿 · 응답 크기 · 의도별 경로 ①②③) · §5-12 평가용 원장 도구 3(골드 아님) |
| §6 | 품질 · E2E |
| §7 | 열린 것 · 결정된 것(O-1~O-4) |

---

## 1. 범위 · 경계

### 1-1. 허브가 하는 것

| # | 하는 것 | 근거 |
|---|---|---|
| B-1 | 실버 8 + 시맨틱 정본을 골드 그래프로 빌드(규칙 적용 · 펼침 · 표시 · 근거) | 10-30 「골드 = 규칙 적용 그래프 + 허브 도구 탐색(카드 묶음 아님)」 |
| B-2 | 골드를 DB 에 빌드 번호로 저장 · 발행 · 서버가 발행본을 메모리에 올려 조회 | gold-research S4 · D-01 |
| B-3 | 결정론 조회 도구 9 를 REST 와 MCP 로 같은 코어에서 냄 | 10-26 경계 「Hub = 데이터 그래프 + 범용 조회 tool(MCP/REST)만」 |
| B-4 | 말 → 노드 후보는 사전 · 규칙(resolve_rules)으로만 — 후보 여럿이면 전부 | 10-26 「노드 검색도 결정론 · 후보만」 · 10-27 W-1 |
| B-5 | Jev 슬롯 선택지 = 노드 목록 · 스키마(vocab) | 10-26 「Jev 선택지는 Hub 가 노드 목록 · 스키마로 제공」 |
| B-6 | **평가용 원장 도구(골드 아님)** — 원장(브론즈 21 파일)을 그대로 읽는 MCP 도구 3. 골드 · 시맨틱 사전 · 규칙에 기대지 않음 · 허브 본 역할(골드 도구 9)과 섞지 않음(§5-12) | 10-30 「원장도 MCP 로 — hub-evals 는 원장 · 골드를 같은 환경으로」 |

### 1-2. 허브 밖(이 스펙에서 만들지 않음)

| 밖 | 누가 | 근거 |
|---|---|---|
| 질의 해석 · 슬롯 추출 · 추천 판단 · 문장 생성 | 외부 LLM(Jev · Claude) | 10-26 · 10-30 「허브에는 LLM 없음」 |
| 병원 상품 · 가격 · KOS 어댑터 · 미라쥬 영역 대응(연결 층) | 앱 | 10-30 「허브 고정 · 병원 무관 · 병원 상품은 표준 꼴 + 소스별 어댑터 → 연결 층」 · 10-30 「KOS 연결 = 기록만」 |
| 허브 호출 주체(U-2) · 시장가 표시(U-3) | 앱 · 화면 설계 | 10-30 「U-2 · U-3 는 데이터 단계 아님」 |
| 허브 평가 실험(원장 vs 골드 vs 골드 + Jev) | 골드 완성 뒤 별도 | 10-30 「hub-evals 는 골드 완성 뒤」 |
| 실버 · 시맨틱 · 브론즈 수정 | — | 이 스펙은 읽기만. 실버에 빈 곳이 보이면 「허브 보강 후보」(§3-6)로 적고 고치지 않는다 |

- 허브는 단위 시술 id · 제품 id 를 **안정 키**로 낸다(G1). 연결 층은 이 키에 붙는다
- 허브에 없는 것(샘플 대조로 드러난 빈칸)은 허브가 채우지 않고 「허브 보강 후보」 목록으로만 남긴다(10-30)

### 1-3. 코드 자리

| 항목 | 값 |
|---|---|
| 레포 | `/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-recommend` — 로컬 전용 · push 금지 |
| 브랜치 | `kknaksss/phub-recommend`(지금 브랜치 · v1 그래프 파일은 아직 커밋 안 된 상태 — WORK-003 Phase 0 에서 기준점 커밋) |
| 재사용(뼈대만) | `backend/app/graph_main.py`(ASGI 진입점 · `FastAPIBuilder` · lifespan 안 `mcp.session_manager.run()` · `app.mount(MCP)`) · `backend/app/modules/graph/config.py`(env 파일 규칙) · `container.py`(DI 모양) · `backend/graph-local.compose.yml`(postgres 16 · 호스트 55434) · `backend/envs/graph.env.example` · `app/core/tx.db_provider` · alembic 체인 |
| 새로 | 골드 모듈(빌드 · 저장 · 메모리 그래프 · 도구 코어 · REST 라우터 · MCP 서버) · alembic 새 리비전(골드 테이블) · 빌드 · 발행 스크립트 · 시험 · 평가용 원장 모듈 `app/modules/raw/`(§5-12 · 골드와 별도) |
| v1 그래프 모듈 | `app/modules/graph/{application,curation,lowering,domain,sources,validation,resolve,repository}.py` · `app/router/graph.py` 는 골드 앱이 import 하지 않는다(지우지는 않음) |
| 포트 | 앱 `127.0.0.1:18005` · REST 접두 `/procedure-hub/gold` · MCP `/procedure-hub/gold-mcp/mcp`(Streamable HTTP · stateless · JSON) · 평가용 원장 MCP `/procedure-hub/raw-mcp/mcp`(같은 앱 · 별도 마운트 · 같은 전송 — §5-12) · DB `localhost:55434` |
| 사용자 포트 | 3700 · 3800 · 8700 · 8800 · 54329 와 기존 `procedure-*` 컨테이너는 쓰지 않는다(graph-local.compose.yml 머리 주석 그대로) |

---

## 2. 입력 계약 — 실버 · 시맨틱 파일 · 칸 경로(실물 대조 2026-10-30)

입력 폴더 = `orchestration/work/phub-recommend/`(이하 `$W`). 아래 칸 경로는 이 날 실물 파일에서 뽑은 것이다(10-27 SPEC-004 검수 FAIL 「입력 계약이 실물과 다름」 되풀이 방지).

### 2-1. 파일 · 해시 가드

| 파일 | version 칸 | sha256 앞 16자(10-30) | 읽는 이유 |
|---|---|---|---|
| `semantic.json` | `version` = `semantic-v1` | (빌드가 기록) | 노드 · 엣지 종류 · 사전 · resolve_rules · id 대응 · 표시 · 상속 · reading_contract |
| `step1-products.json` | `2` | `41128c7d5bce171b` | 제품 |
| `step2-families.json` | `step2-families v1` | `42eef4dc7dc70b26` | 계열 · 제품 → 계열 |
| `step3-sites.json` | `3.0` | `f92f4a8411c15cd1` | 부위 트리 |
| `step4-techniques.json` | `v1` | `cc6c0291a0b3506a` | 기법 트리 · 계열 기법 · 단위 시술 속성 |
| `step5-units.json` | `step5-units v1` | `38bcc0853547edb7` | 단위 시술 · 제품 연결 · 부작용 덮어쓰기 · PIH · 운영 · 용량 |
| `step6-packages.json` | `step6-packages v1` | `293b50e565ddf61e` | 패키지 |
| `step7-concerns.json` | `step7-concerns v1 (2026-10-29)` | `b2fa90915876de1d` | 고민 · 목적 · 추천 엣지 · 추천 조합 |
| `step8-relations.json` | `step8-v1` | `4f91a2abe7e3aae2` | 관계 · resolved · 확인 조건 · 안전 · 근거 |
| `step7-decisions.json` | `2` | `ae73f09bced8c13b` | 부위 규칙(site_rules) — 질의 때 층 거르기(G6) |
| `step8-decisions.json` | `1` | `2fbeb45c010185e6` | (semantic 입력 · 해시 가드만) |
| `step3-lexicon.json` | `1.1` | `c3b4effa7662af8c` | (semantic 입력 · 해시 가드만) |

- **해시 가드(빌드 실패 조건)**: `semantic.json` `inputs{파일: {version, sha256}}` 11개가 같은 폴더 실물 파일의 sha256 앞 16자와 하나라도 다르면 빌드 실패 — 시맨틱이 실버보다 낡았다는 뜻. 10-30 실물 대조 11/11 같음
- 해시 = `hashlib.sha256(파일 바이트).hexdigest()[:16]`(`semantic-build.py:661` 와 같은 식)
- `semantic.md` 는 읽지 않는다 — 정본은 `semantic.json`
- 브론즈(stg 원본)는 읽지 않는다. 부작용 덮어쓰기 값(G9)과 조합 구성(G17)은 이미 실버에 있다(§2-2 step5 · step7)

### 2-2. 칸 경로

정본 id 는 `semantic.json ids.map[]{canonical, kind, silver_id, name}`(1,071행)로 바꾼다(G1). 실버 안 문자열 꼴(`family:` · `units:` · `bundle:` · `unit:` · `ledger:` · `목적:` · `J{n}-{한글}` · `all`)은 `ids.string_forms[]` · `ids.silver_string_map{}`(41) 규칙대로.

| 파일 | 칸 경로 | 골드에서 | 실물 셈(10-30) |
|---|---|---|---|
| semantic | `node_kinds[]{kind, required, optional, path, count}` · `edge_kinds[]{kind, frm, to, attrs, path, count}` | 종류 목록 · 저장 엣지 셈 가드(S7) | 13 · 21 · 노드 합 1,071 · 저장 엣지 합 3,179 |
| semantic | `dictionary.expressions[]{expr, norm, variants, targets[{id, qualifier, reasons}], sources, collision, mode, ambiguous}` | resolve 사전 | 2,053 |
| semantic | `dictionary.resolve_rules{normalize[], fold{}, strip_chars, split, order[], tails[], prefix_min, prefix_rule}` | resolve 규칙(문서 = 코드) | order 4 · tails 「주사 · 시술」 · prefix_min 2 |
| semantic | `ids.map[]` · `ids.string_forms[]` · `ids.silver_string_map{}` | G1 | 1,071 · 8 · 41 |
| semantic | `reading.reading_contract` · `reading.interval_fields{}` · `reading.flags[]{flag, fields, read}` · `reading.gate_status{values, rule}` · `reading.default_response[]` | 읽는 규칙 · 표시 12 · gate 3값 | flags 12 · gate 3 |
| semantic | `inheritance[]{id, rule, fields}` | I1~I9 | 9 |
| semantic | `statements.table[]{statement, field, class}` | 근거 문장 class(B2) | 119 |
| step1 | `items[]` 중 `active == true` — `ledger_id` · `2_names.display_name` · `2_names.search_names[]` · `1_identity` · `4_license{status, recommendable, licenses[]}` · `5_spec` · `6_companies` · `evidence` · `open` | product 노드 | items 395 · active 354 · recommendable true 236 · false 118 |
| step1 | `lines{라인 이름: {…, items[]}}` | line_item 엣지 · 라인 속성 | 라인 11 · 엣지 5 |
| step2 | `families[]{id, name, name_status, definition, synonyms, sub_families, literature_*}` | family 노드 | 27 |
| step2 | `product_family[]{ledger_id, family, also_families, sub_family, also_sub_families, verdict, evidence_level, conflict, confirm_question, pending_director}` | product_family 엣지 | 354행 → 엣지 370 |
| step3 | `nodes[]{id, name, parent, status, synonyms, anatomical_name, danger_zone}` | site 노드 · 부위 트리 · 최상위 영역 계산 | 53 |
| step4 | `nodes[]{id, name, parent, level, medical_name}` · `family_defaults[]{family, default, also, default_layer}` · `unit_procedure_attrs{safe_layers, target_muscles, landmarks}` | technique 노드 · family_technique 엣지 | 26 · 27 |
| step5 | `units[]{id, key{family, sub_family, ingredient, site, technique}, name, site_basis, synonyms[], candidate_of[], uses_product[], purposes[], route_status, market[], side_effect_override[], pih_not_applicable, ops{}, step4_attrs, dose_range_text, evidence_level, decided_by}` | unit_procedure 노드 · key_* 엣지 · 운영 · 용량 · 시장가 속성 | 162 · side_effect_override 있는 단위 96 |
| step5 | `product_links[]{product, family, sub_family, recommendable, stored_units, inherited_candidates[], technique_excluded, guard, link, side_effect_override[{level, values{common, serious, …}, sub_family, override_of, priority}]}` | I4 assert · 부작용 덮어쓰기(제품 × 계열) | 354 · inherited_candidates 합 1,379 · side_effect_override 있는 제품 316 |
| step5 | `rules.product_link{stored, inherit, guards[], extra_stored[], technique_compat}` | I4 재계산 규칙 | — |
| step5 | `extracted[]{id, keys, attach, product, family, sub_family, source_text{…}}` · `taxonomy_products[]{id, product, attach, keys, source_text}` | 카드 원문 — `source_text` 안 칸은 `aftercare` · `safety.*`(common · serious · note · contraindications · long_term — 부작용 덮어쓰기 원문)뿐(실물: extracted aftercare 521 · safety.common 521 · safety.serious 189 · note 4 · contraindications 4 · long_term 1 / taxonomy_products aftercare 59 · common 59 · serious 31 · note 1 · contraindications 1). `overview` · `mechanism` · `onset_duration` 칸은 0행 | 521 · 59 |
| step5 | `pih[]{attach, target, condition, units}` · `pih_not_applicable_units[]` · `pih_gap_units[]` · `dose_range[]` | PIH · gap 3상태 · 용량 | 26 · 77 · 63 · 11 |
| step6 | `packages[]{id, name, kind, recommendable, synonyms, price, same_day_raw, detail_raw}` · `contains[]` · `slots[]{candidates}` | package 노드 · contains 엣지 | 24(recommendable false 2) · 49 · 8 → 엣지 71 |
| step7 | `concerns.categories[] · subcategories[] · items[] · extra_items[]` · `purposes[]` | concern · purpose 노드 · child_of · concern_related · concern_site | 고민 57 · 목적 13 |
| step7 | `edges[]{source, from, purpose_nodes, to_units, to_family, target_kind, ccs[], cc_named?, layer, site_check, lowering, resolve_flag, concern_region_check, anchor_sites}` | treats 엣지(값 그대로 · 다시 판정 안 함 — G6) | 437 · layer 부위 119 · 상위 35 · null 283 · ccs 있는 엣지 180 |
| step7 | `combos[]{id, kind, source, anchor{concern, concerns, source_label}, name, tier, components[], members[]?, upgrade[]?, schedule[]?, sales_copy{default_response}, concern_regions}` | combo 노드 · anchors_combo · combo_component(구성 칸 이름 그대로) | 79 · 구성 581(components 462 · members 107 · upgrade 12) |
| step7-decisions | `site_rules{lowering, climb, concern_region}` | 질의 때 부위 층 거르기(R21 같은 규칙) | — |
| step8 | `edges[]{id, a, b, endpoints{a,b{kind, id, qualifier, candidates[]}}, self_pair, claims[], conditional_claims, kinds, review_status, review_label, resolved{first, days, open_high, same_day, by_sub_condition, options[], by_direction?, field_status, rules, alternatives[], from_claims, status, inherited_claims, inherited_from_edges}}` | procedure_relation(앱 값 = resolved) | 230 · resolved 230 · by_sub_condition true 32 · by_direction 56 |
| step8 | `resolved_pairs[]{id, a, b, most_specific_edges, applicable_edges, resolved}` | 단위 쌍 값 우선 | 105 |
| step8 | `claims[]{id, kind, text, interval, gate_status, evidence, review_status, …}` | 근거 · alternatives(앱에 바로 안 냄) | 395 |
| step8 | `avoid_edges[]{id, from_concerns, to, qualifier, scope, default_apply}` | concern_avoid | 5(default_apply false 3) |
| step8 | `conditions.nodes[]` · `conditions.claims[]{id, target, target_level, grade3, conditions, scope_conditional, grade3_resolved}` · `conditions.resolved[]{id, target, condition, grade3, status, from, inherited, alternatives}` · `conditions.wait_resolved[]` · `conditions.not_condition[]` | check_condition 노드 · requires_check(등급 = resolved) · 대기 기간 | 53 · 336 · 241(target family 195 · units 20 · all 16 · product 7 · ledger 3) · 1 · 37 |
| step8 | `safety.complications[]{id, family, severity, …, units_inherit}` · `safety.side_effects[]{id, family, …, attach}` · `safety.site_caution[]` · `safety.timelines[]{attach_level, attach, units, phases}` · `safety.pih[]` · `safety.family_text{계열: {칸 이름: 원문}}` · `safety.unit_safety_status[]{unit, fields{…: 값 있음 · 해당 없음(원천) · 정보 없음(gap)}}` · `safety.unit_gaps[]` · `safety.side_effect_gap_families[]` · `safety.complication_gap_families[]` · `safety.complication_mild_only_families` | 안전 묶음 · gap 3상태 | 35 · 72 · 22 · 10 · 26 · 17계열 · 162 · 17 · 10 · 12 |
| step8 | `evidence.statements[]{id, family, field, statement, patient{}, evidence[]}` · `evidence.literature[] · web[] · guides[]` | evidence_statement · evidence_source 노드 · has_statement · cites | 119 · 25 · 29 · 15 |

`safety.family_text` 칸 이름(17계열 공통 · 실물): 필수 고지(consent mandatory_disclosures) · 즉시 내원이 필요한 징후(consent emergency_signs) · 환자 설명 가이드(patient-education) · 사후관리 3종(taxonomy modality extracted.aftercare · extracted.json aftercare · procedure-profiles aftercare) · 부작용 문장 common · uncommon · serious(근거 — 합병증 노드 아님) · 상담 · 준비 · 고지 · 조건 아닌 문장(16) · 응급(extracted.json safety.emergency · 2) · critical_safety_facts(anatomy · 1) · 안전 원문(규칙 행 · 쌍 없음 · 1). 카드 칸 대응은 §5-4.

---

## 3. 골드 빌드

### 3-0. gold-research 대비 정정(이 스펙이 정본)

| 곳 | gold-research | 이 스펙 | 근거 |
|---|---|---|---|
| G14 · D-08 | 충돌 = 고르지 않고 값 집합 · 양쪽 주장 id | **충돌 = 8단계 `resolved` 하나.** 값 집합 요약 안 만듦 · 원문 주장은 `alternatives` · 근거로만 | 10-30 D-13b 바꿈 · 10-30 골드 판단 「D-08 → 충돌은 resolved 하나만」 |
| G9 · D-07 | 부작용 덮어쓰기 값은 실버에 없음 → 적재가 브론즈 원문을 싣는다 | 값은 실버 `step5 units[].side_effect_override[]` · `product_links[].side_effect_override[]` 에서 읽는다. 브론즈 안 읽음 | 품질 3차 ③(quality-report §0-2) · 실물 96 · 316 |
| G17 · D-04 | combo_component 462 → 581 로 정본 보강 | 7단계 · 시맨틱이 이미 581(components · members · upgrade) — 그대로 읽는다 | 품질 3차 ④ · semantic edge_kinds combo_component 581 |
| G3 | semantic I1 문구 「추천 계열만」을 SPEC-005 에서 뺀다 | treats 「계열만」은 펼치지 않는다(골드 판단 ④ · W2 유지) | 10-30 골드 판단 ④ |
| 골드 판단 ⑤ | 다파장 4(노블린 · 클라리티2 · 아포지 엘리트 플러스 · 디스커버리 피코) KTP 보조 하위 | 실버 `step2 product_family[].also_sub_families` 에 이미 반영(실물 4행 KTP) — G5 가 그 칸을 읽어 단위 시술 연결에 씀. 골드에서 따로 하는 일 없음 | 10-30 골드 판단 ⑤ |
| 판단 ② 범위 | 「메뉴 이름 → 추천 조합(쁘띠시술 등)」 | 메뉴 이름 = 사이트 추천 패키지 메뉴 라벨(`anchor.source_label`) **8개 전부**(G18) — 쁘띠시술만이 아님. 판단 ③ 만으로는 7단계 R12 앵커(「피부결/톤/항노화」 = P4 + P5 + 피부결)로 P5 질의에 P4 패키지가, P4 질의에 하위 P4-1 앵커로 P3 패키지가 섞여 Q109 · Q110 이 틀림(실물 셈) | 코디 답 10-30(이 스펙 작성 중 ask · 「같은 규칙의 일관 적용」) · J5 「사이트 「고민 선택」에는 그대로 뜸(원천 라벨)」 |
| §3 셈 | I4 1,364 · 저장 엣지 3,044 | 고정 숫자를 쓰지 않는다 — **빌드 때 입력 파일에서 센 값과 대조**(지금 실물 I4 1,379 · 저장 엣지 3,179) | 실물 대조 · step2 고정 assert 의 「알려진 한계」(_RESUME 10-28) |

### 3-1. 규칙 G1~G17

| id | 규칙 | 골드에서 하는 것 | 가드(빌드 실패) |
|---|---|---|---|
| G1 | 정본 id | 모든 노드 · 엣지 끝을 `ids.map` 으로 정본 id(`{kind}:{키}`)로 바꿔 싣는다. 단위 시술 · 제품 id 는 안정 키 | 맵에 없는 실버 id 가 엣지 끝에 있으면 실패 |
| G2 | 계열 → 단위 시술 펼치기(I1) | 관계 · 확인 조건 · 합병증 · 근거 문장 · 부작용 · 위험지대 · 피함의 **계열 끝**을 `key.family` 가 그 계열인 단위 시술 전부로 펼쳐 단위 시술 수준 행으로 싣는다. 행마다 `inherited_from`(계열 정본 id) | 펼친 합병증 행 수 = `safety.complications[].units_inherit` 길이 합(실물 285) |
| G3 | treats 「계열만」은 펼치지 않음 | `step7 edges[] target_kind == 계열만` 은 계열 엣지 그대로 + 표시(site_check · resolve_flag 값 그대로) | — |
| G4 | 하위 계열 · 기법 조건 끝(I2 · I3) | `endpoints.*.qualifier.sub_family` · `.technique` 끝은 같은 하위 · 같은 기법(또는 하위 기법) 단위 시술로. 키에 그 하위 없는 계열은 「candidates」 표시 | — |
| G5 | 제품 → 단위 시술(I4) | `step5 rules.product_link`(같은 계열 주 · 보조 · 하위 일치 · technique_compat · guards · extra_stored)를 다시 계산 | 결과가 `product_links[].inherited_candidates` 와 제품마다 같아야 함 · 저장 `units[].uses_product` 합(실물 44)과 같아야 함 |
| G6 | 부위 — 저장값 그대로 · 질의 때 거르기 | treats 엣지의 부위 판정(R21 · R22 · R23 · R25 · R28 · R32)은 7단계 값 그대로(다시 판정 안 함). 질의에 부위가 오면 `step7-decisions site_rules.climb` 와 같은 층 규칙으로 거른다 · `site_rules.site_free`(「해당 없음」 · 「병변 단위」) 단위 시술은 층 거르기 통과(품질 2차 · quality-report §0-1) · `layer` 「상위」(얼굴 전체 층)도 같이 낸다(골드 U-1 = ②) | — |
| G7 | 끝점 묶음(I6) | `candidates[]` 는 OR — 펼친 행마다 `candidates` 표시. 고르지 않는다 | — |
| G8 | 조건부 제외(I7) | `default_apply false` · `scope_conditional true` 는 펼치되 `conditional` 표시 → 기본 응답 · 기본 탐색 · 값 접기에서 뺀다(`include_conditional` 로만) | — |
| G9 | 부작용 덮어쓰기(I8) | 계열 부작용(`safety.side_effects[] attach family:*`)을 단위 시술로 펼친 뒤, 아래 수준 `side_effect_override[]` 값이 있으면 그 값으로 바꾼다. 우선순위 = `priority` 칸 — **작을수록 먼저**: 0 제품 × 계열 × 키 하위(실물 111) < 1 제품 × 계열(207 · taxonomy products 58) < 2 단위 시술(159) < 3 단위 시술 후보(89) < 계열 값. 덮인 계열 값은 `override_of` 로 근거만 남김. 계열 부작용이 gap 인 계열(`safety.side_effect_gap_families` — N1~N10)을 덮은 행(실물 72 — N1 63 · N4 4 · N5 2 · N2 1 · N6 1 · N7 1)은 아래 수준 값이 유일한 값 — `override_of` 를 남기고 계열 쪽 상태는 「정보 없음(gap)」. **합병증 노드는 덮지 않는다** | `override_of` 가 계열 노드(27)에 없으면 실패 |
| G10 | 해당 없음 ≠ gap(I9) | 안전 칸마다 상태 3값 — `값 있음` · `해당 없음(원천)` · `정보 없음(gap)` — `safety.unit_safety_status[].fields` 그대로. 합병증 원천이 전부 mild 인 계열은 「중대 반응 없음(원천)」 | unit_safety_status 가 단위 시술 162 전부를 덮지 않으면 실패 |
| G11 | 붙는 수준 원문 | 경과 타임라인(`safety.timelines[] attach_level · attach · units`) · PIH(`step5 pih[]` · `step8 safety.pih[]`) · 운영(`units[].ops`) · 계열 원문(`safety.family_text`)은 원천이 가리킨 수준에 붙여 아래로 상속(엣지 아님 · 속성). 하위 계열에 붙은 것은 그 하위 단위 시술만 | — |
| G12 | 기본 응답 거르기 | 뺀다: 제품 `4_license.recommendable false` · 패키지 `recommendable false` · 병원 시그니처 · 영업 문구(`sales_copy.default_response false`) · conditional · 시술 아님 · 못 풂. gate 3값(자동(완전 일치) · 자동(규칙) · 결정)은 전부 통과 — 「미확인」은 상태가 아니라 표시(question · weak · gap)로 값과 같이 낸다(10-27 W-1 · D-05) | — |
| G13 | 안전 정보 늘 동봉 | 시술이 응답에 나오면 거르기와 무관하게: 합병증 · 부작용 · 확인 조건(전 등급) · 위험지대 · 금기류 관계(간격 금기 · 조합 금기 · 같은 날 불가 · 대체(택 1)) · 피함(조건부 아닌 것) · 응급 징후 · 필수 고지 · gap 상태(D-06 · 10-26) | — |
| G14 | 충돌 = resolved 하나(정정) | 시술 쌍 값 = §3-3. 확인 조건 등급 = `conditions.resolved` · 대기 기간 = `conditions.wait_resolved`. 원문 `claims[].interval` 은 근거 · `alternatives` 로만 | 단위 쌍마다 앱 값이 둘 이상이면 실패(§3-3 가드) · 단위 시술 × 조건 등급이 둘 이상이면 실패 |
| G15 | by_sub_condition | 겉 칸이 null 이고 `by_sub_condition true` 면 `options[]` 를 그대로 전달 — 한 값으로 접지 않는다. 조건을 모르면 `sub_condition` 「조건: 모름(전부 접음 — 가장 보수적)」 옵션 | 옵션이 있는 칸의 겉 칸이 채워져 있으면 실패 · 조건 모름 옵션이 칸마다 정확히 1개가 아니면 실패 |
| G15b | by_direction | 같은 날 값이 먼저 하는 쪽에 따라 갈리면 `resolved.by_direction.a\|b.same_day`(a = 엣지 a 끝 먼저 · 겉 same_day null)를 그대로 전달 · 쌍 방향에 맞춰 a/b 를 뒤집어 싣는다 | 겉 same_day 가 채워졌는데 `None` 을 뺀 방향별 same_day 값이 둘 이상이면 실패(`step8-apply.py:2008` 과 같은 식 · 실물 0 — 한쪽 None 인 11건은 통과) |
| G16 | 와일드카드 · 전역은 안 펼침 | 「모든 시술」 끝 관계(`endpoints.*.kind == 모든 시술`)와 `conditions.resolved[] target == all`(16)은 전역 행 하나로 두고 모든 시술 응답에 붙인다 | — |
| G17 | 추천 조합 구성 | `combo_component` = `combos[].components\|members\|upgrade[].units[]`(구성 칸 이름 `field` 그대로 · order · status · flag) | 셈 = semantic combo_component count(실물 581) |
| G18 | 메뉴 라벨(판단 ② · 코디 10-30) | 사이트 추천 화면 라벨 = `step7 combos[] kind == 「고민 패키지(사이트 「추천 패키지」)」` 의 `anchor.source_label`(실물 8 — 주름 4 · 처짐/탄력 4 · 쁘띠시술 3 · 피부결/톤/항노화 3 · 색소/미백 3 · 모공 3 · 흉터 2 · 얼굴윤곽 2). 라벨마다 resolve 사전에 `menu:{라벨}` 대상(kind `menu` — 노드 종류 13 에 안 넣음 · 사전 대상 · T7 입력 값일 뿐)을 더한다 — 같은 norm 행이 있으면 그 match 안에 **별도 후보**로 더하고 기존 고민 대상의 mode(전부 · 하나 · 후보)는 바꾸지 않는다(코디 판단 ① · 10-30 「고민 id 질의는 그대로」) · 없으면 새 행. 실버 · 시맨틱은 안 고침 | 라벨 수 = 실물 셈(8) · 라벨마다 추천 패키지 1+ |

### 3-2. 펼치기 · 거르기 · 안전 동봉 순서(빌드 한 번)

1. 입력 해시 가드(§2-1) → 실패면 멈춤
2. 노드 1,071 을 정본 id 로 싣기(G1) · 표시 12(`reading.flags[].fields` 의 실버 칸에서) · gate 3값(`reading.gate_status.rule` — gate 칸 있으면 그대로 · 없으면 decided_by 가 사용자 결정 id 면 「결정」 · 나머지 「자동(규칙)」)
3. 저장 엣지 21종을 싣기(semantic edge_kinds path 대로) → 저장 엣지 셈 = semantic 셈(S7 · 종류마다)
4. 펼친 엣지 계산: G2 · G4 · G5 · G7 · G9 · G11 · G16 · G17 → 단위 시술 수준 행(행마다 `derived_by`(G 규칙 id) · `inherited_from` · 표시)
5. 시술 쌍 값 · 확인 조건 등급 계산(§3-3)
6. 기본 응답 표시(G8 · G12) — 지우지 않고 `default_out: true` 칸으로(조회 옵션으로 다시 낼 수 있게)
7. 안전 묶음(G13)을 단위 시술 · 제품마다 미리 모아 둔다(카드 응답이 dict 조회 하나로 끝나게 — S4)
8. 카드 원문 facts 만들기(§4-3 · fact id 결정론)
9. 사전 적재 — `dictionary.expressions` + 메뉴 라벨(G18)
10. 빌드 가드 전부(§3-1 가드 열 · §3-3 · §3-5) → 하나라도 실패면 발행 안 함
11. 빌드 해시(§3-5) · 셈 기록 · 발행

### 3-3. 시술 쌍 값(reading_contract 그대로)

| 경우 | 앱 값 |
|---|---|
| 단위 쌍이 `step8 resolved_pairs[]` 에 있음(105) | 그 `resolved` |
| 없음 | 그 쌍에 닿는 엣지 중 **가장 구체적인 엣지**들의 `resolved`(엣지 a 끝이 쌍의 어느 쪽인지에 맞춰 first · by_direction 을 뒤집음). 가장 구체적 = 다른 닿는 엣지의 끝 단위 집합을 자기 끝 집합이 덮지 않는 엣지(`step8-apply.py:1976` 의 `covers` · `:2022-2050` 의 `most_specific` · `two_value` 정의). 위 엣지 주장은 8단계가 상속해 이미 접었다(`resolved.inherited_claims`) |
| 쌍에 닿는 엣지 없음 | 관계 없음(「정보 없음」 · 빈 값) |
| 전역(「모든 시술」) | 모든 쌍 응답에 전역 행을 따로 붙임(G16) |
| 같은 단위 시술끼리(자기 쌍 · 재시술 간격) | 8단계 쌍 셈은 u == v 를 건너뛴다(`step8-apply.py:2028`) — 자기 쌍은 `edges[].self_pair == true` 엣지(실물 4 — E8-0059 M2↔M2 · E8-0214 · E8-0225 · E8-0228)의 `resolved` 만 읽는다. 끝 단위 집합에 그 단위 시술이 든 자기 쌍 엣지 중 가장 구체적인 것 · 없으면 관계 없음 |

- **가드**: 단위 쌍마다 위 규칙의 값이 하나(가장 구체적 엣지들 값이 갈리면 resolved_pairs 에 있어야 함) — 8단계 전수 가드(`two_value`)와 같은 검사를 골드에서 다시 한다. 실물(`UnitSets` 셈): 전역 엣지(G16 · E8-0001 「모든 시술」) 제외 229엣지 → 단위 쌍 4,674 · 엣지 둘 이상 닿는 쌍 2,048 · 그중 resolved_pairs 100 · 나머지는 가장 구체적 엣지 값이 하나 / 전역 엣지 포함 230엣지 → 4,791 · 2,075 · 105 — resolved_pairs 105 중 5 는 전역 엣지 때문에만 생긴 쌍(전역 행으로 따로 붙이므로 G16 과 같이 읽음)
- 확인 조건 등급: 단위 시술 × 조건마다 `conditions.resolved[]` 중 대상 키(units · family · all)가 그 단위 시술을 덮는 가장 구체적인 것(`step8-apply.py:2101` `key_covers`) — 둘 이상이면 가드 실패. 실물 대상 키 = family 195 · units 20 · all 16 · product 7 · ledger 3. **product 7 · ledger 3 은 단위 시술을 하나도 덮지 않는다**(`key_covers` · UnitSets 빈 집합) — product 키 행(product:M1-1-7 4 · product:M9-2-3 3)은 그 제품에만 붙음(T3 제품 카드 · T5 `id=product`) · 단위 시술로 내리지 않음. ledger 키 행(KR8-0212~0214 · `ledger:auto-6-…` 3 — 원장 「넥큐레이션」 · 5단계 행선지 6단계 패키지)은 **`package:P6-03` 에 붙인다**(10-30 O-4 결정 · 대응 = `step6 packages[].ledger_id`) — T5 `id=package` · T7 `packages[]` 의 안전 묶음에 실림 · 단위 시술로 내리지 않음. 가드: ledger 키마다 `ledger_id` 가 같은 패키지가 정확히 1개(아니면 실패)
- 이전 시술 경과 판정(I-08 · D-10): 경과일 ≥ `days[0]`(하한)이면 충족 · 상한 · `open_high` 는 원문 표시만 · `same_day` 는 경과 0 일 때만 · by_sub_condition 이면 옵션별 판정을 다 냄
- 앱 값에 원문 `claims[].interval` 을 섞지 않는다. 쌍 응답의 `claims` 칸은 `{id, kind, text}`(근거) · `alternatives` 는 resolved 칸 그대로

### 3-4. gap 3상태

| 상태 | 뜻 | 실버 칸 | 응답 |
|---|---|---|---|
| `값 있음` | 원천 값 있음 | `unit_safety_status[].fields.*` | 값 + facts |
| `해당 없음(원천)` | 원천이 「해당 없음」이라 함(PIH 해당 없음 계열 등) | `pih_not_applicable_units` · fields | 「해당 없음」 그대로 |
| `정보 없음(gap)` | 원천에 없음 — 「없음 = 안전」 아님 | `pih_gap_units` · `side_effect_gap_families` · `complication_gap_families` · `unit_gaps` | 「정보 없음」 + `gap` 표시(must_show) |
| (보조) `중대 반응 없음(원천)` | 합병증 원천은 있으나 전부 mild | `complication_mild_only_families` | 합병증 칸 상태로 |

### 3-5. 결정론 · 빌드 해시 · 가드

- 같은 입력(해시 11 같음) → 같은 골드. 시각 · 난수 · 순서 미정 dict 순회 · 환경 값이 골드 내용에 들어가지 않는다
- **빌드 해시** = 골드 내용(노드 · 엣지 · facts · 사전 · 전역 행)을 정본 id 순으로 정렬한 canonical JSON(`sort_keys`, `ensure_ascii=False`, 구분자 고정) 의 sha256 앞 16자. 입력 해시 11 과 같이 `gold_build` 에 기록
- 같은 입력으로 두 번 빌드 → 빌드 해시 같음(가드 · 시험)
- 빌드 가드 묶음(S7 확장): 입력 해시 · 저장 엣지 셈(종류마다 = semantic) · 노드 셈(종류마다 = semantic) · G1 · G2 합병증 285(= units_inherit 합) · G5 I4(= product_links 제품마다) · G10 · G14 · G15 · G15b · G17(= 581) · 고정 숫자 대신 입력 파일에서 센 값과 대조
- 펼친 뒤 셈은 빌드가 계산해 `gold_build.counts` 에 기록(gold-research §2-1 의 24,392 는 그때 입력 기준 참고값 — 가드 아님)

### 3-6. 허브 보강 후보

빌드 · 도구가 찾은 「허브에 없는 것」은 고치지 않고 목록으로만(10-30). 출처 2갈래:

- 빌드: resolve 사전에 없어 sample 대조에서 비는 말 등 — gold-research D-18 이 든 3건(쥬비덤 볼루마 품목 · 「Sofwave」 단독 표기 · 소프웨이브 「2주 사우나」(원천 없음))을 첫 행으로
- 빌드: 단위 시술 · 제품마다 따로 쓴 개요 · 기전 · 발현 · 지속 문장 없음(실버 `source_text` 에 그 칸 0행 · 계열 수준 환자 설명 가이드만 — F-1)
- 도구: `resolve` 의 `unmatched` 를 E2E 동안 모은 것

산출 = `gold-hub-gaps.json`(코드 레포 빌드 출력 폴더) · 각 행 `{text, where, kind, first_seen_build}`. 실버 반영은 사용자 결정 몫(이 스펙 밖).

---

## 4. 저장

### 4-1. 적재 방식

1. **적재**(Phase 1): `$W` 의 입력 파일 12(§2-1)를 원문 그대로 `gold_source_snapshot` 에 넣는다(파일 이름 · version · sha16 · 바이트 크기 · JSON 본문). 같은 sha 면 다시 안 넣음
2. **빌드**(Phase 2): 스냅샷 한 벌(파일 12 의 sha 묶음)을 읽어 골드 계산 → `gold_build` 한 행 + 그 빌드의 노드 · 엣지 · facts · 사전을 **한 트랜잭션**으로. 가드 실패면 `status = rejected` 로 기록만(행 안 씀)
3. **발행**: `gold_publication` 의 현재 포인터를 새 빌드로 바꾼다(지난 빌드는 지우지 않음)
4. **서버**: 시작 때 발행된 빌드를 메모리 그래프로 올린다(dict · 인접 목록 · 사전 norm 색인). 요청은 메모리만 읽는다(S4). 발행 바뀌면 재시작으로 반영(이 스펙 범위)

명령(코드 레포 `backend/` 에서 · 이름은 WORK-003 이 정함): 적재 `--from-dir $W` · 빌드 · 발행 · 서버 기동. env 는 `envs/.env.gold`(git 제외 · 예시 파일만 커밋 · 비밀값 없음).

### 4-2. 스키마(새 alembic 리비전 · 기존 테이블과 FK 없음)

| 테이블 | 키 | 칸 |
|---|---|---|
| `gold_source_snapshot` | `id` | `file` · `version` · `sha16` · `size` · `body jsonb` · `loaded_at` |
| `gold_build` | `id` | `started_at` · `finished_at` · `status`(published · rejected · unchanged) · `input_hashes jsonb`(파일 12 → sha16) · `build_hash` · `counts jsonb` · `guards jsonb`(가드마다 기대 · 실제 · 통과) |
| `gold_node` | (`build_id`, `id`) | `kind`(13) · `name` · `attrs jsonb`(실버 필수 · 선택 칸 · 운영 · 용량 · 시장가 · PIH · 계열 원문 상속 결과) · `flags jsonb`(표시 12 중 해당) · `gate_status` · `default_out bool` · `source_refs jsonb`(실버 파일 · 경로 · 실버 id) |
| `gold_edge` | (`build_id`, `id`) | `kind`(21 + 펼친 종류) · `from_id` · `to_id` · `stored bool`(저장 엣지 / 펼친 행) · `derived_by`(G id) · `inherited_from` · `attrs jsonb` · `resolved jsonb`(procedure_relation · requires_check 만) · `flags jsonb` · `gate_status` · `layer` · `default_out bool` · `evidence jsonb`(주장 id · 근거 출처 id) |
| `gold_global` | (`build_id`, `id`) | 전역 행(G16) — `kind` · `payload jsonb` |
| `gold_fact` | (`build_id`, `id`) | `owner_id` · `section`(§4-3) · `text`(원문 그대로) · `flags jsonb` · `state`(값 있음 · 해당 없음 · 정보 없음) · `source`(실버 경로 · evidence_source id) |
| `gold_dictionary` | (`build_id`, `norm`) | `expr` · `variants` · `targets jsonb` · `mode` · `ambiguous` · `collision` |
| `gold_publication` | `id`(한 행) | `build_id` · `published_at` |

- 인덱스: `gold_edge(build_id, from_id)` · `(build_id, to_id)` · `(build_id, kind)` · `gold_fact(build_id, owner_id)`. 인덱스 · 제약 이름을 명시(v1 `app/model/graph.py` 머리 주석의 naming 충돌 교훈)
- jsonb 는 postgres · 시험용 sqlite 는 JSON(v1 `_JSON_DOCUMENT` 꼴 재사용)

### 4-3. facts(근거 인용 단위 · S5)

- fact = 응답에 나가는 원문 한 덩이. 원문은 고치지 않는다(번역 · 요약 · 합치기 없음)
- **fact id(결정론)**: 원천에 id 가 있으면 그 id(`ST-…` · `SE-…` · `CX-…` · `K8-…` · `KR8-…` · `WR8-…` · `R8-…` · `SC-…` · 타임라인 `id`) · 없으면 `{owner 정본 id}#{section}#{실버 칸 경로}[{순번}]`(예: `unit_procedure:U5-001#ops#durationMin`)
- 부작용 덮어쓰기 fact 는 `override_of` · `priority` · 덮은 수준(`level`)을 같이 싣는다
- section 값: `overview` · `method` · `recovery` · `aftercare` · `timeline` · `emergency` · `disclosure` · `safety.side_effects` · `safety.complications` · `safety.pih` · `checks` · `site_caution` · `dose` · `products` · `evidence` · `ops` · `market`

---

## 5. 도구(REST · MCP 같은 코어 · LLM 없음)

### 5-0. 공통

- 도구 코어 = 순수 함수(메모리 그래프 → 응답 dict). REST 라우터와 MCP tool 은 같은 함수를 부르기만 한다(v1 `mcp_server.py` 머리 원칙과 같음). 입력 이름 · 기본값 · 검증 · 오류 문구가 둘에서 같다
- 모든 응답 머리: `{"build": {"id", "build_hash", "published_at"}, "request": {입력 그대로}, …}`
- 오류: 없는 id · 틀린 종류 · 한도 넘음 = 4xx + 도메인 오류 문구(MCP 는 같은 문구의 tool 오류)
- **후보 여럿 처리**(10-27 W-1 · G7): 말이 여러 노드를 가리키면 고르지 않고 후보 전부 + `candidates` 표시. 도구 입력은 id 만 받는다(말은 resolve 만 받음). 되묻기는 밖(LLM · 앱)
- **표시**: 행마다 표시 12 중 해당하는 것을 그대로(S6). 응답 끝 `must_show_flags` = 응답 안에 실제로 나온 표시 중 conflict · candidates · gap · weak · question · default_value · license_unconfirmed 의 집합
- **Claude 계약 블록**(10-30 O-3 결정 = D-16 추천): 응답마다 `claude_contract{allowed_fact_ids, must_show_flags, rule}` — `allowed_fact_ids` = 이 응답 `facts[].id` 전부 · `must_show_flags` = 위 표시 집합 · `rule` = 고정 문장 「카드 밖 말 금지 — 문장마다 facts id 하나 이상 · 숫자 · 기간 · 금기는 facts 원문 값만 · 시술 쌍 값은 resolved 하나(원문 대안은 alternatives 로만) · gap 은 「정보 없음」 · 후보 여럿이면 되묻기」(gold-research 6-3 문장에서 「충돌은 양쪽」만 10-30 D-13b 「충돌 하나로」에 맞춤). 허브는 블록을 낼 뿐 지키게 하는 건 앱 · Claude 몫
- **기본 응답**: G12 거르기 · G8 조건부 제외 적용. 옵션 `include_conditional`(기본 false) · `include_not_recommended`(기본 false)로만 뺀 것을 다시 냄(뺀 것은 `excluded_counts` 로 셈만 늘 냄)
- **안전 동봉**: 시술(단위 시술 · 제품)이 응답 어디에든 나오면 그 시술의 G13 안전 묶음을 같이 냄 — slim 이어도 안전 칸은 빠지지 않음(상태 · fact id · 짧은 이름. 긴 원문은 full)
- **응답 크기**(D-14 · S1 · S2): 카드는 기본 slim · 원문 전문은 `sections` 를 요청했을 때만 · 단위 시술 관계 목록은 카드에 싣지 않고 `pair_check` 로만
- **facts**: 응답에 나온 원문은 `facts[]{id, text, section, flags, state, source}` 로 모아 내고 카드 · 행은 fact id 로 가리킨다

### 5-1. 도구 목록

| id | 이름 | REST | MCP tool | 의도 | 경로 |
|---|---|---|---|---|---|
| T1 | resolve | `GET /procedure-hub/gold/resolve` | `resolve` | 공통(말 → 후보) | — |
| T2 | recommend | `POST /procedure-hub/gold/recommend` | `recommend` | I-01 | P-01 |
| T3 | procedure_card | `GET /procedure-hub/gold/procedures/{id}` | `procedure_card` | I-02 · I-03 · I-04 · I-05 · I-10 | P-02~P-05 · P-10 |
| T4 | pair_check | `POST /procedure-hub/gold/pairs` | `pair_check` | I-07 · I-08 | P-07 · P-08 |
| T5 | check_conditions | `GET /procedure-hub/gold/procedures/{id}/checks` | `check_conditions` | I-09 | P-09 |
| T6 | compare | `POST /procedure-hub/gold/compare` | `compare` | I-06 | P-06 |
| T7 | combos | `GET /procedure-hub/gold/combos` | `combos` | I-11 | P-11 |
| T8 | neighbors | `GET /procedure-hub/gold/nodes/{id}/neighbors` | `neighbors` | 정해 둔 경로 밖 | — |
| T9 | vocab | `GET /procedure-hub/gold/vocab` | `vocab` | Jev 슬롯 선택지 | — |

- 헬스 `GET /procedure-hub/gold/health` = DB 연결 · 발행 빌드 id · 메모리 적재 셈(도구 셈에 안 넣음)
- I-12 가격은 허브 도구 없음(연결 층) — 허브는 단위 시술 · 제품 id 만

### 5-2. T1 resolve — 사전 검색

| 칸 | 값 |
|---|---|
| 입력 | `text: str`(필수 · 1~200자) · `kinds?: [node kind]`(거르기) · `limit_per_span?: int = 20`(≤ 50) |
| 규칙 | `semantic.json dictionary.resolve_rules` 그대로(문서 = 코드 · 품질 M): 정규화(NFKC → 라틴 악센트 접기 → fold 「쳐짐 → 처짐」 → 공백 제거 → 괄호 지움 → 소문자) → order 4단계: ① 완전 → ② 낱말 나눔(split `[\s/·,()\[\]+]+` 으로 나눠 낱말마다 완전) → ③ 끝말 떼기(tails 「주사 · 시술」) → ④ 접두(질의 2자 이상 · 대상 계열 · 고민 대분류 · 부위 · 목적이 하나로 모일 때만 — 여럿이면 못 찾음). 앞 단계에서 찾으면 다음 단계 안 감(D-11) |
| 출력 | `{"matches": [{"span", "stage": "완전\|낱말\|끝말\|접두", "mode": "하나\|전부\|후보", "ambiguous", "collision", "candidates": [{"id", "kind", "name", "qualifier", "reasons", "flags"}], "menu_candidates": [{"id", "label", "kind"}]}], "unmatched": [str]}` |
| qualifier | 사전 `targets[].qualifier` 그대로 — `{"cc": …}`(CC 고민 앵커 · R28) · `{"taxonomy_entry": "P1"}`(메뉴 · J5) · `{"ledger": …}` 등 |
| 메뉴 후보 | G18 이 더한 `menu:{라벨}` 대상은 같은 match 안의 별도 후보 `menu_candidates[]{id, label, kind: "menu"}` 로 낸다 — 기존 `candidates[]` 와 `mode` 는 사전 그대로(예: 「처짐/탄력」 → `candidates` = P3 · P4-1 · mode 「전부」 그대로 + `menu_candidates` = `menu:처짐/탄력` · 「쁘띠시술」 → `candidates` = `none:고민 노드 아님(트리 항목)` + `menu_candidates` = `menu:쁘띠시술`). 메뉴 후보는 T7 `menu` 입력으로만 이어짐(판단 ②) · 고르지 않음 |
| mode | `하나` = 대상 1 · `전부` = 대상 전부에 적용(묶음 이름 → 고민 여럿 · 갈래 A · I) · `후보` = 고르지 않음(나머지 갈래) |
| 부분 일치 표시 | 접두로 찾은 후보는 `flags` 에 `prefix` |
| unmatched | 끝까지 못 찾은 낱말 — §3-6 보강 후보로 기록(응답에는 그대로) |

### 5-3. T2 recommend — 고민 → 추천(① CC 슬롯)

| 칸 | 값 |
|---|---|
| 입력 | `concerns: [concern id]`(1+) · `site?: site id` · `cc?: str`(원천 CC 이름 · 골드 판단 ① · R28) · `include_conditional?: false` · `include_not_recommended?: false` |
| 경로 P-01 | ① 고민 + 하위 고민(child_of) — 조상 · 자손이 같이 오면 자손만 · 고민에 부위 1개면 그 부위 · 부위만 오면 그 부위 고민 → ② **cc 가 오면**: 같은 원천 문제(P) 안에서 `ccs[]` 에 그 CC 가 든 treats 엣지만(출발이 고민 · 목적 · 앵커 없음이어도 CC 로 찾음). cc 가 없거나 원천 CC 가 아니면 고민 노드 treats 엣지 전부 → ③ 부위 층 거르기(`site_rules.climb` — 부위 · 하위 → 상위(묶음 통과) → 영역 「전체」 노드 · `site_rules.site_free` 「해당 없음」 · 「병변 단위」 단위 시술은 통과) · `layer` 「상위」(얼굴 전체 층) 엣지도 같이 내되 `layer` 표시(U-1 = ②) → ④ 부위 없이 고민만이면 기본 영역 = 얼굴 + 다른 영역 시술이 있으면 `other_regions` 표시(D-12) → ⑤ 단위 시술마다 G13 안전 묶음 · 쓰는 제품(G5 · recommendable 만) · 추천 조합 앵커 id |
| 출력 | `areas[]{site, name, layer: "부위\|상위\|영역 전체", concerns[], card_ids[]}` · `cards[]`(slim 카드 §5-4 + `why[]{edge, from, source, layer, flags}`) · `family_only[]{family, reason(site_check · resolve_flag 값), flags}` · `facts[]` · `must_show_flags` · `excluded_counts` |
| 정렬 | 결정론 — `layer`(부위 → 상위) · 엣지 원천 순서 · 단위 시술 id |

### 5-4. T3 procedure_card — 시술 카드

| 칸 | 값 |
|---|---|
| 입력 | `id: unit_procedure\|product\|family id` · `product?: product id`(단위 시술 카드에 특정 제품 원문 · 부작용 덮어쓰기 적용) · `sections?: [overview, method, recovery, aftercare, timeline, emergency, disclosure, safety, checks, site_caution, dose, products, evidence, ops, market]` · `full?: false` |
| slim(기본) | 이름 · 키(무엇을 · 어디에 · 어떻게) · 동의어 · 표시 · 안전 묶음 요약(칸마다 상태 · fact id · 짧은 이름) · 쓰는 제품 id · 이름 · 허가 상태 |
| sections | 요청한 칸만 fact 원문으로. `full: true` 는 전 칸 |
| 제품 · 계열 id | 제품 → 그 제품이 쓰이는 단위 시술 id(G5) + 제품 속성 · 원문 · 덮어쓰기 부작용 / 계열 → 정의 · 근거 문장 · 단위 시술 id 목록 · 계열 안전 |
| 관계 | 싣지 않음(S2 — pair_check 로) |

카드 칸 ↔ 실버 원문(fact section):

| 칸 | 실버 |
|---|---|
| overview · method | `step8 safety.family_text[계열][「환자 설명 가이드(patient-education)」][]` 의 `simple_explanation` · `how_it_works` · `pain_level` · `common_concerns`(17계열) · `step8 evidence.statements[] field moa · effects`(class 그대로 · `patient{}`) · `units[].ops`. 단위 시술 · 제품마다 따로 쓴 개요 · 기전 문장은 실버에 없다(계열 수준만) → §3-6 보강 후보 |
| recovery | `family_text` 환자 설명 가이드의 `downtime` · `duration_simple` |
| aftercare | `family_text` 사후관리 3종 · `step5 extracted[] · taxonomy_products[] source_text.aftercare`(붙는 수준 그대로 — 제품 × 계열 · 단위 시술) |
| timeline | `safety.timelines[]`(G11 붙는 수준) |
| emergency · disclosure | `family_text` 「즉시 내원이 필요한 징후」 · 「응급(extracted.json safety.emergency)」 / 「필수 고지」 |
| safety | 부작용(G9 덮어쓴 값 + override_of) · 합병증(`safety.complications` 펼친 행) · PIH · 상태(G10) |
| checks | T5 결과 요약(조건 · grade3) |
| site_caution | `safety.site_caution[]` 펼친 행 |
| dose | `units[].dose_range_text` · `step5 dose_range[]` · `step4_attrs` |
| products | G5 결과 · `step1` 제품 이름 · 허가 상태 · 라인 품목 · `5_spec` |
| evidence | 근거 문장 · 출처(`cites`) |
| market | `units[].market[]` 원문(요청 때만 · 화면 표시 여부는 U-3 · 앱 몫) |

### 5-5. T4 pair_check — 같이 · 순서 · 간격 · 이전 시술

| 칸 | 값 |
|---|---|
| 입력 | `procedures: [unit_procedure id]`(2~6 · 같은 id 두 번 = 자기 쌍(재시술 간격) — §3-3 자기 쌍 규칙) · `prior?: {procedure: unit_procedure id, elapsed_days: int ≥ 0}` · `sub_condition?: {키: 값}`(예: `{"세션": "같은 날"}`) · `include_conditional?: false` |
| 경로 P-07 | 쌍 C(n,2) 마다 §3-3 앱 값 · 금기류(간격 금기 · 조합 금기 · 같은 날 불가 · 대체) 먼저 정렬 · 전역 행 |
| 경로 P-08 | (prior, 지금) 쌍의 앱 값으로 D-10 판정 · `C-PRIOR` 확인 조건이 있으면 같이 |
| 출력 | `pairs[]{a, b, value{first, days, open_high, same_day, by_sub_condition, options[], by_direction?, field_status, status}, prior_ok?: true\|false\|null, prior_basis?, alternatives[], claims[]{id, kind, text}, edges[]}` · `global[]` · `facts[]` · `must_show_flags` |
| sub_condition | 주면 그 조건 옵션만 · 안 주면 옵션 전부(「조건 모름」 포함) — 고르지 않음 |
| 쌍 방향 | `value.first` 의 a · b 는 응답 쌍의 a · b 기준으로 맞춰 냄 |

### 5-6. T5 check_conditions

| 칸 | 값 |
|---|---|
| 입력 | `id: unit_procedure\|product\|package id`(package = O-4 ledger 행이 붙은 패키지 · 그 밖 패키지는 빈 결과) · `conditions?: [check_condition id]` |
| 경로 P-09 | 단위 시술 × 조건 등급(§3-3 확인 조건) + 전역(target all 16) + 대기 기간(`wait_resolved` · 옵션 그대로) |
| 출력 | `checks[]{condition, name, grade3, scope: "unit\|product\|family\|global", resolved_id, from[], alternatives[]}` · `waits[]` · `not_condition[]`(그 계열 「상담 · 준비 · 고지」 원문 · 엣지 아님) · `facts[]` |
| 등급 | `grade3` 4값(금기 · 주의 · 확인만 · 확인만(고지)) 그대로 · 거르기 없음(G13 — 전 등급) |

### 5-7. T6 compare

| 칸 | 값 |
|---|---|
| 입력 | `procedures: [unit_procedure id]`(2~4) |
| 경로 P-06 | 키 칸 나란히(계열 · 하위 · 부위 · 기법) · ops · 회복 · 지속 fact · 안전 셈 → 같은 단위 시술이 든 비교 combo(`kind == 비교`)의 `members` 원문 → 대체(택 1) 관계 앱 값 |
| 출력 | `rows[]{field, values{id: …}}` · `source_comparisons[]{combo, members, text}` · `alternatives[]`(대체 관계) · 각 시술 안전 묶음 요약 · `facts[]` |

### 5-8. T7 combos — 추천 조합(② 메뉴 → 조합 · ③ 기본 응답 범위)

| 칸 | 값 |
|---|---|
| 입력 | 셋 중 하나 이상: `concern?: concern id` · `purpose?: purpose id` · `procedure?: unit_procedure id` · `menu?: str`(resolve 의 `menu:{라벨}` 후보 · 판단 ② · G18) / `include_sales_copy?: false` · `include_not_recommended?: false` |
| ② 메뉴 경로 | `menu` 가 오면 `combos[]` = `kind == 추천 패키지` 이고 `anchor.source_label == menu` 인 조합만(라벨 8 · 근거: 사이트 추천 화면 라벨 = `anchor.source_label` · J5). 고민 앵커로 넓히지 않는다(R12 앵커로 다른 라벨 패키지가 섞이지 않게). 쁘띠시술은 고민 앵커가 없어 이 경로로만 나옴(J5 유지) · 같은 라벨의 나머지 6종 조합은 없음(라벨은 추천 패키지에만 있음 — 실물) |
| 고민 · 목적 · 시술 경로 | 고민 id 로 물으면 지금대로 `anchors_combo`(R12 앵커 전부 · 고민 + 하위) · 목적 · 시술은 combo_component(G17)로 그 시술이 든 조합 · 패키지 `contains`. 이때도 ③ 으로 나눔 |
| ③ 기본 응답 범위 | 응답을 두 묶음으로: `combos[]` = `kind == 「고민 패키지(사이트 「추천 패키지」)」` 만(먼저) · `reference[]` = 나머지 6종(목적 레시피 · 비교 · 세션 조합(순서) · 연간 플랜 · 연령 플랜 · 중증도 조합)에 `role: "참고"` + `kind` 표시. 패키지(step6)는 `packages[]` 로 따로 |
| 칸 | 조합마다 `{id, kind, name, tier, anchor, components[]{field, family, units[], status, flag}, flags, facts}` — 영업 문구(`sales_copy`)는 `include_sales_copy` 때만 · 구성 단위 시술의 안전 묶음 요약 동봉(G13) |
| 정렬 | combos: tier 원천 순서 · 조합 id / reference: kind 고정 순서(위 열거 순) · 조합 id |

### 5-9. T8 neighbors — 범용 이웃 탐색

| 칸 | 값 |
|---|---|
| 입력 | `id: 정본 id` · `edge_kinds?: [kind]` · `direction?: out\|in\|both = both` · `depth?: int = 1` · `limit?: int = 50` · `include_conditional?: false` · `include_derived?: true`(펼친 행 포함) |
| 한도 | `depth ≤ 2` · `limit ≤ 50`(기본 50) · 넘으면 자르고 `truncated: true`(10-30 O-1 결정 = D-15 추천). 값은 설정(`GOLD_NEIGHBORS_MAX_DEPTH=2` · `GOLD_NEIGHBORS_MAX_LIMIT=50`) · 상한 넘는 요청은 4xx |
| 출력 | `nodes[]` · `edges[]`(표시 · 앱 값 포함) · `truncated: bool` · `counts_by_kind{}`(자르기 전 셈) |
| 안전 | 이웃에 시술이 나오면 안전 묶음 요약 동봉(G13) |

### 5-10. T9 vocab

| 칸 | 값 |
|---|---|
| 입력 | `kinds?: [concern, site, purpose, check_condition, technique, family, intent, menu]` |
| 출력 | 고민 트리 · 부위 트리 · 목적 · 확인 조건 · 기법 트리 · 계열 · 의도 12 · 메뉴 이름(G18 라벨 8 — `kind == 고민 패키지(사이트 「추천 패키지」)` 의 `anchor.source_label`) · 도구 입력 enum(sections · sub_condition 키) — Jev 슬롯 선택지(10-26) |

### 5-11. 응답 크기 · 속도 장치(D-14 · S1~S7)

| 장치 | 규칙 |
|---|---|
| slim 기본 | 카드 기본 slim · 원문은 sections · full 요청 때만 |
| 관계는 쌍에서만 | 카드 · recommend 에 관계 목록 없음 → pair_check |
| 홉 제한 | 정해 둔 경로(P-01~P-11)는 고정 홉 · neighbors 만 depth · limit · truncated |
| 빌드 때 펼침 | 요청 때 규칙 계산 없음 — 메모리 dict 조회만 |
| 근거 인용 | fact id + 원천(evidence_source) |
| 표시 전달 | 표시 12 를 행마다 그대로 + must_show_flags |

---

### 5-12. 평가용 원장 도구 3 — raw-mcp(골드 아님)

hub-evals(`reference/2026-10-30-hub-evals/README.md`)가 원장 · 골드를 같은 환경(Claude SDK 에 MCP 도구로)에서 재도록 원장을 그대로 읽는 범용 도구(10-30 「원장도 MCP 로」). **골드 그래프 · 시맨틱 사전 · resolve_rules · 실버 · 골드 규칙에 기대지 않는다.** 골드 도구 9 와 응답 꼴 · 표시 · 안전 동봉 규칙을 나누지 않는다(§5-0 은 적용 안 함).

| 칸 | 값 |
|---|---|
| 마운트 | 같은 허브 앱 `127.0.0.1:18005` 에 별도 마운트 `/procedure-hub/raw-mcp/mcp` — 골드 MCP 와 같은 전송(Streamable HTTP · stateless · JSON 응답) · 별도 MCP 서버 이름(`procedure-hub-raw`) |
| REST | 만들지 않는다(사용자 결정 「REST 출구는 선택」 — hub-evals 는 MCP 만 씀). 필요해지면 같은 코어에 `/procedure-hub/raw/*` 라우터만 더함 |
| 입력 원장 | env `PHUB_RAW_DIR`(로컬 기본값 = `/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-stg-2026-10-26` — 예시 env 에만) · 파일 21(아래) · DB 안 씀 · 서버 시작 때 메모리에 읽음 |
| 해시 가드 | 시작 때 파일 21 의 sha256 앞 16자를 `raw-manifest.json`(코드 레포 `backend/` · 파일 이름 · 바이트 · sha16 21행 · 비밀값 없음)과 대조 — 파일이 빠지거나 더 있거나 해시가 다르면 원장 MCP 를 마운트하지 않고 헬스에 사유를 냄(골드 도구는 영향 없음). 응답 머리 `raw: {dir_manifest_sha16, files: 21}` |
| 모듈 경계 | `app/modules/raw/` — `app.modules.gold` · 시맨틱 · 실버 파일을 import · 읽기 하지 않는다. 골드 모듈도 raw 를 import 하지 않는다(시험 §6-4 가드) |

원장 파일 21(10-30 실물 · `phub-stg-2026-10-26/` · 합 1,252,346 바이트): anatomy-danger-zones · combo-recipes · complications · consent-checklist · contraindications · extracted · literature-evidence · market-pricing · patient-education · pih-risk · post-procedure-timeline · pre-procedure-checklist · problem-combos · problem-packages · procedure-comparison · procedure-profiles · products · synergy · taxonomy(660,497 바이트 · `modality[17]` · `problem[14]`) · treatment-optimization · treatment-sequence(`.json`)

경로 문법(세 도구 공통): `{파일 이름(.json 뺌)}` 다음에 `.{키}` 또는 `[{번호}]` 또는 `["{키}"]`(키에 `.` · `[` · 공백이 있을 때). 예 `taxonomy.problem[3]` · `extracted.M9` · `products.botulinum_toxin`. 없는 경로 = 4xx(도메인 오류 문구)

| id | 도구 | 입력 | 출력 | 규칙 |
|---|---|---|---|---|
| R1 | `raw_list` | `file?: str`(없으면 21 전부) · `depth?: int = 2`(≤ 3) | `files[]{name, bytes, sha16, structure}` — `structure` = 키 구조 트리(키 · 값 종류 object/array/string/number/bool/null · 배열 길이 · 객체 키 수) depth 까지 · 배열은 첫 원소 구조만 대표로 | 값 본문은 안 냄 |
| R2 | `raw_get` | `path: str`(필수) · `offset?: int = 0`(배열 · 객체 원소 건너뛰기) · `max_bytes?: int`(≤ 설정 상한) | `{path, type, value, bytes_total, truncated, next_offset?}` — 값은 원문 JSON 그대로 | 크기 한도 = 설정 `RAW_GET_MAX_BYTES`(기본 20,000 바이트 — 골드 카드 full 최대 18.4KB 수준). 넘으면 배열 · 객체는 원소 단위로 앞에서부터 한도까지 + `truncated: true` · `next_offset` · 문자열 하나가 넘으면 앞부분 + `truncated` |
| R3 | `raw_search` | `query: str`(필수 · 1~100자) · `files?: [str]` · `limit?: int = 20`(≤ 100) · `snippet_chars?: int = 80`(≤ 200) | `{query_norm, total, truncated, hits[]{file, path, in: "value\|key", snippet}}` | 정규화 = **공백 지우기 · 소문자만**(질의 · 원문 둘 다 · 시맨틱 정규화 · fold · 괄호 지움 · 사전 안 씀). 문자열 값과 객체 키에서 부분 일치 · 순서 = 파일 이름 순 → 문서 순(결정론) · `snippet` = 일치 앞뒤 원문 그대로(정규화 전 글자) · `total` = 자르기 전 셈 |

- LLM 없음 · 결정론(같은 원장 · 같은 입력 → 같은 출력)
- 품질 측정(§6-1)과 완료 조건에 들어가지 않는다 — hub-evals 는 골드 완성 뒤 별도(10-30)

## 6. 품질 · E2E

### 6-1. 골드 위 품질 측정(완료 조건)

- 정답 세트 = `quality-eval-set.json`(문항 111 · 의도 11 · 슬롯 · 정답 · 채점 식) **그대로**. 문항 · 정답 · 채점 식을 고치지 않는다
- 측정 = `quality-eval.py` 에 골드 모드를 더해 돌린다: `--gold <base_url>` 이면 M1(질문 세트) · M2(말 → 노드)는 **로컬 서버 REST 도구 호출**로 답을 얻고, M3(엣지 표본) · M4(원천 안전 원문)는 **발행된 골드 빌드 내용**(DB 에서 내보낸 `gold-export.json` — 노드 · 엣지 · facts)에서 잰다. 실버 직접 읽기 경로(지금 판)는 그대로 둔다(대조용)
- 의도 → 도구: I-01 → T1 + T2(`cc` 슬롯을 문항 슬롯 `cc` 로 · **T1 결과 중 `candidates` 의 concern · site 만 쓴다 — `menu_candidates` 는 I-11 T7 만**) · I-02 · I-03 · I-04 · I-05 · I-10 → T1 + T3 · I-06 → T6 · I-07 · I-08 → T4(I-07 자기 쌍 문항은 같은 id 두 번 — 예 Q091) · I-09 → T1 + T5 · 확인 조건 노드가 안 잡히는 문항(예 Q101 「통증 민감」 — 원문은 `family_text.M9` 환자 설명 가이드 `pain_level`)은 T3 `sections=overview,ops` 로 · I-11 → T1 + T7 · M2 → T1
- I-11 채점은 T7 의 `combos[]`(판단 ③ 「추천 패키지」 먼저 묶음)로 — `reference[]` 는 채점에 안 넣는다(판단 ③ 이 정한 기본 응답 범위가 정답 범위). I-11 경로: 질의 말(문항 `concern_text`)이 라벨이면 T1 `menu_candidates` 의 menu 후보로 T7 `menu`(판단 ② · G18) · 아니면 고민 후보로 T7 `concern`. 실물 셈(이 스펙 작성 때 실버로): 라벨 경로 + 추천 패키지만 채점이면 Q106~Q111 6문항 계열 집합이 정답과 같음
- 목표(10-30 사용자 승인 · 계산 밖 = 의료진 질문 5문항 Q042 · Q075 · Q083 · Q084 · Q102):

| 지표 | 목표 | 지금(실버 · CC 슬롯 판) |
|---|---|---|
| 질문 세트 재현율(전체) | ≥ 0.95 | 0.991 |
| 질문 세트 정밀도(전체) | ≥ 0.95 | 0.984 |
| I-01 재현율 · 정밀도 | ≥ 0.95 · ≥ 0.95 | 1.0 · 1.0 |
| 문항 안전 누락 · 원천 안전 원문 누락(M4) | 0 · 0 | 0 · 0 |
| 말 → 노드 찾기 | ≥ 97% | 98.4% |
| 엣지 표본 오류율 | ≤ 1% | 0.5% |

- **완료 조건**: 골드 모드 6/6 **그리고** 지금 틀린 4문항 Q106 · Q108 · Q109 · Q110 이 「맞음」. 나머지 문항은 실버 판에서 맞던 것이 골드 판에서 틀리면 안 됨(문항별 대조표를 리포트에)
- 리포트 = `quality-report-gold.json` · `.md`(실버 판 리포트는 덮지 않음) · 머리에 빌드 해시 · 입력 해시 · 서버 주소 · 시드
- 결정론: 같은 빌드 · 같은 서버로 두 번 → 리포트 바이트 같음(시간 칸은 §6-3 속도 리포트로 분리)

### 6-2. 실물 호출

- 로컬 서버(`127.0.0.1:18005`) 기동 상태에서 REST 9 도구 각 1회 이상 · MCP 9 tool 각 1회 이상 실제 호출(같은 입력이면 REST 와 MCP 응답 JSON 이 같음 — 머리 `build` 칸 포함)
- 샘플 흐름(gold-research §1 의 3~10단계)을 실제 도구로 한 번 따라간 기록: 이마 주름 → 팔자 → 턱선 처짐 → 소프웨이브 카드(method · aftercare) → 팔자 필러 dose · products → 조합 A 쌍 확인. 원천에 없는 샘플 값(「2주 사우나」 · 볼루마 품목 · 「Sofwave」 단독)은 허브 응답에 안 나와야 하고 §3-6 보강 후보에 있어야 한다
- 원장 MCP(§5-12): `raw_list` · `raw_get`(`taxonomy.problem[3]` · 한도 넘는 경로 하나 → `truncated`) · `raw_search`(원장에 있는 낱말 하나 · 대소문자 · 공백만 다른 질의가 같은 결과) 실제 호출 각 1회 이상 · 헬스에 manifest 21/21
- 백엔드 커밋 뒤 서버 재시작 후 측정(옛 코드가 떠 있는 상태 측정 금지)

### 6-3. 속도 측정

- 측정만 — 통과 기준은 실측 보고 뒤 사용자가 정한다(10-30 O-2 결정): 문항 111 을 도구 호출로 바꾼 요청 묶음을 따뜻한 서버에 3회 → 도구별 p50 · p95 · 최대(ms, 서버 측 처리 시간 + 클라이언트 왕복 둘 다) · 응답 바이트 중앙 · 최대 · 서버 기동 시 메모리 적재 시간
- 산출 `gold-speed.json` · `.md`

### 6-4. 시험(코드 레포)

| 시험 | 무엇 |
|---|---|
| 빌드 가드 | §3-1 가드 열 · §3-3 · §3-5 를 실물 입력으로 · 일부러 깬 고정 입력(fixture)으로 실패하는지 |
| 결정론 | 같은 입력 두 번 빌드 → 빌드 해시 같음 |
| 도구 코어 | 도구마다 정해 둔 입력 → 기대 출력(실물 빌드에서 뽑은 값 · 가상 문장 없음) |
| REST ↔ MCP 같음 | 같은 입력 응답 JSON 같음 |
| 원장 도구 경계 | `app/modules/raw/` 가 `app.modules.gold` 를 import 하지 않음 · 골드 모듈이 raw 를 import 하지 않음(소스 import 검사 시험) · 원장 도구가 `$W`(실버 · 시맨틱) 경로를 열지 않음 |
| 원장 도구 | manifest 대조(빠진 파일 · 다른 해시 → 마운트 안 함) · 경로 문법 · 잘림 · 검색 정규화(공백 · 대소문자만 — 「쳐짐」 · 「처짐」은 다른 말) · 결정론 |
| 안전 동봉 | 시술이 나오는 모든 도구 응답에 안전 묶음 칸이 있음 |

---

## 7. 열린 것 · 결정된 것

열린 것: **없음**(O-1 ~ O-4 는 10-30 사용자 결정 「열린 것은 추천으로 가자」로 닫힘 — _RESUME §2 10-30 행).

| id | 무엇 | 결정(10-30) | 본문 |
|---|---|---|---|
| O-1 | neighbors 한도(D-15) | depth ≤ 2 · limit 50 · truncated | §5-9 |
| O-2 | 속도 통과 기준 | 실측 보고 뒤 사용자가 정함 — 이 작업은 측정 · 보고까지 | §6-3 |
| O-3 | Claude 계약 블록(D-16) | 응답에 `claude_contract{allowed_fact_ids, must_show_flags, rule}` 블록을 낸다 | §5-0 |
| O-4 | 확인 조건 ledger 대상 3행(원장 「넥큐레이션」) | 패키지 P6-03 에 붙인다 | §3-3 · §5-6 |

- U-2(허브 호출 주체) · U-3(시장가 표시)는 10-30 결정대로 앱 · 화면 설계 때 — 이 스펙의 열린 것 아님
- D-17(미라쥬 영역 대응 = 연결 층) · D-18(보강 후보 목록)은 10-30 경계 결정(「병원 상품 · 연결 층은 앱」 · 「허브에 없는 건 보강 후보 목록만」)과 같아 열린 것 아님 — §1-2 · §3-6
