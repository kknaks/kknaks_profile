# 리뷰 리포트 — sc-rank-desktop / doc (2026-09-30)

대상: `para/projects/summer-star/sc-rank/20-spec/spec-001-desktop-app.md`(이하 SPEC) ·
`para/projects/summer-star/sc-rank/30-work/work-001-desktop-port.md`(이하 WORK).
기준: DEC-001 D-01~D-14 · PoC `reference/2026-09-09-sc-prototype/`(이하 PoC, 경로는 이 폴더 기준).
방법: PoC `server/*.mjs`(search.mjs 제외 — D-06 범위 밖)·`src/main.jsx`·`tests/*.mjs`·`index.html`·`scripts/smoke.mjs` 를 줄 단위로 읽고 SPEC §2·§4·§5·§6, WORK Phase 에 대조했다. 네이버 요청 없음.

## 판정: FAIL

FAIL 6 · WARN 11. FAIL 은 전부 **「워커가 추측으로 메워야 하는 빈칸」 또는 「SPEC 안의 자기모순」**이다. 결정(DEC) 자체를 뒤집어야 하는 것은 없다 — 전부 SPEC·WORK 문장 보강으로 닫힌다.

---

## FAIL

### F-1. §4 가 「전수」라고 선언하는데 PoC 의 제한값·문구가 빠져 있다
- 위치: SPEC:72 「여기 목록은 옮길 대상의 전수다」, SPEC:76·79·80
- 근거: 표가 가리키지 않는 PoC 값들 —
  - 플레이스 (`server/place.mjs`)
    - `page.goto` 30초(`:65`) · 목록 첫 항목 대기 20초(`:67`) — 표에는 「60초 제한 · 개별 대기 8초」뿐
    - 목록 셀렉터 `#_pcmap_list_scroll_container a.uD1F4 > span:first-child`(`:67`·`:94`), 항목 셀렉터 `> ul > li`(`:74`), 프레임 판정 `name()==='searchIframe' && url.includes('pcmap')`(`:64`)
    - 항목 추출 정규식: `id` = `/\/(\d{6,})(?:[/?#]|$)/`, `ad` = `/광고/`, `reviews` = `/리뷰\s*([\d,]+)/`, `addr` = `/(서울 [가-힣]+구 [가-힣\d]+동)/`, `title` 셀렉터 `a.uD1F4 > span:first-child, .place_bluelink`(`:75-79`) — 표는 필드 **이름**만 적었다
    - 수집 중 상호 판정: 상호 없음 + (`id`||`title`) → 「일부 업체의 상호를 읽지 못했습니다.」, 둘 다 없으면 건너뜀(`:86`) · 한 페이지 `added==0` → 첫 페이지면 「플레이스 목록을 읽지 못했습니다.」 아니면 종료(`:91`)
    - 페이지 이동: `a, button` 중 텍스트가 정확히 다음 번호인 **마지막** 요소 클릭, 못 찾으면 조용히 종료(`:95-100`)
    - 오류 문구 `「플레이스 검색 프레임을 읽지 못했습니다.」`(`:68`), `「조회 페이지는 1~5 사이여야 합니다.」`(`:51`), not_found 안내 `「수집한 최대 5페이지 목록에서 찾지 못했습니다.」`(`:116`)
  - 블로그 (`server/blog-browser.mjs` · `server/blog.mjs`)
    - `page.goto` 25초(`blog-browser:13`) · 첫 카드 대기 12초(기본 타임아웃, `:12`·`:14`)
    - 추가 응답 판정: `!response.ok()` → 「블로그 추가 결과 요청에 실패했습니다(HTTP n).」, `payload.collection` 배열 아님 → 오류, 추가 카드 0 + `payload.url` 없음 → 정상 종료 / 있음 → 「추가 결과를 읽지 못해 순위를 확정할 수 없습니다.」, 배치 뒤 `payload.url` 없으면 종료(`:27-33`·`:44`)
    - 렌더 완료 조건: headline 을 가진 카드 수 ≥ `before + added`(`:36`·`:42`)
    - 썸네일 다운로드: 8초 · 최대 6MB(`--max-filesize 6291456`) · UA `Chrome/140` Mac 문자열 · 비 2xx 는 실패(`--fail`)(`blog.mjs:7`·`:55`·`:92`)
    - 이미지 전처리: EXIF 회전(`rotate()`) · 흰 배경 합성(`flatten #fff`) · `fit: fill` 32×32 · 입력 픽셀 상한 25,000,000(`blog.mjs:35`) — 표는 「32×32 회색조 DCT」만. 알파·EXIF 처리가 빠지면 해시가 달라진다
    - 목표 해시와의 거리 = 두 목표 해시 중 **최솟값**(`:92`) · 배치 간 썸네일 결과 캐시(새 URL만 비교, `:87-88`·`:95`) · 썸네일 0건 → 「비교할 검색 썸네일을 읽지 못했습니다.」(`:89`) · found 면 다음 배치 중단(`:105`)
    - 입력 검증 문구 3종(`:74-76`) · `scope` 문자열(타겟 종류별 두 가지, `:72`) · 이미지 모드 `target` = `imageName || '업로드 이미지'`(`:72`) · not_found 안내 `「이번 블로그 탭 초기 목록 + 최대 3회 스크롤에서 찾지 못했습니다.」`(`:109`)
- 왜 FAIL: 「전수」라고 적힌 표는 워커가 **목록 밖을 안 옮겨도 되는 근거**가 된다(발주서 전수조사 원칙). 리뷰어도 표를 기준으로 코드 검수를 한다(`roles/.../rules.md` 코드 검수 1번).
- 제안: 둘 중 하나. (a) 72행을 「**정본 함수 본문 전체**를 옮긴다. 아래는 특히 틀리기 쉬운 것」으로 바꾸고 표를 예시로 격하, 또는 (b) 위 값을 표에 추가. (a) 가 PoC 와 어긋날 여지가 적다.

### F-2. 오류 메시지 폴백 규칙(한글 판정)이 블로그 쪽에 없고, Rust 에서의 대응이 정의되지 않았다
- 위치: SPEC:78(플레이스 「오류 문구」), SPEC:80(블로그 행에 오류 문구 없음)
- 근거: PoC 는 예외 메시지에 한글이 있으면 그대로, 없으면 고정 문구로 바꾼다.
  - 플레이스 `place.mjs:118` — 폴백 「플레이스 조회에 실패했습니다. 브라우저 설치 또는 네이버 접근 제한을 확인해 주세요.」
  - 블로그 `blog.mjs:112` — `한글 && !error.code` 일 때만 그대로, 아니면 「블로그 조회 또는 이미지 처리가 실패했습니다. 잠시 후 다시 확인해 주세요.」
- 왜 FAIL: Rust 에서는 CDP·reqwest·image 오류가 영어로 올라온다. 규칙이 없으면 워커가 `format!("{e}")` 를 그대로 화면에 내거나(영어 메시지 노출) 전부 폴백으로 덮는다(한글 도메인 문구 소실). `!error.code`(Node 시스템 오류 제외)에 대응하는 Rust 규칙도 정해야 한다.
- 제안: §4 에 한 줄 — 「도메인 오류(PoC 가 한글 문구로 던지는 것)는 문구 그대로, 그 밖의 모든 오류(CDP·HTTP·IO·디코드)는 영역별 폴백 문구」. 블로그 행에 오류 문구·폴백 추가.

### F-3. 명령 실패(`Err(String)`)를 화면이 어떻게 받는지 — PoC 코드 그대로면 메시지가 비고, 180초 타임아웃이 사라진다
- 위치: SPEC:52-53, SPEC:86, SPEC:82(「화면 전부 그대로」)
- 근거: PoC `src/main.jsx:62-66`
  - `fetch(..., { signal: AbortSignal.timeout(180000) })` → `TimeoutError` 면 「조회 시간이 초과되었습니다.」(`:66`)
  - `!res.ok` → `throw Error(data.message || '조회에 실패했습니다.')`(`:64`), catch 에서 `error.message` 를 행 메시지로 쓴다(`:66`)
- 문제:
  1. Tauri `invoke` 는 `Err(String)` 을 **문자열 그대로 reject** 한다. PoC catch 의 `error.message` 는 `undefined` → 「다른 조회가 진행 중입니다…」 가 화면에 안 나온다. SPEC:53 「`!res.ok` 분기처럼 바꾼다」는 이 변환을 누가·어떻게 하는지 말하지 않는다.
  2. `invoke` 에는 abort 신호가 없다. 180초 상한과 「조회 시간이 초과되었습니다.」 문구를 버리는지, 화면에서 `Promise.race` 로 유지하는지 SPEC 에 없다. PoC 블로그는 브라우저 기동(`blog-browser.mjs:7`)이 150초 데드라인 **밖**이라, 180초 화면 상한이 유일한 바깥 경계였다 — 버리면 기동이 멈출 때 화면이 영원히 「조회 중」.
- 제안: §5-1 에 「reject 값(문자열)을 `Error` 로 감싸 기존 catch 로 넘긴다 · 180초 상한은 화면에서 `Promise.race` 로 유지(문구 동일)」 또는 「Rust 쪽 전체 상한 N초 + 문구」 중 하나를 못 박는다.

### F-4. User-Agent 계약이 PoC 와 다르고, 어떤 문자열인지 비어 있다
- 위치: SPEC:67 「헤드리스 표식(`HeadlessChrome`)을 뺀 데스크톱 UA 로 덮는다」
- 근거:
  - 플레이스 컨텍스트: **고정** Mac UA `…Mac OS X 10_15_7…Chrome/128.0.0.0…`(`place.mjs:59`)
  - 블로그 컨텍스트: UA 덮어쓰기 **없음**(`blog-browser.mjs:8`) — PoC 블로그는 헤드리스 UA 그대로 네이버에 갔다
  - 썸네일 다운로드: Mac UA `Chrome/140`(`blog.mjs:7`)
- 문제: SPEC 머리말(SPEC:24)은 「동작의 정본은 PoC」인데 §3 은 블로그에도 UA 를 덮게 한다(PoC 와 다름을 명시하지 않음). 그리고 「데스크톱 UA」가 PoC 고정 문자열(Mac·Chrome/128)인지, 실행 브라우저의 실제 UA 에서 `Headless` 만 뺀 것(Windows·Edge 면 `Edg/…` 포함)인지 정해지지 않았다. 네이버 응답이 UA 에 따라 달라질 수 있어 A-4·A-5 결과에 직결된다.
- 제안: 「플레이스·블로그 모두 `<정확한 문자열 또는 규칙>` · PoC 블로그와 다른 점은 의도된 변경」을 §3 에 적는다. 썸네일 HTTP UA 도 같은 줄에.

### F-5. 결과 링크를 OS 브라우저로 여는 것은 세 번째 화면 변경인데 §5 는 「이 둘뿐」이라 한다
- 위치: SPEC:84 「이 둘뿐」 vs SPEC:90-91 「링크는 OS 기본 브라우저로 연다」 · WORK:31 P4 「§5 두 곳만 바꾼다. 링크는 OS 브라우저로」 · DEC D-14(DEC:75) 「바뀌는 곳은 호출부와 저장뿐」
- 근거: PoC 링크는 `<a href target="_blank">` 두 개(`src/main.jsx:115` — 「매칭 글」, 「네이버」). Tauri 웹뷰에서 `target="_blank"` 는 OS 브라우저로 나가지 않는다 — `tauri-plugin-opener`(WORK:40) 호출을 화면 코드에 넣어야 한다. 즉 화면 변경이 셋이다.
- 왜 FAIL: 체크리스트 「화면 변경이 §5 두 곳으로 닫혀 있나」 불충족. 워커는 (a) `main.jsx` 의 `<a>` 를 고친다, (b) 전역 클릭 가로채기 스크립트를 따로 둔다, (c) Rust 쪽 new-window 핸들러 중 추측해야 한다. D-14 문구와도 충돌.
- 제안: §5 를 세 항목으로 늘리고 방식(권장: `main.jsx` 는 그대로 두고 `desktop/src/` 진입부에서 `a[target=_blank]` 클릭을 가로채 opener 로 여는 것 — 화면 코드 무변경 유지)을 적는다. DEC D-14 에 링크 한 줄 보강 여부는 코디 판단.

### F-6. 실수집 인수조건 A-4·A-5·A-7·A-8 에 「무엇으로」가 없다
- 위치: SPEC:100-104, WORK:30
- 근거: PoC 는 실수집을 `npm run smoke`(`scripts/smoke.mjs:1-7` — `checkPlace('강남역성형외과','무이성형외과')`, found 아니면 exit 1, 끝나면 브라우저 닫음)로 확인했다. SPEC 에는 대응 수단이 없다.
  - A-4·A-5 「코디 실행」 — GUI 로 누르나, `cargo test -- --ignored` 인가, 예제 바이너리인가 불명. 코디가 관문 명령을 직접 1회 돌리는 규칙(WORK:49)과 맞물리려면 **명령**이 있어야 한다
  - A-5 키워드·타겟 미지정 — 「1건」이 무엇인지 워커가 고른다
  - A-7 「브라우저 경로를 못 찾게 한 상태」 — 개발 macOS 에는 Chrome/Edge 가 있다. 경로 후보를 주입하는 테스트 이음새인지, 환경변수인지, 앱 번들 이름 변경인지 없음. 환경변수를 만들면 SPEC 에 없는 설정 표면이 생긴다
  - A-8 「앱 종료」 — 창 닫기인지 Cmd+Q 인지, 확인 명령(예: 임시 프로필 경로로 `pgrep -f`)이 없음
- 제안: A-4·A-5 는 `cargo test --ignored <이름>` 또는 `cargo run --example smoke` 처럼 명령을 박는다(smoke.mjs 대응, 키워드·타겟 고정). A-7 은 「브라우저 후보 목록을 인자로 받는 탐색 함수 + 빈 목록 단위 테스트」로 확인 수단을 정한다. A-8 은 종료 동작과 확인 명령을 적는다.

---

## WARN

### W-1. `check_blog` 입력 검증은 `Err` 가 아니라 정상 반환이다 — SPEC:52 가 일반화했다
- 위치: SPEC:52 「명령 실패는 … 입력 검증 실패, 다른 조회 진행 중」
- 근거: PoC `/api/blog/check` 에는 400 이 **없다**(`index.mjs:27-32`). 검증은 `checkBlog` 안에서 `status:"error"` 행으로 돌아온다(`blog.mjs:74-77`·`:112`). 400 은 플레이스(`index.mjs:35`)와 export(`:45`)뿐. 또 플레이스 400 은 busy 검사 **앞**(`:35`→`:36`), 간격 갱신 없음.
- 제안: 표로 명확히 — `check_place`: 입력 검증 Err(문구 index.mjs:35, busy 앞) / `check_blog`: Err 는 busy 뿐 / `export_xlsx`: 검증 Err.

### W-2. 출력 키가 PoC 와 같다는 근거가 함수 이름뿐이다
- 위치: SPEC:43·47-48
- 근거: 화면이 읽는 키(`status·rank·organicRank·page·checkedAt·message·matches[0].url·searchUrl·target·keyword`, `main.jsx:115` 등)와 엑셀이 읽는 키(`total·totalAds·scope·matches[].name/title/url`, `workbook.mjs:8-17`)가 camelCase 이고, **없음은 `null`**(키 생략 아님)이다. 오류 반환 모양도 두 함수가 다르다(플레이스 `total/totalAds:null, matches:[], rows:[]` `place.mjs:118` / 블로그 `total:null, matches:[]`, `scrolls` 없음 `blog.mjs:112`). 성공 시 블로그는 `scrolls`, 이미지 모드는 `comparedImages`·`matches[].imageUrl/hashDistance` 가 붙는다.
- 제안: §2 에 명령별 출력 키 표(키·타입·null 여부) 또는 최소 「serde `rename_all = camelCase`, `Option` 은 `null` 로 직렬화(skip 금지)」 한 줄.

### W-3. `invoke` 인자 모양이 정해지지 않았다
- 위치: SPEC:47-49, SPEC:86
- 근거: Tauri 2 는 명령 인자를 **최상위 키 = Rust 파라미터 이름**(camelCase↔snake_case 자동 변환)으로 받는다. 구조체 하나로 받으면 화면은 `invoke('check_blog', { req: {...} })` 처럼 감싸야 한다. SPEC 의 「입력 `{ keyword, targetType, … }`」는 둘 다로 읽힌다.
- 제안: 「평평한 인자(`invoke('check_blog', { keyword, targetType, target, imageData, imageName })`)」처럼 한 가지로 고정.

### W-4. `export_xlsx` 행 역직렬화가 엄격하면 화면이 만든 행에서 깨진다
- 위치: SPEC:56 「각 행 `keyword` 문자열」
- 근거: 저장하는 `rows` 에는 명령 결과뿐 아니라 화면이 만든 행이 섞인다 — 대기→중단 행(`status:'cancelled'`, `matches` 없음, `main.jsx:70`), 화면 catch 가 만든 오류 행(`main.jsx:66`, `snapshot` 키 + `domain`), 플레이스 결과의 `rows` 전체 목록(수백 개). PoC 는 `keyword` 만 검사하고 나머지는 느슨하게 읽는다(`index.mjs:45`, `workbook.mjs:17` 의 `?.`).
- 제안: 「행은 `serde_json::Value`(또는 전 필드 `Option`)로 받고, 검증은 PoC 와 같은 `keyword` 문자열 · 1~50행만」.

### W-5. 엑셀 파생 열 값이 §4 에 없다
- 위치: SPEC:81
- 근거: `workbook.mjs:17` — `매칭 글 URL`=`matches[0].url`, 플레이스 `매칭 상호`=`matches[].name` 을 `' / '` 로 이음, 블로그 `매칭 글 제목`=`matches[0].title`, 모르는 상태는 원문 그대로, `message` 가 비고 `not_found` 면 **파워링크 문구** 「이번 응답의 첫 파워링크 광고 목록에 없음」. 머리행 스타일 세부(높이 28, 굵은 흰 글씨, 배경 `FF5467F7`), 본문 행 높이 25·글꼴 11·세로 가운데(`:19-22`), 열 너비(`:8-10`), `creator='SCAX'`(`:5`), 필터 범위 `A1:K{n}`/`A1:M{n}`(`:21`).
- 제안: F-1 (a) 로 가면 자동 해소. 파워링크 폴백 문구는 블로그·플레이스 결과에 항상 `message` 가 있어 실제로는 안 나오지만, 옮길지 뺄지 한 줄 정해 둔다.

### W-6. 저장 실패 문구가 둘 중 어느 것인지 모호
- 위치: SPEC:88 「쓰기 실패는 PoC 저장 실패 문구」
- 근거: PoC 에 두 문구 — 서버 「엑셀을 만들지 못했습니다. 결과를 다시 조회해 주세요.」(`index.mjs:51`), 화면 「엑셀을 저장하지 못했습니다. 다시 시도해 주세요.」(`main.jsx:77`, 서버 메시지 무시하고 항상 이것). 검증 실패 Err(`index.mjs:45` 문구)가 화면에 어떻게 보이는지도 없음.
- 제안: 「화면은 모든 `export_xlsx` 실패에 `main.jsx:77` 문구」로 고정.

### W-7. 페이지 안 JS 재사용 범위가 `place-dom.mjs` 에만 걸려 있다
- 위치: SPEC:77, DEC D-05(DEC:54)
- 근거: 페이지 안에서 도는 JS 는 `place-dom.mjs` 말고도 있다 — 플레이스 항목 추출 `evaluateAll`(`place.mjs:74-80`), 페이지 서명·번호 클릭(`:94-99`), 블로그 스크롤·렌더 대기(`blog-browser.mjs:25`·`:35-42`). Rust 에서 DOM 을 CDP 로 따로 질의해 다시 짜면 F-1 의 정규식·셀렉터가 어긋날 여지가 크다.
- 제안: 「PoC 가 `evaluate` 로 넘기는 함수 본문은 전부 문자열 그대로 주입」으로 넓힌다.

### W-8. CDP 디버깅 포트와 D-02 「HTTP 포트 없음」의 해석
- 위치: SPEC:34, DEC D-02(DEC:51)
- 근거: `chromiumoxide` 는 브라우저를 `--remote-debugging-port`(로컬 WebSocket)로 띄운다. 앱이 여는 서버는 아니지만 **포트는 생긴다**. 코드 검수 체크리스트 「서버·포트가 생기지 않았나」(rules.md)에 걸릴 수 있다.
- 제안: §1 에 「D-02 의 포트는 앱이 여는 서버를 뜻한다. 브라우저 CDP 는 `127.0.0.1` 임의 포트(0)로 허용」 또는 파이프(`--remote-debugging-pipe`) 강제 중 하나를 적는다. 결정 변경이 아니라 해석 고정.

### W-9. A-3 이 어느 Phase 끝 조건에도 없다 / P1·P4 끝 조건이 눈 확인뿐
- 위치: WORK:28-32, SPEC:99
- 근거: Phase 표 끝 조건에 `cargo clippy -- -D warnings`·`npm run build` 가 없다(검증 분담 WORK:47 에만). A-1·A-2→P2, A-4·5·7·8→P3, A-6·A-9→사용자로 배정됐고 **A-3 만 빈다**. P1 「화면이 뜬다」, P4 「조회→저장이 돈다(워커 확인 1회)」는 네이티브 저장 대화상자를 워커가 어떻게 확인·보고하는지(스크린샷? 로그?) 없음.
- 제안: A-3 을 P2~P4 공통 끝 조건으로. P4 확인 산출물(예: 저장된 xlsx 경로 + 앱 로그)을 지정.

### W-10. 실수집 단언과 이미지 모드
- 위치: SPEC:100-101
- 근거: A-4 는 `found` 를 요구하지만 PoC README 도 실측 숫자는 「고정값이 아니다」라고 적는다(README 「검증된 사실」). 블로그 **이미지 모드**(썸네일 다운로드·해시·앞순위 실패 판정, `blog.mjs:86-103`)는 실물 경로인데 A-1 의 단위 테스트(해시만) 외에 실수집 확인이 없다 — 외부 서비스 경로는 실물 1회가 완료 조건이다.
- 제안: A-4 가 `not_found` 일 때의 처리(재시도·사용자 보고)를 한 줄. A-5 에 이미지 모드 1건(`found`/`not_found`, 오류 아님) 추가.

### W-11. 작은 빈칸들
- DEC D-11(DEC:72) 「RUNBOOK 로 절차 고정」 ↔ WORK P5(WORK:32) `desktop/README.md` — 이름·위치 하나로.
- SPEC §1 구성(SPEC:33) 「PoC `src/` 사본」 — `index.html`(PoC 루트, `<title>블로그 상위 노출 · SCAX</title>`)이 `src/` 밖이라 사본 대상에서 빠진다. 창 제목도 이것인지 `SC Rank` 인지.
- PoC `vite.config.js:4` 는 포트 13000 strictPort + `/api` 프록시. desktop 쪽 dev 포트를 PoC 와 다르게(동시에 떠 있으면 충돌) 하고 프록시는 없앤다고 적어 두면 좋다.
- A-1 의 블로그 해시 테스트는 PoC 루트 `1.png`(`tests/blog.test.mjs:12`)와 sharp 로 만든 변형(JPEG q60 축소·좌우반전, `:13-15`)에 기댄다. 픽스처를 `desktop/` 로 복사할지 상대경로로 읽을지, 변형을 `image` 크레이트로 만들 때 단언(≤6 / >6)은 그대로라는 점을 적어 둔다.
- 번들: SPEC 배포물은 NSIS 1개(D-09·D-13)인데 macOS 에서 `tauri build` 기본값은 `.app`/`.dmg` 를 만든다. `bundle.targets = ["nsis"]` 로 고정할지 명시.
- 로그: PoC 의 단계 로그(`[place]`·`[blog]` JSON, `place.mjs:53`, `blog.mjs:84·90·108·111`)를 옮길지 없음. WORK P3 가 「로그를 보고」하라는데 GUI 앱(Windows 는 콘솔 없음)에서 로그가 어디로 가는지 정해야 워커·코디가 같은 걸 본다.

---

## PASS 로 본 것
- DEC 정합: 범위(D-06 파워링크 제외 · SPEC:107), OS(D-04·D-13 · SPEC:38), 브라우저 순서·없을 때(D-12 · SPEC:62-63), 배포(D-09·D-10 · SPEC:39), 위치(D-07 · SPEC:32), 상태(D-03 · SPEC:36) — 어긋남 없음.
- §2 명령 셋 ↔ PoC 화면 호출 1:1: 화면이 부르는 것은 `/api/place/check`·`/api/blog/check`(`main.jsx:62`)·`/api/export`(`:76`) 셋뿐 — `check_place`·`check_blog`·`export_xlsx` 와 일치. 입력 필드도 화면 전송 본문과 같다(`main.jsx:62` — 블로그 `{keyword,target,targetType,imageData(이미지일 때만),imageName}`, 플레이스 `{keyword,target}`).
- 동시 1건·간격: 공유 `busy`·`nextAllowed`, 블로그 700ms·플레이스 2000ms, 결과가 오류여도 갱신(`index.mjs:13-14·31·39`) — SPEC:54 와 일치. 화면 대기 1000/2200ms(`main.jsx` run 루프) 일치.
- export 검증 1~50행·`keyword` 문자열(`index.mjs:45`) — SPEC:56 일치. 기본 파일명 `네이버_키워드순위_YYYY-MM-DD.xlsx`(한국 날짜, `main.jsx:79`) — SPEC:87 일치.
- 브라우저 재사용·끊기면 재기동(`place.mjs:36-43`), 조회마다 컨텍스트, `ko-KR`·1400×900(플레이스·블로그 둘 다, `place.mjs:59`·`blog-browser.mjs:8`) — SPEC:65-66 일치. 블로그도 같은 브라우저를 공유(`blog-browser.mjs:2·7`).
- 판정 핵심: 공백 무시 부분 일치(`place.mjs:32`), 거리 ≤6(`blog.mjs:98`), 동시 8건(`:91`), 250×208 cover(`:78`), 앞순위 실패 시 확정 불가(`:101-102`), 이미지 4MB·PNG/JPEG/WebP(`:59-61`), 썸네일 호스트·경로(`:66`) — 표가 가리킨다.
- A-1 범위: `place.test.mjs` 9개(엑셀 1개 포함)·`blog.test.mjs` 3개(`mapConcurrent` 포함), `search.test.mjs` 제외는 D-06 과 정합.
- WORK P5 의 Windows 타깃 `cargo check` 는 「못 하면 사유 보고」가 붙어 있어 확인 가능.

## 사용자가 실물에서 만날 자리
- **F-3**: 다른 조회가 진행 중일 때 오류 행 메시지가 빈 칸 / 브라우저 기동이 멈추면 화면이 끝없이 「조회 중」.
- **F-5**: 「네이버」「매칭 글」 버튼을 눌러도 아무 일도 안 일어남.
- **F-2**: 조회 실패 행에 영어 CDP/HTTP 오류 문장이 그대로 뜸.
- **F-4**: Windows·Edge 에서 macOS·PoC 와 다른 목록(=다른 순위)이 나올 수 있음 — A-9 에서야 드러난다.
- W-4: 중단한 뒤 「엑셀 저장하기」가 실패(취소·오류 행 역직렬화).
- W-8·W-11: 첫 실행 시 Windows 방화벽/보안 프롬프트나 dev 포트 충돌 — 방화벽은 CDP 가 `127.0.0.1` 바인딩이면 뜨지 않는다(확인 대상).
- 이미지 모드(W-10)는 실물 확인 없이 Windows 사용자 손에 처음 닿는다.

## 참고(기존 부채) — 이번 판정과 무관
- PoC `README.md` 상단은 「블로그 상위 노출 = 파워링크」 시절 서술이 남아 있고(파워링크 기본 도메인 `daybeauclinic13.com`, 단위 테스트 6개 등) 아래 절과 모순된다. SPEC 이 README 를 정본으로 인용하지 않으므로 영향 없음.
- PoC `index.mjs:11` 의 `express.json({limit:'7mb'})` 는 이미지 dataURL(4MB → 약 5.6MB)을 담기 위한 상한. `invoke` 로 옮기면 사라지는 제한이라 옮길 대상 아님 — 다만 키워드마다 5.6MB 가 IPC 로 반복 전송된다(PoC 도 매 요청 전송, 동작 동일).
- PoC `collectPlaceList` 의 60초 상한은 `Promise.race` 라 **작업을 취소하지 않고** 컨텍스트만 닫는다(`place.mjs:107-108`). Rust 에서 실제 취소로 구현해도 관측 동작은 같다.

---

## 재검수 (2회차) — 2026-09-30

대상: SPEC-001 v0.2.0 · WORK-001 · DEC-001 D-11/D-14. 1회차 F-1~F-6 · W-1~W-11 이 닫혔는지와 **수정이 만든 새 모순**만 봤다. 새 전수조사는 하지 않았다.

### 판정: WARN (구현 발주 가능)

FAIL 6건 전부 닫힘 · WARN 11건 전부 닫힘. 수정 과정에서 새로 생긴 작은 불일치 3건(N-1~N-3)이 있다. 셋 다 워커가 추측으로 메울 자리는 아니고 문구 정합 문제다.

### 1회차 항목 대조

| # | 결과 | 근거 |
|---|---|---|
| F-1 §4 전수 | 닫힘 | SPEC:88-89 「본문 전체를 옮긴다 … 표에 없다고 옮기지 않아도 되는 것이 아니다」 + SPEC:94-98 에 1회차 누락값(30/20/8/60초, 25/12/150초, 정규식·셀렉터, 썸네일 8초·6MB, 전처리, 최솟값 거리, 캐시, 문구) 반영 |
| F-2 오류 문구 폴백 | 닫힘 | SPEC:102-110 — 도메인 오류는 그대로, 나머지(CDP·HTTP·IO·디코드·기동)는 영역별 폴백, 블로그 폴백 문구 포함, 원래 오류는 로그로 |
| F-3 Err 문자열·180초 | 닫힘 | SPEC:114-117 — reject 문자열 → `Error` 로 감쌈, 화면 `Promise.race` 180초 유지, 문구 `main.jsx:66` 동일 |
| F-4 UA | 닫힘 | SPEC:83 — 실행 브라우저 실제 UA 의 `HeadlessChrome`→`Chrome`, PoC 와 다른 점을 의도된 변경으로 명시, 썸네일은 `blog.mjs:7` 그대로 |
| F-5 링크 = 세 번째 변경 | 닫힘 | SPEC:112 「이 셋뿐」, SPEC:120-121 진입부 가로채기 + opener, DEC D-14(DEC:75) 링크 추가 |
| F-6 실수집 수단 | 닫힘 | SPEC:125-126 `examples/smoke.rs`, A-4·A-5 명령·인자 고정(SPEC:133-134), A-7 후보 목록 인자 + `cargo test`(SPEC:78·136), A-8 창 닫기 + `pgrep -f sc-rank-cdp-`(SPEC:84·137) |
| W-1 블로그 검증 = 정상 반환 | 닫힘 | SPEC:62-68 명령별 Err 표(플레이스 검증은 busy 앞·간격 갱신 없음) |
| W-2 출력 키 | 닫힘 | SPEC:50·58-60 camelCase · `null` 직렬화 · 분기별 모양 |
| W-3 invoke 인자 모양 | 닫힘 | SPEC:49 평평한 인자 |
| W-4 export 느슨한 행 | 닫힘 | SPEC:72 |
| W-5 엑셀 파생 열 | 닫힘 | SPEC:98 (파워링크 폴백 문구는 그대로 옮기는 것으로 결정) |
| W-6 저장 실패 문구 | 닫힘 | SPEC:119 모든 실패에 `main.jsx:77` 문구 |
| W-7 페이지 안 JS 범위 | 닫힘 | SPEC:99 `place.mjs:74-80·94-99`, `blog-browser.mjs:25·35-42` 포함 문자열 주입. DEC D-05(DEC:54)는 `place-dom.mjs` 만 적지만 SPEC 이 상위집합이라 모순 아님 |
| W-8 CDP 포트 해석 | 닫힘 | SPEC:37 — 앱이 여는 서버만 금지, CDP 는 `127.0.0.1` 임의 포트/파이프 허용. D-02 본문(DEC:51)에는 주석이 없다 — 코드 검수는 SPEC:37 을 기준으로 삼으면 됨 |
| W-9 A-3 배정·P1/P4 확인 | 닫힘 | WORK:29-31 끝 조건에 A-3, P4 산출물(xlsx 경로 + 로그 발췌), A-7→P2, A-8→P4. A-1~A-9 전부 Phase 또는 사용자에 배정됨 |
| W-10 A-4 not_found·이미지 모드 | 닫힘 | SPEC:133 not_found 는 실패 아님·그대로 보고, SPEC:134 이미지 모드 1회 |
| W-11 잔여 | 닫힘 | RUNBOOK=README(DEC:72, WORK:32) · `index.html` 사본(SPEC:35) · dev 포트 13100 · 프록시 없음(SPEC:37) · 픽스처 복사·`image` 변형·단언 유지(SPEC:130) · `bundle.targets=["nsis"]`(SPEC:42) · 로그 위치(SPEC:43) |

### 새로 생긴 불일치 (WARN)

- **N-1. clippy 명령이 두 곳에서 다르다.** SPEC:132 A-3 은 `cargo clippy --all-targets -- -D warnings`, WORK:47 검증 분담은 `cargo clippy -- -D warnings`. `--all-targets` 가 빠지면 테스트·`examples/smoke.rs` 의 경고가 관문을 통과한다. → WORK:47 을 SPEC 에 맞춘다.
- **N-2. 「화면 변경은 셋뿐」과 `index.html` 제목 변경.** SPEC:35 는 사본의 `<title>` 을 `SC Rank` 로 바꾸는데 SPEC:112·DEC D-14 는 「이 셋뿐」이다. 창 제목은 `tauri.conf` 가 정하므로(SPEC:42) 실질 영향은 없지만, 코드 검수에서 「§5 외 변경」으로 걸릴 수 있다. → §5 에 「`index.html` 제목은 앱 이름으로」 한 줄 두거나 SPEC:35 에서 제목 변경을 뺀다.
- **N-3. SPEC 이 작업 폴더 파일을 가리킨다.** SPEC:28·90 이 `orchestration/work/sc-rank-desktop/review-doc-report.md` 를 세부 목록 출처로 든다. slug 마감(아카이브) 때 `work/` 가 옮겨지면 링크가 끊긴다. SPEC:88 이 「본문 전체」라 동작 영향은 없음. → 아카이브 때 경로 갱신, 또는 「PoC 정본 함수」만 근거로 남긴다.

### 참고 (판정 무관)
- SPEC:114-117 은 연결 모듈이 fetch 의 `Response` 모양을 흉내 낼지, `main.jsx:63-64·77-79` 를 직접 고칠지를 워커 재량으로 남긴다. 어느 쪽이든 §5-1·§5-2 범위 안이라 빈칸으로 보지 않았다.
- 180초 화면 상한이 먼저 끝나도 Rust 쪽 잠금은 조회가 끝날 때까지 유지되어 다음 키워드가 「다른 조회가 진행 중」으로 실패할 수 있다. PoC 도 abort 가 서버를 멈추지 않아 동작이 같다.
