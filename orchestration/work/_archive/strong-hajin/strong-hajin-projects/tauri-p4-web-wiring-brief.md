# WORK-006 Phase 4 — 웹 최소 배선

코드 워크트리: `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-projects`.

Phase 3 제품 셸과 Phase 2 조건부 판정을 전제로 웹 배선만 구현한다. 허용 파일은 다음으로 제한한다.

- `frontend/src/lib/shell.ts` (신규)
- `frontend/src/lib/labels.ts`
- `frontend/src/features/meetings/stream.ts`
- `frontend/src/features/meetings/MeetingDetailPage.tsx`
- `frontend/src/features/meetings/BrowserRecordingPage.tsx`
- `frontend/src/App.tsx`

`api.ts`, `microphone.ts`, 서버 코드, `src-tauri/**`는 수정하지 않는다. 셸이 없는 브라우저에서는 기존 동작을 그대로 유지한다.

구현 계약:

1. Tauri 환경 감지 뒤에만 `shell_info`, `wake_guard_acquire`, `wake_guard_release`를 호출한다. 운영 origin·범용 invoke·파일 권한을 추가하지 않는다.
2. 회의 녹음 경로는 마이크가 실제로 열린 뒤 acquire하고, stop·실제 닫힘 완료 뒤 release한다. 세션 키는 회의 id가 아니라 회차마다 새로 생성하며 중복 acquire는 만들지 않는다.
3. 브라우저 녹음 경로도 동일하게 배선한다. 구독·마이크 권한 거부·마이크가 열리기 전 실패에서는 acquire하지 않는다.
4. acquire 실패/셸 부재/`degraded`는 녹음을 실패시키지 않는다. `labels.ts`에 U-3 한 줄만 추가하고, release 실패는 E-14b 사실을 드러내되 녹음을 다시 켜지 않는다.
5. 두 화면 동시 요구는 현재 App의 early return 계약을 존중한다. 화면 전환·닫기 취소·막힌 이동에서는 release하지 않는다.

검증: TypeScript, 기존 프론트 전체 테스트, 배선 관련 회귀 테스트를 실행한다. Tauri 네이티브 코드는 건드리지 않았음을 diff로 확인한다. 운영 서버 접속·설치·Release는 하지 않는다. 결과 보고서는 `orchestration/work/strong-hajin-projects/tauri-p4-web-wiring-report.md` 한 파일만 작성한다.
