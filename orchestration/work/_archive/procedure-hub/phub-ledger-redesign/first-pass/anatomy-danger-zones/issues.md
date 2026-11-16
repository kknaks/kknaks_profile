# anatomy-danger-zones.json — 미결·후속 목록

상태 문자: **A**=에이전트 추출/해석 오류, **B**=원문 정보 부족, **C**=현재 사용자 결정 필요,
**I**=원문 내 불일치(후보), **P**=잠정 관찰, **F**=후속 의미 조사, **K**=알려진 분석 한계.
원본 변경 제안은 현재 원본 보존 지시 아래 **후속 확인 후보**일 뿐이며 선택 대기로 올리지 않는다.
원문 위치는 JSON Pointer, 상세 구간은 `expressions.json`·`morphology.json`. 임상적 옳고 그름은 판단하지 않았다.

## 상태 요약

| 상태 | 건수 | 처리 상태 |
|---|---|---|
| A | 0 열림 | 작업 중 생긴 추출 오류 3건은 고쳤고 재검증했다(아래 「해결된 A」) |
| B | 5 | 열림 — 원문에 없는 정보. 지금 채우지 않는다 |
| C | 0 | 아래 「사용자 결정 0 의 근거」 참고 |
| I | 4 | 열림 — 원문 대조 후보. 원본은 그대로 둔다 |
| P | 11 | 기록됨 — 의미 확정 아님 |
| F | 3 | 열림 — 후속 의미 조사·원장 간 비교 단계 |
| K | 5 묶음 | 기록됨 — 출현별 원시 결과는 morphology.json |

## I — 원문 내 불일치 후보

### ADZ-I01 — 최고 위험 부위 표현
- `/zones/1/filler_specific/primary_risk` = 「역행성 색전 → 실명 (최고 위험)」(미간)
- `/critical_safety_facts/blindness_highest_risk_zones` = 「… — 코가 현재 최고위험부위」
- `/zones/4/clinical_pearls/0` = 「실명 원인 부위 1위 — 최신 문헌에서 코가 글라벨라를 제치고 최다 부위 …」
- 영향: 부위 간 순위를 원문에서 뽑으면 서로 맞지 않는다. 「최고 위험」이 순위를 뜻하는지, 위험 등급(risk_level 5)을 뜻하는지 원문에 없다. danger_level·risk_level 은 미간·코 모두 5다.
- 다음 단계: 후속 의미 조사(F). 원본 문구 확인 후보.

### ADZ-I02 — 「비근근」 한 표기에 두 영문 근육명
- `/zones/1/botox_specific/target_muscle` 「…, 비근근 (Procerus)」 / `/zones/1/botox_specific/dose_range` 「비근근 5-10U」
- `/zones/4/botox_specific/target_muscle` 「비근근 (Nasalis) — …」 / `/zones/4/botox_specific/key_warning` 「비근근 외측 과다 주사 → …」
- 영향: 한글 표기만으로 근육을 묶으면 두 대상이 하나로 합쳐질 수 있다. 영문 병기를 같이 보존해야 한다.
- 다음 단계: 공통 개념 단계에서 확인(F). 원본 표기 확인 후보.

### ADZ-I03 — 입술 안전 깊이 「점막하」
- `/zones/7/safe_injection_depth` 「점막-피부 경계(vermillion border) 진피 내 또는 점막하」
- `/zones/7/tissue_data/notes` 「… 구각부 심부·정중/중간 vermillion 점막하 주입은 동맥 손상 위험이 높아 금지」
- 영향: 「점막하」가 안전 깊이와 금지 대상 양쪽에 나온다. 적용 범위(부위 한정)가 다른 것인지 원문만으로 정할 수 없다.
- 다음 단계: 후속 의미 조사(F). 원본 문구 확인 후보.

### ADZ-I04 — 하악변연신경 20% 범위 표현
- `/zones/9/tissue_data/marginal_mandibular_depth` 「… (20% 환자에서 하악연 하방 1cm까지)」
- `/zones/9/clinical_pearls/2` 「… (20%는 1cm 하방)」
- 영향: 「1cm까지」(상한)와 「1cm 하방」(위치)이 같은 20% 에 붙어 범위 해석이 갈린다.
- 다음 단계: 후속 의미 조사(F).

## B — 원문 정보 부족

### ADZ-B05 — 입술 tissue_data 깊이 범위가 어느 혈관 기준인지
- `/zones/7/tissue_data/labial_artery_depth_range_mm` [3.0, 6.0] = `/zones/7/vessels/1/depth_range_mm`(하순동맥) [3.0, 6.0]; `/zones/7/vessels/0/depth_range_mm`(상순동맥) [3.2, 5.6]
- 부족한 것: 필드명에 상·하순 구분이 없고 기준 혈관을 말하지 않는다. 값 일치만으로 연결하지 않는다.
- 제한되는 판단: 입술 깊이 수치의 대상 연결.

### ADZ-B07 — DAO 67.7% 의 기준
- `/zones/8/tissue_data/dao_coverage`, `/zones/8/tissue_data/notes`, `/zones/8/clinical_pearls/0`
- 부족한 것: 67.7% 가 사례 비율인지 면적 비율인지 등 분모가 없다.
- 제한되는 판단: 수치의 단위·성격 분류.

### ADZ-B08 — `asian_adjacent_distribution_percent` 의 집단 한정
- `/zones/5/tissue_data/asian_adjacent_distribution_percent` = 93.3. 같은 수치를 쓰는 `/zones/5/vessels/0/course`·`/zones/5/tissue_data/notes`·`/zones/5/clinical_pearls/0` 문장에는 대상 집단이 없다.
- 부족한 것: 집단 한정의 근거가 필드명뿐이다.

### ADZ-B17 — 등급 척도 정의 없음
- `/zones/*/danger_level`(정수 2~5), `/zones/*/danger_color`(red/orange/yellow/green), `/zones/*/filler_specific/risk_level`
- 원문 사실: 11개 zone 모두 danger_level = filler_specific.risk_level 이다. 색은 5→red, 4→orange, 3→yellow, 2→green 으로 짝지어 나온다.
- 부족한 것: 척도 정의, 두 등급의 관계, 색 대응 규칙이 원장 안에 없다. `/zones/1/tissue_data/csm_thickness_variation_mm`(0.4)의 통계적 의미(± 의 성격)도 없다.

### ADZ-B18 — 약식 출처·자료 생성 방식
- `/consensus_method` 「3-AI Expert Consensus (…)」, 약식 출처: `/zones/0/vessels/0/note`(Anat Rec 2024 cadaver), `/zones/3/tissue_data/muscle_fiber_data`(SRA 2024), `/zones/3/tissue_data/notes`(교과서), `/zones/4/tissue_data/rhinion_data_source`(JCD 2024, USG n=52), 「Beleznay 2019 업데이트」 등
- 부족한 것: 수치별 출처가 일부만 있고 약식이다. 외부 자료로 보충하지 않았다. 수치의 임상적 타당성은 1차 범위가 아니다.

## F — 후속 의미 조사

### ADZ-F06 — 「관자궁」 표기
- `/zones/2/clinical_pearls/6` 「중측두정맥은 관자궁 상방 약 2cm에서 …」. 원장 다른 곳에는 「관골궁」(`/zones/6/vessels/0/course`)이 있다.
- 오기인지 다른 낱말인지 원문만으로 확정하지 않는다. 원본 표기 확인 후보. Kiwi 는 「관/NNG + 자궁/NNG」로 분석한다(K01).
- 「중측두정맥」은 이 zone 의 vessels 목록에 없다(목록에는 「측두동맥 중간가지 (Middle temporal artery)」).

### ADZ-F13 — 같은 대상을 가리킬 수 있는 다른 표기
원문 그대로 보존. 같은 대상인지는 판정하지 않았다.

| 표기 묶음 | Pointer |
|---|---|
| 비순주름 / 팔자주름 / Nasolabial Fold / NLF | `/critical_safety_facts/blindness_highest_risk_zones`, `/zones/5/name_ko`, `/zones/5/name_en`, `/zones/5/vessels/0/course` 외 |
| 글라벨라 / 미간 / Glabella | `/zones/4/clinical_pearls/0`, `/zones/1/name_ko`, `/zones/1/name_en` |
| hyaluronidase / 히알루로니다제 | `/critical_safety_facts/caveat`, `/zones/3/vessels/1/danger`, `/zones/9/clinical_pearls/5` 외 |
| 측두신경 (Temporal branch of facial nerve) / 안면신경 측두분지 | `/zones/2/nerves/0/name`, `/zones/2/clinical_pearls/1`, `/zones/2/botox_specific/key_warning` |
| 광대근 (Zygomaticus) / 관골근(zygomaticus major) | `/zones/6/botox_specific/target_muscle`, `/zones/6/botox_specific/key_warning` |
| 내안각동맥 / Medial palpebral artery | `/zones/3/vessels/2/name` |
| 비배부 / 배비동맥 / Dorsal nasal artery / dorsal nasal | `/zones/1/filler_specific/emergency_protocol`, `/zones/1/vessels/1/name`, `/critical_safety_facts/minimum_filler_for_blindness` |
| 협근신경 / Buccal branch of facial nerve | `/zones/5/nerves/1/name`, `/zones/6/nerves/1/name` |
| 모터 신경 / motor | `/zones/9/clinical_pearls/1`, `/zones/9/nerves/0/type` |
| 볼류메트릭 / 볼루스 | `/zones/6/clinical_pearls/2`, `/zones/6/filler_specific/safe_technique` |
| lip incompetence = 하순 외반 / 입술 마비 → 발음/식사 장애 | `/zones/8/botox_specific/risk`, `/zones/7/botox_specific/key_warning` |

### ADZ-F14 — 다른 항목·다른 원장을 가리키는 참조 표현
참조 표현과 위치만 보존했다. 연결은 하지 않았다.

| 참조 표현 | Pointer |
|---|---|
| critical_safety_facts 의 부위 비율(코·미간·이마·비순주름) ↔ zones | `/critical_safety_facts/blindness_highest_risk_zones` |
| 「코 56.3% 다음」 | `/zones/1/clinical_pearls/0` |
| 「색전 시 안과 응급 프로토콜 준용」(temple 에 emergency_protocol 없음) | `/zones/2/clinical_pearls/5` |
| 「관자놀이 필러와 병행 시 주의」, 「이갈이/사각턱 보조」 | `/zones/2/botox_specific/dose_range`, `/zones/2/botox_specific/target_muscle` |
| 「상순동맥과 유사 경로」 | `/zones/7/vessels/1/course` |
| 「NLF 필러와 병행」 | `/zones/5/botox_specific/safe_zone` |
| 교근 25-50U/측 — cheek·jawline 양쪽 | `/zones/6/botox_specific/dose_range`, `/zones/9/botox_specific/dose_range` |
| Nefertiti lift — jawline·neck 양쪽 | `/zones/9/botox_specific/dose_range`, `/zones/10/clinical_pearls/2` |
| 제품·재료명(HA, CaHA, PLLA, Profhilo, 스킨부스터, 바이오스티뮬레이터) — 제품 원장과의 연결 | `/zones/*/filler_specific/preferred_product` 외 |
| 턱(Chin) / 턱선(Jawline) 별개 zone | `/zones/8`, `/zones/9` |

## P — 잠정 관찰 (구조·표기)

### ADZ-P09 — 「→」의 여러 기능
인과·연쇄(「표재성 주사 → … 마비 → …」), 경로(「안동맥(ophthalmic artery)으로 역류 → 망막 허혈」), 지점 연결(`/zones/2/tissue_data/pitanguy_line` 「이주(tragus) 하부 0.5cm → 눈썹 외측 1.5cm 상방을 잇는 선」), 위치별 변화(`/zones/5/clinical_pearls/1` 「하악 1.9mm → 비측 0.8mm」), 처치 순서(`/zones/4/filler_specific/emergency_protocol`). 공백 없는 「occlusion→necrosis」(`/zones/9/filler_specific/primary_risk`)도 있다. 기호만으로 관계 종류를 정하지 않는다.

### ADZ-P10 — 「/」의 여러 기능
README 는 「/ = 둘 중 하나」라고 하지만 이 원장의 「/」는 대안(「CaHA/PLLA」), 단위당(「U/측」「mL/점」「mg/일」「포인트/band」), 연도 묶음(「2023/24」), 분수(「1/3」), 대비 쌍 구분(「Sub-SMAS: … / Subcutaneous: …」), 영문 이름 병기(「External nasal artery / Lateral nasal artery」), 명칭 병기(「Malar/Buccal」), 나열(「혈관/신경」「발음/식사」)로 쓰인다. 전 출현은 `expressions.json` regex_candidates(pattern=slash).

### ADZ-P11 — 범위·연결 기호
범위 구분자가 「-」「–」(1,500–3,000U)「~」(15~60분, 75~100mg, 쇄골~하악연) 세 가지다. 「-」는 범위 외에 구조 연결(「피부-골막」「점막-피부」「천측두동맥-안동맥」「미간-상활차」「피하-근막」)과 단계 범위(「저-중점도」)에도 쓰인다.

### ADZ-P12 — 숫자가 문자열·필드명에 들어간 곳
`/zones/0/botox_specific/diffusion_range_cm` 는 문자열 "1.5-3.0" 이다(이 필드는 forehead 에만 있다). 용량은 전부 문자열(`dose_range`)이고 단위 표기가 「units」「U」「IU」「U(IU)」로 섞인다. 숫자형 필드의 단위는 필드명 접미사(_mm, _ml, _cm, _percent)로만 표시된다.

### ADZ-P15 — 같은 문장의 반복 출현
완전 일치 문장이 서로 다른 필드에 있다: `/zones/0/tissue_data/notes` = `/zones/0/clinical_pearls/0`, `/zones/5/vessels/0/course` = `/zones/5/clinical_pearls/0`(`/zones/5/tissue_data/notes` 는 어미만 다름). 혈관·신경 이름도 zone 사이에서 같은 문자열로 반복된다(review.md 「같은 문자열의 반복 출현」 표). 어느 필드가 원천인지 원문에 없다. 각 출현 위치를 그대로 유지했다.

### ADZ-P16 — 선택 필드·구조 변형
`vessels/*/note` 는 forehead 만, `depth_range_mm` 은 forehead 2·glabella 1·lips 2 에만, `depth_mm` 은 lips 에 없다. `emergency_protocol` 은 glabella·periorbital·nose 에만, `diffusion_range_cm` 은 forehead 에만 있다. `tissue_data` 키 구성은 zone 마다 다르다. 일부 이름에는 영문 병기가 없다(`/zones/4/nerves/1/name`, `/zones/8/vessels/1/name`). 표는 review.md 「구조 변형 · 선택 필드 · 빈 값」.

### ADZ-P19 — 편집 이력이 값 안에
`/zones/1/tissue_data/notes` 「기존 15mm/21mm 값은 근육 두께로 해부학적으로 성립하지 않아 삭제했으며 …」. 데이터 값과 변경 기록이 섞여 있다.

### ADZ-P20 — 기준이 다른 수량
`/zones/3/filler_specific/safe_technique` 「극소량(0.1mL/측)」 ↔ `/zones/3/filler_specific/max_per_point_ml` 0.05. 측/점 기준이 달라 비교하지 않았다.

### ADZ-P21 — vessels 목록에 없는 혈관명
`/zones/2/filler_specific/primary_risk` 「심부측두동맥」, `/zones/2/clinical_pearls/6` 「중측두정맥」은 temple 의 vessels 목록에 없다.

### ADZ-P22 — 필드 이름과 내용의 성격 차이
`/zones/5/vessels/0/course` 에 경로가 아니라 통계(93.3%, 42.9%)가 있다. `/zones/5/botox_specific/safe_zone` 에 위치가 아니라 병행·빈도(「NLF 필러와 병행, 보톡스 단독은 드묾」)가 있다.

### ADZ-P23 — 목 필러 사용 빈도와 filler_specific 구조
`/zones/10/clinical_pearls/3` 「목 필러는 거의 사용하지 않음」이지만 `/zones/10/filler_specific` 은 다른 zone 과 같은 구조로 채워져 있다.

## K — 알려진 형태소 분석 한계 (Kiwi 0.24.1 cong, 기본 사전)

출현별 원시 토큰은 `morphology.json` 에 있다. 교정하지 않았다. 형태소 기본형은 도메인 표준명이 아니다.

### ADZ-K
아래 K01~K05 묶음 전체를 가리킨다(review-part 관찰 표에서 이 묶음 ID 로 참조).

- **K01 전문어 분절** — `segmentation_review`: 관찰 낱말 249 출현 중 117 출현이 여러 형태소로 나뉜다. 뜻이 바뀌는 예: 「관자궁」→관/NNG+자궁/NNG, 「천측두동맥」→천/NR(수사)+측두+동맥, 「대이개신경」→대/XPN+이/NR+개/NNB+신경, 「비중격하강근」→비중/격하/강/근, 「저점도·고점도」→저·고/MM+점/NNG+도/JX(조사로 분석), 「중점도」→중점/NNG+도/JX, 「표재성」→표/재/성, 「상순거근」→상순+거/MM+근. 영향: 토큰 단위로 개념을 세면 조각과 다른 뜻 낱말(자궁·이·천)이 생긴다. 복합 표현은 원문 구간(expressions.json)으로 따로 보존했다.
- **K02 명사 form 이 표면과 다름** — `form_mismatch_review` 3 출현: 「하안검」→ form「하안거」(`/zones/3/nerves/0/significance`, `/zones/3/clinical_pearls/4`, `/zones/6/nerves/0/significance`). 영향: form/lemma 로 모으면 다른 낱말이 된다. surface 칸을 같이 써야 한다.
- **K03 범위 표기의 비일관 분석** — `serial_token_review` 36 출현: 정수 범위(「10-30」「4-6」), 분수「1/3」, 연도「2023/24」, 쪽수「203-208」은 W_SERIAL 한 토큰이 되고, 소수 범위(「0.5-1.0mm」)와 「~」 범위는 SN+SO+SN 으로 갈라진다. 「–」(en dash)는 SW. 영향: 범위를 토큰으로 찾으면 일부를 놓친다. `number_unit_review` 에 출현별로 있다.
- **K04 기호** — 「→」「≥」「+」「%」「—」「–」는 SW, 「-」「~」는 SO. 기호의 기능(ADZ-P09~P11)은 분석기가 구분하지 않는다. 「occlusion→necrosis」처럼 붙은 표기는 SL+SW+SL 로 나뉜다.
- **K05 부정·가능성 단서** — `cue_review` 51 출현 모두 단서 표면이 토큰에 남아 있었다(사라진 곳 0). 다만 단서와 그것이 걸리는 대상(무엇이 금지·가능인지)의 범위는 분석기가 주지 않는다. 범위는 expressions.json 수동 표현·절 구간으로만 보존했다.

## 해결된 A (작업 중 발견·수정)

| # | 내용 | 조치 | 재검증 |
|---|---|---|---|
| A-fix-1 | 분절 관찰에서 「골막상」이 「골막상층」「연골막상」 안의 부분 문자열로, 「각동맥」이 「내안각동맥」 안에서 잡혀 「경계 넘음」으로 잘못 분류됐다(4 출현) | 상태를 「관찰 대상 아님: 더 긴 낱말(토큰)의 부분 문자열」로 구분 | build 재실행, verify.py 통과 |
| A-fix-2 | 읽기 문서의 숫자 값이 파싱 값 재직렬화로 표시돼 원문 리터럴(예: `3.0`)과 달라질 위험 | 원문 숫자 리터럴(`number_literal`)을 그대로 싣도록 변경 | verify.py 가 리터럴 일치 검사 |
| A-fix-3 | 절 구간(clause_segments)이 소수점·「et al.,」·숫자 사이 「;」에서 잘렸다 | 분할 정규식 수정(494 → 410 구간) | build 재실행, verify.py 통과 |

## 사용자 결정 0 의 근거

남은 항목을 하나씩 보았다. I 4건은 원문 내부 대조 후보이고 원본 보존 지시 아래 지금 고를 것이 없다(원본 확인 후보로만 남김). B 5건은 원문에 없는 정보라 사용자 추측으로 채우지 않는다. F 3건은 원장 간 비교·공통 개념 단계의 과제다. K 는 도구 한계로 기록했다. 도구·출력 형식 선택은 에이전트가 정했다. 그래서 지금 사용자에게 올릴 선택(C)은 없다. 의미 단계에서 원본 수정이 필요해지면 그때 원문·위치·선택지·영향을 묶어 올린다.
