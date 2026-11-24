# WP-2 리포트 — 화면 틀 (app 워커 · 2026-11-20)

발주 `task_a9db7188b608` · `ctx_4143f95e481c` · SPEC-010 0.2.3 §4 · §12 · §13 WP-2. 커밋 0 · push 0 · 18222 손 안 댐(pid 64439 그대로) · 확인 서버 18298(끝에 내림).

## 1. 바뀐 파일

| 파일 | 무엇 |
|---|---|
| `clinic_chat/consult/static/consult.css` | **시안 둘째 `<style>`(줄 162 ~ 446)로 통째 바꿈**(첫째 덩이 줄 3 ~ 161 = 0.4 `medikit.css` 와 같음 — 빈 줄 하나 차이 · 그대로 둠). 글꼴만 시안의 base64 인라인 → 0.4 파일 `PretendardVariable.woff2`. 끝에 시안에 없는 자리 11 줄(아래 §4) |
| `clinic_chat/consult/ui_text.json`(새) | **시안 글자**(§12 「시안에 있는 글자」 33 + 시안의 aria 글자 「빼기」 · 「시술 설명 목차」 + 사용자 문구 「옵션 추가 +」 · 「추가」). 0.4 T17(코드 · 템플릿 · css · js 한글 0)을 지키려고 화면 글자를 이 파일에 둠 → `Render` 가 `txt` 로 실음 |
| `clinic_chat/consult/items_view.py`(새) | IL · FS 값: `view(kos, codes, site=)`(묶음 = 감지 순 · 묶음 안 = groups 순 · 합계 · 얼굴 점 비율 × 590 · 1060 · 같은 부위 한 번 · 몸 목록 처음 나온 순 · 카드 강조 자리) · `card`(IL4 data-site 가장 아래 단 · IL6 약물 → 기기 → 숨김 · §4-7 status → slot) · `filter_site`(FS4 자손 포함) · `cart_item`(CT2 + OP3 드롭다운 = single · 판매 종료 상품 / 옵션 뺌 · option_refs 순서 · 원본 제목 · 정가 · 이벤트가) |
| `templates/partials/main.html` | 시안 배치: 드로어 \| `cs-left`(얼굴 + `marks` · 진료항목 `items`) \| **`cs-right`**(`header.cs-top` 「상담 · 명동점 · 담은 시술 + 수」 + `cs-chat`) \| 패널 · 뒤에 dialog 둘 |
| `templates/partials/items.html`(새) | `#procedure-list` — `cs-kinds__sum` · `details.cs-kind`(첫 묶음만 open) · `article.cs-pcard`(data-code · kind · site · device · status · points · body-sites) · 「시술설명」 · 「담기 / 담김」 · 빈 목록 `items-empty` · 같은 조각 안 `#face-marks` `hx-swap-oob` |
| `templates/partials/marks.html`(새) | `#face-marks` — `circle.cs-dot`(data-site-code · role=button · `hx-get /c/<id>/items?site=` · 다시 누르면 `site` 없이 = 풂) · `.cs-labels` 몸 목록(`ms-chip cs-label data-region="body"` · 머리 `body-sites-title`) |
| `templates/partials/cart.html` · `cart_item.html`(새) | 시안 `dialog#cs-cart` 그대로(머리 · 시술 목록 · 빈 줄 「담은 시술이 없어요」 · 최저가 추천 스켈레톤 `CHAT_REC_MAX` 개 · 「모두 비우기」 · 「저장」 disabled) · 진료항목 줄 = 시안 `li.cs-cart__item` + 「옵션 추가 +」(`cs-cart__opt-add`) → `select.cs-cart__opt-select` + 「추가」(OP2 · OP3 · OP5 single 0 이면 단추 없음) |
| `templates/partials/modal.html`(새) | 시안 `dialog#cs-proc-modal` 그대로(탭 넷 · dl 칸 여섯 · 「게시됨」 · `figure.cs-pm__fig` 둘 = 「시술 원리」 · 「시술 방법」 태그 자리 · 효과 · 부작용 ul · 「닫기」 · 「담기」) · 빈 자리 `pm-empty` · `pm-effect-course`(hidden) · **img 0 · 허브 글 0**(WP-4) |
| `templates/partials/drawer.html` | 「+ 새 대화」 글자(시안 · F1 — `data-slot="drawer-new-label"` 그대로) |
| `templates/partials/turn.html` | 줄기 받는 자리 `list` · `sites` → **`items` 하나**(§4-9 — 0.4 `list` · `sites` 는 장부에만) |
| `clinic_chat/consult/static/consult.js` | 시안 동작 꼴(줄 925 ~ 1083 · 의학 예시 상수 `INFO` · `COMMON_*` 안 옮김): 카드 누름 강조 · `g.cs-pick` 링(data-points) · 몸 이름 `is-pick` · 모달 `$J` 칸 채움 · 목차 탭 · 장바구니 드로어(담기 · 빼기 · 비우기 · 저장 표시 · 수 배지 · is-bump) · 「옵션 추가 +」 열기. 글자는 data-on / off / save / saved(한글 0) |
| `clinic_chat/consult/render.py` | `txt`(ui_text) · `rec_max` 전역 · `page(iv=, cart=)` · `items()` · `cart_item()` |
| `clinic_chat/consult/server.py` | 페이지 = 마지막 장부 `items.codes` 로 왼쪽 그림 · **`GET /c/<id>/items?site=`**(FS4 · 없는 부위 404 · 장부 줄 0) · **`GET /c/<id>/cart/item?code=`**(RT1 — 쿼리 값 · `$J` 에 정확히 있을 때만 · 없으면 404 · 상태 없음 — 서버 장바구니는 WP-5) |
| `clinic_chat/consult/ledger.py` | `Conv.last_items()` |
| `clinic_chat/consult/fake_turn.py` | `list` · `sites` 대신 **`items` 이벤트**(목록 + 점 · 몸 oob) · 장부 `items{codes}`(0.4 `list` · `sites` 칸도 남김) · 가짜 감지 = KOS 시술 이름 포함 · 없으면 앞 묶음 셋 · 말에 `empty` 면 0 |
| `tests/test_v05_page.py`(새) | 17 시험 |
| `tests/test_consult_page.py`(0.4 · 고침 둘) | ① T24 `SLOTS`: `list-empty` · `face-empty` → `items-empty` + 모달 빈 자리 2(화면이 바뀐 만큼) ② E0 가짜 턴 줄기: `list` · `sites` → `items`(그 밖 단언 그대로) |

## 2. 시험

| 명령 | 결과 |
|---|---|
| `.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_v05_page.py` | **17 passed** — 시안 글자 = ui_text(+ dict 메서드 이름 함정) · 시안 틀 자리(cs-right · cs-top · dialog 둘 · 탭 넷 · data-pm 칸 · 스켈레톤 수 · 저장 disabled) · `CHAT_REC_MAX` · 빈 목록 · 빈 slot · 묶음 순서 · 카드 값(IL4 · IL6 · U-23 · status slot) · 점 좌표 · pair · 몸 목록 순서 · 조각 마크업 · 이스케이프 · 가짜 턴 `items` 이벤트 · 장부 codes · 새로 고침 유지 · 이름 일치 · 빈 목록 · FS4(자손 · 풂 · 404) · RT1(`+` · 공백 · 한글 · `--` · 날 `+` 함정 404) · 드롭다운(판매 종료 뺌 · single 만 · OP5) · 실물 v3(RT1 코드 여섯 · 324 / 131 · 얼굴 32 전부 point / pair · 좌표 범위) · 장부 가격 0 |
| 위 + v05_kos_map + 0.4 관련 15 파일(`test_consult_{page,chat_ui,sites,turn,ledger,prompt}` · `test_v03_{sites,frame,start,fixes,prompt}` · `test_v04_{turn,ledger,start}` · `test_state_blanks`) | **166 passed**(마지막 7 번 연속) |
| `ruff check` 손댄 py 9 · `ruff format` 새 py 2 | 통과 |

- **흔들림 관찰**: 같은 묶음을 10 번 돌려 2 번(「2 failed · 52 errors」 · 「3 failed · 1 error」) 깨졌고 다시 못 냈다(그때 기계 load 9 ~ 11 · 다른 워커 동시). 0.4 시간 민감 시험(가짜 CLI 시간 초과류)로 보이나 원인은 못 잡았다 — WP-7 전체 pytest 때 다시 본다.
- 전체 pytest 는 안 돌림(D-8).

## 3. 스크린숏(`$W/wp2-shots/` · 1440 × 900 · 실물 v3 + 가짜 턴 「보톡스」 · 18298)

| 파일 | 무엇 | 시안 대조 |
|---|---|---|
| `01-first.png` | 첫 화면 — 가짜 턴 뒤(진료항목 23 종 106 개 · 얼굴 점 24 · 몸 목록 8) | `design-01-first.png` 와 같은 자리 · 글자 · 클래스(드로어 · 얼굴 카드 · 「감지된 시술 n종 · 진료항목 n개」 · 첫 묶음 펼침 · 카드 · 상단 「상담 명동점 · 담은 시술 0」 · 채팅 · 입력) |
| `02-expanded.png` | 둘째 묶음 펼침 + 카드 누름(강조 테 · 눈가 점 링) | 시안 pick 꼴 |
| `03-cart.png` | 담기 둘 → 장바구니 드로어 · 「옵션 추가 +」 → 드롭다운 + 「추가」 | `design-03-cart.png` 와 같은 자리(머리 「명동점 상담 / 담은 시술 2」 · 시술 목록 · 최저가 추천 스켈레톤 2 · 「모두 비우기」 · 「저장」) + 옵션 자리(시안 밖 · D-15) |
| `04-modal.png` | 「시술설명」 → 모달(탭 넷 · 개요 칸 여섯 · 게시됨 · 설명 「시술 원리」 · 「시술 방법」 태그 · 효과 · 부작용 · 「닫기」 · 「담김」) | `design-04-modal.png` 와 같은 자리 · 글자 · 클래스 — 허브 글 · 그림은 빈칸(WP-4) |
| `05-site-filter.png` | 얼굴 점 누름 → 그 부위 진료항목만(4) · 누른 점 표시 | FS4(시안에 없는 동작) |
| `06-empty.png` | 감지 0 → 빈 목록(`items-empty` 빈칸) · 점 0 | IL9 |
| `design-01-first.png` · `design-03-cart.png` · `design-04-modal.png` | 시안을 같은 크기로 찍은 것(대조용) | — |

다시 읽기 확인: 새로 고침 뒤 카드 106 · 점 24 · 몸 목록 「겨드랑이 · 손 · 목 · 전신 · 발 · 승모근 · 종아리 · 앞허벅지」 그대로. 콘솔 오류 = `/favicon.ico` 404 하나(0.4 부터).

## 4. 시안과 다른 점(이유)

| # | 다른 점 | 이유 |
|---|---|---|
| G1 | 예시 값(진료항목 · 대화 · 답 글)이 다름 | IL4b — 가짜 턴 · 실물 `$J` 값 · FAIL 아님 |
| G2 | 모달 개요 글 · 원리 / 방법 글 · 그림 · 효과 · 부작용이 빈칸 | WP-4(허브 조각 · 그림 서빙) · 시안 예시 글 · `INFO` · `COMMON_*` 은 옮기지 않음(ST4) |
| G3 | 몸 목록 칩이 얼굴 그림 아래쪽 목 · 어깨 선에 겹쳐 놓임(행 둘일 때) | 시안에 몸 목록 예시가 없어 0.4 `.cs-labels`(카드 바닥 고정) 꼴을 그대로 씀 · 「•」 는 CSS `::before` · 자리를 옮길지 사용자 · 코디 판단 |
| G4 | 장바구니 담기 · 빼기 · 저장은 **화면 안에서만**(새로 고침이면 비워짐) | 서버 장바구니 · 장부 `cart` · 옵션 줄 넣기 · 최저가 = WP-5(D-15). 줄 조각만 서버(`/cart/item`)가 그림 |
| G5 | 「옵션 추가 +」 · 드롭다운 · 「추가」 · 옵션 줄 자리 | 시안 밖 · 사용자 문구(D-15) · 클래스 `cs-cart__opt-add` · `cs-cart__opt-select`(스펙 제안) + `cs-cart__opts` · `cs-cart__opt-list` · `cs-cart__opt-pick`(새) · 드롭다운 글 = 「옵션 제목 정가[price-unit] [opt-event-mark]이벤트가[price-unit]」(`<option>` 안이라 slot 은 값만 · 속성 자리 없음) |
| G6 | 시안에 없는 클래스 · 속성 | `cs-pcard__status`(상태 표지 자리) · `data-status` · `data-points` · `data-body-sites` · `data-published` · `.cs-label.is-pick`(FS3 제안) · `data-region="body"` · `data-site-filter` · CSS 11 줄 |
| G7 | 시안 `.cs-artifact-root` 감싸개 없음 | 시안 미리보기 전용 |
| G8 | 화면 글자를 템플릿이 아니라 `ui_text.json` 에서 읽음 | 0.4 T17(코드 · 템플릿 한글 0) — 글자는 시안 그대로 |
| G9 | **실제 턴(0.4 `run_turn`)은 아직 `list` · `sites` 를 보내고 받는 자리가 없다** → 실제 대화에서는 WP-3 전까지 왼쪽 목록이 안 바뀐다 | 화면은 `items` 하나(§4-9) · 감지 → `items` 는 WP-3 |

## 5. slot 대조(§12 — 26)

| slot | WP-2 자리 |
|---|---|
| 0.4 부터 일곱(`face-title` · `list-title` · `chat-title` · `drawer-list-title` · `drawer-toggle-label` · `input-placeholder` · `send-label`) | 있음(시안과 같은 자리) |
| `body-sites-title` | 있음(몸 부위가 있을 때 `.cs-labels` 머리) |
| `items-empty` | 있음(IL9) |
| `status-product-check` · `status-procedure-check` · `status-bbl-filter` · `status-not-hub` | 있음(카드 `cs-pcard__status` — 그 status 카드에만) |
| `pm-empty` · `pm-effect-course` | 있음(모달 · hidden — 켜는 것은 WP-4) |
| `price-unit` · `opt-event-mark` | 값만(드롭다운 `<option>` 글 안 · data-slot 속성 자리 없음) · 추천 카드 쪽은 WP-5 |
| `pm-fig-missing` · `fig-alt` | WP-4(img 를 그릴 때) |
| `rec-tag-event` · `rec-no-price` · `rec-total` · `rec-comp-unit` · `rec-list-price` · `rec-no-pick` | WP-5(추천 카드 값) |

- 셈 메모: §12 는 「새 slot 19」 라 적었지만 나열된 이름은 **18**(status 넷 포함)이다 → 합 25. 스펙 셈 한 줄 고침 거리(코디).
- 0.4 의 `list-empty` · `face-empty` · `label-area-title` 은 0.5 화면에서 빠졌다(0.4 `list.html` · `sites.html` 조각은 `/c/<id>/list` · `/face-check` 용으로 남김).

## 6. 다음 WP 메모

- WP-3: `run_turn` 이 감지 결과로 `push("items", r.items(iv_mod.view(kos, codes), conv_id))` + 장부 `items{codes, …}` 를 내면 화면 · 새로 고침이 그대로 붙는다(`Conv.last_items`). 0.4 `list` · `sites` 이벤트는 지금 받는 자리 없음.
- WP-4: 모달 = `dialog#cs-proc-modal` 안 `data-pm` · `data-pm-list` · `data-pm-fig`(figure 둘)를 `GET /c/<id>/item?code=` 조각으로 채움 · `consult.js` `openModal` 에서 부르면 됨.
- WP-5: `/cart/item` 조각 · `data-cart-*` · `data-opt-*` 자리 그대로 서버 장바구니(`POST /c/<id>/cart`)로 바꾸고 consult.js 의 화면 안 `cart` Map 을 걷어낸다 · 추천 카드는 `[data-rec]` 안.
