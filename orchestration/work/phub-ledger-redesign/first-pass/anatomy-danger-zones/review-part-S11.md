# S11 — zones[10] neck (목 / Neck)

[← review.md](review.md) · 범위 `/zones/10/**` · 소유 노드 51 · 말단 40 · 직접 읽기 done

상위 문맥: 루트 객체 → `zones` 배열(S00 소유) → `/zones/10` (id=`neck`, name_ko=`목`, name_en=`Neck`).

## 원문 값 (문서 순서 · 전부)

| # | JSON Pointer | 원본 컬럼명 | 배열 순번 | 자료형 | 원문 값 |
|---|---|---|---|---|---|
| 564 | `/zones/10` | `(zones 원소)` | 10 | object{12} | (컨테이너 · 키: `id`, `name_ko`, `name_en`, `danger_level`, `danger_color`, `vessels`, `nerves`, `safe_injection_depth`, `tissue_data`, `clinical_pearls`, `botox_specific`, `filler_specific`) |
| 565 | `/zones/10/id` | `id` |  | string | neck |
| 566 | `/zones/10/name_ko` | `name_ko` |  | string | 목 |
| 567 | `/zones/10/name_en` | `name_en` |  | string | Neck |
| 568 | `/zones/10/danger_level` | `danger_level` |  | integer | `2` |
| 569 | `/zones/10/danger_color` | `danger_color` |  | string | green |
| 570 | `/zones/10/vessels` | `vessels` |  | array[2] | (배열 · 2개) |
| 571 | `/zones/10/vessels/0` | `(vessels 원소)` | 0 | object{5} | (컨테이너 · 키: `name`, `depth_mm`, `diameter_mm`, `course`, `danger`) |
| 572 | `/zones/10/vessels/0/name` | `name` |  | string | 외경정맥 (External jugular vein) |
| 573 | `/zones/10/vessels/0/depth_mm` | `depth_mm` |  | number | `5.0` |
| 574 | `/zones/10/vessels/0/diameter_mm` | `diameter_mm` |  | number | `5.0` |
| 575 | `/zones/10/vessels/0/course` | `course` |  | string | 흉쇄유돌근(SCM) 표면을 사선으로 주행 |
| 576 | `/zones/10/vessels/0/danger` | `danger` |  | string | 대형 정맥 — 천자 시 대량 출혈 |
| 577 | `/zones/10/vessels/1` | `(vessels 원소)` | 1 | object{5} | (컨테이너 · 키: `name`, `depth_mm`, `diameter_mm`, `course`, `danger`) |
| 578 | `/zones/10/vessels/1/name` | `name` |  | string | 전경정맥 (Anterior jugular vein) |
| 579 | `/zones/10/vessels/1/depth_mm` | `depth_mm` |  | number | `3.0` |
| 580 | `/zones/10/vessels/1/diameter_mm` | `diameter_mm` |  | number | `3.0` |
| 581 | `/zones/10/vessels/1/course` | `course` |  | string | 정중선 양측, 피하 주행 |
| 582 | `/zones/10/vessels/1/danger` | `danger` |  | string | 정중선 목 주사 시 주의 |
| 583 | `/zones/10/nerves` | `nerves` |  | array[2] | (배열 · 2개) |
| 584 | `/zones/10/nerves/0` | `(nerves 원소)` | 0 | object{3} | (컨테이너 · 키: `name`, `type`, `significance`) |
| 585 | `/zones/10/nerves/0/name` | `name` |  | string | 대이개신경 (Great auricular nerve) |
| 586 | `/zones/10/nerves/0/type` | `type` |  | string | sensory |
| 587 | `/zones/10/nerves/0/significance` | `significance` |  | string | 이개, 이하부 감각 — SCM 중간부 표면에서 표재성 |
| 588 | `/zones/10/nerves/1` | `(nerves 원소)` | 1 | object{3} | (컨테이너 · 키: `name`, `type`, `significance`) |
| 589 | `/zones/10/nerves/1/name` | `name` |  | string | 부신경 (Spinal accessory nerve, CN XI) |
| 590 | `/zones/10/nerves/1/type` | `type` |  | string | motor |
| 591 | `/zones/10/nerves/1/significance` | `significance` |  | string | 승모근, 흉쇄유돌근 운동 — 손상 시 어깨 처짐 |
| 592 | `/zones/10/safe_injection_depth` | `safe_injection_depth` |  | string | 광경근(Platysma) 내 또는 피내 (진피층) |
| 593 | `/zones/10/tissue_data` | `tissue_data` |  | object{3} | (컨테이너 · 키: `platysma_thickness_mm`, `platysma_coverage`, `notes`) |
| 594 | `/zones/10/tissue_data/platysma_thickness_mm` | `platysma_thickness_mm` |  | number | `1.5` |
| 595 | `/zones/10/tissue_data/platysma_coverage` | `platysma_coverage` |  | string | 광경근은 쇄골~하악연까지, 정중선에서 결손 부위 있음 |
| 596 | `/zones/10/tissue_data/notes` | `notes` |  | string | 광경근(Platysma) 하방에 외경정맥 등 주요 혈관 — 광경근 관통 주사 주의 |
| 597 | `/zones/10/clinical_pearls` | `clinical_pearls` |  | array[5] | (배열 · 5개) |
| 598 | `/zones/10/clinical_pearls/0` | `(clinical_pearls 원소)` | 0 | string | 광경근(Platysma) 하방에 주요 혈관/신경 → 피내 또는 광경근 내 주사 |
| 599 | `/zones/10/clinical_pearls/1` | `(clinical_pearls 원소)` | 1 | string | 외경정맥은 직경 5mm 이상 — 촉진/가시적 확인 가능 |
| 600 | `/zones/10/clinical_pearls/2` | `(clinical_pearls 원소)` | 2 | string | 목 보톡스(Nefertiti lift)는 광경근 band에 소량 다점 주사 |
| 601 | `/zones/10/clinical_pearls/3` | `(clinical_pearls 원소)` | 3 | string | 목 필러는 거의 사용하지 않음 — 스킨부스터/바이오스티뮬레이터 위주 |
| 602 | `/zones/10/clinical_pearls/4` | `(clinical_pearls 원소)` | 4 | string | 갑상선, 경동맥 등 심부 구조물에 대한 안전 거리 확보 |
| 603 | `/zones/10/botox_specific` | `botox_specific` |  | object{5} | (컨테이너 · 키: `target_muscle`, `risk`, `safe_zone`, `key_warning`, `dose_range`) |
| 604 | `/zones/10/botox_specific/target_muscle` | `target_muscle` |  | string | 광경근 (Platysma) — platysmal bands, 목 주름 |
| 605 | `/zones/10/botox_specific/risk` | `risk` |  | string | 연하곤란(dysphagia), 경부 약화, 호흡 불편 |
| 606 | `/zones/10/botox_specific/safe_zone` | `safe_zone` |  | string | 광경근 band 직상, 피하 표재성 |
| 607 | `/zones/10/botox_specific/key_warning` | `key_warning` |  | string | 깊은 주사 → 인두근/후두근 마비 → 연하곤란/발성장애 |
| 608 | `/zones/10/botox_specific/dose_range` | `dose_range` |  | string | Platysmal band 2-4U x 4-6포인트/band, 총 20-60U |
| 609 | `/zones/10/filler_specific` | `filler_specific` |  | object{5} | (컨테이너 · 키: `risk_level`, `primary_risk`, `safe_technique`, `max_per_point_ml`, `preferred_product`) |
| 610 | `/zones/10/filler_specific/risk_level` | `risk_level` |  | integer | `2` |
| 611 | `/zones/10/filler_specific/primary_risk` | `primary_risk` |  | string | 외경정맥 천자(혈종), 깊은 주사 시 기도/식도 위험 |
| 612 | `/zones/10/filler_specific/safe_technique` | `safe_technique` |  | string | 피내 주사 위주, 스킨부스터/바이오스티뮬레이터 사용 |
| 613 | `/zones/10/filler_specific/max_per_point_ml` | `max_per_point_ml` |  | number | `0.1` |
| 614 | `/zones/10/filler_specific/preferred_product` | `preferred_product` |  | string | 스킨부스터(Profhilo 등) 또는 희석 CaHA |

## 잠정 관찰 (원문 칸과 분리)

| # | 상태 | 근거 Pointer | 관찰 | issues.md |
|---|---|---|---|---|
| OBS-S11-01 | P | `/zones/10/clinical_pearls/3`, `/zones/10/filler_specific` | pearls 는 '목 필러는 거의 사용하지 않음' 이라 하나 filler_specific 객체는 다른 zone 과 같은 구조로 채워져 있다(max_per_point_ml 0.1 등). | ADZ-P23 |
| OBS-S11-02 | P | `/zones/10/vessels/0/diameter_mm`, `/zones/10/clinical_pearls/1` | diameter_mm 5.0 과 pearls '직경 5mm 이상' — 점값과 하한 표현. |  |
| OBS-S11-03 | P | `/zones/10/safe_injection_depth`, `/zones/10/botox_specific/safe_zone`, `/zones/10/filler_specific/safe_technique` | 층 표현이 '광경근 내 또는 피내 (진피층)', '피하 표재성', '피내 주사 위주' 로 필드마다 다르다. |  |
| OBS-S11-04 | P | `/zones/10/tissue_data/platysma_coverage` | '쇄골~하악연까지' 의 '~' 는 공간 범위다. | ADZ-P11 |
| OBS-S11-05 | F | `/zones/10/clinical_pearls/2`, `/zones/9/botox_specific/dose_range` | 'Nefertiti lift' 가 neck pearls 와 jawline dose_range 양쪽에 나온다. | ADZ-F14 |
| OBS-S11-06 | P | `/zones/10/filler_specific/preferred_product` | 제품명 'Profhilo' 가 '등' 과 함께 예시로 나온다. 제품 체계와의 연결은 후속(다른 원장 범위). | ADZ-F14 |

## 수동 복합 표현 (직접 읽기)

탐색 관점은 수집용 꼬리표이며 확정 분류가 아니다. 구간은 값 문자열 기준 코드 포인트 `[start,end)`.

| ID | Pointer | 원문 구간 | 구간 | 탐색 관점 | 메모 |
|---|---|---|---|---|---|
| MX-S11-001 | `/zones/10/vessels/0/course` | 흉쇄유돌근(SCM) 표면을 사선으로 주행 | [0, 22] | 위치·방향, 약어 |  |
| MX-S11-002 | `/zones/10/vessels/0/danger` | 대형 정맥 — 천자 시 대량 출혈 | [0, 18] | 조건(시), 결과 |  |
| MX-S11-003 | `/zones/10/vessels/1/course` | 정중선 양측, 피하 주행 | [0, 13] | 위치 |  |
| MX-S11-004 | `/zones/10/vessels/1/danger` | 정중선 목 주사 시 주의 | [0, 13] | 조건(시), 주의 |  |
| MX-S11-005 | `/zones/10/nerves/0/significance` | 이개, 이하부 감각 — SCM 중간부 표면에서 표재성 | [0, 29] | 기능, 위치 |  |
| MX-S11-006 | `/zones/10/nerves/1/name` | 부신경 (Spinal accessory nerve, CN XI) | [0, 35] | 신경명, 영문 병기, 코드(CN XI) |  |
| MX-S11-007 | `/zones/10/nerves/1/significance` | 승모근, 흉쇄유돌근 운동 — 손상 시 어깨 처짐 | [0, 26] | 기능, 조건(시) |  |
| MX-S11-008 | `/zones/10/safe_injection_depth` | 광경근(Platysma) 내 또는 피내 (진피층) | [0, 27] | 층, 대안(또는) |  |
| MX-S11-009 | `/zones/10/tissue_data/platysma_coverage` | 광경근은 쇄골~하악연까지 | [0, 13] | 공간 범위(~·까지) |  |
| MX-S11-010 | `/zones/10/tissue_data/platysma_coverage` | 정중선에서 결손 부위 있음 | [15, 29] | 존재 |  |
| MX-S11-011 | `/zones/10/tissue_data/notes` | 광경근(Platysma) 하방에 외경정맥 등 주요 혈관 — 광경근 관통 주사 주의 | [0, 45] | 위치, 예시(등), 주의 |  |
| MX-S11-012 | `/zones/10/clinical_pearls/0` | 광경근(Platysma) 하방에 주요 혈관/신경 → 피내 또는 광경근 내 주사 | [0, 43] | 결과(→), 대안(또는), 기호(/) |  |
| MX-S11-013 | `/zones/10/clinical_pearls/1` | 외경정맥은 직경 5mm 이상 — 촉진/가시적 확인 가능 | [0, 30] | 하한(이상), 가능, 기호(/) |  |
| MX-S11-014 | `/zones/10/clinical_pearls/2` | 목 보톡스(Nefertiti lift)는 광경근 band에 소량 다점 주사 | [0, 41] | 시술명, 기법 |  |
| MX-S11-015 | `/zones/10/clinical_pearls/3` | 목 필러는 거의 사용하지 않음 | [0, 16] | 빈도(거의), 부정(않음) |  |
| MX-S11-016 | `/zones/10/clinical_pearls/3` | 스킨부스터/바이오스티뮬레이터 위주 | [19, 37] | 기호(/), 위주 |  |
| MX-S11-017 | `/zones/10/clinical_pearls/4` | 갑상선, 경동맥 등 심부 구조물에 대한 안전 거리 확보 | [0, 30] | 예시(등), 지시 |  |
| MX-S11-018 | `/zones/10/botox_specific/target_muscle` | 광경근 (Platysma) — platysmal bands, 목 주름 | [0, 38] | 근육명, 적응 |  |
| MX-S11-019 | `/zones/10/botox_specific/risk` | 연하곤란(dysphagia), 경부 약화, 호흡 불편 | [0, 29] | 부작용 나열 |  |
| MX-S11-020 | `/zones/10/botox_specific/safe_zone` | 광경근 band 직상, 피하 표재성 | [0, 19] | 위치, 층 |  |
| MX-S11-021 | `/zones/10/botox_specific/key_warning` | 깊은 주사 → 인두근/후두근 마비 → 연하곤란/발성장애 | [0, 30] | 연쇄(→), 기호(/) |  |
| MX-S11-022 | `/zones/10/botox_specific/dose_range` | Platysmal band 2-4U x 4-6포인트/band | [0, 33] | 범위, 곱(x), 단위당(/band) |  |
| MX-S11-023 | `/zones/10/botox_specific/dose_range` | 총 20-60U | [35, 43] | 총량, 범위 |  |
| MX-S11-024 | `/zones/10/filler_specific/primary_risk` | 외경정맥 천자(혈종), 깊은 주사 시 기도/식도 위험 | [0, 29] | 조건(시), 기호(/) |  |
| MX-S11-025 | `/zones/10/filler_specific/safe_technique` | 피내 주사 위주, 스킨부스터/바이오스티뮬레이터 사용 | [0, 28] | 위주, 기호(/) |  |
| MX-S11-026 | `/zones/10/filler_specific/preferred_product` | 스킨부스터(Profhilo 등) 또는 희석 CaHA | [0, 28] | 제품명 예시, 대안(또는), 수식(희석) |  |

## 정규식 보조 후보 (기계 · 요약)

| 패턴 | 출현 |
|---|---|
| condition | 4 |
| em_dash | 7 |
| comparator | 3 |
| arrow | 3 |
| slash | 8 |
| number_unit | 4 |
| possibility_frequency | 2 |
| negation_prohibition | 1 |
| range | 3 |

전체 출현·구간은 `expressions.json` → `regex_candidates` (section=S11).

## 전문어 분절 관찰 (Kiwi 원시 · K)

| Pointer | 낱말 | 구간 | Kiwi 토큰 | 상태 |
|---|---|---|---|---|
| `/zones/10/nerves/0/name` | 대이개신경 | [0, 5] | 대/XPN + 이/NR + 개/NNB + 신경/NNG | K: 여러 형태소로 분절(원시 결과 보존) |
| `/zones/10/nerves/0/significance` | 표재성 | [26, 29] | 표재/NNG + 성/XSN | K: 여러 형태소로 분절(원시 결과 보존) |
| `/zones/10/botox_specific/safe_zone` | 표재성 | [16, 19] | 표재/NNG + 성/XSN | K: 여러 형태소로 분절(원시 결과 보존) |
| `/zones/10/botox_specific/key_warning` | 연하곤란 | [21, 25] | 연하/NNG + 곤란/NNG | K: 여러 형태소로 분절(원시 결과 보존) |

단일 형태소로 나온 출현은 표에서 생략했다(`morphology.json` → `segmentation_review` 에 전부 있음).

