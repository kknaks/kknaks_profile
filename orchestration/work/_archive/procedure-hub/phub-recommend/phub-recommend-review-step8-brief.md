# [reviewer] 실버 8단계(관계 · 확인 조건 · 안전 · 근거) 짧은 검수 — 지금 원천 기준만

read-only · 산출 리포트 1개. 워크트리 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온`. 역할 `orchestration/roles/procedure-hub/reviewer/role.md`.
- 기준: `_RESUME.md` §2 2026-10-29 「8단계 조사 반영」(G1~G14 · U8-1 (나) 게이트 없음 · U8-2 (가) 피함 엣지 · 간격 낱말 사전 · 숫자 칸만 읽음) · 「게이트 → 규칙」 · 지시 `phub-recommend-step8-apply-brief.md` · 조사 `step8-research.md`
- 볼 것(전수 · 짧게): ① 간격 — 원문 간격 낱말 있는 주장 전부가 days · first · same_day 또는 사전 표시를 갖는지 · 사전 갈래가 원문과 맞는지(표본 아닌 전수 grep) ② 끝점 — 7단계 지금 산출(J10 피부결 · J14 잇몸미소 · P1-1 · P1-5 · P2-2/3)과 어긋남 0 · 계열/단위 시술 해석이 5단계 정본 키에 있는지 ③ 게이트 — unconfirmed · manual_map 행별 결정이 남지 않았는지(U8-1) ④ 피함 엣지 — 고민 노드가 7단계 노드인지 · 원문 근거 ⑤ 충돌 — 자동으로 고른 것 0 · 전부 보존 ⑥ 조건 · 합병증 · site_caution · 근거 셈이 원천과 맞는지(조사 → 반영 셈 차이 research_diff 이유) ⑦ 원천 질문 16 — 규칙으로 닫을 수 있는데 질문으로 남긴 것 ⑧ open 0 · 결정론(scratch 사본 cmp) · 고정 시험 · 스킬 점검 8종(`reference/2026-10-27-skills-procedure-hub/*/scripts/check_*.py`) · 1~7단계 산출 · 원천 · DEC 수정 없음
- **가상 문장 · 미래 원천은 보지 않는다.** 지적은 지금 데이터에 실제로 있는 것만
- 산출 `orchestration/work/phub-recommend/review-step8-report.md` · 맨 위 PASS/FAIL + 「open = N」

## 완료 보고 — 문구 변경 금지
```bash
orca orchestration send --to term_15f07066-c2d1-4037-a5d1-d09830057ddb --from term_ca3bba94-1c09-43f1-83c7-ff96cc5a0779 --type worker_done \
  --task-id <taskId> --dispatch-id <dispatchId> \
  --subject "reviewer 완료: 실버 8단계 검수" --body "PASS|FAIL · FAIL N · WARN N · open N"
orca terminal send --terminal term_15f07066-c2d1-4037-a5d1-d09830057ddb --text "[worker_done] reviewer 완료 — 실버 8단계 검수. 상세는 인박스." --enter
```
