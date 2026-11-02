# step8 결정 · 원장 칸

## 1. step8-decisions.json

| 칸 | 무엇 |
|---|---|
| `source.path` · `canon` | 원천 폴더 · 1~7단계 정본 · source-map 경로 |
| `user_decisions[]` | G1~G14 · U8-1 · U8-2 · 간격 · 충돌(사용자 10-29 — superseded) · 충돌(10-30) |
| `conflict_resolution` | 10-30 충돌 하나로 — `rules[]`(R1~R6 문장) · `axes[]`(부위 · 박리 · 깊이 · 출력 · 용도 낱말) · `session_label_marks` · `field_axes`(필드별 비교 축 — first: 세션 … · same_day: 순서 …) · `grade_order` · `wait_axes` · `unknown_condition_*` · `review_status` · `review_label` · `x8_why` · `guards` |
| `origin_questions_retired[]` | 규칙으로 정해 내린 질문(id 다시 안 씀 · resolution) |
| `avoid_edge_type` | 피함 엣지 이름 `concern_avoid` · 라벨 · SPEC 개정 메모 |
| `labels` | 원문 등급 → 사이트 라벨 · 3분류 · 합병증 중증도 · 경과표 라벨 |
| `resolver` | `strip_prefix`(저출력 · 고출력 …) · `tail_words` · `tail_regex` · `cut_regex`(「…로 …」) · `note_filters`(제모 · 혈관) · `alias[]`(원천 낱말 → target{units · family · sub · technique · site · note · family_set · wildcard · none} · basis) |
| `interval_lexicon` | `units_days` · `branches[]`(id · pattern · set{kind · days · same_day · mark · condition · repeat · days_if_none · first_from_source_order}) · `word_branches[]` · `open_high_after/before` · `option_split` · `sub_condition_head` · `interval_words` |
| `sentence` | `patterns[]`(id · regex · emit(pair · chain · first_or_gap · gap_or_first · list_pair · list_ellipsis · concern_avoid · condition_forbid · row_concern_avoid) · first · kind · only_order_mode) · `mixed_mode_fields` · `order_mode_fields` · `orphan_interval_regex` · `qualifier_words` · 규칙 설명 |
| `conditions[]` | 확인 조건 노드 id · 이름 · 패턴 |
| `not_person_rules[]` · `age_avoid_patterns[]` | 사람 조건 아닌 문장 · 연령 avoid |
| `guide_not_source_rule` | 출처 낱말 정규식 |
| `timeline_attach{}` | 경과표 id → 붙는 곳(level · attach · units · units_where) |
| `step7_note_sources{}` | 7단계 메모 원천 → 8단계 원천 칸 |
| `field_handlers[]` | source-map 8단계 칸 접두 → 원장 자리 |
| `wide_candidates_threshold` · `_levels` · `purpose_ok[]` | 원천 질문 기준 |
| `scope_rule` · `reading_contract` · `web_evidence_rule` · `research_diff_reasons{}` | 한정어 조건부(검수 F1) · 읽기 규칙(by_sub_condition · default_apply) · 웹 근거 종류 · multi_url(W2) · 조사 대비 셈 차이 이유(W1 — 없으면 open) |
| `origin_questions[]` | id · to · q · match{type · texts · pairs · conditions · all} |

## 2. step8-relations.json

| 칸 | 무엇 |
|---|---|
| `reading_contract` | AI 는 `claims[].interval.days · first · same_day` 만 읽는다 |
| `edges[]` | id · a · b(끝점 키 `units:…` · `family:…#하위#기법` · `bundle:…` · `all`) · self_pair · claims · kinds · review_status |
| `claims[]` | id(R8-) · source · source_index · text · kind · a · b(끝점: level · via · families · sub_family · technique · units · flag · text · source_code · code_mismatch · parts) · directed · interval{text · days · open_high · first · first_basis · same_day · marks · condition · options[](sub_condition · first · days · same_day) · by_sub_condition · repeat · kind · branches} · 끝점 scope · default_apply · scope_words · scope_conditional · rule · condition{cc · problem · concern_ids · combo · severity} · strength_original · level_original · level_site · reason · evidence · evidence_text · evidence_kind · gate_status(자동(규칙)) · lowering · not_procedure · bundle_word · resolved · review_status |
| `conflicts[]` | id(X8-) · pair · type · sides · note |
| `avoid_edges[]` | id(AV8-) · edge_type · from_concerns(7단계 id) · to(끝점) · qualifier · text · source · rule · concern_basis |
| `conditions` | nodes · claims(K8- · target · grade_original · grade_site · grade3 · conditions · kind · wait) · grade_conflicts(XK-) · wait_conflicts(XW-) · extracted_vs_taxonomy |
| `safety` | complications(CX-) · complication_gap_families · site_caution(SC-) · critical_safety_facts · timelines · pih · family_text · item_text_counts |
| `evidence` | literature(EV-LIT-) · statements(ST-) · web(EV-WEB-) · guides(EV-GD-) · evidence_kind_by_file |
| `attrs[]` | 쌍 아닌 원문(7단계 조합 속성 · 계열 안전 원문 · 터치업 · 레시피 후속) |
| `sequence_rank` · `principles_text_only` · `package_evidence` · `profile_attrs` | 순위 표 · 원문만 원칙 · 6단계 근거 · 계열 플래그 |
| `origin_questions` · `source_fix_candidates` | 원천 질문(걸린 행) · 원천 수정 후보 |
| `step7_reconcile` · `coverage` · `research_diff` | 7단계 메모 대조 · source-map 칸 전수 · 조사 판 대비 |
| `open` · `stale_decisions` | 끝 조건 · 안 쓰인 결정 |

### 2-1. 시맨틱 반영 칸(10-30)

- `step8-decisions.json` `semantic_apply` — complication_severities · side_effect_severities · side_effect_common_incidence · gap_fill · endpoint_candidates · not_condition_rule · `origin_questions` Q8-19(side_effect_exception)
- `step8-relations.json` `safety.side_effects[]`{id SE-…, name, family, severity, severity_site, incidence, source, attach, staff_question?} · `safety.complication_mild_only_families` · `safety.side_effect_gap_families` · `conditions.not_condition[]` · `edges[].endpoints` · summary `side_effects` · `not_condition_claims` · `gap_filled_families`

## 3. step8-apply.py open 종류와 닫는 법

| open | 닫는 법 |
|---|---|
| 원천 질문이 필요한데 결정에 없음 | `origin_questions` 한 줄(질문만 · 추천값 안 채움) |
| 간격 원문 낱말을 읽는 사전 갈래 없음 · … 숫자 칸 · 표시 비어 있음 | `interval_lexicon.branches` · `word_branches` 한 줄 + 고정 시험 |
| 금기 조합 문장이 패턴 밖 · 규칙 행에서 쌍 · 속성 행선지가 안 나옴 · 세션 조합 note 가 패턴 밖 · 연령 avoid 문장이 패턴 밖 | `sentence.patterns` · `age_avoid_patterns` 한 줄(최종 판단) |
| 원천 행 행선지 없음 | 그 칸 처리 규칙 |
| 7단계 끝점 어긋남 — … | 7단계(concern-check)부터 |
| 8단계 칸인데 반영 규칙 없음 · 값 수가 source-map 과 다름 | `field_handlers` 한 줄 · source-map 재생성 확인 |
| 결정이 가리키는 단위 시술 · 계열 없음 | 5단계(unit-check) · 2단계 |
| 사람 조건인데 조건 사전에 안 걸림 | `conditions` 한 줄 또는 `not_person_rules` |
| 결정 없는 경과표 | `timeline_attach` 한 줄 |
| 7단계 메모 … | 메모 원천 → 8단계 칸 대응(`step7_note_sources`) |

## 충돌 하나로 칸(10-30 · step8-relations.json · 더하기만)

| 칸 | 무엇 |
|---|---|
| `edges[].resolved` | 앱이 읽는 값 — first(a · b · null) · days · open_high · same_day · by_sub_condition · options[](sub_condition · field · 값 · status · rule · from · 「조건 모름」 하나) · by_direction{a, b}.same_day · field_status · rules · status · alternatives[](원문 보관) · from_claims · inherited_claims · inherited_from_edges |
| `edges[].review_status` · `review_label` · `conflict_before` | ok · conservative · staff_check / 「」 · 보수적 선택 · 의료진 확인 / 옛 「conflict」 였나 — `claims[]` 도 같음 |
| `resolved_pairs[]` | 형제 엣지가 겹쳐 가장 구체적인 엣지 값이 둘인 단위 시술 쌍 — 쌍 하나로 접은 resolved |
| `conflicts[].resolution` · `sides_from_bundle` · `from_bundle` | 처분(status · rule · where · why) · 묶음 끝점 몫 · 묶음 끝점으로 새로 드러난 쌍(X8 뒤에 붙임 · 기존 id 유지) |
| `conditions.resolved[]` · `claims[].grade3_resolved` · `grade_conflicts[].resolution` | 대상 키 × 조건 등급 하나(R2 · 상속 접음) |
| `conditions.wait_resolved[]` · `claims[].wait_resolved` · `wait_conflicts[].resolution` | 대기 기간 하나(R6 · 깊이로 나누면 options + 조건 모름) |
| `origin_questions_retired` · `conflict_resolution_rules` · `summary.conflict_resolution` | 내린 질문 · 규칙 문장 · 셈(가짜 충돌 해제 · 보수 선택 · 진짜 반대 · 두 값 쌍) |

