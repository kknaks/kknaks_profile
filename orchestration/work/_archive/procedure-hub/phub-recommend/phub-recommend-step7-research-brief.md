# [researcher] 실버 7단계(고민 · 목적 · 추천 조합) 조사 (read-only)

너는 맥락이 없다. 역할 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/roles/procedure-hub/researcher/role.md`. 워크트리 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온`. 원장 · 결정 · 원천 수정 금지. 산출 2파일만.

## 읽을 것
- 결정 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/_RESUME.md` §2 — 특히 10-28 source-map 승인(U1 단계 경계 · U2 고민 정본 · U3 추천 조합 노드) · 10-29 「실버 7단계 시작」 행 · DEC-001 D-13d · D-13e · OQ-104 · OQ-105 · OQ-120 · DEC-002 D-03 · D-07
- 지도 `source-map.json` · `.md`(B07 · B08 · B09 · B12 · O6 · O7) · `SPEC-004.md`(concern 노드 · treats 엣지)
- 정본: `step3-sites.json`(deferred 7단계) · `step5-units.json`(units[].purposes · 동의어) · `step6-packages.json`(non_packages 메뉴 분류 → 7단계)
- 원천 `/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-stg-2026-10-26/`: taxonomy.problem · problem-packages · problem-combos · combo-recipes · treatment-optimization · procedure-comparison · synergy(target 만) · treatment-sequence(common_combos)
- 사이트 화면 코드(무엇이 사용자에게 보이는지) `/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-recommend/frontend/src/app/recommend/page.tsx` · `compare` · `optimize` · `synergy`
- 앞 단계 교훈 `para/projects/company/procedure-hub/log/2026-10-29-silver-step5-unit.md` · `-step6-package.md` §5 — 지금 원천 기준 · 추정 금지 · 같은 성격 전수 · 가상 문장 없음 · 사이트 용어 확인

## 할 것
A. **고민 노드**: taxonomy problem 3층(대 · 중 · 항목) 전수 · 쁘띠시술 · 기타 분해(부위 + 목적) · 제모 · 얼굴윤곽 목적형 · 이름 정리(쳐짐 → 처짐 등 결정된 것) · 부위가 붙은 고민은 3단계 D-07 대로 분리
B. **고민 대응표**: 다른 원천의 고민 표현(problem-packages CC 115 · problem-combos · 최적화 고민 · 시너지 target · 레시피 goal · 비교 테마 · 연령 주 고민 · 3단계 넘김 6 · 6단계 메뉴 분류 7) → 고민 노드. 완전 일치 / 동의어 / 상하위 / 대응 없음 + 근거 · 사람 확인 필요 표시
C. **목적**: 목적 노드 목록(원천 표현에서 — 5단계 purposes 25 · 원장 용도 · 메뉴 분류) · 고민 ↔ 목적 경계(같은 말이 둘 다인 것) · 「고민 → 단위 시술」 엣지 = 원천에 적힌 구조만(CC 추천 시술 · problem-combos 구성 · 최적화 등) · 적응증 문장은 근거로만
D. **추천 조합 노드**: 원천별(problem-combos 24 · combo-recipes 7 · common_combos · 최적화 중증도 조합 · 연간 · 연령 플랜 · 비교 9) — 종류 · 고민 앵커 · 구성(계열 코드 → 고민 부위로 단위 시술 내림 · 못 내리면 후보 전부 + 표시) · 등급 · 가격 · 기대 효과 · 영업 문구(보관 · 기본 제외) 원문
E. **8단계 메모**: 쌍 주장(금기 · 간격 · 순서 · 시너지)은 8단계로 표시만
F. **못 정하는 것은 표 하나로**(빈 추천 금지)

## 산출
`/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/step7-research.json` · `step7-research.md`. md 맨 위: ① 결정 묶음 ② 사용자 최종 판단 — 한 표 ③ 셈(고민 노드 · 대응 · 목적 · 엣지 · 추천 조합 · open 후보 전부 해결 안)

## 완료 보고 — 문구 변경 금지

```bash
orca orchestration send \
  --to term_15f07066-c2d1-4037-a5d1-d09830057ddb --from term_e26156f4-8782-44ae-a353-d8e898aac111 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "researcher 완료: 실버 7단계 조사" \
  --body "고민 N / 대응 N / 목적 N / 추천 조합 N / 사용자 판단 N"

orca terminal send --terminal term_15f07066-c2d1-4037-a5d1-d09830057ddb \
  --text "[worker_done] researcher 완료 — 실버 7단계 조사. 상세는 인박스." --enter
```
