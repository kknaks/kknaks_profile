# 버그 — 전체화면 나갔다 다시 들어가면 아래 빈 공간 (medi-ax 서명 dmg `3321504`)

## 상태: 고침 2곳(셸 · 화면) — **어느 쪽이 원인인지는 코디 실측으로 가른다**(§4) · 커밋 없음

- 브랜치 `kknaksss/strong-hajin-notify-label`(「메시지」 세 곳 정정과 같은 브랜치)
- 앱은 실행하지 않았다. 사용자 포트도 건드리지 않았다. 코드 · 크레이트 소스로만 갈랐다

## 1. 원인 가르기

### ① 셸(웹뷰) — 1순위 후보: wry 0.56 이 WKWebView 「요소 전체화면」 을 늘 켠다
- 이번 판에 tauri 2.11.6 → 2.12.1 로 올랐고, 그 아래가 함께 바뀌었다:

  | 크레이트 | 전 판(`d2a06fa` lock) | 지금 |
  |---|---|---|
  | wry | 0.55.1 | 0.57.0 |
  | tao | 0.35.3 | 0.37.1 |
  | tauri-runtime-wry | 2.11.4 | 2.12.1 |

- **wry 0.55.1 → 0.57.0 의 macOS 웹뷰 생성(`src/wkwebview/mod.rs`) 차이 전수**(로컬 crates 소스 diff):
  1. **`fullScreenEnabled`** — 0.55.1 은 `#[cfg(feature = "fullscreen")]` 일 때만 켰다. 0.57.0 은 **늘** 켠다 — macOS 12.3+ 는 공개 API `setElementFullscreenEnabled(true)`, 그 아래는 private KVC 다. CHANGELOG 0.56.0:
     - [#1779](https://github.com/tauri-apps/wry/pull/1779) 「Enable WebView element fullscreen support on macOS 12.3+」
     - [#1780](https://github.com/tauri-apps/wry/pull/1780) 「**Removed the macOS/iOS specific `transparent` and `fullscreen` feature flags. The functionalities are now always enabled.**」
  2. `drawsBackground` · iOS 색 — `attributes.transparent` 일 때만 실행되는 갈래다. 우리는 투명 창을 쓰지 않는다 → 무관
  3. 프레임 · `setAutoresizingMask`(비자식 웹뷰 = 폭·높이 자동) · 부모 뷰(`WryWebViewParent` 를 `contentView` 로) — **무변경**
- **전 판에서 그 값이 꺼져 있었다는 근거**: tauri-runtime-wry 2.11.4 `Cargo.toml` 은 `macos-private-api = ["wry/fullscreen", "wry/transparent", …]` 이다 — `wry/fullscreen` 은 그 기능일 때만 켜진다. 우리 `Cargo.toml` 의 `tauri` features 는 `[]` 이다(`macos-private-api` 없음) → **전 판은 꺼짐 · 지금은 켜짐**
- tao 0.35.3 → 0.37.1 의 macOS 차이: 전체화면을 나갈 때 신호등 단추 위치 다시 적용(`reapply_traffic_light_inset` — 위치를 지정한 창만 · 우리는 지정 없음) · `set_title_async` 인자 · `Lazy` → `LazyLock`. 창 · 뷰 크기 처리는 무변경
- tauri-runtime-wry 의 `Resized` 처리(`inner_size` 로 크기 사건)는 타입 정리뿐이고 동작은 같다
- **우리 셸 설정**: 창은 `spawn_main_window`(`T/src/lib.rs`) 한 곳에서 `inner_size(1280, 860)` 로 만든다. 전체화면 · 크기 관련 설정 · `tauri.conf.json` 창 설정은 없다(`app.windows: []`) — 바뀐 것이 없다
- 결론: 두 판 사이 **macOS 웹뷰 동작이 바뀐 곳은 「요소 전체화면 상시 켬」 하나**다. 창 전체화면(초록 단추)과 WKWebView 의 전체화면 지원이 얽히는 WebKit 쪽 이상 보고는 있다(아래 링크). 다만 이 증상(110px)과 정확히 같은 보고는 찾지 못했다 → **1순위 후보 · 실측으로 확정**
  - [Apple Forums 768688 — WKWebView breaks with isElementFullscreenEnabled set to true](https://developer.apple.com/forums/thread/768688)
  - [Apple Forums 725494 — WKWebView on Mac Autolayout crash after exiting full screen](https://developer.apple.com/forums/thread/725494)

### ② 화면(CSS) — 2순위 후보: 앱 셸이 `height:100vh`
- `F/styles/shell.css:70`(고치기 전) `.scax-app-shell{…height:100vh;overflow:hidden}` 이다. 문서 높이를 뷰포트 단위로 잡는다. 웹뷰가 창 크기 변화를 늦게 알리면 `vh` 가 옛 값에 머물 수 있다. 그러면 「문서가 창보다 짧고 사이드바 배경이 그 위에서 끊긴다」 는 증상과 맞는다
- `innerHeight` · `--app-height` 로 셸 높이를 JS 가 재는 자리는 **없다**(grep). `100vh` 는 다른 데서 모달 상한(`components.css:256,795,797`)과 로그인 화면(`screens-a.css:63` — 셸 밖)에만 쓴다
- 이 규칙은 **전 판에도 그대로**였다 — 전 판에서 안 났다면 이것만으로는 회귀를 설명하지 못한다. 그래서 2순위다

### ③ 전 판(2.11.6 · `d2a06fa`)에서 안 났는가
- 코드로는: CSS 는 같고, 셸 쪽 차이는 위 ①(요소 전체화면 꺼짐 → 켜짐)뿐이다 → **회귀라면 ① 쪽**
- 실행 확인은 코디·사용자 몫이다(§4-0)

## 2. 고친 것

| # | 자리 | 내용 |
|---|---|---|
| 셸 | `T/src/lib.rs:361` `restore_element_fullscreen_off` · 부르는 곳 `:708`(`spawn_main_window` — 부팅 창과 트레이 「열기」 가 같은 함수) | macOS 에서 창을 만든 뒤 `with_webview` 로 WKWebView `configuration.preferences` 에 **`setElementFullscreenEnabled: NO`**(존재를 `respondsToSelector` 로 묻고 부름) — **전 판 설정으로 되돌림**<br>• 웹은 요소 전체화면(`requestFullscreen`)을 쓰지 않는다(grep 0) — 잃는 기능이 없다<br>• 실패해도 창은 뜬다(로그만)<br>• macOS 12.3 미만은 공개 API 가 없어 손대지 않는다(wry 가 private 키로 켬 — 대상 기기 판이면 실측 기록) |
| 셸(진단) | `T/src/lib.rs:718` `WindowEvent::Resized` | `[shell][win] resized WxH fullscreen=Some(true/false)` 한 줄 — 실측 때 창 크기가 화면을 다 덮는지 가른다. 동작은 바꾸지 않는다 |
| 화면 | `F/styles/shell.css:72-73` | `html,body,#root{height:100%}` + `.scax-app-shell{height:100%}`(`100vh` 걷음) — 높이를 지금 레이아웃 뷰포트의 `%` 사슬로. 주석 `:161` 도 고침 |

⚠ **배포 경로가 다르다**:
- 셸 수정은 **새 dmg**(Rust)가 있어야 앱에 실린다
- CSS 수정은 **웹 배포**(앱은 운영 origin 의 웹을 연다)가 있어야 실린다
- 이 차이로 둘을 따로 실측할 수 있다(§4)

## 3. 시험

| 명령 | 결과 |
|---|---|
| `cd frontend/src-tauri && cargo test` | **82 passed**(+1 「제품_창은_macos_에서_요소_전체화면을_끈다」 — `spawn_main_window` 가 부르는지 · 공개 API 를 묻고 쓰는지 소스 단언) |
| `SHELL_FLAVOR=medi-ax cargo test --features kakao-collector` | **103 passed** · 6 ignored(기존 실기기 시험) |
| `cargo clippy --all-targets -- -D warnings`(두 판) | **경고 0** |
| `cd frontend && npx vitest run src/shell/AppShell.test.tsx --no-file-parallelism` | exit 0 · 1 passed(셸 틀 회귀 없음) |
| `npx tsc --noEmit` | 0 오류 |

- CSS 높이를 단언하는 vitest 를 시도했지만 넣지 않았다. 시험 환경이 CSS 를 빈 글자로 불러와서(`?raw` · `import.meta.glob` 모두 빈 값) 단언이 성립하지 않는다. CSS 는 jsdom 에서 레이아웃도 하지 않는다 — 실물 확인으로 갈음한다
- 웹뷰 실제 크기 · 전체화면 왕복은 단위 시험으로 잴 수 없다(§4)

## 4. 코디 실측 절차 (원인 확정 · macOS)

0. **(선택) 전 판 대조** — `d2a06fa` dmg(tauri 2.11.6)로 같은 왕복을 해서 나면 「회귀 아님」 · 안 나면 「회귀」
1. **셸만 바꾼 상태** — 이 브랜치로 medi-ax dmg 를 굽는다(웹은 운영 그대로 = CSS 옛것)
   - 실행 파일을 터미널에서 띄운다(`/Applications/medi-ax.app/Contents/MacOS/medi-ax`) — 로그 「WKWebView 요소 전체화면을 껐다(전 판 설정)」 가 보여야 한다
   - 홈에서 전체화면 → 나가기 → 다시 전체화면
   - **빈 공간이 없어지면 → 원인 ①(셸)** 확정. CSS 수정은 보험으로 남겨도 되고 걷어도 된다
2. 1에서 그대로면 — 터미널의 `resized …` 줄을 본다
   - 다시 전체화면일 때 `resized` 크기가 **화면 크기와 같다**(창은 다 덮었다) → 웹뷰 안쪽 문제 → **원인 ②(CSS `vh`)** 쪽. 웹을 배포하거나 `make tauri-local` 로 이 브랜치 웹을 열어 다시 왕복 → 없어지면 ② 확정
   - 크기가 **화면보다 작다** → 창/tao 쪽(전체화면 전환 사건 · 크기 알림). 그 수치와 함께 다시 발주
3. 결과(판 · 단계 · resized 수치)를 기록하면 남길 수정을 정한다

## 5. 미결

- 원인 확정은 §4 실측 뒤 — 지금은 「두 후보를 각각 고쳤고 배포 경로가 달라 따로 잴 수 있다」 까지다
- 판 고정(tauri 2.11 로 되돌리기)은 고르지 않았다. Windows 알림 플러그인이 2.12 를 요구하고(WP4 처분 ③), 바뀐 동작 하나만 되돌리는 쪽이 범위가 좁다
- strong-hajin 판도 같은 셸 코드다(두 판 공통) — 같은 실측을 권한다
