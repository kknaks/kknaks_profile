# 발주서 — 기본 단위: 효과 사전 (+ 효과 → 고민)

너는 이 작업의 맥락이 없다. 이 문서 한 장과 「읽을 것」만으로 일한다.
작업 레포(코디 워크트리): `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온` — 아래 상대 경로는 `orchestration/work/` 기준.

## 1. 목표 · 구조

Procedure Hub 는 **시술 원장**이다. 실버 3층: ① 기본 단위(사전) → ② 조합(시술 · 케이스) → ③ 관계(적응 · 케이스→효과 · 부작용 위험 · 금기 · 시너지 · 근거).
확정 실버(`phub-ledger-redesign/silver-model/silver/`, DB 모양 — `;` 여러 값 칸 없음): 사전 표(modality · material · mechanism · tissue · method · product · organization · site · anatomy · **concern**(고민, 대·중·소 3단 · 명사형 이름 · 자세한 설명)) + 관계 표(id) + 공통 `alias.csv`(target_table · target_code · name · kind: 별칭/약어/의학 용어) + 공통 `source_ref.csv`(target_table · target_id · field · ref).

이번 일: ① 중 **효과** 사전 — 시술로 생기는 결과(주름 개선 · 모공 축소 · 리프팅 · 볼륨 증가 · 광채 · 톤 밝아짐 …)와, 시술과 상관없이 **말뜻으로 정해지는 효과 → 고민** 연결만.
**하지 않는 것**: 케이스/시술 → 효과 · 효과가 나타나는 시점·지속 기간 · 기전 → 효과 · 문헌 근거 연결(모두 관계 단계 — 원문 위치만 notes 에 모은다).

## 2. 산출물

`phub-ledger-redesign/silver-model/drafts/effect/`: `effect.csv` · `effect_concern.csv` · `alias.csv`(효과 행만, 공통 표와 같은 칼럼) · `source_ref.csv`(효과 계열 행만) · `effect-notes.md` · `effect-build.py` · `effect-check.py`
CSV 는 UTF-8 BOM. `;` 여러 값 칸 금지. `silver/`·원장 변경 금지. 커밋·push 금지. 빌드 스크립트는 레포 안(이 폴더)에 둔다.

## 3. 읽을 것

- 원장(브론즈 3판): `phub-recommend/bronze/phub-ledger/*.json` **21개 전부에서 효과를 가리키는 자리**. 특히:
  - taxonomy 항목·제품·계열의 `extracted/indications/primary|secondary|extended`(「주름 개선」 등 효과형 적응증) · `extracted/overview` · `mechanism` 속 결과 표현
  - literature-evidence `categories/*/effects/*`(statement · patient_ko)
  - problem-combos `packages/*/expectedResult` · `riskBenefit` · combo-recipes `goal` · `expectedResults` · problem-packages(procedures[].role 등)
  - patient-education · procedure-profiles · procedure-comparison · treatment-optimization 속 효과 표현 · market-pricing 이름(**이름만**)
- 확정 사전: `silver/concern.csv`(+ alias) · `silver/mechanism.csv`(+ alias) — 기전과 겹치는지 대조
- 고민 작업 기록(같은 방식 참고): `silver-model/drafts/concern/concern-notes.md`(특히 §4 「고민 아님」 중 효과/목표 목록 · §7 v2 방식)
- 색인(누락 확인): `phub-ledger-redesign/first-pass/<원장>/source-map.json`

## 4. 테이블

**`effect.csv`** — `code`(EFF-…) · `name_ko` · `name_en` · `name_en_source`(원장 / 보충) · `level`(대분류 / 중분류 / 소분류) · `parent_code` · `description`
- **3단**: 모든 행은 대분류 하나 아래. 대분류는 원장 효과 표현을 묶는 말(예: 주름 개선 · 탄력 · 리프팅 · 볼륨 · 톤/미백 · 피부결 · 윤곽 · 체형 …)로, **원장에 있는 말** 중에서 정하고 근거를 단다. 중분류는 원장이 묶는 말이 있을 때만. 자식 없는 중분류는 그 자체가 끝 단계(복제 행 만들지 않음). 깊이 ≤ 3.
- **이름 = 명사형**(「대상 + 변화 명사」: 주름 개선 · 모공 축소 · 피부톤 밝아짐 → 원장에 명사형이 있으면 그것). 원장 형용사·동사형 표현은 alias(별칭). 뜻이 바뀌면 바꾸지 말고 notes 판단 목록.
- **설명**: 원장 문장을 근거로 자세하게 — 무엇이 어떻게 달라지는지 · 원장이 말하는 범위 · 비슷한 효과와의 차이(원장이 가르는 대로, 안 가르면 「원장이 적지 않는다」) · 합쳐진 별칭. 「」 인용은 원장 글자 그대로, 근거는 source_ref(field = description). **원장에 없는 임상 사실 금지.** 「드물게」 「얕게」를 수치로 바꾸지 않는다.

**`effect_concern.csv`** — `id` · `effect_code` · `concern_code`(→ `silver/concern.csv`)
- 효과가 **말뜻으로** 해결하는 고민(주름 개선 → 주름 대분류 · 모공 축소 → 모공 확대). 원장이 「○○ 개선」처럼 고민 말을 직접 쓴 것, 또는 원장이 둘을 같은 자리에서 짝지은 것만. 가장 맞는 층(대·중·소)에 잇고, 아래 단계로 다 펼치지 않는다.
- 고민에 대응하지 않는 효과(광채 · 리프팅감 등)는 행 없음.
- 근거는 source_ref(target_table = effect_concern).

## 5. 규칙

1. **원장 표현만.** 원장에 없는 효과를 만들지 않는다. 영어 이름이 원장에 없으면 표준 표기 + 보충.
2. **효과가 아닌 것은 넣지 않는다**: 몸 안의 작용(콜라겐 생성 · 근육 이완 · 멜라닌 파괴 — 기전 사전 몫, 이미 있으면 notes 에 기전 코드와 함께) · 고민 자체(주름 · 기미 — 고민 사전) · 시술 이름 · 부작용 · 수치(지속 기간 · 개선율). notes 「효과 아님」 목록.
   - 기전과 효과 경계가 애매한 말(예: 「피부 재생」 「탄력 증가」)은 원장 문맥이 **결과로 보이는 변화**를 말하면 효과, **몸 안의 작용**을 말하면 기전 — 판단 못 하면 notes 판단 목록.
3. 이름 괄호 금지. 「주름 개선 (잔주름뿐만 아니라 굵은 주름도)」 → 이름 주름 개선, 괄호 풀이는 설명.
4. 한 효과 = 한 행. 같은 변화를 가리키는 말은 합치고(일반 말 이름, 한자 의학 용어는 alias kind 의학 용어, 나머지 별칭), 범위·대상이 다르면 나눈다. 애매하면 나누고 notes 에.

## 6. 확인 (notes 에 표)

아래가 행 + 부모 + 고민 연결로 표현되는지: **주름 개선**(→ 주름) · **모공 축소**(→ 모공 확대) · **리프팅**(→ 처짐) · **볼륨 증가 / 볼륨 회복**(→ 볼륨 손실) · **피부톤 밝아짐 / 미백**(→ 피부 칙칙함 · 색소) · **광채**(고민 연결 없음) · **V라인**(→ 윤곽 계열, 원장대로).
그리고 원장의 효과 언급 전부가 행에 붙었는지(원장별 자리 수 · 못 붙인 것).

## 7. notes (짧게)

1. 행 수(level 별 · 대분류별 · 고민 연결) · 누락 확인 방법
2. 확인 사례 표
3. 합친 것 / 합치지 않은 후보
4. 효과 아님 목록(기전 · 고민 · 시술 · 수치 …)
5. **관계 단계 몫 원문 위치**: 케이스/시술 → 효과(어느 원장 어느 칸) · 시점·지속(onset/duration/peak 칸) · 기전 → 효과 문장 · 문헌 근거(literature effects) — 목록·개수만
6. 사용자 판단이 필요한 것 — 원문 · 이유 · 추천 · 선택지

## 8. 완료 기준 (`effect-check.py` — 코디가 다시 돌린다)

- level · 3단 규칙(대분류 parent 없음 · 모두 대분류에 닿음 · 깊이 ≤ 3) · 이름 괄호 0 · `;` 0 · name_ko 중복 0 · 형용사·동사형 이름 = notes 판단 목록과 같음.
- 모든 effect · effect_concern 행 근거 ≥ 1 · description 있음 · 「」 인용이 원장 글자 그대로(근거 말단 안) · 참조 전부 존재(concern_code).
- 효과 이름이 concern · mechanism 이름 · alias 와 겹치는 것 = notes 목록과 같음.
- `silver/`·원장 변경 없음 · 산출물 외 변경 없음(`git status`).

## 9. 완료 보고

막히면 원문 먼저, 사용자 선택이 필요하면 preamble 의 ask. 범위를 넓히지 않는다(관계 만들기 · 외부 조사 하지 않음).
preamble 의 `worker_done` 을 정확히 한 번(`--outcome succeeded|failed`, `--report-path orchestration/work/phub-ledger-redesign/silver-model/drafts/effect/effect-notes.md`).
그다음 코디 터미널에 한 줄:
`orca terminal send --terminal term_107c16b1-6066-4654-9272-359649efd67f --text "effect 사전 완료: orchestration/work/phub-ledger-redesign/silver-model/drafts/effect/" --enter`
