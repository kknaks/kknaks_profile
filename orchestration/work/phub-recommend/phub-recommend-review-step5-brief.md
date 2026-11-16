# [reviewer] 실버 5단계(단위 시술) 검수 — 짧게 · 지금 원천 기준만

너는 맥락이 없다. read-only · 산출 리포트 1개. 워크트리 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온`. 역할 `orchestration/roles/procedure-hub/reviewer/role.md`.

## 기준
- 정본 `orchestration/work/phub-recommend/_RESUME.md` §2 2026-10-29 행 전부(5단계 시작 · 원칙 「클리닉에서 하는 시술은 전부 단위 시술」 · 재추천 · 웹 조사 · 추가 조사 반영 U1~U9 + 보정 · 반영 확인 3)
- **지금 원천 기준만** — 가상 문장 · 미래 원천 대비는 보지 않는다. 지적은 지금 데이터에 실제로 있는 것만. 끝 조건 = open 0 · 결정대로 · 결정론 · **원장 521 중 시술은 전부 단위 시술**

## 볼 것
1. 원장 521 행선지 전수 — 시술 167 = 단위 시술 167 · 시술 아님 20(아큐탄 · 성분 17 · 확인 조건 약물 2)이 맞나 · 시술인데 빠진 것 0 인지 **원천에서 독립 판정**
2. 단위 시술 키 138: 계열 × [안 C 하위] × 부위 × 기법 · 이름 규칙 · 동의어(원장 · 메뉴 · 장비 이름) · 성분 미상 수액 4 「미상」 · 카복시 바디 기본값 · 프로락틴 두피 · 병변 단위 2 · N2~N7
3. 붙는 것: 쓰는 제품(도포 가드 U5 · 1단계 recommendable) · 시장가 시술 1회 115 · PIH · 운영 · 4단계 속성 · extracted
4. 앞 단계 정본 보강: 1단계(듀오 하이드로젠 · 파셀라) · 2단계(N2~N7 · 354행 · 고정 assert 제거) · 4단계(K13 · K06 · 기본 기법) — 결정대로 · 그 밖 회귀 0
5. open 0 · 결정론(1 · 2 · 4 · 5 재실행) · 스킬 점검 3종 · 원천 질문 `step5-origin-questions.md`
- 대상: `step5-decisions.json` · `step5-apply.py` · `step5-units.json` · `.md` · `step5-fixtures/` · 고친 `step1-*` · `step2-*` · `step4-*` / 근거 `step5-research.*` · `step5-research2.*`
- 산출 `orchestration/work/phub-recommend/review-step5-report.md` · 맨 위 PASS/FAIL + 「open = N」

## 완료 보고 — 문구 변경 금지

```bash
orca orchestration send \
  --to term_15f07066-c2d1-4037-a5d1-d09830057ddb --from term_d296be39-1916-4c6e-bbea-9d15eb4098f4 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "reviewer 완료: 실버 5단계 검수 <판정>" \
  --body "open N / FAIL N / WARN N"

orca terminal send --terminal term_15f07066-c2d1-4037-a5d1-d09830057ddb \
  --text "[worker_done] reviewer 완료 — 실버 5단계 검수 <판정>. 상세는 인박스." --enter
```
