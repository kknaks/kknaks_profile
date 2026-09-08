
# [backend] WORK-001 Phase 1·2 — 백엔드 기동 · 스키마 · 시드

너는 **task-management `backend` 워커**다. 먼저 역할 문서를 읽어라 (**문서 레포 절대경로 — read-only**):

- `/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/orchestration/roles/task-management/backend/role.md`

작업 워크트리: `/Users/kknaks/orca/workspaces/task_management/work-001-scaffold`
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

**이 워크트리는 코드 레포다.** 레포에 README·.gitignore 만 있는 **빈 상태**이고, 네가 첫 코드를 만든다.

## 1. SSOT — 먼저 읽을 것 (전부 문서 레포, **읽기 전용**)

경로 기준: `/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/para/projects/summer-star/task-management/`

**빌드 계획 — 네가 실행할 것**
- `30-work/work-001-scaffold.md` — **Phase 1·2 가 이번 범위다.** 작업·검증 체크리스트를 그대로 따른다. Phase 3(프론트)·4(Tauri)는 **네 몫이 아니다**

**계약**
- `20-spec/spec-000-scaffold.md` — 기동·환경변수·헬스체크·시드 계약

**구조·규약 (여기서 계층·파일 배치가 나온다)**
- `40-architecture/backend/README.md` — **계층·디렉토리 트리·schema/dto 경계·에러 규약·설정 env·테스트 규약**
- `40-architecture/database/README.md` + `domains/account.md` — **ERD·불변식**(account·career·auth_session·work_type·project)
- `40-architecture/system/README.md` — 구성·흐름

**정책 (참조)**
- `10-decision/decision-001-auth-settings.md` — 계정은 **DB 시드로만 생성**, 비밀번호 규칙, 기본 유형 3종

## 2. 배경 / 무엇을 만드나

문서(정책·아키텍처·spec·WP)가 전부 서 있고 **코드는 아직 한 줄도 없다.** 네가 백엔드의 바닥을 놓는다.

끝나면 **화면이 없어도 백엔드가 그 자체로 돈다** — compose 로 Postgres·API 가 뜨고, 헬스체크가 DB 왕복을 포함해 응답하고, 마이그레이션과 시드가 멱등하게 돈다.

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
| 계정 | **DB 시드로만 생성.** 회원가입 API 를 만들지 마라 |
| 비밀번호 | 8자 이상 + 문자·숫자·특수문자. **해시만 저장** |
| 기본 유형 | 시드 3종(미팅·회의 / 개인 업무 / 문서·보고), `is_default` |

## 4. 이번 범위 — WORK-001 Phase 1·2 만

**Phase 1** — 레포 초기화 · 백엔드 기동 · 헬스체크
**Phase 2** — Alembic · account 도메인 마이그레이션 · 시드

작업·검증 항목은 **WP 문서에 그대로 있다.** 여기 옮겨 적지 않는다 — WP 를 열어서 체크리스트대로 한다.

**Phase 3·4(프론트·Tauri)는 하지 마라.** `app/front` 를 만들지 않는다.

## 5. allowed_paths — 이 밖은 건드리지 마라

- `app/back/` — 전부
- 루트 `docker-compose.local.yml` · `.env.example` · `Makefile` · `.gitignore`(보강만)

**문서 레포는 읽기 전용이다.** WP·SPEC·아키텍처·정책을 **고치지 마라** — 틀렸으면 보고한다.
`app/front/` 를 만들지 마라. **커밋·push·PR 하지 마라.**

## 6. 구현 단계

1. 역할 문서 → WP(Phase 1·2) → SPEC-000 → 아키텍처 backend·database.
2. **Phase 1 을 끝내고 검증까지 통과시킨 뒤** Phase 2 로 간다. 반쯤 만든 채로 넘어가지 않는다.
3. Phase 2 의 마이그레이션은 **`autogenerate` 초안을 사람이 읽고 고친다** — CHECK 제약·부분 유니크·인덱스는 `domains/account.md` 의 불변식을 보고 손으로 채운다.
4. 각 Phase 의 **검증 항목을 실제로 실행**하고 결과를 보고에 적는다.

## 7. 범위 제약 — 하지 말 것

- **Phase 3·4 를 하지 않는다**(프론트·Tauri).
- WORK-002·003 의 기능(로그인 API·유형/프로젝트 CRUD)을 **미리 만들지 않는다.** 이번은 **바닥만**이다. 단 **모델·마이그레이션은 Phase 2 범위대로** account·career·auth_session·work_type·project 를 함께 만든다(WP 가 그렇게 잡았다).
- 「하는 김에」 리팩터·추가 기능 금지.
- 문서를 고치지 않는다.
- **테스트를 전체로 돌리지 않는다** — 네가 만든 것만.

## 8. 검증

```
cd app/back && uv run pytest -q <네가 만들거나 고친 테스트만> (전체 스위트 금지). 계층 준수 자기점검 — ORM 이 repository 를 넘지 않는가 · schema/dto 를 섞지 않았는가 · except Exception 을 쓰지 않았는가. 검증은 1회만
```

**WP 의 Phase 1·2 검증 체크리스트를 전부 실행하고 결과를 보고에 적어라.** 특히:

- 헬스체크가 **DB 컨테이너를 내리면 503 `db_unavailable`** 인가 (200 「정상」이면 실패다)
- `JWT_SECRET` 을 지우면 **기동이 실패**하고 누락 변수명이 로그에 남는가
- **`make seed` 를 두 번 실행해도 행 수가 그대로**인가
- 시드 비밀번호가 규칙 위반이면 **시드가 실패**하는가
- `alembic downgrade -1` → `upgrade head` 왕복이 되는가

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
