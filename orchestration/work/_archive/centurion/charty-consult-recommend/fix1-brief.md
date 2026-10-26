# frontend 수정 1판 — 코드 검수 FAIL 처리

근거: 같은 폴더 `code-review-report.md` §7·§8. 범위·금지 사항은 `fe-brief.md` §3 그대로(커밋 금지 · 3417 서버 재시작 금지).

## 고칠 것
1. **F-1** `anchor-projector.tsx` useFrame 첫 줄에 `camera.updateMatrixWorld()` — 투영 한 프레임 지연 제거. 확인: `npx playwright test e2e/areas.spec.ts -g R-13 --repeat-each 3` 3회 통과. 시험 기준(1px) 그대로
2. **W-1** R-14 시험이 드래그 방향마다 먼 쪽 키를 고정하고 `hidden ∩ far ≥ 1` 을 단언하게
3. **W-4** 측정값 없음 상태의 카드 안 문구를 짧게(「측정 데이터 없음」), 긴 안내는 오른쪽 열 `ReportPlaceholder` 에 맡긴다(`report-missing` testid 유지 · viewer.spec AC-23 통과)
4. **N-2** `leader-lines.tsx:31-34` 렌더 중 레지스트리 변경 루프 제거(ref 콜백이 이미 넣음)

## 하지 마라
- W-5·W-6·W-7(흐린 선 · 모달 가독성 · 카드 여백 · 긴 선)은 **손대지 마라** — 사용자 눈 확인 뒤 2루프에서 모아 처리한다

## 확인 · 보고
- 관련 시험만: `npm run lint` · `npm run test` · `e2e/areas.spec.ts` · `e2e/viewer.spec.ts`
- `fe-report.md` 에 「수정 1판」 절 추가(항목별 결과 · 명령 출력)
- 완료:
```bash
orca orchestration send --type worker_done --task-id <task_id> --dispatch-id <dispatch_id> --json
orca terminal send --terminal term_b9769e7c-1d9b-4064-b187-8f47aaefc476 --text "[frontend 수정1 완료] orchestration/work/charty-consult-recommend/fe-report.md" --enter
```
