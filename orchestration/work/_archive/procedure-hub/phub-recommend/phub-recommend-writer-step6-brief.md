# [writer] 실버 6단계(패키지) 과정 기록

너는 맥락이 없다. 역할 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/roles/procedure-hub/writer/role.md`. 워크트리 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온`. 1~5단계 기록(`/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/para/projects/company/procedure-hub/log/` 의 silver-step1~5)과 같은 형식 · 같은 자리: `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/para/projects/company/procedure-hub/log/2026-10-29-silver-step6-package.md` · README 지도 한 줄. 분량은 6단계 크기에 맞게(작게).

## 원천
- 결정 `orchestration/work/phub-recommend/_RESUME.md` §2 2026-10-29 6단계 행 전부(패키지 이해 · 시작 · 조사 반영 · 데이터 끝)
- `step6-research.*` · `step6-decisions.json` · `step6-apply.py` · `step6-packages.*` · `step6-origin-questions.md` · `step6-source-fix.md` · 검수 `review-step6-report.md` · 브리프 `phub-recommend-step6-*-brief.md` · 5단계 보강(포토나4D · 리쥬하이 · 시장가 회차)
- Procedure Hub 화면 코드 `/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-recommend/frontend/src/app/recommend/page.tsx` · `src/components/AppShell.tsx`(사이트의 「추천 패키지」 = problem-combos)

## 담을 것
1. 왜 — 「패키지」라는 말이 둘: 사이트 「추천」 화면의 추천 패키지(problem-combos → 7단계) ↔ 원천 이름 있는 묶음(꿀광토닝 · 3회 패키지 → 6단계)
2. 전후 — 입력 36 → 패키지 24 · 묶음 이름 9 · 단위 시술로 2 · 구성 49 · 슬롯 8 · 같은 것 전/후 5(꿀광토닝 · 포토나4D · 리쥬하이 · 셀리부트 · 스컬트라 3회)
3. 정한 규칙 — 패키지 = 이름 있는 단위 시술 묶음 · 구성은 원천 적힌 만큼(적응증 아님) · 가격 원문 · 같은 날은 원문만 · 시그니처는 추천 기본 제외 · 패키지 → 구성 엣지는 6단계 · 시너지는 8단계(패키지는 「함께 판매 사례」 근거)
4. 과정 · 5. 틀린 것(코디가 「패키지」를 사이트와 다른 뜻으로 써서 사용자 혼동 · 「병원 메뉴 묶음」 표현 · 브랜드 메뉴를 특정 병원으로 의심 → 사용자 「꿀광토닝은 일반적」 · 옛 번호가 문구에 남음) · 6. 남은 것(원천 질문 13 · 8단계 메모 37)
- 실명 · 키 금지 · 수치는 파일에서 다시 셈 · 추정 금지

## 완료 보고 — 문구 변경 금지

```bash
orca orchestration send \
  --to term_15f07066-c2d1-4037-a5d1-d09830057ddb --from term_f086aeca-5681-442a-be1b-becc8a187a9a \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "writer 완료: 6단계 패키지 기록" \
  --body "경로 / 섹션 / 전후 수치"

orca terminal send --terminal term_15f07066-c2d1-4037-a5d1-d09830057ddb \
  --text "[worker_done] writer 완료 — 6단계 패키지 기록. 상세는 인박스." --enter
```
