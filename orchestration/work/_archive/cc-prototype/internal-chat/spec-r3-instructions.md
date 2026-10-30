# [planner] 직원 앱 내부 채팅 — SPEC-007 0.3.0 · WORK-011 r3 (시뮬레이터 피드백 F1 ~ F4 · 동기)

역할 · allowed_paths · 하지 말 것 · 완료 보고(§9 두 명령)는 **앞 브리프 `/Users/kknaks/orca/workspaces/kknaks_profile/cc-내부채팅/orchestration/work/internal-chat/internal-chat-spec-brief.md` 그대로**다. 먼저 그 브리프와 역할 문서를 읽어라. 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/cc-내부채팅/orchestration/work/internal-chat/spec-r3-report.md` (subject 「planner r3 완료: …」).

## 무엇이 바뀌었나
- **DEC-009 D-45 ~ D-57**(코디가 더함): 처음 추가 읽음 시작점 · 하이퍼링크 · 입력창 · [+] 바텀 시트 · **동영상** · **여러 개(최대 10 · 하나에 메시지 하나)** · **포맷 변환(사진 → JPEG · 동영상 → H.264 MP4 1280 · 썸네일)** · 동영상 한도 3분 · 100MB · 재생 · **길게 누르기 5메뉴** · **수정** · 공유(저장 빼기) · 볼륨
- 사용자 피드백 원문: `/Users/kknaks/orca/workspaces/kknaks_profile/cc-내부채팅/orchestration/work/internal-chat/sim-feedback.md` · 참고 스샷 설명은 D-47 · D-48
- **1판 코드가 이미 있다**(코드 브랜치 `kknaksss/internal-chat` 커밋 `0f0d969` · 워크트리 `/Users/kknaks/orca/workspaces/cc-prototype/internal-chat` · 읽기만). SPEC 은 지금 코드 위에 얹는 변경으로 쓴다 — §12 「바뀌는 코드 자리」를 **지금 코드의 파일:줄**로 다시 grep 해서 쓴다(dbf0b53 기준이 아니다)

## 할 것
1. **SPEC-007 0.2.0 → 0.3.0** · 바뀐 줄 끝 `(r3)` · 머리 변경 표
   - 동기(이미 코드에 있는 것 · 문서만 늦음): backend 브리프 §0 W2-1 ~ W2-6(`/Users/kknaks/orca/workspaces/kknaks_profile/cc-내부채팅/orchestration/work/internal-chat/internal-chat-be-brief.md` §0) · 코드 리뷰 r1 처분(`review-code-r1.md` FAIL-1 · WARN-1 — since 원천 · 푸시 열기 요청 보존) · backend 가 고른 값(1:1 비활성 이름 꼴 · 혼자 남은 이름 없는 그룹 name · 숨긴 1:1 다시 열기 · read 0 · 사진 width/height 필수 — 코드에서 확인해 그대로 SPEC 에, 기본값 표시)
   - 새 계약: D-46 ~ D-56. 특히 **표**(메시지 종류 `video` · 첨부 행에 종류 · 길이 · 썸네일 · `edited_at`) · **API**(수정 경로 · 동영상 올리기 · 열기(끊어 받기 `Range` · Bearer) · 썸네일 열기 — 경로 수 다시 셈) · **SSE**(수정 이벤트) · **푸시**(동영상 본문 「동영상」 · 수정은 푸시 없음) · **변환 규칙**(앱 쪽 · iOS 네이티브 내보내기 · 실패 시 토스트) · **한도 · 오류 코드** · **화면**(입력창 · [+] 시트 · 최근 줄 권한 · 여러 개 고르기 · 보내는 중 N개 · 동영상 말풍선 · 재생 화면 · 길게 누르기 5메뉴 · 선택 복사 · 수정 화면 · 「수정됨」 · 하이퍼링크) · **공유 시트 저장 빼기**(iOS `excludedActivityTypes` 류 — 플러그인으로 안 되면 네이티브 채널) · 시험 · 실기기 E2E 시나리오 추가
   - 시안 밖 화면이 생긴다(입력창 · [+] 시트 · 메뉴 · 재생) → 「시안과 다른 곳」 표에 「D9-47 ~ D9-56 · 사용자 스샷 기준 · 기존 위젯 · 테마로」
2. **WORK-011** 에 새 WP: **WP-BE3**(수정 · 동영상 저장 · 끊어 받기 · 썸네일 · 한도 · 경로 수 · SSE · 푸시) ∥ **WP-APP4**(입력창 · [+] 시트 · 최근 줄 · 여러 개 · 포맷 변환 · 동영상 말풍선 · 재생) → **WP-APP5**(길게 누르기 5메뉴 · 선택 복사 · 공유(저장 빼기) · 수정 · 하이퍼링크) → REVIEW → 시뮬레이터 → E2E. 대상 파일 · 완료 조건 · 부분 검증 명령. **infra**: 동영상 저장 용량(D-57 · OQ-931) — 코디 확인 단계를 WP-E2E 앞에
3. SPEC-004 는 고치지 않는다 · README · log 한 줄 · DEC-009 는 고치지 않는다

## 검증 (앞 브리프 §8 + 아래)
- DEC D-01 ~ D-57 → SPEC 대조 빠짐 0 (부록 A) · 뒤집힌 D-03 · D-15 일부 · 바뀐 곳 표시
- sim-feedback F1 ~ F4 → SPEC 절 대조
- §12 를 지금 코드(0f0d969)에서 다시 grep — 명령과 수
- 패키지 후보(동영상 고르기 · 변환 · 재생 · 공유 · 링크)는 **pub.dev 공식 문서로 iOS 지원 · 기능을 확인**해 근거 URL 을 달고, 못 하는 것은 네이티브 채널로 적는다. 결정하지 말고 후보 + 권장 1개
