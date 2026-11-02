# report-fe-flavors — 앱 두 판(개인 Strong Hajin / 회사 medi-ax) · 회사판 서명·공증 (2026-10-01)

브랜치 `kknaksss/strong-hajin-medi-ax` (origin/main e575194 기준) · 커밋·push·Release 없음.
fe-03(이름만 medi-ax 로 바꾸기) 작업은 fe-04 로 대체했다. fe-03 편집은 되돌렸고, 그때 `~/Downloads/medi-ax_0.0.1_arm64.dmg` 에 넣었던 판(identifier 가 app.stronghajin.desktop 이던 것)은 **이번 회사판으로 덮어썼다**.

## 1. 설계 — 코드 한 벌, 판마다 설정 한 폴더
```
frontend/src-tauri/
  tauri.conf.json                      공통 설정. 기본판(개인판) 이름·identifier 를 그대로 갖는다
  flavors/strong-hajin/                개인판(기본)
    tauri.conf.json                    오버레이: productName "Strong Hajin" · identifier app.stronghajin.desktop
    shell.config.json                  operationalOrigin: null → 「서버 주소가 설정되지 않았습니다」 (현행 유지)
    capabilities/product-shell.json    remote.urls: https://operational-origin-not-yet-decided.invalid/*
  flavors/medi-ax/                     회사판
    tauri.conf.json                    오버레이: productName/mainBinaryName "medi-ax" · identifier app.ax.desktop
    shell.config.json                  operationalOrigin: https://ax.medisolveai.xyz
    capabilities/product-shell.json    remote.urls: https://ax.medisolveai.xyz/*
```
**왜 이 방식인가 (현재 코드가 설정을 읽는 방식에 맞춤)**
- `shell.config.json` 은 Rust 가 **컴파일할 때 `include_str!`** 로 싣는다. 그래서 `tauri build --config` 오버레이만으로는 주소를 바꿀 수 없다(`run-tauri-local.mjs` 주석이 같은 이유로 임시 복사본을 쓴다). → build.rs 가 `cargo:rustc-env=SHELL_FLAVOR=<판>` 을 내보내고, 소스는 `include_str!(concat!("../flavors/", env!("SHELL_FLAVOR"), "/shell.config.json"))` 로 그 판의 파일을 싣는다.
- capability 는 tauri-build 가 읽는다. 여기에 `Attributes::capabilities_path_pattern("./flavors/<판>/capabilities/**/*")` 를 준다(tauri-build 2.6.3 API. `removeUnusedCommands` 는 쓰지 않아 제약이 없다).
- 이름·identifier 는 Tauri 가 공식으로 지원하는 `--config` 오버레이(JSON merge patch)로 얹는다. 오버레이에 들어갈 수 있는 키는 `productName`·`mainBinaryName`·`identifier` 셋뿐이고, 시험과 verify 둘 다 이를 강제한다. 권한·창·번들 구성은 판과 무관하게 공통이다.
- **판을 가리는 두 손잡이(`--config` 오버레이, `SHELL_FLAVOR`)를 build.rs 가 서로 대조한다**:
  - CLI 빌드: CLI 가 `TAURI_CONFIG` 로 오버레이를 싣는다 → build.rs 가 그 identifier 로 판을 찾는다. `SHELL_FLAVOR` 가 다른 판이거나 오버레이 값이 덜 실렸으면 **빌드를 멈춘다**.
  - `cargo check`/`cargo test`: `TAURI_CONFIG` 가 없다 → build.rs 가 `SHELL_FLAVOR`(없으면 기본판)의 오버레이를 `TAURI_CONFIG` 로 싣는다. tauri-build 에는 `set_var` 로, `generate_context!` 에는 `rustc-env` 로 준다.
  - CLI 빌드인데 `--config` 가 없고 판이 기본판이 아니면 **멈춘다**. CLI 는 cargo 에 `TAURI_CLI_VERBOSITY` 를 주므로 이걸로 알아본다(실측 확인). 이 경우를 그냥 두면 Info.plist 는 개인판, 실행 파일은 회사판이 된다.
  - 가드 실측(모두 빌드가 멈춤): 「--config 는 medi-ax, SHELL_FLAVOR 는 strong-hajin」 → 「판이 갈렸다」 / 오버레이에서 mainBinaryName 누락 → 「실린 설정과 다르다」 / `SHELL_FLAVOR=nope` → 「그런 판이 없다」 / `SHELL_FLAVOR=medi-ax npx tauri build`(--config 없음) → 「--config 가 없다」
- 기본판을 **개인판**으로 둔 이유: 오버레이 없이 도는 `cargo test`·`tauri dev`·`make tauri-local` 은 기본판을 쓴다. 기본판이 주소 미정(null)이면 회사 주소를 실수로 싣고 구울 길이 없다(OQ-T02 「발명 금지」). 회사판은 명시해야만 나온다.

## 2. make — 모든 shell-* 타깃이 `SHELL_FLAVOR` 를 받는다(기본 strong-hajin)
- `make shell-verify[-strict] SHELL_FLAVOR=medi-ax`
- **신규** `make shell-build SHELL_FLAVOR=medi-ax SHELL_BUILD_ARGS="--bundles app,dmg"`: strict 검증을 먼저 돌리고, 통과하면 `SHELL_FLAVOR` 와 `--config flavors/<판>/tauri.conf.json` 를 함께 넘겨 굽는다. 서명은 `APPLE_SIGNING_IDENTITY` 를 환경으로 주면 된다.
- `shell-build-fixture` · `shell-final-preflight` · `shell-release-preflight` · `tauri-local` 도 판을 받는다.

## 3. 파일
| 파일 | 변경 |
|---|---|
| `src-tauri/build.rs` | 판을 정하는 로직과 가드 추가, capabilities 경로 패턴 지정 |
| `src-tauri/Cargo.toml` | build-dep `serde_json`(lock 에 이미 있어 lock 은 안 바뀜). description 에서 제품 이름 제거(바이너리에 실리므로) |
| `src-tauri/src/config.rs` | `include_str!` 경로를 판별로. `CONFIG_SLOT` = `flavors/<판>/shell.config.json · operationalOrigin`(미설정 화면에 보이는 문구). 시험을 「판마다 실린 주소」로 교체 |
| `src-tauri/src/lib.rs` | 창 제목을 `app.package_info().name`(= 판의 productName)으로 바꿔 이름을 한 곳에만 둔다. 시험: identifier **판마다 고정**(개인 app.stronghajin.desktop · 회사 app.ax.desktop · 기본 conf = 개인판), 오버레이 키 셋 제한, 판별 origin·capability 일치 |
| `src-tauri/shell-noop/index.html` | `<title>` 을 `shell-noop` 으로 바꿔 제품 이름을 뺐다(두 판이 함께 싣는 파일이고, 화면에 뜨지 않는다) |
| `src-tauri/flavors/**` | 신규. medi-ax 의 shell.config·capability 는 기존 파일을 `git mv` 한 것(staged rename). strong-hajin 쪽은 #7 이전 값(null·.invalid)을 되살린 것 |
| `scripts/shell-flavor.mjs` | 신규 공용 헬퍼: 판 이름 결정, 경로 계산, 오버레이 merge |
| `scripts/verify-shell-build.mjs` | 판별로 읽게 바꿈. 추가 검사: 오버레이 키 · 판끼리 identifier 중복 · 기본 conf 와 기본판 일치 · 같은 판 안에서 shell.config 와 capability 의 origin 일치 · 주소가 null 인데 capability 가 실주소인 경우 |
| `scripts/verify-final-build.mjs` | 판별로 읽게 바꿈. manifest 에 `flavor` 추가, identifier 는 판의 것. 아티팩트는 **이 판 productName 으로 시작하는 것만** 해시한다(번들 폴더를 두 판이 같이 씀) |
| `scripts/verify-release-artifact.mjs` | manifest 의 `flavor` 로 트리를 읽는다. 조합 대조에 identifier 추가 |
| `scripts/build-shell-fixture.mjs` | 판별로 바꿈. 안내 문구 「식별자는 판마다 고정」. 빌드 명령 = `npx tauri build --config <오버레이>` + `SHELL_FLAVOR` |
| `scripts/run-tauri-local.mjs` | 임시 복사본에서도 그 판의 파일만 고치고, `--config` 와 `SHELL_FLAVOR` 를 넘긴다 |
| `Makefile` | 위 §2 |

## 4. 이름 전수 (회사판 medi-ax / 개인판 Strong Hajin)
| 자리 | 회사판 결과 |
|---|---|
| productName → CFBundleName·CFBundleDisplayName·dmg 볼륨·dmg 파일명·macOS 메뉴(About/Quit/Hide) | medi-ax (볼륨 `/Volumes/medi-ax` 실측) |
| 실행 파일 이름(`mainBinaryName`) | `Contents/MacOS/medi-ax` (개인판은 전처럼 crate 이름 `strong-hajin-shell`) |
| 창 제목 | productName 을 그대로 쓴다 → medi-ax |
| 셸 자기 화면(연결 오류·미설정) | 제품 이름 없음. 미설정 화면의 설정 자리 문구만 판 경로로 바뀜 |
| Info.plist (NSMicrophoneUsageDescription) | 제품 이름 없음 → 수정 없음 |
| shell-noop `<title>` | 두 판 공통 파일이라 이름을 뺌 |
| Cargo description(바이너리에 실림) | 이름을 뺌 |

회사판 바이너리를 strings 로 확인: `Strong Hajin` 0 · `app.stronghajin.desktop` 0 · `.invalid` 자리표시 0 · `app.ax.desktop` 있음 · ax origin 있음 · `flavors/medi-ax/shell.config.json` 있음.
개인판 바이너리(`--config strong-hajin` 로 CLI 빌드): `app.ax.desktop` 0 · ax origin 0 · `app.stronghajin.desktop` 있음 · `.invalid` 있음.

**바꾸지 않은 것과 이유**: `stronghajin://` 스킴과 crate 이름 `strong-hajin-shell` 은 브리프대로 두었다(내부 이름이고 회사판에서도 사용자에게 보이지 않는다. 실행 파일 이름은 mainBinaryName 으로 medi-ax). 주석·레포·차트 이름도 그대로다. `deploy/k8s/*.Dockerfile` 주석은 이 작업 범위(infra)가 아니라 손대지 않았다.

## 5. 검증
- `cargo test`: 기본판 46 passed · `SHELL_FLAVOR=medi-ax cargo test` 46 passed
- `cargo check`(개인판·기본) 통과
- `make shell-verify-strict`: 개인판 통과 · `SHELL_FLAVOR=medi-ax` 통과
- `verify-final-build --flavor medi-ax --evidence fe-02-final-evidence.json` → exit 1, **M-5 한 건만 막힘**(G1~G4 일치 · manifest 에 flavor=medi-ax · identifier=app.ax.desktop · dmg sha256 기록). 출력: `fe-04-preflight.txt`
- 개인판 preflight 는 G2(null)·G3(.invalid)·G5 로 막힌다 — 의도한 대로(주소 미정)
- `node --check` 로 scripts/*.mjs 문법 확인
- 서브명령 `cargo fmt --check` 는 이 작업 전부터 guard.rs·power.rs 에서 diff 가 난다(저장소가 rustfmt 를 강제하지 않음). 그래서 새로 쓴 build.rs 만 rustfmt 했다

## 6. 회사판 빌드·서명·공증
- `CI=true APPLE_SIGNING_IDENTITY="Developer ID Application: keonhak lee (UYQF47UCVR)" make shell-build SHELL_FLAVOR=medi-ax SHELL_BUILD_ARGS="--bundles app,dmg"`
  - `CI=true` 는 fe-02 와 같은 이유다. 헤드리스라 Finder 로 dmg 창을 꾸미는 단계가 막혀 그 단계를 건너뛰었다
- .app 의 PlistBuddy 값: CFBundleName=medi-ax · CFBundleDisplayName=medi-ax · CFBundleExecutable=medi-ax · **CFBundleIdentifier=app.ax.desktop** · 0.0.1
- codesign: Identifier=app.ax.desktop · `flags=0x10000(runtime)` · Developer ID Application (UYQF47UCVR) · audio-input entitlement
- notarytool: `dbf66f10-9fcf-46f4-bf5f-05295a766456` **Accepted**, 로그 issues 없음 (`fe-04-notary.txt`)
- stapler: dmg · .app 둘 다 「The staple and validate action worked!」
- spctl `accepted source=Notarized Developer ID`: dmg(install) · .app(exec) · dmg 안에 마운트된 .app · Downloads 사본
- **산출물** `~/Downloads/medi-ax_0.0.1_arm64.dmg` — 3,985,621 bytes, sha256 `7e9ec4604829c4b04a89734c4b791cc7223a9b302730a2880b54d4b84019e92c`
- 남겨 둔 것: `StrongHajin_0.0.1_arm64.dmg`(fe-02) · `Strong Hajin_0.0.1_aarch64_local.dmg`. `/Applications/Strong Hajin.app` 은 건드리지 않았다

## 7. 미결·주의
- **M-5 pending**: 사용자가 medi-ax dmg 를 설치해 로그인→종료→재실행으로 확인한다. identifier 가 app.ax.desktop 으로 바뀌어 **저장소가 새로 잡히므로**, fe-02 판(StrongHajin dmg)에서 했던 로그인은 이어지지 않는다. 한 번 새로 로그인해야 한다
- fe-02 판(`StrongHajin_0.0.1_arm64.dmg`, identifier app.stronghajin.desktop + ax origin)은 이제 **어느 판에도 속하지 않는 조합**이다. 배포하지 말 것
- dmg 창 꾸밈(배경·아이콘 배치) 없음 — 헤드리스 한계
- 스테이징: `git mv` 두 건이 staged rename 으로 잡혀 있다(커밋 안 함)
