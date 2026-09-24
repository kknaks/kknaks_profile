# WORK-006 Phase 7 — fixture 판 빌드 구성

- **작성**: 2026-09-22 **23:26 KST**
- **검수 보정**: 2026-09-22 **23:30 KST** — WARN 3건 반영(strict 검증 경로 · 상류 권고 명시 · 시각). 상세는 `tauri-p7-build-fix-report.md`
- **코드 워크트리**: `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-projects` · HEAD `a1f6791`(변동 없음)
- **결과**: 빌드 구성·판 번호 검증을 코드에 마련했다. **설치파일을 굽지 않았고, 아무것도 설치하지 않았다**
- 커밋 · push · 태그 · Release · 서명 · 공증 **없음**

---

## 1. 한 줄 결론

**판 번호가 두 곳에서 갈라져 있던 것을 찾아 한 곳으로 모았다**(§3 — 설치파일은 `0.1.0`,
셸이 웹에게 말하는 값은 `0.0.1` 이었다). 그 일관성과 양 플랫폼 번들 구성을 **다시 돌려도 안전한
정적 검증**으로 자동화했고, fixture 판 절차는 **주소를 지어내지 않고 점검만** 하는 dry-run 으로 두었다.
**Windows 는 이 기기에서 «검증 불가»** 이고 **M-10 은 미측정**이다.

---

## 2. 변경 파일

| 파일 | 변경 | 성격 |
|---|---|---|
| `frontend/src-tauri/tauri.conf.json` | **`"version"` 필드 제거** (§3) | 수정 — 1줄 |
| `frontend/scripts/verify-shell-build.mjs` | 빌드 구성 정적 검증 | **신규** |
| `frontend/scripts/build-shell-fixture.mjs` | fixture 판 점검 + 명령 안내(기본 dry-run) | **신규** |
| `Makefile` | `shell-verify` · `shell-build-fixture` 타깃 + `.PHONY` | 수정 |

**건드리지 않은 것**: `src-tauri/src/**` · `Cargo.toml` · `shell.config.json` ·
`capabilities/product-shell.json` · 제품 프론트 · backend · 인프라 레포 · SPEC/WORK.

---

## 3. ⚠ 찾은 결함 — 판 번호가 두 곳에서 갈라져 있었다

### 무엇이 어긋났나

| 출처 | 값(이전) | 어디에 나타나나 |
|---|---|---|
| `tauri.conf.json:4` `"version"` | **`0.1.0`** | **설치파일의 판 번호** |
| `src-tauri/Cargo.toml:3` `version` | **`0.0.1`** | `shell_info.app_version`(`lib.rs:197` `env!("CARGO_PKG_VERSION")`) |

→ 설치파일은 **0.1.0** 이라 하고, 그 설치본이 웹에게는 **0.0.1** 이라고 말한다.
SPEC-006 §5 가 요구한 **「설치파일을 낼 때마다 판 번호 · 여는 주소 · `shell_api` 를 기록으로 남긴다」**
가 애초에 성립하지 않는 상태였다.

### 어떻게 고쳤나 — **한 곳으로 모았다**

`tauri.conf.json` 에서 **`"version"` 필드를 지웠다.** Tauri 의 계약이 그것이다:

> `version` — App version. … **If removed the version number from `Cargo.toml` is used.**
> (`tauri-utils-2.9.3/src/config.rs:3610-3612`)

- 이제 **`Cargo.toml` 의 `[package] version` 하나**가 설치파일·`shell_info`·코드 태그의 공통 출처다
- **`Cargo.toml` 을 고치지 않았다** — 허용 경로가 아니고, 무엇보다 **어느 값이 «맞는» 판인지는
  이 작업이 정할 일이 아니다.** 두 값 중 하나를 고르는 대신 **출처를 하나로 만들었다**
- 값은 현재 **`0.0.1`**(Cargo.toml 그대로). 판을 올리는 것은 Phase 8/9 의 결정이다

> **근거 기록(계약 요구)**: 기존 버전·식별자를 함부로 바꾸지 않았다. 식별자
> `app.stronghajin.desktop` 는 **그대로** 두었다 — 판을 넘어 고정해야 웹뷰 저장소가 유지된다(AC-T35).
> 바꾼 것은 **중복된 선언 하나를 없앤 것**이지 판 번호 자체가 아니다.

### ⚠ 상류(Tauri)는 «반대쪽»을 권고한다 — 그럼에도 이렇게 고른 이유

`@tauri-apps/cli` 가 싣는 공식 설정 스키마(`config.schema.json` 의 `version`)는 이렇게 적는다:

> App version. … If removed the version number from `Cargo.toml` is used.
> **It's recommended to manage the app versioning in the Tauri config.**

즉 **상류의 권고는 「`tauri.conf.json` 에서 판을 관리하라」**이고, 이번 선택(설정에서 빼고
`Cargo.toml` 을 단일 출처로)은 **그 권고와 반대 방향**이다. 그 사실을 숨기지 않고 적는다.

**그럼에도 이번 Phase 가 이렇게 고른 이유는 둘이고, 둘 다 «이번 회차의 제약»이다.**

1. **허용 경로** — 이번 작업의 허용 파일에 `src-tauri/Cargo.toml` 이 없다. 상류 권고대로 가려면
   `tauri.conf.json` 의 값을 살리고 **`Cargo.toml` 쪽을 그 값에 맞춰야** 하는데, 그 파일을 고칠 수 없다
2. **값 선택이 미결** — 두 값(`0.1.0` · `0.0.1`) 중 **어느 것이 맞는 판인지 정해진 바가 없다.**
   한쪽을 고르는 것은 판 번호 정책 결정이고, 이 Phase 가 할 일이 아니다

그래서 **값을 고르지 않고 출처를 하나로 만드는** 쪽을 택했다 — 지금의 불일치(§3)는 확실히 닫히고,
정책 결정은 열어 둔다.

> **Phase 8 이 판 번호 정책을 다시 본다.** 그때 정할 것은 ① 첫 배포판의 판 번호 ②
> **상류 권고대로 `tauri.conf.json` 관리로 되돌릴지**(그러면 `Cargo.toml` 과 동기화 수단이 필요하다)
> ③ 코드 태그와의 묶는 방식이다. **이번 선택은 잠정이고, 되돌리는 비용은 한 줄이다.**

---

## 4. 추가한 검증 — `make shell-verify`

`frontend/scripts/verify-shell-build.mjs`. **읽고 대조만 한다** — 굽지도, 설치하지도 않으므로
**몇 번을 돌려도 안전**하다.

| # | 재는 것 | 왜 |
|---|---|---|
| 1 | **판 번호 단일 출처** — `Cargo.toml` → `tauri.conf`(version 미기재) → `shell_info`(`CARGO_PKG_VERSION`) | §3 의 결함이 되돌아오면 여기서 붉어진다. `tauri.conf` 에 version 이 «있는데 다르면» 실패 |
| 2 | **코드 태그 대조**(선택) | `make shell-verify SHELL_TAG=v0.0.1` — 태그를 **만들지 않고** 주어진 값과 비교만 한다 |
| 3 | **양 플랫폼 번들 타깃** | macOS(`app`·`dmg`) · Windows(`msi`·`nsis`). `"all"` 이면 둘 다 포함으로 인정 |
| 4 | **아이콘 실재 + 형식** | 목록에 있는데 파일이 없으면 번들이 거기서 멈춘다. PNG/ICO 매직바이트까지 본다 |
| 5 | **원격 문서 계약 보존** | `frontendDist: shell-noop` · `app.windows: []` · `withGlobalTauri: false` · **셸이 CSP 를 박지 않음** |
| 6 | **권한 경계** | capability `local:false` · `remote.urls` 하나 · 와일드카드 서브도메인 없음 · 권한 정확히 넷 |
| 7 | **식별자** | 참조 제품(`com.kknaks.task-management`)과 겹치지 않음(AC-T34) |

**플랫폼을 섞지 않는다.** 스크립트가 끝에 이 호스트에서 **구울 수 있는 것과 없는 것**을 갈라 적는다:

```text
⚠ 이 호스트(darwin)에서 구울 수 있는 것: macOS(app·dmg).
  Windows(msi·nsis) 는 **이 기기에서 검증 불가** — 다른 쪽 결과로 대체하지 않는다
```

### ⚠ 「문제 0건」은 「빌드 가능」이 아니다 — strict 모드

이 스크립트가 **못 재는 것**(`.icns` 부재가 실제 번들을 막는지 · 다른 플랫폼 번들)은
**«검증 불가»로 따로 센다.** 기본 모드는 그 수를 찍고 **경고**로 두고,
**strict 모드는 그것을 실패로 올린다** — 「0건이니 구우면 된다」는 오독을 막기 위해서다.

```bash
make shell-verify            # 구성 미비는 경고 · 호스트 한계는 정보 (exit 0)
make shell-verify-strict     # **구성 미비만** 실패로 승격 (exit != 0)
SHELL_STRICT=1 make shell-verify   # 위와 같다
SHELL_TAG=v0.0.1 SHELL_STRICT=1 make shell-verify   # 판 번호 + 구성, 한 번에
```

**태그와 strict 를 함께 거는 목적**: 발행 직전에 확인할 것이 둘이기 때문이다 —
「**이 판 번호가 맞는가**」(태그 ↔ `Cargo.toml` ↔ `shell_info`)와 「**구성이 갖춰졌는가**」
(아이콘·번들 타깃·권한 경계). 따로 돌리면 한쪽만 보고 넘어가기 쉬워, **발행 관문에서는 이 조합**을 쓴다.

> **못 재는 것은 두 종류다.** **구성 미비**(채우면 사라진다 — 예: `.icns` 부재)는 strict 가 실패로
> 올리고, **호스트 한계**(이 기기가 다른 플랫폼을 못 굽는다)는 어느 모드에서도 **정보**다.
> 후자를 승격하면 strict 가 영원히 붉어 경보로서 죽는다. **다만 못 구운 플랫폼을 «검증됐다»고
> 쓰지 않는 금지는 그대로다.**

**판정을 바꾸는 것은 «모드»이지 관측이 아니다** — 두 모드가 같은 것을 재고, 검증 불가 항목의
내용도 같다. 다른 것은 **그것을 통과로 볼 것인가**뿐이다. fixture/운영 판을 굽기 직전의 관문으로는
**strict** 를 쓴다.

---

## 5. fixture 판 절차 — `make shell-build-fixture`

`frontend/scripts/build-shell-fixture.mjs`. **기본이 dry-run 이라 굽지 않는다.**

```bash
make shell-build-fixture SHELL_FIXTURE_ORIGIN=https://<fixture-host>            # 점검 + 명령 출력
make shell-build-fixture SHELL_FIXTURE_ORIGIN=https://<fixture-host> SHELL_BUILD=1  # 실제 빌드(호스트 플랫폼만)
```

### 5-1. 굽기 «전»에 두 곳이 같은지 본다

셸이 여는 주소는 **두 파일**이 함께 정한다. 어긋나면 **창은 뜨는데 커맨드가 ACL 에서 거절된다**(`E-06`) —
구운 뒤에야 알게 되는 종류의 실수다.

| 파일 | 자리 |
|---|---|
| `src-tauri/shell.config.json` | `operationalOrigin` — 창이 여는 곳 |
| `src-tauri/capabilities/product-shell.json` | `remote.urls` — 커맨드를 쓸 수 있는 origin |

**스크립트는 이 둘을 고치지 않는다.** 어긋나 있으면 무엇을 어디에 쓸지 알려 주고 **멈춘다** —
**주소를 지어내지 않는다**(OQ-T02). 실제 동작:

```text
== 주소가 아직 이 fixture 판의 것이 아니다 ==
  ✗ shell.config.json · operationalOrigin = null
  ✗ capabilities/product-shell.json · remote.urls[0] = https://operational-origin-not-yet-decided.invalid/*
  1) src-tauri/shell.config.json          "operationalOrigin": "<요청한 origin>"
  2) src-tauri/capabilities/product-shell.json  "remote.urls": ["<요청한 origin>/*"]
```

`--origin` 은 **https 만** 받는다 — 마이크는 secure context 에서만 열리므로 fixture 도 같은 조건이어야 한다.

### 5-2. 판 두 개를 만드는 법 (M-10 용)

M-10(재설치·판 올림 뒤 쿠키 유지, AC-T35)은 **판이 둘** 필요하다. 판 번호의 단일 출처가
`Cargo.toml` 이므로 절차는 이렇게 된다:

1. **1판** — 현재 판(`0.0.1`)을 굽고 **사람이 설치** → 로그인
2. `src-tauri/Cargo.toml` 의 `[package] version` **한 줄을 올린다**
3. **2판** — 다시 굽고 **덮어 설치** → 쿠키가 남아 로그인이 유지되는지 본다
4. ⚠ **식별자는 그대로 둔다** — 바꾸면 웹뷰 저장소가 새로 잡혀 **그것 때문에** 로그아웃된다

> **스크립트가 `Cargo.toml` 을 대신 고치지 않는다.** 판 번호를 올리는 것은 기록에 남아야 하는
> 결정이고, 그 파일은 이번 허용 경로도 아니다.

---

## 6. 실행한 검증

| # | 명령 | 결과 |
|---|---|---|
| V-1 | `make shell-verify` | **exit 0** · 문제 **0건** · **구성 미비 1건**(경고) · **호스트 한계 1건**(정보) — 「빌드 가능」을 뜻하지 않는다 |
| V-1b | `make shell-verify-strict` · `SHELL_STRICT=1 make shell-verify` | **exit != 0** — **구성 미비 1건만 실패로 승격**한다. **호스트 한계 1건은 정보로 남는다**(승격하면 이 기기에서 strict 가 영원히 붉다) |
| V-2 | `make shell-verify SHELL_TAG=v0.0.1` | 「코드 태그 v0.0.1 가 판 번호 0.0.1 와 같다」 |
| V-3 | `make shell-verify SHELL_TAG=v9.9.9` | **exit 2** — 불일치를 실제로 잡는다(검증기가 검증된다) |
| V-4 | `make shell-build-fixture`(인자 없이) | **exit 2** — origin 을 요구하고 멈춘다 |
| V-5 | `make shell-build-fixture SHELL_FIXTURE_ORIGIN=https://fixture.example.invalid` | **거부 + 안내**(§5-1). **굽지 않았다** |
| V-6 | `cargo check --all-targets` (`src-tauri`) | **warning 0 · error 0** |
| V-7 | `cargo test` (`src-tauri`) | **45 passed · 0 failed** — `tauri.conf` 변경 뒤 context 재생성 포함 |
| V-8 | `cargo clippy --all-targets -- -D warnings` | **통과** |
| V-9 | `npx tsc --noEmit` | **통과**(출력 0줄) |
| V-10 | `make frontend-test` | **exit 0 · 1053 passed** |

- **JSON 검증**: `tauri.conf.json` · `shell.config.json` · capability 를 `JSON.parse` 로 읽어
  구조까지 대조한다(V-1 에 포함). 별도 schema validator 는 도입하지 않았다 —
  `$schema` 가 가리키는 파일은 `@tauri-apps/cli` 안에 있고, 그 검증은 `tauri build`/`cargo` 가 한다
- **실제 빌드는 하지 않았다.** `cargo check`·`cargo test`·`clippy` 는 **컴파일 검사**이지
  설치파일 생성이 아니다

---

## 7. 구분해 적는 것 — 무엇이 «안» 됐나

| 항목 | 상태 | 사유 |
|---|---|---|
| **실제 설치파일 생성** | **하지 않음** | 발주가 fixture 판을 Release 대상에서 제외했고, 굽기 전에 fixture origin(§5-1)이 먼저 필요하다 |
| **Windows 축 전부** | **검증 불가(이 기기)** | Windows 실기가 없고, 교차 컴파일도 `llvm-rc` 부재로 막혀 있다(Phase 3·5 에서 확인). **macOS 결과로 대체하지 않는다** |
| **M-10**(재설치·판 올림 쿠키 유지) | **미측정** | 사람이 **설치**해야 한다. 절차만 §5-2 에 적었다. **정적 검증을 실기 통과로 쓰지 않는다** |
| **macOS `.icns` 아이콘** | **없음(경고로 표시)** | 번들 단계에서 필요할 수 있다. 제품 아이콘 자체가 아직 자리표시이고 Phase 7 범위 밖이라 **만들지 않았다** — 스크립트가 매번 경고한다 |
| **운영 origin · 도메인** | **미정** | OQ-T02. placeholder 그대로 두었다 |
| **서명 · 공증 · 자동업데이트 · CI 러너** | **없음** | 발주 금지. 계승할 선례도 0건(OQ-T03) |
| **최소 OS 버전** | **미정** | OQ-T01. 발명하지 않았다 |
| **Phase 6b D-4**(PRODUCTION 로그인 수단) | **미결 유지** | 이번 작업이 건드리지 않았다 |

---

## 8. 남은 것 / 다음 단계

| # | 내용 | 주인 |
|---|---|---|
| 1 | **fixture origin 확정** → `shell.config.json` · capability 두 곳을 같은 값으로 | 사용자·코디(OQ-T02) |
| 2 | **macOS `.icns` 포함한 제품 아이콘 세트** — 지금은 자리표시 | Phase 7 후속/8 |
| 3 | **판 번호 정책** — `0.0.1` 을 그대로 갈지, 첫 배포판으로 올릴지 | 코디 |
| 4 | **M-10 실기** — 1판 설치 → 로그인 → 판 올림 → 덮어 설치 → 쿠키 유지 확인 | 사용자 |
| 5 | **Windows 실기/빌드 환경** | OQ-W01 |

---

## 9. 금지 사항 준수

| 금지 | 확인 |
|---|---|
| 운영 서버·인프라 레포 변경 | **0줄** — 이번 회차에 열지도 않았다 |
| Release · 태그 · push · 커밋 | 하지 않았다. HEAD `a1f6791` 그대로 |
| 비밀값 조회 | 하지 않았다 |
| 사용자 기기 설치 | **하지 않았다.** 두 스크립트 모두 설치 동작이 없고, 빌드도 기본 dry-run 이다 |
| 로그인·권한 구현 변경 | `src-tauri/src/**` · backend **0줄** |
| 확인하지 않은 설치 성공 주장 | 없다 — §7 이 「안 된 것」을 항목별로 적는다 |
