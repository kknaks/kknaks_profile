# WORK-001 P1·P2 결과 보고

## 상태: done

P1 뼈대와 P2 순수 로직·테스트 이식을 끝냈다. 커밋·push·PR 은 하지 않았고, 워크트리에 변경만 있다(`reference/2026-09-09-sc-prototype/desktop/` 아래 파일 37개, 그 밖은 무변경).
P3(브라우저·CDP·네이버 요청)와 P4(화면 연결)는 하지 않았다.

## 수행 — 파일·모듈 목록

모든 경로는 `reference/2026-09-09-sc-prototype/desktop/` 기준이다.

**P1 뼈대**
| 파일 | 내용 |
|---|---|
| `index.html` | PoC `index.html` 사본, 무변경(`cmp` 로 동일 확인) |
| `src/` (`main.jsx`·`style.css`·`vendor/Icon.tsx`·`vendor/scax.css`) | PoC `src/` 사본, 무변경(`diff -r` 로 동일 확인). 화면은 P4 까지 그대로 둔다 |
| `package.json` · `package-lock.json` | react/react-dom 19.1.1 · vite 6.4.3(PoC 와 같은 판) · `@tauri-apps/api`·`@tauri-apps/cli` 2.12.0 |
| `vite.config.js` | `127.0.0.1:13100` strictPort, `/api` 프록시 없음 |
| `.gitignore` | `node_modules/`·`dist/`·`src-tauri/target/`·`src-tauri/gen/schemas/` |
| `src-tauri/tauri.conf.json` | productName `SC Rank` · identifier `com.summerstar.scrank` · 창 제목 `SC Rank` · `bundle.targets=["nsis"]` · devUrl `http://127.0.0.1:13100` |
| `src-tauri/capabilities/default.json` | `core:default`·`log:default`·`dialog:default`·`opener:default` |
| `src-tauri/Cargo.toml` · `build.rs` · `Cargo.lock` | tauri 2.12.0 · plugin-log 2.10.0 · plugin-dialog 2.8.0 · plugin-opener 2.7.0 · scraper 0.24 · image 0.25.10 · rust_xlsxwriter 0.90.2. 테스트 전용: calamine 0.30 · zip 2. `Cargo.lock` 에 openssl 계열 없음 |
| `src-tauri/icons/` | 자리표시 아이콘(단색 `#5467F7`)을 `tauri icon` 으로 생성 |
| `src-tauri/src/main.rs` · `lib.rs` | 플러그인 등록(log 는 OS 로그 디렉터리 파일 `sc-rank.log` 하나, Info) · 명령 셋 등록 |
| `src-tauri/src/commands.rs` | `check_blog(keyword, targetType, target, imageData, imageName)` · `check_place(keyword, target)` · `export_xlsx(rows, mode)` — 평평한 인자, 전부 `Option<serde_json::Value>`. 본문은 `Err("아직 구현되지 않은 기능입니다.")` 만 돌려준다. 반환 타입은 `BlogResult`·`PlaceResult`·`ExportResult{saved, path?}` |

**P2 순수 로직**
| 파일 | PoC 정본 | 옮긴 것 |
|---|---|---|
| `src/js.rs` | — | JS 의미 도우미: `\s`·`trim()` 문자 집합, `length`(UTF-16), 참/거짓, `String()`, `encodeURIComponent`, `toISOString()` |
| `src/errors.rs` | `place.mjs:118` · `blog.mjs:112` | `ScrapeError::{Domain, Other}` · `user_message(Area)` — Domain 은 문구 그대로, Other 는 영역별 폴백 |
| `src/place.rs` | `place.mjs:4-34` · `:111-118` · `index.mjs:35` | `PLACE_SCOPE` · `place_url` · `extract_place_name` · `parse_place_list` · `validate_place_input` · `place_result`(성공·오류 반환 모양) · `PlaceItem`(페이지 JS 추출 결과 역직렬화 겸용) |
| `src/blog.rs` | `blog.mjs` 전부 (curl·`blogBatches` 호출 제외) | `blog_url` · `parse_blog_list` · `match_blog_keyword` · `decode_image`(EXIF 회전 + 25,000,000 픽셀 상한) · `hash_image`/`image_hash` · `target_hashes`(2종) · `hash_distance`/`min_distance` · `map_concurrent` · `decode_target_image` · `image_url` · `new_thumbnail_urls`(배치 간 캐시·0건 문구) · `judge_image_batch`(최솟값·≤6·앞순위 실패) · `BlogInput`(검증 3종·scope·target) · `blog_result`(반환 모양) · P3 에서 쓸 상수(썸네일 UA·8초·6MB·동시 8) |
| `src/workbook.rs` | `workbook.mjs` 전부 · `index.mjs:45·51` | `label` · 열 세 벌(블로그 11 · 플레이스 13 · 그 밖 10) · 파생 열 · `make_workbook` · `validate_rows` · `Mode::from_value` |
| `src/browser.rs` | SPEC §3 | `find_browser(candidates)` — 없으면 §3 문구의 Domain 오류 · `default_candidates()`(Windows `ProgramFiles`·`ProgramFiles(x86)`·`LOCALAPPDATA`, macOS `/Applications`, Edge→Chrome 순서, `cfg` 로 나눔) |
| `src-tauri/tests/fixtures/1.png` | PoC `1.png` | 복사본 |
| `tests/place.rs` | `tests/place.test.mjs` | 9개, 같은 단언 |
| `tests/blog.rs` | `tests/blog.test.mjs` | 3개, 같은 단언(변형은 `image` 크레이트: 폭 180 Lanczos3 → JPEG q60 · 좌우 반전 PNG) |
| `tests/workbook.rs` | A-2 | 블로그 11열·플레이스 13열 머리와 순서 · 숫자 순위 · 빈 값 · 수식형 문자열 텍스트 · 라벨/원문 상태 · 파생 열 · 머리행 28/굵게/흰 글씨/`FF5467F7` · 본문 25/세로 가운데 · 틀 고정 · 필터 `A1:M4`·`A1:K2` · 너비 · creator `SCAX` · 1~50행 검증 |
| `tests/browser.rs` | A-7 | 빈 후보 → §3 문구 · 없는 경로와 디렉터리를 건너뛰고 Edge→Chrome 순으로 고른다 |
| `tests/blog_rules.rs` · `tests/place_rules.rs` | `blog.mjs` · `place.mjs` 나머지 | 검증 문구·scope·target·dataURL·썸네일 주소·이미지 배치 판정·캐시·반환 모양(성공·오류 키) |

## 검증 — 명령과 수치

| 명령 | 결과 |
|---|---|
| `cd desktop/src-tauri && cargo test` | **33 passed / 0 failed** (lib 단위 3 · blog 3 · blog_rules 8 · browser 2 · place 9 · place_rules 2 · workbook 6) |
| `cargo clippy --all-targets -- -D warnings` | 경고 0 |
| `cargo fmt` | 적용함 |
| `cd desktop && npm run build` | 성공(vite, 30 modules, 391ms) |
| `npm run tauri dev` | 13100 이 비어 있는지 먼저 확인한 뒤 띄웠다. 앱 창 제목은 `SC Rank`(System Events 로 읽음)이고, PoC 화면(블로그 상위 노출, 키워드 19개)이 그대로 뜬 것을 창 캡처로 봤다. 확인 뒤 내가 띄운 프로세스(npm·tauri·vite·esbuild·sc-rank)만 종료했고 13100 이 풀린 것도 확인했다 |
| 실수집 | 해당 없음 — P2 는 네이버에 요청하지 않는다 |

**해시가 sharp 와 같은지 따로 쟀다.** 저장소 밖 스크래치 폴더에 `sharp@0.34.5` 를 깔고 PoC `imageHash` 본문을 그대로 돌려 비교했다(저장소에는 남기지 않았다).

| | sharp (PoC) | Rust (`image`) |
|---|---|---|
| `1.png` 해시 | `0111110110100110…0110100` | **비트까지 같음(거리 0)** |
| 축소 JPEG q60 거리 (≤6 이어야 함) | 0 | 0 |
| 좌우 반전 거리 (>6 이어야 함) | 34 | 34 |
| cover 250×208 과 원본의 거리 | 10 | 10 |

## PoC 대조 — SPEC-001 §4 의 P2 항목

| 영역 | 항목 | 판정 |
|---|---|---|
| 플레이스 판정 | `PLACE_SCOPE` 문자열 · `placeUrl` | 같음 |
| | `extractPlaceName`: generic 정규식 · 접미 정규식 · 제외 정규식(`\d` 는 ASCII `[0-9]`) · 길이 <80(UTF-16) · span 두 개 결합 | 같음 |
| | `parsePlaceList`: 오류 문구 3종 · 누적 순위 · `organicRank` · `page \|\| 1` · 공백 무시 부분 일치 · 결과 키 | 같음 |
| | `checkPlace` 반환: 입력 검증 문구 · not_found 안내 · 오류 모양 `total·totalAds:null, matches:[], rows:[]` · 폴백 문구 | 같음 |
| | `rows[]` 항목 키 | **다름(작음)** — 아래 이슈 1 |
| 블로그 판정 | `parseBlogList`: 제목 검사 · 카드 셀렉터 · headline/body1 · href 같은 앵커 · `src \|\| data-src` 중복 제거 · blogger 정규식 · `새 창 열림` 제거 · 오류 문구 3종 | 같음 |
| | `matchBlogKeyword`: 공백 제거·소문자·`title + ' ' + snippet` | 같음 |
| | 전처리 순서: EXIF 회전 → 흰 배경 합성 → 32×32 fill → 회색조 · 픽셀 상한 25,000,000 | 같음 (해시 비트 동일, 위 표) |
| | DCT 63비트 · 중앙값 `[31]` · 거리 · 목표 해시 2종의 **최솟값** | 같음 |
| | 목표 해시 2번째(`rotate().resize(250,208,cover)`) | PNG·JPEG 는 같음 · **WebP 는 다름** — 아래 이슈 2 |
| | `decodeTargetImage`: dataURL 정규식 · 문구 2종 · 4MB 경계 · Node 방식의 느슨한 base64 | 같음 |
| | `imageUrl`: https · `search.pstatic.net` · `/common/`·`/sunny/` · 문구 · 원래 URL 그대로 돌려줌 | 같음 |
| | `mapConcurrent`: 동시 상한 · 입력 순서 보존 | 같음 (`limit ≥ 1` 전제 — 이슈 5) |
| | 배치 간 캐시(새 URL 만) · 썸네일 0건 문구 · 거리 ≤6 · 가장 가까운 썸네일 · 앞순위 실패 문구 · `comparedImages` | 같음 |
| | 검증 문구 3종 · `scope` 두 가지 · 이미지 모드 `target = imageName \|\| '업로드 이미지'` · not_found 안내 · 오류 모양(`total:null, matches:[]`, `scrolls` 없음) · 폴백 문구 | 같음 (`null` 입력은 이슈 3) |
| | 썸네일 8초·6MB·비 2xx · UA · found 면 다음 배치 중단 | 상수만 옮겼다. 동작은 P3 |
| 엑셀 | 열 이름·키·너비 세 벌 · 라벨 · 모르는 상태 원문 · `matches[0].url` · 상호 `' / '` · `matches[0].title` · not_found 빈 메시지 → 파워링크 문구 | 같음 |
| | 머리행 28/굵게/흰 글씨/`FF5467F7` · 본문 25/11pt/세로 가운데 · 틀 고정 · 필터 `A1:K{n}`/`A1:M{n}`/`A1:J{n}` · creator `SCAX` · 시트 이름 · 수식형 문자열은 텍스트 | 같음 |
| | 한국 시각 `YYYY-MM-DD HH:MM:SS` | 같음 (파싱 범위는 이슈 4) |
| | 빈 문자열 셀 · 객체/배열 값 | **다름(작음)** — 이슈 4 |
| | 저장 검증 1~50행·`keyword` 문자열 · 문구 | 같음 |
| 오류 문구 규칙 | 도메인 오류는 그대로, 나머지는 영역별 폴백 | 같음. PoC 는 「한글이 있는가」로 가르고, Rust 는 `Domain`/`Other` 변형으로 명시해서 가른다 |
| §3 브라우저 탐색 | 후보 목록 인자 · Edge→Chrome · 없으면 §3 문구(도메인 오류) | 같음 (A-7 통과) |

## 이슈 · 코디가 확인할 것

1. **플레이스 `rows[]` 키.** PoC 는 `{...item}` 을 펼쳐서 항목에 있던 키만 남긴다. Rust 는 `id·reviews·addr` 를 늘 `null` 로 내보낸다(`title·spans` 는 항목에 있을 때만 붙는다). 실제 수집 항목에는 PoC 도 이 셋이 늘 들어 있어서(`place.mjs:88`) 실사용 출력은 같다. 테스트처럼 `{name, ad, page}` 만 넣었을 때만 달라진다.
2. **WebP 목표 이미지의 두 번째 해시.** sharp 는 cover 로 줄인 이미지를 입력과 같은 형식으로 다시 인코딩한다(JPEG q80, WebP 손실 q80). JPEG 는 Rust 도 q80 으로 다시 인코딩하고, PNG 는 무손실이라 차이가 없다. `image` 크레이트에는 손실 WebP 인코더가 없어서 WebP 는 다시 인코딩하지 않고 픽셀을 바로 해시한다. 판정 기준(≤6, 두 해시 중 최솟값)은 그대로다. 받아들일지 정해 달라.
3. **`check_blog` 인자가 `null` 일 때.** Tauri 의 `Option` 은 「키 없음」과 `null` 을 구분하지 못한다. 그래서 `targetType: null` 이 PoC 의 「타겟 종류를 확인해 주세요.」가 아니라 기본값 `'keyword'` 로 처리된다. `keyword` 가 아예 없으면 PoC 는 반환에서 키를 빼지만 Rust 는 `null` 을 낸다. 화면(`main.jsx:62`)은 늘 문자열을 보내므로 실사용 영향은 없다.
4. **엑셀의 작은 차이 셋.** (a) 빈 문자열 값: ExcelJS 는 빈 문자열 셀을 쓰고, Rust 는 서식만 있는 빈 셀을 쓴다. 읽으면 둘 다 빈 값이다. (b) 객체·배열 값은 ExcelJS 해석을 흉내 내지 않고 JS `String()` 결과를 텍스트로 쓴다. 화면이 보내는 행에는 이런 값이 없다. (c) `checkedAt` 은 RFC3339 문자열과 epoch 숫자만 해석하고 나머지는 JS 처럼 `Invalid Date` 로 쓴다. JS `Date` 는 더 많은 형식을 받는다. 한국 시각은 +9 고정이다.
5. **`map_concurrent` 의 `limit` 은 1 이상이어야 한다**(0 이면 assert). PoC 는 0 이면 undefined 배열을 돌려준다. 호출부는 늘 8 이다.
6. **SPEC 에 없어서 내가 정한 값** — 뒤집어도 비용이 작다.
   - 앱 창 크기 1400×900
   - 자리표시 아이콘(단색 `#5467F7`)
   - 로그: 파일 대상 하나(`sc-rank.log`, Info)
   - capabilities: 플러그인 기본 권한 네 개
   - 미구현 명령의 Err 문구 「아직 구현되지 않은 기능입니다.」(P3·P4 에서 없어진다)
7. **macOS 권한 대화상자가 떠 있다.** `tauri dev` 창을 확인할 때 System Events 로 창 제목·위치를 읽었는데, 그 뒤에 「'Orca'이(가) 다른 앱의 데이터에 접근하려고 합니다」 대화상자가 떴다. 누르지 않고 그대로 두었다. 사용자가 결정할 일이다.
8. **대기 중인 검증: 없음.** A-1·A-2·A-3·A-7 은 통과했다. A-4·A-5·A-8 은 P3·P4 몫이고 A-6·A-9 는 사용자 몫이다.
