# [mobile] 코드 리뷰 r2 WARN 7 수정

리뷰 `/Users/kknaks/orca/workspaces/kknaks_profile/cc-내부채팅/orchestration/work/internal-chat/review-code-r2.md` WARN W-1 ~ W-7 을 리뷰의 「권장」대로 고친다. 역할 · allowed_paths(`procedure/app/`) · 하지 말 것 · 완료 보고는 앞 브리프 그대로. subject 「mobile 수정 r2 완료: …」.

코디 처분:
- **W-1** 3분 경계 = 서버와 같은 규칙 하나로(`durationMs > 180000` 이면 못 보냄). 앱이 보는 길이는 **변환 뒤 실제 ms** 와 같은 값으로 판단하고, 최근 줄 흐림은 초 반올림 값이 아니라 가능한 한 정확한 ms(photo_manager 의 `videoDuration` 등)로 — 못 하면 최근 줄은 181초 이상만 흐리고, 보내기 직전 실제 ms 로 다시 막아 「3분 이하 동영상만 보낼 수 있어요」. 서버(`procedure/back`)는 고치지 않는다
- **W-2** 진행률 = 실제로 보낸 바이트 · 메모리에 다 쌓지 않기(되밀기 있는 스트림 · 예: `http` 의 `StreamedRequest` 대신 `dart:io` `HttpClient` 로 파일 스트림을 `addStream` 하고 보낸 양을 센다 — `Content-Length` 는 그대로 싣는다)
- **W-3** 임시 사본 지우기 = 항목마다 그 파일만(전역 `clearFileCache` 금지)
- **W-4** 동영상 재생 = **무음 스위치를 따른다**(SPEC §9.2) — 재생 화면 열 때 오디오 세션을 `.soloAmbient`(또는 `.ambient`)로 두는 네이티브 채널 · 닫을 때 원래대로. 통역 기능 오디오 세션과 충돌하지 않게 확인
- **W-5** `Info.plist` `PHPhotoLibraryPreventAutomaticLimitedAccessAlert = true`
- **W-6** `probe` 를 배경 큐에서 · 결과는 메인으로
- **W-7** 공유 [취소]를 누르는 시험(파일 지움 · 토스트 없음)

검증: `/Users/kknaks/fvm/versions/3.44.8/bin/flutter analyze && … flutter test` 1회 · `flutter build ios --simulator --debug` 1회. 시뮬레이터 · 기기는 건드리지 않는다(사용자가 지금 보고 있다).
