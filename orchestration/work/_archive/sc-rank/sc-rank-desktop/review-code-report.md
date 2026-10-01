# 리뷰 리포트 — sc-rank-desktop / code (2026-10-01)

대상: `reference/2026-09-09-sc-prototype/desktop/` (미추적 새 폴더, WORK-001 P1~P5)
기준: SPEC-001 v0.2.0 · DEC-001 · PoC `server/`·`src/`·`tests/`
방식: read-only. 테스트·앱·네이버 요청은 실행하지 않았다. 수치는 워커 리포트를 인용했다(`cargo test` 38/0, clippy 0, `npm run build` 성공 — report-desktop-p4-p5.md 「검증」).
추가로 본 것: 앱 로그 `~/Library/Logs/com.summerstar.scrank/sc-rank.log` 읽기(따로 볼 것 1의 근거), 의존 크레이트 소스(`~/.cargo/registry`: chromiumoxide 0.9.1 · aws-lc-sys 0.45.0 · reqwest 0.13.5 · tauri-plugin-opener).

## 판정: WARN

FAIL 은 없다. PoC 와 다르게 도는 곳은 하나 찾았다(W-1). 오류 문구가 바뀌는 드문 경우라 FAIL 이 아니라 WARN 으로 둔다.
나머지 WARN 은 Windows 빌드 위험, 그리고 이미 알려진 미결을 어떻게 처분할지다.

### 범위

- `git status --porcelain -uall` 결과 49줄 전부가 `reference/2026-09-09-sc-prototype/desktop/` 아래다. **desktop/ 밖 변경 0.** PASS
- `.gitignore` 가 `node_modules/`·`dist/`·`src-tauri/target/`·`src-tauri/gen/schemas/` 를 뺀다. 디스크에 있는 `dist/`·`gen/schemas/` 는 커밋 대상이 아니다.
- PoC 무변경 파일 대조: `diff -r ../src desktop/src`(`main.jsx`·`bridge.js` 제외) 동일 · `cmp index.html` 동일 · `cmp src-tauri/js/place-dom.js server/place-dom.mjs` 바이트 동일.

## FAIL

없음.

## WARN

### W-1. 플레이스: 수집 중에 프레임이 사라지면 PoC 폴백 대신 한글 도메인 문구가 나온다
- `desktop/src-tauri/src/place.rs:378-382` — 페이지 루프에서 `frame()` 을 부를 때마다(`:391·:394·:453·:460·:471`) 프레임이 없으면 `Domain("플레이스 검색 프레임을 읽지 못했습니다.")` 을 낸다.
- PoC 는 이 문구를 `place.mjs:68` 한 곳(목록 준비 직후 검사)에서만 던진다. 루프 안(`place.mjs:73·74·94·95·101`)에서 `frame()` 이 `undefined` 가 되면 `TypeError: Cannot read properties of undefined` 가 난다. 영어 문구라서 폴백 「플레이스 조회에 실패했습니다…」(`place.mjs:118`)이 된다.
- 결과: 드물게(페이지를 넘기는 도중 iframe 이 교체될 때) 행 안내 문구가 PoC 와 다르다. 판정·순위에는 영향이 없다.
- 어떻게 할지(코디 결정): PoC 에 맞추려면 루프 안 `frame()` 실패를 `ScrapeError::other` 로 바꾼다. 문구가 더 낫다고 보고 남기려면 SPEC §4 에 의도된 변경으로 적는다. 조용히 둘 일은 아니다.

### W-2. rustls 암호 제공자 `aws-lc-rs` 때문에 Windows 빌드에 NASM 조건이 붙는다. 실기 빌드 전에는 성패를 모른다 (따로 볼 것 4)
- 원인: `desktop/src-tauri/Cargo.toml:37` `reqwest` 의 `rustls` 기능 → reqwest 0.13.5 `rustls = ["__rustls-aws-lc-rs", …]` → `aws-lc-sys 0.45.0`. `cargo tree -i aws-lc-rs` 로 확인했다. 들여오는 쪽은 우리 크레이트뿐이다. chromiumoxide 는 `reqwest` 를 `default-features = false` 로 쓰고 fetcher 가 꺼져 있어 TLS 를 켜지 않는다.
- aws-lc-sys 판단 로직(`builder/main.rs:1186-1195` `use_prebuilt_nasm`): Windows x86_64 에서 NASM 이 없으면, `AWS_LC_SYS_PREBUILT_NASM=1` 이 있거나 `prebuilt-nasm` 기능이 켜져 있을 때만 미리 빌드된 객체를 쓴다. 둘 다 없으면 `cmake_builder.rs:693-698` 에서 「Missing dependency: nasm」으로 실패한다. README 의 설명과 절차(`README.md` §2, PowerShell `$env:AWS_LC_SYS_PREBUILT_NASM = "1"`)는 코드와 맞다.
- 위험:
  - 환경변수는 셸 하나에만 걸린다. 새 창에서 `npm run tauri build` 를 치면 빌드가 실패한다.
  - `cargo check --target x86_64-pc-windows-msvc` 가 macOS 에서 aws-lc-sys 단계에서 멈췄다(P4-P5 리포트). 그래서 **우리 Rust 코드는 Windows 타깃으로 한 번도 타입 검사되지 않았다.**
- `ring` 으로 바꿀 여지: 있다. `ring 0.17` 은 x86_64-pc-windows-msvc 용 어셈블리를 미리 생성된 객체로 싣고 있어 NASM 이 필요 없고, MSVC(Build Tools)만 있으면 된다. 바꾸는 방법은 reqwest 기능을 `rustls-no-provider` 로 하고, `rustls`(features `ring`)를 직접 의존에 넣고, 클라이언트를 만들기 전에 ring 제공자를 설치하는 것이다. 코드 변경은 `blog.rs:643` 의 `HTTP` 초기화 근처 한 곳이다.
  - 비용: WORK 「크레이트 방향(워커 재량, 바꾸면 보고)」 범위 안이다. 대신 `rustls-platform-verifier` 가 제공자를 찾도록 설치 순서를 맞춰야 한다. 바꾼 뒤에는 썸네일 HTTPS 다운로드를 한 번 재확인해야 한다(A-5 이미지 모드).
- 권고: A-9 첫 Windows 빌드에서 aws-lc 경로가 한 번에 통과하면 그대로 둔다. 막히면 ring 으로 바꾼다. **어느 쪽이든 A-9 전에 macOS 에서는 확인할 수단이 없다.** 선택은 코디·사용자에게 남긴다.

### W-3. `cfg(windows)` 경로는 읽어서만 확인했다 (체크리스트)
- `desktop/src-tauri/src/browser.rs:22-38`: `ProgramFiles`·`ProgramFiles(x86)`·`LOCALAPPDATA` × (Edge 먼저, 그다음 Chrome)이고 SPEC §3 순서와 같다. 타입도 맞다(`Vec<PathBuf>`, `root.join(r"…")`). 눈으로 봐서는 틀린 곳이 없다.
- `src/main.rs:2` `windows_subsystem = "windows"`(릴리스)는 맞다. `browser.rs:292-298` 은 Windows 파일 잠금을 5초 동안 다시 시도한다.
- chromiumoxide 가 실행 파일 경로를 `dunce::simplified` 로 정규화하므로(`utils.rs:15-18`) `\\?\` 접두 문제는 없다.
- 다만 W-2 때문에 **컴파일로는 한 번도 확인되지 않았다.** A-9 가 첫 확인이다.

### W-4. 기동할 때 남은 프로필을 지우는 범위가 넓다
- `desktop/src-tauri/src/lib.rs:17` → `browser.rs:93-106`: 임시 폴더의 `sc-rank-cdp-*` 를 **pid 와 상관없이 전부** 지운다.
- 앱을 두 개 띄우거나(single-instance 플러그인 없음), 앱을 쓰는 중에 `cargo run --example smoke` 를 돌리면, 나중에 뜬 쪽이 먼저 떠 있는 Edge 의 프로필을 지운다. 그러면 먼저 뜬 쪽의 조회가 폴백 문구로 실패할 수 있다.
- SPEC §3 「비정상 종료로 남은 `sc-rank-cdp-*` 는 다음 기동 때 지운다」를 글자 그대로 구현한 것이라 계약 위반은 아니다. 사용자 한 명이 쓰는 앱이라 위험도 낮다. 이름에 pid 가 들어 있으니(`browser.rs:149`) 「살아 있는 pid 는 건너뛴다」로 좁힐 수 있다.

### W-5. 플레이스 60초 초과가 브라우저 기동 중에 걸리면 프로필이 앱이 다시 뜰 때까지 남는다
- `place.rs:335` 의 `tokio::time::timeout(60s)` 이 `open_context` → `launch`(`browser.rs:166`)를 중간에 버리면, chromiumoxide `kill_on_drop(true)`(`async_process.rs:23`) 때문에 Edge 는 죽는다. 그러나 프로필 디렉터리를 지우는 코드는 `launch` 의 `Err` 분기(`:169`)와 `stop` 에만 있어서 이 경우에는 돌지 않는다.
- 이 상태로 창을 닫으면 A-8 의 「임시 프로필 디렉터리 없음」이 거짓이 된다. 다음 기동 때 W-4 경로로 지워지기는 한다.
- `open_context` 안에서 `create_browser_context` 뒤에 버려지면 브라우저 컨텍스트 하나가 닫히지 않고 남는다. 브라우저가 끝날 때 함께 사라진다.
- PoC 도 60초 경주 뒤 `getBrowser` 가 계속 돈다(`place.mjs:57-58`). 영향은 작다. 기록만 해 둔다.

### W-6. 이미 알려진 미결 — 처분이 아직 기록되지 않았다
- **WebP 목표 이미지의 두 번째 해시**(`blog.rs:278-290`): sharp 는 cover 결과를 WebP q80 으로 다시 인코딩한다. `image` 크레이트에는 손실 WebP 인코더가 없어 픽셀을 바로 해시한다(P1-P2 이슈 2). 사용자가 WebP 를 올리면 PoC 와 거리 값이 조금 다를 수 있다. 판정 기준(≤6, 최솟값)은 같다. 받아들일지 SPEC/log 에 적어야 한다.
- **UA 변경 뒤 플레이스 광고 0건**(P3 이슈 1)은 이 리뷰에서 풀렸다. 앱 로그 09:02 조회 기준 1페이지 `added 88` = 광고 18 + 일반 70 이고, 저장 파일의 강남역성형외과 행도 광고 18 이다(P4-P5 리포트). 헤드리스 Edge + Edge UA 로도 광고가 나온다. P3 smoke 의 광고 0건은 그 시점 편성으로 본다. 닫아도 된다.

## 따로 볼 것 (코디 요청 5)

### 1. 강남성형외과·신논현역성형외과가 둘 다 「228 · 광고 18」 — **우연이다. 버그가 아니라 페이지 구조가 같아서 생긴 결과다** (PASS)
- 코드: `place.rs:387-472` 는 PoC `place.mjs:70-102` 와 한 줄씩 같다.
  - `all` 은 루프 밖에서 한 번만 만들고 페이지마다 누적한다(`:387`·`:418` ↔ `:70`·`:88`).
  - 이름이 없고 `id`·`title` 도 없는 항목은 건너뛴다(`:410-415` ↔ `:86`).
  - `added == 0` 이면 멈추고(`:435-440` ↔ `:91`), 누적 목록 전체에서 타겟이 보이면 멈춘다(`:441-447` ↔ `:92`).
  - 마지막 페이지면 멈추고, 다음 번호가 없으면 조용히 끝낸다(`:448-466` ↔ `:93-100`).
  - 광고 수는 `parse_place_list` 가 누적 행 전체에서 센다(`:205` ↔ `:33`).
- 실측(앱 로그 `sc-rank.log` 09:02:25~38 UTC, 두 키워드 모두):

  | 페이지 | captured | added | 누적 |
  |---|---|---|---|
  | 1 | 91 | 88 | 88 |
  | 2 | 73 | 70 | 158 |
  | 3 | 73 | 70 | 228 → `target-found` |

  `loadedGroups` 가 키워드마다 다르다(30/23/21 과 29/23/20). hydrate 가 각각 따로 돌았다는 뜻이다.
- 해석: 네이버 지도가 페이지마다 **일반 70개**를 주고, 광고 18개는 1페이지에만 붙는다(강남역성형외과도 1페이지 88 = 18 + 70). 두 키워드 모두 타겟이 3페이지에 있어서 3페이지에서 멈췄다. 순위도 이와 맞는다: 광고 제외 145·208 은 둘 다 140(=70×2)보다 크다. 전체 순위는 163 과 226 으로 서로 달라서 목록 자체는 다르다.
- 따라서 「3페이지까지 · 광고는 1페이지만」이면 누구든 228/18 이 나온다. 누적·광고 집계·종료 로직은 PoC 와 같다.

### 2. `--lang=en_US` 와 SPEC §3 `ko-KR` — **컨텍스트 단위 덮어쓰기로 ko-KR 이 된다** (PASS, 한 가지 기록)
- 출처: 우리 코드가 아니라 chromiumoxide 기본 인자다(`chromiumoxide-0.9.1/src/browser/config.rs:487` `ArgConst::values("lang", &["en_US"])`, puppeteer 기본값에서 가져온 것). `browser.rs:150-165` 는 `disable_default_args` 를 쓰지 않는다.
- 덮어쓰기: `browser.rs:245-254` 에서 조회마다 새 페이지에
  - `Emulation.setUserAgentOverride{ userAgent, acceptLanguage: "ko-KR" }` 를 걸어 `navigator.language(s)` 와 요청 헤더 `Accept-Language` 를 바꾸고,
  - `Emulation.setLocaleOverride{ locale: "ko-KR" }` 를 걸어 `Intl`·날짜 서식을 바꾼다.

  둘 다 navigate 전에 건다. Playwright `newContext({ locale: 'ko-KR' })` 도 같은 두 CDP 명령으로 구현한다. 워커 스파이크에서 `navigator.language=ko-KR` 을 확인했다(P3 리포트 §3).
- 지도 목록 iframe(`pcmap.place.naver.com`)은 `map.naver.com` 과 같은 사이트(naver.com)라 같은 프로세스에 있다. 그래서 페이지 대상에 건 덮어쓰기가 iframe 에도 적용된다. 실제로 목록을 읽었으니 이 경로가 동작한 것도 맞다.
- 남는 것: `--lang` 은 브라우저 UI 언어와, 덮어쓰기가 닿지 않는 서비스 워커·공유 워커의 `navigator.language` 에만 남는다. 조회 경로와는 관계가 없다. 인자 자체를 없애려면 `.arg("--lang=ko-KR")` 을 추가해야 한다(ArgsBuilder 가 같은 키를 덮어쓰는지는 확인하지 않았다). 그럴 필요는 없다고 본다.

### 3. `main.jsx` 의 `import` 1줄 — **SPEC §5 범위 안이다** (PASS)
- diff(`src/main.jsx` ↔ PoC) 결과 바뀐 곳은 셋이다:
  - `+4` `import { checkRank, saveWorkbook } from './bridge';`
  - `63` 조회 호출(PoC 62-65 의 4줄 → 1줄)
  - `74` 저장(PoC 76-79 의 4줄 → 1줄)

  catch 줄(`64`, 「조회 시간이 초과되었습니다.」 분기)·문구·`<a>` 는 PoC 와 같다.
- 근거:
  - SPEC §5 가 「이 셋뿐」이라고 한 것은 **바뀌는 기능 셋(호출·저장·링크)** 이다.
  - §5.1 은 「연결 모듈 `desktop/src/bridge.js` 의 함수 호출」을 요구한다. 부르려면 import 가 있어야 한다.
  - §5.3 은 「**진입부에서** `a[target=_blank]` 클릭을 가로채」라고 적었다. §1 이 `index.html` 무변경을 요구하므로 진입 모듈은 `main.jsx` 하나다. 가로채기는 `bridge.js:26-31` 이 모듈을 불러올 때 등록된다.
- 이 줄은 §5 의 세 변경을 구현하려면 반드시 필요하다. 새로 생긴 변경이 아니다. SPEC 을 다음에 고칠 때 「import 1줄 포함」을 명시해 두면 논란이 없다.

### 4. `aws-lc-rs` → `ring` — W-2 참고 (WARN)

### 5. 화면 180초 상한과 Rust 잠금·브라우저 기동 180초가 겹칠 때 — **PoC 와 같은 동작이다. 사용자가 만날 모습은 아래와 같다** (PASS, 사용자 안내 권고)
- 구조:
  - 화면 `bridge.js:11-16` 은 `invoke` 를 기다리는 것만 180초에 끊는다. Rust 명령을 취소하지 않는다.
  - 잠금(`commands.rs:40·54`의 `_pass`)은 명령 future 가 끝날 때 풀린다(`gate.rs:54-60`).
  - PoC 도 `AbortSignal.timeout(180000)`(PoC `main.jsx:62`)이 서버 작업을 멈추지 않고, `busy` 는 서버 쪽 `finally` 에서 풀린다(`index.mjs:31·39`). 구조가 같다.
- 경우별로 보면:

  | 상황 | Rust 쪽 | 화면 |
  |---|---|---|
  | **플레이스**, 브라우저 기동이 멈춤 | `open_context` 가 `collect_place_list` 의 60초 안에 있다(`place.rs:335`·`:363`). 60초에 「조회 제한 시간 60초를 초과했습니다.」 | 180초에 닿지 않는다. 한글 문구 행 |
  | **블로그**, 브라우저 기동이 멈춤 | `open_context` 는 150초 상한 **밖**이다(`blog_browser.rs:74-75`, PoC `blog-browser.mjs:7-9` 와 같음). `LAUNCH_TIMEOUT` 180초(`browser.rs:86·163`, Playwright launch 기본값)에 기동 실패 → 폴백 문구 | 화면 타이머가 몇 ms 먼저 시작하므로 거의 항상 화면이 먼저 끊긴다 → 「조회 시간이 초과되었습니다.」 |
  | 블로그, 이미지 모드에서 썸네일이 느림 | 150초 상한은 컨텍스트 조작에만 걸린다. 썸네일 비교(`blog.rs:762-775`, 8초 × 대략 n/8)는 상한 밖이다(PoC 도 같음). 180초를 넘을 수 있다 | 「조회 시간이 초과되었습니다.」 이후 아래 연쇄 |

- 연쇄: 화면이 180초에 끊어도 Rust 는 계속 돌면서 잠금을 쥐고 있다. 화면은 1초(블로그) 또는 2.2초(플레이스) 뒤 다음 키워드를 보내고(`main.jsx:66`), 이 요청은 `Err(BUSY_MESSAGE)` 를 받는다. 그래서 **다음 행들이 「다른 조회가 진행 중입니다. 잠시 후 다시 조회해 주세요.」로 차례로 실패하다가**, Rust 가 끝나고 간격(0.7초/2초)이 지나면 다시 정상으로 돈다.
- 블로그 기동이 계속 멈추는 경우(예: Edge 가 뜨지 않는 PC): 키워드마다 180초가 걸린다. 19개면 약 57분 동안 행이 하나씩 「조회 시간이 초과되었습니다.」로 채워진다. 「중단」은 키워드 사이에서만 먹는다(`main.jsx:59`). PoC 에서는 `browserPromise` 를 여러 요청이 함께 기다린다. 여기서는 mutex 로 줄을 선다. 기다리는 총 시간은 같다.
- 끼어드는 경우(W-5 와 같은 자리): 브라우저 기동 중에 창을 닫으면, `RunEvent::Exit` 의 `block_on(shutdown)`(`lib.rs:40-43`)이 `running` mutex 를 기다린다. 그래서 **창 닫기가 기동이 끝날 때까지 최대 180초 멈춘 것처럼 보일 수 있다.** 평소 기동은 1.4초(P3 smoke `browser-ready 1397ms`)라 실제로 만날 일은 드물다.

## 체크리스트 (rules.md 「코드 검수」)

| 항목 | 판정 | 근거 |
|---|---|---|
| §4 플레이스 수집: goto 30초·첫 항목 20초·전체 60초·프레임 판정·셀렉터·정규식 4종·`:86`·`:91`·마지막 요소 클릭 | PASS (W-1 제외) | `place.rs:335·365·370·379·290-291·408-440` · `js/place-items.js`·`place-next.js` 는 `place.mjs:74-80·95-99` 원문. 기본 8초는 PoC 에서 걸리는 호출이 없다(evaluate·evaluateAll 은 타임아웃 없음). 워커 판정에 동의 |
| §4 플레이스 판정: `extractPlaceName`·`parsePlaceList`·`PLACE_SCOPE`·문구 | PASS | `place.rs:13-32·122-209·227-271` ↔ `place.mjs:4-34·111-119`. `\d` 는 ASCII, `\s` 는 JS 집합(`:20`) |
| §4 블로그 수집: goto 25초·첫 카드 12초·응답 대기를 스크롤 전에 등록·4갈래·렌더 조건·150초 | PASS | `blog_browser.rs:26-29·137-152·170-222·224-231` ↔ `blog-browser.mjs:9-44`. CDP 사전 요청(Preflight) 제외(`:156`)는 Playwright 의미를 옮긴 것이다 |
| §4 블로그 판정: 썸네일 8초·6MB·비 2xx·전처리·최솟값·캐시·0건 문구·found 면 중단·검증 3종·scope·target | PASS (WebP 는 W-6) | `blog.rs:21-33·210-312·414-490·548-575·643-678·733-786`. `min_by_key` 가 동률일 때 첫 값을 주므로 PoC 안정 정렬 `[0]` 과 같다. curl `--fail` 아래의 3xx 는 PoC 에서 sharp 디코드 실패가 되고 여기서는 비 2xx 가 된다. 둘 다 `error:true` 로 같다 |
| §4 엑셀 | PASS | `workbook.rs` ↔ `workbook.mjs:2-23`: 열 세 벌·너비·파생 열·빈 메시지 폴백·머리행/본문 서식·필터·creator. 빈 문자열 셀과 객체 값 차이는 P1-P2 이슈 4(읽으면 같음) |
| §4 페이지 안 JS 는 문자열 그대로 주입 | PASS | `js/*.js` 6개가 PoC 원문과 같다(`place-dom.js` 는 `cmp` 동일). `collect_offline.rs` 가 원문과 같은지 단언한다 |
| §2 명령 모양·Err 자리·잠금 순서 | PASS | `commands.rs:31-56`: `check_place` 는 검증이 잠금보다 앞, `check_blog` 는 잠금만 Err. `gate.rs` 는 끝난 시점부터 0.7초/2초이고 오류여도 갱신한다 |
| PoC 테스트 단언이 약해지지 않았나 | PASS | `tests/place.rs` 9 · `tests/blog.rs` 3 이 `place.test.mjs`·`blog.test.mjs` 와 테스트 이름·단언 값이 같다(≤6 / >6, 180px JPEG q60, flop). 수치는 워커 리포트 38/0 인용 |
| error 를 not_found 로 떨어뜨리는 폴백 | 없음 (PASS) | 썸네일 오류는 `ThumbnailCheck::Error` 로 남아 `failed_before` 에서 오류가 된다(`blog.rs:470-481`). 블로그 `added==0 && !url` 은 앞 배치 결과로 끝난다(PoC `:32` `return` 과 같음) |
| 브라우저: 전용 임시 프로필·종료 정리·UA 에서 헤드리스 표식 제거·Edge→Chrome→안내 | PASS (W-4·W-5) | `browser.rs:148-149·193·280-303` · `lib.rs:40-43` · `find_browser` + §3 문구. A-8 은 워커·사용자가 실측(P4-P5) |
| 서버·포트 없음 · 화면에 `fetch` 없음 | PASS | 앱이 여는 리스너 없음. CDP 는 chromiumoxide 기본 `--remote-debugging-port=0`(127.0.0.1). `grep fetch desktop/src` 결과는 `main.jsx` 에서 0(bridge 로 대체) |
| `cfg(windows)` | WARN (W-3) | 읽어서는 맞다. 컴파일로는 확인되지 않았다 |

## 조용히 통과하는 자리

| 자리 | 무엇 | 평가 |
|---|---|---|
| `place.rs:378-382` | 루프 안에서 프레임을 못 찾으면 한글 도메인 문구가 된다(PoC 는 폴백) | **W-1** |
| `bridge.js:30` `openUrl(...).catch(() => {})` | 링크 열기가 실패하면 아무 표시도 없다 | 권한은 `opener:default` = http/https/mailto/tel 허용(plugin-opener `permissions/default.toml`)이라 네이버 https 링크는 통과한다. 실패할 경로가 거의 없어 수용. 로그 한 줄은 권고 |
| `blog_browser.rs:135` `before … .as_u64().unwrap_or(0)` | 카드 수를 못 읽으면 0 으로 보고 렌더 대기 기준이 낮아진다 | DOM 식이라 숫자가 아닐 경로가 사실상 없다. 참고 |
| `browser.rs:405-408` `wait_for` 가 평가 오류를 삼키고 다시 본다 | 20초/12초 뒤에는 폴백 문구로 끝난다 | Playwright `waitFor` 도 다시 시도한다. 같음 |
| `bridge.js:6` 빈 reject → 「조회에 실패했습니다.」 | PoC `data.message \|\| '조회에 실패했습니다.'`(PoC `main.jsx:65`)와 같은 문구 | PASS |
| `bridge.js:22` 모든 저장 실패 → 「엑셀을 저장하지 못했습니다…」 | 검증 실패 Err(`저장할 결과는 1~50개…`)도 이 문구로 덮인다 | SPEC §5.2 그대로다. PASS |
| 제한값 | 60·30·20·8·25·12·150·180초, 6,291,456B·4MB·25,000,000px·동시 8·거리 6·간격 0.7/2초 | 전부 PoC 값과 같다 |

## 사용자가 실물에서 만날 자리

1. **Windows 첫 빌드(A-9)**: PowerShell **같은 창**에서 `$env:AWS_LC_SYS_PREBUILT_NASM = "1"` 을 먼저 쳐야 한다. 빠뜨리면 `Missing dependency: nasm` 으로 빌드가 멈춘다. `cfg(windows)` 코드도 이때 처음 컴파일된다(W-2·W-3).
2. **회사 PC 정책**: Edge 에 `RemoteDebuggingAllowed = 0` 이 걸려 있으면 모든 조회가 폴백 문구로 끝난다. Edge 가 설치돼 있으면 Chrome 으로 넘어가지 않는다(README §2 에 적혀 있음).
3. **「조회 시간이 초과되었습니다.」 다음에 「다른 조회가 진행 중입니다…」가 몇 줄 이어지는 모습**: 화면은 180초에 포기하지만 앱은 그 조회를 끝까지 한다. 잠시 뒤 다시 정상으로 돈다. PoC 와 같다(따로 볼 것 5).
4. **Edge 가 아예 뜨지 않는 PC 에서 블로그 조회**: 키워드마다 3분씩 걸리고 모두 시간 초과가 된다. 「중단」은 지금 키워드가 끝난 뒤에 먹는다.
5. **덮개를 닫았다 연 뒤 첫 조회**: CDP 연결이 끊겨 있으므로 브라우저를 새로 띄운다(로그 `launched` 한 줄 더). 그 조회만 1~2초 더 걸린다. 이 재기동 경로는 아직 실측하지 않았다(P4-P5 이슈 3).
6. **창 닫기가 잠깐 멈춤**: 브라우저를 띄우는 도중에 창을 닫으면 기동이 끝날 때까지 기다린다. 평소 1.4초라 드물다.
7. **플레이스 순위 해석**: 한 페이지는 일반 70 + (1페이지만) 광고 약 18 이다. 그래서 같은 페이지에서 멈춘 키워드들은 「확인 업체 수·광고 수」가 똑같이 나온다(따로 볼 것 1). 버그가 아니다.
8. **WebP 로 목표 이미지를 올릴 때**: 두 번째 해시가 PoC 와 조금 다를 수 있다(W-6). PNG·JPG 는 같다.
9. **저장 대화상자·취소·링크 열기**: 눈 확인 pending(A-6 나머지)이다. 코드로는 `.xlsx` 필터·한국 날짜 기본 파일명·취소 시 무메시지·OS 브라우저로 여는 것을 확인했다(`commands.rs:71-89`·`bridge.js:20-31`).

## 참고(기존 부채)

- `check_blog` 인자가 `null` 일 때 Tauri `Option` 이 「키 없음」과 구분하지 못한다(P1-P2 이슈 3). 화면은 늘 문자열을 보내므로 실사용 영향이 없다.
- 플레이스 `rows[]` 키 순서(`rank`·`organicRank` 가 `page` 보다 앞)는 PoC 객체 전개 순서와 다르다. JS 쪽에서 읽을 때는 차이가 없다.
- `map_concurrent` 의 `limit ≥ 1` assert(P1-P2 이슈 5). 호출부는 늘 8 이라 무관하다.
- 페이지 JS 오류 문구에서 Playwright 접두(`frame.evaluate: Error: `)가 빠졌다(P3 §4 「다름(작음)」). SPEC §4 「문구 그대로」에 맞춘 것이라 수용한다.
- 해시 전처리(회색조 계수·Lanczos 구현)는 `1.png` 한 장으로만 sharp 와 비트까지 같다고 확인했다(P1-P2). 다른 이미지에서 ±1비트 차이가 날 가능성은 남는다. 임계값 6 의 여유 안이다.
