# WORK-006 Phase 6a — Strong Hajin 운영 배포 설계

> **이 문서는 설계다. 실행·푸시·배포는 Phase 6b 다.**
> **운영 도메인·비밀값·외부 레포 권한을 발명하지 않는다** — 정해지지 않은 것은 빈 자리로 두고
> 누가 정하는지 적는다.
>
> **표기 규약 — 이 문서의 모든 항목은 셋 중 하나다. 섞어 쓰지 않는다.**
> - **[사실]** 파일을 읽어 확인한 것. 좌표를 붙인다
> - **[기본값]** 이 설계가 제안하는 값. 근거를 붙인다. **6b 가 그대로 쓰면 된다**
> - **[사용자 결정]** 사람이 정해야 하는 것. **6b 는 이것 없이 그 항목을 실행할 수 없다**

- **작성 시각**: 2026-09-22 21:45 KST
- **보정**: 2026-09-22 **21:52 KST** — 검수 **F-1 · W-1 ~ W-5 반영**(수치·좌표·probe·datastores·문구)
- **인프라 레포(읽기 전용)**: `/Users/kknaks/git/harness_works/k8s_infra_mac` · **HEAD `46fdf88`** · **clean**
- **제품 코드**: `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-projects` · HEAD `a1f6791`
- **이번 회차 변경**: 인프라 레포 **0줄**(§9 확인) · 제품 코드 **0줄** · 문서 **이 파일 하나**

---

## 1. 요약 — 6b 가 알아야 할 세 줄

1. **Mediness 의 「3 호스트(front·api·mcp)」 구조를 Strong Hajin 이 그대로 베끼면 안 된다.**
   SPEC-006 이 **같은 origin 하나**를 요구하기 때문이다(방향 A). 호스트 하나 + 경로 분기로 간다(§4)
2. **가장 큰 차단은 인프라가 아니라 제품 코드다.** 지금 `AX_PROFILE=production` 으로 띄우면
   **API 라우트가 단 하나도 등록되지 않는다**(§3-1). 이것을 푸는 것이 6b 의 첫 작업이다
3. **운영 도메인은 이 문서가 정하지 않는다**(OQ-T02). 값이 빌 자리를 `<STRONG_HAJIN_HOST>` 로
   표시했고, 그 자리가 채워지기 전에는 cloudflared·ingress·셸 설정 **세 곳이 함께 막힌다**(§8)

---

## 2. 기준 인프라 — 읽어서 확인한 사실

| # | 사실 | 좌표 |
|---|---|---|
| F-1 | Mac Studio(M2 Ultra, **arm64**) 1대에 Lima + kubeadm **3노드**(master 1 + worker 2) | `README.md` 구성 요약 |
| F-2 | 네트워크: Calico · MetalLB · **ingress-nginx** | `README.md` · `infra/ingress-nginx/` |
| F-3 | 배포: **Helm(values-dev/prod) + ArgoCD GitOps** | `README.md` |
| F-4 | 외부 노출: **Cloudflare Tunnel (outbound only)**. **TLS 는 Cloudflare 에지에서 종단**되고 클러스터 안은 평문 HTTP — **cert-manager 가 없다** | `charts/mediness/templates/ingress.yaml:2-3` |
| F-5 | 공개 호스트는 **단일 레벨 서브도메인만** 쓴다 — Universal SSL 이 `*.<zone>` 만 덮고 `a.b.<zone>` 은 안 덮는다 | `charts/mediness/templates/_helpers.tpl:1-4` |
| F-6 | Mediness 는 **호스트 셋**으로 갈린다: front `<prefix>.<domain>` · api `<prefix>-api.<domain>` · mcp `<prefix>-mcp.<domain>` | `_helpers.tpl:4-6` |
| F-7 | api ingress 는 **WS 용 긴 타임아웃**을 단다 — `proxy-read-timeout: 3600` · `proxy-send-timeout: 3600` · `proxy-body-size: 50m` | `ingress.yaml` api 블록 |
| F-8 | ArgoCD `AppProject: mediness` 는 **sourceRepos 를 이 레포 하나로**, destinations 를 `mediness-dev`·`mediness-prod` **두 네임스페이스로 제한** | `argocd/projects/mediness-appproject.yaml` |
| F-9 | `Application: mediness-prod` — `targetRevision: main` · `path: charts/mediness` · `values-prod.yaml` · `automated{prune,selfHeal}` · `CreateNamespace=true` | `argocd/applications/mediness-prod.yaml` |
| F-10 | cloudflared 는 **hosts 목록에 적힌 호스트만** 받는다. tunnelId 는 공개값이고 **credentials 는 Secret `tunnel-creds` 로 레포 밖에서** 만든다 | `charts/cloudflared/values.yaml:1-30` |
| F-11 | 레지스트리: `ghcr.io/medisolveaidev`, 이미지 `mediness-{back,worker,mcp,front}`, 태그 `<sha>-**arm64**`, pull secret `ghcr-pull` | `charts/mediness/values.yaml:6-12` |
| F-12 | PVC 는 **`local-path`** 이고 **lima-worker-1 에서만 프로비저닝**된다(pgdata 디스크가 거기 있다) | `charts/datastores/values.yaml:3-7` |
| F-13 | 큰 파일·장기 보존 자료는 **hostPath `/mnt/mac/...`**(Mac SSD)로 뺀다 — audio · department-space · task-references | `templates/back.yaml:147·149·151` · 값은 `values.yaml:54-56` |
| F-14 | Mediness front 는 **Next.js standalone** 이고 `/api/*` 를 **자기 BFF 로** 받는다 | `templates/front.yaml:1-2` |

---

## 3. 제품 코드의 운영 차단 — **6b 의 첫 작업**

### 3-1. [사실] PRODUCTION 프로파일은 **라우트를 하나도 등록하지 않는다**

```python
# backend/src/ax_workspace/entrypoints/http.py:606
if settings.developer_auth_enabled:
```

- 이 `if` 의 **본문이 606~2528 줄(1923 줄)** 이고, **그 안에 라우트 데코레이터 159 개**가 있다(기계로 셈)
- **게이트 «밖»의 라우트는 `/health` 하나뿐**이다 — `http.py:2530` `@app.get("/health")`.
  **`/api/*` 와 WS 는 하나도 빠짐없이 게이트 «안»이다**
- `developer_auth_enabled` 는 `profile in {DEVELOPMENT, TEST}` 다 — `settings.py:125-126`
- → **`AX_PROFILE=production` 으로 띄우면 `/api/*` 도 `/api/meetings/{id}/stream` 도 없다.**
  앱은 뜨고 **`/health` 만 답한다** — 그래서 **probe 는 초록인데 제품은 아무것도 못 한다**(§4-5 가 이 점을 쓴다)
- WS 스트림도 그 안이다 — `http.py:1009` `@app.websocket("/api/meetings/{meeting_id}/stream")`

### 3-2. [사실] Secure 쿠키는 **PRODUCTION 에서만** 붙는다

```python
# backend/src/ax_workspace/entrypoints/http_auth.py:106-107
def cookie_secure(settings: Settings) -> bool:
    return settings.profile == RuntimeProfile.PRODUCTION
```

- 세션 쿠키는 `scax_session`(`http_auth.py:21`), `httponly` · `samesite="lax"` · `secure=cookie_secure(settings)`
  — `http.py:639-646`

### 3-3. 그래서 **맞물린 교착**이다

> **Secure 쿠키는 PRODUCTION 에서만 붙는다. 그런데 PRODUCTION 에는 로그인 라우트가 없다.**
> 두 조건을 동시에 만족하는 실행 프로파일이 **지금은 존재하지 않는다.**

이것이 SPEC-006 §5 가 「지금 코드는 이 요건을 만족하지 못한다」로 올린 자리(OQ-T02)이고,
**development/test 프로파일로 운영을 우회하는 것은 SPEC 이 명시적으로 승인하지 않는다.**

### 3-4. [기본값] 푸는 방향 — **권한 판정과 라우트 등록을 분리한다**

| 항목 | 제안 | 근거 |
|---|---|---|
| **라우트 등록** | `if settings.developer_auth_enabled:` **게이트를 라우트 등록에서 떼어낸다.** 159 개 라우트는 **프로파일과 무관하게 등록**된다 | 라우트의 «존재»와 «누가 부를 수 있나»는 다른 질문이다. 지금은 한 `if` 가 둘을 겸한다 |
| **권한 판정** | 지금의 판정(세션·역할)을 **그대로 둔다.** 완화하지 않는다 | 발주 금지: 권한 완화·새 인증 도입은 **별도 decision**(OQ-W05) |
| **개발 전용 표면** | `/api/auth/providers` 의 **demo 계정·demo 비밀번호 노출**과 로컬 로그인은 **`local_login_enabled` 로 계속 갈라** PRODUCTION 에서 닫는다 | `http.py:619-627` 이 이미 그 분기를 갖고 있다 |
| **PRODUCTION 의 로그인 수단** | ⚠ **[사용자 결정]** — 로컬 로그인을 닫으면 **PRODUCTION 에 로그인 수단이 없다**(`local_login_enabled` 가 False). 외부 IdP 도입은 **새 제품 계약**이라 이 문서가 정하지 않는다 | §8 D-4 |

> **6b 의 backend 작업은 「라우트 등록을 프로파일에서 떼는 것」까지다.** 그 이상(인증 방식 신설)은
> 멈추고 올린다.

### 3-5. [사실] FE 정적 서빙 자리가 **없다**

- 백엔드에 `StaticFiles` 마운트가 **0건**이다(`backend/src` 전수 검색)
- Mediness 는 Next.js front 가 자기 BFF 를 갖지만(F-14), **Strong Hajin FE 는 Vite SPA** 라
  구조가 다르다 — `frontend/vite.config.ts` · `npm run build` → `dist/`

### 3-6. [사실] 지금 있는 컨테이너 이미지는 **운영용이 아니다**

- `delivery/Dockerfile` 은 **납품용 보호 이미지**이고 `PROTECTED_PLATFORM ?= linux/amd64`(`Makefile:25`)
- 클러스터는 **전 노드 arm64**(F-1) → **그대로 쓸 수 없다.** 운영 이미지는 **새로 만든다**

---

## 4. 같은 origin 설계 — 호스트 하나, 경로 분기

### 4-1. 왜 Mediness 를 그대로 베끼지 않나

Mediness 는 front·api 를 **다른 호스트**로 가른다(F-6). Strong Hajin 은 그럴 수 없다 —
**SPEC-006 이 방향 A(같은 origin)를 골랐고**, 그 덕분에 REST 상대경로·`same-origin` 자격증명 ·
WS 주소 자동 조립 · 쿠키 · 딥링크 · CORS 부재가 **한 줄도 안 바뀐다.** origin 을 가르면 그 일곱이 전부 깨진다.

### 4-2. [기본값] Ingress 한 장 — 경로 셋

| 경로 | 대상 | 비고 |
|---|---|---|
| `/api/meetings/{id}/stream` | back(WS) | **가장 구체적인 규칙을 먼저** 둔다. nginx ingress 는 **가장 긴 prefix 가 이긴다** |
| `/api/` | back(HTTP) | 업로드가 지나므로 `proxy-body-size` 필요 |
| `/` | front(정적 SPA) | SPA 폴백 필요(§4-4) |

**[기본값] annotation** — Mediness api ingress(F-7)를 근거로 같은 값을 쓴다:

```yaml
nginx.ingress.kubernetes.io/proxy-read-timeout: "3600"   # WS 가 끊기지 않게
nginx.ingress.kubernetes.io/proxy-send-timeout: "3600"
nginx.ingress.kubernetes.io/proxy-body-size: "50m"       # 자료 업로드
```

> **WS 는 별도 annotation 이 필요 없다** — ingress-nginx 는 `Upgrade`/`Connection` 헤더를 기본
> 전달한다. 필요한 것은 **타임아웃**이고 그것이 F-7 의 값이다.

### 4-3. [사실 → 설계] 쿠키 `Secure` 의 성립 조건

- 브라우저가 보는 origin 은 **`https://<STRONG_HAJIN_HOST>`** 다 — TLS 는 Cloudflare 에지에서
  종단되고(F-4) 클러스터 안은 평문이다
- 따라서 **`Secure` 쿠키는 성립한다** — 쿠키는 브라우저↔에지 구간에서만 평가된다
- 다만 **백엔드가 그 쿠키를 `Secure` 로 «찍어야»** 하고, 그것은 `AX_PROFILE=production` 일 때만
  일어난다(§3-2) → **§3-4 의 라우트 분리가 선행이다**

### 4-4. [기본값] FE 정적 서빙 — **nginx 사이드 배포**

| 후보 | 판단 |
|---|---|
| **A. 별도 `front` Deployment(nginx:alpine + `dist/`)** | **채택(기본값).** 백엔드에 `StaticFiles` 를 더하지 않아 **제품 코드 변경이 0** 이고, Mediness 의 front/back 분리 관례와도 맞는다 |
| B. 백엔드가 `StaticFiles` 로 SPA 를 서빙 | 제품 코드 변경이 필요하고, WS·업로드와 같은 프로세스에 정적 트래픽을 얹는다 |

**[사실] 이 제품의 딥링크는 «경로»가 아니라 «질의 문자열»이다** — `?interaction=<id>` 다
(`App.tsx:61` 이 `new URLSearchParams(window.location.search).get('interaction')` 로 읽고,
`App.tsx:400-402` 가 닫을 때 그 파라미터를 지우며 `history.replaceState` 한다).
경로는 언제나 `/` 이므로 **딥링크 때문에 404 가 나지는 않는다.**

**SPA 폴백**: 그래도 `try_files $uri /index.html;` 를 **둔다**(기본값) — 앞으로 경로형 주소가
생기거나 사용자가 `/` 아닌 주소를 직접 치는 경우에 대비하는 **한 줄짜리 보험**이고, 지금 구조에서
해가 없다. **「지금 필요해서」가 아니라 「싸고 안전해서」 두는 것**임을 밝힌다.

### 4-5. [기본값] probe 경로 — `/health`

| probe | 경로 | 대상 |
|---|---|---|
| `livenessProbe` | **`GET /health`** | back |
| `readinessProbe` | **`GET /health`** | back |
| front(nginx) | **`GET /`** | 정적 서빙이라 앱 상태와 무관하다 |

**[사실]** `/health` 는 **프로파일 게이트 «밖»에 있는 유일한 라우트**다(`http.py:2530`) —
그래서 `AX_PROFILE=production` 에서도 답한다.

> ⚠ **바로 그 이유로 probe 만 믿으면 안 된다.** §3-1 의 교착이 풀리기 전에는
> **`/health` 는 200 인데 `/api/*` 는 전부 404** 인 상태가 가능하다. **probe 초록 = 제품 정상이
> 아니다.** 6b 는 배포 확인에 `/health` 말고 **실제 API 한 개와 WS 핸드셰이크**를 함께 본다.

---

## 5. Mediness 와의 분리 — 겹치면 안 되는 여덟

| 축 | Mediness [사실] | Strong Hajin [기본값] | 왜 갈라야 하나 |
|---|---|---|---|
| **namespace** | `mediness-dev` · `mediness-prod` | **`strong-hajin-prod`** | AppProject destinations 가 네임스페이스로 제한된다(F-8) |
| **Argo AppProject** | `mediness` | **`strong-hajin`**(신규) | 기존 project 에 destination 을 더하면 **Mediness 파일을 고치게 된다** — diff 0 규칙 위반 |
| **Argo Application** | `mediness-prod` | **`strong-hajin-prod`**(신규 파일) | 〃 |
| **chart** | `charts/mediness` | **`charts/strong-hajin`**(신규 디렉터리) | 〃 |
| **domain / host** | `mediness*.medisolveai.xyz` | **`<STRONG_HAJIN_HOST>`** — ⚠ **[사용자 결정]** | §8 D-1 |
| **데이터 경로** | `/mnt/mac/audio` · `/mnt/mac/department-space` · `/mnt/mac/task-references` | **`/mnt/mac/strong-hajin/{recordings,materials}`** | 같은 경로를 쓰면 두 제품 파일이 섞인다 |
| **DB** | `postgres` (ns 안, datastores 차트) | **같은 차트를 ns 에 따로 배포** — DB 이름·유저 분리 | ⚠ WORK 가 이미 적었다: **새 데이터베이스가 필요하다.** Mediness DB 를 재사용하지 않는다 |
| **레지스트리 namespace** | `ghcr.io/medisolveaidev` | ⚠ **[사용자 결정]** — §8 D-2 | 제품 코드 레포는 `kknaks/Strong_hajin`(DEC-005 D-09)이라 **소유 org 가 다르다** |

### 5-1. 기존 Mediness 파일 diff 0 — **새 파일만 더한다**

6b 가 이 레포에 더할 파일(전부 **신규**):

```
charts/strong-hajin/                          Chart.yaml · values.yaml · values-prod.yaml
                                              templates/{ingress,back,front,worker,configmap,_helpers}.yaml
charts/datastores/values-strong-hajin.yaml    postgres/redis 를 strong-hajin-prod 에 따로 띄우는 값
argocd/projects/strong-hajin-appproject.yaml
argocd/applications/strong-hajin-prod.yaml
argocd/applications/datastores-strong-hajin.yaml
```

**[사실] datastores 는 «차트»가 아니라 «Application 과 values» 로 환경을 가른다** —
`datastores-prod` 는 `path: charts/datastores` + `values-prod.yaml` + `namespace: mediness-prod`
이고 `project: mediness` 다(`argocd/applications/datastores-prod.yaml`). Strong Hajin 도 같은 꼴로,
**같은 차트에 values 파일 하나와 Application 하나를 더한다.**

- `values-strong-hajin.yaml` 은 **기존 `charts/datastores/` 에 «새 파일»을 더하는 것**이라
  Mediness 의 `values-dev.yaml`·`values-prod.yaml` 은 **한 줄도 바뀌지 않는다**
- `datastores-strong-hajin.yaml` 의 `project:` 는 **`strong-hajin`**(신규 AppProject)이고
  `namespace:` 는 **`strong-hajin-prod`** 다. ⚠ `project: mediness` 를 쓰면 **AppProject 의
  destination 제한(F-8)에 걸려 sync 가 거부된다**

**고쳐야 하는 기존 파일은 하나뿐이다** — `charts/cloudflared/values.yaml` 의 `hosts` 목록에
새 호스트 한 줄을 더해야 외부에서 닿는다(F-10). **이것은 Mediness 차트가 아니라 공용 터널 설정**이고,
**한 줄 추가**다. 그 외 Mediness 파일은 **0줄**이다.

---

## 6. 볼륨·백업·rollback — **세 가지를 구분한다**

### 6-1. [기본값] 보존해야 하는 것

| 데이터 | 지금 자리 [사실] | 운영 [기본값] | 유형 |
|---|---|---|---|
| 녹음 원본 | `.scax/recordings`(`settings.py:54`, env `AX_RECORDINGS_DIR`) | **hostPath `/mnt/mac/strong-hajin/recordings`** | 큰 파일 · 재생성 불가 |
| 자료 | `.scax/materials`(`settings.py:52`, env `AX_MATERIALS_DIR`) | **hostPath `/mnt/mac/strong-hajin/materials`** | 〃 |
| DB | postgres | **PVC(`local-path`)** | 구조 데이터 |

**근거**: Mediness 가 큰 파일을 PVC 가 아니라 **hostPath `/mnt/mac/...`** 로 뺀 것과 같은 이유다(F-13) —
`local-path` PVC 는 **lima-worker-1 에만** 잡히고(F-12) VM 재생성에 약하다.

### 6-2. **rollback ≠ 복구** — 섞지 않는다

| | 무엇을 되돌리나 | 수단 | 되돌아가지 «않는» 것 |
|---|---|---|---|
| **rollback** | **배포된 판**(이미지 태그·차트) | Argo 가 `targetRevision: main` 을 추적하므로 **git revert 후 sync**. 또는 values 의 `image.tag` 를 이전 값으로 | **데이터는 그대로다.** 스키마가 앞으로 갔다면 rollback 이 앱을 깨뜨릴 수 있다 |
| **복구(restore)** | **데이터** | DB 덤프 되돌리기 · hostPath 디렉터리 복사 되돌리기 | 배포된 코드 판은 안 바뀐다 |
| **백업(backup)** | — | ⚠ **[사용자 결정]** 주기·보관 위치·대상 — §8 D-5 | — |

> ⚠ **마이그레이션이 있는 판의 rollback 은 자동이 아니다.** Mediness 는 `alembic` 을 이미지 CMD 에서
> 돌린다(`templates/back.yaml:3`). Strong Hajin 도 같은 형태라면 **앞으로 간 스키마를 코드만
> 되돌리는 것은 위험하다** — 6b 가 롤백 절차에 이 조건을 적어야 한다.

---

## 7. Phase 6b 작업 분해 — 소유와 파일 범위

| # | 작업 | 소유 | 파일 범위 | 선행 |
|---|---|---|---|---|
| **B-1** | **라우트 등록을 프로파일에서 분리**(§3-4). 권한 판정·쿠키 계약은 **그대로** | **backend 워커** | `backend/src/ax_workspace/entrypoints/http.py` · `http_auth.py` · `bootstrap/settings.py` | — |
| **B-2** | PRODUCTION 기동 확인(라우트 등록 + `Secure` 쿠키 동시 성립) + 회귀 테스트 | **backend 워커** | `backend/tests/**` | B-1 |
| **I-1** | `charts/strong-hajin/` 신규 차트(ingress 경로 분기 · back · front · worker · configmap) | **인프라 워커** ⚠ P-5 | `k8s_infra_mac/charts/strong-hajin/**`(신규) | D-1 |
| **I-2** | `argocd/projects/strong-hajin-appproject.yaml` · `applications/strong-hajin-prod.yaml` | **인프라 워커** ⚠ P-5 | 위 두 신규 파일 | — |
| **I-2b** | **datastores 분리** — `charts/datastores/values-strong-hajin.yaml`(신규) + `argocd/applications/datastores-strong-hajin.yaml`(신규). **Mediness values 는 손대지 않는다** | **인프라 워커** ⚠ P-5 | 위 두 신규 파일 | I-2(AppProject 가 먼저 서야 한다) |
| **I-3** | `charts/cloudflared/values.yaml` **hosts 한 줄 추가** + DNS CNAME(`cloudflared tunnel route dns`) | **인프라 워커** ⚠ P-5 | 기존 파일 **1줄** | D-1 |
| **I-4** | **arm64 운영 이미지** 빌드·푸시(back · front) | **인프라 워커** ⚠ P-5 | 신규 Dockerfile(제품 레포) · CI 없음 | D-2 |
| **F-1** | FE 운영 빌드 산출물(`npm run build` → `dist/`)을 **nginx 이미지에 싣는 Dockerfile** | **frontend 워커** | 제품 레포 신규 `frontend/Dockerfile`(또는 `delivery/` 아래 별도) | D-2 |
| **F-2** | 제품 셸의 `shell.config.json` · capability `remote.urls` **두 자리를 운영 origin 으로** | **기본은 Phase 8 소유**(frontend 워커). **6b 로 당길지는 코디 판단** — §7-1 | `frontend/src-tauri/shell.config.json` · `capabilities/product-shell.json` | D-1 |
| **C-1** | 순서 조율 · 승인 게이트 · 배포 실행 판정 | **코디** | — | — |
| **C-2** | 비밀값 생성(`ghcr-pull` · DB 비밀번호 등)을 **레포 밖에서** | **코디/사용자** | 레포 아님 | D-2 |

### 7-1. F-2 는 Phase 8 과 겹친다 — 중복 실행하지 않는다

WORK 는 **운영 origin 을 박고 최종 빌드까지 하는 것을 Phase 8** 로 두었다(「발행판의 설정을 사후에
고치지 않는다」). **그래서 F-2 의 «기본 소유는 Phase 8»** 이다 — 6b 는 운영 origin 이 «서는» 것까지만 하고,
셸 설정에 값을 박는 것은 Phase 8 이 한다. **6b 로 당겨 할지는 코디가 정한다**(당기면 Phase 8 은
그 값을 **다시 박지 않고 검증만** 한다).

### 7-2. ⚠ P-5 — **인프라 워커가 아직 정의되지 않았다**

- 이 저장소의 역할 정의(`orchestration/roles/strong-hajin/`)에는 **frontend · backend · planner ·
  reviewer** 가 있고 **인프라(k8s) 역할이 없다**
- I-1 ~ I-4 는 **다른 레포(`MediSolveAIDev/k8s_infra_mac`)를 고치고 클러스터에 배포**하는 일이라
  기존 역할의 allowed_paths 밖이다
- → **6b 착수 전에 인프라 워커의 역할·권한·레포 접근을 정의해야 한다.** 그렇지 않으면
  I-1 ~ I-4 는 **주인이 없다**

---

## 8. 사용자 결정 — 이것 없이는 6b 가 막힌다

| ID | 결정거리 | 막는 것 | 이 문서가 정하지 «않는» 이유 |
|---|---|---|---|
| **D-1** | **운영 호스트 이름** `<STRONG_HAJIN_HOST>` — Cloudflare zone(`medisolveai.xyz`)의 단일 레벨 서브도메인이어야 한다(F-5) | I-1 · I-3 · F-2 · **M-1 최종 확인** · SPEC OQ-T02 | **도메인을 발명하지 않는다**(발주 금지) |
| **D-2** | **레지스트리 namespace** — Mediness 의 `ghcr.io/medisolveaidev` 를 쓸 것인가, 별도 org/개인 namespace 를 쓸 것인가 | I-4 · F-1 · C-2 | 제품 레포가 `kknaks/Strong_hajin` 이라 **org 소유가 다르다**. **외부 레포 권한을 발명하지 않는다**(OQ-W02) |
| **D-3** | **회사 org 레포(`MediSolveAIDev/k8s_infra_mac`)에 개인 제품 구성을 올려도 되는가** | I-1 ~ I-3 **전부** | OQ-W02. 푸시·PR 시점의 확인 사항이다 |
| **D-4** | **PRODUCTION 의 로그인 수단** — 로컬 로그인을 닫으면 로그인할 방법이 없다(§3-4) | B-1 의 «끝». 라우트만 열고 로그인 수단이 없으면 **아무도 못 들어간다** | 외부 IdP 도입은 **새 제품 계약**(OQ-W05) |
| **D-5** | **백업 주기·보관 위치·대상**(§6-2) | 운영 시작 «후»의 안전. 배포 자체는 안 막는다 | 운영 정책이다 |
| **D-6** | **dev 환경을 둘 것인가** — Mediness 는 dev/prod 둘이다(F-8) | 없음(prod 만으로 시작 가능) | 비용·복잡도 판단 |

---

## 9. 검증 — 발주가 요구한 셋

| 확인 | 결과 |
|---|---|
| **사실/기본값/사용자 결정의 혼합이 없는가** | 각 항목에 **[사실] / [기본값] / [사용자 결정]** 을 달았다. [사실]에는 파일 좌표를, [기본값]에는 근거를, [사용자 결정]에는 **막는 것**을 붙였다 |
| **6b 가 추가 설계 없이 착수 가능한가** | **B-1 · B-2 는 즉시 착수 가능**(선행 결정 없음). **I-1 ~ I-4 (I-2b 포함) · F-1 · F-2 는 D-1/D-2/D-3 가 선행**이고, **P-5(인프라 워커 미정의)가 그 앞에 있다** — §7-2 |
| **기존 Mediness diff 0** | `git -C k8s_infra_mac status --porcelain` → **0줄**(HEAD `46fdf88`, clean). 이 회차는 **읽기만 했다**. 6b 가 더할 것은 **신규 파일**이고, 기존 파일 수정은 **cloudflared hosts 한 줄뿐**임을 §5-1 에 명시 |

---

## 10. 이번 회차에서 하지 않은 것

- 인프라 레포 수정 **0줄** · 제품 코드 수정 **0줄** · 클러스터 조작 **0건**
- 운영 도메인·비밀값·외부 레포 권한 **발명 0** — 빈 자리와 결정 ID 로 남겼다
- **development/test 프로파일로 운영을 우회하는 설계를 쓰지 않았다** — 대신 §3-4 로 정면으로 푼다
- **Vercel 을 전제하지 않았다** — DEC-005 D-08 대로 Mac Studio 클러스터 기준이다
- 커밋 · push · PR · Release · 배포
- 문서 **이 파일 하나**만 썼다
