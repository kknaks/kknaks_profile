# [mobile] 직원 앱 내부 채팅 — 코드 리뷰 r1 수정 (FAIL 1 · WARN 1)

역할 · SSOT · allowed_paths(`procedure/app/` 만) · 하지 말 것(커밋 · 시뮬레이터 · 기기 금지) · 완료 보고(§9 두 명령)는 **앞 브리프 `/Users/kknaks/orca/workspaces/kknaks_profile/cc-내부채팅/orchestration/work/internal-chat/internal-chat-app-brief.md` 그대로**다. 먼저 그 브리프와 역할 문서를 읽어라. subject 「mobile 수정 r1 완료: …」.

작업 워크트리: `/Users/kknaks/orca/workspaces/cc-prototype/internal-chat` (앞 mobile 워커의 미커밋 변경이 그대로 있다 — 이어서 고친다)

리뷰: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-내부채팅/orchestration/work/internal-chat/review-code-r1.md` (FAIL-1 · WARN-1 의 근거 · 재현 · 고칠 것을 그대로 따른다)

## 고칠 것
1. **FAIL-1** `app/lib/chat/chat_state.dart:516` 근처 — 삭제 뒤 `_onDeleted` 가 `DateTime.now().toIso8601String()`(오프셋 없는 로컬 시각)을 `updatedAt` 으로 넣어 `since` 가 9시간 미래가 된다. 앱이 만든 시각을 `since` 원천에 섞지 않는다 — `since` 는 **서버가 준 `updatedAt` 만**으로 고른다(삭제 SSE · DELETE 응답에 서버 값이 있으면 그것, 없으면 그 메시지의 `updatedAt` 을 바꾸지 않는다). 리뷰가 다른 방법을 권하면 그것도 된다. 시험 1개: 삭제 뒤 `since` 쿼리 값 = 서버가 준 가장 늦은 `updatedAt`
2. **WARN-1** `chat_state.dart:589` — 로그아웃 상태에서 채팅 푸시를 눌러 로그인하면 `chat.clear()` 가 `openRequest` 를 지워 그 방이 안 열린다. 계정이 바뀌어도 **푸시로 들어온 열기 요청은 남긴다**(새 계정이 그 방의 멤버가 아니면 SPEC 대로 토스트). 시험 1개

## 검증
`cd procedure/app && /Users/kknaks/fvm/versions/3.44.8/bin/flutter analyze && /Users/kknaks/fvm/versions/3.44.8/bin/flutter test` 각 1회
