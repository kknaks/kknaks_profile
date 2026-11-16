# [planner] 직원 앱 내부 채팅 — SPEC-007 0.4.0 · WORK-011 r4 (앱 안 전달 · 동기)

역할 · allowed_paths · 하지 말 것 · 완료 보고(§9 두 명령)는 **앞 브리프 `/Users/kknaks/orca/workspaces/kknaks_profile/cc-내부채팅/orchestration/work/internal-chat/internal-chat-spec-brief.md` 그대로**다. 먼저 그 브리프와 역할 문서를 읽어라. 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/cc-내부채팅/orchestration/work/internal-chat/spec-r4-report.md` (subject 「planner r4 완료: …」).

## 무엇이 바뀌었나
- **운영에 나간 코드**: 코드 레포 main 머지 `a6c4123`(PR #17) — 코드 워크트리 `/Users/kknaks/orca/workspaces/cc-prototype/internal-chat` HEAD `216b154`(읽기만). §12 「바뀌는 코드 자리」는 이 커밋 기준으로 다시 grep
- DEC-009 **D-58 ~ D-65**(코디가 더함): 동영상 90MB · infra · 입력줄 알약 · 키보드 탭바 숨김 · **공유 = 앱 안 전달(D-62 ~ D-64)** · 통역 드로어 결함(D-65)
- 사용자 피드백 `/Users/kknaks/orca/workspaces/kknaks_profile/cc-내부채팅/orchestration/work/internal-chat/sim-feedback.md` F5 · F6 · F7 · F9 (F8 취소)
- **동기할 처분**(코드에는 이미 있음 · 문서만 늦음): `r3-dispositions.md` 13줄 · `app-fix-r2-instructions.md`(리뷰 r2 WARN 7 처분) · `app-fix-r3-instructions.md`(D-60 · D-61)

## 할 것
1. **SPEC-007 0.3.0 → 0.4.0** · 바뀐 줄 끝 `(r4)` · 머리 변경 표
   - 동기: 위 처분 전부(90MB · Content-Length · 3분 규칙 하나 · 무음 스위치 · 링크 ASCII · 공유 흘려 받기 → **D-62 로 시스템 공유 자체가 없어짐 — 지우거나 취소선** · 입력줄 알약 · 키보드 · 카메라 칸 등)
   - 새 계약 **전달**: API(예: `POST /api/chat/messages/{id}/forward {targets: [{roomId}|{accountId}], clientId…}` — 모양은 네가 근거와 함께 정하고 기본값 표시) · 권한(원본 메시지 방의 지금 멤버만 · 대상 방의 지금 멤버만 · 비활성 1:1 거절) · 사진 · 동영상 파일 공유(같은 첨부 행을 가리키나 새 행인가 — **삭제(D-17)와 얽힘**: 원본을 지워도 전달본 파일은 남아야 한다 · 근거와 함께) · 한 번에 최대 10곳 · 일부 실패 응답 꼴 · SSE · 푸시는 보내기와 같음 · 경로 수
   - 화면: 전달 시트(검색 · 초성 · 칩 · 목록 · 여러 곳 · [전송] · 결과 토스트) · 5메뉴의 [공유] 이름(「공유」 그대로 · 사용자 말) · 아이패드
   - D-65 통역 드로어: SPEC-004 의 통역 드로어 절(§6.5)을 가리키는 한 줄 + SPEC-007 에는 「이 판에서 같이 고침」 줄만(SPEC-004 §6.5 높이 문장을 고친다 — SPEC-004 는 이 줄만)
2. **WORK-011** 에 **WP-BE4**(전달 API) ∥ **WP-APP6**(전달 시트 · [공유] 교체 · 시스템 공유 코드 걷어냄 · 통역 드로어) → REVIEW3 → 시뮬레이터 → 배포 · TestFlight 빌드 13 → 실기기
3. README · log 한 줄 · DEC-009 는 고치지 않는다

## 검증 (앞 브리프 §8 + 아래)
- DEC D-01 ~ D-65 → SPEC 대조 빠짐 0 · 뒤집힌 줄(D-56) 표시
- 처분 문서 3개 → SPEC 반영 대조표
- §12 를 216b154 에서 다시 grep (명령과 수)
