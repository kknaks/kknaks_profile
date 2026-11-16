# 발주서 — 부위 사전 확정: 해부 구조 분리 + 사용자 결정 4건 (silver 직접 수정)

너는 이 작업의 맥락이 없다. 이 문서 한 장과 「읽을 것」만으로 일한다.
작업 레포(코디 워크트리): `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온` — 아래 상대 경로는 `orchestration/work/phub-ledger-redesign/silver-model/` 기준.

## 1. 배경

Procedure Hub 시술 원장의 실버(`silver/`)는 `;` 여러 값을 다 푼 DB 모양이다: 사전 표 + 관계 표(id) + 공통 `alias.csv`(target_table · target_code · name · kind) + 공통 `source_ref.csv`(target_table · target_id · field · ref).
부위 사전 `site.csv`(kind 부위 119 · 해부 구조 108)와 `site_location.csv`(해부 구조 → 부위 89)가 들어와 있으나 미확정이다. 사용자가 아래를 정했다. **silver 에서 직접 고친다**(사용자 지시). 고치기 전 판은 `archive/site-before-finalize/` 에 복사해 둔다.

## 2. 읽을 것

- `silver/` 전부(특히 site · site_location · alias · source_ref · tissue)
- `notes/split-notes.md` · `drafts/site/site-notes.md`(§3 합치지 않은 후보 · §5 판단 목록)
- 원장: `../../phub-recommend/bronze/phub-ledger/*.json`(특히 `anatomy-danger-zones.json`) — 확인용, 고치지 않는다.

## 3. 할 일 (사용자 결정 — 그대로)

**A. 해부 구조를 별도 표로 분리**
- `anatomy.csv`(ANA-…): site 의 kind = 해부 구조 108행. 칼럼 = code · name_ko · name_en · name_en_source · kind(혈관 / 신경 / 근육 / 뼈 / 샘 / 기타 등 원장·이름으로 판정, 목록을 notes 에) · tissue_code · description.
- `site.csv`: 부위 행만. kind 칼럼은 지운다(하나뿐이면). tissue_code 칼럼도 부위에서 안 쓰면 지운다.
- `site_location.csv` → **`anatomy_site.csv`**(id · anatomy_code · site_code). id 접두어 바꿔도 된다.
- alias · source_ref 의 target_table · target_code 를 새 표에 맞게 옮긴다. 옛 SITE 코드 → ANA 코드 대응표를 notes 에.
- 뼈 · 근육 등 해부 구조는 시술 대상이 아니다 — 위치 기준·위험 표지로만 쓴다(description 에 쓸 필요는 없음, notes 한 줄).

**B. 턱 (결정 2)** — 턱 = 큰 개념.
- SITE-072 턱: name_en = jaw, name_en_source = 보충.
- 위험 구역 「턱 / Chin (Mentum)」(zones/8)은 **턱끝**에 대응: 턱끝 name_en = Chin(원장). 이부(Mentum)는 C 규칙대로 턱끝의 의학 용어로 합친다.
- zones/8 근거(source_ref)와 그 구역 해부 구조의 놓인 자리(anatomy_site)는 턱 → 턱끝으로 옮긴다. zones/8 밖 「턱」 근거는 턱에 그대로.
- 턱선 · 사각턱 · 턱밑의 부모는 원장에 포함 문장이 없으므로 비운 채 둔다.

**C. 같은 자리는 한 행 (결정 3)** — 원칙: **부위·해부 구조 모두, 같은 자리를 가리키는 말은 한 행.** 이름(name_ko)은 일반 용어, 한자 의학 용어는 alias `kind = 의학 용어`(새 값), 그 밖 표기는 `kind = 별칭`. 고민·부작용에서의 뉘앙스 차이는 여기서 가르지 않는다.
- 합칠 것(남는 이름 ← 합쳐지는 이름 · 의학 용어 표시):
  - 얼굴 ← 안면(의학) · 안면부(의학) · 전체얼굴 · 얼굴 전체 · 전안면(의학)
  - 눈 주변 ← 눈가 · 눈 주위 · 안와주위(의학) · 안와 주변(의학) · 안와 주변부(의학)
  - 관자놀이 ← 측두부(의학) · 측두 · 관자
  - 코등 ← 비배부(의학) · 콧등 / 코끝 ← 비첨부(의학) · 비첨(의학)
  - 팔자 계열 한 행(이름은 원장 일반 표현 중 「팔자」 쪽 — 팔자주름 행이면 그 행) ← 비순주름 · 비순구 · 비순홈(의학) · 법령선 · 코입술주름 · 팔자
  - 볼 ← 뺨 · 협부(의학) / 광대 ← 관골부(의학)
  - 입 주변 ← 구주위(의학) / 상순 쪽 한 행(일반 용어 윗입술을 이름으로) ← 상순(의학) · 상구순(의학)
  - 입꼬리 ← 구각(의학) · 구각부(의학) · 입가
  - 턱끝 ← 이부(의학) / 턱밑 ← 턱 아래 / 목 ← 경부(의학)
  - 허벅지 ← 대퇴부(의학) / 복부 ← 배 / 전신 ← 바디 · 체부(의학)
  - 중안면 · 중안면부 · 중면부 한 행(일반 용어 쪽 이름)
  - 해부 구조: 안동맥 ← 눈동맥 · 코뼈 ← 비골(의학) · 광대뼈 ← 관골뼈(의학) · 광대근 ← 관골근(의학)
- **합치지 않는 것**(범위가 다름 — 같은 자리가 아님): 눈꺼풀 ↔ 윗눈꺼풀 ↔ 하안검(전체 ↔ 위 ↔ 아래 — 부모로 잇는다, 원장 포함 문장 없으면 notes) · 천측두동맥 ↔ 천측두동정맥 · 하악각(뼈) ↔ 사각턱(부위) · 관골뼈(뼈) ↔ 광대(부위) · 체간 ↔ 전신 · 목선/네크라인 ↔ 목.
- 위 목록에 없는 같은-자리 후보(예: 관자궁 ↔ 관골궁 · 상측두융합선 ↔ 측두선 · 목선 ↔ 네크라인)를 발견하면 합치지 말고 notes 에 근거와 추천.
- 합칠 때: 지워지는 행의 source_ref · alias · anatomy_site · parent_code 참조를 남는 행으로 옮기고 중복 제거. 지워지는 행의 name_ko 는 남는 행의 alias(의학 용어 / 별칭)로. 지운 코드 → 남은 코드 대응표를 notes 에. (아직 케이스가 없어 코드 삭제 가능.)

**D. 영문 해부 지점 추가 (결정 4)** — anatomy 에 Pitanguy line(zones/2 tissue_data · clinical_pearls · taxonomy 1곳) · Rhinion(zones/4) 두 행. name_ko 는 원장 표기 그대로 영문, name_en 같은 값(원장). anatomy_site 는 구역 레코드대로(관자놀이 · 코). 근거는 원장 포인터.

**E. 비근근 (결정 5)** — 코 구역 「비근근 (Nasalis)」(현 SITE-249)은 원장 오기로 보고 **name_ko = 비근**(사용자 판단, 영어 기준). 원장 표기 「비근근」은 그 행의 alias(kind 별칭)로 남기고, description 에 「원장 표기 비근근은 오기 — 사용자 판단으로 영어(Nasalis) 기준 정정」. 미간 구역 비근근(Procerus)은 그대로. `notes/site-ledger-check-list.csv`(what · 원장 포인터 · 원장 값 · 판단 · note)에 이 건을 올린다(원장 작성자 확인용). 원장은 고치지 않는다.

## 4. 산출

- 고친 `silver/` 표들 + 새 `silver/anatomy.csv` · `silver/anatomy_site.csv`(site_location.csv 는 지운다).
- `notes/site-finalize-notes.md`: 행 수(전/후) · SITE→ANA 대응 · 합친 표 · 남긴 후보 · B·D·E 결과 · 검증 결과
- `notes/site-ledger-check-list.csv`
- `notes/site-finalize-check.py`: 검증 스크립트.

## 5. 검증 (스크립트로 — 코디가 다시 돌린다)

- 모든 참조 존재(alias · source_ref 의 target · anatomy_site · parent_code · tissue_code).
- 어느 칸에도 여러 값 `;` 0 · 이름 괄호 0 · 모든 사전 행에 source_ref 1개 이상.
- 근거 보존: 고치기 전 site/site_location 의 source_ref ref 집합 = 고친 뒤 site/anatomy/anatomy_site 의 ref 집합(새로 넣은 D 제외). alias 이름 보존: 전 alias 이름 + 지워진 행 name_ko ⊆ 후 alias 이름 ∪ name_ko.
- 다른 사전·관계 표(site 계열 외)의 내용 불변.

## 6. 완료 보고

막히면 원문 먼저, 사용자 선택이 필요하면 preamble 의 ask. 범위를 넓히지 않는다(고민 · 관계 만들기 · 외부 조사 하지 않는다).
preamble 의 `worker_done` 을 정확히 한 번(`--outcome succeeded|failed`, `--report-path orchestration/work/phub-ledger-redesign/silver-model/notes/site-finalize-notes.md`).
그다음 코디 터미널에 한 줄:
`orca terminal send --terminal term_107c16b1-6066-4654-9272-359649efd67f --text "site 확정 완료: orchestration/work/phub-ledger-redesign/silver-model/notes/site-finalize-notes.md" --enter`
