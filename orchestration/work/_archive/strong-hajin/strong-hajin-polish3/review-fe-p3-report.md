# 리뷰 리포트 — strong-hajin-polish3 / frontend(셸) · WORK-010 Phase 3 (2026-10-04)

## 판정: WARN

FAIL 0 · WARN 7.

**계약은 코드로 지켜졌다.**
- WP Phase 3 계약 6줄과 SPEC-006 U-5 · E-15 · AC-T47·T48 의 코드 측 조건이 모두 PASS 다.
- 보안 기본선은 안전하다: 쿠키를 다른 주소로 보내지 않고, 로그에 남기지 않으며, TLS 검증을 끄지 않는다. 파일 이름의 경로 조작을 막고, `eval` 에 실리는 문자열은 JSON 직렬화한다. capabilities·커맨드·플러그인 변경은 0이다.

**WARN 일곱 가지**
- macOS 격리 표식(quarantine)이 없다
- 막힌 응답(401·3xx·타임아웃)이 소리 없이 끝난다
- 가로채기 기준이 「인증 흐름용 허용 목록」을 함께 쓴다
- 하위 프레임 이동을 거르지 않는다(실기 확인 필요)
- 파일 이름 정리의 Windows·양방향 문자 빈틈
- `on_download` 실패가 소리 없이 끝난다
- 읽기 타임아웃이 없다

AC-T44·T45·T49 는 실기 항목이라 **실측 전에는 통과로 적을 수 없다.**

## 검수 범위

- 대상: 워크트리 `Strong_hajin/strong-hajin-polish3`(HEAD `7f01c5b` = Phase 1 커밋)의 미커밋 diff 중 Phase 3 파일만
  - `frontend/src-tauri/src/download.rs`(신규 480줄)
  - `frontend/src-tauri/src/lib.rs`(+184)
  - `frontend/src-tauri/Cargo.toml` · `Cargo.lock`(ureq 3.4.2)
  - `frontend/src/lib/shell.ts`(+38) · `shell.test.ts`(+49)
  - `frontend/src/App.tsx` 수신부 `:122-131` · `App.test.tsx` 다운로드 시험 1건
  - `frontend/src/lib/labels.ts` `shellDownload`(끝 9줄)
  - 제외: `ds/Modal.tsx` · `ds/InlineText.tsx` · App.tsx 의 AX 정리 — Phase 1·2a 몫
- 기준: SPEC-006 v0.3.1(U-1 · U-4 · U-5 · §2.5 · E-15 · §5 · AC-T44~49 · M-15 · L-09) · WP Phase 3 · `fe-p3-decision.md` §4(B)·§5(X) · `fe-p3-worker-report.md`
- 실행한 검사
  - `SHELL_FLAVOR=medi-ax` / `strong-hajin` 각각 `cargo test` → **두 판 모두 60 passed / 0 failed**
  - 같은 두 판으로 `cargo clippy --all-targets -- -D warnings` → **두 판 모두 경고 0**
  - `npx vitest run --no-file-parallelism src/lib/shell.test.ts src/App.test.tsx` → 49 passed / **1 failed**
    - 실패한 것은 `App.test.tsx` 「keeps the AX composer enabled…」 하나다. 원인은 Phase 2a 가 「AX에게 이 업무 묻기」 단추를 지우는 중이라서다(`Unable to find role="button" … AX에게 이 업무 묻기`). **Phase 3 시험(다운로드 토스트·셸 수신부 4건)은 통과**했고, 이 실패는 Phase 3 판정에 넣지 않는다
  - 의존성 원문 대조
    - ureq 3.4.2 `src/tls/native_tls.rs:147-161`: `PlatformVerifier` 는 OS 내장 루트를 쓰고, `disable_verification` 은 기본 거짓이다
    - ureq `config.rs:948`: 프록시는 환경변수에서 읽는다
    - wry 0.55.1 `wkwebview/navigation.rs:50-103`
  - grep: 웹의 최상위 `/api` 이동·`<form>`·`<object>`·`download=`·`window.open` 자리 · capabilities 문자열 · Info.plist 격리 키

## 위반 (FAIL 사유)

없음.

## 경미 (WARN)

- **W1 · macOS 격리 표식 없음 (보안·방어 깊이)** `download.rs:236-249` `save` · `lib.rs` `on_download` `Requested`
  - 셸이 직접 쓴 파일에는 `com.apple.quarantine` 확장 속성이 붙지 않는다. `Info.plist` 에 `LSFileQuarantineEnabled` 도 없다(grep 0).
  - 브라우저로 받은 파일에는 이 표식이 붙어 Gatekeeper 가 첫 실행을 검사한다. 앱으로 받은 파일은 그 검사를 **건너뛴다.**
  - 업무 자료·요청 첨부는 조직 구성원이 올린 **임의 형식**이다(be §2-4 「원본」). 저장에는 대화상자가 없다. 같은 origin 문서가 `/api/…/content` 로 이동하기만 하면 다운로드 폴더에 파일이 생긴다.

  권장: macOS 에서 저장 직후 격리 속성을 다는 경로를 둔다(`LSFileQuarantineEnabled` 또는 xattr). 그럴 수 없으면 「알려진 차이」로 사용자 승인을 받는다.
- **W2 · 막힌 응답이 소리 없이 끝난다** `lib.rs` `take_over_api_link` 의 `NotAttachment` 갈래 · `download.rs:288-297`
  - 세션 만료 401, 3xx(리다이렉트를 따라가지 않음), 404 는 모두 「첨부 아님」으로 접힌다. 이때는 **토스트도 창 변화도 없다.**
  - 사용자는 「내보내기를 눌렀는데 아무 일도 없다」만 본다. 예전에는 웹뷰가 오류 문서라도 보였다.
  - 결정 X 는 *inline* 응답을 「아무 일 없음」으로 정한 것이지 *오류 응답*까지 정한 것은 아니다. 2xx 가 아닌 응답은 실패 사건(`ok:false`)으로 알리는 쪽이 계약 「실패를 알린다」(WP 3번 줄 · U-5 5)에 더 맞는다.
  - 같은 이유로 **나중에 바깥 인증(OIDC)이 붙어 `/api/auth/…` 로 최상위 이동하면 그 302 가 삼켜져 로그인이 조용히 멈춘다.** 지금은 그런 이동이 0건이다(grep: `location.*`·`<form action>` 0, 로그인은 fetch). 워커 보고 §7 의 「`<form>` 생기면 재검토」와 같은 경계다.
- **W3 · 가로채기 기준이 인증 흐름용 허용 목록과 같은 목록이다** `lib.rs` `download::is_api_request(url, &nav_allow)` · `config.rs:68-80`
  - `navigation_allowlist` 는 「운영 origin + 인증 흐름이 거치는 주소」다(flavor 설정 주석). 지금은 두 판 모두 추가 항목이 0이라 문제가 없다.
  - 나중에 IdP origin 을 넣으면 그 IdP 의 `/api/…` 이동까지 셸이 가로챈다. 쿠키는 그 주소로만 가므로 새는 것은 아니다. 대신 **그 이동이 취소된다.**
  - 계약 「같은 origin」은 운영 origin 하나다. 권장: `is_api_request` 에는 운영 origin 하나(`start_url` 의 origin)만 넘긴다.
- **W4 · 하위 프레임 이동을 거르지 않는다 — 실기 확인 필수** wry `navigation.rs:50-82`
  - wry 의 `navigation_policy` 는 **주 프레임인지 보지 않고** 모든 이동을 `on_navigation` 으로 보낸다. 그래서 iframe/`<object>` 가 `/api/` 를 이동으로 열면 그 로드가 **취소된다.**
  - 지금 해당할 수 있는 자리는 회의 자료 서랍의 PDF 미리보기 `<object data="/api/meetings/{id}/materials/{mid}/content">`(`MaterialDrawer.tsx:88`) 하나다. 회의 자료는 PDF·Markdown 만 받고 늘 inline 이다(`material_policy.py:10-11` · `http.py:1115-1116`).
  - 워커 보고의 「`<object data>` 는 하위 리소스라 이동 훅을 안 지난다」는 코드로 확인되지 않았다. WebKit 이 PDF `<object>` 를 플러그인 스트림으로 받는지 프레임 이동으로 받는지에 달렸다.
  - 이동이라면 미리보기가 빈칸이 되고, 셸은 같은 파일을 한 번 더 받아 버린다(첨부가 아니라 저장은 안 함).
  - 실기 절차 §6-3 에 「서랍 안 PDF 미리보기는 그대로 보인다」 기대가 이미 있다. **이 항목을 꼭 눈으로 보고, 실패면 `on_navigation` 에 주 프레임 판별(또는 `/api/meetings/*/materials/*/content` 예외)이 필요하다.**
- **W5 · 파일 이름 정리의 빈틈** `download.rs:165-195`
  - ① Windows 예약 장치 이름(`CON`·`NUL`·`COM1`·`LPT1` …)을 거르지 않는다. Windows 에서 「CON.html」 같은 이름은 열기에 실패한다. 실패 토스트로 끝나지만, Windows pending 이니 실기 때 함께 본다.
  - ② `char::is_control` 은 Cc 만 잡는다. 양방향 덮어쓰기 문자(U+202E 등, Cf)가 그대로 남는다. 「계약서‮fdp.exe」처럼 **확장자가 뒤집혀 보이는** 이름이 토스트·Finder 에 그대로 선다. 업로드 파일 이름은 사용자가 정한다.
  - ③ `clamp_bytes` 에서 확장자 자체가 200바이트를 넘으면 결과가 `.` 으로 시작하는 확장자 덩어리가 된다. 그 이름은 숨김 파일이 되고 255바이트를 넘을 수도 있다. 극단적인 경우다.

  권장: Cf 범주(최소한 U+202A-202E · U+2066-2069)와 Windows 예약 이름을 `_` 로 바꾼다.
- **W6 · 웹뷰 자체 내려받기의 실패가 소리 없다** `lib.rs` `on_download` `Requested`
  - 다운로드 폴더를 못 찾거나 빈 이름을 못 고르면 `false` 를 돌려 내려받기가 취소된다. 이때 `notify_download(false)` 가 없다.
  - 진행 중 맵이 **URL 을 키로** 쓴다. 같은 URL 을 연달아 받으면 앞의 이름이 덮이고, 둘째 완료 토스트는 이름 없는 문구(`savedUnnamed`)가 된다.
  - 이 경로는 지금 웹에 `download=`·blob 이 0건이라 거의 타지 않는다. 경미하다.
- **W7 · 읽기 타임아웃 없음 · 크기 상한 없음** `download.rs:278`
  - `timeout_connect(15s)` 만 걸려 있다. 서버가 응답 도중 멈추면 받기 스레드가 **끝없이** 기다리고, 성공·실패 토스트가 둘 다 안 뜬다.
  - 반쯤 쓴 파일은 최종 이름으로 남아 있다가 오류가 날 때만 지워진다. 임시 이름 → rename 이 아니라 `create_new` + 실패 시 삭제이므로, 그 사이 Finder 에 자라는 파일이 보인다.
  - 권장: `timeout_recv_body`(또는 `timeout_global`)를 넉넉히 건다(예: 10분).

## 브리프 §3 항목별

### 1. 계약 체크 (WP Phase 3 · SPEC-006)

| 계약 | 판정 | 근거 |
|---|---|---|
| 첨부 응답 = 파일 저장 · 창 문서 불변 · 같은 origin 이동과 `_blank` 둘 다 | PASS(코드) · **실기 pending** | 같은 탭: `lib.rs` `on_navigation` 이 `is_api_request` 면 `false`(취소) → 문서가 안 바뀌므로 `on_page_load Started`(L-09 정리)도 돌지 않는다. `_blank`: macOS 는 같은 훅(wry 가 새 창 이동도 `decidePolicyForNavigationAction` 을 지남), Windows 는 `on_new_window` → `Deny` + 같은 처리 |
| OS 다운로드 폴더 · 대화상자 없음 · `filename*` UTF-8 · 같은 이름이면 번호 | PASS | `app.path().download_dir()` · 대화상자 API 0 · `parse_disposition`(`download.rs:52-78`, 시험 `서버의_한글_filename_별표를_읽는다`) · `reserve` `create_new` 로 `이름 (n).ext`(`:222-232`, 시험 `같은_이름이_있으면_…`) |
| 성공(이름)·실패를 알린다 · 셸 문구 0 · 웹이 공통 토스트 | PASS(오류 응답은 W2) | `event_script`(`:318-322`)는 `{ok, filename}` 만 싣고 경로·문구가 없다. `App.tsx:122-131` → `putNotice`. 문구는 `labels.ts` `shellDownload`. 시험 `App.test.tsx` 다운로드 1건 통과 |
| 헤더로 못 가르면 먼저 묻는다 | PASS | `fe-p3-decision.md` §0·§4·§5 |
| 인라인 `_blank` 불변(OQ-T13) | PASS — 화면 기준 | 셸이 inline 응답을 받아도 **다시 navigate 하지 않는다**(결정 X). macOS 의 `/api/` 가 아닌 `_blank` 는 `Deny` 로, 핸들러가 없던 때 wry 가 nil 을 돌려주던 것과 같다. 차이 둘: ① 셸이 요청을 한 번 더 보낸다 ② 같은 탭 inline(서랍 「내려받기」 PDF)은 「창을 덮음」→「아무 일 없음」. ②는 코디가 승인했다(§5 X). W4 참고 |
| 두 판 모두 | PASS | 코드 한 벌. strong-hajin 판은 origin `null` → 허용 목록이 비어 가로채기 0(시험 `셸이_받아_보는_것은_…` 마지막 단언). 두 판 `cargo test` 60/60 |
| 권한·플러그인 최소 · capabilities 변경 보고 | PASS | capabilities·`tauri.conf.json`·flavors diff 0. 시험 `제품_창은_첨부_응답을_…` 이 `core:`·`fs:` 부재를 단언한다. 커맨드 넷 그대로(AC-T47) |
| `cargo check/test/clippy` | PASS | 위 「실행한 검사」 |
| AC-T44 · T45 · T49 (macOS 실기) | **pending** | 실기 전 통과 금지 |
| AC-T46 (Windows) | **pending** | `cargo check --target windows` 도 호스트 도구 부재로 못 했다(워커 보고) |
| AC-T48 (브라우저 불변) | PASS(코드) | `onShellDownload` 는 `hasShell` 이 거짓이면 구독하지 않는다(`shell.ts`, 시험 `셸이 없으면 듣지 않는다`). 웹의 링크 마크업 변경 0 |

### 2. 가로채기 범위

- **같은 origin + `/api/`** 다: `is_api_request` 는 scheme 이 http/https 이고, `origin().ascii_serialization()` 이 허용 목록과 정확히 같고, `path().starts_with("/api/")` 여야 한다(`download.rs:37-41`).
  - `/apis/x` · `/api` · 다른 origin · http↔https 차이 · 셸 스킴 `stronghajin://` 은 거부된다(시험).
  - `Url` 이 `..`·`%2e%2e` 를 정규화한 뒤의 path 를 보므로 우회 경로가 없다.
- **다른 origin 이동**은 기존 분기(`blocked origin … L-11` → E-05)가 먼저 돈다. 이번 변경과 무관하다.
- **일반 화면 이동**(`/meetings/…` 등)은 그대로 `true` 다.
- **GET 만**: 훅이 메서드를 모르므로 「최상위 이동 = 링크」라는 전제다. 지금 웹에 `/api` 로 가는 `<form>` 제출·`location` 대입은 0건이다(grep). W2 의 OIDC 경계를 참고한다.
- **inline 은 정말 아무것도 안 한다**: `NotAttachment` 갈래는 로그만 남기고 다시 navigate 하지 않는다. 창을 덮을 길이 없다(U-4). 다만 하위 프레임은 W4 에서 실기로 확인해야 한다.
- 범위 기준 목록은 W3 참고.

### 3. 쿠키·보안

- **메인 스레드에서 부르지 않는다**: `cookies_for_url` 은 `take_over_api_link` 가 띄운 `shell-download` 스레드 안에서만 불린다. `on_navigation`·`on_new_window` 콜백은 스레드를 띄우고 바로 돌아온다.
- **로그·파일에 남기지 않는다**: 로그에는 `via`·`path`·`status`·파일 이름만 남는다. 쿼리와 쿠키는 남지 않는다. `cookie_header` 값은 요청 헤더에만 실린다.
- **다른 origin 으로 보내지 않는다**
  - 쿠키는 `cookies_for_url(그 URL)` 결과이고, 같은 URL 에만 보낸다.
  - `max_redirects(0)` 이라 3xx 를 따라가지 않는다(`download.rs:274-275`).
  - ureq 는 기본 기능을 끈 상태라 쿠키 저장소가 없다(`default-features=false`).
  - 환경변수 프록시를 쓰는 경우에도 HTTPS 는 CONNECT 터널이라 끝단 TLS 는 그대로다.
- **TLS 검증을 끄지 않는다**: `TlsProvider::NativeTls` + `RootCerts::PlatformVerifier` → native-tls 의 OS 내장 루트를 쓴다(ureq `native_tls.rs:159-161`). `disable_verification` 호출은 0건이다.
- **새 crate**: `ureq 3.4.2 { default-features=false, features=["native-tls-no-default"] }`. lock 에 rustls·webpki-roots 가 없다(의존: native-tls · ureq-proto · base64 · der · log · percent-encoding · rustls-pki-types · utf8-zero).
- W1(격리 표식)은 보안 지적이다.

### 4. 파일 쓰기

- **경로 조작**
  - 마지막 경로 조각만 쓴다(`/`·`\` 기준 `rsplit`).
  - 예약 문자 `<>:"|?*` 와 제어 문자(NUL 포함)는 `_` 로 바꾼다.
  - 앞의 `.` 를 떼므로 `..` → 없음 → `download` 가 된다.
  - 절대 경로는 마지막 조각만 남는다.
  - 시험 `파일_이름은_다운로드_폴더_밖으로_나가지_않는다` 가 있다.
  - 빈틈은 W5 참고.
- **번호**: `create_new` 로 고르는 순간과 쓰는 순간 사이의 경쟁을 막고, 9,999번까지 시도한다.
- **임시 이름 → rename**: 이 방식은 아니다. `create_new` 로 최종 이름을 바로 잡고 쓰다가 실패하면 지운다(`:236-244`, 시험 `쓰다_실패하면_…`). 실패 시 남는 파일은 없다. 쓰는 도중 보이는 파일·멈춤은 W7.
- **실패 경로**: 쿠키·다운로드 폴더·네트워크·쓰기 실패는 모두 `notify_download(false)` 로 간다. 오류 응답은 W2, `on_download` 는 W6.

### 5. 웹 알림

- **스크립트 주입 없음**: `serde_json::json!` 로 detail 을 직렬화하고, 이벤트 이름도 `Value::String` 으로 직렬화한다. `"`·`\`·`</script>` 가 모두 이스케이프된다(시험 `웹에_보내는_사건에는_…` 이 `회의 \"록\"</script>.html` 을 확인). `eval` 은 HTML 이 아니라 스크립트로 실행되므로 `</script>` 도 해가 없다.
- 받는 쪽은 토스트를 React 텍스트로 그린다. HTML 로 해석되지 않는다.
- **허용 origin 문서일 때만** 보낸다(`notify_download` 의 `window.url()` 판정). 셸 자기 화면(U-2)에는 보내지 않는다.
- **브라우저에서는 구독하지 않는다**: `onShellDownload` 는 `hasShell` 이 거짓이면 아무것도 등록하지 않는다. detail 모양이 다르면 버린다(시험 4건).
- **문구는 labels**: `labels.ts` `shellDownload.saved/savedUnnamed/failed`. 코디 문구 둘과 글자가 같다. `savedUnnamed` 는 워커가 더한 것이고 보고했다.
- 참고: 페이지 스크립트도 같은 사건을 쏠 수 있다(위조 토스트). 결과가 토스트 한 줄뿐이라 위험은 없다.

### 6. capabilities·커맨드·플러그인 · crate

- capabilities·`tauri.conf.json`·flavors diff 0 · 커맨드 넷 · 플러그인 추가 0 · crate 1(ureq, 위 기능 플래그). **PASS.**

### 7. cargo test · clippy

- 두 판 모두 test 60/60, clippy 경고 0. **PASS.**

## 실물에서 만날 자리 (사용자·코디 E2E)

1. **내보내기 → 토스트 「다운로드 폴더에 저장했습니다: {제목}.html」.** 두 번 누르면 `(1)` 이 붙는다. 앱 창은 회의 상세 그대로다.
2. **자료 서랍 「내려받기」(PDF) → 아무 일도 없다**(결정 X · 알려진 차이 1). 사용자는 「버튼이 고장났다」로 볼 수 있다. 코디가 E2E 때 묻기로 한 자리다.
3. **자료 서랍 PDF 미리보기가 그대로 보이는가**(W4). 빈칸이면 하위 프레임 판별이 필요하다.
4. **세션이 만료된 채 내보내기·첨부를 누르면 아무 일도 없다**(W2). 다시 로그인해야 한다는 신호가 없다.
5. **업무 자료·요청 첨부 링크(`_blank`) → 저장 + 토스트, 두 번째 창 없음.** 예전 macOS 에서는 아무 일도 없던 자리라 동작이 새로 생긴다.
6. **AX 답변·채팅 근거의 `/api/…/content` 링크**: 첨부(업무 자료 등)면 이제 저장되고 토스트가 뜬다. inline 이면 아무 일 없음(지금과 같음).
7. **받은 실행 파일·압축을 Finder 에서 열 때 Gatekeeper 경고가 없다**(W1).
8. **큰 파일**: 진행 표시가 없다. 끝날 때 토스트 한 번이고, 그 사이 Finder 에는 자라는 파일이 보인다. 서버가 멈추면 토스트가 영영 안 뜬다(W7).
9. **회사망 프록시**: 셸 요청은 환경변수 프록시만 본다. 시스템 프록시/PAC 만 쓰는 망에서는 웹 화면은 열리는데 저장만 실패할 수 있다(알려진 차이 2).
10. **이상한 파일 이름**: 양방향 문자가 든 이름이 뒤집혀 보인다(W5). Windows 예약 이름은 실패한다.

## 코디 실기 절차(보고 §6)가 계약 AC 를 덮는가

| AC | 절차 | 덮나 |
|---|---|---|
| AC-T44 내보내기 저장 · 창 그대로 | §6-1 | ○ |
| AC-T49 다운로드 폴더 · 번호 · 성공 토스트 | §6-1(두 번 누르기) | ○ |
| AC-T49 실패 토스트 | §6-5(선택 — 폴더 권한 제거) | △ — 「선택」이다. AC-T49 가 실패 토스트를 요구하므로 **필수로 올리기를 권한다** |
| AC-T45 `_blank` 첨부 · 두 번째 창 없음 | §6-2 | ○ |
| L-09 점유 유지 | §6-1 녹음 중 확인 | ○ |
| OQ-T13 인라인 `_blank` 기록 | §6-4 | ○ |
| AC-T48 브라우저 불변 | §6-6 | ○ |
| AC-T46 Windows | pending | — |
| AC-T47 커맨드 넷·파일 권한 0 | 실기 아님(시험·설정) | ○(코드 시험) |
| **빠진 것** | — | ① W4 의 서랍 PDF **미리보기** 확인을 §6-3 기대에서 **판정 항목**으로 올린다 ② 세션 만료 상태에서 내보내기(W2 동작 기록) ③ 다운로드 폴더의 파일에 `xattr -l` 로 격리 속성 확인(W1) |

## 기존 부채 (이번 판정 제외)

- Windows 에서 `/api/` 가 아닌 `_blank` 는 `Allow`(WebView2 기본 팝업)다. 바뀌기 전과 같지만 AC-T33(두 번째 창 없음)과는 긴장이 있다. U-4 의 다른 origin `_blank` 처리도 Windows 에서는 이 경로를 탄다.
- `App.test.tsx` 「keeps the AX composer enabled…」 실패는 Phase 2a 진행 중인 변경 때문이다.

## 확인한 것 (PASS 근거)

- allowed_paths: 리포트 한 장만 썼다. 코드 수정 0.
- Phase 3 파일 diff 전체를 정독했다(download.rs 전문 포함).
- 두 판 cargo test/clippy 를 직접 실행했다.
- 웹 수신부 시험 4 + App 토스트 1 이 통과했다.
- 의존성(ureq TLS·프록시, wry 이동 정책) 원문을 대조했다.
- 사건 이름이 셸과 웹에서 같다. 셸 시험 `사건_이름이_웹_수신부와_같다` 가 `shell.ts` 를 `include_str!` 로 대조한다.
