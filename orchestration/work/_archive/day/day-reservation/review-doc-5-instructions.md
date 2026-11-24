# [reviewer_doc] SPEC-006 5차 검수 — 고침 4 · 4b(R29 ~ R33 · R39) 확인

맥락이 없으면 먼저 읽어라: 원 브리프 `/Users/kknaks/orca/workspaces/kknaks_profile/day-ext/orchestration/work/day-reservation/day-reservation-review-doc-brief.md` · `/Users/kknaks/orca/workspaces/kknaks_profile/day-ext/orchestration/work/day-reservation/review-doc-2-instructions.md`(코디 정정) · `/Users/kknaks/orca/workspaces/kknaks_profile/day-ext/orchestration/work/day-reservation/review-doc-4-instructions.md`(설계를 SPEC 에서 요구하지 마라) · 네 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day-ext/orchestration/work/day-reservation/review-doc-4-report.md` · planner 지시서 `/Users/kknaks/orca/workspaces/kknaks_profile/day-ext/orchestration/work/day-reservation/planner-fix-4-instructions.md` · `/Users/kknaks/orca/workspaces/kknaks_profile/day-ext/orchestration/work/day-reservation/planner-fix-4b-instructions.md` · 결정 파일 `/Users/kknaks/orca/workspaces/kknaks_profile/day-ext/reference/2026-11-23-reservation/reservation-board-decisions.md`(맨 아래 R29 ~ R33 · R39 — **R39 가 R29 의 「첫 열기 즉시 최신화」 · C4 를 뒤집었다**)

작업 워크트리: `/Users/kknaks/orca/workspaces/mediness-mediness/day-reservation-spec` (고치지 마라)

## 볼 것
1. W4-1 ~ W4-3 이 닫혔는지
2. R29 ~ R33 · R39 가 본문 전체(갱신 모델 표 · 흐름 · API · 케이스 · Rule 7 · 실시간 갱신 절 · 닫힌 OQ 표 · 머리 요약 · 20-spec · 10-decision · log)에서 일관한지 — 특히 **요청 경로가 KOS 를 부른다는 문장이 취소선 없이 남은 곳**(R39 위반) · C4 옛 문장 잔존
3. 남은 OQ-R34 ~ R38 · R21 — 기본안이 본문에 결정처럼 섞였는지
4. 이번 고침이 새로 만든 모순만 FAIL · 설계 요구는 FAIL 아님 · 앞 판 PASS 영역을 새로 뒤지지 마라
5. 판정 FAIL / WARN / PASS

리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/day-ext/orchestration/work/day-reservation/review-doc-5-report.md` 1개만. 완료 보고는 preamble 의 taskId · dispatchId 로.
