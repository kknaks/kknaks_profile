# [writer] SPEC-001 · WORK-001 2차 수정 — 재검수 회귀 R1 + WARN-n 4

너는 SPEC-001 · WORK-001 을 쓴 **procedure-hub `writer` 워커**다.

## 1. 읽을 것

- `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/review-spec-001-v2-report.md` — R1(FAIL) · WARN-n 4건
- 수정 대상: 같은 폴더 `SPEC-001.md` · `WORK-001.md`. 기준 `DEC-001.md`(D-06)

## 2. 할 일

1. **R1** — 시술군 단위 safety 묶음이 시술 항목 끝점의 안전 엣지(예: `procedure:M8-2-1` ↔ `procedure_group:M2` incompatible_same_day)를 이웃 · 부분 그래프에서 빠뜨린다. D-06(시술 노드를 내보낼 때 안전 엣지를 **항상** 같이)과 노드 상세에 맞게 safety 포함 규칙을 고치고, WORK:223 테스트 기대도 같이 고친다. 바뀐 규칙으로 영향받는 기대값(M1 safety 6 등)을 다시 센다
2. WARN-n 4건 전부 반영: Mount 예시에 stateless/json 옵션(SPEC:443 · WORK:234) · WORK:182 엣지 종류 수 · §6.3 이소트레티노인 간격 엣지 서술을 실측대로 · 점수표에 names.en 명시
3. 변경 이력에 「재검수 반영 — R1 · WARN-n」 한 줄
4. 이번에 바꾼 줄 외에는 건드리지 않는다

## 3. allowed_paths

- `SPEC-001.md` · `WORK-001.md` 수정만

## 4. 완료 보고 — 문구 변경 금지

```bash
orca orchestration send \
  --to term_92a9e861-40e9-4ab0-bec1-e792cb83801e --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "writer 완료: 재검수 반영" \
  --body "R1 처리(바뀐 규칙 · 다시 센 값) / WARN-n 4 / 바꾼 절 목록"

orca terminal send --terminal term_92a9e861-40e9-4ab0-bec1-e792cb83801e \
  --text "[worker_done] writer 완료 — 재검수 반영. 상세는 인박스." --enter
```
