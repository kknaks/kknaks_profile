# Tauri 배포 결정과 인프라 확인

2026-09-22. 사용자 결정 반영. 제품 구현·서버 변경·배포는 수행하지 않았다.

## 확정

- macOS·Windows 모두 지원. 최소 OS·CPU 아키텍처·설치파일 형식은 후속 확정.
- 운영 프론트·백엔드는 사용자 Mac Studio. 기존 Kubernetes 인프라 활용, 별도 Vercel 없음. 웹·API·WebSocket은 같은 HTTPS origin으로 구성해 쿠키 인증 유지.
- 설치파일은 제품 코드 저장소 GitHub Releases. 릴리즈 문서는 프로필 제품 60-release. 같은 버전·태그와 Release 링크로 연결. 실제 발행 전 릴리즈 완료 기록은 만들지 않음.
- DEC-005 D-07~09 추가, SPEC-006 v0.2.3 및 결정 추적·OQ·index·log 갱신. 기존 녹음·네이티브 수명주기 계약은 유지. 이전 검수 이후 사용자 결정 반영분이며 별도 독립 재검수는 하지 않음.

## 읽기 전용 확인

접속 원천은 orchestration/config/projects/mediness.json의 environments.ssh_host와 kubectl이다. 접속 값을 별도 설정으로 복제하지 않았다.

인프라 원천: /Users/kknaks/git/harness_works/k8s_infra_mac.
README는 Mac Studio ARM64, Lima Kubernetes, Cloudflare Tunnel, Helm·ArgoCD 구성을 기술한다. mediness ingress는 별도 front/api 호스트이고 프론트가 Next BFF를 포함하므로 Strong Hajin의 같은 origin 라우팅을 그대로 대신하지 못한다.

SSH로 kubectl get nodes 및 argocd get applications의 이름·아키텍처·브랜치·상태만 조회했다(exit 0). 노드 셋 모두 arm64. 조회된 Application 열 개는 모두 main, Synced, Healthy였다. mediness-prod manifest도 main이다. README의 k8s-test 설명은 현재 실물과 다르므로 그대로 배포 지침에 인용하지 않는다. Strong Hajin Application은 조회 목록에 없었다.

## 후속 계획에 포함할 것

- Strong Hajin 전용 배포 구성과 같은 origin의 정적 프론트·API·WS 라우팅. 운영 도메인은 미정.
- 운영 프로파일에서 API 등록·인증·Secure 쿠키가 성립하도록 기존 코드 문제 해결.
- 기존 납품 이미지의 linux/amd64 전제와 ARM64 서버의 실행 적합성 확인. 서버 ARM64와 데스크톱 지원 아키텍처는 별개.
- macOS·Windows에서 원격 문서 IPC, 마이크 포맷·전송, 화면 꺼짐·최소화 녹음 실측.
- 코드 Releases 발행 절차와 프로필 60-release 기록 연결. 서명·공증·자동 업데이트는 별도 미결이며 기존 인프라에 있다고 간주하지 않음.
