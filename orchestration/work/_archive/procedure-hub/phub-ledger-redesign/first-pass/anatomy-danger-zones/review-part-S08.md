# S08 — zones[7] lips (입술 / Lips)

[← review.md](review.md) · 범위 `/zones/7/**` · 소유 노드 58 · 말단 44 · 직접 읽기 done

상위 문맥: 루트 객체 → `zones` 배열(S00 소유) → `/zones/7` (id=`lips`, name_ko=`입술`, name_en=`Lips`).

## 원문 값 (문서 순서 · 전부)

| # | JSON Pointer | 원본 컬럼명 | 배열 순번 | 자료형 | 원문 값 |
|---|---|---|---|---|---|
| 407 | `/zones/7` | `(zones 원소)` | 7 | object{12} | (컨테이너 · 키: `id`, `name_ko`, `name_en`, `danger_level`, `danger_color`, `vessels`, `nerves`, `safe_injection_depth`, `tissue_data`, `clinical_pearls`, `botox_specific`, `filler_specific`) |
| 408 | `/zones/7/id` | `id` |  | string | lips |
| 409 | `/zones/7/name_ko` | `name_ko` |  | string | 입술 |
| 410 | `/zones/7/name_en` | `name_en` |  | string | Lips |
| 411 | `/zones/7/danger_level` | `danger_level` |  | integer | `3` |
| 412 | `/zones/7/danger_color` | `danger_color` |  | string | yellow |
| 413 | `/zones/7/vessels` | `vessels` |  | array[2] | (배열 · 2개) |
| 414 | `/zones/7/vessels/0` | `(vessels 원소)` | 0 | object{5} | (컨테이너 · 키: `name`, `diameter_mm`, `course`, `danger`, `depth_range_mm`) |
| 415 | `/zones/7/vessels/0/name` | `name` |  | string | 상순동맥 (Superior labial artery) |
| 416 | `/zones/7/vessels/0/diameter_mm` | `diameter_mm` |  | number | `1.0` |
| 417 | `/zones/7/vessels/0/course` | `course` |  | string | 대부분 점막하층(약 58.5%)에서 점막면 기준 평균 약 4.5-5.6mm 깊이로 주행하며 가장 얕은 경우 약 3.2mm; 구각 쪽에서 더 깊게 후방 주행 |
| 418 | `/zones/7/vessels/0/danger` | `danger` |  | string | 혈관 천자 → 출혈, 혈종, 드물게 조직 괴사 |
| 419 | `/zones/7/vessels/0/depth_range_mm` | `depth_range_mm` |  | array[2] | (배열 · 2개) |
| 420 | `/zones/7/vessels/0/depth_range_mm/0` | `(depth_range_mm 원소)` | 0 | number | `3.2` |
| 421 | `/zones/7/vessels/0/depth_range_mm/1` | `(depth_range_mm 원소)` | 1 | number | `5.6` |
| 422 | `/zones/7/vessels/1` | `(vessels 원소)` | 1 | object{5} | (컨테이너 · 키: `name`, `diameter_mm`, `course`, `danger`, `depth_range_mm`) |
| 423 | `/zones/7/vessels/1/name` | `name` |  | string | 하순동맥 (Inferior labial artery) |
| 424 | `/zones/7/vessels/1/diameter_mm` | `diameter_mm` |  | number | `0.8` |
| 425 | `/zones/7/vessels/1/course` | `course` |  | string | 하순 내 주행, 상순동맥과 유사 경로 |
| 426 | `/zones/7/vessels/1/danger` | `danger` |  | string | 혈관 천자 → 출혈/혈종 |
| 427 | `/zones/7/vessels/1/depth_range_mm` | `depth_range_mm` |  | array[2] | (배열 · 2개) |
| 428 | `/zones/7/vessels/1/depth_range_mm/0` | `(depth_range_mm 원소)` | 0 | number | `3.0` |
| 429 | `/zones/7/vessels/1/depth_range_mm/1` | `(depth_range_mm 원소)` | 1 | number | `6.0` |
| 430 | `/zones/7/nerves` | `nerves` |  | array[2] | (배열 · 2개) |
| 431 | `/zones/7/nerves/0` | `(nerves 원소)` | 0 | object{3} | (컨테이너 · 키: `name`, `type`, `significance`) |
| 432 | `/zones/7/nerves/0/name` | `name` |  | string | 안와하신경 순측분지 (Labial branch of infraorbital nerve) |
| 433 | `/zones/7/nerves/0/type` | `type` |  | string | sensory |
| 434 | `/zones/7/nerves/0/significance` | `significance` |  | string | 상순 감각 |
| 435 | `/zones/7/nerves/1` | `(nerves 원소)` | 1 | object{3} | (컨테이너 · 키: `name`, `type`, `significance`) |
| 436 | `/zones/7/nerves/1/name` | `name` |  | string | 이신경 순측분지 (Labial branch of mental nerve) |
| 437 | `/zones/7/nerves/1/type` | `type` |  | string | sensory |
| 438 | `/zones/7/nerves/1/significance` | `significance` |  | string | 하순 감각 |
| 439 | `/zones/7/safe_injection_depth` | `safe_injection_depth` |  | string | 점막-피부 경계(vermillion border) 진피 내 또는 점막하 |
| 440 | `/zones/7/tissue_data` | `tissue_data` |  | object{3} | (컨테이너 · 키: `labial_artery_depth_range_mm`, `superior_labial_artery_submucosal_percent`, `notes`) |
| 441 | `/zones/7/tissue_data/labial_artery_depth_range_mm` | `labial_artery_depth_range_mm` |  | array[2] | (배열 · 2개) |
| 442 | `/zones/7/tissue_data/labial_artery_depth_range_mm/0` | `(labial_artery_depth_range_mm 원소)` | 0 | number | `3.0` |
| 443 | `/zones/7/tissue_data/labial_artery_depth_range_mm/1` | `(labial_artery_depth_range_mm 원소)` | 1 | number | `6.0` |
| 444 | `/zones/7/tissue_data/superior_labial_artery_submucosal_percent` | `superior_labial_artery_submucosal_percent` |  | number | `58.5` |
| 445 | `/zones/7/tissue_data/notes` | `notes` |  | string | 상순동맥은 대부분 점막하층에 위치(약 58.5%)하고 점막면에서 평균 약 4.5-5.6mm(가장 얕은 경우 약 3.2mm) 깊이로 주행하며 구각(구각에서 0.5cm 이내 유입) 쪽에서 더 깊다. 후방 주행 덕분에 vermillion border의 표재성 진피 내 소량 주입이 가장 안전하며, 구각부 심부·정중/중간 vermillion 점막하 주입은 동맥 손상 위험이 높아 금지 |
| 446 | `/zones/7/clinical_pearls` | `clinical_pearls` |  | array[6] | (배열 · 6개) |
| 447 | `/zones/7/clinical_pearls/0` | `(clinical_pearls 원소)` | 0 | string | 상순동맥은 대부분 점막하층(약 58.5%)에서 점막면 기준 평균 약 4.5-5.6mm 깊이로 주행하며 가장 얕은 경우 약 3.2mm |
| 448 | `/zones/7/clinical_pearls/1` | `(clinical_pearls 원소)` | 1 | string | 상순동맥은 구각에서 0.5cm 이내로 유입되고 구각 쪽에서 더 깊게 후방 주행 |
| 449 | `/zones/7/clinical_pearls/2` | `(clinical_pearls 원소)` | 2 | string | 구각(oral commissure) 부근 주사 시 혈관 천자 위험 높음 |
| 450 | `/zones/7/clinical_pearls/3` | `(clinical_pearls 원소)` | 3 | string | 진피 내(intradermal) 소량 주사가 가장 안전 |
| 451 | `/zones/7/clinical_pearls/4` | `(clinical_pearls 원소)` | 4 | string | 과충전 시 sausage lip → 입술 기능 장애 (발음, 식사) |
| 452 | `/zones/7/clinical_pearls/5` | `(clinical_pearls 원소)` | 5 | string | 이전 영구 필러(실리콘 등) 존재 시 HA 필러 금기 |
| 453 | `/zones/7/botox_specific` | `botox_specific` |  | object{5} | (컨테이너 · 키: `target_muscle`, `risk`, `safe_zone`, `key_warning`, `dose_range`) |
| 454 | `/zones/7/botox_specific/target_muscle` | `target_muscle` |  | string | 구륜근 (Orbicularis oris) — lip flip, 입가 주름 |
| 455 | `/zones/7/botox_specific/risk` | `risk` |  | string | 구강 기능 장애 (빨대 사용, 발음, 식사 불편) |
| 456 | `/zones/7/botox_specific/safe_zone` | `safe_zone` |  | string | 상순 vermillion border, 구각에서 멀리 |
| 457 | `/zones/7/botox_specific/key_warning` | `key_warning` |  | string | 과다 주사 → 입술 마비 → 발음/식사 장애 (lip incompetence) |
| 458 | `/zones/7/botox_specific/dose_range` | `dose_range` |  | string | Lip flip: 4-6U (상순), 구각 거상: 2-4U/측 |
| 459 | `/zones/7/filler_specific` | `filler_specific` |  | object{5} | (컨테이너 · 키: `risk_level`, `primary_risk`, `safe_technique`, `max_per_point_ml`, `preferred_product`) |
| 460 | `/zones/7/filler_specific/risk_level` | `risk_level` |  | integer | `3` |
| 461 | `/zones/7/filler_specific/primary_risk` | `primary_risk` |  | string | 혈종, 부종, 드물게 조직 괴사 (상순동맥 폐색 시) |
| 462 | `/zones/7/filler_specific/safe_technique` | `safe_technique` |  | string | Vermillion border 진피 내, 소량 연속 주입, 캐뉼러 또는 미세 니들 |
| 463 | `/zones/7/filler_specific/max_per_point_ml` | `max_per_point_ml` |  | number | `0.1` |
| 464 | `/zones/7/filler_specific/preferred_product` | `preferred_product` |  | string | 저-중점도 HA (연성, 자연스러운 촉감) |

## 잠정 관찰 (원문 칸과 분리)

| # | 상태 | 근거 Pointer | 관찰 | issues.md |
|---|---|---|---|---|
| OBS-S08-01 | P | `/zones/7/vessels/0`, `/zones/7/vessels/1` | lips 의 두 vessels 에는 depth_mm 이 없고 depth_range_mm 만 있다(다른 zone 과 구조 차이). | ADZ-P16 |
| OBS-S08-02 | B | `/zones/7/tissue_data/labial_artery_depth_range_mm`, `/zones/7/vessels/0/depth_range_mm`, `/zones/7/vessels/1/depth_range_mm` | tissue_data.labial_artery_depth_range_mm [3.0,6.0] 은 이름상 상·하순 구분이 없고 값은 vessels[1](하순동맥)과 같으며 vessels[0](상순동맥) [3.2,5.6] 과 다르다. 어느 혈관 기준인지 원문에 없다. | ADZ-B05 |
| OBS-S08-03 | I | `/zones/7/safe_injection_depth`, `/zones/7/tissue_data/notes` | safe_injection_depth 는 '진피 내 또는 점막하' 를 안전 깊이로 적었고, notes 는 '구각부 심부·정중/중간 vermillion 점막하 주입은 ... 금지' 라고 한다. 적용 범위가 다른지 원문만으로 알 수 없다. | ADZ-I03 |
| OBS-S08-04 | P | `/zones/7/vessels/0/course` | '대부분 ... (약 58.5%)', '평균 약 4.5-5.6mm', '가장 얕은 경우 약 3.2mm' 처럼 빈도·평균·극값 수식이 겹쳐 있다. depth_range_mm [3.2,5.6] 의 두 끝값이 서로 다른 성격(최솟값/평균 범위 상단)에서 왔다. |  |
| OBS-S08-05 | P | `/zones/7/safe_injection_depth`, `/zones/7/filler_specific/safe_technique` | 'vermillion' 철자를 원문 그대로 보존한다(교정하지 않음). 'Vermillion' 대문자 출현도 있다. |  |
| OBS-S08-06 | P | `/zones/7/filler_specific/preferred_product` | '저-중점도' 의 '-' 는 점도 단계 범위다. | ADZ-P11 |

## 수동 복합 표현 (직접 읽기)

탐색 관점은 수집용 꼬리표이며 확정 분류가 아니다. 구간은 값 문자열 기준 코드 포인트 `[start,end)`.

| ID | Pointer | 원문 구간 | 구간 | 탐색 관점 | 메모 |
|---|---|---|---|---|---|
| MX-S08-001 | `/zones/7/vessels/0/course` | 대부분 점막하층(약 58.5%)에서 점막면 기준 평균 약 4.5-5.6mm 깊이로 주행하며 가장 얕은 경우 약 3.2mm | [0, 67] | 빈도(대부분), 비율, 기준면, 평균, 범위, 극값(가장 얕은 경우) |  |
| MX-S08-002 | `/zones/7/vessels/0/course` | 구각 쪽에서 더 깊게 후방 주행 | [69, 86] | 비교(더) |  |
| MX-S08-003 | `/zones/7/vessels/0/danger` | 혈관 천자 → 출혈, 혈종, 드물게 조직 괴사 | [0, 25] | 결과(→), 빈도(드물게) |  |
| MX-S08-004 | `/zones/7/vessels/1/course` | 하순 내 주행, 상순동맥과 유사 경로 | [0, 20] | 참조(유사) |  |
| MX-S08-005 | `/zones/7/vessels/1/danger` | 혈관 천자 → 출혈/혈종 | [0, 13] | 결과(→), 기호(/) |  |
| MX-S08-006 | `/zones/7/nerves/0/name` | 안와하신경 순측분지 (Labial branch of infraorbital nerve) | [0, 48] | 신경명, 영문 병기 |  |
| MX-S08-007 | `/zones/7/nerves/1/name` | 이신경 순측분지 (Labial branch of mental nerve) | [0, 40] | 신경명, 영문 병기 |  |
| MX-S08-008 | `/zones/7/safe_injection_depth` | 점막-피부 경계(vermillion border) 진피 내 또는 점막하 | [0, 39] | 층, 대안(또는), 연결 하이픈 |  |
| MX-S08-009 | `/zones/7/tissue_data/notes` | 상순동맥은 대부분 점막하층에 위치(약 58.5%)하고 | [0, 29] | 빈도, 비율 |  |
| MX-S08-010 | `/zones/7/tissue_data/notes` | 점막면에서 평균 약 4.5-5.6mm(가장 얕은 경우 약 3.2mm) 깊이로 주행하며 | [30, 77] | 평균, 범위, 극값 |  |
| MX-S08-011 | `/zones/7/tissue_data/notes` | 구각(구각에서 0.5cm 이내 유입) 쪽에서 더 깊다 | [78, 107] | 거리 상한(이내), 비교 |  |
| MX-S08-012 | `/zones/7/tissue_data/notes` | 후방 주행 덕분에 vermillion border의 표재성 진피 내 소량 주입이 가장 안전하며 | [109, 161] | 이유(덕분에), 최상급 |  |
| MX-S08-013 | `/zones/7/tissue_data/notes` | 구각부 심부·정중/중간 vermillion 점막하 주입은 동맥 손상 위험이 높아 금지 | [163, 210] | 적용 범위, 기호(/), 이유, 금지 |  |
| MX-S08-014 | `/zones/7/clinical_pearls/1` | 상순동맥은 구각에서 0.5cm 이내로 유입되고 구각 쪽에서 더 깊게 후방 주행 | [0, 43] | 거리 상한, 비교 |  |
| MX-S08-015 | `/zones/7/clinical_pearls/2` | 구각(oral commissure) 부근 주사 시 혈관 천자 위험 높음 | [0, 39] | 조건(시), 위험 |  |
| MX-S08-016 | `/zones/7/clinical_pearls/3` | 진피 내(intradermal) 소량 주사가 가장 안전 | [0, 30] | 최상급 |  |
| MX-S08-017 | `/zones/7/clinical_pearls/4` | 과충전 시 sausage lip → 입술 기능 장애 (발음, 식사) | [0, 37] | 조건(시), 결과(→) |  |
| MX-S08-018 | `/zones/7/clinical_pearls/5` | 이전 영구 필러(실리콘 등) 존재 시 HA 필러 금기 | [0, 29] | 시간(이전), 조건(시), 금기 |  |
| MX-S08-019 | `/zones/7/botox_specific/target_muscle` | 구륜근 (Orbicularis oris) — lip flip, 입가 주름 | [0, 40] | 근육명, 적응 |  |
| MX-S08-020 | `/zones/7/botox_specific/risk` | 구강 기능 장애 (빨대 사용, 발음, 식사 불편) | [0, 27] | 부작용, 예시 나열 |  |
| MX-S08-021 | `/zones/7/botox_specific/safe_zone` | 상순 vermillion border, 구각에서 멀리 | [0, 29] | 위치, 거리(멀리) |  |
| MX-S08-022 | `/zones/7/botox_specific/key_warning` | 과다 주사 → 입술 마비 → 발음/식사 장애 (lip incompetence) | [0, 43] | 연쇄(→), 기호(/) |  |
| MX-S08-023 | `/zones/7/botox_specific/dose_range` | Lip flip: 4-6U (상순) | [0, 19] | 적응+범위 |  |
| MX-S08-024 | `/zones/7/botox_specific/dose_range` | 구각 거상: 2-4U/측 | [21, 34] | 적응+범위, 단위당 |  |
| MX-S08-025 | `/zones/7/filler_specific/primary_risk` | 혈종, 부종, 드물게 조직 괴사 (상순동맥 폐색 시) | [0, 29] | 빈도(드물게), 조건(시) |  |
| MX-S08-026 | `/zones/7/filler_specific/safe_technique` | Vermillion border 진피 내, 소량 연속 주입, 캐뉼러 또는 미세 니들 | [0, 46] | 층, 기법, 대안(또는) |  |
| MX-S08-027 | `/zones/7/filler_specific/preferred_product` | 저-중점도 HA (연성, 자연스러운 촉감) | [0, 23] | 범위(저-중), 수식 |  |
| MX-S08-028 | `/zones/7/clinical_pearls/0` | 대부분 점막하층(약 58.5%)에서 점막면 기준 평균 약 4.5-5.6mm 깊이로 주행하며 가장 얕은 경우 약 3.2mm | [6, 73] | 빈도(대부분), 비율, 평균, 범위, 극값 | vessels/0/course 앞부분과 같은 문구 |

## 정규식 보조 후보 (기계 · 요약)

| 패턴 | 출현 |
|---|---|
| range | 5 |
| number_unit | 13 |
| possibility_frequency | 5 |
| condition | 7 |
| degree_emphasis | 6 |
| arrow | 5 |
| slash | 4 |
| comparator | 2 |
| negation_prohibition | 2 |
| middle_dot | 1 |
| time_order | 1 |
| em_dash | 1 |

전체 출현·구간은 `expressions.json` → `regex_candidates` (section=S08).

## 전문어 분절 관찰 (Kiwi 원시 · K)

| Pointer | 낱말 | 구간 | Kiwi 토큰 | 상태 |
|---|---|---|---|---|
| `/zones/7/vessels/0/course` | 점막하층 | [4, 8] | 점막/NNG + 하층/NNG | K: 여러 형태소로 분절(원시 결과 보존) |
| `/zones/7/vessels/1/name` | 하순동맥 | [0, 4] | 하순/NNG + 동맥/NNG | K: 여러 형태소로 분절(원시 결과 보존) |
| `/zones/7/tissue_data/notes` | 상순동맥 | [0, 4] | 상순/NNG + 동맥/NNG | K: 여러 형태소로 분절(원시 결과 보존) |
| `/zones/7/tissue_data/notes` | 표재성 | [138, 141] | 표재/NNG + 성/XSN | K: 여러 형태소로 분절(원시 결과 보존) |
| `/zones/7/tissue_data/notes` | 점막하층 | [10, 14] | 점막/NNG + 하층/NNG | K: 여러 형태소로 분절(원시 결과 보존) |
| `/zones/7/clinical_pearls/0` | 상순동맥 | [0, 4] | 상순/NNG + 동맥/NNG | K: 여러 형태소로 분절(원시 결과 보존) |
| `/zones/7/clinical_pearls/0` | 점막하층 | [10, 14] | 점막/NNG + 하층/NNG | K: 여러 형태소로 분절(원시 결과 보존) |
| `/zones/7/filler_specific/primary_risk` | 상순동맥 | [19, 23] | 상순/NNG + 동맥/NNG | K: 여러 형태소로 분절(원시 결과 보존) |
| `/zones/7/filler_specific/preferred_product` | 중점도 | [2, 5] | 중점/NNG + 도/JX | K: 여러 형태소로 분절(원시 결과 보존) |

단일 형태소로 나온 출현은 표에서 생략했다(`morphology.json` → `segmentation_review` 에 전부 있음).

