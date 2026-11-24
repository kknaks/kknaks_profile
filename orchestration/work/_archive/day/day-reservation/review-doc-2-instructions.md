# [reviewer_doc] SPEC-006 2차 검수 — 고침 1 확인

너는 1차 검수를 한 reviewer_doc 다. 맥락이 없으면 먼저 읽어라:
- 원 브리프 `/Users/kknaks/orca/workspaces/kknaks_profile/day-ext/orchestration/work/day-reservation/day-reservation-review-doc-brief.md` (§5 read-only · §8 · §9 그대로)
- 네 1차 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day-ext/orchestration/work/day-reservation/review-doc-1-report.md`
- **결정 파일(갱신 — R17 ~ R20 추가 · R1 보충 · 「데이터」 머리 문장 고침)** `/Users/kknaks/orca/workspaces/kknaks_profile/day-ext/reference/2026-11-23-reservation/reservation-board-decisions.md`
- planner 고침 지시서 `/Users/kknaks/orca/workspaces/kknaks_profile/day-ext/orchestration/work/day-reservation/planner-fix-1-instructions.md`

작업 워크트리: `/Users/kknaks/orca/workspaces/mediness-mediness/day-reservation-spec` (planner 미커밋 변경 · 고치지 마라)

## 코디 정정 — 원 브리프 바뀐 곳
원 브리프의 「기대는 개념 read-side-effect — 조회 경로에 KOS 호출 · DB 쓰기가 없어야 한다」는 **취소**(코디 잘못). 사용자 결정 R17: 보는 날짜를 KOS 에서 가져와 DB 를 최신화한 뒤 DB 를 읽는다. 「조회 때 KOS 호출」을 FAIL 로 보지 마라.

## 볼 것
1. 1차 F-1 · W-1 ~ W-9 가 각각 닫혔는지(행별 표)
2. R17 ~ R20 반영이 본문 전체에서 일관한가 — 특히 새 §3 「조회 흐름」 · API · 케이스 · 필터 · 공지 · 회색 규칙. 취소선 처리한 옛 문장이 아직 살아 있는 곳
3. 새 「조회 흐름」 코드 사실(emr_sync.py · kos/__init__.py · sync_schedules.py · tasks/emr.py · pacing.py · config.py 줄)을 `git -C /Users/kknaks/git/CENTURION_DAY show origin/dev:<path>` 로 직접 확인
4. 새 OQ-R21 ~ R25 — 기본안이 결정처럼 본문에 섞였는지 · R18(선동기화 안 함)과 어긋나는 기본안이 없는지
5. 판정 FAIL / WARN / PASS

리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/day-ext/orchestration/work/day-reservation/review-doc-2-report.md` 1개만.
완료 보고는 preamble 의 taskId · dispatchId 로(원 브리프 §9 방식).
