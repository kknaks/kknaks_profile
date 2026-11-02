# WORK-006 Phase 6a — Strong Hajin 운영 배포 설계

## 목적

내일 실행할 운영 배포의 설계를 확정한다. 운영 서버는 `/Users/kknaks/git/harness_works/k8s_infra_mac`의 Mac Studio 클러스터를 기준으로 하며, 기존 Mediness 리소스는 읽기만 한다. 실행·푸시·배포는 Phase 6b다.

## 산출물

`orchestration/work/strong-hajin-projects/tauri-deploy-design.md` 한 파일만 작성한다.

## 반드시 조사할 것

- k8s_infra_mac의 Mediness README·차트·Application·접속 방식과 실제 파일을 읽고 근거 좌표를 남긴다.
- Strong Hajin 운영 서버의 도메인은 발명하지 말고 빈 자리와 OQ-T02로 둔다.
- 같은 origin 경로 `/`, `/api/*`, `/api/meetings/{id}/stream`(WS), 쿠키 Secure 조건을 설계한다.
- PRODUCTION 라우트 등록/권한 판정 분리, Secure 쿠키, FE 정적 서빙, arm64 운영 이미지, 레지스트리 namespace 분리를 사실·기본값·사용자 결정으로 나눈다.
- Mediness와 namespace/domain/Argo project/data/PVC 경로를 분리하고, 기존 파일 diff 0을 확인한다.
- 자료·녹음 볼륨 보존, 백업/복구와 rollback을 구분한다.
- 6b 작업을 인프라/backend/frontend/코디 소유와 파일 범위로 쪼갠다. 인프라 워커가 아직 정의되지 않았다는 P-5를 명시한다.

## 금지

운영 도메인·비밀값·외부 레포 권한을 발명하지 않는다. 인프라 레포·제품 코드는 수정하지 않는다. 운영을 development/test 프로파일로 우회하지 않는다. Vercel을 전제로 하지 않는다.

## 검증

사실/기본값/사용자 결정의 혼합이 없는지, 6b가 추가 설계 없이 착수 가능한지, 기존 Mediness diff가 0인지 확인한다. worker_done으로 보고하고 멈춘다.
