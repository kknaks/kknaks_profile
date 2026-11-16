# 발주서 — modality 실버 데이터 CSV (phub-ledger-redesign)

너는 이 작업의 맥락이 없다. 이 문서 한 장과 「읽을 것」만으로 일한다.
작업 레포(코디 워크트리): `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온` — 아래 경로는 이 레포 기준.

## 1. 목표

taxonomy.json 의 `modality[]` 17개(M1~M17 · 시술 분류의 맨 위)를 실버 테이블 두 개의 **실제 데이터 CSV** 로 만든다. 연결 관계(하위 시술·제품·부작용 등)는 하지 않는다.

## 2. 산출물 (이 셋만 만든다)

- `orchestration/work/phub-ledger-redesign/silver-model/data/modality.csv`
- `orchestration/work/phub-ledger-redesign/silver-model/data/modality_alias.csv`
- `orchestration/work/phub-ledger-redesign/silver-model/data/modality-notes.md` — 근거·하위로 넘긴 문장 메모(짧게)

그 밖의 파일은 만들거나 고치거나 지우지 않는다. 원장·`first-pass/`·`silver-model/` 다른 파일은 읽기 전용. 커밋·push 하지 않는다. CSV 는 UTF-8(BOM 없음) · 쉼표 구분 · 필요한 칸은 큰따옴표로 감싼다.

## 3. 읽을 것

1. 원장(브론즈 3판): `orchestration/work/phub-recommend/bronze/phub-ledger/*.json`
   - 정체·이름: `taxonomy.json:/modality[]` 의 `id`·`category`·`category_en`
   - 설명 근거: `extracted.json:/M{n}`(overview·mechanism — 정본) · `taxonomy.json:/modality[i]/extracted`(복사본·대조용) · `patient-education.json` 의 해당 범주(simple_explanation·how_it_works·patient_name) · `procedure-profiles.json` 의 해당 profile(moa_summary·name·name_en) · 하위분류·항목 이름(공통성 판단용)
2. 참고: `orchestration/work/phub-ledger-redesign/silver-model/family-design.md` §3(이름 표기 목록 — 이미 모아 둔 것)·§4(TX↔EX 차이). 다시 모으지 말고 이것을 출발점으로 쓰되 원문으로 확인한다.

## 4. 테이블 정의

### `modality.csv` — 17행

| 칼럼 | 내용 |
|---|---|
| `code` | M1 … M17 |
| `name_ko` | taxonomy `category` |
| `name_en` | taxonomy `category_en` |
| `overview` | 이 modality **아래 시술 전부에 맞는 공통 수준**의 개요 1~2문장 |
| `mechanism` | 이 modality **아래 시술 전부에 맞는 공통 수준**의 기전 1~3문장 |
| `overview_basis` | overview 를 만든 원문 위치(포인터, `;` 로 여럿) |
| `mechanism_basis` | mechanism 을 만든 원문 위치 |

**overview · mechanism 쓰는 규칙 (사용자 지시)**
- modality 층에는 **공통인 것만** 쓴다. 예 — 기기 리프팅(M9): 원장 mechanism 은 RF(고주파) 전용 문장이지만, 공통 수준은 「장비로 전달한 에너지가 피부 속에서 열로 바뀌어 콜라겐을 수축시키고, 시간이 지나며 섬유모세포를 자극해 새 콜라겐·엘라스틴이 생성된다」이다. RF 고유 내용(「이온 운동 없이…」「감각·운동신경을 자극하지 않아…」)은 쓰지 않는다.
- 문장은 **원장 문장에서 가져오거나 원장 문장을 공통 수준으로 추린 것**만. 원장에 없는 사실을 보충하지 않는다(외부 지식 금지). 추릴 때 뜻을 바꾸지 않는다.
- 공통성 판단은 그 modality 의 하위분류·항목 이름과 원장 설명을 보고 한다. **잘못 들어간 소속은 판단에서 뺀다**: M16 수액치료의 DCA(지방세포파괴)·지방분해주사(마케팅명)·기타 중 정맥 수액이 아닌 항목 / 볼뉴머(M4 의 RF 장비) 등 — 무엇을 뺐는지 notes 에 적는다.
- 보톡스·필러처럼 원장 문장이 이미 공통이면 그대로(정본 = extracted). 단 extracted M2 mechanism 끝 「자가지방이식은 …」 문장은 M6 이야기라 뺀다. 필러 mechanism 의 「칼슘 기반 필러는 … 콜라겐 생성 촉진」처럼 일부 재료만의 문장도 공통이 아니면 뺀다.
- M15 메디컬스킨케어(묶음): overview 는 묶음 정의(「피부과에서 시행하는 전문 피부 관리 시술의 총칭 — 필링·약물 도포·… 등」, 원장 patient-education 표현 활용). 공통 기전이 원장 문장으로 서지 않으면 mechanism 을 비우고 notes 에 이유를 적는다. 다른 modality 도 공통 기전을 원장 문장으로 세울 수 없으면 비운다(지어내지 않는다).

### `modality_alias.csv`

| 칼럼 | 내용 |
|---|---|
| `modality_code` | M1 … |
| `alias` | 표기 원문 |
| `alias_type` | 코드 / 한글 / 영문 / 환자용 |
| `ledger` | 원장 파일명 |
| `pointer` | 첫 위치(같은 원장 반복은 하나) |

- 원장마다 그 modality **자신을** 부르는 이름·코드. 정식 이름(`name_ko`·`name_en`)과 같은 표기는 넣지 않는다. 같은 alias 가 여러 원장에 있으면 원장마다 한 행.
- 넣는다: `M1-BOTOX` 같은 procedure_id · 다른 한글 이름(「에너지기기(HIFU/RF)」「PRP/엑소좀」「기기리프팅」「리프팅기기」「크라이오」 등) · 영문 이름(profiles·extracted·literature) · 환자용 이름(patient-education `patient_name`) · synergy 의 「M1-보톡스」형 표기.
- 넣지 않는다: 범위 키(`M1_to_M7`)·하위 코드(`M16-DCA`·`M8-토닝`)·항목 코드(`M8-1-1`)·「M3-스컬트라」처럼 접두 + 항목·제품 이름·타임라인 슬러그·products 섹션 키 — 하나의 modality 를 부르는 이름이 아니다.

### `modality-notes.md` (짧게, 표 위주)
1. modality 별로 공통성 판단에서 뺀 소속(무엇·왜).
2. modality 층에 쓰지 않고 **하위 층으로 넘긴 원장 문장**(원문 · 포인터 · 어느 하위(예: RF)로 갈 문장인지).
3. mechanism 을 비운 modality 와 이유.

## 5. 완료 기준

- `modality.csv` 17행, 모든 overview·mechanism 칸이 값이 있거나 비운 이유가 notes 에 있다. 각 값에 basis 포인터가 있다.
- overview·mechanism 이 하위 시술 전부에 맞는 공통 수준이고, 원장에 없는 사실이 없다.
- `modality_alias.csv` 가 규칙대로 채워졌다.
- 산출물 셋 외 변경 없음(`git status` 확인).

## 6. 질문

막히면 원문을 먼저 확인하고, 그래도 사용자 선택이 필요하면 preamble 의 ask 로 묻는다. 범위를 넓히지 않는다.

## 7. 완료 보고

preamble 의 `worker_done` 을 정확히 한 번(`--outcome succeeded|failed`, `--report-path orchestration/work/phub-ledger-redesign/silver-model/data/modality-notes.md`).
그다음 코디 터미널에 한 줄:
`orca terminal send --terminal term_107c16b1-6066-4654-9272-359649efd67f --text "modality-data 완료: orchestration/work/phub-ledger-redesign/silver-model/data/" --enter`
