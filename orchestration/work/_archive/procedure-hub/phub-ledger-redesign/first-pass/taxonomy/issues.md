# taxonomy.json — 미결 기록

상태 문자: A=에이전트 추출/해석 오류(에이전트가 고칠 것) · B=원문 정보 부족 · C=현재 사용자 결정 필요 · K=알려진 분석 한계 · P=잠정 해석 · F=후속 의미 조사 · I=원문 내 불일치.
원본 변경 제안은 현재 원본 보존 지시 아래 후속 확인 후보이며 선택 대기(C)로 올리지 않는다.

## 집계

| 상태 | 건수 |
|---|---|
| A | 0 |
| B | 34 |
| C | 0 |
| K | 4 |
| P | 0 |
| F | 47 |
| I | 65 |

위 표는 구조화 기록(`manual/*.json`, verify `issues_by_status`) 기준이다(K 4). batch-03 검토 뒤 덧붙인 문서 기록 K-EXPR01 과 관찰 OBS-M16-PRODUCTS(맨 아래 「batch-03 검토 후 기록 보완」 절)는 이 집계와 JSON 에 들어 있지 않다. 이 파일은 `build.py` 가 생성하므로 rebuild 하면 그 절이 사라진다.

구획을 가로지르는 반복 패턴은 GLOBAL-* 로 묶고, 각 구획 기록이 그 ID 를 참조한다. 출현별 위치는 expressions.json(auto 후보)·morphology.json(known_segmentation_errors)에 있다. 사용자 결정(C) 대기는 0건이다 — 원본 변경 후보는 모두 후속 확인 후보(F/I)로 두었고 지금 선택을 요청하지 않는다.

## 전체 목록

| ID | 구획 | 상태 | Pointer | 내용 | 영향·후속 |
|---|---|---|---|---|---|
| GLOBAL-I01 | GLOBAL | I | `/modality/0/subcategories/0/items/0/extracted/aftercare/3`, `/modality/1/subcategories/0/items/0/extracted/aftercare/2`, `/modality/2/subcategories/0/items/0/extracted/aftercare/2`, `/modality/3/subcategories/0/items/0/extracted/aftercare/2`, `/modality/4/subcategories/0/items/0/extracted/aftercare/3`, `/modality/6/subcategories/0/items/0/extracted/aftercare/3`, `/modality/7/subcategories/0/items/0/extracted/aftercare/6`, `/modality/8/subcategories/0/items/0/extracted/aftercare/3`, `/modality/9/subcategories/0/items/0/extracted/aftercare/3`, `/modality/10/subcategories/0/items/0/extracted/aftercare/2`, `/modality/11/subcategories/0/items/0/extracted/aftercare/5`, `/modality/13/subcategories/0/items/0/extracted/aftercare/5` | '[시술 주기 참고] … (개인차 있으며, 의사와 상의하여 결정)' 상용구가 M1·M2·M3·M4·M5·M7·M8(하위분류별 5종)·M9(출력별 3종)·M10·M11(출력별 3종)·M12·M14 항목 aftercare 마지막 원소에 반복된다. M6·M13·M15·M16·M17 항목과 모든 products 에는 없다. 상용구 수치가 같은 항목 onset_duration·overview 수치와 다른 경우가 많고, 하위분류 성격과 맞지 않는 항목(비HA 필러, 면사, 문신 장비 등)에도 붙어 있다. | 기간·간격 정보가 두 칸에 서로 다르게 존재. 어느 쪽이 기준인지는 후속 의미 조사 |
| GLOBAL-F01 | GLOBAL | F | `/modality/0/group`, `/modality/0/subcategories/2/items/6/name`, `/modality/2/subcategories/0/items/0/extracted/aftercare/2`, `/modality/8/subcategories/4/items/0/detail`, `/problem/1/subcategories/1/items/0/detail` | '/' 와 '+' 기호가 README 규칙(+ 함께, / 대안) 외에도 나열·병기·and/or·성분 결합·상표 일부('리쥬란HB+','젠틀맥스프로+')·하한('24개월+','SPF 50+','2000곳+')으로 쓰인다. '→' 는 절차·결과, '·' 는 detail 속성 구분, '>' 는 canonical_category 경로·비교. | 이름 분해·관계 추출 단계에서 출현별 판단 필요. 기호만으로 관계 확정 금지 |
| GLOBAL-F02 | GLOBAL | F | `/modality/0/products`, `/modality/0/subcategories/1/items`, `/modality/3/subcategories/1/items/8`, `/modality/8/subcategories/1/items/3`, `/modality/8/subcategories/1/items/15` | 같은 이름(또는 표기만 다른 이름)의 레코드가 products·items·여러 하위분류·여러 모달리티에 흩어져 있고 연결 키가 없다(예: 디스포트·제오민 제품/항목, 볼뉴머 3레코드, LDM 3곳, 라라젯 2곳, NAD+ 3항목, 엑셀V/엑셀브이/엑셀V+, 옴니룩스/옴니럭스). | 개체 식별·병합은 설계 단계 과제. 1차에서는 출현별 원문만 보존 |
| GLOBAL-F03 | GLOBAL | F | `/modality/0/subcategories/2`, `/modality/6/subcategories`, `/modality/14/subcategories/9`, `/modality/8/subcategories/4`, `/problem/0` | 같은 깊이(subcategories·items·problem 최상위)가 서로 다른 종류(제품 브랜드/부위·용도/재질/형태/에너지원/고민/판매 패키지/외용약)를 담는다. | 개체 유형은 값 단위로 분해해야 함(설계 단계) |
| GLOBAL-F04 | GLOBAL | F | `/modality/3/subcategories/1/items/8/classification_issue`, `/modality/8/subcategories/1/items/4/classification_issue`, `/modality/8/subcategories/1/items/4/reclassified_to`, `/modality/7/subcategories/4/items/11/correction_note` | 원문이 스스로 오분류·정정을 기록한 필드(classification_issue 2, reclassified_to 1, correction_note 1)가 있으나 구조상 레코드 위치는 바뀌지 않았다. | 재분류 반영은 원본 변경 후보 — 현재 원본 보존 지시 아래 후속 확인 |
| GLOBAL-K01 | GLOBAL | K | `/modality/0/subcategories/0/items/0/extracted/onset_duration/onset`, `/modality/7/subcategories/4/items/5/detail` | W_SERIAL 토큰(숫자 연쇄)은 범위·목록·기법명을 구분하지 않는다. '3~7일' 은 3/SN ~/SO 7/SN 으로 분리되어 같은 뜻의 범위가 표기에 따라 다르게 분석된다. | 형태소만으로 범위 수치를 뽑으면 표기별로 결과가 달라짐. morphology.json known_segmentation_errors 에 W_SERIAL 출현별 기록 |
| GLOBAL-K02 | GLOBAL | K | `/modality/0/subcategories/0/items/0/extracted/safety/serious/0`, `/modality/0/subcategories/0/items/1/extracted/safety/serious/0` | 같은 전문어가 문맥에 따라 다르게 분절된다(안검하수·다한증·압통·셀르디엠·이소트레티노인·비가교HA 등). 브랜드·장비명 상당수가 조사·어미·부사로 오분석된다(구획별 seg_errors). 사용자 사전 없이 기본 결과를 보존했다. | 토큰 기반 빈도·병합이 표기 아닌 분석 결과에 흔들림. 고유명은 원문 구간(expressions) 기준으로 다뤄야 함 |
| GLOBAL-K03 | GLOBAL | K | `/modality/7/subcategories/2/items/3/extracted/indications/primary/2`, `/modality/14/subcategories/2/items/1/extracted/indications/primary/1` | '주사'(질환 주사비/rosacea)와 '주사'(시술 injection)가 같은 형태소. '대이개신경'·'삼염화초산'·'초회통과효과' 처럼 수사·단위 오탐(이/NR 개/NNB, 삼/NR, 초/NNB 회/NNB)이 생기는 어휘가 있다. | 키워드·수량 자동 추출 시 오탐 — 원문 대조 필수 |
| GLOBAL-B01 | GLOBAL | B | `/modality/0/subcategories/0/items/3/extracted/indications/primary/2`, `/modality/7/subcategories/5/items/13/extracted`, `/modality/14/subcategories/14/items` | 원문 자체 정보 부족 묶음: U+FFFD 손상 1, 빈 extracted 2항목, 빈 items 하위분류 2, 빈 문자열 값 22(주로 detail), mfds null 17, '-' 자리표시 2, 정의 없는 약어(ASCE·MCT·CPR·ACT·ACR·IDS·IED·MoD·SMP·DC 등), 기준 모집단 없는 비율(38.8%, 0.04mL, PIH %), 기준 시점 없는 '출시 예정'·허가 연월. | 해당 정보로 판단 불가 — 원본 확인 후보 |
| S001-B01 | S001 | B | `/modality/0/subcategories/0/items/3/extracted/indications/primary/2` | 원문 '눈�리 주름(까치발)' 에 U+FFFD 대체문자가 있다. 원래 글자를 원문만으로 알 수 없다(추정하지 않음). | 부위 표현 식별 제한. 원본 확인은 후속 후보(지금 선택 대기 아님) |
| S001-B02 | S001 | B | `/modality/0/subcategories/1/items/1/extracted/aftercare/1` | '며칠 정기적인 마사지 또는 얼굴 자극 최소화' — 마사지를 권하는지 자극을 줄이라는지 구문상 결정 불가. | 관리 지시의 방향(권장/금지) 판단 제한 |
| S001-F01 | S001 | F | `/modality/0/subcategories/1/items/2/extracted/safety/common`, `/modality/0/subcategories/0/items/0/extracted/safety/serious` | 같은 부작용이 항목에 따라 common/serious 로 갈린다. | 심각도 정보 종류 설계 시 원장 간 비교 필요 |
| S001-I01 | S001 | I | `/modality/0/subcategories/1/items/3/extracted/safety` | 코어톡스 safety 에 common_adverse_effects/serious_adverse_effects 와 common 공존. | 키 변형 정리는 후속. 원문 그대로 보존 |
| S002-B01 | S002 | B | `/modality/0/subcategories/2/items/4/extracted/aftercare/1` | '시술 후 24-당일 동안' — 범위의 한쪽이 숫자(24, 단위 없음), 다른 쪽이 '당일'. 원문만으로 의도(24시간~당일?) 확정 불가. | 시간 범위 해석 제한 |
| S002-B02 | S002 | B | `/modality/0/subcategories/1/items/9` | 톡스온은 원문 스스로 허가·임상 미검증이라고 적는다. 제품 실재·허가 상태 정보 부족. | 제품 항목 채택 여부 판단 제한(후속) |
| S002-I01 | S002 | I | `/modality/0/subcategories/2/items/4/extracted/onset_duration/duration` | duration 키에 정점 시점 문장. | 키 기준 자동 분류 시 오분류 |
| S003-F01 | S003 | F | `/modality/0/products`, `/modality/0/subcategories/0/items`, `/modality/0/subcategories/1/items` | products 와 subcategories items 에 같은 제품명이 따로 존재하고 연결 키가 없다. | 제품 개체 식별·병합은 후속 설계 과제 |
| S003-F02 | S003 | F | `/modality/0/extracted/related_techniques` | related_techniques 는 기법명+설명 문자열(— 구분)이며 taxonomy 항목 이름과의 대응이 없다(메조보톡스·에어보톡스는 M1 항목에 없음). | 참조 표현만 보존. 연결은 후속 |
| S003-I01 | S003 | I | `/modality/0/subcategories/2/items/9/extracted/aftercare/2`, `/modality/0/products/0/extracted/aftercare/3` | 항염증제 지시가 항목/제품 사이에서 반대. | 안전 지시 비교 시 후속 확인 |
| S004-B01 | S004 | B | `/modality/0/products/10/note` | '중국 수출명' 이 어느 제품의 수출명인지 원문에 없다. | 제품 간 관계 연결 불가(후속) |
| S004-I01 | S004 | I | `/modality/0/products/6/name`, `/modality/0/subcategories/1/items/7/name` | 리즈톡스(제품)/리즈톡신(항목), 휴온스바이오파마/휴온스 표기 차이. | 동일 대상 여부 후속 확인 |
| S004-F01 | S004 | F | `/modality/0/products/5/extracted/onset_duration/diffusion`, `/modality/0/products/4/extracted/safety/common/4` | 시간 객체 안 공간 수치, common 배열 안 '드문' 값 — 키가 정보 종류를 보장하지 않는다. | 키 기반 자동 매핑 금지, 값 단위 분해 필요 |
| S005-B01 | S005 | B | `/modality/1/subcategories/0/items/2/extracted/safety/serious/0`, `/modality/1/subcategories/0/items/1/extracted/safety/serious/1`, `/modality/1/subcategories/0/items/4/extracted/safety/serious/0` | 비율(38.8%·25.5%)·임계량(0.04mL)의 기준 모집단·출처가 원문에 없다. | 수치의 뜻을 확정할 수 없음(원문 그대로 보존) |
| S005-I01 | S005 | I | `/modality/1/subcategories/0/items/8/extracted/safety/serious/2`, `/modality/1/subcategories/0/items/10/extracted/aftercare/0`, `/modality/1/subcategories/0/items/10/extracted/aftercare/1` | 구절·문장 중복 결합(육아종 수식 2회, 마사지 자제 문장 2종 연속). | 중복 제거는 후속(원문 보존) |
| S005-I02 | S005 | I | `/modality/1/subcategories/0/items/8/extracted/mechanism` | '겸립' 오기 의심. | 표현 보존 |
| S006-B01 | S006 | B | `/modality/1/subcategories/1/items/1/extracted/safety/serious/2` | 육아종 '3유형' 의 유형명이 같은 구절 반복으로 덮여 원래 유형명을 알 수 없다. | 부작용 하위유형 정보 손실 |
| S006-B02 | S006 | B | `/modality/1/subcategories/0/items/16/detail`, `/modality/1/subcategories/0/items/17/detail` | '휴메딕스프리미엄'·'휴젤프리미엄' 이 회사명인지 라인 등급 표기인지 원문으로 불명. | 제조사 식별 제한 |
| S006-I01 | S006 | I | `/modality/1/subcategories/2/items/0/extracted/aftercare/3`, `/modality/1/subcategories/2/items/0/extracted/onset_duration/duration` | 비HA(영구) 필러에 HA 지속 상용구. | 기간 정보 충돌(GLOBAL-I01) |
| S006-I02 | S006 | I | `/modality/1/subcategories/1/items/4/extracted/mechanism`, `/modality/1/subcategories/0/items/5/extracted/mechanism` | 같은 입자 수(119,856개/시린지)가 한 곳은 '<', 다른 곳은 '이상'으로 방향이 반대. | 수치 비교 시 후속 확인 |
| S007-I01 | S007 | I | `/modality/1/products/0/extracted/mechanism`, `/modality/1/subcategories/1/items/0/extracted/mechanism`, `/modality/1/products/1/extracted/mechanism`, `/modality/1/subcategories/1/items/1/extracted/mechanism` | 같은 이름 제품/항목 사이 G' 수치 불일치(쥬비덤 50-120 vs 200-400 Pa, 레스틸렌 60-150 vs 4-857 Pa). | 물성 수치 채택 시 후속 확인 |
| S007-B01 | S007 | B | `/modality/1/products/6/extracted/mechanism` | '(><99.5%)' 부등호 방향 불명. | 순도 수치 해석 불가 |
| S007-F01 | S007 | F | `/modality/1/extracted/overview`, `/modality/1/products/7` | M2 설명·제품에 PLLA·칼슘 필러·자가지방이식이 포함되어 M3·M6 와 범위가 겹친다. | 계열 경계는 후속 비교 과제 |
| S008-I01 | S008 | I | `/modality/2/subcategories/1/items/1/extracted/overview`, `/modality/2/subcategories/1/items/1/extracted/mechanism` | 디클래씨 재질 서술 충돌(PDLLA/HA vs CaHA/CMC). | 재질 축 분류 시 확인 필요(원본 확인 후보) |
| S008-I02 | S008 | I | `/modality/2/subcategories/2/items/1/extracted/aftercare/0`, `/modality/2/subcategories/2/items/1/extracted/safety/serious/0` | 레티젠 콜라겐 주입 항목에 세포배양 서술. | 다른 항목 서술 혼입 가능성 — 후속 확인 |
| S008-I03 | S008 | I | `/modality/2/subcategories/0/items/2/extracted/overview`, `/modality/2/subcategories/0/items/2/extracted/onset_duration/onset` | 에스테필 즉시효과 서술 충돌. | 시점 정보 채택 시 확인 |
| S008-B01 | S008 | B | `/modality/2/subcategories/2/items/0/detail`, `/modality/2/subcategories/2/items/1/detail`, `/modality/2/subcategories/2/items/2/detail` | detail 빈 문자열 — 제조사·특징 정보 없음. | 제품 식별 정보 부족 |
| S009-I01 | S009 | I | `/modality/2/subcategories/5/items/0/detail`, `/modality/2/subcategories/5/items/0/extracted/overview`, `/modality/2/subcategories/5/items/2/detail`, `/modality/2/subcategories/5/items/2/extracted/overview`, `/modality/2/subcategories/5/description` | hADM 제품 제조·유통사 표기가 detail·overview·description 에서 다르다. | 제조사 식별 시 후속 확인 |
| S009-F01 | S009 | F | `/modality/2/subcategories/5/description`, `/modality/2/subcategories/5` | hADM 하위분류가 M3 안에 있으나 원문이 'ECM 스킨부스터'로 지칭. | 계열 경계(M3/M4) 후속 비교 |
| S009-B01 | S009 | B | `/modality/2/subcategories/5/items/5/detail` | '2025 출시', '판매 예정' — 기준 시점이 원문에 없어 현재 상태를 알 수 없다. | 제품 상태 판단 제한 |
| S010-I01 | S010 | I | `/modality/2/products/5/ingredient`, `/modality/2/products/5/extracted/mechanism` | 글로벨라 성분 PDLLA+HA vs PLLA 서술. | 성분 축 채택 시 원본 확인 후보 |
| S010-I02 | S010 | I | `/modality/2/products/3/manufacturer`, `/modality/2/subcategories/4/items/1/detail` | 쥬베룩 제조사 LG화학 vs 바임. | 제조사 식별 후속 |
| S010-F01 | S010 | F | `/modality/2/products/0/extracted/aftercare/0`, `/modality/2/subcategories/3/items/0/extracted/aftercare/0` | 같은 제품의 products/items 사이 마사지 지시 방향 반대. | 관리 지시 정리 시 후속 |
| S011-I01 | S011 | I | `/modality/3/subcategories/0/items/4/extracted/overview`, `/modality/3/subcategories/0/items/4/extracted/onset_duration` | 인에이블 정정 문구와 마취제형 시간값 공존. | onset_duration 채택 금지 후보 — 원본 확인은 후속 |
| S011-I02 | S011 | I | `/modality/3/subcategories/0/items/5/detail`, `/modality/3/subcategories/0/items/5/extracted/overview` | 스네일샷 PN vs 달팽이 분비물. | 성분 축 분류 후속 확인 |
| S011-F01 | S011 | F | `/modality/3/subcategories/1/items/2`, `/modality/3/subcategories/1/items/5`, `/modality/3/subcategories/1/items/6` | HA(물광) 하위분류에 펩타이드·복합 메조 제품. | 하위분류 축(성분) 과 실제 성분 불일치 — 설계 단계 판단 |
| S012-F01 | S012 | F | `/modality/3/subcategories/1/items/8/classification_issue` | 원문이 볼뉴머 오분류(→M9-2)를 자기 선언. 구조는 M4 그대로. | 재분류 반영 여부는 원본 변경 후보(지금 선택 대기 아님) |
| S012-F02 | S012 | F | `/modality/3/subcategories/1/items/13/canonical_category`, `/modality/3/subcategories/1/items/14/canonical_category`, `/modality/3/subcategories/1/items/15/canonical_category` | canonical_category 경로의 하위 이름이 taxonomy label 에 없다. | 표준 분류 경로를 어디에 매핑할지 후속 |
| S012-B01 | S012 | B | `/modality/3/subcategories/2/items/0/name`, `/modality/3/subcategories/2/items/1/detail` | 'ASCE' 약어 정의 없음, '기타 엑소좀' detail 빈 문자열. | 제품 식별 제한 |
| S013-I01 | S013 | I | `/modality/3/products/3/note`, `/modality/3/products/3/extracted/overview` | 스킨보톡스 제품 레코드: note(보톡스 희석법) vs extracted(성장인자 복합체). | 레코드 내용 혼입 의심 — 원본 확인 후보 |
| S013-I02 | S013 | I | `/modality/3/products/4/note`, `/modality/3/products/4/extracted/overview`, `/modality/3/subcategories/3/items/2/detail`, `/modality/3/subcategories/3/items/2/extracted/overview` | 벨피엔 성분 서술 4종 불일치. | 성분 축 채택 시 확인 |
| S013-I03 | S013 | I | `/modality/3/products/1/extracted/mechanism`, `/modality/3/products/2/extracted/overview` | PN/PDRN 혼용. | 성분명 정규화 시 후속 |
| S013-B01 | S013 | B | `/modality/3/products/3/manufacturer`, `/modality/3/products/3/country` | '-' 자리표시 값. | 제조사·국가 없음 |
| S014-I01 | S014 | I | `/modality/4/products/3/note`, `/modality/4/products/3/extracted/overview`, `/modality/4/products/3/type` | ASCEplus 허가 메모·type·서술 충돌. | 제품 정보 채택 시 확인 |
| S014-I02 | S014 | I | `/modality/4/products/4/name`, `/modality/4/products/4/name_en` | EXOSOME SKIN / ExoSCRT 이름 불일치. | 제품 식별 |
| S014-B01 | S014 | B | `/modality/4/subcategories/2/label`, `/modality/4/subcategories/3/label` | MCT·CPR·ACT·ACR 약어 정의 없음. | 하위분류·항목 의미 식별 제한 |
| S015-I01 | S015 | I | `/modality/5/subcategories/0/items/0/extracted/onset_duration/duration`, `/modality/5/subcategories/2/items/0/extracted/onset_duration/duration`, `/modality/5/extracted/onset_duration/duration` | 유지·생착 비율 수치가 층마다 다름(70-80%, 80-90%↑, 30~70%). | 수치 채택 시 후속 확인 |
| S015-F01 | S015 | F | `/modality/5/subcategories/2`, `/modality/5/extracted/related_techniques/1` | SVF 가 하위분류이자 related_techniques 원소. | 개체 중복 여부 후속 |
| S016-I01 | S016 | I | `/modality/6/subcategories/0/items/2/extracted/overview`, `/modality/6/subcategories/0/items/2/extracted/onset_duration/duration` | PLCL overview 12-18개월 vs duration 24-36개월. | 기간 채택 시 확인 |
| S016-I02 | S016 | I | `/modality/6/subcategories/0/items/1/extracted/onset_duration/duration`, `/modality/6/subcategories/0/items/1/extracted/aftercare/3` | PCL 12-15개월 vs 상용구 24-36개월. | GLOBAL-I01 |
| S016-F01 | S016 | F | `/modality/6/subcategories/0`, `/modality/6/subcategories/1`, `/modality/6/subcategories/2` | 재질·형태·브랜드 세 축이 같은 깊이에 병렬. 브랜드 항목이 어느 재질·형태인지는 detail 문자열에만 있다. | 축 분해는 설계 단계 |
| S017-B01 | S017 | B | `/modality/6/subcategories/2/items/13/extracted/onset_duration/duration`, `/modality/6/subcategories/2/items/13/extracted/mechanism` | PDO 실의 '흡수(분해) 기간'과 '효과 지속 기간'을 원문이 구분해 적지 않아, 6개월·6-8개월·12-18개월 중 무엇이 무엇인지 판단 불가. | 기간 정보 종류 분리 제한 |
| S017-F01 | S017 | F | `/modality/6/subcategories/2/items/11` | N코그(코 성형) 가 브랜드 하위분류에 안면 리프팅과 함께 있다. | 부위·목적 축 분해 후속 |
| S018-I01 | S018 | I | `/modality/6/products/1/material`, `/modality/6/products/1/extracted/overview` | 에버라인 material PDO vs 3재질 복합 서술. | 재질 축 채택 시 확인 |
| S018-I02 | S018 | I | `/modality/6/products/2/extracted/safety/contraindications/0`, `/modality/6/products/2/extracted/aftercare/4` | 미라클 비가교HA 간격이 '24-72시간 내 금지' 와 '72시간 이상 간격' 으로 표현 차이. | 간격 기준 후속 |
| S018-B01 | S018 | B | `/modality/6/subcategories/2/items/19/extracted/mechanism`, `/modality/6/subcategories/2/items/20/detail` | 엘리실·로즈실 재질 미기재. | 재질 축 분류 불가 |
| S019-I01 | S019 | I | `/modality/6/products/3/material`, `/modality/6/products/3/extracted/overview` | 테스리프트 재질 서술 불일치. | 재질 축 후속 |
| S019-I02 | S019 | I | `/modality/6/products/4/extracted/mechanism`, `/modality/6/products/4/extracted/onset_duration/duration` | 실루엣소프트 기간 불일치. | 기간 채택 후속 |
| S020-I01 | S020 | I | `/modality/7/subcategories/0/items/1/extracted/safety/serious/0` | '~10% … 매우 낮은 발생률' 평가 모순. | 빈도 평가 채택 시 확인 |
| S020-B01 | S020 | B | `/modality/7/subcategories/0/items/0/extracted/safety/common/2` | '경미한 결막' 잘린 값. | 부작용 식별 불가 |
| S020-F01 | S020 | F | `/modality/7/subcategories/0/items/1`, `/modality/7/subcategories/0/items/0` | 시술 방식명과 장비명이 같은 층에 공존. | 시술/장비 개체 분리 설계 과제 |
| S021-I01 | S021 | I | `/modality/7/subcategories/1/items/7`, `/modality/7/subcategories/1/items/7/extracted/aftercare/5` | 셀렉V(QS 색소 장비)가 프락셔널 하위분류·상용구. | 분류·주기 정보 채택 시 확인 |
| S021-I02 | S021 | I | `/modality/7/subcategories/1/items/0/extracted/overview`, `/modality/7/subcategories/1/items/1/extracted/mechanism` | '픽토초','톨륨' 오기 의심. | 표기 보존, 정규화 후속 |
| S021-F01 | S021 | F | `/modality/7/subcategories/0/items/13/detail` | 조합 시술명이 다른 계열(스킨부스터·IPL)을 포함. | 조합 관계 표현 설계 과제 |
| S022-B01 | S022 | B | `/modality/7/subcategories/2/items/1/detail` | BBL detail 빈 문자열. | 제조사 정보 없음(형제 항목 detail 은 '사이톤') |
| S022-I01 | S022 | I | `/modality/7/subcategories/2/items/5/extracted/mechanism`, `/modality/7/subcategories/3/items/2/extracted/indications/primary/5` | '세바셈', '루주스' 의미 불명 표기. | 용어 식별 불가 — 원본 확인 후보 |
| S022-K01 | S022 | K | `/modality/7/subcategories/2/items/3/extracted/indications/primary/2` | '주사'(질환/시술) 동형이의. | 형태소·키워드 단독 분류 금지 |
| S023-I01 | S023 | I | `/modality/7/subcategories/4/items/0`, `/modality/7/subcategories/4/items/2`, `/modality/7/subcategories/4/items/3` | 제모 하위분류 항목에 제모 적응증 없음 + 제모 상용구. | 하위분류-적응증 대응 후속 확인 |
| S023-B01 | S023 | B | `/modality/7/subcategories/4/items/2/detail`, `/modality/7/subcategories/4/items/3/detail` | 제조사 두 이름 병기 의미 불명. | 제조사 식별 제한 |
| S023-F01 | S023 | F | `/modality/7/subcategories/3/items/2`, `/modality/7/subcategories/3/items/5`, `/modality/7/subcategories/3/items/0`, `/modality/7/subcategories/4/items/0` | 같은 장비로 보이는 항목 중복(엑셀V+/엑셀브이, 클라리티2 두 하위분류). | 장비 개체 병합은 후속 |
| S024-I01 | S024 | I | `/modality/7/subcategories/4/items/7`, `/modality/7/subcategories/4/items/11` | 제모 하위분류에 지방감소 장비(슬렌더엑스)·색소/혈관 장비(리팟, 정정 후에도 이동 안 됨). | 분류 정합 후속(원본 변경 후보) |
| S024-I02 | S024 | I | `/modality/7/subcategories/5/items/3/detail`, `/modality/7/subcategories/4/items/6/detail` | 시네론/시너론 표기 차이. | 제조사 정규화 후속 |
| S024-F01 | S024 | F | `/modality/7/subcategories/4/items/11/correction_note` | 원문의 외부 출처(URL·허가번호)는 보존만 함. | 출처 검증은 이번 범위 밖 |
| S025-B01 | S025 | B | `/modality/7/subcategories/5/items/13/extracted`, `/modality/7/subcategories/5/items/14/extracted`, `/modality/7/subcategories/5/items/13/detail`, `/modality/7/subcategories/5/items/14/detail` | LLLT·다이오드 레이저 항목은 이름 외 정보 없음(extracted {} · detail ""). | 항목 내용 조사 불가 — 원장 자료 부족 |
| S025-I01 | S025 | I | `/modality/7/subcategories/5/items/9/detail` | 'Er:YAG어성' 의미 불명. | 원본 확인 후보 |
| S025-B02 | S025 | B | `/modality/7/products/0/mfds`, `/modality/7/products/1/mfds`, `/modality/7/products/2/mfds` | mfds null — 허가 여부 미기재. | 허가 정보 없음 |
| S026-I01 | S026 | I | `/modality/7/products/3/type`, `/modality/7/products/3/extracted/overview` | 클라리티2 type 과 서술 불일치. | 장비 유형 정규화 후속 |
| S026-I02 | S026 | I | `/modality/7/products/5/extracted/safety/common/2` | 비박리성 프락셀에 PIH 50%. | 빈도 수치 채택 시 확인 |
| S027-B01 | S027 | B | `/modality/8/subcategories/0/items/0/extracted/aftercare/3`, `/modality/8/subcategories/0/items/2/extracted/aftercare/3`, `/modality/8/subcategories/0/items/9/extracted/aftercare/3` | 장비의 고/중/저출력 등급이 상용구로만 표시되고 판정 기준이 원문에 없다. | 출력 등급을 속성으로 쓸 때 근거 부족 |
| S027-F01 | S027 | F | `/modality/8/subcategories/0/items/2/extracted/mechanism`, `/modality/8/subcategories/0/items/6/extracted/mechanism` | 다수 항목이 같은 mechanism·overview 문장을 공유(템플릿 채움 흔적으로 보임). | 항목별 차이 판단 시 상용구 구분 필요 |
| S028-F01 | S028 | F | `/modality/8/subcategories/1/items/3`, `/modality/3/subcategories/1/items/8` | 볼뉴머 M4/M9-2 두 레코드 공존(원문 통합 권고 미반영). | 개체 병합·재분류는 원본 변경 후보 |
| S028-I01 | S028 | I | `/modality/8/subcategories/1/items/4/extracted/indications/primary`, `/modality/8/subcategories/1/items/4/extracted/overview` | 소프라노 티타늄 레이저 서술 vs RF 리프팅 적응증. | 적응증 채택 시 확인 |
| S028-I02 | S028 | I | `/modality/8/subcategories/1/items/1/detail`, `/modality/8/subcategories/1/items/8/detail`, `/modality/8/subcategories/0/items/15/detail` | 제조사 표기 불일치(원텍/클래시스, 히로닉/하이로닉). | 제조사 정규화 후속 |
| S028-B01 | S028 | B | `/modality/8/subcategories/1/items/6/extracted/safety/serious/0` | '신경 손상(저설정시)' — 저설정이 위험 조건인지 오기인지 불명. | 조건 해석 불가 |
| S029-I01 | S029 | I | `/modality/8/subcategories/2/items/1` | 클래리파이: 마이크로웨이브 하위분류 vs RF 서술. | 에너지원 축 채택 시 확인 |
| S029-F01 | S029 | F | `/modality/8/subcategories/1/items/15`, `/modality/8/subcategories/1/items/3`, `/modality/3/subcategories/1/items/8` | 볼뉴머 계열 3레코드. | 개체 병합은 후속(원본 변경 후보) |
| S029-I02 | S029 | I | `/modality/8/subcategories/3/items/3/extracted/overview` | 튠페이스 '클래시스와 RF' 서술. | 구성 에너지 해석 시 detail 과 대조 |
| S030-B01 | S030 | B | `/modality/8/subcategories/4/items/0/detail`, `/modality/8/subcategories/4/items/1/detail` | 구성 수량(써마지600, 소프웨이브200)의 단위·'튠' 대상 불명. | 패키지 구성 해석 제한 |
| S030-I01 | S030 | I | `/modality/8/subcategories/4/items/1/extracted/overview`, `/modality/8/subcategories/4/items/1/detail` | DNA리셋프로그램 구성 vs HIFU 서술. | 패키지 설명 채택 시 확인 |
| S030-I02 | S030 | I | `/modality/8/products/5/type`, `/modality/8/products/4/manufacturer` | 인모드 type, 올리지오 제조사 불일치. | 제품 속성 정규화 후속 |
| S030-F01 | S030 | F | `/modality/8/subcategories/4` | 가격·구성 수량을 담은 판매 패키지가 시술 분류 트리 안에 있다. | 판매 구성 개체 분리 설계 과제 |
| S031-I01 | S031 | I | `/modality/8/products/6/type`, `/modality/8/products/6/extracted/overview` | LDM type(초음파) vs RF 서술. | 에너지원 속성 채택 시 확인 |
| S032-F01 | S032 | F | `/modality/9/subcategories/0/items/0`, `/modality/9/subcategories/0/items/1`, `/modality/9/subcategories/1/items/1`, `/modality/9/subcategories/1/items/7` | 같은 장비로 보이는 항목 쌍(엠페이스, 엠스컬프트네오/NEO). | 개체 병합 후속 |
| S032-I01 | S032 | I | `/modality/9/subcategories/1/items/4/extracted/aftercare/1` | RF 장비 aftercare 에 EMS 근육통 문장. | 관리 지시 채택 시 확인 |
| S032-F02 | S032 | F | `/modality/9/subcategories/1/items/5`, `/modality/9/subcategories/1/items/4` | M10 에 크라이오·RF 지방감소 장비. | 계열 경계 후속 |
| S033-B01 | S033 | B | `/modality/10/subcategories/0/items/0/extracted/aftercare/2`, `/modality/10/subcategories/0/items/1/extracted/aftercare/2`, `/modality/10/subcategories/0/items/6/extracted/aftercare/5` | 니들RF 출력 등급 판정 근거 없음. | S027-B01 과 같은 성격 |
| S033-B02 | S033 | B | `/modality/10/subcategories/0/items/1/detail` | 시크릿RF detail 빈 문자열. | 제조사 정보 없음 |
| S033-F01 | S033 | F | `/modality/10/subcategories/0/items/8` | 니들RF 하위분류에 비침습 모노폴라 RF 서술 항목. | 계열 경계 후속 |
| S034-I01 | S034 | I | `/modality/10/products/3/name`, `/modality/10/products/3/name_en` | 제니스/AGNES 이름 불일치. | 제품 식별 — 원본 확인 후보 |
| S034-I02 | S034 | I | `/modality/10/extracted/mechanism`, `/modality/10/extracted/safety/uncommon/0`, `/modality/10/extracted/aftercare/0` | 모달리티 설명 안에서 색소침착·딱지 유무 진술 정도 차이. | 부작용 정보 채택 시 확인 |
| S035-I01 | S035 | I | `/modality/11/subcategories/0/items/1/extracted/overview` | '스탐프형' 오기. | 표기 보존 |
| S037-I01 | S037 | I | `/modality/13/subcategories/0/items/1` | 바넥스(RF+석션)가 냉각지방분해 하위분류·PAH 지시. | 분류·안전 지시 정합 후속 |
| S038-I01 | S038 | I | `/modality/14/subcategories/0/items/6/extracted/mechanism`, `/modality/14/subcategories/0/items/7/extracted/overview` | 라라필/호박필 이름-성분 서술 엇갈림. | 항목 내용 혼입 의심 — 원본 확인 후보 |
| S038-I02 | S038 | I | `/modality/14/subcategories/0/items/8/extracted/overview`, `/modality/14/subcategories/0/items/4/detail`, `/modality/14/subcategories/0/items/4/extracted/mechanism` | 밀크필(물리 클렌징), GA필(글리콜산 vs 복합산) 서술 불일치. | 성분 축 분류 시 확인 |
| S038-B01 | S038 | B | `/modality/14/subcategories/0/items/2/detail`, `/modality/14/subcategories/0/items/3/detail`, `/modality/14/subcategories/0/items/5/detail`, `/modality/14/subcategories/0/items/6/detail`, `/modality/14/subcategories/0/items/7/detail`, `/modality/14/subcategories/0/items/8/detail` | 브랜드성 필링 6항목 detail 빈 문자열. | 제조사·성분 식별 정보 부족 |
| S039-F01 | S039 | F | `/modality/14/subcategories/0/items/19`, `/modality/14/subcategories/0/items/30`, `/modality/14/subcategories/0/items/31`, `/modality/14/subcategories/0/items/34`, `/modality/14/subcategories/0/items/33` | 케미컬필링 하위분류에 물리적 박피·메조테라피성 항목. | 박피 방식 축 분해는 설계 단계 |
| S039-F02 | S039 | F | `/modality/14/subcategories/0/items/20`, `/modality/14/subcategories/0/items/3` | 블랙필링/블랙필 유사 이름 별개 항목. | 동일성 판단 후속 |
| S040-I01 | S040 | I | `/modality/14/subcategories/0/items/43/extracted/mechanism` | 알렉스필(필링)에 레이저 755nm 기전. | 기전 정보 채택 시 확인 |
| S040-F01 | S040 | F | `/modality/14/subcategories/0/items/44/detail`, `/modality/14/subcategories/0/items/54/detail`, `/modality/14/subcategories/0/items/49/detail` | 항목 간 변형·업그레이드 참조 표현(라라필→라라닥터, 제스너→쿰스필). | 관계는 원문 표현으로만 보존 — 연결은 후속 |
| S041-I01 | S041 | I | `/modality/14/subcategories/1/items/2/extracted/indications/primary`, `/modality/14/subcategories/1/items/2/extracted/safety` | 라라젯 (클렌징) 적응증·부작용이 클렌징과 맞지 않음. | 레코드 혼입 의심 — 원본 확인 후보 |
| S041-F01 | S041 | F | `/modality/14/subcategories/2/items/0`, `/modality/14/subcategories/2/items/3`, `/modality/14/subcategories/0/items/59`, `/modality/14/subcategories/0/items/29` | 표기만 다른 항목 쌍(옴니룩스/옴니럭스), 이름·별칭 중복(물톡스). | 개체 병합 후속 |
| S042-F01 | S042 | F | `/modality/14/subcategories/3/items/0`, `/modality/8/products/6`, `/modality/14/subcategories/5/items/5`, `/modality/14/subcategories/1/items/2` | 같은 이름 장비가 다른 계열·하위분류에(LDM, 라라젯). | 장비 개체 병합·용도 분리는 설계 단계 |
| S042-B01 | S042 | B | `/modality/14/subcategories/6/label`, `/modality/14/subcategories/7/label` | 하위분류 label '추가' 2개 — 분류 의미 정보 없음. | 하위분류 의미 판단 불가 |
| S043-F01 | S043 | F | `/modality/14/subcategories/9`, `/modality/14/subcategories/10` | M15 안에 고민 축(탈모)과 외용약 성분 하위분류. | 시술/성분/고민 개체 분리는 설계 단계 |
| S043-F02 | S043 | F | `/modality/14/subcategories/9/items/0`, `/modality/7/subcategories/5/items/13` | LLLT 항목 두 곳(하나는 빈 extracted). | 개체 병합 후속 |
| S044-F01 | S044 | F | `/modality/14/subcategories/11/items/2`, `/modality/14/subcategories/11/items/3`, `/modality/14/subcategories/12/items/0`, `/modality/14/subcategories/12/items/1` | '관리' 모달리티에 주사·외과적 시술·경구약 항목. | 시술 방식 축과 group 값의 관계 재검토 필요(설계) |
| S044-F02 | S044 | F | `/modality/14/subcategories/13`, `/modality/8/subcategories/4` | 시그니처 프로그램이 M9·M15 두 곳. | 판매 구성 개체 분리(S030-F01 과 묶음) |
| S045-B01 | S045 | B | `/modality/14/subcategories/14/items`, `/modality/14/subcategories/15/items` | M15-도포·M15-팩 하위분류 items 빈 배열. | 해당 관리 항목 정보 없음 |
| S045-F01 | S045 | F | `/modality/14/subcategories/13` | 시그니처프로그램 조합 항목이 다른 모달리티 시술·제품명 문자열로 구성(연결 키 없음). | 조합 관계 설계 과제(S030-F01·S044-F02) |
| S046-I01 | S046 | I | `/modality/15/subcategories/1/items/0/naming_caveat`, `/modality/15/subcategories/1/items/0/extracted/mechanism` | 마늘주사 '마늘 추출물 아님' vs '마늘 추출물의 협력작용'. | 성분 서술 채택 시 확인 |
| S046-F01 | S046 | F | `/modality/15/subcategories/0/items/3`, `/modality/15/subcategories/1/items/1` | 같은 성분(알파리포산)이 두 항목·두 하위분류. | 성분-마케팅명 관계 설계 |
| S046-F02 | S046 | F | `/modality/15/subcategories/0/items/0/canonical_category`, `/modality/15/subcategories/1/items/0/canonical_category`, `/modality/15/subcategories/1/items/1/canonical_category` | canonical_category 경로 하위명이 실제 label 과 불일치(S012-F02 와 같은 성격). | 표준 분류 매핑 후속 |
| S047-F01 | S047 | F | `/modality/15/subcategories/2/items/3`, `/modality/15/subcategories/2/items/1`, `/modality/15/subcategories/3/items/0`, `/modality/15/subcategories/0/items/5`, `/modality/15/subcategories/3/items/1`, `/modality/15/subcategories/1/items/6` | 같은 성분 항목 중복(NAD+, 비타민D, 종합비타민/마이어스칵테일). | 개체 병합 후속 |
| S047-I01 | S047 | I | `/modality/15/subcategories/3/items/0/extracted/mechanism`, `/modality/15/subcategories/0/items/5/extracted/overview` | 비타민D 투여 경로 서술 불일치(정맥/근육). | 경로 속성 채택 시 확인 |
| S047-F02 | S047 | F | `/modality/15/subcategories/4` | 수액치료 모달리티 안 지방분해 주사제 하위분류. | 계열 경계(S048 LIPO 와 묶음) 후속 |
| S048-I01 | S048 | I | `/modality/15/subcategories/6/items/1`, `/modality/15/subcategories/4/description` | PPC 미용목적 사용 금지 진술과 PPC 시술 항목 공존. | 추천·표시 단계에서 사용 전 확인 필요 — 원본 확인 후보(지금 선택 대기 아님) |
| S048-I02 | S048 | I | `/modality/15/subcategories/4/items/10/extracted/safety`, `/modality/15/subcategories/4/items/10/detail` | 뉴비쥬 '부작용 감소' 주장 vs DCA 와 동일 safety 블록. | 부작용 정보 채택 시 확인 |
| S048-B01 | S048 | B | `/modality/15/subcategories/6/items/0/extracted/aftercare/1`, `/modality/15/subcategories/6/items/0/detail` | 셀레늄 항목 detail 빈 문자열, 항산화제 복용 회피 지시의 이유 불명. | 관리 지시 해석 제한 |
| S049-I01 | S049 | I | `/modality/15/subcategories/6/items/3/name`, `/modality/15/subcategories/6/items/3/extracted/overview` | HP주사(감초주사) 이름 vs 성분 서술(PPC+DCA). | 성분·안전 정보 채택 전 확인 — 원본 확인 후보 |
| S049-I02 | S049 | I | `/modality/15/subcategories/6/items/7/detail`, `/modality/15/subcategories/6/items/7/extracted/mechanism` | 프로락틴/프로작 표기 혼재. | 물질 식별 불가 — 원본 확인 후보 |
| S049-B01 | S049 | B | `/modality/15/subcategories/6/items/12/extracted/mechanism`, `/modality/15/subcategories/6/items/13/extracted/mechanism` | 부위별 지방분해주사 성분 미기재. | 성분 축 분류 불가 |
| S049-F01 | S049 | F | `/modality/15/subcategories/6/items/5`, `/modality/15/subcategories/6/items/11` | LDM·NAD+ 계열 중복 레코드. | 개체 병합 후속(S042-F01, S047-F01 과 묶음) |
| S050-I01 | S050 | I | `/modality/16/subcategories/3/label`, `/modality/16/subcategories/3/items/0/extracted/mechanism` | '자가혈유래 줄기세포' label vs ADSC(지방유래) 서술. | 하위분류 의미 확인 필요 |
| S050-B01 | S050 | B | `/modality/16/subcategories/3/items/0/detail`, `/modality/16/subcategories/3/items/1/detail` | detail 빈 문자열. | 제조사 정보 없음 |
| S050-F01 | S050 | F | `/modality/16/subcategories/1`, `/modality/5/subcategories/2`, `/modality/16/subcategories/2`, `/modality/3/subcategories/2` | SVF·엑소좀이 두 모달리티 하위분류에. | 계열 경계 후속 |
| S051-I01 | S051 | I | `/problem/2/subcategories/0/items/2/detail`, `/problem/2/subcategories/0/items/2/modality_ref`, `/problem/8/subcategories/0/items/5/modality_ref` | detail 에 나열된 시술 계열과 modality_ref 가 일치하지 않는 항목. | 참조 완전성 판단 제한 — 후속 연결 과제 |
| S051-F01 | S051 | F | `/problem/0/subcategories/6/items/0/modality_ref`, `/problem/5/subcategories/0/items/2/modality_ref`, `/problem/6/subcategories/2/items/1/modality_ref`, `/problem/7/subcategories/2/items/0/modality_ref`, `/problem/8/subcategories/0/items/0/modality_ref`, `/problem/8/subcategories/0/items/1/modality_ref`, `/problem/8/subcategories/1/items/0/modality_ref`, `/problem/8/subcategories/2/items/1/modality_ref` | modality_ref 빈 배열 항목(일부는 M15 에 대응 항목 존재). | 고민-시술 연결 설계 시 확인 |
| S051-F02 | S051 | F | `/problem/0`, `/problem/9` | problem 최상위에 고민과 시술군이 같은 깊이. | 고민 개체 설계 과제 |
| S052-F01 | S052 | F | `/problem/10/subcategories/1/items/0/modality_ref`, `/problem/10/subcategories/1/items/1/modality_ref`, `/problem/11/subcategories/0/items/1/modality_ref`, `/problem/11/subcategories/0/items/4/modality_ref`, `/problem/12/subcategories/0/items/0/modality_ref`, `/problem/12/subcategories/2/items/0/modality_ref`, `/problem/13/subcategories/2/items/1/modality_ref` | modality_ref 빈 배열 항목 중 대응 후보가 modality 쪽에 이름으로 존재하는 것(윤곽주사↔M16-LIPO, 브이올렛↔M16-DCA, 두피메조↔M15, 미녹시딜↔M16, 미라드라이↔M9-3 마이크로웨이브 등). | 참조 보강 여부는 후속(원본 변경 후보, 지금 선택 대기 아님) |
| S052-B01 | S052 | B | `/problem/11/subcategories/0/items/2`, `/problem/11/subcategories/0/items/3`, `/problem/11/subcategories/0/items/5`, `/problem/11/subcategories/3/items/0`, `/problem/12/subcategories/3/items/0`, `/problem/12/subcategories/3/items/1` | HPL·BNLS·컷슬린·엔더몰로지·FUE·FUT 는 이름·짧은 detail 만 있고 modality 쪽 대응 항목이 없다. | 시술 내용 정보 부족 |
| S052-I01 | S052 | I | `/problem/11/subcategories/0/items/1`, `/modality/15/subcategories/4/description` | PPC 사용 금지 진술 vs PPC 지방분해주사 항목(problem 쪽). | S048-I01 과 같은 원본 확인 후보 |

## 알려진 형태소 분석 한계 (K · 규칙별)

출현별 위치·원시 토큰은 `morphology.json` 의 `known_segmentation_errors`. 교정하지 않고 기본 분석 결과를 보존했다.

| 기록 구획 | 표면형/태그 | 문제 | 영향 | 표시된 출현 수 |
|---|---|---|---|---|
| GLOBAL | (tag W_SERIAL) | kiwi 가 '3-7', '1.5/3.0', '755/808/1064', '5-5-5' 같은 숫자 연쇄를 W_SERIAL 한 토큰으로 묶는다 — 범위·목록·기법명이 같은 태그 | 형태소만으로 범위 하한·상한, 목록 원소를 구분할 수 없음. expressions auto(수량·단위) 원문 구간을 함께 써야 함 | 1576 |
| S001 | 제테마 | 회사명 '제테마'를 저/NP 의/JKG 테마/NNG 로 분절 | 회사명 토큰 소실, 조사 오탐 | 6 |
| S001 | 메디톡스 | 회사명 '메디톡스'를 메/NNG 디톡스/NNP 로 분절 | 제품·회사명 검색 시 '디톡스' 오탐 | 11 |
| S001 | 눈�리 | 원문 대체문자(U+FFFD) 때문에 눈/NNG �/SW 리/NNP | 원문 손상(S001-B01)과 연동. 분석 결과로 원래 글자를 추정하지 않음 | 1 |
| S001 | kDa의 | '900kDa의' 의 '의' 를 NNG 로 태깅(조사 JKG 아님) | 단위 뒤 조사 오탐 | 5 |
| S002 | 휴메딕스의 | '휴메딕스의' 전체를 NNG 하나로(조사 '의' 미분리) | 회사명 표면형에 조사 포함 | 1 |
| S002 | 비복근의 | 비/NNG 복/NNG 근/NNG 의/JKG — 근육명 '비복근' 분해(같은 원장 다른 곳은 비복근/NNG) | 부위 용어 일관성 없음 | 1 |
| S002 | 사다리꼴근 | 사다리꼴/NNG 근/NNG | 근육명 분해 | 1 |
| S002 | 저작근 | 저작/NNG 근/NNG | 근육명 분해 | 1 |
| S003 | 턱선보톡스 | 턱/NNG 선/NNG 보톡스/NNP — 붙여 쓴 시술명 분해 | 시술명 단위 소실(복합 표현으로 보존) | 1 |
| S003 | 풀페이스큐레이션 | 풀/NNG 페이스/NNG 큐레이션/NNG | 패키지명 분해 | 1 |
| S003 | 에어보톡스 | 에어/NNP 보톡스/NNG — 다른 곳 보톡스/NNP 와 태그 다름 | 태그 일관성 없음 | 1 |
| S003 | 중증근무력증 | form 이 '중증 근무력증'(공백 포함 다어절 사전어)으로 표면형과 다름 | form 을 표면형으로 쓰면 원문과 불일치. surface 칸 사용 | 1 |
| S004 | 타임버스 | 제품명 '타임버스'를 타임/NNG 버스/NNG 로 분해 | 제품명 소실, '버스' 오탐 | 1 |
| S004 | 근신경접합부 | 근/NNG 신경/NNG 접합부/NNG | 해부 용어 분해(복합 표현으로 보존) | 1 |
| S005 | 더채움 | 제품명 '더채움'을 더/MAG 채우/VV ᆷ/EF 로 분석 | 제품명이 부사+동사로 바뀜 | 3 |
| S005 | G' | G/SL 뒤 아포스트로피를 SS 또는 SSO(여는 따옴표)로 태깅 — 저장탄성률 기호 G' 분리 | 물성 기호가 따옴표로 오인 | 17 |
| S005 | μm | μ/SW m/SL 로 분리 | 단위 μm 소실 | 2 |
| S005 | 법령선 | 법령/NNG 선/NNG — '법령선'(팔자주름 계열 표현으로 보임)을 '법령'(law) 으로 | 오탐 의미 | 6 |
| S005 | 겸립 | 겸/NNB 립/NNG — 원문 오기로 보이는 어절의 무의미 분해 | 원문 I 와 연동 | 1 |
| S006 | 스타일에이지 | 제품명을 스타일/NNG 에/JKB 이/VCP 지/EF 로 분석 | 제품명 소실, 조사·어미 오탐 | 1 |
| S006 | 벨로테로 | 벨로테/NNG 로/JKB — 제품명 끝 '로' 를 조사로 분리 | 제품명 절단 | 2 |
| S006 | 비순홈 | 비/NNG 순/NNG 홈/NNG | 해부 용어 분해 | 5 |
| S006 | 냉찜질 | 냉/NNG 찜/NNG 질/XSN 등으로 분해 | 관리 행위어 분해(복합 표현으로 보존) | 117 |
| S007 | 각동맥 | 각/MM 동맥/NNG — 해부명 '각동맥'의 '각'을 관형사로 | 부위명 분해·품사 오탐 | 2 |
| S007 | 드물음 | 문맥에 따라 드물음/NNP 또는 드물/VA 음/ETN | 빈도 수식어가 고유명사로 태깅되는 경우 있음(GLOBAL-K02) | 16 |
| S007 | 애교살 | 애교/NNG 살/NNG | 부위 생활어 분해 | 1 |
| S007 | >< | '><' 를 >/SSC </SSO 괄호류로 태깅 | 부등호 의미 소실 | 1 |
| S008 | 콜라쥬 | 제품명을 콜라/NNG 이/VCP 쥬/EF 로 분석 | 제품명 소실 | 1 |
| S008 | 디클래씨 | 디클래/NNP 씨/NNB — 제품명 끝 '씨'를 의존명사로 | 제품명 절단 | 1 |
| S008 | 콜라겐핀 | 콜라겐/NNP 핀/NNG | 제품명 분해 | 1 |
| S008 | 5-5-5 | 기법명 '5-5-5'를 W_SERIAL 한 토큰으로 — 범위·일련번호와 구분 안 됨 | GLOBAL-K01 과 같은 태그지만 범위 아님 | 3 |
| S009 | 리투오파인 | 리투오파/NNG 이/VCP ᆫ/ETM — 제품명 끝 '인' 을 서술격+어미로 | 제품명 절단 | 1 |
| S009 | 셀르디엠 | 단독 출현 시 셀/NNP 르/NNG 디/NNG 엠/NNG 로 분해(괄호 안에서는 셀르디엠/NNP) | 같은 제품명이 문맥별로 다르게 분석 | 2 |
| S009 | 울트라콜 | 울트라/NNG 콜/NNG | 제품명 분해 | 1 |
| S011 | 리쥬란 | '리쥬란아이','리쥬란HB+' 에서 리쥬/NNP 이/VCP 란/ETM 으로 분해(리쥬란힐러는 한 토큰) | 브랜드명이 서술격+어미로 바뀜 | 15 |
| S011 | 필로르가 | 단독 출현 시 필로르/NNP 가/JKS — 끝 '가' 를 조사로 | 제품명 절단 | 4 |
| S011 | 릴리이드M | 릴리/NNP 이드/NNG M/SL | 제품명 분해 | 1 |
| S011 | 박피부 | 박/NNG 피부/NNG — '얇은 피부(薄皮膚)' 의미가 '박' 으로 분리 | 수식 의미 소실 | 1 |
| S012 | 볼뉴머 | 볼/NNG 뉴/NNG 머/EC — 장비명이 어미까지 포함해 분해 | 기기명 소실 | 6 |
| S012 | 프로파일로 | 프로파일/NNP 로/JKB — 끝 '로' 를 조사로 | 제품명 절단 | 1 |
| S012 | 필로르가135HA | 필로르/NNG 가/JKS 135/SN HA/SL | 제품명 분해·조사 오탐 | 1 |
| S012 | ASCE+엑소좀 | 엑소/NNP 좀/MAG — '엑소좀'의 '좀'을 부사로 | 성분명 분해 | 1 |
| S012 | 드원셀 | 드/NNG 원/NNG 셀/NNG | 제품명 분해 | 1 |
| S013 | 벨피엔 | 벨피/NNG 엔/NNG 또는 벨피/NNG 에/JKB ᆫ/JX — 제품명이 조사로 분해 | 제품명 소실·문맥별 불일치 | 2 |
| S013 | 암침 | 암/NNG 침/NNG — '암침(暗沈, 칙칙함)'을 '암'(cancer?) 으로 분리 | 의미 오탐 위험 | 1 |
| S014 | 엑소솜 | '엑소솜'(다른 곳 '엑소좀') — 표기 변형. 분석 결과는 표기를 따른다 | 같은 성분명 두 표기 | 3 |
| S016 | 비가교HA | 비가교/NNP HA, 비/NNG 가교/NNG HA, 비가교/NNG HA 로 문맥별 상이 — 부정 접두 '비' 가 분리되기도 한다 | '비(非)' 부정 의미가 토큰 단위로 일관되지 않음 | 8 |
| S016 | 마리오네트라인 | 마리오네트/NNP 라인/NNG | 부위 표현 분해(복합 표현으로 보존) | 3 |
| S018 | 대이개신경 | 대/XPN 이/NR 개/NNB 신경/NNG — 신경명(great auricular nerve)을 접두사+수사 '이(2)'+단위 '개'로 분석 | 수량 오탐(2개) — 수치 추출 시 거짓 양 | 1 |
| S018 | 면봉합사 | 면/NNG 봉합/NNG 사/NNG | 재질어 분해 | 2 |
| S018 | 텐선실 | 텐/NNG 선/NNG 실/NNG | 제품명 분해 | 1 |
| S020 | 오타모반 | 문맥에 따라 오타/NNG 모반/NNG(오타=typo 오탐) 또는 오타모반/NNG | 질환명 분해·오탐 | 11 |
| S020 | Nd:YAG | Nd/SL :/SP YAG/SL — 콜론을 구두점으로 분리 | 레이저 매질명 분해(복합 표현으로 보존) | 42 |
| S021 | 주근깨토닝 | 주근깨/NNG 토/NNG 니/JC ᆼ/Z_CODA — '토닝'을 조사·받침 코드로 분해 | 시술명 소실, Z_CODA 태그 출현 | 1 |
| S021 | 어븀야그 | 어븀/NNP 야/EC(또는 IC) 그/MM — 'Er:YAG' 한글 표기를 어미·감탄사·관형사로 | 레이저 매질명 소실 | 3 |
| S021 | CO2 | CO/SL 2/SN 로 분리 | 매질명 분해(숫자 오탐 가능) | 38 |
| S021 | 픽토초 | 픽토초/NNP 또는 픽토/NNG 초/NNB — 원문 오기 + 문맥별 분석 차이 | S021-I02 | 2 |
| S022 | 브이빔 | 브이/NNG 비/VV ᆷ/EF — 장비명 끝 '빔' 을 동사+어미로 | 장비명 소실 | 2 |
| S022 | BBL포에버영 | form '포에버 영'(공백 포함 사전어)/NNP | form ≠ 표면형 | 1 |
| S022 | 장미증 | 장미/NNG 증/NNG | 질환명 분해 | 1 |
| S022 | 주사 | 질환명(주사비)으로 보이는 '주사' 가 주사/NNG — 시술 '주사(injection)' 와 형태소상 구분 불가 | 키워드 검색 시 오탐 | 1 |
| S023 | 더마브이 | 더/MAG 마/NNG 브이/NNG — 장비명 첫 음절을 부사 '더'로 | 장비명 소실·비교 부사 오탐 | 1 |
| S023 | 시너론 | 문맥별 시너론/NNG 또는 시너/NNP 론/XSN | 제조사명 불일치 분석 | 10 |
| S023 | 755/808/1064 | '/' 로 나열한 세 파장을 W_SERIAL 한 토큰으로 — 범위가 아니라 목록인데 GLOBAL-K01 과 같은 태그 | W_SERIAL 을 범위로 해석하면 오류 | 1 |
| S024 | https://classys.co.kr/product/reepot/ | URL 이 SL/SW 조각들로 분해됨(형태소 분석 대상 텍스트 안의 URL 을 따로 제외하지 않음) | URL 토큰은 언어 정보 아님 — 참조 표현은 expressions 에 원문 구간으로 보존 | 1 |
| S027 | 울쎄라 | 단독 '울쎄라' 를 울쎄/NNG 이/VCP 라/EC 로(텐쎄라도 같은 패턴) | 장비명 끝 '라' 를 서술격+어미로 — 장비명 소실 | 4 |
| S027 | 텐쎄라 | 텐쎄/NNG 이/VCP 라/EC | 장비명 소실 | 1 |
| S027 | 더블로 | 단독 '더블로' 를 더블/NNG 로/JKB | 장비명 절단 | 4 |
| S027 | 리니어펌 | 리니어/NNG 퍼/NNG ᆷ/EF | 장비명 소실 | 1 |
| S029 | 온다 | 장비명 '온다'를 오/VV ᆫ다/EF(동사 '오다')로 분석 | 장비명 소실·동사 오탐 | 3 |
| S029 | 에이전 | 에/IC 이전/NNG — 장비명을 감탄사+'이전'(before)으로 | 장비명 소실, 시간어 '이전' 오탐 | 1 |
| S029 | 볼뉴머RF | 볼/NNG 뉴/NNG 머/EC RF/SL | 장비명 소실 | 1 |
| S032 | 엠스컬프트NEO | 엠스컬프/NNG 트/VV NEO/SL — 끝 '트' 를 동사로 | 장비명 소실 | 1 |
| S032 | 복직근이개 | 복직근/NNP 이/JKS 개/NNG — '이개(diastasis)'를 조사+명사로 | 질환명 소실·조사 오탐 | 1 |
| S033 | 실펌X | 실/NNG 퍼/NNG ᆷ/ETN X/SL — 장비명을 명사화 어미로 | 장비명 소실 | 1 |
| S034 | 일루다 | 일루/MAG 다/MAG — 제조사명을 부사 두 개로 | 회사명 소실 | 1 |
| S035 | 더마롤러 | 더/MAG 마/MAG 롤러/NNG — 'derma' 의 '더' 를 비교 부사로 | 기구명 분해·부사 오탐(더마스탬프·더마펜4·더마브이도 같은 패턴) | 1 |
| S035 | 더마스탬프 | 더/MAG 마/NNG 스탬프/NNG | 기구명 분해 | 1 |
| S035 | 더마펜4 | 더/MAG 마/NNG 펜/NNG 4/SN | 제품명 분해 | 1 |
| S038 | 삼염화초산 | 삼/NR 염화/NNG 초산/NNG — 화합물명 접두 '삼(tri)'을 수사 3 으로 | 수량 오탐(3) | 1 |
| S038 | 레소르신 | 레소르/NNP 신/NNG | 성분명 분해 | 1 |
| S039 | 아크네필 | 아크/NNP 네/MM 필/NNB — '네'를 관형사(수 4)로 | 수량 오탐 가능 | 1 |
| S039 | 산소필 | 산소/NNG 필/NNB — '필'을 의존명사로 | 시술명 분해(CO2필도 필/NNB) | 1 |
| S040 | 진주필 | 진/NNP 주필/NNG — '진주' 를 진+주필(主筆)로 | 원료명 소실·다른 낱말 오탐 | 1 |
| S040 | 라라닥터 | 라/NNG 라/NNG 닥터/NNG | 제품명 분해(라라필 연결 표현 손실) | 1 |
| S044 | 이소트레티노인 | 문맥별 이소트레티노인/NNG·NNP 또는 이소트레티노/NNG 이/VCP ᆫ/ETM | 약물명이 서술격+어미로 분해되는 출현 있음 | 6 |
| S044 | 면포압출 | 면/NNG 포/NNG 압출/NNG — '면포(comedo)'를 면+포로 | 병변명 분해 | 1 |
| S046 | 비오틴주사 | 비오티/NNG ᆫ/JX 주사/NNG — 성분명 끝 받침을 조사로 | 성분명 소실 | 1 |
| S046 | 종합아미노산수액 | … 수/NNG 액/NNG — '수액' 분해 | 시술 유형어 분해 | 1 |
| S046 | 고농도C | 고/XPN 농도/NNG C/SL | 수식 접두 '고' 분리(정도 표현은 유지되나 토큰 단위) | 1 |
| S047 | 필발 | 필/NNG 발/NNG — 빈도어 '필발(必發)' 분해 | '거의 필발' 빈도 의미가 토큰으로 드러나지 않음 | 9 |
| S047 | 벨카이라 | 벨카/NNG 이/VCP 라/EC | 제품명 소실 | 1 |
| S047 | 셀레늄 | 셀/NNP 레늄/NNP | 원소명 분해 | 9 |
| S047 | 침침증 | 침/NNG 침/NNG 증/NNG — 원문 '침침증'(의미 불명 표기) | 원문 표기 자체 확인 필요(I 후보) | 1 |
| S048 | 다빼주사 | 다/MAG 빼/VV 어/EC 주사/NNG — 마케팅명(다 빼)을 부사+동사로 | 시술명이 '전부 빼다' 동작으로 분석(오탐 동사) | 1 |
| S048 | 뉴비쥬 | 뉴비/NNP 이/VCP 쥬/EF | 제품명 소실 | 1 |
| S048 | 리포린 | 리/NNG 포/NNG 린/NNG | 제품명 분해 | 1 |
| S049 | 복부슬림주사 | 복/NNG 부/NNG 슬/MAG 림/NNG 주사/NNG — '복부'·'슬림' 분해, 부사 오탐 | 부위어 '복부' 소실 | 1 |
| S049 | 초회통과효과 | 초/NNB 회/NNB 통과/NNG — '초회(first-pass)'를 단위 명사 두 개로 | 수량 단위 오탐(초·회) | 1 |


## batch-03 검토 후 기록 보완 (2026-11-09)

근거: `../../batch-03-review-taxonomy.md` §3-1·§3-2. 아래 수치는 문자열 값에서 단서 정규식이 부분 일치한 횟수다. 「미덮임」은 같은 Pointer 의 auto·manual 어느 표현 구간에도 포함되지 않은 출현이다. **의미 전수 조사 결과가 아니고, 누락 후보를 의미적으로 판정하거나 고친 것도 아니다.** 보완 워커가 `expressions.json`·`source-map.json` 을 읽기만 해서 다시 세어 보니 리뷰와 같았다. 차이는 Pa·N 하나다(13 대 14). 단서 정규식을 어떻게 정의하느냐에 따라 달라지는 차이라 리뷰 값을 그대로 옮긴다.

### K-EXPR01 — 정규식 자동 후보(auto)의 단서 패턴 공백

| 단서 | 출현 | auto·manual 어디에도 없음 | 비고 |
|---|---|---|---|
| `자제` (회피 지시) | 334 | 298 | 「부정·금지」 패턴에 없음. manual 대표 29건 |
| `깊` (깊이·깊숙이·깊게) | 180 | 77 | 패턴은 `깊은`만 잡음 |
| `얇` (두께) | 6 | 3 | 패턴 없음 |
| `서서히` · `점진` (변화 속도) | 16 · 56 | 13 · 44 | 속도 범주 패턴 없음 |
| `권장` · `주의` · `필요` (권고 강도) | 270 · 62 · 83 | 243 · 47 · 49 | 권고 강도 패턴 없음 |
| `심각` | 5 | 4 | 예: `심각한 볼륨 손실 복원` (`/modality/1/subcategories/2/items/0/extracted/indications/primary/1`) |
| `약 N` (근사) | 23 | 10 | 예: `약 3-4개월` (`/modality/0/subcategories/1/items/1/extracted/onset_duration/duration`) |
| 숫자 범위 + Pa·N 단위 | — | 14 (재셈 13) | 예: `G' 200-400 Pa` (`/modality/1/subcategories/0/items/2/extracted/mechanism`). 수량 패턴에 Pa·N 없음 |
| `시 ` (조건) | 360 | 270 | 조건 패턴에는 `시에`만 있음 |

리뷰가 미덮임 0 으로 확인한 단서는 `드물`·`드문`·`매우`·`극히`·`않`·`없`·`금지`·`가능`·`수 있`·`이상`·`이내`·`미만`·`경미`·`심한`·`얕`·`경우`·`%`·`~` 범위다.

- **기존 표현과의 차이:** `expressions.json` 의 manual 1,073 은 구획을 직접 읽으며 고른 대표 표현이다. auto 10,974 는 `method.patterns` 에 든 단서만 잡는다. 따라서 「모든 원문 보존」은 원문 값·Pointer·형태소 토큰(`source-map.json`·`morphology.json`)에 해당하는 말이고, 표현 후보까지 전부 모았다는 뜻은 아니다. 위 출현은 표현 기록에 없다.
- **영향:** 표현 기록만 보고 회피·깊이·두께·속도·권고 강도·근사·물성 단위·`… 시` 조건을 찾으면 위 출현이 빠진다. 이 축을 쓰는 후속 의미 조사·실버 설계에서는 해당 필드의 원문 문맥(`review-part-S###.md` 원문 값 표, `source-map.json`)을 다시 읽어야 한다.
- **상태:** 열림. 이번 보완에서 후보를 다시 뽑거나 rebuild 하지 않았다. 원문 보존만으로는 이 미결이 해결되지 않는다. 후속 과제는 이 단서들을 포함해 표현 후보를 보강하는 것과, 미덮임 출현이 무엇을 수식하는지 원문으로 확인하는 것이다.

### OBS-M16-PRODUCTS — M16 products 빈 배열 (관찰 누락 보완)

- 위치: `/modality/15/products` (구획 S049). 원문 값 `[]` — `source-map.json` 과 `review-part-S049.md` 원문 값 표(빈 배열)에 이미 있다.
- 관찰: 비어 있는 products 7개(M6·M10·M12·M13·M14·M15·M16) 가운데, 구획 관찰 문장에 「products 빈 배열」이 적히지 않은 것은 M16 하나뿐이었다(리뷰 §3-2). 빈 배열이 「해당 제품 없음」인지 「미수집」인지 원문에 나오지 않는다. **뜻 미상.**
- 영향: 제품 연결을 설계할 때 빈 배열을 「없음」으로 읽지 말아야 한다. 다른 빈 products 6개(S015·S032·S035·S036·S037·S045 관찰)와 같은 미상 상태다. GLOBAL-B01 묶음에는 빈 products 가 들어 있지 않다. 문서 기록이며 구조화 미결 JSON 에는 넣지 않았다.
