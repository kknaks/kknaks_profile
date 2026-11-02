# [writer] 지시 5 — 4차 검수 ★·WARN 을 SPEC/WORK 에 반영 (2026-10-06)

리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱-하진/orchestration/work/strong-hajin-inbox/review-spec-work-r4.md` 의 ★1~★4 와 WARN 전부를 문서에 반영한다. **BE-1 은 이미 발주됐다**(★1·★2·BE-1 몫 WARN 은 backend 워커가 코드로 넣는 중) — 문서를 그 상태와 맞춘다.
- ★1 handshake selected_rooms 에 external_id(chatId) · ★2 reset-account 는 웹 세션 라우트
- **★3** 슬랙 완료 조건 로컬 측정: **개발 전용 토큰 주입 타겟**(로컬에서 `~/.slack_test_token` 의 사용자 토큰을 「연결된 슬랙 연동」으로 넣는 make 타겟 · 운영 빌드에 없음)을 BE-2 에 넣고, 「슬랙 연결」 OAuth 버튼 흐름은 운영 반영 뒤 확인으로
- **★4** 반영 순서: 노드 hostPath 디렉터리 mkdir · 수동 SQL(스키마) 선행 → 그다음 back 배포(Directory 타입이라 없으면 back 전체가 멈춤) — RUNBOOK-002 §2-4 와 같은 방식으로 WORK 반영 절에
- WARN: BE-1 에 동기화 상태 칸·NOTIFY·모듈 분할(이미 BE-1 발주에 포함 — 문서만) · operation inventory · 비번 변경 시 기기 토큰 철회 · 토큰 UI · selected_rooms_version · 첫 handshake 연동 생성 · AX_WEB_ORIGIN · **SHELL-0(카톡 DB 탐침)을 BE-1 과 동시로 앞당김** · FE-b→SHELL 바인딩 의존 · 판 가르기 preflight · WP 옛 문장 5곳
allowed: SPEC-008·009 · SPEC-006 · WORK-011 · 20-spec/README · 30-work/README. 커밋 금지. 끝나면 `review-spec-work-fix4.md` + §9.
