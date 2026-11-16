# semantic.json 칸 · 입력 · 누가 무엇을 보나

## 1. 입력 · 출력

| 구분 | 파일 | 무엇을 읽나 |
|---|---|---|
| 실버 | `step1-products.json` | items[](active) · lines{} |
| 실버 | `step2-families.json` | families[] · product_family[] |
| 실버 | `step3-sites.json` | nodes[](parent · synonyms) |
| 실버 | `step4-techniques.json` | nodes[] · family_defaults[] |
| 실버 | `step5-units.json` | units[](key · synonyms · uses_product · purposes) · rules.special_sites · device_name_synonyms |
| 실버 | `step6-packages.json` | packages[] · contains[] · slots[] |
| 실버 | `step7-concerns.json` | concerns · purposes[] · combos[] · edges[] · correspondence[] |
| 실버 | `step8-relations.json` | edges[](endpoints) · claims[] · avoid_edges[] · conditions · safety · evidence |
| 결정 | `step7-decisions.json` | concern_rules · resolver.fam_kw · concern_synonyms · site_rules(상속 I5 문장) |
| 결정 | `step8-decisions.json` | resolver.alias · interval_lexicon · reading 규칙 |
| 결정 | `step3-lexicon.json` | 정규화 |
| 실버 9단계 | `step9-explanations.json` | 값 사전(`value_dictionary` · D9-7) · 설명 사실 셈(`attributes_not_nodes` · `summary.explanation_facts`) — 11-01 |
| 출력 | `semantic.json` · `semantic.md` | 아래 칸 |

`semantic-build.py` 는 자기 폴더(`Path(__file__).parent`)에서 읽고 쓴다 — 시험은 입력 12 + 스크립트를 임시 폴더에 복사해 돌린다(`check_semantic.py` 가 그렇게 한다).

## 2. semantic.json 칸

| 칸 | 모양 | 뜻 |
|---|---|---|
| `version` · `generated_by` · `decision_ref` | 문자열 | 판 · 생성 스크립트 · 결정 행 |
| `inputs{파일: {version, sha256}}` | sha256 = 파일 바이트 sha256 앞 16자리 | 어느 실버 판에서 만들었나 — 지금 파일과 다르면 낡음 |
| `summary` | node_kinds · edge_kinds · glossary · flags · gate_values · inherit_rules · dictionary_expressions · dictionary_targets · dictionary_collisions · id_map · complications · side_effects · complication_gap_families · statements_by_class · open | 셈 요약 — 목록 길이와 같아야 |
| `node_kinds[]` | kind · name · internal · meaning · required · optional · canon · path · count · detail · id_rule · silver_id_patterns · canonical_id | 노드 종류 13 |
| `attributes_not_nodes[]` | what · where · count · rule · detail · decided | 노드가 아닌 것(부작용 · 끝점 묶음 · 조건 아닌 문장 · 허가 · 시장가 · 경과) |
| `edge_kinds[]` | kind · name · meaning · frm · to · directed · attrs · canon · path · count · inherit · page | 엣지 종류 21 · page = 연결 구조 페이지 종류에서 |
| `not_edges[]` | page · why | 저장 엣지 아님(prod_unit_inh · set_member) |
| `glossary[]` | term · definition · source | 용어 47 |
| `dictionary` | summary(셈 · 겹침 갈래 · 출처별 원소 · conflict_reported · tree_entries) · **resolve_rules** · interpret_rules · level_merged[] · expressions[] | 사전 하나 |
| `dictionary.resolve_rules` | normalize[] · fold{} · strip_chars · split · order[] · tails[] · prefix_min · prefix_rule · note | 찾는 규칙 하나(10-30 품질 M — `semantic-build.py RESOLVE_RULES` 그대로 · 측정 · 골드 resolve · `check_semantic.py` 가 읽음) |
| `dictionary.expressions[]` | expr · norm · variants[] · targets[{id, qualifier, reasons[]}] · sources[] · collision · mode · ambiguous · (level_merged · prefer) | 표현 행 |
| `ids` | rule · kinds[] · string_forms[] · silver_string_map{} · map[{canonical, kind, silver_id, name}] | id 대응 |
| `reading` | reading_contract · interval_fields · interval_lexicon · units_days · scope_rule · labels · endpoints · side_effects · not_condition · default_response · counts · flags[] · gate_status | 읽는 규칙 · 표시 12 · gate 3값 |
| `inheritance[]` | id · name · rule · fields · count · stored_now | 상속 9 |
| `statements` | total · by_field · by_class · table · source_fix · rule | 근거 문장 class(B2) |
| `open[]` | 문자열 · 객체 | 비어야 함 — 있으면 build 종료 코드 1 |

## 3. 어느 스크립트가 무엇을 보나

| 무엇 | semantic-build.py | check_semantic.py |
|---|---|---|
| open(만들 때 막힘) | 낸다(종료 코드 1) | build 종료 코드로 본다 |
| 결정론 · 낡음 | — | 임시 폴더 두 번 실행 · 정본과 바이트 비교 |
| 노드 · 엣지 셈 | 센다 | **따로 다시 센다**(`silver_objects` · `silver_edge_counts`) |
| 사전 · id · 표시 · 상속 · 안전 분리 | 만든다 | 불변식으로 본다 |
| 틀린 값 주입 | — | `--selftest` 15가지 |
| 찾는 규칙 문서 = 코드 · 사전 출처 · 접두 · 정규화 | `RESOLVE_RULES` 를 싣는다 | `norm` 을 `resolve_rules` 로 다시 계산해 대조(「norm ≠ 정규화(expr)」) — 칸 = 코드 대조 · 출처 · 접두 · 변형 예는 고정 시험 `semantic-fixture-test.py`(M · F · G · H · L) |

실버 단계별 open · errors 는 그 단계 스킬이 본다(concern-check · relation-check …). 시맨틱 점검은 실버가 이미 끝났다고 보고 그 위만 본다.
