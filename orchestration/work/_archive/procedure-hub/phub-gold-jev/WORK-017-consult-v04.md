---
type: work
id: WORK-017
title: "앱 상담 채팅 0.4 구현 계획 — 켠 상태 턴에서 Jev · resolve 맞춤 꼴을 걷어 내고 소넷 「이해」 호출 하나로 · 목록 적재 · 검증 · 객체 · 조회 · 화면 · 장부 · 프롬프트 · 끈 상태 막기 · 채점기 맞춤 · E8 표 실행"
status: draft
product: procedure-hub
feature: phub-gold-jev
version: 0.1.0
created_at: 2026-11-18
updated_at: 2026-11-18
tags:
  - product/procedure-hub
  - feature/phub-gold-jev
  - doc/work
  - status/draft
links:
  specs:
    - "orchestration/work/phub-gold-jev/SPEC-008-consult-entry.md (0.2.0 — 검수 review-spec-008.md 의 F-1 ~ F-16 은 0.2.0 변경 기록) ← 계약"
    - "orchestration/work/phub-gold-jev/SPEC-001-hub-gold-mcp.md (0.8.1 — §4-1 목록 꼴 · 쓰는 곳별 영향 표) · WORK-016-hub-resolve-v081.md (허브 0.8.1 — 18107)"
    - "orchestration/work/phub-gold-jev/SPEC-004 · 005 · 006 (고치지 않는다 — SPEC-008 §5 「달리 받는 곳」)"
  decisions:
    - "orchestration/work/phub-gold-jev/_RESUME.md §2 (2026-11-18 맨 위 행 전부 — 「SPEC-008 0.2.0 남은 정할 것 코디 답」(U8-3 빈칸 · U8-4 ⓐ 90% · ⓑⓒ 100% · C8-8 · C8-9) · 「SPEC-008 검수 WARN 16 코디 답」 · 「워커 모델 opus」 · 「D-1~D-15 확정」 · 「소넷으로만 — Jev 를 뺀다」 · 「허브 resolve = 최소 목록 꼴」 · 「resolve 를 후보 관문에서 뺀다」) · 11-17 「시험은 구현한 것만 돌림 · 전체 테스트 안 돌림」"
    - "orchestration/work/phub-gold-jev/work-016-017-brief.md (이 문서의 발주서 — 코디 답 U8-3 · U8-4 · C8-8 · C8-9)"
  related:
    - "orchestration/work/phub-gold-jev/WORK-014-consult-v03.md (앞 앱 WORK — 꼴 · 시험 규칙 · B 표)"
    - "orchestration/work/phub-gold-jev/research-input-space/scripts/README.md (표 · 채점 · 돌리는 법)"
---

# WORK-017 — 앱 상담 채팅 0.4 구현 계획

> 경로 접두어: `W` = 이 폴더 · `APP` = clinic_chat 워크트리 `phub-gold-jev`(HEAD `be1c622` = 상담 0.3 · **이 위에 이어서 짓는다**) · `HUB` = PROCEDURE-HUB 워크트리 `phub-gold-jev`(읽기만 · 0.8.1 은 WORK-016) · `RS` = `$W/research-input-space` · `SC` = `$RS/scripts`. 앱 경로는 전부 `APP` 기준이다.
> **계약은 SPEC-008 0.2.0 이다.** 이 문서는 「어느 파일을 · 어떤 순서로 · 무엇으로 확인하나」 만 정한다. SPEC 과 달리 받는 곳은 §17 B 표뿐이다. 그 밖에 어긋나는 것을 만나면 코드를 맞춰 고치지 말고 보고한다.
> **화면 문구 · 답 문구를 짓지 않는다.** 새 빈 자리는 CP7 하나(옛 끈 대화를 막는 자리 — 문구 = U8-3 **빈칸** · 사용자 확인 대상). 프롬프트 `pick` 절은 SPEC §7 초안 **그대로** 옮긴다(사용자 확인 대상 — 고쳐 쓰지 않는다).
> **시험은 구현한 것만 돈다**(사용자 11-17): WP 마다 그 WP 의 시험 파일만 · 전체 pytest 금지 · 돌린 파일 · 통과 수 · 고친 · 지운 기존 시험 이름을 보고.
> 줄 번호는 `APP` `be1c622` 에서 이 워커가 읽은 것이다(읽기만 · 코드 · 서버 · LLM 호출 0).

## 0. 요약

- 0.4 는 **켠 상태 턴의 입구를 통째로 바꾼다**(`consult_rev` = **4**): 걷기 `walk()`(Jev 맨 앞 판단 · resolve 맞춤 꼴 · 입구 고르기 · 값 고르기 · 깊이 Noul · `answer_ready`) · 가르기 · 거둠 요청을 부르지 않고, 턴마다 **소넷 이해 호출 하나** → 검증 → 객체 → 조회(객체 기준 + 걷기의 결정론 함수로 답 재료) → 화면 → 빈 칸 → 답(0.3 그대로) → 장부.
- **끈 상태 = 0.4 서버에서 새로 열지 않는다**(CP1 · CP7): `chat_state` 기본 `on` · `CHAT_STATE=off` 여도 새 대화는 켠 상태 · 옛 끈 대화는 읽기만(새 턴 막음 · 막는 화면 자리 = 빈 `data-slot` 하나). 끈 가지 코드(`turn.py:121-125`)는 **지우지 않는다**.
- `walk/` 는 **얇은 공개 감쌈 추가만**(동작 변경 0 · §3-4 · F-10) · `columns/` 는 **기본 diff 0**(밑줄 함수 `_labels` · `_end_check` 는 그대로 import — 코디 C8-9: 필요하면 얇은 공개 감쌈 허용) · `prompts/jev/` · `llm/` · `web/` diff 0.
- WP 열 — **WP-0** E8-0 실측 · 0.3 기준선 → **WP-1** 목록 적재 → **WP-2** 이해 호출 → **WP-3** 검증 → **WP-4** 객체 · 부위 거르개 → **WP-5** 조회(객체 기준 · QS1 ~ QS6) → **WP-6** 답 재료(정보 종류 · 깊이 · 값 · 걷기 결정론 함수) → **WP-7** 턴 흐름 · 실패 길 · 화면 · 빈 칸 → **WP-8** 장부 · 패널 · SSE → **WP-9** 프롬프트 `pick` · 적재기 → **WP-10** 끈 상태 막기 · `consult_rev` 4 · 설정 → **WP-11** E8-pre 채점기 맞춤 → **WP-12** 실물 E8-1 ~ E8-6 표 실행 · 18224 화면 확인 · README → **코디** 18105 재시작(허브 0.8.1 과 같이) · 18222 · E8-5 · E8-7.
- **완료 조건** = SPEC §8 E8(D-14 · U8-2 · U8-4): 앱 전체 8 검사 **90%↑** · 입구 3 검사 **95%↑** · 정보 종류 **90%↑** · E8-6b ⓐ **90%↑** · ⓑ ⓒ **100%** — 분모는 실행 때 `score.py` 가 낸 수. 표 실행은 구현 워커가 허브 **18107**(0.8.1)로 돌려 수를 보고한다. 사람 표본 검수(E8-5)는 코디 · 사용자 몫 — 워커는 표만 낸다.

## 1. 지금 코드(`APP` · `be1c622`)

| 파일(줄 수) | 지금(0.3) | 0.4 에서 |
|---|---|---|
| `clinic_chat/consult/turn.py`(679) | `run_turn`(`:82`) — `carry_mod.candidates`(`:121`) → `Consult.begin`(`:122`) → 끈: `walk()`(`:125`) / 켬: `cs.walk(hold, release)`(`:127`) → `renumber`(`:143`) → `after_talk` · `after_walk`(`:146` · `:149`) → `screen` → LLM → 장부(`:211-240`). `class Consult`(`:243`) — `retract`(`:296`) · `_mode`(`:309`) · `_walk`(`:319`) · `walk`(`:326-385` — 가르기 · 두 번째 걷기 · TW4 · TW5) · `talk_trace` · `talk_build`(`:387-396`) · `after_talk`(`:398`) · `after_walk`(`:406`) · `_update`(`:415-453`) · `ledger`(`:642-679`) | WP-7 · WP-8 — 켠 가지를 이해 호출로 · 끈 가지는 그대로 |
| `clinic_chat/consult/state.py`(302) | `SLOT_OF`(`:24-25`) · `KEEP`(`:28`) · `WISH_KINDS`(`:29`) · `KIND_CODES_14`(`:30`) · `filter_sites`(`:65-68`) · `_decision_state`(`:71-81`) · `observe`(`:84-111` — 걷기 trace) · `update(…, retract_yes)`(`:134`) · `_focus`(`:200-216` — 글자 자리 `start`) · `retract`(`:261-295` — `hub.resolve(question)` `:272` · `ask_nouls` `:278` · `:280`) · `retract_yes`(`:297`) | WP-4 |
| `clinic_chat/consult/plan.py`(276) | `ALLOWED`(`:27`) · `Reader`(`:46`) · `qy1_calls(obj)`(`:87-95` — 객체 축 부위로 거름) · `run`(`:193`) · QY7(`:220-223`) · `derive`(`:228-266`) | WP-5 |
| `clinic_chat/consult/sites.py`(103) | `place` · `site_pairs`(`:88-92` — 직접 + 하위) · `viewable_subs`(`:95`) | WP-7(DT1) |
| `clinic_chat/consult/blanks.py`(125) | `pick(…, prev_ask, …)`(`:93` — NQ5 `:99-100`) | WP-7(BQ4) |
| `clinic_chat/consult/turn_kind.py`(81) | `EXTRA`(`:16`) · `prev_turn`(`:20`) · `talk_streak`(`:25`) · `prev_state` · `prev_block` · `judge`(`:60`) · `follow_target`(`:69`) | WP-3(VF6 이 `follow_target` · `talk_streak` 을 쓴다) |
| `clinic_chat/consult/carry.py`(72) | `candidates`(`:15` — 끈 가지도 쓴다) · `with_options`(`:34`) · `alive_in_object`(`:60`) | 켠 가지가 안 부른다 |
| `clinic_chat/consult/ledger.py`(214) | `CONSULT_REV = 3`(`:32`) · `start`(`:139` — `consult_rev` 를 첫 턴에 박음 `:144`) · `state_at_start`(`:195-201`) · `blocked`(`:204-214` — `rev_changed` `:208-209`) | WP-10 |
| `clinic_chat/consult/prompt.py`(221) | `KEYS`(`:27`) · `state_ready`(`:67-72`) · `parse`(`:81`) | WP-9 |
| `clinic_chat/consult/server.py`(214) | `POST …/turns` → `blocked(c, …)`(`:146`) · 드로어 `outdated`(`:96-102`) | WP-10 |
| `clinic_chat/consult/material.py`(329) | `renumber(w, …)`(`:162`) · `judgement_v3`(`:248`) · `message_v3`(`:266`) | **안 고친다**(지은 `Walk` 를 넘긴다 · §3-4) — `judgement_v3` 의 `turn_kind` 값만 검증 뒤 `kind` 로 |
| `clinic_chat/consult/e6.py`(130) | 0.3 실측 요약 — `turn_kind.nouls`(`:51` `.get` · `:88` `t["turn_kind"]["nouls"]`) | **안 고친다**(0.3 장부용) — B-8 |
| `clinic_chat/config.py` | `chat_state = "off"`(`:82`) · `chat_*` | WP-10 · 설정 아홉(SPEC §4-2) |
| `clinic_chat/llm/chat_cli.py` | `chat_args`(`:49-57` — 격리 인자) | **안 고친다**(답 실행기 0.3 그대로) — 격리 인자 값은 읽어 같은 값을 쓴다 |
| `clinic_chat/llm/cli.py` · `cli_process.py` | 추론 끔 꼴 = `--settings {"alwaysThinkingEnabled": false}` + env `MAX_THINKING_TOKENS=0`(`cli.py:11-12` · `:96`) · `run_cli(cmd, *, cwd, env, timeout_s, on_line, stdin_text)`(`cli_process.py:54`) · `child_env(extra)`(`:29`) | **안 고친다** — 이해 호출이 `run_cli` · `child_env` 를 부른다(WP-2) · 끄는 꼴은 E8-0 의 첫 후보 |
| `clinic_chat/clients/hub_rest.py` | `read_all(tool, request)`(`:138` — 쪽 끝까지) · `resolve(text, *, range, tables, …)`(`:181`) · `concern_candidates`(`:195`) | **안 고친다** — 목록 적재가 `read_all("resolve", {"tables": …})` 를 부른다 |
| `clinic_chat/walk/front.py` | `FrontResult`(`:50`) · `_coverage`(`:168`) · `nonzero_rows`(`:179`) · `_kind_rows`(`:189`) · `_ranges_for`(`:193`) · `front()`(`:210`) | WP-6 — 공개 감쌈만 더함 |
| `clinic_chat/columns/col_b.py` | `Walk`(`:47`) · `_labels`(`:74`) · `same_day_marks`(`:121`) · `walk()`(`:161-227`) · `_end_check`(`:230`) · `judgement`(`:254`) | **diff 0**(C8-9 감쌈은 B-3) |

## 2. 공통

| 항목 | 이번 판 |
|---|---|
| 시작 조건 | 코디 발주. 앱 작업 트리(`be1c622`) 위에 이어 짓는다. 허브 0.8.1(WORK-016)과 **병행**한다 — WP-1 ~ WP-10 은 가짜 허브 · 가짜 CLI 만 쓴다. **0.4 켠 상태는 목록 꼴만 쓰므로 0.7.2 허브(18105)로도 돈다**(SPEC-001 0.8.1 영향 표) — WP-0 · WP-12 의 실물 판은 §14 |
| allowed_paths(앱) | **새로**: `clinic_chat/consult/{entry_list,understand,verify,site_filter,site_index,kinds_pick,material_read}.py`(이름 제안 — B-1) · `tests/test_v04_*.py` · `tests/v04_fixture.py` · `tests/fake_cli/` 의 이해 호출 응답 길(더하기만 — WP-2). **고침**: `consult/{turn,state,plan,sites,blanks,ledger,prompt,server,render,drawer,steps,listing}.py`(각 WP 의 자리만) · `consult/templates/partials/{main,turn}.html` 또는 막는 자리가 서는 조각 하나(`data-slot` 하나 — WP-10) · `clinic_chat/config.py`(칸 더하기 · `chat_state` 기본값) · `clinic_chat/walk/front.py`(**공개 감쌈 추가만** — WP-6) · `prompts/consult.json`(`pick` 절 더하기만 — WP-9) · `.env.example`(이름만) · `README.md`(상담 절) · `tests/{fake_hub,consult_fixture,state_fixture}.py`(더하기만) · **§15 표에 이름을 박은 기존 시험 파일의 그 시험만** |
| allowed_paths(프로필 — 채점) | `$SC/{score,slim,run_now}.py`(WP-11 — 옛 칸 길을 남기고 더하기) · `$SC/README.md`(돌리는 법 줄만 — WP-12) · `$RS/runs/v04*`(실행 기록) · `$RS/runs/v03-c74*`(WP-0 기준선). **`$RS` 의 `now-turns.jsonl` · `summary.json` · `fail-by-tag.csv` · `pick-*` · `fan-*` 를 덮어쓰지 않는다**(조사 산출물 — B-6) · `conversations.jsonl` · `convs*.py` · `build.py` 고치지 않음(표 · 키는 이 판에서 안 바꾼다 — SPEC §8-1) |
| **고치지 않는 것** | `clinic_chat/columns/**`(B-3 외) · `clinic_chat/walk/**` 의 기존 줄(감쌈 추가만) · `prompts/jev/**` · `prompts/*.md` · `clinic_chat/llm/**` · `clinic_chat/clients/**` · `clinic_chat/web/**` · `consult/templates/_face.svg` · `consult/face_coords.py` · `consult/material.py`(B-2 의 한 줄 외) · `consult/e6.py` · `consult.json` 의 `system[]` · `system_v3` · `jev_front` · `jev_state` · `steps` 글자 · **`tests/test_walk_*.py` · `tests/test_columns.py` · 시험 앱 묶음 시험**(S8-T18) · 허브 레포 |
| 포트 | **워커 18224**(앱 · 실물 화면 확인 — 띄우기 전 `lsof -nP -iTCP:18224 -sTCP:LISTEN` · 차 있으면 멈추고 보고 · 끝나면 자기 PID 만 내림) · **18107**(허브 0.8.1 — WORK-016 §6 명령으로 띄움 · 같은 규칙) · **18105 · 18222 · 18432 를 건드리지 않는다**(18105 는 WP-0 의 0.3 기준선 · `health` 에 **GET 읽기만**) |
| 외부 호출 | 단위 시험은 전부 가짜(CLI · 허브 · Jev). 실물 소넷 · 허브는 **WP-0 · WP-12 만**. 환경 파일을 열거나 고치지 않는다(없으면 「못 돌림」 → 코디) · 키는 env 이름만 |
| 문구 | 새 코드 · 템플릿에 사람에게 보일 문장 0 — `data-slot` 자리만(새 자리 하나 — WP-10). 예외: `prompts/consult.json` `pick`(SPEC §7 초안 그대로) · 시험 자료 |
| **시험** | WP 마다 **그 WP 의 새 파일 `tests/test_v04_<WP>.py` + §15 에 박은 기존 파일만** 돈다. `uv run pytest -q` 를 인자 없이 부르지 않는다. 고치기 전 그 WP 의 기존 파일을 **한 번 돌려 기준 통과 수**를 적고, 고친 뒤 수와 함께 보고한다. `uv run ruff check <고친 경로>` 도 고친 파일만 |
| 커밋 | **안 한다** — 앱 · 프로필 모두 워크트리 변경만(커밋 · push · PR 은 코디) |

## 3. 정해진 값(다시 묻지 않는다)

| # | 값 | 출처 |
|---|---|---|
| 1 | D-1 ~ D-16 · F 답(F-1 ⓒ · F-5 · F-6 · F-8 · F-9 · F-10) | SPEC-008 §1-2 |
| 2 | U8-1 (가) 깊이 = 이번 턴 대상인 후보만 · 값 표지 없앰 · 소넷 호출 안 더함 | SPEC-008 §3-2 · §3-3 |
| 3 | U8-2 (a) 정보 종류 90% | SPEC-008 §8-2 |
| 4 | **U8-3 = 빈칸** — 옛 끈 대화를 막는 화면 문구를 짓지 않는다 · 자리(`data-slot`)만 · 사용자 확인 대상 목록(§17-1 O-1) | 코디(발주서) · `_RESUME` §2 11-18 맨 위 행 |
| 5 | **U8-4 = E8-6b 문턱 ⓐ 90% · ⓑ ⓒ 100%** | 같음 |
| 6 | **C8-8 = 막는 자리는 `rev_changed` 꼴 그대로**(끝난 대화로 읽기만 · 줄을 쓰지 않는다 — 0.3 B-5 와 같은 길) | 같음 |
| 7 | **C8-9 = `columns/col_b.py` 의 `_labels` · `_end_check` 는 그대로 import** · 필요하면 `columns/` 에도 얇은 공개 감쌈(동작 변경 0) 허용 | 같음 |
| 8 | C8-1 ~ C8-7 = SPEC 본문 값(색인은 앱이 `gold_hash` 마다 짓는다 · NQ5 는 QY7 `new` 턴만 뺀다 · 앞 답 요약 200 자 · 2 턴 · 리스트 30 · rev 3 켠 대화 = 끝난 대화 · thinking 끄는 법은 E8-0 · 첫 턴 `talk` 받고 `follow` → `new` · 실패 턴 말 = 「입구 없음」) | SPEC-008 §9-2(바꿀 것만 말하면 된다 — 발주서가 바꾼 것 없음) |

## 4. 지울 곳 — 켠 가지에서 Jev · resolve 맞춤 꼴에 닿는 자리 전수(grep)

명령(이 워커 · `APP` `be1c622`):

```bash
rg -n '\bwalk\(|cs\.walk|self\._walk|\.retract\(|cst\.retract|retract_yes|tk\.judge|tk\.EXTRA|carry_mod\.|cst\.observe|\bobserve\(|d\.jev|jev_front|jev_state|jev_noul|entry_pick|abbr_yes_only|ask_nouls|hub\.resolve|b_trace|front\.carried|nouls|trace_entry|walk_ms|jev_ms|chat_carry_turns|chat_retract|chat_turn_kind|uncertain_kept|_decision_state' clinic_chat/consult/
```

→ 걸린 파일 6: `turn.py` 44 줄 · `state.py` 15 · `prompt.py` 22 · `turn_kind.py` 2 · `e6.py` 2 · `carry.py` 1(주석). `prompt.py` 22 줄은 `jev_front` · `jev_state` 절 **적재**(지우지 않는다 — SPEC §7 적재기 계약)이고 `state_ready` 한 자리(`:67-72`)만 바뀐다. `walk/` 안의 Jev(`front.py` · `value_pick.py` · `depth.py` · `jev_requests.py`)는 **고치지 않는다** — 켠 가지가 그 함수를 부르지 않게 될 뿐이다(CP2 · CP3).

**Jev · resolve 맞춤 꼴에 실제로 닿는 부름 자리 = 6**(켠 가지): `turn.py:321`(`_walk` → `walk()` → `front()` → `hub.resolve(text)` · Jev 맨 앞 판단 · 입구 고르기 · 값 고르기 · 깊이) · `turn.py:333-335`(`_mode` ≠ `classify` 일 때의 `walk()`) · `state.py:272`(`d.hub.resolve(question)` — 거둠) · `state.py:278` · `:280`(`ask_nouls` — 거둠 · 가르기) · `turn.py:350`(`tk.judge` — Noul 판정). 그것을 띄우고 읽는 자리까지 합친 표:

| # | 자리 | 무엇 | 처분 | WP |
|---|---|---|---|---|
| X-1 | `turn.py:89` · `:212` | `jms0 = d.jev.ms_total` · `timing.parts.jev_ms` | 켠 턴 = `understand_ms` 로 · 끈 가지는 남김(`jev_ms` 키는 켠 줄에서 없어짐 — §6-1) | WP-8 |
| X-2 | `turn.py:121` | `carry_mod.candidates(…, chat_carry_turns)` | 끈 가지로만 옮긴다(켠 가지는 안 부름) | WP-7 |
| X-3 | `turn.py:125` | 끈 가지 `walk(question, d, carry, instr=jev_front)` | **남김**(CP7 — 0.4 서버에서 부르는 곳이 없어질 뿐) | — |
| X-4 | `turn.py:127` | `cs.walk(hold, release)` | → `cs.understand()` | WP-7 |
| X-5 | `turn.py:129` | `walk_ms` | 켠 턴 = `material_ms`(재료 조회 시간) | WP-8 |
| X-6 | `turn.py:223` | 턴 줄 `carried` = `w.front.carried` | 켠 턴 = `[]`(든 후보가 없다 — AR-9) | WP-8 |
| X-7 | `turn.py:225-229` | `trace` = `b_trace(w, …)` | 켠 턴 = 지은 `Walk` 의 `b_trace` + `trace.depth` 새 꼴(§6-1 — `noul` · `answer_ready` · `jev_requests` 없음) · `talk` 턴은 `talk_trace` 대신 `{understand: …}` 짧은 꼴 | WP-8 |
| X-8 | `turn.py:253` · `:255` | `carry_mod.alive_in_object` · `with_options` | **지움**(켠 `Consult.__init__` 에서) | WP-7 |
| X-9 | `turn.py:296-307` | `Consult.retract`(`cst.retract` · `tk.EXTRA` · `jev_state["retract"]` · `jev_noul_yes_at`) | **지움** — 거둠 = `withdraw[]`(OU8) | WP-7 |
| X-10 | `turn.py:309-317` | `_mode`(`chat_turn_kind` · TK2 · TT6) | **지움** — VF6 · VF7 · VF11(검증) | WP-3 · WP-7 |
| X-11 | `turn.py:319-324` | `_walk`(`walk(…, instr=jev_front, entry_pick, abbr_yes_only)`) | **지움** | WP-7 |
| X-12 | `turn.py:326-385` | `Consult.walk`(gather · `tk.judge` · `talk` 걷기 거둠 · TW4 앞 대상 다시 걷기 · TW5 입구 고르기 다시 걷기) | **지움** → `understand()` | WP-7 |
| X-13 | `turn.py:387-396` | `talk_trace` · `talk_build`(`self.w0`) | **지움** | WP-8 |
| X-14 | `turn.py:398-404` | `after_talk` 의 `cst.observe(self.w0, …)` | → 검증 뒤 값의 `withdraw` 만(OU10) | WP-4 · WP-7 |
| X-15 | `turn.py:406-413` | `after_walk` 의 `cst.observe(w, prev_ask)` | → `after_understand(acc)` | WP-4 · WP-7 |
| X-16 | `turn.py:418` | `cst.update(…, cst.retract_yes(self.rt))` | → `withdraw` 집합(검증 뒤) | WP-4 |
| X-17 | `turn.py:447` | `kinds_read = w.front.kinds` | 그대로(지은 `FrontResult.kinds`) | WP-6 |
| X-18 | `turn.py:645-648` | 장부 `carried` · `options_carried`(`noul` · `decision`) | **지움**(켠 줄) | WP-8 |
| X-19 | `turn.py:665-673` | 장부 `retract` · `retract_ms` · `retract_resolve_ms` · `retract_requests` · `jev_requests{front, entry_pick, retract}` · `hub_queries` 의 거둠 resolve 몫 · `retract_error` | **지움** → `consult.understand` · `site_filter`(§6-1) | WP-8 |
| X-20 | `state.py:22` | `from walk.jev_requests import ask_nouls, base_state` | **지움** | WP-4 |
| X-21 | `state.py:71-81` | `_decision_state`(`uncertain_kept` → `guess`) | **지움**(급 = `sure` — OU2) | WP-4 |
| X-22 | `state.py:84-111` | `observe(w, prev_ask)`(걷기 trace · `resolve_candidates`) | **지움** → `observe_accepted`(WP-4) | WP-4 |
| X-23 | `state.py:261-295` | `retract`(`hub.resolve(question)` · `ask_nouls` ×2) | **지움** | WP-4 |
| X-24 | `state.py:297-299` | `retract_yes` | **지움** | WP-4 |
| X-25 | `turn_kind.py:16` · `:60-66` | `EXTRA` · `judge` | **지움**(켠 가지만 썼다 — `follow_target` · `talk_streak` · `prev_turn` 은 남김) | WP-3 |
| X-26 | `prompt.py:67-72` | `state_ready` 가 `jev_state.retract` · `jev_front.target_option` · `turn_kind` 셋을 요구 | **고침** — SPEC §7 적재기 계약(`pick` 으로) | WP-9 |
| X-27 | `e6.py:51` · `:88` | 0.3 실측 요약의 `turn_kind.nouls` | **안 고침**(B-8) | — |

- **셈**: 부름 자리 6(위 굵은 글) · 그 자리를 띄우고 읽는 자리 포함 **27 행**(지움 14 — X-8 ~ X-13 · X-18 ~ X-25 / 고침 · 바꿈 · 그대로 11 — X-1 · X-2 · X-4 ~ X-7 · X-14 ~ X-17 · X-26 / 남김 2 — X-3 · X-27). 표 밖으로 WP-4 가 `state.filter_sites`(`:65-68`)를 더 지운다(부르는 곳이 `plan.qy1_calls` 하나 — QS1 로 없어진다). `carry.py`(`candidates` 는 끈 가지가 쓴다 · `with_options` · `alive_in_object` 는 켠 가지만 썼다)는 **함수를 지우지 않는다**(X-8 은 부르는 자리만 지움 — 그 함수 시험 `test_consult_carry.py` 그대로).
- 「지움」 = 0.4 코드에서 그 함수 · 줄을 없앤다(C8-4 「0.3 길을 코드에 남기지 않는다」 — `consult/` 는 고칠 수 있는 자리). `walk/` · `columns/` 의 함수는 지우지 않는다(CP3).
- WP-7 끝 확인: 위 명령을 다시 돌려 남는 줄이 **끈 가지(X-2 의 옮긴 줄 · X-3) · `prompt.py` 의 `jev_front` · `jev_state` 적재 · `e6.py` · `carry.py` 주석**뿐인지 본다(§16 완료 조건 3). 켠 턴 시험(S8-T18)이 Jev 가짜 · `hub.resolve(text=…)` 0 번을 기계로 본다.

## 5. 한 턴 흐름 — `turn.py`(켠 상태 rev 4)

```text
run_turn(켠)
  Consult.begin
  ① el = await entry_list.load(d.hub, gold_hash 캐시)          ─ 실패 → FL(error.kind=list)
  ② raw = await understand.call(s, system_text(pick, el), turn_message(conv, obj, question))
                                                                ─ timeout · cli · json → FL
  ③ acc = verify.verify(raw, el, obj, prev_row, first_turn, talk_streak)
  ④ obs = cst.observe_accepted(acc, prev_ask) → cst.update(obj, obs, wishes, n, withdraw)
     sf  = site_filter.decide(acc, prev_row, prev_ask, obj)      ─ VF8 · OU7 · QS3
  ⑤ plan_mod.run(obj, reader, site_filter=sf, …)                ─ QS1 ~ QS6 (+ site_index)
     w = await material_read.build_walk(d, acc, sf, …)          ─ QM1 ~ QM5 · §3-1 · §3-2 · §3-3
  ⑥ screen → list · sites(점 = 직접만)
  ⑦ blanks.count · pick(…, qy7_new) · close
  ⑧ message_v3 · LLM(0.3 그대로)
  ⑨ ledger(consult.understand · site_filter · turn_kind{kind, from} · …)
```

단계 표시(UC10): ② 동안 `understand` · ⑤ `search` · ⑥ `list` · ⑧ `answer`. `talk` 턴 = `understand` → `answer`(TT5). 0.3 의 B-11(가르기까지 걷기 신호 붙듦 — `hold` · `release`)은 걷기가 없으므로 **지운다**.

## 6. WP-0 — E8-0 실측 · 0.3 기준선 · 줄 번호

| 걸음 | 무엇 | 끝 조건 |
|---|---|---|
| 0-1 | 줄 번호 다시 확인 — §1 · §4 표의 자리가 `be1c622` 와 같은지 | 다른 자리는 보고에 표로 |
| 0-2 | **thinking 끄는 법**(UC3 · C8-5): 후보 ⓐ `llm/cli.py:11-12` 의 꼴 그대로 — `--settings '{"alwaysThinkingEnabled": false}'` + env `MAX_THINKING_TOKENS=0` ⓑ ⓐ 에서 `--settings` 만 ⓒ env 만. 이해 호출 인자(UC2 — §8)로 **실물 소넷 20 회**(시험 입력 = 표 `conversations.jsonl` 의 첫 턴 20 개 · 시스템 글 = SPEC §7 `rules[]` + 목록 글 — 목록은 18105 목록 꼴로 · 18105 는 GET 읽기만) | 20 회 `usage` 의 thinking 토큰(CLI 출력에서 읽는 칸 — `stream-json` 이면 `system/thinking_tokens` 이벤트 · `json` 이면 `usage` 안 · 어느 칸인지 보고) **전부 0** 인 후보 하나 → `CHAT_PICK_THINKING=off` 의 뜻으로 적는다. 셋 다 0 이 안 되면 **멈추고 코디에게 올린다**(D-4 「CLI 그대로」 — SDK 로 넘어가지 않는다) |
| 0-3 | 지연 | 위 20 회의 `ms`(벽시계) · `api_ms`(CLI 가 내면) · 캐시 읽음 토큰 — 중앙 · p90 · 첫 호출(캐시 식음) 따로 |
| 0-4 | **0.3 기준선**(E8-6b 의 0.3 쪽) | 0.3 코드(지금 HEAD — **고치기 전에**)로 `run_now.py v03-c74 C74,C75,C76,C77,C78`(허브 = 18105 · Jev 실물 · 답 = 빈 답 가짜) → `$RS/runs/v03-c74/turns.jsonl`. 까닭: `runs/now-rows.jsonl`(255 턴 — 조사 판)에는 fix1 이 보탠 C74 ~ C78 이 없다(이 워커 확인). 장부에서 재료 줄 집합(`material.new_lines[].gid` · `seen_lines`)을 WP-12 에서 견준다 |
| 0-5 | 포트 | `lsof` — 18224 · 18107 비었나 · 18105 · 18222 가 떠 있나(띄우거나 내리지 않는다) |

- 0-2 · 0-4 의 실물 호출 수 · 시간을 보고에 적는다. 0-4 가 Jev 를 부르는 것은 0.3 코드의 동작 그대로다(이 WORK 가 Jev 를 부르는 유일한 자리).
- **시험**: `tests/test_v04_start.py`(새 — 실측 스크립트가 있으면 그 입력 꼴 · 요약 함수만 · 외부 호출 0). 실측 스크립트를 앱에 둔다면 `consult/e8.py`(0.3 `e6.py` 꼴 · `probe --e8-0`)로 — 이름 제안(B-1).

## 7. WP-1 — ① 목록 적재(LD1 ~ LD8)

**SPEC**: §2-1 · §4-2 `CHAT_PICK_ALIASES` · `CHAT_PICK_LIST_CACHE` · §6-1 `understand.list_sha` · `aliases`.

| 만들 것 | 서명(제안) | 내용 |
|---|---|---|
| `consult/entry_list.py` | `TABLES = ("concern", "site", "modality", "procedure", "product")` · `TABLE_TITLES = {…}`(표 머리의 한국어 이름 — **시안 `pick-prompt.md` 의 「# 목록」 머리 글자 그대로** 베낀다 · 새 글자 0) | — |
| | `@dataclass(frozen=True) class EntryList: gold_hash: str; text: str; sha: str; aliases: bool; items: dict[tuple[str, str], Item]; names: dict[str, tuple[str, str]]` · `Item(table, code, name, aliases: tuple[str, ...])` | `items` = 개념 하나 = (`entity_table`, `entity_code`) 하나(LD2) · `name` = `entity_name` · 별칭 = 그 개념의 다른 행 `text` 가운데 이름과 글자가 다른 것(행 순서 · 같은 글자 한 번) |
| | `async def load(hub, *, aliases: bool, cache: bool = True) -> EntryList` | `hub.read_all("resolve", {"tables": list(TABLES)})`(`clients/hub_rest.py:138` — `next_cursor: null` 까지 · LD1) → 줄 꼴 LD3(`## <표 이름> (table = <t>)` · `<코드> <이름> (= <별칭>, …)` · 표 순서 = `TABLES` · 표 안 = **허브가 낸 순서**(다시 정렬 0)) · `aliases=False` 면 괄호만 뺀다(LD4) · `sha = sha256(text)`(LD6) |
| | 캐시 `_CACHE: dict[tuple[str, bool], EntryList]` | 키 = (허브 응답 머리의 `gold_hash`, `aliases`)(LD5) · 프로세스 메모리 · `cache=False`(`CHAT_PICK_LIST_CACHE=off`)면 턴마다 다시. **캐시 키를 알려면 응답 머리가 필요하다** — 턴마다 `health` 를 부르지 않는다: 캐시가 있으면 `Conv.gold_hash` 와 같을 때 그대로 쓰고, 다르거나 없으면 다시 받는다 |
| | 실패 | 허브 오류 · 쪽 넘김 미완 → `EntryListError`(턴은 FL `error.kind` = `list` — LD7 · 반쪽 목록 0) |

- 목록 글은 같은 `gold_hash` 에서 **글자까지 같아야** 한다(결정론 — 프롬프트 캐시).
- 다섯 표 밖(사건 · 조건 · 효과 · 재료 …)은 목록에 없다(LD8).

**시험**(`tests/test_v04_list.py` — S8-T1): 가짜 `g_entry`(가짜 허브 `fake_hub.py` 에 목록 꼴 응답을 더한다 — 쪽 둘 이상) → 표 머리 · 줄 꼴 · 별칭 괄호 · 같은 글자 별칭 한 번 · `aliases=False` 괄호 없음 · 같은 입력 두 번 = 같은 `sha` · `gold_hash` 가 바뀌면 다시 받음 · 쪽 넘김이 안 끝나면 `EntryListError` · 다섯 표 밖 행 0. **돌릴 파일**: `tests/test_v04_list.py` 만.

## 8. WP-2 — ② 이해 호출(UC1 ~ UC10)

**SPEC**: §2-2 · §4-2 · §6-1 `consult.understand` · §8-3 S8-T2 · S8-T3.

| 만들 것 | 서명(제안) | 내용 |
|---|---|---|
| `consult/understand.py` | `def system_text(pick: dict, el: EntryList) -> str` | `"\n".join(pick["rules"]) + "\n\n" + el.text`(UC5 — 턴 · 대화와 무관 · 같은 글) |
| | `def args(s: Settings) -> list[str]` | `[bin, "-p", "--model", s.chat_pick_model, "--effort", s.chat_pick_effort, "--max-turns", "1", "--output-format", "json", "--no-session-persistence", "--system-prompt", <system_text>, "--setting-sources", "", "--tools", "", "--disallowedTools", DISALLOWED_TOOLS, "--disable-slash-commands", "--strict-mcp-config", "--permission-mode", "bypassPermissions"]` + WP-0 이 정한 thinking 끄는 인자. **격리 인자 값은 `llm/chat_cli.py` 의 상수(`DISALLOWED_TOOLS`)를 import 해 같은 값**(두 벌 금지). `--resume` · `--session-id` · `--fallback-model` **없음**(UC2 · UC4) |
| | `def env(s) -> dict[str, str]` | `llm.cli_process.child_env(extra)` — WP-0 의 env(예: `MAX_THINKING_TOKENS=0`) |
| | `def turn_message(conv: Conv, obj: dict, question: str, pick: dict, s: Settings) -> str` | 세 블록(UC6 — 머리 = `pick.headers.history` · `object` · `utterance`): ⓐ 성공 턴 전부(장부 `conv.turns` 에서 `error` 없는 켠 줄) — 손님 말 · `→ 고른 대상: 이름(table:code), … · <kind>`(그 턴 `consult.understand.accepted` · 없으면 `pick.marks.none`) · 그 턴 `consult.ask.options`(`n) 이름(table:code)`) · **가까운 `CHAT_PICK_CONTEXT_TURNS` 턴**에만 앞 답 요약(장부 `answer` 앞 `CHAT_PICK_ANSWER_CHARS` 자 · LLM 요약 0) · 보여 준 리스트(장부 `list` 를 그린 순서 — 묶음 ① 관심 대상 · ② 계열 → 시술 · ③ 시너지 · 앞 `CHAT_PICK_LIST_MAX` 개 · 안 바뀌었으면 `pick.marks.same_list`)(UC7) · 실패 턴은 손님 말 + `pick.marks.failed`(FL4) ⓑ 객체: 축 항목 · `guess` · `withdrawn`(이름(table:code)) ⓒ 이번 말 그대로. 답 요약 줄 · 리스트 줄의 머리 글자 = `pick.headers` 에 키 둘을 더해 둔다(사람에게 안 보임 — SPEC §7 마지막 불릿 「WORK 에서 정한다」 → B-4) |
| | `async def call(s, system: str, message: str) -> Raw` · `Raw{output_raw, ms, api_ms, usage{input_tokens, cache_read_input_tokens, output_tokens, thinking_tokens}, error{kind, detail} \| None}` | `run_cli(args, cwd=s.chat_cli_cwd_path(), env=env, timeout_s=s.chat_pick_timeout_sec, on_line=…, stdin_text=message)`(UC2 — stdin · 답 실행기의 고정 cwd) · 시간 초과 → 프로세스를 거두고 `error.kind` = `timeout`(UC9) · 종료 코드 · 인증 → `cli` · 출력 JSON 의 `result` 글 = `output_raw` · 재시도 0(FL3) |

- **단계 표시** `understand` 는 이 호출 앞에 낸다(UC10).
- 가짜 CLI: `tests/fake_cli/fake_cli.py` 의 「호출 꼴마다 파일」 규칙에 **`--no-session-persistence` 가 있으면 `understand.json`** 길을 더한다(더하기만 — 지금 길 `judge` · `tools` · `answer` 는 그대로). 응답 · 지연(`FAKE_CLI_SLEEP`) · 종료 코드로 S8-T15 를 짓는다.

**시험**(`tests/test_v04_understand.py` — S8-T2 · S8-T3): 인자(`--no-session-persistence` 있음 · `--resume` · `--session-id` · `--fallback-model` 없음 · 격리 인자 = `chat_args` 의 값 · 시스템 글 = `rules` + 목록) · 턴 메시지(성공 턴 전부 · 가까운 n 턴에만 답 요약 · 글자 수 · 리스트 이름 한도 · `same_list` 표지 · 실패 턴 표지 · 객체 블록) · 시간 초과 · 종료 코드 · stdin 으로 감(argv 에 메시지 없음). **돌릴 파일**: `tests/test_v04_understand.py` 만.

## 9. WP-3 — ③ 검증(VF1 ~ VF12)

| 만들 것 | 서명(제안) | 내용 |
|---|---|---|
| `consult/verify.py` | `@dataclass class Accepted: targets: list[dict]` (`{table, code, name, sure}` · 순서 = 출력 순서) `kind: str; kind_from: str; sites: list[str]; withdraw: list[str]; kinds: list[str]; out: bool; dropped: list[dict]; merged: list[dict]; added_from_sites: list[str]; follow_target: dict \| None` | 장부 `consult.understand.accepted` · `dropped` · `merged` · `added_from_sites` · `consult.turn_kind{kind, from}` · `consult.follow_target` |
| | `def parse(output_raw: str) -> dict` | 첫 `{` ~ 마지막 `}` → JSON 객체 · 아니면 `UnderstandJSONError`(VF1 → FL `json`) |
| | `def verify(parsed: dict, el: EntryList, obj: dict, *, first_turn: bool, talk_streak: int, talk_max: int, prev_row: dict \| None) -> Accepted` | 차례: VF2(목록에 없음 · 다섯 표 밖 · 꼴 틀림 → `dropped{why: not_in_gold \| bad_shape}`) → VF3(같은 것 한 번 · `sure` 갈리면 false · `dup`) → VF4(계열 · 시술 · 제품 이름 `norm` 같음 → 계열 > 시술 > 제품 하나 · `merged` — `norm` = 공백 연속 제거 + 소문자 · 허브 R1 과 같은 식 하나를 `consult/` 에 둔다(B-5)) → VF5(고민 ↔ 부위 같은 이름은 안 접음) → VF6(`kind` 셋 밖 → `new` · `bad_value` / `talk` + 대상 → 대상 버림 `why: talk` / `follow` + `[]` → `turn_kind.follow_target(obj, prev_row)` · `kind_from` = `understand`) → VF7(첫 턴 `follow` → `new` · `first_follow` · 첫 턴 `talk` 그대로) → VF11(잇단 `talk` 가 `talk_max` 면 `new` · `talk_max`) → VF8 ⓐ ⓑ(`sites[]` 는 `site` 코드만 · `sites` 에만 있는 부위 → `targets` 끝에 `sure` true · `added_from_sites`) → VF9(`withdraw` 는 `table:code` · 객체에 살아 있는 것만 · `targets` 와 겹치면 그 대상을 뺌) → VF10(`kinds` = 14 코드만 · 순서 = **`walk/kinds.py:38` `KIND_CODES`** · 중복 한 번 · `sure` · `out` bool 아니면 false) |

- VF12: `Accepted` 가 그 턴의 **유일한 입구** — ④ 이후는 이것만 읽는다(글에서 낱말을 따로 뽑지 않는다).
- `turn_kind.py`: `EXTRA` · `judge` 지움(X-25) · `follow_target` · `talk_streak` · `prev_turn` 은 그대로 쓴다.

**시험**(`tests/test_v04_verify.py` — S8-T4 · S8-T5): S8-T4 · S8-T5 의 기대 전부 + 「검증 뒤 대상은 전부 객체 diff 에 든다」(AR-6 — WP-4 와 함께 한 시험). **돌릴 파일**: `tests/test_v04_verify.py` · `tests/test_v03_turn_kind.py`(§15 의 지움 · 그대로 처분 뒤).

## 10. WP-4 — ④ 객체 갱신 · 부위 거르개(OU1 ~ OU12 · VF8 ⓒ · OU7 · QS3)

| 만들 · 고칠 것 | 어디 · 서명(제안) | 내용 |
|---|---|---|
| 관찰 | `state.py` `def observe_accepted(acc: Accepted, prev_ask: dict \| None) -> list[dict]` | 대상 하나 = 관찰 하나(OU1 — `SLOT_OF` 그대로) · 급 `sure` → `said` / `guess`(OU2) · `how`(OU3 — 앞 `ask.options` 에 있으면 `option` + `from_ask` · `follow` 턴 → `carried` · 그 밖 `text`) · 부위 대상 → `sites[]` 칸 `said` · 이번 턴 고민과 같은 이름이면 `source.pair_concern`(0.2 W-2) · 관찰마다 `order`(= `targets` 안 자리 — OU9 재료) · `source` 새 칸 `sure` · 없어지는 칸 `noul` · `decision` · `matched` · `covered_by`(OU12) |
| 갱신 | `state.update(obj, obs, wish_kinds, turn, withdraw: set[str])` | 서명의 마지막 인자 = 검증 뒤 `withdraw` 집합(옛 `retract_yes`) — 본문 뜻 그대로(RV2 · RV3) · OU4(`follow` 대상이 이미 객체에 있으면 급 그대로 `KEEP` · `history` 에 턴만 · 없으면 `said`) · OU5(`new` 의 앞 대상 = UP6 그대로) · OU11(바람 = `kinds` 가운데 `WISH_KINDS`) |
| `focus` | `state._focus` | OU9 — 이번 턴 `said` 고민 가운데 **`order` 가 가장 큰 것**(글자 자리 `start` 를 읽지 않는다) · 이번 턴 고민 없으면 그대로 · `viewing`(FD6) 규칙 그대로 |
| 거둠 | — | OU8 — `retract` · `retract_yes` · `observe` · `_decision_state` · `ask_nouls` import 지움(X-20 ~ X-24) |
| 부위 거르개 | `consult/site_filter.py` `def decide(acc: Accepted, obj: dict, prev_row: dict \| None, focus: str \| None) -> dict` → `{sites[], carried[], from, pair_kept[], pair_dropped[]}` | VF8 ⓒ(`targets` 의 부위 가운데 `acc.sites` 에 없는 것은 거르개 아님) · **OU7 넷이 다 맞을 때만 이음**: ⓐ `acc.targets` 전부 `concern` ⓑ `acc.sites == []` ⓒ 바로 앞 **성공** 턴(`prev_row` = 오류 없는 마지막 켠 줄 — 실패 턴은 건너뛴다)의 `consult.understand.accepted.targets` 가 전부 `site` ⓓ 그 턴 `consult.ask.slot == "concern"` 이고 `about` 이 그 부위 → 그 턴의 `site_filter.sites`(없으면 그 턴 `targets` 의 부위)를 `carried` · `from` = 그 턴 번호 · QS3(같은 이름 부위는 짝 고민이 `focus` 일 때만 — `pair_kept` · `pair_dropped`). 결과 = 장부 `consult.site_filter`(§6-1) |
| `filter_sites` | `state.py:65-68` | **조회 쪽에서 더 안 부른다**(QS1 — WP-5). 함수는 지운다(부르는 곳 0 — 지울 곳 grep 에 더함) |

**시험**(`tests/test_v04_object.py` — S8-T6 · S8-T7 · S8-T8 의 객체 · 거르개 몫): S8-T6 의 기대 전부(순서 시험 [A, B] → B · [B, A] → A 포함) · S8-T7 의 여덟 꼴 · S8-T8 의 객체 · `site_filter` 몫(조회 몫은 WP-5). **돌릴 파일**: `tests/test_v04_object.py` · `tests/test_state_object.py` · `tests/test_state_carry.py` · `tests/test_v03_fixes.py`(§15 처분 뒤).

## 11. WP-5 — ⑤ (가) 객체 기준 조회(QS1 ~ QS6)

| 고칠 · 만들 것 | 어디 · 서명(제안) | 내용 |
|---|---|---|
| 거르개 | `plan.qy1_calls(obj, site_names: list[str])` | QS1 · QS2 — `site` 값 = **이번 턴 거르개**(`site_filter.sites`)의 **이름**(목록 `entity_name` — `EntryList.items` 에서) · 여럿이면 부위마다 조회 하나 · `[]` 면 거르개 없이 하나. 객체 `sites[]` 축을 읽지 않는다 |
| 앞 리스트 유지 | `plan.run(obj, reader, *, site_names, prev_focus, prev_lists)` | QS4 — `focus` 가 그대로 · 이번 턴 거르개 `[]` → 리스트 ② 조회 0 · 앞 리스트(`Conv` 의 마지막 `list` 상태)를 그대로. `focus` 가 바뀌었거나 거르개가 있으면 다시 조회 · `Conv.memo` 그대로 · OU5(축 · `focus` · 거르개가 앞과 같으면 객체 기준 조회 0) |
| QY7 | `plan.py:220-223` · `consult/site_index.py` `async def concerns_of_site(hub, el: EntryList, site_code: str) -> tuple[list[str], dict \| None]` | QS6 — 선택지 = ⓐ `concern_site` 로 묶인 고민(먼저) ∪ ⓑ 지금의 `facets(site, indication)` 행의 고민 · 같은 고민 한 번. ⓐ 의 색인 = `gold_hash` 마다 **그 `gold_hash` 로 QY7 이 처음 서는 턴에** 한 번 지음(서버 시작 때 미리 짓지 않음) — 목록의 고민 마다 `concern_candidates(concern_code, limit=1)` 머리 `sites[]` 의 `match` = `직접` → `site_code → [concern_code]` · 프로세스 메모리 캐시 · 지은 턴에만 장부 `consult.site_index{built, concerns, ms, calls}`(O8-1). **허브 계약 변경 0** · 이 조회는 `plan.ALLOWED` 의 `concern_candidates` 안이다 |
| 나머지 | — | QS5(QY2 · QY3 · 시너지) 그대로 |

**시험**(`tests/test_v04_plan.py` — S8-T8 조회 몫 · S8-T13 · S8-T16): 턴 1 고민 + 부위 A · 턴 2 같은 고민 + 부위 B → 턴 2 `concern_candidates.site` = B 이름 하나 · 장부 `site_filter.sites` = 조회에 건 값 · 부위 없는 `new` + `focus` 그대로 → 리스트 조회 0 · `focus` 바뀜 + 부위 없음 → 거르개 없는 조회 하나 · QY7 선택지(묶인 고민 먼저 · facets 0 행이어도 나옴 · 색인 `gold_hash` 마다 한 번 · 지은 턴에만 `site_index`) · 재조회 없음(허브 호출 0 · `list` 이벤트 없음). **돌릴 파일**: `tests/test_v04_plan.py` · `tests/test_state_plan.py` · `tests/test_state_list.py`(§15 처분 뒤).

## 12. WP-6 — ⑤ (나) 답 재료(QM1 ~ QM5 · §3-1 KS · §3-2 DP8 · §3-3 VP8 · §3-4)

| 만들 · 고칠 것 | 어디 · 서명(제안) | 내용 |
|---|---|---|
| 공개 감쌈 | `walk/front.py` 끝에 **더하기만**: `async def coverage_of_nodes(hub, nodes): return await _coverage(hub, nodes)` · `def ranges_for(pairs): return _ranges_for(pairs)` · (KS 가 `_kind_rows` 를 쓰면) `def kind_rows(*a, **k): return _kind_rows(*a, **k)` | §3-4 · F-10 — 감싼 함수의 본문 · 기존 줄 변경 0 · 감쌈 본문은 부르는 한 줄(S8-T18). 이름은 제안(B-1) |
| 정보 종류 | `consult/kinds_pick.py` `def decide(entries: list[Entry], kinds: list[str], coverage: dict, …) -> tuple[list[str], list[str], list[str], dict[str, str], list[str]]` → (`kinds`, `required`, `offered`, `by`, `ranges`) | §3-1 KS1 ~ KS8 — 고른 것 = `yes` · KS2(`top`) · KS4(`kd10`) 없음 · KS3(`entry`) · KS5(`kd9`) · KS6(`default`) · KS7(범위 식 그대로 · KD11 = 그 범위에 `yes` · `entry` 가 있으면 안 고른 기본 묶음 종류는 `offered`) · KS8 · KD4 · KD7 그대로. 재료 = `nonzero_rows`(`front.py:179`) · `range_of`(`walk/kinds.py:111`) · `is_attr_start`(`walk/ranges.py:23`) · `ranges_for`. **걷기 `_decide_kinds` 를 고치지 않는다** — 갈리는 곳 = KS2 · KS4 · KS7 · KS8 넷뿐(S8-T9) |
| 재료 걷기 | `consult/material_read.py` `async def build_walk(d: Deps, acc: Accepted, site_codes: list[str], el: EntryList) -> Walk` | QM1 — 도는 턴 = `new` · `follow` + 검증 뒤 대상 1 이상 · 대상 = `targets`(`sure` 무관) + 이번 턴 부위(거르개 입구 — BR1) → `Entry(table, code, name, by="target")`(`walk/calls.py:55`). 차례(§3-4 표 · `col_b.py:161-227` 와 같은 호출 순서 · 같은 값): `FrontResult` 짓기(`entries` · `kinds` · `required` · `offered` · `by` · `ranges` · `attr_start` · `coverage`(= `coverage_of_nodes`) · `groups` · `links`(대상 둘 이상 — `scope_links` · `group_targets`) · `applicable_kinds` · `end` = QM3 일 때만) → `plan_calls(entries, kinds, groups=…)` → `read_calls(hub, calls, w.verified, w.ledger, w.reads, read_as_by_node=None)` → `_labels(d, w)` → `same_day_marks(w)` → **깊이**(DP8 — 아래) → `rq1(f, reads)` → `build(verified, decisions=…, speak_names=w.labels, inherited_kinds=…)` → `roster` → `check(…)` → `_end_check(d, w)` → `es.decide(…)` → `w.end_state` · `w.reason` · `w.material` |
| 깊이 | 같은 곳 | DP8-1 ~ DP8-6 — `depth_candidates` · `depth_calls` 그대로 · 후보가 **이번 턴 대상 노드**면 `gate_forced` → `depth_calls` 로 깊이 조회(`read_calls(…, depth=…)`) · 그 밖 전부 `listed_only`(폭 행은 재료에 그대로) · 걸음 한 번 · `DepthResult(decisions=…, required=rq1)`(`steps` · `jev_requests` · `answer_ready` 기본값) · `check(decisions=…)` 칸 꼴 그대로(`noul` 등 `null`) |
| 값 | 같은 곳 | VP8-1 ~ VP8-3 — `value_pick` 안 부름 · 표지 0 · 미루던 부작용 상세(`adverse_detail`)는 **폭 읽기에서 전부**(미루지 않는 쪽의 `plan_calls` 값 — 걷기에서 미루는 자리가 `value_pick` 가지라면 그 가지를 안 타는 것으로 같은 결과인지 구현 때 확인 · 다르면 보고) |
| QM3 | 같은 곳 | 대상 0 인 `new` → `end` = 「입구 없음」 · `out` 참 + 대상 0 + `kinds` 0 → 「범위 밖」(`front.py:306-313` 의 종료 상태 값 그대로) |
| 재번호 | `turn.py` | `mat.renumber(w, …, v3=True)` 그대로 · `judgement_v3` 의 `turn_kind` = `acc.kind`(AN1 — `material.py` 한 줄 · B-2) |

- `Deps` 는 지금 상담이 쓰는 것을 그대로(`_labels` · `_end_check` 는 `d.hub` 만 읽는다 — Jev 0).
- **걷기 코드를 상담 쪽에 베끼지 않는다**(두 벌 금지) — `build_walk` 는 §3-4 의 함수를 부르기만.

**시험**(`tests/test_v04_material.py` — S8-T9 · S8-T10 · S8-T11 · S8-T18 의 일부): KS 표 · `_decide_kinds` 에 같은 입력(yes = 1.0 · 그 밖 0.0)을 준 결과와 KS2 · KS4 가 닿지 않는 경우 같은 `kinds` · `required` · 깊이(이번 턴 대상만 · Jev 가짜 0 번) · 값(부작용 상세 전부 · `value_pick` 표지 0) · **같은 가짜 허브 · 같은 대상 · 같은 종류로 `col_b.walk()`(Jev 가짜가 같은 값을 낸 꼴)와 `build_walk()` 의 `verified` · `material` 줄 · 종료 상태가 같다**(깊이 · 값 가지를 안 타는 입력에서 — 폭 원칙 · 관문 · 번호가 0.3 과 같은 코드임을 기계로) · 감쌈이 한 줄인지(소스 검사). **돌릴 파일**: `tests/test_v04_material.py` · `tests/test_walk_front.py` · `tests/test_walk_core.py` · `tests/test_walk_material.py` · `tests/test_columns.py`(**안 고친 채 통과** — S8-T18).

## 13. WP-7 — 턴 흐름 · 실패 길 · 화면 · 빈 칸(§2 · §4-1 · DT1 ~ DT5 · BQ1 ~ BQ5)

| 고칠 것 | 어디 | 내용 |
|---|---|---|
| 켠 가지 | `turn.py` `run_turn` · `Consult` | §5 의 흐름 — `Consult.understand()`(① ② ③) · `after_understand(acc)`(④ ⑤ ⑦) · X-4 · X-8 ~ X-15 지움 · 끈 가지(X-2 · X-3)는 손대지 않는다(`carried_in` 계산을 끈 가지 안으로만 옮김). `talk` 턴: 객체는 `withdraw` 로만(OU10) · 안 바뀌면 조회 0 · `list` · `sites` 안 보냄(TT2) |
| 실패 길 | 같은 곳 | FL1 ~ FL6 — `error{kind: timeout \| cli \| json \| list}` → 객체 diff `[]` · 허브 조회 0 · `list` · `sites` 안 보냄 · 종료 상태 「입구 없음」(0.3 말 · 새 문구 0) · 답 LLM 은 부름 · `resolve` · `walk()` · Jev · 다른 모델 · 재시도 0 · 다음 턴 정상 · 실패 턴은 다음 턴 대화 블록에 `failed` 표지(FL4 — WP-2) · 검증으로 다 버려진 턴 = QM3(FL6) · SSE 는 `delta` → `done`(`turn_error` 아님) |
| 점 | `plan.derive`(`:228-266`) · `sites.site_pairs`(`:88-92`) | DT1 — 고민마다 `concern_candidates.sites[]` 의 **`match` = `직접`** 만 점(`하위` 는 점 아님 · `data-match` 값 `직접` 하나) · DT3 — 하위 부위는 `plan.sub_sites`(BK4 선택지)로 그대로 · `viewable_subs`(W-1)는 **코드를 남기고** 부르는 자리가 비는지 보고(DT2 · O8-4) |
| NQ5 | `blanks.pick(…, qy7_new: bool = False)` | BQ4 — 이번 턴 `new` 이고 QY7 이 선 턴(대상이 부위뿐 · `focus` 없음)이면 NQ5(`blanks.py:99-100`)를 걸지 않는다 · 그 밖 그대로 |
| BK5 | — | BQ2 — `sure` false → `guess` → BK5 그대로(새 문구 0) |
| 단계 | `steps.py` · `turn.py` | UC10 · DT5 — `list` · `sites` 는 ⑤ 뒤 곧바로(LLM 을 기다리지 않음) · `hold` · `release`(B-11) 지움 |

**시험**(`tests/test_v04_turn.py` — S8-T12 · S8-T14 · S8-T15 · S8-T16 · S8-T18 의 「켠 턴에서 Jev · `hub.resolve(text=…)` 0 번」): 가짜 CLI(`understand.json`) · 가짜 허브 · 가짜 Jev(부르면 실패하는 가짜) 로 한 턴 · 실패 넷 · 점(직접만 · 하위 선택지에는 있음 · 고민 둘 합집합 · 거두면 빠짐) · NQ5 두 꼴 · 재조회 없음. **돌릴 파일**: `tests/test_v04_turn.py` · `tests/test_consult_turn.py` · `tests/test_state_examples.py` · `tests/test_state_blanks.py` · `tests/test_consult_sites.py` · `tests/test_v03_sites.py` · `tests/test_v03_turn_kind.py` · `tests/test_consult_carry.py`(§15 처분 뒤) + §4 의 grep(남는 줄 표).

## 14. WP-8 — 장부 · 패널 · SSE(§6)

| 칸 | 0.4 | 어디 |
|---|---|---|
| `consult.understand` | `{model, thinking, pick_version, list_sha, aliases, input_bytes{system, message}, output_raw, parsed{…}, accepted{…}, dropped[], merged[], added_from_sites[], ms, api_ms, usage{input_tokens, cache_read_input_tokens, output_tokens, thinking_tokens}, error \| null}` — 턴 메시지 전문은 안 싣고 바이트 수만 | `turn.py` `Consult.ledger` |
| `consult.site_filter` | `{sites[], carried[], from, pair_kept[], pair_dropped[]}` — **조회에 실제로 건 값**(채점 검사 3 이 읽는다 · 칸 이름 그대로 — B-7) | 같음 |
| `consult.site_index` | 지은 턴에만 `{built, concerns, ms, calls}` | 같음 |
| `consult.turn_kind` | `{kind, from: understand \| first_follow \| talk_max \| bad_value}`(`nouls` · `rule` · `requests` · `walks[]` 없음) | 같음 |
| `consult.follow_target` | VF6 의 앞 대상 | 같음 |
| 없어지는 칸 | `consult.retract*` · `options_carried` · `jev_requests` · 턴 줄 `targets[].by` · `noul` · `kinds[].noul` · `top` · `kd10` · `trace.front.targets` · `trace.entry` · `trace.entry_pick` · `source.noul` · `decision` · `matched` · `covered_by` · `timing.parts.jev_ms` · `walk_ms` | X-1 · X-5 ~ X-7 · X-18 · X-19 |
| 턴 줄 `targets[]` | `{table, code, name, sure, how}` | `turn.py` `targets_of` 를 켠 턴에 맞춘 함수로 |
| `kinds[]` · `trace.front.kinds[]` | 종류마다 `by`(`yes` · `entry` · `kd9` · `default`) · `offered[]` | 지은 `FrontResult` |
| `trace.depth` | `{decisions{id: gate_forced \| listed_only}, read[]}` | `build_walk` |
| `timing.parts` | `understand_ms` · `hub_ms` · `llm_ms` · `material_ms` | `run_turn` |
| `consult.queries[]` | 그대로 · `skipped` 값 이름 `material` | `plan.Reader` |
| `sites.dots[]` | 직접만 | WP-7 |
| 객체 패널(SV8) | 턴 묶음에 `turn_kind{kind, from}` · `close` · `ask` + `understand` 의 `accepted` · `dropped` · `merged` · `ms` · `error` + `site_filter` — 칸 이름 = 장부 키(문구 0 · 패널 새 `data-slot` 0) | `render.state_view` · 패널 조각 |
| SSE | 이벤트 이름 · 자리 · 조각 꼴 그대로(새 0 · 없어짐 0) · 실패 턴 = `delta` → `done` | — |

- 쓴 줄은 고치지 않는다 · 옛 줄(rev 3)은 옛 꼴 그대로 읽힌다(드로어 · 되읽기는 `consult_rev` 로 가른다).

**시험**(`tests/test_v04_ledger.py` — S8-T17): 칸 전부 · 없어진 칸이 줄에 없음 · `consult_rev` 4 · 패널 조각에 `understand` · `site_filter` 키 · 한글 문장 0. **돌릴 파일**: `tests/test_v04_ledger.py` · `tests/test_consult_ledger.py` · `tests/test_v03_frame.py`(§15 처분 뒤).

## 15. WP-9 · WP-10 · WP-11

### 15-1. WP-9 — 프롬프트 `pick` · 적재기(§7 · F-7)

| 고칠 것 | 어디 | 내용 |
|---|---|---|
| `pick` 절 | `prompts/consult.json` | SPEC §7 `rules[]` 초안 **글자 그대로**(줄 단위 배열) · `version` = `0.4.0-draft` · `headers{history, object, utterance}` = 시안 글자(`# 대화 지금까지` · `# 지금 객체` · `# 이번 말`) + B-4 의 둘 · `marks{failed, same_list, none}`(턴 메시지 안 표지 — 사람에게 안 보임 · 글자는 B-4). `system[]` · `system_v3` · `jev_front` · `jev_state` · `steps` 는 **안 바꾼다** · 최상위 `version` 은 지금 값 그대로(`-draft` 가 붙어 있으면 그대로 — `draft` 뜻 불변) |
| 적재기 | `consult/prompt.py` | `ConsultPrompt.pick: dict \| None` — `version`(빈 글 아님) · `rules[]`(1 줄 이상 · 빈 줄 아님) · `headers` 셋 · `marks` 셋 하나라도 없거나 비면 `None` · `KEYS` 그대로(`jev_front` 를 지우면 `keys` 오류 — 지금 그대로) · `state_ready` = `system_text_v3` · `pick` · `turn_headers.consult` · `kind_labels` 14 · `voice_check` · V3 머리 둘(**`jev_state.retract` · `jev_front.target_option` · `turn_kind` 셋을 뺀다**) · `draft` = 최상위 `version` 만 |
| E8-2 | 시험 | `rules[]` 의 따옴표(「」) 안 예문이 `$RS/conversations.jsonl` **전체 턴** 글과 공백 무시 부분 문자열로 겹치는 것 0(규칙 11 의 종류 풀이 낱말 · 단계 이름은 SPEC §7 이 밝힌 예외 — 따옴표 밖) |

**시험**(`tests/test_v04_prompt.py` — S8-T20 · E8-2): **돌릴 파일**: `tests/test_v04_prompt.py` · `tests/test_consult_prompt.py` · `tests/test_v03_prompt.py` · `tests/test_state_blanks.py`(`state_ready` 두 자리 — §15-4).

### 15-2. WP-10 — 끈 상태 막기 · `consult_rev` 4 · 설정(CP1 · CP7 · C8-8 · §4-2)

| 고칠 것 | 어디 | 내용 |
|---|---|---|
| 기본값 | `config.py:82` | `chat_state = "on"` · 주석의 「기본은 끈 상태」 줄을 0.4 뜻으로 |
| 새 대화 | `ledger.state_at_start`(`:195-201`) | **새 대화(시작 줄 0)는 늘 `on`** — 설정값이 `off` 여도(CP1 · S8-T19) · 대화 첫 값이 있으면 그 값 · 시작 줄이 있는데 값이 없으면(0.1 대화) `off`(그대로) |
| 판 | `ledger.CONSULT_REV`(`:32`) | **4** |
| 막기 | `ledger.blocked`(`:204-214`) | ① 켠 대화 `consult_rev < 4` → `rev_changed`(지금 줄 그대로 — rev 3 이 여기 걸린다 · C8-4) ② **끈 대화(`consult_state` = `off` · 시작 줄 있음) → `rev_changed`**(C8-8 — 같은 자리 · 같은 꼴 · 줄을 쓰지 않는다 — 0.3 B-5). 코드 값을 새로 짓지 않고 `rev_changed` 를 쓴다(B-9) |
| 열기 | `server.py` · `drawer.py` | 옛 끈 대화 · rev 3 대화는 열면 지난 턴 · 드로어가 0.1 · 0.3 꼴 그대로 보인다(지금 `outdated` 길) · `POST …/turns` 는 `blocked` 로 막힘(새 턴 줄 0 · Jev · 허브 0) |
| 빈 자리 | 템플릿 하나 | 옛 **끈** 대화를 열었을 때 막힘을 보일 **빈 `data-slot` 하나**(이름 제안 `conv-off-closed` — B-10) · 문구 0(U8-3 빈칸 · 사용자 확인 대상). 0.3 의 `conv-outdated` 자리(rev 3)는 그대로 |
| 설정 아홉 | `config.py` · `.env.example`(이름만) | `chat_pick_model`(`sonnet`) · `chat_pick_effort`(`low`) · `chat_pick_thinking`(`off` — 뜻 = WP-0) · `chat_pick_timeout_sec`(`10`) · `chat_pick_aliases`(`on`) · `chat_pick_list_cache`(`on`) · `chat_pick_context_turns`(`2`) · `chat_pick_answer_chars`(`200`) · `chat_pick_list_max`(`30`). 켠 상태에서 안 읽게 되는 설정(`CHAT_CARRY_TURNS` · `CHAT_RETRACT` · `CHAT_TURN_KIND` · `JEV_NOUL_*` · `JEV_KIND_READ_AT` · `JEV_BATCH_SIZE` · `WALK_MAX_STEPS`)은 **지우지 않는다**(시험 앱 B 열이 읽는다) |
| 끈 가지 코드 | `turn.py:121-125` | **남김**(CP7) — 부르는 곳이 없어진 것을 S8-T19 가 본다 |

- **0.4 서버에 남은 옛 끈 대화 수**(SPEC U8-3 근거 칸 · 0.2.0 「확인하지 못한 것」): 워커는 **세지 않는다**(코디 서버 장부 — 18222 의 `CHAT_DIR`). 코디 몫(§16-2).

**시험**(`tests/test_v04_state_gate.py` — S8-T19 · S8-T17 의 rev 몫): **돌릴 파일**: `tests/test_v04_state_gate.py` · `tests/test_v03_start.py` · `tests/test_v03_fixes.py` · `tests/test_v03_frame.py` · `tests/test_consult_ledger.py` · `tests/test_consult_page.py`(§15-4 처분 뒤).

### 15-3. WP-11 — E8-pre 채점기를 0.4 장부에 맞춤(`$SC`)

**SPEC**: §8-1 E8-pre · F-4. **옛 칸 길을 남긴다** — 0.3 장부(`runs/now-rows.jsonl`)로 돌린 수가 고치기 전과 같아야 한다.

| 고칠 것 | 어디 | 내용 |
|---|---|---|
| 판 가르기 | `score.py` `now_turn`(`:85-`) | 줄의 `consult.understand` 가 있으면 0.4 길 · 없으면 지금 길(한 함수 안에서 가르거나 `now_turn_v04` 를 더함) |
| 대상 | 같음 | 0.4: `targets[]{table, code}`(`by` 를 읽지 않는다) |
| 거둠 | 같음 | 0.4: `consult.understand.accepted.withdraw` ∪ `consult.after` 의 `withdrawn` |
| 부위 거르개(검사 3) | 같음(지금 `fs` · `filt` 식 — `after.sites` 의 `said` · `confirmed` + `pair_concern` · SPEC 이 적은 85 ~ 98 행) | 0.4: **`consult.site_filter.sites`** 를 그대로 |
| 턴 종류 | 같음 | `consult.turn_kind.kind`(두 판 같은 자리) |
| 정보 종류(E8-6a) | `kinds_score`(`:40`) 를 부르는 자리 | 0.4: `consult.understand.accepted.kinds` 를 `kinds_score`(엄한 쪽)로 · 0.3 은 지금 그대로 |
| 재료 · 깊이(E8-6b) | `score.py` 에 검사 ⓐ ⓑ ⓒ 를 더함 · `slim.py` | `slim.py` 가 `material.new_lines[].gid` · `material.seen_lines` · `trace.depth.decisions` · `consult.understand` · `consult.site_filter` 를 더 싣는다(`CONS` 에 `understand` · `site_filter` · `site_index` · `follow_target` 더함). ⓐ `key.material.rows` 묶음 전부 ⊆ 재료(새 줄 ∪ 앞 줄이 가리킨 gid) ⓑ `gate_forced` ⊆ `key.material.depth` ⓒ `depth` 가운데 깊이 후보로 선 것 전부 `gate_forced` · 0.3 쪽(WP-0 `v03-c74`)과 재료 줄 집합 견줌(0.3 에만 · 0.4 에만 · FT5 넘은 턴 수) |
| 층 가르기 | 같음 | 옛 층(`trace.front.targets` · `trace.entry` · `trace.entry_pick` · `consult.retract`)이 0.4 줄에서 비어 있어도 떨어지지 않는다(층은 `checks` 만 본다 — README) |
| 출력 자리 | `score.py` · `paths.py` 를 고치지 않는다면 env 로 | **조사 산출물을 덮어쓰지 않게** 0.4 채점의 출력 폴더를 env(`INPUT_SPACE_OUT` 제안 · 기본 = 지금 자리)로 받는 줄을 더하고 0.4 실행은 `$RS/runs/v04-score/` 로 낸다(B-6) |
| 답 LLM 실제 호출 | `run_now.py` | 인자 하나 더함(`--real-answer C56,C57,C58,C65,C69` 꼴) — 그 대화들은 `Fake` 대신 지금 앱의 답 LLM(`Ctx` 의 기본 `ChatLLM` — 구독 CLI · 소넷 · `--resume`)으로 · 그 밖은 빈 답. **5 대화 · 25 턴**(SPEC §8-1 — `ref.to` = `answer` 5 턴이 든 대화 전부) · 허브 주소는 env(`HUB_REST_URL` — 18107) |

**끝 조건**: ① `INPUT_SPACE_NOW=now-rows.jsonl python3 score.py`(옛 장부)의 `summary.json` 수가 고치기 전과 **같다**(세션 임시 폴더에 고치기 전 출력을 떠 두고 견준다 — 조사 산출물 자리를 덮지 않는다) ② 0.4 장부 표본 3 대화(WP-12 의 첫 실행에서 — 아무 3)로 검사 8 개 · 정보 종류 · E8-6b 셋이 `None` 아닌 값. **시험**: 스크립트라 pytest 없음 — 위 ① ② 의 출력을 보고에 붙인다.

### 15-4. 바뀌는 기존 시험(S8-T18 밖 · 이름으로 · 「예상」 = 이 워커가 시험 이름 · grep 으로 본 것 — **WP 첫 실행에서 확정**하고 다르면 보고)

| 파일(시험 수) | 바뀌는 시험 | 처분 | 까닭 |
|---|---|---|---|
| `test_v03_turn_kind.py`(16) | `t1_judge_order_and_threshold` · `t1_first_turn_no_request_then_one_request` · `t1_request_error_is_new_and_recorded` · `t1_extra_on_first_chunk_only` · `t2_talk_without_prev_ask_cancels_walk` · `t2_talk_with_prev_ask_waits_walk_and_discards` · `t3_talk_option_yes_enters_and_queries` · `t3_talk_retract_yes_withdraws` · `t4_follow_no_entry_reruns_with_prev_subject` · `t5_new_with_match_one_walk_without_match_entry_pick` · `t5_turn_kind_off_is_0_2_call_order` · `t25_abbr_candidate_yes_only`(매개 둘 이상) · `tw7_carry_alive_in_object` | **지움 13** | 가르기 Noul · 걷기 거둠 · 두 번째 걷기 · 든 후보 — 켠 상태 기대가 없어졌다(SPEC §8-3 끝 불릿 · X-8 ~ X-12 · X-25) |
| | `t2_talk_steps_understand_then_answer` · `t7_talk_max` | **고침 2**(0.4 꼴로 — 가짜 이해 출력 `talk` · 잇단 `talk`) | TT5 · TT6 은 0.4 에도 있다(UC10 · VF11) |
| | `t4_follow_target_order_and_withdrawn` | 그대로 | `follow_target` 남김 |
| `test_state_carry.py`(7) | `s5_t3_options_carried_yes_only_no_entry_pick_one_turn` · `w4_option_answered_by_name_is_text_and_counts` · `w8_all_options_fail_then_entry_pick_runs` · `s5_t6_retract` · `retract_failure_keeps_turn` | **지움 5** | 든 후보 · 입구 고르기 · 거둠 요청(X-9 · X-23) — 선택지 답 · 거둠은 `test_v04_object.py` 가 0.4 꼴로 |
| | `with_options_merges_previous_target` · `s5_t20_front_without_origin_is_unchanged` | 그대로 | `carry.with_options` · `walk.front` 는 남는다 |
| `test_state_object.py`(10) | `s5_t1_slots_closed_lists` · `s5_t2_t17_certainty_named_not_in_object` · `w2_same_name_site_pairs_with_concern`(`observe` 를 부르는 꼴이면) | **고침**(재료를 `observe_accepted` 로) 또는 지움(뜻이 걷기 trace 에만 있으면 — `named`) | X-22 |
| | `s5_t7_two_concerns_focus_moves_and_returns` | **고침** | OU9 — `focus` = `targets` 순서 |
| | `s5_t13_…` · `s5_t18_…`(둘) | **고침**(가짜 Jev → 가짜 이해 출력) | 켠 턴 흐름 |
| | `off_state_has_no_consult` | **고침** | CP1 — 새 대화는 늘 켬 · S8-T19 와 겹치면 지움 |
| | `s5_t4_derived_procedures` · `s5_t5_guess_is_not_an_axis` | 그대로(DT1 로 `derive` 의 점 재료가 바뀌면 고침) | — |
| `test_consult_turn.py`(11) | 10 개(`t6_order_t7_tail_hidden_and_ledger` · `t6_out_of_scope_has_no_list_or_sites` · `t16_reload_…` · `t20_…` · `t21_…` · `t22_…` · `w8_build_changed_…` · `w8_turn_limit_and_busy` · `w8_message_over_limit_aborts_ft5_without_list` · `prompt_changed_marked_and_kept_copy_used`) | **고침**(가짜 CLI 에 `understand.json` · `t6_out_of_scope` 는 `out` = 참 길) | `consult_fixture.make_settings` 가 `chat_state` 를 주지 않아 지금 **끈 상태(기본 `off`)로 돈다** → 기본 `on` 이 되면 켠 가지로 돈다(CP1). SPEC-004 의 뜻(T6 · T7 · T16 · T20 ~ T22 · W8)은 0.4 켠 턴에도 서야 한다 |
| | `t12_flow_second_turn_carries_previous_target` | **지움** | 든 후보(AR-9) — 0.4 는 S8-T3 |
| `test_state_examples.py`(5) | 예 1 ~ 3 · `on_state_system_text_and_conv_keeps_state` | **고침 4**(가짜 Jev → 가짜 이해 출력 · 기대 객체는 같은 뜻) | 켠 턴 입구 교체 |
| | `s5_t15_off_state_is_0_1` | **지움**(S8-T19 가 대신) | CP1 |
| `test_v03_fixes.py`(7) | `s6_t21_off_conv_marked_but_runs_as_0_1` | **고침** → 「표지 · 열기 · 새 턴 막힘」(CP7) | 끈 대화는 0.4 에서 턴을 받지 않는다 |
| | `s6_t21_new_on_conv_has_rev_and_no_marker`(`== 3` `:105`) | **고침**(`CONSULT_REV` 로) | rev 4 |
| | `s6_t12_target_option_bk5_yes_confirm` | 재료가 `observe` 면 **고침** | X-22 |
| | 나머지 4 | 그대로 | `_again` · BK5 · `rev_less` · `w3_abbr_carry` 는 남는 함수 |
| `test_v03_start.py` | `[3, 3]` · `== 3`(`:29-30`) | **고침**(`CONSULT_REV` = 4) | rev 4 |
| `test_v03_frame.py` | 픽스처 `consult_rev=3`(`:51-54` · `:104`) | **고침**(`CONSULT_REV` 로 — 드로어 시험의 뜻은 「같은 판 대화」) | 서버 판 4 와 견주면 전부 `outdated` 가 된다 |
| `test_v03_prompt.py` | `state_ready` 가 `turn_kind` 를 요구하는 단언(`:44-45` · `:51` · `:60` · `:69`) | **고침**(S8-T20 — `pick` 기준 · `turn_kind` 가 없어도 참) | X-26 |
| `test_state_blanks.py` | `state_ready` 두 자리(`:107` · `:113`) · NQ5 를 보는 시험 · `w1_site_only_blank_and_not_with_focus`(`:77`) | **고침**(`pick` 을 더한 프롬프트로 · BQ4) | X-26 · BQ4 |
| `test_state_plan.py` | `qy1_calls` 를 객체 축 부위로 보는 시험 · `w1_site_only_gives_concern_options`(`:64`) | **고침**(QS1 이번 턴 거르개 · QS6 묶인 고민 먼저) | AR-4 · AR-11 |
| `test_consult_sites.py` · `test_v03_sites.py` | 하위 고민 부위도 점이라는 기대 | **고침**(DT1 — 직접만) · `viewable_subs` 시험은 그대로 | AR-5 |
| `test_state_list.py` | 부위 없는 턴에 리스트를 다시 짓는 기대가 있으면 | **고침**(QS4) | D-12 |
| **안 고침** | `test_walk_*.py` 다섯 · `test_columns.py` · `test_consult_carry.py` · `test_v03_shared.py` · `test_v03_e6.py` · `test_v03_close.py` · `test_v03_list.py` · `test_consult_listing.py` · `test_consult_material.py` · `test_consult_page.py` · `test_consult_chat_ui.py` · `test_consult_cli.py` · `test_state_synergy.py` · 시험 앱 묶음(`test_answer_key` · `test_batch` · `test_v06_*` …) | — | S8-T18 · 그 모듈을 고치지 않거나 뜻이 그대로. 이 가운데 §13 · §15-2 의 「돌릴 파일」 에 든 것은 **고치지 않은 채 통과**해야 한다(깨지면 고치지 말고 보고) |

**셈(예상)**: 지움 **20**(turn_kind 13 · carry 5 · consult_turn 1 · examples 1) · 고침 **약 30**(turn_kind 2 · object 6 · consult_turn 10 · examples 4 · fixes 2 ~ 3 · start 1 · frame 2 · prompt 4 · blanks 3 · plan 2 · sites 2 · list 0 ~ 1) · 그대로 확인 = 위 「안 고침」 줄. 확정 수는 WP 보고.

## 16. WP-12 — 실물 E8 표 실행 · 18224 화면 확인 · README

### 16-1. 워커 몫

| # | 무엇 | 어떻게 | 끝 조건 |
|---|---|---|---|
| 12-0 | 허브 18107(0.8.1) | WORK-016 §6 명령으로 CSV 판을 18107 에(WORK-016 이 띄운 채 넘겼으면 그대로 — WORK-016 B-2) · `health` 의 `gold_hash` 를 적는다 | 18107 `resolve` 목록 꼴이 820 개념(또는 그 판의 수) |
| E8-1 | 목록 글 대조 | 앱이 지은 목록 글의 항목 수 = 다섯 표 개념 수 · 시안 `pick-prompt.md` 의 「# 목록」 과 줄 단위로 견줘 다른 줄을 까닭과 함께 | 보고 |
| E8-2 | 예문 겹침 | WP-9 시험 | 0 |
| E8-3 · E8-4 · E8-6a | **표 전체** | `$SC` 에서 `HUB_REST_URL=http://127.0.0.1:18107 PYTHONPATH=$APP $APP/.venv/bin/python run_now.py v04 --real-answer C56,C57,C58,C65,C69`(그 밖은 빈 답) → `slim.py ../runs/v04/turns.jsonl v04` → `INPUT_SPACE_NOW=v04-rows.jsonl INPUT_SPACE_OUT=../runs/v04-score python3 score.py` | **입구 3 검사 `pass3_pct` ≥ 95** · **앱 전체 8 검사 `pass8_pct` ≥ 90** · **정보 종류 ≥ 90** — 분모 = `score.py` 가 낸 채점 턴(애매 턴 전부 밖 · D-15). 그 판의 대화 · 턴 · 애매 · 채점 턴 수를 함께 |
| E8-6b | 값 · 깊이 | 같은 실행의 C74 ~ C78(22 턴) · WP-0 `v03-c74` 와 견줌 | **ⓐ ≥ 90% · ⓑ = 100% · ⓒ = 100%**(U8-4) · 0.3 에만 있는 줄 수 · 0.4 에만 있는 줄 수 · FT5 넘은 턴 수 |
| E8-5 재료 | 사람 검수용 표 | 의도 꼴 · 말 꼴(`tags`)마다 표본 행(턴 · 손님 말 · 키 · 0.4 값 · 통과 여부) + **이름 박은 넷**(C05-2 · C15-3 · C28-3 · C38-4 — SPEC §8-1 「D-6 규칙과 표의 키」 · 각 턴의 `site_filter` · 앞 턴 `ask` · 고른 고민) | 표만 낸다(판정은 코디 · 사용자) |
| 실패 층 | 떨어진 턴 | `fail-by-tag` 꼴의 표(층 = `checks` 기준) · 층마다 대표 턴 셋 · `dropped[]` 수(지어낸 코드 수) · 이해 호출 오류 수 · `ms` 중앙 · p90 · thinking 토큰 합(0 이어야 — E8-0) | 보고 |
| 18224 | 실물 화면 확인(답 LLM 포함) | `lsof` 확인 → `CHAT_STATE` 없이 앱을 18224 에(허브 = 18107) · 대화 셋: 앞 답 글을 가리키는 말 · 거둠 · 애매한 말(`sure` false → BK5) + 실패 길 한 턴(`CHAT_PICK_TIMEOUT_SEC=1` 로 다시 띄워) + **옛 끈 대화 하나**(세션 임시 `CHAT_DIR` 에 `consult_state` = `off` 시작 줄을 둔 장부로 — 열림 · 새 턴 막힘 · 빈 `data-slot`) → 장부 `consult.understand` · `site_filter` · 객체 diff · 화면이 §2 대로인지 · **끝나면 자기 PID 만 내리고 `lsof` 로 확인** | 보고(스크린샷 · 장부 줄 요약) |
| README | 상담 절 | 0.4 한 묶음: 설정 아홉 · 이해 호출 · 목록 캐시 · 끈 상태 막힘 · `run_now --real-answer` 는 `$SC/README.md` 가 적는다(그 README 도 고친다 — 돌리는 법 한 줄) | — |
| 내림 | 18107 · 18224 | 자기 PID 만 · `lsof` 로 비었는지 | 둘 다 비었다 |

- 문턱에 못 미치면 **프롬프트 · 규칙을 고치지 말고** 수 · 떨어진 층 · 대표 턴을 보고한다(프롬프트는 사용자 확인 대상 · 키는 E8-5 몫). 코디가 다음 걸음을 정한다.
- 표 실행의 이해 호출 수(≈ 턴 수) · 답 LLM 실제 호출 수(25)를 보고한다.

### 16-2. 코디 · 사용자 몫

| 순서 | 무엇 |
|---|---|
| WP-12 뒤 | 워커 보고 검증 — 바뀐 WP 의 시험만 · grep(§4 · §16-3) · 코드 검수 발주 |
| 검수 PASS 뒤 | **18105 를 허브 0.8.1 로 · 18222 를 앱 0.4 로 같이 다시 띄운다**(SPEC-001 0.8.1 영향 표 — 0.3 앱을 0.8.0 허브에 붙이지 않는다) |
| 뒤 | 18222 서버 장부의 **옛 끈 대화 수**를 센다(U8-3 근거) |
| 뒤 | E8-5 표본 사람 검수(이름 박은 넷 포함) · E8-7 실물 화면(사용자) · U8-3 문구 · `pick` 프롬프트 문구 확인(사용자) |
| 뒤 | 커밋(앱 · 프로필 `$SC`) · SPEC 되적기(§17-3) |

### 16-3. 완료 조건 · 검증 명령

1. **단위 시험**: S8-T1 ~ T20 이 `tests/test_v04_*.py` 의 시험 이름 또는 주석으로 찾아지고 통과 · §15-4 의 처분대로 · WP 마다 돌린 파일 · 통과 수 · 고친 · 지운 시험 이름 · **전체 pytest 를 돌리지 않았다**.
2. **경로 나눔(S8-T18)**: `git diff --stat -- clinic_chat/columns prompts/jev clinic_chat/llm clinic_chat/web` 비어 있음(B-3 를 쓰지 않았다면) · `git diff -- clinic_chat/walk` 가 **더한 줄뿐**(`^-` 0) · 감쌈마다 본문 한 줄 · `tests/test_walk_*.py` · `test_columns.py` diff 0 · 통과.
3. **지울 곳**: §4 grep 의 남는 줄 = 끈 가지 · `prompt.py` 적재 · `e6.py` · `carry.py` 주석뿐 · `state.filter_sites` 부르는 곳 0.
4. **문구**: 새 템플릿 · `consult/` 새 코드에 한글 문장 0 · 새 `data-slot` = 하나(`conv-off-closed` 꼴) · `prompts/consult.json` 의 `pick` 밖 글자 변경 0.
5. **실물**: E8-0(thinking 0 · 끄는 법) · E8-1 · E8-3 ≥ 95 · E8-4 ≥ 90 · E8-6a ≥ 90 · E8-6b ⓐ ≥ 90 · ⓑ ⓒ = 100 · E8-5 표 · 18224 확인 — 못 미치면 그 수 그대로(완료 아님으로 보고).
6. **포트**: 18224 · 18107 내림 · 18105 · 18222 · 18432 를 건드리지 않았다.
7. **커밋 0**(앱 · 프로필).

```bash
# APP 에서 — WP-7 끝 · 마감 때(전체가 아니다)
rg -n '<§4 의 명령 그대로>' clinic_chat/consult/
git diff --stat -- clinic_chat/columns prompts/jev clinic_chat/llm clinic_chat/web clinic_chat/clients   # 비어 있다
git diff -- clinic_chat/walk | grep -c '^-[^-]'                                                         # 0
rg -n 'filter_sites' clinic_chat/                                                                       # 0
lsof -nP -iTCP:18224 -sTCP:LISTEN; lsof -nP -iTCP:18107 -sTCP:LISTEN                                    # 비어 있다
git status --porcelain                                                                                  # §2 allowed_paths 안뿐
```

## 17. 열린 것 · 이 문서를 쓰며 본 것(SPEC 은 고치지 않았다)

### 17-1. 열린 것 · 사용자 확인 대상

| # | 무엇 | 상태 |
|---|---|---|
| O-1 | **U8-3 옛 끈 대화를 막는 화면 문구**(빈 `data-slot` 하나) | **빈칸** — 사용자 확인 대상 |
| O-2 | `pick` 프롬프트 문구(SPEC §7 초안 · 규칙 12 의 「예약 · 위치」 예 포함) | 사용자 확인(구현은 초안 그대로) |
| O-3 | O8-1 실서버 지연 · 캐시 식은 첫 호출 · QS6 색인 턴 | 구현 뒤 서버에서(코디) — WP-0 · WP-12 의 수가 재료 |
| O-4 | O8-2 ~ O8-5(표 밖 꼴 · 「받아 본 것」 · `viewable_subs` · `entry_pick` · `abbr_yes_only` · 안 읽는 설정 정리 · 긴 대화의 블록 길이) | 마감 뒤 |
| O-5 | 0.4 서버의 옛 끈 대화 수 | 코디(§16-2) |
| O-6 | E8 문턱 미달일 때 다음 걸음(프롬프트 · 키 · 규칙) | 코디 · 사용자 |

### 17-2. B — 구현 워커가 추측으로 메우지 않게 이 문서가 정한 값(코디가 바꿀 수 있다)

| # | 무엇 | 이 문서의 값 | 왜 |
|---|---|---|---|
| B-1 | 새 모듈 · 감쌈 이름 | `entry_list` · `understand` · `verify` · `site_filter` · `site_index` · `kinds_pick` · `material_read` · `walk/front.py` 의 `coverage_of_nodes` · `ranges_for` · (`kind_rows`) · 실측 `consult/e8.py` | SPEC §3-4 「감쌈 이름은 제안 — WORK 가 정한다」 |
| B-2 | `material.py` | `judgement_v3` 의 `turn_kind` 값 출처 한 줄만(검증 뒤 `kind`) — 그 밖 diff 0 | AN1 |
| B-3 | `columns/` 감쌈(C8-9) | **쓰지 않는 것이 기본** — `_labels` · `_end_check` 를 그대로 import 해 서명이 맞으면 `columns/` diff 0. 맞지 않을 때만 `col_b.py` 끝에 한 줄 감쌈(더하기만)을 더하고 보고 | 코디 「필요하면」 |
| B-4 | 턴 메시지의 답 요약 · 리스트 줄 머리 글자 · `marks` 글자 | `pick.headers` 에 키 둘(`answer` · `list` 제안) · `marks` 셋 — 글자는 **시안 `pick-prompt.md` 에 있는 것이면 그대로 · 없으면 짧은 기호 꼴**(예 `(이해 실패)` 는 SPEC FL4 의 글자 그대로) · 사람에게 안 보인다 | SPEC §7 「WORK 에서 정한다」 · FL4 |
| B-5 | VF4 의 `norm` | `consult/verify.py` 에 한 줄 함수(공백 연속 제거 + 소문자) — 허브 코드를 import 하지 않는다(다른 레포) | SPEC VF4 · R1 |
| B-6 | 채점 출력 자리 | env `INPUT_SPACE_OUT`(기본 = 지금 자리) · 0.4 는 `$RS/runs/v04-score/` · 0.3 기준선 장부 `$RS/runs/v03-c74/` | `score.py` 가 `now-turns.jsonl` · `summary.json` 을 덮어쓴다(README) — 조사 산출물 보존 |
| B-7 | 장부 칸 이름 | SPEC §6-1 그대로(`consult.site_filter` 등) — 바꾸지 않는다 | 채점(E8-pre)이 그 이름을 읽는다 |
| B-8 | `e6.py` | 안 고친다 — `:88` 은 0.4 줄에서 `KeyError` 가 나지만 0.3 장부 전용 도구다(0.4 실측은 `e8.py`) | 0.3 산출물 |
| B-9 | 옛 끈 대화 막힘의 코드 값 | `rev_changed`(새 값 0) | C8-8 「`rev_changed` 꼴 그대로」 |
| B-10 | 새 `data-slot` 이름 | `conv-off-closed`(제안) — 0.3 `conv-outdated` 와 따로(끈 대화 · rev 3 대화가 화면에서 갈린다) | SPEC CP7 「새 `data-slot` 하나」 |
| B-11 | 0.3 기준선을 언제 | **WP-0 — 코드를 고치기 전**(지금 HEAD 로 · 허브 18105 읽기 · Jev 실물) | `runs/now-rows.jsonl` 에 C74 ~ C78 이 없다 · 0.3 코드는 고친 뒤 없다 |
| B-12 | thinking 칸 | WP-0 이 읽은 칸을 `usage.thinking_tokens` 로 · 못 읽으면 `null` + `thinking_seen`(0.3 의 꼴)로 | UC3 의 끝 조건이 그 칸이다 |
| B-13 | 0.4 이해 호출에 쓰는 허브 | 단위 시험 = 가짜 · WP-0 = 18105(0.7.2 · 읽기만) · WP-12 = 18107(0.8.1) | 목록 꼴은 두 판이 `request.abbr` 칸 하나만 다르다(SPEC-001 0.8.1) |

### 17-3. 되적기 후보(코디)

- SPEC-008: §3-4 감쌈 이름(B-1) · §7 `headers` 키 둘 · `marks` 글자(B-4) · CP7 막힘 코드 값 `rev_changed`(B-9) · `data-slot` 이름(B-10) · `filter_sites` 지움 · `turn_kind.judge` · `EXTRA` 지움 · 0.3 기준선 실행(B-11).
- SPEC-006: TK · TW · FD1 · W-1 · W-3(SPEC-008 §5 표대로 — 「달리 받는 곳」).

## 18. SPEC-008 절 ↔ WP 대응(미대응 0)

| SPEC-008 | 규칙 | WP |
|---|---|---|
| §1-3 | CP1 · CP7 | WP-10 |
| | CP2 · CP3 | WP-6 · WP-7 · §4 · §16-3 2 |
| | CP4 · CP5 · CP6 | 범위 밖 · 0.3 그대로(WP-7 AN) |
| §2-1 | LD1 ~ LD8 | WP-1 |
| §2-2 | UC1 ~ UC10 · 출력 필드 | WP-2 · UC3 = WP-0 · UC10 = WP-7 |
| §2-3 | VF1 ~ VF12 | WP-3 · VF8 ⓒ = WP-4 |
| §2-4 | OU1 ~ OU12 | WP-4 · OU5 = WP-5 · OU10 = WP-7 |
| §2-5 (가) | QS1 ~ QS6 | WP-5 |
| §2-5 (나) | QM1 ~ QM5 | WP-6 |
| §2-6 | DT1 ~ DT5 | WP-7 |
| §2-7 | BQ1 ~ BQ5 | WP-7 |
| §2-8 | AN1 ~ AN3 | WP-6(B-2) · WP-7 · WP-8 |
| §3-0 ~ §3-3 | KS1 ~ KS8 · DP8-1 ~ DP8-6 · VP8-1 ~ VP8-4 | WP-6 |
| §3-4 | 함수 서명 표 · 감쌈 | WP-6(B-1 · B-3) |
| §4-1 | FL1 ~ FL6 | WP-7 · FL4 = WP-2 |
| §4-2 | 설정 아홉 · 안 읽는 설정 | WP-10 |
| §5 | AR-1 ~ AR-12 | AR-1 · 2 · 3 · 8 · 9 = WP-3 · WP-7(§4 지움) · AR-4 = WP-4 · WP-5 · AR-5 = WP-7 · AR-6 · 7 · 10 = WP-4 · AR-11 = WP-5 · AR-12 = WP-7 |
| §5 「달리 받는 곳」 | SPEC-004 · 005 · 006 | 각 WP · §15-4 |
| §6-1 · §6-2 · §6-3 | 장부 · 패널 · SSE | WP-8 |
| §7 | `pick` · 적재기 계약 | WP-9 |
| §8-1 | E8-0 | WP-0 |
| | E8-pre | WP-11 |
| | E8-1 ~ E8-4 · E8-5 표 | WP-12 · E8-2 = WP-9 |
| §8-2 | E8-6a · E8-6b | WP-12(0.3 쪽 = WP-0) |
| | E8-7 | 코디 · 사용자(§16-2) — 워커는 18224 사전 확인 |
| §8-3 | S8-T1 | WP-1 |
| | S8-T2 · T3 | WP-2 |
| | S8-T4 · T5 | WP-3 |
| | S8-T6 · T7 · T8(객체) | WP-4 |
| | S8-T8(조회) · T13 · T16 | WP-5 |
| | S8-T9 · T10 · T11 | WP-6 |
| | S8-T12 · T14 · T15 | WP-7 |
| | S8-T17 | WP-8 · WP-10 |
| | S8-T18 | WP-6 · WP-7 · §16-3 2 |
| | S8-T19 | WP-10 |
| | S8-T20 | WP-9 |
| §9 | U8-1 ~ U8-4 · C8-1 ~ C8-9 · O8-1 ~ O8-5 | §3 · §17 |

## 19. 순서 · 의존

| WP | 앞선 것 | 허브 | 도는 시험 파일(이것만) |
|---|---|---|---|
| WP-0 | — | 18105 읽기(0-2 · 0-4) | `test_v04_start.py` |
| WP-1 | WP-0 | 가짜 | `test_v04_list.py` |
| WP-2 | WP-0 · WP-1 | 가짜 | `test_v04_understand.py` |
| WP-3 | WP-1 | 가짜 | `test_v04_verify.py` · `test_v03_turn_kind.py` |
| WP-4 | WP-3 | 가짜 | `test_v04_object.py` · `test_state_object.py` · `test_state_carry.py` · `test_v03_fixes.py` |
| WP-5 | WP-4 | 가짜 | `test_v04_plan.py` · `test_state_plan.py` · `test_state_list.py` |
| WP-6 | WP-3 | 가짜 | `test_v04_material.py` · `test_walk_front.py` · `test_walk_core.py` · `test_walk_material.py` · `test_columns.py` |
| WP-7 | WP-2 ~ WP-6 · WP-9(적재기) | 가짜 | `test_v04_turn.py` · `test_consult_turn.py` · `test_state_examples.py` · `test_state_blanks.py` · `test_consult_sites.py` · `test_v03_sites.py` · `test_v03_turn_kind.py` · `test_consult_carry.py` |
| WP-8 | WP-7 | 가짜 | `test_v04_ledger.py` · `test_consult_ledger.py` · `test_v03_frame.py` |
| WP-9 | WP-0 | 무관 | `test_v04_prompt.py` · `test_consult_prompt.py` · `test_v03_prompt.py` · `test_state_blanks.py` |
| WP-10 | WP-8 | 무관 | `test_v04_state_gate.py` · `test_v03_start.py` · `test_v03_fixes.py` · `test_v03_frame.py` · `test_consult_ledger.py` · `test_consult_page.py` |
| WP-11 | WP-8(장부 칸) | 무관 | 스크립트 끝 조건 ①(옛 장부 수 같음) |
| WP-12 | 전부 · WORK-016 WP-4 | **18107** | 실물 — 시험 아님(§16-1) · 끝 조건 ② 는 첫 표 실행에서 |

- **직렬**(한 워커 · 같은 워크트리). WP-9 의 적재기(`pick` · `state_ready`)는 WP-7 앞에 끝나야 켠 대화가 선다 — WP-9 를 WP-3 뒤 · WP-7 앞 아무 때나.
- 허브 WORK-016 과는 병행 — 앱은 WP-12 에서만 18107 을 본다.

## 변경 기록

### 0.1.0 (2026-11-18) — 처음 씀

- SPEC-008 0.2.0 전부를 WP-0 ~ WP-12 로(대응표 §18 — 미대응 0).
- 코디 답 반영: U8-3 빈칸 · U8-4 ⓐ 90% · ⓑ ⓒ 100% · C8-8 `rev_changed` 꼴 · C8-9 `columns/` 밑줄 함수 import(감쌈은 필요할 때만 — B-3).
- 지울 곳 grep 전수(§4): 켠 가지에서 Jev · resolve 맞춤 꼴에 닿는 부름 자리 **6** · 띄우고 읽는 자리 포함 **27 행**(지움 14 · 고침 · 바꿈 · 그대로 11 · 남김 2) + `filter_sites` 1.
- 바뀌는 기존 시험(§15-4 — 예상): 지움 20 · 고침 약 30 · 「안 고침」 목록.
- 이 워커가 본 것: `llm/cli.py:11-12` 에 추론 끄는 꼴(`--settings {"alwaysThinkingEnabled": false}` + `MAX_THINKING_TOKENS=0`)이 이미 있다 → E8-0 첫 후보 · `consult_fixture` 가 `chat_state` 를 주지 않아 `test_consult_turn.py` 11 이 기본값 변경으로 켠 가지로 돈다 · `runs/now-rows.jsonl` 에 C74 ~ C78 이 없어 0.3 기준선을 WP-0 에서 고치기 전에 돌린다(B-11) · `score.py` 가 조사 산출물을 덮어쓴다(B-6).
- 이 워커는 서버 · DB · LLM · Jev · 허브를 부르지 않았고 코드 · 데이터를 고치지 않았다(읽기만).
