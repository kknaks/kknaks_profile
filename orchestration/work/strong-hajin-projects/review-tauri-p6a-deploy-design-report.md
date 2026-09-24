# WORK-006 Phase 6a 운영 배포 설계 — 독립 검수

- **검수 대상**: `tauri-deploy-design.md`
- **대조**: `k8s_infra_mac`(HEAD `46fdf88`) · 제품 코드(HEAD `a1f6791`) · `tauri-p6a-deploy-design-brief.md`
- **제품 코드·인프라 레포 수정 0줄. 이 보고서 한 파일만 작성.**

---

## 0. 종합 판정 — **FAIL 1 · WARN 5**

**설계의 골격과 판단은 옳다.** 인프라 근거 F-1 ~ F-14 의 좌표를 **전수로 열어 확인했고 전부
맞다.** clean/diff 0 도 재현된다. 같은 origin 경로 분기 · nginx 정적 서빙 · Mediness 분리 ·
미결 발명 금지 · P-5 명시까지 발주가 요구한 항목이 **모두 들어가 있다.**

**FAIL 은 한 자리다** — §3-1 의 「게이트 «밖»의 라우트는 **0 개**다(기계로 셈)」가 **사실과 다르다.**
게이트 밖에 `@app.get("/health")` 가 **1 개 있다**(`http.py:2530`). 라우트 수도 155 가 아니라 **159**다.
**결론(「PRODUCTION 에 `/api/*` 도 WS 도 없다」)은 그대로 옳지만**, 이 오류가 **설계의 빈칸과
맞물린다** — 그 `/health` 야말로 **B-1 이전에도 PRODUCTION 에서 도는 유일한 경로**이고,
k8s liveness/readiness probe 가 쓸 자리인데 **이 설계에는 probe 가 한 줄도 없다.**

---

## 1. 판정표

| # | 발주 검수 항목 | 판정 |
|---|---|---|
| 1 | k8s_infra_mac 근거 좌표 정확성 | **PASS** (F-1~F-14 전수 확인 · 좌표 미세 어긋남은 W-2) |
| 2 | clean / diff 0 주장 | **PASS** (HEAD `46fdf88` · `status --porcelain` **0줄**) |
| 3 | PRODUCTION 라우트 미등록의 **정확한 표현** | **FAIL** (§3-1 — 아래 F-1) |
| 4 | Secure 쿠키 충돌의 정확한 표현 | **PASS** |
| 5 | development/test 우회를 기본안으로 쓰지 않음 | **PASS** |
| 6 | 같은 origin `/` · `/api/*` · WS · FE nginx · 데이터/PVC/DB 분리가 **6b 로 옮겨지는가** | **PASS** (단 DB 배포 산출물 누락 — W-1) |
| 7 | 미결 사용자 결정을 발명하지 않음 | **PASS** |
| 8 | 6b 소유표 · P-5 인프라 워커 미정의 명시 | **PASS** |
| 9 | 코드·인프라 무수정 | **PASS** (0줄) |

---

## 2. FAIL

### F-1 — §3-1 「게이트 밖의 라우트는 0 개」가 **틀렸다**. 그리고 그 오류가 probe 설계 공백과 맞물린다

**위치**: `tauri-deploy-design.md` §3-1 (두 번째·세 번째 불릿)

| 주장 | 실제 | 확인 방법 |
|---|---|---|
| 「본문이 606~2528 줄」 | **맞다** — 게이트 안 마지막 라우트는 `@app.post("/api/tasks/{task_id}/cancel")` (`http.py:2522`) | `sed -n '2520,2537p'` |
| 「그 안에 라우트 데코레이터 **155 개**가 전부」 | **159 개**다(게이트 안). 파일 전체는 **160 개** | `awk 'NR>=606&&NR<=2528' \| grep -c '@app\.'` |
| 「게이트 «밖»의 라우트는 **0 개**다(기계로 셈)」 | **1 개 있다** — `@app.get("/health")` (`http.py:2530`), `create_app()` 안이지만 **`if` 밖**이다 | `awk 'NR>2528' \| grep -n '@app\.'` |

**왜 이 오류가 났는가(추정)**: 「밖」을 **들여쓰기 0** 으로 셌을 가능성이 높다. 모든 라우트가
`create_app()` 안에 있어 **들여쓰기 0 인 데코레이터는 실제로 0 개**다. 그러나 게이트는 `if` 이고,
`/health` 는 그 `if` 의 형제다.

**결론은 바뀌지 않는다** — `/api/` 로 시작하는 라우트와 `@app.websocket(...)` 은 **전부 게이트 안**이다
(`@app.websocket` 은 파일 전체에 **1 개**, `http.py:1009`, 게이트 안). §1-2 의 「가장 큰 차단은
제품 코드다」와 §3-4 의 방향은 **그대로 유효하다.**

**그런데 설계상 실해가 있다**:
- `/health` 는 `{"status":"ok","profile":settings.profile}` 를 돌려주고 **PRODUCTION 에서도 산다.**
  즉 **B-1 이전에도 pod 가 «살아 있다»고 답할 수 있는 유일한 경로**다
- 그런데 이 설계에는 **liveness/readiness probe 가 한 줄도 없다** — §4-2 ingress 표에도, §7 I-1 의
  차트 범위에도 없다. Mediness `back.yaml` 은 실제로 probe 를 갖는다
- **「라우트가 0 개」라고 적어 버리면 6b 인프라 워커는 probe 로 쓸 경로가 없다고 읽는다**

**수정 방향**
1. §3-1 의 숫자를 **159** 로, 「게이트 밖 0 개」를 **「게이트 밖은 `/health` 하나뿐 (`http.py:2530`) —
   `/api/*` 와 WS 는 전부 안쪽」** 으로 고친다
2. §4-2 또는 §7 I-1 에 **probe 경로 `/health`** 를 **[기본값]** 으로 추가한다.
   B-1 전후 모두 유효하므로 **선행 의존이 없다**

---

## 3. WARN

| # | 내용 | 위치 | 수정 방향 |
|---|---|---|---|
| **W-1** | **DB 배포 산출물이 목록에서 빠졌다.** §5 는 「`charts/datastores` 를 ns 에 따로 배포」로 정했는데, **§5-1 의 신규 파일 목록과 §7 I-2 에 그 Argo Application 이 없다.** 실제로 `datastores-prod.yaml` 은 `project: mediness` · `namespace: mediness-prod` 라 **재사용이 불가능**하고, `charts/datastores/` 에는 `values-{dev,prod}.yaml` 만 있어 **Strong Hajin 용 values 파일도 새로 필요**하다. 「6b 가 추가 설계 없이 착수 가능한가」에 걸리는 유일한 실질 공백 | `§5-1` · `§7` I-2 | 신규 파일 둘을 목록에 추가: `argocd/applications/datastores-strong-hajin.yaml`(project `strong-hajin` · ns `strong-hajin-prod`) · `charts/datastores/values-strong-hajin.yaml`. **기존 Mediness 파일은 여전히 0줄**이므로 diff 0 규칙과 충돌하지 않는다 |
| **W-2** | **좌표 미세 어긋남 3건** — F-6 `_helpers.tpl:5-7` → 실제 host define 은 **4~6행**. F-13 `back.yaml:147-151` → 실제 hostPath 셋은 **146~151**. §4-4 의 `App.tsx:401` → `history.replaceState` 는 **402행**. **내용은 전부 맞다** | §2 · §4-4 | 숫자만 보정. 근거 자체는 유효 |
| **W-3** | **§5 제목이 「겹치면 안 되는 **다섯**」인데 표의 행은 8개**(namespace · AppProject · Application · chart · domain · 데이터 경로 · DB · 레지스트리) | `§5` 제목 | 「여덟」로 고치거나 제목에서 수를 뺀다 |
| **W-4** | **§4-4 의 딥링크 예시가 이 제품과 맞지 않는다.** 「`/meetings/...` 가 404 가 되지 않게」라고 썼으나, 이 앱은 **경로가 아니라 쿼리 파라미터**(`?interaction=`)로 화면을 가르므로 그런 경로가 생기지 않는다. **결론(폴백을 두는 편이 안전)은 타당**하고 본문도 「항상 `/` 로 떨어져도 동작한다」고 이미 하자를 밝혔다 | `§4-4` | 예시를 `?interaction=` 로 바꾸거나 「장래 라우터 도입 대비」로 근거를 바꾼다 |
| **W-5** | **F-2(셸 설정에 운영 origin 박기)의 주인이 열려 있다.** §7-1 이 「6b 가 당겨 할지는 코디가 정한다」로 **정직하게 미정으로 두었으나**, §7 표에는 `frontend 워커` 로 적혀 있어 **표만 보면 6b 작업으로 읽힌다** | `§7` F-2 행 | 표의 소유 칸에 「**Phase 8 기본 · 6b 는 코디 판단**」을 함께 적는다 |

---

## 4. PASS — 직접 확인한 것

### 4-1. 인프라 근거 F-1 ~ F-14 — **전수 확인, 전부 사실**

| F | 확인 |
|---|---|
| F-4 | `ingress.yaml:2-3` 「TLS is terminated at the Cloudflare edge (no cert-manager), so these are plain HTTP」 — **좌표까지 정확** |
| F-5 | `_helpers.tpl` 주석 「Universal SSL covers `*.<zone>` but NOT `a.b.<zone>`」 — **정확** |
| F-6 | front `<prefix>.<domain>` · api `<prefix>-api` · mcp `<prefix>-mcp` — **정확**(행 번호만 W-2) |
| F-7 | api 블록 `proxy-read-timeout: "3600"` · `proxy-send-timeout: "3600"` · `proxy-body-size: "50m"` — **정확** |
| F-8 | `sourceRepos` 1개 · destinations `mediness-dev`/`mediness-prod` 2개 — **정확** |
| F-9 | `targetRevision: main` · `path: charts/mediness` · `values-prod.yaml` · `prune`·`selfHeal` · `CreateNamespace=true` — **정확** |
| F-10 | `tunnelId` 공개값 · `credsSecret: tunnel-creds` 「created out-of-band」 · hosts 목록이 곧 노출 범위 — **정확** |
| F-11 | `ghcr.io/medisolveaidev` · tag `…-arm64` · `imagePullSecrets: ghcr-pull` — **정확** |
| F-12 | 「local-path … only provisions on lima-worker-1 (the pgdata disk owner)」 — **정확** |
| F-13 | audio · deptspace · taskrefs 가 `hostPath` — **정확** |
| F-14 | 「front — Next.js standalone … same-origin BFF `/api/*`」 — **정확** |
| §6-2 | `back.yaml:3` 「alembic runs in the image CMD」 — **정확** |

- **`medisolveai.xyz` 는 발명이 아니다** — 레포의 실제 zone 이다(`cloudflared/values.yaml:20-28`).
  Strong Hajin 호스트는 **`<STRONG_HAJIN_HOST>` 자리표시**로 비워 두었다.

### 4-2. clean / diff 0 (PASS)
`git -C k8s_infra_mac rev-parse --short HEAD` → **`46fdf88`** · `status --porcelain` → **0줄**. 재현됨.
§5-1 의 「고쳐야 하는 기존 파일은 `charts/cloudflared/values.yaml` 한 줄뿐」도 타당하다 —
`argocd/root-app.yaml` 이 `path: argocd/applications` 를 통째로 보므로(**app-of-apps**) 신규
Application 파일은 **자동으로 잡히고 root-app 을 고칠 필요가 없다.** 검수가 직접 확인했다.

### 4-3. Secure 쿠키 충돌 (PASS)
- `http_auth.py:106-107` `cookie_secure` → `profile == PRODUCTION` — **정확**
- `settings.py:125-126` `developer_auth_enabled` → `{DEVELOPMENT, TEST}` — **정확**
- §3-3 의 **「Secure 쿠키는 PRODUCTION 에서만 붙는데 PRODUCTION 에는 로그인 라우트가 없다 →
  두 조건을 동시에 만족하는 프로파일이 존재하지 않는다」** 는 **정확하고, 교착을 가장 짧게 짚었다.**
- §4-3 이 「TLS 는 에지 종단이지만 **브라우저가 보는 origin 이 https 라 Secure 가 성립**한다」고
  가른 것도 옳다.

### 4-4. development/test 우회 (PASS)
§3-4 가 **라우트 등록과 권한 판정을 분리**하는 정면 해법을 기본안으로 세웠고, 권한 완화는
OQ-W05 로 **명시적으로 배제**했다. §10 에 「development/test 프로파일로 우회하는 설계를 쓰지
않았다」를 못 박았다. **우회 흔적 0.**

### 4-5. 같은 origin · 정적 서빙 · 분리 (PASS, W-1 제외)
- **경로 우선순위**를 명시했다 — WS 경로를 가장 구체적으로 먼저(nginx ingress 는 최장 prefix 승)
- **WS 에 별도 annotation 이 필요 없고 타임아웃이 핵심**이라는 판단이 정확하다
- **FE nginx 사이드 배포**를 채택하고 대안 B(백엔드 `StaticFiles`)를 근거와 함께 기각.
  **`StaticFiles` 마운트 0건**을 검수도 재확인했다(`grep -rn StaticFiles backend/src` → 0)
- **arm64 불일치**도 사실이다 — `Makefile:25` `PROTECTED_PLATFORM ?= linux/amd64` **정확**
- 데이터 경로·PVC·DB 를 `/mnt/mac/strong-hajin/{recordings,materials}` · `local-path` · 별도 DB 로
  갈랐고, 근거(F-12·F-13)가 붙어 있다. `settings.py:52,54` 좌표도 **정확**
- **rollback ≠ 복구 ≠ 백업** 을 세 칸으로 가르고, 「마이그레이션이 앞서 간 판의 rollback 은
  자동이 아니다」를 경고로 남긴 것은 **이 문서에서 가장 값진 대목**이다

### 4-6. 미결 발명 금지 (PASS)
D-1 도메인 · D-2 레지스트리 namespace · D-3 외부 org 레포 권한 · D-4 **PRODUCTION 로그인 수단** ·
D-5 백업 정책 · D-6 dev 환경 — **여섯 전부 [사용자 결정]** 이고 각각 **막는 것**이 붙어 있다.
특히 **D-4** 는 「라우트만 열고 로그인 수단이 없으면 아무도 못 들어간다」로, §3-4 를 실행해도
남는 구멍을 **스스로 찾아 올렸다.** 발명 0.

### 4-7. 6b 소유표 · P-5 (PASS)
- B-1·B-2(backend) · I-1~I-4(인프라) · F-1·F-2(frontend) · C-1·C-2(코디) — **소유·파일 범위·선행**
  세 칸이 모두 채워져 있다
- **§7-2 P-5** 가 「역할 정의에 인프라(k8s) 워커가 없다 → I-1~I-4 는 **주인이 없다**」를 명시했다.
  검수도 `orchestration/roles/strong-hajin/` 에 인프라 역할이 없음을 확인했다

---

## 5. 6b 착수 가능성 — 검수 의견

| 작업 | 착수 가능? |
|---|---|
| **B-1 · B-2**(backend) | **즉시 가능.** 선행 결정 없음. 단 F-1 수정 후 **`/health` 가 이미 게이트 밖이라는 사실**을 반영할 것 |
| **I-1 ~ I-4**(인프라) | **D-1·D-2·D-3 선행 + P-5 해소 필요.** 여기에 **W-1(DB 배포 산출물) 추가 정의**가 더 필요하다 |
| **F-1**(FE 이미지) | D-2 선행 |
| **F-2**(셸 설정) | D-1 선행 · **Phase 8 과 소유 중복**(W-5) |

→ **「추가 설계 없이 착수」는 B-1·B-2 에 한해 성립한다.** 인프라 축은 W-1 을 메우면 성립한다.

---

## 6. 코디에게 올리는 결정거리

1. **F-1 수정**(숫자 159 · `/health` 예외 명시 · probe 경로 추가) — 6b 인프라 착수 전에 반영.
2. **W-1 보강**(datastores Application·values 신규 파일 2개를 §5-1·§7 에 추가) — 이것이 메워져야
   I-1~I-4 가 **추가 설계 없이** 돌아간다.
3. **D-1 · D-2 · D-3 + P-5** — 인프라 축 전체를 막고 있다. **P-5(인프라 워커 정의)가 가장 앞**이다.
4. **D-4(PRODUCTION 로그인 수단)** — B-1 을 끝내도 로그인 수단이 없으면 배포가 무의미하다.
   **B-1 착수와 동시에 결정 절차를 여는 것**을 권고한다.
5. W-2 ~ W-5 는 문구·좌표 정리 수준이다.
