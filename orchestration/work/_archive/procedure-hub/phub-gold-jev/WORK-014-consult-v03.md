---
type: work
id: WORK-014
title: "앱 상담 채팅 0.3 구현 계획 — 턴 종류 가르기 · 상담 말투(`system_v3`) · 끝맺음 하나 · 없음은 없다고 · 리스트(계열 → 시술 · 내려온 묶음) · 얼굴 점 누적과 누르기 · 화면 네 칸(드로어 · 객체 패널) · 부위 없는 고민 + 부위(SP) · 실물 E6-0 ~ E6-6"
status: draft
product: procedure-hub
feature: phub-gold-jev
version: 0.1.0
created_at: 2026-11-17
updated_at: 2026-11-17
tags:
  - product/procedure-hub
  - feature/phub-gold-jev
  - doc/work
  - status/draft
links:
  specs:
    - "orchestration/work/phub-gold-jev/SPEC-006-consult-v03.md (0.1.0 · 검수 PASS — FAIL 0 · WARN 12 · NOTE 9 · review-spec-006.md) ← 계약"
    - "orchestration/work/phub-gold-jev/SPEC-001-hub-gold-mcp.md (0.7.1 — §4-1 `matched.how` · §4-5 `descended[]` · `sites[]` · `site_mode` · `site_applied` · `site_prefer` · `n_site_prefer` · §5-11 DP · CS · NM · SP)"
    - "orchestration/work/phub-gold-jev/SPEC-004-consult-chat.md · SPEC-005-consult-state.md (0.1.0 — 이 판이 얹는 계약 · 고치지 않는다)"
  decisions:
    - "orchestration/work/phub-gold-jev/_RESUME.md §2 (2026-11-17 「순차 진행 · 시험은 구현한 것만 돌림」 · 「SPEC-006 W-9 = (a) · W-10 = ○○ 계열 시술」 · 「SPEC-006 검수 뒤 코디 값 W-1 ~ W-8 · W-11 · W-12」 · 「SPEC-006 U6-1~3 = (a) · U6-4 보류 · ① 규칙(사용자 결정)」 · 「A8 화면 구조 · U7-1~3 = (a)」 · 「얼굴 점 = 대화에서 나온 고민 부위 …」 · 「Procedure Hub 데이터는 공개 정보」)"
    - "orchestration/work/phub-gold-jev/work-chat-v03-instructions.md (이 문서의 지시서)"
  related:
    - "orchestration/work/phub-gold-jev/review-spec-006.md (WARN 12 · NOTE 9 — 이 문서 §16)"
    - "orchestration/work/phub-gold-jev/review-spec-001-v071.md (N-4 — 표지 0 일 때 화면 · 이 문서 §12)"
    - "orchestration/work/phub-gold-jev/WORK-012-consult-state.md (0.2 계획 — 공통 규칙의 꼴)"
    - "orchestration/work/phub-gold-jev/WORK-013-hub-v07.md (허브 0.7.1 구현 계획 — 다른 writer 가 같은 때에 쓴다 · 이 문서는 읽지 않았다)"
---

# WORK-014 — 앱 상담 채팅 0.3 구현 계획

> 경로 접두어: `W` = 이 폴더 · `APP-WT` = clinic_chat 워크트리 `phub-gold-jev`(HEAD `68a31b1` = 0.1 + 수정 1 + 0.2 · 작업 트리 깨끗함 — 11-17 확인). 아래 앱 경로는 전부 `APP-WT` 기준이다.
> **계약은 SPEC-006 0.1.0 이다.** 이 문서는 「어느 파일을 · 어떤 순서로 · 무엇으로 확인하나」 만 정한다. SPEC 과 달리 받는 곳은 §3 의 결정 행(U6 · 코디 W · 규칙 ①)과 §17 B 표에 적은 것뿐이다. 그 밖에 SPEC 과 어긋나는 것을 만나면 코드를 맞춰 고치지 말고 보고한다.
> **화면 문구 · 답 문구를 짓지 않는다**(SPEC-004 ST4 · SPEC-006 SV10). 프롬프트 절은 SPEC §3-2 의 「담을 뜻」 을 옮긴 **초안**이고 확정은 사용자다(U6-2 (a) — 초안대로 구현 뒤 e2e).
> **시험은 구현한 것만 돈다**(사용자 11-17) — WP 마다 「그 WP 시험 파일만 돌림 · 전체 pytest 금지 · 돌린 파일 목록 보고」(§2).
> Procedure Hub 데이터(코드 · 이름 · 행 수) · medikit 은 공개 정보다. 비밀값 · 키 · 내부 주소는 그대로 금지.

## 0. 요약

- 0.3 은 **켠 상태의 판을 통째로 바꾼다**(`consult_rev` = 3). 끈 상태 = 0.1 그대로. 0.2 로 시작한 켠 대화는 0.3 서버에서 끝난 대화다(FX4 — 0.2 길을 코드에 남기지 않는다).
- 새 모듈 다섯(`consult/turn_kind.py` · `close.py` · `voice.py` · `drawer.py` · `e6.py`) + 0.1 · 0.2 모듈의 고치는 곳 + 함께 쓰는 코드 `walk/front.py` · `columns/col_b.py` 의 **선택 인자 둘**(`entry_pick` · `abbr_yes_only` — 안 주면 지금과 글자 그대로 · §8).
- WP 열(SPEC C6-11 순서): **WP-0** 시작 확인 · 설정 여섯 · `consult_rev` → **WP-1** 화면 네 칸 · 드로어 · 객체 패널 → **WP-2** `system_v3` · 「앱 판정」 칸 · 금지 낱말 검사 → **WP-3** 턴 종류 · 걷기 순서 · 함께 쓰는 코드 → **WP-4** `close` · `empty` · 꼬리 → **WP-5** 객체 구멍 · 옛 대화 → **WP-6** 리스트 · 요약 줄 · 내려온 묶음 · **SP** → **WP-7** 점 누적 · 누르기 · `viewing` → **WP-8** 실물 E6-0 ~ E6-5 · README → **코디** 18105 재시작 · 18222 · 사용자 E6-6.
- **허브는 고치지 않는다.** 0.7.1 칸(§4)은 가짜 허브로 짓고 시험한다. 실물은 **18105 가 0.7.1 로 다시 뜨기 전에는 0.7.1 칸 없이 도는 꼴**(점 0 · 내려온 묶음 0 · `site_applied` 없음)이다 — 그 전 실물은 A1 ~ A4 기대만 본다(§14).
- **얼굴 SVG · `face_coords.py` 는 고치지 않는다**(D6-9 · FD9).
- **U6-4(부위 없는 고민의 누를 자리 — FD8 칩)는 보류다** — 짓지 않는다. S6-T20 은 이 판에 없다(§17 O-1).

## 1. 지금 코드(11-17 확인 — `APP-WT` HEAD `68a31b1`)

| 파일(줄 수) | 지금(0.2) | 0.3 에서 |
|---|---|---|
| `clinic_chat/consult/turn.py`(408) | `run_turn`(`:76`) — 든 후보(`:103`) → `Consult.begin`(`:104`) → `asyncio.gather(walk, cs.retract())`(`:109`) → `after_walk`(`:126`) → `message`(`:127`) → `screen`(`:142`) → LLM(`:165`) → 꼬리(`:171`) → `done`(`:179`) → 맺는 줄(`:189-207`) · `class Consult`(`:210`) | 가르기를 걷기와 함께(§5) · `talk` 가지 · 둘째 걷기 · `close` · `empty` · `state` 이벤트 · `viewing` |
| `clinic_chat/consult/state.py`(281) | `SLOT_OF`(`:24`) · `HOWS`(`:32`) · `observe`(`:81`) · `_again`(`:118-122` — 다시 나오면 늘 `confirmed`) · `update`(`:125`) · `_focus`(`:189`) · `retract`(`:250` — `resolve` + `ask_nouls`) | FX1(`_again`) · 줄임 후보는 yes 만(TW8) · `viewing` 으로 `focus` 옮기기(FD6) · 거둠 요청에 가르기 셋을 함께 |
| `clinic_chat/consult/ledger.py`(199) | `Conv`(`:36`) · `rows()`(`:86-98` — 파일 통째 파싱) · `get`(`:107`) · `start`(`:132`) · `_apply_end`(`:152`) · `state_at_start`(`:182`) · `blocked`(`:191`) · `END_KINDS`(`:28`) | 시작 줄 `consult_rev` · 메모리 색인(W-11) · `blocked` 에 `rev_changed` |
| `clinic_chat/consult/carry.py`(57) | `candidates`(`:15` — 장부 가까운 턴 `targets[]`) · `with_options`(`:34`) | 객체 기준으로 거르기(TW7 · W-3) · 앞 대상 `origin` = `follow`(TW4 · TW6) |
| `clinic_chat/consult/material.py`(270) | `summaries`(`:71`) · `judgement_of`(`:211`) · `add_summaries`(`:222`) · `consult_view`(`:246`) · `message`(`:256`) | 켠 상태 요약 줄에서 `reach` · `concern_match` 뺌 + `modality_level`(LS6) · 「앱 판정」 칸 더하고 빼기(§3-3) |
| `clinic_chat/consult/listing.py`(140) | `build_list`(`:19` — `groups` · `modality_only` · `unreached`) · `state_list`(`:98`) · `list_codes`(`:130`) | `descended[]` 계열 묶음(LS4 · LS4-1) · `hidden` · SP 표지 · 순서(§12) |
| `clinic_chat/consult/sites.py`(69) | `SITES_FIELD = "concern_sites"`(`:14` 임시 이름) · `PAIR_KEYS`(`:15`) · `from_response`(`:18`) · `place`(`:44`) | `SITES_FIELD` = `sites` 한 줄 · `match` 칸 · 점마다 `concern_codes[]` · `focus`(FD1 · FD2) |
| `clinic_chat/consult/plan.py`(235) | `qy1_calls`(`:87-95` — 부위 거르개가 있으면 `site` 를 건다) · `concern_sites_of`(`:161`) · `run`(`:175`) · `derive`(`:206`) | `concern_sites[]` 를 고민 전부로 · `site_applied` 를 읽어 넘김(§12) |
| `clinic_chat/consult/blanks.py`(121) | `SAFETY_KINDS`(`:17`) · `count`(`:35`) · `pick`(`:89`) · `record`(`:116`) | CS7(BK5 줄임) · `said` = 0 이면 `record` 안 함(CS5 · W-8) |
| `clinic_chat/consult/prompt.py`(157) | `SECTION_IDS`(`:19`) · `STATE_SECTION_IDS`(`:24`) · `JEV_STATE_KEYS`(`:26`) · `state_ready`(`:51`) · `parse`(`:63`) | `system_v3` 열세 절 · `jev_state.turn_kind` · `kind_labels` · `voice_check` · `turn_headers.close` · `prev` · `slots`(§9) |
| `clinic_chat/consult/tail.py`(60) | `TAIL_LINE`(`:10`) · `split_tail`(`:13`) · `TailFilter`(`:34`) | 꼬리의 `close: <n>` 한 줄(CS5) |
| `clinic_chat/consult/server.py`(165) | 라우트 다섯 + 정적(`GET /` `:108` · `GET /c/{conv_id}` `:114` · `POST …/turns` `:118` · `GET …/events` `:142` · `GET /face-check` `:150`) · `page`(`:87`) | `GET /convs` · `GET /c/{conv_id}/list` · `POST` 폼의 `viewing` · 옛 대화 표지 |
| `clinic_chat/consult/render.py`(68) · `steps.py`(46) | 조각 그리기 · 단계 넷 | 새 조각(드로어 · 객체 패널) · `talk` 턴은 `understand` → `answer`(TT5) |
| `consult/templates/partials/main.html` · `list.html` · `sites.html` · `turn.html` | 두 칸(`cs-left` · `cs-chat`) · `reach` · `concern_match` 배지 · 「계열 층만」 · 「그 밖」 묶음 · 점에 `data-site-code` 만 · 이벤트 자리 여섯 | 네 칸 · 배지 · 두 묶음 안 그림 · 점 · 라벨 누르기 · `state` 자리 |
| `consult/static/consult.js`(96) · `consult.css` | 이벤트 위임 · `data-*` 만 | 드로어 접기 · 펴기 · 목록 다시 받기 · `viewing` 싣고 비우기 · 누른 점 표시(인라인 스크립트 0) |
| `clinic_chat/walk/front.py`(440) | `front(…, carry, instr)`(`:202`) · 든 후보 판정(`:268-279` — yes 만) · 든 후보만 yes(`:281`) · 입구 고르기(`:284-306`) · 글에 든 이름 판정(`:337-360` — `target` · `dropped` · `uncertain_kept` · `named`) | 선택 인자 둘 + `origin` = `follow` 가지(§8) |
| `clinic_chat/columns/col_b.py` | `walk(question, d, *, read_kinds, carry, instr)`(`:161`) → `front(…)`(`:169`) | 두 인자를 `front` 로 넘기는 줄만 |
| `clinic_chat/walk/jev_requests.py`(101) | `ask_nouls`(`:37` — `extra` 는 묶음이 여럿이면 가장 낮은 값) · `_target_instr`(`:64`) | **안 고친다**(부르기만 — §8 N-3) |
| `clinic_chat/walk/calls.py` · `walk/material.py` | 걷기의 고민 + 부위 조회(`calls.py:259-264`) · `site_match` 표지(`material.py:115-117` — `site_match[]` 가 있는 행에만) | **안 고친다** — 확인 시험 한 꼴(§12 SP-T4) |
| `clinic_chat/config.py`(152) | `jev_noul_yes_at`(`:51`) · `chat_*`(`:69-85`) | 칸 여섯(§6) |
| `prompts/consult.json`(125) | `version` `0.1.0-draft` · `system` 다섯 · `system_state` 셋 · `jev_front` 다섯 · `jev_state.retract` · `turn_headers` 다섯 · `steps` | 키를 **더한다**(`system[]` 글자는 안 바꾼다 — 끈 상태 sha 유지) |
| `tests/` | `test_consult_*.py` 열(0.1 · 수정 1) · `test_state_*.py` 일곱(0.2) · `test_walk_*.py` · `state_fixture.py` · `fake_hub.py` · `fake_jev.py` · `fake_cli/` | 새 `tests/test_v03_*.py` · `v03_fixture.py` · 가짜는 더하기만 · `test_state_*.py` 는 달리 받는 시험만 고침(§15) |

기준선은 재지 않는다 — 전체 pytest 를 돌리지 않는다(§2). WP-0 은 줄 번호만 다시 확인한다.

## 2. 공통

| 항목 | 이번 판 |
|---|---|
| 시작 조건 | 코디 발주. 앱 작업 트리(`68a31b1` · 깨끗함) 위에 이어 짓는다. 허브 0.7.1 구현(WORK-013)과 **병행한다** — WP-0 ~ WP-7 은 가짜 허브만 쓴다 |
| allowed_paths(앱) | 새로: `clinic_chat/consult/{turn_kind,close,voice,drawer,e6}.py` · `consult/e6_inputs.json` · `consult/templates/partials/{drawer,drawer_list,state,state_turn}.html` · `tests/test_v03_*.py` · `tests/v03_fixture.py`. 고침: `consult/{turn,state,ledger,carry,material,listing,sites,plan,blanks,synergy,prompt,tail,render,server,steps,probe}.py` · `consult/templates/{page.html,partials/main.html,partials/list.html,partials/list_interest.html,partials/list_synergy.html,partials/sites.html,partials/turn.html}` · `consult/static/{consult.js,consult.css}`(`--ms-*` 토큰만) · `clinic_chat/config.py`(칸 더하기만) · `clinic_chat/walk/front.py` · `clinic_chat/columns/col_b.py`(§8 의 줄만) · `prompts/consult.json` · `.env.example`(이름만) · `README.md`(상담 절) · `tests/{fake_hub,fake_jev,consult_fixture,state_fixture}.py`(더하기만) · `tests/test_state_*.py`(§15 의 달리 받는 시험만) |
| **고치지 않는 것** | **`consult/templates/_face.svg` · `consult/face_coords.py`** · `clinic_chat/web/**` · `llm/**` · `columns/**`(`col_b.py` 의 §8 줄 빼고) · `walk/**`(`front.py` 의 §8 줄 빼고 — `jev_requests.py` · `calls.py` · `material.py` · `gate.py` · `breadth.py` · `entry.py` 포함) · `prompts/*.md` · `prompts/jev/*.md` · `consult.json` 의 `system[]` · `steps` 글자 · **0.1 · 수정 1 의 시험 파일**(`tests/test_consult_*.py` · `tests/test_walk_*.py` · 그 밖 `tests/test_*.py`) |
| allowed_paths(허브) | **없음** — 읽기만 |
| 포트 | **워커 18223**(차 있으면 빈 포트를 찾아 쓴다) — 띄워 확인한 뒤 스스로 내린다 · **18222 는 코디**(사용자 e2e) · **18105(허브)는 HTTP 읽기만** — 띄우기 · 내리기 · 다시 띄우기 금지. **허브 0.7.1 구현 뒤 코디가 18105 를 다시 띄운다** · 그 밖의 포트는 건드리지 않는다 |
| 외부 호출 | 단위 시험은 전부 가짜(CLI · 허브 · Jev). 실물은 WP-8 뿐(허브 읽기 · Jev · 구독 CLI). 환경 파일을 열거나 고치지 않는다(없으면 「못 돌림」 → 코디). 키는 env 이름만 |
| 문구 | 새 템플릿 조각 · `consult/` 새 코드에 사람에게 보일 문장 0(`data-slot` 자리만 — S6-T23). 예외: 실측 입력 글(`consult/e6_inputs.json`) · 시험 자료 · `prompts/consult.json`(프롬프트 초안 · 정해진 문구 값 — §9) |
| **시험** | **WP 마다 「그 WP 시험 파일만 돌림 · 전체 pytest 금지 · 돌린 파일 목록 보고」**(사용자 11-17 — `_RESUME` §2 맨 위 행). 도는 것 = ① 그 WP 의 새 파일 `tests/test_v03_<이 WP>.py` ② 그 WP 가 **고친 모듈의 기존 시험 파일**(WP 절에 이름을 박았다) — 그 둘뿐. `uv run pytest -q` 를 인자 없이 부르지 않는다. 보고에 「돌린 파일 · 통과 수 · 고친 기존 시험」 을 WP 마다 적는다. `uv run ruff check <고친 경로들>` 도 고친 파일만 |
| 커밋 | 워커는 커밋 · push · PR 을 하지 않는다(코디 몫) |

## 3. 정해진 값(`_RESUME` §2 11-17 행 그대로)

### 3-1. 사용자 결정

| # | 결정 | 이 문서 |
|---|---|---|
| U6-1 | **(a)** 턴 종류는 Jev Noul 셋 — 걷기와 함께 · 거둠 요청에 실음 | §7 WP-3 |
| U6-2 | **(a)** 말투 초안대로 구현하고 e2e 에서 고친다 — 층은 주인 이름으로 · 「원장 진술」 표기는 화면에서 뺌 | §9 WP-2 |
| U6-3 | **(a)** 점을 누른 고민이 다음 턴의 `focus` | §13 WP-7 |
| **U6-4** | **보류 — 열린 것**(부위 없는 고민의 누를 자리 · FD8 칩). 짓지 않는다 | §17 O-1 |
| W-9 | **(a)** 직접 닿은 시술이 있는 계열은 그 시술만 · 없는 계열만 내려온 시술 전부(LS4-1 그대로) | §12 |
| W-10 | 내려온 묶음 머리 문구 = **「○○ 계열 시술」**(빈 자리 `mark-modality-level` 의 값 — 초안 확정 · ○○ = 계열 이름) | §12 |
| A8 | 화면 = [드로어(기본 열림 · 새 대화 · 지난 대화 목록) \| 얼굴 + 점(위) · 시술 리스트(아래) \| 채팅 \| 상담 객체 패널(개발용 · env)] | §6a WP-1 |
| 규칙 ① | 부위가 묶이지 않은 고민 + 부위 = **부위로 거르지 않는다** — 그 고민의 시술 전부 + 그 부위 행은 「우선 표시」 표지로 앞에 · 부위가 묶인 고민은 HG3 그대로 | §12 SP |
| 시험 | 시험은 구현한 것만 · 전체 안 돌림 | §2 |

### 3-2. SPEC-006 검수 뒤 코디 값(한 줄씩)

| # | 코디가 정한 것 | 이 문서 |
|---|---|---|
| **W-1** | 하위 고민 부위의 점 = **객체 고민의 하위면 누를 수 있다**(그 하위 고민으로 `viewing`) | §13 FD4 · FD7 |
| **W-2** | `viewing` 은 **누른 다음 한 턴만** · 같은 턴 글의 새 고민이 `viewing` 보다 앞 · 한 점에 고민 여럿이면 객체에서 **가장 최근 고민** | §13 FD6 |
| **W-3** | 객체에 안 드는 표(`package` · `adverse` · `condition` · `anatomy` · `offer`)가 앞 대상이면 **0.1 CR1 대로** 앞 턴 대상을 든 후보로(끊김 없음) | §7 TW6 · TW7 |
| **W-4** | 줄임 판정(TW8)은 **상담 쪽 선택 인자로만**(시험 앱 B 열 무변경) | §8 |
| **W-5** | 안전 종류(부작용 · 금기 · 회피) 0 행은 「없어요」 금지 → **「확인된 정보가 없어요」 꼴**(없다 · 안전하다로 말하지 않음) | §10 EM1 · §9 절 `empty` · `safety` |
| W-6 | `talk` 턴 기대 = 「**객체 조회(QY) 0 · 깊이 읽기 0** · 허브는 `resolve` 뿐」(「허브 조회 0」 이 아니다) | §7 S6-T2 · §14 |
| W-7 | `talk` 턴의 앞 `ask` 선택지 값은 **버린 걷기의 `front` 가 낸 값**(`option_from` 항목)을 쓴다 — 요청 추가 0 | §7 TT1 |
| W-8 | `close.said` = 0 이면 `asked[]` 에 안 적는다(걸린 선택지 · NQ5 에도 없는 턴) · `null`(꼬리에 줄 없음)은 센다 | §10 CS5 |
| W-11 | 드로어 목록은 **서버가 뜰 때 한 번 훑은 메모리 색인**으로 — 줄을 쓸 때 함께 고친다(목록을 그릴 때 장부를 다시 읽지 않는다) | §6a SV3 · SV6 |
| W-12 | 수 · 기대 고침: ① `80581…` 턴 2 「볼」 = **0.59**(`uncertain_kept`) ② `asked_concern_code` 로 센 행 = `CON-168` **1** · `CON-169` **2** · `CON-181` **39** · `CON-024` **10** · `CON-137` **9** ③ 실물 턴 수 = **12(첫 턴 빼고 9)** ④ ① 턴 6 기대 = `ask` null → `close.by` = `offered`(안전 빼고) 또는 `null`(BK2 아님) ⑤ S6-T24 는 「달리 받는 S5 시험 목록」 과 함께(§15) | §14 · §15 |

## 4. SPEC-001 0.7.1 칸 — 앱이 읽는 곳(이름은 그 문서 그대로)

| 칸(SPEC-001 0.7.1) | 어디 | 앱이 읽는 곳 | 없을 때(허브 0.6) |
|---|---|---|---|
| `descended[]{modality_code, modality_name, unit, procedures[]{procedure_code, procedure_name, scope_gid, in_groups}, from[]{gid, reach, lands, path[], procedure_codes[]}}` | `concern_candidates` 응답 · §4-5 · DP | `consult/listing.py`(§12 LS4 · LS4-1) — `from[].path[]` · `procedure_codes[]` 는 그리지 않는다(장부에 `from_gids[]` 만) | 묶음 0 — 0.2 꼴 리스트 |
| `counts.descended.undescended` | 같음 · DP9 | 장부 `list.hidden` | 없음 |
| `sites[]{site_code, site_name, concern_code, csi_id, match}`(`match` = `직접` · `하위`) | 같음 · CS | `consult/sites.py` 의 `SITES_FIELD` 한 줄 · `consult/plan.py` `concern_sites_of` | 점 0 · 라벨 0(오류 없음 — 0.1 그대로) |
| `matched.how` = `줄임` | `resolve` 후보 · §4-1 · NM | `walk/front.py`(선택 인자 `abbr_yes_only` 일 때만 — §8) · `consult/state.py` `observe` | 칸 없음 = 줄임 후보 0 |
| 입력 `site_mode`(`auto` · `filter`) | `concern_candidates` 요청 · SP7 | **안 보낸다**(기본 `auto` — 걷기 · 답 키와 같은 기본값) | — |
| 머리 `site_applied`(`null` · `filter` · `prefer`) | 응답 머리 · SP1 | `consult/plan.py` → `consult/listing.py`(§12) · 장부 `list.site.applied` | `None` = 0.2 동작(거른 응답 그대로) |
| 행 `site_prefer`(`true` · `false`) + `site_match[]` | `groups[].rows[]` · `modality_only[]` · `unreached[]` · SP3 | `consult/listing.py` — 시술 · 계열 묶음의 표지 | 없음 |
| 묶음 `groups[].n_site_prefer` | 묶음 · SP3 | `consult/listing.py` — 그 시술이 표지 행을 가졌나(> 0) | 없음 |
| `counts.site_prefer{rows, groups}` | 머리 · SP3 | 장부 `list.site{prefer_rows, prefer_groups}` · 표지 0 판정(§12 SP5) | `null` |

- 칸 이름이 구현 때 바뀌면(SPEC-001 O-27 · O-29 · O-30 「구현 때 정함」) 앱은 그 칸을 읽는 **한 곳씩**만 맞춘다(SPEC-006 O6-9). 가짜 허브(`tests/fake_hub.py`)의 응답 꼴은 위 표와 SPEC-001 부록 A 로 짓는다.
- 「고민당 최대 시술」 은 **107**(SPEC-001 0.7.1 — SPEC-006 LS4-1 의 130 은 0.7.0 값이다). 규칙은 같다.

## 5. 한 턴 루프 — `turn.py`(켠 상태 rev 3)

| 순서 | 무엇 | 자리 |
|---|---|---|
| L0 | `POST` 의 폼 값 `viewing` 을 받아 턴에 싣는다(FD6) | `server.py` `post_turn` → `run_turn(…, viewing=)` |
| L1 | 든 후보 — 객체 기준으로 거른 것 + 걸린 선택지(TW7 · W-3) | `carry.py` |
| L2 | **첫 턴** = 가르지 않고 `new`(TK2) — 걷기는 지금과 같다(`entry_pick` 기본값). **둘째 턴부터** = 걷기(`entry_pick=False` · `abbr_yes_only=True`)와 **가르기 요청**(거둠 + `tk_new` · `tk_talk` · `tk_follow`)을 함께 띄운다(TW1 · TK3) | `turn.py:109` 의 `gather` 자리 |
| L3 | 판정(TK5 · TK6 · TT6) → `new` · `follow` · `talk` | `consult/turn_kind.py` |
| L3a | `talk` → 걷기 결과를 버린다(TW3). `follow` · 첫 걷기가 「입구 없음」 → 앞 대상을 `origin` = `follow` 로 실어 한 번 더(TW4). `new` · 「입구 없음」 → `entry_pick=True` 로 한 번 더(TW5) | `turn.py` |
| L4 | 객체 갱신 — `talk` 는 걷기 없이(TT1) · `viewing` 으로 `focus` 옮기기(FD6) · FX1 | `state.py` |
| L5 | 객체 기준 조회 · 시너지(0.2 그대로 — `talk` 는 객체가 바뀐 때만 · TT2) | `plan.py` · `synergy.py` |
| L6 | `list` · `sites`(합집합이 바뀐 턴 · `focus` 가 바뀐 턴 — FD3) | `Consult.screen` |
| L7 | 빈 칸 · `ask`(CS7) → `empty[]` → `close`(CS2) | `blanks.py` · `close.py` |
| L8 | 메시지(「앱 판정」 rev 3 칸) → LLM(`system_v3`) | `material.py` |
| L9 | 꼬리(`close:` 줄) → 금지 낱말 검사 → 장부 `consult.*` → **`state` 이벤트 → `done`**(SV8) | `tail.py` · `voice.py` · `turn.py` |

- 단계 표시: 둘째 턴부터는 **판정이 나기 전에 `search` 단계를 켜지 않는다** — 함께 띄운 걷기의 단계 신호(`hub` · `depth` · `gate`)를 판정까지 붙들었다가 `talk` 면 버리고(`understand` → `answer` 둘만 — TT5), 아니면 그때 흘린다(검수 N-4).
- `CHAT_TURN_KIND=off` 면 L2 ~ L3a 가 없다 — 모든 턴 `new` · 걷기는 기본 인자(0.2 와 같은 호출 순서 · S6-T5).

## 6. WP-0 — 시작 확인 · 설정 · `consult_rev`

**SPEC**: §10-2 · FX3(시작 줄 칸) · C6-10.

| 무엇 | 구현 |
|---|---|
| 시작 확인 | `git status --porcelain` 이 비어 있는지 · HEAD 가 `68a31b1` 인지 보고 **§1 표의 줄 번호를 다시 확인**해 다른 곳을 보고에 적는다. `_face.svg` · `face_coords.py` 의 sha 를 떠 둔다(끝에 「변경 0」 대조) |
| 설정 칸 여섯 | `config.py` 에: `CHAT_TURN_KIND`(`on`) · `CHAT_TALK_MAX`(`3`) · `CHAT_ALT_MAX`(`3`) · `CHAT_VOICE_CHECK`(`on`) · `CHAT_DEBUG_PANEL`(`off`) · `CHAT_DRAWER_MAX`(`50`) — SPEC §10-2 그대로(검수 N-7: 넷이 아니라 여섯) · `.env.example` 에 이름만 |
| `consult_rev` | 켠 대화의 시작 줄에 `consult_rev: 3`(`ledger.py` `start` — 첫 턴에 정하고 그 대화는 끝까지) · `Conv.consult_rev` · 되읽기(`get`)가 시작 줄에서 세운다(없으면 `None`) |

**완료 조건**: 설정 여섯이 기본값으로 선다 · 켠 새 대화의 시작 줄에 `consult_rev` 가 있다 · 끈 대화의 시작 줄은 0.2 와 같다(칸 없음).
**시험**: `tests/test_v03_start.py`(새) + `tests/test_consult_ledger.py`(기존 · 안 고침) — 이 둘만.

## 6a. WP-1 — 화면 네 칸 · 드로어 · 객체 패널

**SPEC**: §8A SV1 ~ SV11 · §9(라우트 · 이벤트 · 빈 자리 행) · S6-T27 ~ T29 · 검수 W-11 · N-9.

| 규칙 | 구현 |
|---|---|
| SV1 틀 | `partials/main.html` — 왼쪽에 드로어 칸(`#conv-drawer` · 기본 열림) · 오른쪽 끝에 객체 패널 칸(켰을 때만). `cs-left` · `cs-chat` 은 그대로(리스트는 이미 얼굴 아래다). `page.html` 도 같은 틀 |
| SV2 · SV5 드로어 | `partials/drawer.html` — 「새 대화」 = `GET /` 로 가는 링크(지금 길 · 새 `conv_id` · 새 세션 UUID) · 목록 항목 = `/c/<id>` 링크 · 항목에 `data-conv-state`(글 없음) · 지금 대화에 `aria-current`. 문구는 빈 자리(`drawer-new-label` · `drawer-list-title` · `drawer-empty` · `drawer-toggle-label`) |
| SV3 · **W-11** 색인 | `consult/drawer.py` — `Ledger` 가 **뜰 때 장부를 한 번 훑어** 메모리 색인 `{conv_id → first_question, first_asked_at, last_asked_at, n_turns, state}` 를 세우고, `start` · `end` 가 줄을 쓸 때 함께 고친다. 목록 = 마지막 턴 `asked_at` 내림차순 · 앞에서 `CHAT_DRAWER_MAX` 개. **목록을 그릴 때 장부 파일을 다시 읽지 않는다**(S6-T27 에 그 기대) |
| SV3 「턴 0」(N-9) | 시작 줄이 하나도 없는 대화(`GET /` 가 만든 빈 대화)는 목록에 없다. **시작 줄만 있고 맺는 줄이 없는 대화**(턴 도중 죽음)는 첫 질문이 있으므로 목록에 나온다 — `data-conv-state` = `broken`(§17 B-6) |
| SV4 이어 감 | 새 코드 0 — `GET /c/{conv_id}` 가 이미 장부 되읽기 · `--resume` 으로 선다(S6-T28 로 확인만) |
| SV6 `GET /convs` | HTML 조각(`partials/drawer_list.html`) → `#conv-drawer-list`. 화면을 열 때 틀에 함께 그리고, `consult.js` 가 줄기가 닫힐 때(`close` · 오류) 한 번 다시 받는다. 드로어 접기 · 펴기도 `consult.js`(이벤트 위임 · 인라인 스크립트 0) |
| SV7 패널 | `CHAT_DEBUG_PANEL=on` 일 때만 틀에 `#consult-state` 칸 · `turn.html` 에 `state` 받는 자리 · 서버가 `state` 이벤트를 보낸다. `off` 면 칸 · 자리 · 이벤트 0 이고 나머지 이벤트는 같다 |
| SV8 · SV9 내용 | `partials/state_turn.html` — 그 턴 장부 줄의 `consult.after` · `consult.diff` · `consult.blanks` · `consult.ask` · `consult.turn_kind{kind, nouls}` · `consult.close{by, said}` 를 **값 그대로**(칸 이름 = 장부 키). `state` 이벤트 = `#consult-state` 맨 위에 덧붙임(최근 턴이 위) · **`done` 바로 앞**에 보낸다. 화면을 열 때는 장부의 성공 턴들로 다시 그린다(`partials/state.html`). 끈 대화 · 오류 턴은 빈 묶음. WP-1 때는 `turn_kind` · `close` 칸이 아직 없다 — 없는 칸은 안 그리고 WP-3 · WP-4 가 장부에 쓰면 저절로 보인다 |
| SV10 문구 | 패널 · 드로어에 지은 문구 0 — 빈 자리 `state-title` · `state-empty` |
| SV11 | 구현 없음(로컬 한 사람 전제 — README 한 줄) |

**완료 조건**: S6-T27 ~ T29 통과 · 인라인 스크립트 0.
**시험**: `tests/test_v03_frame.py`(새) + `tests/test_consult_page.py` · `tests/test_consult_chat_ui.py`(기존 · 안 고침 — 끈 상태 · 패널 `off` 의 화면이 지금과 같은가) — 이 셋만.

## 7. WP-3 — 턴 종류 · 걷기 순서

(순서는 WP-2 뒤다 — 절 번호는 묶음 순.)

**SPEC**: §2 TK1 ~ TK7 · TW1 ~ TW8 · TT1 ~ TT6 · S6-T1 ~ T7 · T25 · 코디 W-3 · W-4 · W-6 · W-7 · 검수 N-3 · N-4 · N-5.

| 규칙 | 구현 |
|---|---|
| TK1 · TK2 | `consult/turn_kind.py` — 종류 셋(`new` · `follow` · `talk`) · 첫 턴은 요청 0 · `new` |
| TK3 · N-3 | 거둠 요청(`state.py` `retract`)에 `extra` = `tk_new` · `tk_talk` · `tk_follow` 를 실어 **요청 하나**. 객체에 항목이 없어 거둠 항목이 0 이어도 셋은 묻는다. 거둠 항목이 묶음 크기를 넘으면 **첫 묶음에만** 셋을 싣는다(`ask_nouls` 를 첫 묶음 + 나머지로 나눠 부른다 — 함께 쓰는 `ask_nouls` 는 안 고친다) |
| TK4 | Jev state = `question` · `prev{question, answer, targets[이름], ask{slot, options[이름]}, closed_by, empty[]}`(바로 앞 **성공** 턴의 장부 줄) · `consult`(`material.consult_view` — 이름만). 코드 · 줄 번호 0 |
| TK5 · TK6 | 문턱 = `jev_noul_yes_at`(`config.py:51`). ① `tk_new` ≥ yes → `new` ② `tk_talk` ≥ yes → `talk` ③ `tk_follow` ≥ yes → `follow` ④ 그 밖 → `new`. 요청 오류 · 시간 초과 → `new` + `consult.turn_kind.error`(턴을 죽이지 않는다). 시간 한도는 Jev 클라이언트의 지금 값(새 설정 0 — N-4) |
| TK7 | 지시문 = `prompts/consult.json` `jev_state.turn_kind{new, talk, follow}`(영어 초안 — §9) |
| TW1 · TW2 | 둘째 턴부터 `gather(walk(…, entry_pick=False, abbr_yes_only=True), 가르기)` — `CHAT_TURN_KIND=off` 면 기본 인자 |
| TW3 · W-6 | `talk` → 걷기 결과를 버린다. **앞 턴에 `ask` 가 없으면** 가르기가 끝나는 대로 걷기 작업을 거둔다(`cancel`) · **있으면** 걷기의 `front` 값이 있어야 하므로(W-7) 끝까지 기다렸다 버린다(§17 B-3). 그 턴에 객체 조회(QY) 0 · 깊이 읽기로 얻은 재료 0 · `targets` = `[]` — 허브에 남는 것은 걷기 · 거둠의 `resolve`(와 거두기 전에 떠난 조회)뿐이다 |
| TW4 | `follow` · 첫 걷기가 대상을 잡았으면 그대로 · 「입구 없음」 이면 앞 대상(TW6)을 든 후보 꼴 + `origin` = `follow` 로 실어 한 번 더 — 그 후보는 Noul 과 무관하게 대상(§8) |
| TW5 | `new` · 첫 걷기가 대상을 잡았으면 그대로 · 「입구 없음」 이면 `entry_pick=True` 로 한 번 더(시간은 지금과 같다 — O6-3) |
| TW6 · **W-3** | 앞 대상 = ① 바로 앞 성공 턴의 `targets[]` 가 **객체에 안 드는 표**(`SLOT_OF` 밖 — `package` · `adverse` · `condition` · `anatomy` · `offer`)면 그 대상(0.1 CR1 그대로) ② 아니면 객체의 가장 최근 `subjects[]`(`said` · `confirmed`) ③ 없으면 `focus` 고민 |
| TW7 · **W-3** | 든 후보(`carry.candidates`)를 켠 상태에서 거른다: **객체 칸에 드는 표(`SLOT_OF`)의 것만** 객체의 생사로(객체에 없거나 `withdrawn` 이면 뺀다) · 그 밖의 표는 CR1 그대로 싣는다 |
| TW8 · **W-4** | 줄임 후보(`matched.how` = `줄임`)는 Noul yes 일 때만 대상 — `front()` 의 선택 인자 `abbr_yes_only` 로만 건다(§8). 객체에도 yes 만 든다(`state.observe`) |
| TT1 · **W-7** | `talk` 턴의 객체 갱신 = ① 거둠 yes → `withdrawn` ② 앞 턴에 `ask` 가 있었으면 **버린 걷기의 `front.carried[]` 가운데 `origin` = `option` 이고 yes 인 항목**을 `how` = `option` 으로 든다(요청 추가 0). 글에서 새 낱말을 뽑지 않는다 |
| TT2 | TT1 로 객체가 바뀌면 L5 · L6 이 0.2 대로 돈다 · 안 바뀌면 객체 조회 0 · `list` · `sites` 안 보냄 |
| TT3 · N-5 | 「앱 판정」 = `{turn_kind: "talk", prev{closed_by, empty[], end_state}, close, seen_lines: []}` + 「상담 상태」 + 자료 `(없음)` + 질문. 새 재료 줄 0. 꼬리가 가리키는 줄은 **이 대화에서 이미 보낸 줄**이어도 된다 — `answer_lines` 는 대화 전체의 보낸 줄(`Conv.sent` · `summaries`)에 대조해 장부에 남긴다(고치지 않는다) |
| TT4 | 장부: `end_state` = `null` · `targets` = `[]` · `kinds` = `[]` · `trace` = 버린 걷기의 `front` 만(거둔 걷기는 `{cancelled: true}`) · `consult.turn_kind.walks[{entry_pick, used, ms, cancelled}]` |
| TT5 | 단계 = `understand` → `answer`(§5 끝 줄) |
| TT6 | `talk` 가 잇달아 `CHAT_TALK_MAX` 턴이면 다음 턴은 요청 없이 `new` |

**완료 조건**: S6-T1 ~ T7 · T25 통과(S6-T2 의 기대는 W-6 꼴) · `CHAT_TURN_KIND=off` 의 호출 순서가 0.2 와 같다.
**시험**: `tests/test_v03_turn_kind.py` · `tests/test_v03_shared.py`(새) + §8 의 기존 묶음 — WP 절 §8 에 적은 파일만.

## 8. 함께 쓰는 코드 — 선택 인자(C6-1 · 코디 W-4) ← WP-3 이 쓴다

**손대는 곳은 셋이고(검수 W-4), 셋 다 안 주면 `front()` · `walk()` 가 지금과 글자 그대로 같다.**

| # | 무엇 | 자리 | 기본값 = 지금 동작 |
|---|---|---|---|
| ① | 선택 인자 `entry_pick: bool = True` — `False` 면 이번 글의 후보 0 · 든 후보 yes 0 일 때 입구 고르기(`pick_entries`)를 부르지 않고 곧바로 「입구 없음」 으로 돌아온다(trace 에 `entry_pick: {skipped: true}`) | `walk/front.py:284` 의 `elif not concepts:` 가지 | `True` |
| ② | 선택 인자 `abbr_yes_only: bool = False` — `True` 면 `matched.how` = `줄임` 인 후보는 yes 일 때만 대상(사이 값 · no → `dropped` · TG2 · TG3 를 걸지 않는다). `부분` 후보 · 덮인 조각 규칙은 그대로 | `walk/front.py:337-349` 의 판정 가지 | `False` — **시험 앱 B 열 무변경** |
| ③ | 든 후보 항목의 `origin` = `follow` — Noul 과 무관하게 대상(`decision` = `carried` · trace 에 `origin`). `origin` 이 없거나 `option` 인 항목은 지금 그대로(yes 만) | `walk/front.py:268-279` | 상담만 그 값을 싣는다 |
| — | `walk()` 가 두 인자를 받아 `front()` 로 넘긴다 | `columns/col_b.py:161` · `:169` | 안 주면 안 넘김 |

- SPEC-004 ST3 「선택 인자 둘뿐」 은 **넷**(`carry` · `instr` · `entry_pick` · `abbr_yes_only`)이 된다 — SPEC 은 「셋」 이라 적었다(§17 B-12 되적기 후보).
- `walk/jev_requests.py` 는 안 고친다(`_target_instr` 는 `follow` 후보에 지금 `target_carried` 절을 준다 — 값을 안 쓰므로 그대로 둔다).
- **S6-T6**: 인자 둘을 안 주고 `origin` 을 안 실으면 `front()` 결과 · trace 가 지금과 같다 → **기존 시험 파일을 안 고치고** 통과로 본다: `tests/test_walk_front.py` · `tests/test_walk_core.py` · `tests/test_walk_entry.py` · `tests/test_consult_carry.py` · `tests/test_state_carry.py`. WP-3 이 도는 기존 묶음은 이 다섯 + `tests/test_consult_turn.py`(끈 상태 턴)이다. 보고에 고친 줄 수를 적는다.

## 9. WP-2 — `system_v3` · 「앱 판정」 칸 · 금지 낱말 검사

**SPEC**: §3 VO1 ~ VO10 · §3-2 열세 절 · §3-3 · §5-2(절 `material` 안) · S6-T8 · T9 · T22 · 코디 W-5 · W-10.

| 규칙 | 구현 |
|---|---|
| VO1 | `prompts/consult.json` 에 새 배열 `system_v3[]`(절 꼴 `{id, lines[]}` · 순서 = `role` · `voice` · `facts` · `owner` · `hidden` · `turn` · `state` · `empty` · `close` · `synergy` · `safety` · `material` · `tail`) · `version` = `0.3.0-draft`. `prompt.py` — 켠 상태(rev 3)의 시스템 글 = `system_v3` 를 이어 붙인 글 · 꼬리 표식이 그 글에 있어야 한다. **`system[]` 의 글자는 안 바꾼다** → 끈 상태 시스템 글이 0.1 과 글자 그대로(S5-T15 유지). `system_state[]` 는 지우지 않는다(안 쓴다 · 있으면 꼴 검사만) |
| VO1(거절) | 켠 대화를 시작할 수 있나(`state_ready` 자리) = `system_v3` · `jev_state.turn_kind` 셋 · `kind_labels` · `voice_check` · `turn_headers.close` · `prev` 가 전부 있다 — 없으면 0.2 와 같은 길로 거절(`rejected("prompt")`) |
| VO2 ~ VO9 · §3-2 | 절의 글 = SPEC §3-2 「담을 뜻」 을 옮긴 **초안**(문장을 더 짓지 않는다 — 뜻이 없는 줄 0). `owner` = `holder` 로 말한다(VO4) · `hidden` = VO3 의 낱말 목록 · `turn` = TT3 · `close` = §10 · `material` = 0.1 의 표지 뜻 + `modality_level` + 종료 상태별 말(§5-2) + 「표지 이름 · 값 낱말을 답에 쓰지 않는다」 |
| **W-5** | 절 `empty` · `safety` 에 한 줄씩: `empty[]` 의 `safety` 가 참인 것(부작용 · 금기 · 회피)은 「없어요」 로 말하지 않는다 — **「확인된 정보가 없어요」 꼴까지**(없다 · 안전하다로 말하지 않는다) |
| SP(§12) | 절 `material` 에 한 줄(초안): 요약 줄 · 「앱 판정」 의 `site.applied` 가 `prefer` 면 그 부위로 좁힌 것이 아니다 — `site_prefer` 표지가 없는 시술을 그 부위의 것이라고 말하지 않는다(그 고민의 것으로 말한다 · SPEC-001 SP8) |
| §3-3 키 | `jev_state.turn_kind{new, talk, follow}`(영어) · `kind_labels{}`(정보 종류 14 → 손님 말 이름 · 초안) · `voice_check[]`(정규식 · 초안 — 한 글자 「행」 은 「n행」 · 「행이」 꼴로만) · `turn_headers.close` · `turn_headers.prev` |
| **W-10** `slots` | 선택 키 `slots{}` — 빈 자리의 **정해진 문구 값**. 이 판은 하나: `mark-modality-level` = 「{name} 계열 시술」(`{name}` = 계열 이름 — 사용자 초안 확정). 템플릿은 그 값을 받아 그리기만 한다(템플릿에 한글 문장 0 — S6-T23 유지 · 단계 문구 `steps` 와 같은 길). 그 밖의 빈 자리는 비워 둔다(§17 B-1) |
| 「앱 판정」 빼기(S6-T9) | 켠 상태 메시지에서 `read_as[]` · `offered[].rows` · `unresolved[]` 를 뺀다 · `ask.options[].layer` → `holder`(주인 이름). 끈 상태는 0.1 그대로(`col_b.judgement` 는 안 고친다 — `material.judgement_of` 의 켠 가지에서 뺀다) |
| VO10 | `consult/voice.py` — `voice_check[]` 를 꼬리 뗀 답 본문에 돌려 `consult.voice{hits[{pattern, text}], n}` 에 남긴다(`CHAT_VOICE_CHECK=on`). **답을 고치거나 다시 돌리지 않는다** |

**완료 조건**: S6-T8 · T9 · T22 통과 · 끈 상태 시스템 글의 sha 가 0.1 값 그대로.
**시험**: `tests/test_v03_prompt.py`(새) + `tests/test_consult_prompt.py` · `tests/test_consult_material.py`(기존 · 안 고침) — 이 셋만. (`close` · `empty` 칸의 값은 WP-4 가 채운다 — 이 WP 는 칸의 자리와 빼기까지.)

## 10. WP-4 — `close` · `empty` · 꼬리

**SPEC**: §4 CS1 ~ CS6 · §5 EM1 ~ EM6 · §5-2 · S6-T10 · T11 · T14 · 코디 W-5 · W-8 · 검수 N-6.

| 규칙 | 구현 |
|---|---|
| EM1 · EM2 | `consult/close.py` `empties()` — 걷기 · 객체 조회가 그 (대상 × 정보 종류)를 **끝까지 읽었고 0 행**인 것만. 「앱 판정」 `empty[{about: 대상 이름, what: kind_labels 이름, safety: bool}]` · 장부 `consult.empty[{about{table, code}, what: 종류 코드, tool, total: 0, complete: true}]`. 오류 · 쪽 넘김 미완 · 「실행 중단」 은 `empty` 아님 |
| **W-5** | `safety` = 종류가 `blanks.SAFETY_KINDS`(`adverse` · `contraindication` · `avoid`)에 든다 — LLM 이 절 `empty` · `safety` 로 가른다(§9) |
| EM3 | `alt` = `focus` 고민 리스트의 계열 가운데 이번 대상의 계열이 아닌 것 — 허브 순서 앞에서 `CHAT_ALT_MAX` 개 · 이름만. `focus` 가 없거나 다른 계열 0 이면 없음 |
| EM4 | 행 수를 LLM 에 주지 않는다(WP-2 의 빼기와 같은 곳) |
| EM5 | 시너지(QY4 「보완」) 0 행 = `empty`(`what` = 조합) — **그 턴 걷기의 종류에 조합이 든 턴에만** |
| EM6 | 리스트가 0 인 고민(내려온 묶음까지 0 · 물려받은 리스트도 없음) = `empty`(`what` = 시술) |
| CS1 · CS2 | `close{by, …}` 를 턴마다 하나: ① `ask` 가 있으면 언제나 `ask` ② `empty` 가 있고 `alt` 가 있으면 `alt` ③ `offered`(종류 이름만 — `kind_labels`) ④ `null`. 같은 장부 → 같은 `close`(결정론) |
| CS3 | `ask` 가 있으면 `close.by` = `ask` — 0.1 `rules` 10 의 「끝은 `offered` 되묻기」 는 `system_v3` 에 없다 |
| CS4 | `offered` 에서 안전 종류를 뺀다(`SAFETY_KINDS`). NQ6 그대로 |
| CS5 · **W-8** | `tail.py` — 꼬리(`<<<근거>>>` 아래)의 `close: <답 줄 번호>` 한 줄을 읽어 `consult.close.said` 에(줄 없으면 `null` · `close: 0` 이면 `0`). 화면 조각에 꼬리 글자 0(`TailFilter` 그대로). `by` = `ask` 이고 **`said` = 0 이면 `blanks.record` 를 부르지 않는다**(`asked[]` 에 없다 → 준 횟수 · 걸린 선택지 · NQ5 에 없는 턴). `said` = `null` 은 센다(지금 동작) |
| CS6 | `by` = `null` 인데 물음으로 끝났는지는 고치지 않는다 — 장부 `said` 로만 |
| N-6 | `close.by` = `offered` 에 `package` 종류가 남는다 — 이 판은 그대로 두고 E6-6 확인 거리로 넘긴다(§17 O-6) |

(CS7 은 WP-5.)

**완료 조건**: S6-T10 · T11 · T14 통과(T14 에 「안전 종류 0 행 → `safety: true`」 한 꼴).
**시험**: `tests/test_v03_close.py`(새) + `tests/test_state_blanks.py`(기존 — 달리 받는 시험이 있으면 §15 대로) — 이 둘만.

## 11. WP-5 — 객체 구멍 · 옛 대화

**SPEC**: §8 FX1 ~ FX4 · §4 CS7 · S6-T12 · T13 · T21.

| 규칙 | 구현 |
|---|---|
| FX1 | `state.py` `_again`(`:118-122`) — `guess` → `confirmed` 는 ① 다시 나온 관찰이 `target`(`said` 급) ② 걸린 선택지 yes ③ BK5 답 yes 일 때만. `guess` 급으로 다시 나오면 `history[]` 에 턴만 더하고 `state` 는 그대로 |
| FX2 | SPEC-005 S5-T2 의 기대를 FX1 로 고친다 — `tests/test_state_object.py` 의 그 시험(§15) |
| CS7 | `blanks.count` — `guess` 인 부위가 `focus` 고민의 고민 부위(`concern_sites[]`)와 같은 코드면 BK5 빈 칸으로 세지 않는다 |
| FX3 | 서버 값과 대화 값이 다르면(서버 켬 · 대화 끔 / 대화에 `consult_rev` 없음 · 작음) 대화 화면에 빈 자리 `conv-outdated`(문구 사용자)와 새 대화로 가는 링크(`/`). 드로어 항목의 `data-conv-state` = `outdated` |
| FX4 | 끈 상태로 시작한 대화 = 0.1 로 끝까지 돈다(표지만). **`consult_rev` 없는 켠 대화**(0.2 로 시작) = `blocked()` 가 `rev_changed` 를 돌려 `POST` 를 거절한다(장부 줄을 쓰지 않는다 — 쓴 줄은 고치지 않는다 · §17 B-5) |

**완료 조건**: S6-T12 · T13 · T21 통과.
**시험**: `tests/test_v03_fixes.py`(새) + `tests/test_state_object.py`(S5-T2 고친 꼴) · `tests/test_consult_ledger.py`(기존 · 안 고침) — 이 셋만.

## 12. WP-6 — 리스트 · 요약 줄 · 내려온 묶음 · SP

**SPEC**: §6 LS1 ~ LS8 · LS4-1 · S6-T15 · T16 · T26 · 코디 W-9 · W-10 · SPEC-001 0.7.1 §5-11 SP1 ~ SP8 · 검수(`review-spec-001-v071.md`) N-4.

| 규칙 | 구현 |
|---|---|
| LS1 · LS2 | `partials/list.html` — 글로 그리는 것은 고민 · 계열 · 시술 이름뿐. `reach` · `concern_match` 배지를 지우고 값은 `data-reach` · `data-concern-match` 로만. 「그 밖」(`list-section-unreached`) · 「계열 층만」(`list-section-modality-only`) 묶음은 켠 상태 꼴에서 안 그린다(끈 상태 꼴은 0.1 그대로 — 꼴에 `hidden` 칸이 있을 때만 새 길) |
| LS3 | 메뉴 · 패키지 이름을 조각에 안 그린다 — 장부 `list.hidden{unreached_n, names[], descended_n}` |
| LS4 · **W-10** | `listing.py` — `descended[]` 한 항목 = 계열 묶음 하나. 묶음에 `modality_level: true` · `from_gids[]`(`from[].gid`) · 시술에 `descended: true`. 화면: 묶음 머리에 `data-unit` · `data-modality-level` · 빈 자리 `mark-modality-level` 에 `slots` 값(「{name} 계열 시술」 — §9) · 시술 행에는 표지 글 없이 `data-descended` 만. `from[].path[]` 의 이름 0 |
| LS4-1 · **W-9 (a)** | ① `in_groups` 참인 시술은 다시 그리지 않는다 ② 그 고민의 `groups[]` 에 **시술이 하나도 없는 계열**만 `procedures[]` 를 전부 그린다 ③ `groups[]` 에 시술이 있는 계열은 직접 닿은 시술만(내려온 나머지는 `hidden.descended_n` 에 수만) |
| LS5 | `modality_only[]` 는 따로 묶음으로 안 그린다(같은 행이 `descended[]` 로 온다). 못 내린 행(`counts.descended.undescended`)만 `list.hidden` 에 |
| LS6 | `material.summaries` 의 켠 가지 — 요약 줄 = `{n, 계열 이름, 시술 수, 원리 이름들, modality_level}`(`reach[]` · `concern_match[]` 뺌). 장부의 `gids[]` 는 그대로(내려온 묶음은 `from[].gid`) |
| LS7 · LS8 | 묶음 ① · ③ 은 0.2 그대로(① 의 표 값은 `data-table` 로만) · 순서 · 순위 없음 |

### SP — 부위가 묶이지 않은 고민 + 부위(규칙 ① · SPEC-001 0.7.1)

SPEC-006 0.1.0 은 0.7.0 기준이라 이 규칙의 줄이 없다. 지시서가 「SP 꼴」 을 이 WORK 에 넣었고, 아래는 SPEC-001 0.7.1 §5-11 SP 와 그 문서의 「따라 고칠 곳 — SPEC-006: 리스트에서 `site_prefer` 묶음을 앞에」 를 옮긴 것이다. **상담 쪽만이다**(걷기 · 답 키는 §17 B-9).

| # | 규칙 | 구현 |
|---|---|---|
| SP-1 | 객체 기준 조회 QY5(`plan.qy1_calls` — `focus` 고민 + 거르개 부위)는 지금처럼 `site` 를 건다 · **`site_mode` 는 보내지 않는다**(기본 `auto`) | `plan.py:87-95` 안 고침 |
| SP-2 | 응답 머리 `site_applied` 를 읽는다: `filter` · `None` → 0.2 그대로(거른 리스트) · **`prefer` → 거르지 않은 리스트**(그 고민의 행 전부 — `site` 없이 부른 것과 같은 행). 부위가 여럿이라 조회가 여럿이어도 `prefer` 면 행이 같으므로 리스트는 한 번만 짓고 표지는 합친다(같은 `gid` 를 다시 세지 않는다 — `build_list` 의 `_seen` 그대로) | `plan.py` → `listing.py` |
| SP-3 | **표지** — 시술 = 그 묶음의 `n_site_prefer` > 0(없으면 행의 `site_prefer` 가 하나라도 참) → `site_prefer: true` · 계열 묶음 = 표지 시술이 하나라도 있다. 화면: `data-site-prefer` + 빈 자리 `mark-site-prefer`(문구 사용자 — 짓지 않는다) | `listing.py` · `list.html` |
| SP-4 | **앞에 둔다**(SPEC-001 SP4 「순서는 앱」) — `prefer` 일 때만: 계열 묶음은 표지 있는 것이 먼저 · 묶음 안 시술도 표지 있는 것이 먼저. **안정 정렬**(그 밖의 순서는 허브 순서 그대로 · LS8 「순위 없음」 은 표지 밖에서 그대로) | `listing.py` |
| SP-5 | **표지 0 일 때**(`counts.site_prefer.rows` = 0 — 실물 「볼 + 탄력 저하」 꼴 · 검수 N-4) = 리스트는 허브 순서 그대로 · 표지 요소 0 · **새 문구 0**(빈 화면 · 안내 글을 짓지 않는다). 그 사실은 ① 장부 `list.site{name, applied: "prefer", prefer_rows: 0, prefer_groups: 0}` ② 「앱 판정」 `site{name, applied, prefer_n}` 로 LLM 에 간다 — 절 `material` 의 한 줄(§9)로 「그 부위의 것이라고 말하지 않는다」 | `listing.py` · `material.py` |
| SP-6 | 부위가 묶인 고민(`filter`)은 0.2 와 같은 리스트다(이마 꼴 회귀 0). `filter` 로 0 행이면 0 그대로(`counts.unfiltered_rows` 는 장부에만) | 확인만 |
| SP-7 | `descended[]` 는 `prefer` 일 때 거르지 않은 행 전부에서 온다 — LS4 · LS4-1 그대로 그린다(내려온 묶음에는 표지를 달지 않는다 — 허브가 `descended[]` 에 표지를 주지 않는다) | 확인만 |

**SP 시험 꼴**(`tests/test_v03_list.py` 안 — 가짜 허브):

| # | 무엇 | 기대 |
|---|---|---|
| SP-T1 | 부위 없는 고민 + 부위 · 표지 있음 | `site_applied` = `prefer` 응답(행 넷 · 표지 둘) → 리스트에 시술 넷 전부 · 표지 시술 둘이 앞 · 계열 묶음도 표지 있는 것이 앞 · `data-site-prefer` 둘 · 장부 `list.site.prefer_rows` = 2 · 요청에 `site_mode` 없음 |
| SP-T2 | **표지 0 일 때** | `prefer` · `counts.site_prefer.rows` = 0 → 리스트 = `site` 없이 부른 것과 같은 순서 · `data-site-prefer` 0 · 새 `data-slot` 글 0 · 「앱 판정」 `site.prefer_n` = 0 · 장부 `list.site.applied` = `prefer` |
| SP-T3 | 부위 있는 고민 + 부위(회귀) | `site_applied` = `filter` → 0.2 와 같은 리스트 꼴(표지 칸 없음) · `site_applied` 칸이 없는 응답(허브 0.6)도 같다 |
| SP-T4 | 걷기 재료(안 고침 · 확인만) | `prefer` 응답을 걷기가 읽을 때 재료 줄의 `site_match` 표지가 **표지 행에만** 붙는다(`walk/material.py:115-117` — `site_match[]` 가 있는 행만) · 어긋나면 고치지 말고 보고 |

**완료 조건**: S6-T15 · T16 · T26 · SP-T1 ~ T4 통과.
**시험**: `tests/test_v03_list.py`(새) + `tests/test_consult_listing.py`(기존 · 안 고침 — 끈 상태 꼴) · `tests/test_state_list.py` · `tests/test_state_plan.py`(기존 — 달리 받는 시험은 §15) — 이 넷만.

## 13. WP-7 — 점 누적 · 누르기 · `viewing`

**SPEC**: §7 FD1 ~ FD7 · FD9 ~ FD11 · S6-T17 ~ T19 · E6-0 · 코디 W-1 · W-2 · 검수 N-9. **FD8 · S6-T20 은 보류**(U6-4).

| 규칙 | 구현 |
|---|---|
| FD1 | `sites.py` `SITES_FIELD` = `sites` · `PAIR_KEYS` 에 `match`. 점의 재료 = `concerns[]` 가운데 `said` · `confirmed` **전부**의 고민 부위(`guess` · 거둔 것 빼고) — `plan.derive` 가 `concern_sites[]` 를 `focus` 하나가 아니라 그 고민 전부에서 세운다(항목에 `asked` = 그 응답을 물은 객체 고민 코드 · `match`). `focus` 가 아닌 고민의 응답은 대화 메모(`Conv.memo`)에서 · 없으면 QY1 과 같은 조회 |
| FD2 | `sites` 꼴 — 점 · 라벨마다 `concern_codes[]`(그 부위를 가진 고민 코드 — `match` = `하위` 면 **하위 고민 코드** · SPEC-001 CS2 값 그대로) · `asked_codes[]`(그 점이 온 객체 고민) · `match` · `focus`. 화면: `data-site-code` · `data-concern-codes` · `data-match` · `data-focus`. 같은 부위는 한 번 |
| FD3 | 보내는 때 = 합집합이 바뀐 턴 · `focus` 가 바뀐 턴. 새 고민에 부위가 없어도 앞 점은 남는다(빈 조각으로 지우지 않는다) |
| FD4 · N-9 | 라우트 `GET /c/{conv_id}/list?concern=<코드>`(여럿이면 되풀이) → HTML 조각(`#procedure-list`). 재료 = 그 대화가 이미 읽은 그 고민의 `concern_candidates` 응답(메모) · 없으면 **QY1 꼴 조회**(부위 거르개 없음). **허브만** — Jev · LLM 0 · 장부 줄 0 |
| FD5 | 누른 조각 = §12 의 꼴 · 묶음 ② 만 그 고민 것(① · ③ 은 그대로) · 고민이 여럿이면 고민마다 차례로 |
| FD7 · **W-1** | 받는 코드 = ① 객체 `concerns[]`(`said` · `confirmed`)의 코드 ② **객체 고민의 하위 고민 코드**(그 대화의 `concern_sites[]` 에 `match` = `하위` 로 실린 `concern_code`). 그 밖은 거절(누르기 = 4xx 조각 · `viewing` = 버리고 장부 `consult.viewing.rejected`) |
| FD6 · **W-2** | `consult.js` 가 누른 고민 코드를 폼의 숨은 칸 `viewing` 에 싣고, **`POST` 한 번 뒤 비운다**(누른 다음 한 턴만). 앱은 그 턴 L4 에서 `focus` 를 그 고민으로 옮긴다(diff `op` = `focus` · `why` = `view`). **같은 턴 글에서 새 고민이 `said` 로 들면 글이 이긴다**(`viewing` 은 장부에 `accepted: false · why: "text"`). 코드가 여럿이면(한 점에 고민 여럿) **객체에서 가장 최근 고민**(`source.turn` 이 가장 큰 것) 하나 |
| FD6(하위 고민) | `viewing` 이 W-1 ② 의 하위 고민 코드면 그 고민을 객체 `concerns[]` 에 들이고(`state` = `said` · `how` = `view` — `HOWS` 에 값 하나 더) `focus` 로 삼는다(§17 B-2) |
| FD9 | 좌표 · 꼴은 `face_coords.py` 그대로(`place()` 를 부르기만) |
| FD10 · E6-0 | 누르기는 htmx 속성(`hx-get` · `hx-target="#procedure-list"`)으로 건다. **SVG 안 `<circle>` 에 htmx 속성이 서는지는 E6-0 에서 본다** — 안 서면 `consult.js` 의 이벤트 위임으로 같은 주소를 부른다(인라인 스크립트 0) |
| FD11 | 누른 점 표시(`aria-pressed`)는 `consult.js` — 서버는 `sites` 를 다시 보내지 않는다 |

**완료 조건**: S6-T17 ~ T19 통과(T17 에 `하위` 점 누르기 한 꼴 · T19 에 W-2 의 세 꼴 + `talk` 턴 한 꼴) · E6-0 의 결과가 보고에 있다 · `_face.svg` · `face_coords.py` sha 변경 0.
**시험**: `tests/test_v03_sites.py`(새) + `tests/test_consult_sites.py`(기존 · 안 고침) — 이 둘만. E6-0 은 워커가 18223 을 가짜 턴(`CHAT_FAKE_TURN`)으로 띄워 본다(외부 호출 0).

## 14. WP-8 — 실물 E6-0 ~ E6-5 · README

**SPEC**: §11-2 · §11-3 · §11-4.

| # | 무엇 | 누가 | 어떻게 |
|---|---|---|---|
| E6-0 | SVG 안 점 누르기 · 조각 갈아 끼우기 | 워커 | WP-7 에서(18223 · 가짜 턴) |
| E6-1 | 실물 대화 셋(SPEC §11-3 의 12 턴)을 **새 대화로 같은 글을 차례로** + SP 실물 한 대화(「볼에 탄력 저하 시술 추천해줘」 — `_RESUME` §2 규칙 ①) | 워커(안 되면 코디) | `consult/e6.py` + `consult/e6_inputs.json`(0.2 의 `e5.py` 꼴 · `probe --e6 [--only …]`) · 장부는 `CHAT_DIR/e6/` |
| E6-2 | 가르기 Noul 분포 | 같음 | **12 턴 가운데 첫 턴 빼고 9**(W-12 ③)의 `tk_*` 값 · 틀린 판정 수 · 가르기 요청 시간 |
| E6-3 | 걷기 버리기 | 같음 | `talk` 턴에 버린 걷기가 남긴 허브 · Jev 요청 수 · 거둔 걷기 수 · 다음 턴 영향 |
| E6-4 | 꼬리 `close:` | 같음 | LLM 이 줄을 쓰는 비율 · `by` = `ask` 인데 `said` = 0 인 턴 수 |
| E6-5 | 금지 낱말 | 같음 | 전 턴 `consult.voice.n` 합(기대 0) · 걸린 낱말 · `by` = `null` 인데 물음으로 끝난 턴 수 |
| E6-6 | 화면 e2e | **코디가 18222 를 띄우고 사용자가 확인** | SPEC E6-6 의 목록 + 내려온 묶음 머리 「○○ 계열 시술」 이 보이는가(W-10) · 직접 닿은 시술이 있는 계열은 그 시술만 보이는가(W-9) · 끝맺음에 패키지를 권하는 턴(N-6) · SP 꼴(표지 0 일 때 리스트) |

**허브 판 — 두 번 돈다.**

| 때 | 18105 | 워커가 보는 것 |
|---|---|---|
| ① 코드가 선 직후 | **0.7.1 구현 전**(0.6 응답 — `descended` · `sites` · `matched.how` · `site_applied` 칸 없음) | **A1 ~ A4 기대만**: 턴 종류 · 걷기 수 · Jev 요청 수 · `close` · `empty` · 금지 낱말 · `first_list_ms` · `ttft_ms` · `total_ms`. 리스트는 0.2 꼴(내려온 묶음 0) · 점 0 · 「지방 주사」 오독은 남는다 — 보고에 「0.7.1 칸 없이 돈 판」 이라고 밝힌다(응답에 `descended` 칸이 있는지로 가른다) |
| ② 코디의 「18105 다시 띄움」 알림 뒤 | **0.7.1** | SPEC §11-3 표의 턴마다 전부(리스트 · 점 · 「지방 주사」 → `M18` · SP 실물의 `site_applied` = `prefer` · 표지 수) |

- 워커는 18223 만 띄우고 내린다. **18105 · 18222 를 띄우거나 내리지 않는다.**
- §11-3 의 기대는 W-12 로 고친 값으로 읽는다: ③ 턴 2 「볼」 = 0.59 `uncertain_kept`(→ `guess`) · ① 턴 6 = `ask` null → `close.by` = `offered`(안전 빼고) 또는 `null` · `talk` 턴 = 객체 조회 0 · 깊이 읽기 0(허브는 `resolve` 뿐 — W-6).
- 「(가정)」 인 곳(Jev 값이 드는 `talk` · `new` · 줄임 yes)은 실제 값을 그대로 적는다. 기대와 다르면 문턱 · 지시문을 고치지 말고 보고한다(O6-1).
- README 상담 절에 0.3 한 묶음: 설정 여섯 · `probe --e6` · 드로어 · 객체 패널 · 로컬 한 사람 전제(SV11).

**시험**: `tests/test_v03_e6.py`(새 — 입력 파일 꼴 · 요약 함수만 · 외부 호출 0) — 이것만. 실물은 시험이 아니다.

## 15. 순서 · 의존 · 앞 판 시험(S6-T24)

| WP | 앞선 것 | 허브 0.7.1 | 도는 시험 파일(이것만) |
|---|---|---|---|
| WP-0 | — | 무관 | `test_v03_start.py` · `test_consult_ledger.py` |
| WP-1 | WP-0 | 무관 | `test_v03_frame.py` · `test_consult_page.py` · `test_consult_chat_ui.py` |
| WP-2 | WP-0 | 무관 | `test_v03_prompt.py` · `test_consult_prompt.py` · `test_consult_material.py` |
| WP-3 | WP-2 | 가짜 | `test_v03_turn_kind.py` · `test_v03_shared.py` · `test_walk_front.py` · `test_walk_core.py` · `test_walk_entry.py` · `test_consult_carry.py` · `test_state_carry.py` · `test_consult_turn.py` |
| WP-4 | WP-2 · WP-3 | 가짜 | `test_v03_close.py` · `test_state_blanks.py` |
| WP-5 | WP-0 | 가짜 | `test_v03_fixes.py` · `test_state_object.py` · `test_consult_ledger.py` |
| WP-6 | WP-2 | 가짜(0.7.1 꼴) | `test_v03_list.py` · `test_consult_listing.py` · `test_state_list.py` · `test_state_plan.py` |
| WP-7 | WP-6 | 가짜(0.7.1 꼴) | `test_v03_sites.py` · `test_consult_sites.py` |
| WP-8 | 전부 | ① 전 · ② 뒤 | `test_v03_e6.py` |

- **직렬**(같은 워크트리 · 한 워커). 허브 구현(WORK-013)과는 병행 — 칸 이름은 §4 로 맞춘다.
- **S6-T24 를 달리 받는다**: 「SPEC-004 T1 ~ T18 · SPEC-005 S5-T1 ~ T21 · 시험 앱의 지금 시험 전부 통과」 를 **전체 pytest 로 확인하지 않는다**(사용자 11-17). 대신 위 표의 기존 파일을 그 WP 에서 돈다. 표에 없는 기존 파일(`test_state_examples.py` · `test_state_synergy.py` · `test_web.py` · 시험 앱 묶음)은 이 판이 그 모듈을 고치지 않거나 켠 상태 통째 교체로 기대가 바뀌는 것이다 — 워커가 돌리지 않는다(코디 판단 — §17 B-10).
- **달리 받는 S5 시험**(W-12 ⑤ — 0.3 이 켠 상태를 바꿔 기대가 달라지는 것 · `tests/test_state_*.py` 에서 **그 시험만** 고친다 · 고친 시험 이름을 보고에 적는다): ① S5-T2 「`guess` 가 다시 나오면 `confirmed`」 → FX1 ② S5-T7 「리스트 · 점이 `focus` 것」 → 점은 전부(FD1) ③ 켠 상태 시스템 글(`system` + `system_state`) → `system_v3`(VO1) ④ 「앱 판정」 칸(`read_as` · `offered[].rows` · `unresolved` · `options[].layer`) → §9 의 빼기 ⑤ 리스트 조각의 배지 · 「그 밖」 묶음 → §12 ⑥ 요약 줄의 `reach[]` · `concern_match[]` → LS6. 이 여섯 밖에서 0.2 시험이 깨지면 고치지 말고 보고한다.

## 16. 검수 지적 반영 — `review-spec-006.md` WARN 12 · NOTE 9

| # | 무엇 | 이 문서 |
|---|---|---|
| W-1 | 하위 고민 부위 점 | 코디 값 → §13 FD7 · FD6(하위 고민) |
| W-2 | `viewing` 수명 · 우선 · 여럿 | 코디 값 → §13 FD6 · `talk` 턴은 §17 B-4 |
| W-3 | 객체 밖 표의 이어 묻기 | 코디 값 → §7 TW6 · TW7 |
| W-4 | 함께 쓰는 코드 손대는 곳 셋 | 코디 값 → §8(선택 인자 둘 + `follow` 가지 · S6-T6 「셋 다 안 주면 글자 그대로」) |
| W-5 | 안전 종류의 `empty` | 코디 값 → §9 · §10 |
| W-6 | `talk` 턴 「허브 조회 0」 | §7 TW3 · §14 |
| W-7 | 선택지를 두 번 묻지 않음 | §7 TT1 |
| W-8 | 안 실린 `ask` 의 뒤처리 | §10 CS5 |
| W-9 | 내려온 시술의 화면 폭 | 사용자 (a) → §12 LS4-1 · E6-6 확인 거리 |
| W-10 | 묶음 머리 표지 문구 | 사용자 「○○ 계열 시술」 → §9 `slots` · §12 LS4. `conv-outdated` · `label-concern-title` 은 빈 자리 그대로(뒤 것은 FD8 보류라 이 판에 없다) |
| W-11 | 드로어 색인 | §6a SV3 |
| W-12 | 수 · 기대 고침 | §3-2 · §14 · §15 |
| N-1 | 「34 요청」 = 그 턴 Jev 전체(입구 고르기 33) | E6-1 보고는 `trace.entry_pick.requests` 와 턴 전체를 따로 적는다 |
| N-2 | 첫 걷기가 이름을 `target` 으로 잡았는데 `tk_talk` 만 yes | 이 판은 TK5 그대로(걷기를 버린다) — E6-2 에 그 턴 수를 세고 §17 O-3 |
| N-3 | `extra` 는 묶음 여럿이면 가장 낮은 값 | §7 TK3(첫 묶음에만) |
| N-4 | 가르기 시간 한도 · 판정까지 붙들기 | §5 끝 줄 · §7 TK6 |
| N-5 | `talk` 턴의 꼬리 | §7 TT3 |
| N-6 | `close.by` = `offered` 의 `package` | §10 · §14 E6-6 |
| N-7 | 설정 여섯 · 라우트 둘 | §6 · §6a · §13 |
| N-8 | A8 근거는 `_RESUME` §2 행 | 머리말 links |
| N-9 | 「턴 0」 의 뜻 · 누른 리스트 = QY1 | §6a · §13 FD4 |

## 17. 열린 것 · 이 문서를 쓰며 본 것(SPEC 은 고치지 않았다)

### 17-1. 열린 것(이 판에 짓지 않는다)

| # | 무엇 | 상태 |
|---|---|---|
| **O-1** | **U6-4 — 부위가 없는 고민의 누를 자리**(FD8 고민 이름 칩 · `sites.chips[]` · 빈 자리 `label-concern-title` · S6-T20) | **보류(사용자가 더 조사)** — 짓지 않는다. 그동안 부위 없는 고민은 `focus` 일 때만 리스트가 보인다 |
| O-2 | `concern_site` 데이터 보강(규칙 ② — 후보 약 10) | 코드 끝난 뒤 한 번에(`_RESUME` §2) — 이 WORK 밖. 그 전에는 SP 표지가 대부분 0 이다(SPEC-001 O-31 ②) |
| O-3 | 가르기가 틀렸을 때(O6-1 · N-2) · `follow` 의 앞 대상이 둘 이상(O6-2) | E6-2 값을 본 뒤 코디 |
| O-4 | 글자 맞춤 0 인 `new` 턴의 입구 고르기 시간(O6-3) · `uncertain_kept` 이름이 재료 · 리스트에 드는 것(O6-4) | 걷기 쪽 — 별도 |
| O-5 | `kind_labels` · `voice_check` · 종료 상태별 말 · 빈 자리 문구(`conv-outdated` · `mark-site-prefer` · 드로어 · 패널 여섯) | 사용자(E6-6 에서) |
| O-6 | 끝맺음에서 패키지를 권할지(N-6) · 내려온 시술의 폭(O6-11) · 점이 많을 때의 화면(O6-7) | E6-6 뒤 |
| O-7 | 드로어의 지우기 · 이름 붙이기 · 찾기(O6-12) · 패널에 걷기 trace(O6-13) · 누르기 흔적(O6-8) | 이 판 없음 |
| O-8 | SPEC-004 · SPEC-005 · SPEC-006 되적기 | 구현 뒤 코디(§17-2 의 「되적기」 줄) |

### 17-2. B — 구현 워커가 추측으로 메우지 않게 이 문서가 정한 값(코디가 바꿀 수 있다)

| # | 무엇 | 이 문서의 값 | 왜 |
|---|---|---|---|
| B-1 | 「○○ 계열 시술」 을 어디에 두나 | `prompts/consult.json` 의 선택 키 `slots{}` — 템플릿은 값만 받는다 | 템플릿 · 코드에 한글 문장 0(S6-T23)을 지키면서 정해진 문구를 싣는 길 — 단계 문구 `steps` 와 같은 꼴 |
| B-2 | 하위 고민을 `viewing` 으로 받았을 때 객체 | `concerns[]` 에 `said` · `how` = `view` 로 들이고 `focus` | 코디 W-1 「그 하위 고민으로 `viewing`」 — `focus` 는 `concerns[]` 의 코드여야 한다. `how` 값이 하나 는다(SPEC-005 의 넷 → 다섯 · 되적기) |
| B-3 | `talk` 일 때 걷기를 언제 거두나 | 앞 턴 `ask` 가 없으면 곧바로 · 있으면 끝까지 기다렸다 버림 | TW3 「거둔다」 와 W-7 「버린 걷기의 `front` 값」 이 부딪히는 곳 — `walk()` 는 끝나야 `front` 를 돌려준다(함께 쓰는 코드에 인자를 더 열지 않는다) |
| B-4 | `talk` 턴에 `viewing` 이 오면 | 받는다 — `focus` 가 옮고 TT2 로 객체 조회 · `list` 가 간다 | 검수 W-2 ④ 의 고칠 방향 · 코디 값에는 그 꼴이 없다 |
| B-5 | `rev_changed` 거절의 장부 | 줄을 쓰지 않는다(다른 거절과 같은 길) | SPEC FX4 는 「`conv_end` = `rev_changed`」 라 적었지만 옛 대화에 새 줄을 쓰면 「쓴 줄은 고치지 않는다 · 턴을 받지 않는다」 와 엇갈린다 — 되적기 |
| B-6 | 맺는 줄 없는 첫 턴만 있는 대화 | 드로어에 나온다(`broken`) | N-9 |
| B-7 | SP 표지 0 일 때 화면 | 순서 그대로 · 표지 0 · 문구 0 · 「앱 판정」 과 장부로만 | 검수(`review-spec-001-v071.md`) N-4 가 앱 몫으로 넘겼고 결정 행이 없다 — 문구를 짓지 않는 쪽 |
| B-8 | SP 표지의 화면 꼴 | `data-site-prefer` + 빈 자리 `mark-site-prefer` · 안정 정렬로 앞에 | 규칙 ① 「우선 표시 표지로 앞에」 — 문구는 사용자 |
| **B-9** | **걷기 · 답 키 쪽 SP**(SPEC-001 0.7.1 「SPEC-002 되적기 후보」 1 ~ 7 — 표지 행을 앞에 · 두 조회를 한 조회로 · 키 함수 · 시험 세트 · trace) | **이 WORK 에 없다** — 걷기 코드는 안 고치고 SP-T4 로 「재료 표지가 틀린 말이 되지 않는다」 만 확인한다 | SPEC-002 가 아직 안 되적혔고(계약 없음) 지시서의 범위는 상담 0.3 이다. `_RESUME` §2 규칙 ① 은 「앱 걷기 · 키 같은 함수 · 실물 B · C」 를 함께 적었다 — **별도 발주가 필요하다**(코디 확인) |
| B-10 | 표에 없는 기존 시험 파일 | 워커는 안 돈다 | 사용자 「전체 안 돌림」 — 끝에 한 번 돌릴지는 코디 |
| B-11 | 가르기 판정 전 단계 신호 | 판정까지 붙든다 | TT5 「`understand` → `answer` 둘만」 을 지키려면 함께 띄운 걷기의 `search` 신호가 먼저 나가면 안 된다 |
| B-12 | 되적기 후보(SPEC-006 0.1.1 — 코디) | ST3 「셋」 → 넷(§8) · FD2 · FD7(W-1) · FD6(W-2) · TW6 · TW7(W-3) · EM1 `safety`(W-5) · S6-T2(W-6) · TT1(W-7) · CS5(W-8) · SV3 색인(W-11) · §11-3 수(W-12) · LS4-1 「130」 → 107 · SP 절(§12) · FD8 보류 | — |

## 18. SPEC-006 절 ↔ WP 대응(미대응 0)

| SPEC-006 | 규칙 | WP(절) |
|---|---|---|
| §2-1 | TK1 · TK2 · TK3 · TK4 · TK5 · TK6 · TK7 | WP-3(§7) · TK7 의 JSON 키는 WP-2(§9) |
| §2-2 | TW1 · TW2 · TW3 · TW4 · TW5 · TW6 · TW7 · TW8 | WP-3(§7 · §8) |
| §2-3 | TT1 · TT2 · TT3 · TT4 · TT5 · TT6 | WP-3(§7) · TT3 의 절 `turn` 은 WP-2 |
| §3-1 | VO1 · VO2 · VO3 · VO4 · VO5 · VO6 · VO7 · VO8 · VO9 · VO10 | WP-2(§9) — VO6 은 새 코드 0(꼬리 → `material.new_lines[]` 그대로) |
| §3-2 | `system_v3` 열세 절 | WP-2(§9) |
| §3-3 | `jev_state.turn_kind` · `kind_labels` · `voice_check` · `turn_headers.close` · `prev` · 빼는 칸 | WP-2(§9) |
| §4 | CS1 · CS2 · CS3 · CS4 · CS5 · CS6 | WP-4(§10) |
| §4 | CS7 | WP-5(§11) |
| §5-1 | EM1 · EM2 · EM3 · EM4 · EM5 · EM6 | WP-4(§10) |
| §5-2 | 종료 상태별 말 | WP-2(§9 절 `material`) |
| §6 | LS1 · LS2 · LS3 · LS4 · LS4-1 · LS5 · LS6 · LS7 · LS8 | WP-6(§12) |
| §7 | FD1 · FD2 · FD3 · FD4 · FD5 · FD6 · FD7 · FD9 · FD10 · FD11 | WP-7(§13) |
| §7 | **FD8** | **보류 — 구현 없음**(U6-4 · §17 O-1) |
| §8 | FX1 · FX2 · FX3 · FX4 | WP-5(§11) · 시작 줄 `consult_rev` 는 WP-0(§6) |
| §8A | SV1 · SV2 · SV3 · SV4 · SV5 · SV6 · SV7 · SV8 · SV9 · SV10 · SV11 | WP-1(§6a) |
| §9 | SPEC-004 · 005 위에 얹는 표 | 각 WP(행마다 위 규칙) · 끈 상태 = 0.1 그대로는 WP-2 · WP-3 의 기존 시험 |
| §10-1 | 장부 칸(`consult_rev` · `turn_kind` · `follow_target` · `empty` · `close` · `voice` · `viewing` · `list.hidden` · `modality_level` · `sites.dots[].concern_codes`) | WP-0 · WP-3 · WP-4 · WP-2 · WP-7 · WP-6 — `sites.chips[]` 는 보류 |
| §10-2 | 설정 여섯 | WP-0(§6) |
| §11-1 | S6-T1 ~ T7 · T25 | WP-3 |
| §11-1 | S6-T8 · T9 · T22 | WP-2 |
| §11-1 | S6-T10 · T11 · T14 | WP-4 |
| §11-1 | S6-T12 · T13 · T21 | WP-5 |
| §11-1 | S6-T15 · T16 · T26 | WP-6(+ SP-T1 ~ T4) |
| §11-1 | S6-T17 · T18 · T19 | WP-7 |
| §11-1 | **S6-T20** | **보류**(U6-4) |
| §11-1 | S6-T23 | 새 템플릿 · 코드를 지은 WP 마다(그 WP 의 새 시험 파일 안에 grep 한 꼴) |
| §11-1 | S6-T24 | §15(달리 받음 — WP 별 기존 파일) |
| §11-1 | S6-T27 · T28 · T29 | WP-1 |
| §11-2 | E6-0 | WP-7 |
| §11-2 | E6-1 · E6-2 · E6-3 · E6-4 · E6-5 | WP-8(§14) |
| §11-2 | E6-6 | 코디 · 사용자(§14) |
| §11-3 | 실물 대화 셋 12 턴 | WP-8(§14 — W-12 로 고친 기대) |
| §11-4 | 끝 조건 | §19 |
| §12 | U6-1 ~ U6-4 · C6-1 ~ C6-13 · O6-1 ~ O6-13 | §3 · §8 · §17 |
| (SPEC-001 0.7.1) | SP1 ~ SP8 의 앱 몫 · `site_mode` · `site_applied` · `site_prefer` · `n_site_prefer` | WP-6(§12 SP) · §4 |

## 19. 완료 조건

1. **단위 시험**: S6-T1 ~ T19 · T21 ~ T23 · T25 ~ T29 + SP-T1 ~ T4 통과(S6-T20 은 보류 · S6-T24 는 §15 꼴). WP 마다 「돌린 파일 목록 · 통과 수 · 고친 기존 시험 이름」 이 보고에 있다. **전체 pytest 를 돌리지 않았다.** `ruff` 는 고친 파일에 통과.
2. **함께 쓰는 코드**: `walk/front.py` · `columns/col_b.py` 의 고친 줄 수가 보고에 있고, §8 의 기존 다섯 파일이 **안 고친 채** 통과한다.
3. **안 고친 것**: `_face.svg` · `face_coords.py` 의 sha 가 WP-0 때와 같다 · 허브 레포 변경 0 · 0.1 · 수정 1 시험 파일 변경 0.
4. **문구**: 새 템플릿 · `consult/` 새 코드에 한글 문장 0(S6-T23) · 지은 화면 문구 0(`slots` 의 「{name} 계열 시술」 하나가 전부).
5. **실물**: E6-0 의 결과 · E6-1 ~ E6-5 의 값이 보고에 있다 — ① 허브 0.7.1 전 판(A1 ~ A4)과 ② 코디 알림 뒤 판(SPEC §11-3 표의 턴마다 실제 값 · SP 실물의 `site_applied` · 표지 수)을 **갈라** 적는다.
6. **포트**: 워커가 띄운 18223 을 내렸다 · 18105 · 18222 를 건드리지 않았다.
7. **코디 · 사용자**: 18105 를 0.7.1 로 다시 띄움 → 18222 → E6-6(사용자 확인).

## 변경 기록

### 0.1.0 (2026-11-17) — 처음 씀

- SPEC-006 0.1.0 의 A1 ~ A8 을 WP-0 ~ WP-8 로 나눔(대응표 §18 · FD8 · S6-T20 은 U6-4 보류).
- 코디 값 W-1 ~ W-8 · W-11 · W-12 · 사용자 W-9 (a) · W-10 「○○ 계열 시술」 · U6-1 ~ 3 (a) · A8 반영(§3 · §16).
- SPEC-001 0.7.1 칸(`descended[]` · `sites[]` · `matched.how` · `site_mode` · `site_applied` · `site_prefer` · `n_site_prefer`)을 앱이 읽는 곳(§4) · 규칙 ① 의 상담 쪽(§12 SP — 표지 0 일 때 포함).
- 시험 규칙(WP 마다 그 WP 시험 파일만 · 전체 pytest 금지 · 돌린 파일 목록 보고)을 §2 · §15 · WP 절마다.
- 이 워커가 정한 값 B-1 ~ B-12(§17-2) — 특히 **B-9: 걷기 · 답 키 쪽 SP 는 이 WORK 에 없다(별도 발주 필요)**.
