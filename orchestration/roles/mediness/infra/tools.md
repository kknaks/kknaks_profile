# @mediness-infra — 도구

## 사용 도구
- **Read/Edit/Write**: charts·argocd·provisioning·docs 파일 편집
- **Bash**: `helm`(template/lint), `kubectl`(get/describe/--dry-run), `make`(Makefile 타겟), `git`(상태·diff 확인), `argocd`(있으면 sync/app 확인)
- **Grep/Glob**: 기존 차트·매니페스트 패턴 검색

## 자주 쓰는 명령
```bash
helm lint charts/<app>
helm template <app> charts/<app> -f charts/<app>/values-dev.yaml   # 렌더 확인(클러스터 불요)
kubectl apply --dry-run=client -f <manifest>                        # 매니페스트 검증
kubectl get pods -n <ns>                                            # 상태 확인(클러스터 있을 때)
make help                                                           # 운영 타겟 목록
```

## 주의
- **직접 `kubectl apply` 로 배포 금지**(GitOps 위반) — 매니페스트 커밋 → ArgoCD 동기. 검증용 `--dry-run` 은 허용.
- 클러스터가 안 떠있는 환경(코드만)에서는 `helm template`/`--dry-run`/`lint` 로 정합만 검증하고, 실배포·sync 는 클러스터 있는 환경에서.
- 파괴적 kubectl(delete ns/pv/cluster)은 사용자 확인.
- 커밋·`git push`·PR은 코디네이터가 담당한다. 워커는 brief의 allowed_paths 안에 변경만 남긴다.
