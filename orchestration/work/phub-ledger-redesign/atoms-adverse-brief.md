# 발주서 — 기본 단위: 부작용 개념 사전

너는 이 작업의 맥락이 없다. 이 문서 한 장과 「읽을 것」만으로 일한다.
작업 레포(코디 워크트리): `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온` — 아래 상대 경로는 `orchestration/work/` 기준.

## 1. 목표 · 구조

Procedure Hub 는 **시술 원장**이다. 실버 3층: ① 기본 단위(사전) → ② 조합(시술 · 케이스) → ③ 관계(적응 · 케이스→효과 · **부작용 위험**(케이스 × 부작용 + 생기는 자리 · 빈도 · 시점 · 기간 · 대처) · 금기 · 시너지 · 근거).
확정 실버(`phub-ledger-redesign/silver-model/silver/`, DB 모양 — `;` 칸 없음): 사전(modality · material · mechanism · tissue · method · product · organization · site · anatomy · concern(대·중·소 3단) · effect(3단)) + 관계 표(id) + 공통 `alias.csv`(target_table · target_code · name · kind: 별칭/약어/의학 용어) + 공통 `source_ref.csv`(target_table · target_id · field · ref).

이번 일: ① 중 **부작용 개념** 사전 — 시술 뒤 생길 수 있는 사건 · 증상의 **개념만**(멍 · 부종 · 홍반 · 통증 · 혈관폐색 · 실명 · 색소침착 · 결절 · 실 노출 · 역설적 지방 증식 …).
**하지 않는 것**: 어느 시술 · 케이스에 생기는지 · 빈도(incidence) · 심각도 등급 · 발현 시점(onset) · 지속 · 위험 요인 · 대처 · 예방 · 생기는 자리 — 모두 관계 단계(케이스 × 부작용). 원문 위치만 notes 에 모은다.

## 2. 산출물

`phub-ledger-redesign/silver-model/drafts/adverse/`: `adverse.csv` · `alias.csv`(부작용 행만) · `source_ref.csv`(부작용 행만) · `adverse-notes.md` · `adverse-build.py` · `adverse-check.py`
CSV 는 UTF-8 BOM. `;` 칸 금지. `silver/`·원장 변경 금지. 커밋·push 금지. 스크립트는 이 폴더에.

## 3. 읽을 것

- 원장(브론즈 3판): `phub-recommend/bronze/phub-ledger/*.json` **21개 전부에서 부작용을 가리키는 자리**. 특히:
  - `complications.json`(categories[] 계열별 · complications[].name · severity · incidence · onset · mechanism · risk_factors · management · prevention · evidence · severity_levels)
  - taxonomy `extracted/safety/common_adverse_effects|serious_adverse_effects|common_side_effects` · 항목 · 제품 detail
  - literature-evidence `adverse_effects`(statement · patient_ko) · pih-risk · anatomy-danger-zones(위험 · 실명 · 괴사 등) · consent-checklist · patient-education · post-procedure-timeline · procedure-profiles · contraindications 속 부작용 이름
- 지난 시범(같은 문제를 먼저 본 기록, 믿지 말고 원문 확인): `phub-ledger-redesign/silver-model/archive/pilot-botox-adverse.md` · `pilot-filler-adverse.md`
- 확정 사전: `silver/concern.csv` · `silver/effect.csv` · `silver/site.csv` · `silver/anatomy.csv` · `silver/mechanism.csv`(+ alias) — 겹침 대조
- 이름 · 분류 방식 참고: `silver-model/drafts/concern/concern-notes.md` §7(3단 · 명사형 · 설명)
- 색인(누락 확인): `phub-ledger-redesign/first-pass/<원장>/source-map.json`

## 4. 테이블 `adverse.csv`

`code`(ADV-…) · `name_ko` · `name_en` · `name_en_source`(원장 / 보충) · `level`(대분류 / 중분류 / 소분류) · `parent_code` · `description`
- **3단**: 모든 행은 대분류 하나 아래, 깊이 ≤ 3, 자식 없는 중분류는 그 자체가 끝 단계. 대분류는 원장이 묶는 말(예: 주사 부위 반응 · 염증/감염 · 혈관 합병증 · 신경 · 색소 · 흉터 · 결절/육아종 · 시술물 관련(실 노출 · 이동) · 열/화상 · 전신 반응 · 결과 불만족(비대칭 등) …) 중에서 — **원장에 있는 말**로 정하고 근거를 단다. complications 의 계열(M1 보톡스 …)은 시술 쪽이라 분류 축으로 쓰지 않는다.
- **원자 개념으로 쪼갠다**: 원장 이름이 여러 개념을 붙여 쓴 경우(「멍·타박상」 · 「주사 부위 홍반·부종」 · 「통증·불편감 및 지연성 통증」 · 「감염 및 바이오필름」) 개념마다 한 행. 같은 개념의 다른 말(멍 = 타박상 = 반상출혈 · 부종 = 종창 = 붓기)은 한 행 + alias(한자 의학 용어는 의학 용어, 영어 · 약어(PIH · PAH)는 별칭/약어).
  - 수식어는 이름에서 뺀다: 자리(「주사 부위」 → 관계의 생기는 자리) · 시점(「시술 직후」 · 「지연성」) · 기간(「일시적」) · 정도(「경미한」). **단 원장이 별개 사건으로 다루는 것**(지연성 결절 vs 결절 · 역설적 지방 증식)은 원장대로 별개 행 — 판단 못 하면 notes.
  - 뺀 수식어는 버리지 않는다 — notes 「관계 단계로 넘길 수식어」 목록(원장 이름 · 뺀 말 · 종류: 자리/시점/기간/정도).
- **이름 = 명사형 일반 용어**, 원장 다른 표기는 alias. 이름 괄호 금지(「멍 / 반상출혈 (Bruising / Ecchymosis)」 → 이름 멍 · 반상출혈 의학 용어 · Bruising/Ecchymosis 별칭 · name_en 원장).
- **설명**: 원장 문장을 근거로 자세하게 — 무엇인지 · 원장의 mechanism 서술(개념 수준, 특정 시술 수치 없이) · 비슷한 부작용과의 차이(원장이 가르는 대로, 안 가르면 「원장이 적지 않는다」) · 합쳐진 별칭. 「」 인용은 원장 글자 그대로, 근거는 source_ref(field = description). **원장에 없는 임상 사실 금지. 「드물게」 「얕게」를 수치로 바꾸지 않는다. 빈도 · 등급 값은 설명에도 쓰지 않는다**(관계 몫).

## 5. 규칙

1. **원장 표현만.** 원장에 없는 부작용을 만들지 않는다. 영어가 원장에 없으면 표준 표기 + 보충.
2. **부작용이 아닌 것은 넣지 않는다**: 금기 · 위험 요인(흡연 · 항응고제) · 대처/치료(히알루로니다제 · 항생제) · 예방법 · 시술 과정 설명 · 기전 · 고민. notes 「부작용 아님」 목록.
3. **고민 · 효과 사전과 같은 말**(색소침착 · 흉터 · 홍조 · 부종 등)은 부작용 사전에 **별개 행**으로 둔다(쓰임이 다름 — 고민은 찾아오는 이유, 부작용은 시술 뒤 사건). 겹치는 이름 목록을 notes 에(부작용 코드 · 고민/효과 코드).
4. 한 부작용 = 한 행. 같은 사건은 합치고, 범위 · 원인이 다르면 나눈다. 애매하면 나누고 notes.

## 6. 확인 (notes 에 표)

아래가 행 + 부모 + 별칭으로 표현되는지: **멍**(타박상 · 반상출혈 · Bruising) · **부종**(종창 · 붓기) · **혈관폐색**(색전 — 원장이 같게 쓰면 합침, 아니면 나눔) · **실명** · **안검하수**(보톡스) · **PIH**(염증후 과색소침착) · **실 노출 / 실 이동** · **역설적 지방 증식(PAH)** · **결절 / 육아종 / 지연성 결절**(원장대로).
그리고 원장의 부작용 언급 전부가 행에 붙었는지(원장별 자리 수 · 못 붙인 것).

## 7. notes (짧게)

1. 행 수(level · 대분류별) · 누락 확인 방법
2. 확인 사례 표
3. 쪼갠 원장 이름 표(원장 이름 → 행들) · 합친 것 / 합치지 않은 후보
4. 관계 단계로 넘길 수식어 목록 · 관계 단계 몫 원문 위치(incidence · severity · onset · duration · risk_factors · management · prevention — 칸별 개수만)
5. 부작용 아님 목록 · 고민/효과 이름 겹침 표
6. 사용자 판단이 필요한 것 — 원문 · 이유 · 추천 · 선택지

## 8. 완료 기준 (`adverse-check.py` — 코디가 다시 돌린다)

- level · 3단 규칙 · 이름 괄호 0 · `;` 0 · name_ko 중복 0 · 수식어(주사 부위 · 일시적 · 지연성 · 시술 직후 …)가 이름에 남은 것 = notes 판단 목록과 같음.
- 모든 행 근거 ≥ 1 · description 있음 · 「」 인용 원장 글자 그대로 · 설명에 빈도 수치(% 등) 없음 · 참조 전부 존재.
- `silver/`·원장 변경 없음 · 산출물 외 변경 없음(`git status`).

## 9. 완료 보고

막히면 원문 먼저, 사용자 선택이 필요하면 preamble 의 ask. 범위를 넓히지 않는다(관계 · 외부 조사 하지 않음).
preamble 의 `worker_done` 을 정확히 한 번(`--outcome succeeded|failed`, `--report-path orchestration/work/phub-ledger-redesign/silver-model/drafts/adverse/adverse-notes.md`).
그다음 코디 터미널에 한 줄:
`orca terminal send --terminal term_107c16b1-6066-4654-9272-359649efd67f --text "adverse 사전 완료: orchestration/work/phub-ledger-redesign/silver-model/drafts/adverse/" --enter`
