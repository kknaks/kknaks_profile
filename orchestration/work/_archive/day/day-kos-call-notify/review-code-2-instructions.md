# [reviewer] #283 코드 재검수 r2

같은 워크트리 · 같은 맥락(읽기만 · 시험 실행 가능). 역할 · 금지는 첫 브리프 `/Users/kknaks/orca/workspaces/kknaks_profile/day-시술/orchestration/work/day-kos-call-notify/day-kos-call-notify-review-brief.md` 그대로.

- 너의 r1 리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/day-시술/orchestration/work/day-kos-call-notify/review-code-r1-report.md`
- 수정 지시: `/Users/kknaks/orca/workspaces/kknaks_profile/day-시술/orchestration/work/day-kos-call-notify/be-fix-1-instructions.md` (코디 결정)
- 수정 보고: `/Users/kknaks/orca/workspaces/kknaks_profile/day-시술/orchestration/work/day-kos-call-notify/be-fix-1-report.md`

## 볼 것

1. r1 W1 ~ W4 · I1 · I3 · I5 가 지시대로 고쳐졌나(파일:줄 · 시험 · 변이). I2 · I4 · I6 「그대로 둔 이유」가 타당한가. 닫힘/남음 표.
2. 수정이 새 문제를 만들었나 — 특히 W1 ② `event_log` `kosCalledAt` 최댓값 조회(잠금 안 · 같은 tx · 쿼리 비용 · 시각 비교 단위/시간대) · W2 합집합이 DAY 일반 호출 받는 사람을 바꾸지 않나 · I1 예외 범위.
3. 보고서 「이슈」: DAY 호출 메아리 시각은 `kosCalledAt` 에 안 남아, 메아리 창 뒤 옛 사본이 빈 값 → 값으로 되돌리면 새 호출이 생기는 좁은 틈. **migration · 새 enum 없이** 막는 방법이 있는지 코드로 따져 고칠 방향을 적어라(예: 메아리로 판정한 회차에 그 DAY 호출의 event_log 에 kosCalledAt 를 남기기 — event type 이 enum/제약인지 확인).
4. 시험 실행: 새 · 바뀐 시험 + 동기화 · 판 호출 · 알림 기존 시험 1회 · ruff.

## 판정

`/Users/kknaks/orca/workspaces/kknaks_profile/day-시술/orchestration/work/day-kos-call-notify/review-code-r2-report.md` — PASS / WARN / FAIL + 지적마다 [심각도 · 파일:줄 · 근거 · 고칠 방향] + 「사용자가 실물에서 만날 자리」. 완료 보고 두 명령(subject 「reviewer 완료: 코드 r2」 · 이번 dispatch 값 · 코디 term_ff2b168e-072a-4b6d-ac4a-8dd2eacda5ce):

```bash
orca orchestration send --to term_ff2b168e-072a-4b6d-ac4a-8dd2eacda5ce --from <네 워커handle> --type worker_done --task-id <taskId> --dispatch-id <dispatchId> --subject "reviewer 완료: 코드 r2" --body "<요약>"
orca terminal send --terminal term_ff2b168e-072a-4b6d-ac4a-8dd2eacda5ce --text "[worker_done] reviewer 완료 — 코드 r2 <한 줄>. 상세는 인박스." --enter
```
