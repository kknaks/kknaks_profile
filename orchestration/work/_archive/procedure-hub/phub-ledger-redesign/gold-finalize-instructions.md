# 지시서 — silver 보강 2(같은 날 · 제품 ↔ 시술) + gold 확정

너는 이 작업의 맥락이 없다. 이 문서 한 장과 「읽을 것」만으로 일한다.
작업 레포(코디 워크트리): `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온` — 아래 상대 경로는 `orchestration/work/phub-ledger-redesign/silver-model/` 기준.

## 1. 배경

gold 설계안 · 질문 시범(`drafts/gold/` — gold-check PASS · 구조 문제 0 · 질문 35 중 32 답함)을 만들었다. 사용자가 판단 6(`drafts/gold/gold-notes.md` §6)을 정했다. 이번 일: silver 를 두 군데 보강하고, gold 를 다시 빌드해 확정 자리에 둔다.

## 2. 읽을 것

- `drafts/gold/` 전부(gold-notes · semantic-map.md · gold-build.py · gold-check.py · questions.csv)
- `drafts/silver-check/`(silver-check.py · silver-schema.json) · `notes/silver-erd.md` · `notes/silver-tables.md`
- `notes/combo-item-judgment.csv`(② 판정 — 제품 → 시술) · `notes/combo-notes.md` · `drafts/relation-pilot/relation-notes.md` §9-2 · `notes/relation-judgment.csv`
- `silver/` 전부 · 원장 `../../phub-recommend/bronze/phub-ledger/*.json`(확인용, 고치지 않음)

## 3. 사용자 결정 (11-16 「응!!」)

1. **같은 날 칸 — silver 보강**: `procedure_relation` 에 칸 `same_day`(값 3: 가능 / 불가 / 조건부 + 빈칸) 와 `same_day_text`(판정에 쓴 원문 조각). 원문 글자가 같은 날 시행을 말할 때만 채운다(「같은 날 가능」 · 「같은 날 시술 가능」 · 「당일 병행」 · 「같은 날 금지」 · 「같은 날 … 경우」 등 — 실제 원문을 전수 grep 해 낱말 목록과 판정 표를 notes 에). 원문이 말하지 않으면 빈칸(보완 관계라고 같은 날 가능으로 채우지 않음 — 「보완 ≠ 같은 날 가능」). 패키지 kind 「같은 날 조합」 은 package 칸이 이미 말하므로 procedure_relation 에 복사하지 않고 semantic-map 에 조회 경로로만.
2. **물려받지 않음**: 상위 제품(parent_code) 진술은 하위 제품에 물려주지 않음 — 지금대로. semantic-map 에 규칙으로 적음.
3. **제품 ↔ 시술 연결 표 — silver 보강**: 새 표 `product_procedure`(id · product_code · procedure_code · note) — `notes/combo-item-judgment.csv` 에서 제품이 케이스 없이 시술까지 닿은 판정(약 81 제품)을 그대로. 근거 = 그 판정의 원장 포인터(source_ref). case_product 로 이미 케이스에 닿은 제품은 넣지 않는다(케이스 → 시술로 조회됨). 셈을 notes 에.
4. **저장소 = 관계형 먼저 + 그래프 내보내기**: gold 는 관계형 표(CSV) + `g_node` / `g_edge` 내보내기 그대로. DB 로 올리는 일은 이번 범위 아님.
5. **문헌 gold 표는 나중**: 이번엔 만들지 않음.
6. **근거 표 참조로**: `g_evidence` 를 펼친 복사 대신 gold 행 → (silver_table, silver_id) 참조로 바꾼다. silver source_ref 로 되짚는 조회 규칙을 semantic-map 에. 근거 종류(evidence_kind) 칸은 gold 행에 남김.

## 4. 할 일 · 쓰기 규칙

- 고치기 전 `silver/` 전체 · `drafts/gold/` 를 `archive/silver-before-gold-final/` 에 복사.
- silver: `procedure_relation` 칸 2 추가(기존 칸 · 행 값 그대로) · 새 표 `product_procedure` · source_ref 끝 덧붙임. 그 밖 바이트 불변. `silver-schema.json` · `silver-check.py` 에 반영 → `--write-docs` 로 `notes/silver-erd.md` · `silver-tables.md` 갱신 → **silver-check PASS(WARN 0)**.
- gold: `gold-build.py` 를 갱신(같은 날 칸 · product_procedure 물려받기 경로 · 근거 참조)해 **확정 자리 `silver-model/gold/`** 에 gold 표 CSV 를 쓴다. 스크립트 · semantic-map · questions 는 `silver-model/gold/` 옆 정본으로(`gold/README.md` — 표 목록 · 빌드 방법 · 검사 방법 · 조회 규칙 요약). `drafts/gold/` 는 지우지 않는다.
- 질문 시범 다시: 35 질문 + 같은 날 질문 · 보톡스 제품 → 보톡스 시술 질문을 더해 다시 답함. 구조 문제 0.
- notes: `gold/gold-final-notes.md`. CSV UTF-8 BOM · `;` 금지. 원장 변경 · 커밋 · push 금지.

## 5. 검증 (코디가 다시 돌린다)

- `python3 drafts/silver-check/silver-check.py` → PASS(WARN 0) · silver 바뀐 것 = procedure_relation(칸 2) · product_procedure(새) · source_ref 뿐.
- `gold/gold-check.py` → PASS · 구조 문제 0 · 재빌드 해시 같음 · gold 값 = silver 되짚어짐 · 질문 시범 결과 표.
- `git status` 산출물 외 변경 없음.

## 6. notes (`gold/gold-final-notes.md`, 짧게)

1. 같은 날 판정(낱말 목록 · 값별 수 · 예) 2. product_procedure(수 · 보톡스 제품 → 시술 닿음 전/후) 3. gold 표 · 행 수 · 근거 참조 크기 전/후 4. 질문 시범 결과(전/후) 5. 사용자 판단이 필요한 것(새로 나온 것만) 6. 검증 출력

## 7. 완료 보고

범위를 넓히지 않는다(다른 silver 변경 · 외부 조사 · DB · 화면 하지 않음).
preamble 의 `worker_done` 을 정확히 한 번(`--outcome succeeded|failed`, `--report-path orchestration/work/phub-ledger-redesign/silver-model/gold/gold-final-notes.md`).
그다음:
`orca terminal send --terminal term_107c16b1-6066-4654-9272-359649efd67f --text "silver 보강 · gold 확정 완료: silver-model/gold/gold-final-notes.md" --enter`
