---
type: runbook
id: RUNBOOK-002
title: 운영 배포 — Mac Studio k8s 와 데스크톱 앱
status: active
created_at: 2026-10-01
updated_at: 2026-10-03
tags: [product/strong-hajin, doc/runbook, status/active]
links:
  baselines: []
  decisions: ["[[decision-005-tauri-wrapper]]", "[[decision-007-production-deploy]]"]
  specs: ["[[spec-006-tauri-wrapper]]"]
  works: []
  releases: []
sources:
  - orchestration/work/strong-hajin-deploy/report-infra-deploy.md
  - orchestration/work/strong-hajin-deploy/report-fe-release-dmg.md
  - orchestration/work/strong-hajin-deploy/report-fe-flavors.md
  - orchestration/work/strong-hajin-deploy/_RESUME.md
---

# RUNBOOK-002 — 운영 배포

## 목적

운영 서버(`https://ax.medisolveai.xyz`)에 코드 변경을 반영하고, 데스크톱 앱을 서명·공증해 사람들에게 전달한다.
다음 세션은 이 문서만으로 재배포한다. 최초 배포는 2026-10-01 에 했다.

여기 적힌 명령은 **실제로 실행한 것**이다. 비밀번호·토큰·DB 접속 문자열은 어디에도 적지 않는다.
결정의 근거는 [DEC-007](../10-decision/decision-007-production-deploy.md), 환경 현황은 [환경 구성](../40-architecture/deploy/environments.md)에 있다.

## 구성

```text
사람 (medi-ax 앱 · 브라우저)
  → https://ax.medisolveai.xyz            Cloudflare (proxied, TLS 종단)
  → cloudflared (클러스터 안, mediness 와 같은 터널)
  → ingress-nginx
  → ns strong-hajin-prod
      ├ /api/meetings · /api · /health → back:28080   (FastAPI, WebSocket 포함)
      ├ /                              → front:80     (nginx + 빌드한 SPA)
      ├ worker-conversation · worker-material · worker-meeting · worker-report  (back 과 같은 이미지)
      └ postgres-0 (10Gi) · redis-0 (2Gi)          (charts/datastores, 같은 ns)
```

- 프론트·API·WebSocket 은 **같은 origin 하나**다. 세션 쿠키가 그대로 동작하는 조건이다(DEC-005 D-02·D-08).
- back 과 워커 4개는 `lima-worker-1` 에 고정된다. hostPath(`/mnt/mac/strong-hajin/{recordings,materials}`) 와 codex 인증 PVC 를 함께 쓰기 때문이다.
- 노드의 `/mnt/mac` 은 Mac Studio 의 `~/mediness-data` 다.

### 레포 셋

| 레포 | 무엇 | 이 문서에서 쓰는 곳 |
|---|---|---|
| `kknaks/Strong_hajin` (코드) | 백엔드·프론트·데스크톱 셸 | `deploy/k8s/{back,front}.Dockerfile` · `frontend/src-tauri/` · `Makefile` |
| `MediSolveAIDev/k8s_infra_mac` (인프라, 회사 org) | 차트·Argo CD 앱 | `charts/strong-hajin/` · `charts/datastores/values-strong-hajin.yaml` · `argocd/applications/strong-hajin-*.yaml` · `argocd/projects/strong-hajin.yaml` · `charts/cloudflared/values.yaml`(hosts 1줄) |
| `kknaks/kknaks_profile` (문서) | 결정·런북·환경 기록 | 이 문서 |

### 클러스터에 붙는 법

```bash
ssh medi-me
/opt/homebrew/bin/kubectl -n strong-hajin-prod get pods     # 비대화 ssh 는 PATH 가 짧아 절대경로가 필요하다
```

---

## 1. 코드 변경 → 운영 반영 (매번)

### 1-1. 코드 main 머지

Strong_hajin 의 변경을 PR 로 `main` 에 머지한다. 이미지 태그는 그 커밋의 짧은 sha 로 단다.

### 1-2. arm64 이미지 빌드·푸시

Strong_hajin 워크트리 루트에서 실행한다. API 와 워커 4개는 같은 back 이미지를 쓴다.

```bash
docker buildx build --platform linux/arm64 -f deploy/k8s/back.Dockerfile  -t ghcr.io/kknaksss/strong-hajin-back:<sha>-arm64  --push .
docker buildx build --platform linux/arm64 -f deploy/k8s/front.Dockerfile -t ghcr.io/kknaksss/strong-hajin-front:<sha>-arm64 --push .
docker manifest inspect ghcr.io/kknaksss/strong-hajin-back:<sha>-arm64
docker manifest inspect ghcr.io/kknaksss/strong-hajin-front:<sha>-arm64
```

- 푸시에는 `kknaksss` 계정의 `write:packages` 권한이 필요하다(`gh auth refresh -h github.com -s write:packages` → `gh auth token | docker login ghcr.io -u kknaksss --password-stdin`).
- 각 Dockerfile 옆의 `*.Dockerfile.dockerignore` 가 빌드 컨텍스트를 좁힌다. 레포 루트 `.dockerignore` 는 고객 납품용 보호 이미지(`delivery/`) 것이라 건드리지 않는다.
- 데스크톱 셸(`frontend/src-tauri/`)만 바뀐 머지는 웹 이미지에 들어가지 않는다(front 의 dockerignore 가 뺀다). 그때는 이 절이 아니라 §3 이다.

### 1-3. 태그 커밋

인프라 레포 `charts/strong-hajin/values-prod.yaml` 의 `image.tag` 한 줄을 새 태그로 바꿔 PR → `main` 머지.
렌더 확인:

```bash
helm lint charts/strong-hajin -f charts/strong-hajin/values-prod.yaml
helm template strong-hajin charts/strong-hajin -f charts/strong-hajin/values-prod.yaml -n strong-hajin-prod
```

### 1-4. Argo CD 수동 sync

medi-me 에 argocd CLI 가 없어 Application 의 `operation` 필드로 한 번 sync 를 건다.

```bash
kubectl -n argocd patch application strong-hajin-prod --type merge \
  -p '{"operation":{"initiatedBy":{"username":"kknaksss"},"sync":{"revision":"main"}}}'
kubectl -n argocd get application strong-hajin-prod      # Synced / Healthy
kubectl -n strong-hajin-prod get pods                    # 8/8 Running
```

**automated sync 를 꺼 둔 이유:** 첫 배포 때 이 차트는 한 번도 클러스터에서 돌아본 적이 없었다. 잘못된 렌더 하나에
`selfHeal` 이 붙으면 되돌리기·재적용이 반복된다. 수동 sync 가 몇 번 문제없이 돈 것을 본 뒤 켠다(`argocd/applications/strong-hajin-prod.yaml` 주석).
`kubectl rollout restart` 는 pod template 에 `restartedAt` 주석을 남긴다 — 다음 수동 sync 때 원복되며 그게 정상이다.

### 1-5. 확인

```bash
curl -s -o /dev/null -w "%{http_code}\n" https://ax.medisolveai.xyz/          # 200
curl -s https://ax.medisolveai.xyz/health                                       # {"status":"ok","profile":"production"}
curl -s https://ax.medisolveai.xyz/api/auth/providers                           # {"local":true,"oidc":false} — demo_accounts 가 없어야 한다
kubectl -n strong-hajin-prod logs deploy/back --tail=200 | grep -iE "error|traceback"
```

### 되돌리기

- 앱: `values-prod.yaml` 의 태그를 이전 값으로 되돌려 머지 → §1-4 수동 sync.
- 데이터: postgres PVC(10Gi, local-path, worker-1)가 남아 있다. **PVC 를 지워서 되돌리지 않는다.** 되돌리기(rollback)는 이미지 이야기이고 데이터 복구가 아니다.

---

## 2. 최초 1회 — 클러스터를 처음부터 세울 때

2026-10-01 에 한 번 했다. 클러스터를 다시 세울 때만 이 순서로 한다.

1. **AppProject.** root 앱은 `argocd/applications/` 만 보고 `argocd/projects/` 는 보지 않는다.
   ```bash
   kubectl apply -f argocd/projects/strong-hajin.yaml          # argocd ns
   ```
2. **DNS.** medi-me 에서 mediness 와 같은 터널에 이름을 하나 더한다(터널 id 는 `charts/cloudflared/values.yaml` 의 `tunnelId`).
   ```bash
   cloudflared tunnel route dns <tunnelId> ax.medisolveai.xyz
   dig +short ax.medisolveai.xyz A                             # Cloudflare 주소가 나오면 된다
   ```
   cloudflared 의 hosts 목록은 인프라 레포에 이미 있다 — 그 줄이 머지되면 cloudflared 파드 2개가 순서대로 재시작한다(mediness 도 같은 파드를 쓴다).
3. **네임스페이스와 시크릿.** 값은 파이프로만 넘긴다(§4).
   ```bash
   kubectl create ns strong-hajin-prod --dry-run=client -o yaml | kubectl apply -f -
   # ghcr-pull — gh 토큰으로 dockerconfigjson({"auths":{"ghcr.io":{"auth":…}}})을 조립해 stdin 으로
   gh auth token | python3 <조립> | ssh medi-me 'kubectl -n strong-hajin-prod create secret generic ghcr-pull --type=kubernetes.io/dockerconfigjson --from-file=.dockerconfigjson=/dev/stdin'
   # postgres-secret — 키 POSTGRES_PASSWORD, 무작위 값
   printf %s "$(openssl rand -hex 24)" | kubectl -n strong-hajin-prod create secret generic postgres-secret --from-file=POSTGRES_PASSWORD=/dev/stdin
   # strong-hajin-secret — 먼저 빈 시크릿, 키는 다음 줄에서 patch 로
   kubectl -n strong-hajin-prod create secret generic strong-hajin-secret
   ```
   `strong-hajin-secret` 의 키: `SONIOX_API_KEY`(실시간 STT) · `TDL_EMAIL` · `TDL_PASSWORD`(회의실 예약). 원천은 사용자 Mac 의 `~/.config/soniox/env` · `~/.config/theconnect/env`. `TDL_BASE_URL`·`TDL_COMPANY_ID`·`TDL_NOTIFY`·`TDL_HTTP_TIMEOUT_SECONDS` 는 코드 기본값을 쓴다.
   ```bash
   cat ~/.config/soniox/env ~/.config/theconnect/env | python3 <{"stringData":{세 키}} 로 조립> \
     | ssh medi-me 'kubectl -n strong-hajin-prod patch secret strong-hajin-secret --type merge --patch-file /dev/stdin'
   kubectl -n strong-hajin-prod rollout restart deploy/back deploy/worker-{conversation,material,meeting,report}
   ```
   **외부 채널(WORK-011, 2026-10-06 추가)** — 같은 `strong-hajin-secret` 에 키 여덟 + 별도 Secret 하나:
   - 원천 `~/.config/google/env` → `GOOGLE_OAUTH_CLIENT_ID` · `GOOGLE_OAUTH_CLIENT_SECRET` · `GMAIL_PUBSUB_TOPIC` · `GMAIL_PUBSUB_SUBSCRIPTION`
   - 원천 `~/.config/slack/env` → `SLACK_CLIENT_ID` · `SLACK_CLIENT_SECRET` · `SLACK_APP_TOKEN`
   - `AX_EXTERNAL_TOKEN_ENCRYPTION_KEY` — **운영 전용**(로컬과 다름 · Secret 에만 있다). **바꾸면 저장된 OAuth 토큰을 못 연다** — 재생성 금지
   - 별도 Secret `strong-hajin-pubsub-sa`(키 `sa.json`) ← 원천 `~/.config/google/pubsub-sa.json` · worker-external 에 파일로 마운트
   - Google 웹 클라이언트 원본 JSON: `~/.config/google/oauth-web-client.json` · 콘솔 설정 목록: `reference/2026-10-06-strong-hajin-inbox/사용자-설정.md`
   - 명령 전문(파이프로만 · 키 이름·길이 확인): `orchestration/work/_archive/strong-hajin/strong-hajin-inbox/infra-deploy-steps.md` §3
   - 바꾼 뒤 재시작 대상은 `deploy/back deploy/worker-external`
   `apply` 가 아니라 `patch --type merge` 를 쓰는 이유: 이미 있는 다른 키를 지우지 않는다.
4. **hostPath.**
   ```bash
   limactl shell worker-1 -- sudo mkdir -p /mnt/mac/strong-hajin/{recordings,materials,codex-runtime}
   ```
   `codex-runtime` 은 AX(codex) 세션 홈이다(2026-10-02, WORK-008 Phase 4). back·워커 4개가 `/app/.scax/codex-runtime` 으로 함께 쓴다 — 회의 중 back 이 연 세션을 worker-meeting 이 종료 합성 때 이어 가야 해서다. hostPath type 이 `Directory` 라 **이 디렉터리가 없으면 back·워커 다섯이 뜨지 않는다**(Mac 마운트가 빠졌을 때 VM 디스크에 조용히 쓰지 않게 일부러).
5. **datastores sync.**
   ```bash
   kubectl -n argocd patch application strong-hajin-datastores --type merge \
     -p '{"operation":{"initiatedBy":{"username":"kknaksss"},"sync":{"revision":"main"}}}'
   ```
6. **시드 복원.** 원천은 로컬 시드 DB 의 dump 다(로그인 세션 행 제외). 파일은 Git 밖 `~/strong-hajin-deploy-data/strong-hajin-seed.dump`(권한 600)에 있다. 스트림으로만 넘겨 노드·파드에 파일을 남기지 않는다.
   ```bash
   cat ~/strong-hajin-deploy-data/strong-hajin-seed.dump \
     | ssh medi-me 'kubectl -n strong-hajin-prod exec -i postgres-0 -- pg_restore -U strong_hajin -d strong_hajin --no-owner --no-acl'
   ```
   복원 전에 public 테이블이 0 인지 본다. 복원 뒤: members 4 · member_credentials 4 · auth_sessions 0.
7. **앱 sync.** §1-4 와 같다.
8. **codex 인증.** §4 의 전용 로그인 결과를 codex-home PVC 에 넣는다.
   ```bash
   cat ~/strong-hajin-deploy-data/codex-home/auth.json \
     | ssh medi-me 'kubectl -n strong-hajin-prod exec -i deploy/back -- sh -c "umask 077; cat > /root/.codex/auth.json.tmp && mv /root/.codex/auth.json.tmp /root/.codex/auth.json"'
   kubectl -n strong-hajin-prod rollout restart deploy/back deploy/worker-{conversation,material,meeting,report}
   ```

---

## 3. 데스크톱 앱 — 빌드·서명·공증

### 두 판

| 판 | 보이는 이름 | identifier | origin | 상태 |
|---|---|---|---|---|
| 개인 | Strong Hajin | `app.stronghajin.desktop` | **미정** → 「서버 주소가 설정되지 않았습니다」 화면 | 빌드 가능, 배포 안 함 |
| 회사 | `medi-ax` | `app.ax.desktop` | `https://ax.medisolveai.xyz` | 서명·공증본 전달 |

코드는 한 벌이고 판마다 `frontend/src-tauri/flavors/<판>/` 에 설정이 있다(`tauri.conf.json` 오버레이 · `shell.config.json` · `capabilities/product-shell.json`).
기본판은 개인판이다 — 오버레이 없이 도는 `cargo test`·`make tauri-local` 이 회사 주소를 실수로 싣지 않게 하려는 것이다.

**identifier 는 판 안에서 바꾸지 않는다.** 바꾸면 앱 저장소가 새로 잡혀 사용자가 로그아웃된다. 회사판이 `app.stronghajin.desktop` 에서 `app.ax.desktop` 으로 갈라질 때 한 번 그렇게 됐다(그 전 판으로 로그인한 사람은 새로 로그인한다).

### 굽기

Strong_hajin 워크트리 루트에서 실행한다.

```bash
make shell-verify-strict SHELL_FLAVOR=medi-ax
CI=true APPLE_SIGNING_IDENTITY="<Developer ID Application 인증서 이름>" \
  make shell-build SHELL_FLAVOR=medi-ax SHELL_BUILD_ARGS="--bundles app,dmg"
```

- `CI=true`: 헤드리스 세션에서는 dmg 창을 Finder 로 꾸미는 단계가 막혀 빌드가 실패한다. 그 단계만 건너뛴다. 그래서 dmg 창에는 배경·아이콘 배치가 없다(`.app` 과 `Applications` 링크는 있다).
- 인증서 이름은 `security find-identity -v -p codesigning` 의 `Developer ID Application: …` 줄 그대로다(login keychain). 공증 프로필 `AC_NOTARY` 는 `xcrun notarytool history --keychain-profile AC_NOTARY` 로 살아 있는지 본다.
- 서명은 hardened runtime 과 `Entitlements.plist`(마이크) 로 들어간다.

### 공증·확인

```bash
DMG=frontend/src-tauri/target/release/bundle/dmg/medi-ax_0.0.1_aarch64.dmg
xcrun notarytool submit "$DMG" --keychain-profile AC_NOTARY --wait          # status: Accepted
xcrun stapler staple "$DMG"
xcrun stapler staple frontend/src-tauri/target/release/bundle/macos/medi-ax.app
spctl -a -vvv -t install "$DMG"                                              # accepted source=Notarized Developer ID
spctl -a -vvv -t exec frontend/src-tauri/target/release/bundle/macos/medi-ax.app
/usr/libexec/PlistBuddy -c "Print :CFBundleIdentifier" frontend/src-tauri/target/release/bundle/macos/medi-ax.app/Contents/Info.plist   # app.ax.desktop
```

전달본은 `~/Downloads/medi-ax_0.0.1_arm64.dmg` 로 복사했다(2026-10-01). GitHub Releases 발행은 아직 하지 않았다.

### 최종 관문 (preflight)

```bash
cd frontend && node scripts/verify-final-build.mjs --flavor medi-ax --evidence <증거 파일>
```

입력·`shell.config`·capability 의 origin 이 같은지(G1~G4)와 사람이 확인할 항목을 본다. 지금 **M-5(앱 재시작 후 로그인 유지)** 하나가 `pending` 이라 관문이 막혀 있다.
사용자가 설치본으로 로그인 → 종료 → 재실행을 확인하면 증거 파일에 `resolved: true` 로 적고 다시 돌린다. 증거가 없는 항목을 통과로 바꾸지 않는다.

---

## 4. 비밀값 다루는 법

- 비밀값은 **파이프로만** 옮긴다(`cat … | ssh medi-me 'kubectl … --from-file=…=/dev/stdin'`). 화면·로컬 파일·리포트·이 문서에 값을 적지 않는다. 확인은 키 이름과 길이로만 한다.
- **codex 인증은 Strong Hajin 전용 로그인 1회로 만든다.**
  ```bash
  CODEX_HOME=~/strong-hajin-deploy-data/codex-home codex login --device-auth
  ```
  mediness 의 codex PVC 나 사용자 로컬 `~/.codex` 와 **공유하지 않는다**. codex 는 쓸 때마다 refresh token 을 돌려 새로 받는다 — 같은 토큰을 두 곳에서 쓰면 먼저 돈 쪽이 다른 쪽을 끊는다.
  같은 이유로 로컬 `~/strong-hajin-deploy-data/codex-home/auth.json` 은 운영 PVC 와 같은 토큰을 갖고 있으니 **로컬에서 그 CODEX_HOME 으로 codex 를 쓰지 않는다.**
- 시드 dump 에는 실명·메일·비밀번호 해시가 들어 있다. Git 밖(`~/strong-hajin-deploy-data/`, 권한 600)에만 둔다.

---

## 5. 상태 확인

```bash
curl -s -o /dev/null -w "%{http_code}\n" https://ax.medisolveai.xyz/
ssh medi-me '/opt/homebrew/bin/kubectl -n strong-hajin-prod get pods'
ssh medi-me '/opt/homebrew/bin/kubectl -n argocd get applications strong-hajin-prod strong-hajin-datastores'
ssh medi-me '/opt/homebrew/bin/kubectl -n strong-hajin-prod logs deploy/worker-conversation --tail=100'
```

정상: 파드 8개(back · front · worker 4 · postgres-0 · redis-0) 1/1 Running, 두 앱 `Synced Healthy`.
워커에는 readinessProbe 가 없다 — 워커의 Ready 는 「프로세스가 살아 있다」는 뜻이다.

## 6. 알려진 함정

| 함정 | 대응 |
|---|---|
| medi-me SSH(cloudflared access)가 자주 끊긴다 | 명령을 짧고 멱등으로. 긴 작업은 원격에서 `nohup … > /tmp/sh-*.log &` 로 띄우고 로그를 읽는다 |
| 작업하는 Mac 이 잠들면 진행 중인 세션이 끊긴다 | 2026-10-01 인프라 작업 세션이 그렇게 중단됐다(AppProject·DNS 까지 하고 멈춤). 단계마다 결과를 리포트에 적어 두고, 재개 때 이미 된 것을 다시 하지 않는다 |
| 노드 codex 는 0.146.0 이다(개발은 0.158) | AX 턴 생성은 동작한다. 다만 기록 필드(observed_model 등)가 비어 남는다 — 0.146 의 이벤트 형식을 앱 파서가 못 읽는 것으로 추정. 노드 codex 는 mediness 와 공유라 업그레이드는 사용자 결정 |
| 운영 TLS 인증서 만료 **2026-11-28** | Cloudflare 엣지 인증서(Google Trust Services WE1, `*.medisolveai.xyz`). 자동 갱신을 가정하지만 확인하지 않았다. 앱 서명용 Developer ID 인증서는 별개이며 2031-05-26 까지다 |
| dmg 창 꾸밈이 없다 | 헤드리스 빌드(`CI=true`) 때문이다. GUI 세션에서 `CI` 없이 구우면 꾸며지지만 해시가 바뀌므로 다시 공증해야 한다 |
| back·워커가 `ContainerCreating` 에서 멈춘다 | 노드의 `/mnt/mac/strong-hajin/codex-runtime`(또는 recordings·materials)이 없다 — §2-4 의 mkdir. 2026-10-02 첫 반영 때 미리 만들었다 |
| 배포 전에 시작한 AX 대화가 「session to resume is not available」로 실패 | 2026-10-02 반영(세션 공유 도입) 직후 한 번 있었다 — 그 세션은 옛 파드 로컬에 있었다. 새 대화로 쓴다. 공유 이후 세션은 재배포에도 남는다 |
| 원격 kubectl 의 `-o custom-columns=…[0]…` 가 `no matches found` | medi-me 로그인 셸이 zsh 라 대괄호를 glob 으로 먹는다. `-o jsonpath='…'` 를 따옴표로 감싸 쓴다(2026-10-03 WORK-009 반영 때) |
| 9/30 의 로컬 ad-hoc 판(`Strong Hajin.app`, origin 127.0.0.1)이 `/Applications` 에 남아 있을 수 있다 | 서명이 깨진 판이다. medi-ax 판과 섞지 않는다 |

## 7. 이번에 하지 않은 것

- GitHub Releases 발행 · `60-release` 기록 — DEC-005 D-09 의 자리는 그대로 비어 있다
- Windows 빌드·서명
- Argo automated sync
- 백업 주기·보관 위치(배포 설계 D-5)
