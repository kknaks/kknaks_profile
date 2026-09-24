# Phase 4 검수 수정 — W-1·W-3·W-4 및 배선 테스트

검수 보고서 `review-tauri-p4-web-wiring-report.md`의 WARN을 수정한다. 기존 셸 계약과 브라우저 동작은 유지한다.

- 브라우저 녹음은 `start()` 실패 뒤 재시작할 때 새 세션 키를 만든다. 마운트 단위 `captureId` 재사용을 제거하거나 회차 키를 별도로 둬 W-1을 닫는다.
- 회의 경로의 언마운트 release 실패는 React state 업데이트 없이도 사실을 남길 수 있는 방식으로 처리한다. 녹음을 재시작하지 않는다(W-3).
- 브라우저 경로의 늦은 hold/drop 호출이 언마운트·회차 교체 후 상태를 오염시키지 않도록 가드를 보강한다(W-4).
- `open_external`/U-4는 Phase 3의 실제 네이티브 커맨드 넷 계약에 포함된 기능이므로 유지한다. 임의 권한·운영 URL은 추가하지 않는다(W-5/W-6은 조용한 실패가 없도록 필요한 경우 실패 상태를 반환/표시).
- 이번 수정에서는 `frontend/src/lib/shell.test.ts` 테스트 파일 1개를 추가로 허용한다. 셸 전역 absent, acquire 후 degraded/E-14a, 직렬화와 release 실패(E-14b)를 단위 검증하되 브라우저 기본 경로를 깨지 않는다.

허용 범위: 위 6개 배선 파일 + `src/lib/shell.test.ts`. `api.ts`, `microphone.ts`, `src-tauri/**`, 서버·운영·배포는 금지. tsc와 관련 테스트 및 전체 회귀를 실행하고 `tauri-p4-web-wiring-fix-report.md`만 보고한다.
