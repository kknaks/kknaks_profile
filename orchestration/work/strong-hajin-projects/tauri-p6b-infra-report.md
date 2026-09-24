# WORK-006 Phase 6b 인프라 — Strong Hajin 차트 · AppProject · Application

- **작성**: 2026-09-23 **01:00 KST**
- **인프라 레포**: `/Users/kknaks/git/harness_works/k8s_infra_mac` · HEAD `46fdf88`(변동 없음)
- **결과**: 신규 파일 **14개**. **기존 파일 diff 0줄** · 커밋 · push · PR · 클러스터 적용 **전부 0**
- **helm**: v4.2.3 · lint 4종 통과 · template **주입 없이는 의도대로 실패**, 주입하면 정상 렌더

---

## 1. 한 줄 결론

**차트가 «자리표시로는 렌더되지 않게» 만들었다.** 운영 호스트(D-1)·레지스트리(D-2)·이미지 태그(I-4)가
비어 있으면 `helm template` 이 **실패한다** — 그럴듯한 기본값을 넣어 두면 **렌더된 매니페스트에
발명한 도메인이 박히고, 렌더된 매니페스트는 복사된다.** 실패가 곧 이 차트가 작동하는 모습이다.

---

## 2. 새로 만든 파일 — 전부 신규

| 파일 | 무엇 |
|---|---|
| `charts/strong-hajin/Chart.yaml` | 차트 메타 |
| `charts/strong-hajin/values.yaml` | 기본값 — **host · image.registry · image.tag 는 비어 있다** |
| `charts/strong-hajin/values-prod.yaml` · `values-dev.yaml` | 환경별 override(셋은 여전히 비어 있다) |
| `charts/strong-hajin/templates/_helpers.tpl` | host · image · labels. **required 로 발명을 막는다** |
| `charts/strong-hajin/templates/configmap.yaml` | `AX_PROFILE` · `PUBLIC_ORIGIN` · 경로 — **비밀값 없음** |
| `charts/strong-hajin/templates/back.yaml` | Service + Deployment · `/health` probe · hostPath 둘 |
| `charts/strong-hajin/templates/worker.yaml` | `worker.kinds` 당 Deployment 하나(**기본은 0개**) |
| `charts/strong-hajin/templates/front.yaml` | nginx + SPA |
| `charts/strong-hajin/templates/ingress.yaml` | **Ingress 한 장 · 호스트 하나 · 경로 넷** |
| `charts/strong-hajin/templates/NOTES.txt` | **「렌더 성공이 뜻하지 «않는» 것」 다섯** |
| `charts/datastores/values-strong-hajin.yaml` | 별도 postgres/redis 값(**코디 승인 후 추가** — §7) |
| `argocd/projects/strong-hajin.yaml` | **신규 AppProject** — mediness 와 분리 |
| `argocd/applications/strong-hajin-prod.yaml` | 앱 Application |
| `argocd/applications/strong-hajin-datastores.yaml` | datastores Application |

**기존 파일 diff 0줄** — `git diff --stat` **출력 없음**. `git status --porcelain` 은 위 신규 항목만.
`charts/mediness/**` · `charts/datastores/values-{dev,prod}.yaml` · `charts/cloudflared/**` ·
mediness AppProject/Application **전부 무편집**.

> **I-3(cloudflared `hosts` 한 줄 추가)는 하지 않았다** — 허용 경로 밖이고, **D-1 이 정해지기 전에는
> 더할 값 자체가 없다.**

---

## 3. 핵심 설계 — Mediness 를 베끼지 «않은» 곳

### 3-1. Ingress 한 장, 호스트 하나 (Mediness 는 호스트 셋)

Mediness 는 front·api·mcp 를 **다른 호스트**로 가른다. Strong Hajin 은 그럴 수 없다 —
SPEC-006 이 **같은 origin 하나**를 골랐고, 그 한 선택 덕분에 REST 상대경로 · `same-origin` 자격증명 ·
WS 주소 자동 조립 · 세션 쿠키 · CORS 부재가 **제품 코드 한 줄 없이** 성립한다. origin 을 가르면 그 전부가 깨진다.

렌더된 경로(실측):

```
/api/meetings   -> back:28080     ← 가장 긴 prefix 가 이긴다(WS 스트림)
/api            -> back:28080
/health         -> back:28080
/               -> front:80
```

**WS 에 별도 annotation 을 넣지 않았다** — ingress-nginx 는 `Upgrade`/`Connection` 을 기본 전달한다.
필요한 것은 **타임아웃**이고, Mediness api ingress 와 같은 값(`3600`)을 썼다. 없으면 스트림이 60초에 죽는다.

**`CORS_ORIGINS` 를 configmap 에 넣지 않았다**(렌더 확인: `CORS_ORIGINS present: False`).
origin 이 하나면 브라우저가 교차 출처 요청을 보내지 않으므로 **허용할 것이 없다** —
한 줄 넣어 두면 SPEC-006 이 일부러 닫은 문을 조용히 다시 연다.

### 3-2. 「렌더 성공 ≠ 제품 정상」을 차트가 말한다

`/health` 는 **프로파일 게이트 밖의 유일한 라우트**다. 그래서 **`/health` 200 인데 `/api/*` 가 전부
404** 인 상태가 가능하다 — probe 는 초록인데 아무것도 안 되는 상태. back.yaml 주석과 `NOTES.txt` 가
그 사실을 적고, **배포 확인에 실제 API 하나 + WS 핸드셰이크를 같이 보라**고 말한다.

### 3-3. 큰 파일은 PVC 가 아니라 hostPath

녹음·자료는 `/mnt/mac/strong-hajin/{recordings,materials}` 다(Mediness 가 `/mnt/mac/audio` 를 쓰는 것과
같은 이유 — `local-path` PVC 는 **lima-worker-1 에만** 잡히고 VM 재생성에 약하다).
`type: Directory` 라 **경로가 없으면 파드가 뜨지 않는다** — 녹음이 사라지는 빈 임시 디렉터리에
조용히 쌓이는 것보다 낫다. 그래서 back·worker 는 같은 노드에 핀된다.

### 3-4. `worker.kinds` 는 **기본이 빈 목록**이고, 그러면 worker 가 **0개** 렌더된다

제품에는 워커가 넷이다(conversation · material · meeting · report). **어느 것을 띄울지는 배포 결정**이라
여기서 추측하지 않았다. 추측하면 **조용히 안 뜨거나 조용히 뜬다** — 둘 다 나쁘다.
(prod 렌더에서 넷을 주입하면 10 오브젝트, 주입 안 하면 6 오브젝트다.)

### 3-5. 비밀값은 **이름만** 있다

차트에 비밀값 **0**. `strong-hajin-secret`(앱) · `postgres-secret`(DB 비밀번호)을 **참조만** 한다
(`secretKeyRef` · `secretRef`). 둘 다 레포 «밖»에서 사람이 만든다(설계서 C-2).
`DATABASE_URL` 은 configmap 이 아니라 **파드 env 에서 조립**한다 — 비밀번호가 ConfigMap 에 남지 않게.
평문 비밀값 검사: **0건**.

### 3-6. ⚠ `values-dev.yaml` 의 `profile: development` 는 **개발 전용 표면을 연다**

`values-dev.yaml` 은 `back.profile: development` 다. 이것은 로그 수준 같은 취향이 아니라
**인증 표면을 바꾸는 스위치**다. 제품 코드로 확인한 사실:

| 사실 | 근거 |
|---|---|
| `local_login_enabled` = **`profile is not PRODUCTION`** | `bootstrap/settings.py` — 즉 `development` 면 **이메일/비밀번호 로그인이 열린다** |
| `GET /api/auth/providers` 가 **demo 계정 목록과 demo 비밀번호를 응답 본문에 담는다** | `entrypoints/http.py` — `local_login_enabled` 일 때 `demo_accounts` · `demo_password` 를 실어 보낸다. **PRODUCTION 은 둘 다 돌려주지 않는다** |
| 세션 쿠키의 `Secure` 는 **PRODUCTION 에서만** 찍힌다 | 설계서 §3-2 |

**그래서 `strong-hajin-dev` 는 «작은 운영»이 아니라 «열린 개발 환경»이다.**
그 주소에 닿을 수 있는 사람은 **응답 본문에서 계정과 비밀번호를 그대로 읽어** 로그인할 수 있다.
D-1 이 정해져 그 호스트가 Cloudflare 터널로 **공개**되면, 이것은 인터넷에 열린 문이 된다.

**그래서 이번 작업이 한 것과 하지 않은 것**:

- `values-dev.yaml` 에 `profile: development` 를 **두되**, 파일 주석에 「`production` 으로 두면
  데스크톱 셸의 쿠키·라우트 동작을 그대로 재현할 수 있다. **의도적으로 고르라**」고 적었다
- **dev Application 은 만들지 않았다** — `argocd/applications/` 에 `strong-hajin-dev.yaml` 이 없다.
  AppProject destination 과 `values-dev.yaml` 이라는 **자리만** 있고, **띄우는 장치는 없다**
- `values-prod.yaml` · `values.yaml` 은 **`production` 그대로**이고 host·registry·tag 는
  **여전히 빈 placeholder** 다. 이번 회차는 **values 파일을 한 글자도 고치지 않았다**

> **D-6(dev 환경을 둘 것인가)이 «비용·복잡도» 판단만이 아닌 이유가 이것이다.**
> dev 를 두기로 한다면 **공개 여부·접근 제한**을 함께 정해야 한다 — 그 결정 없이 dev 호스트를
> 터널에 올리면 demo 계정이 공개된다. 이 워커는 그 결정을 대신하지 않았고,
> **dev 를 띄우는 파일을 만들지 않는 것**으로 기본값을 「없음」에 두었다.

---

---

## 4. Mediness 와의 격리 — 정적 확인

| 축 | Mediness | Strong Hajin | 확인 |
|---|---|---|---|
| namespace | `mediness-dev` · `mediness-prod` | `strong-hajin-prod`(+`-dev`) | Application 목록에서 겹침 없음 |
| AppProject | `mediness` | **`strong-hajin`**(신규) | destinations 에 mediness ns 없음 |
| chart | `charts/mediness` | `charts/strong-hajin`(신규 디렉터리) | — |
| datastores | 같은 차트 · `values-{dev,prod}.yaml` | 같은 차트 · **`values-strong-hajin.yaml`**(신규) | Mediness values **무편집** |
| 이름 충돌 | — | — | Argo 오브젝트 이름 중복 **0**(기존 `kakao-tracker`·`private-pypi` 쌍은 **원래 있던 것**) |
| 렌더물 오염 | — | — | prod 렌더에 `medisolveai.xyz` **0건**, `mediness` 는 **내 주석 한 줄뿐** |

> ⚠ **`project: mediness` 를 쓰면 안 된다** — 그 AppProject 의 destination 에 `strong-hajin-prod` 가
> 없어 sync 가 **거부된다**. 두 Application 모두 `project: strong-hajin` 이고, 파일에 그 이유를 적었다.

---

## 5. 검증 — 실제로 돌린 것 (helm v4.2.3)

### 5-1. `helm lint` — 4종 **통과**

| 대상 | 종료 | 비고 |
|---|---|---|
| `charts/strong-hajin`(values.yaml) | **0** | `missing required values` **경고 8건** |
| 〃 `-f values-prod.yaml` | **0** | 〃 |
| 〃 `-f values-dev.yaml` | **0** | 〃 |
| `charts/datastores -f values-strong-hajin.yaml` | **0** | 경고 없음 |

**helm v4 의 lint 는 `required` 미충족을 WARN 으로 센다** — 차트 구조는 유효하고,
비어 있는 세 값은 **경고로 드러난다.**

### 5-2. `helm template` — **주입 없이는 실패한다(의도)**

| 실행 | 종료 | 메시지 |
|---|---|---|
| prod, 주입 없음 | **1** | `host is not set — the operational host is undecided (D-1). … This chart does not invent a domain.` |
| dev, 주입 없음 | **1** | 〃 |

**이 실패를 임의값으로 통과시키지 않았다.** 값 파일에는 여전히 `host: ""` 다.

### 5-3. `helm template` — **명령줄 주입 시 정상 렌더**

렌더가 되는지 자체는 확인해야 하므로, **파일에 한 글자도 남기지 않고 명령줄로만** 주입했다.
쓴 값은 `strong-hajin.example.invalid` — **RFC 6761 예약 TLD 라 절대 해석되지 않는다.**
진짜 도메인으로 오인될 수 없는 값을 일부러 골랐다.

| 실행 | 종료 | 결과 |
|---|---|---|
| prod + 주입 + `worker.kinds={4개}` | **0** | **10 오브젝트** — ConfigMap · Service ×2 · Deployment ×6 · Ingress |
| dev + 주입(`worker.kinds` 빈 채) | **0** | **6 오브젝트** — worker 0개 |
| `charts/datastores -f values-strong-hajin.yaml` | **0** | Service ×2 · StatefulSet ×2 |

렌더물은 `yaml.safe_load_all` 로 **파싱까지 확인**했다(10 문서). 확인한 값:
`AX_PROFILE: production` · `PUBLIC_ORIGIN: https://strong-hajin.example.invalid` · 경로 넷(위 §3-1).

---

## 6. 하지 않은 것

| 금지 | 확인 |
|---|---|
| 커밋 · push · PR | **없음** — HEAD `46fdf88` 그대로, 전부 `??`(untracked) |
| 클러스터 적용 · GitOps sync | **없음** — `kubectl`·`helm install/upgrade` 한 번도 부르지 않았다. `lint`·`template` 은 **로컬 렌더**다 |
| 운영 도메인 발명 | **0** — 비워 두고 렌더를 **실패시켰다**. 검증 주입값은 `.invalid` |
| 비밀값 발명 | **0** — `secretRef`/`secretKeyRef` 이름만 |
| Mediness 파일 수정 | **0줄** — `git diff --stat` 출력 없음 |
| cloudflared `hosts` 추가(I-3) | **하지 않았다** — 허용 경로 밖 + D-1 미결이라 더할 값이 없다 |

**Argo `syncPolicy.automated` 를 일부러 주석 처리했다.** 한 번도 클러스터에서 돈 적 없는 차트에
`selfHeal` 을 켜면 **잘못된 렌더 하나가 루프**가 된다. 수동 sync 가 되는 것을 본 뒤 켜는 순서다.

---

## 7. 경로 두 건 — **코디에게 물어보고 진행했다**

허용 경로와 설계서가 두 군데서 어긋나 `orca orchestration ask` 로 확인했다(첫 호출은 Orca 런타임이
닫혀 실패, 재시도에서 응답 수신).

| # | 어긋남 | 코디 답 | 결과 |
|---|---|---|---|
| **A** | 구현 4번은 `charts/datastores/values-strong-hajin.yaml` 을 요구하는데 허용 경로에는 `charts/datastores/**` 가 없다 | **허용** — 설계서 I-2b 와 Argo `valueFiles` 가 그 경로를 요구하므로 **그 신규 파일만** | 추가함 |
| **B** | 파일명: 허용 경로 `strong-hajin.yaml` vs 레포 관례 `*-appproject.yaml` | **허용 경로 유지** | `argocd/projects/strong-hajin.yaml` |

**설계서와 파일명이 다른 두 곳을 기록해 둔다**(코디 지시):

| 설계서 | 실제 | 이유 |
|---|---|---|
| `argocd/projects/strong-hajin-appproject.yaml` | **`strong-hajin.yaml`** | 허용 경로 |
| `argocd/applications/datastores-strong-hajin.yaml` | **`strong-hajin-datastores.yaml`** | 허용 glob `strong-hajin-*.yaml` |

같은 오브젝트이고 파일 이름만 다르다. 레포 관례(`*-appproject.yaml`)와도 다르므로,
**나중에 관례로 맞추려면 rename 한 번**이면 된다(Argo 는 디렉터리를 통째로 읽으므로 참조가 깨지지 않는다).

---

## 8. 미결 — 이번 작업이 풀지 못한 것

| # | 항목 | 이 차트에서 어떻게 드러나나 |
|---|---|---|
| **D-1** | **운영 호스트** `<STRONG_HAJIN_HOST>` | `host: ""` → **`helm template` 이 실패한다.** 발명하지 않았다 |
| **D-2** | **레지스트리 namespace**(제품 레포가 `kknaks/Strong_hajin` 이라 org 소유가 다르다) | `image.registry: ""` → **렌더 실패** |
| **D-3** | 회사 org 레포에 개인 제품 구성을 올려도 되는가 | **push 시점의 문제다** — 이번엔 커밋조차 하지 않았다 |
| **D-4** | **PRODUCTION 로그인 수단** | 차트가 `AX_PROFILE=production` 을 켜지만 **아무도 로그인할 수 없다.** `NOTES.txt` 가 그렇게 적는다. 인프라가 풀 수 있는 문제가 아니다 |
| **D-6** | **dev 환경을 둘 것인가** | `values-dev.yaml` 과 AppProject destination 에 `strong-hajin-dev` **자리만** 만들어 뒀다. dev Application 은 **만들지 않았다** — 둘지 자체가 미결이고, **`profile: development` 가 demo 계정·비밀번호를 응답에 싣는 개발 전용 표면을 열기 때문**이다(§3-6). 둔다면 **공개 여부·접근 제한을 함께** 정해야 한다 |
| **I-4** | arm64 이미지 | `image.tag: ""` → **렌더 실패**. 이 차트는 굽지 않는다 |
| **I-3** | cloudflared `hosts` 한 줄 | **미수행** — D-1 미결 + 허용 경로 밖 |
| **D-5** | 백업 주기·보관 | **미결** — 배포를 막지는 않는다 |

**그래서 지금 이 레포에서 `helm template` 은 실패하는 것이 옳은 상태다.**

---

## 9. 다음 워커가 할 일 (순서)

> ⛔ **구분선 «아래»는 전부 클러스터 쓰기다 — AppProject 적용도 그중 하나다.**
> 이 워커는 그 아래를 하나도 하지 않았고, **사용자·코디의 명시적 승인 전에는 다음 워커도 하지
> 않는다.** 구분선 위의 1)·2) 만 승인 없이 진행할 수 있다 — 다만 **2) 안에도 승인이 필요한
> 절반이 있다(레지스트리 push). 아래 2) 를 그대로 읽을 것.**

```
1) D-1 · D-2 결정 → values-prod.yaml 의 host/registry 를 채우거나
                     Application 의 helm.parameters 주석을 푼다
2) I-4 arm64 이미지 — **빌드와 push 는 다른 일이다. 갈라서 읽는다.**
   2a) 로컬 빌드·검증 (승인 없이 가능)
       `docker build --platform linux/arm64 …` → 로컬에서 실행·헬스체크까지.
       이 기기 밖으로 아무것도 나가지 않는다.
   2b) 레지스트리 push (**승인 필요 · 외부 쓰기**)
       ⚠ push 는 **클러스터가 아니라 외부 레지스트리에 쓰는 일**이고, 되돌리기 어렵다
         (태그를 지워도 당긴 사람에게는 남는다).
       ⚠ **D-2 가 먼저다** — 어느 레지스트리 namespace 에 올릴지 정해지지 않았다.
         제품 레포는 `kknaks/Strong_hajin` 이라 `ghcr.io/medisolveaidev` 와 **org 소유가 다르다.**
       ⚠ **D-3 가 먼저다** — 회사 org 이름으로 이미지를 «발행»해도 되는지가 미결이다.
         이것은 기술 문제가 아니라 **소유·권한 문제**다.
       → **둘 다 풀리기 전에는 2a) 까지만 한다.** image.tag 주입은 push 가 끝난 뒤의 일이다.

════════ 승인 게이트 · 여기서부터 «전부» 클러스터를 건드린다 ════════
        (사용자/코디 승인 후, 별도 지시로만 실행한다)

3) argocd/projects/strong-hajin.yaml (AppProject) 를 **먼저** 적용한다
   ⚠ 클러스터 쓰기다 — `kubectl apply`. 승인 대상이다.
   ⚠ 이것이 없으면 두 Application 은 «project: strong-hajin 이 없다»로 거부된다.
     AppProject 가 destination(strong-hajin-prod) 을 여는 문이고, 그 문이 없으면
     Application 은 sync 를 시작조차 못 한다. **클러스터 작업들 «사이»의 선행 조건**이지
     승인보다 앞서는 예외가 아니다.
4) postgres-secret · strong-hajin-secret 을 strong-hajin-prod 에 생성(레포 밖, C-2)
5) /mnt/mac/strong-hajin/{recordings,materials} 를 lima-worker-1 에 생성
   (없으면 hostPath type: Directory 때문에 파드가 뜨지 않는다 — 의도된 동작)
6) strong-hajin-datastores 를 먼저 수동 sync(앱보다 DB 가 먼저 서야 한다)
7) I-3 cloudflared hosts 한 줄 + DNS CNAME
8) strong-hajin-prod 수동 sync → 실제 API 하나 + WS 핸드셰이크 확인
   (→ /health 만으로 판단하지 않는다)
9) 그 뒤에 syncPolicy.automated 주석 해제
```

**3) 을 빼먹으면 1)~2) 를 아무리 잘해도 sync 가 서지 않는다** — 그리고 그때 나오는 오류는
「호스트가 틀렸다」가 아니라 「project 를 찾을 수 없다」라, 엉뚱한 곳을 보게 만든다.
**5) 를 4) 보다 먼저 하면** 파드가 CrashLoop 이 아니라 **Pending** 에서 멈춘다 — 원인을 찾기 더 어렵다.
**D-4 가 풀리기 전에는 8) 의 «실제 API» 가 인증을 통과하지 못한다.**
**2b) 는 구분선 위에 있지만 승인 대상이다** — 구분선이 가르는 것은 「클러스터냐 아니냐」이고,
2b) 는 **클러스터 밖이지만 이 기기 밖**이다. 승인이 필요한 이유가 구분선과 다르므로 단계 안에 적었다.

### 9-1. 승인 경계 — **이 워커가 넘지 않은 선**

| | 한 것 | 하지 않은 것 |
|---|---|---|
| 레포 | 신규 파일 14개 작성 | **커밋 · push · PR** |
| helm | `lint` · `template`(로컬 렌더) | **`install` · `upgrade`** |
| **레지스트리** | **아무것도** | **이미지 빌드 · `docker push`**(§9 2b — D-2·D-3 선행) |
| 클러스터 | **아무것도** | `kubectl apply` · AppProject 적용 · Argo sync |

**`helm lint`·`helm template` 은 클러스터에 접속하지 않는다** — 로컬에서 문자열을 만들어 보는 일이다.
그래서 이 워커의 검증은 **클러스터 상태에 대해 아무것도 증명하지 않는다.**
위 **3)~9)** 는 **사용자/코디 승인 후** 별도 지시로 실행될 일이다 — **AppProject 적용(3)도 그 안**이다.
표의 「하지 않은 것」에 `AppProject 적용` 이 들어 있는 것과 §9 의 구분선 위치가 **같은 말을 한다.**
