# S16 — M16 수액치료 (8항목)

[← review.md](review.md) · 소유 말단 42 · 직접 읽기 ○ · 마지막 읽은 Pointer `/categories/15/items/7/high`

## S16

### 상위 문맥 (S00 소유, 공동 참조)

- `/currency` = `KRW` · `/updated` = `2026-07-26` · `/note` = `한국 시장 참고 가격 범위. 클리닉/지역/의사에 따라 상이. 정가 아닌 시장 범위.`

### 원문 값 — 카테고리

| Pointer | 원본 컬럼명 | 자료형 | 원문 값 |
|---|---|---|---|
| `/categories/15/id` | `id` | string | `M16` |
| `/categories/15/name` | `name` | string | `수액치료` |
| `/categories/15/items` | `items` | array[8] of object | (아래 표) |

### 원문 값 — `items` (원본 순서, 각 값의 Pointer = 항목 Pointer + `/` + 컬럼명)

자료형: `name`·`unit` string, `low`·`mid`·`high` integer.

| 항목 Pointer | `name` | `unit` | `low` | `mid` | `high` |
|---|---|---|---|---|---|
| `/categories/15/items/0` | 백옥주사 (글루타치온) | 1회 | 30000 | 60000 | 150000 |
| `/categories/15/items/1` | 신데렐라주사 (알파리포산) | 1회 | 50000 | 100000 | 200000 |
| `/categories/15/items/2` | 마늘주사 (비타민B1) | 1회 | 20000 | 50000 | 100000 |
| `/categories/15/items/3` | 감초주사 (간해독) | 1회 | 30000 | 60000 | 120000 |
| `/categories/15/items/4` | 고농도 비타민C 수액 | 1회 | 50000 | 100000 | 200000 |
| `/categories/15/items/5` | 면역 수액 (종합 비타민) | 1회 | 40000 | 80000 | 150000 |
| `/categories/15/items/6` | 태반주사 (라이넥) | 1회 | 30000 | 60000 | 120000 |
| `/categories/15/items/7` | 다이어트 수액 | 1회 | 50000 | 100000 | 200000 |

### 잠정 관찰 (원문 아님 — 근거 Pointer 와 상태)

| 근거 Pointer | 관찰 | 상태 |
|---|---|---|
| `/categories/15/items/0/name` | '<별칭>주사 (<성분/제품>)' 형태: 백옥주사(글루타치온)·신데렐라주사(알파리포산)·마늘주사(비타민B1)·태반주사(라이넥). 괄호가 성분 또는 제품명 후보('라이넥'은 제품명으로 보이나 원문 명시 없음). | P |
| `/categories/15/items/3/name` | '감초주사 (간해독)' — 괄호가 성분이 아니라 목적/효과 후보. 같은 형태의 괄호가 성분·목적 두 역할. | P |
| `/categories/15/items/4/name` | '고농도 비타민C 수액' — '고농도' 농도 수식, 수치 없음. | B |
| `/categories/15/items/5/name` | '면역 수액 (종합 비타민)' — 목적(면역)+성분 묶음(종합 비타민). '종합' 의 구성 없음. | B |
| `/categories/15/items/7/name` | '다이어트 수액' — 목적만, 성분 없음. | B |
| `/categories/15/items/0/unit` | 8항목 모두 '1회'. 용량(ml)·농도 없음. | B |
| `/categories/15/items/0/low` | 8항목 모두 low < mid < high. | P |

### 직접 읽기로 수집한 표현 (문자열 값 코드포인트 구간 [start,end))

| Pointer | 구간 | 원문 구절 | 탐색 관점(확정 분류 아님) | 메모 | 자동 패턴 동일 구간 |
|---|---|---|---|---|---|
| `/categories/15/items/0/name` | [0,4) | 백옥주사 | 시술 별칭 후보 |  | 없음(패턴 밖) |
| `/categories/15/items/0/name` | [5,12) | (글루타치온) | 성분 후보 |  | paren |
| `/categories/15/items/1/name` | [0,6) | 신데렐라주사 | 시술 별칭 후보 |  | 없음(패턴 밖) |
| `/categories/15/items/1/name` | [7,14) | (알파리포산) | 성분 후보 |  | paren |
| `/categories/15/items/2/name` | [0,4) | 마늘주사 | 시술 별칭 후보 |  | 없음(패턴 밖) |
| `/categories/15/items/2/name` | [5,12) | (비타민B1) | 성분 후보, 영한 혼합 |  | paren |
| `/categories/15/items/3/name` | [0,4) | 감초주사 | 시술 별칭 후보 |  | 없음(패턴 밖) |
| `/categories/15/items/3/name` | [5,10) | (간해독) | 목적/효과 후보 |  | paren |
| `/categories/15/items/4/name` | [0,11) | 고농도 비타민C 수액 | 농도 수식, 성분 후보 |  | 없음(패턴 밖) |
| `/categories/15/items/4/name` | [0,3) | 고농도 | 농도 수식 | 정도 수식, 수치 없음. | kw |
| `/categories/15/items/5/name` | [0,5) | 면역 수액 | 목적 후보 |  | 없음(패턴 밖) |
| `/categories/15/items/5/name` | [6,14) | (종합 비타민) | 성분 후보, 구성 범위 |  | paren |
| `/categories/15/items/6/name` | [0,4) | 태반주사 | 시술 별칭 후보 |  | 없음(패턴 밖) |
| `/categories/15/items/6/name` | [5,10) | (라이넥) | 제품명 후보 |  | paren |
| `/categories/15/items/7/name` | [0,7) | 다이어트 수액 | 목적 후보 |  | 없음(패턴 밖) |

### 자동 후보 (정규식 일치분뿐 — 의미 해석 아님)

| Pointer | 구간 | 패턴 | 일치 구절 | 검토 |
|---|---|---|---|---|
| `/categories/15/items/0/name` | [5,12) | paren | (글루타치온) | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/15/items/0/unit` | [0,2) | num_unit | 1회 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/15/items/1/name` | [7,14) | paren | (알파리포산) | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/15/items/1/unit` | [0,2) | num_unit | 1회 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/15/items/2/name` | [5,12) | paren | (비타민B1) | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/15/items/2/unit` | [0,2) | num_unit | 1회 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/15/items/3/name` | [5,10) | paren | (간해독) | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/15/items/3/unit` | [0,2) | num_unit | 1회 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/15/items/4/name` | [0,3) | kw | 고농도 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/15/items/4/unit` | [0,2) | num_unit | 1회 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/15/items/5/name` | [6,14) | paren | (종합 비타민) | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/15/items/5/unit` | [0,2) | num_unit | 1회 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/15/items/6/name` | [5,10) | paren | (라이넥) | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/15/items/6/unit` | [0,2) | num_unit | 1회 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/15/items/7/unit` | [0,2) | num_unit | 1회 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |

### 형태소 (Kiwi 원시 결과 — 도메인 정답 아님. `form/tag[start,end)`)

| Pointer | 원문 값 | 토큰 |
|---|---|---|
| `/categories/15/id` | M16 | 제외: 카테고리 ID(Mn) — 식별자 |
| `/categories/15/name` | 수액치료 | 수액/NNG[0,2) 치료/NNG[2,4) |
| `/categories/15/items/0/name` | 백옥주사 (글루타치온) | 백옥주사/NNP[0,4) (/SSO[5,6) 글루타치온/NNP[6,11) )/SSC[11,12) |
| `/categories/15/items/0/unit` | 1회 | 1/SN[0,1) 회/NNB[1,2) |
| `/categories/15/items/1/name` | 신데렐라주사 (알파리포산) | 신데렐라/NNP[0,4) 주사/NNG[4,6) (/SSO[7,8) 알파리포산/NNP[8,13) )/SSC[13,14) |
| `/categories/15/items/1/unit` | 1회 | 1/SN[0,1) 회/NNB[1,2) |
| `/categories/15/items/2/name` | 마늘주사 (비타민B1) | 마늘/NNG[0,2) 주사/NNG[2,4) (/SSO[5,6) 비타민/NNG[6,9) B/SL[9,10) 1/SN[10,11) )/SSC[11,12) |
| `/categories/15/items/2/unit` | 1회 | 1/SN[0,1) 회/NNB[1,2) |
| `/categories/15/items/3/name` | 감초주사 (간해독) | 감초/NNG[0,2) 주사/NNG[2,4) (/SSO[5,6) 간해독/NNP[6,9) )/SSC[9,10) |
| `/categories/15/items/3/unit` | 1회 | 1/SN[0,1) 회/NNB[1,2) |
| `/categories/15/items/4/name` | 고농도 비타민C 수액 | 고/XPN[0,1) 농도/NNG[1,3) 비타민/NNG[4,7) C/SL[7,8) 수액/NNG[9,11) |
| `/categories/15/items/4/unit` | 1회 | 1/SN[0,1) 회/NNB[1,2) |
| `/categories/15/items/5/name` | 면역 수액 (종합 비타민) | 면역/NNG[0,2) 수액/NNG[3,5) (/SSO[6,7) 종합/NNG[7,9) 비타민/NNG[10,13) )/SSC[13,14) |
| `/categories/15/items/5/unit` | 1회 | 1/SN[0,1) 회/NNB[1,2) |
| `/categories/15/items/6/name` | 태반주사 (라이넥) | 태반/NNG[0,2) 주사/NNG[2,4) (/SSO[5,6) 라이넥/NNP[6,9) )/SSC[9,10) |
| `/categories/15/items/6/unit` | 1회 | 1/SN[0,1) 회/NNB[1,2) |
| `/categories/15/items/7/name` | 다이어트 수액 | 다이어트/NNG[0,4) 수액/NNG[5,7) |
| `/categories/15/items/7/unit` | 1회 | 1/SN[0,1) 회/NNB[1,2) |

알려진 오분절 출현(교정 안 함):

- `/categories/15/items/2/name` [9,11) `B1` → [['B', 'SL'], ['1', 'SN']] — 제품명·단위(CO2·cm2·FLX 등) 영숫자 결합이 SL/SN 으로 나뉜다. 이름 단위 검색은 원문 구간으로 해야 한다.

### 미결 (이 구획)

| ID | 상태 | Pointer | 내용 |
|---|---|---|---|
| B-S16-1 | B | `/categories/15/items/0/unit` | 수액 용량·농도·성분 함량이 없다(8항목). '고농도'의 기준값 없음. |
| P-S16-1 | P | `/categories/15/items/0/name` | 괄호가 성분·제품·목적 세 역할로 쓰인다 — 역할 구분은 잠정. |
