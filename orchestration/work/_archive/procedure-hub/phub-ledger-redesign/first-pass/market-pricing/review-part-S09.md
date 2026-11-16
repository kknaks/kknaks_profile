# S09 — M9 에너지기기(HIFU/RF) (8항목)

[← review.md](review.md) · 소유 말단 42 · 직접 읽기 ○ · 마지막 읽은 Pointer `/categories/8/items/7/high`

## S09

### 상위 문맥 (S00 소유, 공동 참조)

- `/currency` = `KRW` · `/updated` = `2026-07-26` · `/note` = `한국 시장 참고 가격 범위. 클리닉/지역/의사에 따라 상이. 정가 아닌 시장 범위.`

### 원문 값 — 카테고리

| Pointer | 원본 컬럼명 | 자료형 | 원문 값 |
|---|---|---|---|
| `/categories/8/id` | `id` | string | `M9` |
| `/categories/8/name` | `name` | string | `에너지기기(HIFU/RF)` |
| `/categories/8/items` | `items` | array[8] of object | (아래 표) |

### 원문 값 — `items` (원본 순서, 각 값의 Pointer = 항목 Pointer + `/` + 컬럼명)

자료형: `name`·`unit` string, `low`·`mid`·`high` integer.

| 항목 Pointer | `name` | `unit` | `low` | `mid` | `high` |
|---|---|---|---|---|---|
| `/categories/8/items/0` | 울쎄라 (풀페이스) | 1회 | 1000000 | 2000000 | 4000000 |
| `/categories/8/items/1` | 울쎄라 (턱라인) | 1회 | 500000 | 1000000 | 2000000 |
| `/categories/8/items/2` | 슈링크 유니버스 (풀페이스) | 1회 | 200000 | 400000 | 800000 |
| `/categories/8/items/3` | 슈링크 유니버스 (턱라인) | 1회 | 100000 | 200000 | 400000 |
| `/categories/8/items/4` | 더블로골드 (풀페이스) | 1회 | 200000 | 400000 | 700000 |
| `/categories/8/items/5` | 써마지 FLX (풀페이스 900샷) | 900샷 | 1500000 | 2500000 | 4000000 |
| `/categories/8/items/6` | 써마지 FLX (눈가 450샷) | 450샷 | 600000 | 1000000 | 1800000 |
| `/categories/8/items/7` | 인모드 (풀페이스) | 1회 | 200000 | 400000 | 700000 |

### 잠정 관찰 (원문 아님 — 근거 Pointer 와 상태)

| 근거 Pointer | 관찰 | 상태 |
|---|---|---|
| `/categories/8/name` | '에너지기기(HIFU/RF)' — 괄호 안 '/' 로 두 기술 계열. 각 항목이 HIFU·RF 중 어느 쪽인지 원문에 없음(항목에 계열 표시 없음). | B |
| `/categories/8/items/0/name` | 장비명 후보(울쎄라·슈링크 유니버스·더블로골드·써마지 FLX·인모드) + 괄호 적용 범위(풀페이스·턱라인·눈가). 이 카테고리는 '전체얼굴' 대신 '풀페이스' 를 씀. | P |
| `/categories/8/items/5/name` | '써마지 FLX (풀페이스 900샷)' unit '900샷', '(눈가 450샷)' unit '450샷' — 샷 수가 가격 기준. 다른 장비 항목(unit '1회')은 샷 수 없음. | P |
| `/categories/8/items/0/low` | 8항목 모두 low < mid < high. | P |

### 직접 읽기로 수집한 표현 (문자열 값 코드포인트 구간 [start,end))

| Pointer | 구간 | 원문 구절 | 탐색 관점(확정 분류 아님) | 메모 | 자동 패턴 동일 구간 |
|---|---|---|---|---|---|
| `/categories/8/name` | [0,14) | 에너지기기(HIFU/RF) | 분류명, '/' 연결, 영문 약어 |  | 없음(패턴 밖) |
| `/categories/8/items/0/name` | [0,3) | 울쎄라 | 장비명 후보 |  | 없음(패턴 밖) |
| `/categories/8/items/0/name` | [4,10) | (풀페이스) | 적용 범위, 부위 후보 |  | paren |
| `/categories/8/items/1/name` | [0,3) | 울쎄라 | 장비명 후보 |  | 없음(패턴 밖) |
| `/categories/8/items/1/name` | [4,9) | (턱라인) | 부위 후보 |  | paren |
| `/categories/8/items/2/name` | [0,8) | 슈링크 유니버스 | 장비명 후보 |  | 없음(패턴 밖) |
| `/categories/8/items/2/name` | [9,15) | (풀페이스) | 적용 범위, 부위 후보 |  | paren |
| `/categories/8/items/3/name` | [0,8) | 슈링크 유니버스 | 장비명 후보 |  | 없음(패턴 밖) |
| `/categories/8/items/3/name` | [9,14) | (턱라인) | 부위 후보 |  | paren |
| `/categories/8/items/4/name` | [0,5) | 더블로골드 | 장비명 후보 |  | 없음(패턴 밖) |
| `/categories/8/items/4/name` | [6,12) | (풀페이스) | 적용 범위, 부위 후보 |  | paren |
| `/categories/8/items/5/name` | [0,7) | 써마지 FLX | 장비명 후보, 영한 혼합 |  | 없음(패턴 밖) |
| `/categories/8/items/5/name` | [8,19) | (풀페이스 900샷) | 적용 범위, 수량·단위 |  | paren |
| `/categories/8/items/6/name` | [0,7) | 써마지 FLX | 장비명 후보, 영한 혼합 |  | 없음(패턴 밖) |
| `/categories/8/items/6/name` | [8,17) | (눈가 450샷) | 부위 후보, 수량·단위 |  | paren |
| `/categories/8/items/7/name` | [0,3) | 인모드 | 장비명 후보 |  | 없음(패턴 밖) |
| `/categories/8/items/7/name` | [4,10) | (풀페이스) | 적용 범위, 부위 후보 |  | paren |

### 자동 후보 (정규식 일치분뿐 — 의미 해석 아님)

| Pointer | 구간 | 패턴 | 일치 구절 | 검토 |
|---|---|---|---|---|
| `/categories/8/name` | [5,14) | paren | (HIFU/RF) | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/8/name` | [6,13) | slash | HIFU/RF | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/8/items/0/name` | [4,10) | paren | (풀페이스) | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/8/items/0/name` | [5,9) | kw | 풀페이스 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/8/items/0/unit` | [0,2) | num_unit | 1회 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/8/items/1/name` | [4,9) | paren | (턱라인) | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/8/items/1/unit` | [0,2) | num_unit | 1회 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/8/items/2/name` | [9,15) | paren | (풀페이스) | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/8/items/2/name` | [10,14) | kw | 풀페이스 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/8/items/2/unit` | [0,2) | num_unit | 1회 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/8/items/3/name` | [9,14) | paren | (턱라인) | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/8/items/3/unit` | [0,2) | num_unit | 1회 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/8/items/4/name` | [6,12) | paren | (풀페이스) | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/8/items/4/name` | [7,11) | kw | 풀페이스 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/8/items/4/unit` | [0,2) | num_unit | 1회 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/8/items/5/name` | [8,19) | paren | (풀페이스 900샷) | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/8/items/5/name` | [14,18) | num_unit | 900샷 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/8/items/5/name` | [9,13) | kw | 풀페이스 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/8/items/5/unit` | [0,4) | num_unit | 900샷 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/8/items/6/name` | [8,17) | paren | (눈가 450샷) | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/8/items/6/name` | [12,16) | num_unit | 450샷 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/8/items/6/unit` | [0,4) | num_unit | 450샷 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/8/items/7/name` | [4,10) | paren | (풀페이스) | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/8/items/7/name` | [5,9) | kw | 풀페이스 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/8/items/7/unit` | [0,2) | num_unit | 1회 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |

### 형태소 (Kiwi 원시 결과 — 도메인 정답 아님. `form/tag[start,end)`)

| Pointer | 원문 값 | 토큰 |
|---|---|---|
| `/categories/8/id` | M9 | 제외: 카테고리 ID(Mn) — 식별자 |
| `/categories/8/name` | 에너지기기(HIFU/RF) | 에너지/NNG[0,3) 기기/NNG[3,5) (/SSO[5,6) HIFU/SL[6,10) //SP[10,11) RF/SL[11,13) )/SSC[13,14) |
| `/categories/8/items/0/name` | 울쎄라 (풀페이스) | 울쎄라/NNP[0,3) (/SSO[4,5) 풀페이스/NNP[5,9) )/SSC[9,10) |
| `/categories/8/items/0/unit` | 1회 | 1/SN[0,1) 회/NNB[1,2) |
| `/categories/8/items/1/name` | 울쎄라 (턱라인) | 울쎄라/NNP[0,3) (/SSO[4,5) 턱라인/NNP[5,8) )/SSC[8,9) |
| `/categories/8/items/1/unit` | 1회 | 1/SN[0,1) 회/NNB[1,2) |
| `/categories/8/items/2/name` | 슈링크 유니버스 (풀페이스) | 슈링크/NNP[0,3) 유니버스/NNG[4,8) (/SSO[9,10) 풀페이스/NNP[10,14) )/SSC[14,15) |
| `/categories/8/items/2/unit` | 1회 | 1/SN[0,1) 회/NNB[1,2) |
| `/categories/8/items/3/name` | 슈링크 유니버스 (턱라인) | 슈링크/NNP[0,3) 유니버스/NNG[4,8) (/SSO[9,10) 턱/NNG[10,11) 라인/NNG[11,13) )/SSC[13,14) |
| `/categories/8/items/3/unit` | 1회 | 1/SN[0,1) 회/NNB[1,2) |
| `/categories/8/items/4/name` | 더블로골드 (풀페이스) | 더블로골드/NNP[0,5) (/SSO[6,7) 풀페이스/NNP[7,11) )/SSC[11,12) |
| `/categories/8/items/4/unit` | 1회 | 1/SN[0,1) 회/NNB[1,2) |
| `/categories/8/items/5/name` | 써마지 FLX (풀페이스 900샷) | 써마지/NNG[0,3) FLX/SL[4,7) (/SSO[8,9) 풀페이스/NNP[9,13) 900/SN[14,17) 샷/NNG[17,18) )/SSC[18,19) |
| `/categories/8/items/5/unit` | 900샷 | 900/SN[0,3) 샷/NNG[3,4) |
| `/categories/8/items/6/name` | 써마지 FLX (눈가 450샷) | 써마지/NNP[0,3) FLX/SL[4,7) (/SSO[8,9) 눈가/NNG[9,11) 450/SN[12,15) 샷/NNG[15,16) )/SSC[16,17) |
| `/categories/8/items/6/unit` | 450샷 | 450/SN[0,3) 샷/NNG[3,4) |
| `/categories/8/items/7/name` | 인모드 (풀페이스) | 인모드/NNP[0,3) (/SSO[4,5) 풀페이스/NNP[5,9) )/SSC[9,10) |
| `/categories/8/items/7/unit` | 1회 | 1/SN[0,1) 회/NNB[1,2) |

### 미결 (이 구획)

| ID | 상태 | Pointer | 내용 |
|---|---|---|---|
| B-S09-1 | B | `/categories/8/name` | 항목별 HIFU/RF 계열 표시가 없다. |
| B-S09-2 | B | `/categories/8/items/0/unit` | unit '1회' 장비 항목들의 샷 수가 없다(써마지만 샷 수 있음). |
