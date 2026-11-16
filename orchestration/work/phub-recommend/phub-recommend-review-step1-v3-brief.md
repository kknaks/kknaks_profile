# [reviewer] 1단계 반영 검수 — 결정이 원장에 빠짐없이 · 틀림없이 들어갔나

너는 1단계를 두 번 검수한 reviewer 다(read-only). 워크트리 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온`.

## 기준 (정본)
- `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/_RESUME.md` §2 결정표 10-27 · 10-28 행 · `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/gate-answers/step1-decisions-db-2026-10-28.md`
- 조사 결과 `step1-d09-web` · `d12-web` · `d15-web` · `d16-web` · `d17` · `d17-2` · `d18` · `d19` · `d20-31` · `cancel-recheck`

## 대상
`/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/step1-products.json` · `.md` · `step1-apply-log.md` · `step1-source-fix.json/.md` · `step1-origin-questions.md`

## 볼 것
1. **결정 → 원장 전수 대조**: 결정표의 모든 결정(묶음 · 제품)이 원장 해당 행에 반영됐나 — 빠짐 · 다름 목록
2. **규칙 전수 적용**(390+행 전부, 표본 아님): 정상만 연결 · 취소/취하/재제조 이력 · **수출용 허가가 연결에 남은 행 0** · 상태 6종과 recommendable 일치 · 「허가 대상 아님」은 출처 있음 · 대표 이름 한글 1 · 이유는 근거 칸에만 · 국내 제조 수입사 「해당 없음」
3. 합침 · 시술 이름으로 빠짐 행이 지워지지 않고 표시만 됐나
4. **결정에 없는 변경**(회귀) — 반영하면서 건드린 다른 행
5. 의약품 KPIC 보강 출처 · 원천 수정 · 질문 목록이 결정과 맞나
- 산출 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/review-step1-v3-report.md` 1개 · 맨 위 PASS/FAIL · 지적은 행 id + 한 줄

## 완료 보고 — 문구 변경 금지

```bash
orca orchestration send \
  --to term_230b7660-9039-4f63-9c96-f8e68bde732b --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "reviewer 완료: 1단계 반영 검수 <판정>" \
  --body "빠짐 N / 다름 N / 규칙 위반 N / 회귀 N"

orca terminal send --terminal term_230b7660-9039-4f63-9c96-f8e68bde732b \
  --text "[worker_done] reviewer 완료 — 1단계 반영 검수 <판정>. 상세는 인박스." --enter
```
