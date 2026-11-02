# [frontend] WORK-008 Phase 3b — 검수 FAIL 재수정 (fix1)

너는 Phase 3b 를 구현한 **strong-hajin `frontend` 워커**다. 같은 워크트리·같은 규칙(`strong-hajin-polish-fe-p3b-brief.md`). `frontend/` 만 — ⚠ backend 워커가 동시에 `backend/` 에 채팅 뷰 `created_at` 한 줄을 더한다(아래 4).

검수 리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱하진-고도화/orchestration/work/strong-hajin-polish/review-fe-p3b-report.md` — FAIL 1 · WARN 5.

## 고칠 것
1. **FAIL-1 (P-1)** 「수정」 창의 등록이 초안의 `reference_task_ids` 를 잃는다. 리포트 권장대로: 참고 목록이 오기 전·조회 실패·목록에 없는 id 모두 **초안 값을 보존**(목록에 없는 id 는 draft 에 그대로 싣고, 표에는 「읽을 수 없는 업무」 등으로). 테스트: getTasks 보류/실패 상태에서 [등록] → draft 의 reference_task_ids = 초안 값. **같은 「비동기로 채워지는 칸」이 다른 필드에도 없는지 다시 전부 센다**
2. **WARN-1 (코디 결정: 되살린다)** 두 kind 에서 확인 전 자료를 붙이던 입구가 사라진 것은 기존 기능 회귀다. 「수정」 창의 자료 탭(axDraft 모드)에서 기존 AX 자료 초안 API(`stageActionMaterialFile` · `stageActionMaterialLink`, 지우기 포함)로 링크·파일을 붙이고, 그 초안 id 가 등록(confirm)에 실리게 한다. 예전 `ActionTaskCard` 첨부 피커와 같은 규칙. 카드의 자료 페이지 요약 숫자도 갱신
3. **WARN-2 (코디 결정)** 기본 정보 페이지가 96px 에 안 들어가 결재자·참조자가 잘린다 → 카드 본문 고정 높이를 **기본 정보 최대 6줄이 다 들어가는 높이**로 올린다(모든 페이지 같은 높이 — 고정은 유지). 참조자·결재자가 길면 한 줄 말줄임
4. **WARN-3** 채팅 카드 「만든 지 며칠」 — backend 워커가 채팅 뷰의 action 에 `created_at`(ISO) 을 더한다. `viewModels` 의 `ActionItem` 에 선택 필드로 받아 채팅 카드에도 표시(없으면 지금처럼 숨김)
5. **WARN-4** 결재자 후보에 편집 계약 `approver_id.options` 를 합친다(중복 제거) — 초안 결재자가 이름 없이 서지 않게
6. **WARN-5** 확인만: Phase 2 fix2(커밋 `1ef8db0`)에서 잠금 해제가 reload 성공 지점으로 옮겨졌다. AxDraftModal 의 `locked` 가 그 플래그를 쓰면 이미 닫혔다 — 확인하고 보고

## 하지 말 것 / 검증
- 위 밖 금지. 커밋·push·서버·브라우저 금지(코디 스택이 떠 있다)
- 직렬 vitest(바뀐 파일 + 마지막 전체 1회) · `npx tsc --noEmit` · `make frontend-build`

## 완료 보고 — **문구 변경 금지**
> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.**
```bash
orca orchestration send \
  --to term_7941dbc9-8078-4818-8d3d-bfd5545cce31 --from <네 워커handle> \
  --type worker_done \
  --task-id <dispatch context 의 taskId> --dispatch-id <dispatch context 의 dispatchId> \
  --subject "frontend 완료: WORK-008 Phase 3b fix1" \
  --body "FAIL-1·WARN 1~5 처리(파일:줄) / 비동기 칸 전수 / 테스트·tsc·build"
orca terminal send --terminal term_7941dbc9-8078-4818-8d3d-bfd5545cce31 \
  --text "[worker_done] frontend 완료 — Phase 3b fix1. 상세는 인박스." --enter
```
