# treatment-optimization.json — 1차 조사 review-part-3

> 원문 값 표는 build.py 가 원본에서 자동 생성했다. 잠정 관찰·수동 구절은 manual/seg-XX.json 의 직접 읽기 기록이다. 원장의 임상·규제 서술은 **원장에 적혀 있다는 사실**로만 기록했고 검증·보충하지 않았다.
> 상태 기호: P 잠정 · B 원문 정보 부족 · I 원문 내 불일치 후보 · F 후속 의미 조사 · K 알려진 분석 한계 · A 에이전트 추출 오류 · C 사용자 결정 필요.

[← 목차 review.md](./review.md)

<a id="seg-09"></a>
## SEG-09 — by_age_group 전체

- 직접 읽기: **direct_read_done** — /by_age_group/0~3 각 age·primary_concerns·recommended_base·avoid 전 원소, maintenance·annual_focus, 선택 필드 upgrade(1~3)·note(3)를 원문 순서로 직접 읽음
- 소유 노드 77 · 말단(빈 컨테이너 포함) 58

### 원문 값 (자동 생성 · 원본 컬럼명 그대로 · 원본 순서)

| Pointer | 원본 컬럼명 | 자료형 | 원문 값 |
|---|---|---|---|
| `/by_age_group/0` | `by_age_group[0]` | object(6) | _키: age, primary_concerns, recommended_base, avoid, maintenance, annual_focus_ |
| `/by_age_group/0/age` | `age` | string | "20대" |
| `/by_age_group/0/primary_concerns` | `primary_concerns` | array(4) | _원소 4개_ |
| `/by_age_group/0/primary_concerns/0` | `primary_concerns[0]` | string | "여드름/흉터" |
| `/by_age_group/0/primary_concerns/1` | `primary_concerns[1]` | string | "모공" |
| `/by_age_group/0/primary_concerns/2` | `primary_concerns[2]` | string | "피부결" |
| `/by_age_group/0/primary_concerns/3` | `primary_concerns[3]` | string | "색소(기미 초기)" |
| `/by_age_group/0/recommended_base` | `recommended_base` | array(4) | _원소 4개_ |
| `/by_age_group/0/recommended_base/0` | `recommended_base[0]` | string | "스킨부스터" |
| `/by_age_group/0/recommended_base/1` | `recommended_base[1]` | string | "필링" |
| `/by_age_group/0/recommended_base/2` | `recommended_base[2]` | string | "토닝" |
| `/by_age_group/0/recommended_base/3` | `recommended_base[3]` | string | "LED" |
| `/by_age_group/0/avoid` | `avoid` | array(2) | _원소 2개_ |
| `/by_age_group/0/avoid/0` | `avoid[0]` | string | "과도한 필러 (자연스러운 노화 중요)" |
| `/by_age_group/0/avoid/1` | `avoid[1]` | string | "불필요한 보톡스(예방 목적 과잉 금지)" |
| `/by_age_group/0/maintenance` | `maintenance` | string | "토닝 월 1-2회, 스킨부스터 분기 1회, 필링 월 1회" |
| `/by_age_group/0/annual_focus` | `annual_focus` | string | "피부 기초 관리, 여드름/흉터 집중 치료, 자외선 차단 습관화" |
| `/by_age_group/1` | `by_age_group[1]` | object(7) | _키: age, primary_concerns, recommended_base, avoid, maintenance, annual_focus, upgrade_ |
| `/by_age_group/1/age` | `age` | string | "30대" |
| `/by_age_group/1/primary_concerns` | `primary_concerns` | array(4) | _원소 4개_ |
| `/by_age_group/1/primary_concerns/0` | `primary_concerns[0]` | string | "초기 주름" |
| `/by_age_group/1/primary_concerns/1` | `primary_concerns[1]` | string | "탄력 저하" |
| `/by_age_group/1/primary_concerns/2` | `primary_concerns[2]` | string | "색소/기미" |
| `/by_age_group/1/primary_concerns/3` | `primary_concerns[3]` | string | "눈가 노화" |
| `/by_age_group/1/recommended_base` | `recommended_base` | array(4) | _원소 4개_ |
| `/by_age_group/1/recommended_base/0` | `recommended_base[0]` | string | "보톡스" |
| `/by_age_group/1/recommended_base/1` | `recommended_base[1]` | string | "스킨부스터" |
| `/by_age_group/1/recommended_base/2` | `recommended_base[2]` | string | "토닝" |
| `/by_age_group/1/recommended_base/3` | `recommended_base[3]` | string | "IPL" |
| `/by_age_group/1/avoid` | `avoid` | array(1) | _원소 1개_ |
| `/by_age_group/1/avoid/0` | `avoid[0]` | string | "과도한 필러량(자연스러움 유지)" |
| `/by_age_group/1/maintenance` | `maintenance` | string | "보톡스 3-4개월, 스킨부스터 분기, 토닝 월 1-2회" |
| `/by_age_group/1/annual_focus` | `annual_focus` | string | "노화 예방 시작, 보톡스로 동적주름 관리, 콜라겐 투자 시작" |
| `/by_age_group/1/upgrade` | `upgrade` | array(1) | _원소 1개_ |
| `/by_age_group/1/upgrade/0` | `upgrade[0]` | string | "바이오스티뮬레이터 (콜라겐 예방적 투자)" |
| `/by_age_group/2` | `by_age_group[2]` | object(7) | _키: age, primary_concerns, recommended_base, avoid, maintenance, annual_focus, upgrade_ |
| `/by_age_group/2/age` | `age` | string | "40대" |
| `/by_age_group/2/primary_concerns` | `primary_concerns` | array(4) | _원소 4개_ |
| `/by_age_group/2/primary_concerns/0` | `primary_concerns[0]` | string | "주름 심화" |
| `/by_age_group/2/primary_concerns/1` | `primary_concerns[1]` | string | "처짐" |
| `/by_age_group/2/primary_concerns/2` | `primary_concerns[2]` | string | "볼륨 손실" |
| `/by_age_group/2/primary_concerns/3` | `primary_concerns[3]` | string | "색소 심화" |
| `/by_age_group/2/recommended_base` | `recommended_base` | array(4) | _원소 4개_ |
| `/by_age_group/2/recommended_base/0` | `recommended_base[0]` | string | "보톡스" |
| `/by_age_group/2/recommended_base/1` | `recommended_base[1]` | string | "필러" |
| `/by_age_group/2/recommended_base/2` | `recommended_base[2]` | string | "HIFU/RF" |
| `/by_age_group/2/recommended_base/3` | `recommended_base[3]` | string | "바이오스티뮬레이터" |
| `/by_age_group/2/avoid` | `avoid` | array(1) | _원소 1개_ |
| `/by_age_group/2/avoid/0` | `avoid[0]` | string | "과도한 시술 빈도(피부 회복력 저하 고려)" |
| `/by_age_group/2/maintenance` | `maintenance` | string | "보톡스 3-4개월, 필러 6개월+, HIFU 6개월+, 바이오스티뮬 연 1사이클" |
| `/by_age_group/2/annual_focus` | `annual_focus` | string | "적극적 안티에이징, 처짐/볼륨 동시 관리, 복합 시술 조합" |
| `/by_age_group/2/upgrade` | `upgrade` | array(2) | _원소 2개_ |
| `/by_age_group/2/upgrade/0` | `upgrade[0]` | string | "실리프팅(PCL/PDO)" |
| `/by_age_group/2/upgrade/1` | `upgrade[1]` | string | "프락셔널 레이저" |
| `/by_age_group/3` | `by_age_group[3]` | object(8) | _키: age, primary_concerns, recommended_base, avoid, maintenance, annual_focus, note, upgrade_ |
| `/by_age_group/3/age` | `age` | string | "50대+" |
| `/by_age_group/3/primary_concerns` | `primary_concerns` | array(5) | _원소 5개_ |
| `/by_age_group/3/primary_concerns/0` | `primary_concerns[0]` | string | "처짐" |
| `/by_age_group/3/primary_concerns/1` | `primary_concerns[1]` | string | "깊은 주름" |
| `/by_age_group/3/primary_concerns/2` | `primary_concerns[2]` | string | "볼륨 손실" |
| `/by_age_group/3/primary_concerns/3` | `primary_concerns[3]` | string | "피부 노화" |
| `/by_age_group/3/primary_concerns/4` | `primary_concerns[4]` | string | "목주름" |
| `/by_age_group/3/recommended_base` | `recommended_base` | array(5) | _원소 5개_ |
| `/by_age_group/3/recommended_base/0` | `recommended_base[0]` | string | "HIFU(울쎄라급)" |
| `/by_age_group/3/recommended_base/1` | `recommended_base[1]` | string | "필러" |
| `/by_age_group/3/recommended_base/2` | `recommended_base[2]` | string | "보톡스" |
| `/by_age_group/3/recommended_base/3` | `recommended_base[3]` | string | "바이오스티뮬레이터" |
| `/by_age_group/3/recommended_base/4` | `recommended_base[4]` | string | "실리프팅" |
| `/by_age_group/3/avoid` | `avoid` | array(2) | _원소 2개_ |
| `/by_age_group/3/avoid/0` | `avoid[0]` | string | "과도한 필러(부자연스러운 외관)" |
| `/by_age_group/3/avoid/1` | `avoid[1]` | string | "회복력 초과 시술 빈도" |
| `/by_age_group/3/maintenance` | `maintenance` | string | "보톡스 3-4개월, 필러 6-12개월, HIFU 6-12개월, 바이오스티뮬 연 1사이클" |
| `/by_age_group/3/annual_focus` | `annual_focus` | string | "유지와 자연스러운 개선, 수술 대안/보완, 전체 조화 중시" |
| `/by_age_group/3/note` | `note` | string | "수술(페이스리프트) 대안 또는 보완으로 비수술 조합. 전체적 조화 중시" |
| `/by_age_group/3/upgrade` | `upgrade` | array(2) | _원소 2개_ |
| `/by_age_group/3/upgrade/0` | `upgrade[0]` | string | "프락셔널 CO2(피부결)" |
| `/by_age_group/3/upgrade/1` | `upgrade[1]` | string | "목전용 HIFU/RF" |

### 잠정 관찰 (직접 읽기 · 원문 칸과 분리 · 확정 의미 아님)

| ID | 상태 | 근거 Pointer | 관찰 |
|---|---|---|---|
| O09-1 | P | `/by_age_group/0`<br>`/by_age_group/1`<br>`/by_age_group/2`<br>`/by_age_group/3` | 선택 필드: upgrade 는 30대·40대·50대+ 에만, note 는 50대+ 에만 있다. 20대에 upgrade 가 없는 것이 「없음」 인지 「미기록」 인지 원문에 없다(B). |
| O09-2 | F | `/by_age_group/0/primary_concerns`<br>`/by_age_group/1/primary_concerns`<br>`/by_age_group/2/primary_concerns`<br>`/by_age_group/3/primary_concerns` | primary_concerns 표기가 by_concern 의 concern 과 일부만 같다: 「여드름/흉터」「색소/기미」 는 같은 문자열, 「모공」「피부결」 은 by_concern 「피부결/모공」 을 둘로 나눈 꼴, 「초기 주름」「주름 심화」「깊은 주름」 은 정도 수식이 붙은 꼴, 「눈가 노화」「피부 노화」「목주름」 은 by_concern 에 대응 고민이 없다. 연결은 하지 않았다. |
| O09-3 | P | `/by_age_group/0/primary_concerns/3` | 「색소(기미 초기)」: 괄호가 하위 상태·시기(초기) 를 좁힌다. |
| O09-4 | P | `/by_age_group/0/avoid/0`<br>`/by_age_group/1/avoid/0`<br>`/by_age_group/3/avoid/0` | avoid 는 시술 이름만이 아니라 정도 수식(과도한·불필요한)+시술 꼴이다. 괄호는 사유(자연스러운 노화 중요·자연스러움 유지·부자연스러운 외관). 「과도한」 의 양 기준은 원문에 없다(B). 「과도한 필러 (」 는 괄호 앞 공백, 「과도한 필러량(」 「과도한 필러(」 는 공백 없음. |
| O09-5 | P | `/by_age_group/0/avoid/1`<br>`/by_age_group/1/annual_focus`<br>`/by_age_group/1/upgrade/0` | 20대 avoid 「불필요한 보톡스(예방 목적 과잉 금지)」 는 예방 목적 「과잉」 을 금지하고, 30대 annual_focus 「노화 예방 시작」·upgrade 「(콜라겐 예방적 투자)」 는 예방을 권한다. 연령 조건이 달라 충돌로 판정하지 않는다. 「과잉」 의 기준은 원문에 없다. |
| O09-6 | P | `/by_age_group/2/avoid/0`<br>`/by_age_group/3/avoid/1` | 「과도한 시술 빈도(피부 회복력 저하 고려)」·「회복력 초과 시술 빈도」: 빈도 회피. 회복력·초과의 기준은 원문에 없다(B). |
| O09-7 | P | `/by_age_group/0/maintenance`<br>`/by_age_group/1/maintenance`<br>`/by_age_group/2/maintenance`<br>`/by_age_group/3/maintenance` | maintenance 는 「시술 빈도」 를 쉼표로 나열한다. 빈도 표기 꼴이 섞인다: 「월 1-2회」「분기 1회」「분기」(횟수 없음)「3-4개월」(주기, '마다' 없음)「6개월+」(이상, 열린 범위)「6-12개월」「연 1사이클」(사이클 단위 정의 없음). |
| O09-8 | P | `/by_age_group/2/maintenance`<br>`/by_age_group/3/maintenance` | 「바이오스티뮬 연 1사이클」: 사이클이 몇 회인지 원장 안 다른 값(by_concern 의 「바이오스티뮬 3-4회」 등)과 연결하지 않았다(B·F). |
| O09-9 | P | `/by_age_group/3/recommended_base/0` | 「HIFU(울쎄라급)」: 「급」 은 특정 장비가 아니라 등급/수준 근사 표현. 괄호 안 장비 예시(README)와 다른 쓰임. |
| O09-10 | P | `/by_age_group/2/upgrade/0`<br>`/by_age_group/3/upgrade/0`<br>`/by_age_group/3/upgrade/1` | 「실리프팅(PCL/PDO)」 은 by_concern 의 「실리프팅(PDO/PCL)」 과 순서가 반대다. 「프락셔널 CO2(피부결)」 은 by_concern 의 「CO2 프락셔널」 과 어순이 다르고 괄호가 대상. 「목전용 HIFU/RF」 는 부위 한정(목전용). |
| O09-11 | P | `/by_age_group/3/annual_focus`<br>`/by_age_group/3/note` | annual_focus 「수술 대안/보완」 과 note 「수술(페이스리프트) 대안 또는 보완으로 비수술 조합」: 같은 내용을 `/` 와 「또는」 으로 각각 쓴다. note 와 annual_focus 의 「전체 조화 중시」/「전체적 조화 중시」 가 겹친다. |
| O09-12 | P | `/by_age_group/3/age` | 「50대+」 의 `+` 는 이상(열린 연령 범위)이다. README `+`(함께 시술)와 다른 쓰임. |
| O09-13 | P | `/by_age_group/2/annual_focus` | 「처짐/볼륨 동시 관리, 복합 시술 조합」: 「동시」 가 고민 두 개를 함께 관리한다는 뜻으로 쓰여, 금지문의 「동시」(같은 시술 시점) 와 다르다(잠정). |

### 수동 수집 구절 (48건 · 구간은 expressions.json `source=manual_direct_reading`)

| Pointer | 원문 구절 | 탐색 관점(kinds) |
|---|---|---|
| `/by_age_group/0/primary_concerns/3` | 색소(기미 초기) | target_concern, parenthetical, time, severity |
| `/by_age_group/0/avoid/0` | 과도한 필러 (자연스러운 노화 중요) | avoid_prohibit, degree_modifier, parenthetical, reason |
| `/by_age_group/0/avoid/1` | 불필요한 보톡스(예방 목적 과잉 금지) | avoid_prohibit, degree_modifier, negation, parenthetical, purpose |
| `/by_age_group/0/maintenance` | 토닝 월 1-2회 | frequency, range, maintenance |
| `/by_age_group/0/maintenance` | 스킨부스터 분기 1회 | frequency, maintenance |
| `/by_age_group/0/maintenance` | 필링 월 1회 | frequency, maintenance |
| `/by_age_group/0/annual_focus` | 피부 기초 관리 | focus |
| `/by_age_group/0/annual_focus` | 여드름/흉터 집중 치료 | focus, degree_modifier, slash_non_alternative |
| `/by_age_group/0/annual_focus` | 자외선 차단 습관화 | focus, lifestyle_event |
| `/by_age_group/1/primary_concerns/0` | 초기 주름 | target_concern, time, severity |
| `/by_age_group/1/primary_concerns/1` | 탄력 저하 | target_concern |
| `/by_age_group/1/primary_concerns/3` | 눈가 노화 | target_concern, body_part |
| `/by_age_group/1/avoid/0` | 과도한 필러량(자연스러움 유지) | avoid_prohibit, degree_modifier, quantity_vague, parenthetical, reason |
| `/by_age_group/1/maintenance` | 보톡스 3-4개월 | frequency_period, range, maintenance |
| `/by_age_group/1/maintenance` | 스킨부스터 분기 | frequency_period, maintenance, count_unspecified |
| `/by_age_group/1/maintenance` | 토닝 월 1-2회 | frequency, range, maintenance |
| `/by_age_group/1/annual_focus` | 노화 예방 시작 | focus, prevention, series_start |
| `/by_age_group/1/annual_focus` | 보톡스로 동적주름 관리 | focus, target_concern |
| `/by_age_group/1/annual_focus` | 콜라겐 투자 시작 | focus, series_start |
| `/by_age_group/1/upgrade/0` | 바이오스티뮬레이터 (콜라겐 예방적 투자) | procedure_like, parenthetical, prevention, upgrade |
| `/by_age_group/2/primary_concerns/0` | 주름 심화 | target_concern, severity, degree_modifier |
| `/by_age_group/2/primary_concerns/3` | 색소 심화 | target_concern, severity, degree_modifier |
| `/by_age_group/2/recommended_base/2` | HIFU/RF | procedure_like, alternative |
| `/by_age_group/2/avoid/0` | 과도한 시술 빈도(피부 회복력 저하 고려) | avoid_prohibit, degree_modifier, frequency, parenthetical, reason, consideration |
| `/by_age_group/2/maintenance` | 보톡스 3-4개월 | frequency_period, range, maintenance |
| `/by_age_group/2/maintenance` | 필러 6개월+ | frequency_period, open_ended, maintenance |
| `/by_age_group/2/maintenance` | HIFU 6개월+ | frequency_period, open_ended, maintenance |
| `/by_age_group/2/maintenance` | 바이오스티뮬 연 1사이클 | frequency, cycle_unit, maintenance, abbreviation |
| `/by_age_group/2/annual_focus` | 적극적 안티에이징 | focus, degree_modifier |
| `/by_age_group/2/annual_focus` | 처짐/볼륨 동시 관리 | focus, same_time_non_procedure, slash_non_alternative |
| `/by_age_group/2/annual_focus` | 복합 시술 조합 | focus, combination |
| `/by_age_group/2/upgrade/0` | 실리프팅(PCL/PDO) | procedure_like, material, parenthetical, alternative, upgrade |
| `/by_age_group/3/age` | 50대+ | age, open_ended, plus_non_procedure |
| `/by_age_group/3/primary_concerns/1` | 깊은 주름 | target_concern, layer_depth, degree_modifier |
| `/by_age_group/3/primary_concerns/4` | 목주름 | target_concern, body_part |
| `/by_age_group/3/recommended_base/0` | HIFU(울쎄라급) | procedure_like, parenthetical, approximation, product_like |
| `/by_age_group/3/avoid/0` | 과도한 필러(부자연스러운 외관) | avoid_prohibit, degree_modifier, parenthetical, reason, negation |
| `/by_age_group/3/avoid/1` | 회복력 초과 시술 빈도 | avoid_prohibit, frequency, threshold |
| `/by_age_group/3/maintenance` | 필러 6-12개월 | frequency_period, range, maintenance |
| `/by_age_group/3/maintenance` | HIFU 6-12개월 | frequency_period, range, maintenance |
| `/by_age_group/3/maintenance` | 바이오스티뮬 연 1사이클 | frequency, cycle_unit, maintenance, abbreviation |
| `/by_age_group/3/annual_focus` | 유지와 자연스러운 개선 | focus, maintenance, manner |
| `/by_age_group/3/annual_focus` | 수술 대안/보완 | surgery, alternative, complement |
| `/by_age_group/3/annual_focus` | 전체 조화 중시 | focus, range_area |
| `/by_age_group/3/note` | 수술(페이스리프트) 대안 또는 보완으로 비수술 조합 | surgery, parenthetical, alternative, complement, category_term, negation, combination |
| `/by_age_group/3/note` | 전체적 조화 중시 | focus, range_area |
| `/by_age_group/3/upgrade/0` | 프락셔널 CO2(피부결) | procedure_like, parenthetical, target_concern, upgrade |
| `/by_age_group/3/upgrade/1` | 목전용 HIFU/RF | procedure_like, body_part, alternative, upgrade |

### 이 구획의 미결 (issues.md 에 모음)

- **B-09-1** [B] avoid 의 정도 기준(과도한·불필요한·과잉·회복력 초과)이 원문에 없다. 회피 조건을 판정 규칙으로 쓸 수 없다. — `/by_age_group/0/avoid/0`, `/by_age_group/0/avoid/1`, `/by_age_group/1/avoid/0`, `/by_age_group/2/avoid/0`, `/by_age_group/3/avoid/0`, `/by_age_group/3/avoid/1`
- **B-09-2** [B] 「연 1사이클」 의 사이클 정의(회차)가 원문에 없다. — `/by_age_group/2/maintenance`, `/by_age_group/3/maintenance`
- **B-09-3** [B] 20대에 upgrade 가 없는 것이 없음인지 미기록인지, 50대+ 외에 note 가 없는 것의 뜻이 원문에 없다. — `/by_age_group/0`

<a id="seg-10"></a>
## SEG-10 — combination_rules 전체

- 직접 읽기: **direct_read_done** — /combination_rules/0~7 각 rule·detail·evidence·consensus·priority 를 원문 순서로 직접 읽음. 같은 원장 by_concern 의 대응 문구와 대조(원장 내부 대조만, 외부 자료 없음)
- 소유 노드 48 · 말단(빈 컨테이너 포함) 40

### 원문 값 (자동 생성 · 원본 컬럼명 그대로 · 원본 순서)

| Pointer | 원본 컬럼명 | 자료형 | 원문 값 |
|---|---|---|---|
| `/combination_rules/0` | `combination_rules[0]` | object(5) | _키: rule, detail, evidence, consensus, priority_ |
| `/combination_rules/0/rule` | `rule` | string | "열시술 → 주사 순서" |
| `/combination_rules/0/detail` | `detail` | string | "보톡스와 HIFU/RF 열시술은 당일 시술 가능하나 웬만하면 열시술을 먼저 시행. MFU/HIFU는 보톡스 주입 후 2주 이내 효력을 감소시킬 수 있어 HIFU를 먼저 시행하거나 2주 이상 간격을 둔다. HA 필러는 필러 후 HIFU를 4주 이상 간격 권장하거나 HIFU를 먼저 시행한다. RF·IPL·비침습 레이저는 보톡스와 당일 병행 가능하므로 HIFU와 동일한 절대 규칙으로 취급하지 않음." |
| `/combination_rules/0/evidence` | `evidence` | string | "MFU-보툴리눔독소 진피내 주입 RCT (J Cosmet Dermatol, PMC11945533); HIFU-HA 필러 열분해 연구(2024); 보툴리눔독소 당일 병용 안전성 리뷰(2014/2020)" |
| `/combination_rules/0/consensus` | `consensus` | string | "근거 기반 임상 권고" |
| `/combination_rules/0/priority` | `priority` | string | "moderate" |
| `/combination_rules/1` | `combination_rules[1]` | object(5) | _키: rule, detail, evidence, consensus, priority_ |
| `/combination_rules/1/rule` | `rule` | string | "필러 → RF 14일 간격" |
| `/combination_rules/1/detail` | `detail` | string | "HA 필러 주입 후 14일 이내 RF/HIFU 시 필러 용해 위험" |
| `/combination_rules/1/evidence` | `evidence` | string | "JCD 2023 논문" |
| `/combination_rules/1/consensus` | `consensus` | string | "3/3 AI 합의" |
| `/combination_rules/1/priority` | `priority` | string | "critical" |
| `/combination_rules/2` | `combination_rules[2]` | object(5) | _키: rule, detail, evidence, consensus, priority_ |
| `/combination_rules/2/rule` | `rule` | string | "바이오스티뮬 결절 예방 = 희석·수화·주입 깊이 (마사지는 선택)" |
| `/combination_rules/2/detail` | `detail` | string | "PLLA 균일 분포를 위한 5-5-5 마사지는 기술적 보조로 권장. 2025 동물실험은 균일 분포·결절 예방 효과를 지지하지만 인체 RCT에서는 결절률 차이가 없었으며, 핵심은 적정 희석·충분한 수화·정확한 주입 깊이" |
| `/combination_rules/2/evidence` | `evidence` | string | "Dermatologica Sinica 2025;43(3):247-248 동물실험은 마사지 효과 지지. Wu & Goldman RCT(Dermatol Surg 2016)는 마사지군·비마사지군 결절률 차이 없음" |
| `/combination_rules/2/consensus` | `consensus` | string | "3/3 AI 합의" |
| `/combination_rules/2/priority` | `priority` | string | "important" |
| `/combination_rules/3` | `combination_rules[3]` | object(5) | _키: rule, detail, evidence, consensus, priority_ |
| `/combination_rules/3/rule` | `rule` | string | "프락셔널 후 당일 필러 금지" |
| `/combination_rules/3/detail` | `detail` | string | "열린 상처에 필러 주입 시 감염 위험. 최소 4주 간격." |
| `/combination_rules/3/evidence` | `evidence` | string | "임상 가이드라인" |
| `/combination_rules/3/consensus` | `consensus` | string | "3/3 AI 합의" |
| `/combination_rules/3/priority` | `priority` | string | "critical" |
| `/combination_rules/4` | `combination_rules[4]` | object(5) | _키: rule, detail, evidence, consensus, priority_ |
| `/combination_rules/4/rule` | `rule` | string | "기미에 고에너지 레이저 금지" |
| `/combination_rules/4/detail` | `detail` | string | "기미 환자에 고출력 레이저 시 반동 색소침착(PIH) 위험. 저출력 토닝만 권장." |
| `/combination_rules/4/evidence` | `evidence` | string | "피부과 교과서 + 다수 임상연구" |
| `/combination_rules/4/consensus` | `consensus` | string | "3/3 AI 합의" |
| `/combination_rules/4/priority` | `priority` | string | "critical" |
| `/combination_rules/5` | `combination_rules[5]` | object(5) | _키: rule, detail, evidence, consensus, priority_ |
| `/combination_rules/5/rule` | `rule` | string | "같은날 필러+보톡스 순서" |
| `/combination_rules/5/detail` | `detail` | string | "같은날: 필러 먼저 → 보톡스 나중. 필러 위치 안정화 우선, 보톡스 확산 방지." |
| `/combination_rules/5/evidence` | `evidence` | string | "임상 컨센서스" |
| `/combination_rules/5/consensus` | `consensus` | string | "3/3 AI 합의" |
| `/combination_rules/5/priority` | `priority` | string | "important" |
| `/combination_rules/6` | `combination_rules[6]` | object(5) | _키: rule, detail, evidence, consensus, priority_ |
| `/combination_rules/6/rule` | `rule` | string | "제모 부위 타 시술 간격" |
| `/combination_rules/6/detail` | `detail` | string | "레이저 제모 후 2주 내 동일 부위 필링/프락셔널 금지. 피부 장벽 회복 필요." |
| `/combination_rules/6/evidence` | `evidence` | string | "제조사 가이드 + 임상 경험" |
| `/combination_rules/6/consensus` | `consensus` | string | "3/3 AI 합의" |
| `/combination_rules/6/priority` | `priority` | string | "important" |
| `/combination_rules/7` | `combination_rules[7]` | object(5) | _키: rule, detail, evidence, consensus, priority_ |
| `/combination_rules/7/rule` | `rule` | string | "PDO실 + 비가교HA 금지" |
| `/combination_rules/7/detail` | `detail` | string | "비가교 HA가 PDO를 24-72시간 내 분해할 수 있음 (in vitro). 동시 시술 금지." |
| `/combination_rules/7/evidence` | `evidence` | string | "in vitro 연구" |
| `/combination_rules/7/consensus` | `consensus` | string | "2/3 AI 합의 (제한적 근거)" |
| `/combination_rules/7/priority` | `priority` | string | "caution" |

### 잠정 관찰 (직접 읽기 · 원문 칸과 분리 · 확정 의미 아님)

| ID | 상태 | 근거 Pointer | 관찰 |
|---|---|---|---|
| O10-1 | B | `/combination_rules/0/priority`<br>`/combination_rules/1/priority`<br>`/combination_rules/2/priority`<br>`/combination_rules/7/priority` | priority 값은 critical·important·moderate·caution 네 가지다. 값 사이 순서·척도는 원문에 정의돼 있지 않다. by_concern 의 evidence_level(high·moderate) 과 moderate 가 겹치지만 다른 칸이다. |
| O10-2 | P | `/combination_rules/0/consensus`<br>`/combination_rules/1/consensus`<br>`/combination_rules/7/consensus` | consensus 값 꼴: 「근거 기반 임상 권고」(0), 「3/3 AI 합의」(1~6), 「2/3 AI 합의 (제한적 근거)」(7). `/` 는 분수(합의 수/패널 수). consensus_method 의 3-AI 패널과 연결되는 것으로 읽히나 확정하지 않음. |
| O10-3 | P | `/combination_rules/0/detail` | detail/0 은 네 문장: (1) 「당일 시술 가능하나 웬만하면 열시술을 먼저」(양보 + 완곡 권고), (2) 「보톡스 주입 후 2주 이내 효력을 감소시킬 수 있어 HIFU를 먼저 시행하거나 2주 이상 간격」(가능성 → 두 대안), (3) 「필러 후 HIFU를 4주 이상 간격 권장하거나 HIFU를 먼저 시행」(대안), (4) 「RF·IPL·비침습 레이저는 보톡스와 당일 병행 가능하므로 HIFU와 동일한 절대 규칙으로 취급하지 않음」(범위 한정 + 부정). rule 제목 「열시술 → 주사 순서」 는 이 한정을 담지 않는다. |
| O10-4 | I | `/combination_rules/0/detail`<br>`/combination_rules/1/rule`<br>`/combination_rules/1/detail`<br>`/by_concern/0/severity_levels/2/contraindicated_combos/0` | HA 필러 뒤 HIFU 간격이 원장 안에서 다르다: combination_rules/0 「4주 이상 간격 권장」, combination_rules/1 「14일 이내 RF/HIFU 시 필러 용해 위험」·제목 「필러 → RF 14일 간격」, by_concern/0 중증 「14일 이내 RF/HIFU 금지」. 서로 다른 강도(권장/위험/금지)와 기간(4주/14일)이다(원문 내 불일치 후보, 판정 안 함). |
| O10-5 | P | `/combination_rules/1/rule`<br>`/combination_rules/1/detail` | rule 제목은 「RF」 만, detail 은 「RF/HIFU」. 「→」 는 순서(필러 다음 RF)를 나타낸다. |
| O10-6 | P | `/combination_rules/2/rule`<br>`/combination_rules/2/detail`<br>`/combination_rules/2/evidence` | rule/2 는 등식 꼴 「결절 예방 = 희석·수화·주입 깊이 (마사지는 선택)」. detail 은 「5-5-5 마사지는 기술적 보조로 권장」 → 「동물실험은 … 지지하지만 인체 RCT에서는 결절률 차이가 없었으며」 → 「핵심은 적정 희석·충분한 수화·정확한 주입 깊이」. 대조(지지하지만/없었으며)·정도(적정·충분한·정확한) 수식. 「5-5-5」 의 뜻은 원문에 없다(B). 「바이오스티뮬」 이 detail 에서 PLLA 로 좁혀진다. |
| O10-7 | I | `/combination_rules/3/rule`<br>`/combination_rules/3/detail`<br>`/by_concern/3/severity_levels/1/contraindicated_combos/0`<br>`/by_concern/3/severity_levels/2/contraindicated_combos/0` | rule/3 제목 「프락셔널 후 당일 필러 금지」 와 detail 「최소 4주 간격」: 제목은 당일만, detail 은 4주 최소 간격. by_concern 의 같은 금지문은 당일만 적는다(원문 내 불일치 후보). |
| O10-8 | I | `/combination_rules/4/detail`<br>`/by_concern/4/severity_levels/1/optimal_combo/3`<br>`/by_concern/4/severity_levels/1/contraindicated_combos/1` | rule/4 detail 「저출력 토닝만 권장」(제한 「만」) 과 by_concern/4 중등도의 「저출력 IPL(병용 보조)」 추천·「저출력·병용 보조로만」 허용이 다르다(원문 내 불일치 후보). rule 제목 「고에너지」, detail 「고출력」 표기 차이. |
| O10-9 | P | `/combination_rules/5/detail`<br>`/by_concern/0/severity_levels/1/sequence` | rule/5 「같은날: 필러 먼저 → 보톡스 나중. 필러 위치 안정화 우선, 보톡스 확산 방지.」 는 by_concern/0 중등도 「같은날: 필러→스킨부스터→보톡스」 와 방향이 같다. 목적 서술(안정화 우선·확산 방지) 이 있다. |
| O10-10 | I | `/combination_rules/6/detail`<br>`/by_concern/6/severity_levels/2/contraindicated_combos/0` | rule/6 「레이저 제모 후 2주 내 동일 부위 필링/프락셔널 금지」 와 by_concern/6 중증 「제모 부위 필링/프락셔널 동시 금지」: 기간(2주 내 vs 동시) 이 다르다(원문 내 불일치 후보). rule/6 제목 「제모 부위 타 시술 간격」 은 대상 시술을 「타 시술」 로 넓게 부른다. |
| O10-11 | P | `/combination_rules/7/detail`<br>`/combination_rules/7/consensus`<br>`/by_concern/1/severity_levels/2/contraindicated_combos/0` | rule/7 「비가교 HA가 PDO를 24-72시간 내 분해할 수 있음 (in vitro). 동시 시술 금지.」: 가능성(할 수 있음)·실험 조건(in vitro)·시간 범위·금지. consensus 「2/3 AI 합의 (제한적 근거)」, priority 「caution」. by_concern/1 중증의 「PDO실 + 비가교HA 동시 금지」 와 같은 내용이며 표기 「비가교HA」/「비가교 HA」 띄어쓰기가 다르다. 24-72시간 근거와 「동시」 의 범위 관계는 원문에 없다. |
| O10-12 | B | `/combination_rules/0/evidence`<br>`/combination_rules/1/evidence`<br>`/combination_rules/2/evidence`<br>`/combination_rules/3/evidence`<br>`/combination_rules/4/evidence`<br>`/combination_rules/5/evidence`<br>`/combination_rules/6/evidence`<br>`/combination_rules/7/evidence` | evidence 는 서지 식별 정도가 제각각이다: PMC 번호·학술지·권호·쪽이 있는 것(0·2), 연도만(0의 일부·1 「JCD 2023 논문」), 범주만(「임상 가이드라인」「피부과 교과서 + 다수 임상연구」「임상 컨센서스」「제조사 가이드 + 임상 경험」「in vitro 연구」). 원장만으로 문헌을 특정할 수 없는 값이 있다. 사실 여부는 검증하지 않았다. |

### 수동 수집 구절 (45건 · 구간은 expressions.json `source=manual_direct_reading`)

| Pointer | 원문 구절 | 탐색 관점(kinds) |
|---|---|---|
| `/combination_rules/0/rule` | 열시술 → 주사 순서 | order_sequence, category_term |
| `/combination_rules/0/detail` | 보톡스와 HIFU/RF 열시술은 당일 시술 가능하나 | same_day, possibility, concession, alternative, category_term |
| `/combination_rules/0/detail` | 웬만하면 열시술을 먼저 시행 | hedge, order_sequence, recommendation |
| `/combination_rules/0/detail` | MFU/HIFU는 보톡스 주입 후 2주 이내 효력을 감소시킬 수 있어 | possibility, interval_within, time, effect_interference, causal, abbreviation |
| `/combination_rules/0/detail` | HIFU를 먼저 시행하거나 2주 이상 간격을 둔다 | order_sequence, alternative, interval_min, time |
| `/combination_rules/0/detail` | 필러 후 HIFU를 4주 이상 간격 권장하거나 HIFU를 먼저 시행한다 | interval_min, time, recommendation, alternative, order_sequence |
| `/combination_rules/0/detail` | RF·IPL·비침습 레이저는 보톡스와 당일 병행 가능하므로 | same_day, possibility, causal, category_term, negation |
| `/combination_rules/0/detail` | HIFU와 동일한 절대 규칙으로 취급하지 않음 | negation, scope_limit, comparison |
| `/combination_rules/0/evidence` | MFU-보툴리눔독소 진피내 주입 RCT (J Cosmet Dermatol, PMC11945533) | citation, language_en, identifier, layer_depth, parenthetical |
| `/combination_rules/0/evidence` | HIFU-HA 필러 열분해 연구(2024) | citation, date, parenthetical |
| `/combination_rules/0/evidence` | 보툴리눔독소 당일 병용 안전성 리뷰(2014/2020) | citation, same_day, date, parenthetical, slash_non_alternative |
| `/combination_rules/0/consensus` | 근거 기반 임상 권고 | consensus, recommendation |
| `/combination_rules/1/rule` | 필러 → RF 14일 간격 | order_sequence, interval, time |
| `/combination_rules/1/detail` | HA 필러 주입 후 14일 이내 RF/HIFU 시 | interval_within, time, condition_when, alternative, order_sequence |
| `/combination_rules/1/detail` | 필러 용해 위험 | risk_reason |
| `/combination_rules/1/evidence` | JCD 2023 논문 | citation, date, abbreviation |
| `/combination_rules/1/consensus` | 3/3 AI 합의 | consensus, quantity_unit, slash_fraction |
| `/combination_rules/2/rule` | 바이오스티뮬 결절 예방 = 희석·수화·주입 깊이 | prevention, equation, layer_depth, abbreviation |
| `/combination_rules/2/rule` | (마사지는 선택) | parenthetical, optional |
| `/combination_rules/2/detail` | PLLA 균일 분포를 위한 5-5-5 마사지는 기술적 보조로 권장 | purpose, material, quantity_unit, adjunct, recommendation |
| `/combination_rules/2/detail` | 2025 동물실험은 균일 분포·결절 예방 효과를 지지하지만 | evidence_level_text, date, concession, prevention |
| `/combination_rules/2/detail` | 인체 RCT에서는 결절률 차이가 없었으며 | evidence_level_text, negation, comparison, language_en |
| `/combination_rules/2/detail` | 핵심은 적정 희석·충분한 수화·정확한 주입 깊이 | degree_modifier, layer_depth, requirement |
| `/combination_rules/2/evidence` | Dermatologica Sinica 2025;43(3):247-248 동물실험은 마사지 효과 지지 | citation, identifier, date, language_en |
| `/combination_rules/2/evidence` | Wu & Goldman RCT(Dermatol Surg 2016)는 마사지군·비마사지군 결절률 차이 없음 | citation, language_en, date, negation, comparison, parenthetical |
| `/combination_rules/3/rule` | 프락셔널 후 당일 필러 금지 | avoid_prohibit, same_day, order_sequence |
| `/combination_rules/3/detail` | 열린 상처에 필러 주입 시 감염 위험 | condition_when, risk_reason, target_condition |
| `/combination_rules/3/detail` | 최소 4주 간격 | interval_min, time |
| `/combination_rules/4/rule` | 기미에 고에너지 레이저 금지 | avoid_prohibit, target_condition, energy_level |
| `/combination_rules/4/detail` | 기미 환자에 고출력 레이저 시 반동 색소침착(PIH) 위험 | condition_when, target_condition, energy_level, risk_reason, parenthetical, abbreviation |
| `/combination_rules/4/detail` | 저출력 토닝만 권장 | restriction, energy_level, recommendation |
| `/combination_rules/4/evidence` | 피부과 교과서 + 다수 임상연구 | citation, plus_non_procedure, quantity_vague |
| `/combination_rules/5/rule` | 같은날 필러+보톡스 순서 | same_day, plus_list, order_sequence |
| `/combination_rules/5/detail` | 같은날: 필러 먼저 → 보톡스 나중 | same_day, order_sequence |
| `/combination_rules/5/detail` | 필러 위치 안정화 우선 | purpose, priority_preference |
| `/combination_rules/5/detail` | 보톡스 확산 방지 | purpose, prevention |
| `/combination_rules/6/rule` | 제모 부위 타 시술 간격 | body_part, interval, category_term |
| `/combination_rules/6/detail` | 레이저 제모 후 2주 내 동일 부위 필링/프락셔널 금지 | avoid_prohibit, interval_within, time, body_part, order_sequence, slash_ambiguous |
| `/combination_rules/6/detail` | 피부 장벽 회복 필요 | reason, need, recovery_period |
| `/combination_rules/6/evidence` | 제조사 가이드 + 임상 경험 | citation, plus_non_procedure |
| `/combination_rules/7/rule` | PDO실 + 비가교HA 금지 | avoid_prohibit, material, plus_in_prohibition |
| `/combination_rules/7/detail` | 비가교 HA가 PDO를 24-72시간 내 분해할 수 있음 (in vitro) | possibility, interval_within, range, time, parenthetical, language_en, effect_interference |
| `/combination_rules/7/detail` | 동시 시술 금지 | avoid_prohibit, same_time |
| `/combination_rules/7/consensus` | 2/3 AI 합의 (제한적 근거) | consensus, slash_fraction, parenthetical, evidence_limit |
| `/combination_rules/0/detail` | HA 필러는 | topic_subject, material |

### 이 구획의 미결 (issues.md 에 모음)

- **I-10-1** [I] HA 필러 → HIFU 간격: 4주 이상 권장 vs 14일 이내 위험/금지(원문 내 불일치 후보). — `/combination_rules/0/detail`, `/combination_rules/1/detail`, `/by_concern/0/severity_levels/2/contraindicated_combos/0`
- **I-10-2** [I] 프락셔널 후 필러: 제목 「당일 금지」 vs detail 「최소 4주 간격」(원문 내 불일치 후보). — `/combination_rules/3/rule`, `/combination_rules/3/detail`
- **I-10-3** [I] 기미: 「저출력 토닝만 권장」 vs 중등도 추천 「저출력 IPL(병용 보조)」(원문 내 불일치 후보). — `/combination_rules/4/detail`, `/by_concern/4/severity_levels/1/optimal_combo/3`
- **I-10-4** [I] 제모 부위 필링/프락셔널: 「2주 내」 vs 「동시」(원문 내 불일치 후보). — `/combination_rules/6/detail`, `/by_concern/6/severity_levels/2/contraindicated_combos/0`
- **B-10-1** [B] priority 네 값의 척도·순서가 원문에 없다. — `/combination_rules/0/priority`, `/combination_rules/1/priority`, `/combination_rules/2/priority`, `/combination_rules/3/priority`, `/combination_rules/4/priority`, `/combination_rules/5/priority`, `/combination_rules/6/priority`, `/combination_rules/7/priority`
- **B-10-2** [B] evidence 가 범주·연도만 있어 문헌을 특정할 수 없는 값이 있다. — `/combination_rules/1/evidence`, `/combination_rules/3/evidence`, `/combination_rules/4/evidence`, `/combination_rules/5/evidence`, `/combination_rules/6/evidence`, `/combination_rules/7/evidence`
- **B-10-3** [B] 「5-5-5 마사지」 의 정의가 원문에 없다. — `/combination_rules/2/detail`

