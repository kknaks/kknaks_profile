---
type: spec
id: SPEC-005
title: "허브 골드 그래프 · 결정론 도구 — 실버 · 시맨틱 → 골드 빌드 · 저장 · REST/MCP 도구 9 · 골드 E2E"
status: draft
product: procedure-hub
feature: phub-recommend
version: 0.3.1
created_at: 2026-10-30
updated_at: 2026-10-31
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
    - "orchestration/work/phub-recommend/WORK-005.md"
  evals:
    - "reference/2026-10-30-hub-evals/build-out/fail-triage.md · fail-triage.json(B 239 · 오류 15 — v3 근거)"
    - "reference/2026-10-30-hub-evals/build-out/fail-triage-scripts/{replay,triage}.py(v3 끝 조건 대조 스크립트의 바탕)"
---

# SPEC-005 — 허브 골드 그래프 · 결정론 도구

> 검수 반영 2026-10-30(F-1 ~ F-5 · W-1 ~ W-9) — `review-spec005-report.md`
> 보강 2026-10-30(raw-mcp · O-1~O-4) — `_RESUME.md` §2 10-30 「원장도 MCP 로」 · 「SPEC-005 열린 것 O-1~O-4 추천대로」
> **v3.1 2026-10-31 — 검수 반영(`review-spec005-v3-report.md` F-1~F-8 · W-1~W-8 · 코디 결정 위임)** — 바뀐 곳: §2-2 family_text 문구 · §4-3 F-A ⑤ 연결 키 · F-C treats · F-D pih 칸 · W-7 열거 · §5-13 C2 · C3 종류 이름 · 의도 × 동봉 표(I-06 C7 · C14 · C11 / I-07 · I-09 C12 / I-11 C2) · §5-14 표(근거 열의 section 전부 묶음에) · §5-15 문턱 → V-6 · §6-5(분모 205 · 판정 = 새 export 로 gold_match 재실행 · 셈 규칙 · case3 201 · 「닫지 않는 행」 19 · 목표 = 조항이 닿는 행의 ≥ 90%) · §7 V-1 숫자 · V-6 · V-7
> **v3 2026-10-31 — 허브 응답 설계 수정(전달 문제 B 239건 + 오류 15건)** — `fail-triage.md`(정본) · `_RESUME.md` §2 10-31 「고칠 순서 1 허브 응답 설계」. v2(0.1.0 · 검수 PASS)는 `SPEC-005.v2.md` 로 보관. 바뀐 조항 = §0 · §3-0(v3 행) · §4-3(F-A~F-E) · §5-0 · §5-3~§5-9 · **§5-13 · §5-14 · §5-15(새)** · §6-1 · **§6-5(새)** · §7. A(골드에 없음 61)는 실버 9단계(다음 단계) — 이 스펙 밖

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
- **v3(응답 설계)**: 도구마다 `intent`(I-01~I-12)를 받아 ① 의도별 **섹션 기본 묶음**(§5-14 · B ① 53) ② 의도별 **고정 동봉**(§5-13 · B ⑤ 90 · ⑦ 20) 을 slim 원칙 안에서 같이 낸다 · 쌍 도구는 evidence 원문을 기본 포함하고 입력 1개 · 계열 · 제품도 받는다(§5-5 · §5-7 · B ④ 27) · full 전용 속성 중 건수 큰 것만 slim 으로(§5-15 · B ⑥ 18) · 어느 노드에도 안 붙던 fact 를 붙이고 섹션 매핑 구멍을 메운다(§4-3 F-A~F-E · B ② 16 · ⑧ 15) · check_conditions 가 계열 · 제품 id 를 받아 펼친다(§5-6 · 오류 15) · 끝 조건 = B 재인용률(분모 = 카드 도구 호출이 있던 B 205 · 조항이 닿는 186 의 ≥ 90%) · 응답 크기 중앙값 ≤ 현 ×2 · 품질 6/6 · 106/106 유지(§6-5)

| 절 | 내용 |
|---|---|
| §1 | 범위 · 경계 |
| §2 | 입력 계약(파일 · 해시 · 칸 경로 — 실물 대조) |
| §3 | 골드 빌드(G1~G18 · G1~G17 정정 반영 · 펼치기 · 거르기 · 안전 동봉 · resolved · gap · 결정론) |
| §4 | 저장(스키마 · 적재 방식) |
| §5 | 도구 9(입력 · 출력 · 후보 여럿 · 응답 크기 · 의도별 경로 ①②③) · §5-12 평가용 원장 도구 3(골드 아님) |
| §5-13 · §5-14 · §5-15 | **v3** 의도별 고정 동봉 · 의도 → 섹션 기본 묶음 · full 전용 속성의 slim 승격 |
| §6 | 품질 · E2E · **§6-5 v3 끝 조건(B 재인용률 · 크기 · 회귀)** |
| §7 | 열린 것 · 결정된 것(O-1~O-4 · **v3 아직 안 정한 것 V-1~V-7**) |

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

`safety.family_text` 칸 이름(실물 · 17계열의 합집합 13칸 · 17계열 모두에 있는 칸 9 — 「상담 · 준비 · 고지 · 조건 아닌 문장」 · 「critical_safety_facts」 · 「안전 원문」 은 일부 계열만 · v3.1 W-8): 필수 고지(consent mandatory_disclosures) · 즉시 내원이 필요한 징후(consent emergency_signs) · 환자 설명 가이드(patient-education) · 사후관리 3종(taxonomy modality extracted.aftercare · extracted.json aftercare · procedure-profiles aftercare) · 부작용 문장 common · uncommon · serious(근거 — 합병증 노드 아님) · 상담 · 준비 · 고지 · 조건 아닌 문장(16) · 응급(extracted.json safety.emergency · 2) · critical_safety_facts(anatomy · 1) · 안전 원문(규칙 행 · 쌍 없음 · 1). 카드 칸 대응은 §5-4.

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

**v3 — 구현이 이미 달라진 점을 본문에 반영(SPEC = 실물 · 2026-10-31)**. 출처 `WORK-003.md` §SPEC 과 다른 점 · 코드 레포 `backend/build-out/work003-report.md` D-1~D-10(코디 ask 합의 10-30). 아래 표의 「본문」 절이 v3 에서 그 값으로 고쳐졌다. (`cli-provider-report.md` 는 이 날 두 워크스페이스에서 찾지 못했다 — 브리프가 든 항목은 D-8~D-10 과 같아 그 셋으로 반영)

| # | v2 문구 | 실물(v3 본문) | 본문 |
|---|---|---|---|
| D-1 | T2 `concerns` 1+ · cc 범위 「같은 원천 문제(P)」 | `cc_roots?: [P{n}]` 선택 입력(고민 노드 없는 대분류 — 쁘띠시술 P1 · 기타 P14) · cc 나 site 가 있으면 concerns 0 허용 · cc_roots 없으면 P = concerns 의 대분류 | §5-3 |
| D-2 | G5 `rules.product_link` 전부 재계산 | 계열(주 · 보조) · 하위 일치 · guards · extra_stored 재계산 · **technique_compat 판정은 실버 `product_links[].technique_excluded` 값** · 제품마다 = inherited_candidates 가드 354/354 | §3-1 G5 |
| D-3 | `$W/quality-eval.py` 에 `--gold` 모드 | `$W` 는 읽기만 — 코드 레포 어댑터 `scripts/gold_quality_eval.py` 가 채점 식을 exec 로 빌림 · 리포트 `backend/build-out/quality-report-gold.*` | §6-1 |
| D-4 | slim 안전 칸 = 상태 · fact id · 짧은 이름 · T3 만 `sections` | **도구 9 모두 `sections`**(이름 = §4-3 fact section + `all` · T3 `full=true` = all) · 짧은 안전 요약 = 금기 조건 id(이름은 응답 머리 `names`) · 그 밖 등급 셈 · 금기류 엣지 id · 피함 고민 · gap 칸 · 원문 셈(`counts`) · 응답 머리 `more`(section 별 안 실은 원문 셈) | §5-0 · §5-4 |
| D-5 | claude_contract allowed = facts id 전부 | 그대로 · 머리 `names` · `emergency_signs`(계열마다 consent 응급 징후 문장)는 facts 밖 이름표 | §5-0 |
| D-6 | 카드 slim 에 쓰는 제품 id · 이름 · 허가 | 짧은 카드 = 쓰는 제품 **셈** · `sections=products` 면 목록 · 추천 조합 앵커는 짧은 카드에서 뺌 → **v3 §5-13 이 의도별로 되살림**(I-01 · I-10 · I-11) | §5-4 · §5-13 |
| D-7 | — | 측정 · E2E · 속도 `--gold inprocess`(TestClient · 포트 안 엶) | §6 |
| D-8 | resolve order 4단계(문서 = 코드) | 낱말 끝 **조사 떼기**(랑 · 이랑 · 하고 · 와 · 과 · 는 · 은 · 이 · 가 · 을 · 를 · 도 · 에 · 에서 · 으로 · 로 — 긴 것 먼저 · 끝 하나만 · 원 낱말 사전 일치 먼저 · 뗀 뒤 완전 일치일 때만 · `particle` 표시) — 질의 쪽만 · 골드 재빌드 없음 | §5-2 |
| D-9 | T4 · T6 · T7 `procedure` = unit_procedure id | **계열 · 제품 id 도 받아 단위 시술로 펼침**(`expanded` · 상한 pair 30쌍 · compare 8 단위 · 짧은 응답은 같은 값 쌍 묶음 `pairs[[a,b]…]`) | §5-5 · §5-7 · §5-8 |
| D-10 | T2 카드 전부 | `limit`(기본 10 · 1~200) · 넘는 카드 `more_cards` · `cards_total` | §5-3 |

### 3-1. 규칙 G1~G17

| id | 규칙 | 골드에서 하는 것 | 가드(빌드 실패) |
|---|---|---|---|
| G1 | 정본 id | 모든 노드 · 엣지 끝을 `ids.map` 으로 정본 id(`{kind}:{키}`)로 바꿔 싣는다. 단위 시술 · 제품 id 는 안정 키 | 맵에 없는 실버 id 가 엣지 끝에 있으면 실패 |
| G2 | 계열 → 단위 시술 펼치기(I1) | 관계 · 확인 조건 · 합병증 · 근거 문장 · 부작용 · 위험지대 · 피함의 **계열 끝**을 `key.family` 가 그 계열인 단위 시술 전부로 펼쳐 단위 시술 수준 행으로 싣는다. 행마다 `inherited_from`(계열 정본 id) | 펼친 합병증 행 수 = `safety.complications[].units_inherit` 길이 합(실물 285) |
| G3 | treats 「계열만」은 펼치지 않음 | `step7 edges[] target_kind == 계열만` 은 계열 엣지 그대로 + 표시(site_check · resolve_flag 값 그대로) | — |
| G4 | 하위 계열 · 기법 조건 끝(I2 · I3) | `endpoints.*.qualifier.sub_family` · `.technique` 끝은 같은 하위 · 같은 기법(또는 하위 기법) 단위 시술로. 키에 그 하위 없는 계열은 「candidates」 표시 | — |
| G5 | 제품 → 단위 시술(I4) | `step5 rules.product_link`(같은 계열 주 · 보조 · 하위 일치 · guards · extra_stored)를 다시 계산 · **technique_compat 판정만 실버 `product_links[].technique_excluded` 값을 읽는다**(v3 · D-2 — 4단계 장비 속성 판정 로직 재구현 안 함) | 결과가 `product_links[].inherited_candidates` 와 제품마다 같아야 함 · 저장 `units[].uses_product` 합(실물 44)과 같아야 함 |
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

**v3 — 붙지 않은 fact · 속성 → fact(F-A ~ F-E)**. 근거 = `fail-triage.md` §3 ⑧ 15 · ② 16 · ⑦ 20 · ⑥ 18(건수) · 부록 fact id. 원칙: 원문은 그대로(복사 · 요약 없음) · fact 는 하나 · **부착은 색인으로**(`gold_fact.attached_to jsonb` = 정본 id 목록 · 메모리 `facts_by_attach[(node, section)]`). owner 는 바꾸지 않는다(원천 수준 기록) · 도구는 owner 와 attached_to 둘 다로 찾는다.

| id | 무엇(실물 셈 · 2026-10-31 gold-export e9d30ace) | 붙이는 규칙(결정론 · 빌드 때) | 가드 |
|---|---|---|---|
| F-A | `step7 step8_notes[]` 245행(지금 owner `scope:all` · section evidence — 도구가 못 꺼냄 · B ⑧ 14건: Q086 · Q115 · Q147 · Q148 · Q159 · Q198 · Q227 → `step8_notes[124 · 138~140 · 190 · 191 · 193 · 229]`) | 행의 `where` 로 앵커를 정한다 — ① `P{n}-{m}`(13) → `combo:RC-PC-P{n}-{m}` ② `P{n} {CC}`(152) → 7단계 treats 엣지 중 `root == P{n}` 이고 `ccs ∋ CC` 인 엣지의 `to_units` 단위 시술 전부(+ 그 CC 가 `anchor` 에 든 추천 조합) ③ `where == combos[].name`(중증도 조합 · 세션 조합 44) → 그 combo ④ 후속 간격 `R{n}`(28) → `combo:RC-RE-R{n}` ⑤ 규칙 8(`combination_rules` 제목) → **연결 키 = `step8_notes[i].text == avoid_edges[j].text` 이고 두 행의 `source` 가 같음**(실물 1건 — `step8_notes[45]` ↔ `AV8-001` · W-2) 인 `concern_avoid` 의 고민 · 대상 단위 시술 · 나머지 7은 `scope:all` 유지(닫히는 B 행 없음 · 추측으로 더 잇지 않음). 단위 시술에 붙는 행은 section `evidence` · meta `{where, kind, cc}` | 245행 전부 앵커 종류가 정해짐(①~⑤ 합 = 13 + 152 + 44 + 28 + 8 = 245 · ⑤ 중 concern_avoid 연결 1 · scope:all 유지 7 · 미해결 0) · ②의 CC 는 7단계 `edges[].ccs` 집합에 있어야 함(실물 152/152) |
| F-B | 8단계 `attrs[]` 56행 중 owner 가 노드가 아닌 것 — `CC P{n}:{CC} 속성(원소 1개 — 쌍 아님)` 21(B ⑧ 1건 Q198 `attrs[25]`) · `7단계 추천 조합(목적 레시피) 후속 일정 원문` 28 · `단위 시술 U5-124,U5-125,U5-126 재시술(터치업) 간격 원문` 4 · `7단계 추천 조합 RC-OP-Hair-* 속성` 2 | `source_index` 로 — `P{n}:{CC}#k` → F-A ② 와 같은 규칙(treats 엣지 to_units) · `R{n}#k` → `combo:RC-RE-R{n}` · `U5-…` 열거 → 그 단위 시술들 · `RC-OP-…` → 그 combo. section `evidence` | 56행 전부 owner 또는 attached_to 가 노드 1+ |
| F-C | 엣지 속성에만 있는 원문(B ⑦ 20건): `site_caution` 엣지 `attrs.row.spec{key_warning, risk, safe_zone, dose_range, target_muscle}` · `vessels[].danger` · `clinical_pearls[]` · `safe_injection_depth`(4건 — Q002 · Q018 · Q036 · Q043) / 비교 조합 `members[].attrs_text{best_for, downtime, duration, limitations, onset, pain, pih_risk, cost_range, mechanism_simple, asian_skin_note(2)}` · `anchor.subtitle`(combo_component 11건 · 열거는 보기 · 규칙은 잎 전부 — W-7) / `product_family` 엣지 `attrs.row.basis`(3건) / treats 엣지 `attrs.row.evidence.role`(1건 Q118 — treats 에 `row.claims` 는 0건 · `R8-0321#reason` 은 이미 procedure_relation evidence fact · F-8) / `concern_avoid` ↔ `step8_notes[45]`(1건 · F-A ⑤) | 잎 값마다 fact 를 만든다 — id `{엣지 id}#{section}#{칸 경로}` · owner = 엣지 id · attached_to = 엣지 양끝 노드(site_caution → 계열 + 부위 + `units_affected` 단위 시술 · 비교 조합 members → 그 멤버 단위 시술(`members[].units`) + combo · product_family → 제품 · treats `evidence.role` → to_units). section: site_caution 칸 → `site_caution` · members attrs_text → `evidence`(downtime · duration · onset 은 `recovery` 로도 색인) · basis → `overview` · treats `evidence.role` → `evidence` | site_caution 22엣지 × spec 잎 전부 fact 있음 · 비교 조합 9 × members attrs_text 잎 전부 |
| F-D | 노드 속성(full 전용)으로만 있던 원문(B ⑥ 18 중 fact 가 없던 것): 단위 시술 `silver.pih[]{attach, condition, fitzpatrick_note, pih_rate, pih_risk, source, target}` 잎(실물 32행 · `prevention` 은 이 칸에 없음 — step8 `safety.pih[]` 의 `pih[k]` fact 본문에 이미 있음 · 9건 중 7 — 지금 `pih[k]` fact 는 묶음 1개) · `sources[].detail`(1) · 조합 `effect{expectedResult, clinicalRationale, riskBenefit}`(목적 레시피는 `effect{expectedResults, repeatCycle}` 7 — W-7) · `price` · `evidence_notes[]` · `caveats[]` · `rationale` · `maintenance` · `sessions` · `subtitle` · `follow_up` · `avoid_text` · `annual_focus`(combo 8 + ⑤ combo 27 의 같은 칸) — **열거는 보기 · 규칙은 「잎 전부」** · 계열 `silver.definition`(1) | 잎 값마다 fact — id `{노드 정본 id}#{section}#{칸 경로}` · owner = 그 노드 · section: pih 잎 → `safety.pih` · sources detail → `overview` · 조합 effect · rationale · caveats · evidence_notes · subtitle → `evidence` · price → `market` · sessions · maintenance · follow_up · annual_focus → `timeline` · avoid_text → `checks` · definition → `overview` | 조합 79 × 위 칸 잎 전부 · 단위 시술 pih 잎 전부 |
| F-E | 섹션 매핑 구멍(B ② 16건 — 부록 fact id): 계열 카드가 **단위 시술 수준 fact 를 못 냄**(Q078 · Q219 `unit_procedure:U5-091#ops#ops.needsAnesthesia` · `…U5-090#ops#ops.prepNotes` · Q110 `pih[1]`(U5-023) · Q136 `fractional-co2#phases[4].normal[3]`(U5-028)) · 계열 카드 `site_caution` 이 SC 엣지 fact 를 안 냄(Q013 `SC-cheek-M1` · Q041 `SC-temple-M1`) · compare 가 `overview` · `method` 를 안 냄(Q015 · Q016 · Q042 · Q057 · Q069 · Q073 · Q209 `family:M*#overview#family_text[환자 설명 가이드…]` · `#method#…how_it_works`) · check_conditions 가 `emergency` 요청을 무시(Q036 `botox#phases[3].emergency[1]`) · recommend 가 `checks` 요청을 무시(Q001 `family:M9#checks#family_text[상담 · 준비 · 고지…][1]` · `K8-0303`) · recommend `overview`(Q103) | 매핑 규칙(§5-4 카드 칸 표 · §5-14): ① 계열 카드 `ops · dose · market · timeline · aftercare · safety.pih · site_caution · products` = 그 계열 단위 시술 facts 를 **단위 시술별로 묶어**(`by_unit{unit: [fact id]}` · 단위 시술 상한 §5-13 표) ② 계열 · 단위 카드 `site_caution` = `facts_by_owner((family, site_caution))` ∪ SC 엣지 fact(F-C · 단위는 부위 일치 · 계열은 전부) ∪ `family_text` critical_safety_facts ③ **`sections` 는 도구 9 공통으로 「응답에 나온 시술 노드(단위 · 제품 · 계열)마다 그 section 의 카드 facts」 를 뜻한다**(T4 · T5 · T6 · T2 · T7 · T8 도 같은 매핑 함수 · 지금은 T3 만 전 section) | §6-5 재실행에서 ② 16건 fact id 가 응답에 있음 |

- 빌드 가드에 더한다: F-A ~ F-D 셈(행 수 · 잎 수)을 `gold_build.counts.v3_facts` 에 기록 · F-A 미해결 0 · F-B owner 없음 0. 빌드 해시가 바뀐다(새 fact) → 발행 · 서버 재시작(WORK-005)
- `family:None` owner fact 40행(실물 — `taxonomy_products[M1-P-10…].source_text.aftercare` 가 계열 코드 없이 들어감)은 빌드 버그 — owner 를 그 taxonomy 제품(`product:` 정본 id)으로 바로잡는다(실버 수정 아님 · 읽는 칸 `step5 taxonomy_products[].product`)

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
- **응답 크기**(D-14 · S1 · S2 · v3): 카드는 기본 slim · 원문은 `sections`(명시 ∪ **의도 기본 묶음 §5-14**)의 칸만 · 단위 시술 관계 목록은 카드에 싣지 않고 `pair_check` 로만 — 단 **의도별 고정 동봉(§5-13)** 은 요약 꼴(id · 이름 · 등급 · 값 · fact id · 상한 안의 원문)로 늘 같이 낸다
- **facts**: 응답에 나온 원문은 `facts[]{id, text, section, flags, state, source}` 로 모아 내고 카드 · 행은 fact id 로 가리킨다
- **`intent?: I-01 … I-12`(v3 · 도구 9 공통 입력)**: 의도를 받으면 §5-13 동봉 묶음과 §5-14 섹션 기본 묶음을 그 의도로 고른다. **없으면 도구의 기본 의도**(표 §5-1 의도 열의 첫 값 — T2 I-01 · T3 I-02 · T4 I-07 · T5 I-09 · T6 I-06 · T7 I-11 · T1 · T8 · T9 = 없음 → G13 안전 요약만)로 같은 일을 한다 — Jev · Claude 가 안 골라도 기본이 붙는다(B ① 53 · case3 Jev 가 상위 4 밖으로 자르거나(8) 안 고른(10) 건). 모르는 값 = 4xx
- **`sections` 합집합(v3)**: 요청 `sections` 가 오면 **의도 기본 묶음 ∪ 요청** · `sections=none` 은 기본 묶음도 끈다(실험 대조용 · 안전 요약 · 동봉 요약은 그대로) · `sections=all` 은 전부. 응답 머리 `sections_used[]`(실제 적용된 집합) · `intent_used`
- **동봉 · 섹션은 「응답에 나온 시술 노드」 단위**(v3): 단위 시술 · 제품 · 계열이 응답 어디에 나오든(카드 · 쌍 · 비교 · 조합 구성 · 이웃) 그 노드마다 같은 매핑 함수(§5-4 카드 칸 표 + F-E)로 facts 를 찾는다 — 도구마다 따로 매핑하지 않는다(B ② 의 compare · check_conditions · recommend 구멍)

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
- **v3**: 의도 열의 첫 값이 그 도구의 기본 의도(§5-0 `intent` 없을 때). **I-07 · I-08 경로는 쌍 도구(T4) 필수** — 시술이 하나만 잡혀도 T4 를 부른다(§5-5 「입력 1개」 모드 · B ④ 「pair_check/compare 안 부름」 4건 · 「다른 쌍」 14건 중 한쪽만 잡힌 건). I-06 은 T6 필수 · 둘 다 §5-13 동봉을 낸다

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
| 입력 | `concerns?: [concern id]`(cc 나 site 가 있으면 0 허용 · D-1) · `site?: site id` · `cc?: str`(원천 CC 이름 · 골드 판단 ① · R28) · `cc_roots?: [P{n}]`(고민 노드 없는 대분류만 — 쁘띠시술 P1 · 기타 P14 · 없으면 P = concerns 의 대분류 · D-1) · `limit?: int = 10`(1~200 · 넘는 카드는 `more_cards` id 목록 + `cards_total` · D-10) · `include_conditional?: false` · `include_not_recommended?: false` · `intent?` · `sections?`(§5-0) |
| 경로 P-01 | ① 고민 + 하위 고민(child_of) — 조상 · 자손이 같이 오면 자손만 · 고민에 부위 1개면 그 부위 · 부위만 오면 그 부위 고민 → ② **cc 가 오면**: 같은 원천 문제(P) 안에서 `ccs[]` 에 그 CC 가 든 treats 엣지만(출발이 고민 · 목적 · 앵커 없음이어도 CC 로 찾음). cc 가 없거나 원천 CC 가 아니면 고민 노드 treats 엣지 전부 → ③ 부위 층 거르기(`site_rules.climb` — 부위 · 하위 → 상위(묶음 통과) → 영역 「전체」 노드 · `site_rules.site_free` 「해당 없음」 · 「병변 단위」 단위 시술은 통과) · `layer` 「상위」(얼굴 전체 층) 엣지도 같이 내되 `layer` 표시(U-1 = ②) → ④ 부위 없이 고민만이면 기본 영역 = 얼굴 + 다른 영역 시술이 있으면 `other_regions` 표시(D-12) → ⑤ 단위 시술마다 G13 안전 묶음 · 쓰는 제품(G5 · recommendable 만) · 추천 조합 앵커 id |
| 출력 | `areas[]{site, name, layer: "부위\|상위\|영역 전체", concerns[], card_ids[]}` · `cards[]`(slim 카드 §5-4 + `why[]{edge, from, source, layer, flags}` + **I-01 동봉 §5-13**) · `cc_roots_used` · `by_cc` · `more_cards?` · `cards_total?` · `family_only[]{family, reason(site_check · resolve_flag 값), flags}` · `facts[]` · `must_show_flags` · `excluded_counts` |
| 정렬 | 결정론 — `layer`(부위 → 상위) · 엣지 원천 순서 · 단위 시술 id |

### 5-4. T3 procedure_card — 시술 카드

| 칸 | 값 |
|---|---|
| 입력 | `id: unit_procedure\|product\|family id` · `product?: product id`(단위 시술 카드에 특정 제품 원문 · 부작용 덮어쓰기 적용) · `sections?: [§4-3 fact section 이름 · all · none]`(D-4 — `safety` 는 `safety.side_effects` · `safety.complications` · `safety.pih` 셋) · `full?: false`(= `sections=all`) · `intent?`(기본 I-02) |
| slim(기본 · D-4 · D-6) | 이름 · 키(무엇을 · 어디에 · 어떻게) · 표시 · 안전 요약(금기 조건 id · 등급 셈 · 금기류 엣지 id · 피함 · gap · 원문 셈 `counts`) · 쓰는 제품 **셈**(목록은 `sections=products` 또는 §5-13 I-10) · **v3: §5-15 승격 칸**(단위 시술 `pih` 요약 · 계열 `definition` 1문장은 이미 있음) + **§5-13 의도 동봉** |
| sections | 의도 기본 묶음(§5-14) ∪ 요청 칸을 fact 원문으로 · 응답 머리 `more` = 안 실은 section 별 셈 |
| 제품 · 계열 id | 제품 → 그 제품이 쓰이는 단위 시술 id(G5) + 제품 속성 · 원문 · 덮어쓰기 부작용 / 계열 → 정의 · 근거 문장 · 단위 시술 id 목록 · 계열 안전. **v3(F-E ①)**: 계열 · 제품 카드의 단위 시술 수준 section(`ops · dose · market · timeline · aftercare · safety.pih · site_caution · products`)은 `sections[s].by_unit{unit id: [fact id]}` 로 단위 시술별 묶음 · 단위 시술 수 상한 = §5-13 표 「계열 펼침」(넘으면 `truncated` · `units_total`) |
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
| 입력 | `procedures: [unit_procedure\|family\|product id]`(**1~6** · v3: 1개 = 「관계 목록」 모드 · 같은 id 두 번 = 자기 쌍(재시술 간격) — §3-3 자기 쌍 규칙 · 계열 · 제품은 단위 시술로 펼침 D-9 · 펼친 쌍 상한 30 `pairs_total` · `truncated`) · `prior?: {procedure: id, elapsed_days: int ≥ 0}` · `sub_condition?: {키: 값}`(예: `{"세션": "같은 날"}`) · `include_conditional?: false` · `intent?`(기본 I-07) · `sections?` |
| 경로 P-07 | 쌍 C(n,2) 마다 §3-3 앱 값 · 금기류(간격 금기 · 조합 금기 · 같은 날 불가 · 대체) 먼저 정렬 · 전역 행. **v3 입력 1개**(B ④ 「다른 쌍」 — 질문의 둘째 시술이 안 잡힌 Q017 · Q018 · Q019 · Q084 · Q112 · Q139 꼴): 그 시술(펼친 단위 시술)에 닿는 `procedure_relation` 전부를 `relations[]{edge, kinds, other{kind, id, name}, value 요약(first · days · same_day · status), claims[] id}` 로 — 금기류 먼저 · 상한 §5-13 · 되묻기 재료(상대 시술 후보 = `other`) |
| 경로 P-08 | (prior, 지금) 쌍의 앱 값으로 D-10 판정 · `C-PRIOR` 확인 조건이 있으면 같이 |
| **같은 계열 자기 쌍(v3)** | 계열 하나가 오거나 두 입력이 같은 계열로 펼쳐져 같은 단위 시술이 만나면 그 쌍은 건너뛴다(지금 규칙) · 대신 **`self_pair[]`** = 그 계열의 `self_pair == true` 엣지(실물 4 — E8-0059 M2↔M2 · E8-0214 · E8-0225 · E8-0228)의 `resolved` 를 한 번 낸다(재시술 간격 질문 · 같은 id 두 번과 같은 값) · 없으면 `self_pair: []` |
| 출력 | `pairs[]{a, b, inputs?, value{first, days, open_high, same_day, by_sub_condition, options[], by_direction?, field_status, status}, prior_ok?: true\|false\|null, prior_basis?, alternatives, claims[]{id, kind, text, flags}, edges[], relation}` · `relations[]?`(입력 1개) · `self_pair[]?` · `expanded[]?` · `global[]` · `prior_checks[]` · `safety{}` · `facts[]` · `must_show_flags`. **v3 evidence 기본**(B ④ 「쌍 맞음 · evidence 안 요청」 8건 · 「요청했는데도 안 실림」 1건 Q097): 짧은 응답에서도 쌍마다 `claims[]` 는 **원문 포함**(`text` · `kind`) — 금기류 주장 먼저 · 쌍당 상한 §5-13(넘으면 id 만 + `claims_total`) · **조건부 주장은 `include_conditional` 과 무관하게 id + `conditional` 표시로 늘 내고** 원문은 상한 안에서 · 같은 값 쌍 묶음(D-9)은 claims 까지 같으면 묶음 |
| sub_condition | 주면 그 조건 옵션만 · 안 주면 옵션 전부(「조건 모름」 포함) — 고르지 않음 |
| 쌍 방향 | `value.first` 의 a · b 는 응답 쌍의 a · b 기준으로 맞춰 냄 |

### 5-6. T5 check_conditions

| 칸 | 값 |
|---|---|
| 입력 | `id: unit_procedure\|product\|package\|**family** id`(package = O-4 ledger 행이 붙은 패키지 · 그 밖 패키지는 빈 결과) · `conditions?: [check_condition id]` · `intent?`(기본 I-09) · `sections?` |
| **계열 · 제품 펼침(v3 · 오류 15)** | 계열 id → 그 계열 단위 시술 전부 · 제품 id → 쓰는 단위 시술(G5 저장 + 상속 후보) — `expand_units` 와 **같은 규칙**(resolve 펼침 · D-9). 지금은 계열이 400(`id: family:M8 는 family — 받는 종류 …` · 15건 = Q008 · Q021 · Q070 · Q074 · Q096 · Q099 · Q108 · Q120 · Q138 · Q141 · Q150 · Q161 · Q168 · Q169 · Q202 · 계열 M8 9 · M15 2 · M4 · M9 · M11 · M12 각 1). 펼친 결과는 **합쳐서** 낸다: 조건마다 가장 엄격한 등급 하나(금기 > 주의 > 확인만 > 확인만(고지)) + `by_unit{condition: {grade3: [unit id]}}`(등급이 단위 시술마다 갈리면 그대로 보임 · 접지 않음) · `expanded{input, kind, units}` · 단위 시술 상한 §5-13 표(넘으면 `truncated`) · 제품 id 일 때 product 키 행(7)은 지금처럼 제품 자체 행으로 |
| 경로 P-09 | 단위 시술 × 조건 등급(§3-3 확인 조건) + 전역(target all 16) + 대기 기간(`wait_resolved` · 옵션 그대로) |
| 출력 | `checks[]{condition, name, grade3, scope: "unit\|product\|family\|global", resolved_id, from[], alternatives, facts[], by_unit?}` · `global[]` · `waits[]` · `not_condition`(짧은 응답 = 셈 · `sections=checks` 면 원문) · `claims[]`(그 시술 대상 확인 조건 주장 · 조건부 표시) · `safety{}` · `expanded?` · `facts[]`. **v3**: `sections` 는 §5-0 공통 규칙대로 적용된다(Q036 `emergency` 요청 무시 → 응답에 나온 시술의 emergency facts) |
| 등급 | `grade3` 4값(금기 · 주의 · 확인만 · 확인만(고지)) 그대로 · 거르기 없음(G13 — 전 등급) |

### 5-7. T6 compare

| 칸 | 값 |
|---|---|
| 입력 | `procedures: [unit_procedure\|family\|product id]`(2~4 · 계열 · 제품은 펼침 D-9 · 펼친 단위 시술 상한 8 — 입력마다 돌아가며 · `compared[]` · `truncated`) · `intent?`(기본 I-06) · `sections?` |
| 경로 P-06 | 키 칸 나란히(계열 · 하위 · 부위 · 기법) · ops · 회복 · 지속 fact · 안전 셈 → 같은 단위 시술이 든 비교 combo(`kind == 비교`)의 `members` 원문 → 대체(택 1) 관계 앱 값. **v3**: ① 차이 필드에 `overview` · `method` 를 더한다(B ② compare 7건 — 계열 환자 설명 가이드 `simple_explanation` · `how_it_works` · `common_concerns`) — 기본 묶음 §5-14 I-06 ② `source_comparisons[]` 는 짧은 응답에서도 **비교 대상 멤버의 `attrs_text` 원문**(F-C fact id + text)을 낸다 — 비교 대상이 아닌 멤버는 id · 이름만(B ⑦ 10건 · ⑥ 2건 · ⑤ combo 속성 중 비교 조합 분) ③ 두 시술 사이 `procedure_relation` 이 있으면 종류 무관하게 `relations[]`(값 요약 + claims 원문 상한 §5-13)로 — 대체(택 1)만 내던 것을 넓힘(B ④ 「compare 다른 쌍」 Q134 2건) |
| 출력 | `rows[]{field, values{id: …}}`(field = family · sub_family · site · technique · **overview · method** · ops · recovery · dose · safety_counts) · `source_comparisons[]{combo, name, members[]{unit, text, attrs_text facts}}` · `relations[]`(v3 · 대체 포함) · `alternatives[]` · `expanded?` · `compared?` · 각 시술 안전 묶음 요약 · **§5-13 I-06 동봉** · `facts[]` |

### 5-8. T7 combos — 추천 조합(② 메뉴 → 조합 · ③ 기본 응답 범위)

| 칸 | 값 |
|---|---|
| 입력 | 넷 중 하나 이상: `concern?: concern id` · `purpose?: purpose id` · `procedure?: unit_procedure\|family\|product id`(펼침 D-9) · `menu?: str`(resolve 의 `menu:{라벨}` 후보 · 판단 ② · G18) / `include_sales_copy?: false` · `include_not_recommended?: false` · `intent?`(기본 I-11) · `sections?` |
| ② 메뉴 경로 | `menu` 가 오면 `combos[]` = `kind == 추천 패키지` 이고 `anchor.source_label == menu` 인 조합만(라벨 8 · 근거: 사이트 추천 화면 라벨 = `anchor.source_label` · J5). 고민 앵커로 넓히지 않는다(R12 앵커로 다른 라벨 패키지가 섞이지 않게). 쁘띠시술은 고민 앵커가 없어 이 경로로만 나옴(J5 유지) · 같은 라벨의 나머지 6종 조합은 없음(라벨은 추천 패키지에만 있음 — 실물) |
| 고민 · 목적 · 시술 경로 | 고민 id 로 물으면 지금대로 `anchors_combo`(R12 앵커 전부 · 고민 + 하위) · 목적 · 시술은 combo_component(G17)로 그 시술이 든 조합 · 패키지 `contains`. 이때도 ③ 으로 나눔 |
| ③ 기본 응답 범위 | 응답을 두 묶음으로: `combos[]` = `kind == 「고민 패키지(사이트 「추천 패키지」)」` 만(먼저) · `reference[]` = 나머지 6종(목적 레시피 · 비교 · 세션 조합(순서) · 연간 플랜 · 연령 플랜 · 중증도 조합)에 `role: "참고"` + `kind` 표시. 패키지(step6)는 `packages[]` 로 따로 |
| 칸 | 조합마다 `{id, kind, name, tier, anchor, components[]{field, family, units[], status, flag}, flags, facts}` — 영업 문구(`sales_copy`)는 `include_sales_copy` 때만 · 구성 단위 시술의 안전 묶음 요약 동봉(G13). **v3(§5-15)**: 짧은 조합 카드에 `price`(원문) · `effect{expectedResult, clinicalRationale, riskBenefit}` fact id + 원문 · `evidence_notes` · `caveats` · `rationale` · `sessions` · `maintenance` 는 fact id(원문은 §5-14 I-11 기본 묶음 evidence) · F-A 로 붙은 step8_notes evidence fact id |
| 정렬 | combos: tier 원천 순서 · 조합 id / reference: kind 고정 순서(위 열거 순) · 조합 id |

### 5-9. T8 neighbors — 범용 이웃 탐색

| 칸 | 값 |
|---|---|
| 입력 | `id: 정본 id` · `edge_kinds?: [kind]` · `direction?: out\|in\|both = both` · `depth?: int = 1` · `limit?: int = 50` · `include_conditional?: false` · `include_derived?: true`(펼친 행 포함) |
| 한도 | `depth ≤ 2` · `limit ≤ 50`(기본 50) · 넘으면 자르고 `truncated: true`(10-30 O-1 결정 = D-15 추천). 값은 설정(`GOLD_NEIGHBORS_MAX_DEPTH=2` · `GOLD_NEIGHBORS_MAX_LIMIT=50`) · 상한 넘는 요청은 4xx |
| 출력 | `nodes[]` · `edges[]`(표시 · 앱 값 포함) · `truncated: bool` · `counts_by_kind{}`(자르기 전 셈) |
| 안전 | 이웃에 시술이 나오면 안전 묶음 요약 동봉(G13) · `intent?` · `sections?`(§5-0 공통 — 이웃 시술 노드에 적용) |

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

### 5-13. 의도별 고정 동봉(v3 · B ⑤ 90 · ⑦ 20 · ④ 중 「안 부름 · 다른 쌍」)

recommend · procedure_card · resolve 뒤 경로 · pair_check · compare · check_conditions · combos · neighbors 가 돌려주는 **시술 노드(단위 시술 · 제품 · 계열)마다 1-hop 이웃을 의도에 따라 고정으로** 같이 낸다. LLM 이 고르지 않아도 붙는다(결정론 · 빌드 때 모아 둔 dict 조회 · S4). 꼴은 **요약 + id**(slim 원칙) — 원문은 상한 안의 fact 만 `facts[]` 에 싣고 나머지는 fact id 로 가리킨다(`more` 셈). 카드 안 칸 이름 `companion{…}`.

동봉 묶음(요약 꼴 · 상한은 시술 노드 하나 기준):

| id | 묶음 | 꼴(요약) | 상한 | 원문(facts) | 근거(B) |
|---|---|---|---|---|---|
| C1 | 부위 위험(site_caution) | 그 시술 부위(부위 트리 상위 · 계열 SC 의 `units_affected` 포함)에 닿는 `site_caution` 엣지 `{id, site, danger_level, key_warning: fact id, risk: fact id}` · 금기 아님 · 위험 단계 큰 순 | 3 | `spec.key_warning` 1 · `risk` 1(F-C) | ⑦ 4 · ⑤ family site_caution 1 · ① 1 · ② 2 |
| C2 | 확인 조건(checks) | 그 시술의 `requires_check` 전부(단위 수준 펼친 종류 `requires_check_unit` 1,600 · 제품 `requires_check_product` · 전역 포함 — W-1) `{condition, name, grade3, resolved_id, claims: [fact id]}` — 지금은 금기 id + 등급 셈뿐 → **주의 · 확인만 도 이름 · id 로** | 전부(이름) | 금기 · 주의 주장 원문 ≤ 4(금기 먼저) | ⑤ check_condition 25(1-hop 20 · 경로 5) |
| C3 | 금기류 관계(relations) | 그 시술에 닿는 관계(저장 `procedure_relation` 230 을 단위 시술 쌍으로 펼친 `procedure_pair` 4,687 — 단위 시술은 쌍 색인 `g.pair`/UnitSets 로 닿는 것 · W-1) 중 간격 금기 · 조합 금기 · 같은 날 불가 · 대체(택 1) `{edge, kinds, other{id, kind, name}, first, days, same_day, status, claims: [fact id]}` | 6 | 쌍 도구에서만(C9) | ④ 「안 부름」 4 · 「다른 쌍」 14 · ⑦ 1 |
| C4 | 쓰는 제품(products) | `{id, name, license_status, recommendable}`(D-6 가 뺀 목록을 의도별로 되살림) | 10 | 없음(원문은 `sections=products` · I-10) | ⑤ product 10(aftercare 4 · side_effects 4 · products 1 · 속성 1) |
| C5 | 계열(family) | `{id, name, definition: fact id}` + 계열 안전 상태 2 | 1(+ also_families) | `definition` 1(F-D) | ⑤ family 13(1-hop 4 · 경로 9) · ⑥ 1 |
| C6 | 합병증(complications) | `{id, name, severity, fact}` 전부(지금 items 와 같음 · 계열 카드 · compare · pair 에도) | 전부 | 없음(I-04 기본 묶음) | ⑤ complication 4 |
| C7 | 추천 조합(combos) | 그 시술이 구성에 든 조합 `{id, kind, name, tier, price: fact id, effect: {expectedResult, clinicalRationale, riskBenefit}: fact id}` — 추천 패키지 먼저(판단 ③) | 5 | `price` · `effect.expectedResult` ≤ 2 조합(F-D) | ⑤ combo 27 · ⑥ combo 8 |
| C8 | 패키지(packages) | `contains` 로 그 시술이 든 step6 패키지 `{id, name, kind}` · `package_evidence` fact id | 5 | 없음 | ⑤ package 2 |
| C9 | 쌍 근거(pair evidence) | 쌍마다 `claims[]{id, kind, text, flags}` **원문** · 금기류 주장 먼저 | 쌍당 4(넘으면 id + `claims_total`) | 4/쌍 | ④ 「evidence 안 요청」 8 · 「안 실림」 1 |
| C10 | 비교 멤버 원문 | 비교 조합 `members[].attrs_text` 잎 fact(F-C) — 비교 대상 시술이 멤버인 것만 `{unit, field, fact id, text}` | 멤버당 잎 전부(≤ 9) | 전부 | ⑦ 10 · ⑥ 2 · ⑤ 비교 조합 분 |
| C11 | 경과 타임라인 요약 | `{timeline id, phases[]{name, fact ids}}` — 이름만 | 1 타임라인 | 없음(`sections=timeline`) | ⑤ unit timeline 3 · 경로 1 |
| C12 | PIH 요약 | `{pih_risk, pih_rate, fitzpatrick_note: fact id, source: fact id}`(F-D 잎) · 상태 3값 | 1 | `fitzpatrick_note` 1 | ⑥ unit 9 중 7 |
| C13 | 상담 문장(not_condition) | 계열 `family_text` 「상담 · 준비 · 고지 · 조건 아닌 문장」 fact id | 5 | 5(I-09 만) | ② 1(Q001 K8-0303 · M9 checks) |
| C14 | 붙은 근거 메모(evidence refs) | F-A · F-B 로 그 시술 · 조합 · CC 에 붙은 step8_notes · CC 속성 fact id `{id, kind(meta), where}` | 5 | 원문 ≤ 2(「시너지(쌍 주장)」 먼저) | ⑧ 15 |

의도 × 동봉(I-01~I-12):

| 의도 | 도구 | 동봉 묶음(고정 · 순서대로) | 근거 B 건수(⑤ · ⑦ · ④ · ⑥) |
|---|---|---|---|
| I-01 고민 → 추천 | T2 | 카드마다 C1 · C2 · C3 · C4(상한 5) · C7 · C14 | ⑤ 9 · ⑦ 3 · ④ 1 |
| I-02 시술 설명 | T3 | C5 · C4 · C6 · C2 · C11 | ⑤ 7 |
| I-03 주의 · 사후관리 | T3 | C11 · C1 · C2 · C4(aftercare 원문은 §5-14) | ⑤ 8 |
| I-04 부작용 · 합병증 | T3 | C6 · C1 · C12 · C4 · C2 | ⑤ 13(그중 combo 1 · unit market 1 은 닫지 않음 — §6-5 표) |
| I-05 회복 · 효과 기간 | T3 | C11 · C2 · C12 · C7 · C14 | ⑤ 14 |
| I-06 비교 | T6 | 비교 시술마다 C5 · C12 · C6 · C2 · **C7 · C11 · C14**(v3.1 — ⑤/⑥ combo 8 · Q106 timeline 2 · Q198 ⑧ 2) + 응답에 C10 · 쌍마다 C3(종류 무관 · `relations[]`) | ⑤ 12 · ⑥ 10 · ④ 2 · ⑧ 2 |
| I-07 같이 · 순서 · 간격 | T4 | 쌍마다 C9 · 입력 1개면 C3(`relations[]`) · 시술마다 C2(C-PRIOR 포함) · C1 · C7 · **C12**(v3.1 · Q201) | ④ 21 · ⑤ 11 · ⑥ 1 |
| I-08 이전 시술 뒤 가능? | T4 | I-07 과 같음 + `prior_checks` | ④ 1 · ⑤ 1 · ① 1 |
| I-09 확인 조건 | T5 | C2(원문 상한 4) · C13 · C1 · C6 · **C12**(v3.1 · Q150) | ⑤ 11 · ⑦ 4 · ⑥ 1 |
| I-10 용량 · 회차 · 제품 | T3 | C4(상한 10 · `5_spec` 포함) · C7 · C12 · C14 | ⑤ 2 · ⑥ 1 |
| I-11 추천 조합 | T7 | 조합마다 C7 속성(price · effect) · C14 · C8 · 구성 시술마다 C3 · **C2**(v3.1 · Q025 C-NMJ) | ⑤ 2 · ⑥ 3 · ④ 2 |
| I-12 가격 | — | 허브 도구 없음(연결 층) — 동봉 없음 · §7 V-1 | — |
| (의도 없음 · T1 · T8 · T9) | — | G13 안전 요약만(지금과 같음) | — |

- **계열 펼침 상한**(계열 · 제품 id 가 와서 단위 시술로 펼칠 때 · 동봉 · 섹션 `by_unit` 공통): pair_check 30쌍(D-9) · compare 8 단위(D-9) · check_conditions 20 단위 · 계열 카드 `by_unit` 12 단위 — 넘으면 `truncated` · `units_total` · 나머지는 id 목록. 값은 설정(`GOLD_EXPAND_MAX_UNITS=20` · `GOLD_CARD_BY_UNIT_MAX=12`)
- **크기 상한(응답 전체 · §6-5 로 잼)**: 기본 응답(의도 동봉 + §5-14 기본 묶음 · 요청 `sections` 없음)의 **도구별 바이트 중앙값 ≤ 2 × 현 중앙값**(현 = `runs/runs.jsonl` 10-30 전체 실행 · case2 도구 호출 중앙 · 표는 §6-5) · recommend 는 브리프 기준 7.2KB → **≤ 14.4KB**. 넘으면 동봉 상한(위 표 · 설정)을 줄인다 — 동봉 종류를 빼지 않는다
- 동봉은 **의도의 정의**다(gold-research 의도 12 · 경로 P-01~P-11 의 「→ 단위 시술마다 G13 안전 묶음 · 쓰는 제품 · 추천 조합 앵커」를 의도별로 고정한 것). 새 의도를 더하려면 이 표에 행을 더한다 — 코드 상수 `INTENTS` 와 1:1(시험)

### 5-14. 의도 → 섹션 기본 묶음(v3 · B ① 53 · ② 16)

허브가 `intent` 를 받으면(없으면 도구 기본 의도 — §5-0) 아래 section 을 **기본으로** 붙인다. `sections=` 명시가 오면 합집합 · `none` 이면 끔. section 이름은 §4-3. 적용 대상 = 응답에 나온 시술 노드 전부(§5-0 「시술 노드 단위」 · F-E ③).

| 의도 | 기본 section | 근거(B ① + ② 의 빠진 section · 건) |
|---|---|---|
| I-01 | (없음 — 카드 slim + §5-13 동봉) · `site_caution` 은 C1 으로 | ① site_caution 1 · ② checks 1 · overview 1 |
| I-02 | `overview` · `method` · `ops` | ① overview 3 · ops 1 · ② overview 1 · ops 2 |
| I-03 | `aftercare` · `recovery` · `timeline` · `emergency` · `disclosure` · `overview`(v3.1) | ① aftercare 3 · disclosure 2 · overview 1 · ② safety.pih 1 · timeline 1 |
| I-04 | `safety.side_effects` · `safety.complications` · `safety.pih` · `emergency` · `disclosure` · `overview` · `timeline`(v3.1) | ① disclosure 5 · overview 5 · emergency 2 · timeline 1 · side_effects 1 · ② site_caution 1 · emergency 1 (management 는 A 그룹 · §7 V-4) |
| I-05 | `recovery` · `timeline` · `aftercare` · `overview` · `disclosure` · `ops`(v3.1) | ① aftercare 3 · recovery 3 · overview 1 · disclosure 1 · timeline 1 · ops 1 · ② ops 1 |
| I-06 | compare 차이 필드 = `overview` · `method` · `recovery` · `ops` · `dose`(§5-7 rows) · 비교 시술마다 `safety.pih` · `checks` · `disclosure`(v3.1) · `evidence` 는 조합(C14) 범위만 — 단위 시술 evidence 아님 | ① recovery 2 · overview 1 · checks 1 · disclosure 1 · method 1 · pih 1 · ② overview 6 · method 1 · ⑧ 2 |
| I-07 · I-08 | 쌍 `evidence`(C9 원문) · 시술 `checks`(C-PRIOR) · I-08 은 `safety.side_effects`(v3.1 · Q020) | ① checks 1 · side_effects 1 · ② site_caution 1(C1) · ④ evidence 9 |
| I-09 | `checks` · `site_caution` · `aftercare` · `overview`(v3.1 — 확인 조건 노드 없는 질문의 `overview` · `ops` 경로 §6-1 과 겹침) | ① aftercare 2 · overview 2 · ⑤ checks 25 · ⑦ basis→overview 1 |
| I-10 | `dose` · `products` · `market` · `overview` · `disclosure`(v3.1) | ① overview 2 · disclosure 2 · market 1 |
| I-11 | `products` · `market` · 조합 `evidence`(F-A · F-D) | ⑥ 3 · ⑧ 1 |
| I-12 | — | — |

- 기본 묶음이 커지면 크기 상한(§5-13)이 먼저다 — section 을 빼지 않고 **section 안 fact 수 상한**(`GOLD_SECTION_FACTS_MAX=8` · 넘으면 id 만 + `more`)으로 줄인다. 계열 수준 원문(환자 설명 가이드 등)은 응답에 한 번만(같은 계열 카드가 여럿이어도 facts 는 id 로 중복 제거 — 지금 envelope 와 같음)
- Jev · Claude 가 고른 `sections` 는 그대로 더해진다(합집합) — 「Jev 가 상위 4 밖으로 자름」(case3 8건) · 「noul < 0.5 로 안 고름」(10건)은 **18건 모두** 그 의도의 기본 묶음 안에 있다(v3.1 — Q020 · Q040 · Q042 · Q058 · Q098 · Q104 · Q170 이 위 표 보강으로 들어옴). 앱 쪽 규칙(상위 4 · 0.5)은 SPEC-006 몫 · 여기서 바꾸지 않는다(§7 V-5)

### 5-15. full 전용 속성 → slim 승격(v3 · B ⑥ 18)

건수 기준(fail-triage ⑥ + ⑤ 의 같은 칸)으로 정한다 — **5건 이상이면 slim 에 요약 + fact id · 그 미만은 section(원문)으로만**(문턱 5 는 작성자 기준 · 결정표에 없음 → §7 V-6 · W-3).

| 속성(실물 칸) | 건 | 결정 | 어디로 |
|---|---|---|---|
| 조합 `effect{expectedResult, clinicalRationale, riskBenefit}` · `price` · `evidence_notes` · `caveats` · `rationale` · `sessions` · `maintenance` | ⑥ 8 + ⑤ 27 = 35 | **slim 승격**: 짧은 조합 카드(T7 · C7)에 `price` 원문 · `effect.*` fact id(+ expectedResult 원문 ≤ 2 조합) · 나머지 fact id | §5-8 · C7 · F-D |
| 단위 시술 `pih[]{fitzpatrick_note, source, pih_rate, pih_risk, prevention}` | ⑥ 7(+ ② 1) | **slim 승격**: 안전 요약 `pih` 칸을 셈 → `{pih_risk, pih_rate, note: fact id}` 로(C12) · 원문은 `safety.pih` | §5-4 · C12 · F-D |
| 비교 조합 `members[].attrs_text` · `anchor.subtitle` | ⑥ 2 + ⑦ 11 = 13 | **compare 응답에서만 원문**(C10) — 카드 slim 에는 안 올림(비교 맥락 밖이라) | §5-7 · F-C |
| 계열 `definition`(계열 overview 대용) | ⑥ 1 + ⑤ family overview 4 | 이미 짧은 계열 카드에 있음 → **C5 로 다른 도구 응답에도**(compare · pair · recommend family_only) | C5 · F-D |
| 단위 시술 `sources[].detail` · `schedule` · `members text` | ⑥ 2 | section(`overview`)으로만 | F-D |
| 조합 `sales_copy` | ⑤ 1(Q238) | 바꾸지 않음 — `include_sales_copy` 때만(G12 영업 문구) | — |

---

## 6. 품질 · E2E

### 6-1. 골드 위 품질 측정(완료 조건)

- 정답 세트 = `quality-eval-set.json`(문항 111 · 의도 11 · 슬롯 · 정답 · 채점 식) **그대로**. 문항 · 정답 · 채점 식을 고치지 않는다
- 측정 = 코드 레포 어댑터 `scripts/gold_quality_eval.py`(D-3 · `$W/quality-eval.py` 는 읽기만 — 채점 식을 exec 로 빌림) `--gold <base_url>|inprocess`: M1(질문 세트) · M2(말 → 노드)는 **도구 호출**로 답을 얻고, M3(엣지 표본) · M4(원천 안전 원문)는 **발행된 골드 빌드 내용**(`gold-export.json` — 노드 · 엣지 · facts)에서 잰다. 실버 직접 읽기 경로(지금 판)는 그대로 둔다(대조용). **v3**: 어댑터는 문항 의도를 `intent` 로 넘긴다(기본 묶음 · 동봉이 붙은 응답으로 채점 — 회귀 0 확인)
- 의도 → 도구: I-01 → T1 + T2(`cc` 슬롯을 문항 슬롯 `cc` 로 · **T1 결과 중 `candidates` 의 concern · site 만 쓴다 — `menu_candidates` 는 I-11 T7 만**) · I-02 · I-03 · I-04 · I-05 · I-10 → T1 + T3 · I-06 → T6(**필수** · 계열 · 제품도 받음) · I-07 · I-08 → T4(**필수** · 시술이 하나만 잡혀도 부름 — 「관계 목록」 모드 §5-5 · I-07 자기 쌍 문항은 같은 id 두 번 — 예 Q091) · I-09 → T1 + T5(계열 · 제품 id 는 펼침 §5-6) · 확인 조건 노드가 안 잡히는 문항(예 Q101 「통증 민감」 — 원문은 `family_text.M9` 환자 설명 가이드 `pain_level`)은 T3 `sections=overview,ops` 로 · I-11 → T1 + T7 · M2 → T1. 모든 호출에 `intent`(v3)
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
| **v3 동봉 · 섹션**(WORK-005) | `intent` 12 값 × 도구 → §5-13 묶음 칸이 있고 상한을 안 넘음 · `intent` 없음 = 도구 기본 의도 · 모르는 값 4xx · `sections` 합집합 · `none` · `sections_used` · `intent_used` · 도구 9 공통 section 매핑(T4 · T5 · T6 · T7 에 `sections=emergency` 등이 시술 노드마다 적용) · 계열 카드 `by_unit` 상한 · `INTENTS` 상수 = §5-13 표 행 |
| **v3 facts**(F-A~F-E) | step8_notes 245 앵커 ①~⑤ 셈 · 미해결 0 · attrs 56 owner/attached 1+ · site_caution spec 잎 fact 22엣지 · 비교 조합 members 잎 fact 9조합 · 조합 effect/price fact 79 · pih 잎 fact · `family:None` 0 · 빌드 두 번 해시 같음 |
| **v3 쌍 · 펼침** | pair_check 1개 입력 → `relations[]` · 계열 하나 → `self_pair[]` 4엣지 값 · claims 원문 기본(상한 4 · conditional 표시) · compare `overview · method` rows · `source_comparisons[].members[].attrs_text` · check_conditions family id 6종(M8 · M15 · M4 · M9 · M11 · M12) 200 + `by_unit` 등급 갈림 보임 · 제품 id |
| **v3 재인용 대조** | `recheck.py` 가 B 239 행 · 실패 174문항분 호출을 읽어 결정론으로 판정 · 두 번 같음 · **판정 규칙 동일성**: recheck 의 `norm` · 포함 · fact id 규칙으로 `fail-triage.json` 320행을 옛 export 로 재분류하면 cls · sub 가 320/320 같음(F-6 · triage.py 는 수정 · import 하지 않음) |

### 6-5. v3 끝 조건(측정 · 결정론)

B 239 건은 「골드엔 있는데 허브 응답에 없음」이다 — 끝 조건은 **허브 응답**(LLM 답 아님)에 그 인용이 들어가는지로 잰다. 대조 스크립트는 `fail-triage-scripts/triage.py` 와 **같은 정규화 · 같은 판정**(소문자 · 공백 · 기호 제거 · 골드 쪽 8자 이상 포함 · fact id 일치)을 쓴다. 산출 = `reference/2026-10-30-hub-evals/build-out/recheck/recheck-report.md` · `.json` · 스크립트 `fail-triage-scripts/recheck.py`(WORK-005 WP-0).

| 항목 | 재는 법 | 통과 |
|---|---|---|
| **B 재인용률** | 실패 174문항의 호출을 **같은 입력으로 다시 보낸다**(전체 replay 유일 호출 755 중 실패 174문항분 — case2 는 trace 의 도구 호출 전부 · case3 는 `trace.hub` 경로 1번 · W-6) + 행의 `jev_intent` 를 `intent` 로(「?」면 없이). **판정(v3.1 · F-3)**: recheck 가 **새 gold-export(v3 빌드)** 로 `gold_match`(triage 와 같은 규칙 — 정규화 · 포함 · 8자)를 행마다 다시 돌려 `gold_hits` 를 갱신한 뒤, B 행이 「닫힘」 = 그 문항의 재실행 응답(도구 호출 전부 · `facts[].id` · 동봉의 fact id · 본문 전체) 안에 **갱신된 gold_hits 의 fact id 하나** 또는 정규화 인용이 있음. 옛 export(e9d30ace)와 새 export 의 빌드 해시 둘 다 리포트 머리에 · WP-0 기준선만 옛 export | **분모 = 카드 도구(T2~T8) 호출이 있던 B 행 205**(239 − 허브 안 부름 17 − resolve · vocab 만 17 · 코디 10-31). **목표 = 조항이 닿는 행(186)의 ≥ 90%**(= 168+) · 분모 205 기준 비율(상한 186/205 = 90.7%)과 239 기준 비율은 **보고**(§7 V-7 · 사용자 확인 자리) · 묶음 ①~⑧ · 의도별 표 · 「닫지 않는 행」 19 는 따로 셈 |
| **오류 15** | 같은 재실행에서 `GET /procedures/family:M*/checks` 15건 | 400 → 200 · 재실행 오류 0 |
| **응답 크기** | 재실행 호출 묶음의 **기본 응답**(요청 `sections` 없는 호출)을 도구별 바이트 중앙값으로 · 요청 sections 있는 호출은 따로 | 도구별 중앙값 ≤ 2 × 현 중앙값(아래 표 「case2 오류 제외」 열 — 셈 규칙 아래) · recommend ≤ 14.4KB · p95 는 보고만 |
| **품질 유지** | `gold_quality_eval.py`(intent 포함) | 6/6 · 106/106 · Q106 · Q108~110 맞음 · 회귀 0 |
| **결정론** | 재실행 · 대조 두 번 | 리포트 바이트 같음(시간 칸 분리) |
| **시험** | §6-4 + v3 시험(WORK-005 WP 마다) | 전부 통과 · ruff |

현 중앙값(기준 · `runs/runs.jsonl` 10-30 전체 실행 239문항 · 바이트 · `statistics.median`). **셈 규칙(v3.1 · F-5)**: case2 = `cases.case2.trace.tool_calls[]` 중 `is_error` 가 아닌 것의 `output_bytes`(전부 749 · 오류 87 = check_conditions 58 · procedure_card 15 · recommend 7 · vocab 5 · pair_check 2 → **662**) · case3 = `cases.case3.trace.hub.tool` 이 있는 run 의 `result_bytes`(**201** · 15건 400 포함 · 허브 경로 없는 run 38 제외) · 「sections 없음」 = case2 오류 제외 중 `input.sections` 가 비어 있는 호출(기본 응답 기준):

| 도구 | case2 오류 제외 n / 중앙 | case2 sections 없음 n / 중앙 | case3 n / 중앙 | v3 상한(case2 오류 제외 ×2) |
|---|---|---|---|---|
| recommend | 58 / 7,262 | 47 / 6,567 | 18 / 8,171 | **14,524**(브리프 7.2KB ×2 = 14.4KB) |
| procedure_card | 154 / 17,180(요청 sections 포함) | 16 / 1,447 | 125 / 26,325(Jev sections ≤ 4) | 34,360 — 기본 응답은 「sections 없음」 열(1,447)과 따로 대조 |
| pair_check | 22 / 7,200 | 23 / 7,151 | 29 / 6,882 | 14,400 |
| check_conditions | 28 / 24,206 | 10 / 115(오류 응답 셈) | 5 / 21,977 | 48,412 |
| compare | 14 / 7,997 | 6 / 7,268 | 21 / 6,146 | 15,994 |
| combos | 4 / 9,537 | 4 / 9,537 | 3 / 7,288 | 19,074 |
| neighbors | 9 / 6,544 | 7 / 5,633 | — | 13,088 |
| resolve | 364 / 1,059 | 364 / 1,059 | (경로 안) | 2,118 |
| vocab | 9 / 6,314 | 14 / 5,501(오류 포함) | — | 12,628 |
| 합 | 662 | — | 201 | — |

**닫지 않는 행(v3.1 · 분모 205 안 · 19행)** — 조항이 닿지 않음을 명시한다(재인용률 분자에 안 들어감 · 리포트에 같은 표로):

| 사유 | 행 | 문항 · 케이스 | 왜 안 닫나 |
|---|---|---|---|
| C10(비교 멤버 원문)은 compare 에서만(§5-15 결정 · W-4) | 10 | Q117 c2 · Q119 c2 · Q121 c2 · Q149 c3 ×2 · Q156 c2 · Q156 c3 ×2 · Q192 c3 · Q234 c3 | 비교 조합 members 원문을 카드 · 쌍 · 추천 slim 에 올리지 않기로 함(비교 맥락 밖) |
| 조항 없음(F-1 (c)) | 3 | Q123 c3(concern:P8-2 이름) · Q228 c2(product `1_identity.basis`) · Q118 c2(treats `evidence.role` — F-C 로 fact 는 생기나 I-06 compare 동봉 밖) | 고민 이름 · 제품 정체 근거는 동봉 대상이 아님 · treats role 은 추천 why 에만 |
| I-04 · I-09 에 C7 없음 | 2 | Q050 c3 · Q138 c2 | 부작용 · 확인 조건 의도에 조합 속성을 붙이지 않음(코디 결정 목록 밖 · 크기) |
| 1-hop 기타(동봉 종류 밖) | 4 | Q068 c2(unit market) · Q070 c2(다른 단위 시술 side_effects) · Q082 c3(package evidence) · Q084 c3(product products) | 시장가 · 다른 시술의 부작용 · 패키지 근거는 어느 의도 동봉에도 없음 |

분모 밖(참고): 허브 안 부름 17(문항 14 · case3 13 + case2 Q205) · resolve · vocab 만 호출 17(case2 Q015 · Q028 · Q082 · Q105 · Q113 ×2 · Q115 · Q122 · Q129 ×2 · Q135 · Q136 · Q162 ×2 · Q192 · Q211 · Q231 — T1 은 G13 요약만 · 동봉 · 섹션이 붙을 시술 노드가 없음).

- 허브 도구를 아예 안 부른 B 17건(문항 14 — case3 Q066 · Q101 · Q118 · Q122 · Q130 · Q164 · Q166 · Q178 · Q193 · Q197 · Q203 · Q204 · Q238 + case2 Q205 · 되묻기 · I-12 가격 · 필수 슬롯 없음)과 resolve · vocab 만 부른 17건은 허브 응답에 시술 노드가 없어 재인용률 분모에서 뺀다(코디 10-31) — 앱(SPEC-006) 몫 · §7 V-1
- A 61 · C 6 · 미분류 14 는 이 끝 조건 밖(A = 실버 9단계 · C = 사용자 10-31 「프롬프트 문제 아님으로 둠」)

---

## 7. 열린 것 · 결정된 것

v2 까지 열린 것: **없음**(O-1 ~ O-4 는 10-30 사용자 결정 「열린 것은 추천으로 가자」로 닫힘 — _RESUME §2 10-30 행).

**v3 아직 안 정한 것**(추측으로 메우지 않음 · 본문은 「추천 기본값」으로 써 두고 여기에 표시):

| id | 무엇 | 추천(본문에 쓴 값) | 누가 |
|---|---|---|---|
| V-1 | 허브를 아예 안 부른 B 17건(문항 14) · resolve · vocab 만 부른 17건은 허브 스펙으로 못 닫는다 — 분모(205)에서 빼고 앱(SPEC-006)으로 넘기는가(코디 10-31 「분모 = 카드 도구 호출이 있던 B」 로 진행) | 분모 205 · 239 기준도 같이 보고(§6-5) · I-12 는 허브 도구 없음 유지 | 사용자 |
| V-2 | `intent` 가 없을 때 — 도구 기본 의도의 묶음을 붙이는가(case2 Claude 호출도 커짐) · 아니면 G13 요약만 | 도구 기본 의도(§5-0) | 사용자 |
| V-3 | 크기 상한의 기준 — 브리프 「7.2KB ×2」(recommend) 하나로 전 도구를 재는가 · 도구별 현 중앙 ×2 인가 · 동봉 상한 숫자(§5-13 표) | 도구별 ×2 + recommend 14.4KB · 상한 숫자는 §5-13 표 값으로 시작해 §6-5 측정 뒤 조정 | 사용자 |
| V-4 | I-04 「management」(합병증 관리 · 예방 · A 그룹 `complications.management/prevention`)는 지금 골드에 section 이 없다 — 9단계가 section 이름(`safety.management`?)을 정할 때 §4-3 · §5-14 I-04 에 더한다 | v3 에선 안 넣음 | 9단계 스펙 |
| V-5 | 앱(SPEC-006) 쪽 — Jev 가 `intent` 를 허브에 넘길지 · Jev section 상위 4 · noul 0.5 규칙을 그대로 둘지(기본 묶음이 덮으므로 둬도 됨) · 필수 슬롯 없을 때 되묻기 대신 T4 「관계 목록」을 쓸지 | 허브는 받기만 · 앱 변경은 SPEC-006 v2 | 사용자 · SPEC-006 |
| V-6 | §5-15 slim 승격 문턱 「5건 이상」 — 결정표 · 브리프에 없는 작성자 기준(W-3) | 5건으로 진행 · 측정 뒤 바꿀 수 있음 | 사용자 |
| V-7 | §6-5 재인용률 목표의 분모 — 「조항이 닿는 행 186 의 ≥ 90%」(F-4 · 코디 10-31) 로 재고, 분모 205 기준(상한 90.7%) · 239 기준은 보고만. 어느 숫자를 끝 조건으로 볼지 | 조항이 닿는 행 기준 | 사용자 |

| id | 무엇 | 결정(10-30) | 본문 |
|---|---|---|---|
| O-1 | neighbors 한도(D-15) | depth ≤ 2 · limit 50 · truncated | §5-9 |
| O-2 | 속도 통과 기준 | 실측 보고 뒤 사용자가 정함 — 이 작업은 측정 · 보고까지 | §6-3 |
| O-3 | Claude 계약 블록(D-16) | 응답에 `claude_contract{allowed_fact_ids, must_show_flags, rule}` 블록을 낸다 | §5-0 |
| O-4 | 확인 조건 ledger 대상 3행(원장 「넥큐레이션」) | 패키지 P6-03 에 붙인다 | §3-3 · §5-6 |

- v3 에서 **결정으로 쓴 것**(결정표 안 · 브리프 지시): 허브에 LLM 없음 · 결정론 · 병원 독립 · slim 원칙(D-14) 유지 · 안전 늘 동봉(G13) · 충돌 = resolved 하나(T5 펼침의 「가장 엄격 하나 + by_unit」 도 D-13b 와 같은 방향) · 실버 · 시맨틱 수정 없음(F-A~F-E 는 골드 빌드 규칙 · A 그룹은 9단계)
- U-2(허브 호출 주체) · U-3(시장가 표시)는 10-30 결정대로 앱 · 화면 설계 때 — 이 스펙의 열린 것 아님
- D-17(미라쥬 영역 대응 = 연결 층) · D-18(보강 후보 목록)은 10-30 경계 결정(「병원 상품 · 연결 층은 앱」 · 「허브에 없는 건 보강 후보 목록만」)과 같아 열린 것 아님 — §1-2 · §3-6
