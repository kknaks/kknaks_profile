# [backend] WORK-004 검수 수정 — 할일 응답 형태 · 기한 검증 · 연관 해제 404

너는 **task-management `backend` 워커**다. 먼저 역할 문서를 읽어라 (**문서 레포 절대경로 — read-only**):

- `/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/orchestration/roles/task-management/backend/role.md`

작업 워크트리: `/Users/kknaks/orca/workspaces/task_management/docs-v1`
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

**WORK-004 가 검수에서 FAIL 4 · WARN 10 을 받았다.** 그중 **백엔드 몫 4건**을 고친다.
**네 백엔드 구현은 대부분 통과했다** — 계층·게이트 뒷문·후보 검색은 전부 PASS 다.

## 1. SSOT — 먼저 읽을 것

**검수 리포트 — 이번 작업의 출발점**
- `orchestration/work/docs-v1/work-004-review-report.md` — **F-4 · W-1 · W-7 · W-10 행을 그대로 읽어라**

**계약(2026-09-06 갱신됨 — 갱신분이 이번 수정의 근거다)**
- `para/projects/summer-star/task-management/20-spec/spec-003-tasks-crud.md`
  — **§4 「자식 컬렉션의 쓰기 표면은 전부 갱신된 `TaskDetail` 을 돌려준다」 절**(신설) · **Case Matrix**(`invalid_project` 신설)
- `.../40-architecture/backend/README.md` — **§8-2 코드 표**(코드 4개 등재됨) · §3 규칙 7 · §7

## 2. 무엇을 고치나

### F-4 — 할일 응답 형태가 계약과 다르다 **(먼저 고쳐라)**

`POST /{task_id}/todos` 와 `PATCH /{task_id}/todos/{todoId}` 가 **`TodoItem`** 을 돌려준다.
메모·첨부·연관은 **`TaskDetail`** 을 준다 — **넷 중 할일만 다르다.**

프론트가 그걸 `TaskDetail` 로 받아 **`['tasks','detail', <할일 id>]` 에 써 넣어** 캐시가 오염된다.
`apiFetch<T>` 가 `as T` 캐스팅이라 **타입 검사가 못 잡는다.** 새 DB 에서 `task.id=1`·`todo.id=1` 이 겹치면
상세가 `TodoItem` 을 `TaskDetail` 로 렌더해 **TypeError** 가 난다.

**SPEC 이 그 자리를 비워 뒀던 것이고, 지금 채웠다** — 「자식 컬렉션의 쓰기 표면은 전부 갱신된
`TaskDetail` 을 돌려준다. 삭제만 204」. **서버를 계약에 맞춰라**:

- 두 엔드포인트의 `response_model` 을 **`TaskDetail`** 로 바꾼다
- 파생값(`todoProgress` 등)이 함께 오므로 **화면이 다시 세지 않아도 된다** — 그게 이 계약의 이유다
- **`W-7` 도 같은 뿌리다**: `POST /{task_id}/relations` 는 이미 `TaskDetail` 을 주는데 **SPEC §4 문구가
  「갱신된 연관 목록」이었다.** 문서는 코디가 고쳤다 — **네 구현이 맞았으니 그대로 두고**, 프론트가 맞춘다

### W-1 — 기한 없는 업무에 시각만 보내면 조용히 200 이 난다

`task_service.py` `_resolve_due` 에서 `{"dueStartTime":"14:00","dueEndTime":"15:00"}` 만 오면
`due_date` 가 `None` 이라 `_Due(None,None,None)` 으로 **접히고**, `_validate_due` 가 그 **접힌 결과**를 보므로
통과한다 → `due_changed=False` → 아무것도 안 바뀌고 **200**.

**계약은 422 다**(§4 Validation — 「시각이 있으면 `dueDate` 도 있어야 한다」).
**「실패가 안 보이는」 종류라 네가 지난번에 밟은 alias 함정과 같은 결이다.**

**`_resolve_due` 앞에서 요청 자체를 먼저 검사해라** — 「보낸 시각이 있는데 최종 `due_date` 가 없으면 422」.
지금은 화면이 항상 세 값을 함께 보내 도달하지 않지만, **프론트가 상세에 기한 편집을 붙이면
시각만 보내는 경로가 생긴다**(같은 라운드에서 고치는 중이다).

### W-10 — 없는 연관을 해제해도 204 다

`unlink_relation` 이 삭제문으로 0행을 지우고 끝난다. **할일·첨부는 404 를 내는데 연관만 204 다.**

**SPEC 이 정했다** — 「**없는 자식을 지우면 404** 다. 셋 다 같다. 멱등 삭제로 두지 않는다:
지우려는 것이 이미 없다는 건 화면이 낡았다는 뜻이고, 조용히 204 를 주면 그 사실이 묻힌다.」

**대상 유무를 확인해 404 를 내라.** 할일·첨부가 이미 하는 방식과 같게.

### G-2 — `invalid_project` 신설

`_require_usable_project` 가 「Case Matrix 에 프로젝트 전용 코드가 없어 `validation_error` 로 낸다 —
코드를 발명하지 않는다」라고 적고 그렇게 했다. **그 판단이 옳았다.** 이제 코드를 만들었으니 바꿔라:

- `invalid_project`(**422**) — 프로젝트가 없거나 삭제됐거나 남의 것
- **유형과 코드를 나눈 이유는 화면에 셀렉터가 둘이라서**다. 같은 코드면 어디가 틀렸는지 못 짚는다
- 주석의 「코드를 발명하지 않는다」 설명은 **이제 사실이 아니니 갱신해라**

## 3. allowed_paths — 이 밖은 건드리지 마라

- `app/back/` — 전부

**`app/front/` 을 건드리지 마라**(FE 워커가 같은 워크트리에서 F-1~F-3 을 고치는 중이다).
문서 레포도 **읽기 전용**이다. **커밋·push·PR 하지 마라.**

## 4. 검증

```
cd app/back && pytest
```

**curl 로 실물 확인** — 수치로 보고해라:

1. 할일 **추가** 응답이 `TaskDetail` 인가 — `todos` 배열과 **`todoProgress` 가 함께** 오는가
2. 할일 **수정**(체크) 응답도 같은가 — `todoProgress.done` 이 **1 늘어난 값**으로 오는가
3. 기한 없는 업무에 **시각만** 보내면 **422** 인가(고치기 전 200 → 고친 뒤 422 를 수치로)
4. 날짜와 시각을 **함께** 보내면 여전히 **200** 인가(정상 경로를 막지 않았는지)
5. 없는 연관 해제 → **404**. 있는 연관 해제 → **204**
6. 삭제된 프로젝트로 `PATCH` → **422 `invalid_project`**(전엔 `validation_error`)
7. 삭제된 유형으로 `PATCH` → **422 `invalid_work_type`**(둘이 갈리는지)

**기존 테스트 중 응답 형태를 단언하던 것이 있으면 함께 고쳐라** — 계약이 바뀐 것이지 테스트가 틀린 게 아니다.

계층 자기점검도 붙여라 — `except Exception` 0 · service 의 fastapi/schemas/models import 0 ·
router 의 models/repository import 0 · repository 의 ORM 반환 0 · `commit()` 0.

**dev DB 의 기존 행은 지우지 마라**(FE 워커가 보고 있다).

- 통과할 때까지 고친다. 못 고치면 이유와 함께 보고한다.
- 기존에 이미 깨져 있던 무관한 실패는 "무관"으로 분리해 보고한다.

## 5. 완료 보고 — **문구 변경 금지**

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
