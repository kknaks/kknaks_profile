---
type: research
title: mediness prod 4명 조직 정보로 시드 채우기 가능성 조사
status: draft
created_at: 2026-09-30
slug: strong-hajin-deploy
sources:
  - mediness prod DB (namespace mediness-prod, alembic 0139_deployment_surface_key) — READ-ONLY 조회
  - mediness-app origin/main 67b6a7dc back/app/models/{organization,user}.py
  - reference/2026-09-30-strong-hain-seed/README.md
  - orchestration/work/strong-hajin-deploy/research-seed-path.md
---

# mediness prod 4명 조직 정보로 시드 채우기 가능성 조사

조회는 모두 `SELECT` 였다. asyncpg `transaction(readonly=True)` 안에서 돌렸고, 매 실행마다
`show transaction_read_only = on` 을 확인했다. 쓰기·DDL·재시작은 하지 않았다. DB 접속 정보는 파드 env
`DATABASE_URL` 을 파드 안에서만 읽었고, 출력하거나 기록하지 않았다. 양식 CSV 는 채우지 않았다.

---

## 1. 결론 — **부분적으로 채울 수 있다**

네 명은 모두 **동명이인 없이 1건씩** 찾았다. 아래 값은 mediness 에서 그대로 온다.

- 이름·로그인 메일·재직 상태·고용형태·입사일
- 주소속 조직과 그 상위 트리
- 직위(`org_role`: CTO·리더)

아래 값은 **mediness 에 원천이 없거나 변환 규칙이 필요**하다. 사람이 정해야 한다.

| 없거나 변환이 필요한 것 | 상태 |
|---|---|
| `members.key` | 사번이 네 명 모두 비어 있다 |
| `members.role_key` | mediness 권한 체계가 다르다(`system_admin`·`dev`) |
| `grades` | 직급 전용 표가 없다. `users.position` 은 이름만 「직급」이고 값은 직위(`cto`·`leader`)다 |
| `organization_units.unit_type` | mediness 의 `department` 에 대응하는 종류가 시드에 없다 |
| 회사 루트 | mediness `org_unit` 에는 루트가 없고 `organization` 표에 따로 있다 |
| `jobs`·`job_assignments` | mediness 에 직무 행이 0건이다 |
| `phone`·`birth_date` | 네 명 모두 값이 없다 |

---

## 2. 네 사람 — 찾았나, 로그인 메일

| 이름 | `users` 매치 | `organization_member` 매치 | 로그인 메일(`users.email` = `organization_member.work_email`) | 상태 |
|---|---|---|---|---|
| 구성원A | 1건 | 1건 | <A 회사메일> | active |
| 구성원C | 1건 | 1건 | <C 회사메일> | active |
| 구성원B | 1건 | 1건 | <B 회사메일> | active |
| 구성원D | 1건 | 1건 | <D 회사메일> | active |

- 부분일치(`ilike '%이름%'`)로 세도 각 1건이다. **동명이인은 없다**
- 네 명 모두 소속 조직은 `organization.slug = medisolve`(이름 `MedisolveAI`) 하나다
- 두 표의 메일은 네 명 모두 같다
- `employee_no`·`external_hr_id` 는 네 명 모두 **null** 이다

---

## 3. 시드 표·열 ↔ mediness 테이블.열

「네 명 값」 열은 네 사람에게 실제로 값이 있는지를 적은 것이다.

### `organization_units`

| 시드 열 | mediness | 네 명 값 | 비고 |
|---|---|---|---|
| `key` | `org_unit.slug` | 있음 | `plan`·`ax`·`rnd`·`development`·`operations` |
| `name` | `org_unit.name` | 있음 | |
| `unit_type` | `org_unit.unit_type` | 있음 | **변환 필요**(§5 G3). mediness 는 `division`·`department` 이고 시드는 `company·division·office·team·part` 다 |
| `parent_key` | `org_unit.parent_id` → 부모의 `slug` | 있음 | 최상위 둘은 `parent_id` 가 null 이다. 회사 루트는 `organization` 표에 있다(§5 G4) |
| `display_order` | `org_unit.sort_order` | 있음 | |
| (회사 루트 행) | `organization.slug`·`organization.name` | 있음 | `medisolve` / `MedisolveAI` |

### `grades`

| 시드 열 | mediness | 판정 |
|---|---|---|
| `key`·`name`·`display_order` | **없음**(전용 표 없음) | 후보는 `users.position` 이다. 모델 주석은 「직급 라벨 8값」이라 하지만 허용값이 `ceo·coo·cmo·cto·po·manager·leader·staff`(`back/app/schemas/admin.py:17`)라 **직위에 가깝다**. 네 명 값은 `cto`(구성원C)와 `leader`(나머지 셋)다(§5 G5) |

### `positions`

| 시드 열 | mediness | 판정 |
|---|---|---|
| `key` | `org_role.slug` | 있음. 네 명이 쓰는 것은 `cto`·`leader` |
| `name` | `org_role.name` | 있음. `CTO`·`리더` |
| `unit_type` | **없음** | `org_role` 은 조직 종류에 묶이지 않는다. 변환이 필요하다(§5 G6) |
| `slot` | **없음** | `head` 로 볼지는 규칙이 필요하다 |
| `role_key` | **없음** | 변환이 필요하다(§5 G2) |

### `jobs` · `job_assignments`

| 시드 | mediness | 판정 |
|---|---|---|
| `jobs.key`·`name` | `job_function.slug`·`name` | **표는 있지만 prod 전체가 0행이다** |
| `job_assignments.*` | `org_member_job_function` | 네 명 **0건**이다. 채울 원천이 없다 |

### `members`

| 시드 열 | mediness | 네 명 값 | 비고 |
|---|---|---|---|
| `key` | `organization_member.employee_no` | **없음(4/4 null)** | 규칙이 필요하다(§5 G1) |
| `display_name` | `organization_member.display_name`(= `users.name`) | 있음 | |
| `employment_state` | `organization_member.status` (`active`/`inactive`) | 있음(4/4 `active`) | `active` 는 `active`, `inactive` 는 `ended` 로 옮긴다 |
| `employment_type` | `organization_employment_period.employment_type`(= `users.employment_type`) | 있음(4/4 `fulltime`) | **변환 필요**: `fulltime` 은 `regular`, `parttime` 은 `part_time`, `contract` 는 `contract` |
| `primary_unit_key` | `org_membership`(`is_primary`, `valid_to IS NULL`) → `org_unit.slug` | 있음 | |
| `role_key` | **없음**(체계 다름) | — | 후보 원천은 `org_member_access_role` → `access_role.key`, 또는 `users.role`(§5 G2) |
| `grade_key` | 없음 | — | `grades` 참조 |
| `employed_from` | `organization_employment_period.started_on`(= `users.hire_date`) | 있음 | |
| `employed_until` | `organization_employment_period.ended_on` / `users.resigned_at` | 4/4 null | 재직 중이므로 비우면 된다 |
| `phone` | `users.phone` | **없음(4/4)** | |
| `birth_date` | `users.birth_date` | **없음(4/4)** | |

### `appointments`

| 시드 열 | mediness | 판정 |
|---|---|---|
| `member_key` | `org_member_role.organization_member_id` | 있음 |
| `unit_key` | `org_member_role.org_membership_id` → `org_membership.org_unit_id` → `slug` | 있음. 단 membership 에 묶이지 않은 역할(`cto`)은 **조직이 없다**(§5 G6) |
| `position_key` | `org_member_role.org_role_id` → `org_role.slug` | 있음 |
| `kind` | 없음 | 기본값 `primary` 로 둘 수 있다 |
| `valid_from`·`valid_until` | `org_member_role.valid_from`·`valid_to` | 있음 |

### `memberships`

| 시드 열 | mediness | 판정 |
|---|---|---|
| `member_key`·`unit_key` | `org_membership.organization_member_id`·`org_unit_id` | 있음 |
| `kind` | `org_membership.is_primary` | 있음. 추가 소속은 네 명 모두 **없다**. 주소속은 `primary_unit_key` 가 대신 만드므로 이 표는 비워도 된다 |
| `valid_from`·`valid_until` | `org_membership.valid_from`·`valid_to` | 있음 |

### `logins`

| 시드 열 | mediness | 판정 |
|---|---|---|
| `member_key` | (members.key 와 같은 규칙) | G1 을 따른다 |
| `email` | `users.email` | 있음(4/4). 비밀번호 해시(`users.password_hash`)는 **옮기지 않는다**. 알고리즘도 다르고, 시드는 비밀번호를 받지 않는다 |

---

## 4. 네 사람의 조직 트리와 직급·직위·직무

전화·생년월일은 네 명 모두 **없음**이다.

```text
MedisolveAI  (organization.slug=medisolve — org_unit 밖의 회사)
├─ 운영  operations  [division, sort 10]
│   └─ 기획  plan  [department, sort 20]        ← 구성원A(주소속)
└─ 개발  development  [division, sort 30]       ← 구성원C(주소속)
    ├─ 연구(R&D)  rnd  [department, sort 10]   ← 구성원B(주소속)
    └─ AX  ax  [department, sort 40]           ← 구성원D(주소속)
```

prod `org_unit` 은 전체 12개다. 위 5개는 네 명의 소속과 그 상위뿐이다.

| 이름 | 주소속 | 직위(`org_role`, 현재 유효) | `users.position` | 직무 | mediness 권한(`access_role`, 현재) | `users.role` | 고용형태 | 입사일 |
|---|---|---|---|---|---|---|---|---|
| 구성원A | 기획 `plan` | 리더 `leader` @ plan | leader | 없음 | system_admin | admin | fulltime | 2026-03-24 |
| 구성원C | 개발 `development` | CTO `cto`(조직 무관) + 리더 `leader` @ development | cto | 없음 | dev | dev | fulltime | 2026-04-14 |
| 구성원B | 연구(R&D) `rnd` | 리더 `leader` @ rnd | leader | 없음 | system_admin | admin | fulltime | 2026-04-14 |
| 구성원D | AX `ax` | **현재 없음**(아래 주) | leader | 없음 | system_admin | admin | fulltime | 2025-02-02 |

**주 — 구성원D의 직위:** `leader @ ax` 행이 `2026-08-06 05:19:08` 에 끝났다(`valid_to`). 같은 시각
주소속이 `ax → plan` 으로 옮겨졌고 52초 뒤 다시 `ax` 로 돌아왔다(`org_membership` 3행). 그런데 리더 역할은
다시 만들어지지 않았다. membership 에 묶인 역할이 옛 membership 과 함께 닫힌 것으로 보인다. **mediness 원장
기준으로 구성원D은 지금 직위가 없다.** `users.position` 은 여전히 `leader` 다. 어느 쪽을 믿을지는 OQ-7 이다.

**참고 — `users.department`:** 레거시 텍스트 열이다. 구성원A `plan`, 구성원B `rnd`, 구성원D `ax`, 구성원C null 이다.
`org_membership` 과 일치하므로 원천으로는 `org_membership` 을 쓰면 된다.

---

## 5. 갭과 Open Questions

| # | 갭 | 필요한 변환 규칙 / 결정 |
|---|---|---|
| G1 / OQ-1 | `members.key` 원천 없음(`employee_no` 4/4 null) | 임시 사번(`1001~`, 선례), 메일 로컬파트(`<A>`·`<C>`·`<B>`·`kknaks`), mediness `organization_member.id`(uuid) 중 무엇으로 할까 |
| G2 / OQ-2 | `role_key` 체계가 다르다. mediness 의 `access_role` 은 `system_admin`·`hr_admin`·`dev`·`plan`·`qa`·`member` 이고 `users.role` 은 `admin`·`dev`·`member` 다. 시드는 `executive`·`people-manager`·`team-lead`·`member` 등이다 | 대응표가 필요하다. 예: `system_admin` 을 `executive` 로 할지 `people-manager` 로 할지, `dev` 를 `member` 로 할지 `team-lead` 로 할지. 또는 mediness 직위 `leader` 를 `positions.role_key=team-lead` 로 줄지. **최소 1명은 `executive`/`people-manager` 여야 한다** |
| G3 / OQ-3 | `unit_type`. mediness 의 `department` 가 시드에 없다 | `division` 은 `division`(본부)으로 옮긴다. `department` 를 `team` 으로 할지 `office`(실)로 할지 정해야 한다 |
| G4 / OQ-4 | 회사 루트가 `org_unit` 밖(`organization`)에 있다 | `medisolve`/`MedisolveAI` 를 `company` 행으로 만들어 두 division 의 부모로 둘까. 루트 없이 division 둘을 최상위로 두면 `executive` 의 조직 전체 범위가 한쪽 트리에만 닿는다(`dataset_import.py:406-416` `_root_of`) |
| G5 / OQ-5 | `grades` 원천 없음 | `users.position` 을 직급으로 쓸지(값이 직위와 겹친다), 아니면 직급 표를 비울지 |
| G6 / OQ-6 | `positions.unit_type`·`slot` 원천 없음. `cto` 는 조직에 묶이지 않는다 | `leader` 는 (`team` 또는 G3 결과, `head`)로 한다. `cto` 는 `company` 에 붙일지(appointment 의 `unit_key` 를 회사 루트로), 직위에서 뺄지. 같은 slug `leader` 가 division(구성원C)과 department(나머지)에 모두 쓰인다. 시드 `positions` 는 `unit_type` 하나에 묶이므로 **key 를 둘로 나눠야 한다**(예: division 장 / department 장) |
| G7 / OQ-7 | 구성원D의 현재 직위가 원장에 없다(§4 주) | 원장대로 직위 없이 넣을지, `users.position=leader` 를 근거로 `leader @ ax` 로 넣을지 |
| G8 | `employment_type` 값 이름이 다르다 | `fulltime` 은 `regular`, `parttime` 은 `part_time`, `contract` 는 `contract`. 기계적이라 OQ 가 아니다 |
| G9 | 직무·전화·생년월일 원천 없음 | 비워 둔다. 채우려면 사용자가 직접 줘야 한다 |
| OQ-8 | 트리 범위 | 네 명이 쓰는 5개 단위만 넣을지, prod `org_unit` 12개 전체를 넣을지(나머지 7개는 이번에 조회 결과에 싣지 않았다) |
| OQ-9 | 이력 | `valid_from`(mediness 소속·직위 시작 시각)을 옮길지 비울지. 비우면 적재 시각이 된다 |

---

## 6. 실행한 쿼리

값 없이 문장만 적는다. 이름·id 배열은 파라미터 `$1` 로 넘겼다. 세 번 실행했고, 매번
`BEGIN READ ONLY` 트랜잭션 → `show transaction_read_only` → 아래 쿼리 순서였다.

```sql
-- 실행 1: 스키마
select version_num from alembic_version;
select table_name from information_schema.tables where table_schema='public' and (table_name in (…12개…) or table_name ilike '%grade%' or table_name ilike '%position%' or table_name ilike '%rank%');
select table_name, column_name, data_type from information_schema.columns where table_schema='public' and table_name in (…11개…);

-- 실행 2: 네 사람 찾기
select version_num from alembic_version;
select id, name, email, active, role, position, department, hire_date, resigned_at, employment_type::text, (phone is not null), (birth_date is not null), (slack_id is not null), (last_login is not null) from users where name = any($1);
select name, count(*) from users where name ilike any(array[…4개 패턴…]) group by name;
select m.id, m.display_name, m.user_id, m.work_email, m.employee_no, m.external_hr_id, m.status, m.valid_from, m.valid_to, o.slug, o.name from organization_member m join organization o on o.id=m.organization_id where m.display_name = any($1) or m.user_id in (select id from users where name = any($1));

-- 실행 3: 조직 정보 (member id 4개 = $1)
select … from org_membership ms join organization_member m … join org_unit u … where ms.organization_member_id = any($1);
with recursive t as (select u.* from org_unit u where u.id in (select org_unit_id from org_membership where organization_member_id = any($1)) union select p.* from org_unit p join t on p.id=t.parent_id) select id, parent_id, slug, name, unit_type, sort_order, active, valid_from, valid_to from t;
select … from org_member_role mr join organization_member m … join org_role r … left join org_membership ms … left join org_unit u … where mr.organization_member_id = any($1);
select … from org_member_job_function mj join organization_member m … join job_function j … where mj.organization_member_id = any($1);
select … from org_member_access_role ma join organization_member m … join access_role a … where ma.organization_member_id = any($1);
select m.display_name, e.employment_type::text, e.started_on, e.ended_on, e.cancelled_at from organization_employment_period e join organization_member m … where e.organization_member_id = any($1);
select count(*) from org_role, (select count(*) from job_function), (select count(*) from access_role), (select count(*) from org_unit);
select key, name from access_role;
```

- 마지막 두 쿼리는 네 명 외의 **사람 행을 읽지 않는다.** 개수와 권한 어휘(6종: dev·hr_admin·member·plan·qa·system_admin)만 읽었다
- `org_role` 어휘는 개수(6)만 읽었고, 이름은 네 명이 쓰는 두 개만 적었다
- 파드 접근 경로는 `ssh medi-me` → `/opt/homebrew/bin/kubectl -n mediness-prod exec -i deploy/back -c back -- /app/.venv/bin/python -` (stdin 스크립트)이다
