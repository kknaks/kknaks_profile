# [reviewer_doc] 직원 앱 내부 채팅 — SPEC-007 0.4.0 · WORK-011 r4 문서 검수

역할 · SSOT · allowed_paths · 하지 말 것 · 완료 보고(§9 두 명령)는 **앞 브리프 `/Users/kknaks/orca/workspaces/kknaks_profile/cc-내부채팅/orchestration/work/internal-chat/internal-chat-review-doc-brief.md` 그대로**다. 먼저 그 브리프와 역할 문서를 읽어라. 생성 1개만: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-내부채팅/orchestration/work/internal-chat/review-doc-r4.md` (subject 「reviewer_doc r4 완료: …」).

## 바뀐 것
- DEC-009 D-58 ~ D-66 (전달 D-62 ~ D-64 · 통역 드로어 D-65 · 파일 삭제 읽는 법 D-66)
- SPEC-007 0.3.0 → 0.4.0 (`(r4)`) · SPEC-004 §6.5 한 줄 · WORK-011 (BE4 ∥ APP6 → REVIEW3 → SIM2 → DEPLOY13 → E2E2)
- planner 리포트 `spec-r4-report.md` (OQ-957 ~ 961 은 코디 기본값으로 받음 — FAIL 로 잡지 마라)
- 운영에 나간 코드 = 코드 워크트리 `/Users/kknaks/orca/workspaces/cc-prototype/internal-chat` HEAD `216b154`(= main 머지 a6c4123) · 읽기만

## 볼 것 (코드 워커가 막힐 빈칸만 FAIL)
1. **전달 계약** `POST /api/chat/messages/{id}/forward`: 요청 · 응답(대상별 결과) · 권한(원본 방 멤버 · 대상 방 멤버 · 비활성 1:1) · 1:1 새로 만들기 · `clientId` 중복 방지(대상마다) · 첨부 새 행 + 같은 파일 · **D-66 파일 지우기(참조 셈)가 지금 삭제 코드(216b154)와 맞게 구현 가능하게 적혔나** · SSE · 푸시 · 경로 70 · 오류 코드
2. 전달 시트 화면(검색 · 초성 · 칩 · 목록 규칙 · 10곳 · [전송] · 결과 토스트 · 일부 실패) · 아이패드
3. 시스템 공유 · share_plus 걷어냄이 SPEC 전체에서 일관되나(남은 「공유 시트」 · 「저장 빼기」 문장 = FAIL)
4. 처분 23줄 동기가 실제로 들어갔나 (표본 말고 전부)
5. D-65 통역 드로어: SPEC-004 §6.5 · SPEC-007 · WORK 에 고칠 자리(`lib/widgets/interpret_drawer.dart:192-193`)와 완료 조건이 있나
6. §12.3 을 216b154 에서 직접 grep 해 확인
