# report-fe-release-dmg — 운영 origin dmg · Developer ID 서명 · 공증 (2026-10-01)

브랜치 `kknaksss/strong-hajin-origin` (origin/main b0eb4b4 기준) · 커밋·push·Release·태그 없음

## 1. 바뀐 파일 (주소를 쓰는 곳 grep: `operational-origin-not-yet-decided` · `operationalOrigin` · `.invalid`)
| 파일 | 변경 |
|---|---|
| `frontend/src-tauri/shell.config.json` | `operationalOrigin: "https://ax.medisolveai.xyz"` · `$comment` 의 «미정» 문구를 확정 문구로 |
| `frontend/src-tauri/capabilities/product-shell.json` | `remote.urls: ["https://ax.medisolveai.xyz/*"]` |
| `frontend/src-tauri/src/config.rs` | 자리표시를 고정하던 시험(「Phase 8 이 채우면 함께 바뀐다」 주석) → 확정 origin·allowlist 고정 시험으로 |
| `frontend/src-tauri/src/lib.rs` | `운영_origin_은_아직_자리로만_있다`(`.invalid` 단언) → `운영_origin_은_설정과_커맨드_허용이_같다`(capability = config origin + `/*`) |

grep 결과 주소를 쓰는 곳은 위 두 설정 파일뿐. 나머지 매치는 검증 스크립트(규칙)·config 파서 시험 픽스처·backend 무관 픽스처. `gen/schemas/capabilities.json` 은 추적되지 않는 빌드 생성물.

## 2. 검증
- `cargo test`(src-tauri): 46 passed
- `make shell-verify-strict`: 통과 (문제 0 · 구성 미비 0 · 호스트 한계 1=Windows)
- `node scripts/verify-final-build.mjs --origin https://ax.medisolveai.xyz --evidence fe-02-final-evidence.json` → **exit 1, 1건 막힘: G5 M-5** (지시대로 우회 안 함). 전체 출력 `fe-02-preflight.txt`
  - G1~G4 통과: 입력·shell.config·capability 모두 `https://ax.medisolveai.xyz`
  - 증거 `fe-02-final-evidence.json` (실측만):
    - D-4: `/api/auth/providers` → `{"local":true,"oidc":false}` + 사용자 웹 로그인 성공(코디 전달)
    - 서버 실재: `curl /` → 200
    - M-1: `curl -v` → TLSv1.3, CN=medisolveai.xyz, SAN `*.medisolveai.xyz` 일치, issuer Google Trust Services WE1, 2026-08-30~**2026-11-28**, `SSL certificate verify ok`
    - M-5: **pending** — 서명본을 사용자가 설치해 로그인→종료→재실행으로 확인
- ⚠ 관문이 M-5 로 막힌 상태에서 빌드했다 — M-5 확인에 서명본이 필요하다는 지시(§2·§3)에 따른 것. 사용자가 M-5 를 확인하면 증거 파일에 `resolved:true` 로 적고 preflight 를 다시 돌리면 manifest 가 확정된다(dmg sha256 은 이미 manifest 에 잡힘).

## 3. 빌드·서명·공증
- `CI=true APPLE_SIGNING_IDENTITY="Developer ID Application: keonhak lee (UYQF47UCVR)" npx tauri build --bundles app,dmg`
  - 첫 시도는 `bundle_dmg.sh` 실패 — 헤드리스에서 Finder AppleScript(창 꾸미기) 단계가 막힘. `CI=true` 로 그 단계만 건너뜀 → dmg 창 배경/아이콘 배치 꾸밈이 없는 기본 레이아웃(`Strong Hajin.app` + `Applications` 링크는 있음)
- `.app` codesign: Authority=Developer ID Application (UYQF47UCVR), `flags=0x10000(runtime)` = hardened runtime, 보안 타임스탬프, entitlement `com.apple.security.device.audio-input`
- dmg 도 같은 identity 로 서명됨(tauri)
- `xcrun notarytool submit … --keychain-profile AC_NOTARY --wait` → submission `44183044-06d8-4146-a4c4-accc6878ca04` **Accepted**, 로그 issues 없음 (`fe-02-notary.txt`)
- `xcrun stapler staple` dmg · .app 모두 「The staple and validate action worked!」
- `spctl -a -vvv -t install <dmg>` → `accepted source=Notarized Developer ID`
- `spctl -a -vvv -t exec <.app>` (target 쪽, dmg 안 마운트본 둘 다) → `accepted source=Notarized Developer ID`
- 바이너리에 `ax.medisolveai.xyz` 포함, `not-yet-decided` 없음(strings)

## 4. 산출물
- `~/Downloads/StrongHajin_0.0.1_arm64.dmg` — 3,986,199 bytes
- sha256 `3d90bbf0cd246e070bdaede6564ff7460c53e28bc0f67dad80633077d0a6aff8` (빌드 원본 `target/release/bundle/dmg/Strong Hajin_0.0.1_aarch64.dmg` 과 동일)
- 이전 `~/Downloads/Strong Hajin_0.0.1_aarch64_local.dmg` 는 그대로 둠

## 5. 미결·주의
- **M-5 pending** — 사용자 설치 후 확인 필요. preflight 는 그때까지 막혀 있다
- 인증서 만료 2026-11-28 (Google Trust Services 자동 갱신 가정 — infra 확인 몫)
- dmg 창 꾸밈 없음(헤드리스 한계). GUI 세션에서 `CI` 없이 구우면 꾸밈 포함되나 해시가 달라져 재공증 필요
- 비밀값·Apple ID 출력 없음
