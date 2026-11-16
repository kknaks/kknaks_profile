# 지시서 — 원장 확인 목록 한 장

너는 이 작업의 맥락이 없다. 이 문서 한 장과 「읽을 것」만으로 일한다.
작업 레포(코디 워크트리): `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온` — 아래 상대 경로는 `orchestration/work/phub-ledger-redesign/silver-model/` 기준.

## 1. 배경

Procedure Hub 실버(① 사전 · ② 시술/케이스 · ③ 관계)를 원장 21개(브론즈)로 만들었다. 원장에 말이 없거나 서로 엇갈려 **비워 두거나 보류하거나 뗀 자리**가 여러 notes 에 흩어져 있다. 이번 일: 그것을 **원장 작성자가 한 번에 보고 답할 수 있는 목록 한 장**으로 모은다. 답이 오면(원장 4판 또는 「사용자 제공」 근거) 다음 판에 채운다. **silver 는 고치지 않는다.**

## 2. 읽을 것

- `notes/ledger-check-list.csv`(LCK-001~003 · 칸 id · source · pointer · name · what · evidence) — 이 파일이 한 장의 바탕
- 기존 확인 목록(읽기 전용 — 고치지 않고 행을 가져와 출처 표시): `notes/product-ledger-check-list.csv` · `notes/concern-ledger-check-list.csv` · `notes/site-ledger-check-list.csv`
- `notes/relation-notes.md` §4(안 닿는 고민 18 · 계열 층만 50) · `drafts/dict-fill-2/dict-fill-2-notes.md` §3 · §5 · `drafts/dict-fill/dict-fill-notes.md`(보류 5 · 원리 빈 시술) · `notes/combo-notes.md` · `drafts/combo-merge/`(제품 → 케이스 못 닿음 · 보류) · `notes/combo-item-judgment.csv` · `notes/relation-judgment.csv` · `notes/relation-conflicts.csv`
- `notes/product-notes.md` · `product-v5-notes.md` · `site-finalize-notes.md` · `drafts/concern/concern-notes.md` · `drafts/effect/effect-notes.md` · `drafts/combo-c/combo-c-notes.md`
- `silver/` 전부 · 원장 `../../phub-recommend/bronze/phub-ledger/*.json`(확인용, 고치지 않음)

## 3. 사용자 결정 (11-15 「다음 단계 진행해」 — 사전 보강 2차 판단 6 은 모두 추천 (a))

**A. 한 장에 넣는 것 — 전수.** 아래 목록은 출발점이다. `notes/` · `drafts/` 를 「원장 확인」 「오기 의심」 「원장 오류」 「보류」 「동명이물」 「엇갈」 로 grep 해 **빠진 자리가 없게** 모은다(어디서 찾았는지 notes 에).
1. 기존 LCK-001~003(하모니카 M2 · 스킨보톡스 M4 제품 · LDM M9 제품)
2. 프로락틴주사 PRC-560 — 이름 · 기전 「프로락틴」 ↔ detail · overview 「프로작」
3. 뜻 불명 3 — 「경미한 결막」(피코슈어) · 「신경 과민」(DNA리셋프로그램) · 「눈가 가늘어짐」(PRD-153)
4. 안 닿는 고민 18 · 계열 층 적응만 있는 고민 50 — 고민마다 원장 어디에 나오는지(포인터)와 왜 시술 · 케이스까지 못 가는지. **대분류 고민(CON-235 · 274 · 277 · 278 · 280 등)처럼 설계상 안 닿는 것은 「원장 확인 아님」으로 따로 표시**하고 목록 질문에서 뺀다.
5. 보류(ACR · 두피스케일링 · 모발이식 등 — dict-fill notes 의 보류 전부) · ② 코드 없는 시술 종류(모노 · 볼륨실 등 계열 층 + note 로 둔 것 전부)
6. 원장 ≠ 사전 제품(인모드FX 「RF 니들」 ↔ 비침습 · 잼버실 PCA ↔ PDO · 올리지오 제조사 등 notes 에 적힌 것 전부) · 제품 → 케이스 못 닿음 · 원리 빈 시술
7. 기존 확인 목록 3개의 행(product 68 · concern 4 · site 2) — 가져와 `origin` 칸에 원래 파일 · 행 표시
8. 판단 6-2 의 목표 말 적응 13(간 해독 등) — 「원장에 상태 말 없음」 한 묶음으로

**B. 칸**: 기존 칸에 덧붙여 `category`(위 1~8 꼴 이름) · `group`(묶음 id) · `question`(원장 작성자에게 물을 한 문장 — 원장 말만 근거로, 우리 추측 답을 적지 않음) · `silver_now`(지금 silver 에 어떻게 두었나 — 코드 · 빈칸 · 뗌) · `origin` · `check_by`(값 2개: `원장 작성자` / `외부 확인 후보` — 제품 회사 · 허가 · 재질처럼 원장 밖 공개 자료로 확인할 수 있는 제품 사실만 후보. 임상 사실은 후보 아님). **외부 조사는 하지 않는다** — 칸만 표시.

**C. 사람 몫**: 행은 많아도 된다. 같은 꼴은 `group` 으로 묶어 **원장 작성자가 답할 질문 묶음이 50개 안쪽**이 되게 한다(예: 「대분류 고민 5 — 원장 확인 아님」 은 질문 0). 묶음 수가 50 을 넘으면 넘는 대로 두고 notes 에 이유.

## 4. 쓰기 규칙

- 고치기 전 `notes/ledger-check-list.csv` 를 `archive/ledger-check-before-sheet/` 에 복사.
- `notes/ledger-check-list.csv` 는 **LCK-001~003 앞쪽 행 바이트 그대로 · 칸 덧붙임과 행 덧붙임만**(기존 행의 새 칸은 채움). id 는 LCK-004 부터.
- 사람이 읽을 한 장: `notes/ledger-check-sheet.md` — 묶음별 표(묶음 · 질문 · 행 수 · 예시 원문 · check_by) · 맨 위 요약 수(묶음 수 · 행 수 · 원장 작성자 / 외부 확인 후보 / 원장 확인 아님).
- 스크립트 · notes 는 `drafts/ledger-check/`(`ledger-check-build.py` · `ledger-check-check.py` · `ledger-check-notes.md`). CSV UTF-8 BOM · `;` 칸 금지 · 원문 인용은 원장 글자 그대로 「」.
- **silver · 기존 확인 목록 3개 · 그 밖 notes · 원장 변경 금지.** 커밋 · push 금지.

## 5. 검증 (`ledger-check-check.py` — 코디가 다시 돌린다)

- §3-A 1~8 전부 행으로 있음(셈 표: 출처별 기대 수 = 들어간 수) · grep 으로 찾은 자리 전부가 행 또는 notes 「넣지 않음 — 이유」.
- 모든 행: pointer 가 원장에 있음(JSON 포인터 해석) · evidence 「」 인용이 그 원장 글자 그대로 · silver_now 의 코드가 silver 에 있음 · check_by 값 2개 밖 0 · `;` 0.
- LCK-001~003 앞쪽 바이트 그대로 · silver/ · 기존 확인 목록 3개 · 원장 바이트 불변(`git status` · 해시).
- 묶음 수 · 행 수가 sheet.md 요약과 같음.

## 6. notes (`drafts/ledger-check/ledger-check-notes.md`, 짧게)

1. 출처별 셈 표 2. grep 으로 더 찾은 자리 3. 묶음 목록(수) 4. 사용자 판단이 필요한 것 — 원문 · 이유 · 추천 · 선택지(새로 나온 것만) 5. 검증 출력

## 7. 완료 보고

범위를 넓히지 않는다(silver 수정 · 새 관계 판정 · 외부 조사 하지 않음).
preamble 의 `worker_done` 을 정확히 한 번(`--outcome succeeded|failed`, `--report-path orchestration/work/phub-ledger-redesign/silver-model/drafts/ledger-check/ledger-check-notes.md`).
그다음:
`orca terminal send --terminal term_107c16b1-6066-4654-9272-359649efd67f --text "원장 확인 목록 완료: drafts/ledger-check/ledger-check-notes.md" --enter`
