# [frontend] WORK-008 Phase 1 — 검수 WARN 재수정 (fix1)

너는 Phase 1 을 구현한 **strong-hajin `frontend` 워커**다. 같은 워크트리(`/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-polish`)에서 이어서 고친다. 규칙은 앞 브리프(`…/orchestration/work/strong-hajin-polish/strong-hajin-polish-fe-p1-brief.md`)와 같다.

검수 리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱하진-고도화/orchestration/work/strong-hajin-polish/review-fe-p1-report.md` — 판정 WARN, FAIL 없음.

## 고칠 것 (이것만)

1. **WARN-1** `ProjectPage.test.tsx:427-434` 의 옛 주석을 새 계약(오늘이 보이는 자리)에 맞게 고친다
2. **WARN-2** `ProjectGantt.tsx` 「오늘이 축 밖이면 가장 가까운 끝」 분기 — 이제 도달하지 않는다. 분기를 정리하거나 「F-03 이후 방어용」 주석. 동작 바꾸지 말 것
3. **WARN-3** 담당자 변경 작은 모달의 오류 자리 — 「옮길 담당자를 골라 주세요」는 **대상 칸 아래**, 서버 실패 등 나머지는 지금처럼 모달 안. DS `FieldMessage` 재사용. 테스트 1개로 자리를 잡는다

WARN-4(F-02 테스트 성격)는 고치지 않는다 — 코디가 화면으로 증명한다.

## 하지 말 것
- 위 셋 밖을 고치지 마라. 커밋·push 금지. 서버·브라우저 띄우지 마라(코디가 로컬 스택을 띄워 두었다 — 8001·5176 프로세스를 건드리지 마라)
- 테스트는 **직렬**(`npx vitest run --no-file-parallelism <파일>`)로 바뀐 파일만. 전체 재실행은 하지 않는다. `npx tsc --noEmit` 1회

## 완료 보고 — **문구 변경 금지**
> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.**
```bash
orca orchestration send \
  --to term_7941dbc9-8078-4818-8d3d-bfd5545cce31 --from <네 워커handle> \
  --type worker_done \
  --task-id <dispatch context 의 taskId> --dispatch-id <dispatch context 의 dispatchId> \
  --subject "frontend 완료: WORK-008 Phase 1 fix1" \
  --body "WARN 1~3 처리 파일:줄 / 테스트 결과 / tsc"
orca terminal send --terminal term_7941dbc9-8078-4818-8d3d-bfd5545cce31 \
  --text "[worker_done] frontend 완료 — Phase 1 fix1. 상세는 인박스." --enter
```
