# [reviewer] 1단계 최종 재검수 — v3 지적 수정 + 마지막 반영

너는 v3 를 검수한 reviewer 다(read-only). 워크트리 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온`.
- v3 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/review-step1-v3-report.md` 지적(R1~R3 · G1 · G2 · F1~F8 · 사용자 판단으로 넘어간 것)이 닫혔는지
- 마지막 반영: `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/_RESUME.md` §2 10-28 마지막 두 행(코디 판단 · 사용자 추천대로) · `step1-domestic7.json` · 45행 처리(유통 확인 → 허가 대상 아님 유지 + license_basis + 추천 / 없으면 확인 불가 + 원천 질문)
- v3 와 같은 전수 규칙 검사(수출용 연결 0 · 상태 6종 ↔ recommendable · 합침/빠짐 active=false · 이름 · 업체) + 결정에 없는 변경(회귀)
- 산출 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/review-step1-v4-report.md` · 맨 위 PASS/FAIL

## 완료 보고 — 문구 변경 금지

```bash
orca orchestration send \
  --to term_230b7660-9039-4f63-9c96-f8e68bde732b --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "reviewer 완료: 1단계 최종 재검수 <판정>" \
  --body "v3 지적 닫힘 N/N / 새 지적 N / 회귀 N"

orca terminal send --terminal term_230b7660-9039-4f63-9c96-f8e68bde732b \
  --text "[worker_done] reviewer 완료 — 1단계 최종 재검수 <판정>. 상세는 인박스." --enter
```
