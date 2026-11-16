# 지시서 — 상품 확정 · silver 반영

너는 이 작업의 맥락이 없다. 이 문서 한 장과 「읽을 것」만으로 일한다.
작업 레포(코디 워크트리): `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온` — 아래 상대 경로는 `orchestration/work/phub-ledger-redesign/silver-model/` 기준.

## 1. 배경

가격표(`market-pricing.json` 122행)로 상품 8표 설계안 · 시범을 `drafts/offer/` 에 만들었다(검증 PASS — `drafts/offer/offer-notes.md`). 사용자가 판단 11(같은 notes §6)을 모두 추천 (a)로 정했다. 이번 일: 반영해 silver 에 올린다.

## 2. 읽을 것

- `drafts/offer/` 전부(notes · build · check · CSV · offer-alias-candidates)
- `drafts/silver-check/`(silver-check.py · silver-schema.json) · `notes/silver-erd.md` · `notes/silver-tables.md`
- `notes/ledger-check-list.csv` · `notes/ledger-check-sheet.md`(원장 확인 목록 꼴)
- `notes/external-fill-notes.md` · `drafts/external-fill-3/`(큐어젯 식약처 근거 줄)
- `silver/` 전부 · 원장 `../../phub-recommend/bronze/phub-ledger/*.json`(확인용, 고치지 않음)

## 3. 사용자 결정 (11-16 「응」 — offer-notes §6 전부 (a))

1. 큐어젯 PRD-670 description 을 「분사식주사기 · 품목 분류 gas-powered」 사실로 고친다(식약처 제인22-4689호 — 외부 근거 표시 · source_ref). 원장 오류 의심 문장은 뺀다.
2. `offer.price_mid` = 원장 mid 그대로 · 뜻 「원장 mid(정의 없음 · 산술 중간값 아님) — 계산 · 정렬에 쓰지 않음」 을 표 사전에.
3. 「전체얼굴」 · 「풀페이스」 · 「안면」 = SITE-007(text 원문 그대로).
4. 「볼륨」 = 고민 CON-273.
5. 원장 카테고리 이름 3개(M5 「PRP/엑소좀」 · M9 「에너지기기(HIFU/RF)」 · M12 「마이크로니들링(MTS)」)를 modality alias 로(kind 는 기존 alias kind 값 중 원장 항목 이름에 맞는 것 · 괄호 규칙은 alias 검사 기준에 맞게 — 걸리면 notes). 근거 = market-pricing 카테고리 포인터.
6. 「수입」 · 「국산」 = `offer.product_origin` 칸.
7. 「양쪽」 · 「부위/1회」 = 수량 원문 그대로.
8. 「바디」 · 「간해독」 = 코드 빈칸 + 원문.
9. 근사 연결 4 그대로.
10. ② 판정과 다른 2곳(제네시스 CAS-023 만 · MTS + PRP 에 PRC-116) 시범대로 · combo-item-judgment 는 안 고침.
11. silver 반영: 상품 8표(price_list · offer · offer_item · offer_quantity · offer_site · offer_concern · offer_effect · offer_material)를 `silver/` 에 · 근거는 공통 `source_ref.csv` 에 덧붙임(offer_source_ref → 같은 꼴) · offer-alias-candidates 5 를 공통 `alias.csv` 에 덧붙임(대상 = 그 제품 · 시술 · 케이스 행, 근거 포함).
- 추가: **못 닿은 상품 18**(offer-notes §5)을 `notes/ledger-check-list.csv` 에 행 덧붙임(category 「9 가격표 — 무엇을 파는지 미표기」 · 묶음은 이유별 · question 원장 작성자에게 물을 한 문장 · silver_now = OFR 코드) · `ledger-check-sheet.md` 요약 · 묶음 표 갱신. 앞쪽 바이트 그대로 · 덧붙임만.

## 4. 쓰기 규칙

- 고치기 전 `silver/` 전체 · 바꿀 notes 를 `archive/silver-before-offer/` 에 복사.
- silver: 새 표 8 · PRD-670 description · alias / source_ref 끝 덧붙임 · modality alias 3. 그 밖 바이트 불변(앞쪽 행 바이트 그대로).
- `drafts/silver-check/silver-schema.json` · `silver-check.py` 에 상품 8표(FK · 다형 target · 원문 · 숫자 대조 · 근거 ≥ 1) 추가 → `--write-docs` 로 `notes/silver-erd.md`(상품 층 다이어그램 추가) · `notes/silver-tables.md` 갱신.
- 스크립트 · notes: `drafts/offer/offer-finalize-build.py` · `offer-finalize-notes.md`. CSV UTF-8 BOM · `;` 금지. 원장 변경 · 커밋 · push 금지.

## 5. 검증 (코디가 다시 돌린다)

- `python3 drafts/silver-check/silver-check.py` → PASS(상품 8표 포함 55표).
- `python3 drafts/offer/offer-check.py` → 반영 뒤 silver 기준으로도 PASS(필요하면 경로만 갱신).
- 변경 목록 = 실제 silver diff · 기존 47표 중 바뀐 것 = product(PRD-670) · alias · source_ref 뿐 · `git status` 산출물 외 변경 없음.

## 6. notes (`drafts/offer/offer-finalize-notes.md`, 짧게)

1. 판단 11 반영 표 2. silver 반영(표 · 행 수) 3. 원장 확인 목록 덧붙임 4. 사용자 판단이 필요한 것(새로 나온 것만) 5. 검증 출력

## 7. 완료 보고

범위를 넓히지 않는다(시술 · 케이스 새로 만들지 않음 · 외부 조사 하지 않음 · 못 닿은 18 채우지 않음).
preamble 의 `worker_done` 을 정확히 한 번(`--outcome succeeded|failed`, `--report-path orchestration/work/phub-ledger-redesign/silver-model/drafts/offer/offer-finalize-notes.md`).
그다음:
`orca terminal send --terminal term_107c16b1-6066-4654-9272-359649efd67f --text "상품 silver 반영 완료: drafts/offer/offer-finalize-notes.md" --enter`
