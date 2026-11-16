# [writer] 실버 4단계 — DEC-002 예시 한 줄 수정 + 과정 기록

너는 맥락이 없다. 역할 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/roles/procedure-hub/writer/role.md`. 워크트리 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온`.

## 1. DEC-002 예시 한 줄 (사용자 결정 J2)
`/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/step4-source-fix.md` 「DEC 문구 1」 그대로: `DEC-002.md` D-02 예시 「HA 필러 · 코 · 피하 주입」 → 「HA 필러 · 코 · 주입」(층 속성: 콧등 골막상 · 코끝 연골막상). **이 한 줄만** 고친다. 결정 내용 · 다른 문장 금지. 고친 줄 위치와 근거(_RESUME §2 10-28 4단계 반영 행 · 원천 anatomy nose safe_injection_depth)를 문서 이력 표기 방식에 맞게

## 2. 4단계 과정 기록
1~3단계 기록(`/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/para/projects/company/procedure-hub/log/2026-10-28-silver-step1-product-normalization.md` · `-step2-family.md` · `-step3-site.md`)과 같은 형식 · 같은 자리: `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/para/projects/company/procedure-hub/log/2026-10-28-silver-step4-technique.md` · README 지도 한 줄.
- 원천: `_RESUME.md` §2 10-28 4단계 행 전부 · source-map 승인 행 · `step4-research.*` · `step4-decisions.json` · `step4-apply.py` · `step4-techniques.*` · `step4-source-fix.md` · `review-step4-report.md` · 브리프 `phub-recommend-step4-*-brief.md` · 그리고 4단계 앞에 한 **원천 21 행선지 지도**(`source-map.*` — 왜 했나: 물어볼 때마다 자리 없는 원천이 드러남 · 사용자 「모든 json 이 메달리온에 녹아야」)
- 담을 것: 왜 · 전후(초안 큰 기법 65 → 노드 24 · 표현 181 행선지 · 같은 것 전/후 6개: 메조보톡스 · 피코토닝(펄스는 장비 속성) · 코 필러 층(골막상 · 연골막상 — 사용자 질문 「같은 거야?」) · 셀렉V pulse_scope · 표정근 · 무바늘 제트) · 정한 규칙(큰 기법 = 계열 정의 동사 + mechanism 태그 · 세부 = 부위 쪼개기 규칙 · 층 · 근육 = 단위 시술 속성 · 펄스 · 박피 = 장비 속성) · 과정(지도 → 조사 → 결정 → 반영 → 짧은 검수 1판) · 틀린 것(코디가 J2 를 「골막상 주입」 하나로 냈다가 사용자 질문으로 바로잡음 · 단계마다 필요한 파일만 봐서 지도가 늦었던 것) · 남은 것(원천 수정 후보 3 · step3 표정근 빼기 · 5단계로 넘긴 것)
- 실명 · 키 금지 · 수치는 파일에서 다시 셈 · 추정 금지

## 완료 보고 — 문구 변경 금지

```bash
orca orchestration send \
  --to term_15f07066-c2d1-4037-a5d1-d09830057ddb --from term_3a374029-0ae2-4b5a-a4da-f33c2117db3f \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "writer 완료: 4단계 DEC 예시 · 기록" \
  --body "DEC-002 줄 / 기록 경로 / 전후 수치"

orca terminal send --terminal term_15f07066-c2d1-4037-a5d1-d09830057ddb \
  --text "[worker_done] writer 완료 — 4단계 DEC 예시 · 기록. 상세는 인박스." --enter
```
