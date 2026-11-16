# 시맨틱 규칙 — 결정 B1 ~ B12 · U1 ~ U3 와 정본 칸

결정 정본: `_RESUME.md` §2 10-29 「시맨틱 조사 반영 — 추천대로」(사용자 「응 그렇게 가자」). 조사 `semantic-research.md` §9 · §10. 정본 칸은 `semantic.json`.
셈은 여기 적지 않는다 — `check_semantic.py` 출력이 지금 값이다.

## 1. 결정 묶음 → 정본 자리

| id | 정한 것 | 실버가 바뀌었나 | 정본 · 실버 자리 |
|---|---|---|---|
| B1 | 합병증 노드 = severity moderate 이상만 · mild = 부작용(계열 속성) · 근거 문장 adverse_effects 중 부작용 · 색소는 부작용 근거, 드문 · 중대는 합병증 근거 | 예 — `step8-decisions` → `step8-apply` | `step8 safety.complications` · `side_effects` · semantic `attributes_not_nodes`(부작용) |
| B2 | 근거 문장 field(원천 칸)는 그대로 · class 를 시맨틱에 · 칸과 뜻이 다른 문장 = 원천 수정 후보 | 아니오 | semantic `statements`(by_class · table · source_fix) |
| B3 | 끝점 묶음 = 노드 아님 → 엣지 칸 `endpoints.a\|b{kind, id, qualifier, candidates[]}` · a · b 문자열은 그대로(뒤 호환) | 예 — 8단계 | `step8 edges[].endpoints` · semantic `not_edges` set_member |
| B4 | 엣지 종류 32 → 21(합침 9묶음 · 상위/관련 나눔 1 · 저장 엣지 아님 2 · 새로 1 라인 품목) | 아니오 | semantic `edge_kinds` · `not_edges` |
| B5 | 사전 하나 — 표현 행 + targets[] + qualifier · 7 · 8단계 수준 차이는 qualifier · 단위 시술 펼치기는 상속 I2 · I3 | 아니오(7단계 「비타민C」 충돌은 보고만) | semantic `dictionary` |
| B6 | 정본 id = `{종류}:{키}` · 실버 id 는 그대로 · 대응표 | 아니오 | semantic `ids` |
| B7 | 상속은 저장 안 함 · 골드 계산 · 실버는 붙는 수준만 | 아니오 | semantic `inheritance` |
| B8 | 확인 조건 주장 중 상담 · 시술 준비 · 고지 · 사람/연령 조건 아닌 것 = 엣지 아님 → `conditions.not_condition` · 계열 원문 속성 | 예 — 8단계 | `step8 conditions.not_condition` · semantic `reading.not_condition` |
| B9 | 업체 = 노드(DEC-003 제조사 원장 — 세우기는 적재 때) · 허가 · 규격 = 제품 속성 | 아니오 | semantic `attributes_not_nodes` |
| B10 | 그림 밖 52 중 목적 앵커 18 은 목적 id 로 그림 안 · 나머지는 결정대로 앵커 없음(J5 · J9) | 아니오 | semantic `ids.silver_string_map` |
| B11 | 특수 부위 「해당 없음」 · 「병변 단위」 = 부위 노드 아님 · key.site 값 + 표시 | 아니오 | semantic key_site(특수 부위 엣지 없음) |
| B12 | gate_status 3값 공통 · 「미확인」은 표시 · 표시 12 하나로 | 아니오 | semantic `reading.flags` · `reading.gate_status` |
| U1 | 합병증 gap 17 중 원천 안 문장(taxonomy modality extracted.safety)이 있는 7계열 먼저 — serious → 합병증 · common · uncommon → 부작용 · 남는 gap 유지 · 문헌 조사는 안 함 | 예 — 8단계 | `step8 safety.complications`(`CX-{계열}-T{n}`) · `side_effects` · `complication_gap_families` |
| U2 | 부작용 = 계열 속성 + 제품 × 계열 · 단위 시술 값 덮어씀(골드 계산) | 예 — 8단계 | `step8 safety.side_effects` · `side_effect_rule` · 상속 I8 |
| U3 | 끝점 묶음 = 엣지 칸 candidates[] | 예 — 8단계(B3) | 위 B3 |

## 2. 엣지 종류 합침 · 나눔의 기준

- **같은 뜻이면 합친다** — 주/보조 · 기본/함께 · 확정/슬롯 후보 같은 것은 속성(role · status)
- **이름이 같아도 칸이 다르면 나눈다** — 제품 → 계열(`product_family`)은 판정(verdict · evidence_level · conflict 칸) · 단위 시술 → 계열(`key_family`)은 정체 칸(하나뿐 · 바뀌면 다른 단위 시술)
- **상하와 옆은 다르다** — 고민 트리 상위(`child_of`) · 상위 없는 결정 노드가 걸친 고민(`concern_related` · 방향 없음)
- **출처 3종은 한 뜻**(`cites`) · 관계 주장의 출처는 엣지가 아니라 주장 칸 `claims[].evidence`
- **계산 결과는 저장 엣지가 아니다** — 상속 후보(`prod_unit_inh`) · 끝점 묶음 원소(`set_member`)

## 3. 사전 겹침 갈래

| 갈래 | 뜻 | mode |
|---|---|---|
| A | 묶음 이름 → 고민 · 목적 여럿(R12) | 전부 |
| B | 장비 · 제품 이름 = 단위 시술 동의어(10-27) | 후보 |
| C | 브랜드 이름이 계열 낱말로도(「보톡스」 = 계열 · 제품) | 후보 |
| D | 같은 검색 이름이 제품 둘(라인 · 같은 허가) | 후보 |
| E | 같은 말이 단위 시술 여럿 | 후보 |
| F | 7 · 8단계 수준 차이 — **겹침 아님** · qualifier 로 합침(`level_merged`) | — |
| G | 부위 이름 = 단위 시술 원장 이름(「사각턱」) | 후보 |
| H | 기법 이름 = 단위 시술 이름(서브시전 · 펀치 · 압출) | 후보 |
| I | 나열 문자열이 부위 둘(「볼/관자놀이」) | 전부 |
| J | 종류가 다른 노드끼리 · 고민 이름이 시술 동의어 칸에 든 것은 고민 우선(7단계 W3) | 후보 |

`check_semantic.py` 는 갈래 이름은 안 보고 구조만 본다 — 대상 여럿 ⇔ collision 있음 · 하나 ⇔ mode 하나 · 후보 ⇔ ambiguous · 대상 id 가 대응표에 있음.

## 4. id 대응

- 13종 전부 `ids.map` 행(정본 id · 종류 · 실버 id · 이름). 실버 개체 목록은 `check_semantic.py` `silver_objects` 가 실버에서 따로 뽑는다 — 제품 = active 행만 · 고민 = 대분류 · 중분류 node + 항목 kind 「고민」 + extra_items · 목적 = purposes[] node
- 키가 다른 것 허용: 고민 `J{n}-{한글}` → `concern:J{n}` · 목적 이름 → `purpose:PU-{nn}`
- 7단계 엣지 from 의 「목적:{이름}」 은 `silver_string_map`(고민과 같은 말인 목적은 고민 id 로 — R6), 「J{n}-{한글}」 은 실버 id 그대로 대응표에

## 5. 상속 9 — 실버 칸

정본 문장은 `semantic.json` `inheritance[]`(id · name · rule · fields · count · stored_now). 점검은 구조 · 불변식만 본다:
- I1 — 상속 표시 엣지의 끝에 family
- I5 — site_check 셈 = 7단계 edges[].site_check 재셈(7단계 부위 규칙 R21 · R22 가 바뀌면 같이 바뀜)
- I9 — gap 계열 ⊂ 계열 목록 · gap 계열에 합병증 노드 0 · 전부 mild 계열은 `complication_mild_only_families`
- B1 — 합병증 severity ∈ {moderate, severe, critical} 또는 원문 serious(T 번호) · 부작용에 moderate 이상 0
- B8 — 확인 조건 주장 kind 에 「…항목」 0
