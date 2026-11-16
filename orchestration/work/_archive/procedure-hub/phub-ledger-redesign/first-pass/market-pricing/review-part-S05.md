# S05 — M5 PRP/엑소좀 (6항목)

[← review.md](review.md) · 소유 말단 32 · 직접 읽기 ○ · 마지막 읽은 Pointer `/categories/4/items/5/high`

## S05

### 상위 문맥 (S00 소유, 공동 참조)

- `/currency` = `KRW` · `/updated` = `2026-07-26` · `/note` = `한국 시장 참고 가격 범위. 클리닉/지역/의사에 따라 상이. 정가 아닌 시장 범위.`

### 원문 값 — 카테고리

| Pointer | 원본 컬럼명 | 자료형 | 원문 값 |
|---|---|---|---|
| `/categories/4/id` | `id` | string | `M5` |
| `/categories/4/name` | `name` | string | `PRP/엑소좀` |
| `/categories/4/items` | `items` | array[6] of object | (아래 표) |

### 원문 값 — `items` (원본 순서, 각 값의 Pointer = 항목 Pointer + `/` + 컬럼명)

자료형: `name`·`unit` string, `low`·`mid`·`high` integer.

| 항목 Pointer | `name` | `unit` | `low` | `mid` | `high` |
|---|---|---|---|---|---|
| `/categories/4/items/0` | PRP (전체얼굴) | 1회 | 100000 | 200000 | 400000 |
| `/categories/4/items/1` | PRP (두피) | 1회 | 150000 | 300000 | 500000 |
| `/categories/4/items/2` | 엑소좀 (전체얼굴) | 1회 | 200000 | 400000 | 800000 |
| `/categories/4/items/3` | 엑소좀 (두피) | 1회 | 250000 | 500000 | 900000 |
| `/categories/4/items/4` | PDRN 주사 (부위당) | 1회 | 50000 | 100000 | 200000 |
| `/categories/4/items/5` | PRP + MTS 콤보 | 1회 | 200000 | 350000 | 600000 |

### 잠정 관찰 (원문 아님 — 근거 Pointer 와 상태)

| 근거 Pointer | 관찰 | 상태 |
|---|---|---|
| `/categories/4/name` | 'PRP/엑소좀' — 두 이름을 '/' 로 연결한 카테고리 이름. 항목에는 PRP·엑소좀 외에 'PDRN 주사', 'PRP + MTS 콤보' 가 있어 카테고리 이름이 담는 범위보다 넓음. | P |
| `/categories/4/items/0/name` | 'PRP (전체얼굴)'·'PRP (두피)'·'엑소좀 (전체얼굴)'·'엑소좀 (두피)' — 괄호가 적용 부위. 같은 시술 이름이 부위별로 다른 가격 항목으로 나뉨(부위가 가격 옵션 축). | P |
| `/categories/4/items/4/name` | 'PDRN 주사 (부위당)' 의 name 은 '부위당' 인데 unit 은 '1회' — 같은 항목 안 가격 기준 표현이 둘이며 서로 같은 뜻인지 원문만으로 확정 불가. | I |
| `/categories/4/items/5/name` | 'PRP + MTS 콤보' — '+' 로 두 시술을 함께 묶은 판매 항목. README 규칙상 '+' = 함께 시술. 같은 원장 M12 에 'MTS + PRP (전체얼굴)'(/categories/11/items/1)이 다른 가격으로 있음. | P |
| `/categories/4/items/0/low` | 6항목 모두 low < mid < high. | P |

### 직접 읽기로 수집한 표현 (문자열 값 코드포인트 구간 [start,end))

| Pointer | 구간 | 원문 구절 | 탐색 관점(확정 분류 아님) | 메모 | 자동 패턴 동일 구간 |
|---|---|---|---|---|---|
| `/categories/4/name` | [0,7) | PRP/엑소좀 | 분류명, '/' 연결 |  | slash |
| `/categories/4/items/0/name` | [0,3) | PRP | 시술명 후보, 영문 약어 |  | 없음(패턴 밖) |
| `/categories/4/items/0/name` | [4,10) | (전체얼굴) | 적용 범위, 부위 후보 |  | paren |
| `/categories/4/items/1/name` | [0,3) | PRP | 시술명 후보, 영문 약어 |  | 없음(패턴 밖) |
| `/categories/4/items/1/name` | [4,8) | (두피) | 부위 후보 |  | paren |
| `/categories/4/items/2/name` | [0,3) | 엑소좀 | 시술명/성분 후보 |  | 없음(패턴 밖) |
| `/categories/4/items/2/name` | [4,10) | (전체얼굴) | 적용 범위, 부위 후보 |  | paren |
| `/categories/4/items/3/name` | [0,3) | 엑소좀 | 시술명/성분 후보 |  | 없음(패턴 밖) |
| `/categories/4/items/3/name` | [4,8) | (두피) | 부위 후보 |  | paren |
| `/categories/4/items/4/name` | [0,7) | PDRN 주사 | 시술명 후보, 영문 약어 |  | 없음(패턴 밖) |
| `/categories/4/items/4/name` | [8,13) | (부위당) | 가격 기준, 분모 | '당' — 단위당 표현. | paren |
| `/categories/4/items/5/name` | [0,12) | PRP + MTS 콤보 | 조합, 판매 구성 | '콤보' — 묶음 판매 표시. | 없음(패턴 밖) |
| `/categories/4/items/5/name` | [6,9) | MTS | 시술명 후보, 영문 약어 |  | 없음(패턴 밖) |

### 자동 후보 (정규식 일치분뿐 — 의미 해석 아님)

| Pointer | 구간 | 패턴 | 일치 구절 | 검토 |
|---|---|---|---|---|
| `/categories/4/name` | [0,7) | slash | PRP/엑소좀 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/4/items/0/name` | [4,10) | paren | (전체얼굴) | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/4/items/0/name` | [5,9) | kw | 전체얼굴 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/4/items/0/unit` | [0,2) | num_unit | 1회 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/4/items/1/name` | [4,8) | paren | (두피) | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/4/items/1/unit` | [0,2) | num_unit | 1회 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/4/items/2/name` | [4,10) | paren | (전체얼굴) | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/4/items/2/name` | [5,9) | kw | 전체얼굴 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/4/items/2/unit` | [0,2) | num_unit | 1회 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/4/items/3/name` | [4,8) | paren | (두피) | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/4/items/3/unit` | [0,2) | num_unit | 1회 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/4/items/4/name` | [8,13) | paren | (부위당) | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/4/items/4/name` | [9,12) | kw | 부위당 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/4/items/4/unit` | [0,2) | num_unit | 1회 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/4/items/5/name` | [0,9) | plus | PRP + MTS | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/4/items/5/name` | [10,12) | kw | 콤보 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/4/items/5/unit` | [0,2) | num_unit | 1회 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |

### 형태소 (Kiwi 원시 결과 — 도메인 정답 아님. `form/tag[start,end)`)

| Pointer | 원문 값 | 토큰 |
|---|---|---|
| `/categories/4/id` | M5 | 제외: 카테고리 ID(Mn) — 식별자 |
| `/categories/4/name` | PRP/엑소좀 | PRP/SL[0,3) //SP[3,4) 엑소좀/NNP[4,7) |
| `/categories/4/items/0/name` | PRP (전체얼굴) | PRP/SL[0,3) (/SSO[4,5) 전체/NNG[5,7) 얼굴/NNG[7,9) )/SSC[9,10) |
| `/categories/4/items/0/unit` | 1회 | 1/SN[0,1) 회/NNB[1,2) |
| `/categories/4/items/1/name` | PRP (두피) | PRP/SL[0,3) (/SSO[4,5) 두피/NNP[5,7) )/SSC[7,8) |
| `/categories/4/items/1/unit` | 1회 | 1/SN[0,1) 회/NNB[1,2) |
| `/categories/4/items/2/name` | 엑소좀 (전체얼굴) | 엑소좀/NNP[0,3) (/SSO[4,5) 전체/NNG[5,7) 얼굴/NNG[7,9) )/SSC[9,10) |
| `/categories/4/items/2/unit` | 1회 | 1/SN[0,1) 회/NNB[1,2) |
| `/categories/4/items/3/name` | 엑소좀 (두피) | 엑소좀/NNG[0,3) (/SSO[4,5) 두피/NNP[5,7) )/SSC[7,8) |
| `/categories/4/items/3/unit` | 1회 | 1/SN[0,1) 회/NNB[1,2) |
| `/categories/4/items/4/name` | PDRN 주사 (부위당) | PDRN/SL[0,4) 주사/NNG[5,7) (/SSO[8,9) 부위당/NNP[9,12) )/SSC[12,13) |
| `/categories/4/items/4/unit` | 1회 | 1/SN[0,1) 회/NNB[1,2) |
| `/categories/4/items/5/name` | PRP + MTS 콤보 | PRP/SL[0,3) +/SW[4,5) MTS/SL[6,9) 콤보/NNG[10,12) |
| `/categories/4/items/5/unit` | 1회 | 1/SN[0,1) 회/NNB[1,2) |

알려진 오분절 출현(교정 안 함):

- `/categories/4/items/4/name` [9,12) `부위당` → [['부위당', 'NNP']] — '부위'+'당'(단위당)이 한 고유명사로 묶여 분모 표현 '당' 이 토큰으로 안 잡힘.

### 미결 (이 구획)

| ID | 상태 | Pointer | 내용 |
|---|---|---|---|
| I-S05-1 | I | `/categories/4/items/4/name`, `/categories/4/items/4/unit` | name '(부위당)' 과 unit '1회' 의 가격 기준이 다르게 적혀 있다. 원본 보존 — 둘 중 어느 쪽이 기준인지 후속 확인 후보. |
| F-S05-1 | F | `/categories/4/items/5/name`, `/categories/11/items/1/name` | 'PRP + MTS 콤보'(M5)와 'MTS + PRP (전체얼굴)'(M12)가 순서·부위표기·가격이 다르다. 같은 조합인지 후속 연결 과제(병합하지 않음). |
| B-S05-1 | B | `/categories/4/items/4/name` | '부위당' 의 부위 크기·정의가 없다. |
