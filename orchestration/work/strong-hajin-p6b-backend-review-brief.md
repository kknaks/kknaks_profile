# Phase 6b B-1/B-2 backend 독립 검수

`tauri-p6b-backend-report.md`와 현재 backend diff를 검수한다.

- `http.py`의 라우트 등록 게이트가 제거되고 PRODUCTION에서 대표 REST/WS가 404가 아닌 401/권한 판정으로 도달하는지 확인한다.
- `Secure` 쿠키 조건, `local_login`/developer persona 차단, 권한 판정이 약화되지 않았는지 확인한다.
- 기존 구계약 테스트 2건 갱신과 신규 8건의 의미를 확인한다.
- make test 수치(1453 병렬 + 130 직렬), inventory drift 0을 재현하거나 보고서와 차이를 기록한다.
- 허용 파일 밖 변경·로그인 방식 발명·배포 수행이 없는지 확인한다.
- D-4(PRODUCTION 세션 발급 수단 부재)는 차단으로 유지한다. 코드 수정 없이 검수 보고서 한 파일만 작성한다.
