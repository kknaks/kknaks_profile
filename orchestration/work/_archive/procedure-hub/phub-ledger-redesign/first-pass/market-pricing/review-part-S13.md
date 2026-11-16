# S13 — M13 플라즈마 (6항목)

[← review.md](review.md) · 소유 말단 32 · 직접 읽기 ○ · 마지막 읽은 Pointer `/categories/12/items/5/high`

## S13

### 상위 문맥 (S00 소유, 공동 참조)

- `/currency` = `KRW` · `/updated` = `2026-07-26` · `/note` = `한국 시장 참고 가격 범위. 클리닉/지역/의사에 따라 상이. 정가 아닌 시장 범위.`

### 원문 값 — 카테고리

| Pointer | 원본 컬럼명 | 자료형 | 원문 값 |
|---|---|---|---|
| `/categories/12/id` | `id` | string | `M13` |
| `/categories/12/name` | `name` | string | `플라즈마` |
| `/categories/12/items` | `items` | array[6] of object | (아래 표) |

### 원문 값 — `items` (원본 순서, 각 값의 Pointer = 항목 Pointer + `/` + 컬럼명)

자료형: `name`·`unit` string, `low`·`mid`·`high` integer.

| 항목 Pointer | `name` | `unit` | `low` | `mid` | `high` |
|---|---|---|---|---|---|
| `/categories/12/items/0` | 플라즈마 리프팅 (전체얼굴) | 1회 | 100000 | 200000 | 400000 |
| `/categories/12/items/1` | 플라즈마 (눈가 주름) | 1회 | 80000 | 150000 | 300000 |
| `/categories/12/items/2` | 플라즈마 (여드름 치료) | 1회 | 50000 | 100000 | 200000 |
| `/categories/12/items/3` | 플라즈마 (쥐젖/사마귀 1개) | 1개 | 10000 | 20000 | 50000 |
| `/categories/12/items/4` | 플라즈마 (눈꺼풀 처짐 비수술) | 1회 | 200000 | 400000 | 700000 |
| `/categories/12/items/5` | 플라즈마 샤워 (진정/재생) | 1회 | 30000 | 60000 | 120000 |

### 잠정 관찰 (원문 아님 — 근거 Pointer 와 상태)

| 근거 Pointer | 관찰 | 상태 |
|---|---|---|
| `/categories/12/items/0/name` | 모든 항목이 '플라즈마' 로 시작. 괄호는 부위·범위(전체얼굴), 부위+고민(눈가 주름), 목적(여드름 치료), 대상 병변+수량(쥐젖/사마귀 1개), 고민+시술방식(눈꺼풀 처짐 비수술), 목적(진정/재생)로 역할이 섞임. | P |
| `/categories/12/items/3/name` | '플라즈마 (쥐젖/사마귀 1개)' unit '1개' — 병변 1개 기준. '/' 는 두 병변 대안 또는 나열 — 확정 불가. | P |
| `/categories/12/items/4/name` | '(눈꺼풀 처짐 비수술)' — '비수술' 은 수술이 아님을 나타내는 부정 접두 표현(비-). 형태소상 '비/XPN + 수술/NNG'. | P |
| `/categories/12/items/5/name` | '플라즈마 샤워 (진정/재생)' — '샤워' 가 기법명 일부. 괄호는 효과/목적 두 가지. | P |
| `/categories/12/items/0/low` | 6항목 모두 low < mid < high. | P |

### 직접 읽기로 수집한 표현 (문자열 값 코드포인트 구간 [start,end))

| Pointer | 구간 | 원문 구절 | 탐색 관점(확정 분류 아님) | 메모 | 자동 패턴 동일 구간 |
|---|---|---|---|---|---|
| `/categories/12/items/0/name` | [0,8) | 플라즈마 리프팅 | 시술명 후보 |  | 없음(패턴 밖) |
| `/categories/12/items/0/name` | [9,15) | (전체얼굴) | 적용 범위, 부위 후보 |  | paren |
| `/categories/12/items/1/name` | [5,12) | (눈가 주름) | 부위 후보, 고민 후보 |  | paren |
| `/categories/12/items/2/name` | [5,13) | (여드름 치료) | 고민/목적 후보 |  | paren |
| `/categories/12/items/3/name` | [5,16) | (쥐젖/사마귀 1개) | 병변 후보, '/' 연결, 수량·단위 |  | paren |
| `/categories/12/items/3/name` | [6,12) | 쥐젖/사마귀 | 병변 후보, '/' 연결 |  | slash |
| `/categories/12/items/4/name` | [5,17) | (눈꺼풀 처짐 비수술) | 부위 후보, 고민 후보, 부정 |  | paren |
| `/categories/12/items/4/name` | [6,12) | 눈꺼풀 처짐 | 부위 후보, 고민 후보 |  | 없음(패턴 밖) |
| `/categories/12/items/4/name` | [13,16) | 비수술 | 부정, 시술 방식 | '비-' 부정 접두. | kw |
| `/categories/12/items/5/name` | [0,7) | 플라즈마 샤워 | 시술명 후보 |  | 없음(패턴 밖) |
| `/categories/12/items/5/name` | [8,15) | (진정/재생) | 효과/목적 후보, '/' 연결 |  | paren |

### 자동 후보 (정규식 일치분뿐 — 의미 해석 아님)

| Pointer | 구간 | 패턴 | 일치 구절 | 검토 |
|---|---|---|---|---|
| `/categories/12/items/0/name` | [9,15) | paren | (전체얼굴) | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/12/items/0/name` | [10,14) | kw | 전체얼굴 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/12/items/0/unit` | [0,2) | num_unit | 1회 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/12/items/1/name` | [5,12) | paren | (눈가 주름) | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/12/items/1/unit` | [0,2) | num_unit | 1회 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/12/items/2/name` | [5,13) | paren | (여드름 치료) | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/12/items/2/unit` | [0,2) | num_unit | 1회 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/12/items/3/name` | [5,16) | paren | (쥐젖/사마귀 1개) | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/12/items/3/name` | [13,15) | num_unit | 1개 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/12/items/3/name` | [6,12) | slash | 쥐젖/사마귀 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/12/items/3/unit` | [0,2) | num_unit | 1개 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/12/items/4/name` | [5,17) | paren | (눈꺼풀 처짐 비수술) | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/12/items/4/name` | [13,16) | kw | 비수술 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/12/items/4/unit` | [0,2) | num_unit | 1회 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/12/items/5/name` | [8,15) | paren | (진정/재생) | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/12/items/5/name` | [9,14) | slash | 진정/재생 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/12/items/5/unit` | [0,2) | num_unit | 1회 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |

### 형태소 (Kiwi 원시 결과 — 도메인 정답 아님. `form/tag[start,end)`)

| Pointer | 원문 값 | 토큰 |
|---|---|---|
| `/categories/12/id` | M13 | 제외: 카테고리 ID(Mn) — 식별자 |
| `/categories/12/name` | 플라즈마 | 플라즈마/NNG[0,4) |
| `/categories/12/items/0/name` | 플라즈마 리프팅 (전체얼굴) | 플라즈마/NNG[0,4) 리프팅/NNG[5,8) (/SSO[9,10) 전체/NNG[10,12) 얼굴/NNG[12,14) )/SSC[14,15) |
| `/categories/12/items/0/unit` | 1회 | 1/SN[0,1) 회/NNB[1,2) |
| `/categories/12/items/1/name` | 플라즈마 (눈가 주름) | 플라즈마/NNG[0,4) (/SSO[5,6) 눈가/NNG[6,8) 주름/NNG[9,11) )/SSC[11,12) |
| `/categories/12/items/1/unit` | 1회 | 1/SN[0,1) 회/NNB[1,2) |
| `/categories/12/items/2/name` | 플라즈마 (여드름 치료) | 플라즈마/NNG[0,4) (/SSO[5,6) 여드름/NNG[6,9) 치료/NNG[10,12) )/SSC[12,13) |
| `/categories/12/items/2/unit` | 1회 | 1/SN[0,1) 회/NNB[1,2) |
| `/categories/12/items/3/name` | 플라즈마 (쥐젖/사마귀 1개) | 플라즈마/NNG[0,4) (/SSO[5,6) 쥐젖/NNG[6,8) //SP[8,9) 사마귀/NNG[9,12) 1/SN[13,14) 개/NNB[14,15) )/SSC[15,16) |
| `/categories/12/items/3/unit` | 1개 | 1/SN[0,1) 개/NNB[1,2) |
| `/categories/12/items/4/name` | 플라즈마 (눈꺼풀 처짐 비수술) | 플라즈마/NNG[0,4) (/SSO[5,6) 눈꺼풀/NNG[6,9) 처지/VV[10,12) ᆷ/ETN[11,12) 비/XPN[13,14) 수술/NNG[14,16) )/SSC[16,17) |
| `/categories/12/items/4/unit` | 1회 | 1/SN[0,1) 회/NNB[1,2) |
| `/categories/12/items/5/name` | 플라즈마 샤워 (진정/재생) | 플라즈마/NNG[0,4) 샤워/NNG[5,7) (/SSO[8,9) 진정/NNG[9,11) //SP[11,12) 재생/NNG[12,14) )/SSC[14,15) |
| `/categories/12/items/5/unit` | 1회 | 1/SN[0,1) 회/NNB[1,2) |

### 미결 (이 구획)

| ID | 상태 | Pointer | 내용 |
|---|---|---|---|
| P-S13-1 | P | `/categories/12/items/4/name` | '비수술' 이 수술 대비 방식을 말하는 부정 표현이라는 것은 잠정. 수식 대상(시술 전체)은 원문 위치로만 보존. |
| B-S13-1 | B | `/categories/12/items/1/name`, `/categories/12/items/2/name`, `/categories/12/items/4/name` | 부위·범위 크기 없이 고민·목적만 있는 항목의 시술 범위가 없다. |
