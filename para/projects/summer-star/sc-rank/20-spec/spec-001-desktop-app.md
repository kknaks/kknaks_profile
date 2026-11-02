---
type: spec
id: SPEC-001
title: "SC Rank 데스크톱 앱 — 앱 경계 · 명령 계약 · 수집 규칙 이식"
status: draft
version: 0.2.3
product: sc-rank
created_at: 2026-09-30
updated_at: 2026-10-01
tags:
  - product/sc-rank
  - doc/spec
links:
  baselines:
    - "[[baseline-001-desktop-app|BASE-001]]"
  decisions:
    - "[[decision-001-desktop-app|DEC-001]]"
  works:
    - "[[work-001-desktop-port|WORK-001]]"
---

# SC Rank 데스크톱 앱 — 앱 경계 · 명령 계약 · 수집 규칙 이식

웹 PoC 를 서버 없는 Tauri 앱으로 옮긴다(DEC-001). **동작의 정본은 PoC 코드다.**
이 스펙은 무엇이 바뀌는지(§1~§3·§5)와 옮기는 방식(§4)을 적는다.
PoC 경로는 모두 `reference/2026-09-09-sc-prototype/` 기준이다.

> v0.2.0 — 문서 검수 FAIL 6 · WARN 11 반영(이력은 `log.md`).

## 1. 앱 경계

| 항목 | 계약 |
|---|---|
| 위치 | 코드 레포 `kknaksss/sc-rank` 루트 (D-07, 10-01 개정). PoC(kknaks_profile `reference/2026-09-09-sc-prototype/` 의 `server/`·`src/`·`tests/`·`index.html`·`1.png`)는 **수정 금지** |
| 구성 | `index.html`(PoC 사본, 무변경 — 창 제목은 `tauri.conf.json` 이 정한다) · `src/`(PoC `src/` 사본 + §5 의 연결 모듈) · `src-tauri/` · 주입 JS 동일성 검사용 PoC 원본 사본(`poc/`, 읽기 전용) |
| 프로세스 | 앱 프로세스 1개 + 조회 중에만 쓰는 헤드리스 브라우저 1개 |
| 포트 | D-02 의 「포트 없음」은 **앱이 여는 서버**를 뜻한다. 브라우저 CDP 연결은 `127.0.0.1` 임의 포트 또는 파이프로 허용(외부 바인딩 금지). 개발 서버(vite)는 `13100` strictPort, `/api` 프록시 없음 — PoC(13000)와 동시에 떠도 충돌하지 않게 |
| 화면↔로직 | Tauri `invoke` 명령 셋(§2). 화면에 `fetch` 가 남지 않는다 |
| 상태 | 결과는 화면 메모리에만 (D-03) |
| 네트워크 | 네이버 검색·지도 페이지와 블로그 썸네일(`search.pstatic.net`) 요청만 |
| 대상 OS | 운영 Windows 10/11 x64. 개발 macOS (D-04·D-13) |
| 배포물 | `bundle.targets = ["nsis"]` 고정, 서명 없음 (D-09·D-10). GitHub Actions `windows-build` 가 만든다 — PR 은 산출물, `v*` 태그는 Release (D-11). 앱 이름 `SC Rank`, 식별자 `com.summerstar.scrank`, 창 제목 `SC Rank` |
| 로그 | PoC 단계 로그(`[place]`·`[blog]` JSON 한 줄)를 같은 필드로 남긴다. 앱: OS 앱 로그 디렉터리의 파일(`tauri-plugin-log`), smoke 예제: 표준 출력 |

## 2. 명령 계약

### 2.1 호출 모양

`invoke(명령, 평평한 인자)` — 인자 최상위 키가 곧 입력 필드다(구조체로 한 번 더 감싸지 않는다).
Rust 직렬화는 `rename_all = "camelCase"`, `Option` 은 **`null` 로 직렬화**(키 생략 금지).

| 명령 | 인자 | 성공 반환 | PoC 대응 |
|---|---|---|---|
| `check_blog` | `{ keyword, targetType, target, imageData?, imageName? }` | PoC `checkBlog` 반환 객체와 같은 키 | `POST /api/blog/check` |
| `check_place` | `{ keyword, target }` | PoC `checkPlace` 반환 객체와 같은 키 (`rows` 포함) | `POST /api/place/check` |
| `export_xlsx` | `{ rows, mode }` | `{ saved: true, path }` 또는 `{ saved: false }`(대화상자 취소) | `POST /api/export` |

반환 키는 PoC 성공·오류 반환을 **분기별로 그대로** 따른다 — 플레이스 오류 `total·totalAds: null, matches: [], rows: []`
(`place.mjs:118`), 블로그 오류 `total: null, matches: []`·`scrolls` 없음(`blog.mjs:112`), 블로그 성공 `scrolls`,
이미지 모드 `comparedImages`·`matches[].imageUrl`·`matches[].hashDistance`.

### 2.2 명령 실패(`Err(String)`) — PoC 의 400·429 자리뿐

| 명령 | Err 가 되는 것 (순서대로) | 문구 |
|---|---|---|
| `check_place` | ① 입력 검증 (busy 검사 **앞**, 간격 갱신 없음) ② 진행 중·간격 미달 | `index.mjs:35` · `index.mjs:36` |
| `check_blog` | 진행 중·간격 미달 **만**. 입력 검증은 PoC 처럼 `status: "error"` 정상 반환(`blog.mjs:74-77`) | `index.mjs:28` |
| `export_xlsx` | 입력 검증(1~50행 · 각 행 `keyword` 문자열) · 파일 생성/쓰기 실패 | `index.mjs:45` · `index.mjs:51` |

- 조회 결과 오류는 명령 실패가 아니다 — `status: "error"` + `message` 정상 반환.
- **동시 1건·간격**: 블로그·플레이스가 한 잠금을 공유한다. 결과가 오류여도 끝난 시점부터 블로그 0.7초 · 플레이스 2초 (`index.mjs:13-14·31·39`).
- `export_xlsx` 의 `rows` 는 **느슨하게** 받는다(`serde_json::Value` 또는 전 필드 `Option`). 화면이 만든 중단 행·오류 행·플레이스 `rows` 목록이 섞여 온다(`main.jsx:66·70`).

## 3. 브라우저 (D-05 · D-12)

| 항목 | 계약 |
|---|---|
| 탐색 | Microsoft Edge → Google Chrome, OS 표준 설치 경로 (Windows: `Program Files`·`Program Files (x86)`·`%LOCALAPPDATA%`, macOS: `/Applications`). **탐색 함수는 후보 경로 목록을 인자로 받는다** — 빈 목록·없는 경로로 단위 테스트한다(A-7) |
| 없을 때 | 해당 조회만 `status: "error"`, 문구 「Edge 또는 Chrome 을 찾지 못했습니다. 둘 중 하나를 설치한 뒤 다시 조회해 주세요.」 |
| 조종 | CDP. Chromium 동봉 금지 |
| 기동 | 헤드리스. 전용 임시 프로필 디렉터리(이름 접두 `sc-rank-cdp-`). 사용자 브라우저 프로필 금지. 앱당 1개를 블로그·플레이스가 공유·재사용하고 끊기면 다음 조회에서 다시 띄운다 (`place.mjs:36-43`) |
| 조회 단위 | 조회마다 새 격리 컨텍스트, 끝나면 닫는다. `ko-KR`, 1400×900 |
| User-Agent | 플레이스·블로그 컨텍스트 모두 **실행 브라우저의 실제 UA 에서 `HeadlessChrome` 을 `Chrome` 으로 바꾼 문자열**. PoC 와 다른 점(플레이스는 Mac Chrome/128 고정, 블로그는 헤드리스 UA 그대로)은 **의도된 변경**이다 — Windows 에서 Windows UA 로 보인다. 썸네일 HTTP 요청은 PoC 문자열 그대로(`blog.mjs:7`) |
| 종료 | 앱 창이 닫히면(마지막 창 = 앱 종료) 브라우저 프로세스를 끝내고 임시 프로필을 지운다. 비정상 종료로 남은 `sc-rank-cdp-*` 는 다음 기동 때 지운다 |

## 4. 옮기는 방식

**PoC 정본 함수의 본문 전체를 옮긴다.** 판정·정규식·셀렉터·문구·제한값·타임아웃은 PoC 와 같아야 한다.
아래 표는 범위와 **특히 틀리기 쉬운 것**이다 — 표에 없다고 옮기지 않아도 되는 것이 아니다.

| 영역 | 정본 (본문 전체) | 틀리기 쉬운 것 |
|---|---|---|
| 플레이스 수집 | `place.mjs` `collectPlaceList` | goto 30초 · 첫 항목 20초 · 기본 8초 · 전체 60초 · 프레임 판정(`searchIframe` + `pcmap`) · 셀렉터 · 항목 정규식 4종 · 상호 없음 처리(`:86`) · `added==0` 처리(`:91`) · 다음 번호 **마지막** 요소 클릭, 없으면 조용히 종료 |
| 플레이스 판정 | `extractPlaceName` · `parsePlaceList` · `checkPlace` · `PLACE_SCOPE` | 오류 문구 전부 · not_found 안내 |
| 블로그 수집 | `blog-browser.mjs` `blogBatches` | goto 25초 · 첫 카드 12초 · 응답 대기 **스크롤 전 등록** · 응답 판정 4갈래(`:27-33·44`) · 렌더 조건 `headline 카드 ≥ before+added` · 150초 |
| 블로그 판정 | `blog.mjs` 전부 | 썸네일 8초·6MB·비 2xx 실패 · 전처리(EXIF 회전 → 흰 배경 합성 → 32×32 fill → 회색조, 픽셀 상한 25,000,000) · 목표 해시 2종 중 **최솟값** 거리 · 배치 간 썸네일 캐시 · 썸네일 0건 문구 · found 면 다음 배치 중단 · 검증 문구 3종 · `scope` 두 가지 · 이미지 모드 `target` = `imageName` 또는 「업로드 이미지」 |
| 엑셀 | `workbook.mjs` `makeWorkbook` · `labels` | 열 이름·키·너비 · 파생 열(`matches[0].url` · 상호 `' / '` 연결 · `matches[0].title`) · 모르는 상태 원문 · `not_found` 빈 메시지 폴백 문구(파워링크 문구 그대로) · 머리행 28/굵은 흰색/`FF5467F7` · 본문 25/11pt/세로 가운데 · 틀 고정 · 필터 `A1:K{n}`/`A1:M{n}` · creator `SCAX` · 수식형 문자열도 텍스트 |
| 페이지 안 JS | `place-dom.mjs` 전부 · `place.mjs:74-80`·`:94-99` · `blog-browser.mjs:25`·`:35-42` | PoC 가 `evaluate` 로 넘기는 함수 본문은 **전부 문자열 그대로 주입**한다. Rust 에서 DOM 을 다시 질의해 짜지 않는다 |
| 화면 | `src/` 전부 | §5 외 무변경 |

**오류 문구 규칙 (PoC 의 한글 판정 대응).** PoC 가 한글 문구로 던지는 도메인 오류는 문구 그대로 행 `message` 가 된다.
그 밖의 모든 오류(CDP·HTTP·IO·디코드·브라우저 기동)는 영역별 폴백 문구로 바꾼다 — 영어 오류 문장을 화면에 내지 않는다.

| 영역 | 폴백 문구 |
|---|---|
| 플레이스 | 「플레이스 조회에 실패했습니다. 브라우저 설치 또는 네이버 접근 제한을 확인해 주세요.」 (`place.mjs:118`) |
| 블로그 | 「블로그 조회 또는 이미지 처리가 실패했습니다. 잠시 후 다시 확인해 주세요.」 (`blog.mjs:112`) |

§3 「브라우저 없음」 문구는 도메인 오류로 취급해 그대로 낸다. 원래 오류는 로그에만 남긴다.

## 5. 화면에서 바뀌는 곳 (D-14 — 이 셋뿐)

1. **호출**: `fetch('/api/...')` 세 곳 → 연결 모듈 `src/bridge.js` 의 함수 호출. 연결 모듈이
   - `invoke` 의 reject 값(문자열)을 `Error(문자열)` 로 감싸 PoC 의 기존 `catch` 로 넘긴다 — 「다른 조회가 진행 중입니다…」가 행 메시지로 보인다
   - 조회 명령은 **180초 상한을 화면에서 유지**한다(`Promise.race`). 넘기면 PoC 와 같은 「조회 시간이 초과되었습니다.」 (`main.jsx:66`)
   - `check_place` Err 는 PoC `!res.ok` 분기와 같은 결과(오류 행)가 된다
2. **저장**: 브라우저 다운로드 → 저장 대화상자. 기본 파일명 `네이버_키워드순위_YYYY-MM-DD.xlsx`(한국 날짜), `.xlsx` 필터.
   취소하면 메시지 없음. **모든 `export_xlsx` 실패**는 화면에서 「엑셀을 저장하지 못했습니다. 다시 시도해 주세요.」(`main.jsx:77`).
3. **링크**: 결과 표의 「네이버」「매칭 글」(`<a target="_blank">`, `main.jsx:115`)은 OS 기본 브라우저로 연다.
   `main.jsx` 의 `<a>` 는 그대로 두고 **진입부에서 `a[target=_blank]` 클릭을 가로채** `tauri-plugin-opener` 로 연다. 앱 창은 이동하지 않는다.

## 6. 인수 조건

실수집 수단은 `src-tauri/examples/smoke.rs` 하나다(PoC `scripts/smoke.mjs` 대응). 앱과 같은 수집 함수를 부르고
결과 요약 JSON 을 표준 출력에 낸다. `status == "error"` 면 exit 1.

| # | 조건 | 확인 수단 |
|---|---|---|
| A-1 | `tests/place.test.mjs` 9개 · `tests/blog.test.mjs` 3개가 같은 단언으로 Rust 테스트 통과. 해시 테스트 픽스처는 PoC `1.png` 를 `src-tauri/tests/fixtures/` 로 복사하고, 변형(JPEG q60 축소·좌우 반전)은 `image` 크레이트로 만든다. 단언(≤6 / >6)은 그대로 | `cargo test` |
| A-2 | 엑셀 블로그 11열·플레이스 13열 머리·순서 · 숫자 순위 · 빈 값 · 수식형 문자열 텍스트 | `cargo test` |
| A-3 | `cargo clippy --all-targets -- -D warnings` 0 · `npm run build` 성공 | 명령 |
| A-4 | 플레이스 실수집 `cargo run --example smoke -- place 강남역성형외과 무이성형외과` 가 오류 아님. `found` 를 기대하되 `not_found` 면 실패로 치지 않고 결과를 그대로 보고(순위는 고정값이 아니다) | smoke |
| A-5 | 블로그 실수집 — 키워드 모드 `smoke -- blog 구월동레이저제모 keyword 썸블리의원`, 이미지 모드 `smoke -- blog 구월동피부과 image tests/fixtures/1.png` 각 1회가 오류 아님 | smoke |
| A-6 | 화면에서 조회 → 저장 대화상자 → 파일이 엑셀로 열림 · 링크가 OS 브라우저로 열림 | 사용자 E2E |
| A-7 | 후보 경로가 빈 탐색이 §3 문구의 오류를 낸다 | `cargo test` |
| A-8 | 앱 창을 닫은 뒤 `pgrep -f sc-rank-cdp-` 결과 없음 · 임시 프로필 디렉터리 없음 | 코디 실행 |
| A-9 | Windows: Actions 산출물(또는 Release) 설치 파일로 설치 → 실행 → A-4 에 해당하는 조회와 A-6. Actions 의 Windows `cargo test` 통과는 컴파일·단위 테스트 증거일 뿐 실행 확인을 대신하지 않는다 | 사용자 (Windows PC) — **macOS 통과로 대신하지 않는다** |

## 7. 이식 중 확정한 PoC 와의 차이 (v0.2.1)

구현·검수에서 드러나 **수용한** 차이다. 판정 기준(순위·≤6 거리·오류/미노출 구분)은 바뀌지 않는다.

| 차이 | 사유 |
|---|---|
| WebP 목표 이미지의 두 번째 해시(250×208 cover)는 다시 인코딩하지 않고 픽셀로 바로 해시한다. PoC(sharp)는 손실 WebP q80 으로 재인코딩한다 | Rust `image` 에 손실 WebP 인코더가 없다. PNG·JPEG 는 PoC 와 비트까지 같다 |
| 플레이스 `rows[]` 는 `id`·`reviews`·`addr` 를 늘 싣는다(없으면 `null`) | 실수집 항목에는 PoC 도 셋이 늘 있다 |
| `check_blog` 인자 `null` 은 「키 없음」과 같게 처리된다 | Tauri `Option` 이 둘을 구분하지 않는다. 화면은 늘 문자열을 보낸다 |
| 엑셀: 빈 문자열은 서식만 있는 빈 셀 · 날짜 해석은 RFC3339·epoch 만 | 읽으면 같은 값. 화면이 보내는 값 범위 안 |
| 플레이스 60초 초과가 브라우저 기동 중에 걸리면 임시 프로필이 다음 기동의 잔여 정리까지 남는다 | 기동은 취소할 수 없다. 다음 기동 때 정리된다(§3) |

## 8. 범위 밖

파워링크 조회 · 새 화면·새 기능 · 이력 저장 · 자동 업데이트 · 서명 · macOS 배포.
