---
type: research
id: step3-research
title: "실버 3단계(부위) 조사 — 근거 · 원천 부위 문자열 전수 매핑 · 트리 밖 판정 · 노드 속성안"
product: procedure-hub
feature: phub-recommend
created_at: 2026-10-28
source: PROCEDURE-HUB/phub-stg-2026-10-26 (읽기만)
data: step3-research.json
---

# 실버 3단계(부위) 조사

> 정해진 트리(DEC-002 37 + OQ-206 6 = 43 노드)는 다시 논의하지 않았다. 아래는 원천 문자열이 **어디로 가는지**와 트리 밖 이름의 **해결 안**이다. 행 전체(500)는 `step3-research.json` `rows`.

## ① 결정 묶음

| 묶음 | 추천(한 줄) | 근거 | 영향(단위) | 최종 판단 |
|---|---|---|---|---|
| **B1** 트리 밖 7 판정(브리프 목록) | 등 · 옆구리 · 콧망울 = 새 노드 / 브라라인 → 등 · 엉덩이 → 힙 · 페이스 → 얼굴 · 하관 → 턱(묶음) 동의어 | D-05 규칙 ①(원천 이름 칸) · ②(안전 · 시술) — §3 행마다 파일:키 | 새 노드 3 · 트리 밖 문자열 21문자열 · 77회 | 사용자 |
| **B2** 조사에서 새로 나온 트리 밖 — 새 노드 7 | 제모 부위 팔 · 가슴 · 수염 · 구레나룻 + 얼굴 세부 인중 · 눈썹 · 마리오네트를 새 노드로(상위는 §3) | 모두 고민 · CC 이름 칸에 따로 있음(규칙 ①). 제모 넷은 OQ-206 「다리 · 비키니」 추가와 같은 원천 · 같은 이유 | 새 노드 7 · 14문자열 · 66회 | 사용자 |
| **B3** 기존 노드로 가는 문자열 | §2 표대로 동의어 · 해부학 이름 속성 · 부위+다른 축 분리(D-07)로 단다 | 문자열마다 이름 칸 표본 · 본문 표본(json rows) | 290문자열 · 2185회 → 트리 노드 43 전부에 1개 이상(입가만 이름 칸 근거 0) | 코디(결정대로 적용) |
| **B4** 근거 약 동의어 — 값 + 확인 질문 | 값은 §2 대로 두고 의료진 질문 목록(§8)에 올린다. open 아님 | 본문 1~5곳 · 해부 문맥 추정(하안검 → 눈밑 · 중안면 → 볼(묶음) · 팔뚝 = 위팔 뒤 등) | 노드로 가는 것 중 20문자열 · 78회 + 트리 밖 무릎 · 불독살 · 하관 계열 | 코디 · 확인은 의료진 |
| **B5** 트리 밖 → 기존 노드 동의어(본문 · 고민 말) | 무릎 → 다리 · 불독살 → 턱선 + 고민 처짐 | 무릎: 이름 칸 없음 · 불독살: jowl = 하악연 위 처짐(jawline zone) | 2문자열 · 5회 | 코디 |
| **B6** 트리 밖 → 부위 아님 | 골반저근(요실금 EMS) · 관절치료(줄기세포) = 비미용 — 부위 노드 안 만듦 | 관절치료는 v3 market_rows_skipped 에 이미 빠짐 | 2문자열 · 3회 | 코디 |
| **B7** 부위 아님 문자열 — 단계로 넘김 | 조직층 → 4단계 기법(깊이) · 혈관 · 신경 · 해부 지표 → 위험 부위 속성 · 고민 → 7단계 · 제품 → 1단계 · 정맥 · IV → 5단계 경로 · 합병증 · 사후관리 → 안전 원장 | data-model.md ANATOMY_HAZARD(vessel · nerve · structure) · DEC-003 수액 「해당 없음」 | 173문자열 · 1251회 | 코디 |
| **B8** 경계 — 묶음 ↔ 좁은 · 얼굴 ↔ 얼굴 전체 · 바디 ↔ 전신 | §4 규칙 5개(정해진 트리 그대로, 원천 문자열 가는 곳만) | DEC-002 「상위 = 묶음 · 하위 = 좁은」 · DEC-003 OQ-306 | 이름 같은 묶음 5쌍 + 턱(묶음) · 얼굴 전체 7문자열 · 전신 2 + 계통 전신 9문자열 | 코디 |
| **B9** 위험 부위 대응 — 「확인 필요」 5줄 + 새 노드 | periorbital · nose · cheek · neck = 묶음 / chin = 턱끝(name_ko 「턱」보다 본문 기준) / 새 노드 콧망울 → nose(본문 경고 있음) | zone 본문 키(§6) | zone 11 · 노드 53 | 코디 추천 · 최종 의료진(OQ-202) |
| **B10** 해부학 이름 후보값 | 노드 53(트리 43 + 새 10) 전부에 영문 · 한글 후보를 채운다(빈칸 0) | 레포 근거 강 24 · 레포 일부 중 4 · 표준 용어집만 약 25 | 노드 53 | 코디 · 확정은 의료진(OQ-202) |
| **B11** DEC-002 근거 표 정정 | ① 입가 「원천 근거 없음」 → 있음(본문 6문자열 · 11회, 이름 칸 0) ② 얼굴 전체 근거 「P5-4 전체미백」 빼기(항목 둘 다 정맥 수액 → 해당 없음) ③ 전신 근거 「P4-3 전신항노화」 · 「CC 전신항노화/NAD+수액」 빼기(계통 → 해당 없음, DEC-003 이 이미 분리) | §7 | DEC-002 표 3줄 | 코디 |
| **B12** 원천 수정 후보 | ① anatomy-danger-zones 의 「비근근」이 glabella 에선 Procerus · nose 에선 Nasalis — 같은 한글로 두 근육 ② temple clinical_pearls 「관자궁」(관골궁 오기로 보임 — 근거 약) | zones[glabella]·[nose].botox_specific.target_muscle · zones[temple].clinical_pearls | 원천 문자열 2 | 코디(원천 수정 목록에 추가) |

## ② 사용자가 최종 판단할 것

두 묶음, 14건. 나머지 묶음은 결정대로 적용하거나(코디) 의료진 확인(OQ-202)으로 간다.

**U1 (B1) 트리 밖 7 판정 — 추천대로 갈까**

| 이름 | 추천 | 대안 | 원천 등장(회) |
|---|---|---|---|
| 등 | 새 노드 (상위 바디) | 바디 동의어(새 노드 안 만들면 등살주사는 바디로) | 15 |
| 브라라인 | 등 동의어 | 등을 노드로 안 하면 바디 동의어 | 5 |
| 엉덩이 | 힙 동의어 | 없음 — 이름 칸 근거가 힙 쪽에만 있다 | 12 |
| 옆구리 | 새 노드 (상위 바디) | 복부 동의어 — 시장가가 복부(1부위)와 러브핸들을 따로 매기므로 비추천 | 14 |
| 콧망울 | 새 노드 (상위 코(묶음)) | 코 동의어 — 비익 전용 경고가 노드 없이 묻히므로 비추천 | 14 |
| 페이스 | 얼굴 동의어 | 없음. 함께 정리: 풀페이스 → 얼굴 전체 · 페이스라인 → 얼굴 + 고민 「라인」 · 페이스리프팅 → 얼굴 + 목적 「리프팅」 | 5 |
| 하관 | 턱(묶음) 동의어 | 얼굴 동의어 — 원천 문맥(「하관 부위 볼살과 불분명한 턱선」)이 턱선 · 볼 아래라 턱(묶음)이 더 좁고 맞다 | 12 |

**U2 (B2) 새 노드 7 — 추가할까(아니면 대안의 동의어로)**

| 이름 | 추천 | 대안 | 원천 등장(회) |
|---|---|---|---|
| 팔 | 새 노드 (상위 바디) | 팔뚝 동의어 — 제모 「팔」이 위팔 뒤로 좁아져 비추천 | 6 |
| 가슴 | 새 노드 (상위 바디) | 바디 동의어 | 8 |
| 수염 | 새 노드 (상위 얼굴) | 얼굴 동의어(남성 제모 「얼굴」로 뭉침) | 2 |
| 구레나룻 | 새 노드 (상위 얼굴) | 얼굴 동의어 | 2 |
| 인중 | 새 노드 (상위 입가) | 입술 동의어 | 6 |
| 눈썹 | 새 노드 (상위 눈가(묶음)) | 상위를 이마(묶음)로 — 눈썹은 이마와 눈가 사이. 경고가 이마 · 미간 zone 에 있어 이마(묶음)도 가능. 추천은 눈가(묶음)(상담에서 「눈매」 시술로 묶임) | 32 |
| 마리오네트 | 새 노드 (상위 입가) | 입꼬리 동의어 + 고민 주름 | 10 |

## ③ 셈

- 훑은 범위: 원천 JSON **21개 전부**, 문자열 칸 **22,749개**(이름 칸 + 본문)
- **원천 부위 문자열 500개 · 등장 3,582회** (단위: 공백 없앤 표면 문자열 1개 = 1행)
  - **노드로 감 290문자열 · 2,185회** — 노드 이름 93 · 부위+다른 축(D-07) 113 · 동의어 34 · 해부학 이름(속성) 50. 이 중 근거 약 20문자열(값 + 의료진 확인 질문)
  - **트리 밖 37문자열 · 146회** — 새 노드안 27 · 기존 노드 동의어안 8 · 부위 아님안 2 → 이름 18개로 묶임(§3), 새 노드안 10개
  - **부위 아님 173문자열 · 1,251회** — 4단계 기법 20(631회) · 위험 부위 속성(ANATOMY_HAZARD) 107(315회) · 7단계 고민 9(86회) · 안전 원장(합병증) 16(84회) · 5단계 단위 시술 경로 4(74회) · 사후관리 문구 7(31회) · 1단계 제품 9(20회) · 2단계 계열 1(10회)
- **open 후보 37문자열 = 트리 밖 전부, 모두 해결 안 있음 → 해결 안 없는 open 0**
- 노드: 트리 43 전부 원천 문자열 1개 이상(이름 칸 근거 0 은 입가 하나) · 새 노드안 10 · 해부학 이름 후보 53 노드 전부 채움(강 24 · 중 4 · 약 25)

## 1. 근거(A)

### 1-1. 레포 안 부위 · 해부학 근거

| 파일 | 키 | 무엇 |
|---|---|---|
| `PROCEDURE-HUB/phub-stg-2026-10-26/anatomy-danger-zones.json` | zones[].id · name_ko · name_en | 위험 부위 11곳 영문 이름 — 노드 해부학 이름 근거(강) — version 1.2 · updated 2026-07-26 · consensus_method 「3-AI Expert Consensus (Perplexity research + Gemini analysis + Claude textbook)」 — 사람 의료진 검수 표기 없음 |
| `anatomy-danger-zones.json` | zones[].botox_specific.target_muscle | 부위별 표적 근육(전두근 · 추미근 · 안륜근 · 교근 · 광대근 · 구륜근 · 이근 · 광경근 …) — 해부학 이름 속성 후보 |
| `anatomy-danger-zones.json` | zones[].vessels[] · nerves[] · tissue_data · safe_injection_depth · clinical_pearls | 하위 자리(비첨부 · 비익 · 비주 · 코등 · 협부 · 관골부 · 구각 · 이부 · 눈물고랑 · 하안검)를 본문으로 다룸 — 묶음 대응 근거 |
| `anatomy-danger-zones.json` | critical_safety_facts | 문헌 인용: Beleznay et al., Aesthet Surg J 2019;39(6):662-674(실명 고위험 부위 코 · 미간 · 이마 · 비순주름) · Yi et al., J Cosmet Dermatol 2024 · Khan et al., Aesthet Surg J 2017;37(2):203-208 |
| `literature-evidence.json` | categories.M1/M2/M7/M9 .moa/.effects[].statement + citations | 부위 영문 문장: face · lower face(PMID 33714246) · perioral · jawline(PMID 33633459) · facial and neck(PMID 33469333) · periorbital(PMID 37753689) · gummy smile(PMID 33714246) |
| `phub-recommend/docs/architecture/data-model.md` | ERD ANATOMICAL_SITE(parent_id · public_code · name_ko) · ANATOMICAL_SITE_TRANSLATION · PROCEDURE_SITE · ANATOMY_HAZARD(site_id · hazard_type vessel · nerve · structure) · §10.1 | 「시술 적용 부위와 위험 부위가 동일한 canonical site를 참조함」 — 위험 부위를 같은 부위 노드에 매다는 근거 · 해부학 이름(영문)은 translation 칸 |
| `phub-recommend/docs/references/medical-codes.md` | §2 SNOMED CT | 레포가 외부 표준으로 조사한 것은 시술 개념(SNOMED Procedure)뿐 — 부위(body structure) 코드 매핑은 레포에 없음 |
| `phub-recommend/docs/reviews/*` | plausible-hold.md P1 등 | 부위 기준 문서 없음 — danger zone 필러 안전 고지 논의만 |
| `taxonomy.json · market-pricing.json · problem-packages.json` | 이름 칸(§2 방법) | 상담 이름 · 구어 — 해부학 이름 근거는 아님 |

- **레포 결론**: 부위 · 해부학 기준 문서는 없다. 근거는 ① `anatomy-danger-zones.json`(11곳 영문 이름 · 표적 근육 · 하위 자리 본문) ② `literature-evidence.json` 문헌 문장(PMID) ③ `data-model.md` 의 ANATOMICAL_SITE(부위 계층 + 번역 칸) · ANATOMY_HAZARD(위험 부위를 같은 부위 노드에 매담) 셋뿐이다
- `anatomy-danger-zones.json` 은 「3-AI Expert Consensus」로 만들어졌고 사람 의료진 검수 표기가 없다 — 해부학 이름을 이 파일로 「강」이라 적은 것은 **레포 근거가 있다**는 뜻이지 의학적 확정이 아니다(OQ-202 그대로)

### 1-2. 레포 밖 표준 용어(약)

- **Terminologia Anatomica 2판(TA2)** — FIPAT 2019 https://fipat.library.dal.ca/ta2/ — 라틴 · 영문 부위 이름 후보(regio frontalis · regio buccalis · apex nasi · ala nasi · angulus oris · regio mentalis 등)
- **대한해부학회 해부학용어 6판** — 대한해부학회 2014 — 한글 해부 이름 후보(깨물근 · 등세모근 · 넓은목근 · 눈확부위 · 볼기부위 등)
- 이 둘은 이름 후보를 고르는 데만 썼다. 레포 근거가 없는 노드(바디 하위 · 턱밑 · 잇몸 등)는 해부학 이름이 전부 「약」이다

## 2. 원천 부위 문자열 전수 매핑(B)

### 2-1. 방법

- **scope** — phub-stg-2026-10-26 의 JSON 21개 전부 · 모든 문자열 칸(22,749) — 이름 칸만이 아니라 본문(indications · mechanism · clinical_pearls 등)까지
- **unit** — 「원천 부위 문자열」 = 부위를 가리키는 표면 문자열을 공백 지우고(영문은 소문자) 하나로 센 것. 같은 표면이라도 문맥이 다르면(「팔」 시술 부위 · 「팔」 채혈 위치) 따로 센다. 등장 수 = 문자열 칸 안의 출현 횟수(extracted.json 과 taxonomy.json 의 같은 본문은 중복 셈)
- **rule1_fields** — 규칙 ① 「원천이 따로 부른다」는 DEC-002 정의대로 이름 칸만: market-pricing items.name · taxonomy problem(category · label · items.name · detail) · taxonomy modality(subcategories.label · items.name · detail) · problem-packages(problem · cc_group · cc · cc_detail) · problem-combos.problem · anatomy-danger-zones(id · name_ko · name_en). 행마다 count_name_fields
- **matching** — 사전 200여 패턴(긴 것 · 문맥 있는 것 우선) → 문자열마다 가장 왼쪽 · 우선순위 높은 것 하나. 사전 전체(패턴 · 판정 · 노드)는 json method.lexicon
- **excluded** — 글자만 겹치는 것은 셈에서 뺐다: 볼륨 · 볼뉴머 · 볼루스(볼) · 피코 · 코스 · 코그 · 알코올(코) · 광대역(광대) · 주입 · 수입 · 입자(입) · 손상 · 손실(손) · 발생 · 발적 · 발현(발) · 목적 · 목표 · 항목(목) · 배양 · N배(배) · 「…등」(나열) · 부정맥 · 페이스메이커 · 「눈에 띄」 · craniofacial(학술지명) · foreign body · ALA(성분) · 「…하지」(동사). 「부위 · 국소 · 피부 · 신체(일반)」는 부위를 가리키지 않아 셈 밖
- **residual_check** — 사전 뒤 남은 부위 형태소(얼굴 · 이마 … 등 90여 개)를 다시 훑어 위 「겹침」 외 남은 것 0 — 마지막에 「안면 전체 · 마리오넷 · 마리오네트선 · 상체 거상 · 눈�리」를 사전에 넣고 다시 셈

### 2-2. 노드로 가는 문자열 — 노드별

「이름 칸」= 규칙 ① 칸 등장 수. 문자열 뒤 숫자 = 등장 수. ⚠ = 근거 약(값 + 확인 질문).

| 노드 | 상위 | 문자열(등장 · 이름 칸) | 노드 이름 · 동의어 · 해부학 이름 | 부위+다른 축(D-07) — 나머지 조각 → 단계 |
|---|---|---|---|---|
| 얼굴 | — | 15 (348 · 20) | 안면(113) · 얼굴(126) · facial(21) · 안면부(5) · face(10) · 표정근(23) | 얼굴 윤곽(22) → 윤곽:7단계 고민 · 안면홍조(9) → 홍조:7단계 고민 · 페이스리프트(3) → 리프팅:6단계 목적 · 페이스라인(8) → 라인:7단계 고민 · 안면거상술(1) → 거상(수술):4단계 기법 · 안면홍조증(1) → 홍조:7단계 고민 · 얼굴혈관종(1) → 혈관종:7단계 고민 · 페이스 리프팅(4) → 리프팅:6단계 목적 · 안면거상(1) → 거상(수술):4단계 기법 |
| 이마(묶음) | 얼굴 | 1 (3 · 3) | — | 이마/관자놀이(3) |
| 이마 | 이마(묶음) | 8 (101 · 14) | 이마(47) · forehead(2) · 전두근(3) · Frontalis(1) | 이마 주름(38) → 주름:7단계 고민 · 이마 볼륨(5) → 볼륨:7단계 고민 · 이마지방이식(3) → 지방이식:2단계 계열 · 이마필러(2) → 필러:2단계 계열 |
| 미간 | 이마(묶음) | 7 (84 · 8) | 미간(33) · glabella(2) · 추미근(6) · corrugator supercilii(2) · Procerus(1) · glabellar(1) | 미간 주름(39) → 주름:7단계 고민 |
| 관자놀이 | 얼굴 | 10 (43 · 13) | temple(2) · 관자놀이(20) · 측두부(3) · 측두근(3) · Temporalis(1) · 측두(1) · 관자(4) | 볼/관자놀이(4) · 이마/관자놀이(3) · 관자놀이충전(2) → 충전:6단계 목적 |
| 눈가(묶음) | 얼굴 | 8 (26 · 5) | periorbital(4) · 눈 주변(3) · 안륜근(4) · orbicularis oculi(2) · 눈 주위(5) · 안와주위(2) · 꺼진 눈(4) | 눈가 쳐짐(2) → 쳐짐:7단계 고민 |
| 눈가 | 눈가(묶음) | 11 (111 · 16) | 눈가(29) · ⚠눈�리(1) · ⚠눈꼬리(1) | 까마귀발(10) → 주름:7단계 고민 · 눈가 주름(48) → 주름:7단계 고민 · crows-feet(1) → 주름:7단계 고민 · 까치발 주름(2) → 주름:7단계 고민 · 눈가보톡스(2) → 보톡스:2단계 계열 · 까마귀발 주름(2) → 주름:7단계 고민 · 까치발(11) → 주름:7단계 고민 · crow's feet(4) → 주름:7단계 고민 |
| 눈밑 | 눈가(묶음) | 11 (39 · 10) | ⚠하안검(4) · 눈물고랑(6) · tear trough(2) · 눈밑(7) · 애교살(2) | 눈밑 주름(4) → 꺼짐 · 주름 · 볼륨:7단계 고민 · 다크서클(3) → 다크서클:7단계 고민 · 눈밑 꺼짐(5) → 꺼짐 · 주름 · 볼륨:7단계 고민 · 애교필러(2) → 필러:2단계 계열 · 눈밑 볼륨(2) → 꺼짐 · 주름 · 볼륨:7단계 고민 · 다크서클필러(2) → 다크서클:7단계 고민 / 필러:2단계 계열 |
| 눈꺼풀 | 눈가(묶음) | 7 (33 · 5) | 상안검거근(1) · 안검(2) · 눈꺼풀(6) · 윗눈꺼풀(2) | 눈꺼풀 처짐(18) → 처짐:7단계 고민 · 아이라인반영구(2) → 반영구:2단계 계열 · 눈꺼풀쳐짐(2) → 처짐:7단계 고민 |
| 코(묶음) | 얼굴 | 2 (3 · 2) | nose(2) · 비근근 (Nasalis)(1) | — |
| 코 | 코(묶음) | 5 (53 · 11) | 코(39) | 코필러(7) → 필러:2단계 계열 · 코실리프팅(3) → 실리프팅:2단계 계열 · 코 라인(3) → 라인:7단계 고민 · 코성형(1) → 성형(수술):4단계 기법 |
| 코끝 | 코(묶음) | 6 (24 · 5) | 비주(2) · columella(1) · 비첨부(3) · 코끝(15) · depressor septi nasi(2) · 비첨(1) | — |
| 콧등 | 코(묶음) | 8 (22 · 3) | 코등(4) · 비배부(2) · 코뼈(1) · bunny lines(1) · 콧등(7) · 토끼주름(2) · 콧대(3) | 매부리코(2) → 매부리(혹):7단계 고민 |
| 볼(묶음) | 얼굴 | 6 (16 · 8) | cheek(1) · Cheek (Malar/Buccal)(1) · ⚠중안면부(5) · ⚠중안면(2) | 볼/관자놀이(4) · 볼/광대(3) |
| 볼 | 볼(묶음) | 13 (84 · 12) | 협근(2) · 볼(36) · 협부(7) · 상협부(1) · 뺨(6) · ⚠애플 페이스(1) | 볼 처짐(8) → 처짐:7단계 고민 · 볼살(12) → 살(지방):7단계 고민 · 볼 볼륨 (2) → 볼륨 · 충전:7단계 고민 · 볼지방이식(3) → 지방이식:2단계 계열 · 볼필러(2) → 필러:2단계 계열 · 볼쳐짐(2) → 처짐:7단계 고민 · 볼볼륨충전(2) → 볼륨 · 충전:7단계 고민 |
| 광대 | 볼(묶음) | 7 (44 · 5) | 관골(4) · 관골부(4) · malar(1) · 광대(18) · Zygomaticus(2) · 광대뼈(13) | 광대축소주사(2) → 축소:6단계 목적 / 주사:2단계 계열 |
| 입가 | 얼굴 | 6 (11 · 0) | perioral(2) · 구주위(1) · 입 주변(1) · 입가(2) | 입가 주름(4) → 주름:7단계 고민 · 입가 거상(1) → 거상:6단계 목적 |
| 팔자 | 입가 | 10 (74 · 6) | 비순구(1) · nasolabial(1) · Nasolabial Fold(1) · 상순거근(1) · Levator labii superioris(1) · 팔자(5) · ⚠비순홈(5) | 비순주름(1) → 주름:7단계 고민 · 팔자주름(54) → 주름:7단계 고민 · 코입술주름(4) → 주름:7단계 고민 |
| 입술 | 입가 | 16 (76 · 10) | 상구순(3) · 구륜근(2) · 상순(4) · lips(2) · 입술(25) · 하순(11) · vermillion(5) · lip(6) · Orbicularis oris(1) · 윗입술(2) · 구순(1) | 입술확대(3) → 볼륨 · 확대 · 라인:7단계 고민 · 입술라인(2) → 볼륨 · 확대 · 라인:7단계 고민 · 입술 볼륨(5) → 볼륨 · 확대 · 라인:7단계 고민 · 입술필러(2) → 필러:2단계 계열 · 입술반영구(2) → 반영구:2단계 계열 |
| 입꼬리 | 입가 | 7 (29 · 1) | 구각(8) · 구각부(1) · oral commissure(1) · DAO(4) · 구각하제근(1) · 입꼬리(12) | 입꼬리주름(2) → 주름:7단계 고민 |
| 잇몸 | 입가 | 4 (7 · 1) | 잇몸(1) · gum(1) | gummy smile(3) → 잇몸 노출 미소:7단계 고민 · 잇몸미소(2) → 잇몸 노출 미소:7단계 고민 |
| 턱(묶음) | 얼굴 | 8 (43 · 9) | 하악(4) · 턱(21) · ⚠상악골(2) · ⚠위턱뼈(2) · mandibular(1) | 턱필러(7) → 필러:2단계 계열 · 턱/턱선(4) · 턱보톡스(2) → 보톡스:2단계 계열 |
| 턱끝 | 턱(묶음) | 14 (28 · 7) | chin(1) · Chin (Mentum)(1) · 턱끝(4) · 이부(3) · 이근(4) · Mentalis(1) | 턱 딤플(1) → 자갈턱:7단계 고민 · peach pit chin(1) → 자갈턱:7단계 고민 · 뾰족턱(2) → 뾰족함(형태):7단계 고민 · 턱 끝 볼륨(3) → 볼륨 · 연장:7단계 고민 · 턱 끝 지방이식(1) → 필러 · 지방이식:2단계 계열 · 턱끝 필러(2) → 필러 · 지방이식:2단계 계열 · 턱끝 연장(2) → 볼륨 · 연장:7단계 고민 · 자갈턱(2) → 자갈턱:7단계 고민 |
| 턱선 | 턱(묶음) | 12 (135 · 15) | 하악연(18) · jawline(3) · 턱선(96) · Jawline (Mandibular border)(1) · 턱라인(6) · ⚠얼굴-목 경계선(1) | Nefertiti lift(2) → 네페르티티 리프트:4단계 기법 · 네페르티티(1) → 네페르티티 리프트:4단계 기법 · 턱선실리프팅(2) → 실리프팅:2단계 계열 · 턱선무너짐(2) → 처짐:7단계 고민 · 턱선보톡스(1) → 보톡스:2단계 계열 · 네페르티티 리프트(2) → 네페르티티 리프트:4단계 기법 |
| 사각턱 | 턱(묶음) | 8 (88 · 12) | 사각턱(29) · 교근(36) · Masseter(3) · 하악각(3) · ⚠턱폭(1) · ⚠턱근육(2) | 사각턱 보톡스(6) → 보톡스:2단계 계열 · 교근축소(8) → 축소:6단계 목적 |
| 턱밑 | 턱(묶음) | 6 (102 · 21) | 턱밑(31) · 턱 아래(5) · under the chin(1) · 턱밑지방(1) | 이중턱(63) → 이중턱(지방):7단계 고민 · 턱살(1) → 살(지방):7단계 고민 |
| 얼굴 전체 | 얼굴 | 7 (62 · 33) | 전체얼굴(32) · 풀페이스(8) · 안면 전체(2) · 얼굴 전체(14) · 전안면(4) | 풀페이스큐레이션(1) → 큐레이션:6단계 패키지 · 페이스앤넥큐레이션(1) → 큐레이션:6단계 패키지 |
| 목(묶음) | — | 2 (6 · 2) | neck(4) · 경부(2) | — |
| 목 | 목(묶음) | 21 (141 · 14) | 광경근(12) · Platysma(5) · 목(49) · 흉쇄유돌근(2) · SCM(2) · 네크라인(1) · 플래티스마근(1) · 초음파목(1) | Nefertiti lift(2) → 네페르티티 리프트:4단계 기법 · platysmal bands(2) → 주름 · 밴드:7단계 고민 · 목주름(50) → 주름 · 밴드:7단계 고민 · Platysmal band(1) → 주름 · 밴드:7단계 고민 · 목 리프팅(4) → 리프팅:6단계 목적 · 네페르티티(1) → 네페르티티 리프트:4단계 기법 · 목 실리프팅(1) → 리프팅:6단계 목적 · 목 밴드(1) → 주름 · 밴드:7단계 고민 · 네페르티티 리프트(2) → 네페르티티 리프트:4단계 기법 · 목의 세로 주름(1) → 주름 · 밴드:7단계 고민 · 넥큐레이션(1) → 큐레이션:6단계 패키지 · 목 앞쪽 세로주름(1) → 주름 · 밴드:7단계 고민 · 페이스앤넥큐레이션(1) → 큐레이션:6단계 패키지 |
| 승모근 | 목(묶음) | 4 (27 · 10) | 승모근(15) · 어깨(3) · 어깨라인(6) | 승모근보톡스(3) → 보톡스:2단계 계열 |
| 두피 | — | 12 (81 · 30) | 두피(62) · 헤어라인반영구(2) · SMP(2) · 정수리(1) · Scalp(1) | 두피치료(1) → 시술 이름:2단계 계열 · 두피메조(2) → 시술 이름:2단계 계열 · 두피PRP(2) → 시술 이름:2단계 계열 · 두피엑소좀(2) → 시술 이름:2단계 계열 · 두피스케일링(3) → 시술 이름:2단계 계열 · MTS두피(2) → 시술 이름:2단계 계열 · 두피주사(1) → 시술 이름:2단계 계열 |
| 바디 | — | 11 (77 · 22) | 바디(51) · EMS 바디(2) · 탄탄한 몸(2) · 신체 처짐(1) | 바디리프팅(2) → 라인 · 리프팅 · 탄력:7단계 고민 · 바디 쳐짐(2) → 라인 · 리프팅 · 탄력:7단계 고민 · 바디(여성)(3) → 여성:대상 속성(성별 · 6단계) · 바디탄력(3) → 라인 · 리프팅 · 탄력:7단계 고민 · 바디라인(8) → 라인 · 리프팅 · 탄력:7단계 고민 · 바디큐레이션(1) → 큐레이션:6단계 패키지 · 바디컨투어링(2) → 라인 · 리프팅 · 탄력:7단계 고민 |
| 겨드랑이 | 바디 | 1 (9 · 6) | 겨드랑이(9) | — |
| 팔뚝 | 바디 | 1 (26 · 4) | ⚠팔뚝(26) | — |
| 복부 | 바디 | 3 (61 · 9) | 복부(52) · ⚠배(5) · ⚠임신선(4) | — |
| 허벅지 | 바디 | 2 (28 · 4) | 허벅지(27) | 허벅지 안쪽(1) → 안쪽(위치 수식):1단계 규격 · 단위 |
| 종아리 | 바디 | 2 (14 · 2) | 종아리(12) · 비복근(2) | — |
| 전신 | 바디 | 2 (2 · 1) | 전신(1) · 전신 처짐(1) | — |
| 손 | 바디 | 4 (17 · 3) | ⚠손바닥(2) · ⚠손등 회춘술(6) · ⚠손등(5) · 손(4) | — |
| 발 | 바디 | 2 (6 · 3) | ⚠발바닥(2) · 발(4) | — |
| 다리 | 바디 | 3 (7 · 3) | 다리(5) | 다리라인(1) → 라인:7단계 고민 · 하지정맥류(1) → 정맥류:7단계 고민 |
| 비키니 | 바디 | 1 (2 · 2) | 비키니(2) | — |
| 힙 | 바디 | 2 (5 · 2) | 힙(2) | 힙업(3) → 리프팅:6단계 목적 |

### 2-3. 부위 아님 — 어느 단계로

| 단계 | 문자열 수(등장) | 문자열(등장) |
|---|---|---|
| 4단계 기법 | 20 (631) | 진피(187) · 진피층(135) · 표피(124) · SMAS(61) · 피하(48) · 골막상(18) · 표피층(17) · 점막(7) · 골막(6) · 점막하(5) · 유두진피(4) · 심부측두근막(3) · 근막(3) · 근막층(3) · 골막상층(2) · 측두근막이(2) · 망상진피(2) · 그물진피(2) · 측두근막(1) · 연골막상(1) |
| 위험 부위 속성(ANATOMY_HAZARD) | 107 (315) | 하악변연신경(29) · 안동맥(25) · 정맥(23) · 안면동맥(19) · 이신경(12) · 동맥(11) · 내안각(11) · 각동맥(8) · 안면신경(7) · 안와(7) · 안와연(6) · 상순동맥(6) · 활차상동맥(4) · 안와상연(4) · 천측두동맥(4) · Angular artery(4) · 외경정맥(4) · 배비동맥(3) · Pitanguy(3) · 안면신경 측두분지(3) · 안와하신경(3) · Infraorbital nerve(3) · 협근신경(3) · 협지방체(3) · 이동맥(3) · 침샘(3) · dorsal nasal(2) · ophthalmic artery(2) · Supratrochlear artery(2) · 활차상신경(2) · Supratrochlear nerve(2) · Dorsal nasal artery(2) · 이주(2) · 측두신경(2) · STL(2) · 상측두융합선(2) · 안와하공(2) · 안와격막(2) · Facial artery(2) · Buccal branch of facial nerve(2) · 안면횡동맥(2) · 이하선관(2) · Buccal fat pad(2) · 하순동맥(2) · Mental nerve(2) … 외 62 |
| 7단계 고민 | 9 (86) | 모발(56) · V라인(15) · 체모(5) · 전신항노화(3) · 전체미백(3) · 얼굴형(1) · 거미정맥(1) · 브이라인(1) · 전신재생(1) |
| 안전 원장(합병증) | 16 (84) | 안검하수(28) · 전신(28) · 눈(12) · 발끝(2) · 눈물(2) · 전신발진(2) · 안검외반(1) · 하안검 외반(1) · 전신적(1) · 전신에(1) · 목/가슴으로 확대(1) · 전신독성(1) · 팬더눈(1) · 전신흡수(1) · 눈부심(1) · 전신으로(1) |
| 5단계 단위 시술 경로 | 4 (74) | 정맥(40) · IV(29) · 팔(4) · 대퇴부 전외측(1) |
| 사후관리 문구 | 7 (31) | 입(18) · 손톱(4) · 상체 거상(3) · 손 위생(2) · 손끝(2) · 다리 거상(1) · 손 깨끗(1) |
| 1단계 제품 | 9 (20) | 리쥬란아이(4) · 엠페이스(3) · 인모드바디(3) · 바디HIFU(2) · 바디써마지(2) · 바디인모드(2) · 튠페이스(2) · 코안면전문(1) · 코안면(1) |
| 2단계 계열 | 1 (10) | 모발이식(10) |

- 「정맥」은 두 행이다 — 「정맥 주사 · 정맥 투여」(5단계 경로, 40회)와 「정맥 색전」 등 혈관(위험 부위 속성, 23회)
- 「입」 18회는 전부 「입 벌림 · 입 움직임」(사후관리 · 정상 반응) — 부위 입가와 다르다. 「눈」 12회도 기관(눈 손상 · 눈 건조) 뜻이고, 「눈 주변 · 눈 주위」는 눈가(묶음)으로 갔다

## 3. 트리 밖 판정(C)

D-05 쪼개는 규칙: ① 원천 이름 칸이 따로 부른다 ② 가능 시술 · 안전이 다르다 — 둘 다 아니면 쪼개지 않는다. 브리프 7 + 조사에서 나온 11 = 18 이름, 37문자열.

| 이름 | 판정(해결 안) | 상위 | ① 원천 이름 칸 | ② 시술 · 안전 | 문자열(등장 · 이름 칸) | 대안 | 최종 |
|---|---|---|---|---|---|---|---|
| **등** | 새 노드 | 바디 | 용도 「등살주사」(name) · 「등 브라라인」(detail) · 고민 P10-3 「수염/가슴/등」 | 지방분해 주사 · 제모 — 바디 다른 하위와 시술 대상이 다름(위험 부위 원장은 없음) | S279 브래지어 라인(2·0) · S403 등(8·3) · S494 등살주사(1·1) · S495 브라라인(3·1) · S496 등살(1·0) | 바디 동의어(새 노드 안 만들면 등살주사는 바디로) | 사용자(U1) |
| **브라라인** | 등 동의어 | 바디 | 용도 detail 「등 브라라인」 안에서만 — 따로 부르는 이름 칸 없음 | 등과 같은 시술(등살주사) | S279 브래지어 라인(2·0) · S495 브라라인(3·1) | 등을 노드로 안 하면 바디 동의어 | 사용자(U1) |
| **엉덩이** | 힙 동의어 | 바디 | 이름 칸에 없음(본문 12회) — 힙은 시장가 「이모드 (힙)」으로 이미 노드(OQ-206) | 같은 자리 · 같은 시술(「엉덩이 리프팅 (힙업)」 — 원천이 두 말을 같은 뜻으로 씀) | S268 엉덩이(12·0) | 없음 — 이름 칸 근거가 힙 쪽에만 있다 | 사용자(U1) |
| **옆구리** | 새 노드 | 바디 | 시장가 「쿨스컬프팅 (러브핸들 양쪽)」 · 용도 「러브핸들주사 (옆구리 지방분해 주사)」 | 쿨스컬프팅 어플리케이터 · 지방분해 주사 부위로 복부와 따로 값이 매겨짐 | S277 옆구리(10·1) · S354 러브핸들(3·2) · S493 허리라인(1·0) | 복부 동의어 — 시장가가 복부(1부위)와 러브핸들을 따로 매기므로 비추천 | 사용자(U1) |
| **콧망울** | 새 노드 | 코(묶음) | 용도 detail 「콧망울 지방분해 · 코 라인 날렵하게」 · 위험 부위 nose 본문 「비익」 | 안전이 다름 — nose zone 「비익 괴사 위험」(외비동맥) · 「비익 함몰(alar collapse) … 코 호흡 장애」(비근근 보톡스) | S103 비익(4·0) · S104 ala(1·0) · S121 alar(1·0) · S294 콧구멍(4·0) · S491 콧망울(4·1) | 코 동의어 — 비익 전용 경고가 노드 없이 묻히므로 비추천 | 사용자(U1) |
| **페이스** | 얼굴 동의어 | — | 용도 detail 「페이스/바디/두피」 — 바디 · 두피(최상위)와 나란히 쓴 최상위 뜻 | 얼굴과 다른 시술 · 안전 없음 | S455 페이스(5·1) | 없음. 함께 정리: 풀페이스 → 얼굴 전체 · 페이스라인 → 얼굴 + 고민 「라인」 · 페이스리프팅 → 얼굴 + 목적 「리프팅」 | 사용자(U1) |
| **하관** | 턱(묶음) 동의어 | 얼굴 | 용도 detail 「턱선+하관 라인 정리 전용」 1곳 — 기존 묶음과 같은 범위를 가리키는 말 | 새 시술 · 안전 없음. 문헌 「Botulinum toxin type A contours the lower face」(PMID 33714246)는 교근 보톡스 = 턱 묶음 안 | S328 lower face(2·0) · S329 하안면(5·0) · S486 하안면부(1·0) · S492 하관(4·1) | 얼굴 동의어 — 원천 문맥(「하관 부위 볼살과 불분명한 턱선」)이 턱선 · 볼 아래라 턱(묶음)이 더 좁고 맞다 | 사용자(U1) |
| **팔** | 새 노드 | 바디 | 고민 P10-2 · CC 「겨드랑이/팔/다리」(제모) | 제모는 팔 전체, 팔뚝은 지방 · 탄력(쿨스컬프팅 · EMS) — 범위가 다름. 같은 고민 항목의 「다리」는 OQ-206 에서 노드로 추가됨(선례) | S269 팔(6·2) | 팔뚝 동의어 — 제모 「팔」이 위팔 뒤로 좁아져 비추천 | 사용자(U2) |
| **가슴** | 새 노드 | 바디 | 고민 P10-3 · CC 「수염/가슴/등」(제모) | 제모 · 지방이식(indications 「가슴 확대」) | S312 가슴(8·2) | 바디 동의어 | 사용자(U2) |
| **수염** | 새 노드 | 얼굴 | 고민 P10-3 · CC 「수염/가슴/등」(남성 제모) | 제모 전용 자리 | S402 수염(2·2) | 얼굴 동의어(남성 제모 「얼굴」로 뭉침) | 사용자(U2) |
| **구레나룻** | 새 노드 | 얼굴 | 고민 P10-1 · CC 「인중/구레나룻」(얼굴 제모) | 제모 전용 자리 | S399 구레나룻(2·2) | 얼굴 동의어 | 사용자(U2) |
| **인중** | 새 노드 | 입가 | 고민 P10-1 · CC 「인중/구레나룻」(제모) | 제모 + 보톡스(「짧은 인중 늘리기」) · 필러(「입술라인 및 인중선 확대」) — 입술과 시술이 다름 | S296 인중(4·2) · S309 인중선(2·0) | 입술 동의어 | 사용자(U2) |
| **눈썹** | 새 노드 | 눈가(묶음) | 고민 P1-7 · CC 「눈썹반영구」 | 반영구 · 실 「눈썹 리프팅」 · 보톡스 「눈썹 올리기」. 안전 경고 「눈썹 처짐(Mephisto sign)」(glabella) · 「손상 시 … 눈썹 처짐」(forehead) | S038 눈썹 처짐(4·0) · S039 Mephisto(1·0) · S058 눈썹(24·0) · S384 눈썹반영구(2·2) · S463 눈썹하수(1·0) | 상위를 이마(묶음)로 — 눈썹은 이마와 눈가 사이. 경고가 이마 · 미간 zone 에 있어 이마(묶음)도 가능. 추천은 눈가(묶음)(상담에서 「눈매」 시술로 묶임) | 사용자(U2) |
| **마리오네트** | 새 노드 | 입가 | 고민 P2-2 · CC 「마리오네트라인」 | 필러 · 실리프팅 대상(원천 정의 「입꼬리에서 턱으로 내려가는 주름」). 「팔자주름」 → 노드 팔자와 같은 꼴(D-07) | S319 마리오네트 라인(8·2) · S423 마리오넷(1·0) · S465 마리오네트선(1·0) | 입꼬리 동의어 + 고민 주름 | 사용자(U2) |
| **무릎** | 다리 동의어 | 바디 | 이름 칸 없음 — indications 「무릎 위 지방」 · 「팔뚝/무릎 등 신체 처짐」 | 근거 없음 | S280 무릎(3·0) | 허벅지 동의어(「무릎 위」) — 근거 약 둘 다 | 코디 |
| **불독살** | 턱선 동의어 + 고민 처짐 | 턱(묶음) | 고민 P3-1 · CC 「볼쳐짐/불독살」 — 처진 살(고민)이 붙은 말 | jowl 은 하악연 위 처짐 — jawline zone(Mandibular border) | S390 불독살(2·2) | 볼 동의어 + 고민 처짐 | 코디 |
| **골반저근** | 부위 아님(비미용 적응증) | — | 이름 칸 없음 — EMS indications 「골반저근 강화 (요실금 개선)」 | 미용 상담 부위 아님 | S275 골반저근(2·0) | 새 노드 「골반저」 | 코디 |
| **관절치료** | 부위 아님(비미용 · 계열 밖) | — | 시장가 「줄기세포 관절치료」 — v3 market_rows_skipped 에 이미 빠짐 | 미용 시술 아님 | S357 관절치료(1·1) | 없음 | 코디 |

- 브라라인 · 등살 · 눈썹반영구 · 인중선은 부위 조각이 새 노드안(등 · 눈썹 · 인중)이라 「트리 밖」으로 셌다. 새 노드를 안 받으면 대안 칸으로 간다
- 페이스라인 · 페이스리프팅(얼굴 + 고민/목적)은 「페이스 = 얼굴」이 정해지면 따라간다 — §2-2 얼굴 줄에 이미 넣었다

## 4. 경계 — 묶음 ↔ 좁은 · 얼굴 ↔ 얼굴 전체 · 바디 ↔ 전신

| 경계 | 원천 문자열이 가는 곳 | 근거 |
|---|---|---|
| 이름이 같은 묶음 · 좁은 노드(이마 · 눈가 · 코 · 볼 · 목 + 턱(묶음)) | 원천 문자열 「이마 · 눈가 · 코 · 볼 · 목」은 좁은 노드로. 묶음 노드는 동의어를 갖지 않고 (가) 고민 라벨처럼 하위 이름을 나란히 묶은 칸(「이마/관자놀이」 · 「볼/광대」 · 「턱/턱선」 · 「눈가 쳐짐」) (나) 위험 부위 zone 이름(periorbital · nose · cheek · neck) (다) 그 부위 해부 묶음 이름(Periorbital · Nose · Cheek · Neck · 경부 · 하악 · 하관)만 받는다 | DEC-002 「상위 = 묶음 · 하위 = 그 이름이 가리키는 좁은 부위」 |
| 「턱」 | 턱 단독 · 턱필러 · 턱보톡스 → 턱(묶음). 원천 detail 이 「턱끝 연장」 · 「사각턱 축소」로 하위를 정해 주면 단위 시술(5단계)에서 하위로 내린다 | taxonomy problem P1-3 items detail |
| 얼굴 ↔ 얼굴 전체 | 얼굴 · 안면 · face · 페이스 → 얼굴(최상위 묶음). 전체얼굴 · 얼굴 전체 · 안면 전체 · 전안면 · 풀페이스 → 얼굴 전체. 시장가 「(전체얼굴)」 · 「(풀페이스)」는 모두 얼굴 전체 | DEC-002 D-07 「얼굴 전체」는 부위 노드 · DEC-003 D-05 필링 기본값 |
| 바디 ↔ 전신 | 바디 · 탄탄한 몸 · 몸매 · 신체 처짐 → 바디(묶음). 전신은 「레이저 제모 (전신)」 · 「팔뚝, 복부 등 전신 처짐」 2곳만 노드 「전신」(몸 표면). 그 밖 「전신」 28회 + 전신항노화 · 전신재생 · 전신발진 등은 계통 → 부위 아님(수액은 「해당 없음」) | DEC-003 OQ-306 처리 · _RESUME 10-27 「「전신」 두 뜻 분리」 |
| 「(묶음)」 이름 | v3 트리 이름 그대로(이마(묶음) · 눈가(묶음) · 코(묶음) · 볼(묶음) · 턱(묶음) · 목(묶음)). 입가는 v3 이름 「입가」 그대로 — 좁은 「입가」 노드가 없어 원천 「입가 · 입 주변 · perioral · 구주위」가 바로 이 노드로 간다 | procedure-master-v3.json site_tree |

## 5. 노드 속성안(D)

id 는 제안(`site.<영문>`). 이름 · 상위는 확정 트리 그대로. 동의어 전체 · 등장 수는 json `nodes[].synonyms`.

| id | 이름(상담 용어) | 상위 | 상태 | 해부학 이름 후보(영문 · 한글) | 근거 · 수준 | 위험 부위 대응 | 원천 근거(문자열 · 등장 · 이름 칸) |
|---|---|---|---|---|---|---|---|
| `site.face` | 얼굴 | — | 트리 | Face (facies) · 얼굴 | 레포 literature-evidence.json M1 effects 「contours the lower face」 · M2 moa 「structure and framework to the face」(PMID 33714246 · 32445044) / Terminologia Anatomica 2판(FIPAT 2019) https://fipat.library.dal.ca/ta2/ — **강** | — | 16 · 353 · 21 |
| `site.forehead-group` | 이마(묶음) | 얼굴 | 트리 | Frontal region (regio frontalis) · 이마부위 | Terminologia Anatomica 2판(FIPAT 2019) https://fipat.library.dal.ca/ta2/ · 대한해부학회 『해부학용어』 6판(2014) — 레포에 묶음 이름 없음 — **약** | `forehead` 하위 이마가 소유 | 1 · 3 · 3 |
| `site.forehead` | 이마 | 이마(묶음) | 트리 | Forehead (frons) · 이마 | 레포 anatomy-danger-zones.json zones[forehead].name_en 「Forehead」 · botox_specific.target_muscle 「전두근 (Frontalis)」 — **강** | `forehead` 같음 | 8 · 101 · 14 |
| `site.glabella` | 미간 | 이마(묶음) | 트리 | Glabella · 미간 | 레포 zones[glabella].name_en 「Glabella」 · target_muscle 「추미근 (Corrugator supercilii), 비근근 (Procerus)」 — **강** | `glabella` 같음 | 7 · 84 · 8 |
| `site.temple` | 관자놀이 | 얼굴 | 트리 | Temple / temporal region (regio temporalis) · 관자부위 | 레포 zones[temple].name_en 「Temple」 · target_muscle 「측두근 (Temporalis)」 · tissue_data 「측두부」 — **강** | `temple` 같음 | 10 · 43 · 13 |
| `site.periorbital-group` | 눈가(묶음) | 얼굴 | 트리 | Periorbital region (regio orbitalis) · 눈확부위 | 레포 zones[periorbital].name_en 「Periorbital」 · name_ko 「눈 주변」 — **강** | `periorbital` 묶음(하위 셋 다 덮음) 추천 | 8 · 26 · 5 |
| `site.lateral-canthus` | 눈가 | 눈가(묶음) | 트리 | Lateral canthal area (crow's feet) · 가쪽눈구석 주변 | 레포 zones[periorbital].botox_specific.target_muscle 「안륜근 (Orbicularis oculi) — 까마귀발」 · taxonomy indications 「눈가 주름(crow's feet)」 / 해부 이름 Terminologia Anatomica 2판(FIPAT 2019) https://fipat.library.dal.ca/ta2/(angulus oculi lateralis) — **약** | `periorbital` 상위 묶음 zone | 11 · 111 · 16 |
| `site.infraorbital` | 눈밑 | 눈가(묶음) | 트리 | Infraorbital region · tear trough · 눈확아래부위 · 눈물고랑 | 레포 zones[periorbital].tissue_data.tear_trough_anatomy 「눈물고랑(tear trough)」 / Terminologia Anatomica 2판(FIPAT 2019) https://fipat.library.dal.ca/ta2/(regio infraorbitalis) — **강** | `periorbital` 상위 묶음 zone | 11 · 39 · 10 |
| `site.eyelid` | 눈꺼풀 | 눈가(묶음) | 트리 | Eyelid (palpebra) · 눈꺼풀 | 레포 zones[periorbital].vessels 「내안각동맥 (Medial palpebral artery) — 상하 안검 내측 주행」 · zones[forehead].botox_specific 「상안검거근」 / Terminologia Anatomica 2판(FIPAT 2019) https://fipat.library.dal.ca/ta2/ — **강** | `periorbital` 상위 묶음 zone | 7 · 33 · 5 |
| `site.nose-group` | 코(묶음) | 얼굴 | 트리 | Nose (nasus) · 코 | 레포 zones[nose].name_en 「Nose」 — **강** | `nose` 묶음(코끝 · 콧등 · 콧망울 포함) 추천 | 2 · 3 · 2 |
| `site.nose` | 코 | 코(묶음) | 트리 | External nose · 바깥코 | Terminologia Anatomica 2판(FIPAT 2019) https://fipat.library.dal.ca/ta2/(nasus externus) — 레포에 좁은 「코」의 해부 이름 따로 없음 — **약** | `nose` 상위 묶음 zone | 5 · 53 · 11 |
| `site.nasal-tip` | 코끝 | 코(묶음) | 트리 | Tip of nose (apex nasi) · columella · 코끝 | 레포 zones[nose] 「비첨부 · 비첨」 · tissue_data.nasal_tip_skin_thickness_mm · vessels 「주상동맥 (Columellar artery) — 비주(columella) 내 주행」 — **강** | `nose` 상위 묶음 zone | 6 · 24 · 5 |
| `site.nasal-dorsum` | 콧등 | 코(묶음) | OQ-206 추가 | Dorsum of nose (dorsum nasi) · 콧등 | 레포 zones[nose].vessels 「배비동맥 (Dorsal nasal artery) — 코등(dorsum)을 따라 하행」 · safe_injection_depth 「골막상 (코뼈 부위)」 · complications 「비배부」 — **강** | `nose` 상위 묶음 zone | 8 · 22 · 3 |
| `site.nasal-ala` | 콧망울 | 코(묶음) | **새 노드안** | Ala of nose (ala nasi) · 콧방울 | 레포 zones[nose].vessels 「비익(ala) 외측」 · danger 「비익 괴사 위험」 · botox_specific.risk 「비익 함몰(alar collapse)」 — **강** | `nose` 상위 묶음 zone(비익 괴사 · 함몰 별도 경고) | 5 · 14 · 1 |
| `site.cheek-group` | 볼(묶음) | 얼굴 | 트리 | Cheek (Malar/Buccal) · 볼 | 레포 zones[cheek].name_en 「Cheek (Malar/Buccal)」 — **강** | `cheek` 묶음 추천(Malar=광대 · Buccal=볼 둘 다) | 6 · 16 · 8 |
| `site.cheek` | 볼 | 볼(묶음) | 트리 | Buccal region (regio buccalis) · 볼부위 | 레포 zones[cheek].name_en 「Buccal」 · 「협부」(safe_injection_depth · filler_specific) — **강** | `cheek` 상위 묶음 zone | 13 · 84 · 12 |
| `site.zygoma` | 광대 | 볼(묶음) | 트리 | Zygomatic (malar) region (regio zygomatica) · 광대부위 | 레포 zones[cheek] 「관골부(malar)」 · target_muscle 「광대근 (Zygomaticus)」 — **강** | `cheek` 상위 묶음 zone | 7 · 44 · 5 |
| `site.perioral` | 입가 | 얼굴 | 트리 | Perioral region (regio oralis) · 입부위 | 레포 literature-evidence.json M2 moa 「perioral tissue」(PMID 33633459) · zones[lips].botox_specific.target_muscle 「입가 주름」 · complications 「구주위」 — **강** | `lips` 관련(입가 주름은 lips zone 이 다룸) | 6 · 11 · 0 |
| `site.nasolabial` | 팔자 | 입가 | 트리 | Nasolabial fold (sulcus nasolabialis) · 코입술고랑 | 레포 zones[nasolabial].name_en 「Nasolabial Fold」 · 「비순구」 · extracted 「팔자주름(코입술주름)」 — **강** | `nasolabial` 같음(고민 「주름」 뗌 — D-07) | 10 · 74 · 6 |
| `site.lips` | 입술 | 입가 | 트리 | Lips (labia oris) · 입술 | 레포 zones[lips].name_en 「Lips」 · target_muscle 「구륜근 (Orbicularis oris)」 · 「vermillion border」 — **강** | `lips` 같음 | 16 · 76 · 10 |
| `site.mouth-corner` | 입꼬리 | 입가 | 트리 | Angle of mouth / oral commissure (angulus oris) · 입꼬리 | 레포 zones[lips].clinical_pearls 「구각(oral commissure)」 · zones[chin].tissue_data.dao_coverage 「DAO(구각하제근)」 — **강** | `lips` 관련(구각 · 상순동맥 유입) | 7 · 29 · 1 |
| `site.gingiva` | 잇몸 | 입가 | 트리 | Gingiva (gummy smile 부위) · 잇몸 | 레포 literature-evidence.json M1 effects 「manages gummy smile」(PMID 33714246) — 해부 이름 자체는 Terminologia Anatomica 2판(FIPAT 2019) https://fipat.library.dal.ca/ta2/ — **약** | 위험 부위 원장 없음 | 4 · 7 · 1 |
| `site.marionette` | 마리오네트 | 입가 | **새 노드안** | Marionette line (labiomandibular fold) · 입꼬리-턱 주름 자리 | 레포 extracted.json M7 indications 「마리오네트 라인 (입꼬리에서 턱으로 내려가는 주름)」 — TA 표준 이름 없음(임상 용어) — **약** | `lips` 관련(구각 · DAO) | 3 · 10 · 2 |
| `site.philtrum` | 인중 | 입가 | **새 노드안** | Philtrum · 인중 | Terminologia Anatomica 2판(FIPAT 2019) https://fipat.library.dal.ca/ta2/(philtrum) — 레포에 영문 없음 — **약** | `lips` 관련(상순 · 상구순) | 2 · 6 · 2 |
| `site.chin-group` | 턱(묶음) | 얼굴 | 트리 | Mandibular region (lower jaw) · 아래턱부위 | Terminologia Anatomica 2판(FIPAT 2019) https://fipat.library.dal.ca/ta2/(mandibula) — 레포 「하악」은 뼈 이름 — **약** | 하위 턱끝 · 턱선이 각 zone 소유 | 12 · 55 · 10 |
| `site.chin` | 턱끝 | 턱(묶음) | 트리 | Chin (mentum) · mental region (regio mentalis) · 턱끝부위 | 레포 zones[chin].name_en 「Chin (Mentum)」 · target_muscle 「이근 (Mentalis)」 · 「이부 정중앙」 — **강** | `chin` 턱끝 추천 | 14 · 28 · 7 |
| `site.jawline` | 턱선 | 턱(묶음) | 트리 | Mandibular border (margo inferior mandibulae) · 아래턱뼈 아래모서리 | 레포 zones[jawline].name_en 「Jawline (Mandibular border)」 · 「하악연」 — **강** | `jawline` 같음 | 13 · 137 · 17 |
| `site.masseter` | 사각턱 | 턱(묶음) | 트리 | Mandibular angle · masseter (angulus mandibulae · m. masseter) · 아래턱뼈각 · 깨물근 | 레포 zones[cheek]·[jawline].botox_specific.target_muscle 「교근 (Masseter) — 사각턱」 · 「하악각」(extracted) — **강** | `jawline` 관련(교근 보톡스 경고가 cheek · jawline 두 zone 에) | 8 · 88 · 12 |
| `site.submental` | 턱밑 | 턱(묶음) | 트리 | Submental region (regio submentalis) · 턱끝밑부위 | Terminologia Anatomica 2판(FIPAT 2019) https://fipat.library.dal.ca/ta2/ — 레포는 「턱밑 · 턱 아래 · under the chin」(구어)뿐 — **약** | 위험 부위 원장 없음 | 6 · 102 · 21 |
| `site.full-face` | 얼굴 전체 | 얼굴 | 트리 | Whole face · 얼굴 전체 | 해부 표준 이름 없음(범위 이름) — 레포 「전안면」(complications) · 「안면 전체」 — **약** | 하위 zone 11곳 전부 해당 | 7 · 62 · 33 |
| `site.neck-group` | 목(묶음) | — | 트리 | Neck (collum) · 목 | 레포 zones[neck].name_en 「Neck」 · 「경부」(anatomy botox risk) — **강** | `neck` 묶음 추천 | 2 · 6 · 2 |
| `site.neck` | 목 | 목(묶음) | 트리 | Anterior cervical region · platysma · 앞목부위 · 넓은목근 | 레포 zones[neck].botox_specific.target_muscle 「광경근 (Platysma) — platysmal bands, 목 주름」 — **강** | `neck` 상위 묶음 zone | 21 · 141 · 14 |
| `site.trapezius` | 승모근 | 목(묶음) | 트리 | Trapezius (m. trapezius) · 등세모근 | 레포 taxonomy indications 「사다리꼴근(승모근) 비대증」 / 대한해부학회 『해부학용어』 6판(2014)(등세모근) — **강** | `neck` 관련(부신경) | 4 · 27 · 10 |
| `site.scalp` | 두피 | — | 트리 | Scalp · 머리덮개 | 레포 taxonomy(제품 extracted) 「scalp」 1곳 / Terminologia Anatomica 2판(FIPAT 2019) https://fipat.library.dal.ca/ta2/ — **중** | 위험 부위 원장 없음 | 12 · 81 · 30 |
| `site.body` | 바디 | — | 트리 | Body (trunk · limbs) · 몸통 · 팔다리 | 해부 표준 단일 이름 없음(묶음) — 레포 「body」는 부위 뜻으로 안 쓰임 — **약** | 위험 부위 원장 없음 | 11 · 77 · 22 |
| `site.axilla` | 겨드랑이 | 바디 | 트리 | Axilla (regio axillaris) · 겨드랑부위 | Terminologia Anatomica 2판(FIPAT 2019) https://fipat.library.dal.ca/ta2/ · 대한해부학회 『해부학용어』 6판(2014) — **약** | 위험 부위 원장 없음 | 1 · 9 · 6 |
| `site.upper-arm` | 팔뚝 | 바디 | 트리 | Posterior upper arm (regio brachii posterior) · 위팔 뒤부위 | Terminologia Anatomica 2판(FIPAT 2019) https://fipat.library.dal.ca/ta2/ — 「팔뚝」은 표준국어대사전에선 아래팔 뜻도 있다. 원천 문맥(쿨스컬프팅 · EMS · 바디 쳐짐)은 위팔 뒤 — **약** | 위험 부위 원장 없음 | 1 · 26 · 4 |
| `site.abdomen` | 복부 | 바디 | 트리 | Abdomen (regio abdominalis) · 배부위 | 레포 extracted M10 「복직근」 / Terminologia Anatomica 2판(FIPAT 2019) https://fipat.library.dal.ca/ta2/ — **중** | 위험 부위 원장 없음 | 3 · 61 · 9 |
| `site.flank` | 옆구리 | 바디 | **새 노드안** | Flank (regio lateralis abdominis) · 옆구리 | Terminologia Anatomica 2판(FIPAT 2019) https://fipat.library.dal.ca/ta2/ — 레포 영문 없음(「러브핸들」 구어) — **약** | 위험 부위 원장 없음 | 3 · 14 · 3 |
| `site.back` | 등 | 바디 | **새 노드안** | Back (dorsum · regiones dorsi) · 등부위 | Terminologia Anatomica 2판(FIPAT 2019) https://fipat.library.dal.ca/ta2/ · 대한해부학회 『해부학용어』 6판(2014) — **약** | 위험 부위 원장 없음 | 5 · 15 · 5 |
| `site.chest` | 가슴 | 바디 | **새 노드안** | Chest (regio pectoralis) · breast (mamma) · 가슴부위 | Terminologia Anatomica 2판(FIPAT 2019) https://fipat.library.dal.ca/ta2/ — **약** | 위험 부위 원장 없음 | 1 · 8 · 2 |
| `site.thigh` | 허벅지 | 바디 | 트리 | Thigh (regio femoris) · 넙다리부위 | Terminologia Anatomica 2판(FIPAT 2019) https://fipat.library.dal.ca/ta2/ · 대한해부학회 『해부학용어』 6판(2014) — **약** | 위험 부위 원장 없음 | 2 · 28 · 4 |
| `site.calf` | 종아리 | 바디 | 트리 | Calf (regio surae) · gastrocnemius · 종아리부위 · 장딴지근 | 레포 taxonomy indications 「비복근」 / Terminologia Anatomica 2판(FIPAT 2019) https://fipat.library.dal.ca/ta2/ — **중** | 위험 부위 원장 없음 | 2 · 14 · 2 |
| `site.whole-body` | 전신 | 바디 | 트리 | Whole body surface · 온몸 피부 | 해부 표준 이름 없음(범위 이름) — **약** | 위험 부위 원장 없음 | 2 · 2 · 1 |
| `site.hand` | 손 | 바디 | OQ-206 추가 | Hand (manus) · 손 | Terminologia Anatomica 2판(FIPAT 2019) https://fipat.library.dal.ca/ta2/ · 대한해부학회 『해부학용어』 6판(2014) — **약** | 위험 부위 원장 없음 | 4 · 17 · 3 |
| `site.foot` | 발 | 바디 | OQ-206 추가 | Foot (pes) · 발 | Terminologia Anatomica 2판(FIPAT 2019) https://fipat.library.dal.ca/ta2/ · 대한해부학회 『해부학용어』 6판(2014) — **약** | 위험 부위 원장 없음 | 2 · 6 · 3 |
| `site.leg` | 다리 | 바디 | OQ-206 추가 | Lower limb (membrum inferius) · 다리 · 하지 | 레포 taxonomy problem 「하지정맥류」(하지) / Terminologia Anatomica 2판(FIPAT 2019) https://fipat.library.dal.ca/ta2/ — **중** | 위험 부위 원장 없음 | 4 · 10 · 3 |
| `site.arm` | 팔 | 바디 | **새 노드안** | Upper limb (membrum superius) · 팔 | Terminologia Anatomica 2판(FIPAT 2019) https://fipat.library.dal.ca/ta2/ · 대한해부학회 『해부학용어』 6판(2014) — **약** | 위험 부위 원장 없음 | 1 · 6 · 2 |
| `site.bikini` | 비키니 | 바디 | OQ-206 추가 | Inguinal · pubic region (regio inguinalis · regio pubica) · 샅굴부위 · 두덩부위 | Terminologia Anatomica 2판(FIPAT 2019) https://fipat.library.dal.ca/ta2/ — 「비키니」는 제모 상담 용어 — **약** | 위험 부위 원장 없음 | 1 · 2 · 2 |
| `site.buttock` | 힙 | 바디 | OQ-206 추가 | Gluteal region (regio glutealis) · 볼기부위 | Terminologia Anatomica 2판(FIPAT 2019) https://fipat.library.dal.ca/ta2/ · 대한해부학회 『해부학용어』 6판(2014) — **약** | 위험 부위 원장 없음 | 3 · 17 · 2 |
| `site.eyebrow` | 눈썹 | 눈가(묶음) | **새 노드안** | Eyebrow (supercilium) · 눈썹 | Terminologia Anatomica 2판(FIPAT 2019) https://fipat.library.dal.ca/ta2/ — 레포 「Mephisto sign(눈썹 처짐)」 · 눈썹 처짐 경고 — **약** | `glabella` 관련(forehead · glabella 의 「눈썹 처짐」 경고) | 5 · 32 · 2 |
| `site.beard` | 수염 | 얼굴 | **새 노드안** | Beard area · 수염 자리 | 해부 표준 이름 없음(제모 상담 용어) — **약** | 위험 부위 원장 없음 | 1 · 2 · 2 |
| `site.sideburn` | 구레나룻 | 얼굴 | **새 노드안** | Sideburn (preauricular) area · 귀앞 털 자리 | 해부 표준 이름 없음(제모 상담 용어) — **약** | 위험 부위 원장 없음 | 1 · 2 · 2 |

- 수준: **강** = 레포 파일에 그 영문 · 의학 이름이 있다 · **중** = 레포에 일부(근육 · 한글 의학어)만 · **약** = 레포 밖 표준 용어집에서만 고름. 확정은 의료진(OQ-202) — 값이 있으니 칸은 비지 않는다
- 「팔뚝」은 표준국어대사전 뜻(아래팔)과 미용 상담 뜻(위팔 뒤 「팔뚝살」)이 갈린다. 원천 문맥(쿨스컬프팅 · EMS · 바디 쳐짐)은 위팔 뒤라 그렇게 적고 확인 질문에 올렸다

## 6. 위험 부위 11곳 대응

DEC-002 의 「확인 필요」 5줄에 zone 본문 근거를 붙였다. 최종은 의료진(OQ-202).

| zone | 노드 | 판정 | 근거(zone 본문 키) |
|---|---|---|---|
| `forehead` | 이마 | 같음 | name_ko · name_en |
| `glabella` | 미간 | 같음 | name_ko · name_en |
| `temple` | 관자놀이 | 같음 | name_ko · name_en |
| `periorbital` | 눈가(묶음) | 묶음 추천(확인 필요 → 근거 있음) | target_muscle 「안륜근 — 까마귀발, 눈밑 주름」 · tissue_data.tear_trough_anatomy · clinical_pearls 「하안검 보톡스」 · vessels 「내안각동맥 — 상하 안검 내측 주행」 — 눈가 · 눈밑 · 눈꺼풀 셋 다 |
| `nose` | 코(묶음) | 묶음 추천(확인 필요 → 근거 있음) | safe_injection_depth 「골막상 (코뼈 부위) 또는 연골막상 (비첨부)」 · vessels 주상동맥(비주) · 외비동맥(비익) · 배비동맥(코등) — 코끝 · 콧등 · 콧망울(새) 모두 |
| `nasolabial` | 팔자 | 같음 | 고민 「주름」 뗌(D-07) |
| `cheek` | 볼(묶음) | 묶음 추천(확인 필요 → 근거 있음) | safe_injection_depth 「골막상 (관골부) 또는 피하 (협부)」 · filler_specific 「관골부(malar) … 협부: 피하 캐뉼러」 — 광대 · 볼을 따로 지시 |
| `lips` | 입술 | 같음 + 입꼬리 · 입가 · 인중(새) 관련 | clinical_pearls 「구각(oral commissure)」 · target_muscle 「입가 주름」 · 「상순」 |
| `chin` | 턱끝 | 턱끝 추천(확인 필요 → 근거 있음) | name_en 「Chin (Mentum)」 · safe_injection_depth 「이부 정중앙」 · target_muscle 「이근 (Mentalis)」 · vessels 「턱끝 상방」 — name_ko 「턱」만 넓음 |
| `jawline` | 턱선 | 같음 + 사각턱 관련 | name_en 「Mandibular border」 · target_muscle 「교근 (Masseter) — 사각턱」 |
| `neck` | 목(묶음) | 묶음 추천(확인 필요 → 근거 있음) | target_muscle 「광경근 (Platysma)」(목) + nerves 「부신경 — 승모근, 흉쇄유돌근 운동 — 손상 시 어깨 처짐」(승모근 쪽) |

- 새 노드안의 대응: 콧망울 → `nose`(비익 경고) · 눈썹 → `glabella` · `forehead` 관련(눈썹 처짐 경고) · 인중 · 마리오네트 → `lips` 관련(마리오네트는 `chin` DAO 도) · 바디 · 제모 넷 → 위험 부위 원장 없음(안전하다는 뜻 아님, DEC-001 OQ-119)

## 7. DEC-002 근거 표 정정 · 원천 수정 후보

| 대상 | 지금 | 고칠 것 |
|---|---|---|
| DEC-002 「노드별 원천 근거」 입가(묶음) 줄 | 원천에 「입가」 라는 이름이 없다 | 본문에 있다 — taxonomy 제품 indications 「입가 주름」 · 「입가주름」 · 「팔자주름 및 입가 거상」 · 「눈가, 입가 등 민감 부위의 주름」 · zones[lips].botox_specific.target_muscle 「입가 주름」 · 「입 주변」 · 「구주위」 · perioral(PMID 33633459). 이름 칸(시장가 · 고민 · 용도 · CC)에는 여전히 0 |
| DEC-002 얼굴 전체 줄 | 고민 「P5-4 전체미백」 | P5-4 항목은 백옥주사(글루타치온 IV) · 비타민C주사 둘 다 정맥 — 「전체」는 계통 뜻 → 수액 「해당 없음」(DEC-003). 근거에서 뺀다 |
| DEC-002 전신 줄 | 고민 「P4-3 전신항노화」 · CC 「P4 전신항노화/NAD+수액」 | 계통 뜻 — DEC-003 OQ-306 처리로 「해당 없음」. 몸 표면 「전신」 근거는 시장가 「레이저 제모 (전신)」 · indications 「팔뚝, 복부 등 전신 처짐」 둘 |

원천 수정 후보(B12): ① `anatomy-danger-zones.json` 의 「비근근」이 zones[glabella] 에선 Procerus, zones[nose] 에선 Nasalis — 같은 한글로 두 근육 ② zones[temple].clinical_pearls 「관자궁」 — 관골궁 오기로 보임(근거 약) ③ 다복스 적응증 깨진 글자 「눈�리」(_RESUME 에 이미 있음, 문맥상 눈가)

## 8. 의료진 확인 질문(open 아님 — 값은 들어가 있음)

| 행 | 문자열 | 둔 값 | 질문 |
|---|---|---|---|
| S082 | 하안검 | 눈밑 | 「하안검」 를 눈밑 에 둔다 — 맞나 |
| S237 | 손바닥 | 손 | 「손바닥」 를 손 에 둔다 — 맞나 |
| S238 | 발바닥 | 발 | 「발바닥」 를 발 에 둔다 — 맞나 |
| S272 | 팔뚝 | 팔뚝 | 「팔뚝」 를 팔뚝 에 둔다 — 맞나 |
| S274 | 배 | 복부 | 「배」 를 복부 에 둔다 — 맞나 |
| S306 | 상악골 | 턱(묶음) | 「상악골」 를 턱(묶음) 에 둔다 — 맞나 |
| S307 | 위턱뼈 | 턱(묶음) | 「위턱뼈」 를 턱(묶음) 에 둔다 — 맞나 |
| S310 | 손등 회춘술 | 손 | 「손등 회춘술」 를 손 에 둔다 — 맞나 |
| S311 | 손등 | 손 | 「손등」 를 손 에 둔다 — 맞나 |
| S315 | 임신선 | 복부 | 「임신선」 를 복부 에 둔다 — 맞나 |
| S365 | 턱폭 | 사각턱 | 「턱폭」 를 사각턱 에 둔다 — 맞나 |
| S430 | 눈�리 | 눈가 | 「눈�리」 를 눈가 에 둔다 — 맞나 |
| S432 | 턱근육 | 사각턱 | 「턱근육」 를 사각턱 에 둔다 — 맞나 |
| S449 | 얼굴-목 경계선 | 턱선 | 「얼굴-목 경계선」 를 턱선 에 둔다 — 맞나 |
| S452 | 비순홈 | 팔자 | 「비순홈」 를 팔자 에 둔다 — 맞나 |
| S457 | 애플 페이스 | 볼 | 「애플 페이스」 를 볼 에 둔다 — 맞나 |
| S458 | 중안면부 | 볼(묶음) | 「중안면부」 를 볼(묶음) 에 둔다 — 맞나 |
| S460 | 중안면 | 볼(묶음) | 「중안면」 를 볼(묶음) 에 둔다 — 맞나 |
| S477 | 눈꼬리 | 눈가 | 「눈꼬리」 를 눈가 에 둔다 — 맞나 |
| S490 | 턱살 | 턱밑 | 「턱살」 를 턱밑 에 둔다 — 맞나 |
| DZ | 위험 부위 대응 5줄 | §6 | periorbital · nose · cheek · neck 를 묶음에, chin 을 턱끝에 대는 게 맞나(OQ-202) |
| AN | 해부학 이름 후보 53 | §5 | 후보 영문 · 한글을 확정(OQ-202) |

## 9. 안 한 것

- 시술↔부위 엣지(5 · 8단계) — 안 함
- 기법 목록(4단계) — 조직층 문자열만 넘김
- 원장 · 결정 · 원천 수정 — 안 함
- 사전 기반 매칭이라 사전에 없는 부위 낱말은 놓칠 수 있다 — 부위 형태소 90여 개로 남은 것을 다시 훑어 겹침 외 0 을 확인했다(§2-1). 「…등」 나열 244회는 문맥으로 부위 「등」 8회만 골랐다
