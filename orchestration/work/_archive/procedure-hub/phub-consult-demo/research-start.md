# phub-consult-demo 착수 조사 — 상담 화면 · 명동점 상품 · 시술 그림: 있는 것 / 없는 것

조사일 2026-11-19 · researcher(read-only) · 기준: 허브 `PROCEDURE-HUB/phub-consult-demo`(aa46a86 = release/v1.2.0) · 앱 `clinic_chat/phub-consult-demo`(97d964e = main) · 로컬 PG 76+ 표(SELECT 만) · stg GET 만 · 18222 화면 GET 만(헤드리스 스크린숏 1장).

경로 약어: `H` = `/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-consult-demo` · `C` = `/Users/kknaks/orca/workspaces/clinic_chat/phub-consult-demo` · `CC` = `$C/clinic_chat/consult` · `A` = `orchestration/work/_archive/procedure-hub/phub-gold-jev`(프로필 레포).

## 한눈 표

| | 있음 | 없음 | 정할 것 |
|---|---|---|---|
| **1. 상담 화면(GUI)** | 네 칸(드로어 · 얼굴+리스트 · 채팅 · 객체 패널) · htmx SSR + SSE 7 이벤트 · 벤더링 medikit(고치지 않음) + 앱 CSS 169줄(토큰 `--cs-*`) · 가짜 턴 · 헤드리스 Chrome 스크린숏 가능(실측) | **화면 문구 거의 전부** — `data-slot` 18 종 중 값 있는 것 1(`mark-modality-level`) · 좁은 화면용 `@media` 0 · 그림 자리 0 | 사용자가 화면 보며 말할 불편 목록 · 빈 문구(제목 · 「새 대화」 · 입력 안내 · 표지 · 오류) 값 |
| **2. 명동점 상품** | 허브 silver/gold 에 **시장 참고 가격** 상품(`s_offer` 122 · `g_offer` 163 · 가격표 1 = 「한국 시장 참고 가격」) · 「메뉴」 = `s_package.kind` 57 · 도구 `facets offer/package` · 앱은 상품을 리스트에 안 그림 · 명동점 KOS 원자료 스냅샷이 **다른 레포**에 있음(phub-recommend 조사가 씀) | 허브 · 앱 어디에도 **지점 · 병원 · 이벤트 · 할인 칸 0** · 명동점 상품 데이터 0(허브 · 앱 레포) | 받을 데이터 꼴 전부(§정할 것 U-2x) — 추측 안 함 |
| **3. 시술 그림** | 원천 SVG 103(6.89MB) · silver/DB 2표(103 · 787 실측) · 적재기 V13(`GOLD_IMAGE_DIR` = **적재기만**) · SPEC-007 §9 「다음 스펙이 읽을 자리」 N7-1~7 | 허브 서빙 코드 0 · 도구 응답 그림 칸 0(stg OpenAPI 실측) · 이미지 안 `assets/` 0 · 서빙 컨테이너 마운트 0 · 앱 그림 자리 0(마크다운 image 꺼짐) | 새 도구 꼴 · aux 승격 · 서빙 길(마운트 vs 이미지) · 화면 자리 · 인라인 vs `<img>` |

---

## Q1. 상담 화면 지도(GUI)

### 1-1. 화면 구성 요소 전수

라우트(전부 `$CC/server.py`): `GET /` → 303 새 대화(:134-138) · `GET /c/{id}`(전체 · `HX-Request` 면 `partials/main.html` 조각 :140-142 · `render.py:62`) · `POST /c/{id}/turns`(:144-166 → `partials/turn.html` 조각) · `GET /c/{id}/turns/{n}/events`(SSE :168-174) · `GET /convs`(드로어 목록 조각 :176-179) · `GET /c/{id}/list?concern=`(점 · 라벨 누르기 → 리스트 조각 :181-202) · `GET /face-check`(좌표 확인 :204-206) · `/static` 마운트(:208).

| 요소 | 템플릿 | CSS(`$CC/static/consult.css`) | JS(`$CC/static/consult.js`) | 서버 · SSE |
|---|---|---|---|---|
| 셸 · 머리 | `templates/base.html:1-20`(medikit.css → consult.css → htmx · sse · medikit.js · consult.js) · `page.html` → `partials/main.html:3-45`(`main#consult.cs-app`) | `.cs-app` 그리드 :31-36 · 패널 판 :134-136 | — | `render.page` `render.py:59-65` |
| 왼쪽 드로어(지난 대화) | `partials/drawer.html:3-15` · 목록 `partials/drawer_list.html:3-14`(항목 = `first_question` · 시각 `last_asked_at[5:16]`) | `.cs-drawer*` :133-160 · 말줄임 `.cs-drawer__q` :149 | 접기 :101-108 · 턴 끝나면 목록 다시 받기 `refreshDrawer` :84-90 | `GET /convs` · 색인 `drawer.py:34-101`(서버 뜰 때 장부 한 번 훑음) |
| 얼굴 패널 | `main.html:6-12` · 선 그림 `templates/_face.svg`(48KB) · 점 층 `partials/sites.html:7-24`(점 `circle.cs-dot` · 얼굴 아래 라벨 칩) | :42-50 · `.cs-dot` :47 · 누름 :167 | 점 · 라벨 누르기 `pick` :110-129(aria-pressed · 숨은 칸 `viewing`) | SSE `sites` → `#face-marks` 통째(`turn.html:13` · `turn.py:164,176`) · 좌표 `face_coords.py` · `sites.py` |
| 시술 리스트 패널 | `main.html:13-16` → `partials/list.html:5-58`(0.1/0.2 꼴) · 고민 묶음 0.3 `partials/list_v3.html:5-39` · 관심 `list_interest.html` · 시너지 `list_synergy.html` | :52-64 · :117-131 · :164-165 | — | SSE `list` → `#procedure-list` outerHTML(`turn.html:12` · `turn.py:171,583`) · 누르기 `GET /c/{id}/list` |
| 채팅 로그 · 턴 | `main.html:18-30` · `partials/turn.html:4-24`(손님 말풍선 · 답 · 도는 턴만 `sse-connect`) · `answer.html` · `delta.html` · 단계 `steps.html` · 오류 `error.html` · 거절 `rejected.html` | :65-106 | 끝으로 스크롤 :20-24, :145-146 | SSE `step`(`turn.py:101`) · `delta`(:113) · `done`(:204) · `turn_error`(:202 · `server.py:122`) · 닫기 `close`(`live.py:13`) |
| 입력 | `main.html:31-40`(textarea · 보내기 버튼 · 숨은 `viewing`) | `.cs-form*` :107-116 | Enter 전송 · Shift+Enter · 보내는 중 잠금 :46-80 | `POST /c/{id}/turns` |
| 낡은 대화 띠 | `main.html:20-25`(`outdated` · `off_closed`) | `.cs-outdated` | — | `server.py:100-107` |
| 객체 패널(디버그) | `partials/state.html:3-11` · `state_turn.html:3-13` | `.cs-state*` · `--cs-panel-w` 360px | 새 묶음 위에 붙으면 앞 묶음 접기 :131-137 | `CHAT_DEBUG_PANEL=on`(`config.py:90`) · SSE `state`(`turn.py:198` · `turn.html:14-16`) · `render.state_view` :26-42 |
| 그 밖 | 진행 막대 `#ms-progress`(`base.html:17` · medikit.js) · 좌표 확인 화면 `face_check.html` | `.cs-check` :51 | — | `GET /face-check` |

「드로어」는 이 앱에서 **지난 대화 목록**뿐이다(시술 상세 드로어 같은 것은 없다).

### 1-2. 화면 문구의 출처

- 템플릿은 「문구 0 · `data-slot` 빈 자리」 규칙이다(`render.py:1` · `page.html:3` · `drawer.html:2`). 빈 자리 값은 `prompts/consult.json` 의 `slots{}` 에서만 오며(`render.py:52` · `prompt.py:203-208`), **지금 값은 하나** — `mark-modality-level` = 「{name} 계열 시술」.
- 18222 실물 페이지(`/c/a578141fc2d24a1d`)의 `data-slot` 18 종 가운데 글이 찬 것은 `mark-modality-level` 3 개뿐이다. 나머지(`page-title` · `face-title` · `list-title` · `chat-title` · `drawer-new-label` · `drawer-toggle-label` · `drawer-list-title` · `input-placeholder` · `send-label` · `list-section-interest` · `list-section-synergy` · `list-synergy-outside` · `mark-interest` · `mark-guess` · …)는 빈칸. 템플릿에만 있는 빈 자리도 같다(`list-empty` · `face-empty` · `label-area-title` · `list-section-modality-only` · `list-section-unreached` · `mark-caution` · `mark-site-prefer` · `state-title` · `state-empty` · `conv-outdated` · `conv-off-closed` · `error-*` · `turn-limit` · `error-new-conversation`).
- 문구가 실제로 나오는 곳: 단계 줄 = `consult.json` `steps`(4 — 이해 · 찾기 · 목록 · 답변 · `steps.html:6`) · 답 본문 = LLM(마크다운 · `render.py:19-23`) · 리스트 · 라벨 · 드로어 = 허브 값 · 손님 첫 질문. 앱 코드 · CSS 에 박힌 한글 문구는 찾지 못했다(`consult.css` 의 `content:` 는 빈 문자열 1 곳 :97).
- `consult.json` 의 그 밖 문구 키(`kind_labels` 15 · `turn_headers` · `voice_check` 23 · `pick`)는 LLM 재료 · 장부용이다(화면 글 아님 — `kind_labels.offered` 는 답 재료 `material.py:255`).

### 1-3. 스타일 체계

| 층 | 파일 | 출처 · 규칙 |
|---|---|---|
| 벤더링(고치지 않음) | `static/medikit.css` · `medikit.js` | CENTURION_DAY `backend/day/static/`(dev · c5045a99) 사본 · medikit 1.3.0 값 · `MEDIKIT-NOTICE.txt`. sha256 앞자리 지금 = 37ee05c8 · bf63fd24 — NOTICE 값과 **같다**(고쳐지지 않음 확인) |
| 벤더링 | `htmx.min.js`(2.0.4) · `htmx-ext-sse.js`(2.2.4) · 라이선스 파일 | — |
| 앱 자체 | `static/consult.css`(169줄) | 머리 주석 「치수는 :root 토큰 블록에만 · medikit.css 는 고치지 않는다」(:2) · 토큰 `--cs-*` 16 개(:11-26 — 드로어 240px · 왼쪽 420px · 얼굴 46vh · 패널 360px …) · 색은 `--ms-*` 토큰만(:117 · :133 주석 「새 색 0」) |
| 폰트 | `static/PretendardVariable.woff2`(2.06MB) · `PRETENDARD-LICENSE.txt` | `@font-face` 는 `consult.css:4-6` · medikit 의 `--ms-font` 가 「Pretendard」 를 첫째로 부름 |
| 부품 매크로 | `templates/ui.html` | DAY `ui.html` 꼴 — `ms-*` 클래스만 |

### 1-4. 눈에 띄는 이상

**mojibake(왼쪽 목록 맨 아래 줄) — 원인 자리**

- 화면 데이터: 18222 `GET /convs` 의 마지막 항목(11-17 18:48) `first_question` 이 깨진 글자다(스크린숏 확인).
- 원천: 장부 `$C/runs/consult/turns.jsonl` **21행 · 24행**(대화 `c1b7b741c58a4676` · 턴 1 · `asked_at` 2026-11-17T18:48:33) — `question` 값 자체가 UTF-8 바이트를 latin-1 로 읽은 글자로 저장돼 있다(latin-1 로 되돌려 UTF-8 로 읽으면 정상 한국어 문장 — 「팔자주름…」 꼴). 장부의 깨진 행은 이 대화 하나(시작 · 맺는 줄 2 행)뿐이다(전수 훑음).
- 깨진 자리: 앱 화면 · 템플릿이 아니라 **폼 본문 해석**. Starlette 1.10.0 `FormParser` 는 urlencoded 본문을 `unquote_plus(value.decode("latin-1"))` 로 읽는다(`$C/.venv/.../starlette/formparsers.py:114-115`). 브라우저는 한글을 `%XX` 로 보내 문제없고, **퍼센트 인코딩 없이 날 UTF-8 바이트를 보낸 비브라우저 클라이언트**(예: curl `-d` 날 글자)의 요청이면 이렇게 저장된다. 그 시각에 누가 무엇으로 보냈는지는 **확인 안 됨**(바로 앞뒤 18:47:59 · 18:48:40 행은 정상).
- 그리기: `drawer_list.html:7` 이 장부 값을 그대로 낸다(자동 이스케이프만) — 템플릿 · CSS 쪽 원인 아님.

**그 밖 — 사람 눈에 이상해 보일 자리**(스크린숏 `/c/a578141fc2d24a1d` 1600×1000 기준 + 코드)

| # | 자리 | 무엇이 보이나 | 근거 |
|---|---|---|---|
| E1 | 드로어 위 「새 대화」 버튼 | 글 없는 빈 테두리 상자 | `drawer.html:9` `data-slot="drawer-new-label"` 빈칸 |
| E2 | 얼굴 · 리스트 카드 머리 | 빈 제목 줄(위 여백만) — 채팅 카드만 `:has(> :empty)` 로 숨김 | `main.html:7,14` · `consult.css:66`(채팅 머리만) |
| E3 | 입력창 | 안내 글 없음 · 보내기 버튼 화면 읽기 글 없음 | `main.html:34,36` |
| E4 | 리스트 표지 | 관심 · 추정 · 주의 · 부위 표지가 **글 없는 점/점선 원**만(예: 「실리프팅」 옆 점선 원 = `mark-guess`) | `list_v3.html:19-21` · `list_interest.html:9` · `consult.css:128-131` |
| E5 | 리스트 섞임 | 「관심 대상」 묶음 · 고민 묶음 · 계열 묶음 머리(「기기 리프팅」 — 밑줄+점 = `mark-modality-level` 의 정해진 값과 별개) · 배지(「HIFU」)가 머리 글 없이 한 목록에 이어짐 — 묶음 경계가 안 보임 | `list.html:9-11` 머리 `data-slot` 빈칸 · 스크린숏 |
| E6 | 브라우저 탭 제목 | 비어 있음 | `base.html:8` |
| E7 | 좁은 화면 | 그리드가 240+420+1fr(패널 켜면 +360) 고정 · 너비 `@media` 0 → 1,000px 안쪽에서 가로 넘침 예상(실측 안 함) | `consult.css:33` · `@media` 는 줄임 동작 :95 하나뿐 |
| E8 | 끝난 턴의 단계 줄 | 되읽은 대화에서는 단계 줄이 없다(도는 턴만 SSE 로 받음) — 라이브와 새로 고침 뒤가 다르게 보임 | `turn.html:6-23` |
| E9 | 지금 18222 에서 새 턴 | 앱 기본 허브 주소가 로컬 18105 인데 18105 에 LISTEN 이 없다 → 새 질문 · 점 누르기(메모 없을 때)는 허브 오류 조각이 날 것으로 **예상**(보내 보지 않음 — 확인 안 됨) | `config.py:41-42` · `lsof` 18105 없음 · `.env` 에 허브 주소 키 없음 |
| E10 | 가짜 턴 리스트 꼴 | `CHAT_FAKE_TURN` 의 리스트가 0.1 꼴(`hidden` 없음)이라 지금 화면이 쓰는 0.3 꼴(`list_v3.html`)을 재현하지 못한다 | `fake_turn.py:15-27` · `list.html:13` |

### 1-5. 화면을 띄우고 대화를 재생하는 길

| 길 | 어떻게 | 외부 호출 | 근거 · 한계 |
|---|---|---|---|
| 옛 대화 열기 | `GET /c/<conv_id>` — 장부를 되읽어 턴 · 마지막 리스트 · 점을 그린다. 18222 드로어에 18 개 | 0(그리기만) | `server.py:109-114,140-142` · 단계 줄은 안 나옴(E8) |
| 가짜 턴 | `CHAT_FAKE_TURN=1 uv run python -m clinic_chat.consult --port <빈 포트>` — `step → list → sites → delta → done`(질문에 `error` 가 들면 `turn_error`) | 0 | `$C/README.md:71` · `fake_turn.py:1-5` · 0.1 꼴 리스트(E10) |
| 객체 패널 | `CHAT_DEBUG_PANEL=on` | — | `README.md:107` |
| 헤드리스 스크린숏 | `"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --user-data-dir=<임시> --window-size=1600,1000 --virtual-time-budget=4000 --screenshot=<파일> http://127.0.0.1:18222/c/<id>` — **실측 성공**(187KB PNG · 폰트 · 얼굴 · 리스트 정상 렌더) | GET 1 | Playwright 는 앱 venv 에 없다(import 실패) |
| 좌표 확인 | `GET /face-check` | 0 | `server.py:204-206` |

18222 프로세스(PID 79238 · cwd = 앱 워크트리 · 장부 `runs/consult/turns.jsonl` 4.9MB)는 건드리지 않았다.

---

## Q2. 명동점 상품(데모) — 있는 것만

### 2-1. 허브 silver/gold 의 상품 쪽 표 · 칸(로컬 PG 실측)

| 표 | 행 | 칸(상품 관련만 굵게) | 표본(코드 · 이름) |
|---|---|---|---|
| `s_price_list` | **1** | id · version · updated · currency · note | PLS-001 · 판 1.1 · 2026-07-26 · KRW · note = 「한국 시장 참고 가격 범위 · 클리닉/지역/의사에 따라 상이 · 정가 아닌 시장 범위」 |
| `s_offer` | 122 | id · **price_list_id** · name · modality_code · **price_low · price_mid · price_high**(122 행 전부 값 있음) · product_origin · variant_text · condition_text | OFR-0001 이마 주름(수입) M1 · OFR-0002 이마 주름(국산) M1 · OFR-0003 미간 주름(수입) M1 |
| `s_offer_item` | 163 | offer_id · target_table(procedure_case 59 · procedure 44 · product 40 · 빈칸 20) · target_code · text · note | — |
| `s_offer_quantity` | 129 | offer_id · text · amount · unit · qualifier | — |
| `s_offer_concern` · `s_offer_site` | (안 셈) | offer_id · concern_code / site_code · text | — |
| `g_offer` | 163 | offer_id · offer_name · modality · **price_low · price_high · price_mid_raw · currency** · quantities · item_* · **reach**(케이스 직접 59 · 시술 직접 44 · 제품 경유 29 · 못 닿음 20 · 제품 — 케이스 없음 8 · 제품 → 시술 3) · procedure_code · sites · concerns · effects · materials · variant_text · condition_text · product_origin | — |
| `s_package` | 119 | id · name · **kind**(메뉴 57 · 고민 패키지 24 · 고민 단계 조합 17 · 같은 날 조합 8 · 레시피 7 · 병합 기법 3 · 연간 플랜 2 · 비교표 조합 1) · concern_code · … · 가격 칸 **없음** | PKG-0001 동안 기본(같은 날 조합) · PKG-0002 리프팅 풀코스 · PKG-0003 보톡스+필러+스킨부스터 원데이 |
| `s_package_item` · `g_package` | 312 · 312 | `g_package.package_kind`(메뉴 83 행 · 고민 패키지 63 · 연간 플랜 58 · 고민 단계 조합 56 · …) · item_* · item_procedure_code | — |
| `s_product` | 315 | code · name_ko · **kind**(장비 159 · 약제 33 · 필러 33 · 스킨부스터 31 · 실 21 · 콜라겐 자극 주사제 20 · …) · parent_code · country · mfds | PRD-001 보톡스 · PRD-002 디스포트 · PRD-003 제오민 |
| `s_organization` · `s_product_organization` | 202 · 575 | 제조 · 수입 회사(`role`) — **병원 · 지점 아님** | — |

- 이름으로 훑은 결과(`information_schema` · 정규식 branch · clinic · hospital · store · event · discount · shop · menu · price · 지점 · sale · promo · org): **지점 · 병원 · 이벤트 · 할인 · 판매처 칸 0**. 가격 칸은 `s_offer` · `g_offer` 뿐(+ 옛 허브 표 아래).
- 로컬 DB 에는 옛 허브 표도 있다(전체 244 표 중 메달리온 76): `pricing_item`(가격 low/mid/high) · `recommendation_package`(price_min/max_krw) · `problem_package`(price_range) — **로컬은 셋 다 0 행**. stg 옛 API `GET /procedure-hub/api/v1/market-pricing` 은 200(꼴 = version · updated · currency · note · categories 17 × items{name · unit · low · mid · high}) — 옛 허브 판 시장 가격으로 보이며 지점 값 없음(값은 옮기지 않음).
- 「메뉴」 = `s_package.kind` 값 하나다. 앞 작업 결정: 메뉴는 시술 아님 · 시술로 내지 않음(`$A/_RESUME.md` §2 11-17 「얼굴 점 … V라인주사 등 메뉴는 시술 아님」) · 「메뉴 = 패키지 아님 — 모델링 다시 보기(사용자 결정 몫)」(`$A/_RESUME.md:29`) — 열려 있음.

### 2-2. 허브 응답에서 상품 · 메뉴가 나가는 자리

| 도구(REST `/procedure-hub/gold/…`) | 상품 · 메뉴가 실리는 칸 | 근거 |
|---|---|---|
| `facets` facet=`offer` | `rows[]` = `g_offer` 행(가격 · 수량 · reach · procedure_code …) · `node`(대상 · offer) 또는 `offer_name_contains`(상품 이름 부분 일치) · 제품 노드는 role `자기 · 하위 제품` | SPEC-001 0.8.2 `$A/SPEC-001-hub-gold-mcp.md:427-485` · stg 실측 `facets?facet=offer&node=procedure:PRC-001&limit=1` → 200 · 행 칸 30(`price_low` · `price_high` · `price_mid_raw` · `currency` · `offer_id` · `offer_name` · `reach` · `procedure_code` …) |
| `facets` facet=`package` | `g_package` 행(package_kind = 메뉴 포함) | 같은 문서 :427 |
| `coverage` kinds=`offer`,`package` | 종류별 행 수만(self · lower · inherited) | 안내서 `para/projects/company/procedure-hub/gold-api-guide.md:147,280-290` |
| `pair` | `package_kinds` 거르개 · `same_day_packages[]` | 안내서 :133 |
| `concern_candidates` | 메뉴(패키지) · 제품은 `from[].path[]` 의 층 이름으로만 · 시술로 내려간 묶음 `descended[]` | SPEC-001 :539-543 |
| `resolve` | 입구 offer 122 · package 119(이름 → 코드) | 안내서 :40 |

**지점 · 이벤트 · 최저가를 내는 도구 · 칸은 없다.**

### 2-3. 앱 상담 리스트가 지금 그리는 것 — 상품을 붙일 자리 지도

- 재료: 이번 턴 `concern_candidates` 응답(`purpose == "read"`) + profile 이어 조회의 계열 이름(`listing.py:1-4,26-122`).
- 꼴(켠 상태 0.3 · `list_v3.html`): 고민(`concern_code` · 이름 · 윗고민 `inherited_from`) → 계열 묶음(`modality_code` · 이름) → 시술 행(`procedure_code` · `procedure_name` · `data-reach` · `data-concern-match` · 표지) + 내려온 계열 묶음 `descended[]`(`list_v3.html:27-38`).
- 숨기는 것 `hidden{unreached_n, names[], descended_n, undescended}`(`listing.py:143-145`) — 못 닿은 후보(메뉴 · 패키지 이름이 여기) · 직접 닿은 계열의 내려온 시술 · 못 내려간 수. 장부에만 · 화면 0(`list_v3.html:2`).
- 시술의 키 = **`procedure_code`(`PRC-NNN` · `s_procedure.code` 138)** · 계열 = `modality_code`(`M1`~ · 18) · 상담 객체 `procedures[]` 도 PRC 로만 남긴다(SPEC-005 SL6 `$A/SPEC-005-consult-state.md:109` 「다음 단계(상품 매핑 · 최저가)의 입력 자리」).
- 행에 붙일 자리 후보(지금 코드): 시술 `li.cs-proc`(`list_v3.html:17-22`) · 계열 머리 `h4.cs-mod__name`(:12-14) · 리스트 조각 전체(`render.list` `render.py:99-100` · SSE `list` · `GET /c/{id}/list`).
- 앱은 상품을 **화면에 그리지 않는다**: 상담 객체 칸에서 offer · package 를 뺀다(`state.py:23` · `turn_kind.py:15`) · `offer` 는 「같이 읽을 종류」 이름(`kind_labels.offer` = 「상품 · 가격」)으로만 답 재료에 든다(`material.py:255` · `close.py:121-143`). 가격 값을 화면 · 리스트로 내는 코드 0.

### 2-4. 「명동」 · 「명동점」 · 「지점 상품」 · 「최저가」 · 「이벤트」 언급

- **허브 레포 · 앱 레포: 「명동」 0 건.** 「최저가」 0 · 「지점 상품」 0. 「이벤트」 는 SSE 이벤트 · 용어집 이벤트 뜻뿐(`backend/app/router/gold.py` · `assembly.py` · `glossary_*` · 앱 `turn.py` 등) — 판매 이벤트 뜻 0.
- 프로필 레포(procedure-hub 쪽만):

| 자리 | 무엇 |
|---|---|
| `$A/_RESUME.md:101-102` | 11-17 결정 — 이번 범위는 시술까지 · 다음 단계 = 「명동점 실제 상품(시술 상위 데이터)을 시술에 매핑 → 그 시술을 받을 수 있는 조합 중 최저가(이벤트 포함)」 · 입력 = 시술 코드 |
| `$A/SPEC-005-consult-state.md:55,83,92,109` · `SPEC-006-consult-v03.md:100` · `spec-chat-v02-instructions.md:23` | 범위 밖 표기(명동점 상품 · 최저가 · `g_offer` 가격 칸) |
| `orchestration/work/_archive/procedure-hub/phub-recommend/kos-link-research.md:1,9,13-14,272-313,357,384-393` · `kos-link-research.json:153,816,827,13656` · `…-kos-link-research-brief.md:1,11,18,33,35` · `next-session-architecture-prompt.md:14` | 10-30 조사 「KOS(명동점) 상품 ↔ 허브 실버 연결」 — 명동점 KOS 2026-10-28 스냅샷 · 진료 항목 시술 126 · 약제 50 · 장비 22 · 실버 단위 시술 162 중 닿음 62 · 사용자 판단 U1 · U2 열림 |
| `para/projects/company/procedure-hub/log/2026-10-30-gold-decisions.md:167-173` | 「kos 는 일단 기록만 · 허브 품질 측정이 먼저」(사용자) · U1 · U2 열려 있음 |
| `phub-recommend/step1-d18*.json` · `quality-v*/inputs/step1-d18.json` | 세라미크의원 강남 · 명동 홈페이지 크롤 언급(이름 0 건) |
| `phub-ledger-redesign/first-pass/market-pricing/review-part-S08.md:45` | 「최저가 항목」 = 시장 가격 표 검수 메모(명동 무관) |

- **명동점 원자료가 이미 있는 자리**(읽지 않고 이름만 봄): `/Users/kknaks/git/ax-clinic-project/para/projects/clinic-myeongdong-ax/sources/internal-data/kos-raw/2026-10-28T172138-b5a14ccb/raw/` — KOS API 응답 폴더 22 개(`getProducts` · `getProcedures` · `getMedicalServices` · `getMedicines` · `getMachines` · `getCategories` · `getTicketBundlesQuery` · `getPrepaidCardChargingEvents` · `getPurchaseItemStatistics` …). 같은 상위 폴더에 날짜 스냅샷 8 개. phub-recommend 조사(위)가 이 raw 를 원천으로 썼다.
- 그 밖 프로필 레포의 「명동」 은 다른 프로젝트(cc-prototype `myeongdong-poc-v2` 44 파일 · DAY `day-data-architecture` 46 · agency-settlement 14 · `reference/2026-11-03-cc-day/erd/04-1-menu.md`(DAY 메뉴 ERD) · 통키 `interpreter-idea` 1)다 — 상품 꼴의 근거로 쓰지 않았다(메모리 사례).

### 2-5. 데이터 꼴을 정할 때 사용자에게 물을 것(질문만 — 꼴 제안 없음)

| # | 질문 |
|---|---|
| U-21 | 무엇을 줄 건가 — 원천이 KOS(위 raw 폴더 같은 API 응답) · 엑셀 · 병원 홈페이지 · 손으로 정리한 표 중 무엇인가. 이미 있는 2026-10-28 KOS 스냅샷을 쓰나, 새로 받나 |
| U-22 | 「상품」 한 줄의 단위는 무엇인가 — 진료 항목 하나 · 회차권 · 옵션 · 묶음 중 무엇이 화면의 한 줄인가 |
| U-23 | 「시술 상위 데이터」 의 뜻 — 상품이 허브의 무엇(시술 PRC · 계열 M · 제품 PRD · 케이스 CAS)에 매달리나. 매핑은 누가 하나(사용자가 준 표에 코드가 있나 · 앱 · 허브가 이름으로 맞추나) |
| U-24 | 가격 값의 종류 — 정가 · 할인가 · 이벤트가 · 회차당 가격 중 무엇이 오나. 「최저가」 는 무엇 중의 최저인가(한 시술을 받을 수 있는 상품들 사이 · 조합 전체) |
| U-25 | 「이벤트」 는 기간 · 조건(첫 방문 등)이 있나 · 데모에서 기간을 보나 |
| U-26 | 지점은 명동점 하나로 고정인가 · 다른 지점이 붙을 자리를 지금 두나 |
| U-27 | 데이터를 어디에 두나 — 허브(병원 무관 원칙 — `next-session-architecture-prompt.md:14` 「허브는 병원과 무관 · 고정」) · 앱 · 별도. 공개 레포(clinic_chat 은 공개)에 명동점 가격을 올려도 되나 |
| U-28 | 허브 `g_offer`(시장 참고 가격)와의 관계 — 명동점 가격과 같이 보이나 · 대신하나 · 안 보이나 |
| U-29 | 화면에서 어디에 무엇을 — 리스트의 시술 행 옆 · 따로 칸 · 답 글 안. 「담기」(받고 싶은 시술 고르기 — 11-17 「다음 단계」)가 먼저인가 |
| U-30 | KOS 연결 조사의 열린 둘(U1 명동점에만 있는 부위 · 제품을 허브에 보강하나 · U2 판단 불가 28 · 굵음 14 확인)을 이번에 닫나 |

---

## Q3. 시술 그림 응답

### 3-1. 원천 `$H/assets/procedure-images/`

| 항목 | 값 |
|---|---|
| 파일 | SVG **103**(`images/mechanism/MEC-NNN.svg` 54 · `images/method/MET-NNN.svg` 49) + `README.md` 1 · 다른 확장자 0 |
| 크기 | SVG 합 6,886,445 바이트 · 폴더 6.7MB(du) |
| 판 | `artwork_version` = `2026-11-17-native-svg-v1` 103 전부 |
| 규격 | 1200×800 · 래스터 · 스크립트 · 스타일시트 · `foreignObject` · 바깥 참조 없음 · `<text>` + `data-i18n` · 루트 `lang="ko"`(README · 시험 `backend/tests/test_medallion_image.py`) |
| 매핑 csv | 이 폴더에는 없다 — 매핑은 silver `data/medallion/silver/concept_image.csv`(103 · `svg_path` 가 이 폴더 기준 상대 경로) · `concept_image_label.csv`(787 · `lang` = ko 787) |
| 검수 상태 | `medical_review` = 「검수 전」 103/103 · 게이트 아님(README · `$A/_RESUME` U-4) |
| 외부 사진 | 활성 그림 0. MEC-070 은 직접 그린 SVG(`<text>` · 도형만). 옛 CC BY-SA JPG 는 프로필 `reference/2026-11-17-procedure-images/legacy-source/` 에만(허브로 안 옮김 · `$A/research-images-v2.md:30,113`). 그 SVG 가 사진을 보고 그린 것인지는 파일로 알 수 없음(같은 문서 :115 — 확인 안 됨 그대로) |
| 이미지 포함 | 루트 `.dockerignore` 가 `backend/` 의 일부만 허용 → `assets/` · `data/` 는 build context 밖 |

### 3-2. silver/DB

- 로컬 PG: `s_concept_image` **103** 행 · 칸 `load_seq · id(CIM-) · target_table · target_code · svg_path · sha256 · artwork_version · medical_review` · 유일 (`target_table`, `target_code`) / `s_concept_image_label` **787** 행 · 칸 `load_seq · id(CIL-) · image_id(FK) · element_id · i18n_key · lang · text`(alembic `$H/backend/alembic/versions/b202611170002_medallion_concept_image.py:26-48`).
- gold 15 표에 그림 칸 **없음**(SPEC-007 §5 U7-1 (a) · `g_profile` 칸에 그림 0 — 실측).
- 연결 경로(실측):
  - 원리: `s_procedure.mechanism_code` → 138 중 136 값 · 서로 다른 51 코드 → 그림 51 코드와 전부 맞음. gold 에서는 `g_profile.mechanism_code`(739 행 중 401 · 51 코드). `s_modality.mechanism` 은 글 칸(코드 아님).
  - 방법: gold 에 방법 **코드** 칸 없음(`g_profile.methods` = 이름 글). silver 에서 `s_case_method`(107 행 · 36 코드 — 케이스) · `s_product_method`(63 · 17 — 제품) → 그림 방법 49 중 39 코드가 닿음. 시술(PRC)과는 케이스 · 제품을 거쳐야 한다. SPEC-007 N7-2 「방법 그림을 행 옆에 붙이는 길」 열림.
  - 원리 54 중 3 · 방법 49 중 10 은 위 길로 안 닿음(SPEC-007 :429 「gold 가 안 가리키는 코드 13」 과 같은 수).

### 3-3. 허브 코드

- 그림을 읽는 곳: **적재기만**. `GOLD_IMAGE_DIR`(`modules/gold/config.py:69` · 기본 빈칸)는 `medallion_load.py:219-230` V13 이 폴더 ↔ `s_concept_image`(경로 · sha256)을 대조할 때만 읽는다. 없으면 `image_files unchecked(GOLD_IMAGE_DIR 없음)`(:43). 문서도 같은 말(`backend/README.md:167` · `envs/.env.example:23` 「적재기만」 · SPEC-007 :277).
- DB 판 repository 는 그림 2 표를 **읽지 않는다**(시험 `tests/test_medallion_repo.py:302` IT6).
- 정적 서빙: 허브 `backend/app` 에 `StaticFiles` · 그림 라우트 **0**(grep). gold 부착 = `app/main.py:17,34`(`mount_gold`) — REST `GOLD_API_PREFIX` `/procedure-hub/gold` · MCP `/procedure-hub/gold-mcp`(`config.py:51-52`).
- 도구 응답: SPEC-001 0.8.2 에 「그림 · image」 언급 **0**(grep). 안내서 `gold-api-guide.md:39,413` 「응답에는 아직 없다(다음 판)」.
- stg 실물(GET): `gold/health` 200 · gold_hash 8accbb21 · aux_hash 93ec89fd · `files[]` 22 줄(그림 0) · `gold/openapi.json` 경로 9(`/resolve` · `/scope` · `/neighbors` · `/facets` · `/concern-candidates` · `/pair` · `/evidence` · `/coverage` · `/health`) · 본문에 「image」 「svg」 0 · 시험한 정적 경로 5 개(`/procedure-hub/static/…` · `/images/…` · `/gold/images/…` · `/gold/image` · `/assets/procedure-images/…`) 전부 404.

### 3-4. stg 서빙 자리

- 이미지: `backend/Dockerfile:1-28` — runtime 단계는 `app/` · `alembic/` · 운영 스크립트 4 개(+ `load_medallion.py` :23)만 · `assets/` · `data/` 없음(ADR 0004 「image 는 migration + API 만」 · `docs/adr/0004-…:82,110` · SPEC-003 :773 I-1 「데이터는 싣지 않는다」).
- 볼륨: 레포 안에는 서빙 컨테이너의 실행 옵션이 없다 — CD 는 Bastion 의 `./deploy.sh procedure-hub stg` 를 부른다(`.github/workflows/csp-azure-deploy.yml` 「Bastion 경유 배포」). ADR 0004 :20 「VM 의 `deploy.sh` … 는 이 저장소만으로 확인할 수 없다」. prod 전환 helper 는 「기존 mounts 없음」 을 검사한다(`docs/guides/prod-migration.md:273`). 적재 컨테이너는 그림 폴더를 `-v …:ro` 로 꽂지만 「서빙 컨테이너에 마운트 · `docker cp` 를 하지 않는다」(SPEC-003 `$A/SPEC-003-hub-gold-db.md:838` · `stg-runbook.md:35,43`).
- 정한 것 / 열어 둔 것:
  - 정함: 그림은 허브 레포 에셋 폴더가 원천 · **바인드 마운트**(읽기 전용 · 로컬 = 레포 폴더 · 서버 = VM 디렉터리) 방향(`$A/_RESUME.md` §2 11-17 U-10 · 「바인드 마운트」 행) · 대표 103 만 서빙(SPEC-007 G-8) · 원리 · 방법을 물은 턴에만 화면(U-10 같은 행).
  - 열림: SPEC-003 §11 S-7 「그림 서빙은 다음 스펙」(:672) · SPEC-007 §9 N7-1 ~ N7-7(:360-372) · stg VM 에 그림 폴더 사본은 적재 때 `/opt/procedure-hub/import/<날짜>/` 에 옮겨 둔 것(runbook ②)이 있으나 서빙용 자리는 미정.
- 선택지별 사실(결정 아님):

| | 마운트(VM 디렉터리 → 서빙 컨테이너 `:ro`) | 이미지에 포함(`COPY assets/…`) |
|---|---|---|
| 크기 | 이미지 불변 · VM 디스크 +6.7MB | 이미지 +약 6.9MB(SVG 103) |
| 바꿔야 하는 것 | 레포 밖 VM `deploy.sh`(인프라 · 이 레포로 확인 불가) · prod helper 「기존 mounts 없음」 검사와 부딪힘 · 그림 폴더를 VM 에 옮기는 절차 | `.dockerignore`(지금 `backend/` 만 허용) · `Dockerfile` · ADR 0004 「image 는 migration + API 만」 과의 관계 |
| 그림만 바뀔 때 | VM 폴더 교체(+ 재시작 필요 여부는 서빙 방식 따라 — 확인 안 됨) · 이미지 재배포 0 | CD 트리거 경로가 `backend/**` · `.dockerignore` · 워크플로뿐이라 `assets/` 만 바꾸면 **CD 가 안 돈다**(`csp-azure-deploy.yml:8-13`) — 수동 dispatch 또는 경로 추가 |
| 되돌리기 | 폴더 사본 교체 | `${env}-rollback` 이미지 + DB 백업 묶음(ADR 0004 :112) |
| 메모리 | 정적 파일 읽기 — stg VM 여유 약 210MB · swap 0(SPEC-003 :850) | 같음 |

### 3-5. 앱 쪽 — 그림을 띄울 자리 후보(지금 코드 지도)

| 후보 | 지금 코드 | 사실 |
|---|---|---|
| 채팅 답 안 | `answer.html` · `delta.html`(마크다운) | 마크다운 렌더러가 **이미지 문법을 끔**(`render.py:19` `.disable("image")`) · 날 HTML 이스케이프(`html: False`) — 답 글로는 그림이 못 들어간다. 그림은 별도 조각 · 별도 SSE 이벤트가 필요한 자리 |
| 턴 아래 별도 칸 | `turn.html:7-16`(SSE 받는 자리 6 개) | 새 이벤트 이름을 더하는 자리. `htmx-config` `allowScriptTags:false`(`base.html:7`) — SVG 안 스크립트는 없음(원천 규격) |
| 리스트 시술 행 | `list_v3.html:17-22` | 원리는 시술 → `mechanism_code` 로 닿음 · 방법은 시술에 직접 코드 없음(3-2) |
| 얼굴 패널 · 드로어 | `main.html:6-12` · `drawer.html` | 얼굴은 부위 점 전용 · 드로어는 지난 대화 목록 전용 — 상세 드로어 없음 |
| 앱이 원리 코드를 이미 받나 | profile 이어 조회 `listing.py:76-81` 가 `g_profile` 행을 읽음 | `mechanism_code` 칸이 그 응답에 있다(`g_profile` 칸) — 앱이 화면에 쓰는 코드 0 |

- 인라인 SVG vs `<img>`: 인라인이면 파일 사이 id 54 종이 겹치고 · `<img>` 면 화면 폰트가 안 먹는다(SPEC-007 N7-4 :369 · 조사 2 §6-2). Jinja 자동 이스케이프 켬(`render.py:48`).
- 앱 → 허브는 로컬 18105 기본(`config.py:41-42`) · 허브가 aux 를 바꾸면 coverage 나눔 도중 `build_changed`(`clients/hub_rest.py:216-224` — `gold_hash` · `aux_hash` 둘 다 봄) · 대화 끝(`ledger.py:31`).

### 3-6. SPEC 쪽 공백

| 문서 | 이미 있는 계약 | 열린 것 |
|---|---|---|
| SPEC-007 0.1.0 | silver 2 표 · DB 2 표 · 적재 V13 · 에셋 폴더 · 해시(그림 표 = `silver` · aux 아님 · health 22 줄) · I2(103 코드 = 그림 103) | §9 N7-1 새 도구(9 → 10 · 그때 aux 승격 · `health.files` 증가 :285) · N7-2 방법 그림 연결 · N7-3 정적 서빙 · 마운트 · N7-4 앱 화면 · N7-5 시드 자리(지금은 허브 레포로 닫힘 — SPEC-003 0.2) · N7-6 다국어 · N7-7 검수 절차 · §11 O7-3 · O7-4 · O7-7 |
| SPEC-001 0.8.2 | 도구 9 · 응답 꼴 — 그림 0 | 그림 도구 · 칸 미정(문서 안 언급 0) |
| SPEC-003 0.2.1 §11 | stg = app.main 부착 · 일회성 적재 · 그림 폴더는 적재 때만 꽂음 | S-7 그림 서빙(:672) · O-S6 prod 승격(:886) |
| SPEC-004 ~ 006 · 008 | 앱 화면 · 리스트 · 객체 · 입구 | 그림 · 「담기」 · 상품 · 최저가 = 범위 밖(SPEC-006 :100 · SPEC-005 :55,92) |

---

## Q4. 묶음 · 순서에 영향 주는 사실

### 겹침(같은 파일 · 같은 계약)

| 자리 | 1 GUI | 2 상품 | 3 그림 |
|---|---|---|---|
| `$CC/templates/partials/list_v3.html` · `listing.py` | ○(리스트 꼴 · 묶음 경계 E5) | ○(시술 행 · 계열 머리에 붙음) | △(리스트에 띄우면) |
| `turn.html` · `answer.html` · SSE 이벤트 목록(`turn.py`) | ○ | △(답 · 별도 칸이면) | ○(턴 칸이면 새 이벤트) |
| `main.html` 칸 배치 · `consult.css` 그리드 토큰 | ○ | △(새 칸이면) | △(새 칸이면) |
| `prompts/consult.json` `slots{}` | ○(빈 문구 값) | ○(상품 칸 머리 글) | ○(그림 칸 머리 글) |
| 허브 도구 계약 SPEC-001 · aux_hash · health | — | △(데이터를 허브에 두면) | ○(새 도구 · aux 승격 → 앱 `build_changed` 로 열린 대화가 끝남) |
| 허브 배포(stg CD · VM) | — | △ | ○(서빙 길에 따라 VM `deploy.sh` · Dockerfile) |
| 상담 객체 `procedures[]`(PRC) · 「담기」 | — | ○(매핑의 입력 — SPEC-005 SL6) | — |

### 선후 의존(사실)

- 그림 화면 · 상품 화면은 GUI 와 같은 템플릿(`main.html` · `turn.html` · `list_v3.html`) · 같은 CSS 토큰 블록을 고친다.
- 그림 화면은 허브 쪽(새 도구 · 서빙 · stg 배포)이 먼저 있어야 실물로 보인다. 로컬은 허브 18105 를 띄워야 한다(지금 LISTEN 0 — E9).
- 상품은 데이터가 들어와야 시작된다(사용자 몫). 11-17 결정 순서는 「담기 → 명동점 상품 최저가」(`$A/_RESUME.md:101`) — 「담기」 는 아직 0.
- 화면 문구는 전부 빈칸이 정본 상태다(문구 지어 넣기 금지 · 사용자 값 대기) — 세 가지 모두 새 칸 머리 글이 같은 대기열에 선다.
- 가짜 턴은 0.1 꼴이라(E10) GUI 시험을 0.3 꼴로 재생하려면 옛 대화 열기 · 실물 턴이 필요하다.

### 코디 참고(짧게)

GUI 와 그림 화면은 같은 템플릿을 고치므로 GUI 피드백을 먼저 닫고 그 꼴 위에 그림 칸을 얹는 순서가 충돌이 적어 보인다. 그림의 허브 쪽(도구 · 서빙 · 배포)은 앱과 파일이 안 겹쳐 병행할 수 있다. 상품은 데이터 · U-21~30 답이 오기 전에는 지도 이상 할 것이 없다.

---

## 정할 것 모음

| # | 무엇 | 몫 |
|---|---|---|
| P-1 | 화면에서 무엇이 불편한가(E1~E10 을 보여 주고 받기) | 사용자 |
| P-2 | 빈 문구(`data-slot`) 값 — 제목 · 「새 대화」 · 입력 안내 · 표지 · 묶음 머리 · 오류 | 사용자 |
| P-3 | 좁은 화면(E7)을 이번 범위에 넣나 | 사용자 |
| P-4 | mojibake 장부 행(`turns.jsonl:21,24`) 처리 · 폼 해석 방어를 넣을지 | 코디(사실 확인 뒤 사용자에 한 줄) |
| P-5 | 가짜 턴을 0.3 꼴로 올릴지(GUI 시험 재생용) | 코디 |
| U-21 ~ U-30 | 명동점 상품 데이터 꼴 질문(§2-5) | 사용자 |
| U-31 | 「메뉴 = 패키지 아님 — 모델링 다시 보기」(`$A/_RESUME.md:29`)를 상품 작업과 같이 보나 | 사용자 |
| G-1 | 그림 도구 꼴(새 도구 10 번째 · 응답 칸) · aux 승격(N7-1 · 응답 · `health` 바뀜 → 앱 열린 대화 `build_changed`) | 코디 → 스펙 |
| G-2 | 방법 그림을 시술에 잇는 길(N7-2 — 케이스 · 제품 경유 / 코드 칸 추가) | 사용자(gold 해시 · 37 키가 바뀌는 쪽이면) / 코디 |
| G-3 | stg 서빙 길 — 마운트(VM `deploy.sh` · prod 「mounts 없음」 검사) vs 이미지 포함(ADR 0004 · CD 경로) · VM 반입 자리 | 사용자(인프라 · ADR 와 부딪힘) |
| G-4 | 앱 화면 자리(답 아래 칸 · 리스트 · 따로) · 인라인 vs `<img>` · 「물은 턴에만」 의 판정 기준(턴 종류 `mechanism`?) | 사용자(자리) / 코디(구현 꼴) |
| G-5 | 검수 전 103 장을 그대로 노출(정해짐 U-4) — 화면에 「개념도」 표기가 필요한가(README 의 문장) | 사용자 |
| G-6 | 프로필 `reference/2026-11-17-procedure-images`(미추적 · CC BY-SA JPG 포함) 처리(O7-7) | 코디 |

## 확인 안 됨

- mojibake 요청을 누가 · 무엇으로 보냈는지(18:48:33 · 장부에는 클라이언트 정보 없음).
- E7 좁은 화면 넘침 · E9 18105 없을 때 새 턴의 실제 화면 — 띄우거나 보내 보지 않았다(18222 는 GET 만).
- stg 서빙 컨테이너의 실제 실행 옵션(볼륨 · 마운트) · VM `deploy.sh` 내용 — 레포 밖 · VM ssh 금지.
- stg VM 디스크 여유(그림 6.7MB 를 둘 자리).
- 옛 허브 `api/v1/market-pricing` 값의 원천 · 갱신 시점과 silver `s_price_list` 와의 관계(꼴만 봄).
- 명동점 KOS raw 의 내용 · 가격 · 이벤트 칸(폴더 이름만 봄 — 꼴 추측 금지).
- MEC-070 SVG 가 옛 사진을 보고 그렸는지(앞 조사와 같음).
- `s_offer_concern` · `s_offer_site` 행 수(안 셈).
