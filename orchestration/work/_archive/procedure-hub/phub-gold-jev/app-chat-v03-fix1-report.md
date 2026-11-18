# [app] 상담 0.3 수정 1 보고 — 코드 검수 WARN 6

2026-11-17 · app 워커 · 워크트리 `clinic_chat/phub-gold-jev`(미커밋 0.3 위 · **커밋 안 함**) · 지시서 `app-chat-v03-fix1-instructions.md`. 얼굴 파일 · 허브 안 건드림.

## 1. 고친 것

| # | 파일 | 무엇 |
|---|---|---|
| W-1 | `consult/turn.py` `screen()` | 그 턴 diff 에 `focus` 가 있으면 빈 조각이어도 `sites` 를 보낸다(FD3 글자 그대로). |
| W-2 | `tests/test_state_synergy.py` S5-T11 | 아래 §2. |
| W-3 ⓐ | `walk/front.py` `abbr_yes_only` 가지 | 줄임 후보가 **사이 값**이고 같은 (표, 코드)가 `carry`(앞 대상)에 있으면 `target`. trace `targets[].by = "abbr+carry"` · `Entry.read_as = {by: abbr+carry, table, code}` · 장부 `targets[].read_as = {by: abbr+carry}`. 객체는 **원래 급 그대로**(`state.py` `KEEP` — history 만 +1 · 객체에 없으면 `guess`). |
| W-3 ⓑ | `walk/front.py` `cand_state` · `walk/jev_requests.py` `_target_instr` · `consult/prompt.py` 로더 · `prompts/consult.json` `jev_front.target_abbr`(새 절 · 영어 초안) | 상담일 때만 줄임 후보에 `abbreviated: true`. 그 후보는 `target_abbr` 절로 묻는다. `target` 절은 시험 앱 `front.md` 와 글자가 같아야 해서(CR7 시험 `test_jev_front_sections_equal_test_prompt` · `test_t13_no_carry_same_as_before`) 따로 절로 뺐다. |
| W-4 | `prompts/consult.json` `jev_state.turn_kind`(영어 초안) | `new`: 자기 상태를 새 말로 묘사(예: "the fat feels thick") = new · `prev.ask` 에 고민 · 부위 · 선택지로 답(새 항목이 드는 답) = new. 겹치지 않게 `talk` 에 「`prev.ask` 에 고민 · 부위로 답한 것은 talk 아님」 · `follow` 에 「앞 대상 자체의 정보만 · 자기 상태 묘사는 follow 아님」(검수 §4-2 제안 그대로). 문턱 0.7 그대로. |
| W-5 | `consult/render.py` `state_view` · `consult/turn.py` `_viewing` | 지금대로(`said` + `how=view`). 장부 `consult.viewing.how` = `"view"`(하위 고민을 들인 턴)/`null`. 객체 패널에 `how=view` 칸(누르기로 든 고민 code · name · state)과 `viewing` 칸을 따로 보인다. |
| W-6 | `prompts/consult.json` 절 `material` | 「`site_prefer` 표지가 없는 시술」 → 「`site_match` 표지가 없는 줄의 시술」(초안). |
| N-2 | `consult/turn.py` TW5 | 첫 걷기에 글자 맞춤 후보(`resolve_candidates`)가 있었으면 입구 고르기로 다시 걷지 않는다. |
| N-4 | `consult/server.py` 누르기 라우트 | `HubError` → 오류 조각 `data-error="hub"` · 502(500 아님). |
| — | `prompts/consult.json` `version` | `0.3.0-draft` → **`0.3.1-draft`**(사용자 확인 대상 — `target_abbr` · `turn_kind` · `material` 세 곳). |

NOTE 나머지: N-1 · N-5(18222 재시작은 코디 몫) · N-3(보고 문구 — 코드 그대로 `site_prefer` 행 표지로 센다) · N-6(차이 아님) · N-7(코디 확인) — 코드 안 고침.

**함께 쓰는 코드 줄 수**(이번 수정 분): `walk/front.py` +16 −2 · `walk/jev_requests.py` +2 · `columns/col_b.py` 0. HEAD 대비 합: front +34 −5 · jev_requests +2 · col_b +3 −2. 새 가지는 전부 `abbr_yes_only=True`(상담만) 또는 `abbreviated` 칸(상담만 실음) + `target_abbr` 절(상담 프롬프트만)에서만 지난다 — 기본 인자면 지금과 같음(시험 앱 시험 통과).

## 2. 고친 기존 시험 · 까닭

| 시험 | 고친 것 | 까닭 |
|---|---|---|
| `test_state_synergy.py::test_s5_t11_complement_lines_inside_only_once` | `lines[0]["rows"] == 2` → `"rows" not in lines[0]` + 장부 `queries` 의 QY4 `total == 4` + 장부 `material.new_lines` 그 요약 줄 `gids` 2 | 코디 W-2 — 달리 받음 ④ 에 시너지 요약 줄 `rows` 포함(EM4 — LLM 에 행 수 안 줌) · 행 수는 장부로 센다 |
| `test_v03_prompt.py` (version 단언) | `"0.3.0-draft"` → `"0.3.1-draft"` | 프롬프트 초안 바꿈(W-3 ⓑ · W-4 · W-6) |
| `test_v03_sites.py::test_s6_t19_viewing_moves_focus` | `viewing` 같음 단언에 `"how": None` | W-5 — 장부 `viewing.how` 칸 더함 |

새 시험: `test_v03_shared.py` +2(W-3 ⓐ 앞 대상 줄임 = target · 다른 앞 대상이면 TW8 그대로 · 기본 인자 = 지금 동작 / W-3 ⓑ `target_abbr` 절 쓰임) · `test_v03_fixes.py` +1(abbr+carry = 원래 급 그대로) · `test_v03_sites.py` W-5 단언(장부 · 패널 칸).

## 3. 시험(고친 곳 관련 파일만 · 전체 pytest 안 돌림)

- `uv run ruff check .` — All checks passed.
- 돌린 파일 21: test_state_list · test_state_synergy · test_v03_shared · test_v03_fixes · test_v03_prompt · test_v03_sites · test_v03_turn_kind · test_v03_frame · test_v03_e6 · test_consult_turn · test_consult_prompt · test_consult_carry · test_walk_front · test_walk_core · test_walk_entry · test_columns · test_state_carry · test_state_object · test_consult_sites · test_state_blanks · test_consult_material — 마지막 묶음 실행 **193 passed**(+ 따로 돌린 test_columns 포함 묶음 119 passed) · 실패 0. 검수에서 깨졌던 둘(S5-T12 · S5-T11) 통과.

## 4. 실물 — 18223(CHAT_STATE=on · CHAT_DEBUG_PANEL=on) · 18105 는 읽기 호출만 · 끝나고 내림(`lsof` 0)

대화 `79b290325ac2446c` · 장부 `runs/consult/turns.jsonl`(gitignore).

| 턴 | 글 | 턴 종류(Noul new·talk·follow) | 대상 | 리스트 | 점 | 끝맺음 |
|---|---|---|---|---|---|---|
| 1 | 지금 턱살이 너무 많아서 고민이야 | 첫 턴(TK2) | CON-168 턱살(0.95) | CON-168 — 시술 0 · 계열 0 · 「그 밖」 V라인주사 1 | SITE-072(focus) | `ask` |
| 2 | 지방이 두꺼운 느낌이야 | **`new`**(0.93 · 0.50 · 0.10 — 수정 전 follow 0.75) | 입구 고르기 → CON-169 얼굴 지방 · CON-181 국소 지방(`by` noul) | 안 보냄 | 안 보냄 | `null` |
| 3 | 지방분해주사랑 같이 맞는 시술이 궁금해 | `new`(0.72) | M18 지방분해 주사(0.86) | CON-168 그대로 + 관심 M18 · 시너지 묶음 1 | 안 보냄(같음) | `offered`(lineup · package) · `empty` = M18 × 조합 |
| 4 | 왜 채우지를 못한거야 | `talk`(0.78) | 0 | 안 보냄 | 안 보냄 | `null` |
| 5 | 아니 지방 주사랑 같이 하면 좋은 시술 알려달라고 | `new`(TK5-4 · 0.68) | **M18 — `target` · `by` abbr+carry(Noul 0.67)** · 장부 `read_as {by: abbr+carry}` | 안 보냄(같음) | 안 보냄 | `offered`(overview · package) · `empty` = M18 × 조합 |

- **W-3 잡힘**: 턴 5 가 「입구 없음」 이 아니라 M18 대상 → QY4 조회 · 답이 지방분해 주사 안 시술 · 제품을 말함. 다만 허브 조합(보완) 행이 M18 에 0 이라 「같이 하면 좋은 시술 정보는 없어요」 는 그대로 — 데이터 몫.
- **W-4 잡힘**: 턴 2 가 `new` → 입구 고르기로 얼굴 지방 · 국소 지방을 걸어 답에 나옴.
- **새로 본 것(안 고침 · 코디 판단)**: ① 턴 2 의 입구 고르기 대상(얼굴 지방 · 국소 지방, `by` noul)이 **객체에 들지 않는다**(객체 재료 = `trace_front.targets` 뿐 — UP1 · 0.2 동작) → focus 는 턱살 그대로 · 리스트 · 점 안 바뀜. 답에는 두 고민이 나오는데 리스트는 그대로라 화면이 어긋난다. ② 턴 1 리스트가 시술 0 · 계열 0 · 「그 밖」 1 뿐(0.3 구현 보고 실측은 M18 묶음 시술 6) — 이번에 리스트 코드는 안 건드렸으므로 18105 의 지금 데이터(데이터 판 작업 중) 탓으로 보인다(확인 안 함).

## 5. 남은 것

- 사용자 확인: `prompts/consult.json` 0.3.1-draft 의 세 문구(`jev_front.target_abbr` · `jev_state.turn_kind` · 절 `material`) · SPEC-006 TW8 한 줄 보탬(「앞 대상과 같은 줄임 후보는 사이 값이어도 대상」).
- 코디: §4 새로 본 것 ①(입구 고르기 대상의 객체 반영) · ② 데이터 확인 · 18222 재시작(N-1) · N-7.
- 커밋 안 함.
