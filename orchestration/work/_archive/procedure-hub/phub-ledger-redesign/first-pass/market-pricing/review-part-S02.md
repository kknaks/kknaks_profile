# S02 — M2 필러 (8항목)

[← review.md](review.md) · 소유 말단 42 · 직접 읽기 ○ · 마지막 읽은 Pointer `/categories/1/items/7/high`

## S02

### 상위 문맥 (S00 소유, 공동 참조)

- `/currency` = `KRW` · `/updated` = `2026-07-26` · `/note` = `한국 시장 참고 가격 범위. 클리닉/지역/의사에 따라 상이. 정가 아닌 시장 범위.`

### 원문 값 — 카테고리

| Pointer | 원본 컬럼명 | 자료형 | 원문 값 |
|---|---|---|---|
| `/categories/1/id` | `id` | string | `M2` |
| `/categories/1/name` | `name` | string | `필러` |
| `/categories/1/items` | `items` | array[8] of object | (아래 표) |

### 원문 값 — `items` (원본 순서, 각 값의 Pointer = 항목 Pointer + `/` + 컬럼명)

자료형: `name`·`unit` string, `low`·`mid`·`high` integer.

| 항목 Pointer | `name` | `unit` | `low` | `mid` | `high` |
|---|---|---|---|---|---|
| `/categories/1/items/0` | 팔자주름 (HA 1cc) | 1cc | 150000 | 300000 | 500000 |
| `/categories/1/items/1` | 입술 볼륨 (HA 1cc) | 1cc | 200000 | 350000 | 600000 |
| `/categories/1/items/2` | 코 필러 (HA 1cc) | 1cc | 200000 | 400000 | 700000 |
| `/categories/1/items/3` | 턱 끝 볼륨 (HA 1cc) | 1cc | 200000 | 400000 | 600000 |
| `/categories/1/items/4` | 이마 볼륨 (HA 2cc) | 2cc | 400000 | 700000 | 1200000 |
| `/categories/1/items/5` | 볼 볼륨 (HA 1cc) | 1cc | 200000 | 350000 | 600000 |
| `/categories/1/items/6` | 눈밑 꺼짐 (HA 1cc) | 1cc | 250000 | 400000 | 700000 |
| `/categories/1/items/7` | 관자놀이 (HA 2cc) | 2cc | 400000 | 600000 | 1000000 |

### 잠정 관찰 (원문 아님 — 근거 Pointer 와 상태)

| 근거 Pointer | 관찰 | 상태 |
|---|---|---|
| `/categories/1/items/0/name` | 8항목 모두 '<부위/고민> (HA <n>cc)' 형태. 괄호 안 'HA' 는 재질/성분 약어 후보(HA 의 풀이는 원문에 없음), 'Ncc' 는 용량. unit 칸에도 같은 용량이 반복됨(1cc 6개, 2cc 2개). | P |
| `/categories/1/items/2/name` | '코 필러 (HA 1cc)' — 이 항목만 name 에 시술명 '필러'가 다시 들어 있음. 다른 7항목은 부위/고민만. | P |
| `/categories/1/items/6/name` | '눈밑 꺼짐' — 부위(눈밑)+고민(꺼짐) 결합. '이마 볼륨'·'볼 볼륨'·'입술 볼륨'·'턱 끝 볼륨' 의 '볼륨' 은 고민인지 목적(효과)인지 원문만으로 구분 불가. | P |
| `/categories/1/items/7/name` | '관자놀이 (HA 2cc)' — 고민/목적 표현 없이 부위만. | P |
| `/categories/1/items/4/unit` | 이마 볼륨·관자놀이는 2cc 단위 가격. 1cc 항목과 단위가 달라 cc당 비교 시 단위 환산이 필요하나, 이번 단계에서 환산하지 않음. | P |
| `/categories/1/items/0/low` | 8항목 모두 low < mid < high. | P |

### 직접 읽기로 수집한 표현 (문자열 값 코드포인트 구간 [start,end))

| Pointer | 구간 | 원문 구절 | 탐색 관점(확정 분류 아님) | 메모 | 자동 패턴 동일 구간 |
|---|---|---|---|---|---|
| `/categories/1/items/0/name` | [0,4) | 팔자주름 | 부위 후보, 고민 후보 | 붙여 씀. | 없음(패턴 밖) |
| `/categories/1/items/0/name` | [5,13) | (HA 1cc) | 재질/성분 후보, 수량·단위 |  | paren |
| `/categories/1/items/1/name` | [0,5) | 입술 볼륨 | 부위 후보, 목적/고민 후보 |  | 없음(패턴 밖) |
| `/categories/1/items/1/name` | [6,14) | (HA 1cc) | 재질/성분 후보, 수량·단위 |  | paren |
| `/categories/1/items/2/name` | [0,4) | 코 필러 | 부위 후보, 시술명 후보 |  | 없음(패턴 밖) |
| `/categories/1/items/2/name` | [5,13) | (HA 1cc) | 재질/성분 후보, 수량·단위 |  | paren |
| `/categories/1/items/3/name` | [0,6) | 턱 끝 볼륨 | 부위 후보, 목적/고민 후보 | '턱 끝' 은 띄어 쓴 두 어절 부위 표현. | 없음(패턴 밖) |
| `/categories/1/items/3/name` | [0,3) | 턱 끝 | 부위 후보, 위치 수식 | '끝' 이 턱의 하위 위치를 한정. | 없음(패턴 밖) |
| `/categories/1/items/3/name` | [7,15) | (HA 1cc) | 재질/성분 후보, 수량·단위 |  | paren |
| `/categories/1/items/4/name` | [0,5) | 이마 볼륨 | 부위 후보, 목적/고민 후보 |  | 없음(패턴 밖) |
| `/categories/1/items/4/name` | [6,14) | (HA 2cc) | 재질/성분 후보, 수량·단위 |  | paren |
| `/categories/1/items/5/name` | [0,4) | 볼 볼륨 | 부위 후보, 목적/고민 후보 | '볼'(부위)과 '볼륨'의 첫 글자가 같음 — 문자열 검색 시 부분일치 오탐 위험. | 없음(패턴 밖) |
| `/categories/1/items/5/name` | [5,13) | (HA 1cc) | 재질/성분 후보, 수량·단위 |  | paren |
| `/categories/1/items/6/name` | [0,5) | 눈밑 꺼짐 | 부위 후보, 고민 후보 |  | 없음(패턴 밖) |
| `/categories/1/items/6/name` | [6,14) | (HA 1cc) | 재질/성분 후보, 수량·단위 |  | paren |
| `/categories/1/items/7/name` | [0,4) | 관자놀이 | 부위 후보 |  | 없음(패턴 밖) |
| `/categories/1/items/7/name` | [5,13) | (HA 2cc) | 재질/성분 후보, 수량·단위 |  | paren |

### 자동 후보 (정규식 일치분뿐 — 의미 해석 아님)

| Pointer | 구간 | 패턴 | 일치 구절 | 검토 |
|---|---|---|---|---|
| `/categories/1/items/0/name` | [5,13) | paren | (HA 1cc) | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/1/items/0/name` | [9,12) | num_unit | 1cc | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/1/items/0/unit` | [0,3) | num_unit | 1cc | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/1/items/1/name` | [6,14) | paren | (HA 1cc) | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/1/items/1/name` | [10,13) | num_unit | 1cc | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/1/items/1/unit` | [0,3) | num_unit | 1cc | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/1/items/2/name` | [5,13) | paren | (HA 1cc) | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/1/items/2/name` | [9,12) | num_unit | 1cc | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/1/items/2/unit` | [0,3) | num_unit | 1cc | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/1/items/3/name` | [7,15) | paren | (HA 1cc) | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/1/items/3/name` | [11,14) | num_unit | 1cc | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/1/items/3/unit` | [0,3) | num_unit | 1cc | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/1/items/4/name` | [6,14) | paren | (HA 2cc) | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/1/items/4/name` | [10,13) | num_unit | 2cc | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/1/items/4/unit` | [0,3) | num_unit | 2cc | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/1/items/5/name` | [5,13) | paren | (HA 1cc) | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/1/items/5/name` | [9,12) | num_unit | 1cc | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/1/items/5/unit` | [0,3) | num_unit | 1cc | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/1/items/6/name` | [6,14) | paren | (HA 1cc) | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/1/items/6/name` | [10,13) | num_unit | 1cc | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/1/items/6/unit` | [0,3) | num_unit | 1cc | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/1/items/7/name` | [5,13) | paren | (HA 2cc) | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/1/items/7/name` | [9,12) | num_unit | 2cc | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/1/items/7/unit` | [0,3) | num_unit | 2cc | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |

### 형태소 (Kiwi 원시 결과 — 도메인 정답 아님. `form/tag[start,end)`)

| Pointer | 원문 값 | 토큰 |
|---|---|---|
| `/categories/1/id` | M2 | 제외: 카테고리 ID(Mn) — 식별자 |
| `/categories/1/name` | 필러 | 필러/NNP[0,2) |
| `/categories/1/items/0/name` | 팔자주름 (HA 1cc) | 팔자/NNG[0,2) 주름/NNG[2,4) (/SSO[5,6) HA/SL[6,8) 1/SN[9,10) cc/SL[10,12) )/SSC[12,13) |
| `/categories/1/items/0/unit` | 1cc | 1/SN[0,1) cc/SL[1,3) |
| `/categories/1/items/1/name` | 입술 볼륨 (HA 1cc) | 입술/NNG[0,2) 볼륨/NNG[3,5) (/SSO[6,7) HA/SL[7,9) 1/SN[10,11) cc/SL[11,13) )/SSC[13,14) |
| `/categories/1/items/1/unit` | 1cc | 1/SN[0,1) cc/SL[1,3) |
| `/categories/1/items/2/name` | 코 필러 (HA 1cc) | 코/NNG[0,1) 필러/NNP[2,4) (/SSO[5,6) HA/SL[6,8) 1/SN[9,10) cc/SL[10,12) )/SSC[12,13) |
| `/categories/1/items/2/unit` | 1cc | 1/SN[0,1) cc/SL[1,3) |
| `/categories/1/items/3/name` | 턱 끝 볼륨 (HA 1cc) | 턱/NNG[0,1) 끝/NNG[2,3) 볼륨/NNG[4,6) (/SSO[7,8) HA/SL[8,10) 1/SN[11,12) cc/SL[12,14) )/SSC[14,15) |
| `/categories/1/items/3/unit` | 1cc | 1/SN[0,1) cc/SL[1,3) |
| `/categories/1/items/4/name` | 이마 볼륨 (HA 2cc) | 이마/NNG[0,2) 볼륨/NNG[3,5) (/SSO[6,7) HA/SL[7,9) 2/SN[10,11) cc/SL[11,13) )/SSC[13,14) |
| `/categories/1/items/4/unit` | 2cc | 2/SN[0,1) cc/SL[1,3) |
| `/categories/1/items/5/name` | 볼 볼륨 (HA 1cc) | 볼/NNG[0,1) 볼륨/NNG[2,4) (/SSO[5,6) HA/SL[6,8) 1/SN[9,10) cc/SL[10,12) )/SSC[12,13) |
| `/categories/1/items/5/unit` | 1cc | 1/SN[0,1) cc/SL[1,3) |
| `/categories/1/items/6/name` | 눈밑 꺼짐 (HA 1cc) | 눈/NNG[0,1) 밑/NNG[1,2) 꺼짐/NNG[3,5) (/SSO[6,7) HA/SL[7,9) 1/SN[10,11) cc/SL[11,13) )/SSC[13,14) |
| `/categories/1/items/6/unit` | 1cc | 1/SN[0,1) cc/SL[1,3) |
| `/categories/1/items/7/name` | 관자놀이 (HA 2cc) | 관자놀이/NNG[0,4) (/SSO[5,6) HA/SL[6,8) 2/SN[9,10) cc/SL[10,12) )/SSC[12,13) |
| `/categories/1/items/7/unit` | 2cc | 2/SN[0,1) cc/SL[1,3) |

### 미결 (이 구획)

| ID | 상태 | Pointer | 내용 |
|---|---|---|---|
| B-S02-1 | B | `/categories/1/items/0/name` | 'HA' 의 풀이·제품명이 없다(8항목). 제품별 가격 구분이 불가하다. |
| P-S02-1 | P | `/categories/1/items/1/name` | '볼륨' 이 고민(볼륨 부족)인지 목적(볼륨 증가)인지 잠정. 부위/고민 분리는 후속 의미 조사. |
