# [backend] #283 be-fix-2 — 재검수 r2 N1 시험 + I-a

같은 워크트리 · 같은 맥락. 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day-시술/orchestration/work/day-kos-call-notify/review-code-r2-report.md` (판정 PASS · N1 · I-a · I-b · I-c).

- **N1** 고정 시험 추가 — 리포트 「고칠 방향」 그대로(DAY 호출 → op confirmed updated_at=E+2초 → detail_round(E) 0건 → now 10분 뒤 → 빈 값 → 다시 E → 0건). 창 비교를 관측 시각 now 기준으로 바꾸는 변이에서 빨개지는지 확인 후 되돌림.
- **I-a** `kos_calls.py:126-129` `kosCalledAt` 파싱 — 형식이 틀린 행은 **그 행만 건너뛰고 경고 로그 1줄**(병원 id · event id 만 · 값 없음) · 회차는 계속. 시험 1개.
- I-b · I-c: 코드 변경 없음(I-b 는 스펙 반영 · I-c 는 리포트가 문제없다고 판정).

검증: 바뀐 시험 파일 + 기존 kos_calls 시험 1회 · ruff · format · mypy 바뀐 파일. 커밋 · push 금지.

보고 `/Users/kknaks/orca/workspaces/kknaks_profile/day-시술/orchestration/work/day-kos-call-notify/be-fix-2-report.md` · 완료 보고 두 명령(subject 「backend 완료: be-fix-2」 · 이번 dispatch 값 · 코디 term_ff2b168e-072a-4b6d-ac4a-8dd2eacda5ce):

```bash
orca orchestration send --to term_ff2b168e-072a-4b6d-ac4a-8dd2eacda5ce --from <네 워커handle> --type worker_done --task-id <taskId> --dispatch-id <dispatchId> --subject "backend 완료: be-fix-2" --body "<요약>"
orca terminal send --terminal term_ff2b168e-072a-4b6d-ac4a-8dd2eacda5ce --text "[worker_done] backend 완료 — be-fix-2 <한 줄>. 상세는 인박스." --enter
```
