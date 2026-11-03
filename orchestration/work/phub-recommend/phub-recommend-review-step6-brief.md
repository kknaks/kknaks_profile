# [reviewer] 실버 6단계(패키지) 검수 — 짧게 · 지금 원천 기준만

너는 맥락이 없다. read-only · 산출 리포트 1개. 워크트리 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온`. 역할 `orchestration/roles/procedure-hub/reviewer/role.md`.
- 기준: `orchestration/work/phub-recommend/_RESUME.md` §2 2026-10-29 「6단계 패키지 이해」 · 「실버 6단계 시작」 · 「6단계 패키지 조사 반영」 행 · 조사 `step6-research.*` · 지시 `phub-recommend-step6-apply-brief.md`
- 대상: `step6-decisions.json` · `step6-apply.py` · `step6-packages.json` · `.md` · `step6-origin-questions.md` · `step6-source-fix.md` · `step6-fixtures/` · 5단계 보강(포토나4D · 리쥬하이 · 시장가 회차 행 이동)
- 볼 것: 패키지 24 · 묶음 이름 9 이 원천에서 독립적으로 맞는지 · 구성 엣지 49 가 원천 설명(이름 · detail · extracted overview/mechanism)에 실제로 적힌 시술인지 전수(R1 — 적응증은 구성 아님) · 키 매핑(R2) · 슬롯 8 원천 질문 · 시그니처 2 추천 기본 제외 · 회차 3 · 가격 원문(1회 가격과 안 섞임) · same_day_raw 원문 · 5단계 보강 회귀 · open 0 · 결정론 · 단위 시술 스킬 점검 · 8단계 메모(엣지 만들지 않음)
- **가상 문장 · 미래 원천은 보지 않는다.** 지적은 지금 데이터에 실제로 있는 것만
- 산출 `orchestration/work/phub-recommend/review-step6-report.md` · 맨 위 PASS/FAIL + 「open = N」

## 완료 보고 — 문구 변경 금지

```bash
orca orchestration send \
  --to term_15f07066-c2d1-4037-a5d1-d09830057ddb --from term_85e506ba-903a-482a-8e6d-ceeb8f3382bd \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "reviewer 완료: 실버 6단계 검수 <판정>" \
  --body "open N / FAIL N / WARN N"

orca terminal send --terminal term_15f07066-c2d1-4037-a5d1-d09830057ddb \
  --text "[worker_done] reviewer 완료 — 실버 6단계 검수 <판정>. 상세는 인박스." --enter
```
