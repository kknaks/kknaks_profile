# 지시서 — 외부 조사 결과 반영(제품 사실) + silver 고치기 판단 7

너는 이 작업의 맥락이 없다. 이 문서 한 장과 「읽을 것」만으로 일한다.
작업 레포(코디 워크트리): `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온` — 아래 상대 경로는 `orchestration/work/phub-ledger-redesign/silver-model/` 기준.

## 1. 배경

silver 는 원장 21개만으로 만들었고, 원장에 말이 없거나 엇갈린 자리 303행을 `notes/ledger-check-list.csv`(원장 확인 목록 · 37묶음)로 모았다. 사용자가 그 목록으로 외부 조사를 시켰고 결과가 `drafts/external-research/external-research.csv`(448줄 · id 210 · 칸 id · group · name · answer · answer_type(확인 / 추정 / 못 찾음 / 원장 작성자 확인 필요) · source_url · source_title · source_quote · confidence · searched · note)에 있다. 조사자 자기 검토: 「확인」 164줄 중 128줄은 출처를 다시 받아 인용 글자 대조 일치 · 35줄은 식약처 검색 표 칸 값(상세 주소 없음 — 6건만 재조회 일치) · 1줄(Nokor 니들) 대조 못 함 · note 가 「원장 오류 의심」 으로 시작하는 줄 99(id 78).
이번 일: **제품 사실만** silver 에 외부 근거로 반영하고, 나머지는 원장 확인 목록에 붙인다. 그리고 silver 고치기에서 남은 판단 7 을 반영한다.

## 2. 읽을 것

- `drafts/external-research/external-research.csv` 전부 · `notes/ledger-check-list.csv` · `notes/ledger-check-sheet.md`
- 제품 사전 규칙 · 외부 근거 선례: `notes/product-notes.md` · `product-v4-notes.md` · `product-v5-notes.md` · `product-research.csv` · `mfds-fill-notes.md` · `mfds-fill.csv` · `product-ledger-check-list.csv` · `split-notes.md` · `../_RESUME.md` 11-11 줄(올리지오 = 원텍 · HArmonyCa · 잼버실 · 인모드FX · 울트라V 결정)
- `drafts/silver-fix/silver-fix-notes.md`(§4 칸 29 뜻 초안 · §5 판단 7) · `drafts/silver-check/`(silver-check.py · silver-schema.json · 알려진 예외) · `notes/silver-tables.md` · `notes/silver-erd.md`
- `silver/` 전부 · 원장 `../../phub-recommend/bronze/phub-ledger/*.json`(확인용, 고치지 않음)

## 3. 사용자 결정 (11-15 「그렇게 해」)

**A. silver 에 넣는 것 = 제품 사실 「확인」 줄만**
- 대상 칸: 제품의 회사(organization · product_organization) · 허가명 · 공식명(alias — 이름 자체는 기존 규칙대로) · 재질 · 성분(product_material, `source` = 외부 조사) · 방식 · 계열(product_method · product_modality) · kind · country · 그 밖 product 칸. 사전 행이 없는 회사는 organization 새 행(기존 규칙 — 이름 · country 근거 있는 것만).
- 넣는 줄: answer_type = 확인 이고 **인용 대조 일치한 줄**. 식약처 표 줄(대조 못 한 30줄)은 **네가 식약처(의료기기 전자민원 · 의약품안전나라)를 다시 조회**해 맞는 것만 넣는다. 다시 조회해도 못 맞추면 넣지 않고 「추정」 처럼 다룬다. 테스리프트 허가번호(제허17-128호 ↔ 제허18-377호)도 여기서 가림.
- 근거: 모든 바뀐 칸 · 새 행에 source_ref 덧붙임 — 외부 근거 표기는 기존 선례(product-research · mfds-fill 의 ref 꼴)를 따르고, external-research.csv 줄을 가리킬 수 있게(줄 번호 또는 id+순번) · URL 은 그 CSV 에. 원장 근거와 섞이지 않게.
- **원장 ≠ 외부 확인(원장 오류 의심)인 제품 사실**: 외부 확인 값을 silver 에, 원장 값은 `notes/product-ledger-check-list.csv` 가 아닌 새 notes 표(아래 §4)에 「원장 오류 의심」 으로 남김(11-11 올리지오와 같은 처리). 원장 근거 행은 지우지 않는다.
- **예전 결정과 다른 근거 2건**: 멜스몬 「HCl 가수분해」(원장 표기가 맞다는 근거) → 「근거 못 찾음」 기록이 있는 notes 를 고치지 말고 새 notes 에 정정으로 적고, silver 에 빠진 값이 있으면 채움 · 울트라V PDO(미스코 「울트라V-lift」 제허13-1398호) → 지웠던 재질 연결을 되살림(외부 근거).

**B. silver 에 넣지 않는 것**
- 「추정」 · 「못 찾음」 · 「원장 작성자 확인 필요」 줄 전부.
- 제품 사실이 아닌 「확인」 줄: 시술 정체(ACR 등 G16~G22 · G29) · 고민 · 적응 · 효과(G12~G15 · G37) · 원장 엇갈림 · 뜻(G01~G09) · 해부 · 고민 이름(G35 · G36). **관계(적응 · 효과 · 부작용 · 금기) 행을 외부 근거로 만들지 않는다.** 시술 · 케이스를 새로 만들지 않는다.
- 떼어 둔 하모니카 · LDM · 스킨보톡스 진술 42행은 다시 붙이지 않는다(원장 4판 대기).
- 이것들은 원장 확인 목록에 붙인다: `notes/ledger-check-list.csv` 에 칸 덧붙임 — `ext_type`(그 id 줄 중 가장 강한 판정) · `ext_answer`(요약 한 줄) · `ext_lines`(external-research.csv 줄 번호들) · `ext_silver`(silver 에 넣었음 / 안 넣음 — 이유). 앞쪽 칸 · 행 바이트 그대로 · 칸 덧붙임만.

**C. silver 고치기 판단 7 = 추천대로**
1. 띄어쓰기 별칭 남길 쪽 = 지금 기본값 그대로.
2. M12 「MTS」 alias 근거를 `extracted.json:/M12/name` 으로(지금 overview 근거 행을 바꿈).
3. `*_qualifier` 한 칸 그대로(범위 · 어림 수식 모두 원문 낱말).
4. 값 0 칸 2개 그대로.
5. 뜻 갈림 5칸 = 「원장 원문 등급 · 구분 낱말」 로 뜻 하나 · `package_item.step` = 「package.kind 가 연간 플랜이면 달(1~12), 그 밖은 순서 번호」. `notes/silver-tables.md` 의 29칸 「(초안)」 을 확정 뜻으로(표시 뗌).
6. 지운 별칭이 설명에 남은 14행 그대로.
7. PRD-684 kind 빈칸 그대로 + 원장 확인 목록에 행 덧붙임(외부 조사 Nokor 줄이 있으면 ext 칸에).

## 4. 쓰기 규칙

- 고치기 전 `silver/` 전체 · 바꿀 notes 를 `archive/silver-before-external-fill/` 에 복사.
- silver: 칸 값 채움 · 바꿈 · 행 덧붙임(A · C 만). alias · source_ref 는 앞쪽 행 바이트 그대로 + 끝에 덧붙임(C-2 의 한 행 바꿈만 예외).
- 새 notes: `notes/external-fill-notes.md`(반영 표 · 원장 오류 의심 표 · 정정 2건) · 변경 목록 `drafts/external-fill/external-fill-changes.csv`.
- 스크립트: `drafts/external-fill/`(`external-fill-build.py` · `external-fill-check.py`). `drafts/silver-check/silver-check.py` 는 외부 근거 ref 를 받도록만 갱신(기존 기준 유지).
- CSV UTF-8 BOM · `;` 금지. 원장 · external-research.csv 변경 금지 · 커밋 · push 금지.

## 5. 검증 (코디가 다시 돌린다)

- `python3 drafts/silver-check/silver-check.py` → PASS.
- `external-fill-check.py`: 넣은 줄 전부 = A 조건(확인 · 대조 일치 또는 재조회 일치 · 제품 사실) · 넣지 않은 「확인」 줄 = B 이유와 함께 목록 · 바뀐 칸 · 새 행마다 외부 근거 ≥ 1 · 원장 근거 행 줄어들지 않음(C-2 한 행 바꿈 빼고) · 변경 목록 = 실제 silver diff · 관계 표(③ 20표) · procedure · procedure_case 바이트 불변 · ledger-check-list 앞쪽 바이트 그대로 · 210 id 전부 ext 칸 있음.
- 식약처 재조회 결과 표(제품 · 검색어 · 결과 · 맞음/틀림).
- `git status` 로 산출물 외 변경 없음.

## 6. notes (`drafts/external-fill/external-fill-notes.md`, 짧게)

1. 반영 수(표별 · 칸별) 2. 식약처 재조회 표 3. 원장 오류 의심 → silver 값 바뀐 것 4. 넣지 않은 「확인」 줄 수 · 이유 5. 판단 7 반영 6. 남은 빈칸 셈(통합 검사 §4 셈법 전/후) 7. 사용자 판단이 필요한 것(새로 나온 것만) 8. 검증 출력

## 7. 완료 보고

범위를 넓히지 않는다(관계 행 · 시술 · 케이스 새로 만들지 않음 · 추정 넣지 않음 · 새 외부 조사는 식약처 재조회만).
preamble 의 `worker_done` 을 정확히 한 번(`--outcome succeeded|failed`, `--report-path orchestration/work/phub-ledger-redesign/silver-model/drafts/external-fill/external-fill-notes.md`).
그다음:
`orca terminal send --terminal term_107c16b1-6066-4654-9272-359649efd67f --text "외부 조사 반영 완료: drafts/external-fill/external-fill-notes.md" --enter`
