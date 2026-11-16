# treatment-optimization.json — 1차 조사 review-part-2

> 원문 값 표는 build.py 가 원본에서 자동 생성했다. 잠정 관찰·수동 구절은 manual/seg-XX.json 의 직접 읽기 기록이다. 원장의 임상·규제 서술은 **원장에 적혀 있다는 사실**로만 기록했고 검증·보충하지 않았다.
> 상태 기호: P 잠정 · B 원문 정보 부족 · I 원문 내 불일치 후보 · F 후속 의미 조사 · K 알려진 분석 한계 · A 에이전트 추출 오류 · C 사용자 결정 필요.

[← 목차 review.md](./review.md)

<a id="seg-05"></a>
## SEG-05 — by_concern/4

- 직접 읽기: **direct_read_done** — /by_concern/4 (색소/기미) 전체 필드와 severity_levels 3단계(중등도 contraindicated_combos 2문장·중증 2문장 포함)를 원문 순서로 직접 읽음
- 소유 노드 47 · 말단(빈 컨테이너 포함) 37

### 원문 값 (자동 생성 · 원본 컬럼명 그대로 · 원본 순서)

| Pointer | 원본 컬럼명 | 자료형 | 원문 값 |
|---|---|---|---|
| `/by_concern/4` | `by_concern[4]` | object(4) | _키: concern, concern_en, icon, severity_levels_ |
| `/by_concern/4/concern` | `concern` | string | "색소/기미" |
| `/by_concern/4/concern_en` | `concern_en` | string | "Pigmentation / Melasma" |
| `/by_concern/4/icon` | `icon` | string | "pigment" |
| `/by_concern/4/severity_levels` | `severity_levels` | array(3) | _원소 3개_ |
| `/by_concern/4/severity_levels/0` | `severity_levels[0]` | object(8) | _키: level, optimal_combo, sequence, rationale, expected_sessions, total_duration, evidence_level, contraindicated_combos_ |
| `/by_concern/4/severity_levels/0/level` | `level` | string | "경미 (표재성 색소)" |
| `/by_concern/4/severity_levels/0/optimal_combo` | `optimal_combo` | array(3) | _원소 3개_ |
| `/by_concern/4/severity_levels/0/optimal_combo/0` | `optimal_combo[0]` | string | "피코토닝" |
| `/by_concern/4/severity_levels/0/optimal_combo/1` | `optimal_combo[1]` | string | "IPL" |
| `/by_concern/4/severity_levels/0/optimal_combo/2` | `optimal_combo[2]` | string | "비타민C 이온토포레시스" |
| `/by_concern/4/severity_levels/0/sequence` | `sequence` | string | "피코토닝 → IPL(같은날 가능, 토닝 먼저) → 비타민C 도포" |
| `/by_concern/4/severity_levels/0/rationale` | `rationale` | string | "피코토닝으로 멜라닌 미세 파괴 → IPL로 광범위 색소 제거 → 비타민C로 항산화/미백" |
| `/by_concern/4/severity_levels/0/expected_sessions` | `expected_sessions` | string | "피코토닝 5-10회 + IPL 3-5회" |
| `/by_concern/4/severity_levels/0/total_duration` | `total_duration` | string | "3-6개월" |
| `/by_concern/4/severity_levels/0/evidence_level` | `evidence_level` | string | "high" |
| `/by_concern/4/severity_levels/0/contraindicated_combos` | `contraindicated_combos` | array(0) | _[]_ |
| `/by_concern/4/severity_levels/1` | `severity_levels[1]` | object(8) | _키: level, optimal_combo, sequence, rationale, expected_sessions, total_duration, evidence_level, contraindicated_combos_ |
| `/by_concern/4/severity_levels/1/level` | `level` | string | "중등도 (기미, 혼합 색소)" |
| `/by_concern/4/severity_levels/1/optimal_combo` | `optimal_combo` | array(4) | _원소 4개_ |
| `/by_concern/4/severity_levels/1/optimal_combo/0` | `optimal_combo[0]` | string | "피코토닝" |
| `/by_concern/4/severity_levels/1/optimal_combo/1` | `optimal_combo[1]` | string | "트라넥삼산(경구/국소)" |
| `/by_concern/4/severity_levels/1/optimal_combo/2` | `optimal_combo[2]` | string | "스킨부스터(미백성분)" |
| `/by_concern/4/severity_levels/1/optimal_combo/3` | `optimal_combo[3]` | string | "저출력 IPL(병용 보조)" |
| `/by_concern/4/severity_levels/1/sequence` | `sequence` | string | "트라넥삼산 경구 시작 → 2주 후 피코토닝 + 저출력 IPL 교차(시험 조사·광차단 선행, 반동 색소 모니터링) → 스킨부스터(미백)" |
| `/by_concern/4/severity_levels/1/rationale` | `rationale` | string | "트라넥삼산으로 멜라닌 생성 억제 → 토닝/저출력 IPL로 기존 색소 제거(IPL은 보조요법, 반동·PIH 위험으로 저출력·시험조사 필수) → 스킨부스터로 피부 회복" |
| `/by_concern/4/severity_levels/1/expected_sessions` | `expected_sessions` | string | "트라넥삼산 지속 + 피코토닝 10-15회 + IPL 3-5회 + 스킨부스터 3회" |
| `/by_concern/4/severity_levels/1/total_duration` | `total_duration` | string | "6-12개월" |
| `/by_concern/4/severity_levels/1/evidence_level` | `evidence_level` | string | "high" |
| `/by_concern/4/severity_levels/1/contraindicated_combos` | `contraindicated_combos` | array(2) | _원소 2개_ |
| `/by_concern/4/severity_levels/1/contraindicated_combos/0` | `contraindicated_combos[0]` | string | "기미에 고에너지 레이저 금지(PIH 위험)" |
| `/by_concern/4/severity_levels/1/contraindicated_combos/1` | `contraindicated_combos[1]` | string | "기미에 IPL 단독·고출력 금지 — 저출력·병용 보조로만, 반동 색소·PIH 위험(Fitzpatrick IV~VI 고위험), 시험 조사(test spot)·엄격한 광차단 선행" |
| `/by_concern/4/severity_levels/2` | `severity_levels[2]` | object(8) | _키: level, optimal_combo, sequence, rationale, expected_sessions, total_duration, evidence_level, contraindicated_combos_ |
| `/by_concern/4/severity_levels/2/level` | `level` | string | "중증 (깊은 기미, 진피 색소)" |
| `/by_concern/4/severity_levels/2/optimal_combo` | `optimal_combo` | array(4) | _원소 4개_ |
| `/by_concern/4/severity_levels/2/optimal_combo/0` | `optimal_combo[0]` | string | "저출력 피코토닝" |
| `/by_concern/4/severity_levels/2/optimal_combo/1` | `optimal_combo[1]` | string | "트라넥삼산(경구+주사)" |
| `/by_concern/4/severity_levels/2/optimal_combo/2` | `optimal_combo[2]` | string | "마이크로니들링+미백약물" |
| `/by_concern/4/severity_levels/2/optimal_combo/3` | `optimal_combo[3]` | string | "스킨부스터" |
| `/by_concern/4/severity_levels/2/sequence` | `sequence` | string | "트라넥삼산 경구+국소 → 저출력 피코토닝 장기 → 마이크로니들+미백약 → 스킨부스터" |
| `/by_concern/4/severity_levels/2/rationale` | `rationale` | string | "진피 기미는 공격적 치료 금지. 저출력 장기 토닝 + 약물 병용으로 점진적 개선" |
| `/by_concern/4/severity_levels/2/expected_sessions` | `expected_sessions` | string | "피코토닝 15-20회 + 마이크로니들 5회 + 스킨부스터 4회" |
| `/by_concern/4/severity_levels/2/total_duration` | `total_duration` | string | "12-24개월" |
| `/by_concern/4/severity_levels/2/evidence_level` | `evidence_level` | string | "moderate" |
| `/by_concern/4/severity_levels/2/contraindicated_combos` | `contraindicated_combos` | array(2) | _원소 2개_ |
| `/by_concern/4/severity_levels/2/contraindicated_combos/0` | `contraindicated_combos[0]` | string | "고출력 레이저 금지(반동 색소침착)" |
| `/by_concern/4/severity_levels/2/contraindicated_combos/1` | `contraindicated_combos[1]` | string | "기미에 IPL 단독 금지" |

### 잠정 관찰 (직접 읽기 · 원문 칸과 분리 · 확정 의미 아님)

| ID | 상태 | 근거 Pointer | 관찰 |
|---|---|---|---|
| O05-1 | P | `/by_concern/4/severity_levels/0/sequence` | 「IPL(같은날 가능, 토닝 먼저)」: 괄호 안에 동일일 가능성(가능)과 같은 날일 때의 순서 조건(토닝 먼저)이 함께 있다. 같은 날이 아닐 때의 간격은 원문에 없다(B). |
| O05-2 | P | `/by_concern/4/severity_levels/0/optimal_combo/2`<br>`/by_concern/4/severity_levels/0/sequence`<br>`/by_concern/4/severity_levels/0/expected_sessions` | optimal_combo 「비타민C 이온토포레시스」 를 sequence 는 「비타민C 도포」 로 쓴다(이온토포레시스=도입 방식 vs 도포). expected_sessions 에 비타민C 회차가 없다. |
| O05-3 | I | `/by_concern/4/severity_levels/1/optimal_combo/1`<br>`/by_concern/4/severity_levels/1/sequence`<br>`/by_concern/4/severity_levels/2/optimal_combo/1`<br>`/by_concern/4/severity_levels/2/sequence` | 트라넥삼산 투여 경로 표기가 필드마다 다르다: 중등도 optimal_combo 「(경구/국소)」·sequence 「경구 시작」, 중증 optimal_combo 「(경구+주사)」·sequence 「경구+국소」. 중증에서 optimal_combo(주사)와 sequence(국소)가 어긋난다(원문 내 불일치 후보). |
| O05-4 | P | `/by_concern/4/severity_levels/1/optimal_combo/3`<br>`/by_concern/4/severity_levels/1/sequence`<br>`/by_concern/4/severity_levels/1/rationale`<br>`/by_concern/4/severity_levels/1/contraindicated_combos/1` | IPL 은 중등도에서 추천(「저출력 IPL(병용 보조)」)과 금지(「기미에 IPL 단독·고출력 금지」)에 동시에 나온다. 둘을 가르는 조건은 출력(저/고)과 단독/병용이며, 선행 조건(시험 조사·광차단)과 모니터링(반동 색소)이 붙는다. 조건이 사라지면 추천과 금지가 충돌하는 것처럼 읽힌다. |
| O05-5 | P | `/by_concern/4/severity_levels/1/sequence` | 「2주 후 피코토닝 + 저출력 IPL 교차」: `+` 다음 「교차」 가 붙어 함께(같은 날)가 아니라 번갈아 하는 것으로 읽힐 수 있다(README `+` 와 다른 쓰임 후보). 괄호 「(시험 조사·광차단 선행, 반동 색소 모니터링)」 은 선행 조건·관찰 지시. |
| O05-6 | P | `/by_concern/4/severity_levels/1/rationale` | rationale 괄호 「(IPL은 보조요법, 반동·PIH 위험으로 저출력·시험조사 필수)」: 위험 → 조건 필수의 인과 서술. 「시험 조사」(sequence) 와 「시험조사」(rationale) 띄어쓰기가 다르다. |
| O05-7 | P | `/by_concern/4/severity_levels/1/contraindicated_combos/1` | contraindicated_combos/1 은 금지(단독·고출력), 허용 범위(저출력·병용 보조로만), 위험(반동 색소·PIH), 고위험 대상 조건(Fitzpatrick IV~VI), 선행 조건(test spot·엄격한 광차단)을 한 문장에 담는다. 「—」 로 금지와 허용을 가른다. 「IV~VI」 는 로마숫자 범위. |
| O05-8 | P | `/by_concern/4/severity_levels/1/contraindicated_combos/0`<br>`/by_concern/4/severity_levels/2/contraindicated_combos/0` | 「기미에 고에너지 레이저 금지(PIH 위험)」(중등도) 와 「고출력 레이저 금지(반동 색소침착)」(중증): 「고에너지」/「고출력」 표기 차이, 중증은 대상(기미에) 없이 쓰였다. 고출력의 수치 기준은 원문에 없다(B). |
| O05-9 | P | `/by_concern/4/severity_levels/2/rationale` | 「진피 기미는 공격적 치료 금지. 저출력 장기 토닝 + 약물 병용으로 점진적 개선」: rationale 에 금지 서술이 있다(contraindicated_combos 밖). 「공격적」·「점진적」 은 정도/속도 수식. 「약물」 은 구체 약물을 지정하지 않는다. |
| O05-10 | F | `/by_concern/4/severity_levels/2/optimal_combo/2`<br>`/by_concern/4/severity_levels/2/sequence`<br>`/by_concern/4/severity_levels/2/expected_sessions` | 「마이크로니들링+미백약물」(optimal_combo) / 「마이크로니들+미백약」(sequence) / 「마이크로니들 5회」(sessions): 표기 축약 차이. 여기 `+` 는 시술+약물 결합. |
| O05-11 | P | `/by_concern/4/severity_levels/2/expected_sessions`<br>`/by_concern/4/severity_levels/1/expected_sessions` | 중증 expected_sessions 에 트라넥삼산이 없다. 중등도는 「트라넥삼산 지속」 으로 회차 대신 지속을 쓴다. |
| O05-12 | P | `/by_concern/4/severity_levels/2/contraindicated_combos/1`<br>`/by_concern/4/severity_levels/1/contraindicated_combos/1` | 중증 「기미에 IPL 단독 금지」 는 중등도 문장에서 고출력·조건부 허용이 빠진 짧은 꼴이다. 중증에서 저출력 병용 IPL 이 허용되는지는 원문에 없다(중증 optimal_combo 에 IPL 없음). |

### 수동 수집 구절 (44건 · 구간은 expressions.json `source=manual_direct_reading`)

| Pointer | 원문 구절 | 탐색 관점(kinds) |
|---|---|---|
| `/by_concern/4/concern` | 색소/기미 | target_concern, slash_non_alternative |
| `/by_concern/4/concern_en` | Pigmentation / Melasma | language_en, slash_non_alternative |
| `/by_concern/4/severity_levels/0/level` | (표재성 색소) | parenthetical, severity, layer_depth |
| `/by_concern/4/severity_levels/0/optimal_combo/2` | 비타민C 이온토포레시스 | procedure_like, manner, language_mixed |
| `/by_concern/4/severity_levels/0/sequence` | IPL(같은날 가능, 토닝 먼저) | same_day, possibility, order_sequence, condition, parenthetical |
| `/by_concern/4/severity_levels/0/sequence` | 비타민C 도포 | manner, interval_unspecified |
| `/by_concern/4/severity_levels/0/rationale` | 피코토닝으로 멜라닌 미세 파괴 | effect_mechanism, degree_modifier |
| `/by_concern/4/severity_levels/0/rationale` | IPL로 광범위 색소 제거 | effect_purpose, range_area |
| `/by_concern/4/severity_levels/0/rationale` | 비타민C로 항산화/미백 | effect_purpose, slash_non_alternative |
| `/by_concern/4/severity_levels/0/expected_sessions` | 피코토닝 5-10회 | session_count, range |
| `/by_concern/4/severity_levels/0/expected_sessions` | IPL 3-5회 | session_count, range |
| `/by_concern/4/severity_levels/1/level` | (기미, 혼합 색소) | parenthetical, severity, target_concern |
| `/by_concern/4/severity_levels/1/optimal_combo/1` | 트라넥삼산(경구/국소) | drug_like, route, parenthetical, alternative |
| `/by_concern/4/severity_levels/1/optimal_combo/2` | 스킨부스터(미백성분) | procedure_like, parenthetical, ingredient |
| `/by_concern/4/severity_levels/1/optimal_combo/3` | 저출력 IPL(병용 보조) | procedure_like, energy_level, parenthetical, adjunct, condition |
| `/by_concern/4/severity_levels/1/sequence` | 트라넥삼산 경구 시작 | drug_like, route, series_start |
| `/by_concern/4/severity_levels/1/sequence` | 2주 후 피코토닝 + 저출력 IPL 교차 | interval_after, time, alternate_cross, energy_level, plus_non_same_day |
| `/by_concern/4/severity_levels/1/sequence` | (시험 조사·광차단 선행, 반동 색소 모니터링) | parenthetical, precondition, monitoring, risk_reason |
| `/by_concern/4/severity_levels/1/sequence` | 스킨부스터(미백) | parenthetical, effect_purpose, interval_unspecified |
| `/by_concern/4/severity_levels/1/rationale` | 트라넥삼산으로 멜라닌 생성 억제 | effect_mechanism, drug_like |
| `/by_concern/4/severity_levels/1/rationale` | 토닝/저출력 IPL로 기존 색소 제거 | effect_purpose, energy_level, slash_ambiguous |
| `/by_concern/4/severity_levels/1/rationale` | (IPL은 보조요법, 반동·PIH 위험으로 저출력·시험조사 필수) | parenthetical, adjunct, risk_reason, requirement, energy_level, causal |
| `/by_concern/4/severity_levels/1/rationale` | 스킨부스터로 피부 회복 | effect_purpose |
| `/by_concern/4/severity_levels/1/expected_sessions` | 트라넥삼산 지속 | continuous, drug_like |
| `/by_concern/4/severity_levels/1/expected_sessions` | 피코토닝 10-15회 | session_count, range |
| `/by_concern/4/severity_levels/1/total_duration` | 6-12개월 | time, range |
| `/by_concern/4/severity_levels/1/contraindicated_combos/0` | 기미에 고에너지 레이저 금지(PIH 위험) | avoid_prohibit, target_condition, energy_level, parenthetical, risk_reason |
| `/by_concern/4/severity_levels/1/contraindicated_combos/1` | 기미에 IPL 단독·고출력 금지 | avoid_prohibit, target_condition, monotherapy, energy_level |
| `/by_concern/4/severity_levels/1/contraindicated_combos/1` | 저출력·병용 보조로만 | restriction, energy_level, adjunct, condition |
| `/by_concern/4/severity_levels/1/contraindicated_combos/1` | 반동 색소·PIH 위험(Fitzpatrick IV~VI 고위험) | risk_reason, parenthetical, skin_type, range, language_en |
| `/by_concern/4/severity_levels/1/contraindicated_combos/1` | 시험 조사(test spot)·엄격한 광차단 선행 | precondition, parenthetical, language_en, degree_modifier |
| `/by_concern/4/severity_levels/2/level` | (깊은 기미, 진피 색소) | parenthetical, severity, layer_depth |
| `/by_concern/4/severity_levels/2/optimal_combo/0` | 저출력 피코토닝 | procedure_like, energy_level |
| `/by_concern/4/severity_levels/2/optimal_combo/1` | 트라넥삼산(경구+주사) | drug_like, route, parenthetical, plus_list |
| `/by_concern/4/severity_levels/2/optimal_combo/2` | 마이크로니들링+미백약물 | procedure_like, drug_like, plus_list |
| `/by_concern/4/severity_levels/2/sequence` | 트라넥삼산 경구+국소 | drug_like, route, plus_list |
| `/by_concern/4/severity_levels/2/sequence` | 저출력 피코토닝 장기 | energy_level, duration_long |
| `/by_concern/4/severity_levels/2/sequence` | 마이크로니들+미백약 | procedure_like, drug_like, plus_list, abbreviation |
| `/by_concern/4/severity_levels/2/rationale` | 진피 기미는 공격적 치료 금지 | avoid_prohibit, layer_depth, degree_modifier, target_condition |
| `/by_concern/4/severity_levels/2/rationale` | 저출력 장기 토닝 + 약물 병용으로 점진적 개선 | energy_level, duration_long, combination, speed_time, effect_purpose |
| `/by_concern/4/severity_levels/2/expected_sessions` | 피코토닝 15-20회 | session_count, range |
| `/by_concern/4/severity_levels/2/total_duration` | 12-24개월 | time, range |
| `/by_concern/4/severity_levels/2/contraindicated_combos/0` | 고출력 레이저 금지(반동 색소침착) | avoid_prohibit, energy_level, parenthetical, risk_reason |
| `/by_concern/4/severity_levels/2/contraindicated_combos/1` | 기미에 IPL 단독 금지 | avoid_prohibit, target_condition, monotherapy |

### 이 구획의 미결 (issues.md 에 모음)

- **I-05-1** [I] 중증 트라넥삼산 경로: optimal_combo 「경구+주사」 vs sequence 「경구+국소」(원문 내 불일치 후보). — `/by_concern/4/severity_levels/2/optimal_combo/1`, `/by_concern/4/severity_levels/2/sequence`
- **B-05-1** [B] 저출력·고출력·고에너지의 수치 기준이 원문에 없다. 추천(저출력 IPL)과 금지(고출력 IPL)의 경계를 원장만으로 정할 수 없다. — `/by_concern/4/severity_levels/1/contraindicated_combos/0`, `/by_concern/4/severity_levels/1/contraindicated_combos/1`, `/by_concern/4/severity_levels/2/contraindicated_combos/0`, `/by_concern/4/severity_levels/1/optimal_combo/3`
- **B-05-2** [B] 중증 단계에서 저출력·병용 IPL 이 허용되는지 원문에 없다. — `/by_concern/4/severity_levels/2/contraindicated_combos/1`

<a id="seg-06"></a>
## SEG-06 — by_concern/5

- 직접 읽기: **direct_read_done** — /by_concern/5 (여드름/흉터) 전체 필드와 severity_levels 3단계를 원문 순서로 직접 읽음
- 소유 노드 47 · 말단(빈 컨테이너 포함) 37

### 원문 값 (자동 생성 · 원본 컬럼명 그대로 · 원본 순서)

| Pointer | 원본 컬럼명 | 자료형 | 원문 값 |
|---|---|---|---|
| `/by_concern/5` | `by_concern[5]` | object(4) | _키: concern, concern_en, icon, severity_levels_ |
| `/by_concern/5/concern` | `concern` | string | "여드름/흉터" |
| `/by_concern/5/concern_en` | `concern_en` | string | "Acne / Acne Scars" |
| `/by_concern/5/icon` | `icon` | string | "acne" |
| `/by_concern/5/severity_levels` | `severity_levels` | array(3) | _원소 3개_ |
| `/by_concern/5/severity_levels/0` | `severity_levels[0]` | object(8) | _키: level, optimal_combo, sequence, rationale, expected_sessions, total_duration, evidence_level, contraindicated_combos_ |
| `/by_concern/5/severity_levels/0/level` | `level` | string | "경미 (활성 여드름 위주)" |
| `/by_concern/5/severity_levels/0/optimal_combo` | `optimal_combo` | array(3) | _원소 3개_ |
| `/by_concern/5/severity_levels/0/optimal_combo/0` | `optimal_combo[0]` | string | "ALA-PDT" |
| `/by_concern/5/severity_levels/0/optimal_combo/1` | `optimal_combo[1]` | string | "필링(살리실산/글리콜산)" |
| `/by_concern/5/severity_levels/0/optimal_combo/2` | `optimal_combo[2]` | string | "LED(블루라이트)" |
| `/by_concern/5/severity_levels/0/sequence` | `sequence` | string | "ALA-PDT → 2주 간격 필링 → LED(매회 마무리)" |
| `/by_concern/5/severity_levels/0/rationale` | `rationale` | string | "PDT로 피지선 억제 + 필링으로 각질/모공 관리 + LED로 항균/항염" |
| `/by_concern/5/severity_levels/0/expected_sessions` | `expected_sessions` | string | "PDT 3-5회 + 필링 5-8회 + LED 매회" |
| `/by_concern/5/severity_levels/0/total_duration` | `total_duration` | string | "2-4개월" |
| `/by_concern/5/severity_levels/0/evidence_level` | `evidence_level` | string | "high" |
| `/by_concern/5/severity_levels/0/contraindicated_combos` | `contraindicated_combos` | array(0) | _[]_ |
| `/by_concern/5/severity_levels/1` | `severity_levels[1]` | object(8) | _키: level, optimal_combo, sequence, rationale, expected_sessions, total_duration, evidence_level, contraindicated_combos_ |
| `/by_concern/5/severity_levels/1/level` | `level` | string | "중등도 (여드름 흉터 위주)" |
| `/by_concern/5/severity_levels/1/optimal_combo` | `optimal_combo` | array(4) | _원소 4개_ |
| `/by_concern/5/severity_levels/1/optimal_combo/0` | `optimal_combo[0]` | string | "프락셔널 레이저" |
| `/by_concern/5/severity_levels/1/optimal_combo/1` | `optimal_combo[1]` | string | "서브시전(subcision)" |
| `/by_concern/5/severity_levels/1/optimal_combo/2` | `optimal_combo[2]` | string | "MTS/니들RF" |
| `/by_concern/5/severity_levels/1/optimal_combo/3` | `optimal_combo[3]` | string | "PRP" |
| `/by_concern/5/severity_levels/1/sequence` | `sequence` | string | "서브시전(깊은 흉터 박리) → 4주 후 프락셔널/니들RF → PRP 동시 도포" |
| `/by_concern/5/severity_levels/1/rationale` | `rationale` | string | "서브시전으로 섬유화 박리 → 프락셔널로 표면 리모델링 → PRP로 재생 촉진" |
| `/by_concern/5/severity_levels/1/expected_sessions` | `expected_sessions` | string | "서브시전 1-3회 + 프락셔널 3-5회 + 니들RF 3회 + PRP 3회" |
| `/by_concern/5/severity_levels/1/total_duration` | `total_duration` | string | "6-12개월" |
| `/by_concern/5/severity_levels/1/evidence_level` | `evidence_level` | string | "high" |
| `/by_concern/5/severity_levels/1/contraindicated_combos` | `contraindicated_combos` | array(1) | _원소 1개_ |
| `/by_concern/5/severity_levels/1/contraindicated_combos/0` | `contraindicated_combos[0]` | string | "활성 여드름 시 프락셔널 금지(감염 확산)" |
| `/by_concern/5/severity_levels/2` | `severity_levels[2]` | object(8) | _키: level, optimal_combo, sequence, rationale, expected_sessions, total_duration, evidence_level, contraindicated_combos_ |
| `/by_concern/5/severity_levels/2/level` | `level` | string | "중증 (깊은 박스카/아이스픽 흉터)" |
| `/by_concern/5/severity_levels/2/optimal_combo` | `optimal_combo` | array(5) | _원소 5개_ |
| `/by_concern/5/severity_levels/2/optimal_combo/0` | `optimal_combo[0]` | string | "CO2 프락셔널" |
| `/by_concern/5/severity_levels/2/optimal_combo/1` | `optimal_combo[1]` | string | "서브시전" |
| `/by_concern/5/severity_levels/2/optimal_combo/2` | `optimal_combo[2]` | string | "필러(HA/CaHA)" |
| `/by_concern/5/severity_levels/2/optimal_combo/3` | `optimal_combo[3]` | string | "TCA Cross" |
| `/by_concern/5/severity_levels/2/optimal_combo/4` | `optimal_combo[4]` | string | "PRP/엑소좀" |
| `/by_concern/5/severity_levels/2/sequence` | `sequence` | string | "서브시전 + TCA Cross(아이스픽) → 4주 후 CO2 프락셔널 → PRP 즉시 도포 → 필러(남은 함몰)" |
| `/by_concern/5/severity_levels/2/rationale` | `rationale` | string | "서브시전+TCA로 깊은 흉터 기저부 치료 → CO2로 전체 리서페이싱 → PRP 재생 → 필러로 잔여 함몰 보충" |
| `/by_concern/5/severity_levels/2/expected_sessions` | `expected_sessions` | string | "서브시전 2-3회 + TCA Cross 3-5회 + CO2 3회 + PRP 3회 + 필러 1-2회" |
| `/by_concern/5/severity_levels/2/total_duration` | `total_duration` | string | "12-18개월" |
| `/by_concern/5/severity_levels/2/evidence_level` | `evidence_level` | string | "high" |
| `/by_concern/5/severity_levels/2/contraindicated_combos` | `contraindicated_combos` | array(2) | _원소 2개_ |
| `/by_concern/5/severity_levels/2/contraindicated_combos/0` | `contraindicated_combos[0]` | string | "CO2 후 당일 필러 금지" |
| `/by_concern/5/severity_levels/2/contraindicated_combos/1` | `contraindicated_combos[1]` | string | "활성 여드름 시 침습 시술 금지" |

### 잠정 관찰 (직접 읽기 · 원문 칸과 분리 · 확정 의미 아님)

| ID | 상태 | 근거 Pointer | 관찰 |
|---|---|---|---|
| O06-1 | P | `/by_concern/5/concern`<br>`/by_concern/5/concern_en` | concern 「여드름/흉터」 vs concern_en 「Acne / Acne Scars」: 영어는 흉터를 여드름 흉터로 좁혀 쓴다. 한국어 「흉터」 가 여드름 흉터만인지 원문에 없다. |
| O06-2 | P | `/by_concern/5/severity_levels/0/level`<br>`/by_concern/5/severity_levels/1/level`<br>`/by_concern/5/severity_levels/2/level` | 단계가 정도가 아니라 상태 종류로도 갈린다: 경미 「(활성 여드름 위주)」, 중등도 「(여드름 흉터 위주)」, 중증 「(깊은 박스카/아이스픽 흉터)」. 「위주」 는 근사·주된 정도 표현. |
| O06-3 | P | `/by_concern/5/severity_levels/0/sequence`<br>`/by_concern/5/severity_levels/0/expected_sessions` | 「ALA-PDT → 2주 간격 필링 → LED(매회 마무리)」: 「매회 마무리」 는 각 회차 끝에 한다는 반복 위치 표현. expected_sessions 는 「LED 매회」 로 회차 수 대신 쓴다. 매회가 어느 시술의 회차인지 원문에 없다(B). |
| O06-4 | F | `/by_concern/5/severity_levels/0/optimal_combo/0`<br>`/by_concern/5/severity_levels/0/rationale`<br>`/by_concern/5/severity_levels/0/expected_sessions` | 「ALA-PDT」 를 rationale·sessions 는 「PDT」 로 줄여 쓴다. |
| O06-5 | P | `/by_concern/5/severity_levels/1/optimal_combo/1`<br>`/by_concern/5/severity_levels/1/sequence` | 「서브시전(subcision)」 괄호는 영어 원어. sequence 의 「서브시전(깊은 흉터 박리)」 괄호는 대상·방식. 같은 이름 뒤 괄호의 역할이 다르다. |
| O06-6 | P | `/by_concern/5/severity_levels/1/sequence` | 「4주 후 프락셔널/니들RF → PRP 동시 도포」: 「동시」 가 화살표 뒤에 있어 앞 단계와 같은 회차에 바르는 것으로 읽힌다(잠정). SEG-02 금지문의 「동시」 와 같은 낱말이 추천 문맥에 쓰였다. |
| O06-7 | I | `/by_concern/5/severity_levels/1/optimal_combo/2`<br>`/by_concern/5/severity_levels/1/rationale`<br>`/by_concern/5/severity_levels/1/expected_sessions` | optimal_combo 「MTS/니들RF」, sequence 「프락셔널/니들RF」, rationale 은 니들RF 를 언급하지 않고, expected_sessions 는 「프락셔널 3-5회 + 니들RF 3회」 로 따로 센다. sequence 의 `/` 가 대안이라면 sessions 의 별도 회차와 어긋난다(원문 내 불일치 후보, SEG-04 I-04-1 과 같은 꼴). |
| O06-8 | P | `/by_concern/5/severity_levels/1/contraindicated_combos/0`<br>`/by_concern/5/severity_levels/2/contraindicated_combos/1` | 「활성 여드름 시 프락셔널 금지(감염 확산)」, 「활성 여드름 시 침습 시술 금지」: 「시」 조건절(상태 조건). 중증은 범주어 「침습 시술」 로 넓게 쓴다. 침습 시술에 무엇이 드는지 원문에 없다(B). |
| O06-9 | P | `/by_concern/5/severity_levels/2/sequence` | 「서브시전 + TCA Cross(아이스픽) → 4주 후 CO2 프락셔널 → PRP 즉시 도포 → 필러(남은 함몰)」: 괄호 「(아이스픽)」 은 적용 흉터 유형 조건, 「(남은 함몰)」 은 적용 대상 조건. 「즉시」 는 시간. 필러 간격은 없다. |
| O06-10 | P | `/by_concern/5/severity_levels/2/optimal_combo/4`<br>`/by_concern/5/severity_levels/2/sequence`<br>`/by_concern/5/severity_levels/2/expected_sessions` | optimal_combo 「PRP/엑소좀」 이지만 sequence·rationale·sessions 은 PRP 만 쓴다. SEG-04 caveats(엑소좀 미승인·보조) 가 이 단계에는 없다. |
| O06-11 | P | `/by_concern/5/severity_levels/2/optimal_combo/2` | 「필러(HA/CaHA)」: 괄호 = 재질 대안. |
| O06-12 | P | `/by_concern/5/severity_levels/2/contraindicated_combos/0`<br>`/by_concern/5/severity_levels/2/sequence` | 「CO2 후 당일 필러 금지」 와 sequence 의 「… CO2 프락셔널 → PRP 즉시 도포 → 필러(남은 함몰)」: sequence 는 필러 간격을 적지 않아, 금지 조건(당일)과 합쳐 읽어야 같은 날이 아님이 드러난다. 두 필드를 함께 보존해야 한다. |

### 수동 수집 구절 (40건 · 구간은 expressions.json `source=manual_direct_reading`)

| Pointer | 원문 구절 | 탐색 관점(kinds) |
|---|---|---|
| `/by_concern/5/concern` | 여드름/흉터 | target_concern, slash_non_alternative |
| `/by_concern/5/concern_en` | Acne / Acne Scars | language_en, slash_non_alternative |
| `/by_concern/5/severity_levels/0/level` | (활성 여드름 위주) | parenthetical, severity, approximation, target_condition |
| `/by_concern/5/severity_levels/0/optimal_combo/1` | 필링(살리실산/글리콜산) | procedure_like, material, parenthetical, alternative |
| `/by_concern/5/severity_levels/0/optimal_combo/2` | LED(블루라이트) | procedure_like, parenthetical |
| `/by_concern/5/severity_levels/0/sequence` | 2주 간격 필링 | interval_repeat_or_after, time |
| `/by_concern/5/severity_levels/0/sequence` | LED(매회 마무리) | parenthetical, every_session, order_sequence |
| `/by_concern/5/severity_levels/0/rationale` | PDT로 피지선 억제 | effect_mechanism, abbreviation |
| `/by_concern/5/severity_levels/0/rationale` | 필링으로 각질/모공 관리 | effect_purpose, slash_non_alternative |
| `/by_concern/5/severity_levels/0/rationale` | LED로 항균/항염 | effect_purpose, slash_non_alternative |
| `/by_concern/5/severity_levels/0/expected_sessions` | PDT 3-5회 | session_count, range |
| `/by_concern/5/severity_levels/0/expected_sessions` | 필링 5-8회 | session_count, range |
| `/by_concern/5/severity_levels/0/expected_sessions` | LED 매회 | every_session |
| `/by_concern/5/severity_levels/1/level` | (여드름 흉터 위주) | parenthetical, severity, approximation, target_condition |
| `/by_concern/5/severity_levels/1/optimal_combo/1` | 서브시전(subcision) | procedure_like, parenthetical, language_en |
| `/by_concern/5/severity_levels/1/sequence` | 서브시전(깊은 흉터 박리) | parenthetical, layer_depth, degree_modifier, manner |
| `/by_concern/5/severity_levels/1/sequence` | 4주 후 프락셔널/니들RF | interval_after, time, alternative |
| `/by_concern/5/severity_levels/1/sequence` | PRP 동시 도포 | same_time, manner |
| `/by_concern/5/severity_levels/1/rationale` | 서브시전으로 섬유화 박리 | effect_mechanism |
| `/by_concern/5/severity_levels/1/rationale` | 프락셔널로 표면 리모델링 | effect_purpose, layer_depth |
| `/by_concern/5/severity_levels/1/rationale` | PRP로 재생 촉진 | effect_purpose, effect_complement |
| `/by_concern/5/severity_levels/1/expected_sessions` | 서브시전 1-3회 | session_count, range |
| `/by_concern/5/severity_levels/1/expected_sessions` | 프락셔널 3-5회 | session_count, range |
| `/by_concern/5/severity_levels/1/contraindicated_combos/0` | 활성 여드름 시 프락셔널 금지(감염 확산) | avoid_prohibit, condition_when, target_condition, parenthetical, risk_reason |
| `/by_concern/5/severity_levels/2/level` | (깊은 박스카/아이스픽 흉터) | parenthetical, severity, layer_depth, slash_non_alternative |
| `/by_concern/5/severity_levels/2/optimal_combo/2` | 필러(HA/CaHA) | procedure_like, material, parenthetical, alternative |
| `/by_concern/5/severity_levels/2/optimal_combo/4` | PRP/엑소좀 | procedure_like, slash_ambiguous |
| `/by_concern/5/severity_levels/2/sequence` | 서브시전 + TCA Cross(아이스픽) | plus_list, parenthetical, target_condition, language_en |
| `/by_concern/5/severity_levels/2/sequence` | 4주 후 CO2 프락셔널 | interval_after, time |
| `/by_concern/5/severity_levels/2/sequence` | PRP 즉시 도포 | immediately_after, time, manner |
| `/by_concern/5/severity_levels/2/sequence` | 필러(남은 함몰) | parenthetical, target_condition, interval_unspecified |
| `/by_concern/5/severity_levels/2/rationale` | 서브시전+TCA로 깊은 흉터 기저부 치료 | plus_list, layer_depth, degree_modifier, effect_purpose, abbreviation |
| `/by_concern/5/severity_levels/2/rationale` | CO2로 전체 리서페이싱 | effect_purpose, range_area |
| `/by_concern/5/severity_levels/2/rationale` | PRP 재생 | effect_purpose |
| `/by_concern/5/severity_levels/2/rationale` | 필러로 잔여 함몰 보충 | effect_purpose, target_condition |
| `/by_concern/5/severity_levels/2/expected_sessions` | 서브시전 2-3회 | session_count, range |
| `/by_concern/5/severity_levels/2/expected_sessions` | TCA Cross 3-5회 | session_count, range |
| `/by_concern/5/severity_levels/2/total_duration` | 12-18개월 | time, range |
| `/by_concern/5/severity_levels/2/contraindicated_combos/0` | CO2 후 당일 필러 금지 | avoid_prohibit, same_day, order_sequence |
| `/by_concern/5/severity_levels/2/contraindicated_combos/1` | 활성 여드름 시 침습 시술 금지 | avoid_prohibit, condition_when, target_condition, category_term |

### 이 구획의 미결 (issues.md 에 모음)

- **I-06-1** [I] 중등도: optimal_combo 「MTS/니들RF」, sequence 「프락셔널/니들RF」, sessions 는 프락셔널·니들RF 를 따로 셈(원문 내 불일치 후보). — `/by_concern/5/severity_levels/1/optimal_combo/2`, `/by_concern/5/severity_levels/1/sequence`, `/by_concern/5/severity_levels/1/expected_sessions`
- **B-06-1** [B] 「침습 시술」 의 범위가 원문에 없다. — `/by_concern/5/severity_levels/2/contraindicated_combos/1`
- **B-06-2** [B] 「매회」 가 어느 시술의 회차를 가리키는지, 「2주 간격」 이 반복인지 원문에 없다. — `/by_concern/5/severity_levels/0/sequence`

<a id="seg-07"></a>
## SEG-07 — by_concern/6

- 직접 읽기: **direct_read_done** — /by_concern/6 (제모) 전체 필드와 severity_levels 3단계를 원문 순서로 직접 읽음
- 소유 노드 40 · 말단(빈 컨테이너 포함) 30

### 원문 값 (자동 생성 · 원본 컬럼명 그대로 · 원본 순서)

| Pointer | 원본 컬럼명 | 자료형 | 원문 값 |
|---|---|---|---|
| `/by_concern/6` | `by_concern[6]` | object(4) | _키: concern, concern_en, icon, severity_levels_ |
| `/by_concern/6/concern` | `concern` | string | "제모" |
| `/by_concern/6/concern_en` | `concern_en` | string | "Hair Removal" |
| `/by_concern/6/icon` | `icon` | string | "laser" |
| `/by_concern/6/severity_levels` | `severity_levels` | array(3) | _원소 3개_ |
| `/by_concern/6/severity_levels/0` | `severity_levels[0]` | object(8) | _키: level, optimal_combo, sequence, rationale, expected_sessions, total_duration, evidence_level, contraindicated_combos_ |
| `/by_concern/6/severity_levels/0/level` | `level` | string | "경미 (얇은 털, 소범위)" |
| `/by_concern/6/severity_levels/0/optimal_combo` | `optimal_combo` | array(1) | _원소 1개_ |
| `/by_concern/6/severity_levels/0/optimal_combo/0` | `optimal_combo[0]` | string | "다이오드 레이저(810nm)" |
| `/by_concern/6/severity_levels/0/sequence` | `sequence` | string | "다이오드 레이저 단독 → 4-6주 간격 반복" |
| `/by_concern/6/severity_levels/0/rationale` | `rationale` | string | "단일 파장 레이저로 멜라닌 타겟 → 모낭 파괴. 소범위는 단일 기기로 충분" |
| `/by_concern/6/severity_levels/0/expected_sessions` | `expected_sessions` | string | "6-8회" |
| `/by_concern/6/severity_levels/0/total_duration` | `total_duration` | string | "6-12개월" |
| `/by_concern/6/severity_levels/0/evidence_level` | `evidence_level` | string | "high" |
| `/by_concern/6/severity_levels/0/contraindicated_combos` | `contraindicated_combos` | array(0) | _[]_ |
| `/by_concern/6/severity_levels/1` | `severity_levels[1]` | object(8) | _키: level, optimal_combo, sequence, rationale, expected_sessions, total_duration, evidence_level, contraindicated_combos_ |
| `/by_concern/6/severity_levels/1/level` | `level` | string | "중등도 (보통 굵기, 중범위)" |
| `/by_concern/6/severity_levels/1/optimal_combo` | `optimal_combo` | array(2) | _원소 2개_ |
| `/by_concern/6/severity_levels/1/optimal_combo/0` | `optimal_combo[0]` | string | "알렉산드라이트(755nm)" |
| `/by_concern/6/severity_levels/1/optimal_combo/1` | `optimal_combo[1]` | string | "다이오드(810nm)" |
| `/by_concern/6/severity_levels/1/sequence` | `sequence` | string | "알렉산드라이트 or 다이오드 → 4-6주 간격. 피부톤에 따라 선택" |
| `/by_concern/6/severity_levels/1/rationale` | `rationale` | string | "밝은 피부: 알렉산드라이트(효과적). 어두운 피부: 다이오드/Nd:YAG(안전). 필요시 교차 사용" |
| `/by_concern/6/severity_levels/1/expected_sessions` | `expected_sessions` | string | "6-10회" |
| `/by_concern/6/severity_levels/1/total_duration` | `total_duration` | string | "8-15개월" |
| `/by_concern/6/severity_levels/1/evidence_level` | `evidence_level` | string | "high" |
| `/by_concern/6/severity_levels/1/contraindicated_combos` | `contraindicated_combos` | array(1) | _원소 1개_ |
| `/by_concern/6/severity_levels/1/contraindicated_combos/0` | `contraindicated_combos[0]` | string | "제모 후 2주 내 왁싱/전기분해 금지" |
| `/by_concern/6/severity_levels/2` | `severity_levels[2]` | object(8) | _키: level, optimal_combo, sequence, rationale, expected_sessions, total_duration, evidence_level, contraindicated_combos_ |
| `/by_concern/6/severity_levels/2/level` | `level` | string | "중증 (굵은 털, 대범위/다부위)" |
| `/by_concern/6/severity_levels/2/optimal_combo` | `optimal_combo` | array(2) | _원소 2개_ |
| `/by_concern/6/severity_levels/2/optimal_combo/0` | `optimal_combo[0]` | string | "듀얼파장(알렉+다이오드 or 다이오드+Nd:YAG)" |
| `/by_concern/6/severity_levels/2/optimal_combo/1` | `optimal_combo[1]` | string | "IPL(유지)" |
| `/by_concern/6/severity_levels/2/sequence` | `sequence` | string | "듀얼파장 레이저 → 8-10회 → 이후 IPL로 잔여 유지" |
| `/by_concern/6/severity_levels/2/rationale` | `rationale` | string | "듀얼파장으로 다양한 깊이의 모낭 동시 타겟 → 완료 후 IPL로 장기 유지" |
| `/by_concern/6/severity_levels/2/expected_sessions` | `expected_sessions` | string | "레이저 8-12회 + IPL 유지 2-4회/년" |
| `/by_concern/6/severity_levels/2/total_duration` | `total_duration` | string | "12-18개월 + 유지" |
| `/by_concern/6/severity_levels/2/evidence_level` | `evidence_level` | string | "high" |
| `/by_concern/6/severity_levels/2/contraindicated_combos` | `contraindicated_combos` | array(2) | _원소 2개_ |
| `/by_concern/6/severity_levels/2/contraindicated_combos/0` | `contraindicated_combos[0]` | string | "제모 부위 필링/프락셔널 동시 금지" |
| `/by_concern/6/severity_levels/2/contraindicated_combos/1` | `contraindicated_combos[1]` | string | "선탠 후 2주 내 레이저 제모 금지" |

### 잠정 관찰 (직접 읽기 · 원문 칸과 분리 · 확정 의미 아님)

| ID | 상태 | 근거 Pointer | 관찰 |
|---|---|---|---|
| O07-1 | P | `/by_concern/6/severity_levels/0/level`<br>`/by_concern/6/severity_levels/1/level`<br>`/by_concern/6/severity_levels/2/level` | 제모 단계는 털 굵기(얇은·보통 굵기·굵은)와 범위(소범위·중범위·대범위/다부위) 두 축을 괄호 안에 함께 적는다. 다른 고민의 단계와 축이 다르다. |
| O07-2 | P | `/by_concern/6/severity_levels/0/optimal_combo/0`<br>`/by_concern/6/severity_levels/1/optimal_combo/0`<br>`/by_concern/6/severity_levels/1/optimal_combo/1` | 괄호 안 파장 「(810nm)」「(755nm)」: 수치+단위를 보존. 다른 기기(Nd:YAG)의 파장은 원문에 없다(값을 채우지 않음). |
| O07-3 | P | `/by_concern/6/severity_levels/0/sequence`<br>`/by_concern/6/severity_levels/0/expected_sessions` | 「다이오드 레이저 단독 → 4-6주 간격 반복」: 단독(조합 없음)이 optimal_combo 칸 이름(조합)과 긴장. expected_sessions 「6-8회」 는 시술명 없이 회차만. |
| O07-4 | P | `/by_concern/6/severity_levels/0/rationale` | 「… 모낭 파괴. 소범위는 단일 기기로 충분」: 두 번째 문장은 범위 조건(소범위는) → 충분 판단. 「충분」 은 정도 판단 표현. |
| O07-5 | P | `/by_concern/6/severity_levels/1/sequence`<br>`/by_concern/6/severity_levels/1/rationale` | 중등도: 「알렉산드라이트 or 다이오드 → 4-6주 간격. 피부톤에 따라 선택」, rationale 「밝은 피부: 알렉산드라이트(효과적). 어두운 피부: 다이오드/Nd:YAG(안전). 필요시 교차 사용」. 대상 조건(피부톤) → 기기 선택, 괄호는 평가(효과적·안전), 「필요시」 조건부 교차. 피부톤 기준(밝은/어두운)의 구분값은 원문에 없다(B). |
| O07-6 | I | `/by_concern/6/severity_levels/1/rationale`<br>`/by_concern/6/severity_levels/1/optimal_combo` | rationale 은 어두운 피부에 「다이오드/Nd:YAG」 를 들지만 중등도 optimal_combo 에 Nd:YAG 가 없다(원문 내 불일치 후보). |
| O07-7 | P | `/by_concern/6/severity_levels/1/contraindicated_combos/0` | 「제모 후 2주 내 왁싱/전기분해 금지」: 레이저 제모 뒤 다른 제모 방식 금지(기간 조건). `/` 는 둘 다 금지로 읽힌다(README 「둘 중 하나」 와 다른 쓰임 후보). |
| O07-8 | P | `/by_concern/6/severity_levels/2/optimal_combo/0`<br>`/by_concern/6/severity_levels/2/sequence`<br>`/by_concern/6/severity_levels/2/expected_sessions` | 「듀얼파장(알렉+다이오드 or 다이오드+Nd:YAG)」: 괄호 안에서 `+` 는 한 기기의 두 파장 조합, `or` 는 두 조합 사이 대안. 「알렉」 은 알렉산드라이트 축약(F). sequence 「→ 8-10회 →」 는 순서 칸에 회차를 넣었고, sessions 는 「레이저 8-12회」 로 범위가 다르다. |
| O07-9 | P | `/by_concern/6/severity_levels/2/expected_sessions`<br>`/by_concern/6/severity_levels/2/total_duration` | 「IPL 유지 2-4회/년」(빈도 단위 /년), 「12-18개월 + 유지」(기간 + 끝이 열린 유지). `/` 가 「매」 의 뜻으로 쓰였다. |
| O07-10 | P | `/by_concern/6/severity_levels/2/contraindicated_combos/0`<br>`/by_concern/6/severity_levels/2/contraindicated_combos/1` | 「제모 부위 필링/프락셔널 동시 금지」: 부위 조건(제모 부위) + 동시. 「선탠 후 2주 내 레이저 제모 금지」: 시술이 아닌 생활 사건(선탠) 후 기간 조건. |
| O07-11 | P | `/by_concern/6/icon` | icon 「laser」 는 다른 고민의 icon(wrinkle·lifting·volume…)과 달리 고민이 아닌 기기 계열 이름이다. 아이콘 식별자로만 보존. |

### 수동 수집 구절 (32건 · 구간은 expressions.json `source=manual_direct_reading`)

| Pointer | 원문 구절 | 탐색 관점(kinds) |
|---|---|---|
| `/by_concern/6/severity_levels/0/level` | (얇은 털, 소범위) | parenthetical, severity, degree_modifier, range_area |
| `/by_concern/6/severity_levels/0/optimal_combo/0` | 다이오드 레이저(810nm) | procedure_like, parenthetical, quantity_unit, wavelength |
| `/by_concern/6/severity_levels/0/sequence` | 다이오드 레이저 단독 | monotherapy |
| `/by_concern/6/severity_levels/0/sequence` | 4-6주 간격 반복 | interval_repeat, range, time |
| `/by_concern/6/severity_levels/0/rationale` | 단일 파장 레이저로 멜라닌 타겟 | effect_mechanism, wavelength |
| `/by_concern/6/severity_levels/0/rationale` | 모낭 파괴 | effect_mechanism |
| `/by_concern/6/severity_levels/0/rationale` | 소범위는 단일 기기로 충분 | condition, range_area, sufficiency |
| `/by_concern/6/severity_levels/0/expected_sessions` | 6-8회 | session_count, range |
| `/by_concern/6/severity_levels/1/level` | (보통 굵기, 중범위) | parenthetical, severity, degree_modifier, range_area |
| `/by_concern/6/severity_levels/1/optimal_combo/0` | 알렉산드라이트(755nm) | procedure_like, parenthetical, quantity_unit, wavelength |
| `/by_concern/6/severity_levels/1/optimal_combo/1` | 다이오드(810nm) | procedure_like, parenthetical, quantity_unit, wavelength |
| `/by_concern/6/severity_levels/1/sequence` | 알렉산드라이트 or 다이오드 | alternative, language_en |
| `/by_concern/6/severity_levels/1/sequence` | 4-6주 간격 | interval_repeat_or_after, range, time |
| `/by_concern/6/severity_levels/1/sequence` | 피부톤에 따라 선택 | condition, skin_type, selection |
| `/by_concern/6/severity_levels/1/rationale` | 밝은 피부: 알렉산드라이트(효과적) | condition, skin_type, parenthetical, evaluation |
| `/by_concern/6/severity_levels/1/rationale` | 어두운 피부: 다이오드/Nd:YAG(안전) | condition, skin_type, alternative, parenthetical, evaluation |
| `/by_concern/6/severity_levels/1/rationale` | 필요시 교차 사용 | condition_when, alternate_cross |
| `/by_concern/6/severity_levels/1/expected_sessions` | 6-10회 | session_count, range |
| `/by_concern/6/severity_levels/1/total_duration` | 8-15개월 | time, range |
| `/by_concern/6/severity_levels/1/contraindicated_combos/0` | 제모 후 2주 내 왁싱/전기분해 금지 | avoid_prohibit, interval_within, time, order_sequence, slash_ambiguous |
| `/by_concern/6/severity_levels/2/level` | (굵은 털, 대범위/다부위) | parenthetical, severity, degree_modifier, range_area, slash_non_alternative |
| `/by_concern/6/severity_levels/2/optimal_combo/0` | 듀얼파장(알렉+다이오드 or 다이오드+Nd:YAG) | procedure_like, parenthetical, plus_list, alternative, wavelength, abbreviation |
| `/by_concern/6/severity_levels/2/optimal_combo/1` | IPL(유지) | procedure_like, parenthetical, maintenance |
| `/by_concern/6/severity_levels/2/sequence` | → 8-10회 → | session_count, range, order_sequence |
| `/by_concern/6/severity_levels/2/sequence` | 이후 IPL로 잔여 유지 | after_phase, maintenance, target_condition |
| `/by_concern/6/severity_levels/2/rationale` | 듀얼파장으로 다양한 깊이의 모낭 동시 타겟 | effect_mechanism, layer_depth, same_time, wavelength |
| `/by_concern/6/severity_levels/2/rationale` | 완료 후 IPL로 장기 유지 | after_phase, maintenance, duration_long |
| `/by_concern/6/severity_levels/2/expected_sessions` | 레이저 8-12회 | session_count, range |
| `/by_concern/6/severity_levels/2/expected_sessions` | IPL 유지 2-4회/년 | maintenance, frequency, range, slash_per |
| `/by_concern/6/severity_levels/2/total_duration` | 12-18개월 + 유지 | time, range, maintenance, open_ended |
| `/by_concern/6/severity_levels/2/contraindicated_combos/0` | 제모 부위 필링/프락셔널 동시 금지 | avoid_prohibit, body_part, same_time, slash_ambiguous |
| `/by_concern/6/severity_levels/2/contraindicated_combos/1` | 선탠 후 2주 내 레이저 제모 금지 | avoid_prohibit, lifestyle_event, interval_within, time |

### 이 구획의 미결 (issues.md 에 모음)

- **I-07-1** [I] 중등도 rationale 의 Nd:YAG 가 optimal_combo 에 없다(원문 내 불일치 후보). — `/by_concern/6/severity_levels/1/rationale`, `/by_concern/6/severity_levels/1/optimal_combo`
- **B-07-1** [B] 피부톤(밝은/어두운) 구분 기준과 「필요시」 조건이 원문에 없다. — `/by_concern/6/severity_levels/1/rationale`, `/by_concern/6/severity_levels/1/sequence`

<a id="seg-08"></a>
## SEG-08 — by_concern/7

- 직접 읽기: **direct_read_done** — /by_concern/7 (바디컨투어링) 전체 필드와 severity_levels 3단계를 원문 순서로 직접 읽음
- 소유 노드 44 · 말단(빈 컨테이너 포함) 34

### 원문 값 (자동 생성 · 원본 컬럼명 그대로 · 원본 순서)

| Pointer | 원본 컬럼명 | 자료형 | 원문 값 |
|---|---|---|---|
| `/by_concern/7` | `by_concern[7]` | object(4) | _키: concern, concern_en, icon, severity_levels_ |
| `/by_concern/7/concern` | `concern` | string | "바디컨투어링" |
| `/by_concern/7/concern_en` | `concern_en` | string | "Body Contouring" |
| `/by_concern/7/icon` | `icon` | string | "body" |
| `/by_concern/7/severity_levels` | `severity_levels` | array(3) | _원소 3개_ |
| `/by_concern/7/severity_levels/0` | `severity_levels[0]` | object(8) | _키: level, optimal_combo, sequence, rationale, expected_sessions, total_duration, evidence_level, contraindicated_combos_ |
| `/by_concern/7/severity_levels/0/level` | `level` | string | "경미 (가벼운 부분 지방)" |
| `/by_concern/7/severity_levels/0/optimal_combo` | `optimal_combo` | array(2) | _원소 2개_ |
| `/by_concern/7/severity_levels/0/optimal_combo/0` | `optimal_combo[0]` | string | "크라이오(냉동지방분해)" |
| `/by_concern/7/severity_levels/0/optimal_combo/1` | `optimal_combo[1]` | string | "고주파 바디 RF" |
| `/by_concern/7/severity_levels/0/sequence` | `sequence` | string | "크라이오 먼저 → 2주 후부터 RF 4-6회" |
| `/by_concern/7/severity_levels/0/rationale` | `rationale` | string | "냉동으로 지방세포 아포토시스 → RF로 피부 타이트닝/추가 지방 대사" |
| `/by_concern/7/severity_levels/0/expected_sessions` | `expected_sessions` | string | "크라이오 1-2회 + RF 4-6회" |
| `/by_concern/7/severity_levels/0/total_duration` | `total_duration` | string | "3-6개월" |
| `/by_concern/7/severity_levels/0/evidence_level` | `evidence_level` | string | "moderate" |
| `/by_concern/7/severity_levels/0/contraindicated_combos` | `contraindicated_combos` | array(0) | _[]_ |
| `/by_concern/7/severity_levels/1` | `severity_levels[1]` | object(8) | _키: level, optimal_combo, sequence, rationale, expected_sessions, total_duration, evidence_level, contraindicated_combos_ |
| `/by_concern/7/severity_levels/1/level` | `level` | string | "중등도 (부분 비만, 셀룰라이트)" |
| `/by_concern/7/severity_levels/1/optimal_combo` | `optimal_combo` | array(4) | _원소 4개_ |
| `/by_concern/7/severity_levels/1/optimal_combo/0` | `optimal_combo[0]` | string | "지방분해주사(데옥시콜산)" |
| `/by_concern/7/severity_levels/1/optimal_combo/1` | `optimal_combo[1]` | string | "크라이오" |
| `/by_concern/7/severity_levels/1/optimal_combo/2` | `optimal_combo[2]` | string | "바디 RF" |
| `/by_concern/7/severity_levels/1/optimal_combo/3` | `optimal_combo[3]` | string | "카복시테라피" |
| `/by_concern/7/severity_levels/1/sequence` | `sequence` | string | "지방분해주사 or 크라이오 → 4주 간격 반복 → RF로 타이트닝 → 카복시로 순환 개선" |
| `/by_concern/7/severity_levels/1/rationale` | `rationale` | string | "지방분해(화학적/물리적) → RF로 늘어진 피부 관리 → 카복시로 혈류/림프순환 개선" |
| `/by_concern/7/severity_levels/1/expected_sessions` | `expected_sessions` | string | "지방분해주사 3-5회 or 크라이오 2-3회 + RF 6-8회 + 카복시 5회" |
| `/by_concern/7/severity_levels/1/total_duration` | `total_duration` | string | "4-8개월" |
| `/by_concern/7/severity_levels/1/evidence_level` | `evidence_level` | string | "moderate" |
| `/by_concern/7/severity_levels/1/contraindicated_combos` | `contraindicated_combos` | array(1) | _원소 1개_ |
| `/by_concern/7/severity_levels/1/contraindicated_combos/0` | `contraindicated_combos[0]` | string | "지방분해주사 후 24시간 내 RF 금지" |
| `/by_concern/7/severity_levels/2` | `severity_levels[2]` | object(8) | _키: level, optimal_combo, sequence, rationale, expected_sessions, total_duration, evidence_level, contraindicated_combos_ |
| `/by_concern/7/severity_levels/2/level` | `level` | string | "중증 (광범위 체형 관리)" |
| `/by_concern/7/severity_levels/2/optimal_combo` | `optimal_combo` | array(4) | _원소 4개_ |
| `/by_concern/7/severity_levels/2/optimal_combo/0` | `optimal_combo[0]` | string | "지방흡입(리포)" |
| `/by_concern/7/severity_levels/2/optimal_combo/1` | `optimal_combo[1]` | string | "바디 HIFU(리포셀)" |
| `/by_concern/7/severity_levels/2/optimal_combo/2` | `optimal_combo[2]` | string | "RF 타이트닝" |
| `/by_concern/7/severity_levels/2/optimal_combo/3` | `optimal_combo[3]` | string | "카복시테라피" |
| `/by_concern/7/severity_levels/2/sequence` | `sequence` | string | "지방흡입(수술) → 4-6주 회복 → 바디 HIFU/RF로 잔여 지방+타이트닝 → 카복시 유지" |
| `/by_concern/7/severity_levels/2/rationale` | `rationale` | string | "지방흡입으로 대량 제거 → 비수술로 잔여 윤곽 다듬기 + 피부 탄력 회복" |
| `/by_concern/7/severity_levels/2/expected_sessions` | `expected_sessions` | string | "지방흡입 1회 + HIFU 2-3회 + RF 4-6회 + 카복시 5회" |
| `/by_concern/7/severity_levels/2/total_duration` | `total_duration` | string | "6-12개월" |
| `/by_concern/7/severity_levels/2/evidence_level` | `evidence_level` | string | "moderate" |
| `/by_concern/7/severity_levels/2/contraindicated_combos` | `contraindicated_combos` | array(1) | _원소 1개_ |
| `/by_concern/7/severity_levels/2/contraindicated_combos/0` | `contraindicated_combos[0]` | string | "지방흡입 후 4주 내 RF/HIFU 금지" |

### 잠정 관찰 (직접 읽기 · 원문 칸과 분리 · 확정 의미 아님)

| ID | 상태 | 근거 Pointer | 관찰 |
|---|---|---|---|
| O08-1 | P | `/by_concern/7/severity_levels/0/optimal_combo/0`<br>`/by_concern/7/severity_levels/0/optimal_combo/1` | 「크라이오(냉동지방분해)」 괄호는 한국어 풀이, 「고주파 바디 RF」 는 한국어(고주파)와 영어 약어(RF)가 같은 뜻으로 겹친 이름(잠정). |
| O08-2 | P | `/by_concern/7/severity_levels/0/sequence` | 「크라이오 먼저 → 2주 후부터 RF 4-6회」: 「후부터」 는 시작 시점 이후 시리즈. 순서 칸 안에 회차(4-6회)가 들어 있다. |
| O08-3 | P | `/by_concern/7/severity_levels/0/rationale` | 「냉동으로 지방세포 아포토시스 → RF로 피부 타이트닝/추가 지방 대사」: 기전 서술. 「추가」 는 보완 효과 표현. |
| O08-4 | P | `/by_concern/7/severity_levels/1/sequence`<br>`/by_concern/7/severity_levels/1/expected_sessions` | 「지방분해주사 or 크라이오 → 4주 간격 반복 → RF로 타이트닝 → 카복시로 순환 개선」, sessions 「지방분해주사 3-5회 or 크라이오 2-3회 + RF 6-8회 + 카복시 5회」: `or` 대안이 회차까지 이어진다. `or` 와 `+` 의 결합 범위(어디까지 묶이나)는 원문에 괄호가 없어 구조적으로 모호하다. |
| O08-5 | P | `/by_concern/7/severity_levels/1/rationale` | 「지방분해(화학적/물리적)」: 괄호가 방식 두 가지를 나열하며, 순서상 지방분해주사(화학적)·크라이오(물리적)에 대응하는 것으로 읽히나 원문은 대응을 명시하지 않는다. |
| O08-6 | P | `/by_concern/7/severity_levels/1/contraindicated_combos/0` | 「지방분해주사 후 24시간 내 RF 금지」: 시간 단위 「시간」. 같은 단계 sequence 는 지방분해주사 뒤 반복 후 RF 로 이어져 간격을 적지 않았다. |
| O08-7 | P | `/by_concern/7/severity_levels/2/optimal_combo/0`<br>`/by_concern/7/severity_levels/2/optimal_combo/1`<br>`/by_concern/7/severity_levels/2/sequence` | 「지방흡입(리포)」 괄호는 약칭, 「바디 HIFU(리포셀)」 괄호는 제품/장비명으로 읽힌다(잠정). sequence 「지방흡입(수술)」 괄호는 범주(수술), rationale 은 나머지를 「비수술」 로 대조한다. |
| O08-8 | P | `/by_concern/7/severity_levels/2/sequence` | 「4-6주 회복」: 다음 시술 전 회복 기간을 시술처럼 순서에 넣었다. 「바디 HIFU/RF로 잔여 지방+타이트닝」 은 `/` 대안·`+` 효과 나열이 한 구절에 섞인다. 다만 sessions 는 HIFU 와 RF 를 따로 센다(「HIFU 2-3회 + RF 4-6회」), `/` 가 대안인지 병용인지 원문만으로 정하지 않았다. |
| O08-9 | P | `/by_concern/7/severity_levels/2/contraindicated_combos/0`<br>`/by_concern/7/severity_levels/2/sequence` | 「지방흡입 후 4주 내 RF/HIFU 금지」 와 sequence 「4-6주 회복 →」: 금지 기간(4주 내)과 회복 기간(4-6주) 하한이 같은 4주다. 두 값을 같은 사실로 합치지 않았다. |
| O08-10 | F | `/by_concern/7/severity_levels/2/optimal_combo/2`<br>`/by_concern/7/severity_levels/1/optimal_combo/2`<br>`/by_concern/7/severity_levels/0/optimal_combo/1` | RF 계열 이름이 단계마다 다르다: 「고주파 바디 RF」·「바디 RF」·「RF 타이트닝」. |
| O08-11 | F | `/by_concern/7/severity_levels/1/optimal_combo/3`<br>`/by_concern/7/severity_levels/1/sequence` | 「카복시테라피」 를 sequence·rationale·sessions 는 「카복시」 로 줄여 쓴다. |

### 수동 수집 구절 (33건 · 구간은 expressions.json `source=manual_direct_reading`)

| Pointer | 원문 구절 | 탐색 관점(kinds) |
|---|---|---|
| `/by_concern/7/severity_levels/0/level` | (가벼운 부분 지방) | parenthetical, severity, degree_modifier, range_area |
| `/by_concern/7/severity_levels/0/optimal_combo/0` | 크라이오(냉동지방분해) | procedure_like, parenthetical, gloss |
| `/by_concern/7/severity_levels/0/optimal_combo/1` | 고주파 바디 RF | procedure_like, body_part, language_mixed |
| `/by_concern/7/severity_levels/0/sequence` | 크라이오 먼저 | order_sequence |
| `/by_concern/7/severity_levels/0/sequence` | 2주 후부터 RF 4-6회 | interval_after, time_from, session_count, range |
| `/by_concern/7/severity_levels/0/rationale` | 냉동으로 지방세포 아포토시스 | effect_mechanism |
| `/by_concern/7/severity_levels/0/rationale` | RF로 피부 타이트닝/추가 지방 대사 | effect_purpose, additional, slash_non_alternative |
| `/by_concern/7/severity_levels/0/expected_sessions` | 크라이오 1-2회 | session_count, range |
| `/by_concern/7/severity_levels/0/expected_sessions` | RF 4-6회 | session_count, range |
| `/by_concern/7/severity_levels/1/level` | (부분 비만, 셀룰라이트) | parenthetical, severity, range_area, target_condition |
| `/by_concern/7/severity_levels/1/optimal_combo/0` | 지방분해주사(데옥시콜산) | procedure_like, parenthetical, ingredient |
| `/by_concern/7/severity_levels/1/sequence` | 지방분해주사 or 크라이오 | alternative, language_en |
| `/by_concern/7/severity_levels/1/sequence` | 4주 간격 반복 | interval_repeat, time |
| `/by_concern/7/severity_levels/1/sequence` | RF로 타이트닝 | effect_purpose, interval_unspecified |
| `/by_concern/7/severity_levels/1/sequence` | 카복시로 순환 개선 | effect_purpose, abbreviation, interval_unspecified |
| `/by_concern/7/severity_levels/1/rationale` | 지방분해(화학적/물리적) | parenthetical, manner, slash_non_alternative |
| `/by_concern/7/severity_levels/1/rationale` | RF로 늘어진 피부 관리 | effect_purpose, target_condition |
| `/by_concern/7/severity_levels/1/rationale` | 카복시로 혈류/림프순환 개선 | effect_purpose, slash_non_alternative |
| `/by_concern/7/severity_levels/1/expected_sessions` | 지방분해주사 3-5회 or 크라이오 2-3회 | session_count, range, alternative, language_en |
| `/by_concern/7/severity_levels/1/expected_sessions` | RF 6-8회 | session_count, range |
| `/by_concern/7/severity_levels/1/contraindicated_combos/0` | 지방분해주사 후 24시간 내 RF 금지 | avoid_prohibit, interval_within, time, order_sequence |
| `/by_concern/7/severity_levels/2/level` | (광범위 체형 관리) | parenthetical, severity, range_area, degree_modifier |
| `/by_concern/7/severity_levels/2/optimal_combo/0` | 지방흡입(리포) | procedure_like, parenthetical, abbreviation |
| `/by_concern/7/severity_levels/2/optimal_combo/1` | 바디 HIFU(리포셀) | procedure_like, product_like, parenthetical, body_part |
| `/by_concern/7/severity_levels/2/sequence` | 지방흡입(수술) | parenthetical, category_term, surgery |
| `/by_concern/7/severity_levels/2/sequence` | 4-6주 회복 | recovery_period, range, time |
| `/by_concern/7/severity_levels/2/sequence` | 바디 HIFU/RF로 잔여 지방+타이트닝 | slash_ambiguous, plus_list, effect_purpose, target_condition |
| `/by_concern/7/severity_levels/2/sequence` | 카복시 유지 | maintenance, abbreviation |
| `/by_concern/7/severity_levels/2/rationale` | 지방흡입으로 대량 제거 | effect_purpose, degree_modifier, quantity_vague |
| `/by_concern/7/severity_levels/2/rationale` | 비수술로 잔여 윤곽 다듬기 | category_term, negation, effect_purpose, target_condition |
| `/by_concern/7/severity_levels/2/rationale` | 피부 탄력 회복 | effect_purpose |
| `/by_concern/7/severity_levels/2/expected_sessions` | HIFU 2-3회 | session_count, range |
| `/by_concern/7/severity_levels/2/contraindicated_combos/0` | 지방흡입 후 4주 내 RF/HIFU 금지 | avoid_prohibit, interval_within, time, order_sequence, alternative |

### 이 구획의 미결 (issues.md 에 모음)

- **B-08-1** [B] `or` 와 `+` 의 결합 범위가 원문 표기만으로 정해지지 않는다(괄호 없음). — `/by_concern/7/severity_levels/1/sequence`, `/by_concern/7/severity_levels/1/expected_sessions`
- **B-08-2** [B] 「바디 HIFU/RF」 의 `/` 가 대안인지 병용인지 원문에 없다(sessions 는 따로 셈). — `/by_concern/7/severity_levels/2/sequence`, `/by_concern/7/severity_levels/2/expected_sessions`

