# [frontend] WORK-010 2루프 E2E-1 — 업무 상세 「메타 정보」를 한 줄에 두 항목(2열)으로

같은 frontend 워커다(Phase 1·2a·2b 를 했다). 범위·allowed_paths·하지 말 것은 2b 브리프(`strong-hajin-polish3-fe-p2b-brief.md`) 그대로 — `App.tsx` 다운로드 수신부·`lib/shell.ts`·`src-tauri` 금지. 지금 HEAD = `58e591a`.

## 사용자 지적 (2026-10-05 E2E)
메타 정보가 **한 줄에 항목 하나**(라벨|값)라 세로로 길다 → **한 줄에 두 항목**(라벨·값 × 2). 사용자 「응 그렇게 가자」.

## 계약
- 행 짝(왼쪽 | 오른쪽):
  1. 진행 상태 | 버전
  2. 담당 | 출처 (출처 없으면 오른쪽 칸 비움)
  3. 시작 예정일 | 실제 시작일 (실제 시작일 없으면 오른쪽 칸 비움 — 칸 자리는 유지해 줄이 맞게)
  4. 마감일 | 실제 종료일 (같음)
  5. 결재 · 참조 — 있을 때만 한 줄(둘 다 있으면 짝, 하나면 왼쪽)
  - 읽기 전용에서 빈 행 규칙(SPEC §2.10.2 · 값 없는 읽기 전용 칸은 서지 않음)은 지키되, 짝 안에서 한쪽만 빌 때는 칸만 비운다. 한 줄의 두 칸이 모두 비면 그 줄이 서지 않는다
- 날짜 입력칸(DateField) 폭을 칸 안에 맞게 줄인다(지금 ~360px). 셀렉트·배지·출처 링크가 칸을 넘지 않게(말줄임)
- **좁은 폭**(모달이 좁아질 때 — 기존 반응형 기준 하나를 골라 보고)에서는 지금처럼 한 줄에 하나
- 공용 `.meta-grid`(`components.css:527-534`)는 **다른 사용처가 있으면 건드리지 말고** 업무 상세 스코프(`task-detail.css`)에서 4열을 짠다. 사용처를 grep 으로 세어 보고
- 값·저장 동작·순서 외 계약은 그대로(인라인 저장·셀렉트·마감일 초과 배지·출처 「판단 보기」)

## 검증
- 바뀐/새 테스트(짝 배치·빈 칸 규칙·한 줄 둘 다 비면 줄 없음) + 전체 `npx vitest run --no-file-parallelism`(기준선 5건) + `npx tsc --noEmit` + `make frontend-build`
- 커밋·push 금지 · 서버·프론트를 띄우지 마라(코디가 띄워 둔 로컬 스택 5176 이 HMR 로 바로 반영한다 — 건드리지 마라)
- 리포트 `fe-e2e-worker-report.md`(같은 폴더, 새 파일 — 2루프 항목을 이어 적는다)

## 완료 보고 — 문구 변경 금지
```bash
orca orchestration send --to term_0ad6d618-af6c-4707-b594-389c33e240c1 --from <네 워커handle> --type worker_done \
  --task-id <dispatch context 의 taskId> --dispatch-id <dispatch context 의 dispatchId> \
  --subject "frontend 완료: WORK-010 E2E-1 메타 정보 2열" --body "변경 파일 / 짝·빈 칸 규칙 / 반응형 기준 / 기준선 vs 결과"
orca terminal send --terminal term_0ad6d618-af6c-4707-b594-389c33e240c1 --text "[worker_done] frontend 완료 — E2E-1 메타 정보 2열. 리포트 fe-e2e-worker-report.md" --enter
```
