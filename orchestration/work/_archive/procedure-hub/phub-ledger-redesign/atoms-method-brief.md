# 발주서 — 기본 단위: 방법 사전

너는 이 작업의 맥락이 없다. 이 문서 한 장과 「읽을 것」만으로 일한다.
작업 레포(코디 워크트리): `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온` — 아래 경로는 이 레포 기준.

## 1. 목표 · 구조

Procedure Hub 는 **시술 원장**이다. 실버는 3층: ① 기본 단위(사전) → ② 조합(시술 = 재료 + 기전 · 케이스 = 시술 + 작용 대상·부위·**방법**·제품) → ③ 관계.
확정된 사전(`orchestration/work/phub-ledger-redesign/silver-model/silver/`): 계열 `modality.csv` · 재료 `material.csv`(+ `material_spec.csv`) · 기전 `mechanism.csv` · 작용 대상 조직 `tissue.csv`.

이번 일은 ① 중 **방법(method)** 사전이다. 방법 = **시술을 어떻게 하느냐**:
| 무엇 | 예 |
|---|---|
| 재료 | 글루타치온 · 고주파 · 보툴리눔 톡신 |
| 기전 | 항산화 · 조직 가열 · 아세틸콜린 차단 |
| **방법** | 정맥 투여 · 진피 국소 주입(희석 · 미세 다점) · 모노폴라/바이폴라 RF · Q-스위치/롱펄스 · 프락셔널 · 캐뉼러/니들 · 미세 채널로 경피 흡수 |

시술·케이스 목록, 부위, 제품, 관계는 만들지 않는다.

## 2. 산출물 (작업 중 폴더에)

`orchestration/work/phub-ledger-redesign/silver-model/drafts/method/` 아래: `method.csv` · `method-notes.md`
CSV 는 **UTF-8 BOM**(`utf-8-sig`) · 쉼표 · 필요한 칸 큰따옴표. 다른 파일은 읽기만(`silver/` 확정본 포함). 커밋·push 금지.

## 3. 읽을 것

- 출발점: `silver-model/drafts/method-candidates.csv`(13행 — 재료·기전 사전에서 「방법」이라 빼 둔 것. 그대로 믿지 말고 원문 확인)
- 확정 사전(겹치지 않게 확인용): `silver-model/silver/material.csv` · `mechanism.csv` · `tissue.csv` · `atoms-notes.md`(§ 경계 판정)
- 원장(브론즈 3판): `orchestration/work/phub-recommend/bronze/phub-ledger/*.json` — **방법을 말하는 자리**에서만:
  - taxonomy 항목·제품 `detail`(「Q-switched」「롱펄스」「비박피성」「모노폴라」 등) · `extracted.mechanism`·`overview` 의 시행 방식 문장
  - extracted `M*` overview·mechanism · procedure-comparison `mechanism_simple` · procedure-profiles `practicalNotes`·`prepNotes`
  - anatomy-danger-zones `filler_specific.safe_technique`·`botox_specific`·`clinical_pearls`(캐뉼러 · 볼루스 · fan · 선형 역행 · 다점 · 흡인 등)
  - treatment-sequence·combo-recipes 등에서 시행 방식을 말하는 문장
- 색인(누락 확인): `first-pass/<원장>/source-map.json`

## 4. 테이블 `method.csv`

`code`(MET-…) · `name_ko` · `name_en` · `name_en_source`(원장/보충) · `abbr` · `aliases`(`;`) · `kind` · `parent_code` · `from_code`(method-candidates 에서 온 행이면 원래 코드) · `description` · `basis`

`kind` 는 아래 중 하나(원장 값으로 꼭 필요하면 추가하되 이유를 notes 에):
- `투여 경로` — 정맥 투여 · 피하 · 피내 · 근육 내 · 도포
- `주입 방식` — 미세 다점 · 볼루스 · fan · 선형 역행 · 희석 주입 · 니들리스 고압 분사
- `도구` — 니들 · 캐뉼러 · 롤러 · 스탬프 · 전동 펜
- `에너지 조사 방식` — Q-스위치 · 롱펄스 · 피코초 펄스? (피코는 기전 「광음향」으로 이미 갈림 — 방법으로 둘지 notes 에 판정) · 프락셔널(분획) · 저에너지 반복 조사(토닝) · 모노폴라 · 바이폴라 · 접촉 냉각
- `흡수 촉진` — 피부 장벽 일시 개방 · 이온 도입 · 전기천공 · 초음파 투과 · 미세 채널 형성

## 5. 규칙 (사용자 합의 · 앞선 사전과 같은 기준)

1. 방법을 말하는 자리에서만 모은다. 기준: 「이 값이 시술·케이스를 하는 방식으로 실제 쓰이는가」.
2. **한 개념은 한 행, 한 테이블.** 확정 사전(재료·기전·조직)에 이미 있는 개념은 넣지 않는다. 경계(예: 프락셔널 = 방법 / 비박피 미세 열손상 = 기전? · 피코초 = 기전 광음향 / 방법 펄스?)는 notes 에 근거와 판정 — 확정 사전을 고치지 않고, 고쳐야 한다고 보면 「사용자 판단」으로 올린다.
3. 상·하위는 `parent_code`(예: 니들 > 마이크로니들 · 프락셔널 > 박피성 프락셔널 / 비박피성 프락셔널). 같은 층에 상·하위를 나란히 두지 않는다.
4. **이름 3칸**: `name_ko`(한국어) · `name_en`(영어 · 원장에 없으면 표준 용어로 채우되 `name_en_source`=보충) · `abbr`(약어). **이름에 괄호를 쓰지 않는다** — 약어는 abbr, 다른 표기는 aliases, 설명은 description.
5. 이름은 원장 표현을 쓴다. 원장에 없는 방법을 지어 만들지 않는다.
6. **넣지 않는 것**: 부위(이마·턱선) · 층(진피·골막상 — tissue 사전) · 용량·수량·회차(케이스·상품의 칸) · 제품·장비 브랜드 · 재료·기전 · 관리 지침(시술 후 냉찜질 등 — 시술을 하는 방식이 아님).
7. 원장에 없는 사실 보충 금지. 문맥으로 판단 가능한 것은 판단한다.

## 6. 확인 (완료 전)

notes 에 표로: 아래 사례가 확정 사전 + 방법 사전으로 표현되는지 — **스킨보톡스**(톡신 · 아세틸콜린 차단 · 피지샘 · 진피 희석 미세 다점) · **백옥주사**(글루타치온 · 항산화 · 정맥 투여) · **써마지**(고주파 · 조직 가열 · 모노폴라) · **레이저토닝 vs 제네시스토닝**(1064nm · 선택적 광열 · Q-스위치 저에너지 반복 vs 롱펄스) · **CO2 프락셔널**(CO2 레이저 · 박피 · 프락셔널) · **필러 코등**(HA · 채움 · 캐뉼러 · 골막상) · **MTS + 앰플**(미세바늘 · 미세 상처 치유 · 미세 채널 형성).

## 7. notes 형식 (짧게)

1. 행 수(kind 별) · method-candidates 13행이 어디로 갔는지
2. 확인 사례 표
3. 경계 판정(방법 ↔ 기전 · 재료 · 조직)
4. 넣지 않은 것(규칙 6 분류별 예)
5. 사용자 판단이 필요한 것 — 원문 · 이유 · 추천 · 선택지(판단 가능한 건 올리지 않는다)

## 8. 완료 기준

- 모든 행 basis · 이름 괄호 0 · 확정 사전과 겹치는 개념 0 · 상·하위 parent.
- method-candidates 13행이 전부 method.csv 에 있거나 빠진 이유가 notes 에 있다. 확인 사례가 표현된다.
- 산출물 외 변경 없음(`git status` — `silver-model/` 은 미추적이라 산출물 경로만 새로 생겼는지 확인).

## 9. 질문 · 완료 보고

막히면 원문 먼저, 사용자 선택이 필요하면 preamble 의 ask. 범위를 넓히지 않는다.
preamble 의 `worker_done` 을 정확히 한 번(`--outcome succeeded|failed`, `--report-path orchestration/work/phub-ledger-redesign/silver-model/drafts/method/method-notes.md`).
그다음 코디 터미널에 한 줄:
`orca terminal send --terminal term_107c16b1-6066-4654-9272-359649efd67f --text "method 사전 완료: orchestration/work/phub-ledger-redesign/silver-model/drafts/method/" --enter`
