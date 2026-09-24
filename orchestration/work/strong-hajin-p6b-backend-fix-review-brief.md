# Phase 6b backend WARN 보정 독립 검수

보정된 backend 테스트와 보고서만 확인한다.

- 미인증 WS가 실제 CLOSE_UNAUTHORIZED 4401을 단언하는지 확인한다.
- `/api/work-requests`가 등록·401·persona 401 커버에 들어갔는지 확인한다.
- 보고서가 `developer_auth_enabled`와 `local_login_enabled` 게이트를 분리해 설명하는지 확인한다.
- backend/src 권한·쿠키·로그인 구현 무변경, make test 1454 병렬 + 130 직렬, D-4 미결을 확인한다.
- 검수 보고서 한 파일만 작성한다. FAIL/WARN을 분리한다.
