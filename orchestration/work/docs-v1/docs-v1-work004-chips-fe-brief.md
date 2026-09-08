
# [frontend] WORK-004 마무리 — U-8 필터 칩 3 · 카운트 「n건 중 m」

너는 **task-management `frontend` 워커**다. 먼저 역할 문서를 읽어라 (**문서 레포 절대경로 — read-only**):

- `/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/orchestration/roles/task-management/frontend/role.md`

작업 워크트리: `/Users/kknaks/orca/workspaces/task_management/docs-v1`
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

**네 Phase 4~6 은 커밋됐다(`7550e1b`).** 네가 「코디 판단 필요」로 남긴 **필터 칩 3** 만 마저 붙인다.

## 1. 판단 결과 — 계약을 늘렸다

네 보고가 맞다. 칩(「이 프로젝트」/「최근 30일」/「전체」)은 **필터**인데 표면에는 `projectId`·`dueDate`
**정렬 힌트만** 있었다 — 그대로 붙였으면 칩을 눌러도 같은 목록이 세 번 나왔을 것이다.
카운트 「n건 중 m」의 `n` 도 응답에 없었다. **칩을 빼는 게 아니라 서버에 대응물을 만들었다.**

**SPEC-003 §4·§U-8 을 갱신했다(2026-09-06).** 백엔드 워커가 **지금 같은 워크트리에서** 구현 중이다.

## 2. SSOT — 먼저 읽을 것

- `para/projects/summer-star/task-management/20-spec/spec-003-tasks-crud.md`
  - **§U-8** — 칩·카운트·결과 행·빈 결과 문구
  - **§4 의 `GET /api/tasks/relations/candidates` 절** — `scope` 표와 `total` 규칙
- `.../40-architecture/frontend/README.md` — §6-2(오버레이) · §11(테스트)

## 3. 무엇을 붙이나

### (1) 칩 3 ↔ `scope` 1:1

| 칩 | `scope` |
|---|---|
| 「이 프로젝트」(기본 선택) | `project` |
| 「최근 30일」 | `recent30` |
| 「전체」 | `all` |

### (2) 기준 프로젝트가 없을 때

**무소속 업무이거나 생성 드로어에서 프로젝트를 아직 안 골랐을 때 「이 프로젝트」 칩은 비활성이고
기본 선택이 「전체」로 내려간다.** (서버도 그 경우 `project` 를 `all` 처럼 답하지만, **화면이 먼저 정직해야 한다** —
누를 수 있는데 아무 효과 없는 칩을 두지 마라.)

생성 드로어는 **폼의 프로젝트 값이 바뀌면** 이 판정도 따라 바뀐다.

### (3) 카운트 「n건 중 m」

`n` = 응답 `total`(scope 적용 후 총계) · `m` = `items.length`. **`total` 을 `items.length` 로 대신하지 마라** —
20건을 넘으면 갈리고, 그게 이 카운트가 있는 이유다.

### (4) 빈 결과

칩을 바꿔 결과가 0건이면 §U-8 의 「검색 결과가 없습니다」 + 「다른 검색어나 필터를 써 보세요」. 이미 있는 자리면 재사용해라.

## 4. 서버가 아직 없을 수 있다

백엔드가 **병렬로** 만드는 중이다. 먼저 붙으면 실물로, 아직이면 **MSW 로** 만들고 붙는 대로 실물 확인해라.
**`app/back/` 을 건드리지 마라** — 없다고 네가 만들지 마라.

## 5. allowed_paths — 이 밖은 건드리지 마라

- `app/front/` — 전부

**`app/back/` 을 건드리지 마라**(BE 워커가 같은 워크트리에서 작업 중이다). 문서 레포도 **읽기 전용**이다.
**커밋·push·PR 하지 마라.**

## 6. 검증

```
cd app/front && npx tsc --noEmit (네가 만진 파일 0 에러) + npm test. 정적 빌드 제약 자기점검 — 동적 세그먼트 0 · 모든 page 에 'use client' · 컴포넌트 hex 리터럴 0 · Sheet 직접 import 0 · 폭 리터럴 0. 전체 빌드 금지, 검증은 1회만
```

**앱 창에서 실물로 확인하고 수치를 보고해라:**

1. 상세 드로어의 「업무 연결」 → 칩 3 이 보이고 **「이 프로젝트」가 기본 선택**인지
2. 칩을 바꾸면 **목록이 실제로 달라지는지**(세 칩의 건수를 각각 적어라 — 같으면 안 붙은 것이다)
3. 카운트가 `total` 을 따라가는지 — **후보 21건 이상** 상황에서 `n ≠ m` 인지
4. **무소속 업무**의 상세에서 「이 프로젝트」가 **비활성**이고 기본이 **「전체」**인지
5. 생성 드로어에서 **프로젝트를 고르면** 「이 프로젝트」가 활성으로 바뀌는지
6. 칩 전환으로 0건이 되면 빈 결과 문구가 뜨는지

**3·4 를 위해 dev DB 에 업무를 더 만들어도 된다** — 기존 행은 지우지 마라.

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
  --subject "frontend 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_6a4ac855-2a13-4484-b808-4c25182cbb2b \
  --text "[worker_done] frontend 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_6a4ac855-2a13-4484-b808-4c25182cbb2b --text "[질문] frontend: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
