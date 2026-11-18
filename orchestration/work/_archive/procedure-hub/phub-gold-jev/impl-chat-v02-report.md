# [app] 상담 채팅 0.2 구현 보고 — WORK-012 WP-0 ~ WP-8 (SPEC-005 0.1.0 · 상담 객체)

2026-11-17 · app 워커 · 워크트리 `clinic_chat/phub-gold-jev`(0.1 + 수정 1 미커밋 위 · **커밋 안 함**).

## 0. 요약

- WP-0 ~ WP-8 워커 몫 끝. `uv run ruff check .` 통과 · `uv run pytest -q`(env 없이 = 끈 상태 전체) **333 passed · 1 skipped**(기준선 290 / 1 + 새 43) · `pytest tests/test_state_*.py` 43 passed.
- 실물 E5-1 ~ E5-4: `CHAT_STATE=on uv run python -m clinic_chat.consult.probe --e5` — 7 대화 14 턴 전부 오류 0 · 장부 시작 줄 `consult_state: "on"` 전부 확인 · 서버 18223(`CHAT_STATE=on`)으로 예시 ① 세 턴 `curl --data-urlencode` → 내림(`lsof` 0).
- **코디: 18222 를 `CHAT_STATE=on` 으로 재시작 필요**(프로세스 env 로 — `.env` 에 두지 않는다 · 새 대화부터 켠 상태).

## 1. 바뀐 파일

| 무엇 | 파일 |
|---|---|
| 새 모듈 | `clinic_chat/consult/state.py`(객체 · 갱신 · diff · 거둠) · `plan.py`(객체 기준 조회 QY1 ~ QY3 · QY5 · QY7 · 파생 칸) · `blanks.py`(BK1 ~ BK5 + 부위만 · NQ) · `synergy.py`(QY4 · QY4b · SY5) · `e5.py` + `e5_inputs.json`(실측 입력 글 — T17 이 `.py` 만 보므로 글은 JSON 에) |
| 고침(consult) | `turn.py`(켠 가지 — `Consult` 클래스를 이 파일 안에 · 끈 가지는 0.1 줄 그대로) · `ledger.py`(시작 줄 `consult_state` · `Conv.consult` · `memo` · 성공 줄만 `consult.after`) · `carry.py`(`with_options`) · `material.py`(앱 판정 `ask` · `synergy_lines` · 요약 줄 붙이기 · 「상담 상태」 블록) · `listing.py`(`codes` 선택 인자 · `state_list` · `list_codes`) · `prompt.py`(0.2 키 · `system_text_state` · `state_ready`) · `server.py`(대화 첫 턴 상태 · 켠 대화의 프롬프트 키 검사) · `probe.py`(`--e5` · `--only`) |
| 템플릿 · 스타일 | `partials/list.html`(켠 꼴 칸이 있을 때만 그림 — 끈 출력 0.1 그대로) · 새 `partials/list_interest.html` · `list_synergy.html` · `static/consult.css`(표지 · 묶음 꼴 — `--ms-*` 토큰만) |
| 함께 쓰는 코드(인자 0) | `walk/front.py`(0.1 대비 +8 줄 — `origin` 을 들고 `option_from` 칸 · `out.carried[].origin` · `_from_key`) · `walk/jev_requests.py`(+4 — `target_option` 가지). `origin` 없으면 글자 그대로(S5-T20) |
| 설정 · 문서 | `config.py`(`chat_state`=`off` · `chat_ask_max` · `chat_synergy` · `chat_retract`) · `.env.example`(이름만 + 「`.env` 에 두지 말 것」) · `README.md` 「상담 0.2」 절 · `prompts/consult.json`(`system_state` 절 셋 · `jev_front.target_option` · `jev_state.retract` · `turn_headers.consult` — `system` 다섯 절 글자 무변경) |
| 시험 | 새 `tests/state_fixture.py`(가짜 허브 · Jev · 한 턴 도우미 `Run`) · `test_state_{object,carry,plan,blanks,synergy,list,examples}.py` |

**안 건드림 확인**: 0.1 · 수정 1 시험 파일 · `conftest` · `fake_*` · `consult_fixture` · `walk_fixture` sha = WP-0 목록과 같음 · `_face.svg`(`b3e4af94…`) · `face_coords.py`(`034130b7…`) = WP-0 값과 같음 — **두 파일은 연 적 · 쓴 적 없음**(N-6). `web/` · `llm/` · `walk/{material,gate,calls,breadth}.py` · `prompts/*.md` 무변경.

## 2. WP-0 기준선 · 줄 번호

- 기준선 `pytest -q` = **290 passed · 1 skipped**. 수정 1 뒤 `turn.py` 172 줄(든 후보 `:92` · 걷기 `:94` · 재료 `:109` · `list`/`sites` `:117-128` · 맺는 줄 `:156-172`) — 검수 N-1 그대로.
- 0.1 끈 시스템 글 sha256 = `b3fa8e20…77440`(장부 보관본 둘과 글자 같음) — S5-T19 가 이 값으로 대조.

## 3. 발주서 W-1 ~ W-8 · 검수 반영

| # | 어떻게 |
|---|---|
| W-1 (가) | 축 부위만 있고 `focus` 가 없으면 QY7 = `facets(node=부위, indication)`(걷기와 같은 열쇠 → 대개 `skipped: walk`) → 빈 칸 `concern`(about = 부위 · `bk: BK2s`) · `focus` 가 있으면 서지 않음. WP-1(UP3 둘 다 객체) · WP-4 · WP-6(묶음 ① 만 있는 턴에도 `list` + 「목록」 단계) 줄 반영 |
| W-2 | 같은 조각(`span`·`start`)의 고민과 함께 든 부위 → `sites[]` + `source.pair_concern` · 부위 거르개는 짝 고민이 `focus` 일 때만(`state.filter_sites`) |
| W-3 | 기본 `off` · 켜는 값은 프로세스 env · 새 시험은 설정에서 `chat_state="on"` · `--e5` 는 `off` 면 돌지 않음(`chat_state_off`) · E5 · 18223 시작 줄 `consult_state: "on"` 확인 |
| W-4 | 앞 턴 `ask` 선택지의 (표, 코드)가 이번 글 `target` 이면 `how=text` · `from_ask` 채움 · 답한 것으로 셈(S5-T3 · `test_w4_*` · 실물 ③ 턴 2) |
| W-5 | 18223 확인은 `curl --data-urlencode` · 시작 줄 `question` 이 보낸 글과 같음(세 턴 · E5 14 턴도 `question_matches_start` 참) |
| W-6 | WP-3 · WP-5 첫 걸음 GET(아래 §4) |
| W-7 | `plan` 은 걷기의 `Call` 을 그대로 지어 `key()` 로 견줌 · 부위 거르개 = 이름 글자(`test_w7_query_key_equals_walk_call_key`) · E5 의 `skipped_walk` 수 §5 |
| W-8 | E5 보고에 턴마다 QY1 `site` 값 · 리스트 행 수 · `e5_inputs.json` 에 부위만(「이마가 신경 쓰여요」) · 같은 이름 뒤 `focus` 이동(「팔자주름…」→「볼처짐도…」) 대화 |
| N-3 | 앞 턴 대상이면서 선택지인 항목은 `carried[]` 에도 남기고 `options_carried[]` 에도 적음 |
| N-5 | `how` 닫힌 목록 넷(`text` · `option` · `derived` · `carried`) — S5-T1 |
| N-7 | 장부 `consult.retract_ms` · `retract_resolve_ms` 따로 |

## 4. 허브 18105 GET(W-6 — 키 확인)

- `scope(product:PRD-416)` → `holders[]`: `holder_table` · `holder_code` · `holder_name` · `role` · `gid` · `subject_*` · `path` · `depth` · `via` · `link` — 자기 1 · 물려받음 3 · **하위 제품 1(`PRD-417`)** · 머리 `counts_by_role`.
- `facets(product:PRD-416, indication)`(기본 role) → 27 행 · 행에 `concern_code` · `concern_name` · `concern_match` · `layer{role, path, holder{…}, scope_gid}`.
- `pair(a=product:PRD-416, classes=보완)` → 34 행 · 행 키 `from_*` · `to_*` · `a_side` · `a_layer` · **`b_layer`(b 없으면 null)** · `question_class` · `same_day` · `goal_effects` · 머리 `counts{by_class, same_day, conflict}`. **상대 쪽 층 · 경로 칸이 없다 → B-6 ② 를 탔다**(케이스 · 제품 상대만 `scope` — `rule: "SY5"`).
- `pair(…, classes=회피,간격,순서)` → 45 행(회피 2 · 간격 21 · 순서 22 — WORK §3-1 재셈과 같음) · 불가 2.
- `concern-candidates` 의 후보 profile 행에 `modality_code` 있음 → 켠 `list` 의 계열 코드로 씀.

## 5. 실물 E5-1 ~ E5-4(허브 18105 읽기 · Jev · 구독 CLI · `CHAT_STATE=on`)

ms 는 first_list / ttft / total. 「조회」 = 객체 기준 조회(rule · total · 걷기 겹침).

| 대화 · 턴 | 객체 diff | 조회 | ms | Jev 요청(걷기 · 입구 고르기 · 거둠) · `ask` |
|---|---|---|---|---|
| ① 1 써마지 | + `PRD-416` said · `procedures` `PRC-312` | QY2 5 · QY3 27 | 481 / 1,665 / 4,473 | 1 · 0 · 0 · BK2 선택지 21 |
| ① 2 탄력 | + `CON-048` said(`how=option`) · focus | QY1 55 묶음(walk) · QY4 34 · QY4b 45 | 917 / 3,909 / 6,787 | 1 · 0 · 1 · 없음 |
| ① 3 스킨부스터 | + `M4` said(procedures 그대로) | QY2 44(walk) · QY4 44 · QY4b 52 | 672 / 9,028 / 11,633 | 1 · 0 · 1 · 없음 |
| ② 1 팔자주름 | + `CON-009` · `SITE-046`(짝 CON-009) · focus | QY5 37 묶음(walk · site=「팔자주름」) | 672 / 1,785 / 5,242 | 1 · 0 · 0 · BK1 |
| ② 2 필러 | + `M2` · asked 답함 | QY2 51(walk) · QY4 24 · QY4b 40 · SY5 3 | 532 / 2,572 / 7,575 | 1 · 0 · 1 · 없음 |
| ② 3 주름보다는 볼처짐 | + `CON-024` · focus → CON-024 · `CON-001` 안 넣음(거둠 0.90) · `CON-009` 그대로(거둠 0.69 사이) | QY1 4 묶음(walk · **site 없음** — W-2) | 836 / 1,979 / 5,266 | 1 · 0 · 1 · 없음 |
| ③ 1 리쥬란 힐러 맞아 볼까 | + `PRD-151` · `SITE-051` **guess**(0.33 `uncertain_kept`) | QY2 5 · QY3 47 | 738 / 9,178 / 12,409 | 1 · 0 · 0 · BK2 선택지 40 |
| ③ 2 잔주름 | + `CON-013` said(`text` · `from_ask`=1 — W-4) · focus | QY1 27 묶음(walk) · QY4 44 · QY4b 52 | 788 / 7,529 / 10,136 | **2**(선택지 38 > 32) · 0 · 1 · BK5(볼 확인) |
| ③ 3 보톡스랑 같이 | + `PRC-001` · `PRD-001` · `M1`(같은 조각 「보톡스」 셋 다 target) · asked 답 안 함 | QY2 ×3 · QY4 ×3(walk) · QY4b ×3 · SY5 3 | 966 / 9,470 / 11,508 | 1 · 0 · 1 · 없음(NQ6 — 같은 날 질문이 회피 종류를 읽음) |
| 부위만 「이마가 신경 쓰여요」 | + `SITE-014` | QY7 86(walk) | — / 2,075 / 4,934 | 1 · 0 · 0 · `concern`(about=부위) 16 · `list` 안 보냄(묶음 셋 다 빔) |
| W-2 「팔자주름」→「볼처짐도」 | 2턴: + `CON-024` · focus 이동 · BK1 답 안 함 | QY5(site=팔자주름) → QY1(site 없음) | 496 / 1,720 / 3,389 | 2턴 `ask` 없음(NQ5) |
| 「모공이 신경 쓰여서요」 | + `CON-115` · `ANA-039`(이신경) **named 0.04 → 객체에 없음** | QY1 39(walk) | 839 / 7,957 / 10,908 | BK3 선택지 5 |
| 「팔자주름이 고민입니다」 | + `CON-009` · `SITE-046` · `SITE-057`(입) **named 0.09 → 객체에 없음** | QY5 37(walk) | 594 / 7,299 / 10,096 | BK1 |

- **부록 B 재셈 ↔ 허브**: QY3 `PRD-416` 27 행 · 고민 21 ✓ · `PRD-151` 47 · 40 ✓ / QY1 `CON-048` 105 행 · 시술 34 ✓ · `CON-009` 74 · 15 ✓ · `CON-024` 10 · 4 ✓ · `CON-013` 46 · 16 ✓ / QY4 `PRD-416` 34 행 · 상대 11(안 6 · 밖 5) ✓ · `PRD-151` 44 · 13(안 5 · 밖 8) ✓ · `PRC-001` 33(N-2) ✓ · `M4` 44 ✓. 다른 것: QY2 `PRD-416` 5(하위 제품 `PRD-417` 이 더 있음 — 재셈은 자기 · 물려받음만 셈) · `M4` 44(재셈 39 — 하위 케이스 5 를 안 셈) · **계열 끝 `M2` 보완 24 행 · 상대 10**(재셈 21 · 8 — 하한 · O5-9 그대로).
- **표지(U5-4 (a1))**: ① 턴 2 안 상대 6 가운데 `M7` · `M8` ✓ · ② 턴 2 안 상대 8 가운데 `M8` ✓(검수 W-5 기대와 같음). QY4b 의 gid 는 메시지 · 실은 gid · `shown.info` 0(S5-T21).
- **걷기와 겹친 조회의 `skipped` 수**(W-7): 14 턴 합 13(QY1 · QY5 · QY7 · QY2 · QY4).
- **E5-2 걸린 선택지**: ① 턴 2 — 선택지 21 가운데 yes 는 `CON-048` 0.97 하나 · 틀린 yes 0 · 사이 값 0 · 입구 고르기 안 돎 · Jev 1 요청. ③ 턴 2 — 이름으로 답해 선택지 38(글자 맞춘 2 빠짐) 전부 no · 32 를 넘어 맨 앞 판단 Jev 2 요청.
- **E5-3 거둠**: 「주름보다는 …」 에서 `CON-001` 0.90 withdraw · 앞 고민 `CON-009` 0.69 · `SITE-046` 0.63(사이 — 그대로) · 거두지 않는 말 9 턴의 항목 전부 ≤ 0.05. 거둠 ms 181 ~ 384(resolve 4 ~ 11) — 걷기(493 ~ 941)와 함께 띄워 턴 전체를 늘리지 않음.
- **E5-4 우연 일치**: 「볼」 0.33 사이 → `guess`(QY1 site 없음 — 리스트 안 좁힘) · 「이신경」 0.04 · 「입」 0.09 → `named` → 객체 0(해부 입구도 UP2 로 안 듦) · 걷기는 그대로 읽음(O5-2).
- 이벤트 순서 14 턴 전부 `list` → `sites` → `delta` → `done`(목록 없는 턴은 `sites` → `delta`). 서버 18223: 세 턴 `list sites done close` · 1턴 묶음 ① · 2 · 3턴 ① · ② · ③ 전부.

## 6. SPEC · WORK 와 다르게 지은 곳 · 알릴 것

1. **`prompts/consult.json` `version` 은 `0.1.0-draft` 그대로**(WORK §9a 는 `0.2.0-draft`) — 기존 시험 `test_consult_turn.py::test_prompt_changed_marked_and_kept_copy_used` 가 저장소 JSON 의 version 을 `0.1.0-draft` 로 박아 두어 바꾸면 깨진다(기존 시험은 못 고침). 코디가 그 한 줄을 고치면 0.2.0-draft 로 올린다. sha 는 바뀌었으므로 새 대화부터 새 보관본.
2. 「상담 상태」(객체 요약)는 「앱 판정」 JSON 안이 아니라 **바로 뒤 `turn_headers.consult` 블록**(SPEC §6-3 의 「객체 요약 블록의 머리」) · 앱 판정에는 `ask` · `synergy_lines` 만.
3. 「실행 중단」 턴은 `error` 가 있어 RV9 로 객체가 서지 않는다(diff 는 `not_counted`) — W-6 의 「갱신은 한다」 는 범위 밖 · 입구 없음 턴에서만 남는다(시험은 범위 밖 + 거둠 꼴).
4. 허브 enum 값 「하위 고민」 · 「불가」 는 `consult/` 코드의 T17(한글 0)을 지키려고 `\\u` 이스케이프 상수 · 나머지(보완 · 회피 · 자기 · 물려받음 · 종료 상태)는 `walk/` 상수를 import.
5. `Consult`(켠 상태의 한 턴 몫)는 allowed_paths 를 지키려고 새 파일이 아니라 `turn.py` 안에 둠.
6. S5-T16 은 §8 의 **꼴**을 가짜 코드로(수는 가짜) — 부록 B 의 실물 수 대조는 E5-1(위 §5).
7. S5-T22(얼굴 · 0.1 시험 sha)는 pytest 가 아니라 이 보고의 sha 대조(§1) — 얼굴 파일은 사용자가 바꿀 수 있어 시험으로 박지 않음.
8. 리스트 ② 는 `focus` 고민 하나만(RV6 의 「한 글에 둘이면 고민마다」 는 이 판 안 함).
9. 실물에서 본 것: 「보톡스」 같은 조각의 계열 · 시술 · 제품이 셋 다 `target` → 대상 셋 · QY4 셋(묶음 ③ 셋) — 겹침을 걷기가 가르지 않는 실물 꼴(③ 턴 3). 「상담 상태」 · 「앱 판정」 의 크기는 ③ 턴 3 이 가장 큼(시너지 줄 22).
10. B-12 되적기 후보에 더할 것: 「하위 제품」 holder 가 `scope` 에 섞임(QY2 수) · `pair` 에 상대 쪽 층 칸 없음(B-6 ②) · 1 · 2 · 3 · 4 · 8.

## 7. 공개 · 비밀

- 커밋될 새 · 고친 파일에 홈 절대 경로 · 계정 · 회사 도메인 · 키 꼴 · 내부 URL grep **0**(127.0.0.1 · `fake-hub` 제외) · 상담 인자 `--json-schema` · `anthropic` 0. `.env` 열지 않음(`CHAT_STATE` 줄 없음만 셈).
- 실측 장부 · 결과는 `runs/consult/e5/`(gitignore) · 18223 장부는 세션 임시 폴더(레포 밖).
- `git status --porcelain --ignored`: 커밋될 것 = §1 + 0.1 · 수정 1 의 미커밋분 · gitignore = `.env` · `runs/` · 캐시.

## 8. 남은 것

- **코디: 18222 를 `CHAT_STATE=on` 으로 재시작 필요** → 사용자 E5-5(+ N-10 · U5-4 볼 것). 코드 검수.
- `consult.json` 의 0.2 절은 **초안**(SPEC §6-3 뜻 옮김) — 사용자 확인 · version 올림(§6-1).
- 열린 것 그대로: O5-1 · O5-2(걷기와 객체 어긋남 — ③ 턴 3 · 「주름」) · O5-11 · O5-12.
