# 발주서 — 기본 단위: 사람 조건 사전

너는 이 작업의 맥락이 없다. 이 문서 한 장과 「읽을 것」만으로 일한다.
작업 레포(코디 워크트리): `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온` — 아래 상대 경로는 `orchestration/work/` 기준.

## 1. 목표 · 구조

Procedure Hub 는 **시술 원장**이다. 실버 3층: ① 기본 단위(사전) → ② 조합(시술 · 케이스) → ③ 관계(적응 · 케이스→효과 · 부작용 위험 · **금기 · 주의 · 위험 요인**(케이스 × 사람 조건) · 시너지/순서/간격 · 근거).
확정 실버(`phub-ledger-redesign/silver-model/silver/`, DB 모양 — `;` 칸 없음): 사전(modality · material · mechanism · tissue · method · product · organization · site · anatomy · concern · effect · adverse — concern/effect/adverse 는 대·중·소 3단 · 명사형 이름 · 원장 인용 설명) + 관계 표(id) + 공통 `alias.csv`(target_table · target_code · name · kind: 별칭/약어/의학 용어) + 공통 `source_ref.csv`(target_table · target_id · field · ref).

이번 일: ① 의 마지막 **사람 조건** 사전 — 시술을 받는 **사람의 상태 · 특성**(임신 · 수유 · 피부 타입 · Fitzpatrick 유형 · 켈로이드 체질 · 자가면역질환 · 당뇨 · 항응고제 복용 · 이소트레티노인 복용 · 흡연 · 나이 · 성별 · 최근 햇빛 노출 …)의 **개념만**.
**하지 않는 것**: 어느 시술에 금기인지/주의인지 · 위험도 · 중단 기간(「시술 전 ○주 중단」) · 확인 방법 — 모두 관계 단계(케이스 × 사람 조건). 시술과 시술 사이의 간격 · 순서(contraindications.json rules 의 from → to · interval)는 **사람 조건이 아니라** 시술 간 관계 — 넣지 않고 원문 위치만 notes.

## 2. 산출물

`phub-ledger-redesign/silver-model/drafts/condition/`: `condition.csv` · `alias.csv`(조건 행만) · `source_ref.csv`(조건 행만) · `condition-notes.md` · `condition-build.py` · `condition-check.py`
CSV 는 UTF-8 BOM. `;` 칸 금지. `silver/`·원장 변경 금지. 커밋·push 금지. 스크립트는 이 폴더에.

## 3. 읽을 것

- 원장(브론즈 3판): `phub-recommend/bronze/phub-ledger/*.json` **21개 전부에서 사람의 상태 · 특성을 가리키는 자리**. 특히:
  - taxonomy · extracted 의 `contraindications/absolute|relative` · `safety/contraindications` · `indications`(특정 피부 타입 · 체질 언급)
  - pre-procedure-checklist(universal_checks · category_specific: label · description) · consent-checklist(categories[].contraindications 등) · pih-risk(Fitzpatrick · 피부 타입) · patient-education · procedure-profiles · complications `risk_factors` · treatment-optimization · anatomy-danger-zones(체질 · 나이 언급)
- 고민 작업에서 넘어온 후보: `silver-model/drafts/concern/concern-notes.md`(피부 타입 · 「사람 조건」 표기 줄 · §6.5) · 제품 판단 기록(아큐탄 → 성분 이소트레티노인은 사람 조건으로: `phub-ledger-redesign/_RESUME.md` 결정 표 11-11)
- 확정 사전: `silver/concern.csv` · `adverse.csv` · `material.csv` · `product.csv`(+ alias) — 겹침 대조
- 방식 참고: `silver-model/drafts/adverse/adverse-notes.md` · `drafts/concern/concern-notes.md` §7
- 색인(누락 확인): `phub-ledger-redesign/first-pass/<원장>/source-map.json`

## 4. 테이블 `condition.csv`

`code`(CND-…) · `name_ko` · `name_en` · `name_en_source`(원장 / 보충) · `level`(대분류 / 중분류 / 소분류) · `parent_code` · `material_code`(복용 · 사용 중인 약 · 성분일 때 `silver/material.csv` 코드, 없으면 빈칸 — 재료 사전에 없으면 잇지 말고 notes 「재료 추가 후보」) · `description`
- **3단**: 모든 행은 대분류 하나 아래, 깊이 ≤ 3, 자식 없는 중분류는 그 자체가 끝 단계. 대분류는 원장 말 중에서(예: 임신/수유 · 피부 특성 · 피부 질환 · 전신 질환 · 복용 약 · 알레르기 · 체질 · 생활 습관 · 나이/성별 · 시술 이력 …) — 원장에 그 말이 없으면 가장 가까운 원장 말을 쓰고 notes 판단 목록.
- **이름 = 명사형 일반 용어**(「임신 중」 → 임신 · 「항응고제 복용 중인 환자」 → 항응고제 복용). 원장 다른 표기는 alias. 이름 괄호 금지.
- **수식어 분리**: 「최근 6개월 내 이소트레티노인 복용」 → 이름 이소트레티노인 복용, 「최근 6개월 내」는 관계 단계 수식어 목록(기간). 「활동성 여드름 · 활성 감염」처럼 원장이 상태 자체를 가르는 말은 원장대로 판단.
- **시술 이력**(「최근 필러 시술」 · 「이전 시술 부위」)은 시술 쪽 관계라 개념만 두지 말고 notes 「시술 이력 — 관계 단계」 목록으로(행으로 둘지 판단 목록).
- **설명**: 원장 문장 근거로 자세하게(무엇인지 · 원장이 왜 문제 삼는지 개념 수준 — 특정 시술명 · 중단 기간 · 위험도 수치 없이 · 비슷한 조건과의 차이 · 별칭). 「」 인용은 원장 글자 그대로(source_ref field = description). **원장에 없는 임상 사실 금지. 「드물게」 「얕게」를 수치로 바꾸지 않는다.**

## 5. 규칙

1. **원장 표현만.** 원장에 없는 조건을 만들지 않는다. 영어 없으면 표준 표기 + 보충.
2. **사람 조건이 아닌 것은 넣지 않는다**: 부작용(시술 뒤 사건) · 고민(찾아오는 이유) · 시술 간 간격 · 대처 · 예방법 · 확인 절차. notes 「조건 아님」 목록.
3. **다른 사전과 같은 말**(예: 켈로이드 — 고민 · 부작용에도 있음 / 아토피피부염 — 고민에도 있음)은 사람 조건에 **별개 행**(쓰임이 다름 — 「켈로이드 체질」은 시술 전 사람 특성). 원장이 「체질 · 병력」으로 쓴 것만 조건. 겹침 표를 notes 에.
4. 한 조건 = 한 행. 같은 상태는 합치고(한자 의학 용어 → alias 의학 용어), 범위가 다르면 나눈다(예: 임신 vs 임신 가능성 — 원장대로). 애매하면 나누고 notes.

## 6. 확인 (notes 에 표)

아래가 행 + 부모 + 별칭(+ 재료 연결)으로 표현되는지: **임신** · **수유** · **Fitzpatrick 피부 유형**(원장이 단계별로 다루면 그 단계) · **민감성 피부** · **켈로이드 체질** · **자가면역질환** · **항응고제 복용**(→ 재료 있으면) · **이소트레티노인 복용**(→ 재료 · 아큐탄 별칭 여부는 원장대로) · **헤르페스 병력** · **흡연**.
그리고 원장의 조건 언급 전부가 행에 붙었는지(원장별 자리 수 · 못 붙인 것).

## 7. notes (짧게)

1. 행 수(level · 대분류별 · 재료 연결) · 누락 확인 방법
2. 확인 사례 표
3. 쪼갠 · 합친 것 / 합치지 않은 후보
4. 관계 단계로 넘길 수식어(기간 · 정도) · 관계 단계 몫 원문 위치(금기 절대/상대 · 중단 기간 · 위험도 · 시술 간 간격 rules — 칸별 개수만) · 시술 이력 목록
5. 조건 아님 목록 · 다른 사전 겹침 표 · 재료 추가 후보
6. 사용자 판단이 필요한 것 — 원문 · 이유 · 추천 · 선택지

## 8. 완료 기준 (`condition-check.py` — 코디가 다시 돌린다)

- level · 3단 규칙 · 이름 괄호 0 · `;` 0 · name_ko 중복 0 · 수식어(최근 · ○개월 · 중 · 환자 …)가 이름에 남은 것 = notes 판단 목록과 같음.
- 모든 행 근거 ≥ 1 · description 있음 · 「」 인용 원장 글자 그대로 · 설명에 기간 · 위험도 수치 없음 · 참조 전부 존재(parent · material_code).
- `silver/`·원장 변경 없음 · 산출물 외 변경 없음(`git status`).

## 9. 완료 보고

막히면 원문 먼저, 사용자 선택이 필요하면 preamble 의 ask. 범위를 넓히지 않는다(관계 · 외부 조사 하지 않음).
preamble 의 `worker_done` 을 정확히 한 번(`--outcome succeeded|failed`, `--report-path orchestration/work/phub-ledger-redesign/silver-model/drafts/condition/condition-notes.md`).
그다음 코디 터미널에 한 줄:
`orca terminal send --terminal term_107c16b1-6066-4654-9272-359649efd67f --text "condition 사전 완료: orchestration/work/phub-ledger-redesign/silver-model/drafts/condition/" --enter`
