# 8단계 규칙 상세 — 관계 · 확인 조건 · 피함 · 안전 · 근거

정본은 `step8-decisions.json`. 여기는 왜 그렇게 하는지와 실제 예(지금 원천 기준)다. 셈은 `step8-relations.md` 를 본다.

## 1. 결정 묶음(G1~G14 · 조사 ① 표 추천대로)

| # | 규칙 | 실제 예 |
|---|---|---|
| G1 | 끝점 쌍마다 엣지 하나(D-03) · 주장마다 원천 · 원문 · 종류 · 원문 등급 + 사이트 라벨 · 간격 숫자 칸 · 이유 · 조건 · 근거 · 규칙 id | contraindications M1↔M2 「같은 날 가능」(병행 가능) + synergy 「보톡스 함께 필러 같은 날」 = 같은 계열 쌍 엣지의 주장 둘 |
| G2 | 끝점 = 원천 이름이 가리키는 만큼(고르지 않음) | 「HA 필러」 = M2 하위 히알루론산 → 키에 하위 없음 → M2 단위 시술 후보 전부 + 「하위 원문 보관」 |
| G3 | synergy 「대신」 = 대체(택 1) · 시너지 아님 | 「포텐자 대신 시크릿 · 택 1 시술」 |
| G4 → U8-1 (나) | 원칙 · 규칙 · 위험 문장 쌍 = **문장 패턴**(게이트 없음) | 원칙 2 「HIFU는 보톡스 주입 후 … HIFU 선행 또는 2주 이상 간격을 두며, RF·IPL·비침습 레이저는 당일 병행 가능」 → 순서(HIFU 먼저) · 간격(보톡스 먼저면 14일 이상) · RF/IPL/비침습 레이저 ↔ 보톡스 같은 날(생략 상대 = 앞 절 B) |
| G5 → U8-1 (나) | 화살표 · 「A 후 N 내 B 금지」 분해 = 규칙(auto) | 「토닝 먼저 → 2주 후 스킨부스터」 → first a · days [14,14] · open_high |
| G6 → 10-30 | 충돌 = **하나로**(conflict_resolution R1~R6 · D-13b 바꿈) — 조건 분리 · 등급 더 엄격 · 간격 더 긴 쪽 · 같은 날 불가 · 순서 반대만 순서 단정 안 함 + 의료진 · 원문 alternatives | M1↔M2 같은 날 가능 ↔ 「별도 세션」 문맥(R1 세션) · 필러 → HIFU 같은 날 불가 ↔ HIFU → 필러 가능(R1 방향 · by_direction) · M2↔M8 「레이저/IPL 은 필러 전에」 ↔ 「필러 → 레이저 최소 5일」(R5 · 간격 R3) · 아미노글리코시드 확인만 · 주의 · 금기(R2 → 금기) · 이소트레티노인 6 · 12 · 0~2개월(R6 → 얕은 6 · 박리 12) |
| G7 | 시술 아닌 원소 · 묶음 낱말 | 「제모 후 2주 내 왁싱/전기분해 금지」 → 왁싱 · 전기분해 = 시술 아님(엣지 안 섬 · 원문 보관) |
| G8 | 6단계 메모 = 시너지 「함께 판매」 근거 · 「다름」 = 충돌 표시 | 꿀광토닝 ↔ synergy 「스킨부스터 2주 후 레이저토닝」 |
| G9 | procedure-profiles 플래그 = 계열 원문 속성(파생 계산 안 함) | hasProtein · thermalLoad |
| G10 | 확인 조건 원장 · 등급 3분류 | 임신 consent 「금기」 · pre-check absolute → 금기 · relative → 주의 · must_check → 확인만 |
| G11 | 합병증 계열마다 · gap 표시 | 「감염」이 여러 계열에 따로 노드 |
| G12 | 위험지대 = site_caution(zone × M1/M2) | 미간 × 필러 — 그 부위 필러 단위 시술 없어도 엣지 둠 |
| G13 | 계열 안전 · 상담 원문 · 경과표 붙는 곳 | hifu-rf 경과표 = M9 하위 HIFU · RF 단위 시술 |
| G14 | 근거 노드 · 강도 = 원문 등급만 | 규칙 evidence 「MFU-보툴리눔독소 … PMC11945533」 — 문헌과 PMC 맞으면 문헌 노드 |

## 2. 문장 패턴 — 남은 꼬리로 다시

문장 하나에서 패턴이 맞으면 주장을 만들고, 맞은 끝 뒤 첫 「, 」 다음부터 다시 찾는다. 그래서 원칙 2 처럼 한 문장에 절이 둘이면 둘 다 나온다. 아무 패턴도 안 맞으면 괄호 안 화살표 → 문장 화살표 순으로 본다(섞인 칸은 화살표 원소가 전부 시술 이름일 때만 — 「필러 혈관 폐색 주의 → 히알루로니다아제 비상 준비」 는 쌍 아님).

- 「주입 후」 앞의 B = **생략 상대**: 다음 절이 「X·Y는 당일 병행 가능」처럼 상대 없이 끝나면 그 B
- 규칙 행 제목: detail 에 쌍이 없을 때만(규칙 3 「열린 상처에 필러 주입 시 감염 위험. 최소 4주 간격.」 → 제목 「프락셔널 후 당일 필러 금지」 + 「최소 4주 간격」 붙임 → same_day false · days [28,28])
- 이름 없는 간격 문장만 붙인다(`orphan_interval_regex`) — 「비가교 HA가 PDO를 24-72시간 내 분해할 수 있음」 은 이름 있는 기전 문장이라 안 붙음
- 금기 조합 문장은 「 — 」 앞 본문만 패턴에 넣는다(뒤는 설명)

## 3. 간격 — 낱말별 검사

`word_branches`: 원문에 낱말(택 1 · 의료진 · 세션 · 사이사이 · 직후 · 전에 · 반복 · 순차 · 에 한해 · N단위 · N회 · 같은 날/당일/동시 · 같은/동일 부위)이 있으면 그 낱말을 읽는 갈래가 돌아야 한다. 갈래를 빼면(고정 시험 D-ALT · D-MD · D-BETWEEN) 그 낱말이 남은 주장이 open.
`first` 는 간격 사전이 아니라 원문 머리말(「X 먼저」 · 「X N주 후」 · 「X →」 · 패턴의 A)에서 — 머리말 X 가 어느 쪽 원문에 들어 있나, 아니면 X 의 이름 풀이 계열이 어느 쪽 계열과 겹치나. 둘 다 · 아무도 아니면 null.

## 4. 7단계 끝점

| 8단계가 쓰는 7단계 값 | 어긋나면 |
|---|---|
| 최적화 행 → 조합 `RC-OP-*`(source_id = 「고민|중증도」) · anchor.concern | open 「7단계 끝점 어긋남 — 최적화 행 조합 없음」 |
| 세션 조합 note → `RC-SQ-*`(source_id = 이름) | open 「… 세션 조합 없음」 |
| riskBenefit → `RC-PC-<패키지 id>` | open 「… 추천 패키지 조합 없음」 |
| CC 조합 → ③ 엣지(source_id 「P:CC」 · evidence.name) | open 「… CC 추천 시술 엣지 없음」 |
| 피함 출발 → 고민 노드(categories · subcategories · extra_items) | open 「… 고민 노드 없음」 |

## 5. 원천 질문 갈래

| 갈래(match.type) | 언제 | 지금 예 |
|---|---|---|
| unresolved_name | 끝점 「해석 안 됨」 | TCA Cross · 침습 시술 |
| wide_candidates | 계열 아닌 조건 끝점 후보 > 기준 | 듀얼파장 레이저 |
| purpose_word | 용도 낱말(`purpose_ok` 밖) | 혈관레이저 |
| code_mismatch | 원천 코드 ≠ 해석 계열 | M4-쥬베룩 · M8-서브시전 · M17-엑소좀 |
| conflict | 계열 쌍 **진짜 반대(R5)만**(pairs · 10-30) | M1↔M2 · M2↔M8 · M3↔M9(묶음 원칙 Q8-20) … |
| ~~grade_conflict~~ | 10-30 R2 로 정함 — 질문 없음(Q8-7 내림) | 임신 · 수유 |
| ~~wait_conflict~~ | 10-30 R6 로 정함 — 질문 없음(Q8-1 내림) | 이소트레티노인 |
| guide_not_source | 출처 낱말 없는 표기 | 피부 회복 |
| side_effect_exception | 부작용(mild)인데 발생률에 흔함 낱말 없음(B1 예외) | 비대칭 · 딤플링 · 두통 → Q8-19 |

## 6. 시맨틱 반영(10-30 · 결정 `semantic_apply`)

사용자 10-30 「시맨틱 조사 반영 — 추천대로」(B1~B12 · U1~U3). 새 원천이 들어와도 아래 규칙으로만 나눈다.

| 규칙 | 칸 | 뜻 |
|---|---|---|
| U2 · B1 부작용 ≠ 합병증 | `safety.side_effects` · `safety.complications` | complications.json severity mild = 부작용(계열 속성 · id SE-) · moderate 이상 = 합병증 노드(id CX- · 원천 번호 그대로). 제품 × 계열 · 단위 시술 값(5단계 extracted safety.common)이 계열 값을 덮어쓰는 것은 골드 계산 |
| B1 예외 | `side_effects[].staff_question` | mild 인데 발생률에 흔함 낱말(side_effect_common_incidence)이 없으면 부작용으로 두고 의료진 질문 Q8-19 |
| U1 gap 채움 | `summary.gap_filled_families` | complications.json 에 없는 계열 중 taxonomy modality extracted.safety 원문이 있으면 serious → 합병증(CX-{계열}-T{n} · severity null) · common · uncommon → 부작용. gap = 합병증 원천 없음만 · 원천은 있는데 전부 mild 인 계열은 `complication_mild_only_families` |
| U3 · B3 끝점 묶음 | `edges[].endpoints.a/b{kind, id, qualifier, candidates[]}` | 묶음은 노드가 아니라 엣지 칸. a · b 문자열은 그대로(뒤 호환) |
| B8 조건 아님 | `conditions.not_condition` | 상담 · 시술 준비 · 고지 · 조건 아닌 문장은 확인 조건 엣지에서 빼고 원문 보관(계열 대상은 family_text 「상담 · 준비 · 고지 …」 — G10) |
