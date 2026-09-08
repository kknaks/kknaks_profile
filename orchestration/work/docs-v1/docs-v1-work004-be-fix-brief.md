
# [backend] WORK-004 소수정 — 연관업무 후보 검색을 컬렉션 표면으로

너는 **task-management `backend` 워커**다. 역할 문서는 이미 읽었다 —
`/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/orchestration/roles/task-management/backend/role.md`

작업 워크트리: `/Users/kknaks/orca/workspaces/task_management/docs-v1`

**프론트 워커가 같은 워크트리에서 `app/front` 를 동시에 만지고 있다.** 너는 `app/back` 만 건드린다.

## 1. 무엇을 고치나

네가 만든 `GET /api/tasks/{task_id}/relations/candidates` 가 **생성 드로어에서 쓸 수 없다.**
SPEC-003 U-1 은 **생성 드로어에도** 「업무 연결」을 두는데 그 시점엔 **자기 id 가 없다**(없는 id 는 404).

**SPEC-003 §4 를 갱신했다**(커밋 `bfe9da3`) — 그 절을 읽고 그대로 맞춰라.

```
GET /api/tasks/relations/candidates
```

| 파라미터 | 필수 | 뜻 |
|---|---|---|
| `keyword` | ✖ | 제목 검색 |
| `excludeId` | ✖ | **상세 드로어**가 자기 id 를 준다 → 그 업무와 **이미 연결된 것도 함께 제외**. 생성 드로어는 안 보낸다 |
| `projectId` · `dueDate` | ✖ | 정렬 근거. **`excludeId` 가 있으면 서버가 그 업무 값을 쓴다**(쿼리로 온 값보다 우선). 없으면 쿼리 값으로 정렬 |

정렬은 그대로 — **같은 프로젝트 → 기한 ±7일 → 최근 수정**, 최대 20건, 삭제분 제외.

**기존 `/{task_id}/relations/candidates` 는 제거한다.** 표면을 둘로 두면 생성·상세가 다른 코드를 타고
정렬 규칙이 갈린다.

**라우트 순서 주의** — `/{task_id}` 가 `int` 라 `/relations/candidates` 를 **먼저 선언**해야 한다.
안 그러면 `relations` 를 id 로 파싱하려다 422 가 난다. 그 순서가 실제로 맞는지 테스트로 고정하라.

## 2. allowed_paths

- `app/back/` 만. **`app/front` 를 건드리지 마라**(프론트 워커가 동시에 작업 중이다).
- 문서 레포는 읽기 전용. **커밋·push 금지.**

## 3. 검증

```
cd app/back && uv run pytest -q <네가 만들거나 고친 테스트만>. 계층 자기점검(ORM 이 repository 를 넘지 않는가 · schema/dto 혼용 · except Exception). 검증은 1회만
```

- `excludeId` 없이 부르면 **200 이고 후보가 온다**(생성 드로어 경로)
- `excludeId` 를 주면 **자기 자신과 이미 연결된 업무가 빠진다**
- `excludeId` 가 남의 업무·없는 업무면 **404**
- `projectId`·`dueDate` 로 **정렬이 바뀌는가**(같은 프로젝트가 앞으로)
- **옛 경로 `/api/tasks/{id}/relations/candidates` 가 404** 인가
- 세션 없이 **401**

## 4. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.**

- **커밋·push·PR 하지 마라.**
- 끝나면 **아래 두 명령을 모두** 실행한다.

```bash
orca orchestration send \
  --to term_6a4ac855-2a13-4484-b808-4c25182cbb2b --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId> \
  --dispatch-id <이 태스크의 dispatchId> \
  --subject "backend 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

orca terminal send --terminal term_6a4ac855-2a13-4484-b808-4c25182cbb2b \
  --text "[worker_done] backend 완료 — <한 줄 요약>. 상세는 인박스." --enter
```
