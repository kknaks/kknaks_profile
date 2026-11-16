# S09 — zones[8] chin (턱 / Chin (Mentum))

[← review.md](review.md) · 범위 `/zones/8/**` · 소유 노드 47 · 말단 37 · 직접 읽기 done

상위 문맥: 루트 객체 → `zones` 배열(S00 소유) → `/zones/8` (id=`chin`, name_ko=`턱`, name_en=`Chin (Mentum)`).

## 원문 값 (문서 순서 · 전부)

| # | JSON Pointer | 원본 컬럼명 | 배열 순번 | 자료형 | 원문 값 |
|---|---|---|---|---|---|
| 465 | `/zones/8` | `(zones 원소)` | 8 | object{12} | (컨테이너 · 키: `id`, `name_ko`, `name_en`, `danger_level`, `danger_color`, `vessels`, `nerves`, `safe_injection_depth`, `tissue_data`, `clinical_pearls`, `botox_specific`, `filler_specific`) |
| 466 | `/zones/8/id` | `id` |  | string | chin |
| 467 | `/zones/8/name_ko` | `name_ko` |  | string | 턱 |
| 468 | `/zones/8/name_en` | `name_en` |  | string | Chin (Mentum) |
| 469 | `/zones/8/danger_level` | `danger_level` |  | integer | `3` |
| 470 | `/zones/8/danger_color` | `danger_color` |  | string | yellow |
| 471 | `/zones/8/vessels` | `vessels` |  | array[2] | (배열 · 2개) |
| 472 | `/zones/8/vessels/0` | `(vessels 원소)` | 0 | object{5} | (컨테이너 · 키: `name`, `depth_mm`, `diameter_mm`, `course`, `danger`) |
| 473 | `/zones/8/vessels/0/name` | `name` |  | string | 이동맥 (Mental artery) |
| 474 | `/zones/8/vessels/0/depth_mm` | `depth_mm` |  | number | `8.0` |
| 475 | `/zones/8/vessels/0/diameter_mm` | `diameter_mm` |  | number | `0.8` |
| 476 | `/zones/8/vessels/0/course` | `course` |  | string | 이신경공(mental foramen)에서 출현, 하악 전면 |
| 477 | `/zones/8/vessels/0/danger` | `danger` |  | string | 이신경공 주변 깊은 주사 시 손상 |
| 478 | `/zones/8/vessels/1` | `(vessels 원소)` | 1 | object{5} | (컨테이너 · 키: `name`, `depth_mm`, `diameter_mm`, `course`, `danger`) |
| 479 | `/zones/8/vessels/1/name` | `name` |  | string | 하순동맥 분지 |
| 480 | `/zones/8/vessels/1/depth_mm` | `depth_mm` |  | number | `3.0` |
| 481 | `/zones/8/vessels/1/diameter_mm` | `diameter_mm` |  | number | `0.6` |
| 482 | `/zones/8/vessels/1/course` | `course` |  | string | 턱끝 상방, 하순에서 연장 |
| 483 | `/zones/8/vessels/1/danger` | `danger` |  | string | 턱끝 상방 주사 시 주의 |
| 484 | `/zones/8/nerves` | `nerves` |  | array[1] | (배열 · 1개) |
| 485 | `/zones/8/nerves/0` | `(nerves 원소)` | 0 | object{3} | (컨테이너 · 키: `name`, `type`, `significance`) |
| 486 | `/zones/8/nerves/0/name` | `name` |  | string | 이신경 (Mental nerve) |
| 487 | `/zones/8/nerves/0/type` | `type` |  | string | sensory |
| 488 | `/zones/8/nerves/0/significance` | `significance` |  | string | 하순, 턱 피부 감각 — 손상 시 하순/턱 감각 마비 |
| 489 | `/zones/8/safe_injection_depth` | `safe_injection_depth` |  | string | 골막상 (이부 정중앙) — 이신경공 외측 피할 것 |
| 490 | `/zones/8/tissue_data` | `tissue_data` |  | object{3} | (컨테이너 · 키: `mental_foramen_location`, `dao_coverage`, `notes`) |
| 491 | `/zones/8/tissue_data/mental_foramen_location` | `mental_foramen_location` |  | string | 하악 제2소구치 하방, 하악연에서 상방 약 13mm |
| 492 | `/zones/8/tissue_data/dao_coverage` | `dao_coverage` |  | string | DAO(구각하제근)의 67.7%가 이신경공을 덮고 있음 |
| 493 | `/zones/8/tissue_data/notes` | `notes` |  | string | 이신경공(Mental foramen): DAO의 67.7%가 덮음 — DAO 보톡스 시 이신경 손상 주의 |
| 494 | `/zones/8/clinical_pearls` | `clinical_pearls` |  | array[5] | (배열 · 5개) |
| 495 | `/zones/8/clinical_pearls/0` | `(clinical_pearls 원소)` | 0 | string | 이신경공(Mental foramen): DAO의 67.7%가 덮고 있음 |
| 496 | `/zones/8/clinical_pearls/1` | `(clinical_pearls 원소)` | 1 | string | 이신경공은 제2소구치 하방 위치 — 이 부위 깊은 주사 주의 |
| 497 | `/zones/8/clinical_pearls/2` | `(clinical_pearls 원소)` | 2 | string | 턱끝 정중앙은 상대적으로 안전 (혈관/신경 희소) |
| 498 | `/zones/8/clinical_pearls/3` | `(clinical_pearls 원소)` | 3 | string | 골막상 볼루스 주사로 턱 윤곽 교정 |
| 499 | `/zones/8/clinical_pearls/4` | `(clinical_pearls 원소)` | 4 | string | 턱끝 외측으로 갈수록 이신경/이동맥 위험 증가 |
| 500 | `/zones/8/botox_specific` | `botox_specific` |  | object{5} | (컨테이너 · 키: `target_muscle`, `risk`, `safe_zone`, `key_warning`, `dose_range`) |
| 501 | `/zones/8/botox_specific/target_muscle` | `target_muscle` |  | string | 이근 (Mentalis) — 턱 딤플(peach pit chin) |
| 502 | `/zones/8/botox_specific/risk` | `risk` |  | string | 하순 외반(lip incompetence), 이부 처짐 |
| 503 | `/zones/8/botox_specific/safe_zone` | `safe_zone` |  | string | 이부 정중앙, 이근 body 내 |
| 504 | `/zones/8/botox_specific/key_warning` | `key_warning` |  | string | 이근 과다 마비 → 하순 처짐 + 음식물 흘림 |
| 505 | `/zones/8/botox_specific/dose_range` | `dose_range` |  | string | 4-8U (정중앙 1-2포인트) |
| 506 | `/zones/8/filler_specific` | `filler_specific` |  | object{5} | (컨테이너 · 키: `risk_level`, `primary_risk`, `safe_technique`, `max_per_point_ml`, `preferred_product`) |
| 507 | `/zones/8/filler_specific/risk_level` | `risk_level` |  | integer | `3` |
| 508 | `/zones/8/filler_specific/primary_risk` | `primary_risk` |  | string | 이신경 손상(감각 마비), 이동맥 손상 |
| 509 | `/zones/8/filler_specific/safe_technique` | `safe_technique` |  | string | 정중앙 골막상 볼루스 + 캐뉼러 외측 확장 |
| 510 | `/zones/8/filler_specific/max_per_point_ml` | `max_per_point_ml` |  | number | `0.3` |
| 511 | `/zones/8/filler_specific/preferred_product` | `preferred_product` |  | string | 고점도 HA 또는 CaHA (윤곽 교정용) |

## 잠정 관찰 (원문 칸과 분리)

| # | 상태 | 근거 Pointer | 관찰 | issues.md |
|---|---|---|---|---|
| OBS-S09-01 | B | `/zones/8/tissue_data/dao_coverage`, `/zones/8/clinical_pearls/0`, `/zones/8/tissue_data/notes` | 'DAO 의 67.7% 가 이신경공을 덮고 있음' 의 67.7% 가 무엇의 비율(사례/면적 등)인지 원문에 없다. 세 곳에 같은 수치가 반복된다. | ADZ-B07 |
| OBS-S09-02 | P | `/zones/8/vessels/1/name`, `/zones/8/vessels/1` | vessels[1].name '하순동맥 분지' 에는 영문 병기가 없다(다른 vessels 와 형식 차이). | ADZ-P16 |
| OBS-S09-03 | F | `/zones/8/botox_specific/risk`, `/zones/7/botox_specific/key_warning` | 'lip incompetence' 가 chin 에서는 '하순 외반', lips 에서는 '입술 마비 → 발음/식사 장애' 와 병기된다. | ADZ-F13 |
| OBS-S09-04 | F | `/zones/8/name_ko`, `/zones/9/name_ko` | '턱'(Chin (Mentum)) 과 '턱선'(Jawline (Mandibular border)) 은 별개 zone 이다. 'Chin' 이 다른 원장에서 어떤 표기로 쓰이는지는 이번 범위 밖. | ADZ-F14 |

## 수동 복합 표현 (직접 읽기)

탐색 관점은 수집용 꼬리표이며 확정 분류가 아니다. 구간은 값 문자열 기준 코드 포인트 `[start,end)`.

| ID | Pointer | 원문 구간 | 구간 | 탐색 관점 | 메모 |
|---|---|---|---|---|---|
| MX-S09-001 | `/zones/8/name_en` | Chin (Mentum) | [0, 13] | 영문 명칭, 괄호 병기 |  |
| MX-S09-002 | `/zones/8/vessels/0/course` | 이신경공(mental foramen)에서 출현, 하악 전면 | [0, 32] | 위치, 영문 병기 |  |
| MX-S09-003 | `/zones/8/vessels/0/danger` | 이신경공 주변 깊은 주사 시 손상 | [0, 18] | 수식(깊은), 조건(시) |  |
| MX-S09-004 | `/zones/8/vessels/1/course` | 턱끝 상방, 하순에서 연장 | [0, 14] | 위치 |  |
| MX-S09-005 | `/zones/8/vessels/1/danger` | 턱끝 상방 주사 시 주의 | [0, 13] | 조건(시), 주의 |  |
| MX-S09-006 | `/zones/8/nerves/0/significance` | 손상 시 하순/턱 감각 마비 | [14, 29] | 조건(시), 기호(/) |  |
| MX-S09-007 | `/zones/8/safe_injection_depth` | 골막상 (이부 정중앙) — 이신경공 외측 피할 것 | [0, 27] | 층, 회피 지시 |  |
| MX-S09-008 | `/zones/8/tissue_data/mental_foramen_location` | 하악 제2소구치 하방, 하악연에서 상방 약 13mm | [0, 28] | 위치, 거리, 근사(약) |  |
| MX-S09-009 | `/zones/8/tissue_data/dao_coverage` | DAO(구각하제근)의 67.7%가 이신경공을 덮고 있음 | [0, 30] | 약어, 비율(기준 불명) |  |
| MX-S09-010 | `/zones/8/tissue_data/notes` | DAO 보톡스 시 이신경 손상 주의 | [39, 58] | 조건(시), 주의 |  |
| MX-S09-011 | `/zones/8/clinical_pearls/1` | 이신경공은 제2소구치 하방 위치 — 이 부위 깊은 주사 주의 | [0, 33] | 지시 표현(이 부위), 주의 |  |
| MX-S09-012 | `/zones/8/clinical_pearls/2` | 턱끝 정중앙은 상대적으로 안전 (혈관/신경 희소) | [0, 27] | 정도(상대적으로), 기호(/) |  |
| MX-S09-013 | `/zones/8/clinical_pearls/3` | 골막상 볼루스 주사로 턱 윤곽 교정 | [0, 19] | 기법 |  |
| MX-S09-014 | `/zones/8/clinical_pearls/4` | 턱끝 외측으로 갈수록 이신경/이동맥 위험 증가 | [0, 25] | 점증(갈수록), 기호(/) |  |
| MX-S09-015 | `/zones/8/botox_specific/target_muscle` | 이근 (Mentalis) — 턱 딤플(peach pit chin) | [0, 36] | 근육명, 적응 |  |
| MX-S09-016 | `/zones/8/botox_specific/risk` | 하순 외반(lip incompetence), 이부 처짐 | [0, 30] | 부작용 |  |
| MX-S09-017 | `/zones/8/botox_specific/key_warning` | 이근 과다 마비 → 하순 처짐 + 음식물 흘림 | [0, 25] | 정도(과다), 결과(→), 기호(+) |  |
| MX-S09-018 | `/zones/8/botox_specific/dose_range` | 4-8U (정중앙 1-2포인트) | [0, 17] | 범위, 위치 |  |
| MX-S09-019 | `/zones/8/filler_specific/primary_risk` | 이신경 손상(감각 마비), 이동맥 손상 | [0, 21] | 위험 나열 |  |
| MX-S09-020 | `/zones/8/filler_specific/safe_technique` | 정중앙 골막상 볼루스 + 캐뉼러 외측 확장 | [0, 23] | 기법, 기호(+) |  |
| MX-S09-021 | `/zones/8/filler_specific/preferred_product` | 고점도 HA 또는 CaHA (윤곽 교정용) | [0, 23] | 대안(또는), 용도 |  |
| MX-S09-022 | `/zones/8/clinical_pearls/0` | DAO의 67.7%가 덮고 있음 | [22, 39] | 비율(기준 불명) |  |
| MX-S09-023 | `/zones/8/botox_specific/safe_zone` | 이부 정중앙, 이근 body 내 | [0, 17] | 위치 |  |

## 정규식 보조 후보 (기계 · 요약)

| 패턴 | 출현 |
|---|---|
| condition | 4 |
| slash | 3 |
| em_dash | 5 |
| negation_prohibition | 1 |
| number_unit | 6 |
| possibility_frequency | 1 |
| degree_emphasis | 1 |
| arrow | 1 |
| plus | 2 |
| range | 2 |

전체 출현·구간은 `expressions.json` → `regex_candidates` (section=S09).

## 전문어 분절 관찰 (Kiwi 원시 · K)

| Pointer | 낱말 | 구간 | Kiwi 토큰 | 상태 |
|---|---|---|---|---|
| `/zones/8/vessels/1/name` | 하순동맥 | [0, 4] | 하순/NNG + 동맥/NNG | K: 여러 형태소로 분절(원시 결과 보존) |
| `/zones/8/filler_specific/safe_technique` | 골막상 | [4, 7] | 골/NNG + 막상/MAG | K: 여러 형태소로 분절(원시 결과 보존) |
| `/zones/8/filler_specific/preferred_product` | 고점도 | [0, 3] | 고/MM + 점/NNG + 도/JX | K: 여러 형태소로 분절(원시 결과 보존) |

단일 형태소로 나온 출현은 표에서 생략했다(`morphology.json` → `segmentation_review` 에 전부 있음).

