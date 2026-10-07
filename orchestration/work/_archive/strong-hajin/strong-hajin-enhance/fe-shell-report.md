# SHELL 결과 보고 (frontend · 셸 코드만)

## 상태: done (011 만 · dmg 는 코디)

- 워크트리 `strong-hajin-enhance` · 커밋 없음 · 바꾼 파일 **둘**: `frontend/src-tauri/src/guard.rs` · `frontend/src-tauri/src/lib.rs`
- WP4-FE 변경(워크트리)은 건드리지 않았다 · dmg 빌드·서명·공증 안 함 · 013 ②③ 은 할 일 없음(코디)

## 1. 011 — `about:blank` · `about:srcdoc` 이동 허용

| 무엇 | 위치 |
|---|---|
| 빈 프레임 문서 판별 | `guard.rs` `is_empty_frame_document` — `scheme == "about"` 이고 `path` 가 **`blank` · `srcdoc` 둘뿐**(`about:config` 류 · `data:` 는 아님) |
| 이동 판정 한 곳 | `guard.rs` `navigation_verdict(url, nav_allow, app_origin, shell_scheme) -> NavVerdict` — **순서가 계약**: ① 셸 자기 화면 → 허용 ② **빈 프레임 문서 → 허용(011)** ③ 네비게이션 허용 목록 밖 → 취소(http(s) 면 OS 브라우저로 — `E-05`) ④ **앱 origin** 의 `/api/` → 셸이 받아 봄(U-5 · fix1 W3 — 기준은 허용 목록이 아니라 앱 origin 하나) ⑤ 그 밖 → 허용 |
| 창 훅 | `lib.rs` `spawn_main_window` 의 `.on_navigation` — 판정을 `guard::navigation_verdict` 에 맡기고, 결과대로 **지금과 같은 일**만 한다: 허용 = `true` + `nav` 로그 · 취소 = (외부면 `open_url`) + `blocked origin=… — 점유는 유지한다(L-11)` 로그 + `false` · 가로채기 = `take_over_api_link(…, "navigation")` + `false` |
| 바뀌지 않은 것 | 외부 origin 차단 · OS 브라우저 열기 · `/api/` 가로채기 조건(`download::is_api_request` — 앱 origin + `/api/`) · `on_new_window` · `on_download` · 점유(L-09 · L-11) 규칙 · 커맨드 넷/일곱 · capability · 허용 목록 |

이전 판과의 차이는 **②(빈 프레임 문서 허용) 하나**다. 판정을 함수로 뺀 것은 순서·결과를 단위 시험으로 지키려는 것이고, 창 훅의 동작(로그 문구 · 부작용)은 그대로다.

## 2. 프레임 구분이 없다(I-1) — 주 프레임 `about:blank` 허용이 안전한가

**대안(주 프레임만 가르기)은 이 판 의존성으로는 없다.**
- wry 0.55.1 의 정책 콜백은 `WKNavigationAction` 에서 **주소 문자열만** 꺼내 넘긴다(`wkwebview/navigation.rs` `navigation_policy` — `action.targetFrame()` 은 보지 않는다). tauri 2.11.6 의 `on_navigation` 도 `&Url` 하나다(`manager/webview.rs` · tauri-runtime-wry `lib.rs` `with_navigation_handler`). 프레임 정보를 얻으려면 wry 의 내비게이션 대리자를 갈아 끼우거나 wry 를 고쳐야 한다 — 이 판 범위 밖
- 그래서 **주 프레임의 `about:blank` · `about:srcdoc` 이동도 함께 허용된다**

**그래도 앱 origin 밖으로 나가지 않는 근거**
1. **내용이 없다** — `about:blank` · `about:srcdoc` 는 네트워크로 아무것도 받지 않는 빈 문서다. 외부 서버의 내용·스크립트가 창에 들어오는 길이 아니다(외부 주소는 여전히 ③ 에서 취소되고 OS 브라우저로 간다). 허용은 이 **두 이름**에 한정했다 — `about:` 다른 주소 · `data:` 는 그대로 취소한다(시험)
2. **네이티브 권한이 없다** — 그 문서에서 커맨드를 부르면 tauri 의 ACL 이 문서 주소를 원격 origin 으로 본다(`webview/mod.rs` `on_message` → `is_local_url` — `about:` 은 tauri 프로토콜도, `frontendDist`/`devUrl` 기준도, 등록된 사용자 스킴(`stronghajin`)도 아니다). 그 주소는 capability `remote.urls`(`https://ax.medisolveai.xyz/*` 하나)와 맞지 않으므로 **커맨드 넷/일곱 어느 것도 부를 수 없다**
3. **누가 주 프레임을 보내나** — 우리 웹은 주 프레임을 `about:` 로 보내지 않는다(WORK-012 I-1). 메일 본문 iframe 은 `allow-scripts` · `allow-top-navigation` 이 없는 샌드박스라(`MailFrame.tsx` `MAIL_SANDBOX`) 메일 원문이 최상위 창을 옮길 수 없다
4. **되돌아오는 길** — 혹시 주 프레임이 빈 문서가 되어도 앱 origin 은 허용 목록 안이라 다시 열 수 있다(새로고침·트레이 「열기」). 다만 주 프레임이 실제로 바뀌면 `on_page_load Started` 가 돌아 **그 창의 절전 방지 점유를 푼다**(L-09 — 문서 교체). 하위 프레임 이동은 WKWebView 가 `didCommitNavigation`(주 프레임 전용)을 부르지 않으므로 이 정리가 돌지 않는다 — 메일 iframe 은 점유와 무관하다

→ 판단: **안전하다**(빈 문서 · 권한 없음 · 우리 웹이 쓰지 않는 길). 남는 비용은 「주 프레임이 빈 문서가 되면 점유가 풀린다」 인데, 그것은 지금도 «문서 교체» 의 정해진 동작이다. SPEC-006 「이동 허용」 개정(프레임 무관 허용)은 코디 결정 몫이다(I-1)

## 3. 시험 (새 6 · 개정 1)

`guard.rs` 단위 시험(판정 함수 — 대역 앱 origin `https://ax.example.test`):

| 시험 | 단언 |
|---|---|
| `빈_프레임_문서는_허용한다` | `about:blank` · `about:srcdoc` · `about:blank#top` → 허용 |
| `빈_프레임_밖의_about_과_data_는_여전히_취소한다` | `about:config` · `about:srcdoc2` · `data:text/html,…` → 취소 · OS 브라우저로 넘기지 않음 |
| `외부_origin_은_여전히_취소하고_os_브라우저로_넘긴다` | `https://evil.example/…` · 이름이 비슷한 `https://ax.example.test.evil.example/` → 취소 + 외부 열기 |
| `앱_origin_의_api_는_그대로_셸이_받아_본다` | 내보내기 · 첨부 `?download=1` → 가로채기 · 앱 화면 이동은 허용 |
| `셸_자기_화면은_허용한다` | `stronghajin://shell/connection-error` → 허용 |
| `주소가_없는_판은_api_를_가로채지_않는다` | 허용 목록·앱 origin 없음 → `/api/` 도 취소(가로채지 않음) |

`lib.rs` 정적 시험 **개정** — `제품_창은_첨부_응답을_셸이_받고_웹에_권한을_주지_않는다`(WORK-012 가 가리킨 `lib.rs:992-998`): 창 빌더가 `guard::navigation_verdict(url, &nav_allow, nav_origin.as_deref(), SHELL_SCHEME)` 를 부르는지 · `guard.rs` 판정이 `crate::download::is_api_request(url, app_origin)`(앱 origin)으로 가로채는지 · `is_api_request(url, &nav_allow)` 가 없는지 · 새 창 갈래(`popup_origin`)는 그대로인지

## 4. 검증 수치

| 명령 | 결과 |
|---|---|
| `cargo test`(기본판 strong-hajin) | **72 passed · 0 failed**(guard 16 — 새 6 포함) |
| `SHELL_FLAVOR=medi-ax cargo test --features kakao-collector` | **91 passed · 0 failed · 6 ignored**(무시 6 은 원래부터 — 실기 카톡 DB·키체인 시험) |
| `make shell-verify-strict SHELL_FLAVOR=strong-hajin` | **통과** — 문제 0 · 구성 미비 0 · 호스트 한계 1(Windows 번들은 이 기기에서 검증 불가 — 정보) |
| `make shell-verify-strict SHELL_FLAVOR=medi-ax` | **통과** — 같음 |
| `make shell-final-preflight SHELL_FLAVOR=medi-ax SHELL_OPERATING_ORIGIN=https://ax.medisolveai.xyz` | **G1~G4 통과**(입력·`shell.config`·capability 가 모두 `https://ax.medisolveai.xyz` 로 일치) · **G5 넷 막힘**(D-4 로그인 수단 · 운영 서버 실재 · M-1 https 신뢰 · M-5 쿠키 유지 — **증거 파일 없이 돌렸다**. 이 관문은 네트워크·실기를 재지 않고 «기록된 주장» 을 요구한다 — 서명 없이 되는 것까지는 G1~G4 다). 증거 파일(`SHELL_FINAL_EVIDENCE`)은 dmg 를 굽는 코디가 RUNBOOK-002 로 넣는다 — 지난 판 기록(`_archive/strong-hajin-deploy/fe-02-final-evidence.json`)을 내가 이 판에 다시 쓰지 않았다 |

- 두 make 관문은 **읽기만** 한다(굽지·설치하지·쓰지 않음 — 출력 끝 줄). `cargo test` 는 `target/` 빌드 산출만 남긴다
- `make shell-release-preflight`(WORK-012 「시험」 줄)는 Release 자산 대조라 dmg 가 있어야 의미가 있다 — 돌리지 않았다(코디의 dmg 뒤)

## 5. 미결

1. **I-1 결정** — 「`about:blank` · `about:srcdoc` 는 프레임 무관 허용」 으로 구현했다(§2 근거). SPEC-006 이동 허용 절 개정은 코디/planner 몫
2. **완료 조건(실물)** — 새 dmg 에서 `about:blank` iframe 이 취소되지 않음(셸 로그 `[shell][nav] allowed url-scheme=about origin=null`) · 내보내기 저장·OAuth 외부 열기·카톡 수집 회귀 없음 — 코디 dmg E2E 몫
3. 셸 로그 문구 하나가 바뀌었다 — 허용 줄이 `allowed origin=…` → `allowed url-scheme=… origin=…`(빈 프레임 허용을 로그에서 가려 보이게). 취소·가로채기 로그 문구는 그대로
