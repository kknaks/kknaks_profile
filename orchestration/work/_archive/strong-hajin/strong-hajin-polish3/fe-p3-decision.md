# fe-p3-decision — WORK-010 Phase 3 셸 첨부 저장: 구현 방식 결정 요청

> 작성: frontend(셸) 워커 · 2026-10-04 · 코드 기준 `d1b5137` · 소스 기준 `~/.cargo/registry/src/index.crates.io-*/`
> **아직 구현하지 않았다**(브리프 §2-6 「불리지 않는 구조면 구현 전에 묻는다」). 워크트리 변경 0.

## 0. 확인 결과 (브리프 §2-6)

| # | 질문 | 답 | 근거(소스 줄) |
|---|---|---|---|
| a | 응답 단계에서 `Content-Disposition` 으로 첨부를 가를 수 있나 | **없다.** wry 응답 정책은 `canShowMIMEType()` 하나만 본다. 헤더를 읽는 코드가 없고, tauri 2.11.6 은 응답 헤더 훅을 내주지 않는다(`on_navigation` 은 요청 URL 만, `on_page_load` 는 commit 뒤) | `wry-0.55.1/src/wkwebview/navigation.rs:86-103`(`:93` canShowMIMEType → 거짓이고 핸들러 있을 때만 Download, 그 밖 Allow) |
| b | `on_download`(download_handler)가 WKWebView 에서 `text/html` 첨부에 불리나 | **안 불린다.** 불리는 경우는 둘뿐: ① 이동 액션의 `shouldPerformDownload`(= `<a download>` 속성) ② 응답 MIME 이 표시 불가(docx·zip·octet-stream). `text/html`·PDF·이미지·텍스트는 표시 가능 → **Allow → 창에 그려진다**(사용자 관측과 일치) | `navigation.rs:50-80`(`:61` shouldPerformDownload) · `:86-103` · 기본값 `tauri-2.11.6/src/webview/mod.rs:357` `download_handler: None` |
| c | `_blank` 링크는 지금 무엇을 하나 | **macOS: 아무 일도 안 일어난다**(코드 읽기). new-window 핸들러가 없으면 wry UI delegate 가 `nil` 을 돌려준다. tauri `on_new_window` 를 걸면 URL 을 받고 `Deny` 할 수 있다. **Windows: 핸들러가 없으면 WebView2 기본 동작**(자체 팝업 창 — 미확인) | `wry-0.55.1/src/wkwebview/class/wry_web_view_ui_delegate.rs:140-260`(`:256-258` else → None) · `src/webview2/mod.rs:702-` · tauri `webview/mod.rs:585` `on_new_window` |
| d | Rust 가 웹뷰 쿠키(HttpOnly `scax_session`)를 얻을 수 있나 | **있다.** `Webview::cookies_for_url(url)` — HttpOnly·Secure 포함. macOS 는 `WKHTTPCookieStore getAllCookies`(메인 스레드 콜백 → **별도 스레드에서 불러야** 한다). Windows 는 「동기 핸들러에서 부르면 교착」 경고 → 같은 이유로 별도 스레드 | `tauri-2.11.6/src/webview/mod.rs:2131-2175` · `wry-0.55.1/src/wkwebview/mod.rs:1177-1225` |

→ **wry 에 맡겨서는 `text/html` 첨부를 저장할 수 없다.** 셸이 요청 단계(URL)에서 가로채고 스스로 받아야 한다.

## 1. 선택지

### A (추천) — 셸이 「파일 응답 후보」 경로만 가로채 Rust 가 쿠키를 실어 직접 받는다

- **방식**
  1. `on_navigation`(같은 origin) · `on_new_window`(`_blank`) 에서 URL 경로가 서버의 파일 엔드포인트 패턴이면 가로챈다:
     `/api/meetings/{id}/export` · `/api/**/materials/{id}/content` · `/api/work-requests/{id}/attachments/{id}/content` (= `be-survey-report.md` §2-4 의 7개)
  2. 이동은 **취소**(창 문서 그대로 → `on_page_load Started` 안 돎 → L-09 점유 정리 안 돎), `_blank` 는 **Deny**(두 번째 창 없음 · AC-T33)
  3. 별도 스레드에서 `cookies_for_url` → HTTP GET(쿠키 헤더) → **실제 응답 헤더**로 판정
     - `attachment` → `~/Downloads`(OS 다운로드 폴더, 대화상자 없음)에 `filename*`(UTF-8) 이름으로 저장. 같은 이름이면 `이름 (1).html`. 쓰기는 임시 이름 → rename(반쯤 쓴 파일이 원래 이름으로 남지 않게)
     - `inline`(회의 자료 중 표시 가능 형식) → **지금 동작 유지**: 같은 탭이면 그 URL 로 웹뷰를 다시 `navigate`(한 번 통과 표식), `_blank` 면 지금처럼 아무것도 안 함(OQ-T13 불변)
     - HTTP 오류·네트워크 실패·쓰기 실패 → 실패 알림
  4. 덧붙여 `on_download` 를 걸어, 경로 패턴 밖에서 wry 가 Download 로 넘기는 표시 불가 첨부도 같은 규칙(Downloads·번호·알림)으로 저장
  5. **웹 알림(권한 0)**: Rust 가 `webview.eval` 로 `window.dispatchEvent(new CustomEvent("strong-hajin:download", {detail:{ok, filename}}))` 를 쏜다 → `lib/shell.ts` 가 구독 함수 제공 → `App.tsx` 가 `putNotice("success"|"error", 문구)`. 문구는 웹(`App.tsx`/labels)이 만든다 — 셸은 문구 없음
- **권한·플러그인 변경**: capabilities **변경 0**(파일 권한 0 유지, `core:event:allow-listen` 도 열지 않음 — eval 은 ACL 밖 Rust→웹 방향). 커맨드 **넷 그대로**. 플러그인 추가 0(dialog·fs 없음). **새 crate 1개**: HTTP 클라이언트 `ureq`(`native-tls` 기능 — 이미 쓰는 native-tls 로 OS 신뢰 저장소 = 웹뷰와 같은 기준). Downloads 경로는 tauri `app.path().download_dir()`(추가 의존성 없음)
- **쿠키**: `cookies_for_url`(위 d). 요청에 `Cookie:` 로만 싣고 저장·로그 안 함
- **Windows 영향**: 요청 전에 가로채므로 macOS 와 같은 경로를 탄다(WebView2 자체 다운로드 UI·팝업이 뜨지 않음). `cookies_for_url` 별도 스레드 필수. **실기 pending**
- **약점**: 셸이 서버 파일 경로 패턴을 안다(결합). 서버가 새 파일 엔드포인트를 만들면 패턴에 더해야 한다 — 패턴 밖은 4번(on_download) 까지만 보호(표시 가능 MIME 이면 다시 창에 그려짐). 단위 테스트로 패턴 표를 고정한다. 프록시 설정이 있는 환경이면 웹뷰와 다를 수 있다(ureq 기본은 env 프록시만)

### B — 경로 패턴 없이 같은 origin `/api/` 의 모든 최상위 이동·`_blank` 를 Rust 가 받아 판정

- 방식: A 와 같고 1번 조건만 「같은 origin + 경로가 `/api/` 로 시작」. 판정은 응답 헤더로만
- 권한·쿠키·Windows: A 와 같음
- 장점: 서버 경로 결합이 `/api/` 접두 하나로 줄고, 새 파일 엔드포인트도 자동으로 덮는다
- 약점: `/api/` 최상위 이동이 inline 인 경우(JSON 등) **요청이 두 번** 나간다(Rust GET → 다시 navigate). 지금 웹은 `/api` 로 최상위 이동하는 자리가 위 파일 링크뿐이라(`fe-survey` §2-4) 실제 차이는 작다. GET 이 부작용 없는 전제

### C — 웹에서 처리(`fetch`+Blob 또는 `<a download>`)

- 방식: 웹 링크 10자리를 `download` 속성/fetch+blob 으로 바꾸고, 셸은 `on_download` 만(`<a download>` → `shouldPerformDownload` → Download)
- 권한: 0. 쿠키: 웹뷰가 실음(문제 없음)
- 약점: **Phase 1/2 파일과 겹친다**(MeetingDetailPage·WorkModals 등), 브라우저 동작(AC-T48)이 바뀔 위험, 저장 흐름의 절반을 웹이 진다. 비추천

## 2. 추천

**A** — 계약(파일 저장·창 유지·`_blank` 두 번째 창 없음·권한 0·커맨드 넷)을 셸 안에서 다 지키고 웹 변경이 수신부(`shell.ts`·`App.tsx`)에 머문다.
B 는 A 의 경로 판정만 넓힌 것이라, 서버 경로 결합이 싫으면 B 로 바꾸는 비용은 작다(판정 함수 하나).

## 3. 코디에게 묻는 것

1. **A / B / C** 중 어느 것
2. 새 crate `ureq`(+native-tls) 1개 추가 허용 여부
3. 웹 알림을 `eval` + DOM `CustomEvent`(권한 0)로 하는 것 허용 여부(대안: tauri 이벤트 + capability 에 `core:event:allow-listen` 추가)
4. 토스트 문구 제안: 성공 「{파일 이름}을(를) 다운로드 폴더에 저장했습니다.」 / 실패 「파일을 저장하지 못했습니다.」

## 4. 코디 답 (2026-10-04)

1. **B** — 같은 origin + 경로가 `/api/` 로 시작하는 최상위 이동·`_blank` 를 Rust 가 받아 **실제 응답 헤더로** 판정한다. 서버 파일 경로 패턴을 셸이 알지 않게(새 파일 엔드포인트 자동 포함). `inline` 은 지금 동작 유지(같은 탭 = 한 번 통과 표식으로 다시 navigate, `_blank` = 지금처럼 아무것도 안 함 — OQ-T13 불변). A 의 4번(`on_download` 로 표시 불가 첨부도 같은 규칙)은 그대로 넣는다. GET 만 가로챈다
2. **`ureq`(+native-tls) 1개 허용.** 프록시는 env 만 — 보고의 「알려진 차이」에 적는다
3. **`eval` + DOM `CustomEvent` 허용**(capabilities 변경 0 유지). 이벤트 이름·detail 형태를 `lib/shell.ts` 한 곳에 상수로
4. 문구 — 성공 「다운로드 폴더에 저장했습니다: {파일 이름}」 · 실패 「파일을 저장하지 못했습니다.」. 문구는 `lib/labels.ts` 에 키로 둔다 — **labels.ts 는 이 키 추가(끝에 덧붙이기)만 allowed_paths 에 더한다**(Phase 1 워커도 같은 파일을 만질 수 있으니 전체 덮어쓰기 금지, 정확한 위치에 추가만)
- 실기 확인 절차(코디용)를 보고에 꼭 적는다. 회의 내보내기 · 업무 자료 첨부 `_blank` · 회의 자료 PDF(inline, 같은 탭) · 채팅 근거 링크(inline `_blank`) 넷

## 5. 워커 추가 질문 (구현 중 발견 · 2026-10-04)

**inline 응답의 「같은 탭 = 다시 navigate」 를 macOS 에서 그대로 하면 OQ-T13 이 깨진다.**

- macOS WKWebView 는 `_blank` 클릭도 **먼저 opener 웹뷰의 `decidePolicyForNavigationAction`** 으로 보낸다(Apple 문서: `WKNavigationAction.targetFrame` 은 「새 창 이동이면 nil」 — 즉 새 창 이동도 이 delegate 를 지난다). wry 는 여기서 URL 만 tauri `on_navigation` 에 넘긴다(`wry-0.55.1/src/wkwebview/navigation.rs:76` `function(url)`) — **target 정보가 없다.**
- 그래서 macOS 에서 셸은 `/api/` 이동이 같은 탭인지 `_blank` 인지 **가를 수 없다.** `_blank` 도 `on_navigation` 에서 가로채져 취소된다(첨부면 저장 — 계약대로, 두 번째 창도 안 뜸).
- 문제는 inline 일 때: 「같은 탭이면 다시 navigate」를 하면 **채팅 근거 「원본 열기」·AX 답변 링크(inline `_blank`)가 앱 창을 덮게 된다** — 지금은 아무 일도 안 일어나는 자리라 OQ-T13 「바꾸지 않는다」 위반이고 U-4 사고다.
- Windows 는 `_blank` 가 `NavigationStarting` 이 아니라 `NewWindowRequested` 로만 온다 → 가를 수 있다.

선택지:
- **X(추천)**: inline 이면 **어느 쪽이든 다시 navigate 하지 않는다**(로그만). 영향: 같은 탭 inline(회의 자료 서랍 `MaterialDrawer.tsx:66` 의 표시 가능 형식 — PDF·이미지 등) 클릭이 「앱 창을 덮고 못 돌아옴」 → 「아무 일도 안 일어남」으로 바뀐다. `_blank` inline 은 지금 그대로(아무 일 없음). 서랍 안 PDF 미리보기(`<object data>`)는 하위 리소스라 이동 훅을 안 지나 그대로다.
- **Y**: 지시대로 같은 탭 = 다시 navigate. macOS 에서 inline `_blank`(채팅 근거·AX 링크)도 앱 창을 덮게 된다.
- **Z**: Windows 만 같은 탭 re-navigate, macOS 는 X.

답이 오기 전까지 **X 로 구현**해 두고(판정 함수 한 줄이라 바꾸기 쉽다), 답에 맞춰 고친다.

### §5 코디 답 (2026-10-04)

**X** — inline 이면 같은 탭·`_blank` 어느 쪽이든 다시 navigate 하지 않는다(로그만). OQ-T13 「인라인은 바꾸지 않는다」와 U-4(앱 창을 덮지 않는다)를 지키는 쪽.
- 알려진 차이로 보고에 적는다: 회의 자료 서랍 「내려받기」(`MaterialDrawer.tsx:66`)의 표시 가능 형식(PDF·이미지 등 서버가 inline 으로 주는 것)은 앱에서 「창을 덮고 못 돌아옴」→「아무 일 없음」. 이 자리는 코디가 사용자 E2E 때 따로 묻는다(파일로 저장할지)
- Windows 판정 차이(Z)는 두지 않는다 — 두 OS 같은 규칙
