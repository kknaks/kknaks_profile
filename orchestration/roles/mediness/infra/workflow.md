# @mediness-infra — 워크플로

## 신규 앱을 클러스터에 배포 (GitOps)
1. **파악**: 배포 대상 앱의 이미지(레지스트리·태그), 포트, 필요한 env/시크릿, 헬스체크, 스토리지(PVC) 요구를 확인. 앱 워커/브리프에서 받는다.
2. **차트 작성**: `charts/<app>/` — Chart.yaml + values.yaml(+ values-dev/prod) + templates/(Deployment/Service/Ingress/ConfigMap 등). 기존 `charts/mediness` 패턴 참고.
3. **렌더 검증**: `helm lint charts/<app>` + `helm template <app> charts/<app> -f values-dev.yaml` 로 매니페스트 정합 확인(클러스터 불요).
4. **ArgoCD Application**: `argocd/applications/<app>-dev.yaml`(+prod) 작성 — source(repo/path/chart), destination(namespace), syncPolicy. AppProject 필요 시 `argocd/projects/`. root-app 에 편입되게.
5. **시크릿**: 토큰/비번은 provisioning/secrets 방식(커밋 금지). values 엔 secretRef 만.
6. **변경 준비**: 워크트리에 변경만 남긴다. 커밋·push·PR은 코디네이터가 담당한다.
7. **검증·보고**: dry-run/template 결과 + (클러스터 있으면) `kubectl get`/ArgoCD sync 확인 → worker_done.

## 기존 앱/인프라 변경
- 매니페스트 수정 → helm lint/template → dry-run. 변경 영향(재시작·다운타임) 명시.

## 클러스터 프로비저닝(M0~) 작업
- `docs/build-plan.md`·`milestones.md` 를 기준으로. Makefile 타겟(`make host-prep`/`vm-up`/`bootstrap`/`base`) 흐름 존중. 파괴적 단계는 사용자 확인.

## 협업
- 앱 배포 계약(이미지·포트·env)은 앱 워커와 확인. 정책은 planner 와.
- 클러스터가 없는 코드-온리 환경이면 helm/dry-run 검증까지만 하고, 실배포는 클러스터 있는 곳에서 하도록 보고에 명시.
