# WP8 infra 리포트 — interpret-pwa(통키) 배포 준비

- 워커: @interpret-pwa-infra · task_e8ac3c1f774e · dispatch ctx_7911fa602abe · 2026-10-26
- 워크트리: `/Users/kknaks/orca/workspaces/k8s_infra_mac/interpret-pwa-poc` (base `origin/main` c7e2ed5) — **커밋 · push 없음**
- sync · apply · 시크릿 생성 안 함. 클러스터 접근 없음(kubeconfig 없음 · current-context 미설정)

## 1. 변경 파일

| 파일 | 상태 |
|---|---|
| `charts/interpret-pwa/Chart.yaml` · `values.yaml` · `values-prod.yaml` | 새로 |
| `charts/interpret-pwa/templates/_helpers.tpl` · `back.yaml` · `front.yaml` · `configmap.yaml` · `ingress.yaml` · `NOTES.txt` | 새로 |
| `argocd/applications/interpret-pwa-prod.yaml` | 새로 |
| `argocd/projects/interpret-pwa.yaml` | 새로 |
| `provisioning/secrets/interpret-pwa-prod.env.example` | 새로(이름만) |
| `docs/interpret-pwa-deploy.md` | 새로 |
| `charts/cloudflared/values.yaml` | **한 줄 추가**(`tongky.medisolveai.xyz`, `ccc` 줄 바로 아래) |

다른 앱 차트 · 앱 무수정(`git diff --stat` = cloudflared 1줄뿐).

## 2. 구현 요약

- **차트** — `charts/cc-prototype` 를 본떴다. 뺀 것: PVC · APNs 마운트 · nodeSelector · Recreate 전략 · fsGroup(볼륨이 없어서).
  - back: `ghcr.io/kknaksss/interpret-pwa-back:<tag>` · 8800 · replica 1 · uid 10001(runAsNonRoot · 숫자 uid) · SA 토큰 마운트 안 함 · `envFrom` = ConfigMap `interpret-pwa-config` → Secret `interpret-pwa-secret`(뒤가 이긴다) · readiness · liveness `GET /api/health`(back `glossary.py` 의 `prefix="/api"` + `/health` 확인)
  - front: `ghcr.io/kknaksss/interpret-pwa-front:<tag>` · 3800 · replica 1 · uid 1000 · `PORT=3800` · `HOSTNAME=0.0.0.0`(k8s 가 pod 이름으로 덮는 것 방지 — cc 선례) · 프로브 `/login`(`'use client'` 정적 페이지 — `/` 는 리다이렉트할 수 있어 안 씀)
  - `imagePullSecrets: ghcr-pull`(values-prod) · arm64(클러스터 전 노드 arm64 — cc 처럼 별도 nodeSelector 없음)
  - ingress: 한 호스트 `tongky.medisolveai.xyz` · `/api` → back:8800 · `/` → front:3800 · `proxy-read-timeout` · `proxy-send-timeout` 3600 · `proxy-buffering off` · `proxy-body-size 10m` · className nginx. WS Upgrade 는 ingress-nginx 기본 전달(cc-prototype 의 같은 `/api/interpret` 선례 — annotation 불필요)
  - 이미지 태그: `values-prod.yaml` 의 `image.tag: ""` → `required` 로 **렌더 거부**. `back.imageTag` / `front.imageTag` 가 있으면 우선
- **ArgoCD** — Application `interpret-pwa-prod`(project `interpret-pwa` · `targetRevision: main` · values-prod · **수동 sync** · `CreateNamespace=true`) + AppProject `interpret-pwa`(소스 = 이 레포만 · 목적지 = `interpret-pwa-prod` 만 · 클러스터 범위는 Namespace 만). AppProject 는 root app 이 안 보니 손으로 1회 apply(문서에 적음)
- **cloudflared** — `hosts` 에 `tongky.medisolveai.xyz` 한 줄. 렌더 결과 `hostname: tongky.medisolveai.xyz` 확인. DNS CNAME(`cloudflared tunnel route dns …`)은 수동 1회 — 문서에
- **시크릿 예시** — `SONIOX_API_KEY` · `INTERPRET_LOGIN_ID` · `INTERPRET_LOGIN_PASSWORD` · `INTERPRET_SESSION_SECRET` + 선택 `INTERPRET_SESSION_HOURS` · `GLOSSARY_MATRIX_URL` · `GLOSSARY_CONTEXT_MAX_CHARS`(앱 `.env.example` 이름 그대로 · 값 전부 빈칸). 빠진 것과 이유를 머리 주석에: `INTERPRET_FRONT_ORIGIN`(ConfigMap 소유 — 넣으면 덮어씀) · `NEXT_PUBLIC_API_BASE_URL`(front 빌드 인자)
- **문서** — 시크릿 2종(`interpret-pwa-secret` · `ghcr-pull`) 만드는 명령 · 순서(namespace → 1 → 2 → sync) · DNS · 첫 sync(AppProject apply → tag 채워 머지 → cloudflared sync → app sync) · 재배포 · 확인 curl · SPEC §9.5 휴대폰 체크리스트

> 브리프는 「시크릿 3종」이라 했는데 이 앱은 APNs 가 없어 **2종**(`interpret-pwa-secret` · `ghcr-pull`)이다. cc-prototype 의 3번째(`cc-prototype-apns`)에 해당하는 것이 없다. namespace 생성을 셋째 단계로 함께 적었다.

### `INTERPRET_FRONT_ORIGIN` 을 ConfigMap(git)에 둔 근거

1. 값이 공개 주소 그 자체(`https://tongky.medisolveai.xyz`) — 브라우저 주소창 · DNS · cloudflared values 에 이미 공개되어 있다. 비밀이 아니다.
2. SPEC-001 §2.4 표에서 비밀값으로 분류된 것은 `SONIOX_API_KEY` · 로그인 아이디 · 비밀번호 · 세션 비밀값(§9.5)뿐 — 이 이름은 없다.
3. 호스트와 **정확히 같은 문자열**이어야 CORS · WS Origin 검사(§5.2, 다르면 1008)가 통과한다 → 차트가 `host` 값에서 만들어야 어긋날 일이 없다(cc-prototype `PROC_FRONT_ORIGIN` 선례와 같음).

## 3. 검증 결과

| 검증 | 결과 |
|---|---|
| `helm lint charts/interpret-pwa -f values-prod.yaml --set image.tag=0000000fake` | **1 chart linted, 0 failed** (INFO: icon 권장 — cc 차트와 같음) |
| `helm template … -f values-prod.yaml`(태그 없음) | **렌더 거부** — `image.tag is not set — inject the arm64 commit-sha tag …` (의도대로) |
| `helm template interpret-pwa charts/interpret-pwa -n interpret-pwa-prod -f values-prod.yaml --set image.tag=0000000fake` | rc=0 · **리소스 6개**(ConfigMap 1 · Service 2 · Deployment 2 · Ingress 1) · 이미지 · 호스트 · timeout 3600 · buffering off · ORIGIN 확인 |
| `kubectl apply --dry-run=client` | **실행 불가** — 클러스터 없음(kubectl client dry-run 도 API discovery 가 필요 · `localhost:8080 connection refused`). **pending** |
| 대신: `kubeconform -strict`(k8s 기본 스키마 + datree CRD 카탈로그 — ArgoCD Application · AppProject) | **10 resources / 4 files — Valid 10, Invalid 0, Errors 0, Skipped 0** (차트 렌더 6 + Application 1 + AppProject 1 + cloudflared 렌더 2) |
| 시크릿 값 | **0** — env.example 은 `KEY=` 만, 차트 · values · 문서에 키 값 없음 |
| 다른 앱 차트 | 무수정 |

> 참고: helm v4.2.3 의 `helm lint` 는 `required` 실패를 무시해 태그 없이도 통과한다 — 렌더 거부는 `helm template` 쪽에서 확인했다. 기존에 깨져 있던 무관한 실패는 보지 못했다.

## 4. 계약 준수

- D-26: 도메인 `tongky.medisolveai.xyz` · ns `interpret-pwa-prod` · 이미지 `ghcr.io/kknaksss/interpret-pwa-{back,front}:<sha>` · 실제 sync 는 E2E · 머지 뒤(D-12) — 준수
- SPEC §2.2 포트 8800 · 3800(고정, env 아님) · §2.4 env 이름 · §5.2 WS `/api/interpret` 같은 호스트 · §8 HTTPS(Cloudflare 엣지 TLS) — 준수
- 브리프 allowed_paths 만 수정 · 커밋 · push · sync · apply 없음

## 5. 미결 · 주의점 (코디 · 사용자 몫)

1. **이미지 없음** — `interpret-pwa-{back,front}` main 빌드(Actions · arm64) 뒤 `values-prod.yaml` `image.tag`(또는 `back/front.imageTag`) 채워 머지해야 Argo 가 렌더한다. **front 빌드는 `NEXT_PUBLIC_API_BASE_URL=https://tongky.medisolveai.xyz` 필수**(Dockerfile 이 비면 빌드 실패 · 다르면 WS 가 엉뚱한 곳으로 감).
2. 클러스터 작업(사용자): `kubectl apply -f argocd/projects/interpret-pwa.yaml` · 시크릿 2종 · `cloudflared tunnel route dns … tongky.medisolveai.xyz` · `argocd app sync cloudflared` · `argocd app sync interpret-pwa-prod`.
3. `ghcr-pull` 는 네임스페이스마다 따로 — cc-prototype 의 PAT 로 `interpret-pwa-*` 패키지를 읽을 수 있는지 확인 필요(GHCR private 패키지 권한은 패키지별).
4. `kubectl apply --dry-run=client` 는 클러스터가 있는 곳에서 한 번 돌려 주면 닫힌다(kubeconform 으로 스키마는 통과).
5. 유휴 2분 WS 유지는 ingress 3600 으로 nginx 쪽은 충분. Cloudflare 엣지 유휴 컷(~100s)은 WS 에서 프레임이 오가면 문제없으나, 완전 무음 유휴가 길면 앱 쪽 ping 여부에 달렸다 — §9.5 「유휴 2분」 실측으로 확인.
6. `/login` 프로브는 front 가 정적 페이지로 빌드된다는 가정(`'use client'`) — 첫 배포 때 200 확인.
