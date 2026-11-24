# WP-5 리포트 — 장바구니 옵션 줄 · 최저가 (app 워커 · 2026-11-20)

발주 `task_257fa9f69c1d` · `ctx_bfdb9ed15431` · SPEC-010 0.2.7 §4-6 CT1 ~ CT8 · OP1 ~ OP8 · §6 PR · RC1 ~ RC10 · CO1 ~ CO4 · §6-3 · D-15 ~ D-17 · §13 WP-5. 기준은 `$J` 1af2216c 다. 커밋 0 · push 0 · 18222 손 안 댐(pid 64439 그대로) · 확인 서버 18295(끝에 내림).

## 1. 바뀐 파일

| 파일 | 무엇 |
|---|---|
| `clinic_chat/consult/price.py`(새) | 순수 함수 `recommend(kos, cart)`. **RC1** 단위 = 옵션 줄(진료항목 · 고른 옵션 count) · 줄 없는 진료항목 = `no_pick`(OP6) · 덮는 single 0 = `no_price`(RC6 — 옵션 0 · group 만) · 고른 옵션이 판매 종료이거나 그 진료항목을 안 덮으면 그 줄 = `closed_lines`(RC10). **RC2** 후보 ① 고른 옵션 그대로(0 원 · 회원권이어도) ② 같은 진료항목 · 같은 count 의 다른 single — 판매 종료 뺌 · CO1(0 원) · CO2(「1년권」 · 「가입비」) 뺌 · CO3(「[첫방문]」 · 「10월 첫방문 이벤트」) · CO4 둠 · 상품 제목 「남성」 / 「여성」 낱말이 같을 때만 ③ group — 판매 종료 뺌 · 장바구니 밖 진료항목을 품으면 뺌 · 구성 (진료항목, `compositions[].count`) 전부가 장바구니 옵션 줄에 있을 때만. **RC3** 집합 덮기(되짚기 · 겹침 0 · 같은 (c, n) 줄 둘이면 둘 다). **RC4 · RC5** 쓰인 가격 = 옵션 `event_price` 있으면 그것 · 없으면 정가 · 구성 줄 이벤트가는 안 씀 · 합계 · 정가 합계. **RC7** 카드 2 = 최저 · 두 번째(옵션 키 묶음이 다른 것 · 동점 = 옵션 수 → `$J` 순서). **RC9** 줄 > 10 · 조합 > 10,000 → 「고른 옵션 그대로」 카드 하나 + `capped`. **CO 셈** `filtered{CO1, CO2, CO3}` 은 규칙마다 따로 · `co_counts`(리포트용). `single_options` = 드롭다운(OP3) |
| `clinic_chat/consult/cart.py`(새) | 서버 장바구니: `apply(op = add · del · clear · line_add · line_del)` — 담기는 진료항목만(OP1) · 옵션 줄은 그 진료항목의 single 이고 판매 종료가 아닐 때만(OP3 · group · 다른 진료항목 옵션 · 장바구니 밖 = 422) · 같은 옵션 두 줄 가능(OP4) · 진료항목 빼면 줄도(OP7) · `$J` 에 없는 코드 404(RT1). `view`(드로어 값) · `rec_view`(카드 + 옵션 안 고름 · 가격 없음 이름) · 장부 꼴 `ledger_view` · `rec_ledger`(옵션 키 · 표지만) |
| `clinic_chat/consult/ledger.py` | `Conv.cart` · 장부 줄 **`cart{op, cart[{code, lines[[product_key, option_key]]}], rec{cards(옵션 키), no_pick, no_price, closed_lines, filtered, capped, combos}}`** · **`cart_saved{codes, best_keys}`** · 다시 읽기 = 마지막 `cart` 줄(CT6 — 새로 고침 · 재시작 뒤 같음). **가격 숫자 0**(JS6) |
| `clinic_chat/consult/server.py` | **`POST /c/<id>/cart`**(form `op · code · product_key · option_key · idx` · 코드는 폼 값 — RT1 · 응답 = 장바구니 몸 조각) · **`POST /c/<id>/cart/save`**(CT7 · 빈 장바구니 422) · 페이지가 그 대화 장바구니 · 추천을 그림 |
| `templates/partials/cart.html` · `cart_body.html`(새) · `cart_item.html` | 드로어 몸 = 조각(`#cs-cart-body`). 진료항목 줄(CT2) 아래 옵션 줄 `li.cs-cart__opt`(옵션 제목 · 정가 · 이벤트가 원문 · 지우기 `aria-label` = 옵션 제목). 「옵션 추가 +」 → `select` + 「추가」(single 0 이면 단추 없음 — OP5). 추천 카드 `.cs-rec__card` 2(§6-3 — tag 자리 = slot `rec-tag-event` · 합계 + 정가 합계(다를 때) · 옵션마다 상품명 · 옵션명 · 쓰인 가격 · group 이면 덮은 진료항목 이름). 줄이 없으면 시안 스켈레톤 그대로. 아래 「옵션 안 고름」(slot `rec-no-pick`) · 「가격 없음」(slot `rec-no-price`) 이름 목록. 숫자는 원본 그대로(쉼표 · 단위 = slot `price-unit`) |
| `clinic_chat/consult/static/consult.js` | 장바구니를 서버로: 담기 · 빼기 · 비우기 · 옵션 줄 넣기 · 지우기 = POST → 몸 조각 바꿈 → 수 배지 · 카드 「담기 / 담김」 · 모달 단추 · 저장 단추 맞춤 · 「저장」 = POST `/cart/save` + 시안 표시(「저장했어요」 0.9 초) |
| `clinic_chat/consult/static/consult.css` | 옵션 줄 · 카드 값 자리(15 줄 · 토큰만) |
| `tests/test_v05_price.py` · `test_v05_cart.py`(새) · `test_v05_page.py`(저장 단추 단언 1 줄) | 16 + 9 시험 |

## 2. 시험

| 명령 | 결과 |
|---|---|
| `.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_v05_price.py tests/test_v05_cart.py` | **25 passed**. price: RC4 · CO 규칙마다 따로 · RC2 다른 single 은 CO1 · CO2 뺌(CO3 첫방문 둠 · 이벤트가 · 정가 합계) · 고른 회원권 옵션은 그대로(C9d) · count 지킴 · **남성 / 여성 낱말**(C9b) · **group 조건**(구성 줄 전부 · (가) 줄 없음 → 후보 아님 · (나) count 다름 → 후보 아님 · 장바구니 밖 구성 → 뺌 · group 이벤트가 · 덮은 이름) · 같은 (c, n) 줄 둘 · 겹침 0 · RC6 가격 없음 · OP6 옵션 안 고름 · RC10 고른 옵션 판매 종료(고정본에서 `closed` 바꿈) · 다른 판매 종료 뺌 · 동점 순서 · RC9 줄 > 10 · 조합 한도 · 같은 group 키 한 번 · 고른 옵션이 그 진료항목을 안 덮으면 받지 않음 · 실물 CO 셈 · 실물 온다 + 티타늄 · 실물 C9 · C9b · C9c. cart: 담기 = 진료항목만 + 장부 · 같은 진료항목 한 번 · 옵션 줄 여러 개 · 같은 옵션 두 줄 · 줄 지우기 · 거절(group · 판매 종료 · 다른 진료항목 옵션 · 장바구니 밖 · 틀린 idx · 없는 코드 · 틀린 op) · OP5 단추 없음 + 가격 없음 · OP7 진료항목 빼면 줄도 · 비우기 = 스켈레톤 · group 카드 값 · 재시작 복원 · 저장(CT7) · **장부 가격 숫자 0** · 실물 RT1 코드 여섯 |
| 위 + v05 page · modal + 0.4 `test_consult_page`(T17) · `consult_ledger` · `v04_ledger` · `consult_chat_ui` · `v03_frame` · `v03_start` | **93 passed** |
| `ruff check` · `ruff format` 손댄 py | 통과 · 코드 한글 0(T17) |

## 3. 실물 v3 대조(카드 2 값 = `$J` 원본 `price_amount` · `event_price`)

| 장바구니(옵션 줄) | 카드 1(최저) | 카드 2 | 원본 대조 |
|---|---|---|---|
| **S1 single 만** — 아발란체 제모(겨드랑이) 26-Avalanche-1 · 여성 1 회(P113-3) + 여성 5 회(P113-4) | 200,000(정가 같음) = 여성 겨드랑이 1 회 50,000 + 5 회 150,000 | 없음(같은 회차 · 같은 낱말 다른 single 0) | P113-3 정가 50,000 · P113-4 정가 150,000 · 이벤트가 없음 |
| **S2 group 이 덮는 쌍** — 울쎄라피 프라임 26-USPP-300SHOT(P123-2 정가 1,300,000) + 써마지 FLX 26-THM3-600SHOT(P111-2 정가 2,200,000) | **2,790,000**(정가 5,000,000) = 「[11월 이벤트] 울쎄라피프라임300샷+써마지600샷」(P016-1 · group · 덮음 = 울쎄라피 프라임 · 써마지 FLX) | **3,050,000**(정가 3,800,000) = 「[첫방문] 울쎄라피 프라임 300샷」 850,000(정가 1,600,000 · CO3 둠) + 써마지 FLX 600샷 2,200,000 | P016-1 정가 5,000,000 · event 2,790,000 · P077-2 정가 1,600,000 · event 850,000. 「[오픈] 울써마지 300샷」(P052-1 — 써마지 300샷 구성)과 「[오픈] 울써마지 600샷」(P053-1 — 울쎄라 600샷 구성)은 장바구니 밖 구성이라 후보 아님 · 가입비 0 원(CO1 · CO2) · 블랙 / 플래티넘 회원가(CO2) 3 은 빠짐 |
| **S3 「[11월 이벤트] 온다50kj+티타늄30kj」 구성 둘** — 온다리프팅 얼굴 26-DRPTP-OND-50KJ(P121-6 정가 400,000) + 티타늄리프팅 26-TTNLF-SPRNT-30KJ(P136-3 정가 500,000) | **590,000**(정가 1,100,000) = P015-1 group(덮음 = 온다리프팅 얼굴 · 티타늄리프팅 · **구성 줄 이벤트가 590000 반복 값은 안 씀**) | **630,000**(정가 800,000) = 온다 [FACE] 5만줄 400,000 + 「[첫방문] 티타늄 30kJ」 230,000(정가 400,000) | P015-1 정가 1,100,000 · event 590,000 · P081-1 정가 400,000 · event 230,000. 「My Pick 티타늄40KJ」(P038-3 — 구성에 장바구니 밖 10KJ 추가) · 「[오픈] 온타늄」(P050-1 — 구성 온다 30kJ) 은 후보 아님 |

- C9c: 써마지 FLX 600샷(정가 2,200,000)만 고르면 다른 후보 0 → 카드 하나(가입비 0 원 · 블랙 490,000 · 플래티넘 890,000 회원가가 빠짐 · `filtered` CO1 1 · CO2 3).
- **CO 셈(`$J` 전체 · 규칙마다 따로)**: CO1 **13** · CO2 **22** · CO3 **23** · CO1 ∩ CO2 **10** · 거름 합집합(CO1 ∪ CO2) **25** — 스펙 실측 기대와 같다.

## 4. 장부 가격 숫자 0(grep)

확인 서버 장부(`wp5chat/turns.jsonl` — `cart` 6 줄 + `cart_saved` 1 줄)를 `590000|1100000|400000|230000|500000|800000|630000|price_amount|event_price|"total"` 으로 grep → **0 건**이다. 줄에는 진료항목 코드 · 옵션 키 · 표지만 있다. 예: `cart_saved{codes[4], best_keys: [["P015", "P015-1"]]}`.

## 5. 스크린숏(`$W/wp5-shots/` · 1440 × 900 · 실물 v3)

| 파일 | 무엇 |
|---|---|
| `01-items-no-option.png` | 진료항목 넷 담음(온다 · 티타늄 · 아발란체 · BBL HERO 1 모드) — 옵션 줄 0 · 추천 칸 스켈레톤 |
| `02-option-dropdown.png` | 온다 줄 「옵션 추가 +」 → 드롭다운(single 원문 · 정가 · 이벤트가) + 「추가」 |
| `03-option-line-added.png` | 옵션 줄 「[FACE] 온다 5만줄(50kJ) 400000」 이 붙음(지우기 단추) |
| `04-rec-cards.png` | 티타늄 줄도 넣은 뒤 **최저가 카드 2**: 590000 / 1100000(group · 덮은 이름 둘) · 630000 / 800000(온다 + 첫방문 티타늄) · 아래 이름 둘 |
| `05-no-pick-no-price.png` | 추천 칸 아래: **옵션 안 고름** = 아발란체 제모(겨드랑이) · **가격 없음** = BBL HERO (1가지 모드)(group 만) — 머리 글은 빈 slot |
| `06-saved.png` | 「저장」 → 「저장했어요」(장부 `cart_saved`) |

페이지 오류 0 · 수 배지 4 / 4.

## 6. 스펙과 다른 점 · 남은 것

| # | 무엇 | 제안 |
|---|---|---|
| P1 | 고른 옵션이 그 진료항목을 덮지 않으면(키가 틀림) 받지 않는다 — 판매 종료와 같이 `closed_lines` · 옵션 안 고름(실물 확인 중 잘못된 키로 발견 · 라우트는 이미 422) | RC10 에 한 줄 |
| P2 | 「옵션 안 고름」 · 「가격 없음」 머리 slot 이 빈칸이면 두 목록이 화면에서 구별되지 않는다(이름만 bullet) | §12 slot 문구를 사용자가 채움 |
| P3 | 「이벤트 표지」 tag 는 slot `rec-tag-event` 빈칸이라 지금 화면에 안 보인다(자리 · 장부 표지는 있음 · 첫방문도 표지 대상) | 사용자 문구 |
| P4 | 금액 글꼴 | 원본 숫자 그대로(쉼표 0 · 단위 slot 빈칸 — PR2) |
| P5 | WP-2 임시 라우트 `GET /c/<id>/cart/item` 은 남아 있다(조각 확인용 · JS 는 안 씀) | WP-7 정리 때 지울지 결정 |
| P6 | 회차 · 대상 축(AX2 · AX3) — 장바구니 옵션 안 고른 진료항목 값 넣기 | WP-6 블록과 함께(지금은 `ask_axis` 자리만) |
