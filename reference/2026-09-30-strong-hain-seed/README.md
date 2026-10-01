# Strong Hajin 실제 유저 시드 — 조직도 전체

조직도에 들어가는 것은 전부 여기서 받는다. 프로젝트·업무는 유저가 앱에서 만든다.
표 모양은 코드(`backend/src/ax_workspace/modules/datasets/schema.py`)가 읽는 그대로다 — 열을 더하거나 빼면 거절된다.

각 표의 `예시-삭제` 행은 모양 보기용이다. **지우고 채운다**(남기면 그대로 들어간다).
`key` 는 영문·숫자 식별자다. 한 번 넣으면 id 가 되니 나중에 바꾸지 않는다.

## 1. 조직 구조

### `organization_units.csv` — 조직
| 열 | 필수 | 값 |
|---|---|---|
| `key` | ○ | 조직 식별자 |
| `name` | ○ | 조직 이름 |
| `unit_type` | ○ | `company` · `division`(본부) · `office`(실) · `team` · `part`(파트) |
| `parent_key` | | 상위 조직 key. 최상위(회사)는 비운다 |
| `display_order` | | 같은 상위 안에서의 순서(정수) |

## 2. 어휘 — 조직에서 쓰는 목록

### `grades.csv` — 직급 (사원·대리·과장·이사…)
| `key` ○ | `name` ○ | `display_order`(높은 직급부터 1,2,3…) |

### `positions.csv` — 직위·보직 (대표이사·본부장·팀장·부팀장…)
| 열 | 필수 | 값 |
|---|---|---|
| `key` | ○ | |
| `name` | ○ | |
| `unit_type` | ○ | 이 직위가 붙는 조직 종류(팀장이면 `team`) |
| `slot` | | `head`(장) · `deputy`(부). 장·부가 아니면 비운다 |
| `role_key` | | 이 직위가 주는 권한(아래 §4). 비우면 그 사람 자신의 권한을 쓴다 |

### `jobs.csv` — 직무 (개발·디자인·인사·재무…)
| `key` ○ | `name` ○ |

## 3. 사람

### `members.csv` — 한 사람 한 줄
| 열 | 필수 | 값 |
|---|---|---|
| `key` | ○ | 사람 식별자(사번 등) |
| `display_name` | ○ | 이름 |
| `employment_state` | ○ | `active`(재직) · `ended`(퇴사) |
| `employment_type` | | `regular`(정규) · `part_time` · `contract` |
| `primary_unit_key` | ○ | 주 소속 조직 key |
| `role_key` | ○ | 권한(§4) |
| `grade_key` | | 직급 key |
| `employed_from` | | 입사일 `YYYY-MM-DD` |
| `employed_until` | | 퇴사일 `YYYY-MM-DD`. 재직 중이면 비운다 |
| `phone` | | 전화 |
| `birth_date` | | 생년월일 `YYYY-MM-DD` |

### `appointments.csv` — 누가 어느 조직에서 무슨 직위인가
직위 없는 사람은 줄을 만들지 않는다. 겸직·공동 대표는 여러 줄.
| `member_key` ○ | `unit_key` ○ | `position_key` ○ | `kind` ○ `primary` · 겸직이면 `concurrent` | `valid_from` | `valid_until` |

### `memberships.csv` — 추가 소속 (겸임 부서)
주 소속은 `members.primary_unit_key` 가 자동으로 만든다. **두 번째 소속이 있을 때만** 적는다.
| `member_key` ○ | `unit_key` ○ | `kind` ○ `additional` | `valid_from` | `valid_until` |

### `job_assignments.csv` — 누가 무슨 직무인가
| `member_key` ○ | `job_key` ○ | `kind` ○ `primary` · 부직무면 `additional` |

### `logins.csv` — 로그인
| `member_key` ○ | `email` ○ |
한 사람 한 줄. 비밀번호는 표에 없다 — 적재할 때 환경변수로 준다.

## 4. 권한 (`role_key`)

`guest` · `member` · `team-lead` · `project-participant` · `project-lead` · `people-manager` · `executive`.
조직 관리(권한 부여·명부 전체)는 `people-manager`·`executive` 만 한다 — **최소 1명은 둘 중 하나여야 한다.**

## 5. 적재

코디가 빈 `projects.csv`·`project_assignments.csv` 와 `manifest.yaml` 을 붙여 `make dataset-import` 로 넣는다.
근거·운영 적재 선택지: `orchestration/work/strong-hajin-deploy/research-seed-path.md`
