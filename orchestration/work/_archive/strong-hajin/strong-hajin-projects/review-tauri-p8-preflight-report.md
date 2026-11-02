# WORK-006 Phase 8 preflight — 독립 검수

- **코드 워크트리**: `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-projects` · HEAD `a1f6791`(변동 없음)
- **검수 대상**: `tauri-p8-preflight-report.md` ↔ `frontend/scripts/verify-final-build.mjs` · `Makefile`
- **코드·설정·문서 수정 0줄. 이 검수 보고서 한 파일만 작성.**
- **운영 배포·설치·Release·태그·push 없음.** 돌린 것은 **쓰기 연산이 없는 관문 스크립트**와
  **내 스크래치패드 사본 실험**뿐이다.

---

## 0. 종합 판정 — **FAIL 0 · WARN 2 · 나머지 PASS**

**이 관문은 「채워라」가 아니라 「굽지 말라」를 구현했고, 그 구현이 실제로 막는다.**
현재 환경에서 **7건을 들고 exit 1**(make 는 2)로 멈추며, 그 7건이 **입력 없음 · `shell.config` 미정 ·
capability 자리표시 · 미결 넷**으로 정확히 갈려 있다.

**구조적 안전이 grep 으로 증명된다** — 스크립트의 import 는 `readFileSync · existsSync ·
readdirSync · statSync` 뿐이고, **`writeFile`·`mkdir`·`exec`·`spawn`·`fetch` 가 한 건도 없다.**
「설정 파일을 쓰지 않는다 · 네트워크를 건드리지 않는다」가 주장이 아니라 **코드의 성질**이다.

**`--shell-root` 연습이 저장소를 건드리지 않는다는 것을 검수가 해시로 확인했다** —
실험 전후 `shell.config.json`·`product-shell.json` 의 `shasum` 이 **완전히 동일**하다.

WARN 2 건은 **연습 통과의 «기계 신호»** 와 **M-5 라벨 누락**이다.

---

## 1. 판정표

| # | 검수 항목 | 판정 |
|---|---|---|
| 1 | 운영 origin 미결/placeholder 에서 nonzero 차단 | **PASS** |
| 2 | https 단일 origin · wildcard/path/query/localhost/IP/`.invalid`/빈값 거부 | **PASS** (12종 재현) |
| 3 | `shell.config` ↔ capability 불일치 차단(G4) | **PASS** |
| 4 | D-4 · 서버 실재 · M-1/M-5 를 정적 통과시키지 않고 evidence 있을 때만 `attested` | **PASS** (라벨 누락은 W-2) |
| 5 | `--shell-root` 연습이 실제 repo 설정을 바꾸지 않음 | **PASS** (해시 동일) · 기계 신호는 **W-1** |
| 6 | Phase 7 `shell-verify` 회귀 · 허용 경로 · Release/설치/태그/push 부재 | **PASS** |
| 7 | origin 없는 상태를 Phase 8 완료/최종 아티팩트로 과장하지 않음 | **PASS** |

---

## 2. FAIL

**없다.**

---

## 3. 항목별 확인

### 3-1. 미결/placeholder 차단 (PASS)

```
$ make shell-final-preflight          → MAKE_EXIT=2
$ node scripts/verify-final-build.mjs → NODE_EXIT=1
-- 막은 것: 7건 --
  ✗ G1 입력 없음 — … **이 스크립트는 값을 지어내지 않는다**
  ✗ G2 shell.config.json · operationalOrigin: 값이 비어 있다(미정) … (OQ-T02)
  ✗ G3 product-shell.json · remote.urls[0]: 자리표시 주소다(.invalid) — https://operational-origin-not-yet-decided.invalid
  ✗ G5 D-4 · ✗ G5 운영 서버 실재 · ✗ G5 M-1 · ✗ G5 M-5   (각 «미결»)
관문이 막혔다 — 7건. **최종 빌드로 넘어가지 않는다.**
```

**보고서의 7건·exit 값이 그대로 재현된다.** 「입력 없음」을 **침묵이 아니라 실패**로 다루는 것이
이 관문의 핵심이고, 그것이 코드에 있다(`rawInput === null → block`).

### 3-2. origin 형식 — **12종 전부 거부** (PASS)

보고서가 든 9종에 **검수가 3종을 더해** 돌렸다. 전부 `exit 1`:

| 입력 | 실제 거부 사유 |
|---|---|
| `http://app.example.com` | https 가 아니다(마이크·쿠키 조건) |
| `https://x.invalid` | 자리표시 주소다(.invalid) |
| `https://*.example.com` | 와일드카드를 쓰고 있다 |
| `https://app.example.com/app` | 경로가 붙어 있다(단일 origin 이 아니다) |
| (빈 값) | 값이 비어 있다(미정) |
| `https://localhost` · `https://1.2.3.4` | 운영 origin 이 loopback/IP 다 |
| `not-a-url` | URL 이 아니다 |
| `https://a.example.com?x=1` | 질의/조각이 붙어 있다 |
| **`https://a.example.com#f`**(검수 추가) | 질의/조각이 붙어 있다 |
| **`  https://a.example.com`**(검수 추가) | 앞뒤 공백이 있다 |
| **`https://u:p@a.example.com`**(검수 추가) | 자격증명이 섞여 있다 |

- **「정확한 단일 origin」 판정이 실제로 엄격하다** — `value !== url.origin && value !== url.origin + "/"`
  이면 거부한다. 느슨한 정규식이 아니라 **파서의 정규형과 대조**한다.
- 같은 `checkOrigin` 을 **G1·G2·G3 가 공유**하므로 세 자리의 기준이 갈라질 수 없다.

### 3-3. 불일치 차단 G4 (PASS — 검수가 직접 재현)

사본 트리에 `config=https://app.example.com` · `capability=https://other.example.com/*` 을 만들고 돌렸다:

```
EXIT=1
✗ G4 세 곳의 origin 이 갈렸다 — 입력=https://app.example.com · shell.config=https://app.example.com
  · capability=https://other.example.com. **설치 후에야 드러나는 고장**이므로 여기서 멈춘다
```

→ 「창은 뜨는데 커맨드가 ACL 에서 거절되는」 판이 **구워지기 전에** 막힌다.
capability 를 일치시키자 G4 가 통과하고 **G5 4건만 남았다**(아래).

### 3-4. G5 — 못 재는 것을 잰 척하지 않는다 (PASS)

**코드가 요구하는 조건이 정확하다**: `!entry || entry.resolved !== true || !entry.reference` → **block**.
「resolved 만 true」이거나 「reference 가 빈 문자열」이면 **통과하지 못한다.**

| 검수 실험 | 결과 |
|---|---|
| 셋 일치 · **증거 없음** | **exit 1** · `G5` **4건** 차단 · `관문이 막혔다 — 4건` |
| 셋 일치 · 증거 있음 | exit 0 · manifest 에 `"status": "attested"` · **`"measuredByThisGate": false`** · `attestedBy`(미기재 시 `"(미기재)"`) |

- **「통과」가 「측정」이 아님을 manifest 필드 이름 자체가 말한다** — `measuredByThisGate: false`.
  기계가 읽어도 구분된다.
- 통과 화면이 **「통과가 뜻하지 않는 것」 세 줄**(서버 실재 · 로그인 · 설치파일)을 항상 찍는다 — 재현 확인.
- 증거 파일이 없거나 JSON 이 깨지면 **exit 2**(사용법 오류)로 갈라 낸다 — 조용히 무시하지 않는다.

### 3-5. `--shell-root` 연습 — 저장소 무변경 (PASS)

**해시로 확인했다**:

```
실험 전  shasum shell.config.json · capabilities/product-shell.json
실험 후  ↑ 와 완전히 동일  →  "동일(해시 일치) ✅"
```

- 실험은 **스크래치패드 사본**에서만 이뤄졌고, 사본은 삭제했다.
- **구조적 보증이 더 강하다** — 스크립트에 쓰기 API 가 **한 줄도 없다**(§0). 경로를 어디로 주든
  쓸 수 없다.
- 연습 실행은 **세 곳에 스스로 표시한다**: 상단 배너 `⚠⚠ **연습 실행**` · manifest
  `"rehearsal": true` + `"rehearsalNote"` + `"shellRoot"` · 마지막 줄 `연습 통과(관문 통과가 아니다)`.
  **전부 재현했다.**
- ⚠ 다만 **종료 코드는 진짜 통과와 같다** → **W-1**.

### 3-6. Phase 7 회귀 · 허용 경로 · 금지 (PASS)

| 확인 | 결과 |
|---|---|
| `make shell-verify` | **exit 0** · `문제 0건 · 구성 미비 1건 · 호스트 한계 1건` — **Phase 7 판정 그대로** |
| `make shell-verify-strict` | **exit 2** · `실패 1건`(`.icns`) — 그대로 |
| 이번 회차 변경 | **`Makefile` · `frontend/scripts/verify-final-build.mjs`(신규) 둘**(`find -newermt "23:48"`) + 보고서 1 |
| `src-tauri/**` | **무변경** — `shell.config.json` 은 여전히 `operationalOrigin: null`, capability 는 여전히 `.invalid`(관문 출력이 그 값을 그대로 읽어 보여준다) |
| `verify-shell-build.mjs` · `build-shell-fixture.mjs` · `tauri.conf.json` · `Cargo.toml` · 제품 프론트 · backend · 인프라 | **무변경** |
| Makefile 변경 | `.PHONY` 에 `shell-final-preflight` 한 낱말 + 레시피 4줄(주석 3줄). **기존 타깃 무수정** |
| 태그 · CI · Release · push · 설치 | `git tag --points-at HEAD` **없음** · `.github/workflows` **없음** · HEAD `a1f6791` 그대로 |

### 3-7. 과장하지 않았다 (PASS)

- 제목·머리말이 **`preflight`·「관문 신설」**이고, **「Phase 8 완료」라고 쓰지 않았다.**
  「현재 환경에서 7건을 막고 exit 1 — **이것이 의도한 동작이다**」로 **붉은 상태를 결과로** 제시한다.
- **최종 아티팩트를 만들었다고 하지 않았다** — manifest 재현 결과
  `"artifacts": []` · `"artifactNote": "빌드 아티팩트가 없다(target/release/bundle 부재)"` ·
  `"operationalOrigin": null` · `"originsAgree": false`. **자리표시 해시가 없다.**
- §9 가 **이번 작업이 풀지 못한 것**(운영 origin · D-4 · 서버 실재 · M-1/M-5 · M-10 · Windows ·
  `.icns` · N-2)을 표로 남긴다. **T-5 초록도 「연습」으로 못 박았다.**
- 증거 파일의 `reference` 에 「(연습용 가짜 근거 — 실제 결정 아님)」을 **값 자체에** 써 넣어
  그 초록을 D-4 해결로 읽을 수 없게 한 것은 **특히 좋은 처리**다.

---

## 4. WARN (2건)

| # | 내용 | 근거 | 수정 방향 |
|---|---|---|---|
| **W-1** | **연습 통과의 «기계 신호»가 진짜 통과와 같다.** 사람이 읽는 배너·manifest·마지막 줄은 모두 「연습」이라 말하지만 **종료 코드는 둘 다 `0`** 이다. 관문을 자동화에 걸면(CI·스크립트) **exit 0 만 보고 연습을 통과로 집계**할 수 있다. 게다가 **`SHELL_ROOT` 환경변수가 `make` 를 그대로 통과**해(검수가 확인) `make shell-final-preflight` 로도 연습 경로에 들어갈 수 있다 — Makefile 은 `--shell-root` 를 노출하지 않으나 env 가 뚫려 있다. 덤으로, 없는 경로를 주면 **`node:fs` 원시 스택 트레이스**가 그대로 뜬다(친절한 메시지 없음) | 재현: 사본 트리 + 증거 → **exit 0** · `"rehearsal": true` · `연습 통과(관문 통과가 아니다)` / `SHELL_ROOT=/nonexistent make shell-final-preflight` → node 스택 | ① **연습 통과는 0 이 아닌 코드**(예: 3)로 내보내거나, 0 을 원하면 `--rehearsal` 을 **명시적으로 요구**한다 ② 설정 파일 읽기를 `try/catch` 로 감싸 「그 경로에 `shell.config.json` 이 없다」로 답한다 |
| **W-2** | **`M-5` 차단 줄이 「M-5 가 무엇인지」를 말하지 않는다.** 다른 셋은 이름이 붙어 있는데(`D-4 — PRODUCTION 로그인 수단` · `운영 서버 실재` · `M-1 — https 신뢰(인증서 체인)`) `m5` 만 `what: "M-5"` · `why: "미측정. 실기 확인이 필요하다"` 다. **그 줄만 보고는 무엇을 해결해야 하는지 알 수 없다**(M-5 = 앱 재시작 후 쿠키·로그인 유지) | `verify-final-build.mjs:238-240` | `what: "M-5 — 앱 재시작 후 로그인(쿠키) 유지"` 한 줄 |

> 둘 다 **판정을 뒤집지 않는다** — 관문이 막아야 할 것은 전부 막고 있고, 통과 경로도 정확하다.

---

## 5. 차단·미결 (이번 회차가 만든 것 아님 — 유지)

| # | 항목 | 주인 |
|---|---|---|
| 1 | **운영 origin**(OQ-T02) — **미정.** 이 관문의 G1·G2·G3 가 여기서 멈춘다 | 사용자·코디 |
| 2 | **D-4** — PRODUCTION 세션 발급 수단 부재 | 코디·사용자(OQ-W05) |
| 3 | **운영 서버 실재** · **M-1**(https 신뢰) · **M-5** · **M-10** | 사용자(실기) |
| 4 | **Windows 축 전부** — 검증 불가(이 기기) | OQ-W01 |
| 5 | macOS **`.icns`** — `shell-verify --strict` 가 잡는다 | Phase 7 후속/8 |
| 6 | **N-2 프론트 스위트 불안정** — 이번 회차는 `frontend/src` 무접촉, 재실행하지 않음 | 코디 |

---

## 6. 한 줄 정리

**「굽지 말라」가 코드로 서 있고, 검수가 돌려 보니 실제로 막는다** — 7건 차단 · origin 12종 거부 ·
불일치 차단 · 증거 없으면 미결 4건 차단. **쓰기 API 가 없어** 설정을 건드릴 수 없고, 연습이
저장소를 바꾸지 않음을 **해시로 확인**했다. 남은 것은 **연습 통과의 종료 코드(W-1)** 와
**M-5 라벨(W-2)** 두 줄이며, **Phase 8 을 완료로 쓴 곳은 어디에도 없다.**
