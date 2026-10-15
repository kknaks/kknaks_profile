# [infra] fix1 — back PVC Pending(local-path 는 lima-worker-1 만)

증상(2026-10-13 sync 뒤): `cc-prototype-prod` PVC `cc-db` Pending — `failed to provision volume with StorageClass "local-path": config doesn't contain node lima-worker-2`. local-path-config 의 nodePathMap 은 **lima-worker-1 만**(`/mnt/lima-pgdata/local-path`). datastores · strong-hajin 차트는 `nodeSelector`(`worker: lima-worker-1`)로 맞춘다(`charts/datastores/values.yaml` 주석).

- `charts/cc-prototype`: back Deployment 에 `nodeSelector: {kubernetes.io/hostname: lima-worker-1}`(values 로 — `back.nodeSelector`, values-prod 에 값) · datastores 주석처럼 이유 한 줄
- 이미 생긴 Pending PVC 에 `volume.kubernetes.io/selected-node: lima-worker-2` 가 붙어 있을 수 있다 — **지우는 건 코디가 한다**(파괴적). 리포트에 「PVC 삭제 후 sync」 라고만
- `helm lint` · `helm template` · 리포트 `deploy-infra-report.md` 끝에 「fix1」 절. 워크트리는 같은 곳(브랜치는 main 에 머지됨 — `git fetch origin && git checkout -B kknaksss/cc-prototype-fix1 origin/main` 에서 작업)
- 완료 보고는 infra 브리프 두 명령(subject 「infra 완료: fix1 …」, taskId/dispatchId 는 infra 판 것 task_e88c71b08b70 / ctx_f37a7adab1b6)
