# Phase 6a 운영 배포 설계 독립 검수

`tauri-deploy-design.md`만 검수한다.

- k8s_infra_mac Mediness 근거 좌표와 clean/diff 0 주장이 실제와 맞는지 확인한다.
- PRODUCTION 라우트 미등록·Secure 쿠키 충돌을 정확히 표현하고 development/test 우회를 기본안으로 쓰지 않았는지 확인한다.
- 같은 origin `/`, `/api/*`, WS 경로, FE nginx 정적 서빙과 데이터/PVC/DB 분리가 6b 작업으로 옮길 수 있는지 확인한다.
- 도메인·레지스트리·외부 레포 권한·로그인 수단 등 미결 사용자 결정을 발명하지 않았는지 확인한다.
- 6b 소유표와 P-5 인프라 워커 미정의가 명시됐는지 확인한다.
- 제품 코드·인프라 레포는 수정하지 않고 검수 보고서 한 파일만 작성한다. FAIL/WARN을 분리한다.
