# [reviewer] 실버 4단계(기법) 검수 — 짧게 · 지금 원천 기준만

너는 맥락이 없다. read-only · 산출 리포트 1개. 워크트리 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온`. 역할 `orchestration/roles/procedure-hub/reviewer/role.md`.

## 기준
- 정본 `orchestration/work/phub-recommend/_RESUME.md` §2 10-28 4단계 행(시작 · 반영 J1 안 1 · J2) · 해부학 용어 행 · source-map 승인 행
- **지금 원천 기준만**: 지도(`source-map.json`)가 4단계로 정한 칸 27 이 입력. 설명 문장 전체 · 가상 문장 · 미래 원천 대비는 보지 않는다. 지적은 지금 데이터에 실제로 있는 것만
- 끝 조건 = open 0 · 결정대로 · 결정론

## 볼 것
1. 노드 24 가 조사 S1~S3 · J1 안 1 대로(상위 · 근거)
2. 칸 27 표현 181 행선지가 결정대로 — 원천 칸에서 독립 재추출해 대조
3. 속성(층 · 대상 근육 · 펄스 · 박피) · safe_layers(코 = 콧등 골막상 · 코끝 연골막상) · 계열 기본 18 · 넘겨받은 것 15 · 초안 65 대응
4. open 0 · 결정론 · 구조(결정 = 데이터 파일 · 고정 숫자 assert 없음) · step1~3 · DEC · 원천 미수정
- 대상: `step4-decisions.json` · `step4-apply.py` · `step4-techniques.json` · `.md` · `step4-source-fix.md` · `step4-fixtures/` / 근거 `step4-research.*`
- 산출 `orchestration/work/phub-recommend/review-step4-report.md` · 맨 위 PASS/FAIL + 「open = N」

## 완료 보고 — 문구 변경 금지

```bash
orca orchestration send \
  --to term_15f07066-c2d1-4037-a5d1-d09830057ddb --from term_e949457d-43a2-406f-83e1-6afe10a6484d \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "reviewer 완료: 실버 4단계 검수 <판정>" \
  --body "open N / FAIL N / WARN N"

orca terminal send --terminal term_15f07066-c2d1-4037-a5d1-d09830057ddb \
  --text "[worker_done] reviewer 완료 — 실버 4단계 검수 <판정>. 상세는 인박스." --enter
```
