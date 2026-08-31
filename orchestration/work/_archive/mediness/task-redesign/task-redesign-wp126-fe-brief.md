
# [frontend] WP-126 P6 — 죽은 incident BFF 3건 삭제 (소형)

너는 **mediness `frontend` 워커**다. 역할 문서: `/Users/kknaks/orca/workspaces/kknaks_profile/task/orchestration/roles/mediness/frontend/role.md` (+ 같은 폴더)

작업 워크트리: `/Users/kknaks/orca/workspaces/mediness-app/task-redesign` (브랜치 `task-redesign` — WP-125 착지 위)
⚠ BE 워커가 `back/`·`mcp/` 에서 병렬 작업 중 — 너는 `front/` 만.

## 할 것 (WP-126 P6 의 front 몫)

1. 죽은 BFF 라우트 3건 삭제 — 호출자 0·BE 404 어서션 테스트 존재 확인됨:
   - `front/app/api/ax/incidents/[run_id]/review/revise/route.ts`
   - `front/app/api/ax/incidents/[run_id]/review/publish/route.ts`
   - `front/app/api/ax/incidents/[run_id]/review/finalize-request/route.ts`
2. 삭제 전 grep 으로 호출자 0 재확인 (있으면 삭제하지 말고 §완료 보고에 질문)
3. 그 외 front 파일 수정 금지

## 검증

```
cd front && npx tsc --noEmit (0 에러) — 삭제만이라 prettier 대상 없음. 검증 1회만
```

## 완료 보고 — 문구 변경 금지

> ⚠ 핸들은 dispatch preamble 값을 믿어라. **커밋·push·PR 금지.**

```bash
orca orchestration send \
  --to term_1d6e5d93-2be9-4125-b7eb-42b1de52b5ed --from term_73dc264f-54bb-40f1-9119-9cb6a01ef902 \
  --type worker_done \
  --task-id <dispatch preamble 의 taskId> \
  --dispatch-id <dispatch preamble 의 dispatchId> \
  --subject "frontend(WP-126 P6) 완료: <한 줄>" \
  --body "삭제 파일 / 호출자 grep 결과 / tsc 결과"

orca terminal send --terminal term_1d6e5d93-2be9-4125-b7eb-42b1de52b5ed \
  --text "[worker_done] frontend(WP-126 P6) 완료 — <한 줄>. 상세는 인박스." --enter
```
