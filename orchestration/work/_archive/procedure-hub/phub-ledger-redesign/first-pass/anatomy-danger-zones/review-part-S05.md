# S05 — zones[4] nose (코 / Nose)

[← review.md](review.md) · 범위 `/zones/4/**` · 소유 노드 61 · 말단 49 · 직접 읽기 done

상위 문맥: 루트 객체 → `zones` 배열(S00 소유) → `/zones/4` (id=`nose`, name_ko=`코`, name_en=`Nose`).

## 원문 값 (문서 순서 · 전부)

| # | JSON Pointer | 원본 컬럼명 | 배열 순번 | 자료형 | 원문 값 |
|---|---|---|---|---|---|
| 236 | `/zones/4` | `(zones 원소)` | 4 | object{12} | (컨테이너 · 키: `id`, `name_ko`, `name_en`, `danger_level`, `danger_color`, `vessels`, `nerves`, `safe_injection_depth`, `tissue_data`, `clinical_pearls`, `botox_specific`, `filler_specific`) |
| 237 | `/zones/4/id` | `id` |  | string | nose |
| 238 | `/zones/4/name_ko` | `name_ko` |  | string | 코 |
| 239 | `/zones/4/name_en` | `name_en` |  | string | Nose |
| 240 | `/zones/4/danger_level` | `danger_level` |  | integer | `5` |
| 241 | `/zones/4/danger_color` | `danger_color` |  | string | red |
| 242 | `/zones/4/vessels` | `vessels` |  | array[3] | (배열 · 3개) |
| 243 | `/zones/4/vessels/0` | `(vessels 원소)` | 0 | object{5} | (컨테이너 · 키: `name`, `depth_mm`, `diameter_mm`, `course`, `danger`) |
| 244 | `/zones/4/vessels/0/name` | `name` |  | string | 배비동맥 (Dorsal nasal artery) |
| 245 | `/zones/4/vessels/0/depth_mm` | `depth_mm` |  | number | `2.0` |
| 246 | `/zones/4/vessels/0/diameter_mm` | `diameter_mm` |  | number | `0.6` |
| 247 | `/zones/4/vessels/0/course` | `course` |  | string | 코등(dorsum)을 따라 하행, 안동맥의 직접 분지 |
| 248 | `/zones/4/vessels/0/danger` | `danger` |  | string | 0.0368mL로 안동맥 폐색 → 실명 (최소 용량) |
| 249 | `/zones/4/vessels/1` | `(vessels 원소)` | 1 | object{5} | (컨테이너 · 키: `name`, `depth_mm`, `diameter_mm`, `course`, `danger`) |
| 250 | `/zones/4/vessels/1/name` | `name` |  | string | 외비동맥 (External nasal artery / Lateral nasal artery) |
| 251 | `/zones/4/vessels/1/depth_mm` | `depth_mm` |  | number | `1.5` |
| 252 | `/zones/4/vessels/1/diameter_mm` | `diameter_mm` |  | number | `0.5` |
| 253 | `/zones/4/vessels/1/course` | `course` |  | string | 비익(ala) 외측, 안면동맥 분지 |
| 254 | `/zones/4/vessels/1/danger` | `danger` |  | string | 비익 괴사 위험 |
| 255 | `/zones/4/vessels/2` | `(vessels 원소)` | 2 | object{5} | (컨테이너 · 키: `name`, `depth_mm`, `diameter_mm`, `course`, `danger`) |
| 256 | `/zones/4/vessels/2/name` | `name` |  | string | 주상동맥 (Columellar artery) |
| 257 | `/zones/4/vessels/2/depth_mm` | `depth_mm` |  | number | `2.0` |
| 258 | `/zones/4/vessels/2/diameter_mm` | `diameter_mm` |  | number | `0.4` |
| 259 | `/zones/4/vessels/2/course` | `course` |  | string | 비주(columella) 내 주행 |
| 260 | `/zones/4/vessels/2/danger` | `danger` |  | string | 비첨부 주사 시 손상 위험 |
| 261 | `/zones/4/nerves` | `nerves` |  | array[2] | (배열 · 2개) |
| 262 | `/zones/4/nerves/0` | `(nerves 원소)` | 0 | object{3} | (컨테이너 · 키: `name`, `type`, `significance`) |
| 263 | `/zones/4/nerves/0/name` | `name` |  | string | 외비신경 (External nasal nerve) |
| 264 | `/zones/4/nerves/0/type` | `type` |  | string | sensory |
| 265 | `/zones/4/nerves/0/significance` | `significance` |  | string | 코끝, 코등 하부 감각 |
| 266 | `/zones/4/nerves/1` | `(nerves 원소)` | 1 | object{3} | (컨테이너 · 키: `name`, `type`, `significance`) |
| 267 | `/zones/4/nerves/1/name` | `name` |  | string | 안와하신경 비측분지 |
| 268 | `/zones/4/nerves/1/type` | `type` |  | string | sensory |
| 269 | `/zones/4/nerves/1/significance` | `significance` |  | string | 코 외측 감각 |
| 270 | `/zones/4/safe_injection_depth` | `safe_injection_depth` |  | string | 골막상 (코뼈 부위) 또는 연골막상 (비첨부) |
| 271 | `/zones/4/tissue_data` | `tissue_data` |  | object{4} | (컨테이너 · 키: `rhinion_subcutaneous_mm`, `rhinion_data_source`, `nasal_tip_skin_thickness_mm`, `notes`) |
| 272 | `/zones/4/tissue_data/rhinion_subcutaneous_mm` | `rhinion_subcutaneous_mm` |  | number | `2.02` |
| 273 | `/zones/4/tissue_data/rhinion_data_source` | `rhinion_data_source` |  | string | JCD 2024, USG n=52 |
| 274 | `/zones/4/tissue_data/nasal_tip_skin_thickness_mm` | `nasal_tip_skin_thickness_mm` |  | number | `1.5` |
| 275 | `/zones/4/tissue_data/notes` | `notes` |  | string | Rhinion 피하조직 2.02mm (초음파 측정) — 혈관이 매우 표재성 |
| 276 | `/zones/4/clinical_pearls` | `clinical_pearls` |  | array[7] | (배열 · 7개) |
| 277 | `/zones/4/clinical_pearls/0` | `(clinical_pearls 원소)` | 0 | string | 실명 원인 부위 1위 — 최신 문헌에서 코가 글라벨라를 제치고 최다 부위 (Beleznay 2019 업데이트 56.3%, 2023/24 업데이트 40.6%; 25.5%는 2015년 초기 리뷰 값) |
| 278 | `/zones/4/clinical_pearls/1` | `(clinical_pearls 원소)` | 1 | string | 배비동맥: 0.0368mL로 안동맥 폐색 — 모든 부위 중 최소 용량 |
| 279 | `/zones/4/clinical_pearls/2` | `(clinical_pearls 원소)` | 2 | string | Rhinion 피하조직 2.02mm — 혈관이 피부 바로 아래 |
| 280 | `/zones/4/clinical_pearls/3` | `(clinical_pearls 원소)` | 3 | string | 니들 구부러짐 위험 (비골/연골 접촉 시) → 연골 손상 가능 |
| 281 | `/zones/4/clinical_pearls/4` | `(clinical_pearls 원소)` | 4 | string | 코 필러 후 피부 색상 변화(blanching) 즉시 확인 |
| 282 | `/zones/4/clinical_pearls/5` | `(clinical_pearls 원소)` | 5 | string | 비첨부는 end-artery 영역 → 혈관 폐색 시 괴사 고위험 |
| 283 | `/zones/4/clinical_pearls/6` | `(clinical_pearls 원소)` | 6 | string | 코 필러 시술 전 hyaluronidase 반드시 준비 |
| 284 | `/zones/4/botox_specific` | `botox_specific` |  | object{5} | (컨테이너 · 키: `target_muscle`, `risk`, `safe_zone`, `key_warning`, `dose_range`) |
| 285 | `/zones/4/botox_specific/target_muscle` | `target_muscle` |  | string | 비근근 (Nasalis) — bunny lines, 코끝 처짐(depressor septi nasi) |
| 286 | `/zones/4/botox_specific/risk` | `risk` |  | string | 비익 함몰(alar collapse), 비밸브 기능장애 → 호흡곤란 |
| 287 | `/zones/4/botox_specific/safe_zone` | `safe_zone` |  | string | 비근부 표재성, 비중격하강근(depressor septi nasi)은 비주 기시부 |
| 288 | `/zones/4/botox_specific/key_warning` | `key_warning` |  | string | 비근근 외측 과다 주사 → 비익 함몰 → 코 호흡 장애 |
| 289 | `/zones/4/botox_specific/dose_range` | `dose_range` |  | string | Bunny lines 2-4U/측, 비중격하강근 2-5U |
| 290 | `/zones/4/filler_specific` | `filler_specific` |  | object{6} | (컨테이너 · 키: `risk_level`, `primary_risk`, `safe_technique`, `max_per_point_ml`, `preferred_product`, `emergency_protocol`) |
| 291 | `/zones/4/filler_specific/risk_level` | `risk_level` |  | integer | `5` |
| 292 | `/zones/4/filler_specific/primary_risk` | `primary_risk` |  | string | 역행성 색전 → 실명 + 코 피부 괴사 |
| 293 | `/zones/4/filler_specific/safe_technique` | `safe_technique` |  | string | 코등: 골막상 캐뉼러, 정중선, 극소량. 비첨: 니들 소량 다점 |
| 294 | `/zones/4/filler_specific/max_per_point_ml` | `max_per_point_ml` |  | number | `0.05` |
| 295 | `/zones/4/filler_specific/preferred_product` | `preferred_product` |  | string | HA 필수 (hyaluronidase 용해 가능), 코에 CaHA/PLLA 금기 |
| 296 | `/zones/4/filler_specific/emergency_protocol` | `emergency_protocol` |  | string | blanching 즉시 → 주입 중단 → 고용량 pulsed hyaluronidase 다점 침윤(코 침범 시 약 900IU급, CRT 정상화까지 15~60분 간격 반복) + warm compress + massage + aspirin 300mg 로딩 후 75~100mg/일, 시각증상 동반 시 즉시 안과 이송 |

## 잠정 관찰 (원문 칸과 분리)

| # | 상태 | 근거 Pointer | 관찰 | issues.md |
|---|---|---|---|---|
| OBS-S05-01 | P | `/zones/4/clinical_pearls/0` | 같은 부위의 비율이 시점별로 세 개(2015 초기 25.5%, 2019 56.3%, 2023/24 40.6%) 있다. critical_safety_facts 의 '현재' 주장은 2019 값(56.3%)과 함께 쓰였다. '2023/24' 의 '/' 는 연도 묶음이다. | ADZ-P10 |
| OBS-S05-02 | F | `/zones/4/clinical_pearls/0` | '글라벨라' 는 zone name_ko '미간'(name_en Glabella)과 다른 표기다. | ADZ-F13 |
| OBS-S05-03 | P | `/zones/4/vessels/1/name` | 영문 명칭 두 개를 '/' 로 병기(External nasal artery / Lateral nasal artery). README 의 '/ = 둘 중 하나' 규칙을 이름 병기에 기계 적용하지 않는다. | ADZ-P10 |
| OBS-S05-04 | P | `/zones/4/tissue_data/rhinion_data_source` | 출처가 약식('JCD 2024, USG n=52')이며 같은 tissue_data 의 nasal_tip_skin_thickness_mm 에는 출처 칸이 없다. | ADZ-B18 |
| OBS-S05-05 | P | `/zones/4/filler_specific/emergency_protocol` | 단계 순서(→), 수량(약 900IU급), 반복 간격 범위(15~60분, '~' 구분자), 종료 조건(CRT 정상화까지), 투약 수치(300mg 로딩 후 75~100mg/일), 조건부 이송이 이어진다. '~' 는 이 원장에서 nose·neck 에만 나온다. | ADZ-P11 |

## 수동 복합 표현 (직접 읽기)

탐색 관점은 수집용 꼬리표이며 확정 분류가 아니다. 구간은 값 문자열 기준 코드 포인트 `[start,end)`.

| ID | Pointer | 원문 구간 | 구간 | 탐색 관점 | 메모 |
|---|---|---|---|---|---|
| MX-S05-001 | `/zones/4/vessels/0/course` | 코등(dorsum)을 따라 하행, 안동맥의 직접 분지 | [0, 29] | 경로, 영문 병기 |  |
| MX-S05-002 | `/zones/4/vessels/0/danger` | 0.0368mL로 안동맥 폐색 → 실명 (최소 용량) | [0, 29] | 수량, 결과(→), 최상급 |  |
| MX-S05-003 | `/zones/4/vessels/1/name` | 외비동맥 (External nasal artery / Lateral nasal artery) | [0, 51] | 혈관명, 영문 이중 병기(/) |  |
| MX-S05-004 | `/zones/4/vessels/1/course` | 비익(ala) 외측, 안면동맥 분지 | [0, 19] | 위치 |  |
| MX-S05-005 | `/zones/4/vessels/1/danger` | 비익 괴사 위험 | [0, 8] | 위험 |  |
| MX-S05-006 | `/zones/4/vessels/2/course` | 비주(columella) 내 주행 | [0, 18] | 위치 |  |
| MX-S05-007 | `/zones/4/vessels/2/danger` | 비첨부 주사 시 손상 위험 | [0, 14] | 조건(시) |  |
| MX-S05-008 | `/zones/4/nerves/0/significance` | 코끝, 코등 하부 감각 | [0, 12] | 부위 나열 |  |
| MX-S05-009 | `/zones/4/nerves/1/name` | 안와하신경 비측분지 | [0, 10] | 신경명(영문 병기 없음) |  |
| MX-S05-010 | `/zones/4/safe_injection_depth` | 골막상 (코뼈 부위) 또는 연골막상 (비첨부) | [0, 25] | 층, 대안(또는), 위치 한정 |  |
| MX-S05-011 | `/zones/4/tissue_data/rhinion_data_source` | JCD 2024, USG n=52 | [0, 18] | 인용(약식), 표본 수 |  |
| MX-S05-012 | `/zones/4/tissue_data/notes` | Rhinion 피하조직 2.02mm (초음파 측정) — 혈관이 매우 표재성 | [0, 41] | 수량, 측정 방법, 정도(매우) |  |
| MX-S05-013 | `/zones/4/clinical_pearls/0` | 실명 원인 부위 1위 | [0, 11] | 순위 |  |
| MX-S05-014 | `/zones/4/clinical_pearls/0` | 최신 문헌에서 코가 글라벨라를 제치고 최다 부위 | [14, 40] | 시간(최신), 비교, 최상급 |  |
| MX-S05-015 | `/zones/4/clinical_pearls/0` | Beleznay 2019 업데이트 56.3% | [42, 66] | 인용(약식), 시간, 비율 |  |
| MX-S05-016 | `/zones/4/clinical_pearls/0` | 2023/24 업데이트 40.6% | [68, 86] | 시간(연도 묶음 /), 비율 |  |
| MX-S05-017 | `/zones/4/clinical_pearls/0` | 25.5%는 2015년 초기 리뷰 값 | [88, 108] | 비율, 시간 |  |
| MX-S05-018 | `/zones/4/clinical_pearls/1` | 배비동맥: 0.0368mL로 안동맥 폐색 — 모든 부위 중 최소 용량 | [0, 38] | 수량, 최상급, 전 부위 비교 |  |
| MX-S05-019 | `/zones/4/clinical_pearls/2` | Rhinion 피하조직 2.02mm — 혈관이 피부 바로 아래 | [0, 34] | 수량, 위치 |  |
| MX-S05-020 | `/zones/4/clinical_pearls/3` | 니들 구부러짐 위험 (비골/연골 접촉 시) → 연골 손상 가능 | [0, 34] | 조건(시), 기호(/), 가능성 |  |
| MX-S05-021 | `/zones/4/clinical_pearls/4` | 코 필러 후 피부 색상 변화(blanching) 즉시 확인 | [0, 32] | 시간(후·즉시), 영문 병기 |  |
| MX-S05-022 | `/zones/4/clinical_pearls/5` | 비첨부는 end-artery 영역 → 혈관 폐색 시 괴사 고위험 | [0, 35] | 조건(시), 결과(→) |  |
| MX-S05-023 | `/zones/4/clinical_pearls/6` | 코 필러 시술 전 hyaluronidase 반드시 준비 | [0, 30] | 시간(전), 필수(반드시) |  |
| MX-S05-024 | `/zones/4/botox_specific/target_muscle` | 비근근 (Nasalis) — bunny lines, 코끝 처짐(depressor septi nasi) | [0, 56] | 근육명, 적응, 영문 병기 |  |
| MX-S05-025 | `/zones/4/botox_specific/risk` | 비익 함몰(alar collapse), 비밸브 기능장애 → 호흡곤란 | [0, 37] | 부작용, 결과(→) |  |
| MX-S05-026 | `/zones/4/botox_specific/safe_zone` | 비중격하강근(depressor septi nasi)은 비주 기시부 | [9, 45] | 위치 |  |
| MX-S05-027 | `/zones/4/botox_specific/key_warning` | 비근근 외측 과다 주사 → 비익 함몰 → 코 호흡 장애 | [0, 30] | 연쇄(→), 정도(과다) |  |
| MX-S05-028 | `/zones/4/botox_specific/dose_range` | Bunny lines 2-4U/측 | [0, 18] | 적응+범위, 단위당 |  |
| MX-S05-029 | `/zones/4/botox_specific/dose_range` | 비중격하강근 2-5U | [20, 31] | 근육+범위 |  |
| MX-S05-030 | `/zones/4/filler_specific/primary_risk` | 역행성 색전 → 실명 + 코 피부 괴사 | [0, 21] | 결과(→), 기호(+) |  |
| MX-S05-031 | `/zones/4/filler_specific/safe_technique` | 코등: 골막상 캐뉼러, 정중선, 극소량 | [0, 21] | 적용 대상(코등:), 기법 |  |
| MX-S05-032 | `/zones/4/filler_specific/safe_technique` | 비첨: 니들 소량 다점 | [23, 35] | 적용 대상(비첨:), 기법 |  |
| MX-S05-033 | `/zones/4/filler_specific/preferred_product` | HA 필수 (hyaluronidase 용해 가능) | [0, 27] | 필수, 이유 |  |
| MX-S05-034 | `/zones/4/filler_specific/preferred_product` | 코에 CaHA/PLLA 금기 | [29, 44] | 금기, 기호(/) |  |
| MX-S05-035 | `/zones/4/filler_specific/emergency_protocol` | blanching 즉시 → 주입 중단 → 고용량 pulsed hyaluronidase 다점 침윤 | [0, 53] | 시간(즉시), 순서(→) |  |
| MX-S05-036 | `/zones/4/filler_specific/emergency_protocol` | 코 침범 시 약 900IU급 | [54, 69] | 조건(시), 근사(약·급) |  |
| MX-S05-037 | `/zones/4/filler_specific/emergency_protocol` | CRT 정상화까지 15~60분 간격 반복 | [71, 93] | 종료 조건(까지), 범위(~), 반복 |  |
| MX-S05-038 | `/zones/4/filler_specific/emergency_protocol` | warm compress + massage + aspirin 300mg 로딩 후 75~100mg/일 | [97, 152] | 기호(+), 수량, 순서(후), 범위(~), 단위당(/일) |  |
| MX-S05-039 | `/zones/4/filler_specific/emergency_protocol` | 시각증상 동반 시 즉시 안과 이송 | [154, 172] | 조건(시), 시간(즉시) |  |

## 정규식 보조 후보 (기계 · 요약)

| 패턴 | 출현 |
|---|---|
| number_unit | 13 |
| degree_emphasis | 7 |
| arrow | 9 |
| slash | 6 |
| condition | 5 |
| citation | 2 |
| em_dash | 5 |
| time_order | 8 |
| possibility_frequency | 2 |
| range | 4 |
| plus | 4 |
| negation_prohibition | 1 |
| comparator | 1 |

전체 출현·구간은 `expressions.json` → `regex_candidates` (section=S05).

## 전문어 분절 관찰 (Kiwi 원시 · K)

| Pointer | 낱말 | 구간 | Kiwi 토큰 | 상태 |
|---|---|---|---|---|
| `/zones/4/vessels/1/course` | 안면동맥 | [12, 16] | 안면/NNG + 동맥/NNG | K: 여러 형태소로 분절(원시 결과 보존) |
| `/zones/4/vessels/2/danger` | 비첨부 | [0, 3] | 비/XPN + 첨/NNG + 부/NNG | K: 여러 형태소로 분절(원시 결과 보존) |
| `/zones/4/safe_injection_depth` | 골막상 | [16, 19] | 연골막상/NNG | 관찰 대상 아님: 더 긴 낱말(토큰)의 부분 문자열 |
| `/zones/4/tissue_data/notes` | 표재성 | [38, 41] | 표재/NNG + 성/XSN | K: 여러 형태소로 분절(원시 결과 보존) |
| `/zones/4/clinical_pearls/5` | 비첨부 | [0, 3] | 비/XPN + 첨/NNG + 부/NNG | K: 여러 형태소로 분절(원시 결과 보존) |
| `/zones/4/botox_specific/target_muscle` | 비근근 | [0, 3] | 비/XPN + 근/NNG + 근/NNG | K: 여러 형태소로 분절(원시 결과 보존) |
| `/zones/4/botox_specific/safe_zone` | 비중격하강근 | [9, 15] | 비중/NNG + 격하/NNG + 강/NNG + 근/NNG | K: 여러 형태소로 분절(원시 결과 보존) |
| `/zones/4/botox_specific/safe_zone` | 표재성 | [4, 7] | 표재/NNG + 성/XSN | K: 여러 형태소로 분절(원시 결과 보존) |
| `/zones/4/botox_specific/key_warning` | 비근근 | [0, 3] | 비/XPN + 근/NNG + 근/NNG | K: 여러 형태소로 분절(원시 결과 보존) |
| `/zones/4/botox_specific/key_warning` | 비익 | [15, 17] | 비/XPN + 익/NNG | K: 여러 형태소로 분절(원시 결과 보존) |

단일 형태소로 나온 출현은 표에서 생략했다(`morphology.json` → `segmentation_review` 에 전부 있음).

