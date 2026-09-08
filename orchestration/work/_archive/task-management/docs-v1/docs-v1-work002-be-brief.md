
# [backend] WORK-002 Phase 1 — 인증 API + WORK-001 검수 지적 1건

너는 **task-management `backend` 워커**다. 먼저 역할 문서를 읽어라 (**문서 레포 절대경로 — read-only**):

- `/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/orchestration/roles/task-management/backend/role.md`

작업 워크트리: `/Users/kknaks/orca/workspaces/task_management/docs-v1`
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

**이 워크트리는 코드 레포다.** WORK-001(스캐폴딩)이 **이 브랜치에 이미 커밋돼 있다** — `app/back`(FastAPI·Alembic·시드)과 `app/front`(Next 정적·Tauri 셸)가 돈다. 그 위에 인증을 얹는다.

먼저 확인해라: `git log --oneline -3` 에 `2a4d29a`(백) · `84882c0`(프론트)가 보여야 한다. 안 보이면 **작업을 멈추고 즉시 물어라.**

## 1. SSOT — 먼저 읽을 것 (전부 문서 레포, **읽기 전용**)

경로 기준: `/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/para/projects/summer-star/task-management/`

**빌드 계획 — 네가 실행할 것**
- `30-work/work-002-auth-session.md` — **Phase 1(인증 API)만 이번 범위다.** 작업·검증 체크리스트를 그대로 따른다. Phase 2·3(프론트)은 **네 몫이 아니다**

**계약**
- `20-spec/spec-001-auth-session.md` — **인증 계약**(API·Validation·Case Matrix·상태 전이)
- `20-spec/spec-000-scaffold.md` — 환경변수·시드(참조)

**구조·규약 (여기서 계층·파일 배치가 나온다)**
- `40-architecture/backend/README.md` — **계층·디렉토리 트리·schema/dto 경계·에러 규약·설정 env·테스트 규약**
- `40-architecture/database/README.md` + `domains/account.md` — **ERD·불변식**(account·career·auth_session·work_type·project)
- `40-architecture/system/README.md` — 구성·흐름

**정책 (참조)**
- `10-decision/decision-001-auth-settings.md` — **§4 세션**(access 1h / refresh 7d · **Bearer** · 「로그인 상태 유지」) · **§3 비밀번호 규칙** · 계정은 DB 시드로만
- `40-architecture/backend/README.md` **§8-2 code 표** — 에러 코드의 SoT. `invalid_password`(422)가 이미 등재돼 있다

## 2. 배경 / 무엇을 만드나

스캐폴딩이 끝났고 시드 계정(`kknaks`)이 DB 에 있다. 네가 **그 계정으로 로그인할 수 있는 API** 를 만든다.

끝나면 **프론트 없이도 인증이 그 자체로 돈다** — 시드 계정으로 토큰을 받고, 갱신하고, 로그아웃할 수 있다.

## 3. 계약 — 못박힌 것 (바꾸지 마라)

| 항목 | 결정 |
|---|---|
| 스택 | **FastAPI + uv**, SQLAlchemy 2.0 **async**, psycopg3, pydantic-settings, uvicorn, **Postgres** |
| 계층 | **router → service → repository.** ORM 은 repository 를 넘지 않는다. 아래층은 HTTP 를 모르고 **도메인 예외만** 던진다 |
| 데이터 이동 | **`schema` = 프론트↔백 계약 / `dto` = 백 내부 전달.** 섞지 않는다 |
| 트랜잭션 | 요청 하나가 경계 |
| 실패 | **설계한 실패만 처리** — `except Exception` 금지 · 임의 재시도 금지 · 조용한 기본값 금지. **설계 밖 예외는 그대로 전파** |
| 설정 | env → `Settings`(pydantic-settings) 하나로. **코드에 상수 금지, 비밀값 기본값 금지**(없으면 기동 실패) |
| CORS | **명시 목록**, `allow_credentials=False`(Bearer 이므로), `*` 금지 |
| 계정 | **DB 시드로만 생성.** **회원가입·비밀번호 찾기 API 를 만들지 마라** (정책상 없다) |
| 시드 계정 | `.env.example` 기본값 — 아이디 **`kknaks`** / 비밀번호 **`dev1234!`** |
| 인증 | **Bearer**(쿠키 없음, `allow_credentials=False`). access **1시간** / refresh **7일** |
| 「로그인 상태 유지」 | **서버는 관여하지 않는다** — 토큰 수명은 동일하고, refresh 를 어디 보관할지는 **클라이언트가 정한다**(OS 키체인). 서버에 보관 위치 플래그를 두지 마라 |
| 비밀번호 | 8자 이상 + 문자·숫자·특수문자. **해시만 저장** · 위반은 `invalid_password`(422) |
| 에러 코드 | **아키텍처 §8-2 표가 SoT.** 표에 없는 코드를 발명하지 마라 — 필요하면 보고 |
| 「다른 기기 모두 로그아웃」 | **v2.** 서버측 일괄 무효화를 구현하지 마라 |

## 4. 이번 범위 — WORK-001 Phase 1·2 만

**Phase 1** — 인증 API (로그인 · 갱신 · 로그아웃 · 세션)

작업·검증 항목은 **WP 문서에 그대로 있다.** 여기 옮겨 적지 않는다 — WP 를 열어서 체크리스트대로 한다.

**Phase 2·3(프론트)은 하지 마라.** `app/front` 를 건드리지 않는다.

### 함께 고칠 것 — WORK-001 검수 지적 (W-3)

`app/back/alembic/env.py:27` **docstring 이 코드와 다르다.** 주석은 「`TEST_DATABASE_URL` 이 이긴다」인데
**코드가 읽는 것은 `ALEMBIC_DATABASE_URL`** 이다. 주석을 믿고 `TEST_DATABASE_URL` 만 export 한 사람은
**운영 DB 에 마이그레이션을 걸게 된다.**

→ **주석을 `ALEMBIC_DATABASE_URL` 로 바로잡는다.** 동작은 이미 맞으니 코드는 건드리지 않는다.

## 5. allowed_paths — 이 밖은 건드리지 마라

- `app/back/` — 전부
- 루트 `docker-compose.local.yml` · `.env.example` · `Makefile` · `.gitignore`(보강만)

**문서 레포는 읽기 전용이다.** WP·SPEC·아키텍처·정책을 **고치지 마라** — 틀렸으면 보고한다.
`app/front/` 를 만들지 마라. **커밋·push·PR 하지 마라.**

## 6. 구현 단계

1. **먼저 `git log --oneline -3` 으로 WORK-001 커밋 2건을 확인한다.** 없으면 멈추고 물어라.
2. 역할 문서 → WP(Phase 1) → **SPEC-001** → 아키텍처 backend §8-2.
3. W-3 주석 정정을 먼저 해치운다(1줄).
4. Phase 1 을 구현한다. **SPEC-001 의 Case Matrix 가 에러의 SoT** 다 — 거기 있는 것만, 그대로.
5. **검증 항목을 실제로 실행**하고 결과를 보고에 적는다.

## 7. 범위 제약 — 하지 말 것

- **Phase 2·3 을 하지 않는다**(프론트). `app/front` 를 건드리지 않는다.
- **회원가입·비밀번호 찾기·소셜 로그인 API 를 만들지 않는다.**
- WORK-003 의 유형·프로젝트 CRUD 를 **미리 만들지 않는다.**
- **모델·마이그레이션은 WORK-001 이 이미 만들었다** — `auth_session` 이 필요하면 그것을 쓰고, 스키마 변경이 정말 필요하면 **먼저 보고**하라.
- 「하는 김에」 리팩터·추가 기능 금지.
- 문서를 고치지 않는다.
- **테스트를 전체로 돌리지 않는다** — 네가 만든 것만.

## 8. 검증

```
cd app/back && uv run pytest -q <네가 만들거나 고친 테스트만> (전체 스위트 금지). 계층 준수 자기점검 — ORM 이 repository 를 넘지 않는가 · schema/dto 를 섞지 않았는가 · except Exception 을 쓰지 않았는가. 검증은 1회만
```

**WP 의 Phase 1 검증 체크리스트를 전부 실행하고 결과를 보고에 적어라.** 특히:

- **시드 계정 `kknaks` / `dev1234!` 로 로그인**해서 access·refresh 를 받는가
- **틀린 비밀번호**와 **없는 아이디**가 **같은 응답**으로 거부되는가 (**어느 쪽이 틀렸는지 알려주면 안 된다** — 계정 존재가 새면 실패다)
- **만료·조작된 access** 로 보호된 경로를 부르면 거부되는가
- **refresh 로 새 access 를 받는가.** 로그아웃 뒤 **같은 refresh 가 더는 안 먹는가**
- 응답·로그에 **비밀번호 해시나 토큰 전문이 새지 않는가**
- W-3 주석이 `ALEMBIC_DATABASE_URL` 로 고쳐졌는가

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다. preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_6a4ac855-2a13-4484-b808-4c25182cbb2b --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "backend 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_6a4ac855-2a13-4484-b808-4c25182cbb2b \
  --text "[worker_done] backend 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_6a4ac855-2a13-4484-b808-4c25182cbb2b --text "[질문] backend: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
