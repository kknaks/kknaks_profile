# [planner] SPEC-006 고침 6 — 사용자 결정 R40 (오늘만 실시간 · 다른 날짜는 요청 때 1회 · 잠금)

읽을 것: 결정 파일 `/Users/kknaks/orca/workspaces/kknaks_profile/day-ext/reference/2026-11-23-reservation/reservation-board-decisions.md` 맨 아래 **R40** · 고침 4 · 4b · 5 지시서(`/Users/kknaks/orca/workspaces/kknaks_profile/day-ext/orchestration/work/day-reservation/planner-fix-4-instructions.md` · `-4b-` · `-5-`)
작업 워크트리: `/Users/kknaks/orca/workspaces/mediness-mediness/day-reservation-spec`

## 고칠 것
1. **R40 반영**: 오늘 = 10초 회차만(그대로). 다른 날짜 = 화면이 열거나 바꿀 때 중앙에 최신화 요청 1회 → 중앙이 KOS 에서 받아 저장(R26 범위 · C1 ~ C3) → 화면은 DB 사본 · 저장 뒤 다음 다시 읽기에 최신. 같은 (병원 · 날짜) 최신화에 잠금 — 동시 요청은 한 번만. **주기적 재최신화 없음.** R39 그대로.
2. R29 의 「보는 중」 표시 · 만료 · 중앙 주기 최신화 문장 — 취소선 + R40. **OQ-R34 · R35 · R37 닫음(R40 — 필요 없음)** · 닫힌 OQ 표로. OQ-R36(폴링 / SSE)은 남긴다 — 폴링은 DB 만 다시 읽음(KOS 안 부름) 명시. 케이스: 「다른 날짜를 열어 둔 채 시간이 지남 = 다시 열 때까지 그 사본」 · 「같은 날짜 동시 요청 = 잠금으로 한 번」 · 「받는 중 다시 읽기 = 이전 사본」 줄
3. 잠금 · 큐 · 함수 설계는 여전히 WORK 몫 — 조건만(같은 병원 · 날짜에 한 번 · 오늘 회차와 C1 · C2)
4. 끝으로 R40 위반 잔존 전수 grep(`보는 중|만료|주기|OQ-R3[457]|R29`) — 줄마다 판정을 완료 보고에 적는다
5. `20-spec.md` · `10-decision.md` · `log.md` · 머리 요약 · §8 검증 → §9 완료 보고
