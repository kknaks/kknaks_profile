# [frontend] WORK-008 Phase 2 — 재검수 WARN 재수정 (fix2)

너는 Phase 2 를 구현한 **strong-hajin `frontend` 워커**다. 같은 워크트리·같은 규칙(`strong-hajin-polish-fe-p2-brief.md`). `frontend/` 만(backend 변경은 다른 워커 것).

재검수 리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱하진-고도화/orchestration/work/strong-hajin-polish/review-fe-p2b-report.md` §3 — WARN 셋.

## 고칠 것 (이것만)
1. **WARN-A** 갱신 잠금은 진입 effect 뿐 아니라 **그 화면의 어떤 다시 읽기든 성공하면** 풀린다 — 홈·업무·캘린더·보고(프로젝트처럼 `reload` 안에서 풀기). 갱신 실패 뒤 셸 refresh·쓰기 뒤 reload 가 성공하면 풀리는 테스트 1개 이상
2. **WARN-B** `MyWorkPage` 레일 effect 의존 배열에 잠금 값(`listBusy`)
3. **WARN-C (코디 결정: 잠근다)** 조직 화면도 기억한 `org.profile` 의 권한으로 관리 입구(관리 배지·`canManageAccess`·활동 표)를 열지 않는다 — 갱신 응답 전에는 그 입구를 감추거나 비활성. 근거: WP Phase 2 「envelope 는 갱신된 응답 기준」

## 하지 말 것 / 검증
- 위 밖 금지. 커밋·push·서버·브라우저 금지
- 직렬 vitest(바뀐 파일 + 마지막 전체 1회) · `npx tsc --noEmit` · `make frontend-build`

## 완료 보고 — **문구 변경 금지**
> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.**
```bash
orca orchestration send \
  --to term_7941dbc9-8078-4818-8d3d-bfd5545cce31 --from <네 워커handle> \
  --type worker_done \
  --task-id <dispatch context 의 taskId> --dispatch-id <dispatch context 의 dispatchId> \
  --subject "frontend 완료: WORK-008 Phase 2 fix2" \
  --body "WARN A·B·C 처리(파일:줄) / 테스트·tsc·build"
orca terminal send --terminal term_7941dbc9-8078-4818-8d3d-bfd5545cce31 \
  --text "[worker_done] frontend 완료 — Phase 2 fix2. 상세는 인박스." --enter
```
