# Phase1 구현 중 코디 보완 지시

origin/외부 URL 검증에 자체 url_lite 파서를 만들지 않는다. Tauri가 이미 쓰는 Url/url crate 표준 파서를 재사용한다. 정규화/default port/userinfo/backslash 처리 차이로 권한 경계를 잘못 해석할 수 있기 때문이다. 허용 origin은 파싱한 origin 기준으로 비교하고, open_external 스킴은 http/https만 허용하는 계약을 유지한다. 새 외부 기능이나 다른 Phase 범위 추가 아님. 이번 코디 지시는 검수 브리프에도 전달한다.
