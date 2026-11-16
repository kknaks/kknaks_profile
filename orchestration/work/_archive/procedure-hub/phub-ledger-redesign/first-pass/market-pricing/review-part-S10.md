# S10 — M10 HIFES/EMS (6항목)

[← review.md](review.md) · 소유 말단 32 · 직접 읽기 ○ · 마지막 읽은 Pointer `/categories/9/items/5/high`

## S10

### 상위 문맥 (S00 소유, 공동 참조)

- `/currency` = `KRW` · `/updated` = `2026-07-26` · `/note` = `한국 시장 참고 가격 범위. 클리닉/지역/의사에 따라 상이. 정가 아닌 시장 범위.`

### 원문 값 — 카테고리

| Pointer | 원본 컬럼명 | 자료형 | 원문 값 |
|---|---|---|---|
| `/categories/9/id` | `id` | string | `M10` |
| `/categories/9/name` | `name` | string | `HIFES/EMS` |
| `/categories/9/items` | `items` | array[6] of object | (아래 표) |

### 원문 값 — `items` (원본 순서, 각 값의 Pointer = 항목 Pointer + `/` + 컬럼명)

자료형: `name`·`unit` string, `low`·`mid`·`high` integer.

| 항목 Pointer | `name` | `unit` | `low` | `mid` | `high` |
|---|---|---|---|---|---|
| `/categories/9/items/0` | 이모드 (복부) | 1회 | 100000 | 200000 | 400000 |
| `/categories/9/items/1` | 이모드 (힙) | 1회 | 100000 | 200000 | 400000 |
| `/categories/9/items/2` | 이모드 (복부+힙 동시) | 1회 | 180000 | 350000 | 600000 |
| `/categories/9/items/3` | 이모드 (4회 패키지) | 4회 | 350000 | 700000 | 1200000 |
| `/categories/9/items/4` | 안면 EMS (표정근 강화) | 1회 | 80000 | 150000 | 300000 |
| `/categories/9/items/5` | EMS 바디 (팔뚝/허벅지) | 1회 | 100000 | 200000 | 350000 |

### 잠정 관찰 (원문 아님 — 근거 Pointer 와 상태)

| 근거 Pointer | 관찰 | 상태 |
|---|---|---|
| `/categories/9/items/2/name` | '이모드 (복부+힙 동시)' — '+' 로 두 부위를 묶고 '동시' 로 같은 회차 시행을 명시. 가격(180000/350000/600000)은 복부·힙 단독 합(200000/400000/800000)보다 낮음 — 원문 값 그대로. | P |
| `/categories/9/items/3/name` | '이모드 (4회 패키지)' unit '4회' — 패키지 부위가 무엇인지(복부·힙 등) 원문에 없음. | B |
| `/categories/9/items/4/name` | '안면 EMS (표정근 강화)' — 괄호가 부위가 아니라 목적/효과 후보('강화'). | P |
| `/categories/9/items/5/name` | 'EMS 바디 (팔뚝/허벅지)' — '/' 로 두 부위. 둘 중 하나의 가격인지 둘 다인지 원문만으로 확정 불가. README 규칙상 '/'=대안. | P |
| `/categories/9/items/0/low` | 6항목 모두 low < mid < high. | P |

### 직접 읽기로 수집한 표현 (문자열 값 코드포인트 구간 [start,end))

| Pointer | 구간 | 원문 구절 | 탐색 관점(확정 분류 아님) | 메모 | 자동 패턴 동일 구간 |
|---|---|---|---|---|---|
| `/categories/9/name` | [0,9) | HIFES/EMS | 분류명, '/' 연결, 영문 약어 |  | slash |
| `/categories/9/items/0/name` | [0,3) | 이모드 | 장비명 후보 |  | 없음(패턴 밖) |
| `/categories/9/items/0/name` | [4,8) | (복부) | 부위 후보 |  | paren |
| `/categories/9/items/1/name` | [0,3) | 이모드 | 장비명 후보 |  | 없음(패턴 밖) |
| `/categories/9/items/1/name` | [4,7) | (힙) | 부위 후보 |  | paren |
| `/categories/9/items/2/name` | [0,3) | 이모드 | 장비명 후보 |  | 없음(패턴 밖) |
| `/categories/9/items/2/name` | [4,13) | (복부+힙 동시) | 부위 조합, 동시 시행 |  | paren |
| `/categories/9/items/2/name` | [5,9) | 복부+힙 | 부위 조합, '+' 연결 |  | plus |
| `/categories/9/items/2/name` | [10,12) | 동시 | 동시 시행, 시간 |  | kw |
| `/categories/9/items/3/name` | [0,3) | 이모드 | 장비명 후보 |  | 없음(패턴 밖) |
| `/categories/9/items/3/name` | [4,12) | (4회 패키지) | 회차, 판매 구성 |  | paren |
| `/categories/9/items/4/name` | [0,6) | 안면 EMS | 부위 후보, 기법명 후보 |  | 없음(패턴 밖) |
| `/categories/9/items/4/name` | [7,15) | (표정근 강화) | 목적/효과 후보, 부위 후보 | '강화' — 효과 방향. | paren |
| `/categories/9/items/5/name` | [0,6) | EMS 바디 | 기법명 후보, 부위 범위 |  | 없음(패턴 밖) |
| `/categories/9/items/5/name` | [7,15) | (팔뚝/허벅지) | 부위 후보, '/' 연결 |  | paren |

### 자동 후보 (정규식 일치분뿐 — 의미 해석 아님)

| Pointer | 구간 | 패턴 | 일치 구절 | 검토 |
|---|---|---|---|---|
| `/categories/9/name` | [0,9) | slash | HIFES/EMS | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/9/items/0/name` | [4,8) | paren | (복부) | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/9/items/0/unit` | [0,2) | num_unit | 1회 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/9/items/1/name` | [4,7) | paren | (힙) | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/9/items/1/unit` | [0,2) | num_unit | 1회 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/9/items/2/name` | [4,13) | paren | (복부+힙 동시) | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/9/items/2/name` | [5,9) | plus | 복부+힙 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/9/items/2/name` | [10,12) | kw | 동시 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/9/items/2/unit` | [0,2) | num_unit | 1회 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/9/items/3/name` | [4,12) | paren | (4회 패키지) | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/9/items/3/name` | [5,7) | num_unit | 4회 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/9/items/3/name` | [8,11) | kw | 패키지 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/9/items/3/unit` | [0,2) | num_unit | 4회 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/9/items/4/name` | [7,15) | paren | (표정근 강화) | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/9/items/4/name` | [12,14) | kw | 강화 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/9/items/4/unit` | [0,2) | num_unit | 1회 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/9/items/5/name` | [7,15) | paren | (팔뚝/허벅지) | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/9/items/5/name` | [8,14) | slash | 팔뚝/허벅지 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/9/items/5/unit` | [0,2) | num_unit | 1회 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |

### 형태소 (Kiwi 원시 결과 — 도메인 정답 아님. `form/tag[start,end)`)

| Pointer | 원문 값 | 토큰 |
|---|---|---|
| `/categories/9/id` | M10 | 제외: 카테고리 ID(Mn) — 식별자 |
| `/categories/9/name` | HIFES/EMS | HIFES/SL[0,5) //SP[5,6) EMS/SL[6,9) |
| `/categories/9/items/0/name` | 이모드 (복부) | 이/MM[0,1) 모드/NNG[1,3) (/SSO[4,5) 복부/NNG[5,7) )/SSC[7,8) |
| `/categories/9/items/0/unit` | 1회 | 1/SN[0,1) 회/NNB[1,2) |
| `/categories/9/items/1/name` | 이모드 (힙) | 이/MM[0,1) 모드/NNG[1,3) (/SSO[4,5) 힙/NNP[5,6) )/SSC[6,7) |
| `/categories/9/items/1/unit` | 1회 | 1/SN[0,1) 회/NNB[1,2) |
| `/categories/9/items/2/name` | 이모드 (복부+힙 동시) | 이/MM[0,1) 모드/NNG[1,3) (/SSO[4,5) 복부/NNG[5,7) +/SW[7,8) 힙/NNP[8,9) 동시/NNG[10,12) )/SSC[12,13) |
| `/categories/9/items/2/unit` | 1회 | 1/SN[0,1) 회/NNB[1,2) |
| `/categories/9/items/3/name` | 이모드 (4회 패키지) | 이/MM[0,1) 모드/NNG[1,3) (/SSO[4,5) 4/SN[5,6) 회/NNB[6,7) 패키지/NNG[8,11) )/SSC[11,12) |
| `/categories/9/items/3/unit` | 4회 | 4/SN[0,1) 회/NNB[1,2) |
| `/categories/9/items/4/name` | 안면 EMS (표정근 강화) | 안면/NNG[0,2) EMS/SL[3,6) (/SSO[7,8) 표정근/NNG[8,11) 강화/NNG[12,14) )/SSC[14,15) |
| `/categories/9/items/4/unit` | 1회 | 1/SN[0,1) 회/NNB[1,2) |
| `/categories/9/items/5/name` | EMS 바디 (팔뚝/허벅지) | EMS/SL[0,3) 바디/NNG[4,6) (/SSO[7,8) 팔뚝/NNG[8,10) //SP[10,11) 허벅지/NNG[11,14) )/SSC[14,15) |
| `/categories/9/items/5/unit` | 1회 | 1/SN[0,1) 회/NNB[1,2) |

알려진 오분절 출현(교정 안 함):

- `/categories/9/items/0/name` [0,3) `이모드` → [['이', 'MM'], ['모드', 'NNG']] — 장비명 후보가 관형사 '이'+'모드' 로 쪼개짐. 관형사(MM) 수집 시 오탐.
- `/categories/9/items/1/name` [0,3) `이모드` → [['이', 'MM'], ['모드', 'NNG']] — 장비명 후보가 관형사 '이'+'모드' 로 쪼개짐. 관형사(MM) 수집 시 오탐.
- `/categories/9/items/2/name` [0,3) `이모드` → [['이', 'MM'], ['모드', 'NNG']] — 장비명 후보가 관형사 '이'+'모드' 로 쪼개짐. 관형사(MM) 수집 시 오탐.
- `/categories/9/items/3/name` [0,3) `이모드` → [['이', 'MM'], ['모드', 'NNG']] — 장비명 후보가 관형사 '이'+'모드' 로 쪼개짐. 관형사(MM) 수집 시 오탐.

### 미결 (이 구획)

| ID | 상태 | Pointer | 내용 |
|---|---|---|---|
| B-S10-1 | B | `/categories/9/items/3/name` | '4회 패키지' 의 부위·간격이 없다. |
| P-S10-1 | P | `/categories/9/items/5/name` | '팔뚝/허벅지' 가 대안(둘 중 하나)인지 잠정. |
