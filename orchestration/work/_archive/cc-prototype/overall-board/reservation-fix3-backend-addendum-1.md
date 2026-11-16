# backend WP-FIX3 추가 지시 1 (코디 · 2026-10-27)

review-doc r3 처분(`reservation-review-doc-r3-dispositions.md`) 중 backend 몫:
- **W1**: 저장 대상 = 요청 `noticeId`(행 id → `kos_id`)가 저장 직전 다시 읽은 KOS 목록에 있으면 그것 · 없으면 KOS 응답 첫 번째 · 그것도 없으면 create(빈 값이면 호출 없음). 시험 1개 더함(같은 날 둘 — 화면이 고른 것을 고친다)
- **W2-2**: `event_log(notice_save).noticeId` = 저장 뒤 다시 읽은 행의 ccc id(create = 새 행 · delete = 지운 행) — 지금 그렇지 않으면 맞춘다
- 호출 없음 = event_log 없음(지금 그대로)
검증 `ruff` · `pytest` 다시. 데모 재호출은 필요 없음. 보고서에 「추가 지시 1」 절 + 같은 두 명령.
