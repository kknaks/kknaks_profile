# [planner] SPEC-006 고침 5 — 5차 검수 FAIL 1 · WARN 4 (문장 정리)

읽을 것: 5차 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day-ext/orchestration/work/day-reservation/review-doc-5-report.md` · 결정 파일 `/Users/kknaks/orca/workspaces/kknaks_profile/day-ext/reference/2026-11-23-reservation/reservation-board-decisions.md`(W5-5 는 코디가 고침 — R33 의 R28 ⓐ C4 취소선)
작업 워크트리: `/Users/kknaks/orca/workspaces/mediness-mediness/day-reservation-spec`

## 고칠 것 — 리포트의 「고칠 것」 그대로
1. F5-1 — S6 L62 · L72 · L94 · `20-spec.md:36` 의 「날짜를 열면 KOS 최신화 뒤 그림」 → 취소선 + R39 문구(R27 날짜 잠금 문구도)
2. W5-1 ~ W5-4
3. 끝으로 **R39 위반 잔존 전수 grep**: `grep -nE 'KOS.{0,20}(최신화|가져)|열면|요청 때|첫 열기|즉시|ensure_day|C4' products/day/20-spec/spec-006-reservation-board.md products/day/20-spec.md products/day/10-decision.md` — 걸린 줄마다 취소선 안인지 · R39 와 맞는지 확인하고, 그 결과(줄 · 판정)를 완료 보고 본문에 적는다
4. log.md 한 줄 · §8 검증 → §9 완료 보고(preamble 의 taskId · dispatchId)
