# 지시서 — 아발란체 색소 관계 떼기 · 큐어젯 설명 · 클라리티2 · 아포지엘리트플러스 조사 반영

너는 이 작업의 맥락이 없다. 이 문서 한 장과 「읽을 것」만으로 일한다.
작업 레포(코디 워크트리): `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온` — 아래 상대 경로는 `orchestration/work/phub-ledger-redesign/silver-model/` 기준.

## 1. 배경

직전 작업(`drafts/external-fill-2/external-fill-2-notes.md`)에서 원장 「아발란체」 = Fotona AvalancheLase(식약처 수허25-7호 · 755 + 1064nm · 제모)로 확인해 silver 제품 사실을 맞췄다. 남은 판단 3(같은 notes §4)을 사용자가 정했다.
**사용자 원칙(11-16): 「원장이 틀릴 수 있다. silver 만 제대로 들어가면 된다.」** — 공식 출처로 확인된 사실과 어긋나는 원장 진술 · 값은 silver 에서 떼고 notes 에 「원장 오류 의심」 으로 남긴다(값이 사라지지 않게).

## 2. 읽을 것

- `drafts/external-fill-2/` 전부 · `drafts/external-fill/` · `notes/external-fill-notes.md` · `drafts/external-research/external-research.csv`(큐어젯 · 클라리티2 · 아포지엘리트플러스 줄)
- 관계 떼기 선례: `drafts/dict-fill-2/`(하모니카 · 스킨보톡스 · LDM 진술 뗀 방식 — 관계 행 삭제 · 근거 행 삭제 · `notes/relation-judgment.csv` 판정 바꿈 · `notes/ledger-check-list.csv`)
- `drafts/silver-check/` · `silver/` 전부 · 원장 `../../phub-recommend/bronze/phub-ledger/*.json`(확인용, 고치지 않음)

## 3. 사용자 결정 (11-16 「추천으로 가자」)

**A. 아발란체 PRD-332 관계 행**: notes §4-1 의 IND-1193~1197 · OUT-1130 을 한 행씩 본다. **색소 관련(기미 · 주근깨 · 문신 · 색소 제거 효과 등)은 뗀다.** **혈관 병변은 남긴다**(FDA K223540 1064nm 용도와 맞음 — 근거 줄을 notes 에). 포트와인 등 애매한 행은 FDA 용도 문구와 글자로 맞는지로 가르고 이유를 적는다. 떼는 방식 = dict-fill-2 선례(관계 행 삭제 · 그 근거 행 삭제 · relation-judgment 판정 「안 담음 — 원장 오류 의심(실제 장비 = 제모 · 외부 확인, 사용자 11-16)」 · 뗀 행 원래 값 notes 표). 이 제품에 붙은 다른 관계 표(adverse_risk · outcome 등) 행도 같은 532nm 색소 문장에서 온 것이면 같은 처리 — 목록 전부 notes 에.

**B. 큐어젯 PRD-670 설명**: 원장 문장 「공기압 약물 주입 장비」 를 식약처 확인 사실로 바꾼다(제인22-4689호 · 분사식주사기 · Curejet · 바즈바이오메딕 — external-fill 재조회 결과). description 에 외부 근거 표시 · source_ref. 출처가 말하지 않는 방식(솔레노이드 등)은 쓰지 않는다.

**C. 클라리티2 · 아포지엘리트플러스**(원장 제모 묶음 · 「532+1064nm」 꼴): 아발란체와 같은 방식으로 조사한다 — 원장 자리 · 문장 전부 → 식약처(의료기기 품목 · 허가번호 · 수입사 · 모델) · 제조사 공식 · FDA 510(k) → 실제 장비 · 파장 · 용도 판정. 확인되면 silver 제품 사실(name_en · 회사 · 파장 재료 연결 · description · name_check)을 맞추고, 틀린 원장 값 연결은 떼고, 그 제품의 관계 행 중 실제 장비와 어긋나는 진술은 A 와 같은 기준으로 뗀다. 정체를 못 가리면 silver 를 바꾸지 않고 원장 확인 목록 행 ext 칸에 조사 결과.

## 4. 쓰기 규칙

- 고치기 전 `silver/` 전체 · 바꿀 notes(relation-judgment · ledger-check-list · external-fill-notes) 를 `archive/silver-before-external-fill-3/` 에 복사.
- silver: 위 행 지움 · 칸 바꿈 · 덧붙임만. alias · source_ref 는 지우는 행 말고 앞쪽 행 바이트 그대로 + 끝 덧붙임. procedure · procedure_case 바이트 불변 · ③ 표는 A · C 로 지우는 행만.
- notes 는 앞쪽 바이트 그대로 + 덧붙임(relation-judgment 판정 칸 바꿈만 예외 — 목록을 notes 에).
- 스크립트 · notes: `drafts/external-fill-3/`(`external-fill-3-build.py` · `external-fill-3-check.py` · `external-fill-3-notes.md`). CSV UTF-8 BOM · `;` 금지. 원장 · external-research.csv 변경 금지 · 커밋 · push 금지.

## 5. 검증 (코디가 다시 돌린다)

- `python3 drafts/silver-check/silver-check.py` → PASS.
- `external-fill-3-check.py`: 지운 행 = A · C 목록뿐 · 지운 값 전부 notes 표에 · 새 값 외부 근거 ≥ 1 · 변경 목록 = 실제 diff · 시술 · 케이스 바이트 불변 · 입구 현황(고민 192 / 50 / 18 등) 전/후 셈 · `git status` 산출물 외 변경 없음.

## 6. notes (`drafts/external-fill-3/external-fill-3-notes.md`, 짧게)

1. A 관계 행 판정 표(행 · 원문 · 뗌/남김 · 이유) 2. B 큐어젯 3. C 조사 결과(출처 · 인용 · 판정) · silver 변경 4. 입구 현황 전/후 5. 사용자 판단이 필요한 것(새로 나온 것만) 6. 검증 출력

## 7. 완료 보고

범위를 넓히지 않는다(다른 제품 조사 · 시술 · 케이스 변경 하지 않음).
preamble 의 `worker_done` 을 정확히 한 번(`--outcome succeeded|failed`, `--report-path orchestration/work/phub-ledger-redesign/silver-model/drafts/external-fill-3/external-fill-3-notes.md`).
그다음:
`orca terminal send --terminal term_107c16b1-6066-4654-9272-359649efd67f --text "아발란체 관계 · 큐어젯 · 클라리티2 · 아포지 완료: drafts/external-fill-3/external-fill-3-notes.md" --enter`
