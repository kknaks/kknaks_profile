# [reviewer_doc] 직원 앱 내부 채팅 — SPEC-007 0.2.0 · WORK-011 문서 검수 r2

역할 · SSOT · allowed_paths · 하지 말 것 · 완료 보고(§9 두 명령)는 **앞 브리프 `/Users/kknaks/orca/workspaces/kknaks_profile/cc-내부채팅/orchestration/work/internal-chat/internal-chat-review-doc-brief.md` 그대로**다. 먼저 그 브리프와 역할 문서를 읽어라. 생성 1개만: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-내부채팅/orchestration/work/internal-chat/review-doc-r2.md` (subject 「reviewer_doc r2 완료: …」).

## 바뀐 것
- DEC-009 에 D-38 ~ D-44(r1 처분 · 사용자 결정 2 + 코디 기본값)
- SPEC-007 0.1.0 → 0.2.0 (바뀐 줄 끝 `(r2)` · 머리 변경 표) · WORK-011 · SPEC-004 §6.8 두 줄 더
- planner 처분 대조: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-내부채팅/orchestration/work/internal-chat/spec-r2-report.md`
- 코디가 기본값으로 받은 것: OQ-932(안 읽음 = 메시지 id 기준 — D9-20 의 뜻을 바꾸지 않는 구현 수단) · OQ-933(배너는 셸 안 — 알림 목록 · 사진 크게 보기 위에서는 안 보임) · OQ-939(비활성 1:1 보내기 서버 409 `chat_peer_inactive`)

## 볼 것
1. **r1 FAIL 4 · WARN 17 이 실제로 닫혔나** — 하나씩 SPEC · WORK 줄을 열어 확인(리포트 대조표를 믿지 말고). 닫힘 / 덜 닫힘 / 안 닫힘
2. **r2 가 새로 만든 문제** — 특히 밀리초 시각 · `since >=` · `last_read_message_id` 계약이 back · app 양쪽에서 추측 없이 구현되나(필드 · 타입 · 경계 · 시험), 배너 층 · 숨김 세 길이 코드 자리와 맞나, `async def` 경로 목록이 빠짐없나
3. D-38 ~ D-44 반영 · DEC 44/44
4. 새 §12 자리 18개를 코드에서 직접 확인
5. 「지금 원천」 밖의 가상 상황으로 FAIL 을 만들지 않는다. 취향 지적 금지

판정이 PASS 또는 WARN 만이면 코드 발주로 간다. 그래서 **코드 워커가 막힐 빈칸**만 FAIL 로 둔다.
