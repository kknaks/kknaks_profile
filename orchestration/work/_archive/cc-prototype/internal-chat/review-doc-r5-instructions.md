# [reviewer_doc] 직원 앱 내부 채팅 — SPEC-007 0.5.0 · WORK-011 r5 문서 검수

역할 · SSOT · allowed_paths · 하지 말 것 · 완료 보고(§9 두 명령)는 **앞 브리프 `/Users/kknaks/orca/workspaces/kknaks_profile/cc-내부채팅/orchestration/work/internal-chat/internal-chat-review-doc-brief.md` 그대로**다. 생성 1개만: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-내부채팅/orchestration/work/internal-chat/review-doc-r5.md` (subject 「reviewer_doc r5 완료: …」).

## 바뀐 것
- DEC-009 D-67 ~ D-69 · SPEC-007 0.5.0 `(r5)` · WORK-011 r5(BE5 ∥ APP7) · planner 리포트 `spec-r5-report.md`
- 코드 = 브랜치 `kknaksss/internal-chat-invite` HEAD `3ed1089`(코드 워크트리 `/Users/kknaks/orca/workspaces/cc-prototype/internal-chat` · 읽기만)
- OQ-962 ~ 969 = 코디 기본값으로 받음(OQ-963 = [새 대화] 그룹도 초대 줄 남김) — FAIL 로 잡지 마라

## 볼 것 (코드 워커가 막힐 빈칸만 FAIL)
1. **D-69 읽기 길 V1 ~ V12 를 3ed1089 에서 직접 전수** — 빠진 길(예: SSE 받는 사람 · 푸시 본문 · 방 목록 미리보기 · 안 읽음 · 전달 원본 · 썸네일 · 모아보기 · 검색이 있으면 검색 · 알림)이 있으면 FAIL. `from_message_id` 정의(만들 때 · 처음 추가 · 다시 초대 · 옛 DB 채우기)와 경계(같은 밀리초)가 구현 가능하게 적혔나
2. #20 모아보기 API(모양 · 페이지 · 정렬 · 권한 · D-69) · 화면
3. D-68 초대 — 1:1 [초대] = 기존 `POST /api/chat/rooms` 로 되나(같은 사람 묶음이어도 새 방 · 시스템 줄 · 1:1 그대로) · 문구 바뀜이 시험 · 앱 쪽 전부에 적용되나 · 옛 「초대했어요」 행 처리
4. 처분 4문서 동기 들어갔나
5. §12.4 를 3ed1089 에서 grep 확인
