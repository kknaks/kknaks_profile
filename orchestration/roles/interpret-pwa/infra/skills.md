# @interpret-pwa-infra — 스킬

- **Helm 차트**: Chart.yaml · values.yaml(+ values-prod.yaml) · templates(back · front Deployment/Service · Ingress · ConfigMap · Secret 참조) — `charts/cc-prototype` 패턴
- **ArgoCD**: Application(수동 sync 로 첫 착지) · 필요하면 AppProject(destination 네임스페이스 허용)
- **ingress-nginx**: 경로 라우팅(`/api` → back, 나머지 → front) · WebSocket(Upgrade · 긴 read timeout)
- **Cloudflare Tunnel**: SPEC 이 정한 서브도메인 → ingress (cloudflared 설정 위치는 기존 차트에서 확인)
- **검증**: `helm lint` · `helm template` · `kubectl apply --dry-run=client`
