# 발주서 — 실버 CSV 의 `;` 여러 값 칸 전부 풀기 (DB 모양으로)

너는 이 작업의 맥락이 없다. 이 문서 한 장과 「읽을 것」만으로 일한다.
작업 레포(코디 워크트리): `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온` — 아래 상대 경로는 `orchestration/work/phub-ledger-redesign/silver-model/` 기준.

## 1. 배경 · 사용자 결정

Procedure Hub 시술 원장의 실버 사전(`silver/` 11개 표 + 부위 초안 `drafts/site/site.csv`)에 칸 하나에 `;` 로 여러 값을 넣은 곳이 있다. DB 에 넣을 때 다대다는 별도 표가 필요하다. 사용자: **「나중에 까먹으면 어떡해 — 지금 다 푼다.」** 실버 CSV 가 곧 DB 적재 모양이 되게 한다.
**값은 하나도 바꾸지 않는다** — 칸에 있던 값을 표로 옮기기만 한다(추가 · 삭제 · 고침 · 합침 · 새 조사 없음).

## 2. 산출물

`drafts/silver-split/` 아래: 바뀐 표 전부(바뀌지 않는 표도 같은 폴더에 복사해 한 벌로) + 새 표 + `split-notes.md` + `split-check.py`(검증 스크립트).
출발점 = `silver/*.csv` 11개 + `drafts/site/site.csv`. CSV 는 UTF-8 BOM. `silver/`·`drafts/site/`·원장 변경 금지. 커밋·push 금지.

## 3. 읽을 것

- `silver/` 전부: modality · material · material_spec · mechanism · tissue · method · product · organization · product_organization · product_material · product_method
- `drafts/site/site.csv` · `site-notes.md`
- 먼저 **모든 표의 모든 칸**에서 `;` 가 든 칸을 전수 집계한다(코디가 본 것: aliases · abbr · basis · overview_basis · mechanism_basis · product.modality_code · material_spec.value · site.parent_code — 이 밖에 더 있으면 그것도 이 규칙으로, 규칙에 안 맞으면 notes 에 올리고 ask). 설명문(description · overview 등) 속 문장 부호 `;` 는 여러 값이 아니면 그대로 둔다 — 판정 목록을 notes 에.

## 4. 푸는 규칙

**A. 행 id** — 근거를 가리키려면 모든 행에 키가 있어야 한다.
- 사전 표는 기존 `code` 가 키.
- 관계 표(product_organization · product_material · product_method · 아래 새 관계 표)와 material_spec 에 `id` 칸을 맨 앞에 추가(접두어 예: PORG- · PMAT- · PMET- · SPEC- …, notes 에 목록).

**B. 이름 — 공통 표 `alias.csv`**
- 칼럼: `target_table` · `target_code` · `name` · `kind`(별칭 / 약어)
- 모든 표의 `aliases` · `abbr` 를 값 하나당 한 행으로 옮기고 **두 칸을 지운다.** name_ko · name_en · name_en_source 는 본 표에 그대로.

**C. 근거 — 공통 표 `source_ref.csv`**
- 칼럼: `target_table` · `target_id`(사전은 code, 관계 표는 새 id) · `field`(행 전체 근거면 빈칸, modality 의 overview_basis 처럼 칸별 근거면 그 칸 이름) · `ref`(원장 포인터 또는 URL 등 원래 값 그대로)
- 모든 `basis` · `*_basis` 를 값 하나당 한 행으로 옮기고 **칸을 지운다.** 원래 값에 `name_en: <URL>` 같은 접두가 붙어 있으면 field 로 옮길 수 있는 것은 옮기고(예: field = name_en), 판정 목록을 notes 에.

**D. 관계 — 칸에서 표로**
1. `product.modality_code` → `product_modality.csv`(`id` · `product_code` · `modality_code`) — **여러 값인 2행만이 아니라 전 제품**을 옮기고 칸을 지운다.
2. `material_spec.value` 의 여러 값(808;810 · 1540;1550) → 값마다 한 행(같은 재료 · 항목 · 단위). 근거는 두 행 모두에 같은 ref.
3. 부위 `site.parent_code` 를 둘로 나눈다(사용자 결정):
   - **포함 관계**(부위 > 부위, 예: 이마 > 얼굴) → `parent_code` 한 칸에 남긴다(값 하나).
   - **놓인 자리**(해부 구조 → 부위, 예: 교근 → 볼 · 턱선 · 활차상동맥 → 이마 · 미간) → `site_location.csv`(`id` · `structure_code` · `site_code`). **kind = 해부 구조인 행의 부모는 하나든 여럿이든 전부** 여기로 옮기고 그 행의 parent_code 는 비운다. 해부 구조 → 해부 구조 부모(있으면)는 notes 에 목록 + ask.
   - kind = 부위 인 행에 parent 가 여럿이면 notes 에 목록 + ask(나누지 말 것).
   - 근거: 원래 행 basis 에서 어느 ref 가 어느 관계 근거인지 원장으로 가를 수 있으면 해당 id 에, 못 가르면 사전 행(site code)에 둔다 — 지어내지 않는다.

**E. 지우지 않는 것** — 칸에 단일 값만 있던 다른 코드 칸(parent_code · tissue_code · current_org_code 등)은 그대로.

## 5. 검증 (`split-check.py` — 코디가 다시 돌린다)

- **왕복 검사**: 새 표들에서 원래 칸을 다시 조립(`;` 결합)하면 원래 CSV 값과 집합으로 같다 — 표 · 칸 · 행 단위로 차이 0. (순서는 무시, 중복 값은 notes 에.)
- 행 수: 사전 표 행 수 불변. alias · source_ref · product_modality · site_location 행 수 = 원래 값 개수 합.
- 모든 코드 · id 참조 존재. 결과 표 어느 칸에도 여러 값 `;` 0(설명문 예외 목록 제외).
- 실행 결과(통과/실패 · 집계)를 notes 끝에 붙인다.

## 6. notes (짧게)

1. 전수 집계(표 · 칸 · 여러 값 행 수 · 판정)
2. 새 표 · id 접두어 · 지운 칸 목록
3. 부위 나눔 결과(포함 n · 놓인 자리 n) · basis 를 가르지 못한 것
4. 사용자 판단이 필요한 것(원문 · 이유 · 추천 · 선택지)
5. 검증 결과

## 7. 완료 보고

막히면 원문 먼저, 사용자 선택이 필요하면 preamble 의 ask. 범위를 넓히지 않는다(부위 사전의 다른 결정 — 턱 · 동의어 합치기 · 영문 지점 · 비근근 — 은 하지 않는다).
preamble 의 `worker_done` 을 정확히 한 번(`--outcome succeeded|failed`, `--report-path orchestration/work/phub-ledger-redesign/silver-model/drafts/silver-split/split-notes.md`).
그다음 코디 터미널에 한 줄:
`orca terminal send --terminal term_107c16b1-6066-4654-9272-359649efd67f --text "silver-split 완료: orchestration/work/phub-ledger-redesign/silver-model/drafts/silver-split/" --enter`
