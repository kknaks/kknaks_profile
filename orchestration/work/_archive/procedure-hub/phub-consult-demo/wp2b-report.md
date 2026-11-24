# WP-2 추가분 + WP-2 검수 P2 리포트 (app 워커 · 2026-11-20)

발주 `task_9836cf3185a0` · `ctx_d7045907a6b0` · SPEC-010 0.2.6 §4-3 IL11 · §4-9 `POST /c/<id>/topic` · §12 slot 둘 · §13 WP-2 「추가분」 · 검수 `review-wp2.md` P2 ① ~ ⑦. 커밋 0 · push 0 · 18222 손 안 댐(pid 64439 그대로) · 확인 서버 18298(끝에 내림). 주제 **화면 틀**만이다. 주제 규칙(TP2 ~ TP14)은 WP-3 이다.

## 1. 바뀐 파일

| 파일 | 무엇 |
|---|---|
| `templates/partials/items.html` | 묶음 마크업을 매크로 `kinds_block` 으로 뺐다. **IL11**: 주제가 둘 이상이면 `div.cs-topics` 안에 지금 주제(`details.cs-topic[data-topic-current][open]` · 머리 = 빈 slot `topic-current-mark` + `span.cs-topic__name` 안에 조건 이름마다 `span.cs-topic__cond`(잇는 글자 0) + `cs-topic__n` + `cs-topic__chev` · 안 = 시안 `cs-kinds` 그대로)를 둔다. 그 아래 빈 slot `topic-prev-title` 한 번, 앞 주제들(접힘 · **머리만** · `data-topic-switch` · `hx-post="/c/<id>/topic"` · `hx-vals='{"id": …}'`)이 온다. 주제가 하나면 주제 머리 없이 `cs-kinds` 바로(시안 그대로) |
| `clinic_chat/consult/items_view.py` | `cond_names`(머리 글 = 칸 순서 시술 → 부위 → 고민 → 효과 → 제품 → 국가 · 원문 이름) · `topics_view`(지금 주제 맨 위 · 앞 주제는 `created_turn` 역순 · `CHAT_TOPIC_MAX` 까지 · 점 · 몸 목록 = 지금 주제 진료항목(TP9) · `n` = 주제에 저장된 진료항목 수(TP12)) · `face_sites`(FS6) |
| `clinic_chat/consult/static/consult.css` | `cs-kind*` 규칙 10 줄에 `cs-topic*` 선택자를 붙였다(**같은 값을 물려받음** · 새 값 0). 덧붙인 것: `cs-topic__name` 간격 · 빈 slot 숨김 · 접힌 주제 body 숨김 · `/face-check` `$J` 점(`cs-dot--kos` 빨간 테) · 패널 한 줄 |
| `clinic_chat/consult/server.py` | **`POST /c/<id>/topic`**(form `id` · 그 대화 마지막 주제 목록에 있을 때만 · 없으면 404 · 장부 줄 `topic_switch` · 응답 = 목록 + 점 · 몸 목록 oob) · 페이지 = 마지막 `consult.topics` 가 있으면 `topics_view` · 패널 전역 `kos_check`(P2-1) · `/face-check` 에 `$J` 점(P2-2) |
| `clinic_chat/consult/ledger.py` | `Conv.last_topics()`(마지막 맺는 줄 `consult.topics` · `active_topic`) · `Conv.topic_override` · `Ledger.topic_switch()`(줄 `{phase: "topic_switch", topic_id, at}`) · 다시 읽기 때 맺는 줄 뒤 `topic_switch` 가 `active_topic` 을 덮는다(TP10 · r6 P2-3) · 새 맺는 줄이 오면 덮기를 푼다 |
| `clinic_chat/consult/fake_turn.py` | **가짜 주제**: 감지가 있으면 턴마다 새 주제 하나(id `t<n>` · 조건 = 감지된 KOS 시술 이름 앞 둘을 시술 칸에) · 앞 주제는 남고, 감지가 0 이면 주제를 그대로 둔다 · `items` 이벤트 = `topics_view` · 장부 `consult{topics, active_topic}`(TP10 칸 이름). 가짜 감지 · 가짜 주제는 화면 틀 확인용이다 |
| `clinic_chat/config.py` · `.env.example` | `CHAT_TOPIC_MAX`(6 · TP11) |
| `templates/partials/state.html` | P2-1 — 패널(`CHAT_DEBUG_PANEL=on`)에 `kos_map <sha 8> · made_at · hub_gold_hash <8> · hub <8> · hash_mismatch <값>` 한 줄(`data-kos-hash-mismatch` · 문구 0) |
| `templates/face_check.html` · `render.py` | P2-2 — `$J` 얼굴 32 부위 점(빨간 테 · 코드)을 옛 좌표표 점 위에 나란히 그린다 |
| `templates/partials/cart.html` · `consult.js` | P2-4 — 「저장」 을 `data-cart-save-wip disabled` 로 늘 막았다. JS 가 켜지 않고 「저장했어요」 도 띄우지 않는다(WP-5 가 서버 저장과 함께 푼다) · 앞 주제 머리 누름 때 `details` 펼침 막음(htmx POST 만) |
| `templates/partials/cart_item.html` | P2-6 — 부위가 비면 머리 = 「시술」 만(` · 부위` 는 부위가 있을 때만 · 잇는 글자는 시안 것) |
| `tests/test_v05_page.py` | 15 → **24** 시험(아래) |

## 2. 시험

| 명령 | 결과 |
|---|---|
| `.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_v05_page.py` | **24 passed** — 앞 15 + 시안 파일 대조(P2-7) · `cond_names` 순서 · `topics_view`(순서 · 지금 주제 안 · 점 · 몸 = 지금 주제 · max · active 없음 · 하나면 머리 없음) · 주제 마크업(지금 펼침 하나 · 머리 slot · 조건 span · 수 · `topic-prev-title` 한 번 · 앞 주제 = 머리만 · hx-post · hx-vals · 칸 순서) · **가짜 턴 주제 둘 + `/topic` 라우트**(줄기 · 새로 고침 · 장부 `topic_switch` · 새로 고침 뒤 유지 · **재시작 뒤 덮기 유지** · 없는 id 404 · 없는 대화 404) · `CHAT_TOPIC_MAX` · 패널 한 줄(P2-1 · 패널 끄면 없음) · `/face-check` `$J` 점(P2-2) · 장바구니 머리 부위 빔(P2-6) |
| 위 + v05_kos_map + 0.4 관련 15 파일(WP-2 때와 같은 묶음) | **175 passed** |
| `ruff check` 손댄 py 7 · `ruff format --check` items_view · fake_turn · test_v05_page | 통과 |

- 0.4 시험은 이번에 고친 것이 없다. WP-2 때 0.4 `test_consult_page.py` 단언 둘을 고친 것은 그대로다.
- `fake_turn.py` 는 ruff format 을 돌려 파일 전체 꼴이 바뀌었다. 동작은 위 표의 것만 바뀌었다.

## 3. WP-2 검수 P2 ① ~ ⑦ 처리

| # | 지적 | 처리 |
|---|---|---|
| ① P2-1 | JS4 패널 표시 없음 | **고침** — `state.html` 한 줄(값만) · 시험 `test_panel_kos_line` |
| ② P2-2 | `/face-check` 가 `$J` 좌표를 안 보임(FS6) | **고침** — `$J` 얼굴 점을 빨간 테 + 코드로 나란히 그림 · 시험 `test_face_check_shows_kos_sites` · 스크린숏 `08-face-check.png` |
| ③ P2-3 | 실제 턴은 왼쪽이 안 바뀜 · 18222 재기동 주의 | **코드는 WP-3 몫(그대로)** — 0.4 `run_turn` 이 아직 `list` · `sites` 를 보낸다. **WP-3 전에는 18222 를 이 코드로 다시 띄우지 않는다**(`.env` `CHAT_KOS_MAP` 빠짐도 그대로) |
| ④ P2-4 | 「저장」 이 저장 안 하고 「저장했어요」 | **고침** — 늘 disabled(`data-cart-save-wip`) · JS 가 켜지 않음 · 시험 단언 |
| ⑤ P2-5 | 드롭다운 가격 ↔ PR1 | **코드 그대로**(OP3) — 발주대로 스펙 쪽에서 고친다. 0.2.6 PR1 문구는 아직 「장바구니 목록 줄에는 가격 칸 없음」 이다(코디 확인 거리) |
| ⑥ P2-6 | 부위 빈칸이면 「시술 · 」 | **고침** — 부위가 있을 때만 ` · 부위` · 시험 `test_cart_kind_without_site` |
| ⑦ P2-7 | 시안 글자 시험이 시안 파일을 안 읽음 · 리포트 수 | **고침** — 시안 정본(`$W/design-consult-20261120.html` · 없으면 skip)을 읽어 `DESIGN_TEXT` 35 개가 전부 들어 있고 「옵션 추가 +」 는 없음을 단언(`test_design_text_is_in_design_file`). 수 정정: WP-2 때 `test_v05_page.py` 는 **15** 였다(리포트의 17 은 틀림). 지금은 24 |

## 4. 스크린숏(`$W/wp2-shots/` · 1440 × 900 · 실물 v3 + 가짜 턴 「보톡스」 → 「리프팅」)

| 파일 | 무엇 |
|---|---|
| **`07-topics.png`** | 주제 둘 — **지금 주제(「온다리프팅 (바디) · 온다리프팅 (페이스)」 18 · 펼침 · 안 = KOS 시술 접기)** 아래에 **앞 주제(「겨드랑이다한증보톡스 · 눈가주름보톡스」 106 · 접힘 머리만)** · 얼굴 점 · 몸 목록 = 지금 주제 것(TP9). 목록 카드를 끝까지 내린 화면 |
| `07a-topics-top.png` | 같은 화면의 목록 맨 위(지금 주제 머리 · `cs-kinds__sum`) |
| `07b-topic-switch.png` | 앞 주제 머리 누름 → 그 주제가 맨 위 펼침 · 앞 지금 주제는 접힘(`POST /topic` · 장부 `topic_switch`) |
| `08-face-check.png` | `/face-check` — 옛 좌표표 점(파랑) + `$J` 점(빨간 테 · 코드) 나란히(P2-2) |

- 주제 머리 글은 조건 이름 span 만 있다(가짜 주제라 시술 칸에 KOS 시술 이름 둘). 지금 주제 표지 · 앞 주제 머리 꾸밈은 빈 slot 이라 화면에 글자가 없다.
- 01 ~ 06 은 WP-2 때 것이다. 주제가 하나인 화면이라 그대로 같다(주제 머리 없음).

## 5. slot 대조(0.2.6 §12 — 새 21 + 0.4 7 = 28)

WP-2 리포트 §5 의 표에 주제 둘을 더한다: `topic-current-mark`(지금 주제 머리 · 주제 둘 이상일 때) · `topic-prev-title`(앞 주제 묶음 위 한 번) — **둘 다 있음**. 그 밖 slot 의 자리는 WP-2 리포트 §5 그대로다(WP-4 둘 · WP-5 여섯 · 값만 둘).

## 6. 다음 WP 메모

- WP-3: 맺는 줄 `consult.topics[{id, conditions{procedure, site, concern, effect, product: [{code, name}], country}, items, created_turn}]` · `consult.active_topic` 을 쓰면 화면 · 새로 고침 · `/topic` 이 그대로 붙는다. `conditions` 칸 이름(영문 다섯 + `country`)은 이 판의 화면 꼴이므로 WP-3 이 다른 이름을 쓰면 `items_view.COND_ORDER` 를 맞춘다. `/topic` 은 지금 「지금 주제 바꾸기 + 장부 줄」 까지다. 조건 되살림 셈(TP3 1)은 WP-3 이 한다.
- 0.4 `Ledger._apply_end` 는 `consult.after` 로 객체를 세운다. 가짜 턴 `consult` 에는 `after` 가 없어 객체는 안 바뀐다(WP-3 실제 턴은 둘 다 씀).
