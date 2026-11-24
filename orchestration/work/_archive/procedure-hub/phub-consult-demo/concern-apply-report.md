# 고민 → 케이스 적용 + 케이스 보충 판단 반영 (data · 2026-11-20)

발주 `task_090ba808a9fa` · `ctx_f24499a916d4`. 사용자 11-20 「추천으로 가고」를 따랐다. 커밋 0 · 서브에이전트 0 · 허브 레포 · DB · stg 0 · 사용자 포트 0 · 명동점 BBL 매핑 손대지 않음.

- 스크립트: `silver-model/drafts/clinic-supplement/clinic-a-20261119/build_batch5.py`(재현 · 같은 바이트)
- 로그: `batch5-log.json`
- 기준 사본: `archive/silver-before-clinic-a-20261119-b5/`
- 고치기 전 검사 · 빌드 · gold: `archive/scripts-before-batch5/` · `archive/gold-before-batch5/`

## 1. 결과 한 줄

- **위층(procedure · modality · package) 고민 줄 652 → 0.** 케이스 고민 줄은 276 → **1,630** 이고, 제품 층 797 은 그대로다.
- 새 케이스 **35**, 새 부위 **몸 · 질**, 새 시술 **엑시머 레이저**, 새 고민 **6**, 새 조직 **침샘**.
- **고민 0 케이스 35**(목표 0 · 남은 이유 §7).
- **silver-check PASS(WARN 5) · gold-check PASS(FAIL 0 · WARN 10)** · `gold_hash` **43b95e4e…** · `aux_hash` **58297d11…**.
- 매핑 JSON 324 항목은 두 경로 sha256 이 같다(`e9b257c2…`). 케이스 코드는 바뀌지 않았다.
- 확인 시험 15 고민 모두 적용 전보다 같거나 늘었다. 빠짐 0 · 엉뚱 0(§9).

## 2. 표별 전 → 후

| 표 | 전 | 후 | 무엇 |
|---|---|---|---|
| indication | 1,725 | 2,427 | 위층 652 → 0 · 케이스 276 → 1,630 · 제품 797 그대로 |
| indication_condition | 56 | 73 | 위층 줄 조건을 내린 케이스 줄로 옮김(한 줄이 여러 케이스로 가면 행을 더함) · 안 내린 줄의 조건은 지움 |
| citation_link | 241 | 263 | 같은 방식(위층 indication 8 행) · 안 내린 줄의 링크 1 지움(CTL-0236) |
| statement_translation | 384 | 380 | 지운 링크 CTL-0236 의 번역 4 지움 |
| concern | 260 | 266 | 새 고민 6(전신 상태) |
| concern_site | 103 | 106 | 덮어쓰기 4(바꿈 2 · 더함 2) + 질 주름 × 질 |
| site | 115 | 117 | 몸 · 질 · 몸 부위 16 다시 달기(parent 만) |
| tissue | 25 | 26 | 침샘 |
| procedure · material · procedure_material | 139 · 144 · 176 | 140 · 145 · 177 | 엑시머 레이저 |
| procedure_case | 351 | 386 | 새 35 · 몸만 6 → 몸 · 조직 채움 7(사람 판단 A · B) |
| case_method | 362 | 397 | 새 케이스 방법 |
| source_ref | 51,172 | 55,853 | 위층 indication 근거는 새 케이스 줄로 따라감 · 지운 줄 근거 빠짐 · 새 근거 줄 |

- 새 근거 줄(user.csv)은 꼴 「고민 → 케이스 2026-11-20 · <근거 종류> · <이유>」다. 새 값 전부에 source_ref 가 있다(§8).

## 3. 고민 적용 — 규칙 760 + 사람 판단 21 묶음

- **규칙 760**:
  - 위층 501 은 `붙을 케이스`로 내렸다.
  - 케이스 줄 259 는 그대로 두었다.
  - 같은 (케이스 × 고민)은 한 줄로 만들었다. 근거가 여럿이면 source_ref 를 여러 행으로 달았다. 기존 케이스 줄에 근거를 더한 것이 225 번이다.
- **사람 판단 168 줄**은 `research-concern-link.md` §4 추천대로 했다.

| 묶음 | 줄 | 한 것 |
|---|---|---|
| G01 고민 코드 없는 줄 | 50 | 고민인 말 8 → 새 고민 · 기존 고민으로 전신 투여 케이스에(간 해독 → 스노우주사 · 신진대사 → 마늘주사 · 혈류 → 아르기닌 · 인지기능 → NAD+ · 골밀도 → 비타민D CAS-072 · 영양 → 마이어스칵테일 · 에너지부스트 「신진대사」 → 같은 고민이 붙은 수액 · 이뮨코어 「감염 예방」 → 면역력 저하가 붙은 수액). 「스트레스 해소」는 닻 없음 → 지움. 고민이 아닌 말(평가 · 제품명 · 목표 · 빈 note) 41 → 지움 |
| G2 M4 스킨부스터 | 23 | 얼굴 피부 상태 · 피부 전반 9 → 스킨부스터 6 시술 케이스 전부. 부위 · 몸 14 → 지움 |
| G2 M8 레이저 | 12 | 백반증 · 건선 8 → **새 시술 엑시머 레이저 + 케이스 CAS-133**. 혈관 병변 → CAS-029 · 030 · 031 · 061. 저출력 레이저 상처 · 피부암 전구 병변 · 광선각화증 3 → 지움(추천에 없고 닻 없음) |
| G10 새 케이스 | 12 | 실 · PN · 면사 × 목 · 허벅지 · 팔뚝 · 복부 **새 케이스 21** |
| G2 M2 필러 | 8 | 흉터 3 · 잔주름 → CAS-1046 · 입꼬리주름 → CAS-1043 · 눈 꺼짐 → 눈밑 · 눈꺼풀 · 안와상부. 눈가주름(목록 나열) · 사각턱(역할 턱끝 볼륨) → 지움 |
| G2 M9 기기 리프팅 | 7 | 얼굴 주름 5 → HIFU · 고주파 얼굴 케이스. 이중턱 2 → **새 케이스 고주파 × 턱밑 CAS-3063** |
| G30 패키지 닻 없음 | 7 | 「압출+스킨스케일링」 면포 → 면포압출 CAS-5078(패키지 이름 = 항목). 나머지 6 → 지움 |
| G14 보조 역할 | 6 | 지움 |
| G2 M3 바이오스티뮬레이터 | 6 | 얼굴 케이스 전부 5. 목주름 → **새 케이스 CaHA × 목 CAS-1082**(원장 위험 구역 목 「스킨부스터(Profhilo 등) 또는 희석 CaHA」) |
| G2 M15 | 6 | 지움 |
| G2 M10 | 4 | HIFES · EMS 몸 케이스 CAS-3033 · 3034 |
| G03 | 4 | 그대로(케이스 줄) |
| G07 튼살 | 4 | 튼살 3 → **새 몸 케이스 8**(피코 · 박피 레이저 · TCA · 페놀 · 미라필 · 실크필 · 서브시전 · 마이크로니들링 × 몸). 엑소좀 항산화 → 지움 |
| G12 | 4 | 콧구멍 → 비익 CAS-097 · 매부리 → 코등 CAS-005 · 울퉁불퉁 → 턱끝 CAS-004 · 뾰족턱 → 지움 |
| G2 M13 · M17 · M7 · M5 | 3 · 3 · 3 · 2 | 계열 시술 얼굴 케이스 전부. M5 「색소성 병변」은 원장 「치료 효과는 적은 편」(적응 아님)이라 지움 |
| G06 | 2 | **새 케이스 보톡스 × 인중 CAS-131 · × 턱밑 CAS-132** |
| G04 | 1 | **새 부위 질 + PRF × 질 CAS-1083** |
| G13 | 1 | HIFES × 셀룰라이트 — 추천 없음 · 조직이 안 맞음 → 지움 |

- 추천 칸에 없던 줄(M8 3 · M2 2 · G13 1 · M5 1)은 같은 묶음 추천 꼴로 처리했다. 이유는 `batch5-log.json` `deleted` 에 줄마다 있다.
- 지운 줄은 83 이다. 고민이 아닌 말 41 · M4 부위/몸 14 · 보조 6 · 패키지 6 · M15 6 · 그 밖 10. 원장 원문은 bronze 에 남는다.

## 4. 새 것

### 새 부위

| 코드 | 이름 | 위 | 근거 |
|---|---|---|---|
| SITE-147 | 몸 | SITE-001 전신 | 사용자 결정 2026-11-20 — 얼굴 SITE-007 과 나란한 1단 |
| SITE-148 | 질 | SITE-147 몸 | G04 원장 PRF 「질 주름」 |

- **몸 아래로 다시 단 부위 16**(코드 그대로 · parent 만): 사지 · 상체 · 체간 · 목 · 겨드랑이 · 손 · 발 · 팔 · 다리 · 엉덩이 · 복부 · 옆구리 · 허리 · 등 · 가슴 · 어깨. 「기타」(SITE-122)는 전신 아래에 그대로 두었다.
- **몸만 케이스 → 몸 6**: CAS-044(1060nm 지방) · 3025 · 3026(고주파 지방층) · 3033 HIFES · 3034 EMS · 3044 크라이오. 케이스 보충이 「몸」 근거로 SITE-001 에 넣은 것이다.
- 얼굴 + 몸(문신 · 제모 · 켈로이드 · 지방분해 · 바디 진료항목 케이스)과 전신 투여(수액)는 SITE-001 그대로다.

### 새 고민(전신 상태 · 위 CON-279 전신)

CON-281 간 해독 · 282 신진대사 저하 · 283 혈류 저하 · 284 인지기능 저하 · 285 골밀도 저하 · 286 영양 결핍이다. 모두 name_en(보충)과 description 이 있고, description 근거는 원장 note 를 인용한 근거 줄이다. 「감염 예방」은 기존 CON-263 면역력 저하에 붙였다.

### concern_site(silver 반영)

- 국소 지방 CON-181: 옆구리 → 몸
- 바디 쳐짐 CON-043: 전신 → 몸
- 마리오네트라인 CON-010: + SITE-120 마리오네트라인
- 불독살 CON-025: + SITE-013 하안면
- 질 주름 CON-021: + 질

### 새 시술

- PRC-030 엑시머 레이저(계열 M8 · 재료 MAT-246 엑시머 레이저 ⊂ 레이저).
- 근거는 원장 `extracted.json:/M8/indications/extended/4` 「백반증, 건선 치료 (엑시머 레이저)」다. overview · mechanism 은 원장 문장이 없어 비웠다(C8).
- 케이스: CAS-133 · 전신(얼굴 + 몸) · 레이저 조사 · 표피 · 엑시머 레이저.

### 새 케이스 35(부위 · 방법 · 조직 · 재료 빈칸 0)

| 케이스 | 시술 | 부위 | 방법 | 조직 | 재료 | 묶음 |
|---|---|---|---|---|---|---|
| CAS-131 | PRC-001 보톡스 | 인중 | 근육 주사 | 근육 | 보툴리눔 톡신 A형 | G06 |
| CAS-132 | PRC-001 보톡스 | 턱밑 | 근육 주사 | 근육 | 보툴리눔 톡신 A형 | G06 |
| CAS-1082 | PRC-104 CaHA | 목 | 피하 주사 | 피하지방층 | 칼슘하이드록시아파타이트 | G2 |
| CAS-1083 | PRC-117 PRF | 질 | 피내 주사 | 진피 | 피브린풍부혈장 | G04 |
| CAS-1084 | PRC-110 PN주사 | 목 | 피내 주사 | 진피 | 폴리뉴클레오타이드 | G10 |
| CAS-3055 | PRC-303 PLLA실 | 목 | 실 삽입 | 피하지방층 | 폴리-L-락틱산 | G10 |
| CAS-3056 | PRC-306 PDO 코그실 | 목 | 코그 형태 | 피하지방층 | 폴리디옥사논 | G10 |
| CAS-3057 | PRC-307 PLLA 코그실 | 목 | 코그 형태 | 피하지방층 | 폴리-L-락틱산 | G10 |
| CAS-3058 | PRC-308 PCL 코그실 | 목 | 코그 형태 | SMAS 상층 | 폴리카프로락톤 | G10 |
| CAS-3059 | PRC-306 PDO 코그실 | 허벅지 | 코그 형태 | 피하지방층 | 폴리디옥사논 | G10 |
| CAS-3060 | PRC-307 PLLA 코그실 | 허벅지 | 코그 형태 | 피하지방층 | 폴리-L-락틱산 | G10 |
| CAS-3061 | PRC-308 PCL 코그실 | 허벅지 | 코그 형태 | SMAS 상층 | 폴리카프로락톤 | G10 |
| CAS-3062 | PRC-310 면사리프트 | 목 | 실 삽입 | 피하지방층 | 의료용 면사 | G10 |
| CAS-3063 | PRC-312 고주파 | 턱밑 | 고주파 조사 | 진피 | 고주파 | G2 |
| CAS-3064 | PRC-301 PCL실 | 팔뚝 | 실 삽입 | 피하지방층 | 폴리카프로락톤 | G10 |
| CAS-3065 | PRC-302 PLCL실 | 팔뚝 | 실 삽입 | 피하지방층 | PLCL | G10 |
| CAS-3066 | PRC-306 PDO 코그실 | 팔뚝 | 코그 형태 | 피하지방층 | 폴리디옥사논 | G10 |
| CAS-3067 | PRC-307 PLLA 코그실 | 팔뚝 | 코그 형태 | 피하지방층 | 폴리-L-락틱산 | G10 |
| CAS-3068 | PRC-308 PCL 코그실 | 팔뚝 | 코그 형태 | SMAS 상층 | 폴리카프로락톤 | G10 |
| CAS-3069 | PRC-301 PCL실 | 복부 | 실 삽입 | 피하지방층 | 폴리카프로락톤 | G10 |
| CAS-3070 | PRC-302 PLCL실 | 복부 | 실 삽입 | 피하지방층 | PLCL | G10 |
| CAS-3071 | PRC-306 PDO 코그실 | 복부 | 코그 형태 | 피하지방층 | 폴리디옥사논 | G10 |
| CAS-3072 | PRC-307 PLLA 코그실 | 복부 | 코그 형태 | 피하지방층 | 폴리-L-락틱산 | G10 |
| CAS-3073 | PRC-308 PCL 코그실 | 복부 | 코그 형태 | SMAS 상층 | 폴리카프로락톤 | G10 |
| CAS-3074 | PRC-301 PCL실 | 허벅지 | 실 삽입 | 피하지방층 | 폴리카프로락톤 | G10 |
| CAS-3075 | PRC-302 PLCL실 | 허벅지 | 실 삽입 | 피하지방층 | PLCL | G10 |
| CAS-133 | PRC-030 엑시머 레이저 | 전신 | 레이저 조사 | 표피 | 엑시머 레이저 | G2 |
| CAS-134 | PRC-003 피코레이저 | 몸 | 피코초 펄스 | 진피 | 레이저 | G07 |
| CAS-135 | PRC-004 박피 레이저 | 몸 | 박피성 프락셔널 | 진피 | 레이저 | G07 |
| CAS-5084 | PRC-504 TCA 필링 | 몸 | 점 도포 | 진피 | 트리클로로아세트산 | G07 |
| CAS-5085 | PRC-511 페놀필링 | 몸 | 도포 | 진피 | 페놀 | G07 |
| CAS-5086 | PRC-514 미라필링 | 몸 | 도포 | 진피 | 산호칼슘 미세침 | G07 |
| CAS-5087 | PRC-542 실크필 | 몸 | 도포 | 진피 | 실크 피브로인 | G07 |
| CAS-5088 | PRC-555 서브시전 | 몸 | 피하 박리 | 진피 | 니들 | G07 |
| CAS-5089 | PRC-500 마이크로니들링 | 몸 | 롤러형 | 진피 | 미세바늘 | G07 |

- 방법: 같은 시술 케이스의 가장 많은 방법 묶음(④). 엑시머는 레이저 조사(②).
- 조직: 같은 시술 케이스 조직 과반(④) → 시술 기본. 튼살 몸 케이스는 진피(concern-scope 「튼살 → 피부층(진피)」).
- 재료: 시술 재료 하나(②).

## 5. 케이스 보충 사람 판단 A ~ F(`case-fill-report.md` §6 추천대로)

| # | 한 것 |
|---|---|
| A | 조직 사전 **TIS-027 침샘(샘 조직)** 추가 · CAS-100 · 101 · 102 조직 = 침샘 |
| B | CAS-023 제네시스 = 진피 · CAS-081 태반(경로 미정) = 근육 · CAS-129 · 130 IPL = 멜라닌 |
| C | 복합 성분 재료 19 비움. 성분은 시술 재료(procedure_material)로 읽는다. 검사 예외 이유: 케이스 재료 칸은 한 값이고 대표 성분을 고를 원장 근거가 없다. 공통 상위는 C5(⊆)에 걸린다. silver-check 에는 재료 칸 필수 검사가 없어 예외를 따로 두지 않았다 |
| D · E | 합치지 않음. 같은 조합 묶음 14(묶음 4 의 13 + B 로 생긴 IPL CAS-060 · 129)는 `batch5-log.json` `dup_groups` 이고, silver-check C3 는 이 묶음만 건너뛴다 |
| F | 고주파 목 CAS-3028 · 3029 는 **합치지 않음** — 합칠 후보로 이 리포트에만 남긴다(코드 고정) |

- B 의 IPL 조직(멜라닌)으로 명동점 BBL 진료항목(CAS-129 · 130 을 가리킴)에 기미 · 잡티가 닿기 시작했다(§9). 매핑은 손대지 않았다(사용자 조사 중).

## 6. 고민 0 케이스 채우기

1. 설계 표 「같은 시술 · 같은 조직」 36 을 적용했다(보충 · 같은 시술 다른 케이스). 설계 표 고민 중 **고민 범위(concern-scope.csv)가 그 케이스 부위에 안 드는 것은 뺐다.**
   - 이를 빼지 않으면 확인 시험에서 이중턱이 팔 · 복부 · 허벅지 지방분해 케이스에 닿았다. 바디 필러에 팔자주름 · 볼륨 손실이 닿는 엉뚱도 생겼다.
   - 「원치 않는 체모」는 부위 목록이 좁지만 털은 얼굴 · 몸 어디나라, 모낭(제모) 케이스에는 범위 안으로 쳤다.
   - 결과: 28 케이스 채움 · 8 은 범위가 안 맞아 0 으로 남음.
2. 그 밖 고민 0 케이스에 같은 규칙(범위 거름)을 적용했다 → 19.
3. 그래도 0 인 케이스에는 concern_site 표에서 그 케이스 부위(또는 위 부위)의 고민을 붙였다. 같은 시술 고민과 같은 대분류인 것만이다 → 4(DCA 팔뚝 · 옆구리 · 상복부 · 하복부 ← 팔뚝 · 국소 · 복부 지방).

## 7. 고민 0 케이스 — 남은 35(목표 0 · 이유)

- **같은 시술 다른 케이스엔 고민 있음 — 조직(표적)이 달라 옮길 근거 없음** — 15
  - CAS-028 선택적 광열 레이저 · 전신 · 문신 색소
  - CAS-044 선택적 광열 레이저 · 몸 · 지방세포
  - CAS-051 피코레이저 · 전신 · 문신 색소
  - CAS-063 IPL · 얼굴 · 피지샘
  - CAS-101 보톡스 · 귀밑샘 · 침샘
  - CAS-1066 DCA 지방분해 주사 · 허벅지 안 · 지방세포
  - CAS-1067 DCA 지방분해 주사 · 허벅지 밖 · 지방세포
  - CAS-1068 DCA 지방분해 주사 · 허벅지 승마 · 지방세포
  - CAS-1071 DCA 지방분해 주사 · 부유방 · 지방세포
  - CAS-3030 마이크로웨이브 · 전신 · 피하지방층
  - CAS-3032 HIFES · 얼굴 · 근육
  - CAS-3051 마이크로웨이브 · 얼굴 · 피하지방층
  - CAS-3052 마이크로웨이브 · 전신 · 피하지방층
  - CAS-5068 멀티니들 주입 · 얼굴 · 표피
  - CAS-5069 멀티니들 주입 · 얼굴 · 표피-진피 경계
- **시술 고민 0 — 이 시술 케이스 어디에도 고민이 없음(시술 줄 0 · 계열 · 패키지 줄도 이 시술로 안 내려옴)** — 20
  - CAS-057 비박리성 레이저 · 얼굴 · 진피
  - CAS-058 비박리성 레이저 · 얼굴 · 진피
  - CAS-059 비박리성 레이저 · 얼굴 · 근막층
  - CAS-064 근적외선 타이트닝 · 얼굴 · 진피
  - CAS-070 멀티비타민수액 · 전신 · 혈관
  - CAS-1045 필러 용해 · 얼굴 · 피하지방층
  - CAS-1072 PMMA영구필러 · 얼굴 · 피하지방층
  - CAS-1073 폴리아크릴아미드겔 필러 · 얼굴 · 피하지방층
  - CAS-5030 CO2필 · 얼굴 · 표피
  - CAS-5032 해초필 · 얼굴 · 각질층
  - CAS-5033 허벌 필링 · 얼굴 · 각질층
  - CAS-5042 이지피틱필 · 얼굴 · 각질층
  - CAS-5049 공기압 딥클렌징 · 얼굴 · 표피
  - CAS-5051 산소 주입 피부관리 · 얼굴 · 표피
  - CAS-5063 비타민C 이온토포레시스 · 얼굴 · 표피
  - CAS-5064 니들리스 주입 · 얼굴 · 표피
  - CAS-5065 니들리스 주입 · 얼굴 · 진피
  - CAS-5066 니들리스 주입 · 얼굴 · 진피
  - CAS-5067 니들리스 주입 · 얼굴 · 표피-진피 경계
  - CAS-5072 일렉트로포레이션 · 얼굴 · 표피

- 채우려면 원장 · 제품 문장을 보충 조사해야 한다(지어내기 금지).
  - 「시술 고민 0」 20 은 시술 단위 보충 조사 감이다.
  - 문신 레이저 CAS-028 · 051 은 원장 문신 고민 줄이 토닝 케이스에 붙어 있다(설계 §5). 옮길지 사람 판단이다.

## 8. 검사 · 검증

| 항목 | 결과 |
|---|---|
| 위층 indication | **0**(silver-check 새 검사 C10 · gold-check A1 묶음 5 도 확인) |
| 케이스 고민 0 | 35 = §7 목록 수 |
| 새 케이스 35 부위 · 방법 · 조직 · 재료 빈칸 | 0 · 0 · 0 · 0. 전체 케이스 386 부위 · 방법 · 조직 빈칸 0 · 재료 빈칸 19(§5 C) |
| 새 값 source_ref | 빠진 것 0(indication 새 줄 · 케이스 칸 · 고민 · concern_site · 부위 · 조직 · 시술 · 재료 · procedure_material · case_method · indication_condition · citation_link) |
| 케이스 코드 | 기존 351 그대로 · procedure_code 바뀜 0 · 새 35 끝에 |
| silver-check | **PASS**(WARN 5 — 작업 사본 밖 git) |
| gold-build → glossary-build → gold-check | **PASS**(FAIL 0 · WARN 10) · gold-build 는 고치지 않음 · 재현 A3 묶음 5 바이트 같음 |
| 매핑 JSON | 324 · 두 경로 sha256 `e9b257c25c664873…` 같음 · 진료항목별 케이스 코드 이전과 같음 · 모두 silver 에 있음 · meta 해시 새로 |
| 병원 이름 grep(silver · gold) | 0 |

### 해시

- `gold_hash` **43b95e4e0d7e3de558c14f3e8b71fc1d0c3eec5c216eaf55e3a0cb4d1aa68fde**
- `aux_hash` **58297d11c3d06290bf4cc0d6f64137c1e82176c53019a333accffbaa929a254c**
- 식은 이전과 같다. 묶음 전 사본으로 1a81ae83 이 다시 나오는 것을 확인했다.

### 검사 고친 것(diff)

1. silver-check
   - **C10 위층(시술 · 계열 · 패키지) 고민 줄 0** 을 추가했다.
   - C3 예외 목록에 `batch5-log.json` `dup_groups` 를 더했다.
2. gold-check
   - A1: 묶음 4 대조 대상을 b5 로 바꿨다. 묶음 5 허용 목록을 추가했다. 사전 표는 끝 덧붙임이고, 고민 · 부위 · 케이스 · 근거 표는 바뀜 허용이다(재현 A3 가 바이트 대조). indication 은 위층 0 · 기존 줄 내용 그대로.
   - A3: 묶음 4 재현 → b5, 묶음 5 재현 → 지금 silver · user.csv · batch5-log.


#### silver-check.py

```diff
--- archive/scripts-before-batch5/silver-check.py	2026-11-20 13:10:06
+++ drafts/silver-check/silver-check.py	2026-11-20 13:50:30
@@ -32,6 +32,10 @@
 if os.path.exists(_B4):
     _j = json.load(open(_B4, encoding='utf-8'))
     B4_LOG = {'new_methods': {m[0] for m in _j.get('new_methods', [])}, 'dup_groups': {frozenset(g) for g in _j.get('dup_groups', [])}}
+_B5 = os.path.join(SM, 'drafts', 'clinic-supplement', 'clinic-a-20261119', 'batch5-log.json')          # 묶음 5 — 같은 조합 묶음(사람 판단 B 뒤 · 합치지 않음)
+if os.path.exists(_B5):
+    B4_LOG.setdefault('dup_groups', set())
+    B4_LOG['dup_groups'] |= {frozenset(g) for g in json.load(open(_B5, encoding='utf-8')).get('dup_groups', [])}
 # 11-16 아카이브 이동(work/<slug>/ → work/_archive/procedure-hub/<slug>/) 뒤에도 원장을 찾도록
 # 위로 올라가며 orchestration/work 를 찾는다. 원장은 열린 작업 work/phub-recommend/bronze/ 에 있다.
 WORK = SM
@@ -691,6 +695,10 @@
                 rest = rest.replace(x, '')
             if not ts or rest.strip():
                 hit('C8', 'FAIL', 'procedure', p['code'], f'{fld} 에 원장에 없는 글자 「{rest.strip()[:40]}」')
+    # C10 위층 indication 0(묶음 5 · 사용자 11-20 — 고민은 케이스에만 · 제품 층은 그대로)
+    for x in D['indication']:
+        if x['target_table'] in ('procedure', 'modality', 'package'):
+            hit('C10', 'FAIL', 'indication', x['id'], f'위층 고민 줄({x["target_table"]} {x["target_code"]}) — 고민은 케이스에만')
     _grp = collections.defaultdict(set)
     for x in D['procedure_case']:
         _grp[(x['procedure_code'], x['tissue_code'], x['anatomy_code'], x['site_code'], x['material_code'], frozenset(CMET[x['code']]))].add(x['code'])
@@ -1245,7 +1253,7 @@
     'D7': '사전 이름 · 설명에 수치 0', 'D8': '고민 이름 ≠ 제품 · 계열 · 방법 · 재료 · 기전 이름', 'D9': '설명 근거(field=description)', 'D10': '행 전체 근거(field 빈칸) ≥ 1',
     'N2': 'name_en 있으면 출처 · effect name_en 빈칸 0', 'N3': 'effect name_en 보충이면 name_en 근거 없음', 'E6': '뗀 원장 자리 근거가 관계 행에 없음', 'A7': '이름 · 별칭 띄어쓰기만 다른 겹침',
     'Q1': '설명 「」 인용 = 원장 글자', 'N1': 'name_en 원장 = 근거 글',
-    'C1': '시술 정체 중복 0', 'C2': 'procedure_material ≥ 1', 'C3': '케이스 조합 중복 0', 'C4': '케이스 site 하나', 'C5': '세부 재료 ⊆ 시술 재료 종류(묶음 4 — 같은 값 허용)',
+    'C1': '시술 정체 중복 0', 'C2': 'procedure_material ≥ 1', 'C3': '케이스 조합 중복 0', 'C4': '케이스 site 하나', 'C5': '세부 재료 ⊆ 시술 재료 종류(묶음 4 — 같은 값 허용)', 'C10': '위층(시술 · 계열 · 패키지) 고민 줄 0',
     'C6': '케이스 tissue = anatomy 의 tissue', 'C7': '② 행 근거 ≥ 1', 'C8': '시술 overview · mechanism = 원장 문장', 'C9': '케이스 설명에 효과 · 부작용 없음',
     'C10': '케이스 근거가 가격표뿐 아님', 'C11': '같은 연결 중복 0', 'C12': '제품 → 시술(케이스 없음) — case_product 밖 · 근거 = ② 판정 「제품 + 시술」',
     'O1': '④ 상품 행 근거 ≥ 1', 'O2': '상품 파는 것 · 수량 ≥ 1 · 못 닿음 note', 'O3': '상품 글 칸 = 가격표 원장 글자', 'O4': '상품 가격 · 수량 숫자 = 원문',
```

#### gold-check.py

```diff
--- archive/scripts-before-batch5/gold-check.py	2026-11-20 13:10:49
+++ gold/gold-check.py	2026-11-20 13:51:59
@@ -79,6 +79,10 @@
 B4_APPEND = {f + '.csv' for f in ('case_method', 'method', 'source_ref')}
 B4_CASE_FIELDS = ('tissue_code', 'anatomy_code', 'site_code', 'material_code')
 B4_GENERAL_TAIL = ' 시술의 부위를 정하지 않은 일반 케이스.'
+B5 = os.path.join(SM, 'archive', 'silver-before-clinic-a-20261119-b5')          # 묶음 5 기준 사본(4차 뒤 · 고민 → 케이스 · 사용자 11-20)
+B5S = os.path.join(B5, 'silver')
+B5_APPEND = {f + '.csv' for f in ('concern', 'tissue', 'procedure', 'material', 'procedure_material', 'case_method')}
+B5_CHANGE = {f + '.csv' for f in ('indication', 'indication_condition', 'citation_link', 'statement_translation', 'concern_site', 'site', 'procedure_case', 'source_ref')}
 B2_APPEND = {f + '.csv' for f in ('product', 'organization', 'material', 'procedure', 'procedure_material', 'procedure_case', 'case_product',
                                   'product_organization', 'product_material', 'product_modality', 'alias', 'source_ref')}
 
@@ -160,7 +164,7 @@
     # 묶음 4(build_batch4.py · 사용자 11-20 케이스 보충): 기준 = b4 — procedure_case 기존 행은 tissue · anatomy · site · material 칸(빈칸 → 값)과
     #   「부위를 정하지 않은 일반 케이스」 설명만 바뀜 + 끝 덧붙임(새 케이스) · case_method · method · source_ref 끝 덧붙임 · 그 밖 표 바이트 같음
     for fn in sorted(os.listdir(B4S)):
-        a, b = open(os.path.join(B4S, fn), 'rb').read(), open(os.path.join(SILVER, fn), 'rb').read()
+        a, b = open(os.path.join(B4S, fn), 'rb').read(), open(os.path.join(B5S, fn), 'rb').read()
         if fn in B4_APPEND:
             if not b.startswith(a):
                 bad('A1', f'묶음 4 {fn} 앞쪽(기존 행) 바이트가 바뀜')
@@ -169,7 +173,7 @@
                     if r[0] not in ('procedure_case', 'case_method', 'method') or not r[3].startswith(CLINIC_REF):
                         bad('A1', f'묶음 4 source_ref 덧붙인 행이 목록 밖 {r}')
         elif fn == 'procedure_case.csv':
-            ra, rb = rows(os.path.join(B4S, fn)), rows(os.path.join(SILVER, fn))
+            ra, rb = rows(os.path.join(B4S, fn)), rows(os.path.join(B5S, fn))
             h = ra[0]
             if rb[0] != h or len(rb) < len(ra):
                 bad('A1', '묶음 4 procedure_case 헤더 · 행 수')
@@ -185,6 +189,25 @@
                     bad('A1', f'묶음 4 procedure_case {x[0]} 칸 {col} 바뀜(허용 = 빈칸 채움 · 일반 케이스 설명)')
         elif a != b:
             bad('A1', f'묶음 4 {fn} 바뀜(허용 표 밖)')
+    # 묶음 5(build_batch5.py · 사용자 11-20 고민 → 케이스): 기준 = b5 — 사전 표 끝 덧붙임 · 고민 · 부위 · 케이스 · 근거 표는 바뀜 허용(재현 A3 가 바이트 대조)
+    #   그 밖 표 바이트 같음 · indication 위층 줄 0 · 위층 아닌 기존 줄은 그대로 남거나 지워짐(내용 안 바뀜)
+    for fn in sorted(os.listdir(B5S)):
+        a, b = open(os.path.join(B5S, fn), 'rb').read(), open(os.path.join(SILVER, fn), 'rb').read()
+        if fn in B5_APPEND:
+            if not b.startswith(a):
+                bad('A1', f'묶음 5 {fn} 앞쪽(기존 행) 바이트가 바뀜')
+        elif fn == 'indication.csv':
+            ra, rb = rows(os.path.join(B5S, fn)), rows(os.path.join(SILVER, fn))
+            old = {r[0]: r for r in ra[1:]}
+            for r in rb[1:]:
+                if r[1] in ('procedure', 'modality', 'package'):
+                    bad('A1', f'묶음 5 위층 고민 줄 남음 {r[0]}')
+                if r[0] in old and old[r[0]] != r:
+                    bad('A1', f'묶음 5 기존 고민 줄 {r[0]} 내용 바뀜')
+        elif fn in B5_CHANGE:
+            continue
+        elif a != b:
+            bad('A1', f'묶음 5 {fn} 바뀜(허용 표 밖)')
     now = sorted(f for f in os.listdir(SILVER) if f.endswith('.csv'))
     if now != sorted(os.listdir(CLINIC_BASE)):
         bad('A1', f'silver 표 목록 ≠ 묶음 기준 사본: {sorted(set(now) ^ set(os.listdir(CLINIC_BASE)))}')
@@ -242,12 +265,22 @@
         subprocess.run([sys.executable, os.path.join(SM, 'drafts', 'clinic-supplement', 'clinic-a-20261119', 'build_batch4.py'), B4S, os.path.join(B4, 'user.csv'), out5],
                        capture_output=True, text=True, check=True)
         for fn in sorted(os.listdir(os.path.join(out5, 'silver'))):
-            if open(os.path.join(out5, 'silver', fn), 'rb').read() != open(os.path.join(SILVER, fn), 'rb').read():
-                bad('A3', f'silver {fn} 재현 다름(묶음 4)')
+            if open(os.path.join(out5, 'silver', fn), 'rb').read() != open(os.path.join(B5S, fn), 'rb').read():
+                bad('A3', f'silver {fn} 재현 다름(묶음 4 → 기준 b5)')
         cd = os.path.join(SM, 'drafts', 'clinic-supplement', 'clinic-a-20261119')
-        for fn in ('user.csv', 'batch4-log.json'):
-            if open(os.path.join(out5, fn), 'rb').read() != open(os.path.join(cd, fn), 'rb').read():
-                bad('A3', f'묶음 4 {fn} 재현 다름')
+        if open(os.path.join(out5, 'user.csv'), 'rb').read() != open(os.path.join(B5, 'user.csv'), 'rb').read():
+            bad('A3', '묶음 4 user.csv 재현 다름(→ 기준 b5)')
+        if open(os.path.join(out5, 'batch4-log.json'), 'rb').read() != open(os.path.join(cd, 'batch4-log.json'), 'rb').read():
+            bad('A3', '묶음 4 batch4-log.json 재현 다름')
+        # 묶음 5: b5 위에 build_batch5.py 재현 → 지금 silver · user.csv · batch5-log 와 바이트 대조
+        out6 = os.path.join(tmp, 'batch5')
+        subprocess.run([sys.executable, os.path.join(cd, 'build_batch5.py'), B5S, os.path.join(B5, 'user.csv'), out6], capture_output=True, text=True, check=True)
+        for fn in sorted(os.listdir(os.path.join(out6, 'silver'))):
+            if open(os.path.join(out6, 'silver', fn), 'rb').read() != open(os.path.join(SILVER, fn), 'rb').read():
+                bad('A3', f'silver {fn} 재현 다름(묶음 5)')
+        for fn in ('user.csv', 'batch5-log.json'):
+            if open(os.path.join(out6, fn), 'rb').read() != open(os.path.join(cd, fn), 'rb').read():
+                bad('A3', f'묶음 5 {fn} 재현 다름')
         if open(os.path.join(tmp, 'same-day-judgment.csv'), 'rb').read() != open(os.path.join(NOTES, 'same-day-judgment.csv'), 'rb').read():
             bad('A3', 'notes/same-day-judgment.csv 재현 다름')
     finally:
```


## 9. 확인 시험 — 고민 15(새 gold · 매핑 JSON)

고민은 그 고민 + 아래 고민으로 찾는다. 「설계 적용 뒤」는 `concern-link-check.md`(규칙 줄만)이고, 「실제」는 이번 silver(규칙 + 사람 판단 + 고민 0 채우기)다.

엉뚱은 기계 검사다. 다음 중 하나에 걸리면 엉뚱으로 센다.
- 얼굴 고민 × 몸 케이스
- 제모 항목
- 부위 고민인데 케이스 부위가 고민 부위 위아래 밖

| 고민 | 설계 「적용 뒤」 케이스 → 항목 | 실제 케이스 → 항목 | 적용 전 항목 | 빠짐 | 새로 닿은 진료항목(시술 이름) | 엉뚱 후보 |
|---|---|---|---|---|---|---|
| 여드름 | 32 → 28 | 37 → 34 | 14 | 0 | 물광주사 · 스킨부스터 · 압출관리 · 엑소제 · 엑소좀 · 크라이오 · 포텐자 · 힐로웨이브 | 0 |
| 기미 | 24 → 12 | 35 → 28 | 7 | 0 | BBL HERO (바디) · BBL HERO (페이스) · 물광주사 · 블랙필 · 스킨부스터 · 포텐자 · 힐로웨이브 | 0 |
| 모공 | 44 → 31 | 44 → 31 | 17 | 0 | 라라필 · 볼뉴머 · 써마지FLX · 아이써마지 · 포텐자 · 핑크필 | 0 |
| 입꼬리 처짐 | 1 → 4 | 1 → 4 | 4 | 0 |  | 0 |
| 팔자주름 | 13 → 4 | 23 → 23 | 0 | 0 | 볼뉴머 · 소프웨이브 · 슈링크유니버스 · 슈링크유니버스더마 · 스킨부스터 · 써마지FLX · 울쎄라피 프라임 | 0 |
| 다한증 | 5 → 15 | 5 → 15 | 11 | 0 | 겨드랑이다한증보톡스 | 0 |
| 피부 탄력 저하 | 29 → 24 | 42 → 39 | 3 | 0 | PRP · 더마샤인 · 소프웨이브 · 슈링크유니버스 · 슈링크유니버스더마 · 슈링크유니버스아이 · 스컬트라 · 스킨부스터 · 올리디아120 · 올리디아365 … | 0 |
| 이중턱 | 7 → 3 | 10 → 5 | 0 | 0 | 얼굴지방분해주사 · 이중턱지방분해주사 | 0 |
| 눈가주름 | 6 → 18 | 21 → 18 | 14 | 0 | 볼뉴머 · 슈링크유니버스아이 · 아이써마지 | 0 |
| 사각턱 | 1 → 5 | 1 → 5 | 5 | 0 |  | 0 |
| 셀룰라이트 | 4 → 3 | 4 → 3 | 0 | 0 | 써마지FLX | 0 |
| 잡티 | 11 → 7 | 13 → 13 | 1 | 0 | BBL HERO (바디) · BBL HERO (페이스) · 바디 피코토닝 · 피코토닝 · 피코프락셀 | 0 |
| 홍조 | 8 → 7 | 15 → 14 | 0 | 0 | LDM · 물광주사 · 소노초음파관리 · 스킨부스터 · 힐로웨이브 | 0 |
| 볼륨 손실 | 6 → 6 | 37 → 31 | 0 | 0 | PRP · 바디필러 · 스컬트라 · 스킨부스터 · 애교살필러 · 엑소제 · 엑소좀 · 올리디아120 · 올리디아365 · 쥬베룩 … | 0 |
| 피부 건조 | 8 → 4 | 10 → 5 | 4 | 0 | 소노초음파관리 | 0 |

- 15 모두 적용 전보다 같거나 늘었고, **빠짐 0 · 엉뚱 0** 이다.
- 설계보다 는 것은 사람 판단 묶음(G2 M9 · M4 · M3 · M2) 반영 몫이다. 팔자주름 4 → 23 · 볼륨 손실 6 → 31 · 피부 탄력 저하 24 → 39 다.
- 이중턱은 설계 3 → 5 다. 얼굴 · 이중턱 지방분해주사가 닿았고, 몸 지방분해 항목은 범위 거름으로 빠졌다.
- 기미 · 잡티가 BBL HERO(바디 · 페이스)에 닿은 것은 §5 B(IPL 조직 = 멜라닌) 때문이다. BBL 매핑은 사용자 조사 중이라 그대로 두었다.

## 10. 열린 것

1. 고민 0 케이스 35(§7) — 원장 · 제품 보충 조사로 채울지.
2. BBL 매핑(사용자 조사 중) — CAS-129 · 130 조직이 멜라닌이 되어 색소 고민이 닿는다.
3. 같은 조합 묶음 14 · 고주파 목 3028 · 3029 합칠 후보(코드 고정 원칙).
4. 새 시술 엑시머 레이저의 overview · mechanism(원장 문장 없음)과 새 방법 17 의 그림(앞 묶음).
