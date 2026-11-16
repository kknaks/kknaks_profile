# treatment-optimization.json — 1차 조사 review-part-4

> 원문 값 표는 build.py 가 원본에서 자동 생성했다. 잠정 관찰·수동 구절은 manual/seg-XX.json 의 직접 읽기 기록이다. 원장의 임상·규제 서술은 **원장에 적혀 있다는 사실**로만 기록했고 검증·보충하지 않았다.
> 상태 기호: P 잠정 · B 원문 정보 부족 · I 원문 내 불일치 후보 · F 후속 의미 조사 · K 알려진 분석 한계 · A 에이전트 추출 오류 · C 사용자 결정 필요.

[← 목차 review.md](./review.md)

<a id="seg-11"></a>
## SEG-11 — annual_plans/0

- 직접 읽기: **direct_read_done** — /annual_plans/0 (20대 피부관리 베이직 플랜) plan_name·age_group·annual_budget_range·focus 와 schedule 12개월 각 month·procedures 전 원소를 원문 순서로 직접 읽음
- 소유 노드 66 · 말단(빈 컨테이너 포함) 40

### 원문 값 (자동 생성 · 원본 컬럼명 그대로 · 원본 순서)

| Pointer | 원본 컬럼명 | 자료형 | 원문 값 |
|---|---|---|---|
| `/annual_plans/0` | `annual_plans[0]` | object(5) | _키: plan_name, age_group, annual_budget_range, focus, schedule_ |
| `/annual_plans/0/plan_name` | `plan_name` | string | "20대 피부관리 베이직 플랜" |
| `/annual_plans/0/age_group` | `age_group` | string | "20대" |
| `/annual_plans/0/annual_budget_range` | `annual_budget_range` | string | "100-250만원" |
| `/annual_plans/0/focus` | `focus` | string | "피부 기초 관리, 여드름/흉터 개선, 모공/피부결 관리" |
| `/annual_plans/0/schedule` | `schedule` | array(12) | _원소 12개_ |
| `/annual_plans/0/schedule/0` | `schedule[0]` | object(2) | _키: month, procedures_ |
| `/annual_plans/0/schedule/0/month` | `month` | integer | 1 |
| `/annual_plans/0/schedule/0/procedures` | `procedures` | array(2) | _원소 2개_ |
| `/annual_plans/0/schedule/0/procedures/0` | `procedures[0]` | string | "토닝 4회" |
| `/annual_plans/0/schedule/0/procedures/1` | `procedures[1]` | string | "필링 1회" |
| `/annual_plans/0/schedule/1` | `schedule[1]` | object(2) | _키: month, procedures_ |
| `/annual_plans/0/schedule/1/month` | `month` | integer | 2 |
| `/annual_plans/0/schedule/1/procedures` | `procedures` | array(2) | _원소 2개_ |
| `/annual_plans/0/schedule/1/procedures/0` | `procedures[0]` | string | "토닝 4회" |
| `/annual_plans/0/schedule/1/procedures/1` | `procedures[1]` | string | "스킨부스터 1차" |
| `/annual_plans/0/schedule/2` | `schedule[2]` | object(2) | _키: month, procedures_ |
| `/annual_plans/0/schedule/2/month` | `month` | integer | 3 |
| `/annual_plans/0/schedule/2/procedures` | `procedures` | array(2) | _원소 2개_ |
| `/annual_plans/0/schedule/2/procedures/0` | `procedures[0]` | string | "토닝 4회" |
| `/annual_plans/0/schedule/2/procedures/1` | `procedures[1]` | string | "필링 1회" |
| `/annual_plans/0/schedule/3` | `schedule[3]` | object(2) | _키: month, procedures_ |
| `/annual_plans/0/schedule/3/month` | `month` | integer | 4 |
| `/annual_plans/0/schedule/3/procedures` | `procedures` | array(2) | _원소 2개_ |
| `/annual_plans/0/schedule/3/procedures/0` | `procedures[0]` | string | "토닝 4회" |
| `/annual_plans/0/schedule/3/procedures/1` | `procedures[1]` | string | "IPL(색소 관리)" |
| `/annual_plans/0/schedule/4` | `schedule[4]` | object(2) | _키: month, procedures_ |
| `/annual_plans/0/schedule/4/month` | `month` | integer | 5 |
| `/annual_plans/0/schedule/4/procedures` | `procedures` | array(2) | _원소 2개_ |
| `/annual_plans/0/schedule/4/procedures/0` | `procedures[0]` | string | "스킨부스터 2차" |
| `/annual_plans/0/schedule/4/procedures/1` | `procedures[1]` | string | "토닝 4회" |
| `/annual_plans/0/schedule/5` | `schedule[5]` | object(2) | _키: month, procedures_ |
| `/annual_plans/0/schedule/5/month` | `month` | integer | 6 |
| `/annual_plans/0/schedule/5/procedures` | `procedures` | array(2) | _원소 2개_ |
| `/annual_plans/0/schedule/5/procedures/0` | `procedures[0]` | string | "토닝 4회" |
| `/annual_plans/0/schedule/5/procedures/1` | `procedures[1]` | string | "필링 1회" |
| `/annual_plans/0/schedule/6` | `schedule[6]` | object(2) | _키: month, procedures_ |
| `/annual_plans/0/schedule/6/month` | `month` | integer | 7 |
| `/annual_plans/0/schedule/6/procedures` | `procedures` | array(2) | _원소 2개_ |
| `/annual_plans/0/schedule/6/procedures/0` | `procedures[0]` | string | "토닝 4회" |
| `/annual_plans/0/schedule/6/procedures/1` | `procedures[1]` | string | "LED 집중(여름철)" |
| `/annual_plans/0/schedule/7` | `schedule[7]` | object(2) | _키: month, procedures_ |
| `/annual_plans/0/schedule/7/month` | `month` | integer | 8 |
| `/annual_plans/0/schedule/7/procedures` | `procedures` | array(2) | _원소 2개_ |
| `/annual_plans/0/schedule/7/procedures/0` | `procedures[0]` | string | "스킨부스터 3차" |
| `/annual_plans/0/schedule/7/procedures/1` | `procedures[1]` | string | "토닝 4회" |
| `/annual_plans/0/schedule/8` | `schedule[8]` | object(2) | _키: month, procedures_ |
| `/annual_plans/0/schedule/8/month` | `month` | integer | 9 |
| `/annual_plans/0/schedule/8/procedures` | `procedures` | array(2) | _원소 2개_ |
| `/annual_plans/0/schedule/8/procedures/0` | `procedures[0]` | string | "토닝 4회" |
| `/annual_plans/0/schedule/8/procedures/1` | `procedures[1]` | string | "필링 1회" |
| `/annual_plans/0/schedule/9` | `schedule[9]` | object(2) | _키: month, procedures_ |
| `/annual_plans/0/schedule/9/month` | `month` | integer | 10 |
| `/annual_plans/0/schedule/9/procedures` | `procedures` | array(2) | _원소 2개_ |
| `/annual_plans/0/schedule/9/procedures/0` | `procedures[0]` | string | "토닝 4회" |
| `/annual_plans/0/schedule/9/procedures/1` | `procedures[1]` | string | "IPL(가을 색소 관리)" |
| `/annual_plans/0/schedule/10` | `schedule[10]` | object(2) | _키: month, procedures_ |
| `/annual_plans/0/schedule/10/month` | `month` | integer | 11 |
| `/annual_plans/0/schedule/10/procedures` | `procedures` | array(2) | _원소 2개_ |
| `/annual_plans/0/schedule/10/procedures/0` | `procedures[0]` | string | "스킨부스터 4차" |
| `/annual_plans/0/schedule/10/procedures/1` | `procedures[1]` | string | "토닝 4회" |
| `/annual_plans/0/schedule/11` | `schedule[11]` | object(2) | _키: month, procedures_ |
| `/annual_plans/0/schedule/11/month` | `month` | integer | 12 |
| `/annual_plans/0/schedule/11/procedures` | `procedures` | array(2) | _원소 2개_ |
| `/annual_plans/0/schedule/11/procedures/0` | `procedures[0]` | string | "토닝 4회" |
| `/annual_plans/0/schedule/11/procedures/1` | `procedures[1]` | string | "연말 집중 케어(필링+LED)" |

### 잠정 관찰 (직접 읽기 · 원문 칸과 분리 · 확정 의미 아님)

| ID | 상태 | 근거 Pointer | 관찰 |
|---|---|---|---|
| O11-1 | P | `/annual_plans/0/annual_budget_range` | 「100-250만원」: 금액 범위 + 단위 만원. 무엇을 포함한 금액인지(시술 전부·연간 합계) 원문에 없다(B). |
| O11-2 | P | `/annual_plans/0/schedule` | schedule 은 month(정수 1~12) + procedures(문자열 배열). 월 안의 날짜·순서·같은 날 여부는 원문에 없다. procedures 배열 순서가 시행 순서인지 원문에 없다(5·8·11월은 스킨부스터가 토닝보다 앞, 2월은 뒤). |
| O11-3 | I | `/annual_plans/0/schedule/0/procedures/0`<br>`/by_age_group/0/maintenance` | plan 은 12개월 모두 「토닝 4회」, by_age_group/0(20대) maintenance 는 「토닝 월 1-2회」. 월 횟수가 다르다(원문 내 불일치 후보. plan 은 집중기·maintenance 는 유지기일 가능성이 있으나 원문에 근거 없음). |
| O11-4 | I | `/annual_plans/0/schedule/0/procedures/1`<br>`/annual_plans/0/schedule/2/procedures/1`<br>`/annual_plans/0/schedule/5/procedures/1`<br>`/annual_plans/0/schedule/8/procedures/1`<br>`/by_age_group/0/maintenance` | 「필링 1회」 는 1·3·6·9월(연 4회, 12월은 「연말 집중 케어(필링+LED)」), by_age_group/0 maintenance 는 「필링 월 1회」(원문 내 불일치 후보). |
| O11-5 | P | `/annual_plans/0/schedule/1/procedures/1`<br>`/annual_plans/0/schedule/4/procedures/0`<br>`/annual_plans/0/schedule/7/procedures/0`<br>`/annual_plans/0/schedule/10/procedures/0` | 「스킨부스터 1차~4차」 는 2·5·8·11월(3개월 간격). by_age_group/0 maintenance 「스킨부스터 분기 1회」 와 같은 빈도로 읽힌다(잠정). 「차」 는 시리즈 차수. |
| O11-6 | P | `/annual_plans/0/schedule/3/procedures/1`<br>`/annual_plans/0/schedule/6/procedures/1`<br>`/annual_plans/0/schedule/9/procedures/1`<br>`/annual_plans/0/schedule/11/procedures/1` | 괄호가 목적·계절·시기를 담는다: 「IPL(색소 관리)」, 「LED 집중(여름철)」, 「IPL(가을 색소 관리)」, 「연말 집중 케어(필링+LED)」. 마지막은 괄호 안 `+` 가 함께 시술(README 와 같은 꼴), 괄호 밖은 시술명이 아닌 묶음 이름. |
| O11-7 | P | `/annual_plans/0/schedule/3/procedures/1`<br>`/by_age_group/0/recommended_base` | 20대 by_age_group recommended_base 에 IPL 이 없지만 plan 에는 IPL 이 2회 있다. 추천 기본과 플랜의 관계는 원문에 없다(충돌 판정 안 함). |
| O11-8 | P | `/annual_plans/0/focus`<br>`/by_age_group/0/annual_focus` | focus 「피부 기초 관리, 여드름/흉터 개선, 모공/피부결 관리」 는 by_age_group/0 annual_focus 「피부 기초 관리, 여드름/흉터 집중 치료, 자외선 차단 습관화」 와 첫 항목만 같다. |

### 수동 수집 구절 (13건 · 구간은 expressions.json `source=manual_direct_reading`)

| Pointer | 원문 구절 | 탐색 관점(kinds) |
|---|---|---|
| `/annual_plans/0/plan_name` | 20대 피부관리 베이직 플랜 | age, plan_name, language_mixed |
| `/annual_plans/0/annual_budget_range` | 100-250만원 | cost, range, quantity_unit |
| `/annual_plans/0/focus` | 여드름/흉터 개선 | focus, slash_non_alternative |
| `/annual_plans/0/focus` | 모공/피부결 관리 | focus, slash_non_alternative |
| `/annual_plans/0/schedule/0/procedures/0` | 토닝 4회 | session_count, monthly_count |
| `/annual_plans/0/schedule/1/procedures/1` | 스킨부스터 1차 | series_order |
| `/annual_plans/0/schedule/3/procedures/1` | IPL(색소 관리) | procedure_like, parenthetical, purpose |
| `/annual_plans/0/schedule/4/procedures/0` | 스킨부스터 2차 | series_order |
| `/annual_plans/0/schedule/6/procedures/1` | LED 집중(여름철) | procedure_like, degree_modifier, parenthetical, season |
| `/annual_plans/0/schedule/7/procedures/0` | 스킨부스터 3차 | series_order |
| `/annual_plans/0/schedule/9/procedures/1` | IPL(가을 색소 관리) | procedure_like, parenthetical, season, purpose |
| `/annual_plans/0/schedule/10/procedures/0` | 스킨부스터 4차 | series_order |
| `/annual_plans/0/schedule/11/procedures/1` | 연말 집중 케어(필링+LED) | season, degree_modifier, parenthetical, plus_list, bundle_name |

### 이 구획의 미결 (issues.md 에 모음)

- **I-11-1** [I] 20대 토닝·필링 빈도: plan(토닝 매월 4회·필링 연 4회) vs maintenance(토닝 월 1-2회·필링 월 1회)(원문 내 불일치 후보). — `/annual_plans/0/schedule`, `/by_age_group/0/maintenance`
- **B-11-1** [B] 월 안의 날짜·순서·같은 날 여부와 procedures 배열 순서의 뜻이 원문에 없다. 같은 달 항목에 동일일·간격 규칙을 적용할 수 없다. — `/annual_plans/0/schedule`
- **B-11-2** [B] 예산 범위가 무엇을 포함하는지 원문에 없다. — `/annual_plans/0/annual_budget_range`

<a id="seg-12"></a>
## SEG-12 — annual_plans/1

- 직접 읽기: **direct_read_done** — /annual_plans/1 (30대 동안 유지 플랜) 상위 필드와 schedule 12개월 각 month·procedures 전 원소를 원문 순서로 직접 읽음
- 소유 노드 64 · 말단(빈 컨테이너 포함) 38

### 원문 값 (자동 생성 · 원본 컬럼명 그대로 · 원본 순서)

| Pointer | 원본 컬럼명 | 자료형 | 원문 값 |
|---|---|---|---|
| `/annual_plans/1` | `annual_plans[1]` | object(5) | _키: plan_name, age_group, annual_budget_range, focus, schedule_ |
| `/annual_plans/1/plan_name` | `plan_name` | string | "30대 동안 유지 플랜" |
| `/annual_plans/1/age_group` | `age_group` | string | "30대" |
| `/annual_plans/1/annual_budget_range` | `annual_budget_range` | string | "200-500만원" |
| `/annual_plans/1/focus` | `focus` | string | "노화 예방, 동적주름 관리, 콜라겐 투자 시작" |
| `/annual_plans/1/schedule` | `schedule` | array(12) | _원소 12개_ |
| `/annual_plans/1/schedule/0` | `schedule[0]` | object(2) | _키: month, procedures_ |
| `/annual_plans/1/schedule/0/month` | `month` | integer | 1 |
| `/annual_plans/1/schedule/0/procedures` | `procedures` | array(2) | _원소 2개_ |
| `/annual_plans/1/schedule/0/procedures/0` | `procedures[0]` | string | "보톡스 이마+미간" |
| `/annual_plans/1/schedule/0/procedures/1` | `procedures[1]` | string | "스킨부스터" |
| `/annual_plans/1/schedule/1` | `schedule[1]` | object(2) | _키: month, procedures_ |
| `/annual_plans/1/schedule/1/month` | `month` | integer | 2 |
| `/annual_plans/1/schedule/1/procedures` | `procedures` | array(1) | _원소 1개_ |
| `/annual_plans/1/schedule/1/procedures/0` | `procedures[0]` | string | "토닝 4회" |
| `/annual_plans/1/schedule/2` | `schedule[2]` | object(2) | _키: month, procedures_ |
| `/annual_plans/1/schedule/2/month` | `month` | integer | 3 |
| `/annual_plans/1/schedule/2/procedures` | `procedures` | array(2) | _원소 2개_ |
| `/annual_plans/1/schedule/2/procedures/0` | `procedures[0]` | string | "보톡스 터치업" |
| `/annual_plans/1/schedule/2/procedures/1` | `procedures[1]` | string | "IPL" |
| `/annual_plans/1/schedule/3` | `schedule[3]` | object(2) | _키: month, procedures_ |
| `/annual_plans/1/schedule/3/month` | `month` | integer | 4 |
| `/annual_plans/1/schedule/3/procedures` | `procedures` | array(2) | _원소 2개_ |
| `/annual_plans/1/schedule/3/procedures/0` | `procedures[0]` | string | "스킨부스터" |
| `/annual_plans/1/schedule/3/procedures/1` | `procedures[1]` | string | "토닝 4회" |
| `/annual_plans/1/schedule/4` | `schedule[4]` | object(2) | _키: month, procedures_ |
| `/annual_plans/1/schedule/4/month` | `month` | integer | 5 |
| `/annual_plans/1/schedule/4/procedures` | `procedures` | array(1) | _원소 1개_ |
| `/annual_plans/1/schedule/4/procedures/0` | `procedures[0]` | string | "토닝 4회" |
| `/annual_plans/1/schedule/5` | `schedule[5]` | object(2) | _키: month, procedures_ |
| `/annual_plans/1/schedule/5/month` | `month` | integer | 6 |
| `/annual_plans/1/schedule/5/procedures` | `procedures` | array(2) | _원소 2개_ |
| `/annual_plans/1/schedule/5/procedures/0` | `procedures[0]` | string | "보톡스" |
| `/annual_plans/1/schedule/5/procedures/1` | `procedures[1]` | string | "바이오스티뮬레이터 1차" |
| `/annual_plans/1/schedule/6` | `schedule[6]` | object(2) | _키: month, procedures_ |
| `/annual_plans/1/schedule/6/month` | `month` | integer | 7 |
| `/annual_plans/1/schedule/6/procedures` | `procedures` | array(2) | _원소 2개_ |
| `/annual_plans/1/schedule/6/procedures/0` | `procedures[0]` | string | "바이오스티뮬레이터 2차" |
| `/annual_plans/1/schedule/6/procedures/1` | `procedures[1]` | string | "토닝 4회" |
| `/annual_plans/1/schedule/7` | `schedule[7]` | object(2) | _키: month, procedures_ |
| `/annual_plans/1/schedule/7/month` | `month` | integer | 8 |
| `/annual_plans/1/schedule/7/procedures` | `procedures` | array(2) | _원소 2개_ |
| `/annual_plans/1/schedule/7/procedures/0` | `procedures[0]` | string | "바이오스티뮬레이터 3차" |
| `/annual_plans/1/schedule/7/procedures/1` | `procedures[1]` | string | "스킨부스터" |
| `/annual_plans/1/schedule/8` | `schedule[8]` | object(2) | _키: month, procedures_ |
| `/annual_plans/1/schedule/8/month` | `month` | integer | 9 |
| `/annual_plans/1/schedule/8/procedures` | `procedures` | array(2) | _원소 2개_ |
| `/annual_plans/1/schedule/8/procedures/0` | `procedures[0]` | string | "보톡스" |
| `/annual_plans/1/schedule/8/procedures/1` | `procedures[1]` | string | "토닝 4회" |
| `/annual_plans/1/schedule/9` | `schedule[9]` | object(2) | _키: month, procedures_ |
| `/annual_plans/1/schedule/9/month` | `month` | integer | 10 |
| `/annual_plans/1/schedule/9/procedures` | `procedures` | array(2) | _원소 2개_ |
| `/annual_plans/1/schedule/9/procedures/0` | `procedures[0]` | string | "IPL" |
| `/annual_plans/1/schedule/9/procedures/1` | `procedures[1]` | string | "토닝 4회" |
| `/annual_plans/1/schedule/10` | `schedule[10]` | object(2) | _키: month, procedures_ |
| `/annual_plans/1/schedule/10/month` | `month` | integer | 11 |
| `/annual_plans/1/schedule/10/procedures` | `procedures` | array(2) | _원소 2개_ |
| `/annual_plans/1/schedule/10/procedures/0` | `procedures[0]` | string | "스킨부스터" |
| `/annual_plans/1/schedule/10/procedures/1` | `procedures[1]` | string | "토닝 4회" |
| `/annual_plans/1/schedule/11` | `schedule[11]` | object(2) | _키: month, procedures_ |
| `/annual_plans/1/schedule/11/month` | `month` | integer | 12 |
| `/annual_plans/1/schedule/11/procedures` | `procedures` | array(2) | _원소 2개_ |
| `/annual_plans/1/schedule/11/procedures/0` | `procedures[0]` | string | "보톡스" |
| `/annual_plans/1/schedule/11/procedures/1` | `procedures[1]` | string | "연말 특별 관리(필링+LED)" |

### 잠정 관찰 (직접 읽기 · 원문 칸과 분리 · 확정 의미 아님)

| ID | 상태 | 근거 Pointer | 관찰 |
|---|---|---|---|
| O12-1 | P | `/annual_plans/1/schedule/0/procedures/0` | 「보톡스 이마+미간」: README 「부위 나열은 +」 예시와 같은 문자열. 이 원장에서 부위가 괄호 없이 띄어 붙는 유일한 보톡스 표기다(다른 곳은 「보톡스(턱선+광대)」). |
| O12-2 | P | `/annual_plans/1/schedule/0/procedures/0`<br>`/annual_plans/1/schedule/2/procedures/0`<br>`/annual_plans/1/schedule/5/procedures/0`<br>`/annual_plans/1/schedule/8/procedures/0`<br>`/annual_plans/1/schedule/11/procedures/0`<br>`/by_age_group/1/maintenance` | 보톡스는 1월(이마+미간)·3월(터치업)·6·9·12월. 「터치업」 은 보완 시술로 읽히며 회차 셈에 들어가는지 원문에 없다(B). 1·6·9·12월 간격은 by_age_group/1 「보톡스 3-4개월」 과 대체로 맞으나 1→6월은 5개월이다(판정 안 함). |
| O12-3 | P | `/annual_plans/1/schedule/5/procedures/1`<br>`/annual_plans/1/schedule/6/procedures/0`<br>`/annual_plans/1/schedule/7/procedures/0` | 「바이오스티뮬레이터 1차~3차」 가 6·7·8월 연속(월 1회). 같은 원장 by_concern 의 「4주 간격」 표현과 같은 뜻인지 연결하지 않았다. |
| O12-4 | P | `/annual_plans/1/schedule/0/procedures/1`<br>`/annual_plans/1/schedule/3/procedures/0`<br>`/annual_plans/1/schedule/7/procedures/1`<br>`/annual_plans/1/schedule/10/procedures/0` | 「스킨부스터」 는 1·4·8·11월에 차수 없이 쓰인다(20대 플랜은 차수 표기). |
| O12-5 | I | `/annual_plans/1/schedule/1/procedures/0`<br>`/by_age_group/1/maintenance` | 「토닝 4회」 가 7개월(2·4·5·7·9·10·11월)에 있고 by_age_group/1 maintenance 는 「토닝 월 1-2회」(원문 내 불일치 후보, SEG-11 과 같은 꼴). |
| O12-6 | B | `/annual_plans/1/schedule/5/procedures`<br>`/annual_plans/1/schedule/0/procedures` | 같은 달에 보톡스+바이오스티뮬레이터(6월), 보톡스+스킨부스터(1월)가 있다. 같은 날인지·순서는 원문에 없다. |
| O12-7 | P | `/annual_plans/1/focus`<br>`/by_age_group/1/annual_focus` | focus 「노화 예방, 동적주름 관리, 콜라겐 투자 시작」 은 by_age_group/1 annual_focus 와 표현이 거의 같다(「노화 예방 시작」 vs 「노화 예방」, 「보톡스로 동적주름 관리」 vs 「동적주름 관리」). |

### 수동 수집 구절 (9건 · 구간은 expressions.json `source=manual_direct_reading`)

| Pointer | 원문 구절 | 탐색 관점(kinds) |
|---|---|---|
| `/annual_plans/1/plan_name` | 30대 동안 유지 플랜 | age, plan_name, maintenance |
| `/annual_plans/1/annual_budget_range` | 200-500만원 | cost, range, quantity_unit |
| `/annual_plans/1/focus` | 콜라겐 투자 시작 | focus, series_start |
| `/annual_plans/1/schedule/0/procedures/0` | 보톡스 이마+미간 | procedure_like, body_part, plus_list |
| `/annual_plans/1/schedule/2/procedures/0` | 보톡스 터치업 | touch_up, language_mixed |
| `/annual_plans/1/schedule/5/procedures/1` | 바이오스티뮬레이터 1차 | series_order |
| `/annual_plans/1/schedule/6/procedures/0` | 바이오스티뮬레이터 2차 | series_order |
| `/annual_plans/1/schedule/7/procedures/0` | 바이오스티뮬레이터 3차 | series_order |
| `/annual_plans/1/schedule/11/procedures/1` | 연말 특별 관리(필링+LED) | season, degree_modifier, parenthetical, plus_list, bundle_name |

### 이 구획의 미결 (issues.md 에 모음)

- **I-12-1** [I] 30대 토닝 빈도: plan 월 4회 vs maintenance 월 1-2회(원문 내 불일치 후보). — `/annual_plans/1/schedule`, `/by_age_group/1/maintenance`
- **B-12-1** [B] 「터치업」 의 범위(부위·용량)와 회차 셈 포함 여부가 원문에 없다. — `/annual_plans/1/schedule/2/procedures/0`

<a id="seg-13"></a>
## SEG-13 — annual_plans/2

- 직접 읽기: **direct_read_done** — /annual_plans/2 (40대+ 안티에이징 집중 플랜) 상위 필드와 schedule 12개월 각 month·procedures 전 원소(월당 2~3개)를 원문 순서로 직접 읽음
- 소유 노드 73 · 말단(빈 컨테이너 포함) 47

### 원문 값 (자동 생성 · 원본 컬럼명 그대로 · 원본 순서)

| Pointer | 원본 컬럼명 | 자료형 | 원문 값 |
|---|---|---|---|
| `/annual_plans/2` | `annual_plans[2]` | object(5) | _키: plan_name, age_group, annual_budget_range, focus, schedule_ |
| `/annual_plans/2/plan_name` | `plan_name` | string | "40대+ 안티에이징 집중 플랜" |
| `/annual_plans/2/age_group` | `age_group` | string | "40대+" |
| `/annual_plans/2/annual_budget_range` | `annual_budget_range` | string | "400-1000만원" |
| `/annual_plans/2/focus` | `focus` | string | "처짐/주름 적극 관리, 볼륨 복원, 복합 시술 조합" |
| `/annual_plans/2/schedule` | `schedule` | array(12) | _원소 12개_ |
| `/annual_plans/2/schedule/0` | `schedule[0]` | object(2) | _키: month, procedures_ |
| `/annual_plans/2/schedule/0/month` | `month` | integer | 1 |
| `/annual_plans/2/schedule/0/procedures` | `procedures` | array(3) | _원소 3개_ |
| `/annual_plans/2/schedule/0/procedures/0` | `procedures[0]` | string | "보톡스 풀페이스" |
| `/annual_plans/2/schedule/0/procedures/1` | `procedures[1]` | string | "스킨부스터" |
| `/annual_plans/2/schedule/0/procedures/2` | `procedures[2]` | string | "토닝 4회" |
| `/annual_plans/2/schedule/1` | `schedule[1]` | object(2) | _키: month, procedures_ |
| `/annual_plans/2/schedule/1/month` | `month` | integer | 2 |
| `/annual_plans/2/schedule/1/procedures` | `procedures` | array(2) | _원소 2개_ |
| `/annual_plans/2/schedule/1/procedures/0` | `procedures[0]` | string | "HIFU(울쎄라/슈링크)" |
| `/annual_plans/2/schedule/1/procedures/1` | `procedures[1]` | string | "토닝 2회" |
| `/annual_plans/2/schedule/2` | `schedule[2]` | object(2) | _키: month, procedures_ |
| `/annual_plans/2/schedule/2/month` | `month` | integer | 3 |
| `/annual_plans/2/schedule/2/procedures` | `procedures` | array(2) | _원소 2개_ |
| `/annual_plans/2/schedule/2/procedures/0` | `procedures[0]` | string | "필러(팔자/볼)" |
| `/annual_plans/2/schedule/2/procedures/1` | `procedures[1]` | string | "토닝 4회" |
| `/annual_plans/2/schedule/3` | `schedule[3]` | object(2) | _키: month, procedures_ |
| `/annual_plans/2/schedule/3/month` | `month` | integer | 4 |
| `/annual_plans/2/schedule/3/procedures` | `procedures` | array(3) | _원소 3개_ |
| `/annual_plans/2/schedule/3/procedures/0` | `procedures[0]` | string | "보톡스 터치업" |
| `/annual_plans/2/schedule/3/procedures/1` | `procedures[1]` | string | "바이오스티뮬레이터 1차" |
| `/annual_plans/2/schedule/3/procedures/2` | `procedures[2]` | string | "IPL" |
| `/annual_plans/2/schedule/4` | `schedule[4]` | object(2) | _키: month, procedures_ |
| `/annual_plans/2/schedule/4/month` | `month` | integer | 5 |
| `/annual_plans/2/schedule/4/procedures` | `procedures` | array(3) | _원소 3개_ |
| `/annual_plans/2/schedule/4/procedures/0` | `procedures[0]` | string | "바이오스티뮬레이터 2차" |
| `/annual_plans/2/schedule/4/procedures/1` | `procedures[1]` | string | "스킨부스터" |
| `/annual_plans/2/schedule/4/procedures/2` | `procedures[2]` | string | "토닝 4회" |
| `/annual_plans/2/schedule/5` | `schedule[5]` | object(2) | _키: month, procedures_ |
| `/annual_plans/2/schedule/5/month` | `month` | integer | 6 |
| `/annual_plans/2/schedule/5/procedures` | `procedures` | array(2) | _원소 2개_ |
| `/annual_plans/2/schedule/5/procedures/0` | `procedures[0]` | string | "바이오스티뮬레이터 3차" |
| `/annual_plans/2/schedule/5/procedures/1` | `procedures[1]` | string | "토닝 4회" |
| `/annual_plans/2/schedule/6` | `schedule[6]` | object(2) | _키: month, procedures_ |
| `/annual_plans/2/schedule/6/month` | `month` | integer | 7 |
| `/annual_plans/2/schedule/6/procedures` | `procedures` | array(3) | _원소 3개_ |
| `/annual_plans/2/schedule/6/procedures/0` | `procedures[0]` | string | "보톡스" |
| `/annual_plans/2/schedule/6/procedures/1` | `procedures[1]` | string | "프락셔널(피부결)" |
| `/annual_plans/2/schedule/6/procedures/2` | `procedures[2]` | string | "토닝 2회" |
| `/annual_plans/2/schedule/7` | `schedule[7]` | object(2) | _키: month, procedures_ |
| `/annual_plans/2/schedule/7/month` | `month` | integer | 8 |
| `/annual_plans/2/schedule/7/procedures` | `procedures` | array(2) | _원소 2개_ |
| `/annual_plans/2/schedule/7/procedures/0` | `procedures[0]` | string | "HIFU/RF(하반기)" |
| `/annual_plans/2/schedule/7/procedures/1` | `procedures[1]` | string | "스킨부스터" |
| `/annual_plans/2/schedule/8` | `schedule[8]` | object(2) | _키: month, procedures_ |
| `/annual_plans/2/schedule/8/month` | `month` | integer | 9 |
| `/annual_plans/2/schedule/8/procedures` | `procedures` | array(2) | _원소 2개_ |
| `/annual_plans/2/schedule/8/procedures/0` | `procedures[0]` | string | "필러 터치업" |
| `/annual_plans/2/schedule/8/procedures/1` | `procedures[1]` | string | "토닝 4회" |
| `/annual_plans/2/schedule/9` | `schedule[9]` | object(2) | _키: month, procedures_ |
| `/annual_plans/2/schedule/9/month` | `month` | integer | 10 |
| `/annual_plans/2/schedule/9/procedures` | `procedures` | array(3) | _원소 3개_ |
| `/annual_plans/2/schedule/9/procedures/0` | `procedures[0]` | string | "보톡스" |
| `/annual_plans/2/schedule/9/procedures/1` | `procedures[1]` | string | "IPL(가을 색소)" |
| `/annual_plans/2/schedule/9/procedures/2` | `procedures[2]` | string | "토닝 4회" |
| `/annual_plans/2/schedule/10` | `schedule[10]` | object(2) | _키: month, procedures_ |
| `/annual_plans/2/schedule/10/month` | `month` | integer | 11 |
| `/annual_plans/2/schedule/10/procedures` | `procedures` | array(3) | _원소 3개_ |
| `/annual_plans/2/schedule/10/procedures/0` | `procedures[0]` | string | "스킨부스터" |
| `/annual_plans/2/schedule/10/procedures/1` | `procedures[1]` | string | "바이오스티뮬레이터(유지 1차)" |
| `/annual_plans/2/schedule/10/procedures/2` | `procedures[2]` | string | "토닝 4회" |
| `/annual_plans/2/schedule/11` | `schedule[11]` | object(2) | _키: month, procedures_ |
| `/annual_plans/2/schedule/11/month` | `month` | integer | 12 |
| `/annual_plans/2/schedule/11/procedures` | `procedures` | array(3) | _원소 3개_ |
| `/annual_plans/2/schedule/11/procedures/0` | `procedures[0]` | string | "보톡스" |
| `/annual_plans/2/schedule/11/procedures/1` | `procedures[1]` | string | "연말 리프팅 관리(RF/HIFU 터치)" |
| `/annual_plans/2/schedule/11/procedures/2` | `procedures[2]` | string | "토닝 2회" |

### 잠정 관찰 (직접 읽기 · 원문 칸과 분리 · 확정 의미 아님)

| ID | 상태 | 근거 Pointer | 관찰 |
|---|---|---|---|
| O13-1 | B | `/annual_plans/2/age_group`<br>`/by_age_group/2/age`<br>`/by_age_group/3/age` | age_group 「40대+」 는 by_age_group 의 「40대」·「50대+」 어느 쪽과도 같은 문자열이 아니다. 두 연령대를 모두 덮는지 원문에 없다. 50대+ 전용 플랜은 없다. |
| O13-2 | P | `/annual_plans/2/schedule/1/procedures/0`<br>`/by_concern/1/severity_levels/1/optimal_combo/0` | 「HIFU(울쎄라/슈링크)」 는 by_concern 의 「HIFU(슈링크/울쎄라)」 와 괄호 안 순서가 반대다. |
| O13-3 | P | `/annual_plans/2/schedule/2/procedures/0` | 「필러(팔자/볼)」: 괄호 안은 부위이고 `/` 로 잇는다. README 는 부위 나열에 `+`, 대안에 `/` 를 쓰도록 하므로 이 표기는 「팔자 또는 볼」 로 읽힐 수 있다. 원문 의도(둘 다/둘 중 하나)는 정하지 않았다(F). |
| O13-4 | P | `/annual_plans/2/schedule/1/procedures/1`<br>`/annual_plans/2/schedule/6/procedures/2`<br>`/annual_plans/2/schedule/11/procedures/2` | 토닝 회수가 월마다 다르다: 2·7·12월 「토닝 2회」, 나머지 대부분 「토닝 4회」, 4·8월은 토닝 없음. HIFU(2월)·프락셔널(7월)·리프팅 관리(12월) 달에 2회로 줄어든다(잠정 관찰, 이유는 원문에 없음). |
| O13-5 | P | `/annual_plans/2/schedule/1/procedures/0`<br>`/annual_plans/2/schedule/7/procedures/0`<br>`/annual_plans/2/schedule/11/procedures/1`<br>`/by_age_group/2/maintenance` | HIFU 계열은 2월 「HIFU(울쎄라/슈링크)」, 8월 「HIFU/RF(하반기)」, 12월 「연말 리프팅 관리(RF/HIFU 터치)」. 8→12월은 4개월이다. by_age_group/2 maintenance 「HIFU 6개월+」 와 12월 「터치」 의 관계(같은 HIFU 회차로 보는지)는 원문에 없다(판정 안 함). `/` 순서가 HIFU/RF 와 RF/HIFU 로 바뀐다. |
| O13-6 | P | `/annual_plans/2/schedule/2/procedures/0`<br>`/annual_plans/2/schedule/8/procedures/0`<br>`/by_age_group/2/maintenance` | 필러 3월·필러 터치업 9월(6개월). by_age_group/2 「필러 6개월+」 와 맞는 간격으로 읽히나 터치업을 같은 회차로 보는지 원문에 없다. |
| O13-7 | P | `/annual_plans/2/schedule/3/procedures/1`<br>`/annual_plans/2/schedule/4/procedures/0`<br>`/annual_plans/2/schedule/5/procedures/0`<br>`/annual_plans/2/schedule/10/procedures/1` | 바이오스티뮬레이터 1~3차(4·5·6월) 뒤 11월 「바이오스티뮬레이터(유지 1차)」: 시리즈 차수와 유지 차수를 따로 센다. |
| O13-8 | B | `/annual_plans/2/schedule/0/procedures`<br>`/annual_plans/2/schedule/6/procedures`<br>`/annual_plans/2/schedule/3/procedures` | 같은 달에 보톡스+스킨부스터+토닝(1월), 보톡스+프락셔널+토닝(7월), 보톡스 터치업+바이오스티뮬레이터+IPL(4월)이 있다. combination_rules 의 동일일·순서 규칙을 이 달들에 적용할 날짜 정보가 원문에 없다. |
| O13-9 | P | `/annual_plans/2/schedule/0/procedures/0`<br>`/annual_plans/2/schedule/7/procedures/0`<br>`/annual_plans/2/schedule/9/procedures/1`<br>`/annual_plans/2/schedule/6/procedures/1` | 괄호의 역할: 「보톡스 풀페이스」(부위, 괄호 없음), 「HIFU/RF(하반기)」(시기), 「IPL(가을 색소)」(계절+대상), 「프락셔널(피부결)」(대상). |

### 수동 수집 구절 (17건 · 구간은 expressions.json `source=manual_direct_reading`)

| Pointer | 원문 구절 | 탐색 관점(kinds) |
|---|---|---|
| `/annual_plans/2/plan_name` | 40대+ 안티에이징 집중 플랜 | age, open_ended, plan_name, degree_modifier |
| `/annual_plans/2/age_group` | 40대+ | age, open_ended, plus_non_procedure |
| `/annual_plans/2/annual_budget_range` | 400-1000만원 | cost, range, quantity_unit |
| `/annual_plans/2/focus` | 처짐/주름 적극 관리 | focus, degree_modifier, slash_non_alternative |
| `/annual_plans/2/focus` | 볼륨 복원 | focus, effect_purpose |
| `/annual_plans/2/focus` | 복합 시술 조합 | focus, combination |
| `/annual_plans/2/schedule/0/procedures/0` | 보톡스 풀페이스 | procedure_like, body_part, range_area, language_mixed |
| `/annual_plans/2/schedule/1/procedures/0` | HIFU(울쎄라/슈링크) | procedure_like, product_like, parenthetical, alternative |
| `/annual_plans/2/schedule/1/procedures/1` | 토닝 2회 | session_count, monthly_count |
| `/annual_plans/2/schedule/2/procedures/0` | 필러(팔자/볼) | procedure_like, body_part, parenthetical, slash_ambiguous |
| `/annual_plans/2/schedule/3/procedures/0` | 보톡스 터치업 | touch_up, language_mixed |
| `/annual_plans/2/schedule/6/procedures/1` | 프락셔널(피부결) | procedure_like, parenthetical, target_concern |
| `/annual_plans/2/schedule/7/procedures/0` | HIFU/RF(하반기) | procedure_like, alternative, parenthetical, season |
| `/annual_plans/2/schedule/8/procedures/0` | 필러 터치업 | touch_up, language_mixed |
| `/annual_plans/2/schedule/9/procedures/1` | IPL(가을 색소) | procedure_like, parenthetical, season, target_concern |
| `/annual_plans/2/schedule/10/procedures/1` | 바이오스티뮬레이터(유지 1차) | parenthetical, maintenance, series_order |
| `/annual_plans/2/schedule/11/procedures/1` | 연말 리프팅 관리(RF/HIFU 터치) | season, parenthetical, alternative, touch_up, bundle_name |

### 이 구획의 미결 (issues.md 에 모음)

- **B-13-1** [B] 「40대+」 가 by_age_group 의 40대·50대+ 중 무엇을 덮는지 원문에 없다. — `/annual_plans/2/age_group`
- **B-13-2** [B] 같은 달 여러 시술의 날짜·순서가 원문에 없어 동일일·간격 규칙 적용 여부를 판단할 수 없다. — `/annual_plans/2/schedule`

