# [researcher] 실버 6단계(패키지) 조사 — 이름 있는 단위 시술 묶음 (read-only)

너는 맥락이 없다. 역할 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/roles/procedure-hub/researcher/role.md`. 워크트리 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온`. 원장 · 결정 · 원천 수정 금지. 산출 2파일만.

## 읽을 것
- 결정 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/_RESUME.md` §2 — 특히 2026-10-29 「6단계 패키지 이해」 · 「실버 6단계 시작」 행 · 10-28 source-map 승인(U1 단계 경계) · DEC-002 D-03 · OQ-204
- 단위 시술 정본 `step5-units.json`(키 143 · ledger 의 6단계 18 · market 의 6단계 6 · handoffs) · `step5-decisions.json`
- 원천 `/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-stg-2026-10-26/` taxonomy(패키지 항목 name · detail · extracted) · market-pricing · synergy(대조만)
- 앞 단계 교훈 `para/projects/company/procedure-hub/log/2026-10-29-silver-step5-unit.md` §5 — 지금 원천 기준 · 추정 금지 · 같은 성격 전수 · 가상 문장 시험 없음

## 할 것
A. **패키지 목록**: 원장 18 + 시장가 6 + 5단계 넘김 12 — 겹침 정리 · 패키지마다 종류(일반 패키지 / 회차 묶음 / 경계)
B. **구성 풀기**: 원천 설명 · extracted 의 구성 → 5단계 단위 시술 키(U5-…). 회차 · 같은 날 여부 · 원천 문구 그대로. 키로 못 푸는 구성(5단계에 그 단위 시술이 없음)은 표시 + 행선지 안
C. **구성이 원천에 없는 것**(큐레이션 4 「보톡스 여러 부위」 등 · OQ-204): 원천에 적힌 만큼만(「승모근/종아리 등」) · 나머지는 원천 질문 문장
D. **경계**: 포토나4D(장비 한 대 다중 모드 = 단위 시술인가) · 셀리부트프로그램 · DNA리셋프로그램(고가 고정 — 특정 병원 상품인가 · 일반 패키지인가 근거) · 프리미엄 스킨케어 풀코스 등 — 판정 + 추천
E. **붙는 것**: 이름 · 동의어(시장가 이름 · 원장 이름) · 시장가(패키지 가격 · 단위 시술 1회 가격과 합치지 않음) · 원천 설명
F. **8단계 메모**: 패키지 구성 쌍과 synergy.json 링크를 대조해 같음 / 다름(같은 날 ↔ 간격) 목록 — 엣지는 만들지 않는다(8단계 몫)
G. **못 정하는 것은 표 하나로**(빈 추천 금지)

## 산출
`/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/step6-research.json` · `step6-research.md`. md 맨 위: ① 결정 묶음(추천 · 근거 · 영향) ② 사용자 최종 판단 — 한 표 ③ 셈(패키지 수 · 구성 풀림 · 원천 질문 · open 후보 전부 해결 안)

## 완료 보고 — 문구 변경 금지

```bash
orca orchestration send \
  --to term_15f07066-c2d1-4037-a5d1-d09830057ddb --from term_0933d258-4d62-4e51-b233-79a7c1ecea09 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "researcher 완료: 실버 6단계 패키지 조사" \
  --body "패키지 N / 구성 풀림 N / 사용자 판단 N"

orca terminal send --terminal term_15f07066-c2d1-4037-a5d1-d09830057ddb \
  --text "[worker_done] researcher 완료 — 실버 6단계 패키지 조사. 상세는 인박스." --enter
```
