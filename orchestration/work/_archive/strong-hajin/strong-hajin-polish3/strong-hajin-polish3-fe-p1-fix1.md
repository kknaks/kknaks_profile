# [frontend] WORK-010 Phase 1 fix1 — 검수 WARN 처리

검수 `review-fe-p1-report.md`(같은 폴더) WARN 4. 코디 답:
- **W1** `MeetingTitle.test.tsx:175` 「응답을 세운다」 단언을 **서버 응답 값으로만 통과하게**(예: 응답 제목을 입력과 다른 값으로 돌려주고 그 값이 보이는지) 고친다
- **W2** `saveTitle` 연타 방지(`claim("title")`) 테스트 1건 추가 — 저장 중 두 번째 저장이 요청을 안 보낸다
- **W3** `screens-a.css:71` `.login-brand p` 죽은 규칙 삭제(다른 사용처 grep 0 확인)
- **W4** 긴 제목 줄바꿈 차이 — **이번엔 고치지 않는다**(사용자 E2E 2루프에서 본다). 보고에만 남김
범위·allowed_paths·하지 말 것은 Phase 1 브리프 그대로. 검증: 바뀐 테스트 파일 + `npx tsc --noEmit`. 리포트 `fe-p1-worker-report.md` 끝에 「fix1」 절 덧붙임. 완료 보고는 같은 두 채널(subject 「frontend 완료: WORK-010 Phase 1 fix1」).
