# Phase 6b backend 검수 WARN 보정

검수 W-1~W-3만 처리한다.

- 신규 production route 시험에 미인증 WS 핸드셰이크가 `CLOSE_UNAUTHORIZED`로 닫히는 단언을 추가한다.
- REST 보호 경로 커버에 `/api/work-requests`를 추가한다.
- backend report §3-2에서 `developer_auth_enabled` 게이트와 별도 `local_login_enabled` 게이트를 명확히 구분한다.

허용 파일은 backend tests와 `orchestration/work/strong-hajin-projects/tauri-p6b-backend-report.md`뿐이다. 권한·쿠키·로그인 구현은 변경하지 않는다. 테스트와 보고서 검증 후 worker_done.
