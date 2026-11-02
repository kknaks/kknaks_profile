# 앱 코드 리뷰 r1 수정 (코디 · 2026-10-27) — FAIL 2 · WARN 3

리뷰 `app-review-code-r1.md`. 커밋 금지 · 끝나면 보고서에 「리뷰 r1 수정」 절 + 두 명령.

## backend
- **FAIL-1**: `api/display.py:27` create 를 `async def` 로(띄우기 푸시가 이벤트 루프 없어 건너뜀) + 「만들기 → push_log 1행」 시험
- **FAIL-2(코디 기본값)**: 여권 **손 입력 저장은 사진 없이도 허용** — `method = app_manual` · `photo = null`(ccc · KOS 사진 0 · `identity_check` 는 남김). 카메라로 찍은 길(`app_scan`)은 지금처럼 사진 필수. 시험 · 응답 모양은 SPEC 그대로에 `photo: null` 만
- **W2**: `procedure/.env.example` 에 `CCC_COUNSELOR_ID` · `CCC_COUNSELOR_PASSWORD` · `CCC_COUNSELOR_KOS_ACCOUNT_ID` 이름 한 줄씩(값 금지)

## mobile
- FAIL-2 짝: 손 입력 저장이 사진 없이 가는지 확인(사진 없으면 보내지 않음) · 시뮬레이터에서 손 입력 → 저장 한 번(임시 back)
- **W1**: 이미 연 띄우기 요청은 다시 열지 않는다(연 id 기억 · `resumed` 때 거름)
- **W3**: 알림 목록 항목 누름 = 그 항목 `ids` 로 읽음(SPEC §5-4)

W4(front 보안 권고)는 사용자 결정 — 손대지 않는다.
