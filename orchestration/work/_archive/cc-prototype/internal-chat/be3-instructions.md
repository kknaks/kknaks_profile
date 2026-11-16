# [backend] 직원 앱 내부 채팅 — WORK-011 WP-BE3 (수정 · 동영상 · Range · 썸네일)

역할 · allowed_paths(`procedure/back/`) · 하지 말 것(커밋 · 서버 · compose · `procedure/app` 금지) · 검증 · 완료 보고(§9 두 명령)는 **앞 브리프 `/Users/kknaks/orca/workspaces/kknaks_profile/cc-내부채팅/orchestration/work/internal-chat/internal-chat-be-brief.md` 그대로**다. 먼저 그 브리프 · 역할 문서를 읽어라. subject 「backend BE3 완료: …」.

작업 워크트리: `/Users/kknaks/orca/workspaces/cc-prototype/internal-chat` — 1판이 커밋 `0f0d969` 로 있다. 그 위에 이어서 짓는다(커밋 금지).
⚠ mobile 워커가 같은 워크트리 `procedure/app/` 에서 병렬 작업 중 — 건드리지 마라.

## SSOT (이기는 순)
1. **`/Users/kknaks/orca/workspaces/kknaks_profile/cc-내부채팅/orchestration/work/internal-chat/r3-dispositions.md`** (코디 처분 — SPEC 보다 이김 · 동영상 90MB)
2. `/Users/kknaks/orca/workspaces/kknaks_profile/cc-내부채팅/para/projects/summer-star/cc-prototype/20-spec/spec-007-internal-chat.md` **0.3.0** (`(r3)` 줄) · `/Users/kknaks/orca/workspaces/kknaks_profile/cc-내부채팅/para/projects/summer-star/cc-prototype/30-work/work-011-internal-chat.md` **WP-BE3 행**
3. `/Users/kknaks/orca/workspaces/kknaks_profile/cc-내부채팅/para/projects/summer-star/cc-prototype/10-decision/decision-009-internal-chat.md` D-45 ~ D-59
4. 리뷰 `/Users/kknaks/orca/workspaces/kknaks_profile/cc-내부채팅/orchestration/work/internal-chat/review-doc-r3.md` 의 「조용히 통과하는 자리」 — 전부 **HTTP 경로 시험**으로 막는다

## 검증
WP-BE3 부분 명령 1회 → 마지막 `cd procedure/back && uv run ruff check . && uv run pytest -q` 1회 · 라우트 핸들러 `def` = 0 · 경로 수 시험 = 새 수 · §13.1 r3 줄 → 시험 이름 표
