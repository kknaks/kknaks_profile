# [backend] WORK-009 Phase 1 — 재검수 W5 (fix2, 작음)

리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진-고도화-3/orchestration/work/strong-hajin-polish2/review-be-p1b-report.md` W5. 코디 판단: 이번 판에 고친다, 권장대로.
1. 서버가 `attachment_draft_ids` 를 **중복 제거 + 정렬**해 정규화한다(`payloads.py:84`) — 순서만 다른 같은 집합은 같은 회차·같은 영수증
2. draft 없는 confirm·save 에 `attachment_draft_ids` **키가 없으면 최신 스냅샷의 자료 목록**을 쓴다(draft 생략 = 최신 스냅샷과 같은 결). 키가 있고 빈 목록이면 지금처럼 빈 목록
3. 계약 테스트 2(순서 다른 같은 집합 → 회차 그대로 / 키 없는 confirm → 저장 회차 자료로 업무 생성, 회차 그대로)
검증 test-unit · test-contract. 2채널 보고 subject 「backend 완료: WORK-009 Phase 1 fix2」(코디 term_b2ea0fd5-1473-4b83-9a04-dcf769fbedba).
