# [reviewer] 직원 앱 내부 채팅 — 코드 검수 r2 (2판: BE3 · APP4 · APP5)

역할 · allowed_paths(read-only · 리포트 1개) · 하지 말 것 · 완료 보고(§9 두 명령)는 **앞 브리프 `/Users/kknaks/orca/workspaces/kknaks_profile/cc-내부채팅/orchestration/work/internal-chat/internal-chat-review-brief.md` 그대로**다. 먼저 그 브리프 · 역할 문서를 읽어라. 생성 1개만: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-내부채팅/orchestration/work/internal-chat/review-code-r2.md` (subject 「reviewer 코드 r2 완료: …」).

## 대상
코드 워크트리 `/Users/kknaks/orca/workspaces/cc-prototype/internal-chat` 의 **`0f0d969` 이후 미커밋 변경**(`git diff 0f0d969` · `git status`) — backend BE3(수정 · 동영상 90MB · Range · 썸네일 · 경로 69 · pytest 515) · mobile APP4 · APP5(입력창 · [+] 시트 · 여러 개 · 네이티브 동영상 변환 `AppDelegate.swift` · 5메뉴 · 공유 · 수정 · 링크 · test 210). 코디가 두 수치 다시 돌려 확인함.

## SSOT (이기는 순)
1. `/Users/kknaks/orca/workspaces/kknaks_profile/cc-내부채팅/orchestration/work/internal-chat/r3-dispositions.md` (SPEC 보다 이김)
2. SPEC-007 0.3.0 `(r3)` 줄 · WORK-011 WP-REVIEW2 행 · DEC-009 D-45 ~ D-59
3. `/Users/kknaks/orca/workspaces/kknaks_profile/cc-내부채팅/orchestration/work/internal-chat/review-doc-r3.md` 「조용히 통과하는 자리」 · 「실물 자리」
4. 사용자 피드백 `sim-feedback.md` (입력창 · [+] 시트 = 카톡 꼴)

## 볼 것
- 새 API · SSE `chat_message_edited` · 동영상 필드를 back 과 app **양쪽**에서 대조(이름 · 타입 · 꼴)
- r3-dispositions 13줄이 코드에 있나
- 네이티브 변환 채널(`AppDelegate.swift`): 실패를 Dart 로 오류로 돌려주나 · 임시 파일 지움 · 메인 스레드 막힘 · 동시 호출 · HEVC/세로 방향(preferredTransform)
- 공유: 저장 빼기 · 임시 파일 지움 · 취소
- 「사용자가 시뮬레이터에서 만날 자리」를 따로 모아라 — 코디가 지금 시뮬레이터에 올려 사용자가 보고 있다
- 1판 회귀(원장 · 상담사 호출 · 띄우기 · 여권 · 알림 목록 · 1판 채팅)
