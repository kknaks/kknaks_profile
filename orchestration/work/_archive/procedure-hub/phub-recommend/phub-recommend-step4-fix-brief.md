# [researcher] 실버 4단계 검수 WARN 2 수정

`review-step4-report.md` W1 · W2 를 리포트 권고대로. 다른 것은 바꾸지 마라.
1. W1: 셀렉V(`auto-M8-1775364106103`) `pulse_scope: "보조 하위 계열 엔디야그 레이저"`(조사 `step4-research.json:3413`)를 `step4-decisions.json` 에 되살리고 산출에 칸으로
2. W2: `step4-apply.py:372 · :374` md 셈 줄의 고정 숫자를 결정 파일에서 계산하거나 문구 삭제
3. 재실행 · open 0 · 결정론 · 고정 시험

## 완료 보고 — 문구 변경 금지

```bash
orca orchestration send \
  --to term_15f07066-c2d1-4037-a5d1-d09830057ddb --from term_9df45969-2b27-42b6-a3b3-3c63335b19f7 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "researcher 완료: 실버 4단계 WARN 수정" \
  --body "W1 · W2 / open N / 결정론"

orca terminal send --terminal term_15f07066-c2d1-4037-a5d1-d09830057ddb \
  --text "[worker_done] researcher 완료 — 실버 4단계 WARN 수정. 상세는 인박스." --enter
```
