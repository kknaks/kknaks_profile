# WORK-006 Phase 8 — 운영 origin 최종 빌드 관문(preflight)

- **작성**: 2026-09-22 **23:59 KST**
- **코드 워크트리**: `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-projects` · HEAD `a1f6791`(변동 없음)
- **결과**: 관문 신설. **현재 환경에서 7건을 막고 exit 1** — 이것이 **의도한 동작**이다
- **하지 않은 것**: 빌드 · 설치 · Release · 태그 · push · **설정 파일 수정 0**

---

## 1. 한 줄 결론

운영 origin 이 아직 없으므로 **「채워라」가 아니라 「굽지 말라」를 만들었다.**
`make shell-final-preflight` 는 지금 **7건을 들고 붉게 멈춘다** — 입력 없음 · `shell.config` 미정 ·
capability 자리표시 · **미결 넷**(D-4 · 운영 서버 실재 · M-1 · M-5). **자리표시를 최종판으로 굽는 길이 막혔다.**

---

## 2. 변경 파일 — 셋뿐이다

| 파일 | 변경 |
|---|---|
| `frontend/scripts/verify-final-build.mjs` | **신규**(396줄) — 관문 여섯 · manifest 형식 |
| `Makefile` | `shell-final-preflight` 타깃 + `.PHONY` **한 줄씩** |
| `tauri-p8-preflight-report.md` | **신규** — 이 문서 |

**건드리지 않은 것**(확인: `git diff --stat frontend/src-tauri/` **출력 0줄**):
`shell.config.json`(여전히 `operationalOrigin: null`) · `capabilities/product-shell.json`
(여전히 `https://operational-origin-not-yet-decided.invalid/*`) · `tauri.conf.json` · `Cargo.toml` ·
`src-tauri/src/**` · 제품 프론트 · backend · 인프라 레포.

---

## 3. 왜 Phase 7 관문으로는 부족한가 — **범위가 다르다**

| | `make shell-verify`(P7) | `make shell-final-preflight`(P8) |
|---|---|---|
| 묻는 것 | **구성이 일관한가** | **이 자리표시가 그대로 구워지고 있지 않은가** |
| 자리표시 origin | **초록**(일관하기만 하면 된다) | **붉다** |
| D-4 · 서버 실재 | 보지 않는다 | **막는다** |

**Phase 7 이 느슨한 것이 아니다** — 자리표시로도 「구성이 맞는가」를 물을 수 있어야 개발 중에 쓸 수 있다.
최종판을 굽는 **순간에만** 질문이 달라지고, 그 질문을 받는 파일을 따로 두었다.
회귀 확인: `make shell-verify` 는 **바뀌지 않았다**(`문제 0건 · 구성 미비 1건 · 호스트 한계 1건`, exit 0).

---

## 4. 관문 여섯

| # | 재는 것 | 막는 것 |
|---|---|---|
| **G1** | 입력 origin 형식(`SHELL_OPERATING_ORIGIN` 또는 `--origin`) | `.invalid` · 와일드카드 · 경로/질의 · http · loopback·IP · 빈 값 · **입력 없음** |
| **G2** | `shell.config.json` · `operationalOrigin` 실재 | `null`(미정)인 채 굽는 것 |
| **G3** | capability `remote.urls` 가 **`<origin>/*` 하나** | 자리표시 · `://*.` 서브도메인 · 목록 팽창 · `local!==false` · 권한≠4 |
| **G4** | **입력 · config · capability 가 정확히 같다** | 「설정은 A 인데 권한은 B」 — **설치 후에야 드러나는 고장** |
| **G5** | **미결 넷** | 이것들을 **침묵으로 통과시키는 것** |
| **G6** | manifest 를 찍는다 | **없는 아티팩트의 해시를 지어내는 것** |

### G1 의 「정확한 단일 origin」 판정

`new URL()` 로 파싱한 뒤 **스킴·호스트만 남은 형태**만 받는다 — `value === url.origin`(끝 슬래시 하나까지 허용).
느슨하게 두면 관문이 관문이 아니게 된다.

---

## 5. G5 — **이 관문이 잴 수 없는 것을 잰 척하지 않는다**

D-4(PRODUCTION 로그인 수단) · 운영 서버 실재 · M-1(https 신뢰) · M-5 는 **정적 검사로 잴 수 없다.**
그래서 둘 중 하나만 한다:

- 증거가 **없으면 막는다**(기본값). **없음을 통과로 바꾸지 않는다**
- 증거 파일(`SHELL_FINAL_EVIDENCE`)에 `{ resolved: true, reference: "<근거>" }` 로 있으면
  manifest 에 **`status: "attested"` · `measuredByThisGate: false`** 로 싣고 **누가 무엇을 근거로**
  그렇게 말했는지 남긴다

**즉 초록이 나와도 「운영 서버가 실재한다」는 뜻이 아니라 「그 주장이 기록되었다」는 뜻이다.**
그 구분을 출력에서 지우지 않았다 — 통과 화면이 **「통과가 뜻하지 않는 것」 세 줄**을 항상 찍는다.

> 이 설계의 한계를 숨기지 않는다: 증거 파일은 **사람의 주장**이지 측정이 아니다. 관문이 할 수 있는
> 최선은 **주장을 강제로 기록에 남기게 하는 것**이고, 실제 판정은 그 `reference` 를 읽는 사람이 한다.

---

## 6. G6 manifest — **해시를 지어내지 않는다**

기록 항목: `appVersion`(Cargo.toml=`0.0.1`) · `shellApi`(lib.rs=`1`) · `identifier`
(`app.stronghajin.desktop`) · `productName` · `bundleTargets` · `operationalOrigin` ·
`capabilityRemoteUrl` · `originsAgree` · `attestations` · `artifacts` · `hostPlatform`.

아티팩트는 **`target/release/bundle` 에 실재하는 파일만** 읽어 sha256 을 만든다.
현재는 그 디렉터리가 없어 **`artifacts: []` · `artifactNote: "빌드 아티팩트가 없다"`** 다 —
**자리표시 해시를 만들지 않았다.** `.app` 은 디렉터리라 해시 대신 «있다»는 사실만 적는다.

manifest 는 **stdout 으로만** 나간다. 이 스크립트는 **어떤 파일도 쓰지 않는다.**

---

## 7. 검증 — 실제로 돌린 것

### 7-1. 현재 환경(T-1) — **막힌다**

```
$ make shell-final-preflight
-- 막은 것: 7건 --
  ✗ G1 입력 없음 — 최종 origin 을 주지 않았다 … **이 스크립트는 값을 지어내지 않는다**
  ✗ G2 shell.config.json · operationalOrigin: 값이 비어 있다(미정) … (OQ-T02)
  ✗ G3 product-shell.json · remote.urls[0]: 자리표시 주소다(.invalid)
  ✗ G5 D-4 — PRODUCTION 로그인 수단 — **미결**
  ✗ G5 운영 서버 실재 — **미결**
  ✗ G5 M-1 — https 신뢰(인증서 체인) — **미결**
  ✗ G5 M-5 — **미결**
관문이 막혔다 — 7건. **최종 빌드로 넘어가지 않는다.**
```

**스크립트 exit 1**(`make` 는 레시피 실패를 자기 규칙대로 **2** 로 되돌린다 — 둘 다 0 이 아니다).

### 7-2. 형식 거부(T-2) — 9종 전부 막았다

| 입력 | 거부 사유 |
|---|---|
| `http://app.example.com` | https 가 아니다 |
| `https://x.invalid` | 자리표시 주소다(.invalid) |
| `https://*.example.com` | 와일드카드 |
| `https://app.example.com/app` | 경로가 붙어 있다 |
| (빈 값) | 값이 비어 있다 |
| `https://localhost` · `https://1.2.3.4` | loopback/IP |
| `not-a-url` | URL 이 아니다 |
| `https://a.example.com?x=1` | 질의/조각 |

### 7-3. 불일치·증거 부재(T-3·T-4)

| # | 상황 | 결과 |
|---|---|---|
| T-3 | config=`app.example.com` · capability=`other.example.com` | **G4 가 막았다** — 「설치 후에야 드러나는 고장」 |
| T-4 | 셋 일치하되 **증거 없음** | **G5 4건이 막았다** · exit 1 |
| T-5 | 셋 일치 + 증거 있음 | exit 0 — **단, 「연습」으로 표시된다**(아래) |

### 7-4. T-3~T-5 를 어떻게 돌렸는가 — **진짜 설정을 건드리지 않았다**

운영 origin 이 정해지기 전에는 **「값이 들어오면 관문이 실제로 초록이 되는가」를 확인할 방법이 없다.**
Phase 7 에서 `.icns` 가 없어 strict 가 영원히 붉던 문제와 같은 함정이다 — **통과 경로가 한 번도
실행되지 않은 관문은 관문이 아니다.**

그래서 읽기 전용 `--shell-root` 를 두고, 설정 **사본**을 scratchpad 에 만들어 돌렸다.
**진짜 `src-tauri` 는 한 글자도 바뀌지 않았다**(§2 확인).

**대신 그 경로를 악용할 수 있다는 사실을 스스로 크게 적게 했다** — 기본이 아닌 트리로 돌리면:

- 배너: `⚠⚠ **연습 실행** … **이 실행은 관문 통과로 쓸 수 없다.**`
- manifest: `"rehearsal": true` · `"rehearsalNote": "…관문 통과로 쓸 수 없다"` · `"shellRoot": "<경로>"`
- 마지막 줄: `연습 통과(관문 통과가 아니다)`

T-5 의 증거 파일도 `reference: "(연습용 가짜 근거 — 실제 결정 아님)"` 로 적었다 —
**그 초록을 D-4 해결로 읽을 수 없게** 값 자체에 써 넣었다.

---

## 8. 운영 origin 이 정해진 뒤의 순서 (후속 워커용)

```
1) make shell-final-preflight SHELL_OPERATING_ORIGIN=https://<host>
   → G2·G3 가 «설정이 아직 자리표시다»로 막는다
2) 사람이 shell.config.json · capabilities/product-shell.json 을 그 origin 으로 확정
   (capability 는 정확히 "<origin>/*" 하나)
3) D-4 결정 · 운영 서버 실재 · M-1 · M-5 를 실제로 해결하고 근거를 증거 파일에 기록
4) make shell-final-preflight SHELL_OPERATING_ORIGIN=… SHELL_FINAL_EVIDENCE=…   → exit 0
5) make shell-verify SHELL_STRICT=1        → 구성 미비 0건(.icns 포함)
6) 호스트 플랫폼 번들 빌드 → 4) 를 다시 돌려 manifest 의 해시를 채운다
```

**2) 를 1) 보다 먼저 하지 않는다** — 관문이 먼저 붉어야 «무엇을 채울지»가 화면에 적힌다.

---

## 9. 남은 차단 — **이번 작업이 풀지 못한 것**

| 항목 | 상태 | 왜 여기서 못 푸는가 |
|---|---|---|
| **운영 origin**(OQ-T02) | **미정** | 결정 사항이다. **발명 금지** |
| **D-4** PRODUCTION 로그인 수단 | **미결** | 백엔드 설계 결정. 이번 허용 경로 밖 |
| **운영 서버 실재** | **미확인** | 이 관문은 네트워크를 건드리지 않는다 |
| **M-1**(https 신뢰) · **M-5** | **미측정** | 실기·사용자 설치가 필요하다 |
| **M-10** | **미측정** | 사람의 설치가 필요하다 |
| **Windows 축 전부** | **검증 불가(이 기기)** | macOS 결과로 대체하지 않는다 |
| macOS `.icns` | **없음** | `shell-verify --strict` 가 잡는다 |
| **N-2 프론트 스위트 불안정** | **이월** | 이번 회차는 `frontend/src` 를 건드리지 않았다. **통과로 만들려 재실행하지 않았다** |

---

## 10. 금지 사항 준수

| 금지 | 확인 |
|---|---|
| capability placeholder/fixture origin 변경 | **하지 않았다** — `git diff --stat frontend/src-tauri/` 출력 0줄 |
| 운영 origin · 도메인 · 로그인 수단 발명 | **0** — 스크립트가 값을 지어내지 않고 **입력 없음을 실패로 처리**한다 |
| placeholder 를 최종판으로 굽기 | **막았다**(G1·G2·G3) |
| 미결(D-4 · 서버 · M-1 · M-5)을 통과로 쓰기 | **막았다**(G5) · 증거가 있어도 **«attested»** 이지 «측정»이 아니다 |
| 실제 설정 파일 쓰기 · 빌드 · 설치 · Release · 태그 · push | **없음** · HEAD `a1f6791` 그대로 |
| 허용 경로 밖 변경 | 없다 — 스크립트 1(신규) · Makefile(타깃 1 + `.PHONY`) · 보고서 1 |
