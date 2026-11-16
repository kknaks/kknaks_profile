# 발주서 — 계열 · 시술 종류 · 케이스 3층 시범 (M1 · M9 · M8)

너는 이 작업의 맥락이 없다. 이 문서 한 장과 「읽을 것」만으로 일한다.
작업 레포(코디 워크트리): `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온` — 아래 경로는 이 레포 기준.

## 1. 목표 · 배경

피부과 시술 원장 21개를 실버로 정규화한다. 확정: `silver-model/data/modality.csv`(계열 M1~M17).
직전 시범(`silver-model/data/pilot-set/`)은 시술 정체에 **작용 대상**까지 넣어서 보톡스가 셋(보톡스·스킨보톡스·다한증)으로, 레이저가 표적·파장마다 29개로 갈렸다. 사용자와 다시 정한 구조:

```text
계열(modality)  →  시술 종류(procedure_type)  →  케이스(procedure_case)
M1 보톡스        →  보톡스 (1개)                →  근육·사각턱 / 피지샘·진피 희석 다점(=스킨보톡스) / 땀샘·겨드랑이(다한증)
M9 기기 리프팅   →  RF · HIFU · 마이크로웨이브 …  →  써마지·얼굴 / 울쎄라·SMAS·턱선 …
```

| 층 | 무엇이 다르면 다른 행인가 |
|---|---|
| 계열 | 원장 묶음(확정 · 손대지 않음) |
| **시술 종류** | **재료·에너지의 종류 + 작용 원리** 만. 작용 대상·부위·방법·제품·파장은 시술 종류를 가르지 않는다 |
| **케이스** | 시술 종류 + 작용 대상 · 부위 · 방법 · 제품 · 세부 재료(파장 등) — **원장이 실제로 말한 조합만** |

- 보톡스: 시술 종류 1개. 스킨보톡스(=메조보톡스=더모톡신, 사용자 확정)·다한증 보톡스는 **케이스**(이름 있는 케이스).
- 기기 리프팅: 에너지 종류가 다르면(고주파 / 집속 초음파 / 마이크로웨이브 …) 다른 시술 종류.
- 레이저: 시술 종류는 **재료 종류(레이저 빛 / IPL 광대역 빛 …) + 원리(선택적 광열 / 광음향 / 박피 / 비박피 미세 열손상 / 조직 가열 …)**. 표적(멜라닌·혈관·모낭)과 파장(1064nm·755nm…)·프락셔널 여부는 **케이스**로 내린다. 원리 값은 원장 문장으로 정한다.

**시범 범위: M1 보톡스 · M9 기기 리프팅 · M8 레이저** 셋뿐. 다른 계열·부위 테이블·제품 테이블·다른 개체와의 연결은 하지 않는다.

## 2. 산출물 (새 폴더 · 이것만)

`orchestration/work/phub-ledger-redesign/silver-model/data/pilot-3level/` 아래:
`procedure_type.csv` · `procedure_case.csv` · `material.csv` · `tissue.csv` · `item-judgment.csv` · `pilot-3level-notes.md`

CSV 는 **UTF-8 BOM**(`utf-8-sig`) · 쉼표 · 필요한 칸 큰따옴표. 그 밖의 파일(기존 `silver-model/data/**` 포함)은 읽기만. 커밋·push 금지.

## 3. 읽을 것

- 원장(브론즈 3판): `orchestration/work/phub-recommend/bronze/phub-ledger/*.json` — M1·M8·M9 에 해당하는 것 전부(taxonomy `modality[0]`·`[7]`·`[8]` 하위분류·항목·제품 · extracted `M1`·`M8`·`M9` · procedure-profiles · procedure-comparison · pih-risk · patient-education · products.json 해당 섹션 · market-pricing · taxonomy problem 쪽 해당 메뉴).
- 확정: `silver-model/data/modality.csv` · `modality-notes.md`(§2 하위로 넘긴 기전 문장 — 시술 종류 기전으로 쓴다).
- **직전 시범(재사용)**: `silver-model/data/pilot-set/` — item-judgment(M1·M8 판정 대부분 재사용 가능 · 「케이스」 대상이 바뀐다) · material · tissue · notes. 판정을 처음부터 다시 하지 말고 새 구조에 맞게 고친다. M9 는 새로.
- 색인(누락 확인): `first-pass/<원장>/source-map.json`.

## 4. 테이블 칼럼

**`procedure_type.csv`** — `code`(PT-…) · `name_ko` · `name_en` · `modality_code` · `material_code`(재료 **종류** — 레이저 빛·고주파·집속 초음파·보툴리눔 톡신 …) · `principle`(짧은 값) · `overview` · `mechanism` · `basis`
- 계열과 1:1 인 경우(보톡스): 개요·기전은 **시술 종류에** 둔다. 계열 쪽 문장과 겹치면 notes 에 「계열 overview 를 묶음 수준 한 줄로 바꿀 후보」로 적는다(modality.csv 는 고치지 않는다).

**`procedure_case.csv`** — `code`(PC-…) · `procedure_type_code` · `case_name`(원장에 이름이 있을 때만: 스킨보톡스 · 다한증 보톡스 …) · `case_name_alias`(같은 케이스를 부르는 다른 이름 — 원문으로 같은 것임을 확인한 것만: 메조보톡스·더모톡신) · `target_code`(→ tissue) · `site_text`(부위 원문 — 부위 테이블 전이라 원문 그대로) · `method`(방법: 깊이·희석·주사 패턴·프락셔널 여부 등 원장에 있을 때) · `material_detail_code`(세부 재료: 1064nm 등 → material 의 하위 행) · `product_text`(제품 원문 — 제품 테이블 전이라 원문 그대로) · `basis`
- **원장이 실제로 말한 조합만** 행으로. 모든 부위×대상 조합을 만들지 않는다. 같은 조합이 여러 원장에 나오면 한 행 + basis 여럿.
- 「보톡스 터치업」 같은 회차·일정은 케이스가 아니다(item-judgment 에 `회차·일정` 으로).

**`material.csv`** — `code` · `name_ko` · `name_en` · `kind`(물질/에너지/기계적 자극) · `parent_code` · `description` · `basis`. 시술 종류가 쓰는 **종류** 행과, 케이스가 쓰는 **세부** 행(parent 로 종류를 가리킴)만. 한 개념 한 행.

**`tissue.csv`** — `code` · `name_ko` · `name_en` · `kind`(층/구조/표적) · `parent_code` · `description` · `basis`. 케이스가 쓰는 것만. 병변·미생물·혈류·모공은 넣지 않는다.

**`item-judgment.csv`** — `source` · `pointer` · `name` · `judgment`(시술 종류 / 케이스 / 제품 / 메뉴 / 성분 / 분류 칸 / 회차·일정 / 시술 아님 / 재분류) · `procedure_type_code` · `procedure_case_code` · `reason`
- 조합 메뉴(「보톡스 + 필러 + HIFU」)는 `메뉴` — 가리키는 시술 종류를 `;` 로 여럿 적어도 된다(연결은 나중).

## 5. 공통 규칙

원장에 있는 값만 · 외부 지식 보충 금지 · 문맥으로 판단 가능한 것은 판단. 이름은 그 이름이 **실제로 무엇을 가리키는지** 원문으로 확인한 대상에만. 판단 가능한 것은 판단하고 notes 에 근거만.

## 6. notes 형식

1. 집계(계열 × 판정) · 누락 확인 방법
2. 시술 종류 목록(계열별: 이름 · 재료 종류 · 원리 · 나눈 이유 한 줄)
3. 케이스 요약(시술 종류별 케이스 수 · 이름 있는 케이스)
4. 직전 시범(pilot-set) 대비 바뀐 점
5. 사용자 판단이 필요한 것 — 원문 · 이유 · 추천 · 선택지(정의로 판단 가능한 건 올리지 않는다)

## 7. 완료 기준

- M1·M8·M9 원장 항목이 전부 item-judgment 에 판정돼 있다.
- 시술 종류가 재료 종류 + 원리로만 나뉘었다(표적·파장·부위로 갈린 시술 종류가 없다). 케이스는 원장이 말한 조합만이다.
- material·tissue 에 시술 종류·케이스가 쓰지 않는 값이 없고, 종류/세부가 parent 로 이어졌다.
- 산출물 외 변경 없음(`git status`).

## 8. 질문 · 9. 완료 보고

막히면 원문을 먼저 확인하고, 사용자 선택이 필요하면 preamble 의 ask. 범위를 넓히지 않는다.
preamble 의 `worker_done` 을 정확히 한 번(`--outcome succeeded|failed`, `--report-path orchestration/work/phub-ledger-redesign/silver-model/data/pilot-3level/pilot-3level-notes.md`).
그다음 코디 터미널에 한 줄:
`orca terminal send --terminal term_107c16b1-6066-4654-9272-359649efd67f --text "pilot-3level 완료: orchestration/work/phub-ledger-redesign/silver-model/data/pilot-3level/" --enter`
