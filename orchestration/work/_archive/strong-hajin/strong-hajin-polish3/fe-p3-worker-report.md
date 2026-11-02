# fe-p3-worker-report — WORK-010 Phase 3 · 데스크톱 셸 · 첨부 응답을 파일로 저장

> frontend(셸) 워커 · 2026-10-04 · 워크트리 `strong-hajin-polish3`(HEAD `7f01c5b` = Phase 1 커밋 위) · **커밋·push 안 함**
> 결정 근거: `fe-p3-decision.md` §0(소스 확인) · §4(코디 답: B · ureq · eval+CustomEvent · 문구) · §5(코디 답: X)

## 1. 변경 파일

| 파일 | 무엇 |
|---|---|
| `frontend/src-tauri/src/download.rs` (새) | 판별(`is_api_request` = 같은 origin + `/api/`) · `Content-Disposition` 파싱(`filename*` UTF-8/ISO-8859-1 우선, `filename` 따옴표·이스케이프) · 파일 이름 정리(경로 조각 제거·예약 문자·숨김 `.`·200바이트) · 번호(`이름 (1).ext`) · `create_new` 로 자리 잡고 쓰기(실패 시 반쯤 쓴 파일 삭제) · ureq GET(쿠키·리다이렉트 0·native-tls+OS 루트) · 사건 스크립트 · 시험 13 |
| `frontend/src-tauri/src/lib.rs` | `on_navigation` 에 `/api/` 가로채기 · `on_new_window`(신규) · `on_download`(신규) · `take_over_api_link`(별도 스레드: `cookies_for_url` → fetch → 저장/알림) · `notify_download`(`eval` → DOM `CustomEvent`, 허용 origin 문서일 때만) · `Shell.downloads` 맵 · 머리 주석/`log_event` 주석 갱신 · 시험 1 추가(빌더에 훅 셋 · capability 에 `core:`/`fs:` 없음) |
| `frontend/src-tauri/Cargo.toml` · `Cargo.lock` | `ureq 3.4.2`(`default-features=false`, `native-tls-no-default`) 1개 — rustls·Mozilla 루트 묶음 없음 |
| `frontend/src/lib/shell.ts` | `SHELL_DOWNLOAD_EVENT = "strong-hajin:download"` · `ShellDownloadResult` · `onShellDownload(handler)`(셸 없으면 구독 안 함, 모양 다른 detail 버림) |
| `frontend/src/App.tsx` | `useEffect` 로 `onShellDownload` 구독 → `putNotice("success"|"error", …)` |
| `frontend/src/lib/labels.ts` | **끝에 덧붙이기만**: `shellDownload.saved(name)` 「다운로드 폴더에 저장했습니다: {이름}」 · `savedUnnamed` 「다운로드 폴더에 저장했습니다.」 · `failed` 「파일을 저장하지 못했습니다.」 |
| `frontend/src/lib/shell.test.ts` · `frontend/src/App.test.tsx` | 수신부 시험 4 · App 토스트 시험 1 |

capabilities · `tauri.conf.json` · `flavors/*` : **변경 0**.

## 2. 동작 (최종)

| 경로 | 셸이 하는 일 |
|---|---|
| 같은 origin `/api/…` 최상위 이동(같은 탭) | 이동 **취소** → 별도 스레드에서 쿠키 실어 GET → `attachment` 면 다운로드 폴더 저장 + 사건 / 아니면 **아무것도 안 함**(로그만) |
| `_blank` `/api/…` — macOS | WKWebView 가 새 창 이동도 `on_navigation` 을 먼저 지나므로 위와 같은 길(취소 → 두 번째 창 없음) |
| `_blank` `/api/…` — Windows | `on_new_window` → `Deny` + 같은 처리 |
| `_blank` 그 밖 | 지금 동작 유지: macOS `Deny`(핸들러가 없을 때 wry 가 nil 을 돌려준 것과 같다) · Windows `Allow`(WebView2 기본) |
| 웹뷰 자체 내려받기(표시 불가 형식·`<a download>`) | `on_download`: 다운로드 폴더 · 같은 규칙의 번호 · 끝나면 사건 |
| 다른 origin 이동 | 지금 그대로(`E-05` OS 브라우저) |

사건: `window.dispatchEvent(new CustomEvent("strong-hajin:download", {detail:{ok, filename}}))` — 경로·문구 없음.

## 3. 계약 체크 (WP Phase 3 · SPEC-006)

- [x] 첨부 응답은 파일로 저장 · 창 문서 안 바뀜(이동 취소 → `on_page_load Started`/L-09 안 돎) · 같은 origin 이동과 `_blank` 둘 다 — **코드·단위 시험까지. 실기 pending**
- [x] OS 다운로드 폴더(tauri `path().download_dir()`) · 대화상자 없음 · `filename*` UTF-8 · 같은 이름이면 `이름 (1).html`(시험 `같은_이름이_있으면_덮지_않고_번호를_붙인다`)
- [x] 성공(이름)/실패를 셸 → 웹 사건으로 · 웹이 기존 공통 토스트로(App 시험) · 셸 문구 0
- [x] Content-Disposition 으로 가를 수 없음을 먼저 코디에게 물음(§0 · §4 · §5)
- [x] 인라인 `_blank` 바꾸지 않음(OQ-T13 · X) — macOS·Windows 모두 inline 이면 다시 navigate 안 함
- [x] 두 판 모두 — 코드 한 벌, 판 차이는 `navigation_allowlist`(운영 origin)뿐. strong-hajin 판은 origin `null` → 허용 목록 비어 `/api/` 가로채기 0(시험 `셸이_받아_보는_것은_…` 의 빈 목록 단언)
- [x] 권한·플러그인 최소 — capabilities 변경 0 · 커맨드 넷 · 플러그인 추가 0 · crate 추가 1(ureq)

### capabilities 변경 보고
**없음.** 두 판 `product-shell.json` 권한 4개 그대로(`allow-shell-info` · `allow-wake-guard-acquire` · `allow-wake-guard-release` · `allow-open-external`). `core:event:*` 도 열지 않음(사건은 eval).

## 4. grep 으로 센 자리

| 패턴 (`src-tauri/src/*.rs`) | 기준선 `d1b5137` lib.rs | 결과 |
|---|---|---|
| `on_download\|on_new_window` | 0 | 6 |
| `is_api_request` | 0 | 7 |
| `notify_download` | 0 | 7 |
| `cookies_for_url` | 0 | 3 |
| `strong-hajin:download`(src + src-tauri/src) | 0 | 9 |
| capability permissions(두 판) | 4 / 4 | 4 / 4 |

## 5. 검증 (기준선 vs 결과)

| 검증 | 결과 |
|---|---|
| `cargo check` | 통과 |
| `cargo test` — `SHELL_FLAVOR=strong-hajin` / `medi-ax` | 기준선 46 → **60 passed / 0 failed**(두 판) |
| `cargo clippy --all-targets -- -D warnings`(두 판) | 통과 |
| `node scripts/verify-shell-build.mjs --flavor medi-ax/strong-hajin`(정적) | 문제 0 · 구성 미비 0 · 호스트 한계 1(기존) |
| `npx vitest run --no-file-parallelism src/lib/shell.test.ts src/App.test.tsx` | **50 passed**(셸 17 · App 33) |
| `npx tsc --noEmit` | 통과 |
| `cargo check --target x86_64-pc-windows-msvc` | **못 함** — 호스트에 `llvm-rc` 가 없어 `tauri-winres` 빌드 스크립트가 멈춤(변경과 무관). Windows 는 pending |
| macOS 실기 · Windows 실기 | **pending**(띄우지 않음 — 금지) |

## 6. 코디 실기 확인 절차 (macOS · `make local-stack` + `make tauri-local`, 또는 운영 medi-ax) — *fix1 보강*

미리: Finder 에서 다운로드 폴더를 열어 둔다. 셸 로그(`[shell][download] …`)를 터미널에서 본다. 판정 칸이 있는 항목은 **눈으로 보고 통과/실패를 적는다.**

1. **회의 내보내기 (AC-T44 · AC-T49)** — 회의 상세 → 「내보내기」
   - 기대: 다운로드 폴더에 `{회의 제목}.html` · 앱 창은 **회의 상세 그대로** · 토스트 「다운로드 폴더에 저장했습니다: {회의 제목}.html」 · 로그 `saved via=navigation`
   - 한 번 더 누른다 → `{회의 제목} (1).html` · 토스트에 `(1)` 이 붙은 이름
   - 녹음 중이었다면 점유가 풀리지 않는다(로그에 `cleanup … document-replaced` 가 **없어야** 한다)
   - **격리 표식(W1)**: `xattr -l ~/Downloads/'{회의 제목}.html'` → `com.apple.quarantine: 0081;…;medi-ax;` 줄이 있어야 한다(없으면 셸 로그에 `격리 표식을 달지 못했다` 가 있는지 함께 적는다 — 저장 자체는 성공이어야 한다)
2. **업무 자료 첨부 `_blank` (AC-T45)** — 업무 상세 → 참고/결과 자료 링크(요청 첨부도 같은 길)
   - 기대: 파일이 다운로드 폴더에 저장 · 앱 창 그대로 · **두 번째 창 없음** · 성공 토스트 · 로그 `saved via=navigation`(macOS 는 `_blank` 도 이 길) · `xattr -l` 로 격리 표식
3. **회의 자료 서랍 — PDF 미리보기 [판정 · W4]** — 회의 상세 → 자료 서랍에서 PDF 자료를 연다
   - **판정 ①**: 서랍 안 PDF **미리보기(`<object>`)가 그려지는가.** 빈칸이면 **실패** → 로그에 같은 시각 `not-attachment via=navigation path=/api/meetings/…/materials/…/content` 가 찍혔는지 함께 적는다(찍혔으면 하위 프레임 이동이 가로채진 것 — §8 W4 고침 후보로 재발주)
   - 판정 ②: 같은 서랍의 「내려받기」 링크(PDF·Markdown = inline) → **아무 일도 없음**이 기대(알려진 차이 1) · 로그 `not-attachment … status=200 — 그대로 둔다`
4. **채팅 근거 「원본 열기」 · AX 답변 안 `/api/…/content` 링크 (inline `_blank` · OQ-T13 기록)**
   - 기대: 응답이 inline 이면 아무 일 없음(지금과 같음) · 첨부면 저장 + 토스트. **앱 화면을 덮는지 기록**한다(덮으면 실패 — 사용자에게 다시 묻기)
5. **실패 토스트 — 필수 [판정 · W2]** 아래 둘 중 **최소 하나**를 재현한다
   - 5a **세션 만료**: 앱에서 로그인한 채로, 서버 쪽에서 그 세션만 지운다. 세션은 DB 표 `auth_sessions`(쿠키 `scax_session` = 행 id, `platform/auth_sessions.py`)에 있다 — 로컬 스택이면 psql 로 `DELETE FROM auth_sessions WHERE member_id = '<로그인한 구성원 id>';`. 화면을 새로고침하지 말고 회의 상세 「내보내기」 → 기대: **토스트 「파일을 저장하지 못했습니다.」** · 앱 창 그대로 · 로그 `refused … status=401`. (웹뷰는 개발용 `X-Demo-Persona` 헤더를 싣지 않으므로 개발 프로파일에서도 401 이다.) 확인 뒤 다시 로그인한다
   - 5b **없는 자료**: 업무 자료를 다른 사용자가 지운 뒤(또는 회의를 지운 뒤) 남아 있는 링크/단추를 누른다 → 기대: 실패 토스트 · 로그 `refused … status=404`
   - 5c (선택) 쓰기 실패: 다운로드 폴더 쓰기 권한을 잠시 뺀다(`chmod u-w ~/Downloads` → 확인 뒤 **반드시** `chmod u+w ~/Downloads`) → 실패 토스트 · 로그 `failed …`
6. **브라우저(AC-T48)** — 같은 웹을 브라우저로 열어 1·2번: 지금처럼 브라우저가 내려받는다(셸 코드는 `__TAURI_INTERNALS__` 없으면 구독도 안 함)

Windows(AC-T46): 같은 1·2·5번을 WebView2 실기에서 — **pending**. Windows 는 격리 표식(`Zone.Identifier`)을 달지 않는다(알려진 차이 5).

## 7. 알려진 차이 · DS-gaps · 미결

- **알려진 차이 1 (코디 결정 X)**: 같은 탭 inline 응답(회의 자료 서랍 「내려받기」의 표시 가능 형식)은 「앱 창을 덮고 못 돌아옴」 → 「아무 일도 안 일어남」으로 바뀐다. 이유: macOS 는 `_blank` 도 `on_navigation` 을 먼저 지나 같은 탭과 가를 수 없고, 다시 navigate 하면 inline `_blank`(채팅 근거·AX 링크)가 앱 창을 덮는다
- **알려진 차이 2**: 셸의 HTTP 요청은 프록시를 **환경변수만** 본다 — 웹뷰가 쓰는 macOS 시스템 프록시/PAC 설정과 다를 수 있다
- **알려진 차이 3**: `/api/` 최상위 이동이 inline 이면 셸이 한 번 받아 본 뒤 버린다(요청 1회 더). 지금 웹에서 `/api` 로 최상위 이동하는 자리는 파일 링크뿐(`fe-survey` §2-4)
- **알려진 차이 4**: 셸의 GET 은 리다이렉트를 따라가지 않는다(3xx → `not-attachment`, 아무 일 없음) — 쿠키 유출 방지
- `on_navigation` 은 요청 메서드를 모른다 — 「GET 만」은 「최상위 이동 = 링크 클릭」이라는 전제다(웹에 `/api` 로 가는 `<form>` 제출이 생기면 다시 봐야 한다)
- 저장은 응답을 받아 스트리밍으로 쓴다(크기 상한 없음) · 진행 표시 없음 — 큰 파일은 끝날 때 토스트 한 번
- 토스트 문구 키 `savedUnnamed` 를 하나 더 뒀다(웹뷰 자체 내려받기가 이름을 못 줄 때) — 코디 문구 둘은 그대로
- DS-gaps: 없음(기존 공통 토스트 그대로)
- SPEC 사건 이름 「(제안 — 30-work/)」 → `strong-hajin:download` 로 정함. WP/SPEC 에 반영 필요(문서 수정은 내 몫 아님)

## 8. fix1 — 검수 WARN 7 처리 (`review-fe-p3-report.md` · 지시 `strong-hajin-polish3-fe-p3-fix1.md`)

### 변경 파일 (fix1)
`frontend/src-tauri/src/download.rs` · `frontend/src-tauri/src/lib.rs` 만. **웹(`shell.ts`·`App.tsx`·`labels.ts`)·Cargo·capabilities 변경 없음.**

| WARN | 처리 | 자리 · 시험 |
|---|---|---|
| **W1** macOS 격리 표식 | 셸이 쓴 파일(`save`)과 웹뷰 자체 내려받기 완료(`on_download Finished` 성공)에 `com.apple.quarantine` = `0081;{시각 16진};{실행 파일 이름};` 를 단다. libSystem `setxattr` 직접 호출(새 의존성 0). **실패해도 저장은 성공**, 로그만. Windows `Zone.Identifier` 는 **미처리**(알려진 차이 5) | `download::mark_quarantined` · `quarantine` 모듈 · 시험 `저장한_파일에는_macos_격리_표식이_붙는다`(getxattr 로 읽어 `0081;` 확인) |
| **W2** 오류 응답이 조용함 | `Fetched::Refused(status)` 신설 — **2xx 가 아니면**(401·3xx·404·5xx) 실패 사건 → 「파일을 저장하지 못했습니다.」. **2xx + inline 만** 아무것도 안 함 | `download::judge` · `take_over_api_link` · 시험 `오류_응답은_실패이고_2xx_inline_만_아무것도_안_한다` |
| **W3** 가로채기 기준 = 인증 허용 목록 | 기준을 **앱(운영) origin 하나**(`start_url` 의 origin · 미설정 판은 `None`)로 좁힘. 알림 대상 문서 판정도 같은 기준. `nav_allow` 는 이동 허용(E-05)에만 쓴다 | `is_api_request(url, Option<&str>)` · 시험 `셸이_받아_보는_것은_…`(IdP 주소 단언 추가) · lib 시험이 `nav_allow` 로 돌아가지 않음을 단언 |
| **W4** 하위 프레임 | **코드 변경 없음 — 코디 실기 판정**(§6-3 판정 ①). 고침 후보는 아래 |
| **W5** 파일 이름 빈틈 | ① Windows 예약 장치 이름(첫 `.` 앞이 CON·PRN·AUX·NUL·COM1-9·LPT1-9, 대소문자 무시) → 앞에 `_` ② 양방향 제어 문자(U+200E·200F·202A-202E·2066-2069) → `_` ③ 확장자가 100바이트를 넘으면 확장자로 보지 않고 통째로 자른다(숨김 파일 방지) | 시험 `양방향_제어_문자로_…` · `windows_예약_장치_이름은_피한다`(비슷하지만 예약 아닌 6개 포함) · `터무니없이_긴_확장자는_…` |
| **W6** `on_download` 실패·키 충돌 | 다운로드 폴더 없음 · 장부 잠금 실패 · 빈 이름 없음 → **실패 사건** 후 취소. 진행 장부를 `주소 → 경로 큐`(`PendingDownloads`)로 — 같은 주소 둘이 서로 덮지 않고, **아직 쓰기 전인 진행 중 이름도 피해서** 같은 자리를 고르지 않는다. 같은 주소끼리는 시작 순서로 짝짓는다(완료 순서가 뒤바뀌면 토스트의 두 이름이 서로 바뀔 수 있다 — 두 파일 모두 저장은 정상) | `download::PendingDownloads` · `free_path_avoiding` · 시험 `같은_주소를_연달아_내려받아도_…` |
| **W7** 읽기 타임아웃 | 연결 **30초**(코디) · 응답 헤더 **60초**(서버가 파일을 메모리에서 한 번에 싣는다 — 스트리밍 0) · 본문 **전체 600초**(서버 업로드 상한 25MB `MAX_MATERIAL_BYTES` → 약 42KB/s 까지 견딤; 회의 자료는 20MB). 넘으면 실패 사건 + 반쯤 쓴 파일 삭제(기존 `save` 실패 경로) | `CONNECT_TIMEOUT` · `RECV_RESPONSE_TIMEOUT` · `RECV_BODY_TIMEOUT` |

### W4 — 실기에서 깨질 때의 고침 후보와 대가
1. **주 프레임 판별** — tauri 2.11.6 `on_navigation` 은 URL 만 받는다(wry `navigation.rs:76` `function(url)`; `WKNavigationAction.targetFrame`/`isMainFrame` 을 넘기지 않음). 그래서 **tauri 훅만으로는 불가**하다. 하려면 `with_webview` 로 네이티브 WKWebView 를 잡아 wry 의 navigation delegate 를 감싸거나 바꾸는 objc2 코드가 필요하다(`objc2`·`objc2-web-kit` 직접 의존 추가 · wry 내부 delegate 동작(다운로드·페이지 로드 훅)을 함께 재현해야 함 · Windows 는 WebView2 의 `FrameNavigationStarting` 이 따로라 원래 영향 없음). **대가: 큼** — 셸이 wry 내부에 결합되고 tauri/wry 올릴 때마다 깨질 수 있다. 장점은 일반적(어떤 하위 프레임이든 정확)
2. **회의 자료 content 경로 예외** — `is_api_request` 에서 `/api/meetings/{id}/materials/{mid}/content` 만 가로채지 않는다(웹뷰 기본 동작으로 돌려보냄). **대가: 작음**(판정 함수 한 줄 + 시험) — 대신 ① 셸이 서버 경로 하나를 다시 알게 된다(결정 B 의 「경로를 모른다」 일부 후퇴) ② 같은 경로의 같은 탭 「내려받기」 링크는 예전처럼 **inline 이면 앱 창을 덮는다**(서랍 PDF·Markdown 은 늘 inline — 알려진 차이 1 이 사라지는 대신 U-4 사고가 그 링크에 되살아난다). 웹의 그 링크에 `download` 속성을 주거나 서버가 attachment 로 주면 해소되나 웹/서버 변경이다

### 검증 (fix1)
| 검증 | 결과 |
|---|---|
| `cargo test`(두 판) | 60 → **66 passed / 0 failed** |
| `cargo clippy -- -D warnings` · `--all-targets`(두 판) | 통과 |
| 웹 | 변경 없음 → vitest·tsc 재실행 불필요(Phase 3 본 결과 그대로: 50 passed · tsc 통과) |
| 실기 | pending — §6 보강 절차(특히 3 판정 ① · 5 실패 토스트 · 1 `xattr -l`) |

### 알려진 차이 (fix1 로 더해진 것)
- **알려진 차이 5**: Windows 는 `Zone.Identifier`(MOTW)를 달지 않는다 — 셸이 저장한 파일은 SmartScreen 의 「인터넷에서 받은 파일」 검사를 거치지 않는다
- §7 의 「알려진 차이 4」(리다이렉트) 는 이제 **실패 토스트**로 끝난다(W2) — 「아무 일 없음」 아님
- 바깥 인증(OIDC)이 생겨 **앱 origin 의** `/api/auth/…` 로 최상위 이동하면 그 302 는 실패 토스트가 된다(가로챔은 그대로) — 그때 `is_api_request` 에 인증 경로 예외가 필요하다(지금 그런 이동 0건)
