# [reviewer] review-code-2 — 2루프 코드 검수 (read-only)

너는 앞 맥락이 없다. 먼저 읽어라:
1. 원 브리프 `/Users/kknaks/orca/workspaces/kknaks_profile/day-fix-feedback/orchestration/work/fix-feedback/fix-feedback-review-brief.md` — 역할 · read-only · 검증 그대로.
2. 앞 검수 `…/fix-feedback/review-code-1-report.md` · 2루프 지시 `be-2-instructions.md` · `fe-2-instructions.md` · 결과 `be-2-report.md` · `fe-2-report.md`.
3. 결정 정본 `…/fix-feedback/e2e-feedback.md`(F-5 · E2 · E3 · E5 · E6) · `_RESUME.md` §2 · 스펙 `/Users/kknaks/orca/workspaces/mediness-mediness/fix-feedback-spec/products/day/20-spec/spec-002-procedure-board.md` 개정 ㉒ · `spec-005-notifications.md` 2차 개정. **호출 취소 알림 · 새 알림 종류 · migration · KOS 쓰기는 없어야 한다**(사용자 결정 — SPEC-005 :444 의 migration 문장은 옛 문장).

리뷰 대상: `/Users/kknaks/orca/workspaces/CENTURION_DAY/fix-feedback` 미커밋 diff 전체(1루프 + 2루프).

## 볼 것
1. 2루프 결정 각각이 코드와 맞나(파일:줄): F-5 ⋮(준비중 · 수락 줄 없음 · 호출 → 호출 취소 · 진행중 · 완료 그대로) · `cancel_call` 규칙 38 · 검사 순서 · 저장(deleted_at · closed_at) · event_log · KOS outbox 0 · 알림 행 0 · E3 「간호관리」 + 원장 변경 똑같이 · E6 이름 글자만 · 호버 「차트 작성」 · 나머지 클릭 안 열림 · E5 늘 띄움 · W2 고침 · E2 원인 · 수정(`.day-opt` · `.day-pick` — 다른 팝오버 회귀).
2. 1루프 W 들이 해소됐나(W1 infra · W2 · W7 · W9 상태).
3. 앱 영향 — `routers/api/` · 앱 스냅샷 모양: 더한 칸(`systemDoctor`)뿐인가.
4. 테스트 — `pytest -m "not infra"` 1회 직접. (infra 는 코디가 따로 — Docker 컨테이너 건드리지 마라.)
5. 「조용히 통과하는 자리」 · E2E 2회차에서 사용자가 만날 자리.

리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/day-fix-feedback/orchestration/work/fix-feedback/review-code-2-report.md` — 판정 PASS/WARN/FAIL · 지적 파일:줄. 완료 보고는 preamble 의 worker_done.
