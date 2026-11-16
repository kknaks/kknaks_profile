# 발주서 — 상품(market-pricing) 설계안 + 시범 · 큐어젯 고압 공기 연결 되살림

너는 이 작업의 맥락이 없다. 이 문서 한 장과 「읽을 것」만으로 일한다.
작업 레포(코디 워크트리): `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온` — 아래 상대 경로는 `orchestration/work/phub-ledger-redesign/silver-model/` 기준.

## 1. 배경

Procedure Hub silver(① 사전 22표 · ② 시술 138 · 케이스 268 · ③ 관계 20표 · 47표 통합 검사 PASS)를 원장 21개로 만들었다. 남은 원장 하나가 가격표 `market-pricing.json`(약 122행)이다. 이번 일: **상품 표 설계안을 만들고 시범으로 검증한다.** silver 에는 아직 올리지 않는다(사용자 확인 뒤). 그 전에 작은 silver 고침 하나(A)를 먼저 한다.

## 2. 읽을 것

- 원장 `../../phub-recommend/bronze/phub-ledger/market-pricing.json` 전부(+ README · CHANGELOG — 확인용, 고치지 않음)
- 1차 조사 결과 `../first-pass/market-pricing/` 전부(읽기 전용)
- 상품 관련 사용자 결정: `../_RESUME.md` 결정 표 11-10 줄들(「상품 = 제품 · 시술 + 수량(샷 · cc · 줄 · 회) + 가격(병원 무관, 예: 써마지 300샷)」 · 「패키지는 상품 아님 = 시너지」 · 「피부과 메뉴 이름은 범위 밖」) · 11-14 「가격표로 케이스 안 만듦」 · 11-16 「원장이 틀릴 수 있다. silver 만 제대로 들어가면 된다」
- silver 구조: `notes/silver-erd.md` · `notes/silver-tables.md` · `drafts/silver-check/`(silver-check.py · silver-schema.json) · `notes/combo-item-judgment.csv`(가격표 자리 판정이 있으면) · `notes/relation-judgment.csv`
- 설계 원칙 선례: `drafts/relation-pilot/relation-notes.md` §9-2(정규화 — 값 하나면 칸, 여럿이거나 척도 다르면 표) · `../combo-pilot-brief.md` §2
- 외부 근거 꼴: `drafts/external-fill-3/` · `notes/external-fill-notes.md`

## 3. 사용자 결정

**A. 큐어젯 고압 공기 연결 되살림(11-16 「응」)**: external-fill-2 에서 뗀 PRD-670 큐어젯의 PMAT-0353(고압 공기) 연결을 되살린다. 근거 = 원장 원래 포인터 + 식약처 품목 분류 「Injector, medication/vaccine, needleless, gas-powered」(제인22-4689호 — `drafts/external-fill-3/` 재조회 줄). `notes/external-fill-notes.md` 「원장 오류 의심 — 뗀 연결」 표의 그 행에 「정정 — 되살림(11-16)」 덧붙임. 고치기 전 `silver/` 를 `archive/silver-before-offer-a/` 에 복사 · 그 밖 silver 바이트 불변 · `silver-check.py` PASS.

**B. 상품 설계안(drafts 만 — silver 변경 금지)**
- 가격표 행을 **전부** 값으로 쪼갠다: 행마다 이름 · 무엇을 파는가(시술 · 케이스 · 제품 · 여러 개 묶음) · 수량(샷 · cc · 줄 · 회 · 부위 · 바이알 …) · 가격(최소 · 최대 · 대표값 · 통화 · 원문) · 부위 · 조건 · 그 밖 칸. 원장 글자 그대로 · 숫자는 원문에 있을 때만.
- 그 값으로 표를 설계한다(사용자 결정 기준): 상품 = 시술/케이스/제품 + 수량 + 가격, 병원 무관. 상품이 가리키는 대상은 silver 코드(procedure · procedure_case · product · package)로 — 못 닿으면 이유. 수량 단위 · 가격 범위처럼 여러 값이거나 척도가 다르면 표, 하나면 칸. 공통 alias · source_ref 꼴 그대로.
- **담을 칸 없는 값 0** 이 기준. 못 담으면 판단 목록.
- 가격표에서 시술 · 케이스를 새로 만들지 않는다(11-14). 가격표에만 있는 시술 이름은 「못 닿음 — 이유」 로.
- 원장끼리 · silver 와 어긋나는 값(제품 이름 · 회사 등)은 silver 값을 따르고 「원장 오류 의심」 목록.

**C. 시범**: 설계 표로 가격표 행 **전부**를 drafts 에 채운다(`drafts/offer/` 에 CSV). 연결 현황: 상품 → 시술 · 케이스 · 제품에 닿은 수 · 못 닿은 수와 이유.

## 4. 쓰기 규칙

- A 만 silver 변경. B · C 는 `drafts/offer/`(`offer-build.py` · `offer-check.py` · `offer-notes.md` · 표 CSV). CSV UTF-8 BOM · `;` 금지. 원장 · first-pass 변경 금지 · 커밋 · push 금지.

## 5. 검증 (코디가 다시 돌린다)

- A: `python3 drafts/silver-check/silver-check.py` PASS · silver 변경 = PMAT-0353 행 + 근거 행뿐(archive 대비).
- `offer-check.py`: 가격표 행 전부 판정(상품 행 또는 「안 담음 — 이유」) · 원장 글자 그대로 · 숫자 대조 · silver 코드 참조 존재 · 담을 칸 없는 값 0(또는 판단 목록과 같음) · `;` 0 · `git status` 산출물 외 변경 없음.

## 6. notes (`drafts/offer/offer-notes.md`, 짧게)

1. A 결과 2. 가격표 값 쪼개기 요약(칸 종류 · 수량 단위 종류 · 가격 꼴) 3. **설계안 — 표 · 칸 · FK · 근거**(mermaid erDiagram 포함) 4. 시범 결과 · 연결 현황 5. 원장 오류 의심 · 못 닿음 목록 6. 사용자 판단이 필요한 것 — 원문 · 이유 · 추천 · 선택지 7. 검증 출력

## 7. 완료 보고

범위를 넓히지 않는다(silver 에 상품 올리지 않음 · 시술 · 케이스 새로 만들지 않음 · 외부 조사 하지 않음).
preamble 의 `worker_done` 을 정확히 한 번(`--outcome succeeded|failed`, `--report-path orchestration/work/phub-ledger-redesign/silver-model/drafts/offer/offer-notes.md`).
그다음:
`orca terminal send --terminal term_107c16b1-6066-4654-9272-359649efd67f --text "상품 설계안 · 시범 완료: drafts/offer/offer-notes.md" --enter`
