# S07 — M7 실리프팅 (7항목)

[← review.md](review.md) · 소유 말단 37 · 직접 읽기 ○ · 마지막 읽은 Pointer `/categories/6/items/6/high`

## S07

### 상위 문맥 (S00 소유, 공동 참조)

- `/currency` = `KRW` · `/updated` = `2026-07-26` · `/note` = `한국 시장 참고 가격 범위. 클리닉/지역/의사에 따라 상이. 정가 아닌 시장 범위.`

### 원문 값 — 카테고리

| Pointer | 원본 컬럼명 | 자료형 | 원문 값 |
|---|---|---|---|
| `/categories/6/id` | `id` | string | `M7` |
| `/categories/6/name` | `name` | string | `실리프팅` |
| `/categories/6/items` | `items` | array[7] of object | (아래 표) |

### 원문 값 — `items` (원본 순서, 각 값의 Pointer = 항목 Pointer + `/` + 컬럼명)

자료형: `name`·`unit` string, `low`·`mid`·`high` integer.

| 항목 Pointer | `name` | `unit` | `low` | `mid` | `high` |
|---|---|---|---|---|---|
| `/categories/6/items/0` | PDO 실 (10줄 기준) | 10줄 | 200000 | 400000 | 700000 |
| `/categories/6/items/1` | 코그 실 리프팅 (양쪽 8줄) | 8줄 | 400000 | 800000 | 1500000 |
| `/categories/6/items/2` | 민트 리프팅 (양쪽) | 1회 | 500000 | 1000000 | 1800000 |
| `/categories/6/items/3` | 몰딩 실 (V라인) | 1회 | 300000 | 600000 | 1000000 |
| `/categories/6/items/4` | 코 실리프팅 | 1회 | 150000 | 300000 | 600000 |
| `/categories/6/items/5` | 풀페이스 실리프팅 (20줄 이상) | 1회 | 800000 | 1500000 | 3000000 |
| `/categories/6/items/6` | 목 실리프팅 | 1회 | 500000 | 900000 | 1500000 |

### 잠정 관찰 (원문 아님 — 근거 Pointer 와 상태)

| 근거 Pointer | 관찰 | 상태 |
|---|---|---|
| `/categories/6/items/0/name` | 'PDO 실 (10줄 기준)' unit '10줄' — '기준' 은 가격이 10줄을 기준으로 한다는 표현. 줄 수가 달라질 때의 가격은 원문에 없음. | P |
| `/categories/6/items/1/name` | '코그 실 리프팅 (양쪽 8줄)' unit '8줄' — 괄호에 양측성('양쪽')과 수량이 함께. unit 에는 '양쪽' 이 빠짐(8줄이 양쪽 합계인지 한쪽인지 원문 명시는 name 의 '양쪽 8줄' 뿐). | P |
| `/categories/6/items/2/name` | '민트 리프팅 (양쪽)' unit '1회' — 줄 수 없음. | B |
| `/categories/6/items/3/name` | '몰딩 실 (V라인)' — 괄호가 목표 윤곽/부위('V라인'). 영문+한글 혼합. | P |
| `/categories/6/items/5/name` | '풀페이스 실리프팅 (20줄 이상)' unit '1회' — '이상' 은 하한만 있는 범위. 가격이 20줄 이상 전체에 같은지 원문에 없음. name 의 수량 기준(줄)과 unit(회)이 다름. | P |
| `/categories/6/items/4/name` | '코 실리프팅'·'목 실리프팅' — 부위가 앞에, 괄호 없음. '실리프팅'(붙임)·'실 리프팅'(띄움, items/1) 띄어쓰기 혼재. | P |
| `/categories/6/items/0/low` | 7항목 모두 low < mid < high. | P |

### 직접 읽기로 수집한 표현 (문자열 값 코드포인트 구간 [start,end))

| Pointer | 구간 | 원문 구절 | 탐색 관점(확정 분류 아님) | 메모 | 자동 패턴 동일 구간 |
|---|---|---|---|---|---|
| `/categories/6/items/0/name` | [0,5) | PDO 실 | 재질 후보, 시술명 후보 | 'PDO' 영문 약어. | 없음(패턴 밖) |
| `/categories/6/items/0/name` | [6,14) | (10줄 기준) | 수량·단위, 가격 기준 | '기준'. | paren |
| `/categories/6/items/1/name` | [0,8) | 코그 실 리프팅 | 시술명 후보, 실 형태 후보 | '코그' — 실 형태 수식 후보. '코'(부위)와 첫 글자 같음 — 부분일치 오탐 위험. | 없음(패턴 밖) |
| `/categories/6/items/1/name` | [9,16) | (양쪽 8줄) | 양측성, 수량·단위 |  | paren |
| `/categories/6/items/1/name` | [10,12) | 양쪽 | 양측성 |  | kw |
| `/categories/6/items/2/name` | [0,6) | 민트 리프팅 | 시술명/제품명 후보 |  | 없음(패턴 밖) |
| `/categories/6/items/2/name` | [7,11) | (양쪽) | 양측성 |  | paren |
| `/categories/6/items/3/name` | [0,4) | 몰딩 실 | 실 형태 후보, 시술명 후보 |  | 없음(패턴 밖) |
| `/categories/6/items/3/name` | [5,10) | (V라인) | 목표 윤곽/부위 후보, 영한 혼합 |  | paren |
| `/categories/6/items/4/name` | [0,6) | 코 실리프팅 | 부위 후보, 시술명 후보 |  | 없음(패턴 밖) |
| `/categories/6/items/5/name` | [0,9) | 풀페이스 실리프팅 | 적용 범위, 시술명 후보 |  | 없음(패턴 밖) |
| `/categories/6/items/5/name` | [10,18) | (20줄 이상) | 범위, 수량·단위 | '이상' — 하한. | paren |
| `/categories/6/items/6/name` | [0,6) | 목 실리프팅 | 부위 후보, 시술명 후보 |  | 없음(패턴 밖) |

### 자동 후보 (정규식 일치분뿐 — 의미 해석 아님)

| Pointer | 구간 | 패턴 | 일치 구절 | 검토 |
|---|---|---|---|---|
| `/categories/6/items/0/name` | [6,14) | paren | (10줄 기준) | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/6/items/0/name` | [7,10) | num_unit | 10줄 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/6/items/0/name` | [11,13) | kw | 기준 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/6/items/0/unit` | [0,3) | num_unit | 10줄 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/6/items/1/name` | [9,16) | paren | (양쪽 8줄) | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/6/items/1/name` | [13,15) | num_unit | 8줄 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/6/items/1/name` | [10,12) | kw | 양쪽 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/6/items/1/unit` | [0,2) | num_unit | 8줄 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/6/items/2/name` | [7,11) | paren | (양쪽) | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/6/items/2/name` | [8,10) | kw | 양쪽 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/6/items/2/unit` | [0,2) | num_unit | 1회 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/6/items/3/name` | [5,10) | paren | (V라인) | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/6/items/3/unit` | [0,2) | num_unit | 1회 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/6/items/4/unit` | [0,2) | num_unit | 1회 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/6/items/5/name` | [10,18) | paren | (20줄 이상) | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/6/items/5/name` | [11,14) | num_unit | 20줄 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/6/items/5/name` | [0,4) | kw | 풀페이스 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/6/items/5/name` | [15,17) | kw | 이상 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/6/items/5/unit` | [0,2) | num_unit | 1회 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/6/items/6/unit` | [0,2) | num_unit | 1회 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |

### 형태소 (Kiwi 원시 결과 — 도메인 정답 아님. `form/tag[start,end)`)

| Pointer | 원문 값 | 토큰 |
|---|---|---|
| `/categories/6/id` | M7 | 제외: 카테고리 ID(Mn) — 식별자 |
| `/categories/6/name` | 실리프팅 | 실/NNG[0,1) 리프팅/NNG[1,4) |
| `/categories/6/items/0/name` | PDO 실 (10줄 기준) | PDO/SL[0,3) 실/NNG[4,5) (/SSO[6,7) 10/SN[7,9) 줄/NNG[9,10) 기준/NNG[11,13) )/SSC[13,14) |
| `/categories/6/items/0/unit` | 10줄 | 10/SN[0,2) 줄/NNG[2,3) |
| `/categories/6/items/1/name` | 코그 실 리프팅 (양쪽 8줄) | 코그/NNP[0,2) 실/NNG[3,4) 리프팅/NNG[5,8) (/SSO[9,10) 양쪽/NNG[10,12) 8/SN[13,14) 줄/NNG[14,15) )/SSC[15,16) |
| `/categories/6/items/1/unit` | 8줄 | 8/SN[0,1) 줄/NNG[1,2) |
| `/categories/6/items/2/name` | 민트 리프팅 (양쪽) | 민트/NNG[0,2) 리프/NNP[3,5) 팅/NNP[5,6) (/SSO[7,8) 양/MM[8,9) 쪽/NNB[9,10) )/SSC[10,11) |
| `/categories/6/items/2/unit` | 1회 | 1/SN[0,1) 회/NNB[1,2) |
| `/categories/6/items/3/name` | 몰딩 실 (V라인) | 몰/NNG[0,1) 딩/MAG[1,2) 실/NNG[3,4) (/SSO[5,6) V/SL[6,7) 라인/NNG[7,9) )/SSC[9,10) |
| `/categories/6/items/3/unit` | 1회 | 1/SN[0,1) 회/NNB[1,2) |
| `/categories/6/items/4/name` | 코 실리프팅 | 코/NNG[0,1) 실/NNG[2,3) 리프팅/NNG[3,6) |
| `/categories/6/items/4/unit` | 1회 | 1/SN[0,1) 회/NNB[1,2) |
| `/categories/6/items/5/name` | 풀페이스 실리프팅 (20줄 이상) | 풀페이스/NNG[0,4) 실리프팅/NNG[5,9) (/SSO[10,11) 20/SN[11,13) 줄/NNG[13,14) 이상/NNG[15,17) )/SSC[17,18) |
| `/categories/6/items/5/unit` | 1회 | 1/SN[0,1) 회/NNB[1,2) |
| `/categories/6/items/6/name` | 목 실리프팅 | 목/NNG[0,1) 실/NNG[2,3) 리프팅/NNG[3,6) |
| `/categories/6/items/6/unit` | 1회 | 1/SN[0,1) 회/NNB[1,2) |

알려진 오분절 출현(교정 안 함):

- `/categories/6/items/2/name` [3,6) `리프팅` → [['리프', 'NNP'], ['팅', 'NNP']] — 다른 출현에서는 '리프팅/NNG' 한 토큰인데 이 출현만 둘로 쪼개짐 — 같은 말의 분석 불일치.
- `/categories/6/items/2/name` [8,10) `양쪽` → [['양', 'MM'], ['쪽', 'NNB']] — 다른 출현에서는 '양쪽/NNG' 인데 이 출현만 관형사+의존명사. 양측성 표현 토큰 검색 시 누락 위험.
- `/categories/6/items/3/name` [0,2) `몰딩` → [['몰', 'NNG'], ['딩', 'MAG']] — '딩'이 부사(MAG)로 태깅 — 부사(수식) 수집 시 오탐.

### 미결 (이 구획)

| ID | 상태 | Pointer | 내용 |
|---|---|---|---|
| B-S07-1 | B | `/categories/6/items/0/name` | '10줄 기준' 외 줄 수의 가격, 실 종류별(PDO 외) 차이가 없다. |
| B-S07-2 | B | `/categories/6/items/2/name`, `/categories/6/items/3/name`, `/categories/6/items/4/name`, `/categories/6/items/6/name` | unit '1회' 항목들의 줄 수가 없다. |
| I-S07-1 | I | `/categories/6/items/5/name`, `/categories/6/items/5/unit` | name 은 줄 수 기준('20줄 이상'), unit 은 '1회' — 가격 기준 표기가 항목 안에서 다르다. 원본 보존, 후속 확인 후보. |
