# WORK-006 Phase 6b B-1/B-2 — PRODUCTION 라우트 등록 분리

## 목적

Phase6a 설계에 따라 Strong Hajin 백엔드가 PRODUCTION에서도 API/WS 라우트를 등록하도록 고친다. 권한 판정·세션 쿠키 계약은 그대로 두고, 로그인 방식·권한 완화·외부 IdP는 도입하지 않는다.

## 코드 워크트리

`/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-projects`

## 허용 파일

- `backend/src/ax_workspace/entrypoints/http.py`
- `backend/src/ax_workspace/entrypoints/http_auth.py`
- `backend/src/ax_workspace/bootstrap/settings.py`
- `backend/tests/**`
- 구현/검증 보고서: `orchestration/work/strong-hajin-projects/tauri-p6b-backend-report.md`

## 계약

- 라우트 등록과 권한 판정을 분리한다. PRODUCTION에서 기존 API/WS 경로가 존재해야 한다.
- PRODUCTION의 Secure 쿠키 조건은 유지한다.
- DEVELOPMENT/TEST 전용 demo/local login 표면은 계속 닫힌다.
- 새 인증 수단, 권한 완화, FE 정적 서빙, 인프라 차트는 이 작업에 포함하지 않는다. 필요하면 즉시 올린다.
- `/health`는 게이트 밖 기존 경로로 유지한다.

## 검증

- PRODUCTION 설정으로 앱을 만들었을 때 대표 REST·WS 라우트가 등록되는 테스트를 추가한다.
- 동일 설정에서 `cookie_secure()`가 true이고, 기존 세션/권한 테스트가 회귀하지 않는지 확인한다.
- 전체 backend 관련 테스트와 정적 검사 수치를 기록한다. 실패를 숨기지 않는다.
- 코드·테스트 외 레포, 비밀값, 배포, 커밋/push/PR은 건드리지 않는다.

완료 후 worker_done으로 변경 파일, 테스트 수치, 미결 로그인 결정(D-4)을 보고한다.
