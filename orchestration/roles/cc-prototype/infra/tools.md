# @cc-prototype-infra — 도구

## 작업 위치
- 레포 `k8s_infra_mac`(MediSolveAIDev) — 워크트리 · base 는 브리프가 SSOT. canonical 체크아웃은 사용자 것(pull · checkout 금지)

## 명령
```bash
helm lint charts/cc-prototype
helm template cc-prototype charts/cc-prototype -f charts/cc-prototype/values-prod.yaml
kubectl apply --dry-run=client -f <렌더된 매니페스트>
kubectl get pods -n cc-prototype-prod      # 클러스터 접근이 있을 때 · 읽기만
```

## 주의
- 직접 `kubectl apply` 로 배포 금지 — 매니페스트 → ArgoCD
- 클러스터 접근이 없으면 lint · template · dry-run 까지, 실배포 · sync 는 코디네이터 · 사용자
- 커밋 · push · PR 금지
