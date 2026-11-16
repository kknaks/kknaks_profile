# 원천 수정 목록 — Procedure Hub stg 데이터

> 정본: `source-fix-list.json` (이 문서는 그 요약이고 수치는 JSON 에서 뽑았다) · 생성 2026-10-27T00:33:34+00:00 · 그래프 발행본 v1 · 원천 저장본 `phub-stg-2026-10-26`
> 작성: researcher 워커(read-only) · 로컬 graph DB SELECT + stg 저장본 JSON. stg 재호출 없음
> 갱신 2026-10-27T08:52:27+00:00 — **E7 원장 업체 표기 오류 13 · E8 원장 이름 오기 6 추가**(기존 그룹 · 항목 · id 그대로). 근거는 `company-relation-check.json` · `product-master-draft.md`(4차) 그대로 — 식약처 · stg · 웹 새 호출 없음. 업체 관계 결정은 `gate-answers/company-relation-decisions.json`

## 왜 이 목록인가

사용자 결정(2026-10-27): 「처짐/쳐짐」 같은 문제는 Hub 동의어 사전이 아니라 **원천 표기 수정**으로 푼다. 원천은 회사 데이터라 직접 고치지 않고 데이터 관리자에게 넘긴다. 사용자가 항목마다 수정 / 보류 / 확인 요청을 단다.

## 합계

- 그룹 27개 · 항목 **276** · `proposed` 채움 **37** · null **239** · 의료 판단 필요 94 (E7 · E8 추가 전: 그룹 25 · 항목 257 · 채움 24 · 의료 93)
- `proposed` 는 원장에 실제로 있는 이름일 때만 채웠다(괄호 설명을 뺀 본문이 원장 이름과 정규화 완전 일치 · A1 은 사용자 결정 표기 · A5 는 같은 CC 권장 시술명). 나머지는 `candidates` 에 원장 실물 후보 0~3개 — 글자로만 뽑은 후보라 의미 확인이 필요하다
- 같은 `current` 가 여러 번 나오면 한 항목으로 묶고 `occurrences` 에 횟수를 적었다

| 그룹 | 분류 | 제목 | count | 항목 | proposed | 검증(줄어야 할 것) |
|---|---|---|---|---|---|---|
| A1 | A | 고민 이름 오기 「쳐짐」 | 14 | 6 | 6 | graph_search 「처짐」 이 concern:P3 · P3 하위 · 항목을 돌려준다(SPEC S-3 결과가 바뀐다). 원천 전체 「쳐짐」 문자열 0 |
| A2 | A | synergy 끝점 이름 | 67 | 22 | 2 | unresolved_name_ref(synergy.endpoints) 67/230 → 0 |
| A3 | A | optimization 조합 문자열 | 48 | 44 | 11 | unresolved_name_ref(treatment-optimization.optimal_combo) 48/74 → 0 |
| A4 | A | CC 권장 시술 name | 66 | 15 | 0 | unresolved_name_ref(problem-packages.procedures.name) 66/254 → 0 |
| A5 | A | CC 조합 이름 | 36 | 4 | 3 | combo_not_in_procedures 36/277 → 0 |
| A6 | A | treatment-sequence 이름 | 23 | 18 | 2 | unresolved_name_ref(treatment-sequence.names) 23/35 → 0 |
| A7 | A | 패키지 제품 문장 | 37 | 15 | 0 | 패키지 제품 토큰 37/88 미일치 → 0 (검증 코드 없음 — 이 목록의 셈 규칙으로 재계산) |
| B1 | B | 원천 충돌 — 시술 순서 | 7 | 7 | 0 | source_conflict 7 → 0 |
| B2 | B | 「서브시전」 시술군 불일치 | 6 | 1 | 0 | problem-packages 「서브시전」 category 와 taxonomy 소속 시술군 일치 — 불일치 6행 → 0 (검증 코드 없음) |
| B3 | B | 이소트레티노인이 시술 항목 | 1 | 1 | 0 | 시술 노드에 약물 0 · 또는 이소트레티노인 procedure_relation ≥ 1 |
| B4 | B | CC 권장 목록 동일 | 98 | 29 | 0 | 권장 목록이 다른 CC 와 완전히 같은 CC 98/115 → 줄어듦(서로 다른 목록 46 → 늘어남, 검증 코드 없음) |
| C1 | C | 고민 항목 시술 연결 없음 | 26 | 26 | 0 | coverage_gap/concern_item_without_taxonomy_ref 26/117 → 0 · concern_item_without_any_treats 1 → 0 |
| C2 | C | 패키지 없는 고민 | 6 | 6 | 0 | coverage_gap/concern_without_curated_package 6 → 0 |
| C3 | C | 금기 규칙 없는 시술군 | 6 | 6 | 0 | coverage_gap/procedure_group_without_contraindication_rule 6 → 0 |
| C4 | C | 합병증 없는 시술군 | 7 | 7 | 0 | coverage_gap/procedure_group_without_complication 7 → 0 |
| D1 | D | 고민 아닌 항목이 고민 트리에 | — | 5 | 0 | 검증 코드 없음 — 고민 어휘 정본 결정(DEC OQ-104 · OQ-105) 뒤에 정한다 |
| D2 | D | 고민 항목 이름이 시술명 | 25 | 5 | 0 | 검증 코드 없음 — 고민 항목 이름이 시술 원장 이름과 완전 일치 25/117 |
| D3 | D | 같은 제품 두 원장 | 57 | 5 | 0 | product synonym 엣지 57 — 원장을 하나로 합치면 0 |
| D4 | D | 부위 마스터 없음 | — | 3 | 0 | 검증 코드 없음 — 부위 노드 정본 결정(DEC OQ-107) 뒤 |
| E1 | E | 고민 연결 없는 시술군(M13) | 1 | 1 | 0 | coverage_gap/procedure_group_without_concern 1 → 0 |
| E2 | E | 고민 트리와 안 이어진 다른 고민 어휘 | 16 | 16 | 0 | unlinked_vocabulary 16/25 → 줄어듦 |
| E3 | E | 제품끼리 시너지 자기쌍 | 1 | 1 | 0 | self_relation_skipped 1 → 0 |
| E4 | E | CC 권장 제품 이름 | 9 | 4 | 0 | CC 권장 제품 9/388 미일치 → 0 (검증 코드 없음) |
| E5 | E | 금기 note 순서 표기 | 1 | 1 | 0 | M2↔M7 relation 에 first 주장 생김 |
| E6 | E | 같은 고민 항목에서 두 원천이 다른 시술군 | 9 | 9 | 0 | 겹침 ∅ 9/90 → 0 (검증 코드 없음) |
| E7 | E | 원장 업체 표기 오류 | 13 | 13 | 7 | 이 항목 원장 업체가 company-relation-decisions.json 역할(제조사 · 수입사 · 판매사) 중 하나와 법인 표기 제거 일치 · 「이름 맞고 업체 다름」 0 (검증 코드 없음) |
| E8 | E | 원장 이름 오기 | 6 | 6 | 6 | 고친 이름으로 식약처 · 원장 정규화 완전 일치 — 지금 0 (검증 코드 없음) |

**수치 차이**(브리프 · 리포트 ↔ 실물):

- **A1** — 코디 분류의 「3곳」 = taxonomy 고유 문자열 6개(대분류 1 · 하위 라벨 3 · 항목 2) 중 하위 3곳을 센 것으로 보인다. 실물은 고유 문자열 6개 · 등장 14곳(taxonomy 6 · problem-packages 8)
- **A7** — 리포트 36/88 ↔ 실물 37/88. 셈 규칙: `+ · or · / · ( )` 로 쪼갠 토큰을 제품 원장(taxonomy 59 + products 59 이름 — 영문명을 더해도 37) 정규화 완전 일치로 판정. 1건 차이는 리포트의 토큰 분리 규칙이 남아 있지 않아 대조 불가
- **B4** — 리포트 「서로 다른 목록 48개」 ↔ 실물 46개 — (name, category) 쌍 순서까지 같은 것을 같은 목록으로 셌다. 98 은 일치
- **D2** — count = 고민 항목 이름이 원장(시술 항목 · 시술군 · 제품)과 정규화 완전 일치 25/117 — 리포트 25(시술군 6 + 시술 항목 19)와 같다. 원장과 글자가 다른 시술명(「CO2프락셀」 등)은 세지 않아 실제보다 작다. 항목은 대표 예시 5개(occurrences 합 ≠ count)
- **E4** — 리포트 9/388

## A. 표기 · 이름

### A1 고민 이름 오기 「쳐짐」 — 14건

- **왜**: 고민 트리(P3 대분류 · 하위 3 · 항목 2)와 problem-packages 가 「쳐짐」으로 적혀 「처짐」 검색이 고민 노드에 닿지 않는다. 다른 원장(optimization · 적응증 문장)은 「처짐」이라 어휘끼리도 안 이어진다
- **확인**: graph_search 「처짐」 이 concern:P3 · P3 하위 · 항목을 돌려준다(SPEC S-3 결과가 바뀐다). 원천 전체 「쳐짐」 문자열 0
- **근거**: research-report.md §Q3 3-4 · 요약 3 · SPEC-001.md §6.1 S-3 · _RESUME.md §2 2026-10-27
- **메모**: 코디 분류의 「3곳」 = taxonomy 고유 문자열 6개(대분류 1 · 하위 라벨 3 · 항목 2) 중 하위 3곳을 센 것으로 보인다. 실물은 고유 문자열 6개 · 등장 14곳(taxonomy 6 · problem-packages 8)

| id | 현재 | 횟수 | 제안 | 위치 |
|---|---|---|---|---|
| A1-002 | 얼굴 쳐짐 | 4 | 얼굴 처짐 | `taxonomy · problem-packages` taxonomy $.problem[2].subcategories[0].label 외 3곳 |
| A1-001 | 쳐짐 | 2 | 처짐 | `taxonomy · problem-packages` taxonomy $.problem[2].category 외 1곳 |
| A1-003 | 볼쳐짐/불독살 | 2 | 볼처짐/불독살 | `taxonomy · problem-packages` taxonomy $.problem[2].subcategories[0].items[0].name 외 1곳 |

### A2 synergy 끝점 이름 — 67건

- **왜**: `M?-이름` 의 이름 부분이 시술 항목 · 시술군 · 제품 어디에도 없다. 시너지 주장이 시술 항목이 아닌 시술군(*_category)에 붙어 「어느 장비 · 시술끼리」가 사라진다
- **확인**: unresolved_name_ref(synergy.endpoints) 67/230 → 0
- **근거**: research-report.md §Q3 3-3 · SPEC-001.md §3.4 unresolved_name_ref

| id | 현재 | 횟수 | 제안 | 위치 |
|---|---|---|---|---|
| A2-005 | M12-MTS | 8 | 후보: MTS롤러 (시술 항목 procedure:auto-M12-1775364775166), 마이크로니들링(MTS) (시술군 procedure_group:M12) | `synergy` $.links[10].to 외 7곳 |
| A2-001 | M9-리프팅기기 | 7 | — | `synergy` $.links[2].to 외 6곳 |
| A2-011 | M17-줄기세포 | 7 | 후보: 줄기세포배양액 (시술 항목 procedure:M17-1-1), 줄기세포유래 엑소좀 (시술 항목 procedure:M17-3-1), 줄기세포치료 (시술군 procedure_group:M17) | `synergy` $.links[27].from 외 6곳 |

### A3 optimization 조합 문자열 — 48건

- **왜**: 최적화 고민의 optimal_combo 가 표시용 문자열(괄호 설명 · 슬래시 묶음)이라 시술 노드로 안 풀린다. 최적화 고민 → 시술 treats ④ 엣지가 그만큼 빠진다
- **확인**: unresolved_name_ref(treatment-optimization.optimal_combo) 48/74 → 0
- **근거**: research-report.md §Q3 3-3 · §Q6 SPEC-015 INV-4 · SPEC-001.md §3.3 treats ④

| id | 현재 | 횟수 | 제안 | 위치 |
|---|---|---|---|---|
| A3-013 | 바이오스티뮬레이터 | 3 | 후보: 바이오스티뮬레이터/콜라겐부스터 (시술군 procedure_group:M3) | `treatment-optimization` $.by_concern[2].severity_levels[2].optimal_combo[3] 외 2곳 |
| A3-024 | MTS/니들RF | 2 | 후보: 니들RF (시술군 procedure_group:M11), MTS롤러 (시술 항목 procedure:auto-M12-1775364775166), 마이크로니들링(MTS) (시술군 procedure_group:M12) | `treatment-optimization` $.by_concern[5].severity_levels[1].optimal_combo[2] 외 1곳 |
| A3-028 | 프락셔널 레이저 | 2 | 후보: 레이저 (시술군 procedure_group:M8) | `treatment-optimization` $.by_concern[5].severity_levels[1].optimal_combo[0] 외 1곳 |

### A4 CC 권장 시술 name — 66건

- **왜**: CC 권장 시술 이름이 원장에 없어 category(시술군)까지만 이어진다. 「리프팅기기」 「프락셔널」 처럼 장비 묶음 이름이 많다
- **확인**: unresolved_name_ref(problem-packages.procedures.name) 66/254 → 0
- **근거**: research-report.md §Q3 3-1

| id | 현재 | 횟수 | 제안 | 위치 |
|---|---|---|---|---|
| A4-003 | 리프팅기기 | 17 | — | `problem-packages` $.problems[10].complaints[2].procedures[1].name 외 16곳 |
| A4-014 | 프락셔널 | 10 | 후보: CO2프락셔널 (시술 항목 procedure:M8-2-1), 어븀야그 프락셔널 (시술 항목 procedure:M8-2-3) | `problem-packages` $.problems[8].complaints[3].procedures[0].name 외 9곳 |
| A4-004 | 크라이오 | 8 | 후보: 크라이오듀얼 (시술 항목 procedure:auto-M14-1775364775188), 크라이오리포라이시스 (시술군 procedure_group:M14) | `problem-packages` $.problems[11].complaints[3].procedures[0].name 외 7곳 |

### A5 CC 조합 이름 — 36건

- **왜**: CC 조합 구성원이 같은 CC 권장 시술명과 글자가 달라(「PRP」 ↔ 「PRP/자가혈」) 조합이 권장 시술을 가리키지 못한다. SPEC-018 INV-4 위반
- **확인**: combo_not_in_procedures 36/277 → 0
- **근거**: research-report.md §Q3 3-3 · SPEC-001.md §3.4 combo_not_in_procedures

| id | 현재 | 횟수 | 제안 | 위치 |
|---|---|---|---|---|
| A5-002 | PRP | 23 | PRP/자가혈 | `problem-packages` $.problems[12].complaints[9].combos[0].combo[1] 외 22곳 |
| A5-003 | MTS | 6 | 마이크로니들링(MTS) | `problem-packages` $.problems[12].complaints[3].combos[0].combo[1] 외 5곳 |
| A5-001 | 바이오스티뮬레이터 | 4 | 바이오스티뮬레이터/콜라겐부스터 | `problem-packages` $.problems[10].complaints[6].combos[0].combo[1] 외 3곳 |

### A6 treatment-sequence 이름 — 23건

- **왜**: 간격 · 같은 날 불가 규칙의 양 끝 이름이 원장에 없어 엣지가 안 생긴다. 안전 정보(간격)가 그래프에서 빠진다
- **확인**: unresolved_name_ref(treatment-sequence.names) 23/35 → 0
- **근거**: SPEC-001.md §3.3 시술↔시술 주장 · §6.3 이소트레티노인

| id | 현재 | 횟수 | 제안 | 위치 |
|---|---|---|---|---|
| A6-001 | HA 필러 | 3 | — | `treatment-sequence` $.incompatible_same_day[5].pair[0] 외 2곳 |
| A6-013 | 이소트레티노인 복용 중 | 3 | 후보: 이소트레티노인 (시술 항목 procedure:auto-M15-1775361878302), 트레티노인 (시술 항목 procedure:auto-M15-1775361951887) | `treatment-sequence` $.incompatible_same_day[8].pair[0] 외 2곳 |
| A6-002 | RF/HIFU | 2 | — | `treatment-sequence` $.minimum_intervals[0].to 외 1곳 |

### A7 패키지 제품 문장 — 37건

- **왜**: problem-combos 패키지 제품이 「나보타 or 보툴렉스」 같은 문장이라 제품 노드로 이어지지 않는다. 그래프 빌드는 아직 이 칸을 쓰지 않아 검증 코드가 없다
- **확인**: 패키지 제품 토큰 37/88 미일치 → 0 (검증 코드 없음 — 이 목록의 셈 규칙으로 재계산)
- **근거**: research-report.md §Q3 3-3 · §Q2 2-1
- **메모**: 리포트 36/88 ↔ 실물 37/88. 셈 규칙: `+ · or · / · ( )` 로 쪼갠 토큰을 제품 원장(taxonomy 59 + products 59 이름 — 영문명을 더해도 37) 정규화 완전 일치로 판정. 1건 차이는 리포트의 토큰 분리 규칙이 남아 있지 않아 대조 불가

| id | 현재 | 횟수 | 제안 | 위치 |
|---|---|---|---|---|
| A7-002 | 리쥬란 | 10 | 후보: 리쥬란HB+ (시술 항목 procedure:M4-1-3), 리쥬란아이 (시술 항목 procedure:M4-1-2), 리쥬란힐러 (시술 항목 procedure:M4-1-1) | `problem-combos` $.combos[0].packages[2].products[0] 외 9곳 |
| A7-001 | 엘러간 | 6 | 후보: 보톡스(엘러간) (시술 항목 procedure:M1-2-1) | `problem-combos` $.combos[0].packages[2].products[0] 외 5곳 |
| A7-006 | PRP | 6 | 후보: PRP (시술 항목 procedure:M5-1-1), PRP/자가혈 (시술군 procedure_group:M5), 두피 PRP (시술 항목 procedure:auto-M15-1775361179322) | `problem-combos` $.combos[3].packages[2].products[0] 외 5곳 |

## B. 값 오류 · 충돌(의료 판단 필요)

### B1 원천 충돌 — 시술 순서 — 7건

- **왜**: 같은 시술 쌍에 원천끼리 「먼저」가 갈린다. 값을 고르지 않고 conflict 로 서빙한다(D-13b)
- **확인**: source_conflict 7 → 0
- **근거**: SPEC-001.md §3.3 · §6.3 M1↔M2 · review-code-report.md §7-5

| id | 현재 | 횟수 | 제안 | 위치 |
|---|---|---|---|---|
| B1-001 | 메디컬스킨케어(M15) ↔ 스킨부스터(M4) 순서 갈림 — synergy(synergy): 메디컬스킨케어 먼저 / synergy(synergy): 스킨부스터 먼저 / treatment-sequence(sequence_order): 메디컬스킨케어 먼저 | 1 | — | `synergy · treatment-sequence` synergy $.links[24] 외 2곳 |
| B1-002 | 니들RF(M11) ↔ 메디컬스킨케어(M15) 순서 갈림 — synergy(synergy): 니들RF 먼저 / synergy(synergy): 메디컬스킨케어 먼저 / treatment-sequence(sequence_order): 메디컬스킨케어 먼저 | 1 | — | `synergy · treatment-sequence` synergy $.links[11] 외 2곳 |
| B1-003 | 보톡스(M1) ↔ 기기 리프팅(M9) 순서 갈림 — synergy(synergy): 보톡스 먼저 / treatment-sequence(sequence_order): 기기 리프팅 먼저 | 1 | — | `synergy · treatment-sequence` synergy $.links[3] 외 1곳 |

### B2 「서브시전」 시술군 불일치 — 6건

- **왜**: CC 권장은 서브시전을 M8(레이저)로, taxonomy 시술 항목은 M15 로 둔다. 어느 시술군의 안전 · 시너지가 붙는지 갈린다
- **확인**: problem-packages 「서브시전」 category 와 taxonomy 소속 시술군 일치 — 불일치 6행 → 0 (검증 코드 없음)
- **근거**: research-report.md §Q3 3-3 · SPEC-001.md §7 OQ-S08

| id | 현재 | 횟수 | 제안 | 위치 |
|---|---|---|---|---|
| B2-001 | 「서브시전」 category=M8 ↔ taxonomy 시술 항목 「서브시전」 은 M15 소속 | 6 | 후보: M8, M15 | `problem-packages` $.problems[8].complaints[0].procedures[1].category 외 5곳 |

### B3 이소트레티노인이 시술 항목 — 1건

- **왜**: 약물이 시술 노드로 있다. 간격 규칙 상대편도 안 풀려 relation 0
- **확인**: 시술 노드에 약물 0 · 또는 이소트레티노인 procedure_relation ≥ 1
- **근거**: SPEC-001.md §6.3 · review-spec-001-report.md §7

| id | 현재 | 횟수 | 제안 | 위치 |
|---|---|---|---|---|
| B3-001 | 약물 「이소트레티노인」 이 시술 항목(procedure:auto-M15-1775361878302, M15 · 하위 「여드름 전용」) | 1 | — | `taxonomy` $.modality[14].subcategories[12].items[0] |

### B4 CC 권장 목록 동일 — 98건

- **왜**: CC 115개 중 98개가 다른 CC 와 권장 시술 목록이 완전히 같다. 고민이 달라도 추천이 같다
- **확인**: 권장 목록이 다른 CC 와 완전히 같은 CC 98/115 → 줄어듦(서로 다른 목록 46 → 늘어남, 검증 코드 없음)
- **근거**: research-report.md §Q3 3-1
- **메모**: 리포트 「서로 다른 목록 48개」 ↔ 실물 46개 — (name, category) 쌍 순서까지 같은 것을 같은 목록으로 셌다. 98 은 일치

| id | 현재 | 횟수 | 제안 | 위치 |
|---|---|---|---|---|
| B4-001 | 권장 [레이저(M8), 스킨부스터(M4)] 를 CC 8개가 똑같이 씀: P5:레이저토닝, P5:피코토닝, P5:미백필링, P5:피코레이저, P5:IPL, P5:피코/Q스위치, P6:토닝, P6:재생치료 | 8 | — | `problem-packages` $.problems[4].complaints[0].procedures 외 7곳 |
| B4-002 | 권장 [필러(M2), 보톡스(M1)] 를 CC 7개가 똑같이 씀: P1:코필러, P1:이마필러, P1:턱필러, P1:입술필러, P1:애교필러, P1:다크서클필러, P1:볼필러 | 7 | — | `problem-packages` $.problems[0].complaints[0].procedures 외 6곳 |
| B4-003 | 권장 [크라이오(M14), 인모드(M9)] 를 CC 7개가 똑같이 씀: P12:쿨스컬프팅, P12:지방분해주사(PPC/DC), P12:HPL주사, P12:BNLS주사, P12:브이올렛, P12:컷슬린, P12:바디HIFU | 7 | — | `problem-packages` $.problems[11].complaints[0].procedures 외 6곳 |

## C. 연결 빈칸

### C1 고민 항목 시술 연결 없음 — 26건

- **왜**: taxonomy modality_ref 가 빈 고민 항목. 25개는 problem-packages CC 가 대신 잇고 1개(「경화요법」)는 어디서도 안 이어진다
- **확인**: coverage_gap/concern_item_without_taxonomy_ref 26/117 → 0 · concern_item_without_any_treats 1 → 0
- **근거**: research-report.md §Q3 3-1 · SPEC-001.md §3.4 coverage_gap

| id | 현재 | 횟수 | 제안 | 위치 |
|---|---|---|---|---|
| C1-001 | 고민 항목 「약물치료」(하위 P6-1 「급성(활성) 여드름」) — modality_ref 비어 있음 | 1 | — | `taxonomy` $.problem[5].subcategories[0].items[2].modality_ref |
| C1-002 | 고민 항목 「서브시전」(하위 P7-3 「흉터형(열린모공)」) — modality_ref 비어 있음 | 1 | — | `taxonomy` $.problem[6].subcategories[2].items[1].modality_ref |
| C1-003 | 고민 항목 「경화요법」(하위 P8-3 「하지정맥류」) — modality_ref 비어 있음 | 1 | — | `taxonomy` $.problem[7].subcategories[2].items[0].modality_ref |

### C2 패키지 없는 고민 — 6건

- **왜**: problem-combos tier 패키지가 없는 고민 대분류
- **확인**: coverage_gap/concern_without_curated_package 6 → 0
- **근거**: research-report.md §Q3 3-1 (SPEC-004 OPEN-012)

| id | 현재 | 횟수 | 제안 | 위치 |
|---|---|---|---|---|
| C2-001 | 고민 P10 「제모」 — tier 패키지(problem-combos) 없음 | 1 | — | `problem-combos` $.combos[] (problem_id 없음) |
| C2-002 | 고민 P12 「바디」 — tier 패키지(problem-combos) 없음 | 1 | — | `problem-combos` $.combos[] (problem_id 없음) |
| C2-003 | 고민 P13 「두피/탈모」 — tier 패키지(problem-combos) 없음 | 1 | — | `problem-combos` $.combos[] (problem_id 없음) |

### C3 금기 규칙 없는 시술군 — 6건

- **왜**: 시술 간 금기 · 간격 규칙(contraindications)이 하나도 없는 시술군
- **확인**: coverage_gap/procedure_group_without_contraindication_rule 6 → 0
- **근거**: research-report.md §Q3 3-4 · DEC OQ-119

| id | 현재 | 횟수 | 제안 | 위치 |
|---|---|---|---|---|
| C3-001 | 시술군 M10 「HIFES/EMS」 — 시술 간 금기 · 간격 규칙 0 | 1 | — | `contraindications` $.rules[] (from/to 에 없음) |
| C3-002 | 시술군 M13 「플라즈마」 — 시술 간 금기 · 간격 규칙 0 | 1 | — | `contraindications` $.rules[] (from/to 에 없음) |
| C3-003 | 시술군 M14 「크라이오리포라이시스」 — 시술 간 금기 · 간격 규칙 0 | 1 | — | `contraindications` $.rules[] (from/to 에 없음) |

### C4 합병증 없는 시술군 — 7건

- **왜**: complications 에 항목이 없는 시술군
- **확인**: coverage_gap/procedure_group_without_complication 7 → 0
- **근거**: research-report.md §Q3 3-4 · DEC OQ-119

| id | 현재 | 횟수 | 제안 | 위치 |
|---|---|---|---|---|
| C4-001 | 시술군 M10 「HIFES/EMS」 — 합병증 0 | 1 | — | `complications` $.categories[] (id 없음) |
| C4-002 | 시술군 M12 「마이크로니들링(MTS)」 — 합병증 0 | 1 | — | `complications` $.categories[] (id 없음) |
| C4-003 | 시술군 M13 「플라즈마」 — 합병증 0 | 1 | — | `complications` $.categories[] (id 없음) |

## D. 구조(표기 수정만으로 안 됨)

### D1 고민 아닌 항목이 고민 트리에 — 대표 예시

- **왜**: 고민 트리에 시술 범주 · 부위가 섞여 「고민」 노드가 고민이 아닐 때가 있다 — 이름만 고쳐서는 안 되고 고민 어휘 정본을 정해야 한다(DEC OQ-104 · OQ-105)
- **확인**: 검증 코드 없음 — 고민 어휘 정본 결정(DEC OQ-104 · OQ-105) 뒤에 정한다
- **근거**: research-report.md §Q5 5-1 · SPEC-001.md §7 OQ-104 · OQ-105
- **메모**: 대표 예시만. 전수 셈은 「고민인가」 판정 기준이 없어 하지 않았다

| id | 현재 | 횟수 | 제안 | 위치 |
|---|---|---|---|---|
| D1-001 | 고민 대분류 「쁘띠시술」(P1) — 시술 범주 | 1 | — | `taxonomy` $.problem[0].category |
| D1-002 | 고민 대분류 「제모」(P10) — 시술 범주 | 1 | — | `taxonomy` $.problem[9].category |
| D1-003 | 고민 대분류 「얼굴윤곽」(P11) — 시술 · 부위 범주 | 1 | — | `taxonomy` $.problem[10].category |

### D2 고민 항목 이름이 시술명 — 25건

- **왜**: 고민 항목이 시술명이라 「고민 → 시술」 엣지가 사실상 「시술 → 시술군」이다 — 환자 말(증상)로 들어오는 검색이 고민 항목에 안 닿는다
- **확인**: 검증 코드 없음 — 고민 항목 이름이 시술 원장 이름과 완전 일치 25/117
- **근거**: research-report.md §Q3 3-1 「고민 항목 이름이 시술 엔티티 이름과 일치」
- **메모**: count = 고민 항목 이름이 원장(시술 항목 · 시술군 · 제품)과 정규화 완전 일치 25/117 — 리포트 25(시술군 6 + 시술 항목 19)와 같다. 원장과 글자가 다른 시술명(「CO2프락셀」 등)은 세지 않아 실제보다 작다. 항목은 대표 예시 5개(occurrences 합 ≠ count)

| id | 현재 | 횟수 | 제안 | 위치 |
|---|---|---|---|---|
| D2-001 | 고민 항목 「레이저토닝」 = 레이저토닝 (시술 항목 procedure:M8-1-1) | 1 | — | `taxonomy` $.problem[4].subcategories[0].items[0].name |
| D2-002 | 고민 항목 「피코토닝」 = 피코토닝 (시술 항목 procedure:M8-1-2) | 1 | — | `taxonomy` $.problem[4].subcategories[0].items[1].name |
| D2-003 | 고민 항목 「IPL」 = IPL (시술 항목 procedure:M8-3-1) | 1 | — | `taxonomy` $.problem[4].subcategories[1].items[1].name |

### D3 같은 제품 두 원장 — 57건

- **왜**: 같은 제품이 taxonomy 제품 · products 사전 두 원장에 따로 있어 검색에 같은 이름이 둘씩 나온다 — synonym 엣지로만 이어 둔 상태
- **확인**: product synonym 엣지 57 — 원장을 하나로 합치면 0
- **근거**: SPEC-001.md §3.2 · §6.3 · review-code-report.md §7-8
- **메모**: 대표 예시만(항목 occurrences 합 ≠ count)

| id | 현재 | 횟수 | 제안 | 위치 |
|---|---|---|---|---|
| D3-001 | 「쥬베룩」 product:M3-P-3 ↔ product:products:biostimulator:쥬베룩 | 1 | — | `taxonomy · products` taxonomy $.modality[2].products[3] ↔ products $.biostimulator.products[3] |
| D3-002 | 「테스리프트」 product:M7-P-3 ↔ product:products:thread_lift:테스리프트 | 1 | — | `taxonomy · products` taxonomy $.modality[6].products[3] ↔ products $.thread_lift.products[1] |
| D3-003 | 「보톡스」 product:M1-P-0 ↔ product:products:botulinum_toxin:보톡스 | 1 | — | `taxonomy · products` taxonomy $.modality[0].products[0] ↔ products $.botulinum_toxin.products[0] |

### D4 부위 마스터 없음 — 대표 예시

- **왜**: 부위 노드가 위험 부위 11곳뿐이라 「이마 주름」 같은 부위 질의가 고민 · 시술 · 가격으로 이어지지 않는다(DEC OQ-107)
- **확인**: 검증 코드 없음 — 부위 노드 정본 결정(DEC OQ-107) 뒤
- **근거**: research-report.md §Q2 2-1 부위 엔티티 · §Q3 3-4
- **메모**: 대표 예시만

| id | 현재 | 횟수 | 제안 | 위치 |
|---|---|---|---|---|
| D4-001 | 위험 부위 11곳 — body_part_key 전부 null, 고민 · 가격과 연결 없음 | 1 | — | `anatomy-danger-zones` $.zones[] |
| D4-002 | 부위가 고민 하위 라벨로만 있음(「코」 「턱/턱선」) | 1 | — | `taxonomy` problem[].subcategories[].label |
| D4-003 | 부위 · 국산/수입 구분이 가격 항목명 텍스트 안(「이마 주름 (수입)」) | 1 | — | `market-pricing` items[].name |

## E. 기타(분류 밖에서 새로 보인 것)

### E1 고민 연결 없는 시술군(M13) — 1건

- **왜**: 어떤 고민 원천에서도 들어오는 연결이 없는 시술군
- **확인**: coverage_gap/procedure_group_without_concern 1 → 0
- **근거**: research-report.md §Q3 3-2

| id | 현재 | 횟수 | 제안 | 위치 |
|---|---|---|---|---|
| E1-001 | 시술군 M13 「플라즈마」 — 들어오는 고민 연결 0 | 1 | — | `taxonomy · problem-packages · problem-combos` (어느 고민 원천에도 M13 없음) |

### E2 고민 트리와 안 이어진 다른 고민 어휘 — 16건

- **왜**: optimization 고민 · synergy 목표 효과 중 고민 트리에 같은 이름이 없는 것
- **확인**: unlinked_vocabulary 16/25 → 줄어듦
- **근거**: SPEC-001.md §3.4 unlinked_vocabulary · research-report.md §Q3 3-4

| id | 현재 | 횟수 | 제안 | 위치 |
|---|---|---|---|---|
| E2-001 | 최적화 고민 「바디컨투어링」 — 고민 트리에 같은 이름 없음 | 1 | — | `treatment-optimization` $.by_concern[7] |
| E2-002 | 최적화 고민 「볼륨 손실」 — 고민 트리에 같은 이름 없음 | 1 | — | `treatment-optimization` $.by_concern[2] |
| E2-003 | 최적화 고민 「색소/기미」 — 고민 트리에 같은 이름 없음 | 1 | — | `treatment-optimization` $.by_concern[4] |

### E3 제품끼리 시너지 자기쌍 — 1건

- **왜**: synergy 두 끝이 같은 시술군 제품이라 버려진 주장
- **확인**: self_relation_skipped 1 → 0
- **근거**: SPEC-001.md §3.3 · OQ-S10

| id | 현재 | 횟수 | 제안 | 위치 |
|---|---|---|---|---|
| E3-001 | 시너지 「M11-인트라셀 → M11-시크릿」 — 두 끝이 다 제품명이라 같은 시술군 M11 로 뭉개짐 | 1 | — | `synergy` $.links[9] |

### E4 CC 권장 제품 이름 — 9건

- **왜**: CC 권장 제품(product_name)이 제품 원장에 없는 것
- **확인**: CC 권장 제품 9/388 미일치 → 0 (검증 코드 없음)
- **근거**: research-report.md §Q3 3-3
- **메모**: 리포트 9/388

| id | 현재 | 횟수 | 제안 | 위치 |
|---|---|---|---|---|
| E4-003 | 헤어맥스(LLLT) | 3 | 후보: LLLT (저출력 레이저) (시술 항목 procedure:auto-M15-1775361031036) | `problem-packages` $.problems[12].complaints[3].procedures[0].products[0] 외 2곳 |
| E4-001 | 트리암시놀론(±5-FU) | 2 | — | `problem-packages` $.problems[8].complaints[6].procedures[0].products[0] 외 1곳 |
| E4-002 | PDL(V빔) | 2 | — | `problem-packages` $.problems[8].complaints[6].procedures[1].products[0] 외 1곳 |

### E5 금기 note 순서 표기 — 1건

- **왜**: note 의 「실 먼저」 가 시술군 이름과 달라 순서로 안 읽힌다
- **확인**: M2↔M7 relation 에 first 주장 생김
- **근거**: SPEC-001.md §6.3 M2↔M7 · review-spec-001-report.md §7

| id | 현재 | 횟수 | 제안 | 위치 |
|---|---|---|---|---|
| E5-001 | 실로 올리고 필러로 채우는 보완적 조합. 실 먼저 → 필러 순서 | 1 | 후보: 필러, 실리프팅 | `contraindications` $.rules[6].note |

### E6 같은 고민 항목에서 두 원천이 다른 시술군 — 9건

- **왜**: taxonomy modality_ref 와 CC 권장 시술군이 하나도 안 겹치는 고민 항목
- **확인**: 겹침 ∅ 9/90 → 0 (검증 코드 없음)
- **근거**: research-report.md §Q3 3-1 「교집합이 ∅ 9/90」

| id | 현재 | 횟수 | 제안 | 위치 |
|---|---|---|---|---|
| E6-001 | 고민 항목 「CO2프락셀」: taxonomy ref [M8] ↔ CC 권장 [M11, M4] — 겹치는 시술군 없음 | 1 | — | `taxonomy · problem-packages` $.problem[6].subcategories[2].items[0].modality_ref |
| E6-002 | 고민 항목 「광대축소주사」: taxonomy ref [M1] ↔ CC 권장 [M14] — 겹치는 시술군 없음 | 1 | — | `taxonomy · problem-packages` $.problem[10].subcategories[3].items[0].modality_ref |
| E6-003 | 고민 항목 「니들RF」: taxonomy ref [M11] ↔ CC 권장 [M4, M8] — 겹치는 시술군 없음 | 1 | — | `taxonomy · problem-packages` $.problem[8].subcategories[3].items[1].modality_ref |

### E7 원장 업체 표기 오류 — 13건

- **왜**: 원장 제품의 업체(detail)가 식약처 허가 업체 · 웹 확인과 다르다 — 업체 대조(SPEC-003 §3.3)에서 자동 확정이 빠지고, 제조사 · 수입사 · 판매사 역할이 틀리게 들어간다
- **확인**: 이 항목 원장 업체가 company-relation-decisions.json 역할(제조사 · 수입사 · 판매사) 중 하나와 법인 표기 제거 일치 · 「이름 맞고 업체 다름」 0 (검증 코드 없음)
- **근거**: company-relation-check.json · .md(관계 「원장 업체 표기 오류」 6) · product-master-draft.md ⑤ · §5 · gate-answers/company-relation-decisions.json
- **메모**: 업체 값이 역할별로 갈리는 항목(LDM · 리투오파인 · 튠페이스 · 포텐자 · 인에이블 · 퓨어녹스)은 proposed 를 비우고 notes 에 역할을 적었다

| id | 원장 | 현재 | 제안 | 왜 | 근거 · 출처 | 위치 |
|---|---|---|---|---|---|---|
| E7-001 | `auto-10-1774737181584` | PRP사이언스 | 피알피사이언스 | 원장 업체 「PRP사이언스」는 식약처 허가 업체 「(주)피알피사이언스」의 영문 표기 — 같은 회사로 보이나 글자가 달라 업체 대조(법인 표기 제거 일치)에서 빠진다 | company-relation-check.json 올리디아: 허가 제허 21-599 호 (주)피알피사이언스 · 모델 「올리디아(Olidia)」 · 관계 「원장 업체 표기 오류(표기 차이 — 같은 회사)」 · 동일 법인은 회사 공식 페이지로 확인 못 함 · 성분 충돌(PLLA/PCL)은 별건<br>https://www.smarttoday.co.kr/ko-kr/articles/102952<br>https://www.gangnamunni.com/events/147799 | `taxonomy` taxonomy 항목 auto-10-1774737181584 $.modality[2].subcategories[0].items[1].detail |
| E7-002 | `auto-34-1774737181584` | 화인맥  · 롱펄스 532+1064nm | 화인엠이씨  · 롱펄스 532+1064nm | 원장 업체 「화인맥」과 식약처 허가 업체 「화인엠이씨(주)」(FineMEC)가 글자가 달라 업체 대조에서 빠진다 | company-relation-check.json 노블린: 허가 제허 18-176 호 화인엠이씨(주) · 모델 Nobleen · FDA 510k K182663 제조사 FineMEC Co., Ltd. · 국문 법인명 = FineMEC 대응을 직접 적은 출처는 없음 · 현장 사진 DEV-006 Nobleen<br>https://fda.innolitics.com/device/K182663<br>https://healthmanagement.org/site/p/finemec-ltd | `taxonomy` taxonomy 항목 auto-34-1774737181584 $.modality[7].subcategories[3].items[4].detail |
| E7-003 | `auto-M8-1775362928187` | 팔로마/시너론 · 810nm 다이오드 · 대면적 | 사이노슈어(구 팔로마) · 810nm 다이오드 · 대면적 | 벡터스는 Palomar 제품이고 2013 Cynosure 가 Palomar 를 인수 — 원장의 「시너론」은 근거 없는 표기 | company-relation-check.json 벡터스: 허가 수허 13-532 호 (주)루트로닉(제조원 Cogmedix, Inc) · 취소 · SEC 8-K: Cynosure 의 Palomar 인수 · 시너론과의 관계 근거 없음 — 충돌 「원장 팔로마/시너론 vs 출처 Palomar → Cynosure」<br>https://www.sec.gov/Archives/edgar/data/0000881695/000119312513112490/d503633dex991.htm<br>https://www.smarttoday.co.kr/ko-kr/articles/42188 | `taxonomy` taxonomy 항목 auto-M8-1775362928187 $.modality[7].subcategories[4].items[10].detail |
| E7-004 | `auto-M9-1775361433713` | 비올 · 고주파 리프팅 | 쉬엔비 · 고주파 리프팅 | 버츄RF(VirtueRF)는 쉬엔비 자체 제조 · 국내 판매 — 비올은 경쟁사(쉬엔비 상대 미국 특허 소송)로 판매 관계 근거 없음 | company-relation-check.json 버츄RF: 허가 제허 21-970 호 (주)쉬엔비 · 모델 VirtueRF · 현장 사진 DEV-019 「VIRTUE RF · SHENB」 · product-master-draft.md 「maker_hint 비올은 오류 — 쉬엔비 제조, 미국은 Cartessa 유통」<br>https://mdon.co.kr/mobile/article.html?no=32027<br>http://www.bosa.co.kr/news/articleView.html?idxno=2209773<br>https://www.hitnews.co.kr/news/articleView.html?idxno=47120<br>https://www.cartessaaesthetics.com/blog/cartessas-virtuerf-microneedling-platform-expands-capabilities-with-two-new-handpieces<br>https://www.imcas.com/en/attend/imcas-asia-2018/sponsor/7137 | `taxonomy` taxonomy 항목 auto-M9-1775361433713 $.modality[8].subcategories[1].items[7].detail |
| E7-005 | `auto-M9-1775361486532` | 클래시스 GX모드 입체가열 | 원텍 GX모드 입체가열 | 올리지오 X 는 원텍 제품 — 클래시스와의 관계 근거 없음 | company-relation-check.json 올리지오X: 허가 제허 23-860 호 원텍(주) · 모델 Oligio X · 현장 사진 DEV-010 Oligio X · product-master-draft.md 「maker_hint 클래시스는 오류 — 원텍 모노폴라 RF」<br>https://www.news1.kr/bio/healthcare/6109292<br>https://www.hankyung.com/article/202605146962r<br>https://www.medifonews.com/news/article.html?no=203339<br>https://medifonews.com/news/article.html?no=216226 | `taxonomy` taxonomy 항목 auto-M9-1775361486532 $.modality[8].subcategories[1].items[8].detail |
| E7-006 | `auto-M16-1775363074847` | 제이시스 · 국소동적미세마사지 · HA 합성 촉진 | — | LDM 은 독일 Wellcomet GmbH 상표 · 국내 허가는 (주)웰코멧아시아 — 원장 업체 「제이시스」는 근거 없음(없다는 근거도 아님). 바꿀 값은 역할별(제조 WELLCOMET GmbH · 수입 (주)웰코멧아시아 · 판매 웰코멧코리아)이라 한 칸 값으로 정하지 않았다 | company-relation-check.json LDM초음파관리: 허가 수인 11-587 호 · 제인 21-5008 호 (주)웰코멧아시아 · 관계 「원장 업체 표기 오류(확인된 관계 없음)」<br>메모: 역할: 제조사 WELLCOMET GmbH(Smart Tri 는 웰코멧아시아 제조 허가) · 수입사 (주)웰코멧아시아 · 판매사 웰코멧코리아<br>https://wellcometkorea.com/history<br>https://www.wellcometkorea.com/<br>http://www.wellcometasia.com/<br>https://www.wellcomet.de/ | `taxonomy` taxonomy 항목 auto-M16-1775363074847 $.modality[15].subcategories[6].items[5].detail |
| E7-007 | `auto-M4-1775361749536` | LG화학 · PN(폴리뉴클레오타이드) 기반 스킨부스터 | — | 인에이블은 동국제약이 2023-07 출시한 주름개선 기능성 화장품 — 원장의 「LG화학」은 웹 근거 없음(LG화학 스킨부스터는 비알팜 PN 「비타란」). 원장 성분 「PN 기반」도 웹(섬유아세포 엑소좀 · FGF · 콜라겐)과 다름 | product-master-draft.md ⑤ 「인에이블 = 동국제약 화장품(LG화학 아님)」 · 4차 웹: 제조 동국제약 · 구분 화장품 · 식약처 의료기기/의약품 DB 대상 아님 · 1차 검수 사용자 첨부: 섬유아세포 배양액 · 엑소좀 · HA · 성장인자<br>메모: 업체 「동국제약」으로 고치는 것과 별개로 화장품이라 원장(의료 시술 제품)에 둘지, 계열 PN/PDRN 을 고칠지도 정할 것<br>https://news.bizwatch.co.kr/article/mobile/2023/10/04/0034<br>https://medigatenews.com/news/865623860<br>https://kormedi.com/1787768/ | `taxonomy` taxonomy 항목 auto-M4-1775361749536 $.modality[3].subcategories[0].items[4].detail |
| E7-008 | `M7-3-3` | 리젠바이오텍 | 테스리프트 | TESSLIFT 제조업체는 주식회사 테스리프트(2008 설립 · 원주 생산, KMDF 업체 목록 등재) — 원장 「리젠바이오텍」과의 관계는 확인 못 함 | product-master-draft.md ⑤ 「테스리프트 = (주)테스리프트(리젠바이오텍 관계 미확인)」 · 4차 웹: 제조사 주식회사 테스리프트 (TESSLIFT Co.,Ltd.) · products.json manufacturer 「리젠바이오텍」 · taxonomy detail 에는 업체 없음<br>메모: 리젠바이오텍이 판매사일 가능성은 확인 안 됨 — 근거 없이 판매사로 넣지 않는다<br>https://app.rndcircle.io/company/bfd2c137-66e3-5b34-864d-97736b23fab9<br>https://www.onreyoung.com/products/24063<br>https://www.kmdf.org/portal/sub0301/file_down/id/1657<br>https://cm.imdad.com/Products/Tesslift | `products` products $.thread_lift.products[1].manufacturer (taxonomy 항목 M7-3-3 detail 「PDO+몰딩 메쉬」에는 업체 없음) |
| E7-009 | `auto-19-1774737181584` | 한스바이오파마 | 한스바이오메드 | 셀르디엠(CellREDM)은 한스바이오메드(주) 제품 — 「한스바이오파마」라는 회사 근거 없음. 국내 판권은 휴젤(2026-04 계약) | product-master-draft.md ⑤ 「셀르디엠 = 한스바이오메드(한스바이오파마 아님)」 · 4차 웹: 제조 한스바이오메드(주) · 판매 휴젤(주) / 민트메디컬<br>메모: 역할: 제조사 한스바이오메드(주) · 판매사 휴젤(주)(국내 판권). 인체조직(hADM) 가능성 — 의료기기 DB 밖<br>https://www.dt.co.kr<br>https://www.medipana.com<br>https://www.hitnews.co.kr<br>https://dailypharm.com/user/news/337064<br>https://www.mt.co.kr/stock/2026/09/11/2026091108453030666 | `taxonomy` taxonomy 항목 auto-19-1774737181584 $.modality[2].subcategories[5].items[2].detail |
| E7-010 | `auto-M1-1775364775103` | 대화제약 | — | 국내 보툴리눔 허가 60건 중 「퓨어녹스」 · 대화제약 제품이 없다. 원장의 「대화제약」은 같은 원장의 미라콜(대화제약 콜라겐)에서 섞인 것으로 보인다(추정) | product-master-draft.md ⑤ 「퓨어녹스의 「대화제약」은 미라콜(대화제약 콜라겐)에서 섞인 것으로 보임」 · 4차 웹: 대화제약 주사제 8건에도 톡신 없음 · 제품 자체 확인 불가<br>메모: 제품 정체부터 미상 — 바꿀 업체 값 없음. 데이터 관리자에게 원래 무엇을 적으려 했는지 확인 요청<br>https://nedrug.mfds.go.kr/searchDrug?itemName=보툴리눔 | `taxonomy` taxonomy 항목 auto-M1-1775364775103 $.modality[0].subcategories[1].items[13].detail |
| E7-011 | `auto-18-1774737181584` | 휴메딕스 | — | 리투오 파인(Re2O Fine)은 엘앤씨바이오가 제조하고 휴메딕스가 국내 판매 — 원장 「휴메딕스」는 판매사이지 제조사가 아니다 | product-master-draft.md ⑤ 「리투오파인 = 엘앤씨바이오(휴메딕스 아님)」 · 4차 웹: 제조 (주)엘앤씨바이오 · 국내 판매 (주)휴메딕스 · company-relation-check.json 리투오(본품)도 같은 관계<br>메모: 역할: 제조사 (주)엘앤씨바이오 · 판매사 (주)휴메딕스. 원장 칸이 한 칸이라 고칠 값은 역할 칸이 생긴 뒤 정할 것<br>https://biz.chosun.com<br>https://www.hitnews.co.kr<br>https://www.hankyung.com/article/202606257004P<br>https://m.dailypharm.com/user/news/343227 | `taxonomy` taxonomy 항목 auto-18-1774737181584 $.modality[2].subcategories[5].items[1].detail |
| E7-012 | `auto-M9-1775360627229` | 클래시스 · RF+HIFU 복합 | — | 튠페이스는 알마(Alma Lasers) Accent Prime 시술명 — 원장 업체 「클래시스」는 근거 없음. 현장 사진(DEV-032)도 Alma Accent Prime | product-master-draft.md §5 「튠페이스: maker_hint 클래시스는 오류 — 튠페이스는 알마 Accent Prime」 · 현장 사진 DEV-032 「Accent Prime · Alma」(partial · 중간 확신) · _RESUME 3차 「원천 업체 오기 지적 … 튠페이스=알마」<br>메모: 국내 수입사는 확인 안 됨 — 그래서 바꿀 값을 「알마」 한 칸으로 정하지 않았다<br>https://doctornow.co.kr/content/magazine/7b2234daa4ec4aeda7953a95227fae93<br>https://www.etoday.co.kr/news/view/1739349 | `taxonomy` taxonomy 항목 auto-M9-1775360627229 $.modality[8].subcategories[3].items[3].detail |
| E7-013 | `M11-1-1` | 사이노슈어(Cynosure) · 다양한 팁 | — | 포텐자 제조사는 (주)제이시스메디칼(국내 허가 · 판매) — 원장의 「사이노슈어」는 북미 판매 파트너다. 국내 판매사로서의 사이노슈어 근거는 없음 | company-relation-check.json 포텐자: 허가 제허 19-126 호 · 19-78 호 (주)제이시스메디칼 · 충돌 「원장은 사이노슈어를 업체로 적었으나 출처상 사이노슈어는 북미 판매 파트너」 · products.json 도 manufacturer 「사이노슈어」 · country US<br>메모: 조사 관계 분류는 「제조사 ≠ 판매사(판매 계약 — 북미)」로 이번 6건에는 없었으나 조사 미결 4 의 「원장 업체 표기를 고칠지」 목록에 있어 함께 올림. 역할: 제조사 (주)제이시스메디칼 · 판매사 국내 제이시스메디칼 / 북미 Cynosure<br>https://www.smarttoday.co.kr/ko-kr/articles/42188<br>https://www.smarttoday.co.kr/ko-kr/articles/38567 | `taxonomy · products` taxonomy 항목 M11-1-1 $.modality[10].subcategories[0].items[0].detail · products $.energy_device.products[7].manufacturer |

### E8 원장 이름 오기 — 6건

- **왜**: 원장 제품 이름이 정식 제품명과 글자가 달라 식약처 허가 · 웹 검색에 닿지 않는다(DEC 「원장 이름은 전부 동의어 · 오기는 원천 수정 목록」)
- **확인**: 고친 이름으로 식약처 · 원장 정규화 완전 일치 — 지금 0 (검증 코드 없음)
- **근거**: product-master-draft.md ⑤ · §5 · 4차 웹 · taxonomy-classify-v2 1차 검수 사용자 첨부 · company-relation-check.json
- **메모**: 「추정」 표시 항목은 웹 · 사진 근거뿐 — 데이터 관리자 확인 요청 대상

| id | 원장 | 현재 | 제안 | 왜 | 근거 · 출처 | 위치 |
|---|---|---|---|---|---|---|
| E8-001 | `M1-1-7` | 리즈톡신 | 리즈톡스 | 정식 제품명은 「리즈톡스」(휴온스바이오파마 보툴리눔 톡신 A형, 식약처 의약품) — 원장 「리즈톡신」으로는 허가 품목명에 닿지 않는다 | 1차 검수 사용자 첨부: 「리즈톡스(Liztox) … 공식 품목명 후보 「리즈톡스」(원천 이름 「리즈톡신」)」 · 식약처 후보: 리즈톡스주200단위 · (주)휴온스바이오파마 · 정상 · product-master-draft.md §5 「리즈톡신: 정식명 리즈톡스(주)」<br>https://dailypharm.com/user/news/50445<br>https://medigatenews.com/news/1846462372 | `taxonomy` taxonomy 항목 M1-1-7 $.modality[0].subcategories[1].items[7].name |
| E8-002 | `auto-M4-1775360463217` | 벨피엔 프로 | 밸피엔 | 휴메딕스 PN+HA 복합 필러의 정식 한글 표기는 「밸피엔」 — 「프로」 라인은 웹에서 확인 안 됨 | product-master-draft.md ⑤ 「벨피엔 프로 = 정식 표기 밸피엔(휴메딕스), 「프로」 라인 미확인」 · 4차 웹: official_ko 「밸피엔」 · 품목허가 신청 단계 보도<br>메모: 「프로」를 뗄지는 라인 확인 뒤 — 제안은 정식 표기만. 같은 오기: products $.skin_booster.products[4].name 「벨피엔」(name_en Belpien — 영문 철자도 미검증)<br>https://dailypharm.com/user/news/339507<br>https://medigatenews.com/news/1103940830<br>https://www.sidae.com/article/2025121909090946675<br>https://www.asiae.co.kr/article/2025121909593159533<br>https://www.asiatoday.co.kr/kn/view.php?key=20251219010010561 | `taxonomy` taxonomy 항목 auto-M4-1775360463217 $.modality[3].subcategories[3].items[2].name |
| E8-003 | `auto-M2-1775364775108` | 더채움프리미어 | 더채움 프리미엄 | 휴젤 더채움 라인은 Premium · Pure · Shape10 · Signature — 「프리미어」 라인명은 웹에서 확인 못 함. 표기 차이로 보이나 확인 안 됨 | company-relation-check.json 더채움프리미어: 「보도에 나오는 라인명은 「더채움 프리미엄」 — 원장 「프리미어」는 표기 차이로 보이나 확인 안 함」 · 3차 웹 official_en: The Chaeum Premium<br>메모: 추정 — 데이터 관리자 확인 요청<br>https://medigatenews.com/news/2630225735<br>https://www.smarttoday.co.kr/ko-kr/articles/109584<br>https://m.dailypharm.com/user/news/340605<br>https://m.dailypharm.com/user/news/35353<br>https://dailypharm.com/user/news/340605 | `taxonomy` taxonomy 항목 auto-M2-1775364775108 $.modality[1].subcategories[0].items[17].name |
| E8-004 | `auto-M8-1775364775128` | 포토나스타발브 | 포토나 스타워커 | 포토나 제품군에 「스타발브」가 없다(StarWalker · TimeWalker · SP Dynamis 등) — 「스타워커」 오기로 추정. 같은 원장에 「스타워커」가 따로 있어 중복 항목일 가능성 | product-master-draft.md ⑤ 「스타워커 ↔ 포토나스타발브(포토나에 스타발브 없음)」 · 4차 웹: 「포토나 「스타워커(StarWalker)」 오기로 추정」 · 현장 사진 DEV-066 「포토나스타워커」<br>메모: 추정 · 중복이면 고치기보다 원장 하나로 합칠 것(같은 원장 「스타워커」 auto-M8-1775364775120)<br>https://www.praiston.pl/en/catalog/view/12916/fotona-starwalker-m031-3a2-maqx-laser | `taxonomy` taxonomy 항목 auto-M8-1775364775128 $.modality[7].subcategories[5].items[9].name |
| E8-005 | `auto-M15-1775364775179` | 바이오프로톤 | 바이오포톤 | 「바이오프로톤」 그대로는 검색 0건 — (주)바이오포톤의 PDP 생육광선 온열돔 「바이오포톤」 오기로 추정 | product-master-draft.md 「바이오프로톤: 「바이오포톤」의 오기 추정」 · 4차 웹: official_ko 바이오포톤 · 제조 (주)바이오포톤 · 의료기기 허가 여부 미확인<br>메모: 추정 · 출처는 네이버 검색 결과 URL(원 페이지 아님)<br>https://search.naver.com/search.naver?query=주식회사+바이오포톤+의료기기+허가<br>https://search.naver.com/search.naver?query=바이오포톤+피부관리+기기 | `taxonomy` taxonomy 항목 auto-M15-1775364775179 $.modality[14].subcategories[2].items[6].name |
| E8-006 | `auto-49-1774737181584` | 아스트로더 | 아스트로돔 | 「아스트로더」로는 검색 0건 — 현장 사진의 「아스트로돔(우주인토닝) · AstrodomeFacial」과 같은 기기로 추정 | product-master-draft.md 「아스트로더: 「아스트로돔(AstrodomeFacial)」의 오기 추정」 · 현장 사진 DEV-046 read_model AstrodomeFacial · 파일명 아스트로돔(우주인토닝) · 사진 연결 메모 「같은 기기인지 확인 필요」<br>메모: 추정 · 출처는 네이버 검색 결과 URL(원 페이지 아님)<br>https://search.naver.com/search.naver?query=아스트로돔페이셜+공식+수입<br>https://search.naver.com/search.naver?query=아스트로돔+의료기기 | `taxonomy` taxonomy 항목 auto-49-1774737181584 $.modality[14].subcategories[2].items[2].name |

## 판정 방법

- 원천: 로컬 graph 발행본 v1 의 graph_validation_issue · graph_node · graph_edge 를 SELECT, A7 · B2 · B4 · E4 · E5 는 stg 저장본 JSON 을 직접 셈
- 정규화: `re.sub('[^0-9A-Za-z가-힣]+','',s).casefold() — SPEC-001 §3.3.1`
- proposed: 괄호 설명을 뺀 본문이 원장(시술 항목 · 시술군 · 제품) 이름과 정규화 완전 일치하고 하나로 정해질 때만. A1 은 사용자 결정 표기, A5 는 같은 CC 권장 시술명 중 포함 관계가 하나일 때
- candidates: 원장 실물에서 토큰(+ / or 또는 , · 괄호로 쪼갬) 완전 일치 > 접두 > 포함 순, 원천이 시술군을 주면 그 시술군 안 우선, 최대 3개. 의미 판단 없이 글자로만 뽑은 후보다

## 미결(이 목록이 정하지 않은 것)

- **B 전체 · C 전체 · E1 · E6** 는 의료 판단이 필요해 `proposed` 를 비웠다 — 무엇이 맞는지는 데이터 관리자(의료진) 몫
- **D 그룹**은 이름만 고쳐서 안 풀린다. 고민 어휘 정본(DEC OQ-104 · OQ-105) · 부위 정본(OQ-107) · 제품 원장 통합 여부가 먼저 정해져야 항목을 셀 수 있다
- **E2**(다른 고민 어휘 16)는 어휘 정본이 정해져야 고칠 이름이 정해진다. **E3** 는 SPEC OQ-S10(제품 노드 관계) 결정이 먼저다
- 괄호를 떼어 낸 `proposed`(예: 「필러 (동일 부위 재시술)」 → 「필러」)는 괄호 안 조건이 이름에서 빠진다 — 조건 칸으로 옮길지 확인 필요
- **A7 · B2 · B4 · E4 · E6** 는 그래프 검증 코드가 없어 이 목록의 셈 규칙으로 다시 세야 한다(고친 뒤 확인할 때 같은 규칙 필요)
- **E7** 에서 업체 값이 역할별로 갈리는 6건(LDM · 인에이블 · 퓨어녹스 · 리투오파인 · 튠페이스 · 포텐자)은 `proposed` 를 비웠다 — 원장 업체 칸이 한 칸이라 제조사 · 수입사 · 판매사 역할 칸이 생긴 뒤 고칠 값이 정해진다. 역할은 각 항목 메모 · `company-relation-decisions.json`
- **E7 에 넣지 않은 것**: 바이리즌 · 더채움 업체 칸의 「PCL」(업체가 아니라 성분 표기 오류 — 바이리즌은 HA) · 에스테필 「레지메드」(리젠바이오텍 표기인지 근거 없음) · 아테콜 · 라풀렌 · 디클래씨 성분 차이(업체 아님) — 넣을지 정할 것
- **E8 「추정」 4건**(더채움프리미어 · 포토나스타발브 · 바이오프로톤 · 아스트로더)은 웹 · 사진 근거뿐이다. 포토나스타발브는 고치기보다 원장 「스타워커」와 합칠 후보. 다복스 · 보리톡스 · 퓨어녹스 · 메테로 · 앨리필 등 「오기 추정」이지만 정식 이름을 못 찾은 것은 넣지 않았다(고칠 값 없음)
