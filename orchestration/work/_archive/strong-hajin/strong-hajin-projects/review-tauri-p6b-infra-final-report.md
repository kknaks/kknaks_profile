# WORK-006 Phase 6b 인프라 — 최종 독립 검수

- **인프라 레포**: `/Users/kknaks/git/harness_works/k8s_infra_mac` · HEAD **`46fdf88`**(변동 없음)
- **검수 대상**: `charts/strong-hajin/templates/ingress.yaml` · `tauri-p6b-infra-report.md`(286줄) ·
  `tauri-p6b-infra-fix2-report.md` · (`tauri-p6b-infra-fix-report.md` → **존재하지 않음**, §5 참고)
- **read-only 검수.** `kubectl` · Argo sync · `helm install/upgrade` · push · Release **0회.**
  돌린 것은 **`helm lint`·`helm template`**(로컬 렌더)과 파일 읽기뿐이다.
- **이 검수 보고서 한 파일만 작성.**

---

## 0. 종합 판정 — **FAIL 0 · WARN 2(둘 다 낮음) · 나머지 PASS**

**직전 회차에 내가 올린 WARN(승인 게이트가 AppProject 아래에 그어진 것)이 닫혔고,
고친 방식이 지적보다 낫다.** 구분선만 옮긴 것이 아니라 —

- **번호를 `0)`→없애고 `1)~9)` 로 연속**시켰다. 「`0)` 이라는 번호 자체가 «본 순서 밖의 예비
  단계»로 읽혔다」는 진단이 정확하다.
- **머리말을 «번호» 기준에서 «구분선» 기준으로** 다시 썼다 — 「번호로 경계를 말하면 번호가
  바뀔 때마다 문장이 낡는다」.
- **AppProject 단계에 「클러스터 쓰기다 — `kubectl apply`. 승인 대상이다」**를 박고,
  「**클러스터 작업들 «사이»의 선행 조건**이지 승인보다 앞서는 예외가 아니다」로 성격을 갈랐다.
- **번호 참조 셋(3/5/8)도 함께 옮겨** 본문이 조용히 어긋나지 않게 했다.
- **자기가 왜 틀렸는지 적었다** — 「「먼저」를 **순서의 맨 앞**으로 옮기는 것으로 읽었는데,
  그 뜻은 **「클러스터 작업들 «사이»에서 첫 번째」**였다」.

**helm 수치와 레포 상태가 그대로다** — lint 4종 exit 0(WARN 8) · 주입 없이는 실패 ·
주입 시 prod 10 / dev 6 / datastores 4 오브젝트 · `git diff --stat` **0줄** · HEAD `46fdf88`.
**이번 회차는 인프라 레포를 한 글자도 건드리지 않았다**(01:08 이후 변경 0건).

WARN 2 건은 **runbook `2)` 의 경계 문구**와 **존재하지 않는 대상 파일**이다.

---

## 1. 판정표

| # | 발주 재현 항목 | 판정 |
|---|---|---|
| 1 | helm lint 4종 | **PASS** (exit 0 ×4 · WARN 8) |
| 2 | placeholder 주입 template | **PASS** (주입 없이 실패 · 주입 시 10/6/4) |
| 3 | runbook 의 AppProject 승인 경계 | **PASS** (게이트 아래로 이동 · 번호 연속) |
| 4 | 네 경로 주석 | **PASS** (`FOUR paths` · 렌더와 일치) |
| 5 | dev `development` · D-6 | **PASS** (§3-6 유지 · D-6 칸에도 반영) |
| 6 | 기존 Mediness 무변경 | **PASS** (tracked diff 0줄) |

---

## 2. FAIL

**없다.**

---

## 3. 재현한 수치

### 3-1. `helm lint` — 4종 **exit 0**

| 대상 | exit |
|---|---|
| `charts/strong-hajin` (values.yaml) | **0** |
| 〃 `-f values-prod.yaml` | **0** |
| 〃 `-f values-dev.yaml` | **0** |
| `charts/datastores -f values-strong-hajin.yaml` | **0** |

`missing required values` **WARN 8건** — helm v4 가 `required` 미충족을 ERROR 가 아니라 WARN 으로
센다는 설명도 그대로 성립한다.

### 3-2. `helm template` — 주입 없이는 **실패**, 주입하면 **정상**

| 실행 | exit | 결과 |
|---|---|---|
| prod, 주입 없음 | **1** | `ingress.yaml:37:15 … host is not set — the operational host is undecided (D-1)` |
| dev, 주입 없음 | **1** | 〃 |
| prod + placeholder 주입 + `worker.kinds={4}` | **0** | **10 오브젝트** |
| dev + placeholder 주입 | **0** | **6 오브젝트**(worker 0) |
| `charts/datastores -f values-strong-hajin.yaml` | **0** | **4 오브젝트**(Service×2 · StatefulSet×2) |

- 주입값은 `*.example.invalid`(예약 TLD) — **파일에 한 글자도 남기지 않고 명령줄로만**.
- 렌더 오염: `medisolveai.xyz` **0건**.
- **값 파일은 여전히 `host/registry/tag: ""`** 다.

### 3-3. 네 경로 — 주석과 렌더가 일치

```
# ONE Ingress, ONE host, FOUR paths:
#   /api/meetings  -> back   (live transcript WebSocket)
#   /api           -> back   (everything else under the API)
#   /health        -> back   (the only route outside the profile gate)
#   /              -> front  (the SPA)
```

렌더 실측: `/api/meetings` · `/api` · `/health` · `/` — **네 줄, 같은 순서.**
파일 내 `three` **0건**.

---

## 4. runbook 승인 경계 (PASS)

**현재 §9**:

```
1) D-1 · D-2 결정 …
2) I-4 arm64 이미지 빌드·푸시 …

════════ 승인 게이트 · 여기서부터 «전부» 클러스터를 건드린다 ════════
        (사용자/코디 승인 후, 별도 지시로만 실행한다)

3) argocd/projects/strong-hajin.yaml (AppProject) 를 **먼저** 적용한다
   ⚠ 클러스터 쓰기다 — `kubectl apply`. 승인 대상이다.
   ⚠ … **클러스터 작업들 «사이»의 선행 조건**이지 승인보다 앞서는 예외가 아니다.
4)~9) …
```

| 검수 확인 | 결과 |
|---|---|
| 구분선이 AppProject **위** | ✅ |
| `0)` 잔존 | **0건** · 번호 `1)~9)` **연속·중복 없음** |
| 머리말 기준 | 「**구분선 «아래»는 전부 클러스터 쓰기다 — AppProject 적용도 그중 하나다**」 — 번호가 아니라 구분선으로 말한다 ✅ |
| §9-1 표 ↔ 꼬리말 | 표「하지 않은 것 · 클러스터: `kubectl apply` · **AppProject 적용** · Argo sync」 ↔ 꼬리말「**3)~9)** 는 승인 후 — **AppProject 적용(3)도 그 안**」 — **같은 말** ✅ |
| 번호 참조 | 본문 셋이 **3) · 5)/4) · 8)** 로 함께 이동 ✅ |
| §9 밖 보존 | §1~§8 **전부 존재**(`## 1`~`## 8` 확인) · §3-6 · D-6 칸 **살아 있다** |

→ **직전 WARN 이 닫혔고, 「같은 문서가 두 말을 하던」 상태가 해소됐다.**

---

## 5. dev · D-6 (PASS)

| 확인 | 결과 |
|---|---|
| §3-6 | **유지** — `local_login_enabled` = `profile is not PRODUCTION` · `demo_accounts`·`demo_password` 응답 본문 적재 · 「인터넷에 열린 문이 된다」 |
| **D-6 칸(§8)** | **보강됨** — 「`profile: development` 가 **demo 계정·비밀번호를 응답에 싣는 개발 전용 표면을 열기 때문**이다(§3-6). 둔다면 **공개 여부·접근 제한을 함께** 정해야 한다」 |
| dev Application | `argocd/applications/` 에 **`strong-hajin-prod.yaml` · `strong-hajin-datastores.yaml` 둘뿐** — dev 없음 ✅ |
| values 파일 | `values-dev.yaml` `profile: development` · `values-prod.yaml` `profile: production` — **이번 회차 무변경** |

→ **위험 서술이 §3-6 에만 있지 않고 미결 표(§8)에도 들어가** 결정하는 사람이 놓치기 어렵다.

---

## 6. 무변경 (PASS)

| 대상 | 확인 |
|---|---|
| **인프라 레포** | `git diff --stat` **0줄** · `git status` **신규 5항목(untracked)** · HEAD **`46fdf88`** |
| **이번(fix2) 회차** | `charts/`·`argocd/` 에 **01:08 이후 변경 0건** — 문서만 고쳤다 |
| Mediness · cloudflared · datastores 기존 values · argocd 기존 | `git diff --stat` **0줄**(대상 지정 확인) |
| 클러스터 · push · Release · 태그 | **0** — 검수도 `lint`/`template` 만 |
| 보고서 | 280 → **286줄**(+6) · §9·§9-1 만 변경(§1~§8 보존 확인) |

---

## 7. WARN (2건 · 둘 다 낮음)

| # | 내용 | 근거 | 수정 방향 |
|---|---|---|---|
| **W-1** | **`2)` 가 「승인 없이 진행할 수 있는」 쪽에 있는데, 그것은 «외부 레지스트리에 이미지를 올리는» 일이다.** 머리말이 「구분선 위의 **1)·2) 만 승인 없이 진행할 수 있는 레포/이미지 작업**」이라 적는데, `2)` 는 `arm64 이미지 **빌드·푸시**` 다 — 클러스터는 아니어도 **바깥으로 나가는 발행**이고, 올리는 곳(`image.registry`)의 소유는 **D-2·D-3 이 걸린 자리**다. 게다가 `1)` 은 「D-1·D-2 **결정**」이라 **워커가 «진행»할 수 있는 일이 아니라 승인 그 자체**다 — 「승인 없이 진행」이라는 말이 두 단계 모두에 느슨하게 걸린다 | §9 머리말 · `2)` · D-2/D-3(§8) | ① `2)` 에 「**D-2 결정 후 · 외부 레지스트리 푸시**」를 붙이거나 ② 구분선 문구를 「여기서부터 **클러스터**」가 아니라 「여기서부터 **되돌리기 어려운 바깥 작업**」으로 넓힌다. **판단은 코디** — 이 워커가 아무것도 푸시하지 않았으므로 **현재 위반은 없다** |
| **W-2** | **이번 발주가 지목한 `tauri-p6b-infra-fix-report.md` 가 존재하지 않는다.** 직전 WARN 보정 회차는 **별도 fix 보고서를 만들지 않고 `tauri-p6b-infra-report.md` 본문에 §3-6·§9·§9-1 을 직접** 넣었다. fix2 §5 가 그 사실과 **만들지 않은 이유**(「없는 파일을 새로 만들어 §9 사본을 두면 runbook 이 두 곳에 생겨 다음 워커가 어느 쪽을 볼지 모르게 된다」)를 적었고, **검수도 그 판단에 동의한다** — 단일 출처가 맞다. 다만 **발주 목록이 없는 파일을 계속 가리키면** 다음 회차에서도 같은 혼선이 난다 | 작업 디렉터리 실측: `tauri-p6b-infra-report.md` · `…-fix2-report.md` 둘뿐(구현 측) | 다음 발주의 대상 목록에서 그 파일명을 빼거나, 보정 회차가 **항상 별도 문서를 남기는** 규칙으로 통일 |

> 둘 다 **차트·Argo·helm 동작과 무관**하다. W-1 은 다음 워커가 읽을 문구, W-2 는 발주 목록 정리다.

---

## 8. 차단·미결 (유지)

| # | 항목 | 이 차트에서 드러나는 방식 |
|---|---|---|
| **D-1** 운영 호스트 · **D-2** 레지스트리 · **I-4** 태그 | `""` → **template 실패**(재현) |
| **D-3** 회사 org 레포 업로드 가부 | **커밋조차 하지 않았다** |
| **D-4** PRODUCTION 로그인 수단 | `NOTES.txt` 「아무도 로그인할 수 없다」 |
| **D-6** dev 환경 | 자리만 · dev Application 없음 · **공개 위험이 결정 요소로 기록됨** |
| **I-3** cloudflared hosts · **D-5** 백업 | 미수행 · 미결 |
| 클러스터 상태 | **아무것도 증명되지 않았다**(§9-1) |

---

## 9. 한 줄 정리

**승인 게이트가 AppProject 위로 올라가면서 「같은 문서가 두 말을 하던」 상태가 끝났고,
번호를 `1)~9)` 로 연속시켜 «예비 단계»로 읽힐 여지까지 없앴다** — 구현이 자기 오독의 원인까지
적었다. helm 4종 lint · 주입 전후 template · 네 경로 · Mediness 무변경을 **전부 재현**했고
인프라 레포는 **01:08 이후 한 글자도 바뀌지 않았다**. 남은 것은 **`2)`(이미지 푸시)의 경계
문구(W-1)** 와 **발주 목록의 없는 파일명(W-2)** 뿐이며, **Phase 6b 인프라에 기능적 지적은 없다.**
