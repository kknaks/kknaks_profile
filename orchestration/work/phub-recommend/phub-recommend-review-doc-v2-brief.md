# [reviewer_doc] SPEC-001 · WORK-001 재검수 — FAIL 7 반영 확인

너는 직전에 SPEC-001 · WORK-001 을 검수한 **procedure-hub `reviewer_doc` 워커**다(read-only).

작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온`

## 1. 읽을 것

- 네 1차 리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/review-spec-001-report.md`
- 수정본: 같은 폴더 `SPEC-001.md` · `WORK-001.md` (writer 가 F1~F7 · WARN 반영)
- 기준: 같은 폴더 `DEC-001.md`

## 2. 할 일

1. F1~F7 각각 닫혔는지 PASS/FAIL. 기대값은 1차 때처럼 stg 응답에 **바뀐 규칙**을 스크래치로 적용해 다시 센다(앞서 받은 응답 재사용 권장, 새 GET 은 엔드포인트당 1회 이내). writer 가 센 값: 노드 941 · 엣지 1,504 · procedure_relation 106 · conflict 7 · S-1 subgraph 노드 16 · 엣지 34 · S-2 노드 7 · 엣지 12 · M1 relation 17
2. WARN 반영 확인, 미반영 W1 이 OQ 로 남았는지
3. **수정이 만든 새 결함**(회귀) — 고친 절이 다른 절 · WORK Phase · E2E 스크립트 기대값과 어긋나는지
4. DEC 이탈 재확인(D-12 · D-13c · d · e)

## 3. allowed_paths

- 생성: 같은 폴더 `review-spec-001-v2-report.md` **1개만**

## 4. 판정

맨 위에 종합 PASS / WARN / FAIL. FAIL 은 「백엔드 워커가 문서대로 만들면 틀린 결과 · 테스트 실패가 나는 것」만. 취향 지적 금지.

## 5. 완료 보고 — 문구 변경 금지

```bash
orca orchestration send \
  --to term_92a9e861-40e9-4ab0-bec1-e792cb83801e --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "reviewer_doc 재검수 완료: <판정>" \
  --body "F1~F7 판정 / WARN / 회귀 / 다시 센 값"

orca terminal send --terminal term_92a9e861-40e9-4ab0-bec1-e792cb83801e \
  --text "[worker_done] reviewer_doc 재검수 완료 — <판정>. 상세는 인박스." --enter
```
