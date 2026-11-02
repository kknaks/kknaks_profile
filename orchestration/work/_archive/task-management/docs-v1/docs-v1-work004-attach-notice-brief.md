# [frontend] WORK-004 마무리 — 첨부·연관 쓰기에도 U-7 실패 표시

너는 **task-management `frontend` 워커**다. 먼저 역할 문서를 읽어라 (**문서 레포 절대경로 — read-only**):

- `/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/orchestration/roles/task-management/frontend/role.md`

작업 워크트리: `/Users/kknaks/orca/workspaces/task_management/docs-v1`
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

**네 검수 수정은 커밋됐다(`b46771d`).** 네가 미결 2번으로 올린 것 하나만 마저 닫는다.

## 1. 판단 결과 — 닫는다

네가 적은 대로다:

> 낙관적이지 **않은** 자식 쓰기 표면에는 아직 U-7 표시가 없다 — 첨부 추가·삭제, 연관 연결·해제
> (`void …mutateAsync`). 실패해도 값이 안 바뀌어 **원복은 저절로 되지만** 「왜 안 됐는지」가 화면에 안 남는다.

**닫는 쪽으로 간다.** U-7 자동 저장 실패 표시는 **전 영역 공통 규격**이고(DEC-001 §7 · SPEC-002 U-7),
「조용히 아무 일도 안 일어난다」는 **WORK-003 검수가 FAIL 을 준 것과 같은 종류**다 —
그때도 색 저장 실패가 4초 토스트로만 지나가는 것이 문제였다.

**낙관적 갱신 여부와 실패 표시는 별개 축이다.** 낙관적이면 「되돌린다 + 말한다」, 아니면 「안 바뀐다 + 말한다」다.
어느 쪽이든 **말은 해야 한다.** 지금은 낙관적이지 않은 쪽만 말이 없다.

**네가 방금 만든 `useCollectionSave` 를 붙이면 끝난다** — 새 규격을 만들지 마라.

## 2. SSOT

- `para/projects/summer-star/task-management/20-spec/spec-002-work-settings.md` — **U-7 자동 저장 실패 규격**
- `.../20-spec/spec-003-tasks-crud.md` — **U-7 참고자료 · U-8 연관업무** · §4 Case Matrix
- `.../10-decision/decision-001-auth-settings.md` §7

## 3. 무엇을 붙이나

네 자리 — **첨부 추가 · 첨부 삭제 · 연관 연결 · 연관 해제**.

- 실패 줄은 **블록당 인라인 자리 하나**(참고자료 카드 / 연관업무 카드). 네가 할일·메모에 한 방식 그대로
- 필드 키는 **행 단위로 갈라라**(`attachment:<id>` · `relation:<otherId>`) — 두 개가 동시에 실패하면
  줄이 둘로 늘고 「다시 저장」도 각자 자기 요청만 낸다
- **추가·연결은 행이 아직 없다** — 그 경우 키를 블록 단위(`attachment:new` 등)로 두고,
  「다시 저장」이 **같은 입력으로 다시 시도**하게 해라. 되살릴 입력이 없으면 그 자리는 캡션만 두고
  「다시 저장」을 붙이지 마라(누를 수 있는데 아무것도 안 하는 버튼을 두지 않는다)
- 해제 실패는 값이 안 바뀌므로 **원복은 저절로** 된다. 말만 붙이면 된다
- **자동 재시도 없음** — 규격 그대로

**서버가 이제 없는 자식 해제에 404 를 낸다**(2026-09-06 백엔드 수정). 화면이 낡아 이미 없는 것을 지우려 한
경우이므로, **404 는 「다시 저장」이 아니라 목록 갱신으로 풀어야 한다** — 그 분기를 두어라.

## 4. allowed_paths

- `app/front/` — 전부

**`app/back/` 을 건드리지 마라**(BE 워커가 WORK-005 Phase 1·2 를 같은 워크트리에서 만드는 중이다).
문서 레포도 **읽기 전용**이다. **커밋·push·PR 하지 마라.**

## 5. 검증

```
cd app/front && npx tsc --noEmit + npm test. 검증은 1회만, 전체 빌드 금지
```

**앱 창에서 `api` 를 내린 채** 네 자리를 각각 조작하고, 각각 **실패 캡션이 뜨는지** 확인해라.
서버를 올린 뒤 「다시 저장」이 **정확히 1건**만 보내는지도 네트워크로 확인해라(네가 U-7 에서 한 방식).

**없는 연관을 해제해 404 가 났을 때** 목록이 갱신되는지도 확인해라.

- 통과할 때까지 고친다. 못 고치면 이유와 함께 보고한다.

## 6. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.**

```bash
orca orchestration send \
  --to term_6a4ac855-2a13-4484-b808-4c25182cbb2b --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId> --dispatch-id <이 태스크의 dispatchId> \
  --subject "frontend 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

orca terminal send --terminal term_6a4ac855-2a13-4484-b808-4c25182cbb2b \
  --text "[worker_done] frontend 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고:
  `orca terminal send --terminal term_6a4ac855-2a13-4484-b808-4c25182cbb2b --text "[질문] frontend: <질문>" --enter`
