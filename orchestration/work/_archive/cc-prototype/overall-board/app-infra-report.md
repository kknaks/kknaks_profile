# WORK-009 WP-INFRA — 사진 볼륨 보고 (infra 워커 · 2026-10-27)

계약: SPEC-004 0.4.1 §2.3 · §6.16 ④-b · §7.4 · OQ-626 / DEC-007 D-54 · D-55 · D-68. 커밋 · push · PR 안 함(코디 몫). 클러스터 apply · ArgoCD sync 안 함.

## 1. 바뀐 파일

**infra** `/Users/kknaks/orca/workspaces/k8s_infra_mac/overall-board` · branch `kknaksss/cc-prototype-app-photo`(`origin/main` = `99920a3` 에서 새로 만듦)

| 파일 | 내용 |
|---|---|
| `charts/cc-prototype/templates/back-photo-pvc.yaml`(새) | PVC `procedure-photos` · 1Gi · RWO · `local-path` · `helm.sh/resource-policy: keep`(지우지 않음 D-55) · 백업 없음 · 머리 주석에 **「법적 검토 필요: 신분증 이미지 · 주민번호 처리 — 볼륨 암호화 없음」** + 암호화 안 되는 근거 |
| `charts/cc-prototype/values.yaml` | `back.photo: { enabled: true, pvcName: procedure-photos, dir: /photos, storage: 1Gi }` · `enabled=false` = PVC · 마운트 · env 다 빠짐(back 이 `disabled`) |
| `charts/cc-prototype/templates/back.yaml` | back 컨테이너에 `photos` → `/photos` 마운트 · volumes 에 PVC(주석 같은 문구) |
| `charts/cc-prototype/templates/configmap.yaml` | `PROC_PHOTO_DIR: "/photos"`(ConfigMap 소유 — Secret 에 넣지 않음) |
| `charts/cc-prototype/values-prod.yaml` | 주석만 — 두 번째 PVC 도 lima-worker-1 · 스케줄 · 자원 영향 없음 |
| `provisioning/secrets/cc-prototype-prod.env.example` | `CCC_COUNSELOR_ID=` · `CCC_COUNSELOR_PASSWORD=` · `CCC_COUNSELOR_KOS_ACCOUNT_ID=`(이름만 · 값 없음) · 「NOT here」 목록에 `PROC_PHOTO_DIR` |
| `docs/cc-prototype-deploy.md` | back 줄 아래 사진 PVC 한 줄(암호화 없음 · 법적 검토 문구 · 끄는 법) |

**코드** `/Users/kknaks/orca/workspaces/cc-prototype/overall-board` · branch `kknaksss/overall-board-2`

| 파일 | 내용 |
|---|---|
| `procedure/docker-compose.yml` | (브리프의 `compose*.yml` = 이 파일 하나) back `environment.PROC_PHOTO_DIR: /photos` · `procedure-photos:/photos` · 최상위 `volumes.procedure-photos` · 법적 검토 주석 |
| `procedure/.env.example` | `PROC_PHOTO_DIR=` 한 줄 + 설명 주석. **`CCC_COUNSELOR_*` 는 안 넣음** — 같은 파일을 WP-BE1(상담사 계정)이 만질 자리라 충돌 피함. BE1 이 넣지 않으면 코디가 챙길 것 |

## 2. 암호화(U2 · OQ-626) — **지원 안 함 → 끔 + 법적 검토 주석**

근거(레포 정의 · 이 머신에서 클러스터 직접 조회는 못 함 — 아래 3절):
- 스토리지 클래스는 **`local-path` 하나**(`infra/local-path/local-path-storage.yaml` — rancher local-path-provisioner v0.0.36 · default · `WaitForFirstConsumer` · `reclaimPolicy: Delete`). 이 provisioner 는 hostPath 디렉터리를 만들 뿐(`setup` = `mkdir -m 0777`)이고 **암호화 파라미터가 없다**. 레포에 CSI 드라이버 · 다른 StorageClass 없음
- 아래 디스크: Lima 추가 디스크 `pgdata`(`provisioning/host/02-create-data-disk.sh` — `limactl disk create --format raw` 100GiB · `lima/worker-1.yaml` `format: true · fsType: ext4`) → **LUKS · dm-crypt 없음**. 경로 `/mnt/lima-pgdata/local-path`
- 레포 전체 grep `encrypt|luks|cryptsetup` → 스토리지 관련 0건
- 남는 층은 Mac Studio 호스트 디스크의 FileVault 뿐(켜져 있다면 꺼진 · 도난 디스크만 막음 — VM · 클러스터 안에서 읽는 것은 못 막음). **Mac Studio FileVault 상태는 확인 못 함**(이 작업 머신은 Mac Studio 가 아님) — 사용자가 `fdesetup status` 로 확인하면 보고서 근거가 하나 늘어난다
- 진짜로 켜려면 = 새 StorageClass(LUKS 디스크 · 암호화 CSI) — 클러스터 전체 변경이라 이 차트 범위 밖. 결정대로 「안 되면 없음 + 주석」

주석 자리(infra): `back-photo-pvc.yaml` 머리 · `back.yaml` volumes · `values.yaml` · `configmap.yaml` · docs. 코드 쪽 「사진 저장 함수」 주석은 WP-BE5(backend) 몫(SPEC-004 §2.3).

## 3. lima-worker-1 영향(`99920a3` CPU 예약 98%)

- back 은 **이미** `nodeSelector: lima-worker-1` + PVC `procedure-db` 로 그 노드에 있다. local-path 가 그 노드에서만 만들어지므로 두 번째 PVC 도 같은 노드 → **스케줄 바뀜 없음 · 새 파드 없음 · CPU/메모리 request 변화 0**(렌더 결과 back `requests: cpu 100m · memory 256Mi` 그대로)
- 단, back 은 `strategy: Recreate` 라 머지 · sync 때 back 파드가 한 번 다시 뜬다(옛 파드 내려간 뒤 같은 100m 로 다시 잡음 → 98% 상태에서도 자기 몫이라 Pending 위험 없음. 다른 파드가 그 사이 자리를 먹으면 예외 — 실 sync 때 `kubectl get pods` 로 확인)
- 디스크: 1Gi 는 local-path 가 강제하지 않는 표시값 · 실제는 pgdata 100GiB 공유. 사진 1장 ≤ 5MB(413) — PoC 규모에선 무시할 만

## 4. 검증

| 명령 | 결과 |
|---|---|
| `helm lint charts/cc-prototype -f values-prod.yaml` | 1 chart linted, 0 failed(INFO icon 만) |
| `helm template … -f values-prod.yaml` | 렌더 OK · 8 문서(ConfigMap · PVC ×2 · Service ×2 · Deployment ×2 · Ingress) · YAML 파싱 OK · `PROC_PHOTO_DIR: "/photos"` · 마운트 · PVC 확인 |
| `helm template … --set back.photo.enabled=false` | `photo` 0건(PVC · 마운트 · env 다 빠짐) |
| `kubectl apply --dry-run=client` | **못 함** — 이 머신에 kubeconfig 없음(localhost:8080 거절 · `--validate=false` 도 API 디스커버리 필요). 코디 · 사용자가 Mac Studio 에서 `helm template … | kubectl apply --dry-run=client -f -` |
| `docker compose config`(procedure/) | OK — `PROC_PHOTO_DIR: /photos` · `procedure-photos → /photos` · 최상위 볼륨 |
| compose 재시작 뒤 파일 남음 | **현 이미지 그대로면 실패** → 아래 5절 · Dockerfile 한 줄을 넣은 임시 이미지로는 통과 |

## 5. 막힌 것 · 넘길 것 — **backend(WP-BE5 또는 BE1)에 Dockerfile 한 줄**

- 현 `procedure-back:latest` + 이름 있는 볼륨 `/photos`: 이미지에 `/photos` 가 없어 Docker 가 **root 소유 · 755** 로 만든다 → uid 10001 쓰기 `Permission denied`(실측)
- 고침(제 범위 `procedure/back/**` 밖이라 안 만짐): `procedure/back/Dockerfile` 17행을 `&& mkdir -p /data /photos && chown app:app /data /photos` 로
- 확인: 위 한 줄을 얹은 임시 이미지(FROM procedure-back:latest)로 새 볼륨 → `app:app` 소유 · 쓰기 OK · 컨테이너 restart → 지움 → 새 컨테이너에서 파일 남음. 임시 이미지 · 볼륨 · 컨테이너는 지움(사용자 compose 프로젝트 · 포트 안 건드림)
- k8s 쪽은 이 줄 없이도 된다(local-path 가 디렉터리를 0777 로 만듦) — 그래도 compose 와 맞추려면 넣는 게 좋다

## 6. 미결

- Mac Studio 호스트 FileVault 상태(근거 보강 · 결론은 안 바뀜)
- kubectl dry-run · 실 sync 뒤 `kubectl -n cc-prototype-prod get pvc procedure-photos`(Bound) · back 파드 Running — 코디 · 사용자
- `procedure/.env.example` 의 `CCC_COUNSELOR_*` — WP-BE1 과 겹치지 않게 그쪽에서
- 운영 Secret `cc-prototype-secret` 에 `CCC_COUNSELOR_*` 값 넣기 — 사용자(값은 레포 밖)
- 데모 흔적: 없음(KOS 호출 0 · 클러스터 쓰기 0)
