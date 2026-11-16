# [reviewer] 코드 리뷰 — CENTURION_DAY#234 데모/운영 연결 구분 없앰

너는 이 작업의 day reviewer 워커다(앞서 seed_demo_board 를 리뷰한 세션). 같은 규칙(원 브리프 `/Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck/orchestration/work/day-procedure-board-2/day-procedure-board-2-review-brief.md` §5 · §7 — 읽기만 · 코드 수정 · 커밋 금지 · KOS 호출 · 공유 DB 금지).

워크트리: `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-procedure-board-2` — `git diff`(추적 파일 23개). 미추적 seed_demo_board.py · tests/scripts 는 이미 리뷰 PASS — 이번 대상 밖.

## SSOT
- Delivery #234 v2(승인됨): `gh issue view 234 --repo MediSolveAIDev/CENTURION_DAY` — 바뀌는 것 · 하지 않는 것 · A1~A5
- 스펙 PR #920 워크트리 `/Users/kknaks/orca/workspaces/mediness-mediness/day-procedure-board-2-spec/products/day/20-spec/` (SPEC-000 · 001 · 002 개정)
- 자리 전수 `/Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck/orchestration/work/day-procedure-board-2/research-demo-vs-live-report.md` §1 · §3
- 사용자 결정: `is_demo` 칸은 **표시 데이터로 남고 어떤 코드도 그 값으로 동작을 가르지 않는다** · 데모/운영 · dev/prod 가 같은 코드로 같게 동작

## 볼 것
1. 동작 분기 0: `git grep -n -E 'is_demo|app_env|APP_ENV|trial|demo|live'` 을 backend/day 에 돌려 남은 분기를 전부 판정 — 칸 · 모델 · 시드 · 테스트 외에 is_demo 로 가르는 자리 0, APP_ENV 로 연결을 거르는 자리 0. 남은 APP_ENV 쓰임(/dev/kit · /docs · 스키마 짝)은 Non-Goals 라 OK
2. 다른 not-supported 경로(시스템 계정 없음 · 표에 없는 flow step · 알 수 없는 write · writer 미설정)가 살아 있나 — 조용히 열려 버린 쓰기 없나(`OPEN_STEPS = KOS_STEPS 세 값` 이 의도한 것만인지 · write_open 이 경로+값으로 여전히 막는지)
3. outbox: 예전 trial 거절로 failed(NOT_SUPPORTED) 된 행 · 큐 처리에 회귀 없나
4. auth: 로그인 후보 · 다시 고르기에서 app_env 를 뺀 뒤 다른 조건(끊긴 연결 · 꺼진 병원 · 소속 테넌트)이 그대로인가
5. 테스트가 A1~A3 을 실제로 막나 — 특히 새 `test_cc_근거_쓰기는_데모_실제_병원_연결에서_같은_op_을_쌓는다` · test_emr_sync_service · test_auth_api(이 셋은 infra 라 지금 못 돌림 — 코드로 읽고 판정)
6. 화면 · API 계약 · 문구 변경 0
7. `uv run pytest -q -m 'not infra'` · ruff 1회

## 산출물
리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/cc-2ck/orchestration/work/day-procedure-board-2/review-234-report.md` · 판정 FAIL / WARN / PASS · 지적마다 파일:줄 + 근거. 「조용히 통과하는 자리」 따로. 완료 보고는 원 브리프 §9 두 명령, 코디 핸들 `term_b915fb18-742f-4779-962c-79848020b8d5`.
