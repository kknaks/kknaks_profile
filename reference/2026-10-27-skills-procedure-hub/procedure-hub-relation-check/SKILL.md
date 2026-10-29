---
name: procedure-hub-relation-check
description: 시술↔시술 관계(시너지 · 순서 · 간격 · 같은 날 · 금기 · 대체) · 확인 조건(사람 조건 금기 · 사전 체크 · 연령) · 고민 조건 금기(피함) · 안전(합병증 · 위험지대 · 경과표 · PIH · 고지 · 사후관리) · 근거(문헌 · 문장 · 웹 · 가이드) 원천이 들어오거나 바뀌거나, 원천 질문 답이 왔을 때 Procedure Hub 실버 관계 원장(step8-relations)을 갱신한다. 사람 확인 게이트 없이 규칙으로만 — 이름은 5단계 정본 → 조사 사전 순으로 풀고(고르지 않음 · 후보 전부 + 표시) → 원칙 · 규칙 · 위험 · 화살표 문장은 문장 패턴(sentence.patterns)으로 쌍을 만들고 → 간격은 간격 낱말 사전(interval_lexicon)으로 숫자 칸(interval.days · first · same_day)만 채우고 → 고민 낱말은 7단계 고민 노드로만(「피함」 엣지) → 사람 조건은 확인 조건 사전으로 → 충돌은 전부 보존 + 표시 → 규칙으로 하나로 안 정해지는 것만 원천 질문 순으로 판정한다. 결정 파일 한 줄만 고친 뒤 step8-apply.py 로 결정론 반영하고, 끝 조건은 open 0 · 두 번 실행 cmp 같음 · 고정 시험 전부 PASS · check_relations errors 0. 트리거 예 — 「시너지 · 순서 원천 바뀌었어」「새 금기 문장 들어왔어」「이 간격 문장 숫자로 어떻게 읽어」「원천 질문 답 왔어(이소트레티노인 · 보톡스 필러 순서 …)」「사전 체크 항목 늘었어」「합병증 · 위험지대 원천 바뀌었어」「step8-apply 가 open 을 냈어」「step8-relations 갱신」「관계 원장 점검」.
---

# Procedure Hub 관계 판정 · 실버 관계 원장 갱신

실버 8단계(관계 · 확인 조건 · 안전 · 근거, 2026-10-29)에서 실제로 한 방법을 옮긴 것이다. 새로 지어낸 절차가 아니다.
7단계(고민 — `procedure-hub-concern-check`) 다음 단계다. 시술과 시술 사이의 말(같이 해도 되나 · 무엇을 먼저 · 며칠 띄우나 · 같은 날 되나 · 하면 안 되나)과
사람 · 고민 쪽 금기, 안전 원문, 근거를 **원천에 적힌 만큼** 엣지 · 속성 · 노드로 옮긴다.

- 정본 원장: `orchestration/work/phub-recommend/step8-relations.json` · `.md` · `step8-origin-questions.md` — 현재 값 = `scripts/check_relations.py` 출력. 숫자를 여기 박지 않는다(규칙 한 줄이 바뀌면 주장 · 충돌 셈이 바뀐다 — 8단계에서도 조사 판(행별 대응표)과 반영 판(문장 패턴)의 원천별 주장 수가 달랐다)
- 결정(사람이 고치는 곳): `step8-decisions.json` — 이름 풀이 `resolver`(5단계 다음 조사 사전 `alias` · 꼬리 낱말 · 앞 낱말) · 간격 낱말 사전 `interval_lexicon`(`branches` · `word_branches`) · 문장 패턴 `sentence.patterns` · 확인 조건 사전 `conditions` · 사람 조건 아닌 문장 `not_person_rules` · 연령 패턴 `age_avoid_patterns` · 피함 엣지 타입 `avoid_edge_type` · 경과표 붙는 곳 `timeline_attach` · 8단계 칸 반영 규칙 `field_handlers` · 원천 질문 `origin_questions` · 넓은 후보 기준 `wide_candidates_*` · 원천 질문 아닌 용도 낱말 `purpose_ok` · 사용자 판단 `user_decisions`
- 결정론 반영: `step8-apply.py`(입력 = 결정 · 원천 18파일 · 1~7단계 정본 · source-map → 출력 `step8-relations.json` · `.md` · `step8-origin-questions.md`) · 가드 시험 `step8-fixture-test.py` + `step8-fixtures/cases.json`(간격 사전 각 갈래 · 결정 한 줄 빼면 open · 7단계 끝점 빼면 open · 피함 · 문장 패턴)
- 결정 정본: `orchestration/work/phub-recommend/_RESUME.md` §2 2026-10-29 「8단계 조사 반영 — G1~G14 추천대로 · U8-1 (나) · U8-2 (가)」 · 「게이트 → 규칙」 · 「7단계 재반영 결과 + 남은 13」 · 10-28 source-map B04 · B05 · B06 · B11 · B13 · C4 · C5 · C9 · C10. 규칙이 바뀌면 거기가 이긴다
- 조사: `step8-research.json` · `.md`(조사 판 — 행별 대응표가 있던 판. 반영 판은 그 표를 문장 패턴으로 바꿨다)
- 원천: `step8-decisions.json` `source.path`

**원장 · 결정 파일은 승인 없이 고치지 않는다.** 판정 → 결정 목록(사람) → 결정 한 줄(승인된 것만) → 반영(스크립트) → 점검 · 검수 고리를 그대로 돈다. 1~7단계 산출 · 원천 · DEC 파일은 고치지 않는다(7단계 값이 틀려 보이면 보고).

## 1. 언제

| 경우 | 시작점 |
|---|---|
| ① **원천 새 스냅샷**(contraindications · synergy · treatment-sequence · treatment-optimization · problem-packages · problem-combos · 사전 체크 · 동의서 · 합병증 · 위험지대 · 경과표 · PIH · 문헌 · profiles 가 늘거나 바뀜) | `step8-apply.py --out <scratchpad> --source <폴더>` 의 open → 종류마다 §2 |
| ② **새 문장 꼴**(원칙 · 규칙 · 위험 · 금기 조합 문장이 패턴 밖) | open 「금기 조합 문장이 패턴 밖」 · 「규칙 행에서 쌍 · 속성 행선지가 안 나옴」 · 「원천 행 행선지 없음」 → §2-3 패턴 한 줄(규칙 바꾸기 = 최종 판단) |
| ③ **새 간격 낱말**(「N주 후」 밖 표현) | open 「간격 원문 낱말을 읽는 사전 갈래 없음」 · 「… 숫자 칸 · 표시 비어 있음」 → §2-4 사전 갈래 한 줄 |
| ④ **원천 질문 답이 옴**(의료진 · 병원) | `step8-origin-questions.md` 그 행 — §6 |
| ⑤ **앞 단계가 바뀜**(5단계 새 키 · 7단계 고민 · 조합 · CC 엣지) | `step8-apply.py` 재실행만 — open 「7단계 끝점 어긋남 — …」 이 나면 7단계부터(concern-check) |
| ⑥ **규칙 바꾸기 요청**(엣지 타입 · 간격 읽는 법 · 충돌 고르기) | 최종 판단(사용자). 규칙이 닿는 원천 칸 전부를 먼저 센다(§5 W2) |
| ⑦ 정기 점검 · 결정을 고친 뒤 | `scripts/check_relations.py --selftest` 한 번 — errors 0 · open 0 · selftest 전부 잡힘 |

점검(읽기만 · 표준 라이브러리):

```bash
python3 <스킬>/scripts/check_relations.py \
  --work orchestration/work/phub-recommend \
  --out <scratchpad>/relation-check.json --selftest     # 새 스냅샷은 --source <폴더>
```

`errors[]` = 원장 낡음(apply 재실행과 바이트 다름) · **사람 확인 게이트 상태가 남음(U8-1 위반)** · `interval.first` 가 a · b · null 밖 · days 하한 > 상한 ·
**원문 간격 낱말이 있는데 숫자 칸 · 표시 빔 · 간격 낱말을 읽는 사전 갈래 없음** · 「같은 날 불가」인데 same_day ≠ false · 「대체(택 1)」인데 간격 숫자 ·
끝점 단위 시술이 5단계에 없음 · 엣지 ↔ 주장 어긋남 · 충돌 표시 ↔ 충돌 표 어긋남 · **피함 출발이 7단계 고민 노드 아님** · 확인 조건 id 가 사전 밖 · 원천 질문 걸린 행 없음 · summary 불일치 · open 남음.
`--selftest` 는 원장 사본에 틀린 값 11가지(피함 조건부를 기본 적용으로 · 하위 조건 갈리는데 겉 칸 채움 포함)를 넣어 각각 errors 로 잡히는지 본다(점검기가 무뎌지면 여기서 걸린다).
`step8-apply.py` 의 open 은 이보다 넓다 — `references/record-schema.md` §3.

## 2. 판정 순서

원천 행 하나마다 위에서부터. **앞에서 끝나면 뒤로 가지 않는다.** 상세 `references/relation-rules.md`.

### 2-1. 이 칸은 어느 묶음인가(source-map 8단계 칸)

`source-map.json` 에서 stage 8 칸만 — 관계(시술↔시술) · 확인 조건(사람 · 연령) · 고민 조건 금기(피함) · 안전(합병증 · site_caution · 경과표 · PIH · 계열 원문) · 근거.
반영 규칙은 `field_handlers`(원천 · 칸 접두 → 원장 자리). **칸 하나라도 규칙이 없으면 open** · 칸 값 수가 지도와 다르면 open(전수).

### 2-2. 끝점 = 원천 이름이 가리키는 만큼(G2 · 고르지 않음)

1. 원천 시술군 코드(contraindications) = 계열 끝점 — 단위 시술은 조회 때 상속(C4)
2. 이름 = 5단계 정본(단위 시술 이름 · 동의어 → 장비 이름 → 조사 사전 `alias` → 1단계 제품 → 계열 → 하위 계열 → 기법 낱말) — 하나면 「이름 일치」 · 여럿이면 「후보 전부」
3. `/ + , or 또는` = 원소마다 끝점(복합) · 괄호 = 부위면 부위 조건 · 아니면 수식(묶음 낱말 + 괄호 이름이면 괄호로 — 「에너지 기기(HIFU)」)
4. 7단계 CC 조합 = 7단계 ③ 엣지 재사용(조합 원소 ↔ CC 추천 시술 이름 · 「/ ( )」 조각) · **CC 추천 시술인데 ③ 엣지가 없으면 open(7단계 끝점 어긋남)**
5. 시술 아님(왁싱 · 트라넥삼산 · 미백약 · 비타민C 도포) = 끝점 안 됨 · 원문 보관 / 묶음 낱말(열시술 · 주입 시술 · 에너지 기기 · 모든 시술) = 후보 계열 전부 + 표시
6. 못 풀면 「해석 안 됨」 → **원천 질문**(§2-7). 억지로 붙이지 않는다

### 2-3. 문장 = 패턴 규칙(U8-1 (나) — 행별 대응표 없음)

- 구조 칸(contraindications · synergy · minimum_intervals · incompatible_same_day · CC combos)은 칸 그대로 쌍
- 섞인 문장 칸(principles · combination_rules · riskBenefit · alternatives · contraindicated_combos)은 **패턴에 맞는 절만** 쌍. 화살표 원소는 전부 시술 이름으로 풀릴 때만. 패턴 없는 문장 = 그 칸 기본 행선지(원문 · 7단계 조합 속성 · 계열 원문)
- 순서 칸(by_concern.sequence · common_combos.note)은 화살표 · 「A 후 B」를 늘 분해 — 원소 끝 낱말을 떼며 풀고, 못 풀면 「해석 안 됨」
- 패턴(순서대로 첫 맞음 · 남은 꼬리로 다시): 같은 날/별도 세션 머리 → `A → B: 간격` → 역순 → `선행 또는 N 이상` · `N 이상 또는 먼저`(주장 둘) → `A와 B는 당일 가능하나 F 먼저` → 목록 + 상대 · **생략 상대**(앞 절 B) → `…전에` → `A 후 N 이내 B 시 위험` → `A 후 N 내 (같은 부위) B 금지 · 피할 것` → `A 부위 B 동시 금지` → `A + B (동시) 금지 · 병합 금기` → `A 후 B는 N 간격` → `A 후 B 순서` → **`<고민>에 B 금지`(피함)** → **`<사람 조건> 시 B 금지`(확인 조건)** → 주어 없는 `B 금지`(행 고민) → 순서 칸 `A 후 B`
- 규칙 행: detail 에서 쌍이 안 나오면 rule 제목 · 이름 없는 간격 문장(「최소 4주 간격」 「동시 시술 금지」 — `orphan_interval_regex`)은 같은 행 앞 주장에 붙임 · 쌍 없고 이름 하나면 그 계열 원문 속성
- 「A 후 …」의 A 가 시술로 안 풀리고 사람 조건 사전에 걸리면(선탠 · 이소트레티노인) = 확인 조건(C10)

### 2-4. 간격 = 간격 낱말 사전 → 숫자 칸(사용자 10-29)

**추천 · AI 는 `interval.days`(일 [하한, 상한]) · `interval.first`(a | b) · `interval.same_day` 만 읽는다.** 원문 `interval.text` 는 보관만.

| 원문 | 숫자 칸 · 표시 |
|---|---|
| N일/N주/N개월(후 · 이상 · 간격) | days [N,N] · 「이상 · 최소 · 후 · 뒤 · 부터 · 이내/내 금지」 = open_high |
| N~M주 · 3일~1주 · 24시간 | days [N,M] (단위 일) |
| 택 1 시술 | kind 대체 · 간격 비움 |
| 동시 금지 · 동시 시술 금지 · 당일 금지 · 같은 날 불가 | same_day false (+ 같은/동일 부위 = condition) |
| 직후 · 즉시 | same_day true · days [0,0] |
| 같은 날 가능 · 당일 병행 · 동시(금지 없이) | same_day true |
| …전에 | first 만 |
| 사이사이 | 반복 사이 표시 · 간격 없음 |
| 의료진이 … 평가해 간격 결정 | 간격 없음 + 의료진 판단 표시 |
| 별도 세션 | same_day false |
| 같은 날이면 다른 부위 | same_day false(같은 부위) |
| A: … / B: …(하위 조건이 갈림) | 겉 days · first · same_day 비움 · `by_sub_condition` true → options[].sub_condition 별 값을 읽음(검수 F2) |
| 하위 조건 없는 「또는」 | options + 겉 칸 = 감싼 범위 |

**원문 간격 낱말이 있는데 숫자 칸 · 표시가 비면 open · 낱말마다 그 낱말을 읽는 갈래(`word_branches`)가 안 돌면 open.** 새 낱말은 갈래 한 줄 + 고정 시험 한 줄.

### 2-5. 고민 조건 금기 = 「피함」 엣지(U8-2 (가))

「기미에 고에너지 레이저 금지」 = 7단계 고민 노드(기미) → 단위 시술 `concern_avoid`(피함(금기 조합)). **고민 낱말은 7단계 고민 노드 이름으로만** 찾는다(확인 조건 노드를 따로 세우지 않음 — 7단계 W3). 주어 없는 「고출력 레이저 금지」 = 그 행 중증도 이름 안 고민 낱말 → 없으면 행 앵커 고민 전부. 수식(고에너지 · 고출력 · 단독)은 qualifier. SPEC-004 엣지 타입 개정은 빌드 때.

**한정어 조건부(`scope_rule` · 검수 F1)**: 피함 · 간격 금기 · 같은 날 불가 · 조합 금기 · 확인 조건 끝점에서 출력 · 깊이 한정어(고출력 · 고에너지 · 박리성 · 심부 …)를 떼고 묶음(계열 · 기법 · 하위 · 용도 · 낱말 교집합)으로 열었으면 = 「조건부 — 단위 시술 미특정」 · `default_apply` false(기본 상속 · 기본 응답에서 뺌) · 한정어 원문 보관 · 원천 질문. 이름 일치 단위 시술(「IPL 단독·고출력」 → U5-030)은 그대로. 「기미 → 고출력 레이저 피함」을 M8 전체로 열면 7단계 「기미 → 토닝」 추천과 부딪친다.

### 2-6. 확인 조건 · 안전 · 근거

- 확인 조건 노드 = `conditions` 사전(패턴 공개 · 한 문장이 둘에 걸리면 둘 다) · 등급 = 원문 + 3분류(금기 · 주의 · 확인만) · 공통 = 모든 시술 1벌 · 상담 · 시술 준비 · 고지 = 계열 원문(엣지 아님) · 사람 조건 아닌 문장 = `not_person_rules`
- 합병증 = 계열마다 따로 노드(같은 이름도) · 원천 없는 계열 = gap(「없음 = 안전」 아님) · site_caution = zone × M1/M2 · 그 부위 단위 시술 없어도 둠 · 경과표 = `timeline_attach` · PIH = 5단계 pih 그대로 · N1 은 M16 원천 안 빌림(C5)
- 근거 = 문헌(PMID 키) · 문장 · 웹(합병증 URL) · 가이드 · 표기(PMC 가 맞으면 문헌) · 출처 낱말 없는 표기(「피부 회복」) = 출처 아님 → 원천 수정 후보 · 강도 = 원문 등급만(숫자 만들지 않음)

### 2-7. 충돌 · 원천 질문

- 충돌 = 같은 계열 쌍에서 먼저 하는 쪽 · 같은 날 · 간격 범위가 갈림 / 같은 계열 × 조건 등급 / 같은 조건 대기 기간 — **전부 보존 + 표시 · 자동으로 고르지 않음**(D-13b)
- 원천 질문은 **규칙으로 하나로 안 정해지는 것만**: 못 푼 이름 · 넓은 후보(`wide_candidates_*`) · 용도 낱말(`purpose_ok` 밖) · 원천 코드 어긋남 · 충돌 · 출처 아닌 표기. 필요한데 결정 `origin_questions` 에 없으면 open. 후보는 적되 추천값으로 채우지 않는다

## 3. 판정 체크리스트

- [ ] 사람 확인 게이트 · 행별 대응표(manual_map) 없음 — 전부 규칙 id(`rule`)가 붙었다
- [ ] 끝점 = 고르지 않음(후보 전부 + 표시) · 원천 코드 ≠ 해석 계열이면 source_code 보존 + 원천 수정 후보
- [ ] 간격 원문 낱말마다 사전 갈래가 돌았다 · days 하한 ≤ 상한 · 「같은 날 불가」 = same_day false
- [ ] 고민 낱말은 7단계 노드로만 · 7단계 끝점(조합 · CC 엣지 · 고민 노드)이 지금 7단계에 있다
- [ ] 충돌은 표시만(고르지 않음) · 질문은 규칙 밖만
- [ ] source-map 8단계 칸 전부 `field_handlers` · 값 수 = 지도 · 원천 행 전부 행선지 · 7단계 메모 원문 전부 처리
- [ ] 고정 숫자 assert 없음(셈은 결정 · 원천에서 계산)

## 4. 갱신 방법

```bash
W=orchestration/work/phub-recommend
python3 $W/step8-apply.py --out <scratchpad>     # 시험 — open 확인
python3 $W/step8-apply.py                         # 정본 재생성(승인된 반영 때만)
python3 $W/step8-fixture-test.py                  # 간격 사전 갈래 · 결정 한 줄 빼면 open · 7단계 끝점 · 피함 · 패턴
python3 $W/step8-apply.py                         # md 에 시험 결과 싣기
python3 $W/step8-apply.py --out <scratchpad>/b && cmp $W/step8-relations.json <scratchpad>/b/step8-relations.json   # 결정론
python3 <스킬>/scripts/check_relations.py --work $W --selftest
```

끝 조건: open 0 · 두 번 실행 cmp 같음 · 고정 시험 전부 PASS · check_relations errors 0 · selftest 전부 잡힘 · 앞 스킬 점검(concern · package · unit · technique · site · family · product) errors 0.

## 5. 틀리기 쉬운 것

`references/mistakes.md`. 요약 — W1 행별 대응표로 문장을 쌍으로 옮김(게이트가 생김 → 패턴으로) · W2 간격 낱말을 정규식 한 줄로 읽음(「같은날:」 머리 · 「사이사이」 · 「택 1」이 빈칸으로 남음 → 사전 갈래 + 낱말별 검사) · W3 꼬리 낱말을 먼저 떼서 「모든 시술」이 「모든」이 됨(전체 이름 먼저) · W4 「24시간 내」의 「간」을 「…간」으로 읽음 · W5 이름 있는 기전 문장(「HA가 PDO를 24-72시간 내 분해」)을 간격 문장으로 붙임 · W6 CC 조합 원소(PRP)를 CC 추천 시술(PRP/자가혈)과 글자 비교만 함.

## 6. 원천 질문 답이 왔을 때

그 질문의 걸린 행만. 이름 답(TCA Cross · 침습 시술 · 듀얼파장 · 혈관레이저) = 5단계 키가 있으면 `resolver.alias` 한 줄(없으면 unit-check 로) · 충돌 답 = 고르지 않던 쪽을 정하는 것이므로 최종 판단(사용자) → 결정에 「충돌 해소」 칸을 새로 둘지부터 · 원천 수정 답 = 원천 스냅샷이 바뀐 뒤 재실행 · 이소트레티노인 기간 = 확인 조건 대기 기간 원문 그대로 두고 상담 기준 표시. 답 반영 뒤 §4 전부.

## 7. 변경 보고 형식

```text
8단계 관계 원장 갱신 — <무엇>
- 결정: <decisions 칸 · 한 줄>  (승인: <누가 · 언제>)
- 셈: 주장 <전→후> · 엣지 <전→후> · 충돌 <전→후> · 조건 <전→후> · 피함 <전→후> · 원천 질문 <전→후>
- open 0 · cmp 같음 · 고정 시험 N/N · check_relations errors 0 · selftest N/N
- 남은 것: <원천 질문 id …>
```
