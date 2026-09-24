# Phase 4 수정2 재검수

- 판정: **PASS (FAIL 0)**
- 확인일: 2026-09-22

## 확인 결과

1. `BrowserRecordingPage.tsx`의 effect가 재마운트 시 `mounted.current = true`를 복원한 뒤 cleanup에서 false로 내린다. StrictMode 개발 재마운트에서 U-3 호출이 영구 차단되는 회귀가 닫혔다.
2. `tauri-p4-web-wiring-fix-report.md`의 R-2 서술은 제품 결함 단정이 아니라 `vi.mock`/`vi.resetModules()` 모듈 러너에서 관측된 시험 환경 경합과 동시 호출 안전성 보강으로 정정됐다. `shell.ts` 동작은 유지된다.
3. 이번 수정2 코드 변경은 화면 파일 한 곳이며 `src-tauri`, `api.ts`, `microphone.ts`, `shell.ts`, `shell.test.ts`, `stream.ts`, `App.tsx`에는 추가 변경이 없다.
4. tsc, shell 13건, browser+shell 24건 3회, 전체 프론트 1053건 3회가 통과했다. 과거 전체 스위트의 서로 다른 파일 실패는 시간 의존 기준선 불안정으로 남긴다.

## 이월 WARN

- 화면 배선을 직접 잠그는 회귀 시험은 아직 없다.
- `open_external` 실패의 사용자 표시(UI)는 별도 범위다.
- M-1 원격 HTTPS 문서 실측은 CA 신뢰 설치 후 내일 제품판에서 수행한다.

이월 항목은 FAIL이 아니며 Phase 5 실측·후속 운영 범위로 넘긴다. 설치·실기 E2E를 수행했다고 주장하지 않는다.
