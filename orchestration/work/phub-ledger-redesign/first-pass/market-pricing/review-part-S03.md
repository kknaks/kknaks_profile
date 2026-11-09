# S03 — M3 바이오스티뮬레이터/콜라겐부스터 (7항목)

[← review.md](review.md) · 소유 말단 37 · 직접 읽기 ○ · 마지막 읽은 Pointer `/categories/2/items/6/high`

## S03

### 상위 문맥 (S00 소유, 공동 참조)

- `/currency` = `KRW` · `/updated` = `2026-07-26` · `/note` = `한국 시장 참고 가격 범위. 클리닉/지역/의사에 따라 상이. 정가 아닌 시장 범위.`

### 원문 값 — 카테고리

| Pointer | 원본 컬럼명 | 자료형 | 원문 값 |
|---|---|---|---|
| `/categories/2/id` | `id` | string | `M3` |
| `/categories/2/name` | `name` | string | `바이오스티뮬레이터/콜라겐부스터` |
| `/categories/2/items` | `items` | array[7] of object | (아래 표) |

### 원문 값 — `items` (원본 순서, 각 값의 Pointer = 항목 Pointer + `/` + 컬럼명)

자료형: `name`·`unit` string, `low`·`mid`·`high` integer.

| 항목 Pointer | `name` | `unit` | `low` | `mid` | `high` |
|---|---|---|---|---|---|
| `/categories/2/items/0` | 스컬트라 (1바이알) | 1바이알 | 200000 | 350000 | 600000 |
| `/categories/2/items/1` | 스컬트라 (3회 패키지) | 3회 | 500000 | 900000 | 1500000 |
| `/categories/2/items/2` | 엘란쎄 S (1cc) | 1cc | 250000 | 400000 | 700000 |
| `/categories/2/items/3` | 엘란쎄 M (1cc) | 1cc | 300000 | 500000 | 800000 |
| `/categories/2/items/4` | 쥬베룩 볼륨 (2cc) | 2cc | 200000 | 350000 | 550000 |
| `/categories/2/items/5` | 쥬베룩 볼륨 (4cc) | 4cc | 350000 | 600000 | 900000 |
| `/categories/2/items/6` | 래디에스 (1.5cc) | 1.5cc | 250000 | 450000 | 700000 |

### 잠정 관찰 (원문 아님 — 근거 Pointer 와 상태)

| 근거 Pointer | 관찰 | 상태 |
|---|---|---|
| `/categories/2/name` | 카테고리 이름 '바이오스티뮬레이터/콜라겐부스터' — '/' 로 두 명칭을 이음. 대안(둘 중 하나)인지 같은 계열의 별칭 병기인지 원문만으로 확정 불가. | P |
| `/categories/2/items/0/name` | 항목 name 이 부위가 아닌 제품명 후보(스컬트라·엘란쎄·쥬베룩 볼륨·래디에스)+괄호 용량/회차. 부위 정보가 없음 — 필러 카테고리(부위 중심)와 이름 구성 방식이 다름. | P |
| `/categories/2/items/1/name` | '스컬트라 (3회 패키지)' unit '3회' — 3회 묶음 가격으로 읽히나, 회당 용량(바이알 수)·회차 간격은 원문에 없음. items/0 '1바이알' 과 단위 종류가 다름(바이알 vs 회). | B |
| `/categories/2/items/2/name` | '엘란쎄 S'·'엘란쎄 M' — 이름 뒤 S·M 이 제품 변형 표시 후보. 뜻(지속기간 등)은 원문에 없음. | B |
| `/categories/2/items/4/name` | '쥬베룩 볼륨' 은 2cc·4cc 두 항목. 4cc 가격(low 350000)이 2cc 의 2배(400000)보다 낮음 — 원문 값 그대로 보존, 해석하지 않음. | P |
| `/categories/2/items/6/unit` | '1.5cc' 소수 용량. | P |
| `/categories/2/items/0/low` | 7항목 모두 low < mid < high. | P |

### 직접 읽기로 수집한 표현 (문자열 값 코드포인트 구간 [start,end))

| Pointer | 구간 | 원문 구절 | 탐색 관점(확정 분류 아님) | 메모 | 자동 패턴 동일 구간 |
|---|---|---|---|---|---|
| `/categories/2/name` | [0,16) | 바이오스티뮬레이터/콜라겐부스터 | 분류명, '/' 연결 | README '/'=대안 규칙이 카테고리 이름에도 적용되는지 미확정. | slash |
| `/categories/2/items/0/name` | [0,4) | 스컬트라 | 제품명 후보 |  | 없음(패턴 밖) |
| `/categories/2/items/0/name` | [5,11) | (1바이알) | 수량·단위 | 용기 단위. | paren |
| `/categories/2/items/1/name` | [0,4) | 스컬트라 | 제품명 후보 |  | 없음(패턴 밖) |
| `/categories/2/items/1/name` | [5,13) | (3회 패키지) | 회차, 판매 구성 | '패키지' — 묶음 판매. | paren |
| `/categories/2/items/2/name` | [0,5) | 엘란쎄 S | 제품명 후보, 변형 표시 |  | 없음(패턴 밖) |
| `/categories/2/items/2/name` | [6,11) | (1cc) | 수량·단위 |  | paren |
| `/categories/2/items/3/name` | [0,5) | 엘란쎄 M | 제품명 후보, 변형 표시 |  | 없음(패턴 밖) |
| `/categories/2/items/3/name` | [6,11) | (1cc) | 수량·단위 |  | paren |
| `/categories/2/items/4/name` | [0,6) | 쥬베룩 볼륨 | 제품명 후보 | '볼륨' 이 제품명 일부인지 목적인지 미확정(M4 '쥬베룩 파인'·'쥬베룩 울트라' 와 대조 필요 — 같은 원장 안). | 없음(패턴 밖) |
| `/categories/2/items/4/name` | [7,12) | (2cc) | 수량·단위 |  | paren |
| `/categories/2/items/5/name` | [0,6) | 쥬베룩 볼륨 | 제품명 후보 |  | 없음(패턴 밖) |
| `/categories/2/items/5/name` | [7,12) | (4cc) | 수량·단위 |  | paren |
| `/categories/2/items/6/name` | [0,4) | 래디에스 | 제품명 후보 |  | 없음(패턴 밖) |
| `/categories/2/items/6/name` | [5,12) | (1.5cc) | 수량·단위 | 소수. | paren |

### 자동 후보 (정규식 일치분뿐 — 의미 해석 아님)

| Pointer | 구간 | 패턴 | 일치 구절 | 검토 |
|---|---|---|---|---|
| `/categories/2/name` | [0,16) | slash | 바이오스티뮬레이터/콜라겐부스터 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/2/items/0/name` | [5,11) | paren | (1바이알) | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/2/items/0/name` | [6,10) | num_unit | 1바이알 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/2/items/0/unit` | [0,4) | num_unit | 1바이알 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/2/items/1/name` | [5,13) | paren | (3회 패키지) | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/2/items/1/name` | [6,8) | num_unit | 3회 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/2/items/1/name` | [9,12) | kw | 패키지 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/2/items/1/unit` | [0,2) | num_unit | 3회 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/2/items/2/name` | [6,11) | paren | (1cc) | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/2/items/2/name` | [7,10) | num_unit | 1cc | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/2/items/2/unit` | [0,3) | num_unit | 1cc | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/2/items/3/name` | [6,11) | paren | (1cc) | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/2/items/3/name` | [7,10) | num_unit | 1cc | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/2/items/3/unit` | [0,3) | num_unit | 1cc | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/2/items/4/name` | [7,12) | paren | (2cc) | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/2/items/4/name` | [8,11) | num_unit | 2cc | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/2/items/4/unit` | [0,3) | num_unit | 2cc | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/2/items/5/name` | [7,12) | paren | (4cc) | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/2/items/5/name` | [8,11) | num_unit | 4cc | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/2/items/5/unit` | [0,3) | num_unit | 4cc | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/2/items/6/name` | [5,12) | paren | (1.5cc) | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/2/items/6/name` | [6,11) | num_unit | 1.5cc | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/2/items/6/unit` | [0,5) | num_unit | 1.5cc | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |

### 형태소 (Kiwi 원시 결과 — 도메인 정답 아님. `form/tag[start,end)`)

| Pointer | 원문 값 | 토큰 |
|---|---|---|
| `/categories/2/id` | M3 | 제외: 카테고리 ID(Mn) — 식별자 |
| `/categories/2/name` | 바이오스티뮬레이터/콜라겐부스터 | 바이오스티뮬레이터/NNP[0,9) //SP[9,10) 콜라겐부스터/NNP[10,16) |
| `/categories/2/items/0/name` | 스컬트라 (1바이알) | 스컬트라/NNP[0,4) (/SSO[5,6) 1/SN[6,7) 바이알/NNG[7,10) )/SSC[10,11) |
| `/categories/2/items/0/unit` | 1바이알 | 1/SN[0,1) 바이알/NNG[1,4) |
| `/categories/2/items/1/name` | 스컬트라 (3회 패키지) | 스컬트라/NNP[0,4) (/SSO[5,6) 3/SN[6,7) 회/NNB[7,8) 패키지/NNG[9,12) )/SSC[12,13) |
| `/categories/2/items/1/unit` | 3회 | 3/SN[0,1) 회/NNB[1,2) |
| `/categories/2/items/2/name` | 엘란쎄 S (1cc) | 엘란쎄/NNP[0,3) S/SL[4,5) (/SSO[6,7) 1/SN[7,8) cc/SL[8,10) )/SSC[10,11) |
| `/categories/2/items/2/unit` | 1cc | 1/SN[0,1) cc/SL[1,3) |
| `/categories/2/items/3/name` | 엘란쎄 M (1cc) | 엘란쎄/NNP[0,3) M/SL[4,5) (/SSO[6,7) 1/SN[7,8) cc/SL[8,10) )/SSC[10,11) |
| `/categories/2/items/3/unit` | 1cc | 1/SN[0,1) cc/SL[1,3) |
| `/categories/2/items/4/name` | 쥬베룩 볼륨 (2cc) | 쥬베/NNG[0,2) 룩/NNG[2,3) 볼륨/NNG[4,6) (/SSO[7,8) 2/SN[8,9) cc/SL[9,11) )/SSC[11,12) |
| `/categories/2/items/4/unit` | 2cc | 2/SN[0,1) cc/SL[1,3) |
| `/categories/2/items/5/name` | 쥬베룩 볼륨 (4cc) | 쥬베/NNG[0,2) 룩/NNG[2,3) 볼륨/NNG[4,6) (/SSO[7,8) 4/SN[8,9) cc/SL[9,11) )/SSC[11,12) |
| `/categories/2/items/5/unit` | 4cc | 4/SN[0,1) cc/SL[1,3) |
| `/categories/2/items/6/name` | 래디에스 (1.5cc) | 래디에스/NNP[0,4) (/SSO[5,6) 1.5/SN[6,9) cc/SL[9,11) )/SSC[11,12) |
| `/categories/2/items/6/unit` | 1.5cc | 1.5/SN[0,3) cc/SL[3,5) |

알려진 오분절 출현(교정 안 함):

- `/categories/2/items/4/name` [0,3) `쥬베룩` → [['쥬베', 'NNG'], ['룩', 'NNG']] — 제품명 후보 분절. 같은 원장의 '쥬베룩 울트라' 출현에서는 '쥬베룩/NNG' 한 토큰 — 분석 불일치.
- `/categories/2/items/5/name` [0,3) `쥬베룩` → [['쥬베', 'NNG'], ['룩', 'NNG']] — 제품명 후보 분절. 같은 원장의 '쥬베룩 울트라' 출현에서는 '쥬베룩/NNG' 한 토큰 — 분석 불일치.

### 미결 (이 구획)

| ID | 상태 | Pointer | 내용 |
|---|---|---|---|
| B-S03-1 | B | `/categories/2/items/1/name`, `/categories/2/items/1/unit` | '3회 패키지' 의 회당 용량·간격·총 바이알 수가 없다. 회당 가격 비교가 제한된다. |
| B-S03-2 | B | `/categories/2/items/2/name`, `/categories/2/items/3/name` | 'S'·'M' 변형의 뜻이 원문에 없다. |
| P-S03-1 | P | `/categories/2/name` | 카테고리 이름의 '/' 의미(대안·별칭·병기) 잠정. 같은 형식이 M5·M9·M10 에도 있음. |
| F-S03-1 | F | `/categories/2/items/4/name`, `/categories/3/items/2/name` | '쥬베룩 볼륨'(M3)과 '쥬베룩 파인'·'쥬베룩 울트라'(M4)가 서로 다른 카테고리에 있다 — 제품 계열·변형 관계는 후속 연결 과제. |
