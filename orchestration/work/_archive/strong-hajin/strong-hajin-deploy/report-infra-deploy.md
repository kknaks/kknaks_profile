# report — infra: Strong Hajin 운영 첫 배포 (task_6c94c10eb391 / ctx_4753ad0883ad)

상태: 단계 2 완료 · 태그 머지 infra #6 `7ba1050` · F1 AppProject `strong-hajin` apply 완료 · F2 `cloudflared tunnel route dns b9610413-… ax.medisolveai.xyz` 완료(dig → 104.21.75.230/172.67.182.232, https 404 = 앱 없음) · 단계 3·5·6 완료(2026-10-01) · 2차 §A(STT·회의실)·§B(codex 전용 로그인, AX 턴 성공) 완료 — **남음: 로그인 1명 실측(비번 대기)**

## 0. 기준

- infra: `kknaksss/strong-hajin-deploy-infra` = `origin/main` `f04d4cb` 에서 재생성(checkout -B)
- code: `origin/main` `cdb0f3f` detached, 미커밋 변경 0
- 보충 `infra-01-handoff-notes.md` 반영

## 1. 이미지 (단계 1) — 완료

```
cd <code worktree>
docker buildx build --platform linux/arm64 -f deploy/k8s/back.Dockerfile  -t ghcr.io/kknaksss/strong-hajin-back:cdb0f3f-arm64  --push .   # exit 0
docker buildx build --platform linux/arm64 -f deploy/k8s/front.Dockerfile -t ghcr.io/kknaksss/strong-hajin-front:cdb0f3f-arm64 --push .   # exit 0
docker manifest inspect ghcr.io/kknaksss/strong-hajin-{back,front}:cdb0f3f-arm64
```

| 이미지 | index digest | 플랫폼 |
|---|---|---|
| strong-hajin-back:cdb0f3f-arm64 | `sha256:a81e266c6d1a…` | linux/arm64 (`7d5f5ecbd966…`) + attestation(unknown/unknown) |
| strong-hajin-front:cdb0f3f-arm64 | `sha256:227e8faf088d…` | linux/arm64 (`54affd05d33c…`) + attestation |

주의: ghcr 패키지는 신규 → 기본 private. `ghcr-pull` 시크릿 필수(차트 values-prod 가 이미 참조).

## 2. 태그 (단계 2) — 완료, 커밋은 코디

변경: `charts/strong-hajin/values-prod.yaml` 1줄 `tag: ""` → `tag: cdb0f3f-arm64` (미커밋).

```
helm lint charts/strong-hajin -f charts/strong-hajin/values-prod.yaml         # 1 linted, 0 failed (icon INFO만)
helm template strong-hajin charts/strong-hajin -f …/values-prod.yaml -n strong-hajin-prod   # exit 0
helm template d charts/datastores -f charts/datastores/values-strong-hajin.yaml -n strong-hajin-prod  # exit 0
```

렌더 결과: ConfigMap 1 · Deployment 6(back·front·worker-{conversation,material,meeting,report}) · Service 2 · Ingress 1 · PVC 1(codex-home) / datastores: StatefulSet 2 · Service 2(PVC 10Gi·2Gi)

- 이미지: back 5곳 `ghcr.io/kknaksss/strong-hajin-back:cdb0f3f-arm64`, front 1곳 — 명시 태그 ✓
- Ingress: host `ax.medisolveai.xyz` 1개, path `/api/meetings`·`/api`·`/health` → back:28080, `/` → front:80 (같은 origin FE/API/WS) ✓
- secretRef: `strong-hajin-secret`(envFrom, optional) 5 · `postgres-secret/POSTGRES_PASSWORD` 5 ✓
- 격리: 네임스페이스 `strong-hajin-prod`(Argo destination), AppProject `strong-hajin` ✓ — mediness ns 와 리소스 이름 충돌 없음

## 3. 단계 3~5 착수 전 발견 (읽기 전용 조사)

| # | 사실 | 영향 |
|---|---|---|
| F1 | **AppProject `strong-hajin` 이 클러스터에 없다.** 두 앱 condition: `Application referencing project strong-hajin which does not exist` (InvalidSpecError, Sync/Health Unknown). root 앱은 `argocd/applications/` 만 보고 `argocd/projects/` 는 수동 apply 대상 | **sync 불가.** `kubectl apply -f argocd/projects/strong-hajin.yaml`(argocd ns) 가 필요 — 내 allowed 범위(strong-hajin-prod ns) 밖. 또 이 프로젝트는 `clusterResourceWhitelist: */*` 로 넓다(차트엔 클러스터 리소스 없음 — 좁혀도 됨) |
| F2 | `ax.medisolveai.xyz` NXDOMAIN. mediness 호스트는 Cloudflare proxied(A 172.67.x/104.21.x) — values 주석상 `cloudflared tunnel route dns` 로 CNAME 생성. medi-me `~/.cloudflared/cert.pem` 존재 → `cloudflared tunnel route dns b9610413-… ax.medisolveai.xyz` 로 대시보드 없이 가능 | 공유 Cloudflare 존 쓰기 → 승인 필요 |
| F3 | cloudflared(auto-sync) ConfigMap 에 `ax.medisolveai.xyz` 이미 반영됨 | 터널 ingress 쪽 추가 작업 없음 |
| F4 | worker-1: `/opt/codex`(codex-cli **0.146.0**)·`/opt/claude`(Claude Code 2.1.220) 존재. `/mnt/mac` virtiofs rw, `/mnt/mac/strong-hajin` **없음** → 단계 3 에서 `recordings`·`materials` 생성 필요 | 계획대로 |
| F5 | 시드 dump `~/strong-hajin-deploy-data/strong-hajin-seed.dump`(600, 227KB) 존재 — 단계 5 에서 사용 예정 | |
| F6 | codex-home PVC 는 비어서 뜬다 — AX 턴 실측엔 auth.json(`kubectl cp`) 또는 claude 토큰(`strong-hajin-secret`)이 필요. 어떤 인증을 쓸지 미정 | 단계 6 AX 실측 전 결정 필요 |

## 4. 미결

- 코디: values-prod 태그 커밋·머지
- F1 AppProject apply 주체/승인 · F2 DNS route 승인 · F6 AX 인증 방식

## 5. 단계 3 — 클러스터 준비 (2026-10-01) — 완료

모든 명령은 `ssh medi-me`, kubectl=`/opt/homebrew/bin/kubectl`. 비밀값은 파이프로만 전달, 출력 없음.

```
kubectl create ns strong-hajin-prod --dry-run=client -o yaml | kubectl apply -f -         # created
gh auth token | python3 (dockerconfigjson 조립, stdout→pipe) | ssh medi-me 'kubectl -n strong-hajin-prod create secret generic ghcr-pull --type=kubernetes.io/dockerconfigjson --from-file=.dockerconfigjson=/dev/stdin'   # created
printf %s "$(openssl rand -hex 24)" | kubectl -n strong-hajin-prod create secret generic postgres-secret --from-file=POSTGRES_PASSWORD=/dev/stdin   # created, 길이 48 확인만
kubectl -n strong-hajin-prod create secret generic strong-hajin-secret                    # created, 키 0개
limactl shell worker-1 -- sudo mkdir -p /mnt/mac/strong-hajin/{recordings,materials}      # = Mac ~/mediness-data/strong-hajin/* 확인
```

- `strong-hajin-secret` 은 **빈 시크릿**: 백엔드에 필수 비밀 키가 없다(세션은 DB). 선택 키 `SONIOX_API_KEY`(실시간 STT)·`TDL_*`(회의실 예약) 미설정 → 해당 기능은 비활성. 값 출처는 사용자 결정
- AI 노드 마운트: `/opt/codex`(0.146.0)·`/opt/claude`(2.1.220) 존재

## 6. 단계 5 — datastores sync · 시드 복원

argocd CLI 가 medi-me 에 없음 → Application `operation` 필드로 1회 수동 sync(automated 는 켜지 않음):
```
kubectl -n argocd patch application strong-hajin-datastores --type merge -p '{"operation":{"initiatedBy":{"username":"kknaksss"},"sync":{"revision":"main"}}}'
```
→ Synced / Succeeded. postgres-0·redis-0 1/1 Running (lima-worker-1), PVC 10Gi·2Gi Bound.

시드: writer dump `~/strong-hajin-deploy-data/strong-hajin-seed.dump` **사용**(재덤프 안 함). TOC: 90 TABLE DATA, `auth_sessions` 는 스키마만(데이터 없음), extension 불필요, owner `ax`.
```
(복원 전) public 테이블 0
cat seed.dump | ssh medi-me 'kubectl -n strong-hajin-prod exec -i postgres-0 -- pg_restore -U strong_hajin -d strong_hajin --no-owner --no-acl'   # exit 0, 에러 0
```
dump 를 stdin 스트림으로만 넘김 → 노드·파드에 파일 없음(삭제할 것 없음).
복원 후: public 테이블 91 · members 4 · member_credentials 4 · memberships 4 · auth_sessions 0.

### strong-hajin-prod sync
```
kubectl -n argocd patch application strong-hajin-prod --type merge -p '{"operation":{"initiatedBy":{"username":"kknaksss"},"sync":{"revision":"main"}}}'
```
→ Synced / Succeeded (rev main `7ba1050`). back 이미지 pull ~40초. syncPolicy automated 는 **켜지 않음**.

## 7. 단계 6 — 실측 (2026-10-01 08:26 KST)

| 항목 | 결과 |
|---|---|
| 파드 | back·front·worker-{conversation,material,meeting,report}·postgres-0·redis-0 **8/8 1/1 Running, restarts 0** (워커 4 Ready) |
| `GET https://ax.medisolveai.xyz/` | **200** text/html, `<title>MEDISOLVE</title>` |
| `GET /health` | 200 |
| `GET /api/auth/providers` | **200 `{"local":true,"oidc":false}`** — `demo_accounts` 없음 ✓ |
| WS `wss://ax…/api/meetings/<uuid>/stream` (비로그인) | **101 Switching Protocols** → 서버가 close **4401 unauthorized** (설계대로 — Cloudflare→ingress→back WS 경로 통과) |
| 로그 | back·워커4·front tail 200줄 error/traceback 0 |
| 로그인 1명 | **미실측 — 비밀번호 사용자 답 대기** |
| AX 턴 | **실패 — 멈춤** (아래) |

### AX (F6 = (a) 호스트 auth.json)
```
cat ~/.codex/auth.json | kubectl -n strong-hajin-prod exec -i deploy/back -- sh -c 'umask 077; cat > /root/.codex/auth.json.tmp && mv … auth.json'   # 4574B, 0600, 내용 미출력
kubectl -n strong-hajin-prod exec -i deploy/worker-conversation -- sh -s < smoke.sh   # codex exec "Reply with exactly the word: PONG"
```
결과: codex-cli 0.146.0 기동 OK(model gpt-5.6-sol) → `401 Unauthorized` + **`Failed to refresh token: … your refresh token has expired. Please log out and sign in again.`** exit 1.
- 원인은 **버전이 아니라 인증**: 호스트 auth.json(7/2)의 refresh token 만료(이후 mediness PVC 쪽에서 회전된 것으로 추정). refresh 가 실패했으므로 mediness 토큰에 영향 없음
- mediness `worker-codex` PVC 는 읽지도 않음(지시대로)
- PVC 의 무효 auth.json 은 그대로 둠(무해). 전용 `codex login` 후 같은 파이프 명령으로 덮어쓰면 됨
- 0.146 호환성은 인증이 풀린 뒤에야 판정 가능

## 8. 남은 것 / 주의

1. **AX 인증** — Strong Hajin 전용 codex login(사용자 결정). 이후 `cat auth.json | kubectl exec -i deploy/back -- …` + worker 로그로 AX 턴 1회 재실측, 0.146 호환 판정
2. **로그인 실측** — 4명 중 1명 비밀번호(사용자 → 코디)
3. `strong-hajin-secret` 비어 있음 — `SONIOX_API_KEY`(실시간 STT)·`TDL_*` 없으면 해당 기능 비활성
4. 워커 Deployment 는 readinessProbe 가 없어 "Ready" = 프로세스 생존 의미
5. medi-me SSH(cloudflared access)가 자주 끊김 — 명령은 짧게/멱등으로. route dns 는 1회 실행 후 해석 확인(재실행 로그는 끊김으로 못 읽음; 레코드는 1개 해석됨)
6. rollback: app = Argo 에서 이전 태그로 수동 sync. 데이터 = postgres PVC(10Gi, local-path worker-1) 보존 — 삭제로 되돌리지 말 것. 시드 원본 dump 는 로컬 `~/strong-hajin-deploy-data/` 에 그대로

변경 파일: infra 워크트리 변경 없음(태그는 #6 으로 머지됨). 클러스터: AppProject `strong-hajin`(argocd, 승인) · ns `strong-hajin-prod` 와 그 안의 시크릿 3·Argo 관리 리소스 · worker-1 `/mnt/mac/strong-hajin/{recordings,materials}` · DNS `ax.medisolveai.xyz`(승인).

## §A. STT·회의실 키 주입 (2차, 2026-10-01) — 완료

코드가 읽는 키(`git grep 'SONIOX\|TDL_' -- backend/src`): `SONIOX_API_KEY` · `TDL_EMAIL` · `TDL_PASSWORD` 는 기본값 없음 → 주입. `TDL_BASE_URL`·`TDL_COMPANY_ID`·`TDL_NOTIFY`·`TDL_HTTP_TIMEOUT_SECONDS` 는 코드 기본값(`settings.py:172-177`) 사용 — 주입 안 함.

원천: 사용자 Mac `~/.config/soniox/env`(키 1) · `~/.config/theconnect/env`(키 2). 형식 점검(키 이름·따옴표 없음·후행 공백 없음)만 하고 값은 출력하지 않음.
```
cat ~/.config/soniox/env ~/.config/theconnect/env | python3 (→ {"stringData":{3키}} JSON, 키 집합 assert) \
  | ssh medi-me 'kubectl -n strong-hajin-prod patch secret strong-hajin-secret --type merge --patch-file /dev/stdin'
```
- `apply` 대신 `patch --type merge`(stringData) — 기존 키 보존(주입 전 키 0개). 주입 후 키 3개, 길이만 원천과 일치 확인
- `kubectl -n strong-hajin-prod rollout restart deploy/back deploy/worker-{conversation,material,meeting,report}` → 전부 1/1 Running, Argo `Synced Healthy`
  (rollout restart 는 pod template 에 restartedAt 주석을 남김 — 다음 수동 sync 때 원복되며 그게 정상)

실측(back 파드 안에서 파드 env 로 — 앱 경로 `/api/meetings/rooms` 는 로그인 필요, 비번 대기 중이라 대체):
| 항목 | 결과 |
|---|---|
| Soniox 키: `GET https://api.soniox.com/v1/files?limit=1` (읽기 전용) | **200** |
| 회의실: 앱 `Settings.from_environment()` → `room_booking_configured` | **True** |
| 회의실: 앱 `TheConnectGateway(...).rooms()` (조회만) | **7개** |

메모: 앱에는 "STT 토큰 발급 API" 가 없다 — 실시간 STT 는 back 이 서버측에서 Soniox WS 를 연다(`platform/soniox.py`, 키는 브라우저로 안 나감). 브라우저 경유 실측은 로그인 후 회의 스트림(WS upstream)으로 가능.

## §B. AI(codex) — 전용 로그인 (2026-10-01) — 완료

원천: 사용자 전용 로그인 `~/strong-hajin-deploy-data/codex-home/auth.json`(3859B, 0600, 키 이름만 확인: auth_mode·last_refresh·tokens·OPENAI_API_KEY). mediness·사용자 `~/.codex` 와 무관.
```
cat ~/strong-hajin-deploy-data/codex-home/auth.json | ssh medi-me 'kubectl -n strong-hajin-prod exec -i deploy/back -- sh -c "umask 077; cat > /root/.codex/auth.json.tmp && mv … /root/.codex/auth.json"'   # 3859B 일치, 앞서 넣은 만료본(4574B) 덮음
kubectl -n strong-hajin-prod rollout restart deploy/back deploy/worker-{conversation,material,meeting,report}   # 5개 rolled out, 1/1
```
AX 턴 실측 — worker-conversation 파드에서 **앱 자체 경로** `create_codex_cli_provider(Settings.from_environment()).generate(...)`(격리 CODEX_HOME + auth 심링크 + SCAX MCP 바인딩, 앱과 동일):

| 항목 | 결과 |
|---|---|
| ai_provider | codex |
| 결과 | **성공** body `{"answer": "PONG"}` (structured output schema 통과) |
| 모델 요청 | gpt-5.6-terra (앱 기본 프로파일) |
| latency | 5148 ms |
| codex CLI | 노드 `/opt/codex` **0.146.0** — 동작함(개발 0.158 과 버전차 있어도 generate 경로 OK) |
| 로그 | back·워커4 tail 300 error/traceback 0 |

관찰: provenance 의 observed_model·observed_tier·run_ref 가 None 으로 파싱됨 — 0.146 의 `--json` 이벤트 형식이 0.158 과 달라 앱 파서가 못 읽는 것으로 추정. 생성 자체엔 영향 없음, 기록 필드만 빈다(노드 codex 업그레이드는 공유 자원 → 사용자 결정).
한계: 로그인 비번이 없어 **HTTP 로 연 대화 턴 → 워커 큐 소비** 경로는 못 탔다. 위는 같은 어댑터를 워커 파드에서 직접 부른 것.

주의: 로컬 `~/strong-hajin-deploy-data/codex-home/auth.json` 과 PVC 가 이제 **같은 refresh token** 을 가진다 — 로컬에서 그 CODEX_HOME 으로 codex 를 쓰면 회전으로 운영 쪽이 끊길 수 있다. 로컬 사본은 쓰지 말고 백업으로만 두거나 지울 것(사용자 결정).

## 최종 상태 (2026-10-01)
- 파드 8/8 1/1 restarts 0 · Argo strong-hajin-prod·datastores `Synced Healthy`(automated 끔) · `https://ax.medisolveai.xyz/` 200
- 완료: 이미지·태그·클러스터 준비·DNS·시드 복원·sync·providers·WS·STT 키·회의실·AX
- **남은 것 1개: 로그인 1명 실측**(비밀번호 사용자 대기) — 받으면 `POST /api/auth/login` 계열 1회 + 로그인 세션으로 `/api/meetings/rooms`·대화 턴까지 한 번에 확인 가능
