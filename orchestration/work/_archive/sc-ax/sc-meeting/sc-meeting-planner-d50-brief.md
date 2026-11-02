# [planner] SPEC-004 0.4.11 — D49 근거 칩 전부 표시(눌리는 칩) · D50 시각 표기는 회의 경과 mm:ss(D31·D34 정정)

너는 **sc-ax planner 워커**다. 세션 그대로. 워크트리 `/Users/kknaks/orca/workspaces/mediness-mediness/sc-meeting-spec`(HEAD 3f5cada4 = 0.4.10). `products/sc-ax/20-spec/spec-004-meeting-note.md` · `10-decision.md` · `30-work/work-006-*.md` 만. 커밋 금지.

## 사용자 결정 (2026-09-11, 실물 3회차)
- **D49**: 줄의 근거 구간(최대 3)을 **전부** 칩으로 낸다(D34 「첫 구간 하나」 정정). 칩은 눌리는 칩 부품(TimeChip), 누르면 스크립트의 그 구간(겹치는 줄)으로. 회의 중·끝난 회의 모두. 같은 시작 시각은 하나로 접음.
- **D50**: 칩·스크립트 시각·메모 시각은 **회의 시작 기준 경과 mm:ss**(60분 넘으면 h:mm:ss). D31 벽시계 표기 철회 — 1분 안에 발화가 많아 HH:MM 으로는 구분이 안 된다. 회의 정보 머리의 날짜·시간 범위는 벽시계 그대로.
- 점프 규칙: 근거 구간과 **겹치는** 스크립트 줄을 켠다(줄 시작이 구간 안일 필요 없음).

## 할 것
§4.2-4(칩) · §5.4(스크립트 시각) · §6(메모 시각) 정정, 10-decision D31·D34 철회 표시 + D49·D50 행, work-006 검증 항목. SPEC 0.4.11 변경 이력 한 줄. 다른 절 손대지 마라.

## 완료 보고 — **문구 변경 금지**
```bash
orca orchestration send \
  --to term_828dfb7e-5785-487c-b90c-863c6eaa8261 --from term_e155b48b-1a1f-4392-99eb-2889228625e7 \
  --type worker_done --task-id <taskId> --dispatch-id <dispatchId> \
  --subject "planner 완료: SPEC 0.4.11 D49·D50" \
  --body "변경 파일 / 요약 / 미결"
orca terminal send --terminal term_828dfb7e-5785-487c-b90c-863c6eaa8261 \
  --text "[worker_done] planner 완료 — 0.4.11. 상세는 인박스." --enter
```
