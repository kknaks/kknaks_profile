# 레코드 스키마 — 결정 · 사전 · 원장

3단계는 **결정이 데이터**다. 사람이 고치는 것은 `step3-decisions.json`(행선지 · 노드 속성)과 `step3-lexicon.json`(사전 · 허용 목록) 둘뿐이고,
원장 `step3-sites.json` · `.md` · `step3-source-fix.md` 는 `step3-apply.py` 가 매번 원천에서 다시 만든다. 칸을 새로 만들지 말고 이 칸에 넣는다.
아래 발췌는 v5 + 한 줄 수정 판(2026-10-28 · open 0)의 실제 값이다.

## 1. 결정 `step3-decisions.json`

| 칸 | 무엇 | 비고 |
|---|---|---|
| `version` · `decided_at` · `decision_ref` · `revision` | 판 · 날짜 · 근거 결정 · 판 설명 | 지금 `v5 — 범위 바로잡기` |
| `source{path, glob, snapshot}` | 원천 폴더 · 파일 패턴 · 스냅샷 이름 | `/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-stg-2026-10-26` · `*.json` |
| `tree_source{file, key}` | 트리 = `procedure-master-v3.json` `site_tree`(DEC-002 37 + OQ-206 6) | 트리는 이 파일에서 읽는다 |
| `lexicon` | 사전 파일 이름 | `step3-lexicon.json` |
| `name_fields{rule, fields[{file, key, what}]}` | **이름 칸 17** — 부위 원천은 여기만 | `references/name-fields.md` |
| `node_additions[{name, parent, bundle}]` | 트리 밖에서 세운 노드 10 | 상위는 이미 있는 노드여야 한다(스크립트 가드) |
| `node_ids{이름: id}` · `nodes{이름: 속성}` | 노드 53 의 id · 속성(아래) | 셋(트리 + 추가 · ids · nodes)이 같은 집합이어야 한다 |
| `strings[]` | **문자열 행선지** — 이름 칸에서 뽑힌 문자열마다 한 줄(아래). 지금 176 | 새 문자열은 여기 한 줄로 닫는다 |
| `out_of_tree[]` | 트리 밖 이름 판정 18(`resolution_type` new_node · synonym · not_site · `strings[]` · `basis{rule1, rule2}` = D-05 ① ②) | strings 의 `out_of_tree` 와 서로 맞아야 한다 |
| `boundary_rules[{rule, decision, basis}]` | 경계 규칙 6(묶음 ↔ 좁은 · 턱 · 얼굴 ↔ 얼굴 전체 · 바디 ↔ 전신 · (묶음) 이름 · ‹부위›라인) | `references/nodes.md` 경계 절 |
| `danger_zone_mapping[{zone, node, verdict, basis}]` | 위험 부위 zone 11 → 노드 | 노드 `danger_zone` 과 맞아야 한다(가드) |
| `weak_string_question_template` | 근거 약 문자열 질문 틀 「「{string}」 를 {nodes} 에 둔다 — 맞나」 | `question` 칸이 비면 이 틀 |
| `doctor_questions_weak_anatomical` · `doctor_questions_extra[]` | 해부학 이름 「약」 노드마다 질문 틀 · 묶음 질문 2(위험 부위 대응 · 강 · 중 확정) | 질문 35 = 약 문자열 4 + 약 노드 29 + 2 |
| `node_naming{rule, reviewed[], changed[], kept_note}` | 이름 2벌 규칙 · 본 노드 53 · 바꾼 5 | |
| `strings_out_of_scope{reason, strings[], residual_reviewed[]}` | **셈 밖 기록** — 이름 칸에 한 번도 안 나오던 v4 까지의 결정 350행 | 지우지 않는다. 이름 칸에 나타나면 strings 로 되돌린다 |
| `residual_reviewed[]` | 사람이 문맥을 보고 닫은 잔여(`{token, context, verdict, file}`) | 지금 0(셈 밖 쪽에 1) |
| `source_fix{B11, B12, withdrawn_v5, known}` | DEC-002 근거 표 정정 · 원천 수정 후보 · 철회 | 목록만 — 원천은 안 고친다 |
| `changes[{version, key, change}]` | 판마다 바뀐 행 표(73) | 판의 기록이지 지금 행 목록이 아니다 |
| `rescope_before` | 범위 바로잡기 전(v4) 셈 | md 「전 → 후」 줄 |
| `bundles[]` · `user_decisions[]` | 조사 묶음 B1~B12 · 사용자 판단 U1 · U2 | |

### 1-1. 문자열 행 `strings[]`

| 칸 | 값 | 규칙 |
|---|---|---|
| `key` | `[정규형, 사전 무리(expr)]` | 정규형 = 공백 제거 · 영문 시작이면 소문자 · 라틴 악센트 접기. 무리 = 사전 `entries[].expr`. **키가 같으면 같은 곳으로 간다** |
| `destination` | `node` · `deferred` | 둘뿐. 다른 값은 open |
| `nodes[]` | 노드 이름 | `node` 면 1개 이상 · 53 안 |
| `kind` | 노드 이름 · 동의어 · 부위+다른 축(D-07) · 여러 부위(나열) · 해부학 이름(속성) · 부위 아님 | 지금 79 · 49 · 14 · 4 · 8 · 22 |
| `synonym_type` | 구어 · 외래어 · 영문 · 해부 · 의학 … | 동의어일 때 |
| `handoff[{part, axis, stage}]` | 떼어 넘긴 다른 축 | **있으면 kind = D-07, 없으면 D-07 아님**(어긋나면 open) |
| `deferred_stage` | 넘김 단계 | `deferred` 면 필수 |
| `weak` · `question` | 근거 약 · 의료진 질문 | weak 면 질문(비면 틀) |
| `out_of_tree` | 트리 밖 결정 이름 | `out_of_tree[]` 의 `strings` 에 이 키가 있어야 한다 |
| `decided_by` · `note` | 결정 근거(묶음 · 검수 · 사용자) · 메모 | 원천 위치를 적는다 |

실제 행:

```json
{"key": ["팔자주름", "팔자주름"], "destination": "node", "nodes": ["팔자"], "kind": "부위+다른 축(D-07)", "synonym_type": null,
 "handoff": [{"part": "주름", "axis": "고민", "stage": "7단계 고민"}], "deferred_stage": null, "weak": false, "out_of_tree": null, "decided_by": "B3", "note": ""}

{"key": ["코조각주사", "코조각주사"], "destination": "node", "nodes": ["코"], "kind": "부위+다른 축(D-07)", "synonym_type": null,
 "handoff": [{"part": "조각주사", "axis": "계열", "stage": "2단계 계열(지방분해 주사)"}], "deferred_stage": null, "weak": false, "out_of_tree": null,
 "decided_by": "review-step3-v5-report F-1 · 코디 기본값(고객이 부르는 이름대로 코 — 콧망울은 꼬리표 행이 이미 있음)",
 "note": "taxonomy 수액치료 > 지방분해주사(마케팅명) 단위 시술 이름 「코조각주사」 · 꼬리표 「콧망울 지방분해 · 코 라인 날렵하게」"}

{"key": ["브라라인", "브라라인"], "destination": "node", "nodes": ["등"], "kind": "동의어", "synonym_type": "구어", "handoff": [],
 "deferred_stage": null, "weak": false, "out_of_tree": "브라라인", "decided_by": "U1 브라라인 — 등 동의어", "note": "용도 detail 「등 브라라인」 — 등 안의 자리"}

{"key": ["볼/관자놀이", "볼/관자놀이"], "destination": "node", "nodes": ["볼(묶음)", "관자놀이"], "kind": "여러 부위(나열)", "synonym_type": null,
 "handoff": [], "deferred_stage": null, "weak": false, "out_of_tree": null, "decided_by": "B3", "note": "고민 라벨 P11-5"}

{"key": ["하관", "하관"], "destination": "node", "nodes": ["턱(묶음)"], "kind": "동의어", "synonym_type": "구어", "handoff": [],
 "deferred_stage": null, "weak": true, "out_of_tree": "하관", "decided_by": "U1 하관 — 턱(묶음) 동의어", "note": "트리 밖 7 중 하나"}

{"key": ["진피", "조직층"], "destination": "deferred", "nodes": [], "kind": "부위 아님", "synonym_type": null,
 "handoff": [{"part": "층 · 깊이", "axis": "기법", "stage": "4단계 기법"}], "deferred_stage": "4단계 기법", "weak": false, "out_of_tree": null, "decided_by": "B7", "note": "4단계 기법(주입 깊이) 재료"}
```

넘김 22행의 단계(지금): 1단계 제품 8(바디HIFU · 바디써마지 · 바디인모드 · 인모드바디 · 엠페이스 · 튠페이스 · 리쥬란 아이 · 코안면전문 — 이름 전체가 제품 · 장비) · 7단계 고민 6(V라인 · Hair · 모발 · 전신항노화 · 전신재생 · 전체미백) · 4단계 기법 3(진피 · 표피 · 피하) · 5단계 단위 시술 경로 2(IV · 정맥) · 계열 밖(비미용) 1(관절치료) · 2단계 계열 1(모발이식) · 사후관리 문구 1(손톱).

### 1-2. 노드 속성 `nodes{}`

| 칸 | 무엇 | 규칙 |
|---|---|---|
| `anatomical_en` · `anatomical_ko` | 전문의 용어 = **겉자리(체표) 이름만** | 근육 · 뼈 · 혈관 · 신경 이름 금지. 표준 이름이 없으면 비우거나 「상담 용어 + 수준」 — 지어내지 않는다 |
| `anatomical_basis` | 근거 원문 · 출처(레포 파일#칸 · TA2 번호 · KMA 조회일) | |
| `anatomical_level` | 강 · 중 · 약 | 약이면 노드마다 의료진 질문 |
| `danger_zone` · `danger_zone_relation` · `danger_zone_basis` | zone id · 관계(같음 · 상위 묶음 zone · 관련 · 하위가 소유 · 원장 없음) · 근거 | `danger_zone_mapping` 과 맞아야 한다 |
| `name_field_exception` | 이름 칸 근거 0 인 묶음 자리의 이유 | 지금 입가 하나. 없이 근거 0 이면 open |
| `handoff_note` · `anatomical_before_v5{ko, en, level}` | 전문의 용어에서 뺀 근육 · 뼈 → 4단계 메모 · 이전 값 | 지운 값을 남긴다(5 노드) |
| `note` | 메모 | |

실제 값:

```json
"사각턱": {"anatomical_en": "Parotideomasseteric region (regio parotideomasseterica)", "anatomical_ko": "(KMA 표제어 없음 — TA2 이름만)",
  "anatomical_basis": "FIPAT TA2 Part 1(…) 214 Regio parotideomasseterica — 귀밑 · 아래턱 각 바깥 겉자리. KMA 의학용어 6.1판(term.kma.org, 2026-10-28 조회) 「parotideomasseteric」 등록 없음 → 한글 이름 비움",
  "anatomical_level": "약", "danger_zone": "jawline", "danger_zone_relation": "관련(교근 보톡스 경고가 cheek · jawline 두 zone 에)", "danger_zone_basis": "사각턱 전용 zone 없음", "note": "",
  "anatomical_before_v5": {"ko": "아래턱뼈각 · 깨물근", "en": "Mandibular angle · masseter (angulus mandibulae · m. masseter)", "level": "강"},
  "handoff_note": "대상 근육 깨물근(masseter) · 뼈 지표 아래턱뼈각(angulus mandibulae) → 4단계 기법(대상 근육)"}

"콧망울": {"anatomical_en": "Ala of nose (ala nasi)", "anatomical_ko": "콧방울",
  "anatomical_basis": "레포 zones[nose].vessels 「비익(ala) 외측」 · danger 「비익 괴사 위험」 · botox_specific.risk 「비익 함몰(alar collapse)」",
  "anatomical_level": "강", "danger_zone": "nose", "danger_zone_relation": "상위 묶음 zone(비익 괴사 · 함몰 별도 경고)", "danger_zone_basis": "", "note": ""}
```

새 노드는 세 곳에 같이 넣는다: `node_additions[]`(`{name, parent, bundle}`) · `node_ids{}`(`site.<영문>`) · `nodes{}`(위 칸 전부).

## 2. 사전 `step3-lexicon.json`

| 칸 | 무엇 | 규칙 |
|---|---|---|
| `entries[{expr, pattern, case_sensitive, first}]` | 부위 문자열 패턴 251(그중 `#skip:` 39 = 글자 겹침 막기 — 「광대역」 · 「페이스메이커」) | **순서 = 우선순위**(같은 시작 위치면 앞 것) · `first: true` 는 맨 앞. 시작 위치가 같으면 앞 항목이 이기므로 긴 복합어는 짧은 노드 이름 **앞에** 둔다(지금 코필러 120 · 코조각주사 122 < 코 125 · 팔자주름 159 < 팔자 160 · 사각턱보톡스 164 < 사각턱 165) |
| `normalize` | 공백 제거 · 영문 소문자 · 악센트 접기 | |
| `excluded_keys[{suffix, reason}]` | 서지(논문 제목) | |
| `residual{morphemes_ko 171, morpheme_patterns_ko 1, stems_en 165, allowed[13 무리 · 421 낱말], allowed_patterns 4, sources}` | 사전 밖 부위 형태소 잔여 검사(**이름 칸에만**) · 글자 겹침 허용 | 허용 목록에 부위 문자열을 넣지 않는다(코조각주사) |

실제 항목 — 낱말 경계를 보는 꼴:

```json
{"expr": "코", "pattern": "(?<![가-힣])코(?=$|[\\s/·,.)(]|가|에|의|를|는|와|로|,)", "case_sensitive": false, "first": false}
{"expr": "입술", "pattern": "(?<!흡)입술|윗입술|상구순|상순|하순|구순(?!포진|염)|[Vv]ermill?ion|\\b[Ll]ips?\\b|[Ll]ip flip|구륜근|[Oo]rbicularis oris", "case_sensitive": false, "first": false}
{"expr": "브라라인", "pattern": "브라라인|브래지어 라인|브라 라인", "case_sensitive": false, "first": false}
{"expr": "코조각주사", "pattern": "코 ?조각주사", "case_sensitive": false, "first": false}
```

## 3. 원장 `step3-sites.json`(스크립트 출력 — 손으로 고치지 않는다)

| 칸 | 무엇 |
|---|---|
| `summary` | 원천(파일 21 · 문자열 칸 22,749 · 이름 칸 1,953) · 노드 53(트리 37 · OQ-206 6 · 3단계 10) · 문자열 176 · 등장 440 · 노드로 154(394회 · 동의어 칸 77 · 부위+다른 축 칸 82 — **칸 수**, 행 수 아님) · 넘김 22(46회) · open 0 · stale 0 · 근거 약 4 · 해부학 수준 강 20 · 중 4 · 약 29 · 의료진 질문 35 |
| `nodes[]` | 노드 53 — `id · name · parent · status · synonyms[] · compound_strings[]{handoff} · anatomical_name{en, ko, basis, level} · danger_zone{} · source{strings, count, count_name_fields} · name_field_exception · handoff_note · anatomical_before_v5 · weak_strings` |
| `strings[]` | 결정 칸 + 재추출 칸(`string` 대표형 · `normalized` · `group` · `count` · `count_name_fields` · `variants` · `by_file` · `name_field_samples[]` · `prose_samples[]`) |
| `deferred[]` · `open[]` · `stale_decisions[]` · `doctor_questions[]` | 넘김 22 · open(**끝 조건 = 빈 목록**) · 원천에 없는 결정 · 질문 35 |
| `changes[]` · `boundary_rules[]` · `danger_zone_mapping[]` | 결정 파일 그대로 |

open 종류(`step3-apply.py` 가드): 결정 없는 문자열 · 사전 밖 부위 형태소 · 행선지 오류(nodes 없음 · deferred 단계 없음 · handoff ⇔ kind · 트리 밖 결정과 안 맞음) · 트리 밖 결정 문자열에 행선지 없음 · 해부학 이름 후보 없음 · 원천 문자열 0(노드) · 위험 부위 대응 불일치 · 조사 판 근거 약이 결정에서 빠짐.
