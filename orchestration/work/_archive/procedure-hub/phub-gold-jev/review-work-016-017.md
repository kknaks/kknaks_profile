# 검수 — WORK-016 허브 resolve 0.8.1 · WORK-017 앱 상담 0.4 (+ SPEC-008 0.2.0 · SPEC-001 0.8.1 고친 곳)

**판정: WARN** — SPEC 의 F-1 ~ F-16 처분은 코디 답과 맞고 새로 생긴 계약 구멍은 없다. WORK 두 개는 SPEC 줄을 빠짐없이 WP 에 나눴고 완료 조건(D-14 · U8-2 · U8-4 · 답 LLM 실제 호출 5 대화 · 포트 · 커밋 금지)도 맞다. 다만 **표면 전수에 빈 곳이 셋 있다**: ① 허브 시험 가운데 표 밖에서 깨지는 자리(`test_gold_contract` 의 `abbr` 입력 · 문장 입력 · NM 부록 줄, `headers.py` 의 상수 둘) ② 앱 시험 가운데 끈 대화를 새로 여는 기존 시험 넷 ③ 채점기 「고치기 전 출력」 을 뜨는 길이 조사 산출물을 덮을 수 있다. 셋 다 WORK 에 줄 몇 개를 보태면 닫힌다(재설계 아님).

검수 범위: `WORK-016-hub-resolve-v081.md` 전부 · `WORK-017-consult-v04.md` 전부 · `SPEC-008-consult-entry.md` 0.2.0(변경 기록 · §1-2 · §2 · §3-4 · §4-2 · §6-1 · §7 · §8) · `SPEC-001-hub-gold-mcp.md` 0.8.1(변경 기록 0.8.0 · 0.8.1 · §4-1 · §5-1 · §10 O-32 · O-33). 대조: `review-spec-008.md` · `_RESUME.md` §2 11-18 맨 위 두 행 · `work-016-017-brief.md` · `spec-008-fix1-brief.md` · `research-input-space/conversations.jsonl`(78 대화 · 356 턴) · `scripts/{paths,score,slim,run_now}.py` · 허브 `PROCEDURE-HUB/phub-gold-jev`(HEAD `d97a9ad` · 깨끗함) · 앱 `clinic_chat/phub-gold-jev`(HEAD `be1c622`). 서버 · DB · LLM · Jev 를 부르지 않았다. 아무것도 고치지 않았다.

## 결함 표

| # | 심각도 | 자리 | 무엇 | 근거 | 고칠 방향 |
|---|---|---|---|---|---|
| R-1 | **Medium** | WORK-016 §5-1(H 표) · §1 · WP-2 완료 조건 4 | **표 밖에서 깨지는 허브 자리가 남았다.** ⓐ `test_gold_contract.py:191` `V07_CALLS` 의 `("resolve", {"text": "푸른하별빛 좋아", "abbr": "off"})` 는 0.8.1 에서 `invalid_argument` 를 내므로 `test_T3_v07_response_fields`(204 ~ 209)가 깨진다. ⓑ 같은 파일 `SYN_CALLS[0]`(166 · `"겹침 시술가랑"`) · `V07_CALLS[0]`(191 · `"가나 마바사 어때"`)는 문장이다. 0.8.1 에서 후보가 0 이 되어 `check_response` 의 `matched` 꼴 검사가 **빈 검사**로 통과한다. ⓒ `V07_LINES` 의 `("g_entry", NM_ENTRY_COLUMNS)`(188)는 부록 A 에서 지운 NM 줄이다. 그런데 앱 쪽 `headers.py:151` `NM_ENTRY_COLUMNS` · `:114` `MATCHED_HOW` 처분이 WP-1 에 없다(§1 표는 `MATCHED_FIELDS` · `MATCHED_ABBR_FIELDS` 만 적었다). WP-2 완료 조건 4 의 `rg` 꼴(`HOW_ABBR\|HOW_PART`)은 `MATCHED_HOW` 를 못 잡는다. 이대로면 §7 완료 조건 2 「그 밖에서 깨진 시험 0」 이 서지 않는다 | `rg -n '"resolve"' backend/tests`(이 검수) · `test_gold_contract.py:16,31,34,92-96,165-166,188-209` · `headers.py:112-114,151` · SPEC-001 부록 A 1190 행 | H 표에 H-17 을 더한다(`test_gold_contract` `V07_CALLS[1]` 은 `abbr` 를 뺀 이름 하나로 · `SYN_CALLS[0]` · `V07_CALLS[0]` 은 합성 이름 하나로 · `V07_LINES` NM 줄은 지움). WP-1 `headers.py` 줄에 `MATCHED_HOW` · `NM_ENTRY_COLUMNS` 지움을 더한다. `rg` 꼴에는 `MATCHED_HOW\|NM_ENTRY` 를 더한다. ★ 수 · 고침 수는 다시 센다 |
| R-2 | **Medium** | WORK-017 §15-4 | **끈 대화를 새로 여는 기존 시험 넷이 표에 없다.** CP1(새 대화는 설정이 `off` 여도 켬)로 아래 넷이 켠 가지로 돌아 기대가 깨진다. 넷 다 WP 「돌릴 파일」 안에 있어 첫 실행에서 바로 떨어진다. ⓐ `test_v03_prompt.py` `test_s6_t8_on_conv_uses_v3_off_conv_uses_0_1`(83 — `Run(state="off")` → 0.1 시스템 sha 단언) ⓑ 같은 파일 `test_s6_t9_off_conv_judgement_is_0_1`(121) ⓒ `test_v03_frame.py` `test_s6_t29_off_conv_panel_is_empty_bundle`(161) ⓓ `test_state_blanks.py:119` 의 `r2 = Run(state="off", chat_prompt_file=bad)` → 「끈 대화는 된다」(`state_ready` 거짓이어도 끈 대화는 돈다 — 0.4 에서는 새 대화가 켬이라 `prompt` 오류). §15-4 의 `test_v03_prompt` 줄은 `state_ready` 단언만 · `test_v03_frame` 줄은 `consult_rev=3` 픽스처만 · `test_state_blanks` 줄은 `:107` · `:113` 만 적었다 | `tests/state_fixture.py:191-197`(`Run(state=…)` → `chat_state`) · `rg -n 'state="off"' tests`(이 검수 — 9 자리 가운데 §15-4 가 다룬 것은 `test_state_object:174` · `test_state_examples:93` 둘) · SPEC-008 CP1 · S8-T19 | 네 자리를 §15-4 에 넣는다. 처분 제안: 「끈 대화의 0.1 동작」 을 보는 시험(ⓐ 뒤 반 · ⓑ · ⓒ · ⓓ 뒤 반)은 S8-T19(새 대화는 켬 · 옛 끈 대화는 막힘)와 겹치므로 지우거나, 장부에 `off` 시작 줄을 둔 **옛 대화**로 「열기만 되고 턴은 막힘」 을 보게 고친다. ⓐ 앞 반(켠 대화 = v3)은 그대로 둔다. 까닭 칸 = CP1 · CP7 |
| R-3 | **Medium** | WORK-017 §15-3 WP-11 끝 조건 ① · B-6 · §16-1 E8-3 명령 | **「고치기 전 출력」 을 뜨는 길이 조사 산출물을 덮을 수 있다.** `score.py` 의 출력 자리는 env 가 아니라 스크립트 자리에서 센 `OUT`(`paths.py:4` = `research-input-space/`)이다. 고치기 전 `score.py` 를 그대로 돌리면 `now-turns.jsonl` · `pick-*-turns.jsonl` · `fail-by-tag.csv` · `summary.json` 을 덮어쓴다(`score.py:211,282,295,300,322,326`). WORK 는 「세션 임시 폴더에 고치기 전 출력을 떠 두고 견준다 — 덮지 않는다」 고만 적어 어떻게 뜨는지가 없다. 또 `score.py` 는 표도 `OUT+"/conversations.jsonl"`(`:14`)로 읽는다. 그래서 `INPUT_SPACE_OUT` 이 `OUT` 을 통째로 바꾸면 표를 못 읽는다. 출력 자리만 바꾸는지가 적혀 있지 않다 | `scripts/paths.py:3-9` · `score.py:4,14,21,211-326` · README(「score.py 가 덮어쓴다」 — WORK B-6) | 차례를 박는다: ⓐ 고치기 **전에** 지금 `$RS` 의 다섯 산출물을 세션 임시 폴더에 복사한다(기준 = 지금 파일 · 「고치기 전 실행」 을 하지 않는다) ⓑ `INPUT_SPACE_OUT` 은 **쓰는 자리만** 바꾼다(표 · `RUN` 읽기는 그대로) ⓒ 끝 조건 ① = 고친 `score.py` 를 `INPUT_SPACE_OUT=<임시>` 로 옛 장부에 돌려 ⓐ 의 `summary.json` 과 견준다. 지금 `summary.json` 이 지금 표(356 턴)로 낸 것이 아니면 ⓐ 의 기준을 무엇으로 할지를 보고에 적는다 |
| R-4 | Low | WORK-017 §4 X 표 · WP-4 | **OU12 「`source` 의 `noul` · `decision` · `matched` · `covered_by` 없어짐」 을 내는 자리가 하나 더 있다.** `turn.py:479`(점 누르기 viewing → 하위 고민을 객체에 들임 · `how = view`)가 그 넷을 `None` · `"view"` 로 싣는다. X 표 · WP-4 는 `observe_accepted` 만 다룬다. §4 grep 꼴(`nouls` 만 · `noul":` 없음)이 이 줄을 못 잡는다. 그 밖에 `turn.py` 는 grep 에 43 줄로 걸린다(WORK 는 44 — 뜻은 같다). `e3.py:35` · `e5.py:30` 의 옛 실측 도구도 `noul` 을 읽는데 `e6.py`(B-8)처럼 처분이 적혀 있지 않다 | 앱 `turn.py:476-481` · `e3.py:35` · `e5.py:30` | X-28 을 더한다(`turn.py:479` `source` 를 OU12 꼴로 — `sure` 칸 값은 WORK 가 정함. 제안: 손님이 말한 것이 아니라 `how = view` 이므로 `null`). `e3.py` · `e5.py` 는 B-8 줄에 함께 적는다(안 고침) |
| R-5 | Low | WORK-017 B-4 · WP-2 · WP-9 | **SPEC 이 「WORK 에서 정한다」 고 맡긴 글자를 WORK 가 다시 구현 워커에게 넘겼다.** 답 요약 줄 · 리스트 줄의 머리 글자와 `marks.same_list` 는 「시안에 있으면 그대로 · 없으면 짧은 기호 꼴」 로만 적혀 있다(시안 `pick-prompt.md` 에는 그 줄이 없다 — 이 검수 확인). 프롬프트 글자를 구현 워커가 짓게 된다(사람에게 안 보이지만 `pick` 은 사용자 확인 대상이다). `marks.none` = 「없음」(UC6) · `marks.failed` = `(이해 실패)`(FL4)는 SPEC 에 글자가 있다 | SPEC-008 §7 끝 불릿(523 행) · UC6 · FL4 · `pick-prompt.md` 머리 줄 | B-4 에 글자를 박는다(예: 머리 둘 · `same_list` 하나 — 코디가 정하거나 WORK 가 제안 값을 적고 O-2 「사용자 확인」 에 넣는다) |
| R-6 | Low | WORK-016 §0 · §5 · H-6 · H-4/H-5 | ⓐ §0 은 「SPEC 표 8 파일 + grep 으로 더 찾은 3 파일」, §5 는 「8 줄 = 7 파일 + 표 밖 파일 2 = 9」 다(§5 가 맞다). ⓑ H-6 「`OLD_FRAGMENTS` 가 『남아 있어야』 인지 『없어야』 인지 읽고 맞춘다」 — 이 검수가 읽었다. **「있어야」 단언이다**(`test_gold_v07_compat.py:93-94` · `:109` `frags + OLD_FRAGMENTS[tool]` 가 설명 안에 있음을 단언). 그래서 「부분 문자열」 · 「조사를 떼지 않는다」 는 목록에서 빼고, 「없음」 단언은 T29 쪽(H-10)에 둔다. ⓒ H-4 · H-5 뒤 `TEXTS` · `MATCHED_06` · `RESOLVE_REQUEST_06`(`:32-33,42`)이 쓰는 곳 없이 남는다 | 허브 `test_gold_v07_compat.py:32-42,88-118,128-130` | ⓐ 수를 하나로 맞춘다 ⓑ H-6 을 확정 문장으로 바꾼다 ⓒ 세 상수 지움을 H-4 에 붙인다 |
| R-7 | Low | WORK-016 §6-1 · WORK-017 §16-2 | **18105 재시작이 O-33 보다 앞에 적혀 있다.** 상담 앱과 시험 앱의 기본 허브 주소가 같은 18105 다(`config.py:40-41`). 그래서 「검수 PASS 뒤 18105 를 0.8.1 로」 하면 시험 앱 B · C 열(D-2 · O-33 (a) — 0.7.2 옛 판에 묶음)이 그 순간 0.8.1 에 붙는다. O-33 은 「시험 앱을 다시 돌릴 때(코디)」 로 미뤄져 있다 | 앱 `clinic_chat/config.py:40-41` · SPEC-001 O-33 · 변경 기록 0.8.0 B 열 줄 | 코디 몫 표에 「18105 를 올리기 전 · 또는 같이: 시험 앱이 붙을 0.7.2 허브 자리(옛 커밋 워크트리 · 다른 포트)를 정한다」 한 줄을 더한다(정하는 것은 코디) |

## 볼 것별 결과

### 1. SPEC 고친 곳(F-1 ~ F-16 ↔ 코디 답)

| F | 코디 답 | SPEC 0.2.0 · 0.8.1 | 판정 |
|---|---|---|---|
| F-1 ⓒ | 끈 상태 새 대화 안 엶 · 옛 끈 대화 읽기만(문구 빈칸) · 0.4 켠 상태는 0.7.2 로도 돎 | CP1 · **CP7** · S8-T19 · U8-3 · C8-8 · SPEC-001 0.8.1 영향 표 끈 상태 줄 + 「같이 올리는 것 필수 아님」 · 0.3 앱 줄 「0.3 앱을 0.8.0 허브에 붙이지 않는다 · 앱 0.4 만 먼저는 된다」 | 맞음. 새 구멍 = R-7(같은 18105 를 시험 앱이 쓴다 — 코디 순서 몫) |
| F-2 | 고정 수 → score.py 가 낸 수 | §8-1 · 표 판 78 · 356 · 애매 18 은 참고 | 맞음(이 검수가 다시 셈: 78 대화 · 356 턴 · 애매 18 · 정보 종류 키 156) |
| F-3 | 답 LLM 실제 호출 · 그 턴이 든 대화 전부 · 직접 세기 | 5 턴 = C56-5 · C57-2 · C58-3 · C65-4 · C69-2 · 5 대화 25 턴 · 「7」 과 갈린 까닭 | 맞음(이 검수가 `key.ref.to = answer` 로 다시 셈 — 같은 5 · 25 턴) |
| F-4 | 리포트대로 | §6-1 `consult.site_filter` · E8-pre | 맞음 |
| **F-5** | 「답」 = 앞 턴 되물음에 대한 답 · 네 턴 표 | OU7 ⓓ(앞 턴 `consult.ask.slot = concern` · `about` = 그 부위) · §8-1 표(C05-2 · C15-3 · C28-3 맞음 · C38-4 갈림 → E8-5 이름 박음) | 맞음. C15-3 · C28-3 은 앞 턴에 `focus` 가 있어 QY7 이 안 서므로(`blanks.py:45`) 키 `[]` 와 맞는다는 근거가 섰다 |
| F-6 | E8-6a = 있는 키 · U8-1 (가) · U8-2 90% · 값 · 깊이 키 20↑ | `key.material{rows, depth}` 22 턴(C74 ~ C78) · E8-6b 검사 ⓐ ⓑ ⓒ · U8-4 를 새로 올림 | 맞음(이 검수 확인 — `material` 키 22 · C74 ~ C78 22 턴). U8-4 는 11-18 코디 답 ⓐ 90 · ⓑⓒ 100 으로 닫혔다 |
| F-7 | 리포트대로 | §7 적재기 계약 표 | 맞음 |
| **F-8** | 부위는 늘 `targets` 에도 · `sites` = 거르개 | UC8 · VF8 ⓐ ~ ⓒ · OU3 · OU7 · QM3 · §7 | 맞음(ⓑ ⓒ 앱 받침은 「제안」 으로 밝힘) |
| F-9 | 말 차례 · focus = 마지막 고민 | OU9 · §7 규칙 1 · S8-T6 | 맞음 |
| **F-10** | 서명 표 · `walk/` 얇은 감쌈은 diff 0 예외 · S8-T18 고침 | §3-4 표 · S8-T18 · C8-9 | 맞음. 이 검수가 서명 19 개를 앱 코드에서 열어 봄 — `plan_calls` · `read_calls` · `scope_links` · `group_targets` · `_coverage` · `nonzero_rows` · `_kind_rows` · `_ranges_for` · `range_of` · `is_attr_start` · `_labels` · `same_day_marks` · `_end_check` · `rq1` · `DepthResult` · `depth_candidates` · `depth_calls` · `build` · `roster` · `check` · `es.decide` · `Walk` · `FrontResult` 의 자리 · 서명이 표와 같다 |
| F-11 | 리포트대로 | SPEC-001 0.8.1 고칠 · 지울 시험 표 8 줄 | 맞음. 다만 표 밖 자리는 WORK-016 이 ★ 6 을 더 찾았고, 이 검수가 R-1 을 더 찾았다(표의 「같은 처분」 규칙으로 닫힌다) |
| F-12 ~ F-16 | 리포트대로 | QS6 · §6-1 · VF4 · VF10(`walk/kinds.py:38` — 이 검수 확인) · 줄 번호 · 출처 · 예문 | 맞음 |

새 계약 구멍: 없음(R-1 · R-7 은 WORK · 운영 순서 몫).

### 2. WORK ↔ SPEC 계약 줄

- **WORK-016**: §9 대응표의 줄(§4-1 입력 · 계산 필드 · 순서 · 도구 설명 · 목록 꼴 · §5-1 R1 ~ R9 · §5-11 NM · §3-1 · §9 T13 · T15 · T23 · T26 · T27 · T29 · O-32 · 변경 기록 0.8.0 · 0.8.1 · 부록 A)를 하나씩 대 봄 → 빠진 줄 없음. 부록 A 의 NM 줄 지움이 WP-1 의 `headers.py` 줄에 빠졌다(R-1 ⓒ). O-32 (a) 「`abbr` 없앰」 을 「스키마에 남기고 주면 거절」 로 받은 것은 A-3 으로 밝혔다(REST 가 모르는 쿼리를 버리면 SPEC 「주면 `invalid_argument`」 가 안 선다 — 까닭 맞음 · 코디 되적기 몫).
- **WORK-017**: §18 대응표 — LD · UC · VF · OU · QS · QM · DT · BQ · AN · KS · DP8 · VP8 · §3-4 · FL · 설정 · AR · 장부 · 패널 · SSE · `pick` · 적재기 · E8-0 ~ E8-7 · S8-T1 ~ T20 · §9 를 하나씩 대 봄 → 빠진 줄 없음. 같은 줄을 둘이 다르게 맡는 곳 없음(OU7 은 WP-4 `site_filter.decide` 하나 · QS1 은 WP-5 가 그 값을 읽기만 · VF8 ⓒ 는 WP-4). 장부 칸(§14)은 SPEC §6-1 표와 칸마다 같다. 설정 아홉은 SPEC §4-2 와 이름 · 기본값이 같다.

### 3. 표면 전수(다시 grep)

- **허브 `app/` 의 `abbr` 7 파일**: `resolve.py` · `memory.py` · `repository.py` · `service.py` · `router/gold.py` · `mcp_server.py` · `swagger_docs/gold.py` — **맞음**. `covered_by` · `how` · `full` 은 `resolve.py` · `headers.py` · `mcp_server.py` · `swagger_docs/gold.py` — 맞음. 빠진 상수 = `headers.py` `MATCHED_HOW` · `NM_ENTRY_COLUMNS`(R-1 ⓒ).
- **허브 시험**: `resolve(` 13 파일 가운데 gold 7 — 맞음. `"resolve"` · `/resolve` 꼴까지 다시 grep 하니 표 밖 깨짐 · 빈 검사 자리 3(`test_gold_contract` 166 · 188 · 191)이 더 나왔다(R-1). `test_gold_mcp:55-56` · `test_medallion_repo:106,318` · `test_gold_rest:40` · `test_gold_real:207,368,373` 은 이름 · 목록 꼴이라 그대로 맞다.
- **「지움 20 · 고침 13 · 표 밖 ★6」 다시 셈**: `test_gold_v07_resolve.py` 의 `test_` 함수 **16**(이 검수가 셈) + H-4 1 + H-8 3 = **20 맞음** · 고침 H-1 · 2 · 5 · 6 · 7 · 9 · 10 · 11 · 12 · 13 · 14 · 15 · 16 = **13 맞음** · ★ H-2 · 7 · 12 · 14 · 15 · 16 = **6 맞음**. R-1 을 넣으면 고침이 하나 늘고(H-17) ★ 가 7 이 된다.
- **앱 켠 가지 부름 6 자리**: `turn.py:321`(`_walk` → `walk()`) · `:333-335` · `:350`(`tk.judge`) · `state.py:272`(`hub.resolve(question)`) · `:278` · `:280`(`ask_nouls`) — 줄 번호 · 뜻 **맞음**(이 검수가 열어 봄). `turn.py:306`(`cst.retract` 부름)은 X-9 안 · `:338` 은 X-12 안이다.
- **27 행**: X-1 ~ X-27 셈 맞음(지움 14 · 고침 · 바꿈 · 그대로 11 · 남김 2). 빠진 자리 = `turn.py:479`(R-4). §4 grep 은 이 검수에서 `turn.py` 43 · `state.py` 15 · `prompt.py` 22 · `turn_kind.py` 2 · `e6.py` 2 · `carry.py` 1(+ `static/htmx.min.js` 1 — 상관없음)이다.

### 4. 시험 범위

- WP 마다 「돌릴 파일」 이 적혀 있고, 전체 pytest 금지가 두 WORK 의 §2 · 완료 조건에 있다 — 지켜지는 목록이다. WORK-016 은 WP-1 ~ WP-3 을 한 묶음으로 돌린다(기대를 바꾸는 WP-3 뒤에 — 까닭이 적혀 있다).
- 바뀌는 기존 시험의 까닭은 모두 계약 줄(SPEC-001 R2 · O-32 · T27 · T29 / SPEC-008 CP1 · OU9 · QS1 · QS4 · DT1 · BQ4 · X-26 · rev 4)에서 온다. **「시험이 낸 수를 기대값으로 옮기는」 지시는 없다**: WORK-016 H-15 · WP-1 완료 조건 5 는 「직접 센 개념 집합 = 도구 후보 집합」(두 셈을 견줌)이다. E4 의 820 · E8 의 분모는 「그 판의 수와 까닭을 보고」 · 「`score.py` 가 낸 수」 다. WORK-017 §15-4 의 「예상」 수도 「첫 실행에서 확정 · 다르면 보고」 다.
- 빠진 것 = R-1(허브) · R-2(앱 끈 대화 시험 넷).

### 5. 완료 조건

| 조건 | 자리 | 판정 |
|---|---|---|
| D-14 앱 전체 8 검사 ≥ 90 · 입구 3 검사 ≥ 95 | WORK-017 §0 · §16-1 E8-3 · E8-4 · §16-3 5 | 맞음(`pass8_pct` · `pass3_pct` · 분모 = score.py · 애매 밖) |
| U8-2 정보 종류 ≥ 90 | E8-6a | 맞음(`kinds_score` 엄한 쪽) |
| U8-4 ⓐ ≥ 90 · ⓑ ⓒ = 100 | E8-6b · §3 5 | 맞음 · 0.3 기준선을 WP-0 에서 **고치기 전에**(B-11 — `now-rows.jsonl` 에 C74 ~ C78 이 없음은 이 검수도 확인 못 함 · 조사 판 255 턴이라 맞는 말) |
| `ref.to = answer` 5 대화 답 LLM 실제 호출 | WP-11 `run_now --real-answer C56,C57,C58,C65,C69` · E8-3 명령 | 맞음(5 대화 · 25 턴 — 이 검수가 셈) |
| `score.py` 를 덮어쓰지 않는 길(B-6) | `INPUT_SPACE_OUT` · `runs/v04-score/` | 방향 맞음 · 뜨는 차례 · env 의 뜻이 빠짐(**R-3**) |
| 포트 18224 · 18107 만 · 18105 · 18222 · 18432 금지 | WORK-016 §2 · WORK-017 §2 · §16-3 6 | 맞음(18105 는 GET 읽기만 — WP-0 목록 · 0.3 기준선 · WORK-016 E1 · E4 · E6) · 띄우기 전 `lsof` · 자기 PID 만 |
| 커밋 금지 | WORK-016 §2 · WORK-017 §2 · §16-3 7 | 맞음(앱 · 허브 · 프로필) |
| 문턱 미달 때 | WORK-017 §16-1 끝 불릿 | 맞음 — 프롬프트 · 규칙을 고치지 않고 보고 |

### 6. 화면 문구 · 비밀값

- 화면 문구: 지어 넣은 곳 없음. 새 화면 자리는 빈 `data-slot` 하나(`conv-off-closed` — U8-3 빈칸 · 사용자 확인 대상 O-1)뿐이다. 실패 턴은 0.3 「입구 없음」 말 그대로다. `TABLE_TITLES` 는 시안 글자를 베낀다(LLM 에게 가는 글 · 사람에게 안 보임). 남은 것 = 사람에게 안 보이는 프롬프트 표지 글자를 구현 워커에게 넘긴 R-5 하나.
- 비밀값: WORK-016 은 DB 접속 값을 `set -a` 로 프로세스 env 에만 넣고 `cat` · `echo` 를 금한다(§2). 마감 때 diff 에서 비밀값을 grep 한다(§7). WORK-017 은 환경 파일을 열지 · 고치지 않고 env 이름만 쓴다(§2). 장부 `output_raw` 는 코드 · JSON 뿐이고 턴 메시지 전문은 싣지 않는다(SPEC §6-1). 노출 길 없음.

## 구현 발주 전에 꼭 고칠 것

1. **R-1** — WORK-016 H 표에 `test_gold_contract` 의 `V07_CALLS[1]`(`abbr`) · `SYN_CALLS[0]` · `V07_CALLS[0]`(문장) · `V07_LINES` NM 줄을 넣는다. WP-1 에 `headers.py` `MATCHED_HOW` · `NM_ENTRY_COLUMNS` 지움을 넣는다. `rg` 완료 조건 꼴을 넓힌다.
2. **R-2** — WORK-017 §15-4 에 끈 대화 시험 넷(`test_v03_prompt` s6_t8 뒤 반 · s6_t9 · `test_v03_frame` s6_t29 · `test_state_blanks:119`)의 처분 · 까닭(CP1 · CP7)을 넣는다.
3. **R-3** — WORK-017 WP-11 에 「고치기 전 산출물 복사 → `INPUT_SPACE_OUT` 은 쓰는 자리만 → 고친 score.py 로 옛 장부 견줌」 차례를 박는다.

나머지(R-4 ~ R-7)는 구현 보고 · 되적기에서 받아도 된다. R-7 은 18105 를 다시 띄우기 전에 코디가 볼 것이다.
