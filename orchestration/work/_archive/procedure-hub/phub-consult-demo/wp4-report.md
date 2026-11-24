# WP-4 리포트 — 모달 값 · 그림 라우트 (app 워커 · 2026-11-20)

발주 `task_cc1b5c2dbcd1` · `ctx_99756efd278c` · SPEC-010 0.2.7 §4-5 · MD1 ~ MD5 · §8 IM1 ~ IM13 · D-11 · D-12 · D-19 · §13 WP-4. 허브는 18105 `caa03560`(WP-H 뒤 · GET 만)이다. 커밋 0 · push 0 · 18222 손 안 댐(pid 64439 그대로) · 확인 서버 18296(끝에 내림).

## 0. 먼저 알릴 것 — 그림 시드 폴더가 사라졌다

발주의 시드 경로 `kknaks_profile/프로시저허브-데이터-메달리온/reference/2026-11-17-procedure-images/images/` 가 **디스크에 없다**(WP-0 때는 있었다). `kknaks_profile/` 은 17:10 에 바뀌었고, 지금 그 자리에는 `프로시져허브메달리ոն/`(안에 `orchestration/` 만) · `data-medalion/` 이 있다. 같은 그림은 **허브 레포 `PROCEDURE-HUB/phub-consult-demo/assets/procedure-images/images/`** 에 있다(정규식 파일 원리 55 · 방법 66 · MEC-108 포함). silver `concept_image.csv` 121 행과 **sha256 이 모두 같다**(어긋남 0). 그래서 실물 확인은 이 경로를 `CHAT_IMAGE_DIR` 로 했다. 스펙 IM1 · D-19 의 시드 경로 문구 · 배포 바인드 마운트 자리(IM4)는 코디가 확인할 거리다.

## 1. 바뀐 파일

| 파일 | 무엇 |
|---|---|
| `clinic_chat/consult/modal.py`(새) | `build(kos, hub, gold, code, image_dir)`: **`$J` 칸** kind · name · code · kind2 · site(IL4) · drug · device(원문) · 게시 배지. **허브 칸**(케이스마다 `facets` profile · outcome · adverse · 프로세스 캐시 (gold_hash, 노드, facet) · 오류는 캐시 안 함): lead · 원리 글 · 원리 이름 · 원리 코드 = 케이스 profile 의 **물려받은 시술 행**(N5 · 계열 행은 안 씀) · 시술이 여럿이면 `hub.procedure_codes` 순서로 원리 하나씩 · 방법 = 케이스 행 `method_codes`(` · `)와 `method_texts`(`\n`)를 같은 자리끼리 · 케이스 순서 → 안 순서 · 같은 코드 한 번(MD1 · IM6) · 효과 = `effect_code` 있는 행만(N3 · 경과 줄은 `course` 로 따로 — LLM 몫) · 부작용 = `polarity` 「발생함」 만(N4 · 나머지 `side_other`) · 같은 코드는 먼저 나온 케이스 하나 · `data-case`. 케이스 0(MD2) = 허브 칸 0 · 허브 오류(MD3) = 허브 칸 0 + `error`. 그림 = 코드 + 있음(요청마다 파일) · `figs()` = 장부 IM12 |
| `clinic_chat/consult/images.py`(새) | IM1 · IM2: `CHAT_IMAGE_DIR/<표>/<코드>.svg` · 표 = mechanism · method 둘 · 정규식 `^MEC-\d{3}\.svg$` · `^MET-\d{3}\.svg$`(표 ↔ 접두어) · `..` · 다른 확장자 · 폴더 밖 심볼릭 링크 = 없음. IM3: 있음 판단은 요청마다 · ETag = sha256 앞 16. IM13: 정규식 파일만 셈 |
| `templates/partials/modal.html` · `modal_body.html`(새) | 모달 안을 `modal_body.html` 로 뺐다. `pm` 이 없으면 WP-2 빈 틀 그대로다. 있으면 시안 칸에 값을 넣는다 · 원리 figure 는 원리 코드마다 · 방법 figure 는 방법마다(`data-pm-fig` · `data-code` · `data-case`) · img = `/img/<표>/<코드>.svg`(alt = slot `fig-alt`) · 파일 없음 / 폴더 빔 = img 0 + 빈 slot `pm-fig-missing`(IM8) · 코드 없음 = figure 0(IM9) · 효과 · 부작용 줄 = `<b>이름</b>` + 원문 칸 span(잇는 글자 0) · MD2 · MD3 = 탭 넷 그대로 + 빈 slot `pm-empty` 셋 |
| `clinic_chat/consult/server.py` | **`GET /c/<id>/item?code=`**(RT1 쿼리 값 · `$J` 에 정확히 있을 때만 · 장부 줄 `viewed{code, modal{figs, error}}`) · **`GET /img/{table}/{name}`**(헤더 `image/svg+xml` · `nosniff` · `no-cache` · ETag · `If-None-Match` → 304) · `image_on` 전역(비면 그림 칸 숨김) · `app.state.image_counts` + 로그(IM13) |
| `clinic_chat/consult/ledger.py` · `render.py` | `Ledger.viewed()`(MD4 · IM12) · `Render.modal_body()` |
| `clinic_chat/consult/static/consult.js` | 「시술설명」 → 서버 조각을 받아 dialog 안을 바꾸고 연다(카드 · 장바구니 「시술설명」 둘 다 · 담김 단추 맞춤) |
| `clinic_chat/consult/static/consult.css` | 원문 칸 span 간격 · 빈 `pm-fig-missing` 숨김(3 줄) |
| `tests/test_v05_modal.py` · `test_v05_images.py`(새) | 9 + 5 시험 |

## 2. 시험

| 명령 | 결과 |
|---|---|
| `.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_v05_modal.py tests/test_v05_images.py` | **14 passed** — 모달: 케이스 1(`$J` 칸 원문 · lead = 시술 행(계열 아님) · 원리 · 방법 figure 순서 · `method_texts` 줄바꿈 나눔(「·」 든 글 그대로) · 있는 그림 img · 없는 그림 MET-004 = img 0 + `pm-fig-missing` · alt 빈칸 · `pm-empty` 숨김) · **MD1**(케이스 둘 — 방법 MET-002 · 006 · 007 · 같은 코드 한 번 · 효과 `data-case` 먼저 케이스 · 경과 줄 뺌 · 부작용 「발생함」 만 · 심각도 · 메모) · **MD2**(케이스 0 — figure 0 · `pm-empty` 셋 보임 · 허브 호출 0 · 탭 넷) · **IM9**(원리 코드 빔 → figure 0) · **MD3**(허브 500 → 허브 칸 0 · 장부 `viewed.modal.error` · 다시 열면 다시 부름) · 캐시 · 장부 `viewed.figs`(IM12) · 장부 가격 0 · `CHAT_IMAGE_DIR` 빔 → img 0 · RT1 코드 셋 · 없는 코드 404 · 페이지 빈 틀 그대로. 그림: 헤더 · 거절 아홉(표 ↔ 접두어 · 다른 표 · 사본 이름 · 자리 수 · 확장자 · `..` · 없는 파일 · 폴더 밖 링크) · 요청마다 있음 판단 · 304 · 파일 바뀌면 ETag 바뀜 · 폴더 빔 = 404 · IM13 셈 |
| 위 + v05 전부(page · detect · ask_axis · kos_map) + 0.4 `test_consult_page`(T17) · `chat_ui` · `v03_frame` · `consult_ledger` · `v04_ledger` · `v03_start` · `consult_turn` | **158 passed** |
| `ruff check` · `ruff format` 손댄 py | 통과 |

- 걸렸다 고친 것: 0.4 T17 이 `modal.py` 의 「발생함」 상수를 잡음 → `\u` 이스케이프.

## 3. 실물 대조(허브 caa03560 · `$J` 1af2216c · `CHAT_IMAGE_DIR` = 허브 레포 그림)

| 진료항목 | 케이스 | 원리(시술 · 코드 · 그림) | 방법(케이스 · 코드 · 그림) | 효과(목록 · 뺀 경과 줄) | 부작용(목록 · 뺀 줄) | 허브 원문과 같음 |
|---|---|---|---|---|---|---|
| 26-JUREK-ZOMN 입꼬리보톡스 제오민 | CAS-006(1) | PRC-001 · MEC-001 아세틸콜린 차단 · 있음 | CAS-006 · MET-002 · 있음 | 11(사각턱 축소 · 턱선 정리 · 항노화 · 리프팅 …) · 경과 4 뺌 | 41(신경 손상 · 부종 · 멍 …) · 해당 없음 3 · 보고 없음 1 뺌 | 케이스 행 `method_codes` = 'MET-002' · 글 1 줄 |
| 26-BBL-1MODE BBL HERO (1가지 모드) | CAS-060 + 061(둘 — MD1) | PRC-006 · MEC-041 선택적 광열 · 있음 | MET-111(두 케이스 모두 MET-111 → 한 번) · 있음 | 6(제모 · 색소 개선 · 톤 균일 · 문신 제거 · 피부 재생 · 주름 개선) · 경과 4 뺌 | 23 | 두 케이스 모두 'MET-111' |
| 26-SKBST-CLCR-5CC 셀코어 | 0(MD2 · 시술 확인 필요) | — | — | — | — | 허브 칸 0 · `$J` 칸만 |

- **방법 그림 순서**: 방법이 둘인 명동점 케이스 5 개(CAS-016 · 046 · 050 · 081 · 1026) 모두 모달 순서 = silver `case_method` 행 순서이고, 글 = silver `method.csv` `description` 원문이다(5 / 5).
- **명동점 그림 빠짐 0**: 324 진료항목 전부를 모달로 지었다. 원리 figure 306 · 방법 figure 332 가운데 **파일 없음 0** · 허브 오류 0. 시작 셈 `image_counts` = 원리 55 · 방법 66(IM13 정상).
- 「BBL HERO (1가지 모드)」 효과에 「제모」 · 「문신 제거」 가 든다 — O-6(시술 · 계열 층 물려받음)대로 원본을 보인 것이다.

## 4. 스크린숏(`$W/wp4-shots/` · 1440 × 900 · 18296)

| 파일 | 무엇 |
|---|---|
| `1-jurek-zomn-overview.png` · `-desc.png` · `-effect.png` | 입꼬리보톡스 제오민 — 개요(lead · 칸 여섯 · 게시됨) · 설명(「시술 원리」 글 + 아세틸콜린 차단 그림 · 「시술 방법」 글 + 근육 주사 그림) · 효과 목록 |
| `2-bbl-1mode-overview.png` · `-desc.png` · `-effect.png` | BBL HERO (1가지 모드) — 케이스 둘 · 원리 MEC-041 · 방법 MET-111 하나 |
| `3-celcore-overview.png` · `-desc.png` · `-effect.png` | 셀코어 — 케이스 0 · `$J` 칸만(약물 셀코어 · 기기 해당 없음) · 설명 · 효과 · 부작용은 빈 slot(문구 0) |

페이지 오류 0 · 그림 img 4 개 모두 그려짐(naturalWidth > 0).

## 5. 스펙과 다른 점 · 남은 것

| # | 무엇 | 제안 |
|---|---|---|
| G1 | 시드 경로 사라짐(§0) | IM1 · D-19 · IM4 의 경로를 허브 레포 `assets/procedure-images/images/`(같은 sha) 또는 새 시드 자리로 코디가 정함 |
| G2 | MD4 라우트 꼴 | 스펙 MD4 는 `/c/<id>/item/<code>` 이지만 RT1(코드를 경로에 넣지 않음) · §4-9 표대로 **`/c/<id>/item?code=`** 로 했다 | MD4 문구 맞춤 |
| G3 | 모달 조각 = dialog **안**(머리 · 탭 · 몸 · foot) | dialog 자체는 페이지에 한 번 · JS 가 안을 바꿈 | — |
| G4 | 효과 · 부작용 줄 꼴 | `<b>이름</b>` + 원문 칸 span(심각도 · 메모) · 잇는 글자 0(시안 예시 「— 설명」 꼴의 줄표는 지어 넣지 않음) | — |
| G5 | 경과(`pm-effect-course`) · 「보고 없음 / 해당 없음」 부작용 | 화면 0(slot 빈칸 숨김) · 값은 `modal.build` 의 `course` · `side_other` 로 들고 있음 → LLM 블록은 WP-6 | WP-6 |
| G6 | 장부 `viewed` → 다음 턴 LLM 블록 「본 진료항목」 | 줄은 남김 · 싣기는 WP-6 | WP-6 |
| G7 | 시술 여럿인 진료항목 | 원리는 시술마다 하나(`hub.procedure_codes` 순서) · lead 는 첫 시술의 개요 하나 | — |
