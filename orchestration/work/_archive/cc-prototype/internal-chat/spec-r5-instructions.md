# [planner] 직원 앱 내부 채팅 — SPEC-007 0.5.0 · WORK-011 r5 (사진 모아보기 · 초대 · 들어온 뒤 대화만 · 동기)

역할 · allowed_paths · 하지 말 것 · 완료 보고(§9 두 명령)는 **앞 브리프 `/Users/kknaks/orca/workspaces/kknaks_profile/cc-내부채팅/orchestration/work/internal-chat/internal-chat-spec-brief.md` 그대로**다. 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/cc-내부채팅/orchestration/work/internal-chat/spec-r5-report.md` (subject 「planner r5 완료: …」).

## 무엇이 바뀌었나
- 운영 코드 = main `b988f21`(PR #18) · 코드 워크트리 `/Users/kknaks/orca/workspaces/cc-prototype/internal-chat` 브랜치 `kknaksss/internal-chat-invite` HEAD `3ed1089`(F10 정렬 커밋 포함 · 읽기만). §12 는 3ed1089 기준 grep
- DEC-009 **D-67 · D-68 · D-69**(코디가 더함 · 사용자 승인): 사진 · 동영상 모아보기 · 초대(1:1 → 새 그룹 · 문구) · 들어온 뒤 대화만(D-12 뒤집음)
- 사용자 피드백 `sim-feedback.md` F10 · F11 · F13 · F14 (F12 안 함)
- **동기할 처분**(코드에만 있음): `r4-dispositions.md` · `app-fix-r4-instructions.md`(공용 시트 `showAppSheet` · 보내는 중 닫힘) · `be-fix-r4-instructions.md`(전달 쓰기 잠금) · `app-fix-r5-instructions.md`(F10 정렬)

## 할 것
1. **SPEC-007 0.4.0 → 0.5.0** · `(r5)` · 머리 변경 표
   - 동기: 위 처분 전부
   - D-67: 방 첨부 목록 API(모양 · 페이지 · 정렬 · 권한 · D-69 적용) · 방 정보 화면 줄 · 격자 화면 · 빈 상태 · 아이패드
   - D-68: [참여자 추가] → [초대] · 1:1 [초대] = 새 그룹 만들기(지금 `POST /api/chat/rooms` 를 쓰나 새 경로인가 — 근거와 함께 · 같은 사람 묶음이어도 새 방 D-08) · 시스템 줄 문구 「A님이 B님을 초대했습니다」(기존 「…을 초대했어요」 대체 · 옛 행 그대로 둘지) · 1:1 안내 줄 없앰
   - D-69: 「들어온 시각」 정의(`joined_at` — 처음 · 다시 초대 · 방 만들 때) · 걸러야 하는 **모든 읽기 길을 코드에서 전수**(메시지 목록 · since · 방 목록 미리보기 · 안 읽음 · 사진/동영상/썸네일 열기 · 전달 원본 · 모아보기 · SSE 는 이미 멤버만?) · 경계(같은 밀리초) · 시험
2. **WORK-011**: WP-BE5 ∥ WP-APP7 → REVIEW4 → 시뮬레이터 → 배포 · TestFlight 빌드 14
3. README · log · DEC 안 고침

## 검증 (앞 브리프 §8 + 아래)
- DEC D-01 ~ D-69 → SPEC 빠짐 0 · 뒤집힌 D-11 문구 · D-12 · D-02 일부 표시
- D-69 읽기 길 전수 표(파일:줄 · grep 명령 · 수)
