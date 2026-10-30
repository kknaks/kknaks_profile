# infra 리포트 — 직원 앱 내부 채팅: 사진 볼륨 20Gi · 업로드 한도 100m

- 워크트리: `/Users/kknaks/orca/workspaces/k8s_infra_mac/internal-chat` (base `origin/main` 6fb7b36) · 커밋 없음
- 근거: DEC-009 D-49 ~ D-53 · **D-58(동영상 90MB)** · **D-59(20Gi · 100m)**

## 1. 변경 파일 (3개)

| 파일 | 변경 |
|---|---|
| `charts/cc-prototype/values.yaml` | `back.photo.storage` 1Gi → **20Gi** · `ingress.proxyBodySize` "10m" → **"100m"** · photo 주석(「Small ≤ 5MB」 → 채팅 사진 · 동영상 `<dir>/chat/` · D-58 90MB · Cloudflare 100MB · **크기는 quota 아님 · 기존 PVC 는 resize 안 됨**) · proxyBodySize 주석 신설 |
| `charts/cc-prototype/templates/back-photo-pvc.yaml` | 머리 주석에 채팅 사진 · 동영상 한 줄 추가. 법적 검토 주석 그대로 |
| `docs/cc-prototype-deploy.md` | procedure-photos 1Gi → 20Gi · chat/ 하위 · quota 아님 · **resize 불가 경고와 다시 만드는 절차(결정 있을 때만)** · Ingress 줄에 proxy-body-size 100m |

`values-prod.yaml` 에는 `proxyBodySize` · `photo.storage` 덮어쓰기가 없다 → 손대지 않음. ArgoCD 앱 · AppProject · env.example 무수정. 다른 앱 차트 무수정 · 시크릿 값 0.

## 2. ⚠ 기존 PVC 는 20Gi 로 늘릴 수 없다 (사실)

- `infra/local-path/local-path-storage.yaml` 의 StorageClass `local-path`: `provisioner: rancher.io/local-path` · `volumeBindingMode: WaitForFirstConsumer` · `reclaimPolicy: Delete` · **`allowVolumeExpansion` 없음(=false)**.
- 쿠버네티스 API 서버는 바인딩된 PVC 의 `spec.resources.requests.storage` 증가를 StorageClass 가 `allowVolumeExpansion: true` 일 때만 받는다. 아니면 `forbidden: only dynamically provisioned pvc can be resized and the storageclass that provisions the pvc must support resize` 로 거절.
- → 이 변경을 머지하고 ArgoCD 로 sync 하면 **`PersistentVolumeClaim/procedure-photos` 한 리소스의 apply 가 실패**하고 sync 결과는 Failed / 앱은 OutOfSync 로 남는다. 다른 리소스(Ingress 100m 등)는 적용된다. 데이터는 그대로다.
- **크기는 실제 제한이 아니다**: local-path 는 `lima-worker-1:/mnt/lima-pgdata/local-path/<pv>` 디렉터리일 뿐 quota 가 없다. 지금 1Gi PVC 도 1Gi 넘게 써진다. 실제 한계는 pgdata 디스크 전체(100GiB, 다른 local-path PV 와 공유)다.
- 즉 **동영상을 저장하는 데는 PVC 를 키울 필요가 없다.** 20Gi 는 새 환경(처음 만드는 PVC)과 문서상 예약 값 역할만 한다.

### 코디가 고를 길 (내가 실행한 것 없음)

| 안 | 내용 | 비고 |
|---|---|---|
| A (권장) | 이 PR 은 그대로 두고, prod 기존 PVC 는 그대로 쓴다. sync 실패를 없애려면 ArgoCD 앱에 `ignoreDifferences`(PVC `/spec/resources/requests/storage`) + `syncOptions: RespectIgnoreDifferences=true` 추가 | `argocd/applications/cc-prototype-prod.yaml` — allowed_paths 안. 승인하면 넣는다 |
| B | `values-prod.yaml` 에 `back.photo.storage: 1Gi` 를 덮어써 기존 PVC 와 맞춘다 | D-59 와 글자는 다르지만 동작은 같다 |
| C | PVC 를 20Gi 로 다시 만든다 | 파괴적 · 아래 절차. **하지 않았다** |

### C 절차 (결정이 있을 때만 · 사용자 확인 필요)

1. back 을 0 으로(쓰기 멈춤): ArgoCD 수동 sync 직전에 `kubectl -n cc-prototype-prod scale deploy/back --replicas=0`
2. 데이터 백업: worker-1 에서 `PV` 경로(`kubectl get pv <procedure-photos 의 pv> -o jsonpath='{.spec.local.path}{.spec.hostPath.path}'`) 를 `tar` 로 복사
3. PVC 삭제(`resource-policy: keep` 이라 Helm/Argo 는 안 지운다 → 손으로). StorageClass `reclaimPolicy: Delete` → **PV 디렉터리도 지워진다** — 2 의 백업이 유일한 사본
4. ArgoCD sync → 20Gi PVC 새로 생성(WaitForFirstConsumer — back 이 뜰 때 바인딩)
5. 새 PV 경로로 복원 · 소유권 `10001:10001` · back 재기동 확인

## 3. 노드(lima-worker-1) 디스크 여유 — 레포에서 아는 것만

- 클러스터 접근 **없음**(kubeconfig 없음 · `current-context is not set`) → 실제 사용량은 **pending**.
- pgdata 디스크: 100GiB (`provisioning/host/02-create-data-disk.sh` `SIZE="100GiB"`), local-path 의 유일한 저장소(`nodePathMap → lima-worker-1:/mnt/lima-pgdata/local-path`).
- 레포 values 의 local-path 요청 합(설정값 기준, 실제 사용량 아님): datastores prod 20Gi + 3Gi · strong-hajin 10Gi + 2Gi · private-pypi 10Gi · kakao-tracker 2Gi · mediness docs 5Gi + pyannote 5Gi · mediness worker 2Gi + 2Gi · cc-prototype db 1Gi + photos 1Gi(→20Gi) · dev values 는 별도 → 대략 **63Gi + 이번 +19Gi ≈ 82Gi / 100GiB**. 요청은 강제되지 않으니 실제 여유는 `df` 로 봐야 한다.
- 확인 명령(읽기만): `limactl shell worker-1 -- df -h /mnt/lima-pgdata` · `limactl shell worker-1 -- sudo du -sh /mnt/lima-pgdata/local-path/*`
- 루트 디스크: worker-1 `disk: "60GiB"`(OS + 이미지 + 컨테이너 쓰기 레이어).

## 4. back 컨테이너 임시 디스크 (/tmp)

- `templates/back.yaml`: emptyDir **없음** · `ephemeral-storage` request/limit **없음** · `readOnlyRootFilesystem` 없음 → `/tmp` 는 컨테이너 쓰기 레이어(worker-1 루트 디스크 60GiB) 위.
- Starlette multipart 는 1MB 넘는 파트를 `SpooledTemporaryFile` 로 `/tmp` 에 쓴다 → 동영상 1건 ≈ 90MB, 요청이 끝나면 지워진다. limit 이 없으니 **동영상 때문에 파드가 eviction 되지는 않는다** — 동시 업로드 몇 건이면 수백 MB 수준.
- 남는 위험: 노드 DiskPressure 때 ephemeral request 0 인 파드는 사용량 순으로 먼저 쫓겨난다(`charts/mediness/values.yaml` 주석과 같은 논리). 지금은 문제로 보지 않음. 필요하면 `back.resources.requests.ephemeral-storage: 1Gi`(limit 없이) — **코디 승인 뒤**. 이번엔 안 바꿈.

## 5. 검증

| 항목 | 결과 |
|---|---|
| `helm lint charts/cc-prototype -f values-prod.yaml` | 1 chart linted, 0 failed (INFO: icon recommended) |
| `helm template cc-prototype charts/cc-prototype -f values-prod.yaml` | 8 리소스 렌더 · `procedure-photos` storage `"20Gi"` · `procedure-db` `"1Gi"` · Ingress `proxy-body-size: "100m"` |
| `kubectl apply --dry-run=client` | **실행 불가** — 클러스터 없음(client dry-run 도 API discovery 필요 · `localhost:8080 refused`). 대신 렌더 결과를 YAML 로 파싱해 8 문서 모두 정상 확인 |
| 실배포 · ArgoCD sync · 노드 df | **pending** (클러스터 접근 없음) |

## 6. 계약 · 주의

- 앱 · back 계약 무변경. infra 값만.
- 업로드 경로 한계는 실제로 **Cloudflare 100MB** 가 먼저다 — nginx 100m 은 그 뒤에서 막지 않는 역할. back 의 90MB(D-58) 한도가 둘보다 작아 모순 없음.
- **머지 전에 §2 의 A/B/C 결정이 필요하다** — 그대로 sync 하면 PVC 한 개가 apply 실패로 남는다(데이터 손상은 없음).

## 7. B 처분 (코디 10-29)

- `charts/cc-prototype/values.yaml` `back.photo.storage` 20Gi → **1Gi 로 되돌림** (줄 끝 주석 `# not a quota — see above`).
- photo 주석 바꿈: local-path 는 quota 없음 · 1Gi 넘게 써짐 · 실제 한도 = lima-worker-1 pgdata 디스크(100GiB, 다른 local-path PV 와 공유) · allowVolumeExpansion 없음 → 값을 바꾸면 sync 실패 · 채팅 사진 · 동영상 포함(DEC-009 D-58 · D-59). 「hence 20Gi」 문구는 지웠다.
- 그대로 둔 것: `proxyBodySize: "100m"` · `back-photo-pvc.yaml` 머리 주석 · `docs/cc-prototype-deploy.md`.
- 재검증: `helm lint` (prod) → 1 chart linted, 0 failed · `helm template` (prod) → 8 리소스, `procedure-photos` `"1Gi"` · `procedure-db` `"1Gi"` · `proxy-body-size: "100m"`. 이제 기존 prod PVC 와 크기가 같아 sync 가 실패할 일이 없다.
- ⚠ **docs 가 차트와 안 맞는다**: 지시대로 docs 를 그대로 뒀더니 `docs/cc-prototype-deploy.md` 20 · 26 · 31행에 아직 「20Gi」가 있다(B 전에 쓴 문구). 차트는 1Gi. 「(1Gi, …)」 · 「The 1Gi is a request, not a quota」로 고치는 데 3줄이면 되고, 승인하면 바로 고친다.
- 최종 변경 파일: `charts/cc-prototype/values.yaml` · `charts/cc-prototype/templates/back-photo-pvc.yaml` · `docs/cc-prototype-deploy.md` (커밋 없음).

## 8. docs 정정 (코디 승인 10-29)

- `docs/cc-prototype-deploy.md`: procedure-photos `(20Gi, …)` → `(1Gi, …)` · 「The 1Gi is a request, not a quota — 1Gi 넘게 써짐 · 실제 한도 = lima-worker-1 pgdata 디스크(100GiB, 공유) · D-59 처분 B」 · 다시 만들기 문장에서 20Gi 를 빼고 「`back.photo.storage` 를 바꾸지 마라」로.
- `grep -rn '20Gi' charts/cc-prototype docs` → **0건**.
