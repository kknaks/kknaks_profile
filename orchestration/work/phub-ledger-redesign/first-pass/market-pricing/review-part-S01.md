# S01 — M1 보톡스 (10항목)

[← review.md](review.md) · 소유 말단 52 · 직접 읽기 ○ · 마지막 읽은 Pointer `/categories/0/items/9/high`

## S01

### 상위 문맥 (S00 소유, 공동 참조)

- `/currency` = `KRW` · `/updated` = `2026-07-26` · `/note` = `한국 시장 참고 가격 범위. 클리닉/지역/의사에 따라 상이. 정가 아닌 시장 범위.`

### 원문 값 — 카테고리

| Pointer | 원본 컬럼명 | 자료형 | 원문 값 |
|---|---|---|---|
| `/categories/0/id` | `id` | string | `M1` |
| `/categories/0/name` | `name` | string | `보톡스` |
| `/categories/0/items` | `items` | array[10] of object | (아래 표) |

### 원문 값 — `items` (원본 순서, 각 값의 Pointer = 항목 Pointer + `/` + 컬럼명)

자료형: `name`·`unit` string, `low`·`mid`·`high` integer.

| 항목 Pointer | `name` | `unit` | `low` | `mid` | `high` |
|---|---|---|---|---|---|
| `/categories/0/items/0` | 이마 주름 (수입) | 1회 | 50000 | 100000 | 200000 |
| `/categories/0/items/1` | 이마 주름 (국산) | 1회 | 30000 | 60000 | 100000 |
| `/categories/0/items/2` | 미간 주름 (수입) | 1회 | 40000 | 80000 | 150000 |
| `/categories/0/items/3` | 미간 주름 (국산) | 1회 | 20000 | 50000 | 80000 |
| `/categories/0/items/4` | 눈가 주름 (수입) | 1회 | 40000 | 80000 | 150000 |
| `/categories/0/items/5` | 눈가 주름 (국산) | 1회 | 20000 | 50000 | 80000 |
| `/categories/0/items/6` | 사각턱 (수입) | 1회 | 80000 | 150000 | 300000 |
| `/categories/0/items/7` | 사각턱 (국산) | 1회 | 50000 | 100000 | 200000 |
| `/categories/0/items/8` | 승모근 | 1회 | 100000 | 200000 | 400000 |
| `/categories/0/items/9` | 목주름 (네페르티티) | 1회 | 150000 | 250000 | 400000 |

### 잠정 관찰 (원문 아님 — 근거 Pointer 와 상태)

| 근거 Pointer | 관찰 | 상태 |
|---|---|---|
| `/categories/0/name` | 카테고리 이름 '보톡스'. 항목 name 에는 시술명(보톡스)이 반복되지 않고 부위·고민 표현만 있음 — 항목 정체를 이해하려면 카테고리 이름이 상위 문맥으로 필요. | P |
| `/categories/0/items/0/name` | '<부위> 주름 (수입\|국산)' 형태가 이마·미간·눈가 3부위 × 수입/국산 2종(items/0~5), '사각턱 (수입\|국산)'(items/6~7). 괄호 안 '수입'·'국산'은 제품 원산지 수식으로 보이며 제품명은 없음. | P |
| `/categories/0/items/8/name` | '승모근' — 수입/국산 표기가 없음. 같은 카테고리의 다른 항목과 표기 형식이 다름. | P |
| `/categories/0/items/9/name` | '목주름 (네페르티티)' — 괄호 안이 원산지가 아니라 다른 이름(기법/별칭 후보). 같은 카테고리 안에서 괄호의 역할이 다름. | P |
| `/categories/0/items/0/unit` | 10항목 모두 unit '1회'. 사용 용량(유닛 수)·제품명은 없음 — 같은 '1회' 라도 부위별 용량이 다를 수 있으나 원문에 없음. | B |
| `/categories/0/items/0/low` | 10항목 모두 low < mid < high (기계 확인과 일치). 수입 항목이 같은 부위의 국산 항목보다 세 값 모두 높음(이마·미간·눈가·사각턱). | P |

### 직접 읽기로 수집한 표현 (문자열 값 코드포인트 구간 [start,end))

| Pointer | 구간 | 원문 구절 | 탐색 관점(확정 분류 아님) | 메모 | 자동 패턴 동일 구간 |
|---|---|---|---|---|---|
| `/categories/0/items/0/name` | [0,5) | 이마 주름 | 부위 후보, 고민 후보 | 부위(이마)+고민(주름) 결합. 분리는 후속. | 없음(패턴 밖) |
| `/categories/0/items/0/name` | [6,10) | (수입) | 원산지 수식 |  | paren |
| `/categories/0/items/1/name` | [0,5) | 이마 주름 | 부위 후보, 고민 후보 |  | 없음(패턴 밖) |
| `/categories/0/items/1/name` | [6,10) | (국산) | 원산지 수식 |  | paren |
| `/categories/0/items/2/name` | [0,5) | 미간 주름 | 부위 후보, 고민 후보 |  | 없음(패턴 밖) |
| `/categories/0/items/2/name` | [6,10) | (수입) | 원산지 수식 |  | paren |
| `/categories/0/items/3/name` | [0,5) | 미간 주름 | 부위 후보, 고민 후보 |  | 없음(패턴 밖) |
| `/categories/0/items/3/name` | [6,10) | (국산) | 원산지 수식 |  | paren |
| `/categories/0/items/4/name` | [0,5) | 눈가 주름 | 부위 후보, 고민 후보 |  | 없음(패턴 밖) |
| `/categories/0/items/4/name` | [6,10) | (수입) | 원산지 수식 |  | paren |
| `/categories/0/items/5/name` | [0,5) | 눈가 주름 | 부위 후보, 고민 후보 |  | 없음(패턴 밖) |
| `/categories/0/items/5/name` | [6,10) | (국산) | 원산지 수식 |  | paren |
| `/categories/0/items/6/name` | [0,3) | 사각턱 | 부위 후보, 고민 후보 | 부위인지 윤곽 고민인지 원문만으로 구분 불가. | 없음(패턴 밖) |
| `/categories/0/items/6/name` | [4,8) | (수입) | 원산지 수식 |  | paren |
| `/categories/0/items/7/name` | [0,3) | 사각턱 | 부위 후보, 고민 후보 |  | 없음(패턴 밖) |
| `/categories/0/items/7/name` | [4,8) | (국산) | 원산지 수식 |  | paren |
| `/categories/0/items/8/name` | [0,3) | 승모근 | 부위 후보 | 근육 이름. 원산지 수식 없음. | 없음(패턴 밖) |
| `/categories/0/items/9/name` | [0,3) | 목주름 | 부위 후보, 고민 후보 | 띄어쓰기 없이 '목주름' — 다른 항목('이마 주름')과 띄어쓰기 다름. | 없음(패턴 밖) |
| `/categories/0/items/9/name` | [4,11) | (네페르티티) | 괄호 부가, 기법/별칭 후보 | 원산지가 아닌 이름. 무엇의 이름인지 원문에 없음. | paren |

### 자동 후보 (정규식 일치분뿐 — 의미 해석 아님)

| Pointer | 구간 | 패턴 | 일치 구절 | 검토 |
|---|---|---|---|---|
| `/categories/0/items/0/name` | [6,10) | paren | (수입) | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/0/items/0/name` | [7,9) | kw | 수입 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/0/items/0/unit` | [0,2) | num_unit | 1회 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/0/items/1/name` | [6,10) | paren | (국산) | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/0/items/1/name` | [7,9) | kw | 국산 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/0/items/1/unit` | [0,2) | num_unit | 1회 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/0/items/2/name` | [6,10) | paren | (수입) | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/0/items/2/name` | [7,9) | kw | 수입 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/0/items/2/unit` | [0,2) | num_unit | 1회 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/0/items/3/name` | [6,10) | paren | (국산) | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/0/items/3/name` | [7,9) | kw | 국산 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/0/items/3/unit` | [0,2) | num_unit | 1회 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/0/items/4/name` | [6,10) | paren | (수입) | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/0/items/4/name` | [7,9) | kw | 수입 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/0/items/4/unit` | [0,2) | num_unit | 1회 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/0/items/5/name` | [6,10) | paren | (국산) | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/0/items/5/name` | [7,9) | kw | 국산 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/0/items/5/unit` | [0,2) | num_unit | 1회 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/0/items/6/name` | [4,8) | paren | (수입) | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/0/items/6/name` | [5,7) | kw | 수입 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/0/items/6/unit` | [0,2) | num_unit | 1회 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/0/items/7/name` | [4,8) | paren | (국산) | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/0/items/7/name` | [5,7) | kw | 국산 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/0/items/7/unit` | [0,2) | num_unit | 1회 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/0/items/8/unit` | [0,2) | num_unit | 1회 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/0/items/9/name` | [4,11) | paren | (네페르티티) | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/0/items/9/unit` | [0,2) | num_unit | 1회 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |

### 형태소 (Kiwi 원시 결과 — 도메인 정답 아님. `form/tag[start,end)`)

| Pointer | 원문 값 | 토큰 |
|---|---|---|
| `/categories/0/id` | M1 | 제외: 카테고리 ID(Mn) — 식별자 |
| `/categories/0/name` | 보톡스 | 보톡스/NNG[0,3) |
| `/categories/0/items/0/name` | 이마 주름 (수입) | 이마/NNG[0,2) 주름/NNG[3,5) (/SSO[6,7) 수입/NNG[7,9) )/SSC[9,10) |
| `/categories/0/items/0/unit` | 1회 | 1/SN[0,1) 회/NNB[1,2) |
| `/categories/0/items/1/name` | 이마 주름 (국산) | 이마/NNG[0,2) 주름/NNG[3,5) (/SSO[6,7) 국산/NNG[7,9) )/SSC[9,10) |
| `/categories/0/items/1/unit` | 1회 | 1/SN[0,1) 회/NNB[1,2) |
| `/categories/0/items/2/name` | 미간 주름 (수입) | 미간/NNG[0,2) 주름/NNG[3,5) (/SSO[6,7) 수입/NNG[7,9) )/SSC[9,10) |
| `/categories/0/items/2/unit` | 1회 | 1/SN[0,1) 회/NNB[1,2) |
| `/categories/0/items/3/name` | 미간 주름 (국산) | 미간/NNG[0,2) 주름/NNG[3,5) (/SSO[6,7) 국산/NNG[7,9) )/SSC[9,10) |
| `/categories/0/items/3/unit` | 1회 | 1/SN[0,1) 회/NNB[1,2) |
| `/categories/0/items/4/name` | 눈가 주름 (수입) | 눈가/NNG[0,2) 주름/NNG[3,5) (/SSO[6,7) 수입/NNG[7,9) )/SSC[9,10) |
| `/categories/0/items/4/unit` | 1회 | 1/SN[0,1) 회/NNB[1,2) |
| `/categories/0/items/5/name` | 눈가 주름 (국산) | 눈가/NNG[0,2) 주름/NNG[3,5) (/SSO[6,7) 국산/NNG[7,9) )/SSC[9,10) |
| `/categories/0/items/5/unit` | 1회 | 1/SN[0,1) 회/NNB[1,2) |
| `/categories/0/items/6/name` | 사각턱 (수입) | 사각/NNG[0,2) 턱/NNG[2,3) (/SSO[4,5) 수입/NNG[5,7) )/SSC[7,8) |
| `/categories/0/items/6/unit` | 1회 | 1/SN[0,1) 회/NNB[1,2) |
| `/categories/0/items/7/name` | 사각턱 (국산) | 사각/NNG[0,2) 턱/NNG[2,3) (/SSO[4,5) 국산/NNG[5,7) )/SSC[7,8) |
| `/categories/0/items/7/unit` | 1회 | 1/SN[0,1) 회/NNB[1,2) |
| `/categories/0/items/8/name` | 승모근 | 승모근/NNG[0,3) |
| `/categories/0/items/8/unit` | 1회 | 1/SN[0,1) 회/NNB[1,2) |
| `/categories/0/items/9/name` | 목주름 (네페르티티) | 목/NNG[0,1) 주름/NNG[1,3) (/SSO[4,5) 네페르티티/NNP[5,10) )/SSC[10,11) |
| `/categories/0/items/9/unit` | 1회 | 1/SN[0,1) 회/NNB[1,2) |

### 미결 (이 구획)

| ID | 상태 | Pointer | 내용 |
|---|---|---|---|
| B-S01-1 | B | `/categories/0/items/0/unit` | 보톡스 '1회' 가격의 용량(유닛)·제품명이 없다(10항목). 용량 기준 가격 비교가 제한된다. |
| P-S01-1 | P | `/categories/0/items/9/name` | '(네페르티티)' 의 역할(기법명·별칭)은 잠정. 같은 카테고리의 괄호가 원산지·별칭 두 역할로 쓰인다. |
