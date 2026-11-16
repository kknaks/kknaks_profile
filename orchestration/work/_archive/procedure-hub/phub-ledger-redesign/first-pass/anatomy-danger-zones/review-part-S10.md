# S10 — zones[9] jawline (턱선 / Jawline (Mandibular border))

[← review.md](review.md) · 범위 `/zones/9/**` · 소유 노드 52 · 말단 41 · 직접 읽기 done

상위 문맥: 루트 객체 → `zones` 배열(S00 소유) → `/zones/9` (id=`jawline`, name_ko=`턱선`, name_en=`Jawline (Mandibular border)`).

## 원문 값 (문서 순서 · 전부)

| # | JSON Pointer | 원본 컬럼명 | 배열 순번 | 자료형 | 원문 값 |
|---|---|---|---|---|---|
| 512 | `/zones/9` | `(zones 원소)` | 9 | object{12} | (컨테이너 · 키: `id`, `name_ko`, `name_en`, `danger_level`, `danger_color`, `vessels`, `nerves`, `safe_injection_depth`, `tissue_data`, `clinical_pearls`, `botox_specific`, `filler_specific`) |
| 513 | `/zones/9/id` | `id` |  | string | jawline |
| 514 | `/zones/9/name_ko` | `name_ko` |  | string | 턱선 |
| 515 | `/zones/9/name_en` | `name_en` |  | string | Jawline (Mandibular border) |
| 516 | `/zones/9/danger_level` | `danger_level` |  | integer | `4` |
| 517 | `/zones/9/danger_color` | `danger_color` |  | string | orange |
| 518 | `/zones/9/vessels` | `vessels` |  | array[2] | (배열 · 2개) |
| 519 | `/zones/9/vessels/0` | `(vessels 원소)` | 0 | object{5} | (컨테이너 · 키: `name`, `depth_mm`, `diameter_mm`, `course`, `danger`) |
| 520 | `/zones/9/vessels/0/name` | `name` |  | string | 안면동맥 (Facial artery) |
| 521 | `/zones/9/vessels/0/depth_mm` | `depth_mm` |  | number | `4.0` |
| 522 | `/zones/9/vessels/0/diameter_mm` | `diameter_mm` |  | number | `1.9` |
| 523 | `/zones/9/vessels/0/course` | `course` |  | string | 하악각 전방에서 하악연을 넘어 상방 주행 — 하악 부위에서 가장 굵음(1.9mm) |
| 524 | `/zones/9/vessels/0/danger` | `danger` |  | string | 하악연 주변 깊은 주사 시 대량 출혈·혈종; 동맥 내 주입 시 혈관 폐색 → 피부 괴사 (blanching·livedo reticularis·지연성 capillary refill·통증 증가가 조기 징후) |
| 525 | `/zones/9/vessels/1` | `(vessels 원소)` | 1 | object{5} | (컨테이너 · 키: `name`, `depth_mm`, `diameter_mm`, `course`, `danger`) |
| 526 | `/zones/9/vessels/1/name` | `name` |  | string | 안면정맥 (Facial vein) |
| 527 | `/zones/9/vessels/1/depth_mm` | `depth_mm` |  | number | `3.0` |
| 528 | `/zones/9/vessels/1/diameter_mm` | `diameter_mm` |  | number | `2.5` |
| 529 | `/zones/9/vessels/1/course` | `course` |  | string | 안면동맥보다 외측, 하악연을 따라 주행 |
| 530 | `/zones/9/vessels/1/danger` | `danger` |  | string | 정맥 천자 → 혈종, 드물게 정맥 혈전 |
| 531 | `/zones/9/nerves` | `nerves` |  | array[2] | (배열 · 2개) |
| 532 | `/zones/9/nerves/0` | `(nerves 원소)` | 0 | object{3} | (컨테이너 · 키: `name`, `type`, `significance`) |
| 533 | `/zones/9/nerves/0/name` | `name` |  | string | 하악변연신경 (Marginal mandibular nerve) |
| 534 | `/zones/9/nerves/0/type` | `type` |  | string | motor |
| 535 | `/zones/9/nerves/0/significance` | `significance` |  | string | 하순하제근(DLI), 이근 운동 — 손상 시 비대칭 미소 (하순 하강 불가) |
| 536 | `/zones/9/nerves/1` | `(nerves 원소)` | 1 | object{3} | (컨테이너 · 키: `name`, `type`, `significance`) |
| 537 | `/zones/9/nerves/1/name` | `name` |  | string | 이신경 (Mental nerve) |
| 538 | `/zones/9/nerves/1/type` | `type` |  | string | sensory |
| 539 | `/zones/9/nerves/1/significance` | `significance` |  | string | 하순, 턱 피부 감각 |
| 540 | `/zones/9/safe_injection_depth` | `safe_injection_depth` |  | string | 골막상 또는 피하 (하악연 위/아래 구분) |
| 541 | `/zones/9/tissue_data` | `tissue_data` |  | object{3} | (컨테이너 · 키: `marginal_mandibular_depth`, `facial_artery_crossing`, `notes`) |
| 542 | `/zones/9/tissue_data/marginal_mandibular_depth` | `marginal_mandibular_depth` |  | string | 하악연에서 1-2cm 하방에서 표재성 주행 (20% 환자에서 하악연 하방 1cm까지) |
| 543 | `/zones/9/tissue_data/facial_artery_crossing` | `facial_artery_crossing` |  | string | 안면동맥은 하악연의 교근 전연(anterior border of masseter)에서 교차 |
| 544 | `/zones/9/tissue_data/notes` | `notes` |  | string | 안면동맥: 하악각 부위에서 직경 1.9mm로 가장 굵음 — 하악연 주사 최대 위험 혈관 |
| 545 | `/zones/9/clinical_pearls` | `clinical_pearls` |  | array[6] | (배열 · 6개) |
| 546 | `/zones/9/clinical_pearls/0` | `(clinical_pearls 원소)` | 0 | string | 안면동맥: 하악각 부위에서 가장 굵음(1.9mm) — 교근 전연에서 하악연 교차 |
| 547 | `/zones/9/clinical_pearls/1` | `(clinical_pearls 원소)` | 1 | string | 하악변연신경: 모터 신경 → 손상 시 비대칭 미소 (하순 하강 불가) |
| 548 | `/zones/9/clinical_pearls/2` | `(clinical_pearls 원소)` | 2 | string | 하악변연신경은 하악연 하방 1-2cm에서 표재성 주행 (20%는 1cm 하방) |
| 549 | `/zones/9/clinical_pearls/3` | `(clinical_pearls 원소)` | 3 | string | 하악연 주사 전 안면동맥 촉진 필수 |
| 550 | `/zones/9/clinical_pearls/4` | `(clinical_pearls 원소)` | 4 | string | 턱선 필러는 하악연 위(상방)에서 골막상 주사가 가장 안전 |
| 551 | `/zones/9/clinical_pearls/5` | `(clinical_pearls 원소)` | 5 | string | 혈관폐색 의심 시 즉시 시술 중단, 발생 4-6시간 내 고용량 반복 히알루로니다제 시행 |
| 552 | `/zones/9/botox_specific` | `botox_specific` |  | object{5} | (컨테이너 · 키: `target_muscle`, `risk`, `safe_zone`, `key_warning`, `dose_range`) |
| 553 | `/zones/9/botox_specific/target_muscle` | `target_muscle` |  | string | 교근 (Masseter) — 사각턱, 광경근 (Platysma) — 턱선 리프트 |
| 554 | `/zones/9/botox_specific/risk` | `risk` |  | string | 하악변연신경 마비 → 비대칭 미소, 교근 과위축 |
| 555 | `/zones/9/botox_specific/safe_zone` | `safe_zone` |  | string | 교근 하방 1/3, 하악연 상방 |
| 556 | `/zones/9/botox_specific/key_warning` | `key_warning` |  | string | 교근 전연 상방 주사 → 하악변연신경/협근신경 마비 위험 |
| 557 | `/zones/9/botox_specific/dose_range` | `dose_range` |  | string | 교근 25-50U/측, Nefertiti lift (광경근) 2-4U x 4-6포인트 |
| 558 | `/zones/9/filler_specific` | `filler_specific` |  | object{5} | (컨테이너 · 키: `risk_level`, `primary_risk`, `safe_technique`, `max_per_point_ml`, `preferred_product`) |
| 559 | `/zones/9/filler_specific/risk_level` | `risk_level` |  | integer | `4` |
| 560 | `/zones/9/filler_specific/primary_risk` | `primary_risk` |  | string | 안면동맥 내 주입에 의한 occlusion→necrosis, 안면동맥 천자(1.9mm 굵은 동맥), 하악변연신경 손상 |
| 561 | `/zones/9/filler_specific/safe_technique` | `safe_technique` |  | string | 하악연 상방 골막상 캐뉼러, 동맥 촉진 후 회피, 소량 연속 |
| 562 | `/zones/9/filler_specific/max_per_point_ml` | `max_per_point_ml` |  | number | `0.2` |
| 563 | `/zones/9/filler_specific/preferred_product` | `preferred_product` |  | string | 고점도 HA 또는 CaHA (턱선 윤곽용) |

## 잠정 관찰 (원문 칸과 분리)

| # | 상태 | 근거 Pointer | 관찰 | issues.md |
|---|---|---|---|---|
| OBS-S10-01 | I | `/zones/9/tissue_data/marginal_mandibular_depth`, `/zones/9/clinical_pearls/2` | tissue_data 는 '(20% 환자에서 하악연 하방 1cm까지)', pearls 는 '(20%는 1cm 하방)' 으로 같은 20% 를 다른 범위 표현으로 적었다. | ADZ-I04 |
| OBS-S10-02 | P | `/zones/9/filler_specific/primary_risk` | 'occlusion→necrosis' 는 공백 없이 붙은 화살표다. 형태소 분석에서 한 덩어리 또는 분리 처리될 수 있다. | ADZ-K |
| OBS-S10-03 | P | `/zones/9/vessels/0/danger` | 조기 징후 네 개를 가운뎃점으로 나열(blanching·livedo reticularis·지연성 capillary refill·통증 증가). 한·영 혼합 나열이다. |  |
| OBS-S10-04 | P | `/zones/9/clinical_pearls/5` | '발생 4-6시간 내' 시간 창과 '고용량 반복' 이 같은 문장에 있다. |  |
| OBS-S10-05 | F | `/zones/9/clinical_pearls/1`, `/zones/9/nerves/0/type` | '모터 신경' 과 type 값 'motor' — 한글 음차와 영문 코드값. | ADZ-F13 |

## 수동 복합 표현 (직접 읽기)

탐색 관점은 수집용 꼬리표이며 확정 분류가 아니다. 구간은 값 문자열 기준 코드 포인트 `[start,end)`.

| ID | Pointer | 원문 구간 | 구간 | 탐색 관점 | 메모 |
|---|---|---|---|---|---|
| MX-S10-001 | `/zones/9/name_en` | Jawline (Mandibular border) | [0, 27] | 영문 명칭, 괄호 병기 |  |
| MX-S10-002 | `/zones/9/vessels/0/course` | 하악각 전방에서 하악연을 넘어 상방 주행 | [0, 22] | 위치·방향 |  |
| MX-S10-003 | `/zones/9/vessels/0/course` | 하악 부위에서 가장 굵음(1.9mm) | [25, 45] | 최상급, 수량 |  |
| MX-S10-004 | `/zones/9/vessels/0/danger` | 하악연 주변 깊은 주사 시 대량 출혈·혈종 | [0, 23] | 조건(시), 결과 |  |
| MX-S10-005 | `/zones/9/vessels/0/danger` | 동맥 내 주입 시 혈관 폐색 → 피부 괴사 | [25, 48] | 조건(시), 결과(→) |  |
| MX-S10-006 | `/zones/9/vessels/0/danger` | blanching·livedo reticularis·지연성 capillary refill·통증 증가가 조기 징후 | [50, 112] | 징후 나열, 시간(조기) |  |
| MX-S10-007 | `/zones/9/vessels/1/course` | 안면동맥보다 외측, 하악연을 따라 주행 | [0, 21] | 비교(보다), 위치 |  |
| MX-S10-008 | `/zones/9/vessels/1/danger` | 정맥 천자 → 혈종, 드물게 정맥 혈전 | [0, 21] | 결과(→), 빈도(드물게) |  |
| MX-S10-009 | `/zones/9/nerves/0/significance` | 하순하제근(DLI), 이근 운동 — 손상 시 비대칭 미소 (하순 하강 불가) | [0, 42] | 기능, 조건(시), 불가 |  |
| MX-S10-010 | `/zones/9/safe_injection_depth` | 골막상 또는 피하 (하악연 위/아래 구분) | [0, 23] | 층, 대안(또는), 기호(/) |  |
| MX-S10-011 | `/zones/9/tissue_data/marginal_mandibular_depth` | 하악연에서 1-2cm 하방에서 표재성 주행 | [0, 23] | 범위, 위치 |  |
| MX-S10-012 | `/zones/9/tissue_data/marginal_mandibular_depth` | 20% 환자에서 하악연 하방 1cm까지 | [25, 46] | 비율, 범위(까지) |  |
| MX-S10-013 | `/zones/9/tissue_data/facial_artery_crossing` | 안면동맥은 하악연의 교근 전연(anterior border of masseter)에서 교차 | [0, 50] | 해부 관계, 영문 병기 |  |
| MX-S10-014 | `/zones/9/tissue_data/notes` | 안면동맥: 하악각 부위에서 직경 1.9mm로 가장 굵음 | [0, 30] | 수량, 최상급 |  |
| MX-S10-015 | `/zones/9/tissue_data/notes` | 하악연 주사 최대 위험 혈관 | [33, 48] | 최상급 |  |
| MX-S10-016 | `/zones/9/clinical_pearls/0` | 교근 전연에서 하악연 교차 | [30, 44] | 해부 관계 |  |
| MX-S10-017 | `/zones/9/clinical_pearls/1` | 하악변연신경: 모터 신경 → 손상 시 비대칭 미소 (하순 하강 불가) | [0, 38] | 결과(→), 조건(시), 불가 |  |
| MX-S10-018 | `/zones/9/clinical_pearls/2` | 하악변연신경은 하악연 하방 1-2cm에서 표재성 주행 (20%는 1cm 하방) | [0, 43] | 범위, 비율 |  |
| MX-S10-019 | `/zones/9/clinical_pearls/3` | 하악연 주사 전 안면동맥 촉진 필수 | [0, 19] | 시간(전), 필수 |  |
| MX-S10-020 | `/zones/9/clinical_pearls/4` | 턱선 필러는 하악연 위(상방)에서 골막상 주사가 가장 안전 | [0, 32] | 위치, 최상급 |  |
| MX-S10-021 | `/zones/9/clinical_pearls/5` | 혈관폐색 의심 시 즉시 시술 중단 | [0, 18] | 조건(의심 시), 시간(즉시) |  |
| MX-S10-022 | `/zones/9/clinical_pearls/5` | 발생 4-6시간 내 고용량 반복 히알루로니다제 시행 | [20, 48] | 시간 창(4-6시간 내), 수식(고용량·반복) |  |
| MX-S10-023 | `/zones/9/botox_specific/target_muscle` | 교근 (Masseter) — 사각턱, 광경근 (Platysma) — 턱선 리프트 | [0, 44] | 근육명, 적응 |  |
| MX-S10-024 | `/zones/9/botox_specific/risk` | 하악변연신경 마비 → 비대칭 미소, 교근 과위축 | [0, 26] | 결과(→) |  |
| MX-S10-025 | `/zones/9/botox_specific/safe_zone` | 교근 하방 1/3, 하악연 상방 | [0, 17] | 분수(1/3), 위치 |  |
| MX-S10-026 | `/zones/9/botox_specific/key_warning` | 교근 전연 상방 주사 → 하악변연신경/협근신경 마비 위험 | [0, 31] | 결과(→), 기호(/) |  |
| MX-S10-027 | `/zones/9/botox_specific/dose_range` | 교근 25-50U/측 | [0, 11] | 근육+범위, 단위당 |  |
| MX-S10-028 | `/zones/9/botox_specific/dose_range` | Nefertiti lift (광경근) 2-4U x 4-6포인트 | [13, 47] | 시술명, 범위, 곱(x) |  |
| MX-S10-029 | `/zones/9/filler_specific/primary_risk` | 안면동맥 내 주입에 의한 occlusion→necrosis | [0, 32] | 원인(에 의한), 결과(→ 붙임) |  |
| MX-S10-030 | `/zones/9/filler_specific/primary_risk` | 안면동맥 천자(1.9mm 굵은 동맥) | [34, 54] | 수량, 수식 |  |
| MX-S10-031 | `/zones/9/filler_specific/safe_technique` | 하악연 상방 골막상 캐뉼러, 동맥 촉진 후 회피, 소량 연속 | [0, 33] | 순서(후), 기법 |  |
| MX-S10-032 | `/zones/9/filler_specific/preferred_product` | 고점도 HA 또는 CaHA (턱선 윤곽용) | [0, 23] | 대안(또는), 용도 |  |

## 정규식 보조 후보 (기계 · 요약)

| 패턴 | 출현 |
|---|---|
| number_unit | 14 |
| degree_emphasis | 6 |
| em_dash | 6 |
| condition | 5 |
| time_order | 5 |
| arrow | 6 |
| middle_dot | 4 |
| possibility_frequency | 1 |
| negation_prohibition | 2 |
| slash | 4 |
| range | 6 |
| comparator | 1 |

전체 출현·구간은 `expressions.json` → `regex_candidates` (section=S10).

## 전문어 분절 관찰 (Kiwi 원시 · K)

| Pointer | 낱말 | 구간 | Kiwi 토큰 | 상태 |
|---|---|---|---|---|
| `/zones/9/vessels/0/name` | 안면동맥 | [0, 4] | 안면/NNG + 동맥/NNG | K: 여러 형태소로 분절(원시 결과 보존) |
| `/zones/9/vessels/1/course` | 안면동맥 | [0, 4] | 안면/NNG + 동맥/NNG | K: 여러 형태소로 분절(원시 결과 보존) |
| `/zones/9/nerves/0/name` | 하악변연신경 | [0, 6] | 하악/NNG + 변연/NNG + 신경/NNG | K: 여러 형태소로 분절(원시 결과 보존) |
| `/zones/9/nerves/0/significance` | 하순하제근 | [0, 5] | 하순/NNG + 하/NNG + 제/NNG + 근/NNG | K: 여러 형태소로 분절(원시 결과 보존) |
| `/zones/9/tissue_data/marginal_mandibular_depth` | 표재성 | [17, 20] | 표재/NNG + 성/XSN | K: 여러 형태소로 분절(원시 결과 보존) |
| `/zones/9/tissue_data/facial_artery_crossing` | 교근 | [11, 13] | 교/NNG + 근/NNG | K: 여러 형태소로 분절(원시 결과 보존) |
| `/zones/9/tissue_data/notes` | 안면동맥 | [0, 4] | 안면/NNG + 동맥/NNG | K: 여러 형태소로 분절(원시 결과 보존) |
| `/zones/9/clinical_pearls/0` | 안면동맥 | [0, 4] | 안면/NNG + 동맥/NNG | K: 여러 형태소로 분절(원시 결과 보존) |
| `/zones/9/clinical_pearls/0` | 교근 | [30, 32] | 교/NNG + 근/NNG | K: 여러 형태소로 분절(원시 결과 보존) |
| `/zones/9/clinical_pearls/1` | 하악변연신경 | [0, 6] | 하악/NNG + 변연/NNG + 신경/NNG | K: 여러 형태소로 분절(원시 결과 보존) |
| `/zones/9/clinical_pearls/2` | 하악변연신경 | [0, 6] | 하악/NNG + 변연/NNG + 신경/NNG | K: 여러 형태소로 분절(원시 결과 보존) |
| `/zones/9/clinical_pearls/2` | 표재성 | [23, 26] | 표재/NNG + 성/XSN | K: 여러 형태소로 분절(원시 결과 보존) |
| `/zones/9/clinical_pearls/3` | 안면동맥 | [9, 13] | 안면/NNG + 동맥/NNG | K: 여러 형태소로 분절(원시 결과 보존) |
| `/zones/9/clinical_pearls/4` | 골막상 | [19, 22] | 골/NNG + 막상/MAG | K: 여러 형태소로 분절(원시 결과 보존) |
| `/zones/9/botox_specific/target_muscle` | 교근 | [0, 2] | 교/NNG + 근/NNG | K: 여러 형태소로 분절(원시 결과 보존) |
| `/zones/9/botox_specific/risk` | 교근 | [20, 22] | 교/NNG + 근/NNG | K: 여러 형태소로 분절(원시 결과 보존) |
| `/zones/9/botox_specific/risk` | 하악변연신경 | [0, 6] | 하악/NNG + 변연/NNG + 신경/NNG | K: 여러 형태소로 분절(원시 결과 보존) |
| `/zones/9/botox_specific/safe_zone` | 교근 | [0, 2] | 교/NNG + 근/NNG | K: 여러 형태소로 분절(원시 결과 보존) |
| `/zones/9/botox_specific/key_warning` | 교근 | [0, 2] | 교/NNG + 근/NNG | K: 여러 형태소로 분절(원시 결과 보존) |
| `/zones/9/botox_specific/key_warning` | 하악변연신경 | [14, 20] | 하악/NNG + 변연/NNG + 신경/NNG | K: 여러 형태소로 분절(원시 결과 보존) |
| `/zones/9/botox_specific/dose_range` | 교근 | [0, 2] | 교/NNG + 근/NNG | K: 여러 형태소로 분절(원시 결과 보존) |
| `/zones/9/filler_specific/primary_risk` | 안면동맥 | [0, 4] | 안면/NNG + 동맥/NNG | K: 여러 형태소로 분절(원시 결과 보존) |
| `/zones/9/filler_specific/primary_risk` | 안면동맥 | [34, 38] | 안면/NNG + 동맥/NNG | K: 여러 형태소로 분절(원시 결과 보존) |
| `/zones/9/filler_specific/primary_risk` | 하악변연신경 | [56, 62] | 하악/NNG + 변연/NNG + 신경/NNG | K: 여러 형태소로 분절(원시 결과 보존) |
| `/zones/9/filler_specific/safe_technique` | 골막상 | [7, 10] | 골/NNG + 막상/MAG | K: 여러 형태소로 분절(원시 결과 보존) |
| `/zones/9/filler_specific/preferred_product` | 고점도 | [0, 3] | 고/MM + 점/NNG + 도/JX | K: 여러 형태소로 분절(원시 결과 보존) |

단일 형태소로 나온 출현은 표에서 생략했다(`morphology.json` → `segmentation_review` 에 전부 있음).

