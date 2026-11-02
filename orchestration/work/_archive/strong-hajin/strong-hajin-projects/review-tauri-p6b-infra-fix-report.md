# WORK-006 Phase 6b 인프라 WARN 보정 — 독립 재검수

- **인프라 레포**: `/Users/kknaks/git/harness_works/k8s_infra_mac` · HEAD **`46fdf88`**(변동 없음)
- **검수 대상**: `charts/strong-hajin/templates/ingress.yaml` · `tauri-p6b-infra-report.md`
  (직전 검수 `review-tauri-p6b-infra-report.md` 의 **W-1 · W-2 · W-3**)
- **read-only 검수.** `kubectl` · `helm install/upgrade` **0회.** `lint`·`template` 은 로컬 렌더.
- **이 검수 보고서 한 파일만 작성.**

---

## 0. 종합 판정 — **FAIL 0 · WARN 1(낮음) · 나머지 PASS**

**세 지적이 모두 닫혔고, 둘은 요구보다 멀리 갔다.**

- **W-1**: runbook 에 **`0)` AppProject 선행 적용**이 들어갔다. 순서 한 줄이 아니라
  「**순서가 아니라 «선행 조건»**」으로 성격을 적었고, **「그때 나오는 오류는 «호스트가 틀렸다»가
  아니라 «project 를 찾을 수 없다»라 엉뚱한 곳을 보게 만든다」**는 **진단 힌트**까지 붙였다.
  요구하지 않은 **승인 게이트**(§9 머리말 ⛔ · 본문 구분선 · §9-1 표)도 함께 세웠다.
- **W-2**: 주석이 `three paths` → **`FOUR paths`** 로 고쳐졌고, **네 경로를 나열**하고
  **왜 그 순서로 적었는지**(최장 prefix 우선 → 파일이 라우터가 푸는 순서대로 읽히게)까지 적었다.
- **W-3**: §3-6 신설. **제품 코드를 직접 확인해** `local_login_enabled` 와 demo 계정 노출을
  근거로 적었고, **D-6 을 「비용·복잡도 판단」에서 「공개 여부·접근 제한 결정」으로 재정의**했다.

**검수가 제품 코드로 §3-6 의 사실을 교차 확인했다** — `settings.py:131`
`return self.profile is not RuntimeProfile.PRODUCTION` · `http.py:625-630` 이 `demo_accounts` 와
`demo_password` 를 **응답 본문에** 싣는다. **보고서의 서술이 원문과 일치한다.**

**helm 수치가 그대로다**(lint 4종 exit 0 · WARN 8 · 주입 없으면 실패 · prod 10 / dev 6).
**이번 회차 변경은 `ingress.yaml` 하나**이고 `git diff --stat` 은 여전히 **0줄**이다.

WARN 1 건은 **새 runbook 안에서 승인 게이트 선이 `0)` 보다 아래에 그어진 것**이다.

---

## 1. 판정표

| # | 발주 확인 항목 | 판정 |
|---|---|---|
| 1 | runbook 에 AppProject 선행 적용 | **PASS** |
| 2 | runbook 에 승인 경계 | **PASS** (게이트 위치는 W-1) |
| 3 | ingress 주석이 실제 4경로와 일치 | **PASS** |
| 4 | `values-dev` `profile=development`/demo auth · D-6 개발 전용 경계 문서화 | **PASS** (제품 코드로 교차 확인) |
| 5 | chart/infra/기존 Mediness 무변경 | **PASS** |
| 6 | helm 검증 수치 유지 | **PASS** (전부 재현) |

---

## 2. FAIL

**없다.**

---

## 3. 항목별 확인

### 3-1. W-1 — AppProject 선행 적용 + 승인 경계 (PASS)

**신설된 `0)`**:

```
0) argocd/projects/strong-hajin.yaml (AppProject) 를 **먼저** 적용한다
   ⚠ 이것이 없으면 두 Application 은 «project: strong-hajin 이 없다»로 거부된다.
     AppProject 가 destination(strong-hajin-prod) 을 여는 문이고, 그 문이 없으면
     Application 은 sync 를 시작조차 못 한다. 순서가 아니라 «선행 조건»이다.
```

- 내가 지적한 것은 **한 줄 추가**였다. 구현은 ① **왜 필요한지**(root-app 이 보지 않는 디렉터리)
  ② **빠뜨리면 무슨 오류가 나는지** ③ 그 오류가 **엉뚱한 곳을 보게 만든다**는 것까지 적었다.
  검수가 직전 회차에 확인한 사실(`root-app.yaml` `path: argocd/applications` · `recurse: false` ·
  `argocd/projects` 를 가리키는 Application **0건**)과 정확히 맞는다.
- **승인 경계도 함께 세웠다**(요구 밖):
  - §9 머리말: 「⛔ **사용자·코디의 명시적 승인 전에는 다음 워커도 하지 않는다.**
    아래는 승인이 난 뒤의 순서지 **지금 실행해도 되는 목록이 아니다.**」
  - 본문 구분선: `──── 여기서부터 클러스터를 건드린다 · 승인 게이트 ────`
  - **§9-1 「승인 경계 — 이 워커가 넘지 않은 선」** 표: 레포(작성 ↔ **커밋·push·PR 안 함**) ·
    helm(`lint`/`template` ↔ **`install`/`upgrade` 안 함**) · 클러스터(**아무것도** ↔ `kubectl apply`·sync)
  - 「**이 워커의 검증은 클러스터 상태에 대해 아무것도 증명하지 않는다**」 — 관문 보고서들이
    지켜 온 「통과가 뜻하지 않는 것」과 같은 태도다.
- **순서도 개선됐다** — `5) datastores 를 먼저 수동 sync(앱보다 DB 가 먼저 서야 한다)` 가 새로 들어갔다.

### 3-2. W-2 — ingress 주석이 네 경로와 일치 (PASS)

```make
# ONE Ingress, ONE host, FOUR paths:
#   /api/meetings  -> back   (live transcript WebSocket)
#   /api           -> back   (everything else under the API)
#   /health        -> back   (the only route outside the profile gate)
#   /              -> front  (the SPA)
```

- 숫자만 고치지 않고 **네 경로를 나열**했고, 경로 우선순위 설명도
  「**최장 prefix 가 이기므로 `/api/meetings` 가 `/api` 를, `/health` 가 `/` 를 이긴다.
  파일이 라우터가 푸는 순서대로 읽히도록 길이 내림차순으로 적었다**」로 다듬어졌다.
- **렌더 실측이 주석과 일치한다**:
  `/api/meetings → back:28080` · `/api → back:28080` · `/health → back:28080` · `/ → front:80`
- 파일 전체에서 `three` **0건**.

### 3-3. W-3 — dev 프로파일 · demo auth · D-6 (PASS — 제품 코드로 교차 확인)

보고서 **§3-6** 이 신설됐다. **검수가 주장 셋을 원문에서 직접 확인했다**:

| 보고서의 주장 | 제품 코드 원문 | 판정 |
|---|---|---|
| `local_login_enabled` = **`profile is not PRODUCTION`** | `bootstrap/settings.py:129-131` — `def local_login_enabled(self) -> bool: … return self.profile is not RuntimeProfile.PRODUCTION` | ✅ **문장까지 일치** |
| `GET /api/auth/providers` 가 **demo 계정 목록과 demo 비밀번호를 응답 본문에** 담는다 | `entrypoints/http.py:625-630` — `if settings.local_login_enabled:` → `answer["demo_accounts"] = …` · `answer["demo_password"] = DEMO_PASSWORD` | ✅ |
| PRODUCTION 은 둘 다 돌려주지 않는다 | 같은 분기 밖 — Phase 6b 백엔드 검수에서 `{"local": False, "oidc": False}` 로 확인했다 | ✅ |

- **위험을 구체적으로 적었다** — 「그 주소에 닿을 수 있는 사람은 **응답 본문에서 계정과 비밀번호를
  그대로 읽어** 로그인할 수 있다. D-1 이 정해져 그 호스트가 Cloudflare 터널로 **공개**되면,
  이것은 **인터넷에 열린 문**이 된다.」
- **D-6 의 성격을 바꿔 적었다** — 「D-6 이 «비용·복잡도» 판단만이 아닌 이유가 이것이다.
  dev 를 두기로 한다면 **공개 여부·접근 제한**을 함께 정해야 한다.」
  내가 요구한 것은 **한 줄 각주**였는데, **결정의 정의 자체를 고쳤다.**
- **기본값을 「없음」에 두었다** — dev Application 파일을 만들지 않은 것을
  「**띄우는 장치는 없다**」로 명시. 검수 확인: `argocd/applications/` 에 `strong-hajin-dev.yaml` **없음**.
- **values 파일은 한 글자도 안 고쳤다**(mtime `00:55:53` — 직전 회차 그대로).

### 3-4. 무변경 (PASS)

| 확인 | 결과 |
|---|---|
| **이번 회차 변경** | **`charts/strong-hajin/templates/ingress.yaml` 하나**(mtime **01:07:36**) + 보고서 |
| 나머지 차트/argocd 파일 | mtime **00:55~01:00** — 직전 회차 그대로(`values-dev.yaml` 00:55:53 포함) |
| **tracked diff** | `git diff --stat` → **0줄** |
| `git status --porcelain` | **신규 5항목만** — 직전과 동일 |
| HEAD | **`46fdf88`** · 커밋·태그·push **없음** |
| Mediness · datastores 기존 values · cloudflared | **무편집** |

### 3-5. helm 수치 유지 (PASS — 전부 재실행)

| 실행 | **재현 결과** |
|---|---|
| `helm lint` (values.yaml / prod / dev / datastores) | **exit 0 · 0 · 0 · 0** — `missing required values` **WARN 8건** |
| `helm template` prod, 주입 없음 | **exit 1** — `ingress.yaml … host is not set (D-1) … does not invent a domain` |
| `helm template` prod + 주입 + `worker.kinds={4}` | **exit 0 · 10 오브젝트** |
| `helm template` dev + 주입 | **exit 0 · 6 오브젝트** |
| 렌더 오염 | `medisolveai.xyz` **0건** · ConfigMap data 에 `CORS_ORIGINS` **False** |

→ **주석 편집이 렌더를 건드리지 않았다.** 직전 검수의 수치와 **완전히 같다.**

---

## 4. WARN (1건 · 낮음)

### W-1 — **`0)` 이 승인 게이트 «위»에 있다**

**좌표**: `tauri-p6b-infra-report.md` §9

- §9 머리말: 「이 순서의 **3) 부터는** «클러스터에 손대는» 일이다 … **1)·2) 는 레포/이미지 작업**이라
  그 앞에 둘 수 있다」 — **`0)` 을 언급하지 않는다.**
- 본문 구분선도 **2) 와 3) 사이**에 그어져 있다.
- 그런데 **`0)` 은 `argocd/projects/strong-hajin.yaml` 을 «적용»하는 일** — 즉 **클러스터 쓰기**다.
  §9-1 표가 「클러스터: 한 것 **아무것도** / 하지 않은 것 **`kubectl apply` · AppProject 적용**」로
  **AppProject 적용을 명시적으로 클러스터 조작으로 분류**하고 있어, **§9 본문과 §9-1 이 어긋난다.**

**왜 사소하지 않은가(그러나 왜 WARN 인가)**
- 이 워커는 **아무것도 적용하지 않았으므로** 지금 위반은 없다. 문제는 **다음 워커가 읽을 지시**다.
- 「3) 부터 승인」으로 읽으면 **0) 을 승인 전에 해도 되는 것으로** 읽을 수 있다.
- 다만 머리말이 「**아래는 승인이 난 뒤의 순서지 지금 실행해도 되는 목록이 아니다**」라고 **전체를**
  덮고 있어, 전체를 읽으면 오해 여지가 줄어든다 — 그래서 FAIL 이 아니다.

**수정 방향**(한 줄): 구분선을 **`0)` 위로** 올리고, 머리말의 「3) 부터는」을
「**0) 부터는**(1·2 는 레포/이미지 작업이라 그 사이에 둘 수 있다)」로 바꾼다.

---

## 5. 차단·미결 (유지)

| # | 항목 | 상태 |
|---|---|---|
| 1 | **D-1** 운영 호스트 · **D-2** 레지스트리 · **I-4** arm64 태그 | `host/registry/tag: ""` → **template 실패**(재현) |
| 2 | **D-3** 회사 org 레포 push 허용 여부 | 커밋조차 하지 않음 |
| 3 | **D-4** PRODUCTION 로그인 수단 | `NOTES.txt` 「아무도 로그인할 수 없다」 |
| 4 | **D-6** dev 환경 | 자리만 · dev Application **없음** · **§3-6 이 공개 위험을 결정 요소로 추가** |
| 5 | **I-3** cloudflared hosts · **D-5** 백업 | 미수행 · 미결 |
| 6 | 클러스터 상태 | **아무것도 증명되지 않았다**(§9-1) |

---

## 6. 한 줄 정리

**세 지적이 닫혔고, W-1(AppProject)과 W-3(dev 프로파일)은 내가 요구한 한 줄을 넘어
«왜»와 «결정의 성격»까지 다시 썼다** — 특히 §3-6 은 제품 코드 두 곳을 인용했고, 검수가 원문과
대조해 **문장까지 일치**함을 확인했다. 이번 회차 변경은 `ingress.yaml` 하나이고 helm 수치와
`git diff` 0줄이 그대로다. 남은 것은 **runbook 의 승인 게이트 선을 `0)` 위로 올리는 한 줄(W-1)** 뿐이다.
