# WORK-006 Phase 6b 인프라 — 독립 검수

- **인프라 레포**: `/Users/kknaks/git/harness_works/k8s_infra_mac` · HEAD **`46fdf88`**(변동 없음)
- **검수 대상**: `charts/strong-hajin/**` · `charts/datastores/values-strong-hajin.yaml` ·
  `argocd/{projects/strong-hajin.yaml, applications/strong-hajin-prod.yaml, applications/strong-hajin-datastores.yaml}` ·
  `tauri-p6b-infra-report.md`
- **read-only 검수.** `kubectl` · `helm install/upgrade` **한 번도 부르지 않았다.**
  돌린 것은 **`helm lint` · `helm template`**(로컬 렌더)와 파일 읽기뿐이다.
- **이 검수 보고서 한 파일만 작성.**

---

## 0. 종합 판정 — **FAIL 0 · WARN 3(낮음) · 나머지 PASS**

**차트의 중심 설계가 옳고, 그 설계가 실제로 동작한다.** 「자리표시로는 렌더되지 않는다」가
구호가 아니라 **`required` 로 강제**되며, 검수가 돌리니 **주입 없이는 exit 1**, 호스트만 주면
**다음 미결(D-2)에서 또 막힌다** — 세 미결이 **독립적으로** 걸린다.

**기존 레포가 한 줄도 바뀌지 않았다** — `git diff --stat` **출력 0줄**, `git status` 는
**신규 5항목(untracked)** 뿐. Mediness · datastores 기존 values · cloudflared · mediness
AppProject/Application **전부 무편집**이고, **`charts/cloudflared/values.yaml` 의 `hosts` 도
건드리지 않았다**(I-3 — D-1 이 없으면 더할 값 자체가 없다는 판단이 옳다).

**보고서의 수치도 정확하다** — lint 4종 exit 0(경고 8건) · 주입 없으면 template 실패 ·
주입하면 prod **10 오브젝트** / dev **6 오브젝트** · datastores Service×2 + StatefulSet×2.
**전부 재현했다.**

WARN 3 건은 **runbook 의 빠진 한 걸음**, **주석 숫자 하나**, **dev 프로파일의 장래 함정**이다.

---

## 1. 판정표

| # | 발주 확인 항목 | 판정 |
|---|---|---|
| 1 | 기존 Mediness/datastores/cloudflared 무수정 · 이름·namespace·AppProject 격리 | **PASS** |
| 2 | chart templates 가 `/` SPA · `/api` REST · WS 경로 · front/back/worker/configmap 경계 반영 | **PASS** |
| 3 | placeholder 를 임의값으로 통과시키지 않음 · lint/template 결과가 정직 · 주입 시 정상 렌더 | **PASS** |
| 4 | datastores 는 신규 파일만 추가 · Mediness values 그대로 | **PASS** |
| 5 | Argo source/path/project/destination 일관 | **PASS** (적용 순서는 W-1) |
| 6 | 클러스터 적용·push·Release·비밀값 열람 없음 · 미결(D-1~D-4, D-6) 유지 | **PASS** |

---

## 2. FAIL

**없다.**

---

## 3. 격리 (PASS)

| 확인 | 결과 |
|---|---|
| **tracked diff** | `git diff --stat` → **0줄** |
| `git status --porcelain` | **신규 5항목만**(`charts/strong-hajin/` · `charts/datastores/values-strong-hajin.yaml` · argocd 셋) |
| HEAD | **`46fdf88`** — 커밋·태그 없음 |
| **cloudflared** | **무편집** — I-3 미수행. 「D-1 이 정해지기 전에는 더할 값이 없다」는 판단이 옳다 |
| namespace | `strong-hajin-prod`(+`-dev` 자리) — mediness ns 와 겹치지 않음 |
| **AppProject** | 신규 `strong-hajin`. destinations 에 **mediness ns 없음** · `sourceRepos` 는 이 레포 하나 |
| Argo 오브젝트 이름 | Application 이름 **중복 0**(기계로 셈) · AppProject 이름 목록에 `strong-hajin` 신규 |
| **렌더물 오염** | prod 렌더에 `medisolveai.xyz` **0건** · `mediness` **1건**(ingress.yaml **주석** 한 줄) |

**`project: mediness` 를 쓰지 않은 이유가 파일에 적혀 있다** — 그 AppProject destinations 에
`strong-hajin-prod` 가 없어 **sync 가 거부된다**. 두 Application 모두 `project: strong-hajin` ✅.

---

## 4. 템플릿 경계 (PASS)

### 4-1. Ingress — 호스트 하나 · 경로 넷 (실측 렌더)

```
host: "strong-hajin.example.invalid"
  /api/meetings → back:28080     ← 최장 prefix 가 이긴다(WS 스트림)
  /api          → back:28080
  /health       → back:28080
  /             → front:80
```

- **WS 전용 annotation 이 없다** — ingress-nginx 가 `Upgrade`/`Connection` 을 기본 전달하므로
  필요한 것은 **타임아웃**이고, Mediness api ingress 와 같은 `3600`/`3600`/`50m` 을 쓴다.
  **근거를 베낀 것이 아니라 «왜 그 값인가»를 적었다.**
- **Mediness 의 호스트 셋을 베끼지 않은 이유**(SPEC-006 단일 origin → 상대 REST·same-origin
  자격증명·WS 자동 조립·세션 쿠키·CORS 부재)가 `values.yaml`·`ingress.yaml`·`Chart.yaml`
  **셋 다**에 적혀 있다.

### 4-2. 경계 — front / back / worker / configmap

| 오브젝트 | 확인 |
|---|---|
| **front** | nginx + SPA · **hostPath 없음 · 노드 자유** · probe 는 `/` (「정적 서빙이라 앱 상태와 무관」) · **SPA fallback 은 이미지의 nginx conf 몫**이라고 명시 |
| **back** | `strategy: Recreate`(hostPath 단일 writer) · `nodeSelector: lima-worker-1` · hostPath **`type: Directory`** → **경로 없으면 파드가 안 뜬다**(빈 임시 디렉터리에 녹음이 쌓이는 것보다 낫다) |
| **worker** | `worker.kinds` **기본 빈 목록 → 0개 렌더** · kind 당 Deployment 하나(「막힌 material 워커가 meeting 워커를 끌고 내려가지 않게」) · back 과 **같은 노드**(같은 hostPath) |
| **configmap** | data 키 **7개**(`AX_PROFILE` `PUBLIC_ORIGIN` `REDIS_URL` `AX_*_DIR` `LOG_LEVEL` `DEBUG`) — **`DATABASE_URL` 없음**, 파드 env 에서 `$(POSTGRES_PASSWORD)` 로 조립 |
| **`CORS_ORIGINS`** | ConfigMap data 에 **없다**(키 목록으로 확인). 유일한 등장은 **「넣지 않은 이유」 주석** — 「한 줄 넣어 두면 SPEC-006 이 일부러 닫은 문을 조용히 다시 연다」 |

- **`$(POSTGRES_PASSWORD)` 확장 순서가 맞다** — `POSTGRES_PASSWORD` 가 `env[]` 에 **먼저** 선언돼
  있어 k8s 가 확장한다(`envFrom` 값은 확장 대상이 아니므로 이 순서가 중요하다). ✅
- **`/health` 의 한계를 차트가 말한다** — back.yaml 주석과 `NOTES.txt` 가 「probe 초록 ≠ `/api/*`
  응답. 실제 API 하나 + WS 핸드셰이크로 확인하라」를 적는다. Phase 8·9 관문과 같은 태도다.
- **비밀값 0** — `secretRef`/`secretKeyRef` **이름만**. 렌더물 평문 비밀값 검사 **0건**.

---

## 5. 자리표시를 통과시키지 않는가 (PASS) — 검수 실측

### 5-1. `helm lint` — **4종 모두 exit 0**, 경고 8건

| 대상 | exit | 비고 |
|---|---|---|
| `charts/strong-hajin` (values.yaml) | **0** | `level=WARN msg="missing required values"` **8건** |
| 〃 `-f values-prod.yaml` | **0** | 〃 |
| 〃 `-f values-dev.yaml` | **0** | 〃 |
| `charts/datastores -f values-strong-hajin.yaml` | **0** | `1 chart(s) linted, 0 failed` |

**보고서 §5-1 의 「4종 통과 · 경고 8건」이 정확하다.** helm **v4.2.3** 이 `required` 미충족을
**ERROR 가 아니라 WARN** 으로 센다는 설명도 출력으로 확인된다.

> 📌 **검수 자신의 정정**: 처음 루프로 잰 값에서 prod/dev 가 `exit 1` 로 보였으나, **셸 문법
> 아티팩트**였다. 직접 실행한 값이 위 표이고 **보고서가 맞다.**

### 5-2. `helm template` — **주입 없이는 실패한다**

| 실행 | exit | 메시지 |
|---|---|---|
| prod, 주입 없음 | **1** | `ingress.yaml:31:15 … host is not set — the operational host is undecided (D-1). … This chart does not invent a domain.` |
| dev, 주입 없음 | **1** | 〃 |
| **host 만 주입**(검수 추가) | **1** | `front.yaml:37:20 … image.registry is not set — registry namespace is undecided (D-2).` |

→ **세 미결이 독립적으로 걸린다.** 하나를 채워도 나머지가 막는다 — 「한 번 뚫으면 다 통과」가 아니다.
**값 파일에는 여전히 `host: "" · registry: "" · tag: ""` 다.**

### 5-3. 주입하면 정상 렌더 — **구조까지 확인**

검수도 **파일에 한 글자도 남기지 않고 명령줄로만** 주입했다(`*.invalid` — 예약 TLD).

| 실행 | exit | 결과 |
|---|---|---|
| prod + `worker.kinds={4}` | **0** | **10 오브젝트** — ConfigMap 1 · Service 2 · **Deployment 6** · Ingress 1 |
| dev(`worker.kinds` 빈 채) | **0** | **6 오브젝트** — worker **0개** |
| datastores `-f values-strong-hajin.yaml` | **0** | **Service ×2 · StatefulSet ×2** · `POSTGRES_USER`/`POSTGRES_DB` 렌더 |

`yaml.safe_load_all` 로 **10 문서 파싱 OK**. `AX_PROFILE: "production"` ·
`PUBLIC_ORIGIN: "https://strong-hajin.example.invalid"` 확인.
**보고서의 모든 수치가 그대로 재현된다.**

---

## 6. datastores (PASS)

- **신규 파일 하나만 추가**됐고 `values.yaml` · `values-dev.yaml` · `values-prod.yaml` 은 **무편집**.
- **키 집합이 기존 차트와 정확히 일치**한다(`worker` · `storageClassName` ·
  `postgres.{image,user,db,existingSecret,passwordKey,storage,resources}` · `redis.{image,storage,resources}`)
  → **조용히 무시되는 키가 없다.** 검수가 기존 `values.yaml` 과 대조해 확인했다.
- 「**스키마가 아니라 별도 postgres**」라는 선택과 그 이유(두 제품 = 두 실패 도메인 = 두 백업 이야기)가
  파일 머리에 적혀 있다. `user`/`db` 를 **밑줄**로 쓴 이유(역할 이름 인용 문제)까지 적었다.
- `storage: 10Gi`(mediness prod 20Gi 보다 작게) 근거도 적혀 있다 — 큰 파일은 DB 가 아니라 Mac 마운트.

---

## 7. Argo 일관성 (PASS)

| 축 | prod | datastores | 확인 |
|---|---|---|---|
| `project` | `strong-hajin` | `strong-hajin` | AppProject destinations 에 **둘 다 포함** ✅ |
| `repoURL` | `…/k8s_infra_mac.git` | 동일 | AppProject `sourceRepos` 와 **일치** ✅ |
| `path` | `charts/strong-hajin` | `charts/datastores` | 실재 ✅ |
| `valueFiles` | `values-prod.yaml` | `values-strong-hajin.yaml` | 실재 ✅ |
| `destination.namespace` | `strong-hajin-prod` | `strong-hajin-prod` | AppProject 허용 목록 안 ✅ |
| `syncOptions` | `CreateNamespace=true` | 동일 | ✅ |
| `syncPolicy.automated` | **주석 처리** | **주석 처리** | 「한 번도 돈 적 없는 차트에 selfHeal 을 켜면 잘못된 렌더 하나가 루프가 된다」 — **판단이 옳다** |

---

## 8. 금지 사항 (PASS)

| 금지 | 확인 |
|---|---|
| 클러스터 적용 · sync | **없음** — 검수도 `kubectl`·`helm install/upgrade` 0회. `lint`/`template` 은 로컬 렌더 |
| 커밋 · push · PR · Release · 태그 | **없음** — HEAD `46fdf88` · 전부 `??` |
| 운영 도메인 발명 | **0** — 비워 두고 **렌더를 실패시켰다**. 검수 주입값도 `.invalid` |
| 비밀값 열람·발명 | **0** — 이름 참조만. 평문 비밀값 렌더 **0건** |
| Mediness 파일 수정 | **0줄** |
| **미결 유지** | **D-1**(`host: ""`) · **D-2**(`image.registry: ""`) · **D-3**(push 시점 문제, 커밋조차 안 함) · **D-4**(`NOTES.txt` 가 「아무도 로그인할 수 없다」) · **D-6**(dev 자리만, Application 없음) · I-4(`tag: ""`) · I-3(미수행) · D-5(백업 미결) — **전부 문서와 파일 양쪽에 남아 있다** |

---

## 9. WARN (3건 · 낮음)

| # | 내용 | 근거 | 수정 방향 |
|---|---|---|---|
| **W-1** | **runbook 에 「AppProject 를 먼저 적용한다」가 빠졌다.** `argocd/root-app.yaml` 은 **`path: argocd/applications` · `recurse: false`** 만 본다. `argocd/projects/` 를 가리키는 Application 은 **레포에 하나도 없다**(기계로 확인) → **`strong-hajin.yaml` 은 사람이 `kubectl apply` 해야 한다.** 그 전에는 두 Application 이 **`project` 를 찾지 못해 sync 되지 않는다.** 보고서 §9 의 7단계에 이 한 걸음이 없다. (Mediness AppProject 도 같은 구조라 **레포 관례**이긴 하다 — 그래서 결함이 아니라 **runbook 누락**이다) | `root-app.yaml:13,15` · `grep -rl "argocd/projects" argocd/` → 0건 | §9 의 **1) 앞**에 「`kubectl apply -f argocd/projects/strong-hajin.yaml`(root-app 이 이 디렉터리를 보지 않는다)」 한 줄 |
| **W-2** | **`ingress.yaml` 머리 주석이 「three paths」라고 적는데 실제로는 넷**이다(`/api/meetings` · `/api` · `/health` · `/`). 보고서 §3-1 은 **「경로 넷」으로 맞게** 적었다 — 어긋난 것은 템플릿 주석 하나다 | `charts/strong-hajin/templates/ingress.yaml` 머리 주석 vs 렌더 실측 | `three` → `four` |
| **W-3** | **`values-dev.yaml` 의 `back.profile: development` 가 장래의 함정이다.** 그 프로파일은 **로컬 로그인과 데모 계정을 연다**(`local_login_enabled`). 지금은 **dev Application 이 없어 무해**하고 **파일 자신이 경고를 적어 두었다**(「Choose deliberately」). 다만 **보고서 §8 의 D-6 칸은 「자리만 만들어 뒀다」까지만 적고 이 사실을 말하지 않는다** — D-6 을 「둔다」로 결정하는 사람이 그 한 줄을 못 볼 수 있다 | `charts/strong-hajin/values-dev.yaml` `back.profile: development` | 보고서 D-6 칸에 「dev 를 열면 **데모 계정 표면이 함께 열린다**(values-dev 의 profile)」 한 줄 |

> 셋 다 **차트 동작을 바꾸지 않는다.** W-1 만 **실제 배포 순서에 영향**이 있으므로 먼저 보는 것이 좋다.

---

## 10. 차단·미결 (유지 — 이번 작업이 풀 수 없는 것)

| # | 항목 | 이 차트에서 드러나는 방식 |
|---|---|---|
| **D-1** 운영 호스트 | `host: ""` → **template 실패** |
| **D-2** 레지스트리 namespace | `image.registry: ""` → **template 실패** |
| **D-3** 회사 org 레포에 개인 제품 구성 | **push 시점** — 커밋조차 하지 않았다 |
| **D-4** PRODUCTION 로그인 수단 | `AX_PROFILE=production` 은 켜지만 **아무도 로그인할 수 없다**(`NOTES.txt` 2번) |
| **D-6** dev 환경 | 자리만 — dev Application **없음**(+ W-3) |
| **I-4** arm64 이미지 · **I-3** cloudflared hosts · **D-5** 백업 | `tag: ""` 실패 · 미수행 · 미결 |

**그래서 지금 이 레포에서 `helm template` 이 실패하는 것이 옳은 상태다.**

---

## 11. 한 줄 정리

**「자리표시로는 렌더되지 않는다」가 `required` 로 강제되고, 세 미결이 독립적으로 걸리는 것까지
검수가 확인했다** — 주입 없이 exit 1, host 만 주면 D-2 에서 또 막히고, 셋을 주면 prod 10 /
dev 6 오브젝트가 정상 렌더된다. **기존 레포는 diff 0줄**이고 Argo 축도 일관된다.
남은 것은 **runbook 의 AppProject 적용 한 걸음(W-1)** 과 주석·문서 두 줄이며,
**Phase 6b 인프라에 기능적 지적은 없다.**
