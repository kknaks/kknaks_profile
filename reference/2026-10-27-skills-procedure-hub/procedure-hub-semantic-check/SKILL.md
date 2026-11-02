---
name: procedure-hub-semantic-check
description: Procedure Hub 실버 1~8단계 원장(step1-products ~ step8-relations) 중 하나라도 바뀌었거나, 시맨틱 정본(semantic.json — 노드 종류 · 엣지 종류 · 용어 · 사전 하나 · id 대응 · 읽는 규칙 · 표시 · gate_status · 상속 규칙)을 골드 · 적재 · 연결 구조 페이지가 읽기 전에, 또는 시맨틱 규칙(B1~B12 · U1~U3)을 바꾸자는 요청이 왔을 때 쓴다. semantic-build.py 를 재생성하고(결정론 · 정본과 바이트 같음) 노드 · 엣지 종류 셈을 실버에서 다시 세고 · 사전 겹침 표시 · id 대응 빠짐 · 표시 12 · gate_status 3값 · 상속 규칙 9 · 합병증/부작용 분리를 점검한다. 실버 · 시맨틱 데이터는 손으로 고치지 않는다 — 실버가 틀리면 그 단계 스킬(product · family · site · technique · unit · package · concern · relation-check)로 돌려보내고, 시맨틱 규칙이 바뀌면 semantic-build.py 를 고쳐 재생성한다. 끝 조건은 build 종료 코드 0 · 두 번 실행 cmp 같음 · 정본 낡음 0 · check_semantic errors 0 · selftest 전부 잡힘. 트리거 예 — 「실버 바뀌었어 시맨틱 다시」「semantic.json 낡았나」「이 말 사전에서 뭘 가리켜」「실버 id 정본 id 대응 빠진 거 없나」「노드 · 엣지 종류 몇 개야」「합병증이랑 부작용 나뉘어 있나」「골드 들어가기 전에 시맨틱 점검」「시맨틱 점검」「이 말이 사전에서 못 찾아져」「쳐짐으로 쳐도 찾아지나」「접두로 엉뚱한 계열이 잡혀」「정규화 문서랑 코드가 같나」.
---

# Procedure Hub 시맨틱 정본 점검 · 재생성

시맨틱 정의(2026-10-29 ~ 10-30)에서 실제로 한 방법을 옮긴 것이다. 새로 지어낸 절차가 아니다.
실버 8단계(`procedure-hub-relation-check`) 다음 층이다. 실버 단계 파일마다 흩어진 「무엇이 노드고 엣지인가 · 이 말은 무엇을 가리키나 · 이 칸은 어떻게 읽나 · 무엇이 아래로 상속되나」를 **한 정본**으로 둔다. 골드가 이것을 읽는다.

- 정본: `orchestration/work/phub-recommend/semantic.json` · `.md`(json 에서 만든 것) — 현재 값 = `scripts/check_semantic.py` 출력. 숫자를 여기 박지 않는다(7단계 R21~R27 반영으로 treats 엣지가 537 → 427 로 바뀌었듯 실버가 바뀌면 셈이 바뀐다)
- 결정론 생성: `semantic-build.py` — 입력 = 실버 정본 json 8(`step1-products` ~ `step8-relations`) + `step9-explanations`(11-01 · 값 사전 · 설명 사실 셈) + `step7-decisions` · `step8-decisions`(사전 · 규칙 원문) · `step3-lexicon`(정규화) → 출력 `semantic.json` · `.md`. 시각 · 무작위 없음 · 목록 정렬 · 셈을 스크립트에 박지 않음 · open 있으면 종료 코드 1
- 결정 정본: `orchestration/work/phub-recommend/_RESUME.md` §2 10-29 「빌드 앞 순서 확정」 · 「부작용 ≠ 합병증」 · 「시맨틱 조사 반영 — 추천대로」(B1~B12 · U1~U3) · 10-30 「시맨틱 확정 · 실버 정리 끝」 · 「품질 목표(사용자 승인)」(사전 F · G · H · L · M — `dictionary.resolve_rules`) · 「골드 전 순서」(조합 구성 581). 규칙이 바뀌면 거기가 이긴다
- 과정 기록: `para/projects/company/procedure-hub/log/2026-10-30-semantic.md` · `2026-10-30-quality-eval.md`(말 → 노드 찾기 92.5% → 98.4% · 사전 원인 F · G · H · M) · 측정 정본 `quality-report.md` §0-2 · 고정 시험 `semantic-fixture-test.py` + `semantic-fixtures/`(M1~M3 · F1~F5 · G1 · G2 · H1~H3 · L1 · L2) · 조사 `semantic-research.json` · `.md`(조사 판 — 지금 정본과 셈이 다른 곳이 있다)

**실버 json · 결정 파일 · semantic.json 은 손으로 고치지 않는다.** 실버가 틀리면 그 단계 스킬로, 시맨틱 규칙이 바뀌면 `semantic-build.py` 를 고쳐 재생성 — 승인된 것만.

## 1. 언제

| 경우 | 시작점 |
|---|---|
| ① **실버가 바뀜**(어느 단계든 apply 재실행 뒤) | `check_semantic.py` — 「정본 낡음」 · 「입력 판 다름」이 나면 §4 재생성 |
| ② **골드 · 적재 · 페이지가 시맨틱을 읽기 전** | `check_semantic.py` 한 번 — errors 0 이어야 읽는다 |
| ③ **이 말이 무엇을 가리키나**(사전 조회) | `semantic.json` `dictionary.resolve_rules` 순서대로(정규화 → 완전 → 낱말 나눔 → 끝말 떼기 → 접두) `dictionary.expressions[]` 의 `norm` 과 대조 — §2-3 · §2-3b |
| ③-b **허브 품질 측정 M2(말 → 노드)가 못 찾음 · 틀리게 찾음을 냄** | 원인 갈래(F 사전 출처 · G 접두 · H 정규화 · M 문서 ≠ 코드 · L 쌍 이름 · 와일드카드)를 보고 §2-3b 의 그 칸을 고친다 — 표현 행을 손으로 넣지 않는다 |
| ④ **실버 id ↔ 정본 id** | `ids.map` · `ids.silver_string_map` — §2-4 |
| ⑤ **규칙 바꾸기 요청**(노드 · 엣지 종류 · 사전 구조 · id 규칙 · 표시 · 상속 · 부작용/합병증 경계) | 최종 판단(사용자). 실버 데이터가 바뀌는 것(B1 · B3 · B8 꼴)은 **실버 결정 파일 → apply**, 시맨틱만 바뀌는 것은 `semantic-build.py` |
| ⑥ 정기 점검 | `check_semantic.py --selftest` |

점검(읽기만 · 표준 라이브러리 · 작업 폴더에 아무것도 안 씀 — 재생성은 임시 폴더 둘에서):

```bash
python3 <스킬>/scripts/check_semantic.py \
  --work orchestration/work/phub-recommend \
  --out <scratchpad>/semantic-check.json --selftest
```

`errors[]` = build 종료 코드 ≠ 0 · **결정론 아님(두 번 실행 바이트 다름)** · **정본 낡음(재생성 결과와 바이트 다름)** · 입력 판 다름 · 노드 · 엣지 종류 목록 다름 · **노드 · 엣지 종류 셈 ≠ 실버 재셈** · 정본 id 중복 · 정본 키가 실버 id 와 다름(허용 밖) · **id 대응 빠짐** · 대응표에 실버 밖 행 · 7단계 엣지 from 문자열이 대응표에 없음 · 문자열 대응 → 없는 정본 id · 사전 norm 중복 · norm ≠ 정규화(expr) · 사전 대상 없음 · **사전 겹침인데 collision 표시 없음** · 대상 하나인데 collision · mode 어긋남 · 후보 ⇔ ambiguous 어긋남 · **사전 대상 id 가 대응표에 없음** · 표시 12 아님 · 표시 칸 빠짐 · gate_status ≠ 3값 · 실버 gate_status 가 3값 밖 · 상속 I1 ~ I9 아님 · 상속 칸 빠짐 · **상속 엣지인데 끝에 계열 없음** · 저장 엣지 아님 목록 다름 · I5 site_check 셈 ≠ 7단계 · **합병증에 중대 반응 아닌 것(B1)** · 부작용에 moderate 이상 · gap 계열이 계열 목록 밖 · **gap 계열에 합병증 노드** · 확인 조건 주장에 조건 아닌 문장(B8) · summary 불일치 · 정본 open.
`selftest[]` = 틀린 값 15가지를 넣어 각각 잡히는지 — 하나라도 안 잡히면 종료 코드 1.

## 2. 정본을 읽는 법

상세 `references/semantic-rules.md` · 칸 `references/record-schema.md`.

### 2-1. 노드 13 · 엣지 21 — 실버 칸에서 센다

- 노드 종류 13: product · family · site · technique · unit_procedure · package · concern · purpose · combo · check_condition · complication · evidence_statement · evidence_source. 종류마다 정본 파일 · 칸 경로 · 필수 · 선택 속성 · id 규칙
- **노드가 아닌 것**: 부작용(계열 속성) · 끝점 묶음(엣지 칸 `endpoints.a|b.candidates[]` — U3) · 확인 조건 아닌 문장(`conditions.not_condition`) · 허가 · 업체 · 규격 · 시장가 · 경과 · PIH · 운영 속성
- 엣지 종류 21(페이지 32 → 합침 · 나눔 · B4). **저장 엣지 아님** 2: `prod_unit_inh`(상속 후보 = 계산) · `set_member`(끝점 묶음 원소)
- **연결 구조 페이지(`silver-graph-build.py`)의 노드 · 엣지는 그림용 뽑기다 — 정본 아님**(틀렸던 예 S1)

### 2-2. 상속 9 — 저장 안 함 · 골드 계산(B7)

I1 계열 → 단위 시술 · I2 하위 계열 · I3 기법 조건 · I4 제품 → 단위 시술 · I5 부위(내림 · R21 올라가기 · R22 고민 영역 — **7단계가 엣지에 저장한 값**, 상속 아님) · I6 끝점 묶음(후보 전부 · 고르지 않음) · I7 조건부 제외(default_apply false) · I8 안전 · 운영 원문 붙는 수준 · 부작용 덮어쓰기 · I9 해당 없음 ≠ gap.
- 상속 표시(`edge_kinds[].inherit`)가 붙는 엣지는 끝에 계열이 있는 것뿐 — treats · procedure_relation · concern_avoid · requires_check · has_complication · site_caution · has_statement
- 지금 실버에 미리 펼쳐 저장된 것(합병증 `units_inherit` · 5단계 `inherited_candidates`)은 남아 있어도 정본은 계산

### 2-3. 사전 하나(B5)

- 행 = `expr` · `norm` · `variants[]` · `targets[{id, qualifier, reasons[]}]` · `sources[]` · `mode`(하나 · 전부 · 후보) · `ambiguous` · `collision` · `prefer`
- **norm 하나에 행 하나** · 대상 여럿 ⇔ collision 갈래(A ~ J) · 후보 ⇔ ambiguous · 대상 id 는 정본 id(또는 `none:` — 시술 아님 · 고민 노드 아님(트리 항목))
- **7 · 8단계 수준 차이(F)는 겹침이 아니라 qualifier** — 「토닝」 → `family:M8` + `{technique: K04a}`. 단위 시술로 펼치는 것은 상속 I2 · I3
- 고르지 않는다 — 후보는 전부 돌려주고 외부 LLM 이 고르거나 되묻는다(표시 candidates)
- 사전 행이 아닌 해석 규칙(고민 규칙 R12~R22 · 8단계 꼬리 낱말 · 3단계 패턴 · 문장 · 조건 패턴)은 `dictionary.interpret_rules`

### 2-3b. 찾는 규칙 `dictionary.resolve_rules` — 문서 = 코드(2026-10-30 허브 품질 측정)

말 → 노드 찾기는 이 칸 하나가 정본이다. **`semantic-build.py` 의 `RESOLVE_RULES` 가 그대로 `semantic.json` 에 실리고**, 사전 행의 `norm` · 골드 resolve(SPEC-005 T1) · 측정(`quality-eval.py`) · 이 스킬의 `check_semantic.py` 가 모두 이 칸을 읽는다. 1차 측정 때 문서(「영문으로 시작하면 소문자 · 악센트 제거」)와 코드(NFKC · 전부 소문자 · 악센트 안 접음)가 달라 골드를 문서대로 짜면 「니들RF」 같은 한글 + 영문 말이 전부 못 찾아질 뻔했다(원인 M).

| 칸 | 지금 값 | 측정 원인 · 예 |
|---|---|---|
| `normalize`(순서대로) | NFKC → 라틴 악센트 접기(NFKD 결합 부호 제거 · NFC) → `fold` → 공백 제거 → 괄호 `( ) [ ]` 지움(안 글자는 남김) → 전부 소문자 | M — 「Juvéderm」 = 「juvederm」(고정 시험 M2) |
| `fold` | 「쳐짐」 → 「처짐」(사전 · 질의 **양쪽**) | H — 「볼쳐짐/불독살」 = 「볼처짐/불독살」(H1). 10-27 원천 수정 결정(쳐짐 → 처짐)과 같은 방향 · 원천은 아직 「쳐짐」이라 입력 쪽에서 접는다 |
| `strip_chars` | `()[]` | H — 「코그(Cog)」 = 「코그 Cog」(H2) · 1차 「투 TU」 못 찾음 → 찾음 |
| `split` | `[\s/·,()\[\]+]+` — 나눈 낱말마다 완전 일치 | 「턱선 처짐」 → 턱선(부위) + 처짐(고민) · 쌍 이름 「RF/HIFU」(L2) |
| `tails` | 끝 「주사 · 시술」 떼고 완전 | H — 「쿨스컬프팅시술」 → 쿨스컬프팅(H3) |
| `prefix_min` · `prefix_rule` | 질의 2자 이상이 표현 앞부분일 때 — **대상의 계열(제품 · 단위 시술 · 계열 · 패키지 → 계열 코드) · 고민 대분류 · 부위 · 목적이 하나로 모일 때만**. 여럿이면 못 찾음 | G — 「리프」 → 리프팅 M9 · M7 · 목적이 섞여 거절(G1) · 「쥬비」 → 쥬비덤(M2) 하나라 씀(G2). 1차 「PLLA」가 접두로 다른 제품을 「틀리게 찾음」 |
| `order` | 완전 → 낱말 나눔 → 끝말 떼기 → 접두. **앞에서 찾으면 다음 단계 안 감** | — |

**사전 출처(원인 F)** — 표현 행은 아래 실버 칸에서만 온다(`expressions[].sources[]` · 셈은 `summary.by_source`). 1차 뒤 더한 것: 5단계 원장 이름(`step5 ledger[].name` — 값 「하이드로퀴논」 → M15 · 단위 시술 「V라인주사」 → U5-070 · F1 · F2) · 시장가 이름(`step5 market[].name`) · 환자용 이름(`patient-education categories[].patient_name` — 「콜라겐 재생 주사」 → M3 · F4) · 원천 CC 이름(`step7 edges[③].ccs[]` → CC 앵커 고민 · 「케미컬필링」 → P6-2 · F5) · 고민 갈래 이름(`step7 concerns.subcategories[].source_label` 등 — 노드 아닌 갈래 「주사치료」 → P13 · F3). **원천에 없는 말(샘플만의 「Voluma」 · 「초음파」 · 미라쥬 「눈물고랑 · 밝기 · 피지」)은 사전에 넣지 않는다** — 허브 보강 후보(골드 D-18) · 연결 층 몫(D-17).

**쌍 이름 · 와일드카드(원인 L)** — 「모든 시술」 = `scope:모든 시술`(노드 아님 · L1). 쌍 이름(「HA 필러」 · 「RF/HIFU」 · 「CO2 프락셔널」)은 F · H 규칙으로 찾는다(L2).

- 정규화 · 접두를 바꾸면 **찾음이 늘기만 하지 않는다** — 10-30 G(접두 거절) 뒤 「꿀광」 · 「등살」 · 「피지」가 「후보 여럿」에서 「못 찾음」으로 갔다(대신 틀리게 찾음이 줄었다). 바꾼 뒤 측정 M2 를 다시 보고 나빠진 말을 보고에 적는다

### 2-4. id 대응(B6)

- 정본 id = `{종류}:{키}` · **실버 id 는 바꾸지 않는다** · 골드 · 적재는 `ids.map` 으로
- 키가 실버 id 와 다른 것은 결정 고민 노드(`J10-피부결` → `concern:J10`)와 목적(id 없음 → `purpose:PU-nn`, purposes[] 순서)뿐
- 실버 안 문자열 꼴(`목적:{이름}` · `units:` · `bundle:` · `all` · `ledger:` …)은 `ids.string_forms` · `silver_string_map`
- ⚠ 목적 PU 번호는 7단계 `purposes[]` 순서다 — 목적 노드가 중간에 끼면 번호가 밀린다(정본 낡음으로 잡힘 → 골드 쪽 영향 확인)

### 2-5. 읽는 규칙 · 표시 · gate_status

- reading_contract(8단계 정본 그대로): `claims[].interval.days` · `first` · `same_day` 만 읽음 · `by_sub_condition` 이면 `options[]` · `default_apply` false 는 기본 응답 · 상속에서 뺌
- 표시 12 하나로(conflict · conditional · candidates · weak · question · not_recommended · gap · default_value · unresolved · not_procedure · by_sub_condition · license_unconfirmed) — 표시마다 실버 칸 · 셈 · 읽는 법
- gate_status 3값(자동(완전 일치) · 자동(규칙) · 결정) · **「미확인」은 상태가 아니라 표시**(question · weak · gap)

### 2-6. 부작용 ≠ 합병증(사용자 10-29 · B1 · U1 · U2)

- **합병증 노드** = complications.json severity moderate · severe · critical + U1 원문 serious(`CX-{계열}-T{n}`)
- **부작용** = 계열 속성 `safety.side_effects`(severity mild + U1 원문 common · uncommon) · 제품 × 계열 · 단위 시술 값이 있으면 덮어씀(골드 계산 · I8)
- 경계(mild 인데 발생률에 「흔함」 낱말 없음)는 추정하지 않고 의료진 질문
- 합병증 gap = 원천이 없는 계열 — **부작용 문장으로 메우지 않는다**. 원천은 있으나 전부 mild 인 계열은 gap 아님(「중대 반응 없음(원천)」 · I9)

## 3. 규칙 체크리스트

틀렸던 예는 `references/mistakes.md`.

- [ ] **정본 = 재생성 결과**(바이트 같음) — 실버를 바꾼 판마다 `semantic-build.py` 재실행. 7단계 반영 워커도 R21 ~ R27 판마다 재생성했다
- [ ] **두 번 실행 cmp 같음**(결정론) · build 종료 코드 0(open 0)
- [ ] **셈은 실버에서 다시** — `check_semantic.py` 가 노드 13 · 엣지 21 셈을 semantic-build 와 따로 센다. semantic.json 숫자를 믿고 끝내지 않는다
- [ ] **페이지 뽑기를 정본으로 안 씀**(S1)
- [ ] **이름이 같다고 합치지 않고, 다르다고 나누지 않는다** — 판정 · 근거 칸이 있나, 바뀌면 정체가 바뀌나로(S2 — 「계열」 엣지 둘 · 「출처」 셋)
- [ ] **수준 차이는 겹침이 아니라 qualifier**(S3)
- [ ] **id 대응 빠짐 0** · 실버 id 안 바꿈
- [ ] **합병증 = 중대 반응만 · 부작용은 속성 · gap 은 gap 으로**(S4)
- [ ] **상속은 저장하지 않는다** — 골드가 계산
- [ ] **실버 · 시맨틱 데이터 손 수정 0** · 가상 문장 시험 없음(지금 데이터만)
- [ ] **찾는 규칙은 `resolve_rules` 한 곳 — 문서 = 코드**(M). 골드 · 측정 · 스킬이 자기 정규화를 따로 짜지 않는다 · `semantic-fixture-test.py` M1 이 `semantic.json` 칸 = `RESOLVE_RULES` 를 본다
- [ ] **접두 일치는 대상이 한 계열 · 한 고민 대분류로 모일 때만**(G) — 짧은 접두가 다른 계열로 「틀리게 찾음」을 만든다
- [ ] **사전 출처는 실버 칸만**(F) — 샘플 · 장비 화면에만 있는 말은 사전에 안 넣고 보강 후보로
- [ ] 사전 · 정규화를 바꾸면 `procedure-hub-quality-eval` M2(말 → 노드 찾기 ≥ 97%)를 다시 재고, 나빠진 말을 적는다

### 끝 조건

- [ ] `semantic-build.py` 종료 코드 0(open 0) · 두 번 실행 cmp 같음
- [ ] `check_semantic.py` **errors 0 · selftest 전부 잡힘**
- [ ] `semantic-fixture-test.py` 전부 PASS(문서 = 코드 M1 포함) — `check_semantic.py` 는 `resolve_rules` 를 읽어 `norm` 을 다시 계산하지만 `RESOLVE_RULES` 와 같은지는 이 고정 시험이 본다
- [ ] 실버를 바꿨다면 그 단계 스킬 errors 0 이 먼저(시맨틱은 실버를 읽기만 한다)

## 4. 갱신 방법

1. **실버가 바뀌었을 때** — 그 단계 스킬로 실버를 먼저 끝낸다(open 0 · errors 0). 그다음 프로필 레포 루트에서

```bash
W=orchestration/work/phub-recommend
python3 <스킬>/scripts/check_semantic.py --work $W --out <scratchpad>/semantic-check.json   # 「정본 낡음」 · 「입력 판 다름」 확인
python3 $W/semantic-build.py                                                               # 정본 재생성(승인된 실버 반영 뒤에만)
python3 <스킬>/scripts/check_semantic.py --work $W --out <scratchpad>/semantic-check.json --selftest
python3 $W/silver-graph-build.py                                                           # 연결 구조 페이지도 같이 재생성(코디가 재게시)
```

   재생성 전후 summary 를 비교해 바뀐 셈을 보고한다(노드 · 엣지 종류 셈 · 사전 표현 · 겹침 · id 대응 · 합병증 · 부작용 · gap)
2. **시맨틱 규칙을 바꿀 때**(최종 판단 받은 것만) — 바뀌는 것이 실버 데이터면 **실버 결정 파일 → apply**(B1 합병증 분리 · B3 끝점 칸 · B8 조건 아닌 문장이 그랬다), 시맨틱 표현만이면 `semantic-build.py` 를 고친다. 셈을 스크립트에 박지 않는다
   - 노드 · 엣지 종류를 늘리거나 줄이면 `check_semantic.py` 의 `NODE_KINDS` · `EDGE_KINDS` · `silver_edge_counts` 도 같은 판에서
3. **검수** — 정본 바이트 = 재생성 · 셈 = 실버 재셈 · 사전 · id 대응 전수. 원천 · 실버 · DEC md5 그대로

## 5. 출력 형식 — 변경 보고

```markdown
## 시맨틱 정본 변경 보고 (YYYY-MM-DD · 바뀐 실버 <stepN …> · 판 <sha 전 → 후>)

### 셈 (전 → 후)
- 노드 종류 13 — <종류>: N → N …(바뀐 것만)
- 엣지 종류 21 — <종류>: N → N …
- 사전 표현 N → N · 대상 N → N · 겹침 N → N(갈래 <A ~ J> 바뀐 것)
- id 대응 N → N · 키 다름 N(결정 고민 노드 · 목적)
- 합병증 N → N · 부작용 N → N · gap N → N
- 찾는 규칙(resolve_rules) 바뀐 칸 <없음 / 칸: 전 → 후> · quality-eval M2 찾음 N% → N% · 나빠진 말 <목록>

### 바뀐 규칙 (없으면 「없음」)
- <B · U id> — <한 줄> · 실버 반영 <결정 파일 → apply / semantic-build 만>

### 점검
- semantic-build: 종료 코드 <0> · 두 번 cmp <같음>
- check_semantic: errors N · selftest N/N · 정본 낡음 <없음>
```

변경이 0 이면 「변경 0 — check_semantic errors 0 · selftest N/N(결과 경로)」 한 줄로 끝낸다.
