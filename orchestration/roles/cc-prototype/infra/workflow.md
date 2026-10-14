# @cc-prototype-infra — 워크플로

1. **파악**: 브리프 · SPEC 배포 절 · 앱 레포의 Dockerfile/README 에서 이미지 · 포트 · env · 시크릿 · 헬스체크 · 데이터 마운트(SQLite PVC · 시나리오 · 직원 파일)를 확인
2. **차트**: `charts/cc-prototype/` — `charts/strong-hajin` 을 본떠 back · front · ingress(`ccc.medisolveai.xyz`, `/api` 경로 · SSE · WS) · configmap · PVC
3. **렌더 검증**: `helm lint` · `helm template` · `--dry-run`
4. **ArgoCD Application**: `argocd/applications/cc-prototype-prod.yaml` — 수동 sync(첫 착지), CreateNamespace. 필요하면 AppProject
5. **시크릿**: `provisioning/secrets/cc-prototype-prod.env.example`(키 이름만) · 주입 방법을 문서에
6. **Cloudflare Tunnel 라우팅**: 기존 방식 확인 → 브리프가 허락하면 추가, 아니면 필요한 변경을 리포트에
7. **보고**: 변경 파일 · 검증 결과 · 사용자가 할 일(시크릿 주입 · sync) → worker_done
