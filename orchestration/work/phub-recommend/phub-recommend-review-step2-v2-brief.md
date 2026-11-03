# [reviewer] 실버 2단계 재검수 — v1 지적 수정 확인

너는 v1 을 검수한 reviewer 다(read-only · 산출 리포트 1개). 워크트리 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온`.
- v1 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/review-step2-report.md` 지적(F1 · F2 · W1~W4)이 닫혔는지
- 수정 지시 `phub-recommend-step2-fix-brief.md`(코디 기본값: M2 원문 확인되면 「성형용 필러」 · M7 「실리프팅」 유지 + name_status 「국내 품목명 있음 · 계열 일부만 해당」 · M8 광원 하위는 원천 · 허가에 적힌 말 그대로 · 약한 행 open)
- 확인: M2 출처 URL(mfds.go.kr/brd/m_550/view.do?seq=200) 실제 제목 · M8 새로 채운 하위 38행 각각 근거가 원천 설명 · 허가 품목에 실제로 있는지(추정 0) · open 34 사유 · 새 PMID 31247326 실재 · v1 과 같은 전수 검사(352 · 셈 · 결정론 · 범위) + 회귀(v1 PASS 였던 것이 바뀌었는지)
- 산출 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/review-step2-v2-report.md` · 맨 위 PASS/FAIL

## 완료 보고 — 문구 변경 금지

```bash
orca orchestration send \
  --to term_15f07066-c2d1-4037-a5d1-d09830057ddb --from term_e935d4d1-c970-4194-b5ff-68be7a928cc5 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "reviewer 완료: 실버 2단계 재검수 <판정>" \
  --body "v1 지적 닫힘 N/N / 새 지적 N / 회귀 N"

orca terminal send --terminal term_15f07066-c2d1-4037-a5d1-d09830057ddb \
  --text "[worker_done] reviewer 완료 — 실버 2단계 재검수 <판정>. 상세는 인박스." --enter
```
