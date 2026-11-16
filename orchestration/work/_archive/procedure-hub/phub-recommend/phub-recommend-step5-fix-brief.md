# [researcher] 5단계 한 줄 — 줄기세포 관절치료 의료진 질문

결정 `_RESUME.md` §2 2026-10-29 「5단계 반영 확인 3」 행: ①② 지금대로 · ③ 시장가 「줄기세포 관절치료」 = 단위 시술 없음(가격 원문 보관 그대로) + **의료진 질문 1줄**(「줄기세포 관절치료를 Procedure Hub 시술로 다룰지 — 피부 · 미용 시술 범위 밖으로 보아 단위 시술을 세우지 않음」)을 `step5-decisions.json` → `step5-origin-questions.md` 에(의료진 질문 절). `step5-apply.py` 재실행 · open 0 · 결정론 · 고정 시험. 다른 것은 바꾸지 마라.

## 완료 보고 — 문구 변경 금지

```bash
orca orchestration send \
  --to term_15f07066-c2d1-4037-a5d1-d09830057ddb --from term_c8fcd5df-52e7-4163-8f94-9b880113c6a6 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "researcher 완료: 5단계 관절치료 질문" \
  --body "질문 수 / open N / 결정론"

orca terminal send --terminal term_15f07066-c2d1-4037-a5d1-d09830057ddb \
  --text "[worker_done] researcher 완료 — 5단계 관절치료 질문. 상세는 인박스." --enter
```
