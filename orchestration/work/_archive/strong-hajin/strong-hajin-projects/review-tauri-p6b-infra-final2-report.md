# WORK-006 Phase 6b 인프라 — 최종2 독립 검수

- **인프라 레포**: `/Users/kknaks/git/harness_works/k8s_infra_mac` · HEAD **`46fdf88`**(변동 없음)
- **검수 대상**: `charts/strong-hajin/**` · `charts/datastores/values-strong-hajin.yaml` · `argocd/` 신규 셋 ·
  `tauri-p6b-infra-report.md`(301줄) · `…-fix2-report.md`(156줄) · `…-fix3-report.md`
- **read-only 검수.** 클러스터 · `kubectl` · Argo sync · `helm install/upgrade` · push · Release **0회.**
- **이 검수 보고서 한 파일만 작성.**

---

## 0. 종합 판정 — **FAIL 0 · WARN 1(낮음) · 나머지 PASS**

**직전 회차에 내가 올린 WARN 둘이 모두 닫혔고, 첫째는 지적보다 정밀하다.**

- **W-1(이미지 push 경계)**: `2)` 를 **2a(로컬 빌드) / 2b(레지스트리 push)** 로 갈랐다.
  2b 에 **「승인 필요 · 외부 쓰기」**를 박고 **D-2 와 D-3 를 둘 다 선행 조건**으로 적었으며,
  **「둘 다 풀리기 전에는 2a) 까지만 한다」**로 금지를 명시했다.
  되돌릴 수 없는 이유(「태그를 지워도 **이미 당긴 사람에게는 남는다**」)까지 적었다.
- **2b 를 구분선 아래로 «내리지 않은» 판단도 옳다** — 「구분선이 가르는 것은 «클러스터냐»이고
  push 는 클러스터 쓰기가 아니다. **거짓 분류로 줄을 맞추기보다 단계 안에 승인 조건을 박는 쪽**」.
  분류를 억지로 맞추지 않고 **경계의 근거가 다르다는 사실 자체를 적었다.**
- **W-2(없는 파일)**: fix2 §5 가 「산출물 — **단일 출처**」로 다시 쓰였고,
  fix3 §3-2 는 **지시 중 하지 못한 것을 정직하게 적었다** — 그 정리 대상이 **검수 측 문서**라
  허용 경로 밖이므로 **건드리지 않았다**. 「허용 파일 밖을 조용히 고쳐 «제거 완료»라고 보고할
  수도 있었지만 그것은 **권한 경계를 넘는 일**」이라는 판단이 **정확하다.**

**helm 수치와 레포 상태가 그대로다** — lint 4종 exit 0(WARN 8) · 주입 없이 실패 ·
주입 시 prod 10 / dev 6 / datastores 4 · `git diff --stat` **0줄** · **01:13 이후 차트·Argo 변경 0건**
(이번 회차는 **문서만** 고쳤다).

WARN 1 건은 **「단일 출처」 절 자신이 한 문서 낡은 것**이다.

---

## 1. 판정표

| # | 발주 확인 항목 | 판정 |
|---|---|---|
| 1 | §9 arm64 image push 가 **D-2/D-3 승인 전 금지**로 명시 | **PASS** |
| 2 | 실제 존재하는 보고서 파일만 목록에 | **PASS**(fix3 §3-1) · fix2 §5 는 **WARN**(W-1) |
| 3 | Helm lint / template 재현 | **PASS** |
| 4 | 기존 Mediness 무변경 | **PASS** (tracked diff 0줄) |
| 5 | placeholder 유지 | **PASS** (`host`/`registry`/`tag` 전부 `""`) |
| 6 | 클러스터 미적용 | **PASS** (untracked 5항목 · HEAD 불변) |

---

## 2. FAIL

**없다.**

---

## 3. §9 — push 금지 명시 (PASS)

**현재 `2)`**:

```
2) I-4 arm64 이미지 — **빌드와 push 는 다른 일이다. 갈라서 읽는다.**
   2a) 로컬 빌드·검증 (승인 없이 가능)
       … 이 기기 밖으로 아무것도 나가지 않는다.
   2b) 레지스트리 push (**승인 필요 · 외부 쓰기**)
       ⚠ push 는 **클러스터가 아니라 외부 레지스트리에 쓰는 일**이고, 되돌리기 어렵다
         (태그를 지워도 당긴 사람에게는 남는다).
       ⚠ **D-2 가 먼저다** — 어느 레지스트리 namespace 에 올릴지 정해지지 않았다. …
       ⚠ **D-3 가 먼저다** — 회사 org 이름으로 이미지를 «발행»해도 되는지가 미결이다.
         이것은 기술 문제가 아니라 **소유·권한 문제**다.
       → **둘 다 풀리기 전에는 2a) 까지만 한다.** image.tag 주입은 push 가 끝난 뒤의 일이다.
```

| 검수 확인 | 결과 |
|---|---|
| **D-2 · D-3 를 둘 다** 선행으로 적는가 | ✅ 각각 별도 ⚠ 줄 |
| **승인 전 금지**가 명시되는가 | ✅ 「**둘 다 풀리기 전에는 2a) 까지만 한다**」 |
| 되돌릴 수 없음의 근거 | ✅ 「태그를 지워도 당긴 사람에게는 남는다」 |
| 머리말 정합 | ✅ 「구분선 위의 1)·2) 만 승인 없이 — 다만 **2) 안에도 승인이 필요한 절반이 있다(레지스트리 push)**」 |
| **§9-1 표에 레지스트리 행** | ✅ 「**레지스트리** \| 한 것 **아무것도** \| 하지 않은 것 **이미지 빌드 · `docker push`**(§9 2b — D-2·D-3 선행)」 |
| 단계 번호 연속 | ✅ `1) 2)(2a·2b) 3)~9)` · `0)` **0건** |

- **표에 행을 더한 이유까지 적었다** — 「표에 행이 없으면 **«안 한 일»이 아니라 «생각해 보지 않은
  일»로 읽힌다**」. 승인 경계 문서가 갖춰야 할 성질을 정확히 짚었다.
- **D-3 를 「기술 문제가 아니라 소유·권한 문제」로 규정**한 것도 옳다 — 워커가 기술적으로
  가능하다고 진행할 수 있는 종류가 아님을 못박는다.

---

## 4. 재현한 수치 (PASS)

| 실행 | **결과** |
|---|---|
| `helm lint` values.yaml / prod / dev / datastores(strong-hajin) | **exit 0 · 0 · 0 · 0** · `missing required values` **WARN 8건** |
| `helm template` prod, **주입 없음** | **exit 1** — `ingress.yaml:37:15 … host is not set … (D-1)` |
| `helm template` prod + placeholder + `worker.kinds={4}` | **exit 0 · 10 오브젝트** |
| `helm template` dev + placeholder | **exit 0 · 6 오브젝트**(worker 0) |
| `helm template` datastores `-f values-strong-hajin.yaml` | **exit 0 · 4 오브젝트** |
| 렌더 오염 | `medisolveai.xyz` **0건** |
| placeholder 유지 | `values.yaml` · `values-prod.yaml` 모두 `host: ""` · `registry: ""` · `tag: ""` |

주입은 **명령줄로만**(`*.example.invalid` 예약 TLD) — 파일에 한 글자도 쓰지 않았다.

---

## 5. 무변경 (PASS)

| 대상 | 확인 |
|---|---|
| **인프라 레포** | `git diff --stat` **0줄** · `status` **신규 5항목(untracked)** · HEAD **`46fdf88`** |
| **01:13 이후 `charts/`·`argocd/`** | **변경 0건** — fix3 회차는 **문서만** 고쳤다 |
| Mediness · cloudflared · datastores 기존 values · argocd 기존 | **무편집** |
| 클러스터 · push · Release · 태그 | **0** — 검수도 `lint`/`template` 만 |
| 문서 줄 수 | infra-report **286 → 301**(+15) · fix2 **144 → 156**(+12) — fix3 §4 기록과 일치 |

---

## 6. 산출물 목록 — **이 검수가 정리한다**

fix3 §3-2 가 「검수 측 문서는 허용 경로 밖이라 건드리지 않았다. **거기 남은 언급은 검수 측이
정리할 일**」이라고 넘겼다. **맞는 판단이므로 여기서 정리한다.**

**현재 이 작업 디렉터리에 실재하는 Phase 6b 인프라 문서 — 전부:**

| 구분 | 문서 |
|---|---|
| **구현 측** | `tauri-p6b-infra-report.md` · `tauri-p6b-infra-fix2-report.md` · `tauri-p6b-infra-fix3-report.md` |
| **검수 측** | `review-tauri-p6b-infra-report.md` · `review-tauri-p6b-infra-fix-report.md` · `review-tauri-p6b-infra-final-report.md` · **이 문서** |

- **`tauri-p6b-infra-fix-report.md` 는 존재하지 않는다**(만들어진 적 없음).
- **`tauri-p6b-infra-final-report.md` 도 존재하지 않는다** — 이번 발주가 「final report」로
  가리킨 것은 검수 측 `review-tauri-p6b-infra-final-report.md` 로 보인다.
- 내 이전 문서 `review-tauri-p6b-infra-final-report.md` 의 머리말·W-2 에 남은
  `tauri-p6b-infra-fix-report.md` 언급은 **이 문서로 대체한다** — 위 표가 정본이다.
- **runbook 의 유일한 자리는 `tauri-p6b-infra-report.md` §9** 다(사본 없음 — 확인).

---

## 7. WARN (1건 · 낮음)

### W-1 — **「단일 출처」 절이 자기 자신을 한 문서 낡게 적는다**

**좌표**: `tauri-p6b-infra-fix2-report.md` §5

```
## 5. 산출물 — **단일 출처**
Phase 6b 인프라 문서는 **이 둘뿐**이다:
  tauri-p6b-infra-report.md / tauri-p6b-infra-fix2-report.md
```

- **fix3 가 존재하므로 「둘뿐」이 아니라 셋이다.** fix3 는 **같은 회차에 fix2 §5 를 고치면서**
  자기 자신을 그 목록에 넣지 않았다(fix3 §3-1 의 표에는 셋이 다 있다).
- **아이러니가 요점이다** — 「목록이 실제와 어긋나면 다음 워커가 헤맨다」를 말하는 절이
  **바로 그 문제를 하나 갖고 있다.** fix2 만 열어 본 사람은 fix3 의 존재를 모른다.
- **완화 요인**: fix3 §3-1 이 셋을 정확히 싣고 있고, 본 검수 §6 이 정본 목록을 고정한다.
  **runbook 사본 문제와 달리 실행에 영향은 없다.**

**수정 방향**: fix2 §5 의 「이 둘뿐」 → **「셋」**(+ `tauri-p6b-infra-fix3-report.md` 행),
또는 「최신 목록은 fix3 §3-1 을 본다」 한 줄.

> **FAIL 이 아닌 이유**: 정확한 목록이 fix3 와 이 검수 문서에 있고, 차트·Argo·helm 동작과 무관하다.

---

## 8. 차단·미결 (유지)

| # | 항목 | 상태 |
|---|---|---|
| **D-1** 운영 호스트 | 미정 — `host: ""` → template 실패(재현) |
| **D-2** 레지스트리 namespace | 미정 — **이제 §9 2b 의 선행 조건으로 명시** |
| **D-3** 회사 org 발행 승인 | 미결 — 〃 · **소유·권한 문제**로 규정됨 |
| **D-4** PRODUCTION 로그인 수단 | 미결 — 라우트가 열려도 아무도 로그인할 수 없다 |
| **D-6** dev 환경 | 미결 — `profile: development` 가 demo 계정·비밀번호를 응답에 싣는다 · dev Application **없음** |
| **I-3** cloudflared · **I-4** 이미지 · **D-5** 백업 | 미수행 · 미결 |
| 클러스터 상태 | **아무것도 증명되지 않았다**(§9-1) |

---

## 9. 한 줄 정리

**push 를 「클러스터 밖이지만 이 기기 밖」으로 정확히 갈라 2a/2b 로 나누고, D-2·D-3 둘 다를
선행으로 못박아 「둘 다 풀리기 전에는 2a 까지만」으로 금지를 명시했다** — 분류를 억지로 맞추지
않고 경계의 근거가 다르다는 사실 자체를 적은 판단이 좋다. 허용 경로 밖 문서를 고치지 않고
**정직하게 남긴 것**도 이 작업 내내 지킨 규칙과 같다. helm 4종 · 주입 전후 · Mediness 무변경 ·
placeholder · 클러스터 미적용을 **전부 재현**했고, 남은 것은 **fix2 §5 의 「둘뿐」 한 낱말(W-1)** 뿐이다.
