# 발주서 — ③ 관계 시범: 보톡스(M1) · 필러(M2)

너는 이 작업의 맥락이 없다. 이 문서 한 장과 「읽을 것」만으로 일한다.
작업 레포(코디 워크트리): `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온` — 아래 상대 경로는 `orchestration/work/` 기준.

## 1. 목표 · 구조

Procedure Hub 는 **시술 원장**이다. 실버 3층: ① 기본 단위 사전(확정) → ② 조합(확정 — 시술 136 · 케이스 261, `phub-ledger-redesign/silver-model/silver/` procedure · procedure_material · procedure_case · case_method · case_product) → **③ 관계(이번)**.
③ 은 원장이 시술에 대해 하는 말을 사전 코드로 잇는 층이다: 어떤 고민에 쓰나(적응) · 무엇이 언제 얼마나 좋아지나(효과) · 무슨 부작용이 얼마나 · 언제 · 어디에(부작용 위험) · 누구에게 안 되나(금기 · 주의) · 다른 시술과 어떻게 엮이나(시술 간 관계 · 패키지) · 무슨 문헌이 받치나(근거).

이번은 **시범: M1 보톡스 · M2 필러** 의 관계 전부. 검수 뒤 나머지 계열을 같은 규칙으로 한다. 기준은 **「담을 칸이 없는 원장 값 0」** — 원장 값을 표에 맞추려 버리거나 바꾸지 않는다.

## 2. 사용자 결정 (바꾸지 않는다)

1. **붙는 자리 = 원장이 말한 층.** 관계 행은 `target_table`(modality / procedure / procedure_case) + `target_code` 로 계열 · 시술 · 케이스 어디에든 붙는다. 원장이 계열 단위로 말하면(complications 의 M1 묶음 등) 계열에, 케이스를 말하면 케이스에. **아래로 복사하지 않는다**(물려받기는 조회 때 계산). 같은 값을 원장이 자식 층에서 따로 말하면 그 자리에 행 + 근거.
2. **시점 · 기간 · 빈도 · 간격 = 원문 + 나눈 값.** 칸 꼴: `*_text`(원문 글자 그대로) · `*_min` · `*_max` · `*_unit` · `*_qualifier`(대부분 · 약 · 이상 · 이내 …) · 필요하면 `*_from`(기준점: 시술 후 / 발현 후 / 시술 전). **숫자는 원문에 숫자가 있을 때만.** 「드물게」 「수일」 「얕게」를 숫자로 바꾸지 않는다 — 빈도는 `grade_text`(서술 등급 원문)에.
3. **빈도 = 수치와 서술 등급을 함께, 서로 바꾸지 않는다**(지난 시범 D2). 한 부작용에 측정이 여럿이면 `adverse_frequency` 여러 행(분모 · 대상이 다르면 그대로).
4. **원장끼리 값이 다를 때 = 그 주제의 전용 원장을 채택**, 나머지는 같은 행의 근거로만(source_ref). 부작용 = complications.json · 금기 = contraindications.json(+ consent) · 시술 간 간격 = contraindications rules / treatment-sequence · 효과 시점 = taxonomy · extracted onset_duration. 채택 못 가르는 충돌은 `relation-conflicts.csv`(사용자 판단). taxonomy · 제품의 safety `common` / `serious` 키는 빈도 근거가 아니다(지난 시범 D6) — 원문 수식(「드물게」 「일시적」)만 쓴다.
5. **패키지 = 시너지 데이터**(사용자 11-10): ② 에서 「메뉴 · 패키지」로 판정한 것 중 M1 · M2 가 든 것을 `package` · `package_item` 에. 가격이 붙은 상품(market-pricing)은 여전히 하지 않는다.
6. **외부 사실 보충 금지.** 원장에 적힌 주장만. 「」 인용은 원장 글자 그대로.
7. 사전에 없는 값은 사전 행을 만들지 않고 `dict-candidates.csv` + 그 칸 빈칸(지금까지와 같음).

## 3. 산출물

`phub-ledger-redesign/silver-model/drafts/relation-pilot/`: 아래 표 CSV · `source_ref.csv`(관계 행 근거만) · `relation-judgment.csv` · `relation-conflicts.csv` · `dict-candidates.csv` · `relation-notes.md` · `relation-build.py` · `relation-check.py`.
CSV 는 UTF-8 BOM · `;` 칸 금지. `silver/`·원장 · archive · 다른 drafts 변경 금지. 커밋 · push 금지.

## 4. 표 (id 접두는 괄호 — `IND-0001` 꼴)

| 표 | 칸 |
|---|---|
| `indication` 적응 (IND) | id · target_table · target_code · concern_code · site_code(원장이 자리를 말할 때) · note(원문 수식 — 「경증」 「1차 선택」 같은 것) |
| `outcome` 효과 (OUT) | id · target_table · target_code · effect_code · site_code · onset_text/min/max/unit/qualifier · peak_text/min/max/unit/qualifier · duration_text/min/max/unit/qualifier · note |
| `adverse_risk` 부작용 위험 (ADR) | id · target_table · target_code · adverse_code · site_code(생기는 자리 — **시술 자리와 다를 때만**, 예: 이마 보톡스 → 눈꺼풀) · severity_text(원장 등급 · 문구 그대로) · onset_text/min/max/unit/qualifier · duration_text/min/max/unit/qualifier · note |
| `adverse_frequency` 빈도 (ADF) | id · adverse_risk_id · value_text(원문) · min · max · unit · qualifier · denominator(분모 · 대상 원문 — 「치료 방문」 등) · grade_text(「드물게」 「흔함」 원문) |
| `adverse_factor` 위험 요인 (ADX) | id · adverse_risk_id · kind(위험 요인 / 유발 조건 / 원인 기전) · text(원문) · condition_code(사람 조건이면) · site_code · anatomy_code |
| `adverse_guidance` 대처 (ADG) | id · adverse_risk_id(또는 target 직접 — 사건 없는 일반 안내는 target_table · target_code) · kind(관리 / 예방 / 경고 기준 / 모니터링) · timing_text(Day 1-3 등 원문) · level_text(정상 / 이상 / 주의 / 응급 — 원장 등급 그대로) · text(원문) |
| `contraindication` 금기 · 주의 (CTR) | id · target_table · target_code · condition_code · level_text(절대 금기 / 상대 금기 / 주의 — **원장 칸 이름 · 문장 말미 그대로**) · period_text/min/max/unit/qualifier/from(중단 · 대기 기간) · reason_text(원문) |
| `procedure_relation` 시술 간 관계 (PRL) | id · from_table · from_code · to_table · to_code · kind(시너지 / 순서 / 최소 간격 / 같은 날 불가 / 이전 시술 확인 — 원장이 쓰는 갈래로, 새 갈래는 notes) · level_text(원장 등급 그대로) · interval_text/min/max/unit/qualifier · order(순서일 때) · text(원문) — **한쪽 끝이 M1 · M2 이면 넣는다**(다른 끝 계열은 그 코드로, 코드가 없으면 빈칸 + judgment 에 이유) |
| `package` 패키지 (PKG) | id · name(원장 이름 그대로) · kind(레시피 / 고민 패키지 / 연간 플랜 / 원데이 …) · concern_code(원장이 고민을 붙였으면) · text(목표 · 설명 원문) |
| `package_item` (PKI) | id · package_id · target_table · target_code · step(순서) · session_text(회차 · 주기 원문) · role_text(역할 원문) |
| `citation` 문헌 (CIT) | id · authors · title · journal · year · pmid · doi · url(원장에 있는 것만) |
| `citation_link` (CTL) | id · citation_id · relation_table · relation_id · statement(원장 문장 그대로) |

- 근거: 모든 관계 행 ≥ 1 근거(source_ref: target_table = 위 표 이름 · target_id = id · field 비우거나 칸 이름 · ref = 원장 포인터).
- 대상 코드: silver 사전 · ② 코드만(concern · effect · adverse · condition · site · anatomy · modality · procedure · procedure_case).
- 지난 시범의 수식어 목록(사전 notes 「관계 단계로 넘길 수식어」)은 위 칸으로 돌아온다(자리 → site_code · 시점 → onset · 기간 → duration · 정도 → severity_text / note).

## 5. 읽을 것

- 원장(브론즈 3판) `phub-recommend/bronze/phub-ledger/*.json` 21개 — **M1 · M2 의 관계 자리 전부**: complications(M1 · M2 묶음) · contraindications(rules 27 중 M1 · M2 끝 · absolute/relative) · consent-checklist · pre-procedure-checklist · post-procedure-timeline · patient-education · pih-risk · anatomy-danger-zones · literature-evidence · procedure-profiles · procedure-comparison · synergy · treatment-sequence · treatment-optimization · combo-recipes · problem-combos · problem-packages · taxonomy(`modality[0]` · `[1]` 와 하위 · problem 중 modality_ref M1 · M2) · extracted `M1` · `M2`(indications · onset_duration · safety · contraindications · aftercare · related_techniques).
- silver 전부(사전 + ② 조합 + 공통 alias · source_ref).
- **지난 시범(재사용 — 믿지 말고 원문 확인)**: `phub-ledger-redesign/silver-model/archive/pilot-botox-adverse.md`(케이스 × 부작용 · 판정 D1~D8 · 테이블 초안 §5 — 이번 표의 바탕) · `archive/pilot-filler-adverse.md`.
- 관계 몫 원문 위치 · 수식어: `silver-model/drafts/effect/effect-notes.md` §5 · `drafts/adverse/adverse-notes.md` §4 · `drafts/condition/condition-notes.md` §4(시술 이력 18 → procedure_relation 「이전 시술 확인」) · `drafts/concern/concern-notes.md` · `silver-model/notes/effect-concern-reference.csv`(효과 ↔ 고민 짝 — 적응 판단 참고).
- ② 판정: `silver-model/notes/combo-item-judgment.csv`(원장 이름 → 시술 · 케이스 코드 — 관계 문장이 어느 시술 · 케이스 얘기인지 찾을 때) · `notes/combo-notes.md`.
- 결정 기록: `phub-ledger-redesign/_RESUME.md`.
- 색인(누락 확인): `phub-ledger-redesign/first-pass/<원장>/source-map.json`.

## 6. 판정 · 확인

**`relation-judgment.csv`** — source · pointer · text(원문) · judgment(표 이름 / 안 담음) · row_id · reason. M1 · M2 관계 자리의 원장 잎 **전부**. 「안 담음」은 이유(관계 아님 · 다른 계열 · 시술 과정 설명 · 마케팅 문구 …) — 담을 칸이 없어서 안 담은 것은 0 이어야 한다(있으면 notes 판단 목록 + 칸 제안).

**notes 확인 표** — 아래가 행으로 표현되는지: 이마 보톡스 → 안검하수(생기는 자리 = 눈꺼풀) · 보톡스 멍(지속 7-14일 원문) · 독감 유사 증상 빈도 두 측정(지난 D1) · 사각턱 보톡스 효과 발현 · 지속 · 보톡스 항체 내성 + 재시술 간격(지난 D7) · 임신 · 수유 금기 · 항응고제 중단 기간 · 필러 혈관폐색 → 실명(위험 부위 · 해부 구조) · 필러 대처(히알루로니다제 — 관리) · 필러 ↔ 레이저 간격 rule · 보톡스 + 필러 패키지 · 고민 「사각턱」 「팔자주름」 → 적응 · 문헌 하나 → citation_link.

## 7. notes (짧게)

1. 집계(표별 행 수 · 붙은 층별 — 계열 / 시술 / 케이스) · 판정 집계 · 누락 확인 방법
2. 확인 표
3. 원장 충돌 처리(전용 원장 채택 수 · `relation-conflicts.csv` 건수)
4. 칸에 담기 어려웠던 값과 담은 자리(지난 시범 §5 「담을 칸이 없었던 값」 꼴)
5. 사전 추가 후보 · 지난 시범 대비 바뀐 점
6. 사용자 판단이 필요한 것 — 원문 · 이유 · 추천 · 선택지

## 8. 완료 기준 (`relation-check.py` — 코디가 다시 돌린다)

- M1 · M2 관계 자리 원장 잎 전부 판정(source-map 대조) · 「담을 칸 없어 안 담음」 = 0(또는 notes 판단 목록과 같음).
- 참조 전부 존재(target · 사전 코드 · adverse_risk_id · package_id · citation_id) · id 중복 0 · `;` 0 · 모든 행 근거 ≥ 1.
- `*_text` · text · statement 는 원장 글자 그대로(원문 대조) · **`*_min` · `*_max` 숫자는 같은 행 `*_text` 원문에 그 숫자가 있음**(바꾼 숫자 0) · grade_text 가 있는 행에 지어낸 수치 없음.
- 같은 target · 같은 대상 코드 관계가 부모 층과 자식 층에 같은 값으로 중복 = notes 목록과 같음(원장이 따로 말한 것만).
- `silver/`·원장 변경 없음 · 산출물 외 변경 없음(`git status`).

## 9. 완료 보고

막히면 원문 먼저, 사용자 선택이 필요하면 preamble 의 ask. 범위를 넓히지 않는다(M1 · M2 밖 계열의 관계 · 외부 조사 · 사전 행 추가 하지 않음).
preamble 의 `worker_done` 을 정확히 한 번(`--outcome succeeded|failed`, `--report-path orchestration/work/phub-ledger-redesign/silver-model/drafts/relation-pilot/relation-notes.md`).
그다음 코디 터미널에 한 줄:
`orca terminal send --terminal term_107c16b1-6066-4654-9272-359649efd67f --text "관계 시범 완료: orchestration/work/phub-ledger-redesign/silver-model/drafts/relation-pilot/" --enter`
