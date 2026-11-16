# 재검수 보고서 — SPEC-005 v3.2.1(0.3.3) · WORK-007

작성 2026-11-01 · 검수자 reviewer 워커(읽기 전용 · 수정 없음) · 전 판 `review-spec005-v32-report.md`(FAIL 3 · WARN 6)
대상 `SPEC-005.md`(0.3.3 · 1,157행 — 0.3.2 보관본이 없어 머리의 「바뀐 곳」 목록 조항을 전부 직접 대조) · `WORK-007.md`(222행) · 대조 = SPEC-006 v2.1 §3-4-2(패치본) · 실버 `step7-concerns.json` · `gold-export.json`(d3a1abd5) · 전 판 근거 그대로

## 판정 — **FAIL(경미 1 · 한 줄이면 PASS)** · FAIL 1 · WARN 0

한 줄: 전 판 FAIL 3 · WARN 6 은 전부 반영됐고 SPEC-006 v2.1 §3-4-2 와 꼴이 맞는다. 남은 것은 WORK-007 Scope 표 한 줄(79행)이 F-D′ 를 옛 문구(`severity_levels[].*`)로 적어 §4-3 · WP-2 5 와 어긋나는 것뿐이다.

| 기준 | 판정 | 요지 |
|---|---|---|
| 1 전수 대조 | PASS | §8 표 변화 없음(186 · 161 · 25 전 판 1:1 확인 그대로) · (iii) C3 = fact 있는 3 + 인용 문자열 5 로 나누고 판정 식 「정규화 인용이 `facts[].text` ∪ 동봉 원문 칸(claims_text · key_warning · price · expectedResult · C9′ · C10′) 안」 · 분모 5 · 통과 5/5 + Q003 2 반대 조건(F-2 해소) |
| 2 실물 대조 | PASS | F-D′ 재대조 = `step7 combos[].consult_copy.patientExplanation` **7**(RC-RE-R1~R7 · 실버 확인) · `severity_levels.*` 는 실버 0 → 9단계(V-4 · §8 N-9단계)로(W-5 해소) · 1-hop 종류별 「그 종류 엣지 1개 이상인 단위만의 중앙(n)」 = pair 69(150) · requires_check 12(136) · has_statement 11(113) · product_unit 11(107) · combo 7(76) **재계산 일치**(W-2 해소) · §5-0-1 「현」 열 출처 = replay2.json 676 명시(W-1) · `not-closed-why.json` 77행 실존 반영(W-3) |
| 3 보충 대조 | PASS | §5-16 입력 `intent?` 받되 무시(`intent_used: null` · 동봉 0 · 모르는 값만 4xx) · M-3 같은 문구 · 이웃 꼴 `neighbors_by_kind{kind: {n, direction, items[:8]{id, kind, name, label}}}` 하나로 통일 · SPEC-006 §3-4-2 대응표(평면 `neighbors[]` = by_kind items 이어 붙임 · `edge` = 키 · `n > items` 면 `expand(neighbor_kinds)`) — **SPEC-006 v2.1 §3-4-2 패치본 「SPEC-005 §5-16 꼴을 따름(neighbors_by_kind · items[:8] · intent 받음)」 과 일치**(F-1 해소) |
| 4 결정표 충돌 | PASS | 변화 없음 |
| 5 끝 조건 검증 가능성 | PASS | (iii) 판정 · 분모 닫힘 · 나머지 (i)(ii)(iv)~(vii) 전 판과 같음 |
| 6 WORK-007 | **FAIL(경미 · F-1)** | depends_on 에 SPEC-006 v2 §3-4-2 · §3-5 · §3-6 + 「§순서 의존」 표(WP-4 → WORK-006 WP-3 · WP-5 → WORK-006 WP-0 · 발주 순서 · heartbeat 문구) 추가(전 판 F-3 해소) · WP-0 grep 에 무관 모듈 「영향 없음」 규칙(W-4) · WP-2 5 · Done 에 `fd2_patient_explanation == 7`(W-5) · WP-4 시험에 `intent=I-03` 넘겨도 같음 · 4xx 3종. 단 **Scope 표 79행** 이 옛 문구 |
| 7 추측 자리 | PASS | §5-16 고정 숫자 전부 설정 이름(`GOLD_PEEK_ITEMS_PER_KIND` · `GOLD_PEEK_NAME_CHARS` · `GOLD_PEEK_KIND_ORDER` · `GOLD_EXPAND_PICK_MAX` · `GOLD_EXPAND_FACT_IDS_MAX` · `GOLD_EXPAND_SECTION_MAX` · `GOLD_EXPAND_NEIGHBORS_MAX`) + V-13(W-6 해소) |

## FAIL

### F-1 · WORK-007 §Scope 79행(`memory.py` · `build.py`) — F-D′ 문구가 §4-3 · WP-2 와 반대(기준 6)

근거: 79행 「F-D′ 잎 fact(combo `patientExplanation` · **`severity_levels[].*`**)」. SPEC-005 §4-3 F-D′(v3.2.1) 「실물은 `consult_copy.patientExplanation` 하나 · 7건 · `severity_levels.*` 는 실버에 칸 없음 → 9단계」 · WORK-007 WP-2 5 · 완료 조건 · Done 모두 `fd2_patient_explanation == 7`. 구현 워커가 표만 보면 없는 칸을 찾는다.
방향: 79행을 「F-D′ 잎 fact(`combos[].consult_copy.patientExplanation` 7 · `counts.v3_facts.fd2_patient_explanation`)」 로. 한 줄이면 PASS.

## 전 판 FAIL · WARN 반영 확인

| 전 판 | 반영 | 확인 |
|---|---|---|
| F-1 intent · 이웃 꼴 | M-3 · §5-16 입력 · 출력 · 대응표 · WORK-007 WP-4 2 · 시험 | SPEC-006 v2.1 §3-4-2 와 일치 |
| F-2 (iii) | fact 3 + 인용 5 · 판정 식 · 분모 5 · 5/5 + Q003 2 | ○ |
| F-3 WORK-006 의존 | depends_on · §순서 의존 표 · 발주 순서 · Related | ○ |
| W-1 현 열 출처 | 열 머리에 replay2.json 676 · 참고 열 | ○ |
| W-2 1-hop 셈 | 「종류 엣지 1+ 단위만의 중앙(n)」 · 162 전부 기준 중앙 병기 | 재계산 일치 |
| W-3 not-closed-why | 77행 실존 · 34 는 부분집합 · WP-0 기준선에서 행 단위 재셈 | ○ |
| W-4 무관 모듈 | WP-0 2 「영향 없음 · meta 대상 아님」 + 목록 | ○ |
| W-5 F-D′ 가드 | patientExplanation 7 · severity_levels 9단계 · 가드 7 | ○(Scope 79행만 F-1) |
| W-6 설정 이름 | 7 설정 이름 + V-13 | ○ |
