# [reviewer] 실버 5단계 재검수 v2 — v1 지적 수정분 · 지금 원천 기준만

read-only · 산출 리포트 1개. 워크트리 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온`. 역할 `orchestration/roles/procedure-hub/reviewer/role.md`. (맥락이 없으면 `review-step5-report.md` 부터 읽어라)
- 기준: `orchestration/work/phub-recommend/review-step5-report.md` F1 · W1 · W2 · 결정 `_RESUME.md` §2 2026-10-29 「5단계 검수 FAIL 1 · WARN 2 처리」 행 · 지시 `phub-recommend-step5-fix2-brief.md` · `-fix3-brief.md`(F1 을 기법이 갈리는 계열 전부에 · 계열 기법 하나면 계열 기본 = 근거 · AAPE 도포 · 노바스템 주입 출처 · 미라셀 예외 · 브이빔 PDL · ASCE+ 엑소좀 도포)
- 볼 것: 제품 → 단위 시술 상속 전수(1203쌍)에서 기법 안 맞는 쌍 0 인지 독립 대조 · 추천 가능 제품 중 단위 시술 0 = 진단 장비 2 + 미라셀(예외 · 원천 질문) 뿐인지 · 새 키 5(U5-139 ~ 143) · W2 · PIH 「쓰는 제품에서」 문구 · open 0 · 결정론 · 회귀(v1 PASS 항목 — 원장 521 · 시술 전부 단위 시술 · 앞 단계 정본)
- **가상 문장 · 미래 원천은 보지 않는다.** 지적은 지금 데이터에 실제로 있는 것만
- 산출 `orchestration/work/phub-recommend/review-step5-v2-report.md` · 맨 위 PASS/FAIL + 「open = N」

## 완료 보고 — 문구 변경 금지

```bash
orca orchestration send \
  --to term_15f07066-c2d1-4037-a5d1-d09830057ddb --from term_c2ab8181-2cce-47df-98ec-3002575b6ff0 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "reviewer 완료: 실버 5단계 재검수 v2 <판정>" \
  --body "open N / FAIL N / WARN N / v1 지적 닫힘 N/3"

orca terminal send --terminal term_15f07066-c2d1-4037-a5d1-d09830057ddb \
  --text "[worker_done] reviewer 완료 — 실버 5단계 재검수 v2 <판정>. 상세는 인박스." --enter
```
