# [planner] SPEC-002 개정 — 사용자 화면 확인 피드백(F3 · F4 · F5 · F6 · F7 · F10)

너는 day planner 다. mediness 워크트리 · 미커밋 · 커밋 금지.
읽을 것: 피드백 모음 `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/board-feedback.md`(F3 · F4 · F5 · F6 · F7 · F10 — 각 줄의 결정 · 근거) · 원천 `/Users/kknaks/orca/workspaces/kknaks_profile/day/reference/2026-11-03-cc-day/screen/procedure-board-decisions.md`(U8 바로잡음 · 「결정 — 화면을 보고」 · 「결정 — KOS 쓰기」 · 「결정 — 다시 호출」) · cc `/Users/kknaks/git/toy_pr2/kknaks_profile/para/projects/summer-star/cc-prototype/10-decision/decision-005-procedure-board.md` D-25 · D-26 · D-27 · cc 코드 `git -C /Users/kknaks/git/toy_pr2/cc-prototype show origin/main:procedure/back/app/kos/ops.py`(귀가 대기 · 되돌리기 요청 모양).
고칠 것:
- **F3** 호출 대상 = cc D-26(대기면 호출 · 수락돼도 다시 호출) · 유효 호출 = 가장 최근 · 다시 호출하면 앞 수락 무효(D-25 · D-27) — 규칙 5 · 6 · 7 · 「cc 와 다른 곳」 표 · 케이스 매트릭스.
- **F4** 카드 안 줄 순서 = 진행중(시작 순) → 대기(오더 순) → 완료(완료 시각 순).
- **F5** U8 — 귀가 대기는 판에서 빠지고 사이드바 「시술 완료」 탭에만(카드 조건 · 상태 절).
- **F6** E09 · E10 — 1차 화면에서 뺌(자리도 안 그림).
- **F7** 고객 줄 — 「입실」 빼고 「국적」(`customer.nationality` 그대로 · 없으면 안 그림 · OQ-02-1).
- **F10** KOS 쓰기 토큰 = **누른 사람 토큰**(규칙 9 · 24 · OQ-05 바로잡음 — 대리 수락도 누른 간호사 토큰 · KOS 엔 수락한 의사 doctorIds) · 귀가 대기 · 시작 취소 · 완료 취소 = **cc 구현 근거로 연다**(W6 바꿈 · KOS 쓰기 표 · 근거 = cc 코드 · 방배정.har PROCEDURE_WAITING). 「HAR 요청」 OQ 에서 이 동작들을 걷는다.
log 한 줄 · lint `--strict`. 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/planner-spec002-feedback-report.md`. 완료는 preamble 의 worker_done 절차대로(둘 다).
