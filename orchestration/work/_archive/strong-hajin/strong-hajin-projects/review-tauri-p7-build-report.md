# WORK-006 Phase 7 — 독립 검수

- **코드 워크트리**: `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-projects` · HEAD `a1f6791`(변동 없음)
- **검수 대상**: `tauri-p7-build-report.md` ↔ 실제 변경
- **코드·설정·문서 수정 0줄. 검수 보고서 한 파일만 작성.**
- **설치·배포·태그·push 없음.** 돌린 것은 **읽기 전용 검증과 dry-run**뿐이다.

---

## 0. 종합 판정 — **PASS · FAIL 0 · WARN 3**

**Phase 7 은 «구성을 고치고 검증기를 세운» 작업이고, 그 둘이 다 맞다.**
판 번호가 `tauri.conf.json`(0.1.0)과 `Cargo.toml`(0.0.1)로 **갈려 있던 실제 결함**을 찾아
**출처를 하나로 모았고**, 그 근거(Tauri 의 「version 을 지우면 Cargo.toml 을 쓴다」)가
**상류 소스에서 확인된다.** 식별자·원격 문서 계약·권한 경계는 **한 글자도 안 바뀌었다.**

**보고된 V-1 ~ V-10 열 건을 전부 재현**했다 — 검증기가 실패를 **실제로 잡는 것**(`SHELL_TAG=v9.9.9`
→ exit 2)까지 확인했다. Windows·M-10·설치파일 생성은 **어디서도 통과로 쓰이지 않았고**,
D-4 는 미결로 유지된다.

WARN 3 건은 **판정을 뒤집지 않는 한계·기록 문제**다.

---

## 1. 판정표

| # | 검수 항목 | 판정 |
|---|---|---|
| 1 | 버전 단일 출처(Cargo.toml `0.0.1`) · 식별자/원격 문서 계약 보존 | **PASS** (상류 권고와의 차이는 W-2) |
| 2 | `make shell-verify` 가 실제로 검증하고 실패를 숨기지 않는가 | **PASS** (단 `.icns` 처리는 W-1) |
| 3 | `make shell-build-fixture` 기본 dry-run · 두 주소 불일치 시 중단 · 운영 주소 미발명 | **PASS** |
| 4 | 허용 경로 밖 코드/인프라/Release/태그/서명/CI 변경 없음 | **PASS** |
| 5 | 기록된 cargo/tsc/frontend 수치가 현재 diff 와 일치 | **PASS** (10/10 재현) |
| 6 | Windows 실기 · M-10 · 설치파일 생성을 통과로 쓰지 않음 | **PASS** |
| 7 | D-4 로그인 미결 유지 | **PASS** |

---

## 2. FAIL

**없다.**

---

## 3. 항목별 확인

### 3-1. 버전 단일 출처 · 계약 보존 (PASS)

**결함이 실재했다**: `tauri.conf.json` 의 `"version": "0.1.0"` 과 `Cargo.toml` 의 `0.0.1` 이 갈려,
**설치파일이 말하는 판과 `shell_info.app_version`(= `CARGO_PKG_VERSION`)이 달랐다.**

**고친 방식의 근거를 상류에서 확인했다** — `tauri-utils-2.9.3/src/config.rs`:

> `/// App version. … **If removed the version number from `Cargo.toml` is used.**`

→ `"version"` 제거로 **단일 출처가 `Cargo.toml` `0.0.1`** 이 된다. `make shell-verify` 출력도
`tauri.conf.json 에 version 이 없다 → Tauri 가 Cargo.toml 을 쓴다. 단일 출처 = 0.0.1` 로 말한다.

**보존 확인(현재 `tauri.conf.json` 전문 대조)**:

| 계약 | 값 | 상태 |
|---|---|---|
| `identifier` | `app.stronghajin.desktop` | **보존**(AC-T34·AC-T35) |
| `build.frontendDist` | `shell-noop` | **보존** |
| `app.windows` | `[]` — 창은 Rust 가 만든다 | **보존**(AC-T33) |
| `app.withGlobalTauri` | `false` | **보존** |
| `app.security` | `{}` — **셸이 CSP 를 박지 않는다** | **보존** |
| `bundle.targets` · `icon` · `macOS.{infoPlist,entitlements}` | 그대로 | **보존** |
| `capabilities/product-shell.json` · `shell.config.json` · `src-tauri/src/**` · `Cargo.toml` | **파일 자체가 이번 회차에 열리지 않았다**(mtime 확인) | **무변경** |

- `cargo test` **45 passed** 안에 `셸_설정이_제품_정체성을_지킨다`(식별자·CSP 부재·trayIcon 부재)가
  포함돼 있고 통과한다 → **version 제거가 `generate_context!` 도 깨뜨리지 않았다.**
- **`Cargo.toml` 을 고치지 않은 판단이 옳다** — 허용 경로 밖이고, 「어느 값이 맞는 판인가」는
  Phase 8/9 의 결정이다. **두 값 중 하나를 고르는 대신 출처를 하나로 만들었다.**

### 3-2. `make shell-verify` — 실제로 검증하고 실패를 잡는다 (PASS)

**재현한 동작**:

| 실행 | 결과 |
|---|---|
| `make shell-verify` | **exit 0 · 「문제 0건」** |
| `make shell-verify SHELL_TAG=v0.0.1` | exit 0 · `코드 태그 v0.0.1 가 판 번호 0.0.1 와 같다` |
| `make shell-verify SHELL_TAG=v9.9.9` | **exit 2** · `✗ 코드 태그와 판 번호가 다르다 — tag=v9.9.9 · version=0.0.1` · `실패 1건` |

→ **검증기가 검증된다.** 초록만 내는 스크립트가 아니라 **틀린 입력에서 실제로 붉어진다.**

**스크립트가 재는 것을 소스에서 직접 확인**(`verify-shell-build.mjs`):

| # | 검사 | 실패 처리 |
|---|---|---|
| 1 | `Cargo.toml` semver · `tauri.conf` 의 version 존재 시 **값 불일치면 fail** · `lib.rs` 가 `env!("CARGO_PKG_VERSION")` 를 쓰는가 | `fail` |
| 2 | 번들 타깃(mac `app`·`dmg` / win `msi`·`nsis`, `"all"` 은 둘 다 포함으로 인정) · `bundle.active` · `Info.plist`·`Entitlements.plist` **실재** | `fail` |
| 3 | 아이콘 **실재 + 매직바이트**(PNG `89 50 4E 47` · ICO `00 00 01 00`) · **`.ico` 없으면 fail** | `fail` |
| 4 | `frontendDist: shell-noop` + **디렉터리 실재** · `app.windows` 빈 배열 · `withGlobalTauri:false` · **CSP 미기재** · 참조 제품 식별자 아님 | `fail` |
| 5 | capability **파일 하나** · `local:false` · `remote.urls` **하나** · `://*.` 와일드카드 없음 · **권한 정확히 넷** | `fail` |

- **플랫폼을 섞지 않는다** — 출력이 「이 호스트(darwin)에서 구울 수 있는 것: macOS(app·dmg).
  Windows(msi·nsis) 는 **이 기기에서 검증 불가** — 다른 쪽 결과로 대체하지 않는다」로 **갈라 적는다.**
- **자리표시를 숨기지 않는다** — `product-shell.json: 운영 origin 이 아직 자리표시다(...invalid/*)` 를
  매번 노트로 낸다.
- ⚠ 한 가지 예외가 `.icns` 다 → **W-1**.

### 3-3. `make shell-build-fixture` — dry-run · 중단 · 주소 미발명 (PASS)

**재현한 동작**:

| 실행 | 결과 |
|---|---|
| `make shell-build-fixture`(인자 없이) | **exit 2** · `SHELL_FIXTURE_ORIGIN 을 주세요` — Makefile 가드가 막는다 |
| `SHELL_FIXTURE_ORIGIN=https://fixture.example.invalid` | **exit 2 · 굽지 않고 중단.** `✗ shell.config.json · operationalOrigin = null` · `✗ capabilities/… remote.urls[0] = https://operational-origin-not-yet-decided.invalid/*` + **무엇을 어디에 쓸지** 두 줄 안내 + `⚠ 어긋난 채로 구우면 창은 뜨는데 커맨드가 ACL 에서 거절된다(E-06)` |
| `--origin http://…`(검수가 추가로 확인) | **exit 2** · `--origin 은 https 여야 한다(마이크·쿠키 조건)` |

- **기본이 dry-run 이다** — `--run`/`SHELL_BUILD` 가 없으면 `process.exit(0)` 전에
  「실제로 구우려면 …」 안내만 내고 **`cargo tauri build` 를 부르지 않는다**(소스 118-124행).
- **두 파일을 고치지 않는다** — 읽어서 대조만 하고 **사람이 맞추라고 말하고 멈춘다.**
  **운영 주소를 발명하지 않는다**(OQ-T02 유지).
- **설치 동작이 아예 없다** — 두 스크립트 어디에도 설치 호출이 없다(검수가 소스 전수 확인).
- **M-10 절차**(1판 설치 → 로그인 → `Cargo.toml` 한 줄 올림 → 2판 덮어 설치)를 출력에 적고,
  **식별자를 바꾸면 저장소가 새로 잡혀 그것 때문에 로그아웃된다**는 함정까지 경고한다. 정확하다.

### 3-4. 허용 경로 (PASS)

**이번 회차에 바뀐 파일은 정확히 넷**(`find -newermt` · `git status` 대조):

```
Makefile                                   (수정 — 타깃 2개 + .PHONY)
frontend/src-tauri/tauri.conf.json         (수정 — "version" 제거)
frontend/scripts/verify-shell-build.mjs    (신규)
frontend/scripts/build-shell-fixture.mjs   (신규)
```

| 금지 | 확인 |
|---|---|
| `src-tauri/src/**` · `Cargo.toml` · `shell.config.json` · `capabilities/` | **열리지 않았다**(mtime 0건) |
| backend · 제품 프론트(`src/**`) · 인프라 레포 | **0줄** |
| **태그** | `git tag --points-at HEAD` → **없음**. HEAD `a1f6791` 그대로 |
| **CI** | `.github/workflows` **존재하지 않음** |
| **서명·공증·자동업데이트** | `tauri.conf.json` 에 `signingIdentity`·`notarize`·`updater` **0건** |
| 커밋 · push · Release | **없음** |

### 3-5. 수치 재현 — 10/10 일치 (PASS)

| # | 명령 | 보고서 | **재현** | 일치 |
|---|---|---|---|---|
| V-1 | `make shell-verify` | exit 0 · 문제 0건 | **exit 0 · 「문제 0건」** | ✅ |
| V-2 | `… SHELL_TAG=v0.0.1` | 같다고 답 | **exit 0 · 같다** | ✅ |
| V-3 | `… SHELL_TAG=v9.9.9` | **exit 2** | **exit 2 · 실패 1건** | ✅ |
| V-4 | `make shell-build-fixture` | exit 2 | **exit 2** | ✅ |
| V-5 | `… SHELL_FIXTURE_ORIGIN=…` | 거부 + 안내 · 굽지 않음 | **exit 2 · 안내 후 중단** | ✅ |
| V-6 | `cargo check --all-targets` | warning 0 · error 0 | **exit 0 · warning 0** | ✅ |
| V-7 | `cargo test` | 45 passed | **45 passed · 0 failed** | ✅ |
| V-8 | `cargo clippy … -D warnings` | 통과 | **exit 0** | ✅ |
| V-9 | `npx tsc --noEmit` | 출력 0줄 | **exit 0 · 0줄** | ✅ |
| V-10 | `make frontend-test` | 1053 passed | **exit 0 · 1053 passed** | ✅ |

- **V-7 이 특히 의미가 있다** — `tauri.conf.json` 을 고친 뒤이므로 `generate_context!` 가 새 설정을
  다시 읽는다. 45건 통과는 **version 제거가 빌드 컨텍스트를 깨지 않았다**는 증거다.
- 「`cargo check`·`cargo test`·`clippy` 는 **컴파일 검사이지 설치파일 생성이 아니다**」라는
  보고서 §6 의 단서도 **정확하다.**

### 3-6. 미검증을 통과로 쓰지 않았다 (PASS)

| 항목 | 보고서 표기 | 판정 |
|---|---|---|
| **실제 설치파일 생성** | 「**하지 않음**」 · §1 「설치파일을 굽지 않았고, 아무것도 설치하지 않았다」 | ✅ |
| **Windows 축 전부** | 「**검증 불가(이 기기)** · macOS 결과로 대체하지 않는다」 · 스크립트 출력도 매번 같은 말 | ✅ |
| **M-10** | 「**미측정** — 사람이 설치해야 한다. **정적 검증을 실기 통과로 쓰지 않는다**」 | ✅ |
| macOS `.icns` | 「**없음(경고로 표시)**」 — 숨기지 않았다 | ✅ (다만 W-1) |
| 운영 origin · 최소 OS · 서명/공증/CI | **미정 · 없음**, 발명 0 | ✅ |

### 3-7. D-4 유지 (PASS)

§7 마지막 행 — 「**Phase 6b D-4**(PRODUCTION 로그인 수단) · **미결 유지** · 이번 작업이 건드리지
않았다」. 실제로 backend **0줄**이므로 사실과 맞다. **차단은 그대로다.**

---

## 4. WARN (3건)

| # | 내용 | 근거 | 수정 방향 |
|---|---|---|---|
| **W-1** | **`shell-verify` 초록이 「구울 수 있다」를 뜻하지 않는다.** macOS `.icns` 부재를 `problems` 가 아니라 `unverifiable`(⚠ 줄)로 보내므로, **번들 단계에서 막힐 수 있는 구성인데 exit 0** 이 나온다. 보고서 §7 이 「없음(경고로 표시)」로 **숨기지는 않았으나**, 「V-1 통과 = 빌드 가능」으로 오독될 여지가 있다 | `verify-shell-build.mjs:131-136` · V-1 출력의 ⚠ 줄 | 마지막 줄을 「문제 0건 — **단 ⚠ 항목은 굽기 전에 닫아야 할 수 있다**」로 한정하거나, macOS 호스트에서 **`--for-build` 같은 엄격 모드**를 두어 `.icns` 를 fail 로 올린다 |
| **W-2** | **Tauri 상류는 반대 방향을 권한다.** 보고서가 인용한 문장 **바로 다음 줄**이 「*It's recommended to manage the app versioning in the Tauri config.*」다. 이번 선택(Cargo.toml 단일화)은 **정당하다** — `Cargo.toml` 이 허용 경로 밖이었고 값 판단을 피했다 — 그러나 **상류 권고와 어긋난다는 사실이 보고서에 없다.** Phase 8 에서 판을 올릴 때 어느 쪽을 출처로 삼을지 **다시 정해야 할 자리**다 | `tauri-utils-2.9.3/src/config.rs` 해당 doc comment | §3 에 「상류는 conf 쪽을 권하나, 허용 경로·값 판단 회피 때문에 Cargo.toml 로 모았다. Phase 8 에서 재검토」 한 줄 |
| **W-3** | **보고서 머리말 작성 시각이 `2026-09-22 23:2x KST` 로 «자리표시»다.** 이 문서들이 감사 기록으로 쌓이므로 분 단위가 비어 있으면 회차 대조가 어려워진다 | 보고서 1행 아래 | 실제 시각으로 치환 |

> 직전 Phase 들에서 올린 「정적 검사(ruff·mypy) 부재」는 이번 범위 밖이라 다시 올리지 않는다.

---

## 5. 차단·미결 (이번 회차가 만든 것 아님 — 유지)

| # | 항목 | 주인 |
|---|---|---|
| 1 | **D-4** — PRODUCTION 세션 발급 수단 부재. **운영 배포를 「사용 가능」으로 판정할 수 없다** | 코디·사용자(OQ-W05) |
| 2 | **fixture origin 확정**(두 파일 같은 값) — 이것 없이는 fixture 판도 굽지 못한다 | 사용자·코디(OQ-T02) |
| 3 | **제품 아이콘 세트(`.icns` 포함)** — 지금은 자리표시 | Phase 7 후속/8 |
| 4 | **판 번호 정책** — `0.0.1` 유지 vs 첫 배포판으로 올림 (W-2 와 함께 결정) | 코디 |
| 5 | **M-10 실기** · **Windows 실기/빌드 환경** | 사용자 · OQ-W01 |

---

## 6. 한 줄 정리

**Phase 7 은 실재하는 판 번호 분열을 찾아 근거 있게 고쳤고, 그 고침이 되돌아오면 붉어지는
검증기를 함께 세웠다.** 허용 경로 밖 변경 0, 수치 10/10 재현, Windows·M-10·설치파일은
어디서도 통과로 쓰이지 않았다. 남은 것은 **`shell-verify` 초록의 한계 표기(W-1)** 와
**판 번호 출처를 Phase 8 에서 재확인하는 것(W-2)**, 그리고 **D-4·fixture origin 결정**이다.
