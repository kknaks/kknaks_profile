# WORK-011 운영 반영 명령 목록 — 외부 채널(INFRA)

> **실행하지 않은 문서다.** infra 워커가 차트 변경과 함께 남긴 명령 목록이다. 실행은 코디가 반영 승인 범위에서 한다.
> 순서는 WORK-011 「Phase 반영」 ★4(hostPath mkdir → manual SQL → Secret → 차트 → 이미지 → dmg)와 같다.
> 비밀값은 **파이프로만** 옮긴다(RUNBOOK-002 §4). 화면·파일·이 문서에 값을 적지 않는다. 확인은 키 이름과 길이로만.
> 클러스터 명령은 `ssh medi-me` 안에서 `/opt/homebrew/bin/kubectl` 로 돈다(비대화 ssh 는 PATH 가 짧다). 아래는 `kubectl` 로 줄여 쓴다.

## 차트가 기대하는 것 (이번 변경 — `charts/strong-hajin/`)

| 항목 | 값 | 어디 |
|---|---|---|
| 새 워커 | `worker-external` · `python -m ax_workspace.entrypoints.external_worker` · back 이미지 · **replicas 1 고정**(`worker.singletonKinds`) · `strategy: Recreate` | `values-prod.yaml` `worker.kinds` · `templates/worker.yaml` |
| hostPath | 노드 `/mnt/mac/strong-hajin/external-channels` → 컨테이너 `/app/var/external-channels` · type `Directory` · **back + worker-external 만** | `values*.yaml` `back.externalChannels*` |
| configmap | `AX_EXTERNAL_CHANNEL_STORAGE_DIR=/app/var/external-channels` · `AX_WEB_ORIGIN=https://ax.medisolveai.xyz`(기존) · `AX_API_ORIGIN=https://ax.medisolveai.xyz`(신규, 명시) | `templates/configmap.yaml` |
| 앱 Secret 키(이름만) | `strong-hajin-secret` 에 `GOOGLE_OAUTH_CLIENT_ID` · `GOOGLE_OAUTH_CLIENT_SECRET` · `GMAIL_PUBSUB_TOPIC` · `GMAIL_PUBSUB_SUBSCRIPTION` · `SLACK_CLIENT_ID` · `SLACK_CLIENT_SECRET` · `SLACK_APP_TOKEN` · `AX_EXTERNAL_TOKEN_ENCRYPTION_KEY` | back·모든 워커 `envFrom secretRef`(기존 길) |
| SA 키 파일 Secret | **별도** Secret `strong-hajin-pubsub-sa`, 키 `sa.json` → worker-external 에 `/var/run/secrets/strong-hajin/pubsub/sa.json`(0400, readOnly) · env `GOOGLE_PUBSUB_SA_KEY_FILE` 이 그 경로 | `values.yaml` `external.pubsubSaKey` |
| ingress | `proxy-body-size: 60m`(앱 50MB 보다 크게 — 앱이 413 을 먼저 낸다) · WS `/api/inbox/stream` 은 `/api` Prefix → back, 타임아웃 3600s(기존) | `values.yaml` `ingress.proxyBodySize` |

SA 키 Secret 볼륨은 `optional: true` 다 — 없으면 파일이 안 생기고 워커는 「history polling only」 경고를 남긴 채 슬랙·Gmail 폴링은 계속 돈다(`bootstrap/external_worker.py` `_make_puller`). Pub/Sub 실시간을 쓰려면 3-②를 반드시 한다.

## 0. 선행 확인 (로컬)

```bash
# 인프라 레포 차트 렌더 (PR 머지 전 · 후 둘 다)
helm lint charts/strong-hajin -f charts/strong-hajin/values-prod.yaml
helm template strong-hajin charts/strong-hajin -f charts/strong-hajin/values-prod.yaml -n strong-hajin-prod \
  | grep -E "name: worker-external|replicas|external-channels|AX_API_ORIGIN|AX_WEB_ORIGIN|proxy-body-size"

# 로컬 env 파일에 키가 있는지 — 이름만 본다(값 출력 금지)
cut -d= -f1 ~/.config/google/env ~/.config/slack/env | sed 's/^export //' | sort
```

## 1. 노드 hostPath mkdir — **차트보다 먼저**

type `Directory` 라 없으면 **back 과 worker-external 이 `ContainerCreating` 에 멈춘다**(RUNBOOK-002 §6 함정).

```bash
ssh medi-me 'limactl shell worker-1 -- sudo mkdir -p /mnt/mac/strong-hajin/external-channels'
ssh medi-me 'limactl shell worker-1 -- ls -ld /mnt/mac/strong-hajin/external-channels'
```

`/mnt/mac` 은 Mac Studio `~/mediness-data` 다 — 같은 이름의 폴더가 Mac 쪽에도 생긴다(보존 대상, 지우지 않는다).

## 2. manual SQL — **이미지보다 먼저**

파일: 코드 레포 `backend/migrations/manual/2026-10-06-external-channels.sql`(새 표 9 · 전부 `IF NOT EXISTS` · 새 표라 `.concurrent.sql` 없음 · 한 트랜잭션).

```bash
# Strong_hajin 워크트리(머지된 main)에서. 파일을 노드·파드에 남기지 않고 stdin 으로.
cat backend/migrations/manual/2026-10-06-external-channels.sql \
  | ssh medi-me '/opt/homebrew/bin/kubectl -n strong-hajin-prod exec -i postgres-0 -- psql -U strong_hajin -d strong_hajin -v ON_ERROR_STOP=1 -1 -f -'

# 확인 — 표 이름만
ssh medi-me "/opt/homebrew/bin/kubectl -n strong-hajin-prod exec postgres-0 -- psql -U strong_hajin -d strong_hajin -Atc \"select tablename from pg_tables where schemaname='public' and (tablename like 'external_%' or tablename='profile_images') order by 1\""
```

## 3. Secret patch — **차트보다 먼저**

### 3-① 앱 Secret `strong-hajin-secret` (기존 Secret 에 키 추가 · `patch --type merge` 라 기존 키 보존)

`~/.config/google/env` · `~/.config/slack/env` 에서 필요한 키만 골라 `{"stringData":{…}}` 로 조립해 stdin 으로 넘긴다.
`GOOGLE_PUBSUB_SA_KEY_FILE` 은 **로컬 경로라 넣지 않는다**(운영 경로는 차트가 env 로 준다 — 3-②).
`AX_EXTERNAL_TOKEN_ENCRYPTION_KEY` 는 **운영 전용으로 새로 만든다**(로컬 키를 재사용하지 않는다).

```bash
python3 - <<'PY' | ssh medi-me '/opt/homebrew/bin/kubectl -n strong-hajin-prod patch secret strong-hajin-secret --type merge --patch-file /dev/stdin'
import base64, json, os, shlex, sys
want = ["GOOGLE_OAUTH_CLIENT_ID", "GOOGLE_OAUTH_CLIENT_SECRET", "GMAIL_PUBSUB_TOPIC", "GMAIL_PUBSUB_SUBSCRIPTION",
        "SLACK_CLIENT_ID", "SLACK_CLIENT_SECRET", "SLACK_APP_TOKEN"]
vals = {}
for path in ("~/.config/google/env", "~/.config/slack/env"):
    for line in open(os.path.expanduser(path)):
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.removeprefix("export ").split("=", 1)
        if k.strip() in want:
            vals[k.strip()] = (shlex.split(v) or [""])[0]
missing = [k for k in want if not vals.get(k)]
if missing:
    sys.exit(f"missing keys: {missing}")          # 이름만 찍는다
# Fernet 키 = 32바이트 urlsafe base64. 한 번 넣으면 바꾸지 않는다(바꾸면 저장된 토큰을 못 연다 · OQ-801 회전 범위 밖)
vals["AX_EXTERNAL_TOKEN_ENCRYPTION_KEY"] = base64.urlsafe_b64encode(os.urandom(32)).decode()
print(json.dumps({"stringData": vals}))
PY
```

⚠ **재실행 주의**: 위 블록을 다시 돌리면 암호화 키가 **새 값으로 덮인다** → 이미 저장된 OAuth 토큰을 못 연다. 두 번째부터는 `AX_EXTERNAL_TOKEN_ENCRYPTION_KEY` 줄을 빼고 돌리거나, 먼저 키가 있는지 본다:

```bash
ssh medi-me "/opt/homebrew/bin/kubectl -n strong-hajin-prod get secret strong-hajin-secret -o jsonpath='{.data}'" \
  | python3 -c 'import json,sys,base64; d=json.load(sys.stdin); [print(k, len(base64.b64decode(v))) for k,v in sorted(d.items())]'   # 키 이름·길이만
```

### 3-② Pub/Sub SA 키 파일 Secret `strong-hajin-pubsub-sa` (새 Secret · 키 `sa.json`)

원천은 로컬 `~/.config/google/env` 의 `GOOGLE_PUBSUB_SA_KEY_FILE` 이 가리키는 파일이다.

```bash
SA_FILE="$(set -a; . ~/.config/google/env; set +a; printf %s "$GOOGLE_PUBSUB_SA_KEY_FILE")"
test -f "$SA_FILE" && python3 -c 'import json,sys; d=json.load(open(sys.argv[1])); print(d.get("type"), d.get("client_email","").split("@")[-1])' "$SA_FILE"   # service_account · 도메인만
cat "$SA_FILE" | ssh medi-me '/opt/homebrew/bin/kubectl -n strong-hajin-prod create secret generic strong-hajin-pubsub-sa --from-file=sa.json=/dev/stdin'
# 이미 있으면(교체):
# cat "$SA_FILE" | ssh medi-me '/opt/homebrew/bin/kubectl -n strong-hajin-prod create secret generic strong-hajin-pubsub-sa --from-file=sa.json=/dev/stdin --dry-run=client -o yaml | /opt/homebrew/bin/kubectl apply -f -'
```

### 3-③ 외부 서비스 쪽 (콘솔 · 코드 밖)

- Google OAuth client 의 승인된 redirect URI 에 `https://ax.medisolveai.xyz/api/integrations/mail/callback`
- Slack 앱 Redirect URL 에 `https://ax.medisolveai.xyz/api/integrations/slack/callback` · 사용자 토큰 11권한 · Socket Mode 켜짐
- (경로는 코드 `redirect_uri()` 기준 — 반영 전에 코드에서 한 번 더 확인)

## 4. 차트 PR 머지

인프라 레포 `kknaksss/strong-hajin-inbox-infra` 브랜치 → `main` (코디). 이 시점엔 이미지 태그가 아직 옛것이어도 된다 —
옛 이미지에 `external_worker` 엔트리포인트가 없으면 worker-external 이 CrashLoop 한다. **그래서 4 와 5 를 같은 PR(또는 같은 sync)로 묶는 것을 권한다.**

## 5. 이미지 태그 → Argo 수동 sync

```bash
# Strong_hajin main 머지 커밋에서 (RUNBOOK-002 §1-2)
docker buildx build --platform linux/arm64 -f deploy/k8s/back.Dockerfile  -t ghcr.io/kknaksss/strong-hajin-back:<sha>-arm64  --push .
docker buildx build --platform linux/arm64 -f deploy/k8s/front.Dockerfile -t ghcr.io/kknaksss/strong-hajin-front:<sha>-arm64 --push .
docker manifest inspect ghcr.io/kknaksss/strong-hajin-back:<sha>-arm64 >/dev/null && echo back ok
docker manifest inspect ghcr.io/kknaksss/strong-hajin-front:<sha>-arm64 >/dev/null && echo front ok
# values-prod.yaml image.tag: <sha>-arm64 → PR 머지 (4 와 함께 권장)

ssh medi-me '/opt/homebrew/bin/kubectl -n argocd patch application strong-hajin-prod --type merge -p "{\"operation\":{\"initiatedBy\":{\"username\":\"kknaksss\"},\"sync\":{\"revision\":\"main\"}}}"'
ssh medi-me '/opt/homebrew/bin/kubectl -n argocd get application strong-hajin-prod'          # Synced / Healthy
ssh medi-me '/opt/homebrew/bin/kubectl -n strong-hajin-prod get pods'                         # 9/9 Running (back·front·worker 5·postgres·redis)
```

확인:

```bash
ssh medi-me '/opt/homebrew/bin/kubectl -n strong-hajin-prod get deploy worker-external -o jsonpath="{.spec.replicas} {.status.readyReplicas} {.spec.strategy.type}"'   # 1 1 Recreate
ssh medi-me '/opt/homebrew/bin/kubectl -n strong-hajin-prod logs deploy/worker-external --tail=100' | grep -iE "error|traceback|pub/sub|socket"
ssh medi-me '/opt/homebrew/bin/kubectl -n strong-hajin-prod exec deploy/back -- sh -c "printenv AX_WEB_ORIGIN AX_API_ORIGIN AX_EXTERNAL_CHANNEL_STORAGE_DIR; test -w \$AX_EXTERNAL_CHANNEL_STORAGE_DIR && echo writable"'
ssh medi-me '/opt/homebrew/bin/kubectl -n strong-hajin-prod exec deploy/worker-external -- sh -c "test -s \$GOOGLE_PUBSUB_SA_KEY_FILE && echo sa-key-present"'
curl -s https://ax.medisolveai.xyz/health
# 50MB 업로드가 ingress 를 통과하는지: 50MB 파일로 카톡 첨부/슬랙 답장 1회 — nginx 413(HTML) 이 아니라 앱 응답(JSON)이어야 한다
# 메시지함 WS: 브라우저에서 /api/inbox/stream 첫 프레임 {"type":"ready"}
```

## 6. 데스크톱 (medi-ax) dmg

RUNBOOK-002 §3 그대로 — 재빌드 · 서명 · 공증 · staple · 사용자 전달. (인프라 몫 아님)

## 롤백 — 역순

1. 데스크톱: 직전 dmg 재설치 · 카톡 수집기는 기기 토큰 철회로 개별 중단.
2. 이미지: `values-prod.yaml` `image.tag` 를 직전 값(`202078b-arm64`)으로 되돌려 머지 → 수동 sync.
   옛 이미지엔 `external_worker` 가 없으므로 **같은 PR 에서 `worker.kinds` 의 `external` 도 뺀다**(아니면 CrashLoop).
   수집만 멈추려면 `external` 만 빼면 된다(저장분 보존).
3. 차트: 필요하면 이 차트 PR 을 revert 머지 → sync. hostPath 마운트·`AX_*` env 가 빠질 뿐 데이터는 노드에 남는다.
4. Secret: **지우지 않는다**(남아도 무해 · 암호화 키를 지우면 저장 토큰을 영영 못 연다).
5. SQL: **되돌리지 않는다** — additive 라 남긴다. 표를 걷는 것은 사람의 별도 결정(`DROP TABLE` FK 역순).
6. hostPath `/mnt/mac/strong-hajin/external-channels`: **지우지 않는다**(회사 데이터 · 보존·파기 없음).
- 외부 잔여: Gmail `users.watch` 가 최대 7일 Pub/Sub 에 쌓이고 슬랙 Socket Mode 가 끊긴 채 남는다(무해 · 재반영 때 메우기가 흡수).

## 미결·주의 (워커 메모)

- **ingress 60m 은 파일 하나(50MB) 기준이다.** 슬랙 답장은 파일 최대 10개 × 50MB 를 한 multipart 로 받는다(`inbox.py` `MAX_REPLY_FILES=10`) — 합계 60MB 를 넘는 답장은 nginx 413 을 받는다. 여러 파일 큰 답장을 받아야 하면 `ingress.proxyBodySize` 를 올리거나 앱에서 요청 합계 한도를 둔다(제품 판단).
- worker-external 도 기존 워커 틀을 따라 recordings·materials·codex hostPath/PVC 를 함께 마운트한다(답장 전송이 `WorkflowApplication` 조립을 쓴다). 모두 이미 노드에 있는 경로라 추가 mkdir 은 external-channels 하나뿐.
- 코드상 연동 워커는 advisory lock 으로 리더를 잡는다 — replicas 1 + Recreate 와 이중 안전장치.
- 렌더 검증만 했다. 클러스터 적용·실측(1/1 · 50MB 통과 · WS)은 반영 때 코디가 위 확인 명령으로 잰다.
