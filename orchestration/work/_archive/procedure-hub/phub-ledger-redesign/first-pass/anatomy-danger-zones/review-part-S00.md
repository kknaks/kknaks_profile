# S00 — 최상위 메타데이터 + critical_safety_facts + zones 배열 컨테이너

[← review.md](review.md) · 범위 `'' (루트 객체 자체), /version, /updated, /consensus_method, /critical_safety_facts/**, /zones (배열 컨테이너만; 원소는 S01~S11)` · 소유 노드 10 · 말단 7 · 직접 읽기 done

상위 문맥: 루트 객체. `/zones` 배열 컨테이너는 이 구획이 소유하고 원소 11개는 S01~S11 이 소유한다.

## 원문 값 (문서 순서 · 전부)

| # | JSON Pointer | 원본 컬럼명 | 배열 순번 | 자료형 | 원문 값 |
|---|---|---|---|---|---|
| 0 | `(root)` | `(루트)` |  | object{5} | (컨테이너 · 키: `version`, `updated`, `consensus_method`, `critical_safety_facts`, `zones`) |
| 1 | `/version` | `version` |  | string | 1.2 |
| 2 | `/updated` | `updated` |  | string | 2026-07-26 |
| 3 | `/consensus_method` | `consensus_method` |  | string | 3-AI Expert Consensus (Perplexity research + Gemini analysis + Claude textbook) |
| 4 | `/critical_safety_facts` | `critical_safety_facts` |  | object{4} | (컨테이너 · 키: `minimum_filler_for_blindness`, `blindness_highest_risk_zones`, `mechanism`, `caveat`) |
| 5 | `/critical_safety_facts/minimum_filler_for_blindness` | `minimum_filler_for_blindness` |  | string | 약 0.04mL (supratrochlear 0.0397mL, supraorbital 0.0409mL, dorsal nasal 0.0368mL; Yi et al., J Cosmet Dermatol 2024). Supratrochlear 단일 경로 부피는 약 0.085mL(범위 0.04-0.12mL; Khan et al., Aesthetic Surgery Journal 2017;37(2):203-208). 수치는 혈관 부피 기반 이론값으로 실제 임계량은 변이가 있어 절대 안전 기준이 아님 |
| 6 | `/critical_safety_facts/blindness_highest_risk_zones` | `blindness_highest_risk_zones` |  | string | 코 56.3%, 미간 27.1%, 이마 18.8%, 비순주름 14.6% (Beleznay et al., Aesthet Surg J 2019;39(6):662-674) — 코가 현재 최고위험부위 |
| 7 | `/critical_safety_facts/mechanism` | `mechanism` |  | string | 역행성 동맥 색전 — 안동맥(ophthalmic artery)으로 역류 → 망막 허혈 |
| 8 | `/critical_safety_facts/caveat` | `caveat` |  | string | 이 수치들은 시술자 경계를 느슨하게 만들지 말 것. 어떤 주사라도 혈관 내 주입이면 실명 가능. 흡인은 음성 결과가 안전을 보장하지 않는 보조 수단이며, 저압·저속·소량 주입·캐뉼러 사용·hyaluronidase 상비가 핵심 |
| 9 | `/zones` | `zones` |  | array[11] | (배열 · 11개) |

## 잠정 관찰 (원문 칸과 분리)

| # | 상태 | 근거 Pointer | 관찰 | issues.md |
|---|---|---|---|---|
| OBS-S00-01 | P | `/consensus_method` | 자료 생성 방식이 '3-AI Expert Consensus' 로 적혀 있다. 원장 전체 수치·권고의 출처 성격(문헌 인용과 AI 합의 혼재)을 보여주는 메타데이터다. 임상적 타당성은 1차에서 판단하지 않는다. | ADZ-B18 |
| OBS-S00-02 | P | `/critical_safety_facts/minimum_filler_for_blindness` | 한 값 안에 세 혈관별 수치(0.0397/0.0409/0.0368mL), 단일 경로 부피(0.085mL, 범위 0.04-0.12mL), 두 인용, 단서('절대 안전 기준이 아님')가 함께 있다. 수치와 단서를 분리하면 단서가 사라진다. |  |
| OBS-S00-03 | F | `/critical_safety_facts/blindness_highest_risk_zones` | 부위 이름 '코·미간·이마·비순주름'이 zones 의 name_ko(코·미간·이마·팔자주름)와 대응하는지 원문은 연결하지 않는다. '비순주름' 과 '팔자주름' 은 다른 표기다. | ADZ-F14 |
| OBS-S00-04 | P | `/critical_safety_facts/mechanism` | '—' 뒤 '→' 로 경로(역류→허혈)를 적었다. 화살표의 기능은 원장 안에서 여러 가지다. | ADZ-P09 |
| OBS-S00-05 | P | `/critical_safety_facts/caveat` | '이 수치들은' 은 같은 객체의 앞 필드 수치를 가리키는 지시 표현이다. 금지 지시('말 것'), 조건부 가능성('주입이면 실명 가능'), 부정('보장하지 않는') 이 한 값에 있다. |  |

## 수동 복합 표현 (직접 읽기)

탐색 관점은 수집용 꼬리표이며 확정 분류가 아니다. 구간은 값 문자열 기준 코드 포인트 `[start,end)`.

| ID | Pointer | 원문 구간 | 구간 | 탐색 관점 | 메모 |
|---|---|---|---|---|---|
| MX-S00-001 | `/consensus_method` | 3-AI Expert Consensus (Perplexity research + Gemini analysis + Claude textbook) | [0, 79] | 출처·방법, 기호(+) |  |
| MX-S00-002 | `/critical_safety_facts/minimum_filler_for_blindness` | 약 0.04mL | [0, 8] | 수량·단위, 근사(약) |  |
| MX-S00-003 | `/critical_safety_facts/minimum_filler_for_blindness` | supratrochlear 0.0397mL | [10, 33] | 영문 혈관 표기, 수량·단위 |  |
| MX-S00-004 | `/critical_safety_facts/minimum_filler_for_blindness` | supraorbital 0.0409mL | [35, 56] | 영문 혈관 표기, 수량·단위 |  |
| MX-S00-005 | `/critical_safety_facts/minimum_filler_for_blindness` | dorsal nasal 0.0368mL | [58, 79] | 영문 혈관 표기, 수량·단위 |  |
| MX-S00-006 | `/critical_safety_facts/minimum_filler_for_blindness` | Yi et al., J Cosmet Dermatol 2024 | [81, 114] | 인용 |  |
| MX-S00-007 | `/critical_safety_facts/minimum_filler_for_blindness` | Supratrochlear 단일 경로 부피는 약 0.085mL | [117, 151] | 수량·단위, 근사(약) |  |
| MX-S00-008 | `/critical_safety_facts/minimum_filler_for_blindness` | 범위 0.04-0.12mL | [152, 166] | 범위 |  |
| MX-S00-009 | `/critical_safety_facts/minimum_filler_for_blindness` | Khan et al., Aesthetic Surgery Journal 2017;37(2):203-208 | [168, 225] | 인용 |  |
| MX-S00-010 | `/critical_safety_facts/minimum_filler_for_blindness` | 수치는 혈관 부피 기반 이론값으로 실제 임계량은 변이가 있어 절대 안전 기준이 아님 | [228, 274] | 단서, 부정(아님), 불확실성 |  |
| MX-S00-011 | `/critical_safety_facts/blindness_highest_risk_zones` | 코 56.3% | [0, 7] | 부위+비율 |  |
| MX-S00-012 | `/critical_safety_facts/blindness_highest_risk_zones` | 미간 27.1% | [9, 17] | 부위+비율 |  |
| MX-S00-013 | `/critical_safety_facts/blindness_highest_risk_zones` | 이마 18.8% | [19, 27] | 부위+비율 |  |
| MX-S00-014 | `/critical_safety_facts/blindness_highest_risk_zones` | 비순주름 14.6% | [29, 39] | 부위+비율 | zones 에는 '팔자주름' |
| MX-S00-015 | `/critical_safety_facts/blindness_highest_risk_zones` | Beleznay et al., Aesthet Surg J 2019;39(6):662-674 | [41, 91] | 인용 |  |
| MX-S00-016 | `/critical_safety_facts/blindness_highest_risk_zones` | 코가 현재 최고위험부위 | [95, 107] | 시간(현재), 최상급 |  |
| MX-S00-017 | `/critical_safety_facts/mechanism` | 역행성 동맥 색전 — 안동맥(ophthalmic artery)으로 역류 → 망막 허혈 | [0, 47] | 경로(→), 영문 병기 |  |
| MX-S00-018 | `/critical_safety_facts/caveat` | 이 수치들은 시술자 경계를 느슨하게 만들지 말 것 | [0, 27] | 금지 지시, 지시 표현(이 수치들) |  |
| MX-S00-019 | `/critical_safety_facts/caveat` | 어떤 주사라도 혈관 내 주입이면 실명 가능 | [29, 52] | 조건(이면), 가능성 |  |
| MX-S00-020 | `/critical_safety_facts/caveat` | 흡인은 음성 결과가 안전을 보장하지 않는 보조 수단이며 | [54, 84] | 부정(않는) |  |
| MX-S00-021 | `/critical_safety_facts/caveat` | 저압·저속·소량 주입·캐뉼러 사용·hyaluronidase 상비가 핵심 | [86, 125] | 나열(·), 권고 |  |

## 정규식 보조 후보 (기계 · 요약)

| 패턴 | 출현 |
|---|---|
| plus | 2 |
| range | 4 |
| number_unit | 10 |
| negation_prohibition | 2 |
| degree_emphasis | 2 |
| citation | 3 |
| time_order | 1 |
| em_dash | 2 |
| arrow | 1 |
| possibility_frequency | 1 |
| condition | 1 |
| middle_dot | 4 |

전체 출현·구간은 `expressions.json` → `regex_candidates` (section=S00).

## 전문어 분절 관찰 (Kiwi 원시 · K)

| Pointer | 낱말 | 구간 | Kiwi 토큰 | 상태 |
|---|---|---|---|---|
| `/critical_safety_facts/mechanism` | 역행성 | [0, 3] | 역행/NNG + 성/XSN | K: 여러 형태소로 분절(원시 결과 보존) |

단일 형태소로 나온 출현은 표에서 생략했다(`morphology.json` → `segmentation_review` 에 전부 있음).

