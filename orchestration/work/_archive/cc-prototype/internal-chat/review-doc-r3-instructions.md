# [reviewer_doc] 직원 앱 내부 채팅 — SPEC-007 0.3.0 · WORK-011 r3 문서 검수

역할 · SSOT · allowed_paths · 하지 말 것 · 완료 보고(§9 두 명령)는 **앞 브리프 `/Users/kknaks/orca/workspaces/kknaks_profile/cc-내부채팅/orchestration/work/internal-chat/internal-chat-review-doc-brief.md` 그대로**다. 먼저 그 브리프와 역할 문서를 읽어라. 생성 1개만: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-내부채팅/orchestration/work/internal-chat/review-doc-r3.md` (subject 「reviewer_doc r3 완료: …」).

## 바뀐 것
- DEC-009 D-45 ~ D-57 (시뮬레이터 피드백 F1 ~ F4 · `sim-feedback.md`)
- SPEC-007 0.2.0 → 0.3.0 (`(r3)` 표시) · WORK-011 (BE3 ∥ APP4 → APP5 → REVIEW2 → SIM · INFRA → E2E)
- planner 리포트 `spec-r3-report.md`
- **1판 코드가 있다**: 코드 워크트리 `/Users/kknaks/orca/workspaces/cc-prototype/internal-chat` 커밋 `0f0d969`(읽기만). §12.2 r3 의 파일:줄은 이 커밋 기준이다

## 코디가 받은 기본값 (FAIL 로 잡지 마라)
OQ-940 ~ OQ-956 은 코디 기본값으로 받는다. 특히 OQ-956(공유 시트용 임시 파일 · 시트 닫히면 지움)은 D9-56 의 결과로 받는다.

## 볼 것
1. D-45 ~ D-57 · F1 ~ F4 가 SPEC 에 맞게 옮겨졌나(뒤집힌 D-03 · D-15 일부가 SPEC 전체에서 일관되게 바뀌었나 — 옛 「영상 없음」 · 「1장」 · 「수정 없음」 문장이 남아 있으면 FAIL)
2. 새 계약(수정 PATCH · 동영상 올리기 · Range 열기 · 썸네일 · SSE `chat_message_edited` · 오류 코드 · 경로 69)이 backend · mobile 이 서로 묻지 않고 구현할 만큼 다 있나 — 필드 · 타입 · 한도 · 경계 · 권한 · 시험
3. 앱 변환(JPEG · H.264 MP4 1280 · 썸네일) · 여러 개 하나씩 · 공유 저장 빼기(share_plus excludedCupertinoActivities) · 링크 · 5메뉴 · 선택 복사 — 화면 · 상태 · 실패 처리가 다 있나
4. §12.2 를 0f0d969 에서 직접 grep 해 전부 확인 · 빠진 자리
5. WORK-011 새 WP 의 순서 · 병렬 · 대상 파일 · 완료 조건 · 검증 명령
6. 코드 워커가 막힐 빈칸만 FAIL. 취향 · 가상 상황 금지
