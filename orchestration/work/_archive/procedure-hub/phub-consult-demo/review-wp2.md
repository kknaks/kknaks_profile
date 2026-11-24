# 검수 — SPEC-010 WP-2 코드(화면 틀) · 2026-11-20

reviewer 워커 · 읽기만(수정 0). 대상은 `clinic_chat/phub-consult-demo` 미커밋 변경(WP-1 위 · 고친 파일 14 · 새 파일 11)이다. 기준은 SPEC-010 §4 · §12 · §13 WP-2 행, 시안 `design-consult-20261120.html`, 리포트 `wp2-report.md`, 스크린숏 `wp2-shots/` 다. 서버는 띄우지 않았다(스크린숏으로 대조) · 18222 손대지 않음.

## 판정 — **PASS**(P0 0 · P1 0 · P2 7)

WP-2 완료 조건 둘을 확인했다. 하나는 `test_v05_page.py` 통과, 다른 하나는 가짜 턴 화면이 시안과 같은 자리 · 글자 · 클래스인 것이다(01 · 03 · 04 스크린숏을 시안 같은 크기 사진과 대조 · 예시 값 차이는 IL4b 로 FAIL 아님). 화면 글자 35 개는 모두 시안에 있고, 시안 밖 글자는 사용자 문구 둘(「옵션 추가 +」 · 「추가」 — D-15)뿐이다. 새 자리는 빈 `data-slot` 이다. 아래 P2 는 다음 WP 에서 받거나 스펙에 한 줄 올리면 된다.

## 1. 다시 돌린 것

| 명령 | 결과 |
|---|---|
| `pytest -q tests/test_v05_page.py` | **15 passed**(리포트는 「17」 — 파일의 시험 함수는 15 · P2-7) |
| 위 + `test_v05_kos_map` + 리포트의 0.4 관련 15 파일 | **166 passed**(리포트와 같은 수) |
| `ui_text.json` 값 35 개를 시안 HTML 에서 셈(스크래치) | 시안 글자 35 개 전부 시안에 1 회 이상 · 「옵션 추가 +」 0 회(사용자 문구) · 「추가」 는 시안에도 있음 |
| 스크린숏 01 ↔ design-01 · 03 ↔ design-03 | 드로어 · 얼굴 카드 · `cs-kinds__sum` · 첫 묶음 펼침 · 카드(약물 칩 · 코드 · 「시술설명」 · 「담기」) · 상단 「상담 명동점 · 담은 시술 n」 · 장바구니 드로어(「명동점 상담 / 담은 시술 n」 · 「시술 목록」 · 「최저가 추천 담은 시술 조합 기준」 · 스켈레톤 2 · 「모두 비우기」 · 「저장」) 자리 같음 |

## 2. 계약 대조

| 계약 | 코드 | 판정 |
|---|---|---|
| §4-1 배치(드로어 · `cs-left` · `cs-right` = `cs-top` + `cs-chat` · dialog 둘) | `main.html` · `cart.html` · `modal.html` | 맞음 |
| FS1 점 = 목록 진료항목의 얼굴 부위 `points` × 590 · 1060 · 같은 부위 한 번 | `items_view.py:87-106` · 시험 `test_view_order_cards_dots_body` | 맞음 |
| FS2 몸 목록 = 이름 원문 · 처음 나온 순 · 머리 slot `body-sites-title` | `items_view.py:105-106` · `marks.html` | 맞음(자리 겹침은 리포트 G3 — 사용자 판단) |
| FS3 카드 누름 강조 `g.cs-pick` · 몸 `is-pick` | `consult.js`(data-points · data-body-sites) | 맞음 |
| FS4 `GET /c/<id>/items?site=` 자손 포함 · 다시 누르면 풂 · 없는 부위 404 · 장부 줄 0 | `server.py` `items_list` · `items_view.py:54-59` · 시험 `test_site_filter_route` | 맞음 |
| FS6 `/face-check` 를 `$J` 값과 나란히 | 그대로 옛 `all_dots()` | P2-2 |
| IL1 ~ IL9 · §4-7 status → slot | `items.html` · `items_view.py:15-51` | 맞음(IL4 data-site 가장 아래 단 · IL6 약물 → 기기 → 숨김) |
| §4-6 장바구니 드로어 · OP2 · OP3(single · 판매 종료 뺌 · 원본 제목 · 정가 · 이벤트가 · slot `price-unit` · `opt-event-mark`) · OP5 | `cart_item.html` · `items_view.py:130-152` · 시험 `test_cart_item_options` | 맞음(서버 장바구니 · 옵션 줄 넣기는 WP-5) |
| §4-5 모달 빈 틀(탭 넷 · 칸 · figure 둘 · img 0 · 허브 글 0) | `modal.html` · 시험 `test_page_has_design_frame` | 맞음 |
| `items` 이벤트 · 받는 자리 하나 | `turn.html:13` · `fake_turn.py` · 시험 E0 고침 | 맞음 |
| RT1 코드는 쿼리 값 · 정확히 있을 때만 | `/cart/item?code=` · 시험(`+` · 공백 · 한글 · `--` · 날 `+` 404) · 실물 여섯 | 맞음 |
| 장부 가격 숫자 0 | 장부 `items{codes}` 만 · 시험 `test_ledger_has_no_prices` | 맞음 |
| 0.4 회귀 | `test_consult_page` 두 곳만 고침 — T24 slot 목록(`list-empty` · `face-empty` → `items-empty` + 모달 2 · 화면이 바뀐 만큼) · E0 줄기 `list` · `sites` → `items` | 고친 까닭이 스펙(§4-9 · IL9)과 맞음 · 나머지 166 통과 |
| 코드 · 템플릿 한글 0(0.4 T17) | 화면 글자는 `ui_text.json` · JS 한글은 주석뿐 | 맞음 |

## 3. 지적

### P2-1 JS4 패널 표시가 아직 없다
- `server.py:240` 의 주석은 「패널 자리는 WP-2」 인데, `templates` 어디에도 `kos_check` · `hash_mismatch` 가 없다(grep 0). WP-1 이 미룬 것이 WP-2 에서도 빠졌다.
- 고칠 방향: `CHAT_DEBUG_PANEL=on` 일 때 `state.html` 에 `app.state.kos_check`(sha 앞자리 · made_at · hub_gold_hash · hash_mismatch)를 한 줄 그린다. 또는 코디가 WP-3 으로 넘기고 주석을 고친다.

### P2-2 `/face-check` 가 `$J` 좌표를 보이지 않는다(FS6)
- `server.py:232-233` — 옛 `face_coords` 의 `all_dots()` 만 그린다. FS6 은 「`$J` 값과 나란히 보여 주는 비교용」 이다.
- 고칠 방향: `kos.sites` 얼굴 32 를 같은 화면에 겹쳐 그린다(다른 색 · 코드 표시). WP-2 범위가 아니라면 남은 일 목록에 올린다.

### P2-3 실제 턴은 왼쪽이 바뀌지 않는다 — WP-3 전 18222 재기동 주의
- `turn.html:13` 은 이제 `items` 만 받는다. 0.4 `run_turn` 은 아직 `list` · `sites` 를 보낸다(리포트 G9). 그래서 이 코드로 18222 를 다시 띄우면 실제 대화에서 왼쪽 목록 · 점이 비거나 처음 값에 머문다(0.4 동작보다 후퇴). WP-1 때 적은 `.env` `CHAT_KOS_MAP` 빠짐도 그대로다.
- 고칠 방향: 코드는 WP-3 에서 고친다(리포트 §6 메모대로 `push("items", …)`). 코디 · 사용자는 **WP-3 전에는 18222 를 이 코드로 다시 띄우지 않는다.**

### P2-4 「저장」 이 저장하지 않고 「저장했어요」 를 보인다
- `consult.js`(diff 165 줄 근처 · CT7 주석) — 장바구니는 화면 안 `Map` 뿐이라 새로 고침이면 비는데, 단추는 시안의 「저장했어요」 를 띄운다. 사용자가 18222 에서 보면 저장된 것으로 오해한다.
- 고칠 방향: WP-5 가 서버 장바구니로 바꿀 때 함께 고친다. 그 전에는 저장 단추를 `disabled` 로 두는 편이 안전하다.

### P2-5 장바구니 드롭다운 가격과 스펙 §6-1 PR1 이 어긋난다(스펙 쪽)
- `cart_item.html` 의 `<option>` 글 = 옵션 제목 · 정가 · 이벤트가 숫자. 이는 OP3(D-15 · 사용자 결정 고침 4)대로다. 그런데 §6-1 PR1 은 아직 「가격이 보이는 자리는 최저가 추천 카드뿐 · 장바구니 목록 줄에는 가격 칸 없음」 이다.
- 고칠 방향: 코드는 그대로 둔다. 스펙 PR1 에 「장바구니 옵션 드롭다운 · 옵션 줄(OP3 · OP4)도 원본 가격을 보인다」 를 한 줄 더한다(코디).

### P2-6 장바구니 줄 머리가 부위 빈칸이면 「시술 · 」 로 끝난다
- `cart_item.html` 의 `{{ ci.kind }} · {{ ci.site }}` — 시안 `render()`(시안 줄 1065)와 같은 꼴이다. `site_tiers` 가 빈 진료항목(예 수액류)에서는 꼬리 「 · 」 만 남는다.
- 고칠 방향: `ci.site` 가 있을 때만 ` · {{ ci.site }}` 를 붙인다(잇는 글자는 시안 것 그대로).

### P2-7 시안 글자 시험이 시안 파일을 읽지 않는다 · 리포트 시험 수
- `tests/test_v05_page.py:25-61` 의 `DESIGN_TEXT` 는 손으로 적은 목록이다. 「`ui_text` = 이 목록」 만 보고, 목록이 시안에 있는지는 보지 않는다(이번에는 35 개 전부 시안에 있음을 따로 확인). 리포트 §2 「17 passed」 는 실제 15 다.
- 고칠 방향: 시험에서 시안 HTML(정본 경로가 앱 밖이면 `tests/` 고정 사본 또는 skipif)을 읽어 `DESIGN_TEXT` 의 각 값이 들어 있는지 단언한다. 리포트 수는 15 로 고친다.

## 4. 남은 것(지적 아님)
- **WP-2 추가분(SPEC 0.2.4 · 고침 7)**: IL11 주제 묶음(`details.cs-topic` · 머리 · 조건 이름 span · 앞 주제 머리만) · 가짜 턴 주제 둘 · `POST /c/<id>/topic` 틀 · slot `topic-prev-title` · `topic-current-mark` 는 이번 변경에 없다. 스펙대로 「WP-2 가 끝난 뒤 덧붙임」 이므로 따로 발주하면 된다. 다만 r6 검수(주제 규칙 FAIL)가 닫힌 뒤가 좋다.
- 리포트 §5 의 slot 셈 메모(「새 19 라 적었지만 18」)는 0.2.5 에서 「새 21」(주제 slot 둘 더함)로 바뀌었다. 지금 문서 기준으로 다시 세면 된다.
- 리포트 §2 의 「흔들림 2/10」 은 이번 재실행 두 번에서는 나지 않았다. WP-7 전체 pytest 때 다시 본다는 리포트 메모 그대로 둔다.
