# mobile (+ backend 참고) — 웹 → 폰 · 태블릿 띄우기가 실기기에서 안 열림 (코디 · 2026-10-28 · 운영 00853e1 · TestFlight 빌드 8)

사용자: 「QR 찍은 건 되는데 폰 · 태블릿으로 보내는 게 안 된다」 — 웹 상세에 「iPhone 16 에 표시 중」인데 폰에 QR 화면이 안 뜸.

## 운영 기록(코디 확인)
- display_request 21 ~ 24(kind questionnaire · device 9 = 「iPhone 16」 · installId 있음) — 매번 back 로그 「띄우기 request=N 푸시 보냄 1 · 실패 0」(APNs 200) · push_log `display sent`
- 푸시 본문: `{"aps":{"alert":{"title":"고객 입력 요청","body":"데스크에서 보냈어요"}},"kind":"display","requestId":N}`
- device 9 `last_seen_at` = 04:54:57 — 요청(04:55 ~ 04:57) 동안 갱신 없음 → **SSE 로 붙어 있지 않았다**(또는 last_seen 은 등록 때만 갱신?)
- 요청 23 은 04:56:07 opened(고객 링크 열림 — 웹 QR 을 찍은 것)

## 찾을 것 (코드로 · 앱 `procedure/app/**`)
1. 앱이 **앞**일 때: iOS 는 앞에서 받은 푸시를 `willPresent` 로 넘긴다 — AppDelegate · push.dart 가 `kind:"display"` 를 받아 QR 화면을 여는가 · 배너만 띄우고 끝인가
2. 앱이 **뒤 · 잠김**일 때: 알림을 눌러야만 여는 구조인가(눌러도 안 열리나) · 콜드 스타트에서 `requestId` 로 pending 읽어 여는가
3. **SSE**: 앱이 앞인데 스트림이 `deviceId` 로 붙어 있나(빌드 8 로그인 뒤 · 재연결 · 백그라운드 복귀) — 붙어 있다면 back 이 SSE 로도 보냈을 텐데 `last_seen` 이 안 바뀐 이유(back 이 SSE 연결에 last_seen 을 갱신하나 — backend 와 확인)
4. `kind:"questionnaire"` 띄우기 = QR 화면 경로가 푸시 · SSE · pending 셋 다에서 같은 함수로 가나

고친 뒤: 시험 · `flutter analyze` · `flutter test` · 시뮬레이터에서 `xcrun simctl push` 로 앞 · 뒤 · 콜드 스타트 세 경우 확인(임시 back) · 보고서 「띄우기 실기기 안 열림」 절 + 두 명령. 커밋 금지. 브랜치: 코디가 새로 만든 `kknaksss/overall-board-7`.

## 추가 단서(사용자)
- 「다시 로그인하니까 된다」 — 빌드 8 로 업데이트한 뒤 저장된 세션으로 켰을 땐 안 됐고, 로그아웃 → 로그인하니 됨. → **앱 시작 · 업데이트 뒤 저장 세션으로 들어올 때 기기 등록 · SSE(deviceId) 를 다시 붙이지 않는 결함**으로 본다. 로그인 때만 하던 것을 앱 시작 · 앞으로 복귀 때도
