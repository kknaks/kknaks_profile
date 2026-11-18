# [app] 상담 채팅 0.3 구현 보고 — WORK-014 WP-0 ~ WP-8

2026-11-17 · app 워커 · 워크트리 `clinic_chat/phub-gold-jev`(HEAD `68a31b1` 위 · **커밋 안 함**) · 계약 SPEC-006 0.1.0 + SPEC-001 0.7.2 · 발주서 `impl-chat-v03-instructions.md`(코디 답 W-1 · W-2 · W-3/B-10 · W-5 · W-9 · B-2 · B-5 · B-9 반영).

## 1. WP 별 — 돌린 파일 · 통과 수(전체 pytest 안 돌림)

| WP | 돌린 파일(통과) | 고친 기존 시험 |
|---|---|---|
| WP-0 | test_v03_start 4 · test_consult_ledger 6 | — |
| WP-1 | test_v03_frame 8 · test_consult_page 8 · test_consult_chat_ui 8 · test_consult_ledger 6 | **test_consult_page T24**: `data-slot` 수 `len(SLOTS)+0` → `+4`(A8 드로어 빈 자리 넷 · 코디 W-2) |
| WP-2 | test_v03_prompt 20 · test_consult_prompt 15 · test_consult_material 6 · test_state_blanks 6 · test_state_examples 5 | **S5-T19**(test_state_blanks): `pop("system_state")` → `pop("system_v3")`(달리 받음 ③) · **S5-T10**(test_state_blanks): `options` 키 `layer` → `holder`(달리 받음 ④) |
| WP-3 | test_v03_turn_kind 18 · test_v03_shared 6 · test_walk_front 18 · test_walk_core 20 · test_walk_entry 7 · test_consult_carry 7 · test_state_carry 7 · test_consult_turn 11 | **test_consult_turn::test_prompt_changed_marked_and_kept_copy_used**: 기대 `"0.1.0-draft"` → src `consult.json` 의 version(VO1 version 0.3.0-draft · 코디 답) |
| WP-4 | test_v03_close 13 · test_state_blanks 6 · test_consult_material 6 · test_consult_turn 11 | — |
| WP-5 | test_v03_fixes 6 · test_state_object 10 · test_consult_ledger 6 · test_consult_turn 11 | S5-T2 은 고칠 필요 없음(그 시험의 재등장은 `target` → `confirmed` 로 FX1 에서도 참) — FX1 꼴은 S6-T12 에 |
| WP-6 | test_v03_list 12 · test_consult_listing 3 · test_state_list 5 · test_state_plan 5 · test_consult_page 8 | — |
| WP-7 | test_v03_sites 8 · test_consult_sites 4 · test_state_object 10 · test_state_plan 5 · test_state_examples 5 · test_consult_turn 11 | **S5-T1**(test_state_object): `HOWS` 닫힌 목록에 `view`(B-2) |
| WP-8 | test_v03_e6 4 | — |

- `ruff check .` 통과. 함께 쓰는 코드: `walk/front.py` +18 −3 · `columns/col_b.py` +3 −2(인자 안 주면 지금과 같음 — §8 기존 다섯 파일 안 고친 채 통과).
- 고친 fixture: `tests/state_fixture.py` 임시 칸 `concern_sites` → `sites`(검수 N-2 · 한 줄).
- `_face.svg` · `face_coords.py` sha1 = WP-0 값 그대로(6337a357… · 669574aa…). 허브 레포 변경 0.

## 2. 구현 요약

- 새 모듈: `consult/turn_kind.py` · `close.py` · `voice.py` · `drawer.py` · `e6.py` + `e6_inputs.json` · 템플릿 `drawer.html` · `drawer_list.html` · `state.html` · `state_turn.html` · **`list_v3.html`**(allowed_paths 밖 새 조각 하나 — 켠 상태 리스트 꼴을 `list.html` 에서 갈라 둠 · 끈 상태 꼴은 글자 그대로).
- 턴 루프: 둘째 턴부터 걷기(`entry_pick=False` · `abbr_yes_only=True`)를 task 로 띄우고 거둠 요청에 `tk_new/talk/follow` 를 첫 묶음에만 실어 함께. 판정까지 단계 신호를 붙들고(B-11) `talk` 면 `understand → answer` 만. `talk` + 앞 `ask` 없음 = 걷기 거둠(이미 끝났으면 결과만 버림) · 있음 = 끝까지 기다렸다 버림(B-3). `follow` · `new` 의 「입구 없음」 재걷기(TW4 · TW5). TT6 · `CHAT_TURN_KIND=off`.
- `system_v3` 13 절 · `kind_labels`(+앱 쪽 `procedures`=「시술」 — EM6 이름) · `voice_check` · `turn_headers.close/prev` · `slots.mark-modality-level`=「{name} 계열 시술」 — 전부 초안. 「앱 판정」 rev 3 = `read_as` · `unresolved` · `offered[].rows` 뺌 · `options[].holder` · 끝맺음 · 앞 턴 블록.
- `close`(CS2 · CS4) · `empty`(EM1 · EM5 · EM6 · W-5 `safety`) · 꼬리 `close:` → `said` · `said`=0 이면 `asked[]` 에 안 적음(W-8).
- FX1 · CS7 · FX3(`conv-outdated` · 드로어 `outdated`) · FX4(`rev_changed` 거절 · **장부 줄 안 씀 — B-5**).
- 리스트: `descended[]` 계열 묶음 · LS4-1(W-9 a) · `hidden` · LS6 요약 줄 · SP(0.7.2 · 앱은 `site_applied` · `site_prefer` · `n_site_prefer` 만 읽음 · 한 고민 응답이 섞이면 prefer + filter 행은 표지 행 — 코디 W-1) · 표지 0 이면 순서 그대로 · 문구 0(B-7).
- 점: `SITES_FIELD`=`sites` · 객체 고민 전부(누적) · `data-concern-codes/asked-codes/match/focus` · 누르기 `GET /c/<id>/list?concern=`(메모 → 없으면 QY1 꼴 · 메모에 넣음 · 4xx 거절) · `viewing`(한 턴 · 글의 새 고민이 이김 · 여럿이면 `source.turn` 최근 · 하위 고민은 객체에 `state` said · **`how=view`** 로 듦 — B-2 를 「손님 말 `text` 가 아니라 `view`」 로 읽음).
- 화면 네 칸 · 드로어(뜰 때 한 번 훑은 메모리 색인 · W-11) · `GET /convs` · 객체 패널 `state` 이벤트(`done` 바로 앞).

## 3. 실물

- **E6-0**(18223 · 가짜 턴 · 헤드리스 Chrome CDP 실제 마우스 이벤트): SVG `<circle>` 의 htmx 속성(`hx-get` · `hx-target="#procedure-list"`)이 **선다** — `elementFromPoint` = 그 점(`pointer-events` 켬) · `GET /c/<id>/list?concern=CON-024` 200 · 조각 갈아 끼움 · 쌍 점 둘 다 `aria-pressed` · 폼 `viewing`=CON-024. JS 폴백 불필요.
- **허브 판**: 실행 시점에 18105 가 이미 0.7.x 칸(`descended` · `sites` · `site_applied` · `matched.how`)을 냈다(코디 알림 「0.7.2 DB 판 재시작」 과 같은 판) — 아래는 **② 칸 있는 판**의 값이다. ① 칸 없는 판은 따로 돌지 않았다.
- **E6-1 · E6-2**(12 턴 · 첫 턴 빼고 9): `new` 6 · `talk` 2 · `follow` 1 · 가르기 요청 183.8 ~ 203.9 ms · 오류 0. 기대(§11-3)와 다른 판정: ① 턴 2 「지방이 두꺼운 느낌이야」 = `follow`(0.75 · 기대 new — 앞 대상 CON-168 로 다시 걸음) · ③ 턴 2 「볼이 처져서요」 = TK5-4 `new`(follow 0.69). 맞은 것: ① 턴 4 「왜 채우지를 못한거야」 = `talk`(0.81) · ② 턴 3 「응 맞아」 = `talk`(0.97).
- ① 턴 1 턱살: 리스트 = M18 묶음 시술 6 · 「V라인주사」 는 `hidden.names` 에만 · 점 SITE-072 · `close`=`ask`. 턴 3: `empty`=[지방분해 주사 × 조합] · `close`=`offered`(package — N-6 꼴). **턴 5 「지방 주사」**: 허브 `M18` `줄임` 후보 Noul 0.58(사이) → TW8 대로 대상 아님 · 덮인 「주사」 도 dropped → 「입구 없음」(입구 고르기 다시 걸어도 같음 — 후보가 있으면 fan-out 안 함). 문턱 · 지시문은 안 고침(O6-1 · 코디).
- ① 턴 6 써마지: `close`=`null`(이미 `focus` 고민이 있어 BK2 안 섬 — §11-3 의 「BK2 ask」 기대와 다름).
- ③ 턴 2: CS7 로 BK5 없음 · 점 SITE-051 · `descended_n` 11. ③ 턴 3: NQ6 · `close`=`offered`(package) — 안전 종류 권유 0. 메시지 50 KB(재료 103 줄 · W-7 확인 거리).
- SP 실물 「볼에 탄력 저하 시술 추천해줘」: CON-048 + SITE-051 → `site_applied`=`prefer` · `prefer_rows` 0(B-7 꼴 — 표지 0 · 순서 그대로) · 시술 34 · `hidden.descended_n` 67 · facets 56 요청(profile 이어 조회).
- **E6-3**: `talk` 두 턴 — 거둔 걷기(① 턴 4) 허브 resolve 2 · coverage 1 · Jev front 0 + 가르기 1 · 객체 조회 0 · 깊이 읽기 0 / 끝난 뒤 버린 걷기(② 턴 3 — 앞 `ask` 있음) 허브 resolve 2 · coverage 1 · Jev front 1 + 1 · 객체 조회 0. 다음 턴 영향 없음.
- **E6-4**: `close:` 줄 13/13 턴 · `by`=`ask` 인데 `said`=0 은 0.
- **E6-5**: 금지 낱말 합 0 · `by`=`null` 인데 물음으로 끝난 턴 1(① 턴 5 — 입구 없음 되묻기).
- 실측 중 찾아 고친 것 하나: EM1 이 `concern_candidates` 의 `total`(묶음 수) 0 을 「맞는 고민 0」 으로 셌다(턱살 — 「그 밖」 · 내려온 행이 있는데 `empty`) → 「계열 층만」 · 「그 밖」 · 내려온 행을 셈에 넣음 + 시험 한 꼴 · ① 대화만 다시 돌려 `empty` 0 확인.
- 18223 은 내렸다(`lsof` 0) · 18105 GET 만 · 18222 안 건드림. 장부 `runs/consult/e6/turns.jsonl` · 결과 `runs/consult/probe/*.json`(gitignore).

## 4. 남은 것 · 주의

- 코디 · 사용자: E6-6(18222) · 프롬프트 · 빈 자리 문구 초안 확정 · TK 판정 틀린 두 턴 · 「지방 주사」 줄임 Noul 0.58 → 대상 아님(문턱 / 지시문 / O6-1) · ① 턴 6 BK2 기대 차이 · `offered`=package 끝맺음(N-6).
- `list_v3.html` 새 조각(allowed_paths 밖) · `kind_labels.procedures` 추가 키 · B-2 해석(`state` said · `how` view).
- 전체 pytest · 표에 없는 기존 시험(test_state_synergy · test_web · 시험 앱 묶음)은 안 돌림(코디 몫).
- 커밋 안 함. 비밀값 grep(`/Users/` · `sk-ant` · 키 값) 0 · `.env` · runs 는 gitignore.
