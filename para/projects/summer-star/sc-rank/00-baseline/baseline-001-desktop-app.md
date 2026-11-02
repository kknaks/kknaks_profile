---
type: baseline
id: BASE-001
title: "웹 PoC 를 서버 없는 데스크톱 프로그램으로"
status: raw
product: sc-rank
source:
  type: conversation
  ref: "사용자 대화 2026-09-30 · reference/2026-09-09-sc-prototype"
links:
  baselines: []
  decisions:
    - "[[decision-001-desktop-app|DEC-001]]"
  specs: []
  works: []
  releases: []
  related: []
created_at: 2026-09-30
updated_at: 2026-09-30
tags:
  - product/sc-rank
  - doc/baseline
  - status/raw
---

# 웹 PoC 를 서버 없는 데스크톱 프로그램으로

> 아직 결정하지 않은 입력이다. 무엇을 정했는지는 DEC-001 이 갖는다.

## Raw

### 입력 1 — 사용자 원문 (2026-09-30)

> 이걸 웹 형식이 아니라 프로그램 형식으로 만들고 싶고 운영 환경은 윈도우야
> 내 생각에는 러스트로 짜면 맥/윈도우 다 가능 할거 같은데 어떻게 생각해
> 사실 이게 서버가 따로 필요한 형태는 아니라고 생각해서

> 응 타우리 러스트 로 할거야

> 이거 프로그램인데 서버 필요 없잖아 로컬에서 만 구동해서 엑셀로 저장 되면 되는거 아니야 ?

> sc-rank에 레포를 둘 필요가 잇어 ? 코드는 레퍼런스 프로토 타입에 아래에 만들자 일단

### 입력 2 — 웹 PoC 관측 (`reference/2026-09-09-sc-prototype`, 커밋 d6954f0)

**구성.** React 프론트(`src/`, 130줄) + Express 백엔드(`server/`, 약 490줄). 두 프로세스가
포트 13000·18000 에 뜬다. DB·이력 저장은 없고 결과는 `.xlsx` 로 내보낸다. 단일 로컬 사용자용.

**기능 셋.**

| 기능 | 엔드포인트 | 수집 방식 | 의존 |
|---|---|---|---|
| 파워링크 순위 | `POST /api/check` | `curl` 로 검색 HTML → Cheerio 파싱 | curl · cheerio |
| 플레이스 순위 | `POST /api/place/check` | Playwright Chromium, 최대 5페이지, lazy-load 스크롤(`place-dom.mjs` 는 페이지 안에서 도는 JS) | playwright |
| 블로그 노출 | `POST /api/blog/check` | Playwright 로 블로그 탭 렌더·스크롤, 제목·본문 키워드 일치 + 썸네일 이미지 DCT 해시 비교 | playwright · sharp |
| 엑셀 저장 | `POST /api/export` | 1~50행 → xlsx | exceljs |

**운영 규칙(PoC 가 이미 가진 것).** 동시 조회 1건. 요청 간격 파워링크·블로그 0.7초,
플레이스 2초. 판정은 `found`·`not_found`·조회 실패 셋. 입력 키워드 최대 50개.

**관측 사실.** 플레이스 스모크(`smoke-result.txt`)는 1페이지 약 3초, 2페이지 포함 약 7초.
Chromium 은 프로세스당 하나를 재사용하고 조회마다 컨텍스트를 닫는다.

### 입력 3 — 코디네이터 분석 (대화 중 제안, 사용자 동의)

- 서버가 필요 없다: 사용자 1명 · DB 없음 · 결과는 파일. Express 는 화면과 수집 코드를 잇는
  역할뿐이고 Tauri `invoke` 로 대체된다.
- 브라우저 자동화가 가장 큰 위험이다. Rust 에는 Playwright 급 라이브러리가 없다.
  Windows 10/11 에는 Edge 가 기본 설치되어 있으므로 시스템 브라우저를 CDP 로 조종하면
  Chromium 동봉이 필요 없다.
- 대응표: curl+cheerio → reqwest+scraper · exceljs → rust_xlsxwriter · sharp → image ·
  playwright → chromiumoxide(CDP).
- 대안: Tauri + Node 사이드카(배포가 지저분), Electron(무겁지만 이식 쉬움 — 포팅이 막힐 때의 후보).
