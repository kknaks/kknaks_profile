# [frontend] 고침 1 — 코드 검수 1차(`review-code-1-report.md` 이 폴더) FE 몫

⚠ 워크트리는 코디가 **origin/dev `3543d8b2`(#298) 위로 옮겼다**(변경 미커밋 그대로 · `day.css` 는 코디가 다시 빌드함). backend 가 같은 워크트리에서 BE 몫을 동시에 고친다 — backend 파일 건드리지 마라.

- **F1(FE 쪽)** 실패 줄 [다시 시도]에서 `data-day-rq-lock` 을 뗀다(backend 는 실패면 `pending_write_id` 를 비우도록 바꾸는 중). 화면 테스트를 **서버가 실제로 만드는 조합**(실패 = `action="failed"` · 보내는 중 = `pending_write_id` 있음)으로 고친다.
- **W5** `rqSent` 가 켜져 있으면 입력 칸 글을 떠 두지 않는다(보낸 글이 다시 차오르지 않게).
- **W12** 3열 변경 요청 배지도 「답변 대기중」으로 통일(사용자 문구 · `test_screen_copy` 근거 「사용자 11-26」).
- 검증: 네 화면 테스트 · `test_screen_copy` · lint 류 1회 · CSS 를 다시 빌드했다면 `scripts/build-css.sh`.

완료 보고 = 브리프 §9 두 명령 · subject `frontend 완료: 고침 1`.
