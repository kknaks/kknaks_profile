# market-pricing.json — 미결 기록

상태 문자: A 에이전트 오류 · B 원문 정보 부족 · C 현재 사용자 결정 필요 · I 원문 내 불일치 · P 잠정 · F 후속 · K 알려진 분석 한계.
이 파일은 build.py 가 manual/S*.json · manual/cross-issues.json 에서 생성한다(직접 고치지 않는다).

## 집계

| 상태 | 건수 |
|---|---|
| A — 에이전트 추출/해석 오류 | 0 |
| B — 원문 정보 부족 | 30 |
| C — 현재 사용자 결정 필요 | 0 |
| I — 원문 내 불일치(원본 보존, 후속 확인 후보) | 4 |
| P — 잠정 해석 | 12 |
| F — 후속 의미·연결 조사 | 7 |
| K — 알려진 분석 한계 | 4 |

원장 전반에 걸친 항목은 구획 X 로 적는다. 다른 원장은 열지 않았고, 다른 원장과의 연결은 모두 후속(F)이다.

## A — 에이전트 추출/해석 오류

없음 — 검증(verify.py)에서 Pointer·구간·원문 재현·소유 누락/중복 오류 0. 작업 중 발견해 고친 추출 오류는 validation.md §작업 중 고친 것 에 기록.

## B — 원문 정보 부족

| ID | 구획 | Pointer | 내용 |
|---|---|---|---|
| B-S00-1 | S00 | `/updated` | 가격 기준 시점: 원장 갱신일만 있고 가격 조사 시점·출처·표본이 없다. 시점별 가격 비교·최신성 판단이 제한된다. |
| B-S00-2 | S00 | `/note` | low·mid·high 의 통계적 정의가 없다. mid 를 '보통 가격' 으로 쓰거나 평균으로 계산하는 것이 근거 없이 된다. |
| B-S00-3 | S00 | `/note` | 부가세·마취·재료 포함 여부, 클리닉/지역/의사별 차이 값이 없다. 지역별 가격 질의에 답할 수 없다. |
| B-S01-1 | S01 | `/categories/0/items/0/unit` | 보톡스 '1회' 가격의 용량(유닛)·제품명이 없다(10항목). 용량 기준 가격 비교가 제한된다. |
| B-S02-1 | S02 | `/categories/1/items/0/name` | 'HA' 의 풀이·제품명이 없다(8항목). 제품별 가격 구분이 불가하다. |
| B-S03-1 | S03 | `/categories/2/items/1/name`, `/categories/2/items/1/unit` | '3회 패키지' 의 회당 용량·간격·총 바이알 수가 없다. 회당 가격 비교가 제한된다. |
| B-S03-2 | S03 | `/categories/2/items/2/name`, `/categories/2/items/3/name` | 'S'·'M' 변형의 뜻이 원문에 없다. |
| B-S04-1 | S04 | `/categories/3/items/5/unit` | '부위/1회' 의 '부위' 가 어떤 부위(크기)인지 없음. |
| B-S04-2 | S04 | `/categories/3/items/6/name` | '물광주사' 에 쓰는 제품·용량이 없다. |
| B-S05-1 | S05 | `/categories/4/items/4/name` | '부위당' 의 부위 크기·정의가 없다. |
| B-S06-1 | S06 | `/categories/5/items/0/unit` | 지방이식 '1회' 의 주입량·채취 부위·마취 포함 여부가 없다. |
| B-S07-1 | S07 | `/categories/6/items/0/name` | '10줄 기준' 외 줄 수의 가격, 실 종류별(PDO 외) 차이가 없다. |
| B-S07-2 | S07 | `/categories/6/items/2/name`, `/categories/6/items/3/name`, `/categories/6/items/4/name`, `/categories/6/items/6/name` | unit '1회' 항목들의 줄 수가 없다. |
| B-S08-1 | S08 | `/categories/7/items/4/name` | '엑셀V' 의 적용 부위·범위가 없다(고민만 있음). |
| B-S08-2 | S08 | `/categories/7/items/6/name`, `/categories/7/items/7/name` | 제모 회차·패키지 구성 없음. |
| B-S09-1 | S09 | `/categories/8/name` | 항목별 HIFU/RF 계열 표시가 없다. |
| B-S09-2 | S09 | `/categories/8/items/0/unit` | unit '1회' 장비 항목들의 샷 수가 없다(써마지만 샷 수 있음). |
| B-S10-1 | S10 | `/categories/9/items/3/name` | '4회 패키지' 의 부위·간격이 없다. |
| B-S11-1 | S11 | `/categories/10/items/4/name`, `/categories/10/items/5/name`, `/categories/10/items/6/name` | 고민 축 항목의 장비·적용 범위가 없다. |
| B-S12-1 | S12 | `/categories/11/items/2/name` | 'MTS + 스킨부스터' 의 스킨부스터 제품·용량·범위가 없다. |
| B-S12-2 | S12 | `/categories/11/items/4/name` | '집중' 의 차이(밀도·깊이·회차)가 없다. |
| B-S13-1 | S13 | `/categories/12/items/1/name`, `/categories/12/items/2/name`, `/categories/12/items/4/name` | 부위·범위 크기 없이 고민·목적만 있는 항목의 시술 범위가 없다. |
| B-S14-1 | S14 | `/categories/13/items/0/unit`, `/categories/13/items/5/name` | '1부위'·'소부위' 의 크기 정의가 없다. |
| B-S15-1 | S15 | `/categories/14/items/6/name`, `/categories/14/items/2/name` | '풀코스' 구성·'LDM' 풀이 없음. |
| B-S15-2 | S15 | `/categories/14/items/1/name` | 박피 성분 농도·범위 없음. |
| B-S16-1 | S16 | `/categories/15/items/0/unit` | 수액 용량·농도·성분 함량이 없다(8항목). '고농도'의 기준값 없음. |
| B-S17-1 | S17 | `/categories/16/items/5/name` | '3회 패키지' 구성 시술·간격이 없다. |
| B-S17-2 | S17 | `/categories/16/items/4/name` | '관절치료' 의 관절 부위·범위가 없다. |
| B-X-1 | X | `/categories/0/items/0/low` | 항목마다 가격 출처·조사 시점·지역(시·도)·표본 수가 없다(122항목). 가격 신뢰도·지역별 비교가 제한된다. |
| B-X-2 | X | `/categories/0/items/0/low`, `/categories/0/items/0/mid`, `/categories/0/items/0/high` | low·mid·high 가 1회/패키지 총액인지, 부가세 포함인지 원문에 없다(122항목). 회차 패키지(3회·4회)의 회당 가격 계산이 근거 없이 된다. |

## C — 현재 사용자 결정 필요

0건. 잔여 B·I·P·F·K 를 검토했고, 지금 사용자가 고를 선택지는 없다 — B 는 원문 부족(사용자 추측으로 메우지 않음), I 는 원본 보존 지시 아래 후속 확인 후보, P·F 는 21개 원장 비교 후 설계 단계에서 묶어 제시할 과제다.

## I — 원문 내 불일치(원본 보존, 후속 확인 후보)

| ID | 구획 | Pointer | 내용 |
|---|---|---|---|
| I-S05-1 | S05 | `/categories/4/items/4/name`, `/categories/4/items/4/unit` | name '(부위당)' 과 unit '1회' 의 가격 기준이 다르게 적혀 있다. 원본 보존 — 둘 중 어느 쪽이 기준인지 후속 확인 후보. |
| I-S07-1 | S07 | `/categories/6/items/5/name`, `/categories/6/items/5/unit` | name 은 줄 수 기준('20줄 이상'), unit 은 '1회' — 가격 기준 표기가 항목 안에서 다르다. 원본 보존, 후속 확인 후보. |
| I-S08-1 | S08 | `/categories/7/items/9/name`, `/categories/7/items/9/unit` | '문신 제거 (10cm2)' 면적 기준과 unit '1회' 가 함께 있다. 10cm2 의 역할(상한·단위면적) 원문 없음 — 후속 확인 후보. |
| I-S14-1 | S14 | `/categories/13/items/5/name`, `/categories/13/items/5/unit` | name '1개' 와 unit '1부위' 의 표기가 다르다(같은 뜻인지 확인 후보). |

## P — 잠정 해석

| ID | 구획 | Pointer | 내용 |
|---|---|---|---|
| P-S00-1 | S00 | `/currency` | currency 가 모든 low·mid·high 에 적용된다는 것은 구조상 추정. 후속 실버 설계에서 적용 범위를 명시해야 한다. |
| P-S01-1 | S01 | `/categories/0/items/9/name` | '(네페르티티)' 의 역할(기법명·별칭)은 잠정. 같은 카테고리의 괄호가 원산지·별칭 두 역할로 쓰인다. |
| P-S02-1 | S02 | `/categories/1/items/1/name` | '볼륨' 이 고민(볼륨 부족)인지 목적(볼륨 증가)인지 잠정. 부위/고민 분리는 후속 의미 조사. |
| P-S03-1 | S03 | `/categories/2/name` | 카테고리 이름의 '/' 의미(대안·별칭·병기) 잠정. 같은 형식이 M5·M9·M10 에도 있음. |
| P-S04-1 | S04 | `/categories/3/items/5/unit` | '부위/1회' 의 '/' 의미 잠정. 가격 분모(부위당·회당)를 확정하지 않는다. |
| P-S06-1 | S06 | `/categories/5/items/3/name`, `/categories/5/items/6/name` | '풀페이스' 와 '전체얼굴' 이 같은 범위인지 잠정 — 원장 전반(M8·M9·M11 등)에 두 표기가 섞여 있다. |
| P-S10-1 | S10 | `/categories/9/items/5/name` | '팔뚝/허벅지' 가 대안(둘 중 하나)인지 잠정. |
| P-S13-1 | S13 | `/categories/12/items/4/name` | '비수술' 이 수술 대비 방식을 말하는 부정 표현이라는 것은 잠정. 수식 대상(시술 전체)은 원문 위치로만 보존. |
| P-S16-1 | S16 | `/categories/15/items/0/name` | 괄호가 성분·제품·목적 세 역할로 쓰인다 — 역할 구분은 잠정. |
| P-X-1 | X | `/categories/3/items/5/unit`, `/categories/7/items/4/name`, `/categories/9/items/5/name`, `/categories/12/items/3/name`, `/categories/14/items/1/name`, `/categories/2/name`, `/categories/4/name`, `/categories/8/name`, `/categories/9/name` | '/' 가 대안·나열·분모 중 무엇인지 출현마다 다를 수 있다. README '/'=둘 중 하나 규칙을 이 원장에 그대로 적용할지 잠정. |
| P-X-2 | X | `/categories/0/items/0/name` | 항목 name 은 하나의 문자열에 시술/제품/장비·부위·고민·목적·용량·회차·원산지가 섞여 있다. 괄호의 역할도 항목마다 다르다(부위·용량·성분·목적·별칭·원산지). 분해 규칙은 후속. |
| P-X-3 | X | `/categories/0/items/0/low` | 122항목 모두 low < mid < high (기계 확인). mid 가 (low+high)/2 와 같은 항목은 122 중 3 — mid 는 산술 중간값이 아니다. mid 의 정의는 B-S00-2. |

## F — 후속 의미·연결 조사

| ID | 구획 | Pointer | 내용 |
|---|---|---|---|
| F-S03-1 | S03 | `/categories/2/items/4/name`, `/categories/3/items/2/name` | '쥬베룩 볼륨'(M3)과 '쥬베룩 파인'·'쥬베룩 울트라'(M4)가 서로 다른 카테고리에 있다 — 제품 계열·변형 관계는 후속 연결 과제. |
| F-S05-1 | S05 | `/categories/4/items/5/name`, `/categories/11/items/1/name` | 'PRP + MTS 콤보'(M5)와 'MTS + PRP (전체얼굴)'(M12)가 순서·부위표기·가격이 다르다. 같은 조합인지 후속 연결 과제(병합하지 않음). |
| F-S15-1 | S15 | `/categories/14/items/5/name` | '시술 후' 가 가리키는 시술이 원문에 없다 — 참조 표현과 위치만 보존, 연결은 후속. |
| F-S17-1 | S17 | `/categories/16/items/1/name`, `/categories/4/items/2/name` | '줄기세포 엑소좀'(M17)과 '엑소좀'(M5)의 관계는 후속 연결 과제(병합하지 않음). |
| F-X-1 | X | `/categories/0/items/0/name` | 같은 카테고리 안 항목 이름 축이 섞인다: 부위 축(M1·M2·M6), 제품/장비 축(M3·M4·M8·M9·M11 일부), 고민 축(M11 items/4~6·M13). 시술·부위·고민 분리는 후속 의미 조사. |
| F-X-2 | X | `/categories/5/items/3/name`, `/categories/5/items/6/name`, `/categories/8/items/0/name` | '풀페이스'·'전체얼굴'·'전신' 등 범위 표현이 카테고리마다 다르다. 같은 범위인지 후속. |
| F-X-3 | X | `/categories/0/name` | 카테고리 id(M1~M17)·name 이 다른 원장의 분류와 같은 체계인지 이 원장만으로 알 수 없다. 원장 간 연결은 21개 비교 후. |

## K — 알려진 분석 한계

| ID | 구획 | Pointer | 내용 |
|---|---|---|---|
| K-S00-1 | S00 | `/note` | Kiwi 가 '정가'를 '정/NNP + 가/XSN' 으로 분절 — 형태소 기본 결과를 보존하고 알려진 오분절로 기록. |
| K-S08-1 | S08 | `/categories/7/items/2/name`, `/categories/7/items/9/name` | 'CO2'·'10cm2' 가 SL/SN 으로 쪼개짐 — 기본 결과 보존, 출현 기록. |
| K-X-1 | X | `/categories/3/items/5/name`, `/categories/9/items/0/name`, `/categories/11/items/3/name` | 제품·장비명 후보 오분절 21출현(정가·쥬베룩·리쥬란·볼뉴머·부위당·리프팅·양쪽·몰딩·이모드·더마펜·이중턱·소부위·영숫자혼합 CO2/10cm2/B1). 수식 탐색 영향: '더'(더마펜)·'딩'(몰딩) 부사 오탐, '이'(이모드)·'양'(민트 양쪽) 관형사 오탐, '볼'(볼뉴머) 부위 오탐, '소'(소부위) 크기 수식 누락, '당'(부위당) 분모 누락. 기본 결과 보존·교정 안 함. 이 목록은 직접 대조한 서명 일치분이며, 그 밖 토큰의 정답성은 보장하지 않는다. |
| K-X-2 | X | `/categories/2/items/4/name`, `/categories/3/items/3/name`, `/categories/3/items/6/name`, `/categories/14/items/4/name`, `/categories/15/items/4/name` | 같은 말의 분석 불일치(오류 아님 포함): '쥬베룩' 분절/비분절, '비타민C' NNP 한 토큰 vs '비타민/NNG C/SL', '줄기세포' NNG/NNP·'줄기/세포' 분절, '엑소좀' NNP/NNG, '풀페이스' NNG/NNP. 토큰 기준 집계 시 같은 말이 갈라진다 — 원문 구간 기준으로 다룬다. |

알려진 오분절 출현 전체(morphology.json `known_missegmentation_occurrences`):

- K-정가 `/note` [34,36) `정가` → [['정', 'NNP'], ['가', 'XSN']]
- K-쥬베룩 `/categories/2/items/4/name` [0,3) `쥬베룩` → [['쥬베', 'NNG'], ['룩', 'NNG']]
- K-쥬베룩 `/categories/2/items/5/name` [0,3) `쥬베룩` → [['쥬베', 'NNG'], ['룩', 'NNG']]
- K-리쥬란 `/categories/3/items/0/name` [0,3) `리쥬란` → [['리쥬', 'NNP'], ['이', 'VCP'], ['란', 'ETM']]
- K-리쥬란 `/categories/3/items/1/name` [0,3) `리쥬란` → [['리쥬', 'NNP'], ['이', 'VCP'], ['란', 'ETM']]
- K-쥬베룩 `/categories/3/items/2/name` [0,3) `쥬베룩` → [['쥬베', 'NNG'], ['룩', 'NNG']]
- K-볼뉴머 `/categories/3/items/5/name` [0,3) `볼뉴머` → [['볼', 'NNG'], ['뉴', 'NNG'], ['머', 'EC']]
- K-부위당 `/categories/4/items/4/name` [9,12) `부위당` → [['부위당', 'NNP']]
- K-리프팅(민트) `/categories/6/items/2/name` [3,6) `리프팅` → [['리프', 'NNP'], ['팅', 'NNP']]
- K-양쪽(민트) `/categories/6/items/2/name` [8,10) `양쪽` → [['양', 'MM'], ['쪽', 'NNB']]
- K-몰딩 `/categories/6/items/3/name` [0,2) `몰딩` → [['몰', 'NNG'], ['딩', 'MAG']]
- K-이모드 `/categories/9/items/0/name` [0,3) `이모드` → [['이', 'MM'], ['모드', 'NNG']]
- K-이모드 `/categories/9/items/1/name` [0,3) `이모드` → [['이', 'MM'], ['모드', 'NNG']]
- K-이모드 `/categories/9/items/2/name` [0,3) `이모드` → [['이', 'MM'], ['모드', 'NNG']]
- K-이모드 `/categories/9/items/3/name` [0,3) `이모드` → [['이', 'MM'], ['모드', 'NNG']]
- K-더마펜 `/categories/11/items/3/name` [0,3) `더마펜` → [['더', 'MAG'], ['마', 'NNG'], ['펜', 'NNG']]
- K-이중턱 `/categories/13/items/2/name` [10,13) `이중턱` → [['이', 'NNP'], ['중턱', 'NNG']]
- K-소부위 `/categories/13/items/5/name` [5,8) `소부위` → [['소', 'NNG'], ['부위', 'NNG']]
- K-영숫자혼합 `/categories/7/items/2/name` [0,3) `CO2` → [['CO', 'SL'], ['2', 'SN']]
- K-영숫자혼합 `/categories/7/items/9/name` [7,12) `10cm2` → [['10', 'SN'], ['cm', 'SL'], ['2', 'SN']]
- K-영숫자혼합 `/categories/15/items/2/name` [9,11) `B1` → [['B', 'SL'], ['1', 'SN']]

