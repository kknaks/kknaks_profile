# S11 — M11 니들RF (7항목)

[← review.md](review.md) · 소유 말단 37 · 직접 읽기 ○ · 마지막 읽은 Pointer `/categories/10/items/6/high`

## S11

### 상위 문맥 (S00 소유, 공동 참조)

- `/currency` = `KRW` · `/updated` = `2026-07-26` · `/note` = `한국 시장 참고 가격 범위. 클리닉/지역/의사에 따라 상이. 정가 아닌 시장 범위.`

### 원문 값 — 카테고리

| Pointer | 원본 컬럼명 | 자료형 | 원문 값 |
|---|---|---|---|
| `/categories/10/id` | `id` | string | `M11` |
| `/categories/10/name` | `name` | string | `니들RF` |
| `/categories/10/items` | `items` | array[7] of object | (아래 표) |

### 원문 값 — `items` (원본 순서, 각 값의 Pointer = 항목 Pointer + `/` + 컬럼명)

자료형: `name`·`unit` string, `low`·`mid`·`high` integer.

| 항목 Pointer | `name` | `unit` | `low` | `mid` | `high` |
|---|---|---|---|---|---|
| `/categories/10/items/0` | 시크릿 (전체얼굴) | 1회 | 200000 | 400000 | 700000 |
| `/categories/10/items/1` | 인피니 (전체얼굴) | 1회 | 200000 | 400000 | 700000 |
| `/categories/10/items/2` | 모피어스8 (전체얼굴) | 1회 | 300000 | 500000 | 900000 |
| `/categories/10/items/3` | 포텐자 (전체얼굴) | 1회 | 300000 | 500000 | 900000 |
| `/categories/10/items/4` | 니들RF (여드름 흉터) | 1회 | 200000 | 400000 | 700000 |
| `/categories/10/items/5` | 니들RF (모공축소) | 1회 | 150000 | 300000 | 600000 |
| `/categories/10/items/6` | 니들RF (목주름) | 1회 | 200000 | 350000 | 600000 |

### 잠정 관찰 (원문 아님 — 근거 Pointer 와 상태)

| 근거 Pointer | 관찰 | 상태 |
|---|---|---|
| `/categories/10/items/0/name` | items/0~3 은 장비명 후보(시크릿·인피니·모피어스8·포텐자)+(전체얼굴). items/4~6 은 카테고리명 '니들RF'+괄호 고민/목적(여드름 흉터·모공축소·목주름) — 같은 카테고리에 장비 축과 고민 축 항목이 섞여 있음. | P |
| `/categories/10/items/4/name` | 고민 축 항목(items/4~6)에는 장비명·적용 범위가 없고, 장비 축 항목(items/0~3)에는 고민이 없음. 두 축 항목 사이 대응은 원문에 없음. | B |
| `/categories/10/items/5/name` | '모공축소' — 고민(모공)+효과 방향(축소) 결합어. | P |
| `/categories/10/items/0/low` | 7항목 모두 low < mid < high. | P |

### 직접 읽기로 수집한 표현 (문자열 값 코드포인트 구간 [start,end))

| Pointer | 구간 | 원문 구절 | 탐색 관점(확정 분류 아님) | 메모 | 자동 패턴 동일 구간 |
|---|---|---|---|---|---|
| `/categories/10/name` | [0,4) | 니들RF | 분류명, 영한 혼합 |  | 없음(패턴 밖) |
| `/categories/10/items/0/name` | [0,3) | 시크릿 | 장비명 후보 |  | 없음(패턴 밖) |
| `/categories/10/items/0/name` | [4,10) | (전체얼굴) | 적용 범위, 부위 후보 |  | paren |
| `/categories/10/items/1/name` | [0,3) | 인피니 | 장비명 후보 |  | 없음(패턴 밖) |
| `/categories/10/items/1/name` | [4,10) | (전체얼굴) | 적용 범위, 부위 후보 |  | paren |
| `/categories/10/items/2/name` | [0,5) | 모피어스8 | 장비명 후보, 숫자 포함 |  | 없음(패턴 밖) |
| `/categories/10/items/2/name` | [6,12) | (전체얼굴) | 적용 범위, 부위 후보 |  | paren |
| `/categories/10/items/3/name` | [0,3) | 포텐자 | 장비명 후보 |  | 없음(패턴 밖) |
| `/categories/10/items/3/name` | [4,10) | (전체얼굴) | 적용 범위, 부위 후보 |  | paren |
| `/categories/10/items/4/name` | [0,4) | 니들RF | 분류명 반복 |  | 없음(패턴 밖) |
| `/categories/10/items/4/name` | [5,13) | (여드름 흉터) | 고민/적응증 후보 |  | paren |
| `/categories/10/items/5/name` | [5,11) | (모공축소) | 고민/목적 후보 | '축소' — 효과 방향. | paren |
| `/categories/10/items/6/name` | [5,10) | (목주름) | 부위 후보, 고민 후보 |  | paren |

### 자동 후보 (정규식 일치분뿐 — 의미 해석 아님)

| Pointer | 구간 | 패턴 | 일치 구절 | 검토 |
|---|---|---|---|---|
| `/categories/10/items/0/name` | [4,10) | paren | (전체얼굴) | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/10/items/0/name` | [5,9) | kw | 전체얼굴 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/10/items/0/unit` | [0,2) | num_unit | 1회 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/10/items/1/name` | [4,10) | paren | (전체얼굴) | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/10/items/1/name` | [5,9) | kw | 전체얼굴 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/10/items/1/unit` | [0,2) | num_unit | 1회 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/10/items/2/name` | [6,12) | paren | (전체얼굴) | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/10/items/2/name` | [7,11) | kw | 전체얼굴 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/10/items/2/unit` | [0,2) | num_unit | 1회 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/10/items/3/name` | [4,10) | paren | (전체얼굴) | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/10/items/3/name` | [5,9) | kw | 전체얼굴 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/10/items/3/unit` | [0,2) | num_unit | 1회 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/10/items/4/name` | [5,13) | paren | (여드름 흉터) | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/10/items/4/unit` | [0,2) | num_unit | 1회 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/10/items/5/name` | [5,11) | paren | (모공축소) | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/10/items/5/name` | [8,10) | kw | 축소 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/10/items/5/unit` | [0,2) | num_unit | 1회 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/10/items/6/name` | [5,10) | paren | (목주름) | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/10/items/6/unit` | [0,2) | num_unit | 1회 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |

### 형태소 (Kiwi 원시 결과 — 도메인 정답 아님. `form/tag[start,end)`)

| Pointer | 원문 값 | 토큰 |
|---|---|---|
| `/categories/10/id` | M11 | 제외: 카테고리 ID(Mn) — 식별자 |
| `/categories/10/name` | 니들RF | 니들/NNP[0,2) RF/SL[2,4) |
| `/categories/10/items/0/name` | 시크릿 (전체얼굴) | 시크릿/NNP[0,3) (/SSO[4,5) 전체/NNG[5,7) 얼굴/NNG[7,9) )/SSC[9,10) |
| `/categories/10/items/0/unit` | 1회 | 1/SN[0,1) 회/NNB[1,2) |
| `/categories/10/items/1/name` | 인피니 (전체얼굴) | 인피니/NNP[0,3) (/SSO[4,5) 전체/NNG[5,7) 얼굴/NNG[7,9) )/SSC[9,10) |
| `/categories/10/items/1/unit` | 1회 | 1/SN[0,1) 회/NNB[1,2) |
| `/categories/10/items/2/name` | 모피어스8 (전체얼굴) | 모피어스/NNG[0,4) 8/SN[4,5) (/SSO[6,7) 전체/NNG[7,9) 얼굴/NNG[9,11) )/SSC[11,12) |
| `/categories/10/items/2/unit` | 1회 | 1/SN[0,1) 회/NNB[1,2) |
| `/categories/10/items/3/name` | 포텐자 (전체얼굴) | 포텐자/NNP[0,3) (/SSO[4,5) 전체/NNG[5,7) 얼굴/NNG[7,9) )/SSC[9,10) |
| `/categories/10/items/3/unit` | 1회 | 1/SN[0,1) 회/NNB[1,2) |
| `/categories/10/items/4/name` | 니들RF (여드름 흉터) | 니들/NNP[0,2) RF/SL[2,4) (/SSO[5,6) 여드름/NNG[6,9) 흉터/NNG[10,12) )/SSC[12,13) |
| `/categories/10/items/4/unit` | 1회 | 1/SN[0,1) 회/NNB[1,2) |
| `/categories/10/items/5/name` | 니들RF (모공축소) | 니들/NNP[0,2) RF/SL[2,4) (/SSO[5,6) 모공/NNG[6,8) 축소/NNG[8,10) )/SSC[10,11) |
| `/categories/10/items/5/unit` | 1회 | 1/SN[0,1) 회/NNB[1,2) |
| `/categories/10/items/6/name` | 니들RF (목주름) | 니들/NNP[0,2) RF/SL[2,4) (/SSO[5,6) 목주름/NNP[6,9) )/SSC[9,10) |
| `/categories/10/items/6/unit` | 1회 | 1/SN[0,1) 회/NNB[1,2) |

### 미결 (이 구획)

| ID | 상태 | Pointer | 내용 |
|---|---|---|---|
| B-S11-1 | B | `/categories/10/items/4/name`, `/categories/10/items/5/name`, `/categories/10/items/6/name` | 고민 축 항목의 장비·적용 범위가 없다. |
