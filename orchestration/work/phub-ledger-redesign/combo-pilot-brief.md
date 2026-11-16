# 발주서 — ② 조합 시범: 시술 종류 · 케이스 (M1 · M8 · M16)

너는 이 작업의 맥락이 없다. 이 문서 한 장과 「읽을 것」만으로 일한다.
작업 레포(코디 워크트리): `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온` — 아래 상대 경로는 `orchestration/work/` 기준.

## 1. 목표 · 구조

Procedure Hub 는 **시술 원장**이다. 입구(고민 · 시술 이름 · 제품) 어디로 들어와도 같은 시술에 닿게 한다. 실버 3층: ① 기본 단위 사전(**확정**, `phub-ledger-redesign/silver-model/silver/` 22표) → **② 조합(이번)** → ③ 관계(적응 · 효과 · 부작용 위험 · 금기 · 시너지 — 이번에 하지 않음).

```text
계열(modality)  →  시술 종류(procedure)              →  케이스(procedure_case)
M1 보톡스        →  보톡스 (재료 + 원리가 같으면 1개)   →  교근 · 사각턱 / 진피 · 희석 · 다점 = 스킨보톡스 / 땀샘 · 겨드랑이 = 다한증
M8 레이저        →  선택적 광열 레이저 · 피코 · 박피 …  →  멜라닌 · 1064nm · 토닝 / 1064nm · 롱펄스 = 제네시스 …
M16 수액치료     →  성분이 다르면 다른 시술              →  (원장이 말한 대상 · 방법 · 제품)
```

이번은 **시범: M1 보톡스 · M8 레이저 · M16 수액치료** 세 계열만. 검수 뒤 나머지 14계열을 같은 규칙으로 한다.

## 2. 사용자 결정 (바꾸지 않는다)

1. **시술 종류 = 계열 + 재료 · 에너지 종류 + 작용 원리.** 작용 대상 · 부위 · 방법 · 제품 · 세부 재료(파장)는 시술 종류를 가르지 않는다.
   - 레이저 · 기기: 에너지 종류 × 원리가 시술 종류. 표적 · 파장 · 펄스 · 프락셔널 여부는 케이스.
   - 약물 · 주사: **성분이 다르면 다른 시술**(같은 계열 안). 예: 백옥주사(글루타치온) ≠ 신데렐라주사. 백옥주사 같은 마케팅 이름도 널리 쓰는 시술 이름이면 시술 이름(입구).
   - 보톡스는 1개. **스킨보톡스(= 메조보톡스 = 더모톡신)** · 다한증 보톡스는 케이스(이름 있는 케이스).
   - **제네시스는 제품이 아니라 케이스 이름**: 1064nm + 롱펄스. 「제네시스토닝」은 같은 케이스의 다른 이름. 원장에 없는 피코제네시스 · 「Q-스위치와 함께 쓴 제네시스 토닝」은 만들지 않는다.
2. **케이스 = 시술 종류 + 작용 대상 + 부위 + 방법 + 세부 재료 — 원장이 실제로 말한 조합만.** 부위 × 대상을 곱해 만들지 않는다. 같은 조합이 여러 원장에 나오면 한 행 + 근거 여럿.
3. **부위만 다른 것은 별개 케이스**(이마 보톡스 ≠ 미간 보톡스) — site 는 케이스당 하나.
4. **제품은 케이스를 가르지 않는다** → `case_product` 연결 표로만.
5. **가격표(market-pricing.json)로 케이스를 만들지 않는다**(상품은 맨 뒤 단계). 가격표 행은 item-judgment 에 「상품」으로 판정만, 가리키는 케이스가 있으면 코드만 적는다.
6. 회차 · 일정(터치업 · 4회 · 유지) = 케이스 아님. 패키지 · 조합 메뉴 = ③ 시너지 몫 — 판정만.
7. 부작용 · 효과 · 고민 · 사람 조건은 넣지 않는다(③). 케이스 설명에도 효과 · 부작용 서술을 넣지 않는다.

## 3. 산출물

`phub-ledger-redesign/silver-model/drafts/combo/`:
`procedure.csv` · `procedure_case.csv` · `case_method.csv` · `case_product.csv` · `alias.csv`(시술 · 케이스 행만) · `source_ref.csv`(시술 · 케이스 · 연결 행만) · `item-judgment.csv` · `dict-candidates.csv` · `combo-notes.md` · `combo-build.py` · `combo-check.py`
CSV 는 UTF-8 BOM · `;` 칸 금지 · 이름 괄호 금지. `silver/`·원장·archive 변경 금지. 커밋 · push 금지. 스크립트는 이 폴더에.

## 4. 읽을 것

- 원장(브론즈 3판): `phub-recommend/bronze/phub-ledger/*.json` — M1 · M8 · M16 에 해당하는 자리 전부(taxonomy `modality[0]` · `[7]` · `[15]` 하위분류 · 항목 · 제품 · extracted `M1` · `M8` · `M16` · taxonomy problem 쪽 해당 항목 · procedure-profiles · procedure-comparison · pih-risk · patient-education · products.json · combo-recipes · problem-packages · problem-combos · treatment-optimization · synergy · treatment-sequence 의 시술 이름 자리 · market-pricing 은 판정만). 계열 번호는 `silver/modality.csv` 로 확인.
- 확정 사전: `silver-model/silver/` 전부 — modality · material(+ material_spec) · mechanism · tissue · anatomy(+ anatomy_site) · site · method · product(+ product_material · product_method · product_modality) · 공통 `alias.csv` · `source_ref.csv`. **코드는 이 사전 코드만 쓴다.**
- 지난 시범(재사용 — 판정을 처음부터 다시 하지 말고 새 구조 · silver 코드로 고친다. 믿지 말고 원문 확인): `silver-model/archive/pilot-3level/`(M1 · M8 · M9 — 시술 종류 · 케이스 · item-judgment · notes §5 판단 7건) · `silver-model/archive/pilot-set/`(M1 보톡스 · M8 레이저 · M16 수액치료).
- 결정 기록: `phub-ledger-redesign/_RESUME.md` 결정 표(11-10 · 11-11 행).
- 색인(누락 확인): `phub-ledger-redesign/first-pass/<원장>/source-map.json`.

## 5. 테이블

**`procedure.csv`** — `code`(PRC-…) · `name_ko` · `name_en` · `name_en_source`(원장 / 보충) · `modality_code` · `material_code`(재료 · 에너지 **종류** — 레이저면 레이저 빛 수준, 약물이면 성분) · `mechanism_code`(주된 작용 원리 하나) · `overview` · `mechanism`
- 이름 = 널리 쓰는 시술 이름(원장 표기). 다른 이름 · 약어는 공통 alias(target_table = procedure).
- overview · mechanism 은 원장 문장 근거(「」 인용은 글자 그대로, source_ref field = overview / mechanism). 원장에 없는 임상 사실 금지. 「드물게」 「얕게」를 수치로 바꾸지 않는다.
- 원리가 둘 이상으로 읽히면 주된 것 하나 + notes 판단 목록(연결 표를 새로 만들지 않는다).
- 계열과 1:1(보톡스)이면 개요 · 기전은 시술 종류에 둔다. modality.csv 는 고치지 않는다.

**`procedure_case.csv`** — `code`(CAS-…) · `procedure_code` · `name_ko`(원장이 이 조합에 붙인 이름이 있을 때만, 없으면 빈칸) · `tissue_code` · `anatomy_code` · `site_code` · `material_code`(세부 재료: 1064nm 등 — 종류 행의 하위 · 없으면 빈칸) · `description`
- 작용 대상: 원장이 이름 있는 구조(교근 · 전두근 …)를 말하면 `anatomy_code`(그 anatomy 의 tissue 를 `tissue_code` 에도), 아니면 `tissue_code` 만. 원장이 대상을 말하지 않으면 둘 다 빈칸.
- `site_code` 하나. 원장이 부위를 말하지 않으면 빈칸.
- 케이스 이름의 다른 표기(메조보톡스 · 더모톡신 · 제네시스토닝 · 턱보톡스)는 공통 alias(target_table = procedure_case) — 원문으로 같은 조합임을 확인한 것만. 띄어쓰기만 다른 표기는 넣지 않는다.
- description: 원장 문장으로 이 조합이 무엇인지(대상 · 방법). 효과 · 부작용 서술 없음.

**`case_method.csv`** — `id` · `case_code` · `method_code`(희석 · 다점 주사 · 프락셔널 · 롱펄스 등 원장이 이 조합에 말한 방법 — `silver/method.csv` 코드)
**`case_product.csv`** — `id` · `case_code` · `product_code` — 원장이 그 제품을 그 조합에 쓴다고 말한 것만. 제품 기전 문장으로 대상을 이었으면 근거에 그 위치.

**`item-judgment.csv`** — `source` · `pointer` · `name` · `judgment`(시술 종류 / 케이스 / 제품 / 상품 / 메뉴 · 패키지 / 성분 / 분류 칸 / 회차 · 일정 / 시술 아님 / 다른 계열) · `procedure_code` · `case_code` · `reason`. 여러 시술을 가리키는 메뉴는 행을 나눈다(`;` 금지).

**`dict-candidates.csv`** — `dictionary` · `name` · `source` · `reason`: 케이스에 필요한데 silver 사전에 없는 재료 · 대상 · 부위 · 방법 · 제품. **사전에 새 행을 만들지 않는다** — 케이스 칸은 빈칸 + 이 목록.

## 6. 확인 (notes 에 표)

아래가 행 + 연결 + alias 로 표현되는지: **보톡스**(시술 1) · **사각턱 보톡스**(교근 · 사각턱) · **이마 / 미간 보톡스**(별개 케이스) · **스킨보톡스**(메조보톡스 · 더모톡신 alias) · **다한증 보톡스** · **레이저토닝** · **제네시스**(제네시스토닝 alias · 1064nm · 롱펄스) · **피코토닝** · **CO2 프락셔널** · **백옥주사** · **보톡스 제품 → 케이스**(보톡스 · 제오민 등 원장에 있는 것).

## 7. notes (짧게)

1. 집계(계열 × 판정) · 시술 종류 수 · 케이스 수 · 누락 확인 방법
2. 시술 종류 목록(계열별: 이름 · 재료 · 원리 · 나눈 이유 한 줄)
3. 케이스 요약(시술별 케이스 수 · 이름 있는 케이스 · 무엇으로 갈렸나)
4. 확인 사례 표 · 입구 점검: 시술 이름(원장 시술 · 케이스 이름 전부가 procedure · procedure_case · alias 에 있나) · 제품(세 계열 제품 중 case_product 로 케이스에 닿지 않는 것과 이유)
5. 지난 시범 대비 바뀐 점 · 지난 notes §5 판단 7건 처리
6. 사전 추가 후보 요약 · 사용자 판단이 필요한 것 — 원문 · 이유 · 추천 · 선택지(정의로 판단 가능한 건 올리지 않는다)

## 8. 완료 기준 (`combo-check.py` — 코디가 다시 돌린다)

- 세 계열 원장 항목 전부 item-judgment 에 판정(source-map 대조) · 가격표로 만든 케이스 0.
- 시술 종류가 재료 종류 + 원리로만 갈림(같은 modality · material · mechanism 인 시술 종류 2개 이상 = 0, 예외는 notes 근거).
- 케이스 (procedure · tissue · anatomy · site · material · 방법 집합) 중복 0.
- 참조 전부 silver 에 존재 · `;` 0 · 이름 괄호 0 · 모든 행 근거 ≥ 1 · 「」 인용 원장 글자 그대로.
- 입구: 원장의 세 계열 시술 · 케이스 이름 중 procedure · procedure_case · alias 어디에도 없는 것 = notes 목록과 같음.
- `silver/`·원장 변경 없음 · 산출물 외 변경 없음(`git status`).

## 9. 완료 보고

막히면 원문 먼저, 사용자 선택이 필요하면 preamble 의 ask. 범위를 넓히지 않는다(③ 관계 · 다른 계열 · 외부 조사 하지 않음).
preamble 의 `worker_done` 을 정확히 한 번(`--outcome succeeded|failed`, `--report-path orchestration/work/phub-ledger-redesign/silver-model/drafts/combo/combo-notes.md`).
그다음 코디 터미널에 한 줄:
`orca terminal send --terminal term_107c16b1-6066-4654-9272-359649efd67f --text "combo 시범 완료: orchestration/work/phub-ledger-redesign/silver-model/drafts/combo/" --enter`
