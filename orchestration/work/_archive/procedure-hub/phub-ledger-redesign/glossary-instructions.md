# 지시서 — 같은 날 판정 3 반영 + 용어집 · 값 목록 + 외부 코드 연결 표 설계

너는 이 작업의 맥락이 없다. 이 문서 한 장과 「읽을 것」만으로 일한다.
작업 레포(코디 워크트리): `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온` — 아래 상대 경로는 `orchestration/work/phub-ledger-redesign/silver-model/` 기준.

## 1. 배경

Procedure Hub silver 56표 · gold 15표(`gold/`)가 완성됐다(silver-check PASS(WARN 0) · gold-check PASS · 구조 문제 0). 마감 전에 (A) 같은 날 판정 3을 반영하고, (B) 흩어진 공통 용어 정의를 한 장의 용어집 · 값 목록으로 모으고, (C) 나중에 외부 표준 코드와 잇기 위한 연결 표를 설계(빈 표)한다.

## 2. 읽을 것

- `gold/` 전부(README · semantic-map.md · gold-final-notes.md · gold-build.py · gold-check.py) · `notes/same-day-judgment.csv`
- `notes/silver-tables.md` · `notes/silver-erd.md` · `drafts/silver-check/`(silver-schema.json · silver-check.py)
- 사전 원칙: `drafts/concern/concern-notes.md` §7 · `drafts/effect/` · `drafts/adverse/` · `drafts/condition/` notes · `notes/atoms-notes.md` · `../_RESUME.md` 「목표 참고 문서 §1~5」 · 결정 표
- `silver/` 전부

## 3. 사용자 결정 (11-16 「응 추천이랑 이거 까지 반영해서」)

**A. 같은 날 판정 3**(`gold/gold-final-notes.md` §5):
1. 「위험」 으로만 말한 5행(PRL-0003 · 0004 · 0019 · 0020 · 0656) = 불가 그대로.
2. 원장 칸 이름 `incompatible_same_day` 만인 4행(PRL-0034 · 0666 · 0834 · 0835) = 불가 그대로.
3. 「같은 날 불가」 갈래인데 빈칸인 3행(PRL-0884 · 0885 · 0886 「PDO+비가교HA 병용 금기」) = **불가로 채움**(2 와 같은 기준 — 원장 분류를 근거로). `same_day_text` = 원장 갈래 표기 그대로 · 근거 source_ref(field=same_day_text) = 그 갈래 포인터. `notes/same-day-judgment.csv` 해당 행 갱신(판정 · 이유 「원장 갈래 같은 날 불가(사용자 11-16)」).
- 고치기 전 `silver/` · `gold/` · `notes/same-day-judgment.csv` 를 `archive/silver-before-glossary/` 에 복사. silver 변경 = procedure_relation 3행 칸 2 + source_ref 덧붙임뿐. gold 는 `gold-build.py` 로 다시 빌드.

**B. 용어집 · 값 목록**(새 조사 없이 있는 것을 모음 — 지어 쓰지 않음):
1. `notes/glossary.md` — 한 장 용어집. 층(① 사전 · ② 조합 · ③ 관계 · 상품 · gold)별로 **개념 · 관계 용어마다**: 용어(한국어 · 영어) · 뜻(semantic-map · silver-tables · notes · 결정에 적힌 문장에서 — 출처 링크) · silver 표 · 코드 접두(CON- · PRC- …) · 헷갈리기 쉬운 짝과 구분(보완 ≠ 같은 날 가능 · 시술 ≠ 케이스 ≠ 제품 ≠ 상품 · 고민 ≠ 효과 ≠ 부작용 · 부위 역할 · 시간 역할 · 빈도 수치 ≠ 서술 등급 · 원장/외부 확인/사용자 제공 · 패키지 ≠ 상품 …). 정의가 어디에도 없으면 「(정의 없음)」 으로 두고 목록.
2. `notes/vocabulary.csv` — **고정 값 목록**(칸 · 값 · 뜻 · 출처): silver · gold 의 모든 고정 값 칸(polarity · same_day · kind 류 · target_table · alias.kind · source_ref 근거 종류 · name_check · product.kind · package.kind · offer 단위 · rating_scale …)을 silver-schema 에서 전수로 뽑아 실제 들어 있는 값 전부 · 각 값의 뜻. 뜻이 적힌 데 없으면 빈칸 + 목록.
3. `silver-check.py` 에 검사 추가: 고정 값 칸의 실제 값 ⊆ vocabulary.csv(새 값이 생기면 FAIL).

**C. 외부 표준 코드 연결 표 — 설계만(빈 표)**:
- 새 표 `silver/external_code.csv`(id · target_table · target_code · system · code · label · relation(같음 / 넓음 / 좁음 / 가까움) · note) — **헤더만, 행 0**. system 후보(KCD · ICD-10 · SNOMED CT · 식약처 의료기기 품목코드 · 의약품 성분코드 · UMLS 등)와 어느 사전에 어느 system 이 맞는지 표를 `notes/glossary.md` 끝 「외부 코드 매핑(나중)」 에. 채우지 않는다(외부 조사 · 연결할 상대 시스템이 정해질 때).
- silver-schema · silver-check · `--write-docs`(silver-erd · silver-tables) 에 반영.

## 4. 쓰기 규칙

- silver 변경 = A 3행 · source_ref 덧붙임 · 새 빈 표 external_code. 그 밖 바이트 불변.
- 스크립트 · notes: `drafts/glossary/`(`glossary-build.py` — vocabulary 뽑기 · `glossary-notes.md`). CSV UTF-8 BOM · `;` 금지. 원장 변경 · 커밋 · push 금지.
- `gold/README.md` 에 용어집 · 값 목록 링크 한 줄.

## 5. 검증 (코디가 다시 돌린다)

- `python3 drafts/silver-check/silver-check.py` → PASS(WARN 0) · 새 검사(고정 값 ⊆ vocabulary) 포함 · 음성 시험(값 하나 바꾼 사본 → FAIL).
- `python3 gold/gold-check.py` → PASS · 구조 문제 0.
- silver diff = A · external_code 뿐 · `git status` 산출물 외 변경 없음.

## 6. notes (`drafts/glossary/glossary-notes.md`, 짧게)

1. A 반영 2. 용어집 셈(용어 수 · 「(정의 없음)」 목록) 3. 값 목록 셈(칸 수 · 값 수 · 뜻 빈칸 목록) 4. external_code 설계 5. 사용자 판단이 필요한 것(새로 나온 것만) 6. 검증 출력

## 7. 완료 보고

범위를 넓히지 않는다(외부 코드 채우지 않음 · 새 판정 · 외부 조사 하지 않음).
preamble 의 `worker_done` 을 정확히 한 번(`--outcome succeeded|failed`, `--report-path orchestration/work/phub-ledger-redesign/silver-model/drafts/glossary/glossary-notes.md`).
그다음:
`orca terminal send --terminal term_107c16b1-6066-4654-9272-359649efd67f --text "용어집 · 같은 날 3 완료: drafts/glossary/glossary-notes.md" --enter`
