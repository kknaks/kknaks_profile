# [reviewer] 코드 검수 — backend P2(커밋 e96b0718)

워크트리 `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-mobile-v2` · 읽기만(다른 워커가 같은 워크트리에서 작업 중 — git 읽기만). 대상 = 커밋 `e96b0718`.

- 지시 `/Users/kknaks/orca/workspaces/kknaks_profile/day-mobile-v2/orchestration/work/day-mobile-v2/be-p2-instructions.md` · 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day-mobile-v2/orchestration/work/day-mobile-v2/be-p2-report.md`
- 스펙 `/Users/kknaks/orca/workspaces/mediness-mediness/day-mobile-v2-spec/products/day/20-spec/spec-001-login-session.md` 개정 ⑩ · `/Users/kknaks/orca/workspaces/mediness-mediness/day-mobile-v2-spec/products/day/20-spec/spec-002-procedure-board.md` 개정 ㉕(OQ-77 · 78)

## 볼 것
1. 앱 `choose_device` · `POST /api/auth/device` · 데모 넘김 `read_success` — 스펙 케이스 매트릭스(만료 · 잘못된 선택 · 재차 막힘 · 비밀번호 임시 보관이 응답 · 로그 · URL 에 새지 않음)
2. quick-start JSON 응답 · 일부/전부 거절 · `can*` 3칸이 서비스 거절 규칙과 같은 판정인가(웹 템플릿과 다른 곳은 스펙 ㉕ ③대로)
3. **웹 동작 무변경** — `tests/day/web/test_board_feedback.py` 가 바뀌었다: 기대값을 바꿔 웹 동작 변화를 덮은 것인지 확인
4. 워커가 적은 구현 선택 2개(`exclude_if` 로 `exclude_none` 대체 · `device_id` JSON 별칭) — 다른 응답 모양에 부작용 없나
5. 관련 테스트 · ruff 1회

리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day-mobile-v2/orchestration/work/day-mobile-v2/review-code-p2-report.md` · FAIL/WARN/PASS · 파일:줄. 수정 · 커밋 금지. 완료 보고는 dispatch preamble 의 worker_done 그대로.
