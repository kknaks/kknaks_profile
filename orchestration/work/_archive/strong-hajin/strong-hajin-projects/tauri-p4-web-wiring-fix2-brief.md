# Phase 4 수정2 — StrictMode 가드 및 증거 문구

`review-tauri-p4-web-wiring-fix-r2-report.md`의 R-1·R-2만 닫는다.

- `BrowserRecordingPage.tsx`의 mounted effect가 개발 StrictMode의 mount→cleanup→mount에서도 다시 `true`가 되도록 수정한다. 언마운트 뒤 늦은 호출은 계속 차단한다.
- `tauri-p4-web-wiring-fix-report.md`에서 jsdom/vitest 동시 dynamic import에서 관측한 결함을 실제 브라우저 제품 결함으로 단정하지 말고, 동시 호출 안전성을 보강한 수정·테스트로 표현한다. 코드 동작은 바꾸지 않는다.
- 허용 파일: `frontend/src/features/browser/BrowserRecordingPage.tsx`, `orchestration/work/strong-hajin-projects/tauri-p4-web-wiring-fix-report.md`만. `src-tauri`, api, microphone, 운영·배포 금지.
- tsc와 `shell.test.ts`, 관련 전체 테스트를 실행하고 `tauri-p4-web-wiring-fix2-report.md`만 신규 작성한다.
