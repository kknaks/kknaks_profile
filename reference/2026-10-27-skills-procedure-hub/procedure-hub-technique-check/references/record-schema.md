# 레코드 스키마 — 결정 · 원장 · 지도 칸

4단계는 **결정이 데이터**다. 사람이 고치는 것은 `step4-decisions.json` 하나뿐이고, 원장 `step4-techniques.json` · `.md` · `step4-source-fix.md` 는 `step4-apply.py` 가 매번 원천 · 지도 · 앞 단계 정본에서 다시 만든다. 칸을 새로 만들지 말고 이 칸에 넣는다.
아래 발췌는 v1 판(2026-10-28 · open 0 · 검수 W1 · W2 수정 뒤)의 실제 값이다.

## 1. 결정 `step4-decisions.json`

| 칸 | 무엇 | 비고 |
|---|---|---|
| `version` · `decided_at` · `decision_ref` · `research` | 판 · 날짜 · 근거 결정 · 조사 파일 | 지금 `v1` |
| `bundles[]` · `user_decisions[]` | 결정 묶음 S1~S12 · 사용자 판단 J1 · J2 | 12 · 2 |
| `source{path, snapshot}` | 원천 폴더 | `/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-stg-2026-10-26` |
| `source_map{file, stage, meaning}` | 입력 = 지도에서 `stage` 로 정한 칸만 | `source-map.json` · stage `4` |
| `index_label` | 지도 경로 `name[]` 을 펼칠 때 원소 이름표 | {"zones": "id", "profiles": "id", "modality": "id", "sequence_order": "order"} — `zones[nose]` · `modality[M8]` · `sequence_order[4]` |
| `dedupe{file, against_file, rule, destination}` | extracted ↔ taxonomy 글자 같은 줄 = 중복 | 다른 줄은 제 행 |
| `nodes[{id, name, parent, medical_name, basis, decided_by}]` | 노드 24 | `references/nodes.md` — 상위는 큰 기법이어야(2층) |
| `dictionaries{layer, pulse_mode, ablative, tool_form, peel_depth, modes[], target_muscle[], device_attrs, unit_procedure_attrs}` | 값 사전 | `references/value-dictionary.md` |
| `zone_site{file, key}` | zone → 3단계 부위 노드 | `step3-decisions.json` `danger_zone_mapping`(읽기만) |
| `site_layer_split[]` | 한 zone 안 자리별 층 | 1(코) |
| `expressions[]` | **표현 행선지** — 지도 칸에서 펼친 (파일, 키, 원문)마다 한 줄(아래 §1-2) | 164 — 새 표현은 여기 한 줄로 닫는다 |
| `handoffs[]` | 넘겨받은 것(§1-3) | 15(H01~H15) |
| `technique_hints[]` | step2 hint → 장비 속성(§1-4) | 25 |
| `pulse_by_medium{매질: [펄스]}` | 매질별 낼 수 있는 펄스 | 매질 = 2단계 하위 계열 |
| `family_defaults[]` | 계열 기본 기법 | 18 — `references/family-defaults.md` |
| `draft_techniques[]` | 초안 큰 기법 → 유지 · 합침 · 버림 | 65 |
| `structure_options[]` | J1 안 1 · 2 · 3 | 3 |
| `conflicts[]` | 원천 충돌 X1~X6 | 6 |
| `source_fix{source_candidates, dec_text, step3}` | 원천 · DEC 문구 · 3단계 정본 수정 후보 — 목록만 | `step4-source-fix.md` 로 나온다 |
| `oq_closed[]` · `not_done[]` | 닫은 OQ · 하지 않은 것 | 4 · 3 |

### 1-1. 노드 행 `nodes[]`

```json
{"id": "K01", "name": "주입", "parent": null, "medical_name": "injection", "basis": "mechanism injection(M1~M6 · M17) · group 주사/주입 · 계열 정의 「주사」「주입」(M1~M6 · M17 · N1) · DEC-002 D-02 예시 「근육 내 주입」「피하 주입」", "decided_by": "S1 · S2 · S3 (J1 안 1)"}
{"id": "K04a", "name": "토닝", "parent": "K04", "medical_name": "laser toning (low-fluence multi-pass)", "basis": "treatment-sequence 「M8-토닝」(레이저 단계 안에서 따로 부름) · 원천 항목 레이저토닝 · 피코토닝 · 알렉스토닝 · 제네시스토닝", "decided_by": "S1 · S2 · S3 (J1 안 1)"}
```

### 1-2. 표현 행 `expressions[]`

| 칸 | 값 | 규칙 |
|---|---|---|
| `file` · `key` · `text` | 원천 파일 · 펼친 경로(`zones[nose].safe_injection_depth`) · 원문 줄 | **셋이 키** — open 에 찍힌 값 그대로. 같은 키 두 줄이면 실패 |
| `verdict` | 근거 수치 · 근거 원문 · 근거 원문 + 넘김 · 근거 원문(관통 금지 지표) + 넘김 · 근거 원문(주입 지표) · 근거 출처 · 기법 노드 · 기법 노드 근거 · 넘김 · 속성 값 · 속성 값 + 넘김 | 판정 |
| `bucket` | 속성 · 넘김 · 노드로 | 셋뿐(산출에는 중복 · open 도 나온다) |
| `stage` | 2단계 · 5단계 · 7단계 · 8단계 · 계열 밖 · 시맨틱 | 넘김이면 필수 |
| `destination` | 행선지 문장 | 사람이 읽는 칸 |
| `node` | 노드 id | 노드로면 필수 · 24 안 |
| `layers[]` · `constraint_text` | 층 값(사전 안) · 원문 제약 | 층이면 키가 `zones[<id>]` 이고 zone 이 3단계 부위에 닿아야 |
| `muscles[{muscle, sites[]}]` | 대상 근육(사전 키) @ 3단계 부위 | |
| `attach[{muscle}]` · `attach[{layer, site}]` | 근거 속성이 붙을 곳 | 근거 수치 · 원문 · 출처 |
| `other_parts` · `name` · `group` | 같은 줄의 다른 몫 · 이름 · 묶음 | |
| `basis` · `note` · `decided_by` | 지도 칸 · 결정 근거 · 메모 · 묶음(S7 · 브리프 · 검수) | |

실제 행:

```json
{"file": "anatomy-danger-zones.json", "key": "zones[nose].safe_injection_depth", "text": "골막상 (코뼈 부위) 또는 연골막상 (비첨부)", "verdict": "속성 값", "bucket": "속성", "stage": null, "destination": "4단계 — 단위 시술 속성 `safe_layers`(부위 × 큰 기법 주입 제약 · 키 밖) · 3단계 danger_zone_mapping 으로 부위 노드 「코(묶음)」에 대응", "layers": ["골막상", "연골막상"], "constraint_text": "골막상 = 코뼈 부위(콧등) · 연골막상 = 비첨부(코끝)(원문) — 코(묶음)은 둘 다", "basis": "source-map 4 · 속성 「기법(층 · 깊이) — 부위별 주입 층 제약」 · _RESUME 10-28 해부학 결정(층 · 깊이 → 4단계)", "note": null, "decided_by": "S7 · 브리프(코 층 나눔)"}

{"file": "anatomy-danger-zones.json", "key": "zones[cheek].botox_specific.target_muscle", "text": "교근 (Masseter) — 사각턱, 광대근 (Zygomaticus) — gummy smile", "verdict": "속성 값", "bucket": "속성", "stage": null, "destination": "4단계 — 대상 근육 값 사전(시맨틱 16) · 단위 시술 속성 `target_muscles`(M1 보툴리눔 톡신 × 부위 · 키 밖)", "muscles": [{"muscle": "Masseter", "sites": ["사각턱"]}, {"muscle": "Zygomaticus", "sites": ["잇몸"]}], "other_parts": ["사각턱 → 3단계 노드 · gummy smile → 7단계 고민(잇몸 노출 미소)"], "basis": "source-map 4 · 속성 「기법(대상 근육) — 톡신 × 부위 단위 시술」 · _RESUME 10-28 해부학 결정", "note": null, "decided_by": "S7"}

{"file": "anatomy-danger-zones.json", "key": "zones[nose].tissue_data.rhinion_subcutaneous_mm", "text": "2.02", "verdict": "근거 수치", "bucket": "속성", "stage": null, "destination": "4단계 — 근거 속성(`evidence`) — layer:피하@코", "attach": [{"layer": "피하", "site": "코"}], "basis": "source-map 4 · 「기법(대상 근육 · 깊이) 근거 수치」/「층 · 깊이 · 주입 지표 근거」", "note": null, "decided_by": "S7"}

{"file": "treatment-sequence.json", "key": "sequence_order[4].categories", "text": "M8-토닝", "verdict": "기법 노드", "bucket": "노드로", "stage": null, "destination": "4단계 K04a 토닝 → 순서 주장 `conditions.technique`", "node": "K04a", "basis": "source-map 4 rec 「꼬리는 4단계 기법 / 2단계 하위 계열 사전으로 풀어 conditions.sub · 마취 · 클렌징 · 진정은 세션 단계」", "note": null, "decided_by": "S7"}

{"file": "taxonomy.json", "key": "modality[M1].extracted.related_techniques", "text": "메조보톡스 (더모톡신) — 피부 탄력 개선, 리프팅 효과", "verdict": "기법 노드 근거", "bucket": "노드로", "stage": null, "destination": "4단계 K01a 메조테라피 — 단위 시술 이름(스킨보톡스 동의어)은 5단계", "name": "메조보톡스 (더모톡신)", "node": "K01a", "basis": "source-map B03 「「— 」 앞 이름은 기법/단위 시술 후보, 뒤 문장은 근거 · 계열 노드에는 붙이지 않음」", "note": null, "decided_by": "S7"}

{"file": "anatomy-danger-zones.json", "key": "zones[temple].tissue_data.notes", "text": "Pitanguy line 위에서 안면신경 측두분지가 표재성으로 주행 — 이 선 위 피하층 주사 주의", "verdict": "넘김", "bucket": "넘김", "stage": "8단계", "destination": "8단계 — site_caution 신경(안면신경 측두분지 · Pitanguy line)", "basis": "source-map 4 · 「기법(층 · 깊이 · 주입 지표) 근거」 · 10-28 해부학 결정(혈관 · 신경 · 합병증 = 8단계)", "note": null, "decided_by": "S7"}

```

### 1-3. 넘겨받은 것 `handoffs[]`

| `source_ref.type` | 무엇을 가리키나 | 역검사 |
|---|---|---|
| `step3_deferred` | `step3-sites.json` `deferred[]` 키(stage 에 「4단계」) | 4단계로 넘긴 deferred 전부가 한 줄을 가져야 |
| `step3_compound` | step3 strings 중 handoff stage 「4단계」 인 D-07 키들 | 같음 |
| `step3_handoff_note` | step3 노드 `handoff_note` 에 「4단계」 | 같음 |
| `step3_string` | step3 strings 키 하나 | 원천에 있는지만 |
| `step2_deferred` | step2 계열 `deferred[].deferred_to` 에 「4단계」 | 같음 |
| `step2_ledger` · `step2_hints` · `source_map` | step2 행 id · hint 전체 · 지도 판단(U5) | 행이 있는지만 |

`muscles[]` · `landmarks[]` 가 있으면 대상 근육 · 주입 지표 값으로도 들어간다.

```json
{"id": "H05", "from": "step3 handoff_note", "item": "사각턱 — 깨물근 · 아래턱뼈각", "destination": "대상 근육 Masseter(M1 × 사각턱) · 「아래턱뼈각」 = 주입 지표 근거(`landmarks` 원문)", "source_ref": {"type": "step3_handoff_note", "node": "사각턱"}, "muscles": [{"muscle": "Masseter", "sites": ["사각턱"]}], "landmarks": [{"site": "사각턱", "text": "아래턱뼈각(angulus mandibulae)"}], "decided_by": "S10"}

{"id": "H15", "from": "step3 strings(브리프 추가)", "item": "표정근(1)", "detail": "3단계 이름 칸 「표정근」(시장가 「안면 EMS (표정근 강화)」) — step3 정본은 4단계 대상 근육으로 넘김", "destination": "대상 근육 값 「Musculi faciei (mimetic muscles) · 표정근(얼굴근육)」(근육 묶음) — M10 × 얼굴 × K06 전자기 자극 단위 시술 속성 `target_muscles`(5단계에서 붙임). step3 얼굴 노드 해부학 이름 속성에서 빼기는 step4-source-fix.md", "source_ref": {"type": "step3_deferred", "key": ["표정근", "표정근"]}, "muscles": [{"muscle": "Musculi faciei (mimetic muscles)", "sites": ["얼굴"]}], "decided_by": "브리프 추가(_RESUME §2 10-28 「4단계 입력 추가」)"}
```

### 1-4. 장비 속성 `technique_hints[]`

`hint` = step2 `product_family[].technique_hint` 원문 그대로(다르면 오류) · `pulse_mode` · `modes` · `ablative[{value, basis}]` 는 사전 안 · `dropped{}` = 버린 hint 와 이유 · `pulse_scope` = 펄스가 보조 하위 계열에만 걸릴 때 그 이름(step2 `also_sub_families` 에 있어야).

```json
{"ledger_id": "M8-1-3", "name": "피코슈어", "sub_family": "알렉산드라이트 레이저", "hint": ["프락셔널", "피코초"], "pulse_mode": ["피코초"], "modes": ["프락셔널"], "ablative": [], "dropped": {}, "destination": "제품(장비) 속성 — 펄스 방식 · 가능 방식 · 박피 여부 → 5단계 uses_product 로 단위 시술(K04a 토닝 · K04b 프락셔널 …)과 잇는 조건", "note": "프락셔널 = 「Focus Lens Array로 프락셔널 효과도 제공」 — 렌즈로 되는 가능 방식(mode)", "decided_by": "S6"}

{"ledger_id": "auto-M8-1775364106103", "name": "셀렉V", "sub_family": "IPL", "hint": ["Q-switched"], "pulse_mode": ["Q스위치(나노초)"], "pulse_scope": "보조 하위 계열 엔디야그 레이저", "modes": [], "ablative": [], "dropped": {}, "destination": "제품(장비) 속성 — 펄스 방식 · 가능 방식 · 박피 여부 → 5단계 uses_product 로 단위 시술(K04a 토닝 · K04b 프락셔널 …)과 잇는 조건", "note": "Q스위치는 원천 설명의 Nd:YAG 에 붙음 → 2단계 보조 하위 계열 「엔디야그 레이저」 쪽 장비 속성으로 한정(주 IPL 에는 펄스 방식 없음) · 허가 ↔ 원천 매질 충돌은 step2 conflict 그대로", "decided_by": "S6 · 검수 W1(조사 pulse_scope 되살림)"}
```

### 1-5. 계열 기본 · 초안

```json
{"family": "M4", "family_name": "스킨부스터", "default": "K01a", "default_name": "메조테라피", "also": ["K01c"], "default_layer": "진피", "basis": "정의 「진피에 소량씩 여러 점 주입(또는 무바늘 제트 주입)」 · 문헌 이름 mesotherapy", "decided_by": "S8"}

{"id": "T04", "name": "토닝", "source_expressions": ["토닝", "532nm 포커스 토닝", "포커스 토닝", "피코토닝", "알렉스토닝", "듀얼 토닝", "제네시스토닝"], "draft_unit_procedures": 3, "verdict": "유지", "node": "K04a", "node_name": "토닝", "reason": "변형 이름(피코토닝 · 알렉스토닝 · 제네시스토닝 · 포커스 · 듀얼)은 5단계 이름 · 동의어 — 펄스 · 매질은 장비 속성/2단계 하위", "decided_by": "S9"}

{"id": "T03", "name": "네페르티티 리프트", "source_expressions": ["네페르티티 리프트"], "draft_unit_procedures": 0, "verdict": "버림", "node": null, "node_name": null, "reason": "5단계 단위 시술 이름(M1 × 턱선 · 목 · 기법 K01 · 대상 근육 Platysma) — D 표 네페르티티", "decided_by": "S9"}
```

## 2. 원장 `step4-techniques.json`(산출 — 손으로 고치지 않는다)

| 칸 | 무엇 |
|---|---|
| `summary` | 셈 — `source{cells, lines, values, unique_values, dup_groups, dup_lines}` · `nodes` · `by_bucket` · `handoff_by_stage` · `dictionaries` · `safe_layer_sites` · `target_muscles` · `landmarks` · `handoffs` · `hints` · `family_defaults` · `draft_techniques` · `open` · `stale_decisions` |
| `nodes[]` | 결정 노드 + `level` · `children` · `family_default` · `family_also` · `source_expressions` · `draft_techniques` · `modes` |
| `unit_procedure_attrs{safe_layers, target_muscles, landmarks}` | 단위 시술 속성(5단계가 붙인다) |
| `device_attrs{technique_hints, pulse_by_medium}` | 장비 속성(5단계 uses_product 조건) |
| `expressions[]` | 표현 행(결정 칸 + `count`) · 중복 묶음 행(`bucket` 중복) |
| `open[]` · `stale_decisions[]` | 끝 조건 = 둘 다 0 |

지금 셈(`summary`):

```json
{"source": {"path": "/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-stg-2026-10-26", "cells": 27, "lines": 215, "values": 181, "unique_values": 164, "dup_groups": 17, "dup_lines": 51}, "nodes": 24, "nodes_by_level": {"큰": 12, "세부": 12}, "by_bucket": {"속성": 64, "넘김": 59, "노드로": 41, "중복": 17}, "by_verdict": {"속성 값": 40, "근거 수치": 11, "근거 원문": 5, "넘김": 59, "근거 원문 + 넘김": 4, "근거 원문(주입 지표)": 1, "근거 원문(관통 금지 지표) + 넘김": 1, "근거 출처": 1, "속성 값 + 넘김": 1, "기법 노드": 22, "기법 노드 근거": 19, "중복": 17}, "handoff_by_stage": {"8단계": 31, "2단계": 21, "계열 밖": 3, "5단계": 2, "시맨틱": 1, "7단계": 1}, "dictionaries": {"layer": 13, "pulse_mode": 3, "ablative": 2, "tool_form": 3, "peel_depth": 3, "modes": 1, "target_muscle": 17}, "safe_layer_sites": 17, "safe_layer_sites_with_layers": 13, "target_muscles": 17, "landmarks": 2, "handoffs": 15, "hints": 25, "family_defaults": 18, "draft_techniques": {"합침": 29, "버림": 32, "유지": 4}, "conflicts": 6, "oq_closed": 4, "open": 0, "open_by_type": {}, "stale_decisions": 0}
```

## 3. 지도 4단계 칸 27(`source-map.json` `fields[]` · `destinations[].stage == "4"`)

| 파일 | 경로 | 값 수(지도) | 무엇 | 다른 단계 |
|---|---|---|---|---|
| anatomy-danger-zones.json | `zones[].safe_injection_depth` | 11 | 안전 주입 층(골막상 등) | — |
| anatomy-danger-zones.json | `zones[].tissue_data.frontalis_thickness.midpupil_mm` | 1 | 근육 두께 · 섬유 · 덮임(전두근 · 추미근 · 광경근 · DAO) | — |
| anatomy-danger-zones.json | `zones[].tissue_data.frontalis_thickness.lateral_canthus_mm` | 1 | 근육 두께 · 섬유 · 덮임(전두근 · 추미근 · 광경근 · DAO) | — |
| anatomy-danger-zones.json | `zones[].tissue_data.frontalis_thickness.lateral_orbital_rim_mm` | 1 | 근육 두께 · 섬유 · 덮임(전두근 · 추미근 · 광경근 · DAO) | — |
| anatomy-danger-zones.json | `zones[].tissue_data.skin_to_periosteum_mm` | 1 | 층 · 깊이 · 구조 수치와 설명(피부-골막 · SMAS · 안와격막 · 눈물고랑 · 협지방 · STL) | — |
| anatomy-danger-zones.json | `zones[].tissue_data.notes` | 11 | 층 · 깊이 · 구조 수치와 설명(피부-골막 · SMAS · 안와격막 · 눈물고랑 · 협지방 · STL) | — |
| anatomy-danger-zones.json | `zones[].botox_specific.target_muscle` | 11 | 보톡스 대상 근육 | — |
| anatomy-danger-zones.json | `zones[].tissue_data.csm_mean_thickness_mm` | 1 | 근육 두께 · 섬유 · 덮임(전두근 · 추미근 · 광경근 · DAO) | — |
| anatomy-danger-zones.json | `zones[].tissue_data.csm_thickness_variation_mm` | 1 | 근육 두께 · 섬유 · 덮임(전두근 · 추미근 · 광경근 · DAO) | — |
| anatomy-danger-zones.json | `zones[].tissue_data.stl_entry_point` | 1 | 층 · 깊이 · 구조 수치와 설명(피부-골막 · SMAS · 안와격막 · 눈물고랑 · 협지방 · STL) | — |
| anatomy-danger-zones.json | `zones[].tissue_data.tear_trough_anatomy` | 1 | 층 · 깊이 · 구조 수치와 설명(피부-골막 · SMAS · 안와격막 · 눈물고랑 · 협지방 · STL) | — |
| anatomy-danger-zones.json | `zones[].tissue_data.muscle_fiber_data` | 1 | 근육 두께 · 섬유 · 덮임(전두근 · 추미근 · 광경근 · DAO) | — |
| anatomy-danger-zones.json | `zones[].tissue_data.orbital_septum` | 1 | 층 · 깊이 · 구조 수치와 설명(피부-골막 · SMAS · 안와격막 · 눈물고랑 · 협지방 · STL) | — |
| anatomy-danger-zones.json | `zones[].tissue_data.rhinion_subcutaneous_mm` | 1 | 층 · 깊이 · 구조 수치와 설명(피부-골막 · SMAS · 안와격막 · 눈물고랑 · 협지방 · STL) | — |
| anatomy-danger-zones.json | `zones[].tissue_data.rhinion_data_source` | 1 | 층 · 깊이 · 구조 수치와 설명(피부-골막 · SMAS · 안와격막 · 눈물고랑 · 협지방 · STL) | — |
| anatomy-danger-zones.json | `zones[].tissue_data.nasal_tip_skin_thickness_mm` | 1 | 층 · 깊이 · 구조 수치와 설명(피부-골막 · SMAS · 안와격막 · 눈물고랑 · 협지방 · STL) | — |
| anatomy-danger-zones.json | `zones[].tissue_data.buccal_fat_pad` | 1 | 층 · 깊이 · 구조 수치와 설명(피부-골막 · SMAS · 안와격막 · 눈물고랑 · 협지방 · STL) | — |
| anatomy-danger-zones.json | `zones[].tissue_data.smas_depth_mm` | 1 | 층 · 깊이 · 구조 수치와 설명(피부-골막 · SMAS · 안와격막 · 눈물고랑 · 협지방 · STL) | — |
| anatomy-danger-zones.json | `zones[].tissue_data.sub_smas_vs_subcutaneous` | 1 | 층 · 깊이 · 구조 수치와 설명(피부-골막 · SMAS · 안와격막 · 눈물고랑 · 협지방 · STL) | — |
| anatomy-danger-zones.json | `zones[].tissue_data.dao_coverage` | 1 | 근육 두께 · 섬유 · 덮임(전두근 · 추미근 · 광경근 · DAO) | — |
| anatomy-danger-zones.json | `zones[].tissue_data.platysma_thickness_mm` | 1 | 근육 두께 · 섬유 · 덮임(전두근 · 추미근 · 광경근 · DAO) | — |
| anatomy-danger-zones.json | `zones[].tissue_data.platysma_coverage` | 1 | 근육 두께 · 섬유 · 덮임(전두근 · 추미근 · 광경근 · DAO) | — |
| extracted.json | `{code}.related_techniques` | 17 | 관련 기법 문장(taxonomy 와 같은 칸) | — |
| procedure-profiles.json | `profiles[].mechanism` | 17 | 작용 방식 태그(injection · regenerative · thermal …) | — |
| taxonomy.json | `modality[].group` | 17 | 시술군 큰 묶음(주사/주입 · 시술/기기) | — |
| taxonomy.json | `modality[].extracted.related_techniques` | 17 | 계열과 관련된 기법 · 응용 시술 문장(메조보톡스 · 에어보톡스 …) | — |
| treatment-sequence.json | `sequence_order[].categories` | 11 | 단계에 든 시술(「M9-HIFU」 · 「M15-클렌징」 · 「국소마취」) | 8 |

경로 읽는 법: `zones[]` = 배열 원소마다(이름표 `index_label`) · `{code}` = 객체 키마다 · 잎 값이 리스트면 한 줄씩. 펼친 키는 `zones[nose].safe_injection_depth` · `M8.related_techniques` 꼴.
treatment-sequence `categories` 는 8단계와 4단계가 나눠 쓴다 — 꼬리(「M8-토닝」)는 4단계, 순서는 8단계.
