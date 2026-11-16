# S04 — zones[3] periorbital (눈 주변 / Periorbital)

[← review.md](review.md) · 범위 `/zones/3/**` · 소유 노드 59 · 말단 47 · 직접 읽기 done

상위 문맥: 루트 객체 → `zones` 배열(S00 소유) → `/zones/3` (id=`periorbital`, name_ko=`눈 주변`, name_en=`Periorbital`).

## 원문 값 (문서 순서 · 전부)

| # | JSON Pointer | 원본 컬럼명 | 배열 순번 | 자료형 | 원문 값 |
|---|---|---|---|---|---|
| 177 | `/zones/3` | `(zones 원소)` | 3 | object{12} | (컨테이너 · 키: `id`, `name_ko`, `name_en`, `danger_level`, `danger_color`, `vessels`, `nerves`, `safe_injection_depth`, `tissue_data`, `clinical_pearls`, `botox_specific`, `filler_specific`) |
| 178 | `/zones/3/id` | `id` |  | string | periorbital |
| 179 | `/zones/3/name_ko` | `name_ko` |  | string | 눈 주변 |
| 180 | `/zones/3/name_en` | `name_en` |  | string | Periorbital |
| 181 | `/zones/3/danger_level` | `danger_level` |  | integer | `5` |
| 182 | `/zones/3/danger_color` | `danger_color` |  | string | red |
| 183 | `/zones/3/vessels` | `vessels` |  | array[3] | (배열 · 3개) |
| 184 | `/zones/3/vessels/0` | `(vessels 원소)` | 0 | object{5} | (컨테이너 · 키: `name`, `depth_mm`, `diameter_mm`, `course`, `danger`) |
| 185 | `/zones/3/vessels/0/name` | `name` |  | string | 각동맥 (Angular artery) |
| 186 | `/zones/3/vessels/0/depth_mm` | `depth_mm` |  | number | `2.3` |
| 187 | `/zones/3/vessels/0/diameter_mm` | `diameter_mm` |  | number | `1.7` |
| 188 | `/zones/3/vessels/0/course` | `course` |  | string | 내안각 내측 9.0mm, 비순구를 따라 상행 → 안동맥과 문합 |
| 189 | `/zones/3/vessels/0/danger` | `danger` |  | string | 안동맥과 직접 문합 — 역행성 색전 시 실명 |
| 190 | `/zones/3/vessels/1` | `(vessels 원소)` | 1 | object{5} | (컨테이너 · 키: `name`, `depth_mm`, `diameter_mm`, `course`, `danger`) |
| 191 | `/zones/3/vessels/1/name` | `name` |  | string | 안동맥 (Ophthalmic artery) |
| 192 | `/zones/3/vessels/1/depth_mm` | `depth_mm` |  | number | `15.0` |
| 193 | `/zones/3/vessels/1/diameter_mm` | `diameter_mm` |  | number | `1.5` |
| 194 | `/zones/3/vessels/1/course` | `course` |  | string | 안와 내 주행, 망막중심동맥 분지 |
| 195 | `/zones/3/vessels/1/danger` | `danger` |  | string | 망막 허혈 내성은 실질적으로 매우 짧아(현대 문헌 약 12-15분; 고전적 90-100분은 동물모델 상한값) 시야 변화 시 사실상 즉각·비가역적일 수 있음. 지체 없이 구후(retrobulbar) 히알루로니다제 및 안과 응급 프로토콜 가동 |
| 196 | `/zones/3/vessels/2` | `(vessels 원소)` | 2 | object{5} | (컨테이너 · 키: `name`, `depth_mm`, `diameter_mm`, `course`, `danger`) |
| 197 | `/zones/3/vessels/2/name` | `name` |  | string | 내안각동맥 (Medial palpebral artery) |
| 198 | `/zones/3/vessels/2/depth_mm` | `depth_mm` |  | number | `2.0` |
| 199 | `/zones/3/vessels/2/diameter_mm` | `diameter_mm` |  | number | `0.5` |
| 200 | `/zones/3/vessels/2/course` | `course` |  | string | 상하 안검 내측 주행 |
| 201 | `/zones/3/vessels/2/danger` | `danger` |  | string | 안와내 역류 경로 |
| 202 | `/zones/3/nerves` | `nerves` |  | array[2] | (배열 · 2개) |
| 203 | `/zones/3/nerves/0` | `(nerves 원소)` | 0 | object{3} | (컨테이너 · 키: `name`, `type`, `significance`) |
| 204 | `/zones/3/nerves/0/name` | `name` |  | string | 안와하신경 (Infraorbital nerve) |
| 205 | `/zones/3/nerves/0/type` | `type` |  | string | sensory |
| 206 | `/zones/3/nerves/0/significance` | `significance` |  | string | 하안검, 코 외측, 상구순 감각 — 안와하공에서 출현 |
| 207 | `/zones/3/nerves/1` | `(nerves 원소)` | 1 | object{3} | (컨테이너 · 키: `name`, `type`, `significance`) |
| 208 | `/zones/3/nerves/1/name` | `name` |  | string | 눈물신경 (Lacrimal nerve) |
| 209 | `/zones/3/nerves/1/type` | `type` |  | string | sensory |
| 210 | `/zones/3/nerves/1/significance` | `significance` |  | string | 외측 안검 감각 |
| 211 | `/zones/3/safe_injection_depth` | `safe_injection_depth` |  | string | 안와연(orbital rim) 외측, 골막상 |
| 212 | `/zones/3/tissue_data` | `tissue_data` |  | object{4} | (컨테이너 · 키: `tear_trough_anatomy`, `muscle_fiber_data`, `orbital_septum`, `notes`) |
| 213 | `/zones/3/tissue_data/tear_trough_anatomy` | `tear_trough_anatomy` |  | string | 눈물고랑(tear trough)은 안와연 바로 아래 — 안륜근(orbicularis oculi) 매우 얇음 |
| 214 | `/zones/3/tissue_data/muscle_fiber_data` | `muscle_fiber_data` |  | string | 눈물고랑 부위 안륜근 섬유 두께 0.5-1.0mm (SRA 2024) |
| 215 | `/zones/3/tissue_data/orbital_septum` | `orbital_septum` |  | string | 안와격막(orbital septum)은 안와 내용물의 방벽 — 관통 시 안와 내 합병증 |
| 216 | `/zones/3/tissue_data/notes` | `notes` |  | string | 각동맥: 내안각에서 medial 9.0mm, 깊이 2.3mm, 직경 1.7mm (교과서) |
| 217 | `/zones/3/clinical_pearls` | `clinical_pearls` |  | array[5] | (배열 · 5개) |
| 218 | `/zones/3/clinical_pearls/0` | `(clinical_pearls 원소)` | 0 | string | 각동맥은 내안각 9mm 내측, 깊이 2.3mm — 매우 표재성 |
| 219 | `/zones/3/clinical_pearls/1` | `(clinical_pearls 원소)` | 1 | string | 눈물고랑(tear trough) 필러는 안와연 아래에서 골막상 주사 |
| 220 | `/zones/3/clinical_pearls/2` | `(clinical_pearls 원소)` | 2 | string | 안와격막 절대 관통 금지 — 안와 내 주입 시 시신경 압박 |
| 221 | `/zones/3/clinical_pearls/3` | `(clinical_pearls 원소)` | 3 | string | 눈물고랑 근육 섬유 매우 얇음(0.5-1mm) → 필러 비침(Tyndall effect) 주의 |
| 222 | `/zones/3/clinical_pearls/4` | `(clinical_pearls 원소)` | 4 | string | 하안검 보톡스는 1-2U 소량만 — 과다 시 안검외반(ectropion) |
| 223 | `/zones/3/botox_specific` | `botox_specific` |  | object{5} | (컨테이너 · 키: `target_muscle`, `risk`, `safe_zone`, `key_warning`, `dose_range`) |
| 224 | `/zones/3/botox_specific/target_muscle` | `target_muscle` |  | string | 안륜근 (Orbicularis oculi) — 까마귀발, 눈밑 주름 |
| 225 | `/zones/3/botox_specific/risk` | `risk` |  | string | 하안검 외반(ectropion), 복시(diplopia), 안구건조 |
| 226 | `/zones/3/botox_specific/safe_zone` | `safe_zone` |  | string | 외안각 외측 1cm, 안와연 외측 |
| 227 | `/zones/3/botox_specific/key_warning` | `key_warning` |  | string | 안와연 내측 보톡스 → 안검하수/외반 위험 |
| 228 | `/zones/3/botox_specific/dose_range` | `dose_range` |  | string | 까마귀발 4-12U/측 (2-4포인트), 눈밑 1-2U (1포인트) |
| 229 | `/zones/3/filler_specific` | `filler_specific` |  | object{6} | (컨테이너 · 키: `risk_level`, `primary_risk`, `safe_technique`, `max_per_point_ml`, `preferred_product`, `emergency_protocol`) |
| 230 | `/zones/3/filler_specific/risk_level` | `risk_level` |  | integer | `5` |
| 231 | `/zones/3/filler_specific/primary_risk` | `primary_risk` |  | string | 역행성 색전 → 실명 (각동맥 → 안동맥) |
| 232 | `/zones/3/filler_specific/safe_technique` | `safe_technique` |  | string | 눈물고랑: 안와연 아래 골막상 캐뉼러, 극소량(0.1mL/측), 저점도 HA |
| 233 | `/zones/3/filler_specific/max_per_point_ml` | `max_per_point_ml` |  | number | `0.05` |
| 234 | `/zones/3/filler_specific/preferred_product` | `preferred_product` |  | string | 저점도 연성 HA (눈물고랑 전용 제품) |
| 235 | `/zones/3/filler_specific/emergency_protocol` | `emergency_protocol` |  | string | 시야 변화 즉시 → hyaluronidase + 안과 응급 |

## 잠정 관찰 (원문 칸과 분리)

| # | 상태 | 근거 Pointer | 관찰 | issues.md |
|---|---|---|---|---|
| OBS-S04-01 | P | `/zones/3/vessels/1/danger` | 한 값에 시간 수치 두 묶음(현대 문헌 약 12-15분 / 고전적 90-100분 동물모델 상한값)이 출처 성격과 함께 있다. 수치만 떼면 '동물모델 상한값' 한정이 사라진다. |  |
| OBS-S04-02 | F | `/zones/3/vessels/2/name` | 한글 '내안각동맥' 과 영문 'Medial palpebral artery' 병기. 두 명칭의 대응은 후속. | ADZ-F13 |
| OBS-S04-03 | P | `/zones/3/filler_specific/safe_technique`, `/zones/3/filler_specific/max_per_point_ml` | '0.1mL/측' 과 max_per_point_ml 0.05 는 기준(측/점)이 달라 직접 비교하지 않는다. | ADZ-P20 |
| OBS-S04-04 | P | `/zones/3/tissue_data/notes`, `/zones/3/clinical_pearls/0` | notes '9.0mm'(교과서) 와 pearls '9mm' — 표기만 다르다. |  |
| OBS-S04-05 | F | `/zones/3/vessels/1/danger`, `/zones/3/filler_specific/emergency_protocol` | '히알루로니다제' 와 'hyaluronidase' 가 원장 안에서 혼용된다. | ADZ-F13 |

## 수동 복합 표현 (직접 읽기)

탐색 관점은 수집용 꼬리표이며 확정 분류가 아니다. 구간은 값 문자열 기준 코드 포인트 `[start,end)`.

| ID | Pointer | 원문 구간 | 구간 | 탐색 관점 | 메모 |
|---|---|---|---|---|---|
| MX-S04-001 | `/zones/3/vessels/0/course` | 내안각 내측 9.0mm, 비순구를 따라 상행 → 안동맥과 문합 | [0, 34] | 거리, 경로(→) |  |
| MX-S04-002 | `/zones/3/vessels/0/danger` | 안동맥과 직접 문합 — 역행성 색전 시 실명 | [0, 24] | 조건(시), 결과 |  |
| MX-S04-003 | `/zones/3/vessels/1/course` | 안와 내 주행, 망막중심동맥 분지 | [0, 18] | 위치 |  |
| MX-S04-004 | `/zones/3/vessels/1/danger` | 망막 허혈 내성은 실질적으로 매우 짧아 | [0, 21] | 정도(매우), 수식(실질적으로) |  |
| MX-S04-005 | `/zones/3/vessels/1/danger` | 현대 문헌 약 12-15분 | [22, 36] | 시간, 범위, 근사(약), 출처 성격 |  |
| MX-S04-006 | `/zones/3/vessels/1/danger` | 고전적 90-100분은 동물모델 상한값 | [38, 59] | 시간, 범위, 출처 한정, 상한 |  |
| MX-S04-007 | `/zones/3/vessels/1/danger` | 시야 변화 시 사실상 즉각·비가역적일 수 있음 | [61, 86] | 조건(시), 가능성(수 있음), 수식(사실상) |  |
| MX-S04-008 | `/zones/3/vessels/1/danger` | 지체 없이 구후(retrobulbar) 히알루로니다제 및 안과 응급 프로토콜 가동 | [88, 133] | 시간(지체 없이), 부정형 수식(없이), 영문 병기 |  |
| MX-S04-009 | `/zones/3/vessels/2/name` | 내안각동맥 (Medial palpebral artery) | [0, 31] | 혈관명, 영문 병기 |  |
| MX-S04-010 | `/zones/3/vessels/2/danger` | 안와내 역류 경로 | [0, 9] | 경로 |  |
| MX-S04-011 | `/zones/3/nerves/0/significance` | 하안검, 코 외측, 상구순 감각 — 안와하공에서 출현 | [0, 29] | 부위 나열, 위치 |  |
| MX-S04-012 | `/zones/3/safe_injection_depth` | 안와연(orbital rim) 외측, 골막상 | [0, 24] | 위치, 층 |  |
| MX-S04-013 | `/zones/3/tissue_data/tear_trough_anatomy` | 눈물고랑(tear trough)은 안와연 바로 아래 | [0, 28] | 위치(바로 아래) |  |
| MX-S04-014 | `/zones/3/tissue_data/tear_trough_anatomy` | 안륜근(orbicularis oculi) 매우 얇음 | [31, 59] | 정도(매우) |  |
| MX-S04-015 | `/zones/3/tissue_data/muscle_fiber_data` | 눈물고랑 부위 안륜근 섬유 두께 0.5-1.0mm (SRA 2024) | [0, 38] | 범위, 인용(약식) |  |
| MX-S04-016 | `/zones/3/tissue_data/orbital_septum` | 관통 시 안와 내 합병증 | [35, 48] | 조건(시) |  |
| MX-S04-017 | `/zones/3/tissue_data/notes` | 각동맥: 내안각에서 medial 9.0mm, 깊이 2.3mm, 직경 1.7mm (교과서) | [0, 49] | 수량 나열, 출처(교과서) |  |
| MX-S04-018 | `/zones/3/clinical_pearls/0` | 각동맥은 내안각 9mm 내측, 깊이 2.3mm — 매우 표재성 | [0, 34] | 거리, 정도(매우) |  |
| MX-S04-019 | `/zones/3/clinical_pearls/1` | 눈물고랑(tear trough) 필러는 안와연 아래에서 골막상 주사 | [0, 37] | 위치, 층 |  |
| MX-S04-020 | `/zones/3/clinical_pearls/2` | 안와격막 절대 관통 금지 | [0, 13] | 강조(절대), 금지 |  |
| MX-S04-021 | `/zones/3/clinical_pearls/2` | 안와 내 주입 시 시신경 압박 | [16, 32] | 조건(시), 결과 |  |
| MX-S04-022 | `/zones/3/clinical_pearls/3` | 눈물고랑 근육 섬유 매우 얇음(0.5-1mm) → 필러 비침(Tyndall effect) 주의 | [0, 52] | 정도, 범위, 결과(→), 영문 병기 |  |
| MX-S04-023 | `/zones/3/clinical_pearls/4` | 하안검 보톡스는 1-2U 소량만 | [0, 17] | 범위, 한정(만) |  |
| MX-S04-024 | `/zones/3/clinical_pearls/4` | 과다 시 안검외반(ectropion) | [20, 40] | 조건(시) |  |
| MX-S04-025 | `/zones/3/botox_specific/target_muscle` | 안륜근 (Orbicularis oculi) — 까마귀발, 눈밑 주름 | [0, 37] | 근육명, 적응 |  |
| MX-S04-026 | `/zones/3/botox_specific/risk` | 하안검 외반(ectropion), 복시(diplopia), 안구건조 | [0, 37] | 부작용 나열 |  |
| MX-S04-027 | `/zones/3/botox_specific/safe_zone` | 외안각 외측 1cm, 안와연 외측 | [0, 18] | 거리, 위치 |  |
| MX-S04-028 | `/zones/3/botox_specific/key_warning` | 안와연 내측 보톡스 → 안검하수/외반 위험 | [0, 23] | 결과(→), 기호(/) |  |
| MX-S04-029 | `/zones/3/botox_specific/dose_range` | 까마귀발 4-12U/측 (2-4포인트) | [0, 21] | 적응+범위, 단위당 |  |
| MX-S04-030 | `/zones/3/botox_specific/dose_range` | 눈밑 1-2U (1포인트) | [23, 37] | 적응+범위 |  |
| MX-S04-031 | `/zones/3/filler_specific/primary_risk` | 역행성 색전 → 실명 (각동맥 → 안동맥) | [0, 23] | 결과(→), 경로(→) |  |
| MX-S04-032 | `/zones/3/filler_specific/safe_technique` | 눈물고랑: 안와연 아래 골막상 캐뉼러, 극소량(0.1mL/측), 저점도 HA | [0, 42] | 적용 대상(눈물고랑:), 수량, 단위당(/측) |  |
| MX-S04-033 | `/zones/3/filler_specific/preferred_product` | 저점도 연성 HA (눈물고랑 전용 제품) | [0, 22] | 수식, 전용 |  |
| MX-S04-034 | `/zones/3/filler_specific/emergency_protocol` | 시야 변화 즉시 → hyaluronidase + 안과 응급 | [0, 32] | 시간(즉시), 순서(→), 기호(+) |  |

## 정규식 보조 후보 (기계 · 요약)

| 패턴 | 출현 |
|---|---|
| number_unit | 17 |
| arrow | 6 |
| condition | 5 |
| em_dash | 8 |
| range | 8 |
| negation_prohibition | 2 |
| possibility_frequency | 2 |
| time_order | 3 |
| degree_emphasis | 6 |
| middle_dot | 1 |
| citation | 1 |
| slash | 3 |
| plus | 1 |

전체 출현·구간은 `expressions.json` → `regex_candidates` (section=S04).

## 전문어 분절 관찰 (Kiwi 원시 · K)

| Pointer | 낱말 | 구간 | Kiwi 토큰 | 상태 |
|---|---|---|---|---|
| `/zones/3/vessels/1/course` | 망막중심동맥 | [9, 15] | 망막/NNG + 중심/NNG + 동맥/NNG | K: 여러 형태소로 분절(원시 결과 보존) |
| `/zones/3/vessels/2/name` | 각동맥 | [2, 5] | 내안각동맥/NNP | 관찰 대상 아님: 더 긴 낱말(토큰)의 부분 문자열 |
| `/zones/3/nerves/0/significance` | 안와하공 | [20, 24] | 안와/NNG + 하/NNG + 공/NNG | K: 여러 형태소로 분절(원시 결과 보존) |
| `/zones/3/tissue_data/orbital_septum` | 안와격막 | [0, 4] | 안와/NNG + 격막/NNG | K: 여러 형태소로 분절(원시 결과 보존) |
| `/zones/3/clinical_pearls/0` | 각동맥 | [0, 3] | 각/MM + 동맥/NNG | K: 여러 형태소로 분절(원시 결과 보존) |
| `/zones/3/clinical_pearls/0` | 표재성 | [31, 34] | 표재/NNG + 성/XSN | K: 여러 형태소로 분절(원시 결과 보존) |
| `/zones/3/clinical_pearls/1` | 골막상 | [31, 34] | 골/NNG + 막상/MAG | K: 여러 형태소로 분절(원시 결과 보존) |
| `/zones/3/clinical_pearls/2` | 안와격막 | [0, 4] | 안와/NNG + 격막/NNG | K: 여러 형태소로 분절(원시 결과 보존) |
| `/zones/3/filler_specific/preferred_product` | 저점도 | [0, 3] | 저/MM + 점/NNG + 도/JX | K: 여러 형태소로 분절(원시 결과 보존) |

단일 형태소로 나온 출현은 표에서 생략했다(`morphology.json` → `segmentation_review` 에 전부 있음).

