# 실버 8단계 — 관계 · 확인 조건 · 안전 · 근거 (반영)

`step8-apply.py` 결정론 산출 · 결정 `step8-decisions.json` · 정본 `step8-relations.json`. 원천 `phub-stg-2026-10-26` 은 읽기만.

- 사람 확인 게이트 없음(U8-1 (나)) — 원칙 · 규칙 · 위험 문장 · 화살표 문장 모두 문장 패턴 규칙(`sentence.patterns`)으로 쌍을 만든다 · 규칙으로 하나로 안 정해지는 것만 원천 질문
- 간격은 간격 낱말 사전(`interval_lexicon`) — **추천 · AI 는 `interval.days` · `interval.first` · `interval.same_day` 만 읽는다** · 원문은 `interval.text` 보관
- 고민 조건 금기 = 7단계 고민 노드 → 「피함(금기 조합)」 엣지(`concern_avoid` · SPEC-004 개정은 빌드 때 · U8-2 (가))
- **충돌은 하나로(10-30 · D-13b 바꿈)** — 조건 다르면 나눔(R1) · 등급 더 엄격(R2) · 간격 더 긴 쪽(R3) · 같은 날 불가(R4) · 순서 반대 = 순서 단정 안 함 + 의료진(R5) · 대기 더 긴 쪽(R6). 원문은 alternatives · **앱은 `edges[].resolved` · `resolved_pairs` · `conditions.resolved` · `conditions.wait_resolved` 만 읽는다**

## 셈

| 항목 | 셈 |
|---|---|
| 관계 주장 | 395 — 간격 9 · 간격 금기 13 · 같은 날 불가 7 · 대체(택 1) 16 · 병행 · 간격 27 · 병행 · 간격(문장) 6 · 순서 · 간격(다음에) 49 · 순서 · 간격(문장) 8 · 순서(문장 화살표) 63 · 순서(문장) 6 · 시너지(CC 조합) 137 · 시너지(함께) 50 · 재시술 간격(자기 쌍) 1 · 조합 금기 3 |
| 관계 엣지(끝점 쌍) | 230 (충돌 표시 0) |
| 충돌 | 계열 쌍 22 (간격 수치 2 · 같은 날 가능 ↔ 불가 4 · 순서(먼저 하는 쪽) 16) · 조건 등급 76 · 대기 기간 1 |
| 간격 숫자 칸 채운 주장 | 239 / 395 |
| 시술 아님 끝점 주장 · 묶음 낱말 주장 · 못 푼 이름 주장 | 6 · 2 · 1 |
| 확인 조건 | 노드 53 · 주장 336(사람 조건 330 — 금기 196 · 주의 55 · 확인만 74 · 확인만(고지) 5) |
| 피함(고민 조건 금기) | 5 |
| 합병증 · 주의(site_caution) | 35 {'U1 taxonomy': 8, 'complications.json': 27} (원천 없는 계열 12) · 22 |
| 부작용(계열 속성 · U2 · B1) | 72(의료진 질문 예외 9 · 없는 계열 10) · U1 채운 계열 {'M10': {'부작용': 5}, 'M12': {'부작용': 6, '합병증': 1}, 'M13': {'부작용': 3}, 'M17': {'부작용': 3, '합병증': 1}, 'M4': {'부작용': 7, '합병증': 2}, 'M5': {'부작용': 4, '합병증': 1}, 'M6': {'부작용': 6, '합병증': 3}} |
| 확인 조건 아님(B8 · 원문 보관) | 37 {'고지 항목': 6, '근거 수준 문장(조건 아님) → 계열 원문 속성': 1, '부위 조건(사람 조건 아님) → 계열 원문 속성 · 부위 표시(site_caution 은 anatomy M1/M2 만)': 2, '상담 항목': 22, '시술 준비 항목': 5, '효과 문장(조건 아님) → 계열 원문 속성': 1} |
| 경과표 · PIH | 10 · 26 |
| 근거 | 문헌 25 · 문장 119 · 웹 29 · 가이드 · 표기 15 |
| 조건부(한정어 · 단위 시술 미특정 · 기본 적용 제외) | 주장 2 · 피함 3 · 조건 1 |
| 하위 조건별 값(by_sub_condition — 겉 칸 비움) | 2 |
| 웹 근거 종류 | 원문 출처 문자열(내부 · 통설) 14 · 웹 15 · multi_url 7 |
| 속성(쌍 아님) | 56 |
| 원천 질문 · 원천 수정 후보 | 18 · 10 |
| 전수 — 8단계 칸 · 원천 행 | 200 · 446 |
| **open** · 낡은 결정 | **0** · 0 |

## 충돌 하나로(10-30)

| 항목 | 셈 |
|---|---|
| 계열 쌍 충돌 X8 처분 | {'보수적 선택': 3, '의료진 확인': 16, '조건 분리(가짜 충돌)': 3} (묶음 끝점으로 새로 드러난 쌍 3 · 기존 쌍에 묶음 몫 더함 7) |
| **가짜 충돌 해제(R1) · 보수 선택(R3 · R4 + 등급 R2 + 대기 R6) · 진짜 반대 → 의료진(R5)** | **3 · 80 · 16** |
| 등급 충돌 → 더 엄격 · 대기 기간 → 더 긴 쪽 | 76 · 1 |
| 엣지 resolved 상태 · 표시 | {'보수적 선택': 24, '의료진 확인': 59, '조건 분리': 3, '하나': 144} · {'conservative': 24, 'ok': 147, 'staff_check': 59} |
| 엣지 규칙 쓰임 · 하위 조건으로 나뉜 엣지 · 방향별 같은 날 값이 갈리는 엣지(by_direction) | {'R1': 32, 'R3': 62, 'R4': 1, 'R5': 59} · 32 · 4 |
| 주장 표시 | {'conservative': 15, 'ok': 305, 'staff_check': 75} |
| 단위 시술 쌍 전수 · 형제 엣지 겹쳐 쌍으로 접음 · **두 값 나가는 쌍** | 4791 · 105 {'보수적 선택': 35, '의료진 확인': 63, '하나': 7} · **0** |
| 확인 조건 등급 표(대상 키 × 조건) · 그중 R2 · 단위 시술 키로 접음 | 241 · 139 · 0 |
| 대기 기간 표 · 질문 내림 | 1 · Q8-1, Q8-7 |

규칙(결정 `conflict_resolution.rules`):

- **R1 조건이 다른 가짜 충돌** — 원문(간격 원문 · 끝점 원문 · 수식 · 하위 조건 원문)에 하위 조건(같은 날 / 별도 세션 · 먼저 하는 쪽(방향 — 「HA 필러 → RF/HIFU 같은 날 불가 · 역순은 같은 날 가능」) · 같은 부위 / 다른 부위 · 박리 / 비박리 · 깊이 · 출력 · 용도)이 적혀 있으면 그 축 값이 같은(또는 한쪽이 안 적은) 것끼리만 비교한다. 묶음마다 값이 다르면 by_sub_condition 으로 나누고 「조건 모름」 옵션(전부 접은 가장 보수적인 값)을 하나 더 둔다. 끝점 단위 시술이 겹치지 않는 주장(레이저 종류 등)은 애초에 같은 엣지 · 단위 시술 쌍에서 만나지 않는다 · 방향 축은 resolved.by_direction{a, b}.same_day 로 따로 남긴다(방향별로 접을 수 없으면 by_direction 안에서 R4)
- **R2 확인 조건 등급** — 같은 대상 키(공통 · 계열 · 단위 시술 · 제품 · 원장 항목 — 위 키에서 상속한 것 포함) × 같은 조건이면 더 엄격한 쪽(금기 > 주의 > 확인만 > 확인만(고지))을 기본값으로 한다. 덜 엄격한 원문은 alternatives 로 보관
- **R3 간격 숫자** — 같은 묶음 안 간격 숫자가 다르면 더 긴 간격 — 하한 = 하한들 중 큰 값 · 상한 = 상한들 중 큰 값 · open_high = 하나라도 위로 열림. 다른 원문은 alternatives 로 보관
- **R4 같은 날 가능 ↔ 불가** — R1 로 안 나뉘는 같은 날 가능 ↔ 불가는 불가(false). 「별도 세션」 문맥 표시로 생긴 false 는 금지 문장이 아니라 하위 조건 표시라 투표에서 뺀다(R1 세션 축)
- **R5 순서 반대** — R1 로 안 나뉘는 순서(먼저 하는 쪽) 반대는 진짜 반대 — first = null(순서 정보 없음 · 둘 다 가능이라는 뜻 아님 · 앱은 순서를 단정하지 않음) · 간격은 R3 · 의료진 질문(원천 질문)으로 보냄
- **R6 이소트레티노인 등 대기 기간** — 같은 조건의 대기 기간(개월)이 원천마다 다르면 R3 — 더 긴 쪽. 원문 조각(, . ;)의 개월 숫자마다 가장 가까운 깊이 · 박리 낱말(앞쪽 우선 · 없으면 뒤쪽 — 얕은 · 비박리 / 박리 · 심부)로 R1 로 나누고, 조각에 깊이 낱말이 없으면 모든 묶음에 들어간다. 조건 모름 = 전부 중 가장 긴 값

| X8 | 쌍 | 종류 | 처분 | 규칙 | 걸린 엣지 · 쌍 |
|---|---|---|---|---|---|
| X8-001 | M1 ↔ M2 | 순서(먼저 하는 쪽) | 의료진 확인 | R5 | E8-0005, E8-0014, E8-0066, E8-0067, E8-0068, E8-0139 … |
| X8-002 | M1 ↔ M2 | 같은 날 가능 ↔ 불가 | 조건 분리(가짜 충돌) | R1 |  |
| X8-003 | M1 ↔ M9 | 순서(먼저 하는 쪽) | 의료진 확인 | R5 | E8-0011, E8-0016, E8-0017, E8-0018, E8-0019, E8-0124 … |
| X8-004 | M11 ↔ M15 | 순서(먼저 하는 쪽) | 의료진 확인 | R5 | E8-0030, E8-0200 |
| X8-005 | M11 ↔ M5 | 순서(먼저 하는 쪽) | 의료진 확인 | R5 | E8-0028, E8-0029 |
| X8-006 | M11 ↔ M8 | 순서(먼저 하는 쪽) | 의료진 확인 | R5 | E8-0026 |
| X8-007 | M12 ↔ M8 | 간격 수치 | 보수적 선택 | R3 | E8-0042 |
| X8-008 | M15 ↔ M8 | 순서(먼저 하는 쪽) | 의료진 확인 | R5 | E8-0198 |
| X8-009 | M15 ↔ M8 | 같은 날 가능 ↔ 불가 | 조건 분리(가짜 충돌) | R1 |  |
| X8-010 | M2 ↔ M8 | 순서(먼저 하는 쪽) | 의료진 확인 | R5 | E8-0064, E8-0071, E8-0072, E8-0073, E8-0123 |
| X8-011 | M2 ↔ M8 | 같은 날 가능 ↔ 불가 | 보수적 선택 | R4 | E8-0073 |
| X8-012 | M2 ↔ M9 | 순서(먼저 하는 쪽) | 의료진 확인 | R5 | E8-0065, E8-0076, E8-0077, E8-0078, E8-0206, E8-0208 … |
| X8-013 | M2 ↔ M9 | 같은 날 가능 ↔ 불가 | 조건 분리(가짜 충돌) | R1 |  |
| X8-014 | M3 ↔ M4 | 순서(먼저 하는 쪽) | 의료진 확인 | R5 | E8-0079, E8-0083, E8-0095, E8-0160 |
| X8-015 | M4 ↔ M8 | 순서(먼저 하는 쪽) | 의료진 확인 | R5 | E8-0089, E8-0158, RP8-0061 |
| X8-016 | M4 ↔ M8 | 간격 수치 | 보수적 선택 | R3 | E8-0089, E8-0090, E8-0091, E8-0092, E8-0093, E8-0098 … |
| X8-017 | M4 ↔ M9 | 순서(먼저 하는 쪽) | 의료진 확인 | R5 | E8-0099, E8-0166, RP8-0051, RP8-0052, RP8-0075 |
| X8-018 | M5 ↔ M8 | 순서(먼저 하는 쪽) | 의료진 확인 | R5 | E8-0172 |
| X8-019 | M7 ↔ M9 | 순서(먼저 하는 쪽) | 의료진 확인 | R5 | E8-0114, E8-0226, RP8-0058 |
| X8-020 | M3 ↔ M9 | 순서(먼저 하는 쪽) (묶음) | 의료진 확인 | R5 | E8-0082, E8-0126, E8-0215, E8-0216 |
| X8-021 | M6 ↔ M9 | 순서(먼저 하는 쪽) (묶음) | 의료진 확인 | R5 | E8-0107, E8-0108 |
| X8-022 | M9 ↔ N1 | 순서(먼저 하는 쪽) (묶음) | 의료진 확인 | R5 | E8-0129, RP8-0081 |

| 대기 기간 | 조건 | 값 | 규칙 |
|---|---|---|---|
| WR8-C-ISO | 이소트레티노인 대기 기간 | 박리 · 심부: 12개월 / 얕은 · 비박리: 6개월 / 모름(전부 접음 — 가장 보수적): 12개월 | R1 · R6 |

## 조사 판 대비(항목별 이유)

| 항목 | 조사 | 지금 | 이유 |
|---|---|---|---|
| `claims.contraindications.rules` | 27 | 27 | 같음 |
| `claims.problem-combos.riskBenefit` | 15 | 17 | 조사 = 행별 대응표(순서 문장 8 → 15) · 반영 = 문장 패턴(화살표 · 「A 후 B 순서」 · 「A 후 B는 N 간격」) — P2-3 「열 시술 후 주입 시술」 · P3-3 화살표 3 등이 패턴으로 나뉨(U8-1 (나)) |
| `claims.problem-packages.complaints[].alternatives` | 2 | 2 | 같음 |
| `claims.problem-packages.complaints[].combos` | 137 | 137 | 같음 |
| `claims.synergy.links` | 115 | 115 | 같음 |
| `claims.taxonomy.modality[].products[].extracted.safety.contraindications` | 1 | 1 | 같음 |
| `claims.treatment-optimization.by_concern.contraindicated_combos` | 10 | 10 | 같음 |
| `claims.treatment-optimization.by_concern.sequence` | 42 | 42 | 같음 |
| `claims.treatment-optimization.combination_rules` | 11 | 13 | 조사 = 대응표(규칙 6 → 11) · 반영 = 패턴 — 규칙 0 의 「선행 또는 N 이상」 · 「N 이상 또는 먼저」가 주장 둘씩(순서 · 반대 방향 간격) · 규칙 0 첫 문장 「보톡스와 HIFU/RF 열시술」 쌍이 더해짐 |
| `claims.treatment-sequence.common_combos.note` | 4 | 5 | 세 번째 note 「프락셔널+MTS 채널 오픈 후 PRP …」를 조사는 화살표가 없어 버렸고, 반영은 순서 칸 「A 후 B」 패턴으로 쌍 하나를 만듦 |
| `claims.treatment-sequence.incompatible_same_day` | 6 | 6 | 같음 |
| `claims.treatment-sequence.minimum_intervals` | 7 | 7 | 같음 |
| `claims.treatment-sequence.principles` | 12 | 13 | 조사 = 대응표(쌍 문장 8 → 12) · 반영 = 패턴 — 원칙 2 가 순서 · 반대 방향 간격 · 생략 상대 3 = 5 주장(조사 4) |
| `conflicts.간격 수치` | 4 | 2 | 반영은 간격 사전 open_high(이상 · 후 · 뒤 = 위로 열림)로 겹침을 비교 — 조사의 「원문 범위 그대로 하한 비교」와 달라 X8-007(M15↔M4) · X8-012(M2↔M8) · X8-020/021(M7↔M9)이 빠지고 M4↔M8 · M12↔M8 이 생김. M2↔M8 · M7↔M9 는 순서 충돌로 질문 Q8-3 · Q8-4 에 남음 |
| `conflicts.같은 날 가능 ↔ 불가` | 4 | 4 | 같음 |
| `conflicts.순서(먼저 하는 쪽)` | 13 | 16 | 패턴 분해로 순서 주장이 바뀌어 계열 쌍 순서 충돌이 다시 셈 — M12↔M8 등 쌍이 달라짐(전부 질문 Q8-2~6 · 14~16 에 걸림) · 10-30 충돌 하나로 전수 가드 — 묶음 낱말 끝점(「열 시술」 · 「주입 시술」)을 계열로 펴 순서 반대 3 쌍을 뒤에 더함(X8-020~022 · 기존 X8 id 유지) |
| `condition_claims` | 378 | 373 | 조사의 「고민 조건 금기(기미) 5」가 확인 조건에서 빠져 피함 엣지로 감(U8-2 (가)) |
| `avoid_edges` | 0 | 5 | 조사 판에는 피함 엣지 타입이 없었음(U8-2 (가)로 새로 생김 — 기미 5) |
| `bundle_claims` | 3 | 2 | 조사의 묶음 낱말 주장 중 「에너지 기기(HIFU)」가 괄호 이름 규칙(bundle_paren_rule)으로 HIFU 로 풀려 묶음에서 빠짐 |
| `claim_kinds` | (json) | (json) | 종류 이름이 패턴 종류로 재분배 — 원칙 문장(쌍) · 조합 규칙(쌍) 이 없어지고 순서(문장) · 순서 · 간격(문장) · 병행 · 간격(문장) · 조합 금기로 감 · 같은 날 불가 12 → 7(조사가 「같은 날 불가」로 둔 금기 문장 일부가 「간격 금기」 · 「조합 금기」 패턴으로 감) |

## 관계 주장

| id | 원천 | 종류 | A | B | first | days | same_day | 표시 | 규칙 | 충돌 처분 |
|---|---|---|---|---|---|---|---|---|---|---|
| R8-0001 | `contraindications.rules`[0] | 병행 · 간격 | 보톡스→계열:M1 | 필러→계열:M2 | a |  | True |  | 구조 칸(from · to · level · interval · note) | 의료진 확인 |
| R8-0002 | `contraindications.rules`[1] | 병행 · 간격 | 보톡스→계열:M1 | 실리프팅→계열:M7 |  | [14.0, 14.0] |  |  | 구조 칸(from · to · level · interval · note) | 보수적 선택 |
| R8-0003 | `contraindications.rules`[2] | 병행 · 간격 | 보톡스→계열:M1 | 레이저→계열:M8 |  |  |  | 하위 조건별 값(by_sub_condition — options[].sub_condition 별로 읽음) | 구조 칸(from · to · level · interval · note) |  |
| R8-0004 | `contraindications.rules`[3] | 병행 · 간격 | 보톡스→계열:M1 | 기기 리프팅→계열:M9 |  | [14.0, 14.0] |  |  | 구조 칸(from · to · level · interval · note) | 보수적 선택 |
| R8-0005 | `contraindications.rules`[4] | 병행 · 간격 | 보톡스→계열:M1 | 스킨부스터→계열:M4 |  |  | True |  | 구조 칸(from · to · level · interval · note) |  |
| R8-0006 | `contraindications.rules`[5] | 병행 · 간격 | 보톡스→계열:M1 | 니들RF→계열:M11 |  | [14.0, 14.0] |  |  | 구조 칸(from · to · level · interval · note) |  |
| R8-0007 | `contraindications.rules`[6] | 병행 · 간격 | 필러→계열:M2 | 실리프팅→계열:M7 | b |  | True |  | 구조 칸(from · to · level · interval · note) |  |
| R8-0008 | `contraindications.rules`[7] | 병행 · 간격 | 필러→계열:M2 | 레이저→계열:M8 |  | [14.0, 28.0] |  |  | 구조 칸(from · to · level · interval · note) | 보수적 선택 |
| R8-0009 | `contraindications.rules`[8] | 병행 · 간격 | 필러→계열:M2 | 기기 리프팅→계열:M9 |  | [28.0, 28.0]+ |  |  | 구조 칸(from · to · level · interval · note) |  |
| R8-0010 | `contraindications.rules`[9] | 병행 · 간격 | 필러→계열:M2 | 니들RF→계열:M11 |  | [28.0, 28.0]+ |  |  | 구조 칸(from · to · level · interval · note) |  |
| R8-0011 | `contraindications.rules`[10] | 병행 · 간격 | 필러→계열:M2 | 마이크로니들링(MTS)→계열:M12 |  | [14.0, 14.0] |  |  | 구조 칸(from · to · level · interval · note) |  |
| R8-0012 | `contraindications.rules`[11] | 병행 · 간격 | 바이오스티뮬레이터/콜라겐부스터→계열:M3 | 기기 리프팅→계열:M9 |  | [28.0, 28.0] |  |  | 구조 칸(from · to · level · interval · note) | 보수적 선택 |
| R8-0013 | `contraindications.rules`[12] | 병행 · 간격 | 바이오스티뮬레이터/콜라겐부스터→계열:M3 | 레이저→계열:M8 |  |  |  | 하위 조건별 값(by_sub_condition — options[].sub_condition 별로 읽음) | 구조 칸(from · to · level · interval · note) | 보수적 선택 |
| R8-0014 | `contraindications.rules`[13] | 병행 · 간격 | 스킨부스터→계열:M4 | 레이저→계열:M8 | b | [7.0, 7.0] |  |  | 구조 칸(from · to · level · interval · note) | 의료진 확인 |
| R8-0015 | `contraindications.rules`[14] | 병행 · 간격 | 스킨부스터→계열:M4 | 마이크로니들링(MTS)→계열:M12 |  |  | True |  | 구조 칸(from · to · level · interval · note) |  |
| R8-0016 | `contraindications.rules`[15] | 병행 · 간격 | PRP/자가혈→계열:M5 | 마이크로니들링(MTS)→계열:M12 |  |  | True |  | 구조 칸(from · to · level · interval · note) |  |
| R8-0017 | `contraindications.rules`[16] | 병행 · 간격 | PRP/자가혈→계열:M5 | 레이저→계열:M8 |  |  | True |  | 구조 칸(from · to · level · interval · note) |  |
| R8-0018 | `contraindications.rules`[17] | 병행 · 간격 | 실리프팅→계열:M7 | 기기 리프팅→계열:M9 |  | [60.0, 90.0] |  |  | 구조 칸(from · to · level · interval · note) | 보수적 선택 |
| R8-0019 | `contraindications.rules`[18] | 병행 · 간격 | 실리프팅→계열:M7 | 레이저→계열:M8 |  | [28.0, 28.0] |  |  | 구조 칸(from · to · level · interval · note) |  |
| R8-0020 | `contraindications.rules`[19] | 병행 · 간격 | 실리프팅→계열:M7 | 니들RF→계열:M11 |  | [60.0, 90.0] |  |  | 구조 칸(from · to · level · interval · note) |  |
| R8-0021 | `contraindications.rules`[20] | 병행 · 간격 | 레이저→계열:M8 | 기기 리프팅→계열:M9 |  | [14.0, 28.0] |  |  | 구조 칸(from · to · level · interval · note) |  |
| R8-0022 | `contraindications.rules`[21] | 병행 · 간격 | 레이저→계열:M8 | 니들RF→계열:M11 |  | [14.0, 14.0] |  |  | 구조 칸(from · to · level · interval · note) |  |
| R8-0023 | `contraindications.rules`[22] | 병행 · 간격 | 레이저→계열:M8 | 마이크로니들링(MTS)→계열:M12 | a | [14.0, 14.0] |  |  | 구조 칸(from · to · level · interval · note) | 보수적 선택 |
| R8-0024 | `contraindications.rules`[23] | 병행 · 간격 | 기기 리프팅→계열:M9 | 니들RF→계열:M11 |  | [14.0, 28.0] |  |  | 구조 칸(from · to · level · interval · note) |  |
| R8-0025 | `contraindications.rules`[24] | 병행 · 간격 | 지방이식→계열:M6 | 기기 리프팅→계열:M9 |  | [90.0, 90.0]+ |  |  | 구조 칸(from · to · level · interval · note) |  |
| R8-0026 | `contraindications.rules`[25] | 병행 · 간격 | 지방이식→계열:M6 | 레이저→계열:M8 |  | [60.0, 90.0] |  |  | 구조 칸(from · to · level · interval · note) |  |
| R8-0027 | `contraindications.rules`[26] | 병행 · 간격 | 지방이식→계열:M6 | 필러→계열:M2 |  | [90.0, 90.0] |  |  | 구조 칸(from · to · level · interval · note) |  |
| R8-0028 | `synergy.links`[0] | 시너지(함께) | M1-보톡스→계열:M1 | M2-필러→계열:M2 |  |  | True |  | 구조 칸(from · to · type · timing) |  |
| R8-0029 | `synergy.links`[1] | 시너지(함께) | M1-보톡스→계열:M1 | M4-스킨부스터→계열:M4 |  |  | True |  | 구조 칸(from · to · type · timing) |  |
| R8-0030 | `synergy.links`[2] | 시너지(함께) | M1-보톡스→계열:M1 | M9-리프팅기기→계열:M9 |  | [0.0, 14.0] | True | 하위 조건 · 「또는」 별 값(options) | 구조 칸(from · to · type · timing) |  |
| R8-0031 | `synergy.links`[3] | 순서 · 간격(다음에) | M1-보톡스→계열:M1 | M9-리프팅기기→계열:M9 | a | [14.0, 14.0]+ |  |  | 구조 칸(from · to · type · timing) | 의료진 확인 |
| R8-0032 | `synergy.links`[4] | 시너지(함께) | M1-사각턱보톡스→단위 시술:U5-006 | M2-턱필러→부위 조건:U5-085 |  |  | True |  | 구조 칸(from · to · type · timing) |  |
| R8-0033 | `synergy.links`[5] | 순서 · 간격(다음에) | M10-HIFES→계열:M10 | M1-보톡스→계열:M1 | a | [14.0, 14.0]+ |  |  | 구조 칸(from · to · type · timing) |  |
| R8-0034 | `synergy.links`[6] | 시너지(함께) | M10-HIFES→계열:M10 | M9-리프팅기기→계열:M9 |  |  | True |  | 구조 칸(from · to · type · timing) |  |
| R8-0035 | `synergy.links`[7] | 대체(택 1) | M11-포텐자→단위 시술:U5-110 | M11-시크릿→제품 → 단위 시술:U5-110 |  |  |  | 대체(택 1) — 간격 비움 | 구조 칸(from · to · type · timing) |  |
| R8-0036 | `synergy.links`[8] | 대체(택 1) | M11-포텐자→단위 시술:U5-110 | M11-인트라셀→제품 → 단위 시술:U5-110,U5-111 |  |  |  | 대체(택 1) — 간격 비움 | 구조 칸(from · to · type · timing) |  |
| R8-0037 | `synergy.links`[9] | 대체(택 1) | M11-인트라셀→제품 → 단위 시술:U5-110,U5-111 | M11-시크릿→제품 → 단위 시술:U5-110 |  |  |  | 대체(택 1) — 간격 비움 | 구조 칸(from · to · type · timing) |  |
| R8-0038 | `synergy.links`[10] | 순서 · 간격(다음에) | M11-니들RF→계열:M11 | M12-MTS→계열:M12 | a | [28.0, 28.0]+ |  |  | 구조 칸(from · to · type · timing) |  |
| R8-0039 | `synergy.links`[11] | 순서 · 간격(다음에) | M11-니들RF→계열:M11 | M15-필링→기법 조건:U5-034 | a | [14.0, 14.0]+ |  |  | 구조 칸(from · to · type · timing) | 의료진 확인 |
| R8-0040 | `synergy.links`[12] | 순서 · 간격(다음에) | M11-니들RF→계열:M11 | M4-스킨부스터→계열:M4 | a | [14.0, 14.0]+ |  |  | 구조 칸(from · to · type · timing) |  |
| R8-0041 | `synergy.links`[13] | 시너지(함께) | M11-니들RF→계열:M11 | M5-PRP→단위 시술:U5-020 |  |  | True |  | 구조 칸(from · to · type · timing) |  |
| R8-0042 | `synergy.links`[14] | 시너지(함께) | M12-MTS→계열:M12 | M17-엑소좀→하위 계열:U5-019,U5-040,U5-142 |  |  | True |  | 구조 칸(from · to · type · timing) |  |
| R8-0043 | `synergy.links`[15] | 시너지(함께) | M12-MTS→계열:M12 | M4-스킨부스터→계열:M4 |  |  | True |  | 구조 칸(from · to · type · timing) |  |
| R8-0044 | `synergy.links`[16] | 시너지(함께) | M12-MTS→계열:M12 | M5-PRP→단위 시술:U5-020 |  |  | True |  | 구조 칸(from · to · type · timing) |  |
| R8-0045 | `synergy.links`[17] | 시너지(함께) | M13-플라즈마→계열:M13 | M15-메디컬스킨케어→계열:M15 |  |  | True |  | 구조 칸(from · to · type · timing) |  |
| R8-0046 | `synergy.links`[18] | 시너지(함께) | M13-플라즈마→계열:M13 | M4-스킨부스터→계열:M4 |  |  | True |  | 구조 칸(from · to · type · timing) |  |
| R8-0047 | `synergy.links`[19] | 시너지(함께) | M14-크라이오→계열:M14 | M10-HIFES→계열:M10 |  |  | True |  | 구조 칸(from · to · type · timing) |  |
| R8-0048 | `synergy.links`[20] | 순서 · 간격(다음에) | M14-크라이오→계열:M14 | M10-HIFES(바디)→부위 조건:U5-105,U5-106,U5-108,U5-109 | a | [14.0, 14.0]+ |  |  | 구조 칸(from · to · type · timing) |  |
| R8-0049 | `synergy.links`[21] | 시너지(함께) | M14-크라이오→계열:M14 | M9-인모드(바디)→계열:M9 |  | [0.0, 14.0] | True | 하위 조건 · 「또는」 별 값(options) | 구조 칸(from · to · type · timing) |  |
| R8-0050 | `synergy.links`[22] | 순서 · 간격(다음에) | M15-필링→기법 조건:U5-034 | M11-니들RF→계열:M11 | a | [14.0, 14.0]+ |  |  | 구조 칸(from · to · type · timing) | 의료진 확인 |
| R8-0051 | `synergy.links`[23] | 순서 · 간격(다음에) | M15-필링→기법 조건:U5-034 | M12-MTS→계열:M12 | a | [14.0, 14.0]+ |  |  | 구조 칸(from · to · type · timing) |  |
| R8-0052 | `synergy.links`[24] | 순서 · 간격(다음에) | M15-필링→기법 조건:U5-034 | M4-스킨부스터→계열:M4 | a | [7.0, 7.0]+ |  |  | 구조 칸(from · to · type · timing) | 보수적 선택 |
| R8-0053 | `synergy.links`[25] | 시너지(함께) | M16-수액치료→계열:M16 | M4-스킨부스터→계열:M4 |  |  | True |  | 구조 칸(from · to · type · timing) |  |
| R8-0054 | `synergy.links`[26] | 시너지(함께) | M16-수액치료→계열:M16 | M8-레이저토닝→단위 시술:U5-023 |  |  | True |  | 구조 칸(from · to · type · timing) |  |
| R8-0055 | `synergy.links`[27] | 시너지(함께) | M17-줄기세포→계열:M17 | M12-MTS→계열:M12 |  |  | True |  | 구조 칸(from · to · type · timing) |  |
| R8-0056 | `synergy.links`[28] | 시너지(함께) | M17-줄기세포→계열:M17 | M4-스킨부스터→계열:M4 |  |  | True |  | 구조 칸(from · to · type · timing) |  |
| R8-0057 | `synergy.links`[29] | 시너지(함께) | M17-줄기세포→계열:M17 | M8-저출력레이저(두피)→하위 계열:U5-039 |  |  | True |  | 구조 칸(from · to · type · timing) |  |
| R8-0058 | `synergy.links`[30] | 시너지(함께) | M2-필러→계열:M2 | M1-보톡스→계열:M1 |  |  | True |  | 구조 칸(from · to · type · timing) |  |
| R8-0059 | `synergy.links`[31] | 순서 · 간격(다음에) | M2-필러→계열:M2 | M4-스킨부스터→계열:M4 | a | [14.0, 14.0]+ |  |  | 구조 칸(from · to · type · timing) |  |
| R8-0060 | `synergy.links`[32] | 시너지(함께) | M2-필러→계열:M2 | M7-실리프팅→계열:M7 |  |  | True |  | 구조 칸(from · to · type · timing) |  |
| R8-0061 | `synergy.links`[33] | 순서 · 간격(다음에) | M2-필러→계열:M2 | M9-리프팅기기→계열:M9 | a | [14.0, 14.0]+ |  |  | 구조 칸(from · to · type · timing) | 의료진 확인 |
| R8-0062 | `synergy.links`[34] | 시너지(함께) | M2-코필러→단위 시술:U5-084 | M1-보톡스(코끝)→부위 조건:U5-015 |  |  | True |  | 구조 칸(from · to · type · timing) |  |
| R8-0063 | `synergy.links`[35] | 시너지(함께) | M3-엘란쎄→단위 시술:U5-090 | M1-보톡스→계열:M1 |  |  | True |  | 구조 칸(from · to · type · timing) |  |
| R8-0064 | `synergy.links`[36] | 대체(택 1) | M3-엘란쎄→단위 시술:U5-090 | M3-래디어스→단위 시술:U5-090 |  |  |  | 대체(택 1) — 간격 비움 | 구조 칸(from · to · type · timing) |  |
| R8-0065 | `synergy.links`[37] | 순서 · 간격(다음에) | M3-엘란쎄→단위 시술:U5-090 | M9-리프팅기기→계열:M9 | a | [30.0, 30.0]+ |  |  | 구조 칸(from · to · type · timing) | 의료진 확인 |
| R8-0066 | `synergy.links`[38] | 시너지(함께) | M3-래디어스→단위 시술:U5-090 | M1-보톡스→계열:M1 |  |  | True |  | 구조 칸(from · to · type · timing) |  |
| R8-0067 | `synergy.links`[39] | 순서 · 간격(다음에) | M3-래디어스→단위 시술:U5-090 | M4-스킨부스터→계열:M4 | a | [28.0, 28.0]+ |  |  | 구조 칸(from · to · type · timing) | 의료진 확인 |
| R8-0068 | `synergy.links`[40] | 대체(택 1) | M3-스컬트라→단위 시술:U5-090 | M3-엘란쎄→단위 시술:U5-090 |  |  |  | 대체(택 1) — 간격 비움 | 구조 칸(from · to · type · timing) |  |
| R8-0069 | `synergy.links`[41] | 대체(택 1) | M3-스컬트라→단위 시술:U5-090 | M3-래디어스→단위 시술:U5-090 |  |  |  | 대체(택 1) — 간격 비움 | 구조 칸(from · to · type · timing) |  |
| R8-0070 | `synergy.links`[42] | 순서 · 간격(다음에) | M3-스컬트라→단위 시술:U5-090 | M4-스킨부스터→계열:M4 | a | [28.0, 28.0]+ |  |  | 구조 칸(from · to · type · timing) | 의료진 확인 |
| R8-0071 | `synergy.links`[43] | 순서 · 간격(다음에) | M3-스컬트라→단위 시술:U5-090 | M9-써마지→단위 시술:U5-091,U5-104 | a | [30.0, 30.0]+ |  |  | 구조 칸(from · to · type · timing) | 의료진 확인 |
| R8-0072 | `synergy.links`[44] | 순서 · 간격(다음에) | M3-스컬트라→단위 시술:U5-090 | M9-울쎄라→단위 시술:U5-102,U5-103 | a | [30.0, 30.0]+ |  |  | 구조 칸(from · to · type · timing) | 의료진 확인 |
| R8-0073 | `synergy.links`[45] | 순서 · 간격(다음에) | M3-바이오스티뮬레이터→계열:M3 | M4-스킨부스터→계열:M4 | a | [28.0, 28.0]+ |  |  | 구조 칸(from · to · type · timing) | 의료진 확인 |
| R8-0074 | `synergy.links`[46] | 시너지(함께) | M4-리쥬란→단위 시술:U5-018 | M1-보톡스→계열:M1 |  |  | True |  | 구조 칸(from · to · type · timing) |  |
| R8-0075 | `synergy.links`[47] | 시너지(함께) | M4-리쥬란→단위 시술:U5-018 | M2-필러→계열:M2 |  |  | True |  | 구조 칸(from · to · type · timing) |  |
| R8-0076 | `synergy.links`[48] | 시너지(함께) | M4-리쥬란→단위 시술:U5-018 | M4-쥬베룩→단위 시술:U5-090 |  | [0.0, 14.0] | True | 하위 조건 · 「또는」 별 값(options) | 구조 칸(from · to · type · timing) |  |
| R8-0077 | `synergy.links`[49] | 순서 · 간격(다음에) | M4-리쥬란→단위 시술:U5-018 | M8-레이저토닝→단위 시술:U5-023 | a | [14.0, 14.0]+ |  |  | 구조 칸(from · to · type · timing) | 의료진 확인 |
| R8-0078 | `synergy.links`[50] | 시너지(함께) | M4-쥬베룩→단위 시술:U5-090 | M1-보톡스→계열:M1 |  |  | True |  | 구조 칸(from · to · type · timing) |  |
| R8-0079 | `synergy.links`[51] | 시너지(함께) | M4-쥬베룩→단위 시술:U5-090 | M11-니들RF→계열:M11 |  |  | True |  | 구조 칸(from · to · type · timing) |  |
| R8-0080 | `synergy.links`[52] | 시너지(함께) | M4-쥬베룩→단위 시술:U5-090 | M5-PRP→단위 시술:U5-020 |  |  | True |  | 구조 칸(from · to · type · timing) |  |
| R8-0081 | `synergy.links`[53] | 시너지(함께) | M4-스킨부스터→계열:M4 | M12-MTS→계열:M12 |  |  | True |  | 구조 칸(from · to · type · timing) |  |
| R8-0082 | `synergy.links`[54] | 순서 · 간격(다음에) | M4-스킨부스터→계열:M4 | M15-필링→기법 조건:U5-034 | b | [7.0, 7.0]+ |  |  | 구조 칸(from · to · type · timing) | 보수적 선택 |
| R8-0083 | `synergy.links`[55] | 시너지(함께) | M4-스킨부스터→계열:M4 | M3-바이오스티뮬레이터→계열:M3 |  | [0.0, 14.0] | True | 하위 조건 · 「또는」 별 값(options) | 구조 칸(from · to · type · timing) |  |
| R8-0084 | `synergy.links`[56] | 순서 · 간격(다음에) | M4-스킨부스터→계열:M4 | M8-레이저토닝→단위 시술:U5-023 | a | [14.0, 14.0]+ |  |  | 구조 칸(from · to · type · timing) | 의료진 확인 |
| R8-0085 | `synergy.links`[57] | 순서 · 간격(다음에) | M4-스킨부스터→계열:M4 | M9-울쎄라→단위 시술:U5-102,U5-103 | a | [14.0, 14.0]+ |  |  | 구조 칸(from · to · type · timing) | 의료진 확인 |
| R8-0086 | `synergy.links`[58] | 시너지(함께) | M5-PRP→단위 시술:U5-020 | M12-MTS(두피)→부위 조건:U5-112 |  |  | True |  | 구조 칸(from · to · type · timing) |  |
| R8-0087 | `synergy.links`[59] | 시너지(함께) | M5-PRP→단위 시술:U5-020 | M17-줄기세포→계열:M17 |  |  | True |  | 구조 칸(from · to · type · timing) |  |
| R8-0088 | `synergy.links`[60] | 시너지(함께) | M5-PRP→단위 시술:U5-020 | M4-스킨부스터→계열:M4 |  |  | True |  | 구조 칸(from · to · type · timing) |  |
| R8-0089 | `synergy.links`[61] | 시너지(함께) | M5-PRP→단위 시술:U5-020 | M8-프락셔널→기법 조건:U5-026,U5-027,U5-028,U5-029 |  |  | True |  | 구조 칸(from · to · type · timing) |  |
| R8-0090 | `synergy.links`[62] | 순서 · 간격(다음에) | M5-PRP→단위 시술:U5-020 | M8-레이저토닝→단위 시술:U5-023 | a | [14.0, 14.0]+ |  |  | 구조 칸(from · to · type · timing) | 의료진 확인 |
| R8-0091 | `synergy.links`[63] | 순서 · 간격(다음에) | M6-지방이식→계열:M6 | M1-보톡스→계열:M1 | a | [30.0, 30.0]+ |  |  | 구조 칸(from · to · type · timing) |  |
| R8-0092 | `synergy.links`[64] | 시너지(함께) | M6-지방이식→계열:M6 | M17-줄기세포→계열:M17 |  |  | True | 조건부(원문 「…에 한해」) | 구조 칸(from · to · type · timing) |  |
| R8-0093 | `synergy.links`[65] | 시너지(함께) | M6-지방이식→계열:M6 | M5-PRP→단위 시술:U5-020 |  |  | True |  | 구조 칸(from · to · type · timing) |  |
| R8-0094 | `synergy.links`[66] | 순서 · 간격(다음에) | M7-실리프팅→계열:M7 | M1-보톡스→계열:M1 | a | [14.0, 14.0]+ |  |  | 구조 칸(from · to · type · timing) |  |
| R8-0095 | `synergy.links`[67] | 시너지(함께) | M7-실리프팅→계열:M7 | M2-필러→계열:M2 |  |  | True |  | 구조 칸(from · to · type · timing) |  |
| R8-0096 | `synergy.links`[68] | 순서 · 간격(다음에) | M7-실리프팅→계열:M7 | M3-스컬트라→단위 시술:U5-090 | a | [30.0, 30.0]+ |  |  | 구조 칸(from · to · type · timing) |  |
| R8-0097 | `synergy.links`[69] | 순서 · 간격(다음에) | M7-실리프팅→계열:M7 | M4-스킨부스터→계열:M4 | a | [14.0, 14.0]+ |  |  | 구조 칸(from · to · type · timing) |  |
| R8-0098 | `synergy.links`[70] | 순서 · 간격(다음에) | M7-실리프팅→계열:M7 | M9-써마지→단위 시술:U5-091,U5-104 | a | [30.0, 30.0]+ |  |  | 구조 칸(from · to · type · timing) | 보수적 선택 |
| R8-0099 | `synergy.links`[71] | 순서 · 간격(다음에) | M7-실리프팅→계열:M7 | M9-울쎄라→단위 시술:U5-102,U5-103 | a | [60.0, 90.0]+ |  |  | 구조 칸(from · to · type · timing) | 의료진 확인 |
| R8-0100 | `synergy.links`[72] | 순서 · 간격(다음에) | M8-서브시전→단위 시술:U5-045 | M11-니들RF→계열:M11 | a | [28.0, 28.0]+ |  |  | 구조 칸(from · to · type · timing) |  |
| R8-0101 | `synergy.links`[73] | 시너지(함께) | M8-서브시전→단위 시술:U5-045 | M2-필러→계열:M2 |  |  | True |  | 구조 칸(from · to · type · timing) |  |
| R8-0102 | `synergy.links`[74] | 시너지(함께) | M8-서브시전→단위 시술:U5-045 | M5-PRP→단위 시술:U5-020 |  |  | True |  | 구조 칸(from · to · type · timing) |  |
| R8-0103 | `synergy.links`[75] | 순서 · 간격(다음에) | M8-프락셔널→기법 조건:U5-026,U5-027,U5-028,U5-029 | M12-MTS→계열:M12 | a | [28.0, 28.0]+ |  |  | 구조 칸(from · to · type · timing) |  |
| R8-0104 | `synergy.links`[76] | 시너지(함께) | M8-프락셔널→기법 조건:U5-026,U5-027,U5-028,U5-029 | M17-줄기세포→계열:M17 |  |  | True |  | 구조 칸(from · to · type · timing) |  |
| R8-0105 | `synergy.links`[77] | 순서 · 간격(다음에) | M8-프락셔널→기법 조건:U5-026,U5-027,U5-028,U5-029 | M4-스킨부스터→계열:M4 | a | [14.0, 14.0]+ |  |  | 구조 칸(from · to · type · timing) |  |
| R8-0106 | `synergy.links`[78] | 시너지(함께) | M8-프락셔널→기법 조건:U5-026,U5-027,U5-028,U5-029 | M5-PRP→단위 시술:U5-020 |  |  | True |  | 구조 칸(from · to · type · timing) |  |
| R8-0107 | `synergy.links`[79] | 대체(택 1) | M8-피코슈어→제품 → 단위 시술:U5-024,U5-025,U5-026,U5-027… | M8-피코웨이→제품 → 단위 시술:U5-023,U5-025,U5-099,U5-131… |  |  |  | 대체(택 1) — 간격 비움 | 구조 칸(from · to · type · timing) |  |
| R8-0108 | `synergy.links`[80] | 순서 · 간격(다음에) | M8-피코토닝→단위 시술:U5-023 | M4-리쥬란→단위 시술:U5-018 | a | [14.0, 14.0]+ |  |  | 구조 칸(from · to · type · timing) | 의료진 확인 |
| R8-0109 | `synergy.links`[81] | 순서 · 간격(다음에) | M8-피코토닝→단위 시술:U5-023 | M4-쥬베룩→단위 시술:U5-090 | a | [14.0, 14.0]+ |  |  | 구조 칸(from · to · type · timing) | 보수적 선택 |
| R8-0110 | `synergy.links`[82] | 순서 · 간격(다음에) | M8-피코토닝→단위 시술:U5-023 | M4-스킨부스터→계열:M4 | a | [7.0, 14.0]+ |  |  | 구조 칸(from · to · type · timing) | 의료진 확인 |
| R8-0111 | `synergy.links`[83] | 시너지(함께) | M8-레이저토닝→단위 시술:U5-023 | M15-필링→기법 조건:U5-034 |  |  | True |  | 구조 칸(from · to · type · timing) |  |
| R8-0112 | `synergy.links`[84] | 순서 · 간격(다음에) | M8-혈관레이저→용도 조건:U5-099,U5-141 | M4-스킨부스터→계열:M4 | a | [14.0, 14.0]+ |  |  | 구조 칸(from · to · type · timing) |  |
| R8-0113 | `synergy.links`[85] | 대체(택 1) | M8-알렉산드라이트→하위 계열:U5-024,U5-026 | M8-다이오드→하위 계열:U5-039 |  |  |  | 대체(택 1) — 간격 비움 | 구조 칸(from · to · type · timing) |  |
| R8-0114 | `synergy.links`[86] | 대체(택 1) | M8-알렉산드라이트→하위 계열:U5-024,U5-026 | M8-IPL→단위 시술:U5-030 |  |  |  | 대체(택 1) — 간격 비움 | 구조 칸(from · to · type · timing) |  |
| R8-0115 | `synergy.links`[87] | 순서 · 간격(다음에) | M8-CO2레이저→하위 계열:U5-028 | M17-줄기세포→계열:M17 | a | [0.0, 7.0]+ | True | 하위 조건 · 「또는」 별 값(options) | 구조 칸(from · to · type · timing) |  |
| R8-0116 | `synergy.links`[88] | 순서 · 간격(다음에) | M8-CO2레이저→하위 계열:U5-028 | M4-스킨부스터→계열:M4 | a | [14.0, 14.0]+ |  |  | 구조 칸(from · to · type · timing) |  |
| R8-0117 | `synergy.links`[89] | 시너지(함께) | M8-CO2레이저→하위 계열:U5-028 | M5-PRP→단위 시술:U5-020 |  |  | True |  | 구조 칸(from · to · type · timing) |  |
| R8-0118 | `synergy.links`[90] | 시너지(함께) | M8-IPL→단위 시술:U5-030 | M1-보톡스→계열:M1 |  |  | True |  | 구조 칸(from · to · type · timing) |  |
| R8-0119 | `synergy.links`[91] | 시너지(함께) | M8-IPL→단위 시술:U5-030 | M2-필러→계열:M2 |  |  | True |  | 구조 칸(from · to · type · timing) | 보수적 선택 |
| R8-0120 | `synergy.links`[92] | 순서 · 간격(다음에) | M8-IPL→단위 시술:U5-030 | M4-스킨부스터→계열:M4 | a | [14.0, 14.0]+ |  |  | 구조 칸(from · to · type · timing) |  |
| R8-0121 | `synergy.links`[93] | 순서 · 간격(다음에) | M9-더블로→제품 → 단위 시술:U5-102,U5-103,U5-154 | M1-보톡스→계열:M1 | a | [14.0, 14.0]+ |  |  | 구조 칸(from · to · type · timing) | 의료진 확인 |
| R8-0122 | `synergy.links`[94] | 순서 · 간격(다음에) | M9-더블로→제품 → 단위 시술:U5-102,U5-103,U5-154 | M4-스킨부스터→계열:M4 | a | [14.0, 14.0]+ |  |  | 구조 칸(from · to · type · timing) | 의료진 확인 |
| R8-0123 | `synergy.links`[95] | 시너지(함께) | M9-볼뉴머→단위 시술:U5-091 | M1-보톡스→계열:M1 |  |  | True |  | 구조 칸(from · to · type · timing) |  |
| R8-0124 | `synergy.links`[96] | 순서 · 간격(다음에) | M9-볼뉴머→단위 시술:U5-091 | M9-리프팅기기→계열:M9 |  |  |  | 의료진 판단(간격 원천 없음) | 구조 칸(from · to · type · timing) |  |
| R8-0125 | `synergy.links`[97] | 순서 · 간격(다음에) | M9-슈링크→제품 → 단위 시술:U5-102,U5-103,U5-154 | M1-보톡스→계열:M1 | a | [14.0, 14.0]+ |  |  | 구조 칸(from · to · type · timing) | 의료진 확인 |
| R8-0126 | `synergy.links`[98] | 순서 · 간격(다음에) | M9-슈링크→제품 → 단위 시술:U5-102,U5-103,U5-154 | M4-스킨부스터→계열:M4 | a | [14.0, 14.0]+ |  |  | 구조 칸(from · to · type · timing) | 의료진 확인 |
| R8-0127 | `synergy.links`[99] | 대체(택 1) | M9-슈링크→제품 → 단위 시술:U5-102,U5-103,U5-154 | M9-더블로→제품 → 단위 시술:U5-102,U5-103,U5-154 |  |  |  | 대체(택 1) — 간격 비움 | 구조 칸(from · to · type · timing) |  |
| R8-0128 | `synergy.links`[100] | 시너지(함께) | M9-슈링크→제품 → 단위 시술:U5-102,U5-103,U5-154 | M9-써마지→단위 시술:U5-091,U5-104 |  |  | True |  | 구조 칸(from · to · type · timing) |  |
| R8-0129 | `synergy.links`[101] | 대체(택 1) | M9-써마지→단위 시술:U5-091,U5-104 | M9-슈링크→제품 → 단위 시술:U5-102,U5-103,U5-154 |  |  |  | 대체(택 1) — 간격 비움 | 구조 칸(from · to · type · timing) |  |
| R8-0130 | `synergy.links`[102] | 대체(택 1) | M9-써마지→단위 시술:U5-091,U5-104 | M9-올리지오→제품 → 단위 시술:U5-091,U5-104,U5-152 |  |  |  | 대체(택 1) — 간격 비움 | 구조 칸(from · to · type · timing) |  |
| R8-0131 | `synergy.links`[103] | 순서 · 간격(다음에) | M9-울쎄라→단위 시술:U5-102,U5-103 | M1-보톡스→계열:M1 | a | [14.0, 14.0]+ |  |  | 구조 칸(from · to · type · timing) | 의료진 확인 |
| R8-0132 | `synergy.links`[104] | 순서 · 간격(다음에) | M9-울쎄라→단위 시술:U5-102,U5-103 | M4-스킨부스터→계열:M4 | a | [14.0, 14.0]+ |  |  | 구조 칸(from · to · type · timing) | 의료진 확인 |
| R8-0133 | `synergy.links`[105] | 순서 · 간격(다음에) | M9-울쎄라→단위 시술:U5-102,U5-103 | M7-실리프팅→계열:M7 | a | [30.0, 30.0]+ |  |  | 구조 칸(from · to · type · timing) | 의료진 확인 |
| R8-0134 | `synergy.links`[106] | 대체(택 1) | M9-울쎄라→단위 시술:U5-102,U5-103 | M9-더블로→제품 → 단위 시술:U5-102,U5-103,U5-154 |  |  |  | 대체(택 1) — 간격 비움 | 구조 칸(from · to · type · timing) |  |
| R8-0135 | `synergy.links`[107] | 대체(택 1) | M9-울쎄라→단위 시술:U5-102,U5-103 | M9-슈링크→제품 → 단위 시술:U5-102,U5-103,U5-154 |  |  |  | 대체(택 1) — 간격 비움 | 구조 칸(from · to · type · timing) |  |
| R8-0136 | `synergy.links`[108] | 시너지(함께) | M9-울쎄라→단위 시술:U5-102,U5-103 | M9-써마지→단위 시술:U5-091,U5-104 |  |  | True |  | 구조 칸(from · to · type · timing) |  |
| R8-0137 | `synergy.links`[109] | 시너지(함께) | M9-울쎄라→단위 시술:U5-102,U5-103 | M9-인모드→단위 시술:U5-091 |  |  | True |  | 구조 칸(from · to · type · timing) |  |
| R8-0138 | `synergy.links`[110] | 순서 · 간격(다음에) | M9-인모드→단위 시술:U5-091 | M1-보톡스→계열:M1 | a | [14.0, 14.0]+ |  |  | 구조 칸(from · to · type · timing) | 의료진 확인 |
| R8-0139 | `synergy.links`[111] | 순서 · 간격(다음에) | M9-인모드→단위 시술:U5-091 | M4-스킨부스터→계열:M4 | a | [14.0, 14.0]+ |  |  | 구조 칸(from · to · type · timing) |  |
| R8-0140 | `synergy.links`[112] | 대체(택 1) | M9-인모드→단위 시술:U5-091 | M9-써마지→단위 시술:U5-091,U5-104 |  |  |  | 대체(택 1) — 간격 비움 | 구조 칸(from · to · type · timing) |  |
| R8-0141 | `synergy.links`[113] | 대체(택 1) | M9-올리지오→제품 → 단위 시술:U5-091,U5-104,U5-152 | M9-울쎄라→단위 시술:U5-102,U5-103 |  |  |  | 대체(택 1) — 간격 비움 | 구조 칸(from · to · type · timing) |  |
| R8-0142 | `synergy.links`[114] | 순서 · 간격(다음에) | M9-리프팅기기→계열:M9 | M4-스킨부스터→계열:M4 | a | [14.0, 14.0] |  |  | 구조 칸(from · to · type · timing) | 의료진 확인 |
| R8-0143 | `treatment-sequence.incompatible_same_day`[0] | 같은 날 불가 | CO2 프락셔널→단위 시술:U5-028 | 필러→계열:M2 |  |  | False | 같은 날 불가(구조 칸) | 구조 칸(pair) |  |
| R8-0144 | `treatment-sequence.incompatible_same_day`[1] | 같은 날 불가 | 심부 필링(페놀)→기법 조건:U5-034 | 레이저→계열:M8 |  |  | False | 같은 날 불가(구조 칸) | 구조 칸(pair) |  |
| R8-0145 | `treatment-sequence.incompatible_same_day`[2] | 같은 날 불가 | PDO실→하위 계열:U5-022,U5-097,U5-098,U5-122 | 비가교HA→하위 계열:U5-018,U5-037,U5-041 |  |  | False | 같은 날 불가(구조 칸) | 구조 칸(pair) |  |
| R8-0146 | `treatment-sequence.incompatible_same_day`[4] | 같은 날 불가 | HA 필러→하위 계열:U5-082,U5-083,U5-084,U5-085… | RF→하위 계열:U5-091,U5-104,U5-152 + HIFU→하위 계열:U5-102,U5-103,U5-154 | a |  | False | 같은 날 불가(구조 칸) | 구조 칸(pair) | 의료진 확인 |
| R8-0147 | `treatment-sequence.incompatible_same_day`[5] | 같은 날 불가 | HA 필러→하위 계열:U5-082,U5-083,U5-084,U5-085… | 레이저→계열:M8 |  |  | False | 같은 날 불가(구조 칸) | 구조 칸(pair) |  |
| R8-0148 | `treatment-sequence.incompatible_same_day`[6] | 같은 날 불가 | 심부 필링(TCA 50%+/페놀)→기법 조건:U5-034 | 모든 시술→모든 시술: |  |  | False | 같은 날 불가(구조 칸) | 구조 칸(pair) |  |
| R8-0149 | `treatment-sequence.minimum_intervals`[0] | 간격 | HA 필러→하위 계열:U5-082,U5-083,U5-084,U5-085… | RF→하위 계열:U5-091,U5-104,U5-152 + HIFU→하위 계열:U5-102,U5-103,U5-154 | a | [14.0, 14.0]+ |  |  | 구조 칸(from · to · min_days) | 의료진 확인 |
| R8-0150 | `treatment-sequence.minimum_intervals`[1] | 간격 | HA 필러→하위 계열:U5-082,U5-083,U5-084,U5-085… | 레이저→계열:M8 | a | [5.0, 5.0]+ |  |  | 구조 칸(from · to · min_days) | 의료진 확인 |
| R8-0151 | `treatment-sequence.minimum_intervals`[4] | 간격 | 심부 필링→기법 조건:U5-034 | 레이저→계열:M8 | a | [14.0, 14.0]+ |  |  | 구조 칸(from · to · min_days) | 의료진 확인 |
| R8-0152 | `treatment-sequence.minimum_intervals`[5] | 간격 | 프락셔널 CO2→단위 시술:U5-028 | 필러→계열:M2 | a | [14.0, 14.0]+ |  |  | 구조 칸(from · to · min_days) | 의료진 확인 |
| R8-0153 | `treatment-sequence.minimum_intervals`[6] | 간격 | 보톡스→계열:M1 | 필러 (별도 세션)→계열:M2 | a | [14.0, 14.0]+ |  |  | 구조 칸(from · to · min_days) |  |
| R8-0154 | `treatment-sequence.minimum_intervals`[7] | 간격 | RF→하위 계열:U5-091,U5-104,U5-152 + HIFU→하위 계열:U5-102,U5-103,U5-154 | 필러→계열:M2 | a | [0.0, 0.0]+ | True |  | 구조 칸(from · to · min_days) | 의료진 확인 |
| R8-0155 | `treatment-sequence.minimum_intervals`[8] | 재시술 간격(자기 쌍) | 필러→계열:M2 | 필러 (동일 부위 재시술)→계열:M2 | a | [14.0, 14.0]+ |  |  | 구조 칸(from · to · min_days) |  |
| R8-0156 | `treatment-sequence.principles`[1] | 순서 · 간격(문장) | 보톡스→계열:M1 | HIFU→하위 계열:U5-102,U5-103,U5-154 + RF 열시술→조건 일치(낱말 교집합):U5-091,U5-104,U5-152 | b |  | True |  | S-OKFIRST |  |
| R8-0157 | `treatment-sequence.principles`[2] | 순서(문장) | HIFU→하위 계열:U5-102,U5-103,U5-154 | 보톡스→계열:M1 | a |  |  |  | S-FIRSTORGAP#순서 | 의료진 확인 |
| R8-0158 | `treatment-sequence.principles`[2] | 간격 | 보톡스→계열:M1 | HIFU→하위 계열:U5-102,U5-103,U5-154 | a | [14.0, 14.0]+ |  |  | S-FIRSTORGAP#간격 | 의료진 확인 |
| R8-0159 | `treatment-sequence.principles`[2] | 병행 · 간격(문장) | RF→하위 계열:U5-091,U5-104,U5-152 | 보톡스→계열:M1 |  |  | True | 생략 상대 = 앞 절 대상(ellipsis_rule) | S-LISTELLIPSIS |  |
| R8-0160 | `treatment-sequence.principles`[2] | 병행 · 간격(문장) | IPL→단위 시술:U5-030 | 보톡스→계열:M1 |  |  | True | 생략 상대 = 앞 절 대상(ellipsis_rule) | S-LISTELLIPSIS |  |
| R8-0161 | `treatment-sequence.principles`[2] | 병행 · 간격(문장) | 비침습 레이저→계열:M8 | 보톡스→계열:M1 |  |  | True | 생략 상대 = 앞 절 대상(ellipsis_rule) | S-LISTELLIPSIS |  |
| R8-0162 | `treatment-sequence.principles`[3] | 순서 · 간격(문장) | 레이저→계열:M8 + IPL→단위 시술:U5-030 | 필러→계열:M2 | a |  |  | 순서만(「…전에」) | S-BEFORE | 의료진 확인 |
| R8-0163 | `treatment-sequence.principles`[8] | 순서(문장 화살표) | 필러 먼저(위치 안정화)→계열:M2 | 보톡스 나중에 (필러 위치 보존, 전문가 합의 기반 기본값, 같은 날엔 순서 유연)→계열:M1 | a |  | True | 순서 유연(원문 「순서 유연 · 무관」) · 같은 날 · 별도 세션 문맥(문장 머리) | S-CTXARROW | 의료진 확인 |
| R8-0164 | `treatment-sequence.principles`[9] | 순서(문장 화살표) | 보톡스 먼저→계열:M1 | 필러 (보톡스 효과 안정 후 필러 위치 정밀 결정)→계열:M2 | a | [14.0, 14.0]+ | False | 같은 날 · 별도 세션 문맥(문장 머리) | S-CTXARROW |  |
| R8-0165 | `treatment-sequence.principles`[10] | 순서 · 간격(문장) | HA 필러→하위 계열:U5-082,U5-083,U5-084,U5-085… | RF→하위 계열:U5-091,U5-104,U5-152 + HIFU→하위 계열:U5-102,U5-103,U5-154 | a | [14.0, 14.0]+ |  |  | S-ARROWCOLON | 의료진 확인 |
| R8-0166 | `treatment-sequence.principles`[11] | 순서 · 간격(문장) | RF→하위 계열:U5-091,U5-104,U5-152 + HIFU→하위 계열:U5-102,U5-103,U5-154 | 필러→계열:M2 | a |  | True |  | S-ARROWCOLON | 의료진 확인 |
| R8-0167 | `treatment-sequence.principles`[11] | 순서 · 간격(문장) | 필러→계열:M2 | RF→하위 계열:U5-091,U5-104,U5-152 + HIFU→하위 계열:U5-102,U5-103,U5-154 | a | [14.0, 14.0]+ |  |  | S-REVERSE | 의료진 확인 |
| R8-0168 | `treatment-sequence.principles`[12] | 순서 · 간격(문장) | 필러→계열:M2 | 레이저→계열:M8 | a | [5.0, 5.0]+ |  |  | S-ARROWCOLON | 의료진 확인 |
| R8-0169 | `treatment-optimization.combination_rules`[0] | 순서 · 간격(문장) | 보톡스→계열:M1 | HIFU→하위 계열:U5-102,U5-103,U5-154 + RF 열시술→조건 일치(낱말 교집합):U5-091,U5-104,U5-152 | b |  | True |  | S-OKFIRST |  |
| R8-0170 | `treatment-optimization.combination_rules`[0] | 순서(문장) | MFU→하위 계열:U5-102,U5-103,U5-154 + HIFU→하위 계열:U5-102,U5-103,U5-154 | 보톡스→계열:M1 | a |  |  |  | S-FIRSTORGAP#순서 | 의료진 확인 |
| R8-0171 | `treatment-optimization.combination_rules`[0] | 간격 | 보톡스→계열:M1 | MFU→하위 계열:U5-102,U5-103,U5-154 + HIFU→하위 계열:U5-102,U5-103,U5-154 | a | [14.0, 14.0]+ |  |  | S-FIRSTORGAP#간격 | 의료진 확인 |
| R8-0172 | `treatment-optimization.combination_rules`[0] | 간격 | HA 필러→하위 계열:U5-082,U5-083,U5-084,U5-085… | HIFU→하위 계열:U5-102,U5-103,U5-154 | a | [28.0, 28.0]+ |  |  | S-GAPORFIRST#간격 | 의료진 확인 |
| R8-0173 | `treatment-optimization.combination_rules`[0] | 순서(문장) | HA 필러→하위 계열:U5-082,U5-083,U5-084,U5-085… | HIFU→하위 계열:U5-102,U5-103,U5-154 | b |  |  |  | S-GAPORFIRST#순서 | 의료진 확인 |
| R8-0174 | `treatment-optimization.combination_rules`[0] | 병행 · 간격(문장) | RF→하위 계열:U5-091,U5-104,U5-152 | 보톡스→계열:M1 |  |  | True |  | S-LISTPARTNER |  |
| R8-0175 | `treatment-optimization.combination_rules`[0] | 병행 · 간격(문장) | IPL→단위 시술:U5-030 | 보톡스→계열:M1 |  |  | True |  | S-LISTPARTNER |  |
| R8-0176 | `treatment-optimization.combination_rules`[0] | 병행 · 간격(문장) | 비침습 레이저→계열:M8 | 보톡스→계열:M1 |  |  | True |  | S-LISTPARTNER |  |
| R8-0177 | `treatment-optimization.combination_rules`[1] | 간격 금기 | HA 필러→하위 계열:U5-082,U5-083,U5-084,U5-085… | RF→하위 계열:U5-091,U5-104,U5-152 + HIFU→하위 계열:U5-102,U5-103,U5-154 | a | [14.0, 14.0]+ |  |  | S-WITHINRISK | 의료진 확인 |
| R8-0178 | `treatment-optimization.combination_rules`[3] | 간격 금기 | 프락셔널→기법 조건:U5-026,U5-027,U5-028,U5-029 | 필러→계열:M2 | a | [28.0, 28.0]+ | False |  | S-AFTERFORBID | 의료진 확인 |
| R8-0179 | `treatment-optimization.combination_rules`[5] | 순서(문장 화살표) | 필러 먼저→계열:M2 | 보톡스 나중.→계열:M1 | a |  | True |  | S-CTXCOLON | 의료진 확인 |
| R8-0180 | `treatment-optimization.combination_rules`[6] | 간격 금기 | 레이저 제모→용도 조건:U5-100,U5-101,U5-144,U5-145… | 필링→기법 조건:U5-034 + 프락셔널→기법 조건:U5-026,U5-027,U5-028,U5-029 | a | [14.0, 14.0]+ |  |  | S-AFTERFORBID |  |
| R8-0181 | `treatment-optimization.combination_rules`[7] | 조합 금기 | PDO실→하위 계열:U5-022,U5-097,U5-098,U5-122 | 비가교HA→하위 계열:U5-018,U5-037,U5-041 |  |  | False |  | S-PLUSFORBID |  |
| R8-0182 | `treatment-optimization.by_concern.sequence`[0.0] | 순서(문장 화살표) | 토닝 먼저→기법 조건:U5-023,U5-024,U5-025 | 스킨부스터→계열:M4 | a | [14.0, 14.0]+ |  |  | S-ARROW | 의료진 확인 |
| R8-0183 | `treatment-optimization.by_concern.sequence`[0.1] | 순서(문장 화살표) | 필러→계열:M2 | 스킨부스터→계열:M4 | a |  | True |  | S-ARROW |  |
| R8-0184 | `treatment-optimization.by_concern.sequence`[0.1] | 순서(문장 화살표) | 스킨부스터→계열:M4 | 보톡스→계열:M1 | a |  | True |  | S-ARROW |  |
| R8-0185 | `treatment-optimization.by_concern.sequence`[0.1] | 순서(문장 화살표) | 보톡스 먼저→계열:M1 | 필러→계열:M2 | a | [14.0, 14.0]+ |  |  | S-ARROW |  |
| R8-0186 | `treatment-optimization.by_concern.sequence`[0.2] | 순서(문장 화살표) | HIFU→하위 계열:U5-102,U5-103,U5-154 + RF→하위 계열:U5-091,U5-104,U5-152 | 보톡스(같은날 가능)→계열:M1 | a |  | True |  | S-ARROW |  |
| R8-0187 | `treatment-optimization.by_concern.sequence`[0.2] | 순서(문장 화살표) | 보톡스(같은날 가능)→계열:M1 | 필러→계열:M2 | a | [14.0, 14.0]+ |  |  | S-ARROW |  |
| R8-0188 | `treatment-optimization.by_concern.sequence`[0.2] | 순서(문장 화살표) | 필러→계열:M2 | 스킨부스터→계열:M4 | a |  |  |  | S-ARROW |  |
| R8-0189 | `treatment-optimization.by_concern.contraindicated_combos`[0.2.0] | 간격 금기 | HA 필러→하위 계열:U5-082,U5-083,U5-084,U5-085… | RF→하위 계열:U5-091,U5-104,U5-152 + HIFU→하위 계열:U5-102,U5-103,U5-154 | a | [14.0, 14.0]+ |  |  | S-AFTERFORBID | 의료진 확인 |
| R8-0190 | `treatment-optimization.by_concern.sequence`[1.0] | 순서(문장 화살표) | RF 시술→하위 계열:U5-091,U5-104,U5-152 | 스킨부스터→계열:M4 | a | [14.0, 14.0]+ |  |  | S-ARROW |  |
| R8-0191 | `treatment-optimization.by_concern.sequence`[1.1] | 순서(문장 화살표) | HIFU 먼저→하위 계열:U5-102,U5-103,U5-154 | 보톡스 가능→계열:M1 | a |  | True |  | S-ARROW |  |
| R8-0192 | `treatment-optimization.by_concern.sequence`[1.1] | 순서(문장 화살표) | 보톡스 가능→계열:M1 | 바이오스티뮬레이터 시작→계열:M3 | a | [28.0, 28.0]+ |  |  | S-ARROW |  |
| R8-0193 | `treatment-optimization.by_concern.sequence`[1.2] | 순서(문장 화살표) | 울쎄라 HIFU→조건 일치(낱말 교집합):U5-102,U5-103 | 실리프팅→계열:M7 | a | [14.0, 28.0]+ |  |  | S-ARROW | 의료진 확인 |
| R8-0194 | `treatment-optimization.by_concern.sequence`[1.2] | 순서(문장 화살표) | 실리프팅→계열:M7 | 필러(볼륨 보충)→계열:M2 | a |  |  |  | S-ARROW |  |
| R8-0195 | `treatment-optimization.by_concern.sequence`[1.2] | 순서(문장 화살표) | 필러(볼륨 보충)→계열:M2 | 바이오스티뮬레이터(유지)→계열:M3 | a |  |  |  | S-ARROW |  |
| R8-0196 | `treatment-optimization.by_concern.contraindicated_combos`[1.2.0] | 조합 금기 | PDO실→하위 계열:U5-022,U5-097,U5-098,U5-122 | 비가교HA→하위 계열:U5-018,U5-037,U5-041 |  |  | False |  | S-PLUSFORBID |  |
| R8-0197 | `treatment-optimization.by_concern.sequence`[2.0] | 순서(문장 화살표) | HA 볼류마이징 스킨부스터 먼저→조건 일치(낱말 교집합):U5-018,U5-037,U5-041 | 바이오스티뮬레이터→계열:M3 | a | [28.0, 28.0] |  |  | S-ARROW | 의료진 확인 |
| R8-0198 | `treatment-optimization.by_concern.sequence`[2.1] | 순서(문장 화살표) | 필러로 즉각 볼륨→계열:M2 | 바이오스티뮬레이터(콜라겐 장기 재생)→계열:M3 | a | [28.0, 28.0]+ |  |  | S-ARROW |  |
| R8-0199 | `treatment-optimization.by_concern.sequence`[2.2] | 순서(문장 화살표) | 지방이식→계열:M6 + 딥필러→계열:M2 | CaHA→하위 계열:U5-090 + 바이오스티뮬→계열:M3 | a | [28.0, 28.0]+ |  |  | S-ARROW |  |
| R8-0200 | `treatment-optimization.by_concern.contraindicated_combos`[2.2.0] | 간격 금기 | 지방이식→계열:M6 | RF→하위 계열:U5-091,U5-104,U5-152 + HIFU→하위 계열:U5-102,U5-103,U5-154 | a | [14.0, 14.0]+ |  |  | S-AFTERFORBID | 의료진 확인 |
| R8-0201 | `treatment-optimization.by_concern.sequence`[3.0] | 순서(문장 화살표) | 토닝→기법 조건:U5-023,U5-024,U5-025 | 얕은 필링 가능→기법 조건:U5-034 | a |  | True |  | S-ARROW |  |
| R8-0202 | `treatment-optimization.by_concern.sequence`[3.0] | 순서(문장 화살표) | 얕은 필링 가능→기법 조건:U5-034 | 스킨부스터→계열:M4 | a | [14.0, 14.0]+ |  |  | S-ARROW |  |
| R8-0203 | `treatment-optimization.by_concern.sequence`[3.1] | 순서(문장 화살표) | 프락셔널→기법 조건:U5-026,U5-027,U5-028,U5-029 + 니들RF→계열:M11 | 스킨부스터→계열:M4 | a |  |  | 반복 사이(사이사이) — 간격 없음 · 앞 시술 반복(원문 「4주 간격 반복」) | S-ARROW |  |
| R8-0204 | `treatment-optimization.by_concern.contraindicated_combos`[3.1.0] | 간격 금기 | 프락셔널→기법 조건:U5-026,U5-027,U5-028,U5-029 | 필러→계열:M2 | a |  | False |  | S-AFTERFORBID | 의료진 확인 |
| R8-0205 | `treatment-optimization.by_concern.sequence`[3.2] | 순서(문장 화살표) | CO2 프락셔널→단위 시술:U5-028 | PRP→단위 시술:U5-020 + 엑소좀→하위 계열:U5-019,U5-040,U5-142 | a | [0, 0] | True |  | S-ARROW |  |
| R8-0206 | `treatment-optimization.by_concern.sequence`[3.2] | 순서(문장 화살표) | PRP→단위 시술:U5-020 + 엑소좀→하위 계열:U5-019,U5-040,U5-142 | 니들RF→계열:M11 | a | [28.0, 28.0]+ |  |  | S-ARROW | 의료진 확인 |
| R8-0207 | `treatment-optimization.by_concern.sequence`[3.2] | 순서(문장 화살표) | 니들RF→계열:M11 | 스킨부스터→계열:M4 | a |  |  |  | S-ARROW |  |
| R8-0208 | `treatment-optimization.by_concern.contraindicated_combos`[3.2.0] | 간격 금기 | CO2 프락셔널→단위 시술:U5-028 | 필러→계열:M2 | a |  | False |  | S-AFTERFORBID | 의료진 확인 |
| R8-0209 | `treatment-optimization.by_concern.sequence`[4.0] | 순서(문장 화살표) | 피코토닝→단위 시술:U5-023 | IPL(같은날 가능, 토닝 먼저)→단위 시술:U5-030 | a |  | True |  | S-ARROW |  |
| R8-0210 | `treatment-optimization.by_concern.sequence`[4.0] | 순서(문장 화살표) | IPL(같은날 가능, 토닝 먼저)→단위 시술:U5-030 | 비타민C 도포→시술 아님: | a |  |  |  | S-ARROW |  |
| R8-0211 | `treatment-optimization.by_concern.sequence`[4.1] | 순서(문장 화살표) | 트라넥삼산 경구 시작→시술 아님: | 피코토닝→단위 시술:U5-023 + 저출력 IPL→단위 시술:U5-030 | a | [14.0, 14.0]+ |  |  | S-ARROW |  |
| R8-0212 | `treatment-optimization.by_concern.sequence`[4.1] | 순서(문장 화살표) | 피코토닝→단위 시술:U5-023 + 저출력 IPL→단위 시술:U5-030 | 스킨부스터(미백)→계열:M4 | a |  |  |  | S-ARROW |  |
| R8-0213 | `treatment-optimization.by_concern.sequence`[4.2] | 순서(문장 화살표) | 트라넥삼산 경구→시술 아님: + 국소→시술 아님: | 저출력 피코토닝 장기→단위 시술:U5-023 | a |  |  |  | S-ARROW |  |
| R8-0214 | `treatment-optimization.by_concern.sequence`[4.2] | 순서(문장 화살표) | 저출력 피코토닝 장기→단위 시술:U5-023 | 마이크로니들→계열:M12 + 미백약→시술 아님: | a |  |  |  | S-ARROW |  |
| R8-0215 | `treatment-optimization.by_concern.sequence`[4.2] | 순서(문장 화살표) | 마이크로니들→계열:M12 + 미백약→시술 아님: | 스킨부스터→계열:M4 | a |  |  |  | S-ARROW |  |
| R8-0216 | `treatment-optimization.by_concern.sequence`[5.0] | 순서(문장 화살표) | ALA-PDT→단위 시술:U5-049 | 필링→기법 조건:U5-034 | a | [14.0, 14.0] |  |  | S-ARROW | 의료진 확인 |
| R8-0217 | `treatment-optimization.by_concern.sequence`[5.0] | 순서(문장 화살표) | 필링→기법 조건:U5-034 | LED(매회 마무리)→하위 계열:U5-043,U5-050 | a |  |  |  | S-ARROW |  |
| R8-0218 | `treatment-optimization.by_concern.sequence`[5.1] | 순서(문장 화살표) | 서브시전(깊은 흉터 박리)→단위 시술:U5-045 | 프락셔널→기법 조건:U5-026,U5-027,U5-028,U5-029 + 니들RF→계열:M11 | a | [28.0, 28.0]+ |  |  | S-ARROW |  |
| R8-0219 | `treatment-optimization.by_concern.sequence`[5.1] | 순서(문장 화살표) | 프락셔널→기법 조건:U5-026,U5-027,U5-028,U5-029 + 니들RF→계열:M11 | PRP 동시 도포→단위 시술:U5-020 | a |  | True |  | S-ARROW |  |
| R8-0220 | `treatment-optimization.by_concern.sequence`[5.2] | 순서(문장 화살표) | 서브시전→단위 시술:U5-045 + TCA Cross→해석 안 됨: | CO2 프락셔널→단위 시술:U5-028 | a | [28.0, 28.0]+ |  |  | S-ARROW |  |
| R8-0221 | `treatment-optimization.by_concern.sequence`[5.2] | 순서(문장 화살표) | CO2 프락셔널→단위 시술:U5-028 | PRP 즉시 도포→단위 시술:U5-020 | a | [0, 0] | True |  | S-ARROW |  |
| R8-0222 | `treatment-optimization.by_concern.sequence`[5.2] | 순서(문장 화살표) | PRP 즉시 도포→단위 시술:U5-020 | 필러(남은 함몰)→계열:M2 | a |  |  |  | S-ARROW |  |
| R8-0223 | `treatment-optimization.by_concern.contraindicated_combos`[5.2.0] | 간격 금기 | CO2→하위 계열:U5-028 | 필러→계열:M2 | a |  | False |  | S-AFTERFORBID | 의료진 확인 |
| R8-0224 | `treatment-optimization.by_concern.contraindicated_combos`[6.1.0] | 간격 금기 | 제모→용도 조건:U5-100,U5-101,U5-144,U5-145… | 왁싱→시술 아님: + 전기분해→시술 아님: | a | [14.0, 14.0]+ |  |  | S-AFTERFORBID |  |
| R8-0225 | `treatment-optimization.by_concern.sequence`[6.2] | 순서(문장 화살표) | 듀얼파장 레이저→조건 일치(낱말 교집합):U5-023,U5-024,U5-025,U5-026… | IPL로 잔여 유지→단위 시술:U5-030 | a |  |  | 회차(횟수 — 간격 아님) | S-ARROW |  |
| R8-0226 | `treatment-optimization.by_concern.contraindicated_combos`[6.2.0] | 같은 날 불가 | 제모→용도 조건:U5-100,U5-101,U5-144,U5-145… | 필링→기법 조건:U5-034 + 프락셔널→기법 조건:U5-026,U5-027,U5-028,U5-029 |  |  | False |  | S-SITESAMEFORBID |  |
| R8-0227 | `treatment-optimization.by_concern.sequence`[7.0] | 순서(문장 화살표) | 크라이오 먼저→계열:M14 | RF 4-6회→하위 계열:U5-091,U5-104,U5-152 | a | [14.0, 14.0]+ |  |  | S-ARROW |  |
| R8-0228 | `treatment-optimization.by_concern.sequence`[7.1] | 순서(문장 화살표) | 지방분해주사→계열:N1 + 크라이오→계열:M14 | RF로 타이트닝→하위 계열:U5-091,U5-104,U5-152 | a |  |  | 앞 시술 반복(원문 「4주 간격 반복」) | S-ARROW | 의료진 확인 |
| R8-0229 | `treatment-optimization.by_concern.sequence`[7.1] | 순서(문장 화살표) | RF로 타이트닝→하위 계열:U5-091,U5-104,U5-152 | 카복시로 순환 개선→계열:N2 | a |  |  |  | S-ARROW |  |
| R8-0230 | `treatment-optimization.by_concern.contraindicated_combos`[7.1.0] | 간격 금기 | 지방분해주사→계열:N1 | RF→하위 계열:U5-091,U5-104,U5-152 | a | [1.0, 1.0]+ |  |  | S-AFTERFORBID | 의료진 확인 |
| R8-0231 | `treatment-optimization.by_concern.sequence`[7.2] | 순서(문장 화살표) | 지방흡입(수술)→계열:N10 | 바디 HIFU→단위 시술:U5-154 + RF→하위 계열:U5-152 | a | [28.0, 42.0] |  |  | S-ARROW | 보수적 선택 |
| R8-0232 | `treatment-optimization.by_concern.sequence`[7.2] | 순서(문장 화살표) | 바디 HIFU→단위 시술:U5-154 + RF→하위 계열:U5-152 | 카복시 유지→계열:N2 | a |  |  |  | S-ARROW |  |
| R8-0233 | `treatment-optimization.by_concern.contraindicated_combos`[7.2.0] | 간격 금기 | 지방흡입→계열:N10 | RF→하위 계열:U5-091,U5-104,U5-152 + HIFU→하위 계열:U5-102,U5-103,U5-154 | a | [28.0, 28.0]+ |  |  | S-AFTERFORBID | 보수적 선택 |
| R8-0234 | `treatment-sequence.common_combos.note`[5] | 순서(문장 화살표) | 필러 위치 안정화 먼저→계열:M2 | 스킨부스터→계열:M4 | a |  |  |  | S-ARROW |  |
| R8-0235 | `treatment-sequence.common_combos.note`[5] | 순서(문장 화살표) | 스킨부스터→계열:M4 | 보톡스 마지막 순서 준수→계열:M1 | a |  |  |  | S-ARROW |  |
| R8-0236 | `treatment-sequence.common_combos.note`[6] | 순서(문장 화살표) | 에너지 기기(HIFU) 먼저→하위 계열:U5-102,U5-103,U5-154 | 레이저 토닝→단위 시술:U5-023 | a |  |  |  | S-ARROW |  |
| R8-0237 | `treatment-sequence.common_combos.note`[6] | 순서(문장 화살표) | 레이저 토닝→단위 시술:U5-023 | 스킨부스터 마지막→계열:M4 | a |  |  |  | S-ARROW | 의료진 확인 |
| R8-0238 | `treatment-sequence.common_combos.note`[7] | 순서(문장) | 프락셔널→기법 조건:U5-026,U5-027,U5-028,U5-029 + MTS→계열:M12 | PRP 성장인자 경피 침투 극대화→조건 일치(낱말 교집합):U5-020,U5-042 | a |  |  |  | S-AFTERGENERIC |  |
| R8-0239 | `problem-combos.riskBenefit`[P2-3] | 순서(문장) | 열 시술→계열 묶음:M11,M8,M9 | 주입 시술→계열 묶음:M1,M17,M2,M3,M4,M5,M6,N1 | a |  |  |  | S-AFTERORDER | 의료진 확인 |
| R8-0240 | `problem-combos.riskBenefit`[P3-2] | 순서(문장) | 울쎄라 열응고→단위 시술:U5-102,U5-103 | 보톡스 주입→계열:M1 | a |  |  |  | S-AFTERORDER | 의료진 확인 |
| R8-0241 | `problem-combos.riskBenefit`[P3-3] | 순서(문장 화살표) | HIFU→하위 계열:U5-102,U5-103,U5-154 | 보톡스→계열:M1 | a |  |  |  | S-ARROW | 의료진 확인 |
| R8-0242 | `problem-combos.riskBenefit`[P3-3] | 순서(문장 화살표) | 보톡스→계열:M1 | 필러→계열:M2 | a |  |  |  | S-ARROW | 의료진 확인 |
| R8-0243 | `problem-combos.riskBenefit`[P3-3] | 순서(문장 화살표) | 필러→계열:M2 | 스킨부스터.→계열:M4 | a |  |  |  | S-ARROW |  |
| R8-0244 | `problem-combos.riskBenefit`[P3-4] | 순서 · 간격(문장) | 실리프팅→계열:M7 | HIFU→하위 계열:U5-102,U5-103,U5-154 | a | [60.0, 90.0] | False | 같은 날이면 다른 부위 | S-AFTERGAP | 의료진 확인 |
| R8-0245 | `problem-combos.riskBenefit`[P4-3] | 순서(문장 화살표) | 레이저→계열:M8 | MTS→계열:M12 | a |  |  |  | S-ARROW |  |
| R8-0246 | `problem-combos.riskBenefit`[P4-3] | 순서(문장 화살표) | MTS→계열:M12 | PRP→단위 시술:U5-020 | a |  |  |  | S-ARROW |  |
| R8-0247 | `problem-combos.riskBenefit`[P4-3] | 순서(문장 화살표) | PRP→단위 시술:U5-020 | 스킨부스터→계열:M4 | a |  |  |  | S-ARROW |  |
| R8-0248 | `problem-combos.riskBenefit`[P5-3] | 순서(문장 화살표) | 레이저→계열:M8 | 니들RF→계열:M11 | a |  |  |  | S-ARROW | 의료진 확인 |
| R8-0249 | `problem-combos.riskBenefit`[P5-3] | 순서(문장 화살표) | 니들RF→계열:M11 | PRP→단위 시술:U5-020 | a |  |  |  | S-ARROW | 의료진 확인 |
| R8-0250 | `problem-combos.riskBenefit`[P5-3] | 순서(문장 화살표) | PRP→단위 시술:U5-020 | SB 순서 엄수.→계열:M4 | a |  |  |  | S-ARROW |  |
| R8-0251 | `problem-combos.riskBenefit`[P7-3] | 순서(문장 화살표) | 니들RF→계열:M11 | 레이저→계열:M8 | a |  |  |  | S-ARROW | 의료진 확인 |
| R8-0252 | `problem-combos.riskBenefit`[P7-3] | 순서(문장 화살표) | 레이저→계열:M8 | PRP→단위 시술:U5-020 | a |  |  |  | S-ARROW | 의료진 확인 |
| R8-0253 | `problem-combos.riskBenefit`[P7-3] | 순서(문장 화살표) | PRP→단위 시술:U5-020 | SB 순서.→계열:M4 | a |  |  |  | S-ARROW |  |
| R8-0254 | `problem-combos.riskBenefit`[P11-2] | 순서(문장 화살표) | HIFU→하위 계열:U5-102,U5-103,U5-154 + RF→하위 계열:U5-091,U5-104,U5-152 | 보톡스→계열:M1 | a |  |  |  | S-ARROW | 의료진 확인 |
| R8-0255 | `problem-combos.riskBenefit`[P11-2] | 순서(문장 화살표) | 보톡스→계열:M1 | 필러 순서.→계열:M2 | a |  |  |  | S-ARROW | 의료진 확인 |
| R8-0256 | `problem-packages.complaints[].combos`[P1:코필러#0] | 시너지(CC 조합) | 필러→단위 시술:U5-084 | 보톡스→단위 시술:U5-005,U5-015 |  |  |  |  | 구조 칸(combo) |  |
| R8-0257 | `problem-packages.complaints[].combos`[P1:코실리프팅#0] | 시너지(CC 조합) | 실리프팅→단위 시술:U5-097 | 필러→단위 시술:U5-084 |  |  |  |  | 구조 칸(combo) |  |
| R8-0258 | `problem-packages.complaints[].alternatives`[P1:코실리프팅#0] | 간격 금기 | 실 시술→계열:M7 | HIFU→하위 계열:U5-102,U5-103,U5-154 + RF→하위 계열:U5-091,U5-104,U5-152 | a | [60.0, 60.0]+ |  |  | S-AFTERFORBID | 의료진 확인 |
| R8-0259 | `problem-packages.complaints[].combos`[P1:이마필러#0] | 시너지(CC 조합) | 필러→단위 시술:U5-086 | 보톡스→단위 시술:U5-001,U5-002 |  |  |  |  | 구조 칸(combo) |  |
| R8-0260 | `problem-packages.complaints[].combos`[P1:이마지방이식#0] | 시너지(CC 조합) | 지방이식→단위 시술:U5-092 | PRP→단위 시술:U5-020 |  |  |  |  | 구조 칸(combo) |  |
| R8-0261 | `problem-packages.complaints[].combos`[P1:턱필러#0] | 시너지(CC 조합) | 필러→단위 시술:U5-085 | 보톡스→단위 시술:U5-004,U5-006,U5-016 |  |  |  |  | 구조 칸(combo) |  |
| R8-0262 | `problem-packages.complaints[].combos`[P1:턱보톡스#0] | 시너지(CC 조합) | 보톡스→단위 시술:U5-004,U5-006,U5-016 | 스킨부스터→단위 시술:U5-018,U5-037 |  |  |  |  | 구조 칸(combo) |  |
| R8-0263 | `problem-packages.complaints[].combos`[P1:턱선실리프팅#0] | 시너지(CC 조합) | 실리프팅→단위 시술:U5-122 | 필러→단위 시술:U5-085 |  |  |  |  | 구조 칸(combo) |  |
| R8-0264 | `problem-packages.complaints[].alternatives`[P1:턱선실리프팅#0] | 간격 금기 | 실 시술→계열:M7 | HIFU→하위 계열:U5-102,U5-103,U5-154 + RF→하위 계열:U5-091,U5-104,U5-152 | a | [60.0, 60.0]+ |  |  | S-AFTERFORBID | 의료진 확인 |
| R8-0265 | `problem-packages.complaints[].combos`[P1:입술필러#0] | 시너지(CC 조합) | 필러→단위 시술:U5-083 | 보톡스→단위 시술:U5-009 |  |  |  |  | 구조 칸(combo) |  |
| R8-0266 | `problem-packages.complaints[].combos`[P1:애교필러#0] | 시너지(CC 조합) | 필러→단위 시술:U5-088 | 보톡스→단위 시술:U5-003 |  |  |  |  | 구조 칸(combo) |  |
| R8-0267 | `problem-packages.complaints[].combos`[P1:눈가보톡스#0] | 시너지(CC 조합) | 보톡스→단위 시술:U5-003 | 스킨부스터→단위 시술:U5-018,U5-037 |  |  |  |  | 구조 칸(combo) |  |
| R8-0268 | `problem-packages.complaints[].combos`[P1:다크서클필러#0] | 시너지(CC 조합) | 필러→단위 시술:U5-088 | 보톡스→단위 시술:U5-003 |  |  |  |  | 구조 칸(combo) |  |
| R8-0269 | `problem-packages.complaints[].combos`[P1:볼필러#0] | 시너지(CC 조합) | 필러→단위 시술:U5-087 | 보톡스→단위 시술:U5-009 |  |  |  |  | 구조 칸(combo) |  |
| R8-0270 | `problem-packages.complaints[].combos`[P1:볼지방이식#0] | 시너지(CC 조합) | 지방이식→단위 시술:U5-093 | PRP→단위 시술:U5-020 |  |  |  |  | 구조 칸(combo) |  |
| R8-0271 | `problem-packages.complaints[].combos`[P2:이마주름#0] | 시너지(CC 조합) | 보톡스→단위 시술:U5-001 | 리프팅기기→단위 시술:U5-091,U5-102 |  |  |  |  | 구조 칸(combo) |  |
| R8-0272 | `problem-packages.complaints[].combos`[P2:이마주름#1] | 시너지(CC 조합) | 보톡스→단위 시술:U5-001 | 스킨부스터→단위 시술:U5-018,U5-037 |  |  |  |  | 구조 칸(combo) |  |
| R8-0273 | `problem-packages.complaints[].combos`[P2:미간주름#0] | 시너지(CC 조합) | 보톡스→단위 시술:U5-002 | 리프팅기기→단위 시술:U5-091,U5-102 |  |  |  |  | 구조 칸(combo) |  |
| R8-0274 | `problem-packages.complaints[].combos`[P2:미간주름#1] | 시너지(CC 조합) | 보톡스→단위 시술:U5-002 | 스킨부스터→단위 시술:U5-018,U5-037 |  |  |  |  | 구조 칸(combo) |  |
| R8-0275 | `problem-packages.complaints[].combos`[P2:눈가주름#0] | 시너지(CC 조합) | 보톡스→단위 시술:U5-003 | 리프팅기기→단위 시술:U5-104 |  |  |  |  | 구조 칸(combo) |  |
| R8-0276 | `problem-packages.complaints[].combos`[P2:눈가주름#1] | 시너지(CC 조합) | 보톡스→단위 시술:U5-003 | 스킨부스터→단위 시술:U5-018,U5-037 |  |  |  |  | 구조 칸(combo) |  |
| R8-0277 | `problem-packages.complaints[].combos`[P2:팔자주름#0] | 시너지(CC 조합) | 보톡스→단위 시술:U5-009 | 필러→단위 시술:U5-082 |  |  |  |  | 구조 칸(combo) |  |
| R8-0278 | `problem-packages.complaints[].combos`[P2:팔자주름#1] | 시너지(CC 조합) | 필러→단위 시술:U5-082 | 리프팅기기→단위 시술:U5-091,U5-102 |  |  |  |  | 구조 칸(combo) |  |
| R8-0279 | `problem-packages.complaints[].combos`[P2:팔자주름#2] | 시너지(CC 조합) | 스킨부스터→단위 시술:U5-018,U5-037 | 리프팅기기→단위 시술:U5-091,U5-102 |  |  |  |  | 구조 칸(combo) |  |
| R8-0280 | `problem-packages.complaints[].combos`[P2:마리오네트라인#0] | 시너지(CC 조합) | 보톡스→단위 시술:U5-009 | 필러→계열:M2 |  |  |  |  | 구조 칸(combo) |  |
| R8-0281 | `problem-packages.complaints[].combos`[P2:마리오네트라인#1] | 시너지(CC 조합) | 필러→계열:M2 | 리프팅기기→단위 시술:U5-091,U5-102 |  |  |  |  | 구조 칸(combo) |  |
| R8-0282 | `problem-packages.complaints[].combos`[P2:목주름#0] | 시너지(CC 조합) | 보톡스→단위 시술:U5-017 | 필러→계열:M2 |  |  |  |  | 구조 칸(combo) |  |
| R8-0283 | `problem-packages.complaints[].combos`[P2:목주름#1] | 시너지(CC 조합) | 필러→계열:M2 | 리프팅기기→계열:M9 |  |  |  |  | 구조 칸(combo) |  |
| R8-0284 | `problem-packages.complaints[].combos`[P2:잔주름#0] | 시너지(CC 조합) | 보톡스→단위 시술:U5-001,U5-002,U5-003,U5-004… | 리프팅기기→계열:M9 |  |  |  |  | 구조 칸(combo) |  |
| R8-0285 | `problem-packages.complaints[].combos`[P2:잔주름#1] | 시너지(CC 조합) | 보톡스→단위 시술:U5-001,U5-002,U5-003,U5-004… | 스킨부스터→단위 시술:U5-018,U5-037 |  |  |  |  | 구조 칸(combo) |  |
| R8-0286 | `problem-packages.complaints[].combos`[P3:볼쳐짐/불독살#0] | 시너지(CC 조합) | 리프팅기기→단위 시술:U5-091,U5-102 | 스킨부스터→단위 시술:U5-018,U5-037 |  |  |  |  | 구조 칸(combo) |  |
| R8-0287 | `problem-packages.complaints[].combos`[P3:볼쳐짐/불독살#1] | 시너지(CC 조합) | 실리프팅→단위 시술:U5-022 | 리프팅기기→단위 시술:U5-091,U5-102 |  |  |  |  | 구조 칸(combo) |  |
| R8-0288 | `problem-packages.complaints[].combos`[P3:턱선무너짐#0] | 시너지(CC 조합) | 리프팅기기→단위 시술:U5-103 | 스킨부스터→단위 시술:U5-018,U5-037 |  |  |  |  | 구조 칸(combo) |  |
| R8-0289 | `problem-packages.complaints[].combos`[P3:턱선무너짐#1] | 시너지(CC 조합) | 실리프팅→단위 시술:U5-122 | 리프팅기기→단위 시술:U5-103 |  |  |  |  | 구조 칸(combo) |  |
| R8-0290 | `problem-packages.complaints[].combos`[P3:이중턱#0] | 시너지(CC 조합) | 리프팅기기→단위 시술:U5-091,U5-102 | 스킨부스터→단위 시술:U5-018,U5-037 |  |  |  |  | 구조 칸(combo) |  |
| R8-0291 | `problem-packages.complaints[].combos`[P3:이중턱#1] | 시너지(CC 조합) | 실리프팅→단위 시술:U5-022 | 리프팅기기→단위 시술:U5-091,U5-102 |  |  |  |  | 구조 칸(combo) |  |
| R8-0292 | `problem-packages.complaints[].combos`[P3:이중턱#2] | 시너지(CC 조합) | 크라이오→단위 시술:U5-118 | 리프팅기기→단위 시술:U5-091,U5-102 |  |  |  |  | 구조 칸(combo) |  |
| R8-0293 | `problem-packages.complaints[].combos`[P3:눈꺼풀쳐짐#0] | 시너지(CC 조합) | 리프팅기기→단위 시술:U5-104 | 스킨부스터→단위 시술:U5-018,U5-037 |  |  |  |  | 구조 칸(combo) |  |
| R8-0294 | `problem-packages.complaints[].combos`[P3:눈꺼풀쳐짐#1] | 시너지(CC 조합) | 실리프팅→단위 시술:U5-022 | 리프팅기기→단위 시술:U5-104 |  |  |  |  | 구조 칸(combo) |  |
| R8-0295 | `problem-packages.complaints[].combos`[P3:팔뚝/복부/허벅지#0] | 시너지(CC 조합) | 리프팅기기→단위 시술:U5-152,U5-154 | 스킨부스터→계열:M4 |  |  |  |  | 구조 칸(combo) |  |
| R8-0296 | `problem-packages.complaints[].combos`[P3:팔뚝/복부/허벅지#1] | 시너지(CC 조합) | 실리프팅→계열:M7 | 리프팅기기→단위 시술:U5-152,U5-154 |  |  |  |  | 구조 칸(combo) |  |
| R8-0297 | `problem-packages.complaints[].combos`[P4:스킨부스터시술#0] | 시너지(CC 조합) | 스킨부스터→단위 시술:U5-018 | 리프팅기기→계열:M9 |  |  |  |  | 구조 칸(combo) |  |
| R8-0298 | `problem-packages.complaints[].combos`[P4:필러볼륨#0] | 시너지(CC 조합) | 필러→단위 시술:U5-082,U5-083,U5-084,U5-085… | 보톡스→계열:M1 |  |  |  |  | 구조 칸(combo) |  |
| R8-0299 | `problem-packages.complaints[].combos`[P4:필러볼륨#1] | 시너지(CC 조합) | 필러→단위 시술:U5-082,U5-083,U5-084,U5-085… | 바이오스티뮬레이터→단위 시술:U5-090 |  |  |  |  | 구조 칸(combo) |  |
| R8-0300 | `problem-packages.complaints[].combos`[P4:지방이식#0] | 시너지(CC 조합) | 지방이식→단위 시술:U5-021,U5-092,U5-093,U5-094… | PRP→단위 시술:U5-020 |  |  |  |  | 구조 칸(combo) |  |
| R8-0301 | `problem-packages.complaints[].combos`[P4:지방이식#1] | 시너지(CC 조합) | 필러→단위 시술:U5-082,U5-083,U5-084,U5-085… | 바이오스티뮬레이터→단위 시술:U5-090 |  |  |  |  | 구조 칸(combo) |  |
| R8-0302 | `problem-packages.complaints[].combos`[P4:NAD+수액#0] | 시너지(CC 조합) | 수액→계열:M16 | 스킨부스터→계열:M4 |  |  |  |  | 구조 칸(combo) |  |
| R8-0303 | `problem-packages.complaints[].combos`[P4:항산화수액#0] | 시너지(CC 조합) | 수액→계열:M16 | 스킨부스터→계열:M4 |  |  |  |  | 구조 칸(combo) |  |
| R8-0304 | `problem-packages.complaints[].combos`[P5:레이저토닝#0] | 시너지(CC 조합) | 레이저→계열:M8 | 스킨부스터→단위 시술:U5-018 |  |  |  |  | 구조 칸(combo) |  |
| R8-0305 | `problem-packages.complaints[].combos`[P5:피코토닝#0] | 시너지(CC 조합) | 레이저→계열:M8 | 스킨부스터→단위 시술:U5-018 |  |  |  |  | 구조 칸(combo) |  |
| R8-0306 | `problem-packages.complaints[].combos`[P5:미백필링#0] | 시너지(CC 조합) | 레이저→계열:M8 | 스킨부스터→단위 시술:U5-018 |  |  |  |  | 구조 칸(combo) |  |
| R8-0307 | `problem-packages.complaints[].combos`[P5:피코레이저#0] | 시너지(CC 조합) | 레이저→단위 시술:U5-023,U5-024,U5-025,U5-026… | 스킨부스터→단위 시술:U5-018 |  |  |  |  | 구조 칸(combo) |  |
| R8-0308 | `problem-packages.complaints[].combos`[P5:IPL#0] | 시너지(CC 조합) | 레이저→단위 시술:U5-023,U5-024,U5-025,U5-026… | 스킨부스터→단위 시술:U5-018 |  |  |  |  | 구조 칸(combo) |  |
| R8-0309 | `problem-packages.complaints[].combos`[P5:피코/Q스위치#0] | 시너지(CC 조합) | 레이저→계열:M8 | 스킨부스터→단위 시술:U5-018 |  |  |  |  | 구조 칸(combo) |  |
| R8-0310 | `problem-packages.complaints[].combos`[P5:백옥주사#0] | 시너지(CC 조합) | 레이저→계열:M8 | 스킨부스터→단위 시술:U5-018 |  |  |  |  | 구조 칸(combo) |  |
| R8-0311 | `problem-packages.complaints[].combos`[P5:백옥주사#1] | 시너지(CC 조합) | 레이저→계열:M8 | 미백주사→계열:M16 |  |  |  |  | 구조 칸(combo) |  |
| R8-0312 | `problem-packages.complaints[].combos`[P5:비타민C주사#0] | 시너지(CC 조합) | 레이저→계열:M8 | 스킨부스터→단위 시술:U5-018 |  |  |  |  | 구조 칸(combo) |  |
| R8-0313 | `problem-packages.complaints[].combos`[P5:비타민C주사#1] | 시너지(CC 조합) | 레이저→계열:M8 | 미백주사→계열:M16 |  |  |  |  | 구조 칸(combo) |  |
| R8-0314 | `problem-packages.complaints[].combos`[P6:압출#0] | 시너지(CC 조합) | 니들RF→단위 시술:U5-110 | 필링→기법 조건:U5-034 |  |  |  |  | 구조 칸(combo) |  |
| R8-0315 | `problem-packages.complaints[].combos`[P6:PDT#0] | 시너지(CC 조합) | 니들RF→단위 시술:U5-110 | 필링→기법 조건:U5-034 |  |  |  |  | 구조 칸(combo) |  |
| R8-0316 | `problem-packages.complaints[].combos`[P6:약물치료#0] | 시너지(CC 조합) | 니들RF→단위 시술:U5-110 | 필링→기법 조건:U5-034 |  |  |  |  | 구조 칸(combo) |  |
| R8-0317 | `problem-packages.complaints[].combos`[P6:아그네스#0] | 시너지(CC 조합) | 니들RF→단위 시술:U5-110 | 스킨부스터→단위 시술:U5-018,U5-037 |  |  |  |  | 구조 칸(combo) |  |
| R8-0318 | `problem-packages.complaints[].combos`[P6:스킨보톡스#0] | 시너지(CC 조합) | 보톡스→단위 시술:U5-009 | 스킨부스터→단위 시술:U5-018 |  |  |  |  | 구조 칸(combo) |  |
| R8-0319 | `problem-packages.complaints[].combos`[P6:스킨보톡스#1] | 시너지(CC 조합) | 니들RF→단위 시술:U5-110 | 스킨부스터→단위 시술:U5-018 |  |  |  |  | 구조 칸(combo) |  |
| R8-0320 | `problem-packages.complaints[].combos`[P6:케미컬필링#0] | 시너지(CC 조합) | 니들RF→단위 시술:U5-110 | 스킨부스터→단위 시술:U5-018,U5-037 |  |  |  |  | 구조 칸(combo) |  |
| R8-0321 | `problem-packages.complaints[].combos`[P6:토닝#0] | 시너지(CC 조합) | 레이저→계열:M8 | 스킨부스터→단위 시술:U5-018,U5-037 |  |  |  |  | 구조 칸(combo) |  |
| R8-0322 | `problem-packages.complaints[].combos`[P6:재생치료#0] | 시너지(CC 조합) | 레이저→계열:M8 | 스킨부스터→단위 시술:U5-018,U5-037 |  |  |  |  | 구조 칸(combo) |  |
| R8-0323 | `problem-packages.complaints[].combos`[P7:스킨보톡스#0] | 시너지(CC 조합) | 보톡스→단위 시술:U5-009 | 스킨부스터→단위 시술:U5-018,U5-037 |  |  |  |  | 구조 칸(combo) |  |
| R8-0324 | `problem-packages.complaints[].combos`[P7:스킨보톡스#1] | 시너지(CC 조합) | 니들RF→단위 시술:U5-110 | 스킨부스터→단위 시술:U5-018,U5-037 |  |  |  |  | 구조 칸(combo) |  |
| R8-0325 | `problem-packages.complaints[].combos`[P7:아그네스#0] | 시너지(CC 조합) | 니들RF→단위 시술:U5-110 | 스킨부스터→단위 시술:U5-018,U5-037 |  |  |  |  | 구조 칸(combo) |  |
| R8-0326 | `problem-packages.complaints[].combos`[P7:프락셔널레이저#0] | 시너지(CC 조합) | 니들RF→단위 시술:U5-110 | 스킨부스터→단위 시술:U5-018,U5-037 |  |  |  |  | 구조 칸(combo) |  |
| R8-0327 | `problem-packages.complaints[].combos`[P7:프락셔널레이저#1] | 시너지(CC 조합) | 니들RF→단위 시술:U5-110 | 리프팅기기→계열:M9 |  |  |  |  | 구조 칸(combo) |  |
| R8-0328 | `problem-packages.complaints[].combos`[P7:니들RF#0] | 시너지(CC 조합) | 니들RF→단위 시술:U5-110 | 스킨부스터→단위 시술:U5-018,U5-037 |  |  |  |  | 구조 칸(combo) |  |
| R8-0329 | `problem-packages.complaints[].combos`[P7:니들RF#1] | 시너지(CC 조합) | 니들RF→단위 시술:U5-110 | 리프팅기기→계열:M9 |  |  |  |  | 구조 칸(combo) |  |
| R8-0330 | `problem-packages.complaints[].combos`[P7:CO2프락셀#0] | 시너지(CC 조합) | 니들RF→단위 시술:U5-110 | 스킨부스터→단위 시술:U5-018,U5-037 |  |  |  |  | 구조 칸(combo) |  |
| R8-0331 | `problem-packages.complaints[].combos`[P7:서브시전#0] | 시너지(CC 조합) | 니들RF→단위 시술:U5-110 | 스킨부스터→단위 시술:U5-018,U5-037 |  |  |  |  | 구조 칸(combo) |  |
| R8-0332 | `problem-packages.complaints[].combos`[P8:V빔#0] | 시너지(CC 조합) | 혈관레이저→단위 시술:U5-099,U5-138 | 스킨부스터→단위 시술:U5-018,U5-037 |  |  |  |  | 구조 칸(combo) |  |
| R8-0333 | `problem-packages.complaints[].combos`[P8:IPL홍조#0] | 시너지(CC 조합) | 혈관레이저→단위 시술:U5-099,U5-138 | 스킨부스터→단위 시술:U5-018,U5-037 |  |  |  |  | 구조 칸(combo) |  |
| R8-0334 | `problem-packages.complaints[].combos`[P8:리쥬란+LDM#0] | 시너지(CC 조합) | 혈관레이저→단위 시술:U5-099,U5-138 | 스킨부스터→단위 시술:U5-018,U5-037 |  |  |  |  | 구조 칸(combo) |  |
| R8-0335 | `problem-packages.complaints[].combos`[P8:엑셀V#0] | 시너지(CC 조합) | 혈관레이저→단위 시술:U5-099,U5-138 | 스킨부스터→단위 시술:U5-018 |  |  |  |  | 구조 칸(combo) |  |
| R8-0336 | `problem-packages.complaints[].combos`[P8:혈관레이저#0] | 시너지(CC 조합) | 혈관레이저→단위 시술:U5-099,U5-138 | 스킨부스터→단위 시술:U5-018 |  |  |  |  | 구조 칸(combo) |  |
| R8-0337 | `problem-packages.complaints[].combos`[P9:서브시전#0] | 시너지(CC 조합) | 프락셔널→단위 시술:U5-027 | PRP→단위 시술:U5-020 |  |  |  |  | 구조 칸(combo) |  |
| R8-0338 | `problem-packages.complaints[].combos`[P9:서브시전#1] | 시너지(CC 조합) | 서브시전→단위 시술:U5-045 | 프락셔널→단위 시술:U5-027 |  |  |  |  | 구조 칸(combo) |  |
| R8-0339 | `problem-packages.complaints[].combos`[P9:서브시전#1] | 시너지(CC 조합) | 서브시전→단위 시술:U5-045 | PRP→단위 시술:U5-020 |  |  |  |  | 구조 칸(combo) |  |
| R8-0340 | `problem-packages.complaints[].combos`[P9:서브시전#1] | 시너지(CC 조합) | 프락셔널→단위 시술:U5-027 | PRP→단위 시술:U5-020 |  |  |  |  | 구조 칸(combo) |  |
| R8-0341 | `problem-packages.complaints[].combos`[P9:에어서브시전#0] | 시너지(CC 조합) | 프락셔널→단위 시술:U5-027 | PRP→단위 시술:U5-020 |  |  |  |  | 구조 칸(combo) |  |
| R8-0342 | `problem-packages.complaints[].combos`[P9:에어서브시전#1] | 시너지(CC 조합) | 서브시전→단위 시술:U5-045 | 프락셔널→단위 시술:U5-027 |  |  |  |  | 구조 칸(combo) |  |
| R8-0343 | `problem-packages.complaints[].combos`[P9:에어서브시전#1] | 시너지(CC 조합) | 서브시전→단위 시술:U5-045 | PRP→단위 시술:U5-020 |  |  |  |  | 구조 칸(combo) |  |
| R8-0344 | `problem-packages.complaints[].combos`[P9:에어서브시전#1] | 시너지(CC 조합) | 프락셔널→단위 시술:U5-027 | PRP→단위 시술:U5-020 |  |  |  |  | 구조 칸(combo) |  |
| R8-0345 | `problem-packages.complaints[].combos`[P9:TCA크로스#0] | 시너지(CC 조합) | 프락셔널→단위 시술:U5-027 | PRP→단위 시술:U5-020 |  |  |  |  | 구조 칸(combo) |  |
| R8-0346 | `problem-packages.complaints[].combos`[P9:TCA크로스#1] | 시너지(CC 조합) | 서브시전→단위 시술:U5-045 | 프락셔널→단위 시술:U5-027 |  |  |  |  | 구조 칸(combo) |  |
| R8-0347 | `problem-packages.complaints[].combos`[P9:TCA크로스#1] | 시너지(CC 조합) | 서브시전→단위 시술:U5-045 | PRP→단위 시술:U5-020 |  |  |  |  | 구조 칸(combo) |  |
| R8-0348 | `problem-packages.complaints[].combos`[P9:TCA크로스#1] | 시너지(CC 조합) | 프락셔널→단위 시술:U5-027 | PRP→단위 시술:U5-020 |  |  |  |  | 구조 칸(combo) |  |
| R8-0349 | `problem-packages.complaints[].combos`[P9:CO2프락셔널#0] | 시너지(CC 조합) | 프락셔널→단위 시술:U5-027 | PRP→단위 시술:U5-020 |  |  |  |  | 구조 칸(combo) |  |
| R8-0350 | `problem-packages.complaints[].combos`[P9:CO2프락셔널#1] | 시너지(CC 조합) | 서브시전→단위 시술:U5-045 | 프락셔널→단위 시술:U5-027 |  |  |  |  | 구조 칸(combo) |  |
| R8-0351 | `problem-packages.complaints[].combos`[P9:CO2프락셔널#1] | 시너지(CC 조합) | 서브시전→단위 시술:U5-045 | PRP→단위 시술:U5-020 |  |  |  |  | 구조 칸(combo) |  |
| R8-0352 | `problem-packages.complaints[].combos`[P9:CO2프락셔널#1] | 시너지(CC 조합) | 프락셔널→단위 시술:U5-027 | PRP→단위 시술:U5-020 |  |  |  |  | 구조 칸(combo) |  |
| R8-0353 | `problem-packages.complaints[].combos`[P9:니들RF#0] | 시너지(CC 조합) | 프락셔널→단위 시술:U5-027 | PRP→단위 시술:U5-020 |  |  |  |  | 구조 칸(combo) |  |
| R8-0354 | `problem-packages.complaints[].combos`[P9:니들RF#1] | 시너지(CC 조합) | 서브시전→단위 시술:U5-045 | 프락셔널→단위 시술:U5-027 |  |  |  |  | 구조 칸(combo) |  |
| R8-0355 | `problem-packages.complaints[].combos`[P9:니들RF#1] | 시너지(CC 조합) | 서브시전→단위 시술:U5-045 | PRP→단위 시술:U5-020 |  |  |  |  | 구조 칸(combo) |  |
| R8-0356 | `problem-packages.complaints[].combos`[P9:니들RF#1] | 시너지(CC 조합) | 프락셔널→단위 시술:U5-027 | PRP→단위 시술:U5-020 |  |  |  |  | 구조 칸(combo) |  |
| R8-0357 | `problem-packages.complaints[].combos`[P9:필러+서브시전#0] | 시너지(CC 조합) | 필러→계열:M2 | 보톡스→계열:M1 |  |  |  |  | 구조 칸(combo) |  |
| R8-0358 | `problem-packages.complaints[].combos`[P9:필러+서브시전#1] | 시너지(CC 조합) | 프락셔널→단위 시술:U5-027 | PRP→단위 시술:U5-020 |  |  |  |  | 구조 칸(combo) |  |
| R8-0359 | `problem-packages.complaints[].combos`[P9:필러+서브시전#2] | 시너지(CC 조합) | 서브시전→단위 시술:U5-045 | 프락셔널→단위 시술:U5-027 |  |  |  |  | 구조 칸(combo) |  |
| R8-0360 | `problem-packages.complaints[].combos`[P9:필러+서브시전#2] | 시너지(CC 조합) | 서브시전→단위 시술:U5-045 | PRP→단위 시술:U5-020 |  |  |  |  | 구조 칸(combo) |  |
| R8-0361 | `problem-packages.complaints[].combos`[P9:필러+서브시전#2] | 시너지(CC 조합) | 프락셔널→단위 시술:U5-027 | PRP→단위 시술:U5-020 |  |  |  |  | 구조 칸(combo) |  |
| R8-0362 | `problem-packages.complaints[].combos`[P9:스테로이드주사#0] | 시너지(CC 조합) | 병변내 스테로이드주사→단위 시술:U5-046 | 레이저→단위 시술:U5-141 |  |  |  |  | 구조 칸(combo) |  |
| R8-0363 | `problem-packages.complaints[].combos`[P9:레이저치료#0] | 시너지(CC 조합) | 병변내 스테로이드주사→단위 시술:U5-046 | 레이저→단위 시술:U5-141 |  |  |  |  | 구조 칸(combo) |  |
| R8-0364 | `problem-packages.complaints[].combos`[P9:프락셔널레이저#0] | 시너지(CC 조합) | 프락셔널→단위 시술:U5-027 | 스킨부스터→단위 시술:U5-018,U5-037 |  |  |  |  | 구조 칸(combo) |  |
| R8-0365 | `problem-packages.complaints[].combos`[P9:실리콘시트#0] | 시너지(CC 조합) | 프락셔널→단위 시술:U5-027 | 스킨부스터→단위 시술:U5-018,U5-037 |  |  |  |  | 구조 칸(combo) |  |
| R8-0366 | `problem-packages.complaints[].combos`[P9:프락셔널레이저#0] | 시너지(CC 조합) | 프락셔널→단위 시술:U5-027 | 스킨부스터→단위 시술:U5-018,U5-037 |  |  |  |  | 구조 칸(combo) |  |
| R8-0367 | `problem-packages.complaints[].combos`[P9:니들RF#0] | 시너지(CC 조합) | 프락셔널→단위 시술:U5-027 | 스킨부스터→단위 시술:U5-018,U5-037 |  |  |  |  | 구조 칸(combo) |  |
| R8-0368 | `problem-packages.complaints[].combos`[P10:겨드랑이/팔/다리#1] | 시너지(CC 조합) | 제모레이저→단위 시술:U5-100 | 보톡스→단위 시술:U5-010 |  |  |  |  | 구조 칸(combo) |  |
| R8-0369 | `problem-packages.complaints[].combos`[P11:사각턱보톡스#0] | 시너지(CC 조합) | 보톡스→단위 시술:U5-006 | 스킨부스터→단위 시술:U5-018,U5-037 |  |  |  |  | 구조 칸(combo) |  |
| R8-0370 | `problem-packages.complaints[].combos`[P11:사각턱보톡스#1] | 시너지(CC 조합) | 보톡스→단위 시술:U5-006 | 필러→계열:M2 |  |  |  |  | 구조 칸(combo) |  |
| R8-0371 | `problem-packages.complaints[].combos`[P11:윤곽주사#0] | 시너지(CC 조합) | 지방분해→단위 시술:U5-070 | 리프팅기기→단위 시술:U5-091,U5-102 |  |  |  |  | 구조 칸(combo) |  |
| R8-0372 | `problem-packages.complaints[].combos`[P11:브이올렛#0] | 시너지(CC 조합) | 지방분해→단위 시술:U5-070 | 리프팅기기→단위 시술:U5-091,U5-102 |  |  |  |  | 구조 칸(combo) |  |
| R8-0373 | `problem-packages.complaints[].combos`[P11:승모근보톡스#0] | 시너지(CC 조합) | 보톡스→단위 시술:U5-007 | 스킨부스터→계열:M4 |  |  |  |  | 구조 칸(combo) |  |
| R8-0374 | `problem-packages.complaints[].combos`[P11:볼볼륨충전#0] | 시너지(CC 조합) | 필러→단위 시술:U5-087,U5-089 | 바이오스티뮬레이터→단위 시술:U5-090 |  |  |  |  | 구조 칸(combo) |  |
| R8-0375 | `problem-packages.complaints[].combos`[P11:관자놀이충전#0] | 시너지(CC 조합) | 필러→단위 시술:U5-089 | 바이오스티뮬레이터→단위 시술:U5-090 |  |  |  |  | 구조 칸(combo) |  |
| R8-0376 | `problem-packages.complaints[].combos`[P12:쿨스컬프팅#0] | 시너지(CC 조합) | 크라이오→단위 시술:U5-116,U5-117,U5-119,U5-120 | 인모드→단위 시술:U5-152 |  |  |  |  | 구조 칸(combo) |  |
| R8-0377 | `problem-packages.complaints[].combos`[P12:지방분해주사(PPC/DC)#0] | 시너지(CC 조합) | 크라이오→단위 시술:U5-116,U5-117,U5-119,U5-120 | 인모드→단위 시술:U5-152 |  |  |  |  | 구조 칸(combo) |  |
| R8-0378 | `problem-packages.complaints[].combos`[P12:HPL주사#0] | 시너지(CC 조합) | 크라이오→단위 시술:U5-116,U5-117,U5-119,U5-120 | 인모드→단위 시술:U5-152 |  |  |  |  | 구조 칸(combo) |  |
| R8-0379 | `problem-packages.complaints[].combos`[P12:BNLS주사#0] | 시너지(CC 조합) | 크라이오→단위 시술:U5-116,U5-117,U5-119,U5-120 | 인모드→단위 시술:U5-152 |  |  |  |  | 구조 칸(combo) |  |
| R8-0380 | `problem-packages.complaints[].combos`[P12:브이올렛#0] | 시너지(CC 조합) | 크라이오→단위 시술:U5-116,U5-117,U5-119,U5-120 | 인모드→단위 시술:U5-152 |  |  |  |  | 구조 칸(combo) |  |
| R8-0381 | `problem-packages.complaints[].combos`[P12:컷슬린#0] | 시너지(CC 조합) | 크라이오→단위 시술:U5-116,U5-117,U5-119,U5-120 | 인모드→단위 시술:U5-152 |  |  |  |  | 구조 칸(combo) |  |
| R8-0382 | `problem-packages.complaints[].combos`[P12:바디HIFU#0] | 시너지(CC 조합) | 크라이오→단위 시술:U5-116,U5-117,U5-119,U5-120 | 인모드→단위 시술:U5-152 |  |  |  |  | 구조 칸(combo) |  |
| R8-0383 | `problem-packages.complaints[].combos`[P12:엔더몰로지#0] | 시너지(CC 조합) | 인모드→단위 시술:U5-152 | HIFES→단위 시술:U5-105,U5-106,U5-108,U5-109 |  |  |  |  | 구조 칸(combo) |  |
| R8-0384 | `problem-packages.complaints[].combos`[P13:두피메조#0] | 시너지(CC 조합) | PRP→단위 시술:U5-042 | MTS→단위 시술:U5-112 |  |  |  |  | 구조 칸(combo) |  |
| R8-0385 | `problem-packages.complaints[].combos`[P13:두피PRP#0] | 시너지(CC 조합) | PRP→단위 시술:U5-042 | MTS→단위 시술:U5-112 |  |  |  |  | 구조 칸(combo) |  |
| R8-0386 | `problem-packages.complaints[].combos`[P13:두피엑소좀#0] | 시너지(CC 조합) | PRP→단위 시술:U5-042 | MTS→단위 시술:U5-112 |  |  |  |  | 구조 칸(combo) |  |
| R8-0387 | `problem-packages.complaints[].combos`[P13:LLLT#0] | 시너지(CC 조합) | 레이저→단위 시술:U5-039,U5-043 | MTS→단위 시술:U5-112 |  |  |  |  | 구조 칸(combo) |  |
| R8-0388 | `problem-packages.complaints[].combos`[P13:두피스케일링#0] | 시너지(CC 조합) | 레이저→단위 시술:U5-039,U5-043 | MTS→단위 시술:U5-112 |  |  |  |  | 구조 칸(combo) |  |
| R8-0389 | `problem-packages.complaints[].combos`[P13:MTS두피#0] | 시너지(CC 조합) | 레이저→단위 시술:U5-039,U5-043 | MTS→단위 시술:U5-112 |  |  |  |  | 구조 칸(combo) |  |
| R8-0390 | `problem-packages.complaints[].combos`[P13:미녹시딜#0] | 시너지(CC 조합) | 약물치료→계열:M15 | PRP→단위 시술:U5-042 |  |  |  |  | 구조 칸(combo) |  |
| R8-0391 | `problem-packages.complaints[].combos`[P13:피나스테리드#0] | 시너지(CC 조합) | 약물치료→계열:M15 | PRP→단위 시술:U5-042 |  |  |  |  | 구조 칸(combo) |  |
| R8-0392 | `problem-packages.complaints[].combos`[P13:두타스테리드#0] | 시너지(CC 조합) | 약물치료→계열:M15 | PRP→단위 시술:U5-042 |  |  |  |  | 구조 칸(combo) |  |
| R8-0393 | `problem-packages.complaints[].combos`[P13:FUE#0] | 시너지(CC 조합) | 모발이식→단위 시술:U5-161 | PRP→단위 시술:U5-042 |  |  |  |  | 구조 칸(combo) |  |
| R8-0394 | `problem-packages.complaints[].combos`[P13:FUT#0] | 시너지(CC 조합) | 모발이식→단위 시술:U5-161 | PRP→단위 시술:U5-042 |  |  |  |  | 구조 칸(combo) |  |
| R8-0395 | `taxonomy.modality[].products[].extracted.safety.contraindications`[M7-P-2#0] | 조합 금기 | PDO→하위 계열:M7 | 비가교HA→하위 계열:U5-018,U5-037,U5-041 |  | [1.0, 3.0]+ |  |  | S-PLUSFORBID | 보수적 선택 |

## 충돌(원문 쪽별 · 처분은 위 「충돌 하나로」)

| id | 쌍 | 종류 | 쪽별 | 처분 |
|---|---|---|---|---|
| X8-001 | M1 ↔ M2 | 순서(먼저 하는 쪽) | M1: R8-0001, R8-0153, R8-0164, R8-0185, R8-0187, R8-0242, R8-0255 / M2: R8-0163, R8-0179 | 의료진 확인 |
| X8-002 | M1 ↔ M2 | 같은 날 가능 ↔ 불가 | 가능: R8-0001, R8-0028, R8-0032, R8-0058, R8-0062, R8-0163, R8-0179 / 불가: R8-0164 | 조건 분리(가짜 충돌) |
| X8-003 | M1 ↔ M9 | 순서(먼저 하는 쪽) | M1: R8-0031, R8-0158, R8-0171 / M9: R8-0121, R8-0125, R8-0131, R8-0138, R8-0156, R8-0157, R8-0169, R8-0170, R8-0186, R8-0191, R8-0240, R8-0241, R8-0254 / 묶음 M9: R8-0239 | 의료진 확인 |
| X8-004 | M11 ↔ M15 | 순서(먼저 하는 쪽) | M11: R8-0039 / M15: R8-0050 | 의료진 확인 |
| X8-005 | M11 ↔ M5 | 순서(먼저 하는 쪽) | M11: R8-0219, R8-0249 / M5: R8-0206 / 묶음 M11: R8-0239 | 의료진 확인 |
| X8-006 | M11 ↔ M8 | 순서(먼저 하는 쪽) | M11: R8-0251 / M8: R8-0248 | 의료진 확인 |
| X8-007 | M12 ↔ M8 | 간격 수치 | R8-0023: 2주 간격 권장 / R8-0103: 프락셔널 4주 후 MTS | 보수적 선택 |
| X8-008 | M15 ↔ M8 | 순서(먼저 하는 쪽) | M15: R8-0151, R8-0217 / M8: R8-0180, R8-0201, R8-0216 | 의료진 확인 |
| X8-009 | M15 ↔ M8 | 같은 날 가능 ↔ 불가 | 가능: R8-0111, R8-0201 / 불가: R8-0144, R8-0226 | 조건 분리(가짜 충돌) |
| X8-010 | M2 ↔ M8 | 순서(먼저 하는 쪽) | M2: R8-0150, R8-0168 / M8: R8-0152, R8-0162, R8-0178, R8-0204, R8-0208, R8-0223 / 묶음 M8: R8-0239 | 의료진 확인 |
| X8-011 | M2 ↔ M8 | 같은 날 가능 ↔ 불가 | 가능: R8-0119 / 불가: R8-0143, R8-0147, R8-0178, R8-0204, R8-0208, R8-0223 | 보수적 선택 |
| X8-012 | M2 ↔ M9 | 순서(먼저 하는 쪽) | M2: R8-0061, R8-0146, R8-0149, R8-0165, R8-0167, R8-0172, R8-0177, R8-0189 / M9: R8-0154, R8-0166, R8-0173 / 묶음 M9: R8-0239 | 의료진 확인 |
| X8-013 | M2 ↔ M9 | 같은 날 가능 ↔ 불가 | 가능: R8-0154, R8-0166 / 불가: R8-0146 | 조건 분리(가짜 충돌) |
| X8-014 | M3 ↔ M4 | 순서(먼저 하는 쪽) | M3: R8-0067, R8-0070, R8-0073 / M4: R8-0197 | 의료진 확인 |
| X8-015 | M4 ↔ M8 | 순서(먼저 하는 쪽) | M4: R8-0077, R8-0084 / M8: R8-0014, R8-0105, R8-0108, R8-0110, R8-0112, R8-0116, R8-0120, R8-0182, R8-0203, R8-0212, R8-0237 / 묶음 M8: R8-0239 | 의료진 확인 |
| X8-016 | M4 ↔ M8 | 간격 수치 | R8-0014: 1주 간격 권장 / R8-0105: 프락셔널 2주 후 스킨부스터 / R8-0108: 피코토닝 2주 후 리쥬란 / R8-0110: 피코토닝 1~2주 후 스킨부스터 / R8-0112: 혈관레이저 2주 후 스킨부스터 / R8-0116: CO2 2주 후 스킨부스터 / R8-0120: IPL 2주 후 스킨부스터 / R8-0182: 2주 후 | 보수적 선택 |
| X8-017 | M4 ↔ M9 | 순서(먼저 하는 쪽) | M4: R8-0085 / M9: R8-0122, R8-0126, R8-0132, R8-0139, R8-0142, R8-0190 / 묶음 M9: R8-0239 | 의료진 확인 |
| X8-018 | M5 ↔ M8 | 순서(먼저 하는 쪽) | M5: R8-0090 / M8: R8-0205, R8-0219, R8-0221, R8-0238, R8-0252 / 묶음 M8: R8-0239 | 의료진 확인 |
| X8-019 | M7 ↔ M9 | 순서(먼저 하는 쪽) | M7: R8-0098, R8-0099, R8-0244, R8-0258, R8-0264 / M9: R8-0133, R8-0193 | 의료진 확인 |
| X8-020 | M3 ↔ M9 | 순서(먼저 하는 쪽) | M3: R8-0065, R8-0071, R8-0072 / M9: R8-0239 | 의료진 확인 |
| X8-021 | M6 ↔ M9 | 순서(먼저 하는 쪽) | M6: R8-0200 / M9: R8-0239 | 의료진 확인 |
| X8-022 | M9 ↔ N1 | 순서(먼저 하는 쪽) | M9: R8-0239 / N1: R8-0228, R8-0230 | 의료진 확인 |

## 피함(고민 조건 금기 · U8-2)

| id | 고민(7단계) | → 시술 | 수식 | 범위 | 원문 | 근거 |
|---|---|---|---|---|---|---|
| AV8-001 | P5-1 | 레이저→계열:M8 | 고출력 | 조건부 — 단위 시술 미특정 | 기미 환자에 고출력 레이저 시 반동 색소침착(PIH) 위험. 저출력 토닝만 권장. | 원문 고민 낱말 「기미」 → 7단계 P5-1 |
| AV8-002 | P5-1 | 레이저→계열:M8 | 고에너지 | 조건부 — 단위 시술 미특정 | 기미에 고에너지 레이저 금지(PIH 위험) | 원문 고민 낱말 「기미」 → 7단계 P5-1 |
| AV8-003 | P5-1 | IPL→단위 시술:U5-030 | 단독·고출력 | 기본 적용 | 기미에 IPL 단독·고출력 금지 — 저출력·병용 보조로만, 반동 색소·PIH 위험(Fitzpatrick IV~VI 고위험), 시험 조사(test spot)·엄격한 광차단 선행 | 원문 고민 낱말 「기미」 → 7단계 P5-1 |
| AV8-004 | P5-1 | 레이저→계열:M8 | 고출력 | 조건부 — 단위 시술 미특정 | 고출력 레이저 금지(반동 색소침착) | 중증도 이름 낱말 「기미」 → 7단계 P5-1 |
| AV8-005 | P5-1 | IPL→단위 시술:U5-030 | 단독 | 기본 적용 | 기미에 IPL 단독 금지 | 원문 고민 낱말 「기미」 → 7단계 P5-1 |

## 확인 조건 노드

| id | 이름 | 주장 | 원천 |
|---|---|---|---|
| C-PREG | 임신 | 37 | consent-checklist · pre-procedure-checklist · taxonomy |
| C-BF | 수유 | 30 | consent-checklist · pre-procedure-checklist · taxonomy |
| C-KEL | 켈로이드 체질 | 22 | consent-checklist · pre-procedure-checklist · taxonomy |
| C-ANTICOAG | 항응고제 · 항혈소판제 | 21 | consent-checklist · pre-procedure-checklist · taxonomy |
| C-NSAID | NSAIDs | 3 | consent-checklist · pre-procedure-checklist |
| C-ISO | 이소트레티노인 | 18 | consent-checklist · pre-procedure-checklist · taxonomy · treatment-sequence |
| C-RETIN | 레티노이드 처방 | 3 | consent-checklist · pre-procedure-checklist |
| C-HSV | 헤르페스 병력 | 4 | pre-procedure-checklist |
| C-AUTO | 자가면역질환 | 15 | consent-checklist · pre-procedure-checklist · taxonomy |
| C-METAL | 체내 금속 · 금속 임플란트 | 15 | consent-checklist · pre-procedure-checklist · taxonomy |
| C-PACE | 심장박동기 · 이식형 전자장치 | 12 | consent-checklist · pre-procedure-checklist · taxonomy |
| C-ALLERGY | 알레르기 · 과민반응 병력 | 24 | consent-checklist · pre-procedure-checklist · taxonomy |
| C-INFECT | 시술 부위 감염 · 염증 | 43 | consent-checklist · pre-procedure-checklist · taxonomy |
| C-ACNE | 활동성 여드름 | 9 | consent-checklist · pre-procedure-checklist · taxonomy · treatment-optimization |
| C-DERM | 시술 부위 피부질환 · 피부 상태(피부염 · 습진 · 건선 · 로사세아) | 10 | consent-checklist · pre-procedure-checklist · taxonomy |
| C-NMJ | 신경근 질환 | 6 | consent-checklist · pre-procedure-checklist · taxonomy |
| C-EPI | 간질 · 경련성 질환 | 5 | consent-checklist · pre-procedure-checklist · taxonomy |
| C-NEURO | 신경계 질환 | 1 | pre-procedure-checklist |
| C-BLEED | 출혈 경향 · 응고장애 · 혈액질환 | 14 | consent-checklist · pre-procedure-checklist · taxonomy |
| C-DM | 당뇨 · 면역저하 · 면역억제 | 13 | consent-checklist · pre-procedure-checklist · taxonomy |
| C-CANCER | 악성종양 · 암 병력 | 6 | consent-checklist · pre-procedure-checklist · taxonomy |
| C-CHF | 심부전 · 신장 질환 | 8 | consent-checklist · pre-procedure-checklist · taxonomy |
| C-G6PD | G6PD 결핍증 | 3 | consent-checklist · pre-procedure-checklist · taxonomy |
| C-COLD | 한냉 질환(한냉두드러기 · 한냉글로불린 · 한냉혈색소뇨 · 레이노) | 11 | consent-checklist · pre-procedure-checklist · taxonomy |
| C-PHOTO | 광과민성 질환 · 약물 | 5 | consent-checklist · pre-procedure-checklist · taxonomy |
| C-SUN | 일광노출 · 태닝 · 자외선 차단 불가 | 5 | consent-checklist · pre-procedure-checklist · taxonomy · treatment-optimization |
| C-AMINO | 아미노글리코시드 항생제 | 3 | consent-checklist · pre-procedure-checklist · taxonomy |
| C-DPEN | D-페니실라민 | 1 | pre-procedure-checklist |
| C-MUSCLE | 근이완제 등 특정 약물 | 1 | taxonomy |
| C-LIDO | 마취제 알레르기(리도카인) | 1 | pre-procedure-checklist |
| C-HYAL | 히알루로니다아제 알레르기 | 1 | pre-procedure-checklist |
| C-PRIOR | 최근 · 이전 시술 이력 | 17 | consent-checklist · pre-procedure-checklist · taxonomy |
| C-RESID | 잔여 필러 · 실 · 영구필러 | 4 | pre-procedure-checklist |
| C-DENTAL | 최근 치과 시술 | 1 | pre-procedure-checklist |
| C-FLIGHT | 48시간 이내 비행 | 1 | pre-procedure-checklist |
| C-CHRONINF | 만성감염(피부결핵 · 매독) | 1 | pre-procedure-checklist |
| C-FITZ | Fitzpatrick 피부타입 · 어두운 피부 · PIH 위험 | 5 | consent-checklist · pre-procedure-checklist · taxonomy |
| C-SURG | 최근 수술 · 흉터(시술 부위) | 5 | consent-checklist · pre-procedure-checklist · taxonomy |
| C-HERNIA | 탈장 | 4 | consent-checklist · pre-procedure-checklist · taxonomy |
| C-BMI | 체형 · 피하지방 두께 · 저체중 | 6 | consent-checklist · pre-procedure-checklist · taxonomy |
| C-LIVER | 간기능 · 지질 수치(레티노이드 처방) | 3 | pre-procedure-checklist |
| C-SKINCARE | 사용 중 스킨케어 제품 | 1 | pre-procedure-checklist |
| C-PEELALG | 필링 제제 알레르기 | 1 | pre-procedure-checklist |
| C-VASC | 혈관 접근 상태 | 1 | pre-procedure-checklist |
| C-SUPPL | 복용 영양제 · 약물 상호작용 | 6 | pre-procedure-checklist · taxonomy |
| C-SMOKE | 흡연 | 2 | consent-checklist · taxonomy |
| C-GRAN | 이물반응 · 육아종 병력 | 1 | consent-checklist |
| C-CARDIO | 심혈관 질환(허혈성 심질환 · 고혈압) | 2 | taxonomy |
| C-RADIO | 방사선 치료 중 | 1 | taxonomy |
| C-HORMONE | 경구 피임약 · 에스트로겐 | 1 | taxonomy |
| C-INDIC | 적응 범위 밖(수술적 교정 필요) | 1 | consent-checklist |
| C-EXPECT | 비현실적 기대 | 2 | taxonomy |
| C-AGE | 연령대 | 6 | treatment-optimization |

등급 충돌 76(전부 R2 더 엄격 — conditions.resolved) · 대기 기간 충돌(R6 — conditions.wait_resolved) XW-C-ISO consent-checklist.contraindications: [6, 12] / pre-procedure-checklist.category_specific: [6, 12] / pre-procedure-checklist.universal_checks: [6, 12] / taxonomy.modality[].extracted.contraindications.relative: [6] / treatment-sequence.incompatible_same_day: [0, 2, 6] / treatment-sequence.minimum_intervals: [0, 2, 6]

## 안전

합병증 35 · 원천 없는 계열(gap — 「없음 = 안전」 아님) M10, M13, N1, N10, N2, N3, N4, N5, N6, N7, N8, N9 · 같은 이름 여러 계열 {'PIH (시술 후 과색소침착)': 2, '감염': 3}

부작용 72(계열 속성 — U2 · B1 — 부작용(흔한 예상 반응) = 계열 속성 safety.side_effects · 합병증 노드 = complications.json severity moderate 이상만. 제품 × 계열 · 단위 시술에 값(5단계 extracted safety.common)이 있으면 그 값이 계열 값을 덮어씀 — 덮어쓰기는 골드 계산(B7 · 저장 안 함)) · 부작용 없는 계열 N1, N10, N2, N3, N4, N5, N6, N7, N8, N9

| 부작용 | 계열 | 이름 | 원천 등급 | 의료진 질문 |
|---|---|---|---|---|
| SE-M1-01 | M1 | 주사 부위 통증 | 경미 |  |
| SE-M1-02 | M1 | 멍 (타박상) | 경미 | Q8-19 |
| SE-M1-03 | M1 | 주사 부위 홍반·부종 | 경미 |  |
| SE-M1-04 | M1 | 두통 | 경미 | Q8-19 |
| SE-M1-06 | M1 | 독감 유사 증상 | 경미 | Q8-19 |
| SE-M1-07 | M1 | 안면 비대칭 | 경미 | Q8-19 |
| SE-M2-01 | M2 | 멍 / 반상출혈 (Bruising / Ecchymosis) | 경미 | Q8-19 |
| SE-M2-02 | M2 | 부종 / 종창 (Swelling / Edema) | 경미 |  |
| SE-M2-03 | M2 | 주사 통증 / 불편감 (Injection Pain / Discomfort) | 경미 |  |
| SE-M2-04 | M2 | 홍반 (Erythema / Redness) | 경미 |  |
| SE-M2-07 | M2 | 비대칭 (Asymmetry) | 경미 | Q8-19 |
| SE-M3-05 | M3 | 주사 부위 반응 (부종·압통·멍·홍반) | 경미 |  |
| SE-M7-04 | M7 | 비대칭 | 경미 | Q8-19 |
| SE-M7-06 | M7 | 피부 딤플링/주름짐 (Skin Dimpling/Puckering) | 경미 | Q8-19 |
| SE-M7-07 | M7 | 통증·당김감 (Pain / Tightness) | 경미 |  |
| SE-M7-08 | M7 | 부종·멍(혈종) (Edema / Bruising / Hematoma) | 경미 |  |
| SE-M8-02 | M8 | 홍반 (Erythema) | 경미 |  |
| SE-M8-03 | M8 | 부종 (Edema) | 경미 |  |
| SE-M9-02 | M9 | 홍반 (시술 직후 빨개짐) | 경미 |  |
| SE-M9-03 | M9 | 부종 (붓기) | 경미 |  |
| SE-M9-04 | M9 | 통증·열감 (시술 중/후) | 경미 |  |
| SE-M9-05 | M9 | 일시적 감각이상 (따끔거림·저림·감각둔화) | 경미 |  |
| SE-M11-05 | M11 | 일시적 홍반·부종 (Transient Erythema/Edema) | 경미 |  |
| SE-M14-03 | M14 | 일시적 감각저하·저림 (Transient Hypoesthesia / Paresthesia) | 경미 |  |
| SE-M14-04 | M14 | 일시적 홍반·부종 (Erythema / Edema) | 경미 |  |
| SE-M14-05 | M14 | 멍·타박상 (Bruising) | 경미 |  |
| SE-M14-07 | M14 | 염증후 색소침착 (Post-inflammatory Hyperpigmentation, PIH) | 경미 | Q8-19 |
| SE-M15-01 | M15 | 일시적 홍반 (Transient erythema) | 경미 |  |
| SE-M15-02 | M15 | 자극감·작열감 (Stinging/burning) | 경미 |  |
| SE-M15-03 | M15 | 건조·낙설(각질 박리) (Dryness/desquamation) | 경미 |  |
| SE-M15-04 | M15 | 소양감 (Pruritus) | 경미 |  |
| SE-M16-01 | M16 | 부종·종창 | 경미 |  |
| SE-M16-02 | M16 | 통증·압통 | 경미 |  |
| SE-M16-03 | M16 | 멍·혈종 | 경미 |  |
| SE-M16-04 | M16 | 감각이상·저림 (표재 감각신경, 가역적) | 경미 |  |
| SE-M16-05 | M16 | 경결·딱딱함(일시적 섬유화) | 경미 |  |
| SE-M16-06 | M16 | 홍반·발적·가려움 | 경미 |  |
| SE-M16-07 | M16 | 주사부위 반응 (통증·발적·멍·경결) | 경미 |  |
| SE-M4-C01 | M4 | 주사 부위 통증 | 원문 common(taxonomy) |  |
| SE-M4-C02 | M4 | 일시적 홍반 (빨개짐) | 원문 common(taxonomy) |  |
| SE-M4-C03 | M4 | 약간의 붓기 | 원문 common(taxonomy) |  |
| SE-M4-C04 | M4 | 멍 | 원문 common(taxonomy) |  |
| SE-M4-U01 | M4 | 알레르기 반응 | 원문 uncommon(taxonomy) |  |
| SE-M4-U02 | M4 | 혈종 (피가 고이는 것) | 원문 uncommon(taxonomy) |  |
| SE-M4-U03 | M4 | 피부색소침착 (시술 부위가 어두워지는 현상) | 원문 uncommon(taxonomy) |  |
| SE-M5-C01 | M5 | 주사 부위 통증 | 원문 common(taxonomy) |  |
| SE-M5-C02 | M5 | 1~2일 정도 붓기 | 원문 common(taxonomy) |  |
| SE-M5-C03 | M5 | 3~7일 정도 멍이 들 수 있음 | 원문 common(taxonomy) |  |
| SE-M5-U01 | M5 | 피부 재생 정도가 사람마다 달라 시술 결과에 차이가 있을 수 있음 | 원문 uncommon(taxonomy) |  |
| SE-M6-C01 | M6 | 채취 부위 및 주입 부위의 멍과 붓기 | 원문 common(taxonomy) |  |
| SE-M6-C02 | M6 | 주입 부위 통증 및 불편감 | 원문 common(taxonomy) |  |
| SE-M6-C03 | M6 | 초기 과교정 (붓기로 인해 볼륨이 과하게 보이는 것) | 원문 common(taxonomy) |  |
| SE-M6-U01 | M6 | 주입된 지방의 불균일한 생착 (울퉁불퉁해지는 것) | 원문 uncommon(taxonomy) |  |
| SE-M6-U02 | M6 | 석회화 (지방이 딱딱하게 굳는 것) | 원문 uncommon(taxonomy) |  |
| SE-M6-U03 | M6 | 지방 낭종 (기름 주머니 형성) | 원문 uncommon(taxonomy) |  |
| SE-M10-C01 | M10 | 시술 부위 근육통 (운동 후와 비슷한 느낌) | 원문 common(taxonomy) |  |
| SE-M10-C02 | M10 | 일시적 근육 경련 | 원문 common(taxonomy) |  |
| SE-M10-C03 | M10 | 시술 중 약간의 불편감 | 원문 common(taxonomy) |  |
| SE-M10-U01 | M10 | 시술 부위 피부 발적 (빨개짐) | 원문 uncommon(taxonomy) |  |
| SE-M10-U02 | M10 | 일시적 관절/건 불편감 | 원문 uncommon(taxonomy) |  |
| SE-M12-C01 | M12 | 시술 중 약간의 출혈과 진물 | 원문 common(taxonomy) |  |
| SE-M12-C02 | M12 | 시술 후 피부가 빨개지고 약간 부을 수 있음 (1~2일 내 호전) | 원문 common(taxonomy) |  |
| SE-M12-C03 | M12 | 출혈에 의해 일시적으로 멍이 들 수 있음 | 원문 common(taxonomy) |  |
| SE-M12-U01 | M12 | 감염 (무균 관리가 안 될 경우) | 원문 uncommon(taxonomy) |  |
| SE-M12-U02 | M12 | 색소침착 (특히 진피까지 깊이 치료한 경우) | 원문 uncommon(taxonomy) |  |
| SE-M12-U03 | M12 | 알레르기성 접촉피부염 (도포 약물에 의한 반응) | 원문 uncommon(taxonomy) |  |
| SE-M13-C01 | M13 | 시술 중 약간의 따끔거림 | 원문 common(taxonomy) |  |
| SE-M13-C02 | M13 | 일시적 홍반 (빨개짐) | 원문 common(taxonomy) |  |
| SE-M13-U01 | M13 | 피부 건조감 | 원문 uncommon(taxonomy) |  |
| SE-M17-C01 | M17 | 지방흡입 부위의 일시적 통증과 멍 | 원문 common(taxonomy) |  |
| SE-M17-C02 | M17 | 이식 부위의 약간의 부종 | 원문 common(taxonomy) |  |
| SE-M17-U01 | M17 | 이식된 세포가 시간이 지나면서 일부 흡수되어 효과가 줄어들 수 있음 | 원문 uncommon(taxonomy) |  |

| site_caution | 부위 | 위험도 | 그 부위 단위 시술 |
|---|---|---|---|
| SC-forehead-M1 | 이마 | 4 | 1 |
| SC-forehead-M2 | 이마 | 4 | 1 |
| SC-glabella-M1 | 미간 | 5 | 1 |
| SC-glabella-M2 | 미간 | 5 | 0 |
| SC-temple-M1 | 관자놀이 | 4 | 0 |
| SC-temple-M2 | 관자놀이 | 4 | 1 |
| SC-periorbital-M1 | 눈가(묶음) | 5 | 1 |
| SC-periorbital-M2 | 눈가(묶음) | 5 | 1 |
| SC-nose-M1 | 코(묶음) | 5 | 2 |
| SC-nose-M2 | 코(묶음) | 5 | 1 |
| SC-nasolabial-M1 | 팔자 | 4 | 0 |
| SC-nasolabial-M2 | 팔자 | 4 | 1 |
| SC-cheek-M1 | 볼(묶음) | 3 | 0 |
| SC-cheek-M2 | 볼(묶음) | 3 | 1 |
| SC-lips-M1 | 입술 | 3 | 0 |
| SC-lips-M2 | 입술 | 3 | 1 |
| SC-chin-M1 | 턱끝 | 3 | 1 |
| SC-chin-M2 | 턱끝 | 3 | 1 |
| SC-jawline-M1 | 턱선 | 4 | 1 |
| SC-jawline-M2 | 턱선 | 4 | 0 |
| SC-neck-M1 | 목(묶음) | 2 | 2 |
| SC-neck-M2 | 목(묶음) | 2 | 0 |

| 경과표 | 붙는 곳 | 단위 시술 |
|---|---|---|
| botox | family:M1 |  |
| ha-filler | family:M2 |  |
| hifu-rf | family:M9 | U5-091,U5-102,U5-103,U5-104,U5-152,U5-154 |
| fractional-co2 | unit:U5-028 | U5-028 |
| thread-lift | family:M7 |  |
| dca-injection | family:N1 |  |
| needle-rf | family:M11 |  |
| skin-booster | family:M4 |  |
| biostimulator | family:M3 |  |
| chemical-peel-mid | family:M15 | U5-034 |

## 7단계 메모 대조

| 7단계 메모 원천 | 메모 | 원천 행 | 주장 | 속성 | 조건 | 피함 |
|---|---|---|---|---|---|---|
| `combo-recipes.followUp` | 28 | 28 | 0 | 28 | 0 | 0 |
| `problem-combos.riskBenefit` | 13 | 24 | 17 | 0 | 0 | 0 |
| `problem-packages.complaints[].alternatives` | 6 | 6 | 2 | 4 | 0 | 0 |
| `problem-packages.complaints[].combos` | 146 | 146 | 137 | 21 | 0 | 0 |
| `treatment-optimization.combination_rules` | 8 | 8 | 13 | 1 | 0 | 1 |
| `treatment-optimization.contraindicated_combos` | 17 | 17 | 10 | 0 | 3 | 4 |
| `treatment-optimization.sequence` | 24 | 24 | 42 | 2 | 0 | 0 |
| `treatment-sequence.common_combos.note` | 3 | 3 | 5 | 0 | 0 | 0 |

## 전수 — source-map 8단계 칸

| 원천 · 칸 | 지도 값 수 | 지금 | 반영 |
|---|---|---|---|
| `anatomy-danger-zones` consensus_method | 1 | 1 | evidence.evidence_kind_by_file |
| `anatomy-danger-zones` critical_safety_facts.minimum_filler_for_blindness | 1 | 1 | safety.critical_safety_facts |
| `anatomy-danger-zones` critical_safety_facts.blindness_highest_risk_zones | 1 | 1 | safety.critical_safety_facts |
| `anatomy-danger-zones` critical_safety_facts.mechanism | 1 | 1 | safety.critical_safety_facts |
| `anatomy-danger-zones` critical_safety_facts.caveat | 1 | 1 | safety.critical_safety_facts |
| `anatomy-danger-zones` zones[].danger_level | 11 | 11 | safety.site_caution |
| `anatomy-danger-zones` zones[].vessels[].name | 24 | 24 | safety.site_caution |
| `anatomy-danger-zones` zones[].vessels[].depth_mm | 22 | 22 | safety.site_caution |
| `anatomy-danger-zones` zones[].vessels[].diameter_mm | 24 | 24 | safety.site_caution |
| `anatomy-danger-zones` zones[].vessels[].course | 24 | 24 | safety.site_caution |
| `anatomy-danger-zones` zones[].vessels[].danger | 24 | 24 | safety.site_caution |
| `anatomy-danger-zones` zones[].vessels[].note | 2 | 2 | safety.site_caution |
| `anatomy-danger-zones` zones[].vessels[].depth_range_mm | 5 | 5 | safety.site_caution |
| `anatomy-danger-zones` zones[].nerves[].name | 21 | 21 | safety.site_caution |
| `anatomy-danger-zones` zones[].nerves[].type | 21 | 21 | safety.site_caution |
| `anatomy-danger-zones` zones[].nerves[].significance | 21 | 21 | safety.site_caution |
| `anatomy-danger-zones` zones[].clinical_pearls | 11 | 11 | safety.site_caution |
| `anatomy-danger-zones` zones[].botox_specific.risk | 11 | 11 | safety.site_caution |
| `anatomy-danger-zones` zones[].botox_specific.safe_zone | 11 | 11 | safety.site_caution |
| `anatomy-danger-zones` zones[].botox_specific.diffusion_range_cm | 1 | 1 | safety.site_caution |
| `anatomy-danger-zones` zones[].botox_specific.key_warning | 11 | 11 | safety.site_caution |
| `anatomy-danger-zones` zones[].filler_specific.risk_level | 11 | 11 | safety.site_caution |
| `anatomy-danger-zones` zones[].filler_specific.primary_risk | 11 | 11 | safety.site_caution |
| `anatomy-danger-zones` zones[].filler_specific.safe_technique | 11 | 11 | safety.site_caution |
| `anatomy-danger-zones` zones[].filler_specific.max_per_point_ml | 11 | 11 | safety.site_caution |
| `anatomy-danger-zones` zones[].filler_specific.preferred_product | 11 | 11 | safety.site_caution |
| `anatomy-danger-zones` zones[].filler_specific.emergency_protocol | 3 | 3 | safety.site_caution |
| `anatomy-danger-zones` zones[].tissue_data.pitanguy_line | 1 | 1 | safety.site_caution |
| `anatomy-danger-zones` zones[].tissue_data.facial_artery_distance_to_nlf_mm | 1 | 1 | safety.site_caution |
| `anatomy-danger-zones` zones[].tissue_data.asian_adjacent_distribution_percent | 1 | 1 | safety.site_caution |
| `anatomy-danger-zones` zones[].tissue_data.within_5mm_percent | 1 | 1 | safety.site_caution |
| `anatomy-danger-zones` zones[].tissue_data.facial_artery_diameter_mandible_mm | 1 | 1 | safety.site_caution |
| `anatomy-danger-zones` zones[].tissue_data.facial_artery_diameter_nasal_mm | 1 | 1 | safety.site_caution |
| `anatomy-danger-zones` zones[].tissue_data.labial_artery_depth_range_mm | 1 | 1 | safety.site_caution |
| `anatomy-danger-zones` zones[].tissue_data.superior_labial_artery_submucosal_percent | 1 | 1 | safety.site_caution |
| `anatomy-danger-zones` zones[].tissue_data.mental_foramen_location | 1 | 1 | safety.site_caution |
| `anatomy-danger-zones` zones[].tissue_data.marginal_mandibular_depth | 1 | 1 | safety.site_caution |
| `anatomy-danger-zones` zones[].tissue_data.facial_artery_crossing | 1 | 1 | safety.site_caution |
| `complications` categories[].id | 10 | 10 | safety.complications · evidence.web |
| `complications` categories[].name | 10 | 10 | safety.complications · evidence.web |
| `complications` categories[].complications[].name | 65 | 65 | safety.complications · evidence.web |
| `complications` categories[].complications[].severity | 65 | 65 | safety.complications · evidence.web |
| `complications` categories[].complications[].incidence | 65 | 65 | safety.complications · evidence.web |
| `complications` categories[].complications[].onset | 65 | 65 | safety.complications · evidence.web |
| `complications` categories[].complications[].mechanism | 65 | 65 | safety.complications · evidence.web |
| `complications` categories[].complications[].risk_factors | 65 | 65 | safety.complications · evidence.web |
| `complications` categories[].complications[].management | 65 | 65 | safety.complications · evidence.web |
| `complications` categories[].complications[].prevention | 65 | 65 | safety.complications · evidence.web |
| `complications` categories[].complications[].evidence | 38 | 38 | safety.complications · evidence.web |
| `complications` categories[].complications[].duration | 19 | 19 | safety.complications · evidence.web |
| `consent-checklist` categories[].id | 17 | 17 | safety.family_text |
| `consent-checklist` categories[].name | 17 | 17 | safety.family_text |
| `consent-checklist` categories[].mandatory_disclosures | 17 | 17 | safety.family_text |
| `consent-checklist` categories[].contraindications | 17 | 17 | conditions.claims |
| `consent-checklist` categories[].emergency_signs | 17 | 17 | safety.family_text |
| `contraindications` rules[].from | 27 | 27 | claims |
| `contraindications` rules[].from_name | 27 | 27 | claims |
| `contraindications` rules[].to | 27 | 27 | claims |
| `contraindications` rules[].to_name | 27 | 27 | claims |
| `contraindications` rules[].level | 27 | 27 | claims |
| `contraindications` rules[].interval | 27 | 27 | claims |
| `contraindications` rules[].note | 27 | 27 | claims |
| `extracted` {code}.aftercare | 17 | 17 | safety.family_text |
| `extracted` {code}.contraindications.absolute | 17 | 17 | conditions.extracted_vs_taxonomy |
| `extracted` {code}.contraindications.relative | 17 | 17 | conditions.extracted_vs_taxonomy |
| `extracted` {code}.safety.emergency | 2 | 2 | safety.family_text |
| `literature-evidence` source_method | 1 | 1 | evidence.evidence_kind_by_file |
| `literature-evidence` categories.{code}.moa[].statement | 50 | 50 | evidence.statements · evidence.literature |
| `literature-evidence` categories.{code}.moa[].citations[].authors | 50 | 50 | evidence.statements · evidence.literature |
| `literature-evidence` categories.{code}.moa[].citations[].title | 50 | 50 | evidence.statements · evidence.literature |
| `literature-evidence` categories.{code}.moa[].citations[].journal | 50 | 50 | evidence.statements · evidence.literature |
| `literature-evidence` categories.{code}.moa[].citations[].year | 50 | 50 | evidence.statements · evidence.literature |
| `literature-evidence` categories.{code}.moa[].citations[].pmid | 50 | 50 | evidence.statements · evidence.literature |
| `literature-evidence` categories.{code}.moa[].citations[].doi | 48 | 48 | evidence.statements · evidence.literature |
| `literature-evidence` categories.{code}.moa[].citations[].pmc | 49 | 49 | evidence.statements · evidence.literature |
| `literature-evidence` categories.{code}.moa[].citations[].oa_url | 49 | 49 | evidence.statements · evidence.literature |
| `literature-evidence` categories.{code}.moa[].accuracy_score | 6 | 6 | evidence.statements · evidence.literature |
| `literature-evidence` categories.{code}.moa[].accuracy_note | 6 | 6 | evidence.statements · evidence.literature |
| `literature-evidence` categories.{code}.moa[].patient_ko | 50 | 50 | evidence.statements · evidence.literature |
| `literature-evidence` categories.{code}.moa[].patient_en | 50 | 50 | evidence.statements · evidence.literature |
| `literature-evidence` categories.{code}.moa[].patient_zh | 50 | 50 | evidence.statements · evidence.literature |
| `literature-evidence` categories.{code}.moa[].patient_ja | 50 | 50 | evidence.statements · evidence.literature |
| `literature-evidence` categories.{code}.adverse_effects[].statement | 32 | 32 | evidence.statements · evidence.literature |
| `literature-evidence` categories.{code}.adverse_effects[].citations[].authors | 32 | 32 | evidence.statements · evidence.literature |
| `literature-evidence` categories.{code}.adverse_effects[].citations[].title | 32 | 32 | evidence.statements · evidence.literature |
| `literature-evidence` categories.{code}.adverse_effects[].citations[].journal | 32 | 32 | evidence.statements · evidence.literature |
| `literature-evidence` categories.{code}.adverse_effects[].citations[].year | 32 | 32 | evidence.statements · evidence.literature |
| `literature-evidence` categories.{code}.adverse_effects[].citations[].pmid | 32 | 32 | evidence.statements · evidence.literature |
| `literature-evidence` categories.{code}.adverse_effects[].citations[].doi | 30 | 30 | evidence.statements · evidence.literature |
| `literature-evidence` categories.{code}.adverse_effects[].citations[].pmc | 29 | 29 | evidence.statements · evidence.literature |
| `literature-evidence` categories.{code}.adverse_effects[].citations[].oa_url | 29 | 29 | evidence.statements · evidence.literature |
| `literature-evidence` categories.{code}.adverse_effects[].accuracy_score | 8 | 8 | evidence.statements · evidence.literature |
| `literature-evidence` categories.{code}.adverse_effects[].accuracy_note | 8 | 8 | evidence.statements · evidence.literature |
| `literature-evidence` categories.{code}.adverse_effects[].patient_ko | 32 | 32 | evidence.statements · evidence.literature |
| `literature-evidence` categories.{code}.adverse_effects[].patient_en | 32 | 32 | evidence.statements · evidence.literature |
| `literature-evidence` categories.{code}.adverse_effects[].patient_zh | 32 | 32 | evidence.statements · evidence.literature |
| `literature-evidence` categories.{code}.adverse_effects[].patient_ja | 32 | 32 | evidence.statements · evidence.literature |
| `literature-evidence` categories.{code}.effects[].statement | 37 | 37 | evidence.statements · evidence.literature |
| `literature-evidence` categories.{code}.effects[].citations[].authors | 37 | 37 | evidence.statements · evidence.literature |
| `literature-evidence` categories.{code}.effects[].citations[].title | 37 | 37 | evidence.statements · evidence.literature |
| `literature-evidence` categories.{code}.effects[].citations[].journal | 37 | 37 | evidence.statements · evidence.literature |
| `literature-evidence` categories.{code}.effects[].citations[].year | 37 | 37 | evidence.statements · evidence.literature |
| `literature-evidence` categories.{code}.effects[].citations[].pmid | 37 | 37 | evidence.statements · evidence.literature |
| `literature-evidence` categories.{code}.effects[].citations[].doi | 35 | 35 | evidence.statements · evidence.literature |
| `literature-evidence` categories.{code}.effects[].citations[].pmc | 36 | 36 | evidence.statements · evidence.literature |
| `literature-evidence` categories.{code}.effects[].citations[].oa_url | 36 | 36 | evidence.statements · evidence.literature |
| `literature-evidence` categories.{code}.effects[].patient_ko | 37 | 37 | evidence.statements · evidence.literature |
| `literature-evidence` categories.{code}.effects[].patient_en | 37 | 37 | evidence.statements · evidence.literature |
| `literature-evidence` categories.{code}.effects[].patient_zh | 37 | 37 | evidence.statements · evidence.literature |
| `literature-evidence` categories.{code}.effects[].patient_ja | 37 | 37 | evidence.statements · evidence.literature |
| `literature-evidence` categories.{code}.effects[].accuracy_score | 3 | 3 | evidence.statements · evidence.literature |
| `literature-evidence` categories.{code}.effects[].accuracy_note | 3 | 3 | evidence.statements · evidence.literature |
| `patient-education` categories[].id | 17 | 17 | safety.family_text |
| `patient-education` categories[].name | 17 | 17 | safety.family_text |
| `patient-education` categories[].simple_explanation | 17 | 17 | safety.family_text |
| `patient-education` categories[].how_it_works | 17 | 17 | safety.family_text |
| `patient-education` categories[].duration_simple | 17 | 17 | safety.family_text |
| `patient-education` categories[].pain_level | 17 | 17 | safety.family_text |
| `patient-education` categories[].downtime | 17 | 17 | safety.family_text |
| `patient-education` categories[].common_concerns[].q | 51 | 51 | safety.family_text |
| `patient-education` categories[].common_concerns[].a | 51 | 51 | safety.family_text |
| `pih-risk` procedures[].risk_factors | 26 | 26 | safety.pih |
| `pih-risk` procedures[].prevention | 26 | 26 | safety.pih |
| `post-procedure-timeline` consensus_method | 1 | 1 | evidence.evidence_kind_by_file |
| `post-procedure-timeline` timelines[].id | 10 | 10 | safety.timelines |
| `post-procedure-timeline` timelines[].category | 10 | 10 | safety.timelines |
| `post-procedure-timeline` timelines[].name | 10 | 10 | safety.timelines |
| `post-procedure-timeline` timelines[].phases[].period | 43 | 43 | safety.timelines |
| `post-procedure-timeline` timelines[].phases[].label | 43 | 43 | safety.timelines |
| `post-procedure-timeline` timelines[].phases[].normal | 43 | 43 | safety.timelines |
| `post-procedure-timeline` timelines[].phases[].abnormal | 43 | 43 | safety.timelines |
| `post-procedure-timeline` timelines[].phases[].caution | 43 | 43 | safety.timelines |
| `post-procedure-timeline` timelines[].phases[].emergency | 43 | 43 | safety.timelines |
| `pre-procedure-checklist` universal_checks[].id | 12 | 12 | conditions.claims |
| `pre-procedure-checklist` universal_checks[].label | 12 | 12 | conditions.claims |
| `pre-procedure-checklist` universal_checks[].type | 12 | 12 | conditions.claims |
| `pre-procedure-checklist` universal_checks[].description | 12 | 12 | conditions.claims |
| `pre-procedure-checklist` category_specific[].id | 17 | 17 | conditions.claims |
| `pre-procedure-checklist` category_specific[].name | 17 | 17 | conditions.claims |
| `pre-procedure-checklist` category_specific[].checks[].label | 123 | 123 | conditions.claims |
| `pre-procedure-checklist` category_specific[].checks[].type | 123 | 123 | conditions.claims |
| `problem-packages` problems[].complaints[].combos[].name | 146 | 146 | claims |
| `problem-packages` problems[].complaints[].combos[].combo | 146 | 146 | claims |
| `problem-packages` problems[].complaints[].combos[].reason | 146 | 146 | claims |
| `problem-packages` problems[].complaints[].combos[].evidence | 146 | 146 | claims |
| `procedure-profiles` profiles[].phase | 17 | 17 | profile_attrs |
| `procedure-profiles` profiles[].phaseOrder | 17 | 17 | profile_attrs |
| `procedure-profiles` profiles[].hasProtein | 17 | 17 | profile_attrs |
| `procedure-profiles` profiles[].hasHA | 17 | 17 | profile_attrs |
| `procedure-profiles` profiles[].usesGel | 17 | 17 | profile_attrs |
| `procedure-profiles` profiles[].createsWound | 17 | 17 | profile_attrs |
| `procedure-profiles` profiles[].createsChannel | 17 | 17 | profile_attrs |
| `procedure-profiles` profiles[].thermalLoad | 17 | 17 | profile_attrs |
| `procedure-profiles` profiles[].bleedingRisk | 17 | 17 | profile_attrs |
| `procedure-profiles` profiles[].swellingRisk | 17 | 17 | profile_attrs |
| `procedure-profiles` profiles[].practicalNotes | 17 | 17 | profile_attrs |
| `procedure-profiles` profiles[].aftercare | 17 | 17 | safety.family_text |
| `synergy` links[].from | 115 | 115 | claims |
| `synergy` links[].from_category | 115 | 115 | claims |
| `synergy` links[].to | 115 | 115 | claims |
| `synergy` links[].to_category | 115 | 115 | claims |
| `synergy` links[].type | 115 | 115 | claims |
| `synergy` links[].reason | 115 | 115 | claims |
| `synergy` links[].timing | 115 | 115 | claims |
| `taxonomy` modality[].subcategories[].items[].extracted.safety.common | 521 | 521 | safety.item_text_counts(5단계 행선지) |
| `taxonomy` modality[].subcategories[].items[].extracted.safety.serious | 187 | 187 | safety.item_text_counts(5단계 행선지) |
| `taxonomy` modality[].subcategories[].items[].extracted.aftercare | 521 | 521 | safety.item_text_counts(5단계 행선지) |
| `taxonomy` modality[].subcategories[].items[].extracted.safety.note | 4 | 4 | safety.item_text_counts(5단계 행선지) |
| `taxonomy` modality[].subcategories[].items[].extracted.safety.contraindications | 4 | 4 | conditions.claims |
| `taxonomy` modality[].subcategories[].items[].extracted.safety.long_term | 1 | 1 | safety.item_text_counts(5단계 행선지) |
| `taxonomy` modality[].extracted.contraindications.absolute | 17 | 17 | conditions.claims |
| `taxonomy` modality[].extracted.contraindications.relative | 17 | 17 | conditions.claims |
| `taxonomy` modality[].extracted.safety.common | 17 | 17 | safety.family_text |
| `taxonomy` modality[].extracted.safety.uncommon | 17 | 17 | safety.family_text |
| `taxonomy` modality[].extracted.safety.serious | 15 | 15 | safety.family_text |
| `taxonomy` modality[].extracted.aftercare | 17 | 17 | safety.family_text |
| `taxonomy` modality[].products[].extracted.safety.contraindications | 1 | 1 | claims |
| `treatment-optimization` consensus_method | 1 | 1 | evidence.evidence_kind_by_file |
| `treatment-optimization` optimization_principles | 1 | 1 | optimization_principles |
| `treatment-optimization` by_concern[].severity_levels[].contraindicated_combos | 24 | 24 | claims · avoid_edges · conditions.claims |
| `treatment-optimization` by_age_group[].age | 4 | 4 | conditions.claims |
| `treatment-optimization` by_age_group[].avoid | 4 | 4 | conditions.claims |
| `treatment-optimization` combination_rules[].rule | 8 | 8 | claims · avoid_edges · attrs · evidence.guides |
| `treatment-optimization` combination_rules[].detail | 8 | 8 | claims · avoid_edges · attrs · evidence.guides |
| `treatment-optimization` combination_rules[].evidence | 8 | 8 | claims · avoid_edges · attrs · evidence.guides |
| `treatment-optimization` combination_rules[].consensus | 8 | 8 | claims · avoid_edges · attrs · evidence.guides |
| `treatment-optimization` combination_rules[].priority | 8 | 8 | claims · avoid_edges · attrs · evidence.guides |
| `treatment-sequence` principles | 1 | 1 | claims · principles_text_only |
| `treatment-sequence` sequence_order[].order | 11 | 11 | sequence_rank |
| `treatment-sequence` sequence_order[].phase | 11 | 11 | sequence_rank |
| `treatment-sequence` sequence_order[].categories | 11 | 11 | sequence_rank |
| `treatment-sequence` sequence_order[].reason | 11 | 11 | sequence_rank |
| `treatment-sequence` incompatible_same_day[].pair | 9 | 9 | claims · conditions.claims(C10) |
| `treatment-sequence` incompatible_same_day[].reason | 9 | 9 | claims · conditions.claims(C10) |
| `treatment-sequence` minimum_intervals[].from | 9 | 9 | claims · conditions.claims(C10) · evidence.guides |
| `treatment-sequence` minimum_intervals[].to | 9 | 9 | claims · conditions.claims(C10) · evidence.guides |
| `treatment-sequence` minimum_intervals[].min_days | 7 | 7 | claims · conditions.claims(C10) · evidence.guides |
| `treatment-sequence` minimum_intervals[].source | 9 | 9 | claims · conditions.claims(C10) · evidence.guides |
| `treatment-sequence` minimum_intervals[].reason | 9 | 9 | claims · conditions.claims(C10) · evidence.guides |
| `treatment-sequence` minimum_intervals[].min_months | 2 | 2 | claims · conditions.claims(C10) · evidence.guides |

## 원천 수정 후보

- 원천 시술군 코드 ↔ 정본 계열 어긋남 — M17-엑소좀 (원천 코드 M17 ↔ 해석 계열 M5R8-0042)
- 원천 시술군 코드 ↔ 정본 계열 어긋남 — M4-쥬베룩 (원천 코드 M4 ↔ 해석 계열 M3R8-0076)
- 원천 시술군 코드 ↔ 정본 계열 어긋남 — M4-쥬베룩 (원천 코드 M4 ↔ 해석 계열 M3R8-0078)
- 원천 시술군 코드 ↔ 정본 계열 어긋남 — M4-쥬베룩 (원천 코드 M4 ↔ 해석 계열 M3R8-0079)
- 원천 시술군 코드 ↔ 정본 계열 어긋남 — M4-쥬베룩 (원천 코드 M4 ↔ 해석 계열 M3R8-0080)
- 원천 시술군 코드 ↔ 정본 계열 어긋남 — M8-서브시전 (원천 코드 M8 ↔ 해석 계열 N4R8-0100)
- 원천 시술군 코드 ↔ 정본 계열 어긋남 — M8-서브시전 (원천 코드 M8 ↔ 해석 계열 N4R8-0101)
- 원천 시술군 코드 ↔ 정본 계열 어긋남 — M8-서브시전 (원천 코드 M8 ↔ 해석 계열 N4R8-0102)
- 원천 시술군 코드 ↔ 정본 계열 어긋남 — M4-쥬베룩 (원천 코드 M4 ↔ 해석 계열 M3R8-0109)
- 출처 칸이 출처가 아님 — 피부 회복 (EV-GD-004)

## open

없음

## 낡은 결정(stale)

없음

## 고정 시험 67/67

- PASS I-ALT — 「택 1 시술」 → kind 대체 · 간격 비움(L-ALT)
- PASS I-MD — 의료진 평가 → 간격 없음 + 의료진 판단 표시(L-MD)
- PASS I-SEP — 별도 세션 → same_day false(L-SEP) + 2주 후
- PASS I-SDNO — 동시 시술 금지 → same_day false(L-SDNO)
- PASS I-SAMESITE — 같은 부위 조건(L-SAMESITE) · 「내 금지」 = 그 기간이 지나야 함
- PASS I-DIFFSITE — 같은 날이면 다른 부위(L-SDIFFSITE) · 범위
- PASS I-IMM — 「직후」 → same_day true · days [0,0](L-IMM)
- PASS I-SDOK — 같은 날 가능 → same_day true(L-SDOK)
- PASS I-BEFORE — 「…전에」 → first 만(L-BEFORE)
- PASS I-BETWEEN — 「사이사이」 → 반복 표시 · 간격 없음(L-BETWEEN)
- PASS I-REPEAT — 반복 표시(L-REPEAT)
- PASS I-COUNT — 회차는 간격 아님(L-COUNT)
- PASS I-SEQ — 「순차」 → 원천 from → to(L-SEQ)
- PASS I-ONLY — 「…에 한해」 조건부(L-ONLY)
- PASS I-NUM-AFTER — 「N주 후」 → days · open_high(L-NUM)
- PASS I-NUM-RANGE — 「N~M주 간격」 → 범위 · 위로 닫힘
- PASS I-NUM-HOUR — 시간 단위 · 「내 금지」 = 위로 열림
- PASS I-NUM-MIX — 단위가 다른 범위
- PASS I-OPTIONS — 하위 조건 「A: … / B: …」 → options 별 값 · 겉 칸 비움(검수 F2 — 이전엔 감싼 범위였음)
- PASS I-OR — 「또는」 → options + 감싼 범위
- PASS B0 — 원천 · 결정 그대로 = open 0
- PASS D-ALT — 간격 사전 「택 1」 갈래를 빼면 원문 간격 낱말이 있는데 숫자 칸 · 표시가 빈 주장이 open
- PASS D-MD — 「의료진 … 간격 결정」 갈래를 빼면 open
- PASS D-BETWEEN — 「사이사이」 갈래를 빼면 open
- PASS D-ALIAS — 이름 풀이 사전 「왁싱」을 빼면 못 푼 이름 → 원천 질문 없음 → open
- PASS D-Q — 원천 질문(TCA Cross)을 빼면 open
- PASS D-QCONF — 충돌 질문(보톡스 ↔ 필러)을 빼면 open
- PASS D-PAT — 고민 조건 금기 패턴을 빼면 그 문장이 패턴 밖 → open
- PASS D-COND — 확인 조건 사전 「일광 · 태닝」을 빼면 open · 「선탠 후 …」가 시술 쌍으로 남아 원천별 주장 셈이 달라짐(이유 없음 open 도 함께)
- PASS D-FIELD — 8단계 칸 반영 규칙을 빼면 그 칸이 open(source-map 전수)
- PASS D-TL — 경과표 붙는 곳 결정을 빼면 open
- PASS S7-COMBO — 7단계 최적화 조합이 없으면 끝점 어긋남 open
- PASS S7-CC — 7단계 CC 추천 시술 엣지가 없으면 끝점 어긋남 open
- PASS S7-CONCERN — 7단계 고민 노드(기미 P5-1)가 없으면 피함 끝점 어긋남 open
- PASS AV — 고민 「기미」 → 레이저 · IPL 「피함」(U8-2 (가))
- PASS P-PRIN2 — 원칙 2 — 「HIFU 선행 또는 2주 이상 간격」 → 순서 + 반대 방향 간격 · 「RF·IPL·비침습 레이저는 당일 병행 가능」 → 생략 상대(보톡스)
- PASS P-RULE3 — 규칙 3 — detail 에 쌍 없음 → 제목 「프락셔널 후 당일 필러 금지」 + 이름 없는 간격 문장 「최소 4주 간격」 붙임
- PASS I-SUBCOND — 검수 F2 — 하위 조건이 갈리면 겉 칸 비움 · options 별로 읽음
- PASS I-OR-NOSUB — 하위 조건 없는 「또는」은 감싼 범위 그대로(R8-0030)
- PASS P-SUBCOND — 검수 F2 — R8-0003 보톡스 ↔ 레이저: 겉 칸 비움 · 비박리 = 같은 날 · 레이저 먼저 / 박리 = 3일~1주
- PASS SC — 검수 F1 — 「고출력 · 고에너지 레이저」 피함(M8 계열로 열림) · 「심부 필링 · 박리성 레이저」 금기 = 조건부 · IPL 단독(이름 일치 단위 시술)은 기본 적용
- PASS D-Q17 — 조건부 피함의 원천 질문을 빼면 open
- PASS D-REASON — 검수 W1 — 조사 대비 셈 차이 이유를 빼면 open
- PASS SEM-side_effect_exceptions — B1 예외 — severity mild 인데 발생률에 흔함 낱말 없음 → 부작용 + 의료진 질문 Q8-19
- PASS SEM-severity_split — U2 · B1 — 합병증 = moderate 이상 + U1 원문 serious · 부작용 = mild + U1 원문 common · uncommon
- PASS SEM-gap_fill — U1 — complications.json 없는 계열 중 taxonomy 원문 있는 7계열 채움 · gap = 원천 없음만 · 전부 mild 인 계열은 따로
- PASS SEM-not_condition — B8 — 상담 · 시술 준비 · 고지 · 조건 아닌 문장은 확인 조건 엣지에서 빠짐(남은 것은 사람 조건 · 연령대만)
- PASS SEM-endpoint_kinds — U3 · B3 — 끝점 묶음 = 엣지 endpoints.candidates[] (노드 아님)
- PASS D-Q19 — 부작용 예외 질문(Q8-19)을 빼면 open
- PASS CR-R1 — R1 — 보톡스 ↔ 필러 같은 날 가능 ↔ 「별도 세션」 문맥 false(세션 축) · 필러 ↔ HIFU 같은 날 가능(RF 먼저) ↔ 불가(필러 먼저 — 순서 축) = 가짜 충돌 해제
- PASS CR-R2 — R2 — 보톡스 × 아미노글리코시드: 사전 체크 확인만 · taxonomy 주의 · 동의서 금기 → 금기
- PASS CR-R3 — R3 — 레이저 ↔ MTS 2주 · 프락셔널 4주 후 MTS → 프락셔널 끝 엣지 4주(더 긴 간격)
- PASS CR-R4 — R4 — IPL + 필러 같은 날 가능 ↔ HA 필러 ↔ 레이저 같은 날 불가(계열 상속) → 불가
- PASS CR-R5 — R5 — 니들RF 2주 후 필링 ↔ 필링 2주 후 니들RF · 레이저 → 니들RF ↔ 니들RF → 레이저 = 진짜 반대(순서 단정 안 함 + 의료진)
- PASS CR-R6 — R6 + R1 — 이소트레티노인 대기: 얕은 · 비박리 6개월(0~2개월 원문 보관) · 박리 · 심부 12개월(6개월 원문 보관) · 조건 모름 12개월
- PASS CR-GUARD — 전수 가드 — 앱에 두 값이 나갈 수 있는 엣지 · 단위 시술 쌍 · 단위 시술 × 조건 0
- PASS CR-D-R1 — 결정 규칙 R1 를 빼면 open
- PASS CR-D-R2 — 결정 규칙 R2 를 빼면 open
- PASS CR-D-R3 — 결정 규칙 R3 를 빼면 open
- PASS CR-D-R4 — 결정 규칙 R4 를 빼면 open
- PASS CR-D-R5 — 결정 규칙 R5 를 빼면 open
- PASS CR-D-R6 — 결정 규칙 R6 를 빼면 open
- PASS QE — 품질 E — 끝점 「바디 HIFU/RF로 잔여 지방+타이트닝」 부위 낱말 「바디」 → 바디 단위 시술만(1차: 얼굴 전체 · 눈가 고주파가 붙음)
- PASS QI — 품질 I — 원천 행 1:1 착지표(row_landing) · 없음 0 · 쌍 없는 원칙 5행은 원문만(규칙)
- PASS QK — 품질 K — 안전 원천 밖 계열(N4 · N9 …) 단위 시술은 「정보 없음(gap)」 명시 · 값 있는 단위 시술(U5-001)은 없음
- PASS QO — 품질 O — HA 필러 → RF/HIFU 같은 날 불가 · 역순 가능 = by_direction 으로 남음(한 값으로 안 접음)
- PASS QJ — 품질 J — extracted.json aftercare 원문이 계열 원문 칸에(1차 M2 · M3 · M5 aftercare 3행 누락)
