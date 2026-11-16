# S08 — M8 레이저 (10항목)

[← review.md](review.md) · 소유 말단 52 · 직접 읽기 ○ · 마지막 읽은 Pointer `/categories/7/items/9/high`

## S08

### 상위 문맥 (S00 소유, 공동 참조)

- `/currency` = `KRW` · `/updated` = `2026-07-26` · `/note` = `한국 시장 참고 가격 범위. 클리닉/지역/의사에 따라 상이. 정가 아닌 시장 범위.`

### 원문 값 — 카테고리

| Pointer | 원본 컬럼명 | 자료형 | 원문 값 |
|---|---|---|---|
| `/categories/7/id` | `id` | string | `M8` |
| `/categories/7/name` | `name` | string | `레이저` |
| `/categories/7/items` | `items` | array[10] of object | (아래 표) |

### 원문 값 — `items` (원본 순서, 각 값의 Pointer = 항목 Pointer + `/` + 컬럼명)

자료형: `name`·`unit` string, `low`·`mid`·`high` integer.

| 항목 Pointer | `name` | `unit` | `low` | `mid` | `high` |
|---|---|---|---|---|---|
| `/categories/7/items/0` | 피코토닝 (전체얼굴) | 1회 | 50000 | 100000 | 200000 |
| `/categories/7/items/1` | 피코프락셀 (전체얼굴) | 1회 | 100000 | 200000 | 400000 |
| `/categories/7/items/2` | CO2 프락셔널 (전체얼굴) | 1회 | 200000 | 400000 | 700000 |
| `/categories/7/items/3` | 제네시스 (전체얼굴) | 1회 | 50000 | 100000 | 200000 |
| `/categories/7/items/4` | 엑셀V (혈관/홍조) | 1회 | 100000 | 200000 | 400000 |
| `/categories/7/items/5` | IPL (전체얼굴) | 1회 | 50000 | 100000 | 200000 |
| `/categories/7/items/6` | 레이저 제모 (겨드랑이) | 1회 | 30000 | 60000 | 120000 |
| `/categories/7/items/7` | 레이저 제모 (전신) | 1회 | 200000 | 400000 | 800000 |
| `/categories/7/items/8` | 점 제거 (1개당) | 1개 | 5000 | 10000 | 30000 |
| `/categories/7/items/9` | 문신 제거 (10cm2) | 1회 | 100000 | 250000 | 500000 |

### 잠정 관찰 (원문 아님 — 근거 Pointer 와 상태)

| 근거 Pointer | 관찰 | 상태 |
|---|---|---|
| `/categories/7/items/0/name` | 장비/기법명 후보(피코토닝·피코프락셀·CO2 프락셔널·제네시스·IPL·엑셀V) + 괄호 적용 범위(전체얼굴). '피코토닝'·'피코프락셀' 은 '피코'+기법 결합어. | P |
| `/categories/7/items/4/name` | '엑셀V (혈관/홍조)' — 괄호가 부위가 아니라 고민/적응증 후보. '/' 는 두 고민의 나열 또는 대안 — 확정 불가. 적용 부위·범위 없음. | P |
| `/categories/7/items/6/name` | '레이저 제모 (겨드랑이)'·'(전신)' — 시술명은 카테고리명+목적, 괄호가 부위/범위. 제모 회차 수(패키지 여부)는 없음. | P |
| `/categories/7/items/8/name` | '점 제거 (1개당)' unit '1개' — name 과 unit 이 같은 기준(개당). 점 크기 기준 없음. | B |
| `/categories/7/items/9/name` | '문신 제거 (10cm2)' unit '1회' — name 괄호가 면적 '10cm2'(위첨자 없이 '2' 로 표기). 면적 기준과 회 기준이 항목 안에 함께 있음. 10cm2 가 상한인지 단위면적인지 원문에 없음. | I |
| `/categories/7/items/0/low` | 10항목 모두 low < mid < high. 최저가 항목은 '점 제거' low 5000. | P |

### 직접 읽기로 수집한 표현 (문자열 값 코드포인트 구간 [start,end))

| Pointer | 구간 | 원문 구절 | 탐색 관점(확정 분류 아님) | 메모 | 자동 패턴 동일 구간 |
|---|---|---|---|---|---|
| `/categories/7/items/0/name` | [0,4) | 피코토닝 | 장비/기법명 후보 |  | 없음(패턴 밖) |
| `/categories/7/items/0/name` | [5,11) | (전체얼굴) | 적용 범위, 부위 후보 |  | paren |
| `/categories/7/items/1/name` | [0,5) | 피코프락셀 | 장비/기법명 후보 |  | 없음(패턴 밖) |
| `/categories/7/items/1/name` | [6,12) | (전체얼굴) | 적용 범위, 부위 후보 |  | paren |
| `/categories/7/items/2/name` | [0,8) | CO2 프락셔널 | 장비/기법명 후보, 영문·숫자 혼합 | 'CO2' 형태소 분절 시 SL+SN 으로 나뉨(K). | 없음(패턴 밖) |
| `/categories/7/items/2/name` | [9,15) | (전체얼굴) | 적용 범위, 부위 후보 |  | paren |
| `/categories/7/items/3/name` | [0,4) | 제네시스 | 장비/기법명 후보 |  | 없음(패턴 밖) |
| `/categories/7/items/3/name` | [5,11) | (전체얼굴) | 적용 범위, 부위 후보 |  | paren |
| `/categories/7/items/4/name` | [0,3) | 엑셀V | 장비명 후보, 영한 혼합 |  | 없음(패턴 밖) |
| `/categories/7/items/4/name` | [4,11) | (혈관/홍조) | 고민/적응증 후보, '/' 연결 |  | paren |
| `/categories/7/items/5/name` | [0,3) | IPL | 장비/기법명 후보, 영문 약어 |  | 없음(패턴 밖) |
| `/categories/7/items/5/name` | [4,10) | (전체얼굴) | 적용 범위, 부위 후보 |  | paren |
| `/categories/7/items/6/name` | [0,6) | 레이저 제모 | 시술명 후보, 목적 |  | 없음(패턴 밖) |
| `/categories/7/items/6/name` | [7,13) | (겨드랑이) | 부위 후보 |  | paren |
| `/categories/7/items/7/name` | [0,6) | 레이저 제모 | 시술명 후보, 목적 |  | 없음(패턴 밖) |
| `/categories/7/items/7/name` | [7,11) | (전신) | 적용 범위, 부위 후보 |  | paren |
| `/categories/7/items/8/name` | [0,4) | 점 제거 | 시술명 후보, 목적 |  | 없음(패턴 밖) |
| `/categories/7/items/8/name` | [5,10) | (1개당) | 가격 기준, 분모, 수량·단위 | '당'. | paren |
| `/categories/7/items/9/name` | [0,5) | 문신 제거 | 시술명 후보, 목적 |  | 없음(패턴 밖) |
| `/categories/7/items/9/name` | [6,13) | (10cm2) | 수량·단위, 면적 | 'cm2' — 제곱 표기를 원문대로. | paren |

### 자동 후보 (정규식 일치분뿐 — 의미 해석 아님)

| Pointer | 구간 | 패턴 | 일치 구절 | 검토 |
|---|---|---|---|---|
| `/categories/7/items/0/name` | [5,11) | paren | (전체얼굴) | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/7/items/0/name` | [6,10) | kw | 전체얼굴 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/7/items/0/unit` | [0,2) | num_unit | 1회 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/7/items/1/name` | [6,12) | paren | (전체얼굴) | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/7/items/1/name` | [7,11) | kw | 전체얼굴 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/7/items/1/unit` | [0,2) | num_unit | 1회 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/7/items/2/name` | [9,15) | paren | (전체얼굴) | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/7/items/2/name` | [10,14) | kw | 전체얼굴 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/7/items/2/unit` | [0,2) | num_unit | 1회 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/7/items/3/name` | [5,11) | paren | (전체얼굴) | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/7/items/3/name` | [6,10) | kw | 전체얼굴 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/7/items/3/unit` | [0,2) | num_unit | 1회 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/7/items/4/name` | [4,11) | paren | (혈관/홍조) | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/7/items/4/name` | [5,10) | slash | 혈관/홍조 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/7/items/4/unit` | [0,2) | num_unit | 1회 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/7/items/5/name` | [4,10) | paren | (전체얼굴) | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/7/items/5/name` | [5,9) | kw | 전체얼굴 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/7/items/5/unit` | [0,2) | num_unit | 1회 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/7/items/6/name` | [7,13) | paren | (겨드랑이) | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/7/items/6/unit` | [0,2) | num_unit | 1회 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/7/items/7/name` | [7,11) | paren | (전신) | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/7/items/7/name` | [8,10) | kw | 전신 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/7/items/7/unit` | [0,2) | num_unit | 1회 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/7/items/8/name` | [5,10) | paren | (1개당) | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/7/items/8/name` | [6,8) | num_unit | 1개 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/7/items/8/name` | [7,9) | kw | 개당 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/7/items/8/unit` | [0,2) | num_unit | 1개 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/7/items/9/name` | [6,13) | paren | (10cm2) | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/7/items/9/name` | [7,12) | num_unit | 10cm2 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/7/items/9/unit` | [0,2) | num_unit | 1회 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |

### 형태소 (Kiwi 원시 결과 — 도메인 정답 아님. `form/tag[start,end)`)

| Pointer | 원문 값 | 토큰 |
|---|---|---|
| `/categories/7/id` | M8 | 제외: 카테고리 ID(Mn) — 식별자 |
| `/categories/7/name` | 레이저 | 레이저/NNG[0,3) |
| `/categories/7/items/0/name` | 피코토닝 (전체얼굴) | 피코토닝/NNP[0,4) (/SSO[5,6) 전체/NNG[6,8) 얼굴/NNG[8,10) )/SSC[10,11) |
| `/categories/7/items/0/unit` | 1회 | 1/SN[0,1) 회/NNB[1,2) |
| `/categories/7/items/1/name` | 피코프락셀 (전체얼굴) | 피코프락셀/NNP[0,5) (/SSO[6,7) 전체/NNG[7,9) 얼굴/NNG[9,11) )/SSC[11,12) |
| `/categories/7/items/1/unit` | 1회 | 1/SN[0,1) 회/NNB[1,2) |
| `/categories/7/items/2/name` | CO2 프락셔널 (전체얼굴) | CO/SL[0,2) 2/SN[2,3) 프락셔널/NNP[4,8) (/SSO[9,10) 전체/NNG[10,12) 얼굴/NNG[12,14) )/SSC[14,15) |
| `/categories/7/items/2/unit` | 1회 | 1/SN[0,1) 회/NNB[1,2) |
| `/categories/7/items/3/name` | 제네시스 (전체얼굴) | 제네시스/NNP[0,4) (/SSO[5,6) 전체/NNG[6,8) 얼굴/NNG[8,10) )/SSC[10,11) |
| `/categories/7/items/3/unit` | 1회 | 1/SN[0,1) 회/NNB[1,2) |
| `/categories/7/items/4/name` | 엑셀V (혈관/홍조) | 엑셀/NNP[0,2) V/SL[2,3) (/SSO[4,5) 혈관/NNG[5,7) //SP[7,8) 홍조/NNG[8,10) )/SSC[10,11) |
| `/categories/7/items/4/unit` | 1회 | 1/SN[0,1) 회/NNB[1,2) |
| `/categories/7/items/5/name` | IPL (전체얼굴) | IPL/SL[0,3) (/SSO[4,5) 전체/NNG[5,7) 얼굴/NNG[7,9) )/SSC[9,10) |
| `/categories/7/items/5/unit` | 1회 | 1/SN[0,1) 회/NNB[1,2) |
| `/categories/7/items/6/name` | 레이저 제모 (겨드랑이) | 레이저/NNG[0,3) 제모/NNG[4,6) (/SSO[7,8) 겨드랑이/NNG[8,12) )/SSC[12,13) |
| `/categories/7/items/6/unit` | 1회 | 1/SN[0,1) 회/NNB[1,2) |
| `/categories/7/items/7/name` | 레이저 제모 (전신) | 레이저/NNG[0,3) 제모/NNP[4,6) (/SSO[7,8) 전신/NNG[8,10) )/SSC[10,11) |
| `/categories/7/items/7/unit` | 1회 | 1/SN[0,1) 회/NNB[1,2) |
| `/categories/7/items/8/name` | 점 제거 (1개당) | 점/NNG[0,1) 제거/NNG[2,4) (/SSO[5,6) 1/SN[6,7) 개/NNB[7,8) 당/NNG[8,9) )/SSC[9,10) |
| `/categories/7/items/8/unit` | 1개 | 1/SN[0,1) 개/NNB[1,2) |
| `/categories/7/items/9/name` | 문신 제거 (10cm2) | 문신/NNG[0,2) 제거/NNG[3,5) (/SSO[6,7) 10/SN[7,9) cm/SL[9,11) 2/SN[11,12) )/SSC[12,13) |
| `/categories/7/items/9/unit` | 1회 | 1/SN[0,1) 회/NNB[1,2) |

알려진 오분절 출현(교정 안 함):

- `/categories/7/items/2/name` [0,3) `CO2` → [['CO', 'SL'], ['2', 'SN']] — 제품명·단위(CO2·cm2·FLX 등) 영숫자 결합이 SL/SN 으로 나뉜다. 이름 단위 검색은 원문 구간으로 해야 한다.
- `/categories/7/items/9/name` [7,12) `10cm2` → [['10', 'SN'], ['cm', 'SL'], ['2', 'SN']] — 제품명·단위(CO2·cm2·FLX 등) 영숫자 결합이 SL/SN 으로 나뉜다. 이름 단위 검색은 원문 구간으로 해야 한다.

### 미결 (이 구획)

| ID | 상태 | Pointer | 내용 |
|---|---|---|---|
| I-S08-1 | I | `/categories/7/items/9/name`, `/categories/7/items/9/unit` | '문신 제거 (10cm2)' 면적 기준과 unit '1회' 가 함께 있다. 10cm2 의 역할(상한·단위면적) 원문 없음 — 후속 확인 후보. |
| B-S08-1 | B | `/categories/7/items/4/name` | '엑셀V' 의 적용 부위·범위가 없다(고민만 있음). |
| B-S08-2 | B | `/categories/7/items/6/name`, `/categories/7/items/7/name` | 제모 회차·패키지 구성 없음. |
| K-S08-1 | K | `/categories/7/items/2/name`, `/categories/7/items/9/name` | 'CO2'·'10cm2' 가 SL/SN 으로 쪼개짐 — 기본 결과 보존, 출현 기록. |
