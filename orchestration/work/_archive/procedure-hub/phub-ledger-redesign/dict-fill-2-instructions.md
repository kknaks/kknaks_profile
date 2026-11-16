# 지시서 — 사전 보강 2차(관계 후보 53) + 다시 잇기 + 관계 보완 판단 3

너는 이 작업의 맥락이 없다. 이 문서 한 장과 「읽을 것」만으로 일한다.
작업 레포(코디 워크트리): `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온` — 아래 상대 경로는 `orchestration/work/phub-ledger-redesign/silver-model/` 기준.

## 1. 배경

Procedure Hub 실버: ① 사전 → ② 시술 · 케이스 → ③ 관계(20표, 11-15 silver 반영 · 보완 완료). ③ 을 만들며 **사전에 없어 칸을 비워 둔 값**이 `notes/relation-dict-candidates.csv`(53 — 고민 · 효과 · 부작용 · 사람 조건 · 시술/케이스 · …)에 모였다. 이번 일: 사전에 넣고, 비워 둔 관계 칸을 다시 잇고, 관계 보완에서 남은 판단 3을 반영한다. 1차 사전 보강(`drafts/dict-fill/`)과 같은 방식이다.

## 2. 읽을 것

- `notes/relation-dict-candidates.csv` · `notes/relation-notes.md`(§4 입구 현황 · §7) · `notes/relation-judgment.csv` · `notes/relation-conflicts.csv` · `notes/relation-id-map.csv`
- `drafts/relation-gapfill/gapfill-notes.md`(§4 충돌 RCF-022~027 · §6 판단 3) · `drafts/relation-merge/` · 표 구조 정본 `drafts/relation-pilot/relation-notes.md` §9-2
- **1차 사전 보강 본보기**: `drafts/dict-fill/` 전부(notes · build · check — 처리 표 꼴 · 다시 잇기 · 검증 꼴)
- 사전 원칙: `drafts/concern/concern-notes.md` §7 · `drafts/effect/` · `drafts/adverse/` · `drafts/condition/` notes(3단 · 명사형 · 원장 인용 설명) · ② 규칙 `../combo-pilot-brief.md` §2
- `silver/` 전부 · 원장 `../../phub-recommend/bronze/phub-ledger/*.json`(확인용, 고치지 않음)

## 3. 사용자 결정 (11-15)

**A. 사전 보강 — 후보 53 전부 처리**(1차와 같은 규칙):
- 이미 있는 행과 같은 뜻이면 **alias**, 포함이면 **parent**, 새 개념이면 새 행. 고민 · 효과 · 부작용 · 사람 조건은 대 · 중 · 소 3단(모든 행 대분류 아래 · 깊이 ≤ 3) · 이름 명사형 일반 용어 · 괄호 금지 · 설명은 원장 문장 「」 글자 그대로(source_ref field = description) · 원장에 없는 영어는 보충 · **원장에 없는 임상 사실 금지 · 「드물게」 「얕게」를 수치로 바꾸지 않음** · 코드는 그 사전 다음 번호.
- 같은 말이 다른 사전에 있어도 쓰임이 다르면 별개 행(고민 vs 부작용 등 — 지금까지 원칙).
- 시술 / 케이스 후보는 ② 규칙대로(원장이 말한 조합만 · site 하나 · 이름은 원장이 붙인 것만 · description 원장 인용) `silver/procedure` · `procedure_material` · `procedure_case`(+ case_method · case_product)에 — 코드는 그 시술 범위 다음 번호.
- 넣지 않는 것은 행을 만들지 않고 notes 「넣지 않음」 표(후보 · 이유 · 원문).

**B. 다시 잇기**: 새 행 · alias 로 채울 수 있게 된 관계 칸만(후보를 낸 자리 — 「사전에 없어 비움」이라 적힌 칸 · 판정). 그 밖 빈칸은 건드리지 않는다. 계열 층 + note 로 둔 진술 중 새 케이스가 생긴 것은 그 케이스로 옮긴다.

**C. 관계 보완 판단 3**(gapfill-notes §6):
1. **하모니카**: PRD-114 HArmonyCa 합침(사용자 11-11 — 외부 조사 근거)은 유지. 원장 M2 필러 칸 하모니카 자리(「앨러간 · 신세대 Vycross HA」 · 「HA 필러 지속 6-18개월」 템플릿 등 — OUT-1594 · OUT-1598 · RCF-022 · 023 이 가리키는 자리)의 진술은 **PRD-114 에서 뗀다**: 관계 행을 지우고 판정을 「안 담음 — 원장 분류 의심(M2 칸 HA 문장 ↔ 사전 HArmonyCa CaHA+HA, 사용자 11-15)」으로. RCF-022 · 023 decision 에 적음. RCF-027(재시술 간격)도 M2 칸 쪽이면 같은 처리.
2. **동명이물 · 원장 오기 의심**: taxonomy `/modality/3/products/3`(M4 스킨부스터 제품 「스킨보톡스」 — 「아르기닌 함유 저분자 성장인자 복합체」) · `/modality/8/products/6`(M9 제품 「LDM」 — 「RF 기술 기반의 피부 리프팅 기기」)의 진술을 지금 대상(CAS-016 · PRD-442)에서 **뗀다**: 관계 행 삭제 · 판정 「안 담음 — 동명이물 · 원장 오기 의심(사용자 11-15)」 · RCF-024 · 025 · 026 decision 에 적음. 같은 두 자리를 가리키는 ② 판정(`notes/combo-item-judgment.csv`) · case_product · product_modality 연결이 있으면 목록만 notes 에(고치지 않음 — 원장 확인 목록 몫).
3. **미녹시딜 두피 메조 · 프로락틴주사 · 알렉스필**: 케이스 후보로 A 와 같이 처리(② 규칙 — 원장 문장으로 시술 · 케이스를 정할 수 있으면 만들고 계열 층 + note 진술을 옮김, 못 정하면 notes 이유).
- 1 · 2 로 뗀 자리는 `notes/ledger-check-list.csv`(새 파일 — 원장 작성자 확인 목록: source · pointer · name · 무엇이 이상한가 · 근거 문장)에 행으로.

## 4. 쓰기 규칙

- 고치기 전 `silver/` 전체 · 바꿀 notes 를 `archive/silver-before-dict-fill-2/` 에 복사.
- 사전 · ② · ③ 표는 행 덧붙임 / 빈칸 채움 / C 의 삭제 · 대상 이동만. 공통 alias · source_ref 는 덧붙임(앞쪽 행 바이트 그대로 — C 로 지운 관계 행의 근거 행만 예외로 지우고 목록을 notes 에).
- 스크립트 · notes 는 `drafts/dict-fill-2/`(`dict-fill-2-build.py` · `dict-fill-2-check.py` · `dict-fill-2-notes.md`). CSV UTF-8 BOM · `;` 칸 금지. 원장 변경 · 커밋 · push 금지.

## 5. 검증 (`dict-fill-2-check.py` — 코디가 다시 돌린다)

- 후보 53 전부 처리 표에 있음(새 행 / alias / parent / 넣지 않음 — 이유).
- 새 사전 행: 3단 규칙 · 이름 괄호 0 · `;` 0 · name_ko 중복 0 · 근거 ≥ 1 · description · 「」 인용 원장 글자 그대로 · 참조 존재. 새 시술 · 케이스: ② 검사(시술 정체 중복 0 · 케이스 조합 중복 0 · procedure_material ≥ 1).
- 다시 잇기 · C: 바뀐 칸 · 지운 행 · 옮긴 행 목록 = 실제 변경과 같음 · 그 밖 칸 불변 · ③ 검사 전부(참조 · 근거 · 원문 · 숫자 대조 · polarity) 갱신된 silver 에 대해 다시.
- 보존: 반영 전 사전 이름(name_ko ∪ alias) · 근거 ⊆ 후 · 지운 관계 행 = C 목록뿐.
- **입구 · 매핑 현황 전/후**(relation-notes §4 셈법): 고민 192 / 50 / 18 · 효과 · 부작용 · 사람 조건 쓰임 · 관계 있는 제품.
- `git status` 로 산출물 외 변경 없음.

## 6. notes (`drafts/dict-fill-2/dict-fill-2-notes.md`, 짧게)

1. 후보 53 처리 표 2. 다시 잇기 · C 반영 표 3. 입구 현황 전/후 4. 원장 확인 목록 새 행 요약 5. 사용자 판단이 필요한 것 — 원문 · 이유 · 추천 · 선택지 6. 검증 출력

## 7. 완료 보고

범위를 넓히지 않는다(새 관계 판정 · 외부 조사 하지 않음).
preamble 의 `worker_done` 을 정확히 한 번(`--outcome succeeded|failed`, `--report-path orchestration/work/phub-ledger-redesign/silver-model/drafts/dict-fill-2/dict-fill-2-notes.md`).
그다음:
`orca terminal send --terminal term_107c16b1-6066-4654-9272-359649efd67f --text "사전 보강 2차 완료: drafts/dict-fill-2/dict-fill-2-notes.md" --enter`
