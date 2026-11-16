# S01 — zones[0] forehead (이마 / Forehead)

[← review.md](review.md) · 범위 `/zones/0/**` · 소유 노드 62 · 말단 48 · 직접 읽기 done

상위 문맥: 루트 객체 → `zones` 배열(S00 소유) → `/zones/0` (id=`forehead`, name_ko=`이마`, name_en=`Forehead`).

## 원문 값 (문서 순서 · 전부)

| # | JSON Pointer | 원본 컬럼명 | 배열 순번 | 자료형 | 원문 값 |
|---|---|---|---|---|---|
| 10 | `/zones/0` | `(zones 원소)` | 0 | object{12} | (컨테이너 · 키: `id`, `name_ko`, `name_en`, `danger_level`, `danger_color`, `vessels`, `nerves`, `safe_injection_depth`, `tissue_data`, `clinical_pearls`, `botox_specific`, `filler_specific`) |
| 11 | `/zones/0/id` | `id` |  | string | forehead |
| 12 | `/zones/0/name_ko` | `name_ko` |  | string | 이마 |
| 13 | `/zones/0/name_en` | `name_en` |  | string | Forehead |
| 14 | `/zones/0/danger_level` | `danger_level` |  | integer | `4` |
| 15 | `/zones/0/danger_color` | `danger_color` |  | string | orange |
| 16 | `/zones/0/vessels` | `vessels` |  | array[2] | (배열 · 2개) |
| 17 | `/zones/0/vessels/0` | `(vessels 원소)` | 0 | object{7} | (컨테이너 · 키: `name`, `depth_mm`, `diameter_mm`, `course`, `danger`, `note`, `depth_range_mm`) |
| 18 | `/zones/0/vessels/0/name` | `name` |  | string | 활차상동맥 (Supratrochlear artery) |
| 19 | `/zones/0/vessels/0/depth_mm` | `depth_mm` |  | number | `1.8` |
| 20 | `/zones/0/vessels/0/diameter_mm` | `diameter_mm` |  | number | `0.7` |
| 21 | `/zones/0/vessels/0/course` | `course` |  | string | 안와상연에서 상방으로 주행, 이마 중앙선 근처 |
| 22 | `/zones/0/vessels/0/danger` | `danger` |  | string | 안동맥과 직접 연결 — 역행성 색전 시 실명 위험 |
| 23 | `/zones/0/vessels/0/note` | `note` |  | string | 평균 1.8mm이나 아시아인 피부는 더 얇고 개인 변이가 커 0.5mm 수준까지 표재성일 수 있음(Anat Rec 2024 cadaver) |
| 24 | `/zones/0/vessels/0/depth_range_mm` | `depth_range_mm` |  | array[2] | (배열 · 2개) |
| 25 | `/zones/0/vessels/0/depth_range_mm/0` | `(depth_range_mm 원소)` | 0 | number | `0.5` |
| 26 | `/zones/0/vessels/0/depth_range_mm/1` | `(depth_range_mm 원소)` | 1 | number | `2.2` |
| 27 | `/zones/0/vessels/1` | `(vessels 원소)` | 1 | object{7} | (컨테이너 · 키: `name`, `depth_mm`, `diameter_mm`, `course`, `danger`, `note`, `depth_range_mm`) |
| 28 | `/zones/0/vessels/1/name` | `name` |  | string | 안와상동맥 (Supraorbital artery) |
| 29 | `/zones/0/vessels/1/depth_mm` | `depth_mm` |  | number | `1.7` |
| 30 | `/zones/0/vessels/1/diameter_mm` | `diameter_mm` |  | number | `0.8` |
| 31 | `/zones/0/vessels/1/course` | `course` |  | string | 안와상절흔에서 상방으로 주행 |
| 32 | `/zones/0/vessels/1/danger` | `danger` |  | string | 안동맥 분지 — 역행성 색전 위험 |
| 33 | `/zones/0/vessels/1/note` | `note` |  | string | 평균값이며 개인 변이 큼 — 고정 깊이 신뢰 금지 |
| 34 | `/zones/0/vessels/1/depth_range_mm` | `depth_range_mm` |  | array[2] | (배열 · 2개) |
| 35 | `/zones/0/vessels/1/depth_range_mm/0` | `(depth_range_mm 원소)` | 0 | number | `0.5` |
| 36 | `/zones/0/vessels/1/depth_range_mm/1` | `(depth_range_mm 원소)` | 1 | number | `2.2` |
| 37 | `/zones/0/nerves` | `nerves` |  | array[2] | (배열 · 2개) |
| 38 | `/zones/0/nerves/0` | `(nerves 원소)` | 0 | object{3} | (컨테이너 · 키: `name`, `type`, `significance`) |
| 39 | `/zones/0/nerves/0/name` | `name` |  | string | 활차상신경 (Supratrochlear nerve) |
| 40 | `/zones/0/nerves/0/type` | `type` |  | string | sensory |
| 41 | `/zones/0/nerves/0/significance` | `significance` |  | string | 이마 내측 감각 |
| 42 | `/zones/0/nerves/1` | `(nerves 원소)` | 1 | object{3} | (컨테이너 · 키: `name`, `type`, `significance`) |
| 43 | `/zones/0/nerves/1/name` | `name` |  | string | 안와상신경 (Supraorbital nerve) |
| 44 | `/zones/0/nerves/1/type` | `type` |  | string | sensory |
| 45 | `/zones/0/nerves/1/significance` | `significance` |  | string | 이마 외측 감각 |
| 46 | `/zones/0/safe_injection_depth` | `safe_injection_depth` |  | string | 골막상층 (supraperiosteal) — 혈관은 표재성이므로 깊은 층이 안전 |
| 47 | `/zones/0/tissue_data` | `tissue_data` |  | object{3} | (컨테이너 · 키: `frontalis_thickness`, `skin_to_periosteum_mm`, `notes`) |
| 48 | `/zones/0/tissue_data/frontalis_thickness` | `frontalis_thickness` |  | object{3} | (컨테이너 · 키: `midpupil_mm`, `lateral_canthus_mm`, `lateral_orbital_rim_mm`) |
| 49 | `/zones/0/tissue_data/frontalis_thickness/midpupil_mm` | `midpupil_mm` |  | number | `1.8` |
| 50 | `/zones/0/tissue_data/frontalis_thickness/lateral_canthus_mm` | `lateral_canthus_mm` |  | number | `1.61` |
| 51 | `/zones/0/tissue_data/frontalis_thickness/lateral_orbital_rim_mm` | `lateral_orbital_rim_mm` |  | number | `0.11` |
| 52 | `/zones/0/tissue_data/skin_to_periosteum_mm` | `skin_to_periosteum_mm` |  | number | `5.0` |
| 53 | `/zones/0/tissue_data/notes` | `notes` |  | string | 이마 피부-골막 거리 평균 0.5cm — 매우 얇음 |
| 54 | `/zones/0/clinical_pearls` | `clinical_pearls` |  | array[4] | (배열 · 4개) |
| 55 | `/zones/0/clinical_pearls/0` | `(clinical_pearls 원소)` | 0 | string | 이마 피부-골막 거리 평균 0.5cm — 매우 얇음 |
| 56 | `/zones/0/clinical_pearls/1` | `(clinical_pearls 원소)` | 1 | string | 활차상동맥은 중앙선 근처에서 표재성 → 정중선 주사 주의 |
| 57 | `/zones/0/clinical_pearls/2` | `(clinical_pearls 원소)` | 2 | string | 캐뉼러 사용 권장 (니들 대비 혈관 천자 위험 감소) |
| 58 | `/zones/0/clinical_pearls/3` | `(clinical_pearls 원소)` | 3 | string | 소량 다점 주사 (0.1mL 이하/점) |
| 59 | `/zones/0/botox_specific` | `botox_specific` |  | object{6} | (컨테이너 · 키: `target_muscle`, `risk`, `safe_zone`, `diffusion_range_cm`, `key_warning`, `dose_range`) |
| 60 | `/zones/0/botox_specific/target_muscle` | `target_muscle` |  | string | 전두근 (Frontalis) |
| 61 | `/zones/0/botox_specific/risk` | `risk` |  | string | 눈꺼풀 처짐 (보톡스 확산 시 상안검거근 영향) |
| 62 | `/zones/0/botox_specific/safe_zone` | `safe_zone` |  | string | 안와상연 상방 2cm 이상, 외측은 측두선 내측 |
| 63 | `/zones/0/botox_specific/diffusion_range_cm` | `diffusion_range_cm` |  | string | 1.5-3.0 |
| 64 | `/zones/0/botox_specific/key_warning` | `key_warning` |  | string | 보톡스 확산 1.5-3cm → 안와상연 너무 가까이 주사 시 안검하수 |
| 65 | `/zones/0/botox_specific/dose_range` | `dose_range` |  | string | 10-30 units (2-5 포인트/측, 2-5U/포인트) |
| 66 | `/zones/0/filler_specific` | `filler_specific` |  | object{5} | (컨테이너 · 키: `risk_level`, `primary_risk`, `safe_technique`, `max_per_point_ml`, `preferred_product`) |
| 67 | `/zones/0/filler_specific/risk_level` | `risk_level` |  | integer | `4` |
| 68 | `/zones/0/filler_specific/primary_risk` | `primary_risk` |  | string | 역행성 색전 → 실명 |
| 69 | `/zones/0/filler_specific/safe_technique` | `safe_technique` |  | string | 골막상 캐뉼러, 소량 다점, 저압 주입 |
| 70 | `/zones/0/filler_specific/max_per_point_ml` | `max_per_point_ml` |  | number | `0.1` |
| 71 | `/zones/0/filler_specific/preferred_product` | `preferred_product` |  | string | 용해 가능한 저점도 HA (CaHA는 hyaluronidase로 용해 불가하여 실명 위험 부위에서는 권장하지 않음) |

## 잠정 관찰 (원문 칸과 분리)

| # | 상태 | 근거 Pointer | 관찰 | issues.md |
|---|---|---|---|---|
| OBS-S01-01 | P | `/zones/0/vessels/0/depth_mm`, `/zones/0/vessels/0/note`, `/zones/0/vessels/0/depth_range_mm` | depth_mm 1.8 은 note 에서 '평균' 으로 한정되고 depth_range_mm [0.5,2.2] 가 따로 있다. 숫자 칸만 읽으면 '평균'·'개인 변이'·'아시아인' 한정이 사라진다. |  |
| OBS-S01-02 | P | `/zones/0/tissue_data/notes`, `/zones/0/clinical_pearls/0` | tissue_data.notes 와 clinical_pearls[0] 이 문자열 완전 일치다(중복 출현, 각자 위치 유지). | ADZ-P15 |
| OBS-S01-03 | P | `/zones/0/tissue_data/skin_to_periosteum_mm`, `/zones/0/tissue_data/notes` | 숫자 5.0(_mm) 과 문장 '평균 0.5cm' 은 단위가 다르게 적혀 있다. 환산 일치 여부는 판단하지 않고 기록만 한다. '피부-골막' 의 '-' 는 범위가 아니라 두 구조를 잇는 표기다. | ADZ-P11 |
| OBS-S01-04 | P | `/zones/0/botox_specific/diffusion_range_cm`, `/zones/0/botox_specific/key_warning` | diffusion_range_cm 은 숫자형이 아닌 문자열 '1.5-3.0' 이며 이 필드는 forehead 에만 있다. key_warning 에는 '1.5-3cm' 로 다시 나온다. | ADZ-P12 |
| OBS-S01-05 | P | `/zones/0/botox_specific/dose_range` | 단위가 'units' 와 'U' 두 표기로 한 값에 공존한다. | ADZ-P12 |
| OBS-S01-06 | P | `/zones/0/filler_specific/preferred_product` | 괄호 안에 제외 이유(CaHA 용해 불가)와 적용 범위('실명 위험 부위에서는')가 붙어 있다. 괄호를 떼면 조건이 사라진다. |  |

## 수동 복합 표현 (직접 읽기)

탐색 관점은 수집용 꼬리표이며 확정 분류가 아니다. 구간은 값 문자열 기준 코드 포인트 `[start,end)`.

| ID | Pointer | 원문 구간 | 구간 | 탐색 관점 | 메모 |
|---|---|---|---|---|---|
| MX-S01-001 | `/zones/0/vessels/0/name` | 활차상동맥 (Supratrochlear artery) | [0, 29] | 혈관명, 영문 병기 |  |
| MX-S01-002 | `/zones/0/vessels/0/course` | 안와상연에서 상방으로 주행, 이마 중앙선 근처 | [0, 25] | 위치·방향 |  |
| MX-S01-003 | `/zones/0/vessels/0/danger` | 역행성 색전 시 실명 위험 | [13, 27] | 조건(시), 위험 |  |
| MX-S01-004 | `/zones/0/vessels/0/note` | 평균 1.8mm이나 아시아인 피부는 더 얇고 개인 변이가 커 0.5mm 수준까지 표재성일 수 있음 | [0, 54] | 평균, 대조(이나), 집단 한정, 가능성(수 있음) |  |
| MX-S01-005 | `/zones/0/vessels/0/note` | Anat Rec 2024 cadaver | [55, 76] | 인용(약식) |  |
| MX-S01-006 | `/zones/0/vessels/1/danger` | 안동맥 분지 — 역행성 색전 위험 | [0, 18] | 위험 |  |
| MX-S01-007 | `/zones/0/vessels/1/note` | 평균값이며 개인 변이 큼 — 고정 깊이 신뢰 금지 | [0, 27] | 평균, 금지 |  |
| MX-S01-008 | `/zones/0/nerves/0/significance` | 이마 내측 감각 | [0, 8] | 부위+기능 |  |
| MX-S01-009 | `/zones/0/safe_injection_depth` | 골막상층 (supraperiosteal) — 혈관은 표재성이므로 깊은 층이 안전 | [0, 44] | 층, 이유(이므로), 비교 |  |
| MX-S01-010 | `/zones/0/tissue_data/notes` | 이마 피부-골막 거리 평균 0.5cm — 매우 얇음 | [0, 28] | 평균, 수량·단위, 정도(매우), 연결 하이픈 |  |
| MX-S01-011 | `/zones/0/clinical_pearls/1` | 활차상동맥은 중앙선 근처에서 표재성 → 정중선 주사 주의 | [0, 31] | 결과(→), 주의 |  |
| MX-S01-012 | `/zones/0/clinical_pearls/2` | 캐뉼러 사용 권장 (니들 대비 혈관 천자 위험 감소) | [0, 29] | 권고, 비교(대비) |  |
| MX-S01-013 | `/zones/0/clinical_pearls/3` | 소량 다점 주사 (0.1mL 이하/점) | [0, 21] | 상한(이하), 단위당(/점) |  |
| MX-S01-014 | `/zones/0/botox_specific/risk` | 눈꺼풀 처짐 (보톡스 확산 시 상안검거근 영향) | [0, 26] | 조건(시), 부작용 |  |
| MX-S01-015 | `/zones/0/botox_specific/safe_zone` | 안와상연 상방 2cm 이상 | [0, 14] | 거리 하한(이상) |  |
| MX-S01-016 | `/zones/0/botox_specific/safe_zone` | 외측은 측두선 내측 | [16, 26] | 경계 |  |
| MX-S01-017 | `/zones/0/botox_specific/key_warning` | 보톡스 확산 1.5-3cm → 안와상연 너무 가까이 주사 시 안검하수 | [0, 38] | 범위, 조건(시), 정도(너무) |  |
| MX-S01-018 | `/zones/0/botox_specific/dose_range` | 10-30 units | [0, 11] | 범위, 단위(units) |  |
| MX-S01-019 | `/zones/0/botox_specific/dose_range` | 2-5 포인트/측 | [13, 22] | 범위, 단위당(/측) |  |
| MX-S01-020 | `/zones/0/botox_specific/dose_range` | 2-5U/포인트 | [24, 32] | 범위, 단위당(/포인트) |  |
| MX-S01-021 | `/zones/0/filler_specific/primary_risk` | 역행성 색전 → 실명 | [0, 11] | 경로·결과(→) |  |
| MX-S01-022 | `/zones/0/filler_specific/safe_technique` | 골막상 캐뉼러, 소량 다점, 저압 주입 | [0, 21] | 기법 나열 |  |
| MX-S01-023 | `/zones/0/filler_specific/preferred_product` | 용해 가능한 저점도 HA | [0, 13] | 수식(용해 가능한·저점도) |  |
| MX-S01-024 | `/zones/0/filler_specific/preferred_product` | CaHA는 hyaluronidase로 용해 불가하여 실명 위험 부위에서는 권장하지 않음 | [15, 63] | 불가, 이유(하여), 적용 범위, 부정(않음) |  |
| MX-S01-025 | `/zones/0/clinical_pearls/0` | 이마 피부-골막 거리 평균 0.5cm — 매우 얇음 | [0, 28] | 평균, 수량·단위, 정도(매우), 연결 하이픈 | tissue_data/notes 와 동일 문자열 |
| MX-S01-026 | `/zones/0/botox_specific/diffusion_range_cm` | 1.5-3.0 | [0, 7] | 범위(문자열형), 단위는 필드명(_cm)에만 |  |

## 정규식 보조 후보 (기계 · 요약)

| 패턴 | 출현 |
|---|---|
| condition | 3 |
| em_dash | 6 |
| number_unit | 11 |
| comparator | 3 |
| possibility_frequency | 2 |
| citation | 1 |
| negation_prohibition | 3 |
| degree_emphasis | 3 |
| arrow | 3 |
| slash | 3 |
| range | 5 |

전체 출현·구간은 `expressions.json` → `regex_candidates` (section=S01).

## 전문어 분절 관찰 (Kiwi 원시 · K)

| Pointer | 낱말 | 구간 | Kiwi 토큰 | 상태 |
|---|---|---|---|---|
| `/zones/0/vessels/0/danger` | 역행성 | [13, 16] | 역행/NNG + 성/XSN | K: 여러 형태소로 분절(원시 결과 보존) |
| `/zones/0/vessels/0/note` | 표재성 | [45, 48] | 표/NNG + 재/NNG + 성/XSN | K: 여러 형태소로 분절(원시 결과 보존) |
| `/zones/0/vessels/1/danger` | 역행성 | [9, 12] | 역행/NNG + 성/XSN | K: 여러 형태소로 분절(원시 결과 보존) |
| `/zones/0/safe_injection_depth` | 골막상 | [0, 3] | 골막상층/NNP | 관찰 대상 아님: 더 긴 낱말(토큰)의 부분 문자열 |
| `/zones/0/safe_injection_depth` | 표재성 | [29, 32] | 표재/NNG + 성/XSN | K: 여러 형태소로 분절(원시 결과 보존) |
| `/zones/0/clinical_pearls/1` | 표재성 | [16, 19] | 표/NNG + 재/NNG + 성/XSN | K: 여러 형태소로 분절(원시 결과 보존) |
| `/zones/0/filler_specific/preferred_product` | 저점도 | [7, 10] | 저/MM + 점/NNG + 도/JX | K: 여러 형태소로 분절(원시 결과 보존) |

단일 형태소로 나온 출현은 표에서 생략했다(`morphology.json` → `segmentation_review` 에 전부 있음).

