# S06 — M6 지방이식 (7항목)

[← review.md](review.md) · 소유 말단 37 · 직접 읽기 ○ · 마지막 읽은 Pointer `/categories/5/items/6/high`

## S06

### 상위 문맥 (S00 소유, 공동 참조)

- `/currency` = `KRW` · `/updated` = `2026-07-26` · `/note` = `한국 시장 참고 가격 범위. 클리닉/지역/의사에 따라 상이. 정가 아닌 시장 범위.`

### 원문 값 — 카테고리

| Pointer | 원본 컬럼명 | 자료형 | 원문 값 |
|---|---|---|---|
| `/categories/5/id` | `id` | string | `M6` |
| `/categories/5/name` | `name` | string | `지방이식` |
| `/categories/5/items` | `items` | array[7] of object | (아래 표) |

### 원문 값 — `items` (원본 순서, 각 값의 Pointer = 항목 Pointer + `/` + 컬럼명)

자료형: `name`·`unit` string, `low`·`mid`·`high` integer.

| 항목 Pointer | `name` | `unit` | `low` | `mid` | `high` |
|---|---|---|---|---|---|
| `/categories/5/items/0` | 이마 지방이식 | 1회 | 1000000 | 2000000 | 3500000 |
| `/categories/5/items/1` | 볼 지방이식 | 1회 | 800000 | 1500000 | 2500000 |
| `/categories/5/items/2` | 눈밑 지방이식 | 1회 | 800000 | 1500000 | 2500000 |
| `/categories/5/items/3` | 풀페이스 지방이식 | 1회 | 2000000 | 3500000 | 6000000 |
| `/categories/5/items/4` | 관자놀이 지방이식 | 1회 | 600000 | 1200000 | 2000000 |
| `/categories/5/items/5` | 턱 끝 지방이식 | 1회 | 600000 | 1000000 | 1800000 |
| `/categories/5/items/6` | 나노 지방이식 (전체얼굴) | 1회 | 2500000 | 4000000 | 7000000 |

### 잠정 관찰 (원문 아님 — 근거 Pointer 와 상태)

| 근거 Pointer | 관찰 | 상태 |
|---|---|---|
| `/categories/5/items/0/name` | items/0~5 는 '<부위> 지방이식' 형태로 부위가 괄호 밖 앞에 옴 — 다른 카테고리(괄호 안 부위)와 어순이 다름. | P |
| `/categories/5/items/3/name` | '풀페이스 지방이식' 과 '나노 지방이식 (전체얼굴)' — 같은 카테고리 안에서 얼굴 전체 표현이 '풀페이스'·'전체얼굴' 두 가지. 같은 범위인지 원문만으로 확정 불가. | P |
| `/categories/5/items/6/name` | '나노' 는 지방이식 방식(입자 크기) 수식 후보. 뜻은 원문에 없음. | B |
| `/categories/5/items/0/unit` | 7항목 모두 '1회'. 지방 채취·주입량(cc)은 없음. | B |
| `/categories/5/items/0/low` | 7항목 모두 low < mid < high. 볼·눈밑 두 항목은 세 값이 같음(800000/1500000/2500000). | P |

### 직접 읽기로 수집한 표현 (문자열 값 코드포인트 구간 [start,end))

| Pointer | 구간 | 원문 구절 | 탐색 관점(확정 분류 아님) | 메모 | 자동 패턴 동일 구간 |
|---|---|---|---|---|---|
| `/categories/5/items/0/name` | [0,2) | 이마 | 부위 후보 |  | 없음(패턴 밖) |
| `/categories/5/items/1/name` | [0,1) | 볼 | 부위 후보 |  | 없음(패턴 밖) |
| `/categories/5/items/2/name` | [0,2) | 눈밑 | 부위 후보 |  | 없음(패턴 밖) |
| `/categories/5/items/3/name` | [0,4) | 풀페이스 | 적용 범위, 부위 후보 |  | kw |
| `/categories/5/items/4/name` | [0,4) | 관자놀이 | 부위 후보 |  | 없음(패턴 밖) |
| `/categories/5/items/5/name` | [0,3) | 턱 끝 | 부위 후보, 위치 수식 |  | 없음(패턴 밖) |
| `/categories/5/items/6/name` | [0,7) | 나노 지방이식 | 기법 수식, 시술명 후보 | '나노' — 크기 관련 수식 후보. | 없음(패턴 밖) |
| `/categories/5/items/6/name` | [8,14) | (전체얼굴) | 적용 범위, 부위 후보 |  | paren |

### 자동 후보 (정규식 일치분뿐 — 의미 해석 아님)

| Pointer | 구간 | 패턴 | 일치 구절 | 검토 |
|---|---|---|---|---|
| `/categories/5/items/0/unit` | [0,2) | num_unit | 1회 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/5/items/1/unit` | [0,2) | num_unit | 1회 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/5/items/2/unit` | [0,2) | num_unit | 1회 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/5/items/3/name` | [0,4) | kw | 풀페이스 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/5/items/3/unit` | [0,2) | num_unit | 1회 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/5/items/4/unit` | [0,2) | num_unit | 1회 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/5/items/5/unit` | [0,2) | num_unit | 1회 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/5/items/6/name` | [8,14) | paren | (전체얼굴) | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/5/items/6/name` | [0,2) | kw | 나노 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/5/items/6/name` | [9,13) | kw | 전체얼굴 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/5/items/6/unit` | [0,2) | num_unit | 1회 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |

### 형태소 (Kiwi 원시 결과 — 도메인 정답 아님. `form/tag[start,end)`)

| Pointer | 원문 값 | 토큰 |
|---|---|---|
| `/categories/5/id` | M6 | 제외: 카테고리 ID(Mn) — 식별자 |
| `/categories/5/name` | 지방이식 | 지방/NNG[0,2) 이식/NNG[2,4) |
| `/categories/5/items/0/name` | 이마 지방이식 | 이마/NNG[0,2) 지방/NNG[3,5) 이식/NNG[5,7) |
| `/categories/5/items/0/unit` | 1회 | 1/SN[0,1) 회/NNB[1,2) |
| `/categories/5/items/1/name` | 볼 지방이식 | 볼/NNG[0,1) 지방/NNG[2,4) 이식/NNG[4,6) |
| `/categories/5/items/1/unit` | 1회 | 1/SN[0,1) 회/NNB[1,2) |
| `/categories/5/items/2/name` | 눈밑 지방이식 | 눈/NNG[0,1) 밑/NNG[1,2) 지방/NNG[3,5) 이식/NNG[5,7) |
| `/categories/5/items/2/unit` | 1회 | 1/SN[0,1) 회/NNB[1,2) |
| `/categories/5/items/3/name` | 풀페이스 지방이식 | 풀페이스/NNG[0,4) 지방/NNG[5,7) 이식/NNG[7,9) |
| `/categories/5/items/3/unit` | 1회 | 1/SN[0,1) 회/NNB[1,2) |
| `/categories/5/items/4/name` | 관자놀이 지방이식 | 관자놀이/NNG[0,4) 지방/NNG[5,7) 이식/NNG[7,9) |
| `/categories/5/items/4/unit` | 1회 | 1/SN[0,1) 회/NNB[1,2) |
| `/categories/5/items/5/name` | 턱 끝 지방이식 | 턱/NNG[0,1) 끝/NNG[2,3) 지방/NNG[4,6) 이식/NNG[6,8) |
| `/categories/5/items/5/unit` | 1회 | 1/SN[0,1) 회/NNB[1,2) |
| `/categories/5/items/6/name` | 나노 지방이식 (전체얼굴) | 나노/NNG[0,2) 지방/NNG[3,5) 이식/NNG[5,7) (/SSO[8,9) 전체/NNG[9,11) 얼굴/NNG[11,13) )/SSC[13,14) |
| `/categories/5/items/6/unit` | 1회 | 1/SN[0,1) 회/NNB[1,2) |

### 미결 (이 구획)

| ID | 상태 | Pointer | 내용 |
|---|---|---|---|
| B-S06-1 | B | `/categories/5/items/0/unit` | 지방이식 '1회' 의 주입량·채취 부위·마취 포함 여부가 없다. |
| P-S06-1 | P | `/categories/5/items/3/name`, `/categories/5/items/6/name` | '풀페이스' 와 '전체얼굴' 이 같은 범위인지 잠정 — 원장 전반(M8·M9·M11 등)에 두 표기가 섞여 있다. |
