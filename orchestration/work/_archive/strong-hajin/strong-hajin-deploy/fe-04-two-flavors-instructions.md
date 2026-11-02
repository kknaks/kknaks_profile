# [frontend 3차 정정] 앱은 두 판 — 개인용 / 회사용 (2026-10-01, 사용자 지시) — fe-03 을 이걸로 대체

| 판 | 이름(보이는 것) | identifier | origin |
|---|---|---|---|
| 개인용 | Strong Hajin | `app.stronghajin.desktop` | **미정** — 발명 금지 |
| **회사용 (지금 만드는 것)** | `medi-ax` | `app.ax.desktop` | `https://ax.medisolveai.xyz` |

## 할 것
1. 판을 설정으로 가른다 — 코드 한 벌에 판별 설정 파일. 기본(`tauri.conf.json`)을 어느 판으로 둘지, 오버레이(`tauri.<판>.conf.json` + `tauri build --config`)와 판별 shell 설정(origin·capabilities)을 어떻게 싣는지는 **현재 코드가 shell.config·capabilities 를 읽는 방식에 맞춰** 네가 설계하고 리포트에 근거를 적어라. `make` 타깃이 판 이름을 받게(예: `SHELL_FLAVOR=medi-ax`)
2. 개인판은 origin 이 없으므로 「서버 주소가 설정되지 않았습니다」 화면이 뜨는 현행 동작을 유지(null). 회사판에만 ax origin
3. 「identifier 는 고정」 시험·안내(`lib.rs:632`, `build-shell-fixture.mjs:115`)는 「판마다 고정」으로 바꾼다 — 판 안에서 바뀌면 로그아웃된다는 뜻은 그대로
4. fe-03 의 이름 전수(창 제목·productName·셸 화면 문구·Info.plist·dmg 볼륨)를 **회사판에서** medi-ax 로. 개인판은 Strong Hajin 유지
5. 회사판 빌드 → Developer ID 서명 → 공증(AC_NOTARY) → staple → spctl → `~/Downloads/medi-ax_0.0.1_arm64.dmg`. `.app` Info.plist 의 CFBundleIdentifier=app.ax.desktop · CFBundleName=medi-ax 확인
6. 개인판은 빌드만 가능한지 `cargo check`/설정 검증까지(dmg 불필요)
7. `cargo test` · `make shell-verify-strict`(두 판 모두) 통과. 리포트 `report-fe-flavors.md`. 커밋 금지, 두 채널 보고

참고: 사용자 Mac 의 `/Applications/Strong Hajin.app` 은 9/30 로컬 ad-hoc 판(127.0.0.1, 서명 깨짐)이다 — 건드리지 마라.
