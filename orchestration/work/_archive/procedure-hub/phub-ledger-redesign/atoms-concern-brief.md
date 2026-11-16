# 발주서 — 기본 단위: 고민 사전

너는 이 작업의 맥락이 없다. 이 문서 한 장과 「읽을 것」만으로 일한다.
작업 레포(코디 워크트리): `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온` — 아래 상대 경로는 `orchestration/work/` 기준.

## 1. 목표 · 구조

Procedure Hub 는 **시술 원장**이다. 입구는 **고민** · 시술 이름 · 제품이다.
실버 3층: ① 기본 단위(사전) → ② 조합(시술 · 케이스) → ③ 관계(적응 = 케이스 × 고민 · 부작용 위험 · 금기 · 시너지 · 근거).
확정 실버(`phub-ledger-redesign/silver-model/silver/`, DB 모양): 사전 표(modality · material · mechanism · tissue · method · product · organization · **site**(부위) · **anatomy**(해부 구조)) + 관계 표(id) + 공통 `alias.csv`(target_table · target_code · name · kind: 별칭 / 약어 / 의학 용어) + 공통 `source_ref.csv`(target_table · target_id · field · ref).

이번 일: ① 중 **고민** 사전 — 사람이 시술을 찾게 만드는 상태·문제(주름 · 처짐 · 기미 · 여드름 · 다한증 …). **시술 · 효과 · 부작용과의 연결(관계)은 만들지 않는다.** 단 고민이 놓인 부위는 이번에 잇는다(아래 `concern_site`).

## 2. 산출물

`phub-ledger-redesign/silver-model/drafts/concern/`: `concern.csv` · `concern_site.csv` · `alias.csv`(고민 행만, 공통 표와 같은 칼럼) · `source_ref.csv`(고민 계열 행만) · `concern-notes.md` · `concern-check.py`
CSV 는 UTF-8 BOM. **`;` 여러 값 칸 금지**(여럿이면 행으로). `silver/`·원장 변경 금지. 커밋·push 금지.

## 3. 읽을 것

- 원장(브론즈 3판): `phub-recommend/bronze/phub-ledger/*.json` **21개 전부에서 고민을 가리키는 자리**. 특히:
  - taxonomy `problem[]`(P1~P14: category · subcategories[].label · items[].name · detail)
  - problem-packages(`problems[].complaints[]`: cc · cc_detail · cc_group) · problem-combos(`combos[]`)
  - procedure-profiles · patient-education · procedure-comparison · market-pricing 이름(**이름만**) · literature-evidence 등 본문 속 고민 표현
- `silver-model/drafts/site/site-notes.md` §4 「고민 후보」 — 부위 작업에서 모은 출발점(믿지 말고 원문 확인)
- 확정 사전 `silver/site.csv` · `silver/alias.csv`(부위 이름 · 의학 용어)
- 색인(누락 확인): `phub-ledger-redesign/first-pass/<원장>/source-map.json`

## 4. 테이블

**`concern.csv`** — `code`(CON-…) · `name_ko` · `name_en` · `name_en_source`(원장 / 보충) · `kind` · `parent_code` · `description`
- `kind`: 원장 고민 분류(주름 · 처짐 · 색소 · 여드름 · 모공 · 홍조/혈관 · 흉터 · 윤곽 · 체형 · 탈모 · 노화 · 기타 등) — 원장 category 를 바탕으로 정하고 notes 에 목록·근거.
- `parent_code`: 원장이 포함으로 적은 것만(주름 > 표정주름 > 미간주름 · 색소 > 기미). 원장 트리(category > subcategory > item)를 따르되, 그 층이 고민이 아니면(아래 5-2) 건너뛴다.
- 이름 = 원장 표현. 「팔자주름」처럼 부위 + 상태가 붙은 말도 **원장 표현 그대로 한 행**(쪼개 지어 넣지 않는다). 상태만인 상위 고민(「주름」)은 원장에 그 말이 있을 때만.

**`concern_site.csv`** — `id` · `concern_code` · `site_code`(→ `silver/site.csv`)
- 고민 이름·원장 문맥이 부위를 말할 때만(미간주름 → 미간 · 이중턱 → 턱밑 · 겨드랑이 다한증 → 겨드랑이). 부위가 특정되지 않는 고민(기미 · 여드름)은 행 없음.
- 부위 사전에 없는 자리가 필요하면 잇지 말고 notes 「부위 추가 후보」.

**`alias.csv`** — 같은 고민의 다른 표기(까치발 · 까마귀발 · crow's feet → 눈가주름 등). 원장이 같은 것이라고 확인되거나 같은 낱말의 표기 차이일 때만. 한자 의학 용어(비순구 등)는 kind 의학 용어 · 영어 표기는 별칭.

**`source_ref.csv`** — 모든 concern · concern_site 행에 원장 포인터 ≥ 1.

## 5. 규칙 (앞 사전들과 같은 기준)

1. **원장 표현만.** 원장에 없는 고민을 만들지 않는다. 영어 이름은 원장(category_en 등)에 없으면 표준 표기로 채우되 보충.
2. **고민이 아닌 것은 넣지 않는다** — 원장 고민 트리·cc 자리에도 섞여 있다: 시술 이름(「코필러」 · 「보톡스」 · 「쁘띠시술」) · 치료 방식(「주사치료」 · 「장비치료」 · 「약물치료」 · 「모발이식」) · 제품 · 효과/목표(「주름 개선」 · 「V라인 완성」 — 효과 사전 몫) · 부작용. 이런 자리는 notes 에 「고민 아님」 목록(원문 · 자리 · 무엇으로 보이나).
   - 단 목표가 상태를 가리키면(「제모」 → 원치 않는 털) 원장 표현으로 고민 행을 둘지 notes 에 사용자 판단으로 올린다(지어 넣지 않는다).
3. 이름 괄호 금지: 「눈가 주름(까치발)」 → name_ko 눈가주름 계열 + alias 까치발. 「오타모반/ABNOM」 같은 `/` 병기는 원장이 같은 것으로 적었으면 한 행 + alias, 다른 것이면 두 행.
4. 한 고민 = 한 행. 원장 곳곳의 같은 고민은 합치고 근거를 여럿 둔다. 같은지 원장으로 판단이 안 되면 합치지 말고 notes 에 후보.
5. 「드물게」 · 「얕게」 같은 말을 수치로 바꾸지 않는다. 심한 정도 · 원인 · 유형(예: 「피지과다형 모공」)은 원장이 별개 고민으로 적은 것만 행으로, 수식어는 description.

## 6. 확인 (notes 에 표)

아래가 행 + 부모 + 부위 연결로 표현되는지: **이마주름**(> 표정주름 > 주름 · → 이마) · **팔자주름**(→ 팔자) · **눈가주름 / 까치발**(alias) · **기미**(> 색소, 부위 없음) · **이중턱**(→ 턱밑) · **사각턱**(고민 — 부위 사각턱과 이름이 같아도 별개 행) · **다한증**(→ 겨드랑이 · 손바닥 · 발바닥 원장대로) · **여드름흉터**(> 흉터).
그리고 원장의 고민 언급 전부가 행에 붙었는지(원장별 자리 수 · 못 붙인 것 목록).

## 7. notes (짧게)

1. 행 수(kind 별 · 부모 있음 · 부위 연결) · 누락 확인 방법
2. 확인 사례 표
3. 합친 것 / 합치지 않은 후보
4. 고민 아님 목록(시술 · 치료 방식 · 효과 · 제품 …) · 부위 추가 후보
5. 사용자 판단이 필요한 것 — 원문 · 이유 · 추천 · 선택지

## 8. 완료 기준 (`concern-check.py`로 — 코디가 다시 돌린다)

- 모든 행 근거 ≥ 1 · 이름 괄호 0 · `;` 0 · parent · site_code 참조 존재 · name_ko 중복 0.
- 시술 이름 · 제품 · 가격 값이 concern 에 없음(제품 사전 이름과 대조).
- `silver/`·원장 변경 없음 · 산출물 외 변경 없음(`git status`).

## 9. 완료 보고

막히면 원문 먼저, 사용자 선택이 필요하면 preamble 의 ask. 범위를 넓히지 않는다(외부 조사 · 관계 만들기 하지 않는다).
preamble 의 `worker_done` 을 정확히 한 번(`--outcome succeeded|failed`, `--report-path orchestration/work/phub-ledger-redesign/silver-model/drafts/concern/concern-notes.md`).
그다음 코디 터미널에 한 줄:
`orca terminal send --terminal term_107c16b1-6066-4654-9272-359649efd67f --text "concern 사전 완료: orchestration/work/phub-ledger-redesign/silver-model/drafts/concern/" --enter`
