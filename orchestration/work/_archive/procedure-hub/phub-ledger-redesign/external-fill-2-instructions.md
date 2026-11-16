# 지시서 — 원장 오류 값 연결 떼기 5 + 아발란체 정체 조사 · 반영

너는 이 작업의 맥락이 없다. 이 문서 한 장과 「읽을 것」만으로 일한다.
작업 레포(코디 워크트리): `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온` — 아래 상대 경로는 `orchestration/work/phub-ledger-redesign/silver-model/` 기준.

## 1. 배경

외부 조사 결과(`drafts/external-research/external-research.csv`) 중 제품 사실 「확인」을 silver 에 반영했다(`drafts/external-fill/` · `notes/external-fill-notes.md`). 남은 판단 2(`drafts/external-fill/external-fill-notes.md` §7)를 사용자가 정했다.
**사용자 원칙(11-16): 「원장이 틀릴 수 있다. silver 만 제대로 들어가면 된다.」** — 제품 사실은 공식 출처로 확인된 값이 silver 에 들어가고, 틀린 원장 값은 silver 연결에서 빠지되 notes 에 「원장 오류 의심」 으로 남는다.

## 2. 읽을 것

- `drafts/external-fill/` 전부(notes §3 · §7 · build · check · changes · external-fill-lines.csv) · `notes/external-fill-notes.md`
- `drafts/external-research/external-research.csv` 의 아발란체 줄 전부 · `notes/ledger-check-list.csv` 아발란체 행
- `notes/product-notes.md` · `product-research.csv` · `mfds-fill.csv`(외부 근거 꼴) · `drafts/silver-check/`
- `silver/` 전부 · 원장 `../../phub-recommend/bronze/phub-ledger/*.json` 의 아발란체 자리 전부(grep — 확인용, 고치지 않음)

## 3. 사용자 결정 (11-16)

**A. 원장 값 연결 떼기 5**: 릴리이드M 펩타이드 PMAT-0100 · 테스리프트 PCL PMAT-0121 · 테스리프트 브랜드 리젠바이오텍 PORG-0213 · 아발란체 532nm PMAT-0190(B 결과에 따라 — 아래) · 큐어젯 고압 공기 PMAT-0353. 연결 행을 silver 에서 지우고, 그 행의 원장 근거 행(source_ref)도 같이 지운다 — 지운 연결 · 근거 행은 전부 `notes/external-fill-notes.md` 끝 「원장 오류 의심 — 뗀 연결」 표에 원래 값 · 원장 포인터 · 원문 · 외부 근거 줄과 함께(값이 사라지지 않게). 해피리프트 PLLA PMAT-0126 은 그대로(외부 출처끼리 엇갈림).

**B. 아발란체 정체 조사 → 반영**
- 조사: 원장이 말하는 「아발란체」(원장 문장 · 회사 · 파장 · 용도 전부 모아서)가 실제 어떤 장비인가. 후보: Fotona 「AvalancheLase」 계열 · 그 밖 같은 이름 장비. 확인할 것 = 제조사 · 국내 허가(식약처 의료기기 — 허가번호 · 품목명 · 수입사) · 레이저 종류 · 파장 · 용도. 출처 우선 = 식약처 · 제조사 공식 · FDA 510(k) > 학술 > 병원 · 기사. 인용은 출처 글자 그대로 · URL.
- 판정: 원장 아발란체 = 그 장비라고 볼 근거(국내 시판명 · 원장의 회사 · 용도 일치)가 있으면 **silver 를 그 장비 사실로 맞춘다**(name_en · 회사 · 파장 재료 연결 · description — 외부 근거). 원장 값 중 틀린 것(파장 · 회사)은 A 처럼 연결을 떼고 notes 에. 근거가 부족해 정체를 못 가리면 지금 붙인 755nm 연결과 name_en 을 떼고 원장 확인 목록 아발란체 행 ext 칸에 조사 결과를 적는다.
- 조사 결과 표를 notes 에(출처 · 인용 · 판정).

## 4. 쓰기 규칙

- 고치기 전 `silver/` 전체 · 바꿀 notes 를 `archive/silver-before-external-fill-2/` 에 복사.
- silver: A · B 의 행 지움 · 덧붙임 · 칸 바꿈만. alias · source_ref 는 지우는 행 말고 앞쪽 행 바이트 그대로 + 끝 덧붙임. ③ 관계 20표 · procedure · procedure_case 바이트 불변.
- 스크립트 · notes: `drafts/external-fill-2/`(`external-fill-2-build.py` · `external-fill-2-check.py` · `external-fill-2-notes.md`). CSV UTF-8 BOM · `;` 금지. 원장 · external-research.csv 변경 금지 · 커밋 · push 금지.

## 5. 검증 (코디가 다시 돌린다)

- `python3 drafts/silver-check/silver-check.py` → PASS.
- `external-fill-2-check.py`: 지운 행 = A · B 목록뿐 · 지운 값 전부 notes 표에 있음 · 새 값 외부 근거 ≥ 1 · 변경 목록 = 실제 diff · ③ · 시술 · 케이스 바이트 불변 · `git status` 산출물 외 변경 없음.

## 6. notes (`drafts/external-fill-2/external-fill-2-notes.md`, 짧게)

1. A 뗀 연결 표 2. 아발란체 조사 결과(출처 · 인용 · 판정) 3. silver 변경 4. 사용자 판단이 필요한 것(새로 나온 것만) 5. 검증 출력

## 7. 완료 보고

범위를 넓히지 않는다(다른 제품 조사 · 관계 · 시술 · 케이스 변경 하지 않음).
preamble 의 `worker_done` 을 정확히 한 번(`--outcome succeeded|failed`, `--report-path orchestration/work/phub-ledger-redesign/silver-model/drafts/external-fill-2/external-fill-2-notes.md`).
그다음:
`orca terminal send --terminal term_107c16b1-6066-4654-9272-359649efd67f --text "원장 오류 연결 · 아발란체 완료: drafts/external-fill-2/external-fill-2-notes.md" --enter`
