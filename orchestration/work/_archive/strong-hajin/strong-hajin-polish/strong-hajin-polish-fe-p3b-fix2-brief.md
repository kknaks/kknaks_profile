# [frontend] WORK-008 Phase 3b — 재검수 WARN (fix2)

너는 Phase 3b 를 구현한 **strong-hajin `frontend` 워커**다. 같은 워크트리·같은 규칙. `frontend/` 만(backend 는 다른 워커들 것).
⚠ **코디 핸들이 바뀌었다: `term_d7b4a334-2cbd-42ab-9eab-e64a7b255d44`** — 완료 보고는 이 핸들로.

재검수 리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱하진-고도화/orchestration/work/strong-hajin-polish/review-fe-p3b2-report.md` §N-1 ~ N-3 — 셋 다 고친다(리포트 권장대로). 그 밖은 금지.

검증: 직렬 vitest(바뀐 파일 + 마지막 전체 1회) · `npx tsc --noEmit` · `make frontend-build`. 커밋·서버·브라우저 금지.

## 완료 보고 — **문구 변경 금지**
```bash
orca orchestration send --to term_d7b4a334-2cbd-42ab-9eab-e64a7b255d44 --from <네 워커handle> --type worker_done \
  --task-id <taskId> --dispatch-id <dispatchId> \
  --subject "frontend 완료: WORK-008 Phase 3b fix2" --body "N-1~3 처리(파일:줄) / 테스트·tsc·build"
orca terminal send --terminal term_d7b4a334-2cbd-42ab-9eab-e64a7b255d44 --text "[worker_done] frontend 완료 — Phase 3b fix2. 상세는 인박스." --enter
```
