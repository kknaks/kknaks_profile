# [reviewer] 실버 3단계(부위) 반영 검수 — read-only · 끝 조건 open 0

너는 맥락이 없다. read-only — 산출 리포트 1개. 워크트리 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온`.

## 읽을 것
- 역할 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/roles/procedure-hub/reviewer/role.md`
- 결정 `orchestration/work/phub-recommend/_RESUME.md` §2 10-28 「3단계(부위) 시작」 · 「3단계 부위 조사 반영」 행 · 부위 정본 `DEC-002.md` · `DEC-003.md`
- 조사 `step3-research.json` · `.md` · 반영 `step3-decisions.json` · `step3-apply.py` · `step3-sites.json` · `.md` · `step3-source-fix.md` · 지시 `phub-recommend-step3-apply-brief.md`
- 원천 `/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-stg-2026-10-26/`
- 앞 단계 검수 방식 참고 `review-step2-report.md` · `review-step2-v5-report.md` (2단계 교훈: 검수 PASS ≠ 끝 · 끝 = open 0 · 출처가 값을 실제로 받치는지 전수)

## 볼 것
1. 결정 ↔ 반영: B1~B12 · U1 · U2 가 결정대로(노드 53 · 새 10 상위 · 동의어 · 트리 밖 판정)
2. 문자열 500 전수: 행선지 · 셈(노드로 325 · deferred 175) · 원천 재추출로 등장 수 대조(표본 아니라 전수 — 놓친 부위 문자열이 없는지 원천에서 독립적으로 다시 뽑아 비교)
3. D-07 분리(부위 + 고민/목적/제품)가 맞는지 · 정해진 트리 위반 0
4. 해부학 이름 후보 53: 근거 「강」 행은 인용한 레포 키 · 출처가 실제로 그 값을 말하는지 전수 · 「약」은 질문에 올라갔는지
5. 위험 부위 11 대응 · 의료진 질문 22
6. 범위 위반(4 · 5 · 6 · 7 · 8단계 일을 해 버린 곳) · DEC · step1 · step2 · 원천 수정 여부
7. 결정론(scratchpad 사본 재실행) · **고정 숫자 assert 없음 · 결정이 데이터 파일로 빠졌는지**(새 부위 · 새 문자열 추가 때 결정 파일만 고치면 되는 구조인지 — 원천 재추출이 조사 판과 같아야만 도는 가드가 새 원천 추가를 어떻게 다루는지 평가)
8. **open 0**
- 산출 `orchestration/work/phub-recommend/review-step3-report.md` · 맨 위 PASS/FAIL + 「open = N」 · 지적마다 위치 · 근거 · 고칠 값

## 완료 보고 — 문구 변경 금지

```bash
orca orchestration send \
  --to term_15f07066-c2d1-4037-a5d1-d09830057ddb --from term_a7ff6cee-c0d1-4402-b300-3e7f44fcb55c \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "reviewer 완료: 실버 3단계 검수 <판정>" \
  --body "open N / FAIL N / WARN N"

orca terminal send --terminal term_15f07066-c2d1-4037-a5d1-d09830057ddb \
  --text "[worker_done] reviewer 완료 — 실버 3단계 검수 <판정>. 상세는 인박스." --enter
```
