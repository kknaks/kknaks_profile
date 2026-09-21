# k8s_infra_mac 조사 리포트

- 조사 대상: `/Users/kknaks/git/harness_works/k8s_infra_mac` (브랜치 `main`, HEAD `46fdf88`)
- 조사 방식: 레포 파일 읽기만. `kubectl` 미실행, 대상 레포 파일 변경 없음
- 조사일: 2026-09-20

---

## 0. 조사 범위와 방법

- 읽은 것: 레포 전체 파일(총 78개, `.git` 제외). 아래 디렉토리 전부
  - `PRD.md` · `README.md` · `Makefile` · `.gitignore` · `.claude/settings.local.json`
  - `lima/` — VM 정의 3 + `networks.yaml`
  - `provisioning/` — `host/` 4, `guest/` 7, 최상위 스크립트 5, `kubeadm-config.yaml`, `secrets/*.example` 2
  - `infra/` — `calico/` `metallb/` `ingress-nginx/` `local-path/` `headlamp/`
  - `charts/` — `mediness` `datastores` `cloudflared` `kakao-tracker` `private-pypi` `arc-controller` `arc-runners-medisolve`
  - `argocd/` — `root-app.yaml`, `applications/` 8, `projects/` 4, `repo/repository.yaml.tmpl`
  - `docs/` — 10개 문서
- 읽지 않은 것: `docs/private-pypi-secrets.md` (`.gitignore:10` 으로 제외, `git ls-files docs/` 에 없음 = 미추적). 자격증명 파일이라 내용을 열지 않았다
- 실행하지 않은 것: `kubectl` · `limactl` · `helm` · `git` 상태 변경 명령. 런타임 사실은 전부 「확인 불가」(§8)

---

## 1. k8s 구성

**배포판 · 버전**

- vanilla Kubernetes, **kubeadm** 로 부트스트랩. k3s/minikube/kind/Docker Desktop 아님 — `README.md:15` (`Lima (vz 백엔드) + kubeadm — vanilla k8s v1.36`), `PRD.md:42`
- apt 저장소 핀: `K8S_MINOR="v1.36"` — `provisioning/guest/20-kube-packages.sh:8`
- 실측 기록 버전: k8s **v1.36.2**, containerd **2.2.5**, Calico **v3.32.1** — `docs/build-plan.md:74`
- 핀 버전 목록: Lima 2.1.3 · kubectl v1.36 · helm 3 · k8s v1.36.2 · containerd 2.x(SystemdCgroup) · Calico v3.32.1 · MetalLB v0.16.1 · ingress-nginx v1.14.3(⚠archived) · local-path v0.0.36 · ArgoCD 3.3 — `docs/build-plan.md:41`
  - 단, 스크립트 실값은 ArgoCD **v3.4.4** (`provisioning/gitops.sh:8`), MetalLB **v0.16.1** (`provisioning/base.sh:7`), Calico **v3.32.1** (`provisioning/bootstrap.sh:10`)
- CRI: containerd (Docker apt 저장소의 `containerd.io`), `SystemdCgroup = true` — `provisioning/guest/10-containerd.sh:29,34`
- cgroupDriver: systemd — `provisioning/kubeadm-config.yaml:25`

**호스트 · 가상화**

- 물리 1대: Mac Studio M2 Ultra, 24코어/64GB/2TB SSD, macOS 15.7.7, arm64 — `PRD.md:37`
- Lima VM 3대, 백엔드 `vmType: vz` — `lima/master.yaml:8`, `lima/worker-1.yaml:4`, `lima/worker-2.yaml:3`
- 게스트 OS: Ubuntu 24.04 server cloudimg arm64 — `lima/master.yaml:13`

**노드 수 · 사이징**

| 노드 | 역할 | CPU/RAM/root disk | k8s0 정적 IP | 근거 |
|---|---|---|---|---|
| master | control-plane 전용(taint 유지) | 2C / 4GiB / 30GiB | 192.168.105.11 | `lima/master.yaml:16-18,46`, `provisioning/kubeadm-config.yaml:13` |
| worker-1 | worker + pgdata 디스크 소유 | 4C / 12GiB / 60GiB | 192.168.105.12 | `lima/worker-1.yaml:12-14,55` |
| worker-2 | worker | 4C / 12GiB / 60GiB | 192.168.105.13 | `lima/worker-2.yaml:11-13,37` |

- 합계 10코어 / 28GB, 호스트 여유 ≈ 14코어 / 36GB — `PRD.md:50`
- master 는 control-plane taint 유지 → 워크로드 스케줄 안 됨 — `provisioning/kubeadm-config.yaml:13`, 실측 `docs/build-plan.md:73`
- HA 아님(control-plane 1대, 단일 물리 서버) — `PRD.md:24`

**CIDR**

- Pod `10.244.0.0/16`, Service `10.96.0.0/12` — `provisioning/kubeadm-config.yaml:20-21`
- controlPlaneEndpoint `192.168.105.11:6443` — `provisioning/kubeadm-config.yaml:18`

**매니페스트 형태 — 혼합**

- raw yaml: `infra/` 전부(`calico/installation.yaml`, `metallb/pool.yaml`, `local-path/local-path-storage.yaml`, `headlamp/*.yaml`), `argocd/` 전부
- Helm 차트(직접 작성): `charts/mediness` `charts/datastores` `charts/cloudflared` `charts/kakao-tracker` `charts/private-pypi`
- Helm wrapper 차트(의존성 = OCI 업스트림): `charts/arc-controller` (`Chart.yaml:7-10`), `charts/arc-runners-medisolve` (`Chart.yaml:7-10`) — 각각 `charts/*.tgz` 로 벤더됨
- 업스트림 원격 매니페스트 직접 apply: Calico operator(`provisioning/bootstrap.sh:73-74`), MetalLB(`provisioning/base.sh:10-11`), ArgoCD(`provisioning/gitops.sh:14-15`)
- 업스트림 helm repo 설치: ingress-nginx(`provisioning/base.sh:21-25`), headlamp(`provisioning/headlamp.sh:10-15`)
- kustomize 사용 흔적 **없음** (레포에 `kustomization.yaml` 없음)

**네임스페이스 구조** (레포에 등장하는 것 전부)

| ns | 생성 주체 | 근거 |
|---|---|---|
| `mediness-dev` / `mediness-prod` | ArgoCD `CreateNamespace=true` + `secrets.sh` | `argocd/applications/mediness-{dev,prod}.yaml:17,20`, `provisioning/secrets.sh:9,14` |
| `argocd` | `argocd/install/namespace.yaml:5` | 〃 |
| `cloudflared` | Application destination | `argocd/applications/cloudflared.yaml:14` |
| `kakao-tracker` | Application + `secrets.sh` | `argocd/applications/kakao-tracker.yaml:14`, `provisioning/secrets.sh:51-52` |
| `private-pypi` | Application | `argocd/applications/private-pypi.yaml:14` |
| `arc-system` / `arc-runners` | Application + `secrets.sh` | `argocd/applications/arc-controller.yaml:14`, `arc-runners-medisolve.yaml:14`, `provisioning/secrets.sh:95-97` |
| `ingress-nginx` | `helm --create-namespace` | `provisioning/base.sh:24` |
| `metallb-system` | 업스트림 매니페스트 | `infra/metallb/pool.yaml:9` |
| `local-path-storage` | `infra/local-path/local-path-storage.yaml:10` | 〃 |
| `headlamp` | `helm --create-namespace` | `provisioning/headlamp.sh:15` |
| `monitoring` | **설계만 있고 매니페스트 없음** | `PRD.md:127` vs `argocd/applications/` 에 없음 |

**AppProject 4개**: `mediness` · `kakao-tracker` · `private-pypi` · `arc` — `argocd/projects/*.yaml`. `cloudflared` 와 `root` 는 `project: default` (`argocd/applications/cloudflared.yaml:7`, `argocd/root-app.yaml:9`)

---

## 2. 현재 워크로드

레포가 선언하는 것 기준(= ArgoCD 가 sync 하는 대상). 실제 기동 상태는 확인 불가(§8).

### 2.1 DB — PostgreSQL (MySQL 은 없음)

- **MySQL / MariaDB 관련 파일·문자열이 레포 전체에 0건.** `grep -rniE 'mysql|mariadb|binlog'` 결과 없음
- PostgreSQL 은 `charts/datastores` 에서 **네임스페이스마다 1세트** (`mediness-dev`, `mediness-prod`)

| 항목 | 값 | 근거 |
|---|---|---|
| 리소스 종류 | **StatefulSet** (`replicas: 1`, `serviceName: postgres`) | `charts/datastores/templates/postgres.yaml:18,25-26` |
| 이미지 | `pgvector/pgvector:pg16` | `charts/datastores/values.yaml:10`, `Chart.yaml:4` |
| 포트 | 컨테이너 5432 / Service `postgres:5432` **ClusterIP** | `charts/datastores/templates/postgres.yaml:9,14-15,42` |
| DB / 사용자 | `mediness` / `mediness` | `charts/datastores/values.yaml:11-12` |
| 비밀번호 | Secret `postgres-secret` 키 `POSTGRES_PASSWORD` (out-of-band 생성) | `charts/datastores/values.yaml:13-15`, `provisioning/secrets.sh:15-22` |
| PGDATA | `/var/lib/postgresql/data/pgdata` (볼륨 루트 아래 서브디렉토리) | `charts/datastores/templates/postgres.yaml:54-55` |
| 볼륨 | `volumeClaimTemplates` `data`, RWO, SC `local-path` | `charts/datastores/templates/postgres.yaml:71-79` |
| 용량 | dev **5Gi** / prod **20Gi** (기본값 10Gi) | `values-dev.yaml:3`, `values-prod.yaml:3`, `values.yaml:16` |
| 배치 | `nodeSelector: kubernetes.io/hostname: lima-worker-1` | `charts/datastores/templates/postgres.yaml:36-37`, `values.yaml:6` |
| probe | `pg_isready` exec (readiness/liveness) | `charts/datastores/templates/postgres.yaml:59-68` |
| 리소스 | dev 기본 req 250m/256Mi lim 1/1Gi · prod req 500m/512Mi lim 2/2Gi | `values.yaml:17-19`, `values-prod.yaml:4-6` |
| 확장 | `vector` / `pg_trgm` / `pgcrypto` — alembic 이 생성(이미지에 포함) | `docs/plan-m5-m8.md:10,49`; 실측 pgvector 0.8.4 `docs/plan-m5-m8.md:45` |
| 복제/WAL 설정 | **레포에 없음** (postgresql.conf override·replica·WAL 아카이브 설정 전무) | §8 |
| 백업 | pg_dump CronJob **없음** — C3 로 연기됨 | `docs/plan-m5-m8.md:32,51`, `PRD.md:114` |

### 2.2 Redis

| 항목 | 값 | 근거 |
|---|---|---|
| 리소스 | StatefulSet, replicas 1 | `charts/datastores/templates/redis.yaml:18,26` |
| 이미지 | `redis:7-alpine` | `charts/datastores/values.yaml:22` |
| 포트 | 6379 / Service `redis:6379` ClusterIP | `charts/datastores/templates/redis.yaml:9,14-15` |
| 영속 | AOF 켬 (`--appendonly yes`) + PVC dev 1Gi / prod 3Gi | `redis.yaml:41`, `values-dev.yaml:5`, `values-prod.yaml:8` |
| 배치 | worker-1 핀 | `charts/datastores/templates/redis.yaml:35-36` |

> ⚠ `PRD.md:112,220` 은 redis 를 「무영속(emptyDir)」로 적었으나, 이후 결정 C4 로 **PVC 영속**으로 바뀌었다 — `docs/plan-m5-m8.md:33`, `charts/datastores/values.yaml:23-25`. 차트가 실물이다

### 2.3 mediness 앱 (ns `mediness-dev`, `mediness-prod`)

| 서비스 | 리소스 | 이미지 | 포트 | 특성 | 근거 |
|---|---|---|---|---|---|
| back | Deployment, replicas 1, `Recreate` | `ghcr.io/medisolveaidev/mediness-back:<tag>` | 28080 | worker-1 핀. PVC 2(docs 5Gi·pyannote 5Gi) + hostPath 3 | `charts/mediness/templates/back.yaml:44,52-53,62-63,97-100`, `values.yaml:7,65-66` |
| worker | Deployment, replicas 1, `Recreate` | `mediness-worker` | 없음 | worker-1 핀. PVC claude 2Gi (+codex 2Gi 조건부), hostPath `/opt/claude`·`/opt/codex` ro | `charts/mediness/templates/worker.yaml:37,44-45,54-55,84-89,97-110` |
| mcp | Deployment, replicas 1 | `mediness-mcp` | 28081 | 무상태, 노드 자유 | `charts/mediness/templates/mcp.yaml:18,24`, `values.yaml:111-113` |
| front | Deployment, replicas 1 | `mediness-front` | 23001 | 무상태, 노드 자유 | `charts/mediness/templates/front.yaml:18,25`, `values.yaml:118-120` |

- 이미지 태그(현재 커밋): prod `366b07565fad617d2eb5ff342c29b6004471d190-arm64` (`charts/mediness/values.yaml:8`), dev `e64b97cfdff1da478ccd221a327c712fc702cbb6-dev-arm64` (`values-dev.yaml:11`)
- DATABASE_URL 은 파드 env 에서 조립: `postgresql+asyncpg://mediness:$(POSTGRES_PASSWORD)@postgres:5432/mediness` — `charts/mediness/templates/back.yaml:106-107`
- 공유 Secret `mediness-secret` 을 `envFrom.secretRef(optional)` 로 주입 — `back.yaml:121`, `worker.yaml:82`, `mcp.yaml:44`

### 2.4 그 외 워크로드

| 앱 | ns | 리소스 | 이미지 | 포트 | 근거 |
|---|---|---|---|---|---|
| cloudflared | `cloudflared` | Deployment, **replicas 2** | `cloudflare/cloudflared:2026.6.1` | metrics 2000 (`/ready` probe) | `charts/cloudflared/values.yaml:10-11`, `templates/deployment.yaml:21` |
| private-pypi | `private-pypi` | Deployment 1 + PVC 10Gi | `pypiserver/pypiserver:v2.4.1` | 컨테이너 8080 / Service 80 | `charts/private-pypi/values.yaml:1-3,9-10,22`, `templates/deployment.yaml:35` |
| kakao-tracker | `kakao-tracker` | Deployment, **replicas 0** (이미지 대기), `Recreate`, PVC 2Gi | `ghcr.io/medisolveaidev/kakao-tracker:e7dd0c7…-arm64` | 9010 (OTP, 첫 로그인 때만) | `charts/kakao-tracker/values.yaml:12-13,23,78`, `templates/deployment.yaml:10,34` |
| ARC controller | `arc-system` | 업스트림 차트 0.14.2, replica 1 | 업스트림 | — | `charts/arc-controller/values.yaml:2-3`, `Chart.yaml:9` |
| ARC runner set | `arc-runners` | `gha-runner-scale-set` 0.14.2, **dind**, min 0 / max 3 | 업스트림 | — | `charts/arc-runners-medisolve/values.yaml:10-17` |
| Headlamp | `headlamp` | 업스트림 helm 차트 + admin-user SA(cluster-admin) | 업스트림 | Service 80 | `provisioning/headlamp.sh:14-18`, `infra/headlamp/admin-user.yaml:23-33` |

- 기반 컴포넌트: Calico(tigera-operator) · MetalLB · ingress-nginx(replica 1) · local-path-provisioner(replica 1) · ArgoCD
- **kube-prometheus-stack / monitoring 은 배포 매니페스트가 없다** — `PRD.md:127`·`docs/plan-m5-m8.md:56-62` 은 계획, `argocd/applications/` · `infra/` 에 해당 파일 없음

---

## 3. 네트워크 / 외부 노출

### 3.1 노드 네트워크 (VM 레벨)

- VM 마다 NIC **2개**: `eth0` = Lima user-mode(ssh + 아웃바운드 인터넷, 기본 라우트), `k8s0` = socket_vmnet(클러스터 트래픽 전용, 정적 IP) — `lima/master.yaml:3-5,31-32`
- socket_vmnet v1.2.2, `/opt/socket_vmnet` 에 root 소유로 설치 — `provisioning/host/01-socket-vmnet.sh:8-9,24`
- **실제 사용 모드는 `shared`(격리 192.168.105.0/24)**. bridged 는 폐기 — `lima/master.yaml:1-7`, `lima/{master,worker-1,worker-2}.yaml` 전부 `networks: - lima: shared`
  - 폐기 사유(기록): 오피스 LAN `192.168.0.0/24` 가 기기 200+ 혼잡 DHCP 망이고 공유기 관리 권한이 없어 예약 블록 확보 불가 → 정적 IP 충돌 — `docs/build-plan.md:19`
  - 토폴로지: `LAN 기기 → 공유기 → [Mac 호스트 192.168.0.156] → VM(192.168.105.x, 격리)`. 호스트는 `bridge100 = 192.168.105.1` 로 VM 에 접근, **LAN 기기는 VM 에 직접 도달 못 함** — `docs/build-plan.md:22-26`
  - ⚠ 불일치: `lima/networks.yaml:6,17-21` 주석은 「클러스터는 ONLY bridged 를 쓴다」고 적혀 있고 `Makefile:11` 은 `MASTER_IP := 192.168.0.161`. 실제 VM 정의·kubeadm·Calico·MetalLB 는 전부 `192.168.105.x`/`shared` 다. `networks.yaml` 은 두 네트워크를 **정의만** 하고, VM 이 고르는 것은 `shared`
- 모든 k8s 주소가 `k8s0` 에 고정 — kubelet `--node-ip`(`provisioning/guest/20-kube-packages.sh:11,16`), Calico `nodeAddressAutodetectionV4.interface: k8s0`(`infra/calico/installation.yaml:12`), MetalLB `L2Advertisement.interfaces: [k8s0]`(`infra/metallb/pool.yaml:22-23`)

### 3.2 CNI / L4

- Calico, VXLANCrossSubnet, `natOutgoing: Enabled`, blockSize 26, pod CIDR 10.244.0.0/16 — `infra/calico/installation.yaml:14-19`
- MetalLB L2, 풀 **192.168.105.240–250** — `infra/metallb/pool.yaml:11-12`
  - ⚠ `docs/build-plan.md:14` 의 확정표는 `192.168.0.240–250` 이지만 같은 문서 `:34` 와 실 매니페스트는 `.105.240–.250`. **매니페스트가 실물**
  - 실측: ingress LB EXTERNAL-IP `192.168.105.240`, 호스트→.240 HTTP 404 확인 — `docs/build-plan.md:84`

### 3.3 Service 타입

- 외부 노출용 LoadBalancer 는 **ingress-nginx 컨트롤러 1개뿐** — `infra/ingress-nginx/values.yaml:5-7` (`controller.service.type: LoadBalancer`, replicaCount 1, 기본 IngressClass)
- 앱 Service 는 전부 **ClusterIP**: postgres·redis(`charts/datastores/templates/*.yaml:9`), back·front·mcp(`charts/mediness/templates/*.yaml` — type 미지정 = ClusterIP), private-pypi(`templates/service.yaml:8`), kakao-tracker(`templates/service.yaml:8`)
- NodePort 사용처 없음

### 3.4 Cloudflare

**cloudflared (in-cluster, `charts/cloudflared`)**

- Deployment replicas **2**, 이미지 `cloudflare/cloudflared:2026.6.1`, `args: ["tunnel","--config","/etc/cloudflared/config.yaml","run"]` — `templates/deployment.yaml:7,18-19`
- **tunnel id `b9610413-2b11-42b5-ba36-5a5e7affe8e4`** — `charts/cloudflared/values.yaml:7` (레포는 「터널 id 는 비밀 아님」으로 명시하고 config 에 둔다 — `values.yaml:5-6`)
- **자격증명은 레포에 없다.** Secret `tunnel-creds` 의 `credentials.json` 을 out-of-band 로 생성해 ro 마운트 — `values.yaml:2-4,8`, `templates/deployment.yaml:35-39`, `provisioning/secrets.sh:113-115`
  - 생성 명령: `kubectl create secret generic tunnel-creds -n cloudflared --from-file=credentials.json=~/.cloudflared/<tunnel-id>.json` — `provisioning/secrets.sh:114-115`
- 토큰 방식(`TUNNEL_TOKEN`) 아님 — credentials-file 방식 — `templates/configmap.yaml:8`
- 전달 대상: `http://ingress-nginx-controller.ingress-nginx.svc.cluster.local:80`, Host 헤더 보존 → ingress 룰 매칭 — `values.yaml:13-15`, `templates/configmap.yaml:14`
- fallback `- service: http_status:404` — `templates/configmap.yaml:16`
- metrics `0.0.0.0:2000`, `no-autoupdate: true` — `templates/configmap.yaml:9-10`

**터널이 서비스하는 공개 호스트 9개** — `charts/cloudflared/values.yaml:19-28`

```
mediness.medisolveai.xyz / mediness-api.* / mediness-mcp.*       (prod)
mediness-dev.medisolveai.xyz / mediness-dev-api.* / mediness-dev-mcp.*  (dev)
pypi.medisolveai.xyz            (private pypi)
dashboard.medisolveai.xyz       (Headlamp — Cloudflare Access 게이트 지시)
kakao-otp.medisolveai.xyz       (kakao-tracker 2FA OTP 폼)
```

- 각 호스트는 DNS CNAME → `<tunnelId>.cfargotunnel.com` 필요, `cloudflared tunnel route dns` 로 생성 — `values.yaml:17-18`, `docs/private-pypi.md:143-147`
- **Cloudflare Access**: 레포에는 **설정 파일이 없다.** 문서상 지시·권고로만 존재 — Headlamp 는 「게이트 필수」(`provisioning/headlamp.sh:32-34`, `infra/headlamp/ingress.yaml:6`), kakao-otp 는 권고(`charts/kakao-tracker/values.yaml:59,70`), private-pypi 는 **초기 롤아웃에서 켜지 않음**(pip/twine 때문) — `docs/plan-private-pypi.md:16,192`
- Cloudflare zone: `medisolveai.xyz` — `charts/mediness/values.yaml:16`. dev 도 **같은 터널**을 쓰고, 단일 레벨 서브도메인만 사용(Universal SSL 이 `a.b.<zone>` 을 못 덮어서) — `values-dev.yaml:4-5`, `charts/mediness/templates/_helpers.tpl:1-3`
- 호스트 레벨 SSH 터널 `medisolve-ssh` 가 별도로 존재하며 이 차트와 무관 — `charts/cloudflared/values.yaml:5-6`. 서버 ssh 접근이 CF Tunnel 경유라는 전제 — `PRD.md:39`

### 3.5 인그레스 (L7)

| Ingress | 호스트 | 백엔드 | 주요 애노테이션 | 근거 |
|---|---|---|---|---|
| `front` | `<prefix>.medisolveai.xyz` | front:23001 | `proxy-body-size: 50m` | `charts/mediness/templates/ingress.yaml:8,14,23` |
| `api` | `<prefix>-api.*` | back:28080 | read/send timeout 3600(WS), body 50m | `ingress.yaml:30,33-35,44` |
| `mcp` | `<prefix>-mcp.*` | mcp:28081 | — | `ingress.yaml:49,56,61` |
| `headlamp` | `dashboard.medisolveai.xyz` | headlamp:80 | WS 용 timeout 3600 | `infra/headlamp/ingress.yaml:10,14-15,19` |
| `private-pypi-read` | `pypi.medisolveai.xyz` `/simple` `/packages` | private-pypi:80 | **basic auth** `private-pypi-read-auth` | `charts/private-pypi/templates/ingress.yaml:5,9-11,18,25` |
| `private-pypi-upload` | `pypi.medisolveai.xyz` `/` | private-pypi:80 | **basic auth** `private-pypi-publisher-auth` | `ingress.yaml:36,40-42,49` |
| `kakao-tracker-otp` | `kakao-otp.medisolveai.xyz` | kakao-tracker:9010 | basic auth 옵션(`authSecretName` 기본 `""` = 없음) | `charts/kakao-tracker/templates/ingress.yaml:8,11-16`, `values.yaml:70` |

- **TLS 는 전부 Cloudflare 엣지에서 종결.** cert-manager 없음, cloudflared→ingress-nginx 구간은 평문 HTTP — `PRD.md:27,107`, `charts/mediness/templates/ingress.yaml:2-3`, `infra/headlamp/ingress.yaml:4`

### 3.6 외부 → 클러스터 진입 경로 (레포가 선언하는 전부)

1. **인터넷 → Cloudflare 엣지 → Tunnel(아웃바운드 연결) → cloudflared 파드 → ingress-nginx:80 → Service** — 인바운드 포트 개방 없음 — `PRD.md:107`, `charts/cloudflared/values.yaml:15`
2. **호스트(Mac) → MetalLB IP `192.168.105.240`** — 호스트에서만 도달, LAN 기기는 못 봄 — `docs/build-plan.md:34,84`
3. **호스트 포트포워딩** — dev LAN 접근은 「M6/M8 에서 해결, 지금 불필요」로 기록만 됨. 구현 파일 없음 — `docs/build-plan.md:36`
4. ArgoCD UI: `kubectl port-forward --address 0.0.0.0 svc/argocd-server 8081:443` → `https://192.168.0.156:8081` — `provisioning/gitops.sh:38-39`
5. Headlamp LAN: `kubectl -n headlamp port-forward svc/headlamp 8443:80` — `provisioning/headlamp.sh:29`

### 3.7 클러스터 → 외부(아웃바운드) 제약

- **NetworkPolicy 가 레포에 하나도 없다.** `grep -rniE 'networkpolicy|egress'` 결과는 `PRD.md:104` 의 「Calico 가 NetworkPolicy 지원」 언급 1건뿐 — 실제 정책 리소스 0개
- Calico `natOutgoing: Enabled` → 파드 아웃바운드는 노드 IP 로 SNAT — `infra/calico/installation.yaml:18`
- 노드 아웃바운드 인터넷은 **user-mode NIC `eth0`** 경유(기본 라우트), `k8s0` 에는 기본 라우트 없음 — `lima/master.yaml:4-5,31-32`. 실측 「VM 인터넷 OK(eth0 경유)」 — `docs/build-plan.md:37`
- 파드가 **Mac 호스트에 도달 가능**한 실사용 사례: dev back 의 로컬 LLM 호출 `192.168.105.1:1234` (호스트 LM Studio) — `charts/mediness/values-dev.yaml:18`
- 아웃바운드로 실제로 나가는 경로(레포가 요구하는 것): GHCR 이미지 pull, `claude.ai/install.sh`·GitHub releases(노드 프로비저닝, `provisioning/guest/40-claude.sh:33`·`41-codex.sh:55`), GitHub(ArgoCD repo sync, ARC 러너 등록, docs git clone `back.yaml:81`), Cloudflare 터널
- HTTP 프록시 설정(`HTTP_PROXY`/`NO_PROXY`) 흔적 없음
- 회사 방화벽·아웃바운드 차단 정책에 대한 기록 없음 → §8

---

## 4. 스토리지

**StorageClass — `local-path` 1개뿐(기본)**

- rancher local-path-provisioner **v0.0.36**, 업스트림 매니페스트를 벤더하고 2군데 수정 — `infra/local-path/local-path-storage.yaml:1-6,97`
- `provisioner: rancher.io/local-path`, `volumeBindingMode: WaitForFirstConsumer`, `reclaimPolicy: Delete`, `is-default-class: "true"` — `local-path-storage.yaml:124-129`
- **nodePathMap 이 `lima-worker-1` 단 하나** → `/mnt/lima-pgdata/local-path` — `local-path-storage.yaml:140-146`
  - 결과: PVC 를 쓰는 파드는 반드시 worker-1 에 스케줄돼야 함. `nodeName` 을 쓰면 스케줄러를 우회해 PVC 가 영구 Pending — `local-path-storage.yaml:3-5`, `charts/datastores/values.yaml:3-6`, 교훈 `docs/build-plan.md:85`
- 다른 StorageClass·CSI 드라이버 없음

**물리 디스크 — Lima 독립 데이터 디스크 `pgdata`**

- `limactl disk create pgdata --size 100GiB --format raw` — `provisioning/host/02-create-data-disk.sh:8-9,17` (raw: vz 가 직접 마운트, qcow2 면 매 부팅 변환)
- worker-1 에만 `additionalDisks: [{name: pgdata, format: true, fsType: ext4}]` 로 붙음. **VM 삭제·재생성에도 데이터 생존**이 목적 — `lima/worker-1.yaml:24-30`
- 실측 마운트: `vdb1` ext4 → `/mnt/lima-pgdata`, 여유 93G — `docs/build-plan.md:62`
- `make destroy` 는 VM 만 지우고 디스크 보존, `make clean-all` 이 디스크까지 삭제 — `Makefile:79-89`
- ⚠ 미검증 항목으로 명시: `format: true` 라 VM 재생성 시 재포맷되지 않는지 확인 필요 — `docs/build-plan.md:64`, `docs/plan-m5-m8.md:46`

**호스트 경로 마운트 (Mac SSD 직결)**

- Lima virtiofs 마운트: worker-1 만 `~/mediness-data` (Mac) → `/mnt/mac` **writable** — `lima/worker-1.yaml:32-39`
- 파드 hostPath (전부 `DirectoryOrCreate`, back 파드) — `charts/mediness/templates/back.yaml:146-151`
  - audio: prod `/mnt/mac/audio` · dev `/mnt/mac/audio-dev` — `values.yaml:54`, `values-dev.yaml:21`
  - department-space: `/mnt/mac/department-space{,-dev}` — `values.yaml:55`, `values-dev.yaml:22`
  - task-references: `/mnt/mac/task-references{,-dev}` — `values.yaml:56`, `values-dev.yaml:23`
- 파드 hostPath (`type: Directory` — 없으면 파드가 그 자리에서 실패): `/opt/claude`(back·worker), `/opt/codex`(worker, ro) — `back.yaml:156-159`, `worker.yaml:97-110`
- 저장 이원화 원칙 기록: DB 원본 = pgdata 디스크(PVC) / 파일류(오디오·백업·문서) = Mac SSD — `docs/plan-m5-m8.md:37-41`

**PVC 목록과 용량 (레포 선언 전부)**

| PVC | ns | 용량 | 근거 |
|---|---|---|---|
| `data-postgres-0` (STS template) | mediness-dev / -prod | 5Gi / 20Gi | `values-dev.yaml:3`, `values-prod.yaml:3` |
| `data-redis-0` (STS template) | mediness-dev / -prod | 1Gi / 3Gi | `values-dev.yaml:5`, `values-prod.yaml:8` |
| `back-docs` | mediness-* | 5Gi | `charts/mediness/values.yaml:65`, `templates/back.yaml:5-15` |
| `back-pyannote` | mediness-* | 5Gi | `values.yaml:66`, `back.yaml:18-28` |
| `worker-claude` | mediness-* | 2Gi | `values.yaml:84`, `worker.yaml:5-15` |
| `worker-codex` (codexEnabled 일 때) | mediness-* | 2Gi | `values.yaml:90`, `worker.yaml:22-33` |
| `kakao-tracker-state` | kakao-tracker | 2Gi | `charts/kakao-tracker/values.yaml:78`, `templates/pvc.yaml:13-14` |
| `packages` | private-pypi | 10Gi | `charts/private-pypi/values.yaml:22`, `templates/pvc.yaml:10-13` |

- 전부 `accessModes: ReadWriteOnce`, SC `local-path`
- 합계 선언 용량(prod+dev 동시 기준): 약 **55Gi** — pgdata 100GiB 안에서 소화
- PV 를 직접 선언한 매니페스트는 없다(전부 동적 프로비저닝)

---

## 5. 시크릿 관리

**방식: 전부 수동 `kubectl create secret` (out-of-band). sealed-secrets · SOPS · 외부 저장소 없음.**

- 결정 C1 = 「직접 생성 + gitignore」. 하드닝(Sealed Secrets)은 **후속으로 미룸** — `docs/plan-m5-m8.md:30`
- 실행 창구: `provisioning/secrets.sh` — 멱등·비파괴(이미 있으면 유지, postgres 비번은 DB init 에 구워지므로 재생성 금지) — `provisioning/secrets.sh:3-5,15-17`

| Secret | ns | 원천 | 근거 |
|---|---|---|---|
| `postgres-secret` | mediness-dev/prod | 스크립트가 `/dev/urandom` 32자 생성, `POSTGRES_PASSWORD=` 로 override 가능 | `secrets.sh:11,18-21` |
| `mediness-secret` | mediness-dev/prod | **gitignore 된 env 파일** `provisioning/secrets/mediness-{dev,prod}.env` → `--from-env-file` | `secrets.sh:27,31-35` |
| `ghcr-pull` (kakao-tracker) | kakao-tracker | 셸 env `GH_USER`+`GHCR_PAT`(read:packages) → docker-registry secret | `secrets.sh:56-64` |
| `kakao-tracker-secret` | kakao-tracker | gitignore 된 `secrets/kakao-tracker.env` (SLACK_BOT_TOKEN·SLACK_CHANNEL_ID·KAKAO_ID·KAKAO_PW) | `secrets.sh:66-89` |
| `arc-github` | arc-runners | gitignore 된 `secrets/arc.env` 의 `GITHUB_TOKEN`(classic, repo/admin:org) | `secrets.sh:91-107`, `charts/arc-runners-medisolve/values.yaml:3,8` |
| `ghcr-pull` (mediness-prod) | mediness-prod | **스크립트 밖**, 수동 `kubectl create secret docker-registry` | `secrets.sh:109-112` |
| `tunnel-creds` | cloudflared | **스크립트 밖**, `~/.cloudflared/<tunnel-id>.json` 파일에서 | `secrets.sh:113-115` |
| `private-pypi-read-auth` / `private-pypi-publisher-auth` | private-pypi | `htpasswd -Bbn` 결과를 수동 `--from-file=auth` | `docs/private-pypi.md:116-135` |
| `repo-k8s-infra-mac` (ArgoCD) | argocd | `.tmpl` 을 `GITHUB_PAT` 로 렌더해 apply. 렌더 결과는 gitignore | `provisioning/gitops.sh:19-25`, `argocd/repo/repository.yaml.tmpl:2-3,14-15` |
| `admin-user-token` (Headlamp) | headlamp | SA 토큰 — k8s 토큰 컨트롤러가 런타임에 채움, git 에 값 없음 | `infra/headlamp/admin-user.yaml:4-7,14-21` |

**레포에 커밋돼 있는가 — 실값은 없다**

- `.gitignore:1-13`: `*.pat` `*.token` `*.key` `*-secret.yaml` `provisioning/secrets/*.env`(단 `*.env.example` 은 허용) `argocd/repo/repository.yaml` `docs/private-pypi-secrets.md` `.env` `kubeconfig` `*.kubeconfig`
- 커밋된 것은 **템플릿·예시 뿐**: `provisioning/secrets/mediness-prod.env.example` (키 이름만, 값 전부 빈칸 — `:15-46`), `arc.env.example` (`GITHUB_TOKEN=ghp_replace_me` — `:3`), `argocd/repo/repository.yaml.tmpl` (`__GITHUB_PAT__` 플레이스홀더)
- `charts/kakao-tracker/templates/secret.yaml` 은 `secret.create=false` 로 **비활성**이며 렌더돼도 값이 빈 문자열 — `:1,22-26`, `values.yaml:37`
- 비밀 아닌 것으로 명시돼 커밋된 값: cloudflare tunnel id `b9610413-…`(`charts/cloudflared/values.yaml:5-7`), Slack 채널 ID `C0APPU6UG4X`(`charts/mediness/values-prod.yaml:14`)
- `docs/private-pypi-secrets.md` 는 디스크에 존재하나 **git 미추적**(`.gitignore:10`, `git ls-files docs/` 에 없음). 내용은 열지 않았다
- 시크릿 변경 시 자동 롤아웃: `secrets.sh` 가 apply 결과가 `unchanged` 가 아니면 `kubectl rollout restart` — `secrets.sh:36-40,81-85`

---

## 6. 배포 흐름

### 6.1 이미지 빌드 — 이 레포는 빌드하지 않는다

- **이 레포에 `.github/` 디렉토리가 없다.** Dockerfile·compose 파일도 없다
- 이미지 빌드는 **각 앱 레포의 GitHub Actions 소관**으로 명시 — `PRD.md:26,117`
  - mediness: `mediness-app` 레포의 `build-k8s.yml` — `charts/mediness/values-dev.yaml:2-3`
  - kakao-tracker: `MediSolveAIDev/kakao_tracker` → `.github/workflows/build-k8s.yml`, `runs-on: ubuntu-24.04-arm` — `docs/kakao-tracker-deploy.md:8,29,111`

### 6.2 레지스트리

- **GHCR(원격), private** — `ghcr.io/medisolveaidev` — `charts/mediness/values.yaml:7`, `charts/kakao-tracker/values.yaml:12`
- 태그 규약: `<sha>-arm64` (prod) / `<sha>-dev-arm64` (dev). `latest` 금지 — `charts/mediness/values-dev.yaml:2-4`, `charts/kakao-tracker/values.yaml:7-10`
- pull 인증: `imagePullSecrets: [ghcr-pull]` — `charts/mediness/values.yaml:10-11`, `charts/kakao-tracker/values.yaml:19-20`
- 퍼블릭 이미지 직접 pull: pgvector·redis·cloudflared·pypiserver·local-path-provisioner·`alpine/git:latest`(initContainer, `back.yaml:70`)
- **로컬 레지스트리 없음.** 단, 별도 자산으로 **사내 Private PyPI**(`pypi.medisolveai.xyz`, pypiserver)가 클러스터 안에서 운영됨 — `docs/private-pypi.md:3-12`

### 6.3 배포 — ArgoCD GitOps (app-of-apps)

```
앱 레포 push → GitHub Actions (arm64 빌드) → GHCR push
  → write-back 커밋: 이 레포 charts/*/values*.yaml 의 image.tag 갱신
  → ArgoCD root-app 이 argocd/applications/ 감지 → 자동 sync
```
근거: `docs/kakao-tracker-deploy.md:6-12`, `argocd/root-app.yaml:10-21`. write-back 실물은 git log (`46fdf88 deploy(mediness main): arm64 366b0756…`, `04d588c deploy(mediness dev): …`)

- root-app: `repoURL https://github.com/MediSolveAIDev/k8s_infra_mac.git`, `path argocd/applications`, `targetRevision: main`, `automated{prune,selfHeal}` — `argocd/root-app.yaml:11-21`
- 자식 Application 8개 전부 같은 repoURL, **전부 `targetRevision: main`**, `automated{prune:true, selfHeal:true}` + `CreateNamespace=true` — `argocd/applications/*.yaml`
  - `arc-controller` 는 `ServerSideApply=true` 추가 — `:21`
  - `arc-runners-medisolve` 는 무한 retry(30s~5m) — `:21-25`
- dev/prod 분기 = 같은 차트 + `helm.valueFiles: [values-dev.yaml | values-prod.yaml]` — `argocd/applications/mediness-{dev,prod}.yaml:12-14`, `datastores-{dev,prod}.yaml:12-14`
- ⚠ **브랜치 불일치**: `README.md:61-68` 은 「ArgoCD 는 `k8s-test` 브랜치를 추적한다(main 아님)」고 적었으나, **모든 Application 매니페스트의 `targetRevision` 은 `main`** 이고 deploy write-back 커밋도 `main` 에 쌓인다. `k8s-test` 문자열은 README 3줄에만 존재

### 6.4 로컬(Mac 호스트) → 클러스터 절차 — Makefile 이 진입점

`Makefile` 타겟 전부 — `Makefile:20-89`

| 타겟 | 하는 일 | 줄 |
|---|---|---|
| `make host-prep` | brew(lima/kubectl/helm) + socket_vmnet + sudoers probe | `:22-25` |
| `make disk` | `pgdata` 100GiB 생성 | `:28-29` |
| `make vm-up` | `limactl start` ×3 | `:33-36` |
| `make bootstrap` | 게스트 prep → kubeadm init → join ×2 → claude/codex 설치 → Calico | `:40-41` → `provisioning/bootstrap.sh` |
| `make kubeconfig` | master `admin.conf` → `/tmp/k8s-admin.conf` | `:44-47` |
| `make base` | MetalLB + ingress-nginx + local-path | `:51-52` |
| `make gitops` | ArgoCD + repo Secret + AppProject + root-app (`GITHUB_PAT=…` 필요) | `:56-57`, `gitops.sh:4` |
| `make headlamp` | (옵션) Headlamp | `:60-61` |
| `make status` | `limactl list` + `kubectl get nodes/pods -A` | `:65-68` |
| `make down` / `up` / `destroy` / `reset` / `clean-all` | VM 정지·재기동·삭제·kubeadm reset·디스크까지 삭제 | `:71-89` |

- kubeconfig: master 의 `/etc/kubernetes/admin.conf` 를 호스트 `~/.kube/config` 로 복사(600) — `provisioning/bootstrap.sh:30-33`
- 모든 스크립트가 멱등하게 설계됐다고 명시 — `bootstrap.sh:4`, `base.sh:3`, `gitops.sh:3`
- 재빌드 사다리 3단계(reset → destroy → clean-all) 문서화 — `docs/build-plan.md:104-108`, `README.md:71-77`
- **앱 배포는 `kubectl apply` 직접 금지, ArgoCD 경유** — `charts/kakao-tracker/README.md:7`
- 원격에서 클러스터를 보는 흔적: `.claude/settings.local.json:5` 에 `ssh … medi-me 'kubectl get nodes …'` 허용 규칙 (ssh 호스트 별칭 `medi-me`)

### 6.5 CI 러너 (사내)

- ARC 0.14.2, org 단위 등록 `https://github.com/MediSolveAIDev`, 스케일셋명(=러너 라벨) **`medisolve-arm64`**, min 0 / max 3, **containerMode dind** — `charts/arc-runners-medisolve/values.yaml:7-17`
- 사용법: `runs-on: medisolve-arm64` — `docs/self-hosted-ci.md:13`
- 제약 기록: arm64 전용(x86 바이너리 잡 실패), 동시 3잡, ephemeral pod, **CI 전용 — CD 잡 금지**(긴급시 예외 절차 있음) — `docs/self-hosted-ci.md:27-39,48-75`

---

## 7. 아키텍처 / 플랫폼

**arm64 전제가 명시적이고 강제된다.**

- 비목표로 못박음: 「**x86 워크로드 지원 없음** — 전 구성요소 arm64 네이티브. arm64 미지원 이미지는 도입하지 않는다」 — `PRD.md:28`
- 호스트 게이트: `uname -m != arm64` 이면 스크립트가 **FATAL 종료** — `provisioning/host/00-brew-tools.sh:6-11`
- VM: `arch: aarch64` + Ubuntu 24.04 **arm64** cloudimg — `lima/{master,worker-1,worker-2}.yaml`
- apt 저장소도 arm64 고정: `deb [arch=arm64 …] download.docker.com` — `provisioning/guest/10-containerd.sh:24`
- 노드 바이너리: codex 는 `uname -m` 으로 타겟 선택(`aarch64-unknown-linux-musl`), claude 는 설치 스크립트가 Linux/aarch64 자동감지. 둘 다 「Darwin 바이너리면 파드 안에서 exec-format-error」를 주석으로 경고 — `provisioning/guest/41-codex.sh:36-40,18-19`, `40-claude.sh:12-14`

**이미지에 `platform:` 지정이 있는가 — 없다**

- k8s Pod spec 에는 `platform` 필드 자체가 없고, 이 레포에 Dockerfile·docker-compose·buildx 설정 파일이 없다. 따라서 **플랫폼 지정은 태그 규약(`-arm64` 접미사)으로만 표현**된다 — `charts/mediness/values.yaml:8`, `values-dev.yaml:11`, `charts/kakao-tracker/values.yaml:13`
- 노드 배치용 `nodeSelector` 는 arch 가 아니라 **hostname**(`lima-worker-1`) 기준. arch 기반 selector·affinity 없음 — `charts/datastores/templates/postgres.yaml:36-37` 등
- ingress-nginx: 「arm64 이미지가 업스트림에 있으니 nodeSelector 불필요(워커가 arm64)」 — `infra/ingress-nginx/values.yaml:10`

**x86_64 이미지를 돌린 흔적 — 클러스터 워크로드에는 없다. CI 잡에만 있다**

- 원칙: 「amd64 이미지 빌드/푸시를 여기서 하지 마세요. arm64 러너라 QEMU 크로스빌드로 매우 느려집니다」 — `docs/self-hosted-ci.md:38-39`
- 예외 실증(2026-08-31, GitHub 결제 장애로 호스팅 러너 차단 시): `docker/setup-qemu-action@v3` `platforms: amd64` 로 사내 arm64 러너에서 amd64 이미지를 QEMU 에뮬레이션 빌드해 **전 구간 성공**. 끝나면 `runs-on` 원복 지시 — `docs/self-hosted-ci.md:48-75`
- codex 설치 스크립트가 `x86_64|amd64` 분기를 갖고 있으나, 이 클러스터 노드는 전부 aarch64라 실행되지 않는 분기 — `provisioning/guest/41-codex.sh:38`
- 과거 블로커 기록: mediness CI 가 amd64 전용이라 arm64 클러스터에서 안 떴고, CI 에 `platforms: linux/arm64` 추가가 M8 전제조건이었다(B1) — `docs/plan-m5-m8.md:23`. 현재 태그가 `-arm64` 인 것으로 보아 해소됨

---

## 7-b. 로컬 개발 환경 기록 (레포에 있는 그대로)

- **호스트 툴체인**: Homebrew 로 `lima` · `kubernetes-cli` · `helm` 설치. 실측 lima 2.1.3 / kubectl v1.36.2 / helm 4.2.2 — `provisioning/host/00-brew-tools.sh:18-30`, `docs/build-plan.md:47`
- **호스트 네트워크 환경**: macOS 15.7.7, arm64, 24C/64GB, 유선 LAN `en0` = `192.168.0.156/24`, 게이트웨이 `.1` — `docs/build-plan.md:15`
- **sudo 요건 2건**: `/etc/sudoers.d/lima`(`limactl sudoers` 생성, visudo 검증 후 0440 설치) — `provisioning/host/01-socket-vmnet.sh:36-50`; `/etc/sudoers.d/lima-probe`(`%everyone ALL=(root:wheel) NOPASSWD: /usr/bin/true` — Lima 2.x passwordLessSudo 프리플라이트 통과용) — `provisioning/host/03-lima-sudo-probe.sh:14-19`
- **`networks.yaml` 의 `group: everyone`** 이 없으면 `limactl sudoers` 가 빈 `%` 그룹을 뱉어 visudo 가 거부 — `lima/networks.yaml:11-14`, `docs/build-plan.md:56`
- **Mac 쪽 작업 디렉토리**: `~/mediness-data` (audio / backups / docs) — worker-1 에 virtiofs 쓰기 마운트 → `/mnt/mac`. Finder 로 접근·전송 가능 — `lima/worker-1.yaml:32-39`, `docs/plan-m5-m8.md:37-40`
- **차트 검증 (클러스터 없이)**: `helm lint charts/kakao-tracker` · `helm template kakao-tracker charts/kakao-tracker -f charts/kakao-tracker/values.yaml` — `charts/kakao-tracker/README.md:48-52`. M8 차트도 `helm lint` + `helm template`(dev/prod) 로 검증했다고 기록 — `docs/plan-m5-m8.md:75`
- **개발 브랜치 규약(README 기준)**: 개발·실험은 `main`/feature 브랜치, 배포는 `k8s-test` 에 머지 — `README.md:61-68` (§6.3 의 불일치 참조)
- **로컬 파이썬 패키지 설치**: `~/.netrc` 에 `machine pypi.medisolveai.xyz` + `readonly` 자격 → `pip install --index-url https://pypi.medisolveai.xyz/simple <pkg>` — `docs/private-pypi.md:84-96`
- **dev 로컬 LLM 연동**: dev back 의 `CHAT_BACKEND=local`, 파드 → 호스트 LM Studio `192.168.105.1:1234` — `charts/mediness/values-dev.yaml:18-19`
- **ArgoCD 접속**: `kubectl -n argocd port-forward --address 0.0.0.0 svc/argocd-server 8081:443` → `https://localhost:8081` 또는 `https://192.168.0.156:8081`, user `admin`, 비번은 `argocd-initial-admin-secret` — `provisioning/gitops.sh:36-42`
- **Headlamp 접속**: `kubectl -n headlamp port-forward svc/headlamp 8443:80` → `http://localhost:8443`, 로그인 토큰 `kubectl -n headlamp create token admin-user --duration=24h` — `provisioning/headlamp.sh:27-37`

---

## 8. 확인 불가 항목

레포에서 근거를 찾지 못한 것 전부. 추측하지 않았다.

**런타임 사실 (브리프에 따라 `kubectl` 미실행)**

1. 실제 노드 수·Ready 여부·k8s 패치 버전 — 레포는 선언만. 마지막 실측 기록은 2026-07-03 `docs/build-plan.md:73-74`
2. 현재 실제로 떠 있는 파드·네임스페이스 목록. 특히 `kakao-tracker` 는 `replicas: 0` 선언(`values.yaml:23`)이라 배포됐는지 알 수 없다
3. ArgoCD Application 들의 현재 Sync/Health 상태, **그리고 실제 추적 브랜치** — 매니페스트는 `main`, README 는 `k8s-test`(§6.3). 어느 쪽이 클러스터에 반영돼 있는지 확인 불가
4. PV/PVC 의 실제 Bound 상태와 현재 사용량. `/mnt/lima-pgdata` 잔여 용량(2026-07-03 기준 93G — `docs/build-plan.md:62` 외 최신값 없음)
5. Cloudflare Tunnel 의 현재 Healthy 여부, 실제로 DNS CNAME 이 걸린 호스트가 9개 전부인지
6. Cloudflare **Access** 정책이 실제로 어느 호스트에 걸려 있는지 — 레포에는 설정이 없고 「걸어라」는 지시만 있다(`infra/headlamp/ingress.yaml:6` 등)
7. 노드의 실제 CPU/메모리 여유, 워크로드 실사용량

**레포에 아예 없는 것**

8. **MySQL / MariaDB 관련 일체** — 이미지·차트·문서·문자열 0건. 이 클러스터에 MySQL 이 있다는 근거 없음
9. **PostgreSQL 복제 설정** — `wal_level`·`max_wal_senders`·replication slot·`pg_hba.conf`·`postgresql.conf` override 가 전무. StatefulSet 은 `pgvector/pgvector:pg16` 기본 설정으로 뜬다(`charts/datastores/templates/postgres.yaml:38-70`)
10. **백업 파이프라인** — pg_dump CronJob·백업 스크립트 없음. C3 로 연기됐고(`docs/plan-m5-m8.md:32,51`) `/mnt/mac/backups` 는 계획상 경로로만 언급(`docs/plan-m5-m8.md:41`)
11. **아웃바운드 방화벽·프록시 제약** — NetworkPolicy 0개, `HTTP_PROXY`/`NO_PROXY` 설정 없음, 회사망 아웃바운드 차단 정책 기록 없음. 「제약이 없다」가 아니라 **레포에 기록이 없다**
12. **모니터링 스택** — kube-prometheus-stack 은 `PRD.md:127`·`docs/plan-m5-m8.md:56-62` 에 계획만 있고 `infra/monitoring/` 도 `argocd/applications/monitoring.yaml` 도 존재하지 않는다
13. 외부에서 **클러스터 API(6443)** 에 접근하는 경로 — kubeconfig 를 호스트로 복사하는 것 외에 원격 접근 설정 없음. `.claude/settings.local.json:5` 의 ssh 별칭 `medi-me` 가 무엇을 가리키는지는 레포에 없다
14. 호스트 SSH 터널 `medisolve-ssh` 의 구성 — 「host-level, 별개, 건드리지 않음」이라고만 적혀 있다(`charts/cloudflared/values.yaml:5-6`)
15. `docs/private-pypi-secrets.md` 의 내용 — gitignore·미추적 자격증명 문서라 열지 않았다
16. 앱 레포들의 CI 워크플로 실체(`build-k8s.yml` 등) — 이 레포에 `.github/` 가 없다. 흐름은 `docs/kakao-tracker-deploy.md:6-12` 의 서술로만 확인
17. `format: true` 상태에서 VM 재생성 시 pgdata 재포맷 여부 — 미검증으로 명시됨(`docs/build-plan.md:64`, `docs/plan-m5-m8.md:46`)
18. dev 의 LAN 접근용 호스트 포트포워딩 — 「M6/M8 에서 해결」로만 기록, 구현 파일 없음(`docs/build-plan.md:36`)

**레포 내부 기술 불일치 (어느 쪽이 현재 사실인지 확인 불가)**

19. 네트워크 모드: `lima/networks.yaml:6,17-21` = bridged / VM 정의·kubeadm·MetalLB = shared `192.168.105.x`. 매니페스트 쪽이 일관되나 클러스터 실물은 미확인
20. `Makefile:11` `MASTER_IP := 192.168.0.161` vs `provisioning/kubeadm-config.yaml:9,18` `192.168.105.11`. 단 `MASTER_IP` 는 Makefile 안에서 **사용되는 곳이 없다**
21. MetalLB 풀: `docs/build-plan.md:14` = `192.168.0.240-250` vs `infra/metallb/pool.yaml:12`·`docs/build-plan.md:34` = `192.168.105.240-250`
22. redis 영속: `PRD.md:112,220` = emptyDir vs `charts/datastores` = PVC(C4)
23. ArgoCD 추적 브랜치: `README.md:61-68` = `k8s-test` vs `argocd/**/*.yaml` = `main`
