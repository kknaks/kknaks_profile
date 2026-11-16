# [researcher] 실버 3단계 최종 검수 v5 F-1 한 줄 수정 — 코조각주사

`review-step3-v5-report.md` F-1 고칠 값 그대로: 허용 목록에서 「코조각주사」 빼기 · 사전 코 계열에 `코조각주사` · 결정 한 줄(node **코** — 코디 기본값: 고객이 부르는 이름대로, 콧망울은 꼬리표 행이 이미 있음 · kind 부위+다른 축(D-07) · handoff 「조각주사 → 2단계 계열(지방분해 주사)」). 재실행 → 셈 176 · 440 · 노드로 154 · open 0 · 결정론. 다른 것은 바꾸지 마라.

## 완료 보고 — 문구 변경 금지

```bash
orca orchestration send \
  --to term_15f07066-c2d1-4037-a5d1-d09830057ddb --from term_fe6fc75e-8ac3-46d0-a4e3-82410870cc67 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "researcher 완료: 실버 3단계 코조각주사 수정" \
  --body "셈 / open N / 결정론"

orca terminal send --terminal term_15f07066-c2d1-4037-a5d1-d09830057ddb \
  --text "[worker_done] researcher 완료 — 실버 3단계 코조각주사 수정. 상세는 인박스." --enter
```
