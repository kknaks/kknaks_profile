# S03 — zones[2] temple (관자놀이 / Temple)

[← review.md](review.md) · 범위 `/zones/2/**` · 소유 노드 53 · 말단 42 · 직접 읽기 done

상위 문맥: 루트 객체 → `zones` 배열(S00 소유) → `/zones/2` (id=`temple`, name_ko=`관자놀이`, name_en=`Temple`).

## 원문 값 (문서 순서 · 전부)

| # | JSON Pointer | 원본 컬럼명 | 배열 순번 | 자료형 | 원문 값 |
|---|---|---|---|---|---|
| 124 | `/zones/2` | `(zones 원소)` | 2 | object{12} | (컨테이너 · 키: `id`, `name_ko`, `name_en`, `danger_level`, `danger_color`, `vessels`, `nerves`, `safe_injection_depth`, `tissue_data`, `clinical_pearls`, `botox_specific`, `filler_specific`) |
| 125 | `/zones/2/id` | `id` |  | string | temple |
| 126 | `/zones/2/name_ko` | `name_ko` |  | string | 관자놀이 |
| 127 | `/zones/2/name_en` | `name_en` |  | string | Temple |
| 128 | `/zones/2/danger_level` | `danger_level` |  | integer | `4` |
| 129 | `/zones/2/danger_color` | `danger_color` |  | string | orange |
| 130 | `/zones/2/vessels` | `vessels` |  | array[2] | (배열 · 2개) |
| 131 | `/zones/2/vessels/0` | `(vessels 원소)` | 0 | object{5} | (컨테이너 · 키: `name`, `depth_mm`, `diameter_mm`, `course`, `danger`) |
| 132 | `/zones/2/vessels/0/name` | `name` |  | string | 천측두동맥 (Superficial temporal artery) |
| 133 | `/zones/2/vessels/0/depth_mm` | `depth_mm` |  | number | `3.0` |
| 134 | `/zones/2/vessels/0/diameter_mm` | `diameter_mm` |  | number | `1.5` |
| 135 | `/zones/2/vessels/0/course` | `course` |  | string | 이주(tragus) 전방에서 상방 주행, 측두근막 표면 |
| 136 | `/zones/2/vessels/0/danger` | `danger` |  | string | 직경 1-2mm의 굵은 동맥 — 천자 시 대량 출혈, 혈종 |
| 137 | `/zones/2/vessels/1` | `(vessels 원소)` | 1 | object{5} | (컨테이너 · 키: `name`, `depth_mm`, `diameter_mm`, `course`, `danger`) |
| 138 | `/zones/2/vessels/1/name` | `name` |  | string | 측두동맥 중간가지 (Middle temporal artery) |
| 139 | `/zones/2/vessels/1/depth_mm` | `depth_mm` |  | number | `6.0` |
| 140 | `/zones/2/vessels/1/diameter_mm` | `diameter_mm` |  | number | `1.0` |
| 141 | `/zones/2/vessels/1/course` | `course` |  | string | 심부측두근막 내 주행 |
| 142 | `/zones/2/vessels/1/danger` | `danger` |  | string | 깊은 층 주사 시 손상 위험 |
| 143 | `/zones/2/nerves` | `nerves` |  | array[2] | (배열 · 2개) |
| 144 | `/zones/2/nerves/0` | `(nerves 원소)` | 0 | object{3} | (컨테이너 · 키: `name`, `type`, `significance`) |
| 145 | `/zones/2/nerves/0/name` | `name` |  | string | 측두신경 (Temporal branch of facial nerve) |
| 146 | `/zones/2/nerves/0/type` | `type` |  | string | motor |
| 147 | `/zones/2/nerves/0/significance` | `significance` |  | string | 전두근 운동 — 손상 시 이마 거상 불가, 눈썹 처짐 |
| 148 | `/zones/2/nerves/1` | `(nerves 원소)` | 1 | object{3} | (컨테이너 · 키: `name`, `type`, `significance`) |
| 149 | `/zones/2/nerves/1/name` | `name` |  | string | 이개측두신경 (Auriculotemporal nerve) |
| 150 | `/zones/2/nerves/1/type` | `type` |  | string | sensory |
| 151 | `/zones/2/nerves/1/significance` | `significance` |  | string | 측두부 감각 |
| 152 | `/zones/2/safe_injection_depth` | `safe_injection_depth` |  | string | 심부측두근막 심층 (deep temporal fascia deep layer) 또는 골막상 |
| 153 | `/zones/2/tissue_data` | `tissue_data` |  | object{3} | (컨테이너 · 키: `stl_entry_point`, `pitanguy_line`, `notes`) |
| 154 | `/zones/2/tissue_data/stl_entry_point` | `stl_entry_point` |  | string | STL(상측두융합선, Superior temporal line)에서 측두근막이 두 층으로 분리 |
| 155 | `/zones/2/tissue_data/pitanguy_line` | `pitanguy_line` |  | string | 이주(tragus) 하부 0.5cm → 눈썹 외측 1.5cm 상방을 잇는 선 위에 측두신경 주행 |
| 156 | `/zones/2/tissue_data/notes` | `notes` |  | string | Pitanguy line 위에서 안면신경 측두분지가 표재성으로 주행 — 이 선 위 피하층 주사 주의 |
| 157 | `/zones/2/clinical_pearls` | `clinical_pearls` |  | array[7] | (배열 · 7개) |
| 158 | `/zones/2/clinical_pearls/0` | `(clinical_pearls 원소)` | 0 | string | 천측두동맥은 촉진 가능 — 주사 전 반드시 촉진으로 위치 확인 |
| 159 | `/zones/2/clinical_pearls/1` | `(clinical_pearls 원소)` | 1 | string | Pitanguy line 위에서 안면신경 측두분지가 표재성 주행 |
| 160 | `/zones/2/clinical_pearls/2` | `(clinical_pearls 원소)` | 2 | string | STL(상측두융합선)에서 측두근막이 두 층으로 분리 → 층 확인 중요 |
| 161 | `/zones/2/clinical_pearls/3` | `(clinical_pearls 원소)` | 3 | string | 측두근 위축(관자놀이 함몰) 교정 시 심부 주사 필수 |
| 162 | `/zones/2/clinical_pearls/4` | `(clinical_pearls 원소)` | 4 | string | 표재성 주사 시 혈종 + 안면신경 손상 동시 위험 |
| 163 | `/zones/2/clinical_pearls/5` | `(clinical_pearls 원소)` | 5 | string | 관자놀이도 실명 위험 부위 — 저압·소량·캐뉼러로 주입하고 색전 시 안과 응급 프로토콜 준용 |
| 164 | `/zones/2/clinical_pearls/6` | `(clinical_pearls 원소)` | 6 | string | 중측두정맥은 관자궁 상방 약 2cm에서 대구경으로 주행하므로 정맥 색전 주의 |
| 165 | `/zones/2/botox_specific` | `botox_specific` |  | object{5} | (컨테이너 · 키: `target_muscle`, `risk`, `safe_zone`, `key_warning`, `dose_range`) |
| 166 | `/zones/2/botox_specific/target_muscle` | `target_muscle` |  | string | 측두근 (Temporalis) — 이갈이/사각턱 보조 |
| 167 | `/zones/2/botox_specific/risk` | `risk` |  | string | 측두부 함몰(과도 위축), 씹는 힘 약화 |
| 168 | `/zones/2/botox_specific/safe_zone` | `safe_zone` |  | string | 측두근 중앙부, 깊은 층 |
| 169 | `/zones/2/botox_specific/key_warning` | `key_warning` |  | string | 표재성 주사 → 안면신경 측두분지 마비 → 이마 거상 불가 |
| 170 | `/zones/2/botox_specific/dose_range` | `dose_range` |  | string | 20-40U/측 (이갈이), 관자놀이 필러와 병행 시 주의 |
| 171 | `/zones/2/filler_specific` | `filler_specific` |  | object{5} | (컨테이너 · 키: `risk_level`, `primary_risk`, `safe_technique`, `max_per_point_ml`, `preferred_product`) |
| 172 | `/zones/2/filler_specific/risk_level` | `risk_level` |  | integer | `4` |
| 173 | `/zones/2/filler_specific/primary_risk` | `primary_risk` |  | string | 천측두동맥-안동맥 및 심부측두동맥-안동맥 문합 경로를 통한 역행성 색전 → 시력손실/실명, 천측두동맥 천자 → 대량 출혈/혈종, 안면신경 손상 |
| 174 | `/zones/2/filler_specific/safe_technique` | `safe_technique` |  | string | 심부측두근막 심층 캐뉼러 주입, 동맥 촉진 후 주사 |
| 175 | `/zones/2/filler_specific/max_per_point_ml` | `max_per_point_ml` |  | number | `0.2` |
| 176 | `/zones/2/filler_specific/preferred_product` | `preferred_product` |  | string | 실명 위험 부위이므로 비가역적 CaHA보다 용해 가능한 HA를 우선 고려. CaHA 사용 시 심부 골막상·저압·소량 주입하며, 응급 hyaluronidase는 HA 성분에만 유효함 |

## 잠정 관찰 (원문 칸과 분리)

| # | 상태 | 근거 Pointer | 관찰 | issues.md |
|---|---|---|---|---|
| OBS-S03-01 | P | `/zones/2/vessels/0/diameter_mm`, `/zones/2/vessels/0/danger` | diameter_mm 1.5 와 danger 의 '직경 1-2mm' 가 같은 값 안팎에서 점값/범위로 적혀 있다. |  |
| OBS-S03-02 | F | `/zones/2/nerves/0/name`, `/zones/2/clinical_pearls/1`, `/zones/2/botox_specific/key_warning` | nerves 이름은 '측두신경 (Temporal branch of facial nerve)', pearls·key_warning 은 '안면신경 측두분지' 다. 같은 대상인지 후속. | ADZ-F13 |
| OBS-S03-03 | P | `/zones/2/tissue_data/pitanguy_line` | 여기 '→' 는 인과가 아니라 두 기준점을 잇는 선(A 지점 → B 지점)이다. | ADZ-P09 |
| OBS-S03-04 | F | `/zones/2/clinical_pearls/6` | '관자궁' 은 원장 다른 곳(cheek '관골궁')과 표기가 다르다. 오기 여부는 원문 확인 후보이며 원본은 그대로 둔다. '중측두정맥' 은 vessels 목록(측두동맥 중간가지)에 없다. | ADZ-F06 |
| OBS-S03-05 | F | `/zones/2/filler_specific/primary_risk` | '심부측두동맥' 은 이 zone vessels 목록에 없다. | ADZ-P21 |
| OBS-S03-06 | F | `/zones/2/clinical_pearls/5`, `/zones/2/botox_specific/dose_range` | '안과 응급 프로토콜 준용', '관자놀이 필러와 병행 시 주의' 는 다른 필드/다른 시술을 가리키는 참조 표현이다. temple 에는 emergency_protocol 필드가 없다. | ADZ-F14 |
| OBS-S03-07 | P | `/zones/2/botox_specific/target_muscle` | 관자놀이 zone 의 botox 대상 설명에 '이갈이/사각턱 보조' 가 붙어 다른 부위 적응을 언급한다. | ADZ-F14 |

## 수동 복합 표현 (직접 읽기)

탐색 관점은 수집용 꼬리표이며 확정 분류가 아니다. 구간은 값 문자열 기준 코드 포인트 `[start,end)`.

| ID | Pointer | 원문 구간 | 구간 | 탐색 관점 | 메모 |
|---|---|---|---|---|---|
| MX-S03-001 | `/zones/2/vessels/0/course` | 이주(tragus) 전방에서 상방 주행, 측두근막 표면 | [0, 30] | 위치·방향, 영문 병기 |  |
| MX-S03-002 | `/zones/2/vessels/0/danger` | 직경 1-2mm의 굵은 동맥 | [0, 15] | 범위, 수식(굵은) |  |
| MX-S03-003 | `/zones/2/vessels/0/danger` | 천자 시 대량 출혈, 혈종 | [18, 32] | 조건(시), 결과 |  |
| MX-S03-004 | `/zones/2/vessels/1/name` | 측두동맥 중간가지 (Middle temporal artery) | [0, 34] | 혈관명, 영문 병기 |  |
| MX-S03-005 | `/zones/2/vessels/1/danger` | 깊은 층 주사 시 손상 위험 | [0, 15] | 수식(깊은), 조건(시) |  |
| MX-S03-006 | `/zones/2/nerves/0/name` | 측두신경 (Temporal branch of facial nerve) | [0, 38] | 신경명, 영문 병기 |  |
| MX-S03-007 | `/zones/2/nerves/0/significance` | 손상 시 이마 거상 불가, 눈썹 처짐 | [9, 29] | 조건(시), 불가 |  |
| MX-S03-008 | `/zones/2/safe_injection_depth` | 심부측두근막 심층 (deep temporal fascia deep layer) 또는 골막상 | [0, 50] | 층, 대안(또는) |  |
| MX-S03-009 | `/zones/2/tissue_data/stl_entry_point` | STL(상측두융합선, Superior temporal line)에서 측두근막이 두 층으로 분리 | [0, 52] | 약어·병기, 해부 관계 |  |
| MX-S03-010 | `/zones/2/tissue_data/pitanguy_line` | 이주(tragus) 하부 0.5cm → 눈썹 외측 1.5cm 상방을 잇는 선 | [0, 42] | 거리, 선 정의(→ 는 지점 연결) |  |
| MX-S03-011 | `/zones/2/tissue_data/notes` | 이 선 위 피하층 주사 주의 | [40, 55] | 지시 표현(이 선), 주의 |  |
| MX-S03-012 | `/zones/2/clinical_pearls/0` | 주사 전 반드시 촉진으로 위치 확인 | [15, 34] | 시간(전), 필수(반드시) |  |
| MX-S03-013 | `/zones/2/clinical_pearls/2` | STL(상측두융합선)에서 측두근막이 두 층으로 분리 → 층 확인 중요 | [0, 38] | 결과(→) |  |
| MX-S03-014 | `/zones/2/clinical_pearls/3` | 측두근 위축(관자놀이 함몰) 교정 시 심부 주사 필수 | [0, 29] | 조건(시), 필수 |  |
| MX-S03-015 | `/zones/2/clinical_pearls/4` | 표재성 주사 시 혈종 + 안면신경 손상 동시 위험 | [0, 27] | 조건(시), 기호(+), 동시 |  |
| MX-S03-016 | `/zones/2/clinical_pearls/5` | 관자놀이도 실명 위험 부위 | [0, 14] | 보조사(도) |  |
| MX-S03-017 | `/zones/2/clinical_pearls/5` | 색전 시 안과 응급 프로토콜 준용 | [33, 51] | 조건(시), 참조(준용) |  |
| MX-S03-018 | `/zones/2/clinical_pearls/6` | 중측두정맥은 관자궁 상방 약 2cm에서 대구경으로 주행하므로 정맥 색전 주의 | [0, 42] | 거리, 근사(약), 이유(므로), 주의 |  |
| MX-S03-019 | `/zones/2/botox_specific/target_muscle` | 측두근 (Temporalis) — 이갈이/사각턱 보조 | [0, 29] | 근육명, 기호(/), 보조 |  |
| MX-S03-020 | `/zones/2/botox_specific/risk` | 측두부 함몰(과도 위축) | [0, 13] | 정도(과도) |  |
| MX-S03-021 | `/zones/2/botox_specific/risk` | 씹는 힘 약화 | [15, 22] | 기능 저하 |  |
| MX-S03-022 | `/zones/2/botox_specific/key_warning` | 표재성 주사 → 안면신경 측두분지 마비 → 이마 거상 불가 | [0, 32] | 연쇄(→), 불가 |  |
| MX-S03-023 | `/zones/2/botox_specific/dose_range` | 20-40U/측 (이갈이) | [0, 14] | 범위, 단위당, 적응 한정 |  |
| MX-S03-024 | `/zones/2/botox_specific/dose_range` | 관자놀이 필러와 병행 시 주의 | [16, 32] | 조건(병행 시), 참조 |  |
| MX-S03-025 | `/zones/2/filler_specific/primary_risk` | 천측두동맥-안동맥 및 심부측두동맥-안동맥 문합 경로를 통한 역행성 색전 → 시력손실/실명 | [0, 49] | 경로(연결 하이픈), 결과(→), 기호(/) |  |
| MX-S03-026 | `/zones/2/filler_specific/primary_risk` | 천측두동맥 천자 → 대량 출혈/혈종 | [51, 70] | 결과(→), 기호(/) |  |
| MX-S03-027 | `/zones/2/filler_specific/safe_technique` | 심부측두근막 심층 캐뉼러 주입, 동맥 촉진 후 주사 | [0, 28] | 층, 순서(후) |  |
| MX-S03-028 | `/zones/2/filler_specific/preferred_product` | 실명 위험 부위이므로 비가역적 CaHA보다 용해 가능한 HA를 우선 고려 | [0, 40] | 이유(이므로), 비교(보다), 우선 |  |
| MX-S03-029 | `/zones/2/filler_specific/preferred_product` | CaHA 사용 시 심부 골막상·저압·소량 주입하며 | [42, 69] | 조건(시), 기법 |  |
| MX-S03-030 | `/zones/2/filler_specific/preferred_product` | 응급 hyaluronidase는 HA 성분에만 유효함 | [71, 100] | 한정(만) |  |
| MX-S03-031 | `/zones/2/clinical_pearls/1` | Pitanguy line 위에서 안면신경 측두분지가 표재성 주행 | [0, 35] | 참조(Pitanguy line = tissue_data.pitanguy_line), 위치 |  |
| MX-S03-032 | `/zones/2/botox_specific/safe_zone` | 측두근 중앙부, 깊은 층 | [0, 13] | 위치, 수식(깊은) |  |

## 정규식 보조 후보 (기계 · 요약)

| 패턴 | 출현 |
|---|---|
| range | 2 |
| number_unit | 5 |
| condition | 8 |
| em_dash | 6 |
| negation_prohibition | 2 |
| arrow | 6 |
| possibility_frequency | 2 |
| time_order | 2 |
| degree_emphasis | 3 |
| plus | 1 |
| middle_dot | 4 |
| slash | 4 |

전체 출현·구간은 `expressions.json` → `regex_candidates` (section=S03).

## 전문어 분절 관찰 (Kiwi 원시 · K)

| Pointer | 낱말 | 구간 | Kiwi 토큰 | 상태 |
|---|---|---|---|---|
| `/zones/2/tissue_data/notes` | 측두분지 | [23, 27] | 측두/NNG + 분지/NNG | K: 여러 형태소로 분절(원시 결과 보존) |
| `/zones/2/tissue_data/notes` | 표재성 | [29, 32] | 표재/NNG + 성/XSN | K: 여러 형태소로 분절(원시 결과 보존) |
| `/zones/2/clinical_pearls/0` | 천측두동맥 | [0, 5] | 천/NR + 측두/NNG + 동맥/NNG | K: 여러 형태소로 분절(원시 결과 보존) |
| `/zones/2/clinical_pearls/1` | 측두분지 | [23, 27] | 측두/NNG + 분지/NNG | K: 여러 형태소로 분절(원시 결과 보존) |
| `/zones/2/clinical_pearls/1` | 표재성 | [29, 32] | 표재/NNG + 성/XSN | K: 여러 형태소로 분절(원시 결과 보존) |
| `/zones/2/clinical_pearls/4` | 표재성 | [0, 3] | 표재/NNG + 성/XSN | K: 여러 형태소로 분절(원시 결과 보존) |
| `/zones/2/clinical_pearls/6` | 관자궁 | [7, 10] | 관/NNG + 자궁/NNG | K: 여러 형태소로 분절(원시 결과 보존) |
| `/zones/2/botox_specific/key_warning` | 측두분지 | [14, 18] | 측두/NNG + 분지/NNG | K: 여러 형태소로 분절(원시 결과 보존) |
| `/zones/2/botox_specific/key_warning` | 표재성 | [0, 3] | 표재/NNG + 성/XSN | K: 여러 형태소로 분절(원시 결과 보존) |
| `/zones/2/filler_specific/primary_risk` | 천측두동맥 | [0, 5] | 천/NR + 측두/NNG + 동맥/NNG | K: 여러 형태소로 분절(원시 결과 보존) |
| `/zones/2/filler_specific/primary_risk` | 천측두동맥 | [51, 56] | 천/NR + 측두/NNG + 동맥/NNG | K: 여러 형태소로 분절(원시 결과 보존) |
| `/zones/2/filler_specific/primary_risk` | 역행성 | [33, 36] | 역행/NNG + 성/XSN | K: 여러 형태소로 분절(원시 결과 보존) |
| `/zones/2/filler_specific/primary_risk` | 심부측두동맥 | [12, 18] | 심부/NNG + 측두/NNG + 동맥/NNG | K: 여러 형태소로 분절(원시 결과 보존) |

단일 형태소로 나온 출현은 표에서 생략했다(`morphology.json` → `segmentation_review` 에 전부 있음).

