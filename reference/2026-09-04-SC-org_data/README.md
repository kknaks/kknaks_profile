# SC 조직도 CSV → ax-workspace dataset

이 폴더의 조직도 CSV 한 장(169행 · 14열)을 ax-workspace 가 읽는 dataset 표로 옮기고, 로컬 데모 데이터베이스에
넣는다. **CSV 원본과 여기서 만든 dataset 폴더는 Git 밖에 둔다** — 저장소는 코드만 갖는다.

이 문서에는 사람의 이름·전화·생년월일·메일 주소를 적지 않는다. 개수와 규칙만 적는다.

---

## 실행법

```bash
# 1) dataset 폴더의 빈 표를 만든다 (폴더가 없을 때 import 가 대신 만들어 준다)
make dataset-import TARGET=~/scax-datasets/the-sc

# 2) CSV → 표 채우기 (표준 라이브러리만 · 멱등)
python3 build_dataset.py "더에쓰씨_조직도_2026-09-02(검수2)_상세추가.csv" ~/scax-datasets/the-sc

# 3) 검사만 (데이터베이스는 그대로)
SCAX_DATASET_PASSWORD=scax-demo-1234 make dataset-import TARGET=~/scax-datasets/the-sc DATASET_ARGS=--dry-run

# 4) 적재
SCAX_DATASET_PASSWORD=scax-demo-1234 make dataset-import TARGET=~/scax-datasets/the-sc
```

`make` 는 ax-workspace 워크트리 루트에서 돈다. `SCAX_DATASET_PASSWORD` 가 없으면 계정(logins)은 만들지 않고
넘어간다 — 조직만 들어간다. 2·4 를 몇 번 다시 돌려도 결과는 같다.

---

## 최종 매핑표

CSV 열 14개 중 **7개만** 들어간다.

| CSV 열 | dataset | 규칙 |
|---|---|---|
| 부서 | `organization_units` (`division`) | slug 표(`DEPT_SLUGS`) · 부모는 회사 루트 `the-sc` · `display_order` 는 CSV 첫 등장 순 |
| 팀 | `organization_units` (`team`) | slug 표(`TEAM_SLUGS`) · 부모는 그 행의 부서 · 빈 칸이면 부서 직속 |
| 이름 | `members.display_name` | 그대로 |
| 직급 | `grades` + `members.grade_key` | `GRADE_SLUGS` 10종 · `display_order` 는 서열 순(사원 1 … 대표이사 10) |
| 고용형태 | `members.employment_type` | 정규직 → `regular` · 시간제 → `part_time` · 빈 칸은 빈 칸 · 그 밖의 값은 경고 후 빈 칸 |
| 직책 | `positions` + `appointments` | 부서장 → (`division`,`head`) · 팀장 → (`team`,`head`) · 부팀장 → (`team`,`deputy`) |
| 입사일 | `members.employed_from` | 적힌 사람만. 없는 사람은 비운다 |
| 위하고메일 | `logins.email` | 적힌 사람만 계정을 만든다. 비밀번호는 폴더에 없고 적재할 때 환경이 준다 |
| 전화 | `members.phone` | 적힌 사람만. 숫자와 하이픈만 남긴다 |
| 생년월일 | `members.birth_date` | 적힌 사람만. ISO(`YYYY-MM-DD`)로 적는다 |
| 비고 | (저장 안 함) | 「겸임」 표시만 읽어 사람 병합에 쓴다 |
| 메모 · 지메일 · 담당 프로젝트 | **미반입** | — |

파생 열:

| dataset 열 | 어디서 오나 |
|---|---|
| `members.key` | **임시 사번** — 병합 후 사람 순서(CSV 첫 등장)로 `1001`부터. 원문에 사번 열이 없다 |
| `members.employment_state` | 전원 `active` — CSV 에 퇴사 표시가 없다 |
| `members.primary_unit_key` | 그 사람이 CSV 에 **처음 나온 행**의 팀(없으면 부서) |
| `members.role_key` | 직급이 대표이사면 `executive` · 직책이 있으면 `team-lead` · 나머지 `member` |
| `memberships.kind` | 첫 소속 `primary` · 나머지 `additional` |
| `appointments.kind` | 주소속에서 맡은 보직 `primary` · 나머지 `concurrent` |

빈 표(헤더만): `jobs` · `job_assignments` · `projects` · `project_assignments`.
예제 8표(`scenario_*`)는 채우지 않는다 — 조직만 넣는다.

---

## 결정 (2026-09-07 사용자 결정)

1. **사번은 임시 번호다.** `members.key` = `1001`부터의 4자리. 스키마는 바꾸지 않는다. 화면이 이 key 를 사번
   자리에 보여 준다.
2. **겸임자의 주소속은 CSV 에서 먼저 나오는 행이다.** 판정은 이름이 아니라 규칙이다 — 「비고에 겸임 + 같은 이름 +
   앞 행에 이미 겸임으로 나옴」이면 같은 사람의 두 번째 소속. 스크립트에 사람 이름 상수를 두지 않는다.
3. **이름이 같아도 「겸임」이 없으면 다른 사람이다.** 동명이인은 병합하지 않고 각자 key 를 받는다.
4. **부서 단계의 「팀장」은 부서장 자리로 넣는다.** 부서에는 head 슬롯이 하나뿐이다. 해당 행은 경고로 남긴다.
5. **대표이사는 `role_key` 만 대표 역할이고 직책 행이 없다.** CSV 의 직책 열이 비어 있어 직급이 유일한 근거다.
6. **`logins` 는 위하고메일이 적힌 사람만** (지메일이 아니다). 주소가 없는 사람은 계정 없이 들어간다.
7. **전화·생년월일은 `members` 의 옵셔널 열이다** (2026-09-07 추가, dataset schema v6). 원문이 말한 사람만
   갖고 나머지는 비어 있다. 명부 API 는 이 두 값을 **`organization.manage` 권한이 있는 Principal 에게만**
   채워 주고, 없으면 필드는 그대로 두고 값만 `null` 이다.

### 계약에 맞추느라 바꾼 것 — `sc-` 접두사

`grades` 와 `position_definitions` 는 **조직을 묻지 않는 전역 표**다. 같은 데모 데이터베이스에 서 있는 예시
회사(SCAX)가 이미 `associate`(대리) · `director`(부장) 를 쓰고 있는데 SC 는 같은 키를 **주임 · 이사**로 쓴다.
importer 는 이미 있는 key 를 덮어쓰지 않으므로 접두사 없이 넣으면 화면에 「주임」이 「대리」로 나온다.

그래서 SC 어휘에는 `sc-` 를 붙인다 (`sc-associate` · `sc-dept-head` …). 접두사를 뺀 뒷부분은 sc-org 선행
적재의 slug 표 그대로다. **부서·팀·사람 key 는 접두사가 필요 없다** — 예시 회사와 겹치지 않는다.

예시 회사를 지우면(`make reset-catalog`) 접두사 없이도 되지만, 그러면 데모 로그인 계정이 사라져 화면을 열 수
없다. 지우지 않는 쪽을 골랐다.

---

## 결과 (2026-09-07 적재)

| 표 | 행 | 비고 |
|---|---|---|
| `organization_units` | 29 | 회사 1 · 부서 10 · 팀 18 |
| `grades` | 10 | — |
| `positions` | 3 | — |
| `members` | 165 | 원본 169행 − 겸임 병합 4행 |
| `memberships` | 169 | `primary` 165 · `additional` 4 |
| `appointments` | 22 | `primary` 18 · `concurrent` 4 |
| `logins` | 15 | 위하고메일이 없는 150명은 계정 없음 |
| `members.phone` | 15 | 전화가 적힌 사람만 |
| `members.birth_date` | 15 | 생년월일이 적힌 사람만 |
| `jobs` · `job_assignments` · `projects` · `project_assignments` | 0 | CSV 에 직무 열이 없다 |

역할: `executive` 2 · `team-lead` 18 · `member` 145.
고용형태: `regular` 124 · `part_time` 39 · 빈 칸 2.
`employed_from`: 15명만. 나머지 150명의 재직 시작 시각은 **레코드 자신의 기본값**(적재 시각)이 되며, 원문의
입사일을 지어낸 것이 아니다.

경고 1건: 팀 없이 「팀장」인 행 1개 → 부서장(`sc-dept-head`) 자리.

---

## 알아 둘 것

- **`division` 은 화면에 「본부」로 나온다.** 조직 단위 종류 이름은 제품 catalog 가 갖고 있고, SC 의 「부서」에
  해당하는 종류가 따로 없다. 이름을 바꾸려면 제품 쪽 결정이 필요하다.
- CSV 는 **현재 시점 스냅샷 한 장**이다. 기간·과거값이 없어 소속·직책 이력은 시드로 채워지지 않는다.
- 직무 축(`jobs`)은 CSV 에 열 자체가 없어 비어 있다.
- `members.phone`·`members.birth_date` 컬럼은 **로컬 데모 DB 에 `make sync-demo-schema` 로만** 들어가 있다.
  운영 스키마 반영은 별도 gate다.
- 전화·생년월일·입사일·위하고메일은 모두 **같은 15명**에게만 있다. 나머지 150명은 네 값이 전부 비어 있다.
