# S02 — zones[1] glabella (미간 / Glabella)

[← review.md](review.md) · 범위 `/zones/1/**` · 소유 노드 52 · 말단 41 · 직접 읽기 done

상위 문맥: 루트 객체 → `zones` 배열(S00 소유) → `/zones/1` (id=`glabella`, name_ko=`미간`, name_en=`Glabella`).

## 원문 값 (문서 순서 · 전부)

| # | JSON Pointer | 원본 컬럼명 | 배열 순번 | 자료형 | 원문 값 |
|---|---|---|---|---|---|
| 72 | `/zones/1` | `(zones 원소)` | 1 | object{12} | (컨테이너 · 키: `id`, `name_ko`, `name_en`, `danger_level`, `danger_color`, `vessels`, `nerves`, `safe_injection_depth`, `tissue_data`, `clinical_pearls`, `botox_specific`, `filler_specific`) |
| 73 | `/zones/1/id` | `id` |  | string | glabella |
| 74 | `/zones/1/name_ko` | `name_ko` |  | string | 미간 |
| 75 | `/zones/1/name_en` | `name_en` |  | string | Glabella |
| 76 | `/zones/1/danger_level` | `danger_level` |  | integer | `5` |
| 77 | `/zones/1/danger_color` | `danger_color` |  | string | red |
| 78 | `/zones/1/vessels` | `vessels` |  | array[2] | (배열 · 2개) |
| 79 | `/zones/1/vessels/0` | `(vessels 원소)` | 0 | object{6} | (컨테이너 · 키: `name`, `depth_mm`, `diameter_mm`, `course`, `danger`, `depth_range_mm`) |
| 80 | `/zones/1/vessels/0/name` | `name` |  | string | 활차상동맥 (Supratrochlear artery) |
| 81 | `/zones/1/vessels/0/depth_mm` | `depth_mm` |  | number | `1.8` |
| 82 | `/zones/1/vessels/0/diameter_mm` | `diameter_mm` |  | number | `0.7` |
| 83 | `/zones/1/vessels/0/course` | `course` |  | string | 미간 정중앙에서 상방 주행, 양측 교차 문합 |
| 84 | `/zones/1/vessels/0/danger` | `danger` |  | string | 0.0397mL로 안동맥 폐색 가능 — 미간은 주요 실명 고위험 부위(2019 업데이트 27.1%) |
| 85 | `/zones/1/vessels/0/depth_range_mm` | `depth_range_mm` |  | array[2] | (배열 · 2개) |
| 86 | `/zones/1/vessels/0/depth_range_mm/0` | `(depth_range_mm 원소)` | 0 | number | `0.5` |
| 87 | `/zones/1/vessels/0/depth_range_mm/1` | `(depth_range_mm 원소)` | 1 | number | `2.2` |
| 88 | `/zones/1/vessels/1` | `(vessels 원소)` | 1 | object{5} | (컨테이너 · 키: `name`, `depth_mm`, `diameter_mm`, `course`, `danger`) |
| 89 | `/zones/1/vessels/1/name` | `name` |  | string | 배비동맥 (Dorsal nasal artery) |
| 90 | `/zones/1/vessels/1/depth_mm` | `depth_mm` |  | number | `2.0` |
| 91 | `/zones/1/vessels/1/diameter_mm` | `diameter_mm` |  | number | `0.6` |
| 92 | `/zones/1/vessels/1/course` | `course` |  | string | 내안각에서 코등으로 하행, 미간과 코 경계부 |
| 93 | `/zones/1/vessels/1/danger` | `danger` |  | string | 안동맥 직접 분지 — 역행성 색전 고위험 |
| 94 | `/zones/1/nerves` | `nerves` |  | array[1] | (배열 · 1개) |
| 95 | `/zones/1/nerves/0` | `(nerves 원소)` | 0 | object{3} | (컨테이너 · 키: `name`, `type`, `significance`) |
| 96 | `/zones/1/nerves/0/name` | `name` |  | string | 활차상신경 (Supratrochlear nerve) |
| 97 | `/zones/1/nerves/0/type` | `type` |  | string | sensory |
| 98 | `/zones/1/nerves/0/significance` | `significance` |  | string | 미간 및 이마 내측 감각 |
| 99 | `/zones/1/safe_injection_depth` | `safe_injection_depth` |  | string | 골막상층 (supraperiosteal) — 절대 피하층 주사 금지 |
| 100 | `/zones/1/tissue_data` | `tissue_data` |  | object{3} | (컨테이너 · 키: `csm_mean_thickness_mm`, `csm_thickness_variation_mm`, `notes`) |
| 101 | `/zones/1/tissue_data/csm_mean_thickness_mm` | `csm_mean_thickness_mm` |  | number | `1.62` |
| 102 | `/zones/1/tissue_data/csm_thickness_variation_mm` | `csm_thickness_variation_mm` |  | number | `0.4` |
| 103 | `/zones/1/tissue_data/notes` | `notes` |  | string | 추미근(CSM, corrugator supercilii muscle) 평균 두께 약 1.62±0.4mm. 기존 15mm/21mm 값은 근육 두께로 해부학적으로 성립하지 않아 삭제했으며, 특정 인종 간 두께 차이로 혈관 표재성을 단정할 근거는 불충분 |
| 104 | `/zones/1/clinical_pearls` | `clinical_pearls` |  | array[6] | (배열 · 6개) |
| 105 | `/zones/1/clinical_pearls/0` | `(clinical_pearls 원소)` | 0 | string | 주요 실명 고위험 부위 — 2015 초기 리뷰 38.8%, Beleznay 2019 업데이트 27.1%(코 56.3% 다음) |
| 106 | `/zones/1/clinical_pearls/1` | `(clinical_pearls 원소)` | 1 | string | 0.0397mL(0.04mL 미만)로 안동맥 폐색 → 실명 |
| 107 | `/zones/1/clinical_pearls/2` | `(clinical_pearls 원소)` | 2 | string | 추미근 평균 두께는 약 1.62±0.4mm이며 개인별 해부 변이가 커 고정 깊이 수치만으로 안전을 판단할 수 없음 |
| 108 | `/zones/1/clinical_pearls/3` | `(clinical_pearls 원소)` | 3 | string | 양측 활차상동맥이 정중선에서 교차 문합 |
| 109 | `/zones/1/clinical_pearls/4` | `(clinical_pearls 원소)` | 4 | string | 흡인 검사는 보조 수단이며 음성 결과가 혈관 내 주입 안전을 보장하지 않음 — 저압·저속·소량 주입과 캐뉼러 사용을 병행 |
| 110 | `/zones/1/clinical_pearls/5` | `(clinical_pearls 원소)` | 5 | string | 캐뉼러 사용 강력 권장, 니들 사용 시 최소량 |
| 111 | `/zones/1/botox_specific` | `botox_specific` |  | object{5} | (컨테이너 · 키: `target_muscle`, `risk`, `safe_zone`, `key_warning`, `dose_range`) |
| 112 | `/zones/1/botox_specific/target_muscle` | `target_muscle` |  | string | 추미근 (Corrugator supercilii), 비근근 (Procerus) |
| 113 | `/zones/1/botox_specific/risk` | `risk` |  | string | 눈썹 처짐 (과다 주사 시), 이마 보상적 주름 증가 |
| 114 | `/zones/1/botox_specific/safe_zone` | `safe_zone` |  | string | 추미근 body 내 주사, 안와상연 상방 1cm 이상 |
| 115 | `/zones/1/botox_specific/key_warning` | `key_warning` |  | string | 추미근 외측 과다 주사 → 눈썹 처짐(Mephisto sign) |
| 116 | `/zones/1/botox_specific/dose_range` | `dose_range` |  | string | 추미근 10-25U, 비근근 5-10U |
| 117 | `/zones/1/filler_specific` | `filler_specific` |  | object{6} | (컨테이너 · 키: `risk_level`, `primary_risk`, `safe_technique`, `max_per_point_ml`, `preferred_product`, `emergency_protocol`) |
| 118 | `/zones/1/filler_specific/risk_level` | `risk_level` |  | integer | `5` |
| 119 | `/zones/1/filler_specific/primary_risk` | `primary_risk` |  | string | 역행성 색전 → 실명 (최고 위험) |
| 120 | `/zones/1/filler_specific/safe_technique` | `safe_technique` |  | string | 골막상 캐뉼러, 0.05mL 이하/점, 흡인은 보조 수단으로만 사용, 저압·저속 주입 |
| 121 | `/zones/1/filler_specific/max_per_point_ml` | `max_per_point_ml` |  | number | `0.05` |
| 122 | `/zones/1/filler_specific/preferred_product` | `preferred_product` |  | string | 저점도 HA (hyaluronidase로 용해 가능한 제품만) |
| 123 | `/zones/1/filler_specific/emergency_protocol` | `emergency_protocol` |  | string | 시력저하·안통 발생 시 즉시 주입 중단/응급콜 및 망막안과·응급실 이송(지체 없이 즉각 대응); HA 필러는 주입부·허혈부 및 미간-상활차/상안와/비배부 혈관경로에 hyaluronidase ≥1,500U(IU) 광범위 다점 침윤 후 필요 시 반복(총량 상한 없음), 안구마사지·안압강하제는 보조, retrobulbar/peribulbar 1,500–3,000U는 안과/숙련자만 시행하고 이송 지연 금지. |

## 잠정 관찰 (원문 칸과 분리)

| # | 상태 | 근거 Pointer | 관찰 | issues.md |
|---|---|---|---|---|
| OBS-S02-01 | P | `/zones/1/vessels/0/depth_range_mm`, `/zones/1/vessels/1` | vessels[0] 에는 depth_range_mm 이 있고 vessels[1] 에는 없다(선택적 필드). | ADZ-P16 |
| OBS-S02-02 | P | `/zones/1/tissue_data/csm_mean_thickness_mm`, `/zones/1/tissue_data/csm_thickness_variation_mm`, `/zones/1/tissue_data/notes` | 숫자 1.62 와 0.4 가 notes 의 '1.62±0.4mm' 에 대응해 보이나 variation 의 통계적 의미(SD 등)는 원문에 없다. | ADZ-B17 |
| OBS-S02-03 | P | `/zones/1/tissue_data/notes` | '기존 15mm/21mm 값은 ... 삭제했으며' 처럼 편집 이력이 데이터 값 안에 있다. | ADZ-P19 |
| OBS-S02-04 | I | `/zones/1/filler_specific/primary_risk`, `/critical_safety_facts/blindness_highest_risk_zones`, `/zones/4/clinical_pearls/0` | 미간 filler primary_risk 에 '(최고 위험)' 이 있으나 critical_safety_facts 는 '코가 현재 최고위험부위', 코 pearls 는 '실명 원인 부위 1위' 라고 한다. | ADZ-I01 |
| OBS-S02-05 | I | `/zones/1/botox_specific/target_muscle`, `/zones/4/botox_specific/target_muscle` | '비근근' 이 미간에서는 'Procerus', 코에서는 'Nasalis' 와 병기된다. | ADZ-I02 |
| OBS-S02-06 | F | `/zones/1/filler_specific/emergency_protocol` | '미간-상활차/상안와/비배부 혈관경로' 의 '비배부' 는 vessels 의 '배비동맥 (Dorsal nasal artery)' 과 표기가 다르다. 대응 여부는 후속. | ADZ-F13 |
| OBS-S02-07 | P | `/zones/1/filler_specific/emergency_protocol` | 한 값에 조건·시간(즉시·지체 없이)·하한(≥1,500U)·반복 조건·상한 부정(총량 상한 없음)·시행자 한정·금지가 연쇄된다. 범위 구분자는 en dash '–'(1,500–3,000U) 다. | ADZ-P11 |

## 수동 복합 표현 (직접 읽기)

탐색 관점은 수집용 꼬리표이며 확정 분류가 아니다. 구간은 값 문자열 기준 코드 포인트 `[start,end)`.

| ID | Pointer | 원문 구간 | 구간 | 탐색 관점 | 메모 |
|---|---|---|---|---|---|
| MX-S02-001 | `/zones/1/vessels/0/course` | 미간 정중앙에서 상방 주행, 양측 교차 문합 | [0, 24] | 위치·방향 |  |
| MX-S02-002 | `/zones/1/vessels/0/danger` | 0.0397mL로 안동맥 폐색 가능 | [0, 19] | 수량·단위, 가능성 |  |
| MX-S02-003 | `/zones/1/vessels/0/danger` | 미간은 주요 실명 고위험 부위(2019 업데이트 27.1%) | [22, 55] | 시간(2019 업데이트), 비율 |  |
| MX-S02-004 | `/zones/1/vessels/1/course` | 내안각에서 코등으로 하행, 미간과 코 경계부 | [0, 24] | 위치·방향, 타 부위 언급(코) |  |
| MX-S02-005 | `/zones/1/vessels/1/danger` | 안동맥 직접 분지 — 역행성 색전 고위험 | [0, 22] | 위험 |  |
| MX-S02-006 | `/zones/1/safe_injection_depth` | 절대 피하층 주사 금지 | [25, 37] | 강조(절대), 금지 |  |
| MX-S02-007 | `/zones/1/tissue_data/notes` | 추미근(CSM, corrugator supercilii muscle) 평균 두께 약 1.62±0.4mm | [0, 57] | 평균, 근사(약), ± |  |
| MX-S02-008 | `/zones/1/tissue_data/notes` | 기존 15mm/21mm 값은 근육 두께로 해부학적으로 성립하지 않아 삭제했으며 | [59, 102] | 편집 이력, 부정(않아) |  |
| MX-S02-009 | `/zones/1/tissue_data/notes` | 특정 인종 간 두께 차이로 혈관 표재성을 단정할 근거는 불충분 | [104, 138] | 불확실성, 근거 부족 |  |
| MX-S02-010 | `/zones/1/clinical_pearls/0` | 2015 초기 리뷰 38.8% | [15, 31] | 시간, 비율 |  |
| MX-S02-011 | `/zones/1/clinical_pearls/0` | Beleznay 2019 업데이트 27.1% | [33, 57] | 인용(약식), 시간, 비율 |  |
| MX-S02-012 | `/zones/1/clinical_pearls/0` | 코 56.3% 다음 | [58, 68] | 순위, 타 부위 언급(코) |  |
| MX-S02-013 | `/zones/1/clinical_pearls/1` | 0.0397mL(0.04mL 미만)로 안동맥 폐색 → 실명 | [0, 32] | 수량, 상한(미만), 결과(→) |  |
| MX-S02-014 | `/zones/1/clinical_pearls/2` | 추미근 평균 두께는 약 1.62±0.4mm이며 개인별 해부 변이가 커 고정 깊이 수치만으로 안전을 판단할 수 없음 | [0, 63] | 평균, 불가(수 없음), 한정(만으로) |  |
| MX-S02-015 | `/zones/1/clinical_pearls/3` | 양측 활차상동맥이 정중선에서 교차 문합 | [0, 21] | 해부 관계 |  |
| MX-S02-016 | `/zones/1/clinical_pearls/4` | 흡인 검사는 보조 수단이며 음성 결과가 혈관 내 주입 안전을 보장하지 않음 | [0, 41] | 부정(않음) |  |
| MX-S02-017 | `/zones/1/clinical_pearls/4` | 저압·저속·소량 주입과 캐뉼러 사용을 병행 | [44, 67] | 나열, 병행 |  |
| MX-S02-018 | `/zones/1/clinical_pearls/5` | 캐뉼러 사용 강력 권장 | [0, 12] | 권고, 강도(강력) |  |
| MX-S02-019 | `/zones/1/clinical_pearls/5` | 니들 사용 시 최소량 | [14, 25] | 조건(시), 수량 수식 |  |
| MX-S02-020 | `/zones/1/botox_specific/target_muscle` | 추미근 (Corrugator supercilii), 비근근 (Procerus) | [0, 43] | 근육명, 영문 병기 |  |
| MX-S02-021 | `/zones/1/botox_specific/risk` | 눈썹 처짐 (과다 주사 시) | [0, 15] | 조건(시) |  |
| MX-S02-022 | `/zones/1/botox_specific/risk` | 이마 보상적 주름 증가 | [17, 29] | 부작용, 타 부위 언급(이마) |  |
| MX-S02-023 | `/zones/1/botox_specific/safe_zone` | 추미근 body 내 주사, 안와상연 상방 1cm 이상 | [0, 29] | 위치, 거리 하한(이상) |  |
| MX-S02-024 | `/zones/1/botox_specific/key_warning` | 추미근 외측 과다 주사 → 눈썹 처짐(Mephisto sign) | [0, 35] | 결과(→), 영문 병기 |  |
| MX-S02-025 | `/zones/1/botox_specific/dose_range` | 추미근 10-25U | [0, 10] | 근육+범위 |  |
| MX-S02-026 | `/zones/1/botox_specific/dose_range` | 비근근 5-10U | [12, 21] | 근육+범위 |  |
| MX-S02-027 | `/zones/1/filler_specific/primary_risk` | 역행성 색전 → 실명 (최고 위험) | [0, 19] | 결과(→), 최상급 |  |
| MX-S02-028 | `/zones/1/filler_specific/safe_technique` | 0.05mL 이하/점 | [9, 20] | 상한(이하), 단위당 |  |
| MX-S02-029 | `/zones/1/filler_specific/safe_technique` | 흡인은 보조 수단으로만 사용 | [22, 37] | 한정(만) |  |
| MX-S02-030 | `/zones/1/filler_specific/preferred_product` | 저점도 HA (hyaluronidase로 용해 가능한 제품만) | [0, 34] | 한정(만), 조건 |  |
| MX-S02-031 | `/zones/1/filler_specific/emergency_protocol` | 시력저하·안통 발생 시 즉시 주입 중단/응급콜 및 망막안과·응급실 이송(지체 없이 즉각 대응) | [0, 52] | 조건(시), 시간(즉시), 기호(/) |  |
| MX-S02-032 | `/zones/1/filler_specific/emergency_protocol` | HA 필러는 주입부·허혈부 및 미간-상활차/상안와/비배부 혈관경로에 hyaluronidase ≥1,500U(IU) 광범위 다점 침윤 후 필요 시 반복(총량 상한 없음) | [54, 147] | 적용 대상(HA 필러는), 하한(≥), 순서(후), 조건(필요 시), 부정(없음) |  |
| MX-S02-033 | `/zones/1/filler_specific/emergency_protocol` | ≥1,500U(IU) | [106, 117] | 하한, 단위 병기 |  |
| MX-S02-034 | `/zones/1/filler_specific/emergency_protocol` | 총량 상한 없음 | [138, 146] | 부정(없음), 한계 |  |
| MX-S02-035 | `/zones/1/filler_specific/emergency_protocol` | 안구마사지·안압강하제는 보조 | [149, 164] | 보조 지위 |  |
| MX-S02-036 | `/zones/1/filler_specific/emergency_protocol` | retrobulbar/peribulbar 1,500–3,000U는 안과/숙련자만 시행하고 이송 지연 금지 | [166, 224] | 범위(–), 시행자 한정(만), 금지 |  |
| MX-S02-037 | `/zones/1/nerves/0/significance` | 미간 및 이마 내측 감각 | [0, 13] | 부위 나열(및) |  |

## 정규식 보조 후보 (기계 · 요약)

| 패턴 | 출현 |
|---|---|
| number_unit | 17 |
| possibility_frequency | 2 |
| em_dash | 5 |
| negation_prohibition | 8 |
| degree_emphasis | 6 |
| comparator | 6 |
| slash | 7 |
| time_order | 5 |
| citation | 1 |
| arrow | 3 |
| middle_dot | 7 |
| condition | 4 |
| range | 3 |

전체 출현·구간은 `expressions.json` → `regex_candidates` (section=S02).

## 전문어 분절 관찰 (Kiwi 원시 · K)

| Pointer | 낱말 | 구간 | Kiwi 토큰 | 상태 |
|---|---|---|---|---|
| `/zones/1/vessels/1/danger` | 역행성 | [12, 15] | 역행/NNG + 성/XSN | K: 여러 형태소로 분절(원시 결과 보존) |
| `/zones/1/safe_injection_depth` | 골막상 | [0, 3] | 골막상층/NNP | 관찰 대상 아님: 더 긴 낱말(토큰)의 부분 문자열 |
| `/zones/1/tissue_data/notes` | 표재성 | [122, 125] | 표재/NNG + 성/XSN | K: 여러 형태소로 분절(원시 결과 보존) |
| `/zones/1/clinical_pearls/2` | 추미근 | [0, 3] | 추/NNP + 미/NNG + 근/NNG | K: 여러 형태소로 분절(원시 결과 보존) |
| `/zones/1/botox_specific/target_muscle` | 추미근 | [0, 3] | 추/NNP + 미/NNG + 근/NNG | K: 여러 형태소로 분절(원시 결과 보존) |
| `/zones/1/botox_specific/safe_zone` | 추미근 | [0, 3] | 추/NNP + 미/NNG + 근/NNG | K: 여러 형태소로 분절(원시 결과 보존) |
| `/zones/1/botox_specific/key_warning` | 추미근 | [0, 3] | 추/NNP + 미/NNG + 근/NNG | K: 여러 형태소로 분절(원시 결과 보존) |
| `/zones/1/botox_specific/dose_range` | 추미근 | [0, 3] | 추/NNP + 미/NNG + 근/NNG | K: 여러 형태소로 분절(원시 결과 보존) |
| `/zones/1/botox_specific/dose_range` | 비근근 | [12, 15] | 비/XPN + 근/NNG + 근/NNG | K: 여러 형태소로 분절(원시 결과 보존) |
| `/zones/1/filler_specific/preferred_product` | 저점도 | [0, 3] | 저/MM + 점/NNG + 도/JX | K: 여러 형태소로 분절(원시 결과 보존) |

단일 형태소로 나온 출현은 표에서 생략했다(`morphology.json` → `segmentation_review` 에 전부 있음).

