# [reviewer_code] 상담 0.3 코드 검수 — WORK-014 구현(SPEC-006 0.1.0 · SPEC-001 0.7.2 칸)

2026-11-17 · reviewer_code(read-only) · 워크트리 `clinic_chat/phub-gold-jev`(HEAD `68a31b1` 위 미커밋) · 지시서 `review-code-chat-v03-instructions.md`.
읽은 것: SPEC-006 0.1.0 전부 · WORK-014(§3 · §13 · §15 · §17 해당 절) · `review-work-014.md`(W-8 · B-2) · `impl-chat-v03-instructions.md` · `impl-chat-v03-report.md` · SPEC-001 0.7.2(§4-5 칸 표 · §5-11 SP) · `_RESUME` §2 11-17 맨 위 행들. 실호출 0(Jev · claude 안 부름) · `.env` 안 엶 · 18105 안 건드림 · 18222 는 GET 만.

## 판정: **WARN**(FAIL 0 · WARN 6 · NOTE 7)

A1 ~ A8 계약은 코드로 선다. 함께 쓰는 코드(front · col_b)도 인자를 안 주면 지금과 같고, 시험 앱 쪽 시험은 다 통과한다. 다만 **기존 시험 두 개가 깨져 있는데, 구현 보고는 이 둘을 통과로 적었거나(WP-6 뒤 WP-7 이 깨뜨렸다) 돌리지 않았다** — 커밋 전에 코디가 결정할 것(W-1 · W-2). 사용자가 처음 짚은 「지방 주사」 는 **문턱보다 든 후보와 줄임 규칙이 맞물려 둘 다 사라지는 자리**가 직접 원인이다(§4 — 고칠 자리 제안).

## 1. 시험 · ruff(바뀐 파일 관련만)

| 무엇 | 결과 |
|---|---|
| `uv run ruff check .` | **All checks passed** |
| 새 시험 `tests/test_v03_*.py` 10 개 + 구현 보고의 WP 표 기존 파일(consult_page · consult_turn · state_blanks · state_object · walk_front · walk_core · walk_entry · consult_carry · state_carry · consult_ledger · consult_listing · consult_sites · consult_material · consult_prompt · state_plan · state_list · state_examples · consult_chat_ui) | **249 passed · 1 failed** — `test_state_list.py::test_s5_t12_subject_only_list_and_order`(W-1) |
| 함께 쓰는 코드(`walk/front.py` · `columns/col_b.py`) · 켠 상태 모듈을 쓰는 나머지 기존 파일(state_synergy · web · columns · consult_cli · walk_material · walk_ranges · v06 넷 · batch · answer_key · covered · holes · interim · speed · quality · runs · cli · clients) | **154 passed · 1 skipped · 1 failed** — `test_state_synergy.py::test_s5_t11_complement_lines_inside_only_once`(W-2) |
| 합 | **403 passed · 2 failed · 1 skipped**. 시험 앱(3열 · 답 키 · 걷기) 시험은 전부 통과 — §3 ③ 의 「시험 앱 동작 안 바뀜」 은 시험으로도 선다 |

## 2. 지적 표

| # | 파일:줄 | 심각도 | 근거 | 무엇 · 고칠 방향 |
|---|---|---|---|---|
| W-1 | `clinic_chat/consult/turn.py:618` · `tests/test_state_list.py:35` | **WARN(커밋 전)** | SPEC-006 FD3 · WORK §15 「여섯 밖에서 깨지면 보고」 · 보고 §1 WP-6 「test_state_list 5」 | 고민이 처음 들어 `focus` 가 바뀌었는데 부위 합집합이 비어 있고 앞 `sites` 가 없으면 `sites` 를 안 보낸다(`last is None and 빈 조각` 조건). FD3 은 「합집합이 바뀐 턴 **또는 `focus` 가 바뀐 턴**」 이다. S5-T12 의 `list < sites < delta` 가 깨진다. WP-6 에서는 통과했고 **WP-7(점 누적)이 깨뜨렸는데 WP-7 은 이 파일을 다시 돌리지 않았다** — 보고의 통과 수가 지금 코드와 다르다. 화면에 보이는 차이는 없다(빈 조각). 고칠 방향(코디가 고름): ⓐ 코드 — `focus` 가 바뀐 턴은 빈 조각도 보낸다(FD3 글자 그대로 · 한 줄) ⓑ 시험 — 달리 받음 ②(S5-T7 「점 = focus」 → FD1)의 꼴로 받고 S5-T12 의 `sites` 순서 단언을 고친다. 추천 ⓐ |
| W-2 | `clinic_chat/consult/turn.py:560`(시너지 요약 줄 `rows` 뺌) · `tests/test_state_synergy.py:43` | **WARN(커밋 전)** | SPEC-006 EM4(「LLM 에 행 수를 주지 않는다」) · WORK §15 ④ · B-10 | 켠 상태 시너지 요약 줄에서 `rows` 를 뺀 것은 EM4 의 뜻에 맞다. 그런데 S5-T11 이 `lines[0]["rows"] == 2` 를 단언해 깨진다. WORK §15 ④ 는 「앱 판정」 의 `offered[].rows` 만 적었고 요약 줄 `rows` 는 목록에 없다. 이 파일은 「표에 없는 파일」 이라 워커가 안 돌렸다(B-10). 고칠 방향: 코디가 「달리 받음 ④ 에 시너지 요약 줄 `rows` 포함」 이라고 정하고 S5-T11 의 그 단언 하나를 고친다(행 수는 장부 `queries` 로 센다) |
| W-3 | `clinic_chat/walk/front.py:238` · `:357-358` | **WARN** | SPEC-006 TW7 · TW8 · SPEC-004 CR2 · 사용자가 처음 짚은 꼴(P3) | **「지방 주사」 가 대상 0 이 되는 직접 원인.** 앞 대상 `M18` 은 객체에 살아 있어 든 후보로 실렸는데(TW7) 이번 글에서도 `M18` 이 줄임으로 맞아 **CR2 가 든 후보를 뺀다**. 이번 글의 `M18` 은 Noul 0.58 · 0.51(사이)이라 **TW8 이 뺀다**. 두 길이 서로를 지워 「입구 없음」(장부 `carried` = `[]` · `targets` 둘 다 `dropped`). 고칠 자리 · 근거는 §4 |
| W-4 | `prompts/consult.json:243-245`(`jev_state.turn_kind`) | **WARN** | SPEC-006 TK5 · O6-1 · E6-2 | 실측 9 턴 가운데 기대와 다른 판정 2. 「지방이 두꺼운 느낌이야」 = `follow`(new 0.27/0.30 · follow 0.75/0.72 — 두 번 다) · 「볼이 처져서요」(③) = `new` 이지만 **TK5-4 기본값으로 맞은 것**(follow 0.69 — 문턱 0.7 바로 아래). 문턱보다 지시문 쪽 문제다(§4-2) |
| W-5 | `clinic_chat/consult/turn.py:475`(`_viewing` · 하위 고민 들이기) | **WARN(코디 확인)** | 코디 답 B-2 「`said` 가 아니라 WORK 가 정한 `how=view`」 · review-work-014 W-8 | 구현은 하위 고민을 `state` = **`said`** · `how` = `view` 로 들인다. 코디 문장은 「`said` 가 아니라」 로 읽힐 수 있다. `said` 면 손님이 말하지 않은 고민이 축 고민이 되어 ① 점 재료(FD1)에 들고 ② 빈 칸 · `ask` 의 재료가 되며 ③ 「상담 상태」 에 「말한 것」 급으로 LLM 에 간다(W-8 이 짚은 위험 그대로). `focus` 는 축 고민이어야 해서 `said` 를 고른 사정은 이해된다. 코디가 한 줄로 정할 것: 지금대로(`said` + `how=view`) 받는지, `consult_view` 에서 `how=view` 를 따로 표시하는지 |
| W-6 | `prompts/consult.json:213`(절 `material`) | **WARN** | SPEC-001 0.7.2 SP3(`site_prefer` = `true` 행에는 `site_match[]` 가 붙는다) · `walk/material.py:115-117` | 절이 「`site_prefer` 표지가 없는 시술을 그 부위의 것이라고 말하지 않는다」 라고 가르치는데 **LLM 이 받는 자료 줄에는 `site_prefer` 표지가 없다** — 걷기 재료는 `site_match` 로만 싣는다(`grep site_prefer` = `listing.py` · 템플릿뿐). LLM 이 없는 표지를 기준으로 삼게 된다. 고칠 방향: 문장을 「`site_match` 표지가 없는 줄」 로 바꾼다(초안 문구 · 사용자 확인 대상 U6-2 안) |
| N-1 | 18222(GET) | NOTE | §7 | 18222 프로세스는 **19:23 에 뜬 것**이고 `server.py` 는 21:07 에 바뀌었다 — 틀에 드로어 빈 자리는 있는데 `GET /convs` = **404**. 지금 18222 는 중간 판이다. E6-6 전에 코디 재시작이 꼭 필요 |
| N-2 | `clinic_chat/consult/turn.py:379` | NOTE | TW5 | `new` 의 두 번째 걷기(`entry_pick=True`)는 첫 걷기의 글자 맞춤 후보가 **있었는데** 다 빠진 경우에도 돈다 — 그때는 입구 고르기가 안 돌아(`concepts` 가 있으면 fan-out 안 함) 같은 「입구 없음」 을 한 번 더 받는다(「지방 주사」 턴: 189 ms · Jev 요청 1 낭비). 첫 걷기 `concepts` 가 0 일 때만 다시 걷게 하면 된다 |
| N-3 | `clinic_chat/consult/listing.py:52-56` | NOTE | SPEC-001 0.7.2 §4-5 | 보고는 「`n_site_prefer` 를 읽는다」 고 했지만 코드는 행의 `site_prefer` 로 직접 센다(`n_site_prefer` 안 읽음). 값은 같다 — 보고만 고치면 된다. 묶음(고민)마다 `site_applied` 를 따로 읽는 것 · 섞이면 `prefer` + `filter` 행은 표지 행(코디 W-1)은 코드대로 선다 |
| N-4 | `clinic_chat/consult/server.py:191` | NOTE | FD4 | 누르기 라우트가 메모에 없어 허브를 부를 때 `HubError` 를 잡지 않는다 → 500. 4xx/5xx 오류 조각으로 받으면 화면이 덜 깨진다 |
| N-5 | 18222 `GET /` | NOTE | SV3 | `GET /` 는 부를 때마다 새 대화를 만든다(빈 대화 — 드로어에는 안 나옴 · 0.1 동작 그대로). 검수 GET 2 번이 빈 대화 2 개를 만들었다(턴 0 · 장부 시작 줄 없음이면 영향 없음) |
| N-6 | 보고 §3 「① 턴 6 BK2 기대와 다름」 | NOTE | WORK W-12 ④ | WORK W-12 ④ 가 이미 「① 턴 6 = `ask` null → `offered`(안전 빼고) 또는 `null`」 로 기대를 고쳤다. 실측 `close` = `null` 은 **고친 기대와 맞다**. 차이로 올릴 거리 아님 |
| N-7 | `clinic_chat/consult/e6_inputs.json` | NOTE | 공개 레포 | 사용자 e2e 질문 문장 13 개가 커밋 후보다. 개인 정보 · 키 · 내부 주소는 없다(시술 질문 꼴). 공개 레포에 두어도 되는지 코디 한 번 확인(SPEC-006 에도 같은 글이 있다) |

## 3. 볼 것 ① ~ ③ — 계약 대조

### 3-1. A1 ~ A8(① · 코드 · 시험으로 확인)

| 계약 | 확인한 자리 | 판정 |
|---|---|---|
| A1 턴 종류(TK1 ~ TK7 · TW1 ~ TW8 · TT1 ~ TT6) | `turn_kind.py` `judge`(TK5 순서 new → talk → follow · 실패 new) · `turn.py` `Consult.walk`(첫 턴 · `off` · TT6 은 요청 없이 · 걷기 task 와 가르기 함께 · `talk` = 거둠/끝까지 기다려 버림 B-3 · `follow` · `new` 다시 걷기) · `front.py` `entry_pick=False` 곧바로 「입구 없음」 | 섬(W-3 · W-4 · N-2 는 판정 값 · 경계) |
| talk 은 검색 재료를 안 씀 | `run_turn` — `talk` 면 `renumber` 안 함 · `after_talk` 는 `option` 관찰만 · 객체 안 바뀌면 `terminal=True`(조회 0 · `list` · `sites` 안 보냄) · 「앱 판정」 `seen_lines: []` · 장부 `targets` [] · `trace` = 버린 걷기 `front` 만 | 섬. 실측 E6-3 허브 resolve 2 · coverage 1 은 **거둔 걷기의 첫 단계**(재료 아님) |
| `system_v3` · 금지 낱말 | `consult.json` `system_v3` 13 절(SPEC §3-2 순서 그대로) · `version` 0.3.0-draft · `voice_check` 23 식(「직접」 · 「앱」 · 「행」 은 낱말 경계) · 검사는 꼬리 뗀 본문 · 기록만. 끈 상태 `system` 그대로 | 섬(W-6 한 줄) |
| `close` 하나 | `close.py` `pick` — ask → (empty + alt) → offered(안전 종류 뺌 CS4) → null · 꼬리 `close:` → `said` · `by=ask` · `said=0` 이면 `asked[]` 에 안 적음(`turn.py:648-649`) | 섬 |
| empty · 안전 종류 | `close.empties` 끝까지 읽어 0 만(오류 · 미완 · 실행 중단 · 범위 밖 · 입구 없음 빼고) · EM5 조합은 물은 턴만 · EM6 리스트 0 · `view` 가 `safety` 참을 달고 절 `empty` · `safety` 가 「확인된 정보가 없어요」 까지만(코디 W-5) | 섬 |
| 리스트 계열 → 시술 · 메뉴 시술 아님 · 「○○ 계열 시술」 | `listing._v3`(LS4-1 ① ② ③ · `hidden{unreached_n, names, descended_n, undescended}`) · `list_v3.html` 글 = 고민 · 계열 · 시술 이름 + 빈 자리 `mark-modality-level` = 「{name} 계열 시술」(W-10 확정 값) · `reach` · `concern_match` 는 `data-*` 만 · 「그 밖」 · 「계열 층만」 · `path[]` 이름 0 | 섬 |
| 점 누적 · 누르기 | `plan.derive` 축 고민 전부의 부위(guess · 거둔 것 빼고) · `sites.place` `concern_codes` · `asked_codes` · `match` · `focus` · `GET /c/<id>/list?concern=`(메모 → 없으면 QY1 꼴 · 받지 않는 코드 422) · htmx 속성 + JS 는 `aria-pressed` · `viewing` 만 | 섬(W-1 · N-4) |
| viewing 한 턴 | JS 가 POST 뒤 숨은 칸 비움 · 서버 `_viewing` — 글의 새 고민이 이김 · 여럿이면 `source.turn` 최근 · 객체 밖 코드 거절 기록 | 섬(W-5) |
| 드로어 · 객체 패널 env | `drawer.py` 메모리 색인 · `GET /convs` · 최근 = 마지막 턴 시각 · 턴 0 대화 없음 · `CHAT_DEBUG_PANEL` off 면 칸 · 이벤트 0 · `state` 이벤트는 `done` 앞 · 값 = 그 턴 장부 `consult` | 섬(N-1 — 18222 는 옛 판) |
| A7 FX1 · FX3 · FX4 | `state._again` 세 길 · `consult_rev` 3 · `conv-outdated` · rev 없는 켠 대화 POST 거절 · 장부 줄 안 씀(B-5) | 섬 |

### 3-2. 0.7.2 칸(②)

| 칸 | 앱이 읽는 자리 | 판정 |
|---|---|---|
| `descended[]` | `listing.py:58-67`(계열 묶음 · `procedures[]` · `from[].gid` → `from_gids`) · `material.py:104`(LS6 요약 줄 · `modality_level`) · `close._outside_rows`(EM1 셈에 넣음 — 보고 §3 실측 중 고친 것) | 맞음 |
| `sites[]` | `sites.SITES_FIELD = "sites"` 한 줄 · `match` 를 함께 읽음 · `plan.concern_sites_of` 가 물은 고민(`asked`)을 단다 | 맞음 |
| `site_applied` | 응답(묶음 = 고민)마다 `c["_applied"]` · 한 고민에 섞이면 `prefer` 로 그림 · 「앱 판정」 `site{name, applied, prefer_n}` | 맞음(코디 W-1 대로) |
| `site_prefer` | `groups[].rows[]` 의 행 표지만 셈 · 시술 · 계열을 안정 정렬로 앞에(허브는 순서 안 바꿈 — SPEC-001 §4-5 「앞에 두는 것은 앱」) · 표지 0 이면 순서 그대로 | 맞음(N-3 · W-6) |

### 3-3. 함께 쓰는 코드 · 고친 기존 시험(③)

- `walk/front.py` +18 −3: 새 인자 둘(`entry_pick` 기본 `True` · `abbr_yes_only` 기본 `False`)과 `origin == "follow"` 한 조건. **기본값이면 지나는 길이 글자 그대로 같다** — `entry_pick` 가지는 `not concepts and not carried_entries and not entry_pick` 일 때만 · `abbr` 가지는 `abbr_yes_only` 일 때만 · `origin` 은 상담만 싣는 값. `columns/col_b.py` +3 −2: 인자를 안 주면 `front()` 에 빈 `opt` — 같다. 시험 앱 쪽 시험 154 통과(§1)가 이를 받친다. 코디 W-4(줄임 판정은 상담 쪽 선택 인자로만)에 맞다.
- 고친 기존 시험 5: T24 `data-slot` +4(코디 W-2 — A8 결정) · S5-T19 `system_v3`(§15 ③) · S5-T10 `holder`(§15 ④) · `test_prompt_changed…` version(코디 답) · S5-T1 `HOWS` + `view`(B-2). **다섯 다 결정된 예외다.** `state_fixture.py` 한 줄(`concern_sites` → `sites` — 검수 N-2)도 결정된 것. 다만 깨진 둘(W-1 · W-2)은 이 목록에 없다.

## 4. 실측에서 본 것 — 판단(④)

### 4-1. 「지방 주사」 — 입구 없음(사용자가 처음 짚은 꼴이 아직 안 잡힘)

장부(`runs/consult/e6/turns.jsonl` · 두 번 돈 ① 대화)의 턴 5:

| 값 | 1 회 | 2 회 |
|---|---|---|
| 턴 종류 | `new`(0.65 — TK5-4) | `new`(0.78 — TK5-1) |
| `modality:M18` 「지방분해 주사」(줄임) | Noul **0.58** → `dropped`(TW8) | **0.51** → `dropped` |
| `concern:CON-137` 「주사」(덮인 조각) | 0.17 → `dropped` | 0.15 → `dropped` |
| 든 후보 `carried` | **[]** | **[]** |
| 끝 | 「입구 없음」 · 다시 걸어도 같음 | 같음 |

**까닭은 셋이 겹친 것이다.**

1. 앞 대상 `M18`(턴 3 대상 · 턴 4 는 `talk` 라 대상이 없어 `carry.candidates` 가 턴 3 을 잡는다 · 객체에 살아 있어 TW7 통과)이 든 후보로 **실렸다**. 그런데 이번 글에서도 `M18` 이 줄임으로 맞아서 **CR2(`front.py:238` — 「이번 글에서 맞은 것과 같은 (표, 코드)는 다시 넣지 않는다」)가 든 후보를 뺐다**.
2. 이번 글의 `M18` 은 사이 값이라 TW8(`front.py:357`)이 뺐다.
3. Jev 가 받는 후보 꼴에는 **줄임이라는 신호가 없다** — `cand_state` 는 `name` 「지방분해 주사」 · `matched`(맞은 글자)만 싣고, 지시문 `jev_front.target` 은 「the thing itself, not a word that merely contains its name」 이다. 글에 이름이 통째로 없으니 Noul 이 사이에 머문다(0.51 ~ 0.58 — 같은 글로 두 번 재도 흔들린다).

**문턱으로는 고치지 않는 것을 추천한다.** 전체 yes 0.7(`config.py`)은 시험 앱 B 열 · 거둠 · 턴 가르기가 함께 쓴다. 줄임만 따로 문턱(예: 0.5)을 두면 0.51 은 겨우 넘지만, 0.1 의 오독 「주사」 가 0.49 였던 것과 거리가 없다 — 잡음 폭 안이다.

**고칠 자리(추천 순서):**

| # | 어디 | 무엇 | 왜 |
|---|---|---|---|
| ⓐ(추천 1) | `front.py:357-358` 의 `abbr_yes_only` 가지(상담만 지나는 길) | 줄임 후보가 **사이 값이고 같은 (표, 코드)가 이번 턴 든 후보(= 객체에 살아 있는 앞 대상)에 있으면** 대상으로 둔다(`target` · `read_as` 에 `by: "abbr+carry"`). 객체에도 그 칸의 원래 급으로 둔다 | 손님이 앞에서 「지방분해주사」 라고 **말한** 것을 줄여 다시 부른 것이다 — 대화 맥락이 줄임을 받친다. CR2 와 TW8 이 서로를 지우는 구멍을 막는다. 결정론 · Jev 요청 0 더함 · 시험 앱 무변경(코디 W-4). **SPEC-006 TW8 에 한 줄 보탬**이 필요하다(코디 — 「앞 대상과 같은 줄임 후보는 사이 값이어도 대상」) |
| ⓑ(추천 2) | `front.py` `cand_state`(상담만 — `abbr_yes_only` 일 때만 칸 하나) + `prompts/consult.json` `jev_front.target` 한 문장 | 줄임 후보에 `abbreviated: true` 를 싣고 지시문에 「`abbreviated` 가 참이면 글이 그 이름을 줄여 썼다(가운데 글자가 빠진 꼴) — 줄인 말이 이 후보를 뜻하는지로 판단하고, 이름이 통째로 없다는 까닭만으로 낮추지 않는다」 를 더한다 | 맥락 없이 처음 줄여 말한 턴(「지방 주사 알려줘」 첫 턴)을 위한 것. 문구는 영어 초안 · 사용자 확인 대상(U6-2). E6 ① 턴 5 를 같은 글로 여러 번 재서(지금 0.51 ~ 0.58 흔들림) 넘는지 본다 |
| ⓒ(같이) | `turn.py:379` | N-2 — 첫 걷기에 글자 맞춤 후보가 있었으면 TW5 다시 걷기를 하지 않는다 | 같은 「입구 없음」 을 두 번 받는 것을 없앤다 |

ⓐ 만으로 사용자가 짚은 대화(① 턴 3 → 5)는 잡힌다. ⓑ 는 처음 말한 줄임까지 넓힌다.

### 4-2. 턴 종류 오판 둘

| 글 | Noul(new · talk · follow) | 판정 | 결과에 닿는 것 |
|---|---|---|---|
| ① 턴 2 「지방이 두꺼운 느낌이야」(앞 = 턱살) | 0.27 · 0.54 · **0.75** / 0.30 · 0.57 · **0.72** | `follow`(TK5-3) — 두 번 다 | 첫 걷기 글자 맞춤 0 → TW4 로 **턱살(CON-168)을 다시 걷는다** → 턴 1 과 같은 리스트 · 답. 기대(`new` → 입구 고르기 → 얼굴 지방 · 국소 지방)와 다르다 |
| ③ 턴 2 「볼이 처져서요」(앞 = 써마지 · BK2 고민 묻기) | 0.36 · 0.45 · **0.69** | `new`(TK5-4 — 기본값) | 결과는 맞다. 그러나 follow 가 0.01 차로 문턱 아래였다. 넘었어도 첫 걷기가 「볼」 을 글자로 잡아 TW4 는 그 대상을 그대로 쓰므로 **이 턴은 해가 없다** |

**판단**: 문턱이 아니라 지시문이다. 지금 `tk_new` 는 새 것을 「concern, procedure, product, body site, or information」 이라는 **이름 꼴**로만 적고, `tk_follow` 는 「without naming anything new」 라 **자기 상태를 새 말로 풀어 말한 것**(이름이 없는 증상 묘사)이 follow 로 간다. ③ 은 앱이 물은 것(`prev.ask`)에 대한 답인데 세 물음 어디에도 「`ask` 에 답함」 자리가 없어 follow · talk 로 흩어진다.

**고칠 자리**(`prompts/consult.json:243-245` · 영어 초안 · 사용자 확인 대상):

- `new` 에 더함: 「손님이 자기 상태 · 증상 · 어디가 어떻게 보이거나 느껴지는지를 새 말로 말하는 것(고민 이름이 없어도)」 · 「`prev.ask` 에 고민 · 부위 · 선택지로 답하는 것」 도 new 다.
- `follow` 에 더함: 「앞 대상 **그 자체**에 대해 정보(효과 · 가격 · 부작용 · 방법 등)를 더 묻는 것만 — 손님이 자기 상태를 말하는 것은 follow 가 아니다」.
- `talk` 의 「giving a short reply」 에 「앱이 물은 것에 고민 · 부위로 답하는 것은 빼고」 를 더한다(TT1 이 선택지는 받지만, 새 부위 · 고민 말은 놓친다).
- 문턱(0.7)은 그대로. E6-2 는 9 턴뿐이라 문턱을 보정할 표본이 안 된다 — 지시문을 고친 뒤 같은 9 턴 + 「자기 상태 묘사」 꼴 몇 턴을 다시 잰다(O6-1).
- 「지방이 두꺼운 느낌이야」 를 턱살 이어 말하기(follow)로 보는 것도 말이 된다 — 기대가 `new` 인 것은 SPEC §11-3 의 「(가정)」 이다. 어느 쪽이 맞는지는 **사용자 결정**으로 올린다.

## 5. 커밋 후보 grep(⑥)

- `git status --porcelain`: 고친 32 · 새 21(모듈 5 · `e6_inputs.json` · 템플릿 5 · 시험 10). gitignore = `.env` · `runs/` · `data/` · 캐시.
- `grep -nE "/Users/|sk-ant|ANTHROPIC_API_KEY=.+|api_key = '…'|http(s)://…"`(커밋 후보 전부 · localhost · 127.0.0.1 · CDN 뺌) = **0**. README 의 주소는 `127.0.0.1` 만.
- `e6_inputs.json` 의 질문 글 — N-7.
- `_face.svg` · `face_coords.py` — `git status` 에 없다(안 바뀜).

## 6. 사용자가 실물에서 만날 자리(⑦ · 18222 GET)

1. **지금 18222 는 옛 판이다**(19:23 기동 · 코드는 21:07 까지 바뀜) — 틀에 드로어는 보이는데 `GET /convs` 404 라 **턴이 끝날 때 드로어 목록 다시 받기가 실패**한다. 객체 패널 칸(`#consult-state`)도 없다. E6-6 전에 코디가 `CHAT_STATE=on` · `CHAT_DEBUG_PANEL=on` 으로 다시 띄워야 한다(N-1).
2. 0.2 로 시작한 켠 대화를 드로어에서 열면 `conv-outdated` 표지 + 새 대화 길만 있고 **턴을 받지 않는다**(FX4) — 사용자가 옛 대화를 이어 쓰려다 막힌다. 「의도된 것」 이라고 미리 알리면 좋다.
3. 「지방 주사」 는 여전히 「무엇을 말씀하시는지」 되묻는다(W-3). 「지방이 두꺼운 느낌이야」 는 턱살 리스트 · 답을 되풀이한다(W-4).
4. ① 턴 3 처럼 `empty` 가 있어도 `focus` 고민 리스트에 다른 계열이 없으면 `alt` 가 없고 `offered`(패키지)로 맺는다 — 「같이 받는 조합 정보는 없어요 … 패키지 정보를 볼까요?」 꼴. 어색하면 E6-6 지적 거리(보고 N-6 꼴).
5. 빈 자리 문구(드로어 넷 · `mark-site-prefer` · `conv-outdated` · `label-concern-title` 등)는 아직 값이 없어 **글 없는 버튼 · 머리**로 보인다 — 「새 대화」 버튼이 빈 버튼일 수 있다(문구 사용자 몫).
6. 객체 패널은 코드 · 장부 키가 그대로 보인다(개발용 — SV10).

## 7. 남은 것

- 커밋 전: W-1(코드 한 줄 또는 시험 한 줄) · W-2(시험 한 줄 + 달리 받음 ④ 넓힘) — **코디 결정**.
- W-3 ⓐ · ⓑ · W-4 지시문 — 코디 · 사용자(TW8 한 줄 보탬 · 영어 초안 문구) → 고친 뒤 E6 ① 턴 2 · 5 · ③ 턴 2 다시 재기.
- W-5 B-2 해석 — 코디 한 줄. W-6 절 `material` 한 문장.
- 18222 재시작 → E6-6.
