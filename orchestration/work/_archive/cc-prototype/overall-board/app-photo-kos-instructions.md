# backend — 여권 사진이 KOS 화면에 안 보임 (E2E batch 2 #5 · 코디 · 2026-10-28)

사용자: KOS 일정 상세 「기타 › 사진 · 펜차트」에 여권 사진이 없다. 운영 `id_photo` #1 `kos_status=ok`(KOS 200). WP-KOS Q-156 기본값으로 `scheduleId` · `path` 를 안 보냈다(`app-wp-kos-report.md`).

1. **데모 실호출**(허가 · 데모 테넌트 assert · 운영 키 금지 · TEST 그림만): `registerVisitorImages` 에 **`scheduleId`(그 예약 일정)** 를 넣어 1회 → KOS 일정 상세 사진 탭이 읽는 조회(KOS 웹 JS · HAR 에서 그 탭이 부르는 API 를 찾아라)에 보이는지 · 안 넣은 이미지(지금 것)는 KOS 웹 어디에 보이는지(고객 정보 화면?)
2. 결과대로 **여권 사진 올리기에 `scheduleId` 를 싣는다**(그 스캔의 예약 일정) · 분류는 지점 코드에 맞는 것이 없으면 그대로 안 보냄 · 시험
3. 브랜치: 코디가 새로 만든 `kknaksss/overall-board-5`(origin/main `affac41`) — 커밋 금지 · 보고서 `app-backend-report.md` 「E2E batch 2 #5」 절(데모 결과 · 남긴 흔적) + 두 명령
