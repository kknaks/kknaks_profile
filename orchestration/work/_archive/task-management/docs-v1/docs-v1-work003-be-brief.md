
# [backend] WORK-003 Phase 1 — 유형·프로젝트 API

너는 **task-management `backend` 워커**다. 먼저 역할 문서를 읽어라 (**문서 레포 절대경로 — read-only**):

- `/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/orchestration/roles/task-management/backend/role.md`

작업 워크트리: `/Users/kknaks/orca/workspaces/task_management/docs-v1`
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

**이 워크트리는 코드 레포다.** WORK-001(스캐폴딩)·WORK-002(인증)가 이 브랜치에 커밋돼 있다 — 로그인이 실제로 된다. 그 위에 **유형·프로젝트 관리**를 얹는다.

먼저 확인해라: `git log --oneline -3` 에 `533843e`(WORK-002 FAIL 수정)가 보여야 한다. 안 보이면 **작업을 멈추고 즉시 물어라.**

## 1. SSOT — 먼저 읽을 것 (전부 문서 레포, **읽기 전용**)

경로 기준: `/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/para/projects/summer-star/task-management/`

**빌드 계획 — 네가 실행할 것**
- `30-work/work-003-work-settings.md` — **Phase 1(유형·프로젝트 API)만 이번 범위다.** 작업·검증 체크리스트를 그대로 따른다. Phase 2·3(프론트)은 **네 몫이 아니다**

**계약**
- `20-spec/spec-002-work-settings.md` — **유형·프로젝트 계약**(API·Validation·Case Matrix·**허용 팔레트 8종**)
- `20-spec/spec-001-auth-session.md` — 세션 가드(참조)

**구조·규약 (여기서 계층·파일 배치가 나온다)**
- `40-architecture/backend/README.md` — **계층·디렉토리 트리·schema/dto 경계·에러 규약·설정 env·테스트 규약**
- `40-architecture/database/README.md` + `domains/account.md` — **ERD·불변식**(account·career·auth_session·work_type·project)
- `40-architecture/system/README.md` — 구성·흐름

**정책 (참조)**
- `10-decision/decision-001-auth-settings.md` — **§3 필드 정책**(유형: 종류·이름·색 / 프로젝트: 이름·색 / **slug 없음**) · **§4 기본 유형 3종은 삭제 불가·이름/종류 고정·색만 편집** · **소프트 딜리트**
- `40-architecture/backend/README.md` **§8-2 code 표** · **§7 트랜잭션**(`persist_changes` 규칙 포함)
- `40-architecture/database/domains/account.md` — **A-4 불변식**(기본 유형)·시드 식별 키

## 2. 배경 / 무엇을 만드나

로그인이 된다(WORK-002). 이제 **업무의 전제**를 만든다 — 업무는 유형을 반드시 참조하고 프로젝트를 선택적으로 참조하므로, 이 API 가 서야 WORK-004(내 업무)가 선다.

끝나면 **프론트 없이도 유형·프로젝트 CRUD 가 돈다** — 만들고, 고치고, 소프트 딜리트한다.

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
| 유형 | **종류(`meeting`\|`task`) + 이름 + 색.** **영문명·slug 필드를 만들지 마라** — 키는 DB 자동 생성 |
| **기본 유형 3종** | 시드로 존재. **삭제 불가 · 이름·종류 고정 · 색만 편집 가능**(DEC-001 §4 · A-4). 위반은 거부 |
| 프로젝트 | 이름 + 색 |
| 색 | **허용 팔레트 8종 중 하나**(SPEC-002 §4). 자유 hex 를 받지 마라 — 위반은 `invalid_color_token` |
| **소프트 딜리트** | 삭제해도 행은 남는다. **목록·선택지에서만 제외**하고, 이미 참조 중인 업무·회의는 **이름·색을 그대로 보여줘야 한다**(DEC-001 §4). **복원 API 는 만들지 마라**(v1 에 복원 없음) |
| 인증 | 모든 표면에 **세션 가드**. 라우터 단위 `Depends(require_account)` — 함수에서 빠뜨릴 여지를 없앤다 |
| 소유 검사 | **남의 유형·프로젝트는 404**(존재를 흘리지 않는다) |
| 에러 코드 | **아키텍처 §8-2 표가 SoT.** 표에 없는 코드를 발명하지 마라 — 필요하면 보고 |
| 트랜잭션 | 요청 하나가 경계. **`persist_changes` 를 켜지 마라** — 이번 범위에 「실패 응답이 쓰기인」 경우는 없다 |

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

1. **먼저 `git log --oneline -3` 으로 `533843e` 를 확인한다.** 없으면 멈추고 물어라.
2. 역할 문서 → WP(Phase 1) → **SPEC-002** → 아키텍처 backend §7·§8-2 · database `domains/account.md`.
3. Phase 1 을 구현한다. **SPEC-002 의 Case Matrix 가 에러의 SoT** 다 — 거기 있는 것만, 그대로.
4. **검증 항목을 실제로 실행**하고 결과를 보고에 적는다.

## 7. 범위 제약 — 하지 말 것

- **Phase 2·3 을 하지 않는다**(프론트). `app/front` 를 건드리지 않는다.
- **복원 API 를 만들지 않는다**(v1 에 복원 UI 가 없다 — DEC-004 §4).
- WORK-004 의 업무 CRUD 를 **미리 만들지 않는다.**
- **slug·영문명 필드를 만들지 않는다**(DEC-001 §3 — 자동 키로 충분하다는 결정).
- 「하는 김에」 리팩터·추가 기능 금지.
- 문서를 고치지 않는다.
- **테스트를 전체로 돌리지 않는다** — 네가 만든 것만.

## 8. 검증

```
cd app/back && uv run pytest -q <네가 만들거나 고친 테스트만> (전체 스위트 금지). 계층 준수 자기점검 — ORM 이 repository 를 넘지 않는가 · schema/dto 를 섞지 않았는가 · except Exception 을 쓰지 않았는가. 검증은 1회만
```

**WP 의 Phase 1 검증 체크리스트를 전부 실행하고 결과를 보고에 적어라.** 특히:

- 유형을 **종류·이름·색**으로 만들고 목록에 나오는가
- **기본 유형 3종**: 이름·종류 변경이 **거부**되는가 · **삭제가 거부**되는가 · **색 변경은 되는가**
- **팔레트 밖 색**(자유 hex)이 `invalid_color_token` 으로 거부되는가
- **소프트 딜리트 후**: 목록·선택지에서 **빠지는가**, 그런데 **이미 참조 중인 곳에서는 이름·색이 그대로 보이는가**
- **남의 유형·프로젝트**를 조회·수정·삭제하면 **404** 인가(403 이 아니다 — 존재를 흘리지 않는다)
- **세션 없이** 부르면 401 인가
- 이름 중복 규칙이 SPEC-002 대로인가

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
