# 발주서 — material · tissue 실버 데이터 CSV (phub-ledger-redesign)

너는 이 작업의 맥락이 없다. 이 문서 한 장과 「읽을 것」만으로 일한다.
작업 레포(코디 워크트리): `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온` — 아래 경로는 이 레포 기준.

## 1. 목표 · 배경

피부과 시술 원장 21개를 실버로 정규화하고 있다. 개체를 하나씩 확정하고, **연결 관계는 개체가 다 선 뒤에** 그린다(사용자 지시 — 연결부터 생각하다 설계가 꼬였다).
확정된 것: `modality.csv`(M1~M17 · `silver-model/data/`).

다음은 **시술(procedure)** 이다. 사용자와 정한 시술의 정의:
> **시술 = 재료·에너지(material) + 작용 대상 조직(tissue) + 작용 원리가 같으면 같은 시술.** 셋 중 하나라도 다르면 다른 시술.
> 예: 보톡스(톡신 · **근육** · 아세틸콜린 차단) ≠ 스킨보톡스(=메조보톡스 · 톡신 · **피지샘·모공(진피)** · 아세틸콜린 차단). 이마든 사각턱이든 보톡스는 한 시술 — **부위(이마·턱)는 시술의 정체가 아니다**(부위는 별도 테이블, 나중에 연결).

시술 테이블이 `material_code` · `target_code`(→ tissue) 로 이 두 테이블을 가리키므로, **이번 일은 material 과 tissue 두 테이블의 값 목록을 원장에서 정규화해 CSV 로 만드는 것**이다. 시술 목록·부위·제품·연결은 하지 않는다.

## 2. 산출물 (이 셋만)

- `orchestration/work/phub-ledger-redesign/silver-model/data/material.csv`
- `orchestration/work/phub-ledger-redesign/silver-model/data/tissue.csv`
- `orchestration/work/phub-ledger-redesign/silver-model/data/material-tissue-notes.md` (짧게, 표 위주)

CSV 는 **UTF-8 BOM**(`utf-8-sig`) · 쉼표 구분 · 필요한 칸은 큰따옴표. 그 밖의 파일은 만들거나 고치거나 지우지 않는다. 원장·`first-pass/`·`silver-model/` 다른 파일은 읽기 전용. 커밋·push 금지.

## 3. 읽을 것

- 원장(브론즈 3판 · 최신 기준): `orchestration/work/phub-recommend/bronze/phub-ledger/*.json` — 특히 taxonomy `modality[]` 의 하위분류 label·항목 name/detail/extracted(overview·mechanism)·products(ingredient·material·type) · extracted `M*`(overview·mechanism·related_techniques) · products.json(ingredient·material·type) · procedure-profiles(mechanism·moa_summary) · procedure-comparison(mechanism_simple) · anatomy-danger-zones(safe_injection_depth·filler_specific.safe_technique — 층 이름) · pih-risk(procedures 이름 속 파장·에너지).
- 확정분: `silver-model/data/modality.csv`, `silver-model/data/modality-notes.md`(하위 층으로 넘긴 기전 문장 — material·tissue 근거로 쓸 수 있다).
- 색인(누락 확인용): `first-pass/<원장>/source-map.json`. first-pass 의 해석은 믿지 말고 원문으로 판단.

## 4. 테이블 정의

### `material.csv` — 시술이 몸에 넣거나 가하는 재료·에너지

| 칼럼 | 내용 |
|---|---|
| `code` | MAT-001 … |
| `name_ko` · `name_en` | 대표 이름 |
| `kind` | 물질 / 에너지 / 기계적 자극 (원장 값으로 필요하면 추가하되 이유를 notes 에) |
| `description` | 한 문장 정의 — 원장 문장에서 가져오거나 추림. 원장에 없으면 비움 |
| `basis` | 근거 원장 위치(포인터, `;` 로 여럿) |

규칙
- **시술의 기전을 가르는 단위**로 잡는다. 예: 보툴리눔 톡신 A형 · 히알루론산 · PMMA · CaHA · PLLA · PCL · PDO · 자가혈(PRP) · 자가지방 · 고주파(RF) · 집속 초음파(HIFU) · 레이저/광(파장은 원장이 기전을 가르면 따로) · 전자기 · 냉각 · 플라즈마 · 화학 박피제 · 영양 성분 · DCA 등 — 목록은 예시일 뿐, 원장 값으로 정한다.
- **제품·장비 브랜드는 넣지 않는다**(쥬비덤·울쎄라·보툴렉스는 제품 — 다음 단계). 「국산·수입」 같은 분류 칸도 아니다.
- 같은 재료의 다른 표기(「HA」「히알루론산」「Hyaluronic acid」)는 한 행. 다른 이름은 notes 에 「합친 표기」로 적는다(별칭 테이블은 만들지 않는다).
- 상하위로 보이는 것(AHA > 글리콜산, 레이저 > 1064nm)은 이번엔 평평하게 행으로 두고 notes 에 「상위 후보」만 적는다.

### `tissue.csv` — 시술이 작용하는 조직(작용 대상)

| 칼럼 | 내용 |
|---|---|
| `code` | TIS-001 … |
| `name_ko` · `name_en` | 대표 이름 |
| `kind` | 층(깊이) / 구조(근육·피지샘·땀샘·모낭·혈관·지방세포 등) / 표적 물질(멜라닌·헤모글로빈·물 등 빛을 흡수하는 표적) — 원장 값으로 필요하면 조정, 이유는 notes |
| `description` | 한 문장 정의 — 원장 문장 근거. 없으면 비움 |
| `basis` | 근거 원장 위치 |

규칙
- **부위가 아니다.** 이마·눈가·턱선·코는 넣지 않는다(부위 테이블은 따로). 「작용 대상」은 근육·진피·피지샘·피하지방·SMAS·멜라닌처럼 **무엇에 작용하는가**다.
- **이름 있는 해부 구조(전두근·교근·활차상동맥·이신경)는 넣지 않는다** — 일반 조직 수준(근육·혈관·신경)만. 특정 근육·혈관은 부위와 함께 나중에 다룬다.
- 원장이 주입·작용 층으로 쓰는 이름(진피층·피하지방층·골막상·SMAS·supraSMAS·근육층 등)은 층으로 넣는다. 같은 층의 다른 표기(「진피층」「진피」「dermis」)는 한 행.

## 5. 공통

- 원장에 있는 값만. 외부 지식으로 항목·설명을 보충하지 않는다. 문맥으로 판단 가능한 것은 판단해서 채운다.
- 값을 고를 때 **이 값이 시술 하나 이상의 정체(재료 또는 작용 대상)로 실제 쓰이는가**를 기준으로 한다. 원장에 스쳐 나온 성분(화장품 성분 나열 등)까지 전부 넣지 않는다 — 넣지 않은 경계 사례는 notes 에.

## 6. notes 형식

1. 합친 표기(같은 값의 다른 이름 · 원장 위치)
2. 상위 후보(평평하게 둔 것)
3. 넣지 않은 경계 사례와 이유(브랜드 · 부위 · 이름 있는 구조 · 스쳐 나온 성분 등)
4. 판단이 안 된 것(원문 · 이유) — 사용자 선택이 필요한 것만, 추천과 함께

## 7. 완료 기준

- 두 CSV 의 모든 행에 basis 포인터가 있다. 브랜드·부위·이름 있는 해부 구조가 섞이지 않았다.
- 원장 21개에서 시술의 재료·작용 대상으로 쓰이는 값이 빠지지 않았다(어떻게 확인했는지 notes 머리에 한 단락).
- 산출물 셋 외 변경 없음(`git status`).

## 8. 질문

막히면 원문을 먼저 확인하고, 그래도 사용자 선택이 필요하면 preamble 의 ask 로 묻는다. 범위를 넓히지 않는다(시술 목록·부위·제품·연결로 넘어가지 않는다).

## 9. 완료 보고

preamble 의 `worker_done` 을 정확히 한 번(`--outcome succeeded|failed`, `--report-path orchestration/work/phub-ledger-redesign/silver-model/data/material-tissue-notes.md`).
그다음 코디 터미널에 한 줄:
`orca terminal send --terminal term_107c16b1-6066-4654-9272-359649efd67f --text "material-tissue 완료: orchestration/work/phub-ledger-redesign/silver-model/data/" --enter`
