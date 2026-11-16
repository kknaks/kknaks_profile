# [reviewer] 실버 7단계(고민 · 목적 · 추천 조합) 검수 + 5단계 보강 — 짧게 · 지금 원천 기준만

너는 맥락이 없다. read-only · 산출 리포트 1개. 워크트리 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온`. 역할 `orchestration/roles/procedure-hub/reviewer/role.md`.
- 기준: `orchestration/work/phub-recommend/_RESUME.md` §2 2026-10-29 「실버 7단계 시작」 · 「7단계 조사 반영」 · 「5단계 보강(J7) G1~G10」 행 · 조사 `step7-research.*` · 지시 `phub-recommend-step7-apply-brief.md` · `-apply2-brief.md`
- 대상: `step7-decisions.json` · `step7-apply.py` · `step7-concerns.json` · `.md` · `step7-origin-questions.md` · `step7-source-fix.md` + 5단계 보강(키 143 → 162) · 2단계(계열 27 · 정의 넓힘 3 · 하위 2) · 4단계(기법 26)
- 볼 것: 고민 노드 55 가 taxonomy problem 에서 결정대로(J1 시술 이름 항목은 노드 아님 · J2 · J3 · J8) · 대응표 249 표본 아니라 **완전 일치 · 동의어 판정 전수 대조**(사람 확인 83 은 게이트 표시 맞는지) · 목적 13 · 엣지 523 이 원천 구조(CC 추천 시술 · problem-combos · 최적화 · modality_ref 등)에 실제로 있는지 전수 · 적응증 문장 유래 엣지 0 · 추천 조합 79 원천별 · 구성 내림 · 영업 문구 기본 제외 · 사이트 용어 · 5단계 보강 19키가 G1~G10 대로 · 새 계열 N8~N10 정의 · PMID 실재 · 수술 표시 · open 0 · 결정론(2 · 4 · 5 · 7) · 스킬 점검 4종 · 8단계 메모는 엣지 안 만듦
- **가상 문장 · 미래 원천은 보지 않는다.** 지적은 지금 데이터에 실제로 있는 것만
- 산출 `orchestration/work/phub-recommend/review-step7-report.md` · 맨 위 PASS/FAIL + 「open = N」

## 완료 보고 — 문구 변경 금지

```bash
orca orchestration send \
  --to term_15f07066-c2d1-4037-a5d1-d09830057ddb --from term_3edd26c3-db5a-4f5d-b572-ea1855280c19 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "reviewer 완료: 실버 7단계 검수 <판정>" \
  --body "open N / FAIL N / WARN N"

orca terminal send --terminal term_15f07066-c2d1-4037-a5d1-d09830057ddb \
  --text "[worker_done] reviewer 완료 — 실버 7단계 검수 <판정>. 상세는 인박스." --enter
```
