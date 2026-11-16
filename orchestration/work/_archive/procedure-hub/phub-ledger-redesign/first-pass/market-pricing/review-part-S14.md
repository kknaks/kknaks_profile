# S14 — M14 크라이오리포라이시스 (6항목)

[← review.md](review.md) · 소유 말단 32 · 직접 읽기 ○ · 마지막 읽은 Pointer `/categories/13/items/5/high`

## S14

### 상위 문맥 (S00 소유, 공동 참조)

- `/currency` = `KRW` · `/updated` = `2026-07-26` · `/note` = `한국 시장 참고 가격 범위. 클리닉/지역/의사에 따라 상이. 정가 아닌 시장 범위.`

### 원문 값 — 카테고리

| Pointer | 원본 컬럼명 | 자료형 | 원문 값 |
|---|---|---|---|
| `/categories/13/id` | `id` | string | `M14` |
| `/categories/13/name` | `name` | string | `크라이오리포라이시스` |
| `/categories/13/items` | `items` | array[6] of object | (아래 표) |

### 원문 값 — `items` (원본 순서, 각 값의 Pointer = 항목 Pointer + `/` + 컬럼명)

자료형: `name`·`unit` string, `low`·`mid`·`high` integer.

| 항목 Pointer | `name` | `unit` | `low` | `mid` | `high` |
|---|---|---|---|---|---|
| `/categories/13/items/0` | 쿨스컬프팅 (복부 1부위) | 1부위 | 200000 | 350000 | 600000 |
| `/categories/13/items/1` | 쿨스컬프팅 (러브핸들 양쪽) | 양쪽 | 350000 | 600000 | 1000000 |
| `/categories/13/items/2` | 쿨스컬프팅 (턱밑 이중턱) | 1부위 | 200000 | 350000 | 600000 |
| `/categories/13/items/3` | 쿨스컬프팅 (허벅지 안쪽 양쪽) | 양쪽 | 400000 | 700000 | 1200000 |
| `/categories/13/items/4` | 쿨스컬프팅 (팔뚝 양쪽) | 양쪽 | 300000 | 500000 | 900000 |
| `/categories/13/items/5` | 쿨미니 (소부위 1개) | 1부위 | 100000 | 200000 | 400000 |

### 잠정 관찰 (원문 아님 — 근거 Pointer 와 상태)

| 근거 Pointer | 관찰 | 상태 |
|---|---|---|
| `/categories/13/items/0/name` | items/0~4 '쿨스컬프팅 (<부위> <수량>)', items/5 '쿨미니 (소부위 1개)'. unit 은 '1부위'·'양쪽' 두 종류 — '양쪽' 은 숫자 없는 양측 단위. | P |
| `/categories/13/items/2/name` | '(턱밑 이중턱)' — 부위(턱밑)+고민(이중턱). unit '1부위'. | P |
| `/categories/13/items/3/name` | '(허벅지 안쪽 양쪽)' — '안쪽' 은 위치 수식, '양쪽' 은 양측성. 두 수식이 한 괄호에 겹침. | P |
| `/categories/13/items/5/name` | '쿨미니 (소부위 1개)' unit '1부위' — name 은 '1개', unit 은 '1부위'(같은 뜻인지 원문 명시 없음). '소부위' 의 '소' 는 크기 수식, 크기 기준 없음. | P |
| `/categories/13/items/0/unit` | '1부위' 의 크기(어플리케이터 1회분 등)가 원문에 없음. | B |
| `/categories/13/items/0/low` | 6항목 모두 low < mid < high. | P |

### 직접 읽기로 수집한 표현 (문자열 값 코드포인트 구간 [start,end))

| Pointer | 구간 | 원문 구절 | 탐색 관점(확정 분류 아님) | 메모 | 자동 패턴 동일 구간 |
|---|---|---|---|---|---|
| `/categories/13/name` | [0,10) | 크라이오리포라이시스 | 분류명, 외래어 |  | 없음(패턴 밖) |
| `/categories/13/items/0/name` | [0,5) | 쿨스컬프팅 | 장비명 후보 |  | 없음(패턴 밖) |
| `/categories/13/items/0/name` | [6,14) | (복부 1부위) | 부위 후보, 수량·단위 |  | paren |
| `/categories/13/items/1/name` | [0,5) | 쿨스컬프팅 | 장비명 후보 |  | 없음(패턴 밖) |
| `/categories/13/items/1/name` | [6,15) | (러브핸들 양쪽) | 부위 후보, 양측성 |  | paren |
| `/categories/13/items/2/name` | [0,5) | 쿨스컬프팅 | 장비명 후보 |  | 없음(패턴 밖) |
| `/categories/13/items/2/name` | [6,14) | (턱밑 이중턱) | 부위 후보, 고민 후보 |  | paren |
| `/categories/13/items/3/name` | [0,5) | 쿨스컬프팅 | 장비명 후보 |  | 없음(패턴 밖) |
| `/categories/13/items/3/name` | [6,17) | (허벅지 안쪽 양쪽) | 부위 후보, 위치 수식, 양측성 |  | paren |
| `/categories/13/items/3/name` | [7,13) | 허벅지 안쪽 | 부위 후보, 위치 수식 |  | 없음(패턴 밖) |
| `/categories/13/items/4/name` | [0,5) | 쿨스컬프팅 | 장비명 후보 |  | 없음(패턴 밖) |
| `/categories/13/items/4/name` | [6,13) | (팔뚝 양쪽) | 부위 후보, 양측성 |  | paren |
| `/categories/13/items/5/name` | [0,3) | 쿨미니 | 장비명 후보 |  | 없음(패턴 밖) |
| `/categories/13/items/5/name` | [4,12) | (소부위 1개) | 크기 수식, 수량·단위 | '소' 크기 수식. | paren |
| `/categories/13/items/1/unit` | [0,2) | 양쪽 | 양측성, 가격 기준 | 숫자 없는 단위. | kw |

### 자동 후보 (정규식 일치분뿐 — 의미 해석 아님)

| Pointer | 구간 | 패턴 | 일치 구절 | 검토 |
|---|---|---|---|---|
| `/categories/13/items/0/name` | [6,14) | paren | (복부 1부위) | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/13/items/0/name` | [10,13) | num_unit | 1부위 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/13/items/0/unit` | [0,3) | num_unit | 1부위 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/13/items/1/name` | [6,15) | paren | (러브핸들 양쪽) | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/13/items/1/name` | [12,14) | kw | 양쪽 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/13/items/1/unit` | [0,2) | kw | 양쪽 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/13/items/2/name` | [6,14) | paren | (턱밑 이중턱) | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/13/items/2/unit` | [0,3) | num_unit | 1부위 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/13/items/3/name` | [6,17) | paren | (허벅지 안쪽 양쪽) | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/13/items/3/name` | [11,13) | kw | 안쪽 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/13/items/3/name` | [14,16) | kw | 양쪽 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/13/items/3/unit` | [0,2) | kw | 양쪽 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/13/items/4/name` | [6,13) | paren | (팔뚝 양쪽) | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/13/items/4/name` | [10,12) | kw | 양쪽 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/13/items/4/unit` | [0,2) | kw | 양쪽 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/13/items/5/name` | [4,12) | paren | (소부위 1개) | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/13/items/5/name` | [9,11) | num_unit | 1개 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/13/items/5/name` | [5,8) | kw | 소부위 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |
| `/categories/13/items/5/unit` | [0,3) | num_unit | 1부위 | reviewed_keep: 원문 구간 일치 확인, 후보로 유지(의미 확정 아님) |

### 형태소 (Kiwi 원시 결과 — 도메인 정답 아님. `form/tag[start,end)`)

| Pointer | 원문 값 | 토큰 |
|---|---|---|
| `/categories/13/id` | M14 | 제외: 카테고리 ID(Mn) — 식별자 |
| `/categories/13/name` | 크라이오리포라이시스 | 크라이오리포라이시스/NNG[0,10) |
| `/categories/13/items/0/name` | 쿨스컬프팅 (복부 1부위) | 쿨스컬프팅/NNP[0,5) (/SSO[6,7) 복부/NNG[7,9) 1/SN[10,11) 부위/NNG[11,13) )/SSC[13,14) |
| `/categories/13/items/0/unit` | 1부위 | 1/SN[0,1) 부위/NNG[1,3) |
| `/categories/13/items/1/name` | 쿨스컬프팅 (러브핸들 양쪽) | 쿨스컬프팅/NNP[0,5) (/SSO[6,7) 러브/NNG[7,9) 핸들/NNG[9,11) 양쪽/NNG[12,14) )/SSC[14,15) |
| `/categories/13/items/1/unit` | 양쪽 | 양쪽/NNG[0,2) |
| `/categories/13/items/2/name` | 쿨스컬프팅 (턱밑 이중턱) | 쿨스컬프팅/NNP[0,5) (/SSO[6,7) 턱밑/NNG[7,9) 이/NNP[10,11) 중턱/NNG[11,13) )/SSC[13,14) |
| `/categories/13/items/2/unit` | 1부위 | 1/SN[0,1) 부위/NNG[1,3) |
| `/categories/13/items/3/name` | 쿨스컬프팅 (허벅지 안쪽 양쪽) | 쿨스컬프팅/NNP[0,5) (/SSO[6,7) 허벅지/NNG[7,10) 안쪽/NNG[11,13) 양쪽/NNG[14,16) )/SSC[16,17) |
| `/categories/13/items/3/unit` | 양쪽 | 양쪽/NNG[0,2) |
| `/categories/13/items/4/name` | 쿨스컬프팅 (팔뚝 양쪽) | 쿨스컬프팅/NNG[0,5) (/SSO[6,7) 팔뚝/NNG[7,9) 양쪽/NNG[10,12) )/SSC[12,13) |
| `/categories/13/items/4/unit` | 양쪽 | 양쪽/NNG[0,2) |
| `/categories/13/items/5/name` | 쿨미니 (소부위 1개) | 쿨/NNG[0,1) 미니/NNG[1,3) (/SSO[4,5) 소/NNG[5,6) 부위/NNG[6,8) 1/SN[9,10) 개/NNB[10,11) )/SSC[11,12) |
| `/categories/13/items/5/unit` | 1부위 | 1/SN[0,1) 부위/NNG[1,3) |

알려진 오분절 출현(교정 안 함):

- `/categories/13/items/2/name` [10,13) `이중턱` → [['이', 'NNP'], ['중턱', 'NNG']] — '이중턱'(고민 후보)이 '이'+'중턱' 으로 쪼개져 다른 뜻의 명사가 나옴.
- `/categories/13/items/5/name` [5,8) `소부위` → [['소', 'NNG'], ['부위', 'NNG']] — 크기 수식 접두 '소-'가 일반명사(NNG)로 태깅 — 크기 수식 탐색 시 누락 위험.

### 미결 (이 구획)

| ID | 상태 | Pointer | 내용 |
|---|---|---|---|
| B-S14-1 | B | `/categories/13/items/0/unit`, `/categories/13/items/5/name` | '1부위'·'소부위' 의 크기 정의가 없다. |
| I-S14-1 | I | `/categories/13/items/5/name`, `/categories/13/items/5/unit` | name '1개' 와 unit '1부위' 의 표기가 다르다(같은 뜻인지 확인 후보). |
