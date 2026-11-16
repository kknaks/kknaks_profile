# E2E batch 3 수정 — 웹 예약 상세 (코디 · 2026-10-28)

원천 + 처분: `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/orchestration/work/overall-board/e2e-feedback-batch3.md`(#1 ~ #5 · 「처분」 칸이 할 일). 코드 워크트리 `/Users/kknaks/orca/workspaces/cc-prototype/overall-board` — **브랜치 `kknaksss/overall-board-8`**(origin/main `113c5e1` · 코디가 체크아웃). 커밋 · push 금지 · 사용자 포트 금지 · 끝나면 보고서에 「E2E batch 3」 절 + 두 명령(코디 `term_678ac61d-2472-4a9b-ba73-61883337b957`).

## backend (`procedure/back/**`) — 보고서 `app-backend-report.md`
- **#1 사진 삭제 API**: ccc `id_photo` 파일 · 행 지움 + `identity_check` 미확인으로 + **KOS 이미지 지움**(KOS 웹 사진 탭 [삭제] 경로 — HAR `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/reference/2026-10-23-cc-overall-board/har/여권스캔.har` · KOS 웹 JS 에서 찾아라) · 이벤트 로그. **데모 실호출 1회**(허가 · 데모 assert · TEST 그림 · 운영 키 금지)
- **#2 유입 채널 쓰기 API**: KOS 고객 유입 채널 칸(예약 등록이 쓰는 코드 목록 그대로)을 고치는 경로(`update-visitor-management-information` 묶음 — `reservation-memo-test-report.md` 의 묶음 규칙: 읽은 묶음 전체 + 바꿀 칸) · 상세 응답에 지금 값 · 코드 목록 · **데모 실호출 1회**
- #3 ~ #5 는 지금 저장 API 그대로 쓰면 되는지 확인(자동 저장이 자주 부름 — 같은 값이면 KOS 안 부르기 · 직전 다시 읽기 유지)
- 검증 `ruff` · `pytest` · 경로 수 시험 갱신

## frontend (`procedure/front/**`) — 보고서 `app-fe-report.md`
- **#1** 신분 확인 칸 [삭제](확인 창) · **#2** 유입 채널 드롭다운(DS Select) · 바꾸면 바로 저장
- **#3 · #4 · #5 자동 저장 한 규칙**: [저장] · [수정] 버튼 없앰 · 입력 멈춤 1초 + 칸 벗어날 때 + 모달 닫을 때 저장 · 칸 옆 상태(저장 중 · 저장됨 · 저장 못 함 + 다시) · 실패 = 글자 유지 · 고객 기본 정보는 늘 편집 가능(칸마다 저장)
- back 이 아직이면 가짜 응답으로 화면부터 · 모양은 back 보고서에 맞춤 · 검증 `tsc` · `lint` · 스크린샷 `fe-shots-reservation/b3-*.png`

## 추가(같은 날 · 사용자) — frontend
- 웹 예약 상세 **[스캔할 기기]의 「QR」 칸은 뺀다**(앱이 QR 을 읽지 않게 됨 — 기기 버튼만). 문진 「QR 로 고객 입력 요청」 QR 은 그대로(고객 폰 웹)
- back: 앱 QR claim 경로를 쓰는 곳이 없어지면 남겨 둘지 보고(지우지는 말고 — 코디가 정함)
