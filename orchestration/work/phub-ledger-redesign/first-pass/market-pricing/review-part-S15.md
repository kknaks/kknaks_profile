# S15 — M15 메디컬스킨케어 (7항목)

[← review.md](review.md) · 소유 말단 37 · 직접 읽기 ○ · 마지막 읽은 Pointer `/categories/14/items/6/high`

## S15

### 상위 문맥 (S00 소유, 공동 참조)

- `/currency` = `KRW` · `/updated` = `2026-07-26` · `/note` = `한국 시장 참고 가격 범위. 클리닉/지역/의사에 따라 상이. 정가 아닌 시장 범위.`

### 원문 값 — 카테고리

| Pointer | 원본 컬럼명 | 자료형 | 원문 값 |
|---|---|---|---|
| `/categories/14/id` | `id` | string | `M15` |
| `/categories/14/name` | `name` | string | `메디컬스킨케어` |
| `/categories/14/items` | `items` | array[7] of object | (아래 표) |

### 원문 값 — `items` (원본 순서, 각 값의 Pointer = 항목 Pointer + `/` + 컬럼명)

자료형: `name`·`unit` string, `low`·`mid`·`high` integer.

| 항목 Pointer | `name` | `unit` | `low` | `mid` | `high` |
|---|---|---|---|---|---|
| `/categories/14/items/0` | 아쿠아필 (전체얼굴) | 1회 | 50000 | 100000 | 200000 |
| `/categories/14/items/1` | 화학 박피 (살리실산/글리콜산) | 1회 | 30000 | 60000 | 120000 |
| `/categories/14/items/2` | LDM 초음파 관리 | 1회 | 50000 | 100000 | 180000 |
| `/categories/14/items/3` | LED 광선치료 (전체얼굴) | 1회 | 20000 | 50000 | 100000 |
| `/categories/14/items/4` | 이온토포레시스 (비타민C) | 1회 | 30000 | 60000 | 120000 |
| `/categories/14/items/5` | 진정관리 (시술 후 재생팩) | 1회 | 30000 | 50000 | 100000 |
| `/categories/14/items/6` | 프리미엄 스킨케어 (풀코스) | 1회 | 100000 | 200000 | 400000 |

### 잠정 관찰 (원문 아님 — 근거 Pointer 와 상태)

| 근거 Pointer | 관찰 | 상태 |
|---|---|---|
| `/categories/14/items/1/name` | '화학 박피 (살리실산/글리콜산)' — 괄호가 성분 두 개를 '/' 로. 대안(둘 중 하나) 해석이 README 규칙과 맞으나 원문 문맥만으로 확정하지 않음. 농도 없음. | P |
| `/categories/14/items/2/name` | 'LDM 초음파 관리' — 괄호·범위 없음. 'LDM' 영문 약어 풀이 없음. | B |
| `/categories/14/items/4/name` | '이온토포레시스 (비타민C)' — 괄호가 성분. | P |
| `/categories/14/items/5/name` | '진정관리 (시술 후 재생팩)' — '시술 후' 는 시간 조건(다른 시술 뒤). 어떤 시술 뒤인지·얼마 뒤인지 원문에 없음. 다른 항목을 가리키는 참조 표현일 수 있음. | P |
| `/categories/14/items/6/name` | '프리미엄 스킨케어 (풀코스)' — '프리미엄' 등급 수식, '풀코스' 구성 범위. 구성 내용 없음. | B |
| `/categories/14/items/0/low` | 7항목 모두 low < mid < high. | P |

### 직접 읽기로 수집한 표현 (문자열 값 코드포인트 구간 [start,end))

| Pointer | 구간 | 원문 구절 | 탐색 관점(확정 분류 아님) | 메모 | 자동 패턴 동일 구간 |
|---|---|---|---|---|---|
| `/categories/14/name` | [0,7) | 메디컬스킨케어 | 분류명, 외래어 |  | 없음(패턴 밖) |
| `/categories/14/items/0/name` | [0,4) | 아쿠아필 | 시술명/장비명 후보 |  | 없음(패턴 밖) |
| `/categories/14/items/0/name` | [5,11) | (전체얼굴) | 적용 범위, 부위 후보 |  | paren |
| `/categories/14/items/1/name` | [0,5) | 화학 박피 | 시술명 후보 |  | 없음(패턴 밖) |
| `/categories/14/items/1/name` | [6,17) | (살리실산/글리콜산) | 성분 후보, '/' 연결 |  | paren |
| `/categories/14/items/2/name` | [0,10) | LDM 초음파 관리 | 시술명 후보, 영문 약어 |  | 없음(패턴 밖) |
| `/categories/14/items/3/name` | [0,8) | LED 광선치료 | 시술명 후보, 영문 약어 |  | 없음(패턴 밖) |
| `/categories/14/items/3/name` | [9,15) | (전체얼굴) | 적용 범위, 부위 후보 |  | paren |
| `/categories/14/items/4/name` | [0,7) | 이온토포레시스 | 기법명 후보 |  | 없음(패턴 밖) |
| `/categories/14/items/4/name` | [8,14) | (비타민C) | 성분 후보, 영한 혼합 |  | paren |
| `/categories/14/items/5/name` | [0,4) | 진정관리 | 시술명/목적 후보 |  | 없음(패턴 밖) |
| `/categories/14/items/5/name` | [5,15) | (시술 후 재생팩) | 시간 조건, 참조 |  | paren |
| `/categories/14/items/5/name` | [6,10) | 시술 후 | 시간 조건, 참조 | '후' — 선후 관계. | kw |
| `/categories/14/items/6/name` | [0,9) | 프리미엄 스킨케어 | 등급 수식, 시술명 후보 |  | 없음(패턴 밖) |
| `/categories/14/items/6/name` | [10,15) | (풀코스) | 구성 범위 |  | paren |

### 자동 후보 (정규식 일치분뿐 — 의미 해석 아님)

| Pointer | 구간 | 패턴 | 일치 구절 | 검토 |
|---|---|---|---|---|
| `/categories/14/items/0/name` | [5,11) | paren | (전체얼굴) | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/14/items/0/name` | [6,10) | kw | 전체얼굴 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/14/items/0/unit` | [0,2) | num_unit | 1회 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/14/items/1/name` | [6,17) | paren | (살리실산/글리콜산) | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/14/items/1/name` | [7,16) | slash | 살리실산/글리콜산 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/14/items/1/unit` | [0,2) | num_unit | 1회 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/14/items/2/unit` | [0,2) | num_unit | 1회 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/14/items/3/name` | [9,15) | paren | (전체얼굴) | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/14/items/3/name` | [10,14) | kw | 전체얼굴 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/14/items/3/unit` | [0,2) | num_unit | 1회 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/14/items/4/name` | [8,14) | paren | (비타민C) | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/14/items/4/unit` | [0,2) | num_unit | 1회 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/14/items/5/name` | [5,15) | paren | (시술 후 재생팩) | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/14/items/5/name` | [6,10) | kw | 시술 후 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/14/items/5/unit` | [0,2) | num_unit | 1회 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/14/items/6/name` | [10,15) | paren | (풀코스) | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/14/items/6/name` | [0,4) | kw | 프리미엄 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/14/items/6/name` | [11,14) | kw | 풀코스 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/14/items/6/unit` | [0,2) | num_unit | 1회 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |

### 형태소 (Kiwi 원시 결과 — 도메인 정답 아님. `form/tag[start,end)`)

| Pointer | 원문 값 | 토큰 |
|---|---|---|
| `/categories/14/id` | M15 | 제외: 카테고리 ID(Mn) — 식별자 |
| `/categories/14/name` | 메디컬스킨케어 | 메디컬/NNG[0,3) 스킨/NNG[3,5) 케어/NNG[5,7) |
| `/categories/14/items/0/name` | 아쿠아필 (전체얼굴) | 아쿠아필/NNP[0,4) (/SSO[5,6) 전체/NNG[6,8) 얼굴/NNG[8,10) )/SSC[10,11) |
| `/categories/14/items/0/unit` | 1회 | 1/SN[0,1) 회/NNB[1,2) |
| `/categories/14/items/1/name` | 화학 박피 (살리실산/글리콜산) | 화학/NNG[0,2) 박피/NNP[3,5) (/SSO[6,7) 살리실산/NNP[7,11) //SP[11,12) 글리콜산/NNP[12,16) )/SSC[16,17) |
| `/categories/14/items/1/unit` | 1회 | 1/SN[0,1) 회/NNB[1,2) |
| `/categories/14/items/2/name` | LDM 초음파 관리 | LDM/SL[0,3) 초음파/NNG[4,7) 관리/NNG[8,10) |
| `/categories/14/items/2/unit` | 1회 | 1/SN[0,1) 회/NNB[1,2) |
| `/categories/14/items/3/name` | LED 광선치료 (전체얼굴) | LED/SL[0,3) 광선치료/NNP[4,8) (/SSO[9,10) 전체/NNG[10,12) 얼굴/NNG[12,14) )/SSC[14,15) |
| `/categories/14/items/3/unit` | 1회 | 1/SN[0,1) 회/NNB[1,2) |
| `/categories/14/items/4/name` | 이온토포레시스 (비타민C) | 이온토포레시스/NNP[0,7) (/SSO[8,9) 비타민C/NNP[9,13) )/SSC[13,14) |
| `/categories/14/items/4/unit` | 1회 | 1/SN[0,1) 회/NNB[1,2) |
| `/categories/14/items/5/name` | 진정관리 (시술 후 재생팩) | 진정관리/NNP[0,4) (/SSO[5,6) 시술/NNG[6,8) 후/NNG[9,10) 재생/NNG[11,13) 팩/NNG[13,14) )/SSC[14,15) |
| `/categories/14/items/5/unit` | 1회 | 1/SN[0,1) 회/NNB[1,2) |
| `/categories/14/items/6/name` | 프리미엄 스킨케어 (풀코스) | 프리미엄/NNG[0,4) 스킨케어/NNG[5,9) (/SSO[10,11) 풀코스/NNG[11,14) )/SSC[14,15) |
| `/categories/14/items/6/unit` | 1회 | 1/SN[0,1) 회/NNB[1,2) |

### 미결 (이 구획)

| ID | 상태 | Pointer | 내용 |
|---|---|---|---|
| F-S15-1 | F | `/categories/14/items/5/name` | '시술 후' 가 가리키는 시술이 원문에 없다 — 참조 표현과 위치만 보존, 연결은 후속. |
| B-S15-1 | B | `/categories/14/items/6/name`, `/categories/14/items/2/name` | '풀코스' 구성·'LDM' 풀이 없음. |
| B-S15-2 | B | `/categories/14/items/1/name` | 박피 성분 농도·범위 없음. |
