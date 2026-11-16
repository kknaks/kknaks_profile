# anatomy-danger-zones.json — 1차 조사 (읽기용)

## 상태

| 항목 | 상태 |
|---|---|
| **1차 범위 종료** | 예 — 아래 기준 충족(상세 validation.md) |
| **원장 전체 완료** | **아님** — 의미 분해·공통 개념·관계 확정·원문 불일치 처리는 후속 단계 |
| 전수 읽기 | 12/12 구획 직접 읽기 완료 (coverage.json) |
| 구조·값 수집 | 노드 615 · 말단 483 (문자열 376 · 숫자 107 · 빈 컨테이너 0 · 빈 문자열 0 · null 0 · 불리언 0) |
| 형태소·표현 수집 | 텍스트 값 331 · 필드명 74 · 제외 152 · 토큰 4273 / 수동 표현 352 · 정규식 후보 568 · 절 구간 410 |
| 기계 검증 | verify.py 통과 기준 — validation.md |
| 읽기 검토 | validation.md §읽기 검토 |
| 알려진 분석 오류 | K — morphology.json segmentation_review / issues.md |
| 열린 미결 · 후속 의미 조사 | issues.md (A 0 · B · C 0 · I · P · F · K) |

## 원본

| 항목 | 값 |
|---|---|
| path | `orchestration/work/phub-recommend/bronze/phub-ledger/anatomy-danger-zones.json` |
| bytes | `29555` |
| codepoints | `19567` |
| sha256 | `34b2a2de737a2770828ce52e49c3f4f17dc54c21ad9754362c24ebf4fced69a4` |
| lines | `1` |
| trailing_newline | `False` |
| encoding | `utf-8` |
| bom | `False` |
| any_string_escape | `False` |
| duplicate_keys | 0 (감지 없음) |

파일은 줄바꿈 없는 한 줄 JSON 이다. 이스케이프 문자열이 없어 따옴표 안쪽 원문과 디코딩 값이 같다. 구간 단위: 값 기준·파일 기준 모두 Unicode 코드 포인트 `[start,end)`, 바이트 구간은 별도 칸(`*_byte_span`).

## 전체 컬럼 구성

경로 패턴의 `*` 는 배열 순번. 자료형 칸의 숫자는 크기 범위. 예시는 첫 출현의 원문 값(전체)과 Pointer.

| 원본 컬럼명 / 경로 패턴 | 자료형 · 중첩 | 출현 수 | 존재 범위 | 원문 예시 | 예시 Pointer |
|---|---|---|---|---|---|
| `(root)` | object (크기 5) | 1 | 최상위 1회 | (컨테이너 · 키: `version`, `updated`, `consensus_method`, `critical_safety_facts`, `zones`) | `(root)` |
| `/version` | string | 1 | 최상위 1회 | 1.2 | `/version` |
| `/updated` | string | 1 | 최상위 1회 | 2026-07-26 | `/updated` |
| `/consensus_method` | string | 1 | 최상위 1회 | 3-AI Expert Consensus (Perplexity research + Gemini analysis + Claude textbook) | `/consensus_method` |
| `/critical_safety_facts` | object (크기 4) | 1 | 최상위 1회 | (컨테이너 · 키: `minimum_filler_for_blindness`, `blindness_highest_risk_zones`, `mechanism`, `caveat`) | `/critical_safety_facts` |
| `/critical_safety_facts/minimum_filler_for_blindness` | string | 1 | 최상위 1회 | 약 0.04mL (supratrochlear 0.0397mL, supraorbital 0.0409mL, dorsal nasal 0.0368mL; Yi et al., J Cosmet Dermatol 2024). Supratrochlear 단일 경로 부피는 약 0.085mL(범위 0.04-0.12mL; Khan et al., Aesthetic Surgery Journal 2017;37(2):203-208). 수치는 혈관 부피 기반 이론값으로 실제 임계량은 변이가 있어 절대 안전 기준이 아님 | `/critical_safety_facts/minimum_filler_for_blindness` |
| `/critical_safety_facts/blindness_highest_risk_zones` | string | 1 | 최상위 1회 | 코 56.3%, 미간 27.1%, 이마 18.8%, 비순주름 14.6% (Beleznay et al., Aesthet Surg J 2019;39(6):662-674) — 코가 현재 최고위험부위 | `/critical_safety_facts/blindness_highest_risk_zones` |
| `/critical_safety_facts/mechanism` | string | 1 | 최상위 1회 | 역행성 동맥 색전 — 안동맥(ophthalmic artery)으로 역류 → 망막 허혈 | `/critical_safety_facts/mechanism` |
| `/critical_safety_facts/caveat` | string | 1 | 최상위 1회 | 이 수치들은 시술자 경계를 느슨하게 만들지 말 것. 어떤 주사라도 혈관 내 주입이면 실명 가능. 흡인은 음성 결과가 안전을 보장하지 않는 보조 수단이며, 저압·저속·소량 주입·캐뉼러 사용·hyaluronidase 상비가 핵심 | `/critical_safety_facts/caveat` |
| `/zones` | array (크기 11) | 1 | 최상위 1회 | (배열 · 11개) | `/zones` |
| `/zones/*` | object (크기 12) | 11 | zone 11/11 | (컨테이너 · 키: `id`, `name_ko`, `name_en`, `danger_level`, `danger_color`, `vessels`, `nerves`, `safe_injection_depth`, `tissue_data`, `clinical_pearls`, `botox_specific`, `filler_specific`) | `/zones/0` |
| `/zones/*/id` | string | 11 | zone 11/11 | forehead | `/zones/0/id` |
| `/zones/*/name_ko` | string | 11 | zone 11/11 | 이마 | `/zones/0/name_ko` |
| `/zones/*/name_en` | string | 11 | zone 11/11 | Forehead | `/zones/0/name_en` |
| `/zones/*/danger_level` | integer | 11 | zone 11/11 | `4` | `/zones/0/danger_level` |
| `/zones/*/danger_color` | string | 11 | zone 11/11 | orange | `/zones/0/danger_color` |
| `/zones/*/vessels` | array (크기 2–3) | 11 | zone 11/11 | (배열 · 2개) | `/zones/0/vessels` |
| `/zones/*/vessels/*` | object (크기 5–7) | 24 | zone 11/11 | (컨테이너 · 키: `name`, `depth_mm`, `diameter_mm`, `course`, `danger`, `note`, `depth_range_mm`) | `/zones/0/vessels/0` |
| `/zones/*/vessels/*/name` | string | 24 | zone 11/11 | 활차상동맥 (Supratrochlear artery) | `/zones/0/vessels/0/name` |
| `/zones/*/vessels/*/depth_mm` | number | 22 | zone 10/11 (있는 zone: 0=forehead, 1=glabella, 2=temple, 3=periorbital, 4=nose, 5=nasolabial, 6=cheek, 8=chin, 9=jawline, 10=neck) | `1.8` | `/zones/0/vessels/0/depth_mm` |
| `/zones/*/vessels/*/diameter_mm` | number | 24 | zone 11/11 | `0.7` | `/zones/0/vessels/0/diameter_mm` |
| `/zones/*/vessels/*/course` | string | 24 | zone 11/11 | 안와상연에서 상방으로 주행, 이마 중앙선 근처 | `/zones/0/vessels/0/course` |
| `/zones/*/vessels/*/danger` | string | 24 | zone 11/11 | 안동맥과 직접 연결 — 역행성 색전 시 실명 위험 | `/zones/0/vessels/0/danger` |
| `/zones/*/vessels/*/note` | string | 2 | zone 1/11 (있는 zone: 0=forehead) | 평균 1.8mm이나 아시아인 피부는 더 얇고 개인 변이가 커 0.5mm 수준까지 표재성일 수 있음(Anat Rec 2024 cadaver) | `/zones/0/vessels/0/note` |
| `/zones/*/vessels/*/depth_range_mm` | array (크기 2) | 5 | zone 3/11 (있는 zone: 0=forehead, 1=glabella, 7=lips) | (배열 · 2개) | `/zones/0/vessels/0/depth_range_mm` |
| `/zones/*/vessels/*/depth_range_mm/*` | number | 10 | zone 3/11 (있는 zone: 0=forehead, 1=glabella, 7=lips) | `0.5` | `/zones/0/vessels/0/depth_range_mm/0` |
| `/zones/*/nerves` | array (크기 1–3) | 11 | zone 11/11 | (배열 · 2개) | `/zones/0/nerves` |
| `/zones/*/nerves/*` | object (크기 3) | 21 | zone 11/11 | (컨테이너 · 키: `name`, `type`, `significance`) | `/zones/0/nerves/0` |
| `/zones/*/nerves/*/name` | string | 21 | zone 11/11 | 활차상신경 (Supratrochlear nerve) | `/zones/0/nerves/0/name` |
| `/zones/*/nerves/*/type` | string | 21 | zone 11/11 | sensory | `/zones/0/nerves/0/type` |
| `/zones/*/nerves/*/significance` | string | 21 | zone 11/11 | 이마 내측 감각 | `/zones/0/nerves/0/significance` |
| `/zones/*/safe_injection_depth` | string | 11 | zone 11/11 | 골막상층 (supraperiosteal) — 혈관은 표재성이므로 깊은 층이 안전 | `/zones/0/safe_injection_depth` |
| `/zones/*/tissue_data` | object (크기 3–6) | 11 | zone 11/11 | (컨테이너 · 키: `frontalis_thickness`, `skin_to_periosteum_mm`, `notes`) | `/zones/0/tissue_data` |
| `/zones/*/tissue_data/frontalis_thickness` | object (크기 3) | 1 | zone 1/11 (있는 zone: 0=forehead) | (컨테이너 · 키: `midpupil_mm`, `lateral_canthus_mm`, `lateral_orbital_rim_mm`) | `/zones/0/tissue_data/frontalis_thickness` |
| `/zones/*/tissue_data/frontalis_thickness/midpupil_mm` | number | 1 | zone 1/11 (있는 zone: 0=forehead) | `1.8` | `/zones/0/tissue_data/frontalis_thickness/midpupil_mm` |
| `/zones/*/tissue_data/frontalis_thickness/lateral_canthus_mm` | number | 1 | zone 1/11 (있는 zone: 0=forehead) | `1.61` | `/zones/0/tissue_data/frontalis_thickness/lateral_canthus_mm` |
| `/zones/*/tissue_data/frontalis_thickness/lateral_orbital_rim_mm` | number | 1 | zone 1/11 (있는 zone: 0=forehead) | `0.11` | `/zones/0/tissue_data/frontalis_thickness/lateral_orbital_rim_mm` |
| `/zones/*/tissue_data/skin_to_periosteum_mm` | number | 1 | zone 1/11 (있는 zone: 0=forehead) | `5.0` | `/zones/0/tissue_data/skin_to_periosteum_mm` |
| `/zones/*/tissue_data/notes` | string | 11 | zone 11/11 | 이마 피부-골막 거리 평균 0.5cm — 매우 얇음 | `/zones/0/tissue_data/notes` |
| `/zones/*/clinical_pearls` | array (크기 4–7) | 11 | zone 11/11 | (배열 · 4개) | `/zones/0/clinical_pearls` |
| `/zones/*/clinical_pearls/*` | string | 61 | zone 11/11 | 이마 피부-골막 거리 평균 0.5cm — 매우 얇음 | `/zones/0/clinical_pearls/0` |
| `/zones/*/botox_specific` | object (크기 5–6) | 11 | zone 11/11 | (컨테이너 · 키: `target_muscle`, `risk`, `safe_zone`, `diffusion_range_cm`, `key_warning`, `dose_range`) | `/zones/0/botox_specific` |
| `/zones/*/botox_specific/target_muscle` | string | 11 | zone 11/11 | 전두근 (Frontalis) | `/zones/0/botox_specific/target_muscle` |
| `/zones/*/botox_specific/risk` | string | 11 | zone 11/11 | 눈꺼풀 처짐 (보톡스 확산 시 상안검거근 영향) | `/zones/0/botox_specific/risk` |
| `/zones/*/botox_specific/safe_zone` | string | 11 | zone 11/11 | 안와상연 상방 2cm 이상, 외측은 측두선 내측 | `/zones/0/botox_specific/safe_zone` |
| `/zones/*/botox_specific/diffusion_range_cm` | string | 1 | zone 1/11 (있는 zone: 0=forehead) | 1.5-3.0 | `/zones/0/botox_specific/diffusion_range_cm` |
| `/zones/*/botox_specific/key_warning` | string | 11 | zone 11/11 | 보톡스 확산 1.5-3cm → 안와상연 너무 가까이 주사 시 안검하수 | `/zones/0/botox_specific/key_warning` |
| `/zones/*/botox_specific/dose_range` | string | 11 | zone 11/11 | 10-30 units (2-5 포인트/측, 2-5U/포인트) | `/zones/0/botox_specific/dose_range` |
| `/zones/*/filler_specific` | object (크기 5–6) | 11 | zone 11/11 | (컨테이너 · 키: `risk_level`, `primary_risk`, `safe_technique`, `max_per_point_ml`, `preferred_product`) | `/zones/0/filler_specific` |
| `/zones/*/filler_specific/risk_level` | integer | 11 | zone 11/11 | `4` | `/zones/0/filler_specific/risk_level` |
| `/zones/*/filler_specific/primary_risk` | string | 11 | zone 11/11 | 역행성 색전 → 실명 | `/zones/0/filler_specific/primary_risk` |
| `/zones/*/filler_specific/safe_technique` | string | 11 | zone 11/11 | 골막상 캐뉼러, 소량 다점, 저압 주입 | `/zones/0/filler_specific/safe_technique` |
| `/zones/*/filler_specific/max_per_point_ml` | number | 11 | zone 11/11 | `0.1` | `/zones/0/filler_specific/max_per_point_ml` |
| `/zones/*/filler_specific/preferred_product` | string | 11 | zone 11/11 | 용해 가능한 저점도 HA (CaHA는 hyaluronidase로 용해 불가하여 실명 위험 부위에서는 권장하지 않음) | `/zones/0/filler_specific/preferred_product` |
| `/zones/*/tissue_data/csm_mean_thickness_mm` | number | 1 | zone 1/11 (있는 zone: 1=glabella) | `1.62` | `/zones/1/tissue_data/csm_mean_thickness_mm` |
| `/zones/*/tissue_data/csm_thickness_variation_mm` | number | 1 | zone 1/11 (있는 zone: 1=glabella) | `0.4` | `/zones/1/tissue_data/csm_thickness_variation_mm` |
| `/zones/*/filler_specific/emergency_protocol` | string | 3 | zone 3/11 (있는 zone: 1=glabella, 3=periorbital, 4=nose) | 시력저하·안통 발생 시 즉시 주입 중단/응급콜 및 망막안과·응급실 이송(지체 없이 즉각 대응); HA 필러는 주입부·허혈부 및 미간-상활차/상안와/비배부 혈관경로에 hyaluronidase ≥1,500U(IU) 광범위 다점 침윤 후 필요 시 반복(총량 상한 없음), 안구마사지·안압강하제는 보조, retrobulbar/peribulbar 1,500–3,000U는 안과/숙련자만 시행하고 이송 지연 금지. | `/zones/1/filler_specific/emergency_protocol` |
| `/zones/*/tissue_data/stl_entry_point` | string | 1 | zone 1/11 (있는 zone: 2=temple) | STL(상측두융합선, Superior temporal line)에서 측두근막이 두 층으로 분리 | `/zones/2/tissue_data/stl_entry_point` |
| `/zones/*/tissue_data/pitanguy_line` | string | 1 | zone 1/11 (있는 zone: 2=temple) | 이주(tragus) 하부 0.5cm → 눈썹 외측 1.5cm 상방을 잇는 선 위에 측두신경 주행 | `/zones/2/tissue_data/pitanguy_line` |
| `/zones/*/tissue_data/tear_trough_anatomy` | string | 1 | zone 1/11 (있는 zone: 3=periorbital) | 눈물고랑(tear trough)은 안와연 바로 아래 — 안륜근(orbicularis oculi) 매우 얇음 | `/zones/3/tissue_data/tear_trough_anatomy` |
| `/zones/*/tissue_data/muscle_fiber_data` | string | 1 | zone 1/11 (있는 zone: 3=periorbital) | 눈물고랑 부위 안륜근 섬유 두께 0.5-1.0mm (SRA 2024) | `/zones/3/tissue_data/muscle_fiber_data` |
| `/zones/*/tissue_data/orbital_septum` | string | 1 | zone 1/11 (있는 zone: 3=periorbital) | 안와격막(orbital septum)은 안와 내용물의 방벽 — 관통 시 안와 내 합병증 | `/zones/3/tissue_data/orbital_septum` |
| `/zones/*/tissue_data/rhinion_subcutaneous_mm` | number | 1 | zone 1/11 (있는 zone: 4=nose) | `2.02` | `/zones/4/tissue_data/rhinion_subcutaneous_mm` |
| `/zones/*/tissue_data/rhinion_data_source` | string | 1 | zone 1/11 (있는 zone: 4=nose) | JCD 2024, USG n=52 | `/zones/4/tissue_data/rhinion_data_source` |
| `/zones/*/tissue_data/nasal_tip_skin_thickness_mm` | number | 1 | zone 1/11 (있는 zone: 4=nose) | `1.5` | `/zones/4/tissue_data/nasal_tip_skin_thickness_mm` |
| `/zones/*/tissue_data/facial_artery_distance_to_nlf_mm` | number | 1 | zone 1/11 (있는 zone: 5=nasolabial) | `5.0` | `/zones/5/tissue_data/facial_artery_distance_to_nlf_mm` |
| `/zones/*/tissue_data/asian_adjacent_distribution_percent` | number | 1 | zone 1/11 (있는 zone: 5=nasolabial) | `93.3` | `/zones/5/tissue_data/asian_adjacent_distribution_percent` |
| `/zones/*/tissue_data/within_5mm_percent` | number | 1 | zone 1/11 (있는 zone: 5=nasolabial) | `42.9` | `/zones/5/tissue_data/within_5mm_percent` |
| `/zones/*/tissue_data/facial_artery_diameter_mandible_mm` | number | 1 | zone 1/11 (있는 zone: 5=nasolabial) | `1.9` | `/zones/5/tissue_data/facial_artery_diameter_mandible_mm` |
| `/zones/*/tissue_data/facial_artery_diameter_nasal_mm` | number | 1 | zone 1/11 (있는 zone: 5=nasolabial) | `0.8` | `/zones/5/tissue_data/facial_artery_diameter_nasal_mm` |
| `/zones/*/tissue_data/buccal_fat_pad` | string | 1 | zone 1/11 (있는 zone: 6=cheek) | 협지방체(Buccal fat pad): SMAS 심층에 위치, 저작공간까지 연장 | `/zones/6/tissue_data/buccal_fat_pad` |
| `/zones/*/tissue_data/smas_depth_mm` | number | 1 | zone 1/11 (있는 zone: 6=cheek) | `4.5` | `/zones/6/tissue_data/smas_depth_mm` |
| `/zones/*/tissue_data/sub_smas_vs_subcutaneous` | string | 1 | zone 1/11 (있는 zone: 6=cheek) | Sub-SMAS: 볼륨 리프팅 / Subcutaneous: 표재성 주름 교정 | `/zones/6/tissue_data/sub_smas_vs_subcutaneous` |
| `/zones/*/tissue_data/labial_artery_depth_range_mm` | array (크기 2) | 1 | zone 1/11 (있는 zone: 7=lips) | (배열 · 2개) | `/zones/7/tissue_data/labial_artery_depth_range_mm` |
| `/zones/*/tissue_data/labial_artery_depth_range_mm/*` | number | 2 | zone 1/11 (있는 zone: 7=lips) | `3.0` | `/zones/7/tissue_data/labial_artery_depth_range_mm/0` |
| `/zones/*/tissue_data/superior_labial_artery_submucosal_percent` | number | 1 | zone 1/11 (있는 zone: 7=lips) | `58.5` | `/zones/7/tissue_data/superior_labial_artery_submucosal_percent` |
| `/zones/*/tissue_data/mental_foramen_location` | string | 1 | zone 1/11 (있는 zone: 8=chin) | 하악 제2소구치 하방, 하악연에서 상방 약 13mm | `/zones/8/tissue_data/mental_foramen_location` |
| `/zones/*/tissue_data/dao_coverage` | string | 1 | zone 1/11 (있는 zone: 8=chin) | DAO(구각하제근)의 67.7%가 이신경공을 덮고 있음 | `/zones/8/tissue_data/dao_coverage` |
| `/zones/*/tissue_data/marginal_mandibular_depth` | string | 1 | zone 1/11 (있는 zone: 9=jawline) | 하악연에서 1-2cm 하방에서 표재성 주행 (20% 환자에서 하악연 하방 1cm까지) | `/zones/9/tissue_data/marginal_mandibular_depth` |
| `/zones/*/tissue_data/facial_artery_crossing` | string | 1 | zone 1/11 (있는 zone: 9=jawline) | 안면동맥은 하악연의 교근 전연(anterior border of masseter)에서 교차 | `/zones/9/tissue_data/facial_artery_crossing` |
| `/zones/*/tissue_data/platysma_thickness_mm` | number | 1 | zone 1/11 (있는 zone: 10=neck) | `1.5` | `/zones/10/tissue_data/platysma_thickness_mm` |
| `/zones/*/tissue_data/platysma_coverage` | string | 1 | zone 1/11 (있는 zone: 10=neck) | 광경근은 쇄골~하악연까지, 정중선에서 결손 부위 있음 | `/zones/10/tissue_data/platysma_coverage` |

### 구조 변형 · 선택 필드 · 빈 값

| 구분 | 원문 사실 | Pointer |
|---|---|---|
| 빈 값 | 빈 문자열 0 · 빈 배열/객체 0 · null 0 — 이 원장에는 없다 | — |
| 선택 필드(일부 zone) | `/zones/*/vessels/*/depth_mm` — zone 10/11 (있는 zone: 0=forehead, 1=glabella, 2=temple, 3=periorbital, 4=nose, 5=nasolabial, 6=cheek, 8=chin, 9=jawline, 10=neck) | `/zones/0/vessels/0/depth_mm`, `/zones/0/vessels/1/depth_mm`, `/zones/1/vessels/0/depth_mm`, `/zones/1/vessels/1/depth_mm`, `/zones/2/vessels/0/depth_mm`, `/zones/2/vessels/1/depth_mm`, `/zones/3/vessels/0/depth_mm`, `/zones/3/vessels/1/depth_mm`, `/zones/3/vessels/2/depth_mm`, `/zones/4/vessels/0/depth_mm`, `/zones/4/vessels/1/depth_mm`, `/zones/4/vessels/2/depth_mm`, `/zones/5/vessels/0/depth_mm`, `/zones/5/vessels/1/depth_mm`, `/zones/6/vessels/0/depth_mm`, `/zones/6/vessels/1/depth_mm`, `/zones/8/vessels/0/depth_mm`, `/zones/8/vessels/1/depth_mm`, `/zones/9/vessels/0/depth_mm`, `/zones/9/vessels/1/depth_mm`, `/zones/10/vessels/0/depth_mm`, `/zones/10/vessels/1/depth_mm` |
| 선택 필드(일부 zone) | `/zones/*/vessels/*/note` — zone 1/11 (있는 zone: 0=forehead) | `/zones/0/vessels/0/note`, `/zones/0/vessels/1/note` |
| 선택 필드(일부 zone) | `/zones/*/vessels/*/depth_range_mm` — zone 3/11 (있는 zone: 0=forehead, 1=glabella, 7=lips) | `/zones/0/vessels/0/depth_range_mm`, `/zones/0/vessels/1/depth_range_mm`, `/zones/1/vessels/0/depth_range_mm`, `/zones/7/vessels/0/depth_range_mm`, `/zones/7/vessels/1/depth_range_mm` |
| 선택 필드(일부 zone) | `/zones/*/vessels/*/depth_range_mm/*` — zone 3/11 (있는 zone: 0=forehead, 1=glabella, 7=lips) | `/zones/0/vessels/0/depth_range_mm/0`, `/zones/0/vessels/0/depth_range_mm/1`, `/zones/0/vessels/1/depth_range_mm/0`, `/zones/0/vessels/1/depth_range_mm/1`, `/zones/1/vessels/0/depth_range_mm/0`, `/zones/1/vessels/0/depth_range_mm/1`, `/zones/7/vessels/0/depth_range_mm/0`, `/zones/7/vessels/0/depth_range_mm/1`, `/zones/7/vessels/1/depth_range_mm/0`, `/zones/7/vessels/1/depth_range_mm/1` |
| 선택 필드(일부 zone) | `/zones/*/tissue_data/frontalis_thickness` — zone 1/11 (있는 zone: 0=forehead) | `/zones/0/tissue_data/frontalis_thickness` |
| 선택 필드(일부 zone) | `/zones/*/tissue_data/frontalis_thickness/midpupil_mm` — zone 1/11 (있는 zone: 0=forehead) | `/zones/0/tissue_data/frontalis_thickness/midpupil_mm` |
| 선택 필드(일부 zone) | `/zones/*/tissue_data/frontalis_thickness/lateral_canthus_mm` — zone 1/11 (있는 zone: 0=forehead) | `/zones/0/tissue_data/frontalis_thickness/lateral_canthus_mm` |
| 선택 필드(일부 zone) | `/zones/*/tissue_data/frontalis_thickness/lateral_orbital_rim_mm` — zone 1/11 (있는 zone: 0=forehead) | `/zones/0/tissue_data/frontalis_thickness/lateral_orbital_rim_mm` |
| 선택 필드(일부 zone) | `/zones/*/tissue_data/skin_to_periosteum_mm` — zone 1/11 (있는 zone: 0=forehead) | `/zones/0/tissue_data/skin_to_periosteum_mm` |
| 선택 필드(일부 zone) | `/zones/*/botox_specific/diffusion_range_cm` — zone 1/11 (있는 zone: 0=forehead) | `/zones/0/botox_specific/diffusion_range_cm` |
| 선택 필드(일부 zone) | `/zones/*/tissue_data/csm_mean_thickness_mm` — zone 1/11 (있는 zone: 1=glabella) | `/zones/1/tissue_data/csm_mean_thickness_mm` |
| 선택 필드(일부 zone) | `/zones/*/tissue_data/csm_thickness_variation_mm` — zone 1/11 (있는 zone: 1=glabella) | `/zones/1/tissue_data/csm_thickness_variation_mm` |
| 선택 필드(일부 zone) | `/zones/*/filler_specific/emergency_protocol` — zone 3/11 (있는 zone: 1=glabella, 3=periorbital, 4=nose) | `/zones/1/filler_specific/emergency_protocol`, `/zones/3/filler_specific/emergency_protocol`, `/zones/4/filler_specific/emergency_protocol` |
| 선택 필드(일부 zone) | `/zones/*/tissue_data/stl_entry_point` — zone 1/11 (있는 zone: 2=temple) | `/zones/2/tissue_data/stl_entry_point` |
| 선택 필드(일부 zone) | `/zones/*/tissue_data/pitanguy_line` — zone 1/11 (있는 zone: 2=temple) | `/zones/2/tissue_data/pitanguy_line` |
| 선택 필드(일부 zone) | `/zones/*/tissue_data/tear_trough_anatomy` — zone 1/11 (있는 zone: 3=periorbital) | `/zones/3/tissue_data/tear_trough_anatomy` |
| 선택 필드(일부 zone) | `/zones/*/tissue_data/muscle_fiber_data` — zone 1/11 (있는 zone: 3=periorbital) | `/zones/3/tissue_data/muscle_fiber_data` |
| 선택 필드(일부 zone) | `/zones/*/tissue_data/orbital_septum` — zone 1/11 (있는 zone: 3=periorbital) | `/zones/3/tissue_data/orbital_septum` |
| 선택 필드(일부 zone) | `/zones/*/tissue_data/rhinion_subcutaneous_mm` — zone 1/11 (있는 zone: 4=nose) | `/zones/4/tissue_data/rhinion_subcutaneous_mm` |
| 선택 필드(일부 zone) | `/zones/*/tissue_data/rhinion_data_source` — zone 1/11 (있는 zone: 4=nose) | `/zones/4/tissue_data/rhinion_data_source` |
| 선택 필드(일부 zone) | `/zones/*/tissue_data/nasal_tip_skin_thickness_mm` — zone 1/11 (있는 zone: 4=nose) | `/zones/4/tissue_data/nasal_tip_skin_thickness_mm` |
| 선택 필드(일부 zone) | `/zones/*/tissue_data/facial_artery_distance_to_nlf_mm` — zone 1/11 (있는 zone: 5=nasolabial) | `/zones/5/tissue_data/facial_artery_distance_to_nlf_mm` |
| 선택 필드(일부 zone) | `/zones/*/tissue_data/asian_adjacent_distribution_percent` — zone 1/11 (있는 zone: 5=nasolabial) | `/zones/5/tissue_data/asian_adjacent_distribution_percent` |
| 선택 필드(일부 zone) | `/zones/*/tissue_data/within_5mm_percent` — zone 1/11 (있는 zone: 5=nasolabial) | `/zones/5/tissue_data/within_5mm_percent` |
| 선택 필드(일부 zone) | `/zones/*/tissue_data/facial_artery_diameter_mandible_mm` — zone 1/11 (있는 zone: 5=nasolabial) | `/zones/5/tissue_data/facial_artery_diameter_mandible_mm` |
| 선택 필드(일부 zone) | `/zones/*/tissue_data/facial_artery_diameter_nasal_mm` — zone 1/11 (있는 zone: 5=nasolabial) | `/zones/5/tissue_data/facial_artery_diameter_nasal_mm` |
| 선택 필드(일부 zone) | `/zones/*/tissue_data/buccal_fat_pad` — zone 1/11 (있는 zone: 6=cheek) | `/zones/6/tissue_data/buccal_fat_pad` |
| 선택 필드(일부 zone) | `/zones/*/tissue_data/smas_depth_mm` — zone 1/11 (있는 zone: 6=cheek) | `/zones/6/tissue_data/smas_depth_mm` |
| 선택 필드(일부 zone) | `/zones/*/tissue_data/sub_smas_vs_subcutaneous` — zone 1/11 (있는 zone: 6=cheek) | `/zones/6/tissue_data/sub_smas_vs_subcutaneous` |
| 선택 필드(일부 zone) | `/zones/*/tissue_data/labial_artery_depth_range_mm` — zone 1/11 (있는 zone: 7=lips) | `/zones/7/tissue_data/labial_artery_depth_range_mm` |
| 선택 필드(일부 zone) | `/zones/*/tissue_data/labial_artery_depth_range_mm/*` — zone 1/11 (있는 zone: 7=lips) | `/zones/7/tissue_data/labial_artery_depth_range_mm/0`, `/zones/7/tissue_data/labial_artery_depth_range_mm/1` |
| 선택 필드(일부 zone) | `/zones/*/tissue_data/superior_labial_artery_submucosal_percent` — zone 1/11 (있는 zone: 7=lips) | `/zones/7/tissue_data/superior_labial_artery_submucosal_percent` |
| 선택 필드(일부 zone) | `/zones/*/tissue_data/mental_foramen_location` — zone 1/11 (있는 zone: 8=chin) | `/zones/8/tissue_data/mental_foramen_location` |
| 선택 필드(일부 zone) | `/zones/*/tissue_data/dao_coverage` — zone 1/11 (있는 zone: 8=chin) | `/zones/8/tissue_data/dao_coverage` |
| 선택 필드(일부 zone) | `/zones/*/tissue_data/marginal_mandibular_depth` — zone 1/11 (있는 zone: 9=jawline) | `/zones/9/tissue_data/marginal_mandibular_depth` |
| 선택 필드(일부 zone) | `/zones/*/tissue_data/facial_artery_crossing` — zone 1/11 (있는 zone: 9=jawline) | `/zones/9/tissue_data/facial_artery_crossing` |
| 선택 필드(일부 zone) | `/zones/*/tissue_data/platysma_thickness_mm` — zone 1/11 (있는 zone: 10=neck) | `/zones/10/tissue_data/platysma_thickness_mm` |
| 선택 필드(일부 zone) | `/zones/*/tissue_data/platysma_coverage` — zone 1/11 (있는 zone: 10=neck) | `/zones/10/tissue_data/platysma_coverage` |
| `vessels` 원소 키 구성 변형 | `name`, `depth_mm`, `diameter_mm`, `course`, `danger`, `note`, `depth_range_mm` | `/zones/0/vessels/0`, `/zones/0/vessels/1` |
| `vessels` 원소 키 구성 변형 | `name`, `depth_mm`, `diameter_mm`, `course`, `danger`, `depth_range_mm` | `/zones/1/vessels/0` |
| `vessels` 원소 키 구성 변형 | `name`, `depth_mm`, `diameter_mm`, `course`, `danger` | `/zones/1/vessels/1`, `/zones/2/vessels/0`, `/zones/2/vessels/1`, `/zones/3/vessels/0`, `/zones/3/vessels/1`, `/zones/3/vessels/2`, `/zones/4/vessels/0`, `/zones/4/vessels/1`, `/zones/4/vessels/2`, `/zones/5/vessels/0`, `/zones/5/vessels/1`, `/zones/6/vessels/0`, `/zones/6/vessels/1`, `/zones/8/vessels/0`, `/zones/8/vessels/1`, `/zones/9/vessels/0`, `/zones/9/vessels/1`, `/zones/10/vessels/0`, `/zones/10/vessels/1` |
| `vessels` 원소 키 구성 변형 | `name`, `diameter_mm`, `course`, `danger`, `depth_range_mm` | `/zones/7/vessels/0`, `/zones/7/vessels/1` |
| `tissue_data` 키 구성(zone 마다 다름) | `frontalis_thickness`, `skin_to_periosteum_mm`, `notes` | `/zones/0/tissue_data` |
| `tissue_data` 키 구성(zone 마다 다름) | `csm_mean_thickness_mm`, `csm_thickness_variation_mm`, `notes` | `/zones/1/tissue_data` |
| `tissue_data` 키 구성(zone 마다 다름) | `stl_entry_point`, `pitanguy_line`, `notes` | `/zones/2/tissue_data` |
| `tissue_data` 키 구성(zone 마다 다름) | `tear_trough_anatomy`, `muscle_fiber_data`, `orbital_septum`, `notes` | `/zones/3/tissue_data` |
| `tissue_data` 키 구성(zone 마다 다름) | `rhinion_subcutaneous_mm`, `rhinion_data_source`, `nasal_tip_skin_thickness_mm`, `notes` | `/zones/4/tissue_data` |
| `tissue_data` 키 구성(zone 마다 다름) | `facial_artery_distance_to_nlf_mm`, `asian_adjacent_distribution_percent`, `within_5mm_percent`, `facial_artery_diameter_mandible_mm`, `facial_artery_diameter_nasal_mm`, `notes` | `/zones/5/tissue_data` |
| `tissue_data` 키 구성(zone 마다 다름) | `buccal_fat_pad`, `smas_depth_mm`, `sub_smas_vs_subcutaneous`, `notes` | `/zones/6/tissue_data` |
| `tissue_data` 키 구성(zone 마다 다름) | `labial_artery_depth_range_mm`, `superior_labial_artery_submucosal_percent`, `notes` | `/zones/7/tissue_data` |
| `tissue_data` 키 구성(zone 마다 다름) | `mental_foramen_location`, `dao_coverage`, `notes` | `/zones/8/tissue_data` |
| `tissue_data` 키 구성(zone 마다 다름) | `marginal_mandibular_depth`, `facial_artery_crossing`, `notes` | `/zones/9/tissue_data` |
| `tissue_data` 키 구성(zone 마다 다름) | `platysma_thickness_mm`, `platysma_coverage`, `notes` | `/zones/10/tissue_data` |
| 숫자 범위를 문자열로 | `diffusion_range_cm` = "1.5-3.0" (string) | `/zones/0/botox_specific/diffusion_range_cm` |
| 숫자 배열 | `depth_range_mm`, `labial_artery_depth_range_mm` = [하한, 상한] 2원소 숫자 배열 | 컬럼 구성 표 참조 |

### 같은 문자열의 반복 출현(각 위치 유지)

| 원문 값 | Pointer 들 |
|---|---|
| orange | `/zones/0/danger_color`, `/zones/2/danger_color`, `/zones/5/danger_color`, `/zones/9/danger_color` |
| 활차상동맥 (Supratrochlear artery) | `/zones/0/vessels/0/name`, `/zones/1/vessels/0/name` |
| 활차상신경 (Supratrochlear nerve) | `/zones/0/nerves/0/name`, `/zones/1/nerves/0/name` |
| sensory | `/zones/0/nerves/0/type`, `/zones/0/nerves/1/type`, `/zones/1/nerves/0/type`, `/zones/2/nerves/1/type`, `/zones/3/nerves/0/type`, `/zones/3/nerves/1/type`, `/zones/4/nerves/0/type`, `/zones/4/nerves/1/type`, `/zones/5/nerves/0/type`, `/zones/6/nerves/0/type`, `/zones/7/nerves/0/type`, `/zones/7/nerves/1/type`, `/zones/8/nerves/0/type`, `/zones/9/nerves/1/type`, `/zones/10/nerves/0/type` |
| 이마 피부-골막 거리 평균 0.5cm — 매우 얇음 | `/zones/0/tissue_data/notes`, `/zones/0/clinical_pearls/0` |
| red | `/zones/1/danger_color`, `/zones/3/danger_color`, `/zones/4/danger_color` |
| 배비동맥 (Dorsal nasal artery) | `/zones/1/vessels/1/name`, `/zones/4/vessels/0/name` |
| motor | `/zones/2/nerves/0/type`, `/zones/5/nerves/1/type`, `/zones/6/nerves/1/type`, `/zones/6/nerves/2/type`, `/zones/9/nerves/0/type`, `/zones/10/nerves/1/type` |
| 각동맥 (Angular artery) | `/zones/3/vessels/0/name`, `/zones/5/vessels/1/name` |
| 안와하신경 (Infraorbital nerve) | `/zones/3/nerves/0/name`, `/zones/5/nerves/0/name`, `/zones/6/nerves/0/name` |
| 안면동맥 (Facial artery) | `/zones/5/vessels/0/name`, `/zones/9/vessels/0/name` |
| 안면동맥 분지가 NLF 인접부에 존재 93.3%; 이 중 NLF 5mm 이내 주행은 약 42.9% | `/zones/5/vessels/0/course`, `/zones/5/clinical_pearls/0` |
| 협근신경 (Buccal branch of facial nerve) | `/zones/5/nerves/1/name`, `/zones/6/nerves/1/name` |
| yellow | `/zones/6/danger_color`, `/zones/7/danger_color`, `/zones/8/danger_color` |
| 이신경 (Mental nerve) | `/zones/8/nerves/0/name`, `/zones/9/nerves/1/name` |

## 구획 목차

| 구획 | 범위 | 소유 노드/말단 | 직접 읽기 | 파일 |
|---|---|---|---|---|
| S00 | 최상위 메타데이터 + critical_safety_facts + zones 배열 컨테이너 — `'' (루트 객체 자체), /version, /updated, /consensus_method, /critical_safety_facts/**, /zones (배열 컨테이너만; 원소는 S01~S11)` | 10 / 7 | done | [review-part-S00.md](review-part-S00.md) |
| S01 | zones[0] forehead (이마 / Forehead) — `/zones/0/**` | 62 / 48 | done | [review-part-S01.md](review-part-S01.md) |
| S02 | zones[1] glabella (미간 / Glabella) — `/zones/1/**` | 52 / 41 | done | [review-part-S02.md](review-part-S02.md) |
| S03 | zones[2] temple (관자놀이 / Temple) — `/zones/2/**` | 53 / 42 | done | [review-part-S03.md](review-part-S03.md) |
| S04 | zones[3] periorbital (눈 주변 / Periorbital) — `/zones/3/**` | 59 / 47 | done | [review-part-S04.md](review-part-S04.md) |
| S05 | zones[4] nose (코 / Nose) — `/zones/4/**` | 61 / 49 | done | [review-part-S05.md](review-part-S05.md) |
| S06 | zones[5] nasolabial (팔자주름 / Nasolabial Fold) — `/zones/5/**` | 54 / 43 | done | [review-part-S06.md](review-part-S06.md) |
| S07 | zones[6] cheek (볼 / Cheek (Malar/Buccal)) — `/zones/6/**` | 56 / 44 | done | [review-part-S07.md](review-part-S07.md) |
| S08 | zones[7] lips (입술 / Lips) — `/zones/7/**` | 58 / 44 | done | [review-part-S08.md](review-part-S08.md) |
| S09 | zones[8] chin (턱 / Chin (Mentum)) — `/zones/8/**` | 47 / 37 | done | [review-part-S09.md](review-part-S09.md) |
| S10 | zones[9] jawline (턱선 / Jawline (Mandibular border)) — `/zones/9/**` | 52 / 41 | done | [review-part-S10.md](review-part-S10.md) |
| S11 | zones[10] neck (목 / Neck) — `/zones/10/**` | 51 / 40 | done | [review-part-S11.md](review-part-S11.md) |

## 산출물

| 파일 | 내용 |
|---|---|
| source-map.json | 모든 노드의 Pointer·자료형·원문 값·리터럴 구간(코드 포인트/바이트)·문맥 참조·필드명 출현·중복 문자열 |
| morphology.json | Kiwi 원시 분석(텍스트 값·필드명), 제외 내역, 전문어 분절·수치·단서 관찰 |
| expressions.json | 수동 복합 표현, 정규식 후보, 절 구간 |
| coverage.json | 구획별 소유 경로·읽기 상태 |
| manual-review.json | 직접 읽기 기록(관찰·수동 표현) — build.py 입력 |
| issues.md | 미결·후속 목록(A/B/C/I/P/F/K) |
| validation.md | 기계 검증 명령·결과, 읽기 검토 |
| build.py / verify.py | 재현 / 독립 검증 |
