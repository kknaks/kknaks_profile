# [backend] 직원 앱 내부 채팅 — WORK-011 WP-BE5 (모아보기 #20 · 초대 문구 · 들어온 뒤 대화만)

역할 · allowed_paths(`procedure/back/`) · 하지 말 것(커밋 · 서버 · compose · `procedure/app` 금지) · 검증 · 완료 보고(§9 두 명령)는 **`/Users/kknaks/orca/workspaces/kknaks_profile/cc-내부채팅/orchestration/work/internal-chat/internal-chat-be-brief.md` 그대로**다. subject 「backend BE5 완료: …」.

작업 워크트리: `/Users/kknaks/orca/workspaces/cc-prototype/internal-chat` 브랜치 `kknaksss/internal-chat-invite`(HEAD 3ed1089 · 커밋 금지). ⚠ mobile 이 `procedure/app` 에서 병렬 — 건드리지 마라.

## SSOT (이기는 순)
1. 코디 처분(있으면) `/Users/kknaks/orca/workspaces/kknaks_profile/cc-내부채팅/orchestration/work/internal-chat/r5-dispositions.md`
2. `/Users/kknaks/orca/workspaces/kknaks_profile/cc-내부채팅/para/projects/summer-star/cc-prototype/20-spec/spec-007-internal-chat.md` **0.5.0** `(r5)` — §4.6 읽기 길 V1 ~ V12 · #20 · §4.7 · §13.1 r5 · WORK-011 **WP-BE5**
3. DEC-009 D-67 ~ D-69 · OQ-962 ~ 969 기본값
4. `review-doc-r5.md` 조용히 통과하는 자리

## 주의
- **D-69 거름은 V 표의 길마다 HTTP 시험**(들어오기 전 메시지 · 첨부 · 썸네일 · 전달 원본 · 모아보기 · since · 미리보기 · 안 읽음 · SSE 받는 사람). 거름을 하나 빼면 시험이 깨지는지(mutation) 한 번 확인
- 옛 DB 채우기(`from_message_id`) 마이그레이션 시험

## 검증
WP-BE5 부분 명령 → 마지막 `uv run ruff check . && uv run pytest -q` 1회 · 라우트 핸들러 `def` = 0 · `test_route_count_71`
