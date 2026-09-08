# [frontend] WORK-012 검수 수정 — `finalBatchState` 프론트 잔재 4줄 제거

너는 **task-management `frontend` 워커**다. WORK-012 Phase 3 를 네가 구현했고 reviewer 검수가 끝났다(FAIL 0 · WARN 4). 그중 프론트 몫 하나만 닫는다.
역할 문서: `/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/orchestration/roles/task-management/frontend/role.md`

## 0. 어디서

**코드 워크트리** — `/Users/kknaks/orca/workspaces/task_management/docs-v1` (브랜치 `kknaksss/docs-v1`). 미커밋 상태 그대로 위에서 고친다. **백엔드가 방금 `finalBatchState` 를 응답에서 뺐다**(`git diff HEAD -- app/back/schemas/meeting.py`).
**검수 리포트** — `/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/orchestration/work/docs-v1/work012-review-report.md` §3 **W-3** (읽기 전용).

## 1. 고칠 것 — SPEC-008 §7 #3 이 09-07 에 지운 필드
```
src/features/meetings/types.ts:150        finalBatchState 필드 삭제(+ 주석)
src/features/meetings/testUtils.tsx:67    픽스처 키 삭제
src/features/meetings/closeFixtures.ts    픽스처 키 2곳 삭제
```
그 밖 참조는 0건이다(검수 확인). 정적 검사 `static.test.ts` 에 `finalBatchState` 0 을 한 줄 추가한다.

## 2. 하지 마라
- 그 밖의 파일 수정 0. 리팩터 0. `app/back/` 금지.

## 3. 검증
```bash
cd /Users/kknaks/orca/workspaces/task_management/docs-v1/app/front && npx tsc --noEmit && npx vitest run 2>&1 | tail -6   # Errors 0
grep -rn "finalBatchState" src   # static.test.ts 의 needle 한 줄만
```

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.**

- **커밋·push·PR 하지 마라.**

```bash
# (1) 인박스 적재
orca orchestration send \
  --to term_98a33032-2134-4bf9-ac48-e9df737f9b8f --from term_1c173ed7-8c1c-4b28-9b4c-f7817cc54ec8 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "frontend 완료: WORK-012 검수 수정" \
  --body "고친 파일 / tsc · vitest 수치 / grep 확인"

# (2) 직접 주입
orca terminal send --terminal term_98a33032-2134-4bf9-ac48-e9df737f9b8f \
  --text "[worker_done] frontend 완료 — WORK-012 검수 수정. 상세는 인박스." --enter
```

- 막히면 `orca terminal send --terminal term_98a33032-2134-4bf9-ac48-e9df737f9b8f --text "[질문] frontend: <질문>" --enter`
