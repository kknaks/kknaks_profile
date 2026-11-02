# [planner] SPEC-001 · WORK-001 fix1 — 문서 리뷰 FAIL 2 · WARN 6 반영

너는 앞서 SPEC-001 · WORK-001 을 쓴 interpret-pwa planner 다. 역할 · allowed_paths · 검증 · 보고 방식은 원 브리프 그대로:
`/Users/kknaks/orca/workspaces/kknaks_profile/PWA-통역기능/orchestration/work/interpret-pwa-poc/interpret-pwa-poc-spec-brief.md`

리뷰 리포트(정본): `/Users/kknaks/orca/workspaces/kknaks_profile/PWA-통역기능/orchestration/work/interpret-pwa-poc/review-doc-report.md` — 지적마다 위치 · 근거가 있다.

## 고칠 것 (전부)

1. **FAIL-1** §4.4 4번 `invalid_request` 재연결 — 원형은 ready 를 먼저 보내고 Soniox 거절은 나중 메시지로 온다. 판별(어느 메시지 · 어느 필드) · 시점 · 재연결 동안 들어오는 클라 PCM 처리(버림 vs 버퍼) · 클라에 보이는 것(같은 WS 유지 여부)을 원형 코드 근거로 확정. 원형 코드로 못 닫는 건 기본값 표시
2. **FAIL-2** §7.3 판정 순서 — 멈춤 중에도 TTS 출력이면 「〈언어〉로 출력 중」이 떠야 한다(D-09). 순서를 고치고 §9 시험 항목도 맞춘다
3. **WARN-1** 백그라운드 복귀(WS 닫힘)와 pause 멈춤(WS 열림)을 표에서 다른 상태로 나누고 원 누름 동작을 각각 적는다
4. **WARN-2** `INTERPRET_BACK_PORT` 는 env 목록에서 빼고 8800 고정. `NEXT_PUBLIC_API_BASE_URL` 은 dev = `front/.env.local`(예시 `front/.env.example`), compose = `build.args` 치환으로 — 읽는 곳을 한 줄로 고정
5. **WARN-3** medikit 실재 이름으로 확정 — 언어 고르기 = `ComboBox`(또는 실재 Menu), 용어집 패널 = `Modal`/`Dialog` 중 하나. README 로 실재 대조
6. **WARN-4** 오류 때 외국어 영역 문구를 표와 본문 중 하나로 맞춘다(외국어 사용자도 알아야 하니 외국어 영역에도 짧은 오류 표시가 기본값)
7. **WARN-5** OQ-003 · OQ-009 를 WP2 완료 조건(결과 기록 → 사용자 결정)에, OQ-006 을 WP5 리뷰 항목에 넣는다. WORK 열린 것 표 갱신
8. **WARN-6** 통역 화면 진입 시 AudioContext 를 깨우는 첫 탭 — 기본값: 세션 시작 전 「탭해서 통역 시작」 오버레이(원 누름과 분리). §7.3 상태표 · §9.2 에 반영

SPEC version 0.1.0 → 0.2.0, 변경 이력에 fix1 한 줄. DEC 는 고치지 않는다.

## 완료 보고

원 브리프 §9 그대로(코디 핸들은 보고 직전 `orca terminal list --json` 에서 제목 'Interpretation PWA with terminology integration' 으로 확인).
