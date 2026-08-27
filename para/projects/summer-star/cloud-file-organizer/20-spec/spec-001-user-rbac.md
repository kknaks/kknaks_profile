---
type: spec
id: CFO-SPEC-001
title: "User & RBAC"
status: stable
product: cloud-file-organizer
version: 0.0.1
created_at: 2026-07-08
updated_at: 2026-07-08
tags:
  - product/cloud-file-organizer
  - doc/spec
  - status/stable
  - user
  - rbac
  - access-control
links:
  baselines:
    - "[[baseline-002-department-document-management-direction]]"
  decisions:
    - "[[decision-006-read-access-from-user-attributes]]"
    - "[[decision-016-read-access-policy-and-boolean-vector]]"
    - "[[decision-017-global-sensitive-policy-source]]"
    - "[[decision-018-sensitive-document-preset-approval]]"
  specs:
    - "[[spec-002-organization-tree]]"
  works: []
  releases: []
  related: []
---

# User & RBAC

이 spec은 제품 내부 사용자 원장과 읽기 권한(RBAC) 판정의 외부 계약을 정의한다. cloud-file-organizer v1은 기존 Mediness PostgreSQL의 `public.users` 데이터를 seed source로 사용해 제품 내부 사용자/RBAC 기준을 만든다. Google social login은 붙이지 않는다. Google Drive OAuth는 사용자 로그인과 분리된 connector 설정이며 env로 주입한다.

## 1. Context

### Meta

- Decision reference: DEC-006, DEC-016, DEC-017, DEC-018
- Baseline reference: BASE-002
- Related spec: SPEC-002 Organization & Tree
- Domain note: 사용자 원장은 Mediness `public.users`를 seed source로 하되, 권한 판정 소속 기준은 조직도 노드 매핑이다.
- Open questions: 없음

### Business Requirement

사용자는 자신의 role/소속/직급에 따라 읽을 수 있는 문서만 탐색해야 하고, admin은 민감 문서를 포함한 전체 문서와 승인 게이트/관리 화면에 접근할 수 있어야 한다. 이를 위해 기존 Mediness 사용자 데이터를 제품 내부 user 원장으로 seed하고, 문서 read policy와 사용자 속성을 매칭하는 판정 계약을 정의한다.

### Scope

In scope:

- seed source(`mediness.public.users`)와 seed 대상 필드 계약
- product user model field 계약
- seed 값 분포(enum 후보)
- login boundary (social login 미사용, Drive OAuth 분리)
- 읽기 권한 판정 규칙 (admin 전체 열람, 축별 match, `ANY`/`ALL`/`PRESET`)
- visibility contract (계정 상태/policy 기반 노출 규칙)
- boolean vector의 성격(판정 결과/log)
- admin 허용 행위

Out of scope:

- Google social login 구현
- Drive OAuth connector 구현 상세
- 사용자 password/JWT 발급 구현 상세
- 조직도/문서 트리 상세 spec
- 문서 metadata record 상세 spec

## 2. UX Contract

### Placement

RBAC의 UX 표면은 로그인 화면과 "권한 없는 문서가 아예 보이지 않는" 탐색 결과다. (참고 시안: `21-html/login-rbac.html`)

```text
+--------------------------------------------------+
| Login: email 기반 product user 세션               |
+--------------------------------------------------+
| 탐색 화면: readable 문서만 목록/트리/검색에 노출    |
+--------------------------------------------------+
```

### U-1. 로그인

- **상태**:
  - product user(active): 로그인 후 탐색 화면으로 진입한다.
  - `active=false` 또는 `resigned_at` 존재: 로그인 후 문서 접근이 차단된다.
- **문구**:
  - 안내 badge: `Google social login 없음`
  - Drive 안내: `Drive OAuth는 사용자 로그인과 분리`
- **CTA**:
  - `로그인`: product user 계정(email) 기준.
- **기대 결과**:
  - 사용자는 개별 Google 계정 연동 없이 product user로 로그인한다.

### U-2. 권한 없는 사용자/문서 숨김

- **상태**:
  - read policy 불만족 문서: 목록/트리/검색/관련 문서에서 제거된다. 잠금 표시하지 않는다.
  - `department_node_id` 없음: 일반 문서 탐색 제한, 조직 매핑 필요 안내를 표시한다.
  - admin session: 민감 문서 포함 전체 열람이 가능하다.
- **문구**:
  - badge: `권한 없는 문서는 보이지 않음`
  - 매핑 필요 안내: `조직 매핑 필요`
- **CTA**: 없음 (숨김이 기본 동작이다).
- **기대 결과**:
  - 일반 사용자는 자신이 읽을 수 없는 문서의 존재를 알 수 없다.

## 3. User Scenario

### S-1. Member — 로그인과 탐색 제한

1. member 사용자가 로그인한다.
2. 시스템은 `active`, `resigned_at`, `department_node_id`를 확인한다.
3. 정상 계정이면 문서 목록/트리/검색에서 read policy를 만족하는 문서만 노출된다.
4. read policy를 불만족하는 문서는 목록/트리/검색/관련 문서에서 숨겨진다.
5. `department_node_id`가 없으면 일반 문서 탐색이 제한되고 admin 보정 대상이 된다.

### S-2. Admin — 전체 접근

1. admin 사용자가 로그인한다.
2. admin은 민감 문서(`sensitivity=sensitive`, `access_logic=PRESET` 포함)를 포함한 모든 문서를 읽을 수 있다.
3. admin은 승인 게이트와 관리 화면에 접근한다.
4. admin은 조직 매핑 실패 사용자의 RBAC를 보정한다.

### S-3. System — seed 재실행

1. 운영자가 `mediness.public.users` seed를 재실행한다.
2. 시스템은 `source_user_id` 기준으로 기존 product user row를 찾는다.
3. 같은 원본 user는 새 row 생성 없이 기존 row가 멱등 upsert된다.
4. 조직도 노드 매핑은 이름 규칙으로 시도되고, 실패분은 admin 보정 대상으로 남는다.

## 4. Interface Contract

### API Contract

| Method | Path | 요약 | 권한 |
|---|---|---|---|
| POST | `/auth/login` | product user 로그인 (`{email, password}`) | public |
| POST | `/auth/refresh` | refresh cookie로 access token 갱신 | refresh cookie |
| POST | `/auth/logout` | 세션 종료, refresh cookie 삭제 | authenticated |
| GET | `/auth/me` | 현재 사용자/권한 속성 조회 | authenticated |

> 구현 확정(WORK-001): email + password 인증. 데모 비밀번호는 seed 시 공통 부여(`SEED_DEFAULT_PASSWORD`, bcrypt hash 저장). JWT access token(Bearer) + refresh token은 httpOnly cookie `refresh_token`(SameSite=Lax, Path=/auth). 비활성/퇴사 계정은 로그인 403.

### Source Seed

기준 seed source:

| 항목 | 값 |
|---|---|
| 원본 환경 | `ssh medi-me` -> Lima `master` VM -> k8s PostgreSQL |
| namespace | `mediness-dev` 우선, `mediness-prod`는 비교/검증용 |
| database | `mediness` |
| table | `public.users` |
| row count 확인일 | 2026-07-08 |
| dev/prod row count | 26 / 26 |

원본 users table의 seed 대상 필드:

| Source Field | 사용 |
|---|---|
| `id` | `source_user_id`로 보존 |
| `email` | login/account identifier |
| `name` | 사용자 표시명 |
| `active` | 계정 활성 여부 |
| `role` | RBAC role |
| `position` | 직급/책임 수준 |
| `department` | 소속 부서 |
| `employment_type` | 고용 형태 참고값 |
| `first_login` | profile/activation 판단 참고 |
| `last_login` | 운영 참고 |
| `resigned_at` | 퇴사/비활성 판단 참고 |

### Product User Model

제품 내부 user id는 `int`를 사용한다. 원본 Mediness user uuid는 추적용으로 별도 보존한다.

| Field | Type | Required | Source | 설명 |
|---|---|---|---|---|
| `id` | int | yes | product | 제품 내부 PK |
| `source_user_id` | uuid | yes | `users.id` | 원본 Mediness user id |
| `email` | text | yes | `users.email` | 사용자 계정 식별자 |
| `name` | text | yes | `users.name` | 표시명 |
| `role` | text | yes | `users.role` | RBAC role |
| `position` | text | yes | `users.position` | 직급/책임 수준 |
| `department` | text | no | `users.department` | 소속 부서 seed 원문 값 |
| `department_node_id` | int | no | product | 조직도 department 노드 id (SPEC-002). 권한 판정 기준 |
| `team_node_id` | int | no | product | 조직도 team 노드 id (SPEC-002) |
| `active` | boolean | yes | `users.active` | 활성 계정 여부 |
| `employment_type` | text | no | `users.employment_type` | 고용 형태 |
| `resigned_at` | timestamptz | no | `users.resigned_at` | 퇴사 시각. Visibility Contract 판정 입력 |
| `seeded_at` | timestamptz | yes | product | seed 반영 시각 |
| `updated_at` | timestamptz | yes | product | 제품 내부 갱신 시각 |

`source_user_id`는 unique해야 한다. 같은 원본 user를 여러 번 seed해도 같은 product user row를 갱신해야 한다.

DEC-012에 따라 사용자 소속의 기준은 조직도 DB다. seed의 `department` 텍스트 값(`be`, `hr` 등)은 참고용 원본이고, 권한 판정에는 조직도 노드 매핑(`department_node_id`, `team_node_id`)을 사용한다. 매핑은 seed 시 이름 규칙으로 시도하고, 실패분은 admin이 보정한다. `department_node_id`가 없는 사용자는 `department is null`과 동일하게 문서 탐색이 제한된다.

### Seed Values

2026-07-08 확인된 seed 값 분포:

| Axis | Values |
|---|---|
| `role` | `admin`, `dev`, `hr`, `member`, `plan`, `qa` |
| `position` | `ceo`, `cmo`, `coo`, `cto`, `leader`, `staff` |
| `department` | `ax`, `be`, `design`, `fe`, `hr`, `plan`, `qa`, `rnd`, null |

v1 spec에서는 위 값을 seed enum 후보로 사용한다. 최종 enum table 분리는 구현/DB spec에서 결정한다.

### Login Boundary

| 구분 | 결정 |
|---|---|
| Google social login | v1에서 사용하지 않음 |
| 사용자 원장 | product user table, seed source는 `mediness.public.users` |
| 인증 방식 | email + password (데모 비밀번호 seed 공통 부여) + JWT access/refresh — WORK-001에서 확정 |
| Drive OAuth | 로그인과 분리된 connector OAuth |
| Drive connector config | env로 설정 |

Drive 연동용 OAuth client/refresh token/scope는 user login/RBAC와 결합하지 않는다.

### RBAC Rules

읽기 권한 판정은 DEC-006/DEC-016을 따른다.

`admin` role은 모든 문서를 읽을 수 있다(DEC-006 규칙 1). 이 규칙은 민감 문서(`sensitivity=sensitive`, `access_logic=PRESET` 포함)에도 동일하게 적용된다.

| 문서 policy | 사용자 field | Match |
|---|---|---|
| `read_roles` | `user.role` | role match |
| `read_departments` | `user.department_node_id` / `user.team_node_id` | 조직도 노드 id match |
| `read_positions` | `user.position` | position match |

`read_departments`는 부서명 텍스트가 아니라 조직도 노드 id 목록으로 저장한다(DEC-012). policy의 노드가 department면 해당 부서 소속(하위 팀 포함) 사용자가 매치되고, team 노드면 해당 팀 소속 사용자가 매치된다.

일반 문서 기본 `access_logic`은 `ANY`다. 즉 role, department, position 중 하나라도 read policy를 만족하면 읽을 수 있다.

`ALL`은 문서 policy에 값이 있는 축(role/department/position)을 모두 만족해야 읽을 수 있다. 값이 비어 있는 축은 판정에서 제외한다.

`PRESET`은 자체 판정 연산이 아니라 policy 출처 표시다. `policy_preset`이 가리키는 preset은 read policy 필드로 풀어 저장되고(DEC-018), 판정은 풀어 저장된 필드를 preset이 정의한 logic(`ANY` 또는 `ALL`)으로 평가한다. v1 preset의 기본 logic은 `ANY`다.

민감 문서는 `PRESET` 또는 `ALL`을 사용할 수 있다. preset 후보는 AI가 추천하고 관리자가 승인한다.

### Visibility Contract

| 조건 | 결과 |
|---|---|
| `active = false` | 문서 탐색 불가 |
| `resigned_at is not null` | 문서 탐색 불가 |
| `department is null` 또는 `department_node_id is null` | 일반 문서 탐색 제한. 관리자 보정 필요 |
| user가 read policy 만족 | 문서 노출 |
| user가 read policy 불만족 | 목록/트리/검색/관련 문서에서 숨김 |
| `role = admin` | 모든 문서 읽기 가능(민감 문서 포함). 승인 게이트와 관리 화면 접근 가능 |

권한 없는 문서는 잠금 표시하지 않는다.

### Boolean Vector

Boolean vector는 metadata 원장이 아니다. 요청 시점의 권한 판정 결과/log로만 사용한다.

| Field | 의미 |
|---|---|
| `role_match` | user role이 문서 read policy와 일치 |
| `department_match` | user department가 문서 read policy와 일치 |
| `position_match` | user position이 문서 read policy와 일치 |
| `final_readable` | 최종 읽기 가능 여부 |

### Admin Behavior

`admin` role 사용자는 다음 작업을 수행할 수 있다.

| 기능 | 허용 |
|---|---|
| 승인 게이트 접근 | yes |
| AI metadata 후보 승인/수정/거절 | yes |
| 문서종류 추가 | yes |
| 민감 preset 승인/수정 | yes |
| user RBAC 보정 | v1 admin tool 범위에서 허용 |

## 5. Implementation Rules

- 사용자 원장 seed source는 `mediness.public.users`이며, Google social login은 v1에서 사용하지 않는다.
- product user table은 int PK를 사용하고 원본 Mediness user uuid를 `source_user_id`로 보존한다.
- seed 재실행은 `source_user_id` 기준으로 멱등 upsert되어야 한다.
- 조직도 노드 매핑은 seed 시 이름 규칙으로 시도하고, 실패분은 admin이 보정한다.
- 권한 판정 소속 기준은 seed `department` 텍스트가 아니라 조직도 노드 매핑(`department_node_id`, `team_node_id`)이다 (DEC-012).
- Drive OAuth 설정(client/refresh token/scope)은 user login/RBAC와 결합하지 않고 env로 관리한다.
- 권한 없는 문서는 잠금 표시하지 않고 목록/트리/검색/관련 문서에서 숨긴다.
- boolean vector는 metadata 원장에 저장하지 않으며 요청 시점 판정 결과/log로만 사용한다.
- 최종 enum table 분리는 구현/DB spec에서 결정한다.

## 6. Verification

### Acceptance Criteria

- [ ] 기존 `mediness.public.users` 26 rows를 seed source로 식별할 수 있다.
- [ ] product user table은 int PK를 사용하고 원본 uuid를 `source_user_id`로 보존한다.
- [ ] seed 재실행은 `source_user_id` 기준으로 멱등 upsert된다.
- [ ] Drive OAuth 설정은 user login 설정과 분리되어 env로 관리된다.
- [ ] `active=false`, `resigned_at is not null`, `department is null` 사용자는 문서 탐색이 제한된다.
- [ ] 권한 없는 문서는 목록/트리/검색/관련 문서에 노출되지 않는다.
- [ ] `admin` role만 승인 게이트에 접근할 수 있다.
- [ ] `admin` role은 민감 문서를 포함한 모든 문서를 읽을 수 있다.
- [ ] `read_departments`는 조직도 노드 id로 저장되고 사용자 `department_node_id`/`team_node_id`와 매칭된다.
- [ ] `access_logic=PRESET` 문서는 preset이 풀어 저장한 read policy 필드로 판정된다.

## 7. Open Questions

없음.
