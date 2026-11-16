# S17 — M17 줄기세포치료 (6항목)

[← review.md](review.md) · 소유 말단 32 · 직접 읽기 ○ · 마지막 읽은 Pointer `/categories/16/items/5/high`

## S17

### 상위 문맥 (S00 소유, 공동 참조)

- `/currency` = `KRW` · `/updated` = `2026-07-26` · `/note` = `한국 시장 참고 가격 범위. 클리닉/지역/의사에 따라 상이. 정가 아닌 시장 범위.`

### 원문 값 — 카테고리

| Pointer | 원본 컬럼명 | 자료형 | 원문 값 |
|---|---|---|---|
| `/categories/16/id` | `id` | string | `M17` |
| `/categories/16/name` | `name` | string | `줄기세포치료` |
| `/categories/16/items` | `items` | array[6] of object | (아래 표) |

### 원문 값 — `items` (원본 순서, 각 값의 Pointer = 항목 Pointer + `/` + 컬럼명)

자료형: `name`·`unit` string, `low`·`mid`·`high` integer.

| 항목 Pointer | `name` | `unit` | `low` | `mid` | `high` |
|---|---|---|---|---|---|
| `/categories/16/items/0` | 줄기세포 배양액 주입 (전체얼굴) | 1회 | 300000 | 600000 | 1200000 |
| `/categories/16/items/1` | 줄기세포 엑소좀 (전체얼굴) | 1회 | 400000 | 800000 | 1500000 |
| `/categories/16/items/2` | 줄기세포 + MTS (전체얼굴) | 1회 | 350000 | 700000 | 1300000 |
| `/categories/16/items/3` | 줄기세포 두피치료 (탈모) | 1회 | 300000 | 600000 | 1000000 |
| `/categories/16/items/4` | 줄기세포 관절치료 | 1회 | 500000 | 1000000 | 2000000 |
| `/categories/16/items/5` | 줄기세포 3회 패키지 (전체얼굴) | 3회 | 800000 | 1500000 | 3000000 |

### 잠정 관찰 (원문 아님 — 근거 Pointer 와 상태)

| 근거 Pointer | 관찰 | 상태 |
|---|---|---|
| `/categories/16/items/0/name` | 모든 항목이 '줄기세포' 로 시작. '배양액 주입'·'엑소좀'·'+ MTS'·'두피치료'·'관절치료'·'3회 패키지' 로 구분. '줄기세포 엑소좀' 은 M5 '엑소좀 (전체얼굴)' 과 다른 항목으로 존재(가격 다름). | P |
| `/categories/16/items/2/name` | '줄기세포 + MTS (전체얼굴)' — '+' 조합. M5·M12 의 'PRP + MTS' 류와 같은 조합 표기 방식. | P |
| `/categories/16/items/4/name` | '줄기세포 관절치료' — 미용 시술이 아닌 관절 적응증 후보. 부위·범위 없음. | B |
| `/categories/16/items/5/name` | '줄기세포 3회 패키지 (전체얼굴)' unit '3회' — 패키지에 포함되는 줄기세포 시술 종류(배양액·엑소좀 등)가 원문에 없음. | B |
| `/categories/16/items/0/low` | 6항목 모두 low < mid < high. | P |

### 직접 읽기로 수집한 표현 (문자열 값 코드포인트 구간 [start,end))

| Pointer | 구간 | 원문 구절 | 탐색 관점(확정 분류 아님) | 메모 | 자동 패턴 동일 구간 |
|---|---|---|---|---|---|
| `/categories/16/items/0/name` | [0,11) | 줄기세포 배양액 주입 | 성분 후보, 시술 행위 후보 |  | 없음(패턴 밖) |
| `/categories/16/items/0/name` | [12,18) | (전체얼굴) | 적용 범위, 부위 후보 |  | paren |
| `/categories/16/items/1/name` | [0,8) | 줄기세포 엑소좀 | 성분 후보, 시술명 후보 |  | 없음(패턴 밖) |
| `/categories/16/items/1/name` | [9,15) | (전체얼굴) | 적용 범위, 부위 후보 |  | paren |
| `/categories/16/items/2/name` | [0,10) | 줄기세포 + MTS | 조합, '+' 연결 |  | plus |
| `/categories/16/items/2/name` | [11,17) | (전체얼굴) | 적용 범위, 부위 후보 |  | paren |
| `/categories/16/items/3/name` | [0,9) | 줄기세포 두피치료 | 부위 후보, 시술명 후보 |  | 없음(패턴 밖) |
| `/categories/16/items/3/name` | [10,14) | (탈모) | 고민 후보 |  | paren |
| `/categories/16/items/4/name` | [0,9) | 줄기세포 관절치료 | 부위/적응증 후보, 시술명 후보 |  | 없음(패턴 밖) |
| `/categories/16/items/5/name` | [5,11) | 3회 패키지 | 회차, 판매 구성 |  | 없음(패턴 밖) |
| `/categories/16/items/5/name` | [12,18) | (전체얼굴) | 적용 범위, 부위 후보 |  | paren |

### 자동 후보 (정규식 일치분뿐 — 의미 해석 아님)

| Pointer | 구간 | 패턴 | 일치 구절 | 검토 |
|---|---|---|---|---|
| `/categories/16/items/0/name` | [12,18) | paren | (전체얼굴) | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/16/items/0/name` | [13,17) | kw | 전체얼굴 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/16/items/0/unit` | [0,2) | num_unit | 1회 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/16/items/1/name` | [9,15) | paren | (전체얼굴) | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/16/items/1/name` | [10,14) | kw | 전체얼굴 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/16/items/1/unit` | [0,2) | num_unit | 1회 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/16/items/2/name` | [11,17) | paren | (전체얼굴) | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/16/items/2/name` | [0,10) | plus | 줄기세포 + MTS | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/16/items/2/name` | [12,16) | kw | 전체얼굴 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/16/items/2/unit` | [0,2) | num_unit | 1회 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/16/items/3/name` | [10,14) | paren | (탈모) | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/16/items/3/unit` | [0,2) | num_unit | 1회 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/16/items/4/unit` | [0,2) | num_unit | 1회 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/16/items/5/name` | [12,18) | paren | (전체얼굴) | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/16/items/5/name` | [5,7) | num_unit | 3회 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/16/items/5/name` | [8,11) | kw | 패키지 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/16/items/5/name` | [13,17) | kw | 전체얼굴 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/16/items/5/unit` | [0,2) | num_unit | 3회 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |

### 형태소 (Kiwi 원시 결과 — 도메인 정답 아님. `form/tag[start,end)`)

| Pointer | 원문 값 | 토큰 |
|---|---|---|
| `/categories/16/id` | M17 | 제외: 카테고리 ID(Mn) — 식별자 |
| `/categories/16/name` | 줄기세포치료 | 줄기세포/NNG[0,4) 치료/NNG[4,6) |
| `/categories/16/items/0/name` | 줄기세포 배양액 주입 (전체얼굴) | 줄기세포/NNG[0,4) 배양액/NNG[5,8) 주입/NNG[9,11) (/SSO[12,13) 전체/NNG[13,15) 얼굴/NNG[15,17) )/SSC[17,18) |
| `/categories/16/items/0/unit` | 1회 | 1/SN[0,1) 회/NNB[1,2) |
| `/categories/16/items/1/name` | 줄기세포 엑소좀 (전체얼굴) | 줄기세포/NNP[0,4) 엑소좀/NNP[5,8) (/SSO[9,10) 전체/NNG[10,12) 얼굴/NNG[12,14) )/SSC[14,15) |
| `/categories/16/items/1/unit` | 1회 | 1/SN[0,1) 회/NNB[1,2) |
| `/categories/16/items/2/name` | 줄기세포 + MTS (전체얼굴) | 줄기세포/NNP[0,4) +/SW[5,6) MTS/SL[7,10) (/SSO[11,12) 전체/NNG[12,14) 얼굴/NNG[14,16) )/SSC[16,17) |
| `/categories/16/items/2/unit` | 1회 | 1/SN[0,1) 회/NNB[1,2) |
| `/categories/16/items/3/name` | 줄기세포 두피치료 (탈모) | 줄기세포/NNG[0,4) 두피/NNP[5,7) 치료/NNG[7,9) (/SSO[10,11) 탈모/NNG[11,13) )/SSC[13,14) |
| `/categories/16/items/3/unit` | 1회 | 1/SN[0,1) 회/NNB[1,2) |
| `/categories/16/items/4/name` | 줄기세포 관절치료 | 줄기세포/NNP[0,4) 관절/NNG[5,7) 치료/NNG[7,9) |
| `/categories/16/items/4/unit` | 1회 | 1/SN[0,1) 회/NNB[1,2) |
| `/categories/16/items/5/name` | 줄기세포 3회 패키지 (전체얼굴) | 줄기/NNG[0,2) 세포/NNG[2,4) 3/SN[5,6) 회/NNB[6,7) 패키지/NNG[8,11) (/SSO[12,13) 전체/NNG[13,15) 얼굴/NNG[15,17) )/SSC[17,18) |
| `/categories/16/items/5/unit` | 3회 | 3/SN[0,1) 회/NNB[1,2) |

### 미결 (이 구획)

| ID | 상태 | Pointer | 내용 |
|---|---|---|---|
| B-S17-1 | B | `/categories/16/items/5/name` | '3회 패키지' 구성 시술·간격이 없다. |
| B-S17-2 | B | `/categories/16/items/4/name` | '관절치료' 의 관절 부위·범위가 없다. |
| F-S17-1 | F | `/categories/16/items/1/name`, `/categories/4/items/2/name` | '줄기세포 엑소좀'(M17)과 '엑소좀'(M5)의 관계는 후속 연결 과제(병합하지 않음). |
