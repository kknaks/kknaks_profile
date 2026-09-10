# 네이버 플레이스 순위 조회 PoC — 작업 의뢰

## 한 줄 목표

키워드(예: `강남역성형외과`)로 네이버 지도를 검색했을 때 **특정 병원(예: `무이성형외과`)이
플레이스 목록에서 몇 번째에 있는지**를 알려주는 PoC 를 만든다. 최종적으로는 매일 배치로
돌아가야 하지만, **이번 범위는 PoC 뿐**이다. 배치·스케줄러·DB 는 만들지 않는다.

## 참고 구조 (그대로 따라간다)

`reference/2026-09-09-sc-prototype/` 이 구조·코드 스타일의 기준이다. 그 프로토타입은
네이버 통합검색 **파워링크(광고)** 순위를 curl + cheerio 로 뽑는 것이고, 이번 건은 같은 틀에
**플레이스 순위 + Playwright** 를 얹는 것이다.

```text
package.json           "type":"module", scripts: dev / dev:backend / dev:frontend / start / build / test
server/index.mjs       express. POST /api/check, POST /api/export, single-flight 잠금(busy → 429), 127.0.0.1 바인딩
server/search.mjs      순수 파서(parseXxx) + 실행기(checkKeyword) 분리. 파서는 HTML/DOM 입력만 받아 테스트 가능하게
server/workbook.mjs    exceljs 로 xlsx. 한글 라벨(labels), 수식 문자열은 텍스트로, 시각은 Asia/Seoul
tests/*.test.mjs       node:test. 파서와 워크북만 테스트(네트워크 X)
src/main.jsx           React 19 + vite. 키워드 최대 50개 붙여넣기, 타겟 입력, 순차 조회, 상태 필터, xlsx 내려받기
scripts/dev.mjs        백·프론트 동시 기동
```

이번 건에서 바뀌는 점:

| 항목 | sc-prototype | 이번 PoC |
|---|---|---|
| 조회 대상 | 통합검색 파워링크 | 지도 플레이스 목록 |
| 타겟 | 도메인 | **병원명** (부분 일치, 공백 무시) |
| 수집 방식 | curl + cheerio | **Playwright(chromium headless)** |
| 결과 | 광고 순위 1개 | **전체 순위 + 광고 제외 순위 + 페이지** |

## 이미 검증된 사실 (다시 조사하지 말 것)

1. **정적 크롤은 전부 막혀 있다.**
   - `map.naver.com/p/search/...` HTML 은 2.3KB SPA 셸. 결과가 없다.
   - 내부 API `map.naver.com/p/api/search/allSearch` 는 200 이 오지만
     `metaInfo.pageId = "ncaptcha-all-search-no-result"`, `ncaptcha.confirmRules = "CE_EMPTY_TOKEN"` 으로 빈 응답.
   - 결과 iframe 주소 `pcmap.place.naver.com/hospital/list?query=...` 를 curl 로 치면 **HTTP 429**.
2. **Playwright headless chromium 으로는 된다.** 브라우저가 ncaptcha 토큰을 받아 결과가 뜬다.
   2026-09-09 실측: `강남역성형외과` → 5페이지 184건(광고 12건), `무이성형외과의원` 은
   **전체 10위 / 광고 제외 6위 / 1페이지**.
3. **동작하는 스크립트가 옆에 있다.** `pw_rank.mjs` 가 위 결과를 낸 그 코드다. 여기서 시작한다.

```bash
npm i playwright@1.63.0      # 크로미움은 ~/Library/Caches/ms-playwright 에 있으면 재사용, 없으면 npx playwright install chromium
node pw_rank.mjs 강남역성형외과 무이성형외과
```

### 스크립트가 이미 해결한 함정

- 결과는 `name="searchIframe"` 이고 url 에 `pcmap` 이 들어간 프레임 안에 있다.
  **프레임 객체를 캐시하면 stale 이 된다** → 매번 `page.frames().find(...)` 로 다시 찾는다.
- 목록은 lazy-load. 프레임 안 스크롤 컨테이너(overflow-y:auto 인 조상)를 바닥까지 반복 스크롤해야 한 페이지가 다 찬다.
- 페이지네이션은 하단의 텍스트가 숫자인 `a` 를 클릭. 새 항목이 0개면 종료.
- 각 `li` 의 첫 span 은 `의191210`, `이미지 수 6` 같은 잡값이다. 이름은 **span 중 `의원|병원|클리닉|외과` 로 끝나는 첫 항목**으로 잡는다.
- 광고 여부는 `li.innerText` 에 `광고` 가 있는지로 판정.
- 알려진 결함 1건: 상호가 `비티성형외과의원 강남성형외과` 처럼 두 span 으로 갈린 경우 `성형외과` 만 잡힌다. 파서 테스트에 케이스로 넣고 고칠 것.

## 만들 것

### 1. `server/place.mjs`
- `parsePlaceList(items, target)` — 순수 함수. `[{name, ad, reviews, addr, page}]` 배열을 받아
  `{status:'found'|'not_found', rank, organicRank, page, total, totalAds, matches, rows}` 를 돌려준다.
  타겟 비교는 공백 제거 후 부분 일치. 동명 다건이면 `matches` 에 전부, `rank` 는 첫 번째.
- `collectPlaceList(keyword, {maxPages=5})` — Playwright 실행. `pw_rank.mjs` 의 수집부를 옮긴다.
  브라우저는 **프로세스당 1개를 재사용**하고 컨텍스트만 조회마다 새로 만든다. 타임아웃 60s.
- `checkPlace(keyword, target)` — 둘을 잇고 sc-prototype 의 `checkKeyword` 처럼 `checkedAt`, `scope`,
  실패 시 `status:'error'` + 한국어 `message` 를 채운다.
  **결과를 못 읽은 것과 목록에 없는 것을 구분한다** — 프레임이 안 뜨거나 li 가 0개면 `error`, 다 읽었는데 없으면 `not_found`.
- `scope` 값: `'PC 네이버지도 플레이스 · 광고 포함 순위 / 광고 제외 순위'`.

### 2. `server/index.mjs`
- sc-prototype 그대로. `/api/check` body 는 `{keyword, target}`. 타겟은 1~50자.
- single-flight 잠금 유지. Playwright 는 무거우니 `nextAllowed` 간격은 2초.

### 3. `server/workbook.mjs`
- 컬럼: 키워드 / 상태 / 전체 순위 / 광고 제외 순위 / 페이지 / 확인 업체 수 / 광고 수 / 타겟 병원명 / 매칭 상호 / 조회 시각(한국) / 조회 기준 / 검색 URL / 안내.

### 4. `src/main.jsx`
- sc-prototype UI 를 그대로 쓰되 「타겟 사이트」 → 「타겟 병원명」, 결과 열에 전체/광고제외/페이지 추가.
- 상세 패널에 그 키워드의 전체 목록(순번·광고·상호·리뷰 수)을 보여준다. 순위가 왜 그렇게 나왔는지 눈으로 확인하는 용도.

### 5. `tests/place.test.mjs`
- 네트워크 없이 `parsePlaceList` 만. 최소 케이스:
  광고 사이에 낀 타겟의 전체/오가닉 순위 · 부분 일치(`무이성형외과` ↔ `무이성형외과의원`) · 공백 차이 ·
  동명 2건 · 미노출 · 빈 배열은 error 로 던짐 · 두 span 으로 갈린 상호 · xlsx 라벨/숫자/시각.
- 실제 Playwright 수집은 테스트하지 않는다. 대신 `npm run smoke` 스크립트 하나로
  `강남역성형외과 / 무이성형외과` 를 실물 조회해 `found` 가 나오는지 확인하고, 그 출력을 PR 본문에 붙인다.

## 하지 않을 것

- 배치·크론·DB·알림. PoC 가 검증되면 별도 건으로 발주한다. 다만 `checkPlace` 가
  **express 없이도 import 해서 쓸 수 있는 순수 모듈**이어야 배치에서 그대로 부를 수 있다.
- 캡차 우회, 프록시 회전, UA 랜덤화. 막히면 막혔다고 `error` 로 보고한다.
- 위치(geolocation) 고정. 결과에 「현재 위치에서 1.4km」 가 붙는 것처럼 순위는 위치에 따라 달라진다.
  PoC 는 헤드리스 기본 위치로 측정하고, 이 사실을 UI 안내문과 xlsx 「조회 기준」에 적는다.
  위치 고정이 필요한지는 사용자가 결정한다.
- 모바일 순위. PC 지도 기준만.

## 완료 조건

1. `npm test` 통과.
2. `npm run smoke` 로 `강남역성형외과 / 무이성형외과` 실물 조회가 `found` 로 나온다(순위 숫자는 달라도 됨).
3. `npm run dev` 에서 키워드 3개 넣고 조회 → xlsx 내려받기까지 손으로 1회.
4. README 에 위 「검증된 사실」과 「하지 않을 것」이 적혀 있다.

## 참고 파일

- `./pw_rank.mjs` — 동작 검증된 수집 스크립트
- `../2026-09-09-sc-prototype/` — 구조 기준
