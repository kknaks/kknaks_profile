# 고도화 조사 (frontend)

- 대상: 코드 `origin/main` `f0ad522`(운영 반영본, 워크트리 `strong-hajin-enhance`) — **읽기만 했다.** 코드·테스트·빌드·서버·앱 실행 0
- 경로는 저장소 기준이다(`frontend/…` · `backend/src/ax_workspace/…` 는 줄여 `backend/…`). 셸 = `frontend/src-tauri/src/`
- 「현재 무엇이 어떻게 도는지」 만 적는다. 고칠 방향은 적지 않았다

## 0. 한 줄 요약

| 항목 | 한 줄 (원인이 보이면 원인) |
|---|---|
| SH-IMP-014 앱 내려받기 | 셸 가로채기 경로(`on_navigation`·`on_new_window`·`on_download`)는 WORK-011 에서 **본문이 한 글자도 안 바뀌었다**(diff 동일) — 「WORK-011 on_navigation 회귀」 근거 없음. 확정된 결함은 **WORK-010 의 ureq `native-tls-no-default` → https 에서 받기 스레드 패닉(로그·토스트 없이 사라짐)** 이었고 `2102772` 에서 고쳐져 **fix2 dmg 에는 들어 있다.** fix2 에서도 안 되는 원인은 읽어서는 하나로 좁혀지지 않는다 — 코드상 「토스트 없이 끝나는」 자리는 ① 가로챈 응답이 `inline`(이미지·PDF·MD 첨부)이면 무알림 종료 ② `<a download>` 는 셸 훅을 건너뛰고 WKDownload(`on_download`)로 감 ③ 창 못 찾음 — 셸 로그(터미널 실행)로 갈라야 한다 |
| SH-IMP-011 하위 프레임 | wry 정책 콜백에 프레임 구분이 없어 하위 프레임 `about:blank`·`about:srcdoc`(origin `"null"`)이 허용 목록 단계에서 **취소**된다. 하위 프레임의 `/api/` 로드도 가로채기 대상이 된다 |
| SH-IMP-001 AX 회의 생성 | 업무는 `AxDraftCard`(4쪽 읽기 전용 요약 + 수정은 `CreateWorkModal`), 회의는 `ActionMeetingCard`(구 `ActionTaskCard` 계열 한 장 카드 + 인라인 편집) — **공유하는 것은 `scax-actioncard` 클래스와 `Badge` 뿐.** 회의 카드에는 거절 단추·AX 배지·회차·참고 업무가 없다 |
| SH-IMP-002·004 모달 겹침 | 왼쪽 열 ≈277px 에 날짜 200px(고정) + 시간쌍(줄지 않음) ≈400px 이 들어가 ≈125px 넘친다. 검색 입력 옆에 **실제 단추 요소는 없다** — 「단추」 는 넘친 **종료 시각 `button.select-trigger`** 이고 검색 입력이 DOM 순서상 그 위에 그려진다 (CSS 계산값, 실측 아님) |
| SH-IMP-003·016 장소 | `#meeting-head-place` 는 수정 모달 한 곳의 자유 입력. 회의실 고르기 UI 는 **생성(`BookingModal`)에만** 있다. 수정 모달·AX 카드에는 없다 |
| SH-IMP-005 불러오기 | 원인 둘 다 코드로 보인다 — ① `applySuggestion` 이 지난 회의의 **날짜·시작·종료를 그대로 넣는다**(`BookingModal.tsx:205-207`) ② 서버가 생성 때 `carried_from_meeting_id` 가 있으면 **모든 안건**에 `source="carried"` 를 단다(`application.py:415`) — 프론트는 안건 제목만 보낸다 |
| SH-IMP-015·008·010 | 메시지 행에 호버 규칙·행동 자리 0 · 답글 0개 스레드는 입구(`ThreadLine`)만 없고 패널·조회·답장 경로에 답글 수 조건 없음 · 카톡도 같은 `Message` 컴포넌트 · 「서랍 열고 보내기」 는 `askAx`(Today 화면 한 곳) · 참고 자료 칩은 **그리는 코드 0** · 설정 화면은 이미 `useInboxStream` 을 구독하고 `integration.changed` 에 다시 읽는다 — 서버가 작은 실시간 저장(≤20건)에는 그 사건을 내지 않는다 |
| SH-IMP-013 ① | 방 목록은 `card.title` 을 그대로 그린다 — 이름이 `""` 면 빈 제목. 프론트 대체 이름 0 |
| SH-IMP-018 메일 이미지 | 외부 이미지는 막는 게 아니라 **자동으로 서버 프록시 경유**(사용자 결정 10-06). 프록시가 거절하는 규칙(SVG·래스터 아님·5MB·리다이렉트 4회+·200 아님·사설 IP·포트 등) 중 하나에 걸린 이미지만 빠진다. 어느 규칙인지는 실제 메일 HTML·서버 로그가 있어야 갈린다. 웹(alt 글자) vs 앱(깨진 `?`)은 서버·번들·CSP 가 같아 **코드로 갈리는 자리는 없다** |

## 1. SH-IMP-014 · 011 — 데스크톱 앱 내려받기 · 하위 프레임 이동 (`frontend/src-tauri/`)

> 경로는 저장소 기준이다. 셸 = `frontend/src-tauri/src/`. 의존 소스는 `Cargo.lock` 이 고정한 판이다 — wry **0.55.1** · tauri **2.11.6** · tauri-runtime-wry **2.11.4** · ureq **3.4.2** (`frontend/src-tauri/Cargo.lock`). 의존 소스는 로컬 cargo 레지스트리(`~/.cargo/registry/src/index.crates.io-*/`)에서 읽었다.

### 1-1. 셸의 다운로드 가로채기 — 위치와 동작 순서

셸에는 **받는 길이 셋** 있다. 셋 다 `spawn_main_window`(lib.rs:408-584) 한 곳의 창 빌더에 걸려 있다.

| 길 | 훅 | 가로채는 조건 | 하는 일 |
|---|---|---|---|
| A. 이동 가로채기 | `.on_navigation`(lib.rs:435-463) | ① 셸 스킴이 아니고(437) ② origin 이 `nav_allow` 에 있고(440-441) ③ `download::is_api_request(url, app_origin)` 가 참(457) | `take_over_api_link(..., "navigation")` 를 띄우고 **이동은 취소**(`return false`, 458-459) |
| B. 새 창 가로채기 | `.on_new_window`(lib.rs:467-477) | `is_api_request` 가 참(468) | `take_over_api_link(..., "new-window")` + `Deny`(469-470). `/api/` 가 아니면 macOS 는 `Deny`(472-473) |
| C. 웹뷰 자체 내려받기 | `.on_download`(lib.rs:480-538) | 웹뷰가 내려받기로 넘긴 것(아래 1-2 의 wry 판정) | `Requested`: 다운로드 폴더의 빈 이름을 골라 `destination` 을 바꿈(487-516) · `Finished`: 격리 표식 + 웹 알림(517-535) |

`is_api_request`(download.rs:54-61) 조건 = **스킴 http/https** · **origin 이 앱 origin 하나와 같음**(`nav_allow` 가 아니라 `app_origin` — lib.rs:605-609) · **경로가 `/api/` 로 시작**. 앱 origin 이 없는 판(`Target::Missing`, 개인판)은 아무것도 가로채지 않는다(download.rs:55-57). 경로 패턴·`download` 속성·`_blank` 여부·MIME 은 **보지 않는다**.

`take_over_api_link`(lib.rs:297-345) 순서 — 별도 스레드 `shell-download`(298-300):
1. 메인 창을 찾는다 — 없으면 **로그 없이** 끝(301-303)
2. `window.cookies_for_url(url)` — 실패 시 `[shell][download] 쿠키를 읽지 못했다` + 실패 알림(305-312). macOS wry 는 쿠키를 `getAllCookies` 로 받아 **1초** 기다리고(wry `wkwebview/mod.rs:1446-1462`), `cookie.domain() == url.domain()` 인 것만 남긴다(mod.rs:1177-1198). 세션 쿠키는 Domain 없이 host-only 로 심는다(`backend/src/ax_workspace/entrypoints/http.py:691-697`)
3. 다운로드 폴더 — 실패 시 로그 + 실패 알림(314-321)
4. `download::fetch`(download.rs:387-426): ureq GET · 리다이렉트 0 · 연결 30초/응답 60초/본문 600초(38-48) · native-tls + OS 신뢰 저장소(390-396)
5. 판정 `judge`(download.rs:370-381): 2xx 아님 → `Refused` → **실패 알림**(lib.rs:331-335) · 2xx + `attachment` → 저장 → **성공 알림**(323-326) · **2xx + `attachment` 아님(`inline`·헤더 없음) → 로그만 남기고 알림도 없이 끝**(lib.rs:327-330 — 「결정 X」, 주석 lib.rs:292-294)
6. 알림 `notify_download`(lib.rs:350-362): 창의 현재 문서가 앱 origin 일 때만 `window.eval(CustomEvent "strong-hajin:download")`(download.rs:474-478). 웹은 `onShellDownload`(`frontend/src/lib/shell.ts:232-243`, 셸 전역 `__TAURI_INTERNALS__` 있을 때만 구독 — shell.ts:70-72)로 받아 토스트(`frontend/src/App.tsx:149-156`, 문구 `labels.ts:1405`~)

**서버 응답의 `Content-Disposition` (5번 판정의 입력)** — 웹 「다운로드 입구」 가 닿는 엔드포인트:

| 엔드포인트 | disposition | 근거 |
|---|---|---|
| `GET /api/meetings/{id}/export?format=html` | 항상 `attachment` | `backend/.../entrypoints/http.py:1085-1099` |
| `GET /api/inbox/mail/{id}/attachments/{aid}` · `GET /api/inbox/rooms/{id}/attachments/{aid}` | **png·jpeg·gif·webp·PDF·Markdown 이면 `inline`**, 그 밖 `attachment` | `_download` `http_inbox.py:122-134` · `INLINE_IMAGE_TYPES` `http_inbox.py:78` · `inline_media_type` `modules/meetings/material_policy.py:60-` |
| `GET /api/meetings/{id}/materials/{mid}/content` | PDF·Markdown 이면 `inline` | `http.py:1292-1310` |
| `/api/tasks/{id}/materials/{mid}/content` · `/api/work-requests/{id}/materials/…/content` · `/api/work-requests/{id}/attachments/…/content` · daily-report·material-folder content | `attachment` | `http.py:2192` · `2568` · `2590` · `1734` · `1822` |

→ **inline 판정 첨부를 셸이 가로채면(길 A·B) 아무 알림 없이 끝난다** — 이미지·PDF 첨부에서 「다운로드도 실패 토스트도 없음」 과 같은 모양이 코드상 나온다(lib.rs:327-330). 첨부가 `download` 속성 링크라 길 A·B 를 타는지는 1-2 참고.

### 1-2. `on_navigation` 허용 목록 — 무엇을 허용·취소하나 · 순서

**wry 가 셸 훅보다 먼저 하는 판정**(wry 0.55.1 `src/wkwebview/navigation.rs:50-83`):
- `WKNavigationAction.shouldPerformDownload` 가 참이면(= `<a download>` 계열, macOS 11.3+) **셸의 `on_navigation` 을 부르지 않고** `Download` 정책으로 넘긴다(68-74, `has_download_handler` 는 `on_download` 가 걸려 있어 참 — `wkwebview/mod.rs:570`). → 길 C(WKDownload → `on_download`)
- 그 밖에는 `navigation_policy_function(url)` = 셸의 `on_navigation` 결과로 Allow/Cancel(75-80)
- 응답 단계(`navigation_policy_response`, 86-105): 표시할 수 없는 MIME 이면 Download, **표시할 수 있으면(HTML·PDF·이미지) Allow** — Content-Disposition 은 보지 않는다
- tauri 는 셸 훅이 `false` 면 그대로 취소한다(tauri 2.11.6 `src/manager/webview.rs:580-596`). wry 의 정책 함수는 **URL 문자열만** 받는다 — 주 프레임/하위 프레임을 가르는 정보가 넘어오지 않는다(navigation.rs:65-77 · tauri-runtime-wry 2.11.4 `src/lib.rs:4899-4905`)

**셸 `on_navigation` 판정 순서**(lib.rs:435-463):
1. `stronghajin://` → 허용(437-439)
2. origin(`guard::origin_of` = url crate 직렬화, guard.rs:141-143)이 `nav_allow` 에 없으면 → http(s) 면 OS 브라우저로 열고, **취소**(442-454). medi-ax 의 `nav_allow` = `["https://ax.medisolveai.xyz"]` 하나(`flavors/medi-ax/shell.config.json` · config.rs:67-76 · 시험 config.rs:95-100)
3. `/api/` 면 가로채고 **취소**(457-460)
4. 그 밖 허용(461-462)

| 이동 | 판정 | 근거 |
|---|---|---|
| 같은 origin `/api/…` (주 프레임 링크 클릭) | 2 통과 → 3 에서 **가로채기 + 취소** | lib.rs:457-460 |
| `<a download href="/api/…">` | wry 가 셸 훅 전에 **Download** → 길 C(`on_download`) | navigation.rs:68-74 |
| `target="_blank"` (download 없음) | 셸 주석: macOS 는 `_blank` 도 `on_navigation` 을 먼저 지난다 → `/api/` 면 3, 아니면 4 후 `on_new_window` 가 `Deny`(macOS) | lib.rs:293-294 · 456 · 472-473 |
| `about:blank` · `about:srcdoc` (하위 프레임 포함) | origin = `"null"`(guard.rs:250 시험) → 2 에서 **취소**(http 아님 → 외부 열기 없음, 로그 `blocked origin=null`) | lib.rs:442-454 |
| `data:` | origin `"null"` → 2 에서 취소 | 같음 |
| `blob:https://ax…` | url crate 는 blob 의 origin 을 안쪽 URL 의 origin 으로 직렬화 → 2 통과, `/api/` 아님 → 허용 | lib.rs:440-462 (url crate 동작은 소스 미확인 — 조사 한계) |
| 하위 프레임의 `/api/…` (`<iframe src>` · `<object data>`) | 프레임 구분이 없어 주 프레임과 같은 판정 → **3 에서 가로채기 + 취소** | 위 wry·tauri 줄 |

**가로채기보다 먼저 취소될 수 있는 경로**: 순서상 2(허용 목록)가 3(가로채기)보다 앞이다(lib.rs:442 → 457). 앱 origin 은 언제나 `nav_allow` 의 첫 항목이라(config.rs:67-68) 같은 origin `/api/` 가 2 에서 취소되는 경로는 코드상 없다. `<a download>` 는 셸 훅 자체를 건너뛴다(navigation.rs:68).

**SH-IMP-011** — about:blank·about:srcdoc 는 위 표대로 2 에서 취소된다. PR #15(`f39eece`)는 메일 iframe 에서 srcdoc 대신 첫 문서에 써 넣는 것으로 피했다(웹 쪽). 셸은 그대로다. 프론트에서 iframe/object 를 쓰는 곳: `features/inbox/MailFrame.tsx:162`(iframe) · `features/meetings/MaterialDrawer.tsx:88`(`<object data="/api/meetings/…/content">` — 하위 프레임 `/api/` 이동이면 길 A 로 가로채져 `inline` 판정 → 아무것도 안 함. 실제로 WebKit 이 이 `<object>` 로드를 정책 콜백에 보내는지는 소스 미확인 — 조사 한계).

### 1-3. 외부 채널 판(WORK-011)의 셸 변경 — 가로채기 경로에 닿는 지점 · 회귀 후보

셸 소스를 바꾼 커밋(`git log -- frontend/src-tauri/src/{lib,download,guard,config}.rs Cargo.toml build.rs`):

| 커밋 | 날짜 | 내용 |
|---|---|---|
| `202078b` | 10-05 | WORK-010 — `download.rs` 신설, `on_navigation`/`on_new_window`/`on_download` 가로채기 |
| `d015091` | 10-06 20:40 | WORK-011 SHELL — 창 빌더를 `spawn_main_window`(lib.rs:408)로 옮김 · 트레이 「열기」가 창을 다시 만듦(lib.rs:666-681) · 닫기 = 웹뷰 파괴 · `kakao-collector` feature 판 가르기 |
| `2102772` | 10-06 23:15 | ureq feature `native-tls-no-default` → `native-tls`(Cargo.toml) |

1. **`on_navigation`·`on_new_window`·`on_download`·`on_page_load` 본문은 WORK-011 에서 한 글자도 바뀌지 않았다** — `d015091^` 와 `d015091` 의 `.on_navigation(` ~ `.build()?;` 구간(120줄)을 들여쓰기만 지우고 diff 하면 **동일**. 바뀐 것은 자리(setup 클로저 → `spawn_main_window`)와 `app.handle().clone()` → `app.clone()` 뿐이다. 즉 「WORK-011 의 on_navigation 허용 목록이 다운로드 이동·`_blank` 를 새로 취소한다」 는 가설은 코드 diff 로는 **근거가 없다**
2. **회귀 후보 ①(확정된 결함, 지금 판에서는 고쳐짐) — ureq TLS provider**: WORK-010 이 넣은 ureq 는 `native-tls-no-default` 였고(`202078b` Cargo.toml), 이 설정에서 `TlsProvider::NativeTls` 로 **https 요청을 하면 패닉**한다(`2102772` 의 Cargo.toml 주석 · 아카이브 `strong-hajin-inbox/shell-report.md` §9 의 stderr `uri scheme is https, provider is NativeTls but feature is not enabled`). `download::fetch` 도 같은 provider 를 쓴다(download.rs:390-396) → 운영(https)에서 `shell-download` 스레드가 패닉 → **로그·토스트 없이 사라진다**(패닉은 `log_event` 를 거치지 않음). 로컬(http)은 TLS 를 안 타 드러나지 않았다. dmg 이력(아카이브 `strong-hajin-inbox/_RESUME.md`): `inbox` dmg = `d015091`(결함 있음) · `inbox-fix1` = `4e48632`(고침) · `inbox-fix2` = `f0ad522`(고침). **사용자가 지금 쓰는 fix2 dmg 에는 고침이 들어 있다** — 그러니 fix2 에서도 네 갈래가 다 안 된다면 이것만으로는 설명되지 않는다. 다만 WORK-010 의 앱 실기 확인은 「pending」 으로 남아 있어(`30-work/work-010-polish3.md:270`) **https 운영에서 앱 내려받기가 한 번이라도 됐다는 기록은 찾지 못했다** — 「회귀」 라는 전제 자체가 확인되지 않았다
3. **회귀 후보 ② — 창 재생성**: 트레이 「열기」가 `spawn_main_window` 를 다시 불러 같은 라벨 `main` 의 창을 만든다(lib.rs:670-681). 훅은 매번 새로 걸린다(408-554). `take_over_api_link`·`notify_download` 는 라벨로 창을 찾는다(301, 482) — 코드상 끊기는 자리는 보이지 않는다
4. **회귀 후보 ③ — 판 가르기**: ureq·download 는 feature 와 무관하게 늘 컴파일된다(Cargo.toml `[dependencies]` · lib.rs:33). `kakao-collector` 는 수집기·트레이·커맨드 셋만 가른다(lib.rs:35-36, 655-682, 686-703)

### 1-4. 프론트의 다운로드 입구 전부

grep 범위: `frontend/src` 의 `*.ts`·`*.tsx`(시험·`.stories`·`dev/` 탐침 제외). 셸 가로채기 열의 「A/B/C」 는 1-1 표의 길.

| # | 파일:줄 | 무엇 | 모양 | 주소 | 셸이 타는 길(코드 판정) | 응답 disposition |
|---|---|---|---|---|---|---|
| 1 | `features/meetings/MeetingDetailPage.tsx:1060` | 회의록 내보내기 | `<a href>` 같은 탭 · download 없음 · target 없음 | `/api/meetings/{id}/export?format=html` (`lib/api.ts:1391-1392`) | **A** (가로채기) | attachment → 저장·토스트 |
| 2 | `features/meetings/MaterialDrawer.tsx:66` | 회의 자료 「받기」 | `<a href>` 같은 탭 | `/api/meetings/{id}/materials/{mid}/content` (`api.ts:1428-1430`) | **A** | PDF·MD 면 inline → **무알림 끝** |
| 3 | `features/meetings/MaterialDrawer.tsx:88` | 회의 자료 PDF 미리보기 | `<object data>` | 같은 주소 | 하위 프레임이면 A(1-2 표) | inline |
| 4 | `features/inbox/InboxAttachments.tsx:40` (`DownloadLink` — 쓰임 :60 `FileCard`, :146) | 슬랙·카톡 파일 카드 받기 · 메일 파일 카드(`MailView.tsx:413` → `FileCard`) | `<a download={name} target="_blank">` | 방: `/api/inbox/rooms/{id}/attachments/{aid}` (`api.ts:1676-1679`, `RoomView.tsx:538`) · 메일: `/api/inbox/mail/{id}/attachments/{aid}` (`api.ts:1668-1670`) | **C**(wry `shouldPerformDownload`) — `_blank` 와 겹칠 때 WebKit 이 어느 콜백을 먼저 부르는지는 미확인(조사 한계) | 이미지·PDF·MD inline, 그 밖 attachment |
| 5 | `features/inbox/MailView.tsx:401` | 메일 이미지 첨부 받기 | `<a download target="_blank">` | 메일 첨부 | 4 와 같음 | 이미지라 **inline** |
| 6 | `features/inbox/InboxAttachments.tsx:79-91` (`downloadAll`, 단추 :103) | 「모두 다운로드」 | JS 로 `<a download>` 만들어 `click()`, 300ms 간격 | 방·메일 첨부 | **C** | 위와 같음 |
| 7 | `features/inbox/InboxAttachments.tsx:162` (`Thumb`, 쓰임 :177 · :194 · `MailView.tsx:394`) | 이미지 눌러 원본 보기 | `<a target="_blank">` download 없음 | 방/메일 첨부 원본 | **A**(macOS `_blank` 가 on_navigation 먼저) 또는 B | 이미지라 inline → **무알림 끝** |
| 8 | `features/work/WorkModals.tsx:1936` | 업무 자료 열기 | `<a target="_blank">` | `item.url ?? /api/tasks/{id}/materials/{mid}/content` (`api.ts:347-349`) | `/api/` 면 A/B, 외부 링크(`item.url`)면 허용 목록 밖 → OS 브라우저 | attachment |
| 9 | `features/work/WorkModals.tsx:4306` · `:4334` | 업무 요청 첨부 | `<a target="_blank">` | `/api/work-requests/{id}/attachments/{aid}/content` (`api.ts:1115-1117`) | A/B | attachment |
| 10 | `features/chat/MessageList.tsx:782` | 근거 「원본 열기」 | `<a target="_blank">` | `item.origin`(서버 값) | `/api/` 면 A/B, 외부면 OS 브라우저 | 주소에 따라 |
| 11 | `features/chat/AssistantMarkdown.tsx:199` | AX 답의 일반 링크 | `<a target="_blank">` | 마크다운 href | 같음 | — |
| 12 | `features/inbox/RoomView.tsx:158-168` · `:658-668` · `features/inbox/inboxStream.ts:91-101` (`openLink`) | 메시지 링크 · 슬랙에서 열기 | `preventDefault` → `openExternal`(셸 커맨드 `open_external`, `lib/shell.ts:185-188`) · 셸 없으면 `window.open(_blank)` | 외부 URL | 셸 커맨드 → OS 브라우저(lib.rs:241-246) | — |
| 13 | `features/inbox/MailFrame.tsx:117-128` | 메일 본문 안 링크 | iframe 클릭 가로채 `openLink` | 외부 URL | 12 와 같음 | — |
| 14 | `App.tsx:704-709` | 리소스 원본 열기 | `openExternal` → 없으면 `window.open` | 외부 | 12 와 같음 | — |
| 15 | `features/settings/consent.ts:26-28` | OAuth 동의 | `openExternal` → 없으면 `location.assign` | 외부 | 12 와 같음 | — |
| 16 | `features/settings/KakaoSection.tsx:215` | 「Mac 앱 받기」 | `<a target="_blank">` | `copy.downloadAppUrl` | 허용 목록 밖이면 OS 브라우저 | — |
| 17 | `features/inbox/inboxStream.ts:100` · `App.tsx:709` | 셸 없을 때 폴백 | `window.open(_blank)` | — | (웹 전용) | — |
| 18 | `features/inbox/InboxAttachments.tsx:286` | 슬랙 링크 미리보기(unfurl) 제목 | `<a target="_blank">` | 외부 URL | 허용 목록 밖 → OS 브라우저(lib.rs:442-453) | — |

grep 결과 **없음**: `createObjectURL`·`new Blob` 로 받기(`new Blob` 1건은 녹음 `features/browser/liveTranscription.ts:43` — 받기 아님) · `location.href =` 로 받기 · `fetch` 후 저장(`readMeetingMaterialText` `api.ts:1433-1437` 는 글자 읽기). 즉 **blob 다운로드 입구는 0건**이다.

### 1-5. 셸 로그가 남는 자리

- 셸 로그는 전부 `println!` 로 **표준 출력**에만 간다 — `log_event`(lib.rs:188-194, 형식 `[shell][태그] t=<ms> …`) · `download.rs:299`(격리 표식). 파일·OS 통합 로그로 쓰는 코드는 없다(`println!/eprintln!` 은 lib.rs 1 · download.rs 3 · kakao/ 13, 파일 쓰기 0)
- Finder·Dock 으로 띄운 앱의 표준 출력은 보이지 않는다. 이전 결함도 **설치된 서명 바이너리를 터미널에서 띄워** stderr 로 잡았다(아카이브 `strong-hajin-inbox/shell-report.md` §9)
- 내려받기와 관련된 태그: `[shell][nav] allowed|blocked origin=…`(lib.rs:452, 461) · `[shell][download] saved|not-attachment|refused|failed via=… path=…`(324, 329, 333, 337) · `쿠키를 읽지 못했다`(308) · `webview-download success=…`(532) · `웹 앱 문서가 아니라 결과를 알리지 않는다`(356). 패닉은 `thread 'shell-download' panicked at …` 로 stderr 에 나온다
- **로그 없이 끝나는 자리**: 메인 창을 못 찾음(lib.rs:301-303) · `/api/` 가로채기 이동은 `nav` 로그를 남기지 않음(457-460 은 `log_event` 전에 return — `take_over_api_link` 의 결과 로그만 남는다) · `on_download` `Requested` 성공(513-515)

## 2. SH-IMP-001 — AX 회의 생성 카드 vs AX 업무 생성

### 2-0. 채팅 서랍이 카드를 고르는 순서
`frontend/src/features/chat/MessageList.tsx:295-333` — ① `edit_contract.editor === "command"` → `CommandConfirmationForm`(295-301) ② `"task_progress_batch"` → `ActionProgressBatchCard`(302-307) ③ `axDraftFromAction(action)` 참 → **`AxDraftCard`**(308-315) ④ `editor === "task"` → `ActionTaskCard`(316-323) ⑤ `editor === "meeting"` → **`ActionMeetingCard`**(324-331) ⑥ 그 밖 `ActionResultCard`(333).
`axDraftFromAction` 은 `editor==="task"` 이면서 kind 가 `ax.task.create_self`·`ax.work_request.create` 인 것만 잡는다(`features/action/AxDraftCard.tsx:35`, `:41-43`, `:64-65`). ③이 ④보다 앞이라 **AX 업무 생성은 채팅에서 `ActionTaskCard` 에 닿지 않는다.**

### 2-1. AX 업무 생성(스텝 바이 스텝) — `AxDraftCard`
- 같은 카드가 모달(`AxDraftModal`, AxDraftCard.tsx:499-567)로 `features/today/TodayPage.tsx:437` · `features/work/MyWorkPage.tsx:1347` 에서도 쓰인다
- 「스텝」 은 입력 마법사가 아니라 **읽기 전용 요약 4쪽**이다 — 이름 `["기본 정보","체크리스트","업무 연결","자료"]`(`lib/labels.ts:1360`). 카드 자체는 아무것도 고치지 않는다(주석 AxDraftCard.tsx:26-28)

| 쪽 | 내용 | 파일:줄 |
|---|---|---|
| 0 기본 정보 | 갈래·기간·담당 후보(요청만)·참조자·결재자·내용(2줄) | AxDraftCard.tsx:179-195 |
| 1 체크리스트 | 항목 한 줄씩 | :197-200 |
| 2 업무 연결 | 상위·프로젝트·**참고**(`reference_task_ids`)·선행 | :202-215 |
| 3 자료(참고자료) | 파일·링크 이름(`materials`) | :217-225 |

- 빈 값은 「없음」(:154-161) · 쪽당 최대 7줄, 넘치면 「외 N개」(:138, :145-148)
- 머리: AX 배지 · 「초안 · N회차」/「거절됨」 · 업무 생성/업무 요청(:347-353) · 4칸 진행 막대 = 탭 단추(:354-367) · ‹ › 단추(:380-383) · 화살표 키(:295-303) · 트랙패드 스와이프(:306-316)
- 단추(`state === "pending"` 일 때만, :388-420): **거절**(사유 필요하면 `ReasonPrompt` :474-488, :391-400) · **수정**(연필 — `save` 커맨드 + 고칠 필드가 있을 때 :263 → `CreateWorkModal` 을 포털로 열고 `save_draft` :422-473, 그 모달의 주 단추는 「저장」 `features/work/WorkModals.tsx:5461`) · **등록**(`confirm` + `base_submission_version`·`draft`·정렬된 `attachment_draft_ids` :286-293, :415-419)
- `data-state`: 승인 후 접힌 한 줄 카드는 `"approved"` **하드코딩**(:318-336, 속성 :323) · 그 밖 `source.state`(pending/rejected, :345) · `data-page`(:344)
- 참고자료 **입력**은 `CreateWorkModal` 안에서만 — `stageActionMaterialFile`·`stageActionMaterialLink`·`discardActionMaterialDraft`(`WorkModals.tsx:4693-4740`) → 카드로 `onMaterialsChange`(AxDraftCard.tsx:433-434, :253-254)
- 서버: `CONFIRM_LABELS["task.create_self"] = "이 내용으로 업무 생성"`(`backend/…/modules/actions/policy.py:21`) — 카드는 쓰지 않고 「등록」 고정(`labels.ts:1385`) · `save_draft` 는 `DRAFT_SAVE_ACTION_TYPES = {task.create_self, work_request.create}`(policy.py:32-35, :134-136) · 채팅의 커맨드 목록 confirm → save_draft → reject(`backend/…/platform/actions.py:530-540`) · task 편집 계약 필드(actions.py 약 1743-1857, `editor` 키 :1852) · 첨부 가능 종류 `{task.create_self, task.assign, meeting.reservation.create}`(`modules/actions/confirmation.py:38-40`)

### 2-2. AX 회의 생성 확인 카드 — `ActionMeetingCard`
- 루트 `<section className="scax-actioncard action-task-card action-meeting-card" data-action-id data-state={action.state} data-view={editing ? "editing" : action.state}>`(`features/action/ActionMeetingCard.tsx:239`) — `data-state` 는 `action.state` 그대로(`"pending"|"approved"|"rejected"`, `lib/viewModels.ts:765`), `data-view` 에 `"editing"` 이 더해진다
- 읽기 모드 필드(`MeetingSummary`, :73-95): 주제(굵게)·목적 · `dl` 주최자·참석자(없으면 「없음」)·날짜·시간. 서버 preview(`platform/actions.py:1309-1327`)에는 장소·외부 참석자도 있으나 **카드가 그리지 않는다**
- 배지: 초록 「회의」 하나(:241-243) — AX 배지·회차 배지 없음
- 편집 모드(`MeetingDraftFields`, :357-505): 회의 명*·목적·장소(자유 입력 `#action-meeting-location` :417-427)·주최자(계약에 `host_id` 있을 때만 :430-438)·참석자(`MultiSelect`)·날짜+시간(같은 날) 또는 `datetime-local` 둘(여러 날). 서버 판이 바뀌면 갱신 배너(:246-255)
- 참고자료(첨부): `ActionTaskCard` 의 `TaskAttachmentGroup` 공유(:12) · 읽기(:281-300) · 편집(:262-276) · 업로드 `stageActionMaterial*`(:199-236) · 묶음 제목 「첨부」(`ActionTaskCard.tsx:702-705`) · 고르개 부제 「회의에 필요한 자료를 찾아 연결하세요.」(:780-781)
- 단추(:310-351): 수정 · 취소/초기화 · 등록/저장(**「저장」 도 confirm** — `save_draft` 아님 :324-344) · 그 밖 서버 커맨드(:346-348) · 회의 상세 보기(:349-351). **거절 단추가 없다** — 서버는 `reject` 를 보내지만(actions.py:539) 카드가 confirm·reject 를 걸러낸다(:346)
- 서버 계약 `_meeting_edit_contract`(`platform/actions.py:2064-2103`): `title, purpose, starts_at*, ends_at*, location, attendee_ids, external_attendees, agendas, carried_from_meeting_id, room_id` — `host_id` 없음(→ 주최자 칸 안 그려짐) · `reference_task_ids` 없음 · `save_command` 없음 · `"warnings": []` 하드코딩(:2102) · 확정 문구 「이 내용으로 회의 생성」(policy.py:24, 카드는 안 씀)

### 2-3. 갈라지는 자리

| 영역 | 업무 `AxDraftCard` | 회의 `ActionMeetingCard` | 공유 |
|---|---|---|---|
| 루트 클래스 | `scax-actioncard ax-draft-card`(AxDraftCard.tsx:342) | `scax-actioncard action-task-card action-meeting-card`(ActionMeetingCard.tsx:239) | `scax-actioncard` 만 |
| 배치 | 높이 고정 4쪽 + 진행 막대(:354-386) | 긴 카드 한 장 · 읽기/편집 전환(:244-302) | 따로 |
| 배지 | AX + 초안·N회차 + 종류(:348-352) | 회의(:242) | ds `Badge` 만 |
| 편집 | 바깥 `CreateWorkModal` 포털(:427-471) | 인라인 `MeetingDraftFields`(:256, :357) | 따로 |
| 초안 복구·갱신 배너 | 없음 | `useActionDraft` + 배너(:114-121, :246-255) | `ActionTaskCard` 와 공유 |
| 참고자료 | 4쪽 「자료」 읽기(:217-225) + 모달 입력 | `TaskAttachmentGroup`(:262, :282) | 따로 (회의는 ActionTaskCard 와 공유) |
| 참고 업무 | 「참고」(:211) | 계약에 없음 | — |
| 확정 | 등록 → `confirmPayload()`(:286-293, :416) | 등록/저장 → confirm + draft(:333-339) | 페이로드 모양만 같음 |
| 초안 저장 | `save_draft`(:442) | 없음(「저장」=confirm) | 의미 다름 |
| 거절 | 있음(:391-400) | 숨김(:346) | 다름 |
| 승인 뒤 | 접힌 한 줄 + 업무 열기(:318-336) | 같은 카드 + 회의 상세 보기(:349-351) | 다름 |
| 스타일 | `.ax-draft-card*`(`styles/ax.css:618-651`) | `.action-task-card*`(ax.css:372-539) + `.action-meeting-card` 덮어쓰기(ax.css:452, 456, 457) | 회의 = 업무 카드 CSS 변형 |

`.action-meeting-note-section`(ax.css:454-457)은 TSX 에서 쓰는 곳이 없다.

## 3. SH-IMP-002 · 004 — 회의 정보 수정 모달 겹침

> 픽셀 값은 **CSS 로 계산한 추정**이다(실측 아님 — 브라우저를 띄우지 않았다).

### 3-1. 그리드·열
- 모달 `.modal.meeting-modal-wide`(`features/meetings/MeetingEditModal.tsx:139`): `.modal { padding: 24px }`(`styles/components.css:522`) · `.meeting-modal-wide { width: min(760px, 100%) }`(`styles/meetings.css:154`) · 본문 `overflow-y: auto`(components.css:655)
- 두 열 `.meeting-meta-edit { display:grid; grid-template-columns: 2fr 3fr; gap: 20px }`(meetings.css:143) → 내용 폭 ≈712px 에서 왼쪽 ≈276.8px · 오른쪽 ≈415.2px. 왼쪽 열 감싸개에 인라인 `minWidth: 0`(MeetingEditModal.tsx:157) → 트랙이 내용에 맞춰 늘지 않는다
- 왼쪽 `[날짜][시작][종료]` 줄 `.meeting-when { display:flex; gap:8px }`(meetings.css:148, 마크업 MeetingEditModal.tsx:175-198)
  - `.meeting-when .date-field { flex: none; width: 200px }`(meetings.css:149) — **날짜 200px 고정**
  - `.meeting-when .time-range { flex: none }`(meetings.css:150) — 시간쌍은 줄지 않는다. `.time-range { display:flex; gap:8px }`(components.css:620), 각 시각은 `.select-trigger`(components.css:590 · `ds/TimeField.tsx:150-153`) — 최소폭·말줄임 없음
  - 줄 폭 ≈ 200 + 8 + (≈86×2 + 대시 + 8×2 ≈195) ≈ **400px** > 왼쪽 열 ≈277px → **≈125px 넘침**, 오른쪽 열(≈297px 부터)에 ≈105px 걸침 = 종료 시각 트리거 거의 전부. 잘라 내는 규칙 없음
- 오른쪽 열: 라벨 → `PickedTags` → `marginTop:12` div → 검색 입력(MeetingEditModal.tsx:215-238). `PickedTags` 는 비면 안 그려지고(`PeoplePicker.tsx:213`) 있으면 ≈50px 상자(:215-224). 회의 만든 사람은 늘 참석자라(`backend/…/modules/meetings/application.py:312`) 보통 태그 상자가 있다 → 검색 입력 세로 위치(≈96-130px)가 날짜/시간 줄(≈98-132px)과 겹친다
- 겹칠 때 위아래: 검색 입력의 부모 `div.popover-root` 인라인 `position: relative`(PeoplePicker.tsx:38) · 시각 트리거의 부모 `span.popover-root`(`ds/Popover.tsx:139`, `position: relative` meetings.css:85) — 둘 다 `z-index: auto` → **DOM 순서상 뒤인 검색 입력이 종료 시각 위에** 그려지고, 검색 입력 배경이 불투명(components.css:737)이라 겹친 부분은 가려진다

### 3-2. 검색 입력 뒤 「단추」 의 정체
- `PersonSearch` 는 `<input class="search-input-box" role="combobox" aria-label={placeholder}>` 하나와, 검색어가 있을 때만 뜨는 listbox 팝오버뿐(PeoplePicker.tsx:39-49, :50-95). 수정 모달 오른쪽 열에 다른 요소 없음(MeetingEditModal.tsx:215-239) → **검색 입력 옆 실제 단추 요소는 없다**
- 보이는 「단추」 는 넘친 **종료 시각 트리거** `<button class="select-trigger" aria-label="날짜 · 시간 종료 시각">`(TimeField.tsx:139-153, 라벨 TimeField.tsx:250-260 + `labels.ts:551`) — 누르면 시각 고르개 팝오버를 연다. 위 계산과 맞는다(실측 확인은 조사 한계)

### 3-3. 같은 모달을 쓰는 화면
- `MeetingEditModal` 을 여는 곳은 **한 곳** — 회의 목록 카드의 [수정](`status === "scheduled"` 일 때, `features/meetings/MeetingListPage.tsx:409-416` → `setEditing` :246, 261, 273 → 렌더 :311-322). 상세 화면은 더 열지 않는다(`MeetingDetailPage.tsx:977`)
- **생성은 다른 컴포넌트** `BookingModal` — 같은 `.meeting-modal-wide`·`.meeting-when` 클래스(`BookingModal.tsx:286, 362`)지만 한 열 `form-stack`(:300), 그 줄에 [지금] 단추(`marginLeft:auto`, :388-397). 여는 곳: 목록 「회의 생성」(MeetingListPage.tsx:186, 326-341) · 상세 「다음 회의 예약」(MeetingDetailPage.tsx:1064-1067, 1391-1410)
- **AX 카드 편집도 다른 컴포넌트**(`ActionMeetingCard.tsx:395-495`) — `.action-meeting-schedule { grid-template-columns: minmax(0,1fr) minmax(0,1fr) }`(ax.css:431), 시각 트리거를 줄인다(ax.css:438-441). 사람 검색 입력 없음

## 4. SH-IMP-003 · 016 — 장소 입력

- `input#meeting-head-place` 를 쓰는 곳 **한 곳** — `MeetingEditModal.tsx:201-212`. 자유 입력, placeholder 「회의실 이름을 적으세요」(`labels.ts:982`), 주석 「여기서 회의실 예약은 하지 않는다」(:200)
- 저장 경로: `updateMeetingInfo(..., { location: head.place.trim() || null })`(MeetingEditModal.tsx:119-125) → `PATCH /api/meetings/{id}`(`lib/api.ts:1244-1256`) → `backend/…/entrypoints/http.py:965-975` → `bootstrap/application.py:1737-1746` → `meeting.location = normalize_optional_text(...)`(`modules/meetings/application.py:519-520`), 컬럼 `location String(300)`(`platform/persistence.py:305`). 장소만 바꾸면 예약은 건드리지 않는다 — 예약 동기화는 `starts_at`·`ends_at` 이 바뀔 때만(`bootstrap/application.py:1742-1744`)
- 다른 장소 입력: AX 카드 `#action-meeting-location`(자유 입력, `ActionMeetingCard.tsx:417-427` · 계약 필드 `platform/actions.py:2087`). 생성(`BookingModal`)에는 장소 글자 입력이 없고 `bookMeeting` 이 `location` 을 보내지 않는다(`api.ts:1219-1230`, 서버는 받을 수 있음 `commands.py:140`)
- **회의실 고르기 UI 는 `BookingModal` 에만** — 라디오 목록 + 기본 「회의실 선택 안 함」(`BookingModal.tsx:506-525`, `labels.ts:860`) · 목록 `readMeetingRooms` → `GET /api/meetings/rooms`(BookingModal.tsx:124-160 · `api.ts:1468-1471` · `http.py:931-947`) · 서버 게이트웨이 `TheConnectGateway`(`bootstrap/application.py:1030-1041`) · 예약 성공 시 `location = reservation.room_name`(`bootstrap/application.py:1615`). 수정 모달·AX 카드에는 회의실 고르개가 없다

## 5. SH-IMP-005 — 「이전 회의 정보 불러오기」

### 5-1. 단추 위치·동작
- 「이전 회의 정보 불러오기」 라는 문구는 코드에 **0건**. 실제 UI 는 `BookingModal` 의 제안 카드 — 제목 「지난 「{주제}」」(`labels.ts:869`) + [불러오기](`labels.ts:870`, `BookingModal.tsx:327-354`). 입력한 주제가 지난 회의 제목과 **정확히 같을 때만** 뜬다(:174-180). 상세 화면에서 연 예약 모달은 `pastRows={[]}`(`MeetingDetailPage.tsx:1392-1410`)라 안 뜬다
- `applySuggestion`(`BookingModal.tsx:198-235`, 주석 :198 「일시 · 장소 · 참석자 · 목적을 넣고」) — `readMeeting(picked.meeting_id)` 결과로:
  - **날짜·시작·종료를 그대로 넣는다** — `setDate(meetingDateInput(starts_at))` · `setFrom(meetingClock(starts_at))` · `setTo(meetingClock(ends_at))`(:205-207). **시간은 화면이 넣는다.** 서버는 과거 날짜를 막지 않는다(시작<종료·시간대만, `modules/meetings/domain.py:232-239`)
  - 목적: 비어 있을 때만(:208) · 회의실: `location` 과 이름이 같은 방(:209) · 참석자: 명단에 있는 사람만(:210-214)
  - 안건: 최종 벌(`track === "final"`)·결론 안 난 것만, 제목 중복 제외, 화면 표시용 `source: "carried"`(:215-228)
  - `setCarried(meeting_id)`(:229)

### 5-2. 안건 출처 문구
- 그리는 자리: `AgendaBlock.tsx:155` ← `source={meetingAgendaSourceText(agenda.source)}`(`MeetingDetailPage.tsx:1210`). **서버의 `agenda.source` 하나로만** 고른다(`labels.ts:749-759`)

| `source` | 문구 |
|---|---|
| `manual` | 직접 입력 |
| `set` | 세트 |
| `carried` | 지난 회의에서 넘어옴 |
| `derived` | 다른 회의에서 파생 |
| `null`(AI·최종 벌) · 모르는 값 | 문구 없음(안 그림) |

  같은 클래스가 결론 남/결론 안 남(`AgendaBlock.tsx:151`, `labels.ts:824-825`)과 「할 일 없음」(AgendaBlock.tsx:217)에도 쓰인다
- 서버가 정하는 법: 프론트는 **제목만** 보낸다 — `agendas.map(a => ({title}))`(`BookingModal.tsx:251`, `api.ts:1228`), 서버도 제목만 취한다(`http.py:923`). 모달 안 행별 manual/carried(BookingModal.tsx:43, 425, 437)는 **화면용이고 보내지 않는다**
- 생성 때 `source = "carried" if carried is not None else "manual"`(`modules/meetings/application.py:415`, carried 는 :412 `_carried_source(principal, carried_from_meeting_id)`) — 이 한 값을 **모든 안건**에 단다(:327-331). → [불러오기] 를 누르거나 「다음 회의 예약」(`MeetingDetailPage.tsx:1393`)으로 만들면 **손으로 쓴 안건도 `carried` = 「지난 회의에서 넘어옴」**
- 생성 뒤 더한 안건은 메모 벌 `manual`, 그 밖 `null`(application.py:1225) · 빠른 시작(:467)·메모 폴백(:564)도 `manual`. **`set`·`derived` 를 쓰는 서버 코드는 0** — 허용 목록(`domain.py:140`)·시험 fixture(`MeetingAfter.test.tsx:236`)에만 있다

## 6. SH-IMP-015 · 008 · 010 — 이미 정한 구현의 화면 쪽 시작점

### 6-1. 메시지 행 · 스레드 줄 · 스레드 패널 (`features/inbox/RoomView.tsx`)
- 행 = `Message`(294-357): 바깥 `<div className="scax-imsg [--grouped|--sending|--failed|--active]" data-message-key>`(316-321) → `.scax-imsg__gutter`(아바타/옆 시각, 322-324) + `.scax-imsg__main`(325-354: 머리 326-332 · 본문 333-337 · unfurl 338-340 · `AttachmentList` 341 · 로컬 파일 342-350 · `Reactions` 351 · `SendState` 352 · `ThreadLine` 353 — `!inPanel && onOpenThread` 일 때). **행동 막대 자리·슬롯 없음.** 스레드 패널도 같은 `Message` 를 `inPanel` 로 쓴다(부모 488 · 답글 495)
- CSS(`styles/inbox.css`): `.scax-imsg` = grid `40px minmax(0,1fr)`, **`position` 없음**(133) · `--active`(255). **`.scax-imsg:hover` 규칙 0** — 호버 규칙은 자식 `.scax-imsg-link:hover`(152)·`.scax-thread__line:hover`(173)뿐
- 답글 0개에서 막히는 것: `toLine` 이 `replyCount > 0 && (!thread_key || thread_key === key)` 일 때만 `thread` 를 채운다(RoomView.tsx:87, 100-107; 카톡 81·로컬 126 은 늘 null) → `ThreadLine` 이 null(277) → **`onOpenThread` 를 부르는 UI 는 이 줄뿐**(280). 패널 쪽에는 답글 수 조건이 없다 — `threadKey`(526) · `onOpenThread={kakao ? undefined : () => setThreadKey(line.key)}`(709) · `parent = lines.find(...)`(628) · 렌더 조건 `parent && !kakao`(740) · 조회 `getInboxRoomMessages(roomId, { threadTs: parent.key })`(459, `api.ts:1645-1651` → `http_inbox.py:180-191` → `modules/external_channels/inbox.py:606-612` → 저장소 `thread_key == ts OR external_key == ts` `platform/external_channels_inbox_store.py:214-215`) · 머리 개수 `Math.max(replies.length, parent.thread?.count ?? 0)`(490) · 답장 `sender.send(text, files, parent.key)`(499 → 387, 서버 `accept_slack_reply` 는 `thread_ts` 공백만 검사 `inbox.py:783`, 카톡 거절 768-769). 남는 조건 = 입구 없음 · 카톡 · 부모가 불러온 최상위 `lines`(604, `inboxModel.ts:458-461`) 안에 있어야 함. 동기화는 `reply_count` 있고 `thread_ts == ts` 인 부모만 답글을 받는다(`modules/external_channels/sync.py:383`)

### 6-2. 카톡 대화 화면
- 같은 컴포넌트다 — 메일 아닌 카드는 모두 `RoomView`(`InboxPage.tsx:292`), `kakao = card.kind === "kakao"`(RoomView.tsx:520)로 가른다: `toLine` 카톡 분기(67-85, `thread: null`) · 스레드 입구 끔(709) · 패널 숨김(740) · 작성창 숨김(727) · 「슬랙에서 열기」 숨김(655). 행 `Message` 는 같다

### 6-3. 메일 머리
- `features/inbox/MailView.tsx:358-364` — `div.scax-mail__top` > `h2.scax-mail__title`(359) + `div.scax-mail__actions` > [답장](361)·[전체 답장](362)(작성 중이면 비활성) · `dl.scax-mail__head`(365~) · CSS `inbox.css:33`, `:215-217` · 문구 `labels.ts:1444-1445`

### 6-4. AX 채팅 서랍을 다른 화면에서 열고 보내기
- `App.tsx`: `isAxOpen`(186) · `chat = useConversations({ personaId, isOpen: isAxOpen, ... })`(210) · 닫혔을 때 런처(609-624, `onOpen` → `setIsAxOpen(true)` 620, `onPrefill` 은 초안만 621) · 서랍(648-650)
- `chat.send(` 는 한 곳 — `onFollowUpCandidate`(666, context `[]`). 나머지는 `chat.sendCurrent` — `askAx`(310) · `sendMessage`(317, 서랍 `onSend` 739)
- **「서랍을 열며 보내는」 기존 사례 = `askAx`**(App.tsx:307-311: `setIsAxOpen(true)` → `await chat.start()` → `await chat.sendCurrent(text, [])`). `TodayPage` 에만 `onAskAx` 로 넘긴다(App.tsx:481 → `TodayPage.tsx:50`, 호출 :290). `InboxPage` 등 다른 화면은 받지 않는다. 주석 App.tsx:300-305 — 맥락 첨부 입구를 걷어내 지금은 맥락 없이 보낸다
- 참고 자료: 타입 `ConversationContextReference = { resource_type: "task" | "work_request"; resource_id; resource_version; included }`(`lib/viewModels.ts:1030-1035`) · `Conversation.context_references`(viewModels.ts:953) · `LocalFragment.context`(`useConversations.ts:28`) · 합침 :83 · 보냄 :319. **말풍선에 칩을 그리는 코드는 0** — `features/chat/*.tsx`(시험 제외)에서 `context` 0줄, `context_references` 를 읽는 곳은 `useConversations.ts:83` 하나
- API: `sendConversationMessage(conversationId, body, context, idempotencyKey, followUpCandidateId?)`(`lib/api.ts:744-756`) → `POST /api/conversations/{id}/messages` `{body, context, follow_up_candidate_id}` + `Idempotency-Key`

### 6-5. 설정 연동 화면 숫자
- 읽는 곳: `SettingsPage.load` → `listIntegrations()`(`features/settings/SettingsPage.tsx:146-160` → `GET /api/integrations` `api.ts:1552-1554`) → `loadRooms` → `listIntegrationRooms(id)`(SettingsPage.tsx:127-136 → `GET /api/integrations/{id}/rooms` `api.ts:1571-1573`). 서버가 `synced_count`·`last_synced_at`·`backfill_count`(`modules/external_channels/application.py:661-663`)·방 `synced_count`(:694)를 채운다
- 그리는 곳: 메일 `IntegrationSections.tsx:56`(합계)·:61(`LiveStrip`)·:70(「적재 N건 · 마지막」)·:73(「과거 메일 채우는 중 · N건」, `labels.ts:1565`) · 슬랙 :233 · 카톡 `KakaoSection.tsx:243`, :257 · `LiveStrip` 문구 「마지막 수집」·「DB 적재 건수」(`settingsParts.tsx:40`, :44 · `labels.ts:1540-1541`)
- 언제 읽나: 마운트(SettingsPage.tsx:162-166) · 창 focus/`visibilitychange`(168-179) · **스트림 `integration.changed` 사건과 재연결**(181-187) · 사용자 동작 뒤(258, 297, 317, 325, 352, 356)
- **설정 화면은 이미 `useInboxStream` 을 구독한다** — 정의 `inboxStream.ts:16` · `InboxPage.tsx:19`, :148 · `SettingsPage.tsx:21`, :182
- 서버 쪽: `_announce`(`platform/external_channels_sync_store.py:204-220`)는 실시간 저장 **20건 이하**(`ARRIVAL_EVENTS_PER_SAVE = 20`, :33)에는 `message.arrived` 만 내고, `integration.changed` 는 백필·큰 저장에만 낸다(215-220). 설정 화면은 `integration.changed` 외 사건을 무시한다 → 작은 실시간 수집은 숫자를 다시 읽게 하지 않는다. 그 밖 `integration.changed` 발신: `sync_store.py:354`(끊기) · `application.py:336`, 652 · `kakao_ingest.py:323` · `inbox.py:1057`

## 7. SH-IMP-013 ① — 카톡 이름 없는 방

- 방 목록 카드: `features/inbox/MessageRail.tsx:82` `<h3 className="scax-inbox-card__title">{card.title}</h3>` — **대체 문구 없음**, 빈 이름이면 빈 h3. `card.title = room.name`(`backend/…/modules/external_channels/inbox.py:537`), 컬럼 `name … nullable=False, default=""`(`platform/persistence.py:2098`) → 값은 null 이 아니라 `""`
- 방 머리: `RoomView.tsx:625` `header?.name ?? card.title` — `??` 는 `""` 를 거르지 않아 `h2.scax-room-head__title`(636)이 비고, 작성창 placeholder 가 「에 메시지 보내기」/「에게 메시지 보내기」가 된다(629, `labels.ts:1487-1488` — 카톡은 작성창을 숨김 RoomView.tsx:727)
- 서버 쪽 대체: 방 추가 때 `name=(detail.name if detail and detail.name else external_id)`(`application.py:404`), 재추가 때 비지 않은 이름만 덮음(418-419) · 슬랙 갱신 `info.name or room.name`, DM 사용자 이름·그룹 DM 멤버 이름 조합(`sync.py:469-476`). **프론트 대체 0**

## 8. SH-IMP-018 — 메일 본문 이미지 깨짐

### 8-1. 본문이 그려지기까지
| 단계 | 파일:줄 |
|---|---|
| 요청 `GET /api/inbox/mail/{id}` | `frontend/src/lib/api.ts:1641` |
| 엔드포인트(`Cache-Control: private, no-store`) | `backend/…/entrypoints/http_inbox.py:170-178` |
| 응답 필드 `safe_html` | `backend/…/modules/external_channels/inbox.py:577` |
| 안전본은 처음 열 때 만들어 저장, 판 접두가 같으면 재사용 | `inbox.py:582-602`(재사용 584-585 · `SAFE_HTML_VERSION = 2` `inbox_html.py:36,42`) |
| Gmail 파싱: 첫 `text/html` 부분 + `cid` → partId 지도 | `inbox_html.py:113-131` |
| 정제 `sanitize_mail_html` — lxml 고쳐 쓰기 → nh3 허용 목록 | `inbox_html.py:277-325` |
| 프론트 정제 없음 — 서버 안전본을 그대로 씀 | `MailFrame.tsx:10-11` |
| `<MailFrame html={mail.safe_html}>`(본문 · 답장 인용) | `MailView.tsx:384`, :153 |
| 첫 문서에 써 넣기(f39eece): `doc.open(); doc.write(html); doc.close(); prepare()` | `MailFrame.tsx:144-153`(이유 주석 20-25) |
| `prepare()`: `img[data-ax-remote-src]` 마다 load/error 를 걸고 `src` = 프록시 주소 | `MailFrame.tsx:102-114` |
| 프록시 주소(상대 · 같은 origin) | `api.ts:1682-1683` |
| iframe: `sandbox={MAIL_SANDBOX}` · `src` 없음 · `referrerpolicy` 없음 | `MailFrame.tsx:161-169`, 값 :28 |

### 8-2. 외부 `<img>` 가 막힐 수 있는 자리 전부
- **iframe sandbox** `allow-same-origin allow-popups allow-popups-to-escape-sandbox`(`MailFrame.tsx:28`) — 이미지 제한 없음. 스크립트가 없어 오류 처리는 부모의 핸들러뿐
- **CSP**: 안전본 앞에 붙는 `<meta>` `default-src 'none'; img-src 'self' data:; style-src 'unsafe-inline'`(`inbox_html.py:37-42`, 붙이는 곳 :325, :341) — 직접 `https://` 는 막히지만 서버가 원격 `src` 를 언제나 떼므로 남지 않는다. 프록시 주소는 같은 origin 이라 허용. 프록시·첨부 **응답** 헤더도 `…; sandbox` + `nosniff` + `CORP: same-origin`(`http_inbox.py:80-84`, `_download` :121-133). `frontend/index.html` CSP 0 · `deploy/k8s/nginx.conf:1-18` CSP/Referrer 헤더 0 · Tauri `"security": {}`(`src-tauri/tauri.conf.json:11`), 판 오버레이는 이름·식별자만(`flavors/medi-ax/tauri.conf.json:1-6`), `"csp"` 가 없다는 시험(`lib.rs:955-956`)
- **정제**: 원격 `src` → 떼고 `data-ax-remote-src` 로 옮김(`inbox_html.py:202-204`) · 래스터 `data:`·`cid:`·원격이 아닌 `src` → 뗌(:205-206) · nh3 는 `src` 를 래스터 `data:` 또는 `/api/inbox/mail/` 일 때만 남김(:260-265)
- **프록시** `GET /api/inbox/mail/{id}/remote-image?u=`(`http_inbox.py:242-251`, 성공 `private, max-age=86400`) — 규칙은 8-6 표
- **referrerpolicy**: 프론트 0건. 브라우저는 우리 origin 에만 요청, 상류 요청은 Referer 없음(`platform/external_inbox_upstream.py:342-344`)

### 8-3. 의도된 정책인가
- SPEC-008 은 「원격 이미지는 기본 차단(추적 픽셀), 「이미지 보기」를 누르면 서버 프록시로만」(spec-008 179-180 · AC-08b 619-622 · API 표 389 「이미지 MIME 만 · 크기 상한 … 규칙 위반=400 · 상류 실패=502」)
- 코드는 바뀌었다 — **처음부터 자동으로, 프록시로만** 받는다(사용자 결정 2026-10-06, `MailFrame.tsx:16-18`, 커밋 `7ab5b9f`). 백엔드 docstring 은 옛 「눌러 보기」 를 그대로 적고 있다(`inbox_html.py:8-9`) · 프록시 docstring 「리다이렉트는 따라가지 않는다」(`upstream:10`)도 코드(최대 3회 따라감)와 다르다
- **SVG 거절은 의도** — 「SVG 거절 — 같은 origin 에서 스크립트가 된다」(`upstream:10`, :51, :356-357)

### 8-4. 인라인 이미지(`cid:`)
- `cid` → partId 는 그 부분에 `body.attachmentId` 가 있을 때만 지도에 든다(`inbox_html.py:122-124`) → `src = /api/inbox/mail/{id}/attachments/{sha}`(`inbox.py:587-591`, aid 공식 `inbox_html.py:134-136` = `sync_messages.py:124`)
- 지도에 없는 `cid`(예: `attachmentId` 없이 `body.data` 로 실린 부분)는 `src` 를 뗀다(`inbox_html.py:196-201`)
- 중계: aid 로 부분을 찾아 사용자 Gmail 토큰으로 받는다(`inbox.py:670-700`) — 없음 404 · 끊김/상류 실패 409/502. 응답 png/jpeg/gif/webp 는 inline, 그 밖은 `attachment`(`http_inbox.py:78`, :121-133)
- `cid` 이미지에는 MailFrame 오류 핸들러가 **걸리지 않는다**(셀렉터가 `data-ax-remote-src` 만, `MailFrame.tsx:102`)

### 8-5. 웹과 앱이 다르게 막는가
- 앱은 배포된 웹 origin 을 그대로 연다(`flavors/medi-ax/shell.config.json:10` · `WebviewUrl::External` `lib.rs:425`) — 같은 번들·같은 서버라 CSP·프록시 동작이 같다
- `on_navigation`(`lib.rs:435-463`)은 **이동**만 본다 — `about:*`(origin `"null"`)는 취소(그래서 srcdoc 를 걷었다, `MailFrame.tsx:20-24`), 같은 origin `/api/` 이동은 가로챈다(:457-459). **이미지 하위 리소스 요청은 이동이 아니라 이 훅을 지나지 않는다.** 셸 CSP 없음(`lib.rs:955-956`)

### 8-6. (물음 6) 일부만 막히는 이유 — 규칙 단위 「입력 → 결과」
> 실제 메일 HTML 은 보지 못했다. 아래는 정제·프록시·CSP 규칙이 **어떤 입력을 통과시키고 어떤 입력을 막는지**다.

| 입력 | 결과 | 파일:줄 |
|---|---|---|
| `<img src="https://…">`·`http://` | `src` 를 떼고 `data-ax-remote-src` 로 → 프론트가 프록시 주소를 단다 · **오류 핸들러 있음** | `inbox_html.py:202-204` · `MailFrame.tsx:102-113` |
| 프록시: 받은 바이트가 PNG·JPEG·GIF·WebP | 보인다(inline) | `upstream:50-58` · `http_inbox.py:78`, :123 |
| 프록시: 바이트가 BMP·ICO | 받아들이지만 `INLINE_IMAGE_TYPES` 밖 → `attachment` 로 그 타입 응답. 그려질지는 엔진 몫 | `upstream:60-63` · `http_inbox.py:122-127` |
| 프록시: **SVG·HTML 등 래스터 아님**(선언 타입 무관, 바이트로 판정) | **400** → img `error` | `upstream:358-360` |
| 리다이렉트 ≤3회(매 회 같은 검사) | 따라감 · 4회 이상 → 502 · `Location` 없는 3xx → 502 | `upstream:47`, :303-316, :346-347 |
| 최종 응답이 200 아님 | 502 `http_<status>` | `upstream:348-349` |
| 5MB 초과(Content-Length 또는 실제 읽기) | 400 | `upstream:46`, :350-355 |
| 10초 초과 · TLS 오류 | 502 | `upstream:297`, :362-365 |
| DNS 실패 · 사설/비공개 IP · 포트 80/443/8080/8443 밖 · userinfo 있음 · http(s) 아님 | 502 `dns_failed` / 400 | `upstream:321-334`, 공개 판정 :246-261 |
| 접속 주소는 해석 결과를 **문자열 정렬한 첫 값**(IPv6 가 IPv4 보다 먼저 뽑힐 수 있음) | 그 주소로만 접속 | `upstream:335` |
| `u` 4000자 초과 | 422 | `http_inbox.py:244` |
| 프록시 `u` 가 그 메일 안전본의 원격 주소 집합에 없음 | 400 `remote_image_rejected` | `inbox.py:749-752` · 집합 `inbox_html.py:344-360` |
| ↳ 집합은 lxml 이 한 번 푼 속성값을 `html.unescape` 로 **한 번 더 푼다**(:357) — 주소에 엔티티처럼 읽히는 조각(예 `&copy`·`&reg`·`&not`·`&amp;`)이 있으면 프론트가 보내는 값(한 번 푼 값)과 달라진다 | 400 | `inbox_html.py:357` · `inbox.py:751` |
| `src="//host/x.png"`(프로토콜 상대) · 상대 경로 · 그 밖 스킴 | 원격으로 보지 않아(`inbox_html.py:161-162`) `src` 를 뗀다 · **원격 속성도 없어 핸들러 없음** | `inbox_html.py:205-206` |
| `data:image/png|jpeg|jpg|gif|webp` | 남김(CSP 도 `data:` 허용) | `inbox_html.py:73`, :263 |
| `data:image/svg+xml` · 그 밖 `data:` | `src` 를 뗀다 · 핸들러 없음 | `inbox_html.py:205-206` |
| `cid:` | 8-4 | — |
| `srcset` · `<picture>` · `<source>` | 허용 목록 밖 — 속성·태그 제거, 안쪽 `<img>` 는 남음 | `inbox_html.py:46-52`, :60 |
| 인라인 `<svg>` | 내용째 삭제 | `inbox_html.py:53-54` |
| img 의 `width`·`height`·`style`·`alt` | 남김 · 프레임 CSS `img{max-width:100%;height:auto}` | `inbox_html.py:55-60` · `MailFrame.tsx:39` |
| CSS `url()`(`<style>`·`style=`·body)·`background=` 의 원격 주소 | 프록시 주소로 고쳐 씀 — 같은 프록시 규칙, **오류 핸들러 없음**(실패하면 아무것도 안 그려짐) | `inbox_html.py:214-221`, :237-251, :295, :301-304 |
| 원격도 래스터 `data:` 도 아닌 CSS `url()` | `none` | `inbox_html.py:233` |
| `@import`·`expression(`·`javascript:` 가 든 CSS 선언 | 그 선언 제거 | `inbox_html.py:210`, :231-232 |

→ 「삼각형은 뜨고 Project·Deployment 는 안 뜬다」 는 **같은 메일 안에서 이미지마다 다른 규칙에 걸린다**는 뜻이고, 코드상 가를 수 있는 축은 위 표의 형식(래스터/SVG)·주소 모양(절대/상대/`//`)·엔티티 조각·상류 응답(상태·리다이렉트·크기)이다. 어느 줄에 걸렸는지는 그 메일의 `safe_html` 과 서버 로그 `remote image refused: host=… reason=…`(`upstream:310`, :315)이 있어야 갈린다(조사 한계).

### 8-7. (물음 7) 웹 「대체 텍스트」 vs 앱 「깨진 ?」
- 실패한 이미지를 alt 글자로 바꾸는 코드는 MailFrame 의 `error` 핸들러 **하나** — img 를 `<span class="ax-img-missing">{alt}</span>` 로 바꾼다(`MailFrame.tsx:106-111`). alt 가 비면 빈 span(= 빈 칸)
- 그 핸들러는 `img[data-ax-remote-src]` 에만, `src` 를 달기 **전에** 건다(:102-113)
- 핸들러가 **없는** img: `cid` 이미지 · `src` 를 뗀 img(상대·`//`·SVG `data:`) · CSS 배경 — 이들의 모양은 엔진이 정한다
- 서버 응답·번들·CSP 는 웹과 앱이 같다(8-5). 그래서 같은 img 에서 「웹 = 글자, 앱 = ?」 가 나오는 모양은 코드로는 둘 중 하나로만 설명된다 — (가) 웹에서는 핸들러가 돌았고 앱에서는 안 돌았다 (나) 그 img 에 처음부터 핸들러가 없고 Chromium·WebKit 이 실패/`src` 없는 img 를 다르게 그린다. 저장소 코드로는 둘을 가를 수 없다(조사 한계). 「Project 빈 칸」 은 alt 가 빈 이미지가 핸들러로 빈 span 이 된 모양과도, 핸들러 없는 img 가 크기 없이 그려지지 않은 모양과도 맞는다

## 9. grep 개수표

범위: 프론트 = `frontend/src` 의 `*.ts`·`*.tsx`, **시험·`.stories`·`dev/` 탐침 제외**(따로 적은 것 빼고).

| 항목 | 심볼 / 패턴 | 개수 | 비고 |
|---|---|---|---|
| 014 | `download={` (JSX) | 2 | InboxAttachments.tsx:40 · MailView.tsx:401 |
| 014 | `.download = ` (JS) | 1 | InboxAttachments.tsx:85 |
| 014 | `target="_blank"` | 12 | 1-4 표 #4·5·7·8·9·10·11·12(2)·16·18 |
| 014 | `window.open(` | 2 | App.tsx:709 · inboxStream.ts:100 (둘 다 셸 없을 때 폴백) |
| 014 | `createObjectURL` | 0 | blob 받기 입구 없음 |
| 014 | `new Blob` | 1 | 녹음(liveTranscription.ts:43) — 받기 아님 |
| 014 | `location.assign/replace/href =` | 1 | consent.ts:26 (셸 없을 때 OAuth) |
| 014 | `openExternal(` | 4 | 정의 shell.ts:185 + 호출 3(App.tsx:704 · consent.ts:28 · inboxStream.ts:99) |
| 014 | `<iframe` / `<object` | 1 / 1 | MailFrame.tsx:162 / MaterialDrawer.tsx:88 |
| 014 | `onShellDownload(` | 2 | 정의 shell.ts:232 + App.tsx:151 |
| 014 | `/api/` 주소 도우미 호출(정의 제외) | meetingExportUrl 1 · meetingMaterialContentUrl 2 · inboxMailAttachmentUrl 2 · inboxRoomAttachmentUrl 2 · taskMaterialContentUrl 1 · requestAttachmentUrl 2 | 1-4 표 |
| 014 | 셸 `log_event(` (lib.rs) | 31 | 출력은 전부 stdout |
| 014 | 셸 `println!/eprintln!` 파일별 | lib.rs 1 · download.rs 3 · kakao/ 13 | 파일 기록 0 |
| 014 | 셸 `is_api_request` 쓰임 | 6 줄 | 정의 · 창 빌더 2 · 시험 |
| 001 | `action-meeting-card` | 4 (시험 0) | ActionMeetingCard.tsx 1 · ax.css 3 |
| 001 | `action-task-card` | 46 (시험 5) | ax.css 39 · ActionTaskCard.tsx 1 · ActionMeetingCard.tsx 1 |
| 001 | `scax-actioncard`(정확한 토큰) | 31 (시험 16) | 부분 문자열(`__badges` 포함) 36 |
| 001 | `ax-draft-card` | 61 (시험 6) | AxDraftCard.tsx 21 · ax.css 34 |
| 002·004 | `search-input-box` | 7 줄 / 6 파일 | |
| 002·004 | `조직도 내 이름 검색` | 2 | labels.ts:863, 983 |
| 002·004 | `meeting-meta-edit` · `meeting-when` · `MeetingEditModal` | 5 · 5 · 12 | |
| 003·016 | `meeting-head-place` | 2 줄 / 1 파일 | MeetingEditModal.tsx |
| 003·016 | `readMeetingRooms` | 28 줄 / 10 파일 | 화면은 BookingModal 만 |
| 005 | `이전 회의 정보 불러오기` | **0** | 실제 단추 = 「불러오기」(`suggestApply` 2) |
| 005 | `scax-agenda-block__source` · `지난 회의에서 넘어옴` · `meetingAgendaSourceText` | 4 · 2 · 5 | |
| 005 | `carried_from_meeting_id` (백엔드 포함) | 14 줄 / 12 파일 | |
| 015 | `scax-imsg` (시험 포함) | 71 줄 / 5 파일 | inbox.css 42 · RoomView.tsx 26 |
| 015 | `.scax-imsg:hover` | **0** | |
| 015·008 | `isAxOpen` · `chat.send(` · `onAskAx`(시험 제외) | 7 · 1 · 4 | App.tsx · TodayPage.tsx |
| 015·008 | `ConversationContextReference` · `sendConversationMessage`(시험 포함) | 8 · 16 | 칩을 그리는 TSX 0 |
| 010 | `useInboxStream` | 5 줄 / 3 파일 | 정의 1 · InboxPage 2 · SettingsPage 2 |
| 018 | `sandbox` · `img-src` · `Content-Security-Policy` (시험 제외) | 9 · 4 · 2 | 범위 frontend/src·backend/src·src-tauri/src·index.html·deploy |
| 018 | `data-ax-remote-src` · `remote_image` · `cid:` | 4 · 14 · 3 | |
| 018 | `srcset` · `referrerpolicy` | 0 · 0 | |
| 018 | `ax-img-missing` | 2 | |

## 10. 앱 재현 때 코디가 볼 것 (SH-IMP-014)

**로그 자리**: 셸 로그는 stdout 에만 나온다(1-5). Finder 로 띄운 앱에서는 보이지 않는다 — 설치된 앱을 끄고(메뉴 막대 「종료」 — 창 닫기는 프로세스를 남긴다, lib.rs:709-718) 터미널에서 실행 파일을 직접 띄운다(이전 결함도 이렇게 잡았다 — 아카이브 `strong-hajin-inbox/shell-report.md` §9):
`/Applications/medi-ax.app/Contents/MacOS/medi-ax 2>&1 | tee ~/medi-ax-shell.log` (실행 파일 이름 = `mainBinaryName` `medi-ax`, `flavors/medi-ax/tauri.conf.json`. 설치 위치는 사용자 Mac 기준으로 확인)

**재현 순서와 갈라 볼 로그** — 한 번에 하나씩 누르고 각 줄을 본다:
1. 부팅: `[shell][boot] url=https://ax.medisolveai.xyz/ nav_allow=["https://ax.medisolveai.xyz"]`(lib.rs:604) — 판·주소 확인
2. **회의록 내보내기**(1-4 #1, 길 A) — 기대 `[shell][download] saved via=navigation path=/api/meetings/…/export name=…`(lib.rs:324). 갈래:
   - 아무 줄도 없음 → 가로채기 스레드까지 안 왔거나(창 못 찾음 lib.rs:301-303 은 무로그) 이동 자체가 셸에 안 옴
   - `refused … status=401` 등 → 쿠키(lib.rs:305-313)·서버
   - `쿠키를 읽지 못했다` → wry 1초 대기 초과(wry `mod.rs:1446-1462`)
   - `failed …` → ureq·TLS·시간 초과
   - `thread 'shell-download' panicked` → 패닉(이전 TLS 결함 모양)
   - `saved` 인데 토스트 없음 → `웹 앱 문서가 아니라 결과를 알리지 않는다`(lib.rs:356) 또는 웹 구독(`App.tsx:149-156`) 쪽. 이 경우 `~/Downloads` 에 파일이 있는지 본다 — 앱은 브라우저식 다운로드 표시가 없고 토스트가 유일한 표시다
3. **메일 파일 첨부 받기 단추**(#4, `<a download target=_blank>`) — 기대 길 C: `[shell][download] webview-download success=… name=…`(lib.rs:532). 대신 `saved|not-attachment via=navigation|new-window` 가 찍히면 WebKit 이 이 링크를 이동/새 창으로 보냈다는 뜻(1-2 미확인 지점이 갈린다)
4. **슬랙·카톡 파일 첨부 받기 단추**(#4, 방 첨부) — 3 과 같은 기대
5. **이미지·PDF 첨부**(#5, #7 썸네일 누르기) — `not-attachment … status=200 — 그대로 둔다`(lib.rs:329) 가 찍히면 「무알림 종료」 경로(서버가 `inline` — `http_inbox.py:122-127`)
6. 같은 메일·방 첨부를 **비이미지(zip·docx 등)** 와 **이미지/PDF** 로 하나씩 — `attachment`/`inline` 갈래를 서로 비교
7. 비교용: 업무 자료 열기(#8)·업무 요청 첨부(#9) — `attachment` 고정 엔드포인트라 길 A/B 만 탄다

## 11. 조사 한계

- **014 원인을 하나로 좁히지 못했다.** fix2 dmg(`f0ad522`)는 읽은 코드로는 회의록 내보내기가 저장·토스트까지 가야 한다. 실제로 어디서 멈추는지는 셸 로그(10절)가 있어야 갈린다. 사용자 Mac 의 설치 판이 fix2 인지·설치 경로도 확인하지 못했다(아카이브 `_RESUME.md` 의 전달 기록만 봤다)
- **WebKit 동작 미확인**(소스 없음): `<a download target="_blank">` 에서 `shouldPerformDownload` 와 새 창 정책 중 어느 콜백이 먼저 오는지 · `<object data>` PDF 로드가 하위 프레임 이동으로 정책 콜백을 타는지 · 셸 주석 「macOS 는 `_blank` 도 `on_navigation` 을 먼저 지난다」(lib.rs:293, 456)의 근거 실측. wry·tauri 는 로컬 cargo 레지스트리 소스를 읽었고, `blob:` origin 직렬화는 url crate 소스를 열지 않았다
- **WORK-010 이후 https 운영에서 앱 내려받기가 된 기록을 찾지 못했다** — WORK-010 앱 실기는 pending(`work-010-polish3.md:270`)이고 그 뒤 첫 dmg(`d015091`)는 TLS 결함 판이다. 「회귀」 전제는 확인되지 않았다
- **002·004** 의 폭·겹침은 CSS 로 계산한 값이다. 실제 렌더 측정(폰트·창 폭에 따른 차이)은 하지 않았다
- **018** 실제 vercel[bot] 메일의 `safe_html` 과 서버 로그(`remote image refused: host=… reason=…` `upstream:310`, :315)를 보지 못해 Project·Deployment 이미지가 어느 규칙에 걸렸는지 정하지 못했다. 웹 alt 글자 / 앱 `?` 차이도 엔진 렌더 동작이라 코드로 가르지 못했다(8-7)
- SPEC-006·DEC-005·WORK-010·WORK-011 문서는 필요한 줄만 grep 으로 확인했고 전문 대조는 하지 않았다
- 서버·앱·브라우저를 띄우지 않았고 테스트·빌드를 돌리지 않았다(브리프 §0·§4)
