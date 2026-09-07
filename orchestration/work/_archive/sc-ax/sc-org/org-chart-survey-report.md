# mediness 조직도(organization) 도메인 조사 리포트 — sc-ax 재사용성 판단 재료

- 작성: 2026-09-04 / `reviewer_code` (read-only 조사, 판정 없음)
- 조사 대상 워크트리
  - 앱: `/Users/kknaks/orca/workspaces/mediness-app/task` (브랜치 `kknaksss/task`)
  - 스펙: `/Users/kknaks/orca/workspaces/mediness-mediness/task-spec` (read-only)
- **아무 파일도 수정·생성하지 않았다.** 산출물은 이 리포트 1개뿐. 테스트 미실행, DB 미접속 — 판단 근거는 전부 소스 파일이다.
- 표기 규칙: **[사실]** = 인용한 `파일:줄` 에서 직접 확인. **[추정]** = 코드/문서에서 유도한 해석이며 확정 아님.
- 개인 식별 정보는 인용하지 않았다 (`back/app/seeds/medi_users.py` 에 실명·이메일 스냅샷이 있으나 구조만 서술).

---

## 0. 세 줄 요약

1. mediness 조직도는 **16개 테이블 + 26개 PostgreSQL 트리거 함수**로 된 tenant-scoped·**기간형(temporal)** 디렉터리다. 단순 부서 트리가 아니라 「누가·언제·어느 조직에·무슨 역할로 있었나」의 이력 원장이다. **[사실]** (§2)
2. 코드 표면은 라우터 2개(673줄)·서비스 5개(약 5,700줄)·스키마 740줄·프론트 약 7,000줄이고, **조직도 자체의 순수 코어와 mediness 전용 legacy 브리지가 한 파일 안에 섞여 있다.** **[사실]** (§3)
3. 떼어갈 때 같이 딸려오는 것: `users`(전역 계정)·capability RBAC 2테이블·legacy `users.role/department/position` 투영 트리거·Medisolve 제품책임 어댑터. **조직도 코어(9테이블)는 이 중 `users` 와 `organization` 만 있으면 선다.** **[추정]** (§4·§5)

---

## 1. 문서 조사 — 조직도 도메인은 문서에서 무엇으로 정의돼 있나

### 1.1 문서 전수 (스펙 워크트리에서 `org_unit|organization_member|org-directory|조직도` grep)

| 문서 | 역할 | 조직도 관련성 |
|---|---|---|
| `20-spec/spec-002-rbac-org.md` (591줄) | **조직도 도메인 계약의 SoT** | 원장. tenant·member lifecycle·access role·org unit/소속/직책/조직역할 외부계약 전부 |
| `40-architecture/organization-directory.md` (329줄) | 아키텍처 경계 문서 | provider port·temporal model·offboarding·legacy projection 전환 |
| `20-spec/spec-003-capability-rbac.md` | capability 체계 | 역할→권한 매핑의 정본(DB) — 조직도가 소비 |
| `20-spec/spec-001-auth.md` | 전역 identity | `users` 와 `X-Organization-Id` selector |
| `30-work/work-055-rbac-org.md` (214줄, done) | **1세대 조직도** | `users.department`+`position` 파생 렌더. 테이블 없음 |
| `30-work/work-082-…foundation.md` (done) | tenant·member·access grant 기반 | PR #41·#46·#58·#95 |
| `30-work/work-083-…directory-management.md` (done) | org unit 트리·소속·직책·역할·관리 UI/API·audit | PR #41·#42·#46·#95 |
| `30-work/work-084-participant-product-adapter.md` (done) | provider port·원자 offboarding·제품책임 합성 | PR #95 |
| `30-work/work-085-capability-rbac-cutover.md` | capability DB 정본 전환 | |
| 소비 SPEC | `spec-129`(부서 스페이스)·`spec-125`(WBS)·`spec-052`(제품 파이프라인)·`spec-031`(회의 v2)·`spec-151`(예약)·`spec-060`(MCP)·`spec-128/130/132` | 전부 조직도를 **소비**한다 |
| `21-html/RBAC Sidebar Gate + Org Chart (User Mgmt).html` | 1세대 조직도 시안 | WP-055 산출물 |

**[사실]** 브리프가 준 두 문서(spec-002 · work-055)가 전부가 아니었다. 특히 **work-055 는 지금 코드의 조직도가 아니다** — §1.3 참조.

### 1.2 조직도 도메인의 의도 (spec-002 §0·§1 · organization-directory.md)

**[사실]** spec-002:42-51 이 세운 어휘 경계가 이 도메인의 핵심 설계다. 축이 넷으로 분리돼 있고 서로 파생하지 않는다.

| 축 | canonical term | 의미 |
|---|---|---|
| tenant | `organization` | 모든 조직·제품·데이터 정책의 root 경계 |
| 사람(전역) | `users` | 조직 밖에서도 유지되는 로그인 identity |
| 사람(조직 내) | `organization_member` | 특정 organization 안의 **안정적 directory identity**. 계정 연결은 선택 |
| 구조 | `org_unit` | 회사/본부/팀 node (parent 자기참조 트리) |
| 소속 | `org_membership` | member ↔ org_unit 의 **기간** 관계 |
| 직능 | `job_position` (문서) / **`job_function` (코드)** | 직책·직능 어휘 |
| 조직역할 | `org_role` | 특정 unit 안의 head/leader 같은 기능 역할. tenant 자유 어휘, **`leader` 는 예약 slug** |
| 시스템권한 | `access_role` | `system_admin`·`hr_admin`·`qa`·`dev`·`plan`·`member` |

**[사실]** 불변 원칙 (spec-002:53-58):
- **조직 사실과 시스템 권한은 독립이다.** 「리더면 자동으로 X 권한」이라는 파생을 계약이 금지한다 (spec-002:322).
- `organization_member` 는 계정이나 한 번의 재직 기간과 **수명을 같이하지 않는다.** 계정 해제·전역 user 삭제·재입사 뒤에도 같은 member 와 이력을 유지한다 (spec-002:58).
- 제품 `department` 축의 **정본은 `org_unit`** 이다 (2026-08-07 개정, spec-002:23-26·57 — 구 «일반화하지 않는다» 를 폐기).

**[사실]** 정책 (spec-002:478-499 · organization-directory.md:129-151):
- 모든 시간 관계의 현재/as-of 판정 = `valid_from <= as_of AND (valid_to IS NULL OR as_of < valid_to)` — **half-open**.
- 고용 기간만 날짜형 `[started_on, ended_on)`.
- 관계 변경은 **기존 row 종료 + 새 row 생성**. 재활성화로 이력을 덮어쓰지 않는다.
- 조직 사실 변경 이력은 `org_directory_event` 에 **append-only** 로 남기고, 수정·삭제 API 를 제공하지 않는다 (spec-002:129, `AUDIT_IMMUTABLE` 405).
- HR PII(사번·외부 HR ID·user_id·계정 연결 여부)는 일반 directory read 에 포함하지 않는다 (spec-002:229).
- 퇴사(offboarding)는 부분 명령이 아니라 **한 트랜잭션**에서 고용기간·소속·직책·조직역할·access grant·제품/버전 책임을 전부 닫는 coordinator 다 (spec-002:181, organization-directory.md:291).
- 마지막 `system_admin` 제거를 막는 **last-admin guard** 는 authorization 위가 아니라 DB/도메인 계층 불변식이다 (spec-002:557-568).

### 1.3 ⚠ 두 세대의 조직도가 문서에 공존한다 — 브리프가 준 work-055 는 구세대다

**[사실]** `work-055-rbac-org.md:72` 는 조직도를 «**저장 구조 아님** — `(department, position)` 파생 렌더. 신규 테이블/컬럼 없음» 이라고 명시한다. 이건 2026-07-01 시점 1세대(`users.department` 8값 + `users.position` 8값 → FE `OrgChart.tsx` 렌더)다.

**[사실]** 현재 코드의 조직도는 WP-082/083/084 가 만든 **2세대 canonical Organization Directory** 다 — `org_unit` 트리 + `organization_member` + 기간형 관계 테이블. `30-work.md:35` 는 WP-055 를 `done` 으로, `:64-65` 는 WP-082/083 을 `done` 으로 각각 기록한다.

**[추정]** sc-ax 재사용 판단에서 참조해야 할 것은 **2세대**다. work-055 의 「테이블 없이 파생 렌더」 모델은 현재 mediness 에서도 legacy projection 으로만 남아 있다(§4.3).

### 1.4 문서↔코드 어긋남 3건 (조사 중 발견 — 사실 기록, 판정 아님)

| # | 문서 | 코드 | 근거 |
|---|---|---|---|
| ① | spec-002:572 «신규 durable 개념: … `job_position`, `org_member_job_position` … `org_membership_role`» | **없다.** `job_position`·`org_member_job_position` 은 `0064` 가 만들고 **`0065` 가 drop** 했고, `org_membership_role` 은 `0065` 가 `org_member_role` 로 rename 했다 | `alembic/versions/0065_organization_job_function.py:1155-1156`(drop) · `:797`(rename) · `app/models/organization.py` 에 `job_position` 없음 |
| ② | spec-002:215 `OrganizationUnit` 응답에 `aliases[]`, :572 에 `org_unit_alias` 테이블, :292 create/patch 에 `aliases?` | **alias 개념이 코드에 전혀 없다.** 스키마·모델·마이그레이션 전부 0 hit | `app/schemas/organization_directory.py:332-379`(OrgUnitView/Create/Patch 에 alias 없음) · `grep -rn "alias" app/schemas/organization_directory.py` → 0 |
| ③ | spec-002:294-297 unit move/archive 는 `preview_token` 을 묶어 commit 시 stale 이면 `IMPACT_PREVIEW_STALE` | **token 없다.** preview 와 commit 이 별도 endpoint 이고 토큰을 주고받지 않는다 | `app/routers/organization_directory.py:231-267` · `app/schemas/organization_directory.py:403-409`(`OrgUnitImpactView` 에 token 필드 없음) |

**[사실]** spec-002 자신이 이 어긋남의 해소 규칙을 갖고 있다 — «table schema, index, partial unique, migration 전문은 **코드가 SoT**» (spec-002:574). ③번 `IMPACT_PREVIEW_STALE` 도 «실제 cancellation/audit column 은 code 와 migration 이 SoT» 계열이다.
**[추정]** 즉 문서를 그대로 sc-ax 요구사항으로 옮기면 **실존하지 않는 3개 기능(alias·preview token·job_position 별도 축)을 구현 범위에 넣게 된다.** 판단 시 반드시 코드 기준으로 봐야 한다.

---

## 2. 테이블 구조 — 조직도 관련 테이블 전수

### 2.1 인벤토리와 마이그레이션 이력

**[사실]** `back/alembic/versions/` 를 `create_table` × 조직 도메인 테이블명으로 전수한 결과(§6 self-check (a) 참조), **현재 head 에 살아 있는 조직 도메인 테이블은 16개**다.

| # | 테이블 | 생성 | 이후 변경 | 왜 그렇게 바뀌었나 (한 줄) |
|---|---|---|---|---|
| 1 | `organization` | `0059:74` | — | tenant root. Medisolve 고정 UUID `00000000-…-0001` 시드 (`0059:85`) |
| 2 | `organization_member` | `0059:93` | `0061:24-38` 에 `display_name/work_email/employee_no/external_hr_id` 추가 + `user_id` **NOT NULL→nullable** | 계정 없는 입사예정자·계약자를 먼저 등록할 수 있게 — 사람의 SoT 를 계정에서 떼어냈다 |
| 3 | `access_role` | `0059:116` | — | 6값 시드 `system_admin/hr_admin/qa/dev/plan/member` (`0059:29,127`) |
| 4 | `org_member_access_role` | `0059:130` | — | 기간형 역할 배정 + grant/revoke actor·reason 보존 |
| 5 | `organization_employment_period` | `0061:147` | `0096:28-66` 에 `cancelled_at/cancelled_by_member_id/cancellation_reason` 추가 + overlap exclusion 을 `cancelled_at IS NULL` partial 로 재생성 | 잘못 등록한 재직 기간을 **삭제 대신 논리 취소**(감사 가능)로 바꿔야 했다 |
| 6 | `org_unit` | `0061:210` | `0065:139-182` 가 Medisolve 3본부(operations/marketing/development) 를 삽입하고 기존 9부서를 그 밑으로 재부모화 | 부서 평면 → 2단 트리로 승격 |
| 7 | `org_membership` | `0061:273` | `0065:601-610` 에 `change_set_id` 추가 | 일괄 발령(change set) 단위로 소속 이동을 묶기 위해 |
| 8 | `org_directory_event` | `0061:357` | `0065:587-600` 에 `change_set_id` 추가 | 같은 이유 + append-only 트리거(`0061` guard) |
| 9 | `org_role` | `0064:86` | `0065:535` 에 `description` 추가 | 조직 역할 자유 어휘. `0065:1063-1071` 이 예약 slug `leader` 를 시드 |
| 10 | `job_function` | `0065:671` | — | **`job_position`(0064:56) 을 대체.** 직책(호칭)과 직능(무슨 일)을 갈라 직능 축만 남겼다 |
| 11 | `org_member_job_function` | `0065:700` | — | `org_member_job_position`(0064:116) 대체 |
| 12 | `org_member_role` | `0064:179` 에 `org_membership_role` 로 생성 → `0065:797` rename | `0065:805-833` 에 `organization_member_id`(NOT NULL) + `change_set_id` 추가, `org_membership_id` 를 **nullable 화** | CEO/CTO 같은 **조직 전역(organization-wide) 역할 배정**을 표현할 수 없었다 — `org_membership_id IS NULL` = 전역 |
| 13 | `organization_change_set` | `0065:538` | — | 일괄 변경 예약·취소 원장 |
| 14 | `organization_member_offboarding` | `0096:69` | `0099:22-32` 에 `corrected_at/corrected_by_member_id/correction_reason` 추가 | 처리된 퇴사를 삭제·재입사 대신 **보상형 정정**으로 되돌리기 위해 |
| 15 | `capability` | `0076:161` | — | 권한 leaf 카탈로그 (`{domain}.{resource}.{action}`) |
| 16 | `access_role_capability` | `0076:194` | — | 역할→leaf 구성. migration 으로만 변경 |

**[사실]** 사라진 테이블 3개: `job_position`·`org_member_job_position` (0065:1155-1156 drop), `org_membership_role` (0065:797 rename). downgrade 경로가 `0065:350-527` 에 복원 코드로 남아 있다.

**[사실]** ⚠ **파일명 번호와 revision 사슬이 다르다.** `0059_organization_tenant_access.py:12` 의 `revision` 은 `"0058_organization_tenant_access"` 다. `0096_organization_member_lifecycle.py:5-11` 이 그 이유를 기록한다 — PR #95 머지 때 `down_revision` 을 옮기지 않아 head 가 둘로 갈렸고, 파일명 재정렬(WP-105)로 번호를 맞췄다. **정본은 `down_revision` 이지 파일명이 아니다.**

### 2.2 테이블별 컬럼 (모델 SoT = `back/app/models/organization.py`)

공통: 모든 PK 는 `uuid_pk()` = `UUID` PK, `gen_random_uuid()` 서버 기본값. `TimestampMixin` 이 붙은 테이블은 `created_at`/`updated_at`(timestamptz, NOT NULL, `now()`).

#### (1) `organization` — `organization.py:32-41`
| 컬럼 | 타입 | 제약 |
|---|---|---|
| `id` | UUID | PK |
| `slug` | Text | NOT NULL, **UNIQUE** |
| `name` | Text | NOT NULL |
| `active` | Boolean | NOT NULL, default `true` |
| `created_by_user_id` / `updated_by_user_id` | UUID | nullable (FK 아님 — 컬럼만) |
| `audit_reason` | Text | nullable |
| + `created_at`/`updated_at` | timestamptz | |

soft delete: **`active` 플래그** (물리 삭제 없음).

#### (2) `organization_member` — `organization.py:44-70`
| 컬럼 | 타입 | 제약 |
|---|---|---|
| `id` | UUID | PK |
| `organization_id` | UUID | **FK → organization.id ON DELETE RESTRICT**, NOT NULL |
| `user_id` | UUID | **FK → users.id ON DELETE SET NULL**, nullable |
| `display_name` | Text | NOT NULL, `ck_org_member_display_name_not_blank` |
| `work_email` | Text | nullable |
| `employee_no` | Text | nullable (HR PII) |
| `external_hr_id` | Text | nullable (HR PII) |
| `status` | Text | NOT NULL, default `active`, **CHECK `IN ('active','inactive')`** |
| `valid_from` | timestamptz | NOT NULL, `now()` |
| `valid_to` | timestamptz | nullable |
| `created_by_user_id`/`updated_by_user_id` | UUID | nullable |
| `audit_reason` | Text | NOT NULL, default `'legacy users backfill'` |

- UNIQUE `(organization_id, user_id)` = `uq_org_member_organization_user` — 한 tenant 에서 1 global user ↔ 1 member.
- CHECK `valid_to IS NULL OR valid_to > valid_from`.
- INDEX: `ix_org_member_user(user_id)`, `ix_org_member_active(organization_id, status, valid_to)` (`0059:112-113`).
- soft delete: **`status='inactive'` + `valid_to` 마감** 2중. 물리 삭제 없음.
- **`ON DELETE SET NULL`** 이 핵심 설계다 — 전역 user 가 물리 삭제돼도 member·고용기간·소속·audit 는 살아남는다 (spec-002:246).

#### (3) `organization_employment_period` — `organization.py:73-116`
| 컬럼 | 타입 | 제약 |
|---|---|---|
| `id` | UUID | PK |
| `organization_member_id` | UUID | FK → organization_member.id RESTRICT, NOT NULL |
| `employment_type` | **PG enum `employment_type`** | nullable. 값 = `fulltime|contract|parttime` (`app/models/user.py:13-18`) |
| `started_on` | Date | NOT NULL |
| `ended_on` | Date | nullable |
| `created_by_member_id` | UUID | FK → organization_member.id, nullable |
| `audit_reason` | Text | NOT NULL |
| `cancelled_at` | timestamptz | nullable |
| `cancelled_by_member_id` | UUID | FK → organization_member.id, nullable |
| `cancellation_reason` | Text | nullable |

- **EXCLUDE (gist)** `ex_org_employment_no_overlap`: `organization_member_id =` + `daterange(started_on, ended_on, '[)') &&` **WHERE `cancelled_at IS NULL`** — 취소되지 않은 재직 기간끼리 겹칠 수 없다.
- CHECK `ended_on IS NULL OR ended_on > started_on`.
- CHECK `ck_org_employment_cancellation_complete` — 취소 3필드는 전부 NULL 이거나 전부 채워져야 한다(사유는 공백 불가).
- soft delete: **`cancelled_at` 논리 취소** (row 삭제 금지 — spec-002:190).

#### (4) `organization_member_offboarding` — `organization.py:119-173`
| 컬럼 | 타입 | 제약 |
|---|---|---|
| `id` | UUID | PK |
| `organization_id` | UUID | FK → organization.id RESTRICT, NOT NULL |
| `organization_member_id` | UUID | FK → organization_member.id RESTRICT, NOT NULL |
| `actor_member_id` | UUID | FK → organization_member.id RESTRICT, **NOT NULL** |
| `state` | Text | NOT NULL, **CHECK `IN ('scheduled','processed','cancelled','corrected')`** |
| `last_working_on` | Date | NOT NULL (유일한 외부 입력) |
| `effective_at` | timestamptz | NOT NULL (= 마지막 근무일 다음날 00:00 KST) |
| `scheduled_at` | timestamptz | NOT NULL, `now()` |
| `processed_at` | timestamptz | nullable |
| `access_ends_at` | timestamptz | NOT NULL |
| `reason` | Text | NOT NULL, 공백 불가 |
| `deactivate_global_identity` / `global_identity_deactivated` | Boolean | NOT NULL, default false |
| `impact_data` | **JSONB** | NOT NULL, default `'{}'` — 취소된 미래 책임의 snapshot |
| `cancelled_at`/`cancelled_by_member_id`/`cancellation_reason` | | 3필드 all-or-nothing CHECK, state='cancelled' 와 동기 |
| `corrected_at`/`corrected_by_member_id`/`correction_reason` | | 동일 패턴, state='corrected' 와 동기 (`0099`) |

`TimestampMixin` **없음** — `created_at`/`updated_at` 컬럼이 없다 (`organization.py:119` 은 `Base` 만 상속).

#### (5) `org_unit` — `organization.py:176-203`
| 컬럼 | 타입 | 제약 |
|---|---|---|
| `id` | UUID | PK |
| `organization_id` | UUID | FK → organization.id RESTRICT, NOT NULL |
| `parent_id` | UUID | **FK → org_unit.id RESTRICT (자기참조)**, nullable |
| `slug` | Text | NOT NULL, 공백 불가 |
| `name` | Text | NOT NULL, 공백 불가 |
| `unit_type` | Text | NOT NULL, default `'department'` — **자유 텍스트, enum 아님** (실제 값 `division`·`department`, `0065:145-150`) |
| `sort_order` | Integer | NOT NULL, default 0 |
| `active` | Boolean | NOT NULL, default true |
| `valid_from` | timestamptz | NOT NULL, `now()` |
| `valid_to` | timestamptz | nullable |
| `created_by_member_id` | UUID | FK → organization_member.id, nullable |
| `audit_reason` | Text | NOT NULL |

- UNIQUE `(organization_id, slug)`.
- CHECK `valid_to IS NULL OR valid_to > valid_from`.
- INDEX `ix_org_unit_parent(organization_id, parent_id)` (`0061:246`).
- soft delete: **`active=false` + `valid_to`** (archive). 트리 cycle 방지는 **애플리케이션**(`organization_directory.py:2718 _validate_unit_move`, `:2764 _descendant_ids`), 부모 tenant 일치는 **DB 트리거** `validate_org_unit_parent_tenant`(`0061:247`).

#### (6) `org_membership` — `organization.py:206-243`
| 컬럼 | 타입 | 제약 |
|---|---|---|
| `id` | UUID | PK |
| `org_unit_id` | UUID | FK → org_unit.id RESTRICT, NOT NULL |
| `organization_member_id` | UUID | FK → organization_member.id RESTRICT, NOT NULL |
| `change_set_id` | UUID | FK → organization_change_set.id RESTRICT, nullable |
| `is_primary` | Boolean | NOT NULL, default false |
| `valid_from`/`valid_to` | timestamptz | half-open |
| `created_by_member_id` | UUID | FK → organization_member.id, nullable |
| `audit_reason` | Text | NOT NULL |

- **EXCLUDE(gist)** `ex_org_membership_unit_no_overlap`: `(organization_member_id, org_unit_id, tstzrange(valid_from,valid_to,'[)'))` — 같은 사람이 같은 unit 에 기간 중복 소속 불가.
- **EXCLUDE(gist)** `ex_org_membership_primary_no_overlap`: `(organization_member_id, tstzrange)` **WHERE `is_primary`** — **주소속은 시점당 1개**.
- INDEX `ix_org_membership_unit(org_unit_id, valid_to)`, `ix_org_membership_member(organization_member_id, valid_to)`, `ix_org_membership_change_set`.
- soft delete 컬럼 **없음** — `valid_to` 마감만.

#### (7) `org_role` — `organization.py:246-265`
`id` / `organization_id`(FK RESTRICT) / `slug`(NOT NULL, 공백불가) / `name`(NOT NULL, 공백불가) / `description`(nullable) / `active`(NOT NULL true) / `created_by_member_id`·`updated_by_member_id`(UUID, **FK 아님**) / `audit_reason`(NOT NULL) + timestamps.
UNIQUE `(organization_id, slug)`. INDEX `ix_org_role_active(organization_id, active, name)` (`0064:113`).
soft delete = `active=false` (spec-002:136 — 이미 쓰인 어휘는 삭제 대신 비활성화).
**예약 slug `leader`** 는 개명·삭제·비활성화 불가 (spec-002:314-323). `0065:1063` 이 시드.

#### (8) `job_function` — `organization.py:268-287`
`org_role` 과 **컬럼 구조가 완전히 동일**하다 (`id/organization_id/slug/name/description/active/created_by_member_id/updated_by_member_id/audit_reason` + timestamps). UNIQUE `(organization_id, slug)`, INDEX `ix_job_function_active`.
**[사실]** spec-002:24 는 2026-08-07 prod 실측에서 `job_function`·`org_member_job_function` 이 **각 0행**이라고 기록한다 — 직능 축은 스키마만 있고 실사용이 없다.

#### (9) `org_member_job_function` — `organization.py:290-325`
`id` / `organization_member_id`(FK RESTRICT NOT NULL) / `job_function_id`(FK RESTRICT NOT NULL) / `change_set_id`(FK nullable) / `is_primary`(NOT NULL false) / `valid_from`·`valid_to` / `created_by_member_id`(UUID, **FK 아님**) / `audit_reason`(NOT NULL) + timestamps.
- EXCLUDE(gist) `(organization_member_id, job_function_id, tstzrange)` + EXCLUDE(gist) `(organization_member_id, tstzrange) WHERE is_primary`.
- CHECK `valid_to IS NULL OR valid_to > valid_from`.
- **cancellation 컬럼 없음** — 이 표에서 `org_member_role` 과 다른 유일한 축.

#### (10) `org_member_role` — `organization.py:328-383` (조직 역할 배정)
| 컬럼 | 타입 | 제약 |
|---|---|---|
| `id` | UUID | PK |
| `organization_member_id` | UUID | FK → organization_member.id RESTRICT, **NOT NULL** |
| `org_membership_id` | UUID | FK → org_membership.id RESTRICT, **nullable = 조직 전역 배정** |
| `org_role_id` | UUID | FK → org_role.id RESTRICT, NOT NULL |
| `change_set_id` | UUID | FK → organization_change_set.id, nullable |
| `valid_from`/`valid_to` | timestamptz | half-open |
| `cancelled_at`/`cancelled_by_member_id`(FK)/`cancellation_reason`/`cancellation_command_id`(UUID, FK 아님)/`cancellation_effective_at` | | 5필드 all-or-nothing CHECK |
| `created_by_member_id` | UUID | FK → organization_member.id, nullable |
| `audit_reason` | Text | NOT NULL |

- EXCLUDE(gist) `ex_org_member_role_global_no_overlap`: `(organization_member_id, org_role_id, tstzrange)` **WHERE `org_membership_id IS NULL AND cancelled_at IS NULL`**.
- EXCLUDE(gist) `ex_org_member_role_membership_no_overlap`: `(org_membership_id, org_role_id, tstzrange)` **WHERE `org_membership_id IS NOT NULL AND cancelled_at IS NULL`**.
- **트리거 `validate_org_member_role_scope`** (`0065:856-897`): membership 지정 시 ① member 일치 ② **배정 기간이 소속 기간을 벗어나지 못함**(`ORG_MEMBER_ROLE_PERIOD_OUTSIDE_MEMBERSHIP`).
- **CONSTRAINT TRIGGER `validate_org_membership_scoped_roles`** (`0065:922-929`, DEFERRABLE INITIALLY DEFERRED): 반대 방향 — 소속 기간을 줄일 때 그 안의 역할 배정이 삐져나가면 `ORG_MEMBERSHIP_PERIOD_EXCLUDES_ROLE`.
- soft delete = `cancelled_at`.

#### (11) `org_directory_event` — `organization.py:386-405` (변경 이력)
`id` / `organization_id`(FK RESTRICT NOT NULL) / `actor_member_id`(FK nullable) / `change_set_id`(FK nullable) / `entity_type`(Text NOT NULL) / `entity_id`(UUID NOT NULL, **FK 아님 — 폴리모픽**) / `event_type`(Text NOT NULL) / `before_data`(JSONB nullable) / `after_data`(JSONB **NOT NULL**) / `reason`(Text NOT NULL) / `created_at`.
- INDEX `ix_org_directory_event_entity(organization_id, entity_type, entity_id, created_at)`, `ix_org_directory_event_change_set`.
- **트리거 `guard_org_directory_event_append_only`** (`0061:459-470`) — UPDATE/DELETE 시 무조건 `RAISE EXCEPTION 'ORG_DIRECTORY_EVENT_APPEND_ONLY'`. **DB 레벨 불변 원장.**
- `TimestampMixin` 없음. soft delete 개념 없음(append-only).

#### (12) `organization_change_set` — `organization.py:408-441`
`id` / `organization_id`(FK RESTRICT NOT NULL) / `actor_member_id`(FK nullable) / `title`(NOT NULL 공백불가) / `reason`(NOT NULL 공백불가) / `effective_at`(timestamptz NOT NULL) / `operation_count`(Integer NOT NULL, **CHECK > 0**) / `source`(Text NOT NULL default `'ui'`, **CHECK `IN ('ui','api','tool')`**) / cancellation 3필드(all-or-nothing CHECK) / `created_at`.
INDEX `ix_organization_change_set_timeline(organization_id, created_at, id)`.

#### (13) `access_role` — `organization.py:444-450`
`id` / `key`(Text NOT NULL **UNIQUE**) / `name`(NOT NULL) / `description`(nullable) + timestamps.
시드 6값 (`0059:29`). **트리거 `guard_access_role_key_immutable`** — key 변경 금지.

#### (14) `org_member_access_role` — `organization.py:453-484`
`id` / `organization_member_id`(FK RESTRICT NOT NULL) / `access_role_id`(FK RESTRICT NOT NULL) / `valid_from`·`valid_to` / `granted_by_member_id`(FK nullable) / `grant_reason`(Text **NOT NULL**) / `revoked_by_member_id`(FK nullable) / `revoke_reason`(nullable) + timestamps.
- UNIQUE `(organization_member_id, access_role_id, valid_from)`.
- EXCLUDE(gist) `(organization_member_id, access_role_id, tstzrange)`.
- INDEX `ix_member_access_role_active(organization_member_id, access_role_id, valid_to)`.
- 트리거 `validate_access_role_actor_tenant`(grantor/revoker tenant 일치), `guard_last_system_admin_assignment`(마지막 관리자 보호).

#### (15) `capability` — `organization.py:487-521`
`id` / `key`(Text NOT NULL UNIQUE) / `name` / `description`(nullable) / `domain`(NOT NULL) / `resource`(nullable) / `action`(NOT NULL) / `parent_id`(FK → capability.id, **분류 전용 — authorization 에 미참여**) / `active`(NOT NULL true) + timestamps.
- CHECK `key !~ '[*]'` (와일드카드 저장 금지), CHECK `key = domain || '.' || coalesce(resource||'.', '') || action`, CHECK `parent_id <> id`.
- 트리거 `guard_capability_key_immutable`.
- 조직 도메인 leaf 11개 시드 (`0076:51-101`): `directory.basic.read`·`directory.structure.manage`·`org_member.manage`·`directory.membership.manage`·`directory.position_role.manage`·`directory.change_set.manage`·`directory.audit.read`·`directory.hr_sensitive.read`·`directory.hr_sensitive.write`·`directory.identity_link.manage`·`access_role.manage`.

#### (16) `access_role_capability` — `organization.py:524-538`
`id` / `access_role_id`(FK RESTRICT NOT NULL) / `capability_id`(FK RESTRICT NOT NULL) / `created_at`. UNIQUE `(access_role_id, capability_id)`. INDEX `ix_access_role_capability_role`.
`0076:144` — `member` 역할에는 `directory.basic.read` 하나만.

### 2.3 DB 레벨 불변식 (조직도가 애플리케이션이 아니라 **DB** 에 박아 둔 것)

**[사실]** 조직 도메인 마이그레이션(0059·0061·0064·0065·0076·0096)이 만든 PL/pgSQL 함수 **26개** / 트리거 **27개**. 성격별로:

| 성격 | 함수 |
|---|---|
| **tenant 격리** | `validate_org_unit_parent_tenant`, `validate_org_membership_tenant`, `validate_org_member_job_function_tenant`, `validate_org_member_role_scope`, `validate_organization_change_set_tenant`, `validate_org_directory_event_change_set_tenant`, `validate_org_assignment_change_set_tenant`, `validate_access_role_actor_tenant`, `validate_product_assignment_tenant`, `validate_version_assignment_tenant`, `validate_action_runtime_task_tenant`, `validate_action_runtime_action_tenant` |
| **불변성 guard** | `guard_org_directory_event_append_only`, `guard_access_role_key_immutable`, `guard_capability_key_immutable`, `protect_directory_cancellation` |
| **last-admin guard** | `guard_last_system_admin_membership`, `guard_last_system_admin_assignment`, `guard_last_system_admin_user_status` |
| **기간 정합** | `validate_org_membership_scoped_roles` (CONSTRAINT TRIGGER, DEFERRABLE) |
| **legacy 투영** | `sync_legacy_user_access_projection`, `sync_legacy_user_directory_projection`, `fill_org_member_directory_identity` |

**[사실]** 확장 의존: `btree_gist` (`0059:71`, 사전 점검 `0059:60-70` 이 확장 가용성과 CREATE 권한을 미리 검사하고 `BTREE_PREFLIGHT` 로 실패). `gen_random_uuid()`(pgcrypto/PG13+), `tstzrange`/`daterange` + GiST EXCLUDE.
**[추정]** 이 스키마는 **PostgreSQL 전용**이다. 다른 RDBMS 로는 EXCLUDE 제약과 트리거 불변식을 애플리케이션으로 옮겨야 하고, 그러면 동시성 하에서 같은 보장이 안 나온다.

---

## 3. 코드 표면 — 파일 단위 지도

### 3.1 라우터 (2개, 총 673줄) — `main.py:351-352` 에서 `/api/v1` 프리픽스로 등록

#### `back/app/routers/organization_directory.py` (380줄, prefix `/org-directory`)
capability 게이트를 `Annotated` 타입 별칭 5개로 선언하고(`:48-67`), 각 엔드포인트는 **서비스 호출 1줄**만 한다 — 라우터에 비즈니스 로직·직접 쿼리 없음.

| Method | Path | capability | 줄 |
|---|---|---|---|
| POST | `/change-sets` | `directory.change_set.manage` | :74 |
| PATCH | `/change-sets/{id}` | 〃 | :87 |
| POST | `/change-sets/{id}/cancel` (204) | 〃 | :100 |
| GET | `/scheduled-changes` | `directory.position_role.manage` | :114 |
| PATCH | `/scheduled-changes/{kind}/{id}` | 〃 | :122 |
| POST | `/scheduled-changes/{kind}/{id}/cancel` (204) | 〃 | :136 |
| **GET** | **`/members`** | `directory.basic.read` | :151 — query `status`·`user_id`·`as_of`·`cursor`·**`q`**·**`org_unit_id`**·`limit`(≤100) |
| GET | `/events` | `directory.audit.read` | :185 — `target_type`·`target_id`·`from`·`to`·`cursor`·`limit` |
| POST | `/units` (201) | `directory.structure.manage` | :208 |
| PATCH | `/units/{id}` | 〃 | :221 |
| POST | `/units/{id}/move/preview` | 〃 | :231 |
| POST | `/units/{id}/move` | 〃 | :241 |
| POST | `/units/{id}/archive/preview` | 〃 | :251 |
| POST | `/units/{id}/archive` | 〃 | :260 |
| GET/POST/PATCH | `/functions[/{id}]` | read=`basic.read`, write=`position_role.manage` | :270/:279/:292 |
| GET/POST/PATCH | `/roles[/{id}]` | 〃 | :302/:311/:324 |
| POST | `/function-assignments` (201) · `/{id}/end` | `position_role.manage` | :334/:347 |
| POST | `/role-assignments` (201) · `/{id}/end` | 〃 | :360/:373 |

응답은 전부 `DataResponse[…View]` = `{data: …}` 봉투 (`app/schemas/common.py`).

#### `back/app/routers/admin_organization.py` (293줄, prefix `/admin/organization`)
| Method | Path | capability | 줄 |
|---|---|---|---|
| GET | `/directory` | `directory.basic.read` (+`access_role.manage` 보유 시 access role 포함) | :63 |
| GET | `/access-roles` | `access_role.manage` | :79 |
| PATCH | `/members/{id}/access-role` | 〃 | :89 |
| POST | `/members` (201) | `org_member.manage` | :105 |
| PATCH | `/members/{id}` | 〃 | :121 |
| GET | `/members/{id}` | **`directory.hr_sensitive.read`** | :134 |
| GET | `/members/{id}/product-responsibilities` | `directory.basic.read` | :146 |
| POST | `/members/{id}/link-user` | `directory.identity_link.manage` | :161 |
| POST/PATCH/DELETE | `/members/{id}/employment-periods[/{pid}]` | `org_member.manage` | :177/:193/:210 |
| POST | `/members/{id}/offboarding` | `org_member.manage` (+`identity.user.update` 시 전역 비활성화 허용) | :227 |
| POST | `/members/{id}/offboarding/correct` | `org_member.manage` | :248 |
| POST | `/members/{id}/primary-membership/move` · `/end` | `directory.membership.manage` | :264/:280 |

**[사실]** HR PII 경계가 **엔드포인트 단위로 갈려 있다** — 목록(`/org-directory/members`)은 `basic.read`, 단건 상세(`/admin/organization/members/{id}`)는 `hr_sensitive.read`.

### 3.2 서비스 (5개 + 감사 1개)

| 파일 | 줄수 | 하는 일 |
|---|---|---|
| `services/organization_directory.py` | **3,544** | **도메인 로직 전부.** unit CRUD/move/archive, member 생성·수정·계정연결, 고용기간 추가·정정·취소, offboarding·correct, 소속 이동·종료, 어휘(function/role) CRUD, 배정·종료, change set 실행·예약변경·취소, 이벤트 기록, 목록/상세 조회 |
| `services/organization_directory_provider.py` | 885 | **읽기 전용 조회 provider.** 공개 동작 1개 `lookup_members(label)` — 라벨(부서·직책·직무·제품·사람)을 「지금 유효한 인원」으로 펼친다. `invitable_members()`(:368)·`active_unit_tree()`(:393)·`primary_unit_of()`(:405)·`member_ids_with_role_slugs()`(:326)·`product_assignments_now()`(:448) 등 |
| `services/legacy_organization_directory_bridge.py` | 749 | **mediness 전용.** legacy `/admin/users` 화면이 쓰는 `users.department/position/name` 을 canonical 조직도에 양방향 반영 (`bootstrap_user`·`sync_department`·`sync_position`·`sync_display_name`) |
| `services/legacy_organization_directory_reconciliation.py` | 232 | **mediness 전용.** legacy user ↔ canonical 디렉터리 정합 plan 수립·적용 |
| `services/organization_membership_scheduler.py` | 161 | APScheduler 60초 sweep — due 소속 투영(`project_due_memberships`:44)·due 퇴사 처리(`project_due_offboardings`:75)·`register_organization_membership_jobs`:154 |
| `services/org_directory_audit.py` | 141 | **mediness 전용.** legacy 마이그레이션 Phase 0 read-only 감사 |
| `services/capabilities.py` | — | `CapabilityResolver.resolve(member)`(:92) — 활성 grant → leaf 합집합. `BASE_ACCESS_ROLE = "member"`(:34) 를 항상 포함 |

**[사실]** ⚠ **레포지토리 계층이 없다.** `organization_directory.py:12` 가 `from sqlalchemy import … select` 를 하고 서비스가 직접 쿼리한다. `repositories/organization_access_repo.py`(224줄)는 조직도 쿼리 레포가 아니라 **legacy `users` 투영 전용**이다 (`:1` «Medisolve mixed-version projection between legacy users and tenant access rows»).
**[추정]** mediness 백엔드의 표준 계층(`routers/ → services/ → repositories/ → models/`)에서 조직도만 repository 를 건너뛴다. 떼어갈 때 이 3,544줄 파일이 통째로 따라오고, 그 안에 mediness 전용 legacy 투영(§4.3)이 섞여 있다.

### 3.3 스키마 — `back/app/schemas/organization_directory.py` (740줄, Pydantic v2)

**[사실]** 리터럴 3개(`:13-15`)가 상태 어휘 SoT:
- `EmploymentStatusValue = "scheduled"|"active"|"ended"|"unknown"`
- `RelationshipLifecycleState = "scheduled"|"active"|"ended"|"cancelled"`
- `OffboardingState = "scheduled"|"processed"|"cancelled"|"corrected"`
- `ScheduledChangeKind = "membership"|"job_function"|"org_role"|"offboarding"` (`:525`)

주요 View 4계층: `OrganizationMemberView`(:226, 관리용 — HR 필드 포함) / `OrganizationDirectoryMemberView`(:277, 일반 read — PII 제외) / `OrgUnitView`(:332) / `DirectoryEventView`(:502).
Request 는 전부 `reason`(min_length=1, max_length=1000) 을 **필수**로 받는다 (예: `:347`·`:367`·`:392`·`:412`) — 감사 사유 없는 write 가 불가능하다.
change set operation 은 discriminated union (`:685-710`).

### 3.4 시드 — `back/app/seeds/medi_users.py` (581줄)

**[사실]** prod DB 스냅샷(2026-07-03 최초, 2026-08-07 재확인)을 코드에 박아 둔 **mediness 전용** 시드다. 각 행이 `email/name/role/department/position` 을 갖고, 실행 시 `users` 를 만든 뒤 `organization_member`·`org_membership`·`org_member_access_role`·임원 leadership 까지 파생시킨다 (`:3-15`, `:157-172`).
**[추정]** sc-ax 로 그대로 가져갈 수 없다 — 실명·이메일이 든 mediness 명부다. 재사용한다면 «시드가 legacy `users` 축에서 조직도 축을 파생시킨다» 는 **구조**만이다.

### 3.5 프론트엔드 (참고)

`front/app/(authenticated)/admin/organization/page.tsx`(19줄) → `components/admin/organization/` 7개 파일.
`OrganizationDirectoryClient.tsx` **2,374줄** · `OrganizationMemberDialog.tsx` 1,227줄 · `OrganizationAssignmentDialog.tsx` 573줄 · `OrganizationStructureDialog.tsx` 453줄 · `OrganizationVocabularyDialog.tsx` 451줄 · `OrganizationScheduledChangesPanel.tsx` 355줄 · `OrganizationHistoryPanel.tsx` 336줄 · `OrganizationDateField.tsx` 52줄.
공용 lib: `front/lib/organization-directory.ts`(328줄, API 클라이언트) · `front/lib/organization-management-view.ts`(425줄, 뷰 모델).
재사용 컴포넌트: `front/components/organization/MemberPicker.tsx`(368줄) — 조직도 외 도메인이 쓰는 사람 선택기.
BFF 프록시: `front/app/api/admin/organization/[...path]/route.ts`.
합계 약 **6,960줄**.

### 3.6 테스트 (참고, 미실행)

`back/tests/api/` 아래 조직도 관련 **9개 파일**: `test_admin_organization.py`, `test_org_change_sets.py`, `test_org_directory_events.py`, `test_org_directory_members.py`, `test_org_directory_position_role.py`, `test_org_member_offboarding.py`, `test_org_member_product_responsibilities.py`, `test_org_membership_management.py`, `test_org_unit_management.py` (+ `test_department_space_org_*.py` 2개는 소비 도메인).

---

## 4. 결합도 — 떼어갈 때 같이 딸려오는 것

### 4.1 조직도 → 바깥 (조직도가 의존하는 것)

**[사실]**
| 대상 | 결합 형태 | 근거 |
|---|---|---|
| **`users`** (전역 계정) | `organization_member.user_id` **FK ON DELETE SET NULL** | `organization.py:51-53` |
| `users` | `employment_type` **PG enum 을 공유** — 조직도 모델이 `app.models.user` 에서 import | `organization.py:26`, `:80-88` |
| `users` | legacy 투영 트리거 3개가 `users` 를 읽고 쓴다 | `0059:312-317`, `0061:137-143` |
| **capability RBAC** (`capability`·`access_role_capability`) | 모든 조직 엔드포인트가 `require_capability(...)` 로 게이트 | `routers/organization_directory.py:50-66`, `routers/admin_organization.py:39-59` |
| `product` / `product_assignment` / `version_assignment` | offboarding coordinator 가 제품·버전 책임까지 같은 트랜잭션에서 닫는다 + tenant 트리거 2개 | `routers/admin_organization.py:33`(`MedisolveProductResponsibilityService`), `0065:265-334` |
| `department_space_*` | 부서 스페이스 접근 범위 판정이 `org_role.slug='leader'` 를 읽는다 | spec-002:318, `app/policies/department_space.py` |
| Asia/Seoul 시간대 | 퇴사 효력 경계가 KST 고정 | `services/organization_directory.py:101`, `organization_membership_scheduler.py:30` |
| APScheduler | 60초 sweep + lifespan catch-up | `organization_membership_scheduler.py:154`, organization-directory.md:174-176 |

### 4.2 바깥 → 조직도 (조직도를 소비하는 것 — 떼면 이쪽이 깨진다)

**[사실]** `app/models/organization` 을 import 하는 파일 **54개**. FK 로 직접 매달린 테이블:

| 소비 도메인 | 매달린 컬럼 | 근거 |
|---|---|---|
| WBS (`version_wbs_task`·`check_item`·`task_log`) | `organization_member.id` ×4, `org_unit.id` ×1 | `models/version_wbs.py:141,150,186,216,248` |
| 부서 스페이스 (`department_space_folder`·`document`·`share`) | `org_unit.id` ×3, `organization_member.id` ×1 | `models/department_space.py:62,104,273,276` |
| 회의 v2 (`meeting_v2`·`attendee`·`summary`·`minutes_*`) | `organization_member.id` ×6, `org_unit.id` ×6 | `models/meeting_v2.py:62,119,162,452,475,509,527,567,577,603,609,635` |
| 제품/버전 (`version_assignment`·`product_assignment`) | `organization_member.id` ×2, `org_unit.id` ×2 | `models/product_version.py:147,155,192,198` |
| Action Runtime | `organization.id` ×5, `organization_member.id` ×2, `org_unit.id` ×2 | `models/action_runtime.py:155,262,305,354,600,644,647,650,737` |
| 랜딩 챗 | `organization.id` ×1, `organization_member.id` ×2 | `models/landing_chat.py:103,106,184` |

**[사실]** 그리고 `0059:28,321-341` 이 `product`·`triggers`·`workflow_runs`·`subjects`·`actions`·`tasks` **6개 root 테이블에 `organization_id` 를 심었다** — tenant 축이 조직도 도메인 밖으로 퍼져 있다.

**[추정]** 조직도는 mediness 에서 **잎(leaf)이 아니라 뿌리**다. 6개 도메인이 사람·조직 축으로 여기에 매달려 있어서, mediness 쪽에서 «떼어낸다» 는 선택지는 사실상 없다. sc-ax 로 가져가는 것은 **복제**이지 이관이 아니다.

### 4.3 mediness 전용 legacy 오염 — 떼어갈 때 **버려야** 하는 부분

**[사실]** canonical 조직도 코드 안에 mediness 의 `users.role/department/position` 투영이 섞여 있다.

| 위치 | 내용 |
|---|---|
| `services/organization_directory.py:100` | `_LEGACY_DEPARTMENT_SLUGS = frozenset(get_args(DepartmentValue))` — mediness 8부서 enum 을 조직도 서비스가 import |
| `services/organization_directory.py:3056` | `_nearest_legacy_department(unit, units_by_id)` — org_unit 트리를 거슬러 올라가 legacy 부서 slug 를 찾는다 |
| `services/organization_directory.py:3230` | `_project_linked_user_employment(member)` — 조직도 write 가 `users` 를 되쓴다 |
| `services/organization_directory.py:39` | `from app.repositories.organization_access_repo import ACCESS_ROLE_LEGACY` |
| `services/legacy_organization_directory_bridge.py` 전체 (749줄) | `_DEPARTMENT_LABELS`(:25)·`_POSITION_LABELS`(:37)·`_ORGANIZATION_WIDE_POSITIONS`(:47) — Medisolve 고정 어휘 |
| `services/legacy_organization_directory_reconciliation.py` 전체 (232줄) | |
| `services/org_directory_audit.py` 전체 (141줄) | `VALID_ROLES`·`VALID_DEPARTMENTS`·`VALID_POSITIONS`(:11-13) 하드코딩 |
| `repositories/organization_access_repo.py` 전체 (224줄) | `LEGACY_ACCESS_ROLE`(:22) 매핑 |
| `models/organization.py:28-29` | `MEDISOLVE_ORGANIZATION_ID` 고정 UUID 상수 |
| DB 트리거 3개 | `sync_legacy_user_access_projection`·`sync_legacy_user_directory_projection`·`fill_org_member_directory_identity` |
| 마이그레이션 | `0059`·`0061`·`0065`·`0096` 안의 백필 SQL 이 전부 `MEDISOLVE_ORGANIZATION_ID` 하드코딩 |

**[추정]** 대략 **1,350줄 + 트리거 3개 + 마이그레이션 백필 SQL 전량**이 mediness 전용이다. sc-ax 에 legacy `users.department/position` 축이 없다면 이 전부가 불필요하고, 있다면 **그쪽 어휘로 새로 써야** 한다 — 그대로는 안 맞는다.

---

## 5. 재사용성 판단 재료 (설계 제안 아님 — 현황과 미결만)

### 5.1 ① 그대로 쓸 수 있는 단위 (도메인 중립 — mediness 이름이 안 들어간 것)

**[추정]** 아래 판단은 §4.3 의 legacy 목록을 제외한 나머지를 대상으로 한 것이다.

**테이블 — 조직도 코어 9개** (mediness 하드코딩 없음, 스키마 자체는 tenant-generic)
`organization` · `organization_member` · `organization_employment_period` · `org_unit` · `org_membership` · `org_role` · `org_member_role` · `org_directory_event` · `organization_change_set`
- 조건: PostgreSQL + `btree_gist` + `gen_random_uuid()`.
- 딸려오는 것: `users` 테이블(최소 `id` 하나) — `organization_member.user_id` FK 때문. `employment_type` PG enum.

**테이블 — 선택 6개**
- 권한 축 4개: `access_role` · `org_member_access_role` · `capability` · `access_role_capability` — sc-ax 가 자체 RBAC 을 가진다면 불필요. 가져가면 조직 엔드포인트의 `require_capability` 게이트를 그대로 쓸 수 있다.
- lifecycle 2개: `organization_member_offboarding`(퇴사 예약·정정이 필요할 때) · `job_function`+`org_member_job_function`(직능 축 — **mediness prod 에서 0행**, spec-002:24).

**코드 — 사실상 무수정 후보**
| 대상 | 근거 |
|---|---|
| `back/app/models/organization.py` (538줄) | mediness 의존은 `MEDISOLVE_ORGANIZATION_ID` 상수 2줄(`:28-29`)과 `EmploymentType` import(`:26`)뿐 |
| `back/app/schemas/organization_directory.py` (740줄) | mediness 어휘 참조 0 — grep 결과 `DepartmentValue` import 없음 |
| `back/app/routers/organization_directory.py` (380줄) | 서비스 위임만. capability key 문자열이 하드코딩(`:50-66`)이라 key 체계를 함께 가져가면 무수정 |
| `back/app/routers/admin_organization.py` (293줄) | 동일. 단 `:33` `MedisolveProductResponsibilityService` 와 `:146` 제품책임 엔드포인트는 mediness 전용 — 제거 대상 |
| 마이그레이션의 **DDL 부분** (`0059`·`0061`·`0064`·`0065`·`0096`·`0099`·`0076`) | `create_table`·EXCLUDE·CHECK·트리거 정의는 tenant-generic. **백필 SQL 만 mediness 전용** |
| `back/app/services/organization_directory_provider.py` (885줄) | 문서가 «도메인 중립 서비스 계층» 으로 명시 승격(`:1-13`, organization-directory.md:238-248) — 라벨→인원 해소 로직에 mediness 어휘 없음 |
| `front/components/admin/organization/*` + `front/lib/organization-*.ts` (약 6,960줄) | Next.js App Router + Tailwind 전제. sc-ax 가 같은 스택이면 이식 후보 |

### 5.2 ② 고쳐야 쓸 수 있는 지점과 이유

| # | 지점 | 왜 고쳐야 하나 | 근거 |
|---|---|---|---|
| 1 | `services/organization_directory.py` (3,544줄) | 도메인 코어와 mediness legacy 투영이 **같은 파일**에 있다. `_LEGACY_DEPARTMENT_SLUGS`·`_nearest_legacy_department`·`_project_linked_user_employment`·`ACCESS_ROLE_LEGACY` 를 걷어내야 선다 | `:39`, `:100`, `:3056`, `:3230` |
| 2 | 마이그레이션 백필 SQL | `MEDISOLVE_ORGANIZATION_ID` 하드코딩 + `users.department/position` 에서 조직 구조를 파생. sc-ax 에 그 축이 없으면 전부 무의미 | `0065:139-182`(3본부 시드), `:966-1058`(position→org_role), `:1063-1151`(임원 leadership) |
| 3 | 3본부 / 9부서 / 8직급 하드코딩 | `operations|marketing|development` + `hr|plan|design|qa|rnd|be|fe|ax|mkt` + `ceo|coo|cmo|cto|po|manager|leader|staff` 가 마이그레이션·브리지·감사 3곳에 박혀 있다 | `0065:145-150,164-166`, `bridge:25-47`, `audit:11-13` |
| 4 | `users` 스키마 전제 | 조직도가 `users.id`·`users.active`·`users.resigned_at`·`users.hire_date`·`users.employment_type`·`users.position`·`users.department` 를 읽는다. sc-ax 의 계정 테이블 형태를 알아야 FK·트리거를 맞출 수 있다 | `0061:189-213`(백필), `0065:23-134` |
| 5 | 레포지토리 계층 부재 | 서비스가 직접 `select()` 한다. sc-ax 백엔드가 계층 규율을 강제하면 3,544줄을 쪼개야 한다 | `services/organization_directory.py:12` |
| 6 | capability key 문자열 | 라우터가 `"directory.basic.read"` 등 11개 key 를 문자열로 하드코딩. sc-ax RBAC 이 다르면 게이트 전부 재배선 | `routers/organization_directory.py:50-66` |
| 7 | 문서 기준 3개 미구현 | alias · move/archive `preview_token` · `job_position` 별도 축. **문서에는 있고 코드에는 없다** (§1.4). sc-ax 가 이 기능을 요구하면 신규 구현이지 이식이 아니다 | §1.4 표 |
| 8 | 스케줄러 | APScheduler 60초 sweep + lifespan catch-up 전제. sc-ax 의 백그라운드 실행 방식에 맞춰야 한다 | `organization_membership_scheduler.py:154` |
| 9 | KST 하드코딩 | 퇴사 효력 경계가 `Asia/Seoul` 고정 | `:30`, `services/organization_directory.py:101` |
| 10 | `product_assignment`/`version_assignment` 트리거 | 조직 마이그레이션이 제품 테이블에 트리거를 심는다. sc-ax 에 그 테이블이 없으면 `0065:265-334` 가 실패 | `0065:216-334` |

### 5.3 ③ sc-ax 쪽 요구를 알아야 판단되는 미결 질문

**[사실]** 아래는 이번 조사로 답할 수 없는 것들이다. mediness 코드만으로는 결정 불가.

1. **sc-ax 는 조직 이력이 필요한가, 현재 상태만 필요한가?** — mediness 조직도의 복잡도 대부분(EXCLUDE 제약 8개·`valid_from/valid_to` 전면·`org_directory_event` append-only·change set·offboarding 예약/정정)이 **이력 보존** 때문이다. 「지금 누가 어느 부서인가」만 필요하면 9개 코어 테이블 중 3~4개로 끝난다.
2. **sc-ax 는 멀티 tenant 인가?** — `organization` root, 12개 tenant 검증 트리거, 모든 쿼리의 tenant predicate 가 전부 이 전제에서 나온다. 단일 조직이면 `organization` 테이블과 트리거 절반이 불필요하다.
3. **sc-ax 의 DB 는 PostgreSQL 인가?** — GiST EXCLUDE·`tstzrange`/`daterange`·PL/pgSQL 트리거 26개·`btree_gist`. 아니면 스키마가 성립하지 않는다.
4. **sc-ax 는 계정 없는 사람(입사예정자·계약자)을 등록해야 하는가?** — `organization_member.user_id` nullable 설계 전체가 이 요구에서 나왔다. 「계정 = 사람」이면 `organization_member` 자체가 불필요할 수 있다.
5. **sc-ax 는 조직도에서 권한을 파생하려 하는가?** — mediness 계약은 **금지**한다(spec-002:322 «리더면 자동으로 X 권한이라는 파생은 이 계약에 없다»). sc-ax 가 「팀장은 팀원 데이터를 본다」를 원하면 access_role/capability 테이블을 그대로 가져와도 그 요구는 안 풀린다.
6. **sc-ax 에 legacy 사용자 축(`users.department`/`position` 같은 것)이 있는가?** — 있으면 브리지 1,350줄을 **그쪽 어휘로 다시 써야** 하고, 없으면 전부 버릴 수 있다.
7. **sc-ax 의 조직 규모와 부서 트리 깊이는?** — mediness 는 2단(3본부 → 9부서, `0065:139-182`) + 활성 구성원 20명대(spec-002:24 «활성 22건·1인 1부서»). 다단 트리·매트릭스 조직·겸직 다수라면 `is_primary` 단일 주소속 EXCLUDE 제약(`organization.py:235-241`)이 그대로 맞는지 재검토가 필요하다.
8. **sc-ax 는 직능(job function) 축이 필요한가?** — mediness prod 에서 `job_function`·`org_member_job_function` **각 0행**(spec-002:24). 스키마는 있으나 검증된 운영 경험이 없다.
9. **sc-ax 프론트는 Next.js App Router + Tailwind 인가?** — 약 6,960줄 이식 가능 여부가 여기 달렸다.
10. **sc-ax 는 mediness 와 같은 DB 인스턴스인가, 별도인가?** — 같으면 `organization` row 추가로 tenant 분리가 되지만, mediness 의 6개 root 테이블이 이미 `organization_id` 를 갖고 있어(`0059:28`) 격리 검증 범위가 넓어진다. 별도면 순수 복제 문제다.

**[추정]** ①~⑤ 다섯 개가 답해지면 「9개 테이블 + 모델/스키마/라우터 무수정 이식」과 「테이블 3~4개로 새로 짜기」 사이의 갈림길이 정해진다. 그 판단은 사용자 몫이며 이 리포트는 설계 제안을 하지 않는다.

---

## 6. Self-check (브리프 §8)

### (a) 테이블 전수 — `back/alembic/versions/` grep 결과와 §2 표 대조

**실행한 검사**
```
grep -rn 'create_table(\s*$' -A1 back/alembic/versions/*.py | grep -E '"(organization|org_|access_role|capability|job_)'
grep -rn "rename_table" back/alembic/versions/*.py
grep -rn "__tablename__" back/app/models/*.py | grep -i "org|access|capab|member"
```

grep 이 찾아낸 `create_table` 20건 → 중복/downgrade 복원/drop 제거 후 **현재 head 16개**:

| grep 결과 | §2.1 표 | 대조 |
|---|---|---|
| `organization`(0059:74) | #1 | ✅ |
| `organization_member`(0059:93) | #2 | ✅ |
| `access_role`(0059:116) | #3 | ✅ |
| `org_member_access_role`(0059:130) | #4 | ✅ |
| `organization_employment_period`(0061:147) | #5 | ✅ |
| `org_unit`(0061:210) | #6 | ✅ |
| `org_membership`(0061:273) | #7 | ✅ |
| `org_directory_event`(0061:357) | #8 | ✅ |
| `job_position`(0064:56) | — | ❌ **0065:1156 drop** — 표에 없는 것이 맞다 |
| `org_role`(0064:86) | #9 | ✅ |
| `org_member_job_position`(0064:116) | — | ❌ **0065:1155 drop** |
| `org_membership_role`(0064:179) | #12 | ✅ (0065:797 rename → `org_member_role`) |
| `job_position`(0065:353) | — | ❌ **downgrade 복원 함수 `_restore_legacy_position_tables`** |
| `org_member_job_position`(0065:380) | — | ❌ 동일 |
| `organization_change_set`(0065:538) | #13 | ✅ |
| `job_function`(0065:671) | #10 | ✅ |
| `org_member_job_function`(0065:700) | #11 | ✅ |
| `capability`(0076:161) | #15 | ✅ |
| `access_role_capability`(0076:194) | #16 | ✅ |
| `organization_member_offboarding`(0096:69) | #14 | ✅ |

**교차검증**: `back/app/models/organization.py` 의 `__tablename__` **16개**(`:33,45,74,120,177,207,247,269,291,329,387,409,445,454,495,527`)가 위 16개와 **정확히 일치**. → **(a) 통과**

### (b) 모든 주장에 `파일:줄` 근거

- §1: 문서 표 12행 전부 파일 경로 명시, 정책 주장 9건 전부 `spec-002:NNN` / `organization-directory.md:NNN` 인용. §1.4 어긋남 3건 전부 문서 줄 + 코드 줄 양쪽 인용.
- §2: 16 테이블 × (생성 마이그레이션 `파일:줄` + 모델 `organization.py:줄범위`) 전부 표기. 제약·인덱스·트리거도 마이그레이션 줄 인용.
- §3: 라우터 엔드포인트 표 전 행에 `:줄`. 서비스 6개 전부 줄수 + 대표 심볼 줄번호.
- §4: FK 결합 표 전 행에 `models/*.py:줄`. legacy 오염 표 11행 전부 `파일:줄`.
- §5: 판단 재료 표에 근거 열을 별도로 두고 전 행 인용.
- **근거 없는 서술이 남은 곳**: §5.3 미결 질문 10개 — 이것은 «mediness 코드로 답할 수 없다» 는 성격이므로 근거 대신 «왜 답할 수 없나» 의 mediness 측 근거를 각 항목에 붙였다. → **(b) 통과**

### (c) 사실/추측 구분

전 절에서 **[사실]** / **[추정]** 태그를 문단 단위로 붙였다. **[추정]** 은 총 12곳이며 전부 「mediness 코드에서 유도한 해석」이지 검증된 결론이 아님을 본문에 명시했다. → **(c) 통과**

### 무관한 기존 문제 (이번 조사 범위 밖 — 참고만)

- `0059_organization_tenant_access.py:12` 의 `revision` 값이 `"0058_…"` 로 파일명과 어긋나는 건 **의도된 상태**다 — `0096:5-11` 이 경위와 정본(`down_revision`) 규칙을 기록하고 있고 WP-105 가 파일명 재정렬을 소유한다. 결함이 아니다.
- 조직도와 무관한 도메인(회의·WBS·Action Runtime 등)은 §4.2 의 **FK 결합 확인 범위까지만** 들여다봤다. 그 내부는 조사하지 않았다.

---

## 7. 조사하지 않은 것 (숨기지 않고 명시)

- **DB 실측 0건** — 브리프 §7 «DB 접속 금지». 테이블별 실제 행 수·데이터 분포는 확인하지 않았다. 본문의 «prod 0행» 류 서술은 전부 `spec-002:24` 의 2026-08-07 실측 기록 **인용**이지 이번 확인이 아니다.
- **테스트 미실행** — 브리프 §7. `back/tests/api/` 의 조직도 테스트 9개는 **존재만** 확인했고 통과 여부는 모른다.
- `services/organization_directory.py` 3,544줄 **전문 정독은 하지 않았다** — 심볼 아웃라인(85개 메서드)과 import·상수·핵심 메서드 위치를 확인했다. 개별 메서드의 내부 로직 정확성은 이 리포트의 주장 범위 밖이다.
- 프론트 6,960줄은 **파일 목록·줄수·역할까지만** 봤다. 컴포넌트 내부 구조는 조사하지 않았다.
- `spec-003-capability-rbac.md` 는 조직도가 소비하는 부분(leaf 카탈로그·역할 구성)까지만 spec-002 인용으로 확인했고 **전문을 읽지 않았다** — 브리프 §7 «조직도와 무관한 도메인으로 넓히지 마라».
- sc-ax 리포지토리는 **열지 않았다** — 브리프 범위 밖.
