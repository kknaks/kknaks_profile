# S06 — zones[5] nasolabial (팔자주름 / Nasolabial Fold)

[← review.md](review.md) · 범위 `/zones/5/**` · 소유 노드 54 · 말단 43 · 직접 읽기 done

상위 문맥: 루트 객체 → `zones` 배열(S00 소유) → `/zones/5` (id=`nasolabial`, name_ko=`팔자주름`, name_en=`Nasolabial Fold`).

## 원문 값 (문서 순서 · 전부)

| # | JSON Pointer | 원본 컬럼명 | 배열 순번 | 자료형 | 원문 값 |
|---|---|---|---|---|---|
| 297 | `/zones/5` | `(zones 원소)` | 5 | object{12} | (컨테이너 · 키: `id`, `name_ko`, `name_en`, `danger_level`, `danger_color`, `vessels`, `nerves`, `safe_injection_depth`, `tissue_data`, `clinical_pearls`, `botox_specific`, `filler_specific`) |
| 298 | `/zones/5/id` | `id` |  | string | nasolabial |
| 299 | `/zones/5/name_ko` | `name_ko` |  | string | 팔자주름 |
| 300 | `/zones/5/name_en` | `name_en` |  | string | Nasolabial Fold |
| 301 | `/zones/5/danger_level` | `danger_level` |  | integer | `4` |
| 302 | `/zones/5/danger_color` | `danger_color` |  | string | orange |
| 303 | `/zones/5/vessels` | `vessels` |  | array[2] | (배열 · 2개) |
| 304 | `/zones/5/vessels/0` | `(vessels 원소)` | 0 | object{5} | (컨테이너 · 키: `name`, `depth_mm`, `diameter_mm`, `course`, `danger`) |
| 305 | `/zones/5/vessels/0/name` | `name` |  | string | 안면동맥 (Facial artery) |
| 306 | `/zones/5/vessels/0/depth_mm` | `depth_mm` |  | number | `5.0` |
| 307 | `/zones/5/vessels/0/diameter_mm` | `diameter_mm` |  | number | `1.2` |
| 308 | `/zones/5/vessels/0/course` | `course` |  | string | 안면동맥 분지가 NLF 인접부에 존재 93.3%; 이 중 NLF 5mm 이내 주행은 약 42.9% |
| 309 | `/zones/5/vessels/0/danger` | `danger` |  | string | NLF 필러 시 안면동맥 천자 → 피부 괴사, 역행성 색전 |
| 310 | `/zones/5/vessels/1` | `(vessels 원소)` | 1 | object{5} | (컨테이너 · 키: `name`, `depth_mm`, `diameter_mm`, `course`, `danger`) |
| 311 | `/zones/5/vessels/1/name` | `name` |  | string | 각동맥 (Angular artery) |
| 312 | `/zones/5/vessels/1/depth_mm` | `depth_mm` |  | number | `3.0` |
| 313 | `/zones/5/vessels/1/diameter_mm` | `diameter_mm` |  | number | `1.0` |
| 314 | `/zones/5/vessels/1/course` | `course` |  | string | NLF 상단부에서 내안각 방향으로 주행, 안면동맥의 말단 |
| 315 | `/zones/5/vessels/1/danger` | `danger` |  | string | 안동맥과 문합 — 역행성 색전 경로 |
| 316 | `/zones/5/nerves` | `nerves` |  | array[2] | (배열 · 2개) |
| 317 | `/zones/5/nerves/0` | `(nerves 원소)` | 0 | object{3} | (컨테이너 · 키: `name`, `type`, `significance`) |
| 318 | `/zones/5/nerves/0/name` | `name` |  | string | 안와하신경 (Infraorbital nerve) |
| 319 | `/zones/5/nerves/0/type` | `type` |  | string | sensory |
| 320 | `/zones/5/nerves/0/significance` | `significance` |  | string | 코 외측, 상구순, 하안검 감각 |
| 321 | `/zones/5/nerves/1` | `(nerves 원소)` | 1 | object{3} | (컨테이너 · 키: `name`, `type`, `significance`) |
| 322 | `/zones/5/nerves/1/name` | `name` |  | string | 협근신경 (Buccal branch of facial nerve) |
| 323 | `/zones/5/nerves/1/type` | `type` |  | string | motor |
| 324 | `/zones/5/nerves/1/significance` | `significance` |  | string | 협근, 구륜근 상부 운동 |
| 325 | `/zones/5/safe_injection_depth` | `safe_injection_depth` |  | string | 피하 또는 피하-근막 경계 (SMAS 상방) |
| 326 | `/zones/5/tissue_data` | `tissue_data` |  | object{6} | (컨테이너 · 키: `facial_artery_distance_to_nlf_mm`, `asian_adjacent_distribution_percent`, `within_5mm_percent`, `facial_artery_diameter_mandible_mm`, `facial_artery_diameter_nasal_mm`, `notes`) |
| 327 | `/zones/5/tissue_data/facial_artery_distance_to_nlf_mm` | `facial_artery_distance_to_nlf_mm` |  | number | `5.0` |
| 328 | `/zones/5/tissue_data/asian_adjacent_distribution_percent` | `asian_adjacent_distribution_percent` |  | number | `93.3` |
| 329 | `/zones/5/tissue_data/within_5mm_percent` | `within_5mm_percent` |  | number | `42.9` |
| 330 | `/zones/5/tissue_data/facial_artery_diameter_mandible_mm` | `facial_artery_diameter_mandible_mm` |  | number | `1.9` |
| 331 | `/zones/5/tissue_data/facial_artery_diameter_nasal_mm` | `facial_artery_diameter_nasal_mm` |  | number | `0.8` |
| 332 | `/zones/5/tissue_data/notes` | `notes` |  | string | 안면동맥 분지가 NLF 인접부에 존재하는 비율은 93.3%이며, 이 중 NLF 5mm 이내 주행은 약 42.9% |
| 333 | `/zones/5/clinical_pearls` | `clinical_pearls` |  | array[5] | (배열 · 5개) |
| 334 | `/zones/5/clinical_pearls/0` | `(clinical_pearls 원소)` | 0 | string | 안면동맥 분지가 NLF 인접부에 존재 93.3%; 이 중 NLF 5mm 이내 주행은 약 42.9% |
| 335 | `/zones/5/clinical_pearls/1` | `(clinical_pearls 원소)` | 1 | string | 안면동맥 직경: 하악 1.9mm → 비측 0.8mm (상방으로 가늘어짐) |
| 336 | `/zones/5/clinical_pearls/2` | `(clinical_pearls 원소)` | 2 | string | NLF 상단부에서 각동맥으로 이행 → 안동맥 문합 → 실명 위험 |
| 337 | `/zones/5/clinical_pearls/3` | `(clinical_pearls 원소)` | 3 | string | 캐뉼러 사용 시 혈관 천자 위험 현저히 감소 |
| 338 | `/zones/5/clinical_pearls/4` | `(clinical_pearls 원소)` | 4 | string | 깊은 층(SMAS 하방) 절대 금지 — 안면동맥은 심부 주행 |
| 339 | `/zones/5/botox_specific` | `botox_specific` |  | object{5} | (컨테이너 · 키: `target_muscle`, `risk`, `safe_zone`, `key_warning`, `dose_range`) |
| 340 | `/zones/5/botox_specific/target_muscle` | `target_muscle` |  | string | 상순거근 (Levator labii superioris) — NLF 보조 치료 |
| 341 | `/zones/5/botox_specific/risk` | `risk` |  | string | 상순 거상 약화 → 미소 비대칭, 음식물 흘림 |
| 342 | `/zones/5/botox_specific/safe_zone` | `safe_zone` |  | string | NLF 필러와 병행, 보톡스 단독은 드묾 |
| 343 | `/zones/5/botox_specific/key_warning` | `key_warning` |  | string | NLF 보톡스는 부작용 위험 대비 효과 제한적 — 필러 우선 |
| 344 | `/zones/5/botox_specific/dose_range` | `dose_range` |  | string | 2-4U/측 (NLF 보조 시) |
| 345 | `/zones/5/filler_specific` | `filler_specific` |  | object{5} | (컨테이너 · 키: `risk_level`, `primary_risk`, `safe_technique`, `max_per_point_ml`, `preferred_product`) |
| 346 | `/zones/5/filler_specific/risk_level` | `risk_level` |  | integer | `4` |
| 347 | `/zones/5/filler_specific/primary_risk` | `primary_risk` |  | string | 안면동맥 천자 → 피부 괴사 + 역행성 색전 |
| 348 | `/zones/5/filler_specific/safe_technique` | `safe_technique` |  | string | 캐뉼러 선형 역행 주입, SMAS 상방, 소량 다점 |
| 349 | `/zones/5/filler_specific/max_per_point_ml` | `max_per_point_ml` |  | number | `0.1` |
| 350 | `/zones/5/filler_specific/preferred_product` | `preferred_product` |  | string | 중점도 HA (NLF 전용) |

## 잠정 관찰 (원문 칸과 분리)

| # | 상태 | 근거 Pointer | 관찰 | issues.md |
|---|---|---|---|---|
| OBS-S06-01 | P | `/zones/5/vessels/0/course`, `/zones/5/tissue_data/notes`, `/zones/5/clinical_pearls/0` | vessels[0].course 에 주행 경로가 아니라 통계(93.3%, 42.9%)가 들어 있고, 같은 문장이 clinical_pearls[0] 과 완전 일치, notes 와는 어미만 다르다. | ADZ-P22 |
| OBS-S06-02 | B | `/zones/5/tissue_data/asian_adjacent_distribution_percent` | 필드명에 'asian' 이 있으나 원문 문장은 대상 집단을 말하지 않는다. 집단 한정의 근거는 필드명뿐이다. | ADZ-B08 |
| OBS-S06-03 | P | `/zones/5/vessels/0/depth_mm`, `/zones/5/tissue_data/facial_artery_distance_to_nlf_mm` | 두 필드가 같은 수 5.0 이나 의미(깊이/NLF 까지 거리)가 다르다. 값 일치만으로 연결하지 않는다. |  |
| OBS-S06-04 | P | `/zones/5/clinical_pearls/1` | '하악 1.9mm → 비측 0.8mm' 의 '→' 는 위치에 따른 변화(점감)다. | ADZ-P09 |
| OBS-S06-05 | F | `/critical_safety_facts/blindness_highest_risk_zones`, `/zones/5/name_ko`, `/zones/5/name_en` | '비순주름'(critical), '팔자주름'(name_ko), 'Nasolabial Fold'/'NLF' 표기가 공존한다. | ADZ-F13 |
| OBS-S06-06 | P | `/zones/5/botox_specific/safe_zone`, `/zones/5/botox_specific/key_warning` | safe_zone 칸에 위치가 아닌 병행·빈도('보톡스 단독은 드묾') 정보가 있다. | ADZ-P22 |

## 수동 복합 표현 (직접 읽기)

탐색 관점은 수집용 꼬리표이며 확정 분류가 아니다. 구간은 값 문자열 기준 코드 포인트 `[start,end)`.

| ID | Pointer | 원문 구간 | 구간 | 탐색 관점 | 메모 |
|---|---|---|---|---|---|
| MX-S06-001 | `/zones/5/vessels/0/course` | 안면동맥 분지가 NLF 인접부에 존재 93.3% | [0, 26] | 비율 |  |
| MX-S06-002 | `/zones/5/vessels/0/course` | 이 중 NLF 5mm 이내 주행은 약 42.9% | [28, 54] | 부분집합(이 중), 거리 상한(이내), 근사(약), 비율 |  |
| MX-S06-003 | `/zones/5/vessels/0/danger` | NLF 필러 시 안면동맥 천자 → 피부 괴사, 역행성 색전 | [0, 32] | 조건(시), 결과(→) |  |
| MX-S06-004 | `/zones/5/vessels/1/course` | NLF 상단부에서 내안각 방향으로 주행, 안면동맥의 말단 | [0, 31] | 위치·방향 |  |
| MX-S06-005 | `/zones/5/vessels/1/danger` | 안동맥과 문합 — 역행성 색전 경로 | [0, 19] | 경로 |  |
| MX-S06-006 | `/zones/5/nerves/1/name` | 협근신경 (Buccal branch of facial nerve) | [0, 36] | 신경명, 영문 병기 |  |
| MX-S06-007 | `/zones/5/nerves/1/significance` | 협근, 구륜근 상부 운동 | [0, 13] | 기능 |  |
| MX-S06-008 | `/zones/5/safe_injection_depth` | 피하 또는 피하-근막 경계 (SMAS 상방) | [0, 24] | 층, 대안(또는), 연결 하이픈 |  |
| MX-S06-009 | `/zones/5/tissue_data/notes` | 안면동맥 분지가 NLF 인접부에 존재하는 비율은 93.3%이며, 이 중 NLF 5mm 이내 주행은 약 42.9% | [0, 62] | 비율, 부분집합, 거리 상한 |  |
| MX-S06-010 | `/zones/5/clinical_pearls/1` | 안면동맥 직경: 하악 1.9mm → 비측 0.8mm (상방으로 가늘어짐) | [0, 40] | 위치별 수치, 변화(→) |  |
| MX-S06-011 | `/zones/5/clinical_pearls/2` | NLF 상단부에서 각동맥으로 이행 → 안동맥 문합 → 실명 위험 | [0, 35] | 연쇄(→) |  |
| MX-S06-012 | `/zones/5/clinical_pearls/3` | 캐뉼러 사용 시 혈관 천자 위험 현저히 감소 | [0, 24] | 조건(시), 정도(현저히) |  |
| MX-S06-013 | `/zones/5/clinical_pearls/4` | 깊은 층(SMAS 하방) 절대 금지 | [0, 19] | 강조(절대), 금지 |  |
| MX-S06-014 | `/zones/5/clinical_pearls/4` | 안면동맥은 심부 주행 | [22, 33] | 위치 |  |
| MX-S06-015 | `/zones/5/botox_specific/target_muscle` | 상순거근 (Levator labii superioris) — NLF 보조 치료 | [0, 43] | 근육명, 보조 |  |
| MX-S06-016 | `/zones/5/botox_specific/risk` | 상순 거상 약화 → 미소 비대칭, 음식물 흘림 | [0, 25] | 결과(→) |  |
| MX-S06-017 | `/zones/5/botox_specific/safe_zone` | NLF 필러와 병행 | [0, 10] | 병행, 참조 |  |
| MX-S06-018 | `/zones/5/botox_specific/safe_zone` | 보톡스 단독은 드묾 | [12, 22] | 빈도(드묾) |  |
| MX-S06-019 | `/zones/5/botox_specific/key_warning` | NLF 보톡스는 부작용 위험 대비 효과 제한적 — 필러 우선 | [0, 33] | 비교(대비), 한계(제한적), 우선 |  |
| MX-S06-020 | `/zones/5/botox_specific/dose_range` | 2-4U/측 (NLF 보조 시) | [0, 17] | 범위, 단위당, 조건(시) |  |
| MX-S06-021 | `/zones/5/filler_specific/primary_risk` | 안면동맥 천자 → 피부 괴사 + 역행성 색전 | [0, 24] | 결과(→), 기호(+) |  |
| MX-S06-022 | `/zones/5/filler_specific/safe_technique` | 캐뉼러 선형 역행 주입, SMAS 상방, 소량 다점 | [0, 28] | 기법, 층 |  |
| MX-S06-023 | `/zones/5/filler_specific/preferred_product` | 중점도 HA (NLF 전용) | [0, 15] | 수식, 전용 |  |
| MX-S06-024 | `/zones/5/clinical_pearls/0` | 이 중 NLF 5mm 이내 주행은 약 42.9% | [28, 54] | 부분집합(이 중), 거리 상한(이내), 근사(약), 비율 | vessels/0/course 와 동일 문자열 |

## 정규식 보조 후보 (기계 · 요약)

| 패턴 | 출현 |
|---|---|
| number_unit | 12 |
| comparator | 3 |
| condition | 3 |
| arrow | 6 |
| em_dash | 4 |
| degree_emphasis | 2 |
| negation_prohibition | 1 |
| possibility_frequency | 1 |
| range | 1 |
| slash | 1 |
| plus | 1 |

전체 출현·구간은 `expressions.json` → `regex_candidates` (section=S06).

## 전문어 분절 관찰 (Kiwi 원시 · K)

| Pointer | 낱말 | 구간 | Kiwi 토큰 | 상태 |
|---|---|---|---|---|
| `/zones/5/name_ko` | 팔자주름 | [0, 4] | 팔자/NNG + 주름/NNG | K: 여러 형태소로 분절(원시 결과 보존) |
| `/zones/5/vessels/0/name` | 안면동맥 | [0, 4] | 안면/NNG + 동맥/NNG | K: 여러 형태소로 분절(원시 결과 보존) |
| `/zones/5/vessels/0/course` | 안면동맥 | [0, 4] | 안면/NNG + 동맥/NNG | K: 여러 형태소로 분절(원시 결과 보존) |
| `/zones/5/vessels/0/danger` | 안면동맥 | [9, 13] | 안면/NNG + 동맥/NNG | K: 여러 형태소로 분절(원시 결과 보존) |
| `/zones/5/vessels/1/course` | 안면동맥 | [23, 27] | 안면/NNG + 동맥/NNG | K: 여러 형태소로 분절(원시 결과 보존) |
| `/zones/5/vessels/1/danger` | 역행성 | [10, 13] | 역행/NNG + 성/XSN | K: 여러 형태소로 분절(원시 결과 보존) |
| `/zones/5/tissue_data/notes` | 안면동맥 | [0, 4] | 안면/NNG + 동맥/NNG | K: 여러 형태소로 분절(원시 결과 보존) |
| `/zones/5/clinical_pearls/0` | 안면동맥 | [0, 4] | 안면/NNG + 동맥/NNG | K: 여러 형태소로 분절(원시 결과 보존) |
| `/zones/5/clinical_pearls/1` | 안면동맥 | [0, 4] | 안면/NNG + 동맥/NNG | K: 여러 형태소로 분절(원시 결과 보존) |
| `/zones/5/clinical_pearls/4` | 안면동맥 | [22, 26] | 안면/NNG + 동맥/NNG | K: 여러 형태소로 분절(원시 결과 보존) |
| `/zones/5/botox_specific/target_muscle` | 상순거근 | [0, 4] | 상순/NNG + 거/MM + 근/NNG | K: 여러 형태소로 분절(원시 결과 보존) |
| `/zones/5/filler_specific/primary_risk` | 안면동맥 | [0, 4] | 안면/NNG + 동맥/NNG | K: 여러 형태소로 분절(원시 결과 보존) |
| `/zones/5/filler_specific/primary_risk` | 역행성 | [18, 21] | 역행/NNG + 성/XSN | K: 여러 형태소로 분절(원시 결과 보존) |
| `/zones/5/filler_specific/preferred_product` | 중점도 | [0, 3] | 중점/NNG + 도/JX | K: 여러 형태소로 분절(원시 결과 보존) |

단일 형태소로 나온 출현은 표에서 생략했다(`morphology.json` → `segmentation_review` 에 전부 있음).

