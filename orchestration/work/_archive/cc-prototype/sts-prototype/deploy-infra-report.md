# cc-prototype infra 배포 준비 결과 — k8s_infra_mac (DEC-003)

## 상태: done (커밋 · push · 실배포 없음)

워크트리 `/Users/kknaks/orca/workspaces/k8s_infra_mac/sts-prototype`

## 만든 · 바꾼 파일

| 파일 | 내용 |
|---|---|
| `charts/cc-prototype/Chart.yaml` · `values.yaml` · `values-prod.yaml` | strong-hajin 방식. `host` · `image.registry` · `image.tag` 가 비면 렌더 실패. prod: host `ccc.medisolveai.xyz` · registry `ghcr.io/kknaksss` · **tag 비워 둠**(첫 빌드 sha 를 넣어야 함) · `imagePullSecrets: [ghcr-pull]`. `back.imageTag` / `front.imageTag` 가 `image.tag` 보다 우선(두 워크플로 sha 가 다를 수 있음) |
| `templates/back.yaml` | Service + Deployment replica **1** · **Recreate** · runAsUser/Group · `fsGroup: 10001` · runAsNonRoot · envFrom ConfigMap + `secretRef cc-prototype-secret` · probes `/api/health` · 마운트 PVC `/data/db` · Secret `cc-prototype-scenario` → `/data/scenario`(평평한 키, 읽기 전용) · Secret `cc-prototype-staff` → `/data/staff/kos-staff.json` |
| `templates/back-pvc.yaml` | PVC `cc-db` 1Gi local-path, `helm.sh/resource-policy: keep` |
| `templates/front.yaml` | Service + Deployment, 포트 3600, runAsNonRoot + runAsUser 1000(이미지 USER 가 이름 `node` 라 숫자로 고정), `PORT` · `HOSTNAME=0.0.0.0`(Next standalone), probe `GET /login`(front.healthPath) · imagePullSecrets `ghcr-pull` |
| `templates/configmap.yaml` | `CC_DB_PATH=/data/db/cc.db` · `CC_SCENARIO_DIR=/data/scenario` · `CC_KOS_STAFF_PATH=/data/staff/kos-staff.json` · `CC_FRONT_ORIGIN=https://ccc.medisolveai.xyz` · `LOG_LEVEL` |
| `templates/ingress.yaml` | host `ccc.medisolveai.xyz`, `/api` → back:8600, `/` → front:3600. read/send timeout 3600 · `proxy-buffering: off`(SSE) · body 10m. WS 는 ingress-nginx 기본 Upgrade 전달 |
| `templates/_helpers.tpl` · `NOTES.txt` | host/image `required` · 라벨 · 렌더 후 체크리스트 |
| `argocd/applications/cc-prototype-prod.yaml` | project `cc-prototype`, ns `cc-prototype-prod`, `CreateNamespace=true`, **automated 주석(수동 sync)** |
| `argocd/projects/cc-prototype.yaml` | 별도 AppProject — destination `cc-prototype-prod` 만, cluster 리소스는 Namespace 만 |
| `charts/cloudflared/values.yaml` | hosts 에 `ccc.medisolveai.xyz` **한 줄만** 추가 |
| `provisioning/secrets/cc-prototype-prod.env.example` | `SONIOX_API_KEY=` (키만) |
| `docs/cc-prototype-deploy.md` | 런북 — Secret 4개 · DNS · AppProject · 수동 sync · 검증 |

front 리포트(deploy-fe-report) 반영: probe `/login` · 포트 3600 · uid 1000 · pull secret.
back 리포트(deploy-be-report) 반영: 이벤트는 Secret 에 `event-<scheduleId>.json` 평평하게 · uid 10001 → fsGroup 10001 · GHCR private 대비 pull secret 참조 · 시드는 DB 빌 때 한 번(문서에 재시드 절차 명시).

## 검증

| 항목 | 결과 |
|---|---|
| `helm lint charts/cc-prototype -f values-prod.yaml --set image.tag=test` | 0 failed (INFO: icon 권장만) |
| `helm template … -f values-prod.yaml --set image.tag=test` | 성공 — 7개 리소스(ConfigMap · PVC · Service×2 · Deployment×2 · Ingress), YAML 파싱 OK |
| tag 없이 렌더 | 의도대로 실패: `image.tag is not set — inject the arm64 commit-sha tag …` |
| `kubectl apply --dry-run=client` | **못 돌림** — 이 호스트에 kubeconfig 없음(`~/.kube` 없음, localhost:8080 거부). `--validate=false` 로도 REST 매핑에 API 서버가 필요. kubeconform 도 없음 → 클러스터 접근 있는 곳에서 1회 필요 |
| 문서의 scenario Secret 생성 루프 | 실제 데이터로 `--dry-run=client -o json`(클러스터 불필요) → 키 9개(`seed.json` + `event-*.json` 8) 확인, 값 출력 · 적용 없음 |
| 시크릿 값 | 0 (env.example 빈 값, 차트는 이름만) |
| 다른 앱 | 무수정 (cloudflared values 한 줄 추가만) |

## 사용자/코디 할 일 체크리스트

- [ ] 이 브랜치 커밋 · PR · main 머지
- [ ] Actions 로 back · front arm64 이미지 빌드 → `charts/cc-prototype/values-prod.yaml` 의 `image.tag`(sha 가 다르면 `back.imageTag` / `front.imageTag`) 채워 커밋
- [ ] AppProject: `kubectl apply -f argocd/projects/cc-prototype.yaml` (root 앱은 projects/ 를 안 봄)
- [ ] Secret 4개 (ns `cc-prototype-prod`):
```bash
NS=cc-prototype-prod
BACK=/Users/kknaks/orca/workspaces/cc-prototype/sts-prototype/cc/back
kubectl create namespace $NS --dry-run=client -o yaml | kubectl apply -f -
# SONIOX — provisioning/secrets/cc-prototype-prod.env 에 값 채운 뒤
kubectl -n $NS create secret generic cc-prototype-secret \
  --from-env-file=provisioning/secrets/cc-prototype-prod.env --dry-run=client -o yaml | kubectl apply -f -
# scenario — events/<id>.json → event-<id>.json 평평하게
ARGS=(--from-file=seed.json="$BACK/data/scenario/seed.json")
for f in "$BACK"/data/scenario/events/*.json; do ARGS+=(--from-file="event-$(basename "$f")=$f"); done
kubectl -n $NS create secret generic cc-prototype-scenario "${ARGS[@]}" --dry-run=client -o yaml | kubectl apply -f -
# staff (이름 · 이메일 가짜로 바꾼 파일 — D-04)
kubectl -n $NS create secret generic cc-prototype-staff \
  --from-file=kos-staff.json="$BACK/data/kos-staff.json" --dry-run=client -o yaml | kubectl apply -f -
# GHCR pull (read:packages PAT)
kubectl -n $NS create secret docker-registry ghcr-pull \
  --docker-server=ghcr.io --docker-username="$GH_USER" --docker-password="$GHCR_PAT"
```
- [ ] DNS: `cloudflared tunnel route dns b9610413-2b11-42b5-ba36-5a5e7affe8e4 ccc.medisolveai.xyz`
- [ ] cloudflared 앱 sync(자동이 아니면 `argocd app sync cloudflared`)
- [ ] `argocd app sync cc-prototype-prod` (수동)
- [ ] 검증: `curl -fsS https://ccc.medisolveai.xyz/api/health` · `curl -N https://ccc.medisolveai.xyz/api/events`(60초 넘게 유지) · 통역 화면에서 `wss://…/api/interpret` 101
- [ ] `kubectl apply --dry-run=client` — 클러스터 접근 있는 곳에서 렌더 결과로 1회

## 미결 · 주의

1. scenario/staff Secret 에 쓸 데이터가 **D-04 가짜 이름 · 이메일 치환본**인지 넣기 전에 확인(인프라는 파일 내용을 안 봤다)
2. 시드는 DB 빌 때만 — Secret 을 바꿔도 이미 시드된 DB 는 그대로. 재시드는 PVC 의 `/data/db/cc.db` · `seed.json` 삭제 후 재시작(파괴적, 명시 결정)
3. `proxy-buffering: off` 는 Ingress 전체(front 포함)에 걸린다 — PoC 에선 무해
4. 공개 주소 → Soniox 과금 노출(DEC-003 위험) — 시연 뒤 내리거나 Cloudflare Access

---

## fix1 — back PVC Pending (local-path 는 lima-worker-1 만) · 2026-10-13

브랜치 `kknaksss/cc-prototype-fix1`(origin/main 38df634 에서), 커밋 · push 없음.

| 파일 | 변경 |
|---|---|
| `charts/cc-prototype/values.yaml` | `back.nodeSelector: {}` 유지 + 이유 주석(local-path 는 nodePathMap 노드에만 만든다 · 환경별 값) |
| `charts/cc-prototype/values-prod.yaml` | `back.nodeSelector: { kubernetes.io/hostname: lima-worker-1 }` + 이유 주석(datastores 와 같은 근거) |

템플릿은 이미 `back.nodeSelector` 를 렌더하게 돼 있어 수정 없음. front 는 PVC 가 없어 그대로 둠.

검증: `helm lint -f values-prod.yaml` 0 failed · `helm template -f values-prod.yaml` 성공(7 리소스) — back Deployment 에 `nodeSelector: kubernetes.io/hostname: lima-worker-1`, 이미지 태그 `2abe7044…` 그대로.

코디 할 일: **PVC 삭제 후 sync** — 이미 생긴 Pending `cc-db` 에 `volume.kubernetes.io/selected-node: lima-worker-2` 가 붙어 있을 수 있다(삭제는 파괴적이라 코디 몫).
