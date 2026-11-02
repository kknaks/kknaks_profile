# [frontend] WORK-010 2루프 E2E-2 — 메타 정보 날짜칸 두 개의 폭이 다르다

같은 frontend 워커. 범위·금지는 E2E-1 지시서(`strong-hajin-polish3-fe-e2e1.md`)와 같다. 미커밋 E2E-1 변경 위에서 고친다.

## 사용자 지적 (2026-10-05)
시작 예정일 날짜칸은 넓고(약 360px) 마감일 날짜칸은 좁다(약 240px) — 「왜 너비가 달라?」

## 코디가 본 원인 (확인하고 맞으면 고쳐라)
- 마감일 `DateField` 는 「마감일 초과」 배지 때문에 `span.meta-info__value` 로 감싸여 내용 폭으로 줄어든다(`WorkModals.tsx` metaDueItem)
- 시작 예정일 `DateField` 는 감싸개 없이 `dd` 직속이라 칸 폭을 따라 늘어난다
- `.scax-td .meta-info .date-field { width:100%; max-width:180px }`(`task-detail.css`)가 실제 DateField 루트 클래스에 걸리지 않는 것으로 보인다 — DateField 가 그리는 실제 루트/입력 클래스를 확인

## 계약
- 메타 정보의 **편집 가능한 날짜칸 둘(시작 예정일·마감일)은 같은 폭** — 같은 감싸개·같은 규칙. 폭은 날짜 `2026/10/13` + 달력 아이콘이 여유 있게 드는 **고정 폭 하나**(값과 근거 보고), 칸이 그보다 좁으면 칸을 따른다
- 「마감일 초과」 배지는 날짜칸 **오른쪽 옆**(줄바꿈 없이, 칸이 좁으면 아래로)
- 시험: 두 날짜칸이 같은 감싸개·클래스를 쓴다(구조 단언)
- 검증: `src/features/work` vitest(기준선 5건) · `npx tsc --noEmit`. 커밋 금지 · 서버 띄우지 마라(5176 HMR)
- 리포트 `fe-e2e-worker-report.md` 에 「E2E-2」 절 추가

## 완료 보고 — 문구 변경 금지
```bash
orca orchestration send --to term_0ad6d618-af6c-4707-b594-389c33e240c1 --from <네 워커handle> --type worker_done \
  --task-id <dispatch context 의 taskId> --dispatch-id <dispatch context 의 dispatchId> \
  --subject "frontend 완료: WORK-010 E2E-2 날짜칸 폭" --body "원인 / 고친 것 / 폭 값 / 검증"
orca terminal send --terminal term_0ad6d618-af6c-4707-b594-389c33e240c1 --text "[worker_done] frontend 완료 — E2E-2 날짜칸 폭. 리포트 fe-e2e-worker-report.md" --enter
```
