# 기록 형식 — step7-decisions.json · step7-concerns.json

출처: `orchestration/work/phub-recommend/step7-decisions.json` · `step7-concerns.json` · `step7-apply.py`. 칸은 실제 파일에서 옮겼다. 셈은 `scripts/check_concerns.py` 출력에서 본다.

## 1. step7-decisions.json — 사람이 고치는 곳

| 칸 | 무엇 |
|---|---|
| `source.path` | 원천 스냅샷 폴더 |
| `canon` | 읽는 앞 단계 정본 `step3` · `step5` · `step6` |
| `rules[]` · `judgements[]` · `required_judgements[]` | R1~R11 규칙 · J1~J9 사용자 판단 — `required_judgements` 의 id 가 `judgements` 에 없으면 open |
| `rename` | 이름 치환(「쳐짐」 → 「처짐」만) |
| `site_terms` · `combo_kind_site_names` · `tier_label_site` | 사이트 화면 용어 · 조합 kind 사이트 이름 · 등급 라벨 |
| `categories[]` | 대분류 `{id, verdict, basis, decided_by}` |
| `subcategories[]` | 중분류 `{id, kind, concern, sites, purpose, note, node}` |
| `items[]` | 항목 `{id, name, kind}`(+ 고민이면 `concern` · `sites`) |
| `extra_concern_items[]` | 원천 밖 고민 노드 `{id, name, parent, sites, basis, decided_by}` |
| `concern_synonyms[]` | 노드 동의어(사이트 이름 · 지도 이름) |
| `composite_items` · `composite_site_split` | 복합 항목 · 부위 나눔 |
| `p1_detail_words` | 쁘띠시술 detail 의 고민 낱말 · 목적 낱말 → 대상 |
| `purpose_map_from_sub` | 목적 중분류 → 목적 노드 |
| `concern_rules` | 대응표 규칙 데이터(R12~R20) — `extra_site_words` · `split_separators` · `tails` · `state_tails` · `lead_words` · `anti_prefix` · `purpose_verb_tails` · `severity_words` · `severity_children` · `severity_survey` · `loanwords` · `en_extra` · `concern_words` · `purpose_concern` · `out_of_tree_purpose_kind` |
| `concern_unresolved[]` | 규칙 밖 사람 질문 `{source, text, question, decided_by}` — 없으면 open · 규칙으로 풀리면 stale |
| `purposes[]` | 목적 `{name, from, same_as_concern, kind, aliases[{source, text}], decided_by}` — `same_as_concern` null = 목적 노드 |
| `resolver` | 이름 풀이 사전 — `fam_kw` · `no_unit` · `generic_synonyms` · `brands` · `body_words` · `site_kw` · `ambiguous_site_kw` · `forced_synonyms` · `exact_overrides` |
| `site_rules` | `site_free`(부위 무관 특수 부위) · `lowering` · `no_unit_at_site` · `edge_check` 규칙 문장 |
| `context_by_source[]` · `purpose_context[]` | 최적화 · 비교 원천의 맥락 부위 · 목적(제모 맥락 → 제모 키) |
| `product_evidence_purpose_units[]` | 5단계 목적 키 → 단위 시술 |
| `unresolved_ok[]` | 못 푼 원소 `{text, basis, decided_by}` |
| `check_flags[]` | 의료진 확인 `{unit, rule, question, to}` |
| `step8_patterns` | 대안 칸 · 위험 대비 효과 문장 중 8단계로 뺄 정규식 |
| `source_fix_rule` · `unknown_concern_words` · `p1_combo_anchor_note` · `remaining[]` | 규칙 문장 · J9 낱말 · J5 문구 · 남은 것(이중턱 노드 둘) |

### 1-1. 대응 한 줄

```json
{"text": "주름 개선", "match": "고민 + 목적", "target": ["P2"], "basis": "「주름」 + 목적 「개선」"}
{"text": "볼륨 손실", "match": "반대말(목적 쪽 대응)", "target": ["목적:볼륨 회복(충전)"], "basis": "P4-2 「볼륨회복」(목적)의 고민 쪽 말 — 고민 노드 없음"}
{"text": "acne", "match": "고민 + 목적", "target": ["P6"], "basis": "「여드름 치료 비교」 — 고민 「여드름」 + 목적 「치료」 꼬리말(완전 일치 아님 · R5 게이트 · 검수 F1)"}   // comparisons — text = 비교 id
{"text": "주름", "target": ["P2"], "basis": "3단계 넘김 조각"}                          // step3_parts — match 없음(apply 가 가림)
```

- `match` 가 「완전」으로 시작하면 자동 — **원천 말과 대상 이름이 글자로 같을 때만** 그렇게 적는다
- `target` 은 고민 id(대분류 P · 중분류 P-n · 항목 auto-… · extra J8-…) 또는 `목적:<이름>`. 없는 id 면 open 「결정이 가리키는 고민 노드 없음」

### 1-2. 이름 풀이 한 줄

```json
// fam_kw — 낱말 → 고정 키(units) 또는 계열(families)
{"kw": "리포셀", "families": null, "units": ["U5-154"], "basis": "J7 G1 — 비교 「리포셀 (HIFU 지방)」 · 최적화 「바디 HIFU(리포셀)」 → U5-154 …"}
// no_unit — 시술 아님 · 단위 시술 없음(결정된 것만)
{"name": "실리콘시트", "basis": "5단계 「값」(실리콘시트 = 시술 아님)", "kind": "시술 아님"}
// exact_overrides — 원문 하나를 정해 둔 대로(원천 질문 함께)
{"text": "트라넥삼산(경구+주사)", "status": "후보 동의어(G10 — 주사 갈래) · 경구 = 시술 아님", "units": ["U5-018"], "flag": "ambiguous", "origin_question": {"to": "원천(병원)", "question": "…", "where": ["…"]}}
```

## 2. step7-concerns.json — 산출(손으로 고치지 않음)

| 칸 | 무엇 |
|---|---|
| `summary` | concern_nodes · taxonomy_layers · correspondence(rows · by_source · by_class · human_check · gate_status) · purposes · edges(total · by_source · to_units · family_only · no_target · unit_pairs · site_check) · combos(total · by_kind · sales_copy_default_excluded) · step8_notes · unit_gaps · not_procedure_names · p10_site_gaps · unresolved · check_flags · family_mismatch · open · stale |
| `concerns` | `categories` · `subcategories` · `items`(+ `resolve` · `modality_lowered`) · `extra_items` — 노드는 `node: true`(항목은 kind 「고민」) |
| `correspondence[]` | 대응 행 — source · field · text · match · target · basis · human_check · match_class · gate_status(「자동(완전 일치)」/「자동(규칙)」/「사람 질문(규칙 밖)」) · gate_initial(규칙 밖이면 후보) · candidates · question · rule_sites · severity · source_word · exact_name |
| `purposes[]` | 목적 — node · same_as_concern · aliases |
| `edges[]` | 엣지 — source(①~⑧) · source_id · from(고민 id / `목적:` / `opt:` / 「(앵커 없음 — 쁘띠시술)」) · to_units · to_family · lowering · basis · evidence · anchor_sites · resolve_flag(`no_unit_at_site` · `sub_undecided` · `concern_without_site` …) · target_kind · site_check · **`ccs[]`(R28 — 원천 CC 이름 목록 · ③ = evidence.ccs · ① = [항목 이름]) · `cc_named[]`(R28 — ⑤ CC 이름 = 그 시술) · `layer`(R32 — 부위 · 상위 · null) · `quality_dropped{R29 · R30 · R31: [뺀 단위 시술]}`**(10-30 품질 수정) |
| `combos[]` | 추천 조합 — id(RC-PC · RC-RE · RC-SQ · RC-OP · RC-AN · RC-AG · RC-CP) · kind · source · anchor · components / members / schedule · sales_copy · consult_copy · site_names |
| `step8_notes[]` | 8단계 메모 — kind · source · where · text |
| `unit_gaps[]` · `not_procedure[]` · `unresolved[]` · `check_flags[]` | 단위 시술 없는 이름(0 이어야) · 시술 아님 묶음 · 못 풂 · check |
| `origin_questions[]` | Q7-NN — 의료진(check) · 원천(병원 — exact_overrides) · **사람(규칙 밖 고민 표현 · R20)** — 규칙 밖 행마다 하나(text · why · candidates) |
| `source_fix_candidates[]` | 계열 코드 어긋남(비교 · CC · taxonomy 항목) |
| `open[]` · `stale_decisions[]` | 0 이어야 |

엣지 한 줄 예(10-30 품질 수정 뒤 · R29 부위 낱말 → 상위 층 · R31 원천 제품 하위로 뺌 · R32 상위 표시 · basis · evidence 줄임):

```json
{"source": "③ problem-packages CC 추천 시술", "source_id": "P1:이마지방이식", "from": "(앵커 없음 — 쁘띠시술)",
 "to_units": ["U5-020"], "to_family": "M5",
 "lowering": "복합 · 나눠 풂 · 원천 부위 낱말 이마(묶음)/이마 → 상위 부위 얼굴 전체 층(R21)(R29) · 원천 제품 하위 혈소판 농축물(PRP·PRF) 밖 2 뺌(R31)",
 "anchor_sites": ["이마(묶음)", "이마"], "resolve_flag": null, "target_kind": "단위 시술",
 "ccs": ["이마지방이식"], "site_check": "상위 부위 얼굴 전체", "layer": "상위",
 "quality_dropped": {"R31": ["U5-019", "U5-142"]}}
```

`site_check` 값: 「앵커 부위 없음」(검사 밖) · 「부위 안」 · 「상위 부위 <층>」(R21) · 「이 부위 단위 시술 없음 · 계열만」 · 「원천 하위 안 정함 · 계열만(R31)」 · 「단위 시술 없음」 · 「부위 밖」(있으면 오류). 10-29 이전 값 「그 부위 단위 시술 없음 · 후보 전부(표시)」는 W2 폐기로 없어졌다.

## 3. open · 오류 — 어느 스크립트가 무엇을

| 무엇 | `step7-apply.py` open | `check_concerns.py` |
|---|---|---|
| 결정 없는 고민 대분류 · 중분류 · 항목 · 항목 이름 바뀜 | ○ | open 「원장에 없는 taxonomy 고민 칸」(원장 쪽) |
| 결정 없는 고민 표현 · 대응 없는 CC · 중분류와 다른 CC 묶음 이름 | ○ | open 「원장 대응표에 없는 고민 표현」(원천 9곳 다시 뽑기) |
| **자동 대응인데 원천 말 ≠ 대상 이름**(F1) | ○ | 오류(원장 행 · 결정 행 둘 다) |
| 결정 target ≠ 원장 target(apply 안 돌림) | — | 오류 「원장 낡음」 |
| 규칙 자동 행 규칙 id · 대상 · 사람 질문 결정 · 질문 수 · 재실행 대조 | — | 오류 |
| 결정이 가리키는 고민 노드 · 목적 · 부위 · 단위 시술 없음 | ○ | 오류(원천 밖 고민 노드 · 단위 시술 없음) |
| 결정 없는 목적 표현 | ○ | — |
| **엣지 단위 시술이 앵커 부위 밖**(F2) | ○ | 오류 + 「후보 전부인데 표시 없음」 · 「후보 전부인데 그 부위 단위 시술 있음」 |
| **원천 구조에 없는 엣지 · 원천 구조 밖 엣지 · 원천 행 수 ≠ 엣지 수** | — | 오류 |
| 단위 시술 없는 이름 · 제모 부위 단위 시술 없음 | ○ → unit-check | — |
| 이름으로 못 푼 원소 · 결정 없음 | ○ | — |
| 결정 없는 세션 조합 앵커 · 추천 조합 등급 · 조합 종류(사이트 이름) | ○ | — |
| 영업 문구 기본 응답 포함 · 상담 문구 제외 | — | 오류 |
| 시술 아님 항목인데 시술 아님 결정 없음 · 쁘띠시술 메뉴가 5단계에 없음 | ○ | — |
| 사용자 판단 결정 없음 | ○ | — |
| 원장 open · stale · summary 불일치 | — | 오류 |

## 10-29 「게이트 → 규칙」 뒤 더해진 칸(키 이름은 그대로 · 더하기만)

- 최상위 `concern_unresolved[]` · `summary.correspondence.auto · auto_exact · auto_rule` · `summary.decision_nodes`
- 엣지 ④ `from_concerns` · `severity` · `severity_rule` · ② 는 대응 대상마다 엣지
- 추천 조합 RC-PC `anchor.concerns` · RC-OP `anchor.concern` = 중증도 앵커 · `opt_concern_targets` · `severity_rule` · RC-SQ `anchor.concern` = 고민 id 목록(전엔 설명 문자열) · 원소 `concern_gloss`(「프락셔널(피부결)」)
- 결정 노드(`extra_items`) `links` · `links_count` — J10 피부결이 붙은 대응 · 엣지 · 추천 조합 · 원소 풀이
