# [reviewer] 코드 검수 — backend P3 호출 취소 알림(커밋 9162ee18) + 통역 시험(bd93b559)

워크트리 `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-mobile-v2` · 읽기만(다른 워커 작업 중 — git 읽기만). 대상 = 커밋 `9162ee18` · `bd93b559`.

- 지시 `/Users/kknaks/orca/workspaces/kknaks_profile/day-mobile-v2/orchestration/work/day-mobile-v2/be-p3-instructions.md` · 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day-mobile-v2/orchestration/work/day-mobile-v2/be-p3-report.md`
- 스펙 `/Users/kknaks/orca/workspaces/mediness-mediness/day-mobile-v2-spec/products/day/20-spec/spec-005-notifications.md` 2026-11-20 개정(OQ-N15 ~ N19) · `/Users/kknaks/orca/workspaces/mediness-mediness/day-mobile-v2-spec/products/day/20-spec/spec-000-data-model.md` enum · `/Users/kknaks/orca/workspaces/mediness-mediness/day-mobile-v2-spec/products/day/20-spec/spec-002-procedure-board.md` 규칙 38

## 볼 것
1. **그 호출이 완전히 닫힐 때만** 한 번 · 일부 취소 = 알림 없음 · 재호출 사슬 · 받는 사람 = 원래 알림 받은 계정(설정 꺼짐 · 비활성 제외) · 제목 「호출 취소」 · 본문 「{방} · 호출 취소」(방 없으면 「방」) · 원래 행 read_at · unread
2. 커밋 뒤 훅 · worker 태스크(`call_cancel_push`) — 중복 발송 · 실패 재시도 · push_log
3. migration 0012 — enum 값 추가 up/down · alembic head 이어짐 · prod 적용 순서 위험(새 worker 태스크 이름이 같이 배포돼야 함)
4. 웹 `day.js` — NOTIFY_KIND 넓힘 · 원래 OS 알림 닫기 — 웹 다른 동작 무변경
5. bd93b559 — 옮긴 15건이 통키 시험과 같은 것을 보나
6. 관련 테스트 · ruff 1회

리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day-mobile-v2/orchestration/work/day-mobile-v2/review-code-p3-report.md` · FAIL/WARN/PASS · 파일:줄. 수정 · 커밋 금지. 완료 보고는 dispatch preamble 의 worker_done 그대로.
