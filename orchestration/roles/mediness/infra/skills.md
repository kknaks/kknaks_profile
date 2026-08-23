# @mediness-infra — 스킬

## 핵심 역량
- **Helm 차트 작성**: Chart.yaml/values.yaml/templates/ 구성, values-dev/prod 분리, 기존 `charts/mediness`·`charts/private-pypi` 패턴 재사용
- **ArgoCD GitOps**: Application/AppProject YAML, sync policy, dev/prod 앱 분리 (`argocd/applications/`, `argocd/projects/`)
- **kubernetes 리소스**: Deployment/StatefulSet/Service/Ingress/ConfigMap/Secret/PVC, 리소스 요청·제한, 헬스체크(liveness/readiness)
- **네트워킹**: ingress-nginx 라우팅, MetalLB LoadBalancer, Cloudflare Tunnel 노출
- **프로비저닝**: Lima VM, kubeadm, Makefile 타겟, provisioning 스크립트 이해

## 배포 워크플로 스킬
- 신규 앱 배포: `charts/<app>/` 차트 작성 → `argocd/applications/<app>-{dev,prod}.yaml` → root-app 에 편입 → 커밋 → ArgoCD 동기 확인
- 이미지 참조: private registry(`private-pypi` 있듯 사내 레지스트리) 또는 GHCR — 앱 워커가 빌드·push 한 이미지 태그를 values 에 반영
- 시크릿: env/토큰은 매니페스트에 평문 금지 — provisioning/secrets 방식

## 검증 스킬
- `helm template` / `helm lint` 로 렌더 검증(클러스터 없이도)
- `kubectl --dry-run=client -o yaml` 로 매니페스트 검증
- ArgoCD sync 상태·앱 health 확인
