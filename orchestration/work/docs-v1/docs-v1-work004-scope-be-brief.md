
# [backend] WORK-004 소수정 — 후보 검색에 `scope` 필터와 `total` 추가

너는 **task-management `backend` 워커**다. 먼저 역할 문서를 읽어라 (**문서 레포 절대경로 — read-only**):

- `/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/orchestration/roles/task-management/backend/role.md`

작업 워크트리: `/Users/kknaks/orca/workspaces/task_management/docs-v1`
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

**네가 방금 만든 `GET /api/tasks/relations/candidates` 를 이어서 고친다.** 그 커밋은 이미 들어가 있다(`70924d7`).

## 1. 왜 다시 부르나

프론트가 U-8 팝오버를 붙이다 **필터 칩 3 을 붙일 수 없다**고 보고했다.
칩(「이 프로젝트」 기본 선택 / 「최근 30일」 / 「전체」)은 **필터**인데, 표면에는 `projectId`·`dueDate`
**정렬 힌트만** 있어 칩을 눌러도 같은 목록이 세 번 나온다. 카운트 「n건 중 m」의 `n`(총계)도 응답에 없다.

**계약을 갱신했다.** 아래 SPEC 을 읽고 그대로 구현해라 — 발명하지 마라.

## 2. SSOT — 먼저 읽을 것

- `para/projects/summer-star/task-management/20-spec/spec-003-tasks-crud.md`
  - **§4 의 `GET /api/tasks/relations/candidates` 절**(2026-09-06 갱신) — `scope` 표와 `total` 규칙이 거기 있다
  - **§U-8** — 칩 3 과 카운트가 무엇을 뜻하는지
- `.../40-architecture/backend/README.md` — §3(특히 **규칙 7 — 쿼리 alias**) · §7 · §8

## 3. 무엇을 고치나

### (1) `scope` 파라미터 — 정렬이 아니라 **자르는 필터**다

| 값 | 무엇을 남기나 |
|---|---|
| `project`(기본) | **기준 프로젝트와 같은 프로젝트**만. 기준은 `excludeId` 가 있으면 **그 업무의 프로젝트**, 없으면 `projectId` |
| `recent30` | **최근 수정 30일 이내**만 |
| `all` | 자르지 않는다 |

**기준 프로젝트가 없는데 `scope=project` 가 오면 `all` 과 같게 답한다.** 빈 목록을 주지 마라 —
무소속 업무이거나 생성 드로어에서 프로젝트를 아직 안 고른 정상 경로이고, 고를 게 없는 팝오버가 뜨는 게 더 나쁘다.
**이건 SPEC 이 명시한 동작이지 폴백이 아니다** — 주석에 SPEC 근거를 적어라.

`scope` 에 세 값 밖이 오면 **422**(FastAPI 의 enum 검증에 맡긴다 — 손으로 잡지 마라).

### (2) 응답에 `total`

`scope` 를 **적용한 뒤의 총계**다. `items` 는 거기서 정렬 상위 20건 그대로.
`total` 은 `len(items)` 가 아니다 — 20건을 넘으면 갈린다. **count 쿼리로 센다.**

### (3) 정렬·스코프는 그대로

같은 프로젝트 → 기한 ±7일 → 최근 수정, 최대 20건, 삭제분 제외, 계정 스코프. **건드리지 마라.**

## 4. 함정 — 네가 지난번에 찾은 것

**`Query(alias=...)` 를 빠뜨리면 `scope` 가 조용히 무시되고 기본값으로 200 이 난다.**
`scope` 는 소문자 한 단어라 alias 가 없어도 우연히 통하지만, **그 우연에 기대지 마라** —
아키텍처 §3 규칙 7 에 올렸다. 새로 만든 파라미터가 **실제로 먹는지 curl 로 확인**해라(값을 바꾸면 결과가 바뀌어야 한다).

## 5. allowed_paths — 이 밖은 건드리지 마라

- `app/back/` — 전부

**`app/front/` 을 건드리지 마라**(FE 워커가 같은 워크트리에서 칩을 붙이는 중이다). 문서 레포도 **읽기 전용**이다.
**마이그레이션·모델은 건드릴 일이 없다** — 읽기 경로만 바뀐다. **커밋·push·PR 하지 마라.**

## 6. 검증

```
cd app/back && pytest tests/test_task_children.py tests/test_task.py
```

**curl 로 실물 확인** — 아래 전부를 수치로 보고에 적어라:

1. `scope` 없이 → 기존과 같은 결과(기본이 `project` 인데 기준이 없으면 `all` 과 같다)
2. `excludeId=<프로젝트 있는 업무>` + `scope=project` → **같은 프로젝트만** 남는지
3. 같은 `excludeId` + `scope=all` → **더 많이** 나오는지 (2 와 건수가 달라야 한다)
4. `scope=recent30` → 30일 넘은 업무가 빠지는지
5. `excludeId=<무소속 업무>` + `scope=project` → **빈 목록이 아니라** `all` 과 같은지
6. `scope=bogus` → **422**
7. `total` 이 20 초과 상황에서 `items.length`(20)와 **다른지** — 후보를 21건 이상 만들어 확인해라
8. 세션 없이 **401**

**7 번을 위해 dev DB 에 업무를 더 만들어도 된다** — 기존 행은 지우지 마라(FE 워커가 보고 있다).

계층 자기점검도 지난번처럼 붙여라 — `except Exception` 0 · service 의 fastapi/schemas/models import 0 ·
router 의 models/repository import 0 · repository 의 ORM 반환 0 · `commit()` 0.

- 통과할 때까지 고친다. 못 고치면 이유와 함께 보고한다.
- 기존에 이미 깨져 있던 무관한 실패는 "무관"으로 분리해 보고한다.

## 7. 완료 보고 — **문구 변경 금지**

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
