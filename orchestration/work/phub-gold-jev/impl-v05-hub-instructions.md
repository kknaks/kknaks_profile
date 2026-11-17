# [backend] 허브 구현 — WORK-005(SPEC-001 0.5.1)

**너는 앞 판의 맥락이 없다.** `phub-gold-jev-be-brief.md`(같은 폴더) 전체를 읽어라 — 역할 · SSOT · allowed_paths(`backend/`) · 제약 · §8 검증 · §9 완료 보고 그대로. 워크트리 `/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-gold-jev`(앞 판 미커밋 위에 이어서).

**이번 일 = `WORK-005-hub-v05.md`(같은 폴더) WP-1 ~ WP-4 전부.** 계약 = `SPEC-001-hub-gold-mcp.md` 0.5.1. 검수 `review-work-v05.md` · `_RESUME.md` §2 맨 위 행(코디 결정 W-1~W-5) 반영.
- 확인 서버는 **18106** 에서 띄웠다 내림 · 18105 는 코디 것(건드리지 마라 — 끝나면 코디가 재시작).
- 앱 워커가 병행 중이다(clinic_chat) — 응답 꼴(resolve 맞춤 · coverage)은 WORK-005 에 고정된 꼴 그대로. 바꿔야 하면 코디에게 먼저 `[질문] backend:`.
- 기준선: 데이터 env 전체 pytest 568 passed · 2 skipped 를 깨지 마라.
