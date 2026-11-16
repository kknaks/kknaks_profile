# [reviewer] 실버 2단계(계열) 반영 검수 — read-only

너는 맥락이 없다. read-only — 산출은 리포트 파일 1개뿐. 워크트리 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온`.

## 읽을 것
- 역할 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/roles/procedure-hub/reviewer/role.md`
- 결정 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/_RESUME.md` §2 10-28 「2단계 계열 기준」 · 「2단계 계열 조사 반영」 두 행 — 이것이 정본
- 조사(추천의 근거) `orchestration/work/phub-recommend/step2-research.json` · `.md` (D01~D18)
- 반영 `orchestration/work/phub-recommend/step2-apply.py` · `step2-families.json` · `.md` · `step2-origin-questions.md`
- 입력(고정) `step1-products.json` · 문헌 `/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-stg-2026-10-26/literature-evidence.json`

## 볼 것
1. **결정 ↔ 반영 전수**: D01~D18 이 결정대로 들어갔는지(유일한 예외 = 카복시 N2 미설립). 묶음별 대상 행이 모두 반영됐는지 행 단위로
2. **352행 전수**: active 352 = product_family 352 · 판정 셈 · family 가 18계열 또는 「계열 밖」 또는 null(null 은 전부 open + 원천 질문) · also_families 코드 유효
3. **조사 추천과 다른 행**: 코디 확인으로 4행(소프라노 티타늄 M8 · 버츄RF M11 · 셀리뉴 M9 · 소노퀸 M9) — 반영이 조사 추천을 바꿨다. 허가 품목명 · 원천 설명으로 어느 쪽이 맞는지 판정. 이 밖에 조사와 다른 행이 더 있는지 전수
4. **이름 규칙(D17)**: 「국내 공식 출처가 있으면 그것 · 없으면 공식 출처 미확인」 — M2(성형용 필러) · M7(안면조직고정용실) 처럼 조사가 국내 출처를 찾은 계열이 규칙대로 처리됐는지
5. **계열 정의 근거**: 계열마다 문헌 근거(PMID/DOI)가 있는지 · 새로 붙인 PMID 는 NCBI ESummary 로 실재 확인(표본 아니라 전수)
6. **범위 위반**: 3 · 4 · 5 · 6단계 일(부위 · 기법 · 단위 시술 · 목적)을 해 버린 곳 · 결정에 없는 변경 · step1-products.json 수정 여부
7. 결정론: `python3 step2-apply.py` 재실행 → 출력 동일(실행은 scratchpad 복사본에서 — 작업 폴더 파일을 바꾸지 마라)

## 산출
`/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/review-step2-report.md` 만. 맨 위 판정 PASS/FAIL/WARN + 지적마다 ledger_id · 파일 위치 · 근거 · 고칠 값.

## 완료 보고 — 문구 변경 금지

```bash
orca orchestration send \
  --to term_15f07066-c2d1-4037-a5d1-d09830057ddb --from term_e935d4d1-c970-4194-b5ff-68be7a928cc5 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "reviewer 완료: 실버 2단계 검수 <판정>" \
  --body "FAIL N / WARN N / 조사와 다른 행 판정"

orca terminal send --terminal term_15f07066-c2d1-4037-a5d1-d09830057ddb \
  --text "[worker_done] reviewer 완료 — 실버 2단계 검수 <판정>. 상세는 인박스." --enter
```
