# S04 — M4 스킨부스터 (7항목)

[← review.md](review.md) · 소유 말단 37 · 직접 읽기 ○ · 마지막 읽은 Pointer `/categories/3/items/6/high`

## S04

### 상위 문맥 (S00 소유, 공동 참조)

- `/currency` = `KRW` · `/updated` = `2026-07-26` · `/note` = `한국 시장 참고 가격 범위. 클리닉/지역/의사에 따라 상이. 정가 아닌 시장 범위.`

### 원문 값 — 카테고리

| Pointer | 원본 컬럼명 | 자료형 | 원문 값 |
|---|---|---|---|
| `/categories/3/id` | `id` | string | `M4` |
| `/categories/3/name` | `name` | string | `스킨부스터` |
| `/categories/3/items` | `items` | array[7] of object | (아래 표) |

### 원문 값 — `items` (원본 순서, 각 값의 Pointer = 항목 Pointer + `/` + 컬럼명)

자료형: `name`·`unit` string, `low`·`mid`·`high` integer.

| 항목 Pointer | `name` | `unit` | `low` | `mid` | `high` |
|---|---|---|---|---|---|
| `/categories/3/items/0` | 리쥬란 힐러 (2cc) | 2cc | 100000 | 200000 | 350000 |
| `/categories/3/items/1` | 리쥬란 아이 (1cc) | 1cc | 80000 | 150000 | 250000 |
| `/categories/3/items/2` | 쥬베룩 파인 (2cc) | 2cc | 80000 | 150000 | 250000 |
| `/categories/3/items/3` | 쥬베룩 울트라 (2cc) | 2cc | 100000 | 180000 | 300000 |
| `/categories/3/items/4` | 프로파일로 (2ml) | 2ml | 200000 | 350000 | 550000 |
| `/categories/3/items/5` | 볼뉴머 | 부위/1회 | 150000 | 250000 | 400000 |
| `/categories/3/items/6` | 스킨부스터 물광주사 (전체얼굴) | 1회 | 80000 | 150000 | 300000 |

### 잠정 관찰 (원문 아님 — 근거 Pointer 와 상태)

| 근거 Pointer | 관찰 | 상태 |
|---|---|---|
| `/categories/3/items/0/name` | items/0~4 는 '<제품명 후보> (<용량>)' 형태, unit 칸에 같은 용량 반복. '리쥬란 힐러'·'리쥬란 아이' 의 '힐러'·'아이' 는 제품 변형 표시 후보('아이'가 부위(눈)를 뜻하는지 원문에 없음). | P |
| `/categories/3/items/4/unit` | '2ml' — 다른 항목의 'cc' 와 다른 부피 단위 표기. 둘의 환산을 이번 단계에서 하지 않음. | P |
| `/categories/3/items/5/unit` | '볼뉴머' unit '부위/1회' — '/' 가 '부위당 1회'(분모)인지 '부위 또는 1회'(대안)인지 원문만으로 확정 불가. README 의 '/'=대안 규칙과 충돌 가능. | P |
| `/categories/3/items/6/name` | '스킨부스터 물광주사 (전체얼굴)' — 카테고리 이름 '스킨부스터'가 항목 name 에 반복되고, '물광주사' 라는 다른 명칭과 붙어 있음. 괄호는 적용 범위(전체얼굴). | P |
| `/categories/3/items/0/low` | 7항목 모두 low < mid < high. | P |

### 직접 읽기로 수집한 표현 (문자열 값 코드포인트 구간 [start,end))

| Pointer | 구간 | 원문 구절 | 탐색 관점(확정 분류 아님) | 메모 | 자동 패턴 동일 구간 |
|---|---|---|---|---|---|
| `/categories/3/items/0/name` | [0,6) | 리쥬란 힐러 | 제품명 후보, 변형 표시 |  | 없음(패턴 밖) |
| `/categories/3/items/0/name` | [7,12) | (2cc) | 수량·단위 |  | paren |
| `/categories/3/items/1/name` | [0,6) | 리쥬란 아이 | 제품명 후보, 변형 표시, 부위 후보 | '아이' 가 눈(eye)을 가리키는지 원문 명시 없음. | 없음(패턴 밖) |
| `/categories/3/items/1/name` | [7,12) | (1cc) | 수량·단위 |  | paren |
| `/categories/3/items/2/name` | [0,6) | 쥬베룩 파인 | 제품명 후보, 변형 표시 |  | 없음(패턴 밖) |
| `/categories/3/items/2/name` | [7,12) | (2cc) | 수량·단위 |  | paren |
| `/categories/3/items/3/name` | [0,7) | 쥬베룩 울트라 | 제품명 후보, 변형 표시 |  | 없음(패턴 밖) |
| `/categories/3/items/3/name` | [8,13) | (2cc) | 수량·단위 |  | paren |
| `/categories/3/items/4/name` | [0,5) | 프로파일로 | 제품명 후보 |  | 없음(패턴 밖) |
| `/categories/3/items/4/name` | [6,11) | (2ml) | 수량·단위 | ml 표기. | paren |
| `/categories/3/items/5/name` | [0,3) | 볼뉴머 | 제품명/장비명 후보 | 괄호·부위 없음. | 없음(패턴 밖) |
| `/categories/3/items/5/unit` | [0,5) | 부위/1회 | 가격 기준, '/' 연결, 회차 | 분모(부위당)인지 대안인지 미확정. | slash |
| `/categories/3/items/6/name` | [0,10) | 스킨부스터 물광주사 | 시술명 후보, 분류명 반복 |  | 없음(패턴 밖) |
| `/categories/3/items/6/name` | [6,10) | 물광주사 | 시술명/별칭 후보 |  | 없음(패턴 밖) |
| `/categories/3/items/6/name` | [11,17) | (전체얼굴) | 적용 범위, 부위 후보 | '전체' 가 범위를 한정. | paren |

### 자동 후보 (정규식 일치분뿐 — 의미 해석 아님)

| Pointer | 구간 | 패턴 | 일치 구절 | 검토 |
|---|---|---|---|---|
| `/categories/3/items/0/name` | [7,12) | paren | (2cc) | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/3/items/0/name` | [8,11) | num_unit | 2cc | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/3/items/0/unit` | [0,3) | num_unit | 2cc | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/3/items/1/name` | [7,12) | paren | (1cc) | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/3/items/1/name` | [8,11) | num_unit | 1cc | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/3/items/1/unit` | [0,3) | num_unit | 1cc | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/3/items/2/name` | [7,12) | paren | (2cc) | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/3/items/2/name` | [8,11) | num_unit | 2cc | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/3/items/2/unit` | [0,3) | num_unit | 2cc | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/3/items/3/name` | [8,13) | paren | (2cc) | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/3/items/3/name` | [9,12) | num_unit | 2cc | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/3/items/3/unit` | [0,3) | num_unit | 2cc | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/3/items/4/name` | [6,11) | paren | (2ml) | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/3/items/4/name` | [7,10) | num_unit | 2ml | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/3/items/4/unit` | [0,3) | num_unit | 2ml | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/3/items/5/unit` | [3,5) | num_unit | 1회 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/3/items/5/unit` | [0,5) | slash | 부위/1회 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/3/items/6/name` | [11,17) | paren | (전체얼굴) | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/3/items/6/name` | [12,16) | kw | 전체얼굴 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/3/items/6/unit` | [0,2) | num_unit | 1회 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |

### 형태소 (Kiwi 원시 결과 — 도메인 정답 아님. `form/tag[start,end)`)

| Pointer | 원문 값 | 토큰 |
|---|---|---|
| `/categories/3/id` | M4 | 제외: 카테고리 ID(Mn) — 식별자 |
| `/categories/3/name` | 스킨부스터 | 스킨부스터/NNG[0,5) |
| `/categories/3/items/0/name` | 리쥬란 힐러 (2cc) | 리쥬/NNP[0,2) 이/VCP[2,2) 란/ETM[2,3) 힐러/NNP[4,6) (/SSO[7,8) 2/SN[8,9) cc/SL[9,11) )/SSC[11,12) |
| `/categories/3/items/0/unit` | 2cc | 2/SN[0,1) cc/SL[1,3) |
| `/categories/3/items/1/name` | 리쥬란 아이 (1cc) | 리쥬/NNP[0,2) 이/VCP[2,2) 란/ETM[2,3) 아이/NNG[4,6) (/SSO[7,8) 1/SN[8,9) cc/SL[9,11) )/SSC[11,12) |
| `/categories/3/items/1/unit` | 1cc | 1/SN[0,1) cc/SL[1,3) |
| `/categories/3/items/2/name` | 쥬베룩 파인 (2cc) | 쥬베/NNG[0,2) 룩/NNG[2,3) 파인/NNG[4,6) (/SSO[7,8) 2/SN[8,9) cc/SL[9,11) )/SSC[11,12) |
| `/categories/3/items/2/unit` | 2cc | 2/SN[0,1) cc/SL[1,3) |
| `/categories/3/items/3/name` | 쥬베룩 울트라 (2cc) | 쥬베룩/NNG[0,3) 울트라/NNG[4,7) (/SSO[8,9) 2/SN[9,10) cc/SL[10,12) )/SSC[12,13) |
| `/categories/3/items/3/unit` | 2cc | 2/SN[0,1) cc/SL[1,3) |
| `/categories/3/items/4/name` | 프로파일로 (2ml) | 프로파일로/NNP[0,5) (/SSO[6,7) 2/SN[7,8) ml/SL[8,10) )/SSC[10,11) |
| `/categories/3/items/4/unit` | 2ml | 2/SN[0,1) ml/SL[1,3) |
| `/categories/3/items/5/name` | 볼뉴머 | 볼/NNG[0,1) 뉴/NNG[1,2) 머/EC[2,3) |
| `/categories/3/items/5/unit` | 부위/1회 | 부위/NNG[0,2) //SP[2,3) 1/SN[3,4) 회/NNB[4,5) |
| `/categories/3/items/6/name` | 스킨부스터 물광주사 (전체얼굴) | 스킨부스터/NNP[0,5) 물광주사/NNP[6,10) (/SSO[11,12) 전체/NNG[12,14) 얼굴/NNG[14,16) )/SSC[16,17) |
| `/categories/3/items/6/unit` | 1회 | 1/SN[0,1) 회/NNB[1,2) |

알려진 오분절 출현(교정 안 함):

- `/categories/3/items/0/name` [0,3) `리쥬란` → [['리쥬', 'NNP'], ['이', 'VCP'], ['란', 'ETM']] — 제품명 후보가 명사+지정사(길이0)+어미로 쪼개진다. 제품명 단위 검색 불가, 길이0 토큰 포함.
- `/categories/3/items/1/name` [0,3) `리쥬란` → [['리쥬', 'NNP'], ['이', 'VCP'], ['란', 'ETM']] — 제품명 후보가 명사+지정사(길이0)+어미로 쪼개진다. 제품명 단위 검색 불가, 길이0 토큰 포함.
- `/categories/3/items/2/name` [0,3) `쥬베룩` → [['쥬베', 'NNG'], ['룩', 'NNG']] — 제품명 후보 분절. 같은 원장의 '쥬베룩 울트라' 출현에서는 '쥬베룩/NNG' 한 토큰 — 분석 불일치.
- `/categories/3/items/5/name` [0,3) `볼뉴머` → [['볼', 'NNG'], ['뉴', 'NNG'], ['머', 'EC']] — 제품명 후보에서 '볼'(부위 후보와 같은 형태)이 명사로 나와 부위 오탐 위험.

### 미결 (이 구획)

| ID | 상태 | Pointer | 내용 |
|---|---|---|---|
| P-S04-1 | P | `/categories/3/items/5/unit` | '부위/1회' 의 '/' 의미 잠정. 가격 분모(부위당·회당)를 확정하지 않는다. |
| B-S04-1 | B | `/categories/3/items/5/unit` | '부위/1회' 의 '부위' 가 어떤 부위(크기)인지 없음. |
| B-S04-2 | B | `/categories/3/items/6/name` | '물광주사' 에 쓰는 제품·용량이 없다. |
