# [reviewer] WORK-010 Phase 1 코드 검수 — 로그인 문구 · 내보내기 단추 · 회의 제목 인라인

같은 reviewer 다(앞 판 SPEC 검수). 역할 문서 `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화/orchestration/roles/strong-hajin/reviewer/role.md`. **read-only** — 리포트 한 장만.

## 1. 대상
코드 워크트리 `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-polish3` 의 미커밋 diff 중 **Phase 1 파일만**:
```
frontend/src/features/auth/LoginPage.tsx · LoginPage.test.tsx
frontend/src/features/meetings/MeetingDetailPage.tsx · MeetingTitle.test.tsx(신규) · MeetingAfter.test.tsx
frontend/src/lib/labels.ts (회의 제목 관련 키만 — Phase 3 이 다운로드 문구 키를 덧붙일 수 있다, 그건 대상 아님)
frontend/src/ds/InlineText.tsx (IME 가드 — 계약 밖 변경)
```
⚠ 같은 워크트리에서 Phase 3(셸) 워커가 `frontend/src-tauri/`·`lib/shell.ts`·`App.tsx`·`labels.ts`(다운로드 키) 를 동시에 고치고 있다 — **대상 아님.**

## 2. 기준
- WP `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화/para/projects/summer-star/strong-hajin/30-work/work-010-polish3.md` **Phase 1(1-1·1-2·1-3)** — 체크박스가 계약(SPEC 없음, WP 가 정본)
- 워커 보고 `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화/orchestration/work/strong-hajin-polish3/fe-p1-worker-report.md`
- 조사 `fe-survey-report.md` §1·§2·§3 · `be-survey-report.md` §3 · 기준선 `flaky-baseline-evidence.md`

## 3. 볼 것
1. WP 체크박스마다 PASS/FAIL(파일:줄)
2. **InlineText IME 가드**가 다른 사용처(`AgendaBlock.tsx` 2곳)를 깨지 않나 · 계약 밖 변경으로 받아도 되나
3. `saveTitle` — 응답으로 바로 세우는 것·연타 방지·실패 원복·`onMeetingChanged` 로 목록 갱신. 권한(`can_edit_info`) 아닌 상태에서 입력·[적용]이 정말 안 서나
4. 「제목 후보:」 문구 변경이 다른 표면(목록·캘린더·테스트)과 어긋나지 않나
5. **조용히 통과하는 자리** — 빈 단언·개명·폴백
6. **사용자가 실물에서 만날 자리** — 긴 제목 말줄임(`workspace.css:16` nowrap) 등 눈으로 이상해 보일 곳 목록

## 4. 판정
FAIL · WARN · PASS. 각 지적에 `파일:줄` + 근거. 테스트를 돌려도 된다(`frontend` 에서 해당 파일만 `npx vitest run <파일>`) — 서버·프론트는 띄우지 마라.

## 5. allowed_paths
- `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화/orchestration/work/strong-hajin-polish3/review-fe-p1-report.md` 하나

## 6. 완료 보고 — **문구 변경 금지**
```bash
orca orchestration send --to term_0ad6d618-af6c-4707-b594-389c33e240c1 --from <네 워커handle> --type worker_done \
  --task-id <dispatch context 의 taskId> --dispatch-id <dispatch context 의 dispatchId> \
  --subject "reviewer 완료: WORK-010 Phase 1 <PASS|WARN|FAIL>" --body "판정 / FAIL·WARN(파일:줄) / 실물 자리 / 리포트 경로"
orca terminal send --terminal term_0ad6d618-af6c-4707-b594-389c33e240c1 --text "[worker_done] reviewer 완료 — Phase 1 <판정>. 리포트 review-fe-p1-report.md" --enter
```
