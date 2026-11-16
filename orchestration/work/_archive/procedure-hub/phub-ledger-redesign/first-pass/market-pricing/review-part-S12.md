# S12 — M12 마이크로니들링(MTS) (6항목)

[← review.md](review.md) · 소유 말단 32 · 직접 읽기 ○ · 마지막 읽은 Pointer `/categories/11/items/5/high`

## S12

### 상위 문맥 (S00 소유, 공동 참조)

- `/currency` = `KRW` · `/updated` = `2026-07-26` · `/note` = `한국 시장 참고 가격 범위. 클리닉/지역/의사에 따라 상이. 정가 아닌 시장 범위.`

### 원문 값 — 카테고리

| Pointer | 원본 컬럼명 | 자료형 | 원문 값 |
|---|---|---|---|
| `/categories/11/id` | `id` | string | `M12` |
| `/categories/11/name` | `name` | string | `마이크로니들링(MTS)` |
| `/categories/11/items` | `items` | array[6] of object | (아래 표) |

### 원문 값 — `items` (원본 순서, 각 값의 Pointer = 항목 Pointer + `/` + 컬럼명)

자료형: `name`·`unit` string, `low`·`mid`·`high` integer.

| 항목 Pointer | `name` | `unit` | `low` | `mid` | `high` |
|---|---|---|---|---|---|
| `/categories/11/items/0` | MTS (전체얼굴) | 1회 | 50000 | 100000 | 200000 |
| `/categories/11/items/1` | MTS + PRP (전체얼굴) | 1회 | 150000 | 300000 | 500000 |
| `/categories/11/items/2` | MTS + 스킨부스터 | 1회 | 100000 | 200000 | 400000 |
| `/categories/11/items/3` | 더마펜4 (전체얼굴) | 1회 | 80000 | 150000 | 300000 |
| `/categories/11/items/4` | MTS (여드름 흉터 집중) | 1회 | 100000 | 200000 | 350000 |
| `/categories/11/items/5` | MTS (두피 탈모) | 1회 | 80000 | 150000 | 300000 |

### 잠정 관찰 (원문 아님 — 근거 Pointer 와 상태)

| 근거 Pointer | 관찰 | 상태 |
|---|---|---|
| `/categories/11/name` | '마이크로니들링(MTS)' — 한글 명칭+괄호 영문 약어. 항목 name 은 약어 'MTS' 를 씀. | P |
| `/categories/11/items/1/name` | 'MTS + PRP (전체얼굴)' (150000/300000/500000) — M5 'PRP + MTS 콤보'(200000/350000/600000)와 구성 요소가 같아 보이나 순서·'콤보'·부위 표기·가격이 다름. | P |
| `/categories/11/items/2/name` | 'MTS + 스킨부스터' — 함께 시행 조합. '스킨부스터' 는 M4 카테고리 이름과 같은 문자열이며 어떤 제품인지·용량은 없음. 적용 범위 없음. | B |
| `/categories/11/items/3/name` | '더마펜4' — MTS 카테고리 안의 장비명 후보(숫자 포함). | P |
| `/categories/11/items/4/name` | 'MTS (여드름 흉터 집중)' — '집중' 은 시술 강도/범위 수식 후보. 무엇이 다른지(밀도·깊이·회차) 원문에 없음. | B |
| `/categories/11/items/5/name` | 'MTS (두피 탈모)' — 부위(두피)+고민(탈모). | P |
| `/categories/11/items/0/low` | 6항목 모두 low < mid < high. | P |

### 직접 읽기로 수집한 표현 (문자열 값 코드포인트 구간 [start,end))

| Pointer | 구간 | 원문 구절 | 탐색 관점(확정 분류 아님) | 메모 | 자동 패턴 동일 구간 |
|---|---|---|---|---|---|
| `/categories/11/name` | [0,12) | 마이크로니들링(MTS) | 분류명, 영문 약어 |  | 없음(패턴 밖) |
| `/categories/11/items/0/name` | [0,3) | MTS | 시술명 후보, 영문 약어 |  | 없음(패턴 밖) |
| `/categories/11/items/0/name` | [4,10) | (전체얼굴) | 적용 범위, 부위 후보 |  | paren |
| `/categories/11/items/1/name` | [0,9) | MTS + PRP | 조합, '+' 연결 |  | plus |
| `/categories/11/items/1/name` | [10,16) | (전체얼굴) | 적용 범위, 부위 후보 |  | paren |
| `/categories/11/items/2/name` | [0,11) | MTS + 스킨부스터 | 조합, '+' 연결 |  | plus |
| `/categories/11/items/3/name` | [0,4) | 더마펜4 | 장비명 후보, 숫자 포함 |  | 없음(패턴 밖) |
| `/categories/11/items/3/name` | [5,11) | (전체얼굴) | 적용 범위, 부위 후보 |  | paren |
| `/categories/11/items/4/name` | [4,15) | (여드름 흉터 집중) | 고민/적응증 후보, 강도/범위 수식 |  | paren |
| `/categories/11/items/4/name` | [12,14) | 집중 | 강도/범위 수식 |  | kw |
| `/categories/11/items/5/name` | [4,11) | (두피 탈모) | 부위 후보, 고민 후보 |  | paren |

### 자동 후보 (정규식 일치분뿐 — 의미 해석 아님)

| Pointer | 구간 | 패턴 | 일치 구절 | 검토 |
|---|---|---|---|---|
| `/categories/11/name` | [7,12) | paren | (MTS) | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/11/items/0/name` | [4,10) | paren | (전체얼굴) | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/11/items/0/name` | [5,9) | kw | 전체얼굴 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/11/items/0/unit` | [0,2) | num_unit | 1회 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/11/items/1/name` | [10,16) | paren | (전체얼굴) | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/11/items/1/name` | [0,9) | plus | MTS + PRP | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/11/items/1/name` | [11,15) | kw | 전체얼굴 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/11/items/1/unit` | [0,2) | num_unit | 1회 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/11/items/2/name` | [0,11) | plus | MTS + 스킨부스터 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/11/items/2/unit` | [0,2) | num_unit | 1회 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/11/items/3/name` | [5,11) | paren | (전체얼굴) | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/11/items/3/name` | [6,10) | kw | 전체얼굴 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/11/items/3/unit` | [0,2) | num_unit | 1회 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/11/items/4/name` | [4,15) | paren | (여드름 흉터 집중) | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/11/items/4/name` | [12,14) | kw | 집중 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/11/items/4/unit` | [0,2) | num_unit | 1회 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/11/items/5/name` | [4,11) | paren | (두피 탈모) | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/11/items/5/unit` | [0,2) | num_unit | 1회 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |

### 형태소 (Kiwi 원시 결과 — 도메인 정답 아님. `form/tag[start,end)`)

| Pointer | 원문 값 | 토큰 |
|---|---|---|
| `/categories/11/id` | M12 | 제외: 카테고리 ID(Mn) — 식별자 |
| `/categories/11/name` | 마이크로니들링(MTS) | 마이크로니들링/NNP[0,7) (/SSO[7,8) MTS/SL[8,11) )/SSC[11,12) |
| `/categories/11/items/0/name` | MTS (전체얼굴) | MTS/SL[0,3) (/SSO[4,5) 전체/NNG[5,7) 얼굴/NNG[7,9) )/SSC[9,10) |
| `/categories/11/items/0/unit` | 1회 | 1/SN[0,1) 회/NNB[1,2) |
| `/categories/11/items/1/name` | MTS + PRP (전체얼굴) | MTS/SL[0,3) +/SW[4,5) PRP/SL[6,9) (/SSO[10,11) 전체/NNG[11,13) 얼굴/NNG[13,15) )/SSC[15,16) |
| `/categories/11/items/1/unit` | 1회 | 1/SN[0,1) 회/NNB[1,2) |
| `/categories/11/items/2/name` | MTS + 스킨부스터 | MTS/SL[0,3) +/SW[4,5) 스킨부스터/NNP[6,11) |
| `/categories/11/items/2/unit` | 1회 | 1/SN[0,1) 회/NNB[1,2) |
| `/categories/11/items/3/name` | 더마펜4 (전체얼굴) | 더/MAG[0,1) 마/NNG[1,2) 펜/NNG[2,3) 4/SN[3,4) (/SSO[5,6) 전체/NNG[6,8) 얼굴/NNG[8,10) )/SSC[10,11) |
| `/categories/11/items/3/unit` | 1회 | 1/SN[0,1) 회/NNB[1,2) |
| `/categories/11/items/4/name` | MTS (여드름 흉터 집중) | MTS/SL[0,3) (/SSO[4,5) 여드름/NNG[5,8) 흉터/NNG[9,11) 집중/NNG[12,14) )/SSC[14,15) |
| `/categories/11/items/4/unit` | 1회 | 1/SN[0,1) 회/NNB[1,2) |
| `/categories/11/items/5/name` | MTS (두피 탈모) | MTS/SL[0,3) (/SSO[4,5) 두피/NNP[5,7) 탈모/NNG[8,10) )/SSC[10,11) |
| `/categories/11/items/5/unit` | 1회 | 1/SN[0,1) 회/NNB[1,2) |

알려진 오분절 출현(교정 안 함):

- `/categories/11/items/3/name` [0,3) `더마펜` → [['더', 'MAG'], ['마', 'NNG'], ['펜', 'NNG']] — 장비명 후보 첫 음절 '더'가 비교 부사(MAG)로 태깅 — 비교·정도 부사 수집 시 오탐.

### 미결 (이 구획)

| ID | 상태 | Pointer | 내용 |
|---|---|---|---|
| B-S12-1 | B | `/categories/11/items/2/name` | 'MTS + 스킨부스터' 의 스킨부스터 제품·용량·범위가 없다. |
| B-S12-2 | B | `/categories/11/items/4/name` | '집중' 의 차이(밀도·깊이·회차)가 없다. |
