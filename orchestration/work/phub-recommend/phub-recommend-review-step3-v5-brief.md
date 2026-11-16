# [reviewer] 실버 3단계 최종 검수 v5 — 짧게 · 지금 원천 기준만

read-only · 산출 리포트 1개. 워크트리 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온`. 역할 `orchestration/roles/procedure-hub/reviewer/role.md`.

## 기준(사용자 10-28 — 바뀜)
- 부위 = 「어디에 맞냐」 = 사람 몸 겉에서 가리키는 자리. 원천은 **이름 칸만**(`step3-decisions.json` name_fields 17). 설명 문장 속 해부 낱말은 부위가 아니다
- 해부학 용어(층 · 근육 · 혈관 · 뼈)는 기법 · 작용기전 · 안전 쪽. 노드 이름 2벌 = 일반인(노드 이름) + 전문의(겉자리 이름만)
- **가상 문장 시험 · 해부학 목록 확장 · 미래 원천 대비는 보지 않는다.** 끝 조건 = 지금 원천 기준 open 0 · 결정대로 · 결정론
- 정본 `orchestration/work/phub-recommend/_RESUME.md` §2 10-28 3단계 행 전부

## 볼 것 (이것만)
1. 이름 칸 17 이 DEC-002 D-05 ① 「원천이 따로 부르는 칸」에 맞는지 · 빠진 이름 칸 없는지(원천 21파일 키 목록 대조)
2. 이름 칸 안 부위 문자열 전수(175 · 439회) 행선지가 결정대로인지 — 원천 이름 칸에서 독립 재추출해 대조
3. 노드 53: 상위 · 이름 칸 근거 · 전문의 용어가 겉자리 이름만인지(근육 · 뼈 · 혈관 0) · 근육 4행 교체
4. 의료진 질문 35 · open 0 · 결정론 · DEC · step1 · step2 · 원천 미수정
- 산출 `orchestration/work/phub-recommend/review-step3-v5-report.md` · 맨 위 PASS/FAIL + 「open = N」. 지적은 지금 원천 데이터에 실제로 있는 것만

## 완료 보고 — 문구 변경 금지

```bash
orca orchestration send \
  --to term_15f07066-c2d1-4037-a5d1-d09830057ddb --from term_8312a270-deaa-40fd-9e56-eb1fcd3be479 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "reviewer 완료: 실버 3단계 최종 검수 v5 <판정>" \
  --body "open N / FAIL N / WARN N"

orca terminal send --terminal term_15f07066-c2d1-4037-a5d1-d09830057ddb \
  --text "[worker_done] reviewer 완료 — 실버 3단계 최종 검수 v5 <판정>. 상세는 인박스." --enter
```
