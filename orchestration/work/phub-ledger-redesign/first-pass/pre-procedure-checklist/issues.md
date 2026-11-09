# issues — pre-procedure-checklist.json 1차 미결

코드: **A**=에이전트 추출/해석 오류 · **B**=원문 정보 부족 · **C**=현재 사용자 결정 필요 · 보조: **K**=알려진 분석 한계 · **P**=잠정 관찰 · **F**=후속 의미 조사 · **I**=원문 내 불일치(원문 변경 제안은 후속 확인 후보이며 지금 선택 대기 아님)

상태: open(열림) · fixed(에이전트가 고침·재검증) · recorded(한계로 기록, 1차 종료를 막지 않음) · deferred(후속 단계 — 21개 비교 후)

## A (1)

- **A-S04-6** [fixed] (S04) 수동 표현 누락 — M12 이소트레티노인 문구의 괄호 앞 구절(복용 여부/중단 시점 확인 · 6개월/12개월 대기 원칙)을 직접 읽기 기록에서 빠뜨렸다. 자동 후보↔수동 표현 대조(읽기 검토)에서 발견, 추가 후 verify 재통과 — 위치: `/category_specific/11/checks/2/label`

## B (15)

- **B-S01-1** [open] (S01) 'x2' 의 뜻(1일 2회 등)과 투여 기간이 `/universal_checks/5/description` 에 없다 — 단위·횟수 해석 불가(채우지 않음) — 위치: `/universal_checks/5/description`
- **B-S01-2** [open] (S01) '일부 시술'(수유)·'대부분의 시술'(임신)이 어떤 시술인지 원문에 없다 — 위치: `/universal_checks/3/description`, `/universal_checks/9/description`
- **B-S01-3** [open] (S01) '최근' 의 기간 기준 없음 — 위치: `/universal_checks/10/label`, `/universal_checks/10/description`
- **B-S01-4** [open] (S01) '프락셔널/얕은 필링' 의 슬래시 범위(프락셔널 레이저 vs 필링)가 원문만으로 결정되지 않음 — 위치: `/universal_checks/6/description`
- **B-S02-1** [open] (S02) '최근' 기간 기준 없음(보톡스·치과·피부 시술) — 위치: `/category_specific/0/checks/3/label`, `/category_specific/1/checks/7/label`, `/category_specific/3/checks/1/label`
- **B-S02-2** [open] (S02) '48시간 이내' 의 기준 시점(시술 전/후)이 없음 — 위치: `/category_specific/1/checks/8/label`
- **B-S03-1** [open] (S03) '충분한 지방량' 의 기준값 없음 — 위치: `/category_specific/5/checks/2/label`
- **B-S03-2** [open] (S03) '에너지 감소 or 시술 연기 판단' 의 선택 기준·감소 정도 없음 — 위치: `/category_specific/7/checks/1/label`
- **B-S03-3** [open] (S03) 'x2' 의 뜻이 M8 헤르페스 문구에도 없음(S01-1 과 같은 원인) — 위치: `/category_specific/7/checks/4/label`
- **B-S04-1** [open] (S04) 수치 자리만 있고 값이 없음 — 지방층 두께 기준, 니들 깊이별 구분, 마취크림 시간, '과도한 세팅' 기준 — 위치: `/category_specific/8/checks/5/label`, `/category_specific/11/checks/5/label`, `/category_specific/10/checks/5/label`, `/category_specific/9/checks/4/label`
- **B-S04-2** [open] (S04) '최근' 기간 기준 없음(골드 실/금속 실, 복부/시술 부위 수술) — 위치: `/category_specific/8/checks/2/label`, `/category_specific/9/checks/2/label`
- **B-S05-1** [open] (S05) '고용량' 비타민 C 기준 없음 — 위치: `/category_specific/15/checks/2/label`, `/category_specific/15/checks/3/label`
- **B-S05-2** [open] (S05) '피하지방 두께'·'지질 수치'·'필링 간격' 기준값 없음(S04-1 과 같은 유형) — 위치: `/category_specific/13/checks/3/label`, `/category_specific/14/checks/3/label`, `/category_specific/14/checks/7/label`
- **B-S05-3** [open] (S05) PAH '0.005-0.39%' 의 분모·출처 없음(값은 그대로 보존, 해석하지 않음) — 위치: `/category_specific/13/checks/5/label`
- **B-G-1** [open] (전체) type 값 6종(must_check·inform·counseling·safety_protocol·relative_contraindication·absolute_contraindication)의 뜻·판정 기준이 원장 안에 없다 — 위치: `/universal_checks/0/type`, `/category_specific/0/checks/0/type`

## C (0)

- 없음 — C 0 — 모든 잔여 항목을 검토한 결과 원문 부족(B)·잠정(P)·후속(F)·불일치 후보(I)·분석 한계(K)로 분류됐고, 지금 사용자 선택이 있어야 1차 수집을 계속하거나 마칠 수 있는 항목은 없다. 설계 선택은 21개 원장 비교 후 묶어 제시하며, 원본 변경 제안(I)은 선택 대기로 올리지 않는다. 도구·패턴 선택은 에이전트 판단으로 처리했다.

## K (8)

- **K-S02-4** [recorded] (S02) 자동 패턴 AP-DEGREE «이상» 이 '이상반응'(abnormal reaction) 안에서 일치 — 오탐(정도 표현 아님). 자동 후보는 패턴 일치분일 뿐임을 재확인 — 위치: `/category_specific/0/checks/1/label`
- **K-S03-7** [recorded] (S03) kiwi 가 '안내' 를 '안/MAG 내/VV' 로 나눠 원문에 없는 부정(안)을 만든다 — 형태소 기반 부정 탐지 시 오탐 — 위치: `/category_specific/6/checks/6/label`
- **K-S05-5** [recorded] (S05) 자동 AP-DEGREE «이상» 이 '감각 이상'(abnormality) 에서 일치 — 오탐 — 위치: `/category_specific/13/checks/6/label`
- **K-S05-6** [recorded] (S05) kiwi 가 '금기' 를 '금/NNG 기/XSN' 로 나눔 — 원문의 유일한 '금기' 명시어가 토큰에서 깨짐. 자동 AP-NEG 는 원문 문자열에서 '금기' 를 잡았다 — 위치: `/category_specific/15/checks/3/label`
- **K-G-4** [recorded] (전체) kiwi 는 영문 약어·영단어(NOAC·NSAIDs·AAD Task Force·ablative·Fitzpatrick·PIH·RF·HIFU·HA·PMMA·BMI·PAH·MTS·HIFES/EMS·mg·or·vs)를 SL 토큰으로만 보존하고 영어 형태 분석을 하지 않는다. 다른 언어 없음 — 위치: 
- **K-G-5** [recorded] (전체) kiwi 는 하이픈 수치 범위를 W_SERIAL 단일 토큰으로 만들어 범위 구조를 주지 않는다(1-3·2-4·7-10·30-70). 소수 범위(0.005-0.39)는 SN/SO/SN 으로 분리. 동음이의(예: '상의')·의미 sense 는 분석하지 않았다 — 위치: 
- **K-G-6** [recorded] (전체) 자동 표현 후보는 build.py AUTO_PATTERNS 정규식에 실제로 일치한 구간뿐이다. 슬래시 범위는 공백에서 끊겨 «프락셔널/얕은»·«이물반응/상처» 처럼 구절 일부만 잡는다. 패턴 밖 수식·조건은 구획별 수동 표현으로 보완했으나 그것도 전수 의미 해석은 아니다 — 위치: 
- **K-G-7** [recorded] (전체) 같은 일반명사·약물명의 품사가 출현마다 NNP/NNG 로 갈린다(항응고제: `/universal_checks/1/label` NNP vs `/category_specific/4/checks/1/label` NNG · 필러 NNP/NNG/오분절 · 아시클로비르·발라시클로비르 NNP/NNG 교차 · 다운타임 NNP/NNG+NNG). 분절은 맞고 태그만 다름 — 태그로 고유명 여부를 판단하지 않는다 — 위치: `/universal_checks/1/label`, `/category_specific/4/checks/1/label`, `/universal_checks/5/description`, `/category_specific/7/checks/4/label`

## P (3)

- **P-S02-3** [open] (S02) '(항체 내성)'·'(잔여 필러)'·'(육아종 위험)' 등 괄호가 사유·목적·예시 중 무엇인지 문법적으로 표시되지 않음 — 잠정 관점 태그만 붙임 — 위치: `/category_specific/0/checks/3/label`, `/category_specific/1/checks/1/label`, `/category_specific/1/checks/3/label`
- **P-S04-4** [open] (S04) M10 임신 항목은 type absolute_contraindication 인데 '(복부 시술 시 특히 중요)' 로 조건적 강조 — type 과 문구의 범위 관계 잠정 — 위치: `/category_specific/9/checks/3/label`, `/category_specific/9/checks/3/type`
- **P-S05-4** [open] (S05) 검사 행위 문구(임신 테스트)에 absolute_contraindication — type 이 문구 종류가 아니라 다른 축(중대도 등)일 가능성. 확정하지 않음 — 위치: `/category_specific/14/checks/1/label`, `/category_specific/14/checks/1/type`

## F (10)

- **F-S00-1** [deferred] (S00) category_specific 의 id(M1–M17)·name 이 어떤 분류 체계를 가리키는지 원문 안에 정의 없음 — 다른 원장과의 연결은 21개 비교 후 과제 — 위치: `/category_specific`
- **F-S01-6** [deferred] (S01) universal 항목 간 겹침(기저질환⊃자가면역질환?, 복용 약물⊃항응고제·이소트레티노인?) 관계 판단은 의미 조사 단계 — 위치: `/universal_checks/7/description`, `/universal_checks/8/description`
- **F-S01-7** [deferred] (S01) 헤르페스 예방 투여 문구가 M8 항목과 순서·세부(7-10일 복용)가 다르다 — 같은 지침의 변형인지 후속 비교 — 위치: `/universal_checks/5/description`, `/category_specific/7/checks/4/label`
- **F-S02-5** [deferred] (S02) type 값(must_check·inform·safety_protocol·counseling·absolute_contraindication)이 같은 주제에서 카테고리마다 다르다 — type 의미·용도는 21개 비교 후 설계 과제 — 위치: `/category_specific/0/checks/2/type`, `/category_specific/2/checks/0/type`, `/category_specific/3/checks/2/type`
- **F-S03-4** [deferred] (S03) ablative 표기 3종(박리성(ablative)/박리성/어블레이티브)의 동일성 — 후속 의미 조사 — 위치: `/universal_checks/6/description`, `/category_specific/7/checks/2/label`, `/category_specific/7/checks/5/label`
- **F-S03-5** [deferred] (S03) M8 안 'RF/HIFU 병행 시' 는 다른 카테고리(M9 기기 리프팅 등) 참조로 보임 — 연결은 후속 — 위치: `/category_specific/7/checks/8/label`
- **F-S03-6** [deferred] (S03) 시술 전 체크리스트 안의 시술 후 지시(입벌리기/마사지 제한) — 시점 범위 모델링은 후속 — 위치: `/category_specific/6/checks/6/label`
- **F-S04-5** [deferred] (S04) 금속 임플란트/페이스메이커 계열 확인이 카테고리마다 문구·type 이 다름 — 같은 확인 대상인지 후속 비교 — 위치: `/category_specific/7/checks/8/label`, `/category_specific/8/checks/0/label`, `/category_specific/9/checks/0/label`, `/category_specific/10/checks/0/label`, `/category_specific/12/checks/0/label`, `/category_specific/12/checks/1/label`
- **F-G-2** [deferred] (전체) 확인 항목을 금기 관계로 일괄 확정하지 않는다 — 항목은 확인·설명·준비·시술 후 지시가 섞여 있고 type 도 그와 1:1 이 아니다. 관계 모델은 21개 비교 후 — 위치: `/universal_checks`, `/category_specific`
- **F-G-3** [deferred] (전체) 같은 주제가 카테고리마다 반복(항응고제·켈로이드·활동성 감염·자가면역질환·이소트레티노인·금속 임플란트)되며 type 이 다르다 — universal 과 category 항목의 관계(대체·보강·중복)는 후속 — 위치: `/universal_checks`, `/category_specific`

## I (2)

- **I-S01-5** [open] (S01) 임신 항목 type=absolute_contraindication 인데 description 은 '대부분의 시술 불가'. type 정의가 원문에 없어 불일치인지 확정 못 함 — 원문 변경 제안 아님, 후속 확인 후보 — 위치: `/universal_checks/9/type`, `/universal_checks/9/description`
- **I-S04-3** [open] (S04) 한 문자열 안에서 '체내'(전신) 와 '(시술 부위)'(국소) 범위가 함께 쓰임 — 범위 불일치 후보. 원문 변경 제안 아님, 후속 확인 후보 — 위치: `/category_specific/10/checks/0/label`

## K-형태소 오분절 출현 목록 (44)

구간 = 해당 Pointer 의 디코딩된 값 문자열 안 Unicode 코드포인트 [start,end). 44출현 모두 그 값에서 표면형이 정확히 1회 나온다.

- `/description` [5,10) «체크리스트» → `체크/NNG 리스트/NNG` — 외래 복합어가 둘로 나뉨 — 의미 손실은 작음(K)
- `/universal_checks/1/description` [54,58) «처방의와» → `처방/NNG 의/JKG 와/JKB` — '처방의'(처방한 의사, 명사)가 '처방'+관형격 조사로 오분석 — 행위 주체 명사 소실
- `/universal_checks/3/label` [0,2) «수유» → `수유/NNP` — 일반명사가 고유명사(NNP)로 태깅 — 품사만 오류
- `/universal_checks/3/description` [0,2) «수유» → `수유/NNP` — 일반명사가 고유명사(NNP)로 태깅 — 품사만 오류
- `/universal_checks/5/description` [0,4) «구순포진» → `구/NNP 순/NNB 포진/NNG` — '구순(입술)' 이 사라져 부위 정보가 토큰에서 소실 — 원문 구절로만 보존
- `/universal_checks/5/description` [10,15) «항바이러스» → `항/NNG 바이러스/NNG` — 접두 '항-' 이 명사로 분리 — '항바이러스'(약효군) 단위 소실
- `/universal_checks/6/description` [99,103) «비박리성» → `비/XPN 박/NNG 리/XSN 성/NNG` — '박리성' 어간이 박/리/성 으로 깨짐. 부정 접두 '비' 는 XPN 으로 남음 — 같은 문장의 '박리성/NNP' 와 토큰 대응 불가
- `/category_specific/0/checks/0/label` [0,6) «신경근접합부» → `신경/NNG 근/NNG 접합부/NNG` — '신경근' 단위가 '신경'+'근' 으로 나뉨 — 의미 손실 작음
- `/category_specific/0/checks/0/label` [10,16) «중증근무력증» → `중증 근무력증/NNP` — kiwi form 에 원문에 없는 공백이 들어감(surface≠form). 구간은 원문 6자를 덮음
- `/category_specific/0/checks/5/label` [0,7) «D-페니실라민» → `D/SL -/SO 페니실라민/NNG` — 약물명이 셋으로 나뉨 — 원문 구절로만 약물명 보존
- `/category_specific/0/checks/5/label` [15,21) «신경근접합부» → `신경/NNG 근/NNG 접합부/NNG` — '신경근' 단위 분리
- `/category_specific/1/checks/1/label` [0,2) «이전» → `이/NNP 전/MM` — 시점어 '이전' 이 고유명사+관형사로 오분석 — 시점 정보가 토큰에서 소실
- `/category_specific/1/checks/2/label` [26,30) «이물반응» → `이/MM 물/NNG 반응/NNG` — '이물'(foreign body) 이 관형사 '이'+'물' 로 오분석 — 위험 대상 소실(같은 단어가 `/universal_checks/2/description` 에서는 이물/NNG)
- `/category_specific/1/checks/7/label` [26,29) «혈행성» → `혈/NNG 행/NNG 성/XSN` — '혈행성' 이 혈/행/성 으로 깨짐
- `/category_specific/1/checks/7/label` [34,36) «필러» → `피/VV ᆯ러/EC` — 시술 대상 명사 '필러' 가 동사 '피-'+어미로 오분석 — 대상 명사 소실(심각)
- `/category_specific/1/checks/8/label` [26,29) «기압이» → `기압/NNG 이/MM` — 주격조사 '이' 가 관형사로 태깅 — 주어 표시 소실
- `/category_specific/2/checks/4/label` [13,16) «1-3» → `1-3/W_SERIAL` — 수치 범위가 일련번호(W_SERIAL) 단일 토큰 — 범위 구조 없음
- `/category_specific/3/checks/4/label` [17,20) «1-3» → `1-3/W_SERIAL` — 수치 범위가 일련번호(W_SERIAL) 단일 토큰
- `/category_specific/3/checks/4/label` [14,16) «구진» → `구/NR 진/NNG` — 증상명 '구진'(papule) 이 수사 '구'+'진' 으로 오분석 — 증상 소실
- `/category_specific/5/checks/4/label` [8,13) «30-70» → `30-70/W_SERIAL` — 수치 범위가 일련번호 단일 토큰 — 범위·% 결합 구조 없음(%/SW 별도)
- `/category_specific/5/checks/5/label` [0,3) «비대칭» → `비대칭/NNP` — 고유명사 태깅. 같은 단어가 `/category_specific/6/checks/5/label` 에서는 비/XPN 대칭/NNG — 출현마다 분석 다름
- `/category_specific/6/checks/4/label` [13,16) «비녹는» → `비/NNG 녹/VV 는/ETM` — 부정 접두 '비' 가 명사(NNG)로 태깅 — 부정 의미가 토큰에서 소실('비HA' 는 XPN 으로 분석됨)
- `/category_specific/6/checks/6/label` [20,22) «안내» → `안/MAG 내/VV 어/EF` — 명사 '안내' 가 부정 부사 '안'+동사 '내다' 로 오분석 — 원문에 없는 부정 생성(심각, 오탐)
- `/category_specific/7/checks/0/label` [21,25) «I-VI» → `I/SL -/SO VI/SL` — 로마숫자 범위가 셋으로 나뉨 — 범위 구조 없음
- `/category_specific/7/checks/1/label` [16,19) «2-4» → `2-4/W_SERIAL` — 수치 범위가 일련번호 단일 토큰
- `/category_specific/7/checks/2/label` [84,88) «비박리성» → `비/XPN 박/NNG 리/XSN 성/NNG` — '박리성' 어간 깨짐(S01 과 같은 패턴)
- `/category_specific/7/checks/4/label` [88,92) «7-10» → `7-10/W_SERIAL` — 수치 범위가 일련번호 단일 토큰
- `/category_specific/7/checks/7/label` [0,3) «중등도» → `중등/NNG 도/JX` — 정도어 '중등도' 의 '도' 가 보조사(도)로 오분석 — '중등도 이상' 정도 표현이 토큰에서 깨짐
- `/category_specific/7/checks/10/label` [8,12) «다운타임» → `다운/NNG 타임/NNG` — 같은 단어가 `/category_specific/3/checks/4/label` 에서는 다운타임/NNP — 출현마다 분석 다름
- `/category_specific/8/checks/0/label` [11,17) «페이스메이커» → `페이스/NNG 메이커/NNG` — 기기명이 둘로 나뉨 — 의미 손실 작음
- `/category_specific/9/checks/0/label` [11,17) «페이스메이커» → `페이스/NNG 메이커/NNG` — 기기명이 둘로 나뉨
- `/category_specific/12/checks/0/label` [0,6) «페이스메이커» → `페이스/NNG 메이커/NNG` — 기기명이 둘로 나뉨
- `/category_specific/8/checks/1/label` [6,8) «필러» → `필/NNG 러/EC` — '필러' 가 명사+어미로 깨짐 — 대상 명사 소실(같은 단어가 다른 곳에서는 필러/NNP)
- `/category_specific/8/checks/4/label` [0,3) «초음파» → `초/XPN 음파/NNG` — '초음파' 가 접두+명사로 분리 — 에너지 종류 단위 소실
- `/category_specific/10/checks/2/label` [61,65) «비박리성» → `비/XPN 박/NNG 리/XSN 성/NNG` — '박리성' 어간 깨짐
- `/category_specific/11/checks/2/label` [61,65) «비박리성» → `비/XPN 박/NNG 리/XSN 성/NNG` — '박리성' 어간 깨짐
- `/category_specific/11/checks/5/label` [0,2) «니들» → `니/NP 들/XSN` — '니들'(needle) 이 대명사 '니'+복수 접미 '들' 로 오분석 — 기구 명사 소실(심각). 카테고리명 '니들RF' 에서는 니들/NNP
- `/category_specific/11/checks/5/label` [7,11) «다운타임» → `다운/NNG 타임/NNG` — 출현마다 분석 다름(다운타임/NNP 인 곳도 있음)
- `/category_specific/13/checks/0/label` [0,6) «한냉두드러기» → `한/MM 냉/NNG 두드러기/NNG` — '한냉' 이 관형사 '한'(one)+'냉' 으로 오분석 — 질환명 단위 소실
- `/category_specific/13/checks/7/label` [13,16) «2-4» → `2-4/W_SERIAL` — 수치 범위가 일련번호 단일 토큰
- `/category_specific/14/checks/0/label` [84,88) «비박리성» → `비/XPN 박/NNG 리/XSN 성/NNG` — '박리성' 어간 깨짐
- `/category_specific/15/checks/3/label` [0,4) «G6PD» → `G/SL 6/SN PD/SL` — 효소명 식별자가 셋으로 나뉨 — 원문 구절로만 보존
- `/category_specific/15/checks/3/label` [23,25) «금기» → `금/NNG 기/XSN` — 금지 명시어 '금기' 가 깨짐 — 형태소 기반 금기 탐지 실패
- `/category_specific/15/checks/2/label` [20,21) «시» → `시/NNG` — 조건 의존명사 '시' 가 다른 곳(NNB)과 달리 NNG — 조건 표지 태그가 출현마다 다름
