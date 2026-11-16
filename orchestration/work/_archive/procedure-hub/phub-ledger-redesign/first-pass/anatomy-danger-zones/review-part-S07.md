# S07 — zones[6] cheek (볼 / Cheek (Malar/Buccal))

[← review.md](review.md) · 범위 `/zones/6/**` · 소유 노드 56 · 말단 44 · 직접 읽기 done

상위 문맥: 루트 객체 → `zones` 배열(S00 소유) → `/zones/6` (id=`cheek`, name_ko=`볼`, name_en=`Cheek (Malar/Buccal)`).

## 원문 값 (문서 순서 · 전부)

| # | JSON Pointer | 원본 컬럼명 | 배열 순번 | 자료형 | 원문 값 |
|---|---|---|---|---|---|
| 351 | `/zones/6` | `(zones 원소)` | 6 | object{12} | (컨테이너 · 키: `id`, `name_ko`, `name_en`, `danger_level`, `danger_color`, `vessels`, `nerves`, `safe_injection_depth`, `tissue_data`, `clinical_pearls`, `botox_specific`, `filler_specific`) |
| 352 | `/zones/6/id` | `id` |  | string | cheek |
| 353 | `/zones/6/name_ko` | `name_ko` |  | string | 볼 |
| 354 | `/zones/6/name_en` | `name_en` |  | string | Cheek (Malar/Buccal) |
| 355 | `/zones/6/danger_level` | `danger_level` |  | integer | `3` |
| 356 | `/zones/6/danger_color` | `danger_color` |  | string | yellow |
| 357 | `/zones/6/vessels` | `vessels` |  | array[2] | (배열 · 2개) |
| 358 | `/zones/6/vessels/0` | `(vessels 원소)` | 0 | object{5} | (컨테이너 · 키: `name`, `depth_mm`, `diameter_mm`, `course`, `danger`) |
| 359 | `/zones/6/vessels/0/name` | `name` |  | string | 안면횡동맥 (Transverse facial artery) |
| 360 | `/zones/6/vessels/0/depth_mm` | `depth_mm` |  | number | `6.0` |
| 361 | `/zones/6/vessels/0/diameter_mm` | `diameter_mm` |  | number | `1.0` |
| 362 | `/zones/6/vessels/0/course` | `course` |  | string | 관골궁 하방, 이하선관 상방 주행 |
| 363 | `/zones/6/vessels/0/danger` | `danger` |  | string | 협부 충전 시 깊은 층에서 손상 가능 |
| 364 | `/zones/6/vessels/1` | `(vessels 원소)` | 1 | object{5} | (컨테이너 · 키: `name`, `depth_mm`, `diameter_mm`, `course`, `danger`) |
| 365 | `/zones/6/vessels/1/name` | `name` |  | string | 안와하동맥 (Infraorbital artery) |
| 366 | `/zones/6/vessels/1/depth_mm` | `depth_mm` |  | number | `4.0` |
| 367 | `/zones/6/vessels/1/diameter_mm` | `diameter_mm` |  | number | `0.7` |
| 368 | `/zones/6/vessels/1/course` | `course` |  | string | 안와하공에서 출현, 협부 상방 |
| 369 | `/zones/6/vessels/1/danger` | `danger` |  | string | 상협부 깊은 주사 시 손상 |
| 370 | `/zones/6/nerves` | `nerves` |  | array[3] | (배열 · 3개) |
| 371 | `/zones/6/nerves/0` | `(nerves 원소)` | 0 | object{3} | (컨테이너 · 키: `name`, `type`, `significance`) |
| 372 | `/zones/6/nerves/0/name` | `name` |  | string | 안와하신경 (Infraorbital nerve) |
| 373 | `/zones/6/nerves/0/type` | `type` |  | string | sensory |
| 374 | `/zones/6/nerves/0/significance` | `significance` |  | string | 하안검, 코 외측, 상구순 감각 |
| 375 | `/zones/6/nerves/1` | `(nerves 원소)` | 1 | object{3} | (컨테이너 · 키: `name`, `type`, `significance`) |
| 376 | `/zones/6/nerves/1/name` | `name` |  | string | 협근신경 (Buccal branch of facial nerve) |
| 377 | `/zones/6/nerves/1/type` | `type` |  | string | motor |
| 378 | `/zones/6/nerves/1/significance` | `significance` |  | string | 협근 운동 |
| 379 | `/zones/6/nerves/2` | `(nerves 원소)` | 2 | object{3} | (컨테이너 · 키: `name`, `type`, `significance`) |
| 380 | `/zones/6/nerves/2/name` | `name` |  | string | 관골신경 (Zygomatic branch of facial nerve) |
| 381 | `/zones/6/nerves/2/type` | `type` |  | string | motor |
| 382 | `/zones/6/nerves/2/significance` | `significance` |  | string | 안륜근 하부, 관골근 운동 |
| 383 | `/zones/6/safe_injection_depth` | `safe_injection_depth` |  | string | 골막상 (관골부) 또는 피하 (협부), Sub-SMAS 층 주의 |
| 384 | `/zones/6/tissue_data` | `tissue_data` |  | object{4} | (컨테이너 · 키: `buccal_fat_pad`, `smas_depth_mm`, `sub_smas_vs_subcutaneous`, `notes`) |
| 385 | `/zones/6/tissue_data/buccal_fat_pad` | `buccal_fat_pad` |  | string | 협지방체(Buccal fat pad): SMAS 심층에 위치, 저작공간까지 연장 |
| 386 | `/zones/6/tissue_data/smas_depth_mm` | `smas_depth_mm` |  | number | `4.5` |
| 387 | `/zones/6/tissue_data/sub_smas_vs_subcutaneous` | `sub_smas_vs_subcutaneous` |  | string | Sub-SMAS: 볼륨 리프팅 / Subcutaneous: 표재성 주름 교정 |
| 388 | `/zones/6/tissue_data/notes` | `notes` |  | string | 협지방체는 관골, 측두, 협부, 익구개 공간에 걸쳐 있음 — 감염 시 파급 위험 |
| 389 | `/zones/6/clinical_pearls` | `clinical_pearls` |  | array[5] | (배열 · 5개) |
| 390 | `/zones/6/clinical_pearls/0` | `(clinical_pearls 원소)` | 0 | string | 협지방체(Buccal fat pad)는 여러 공간에 걸쳐 있어 감염 파급 경로 |
| 391 | `/zones/6/clinical_pearls/1` | `(clinical_pearls 원소)` | 1 | string | Sub-SMAS vs subcutaneous 층 구분 중요 |
| 392 | `/zones/6/clinical_pearls/2` | `(clinical_pearls 원소)` | 2 | string | 관골부(malar): 골막상 볼류메트릭 충전이 안전 |
| 393 | `/zones/6/clinical_pearls/3` | `(clinical_pearls 원소)` | 3 | string | 협부 하방은 상대적으로 안전하나 이하선관(Stensen's duct) 주의 |
| 394 | `/zones/6/clinical_pearls/4` | `(clinical_pearls 원소)` | 4 | string | 필러 이동(migration) 주의 — 중력 방향으로 처질 수 있음 |
| 395 | `/zones/6/botox_specific` | `botox_specific` |  | object{5} | (컨테이너 · 키: `target_muscle`, `risk`, `safe_zone`, `key_warning`, `dose_range`) |
| 396 | `/zones/6/botox_specific/target_muscle` | `target_muscle` |  | string | 교근 (Masseter) — 사각턱, 광대근 (Zygomaticus) — gummy smile |
| 397 | `/zones/6/botox_specific/risk` | `risk` |  | string | 교근 과위축 → 안면 함몰, 씹는 힘 약화 |
| 398 | `/zones/6/botox_specific/safe_zone` | `safe_zone` |  | string | 교근 하방 1/3, 근육 body 내 |
| 399 | `/zones/6/botox_specific/key_warning` | `key_warning` |  | string | 교근 상방·전방·표재 주사 시 독소가 관골근(zygomaticus major)·소근으로 확산 → 미소 비대칭(문헌상 발생률 약 2.4%, 대개 4주 내 자연 회복). 관골뼈 위·교근 전연 인접 주입을 피하고 하방·후방 body에 주입 |
| 400 | `/zones/6/botox_specific/dose_range` | `dose_range` |  | string | 교근 25-50U/측, 광대근 2-4U/측 |
| 401 | `/zones/6/filler_specific` | `filler_specific` |  | object{5} | (컨테이너 · 키: `risk_level`, `primary_risk`, `safe_technique`, `max_per_point_ml`, `preferred_product`) |
| 402 | `/zones/6/filler_specific/risk_level` | `risk_level` |  | integer | `3` |
| 403 | `/zones/6/filler_specific/primary_risk` | `primary_risk` |  | string | 필러 이동, 부종, 안면횡동맥 손상 |
| 404 | `/zones/6/filler_specific/safe_technique` | `safe_technique` |  | string | 관골부: 골막상 볼루스. 협부: 피하 캐뉼러 fan technique |
| 405 | `/zones/6/filler_specific/max_per_point_ml` | `max_per_point_ml` |  | number | `0.3` |
| 406 | `/zones/6/filler_specific/preferred_product` | `preferred_product` |  | string | 고점도 HA (관골부), 중점도 HA (협부) |

## 잠정 관찰 (원문 칸과 분리)

| # | 상태 | 근거 Pointer | 관찰 | issues.md |
|---|---|---|---|---|
| OBS-S07-01 | P | `/zones/6/name_en` | 'Cheek (Malar/Buccal)' — 괄호 안 '/' 병기. README 의 괄호·'/' 규칙을 부위 명칭에 기계 적용하지 않는다. | ADZ-P10 |
| OBS-S07-02 | F | `/zones/6/botox_specific/target_muscle`, `/zones/6/botox_specific/key_warning` | '광대근 (Zygomaticus)', '관골근(zygomaticus major)·소근' 이 한 zone 안에서 다른 표기로 나온다. | ADZ-F13 |
| OBS-S07-03 | F | `/zones/6/botox_specific`, `/zones/9/botox_specific` | 볼 zone 의 botox 대상이 교근(사각턱)이며 같은 용량 표현 '교근 25-50U/측' 이 턱선 zone 에도 있다. zone 간 중복·소속은 후속. | ADZ-F14 |
| OBS-S07-04 | P | `/zones/6/tissue_data/sub_smas_vs_subcutaneous` | 'A: 설명 / B: 설명' 형식으로 '/' 가 두 쌍을 나누는 구분자로 쓰였다. | ADZ-P10 |
| OBS-S07-05 | P | `/zones/6/botox_specific/key_warning` | 발생률(약 2.4%)·경과(대개 4주 내 자연 회복)·회피 지시가 한 값에 있다. '대개' 는 빈도 수식이다. |  |
| OBS-S07-06 | F | `/zones/6/clinical_pearls/2`, `/zones/6/filler_specific/safe_technique` | '볼류메트릭' 과 '볼루스' 는 다른 낱말이며 표기 대응은 후속. | ADZ-F13 |

## 수동 복합 표현 (직접 읽기)

탐색 관점은 수집용 꼬리표이며 확정 분류가 아니다. 구간은 값 문자열 기준 코드 포인트 `[start,end)`.

| ID | Pointer | 원문 구간 | 구간 | 탐색 관점 | 메모 |
|---|---|---|---|---|---|
| MX-S07-001 | `/zones/6/name_en` | Cheek (Malar/Buccal) | [0, 20] | 영문 명칭, 기호(/) |  |
| MX-S07-002 | `/zones/6/vessels/0/course` | 관골궁 하방, 이하선관 상방 주행 | [0, 18] | 위치 |  |
| MX-S07-003 | `/zones/6/vessels/0/danger` | 협부 충전 시 깊은 층에서 손상 가능 | [0, 20] | 조건(시), 가능성 |  |
| MX-S07-004 | `/zones/6/vessels/1/course` | 안와하공에서 출현, 협부 상방 | [0, 16] | 위치 |  |
| MX-S07-005 | `/zones/6/vessels/1/danger` | 상협부 깊은 주사 시 손상 | [0, 14] | 조건(시) |  |
| MX-S07-006 | `/zones/6/nerves/2/name` | 관골신경 (Zygomatic branch of facial nerve) | [0, 39] | 신경명, 영문 병기 |  |
| MX-S07-007 | `/zones/6/nerves/2/significance` | 안륜근 하부, 관골근 운동 | [0, 14] | 기능 |  |
| MX-S07-008 | `/zones/6/safe_injection_depth` | 골막상 (관골부) 또는 피하 (협부), Sub-SMAS 층 주의 | [0, 35] | 층, 대안(또는), 위치 한정, 주의 |  |
| MX-S07-009 | `/zones/6/tissue_data/buccal_fat_pad` | 협지방체(Buccal fat pad): SMAS 심층에 위치, 저작공간까지 연장 | [0, 44] | 위치, 범위(까지) |  |
| MX-S07-010 | `/zones/6/tissue_data/sub_smas_vs_subcutaneous` | Sub-SMAS: 볼륨 리프팅 / Subcutaneous: 표재성 주름 교정 | [0, 42] | 대비 쌍, 구분자(/) |  |
| MX-S07-011 | `/zones/6/tissue_data/notes` | 협지방체는 관골, 측두, 협부, 익구개 공간에 걸쳐 있음 | [0, 31] | 범위 |  |
| MX-S07-012 | `/zones/6/tissue_data/notes` | 감염 시 파급 위험 | [34, 44] | 조건(시) |  |
| MX-S07-013 | `/zones/6/clinical_pearls/0` | 협지방체(Buccal fat pad)는 여러 공간에 걸쳐 있어 감염 파급 경로 | [0, 43] | 이유(어), 경로 |  |
| MX-S07-014 | `/zones/6/clinical_pearls/1` | Sub-SMAS vs subcutaneous 층 구분 중요 | [0, 32] | 대비(vs) |  |
| MX-S07-015 | `/zones/6/clinical_pearls/2` | 관골부(malar): 골막상 볼류메트릭 충전이 안전 | [0, 28] | 적용 대상, 층 |  |
| MX-S07-016 | `/zones/6/clinical_pearls/3` | 협부 하방은 상대적으로 안전하나 이하선관(Stensen's duct) 주의 | [0, 41] | 정도(상대적으로), 대조(나), 주의 |  |
| MX-S07-017 | `/zones/6/clinical_pearls/4` | 필러 이동(migration) 주의 | [0, 19] | 주의 |  |
| MX-S07-018 | `/zones/6/clinical_pearls/4` | 중력 방향으로 처질 수 있음 | [22, 37] | 가능성(수 있음) |  |
| MX-S07-019 | `/zones/6/botox_specific/target_muscle` | 교근 (Masseter) — 사각턱, 광대근 (Zygomaticus) — gummy smile | [0, 52] | 근육명, 적응 |  |
| MX-S07-020 | `/zones/6/botox_specific/risk` | 교근 과위축 → 안면 함몰, 씹는 힘 약화 | [0, 23] | 정도(과), 결과(→) |  |
| MX-S07-021 | `/zones/6/botox_specific/safe_zone` | 교근 하방 1/3, 근육 body 내 | [0, 20] | 분수(1/3), 위치 |  |
| MX-S07-022 | `/zones/6/botox_specific/key_warning` | 교근 상방·전방·표재 주사 시 독소가 관골근(zygomaticus major)·소근으로 확산 → 미소 비대칭 | [0, 60] | 조건(시), 결과(→) |  |
| MX-S07-023 | `/zones/6/botox_specific/key_warning` | 문헌상 발생률 약 2.4%, 대개 4주 내 자연 회복 | [61, 90] | 비율, 근사(약), 빈도(대개), 시간(4주 내) |  |
| MX-S07-024 | `/zones/6/botox_specific/key_warning` | 관골뼈 위·교근 전연 인접 주입을 피하고 하방·후방 body에 주입 | [93, 130] | 회피 지시, 위치 |  |
| MX-S07-025 | `/zones/6/botox_specific/dose_range` | 교근 25-50U/측 | [0, 11] | 근육+범위, 단위당 |  |
| MX-S07-026 | `/zones/6/botox_specific/dose_range` | 광대근 2-4U/측 | [13, 23] | 근육+범위, 단위당 |  |
| MX-S07-027 | `/zones/6/filler_specific/primary_risk` | 필러 이동, 부종, 안면횡동맥 손상 | [0, 19] | 위험 나열 |  |
| MX-S07-028 | `/zones/6/filler_specific/safe_technique` | 관골부: 골막상 볼루스 | [0, 12] | 적용 대상, 기법 |  |
| MX-S07-029 | `/zones/6/filler_specific/safe_technique` | 협부: 피하 캐뉼러 fan technique | [14, 38] | 적용 대상, 기법 |  |
| MX-S07-030 | `/zones/6/filler_specific/preferred_product` | 고점도 HA (관골부), 중점도 HA (협부) | [0, 25] | 수식, 위치 한정 |  |

## 정규식 보조 후보 (기계 · 요약)

| 패턴 | 출현 |
|---|---|
| slash | 5 |
| comparator | 3 |
| possibility_frequency | 4 |
| condition | 4 |
| em_dash | 4 |
| arrow | 2 |
| number_unit | 4 |
| negation_prohibition | 1 |
| time_order | 1 |
| middle_dot | 5 |
| range | 2 |

전체 출현·구간은 `expressions.json` → `regex_candidates` (section=S07).

## 전문어 분절 관찰 (Kiwi 원시 · K)

| Pointer | 낱말 | 구간 | Kiwi 토큰 | 상태 |
|---|---|---|---|---|
| `/zones/6/vessels/0/course` | 관골궁 | [0, 3] | 관골/NNP + 궁/NNG | K: 여러 형태소로 분절(원시 결과 보존) |
| `/zones/6/vessels/1/course` | 안와하공 | [0, 4] | 안와/NNG + 하/NNG + 공/NNG | K: 여러 형태소로 분절(원시 결과 보존) |
| `/zones/6/tissue_data/sub_smas_vs_subcutaneous` | 표재성 | [33, 36] | 표/NNG + 재/NNG + 성/XSN | K: 여러 형태소로 분절(원시 결과 보존) |
| `/zones/6/botox_specific/target_muscle` | 교근 | [0, 2] | 교/NNG + 근/NNG | K: 여러 형태소로 분절(원시 결과 보존) |
| `/zones/6/botox_specific/risk` | 교근 | [0, 2] | 교/NNG + 근/NNG | K: 여러 형태소로 분절(원시 결과 보존) |
| `/zones/6/botox_specific/safe_zone` | 교근 | [0, 2] | 교/NNG + 근/NNG | K: 여러 형태소로 분절(원시 결과 보존) |
| `/zones/6/botox_specific/key_warning` | 교근 | [0, 2] | 교/NNG + 근/NNG | K: 여러 형태소로 분절(원시 결과 보존) |
| `/zones/6/botox_specific/key_warning` | 교근 | [99, 101] | 교/NNG + 근/NNG | K: 여러 형태소로 분절(원시 결과 보존) |
| `/zones/6/botox_specific/dose_range` | 교근 | [0, 2] | 교/NNG + 근/NNG | K: 여러 형태소로 분절(원시 결과 보존) |
| `/zones/6/filler_specific/primary_risk` | 안면횡동맥 | [11, 16] | 안면/NNG + 횡/NNG + 동맥/NNG | K: 여러 형태소로 분절(원시 결과 보존) |
| `/zones/6/filler_specific/preferred_product` | 고점도 | [0, 3] | 고/MM + 점/NNG + 도/JX | K: 여러 형태소로 분절(원시 결과 보존) |

단일 형태소로 나온 출현은 표에서 생략했다(`morphology.json` → `segmentation_review` 에 전부 있음).

