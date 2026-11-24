# 로컬 테스트 고침 A 리포트 — 얼굴 점 · 진료항목 목록 (app 워커 · 2026-11-22)

발주 `task_7175be45c1de` · `ctx_9bd9bdbd6fed` · 사용자 승인 11-22 「a 만 하자」 · A 1 ~ 7 만(효과 · 부작용 · 침샘 계층 · 장바구니 문구 · 묶음 가격 0). 커밋 0 · 서브에이전트 0 · 18222 손 안 댐(지금 pid 84686 — 내가 띄우거나 끈 것 아님) · 실물 확인 = 빈 포트 18294(실제 이해 · 답 호출 · 끝에 내림).

## 0. 코디가 18222 재기동 때 쓸 값

| | 전 | 후 |
|---|---|---|
| `$J` 파일 | `myeongdong-mapping-20261120-v3.json`(같은 이름 덮어씀 · 두 경로) | 같음 |
| sha256 | `1af2216c5a3ed2806936777314ad4fbdc1ca8e70b78fee99ad387ac5f0e26568` | **`8f4e63935ee1995cc5ae83cd5eb5fa3da2bc96ed554d3264101ea485dd9dd131`** |
| sites | 71(얼굴 32 · 몸 39) | **92(얼굴 53 · 몸 39)** |
| 경로 | `/Users/kknaks/git/clinic_chat/data/kos/` · `$A/data/kos/` | 두 곳 같은 sha |

- `CHAT_KOS_MAP_SHA` 를 쓰고 있으면 새 sha 로 바꿔야 시작한다(JS3).
- 옛 파일 사본: `/private/tmp/claude-501/-Users-kknaks-orca-workspaces-clinic-chat-phub-consult-demo/a6af7bd8-5374-42fc-854f-496eb6878c39/scratchpad/fixA-backup/v3-1af2216c.json`(스크립트 원본도 같은 폴더).

## 1. 바뀐 파일

| 파일 | 무엇 |
|---|---|
| `$P/reference/2026-11-19-myeongdong-kos/build_mapping_json_v3.py` | A-7 `widen_sites` — v2 sites + **얼굴 좌표표 부위 전부**(face_coords.py 의 점 꼴 point · pair + v2 대표점 `REP_FACE` 7 + `NEW_FACE`) + **silver `concern_site.csv` 의 얼굴 부위** + 그 조상. 칸 꼴 · `source` 는 v2 와 같은 규칙(기존 좌표 그대로). meta `sites_rule` 한 줄 · 끝에 셈 출력 |
| `clinic_chat/consult/items_view.py` | A-1 · A-2 · A-3 · A-5 — `belongs`(진료항목 매핑 부위가 점 부위를 품는가 = 같음 · 조상) · `dots_of`(점 = 주제 `sites` · 얼굴 = 점 · 몸 = 목록) · `filter_site` = `belongs` · `card_sites` = 속한 점 · `view(sites=)` · `topics_view` 가 지금 주제 `sites` 를 넘김 · **진료항목 부위를 모아 찍던 길은 지움** |
| `clinic_chat/consult/detect.py` | A-4 — 고민의 「케이스 직접」 행마다 `case_site`(행 `site_code` → 비면 `case_site_name` 과 이름이 같은 `$J` 부위 · 이름이 겹치면 안 씀) · `same_procedure_scope`(그 시술 · 매핑 부위가 케이스 부위를 품는 진료항목)를 더함 · `Result.case_scope{케이스: {site, added[]}}` · A-1 `concern_sites`(응답 머리 `sites[]` 가운데 match 「직접」) |
| `clinic_chat/consult/turn.py` | A-1 · A-6 — `_add_sites`: 이번 턴 말한 부위 + 고민 부위를 **지금 주제 `sites` 에 쌓음**(지금 주제 조건에 남은 값만 — 막힌 값은 점 아님) · 장부 `consult.topics[].sites`(되살림 · 재시작 때 같이) · `items.case_scope` · `items.sites_added` |
| `clinic_chat/consult/static/consult.js` | A-6 — 질문을 보낼 때 거른 목록이면 전체 목록을 다시 받음(화면만) |
| `clinic_chat/consult/templates/partials/marks.html` | 머리 주석만(꼴 그대로 — 누른 점 `aria-pressed` · 같은 점 다시 = 전체는 원래 꼴) |
| `tests/test_v05_fix_a.py`(새) | 7 시험(아래) |
| `tests/test_v05_page.py` · `tests/test_v05_kos_map.py` | 옛 규칙 단언 고침: 점 = 진료항목 부위 → 대화 부위 · 거름 = 자손 → 품음 · 얼굴 32 → 53 · sites 71 → 92 |

## 2. 시험

| 명령 | 결과 |
|---|---|
| `.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_v05_fix_a.py` | **7 passed** |
| 위 + v05 전부 + 0.4 관련(`consult_page` T17 · `consult_prompt` · `v03_prompt` · `consult_material` · `consult_turn` · `v04_turn` · `v04_prompt` · `v04_ledger` · `consult_ledger` · `v03_frame` · `consult_chat_ui` · `v04_understand` · `v04_verify` · `state_blanks` · `consult_sites` · `v03_sites`) | **298 passed · 1 skipped** |
| `ruff check clinic_chat/consult/` + 손댄 시험 | 통과 · 코드 한글 0 |

`test_v05_fix_a.py` 각 시험:
- `test_belongs_same_or_ancestor`:
  - 얼굴 · 전신 진료항목은 팔자주름 · 턱 · 목 점에 속한다.
  - 턱 진료항목은 턱끝 점에는 속하지만, 팔자주름 · 얼굴 점에는 속하지 않는다.
- `test_dots_are_conversation_sites_not_item_sites`:
  - 대화 부위가 팔자주름뿐이면 점은 팔자주름 둘뿐이다. 얼굴 대표점 0 · 「전신」 0(사용자가 본 문제).
  - 대화 부위가 0 이면 점도 0 이다.
  - 같은 진료항목이 대화에 따라 다른 점에 붙는다.
- `test_click_filters_and_other_dots_stay`:
  - 턱을 누르면 턱 · 얼굴 진료항목만 남고, 다른 점(팔자주름 · 입)은 그대로다.
  - 누른 점만 `aria-pressed`. 같은 점을 다시 누르는 링크는 `?site` 가 없다(= 전체 목록).
- `test_items_route_filter_keeps_dots`: 서버 `GET /items?site=` 뒤에도 점 둘이 남고, 장부 턴은 그대로 2 다.
- `test_concern_adds_same_procedure_scope`:
  - 팔자필러(직접) + 얼굴필러(같은 시술 · 얼굴 ⊃ 팔자주름) + 얼굴 보톡스. 코필러 0.
  - 케이스 부위를 못 찾으면 직접 진료항목만. 고민 부위는 「직접」 만.
- `test_add_sites_accumulates_only_kept_values`: 막힌 값은 점이 아니고, 앞 점은 남는다.
- `test_turns_accumulate_dots_ledger_restart`(가짜 CLI · 가짜 허브 두 턴):
  - 장부 `topics[0].sites` = [턱] → [턱, 입].
  - 전신 범위 진료항목이 있어도 몸 점 0.
  - 새 턴 목록은 선택이 풀려 있다. 재시작해도 점 둘.

## 3. 목록 수 — 고민 → 같은 시술 범위(A-4 · 실물 허브 caa03560 + 새 `$J` · 칸 하나씩)

| 조건 | 전(케이스 직접만) | 후 | 더해진 것(KOS 시술 · 진료항목 부위) |
|---|---|---|---|
| **팔자주름**(고민 CON-009) | 23 | **52** | 풀페이스필러 6(얼굴필러 레스틸렌 · 레스틸렌 아이라이트 · 벨로테로 · 셀레스텔라 · 수입 · 쥬비덤 — 얼굴) · 스킨보톡스 6 · 주름보톡스 6 · 얼굴보톡스 4(풀페이스 · 시그니처 페이스앤넥 — 얼굴(+목)) · 올리디아120/365 · 스킨부스터 6 · 스컬트라 1(볼 케이스 CAS-1014 → 얼굴) — 모두 매핑 부위 「얼굴」 |
| **미간주름**(고민 CON-006) | 35 | **47** | 스킨보톡스 6 · 풀페이스필러 6(얼굴) |
| 턱 고민 — 자갈턱(CON-171) | 22 | 37 | 턱보톡스 5(턱) · 스킨보톡스 6 · 얼굴보톡스 4(얼굴) |
| 턱 고민 — 턱살(CON-168) · 턱근육 발달(CON-163) | 5 · 0 | 5 · 0 | 없음 |
| 미간(부위 SITE-015) · 턱(부위 SITE-072) | 120 · 142 | 120 · 142 | 부위 칸은 A-4 대상 아님(SF2 그대로) |

- 엉뚱 0 확인: 다한증 · 종아리 · 승모근 · 침샘보톡스 · 코필러 · 몸 부위 진료항목은 하나도 더해지지 않았다.
- 더해진 것은 모두 그 케이스와 같은 시술이고, 매핑 부위가 케이스 부위(팔자주름 · 미간 · 자갈턱(턱) · 볼)이거나 그 조상(볼 · 얼굴)이다.
- 케이스 부위는 허브 행 `site_code` 가 비어 있어, `case_site_name` 과 이름이 같은 `$J` 부위로 찾았다. silver 부위 이름 117 은 서로 겹치지 않는다(실측).

## 4. 실물(18294 · 대화 `fixAreal00000001`) — 「팔자주름 개선하고 싶어」 → 「미간도 신경 쓰여」 → 「턱은?」

| 턴 | 이해 대상 | 주제 · 목록 | 이번 턴 더한 점 | 주제 점(쌓임) |
|---|---|---|---|---|
| 1 | concern CON-009 팔자주름 + site SITE-046 팔자주름 | t1 first · **44**(고민 ∩ 부위 — 옛 규칙이면 23 쪽) | SITE-046 | 팔자주름 |
| 2 | concern CON-006 미간주름 + site SITE-015 미간 | t1 계속(A 39) · **39** — 고민 · 부위 칸 교체(CD2 · 원래 규칙) | SITE-015 | 팔자주름 · 미간 |
| 3 | site SITE-072 턱 | t1 계속(A 33) · **33** | SITE-072 | 팔자주름 · 미간 · 턱 |

- 사용자가 본 문제와 비교:
  - 「얼굴」 가운데 대표점 0 · 「• 전신」 0.
  - 팔자주름 자리에 좌우 점이 있다.
  - 목록에 필러(풀페이스필러) · 보톡스(스킨 · 얼굴 보톡스)가 있다.
- 점 누름(스크린숏 02 · 03):
  - 누른 점만 진하게 바뀌고 다른 점 둘은 그대로다. 같은 점을 다시 누르면 풀린다.
  - 이 대화의 목록 33 은 전부 얼굴 전체 진료항목(턱 부위 ∩ 미간주름 고민 → SF2 의 얼굴 전체)이다. 그래서 세 점 모두에 속해, 어느 점을 눌러도 33 이다(규칙대로).
  - 거름이 실제로 줄어드는 꼴은 아래 두 번째 대화로 확인했다.
- 카드 누름 강조(스크린숏 04 · 「볼뉴머 풀페이스」): 링 4 개 = 팔자주름 좌우 + 미간 + 턱(속한 점 전부).
- 답 글(꼬리 뗀 본문 · 「／」 = 문단):
  1. 팔자주름에는 주름을 채우는 방식, 콜라겐 생성을 자극하는 방식, 열로 당겨 올리는 방식, 실로 끌어올리는 방식 등 여러 갈래가 있어요. … ／ 명동점에는 이 고민으로 볼 수 있는 진료항목이 44개 있어요. … ／ 혹시 궁금한 시술이 있으세요? 예를 들면 올리디아, 소프웨이브, 슈링크 같은 게 있어요.
  2. 미간 쪽도 신경 쓰이시는군요. 팔자주름과는 별개로 미간주름 기준으로 볼게요. ／ … ／ 명동점에는 이 고민으로 볼 수 있는 진료항목이 39개 있어요. 앞서 보신 팔자주름 진료항목은 목록 아래에 남아 있어요. ／ …
  3. 턱 부위는 개요나 맞는 고민에 대해 안내해 드릴 수 있는 정보가 없어요. ／ 명동점 목록은 턱 부위와 미간주름 조건으로 바뀌어서 지금 진료항목이 33개 있어요. ／ …
  - 2 턴 「팔자주름 진료항목은 목록 아래에 남아 있어요」 는 실제와 다르다. 같은 주제 t1 안에서 고민 칸이 교체되었고, 앞 주제는 없다. 답 규칙 · 칸 교체 쪽 문제라 A 밖이다(보고만).

### 두 번째 대화(`fixAreal00000002` · 거름이 줄어드는 꼴)

「보톡스 맞고 싶어요」 → 「턱이랑 입꼬리요」 의 결과:
- 주제 점 = 턱 · 입꼬리, 목록 33.
- 턱을 누르면 **13**(턱 보톡스 + 얼굴 전체), 입꼬리를 누르면 **12**. 다른 점은 그대로다.
- 다음 턴: 입꼬리를 누른 채 「가격은 얼마예요?」 를 보내면, 보내는 순간 목록이 12 → 33 으로 돌아오고 눌린 점도 풀린다(A-6 · 브라우저 실측).

## 5. 스크린숏(`$W/e2e-shots/` · 1440 × 900 · 페이지 오류 0)

| 파일 | 무엇 |
|---|---|
| `fixA-01-three-dots.png` | 3 턴 뒤 점 셋(팔자주름 좌우 · 미간 · 턱) · 얼굴 대표점 · 전신 0 |
| `fixA-02-click-nasolabial.png` | 팔자주름 누름 — 팔자주름만 진함 · 미간 · 턱 점 남음 |
| `fixA-03-click-glabella.png` | 미간 누름 — 미간만 진함 · 다른 점 남음 |
| `fixA-04-card-ring.png` | 카드 누름 → 속한 점(넷)에 강조 링 |
| `fixA-05-botox-click-jaw.png` · `fixA-06-botox-click-mouthcorner.png` | 두 번째 대화 — 턱 13 · 입꼬리 12(거름이 줄어듦 · 다른 점 남음) |

## 6. `$J` sites 넓힘 세부(A-7)

- **더한 21**: SITE-027 · 028 · 029 · 030 · 031 · 032 · 033 · 037 · 040 · 041 · **046(팔자주름)** · 055 · 056 · 060 · 064 · 076 · 084 · 089 · 090 · 091 · 120. 모두 `source: face_coords`(좌표 그대로)다.
- **뺀 9**(좌표표에서 area · line · none 꼴이고 대표점이 없는 부위 — `$J` 는 얼굴 부위에 점 꼴만 받는다, JS2): SITE-011 · 043 · 044 · 045 · 058 · 065 · 071 · 083 · 087. 이 부위가 대화에 나오면 점 0 이다(`_add_sites` 가 `$J` 에 없는 부위는 넣지 않음).
- 그대로인 것: items · groups · products · product_categories 는 옛 파일과 같은 값이다(JSON 비교). 옛 sites 71 은 값이 같다. meta 는 `made_at` · `sites_rule` 만 다르다.

## 7. 스펙과 다른 점 · 남은 것(스펙 워커 · 코디)

| # | 무엇 |
|---|---|
| S1 | SPEC-010 0.2.8 FS1(점 = 목록 진료항목 부위) · FS3(카드 강조 = 진료항목 얼굴 부위) · FS4(거름 = 자손 포함) · E1(「점 = 그 진료항목 부위」) · §2 sites 71 은 이 발주로 바뀌었다. 바뀐 내용은 점 = 대화 부위(주제 `sites`) · 거름 · 강조 = 품음 계산 · sites 92 · 고민 길 = 직접 + 같은 시술 범위(`case_scope`) · 장부 `consult.topics[].sites` · `items.case_scope` · `items.sites_added` 다 |
| S2 | 케이스 부위 코드를 허브가 행에 주지 않아(`site_code` 빈칸 · `case_site_name` 만) 이름으로 `$J` 부위를 찾는다. 허브가 케이스 부위 코드를 주면 그 칸 하나로 바꾸면 된다 |
| S3 | 실물 2 턴의 칸 교체(팔자주름 → 미간주름)와 답의 「목록 아래에 남아 있어요」 어긋남은 A 밖이다(보고만) |
| S4 | 이해 호출이 「팔자주름」 을 고민 + 부위 둘로 내서 1 턴 목록이 고민만(52)이 아니라 교집합 44 다. 원래 규칙이라 손대지 않았다 |
