---
type: research
title: 실제 유저 시드 경로 조사
status: draft
created_at: 2026-09-30
slug: strong-hajin-deploy
sources:
  - Strong_hajin origin/main 0a2a5a3 (read-only)
  - para/projects/summer-star/strong-hajin/40-architecture/deploy/environments.md
  - reference/2026-09-04-SC-org_data/README.md
---

# 실제 유저 시드 경로 조사

코드 근거는 Strong_hajin `origin/main` **0a2a5a3** 이다. 경로에 다른 표시가 없으면
`backend/src/ax_workspace/` 기준이다. 코드와 DB 는 건드리지 않았다. make·테스트도 실행하지 않았다.
양식은 [`reference/2026-09-30-strong-hain-seed/`](../../../reference/2026-09-30-strong-hain-seed/README.md) 에 있다.

---

## §1 결론

실제 유저는 **`dataset import`** 로 넣는 것을 권한다. 사람·소속·역할 grant·로그인을 한 transaction 에 넣는
경로는 이것 하나뿐이다(`bootstrap/dataset_import.py:93-110,523-543`). 사람을 만드는 API 는 없다(§2.5).
순서는 다음과 같다.

1. `make reset-catalog` 로 제품 catalog 만 깐다. 예시 회사 SCAX 와 데모 계정·업무는 만들어지지 않는다
2. 양식을 채우고 `SCAX_DATASET_PASSWORD=… make dataset-import TARGET=<폴더> DATASET_ARGS=--dry-run` 으로 검사한다
3. 같은 명령에서 `--dry-run` 을 빼고 적재한다

단, **이 경로는 로컬 demo DB 에서만 돈다.** 세 명령 모두 development/test 프로파일과 localhost 의
`ax_demo*`/`ax_test*` DB 를 요구한다(`entrypoints/dataset.py:140-148` · `entrypoints/reset_demo.py:13-27,47-49`).
여기에 두 공백이 겹친다.

- **운영 DB 에 스키마·catalog·유저를 넣는 코드 경로가 없다**(§2.6)
- **PRODUCTION 프로파일에는 로그인 라우트가 없다**(§5)

그래서 「실제 유저가 운영에서 로그인해 쓰는」 상태까지는 코드 변경이나 운영 절차 결정이 하나 이상 필요하다.
선택지는 §2.6·§5 에 나열했다. 판정은 하지 않았다.

---

## §2 현재 경로 지도

| 경로 | 명령 | 만드는 것 | 지우는 것 | 운영 DB 에서 |
|---|---|---|---|---|
| seed (catalog + 예시 회사) | `make reset-demo` | 스키마 전체와 catalog. 예시 회사 SCAX(단위 10), 데모 6명과 그 소속·직급·직무·보직·grant, 데모 로그인 6개(비밀번호 `DEMO_PASSWORD`), 데모 업무·요청·프로젝트 | **DB 전체**(`DROP SCHEMA public CASCADE`) | **못 돈다** |
| catalog 만 | `make reset-catalog` | 스키마 전체, 조직 단위 종류 5, capability 전부, 권장 역할 7, `daily-report-generation@1` | **DB 전체** | **못 돈다** |
| 스키마 맞춤 | `make sync-demo-schema` | 모델에 있고 DB 에 없는 표·열(ADD 만) | 없음 | 프로파일 가드만 있다(아래 주) |
| dataset import | `make dataset-import TARGET=…` | 폴더의 조직·어휘·사람·소속·보직·grant·프로젝트·로그인. 선택으로 `scenario_*` 예제 업무 | 없음(멱등 upsert) | **못 돈다** |

### 2.1 seed — `bootstrap/seed.py`

- `seed_catalog(session, demo_organization=True)` 가 입구다(`seed.py:54-67`)
  - 항상 도는 것: `_seed_product_catalog`(단위 종류·capability·역할, `seed.py:180-186`)와 `_install_daily_report_generation`(`seed.py:87-117`)
  - `demo_organization=True` 일 때만 도는 것: `_seed_demo_organization`(`seed.py:189-287`)과 `_seed_local_credentials`(`seed.py:70-84`)
- 예시 회사의 단위·보직·직급·직무는 `seed.py:120-152` 에, 데모 6명은 `SEEDED_MEMBERS`(`seed.py:169-177`)에 있다
- 데모 로그인 주소는 `<member_id>@<AX_DEMO_EMAIL_DOMAIN>`(`seed.py:48-51`)이고 기본 도메인은 `scax.example`(`bootstrap/settings.py:10,169`)이다. 비밀번호는 `DEMO_PASSWORD = "scax-demo-1234"`(`seed.py:45`)
- `seed_catalog` 를 부르는 곳은 `bootstrap/reset.py:22` 하나뿐이다. **앱 기동은 seed 를 부르지 않는다**(`reset.py:1` · `reset_demo.py:31`)

### 2.2 reset-demo / reset-catalog — `entrypoints/reset_demo.py`

- 둘은 같은 명령이다. `reset-catalog` 는 `--catalog-only` 를 붙여 부른다(`Makefile:226-227,234-235`)
- 가드는 두 겹이다
  1. `developer_auth_enabled`: 프로파일이 development/test 가 아니면 `RuntimeError` 가 난다(`reset_demo.py:47-49` · `settings.py:124-126`)
  2. `require_safe_demo_database`: postgres 면 host 가 `localhost`/`127.0.0.1`/`::1` 이고 DB 이름이 `ax_(demo|test)…` 여야 한다. sqlite 면 `demo*`/`test*.db` 여야 한다(`reset_demo.py:13-27,32`)
- 지우는 범위는 **스키마 전체**다. postgres 는 `DROP SCHEMA public CASCADE` 후 `create_all`, 그 밖에는 `drop_all` 후 `create_all` 이다(`bootstrap/reset.py:12-20`)
- catalog-only 가 아니면 이어서 `seed_demo_work` 가 돈다(`reset_demo.py:68-74`). 데모 업무 5건과 요청 7건(`bootstrap/demo_work.py:21-38`), 프로젝트 둘(`demo_work.py:171-`, 소유자 `PROJECT_OWNER = "jiho"` `demo_work.py:87`)이 생긴다. 이 픽스처는 **데모 멤버 id(`mina`·`jiho`·`yuna`)에 고정**되어 있다

### 2.3 sync-demo-schema

- `reset_demo.py --sync` 가 `bootstrap/schema_sync.apply` 를 부른다(`reset_demo.py:52-62` · `Makefile:231-232`)
- **주:** 이 경로에는 가드 1(프로파일)만 있다. `require_safe_demo_database` 는 `reset_database` 안에만 있어서(`reset_demo.py:30-33`) `--sync` 에는 걸리지 않는다. `schema_sync.apply` 자체에도 DB 이름 검사는 없다(`bootstrap/schema_sync.py:64-72`). 운영 스키마 반영에 이 경로를 쓸 수 있는지는 판정하지 않았다(OQ-6)

### 2.4 dataset import — `entrypoints/dataset.py` + `bootstrap/dataset_import.py`

- 폴더에 `manifest.yaml` 이 없으면 빈 표·manifest·README 를 만들고 멈춘다(`dataset.py:224-237`)
- 있으면 순서대로 간다
  1. 표 11개를 읽는다(`dataset.py:115-123`)
  2. 검사한다(`modules/datasets/validation.py:44-61`)
  3. 조직 단위의 순환을 검사한다(`dataset.py:240-248`)
  4. `apply_dataset` 로 넘긴다(`dataset.py:126-169`)
- 가드는 reset 과 같은 두 겹이다(`dataset.py:140-148`). 폴더는 코드 저장소 밖이어야 한다(`dataset.py:219-222`)
- 적재 순서는 단위 → 어휘(직급·직무·보직) → 역할 설치 → 사람(+재직기간·직급·암묵 주소속) → 소속·직무배정 → 보직(+grant) → 사람별 기본 역할 grant → 프로젝트 → 로그인이다(`dataset_import.py:93-110`)
- 한 transaction 이다. `--dry-run` 은 끝까지 넣어 본 뒤 rollback 한다(`dataset_import.py:523-543`). 예제 업무(`scenario_*`)는 dry-run 에서 돌지 않는다(`dataset.py:158-164`)
- 멱등이다. 같은 key 는 찾아서 갱신하고 새로 만들지 않는다. 빈 칸은 기존 값을 지우지 않는다(`dataset_import.py:223-231`)
- 로그인은 `SCAX_DATASET_PASSWORD` 하나를 새 로그인 전원에게 준다(`dataset.py:204-208` · `dataset_import.py:495-520`). 기존 로그인은 **메일만** 갱신된다(`dataset_import.py:506-511`)
- `MemberRecord.account_ref` 를 `local:<email>` 로 채운다(`dataset_import.py:517-519`)

### 2.5 목록 밖에서 나온 것 — 레코드를 만드는 곳 전수

`MemberRecord(` · `MemberCredentialRecord(` · `hash_password` · `MembershipRecord(` · `AccessGrantRecord(` ·
`OrganizationUnitRecord(` 로 `backend/src` 를 grep 한 결과다.

| 레코드 | 만드는 곳 |
|---|---|
| `MemberRecord` | `seed.py:212` · `dataset_import.py:213` — **이 둘뿐** |
| `MemberCredentialRecord` · `hash_password` 호출 | `seed.py:79-82` · `dataset_import.py:516` — **이 둘뿐** |
| `MembershipRecord` | `seed.py:231` · `dataset_import.py:271` |
| `OrganizationUnitRecord` | `seed.py:194` · `dataset_import.py:135` |
| `AccessGrantRecord` | `seed.py:274` · `dataset_import.py:390` · **`platform/organization_access.py:635`**(권한 관리 API `POST /api/access/grants`, `entrypoints/http.py:1309`) · **`platform/projects.py:267`**(프로젝트 배정이 만드는 grant) |

- **HTTP·MCP 에는 사람·로그인·조직 단위를 만드는 입구가 없다.** `http.py` 의 쓰기 라우트 중 조직 쪽은 `/api/access/grants`(생성·회수)와 `/api/access/roles/{id}`(수정)뿐이다(`http.py:1309,1326,1335`)
- 비밀번호를 바꾸는 라우트도 없다. `http.py` 의 password 는 `LoginRequest` 하나다(`http.py:260`)

### 2.6 운영 DB 로 가는 경로 — 없음

- 스키마를 만드는 코드는 `reset.py:20` 의 `create_all` 과 `schema_sync.apply` 두 곳이다. 둘 다 프로파일 가드 뒤에 있다(§2.2·§2.3). `backend/migrations/manual/` 에는 인덱스 SQL 4개만 있다(2026-09-17 · 2026-09-28)
- catalog(단위 종류·역할)가 없으면 dataset import 가 `이 제품에 없는 조직 단위 종류입니다` 로 멈춘다(`dataset_import.py:116-118`)

선택지만 나열한다. 판정은 하지 않았다.

| # | 선택지 | 필요한 것 | 주의 |
|---|---|---|---|
| A | 로컬 demo DB 에서 `reset-catalog` → `dataset-import` 를 하고, 그 DB 를 `pg_dump`/`pg_restore` 로 운영에 옮긴다 | 운영 절차만 있으면 된다. 코드 변경은 없다 | 데모 흔적 없이 catalog + 실제 유저만 옮겨진다. 이후 추가 유저도 같은 경로를 탈지는 미정이다 |
| B | 운영용 부트스트랩 명령을 새로 둔다. 가드를 「운영 DB 명시 허용」으로 바꾼 catalog 설치 + import | 코드 변경(백엔드 워커) | 파괴적 reset 과 분리해야 한다 |
| C | 운영 컨테이너 안에서 프로파일을 development 로 두고 import 를 돈다 | 코드 변경 없음 | `require_safe_demo_database` 가 여전히 DB 이름·host 로 막는다. 우회하려면 DB 이름을 `ax_demo` 로 짓고 localhost 로 붙어야 한다. 가드의 뜻을 거스른다 |

---

## §3 유저 1명이 로그인해서 쓰려면 필요한 최소 레코드

로그인 판정 사슬은 이렇다. `authenticate_with_password` 가 메일로 credential 을 찾고 비밀번호를 검증한 뒤
(`modules/organization_access/application.py:87-99`), `principal_for` 로 권한을 읽는다(`platform/organization_access.py:509-547`).
`principal_for` 는 `profile_for` 가 `None` 이면 거절한다. 조건은 **member 가 active**, **active·미종료 재직기간**
두 가지다(`organization_access.py:43-56`).

| 레코드 | 없으면 | 양식에서 받나 / 어디서 오나 |
|---|---|---|
| `organization_unit_types` | 단위를 못 만든다(`dataset_import.py:116-118`) | **catalog**(`reset-catalog`, `seed.py:120-126,182-184`) |
| `capabilities` · `roles` · `role_capabilities` | grant 가 아무것도 안 연다 | **catalog**. import 도 쓰인 역할은 설치한다(`dataset_import.py:182-198` → `seed.py:290-303`) |
| `organization_units` (최소 루트 1) | `primary_unit_key` 가 가리킬 곳이 없다 | **양식·코디**(`organization_units.csv`) |
| `members` (active) | 로그인해도 거절된다 | **양식**. `display_name` 은 사용자, `key`·`employment_state`·`primary_unit_key`·`role_key` 는 코디가 채운다 |
| `employment_periods` (active) | 로그인해도 거절된다(`organization_access.py:46-56`) | **자동**. members 행마다 만들어진다(`dataset_import.py:233-241`) |
| `memberships` (주소속) | 조직이 비어 보인다. 로그인은 된다 | **자동**. `primary_unit_key` 가 암묵 소속을 만든다(`dataset_import.py:245-251,261`) |
| `standard_grant_rules` · `access_grants` | 로그인은 되지만 **아무 기능도 못 쓴다**(capability 가 없다) | **자동**. `role_key` 가 주소속 범위로 grant 를 만든다(`dataset_import.py:343-351,375-403`). `executive` 는 루트 전체가 범위다(`dataset_import.py:377-378,406-416`) |
| `member_credentials` | 로그인 불가 | **양식** `logins.csv` 의 email + **환경** `SCAX_DATASET_PASSWORD`(`dataset_import.py:516`) |
| `grades` · `appointments` · `jobs` · `projects` | 없어도 로그인·사용이 된다 | 선택 |
| `workflow_definitions` (`daily-report-generation`) | 일일보고 생성이 안 된다(추정: 정의를 찾을 수 없음) | **catalog**(`seed.py:66,87-117`). **import 는 깔지 않는다** |

**관리자 1명 이상:** 권한 관리 쓰기는 「변경 후에도 루트 전체를 관리할 사람이 남아야 한다」를 요구한다
(`modules/organization_access/administration.py:225-236`). `organization.manage` 를 가진 역할은
`people-manager` 와 `executive` 다(`catalog.py:126-135,156-162`). 누구에게 줄지는 OQ-2 다.

---

## §4 목데이터 표면 전수

| 표면 | 어디 | 생기는 조건 | 운영(PRODUCTION)에서 새나 |
|---|---|---|---|
| 예시 회사 SCAX(단위 10·보직 6·직급 5·직무 5) | `seed.py:120-152,189-206` | `reset-demo`(catalog-only 아님) | reset 이 운영에서 못 돈다 → **안 샌다** |
| 데모 6명 + 소속·grant | `seed.py:169-177,208-287` | 같음 | 같음 |
| 데모 로그인 6개 · `DEMO_PASSWORD` | `seed.py:43-45,70-84` | 같음 | 같음 |
| 데모 업무·요청·프로젝트 | `demo_work.py:21-38,171-` · `reset_demo.py:68-74` | `reset-demo` 만 | 같음 |
| `/api/auth/providers` 의 `demo_accounts` · `demo_password` | `http.py:626-641` | `local_login_enabled`(비-PRODUCTION) | **안 샌다**. PRODUCTION 은 `{"local": false, "oidc": false}` 만 준다(`http.py:634-635`) |
| `demo_accounts` 목록 필터 | `organization_access.py:752-778`. `AX_DEMO_EMAIL_DOMAIN` 도메인 credential 만 나열한다 | 비-PRODUCTION | (아래 주 1) |
| 프론트 「바로 로그인」 | `frontend/src/features/auth/LoginPage.tsx:53-58,77-111` · `frontend/src/lib/api.ts:762-763` | `demo_accounts` 가 비어 있지 않을 때 | 서버가 안 주면 안 그린다 → **안 샌다** |
| `X-Demo-Persona` 헤더 이음새 | `http.py:621-624` · `entrypoints/http_auth.py:25-38,69-79,82-99` | development/test 만 붙는다 | **안 붙는다**. PRODUCTION 은 세션만 본다 |
| MCP persona(`AX_MCP_PERSONA`) | `entrypoints/mcp.py:1340-1345` · 파사드 가드 `mcp.py:259-260` | development/test 만 | (아래 주 2) |
| `SEEDED_MEMBERS` import(정렬용) | `http.py:201,638` | 비-PRODUCTION 분기 안 | 정렬에만 쓴다. 데이터는 안 만든다 |
| `WorkflowDefinitionRecord.owner_id/scope` 기본값 `"scax"` | `platform/persistence.py:574-575` · `seed.py:94-96` | catalog | 문자열 라벨이다. 예시 회사 FK 가 아니다. 새는 것은 아니지만 이름이 남는다 |
| 로그인 화면 문구 `SCAX` | `LoginPage.tsx:64-75` | 항상 | 제품명이다. 목데이터는 아니다 |

**주 1 — 비-PRODUCTION 에서 실제 계정이 목록에 오를 수 있다.** `AX_DEMO_EMAIL_DOMAIN` 을 실제 유저 메일
도메인으로 두면 실제 계정이 「바로 로그인」에 나열된다. 선례가 이 방식을 의도적으로 썼다(SC README
「로그인 계정」). 이때 바로가기는 `DEMO_PASSWORD` 로 제출한다(`LoginPage.tsx:54-58`). 따라서
`SCAX_DATASET_PASSWORD` 를 `scax-demo-1234` 와 같게 주면(선례 README 실행법이 그 값을 썼다) **누구나 클릭
한 번으로 실제 유저로 들어간다.** 운영이 비-PRODUCTION 프로파일로 뜨는 경우(§5 선택지 3)에만 해당한다.

**주 2 — PRODUCTION 에서는 MCP 가 막힌다.** 대화 AI 가 여는 MCP 서버의 파사드는 PRODUCTION 에서
`RuntimeError` 를 낸다(`mcp.py:259-260`). 목데이터가 새는 문제는 아니지만, **운영에서 AX 대화의 도구 호출이
돌지 않는다**는 또 하나의 운영 공백이다. 이 조사 범위 밖이라 영향 범위는 확인하지 않았다(OQ-8).

---

## §5 PRODUCTION 로그인 공백

**결론: 지금 코드로는 실제 유저가 PRODUCTION 에서 로그인할 수 없다.**

| 자리 | 무엇이 막나 |
|---|---|
| `bootstrap/settings.py:128-131` | `local_login_enabled` 가 `profile is not PRODUCTION` 이다. 운영에서는 False 다 |
| `entrypoints/http.py:643-645` | `/api/auth/login` 을 `local_login_enabled` 일 때만 **등록**한다. 운영에는 라우트가 없다 |
| `entrypoints/http.py:634` | `oidc` 는 상수 `False` 다. OIDC 구현은 없고 docstring 에 계획만 있다(`http_auth.py:5-6`) |
| `entrypoints/http.py:621-624` · `http_auth.py:69-79` | 개발 헤더 이음새도 운영에는 없다. 남는 인증은 세션 쿠키뿐이다 |
| `frontend/src/features/auth/LoginPage.tsx:114-` | 폼은 `providers.local` 이 true 일 때만 그린다. 운영 화면에는 로그인 폼이 없다 |

세션을 만드는 곳은 `/api/auth/login` 하나다(`http.py:653`). 그러니 운영에서 세션을 얻을 길이 없다.
`environments.md` 「아직 배포할 수 없는 이유」 2번과 같은 사실이다.

선택지는 다음과 같다. 나열만 하고 판정은 하지 않았다.

| # | 선택지 | 코드 변경 | 따라오는 것 |
|---|---|---|---|
| 1 | PRODUCTION 에서도 로컬 이메일/비밀번호 로그인을 연다(`local_login_enabled` 를 env 플래그로 분리하는 식) | 백엔드 소량 | `demo_accounts` 가 같은 조건에 묶여 있다(`http.py:635`). 바로가기 노출을 따로 끊어야 한다. 비밀번호 변경·재설정 경로가 없다(§2.5) |
| 2 | 외부 IdP(OIDC, docstring 은 Google 을 언급)를 붙인다 | 백엔드 + 프론트, 중간 규모 | IdP 계정 ↔ `members` 연결 규칙이 필요하다. `account_ref` 열이 그 자리 후보다(`persistence.py:74`). 이 경우 비밀번호 칸 문제가 사라진다 |
| 3 | 운영을 비-PRODUCTION 프로파일(development)로 띄운다 | 없음 | `X-Demo-Persona` 헤더만으로 **아무 멤버로나 행세할 수 있다**(`http_auth.py:74-78`). 쿠키 `secure` 가 꺼진다(`http_auth.py:106-107`). `demo_password` 가 응답에 실린다(`http.py:640`). §4 주 1 의 위험도 있다 |
| 4 | 앞단 프록시 인증(Cloudflare Access 등)이 신원을 주고 앱이 그 헤더로 세션을 만든다 | 백엔드 | 새 신뢰 경계다. 설계가 필요하다 |

---

## §6 Open Questions

양식 README 의 OQ-S1~S7 과 겹치는 것은 그 번호를 함께 적었다.

| # | 질문 | 왜 못 정했나 |
|---|---|---|
| OQ-1 (=S7) | 비밀번호 전달 방식. 공용 1개(현행 코드)인가, 사람별인가(코드 변경). 전달 채널은 무엇인가. 첫 로그인 후 변경은 어떻게 하나(API 없음) | 로그인 방식(OQ-5)에 따라 필요 없어질 수 있다 |
| OQ-2 (=S2) | 조직 관리자(`executive`/`people-manager`)를 누구에게, 몇 명 주나 | 사람에 대한 결정이다 |
| OQ-3 (=S3) | 조직 구조를 양식에서 받나, 루트 1개 기본값으로 두나. 루트의 key·이름은 무엇인가 | 사용자는 「유저 정보만」 준다고 했다 |
| OQ-4 (=S5) | `members.key` 규칙. 선례처럼 임시 사번 `1001`~ 인가, 읽히는 slug 인가 | 한 번 넣으면 id 라서 바꾸기 어렵다 |
| OQ-5 | PRODUCTION 로그인 수단(§5 선택지 1~4) | 제품 결정이다 |
| OQ-6 | 운영 DB 에 스키마·catalog·유저를 넣는 절차(§2.6 A~C). `sync-demo-schema` 를 운영 스키마 반영에 써도 되나 | 운영 절차 결정이다 |
| OQ-7 (=S1) | 채운 양식(실명·메일)을 kknaks_profile Git 에 두나. 선례 README 는 「Git 밖」이라 했지만 선례 CSV 는 추적 중이다 | 저장소 정책이다 |
| OQ-8 | 운영에서 MCP 가 막히는 것(`mcp.py:259-260`)을 같은 배포 작업에서 다루나 | 이 조사 범위 밖이다 |
| OQ-9 (=S4·S6) | 직급·전화·생년월일을 받나. 전화·생년월일은 운영 스키마 gate 가 따로 있다(`persistence.py:69-71`) | 사용자 결정이다 |
| OQ-10 | 로컬 demo DB 에서 실제 유저를 먼저 넣어 확인할 때 `AX_DEMO_EMAIL_DOMAIN` 을 실제 도메인으로 둘 것인가(§4 주 1) | 편의와 노출 사이의 결정이다 |
| OQ-11 | `daily-report-generation` 워크플로 정의는 catalog 에만 있다. 운영 경로 A 는 dump 에 실려 가지만 B·C 는 따로 챙겨야 한다 | OQ-6 에 딸려 있다 |

---

## 부록 — 양식 열 ↔ 코드 대조표

헤더를 기계로 대조했다. `modules/datasets/schema.py` 의 `TABLES` 를 import 해 각 CSV 첫 줄과 비교했다.
결과는 **11/11 일치**다. 예시 행을 포함한 폴더를 `validate()` 에 넣은 결과는 problems 0 이다. DB 는 쓰지 않았다
(순수 함수만 불렀고 `PYTHONDONTWRITEBYTECODE=1`, 코드 워크트리 `git status` 는 깨끗하다).

| 양식 파일 · 열 | 스키마 정의 | 읽는 자리(importer) | 필수 |
|---|---|---|---|
| `organization_units.key` | `schema.py:64` | `dataset_import.py:115,131-136` | ○ |
| `organization_units.name` | `schema.py:65` | `dataset_import.py:136,142` | ○ |
| `organization_units.unit_type` | `schema.py:66` | `dataset_import.py:116-118,136` | ○ |
| `organization_units.parent_key` | `schema.py:67` | `dataset_import.py:123,128-130` | × |
| `organization_units.display_order` | `schema.py:68` | `dataset_import.py:132` | × |
| `grades.key` · `name` · `display_order` | `schema.py:72` | `dataset_import.py:152-156` | ○ · ○ · × |
| `jobs.key` · `name` | `schema.py:73` | `dataset_import.py:159-162` | ○ · ○ |
| `positions.key` · `name` · `unit_type` · `slot` · `role_key` | `schema.py:78-82` | `dataset_import.py:166-175,189,310` | ○ · ○ · ○ · × · × |
| `members.key` | `schema.py:90` | `dataset_import.py:205` | ○ |
| `members.display_name` | `schema.py:91` | `dataset_import.py:215` | ○ |
| `members.employment_state` | `schema.py:92` | `dataset_import.py:206,237` | ○ |
| `members.employment_type` | `schema.py:93` | `dataset_import.py:207` | × |
| `members.primary_unit_key` | `schema.py:94` | `dataset_import.py:247,348` | ○ |
| `members.role_key` | `schema.py:95` | `dataset_import.py:188,309,347` | ○ |
| `members.grade_key` | `schema.py:96` | `dataset_import.py:242` | × |
| `members.employed_from` | `schema.py:97` | `dataset_import.py:239` | × |
| `members.employed_until` | `schema.py:98` | `dataset_import.py:238` | × |
| `members.phone` | `schema.py:100` | `dataset_import.py:208` | × |
| `members.birth_date` | `schema.py:101` | `dataset_import.py:209` | × |
| `memberships.*`(5열) | `schema.py:109-113` | `dataset_import.py:261-277` | member·unit·kind ○ |
| `appointments.*`(6열) | `schema.py:122-127` | `dataset_import.py:311-335` | member·unit·position·kind ○ |
| `job_assignments.*`(3열) | `schema.py:136-138` | `dataset_import.py:282-288` | ○ |
| `projects.*`(6열) | `schema.py:147-152` | `dataset_import.py:431-441` | key·name ○ |
| `project_assignments.*`(5열) | `schema.py:159-163` | `dataset_import.py:452-488` | member·project·kind ○ |
| `logins.member_key` | `schema.py:173` | `dataset_import.py:504` | ○ |
| `logins.email` | `schema.py:174` | `dataset_import.py:505` | ○ |
| (비밀번호) | 표에 없다(`schema.py:176` note) | `dataset.py:204-208` → `dataset_import.py:512-516` | env |
| `manifest.yaml` | `dataset.py:78-94` 모양 | 있는지만 본다(`dataset.py:224`) | 파일 필수 |
