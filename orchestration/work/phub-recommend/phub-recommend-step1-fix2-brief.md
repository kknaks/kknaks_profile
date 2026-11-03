# [researcher] 1단계 재검수 잔여 정리

`/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/review-step1-v2-report.md` 의 남은 것만 고친다(`step1-products.json` · `.md` · `step1-decisions.json` · `.md`):
1. **R-1** 연결을 해제한 허가 5건이 `5_spec.license`(규격)에 남아 있다(릴리이드M · 레티젠 · 미라콜 · 비타란 22-99) — 규격에서도 뺀다
2. **R-2** 비타란 제조사 근거에 22-99 가 남아 있다 — 정리
3. **W-1** 아큐탄 · 컨트라투벡스 · 라엔넥을 결정 목록에 넣는다(성격에 맞는 묶음 또는 새 묶음, 질문 한 줄)
4. **D29** 레티보(= 보툴렉스 수출명)에 「보툴렉스와 같은 제품으로 합친다」 선택지 추가
다른 건 건드리지 않는다.

## 완료 보고 — 문구 변경 금지

```bash
orca orchestration send \
  --to term_230b7660-9039-4f63-9c96-f8e68bde732b --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "researcher 완료: 1단계 잔여 정리" \
  --body "1~4 처리 / 결정 묶음 수"

orca terminal send --terminal term_230b7660-9039-4f63-9c96-f8e68bde732b \
  --text "[worker_done] researcher 완료 — 1단계 잔여 정리. 상세는 인박스." --enter
```
