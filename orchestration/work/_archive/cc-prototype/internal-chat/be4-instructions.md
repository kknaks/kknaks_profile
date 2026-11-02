# [backend] 직원 앱 내부 채팅 — WORK-011 WP-BE4 (앱 안 전달 API)

역할 · allowed_paths(`procedure/back/`) · 하지 말 것(커밋 · 서버 · compose · `procedure/app` 금지) · 검증 · 완료 보고(§9 두 명령)는 **앞 브리프 `/Users/kknaks/orca/workspaces/kknaks_profile/cc-내부채팅/orchestration/work/internal-chat/internal-chat-be-brief.md` 그대로**다. 먼저 그 브리프 · 역할 문서를 읽어라. subject 「backend BE4 완료: …」.

작업 워크트리: `/Users/kknaks/orca/workspaces/cc-prototype/internal-chat` — 브랜치 `kknaksss/internal-chat-forward`(운영 main `a6c4123` 에서 새로 땀 · 커밋 금지).
⚠ mobile 워커가 같은 워크트리 `procedure/app/` 에서 병렬 작업 중 — 건드리지 마라.

## SSOT (이기는 순)
1. 코디 처분(있으면) `/Users/kknaks/orca/workspaces/kknaks_profile/cc-내부채팅/orchestration/work/internal-chat/r4-dispositions.md`
2. `/Users/kknaks/orca/workspaces/kknaks_profile/cc-내부채팅/para/projects/summer-star/cc-prototype/20-spec/spec-007-internal-chat.md` **0.4.0** `(r4)` 줄 — 전달 API #19 · §5 · §6 · §9 · §13.1 · WORK-011 **WP-BE4** 행
3. `/Users/kknaks/orca/workspaces/kknaks_profile/cc-내부채팅/para/projects/summer-star/cc-prototype/10-decision/decision-009-internal-chat.md` D-62 ~ D-64 · **D-66**(파일 = 마지막 참조 메시지와 함께 지움 — 지금 삭제 코드를 이 규칙으로 바꾼다 · 원본을 지워도 전달본이 열리는 시험)
4. 리뷰 `review-doc-r4.md` 「조용히 통과하는 자리」 — HTTP 경로 시험으로

## 검증
WP-BE4 부분 명령 1회 → 마지막 `cd procedure/back && uv run ruff check . && uv run pytest -q` 1회 · 라우트 핸들러 `def` = 0 · `test_route_count_70`
