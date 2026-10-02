# [frontend] WORK-008 Phase 2 — 검수 FAIL 재수정 (fix1)

너는 Phase 2 를 구현한 **strong-hajin `frontend` 워커**다. 같은 워크트리에서 이어서 고친다. 규칙은 `strong-hajin-polish-fe-p2-brief.md` 와 같다(⚠ backend 워커가 `backend/` 에서 작업 중 — `frontend/` 만).

검수 리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱하진-고도화/orchestration/work/strong-hajin-polish/review-fe-p2-report.md` — FAIL 1 · WARN 5.

## 고칠 것

1. **FAIL-1 (필수)** 주인이 바뀐 뒤 도착한 옛 주인의 응답이 새 주인 기억에 들어가는 경쟁. 리포트 권장대로 **세대 토큰** — 기억을 쓰는 모든 경로(`rememberScreenValue`·`useRemembered` setter)가 「요청을 시작한 세대 = 지금 세대」일 때만 기억한다. 확인된 자리(CalendarPage reload·DailyReportPage·MyWork/MeetingList/Project/Today reload)뿐 아니라 **기억을 쓰는 곳 전부**를 grep 으로 센다. 보류 응답 테스트(A 요청 보류 → 로그아웃 → B 로그인 → A 응답 도착 → B 화면·기억에 A 값 없음)
2. **WARN-1 (코디 결정: 고친다)** 기억해 둔 envelope 로는 **명령을 열지 않는다** — 받아 둔 값으로 그린 판단·명령 단추(홈 판단 카드 등 action item 명령)는 그 화면의 갱신 응답이 도착할 때까지 비활성. 근거: WP Phase 2 「권한(envelope) 판단은 갱신된 응답 기준」
3. **WARN-2 (고친다)** 재진입 테스트를 적용 화면 **7개 전부**에 하나씩 — 주인이 있는(App 경로와 같은) 조건으로
4. **WARN-3 (고친다)** 키가 무한히 쌓이는 캘린더·조직·보고 — 화면(접두사)별 최근 N개(예: 20)만 남긴다
5. **WARN-4 (고친다)** 업무 화면의 actionItems 도 기억 — 재진입 때 판단 행이 늦게 끼어들지 않게
6. **WARN-5 (간단하면)** 보고 running 상태 복원이 잠깐 비치는 것 — 단순히 막을 수 있으면 막고, 아니면 이유를 보고

## 하지 말 것
- 위 밖 금지. 커밋·push 금지. 서버·브라우저 금지(코디 로컬 스택 8001·5176 이 떠 있다)
- 테스트 직렬(`npx vitest run --no-file-parallelism`). 바뀐 파일 위주 + 마지막 전체 1회. `npx tsc --noEmit` · `make frontend-build`

## 완료 보고 — **문구 변경 금지**
> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.**
```bash
orca orchestration send \
  --to term_7941dbc9-8078-4818-8d3d-bfd5545cce31 --from <네 워커handle> \
  --type worker_done \
  --task-id <dispatch context 의 taskId> --dispatch-id <dispatch context 의 dispatchId> \
  --subject "frontend 완료: WORK-008 Phase 2 fix1" \
  --body "FAIL-1·WARN 1~5 처리(파일:줄) / 기억 쓰는 곳 전수 개수 / 테스트·tsc·build"
orca terminal send --terminal term_7941dbc9-8078-4818-8d3d-bfd5545cce31 \
  --text "[worker_done] frontend 완료 — Phase 2 fix1. 상세는 인박스." --enter
```
