# 레코드 스키마 — step5-decisions.json · step5-units.json + 실제 행

경로: `orchestration/work/phub-recommend/`. 사람이 고치는 곳은 **`step5-decisions.json` 뿐**이다. `step5-units.json` · `.md` · `step5-origin-questions.md` 는 `step5-apply.py` 산출(손으로 고치지 않음).
실제 행은 2026-10-29 재검수 v3 PASS 판에서 그대로 옮겼다.

## 1. step5-decisions.json

| 칸 | 무엇 |
|---|---|
| `source.path` | 원천 폴더(지금 `/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-stg-2026-10-26`) — `step5-apply.py --source` 로 덮어씀 |
| `canon` | 앞 단계 정본 파일 이름(step1 ~ step4 · source_map) — 읽기만 |
| `special_sites` | 특수 부위 「해당 없음」 · 「병변 단위」 와 근거 |
| `name_rules` | `family_term` · `sub_term`(「계열\|하위」) · `technique_term` · `medium_term` |
| `key_rule` | 키 규칙 한 줄(J1 안 C) |
| `units[]` | **단위 시술 키** — §1-1 |
| `ledger[]` | **원장 항목 521 행선지** — §1-2 |
| `market[]` | 시장가 122 — 이름 · `kind`(시술 1회 · 6단계 패키지 · 계열 밖) · `units` · `role` · `product` · `grade` · `spec` · `sessions` · `category_conflict` · `fgroup` · `decided_by` (+ `origin_question` · `staff_question`) |
| `problem_P1[]` | 쁘띠시술 메뉴 17 — `id` · `name` · `dest` · `units` · `role` |
| `product_link_rule` | 저장 · 상속 규칙 — `stored` · `inherit` · `guards[]` · `extra_stored[]` · `technique_compat`(`requires[]` · `family_evidence[]` · `product_evidence[]` · `product_evidence_excluded[]` …) — `inheritance-rules.md` |
| `extracted_rule` · `route_rule` · `pih_not_applicable` · `anesthesia_dict` | 붙는 것 규칙 |
| `pih[]` · `step4_attrs[]` · `dose_range[]` · `taxonomy_products[]` | 원천 행마다 붙는 곳 |
| `handoffs` | 앞 단계가 넘긴 것 — `step1_moved_to` · `step2_deferred` · `step3_to5` · `step4_handoffs` · `step4_expressions` · `map_fields` |

### 1-1. units[] 한 줄

| 칸 | 값 |
|---|---|
| `id` | `U5-NNN` — 새 키는 다음 번호 |
| `key` | `{family, sub_family, ingredient, ingredient_of?, site, technique}` — `key-rules.md` §2 |
| `name` | 이름 규칙 C1 ~ C3 |
| `site_basis` | 「원천 이름」 · 「기본값 — …」 · 「규칙 — …」 · 「F3 — …」 |
| `attrs` | 키 밖 속성(예 `svf`) |
| `notes` | 사람용 문장 — 다음 단계가 읽을 값은 여기 두지 않는다 |
| `evidence_level` | null · 「약」 · 「중」 |
| `decided_by` | 결정 행(J1 · U7 · F3 · step5-fix3 …) |

```json
{"id": "U5-133", "key": {"family": "M16", "sub_family": null, "ingredient": "미상", "ingredient_of": "셀디톡스수액", "site": "해당 없음", "technique": "K01b"},
 "name": "셀디톡스 수액(성분 미상)", "site_basis": "규칙 — DEC-003 OQ-306 처리(10-27) 「수액은 부위 해당 없음 + 투여 경로」",
 "attrs": {}, "notes": ["성분 「미상」 그대로(U7 · 추정 금지) — 원천 질문"], "evidence_level": null, "decided_by": "U7"}
```

```json
{"id": "U5-021", "key": {"family": "M6", "sub_family": null, "ingredient": null, "site": "얼굴 전체", "technique": "K01"},
 "name": "얼굴 전체 지방이식", "site_basis": "기본값 — DEC-003 D-05 「원천에 부위 없는 … 기본 얼굴 전체」(site_basis=기본값)",
 "attrs": {"svf": "SVF 보강(원장 「SVF지방이식」 — 근거 약 · F5)"}, "evidence_level": null, "decided_by": "J1 안 C · J2 · S1~S6(step5-research)"}
```

```json
{"id": "U5-128", "key": {"family": "N5", "sub_family": null, "ingredient": null, "site": "해당 없음", "technique": "K01"},
 "name": "태반주사", "site_basis": "규칙 — 전신 투여(수액 「해당 없음」과 같은 값 · step5-research2)", "attrs": {}, "notes": [], "evidence_level": "중", "decided_by": "F8 · U1"}
```

### 1-2. ledger[] 한 줄

| 칸 | 값 |
|---|---|
| `id` · `name` | 원천 원장 항목 id · 이름(이름이 바뀌면 open) |
| `rule` | L1 ~ L11 |
| `dest` | 9종(`key-rules.md` §1) |
| `units` | 단위 시술 · 제품 + 단위 시술이면 1개 이상 |
| `resolve` | 다른 단계 이름일 때 — `{family, sub_family?, technique?, site_group?}` 조회 규칙 |
| `role` | 「이름」 · 「후보」(여러 키 · 이름이 키와 어긋남) |
| `uses_product` · `uses_product_ids` | 장비 행이 그 키의 쓰는 제품(저장) |
| `purposes` | 목적 낱말(7단계 넘김) |
| `origin_question` | 원천 질문 문장 — 있으면 `step5-origin-questions.md` 에 나가고, 추천 가능 제품 단위 시술 0 의 **예외 결정**이 된다 |
| `evidence_level` · `note` · `source_fix` · `to` · `fgroup` · `basis` · `decided_by` | 근거 · 행선지 설명 · 원천 수정 후보 · 묶음 |

```json
{"id": "M8-4-1", "name": "브이빔", "rule": "L1", "dest": "제품 + 단위 시술", "units": ["U5-141"], "role": "이름",
 "basis": "1단계 정본 active · 2단계 계열 · 10-29 step5-fix3 — 장비 · 제품 이름이 그 단위 시술을 부름(쓰는 제품 = 이 제품)",
 "purposes": [], "fgroup": null, "decided_by": "S1(step5-research) · step5-fix3(10-29)", "uses_product": true}
```

```json
{"id": "auto-25-1774737181584", "name": "기타 엑소좀", "rule": "L8", "dest": "다른 단계 이름", "units": [], "role": "후보",
 "resolve": {"family": "M5", "sub_family": "엑소좀"}, "to": "2단계 하위 계열 — M5 하위 「엑소좀」 동의어", "decided_by": "S1(step5-research)"}
```

```json
{"id": "auto-M15-1775364797158", "name": "피나스테리드도포", "rule": "L10", "dest": "값", "units": [], "role": "이름",
 "to": "값 — M15 하위 「외용제」 성분 값 · 사후관리 권장 제품(F9 · 버림 0)", "decided_by": "F9"}
```

예외 결정(추천 가능 · 단위 시술 0) — 원장 행 `origin_question` + `note`:

```json
{"id": "auto-M8-1775364775123", "name": "스마트사이드", "rule": "L1", "dest": "제품", "units": [],
 "origin_question": "「스마트사이드」(DEKA SmartXide · CO2+RF)는 프락셔널(분할 조사)로 쓰나요, 전면 박피 · 절개로 쓰나요? (… 프락셔널 출처 없음 · CO2 키는 얼굴 전체 CO2 프락셀(K04b)뿐 — 지금은 단위 시술 없음 · 추천 가능 제품 예외)",
 "note": "v2 F1(10-29 step5-fix4) — 매질(하위) 일치만으로는 기법 근거 아님 · 출처로 시술 방식이 안 닫혀 예외 표시 + 원천 질문 · 추정 안 함"}
```

### 1-3. market[] · problem_P1[] 한 줄

```json
{"name": "레이저 제모 (겨드랑이)", "kind": "시술 1회", "units": ["U5-100"], "role": "이름", "product": [], "grade": null,
 "spec": {"raw": "1회", "amount": 1.0, "unit": "회"}, "sessions": null, "category_conflict": false, "note": null, "fgroup": null, "decided_by": "S9(step5-research)"}
```

```json
{"id": "auto-63-1774737181584", "name": "코필러", "decided_by": "S2(step5-research)", "dest": "단위 시술 이름", "units": ["U5-084"], "role": "이름"}
```

## 2. step5-units.json(산출)

| 칸 | 무엇 |
|---|---|
| `summary` | `units` · `units_by_family` · `ledger_521`(total · products · procedures · procedures_with_unit · procedures_by_dest · procedures_candidate · package_6 · not_procedure · pending_director · no_decision · check) · `product_links` · `pih` · `ops` · `handoffs` · `open` · `stale_decisions` … |
| `units[]` | 결정 칸 + 산출 칸 `sources[]`(src · id · name · role) · `synonyms[]`(text · type · src · ambiguous) · `candidate_of` · `uses_product[]`(product · basis · name · recommendable) · `purposes` · `route_status` · `market[]` · `pih` / `pih_gap` / `pih_not_applicable` · `ops` · `step4_attrs` · `dose_range_text` |
| `ledger[]` | 결정 칸 + `detail` · `source_family` · `source_sub` · `product` · `product_state` |
| `product_links[]` | 1단계 active 제품마다 — `family` · `sub_family` · `recommendable` · `stored_units` · `inherited_candidates` · `technique_excluded[{unit, reason}]` · `technique_attrs` · `guard` · `link` |
| `market[]` · `problem_P1[]` · `step1_market_copies[]` · `extracted[]` · `taxonomy_products[]` · `pih[]` · `step4_attrs[]` · `dose_range[]` · `handoffs` · `device_name_synonyms[]` · `synonym_multi_unit` | 붙는 것 산출 |
| `origin_questions[]` · `staff_questions[]` | 원천(병원) 질문 19 · 의료진 질문 1 |
| `open[]` · `stale_decisions[]` | 지금 0 · 0 |

`product_links` 한 줄(실제):

```json
{"product": "M8-5-3", "name": "젠틀맥스 프로 플러스", "family": "M8", "sub_family": "알렉산드라이트 레이저", "recommendable": true,
 "stored_units": [], "inherited_candidates": ["U5-023", "U5-099", "U5-100", "U5-101", "U5-131"],
 "technique_excluded": [{"unit": "U5-024", "reason": "매질만 · 기법 근거 없음(K04a)"}, {"unit": "U5-025", "reason": "매질 미지정 키 · 기법 근거 없음(K04a)"},
                        {"unit": "U5-026", "reason": "매질만 · 기법 근거 없음(K04b)"}, {"unit": "U5-031", "reason": "매질 미지정 키 · 기법 근거 없음(K04)"}],
 "technique_attrs": null, "guard": null, "link": "조회 때 상속 후보"}
```

`link` 값: 저장 uses_product · 조회 때 상속 후보 · 계열 has_product 만(기법 호환 단위 시술 없음 — F1) · 계열 has_product 만(이 계열 · 하위에 단위 시술 없음) · 계열 밖(단위 시술 없음) · 원장님 문의(계열 없음).

## 3. open 종류(step5-apply.py)

결정 한 줄로 닫힌다. 고정 시험 `step5-fixtures/cases.json` 24건이 「결정 한 줄 빼면 이 open」을 지킨다.

| open | 닫는 법 |
|---|---|
| 결정 없는 원장 항목 · 원장 항목 이름 바뀜 · 원장 행선지 값 밖 | `ledger[]` 한 줄 |
| 원장 「단위 시술」인데 키 없음 · **시술인데 단위 시술 없음** | 키를 세우거나 기존 키 `units` |
| 원장 「제품」인데 1단계 행 없음 / 1단계에서 시술 이름으로 빠짐 | 1단계 먼저(`procedure-hub-product-check`) |
| 결정 없는 시장가 행 · 시술 1회인데 키 없음 · 시장가 제품이 1단계 active 아님 | `market[]` 한 줄 |
| 결정 없는 쁘띠시술 메뉴 | `problem_P1[]` 한 줄 |
| 단위 시술 키 오류(계열 · 하위 · 성분 · 부위 · 기법 · 겹침) · 이름 겹침 · 원천 근거 없는 키 · 결정이 가리키는 키 없음 · 이름이 부르는 단위 시술 없음 | `units[]` · `resolve` 고침 — 계열 · 부위 · 기법이 정본에 없으면 그 단계 먼저 |
| 넘겨받은 것 행선지 없음(1단계 moved_to · 2단계 deferred · 3단계 · 4단계 handoffs · 4단계 표현 · source-map 5단계 칸) | `handoffs.<출처>` 한 줄 |
| 기법 호환 결정 없는 기법 · 기법 호환 기법 / 펄스 / 가능 방식 / 하위 / 제품이 정본에 없음 | `technique_compat.requires[]` · `family_evidence[]` |
| **추천 가능 제품인데 단위 시술 0 · 예외 결정 없음** | 키를 세우거나 · 출처로 잇거나 · 원장 행 `origin_question`(예외) |
| 결정 없는 PIH 행 · PIH 붙는 단위 값 밖 · 결정 없는 4단계 속성 · 결정 없는 위험 부위 용량 · taxonomy 제품이 1단계 행 없음 · 마취 값 사전 밖 | 그 결정 칸 한 줄 |
| 1단계 active 제품이 2단계에 없음 | 2단계 먼저(`procedure-hub-family-check`) |
