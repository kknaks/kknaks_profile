# 케이스 보충 — 모든 케이스의 부위 · 방법 · 조직 · 재료 (data · 2026-11-20)

발주 `task_b5d5b6b31a9b` · `ctx_ba0a972f5218`. 커밋 0 · 서브에이전트 0 · 허브 레포 · DB · stg 0 · 사용자 포트 0 · 식약처 조회 0(필요한 자리 없음 — 아래 §3).

코디 답 2회를 반영했다.
- (a) 새 방법 17 · kind 「시술 방식」 추가 · I2 는 묶음 4 새 방법만 예외.
- C5 ⊆ · C3 는 묶음 4 중복 묶음만 예외 + 사람 판단.

## 1. 결과 한 줄

케이스 344 → **351**(새 7). **부위 빈칸 216 → 0 · 방법 빈칸 247 → 0** · 조직 191 → **7** · 재료 301 → **19** · 해부 326 → 332.
- 남은 조직 7 · 재료 19 가 사람 판단 목록이다.
- 해부는 대부분 하나로 정할 근거가 없어 두었다(§2).
- **silver-check PASS(WARN 5) · gold-check PASS(FAIL 0 · WARN 10)** · `gold_hash` **1a81ae83…** · `aux_hash` **33f6c0dc…**.
- 매핑 JSON 324 항목은 두 경로 sha256 이 같다(`66f3dbc8…`). 케이스 코드는 바뀌지 않았다.

## 2. 칸별 빈칸 전 → 후

| 칸 | 전(344) | 후(351) | 채움 | 남은 이유 |
|---|---|---|---|---|
| 부위 `site_code` | 216 | **0** | 223 | — |
| 방법 `case_method` | 247 케이스 | **0** | 255 행(새 7 포함 254 케이스 · 태반 CAS-081 은 2 방법) | — |
| 조직 `tissue_code` | 191 | **7** | 191 | 사람 판단 §6-A · B(침샘 3 · 원장끼리 다름 1 · 경로 둘 1 · IPL 일반 2) |
| 재료 `material_code` | 301 | **19** | 289 | 사람 판단 §6-C(복합 성분) |
| 해부 `anatomy_code` | 326 | 332 | 1 | 아래 참고 |

- 해부 칸은 두 길로만 채웠다. ① 같은 시술 · 같은 부위 · 같은 조직 케이스의 해부. ② 기존 표 `anatomy_site` 에서 그 부위 × 조직에 닿는 해부 구조가 하나뿐일 때.
- 그렇게 정해지는 것이 1 개뿐이었다. 해부는 「원장이 이름 있는 구조를 말할 때」의 칸(스키마 뜻)이라 넓은 값이 없다. 새 7 케이스도 비어 있어 332 가 됐다.
- 부위 「몸」: 부위 트리에 「몸」 행이 없다(얼굴 SITE-007 이 따로 뿌리). 그래서 몸 · 얼굴 + 몸 · 전신 작용을 모두 **SITE-001 전신**으로 넣었다. 브리프 「몸 = 몸 코드」에 해당하는 코드가 없는 것이다.
- 「부위를 정하지 않은 일반 케이스」 19 개는 부위를 채웠다. 그중 16 개는 2차 묶음이 만들 때 근거 줄에 「(얼굴 전체 · 부위 없는 진료항목)」이라고 적어 두었다. 그래서 **얼굴**(사용자 제공)로 넣었다. 나머지 3(PMMA · PAAG · 꿀광)은 계열 기본 얼굴(⑤)이다. 설명 문장도 「… 일반 케이스 — 세부 부위를 나누지 않고 넓은 부위(얼굴)로 둔다(케이스 보충 2026-11-20).」로 맞췄다. 바뀐 것은 이 문장뿐이다.

## 3. 근거 종류별 수(새 근거 줄 983 = user.csv L400 ~ L1382 · 각 줄 = source_ref 1 행)

| 칸 | ① 원장 케이스 문장 | ② 원장 시술 · 계열 문장 | ④ 같은 시술 다른 케이스 | ⑤ 보충 | 사용자 제공 | 사용자 결정 | 합 |
|---|---|---|---|---|---|---|---|
| 방법(case_method) | 8 | 134 | 7 | 106 | 0 | 0 | 255 |
| 부위 | 0 | 27 | 1 | 179 | 16 | 0 | 223 |
| 조직 | 1 | 28 | 34 | 102 | 26 | 0 | 191 |
| 재료 | 0 | 288 | 0 | 1 | 0 | 0 | 289 |
| 해부 | 0 | 0 | 0 | 1 | 0 | 0 | 1 |
| 새 방법 사전 | 0 | 12 | 0 | 5 | 0 | 0 | 17 |
| 새 케이스 행 | 0 | 0 | 0 | 0 | 0 | 7 | 7 |

- 조직의 ④ 는 **같은 시술 케이스 조직의 과반**일 때만 썼다(동률 · 과반 없음 → 사람 판단). 고주파 · 마이크로웨이브 · 멀티니들은 과반이 없어 시술 기본 조직을 두었다. 고주파 = 진피(② 원장 「RF 에너지가 진피층의 콜라겐 합성을 촉진」), 마이크로웨이브 = 피하지방층(④ CAS-3030), 멀티니들 = 진피(④ 진피 2/4)다.
- ③ 식약처는 0 이다. 투여 경로가 갈리는 자리는 원장 계열 문장(수액 「정맥주사」) · 같은 시술 다른 케이스(태반 「근육/피하」)로 섰다. 표준 지식이면 충분한 자리(성장호르몬 = 피하 · 칼슘 글루콘산 = 정맥)는 ⑤ 로 적었다.
- 「사용자 제공」 42: 조직 26 · 부위 16.
  - 조직: CAS-103 ~ 128(선택적 광열 레이저 × 얼굴 · 몸 부위)은 이 케이스를 가리키는 진료항목이 **제모**라 모낭이다.
  - 부위: 일반 케이스 16 은 만든 근거 줄 「얼굴 전체」에 따라 얼굴이다. 근거 글은 「케이스를 만든 근거 줄 L…」을 가리키고, 병원 이름은 적지 않았다.
- 원칙: 근거 글 꼴은 「케이스 보충 2026-11-20 · <근거 종류> · <이유>」 · source_ref = `drafts/clinic-supplement/clinic-a-20261119/user.csv:L<줄>`. 새 값 전부에 source_ref 가 있다(검증 §8).

### 시술 기본 방법(`$W/procedure-default-method.csv` · 139 시술)

- 근거: 원장 시술 · 계열 문장 61 · 보충 65 · 같은 시술 다른 케이스 11 · 원장 케이스 문장 2.
- 많은 순: 도포 37(필링 · 관리) · 피하 주사 21 · 정맥 투여 20 · 피내 주사 11 · 실 삽입 11 · 레이저 조사 5 · 광 조사 5 · 그 밖.
- 원장이 따로 말한 케이스 방법(스킨보톡스 희석 · 피내 · 롱펄스 · 코그 형태 등 107 행)은 그대로 두고, **방법이 빈 케이스에만** 넣었다.
- 덮어쓴 규칙:
  - 원장 케이스 문장의 층이 진피인 주사 케이스(필러 · 바이오스티뮬레이터 · 스킨부스터 등) → 피내 주사(①).
  - 다한증 보톡스 3 → 피내 주사(⑤ 땀샘 = 진피).
  - 침샘 · 귀밑샘 · 턱밑샘 보톡스 3 → 샘 내 주사(⑤).

## 4. 새 방법 사전 항목 17(그림 행 없음 — 다음 그림 묶음 대상)

kind 는 에너지 계열은 기존 「에너지 조사 방식」, 물리 시술은 새 kind 「시술 방식」(스키마 값에 추가). 모두 `name_en_source = 보충` 이고 description 이 있다.

| 코드 | 이름 | kind | 근거 종류 | 근거 |
|---|---|---|---|---|
| MET-008 | 샘 내 주사 | 투여 경로 | 보충 | 침샘 · 귀밑샘 · 턱밑샘 보톡스는 근육이 아니라 샘 실질에 주사한다 |
| MET-110 | 레이저 조사 | 에너지 조사 방식 | 원장 시술 · 계열 문장 | 시술 · 계열 이름과 재료가 레이저(원장 계열 M8 「레이저」) |
| MET-111 | 광 조사 | 에너지 조사 방식 | 원장 시술 · 계열 문장 | 원장 IPL 「광대역 빛」 · LED 「LED 광자극」 · PDT 「특정 파장 광선」 |
| MET-112 | 집속 초음파 조사 | 에너지 조사 방식 | 원장 시술 · 계열 문장 | 원장 HIFU 「집속초음파 에너지를 정밀하게 SMAS층에 전달」 |
| MET-113 | 고주파 조사 | 에너지 조사 방식 | 원장 시술 · 계열 문장 | 원장 고주파 「RF 에너지가 진피층의 콜라겐 합성을 촉진」 · 니들RF 「니들을 통해 RF 에너지를 전달」 |
| MET-114 | 마이크로파 조사 | 에너지 조사 방식 | 원장 시술 · 계열 문장 | 원장 마이크로웨이브 「마이크로파로 한선 영구 파괴」 · 「심부(진피-피하층)에 선택적 가열」 |
| MET-115 | 집속 전자기장 자극 | 에너지 조사 방식 | 원장 시술 · 계열 문장 | 원장 HIFES 「고강도 집속 전자기장(HIFEM)이 운동신경을 자극하여 근육의 초극대 수축」 |
| MET-116 | 전기 근육 자극 | 에너지 조사 방식 | 원장 시술 · 계열 문장 | 원장 EMS 「EMS 전기자극이 근육 수축을 강제로 유발」 |
| MET-117 | 냉각 | 에너지 조사 방식 | 원장 시술 · 계열 문장 | 원장 크라이오리포라이시스 「지방 동결 파괴」 · 크라이오셀 「극저온 냉각」 |
| MET-118 | 플라즈마 조사 | 에너지 조사 방식 | 원장 시술 · 계열 문장 | 원장 플라즈마 「플라즈마 에너지」 · 「저온 플라즈마가 활성 산소종 … 생성」 |
| MET-125 | 실 삽입 | 시술 방식 | 원장 시술 · 계열 문장 | 원장 계열 M7 「녹는 특수한 실(thread)을 피부 아래에 삽입하는 비수술적 리프팅」 |
| MET-119 | 미세 연마 | 시술 방식 | 원장 시술 · 계열 문장 | 원장 크리스탈필 「피부 표면의 각질층과 노폐물을 물리적으로 제거」 · 재료 알루미늄옥사이드 결정 |
| MET-120 | 분사 · 흡입 세정 | 시술 방식 | 보충 | 아쿠아필 · 공기압 딥클렌징 · 수소필링은 워터젯 · 고압 공기 분사와 흡입으로 세정한다(재료 워터젯 · 고압 공기 · 수소) |
| MET-121 | 수기 마사지 | 시술 방식 | 보충 | 메디컬 경락은 손으로 하는 마사지(재료 마사지) |
| MET-122 | 피하 박리 | 시술 방식 | 원장 시술 · 계열 문장 | 원장 서브시전 「18G Nokor 니들을 피하 섬유 밴드에 삽입하여 물리적으로 절단」 |
| MET-123 | 펀치 절제 | 시술 방식 | 보충 | 펀치시술은 원통형 펀치로 흉터를 도려낸다(재료 펀치) |
| MET-124 | 압출 | 시술 방식 | 보충 | 면포압출은 압출기로 눌러 면포를 짜낸다(재료 물리적 압력) |

- **그림 없는 방법 목록(다음 그림 묶음 대상)**: MET-008 · 110 · 111 · 112 · 113 · 114 · 115 · 116 · 117 · 118 · 119 · 120 · 121 · 122 · 123 · 124 · 125(17).
- silver-check I2 는 `batch4-log.json` 의 `new_methods` 코드만 건너뛴다.

## 5. 새 케이스 7(케이스 없던 시술)

| 케이스 | 시술 | 부위 | 방법 | 조직 | 재료 |
|---|---|---|---|---|---|
| CAS-1075 | PRC-113 아기주사 | 얼굴 | 피내 주사 | 진피 | **사람 판단**(히알루론산 · 성장인자) |
| CAS-1076 | PRC-114 벨벳주사 | 얼굴 | 피내 주사 | 진피 | **사람 판단**(히알루론산 · 콜라겐 펩타이드) |
| CAS-1077 | PRC-117 PRF | 얼굴 | 피내 주사 | 진피 | 피브린풍부혈장 |
| CAS-1078 | PRC-119 SVF지방이식 | 얼굴 | 피하 주사 | 피하지방층 | 자가지방 |
| CAS-1079 | PRC-121 SVF | 얼굴 | 피하 주사 | 피하지방층 | 기질혈관분획 |
| CAS-1080 | PRC-128 GPC주사 | 전신 | 피하 주사 | 지방세포 | 콩 추출물 |
| CAS-1081 | PRC-129 CGF | 얼굴 | 피내 주사 | 진피 | 농축 성장인자 |

- 설명: 「<시술> 시술의 일반 케이스 — 세부 부위를 나누지 않고 넓은 부위로 둔다(케이스 보충 2026-11-20).」
- 근거: 「사용자 결정 · 케이스 = 단위 시술 · 케이스 없는 시술에 일반 케이스」

## 6. 사람 판단 목록 — 묶음 6(39 건 = 칸 26 + 중복 13 묶음)

「KOS n」 = 그 케이스를 가리키는 명동점 진료항목 수.

| # | 묶음 | 건 | 케이스 | 추천 | 이유 |
|---|---|---|---|---|---|
| A | 침샘 · 귀밑샘 · 턱밑샘 보톡스의 조직 | 3 | CAS-100 침샘(KOS 4) · 101 귀밑샘(KOS 4) · 102 턱밑샘(KOS 4) | **조직 사전에 「침샘(샘 조직)」 한 행 추가** 후 셋 다 그 값 | 조직 사전의 샘 조직은 땀샘 · 피지샘뿐이다. 근육으로 넣으면 틀린다 |
| B | 조직이 하나로 안 갈림 | 4 | CAS-023 제네시스(KOS 1 · 원장끼리 멜라닌 · 진피) · CAS-081 태반 경로 미정(KOS 1 · 근육 + 피하) · CAS-129 IPL 얼굴 일반(KOS 4) · CAS-130 IPL 전신(KOS 2) | 023 → **진피** · 081 → **근육** · 129 · 130 → **멜라닌** | 023 은 롱펄스 1064nm 토닝이 진피 가열로 쓰인다는 원장 문장이 있다(설명 notes §6). 081 은 같은 시술 근육 케이스(CAS-079)가 원장 첫 경로다. IPL 은 같은 시술 케이스 표적 4(멜라닌 · 혈관 · 모낭 · 피지샘)가 1 씩이라 과반이 없다. 원장 IPL 문장 「목표 색소(멜라닌, 옥시헤모글로빈)」의 첫 표적이 멜라닌이다. 모두 고르는 값이라 사람 확인 |
| C | 복합 성분 재료 | 19 | 스노우주사 068 · 마이어스칵테일 077 · HP주사 1041 · 꿀광 1074 · 아기 1075 · 벨벳 1076 · PLLA+PCL복합실 3005 · 필링 12(AHA/BHA 5009 KOS 2 · 제스너 5020 · 블랙필링 5025 · 여우필 5026 · 플라필 5027 KOS 1 · PRX 5029 · 퀸즈 5034 · 마꾸필 5038 · 라라닥터 5039 · 체리 5041 · 쿰스 5044 · 핑크필 5047 KOS 1) | **재료 칸은 비워 두고, 성분은 시술 재료(procedure_material)로 읽는다** | 케이스 재료 칸은 한 값이라 복합 제제의 대표 성분을 고를 원장 근거가 없다. 공통 상위(마꾸필 → 미네랄)는 시술 재료보다 위라 C5 에 걸린다 |
| D | 채우니 같은 조합 — 일반 케이스 ↔ 같은 부위 원장 케이스 | 7 묶음 | PN 1023/1055(KOS 0/4) · 배양액 1035/1057(0/2) · 엑소좀 1036/1058(0/3) · HIFU 3016/3046(1/14) · 고주파 3023/3048(0/4) · 니들RF 3039/3053(0/4) · 멀티니들 5070/5083(0/1) | **합치지 않고 둔다.** 일반 케이스(진료항목이 가리킴)는 「장비 · 제품 연결」로, 원장 케이스는 원장 문장(층 · 방식)으로 갈린다. 합칠 때는 원장 케이스 쪽으로 진료항목을 옮기는 것이 맞다 | 일반 케이스는 얼굴 전체 진료항목용으로 만든 것이다. 넓은 값(얼굴 · 대표 조직 · 기본 방법)이 원장 케이스와 겹쳤을 뿐이다. 합치면 매핑 JSON 의 케이스 코드가 바뀐다(코드 고정 원칙) |
| E | 채우니 같은 조합 — 이름 · 장비로만 다른 케이스 | 4 묶음 | TCA 5011 알라딘필링 / 5012 TCA크로스(0/0) · 글리콜산 5013 기본 / 5014 블랙필(0/1) · LED 5053 기본 / 5054(1/0) · 초음파 5060 LDM / 5061 벨라소닉 / 5082 일반(3/0/2) | **합치지 않는다.** 이름 · 장비(제품 연결)로 갈린다. 5013 · 5053 · 5082(기본 · 일반)는 D 와 같은 꼴 | 원장이 이름 · 장비를 따로 적은 단위다 |
| F | 채우니 같은 조합 — 같은 부위 두 원장 케이스 | 2 묶음 | 고주파 목 3028 / 3029(0/0) · 마이크로웨이브 전신 3030 / 3052(0/6) | 3028 · 3029 → **합칠 후보**(원장 「목전용 HIFU/RF」 · 「목 부위 전용」 같은 뜻) · 3030 · 3052 → **그대로**(3030 은 원장 층 문장 · 3052 는 진료항목 일반) | 3028 은 원장이 층을 안 말해 시술 기본(진피)이 돼 3029 와 겹쳤다 |

- 중복 13 묶음(D 7 · E 4 · F 2 · 29 케이스)은 `batch4-log.json` 의 `dup_groups` 다. silver-check C3 는 이 묶음만 건너뛴다.
- 부위 · 방법 빈칸이 남은 케이스는 0 이다. 사람 판단 목록에는 부위 · 방법 칸이 없다. 브리프 검증 「빈칸 0(목록 제외 · 그 수 = 목록 수)」에서 목록 수 = 0 이다.

## 7. 확인 예

| 케이스 | 부위 | 방법 | 조직 | 재료 | 근거(user.csv) |
|---|---|---|---|---|---|
| CAS-006 입꼬리 보톡스 | 입꼬리(원래) | **근육 주사** | 근육(원래) | **보툴리눔 톡신 A형** | L429 방법 ② 원장 M1 「주사 맞은 부위의 근육」 · L1098 재료 ② 시술 재료 하나 |
| CAS-016 스킨보톡스 | **얼굴** | 희석 주입 + 피내 주사(원래 · 그대로) | 진피(원래) | **보툴리눔 톡신 A형** | L679 부위 ⑤ · L1108 재료 ② |
| CAS-021 레이저토닝 | **얼굴** | 큐스위치 + 저에너지 반복 조사(원래) | 멜라닌(원래) | 1064nm(원래) | L681 부위 ⑤ 「피부 레이저 = 얼굴」 |
| CAS-065 백옥주사(수액) | **전신** | 정맥 투여(원래) | **혈관** | **글루타치온** | L716 부위 ② 원장 M16 「혈관에 직접 투여」 · L904 조직 ⑤ 정맥 → 혈관 · L1124 재료 ② |
| CAS-5078 면포압출 | **얼굴** | **압출**(새 MET-124) | **모낭** | **물리적 압력** | L676 방법 ⑤ · L898 부위 ⑤ · L1088 조직 ⑤ · L1376 재료 ② |

## 8. 검사 · 검증

| 항목 | 결과 |
|---|---|
| silver-check | **PASS**(WARN 5 — 작업 사본 밖 git 변경) · silver 해시 `55dbbd4f…` |
| gold-build → glossary-build → gold-check | **PASS**(FAIL 0 · WARN 10) · gold-build 는 고치지 않음 |
| 케이스 부위 · 방법 빈칸 | 0 / 351 |
| 조직 · 재료 빈칸 | 7 · 19 = 사람 판단 A · B · C 수와 같음 |
| 새 값 source_ref | 빠진 것 0(procedure_case 칸 · case_method 새 행 · method 새 행 · 새 케이스 행 전부) |
| 케이스 코드 | 기존 344 그대로 · procedure_code 바뀜 0 · 새 7 은 끝에 덧붙임 |
| 매핑 JSON | 324 항목 · 두 경로 sha256 `66f3dbc8…` 같음 · 진료항목별 케이스 코드 이전과 같음 · 모두 silver 에 있음 · meta 해시 새로 |
| 병원 이름 · 진료항목 코드 grep(silver · gold) | 0 · 새 user.csv 줄에도 병원 이름 0 |
| 재현 | `build_batch4.py` 를 기준 사본 위에 다시 돌리면 silver · user.csv · batch4-log 바이트가 같다(gold-check A3) |
| 기준 사본 | `archive/silver-before-clinic-a-20261119-b4/`(silver 59 + user.csv) · 고치기 전 검사 · 빌드 · gold 는 `archive/scripts-before-batch4/` · `archive/gold-before-batch4/` |

- `method.csv` 는 기준 파일이 `\r\n` 줄 끝이라 그대로 지켰다(처음 실행에서 A1 「앞쪽 바이트가 바뀜」 1 건 → 스크립트가 표마다 기준 줄 끝을 따르게 고침).

### 해시

- `gold_hash` **1a81ae8314b6b4475a54bccb0b6d969957cc524b4773f02650150ce50574a635**
- `aux_hash` **33f6c0dc5d62150d2c3fa069f55fc9bfc95a479f89cc482d3a87fa7d3683190c**
- 둘 다 이전과 같은 식(gold/*.csv · source_ref + concern + adverse + condition + concern_site + notes/ledger-check-list.csv)이다. 묶음 전 사본으로 7b8669b7 · 624f1e25 가 다시 나오는 것을 확인했다.

## 9. 검사 고친 것(diff)

1. silver-check
   - I2: 묶음 4 새 방법 코드는 그림 행 없어도 통과.
   - C3: 묶음 4 중복 묶음은 건너뜀.
   - C5: 세부 재료 ⊂ → **⊆**(시술 재료 그 자체 = 넓은 값 허용 · 무관한 재료는 여전히 FAIL).
2. silver-schema: method.kind 값에 「시술 방식」.
3. gold-check
   - A1: 묶음 3 대조 대상을 b4 로 바꿈. 묶음 4 허용 목록(procedure_case 빈칸 → 값 · 일반 케이스 설명 · 끝 덧붙임 / case_method · method · source_ref 끝 덧붙임)을 추가.
   - A3: 묶음 3 재현 → b4, 묶음 4 재현 → 지금 silver · user.csv · batch4-log.


### silver-check.py

```diff
--- archive/scripts-before-batch4/silver-check.py	2026-11-19 16:29:22
+++ drafts/silver-check/silver-check.py	2026-11-20 13:10:06
@@ -27,6 +27,11 @@
 
 HERE = os.path.dirname(os.path.abspath(__file__))
 SM = os.path.normpath(os.path.join(HERE, '..', '..'))
+_B4 = os.path.join(SM, 'drafts', 'clinic-supplement', 'clinic-a-20261119', 'batch4-log.json')          # 묶음 4 예외 목록(I2 새 방법 · C3 중복 묶음)
+B4_LOG = {}
+if os.path.exists(_B4):
+    _j = json.load(open(_B4, encoding='utf-8'))
+    B4_LOG = {'new_methods': {m[0] for m in _j.get('new_methods', [])}, 'dup_groups': {frozenset(g) for g in _j.get('dup_groups', [])}}
 # 11-16 아카이브 이동(work/<slug>/ → work/_archive/procedure-hub/<slug>/) 뒤에도 원장을 찾도록
 # 위로 올라가며 orchestration/work 를 찾는다. 원장은 열린 작업 work/phub-recommend/bronze/ 에 있다.
 WORK = SM
@@ -686,7 +691,12 @@
                 rest = rest.replace(x, '')
             if not ts or rest.strip():
                 hit('C8', 'FAIL', 'procedure', p['code'], f'{fld} 에 원장에 없는 글자 「{rest.strip()[:40]}」')
+    _grp = collections.defaultdict(set)
+    for x in D['procedure_case']:
+        _grp[(x['procedure_code'], x['tissue_code'], x['anatomy_code'], x['site_code'], x['material_code'], frozenset(CMET[x['code']]))].add(x['code'])
     for k, c in collections.Counter((x['procedure_code'], x['tissue_code'], x['anatomy_code'], x['site_code'], x['material_code'], frozenset(CMET[x['code']])) for x in D['procedure_case']).items():
+        if c > 1 and frozenset(_grp[k]) in B4_LOG.get('dup_groups', set()):
+            continue          # 묶음 4(사용자 11-20): 칸을 채워 같은 조합이 된 케이스 — 케이스 코드 고정 · 합치기는 사람 판단 목록
         if c > 1:
             hit('C3', 'FAIL', 'procedure_case', str(k[:5]), f'케이스 조합 중복 ×{c}')
 
@@ -702,7 +712,7 @@
             hit('C4', 'FAIL', 'procedure_case', k, f'site 하나 아님 「{x["site_code"]}」')
         if re.search(r'[()（）]', x['name_ko']):
             hit('D2', 'FAIL', 'procedure_case', k, '이름 괄호')
-        if x['material_code'] and x['procedure_code'] in PR and not (PMAT[x['procedure_code']] & set(mat_up(x['material_code'])[1:])):
+        if x['material_code'] and x['procedure_code'] in PR and not (PMAT[x['procedure_code']] & set(mat_up(x['material_code']))):          # ⊆ (묶음 4 · 사용자 11-20 — 시술 재료 그 자체 = 넓은 값 허용)
             hit('C5', 'FAIL', 'procedure_case', k, '세부 재료가 시술 재료 종류의 하위가 아님')
         if x['anatomy_code'] in BY['anatomy'] and BY['anatomy'][x['anatomy_code']]['tissue_code'] and x['tissue_code'] != BY['anatomy'][x['anatomy_code']]['tissue_code']:
             hit('C6', 'FAIL', 'procedure_case', k, 'tissue ≠ anatomy 의 tissue')
@@ -929,7 +939,10 @@
             hit('I1', 'FAIL', 'concept_image', r['id'], f'가리킨 사전 행 없음 {r["target_table"]} {r["target_code"]}')
     dict_codes = KS['mechanism'] | KS['method']
     img_codes = {r['target_code'] for r in D['concept_image']}
+    # 묶음 4(케이스 보충 · 사용자 11-20): 새 방법 사전 항목은 그림 행 없이 둠 — 다음 그림 묶음 대상(case-fill-report.md 목록)
     for c in sorted(dict_codes - img_codes):
+        if c in B4_LOG.get('new_methods', set()):
+            continue
         hit('I2', 'FAIL', 'concept_image', c, '사전 코드에 그림 행 없음')
     for c in sorted(img_codes - dict_codes):
         hit('I2', 'FAIL', 'concept_image', c, '그림 행 코드가 사전(mechanism ∪ method)에 없음')
@@ -1232,7 +1245,7 @@
     'D7': '사전 이름 · 설명에 수치 0', 'D8': '고민 이름 ≠ 제품 · 계열 · 방법 · 재료 · 기전 이름', 'D9': '설명 근거(field=description)', 'D10': '행 전체 근거(field 빈칸) ≥ 1',
     'N2': 'name_en 있으면 출처 · effect name_en 빈칸 0', 'N3': 'effect name_en 보충이면 name_en 근거 없음', 'E6': '뗀 원장 자리 근거가 관계 행에 없음', 'A7': '이름 · 별칭 띄어쓰기만 다른 겹침',
     'Q1': '설명 「」 인용 = 원장 글자', 'N1': 'name_en 원장 = 근거 글',
-    'C1': '시술 정체 중복 0', 'C2': 'procedure_material ≥ 1', 'C3': '케이스 조합 중복 0', 'C4': '케이스 site 하나', 'C5': '세부 재료 ⊂ 시술 재료 종류',
+    'C1': '시술 정체 중복 0', 'C2': 'procedure_material ≥ 1', 'C3': '케이스 조합 중복 0', 'C4': '케이스 site 하나', 'C5': '세부 재료 ⊆ 시술 재료 종류(묶음 4 — 같은 값 허용)',
     'C6': '케이스 tissue = anatomy 의 tissue', 'C7': '② 행 근거 ≥ 1', 'C8': '시술 overview · mechanism = 원장 문장', 'C9': '케이스 설명에 효과 · 부작용 없음',
     'C10': '케이스 근거가 가격표뿐 아님', 'C11': '같은 연결 중복 0', 'C12': '제품 → 시술(케이스 없음) — case_product 밖 · 근거 = ② 판정 「제품 + 시술」',
     'O1': '④ 상품 행 근거 ≥ 1', 'O2': '상품 파는 것 · 수량 ≥ 1 · 못 닿음 note', 'O3': '상품 글 칸 = 가격표 원장 글자', 'O4': '상품 가격 · 수량 숫자 = 원문',
```

### gold-check.py

```diff
--- archive/scripts-before-batch4/gold-check.py	2026-11-20 11:07:51
+++ gold/gold-check.py	2026-11-20 13:10:49
@@ -74,6 +74,11 @@
 B3 = os.path.join(SM, 'archive', 'silver-before-clinic-a-20261119-b3')          # 묶음 3 기준 사본(2차 뒤 · 케이스 = 단위 시술 · 사용자 11-20)
 B3S = os.path.join(B3, 'silver')
 B3_APPEND = {f + '.csv' for f in ('procedure_case', 'case_product', 'indication')}
+B4 = os.path.join(SM, 'archive', 'silver-before-clinic-a-20261119-b4')          # 묶음 4 기준 사본(3차 뒤 · 케이스 보충 · 사용자 11-20)
+B4S = os.path.join(B4, 'silver')
+B4_APPEND = {f + '.csv' for f in ('case_method', 'method', 'source_ref')}
+B4_CASE_FIELDS = ('tissue_code', 'anatomy_code', 'site_code', 'material_code')
+B4_GENERAL_TAIL = ' 시술의 부위를 정하지 않은 일반 케이스.'
 B2_APPEND = {f + '.csv' for f in ('product', 'organization', 'material', 'procedure', 'procedure_material', 'procedure_case', 'case_product',
                                   'product_organization', 'product_material', 'product_modality', 'alias', 'source_ref')}
 
@@ -135,7 +140,7 @@
     # 묶음 3(build_batch3.py · 사용자 11-20): 기준 = b3 — procedure_case · case_product · indication 끝 덧붙임 · product_procedure 헤더만 ·
     #   source_ref = 기준에서 product_procedure 대상 행만 빠진 것 + 끝 덧붙임 · 그 밖 표 바이트 같음
     for fn in sorted(os.listdir(B3S)):
-        a, b = open(os.path.join(B3S, fn), 'rb').read(), open(os.path.join(SILVER, fn), 'rb').read()
+        a, b = open(os.path.join(B3S, fn), 'rb').read(), open(os.path.join(B4S, fn), 'rb').read()
         if fn in B3_APPEND:
             if not b.startswith(a):
                 bad('A1', f'묶음 3 {fn} 앞쪽(기존 행) 바이트가 바뀜')
@@ -143,7 +148,7 @@
             if b != a.split(b'\n', 1)[0] + b'\n':
                 bad('A1', '묶음 3 product_procedure 가 헤더만이 아님')
         elif fn == 'source_ref.csv':
-            ra, rb = rows(os.path.join(B3S, fn)), rows(os.path.join(SILVER, fn))
+            ra, rb = rows(os.path.join(B3S, fn)), rows(os.path.join(B4S, fn))
             keep = [r for r in ra if r[0] != 'product_procedure']
             if rb[:len(keep)] != keep:
                 bad('A1', '묶음 3 source_ref 기존 행이 「product_procedure 대상만 빠짐」 이 아님')
@@ -152,6 +157,34 @@
                     bad('A1', f'묶음 3 source_ref 덧붙인 행 대상 표가 목록 밖 {r}')
         elif a != b:
             bad('A1', f'묶음 3 {fn} 바뀜(허용 표 밖)')
+    # 묶음 4(build_batch4.py · 사용자 11-20 케이스 보충): 기준 = b4 — procedure_case 기존 행은 tissue · anatomy · site · material 칸(빈칸 → 값)과
+    #   「부위를 정하지 않은 일반 케이스」 설명만 바뀜 + 끝 덧붙임(새 케이스) · case_method · method · source_ref 끝 덧붙임 · 그 밖 표 바이트 같음
+    for fn in sorted(os.listdir(B4S)):
+        a, b = open(os.path.join(B4S, fn), 'rb').read(), open(os.path.join(SILVER, fn), 'rb').read()
+        if fn in B4_APPEND:
+            if not b.startswith(a):
+                bad('A1', f'묶음 4 {fn} 앞쪽(기존 행) 바이트가 바뀜')
+            elif fn == 'source_ref.csv':
+                for r in _c.reader(_io.StringIO(b[len(a):].decode('utf-8'))):
+                    if r[0] not in ('procedure_case', 'case_method', 'method') or not r[3].startswith(CLINIC_REF):
+                        bad('A1', f'묶음 4 source_ref 덧붙인 행이 목록 밖 {r}')
+        elif fn == 'procedure_case.csv':
+            ra, rb = rows(os.path.join(B4S, fn)), rows(os.path.join(SILVER, fn))
+            h = ra[0]
+            if rb[0] != h or len(rb) < len(ra):
+                bad('A1', '묶음 4 procedure_case 헤더 · 행 수')
+                continue
+            for x, y in zip(ra[1:], rb[1:]):
+                for k, col in enumerate(h):
+                    if x[k] == y[k]:
+                        continue
+                    if col in B4_CASE_FIELDS and x[k] == '':
+                        continue
+                    if col == 'description' and x[k].endswith(B4_GENERAL_TAIL):
+                        continue
+                    bad('A1', f'묶음 4 procedure_case {x[0]} 칸 {col} 바뀜(허용 = 빈칸 채움 · 일반 케이스 설명)')
+        elif a != b:
+            bad('A1', f'묶음 4 {fn} 바뀜(허용 표 밖)')
     now = sorted(f for f in os.listdir(SILVER) if f.endswith('.csv'))
     if now != sorted(os.listdir(CLINIC_BASE)):
         bad('A1', f'silver 표 목록 ≠ 묶음 기준 사본: {sorted(set(now) ^ set(os.listdir(CLINIC_BASE)))}')
@@ -200,10 +233,21 @@
         subprocess.run([sys.executable, os.path.join(SM, 'drafts', 'clinic-supplement', 'clinic-a-20261119', 'build_batch3.py'), B3S, os.path.join(B3, 'user.csv'), out4],
                        capture_output=True, text=True, check=True)
         for fn in sorted(os.listdir(os.path.join(out4, 'silver'))):
-            if open(os.path.join(out4, 'silver', fn), 'rb').read() != open(os.path.join(SILVER, fn), 'rb').read():
-                bad('A3', f'silver {fn} 재현 다름(묶음 3)')
-        if open(os.path.join(out4, 'user.csv'), 'rb').read() != open(os.path.join(SM, 'drafts', 'clinic-supplement', 'clinic-a-20261119', 'user.csv'), 'rb').read():
-            bad('A3', '묶음 근거 파일 user.csv 재현 다름(묶음 3)')
+            if open(os.path.join(out4, 'silver', fn), 'rb').read() != open(os.path.join(B4S, fn), 'rb').read():
+                bad('A3', f'silver {fn} 재현 다름(묶음 3 → 기준 b4)')
+        if open(os.path.join(out4, 'user.csv'), 'rb').read() != open(os.path.join(B4, 'user.csv'), 'rb').read():
+            bad('A3', '묶음 근거 파일 user.csv 재현 다름(묶음 3 → 기준 b4)')
+        # 묶음 4: b4 위에 build_batch4.py 재현 → 지금 silver · user.csv · batch4-log 와 바이트 대조
+        out5 = os.path.join(tmp, 'batch4')
+        subprocess.run([sys.executable, os.path.join(SM, 'drafts', 'clinic-supplement', 'clinic-a-20261119', 'build_batch4.py'), B4S, os.path.join(B4, 'user.csv'), out5],
+                       capture_output=True, text=True, check=True)
+        for fn in sorted(os.listdir(os.path.join(out5, 'silver'))):
+            if open(os.path.join(out5, 'silver', fn), 'rb').read() != open(os.path.join(SILVER, fn), 'rb').read():
+                bad('A3', f'silver {fn} 재현 다름(묶음 4)')
+        cd = os.path.join(SM, 'drafts', 'clinic-supplement', 'clinic-a-20261119')
+        for fn in ('user.csv', 'batch4-log.json'):
+            if open(os.path.join(out5, fn), 'rb').read() != open(os.path.join(cd, fn), 'rb').read():
+                bad('A3', f'묶음 4 {fn} 재현 다름')
         if open(os.path.join(tmp, 'same-day-judgment.csv'), 'rb').read() != open(os.path.join(NOTES, 'same-day-judgment.csv'), 'rb').read():
             bad('A3', 'notes/same-day-judgment.csv 재현 다름')
     finally:
```

### silver-schema.json

```diff
--- archive/scripts-before-batch4/silver-schema.json	2026-11-17 21:14:28
+++ drafts/silver-check/silver-schema.json	2026-11-20 13:09:59
@@ -1719,7 +1719,7 @@
     },
     {
      "name": "kind",
-     "meaning": "투여 경로 / 주입 방식 / 도구 / 에너지 조사 방식 / 흡수 촉진 / 실 형태 / 재료 처리(추가 kind)",
+     "meaning": "투여 경로 / 주입 방식 / 도구 / 에너지 조사 방식 / 흡수 촉진 / 실 형태 / 재료 처리(추가 kind) / 시술 방식(묶음 4 · 사용자 11-20 — 실 삽입 · 박리 · 절제 · 압출 · 마사지 · 연마 · 세정)",
      "doc": "method",
      "fk": null,
      "values": [
@@ -1729,7 +1729,8 @@
       "에너지 조사 방식",
       "흡수 촉진",
       "실 형태",
-      "재료 처리"
+      "재료 처리",
+      "시술 방식"
      ],
      "vocab": true
     },
```


## 10. 열린 것

1. 사람 판단 §6 묶음 6(특히 A 조직 사전 「침샘」 추가 · D 일반 케이스와 원장 케이스를 합칠지).
2. 새 방법 17 그림(다음 그림 묶음).
3. 해부 칸 332 빈칸 — 이번 원칙(넓은 값)으로는 채울 값이 없다. 해부를 케이스 필수 칸으로 볼지 정해야 한다.
4. 「몸」 부위 코드: 트리에 없어 SITE-001 로 넣었다. 얼굴 · 몸을 가르려면 「몸」 행을 새로 둘지 정해야 한다.
5. 「고민 → 케이스」 설계 워커 참고: 부위가 생긴 일반 케이스(얼굴 · 전신)는 `concern_site` 의 자기 · 조상 · 자손 규칙에 닿기 시작한다. 특히 SITE-001 전신에 몸 부위 고민이 닿는다.
