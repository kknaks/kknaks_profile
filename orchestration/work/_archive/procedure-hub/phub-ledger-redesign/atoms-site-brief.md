# 발주서 — 기본 단위: 부위 사전 (+ 이름 붙은 해부 구조)

너는 이 작업의 맥락이 없다. 이 문서 한 장과 「읽을 것」만으로 일한다.
작업 레포(코디 워크트리): `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온` — 아래 상대 경로는 `orchestration/work/` 기준.

## 1. 목표 · 구조

Procedure Hub 는 **시술 원장**이다. 입구는 고민 · 시술 이름 · 제품이다.
실버 3층: ① 기본 단위(사전) → ② 조합(시술 = 재료 + 기전 · 케이스 = 시술 + 작용 대상 · 부위 · 방법 · 제품) → ③ 관계(적응 · 부작용 위험 + 생기는 자리 · 금기 · 시너지/순서/간격 · 근거).
확정 사전(`phub-ledger-redesign/silver-model/silver/`): modality · material(+material_spec) · mechanism · **tissue**(층 · 구조 · 표적) · method · product(+organization 등).

이번 일: ① 중 **부위** 사전. 부위는 시술의 정체가 아니다(보톡스 이마 ≠ 다른 시술). 나중에 세 역할로 쓰인다 — 시술 대상 부위 · 부작용이 생기는 부위 · 피해야 할 부위. **이번엔 그 연결(관계)을 만들지 않는다.** 사전 자체만 만든다.

## 2. 산출물

`phub-ledger-redesign/silver-model/drafts/site/`: `site.csv` · `site-notes.md`
CSV 는 UTF-8 BOM · 쉼표 · 필요한 칸 큰따옴표. `silver/`·원장 변경 금지. 커밋·push 금지.

## 3. 읽을 것

- 원장(브론즈 3판): `phub-recommend/bronze/phub-ledger/*.json` **21개 전부에서 부위를 가리키는 자리**. 특히:
  - `anatomy-danger-zones.json`(zones[]: name_ko · name_en · vessels[] · nerves[] · safe_in… — 부위 + 이름 붙은 혈관·신경·근육)
  - taxonomy 항목 이름·detail 속 부위(보톡스 이마 · 사각턱 · 눈밑 …) · problem-packages / problem-combos 의 부위 · complications 의 생기는 자리 · market-pricing 이름 속 부위(**이름만** — 상품은 안 다룬다) · procedure-comparison · pih-risk · contraindications 등
- 확정 사전: `silver-model/silver/tissue.csv`(구조: 근육 · 혈관 · 피지샘 … 일반명만 있다)
- 색인(누락 확인): `phub-ledger-redesign/first-pass/<원장>/source-map.json`
- 이름 규칙 참고: `silver-model/silver/product.csv` · `tissue.csv` 의 칼럼 모양

## 4. 테이블 `site.csv`

`code`(SITE-…) · `name_ko` · `name_en` · `name_en_source`(원장 / 보충) · `abbr` · `aliases`(`;`) · `kind` · `parent_code` · `tissue_code` · `description` · `basis`

- `kind`:
  - **부위** — 사람이 몸에서 가리키는 자리(얼굴 · 이마 · 미간 · 눈밑 · 턱 · 목 · 겨드랑이 · 두피 …).
  - **해부 구조** — 원장이 **이름을 붙여** 말한 혈관 · 신경 · 근육 · 샘(안면동맥 · 활차상동맥 · 안와상신경 · 교근 · 광경근 …). `tissue_code` 로 일반 조직(근육 · 혈관 …)에 잇고, `parent_code` 로 놓인 부위에 잇는다. tissue 사전에 맞는 일반명이 없으면(예: 신경) 잇지 말고 notes 「조직 추가 후보」.
- `parent_code`: 원장이 포함 관계로 적은 것만(얼굴 > 이마 · 눈가 > 눈밑). 원장으로 판단이 안 되면 비우고 notes 에.
- 좌·우, 상·하처럼 원장이 나눠 적은 것은 원장이 나눈 만큼만 행.

## 5. 규칙 (앞 사전들과 같은 기준)

1. **원장 표현만.** 원장에 없는 부위 · 해부 구조를 만들지 않는다. 영어 이름이 원장에 없으면 표준 표기로 채우되 `name_en_source` = 보충.
2. **이름 괄호 금지.** 「활차상동맥 (Supratrochlear artery)」 → name_ko 활차상동맥 · name_en Supratrochlear artery(원장). 「이마 (전두근)」 같은 겹침은 두 행으로 나누고 관계를 notes 에.
3. 한 부위 = 한 행. 같은 자리의 다른 표기(사각턱 · 턱각 · 하악각 등)는 원장이 같은 자리라고 확인될 때만 aliases, 아니면 합치지 말고 notes 에 후보.
4. **넣지 않는 것**: 깊이 · 직경 · 위험 등급 · 주행 경로 · 「안전 구역」 같은 **값과 성질**(나중 관계 단계 — 원문 위치만 notes 에 목록), 시술 · 고민(「사각턱」이 근육 비대 고민을 뜻하는 자리는 부위만 · 고민 낱말은 notes 「고민 후보」), 층(진피 · 피하지방층은 tissue).
5. 숫자로 바꾸지 않는다 — 「얕게」 「드물게」 같은 말은 사전 범위가 아니고, 바꾸지도 않는다.

## 6. 확인 (notes 에 표)

아래가 행 + 부모 + 조직 연결로 표현되는지: **이마**(> 얼굴) · **미간** · **눈밑** · **사각턱 / 교근**(부위 ↔ 해부 구조 근육) · **활차상동맥**(해부 구조 · 혈관 · > 이마) · **겨드랑이**(다한증 자리) · **두피**.
그리고 원장의 부위 언급 전부가 행에 붙었는지(못 붙인 것 목록 · 원장별 자리 수).

## 7. notes (짧게)

1. 행 수(kind 별 · 부모 있는 행 · tissue 연결 행) · 누락 확인 방법
2. 확인 사례 표
3. 합친 것 / 합치지 않은 후보(같은 자리 의심)
4. 조직 추가 후보 · 고민 후보 · 넣지 않은 값(깊이 · 등급 등) 원문 위치
5. 사용자 판단이 필요한 것 — 원문 · 이유 · 추천 · 선택지(판단 가능한 건 올리지 않는다)

## 8. 완료 기준

- 모든 행 basis · 이름 괄호 0 · tissue_code · parent_code 참조 전부 존재.
- 깊이 · 등급 · 시술 · 고민 · 가격 값 없음. 확인 사례 표현됨.
- `silver/`·원장 변경 없음 · 산출물 외 변경 없음(`git status`).

## 9. 완료 보고

막히면 원문 먼저, 사용자 선택이 필요하면 preamble 의 ask. 범위를 넓히지 않는다(외부 조사 · 관계 만들기 하지 않는다).
preamble 의 `worker_done` 을 정확히 한 번(`--outcome succeeded|failed`, `--report-path orchestration/work/phub-ledger-redesign/silver-model/drafts/site/site-notes.md`).
그다음 코디 터미널에 한 줄:
`orca terminal send --terminal term_107c16b1-6066-4654-9272-359649efd67f --text "site 사전 완료: orchestration/work/phub-ledger-redesign/silver-model/drafts/site/" --enter`
