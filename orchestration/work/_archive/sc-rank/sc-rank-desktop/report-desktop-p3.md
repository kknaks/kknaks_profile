# WORK-001 P3 결과 보고

## 상태: done — 단, 사용자 확인 사항(헤드리스 Edge 결과가 PoC 와 같은가)은 **「같다고 확인되지 않음」**. 아래 §사용자 확인 사항

P3 만 했다(화면 `src/` 무변경 — `diff -rq` 동일). 커밋·push·PR 없음. 변경은 `reference/2026-09-09-sc-prototype/desktop/` 안뿐.

## 사용자 확인 사항 — 헤드리스 Edge 로 네이버가 PoC 와 같은 결과를 주는가

**블로그는 정상 동작을 확인했다. 플레이스는 목록이 PoC 기록과 달랐다 — 광고가 0건이었다.** 원인은 이번 판에서 가르지 못했다.

| | PoC 기록 (`smoke-result.txt`, Playwright Chromium · Mac Chrome/128 UA, 2026-09-09 무렵) | 이번 smoke (헤드리스 Edge 154 · Edge 실제 UA, 2026-09-30) |
|---|---|---|
| 플레이스 강남역성형외과 → 무이성형외과 | found · 전체 43 / 광고 제외 31 · 1페이지 · 확인 88 · **광고 18** · captured 89 · loadedGroups 30 | found · 전체 53 / 광고 제외 53 · 1페이지 · 확인 70 · **광고 0** · captured 73 · loadedGroups 24 |
| 블로그 키워드 구월동레이저제모 → 썸블리의원 | (기록 없음) | found · 43위 · 1회 스크롤 · 60건 |
| 블로그 이미지 구월동피부과 → 1.png | (기록 없음) | not_found · 3회 스크롤 · 120건 · 썸네일 160개 전부 비교(다운로드 실패 0) |

- **플레이스 광고 0건이 눈에 띈다.** 광고 판정은 PoC 페이지 JS(`/광고/.test(li.innerText)`)를 문자열 그대로 주입했으니 판정 코드 차이는 아니다. 네이버가 이 요청에 광고 표시를 안 줬다는 뜻이다. 후보 원인은 셋인데 이번 판에서 가르지 못했다: (a) UA — Edge 실제 UA(`Edg/154`)로 바꾼 것(SPEC §3 의 의도된 변경) (b) 헤드리스 Edge 판별 (c) 3주 사이 광고 편성 변화. 광고가 빠지면 전체 순위(광고 포함)가 달라지고 광고 제외 순위만 비교 가능해진다.
- 결과 항목 `id` 가 전부 `null` 이다(PoC 기록은 `id` 를 출력하지 않아 비교 불가). 판정에는 쓰지 않는 값이다.
- **가르려면 같은 시각 비교 1회가 필요하다**: PoC `npm run smoke`(Playwright Chromium)와 이 smoke 를 연달아. 네이버 요청이 늘어나는 일이라 코디·사용자 결정으로 남긴다. 실수집 반복 금지 규칙 때문에 나는 재실행하지 않았다(재시도는 「실패 원인 확인용」만 허용인데 결과는 오류가 아니었다).

## 수행 — 파일·모듈 목록 (`desktop/` 기준)

| 파일 | 내용 |
|---|---|
| `src-tauri/Cargo.toml`·`Cargo.lock` | + `chromiumoxide 0.9`(CDP, fetcher 끔 — Chromium 다운로드 없음) · `reqwest 0.13`(rustls·gzip·brotli·deflate) · `serde_json/preserve_order`(로그 필드 순서를 PoC 와 같게). `openssl-sys` 없음(`cargo tree -i` 확인) |
| `src-tauri/js/place-dom.js` | PoC `place-dom.mjs` **바이트 동일 사본**. 주입할 때 `export ` 만 뗀다 |
| `src-tauri/js/place-items.js`·`place-signature.js`·`place-next.js` | `place.mjs:74-80`·`:94`·`:95-99` 함수 본문 원문 |
| `src-tauri/js/blog-scroll.js`·`blog-rendered.js` | `blog-browser.mjs:25`·`:35-42` 함수 본문 원문 |
| `src-tauri/src/browser.rs` | (P2 탐색 +) `BrowserManager`: 기동·재사용·끊기면 재기동·종료 정리 · `Context`: 격리 컨텍스트, `goto`(domcontentloaded), 프레임 실행 맥락 평가, `content()`, attached 대기 · 페이지 JS 예외 → 한글이면 도메인 오류 · `remove_stale_profiles()` |
| `src-tauri/src/place.rs` | + `collect_place_list`(`collectPlaceList` 본문 전체) · `check_place` |
| `src-tauri/src/blog_browser.rs` | 새 파일 — `blogBatches` (PoC 파일 구분을 따랐다) |
| `src-tauri/src/blog.rs` | + `download_thumbnail`(curl 대응) · `check_blog`(`checkBlog` 루프·로그) |
| `src-tauri/src/gate.rs` | 새 파일 — 공유 잠금·간격(블로그 0.7초/플레이스 2초, 끝난 시점부터, 오류여도 갱신) |
| `src-tauri/src/commands.rs` | `check_blog`·`check_place` 실제 연결. `check_place` 는 입력 검증 Err → 잠금 순. `export_xlsx` 는 P4 까지 미구현 Err |
| `src-tauri/src/lib.rs` | 기동 때 잔여 프로필 정리 · `AppState` 등록 · `RunEvent::Exit` 에서 브라우저 종료·프로필 삭제 |
| `src-tauri/examples/smoke.rs` | `place <키워드> <타겟>` · `blog <키워드> keyword <타겟>` · `blog <키워드> image <파일>` — 로그는 stdout, 요약 JSON(플레이스는 `rows` 제외, `smoke.mjs` 와 같게), `status=="error"` 면 exit 1, 끝나면 `shutdown` |
| `src-tauri/tests/collect_offline.rs` | 주입 JS 가 PoC 원문과 같은지 · 브라우저 없음 → 조회 행 오류(§3 문구) · 블로그 입력 검증은 브라우저 앞 |

## 검증 — 명령과 수치

| 명령 | 결과 |
|---|---|
| `cargo test` | **37 passed / 0 failed** (P2 33 + gate 1 + collect_offline 3) |
| `cargo clippy --all-targets -- -D warnings` | 경고 0 |
| `npm run build` | 성공 |
| 스파이크 (임시 예제, 끝나고 삭제) | 지도: `searchIframe`(`pcmap.place.naver.com`) 실행 맥락에서 목록 읽기 **됨**. 블로그: `s.search.naver.com/p/review/` 응답 본문 받기 **됨** — 단 첫 매칭이 CORS 사전 요청(OPTIONS 204, 본문 없음)이었다. Playwright 의 response 이벤트에는 사전 요청이 없으므로 `ResourceType::Preflight` 를 거르는 것으로 맞췄다(우회로가 아니라 Playwright 의미를 옮긴 것). 네이버 요청: 지도 1 + 블로그 2(원인 확인 재시도 1) |
| smoke 3회 (각 1회, 사이 3초) | 아래 원문. 셋 다 exit 0 |
| A-8 예제 쪽 | smoke 뒤 `pgrep -f sc-rank-cdp-` **없음** · `$TMPDIR/sc-rank-cdp-*` **없음**. 스파이크 1차가 패닉으로 남긴 프로필 1개는 다음 smoke 기동의 잔여 정리로 지워졌다(SPEC §3 「다음 기동 때 지운다」 경로 실측) |

### smoke 원문 — `cargo run --example smoke -- place 강남역성형외과 무이성형외과`
```
[place] {"keyword":"강남역성형외과","stage":"start","elapsedMs":0,"maxPages":5}
[browser] {"stage":"launched","executable":"/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge"}
[place] {"keyword":"강남역성형외과","stage":"browser-ready","elapsedMs":1397}
[place] {"keyword":"강남역성형외과","stage":"navigation-ready","elapsedMs":2262}
[place] {"keyword":"강남역성형외과","stage":"list-ready","elapsedMs":4639}
[place] {"keyword":"강남역성형외과","stage":"page-start","elapsedMs":4639,"page":1}
[place] {"keyword":"강남역성형외과","stage":"scroll-complete","elapsedMs":6058,"page":1,"loadedGroups":24,"atBottom":true,"captured":73}
[place] {"keyword":"강남역성형외과","stage":"page-complete","elapsedMs":6061,"page":1,"added":70,"total":70}
[place] {"keyword":"강남역성형외과","stage":"target-found","elapsedMs":6061,"page":1}
[place] {"keyword":"강남역성형외과","stage":"complete","elapsedMs":6061,"total":70}
[browser] {"stage":"closed","profileRemoved":true}
{
  "keyword": "강남역성형외과",
  "target": "무이성형외과",
  "searchUrl": "https://map.naver.com/p/search/%EA%B0%95%EB%82%A8%EC%97%AD%EC%84%B1%ED%98%95%EC%99%B8%EA%B3%BC?searchType=place",
  "scope": "PC 네이버지도 플레이스 · 광고 포함 / 광고 제외 · 페이지 전체 수집 후 타겟 확인(최대 5페이지) · 헤드리스 기본 위치(위치 고정 없음)",
  "checkedAt": "2026-09-30T08:56:09.870Z",
  "status": "found",
  "rank": 53,
  "organicRank": 53,
  "page": 1,
  "total": 70,
  "totalAds": 0,
  "matches": [
    {
      "name": "무이성형외과의원",
      "id": null,
      "ad": false,
      "reviews": "495",
      "addr": "서울 강남구 역삼동",
      "rank": 53,
      "organicRank": 53,
      "page": 1
    }
  ],
  "message": ""
}
exit=0
```

### smoke 원문 — `cargo run --example smoke -- blog 구월동레이저제모 keyword 썸블리의원`
```
[browser] {"stage":"launched","executable":"/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge"}
[blog] {"keyword":"구월동레이저제모","stage":"batch","scrolls":0,"total":30}
[blog] {"keyword":"구월동레이저제모","stage":"batch","scrolls":1,"total":60}
[blog] {"keyword":"구월동레이저제모","stage":"complete","elapsedMs":2572,"rank":43,"total":60,"scrolls":1}
[browser] {"stage":"closed","profileRemoved":true}
{
  "keyword": "구월동레이저제모",
  "target": "썸블리의원",
  "targetType": "keyword",
  "searchUrl": "https://search.naver.com/search.naver?ssc=tab.blog.all&sm=tab_hty.top&query=%EA%B5%AC%EC%9B%94%EB%8F%99%EB%A0%88%EC%9D%B4%EC%A0%80%EC%A0%9C%EB%AA%A8",
  "scope": "PC 네이버 블로그 탭 · 초기 목록 + 최대 3회 스크롤 · 제목·요약 키워드 일치",
  "status": "found",
  "rank": 43,
  "matches": [
    {
      "rank": 43,
      "title": "구월동피부과 썸블리의원 위치와 예약 정보",
      "url": "https://blog.naver.com/nhdotk/224410349268",
      "snippet": "피부 시술 상담 전, 위치와 예약 동선을 먼저 보고 싶은 분이라면 인천 구월동피부과 썸블리의원 정보를 살펴볼 만해요. 필러, 보톡스, 리프팅 계열 시술과 레이저 제모 관련 안내가 있는 의원이에요. 상담 내용에 맞춰 시술을 알아보는 경우라면 예약 여부와 주차 위치를 함께 보는 편이 편해요. 독립된 룸 운영과 여성 대표원장 직접 시술 안내도 확인할 수 있어요....",
      "blogger": "세상읽기노트",
      "thumbnailUrls": [
        "https://search.pstatic.net/common/?src=http%3A%2F%2Fblogfiles.naver.net%2FMjAyNjA5MTNfMjU4%2FMDAxNzg5Mjk1MzMzMTI3.ibpkoxRNqaLIF6M_PP_hWj8RI0sqgxRDRpPXC7mvFY0g.jSlxkh0XF1qqPoSZLRiSaKCABcHncpC7tAZnupDQGdQg.JPEG%2Fnaver-d35f1b7d3c0821be2762.jpg%235450x3633&type=ff192_192"
      ]
    }
  ],
  "total": 60,
  "scrolls": 1,
  "checkedAt": "2026-09-30T08:56:29.459Z",
  "message": ""
}
exit=0
```

### smoke 원문 — `cargo run --example smoke -- blog 구월동피부과 image tests/fixtures/1.png` (썸네일 URL 줄만 생략)
```
[browser] {"stage":"launched","executable":"/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge"}
[blog] {"keyword":"구월동피부과","stage":"batch","scrolls":0,"total":30}
[blog] {"keyword":"구월동피부과","stage":"images-start","images":70,"concurrency":8}
[blog] {"keyword":"구월동피부과","stage":"batch","scrolls":1,"total":60}
[blog] {"keyword":"구월동피부과","stage":"images-start","images":30,"concurrency":8}
[blog] {"keyword":"구월동피부과","stage":"batch","scrolls":2,"total":90}
[blog] {"keyword":"구월동피부과","stage":"images-start","images":30,"concurrency":8}
[blog] {"keyword":"구월동피부과","stage":"batch","scrolls":3,"total":120}
[blog] {"keyword":"구월동피부과","stage":"images-start","images":30,"concurrency":8}
[blog] {"keyword":"구월동피부과","stage":"complete","elapsedMs":8599,"rank":null,"total":120,"scrolls":3}
[browser] {"stage":"closed","profileRemoved":true}
{
  "keyword": "구월동피부과",
  "target": "1.png",
  "targetType": "image",
  "searchUrl": "https://search.naver.com/search.naver?ssc=tab.blog.all&sm=tab_hty.top&query=%EA%B5%AC%EC%9B%94%EB%8F%99%ED%94%BC%EB%B6%80%EA%B3%BC",
  "scope": "PC 네이버 블로그 탭 · 초기 목록 + 최대 3회 스크롤 · 검색 썸네일 pHash(거리 6 이하)",
  "status": "not_found",
  "rank": null,
  "matches": [],
  "total": 120,
  "comparedImages": 160,
  "scrolls": 3,
  "checkedAt": "2026-09-30T08:56:48.894Z",
  "message": "이번 블로그 탭 초기 목록 + 최대 3회 스크롤에서 찾지 못했습니다."
}
exit=0
```

## PoC 대조 — SPEC-001 §3

| 항목 | 판정 |
|---|---|
| 탐색 Edge → Chrome · 표준 경로 · 없으면 §3 문구 | 같음 (이 Mac 에서 Edge 로 기동 확인, 빈 후보 테스트) |
| CDP · Chromium 동봉 없음 | 같음 — 설치된 Edge 실행 파일을 띄운다. chromiumoxide `fetcher` 기능 끔 |
| 헤드리스 · 전용 임시 프로필 `sc-rank-cdp-<pid>-<nanos>` | 같음 (`--headless=new`) |
| CDP 는 127.0.0.1 임의 포트 | 같음 (`--remote-debugging-port=0`, 기본 바인딩 127.0.0.1) |
| 앱당 1개 공유·재사용 · 끊기면 다음 조회에서 재기동 | 같음 — CDP 연결 종료 또는 프로세스 종료를 보고 재기동 |
| 조회마다 격리 컨텍스트, 끝나면 닫음 · ko-KR · 1400×900 | 같음 — 스파이크에서 `navigator.language=ko-KR`, `1400x900` 확인 |
| UA = 실제 UA 에서 `HeadlessChrome`→`Chrome` | 같음 — 실측 `…Chrome/154.0.0.0 Safari/537.36 Edg/154.0.0.0`. 썸네일 HTTP UA 는 PoC 문자열 그대로 |
| 종료: 브라우저 끝내고 프로필 삭제 · 잔여 `sc-rank-cdp-*` 는 다음 기동 때 삭제 | 같음 — 예제 쪽 실측. 앱 창 닫기(A-8)는 P4 |

## PoC 대조 — SPEC-001 §4 수집 행

| 영역 | 항목 | 판정 |
|---|---|---|
| 플레이스 수집 | goto 30초(domcontentloaded) · 첫 항목 20초 · 전체 60초(문구 그대로) | 같음 |
| | 기본 8초 | 같음(해당 없음) — PoC 에서 `setDefaultTimeout(8000)` 이 걸리는 호출이 없다(evaluate 류는 타임아웃 없음) |
| | 프레임 판정 `name()==='searchIframe' && url.includes('pcmap')` · 문구 | 같음. 첫 항목 대기는 `searchIframe` 이름의 프레임 안에서 셀렉터가 붙을 때까지 100ms 폴링(Playwright `frameLocator…waitFor` 대응) |
| | 셀렉터 · 항목 정규식 4종 · 상호 없음 처리 · `added==0` 처리 | 같음 — 페이지 JS 는 원문 주입, 루프는 Rust 로 같은 순서 |
| | 다음 번호 **마지막** 요소 클릭, 없으면 조용히 종료 · 페이지 변화 대기 | 같음 (원문 주입) |
| | `[place]` 단계 로그 필드 | 같음 — 필드 순서까지. 추가로 `[browser]` 기동·종료 한 줄 |
| 블로그 수집 | goto 25초 · 첫 카드 12초 · 150초 | 같음. 150초는 PoC 처럼 **컨텍스트 조작에만** 걸린다(썸네일 비교 시간은 제외) |
| | 응답 대기를 스크롤 **전에** 등록 · 대기 12초(PoC 기본 타임아웃) | 같음 |
| | 응답 판정 4갈래 · 렌더 조건 `headline 카드 ≥ before+added` · `payload.url` 없으면 종료 | 같음 (렌더 대기는 원문 주입) |
| | 응답 매칭에서 CORS 사전 요청 제외 | 같음(Playwright 의미) — 위 스파이크 |
| 블로그 판정 | 썸네일 8초 · 6MB · 비 2xx 실패 · 리다이렉트 안 따라감 · PoC UA · 동시 8 · 캐시 · found 면 중단 | 같음 — curl 대신 reqwest. `--compressed` 대응으로 gzip·br·deflate |
| | `[blog]` 로그 4종(batch·images-start·complete·error, message 200자) | 같음 |
| 오류 문구 | 페이지 JS 예외: 한글이면 문구 그대로, 아니면 폴백 | **다름(작음)** — PoC 는 Playwright 가 붙인 `frame.evaluate: Error: ` 접두까지 화면에 냈다. 여기서는 한글 문구만 낸다(SPEC §4 「문구 그대로」에 맞춤) |
| 공유 잠금·간격 | 블로그 0.7초 / 플레이스 2초, 끝난 시점부터 · 문구 · 플레이스 검증이 잠금 앞 | 같음 (단위 테스트) |

## 이슈 · 코디가 확인할 것

1. **플레이스 광고 0건** — 위 「사용자 확인 사항」. 같은 시각 PoC 대조 1회를 할지 결정해 달라. 광고가 계속 0 이면 전체 순위 의미가 PoC 와 달라진다.
2. **Playwright CSS 는 열린 shadow DOM 을 뚫고, 여기 `querySelectorAll` 은 뚫지 않는다.** 스파이크와 smoke 에서 목록·카드는 정상적으로 읽혔다.
3. **`onPage` 디버그 훅**(`place.mjs:82`)은 옮기지 않았다. `checkPlace` 가 넘기지 않는 인자다.
4. **브라우저 기동 제한 180초** — Playwright `launch` 기본값에 맞췄다. 화면 180초 상한과 겹친다(P4).
5. **Windows 빌드 주의** — `reqwest` 의 rustls 는 aws-lc-rs 를 쓴다. Windows 에서 C 빌드 도구가 필요할 수 있다(P5 README 에서 확인).
6. **대기 중(pending):** A-8 앱 창 닫기(P4) · A-6·A-9(사용자).
