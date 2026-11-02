# [frontend] origin/main 머지 충돌 해소 — frontend/ 10개

너는 **sc-ax frontend 워커**다. 세션 그대로. 워크트리 `/Users/kknaks/orca/workspaces/ax-workspace/sc-meeting`. **코디가 `git merge --no-ff --no-commit origin/main` 을 걸어 둔 상태다(MERGE_HEAD 있음).** 커밋·push·`git merge --abort`·`git reset` **절대 금지** — 충돌 파일을 풀고 `git add <파일>` 까지만. BE 워커가 같은 트리에서 `backend/`·Makefile 을 병렬로 푼다 — 거기 건드리지 마라. vitest 금지(사용자 지시) — `npx tsc --noEmit` 만(BE 쪽 미해결과 무관하게 frontend 는 독립).

## main 에 들어온 것
- #3 「SCAX 채팅창 인터랙션 고도화」 · #8 「프로젝트 참여 이력 보존」. `git log --oneline HEAD..MERGE_HEAD` · `git diff HEAD...MERGE_HEAD -- <파일>` 로 그쪽 의도를 읽어라.

## 네 몫
App.tsx · DateField.tsx · DateField.test.tsx · MeetingDrawer.tsx · MeetingDrawer.test.tsx · WorkModals.tsx · api.ts · chat/ResourcePeek.tsx · styles.css · viewModels.ts

## 원칙
- **둘 다 살린다.** 우리 쪽(HEAD)은 회의·미팅노트 전체(회의 목록/상세, DS 부품 DateField·Popover·TimeChip 등, WorkModals 의 드로어 규칙)이고 main 쪽은 채팅 인터랙션·프로젝트 이력이다. 같은 파일에 양쪽이 더한 것은 둘 다.
- **MeetingDrawer.tsx·MeetingDrawer.test.tsx 는 우리가 지운 파일이다(회의 상세 페이지로 대체, WP-006).** main 이 손댔어도 **삭제를 유지**(`git rm`)하고, main 이 그것을 참조하는 자리(App.tsx·chat/ResourcePeek.tsx 등)는 회의 상세 경로(`/meetings/{id}`)로 바꾼다. 어디를 바꿨는지 보고에.
- DateField 는 우리 최신(DatePicker 하나, OS 달력 없음)이 정본 — main 쪽 변경은 그 위에 얹는다.
- 충돌 마커 0 · `npx tsc --noEmit` 0.

## 완료 보고 — **문구 변경 금지**
```bash
orca orchestration send \
  --to term_828dfb7e-5785-487c-b90c-863c6eaa8261 --from term_1cf6a2f6-1e33-4eee-b180-829175a76d9a \
  --type worker_done --task-id <taskId> --dispatch-id <dispatchId> \
  --subject "frontend 완료: main 머지 충돌 해소(frontend)" \
  --body "푼 파일 / 양쪽 살린 자리·MeetingDrawer 참조 정리 / tsc / 미결"
orca terminal send --terminal term_828dfb7e-5785-487c-b90c-863c6eaa8261 \
  --text "[worker_done] frontend 완료 — main 머지(frontend). 상세는 인박스." --enter
```
