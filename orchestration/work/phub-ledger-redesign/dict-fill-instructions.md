# 지시서 — 사전 보강 54 + 다시 잇기 + 합치기 판단 4

너는 이 작업의 맥락이 없다. 이 문서 한 장과 「읽을 것」만으로 일한다.
작업 레포(코디 워크트리): `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온` — 아래 상대 경로는 `orchestration/work/phub-ledger-redesign/silver-model/` 기준.

## 1. 배경

Procedure Hub 실버: ① 기본 단위 사전(silver 22표) → ② 조합(시술 134 · 케이스 259 — 11-14 silver 에 합침). ② 를 만들며 **사전에 없어 칸을 비워 둔 값** 54개가 `notes/combo-dict-candidates.csv` 에 모였다. 이번 일: 그 값을 사전에 넣고, 비워 둔 칸을 다시 잇는다.

## 2. 읽을 것

- `notes/combo-dict-candidates.csv`(54 — dictionary · name · drafts · source · reason) · `notes/combo-notes.md`(§4 매핑 현황 · §5 판단) · `notes/combo-item-judgment.csv`
- `silver/` 전부 — 각 사전의 칸 형식 · 코드 매김 · 공통 `alias.csv`(target_table · target_code · name · kind: 별칭/약어/의학 용어) · `source_ref.csv`(target_table · target_id · field · ref)
- 사전 원칙 · 형식 참고: `drafts/<material|method|site|product|…>/` 의 notes · build 스크립트 · `notes/atoms-notes.md` · `notes/method-notes.md` · `notes/site-finalize-notes.md` · `notes/product-notes.md`
- 각 후보를 낸 초안 notes: `archive/combo-drafts-before-merge/` (combo · combo-a · combo-b · combo-c)
- 원장 `../../phub-recommend/bronze/phub-ledger/*.json`(확인용, 고치지 않음)

## 3. 사용자 결정 (11-14 「추천대로」)

**A. 사전 보강 — 후보 54 전부 처리.** 후보마다 원장 문장을 다시 읽고:
- **이미 있는 행과 같은 뜻이면 새 행이 아니라 alias**(예: 부위 콧대 → 기존 코등 행의 별칭 · 이중턱 → 턱밑 별칭 · 자갈턱 · 잇몸미소 — 초안 reason 참고, 원장으로 확인). 포함 관계면 parent. 같은 뜻 · 포함 판단 근거는 notes 표.
- 새 행은 그 사전의 칸 · 원칙 그대로: 이름 = 명사형 일반 용어(원장 다른 표기 · 한자어는 alias) · **이름 괄호 금지**(「코그(톱니) 형태」 → 이름 + alias) · 설명은 원장 문장 근거(「」 인용 글자 그대로, source_ref field = description) · 원장에 없는 영어는 보충 · **원장에 없는 임상 사실 금지 · 「드물게」 「얕게」를 수치로 바꾸지 않음** · 코드는 그 사전의 다음 번호.
- 기전 13: 원장이 「원리」로 쓴 말만(수액 · 필링 · 실 · 장비 문장). 효과 · 결과(「피부가 밝아진다」)는 기전이 아니다 — 기전이 아니면 행을 만들지 말고 「넣지 않음」 표.
- 방법 13: 「코그 형태」 「모노 형태」를 넣어도 **실 시술 종류 구조(재질 × 원리)는 바꾸지 않는다**(사용자 11-14) — 케이스의 case_method 로만 쓴다. 「저출력」 같은 정도 수식어가 방법이 아니면 「넣지 않음」 표.
- 제품 10: product 칸 그대로(name_check · kind · country · mfds 는 원장 · 기존 판단 방식대로, 모르면 빈칸). product_modality · product_material 은 원장이 말한 것만. 회사(organization)를 원장이 말하지 않으면 잇지 말고 `notes/product-ledger-check-list.csv` 에 행 덧붙임(기존 행 바이트 그대로). 「리쥬란힐러」처럼 기존 제품의 다른 이름이면 alias.
- material_spec 1(HIFU 깊이): 원장 수치 그대로(material_spec 칸 형식).
- **넣지 않는 것**은 행을 만들지 않고 notes 「넣지 않음」 표(후보 · 이유 · 원문).

**B. 다시 잇기** — 새 행 · alias 가 생겨 채울 수 있게 된 칸을 채운다:
- `procedure.mechanism_code` 빈칸 20 · `procedure_material`(사전에 없어 빠졌던 성분) · `procedure_case` 의 tissue · material · site 빈칸 · `case_method` · `case_product`(새 제품) — **후보를 낸 초안 notes 가 「사전에 없어 비움」이라 적은 자리만.** 그 밖의 빈칸(원장이 말하지 않아 빈 것)은 건드리지 않는다.
- 판정 행(`notes/combo-item-judgment.csv`)에서 「사전에 없어」 코드를 비운 것은 코드를 채운다(GPC주사 — 콩 추출물 등). 판정 값을 바꿔야 하면(보류 → 시술 종류) 근거와 함께 표.
- 이으면서 시술 정체 중복(같은 계열 · 재료 집합 · 원리) · 케이스 조합 중복이 생기면 판단 목록(합치지 않음).

**C. 합치기 판단 4** (`notes/combo-notes.md` §5 · 끝 참고):
1. 두피 메조테라피 4자리 = 그대로.
2. **엑소좀 두피주사 → CAS-1037 · 두피 PRP → CAS-1028 로 잇는다**(판정 「케이스」 + 코드, 근거 원장 자리).
3. 「병합」 언급 8행 = 그대로.
4. **PRC-004 박피 레이저 name_en_source 「원장」 → 「보충」.**

## 4. 쓰기 규칙

- 고치기 전 `silver/` 전체를 `archive/silver-before-dict-fill/` 에, 바꿀 notes 파일을 `archive/notes-before-dict-fill/` 에 복사.
- 사전 표 · 관계 표는 행 덧붙임 / 빈칸 채움만(기존 값 바꿈은 C-4 하나와 판단 목록에 올린 것뿐). 공통 alias · source_ref 는 덧붙임(앞쪽 행 바이트 그대로).
- 스크립트 · 작업 notes 는 `drafts/dict-fill/`(`dict-fill-build.py` · `dict-fill-check.py` · `dict-fill-notes.md`). CSV 는 UTF-8 BOM · `;` 칸 금지. 원장 변경 금지 · 커밋 · push 금지.

## 5. 검증 (`dict-fill-check.py` — 코디가 다시 돌린다)

- 후보 54 전부 처리 표에 있음(새 행 / alias / parent / 넣지 않음 — 이유).
- 새 사전 행: 이름 괄호 0 · `;` 0 · name_ko 중복 0(사전 안) · 근거 ≥ 1 · description 있음 · 「」 인용 원장 글자 그대로 · 참조 존재.
- 다시 잇기: 채운 칸 목록(표 · 행 · 칸 · 새 값 · 근거) = 실제 바뀐 칸과 같음 · 그 밖 칸 불변 · 시술 정체 중복 0 · 케이스 조합 중복 0 · 전체 참조 존재.
- 보존: 반영 전 행 · 이름(name_ko ∪ alias) · 근거 ⊆ 후 · 바꾼 기존 값 = C-4 + 판단 목록만.
- **매핑 현황 다시 집계**(합치기 notes §4 와 같은 셈법, 전/후 숫자): 원리 빈 시술 · 대상 빈 케이스 · 제품 케이스까지 / 시술까지만 / 안 닿음 · 보류.
- `git status` 로 산출물 외 변경 없음.

## 6. notes (`drafts/dict-fill/dict-fill-notes.md`, 짧게)

1. 후보 54 처리 표(사전 · 후보 · 처리 · 새 코드 또는 기존 코드 · 근거)
2. 다시 잇기 표 · C 반영
3. 매핑 현황 전/후
4. 사용자 판단이 필요한 것 — 원문 · 이유 · 추천 · 선택지
5. 검증 출력

## 7. 완료 보고

범위를 넓히지 않는다(새 판정 · ③ 관계 · 외부 조사 하지 않음).
preamble 의 `worker_done` 을 정확히 한 번(`--outcome succeeded|failed`, `--report-path orchestration/work/phub-ledger-redesign/silver-model/drafts/dict-fill/dict-fill-notes.md`).
그다음:
`orca terminal send --terminal term_107c16b1-6066-4654-9272-359649efd67f --text "사전 보강 완료: silver-model/drafts/dict-fill/dict-fill-notes.md" --enter`
