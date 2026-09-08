
# [backend] WORK-004 Phase 1~3 — 업무 도메인 · 본체 API · 자식 컬렉션

너는 **task-management `backend` 워커**다. 먼저 역할 문서를 읽어라 (**문서 레포 절대경로 — read-only**):

- `/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/orchestration/roles/task-management/backend/role.md`

작업 워크트리: `/Users/kknaks/orca/workspaces/task_management/docs-v1`
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

**이 워크트리는 코드 레포다.** WORK-001(스캐폴딩)·WORK-002(인증)가 이 브랜치에 커밋돼 있다 — 로그인이 실제로 된다. 그 위에 **유형·프로젝트 관리**를 얹는다.

먼저 확인해라: `git log --oneline -3` 에 `61ac762`(WORK-003 검수 F-1 수정)가 보여야 한다. 안 보이면 **작업을 멈추고 즉시 물어라.**

## 1. SSOT — 먼저 읽을 것 (전부 문서 레포, **읽기 전용**)

경로 기준: `/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/para/projects/summer-star/task-management/`

**빌드 계획 — 네가 실행할 것**
- `30-work/work-004-tasks-crud.md` — **Phase 1·2·3 이 이번 범위다**(백엔드). 작업·검증 체크리스트를 그대로 따른다. Phase 4·5·6(프론트)은 **네 몫이 아니다**

**계약**
- `20-spec/spec-003-tasks-crud.md` — **업무 계약**(API·Validation·Case Matrix·상태 전이)
- `20-spec/spec-002-work-settings.md` — 유형·프로젝트를 참조하는 쪽(참조)

**구조·규약 (여기서 계층·파일 배치가 나온다)**
- `40-architecture/backend/README.md` — **계층·디렉토리 트리·schema/dto 경계·에러 규약·설정 env·테스트 규약**
- `40-architecture/database/README.md` + `domains/account.md` — **ERD·불변식**(account·career·auth_session·work_type·project)
- `40-architecture/system/README.md` — 구성·흐름

**정책 (참조)**
- `10-decision/decision-002-my-tasks.md` — **§3 필드**(유형 필수·프로젝트 N:1 무소속·**`due_date` 는 업무가 소유**) · §4 생명주기 · **소프트 딜리트**
- `10-decision/decision-005-calendar.md` §3 — **`schedule` 은 파생**·겹침 차단
- `40-architecture/backend/README.md` **§8-2 code 표** · **§7 트랜잭션**
- `40-architecture/database/domains/task.md` · `calendar.md` — **불변식**(T-·C-)

## 2. 배경 / 무엇을 만드나

유형·프로젝트가 선다(WORK-003). 이제 **제품의 원자 도메인**을 만든다 — 회의록·캘린더가 전부 업무를 참조한다.

끝나면 **프론트 없이도 업무 CRUD 가 돈다** — 만들고, 열고, 고치고, 할일·메모·첨부·연관을 붙인다.

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
| 업무 필드 | **제목 필수 · 유형 필수**(WORK-003 목록 참조) · **프로젝트 0..1**(무소속 허용) · `due_date` **업무가 소유** |
| **`schedule` 은 파생** | 기한이 있으면 **종일 일정**으로, 시간까지 지정하면 시간 일정으로 파생한다. **`PATCH /api/schedules` 를 만들지 마라** — 원본을 고치면 파생이 따라간다(단방향) |
| **겹침 차단** | 시간 있는 일정끼리 겹치면 **거부**. 종류 불문(업무↔회의), 종일·기간은 검사 제외, **끝시각=시작시각은 겹침 아님**, 취소 제외 |
| **상태** | 생성 시 `시작전` 고정. **상태 전이는 이번 범위가 아니다**(WORK-005 가 전용 엔드포인트로 소유) — **일반 PATCH 로 `status` 를 받지 마라. 보내면 422** |
| **첨부** | **URL 링크만 실동작.** `document_id` 컬럼·CHECK 는 **최종 형태로 두되 FK 를 걸지 않고**, `kind=doc` 요청은 **거부**한다 — 문서함 work 가 FK 리비전과 함께 실체화한다(사용자 확정) |
| 소프트 딜리트 | 삭제해도 행은 남는다. 목록·집계에서 제외. **복원 API 를 만들지 마라** |
| 인증 | 라우터 단위 `Depends(require_account)` |
| 소유 검사 | **남의 업무는 404** |
| 에러 코드 | **아키텍처 §8-2 표가 SoT.** 표에 없는 코드를 발명하지 마라 — 필요하면 보고 |
| 트랜잭션 | 요청 하나가 경계. **`persist_changes` 를 켜지 마라** |

## 4. 이번 범위 — WORK-001 Phase 1·2 만

**Phase 1** — 유형·프로젝트 API (목록·생성·수정·소프트 딜리트)

작업·검증 항목은 **WP 문서에 그대로 있다.** 여기 옮겨 적지 않는다 — WP 를 열어서 체크리스트대로 한다.

**Phase 2·3(프론트)은 하지 마라.** `app/front` 를 건드리지 않는다.

**모델·마이그레이션은 WORK-001 이 이미 만들었다**(`work_type`·`project`). 스키마 변경이 정말 필요하면 **먼저 보고**하라.

## 5. allowed_paths — 이 밖은 건드리지 마라

- `app/back/` — 전부
- 루트 `docker-compose.local.yml` · `.env.example` · `Makefile` · `.gitignore`(보강만)

**문서 레포는 읽기 전용이다.** WP·SPEC·아키텍처·정책을 **고치지 마라** — 틀렸으면 보고한다.
`app/front/` 를 만들지 마라. **커밋·push·PR 하지 마라.**

## 6. 구현 단계

1. **먼저 `git log --oneline -3` 으로 `61ac762` 를 확인한다.** 없으면 멈추고 물어라.
2. 역할 문서 → WP(Phase 1~3) → **SPEC-003** → 아키텍처 backend §7·§8-2 · database `domains/task.md`·`calendar.md`.
3. **Phase 를 순서대로** 하고, 각 Phase 끝에서 검증까지 통과시킨 뒤 다음으로 간다.
4. **SPEC-003 의 Case Matrix 가 에러의 SoT** 다 — 거기 있는 것만, 그대로.
5. **검증 항목을 실제로 실행**하고 결과를 보고에 적는다.

## 7. 범위 제약 — 하지 말 것

- **Phase 4·5·6 을 하지 않는다**(프론트).
- **상태 전이 엔드포인트를 만들지 않는다** — WORK-005 몫이다. 일반 PATCH 로 `status` 를 받지도 마라.
- **`PATCH /api/schedules` 를 만들지 않는다**(파생은 단방향).
- **복원 API 를 만들지 않는다.**
- 회의록·캘린더 표면을 **미리 만들지 않는다.**
- 「하는 김에」 리팩터·추가 기능 금지.
- 문서를 고치지 않는다.
- **테스트를 전체로 돌리지 않는다** — 네가 만든 것만.

## 8. 검증

```
cd app/back && uv run pytest -q <네가 만들거나 고친 테스트만> (전체 스위트 금지). 계층 준수 자기점검 — ORM 이 repository 를 넘지 않는가 · schema/dto 를 섞지 않았는가 · except Exception 을 쓰지 않았는가. 검증은 1회만
```

**WP 의 Phase 1~3 검증 체크리스트를 전부 실행하고 결과를 보고에 적어라.** 특히:

- 업무를 **제목 + 유형**만으로 만들고 상태가 `시작전` 인가. **유형 없이 만들면 거부**되는가
- **프로젝트 없이도** 만들어지는가(무소속 허용)
- **기한을 넣으면 `schedule` 에 종일 일정이 파생**되는가. 시간까지 넣으면 시간 일정인가. 기한을 지우면 파생 행도 사라지는가
- **겹치는 시간**으로 만들면 거부되는가. **끝시각=시작시각은 통과**하는가
- **일반 PATCH 로 `status` 를 보내면 422** 인가(상태 전이는 WORK-005 몫)
- **`kind=doc` 첨부가 거부**되고 **URL 링크는 되는가**
- **남의 업무**를 조회·수정·삭제하면 **404** 인가
- 삭제 후 목록에서 빠지고 **DB 에는 행이 남는가**
- 삭제된 유형·프로젝트를 참조 중인 업무가 **이름·색을 그대로 보여주는가**(A-6)

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
