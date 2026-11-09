# treatment-optimization.json — 1차 조사 review-part-1

> 원문 값 표는 build.py 가 원본에서 자동 생성했다. 잠정 관찰·수동 구절은 manual/seg-XX.json 의 직접 읽기 기록이다. 원장의 임상·규제 서술은 **원장에 적혀 있다는 사실**로만 기록했고 검증·보충하지 않았다.
> 상태 기호: P 잠정 · B 원문 정보 부족 · I 원문 내 불일치 후보 · F 후속 의미 조사 · K 알려진 분석 한계 · A 에이전트 추출 오류 · C 사용자 결정 필요.

[← 목차 review.md](./review.md)

<a id="seg-00"></a>
## SEG-00 — 상위 메타·원칙

- 직접 읽기: **direct_read_done** — 루트 객체 키 순서 8개, /version /updated /consensus_method /optimization_principles 4원소, 네 블록 배열 길이(8·4·8·3)를 원문 한 줄에서 직접 읽음
- 소유 노드 13 · 말단(빈 컨테이너 포함) 7

### 원문 값 (자동 생성 · 원본 컬럼명 그대로 · 원본 순서)

| Pointer | 원본 컬럼명 | 자료형 | 원문 값 |
|---|---|---|---|
| `` | `(root)` | object(8) | _키: version, updated, consensus_method, optimization_principles, by_concern, by_age_group, combination_rules, annual_plans_ |
| `/version` | `version` | string | "1.4" |
| `/updated` | `updated` | string | "2026-07-26" |
| `/consensus_method` | `consensus_method` | string | "3-AI Expert Panel Consensus (Perplexity+Gemini+Claude)" |
| `/optimization_principles` | `optimization_principles` | array(4) | _원소 4개_ |
| `/optimization_principles/0` | `optimization_principles[0]` | string | "안전성 우선 (Do No Harm)" |
| `/optimization_principles/1` | `optimization_principles[1]` | string | "시너지 극대화 (상호 보완 효과)" |
| `/optimization_principles/2` | `optimization_principles[2]` | string | "다운타임 최소화 (환자 편의)" |
| `/optimization_principles/3` | `optimization_principles[3]` | string | "비용 효율성 고려" |
| `/by_concern` | `by_concern` | array(8) | _원소 8개_ |
| `/by_age_group` | `by_age_group` | array(4) | _원소 4개_ |
| `/combination_rules` | `combination_rules` | array(8) | _원소 8개_ |
| `/annual_plans` | `annual_plans` | array(3) | _원소 3개_ |

### 잠정 관찰 (직접 읽기 · 원문 칸과 분리 · 확정 의미 아님)

| ID | 상태 | 근거 Pointer | 관찰 |
|---|---|---|---|
| O00-1 | P | `/consensus_method` | consensus_method 의 `+` 는 AI 도구 이름(Perplexity·Gemini·Claude)을 잇는다. README 의 `+`(함께 시술) 규칙과 다른 쓰임이다. 이 값은 합의 방법 서술이며 각 추천 문구의 출처 검증 정보는 아니다. |
| O00-2 | P | `/optimization_principles/0`<br>`/optimization_principles/1`<br>`/optimization_principles/2`<br>`/optimization_principles/3` | 원칙 4개 중 3개가 「한국어 표제 (괄호 보충)」 형식이고 0번의 괄호는 영어(Do No Harm), 1·2번은 한국어 보충, 3번은 괄호 없음. 괄호가 번역·목적·보충을 섞어 담는다. |
| O00-3 | B | `/optimization_principles` | 배열 순서가 우선순위인지 원문에 없다(「우선」은 0번 문구 안에만 있음). 원칙들이 아래 by_concern·combination_rules 의 어느 값에 적용되는지 연결 정보가 없다. |

### 수동 수집 구절 (9건 · 구간은 expressions.json `source=manual_direct_reading`)

| Pointer | 원문 구절 | 탐색 관점(kinds) |
|---|---|---|
| `/consensus_method` | 3-AI Expert Panel Consensus | quantity_unit, language_en, source_method |
| `/consensus_method` | (Perplexity+Gemini+Claude) | parenthetical, plus_non_procedure, language_en |
| `/optimization_principles/0` | 안전성 우선 | priority_preference |
| `/optimization_principles/0` | (Do No Harm) | parenthetical, language_en, negation |
| `/optimization_principles/1` | 시너지 극대화 | degree_modifier, effect_complement |
| `/optimization_principles/1` | (상호 보완 효과) | parenthetical, effect_complement |
| `/optimization_principles/2` | 다운타임 최소화 | degree_modifier, downtime |
| `/optimization_principles/2` | (환자 편의) | parenthetical, purpose |
| `/optimization_principles/3` | 비용 효율성 고려 | cost, consideration |

### 이 구획의 미결 (issues.md 에 모음)

- **B-00-1** [B] 원칙 배열 순서의 의미(우선순위 여부)와 적용 대상 연결이 원문에 없다. 원칙별 가중·충돌 시 처리 규칙을 원장만으로 정할 수 없다. — `/optimization_principles`

<a id="seg-01"></a>
## SEG-01 — by_concern/0

- 직접 읽기: **direct_read_done** — /by_concern/0 (주름 개선) concern·concern_en·icon 과 severity_levels 3단계의 모든 필드·배열 원소를 원문 순서로 직접 읽음
- 소유 노드 42 · 말단(빈 컨테이너 포함) 33

### 원문 값 (자동 생성 · 원본 컬럼명 그대로 · 원본 순서)

| Pointer | 원본 컬럼명 | 자료형 | 원문 값 |
|---|---|---|---|
| `/by_concern/0` | `by_concern[0]` | object(4) | _키: concern, concern_en, icon, severity_levels_ |
| `/by_concern/0/concern` | `concern` | string | "주름 개선" |
| `/by_concern/0/concern_en` | `concern_en` | string | "Wrinkle Reduction" |
| `/by_concern/0/icon` | `icon` | string | "wrinkle" |
| `/by_concern/0/severity_levels` | `severity_levels` | array(3) | _원소 3개_ |
| `/by_concern/0/severity_levels/0` | `severity_levels[0]` | object(8) | _키: level, optimal_combo, sequence, rationale, expected_sessions, total_duration, evidence_level, contraindicated_combos_ |
| `/by_concern/0/severity_levels/0/level` | `level` | string | "경미 (fine lines)" |
| `/by_concern/0/severity_levels/0/optimal_combo` | `optimal_combo` | array(2) | _원소 2개_ |
| `/by_concern/0/severity_levels/0/optimal_combo/0` | `optimal_combo[0]` | string | "레이저토닝" |
| `/by_concern/0/severity_levels/0/optimal_combo/1` | `optimal_combo[1]` | string | "스킨부스터(리쥬란)" |
| `/by_concern/0/severity_levels/0/sequence` | `sequence` | string | "토닝 먼저 → 2주 후 스킨부스터" |
| `/by_concern/0/severity_levels/0/rationale` | `rationale` | string | "토닝으로 표피 리뉴얼 후 스킨부스터로 진피 재생" |
| `/by_concern/0/severity_levels/0/expected_sessions` | `expected_sessions` | string | "토닝 5-10회 + 스킨부스터 3회" |
| `/by_concern/0/severity_levels/0/total_duration` | `total_duration` | string | "3-6개월" |
| `/by_concern/0/severity_levels/0/evidence_level` | `evidence_level` | string | "moderate" |
| `/by_concern/0/severity_levels/0/contraindicated_combos` | `contraindicated_combos` | array(0) | _[]_ |
| `/by_concern/0/severity_levels/1` | `severity_levels[1]` | object(8) | _키: level, optimal_combo, sequence, rationale, expected_sessions, total_duration, evidence_level, contraindicated_combos_ |
| `/by_concern/0/severity_levels/1/level` | `level` | string | "중등도 (moderate wrinkles)" |
| `/by_concern/0/severity_levels/1/optimal_combo` | `optimal_combo` | array(3) | _원소 3개_ |
| `/by_concern/0/severity_levels/1/optimal_combo/0` | `optimal_combo[0]` | string | "보톡스" |
| `/by_concern/0/severity_levels/1/optimal_combo/1` | `optimal_combo[1]` | string | "필러" |
| `/by_concern/0/severity_levels/1/optimal_combo/2` | `optimal_combo[2]` | string | "스킨부스터" |
| `/by_concern/0/severity_levels/1/sequence` | `sequence` | string | "같은날: 필러→스킨부스터→보톡스. 또는 보톡스 먼저 → 2주 후 필러" |
| `/by_concern/0/severity_levels/1/rationale` | `rationale` | string | "보톡스(동적주름) + 필러(정적주름/볼륨) + 스킨부스터(피부결)" |
| `/by_concern/0/severity_levels/1/expected_sessions` | `expected_sessions` | string | "보톡스 1회 + 필러 1회 + 스킨부스터 3회" |
| `/by_concern/0/severity_levels/1/total_duration` | `total_duration` | string | "2-4개월" |
| `/by_concern/0/severity_levels/1/evidence_level` | `evidence_level` | string | "high" |
| `/by_concern/0/severity_levels/1/contraindicated_combos` | `contraindicated_combos` | array(0) | _[]_ |
| `/by_concern/0/severity_levels/2` | `severity_levels[2]` | object(8) | _키: level, optimal_combo, sequence, rationale, expected_sessions, total_duration, evidence_level, contraindicated_combos_ |
| `/by_concern/0/severity_levels/2/level` | `level` | string | "중증 (deep wrinkles)" |
| `/by_concern/0/severity_levels/2/optimal_combo` | `optimal_combo` | array(4) | _원소 4개_ |
| `/by_concern/0/severity_levels/2/optimal_combo/0` | `optimal_combo[0]` | string | "보톡스" |
| `/by_concern/0/severity_levels/2/optimal_combo/1` | `optimal_combo[1]` | string | "필러" |
| `/by_concern/0/severity_levels/2/optimal_combo/2` | `optimal_combo[2]` | string | "HIFU/RF" |
| `/by_concern/0/severity_levels/2/optimal_combo/3` | `optimal_combo[3]` | string | "스킨부스터" |
| `/by_concern/0/severity_levels/2/sequence` | `sequence` | string | "HIFU/RF 먼저 → 보톡스(같은날 가능) → 2주 후 필러 → 스킨부스터" |
| `/by_concern/0/severity_levels/2/rationale` | `rationale` | string | "HIFU로 SMAS 리프팅 → 보톡스로 동적주름 → 필러로 볼륨/깊은주름 → 스킨부스터로 피부결" |
| `/by_concern/0/severity_levels/2/expected_sessions` | `expected_sessions` | string | "HIFU 1-2회 + 보톡스 1회 + 필러 1-2회 + 스킨부스터 3회" |
| `/by_concern/0/severity_levels/2/total_duration` | `total_duration` | string | "3-6개월" |
| `/by_concern/0/severity_levels/2/evidence_level` | `evidence_level` | string | "high" |
| `/by_concern/0/severity_levels/2/contraindicated_combos` | `contraindicated_combos` | array(1) | _원소 1개_ |
| `/by_concern/0/severity_levels/2/contraindicated_combos/0` | `contraindicated_combos[0]` | string | "HA 필러 후 14일 이내 RF/HIFU 금지" |

### 잠정 관찰 (직접 읽기 · 원문 칸과 분리 · 확정 의미 아님)

| ID | 상태 | 근거 Pointer | 관찰 |
|---|---|---|---|
| O01-1 | P | `/by_concern/0/severity_levels/0/level`<br>`/by_concern/0/severity_levels/1/level`<br>`/by_concern/0/severity_levels/2/level` | level 은 「한국어 단계명 (영어 보충)」 형식(경미/중등도/중증 + fine lines/moderate wrinkles/deep wrinkles). 단계 기준(무엇으로 경미·중증을 가르나)은 원문에 없다. |
| O01-2 | F | `/by_concern/0/severity_levels/0/optimal_combo/0`<br>`/by_concern/0/severity_levels/0/sequence`<br>`/by_concern/0/severity_levels/0/expected_sessions` | optimal_combo 는 「레이저토닝」, sequence·expected_sessions·rationale 은 「토닝」으로 줄여 부른다. 같은 대상을 가리키는지는 문맥상 그럴듯하나 원문 표기만으로 연결하지 않았다. |
| O01-3 | P | `/by_concern/0/severity_levels/0/optimal_combo/1` | 「스킨부스터(리쥬란)」의 괄호는 README 「괄호 안 대안은 예시」 형식과 같은 꼴이나, 리쥬란이 유일 예시인지 고정 제품인지는 원문에 없다. |
| O01-4 | P | `/by_concern/0/severity_levels/1/sequence` | sequence 하나에 두 안이 「또는」으로 나뉜다: (가) 같은날 필러→스킨부스터→보톡스, (나) 보톡스 먼저 → 2주 후 필러. (나)에는 스킨부스터가 빠져 있다. 「.」로 두 문장을 가른다. 화살표 앞뒤 공백 유무가 섞인다. |
| O01-5 | P | `/by_concern/0/severity_levels/1/rationale` | rationale 의 괄호는 제품 예시가 아니라 각 시술이 겨냥하는 대상(동적주름·정적주름/볼륨·피부결)이다. 같은 원장 안에서 괄호의 역할이 필드마다 다르다. 「정적주름/볼륨」의 `/` 는 대안이 아니라 대상 나열로 읽힌다(잠정). |
| O01-6 | P | `/by_concern/0/severity_levels/0/expected_sessions`<br>`/by_concern/0/severity_levels/1/expected_sessions`<br>`/by_concern/0/severity_levels/2/expected_sessions` | expected_sessions 의 `+` 는 시술별 회차를 잇는 나열이다. 같은 날 함께 한다는 뜻인지 README `+`(함께 시술)와 같은 뜻인지는 원문에 없다. 회차 범위 「5-10회」「1-2회」는 하이픈 범위. |
| O01-7 | B | `/by_concern/0/severity_levels/2/sequence` | 「HIFU/RF 먼저 → 보톡스(같은날 가능) → 2주 후 필러 → 스킨부스터」: 보톡스는 같은날 「가능」(필수 아님), 필러는 2주 후, 스킨부스터는 간격이 적혀 있지 않다. 「2주 후」의 기준점이 HIFU/RF 인지 보톡스인지 원문에 없다. |
| O01-8 | P | `/by_concern/0/severity_levels/2/contraindicated_combos/0`<br>`/by_concern/0/severity_levels/2/sequence` | 금지 「HA 필러 후 14일 이내 RF/HIFU 금지」는 순서(필러 후)·기간(14일 이내)·대상(RF/HIFU)·금지를 한 문장에 담는다. 같은 단계 sequence 는 HIFU/RF 를 필러보다 먼저 두어 금지 방향과 충돌하지 않는다. optimal_combo 는 「필러」라고만 쓰므로 그 필러가 HA 인지는 원문에 없다(B). 「2주」와 「14일」을 같은 값으로 환산하지 않았다. |
| O01-9 | P | `/by_concern/0/severity_levels/2/rationale` | rationale 은 HIFU 만 언급(「HIFU로 SMAS 리프팅」)하고 optimal_combo 의 「HIFU/RF」 중 RF 의 역할은 적지 않았다. |
| O01-10 | B | `/by_concern/0/severity_levels/0/contraindicated_combos`<br>`/by_concern/0/severity_levels/1/contraindicated_combos` | 빈 배열 []: 금지 조합이 없다는 뜻인지, 기록하지 않았다는 뜻인지 원문에 없다. |
| O01-11 | B | `/by_concern/0/severity_levels/0/evidence_level`<br>`/by_concern/0/severity_levels/1/evidence_level`<br>`/by_concern/0/severity_levels/2/evidence_level` | evidence_level(moderate·high) 은 단계 전체에 대한 값이다. 어느 근거·어떤 등급 체계인지, 조합 중 어느 부분에 대한 등급인지 원문에 없다. |

### 수동 수집 구절 (26건 · 구간은 expressions.json `source=manual_direct_reading`)

| Pointer | 원문 구절 | 탐색 관점(kinds) |
|---|---|---|
| `/by_concern/0/severity_levels/0/level` | (fine lines) | parenthetical, language_en, severity |
| `/by_concern/0/severity_levels/0/optimal_combo/1` | 스킨부스터(리쥬란) | procedure_like, product_like, parenthetical |
| `/by_concern/0/severity_levels/0/sequence` | 토닝 먼저 | order_sequence |
| `/by_concern/0/severity_levels/0/sequence` | 2주 후 스킨부스터 | interval_after, time |
| `/by_concern/0/severity_levels/0/rationale` | 토닝으로 표피 리뉴얼 후 | effect_purpose, layer_depth, order_sequence |
| `/by_concern/0/severity_levels/0/rationale` | 스킨부스터로 진피 재생 | effect_purpose, layer_depth |
| `/by_concern/0/severity_levels/0/expected_sessions` | 토닝 5-10회 | session_count, range |
| `/by_concern/0/severity_levels/0/total_duration` | 3-6개월 | time, range |
| `/by_concern/0/severity_levels/1/level` | (moderate wrinkles) | parenthetical, language_en, severity |
| `/by_concern/0/severity_levels/1/sequence` | 같은날: 필러→스킨부스터→보톡스 | same_day, order_sequence |
| `/by_concern/0/severity_levels/1/sequence` | 또는 보톡스 먼저 → 2주 후 필러 | alternative, order_sequence, interval_after |
| `/by_concern/0/severity_levels/1/rationale` | 보톡스(동적주름) | parenthetical, target_concern |
| `/by_concern/0/severity_levels/1/rationale` | 필러(정적주름/볼륨) | parenthetical, target_concern, slash_non_alternative |
| `/by_concern/0/severity_levels/1/rationale` | 스킨부스터(피부결) | parenthetical, target_concern |
| `/by_concern/0/severity_levels/1/total_duration` | 2-4개월 | time, range |
| `/by_concern/0/severity_levels/2/level` | (deep wrinkles) | parenthetical, language_en, severity, layer_depth |
| `/by_concern/0/severity_levels/2/sequence` | HIFU/RF 먼저 | alternative, order_sequence |
| `/by_concern/0/severity_levels/2/sequence` | 보톡스(같은날 가능) | same_day, possibility, parenthetical |
| `/by_concern/0/severity_levels/2/sequence` | 2주 후 필러 | interval_after, time |
| `/by_concern/0/severity_levels/2/sequence` | → 스킨부스터 | order_sequence, interval_unspecified |
| `/by_concern/0/severity_levels/2/rationale` | HIFU로 SMAS 리프팅 | effect_purpose, layer_depth, language_mixed |
| `/by_concern/0/severity_levels/2/rationale` | 필러로 볼륨/깊은주름 | effect_purpose, degree_modifier, slash_non_alternative |
| `/by_concern/0/severity_levels/2/expected_sessions` | HIFU 1-2회 | session_count, range |
| `/by_concern/0/severity_levels/2/expected_sessions` | 필러 1-2회 | session_count, range |
| `/by_concern/0/severity_levels/2/contraindicated_combos/0` | HA 필러 후 14일 이내 RF/HIFU 금지 | avoid_prohibit, interval_within, order_sequence, time, alternative |
| `/by_concern/0/severity_levels/2/contraindicated_combos/0` | 14일 이내 | interval_within, range, time |

### 이 구획의 미결 (issues.md 에 모음)

- **B-01-1** [B] 「2주 후 필러」의 기준 시점과 스킨부스터의 간격이 원문에 없다. — `/by_concern/0/severity_levels/2/sequence`
- **B-01-2** [B] optimal_combo 「필러」가 금지 문구의 「HA 필러」와 같은지 원문에 없다. — `/by_concern/0/severity_levels/2/optimal_combo/2`, `/by_concern/0/severity_levels/2/contraindicated_combos/0`

<a id="seg-02"></a>
## SEG-02 — by_concern/1

- 직접 읽기: **direct_read_done** — /by_concern/1 (처짐/탄력) 전체 필드와 severity_levels 3단계를 원문 순서로 직접 읽음
- 소유 노드 42 · 말단(빈 컨테이너 포함) 33

### 원문 값 (자동 생성 · 원본 컬럼명 그대로 · 원본 순서)

| Pointer | 원본 컬럼명 | 자료형 | 원문 값 |
|---|---|---|---|
| `/by_concern/1` | `by_concern[1]` | object(4) | _키: concern, concern_en, icon, severity_levels_ |
| `/by_concern/1/concern` | `concern` | string | "처짐/탄력" |
| `/by_concern/1/concern_en` | `concern_en` | string | "Sagging / Elasticity" |
| `/by_concern/1/icon` | `icon` | string | "lifting" |
| `/by_concern/1/severity_levels` | `severity_levels` | array(3) | _원소 3개_ |
| `/by_concern/1/severity_levels/0` | `severity_levels[0]` | object(8) | _키: level, optimal_combo, sequence, rationale, expected_sessions, total_duration, evidence_level, contraindicated_combos_ |
| `/by_concern/1/severity_levels/0/level` | `level` | string | "경미 (초기 처짐)" |
| `/by_concern/1/severity_levels/0/optimal_combo` | `optimal_combo` | array(2) | _원소 2개_ |
| `/by_concern/1/severity_levels/0/optimal_combo/0` | `optimal_combo[0]` | string | "써마지/RF" |
| `/by_concern/1/severity_levels/0/optimal_combo/1` | `optimal_combo[1]` | string | "스킨부스터" |
| `/by_concern/1/severity_levels/0/sequence` | `sequence` | string | "RF 시술 → 2주 후 스킨부스터" |
| `/by_concern/1/severity_levels/0/rationale` | `rationale` | string | "RF로 콜라겐 리모델링 + 스킨부스터로 진피 수분/탄력 보충" |
| `/by_concern/1/severity_levels/0/expected_sessions` | `expected_sessions` | string | "RF 1-2회 + 스킨부스터 3회" |
| `/by_concern/1/severity_levels/0/total_duration` | `total_duration` | string | "3-4개월" |
| `/by_concern/1/severity_levels/0/evidence_level` | `evidence_level` | string | "moderate" |
| `/by_concern/1/severity_levels/0/contraindicated_combos` | `contraindicated_combos` | array(0) | _[]_ |
| `/by_concern/1/severity_levels/1` | `severity_levels[1]` | object(8) | _키: level, optimal_combo, sequence, rationale, expected_sessions, total_duration, evidence_level, contraindicated_combos_ |
| `/by_concern/1/severity_levels/1/level` | `level` | string | "중등도 (눈에 띄는 처짐)" |
| `/by_concern/1/severity_levels/1/optimal_combo` | `optimal_combo` | array(3) | _원소 3개_ |
| `/by_concern/1/severity_levels/1/optimal_combo/0` | `optimal_combo[0]` | string | "HIFU(슈링크/울쎄라)" |
| `/by_concern/1/severity_levels/1/optimal_combo/1` | `optimal_combo[1]` | string | "보톡스(턱선+광대)" |
| `/by_concern/1/severity_levels/1/optimal_combo/2` | `optimal_combo[2]` | string | "바이오스티뮬레이터" |
| `/by_concern/1/severity_levels/1/sequence` | `sequence` | string | "HIFU 먼저 → 같은날 보톡스 가능 → 4주 후 바이오스티뮬레이터 시작" |
| `/by_concern/1/severity_levels/1/rationale` | `rationale` | string | "HIFU로 SMAS 수축 → 보톡스로 근육 이완(턱선 슬림) → 바이오스티뮬로 콜라겐 장기 재생" |
| `/by_concern/1/severity_levels/1/expected_sessions` | `expected_sessions` | string | "HIFU 1-2회 + 보톡스 1회 + 바이오스티뮬 3-4회" |
| `/by_concern/1/severity_levels/1/total_duration` | `total_duration` | string | "4-8개월" |
| `/by_concern/1/severity_levels/1/evidence_level` | `evidence_level` | string | "high" |
| `/by_concern/1/severity_levels/1/contraindicated_combos` | `contraindicated_combos` | array(0) | _[]_ |
| `/by_concern/1/severity_levels/2` | `severity_levels[2]` | object(8) | _키: level, optimal_combo, sequence, rationale, expected_sessions, total_duration, evidence_level, contraindicated_combos_ |
| `/by_concern/1/severity_levels/2/level` | `level` | string | "중증 (뚜렷한 처짐)" |
| `/by_concern/1/severity_levels/2/optimal_combo` | `optimal_combo` | array(4) | _원소 4개_ |
| `/by_concern/1/severity_levels/2/optimal_combo/0` | `optimal_combo[0]` | string | "울쎄라 HIFU" |
| `/by_concern/1/severity_levels/2/optimal_combo/1` | `optimal_combo[1]` | string | "실리프팅(PDO/PCL)" |
| `/by_concern/1/severity_levels/2/optimal_combo/2` | `optimal_combo[2]` | string | "필러" |
| `/by_concern/1/severity_levels/2/optimal_combo/3` | `optimal_combo[3]` | string | "바이오스티뮬레이터" |
| `/by_concern/1/severity_levels/2/sequence` | `sequence` | string | "울쎄라 HIFU → 2-4주 후 실리프팅 → 필러(볼륨 보충) → 바이오스티뮬레이터(유지)" |
| `/by_concern/1/severity_levels/2/rationale` | `rationale` | string | "HIFU로 깊은층 수축 → 실리프팅으로 물리적 거상 → 필러로 볼륨 → 바이오스티뮬로 장기 유지" |
| `/by_concern/1/severity_levels/2/expected_sessions` | `expected_sessions` | string | "HIFU 1회 + 실리프팅 1회 + 필러 1회 + 바이오스티뮬 3회" |
| `/by_concern/1/severity_levels/2/total_duration` | `total_duration` | string | "6-12개월" |
| `/by_concern/1/severity_levels/2/evidence_level` | `evidence_level` | string | "moderate" |
| `/by_concern/1/severity_levels/2/contraindicated_combos` | `contraindicated_combos` | array(1) | _원소 1개_ |
| `/by_concern/1/severity_levels/2/contraindicated_combos/0` | `contraindicated_combos[0]` | string | "PDO실 + 비가교HA 동시 금지" |

### 잠정 관찰 (직접 읽기 · 원문 칸과 분리 · 확정 의미 아님)

| ID | 상태 | 근거 Pointer | 관찰 |
|---|---|---|---|
| O02-1 | P | `/by_concern/1/concern`<br>`/by_concern/1/concern_en` | concern 「처짐/탄력」, concern_en 「Sagging / Elasticity」: `/` 가 시술 대안이 아니라 고민 두 개를 묶는다. 영어 쪽은 `/` 앞뒤 공백이 있다. |
| O02-2 | F | `/by_concern/1/severity_levels/0/optimal_combo/0`<br>`/by_concern/1/severity_levels/0/sequence` | 「써마지/RF」는 장비명과 계열명을 `/` 로 잇는다. README `/`(둘 중 하나)로 읽을지 동격(써마지=RF 장비)으로 읽을지 원문만으로 정하지 않았다. sequence 는 「RF 시술」로만 부른다. |
| O02-3 | P | `/by_concern/1/severity_levels/1/optimal_combo/0`<br>`/by_concern/1/severity_levels/1/optimal_combo/1` | 「HIFU(슈링크/울쎄라)」는 README 예시와 같은 꼴(괄호 = 장비 예시, `/` = 둘 중 하나). 「보톡스(턱선+광대)」의 괄호는 부위이고 `+` 는 부위 나열(README 「부위 나열은 +」와 같은 꼴). |
| O02-4 | P | `/by_concern/1/severity_levels/1/sequence` | 「HIFU 먼저 → 같은날 보톡스 가능 → 4주 후 바이오스티뮬레이터 시작」: 같은날은 가능(선택), 4주 후는 시리즈 「시작」 시점. 4주의 기준이 HIFU 인지 원문 위치상 앞 단계 전체인지 불명(B). |
| O02-5 | F | `/by_concern/1/severity_levels/1/rationale`<br>`/by_concern/1/severity_levels/1/expected_sessions`<br>`/by_concern/1/severity_levels/2/rationale`<br>`/by_concern/1/severity_levels/2/expected_sessions` | optimal_combo 의 「바이오스티뮬레이터」를 rationale·expected_sessions 는 「바이오스티뮬」로 줄여 쓴다. 표기 차이만 기록했다. |
| O02-6 | P | `/by_concern/1/severity_levels/2/optimal_combo/0`<br>`/by_concern/1/severity_levels/1/optimal_combo/0` | 중증은 「울쎄라 HIFU」(장비명 앞, 공백), 중등도는 「HIFU(슈링크/울쎄라)」. 같은 장비를 다른 표기 구조로 쓴다. 중증에서는 장비를 하나로 고정한 것처럼 읽히나 확정하지 않았다. |
| O02-7 | P | `/by_concern/1/severity_levels/2/sequence` | 「울쎄라 HIFU → 2-4주 후 실리프팅 → 필러(볼륨 보충) → 바이오스티뮬레이터(유지)」: 간격은 실리프팅 앞에만 범위로 있다. 괄호는 목적(볼륨 보충·유지). 필러·바이오스티뮬레이터의 간격은 원문에 없다(B). |
| O02-8 | P | `/by_concern/1/severity_levels/2/contraindicated_combos/0`<br>`/by_concern/1/severity_levels/2/optimal_combo/1`<br>`/by_concern/1/severity_levels/2/optimal_combo/2` | 「PDO실 + 비가교HA 동시 금지」: `+` 가 「함께 시술」 표기를 금지 대상 조합에 쓴다. 「동시」가 같은 날·같은 회차·같은 부위 중 무엇인지 원문에 없다(B). optimal_combo 는 「실리프팅(PDO/PCL)」「필러」로 적어 PCL·가교 여부와의 관계는 원문에 없다. |

### 수동 수집 구절 (31건 · 구간은 expressions.json `source=manual_direct_reading`)

| Pointer | 원문 구절 | 탐색 관점(kinds) |
|---|---|---|
| `/by_concern/1/concern` | 처짐/탄력 | target_concern, slash_non_alternative |
| `/by_concern/1/concern_en` | Sagging / Elasticity | language_en, slash_non_alternative |
| `/by_concern/1/severity_levels/0/level` | (초기 처짐) | parenthetical, severity, time |
| `/by_concern/1/severity_levels/0/optimal_combo/0` | 써마지/RF | product_like, procedure_like, alternative |
| `/by_concern/1/severity_levels/0/sequence` | RF 시술 → 2주 후 스킨부스터 | order_sequence, interval_after, time |
| `/by_concern/1/severity_levels/0/rationale` | RF로 콜라겐 리모델링 | effect_purpose |
| `/by_concern/1/severity_levels/0/rationale` | 스킨부스터로 진피 수분/탄력 보충 | effect_purpose, layer_depth, slash_non_alternative |
| `/by_concern/1/severity_levels/0/expected_sessions` | RF 1-2회 | session_count, range |
| `/by_concern/1/severity_levels/0/total_duration` | 3-4개월 | time, range |
| `/by_concern/1/severity_levels/1/level` | (눈에 띄는 처짐) | parenthetical, severity, degree_modifier |
| `/by_concern/1/severity_levels/1/optimal_combo/0` | HIFU(슈링크/울쎄라) | procedure_like, product_like, parenthetical, alternative |
| `/by_concern/1/severity_levels/1/optimal_combo/1` | 보톡스(턱선+광대) | procedure_like, body_part, parenthetical, plus_list |
| `/by_concern/1/severity_levels/1/sequence` | HIFU 먼저 | order_sequence |
| `/by_concern/1/severity_levels/1/sequence` | 같은날 보톡스 가능 | same_day, possibility |
| `/by_concern/1/severity_levels/1/sequence` | 4주 후 바이오스티뮬레이터 시작 | interval_after, time, series_start |
| `/by_concern/1/severity_levels/1/rationale` | HIFU로 SMAS 수축 | effect_purpose, layer_depth, language_mixed |
| `/by_concern/1/severity_levels/1/rationale` | 보톡스로 근육 이완(턱선 슬림) | effect_purpose, body_part, parenthetical |
| `/by_concern/1/severity_levels/1/rationale` | 바이오스티뮬로 콜라겐 장기 재생 | effect_purpose, duration_long, abbreviation |
| `/by_concern/1/severity_levels/1/expected_sessions` | 바이오스티뮬 3-4회 | session_count, range, abbreviation |
| `/by_concern/1/severity_levels/1/total_duration` | 4-8개월 | time, range |
| `/by_concern/1/severity_levels/2/level` | (뚜렷한 처짐) | parenthetical, severity, degree_modifier |
| `/by_concern/1/severity_levels/2/optimal_combo/0` | 울쎄라 HIFU | product_like, procedure_like |
| `/by_concern/1/severity_levels/2/optimal_combo/1` | 실리프팅(PDO/PCL) | procedure_like, material, parenthetical, alternative |
| `/by_concern/1/severity_levels/2/sequence` | 2-4주 후 실리프팅 | interval_after, range, time |
| `/by_concern/1/severity_levels/2/sequence` | 필러(볼륨 보충) | parenthetical, effect_purpose, interval_unspecified |
| `/by_concern/1/severity_levels/2/sequence` | 바이오스티뮬레이터(유지) | parenthetical, maintenance, interval_unspecified |
| `/by_concern/1/severity_levels/2/rationale` | HIFU로 깊은층 수축 | effect_purpose, layer_depth, degree_modifier |
| `/by_concern/1/severity_levels/2/rationale` | 실리프팅으로 물리적 거상 | effect_purpose, manner |
| `/by_concern/1/severity_levels/2/rationale` | 바이오스티뮬로 장기 유지 | maintenance, duration_long, abbreviation |
| `/by_concern/1/severity_levels/2/total_duration` | 6-12개월 | time, range |
| `/by_concern/1/severity_levels/2/contraindicated_combos/0` | PDO실 + 비가교HA 동시 금지 | avoid_prohibit, same_time, material, plus_in_prohibition |

### 이 구획의 미결 (issues.md 에 모음)

- **B-02-1** [B] 간격(4주 후·2-4주 후)의 기준 시점과 뒤 단계(필러·바이오스티뮬레이터) 간격이 원문에 없다. — `/by_concern/1/severity_levels/1/sequence`, `/by_concern/1/severity_levels/2/sequence`
- **B-02-2** [B] 「동시」의 범위(같은 날·같은 회차·같은 부위)가 원문에 없다. — `/by_concern/1/severity_levels/2/contraindicated_combos/0`

<a id="seg-03"></a>
## SEG-03 — by_concern/2

- 직접 읽기: **direct_read_done** — /by_concern/2 (볼륨 손실) 전체 필드와 severity_levels 3단계를 원문 순서로 직접 읽음
- 소유 노드 41 · 말단(빈 컨테이너 포함) 32

### 원문 값 (자동 생성 · 원본 컬럼명 그대로 · 원본 순서)

| Pointer | 원본 컬럼명 | 자료형 | 원문 값 |
|---|---|---|---|
| `/by_concern/2` | `by_concern[2]` | object(4) | _키: concern, concern_en, icon, severity_levels_ |
| `/by_concern/2/concern` | `concern` | string | "볼륨 손실" |
| `/by_concern/2/concern_en` | `concern_en` | string | "Volume Loss" |
| `/by_concern/2/icon` | `icon` | string | "volume" |
| `/by_concern/2/severity_levels` | `severity_levels` | array(3) | _원소 3개_ |
| `/by_concern/2/severity_levels/0` | `severity_levels[0]` | object(8) | _키: level, optimal_combo, sequence, rationale, expected_sessions, total_duration, evidence_level, contraindicated_combos_ |
| `/by_concern/2/severity_levels/0/level` | `level` | string | "경미 (미세 볼륨 저하)" |
| `/by_concern/2/severity_levels/0/optimal_combo` | `optimal_combo` | array(2) | _원소 2개_ |
| `/by_concern/2/severity_levels/0/optimal_combo/0` | `optimal_combo[0]` | string | "HA 볼류마이징 스킨부스터" |
| `/by_concern/2/severity_levels/0/optimal_combo/1` | `optimal_combo[1]` | string | "바이오스티뮬레이터(쥬베룩)" |
| `/by_concern/2/severity_levels/0/sequence` | `sequence` | string | "HA 볼류마이징 스킨부스터 먼저 → 4주 간격 바이오스티뮬레이터" |
| `/by_concern/2/severity_levels/0/rationale` | `rationale` | string | "주사형 HA 제품으로 미세 볼륨·수분 보완 → 쥬베룩으로 자가 콜라겐 재생" |
| `/by_concern/2/severity_levels/0/expected_sessions` | `expected_sessions` | string | "스킨부스터 3회 + 바이오스티뮬 2-3회" |
| `/by_concern/2/severity_levels/0/total_duration` | `total_duration` | string | "3-6개월" |
| `/by_concern/2/severity_levels/0/evidence_level` | `evidence_level` | string | "moderate" |
| `/by_concern/2/severity_levels/0/contraindicated_combos` | `contraindicated_combos` | array(0) | _[]_ |
| `/by_concern/2/severity_levels/1` | `severity_levels[1]` | object(8) | _키: level, optimal_combo, sequence, rationale, expected_sessions, total_duration, evidence_level, contraindicated_combos_ |
| `/by_concern/2/severity_levels/1/level` | `level` | string | "중등도 (눈에 띄는 볼륨 감소)" |
| `/by_concern/2/severity_levels/1/optimal_combo` | `optimal_combo` | array(2) | _원소 2개_ |
| `/by_concern/2/severity_levels/1/optimal_combo/0` | `optimal_combo[0]` | string | "HA 필러" |
| `/by_concern/2/severity_levels/1/optimal_combo/1` | `optimal_combo[1]` | string | "바이오스티뮬레이터(스컬트라/엘란쎄)" |
| `/by_concern/2/severity_levels/1/sequence` | `sequence` | string | "필러로 즉각 볼륨 → 4주 후 바이오스티뮬레이터(콜라겐 장기 재생)" |
| `/by_concern/2/severity_levels/1/rationale` | `rationale` | string | "필러로 구조적 볼륨 복원 → 바이오스티뮬로 자가 콜라겐 생성으로 장기 유지" |
| `/by_concern/2/severity_levels/1/expected_sessions` | `expected_sessions` | string | "필러 1-2회 + 바이오스티뮬 3-4회" |
| `/by_concern/2/severity_levels/1/total_duration` | `total_duration` | string | "4-8개월" |
| `/by_concern/2/severity_levels/1/evidence_level` | `evidence_level` | string | "high" |
| `/by_concern/2/severity_levels/1/contraindicated_combos` | `contraindicated_combos` | array(0) | _[]_ |
| `/by_concern/2/severity_levels/2` | `severity_levels[2]` | object(8) | _키: level, optimal_combo, sequence, rationale, expected_sessions, total_duration, evidence_level, contraindicated_combos_ |
| `/by_concern/2/severity_levels/2/level` | `level` | string | "중증 (심한 볼륨 손실/골격 변화)" |
| `/by_concern/2/severity_levels/2/optimal_combo` | `optimal_combo` | array(4) | _원소 4개_ |
| `/by_concern/2/severity_levels/2/optimal_combo/0` | `optimal_combo[0]` | string | "HA 필러(딥)" |
| `/by_concern/2/severity_levels/2/optimal_combo/1` | `optimal_combo[1]` | string | "CaHA(레디에스)" |
| `/by_concern/2/severity_levels/2/optimal_combo/2` | `optimal_combo[2]` | string | "지방이식" |
| `/by_concern/2/severity_levels/2/optimal_combo/3` | `optimal_combo[3]` | string | "바이오스티뮬레이터" |
| `/by_concern/2/severity_levels/2/sequence` | `sequence` | string | "지방이식 or 딥필러 → 4주 후 CaHA/바이오스티뮬(콜라겐 유도) → 유지" |
| `/by_concern/2/severity_levels/2/rationale` | `rationale` | string | "딥 필러/지방이식으로 구조 복원 → CaHA/바이오스티뮬로 장기 콜라겐 → 자연스러운 유지" |
| `/by_concern/2/severity_levels/2/expected_sessions` | `expected_sessions` | string | "딥필러/지방이식 1회 + 바이오스티뮬 3-4회" |
| `/by_concern/2/severity_levels/2/total_duration` | `total_duration` | string | "6-12개월" |
| `/by_concern/2/severity_levels/2/evidence_level` | `evidence_level` | string | "moderate" |
| `/by_concern/2/severity_levels/2/contraindicated_combos` | `contraindicated_combos` | array(1) | _원소 1개_ |
| `/by_concern/2/severity_levels/2/contraindicated_combos/0` | `contraindicated_combos[0]` | string | "지방이식 후 2주 내 RF/HIFU 금지" |

### 잠정 관찰 (직접 읽기 · 원문 칸과 분리 · 확정 의미 아님)

| ID | 상태 | 근거 Pointer | 관찰 |
|---|---|---|---|
| O03-1 | P | `/by_concern/2/severity_levels/0/optimal_combo/0`<br>`/by_concern/2/severity_levels/0/rationale` | 「HA 볼류마이징 스킨부스터」는 재질(HA)+성질(볼류마이징)+계열(스킨부스터)을 붙여 쓴 한 이름. rationale 은 같은 것을 「주사형 HA 제품」으로 다시 부른다(잠정 동일 지시, 연결 확정 안 함). |
| O03-2 | P | `/by_concern/2/severity_levels/0/optimal_combo/1`<br>`/by_concern/2/severity_levels/0/rationale` | optimal_combo 「바이오스티뮬레이터(쥬베룩)」의 괄호 제품명을 rationale 은 단독 「쥬베룩으로」 주어로 쓴다. 같은 원장 다른 단계는 괄호 안에 제품 두 개(스컬트라/엘란쎄)를 둔다. |
| O03-3 | P | `/by_concern/2/severity_levels/0/sequence`<br>`/by_concern/2/severity_levels/1/sequence` | 「4주 간격 바이오스티뮬레이터」(경미)는 반복 간격으로도, 앞 시술과의 간격으로도 읽힐 수 있다. 중등도의 「4주 후」와 표기가 다르다(간격 vs 후). 두 뜻을 구분하지 않고 원문만 보존한다(B). |
| O03-4 | P | `/by_concern/2/severity_levels/1/sequence` | sequence 안에 효과 서술(「즉각 볼륨」, 괄호 「콜라겐 장기 재생」)이 순서와 섞여 있다. 「즉각」 은 속도/시간 수식. |
| O03-5 | F | `/by_concern/2/severity_levels/2/optimal_combo/0`<br>`/by_concern/2/severity_levels/2/sequence`<br>`/by_concern/2/severity_levels/2/rationale`<br>`/by_concern/2/severity_levels/2/expected_sessions` | 같은 대상이 「HA 필러(딥)」「딥필러」「딥 필러」 세 표기로 나온다. 괄호 「(딥)」은 깊이 수식이다. |
| O03-6 | P | `/by_concern/2/severity_levels/2/sequence` | 「지방이식 or 딥필러」: 영어 접속사 `or` 로 대안을 표시한다(다른 곳은 `/`·「또는」). 「→ 유지」 는 시술명이 아닌 단계명. |
| O03-7 | I | `/by_concern/2/severity_levels/2/optimal_combo/1`<br>`/by_concern/2/severity_levels/2/sequence`<br>`/by_concern/2/severity_levels/2/expected_sessions` | optimal_combo 에 「CaHA(레디에스)」가 따로 있고 sequence·rationale 은 「CaHA/바이오스티뮬」로 묶지만 expected_sessions 에는 CaHA 회차가 없다(「딥필러/지방이식 1회 + 바이오스티뮬 3-4회」). CaHA 가 바이오스티뮬 회차에 포함되는지 원문에 없다. |
| O03-8 | P | `/by_concern/2/severity_levels/2/expected_sessions` | 「딥필러/지방이식 1회」의 `/` 는 sequence 의 「or」와 같은 대안으로 읽힌다(잠정). |
| O03-9 | P | `/by_concern/2/severity_levels/2/contraindicated_combos/0` | 「지방이식 후 2주 내 RF/HIFU 금지」: 이 단계 optimal_combo 에는 RF/HIFU 가 없다. 다른 고민의 추천과 섞을 때 걸리는 규칙으로 읽히나 원문은 범위를 말하지 않는다. 「2주 내」 와 SEG-01 「14일 이내」 의 표기가 다르다. |
| O03-10 | P | `/by_concern/2/severity_levels/2/level` | 「(심한 볼륨 손실/골격 변화)」의 `/` 는 상태 나열이다. |

### 수동 수집 구절 (25건 · 구간은 expressions.json `source=manual_direct_reading`)

| Pointer | 원문 구절 | 탐색 관점(kinds) |
|---|---|---|
| `/by_concern/2/severity_levels/0/level` | (미세 볼륨 저하) | parenthetical, severity, degree_modifier |
| `/by_concern/2/severity_levels/0/optimal_combo/0` | HA 볼류마이징 스킨부스터 | procedure_like, material, language_mixed |
| `/by_concern/2/severity_levels/0/optimal_combo/1` | 바이오스티뮬레이터(쥬베룩) | procedure_like, product_like, parenthetical |
| `/by_concern/2/severity_levels/0/sequence` | HA 볼류마이징 스킨부스터 먼저 | order_sequence |
| `/by_concern/2/severity_levels/0/sequence` | 4주 간격 바이오스티뮬레이터 | interval_repeat_or_after, time |
| `/by_concern/2/severity_levels/0/rationale` | 주사형 HA 제품으로 미세 볼륨·수분 보완 | effect_purpose, manner, degree_modifier, effect_complement |
| `/by_concern/2/severity_levels/0/rationale` | 쥬베룩으로 자가 콜라겐 재생 | product_like, effect_purpose |
| `/by_concern/2/severity_levels/0/expected_sessions` | 바이오스티뮬 2-3회 | session_count, range, abbreviation |
| `/by_concern/2/severity_levels/1/level` | (눈에 띄는 볼륨 감소) | parenthetical, severity, degree_modifier |
| `/by_concern/2/severity_levels/1/optimal_combo/1` | 바이오스티뮬레이터(스컬트라/엘란쎄) | procedure_like, product_like, parenthetical, alternative |
| `/by_concern/2/severity_levels/1/sequence` | 필러로 즉각 볼륨 | effect_purpose, speed_time |
| `/by_concern/2/severity_levels/1/sequence` | 4주 후 바이오스티뮬레이터(콜라겐 장기 재생) | interval_after, time, parenthetical, effect_purpose, duration_long |
| `/by_concern/2/severity_levels/1/rationale` | 필러로 구조적 볼륨 복원 | effect_purpose, manner |
| `/by_concern/2/severity_levels/1/rationale` | 자가 콜라겐 생성으로 장기 유지 | effect_purpose, maintenance, duration_long |
| `/by_concern/2/severity_levels/2/level` | (심한 볼륨 손실/골격 변화) | parenthetical, severity, degree_modifier, slash_non_alternative |
| `/by_concern/2/severity_levels/2/optimal_combo/0` | HA 필러(딥) | procedure_like, material, parenthetical, layer_depth |
| `/by_concern/2/severity_levels/2/optimal_combo/1` | CaHA(레디에스) | material, product_like, parenthetical |
| `/by_concern/2/severity_levels/2/sequence` | 지방이식 or 딥필러 | alternative, language_en, layer_depth |
| `/by_concern/2/severity_levels/2/sequence` | 4주 후 CaHA/바이오스티뮬(콜라겐 유도) | interval_after, time, alternative, parenthetical, effect_purpose |
| `/by_concern/2/severity_levels/2/sequence` | → 유지 | maintenance, order_sequence |
| `/by_concern/2/severity_levels/2/rationale` | 딥 필러/지방이식으로 구조 복원 | alternative, layer_depth, effect_purpose |
| `/by_concern/2/severity_levels/2/rationale` | CaHA/바이오스티뮬로 장기 콜라겐 | alternative, duration_long, effect_purpose |
| `/by_concern/2/severity_levels/2/rationale` | 자연스러운 유지 | manner, maintenance |
| `/by_concern/2/severity_levels/2/expected_sessions` | 딥필러/지방이식 1회 | session_count, alternative |
| `/by_concern/2/severity_levels/2/contraindicated_combos/0` | 지방이식 후 2주 내 RF/HIFU 금지 | avoid_prohibit, interval_within, order_sequence, time, alternative |

### 이 구획의 미결 (issues.md 에 모음)

- **B-03-1** [B] 「4주 간격」이 반복 간격인지 앞 시술과의 간격인지 원문에 없다. — `/by_concern/2/severity_levels/0/sequence`
- **I-03-1** [I] CaHA 가 optimal_combo·sequence·rationale 에 있으나 expected_sessions 에 회차가 없다(원문 내 불일치 후보). 원본 수정 제안은 후속 확인 후보로만 둔다. — `/by_concern/2/severity_levels/2/optimal_combo/1`, `/by_concern/2/severity_levels/2/expected_sessions`

<a id="seg-04"></a>
## SEG-04 — by_concern/3

- 직접 읽기: **direct_read_done** — /by_concern/3 (피부결/모공) 전체 필드, severity_levels 3단계, 중증 단계에만 있는 caveats 2문장을 원문 순서로 직접 읽음
- 소유 노드 47 · 말단(빈 컨테이너 포함) 36

### 원문 값 (자동 생성 · 원본 컬럼명 그대로 · 원본 순서)

| Pointer | 원본 컬럼명 | 자료형 | 원문 값 |
|---|---|---|---|
| `/by_concern/3` | `by_concern[3]` | object(4) | _키: concern, concern_en, icon, severity_levels_ |
| `/by_concern/3/concern` | `concern` | string | "피부결/모공" |
| `/by_concern/3/concern_en` | `concern_en` | string | "Skin Texture / Pores" |
| `/by_concern/3/icon` | `icon` | string | "texture" |
| `/by_concern/3/severity_levels` | `severity_levels` | array(3) | _원소 3개_ |
| `/by_concern/3/severity_levels/0` | `severity_levels[0]` | object(8) | _키: level, optimal_combo, sequence, rationale, expected_sessions, total_duration, evidence_level, contraindicated_combos_ |
| `/by_concern/3/severity_levels/0/level` | `level` | string | "경미 (가벼운 피부결 저하)" |
| `/by_concern/3/severity_levels/0/optimal_combo` | `optimal_combo` | array(3) | _원소 3개_ |
| `/by_concern/3/severity_levels/0/optimal_combo/0` | `optimal_combo[0]` | string | "레이저토닝" |
| `/by_concern/3/severity_levels/0/optimal_combo/1` | `optimal_combo[1]` | string | "필링(약한 산)" |
| `/by_concern/3/severity_levels/0/optimal_combo/2` | `optimal_combo[2]` | string | "스킨부스터" |
| `/by_concern/3/severity_levels/0/sequence` | `sequence` | string | "토닝 → 같은날 얕은 필링 가능 → 2주 후 스킨부스터" |
| `/by_concern/3/severity_levels/0/rationale` | `rationale` | string | "토닝으로 멜라닌/각질 관리 + 필링으로 각질 제거 + 스킨부스터로 보습/재생" |
| `/by_concern/3/severity_levels/0/expected_sessions` | `expected_sessions` | string | "토닝 5-10회 + 필링 3-5회 + 스킨부스터 3회" |
| `/by_concern/3/severity_levels/0/total_duration` | `total_duration` | string | "3-6개월" |
| `/by_concern/3/severity_levels/0/evidence_level` | `evidence_level` | string | "moderate" |
| `/by_concern/3/severity_levels/0/contraindicated_combos` | `contraindicated_combos` | array(0) | _[]_ |
| `/by_concern/3/severity_levels/1` | `severity_levels[1]` | object(8) | _키: level, optimal_combo, sequence, rationale, expected_sessions, total_duration, evidence_level, contraindicated_combos_ |
| `/by_concern/3/severity_levels/1/level` | `level` | string | "중등도 (넓은 모공, 거친 피부결)" |
| `/by_concern/3/severity_levels/1/optimal_combo` | `optimal_combo` | array(3) | _원소 3개_ |
| `/by_concern/3/severity_levels/1/optimal_combo/0` | `optimal_combo[0]` | string | "프락셔널 레이저" |
| `/by_concern/3/severity_levels/1/optimal_combo/1` | `optimal_combo[1]` | string | "MTS/니들RF" |
| `/by_concern/3/severity_levels/1/optimal_combo/2` | `optimal_combo[2]` | string | "스킨부스터" |
| `/by_concern/3/severity_levels/1/sequence` | `sequence` | string | "프락셔널 or 니들RF → 4주 간격 반복 → 사이사이 스킨부스터" |
| `/by_concern/3/severity_levels/1/rationale` | `rationale` | string | "프락셔널/니들RF로 미세 상처 → 콜라겐 리모델링 → 스킨부스터로 재생 촉진" |
| `/by_concern/3/severity_levels/1/expected_sessions` | `expected_sessions` | string | "프락셔널/니들RF 3-5회 + 스킨부스터 3회" |
| `/by_concern/3/severity_levels/1/total_duration` | `total_duration` | string | "4-8개월" |
| `/by_concern/3/severity_levels/1/evidence_level` | `evidence_level` | string | "high" |
| `/by_concern/3/severity_levels/1/contraindicated_combos` | `contraindicated_combos` | array(1) | _원소 1개_ |
| `/by_concern/3/severity_levels/1/contraindicated_combos/0` | `contraindicated_combos[0]` | string | "프락셔널 후 당일 필러 금지" |
| `/by_concern/3/severity_levels/2` | `severity_levels[2]` | object(9) | _키: level, optimal_combo, sequence, rationale, expected_sessions, total_duration, evidence_level, contraindicated_combos, caveats_ |
| `/by_concern/3/severity_levels/2/level` | `level` | string | "중증 (심한 모공/흉터급 피부결)" |
| `/by_concern/3/severity_levels/2/optimal_combo` | `optimal_combo` | array(4) | _원소 4개_ |
| `/by_concern/3/severity_levels/2/optimal_combo/0` | `optimal_combo[0]` | string | "CO2 프락셔널" |
| `/by_concern/3/severity_levels/2/optimal_combo/1` | `optimal_combo[1]` | string | "PRP (엑소좀은 보조·근거 제한적)" |
| `/by_concern/3/severity_levels/2/optimal_combo/2` | `optimal_combo[2]` | string | "스킨부스터" |
| `/by_concern/3/severity_levels/2/optimal_combo/3` | `optimal_combo[3]` | string | "니들RF" |
| `/by_concern/3/severity_levels/2/sequence` | `sequence` | string | "CO2 프락셔널 → 직후 PRP/엑소좀 도포 → 4주 후 니들RF → 스킨부스터" |
| `/by_concern/3/severity_levels/2/rationale` | `rationale` | string | "CO2로 깊은 리서페이싱 → 직후 PRP/엑소좀 도포(LAED, 레이저 보조 전달)로 회복·재생 보조 → 니들RF로 추가 리모델링 → 스킨부스터로 유지" |
| `/by_concern/3/severity_levels/2/expected_sessions` | `expected_sessions` | string | "CO2 프락셔널 2-3회 + PRP 3회 + 니들RF 3회 + 스킨부스터 3회" |
| `/by_concern/3/severity_levels/2/total_duration` | `total_duration` | string | "6-12개월" |
| `/by_concern/3/severity_levels/2/evidence_level` | `evidence_level` | string | "moderate" |
| `/by_concern/3/severity_levels/2/contraindicated_combos` | `contraindicated_combos` | array(1) | _원소 1개_ |
| `/by_concern/3/severity_levels/2/contraindicated_combos/0` | `contraindicated_combos[0]` | string | "CO2 프락셔널 후 당일 필러 금지(감염 위험)" |
| `/by_concern/3/severity_levels/2/caveats` | `caveats` | array(2) | _원소 2개_ |
| `/by_concern/3/severity_levels/2/caveats/0` | `caveats[0]` | string | "엑소좀: 국내외 미승인 — 美 FDA 미용·치료 목적 승인 0건(경고서한·집행 확대), 韓 MFDS는 2025-01-21부터 화장품 광고 내 'exosome' 의학적 표현 제한. '재생 촉진·콜라겐 생성' 등 효능 단정 표현은 사용 금지, 보조요법으로만 안내" |
| `/by_concern/3/severity_levels/2/caveats/1` | `caveats[1]` | string | "엑소좀 근거는 파일럿(가설 생성 수준)+소규모 split-face RCT 1건(보조요법으로 유의 개선, 추가 RCT 필요)으로 PRP 대비 제한적. 핵심 효과는 CO2 프락셔널/니들RF에 기인" |

### 잠정 관찰 (직접 읽기 · 원문 칸과 분리 · 확정 의미 아님)

| ID | 상태 | 근거 Pointer | 관찰 |
|---|---|---|---|
| O04-1 | P | `/by_concern/3/severity_levels/2/caveats` | caveats 는 이 원장에서 /by_concern/3/severity_levels/2 에만 있는 선택적 필드다. 다른 단계에 caveats 가 없다는 것이 주의사항이 없다는 뜻인지는 원문에 없다(B). |
| O04-2 | P | `/by_concern/3/severity_levels/0/optimal_combo/1`<br>`/by_concern/3/severity_levels/0/sequence` | optimal_combo 「필링(약한 산)」(괄호 = 강도/재질) 을 sequence 는 「같은날 얕은 필링 가능」(깊이 수식)으로 부른다. 「약한」과 「얕은」 은 서로 다른 수식어다. 수치 농도·깊이는 원문에 없다. |
| O04-3 | P | `/by_concern/3/severity_levels/0/rationale` | 「토닝으로 멜라닌/각질 관리 + 필링으로 각질 제거 + 스킨부스터로 보습/재생」: rationale 의 `+` 는 효과 나열. 「각질」 이 토닝과 필링 양쪽에 대상으로 나온다(효과 겹침 후보). |
| O04-4 | I | `/by_concern/3/severity_levels/1/optimal_combo/1`<br>`/by_concern/3/severity_levels/1/sequence`<br>`/by_concern/3/severity_levels/1/rationale`<br>`/by_concern/3/severity_levels/1/expected_sessions` | optimal_combo 「MTS/니들RF」 가 sequence 에서는 「프락셔널 or 니들RF」, rationale·expected_sessions 에서는 「프락셔널/니들RF」 로 나와 MTS 가 sequence·rationale·sessions 에서 빠진다. 「프락셔널/니들RF」가 대안인지 묶음인지 원문에 없다. |
| O04-5 | P | `/by_concern/3/severity_levels/1/sequence` | 「4주 간격 반복 → 사이사이 스킨부스터」: 반복(「반복」 명시)과 사이 끼워 넣기(「사이사이」)가 있다. 스킨부스터의 정확한 간격은 없다. |
| O04-6 | P | `/by_concern/3/severity_levels/1/contraindicated_combos/0`<br>`/by_concern/3/severity_levels/2/contraindicated_combos/0` | 「프락셔널 후 당일 필러 금지」(중등도) 와 「CO2 프락셔널 후 당일 필러 금지(감염 위험)」(중증): 같은 꼴, 중증만 괄호 사유가 있다. 두 단계 optimal_combo 에 필러가 없다. 「당일」 + 「후」 순서 조건(필러→프락셔널 순서의 당일 허용 여부는 원문에 없다, B). |
| O04-7 | P | `/by_concern/3/severity_levels/2/optimal_combo/1` | optimal_combo 원소 「PRP (엑소좀은 보조·근거 제한적)」 은 시술 이름 칸 안에 다른 대상(엑소좀)에 대한 근거 평가를 괄호로 넣었다. 괄호가 PRP 를 수식하지 않는다. |
| O04-8 | P | `/by_concern/3/severity_levels/2/sequence`<br>`/by_concern/3/severity_levels/2/rationale` | 「직후 PRP/엑소좀 도포」: 「직후」 는 같은 회차 바로 뒤로 읽히는 시간 표현, 「도포」 는 방식. `/` 는 PRP 와 엑소좀의 대안 또는 병용 중 무엇인지 원문만으로 정하지 않았다. rationale 의 「(LAED, 레이저 보조 전달)」 은 약어+풀이. |
| O04-9 | P | `/by_concern/3/severity_levels/2/caveats/0` | caveats/0 은 규제 서술(美 FDA 승인 0건·경고서한·집행 확대, 韓 MFDS 2025-01-21부터 광고 표현 제한)과 문구 지침(「효능 단정 표현은 사용 금지, 보조요법으로만 안내」)을 한 문장에 담는다. 원장에 적힌 서술로만 기록했고 사실 여부는 검증·보충하지 않았다. 한자 국가 약칭(美·韓)과 영어 따옴표 표기('exosome')가 섞인다. |
| O04-10 | I | `/by_concern/3/severity_levels/2/caveats/0`<br>`/by_concern/3/severity_levels/2/rationale` | caveats/0 은 「'재생 촉진·콜라겐 생성' 등 효능 단정 표현은 사용 금지」라 하고, 같은 단계 rationale 은 「PRP/엑소좀 도포 … 로 회복·재생 보조」라 쓴다. 「보조」 로 낮춰 쓴 것이 지침에 맞는지 원문은 판정하지 않는다(원문 내 긴장 후보, 판정 안 함). |
| O04-11 | P | `/by_concern/3/severity_levels/2/caveats/1` | caveats/1 은 근거 수준 서술: 「파일럿(가설 생성 수준)+소규모 split-face RCT 1건(보조요법으로 유의 개선, 추가 RCT 필요)」, 「PRP 대비 제한적」, 「핵심 효과는 CO2 프락셔널/니들RF에 기인」. 비교(대비)·귀속(기인)·필요(추가 RCT 필요) 서술이 있다. 문헌 식별자는 없다(B). |
| O04-12 | P | `/by_concern/3/severity_levels/2/expected_sessions`<br>`/by_concern/3/severity_levels/2/optimal_combo/1` | expected_sessions 는 「PRP 3회」만 있고 엑소좀 회차는 없다. |

### 수동 수집 구절 (41건 · 구간은 expressions.json `source=manual_direct_reading`)

| Pointer | 원문 구절 | 탐색 관점(kinds) |
|---|---|---|
| `/by_concern/3/concern` | 피부결/모공 | target_concern, slash_non_alternative |
| `/by_concern/3/concern_en` | Skin Texture / Pores | language_en, slash_non_alternative |
| `/by_concern/3/severity_levels/0/level` | (가벼운 피부결 저하) | parenthetical, severity, degree_modifier |
| `/by_concern/3/severity_levels/0/optimal_combo/1` | 필링(약한 산) | procedure_like, parenthetical, degree_modifier, material |
| `/by_concern/3/severity_levels/0/sequence` | 같은날 얕은 필링 가능 | same_day, possibility, layer_depth, degree_modifier |
| `/by_concern/3/severity_levels/0/sequence` | 2주 후 스킨부스터 | interval_after, time |
| `/by_concern/3/severity_levels/0/rationale` | 토닝으로 멜라닌/각질 관리 | effect_purpose, slash_non_alternative |
| `/by_concern/3/severity_levels/0/rationale` | 필링으로 각질 제거 | effect_purpose |
| `/by_concern/3/severity_levels/0/rationale` | 스킨부스터로 보습/재생 | effect_purpose, slash_non_alternative |
| `/by_concern/3/severity_levels/0/expected_sessions` | 필링 3-5회 | session_count, range |
| `/by_concern/3/severity_levels/1/level` | (넓은 모공, 거친 피부결) | parenthetical, severity, degree_modifier |
| `/by_concern/3/severity_levels/1/optimal_combo/1` | MTS/니들RF | procedure_like, alternative, language_mixed |
| `/by_concern/3/severity_levels/1/sequence` | 프락셔널 or 니들RF | alternative, language_en |
| `/by_concern/3/severity_levels/1/sequence` | 4주 간격 반복 | interval_repeat, time |
| `/by_concern/3/severity_levels/1/sequence` | 사이사이 스킨부스터 | interleave, interval_unspecified |
| `/by_concern/3/severity_levels/1/rationale` | 프락셔널/니들RF로 미세 상처 | alternative, effect_mechanism, degree_modifier |
| `/by_concern/3/severity_levels/1/rationale` | 스킨부스터로 재생 촉진 | effect_purpose, effect_complement |
| `/by_concern/3/severity_levels/1/expected_sessions` | 프락셔널/니들RF 3-5회 | session_count, range, alternative |
| `/by_concern/3/severity_levels/1/contraindicated_combos/0` | 프락셔널 후 당일 필러 금지 | avoid_prohibit, same_day, order_sequence |
| `/by_concern/3/severity_levels/2/level` | (심한 모공/흉터급 피부결) | parenthetical, severity, degree_modifier, approximation |
| `/by_concern/3/severity_levels/2/optimal_combo/1` | PRP (엑소좀은 보조·근거 제한적) | procedure_like, parenthetical, evidence_limit, adjunct |
| `/by_concern/3/severity_levels/2/optimal_combo/1` | 엑소좀은 보조·근거 제한적 | evidence_limit, adjunct |
| `/by_concern/3/severity_levels/2/sequence` | 직후 PRP/엑소좀 도포 | immediately_after, time, alternative, manner |
| `/by_concern/3/severity_levels/2/sequence` | 4주 후 니들RF | interval_after, time |
| `/by_concern/3/severity_levels/2/sequence` | → 스킨부스터 | order_sequence, interval_unspecified |
| `/by_concern/3/severity_levels/2/rationale` | CO2로 깊은 리서페이싱 | effect_purpose, layer_depth, degree_modifier |
| `/by_concern/3/severity_levels/2/rationale` | 직후 PRP/엑소좀 도포(LAED, 레이저 보조 전달)로 회복·재생 보조 | immediately_after, manner, parenthetical, abbreviation, adjunct, effect_purpose |
| `/by_concern/3/severity_levels/2/rationale` | 니들RF로 추가 리모델링 | effect_purpose, additional |
| `/by_concern/3/severity_levels/2/rationale` | 스킨부스터로 유지 | maintenance |
| `/by_concern/3/severity_levels/2/expected_sessions` | CO2 프락셔널 2-3회 | session_count, range |
| `/by_concern/3/severity_levels/2/contraindicated_combos/0` | CO2 프락셔널 후 당일 필러 금지(감염 위험) | avoid_prohibit, same_day, order_sequence, parenthetical, risk_reason |
| `/by_concern/3/severity_levels/2/caveats/0` | 엑소좀: 국내외 미승인 | regulatory, negation |
| `/by_concern/3/severity_levels/2/caveats/0` | 美 FDA 미용·치료 목적 승인 0건(경고서한·집행 확대) | regulatory, quantity_unit, negation, parenthetical, language_hanja |
| `/by_concern/3/severity_levels/2/caveats/0` | 韓 MFDS는 2025-01-21부터 화장품 광고 내 'exosome' 의학적 표현 제한 | regulatory, date, time_from, language_hanja, language_en, restriction |
| `/by_concern/3/severity_levels/2/caveats/0` | '재생 촉진·콜라겐 생성' 등 효능 단정 표현은 사용 금지 | avoid_prohibit, wording_guidance, quoted |
| `/by_concern/3/severity_levels/2/caveats/0` | 보조요법으로만 안내 | wording_guidance, restriction, adjunct |
| `/by_concern/3/severity_levels/2/caveats/1` | 파일럿(가설 생성 수준) | evidence_level_text, parenthetical |
| `/by_concern/3/severity_levels/2/caveats/1` | 소규모 split-face RCT 1건(보조요법으로 유의 개선, 추가 RCT 필요) | evidence_level_text, quantity_unit, degree_modifier, language_en, parenthetical, need |
| `/by_concern/3/severity_levels/2/caveats/1` | PRP 대비 제한적 | comparison, evidence_limit |
| `/by_concern/3/severity_levels/2/caveats/1` | 핵심 효과는 CO2 프락셔널/니들RF에 기인 | attribution, effect_purpose, alternative |
| `/by_concern/3/severity_levels/2/caveats/1` | 엑소좀 근거는 | topic_subject, evidence_level_text |

### 이 구획의 미결 (issues.md 에 모음)

- **B-04-1** [B] caveats 가 한 단계에만 있다. 다른 단계·고민에 주의사항이 없는 것인지 기록하지 않은 것인지 원문에 없다. — `/by_concern/3/severity_levels/2/caveats`
- **B-04-2** [B] 근거 서술(파일럿·RCT 1건)에 문헌 식별자가 없다. 근거 연결은 원장만으로 할 수 없다. — `/by_concern/3/severity_levels/2/caveats/1`
- **I-04-1** [I] optimal_combo 「MTS/니들RF」 와 sequence·sessions 「프락셔널 …/니들RF」: MTS 가 뒤 필드에서 사라진다(원문 내 불일치 후보). — `/by_concern/3/severity_levels/1/optimal_combo/1`, `/by_concern/3/severity_levels/1/sequence`, `/by_concern/3/severity_levels/1/expected_sessions`
- **I-04-2** [I] caveats/0 의 효능 단정 금지 지침과 rationale 의 「회복·재생 보조」 문구 사이의 긴장 후보. 판정하지 않음. — `/by_concern/3/severity_levels/2/caveats/0`, `/by_concern/3/severity_levels/2/rationale`

