---
type: work
id: WORK-012
title: "앱 상담 채팅 0.2 구현 계획 — 상담 객체 · 걸린 선택지 · 거둠 · 객체 기준 조회 · 빈 칸 하나 = 질문 하나 · 시너지 먼저(같은 날 제약 표지) · `list` 묶음 셋 · `CHAT_STATE` 손잡이 · 실물 E5-1 ~ E5-5"
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
    - "orchestration/work/phub-gold-jev/SPEC-005-consult-state.md (0.1.0 · 검수 PASS — FAIL 0 · WARN 9 · NOTE 10 · review-spec-005.md) ← 계약"
    - "orchestration/work/phub-gold-jev/SPEC-004-consult-chat.md (0.1.0 — 이 판이 얹는 계약 · 고치지 않는다)"
    - "orchestration/work/phub-gold-jev/SPEC-001-hub-gold-mcp.md (0.6.0 — §4-1 · §4-2 · §4-4 · §4-5 · §4-6 · 0.7 의 고민 부위 칸은 별도 발주)"
    - "orchestration/work/phub-gold-jev/SPEC-002-chat-eval.md (0.6.0 — 걷기 · 재료 · 종료 상태는 그대로 쓴다)"
  decisions:
    - "orchestration/work/phub-gold-jev/_RESUME.md §2 (2026-11-17 「0.2 까지 진행 — U5-1~U5-5 = 추천(U5-4 (a1) 표지만)」 · 「SPEC-005 검수 뒤 코디(W-1~W-9)」 · 「얼굴 SVG 는 사용자가 직접 바꿈」(같은 행) · 「0.2 = 상담 객체 제안대로」 · 「0.2 설계 방향(사용자)」 · 「상담 초반부 흐름(사용자 · 0.2 재료)」 · 「WORK-011 B 코디 답」 · 「상담 프롬프트 = JSON 으로 불러옴」 · 「Procedure Hub 데이터는 공개 정보」)"
    - "orchestration/work/phub-gold-jev/work-chat-v02-instructions.md (이 문서의 지시서)"
  related:
    - "orchestration/work/phub-gold-jev/review-spec-005.md (WARN 9 · NOTE 10 — 이 문서 §16)"
    - "orchestration/work/phub-gold-jev/WORK-011-consult-chat.md (0.1 계획 — 공통 규칙의 꼴)"
    - "orchestration/work/phub-gold-jev/impl-chat-app-report.md · review-code-chat-app.md · app-chat-fix1-instructions.md (0.1 구현 · 검수 · 수정 1)"
---

# WORK-012 — 앱 상담 채팅 0.2 구현 계획: 상담 객체

> 경로 접두어: `W` = 이 폴더 · `APP-WT` = `~/orca/workspaces/clinic_chat/phub-gold-jev`(브랜치 `kknaksss/phub-gold-jev` · HEAD `6303e18` 위에 **0.1 미커밋 + 수정 1 진행 중** — 그 위에 이어서 짓는다).
> **계약은 SPEC-005 0.1.0 이다.** 이 문서는 「어느 파일을 · 어떤 순서로 · 무엇으로 확인하나」 만 정한다. SPEC 과 다르게 받는 곳은 §3 의 결정 행(U5 · 코디 W-1 ~ W-9)과 §17 B 표에 적은 것뿐이다. 그 밖에 SPEC 과 어긋나는 것을 만나면 코드를 맞춰 고치지 말고 보고한다.
> **화면 문구 · 답 문구를 짓지 않는다**(SPEC-004 ST4 · SPEC-005 SC6). 프롬프트 절은 SPEC §6-3 의 「담을 뜻」 을 옮긴 **초안**이고 확정은 사용자다.
> 이 문서의 줄 번호는 11-17 작업 트리(수정 1 이 도는 중)에서 본 것이다 — **수정 1 이 끝나면 밀린다.** WP-0 이 다시 확인한다.
> Procedure Hub 데이터(코드 · 이름 · 행 수)는 공개 정보다(`_RESUME` §2 11-17). 비밀값 · 키 · 내부 주소는 그대로 금지.

## 0. 요약

- 0.2 는 0.1 위에 **얹는다.** 새 모듈 넷(`consult/state.py` · `plan.py` · `blanks.py` · `synergy.py`) + 0.1 모듈 여덟의 고치는 곳 + 함께 쓰는 코드 두 파일의 몇 줄(인자는 안 는다 — ST3).
- 손잡이 `CHAT_STATE`: **끈 상태 = 0.1 그대로**(수정 1 뒤의 동작 · 시험 전부 통과) · 켠 상태에서 달라지는 것은 §4 의 목록이 전부다.
- **첫 WP 는 수정 1 이 끝난 코드 위에서 시작한다** — 코디가 발주 때 알린다. 그 전에는 시작하지 않는다(같은 워크트리 · 직렬).
- WP 열: **WP-0** 시작 확인 · 기준선 · 손잡이 → **WP-1** 객체 · 갱신 · 장부 → **WP-2** 걸린 선택지 · 거둠(함께 쓰는 코드) → **WP-3** 객체 기준 조회 → **WP-4** 빈 칸 · `ask` · 프롬프트 절 → **WP-5** 시너지 · 같은 날 제약 표지 → **WP-6** `list` 조각 · 표지 → **WP-7** 예시 셋 · 끈 상태 대조 · 전체 검증 → **WP-8** 실물 E5-1 ~ E5-4 · README → **코디** 18222 · 사용자 E5-5.
- **허브는 고치지 않는다**(새 도구 · 칸 0 — SPEC §3-3). 고민 부위 칸(SPEC-001 0.7)이 없으면 점 0 으로 도는 것은 0.1 그대로다(§2).
- **얼굴 SVG · 좌표표는 사용자가 직접 바꾼다** — 이 WORK 는 `_face.svg` · `face_coords.py` 를 고치지 않는다(§2).

## 1. 지금 코드(11-17 확인 — `APP-WT` 작업 트리 · 수정 1 진행 중)

| 파일 | 지금(0.1 + 수정 1 도중) | 0.2 에서 |
|---|---|---|
| `clinic_chat/consult/turn.py`(158줄) | `run_turn` — 든 후보(`:82`) → `walk(question, d, carry=…, instr=prompt.jev_front)`(`:84`) → 재료 `renumber`(`:99`) → 크기 판정(`:101`) → `list` · `sites`(`:107-116`) → 실행기(`:119-120`) → 맺는 줄(`:142-158`) | L2 · L4 · L5 · L7 을 끼운다(§5). `CHAT_STATE` 가 꺼지면 지금 길 그대로 |
| `clinic_chat/consult/carry.py`(31줄) | `candidates(turns, n_turns)` → `{table, code, name, from_turn}` | 걸린 선택지를 같은 꼴 + `origin` 칸으로 뒤에 붙이는 함수 하나(WP-2) |
| `clinic_chat/consult/ledger.py`(178줄) | `Conv`(`sent` · `summaries` · `next_n` · `last_list` · `last_sites`) · 시작 줄(`:125-133`) · 맺는 줄 반영 `_apply_end`(`:142-167` — `error` 가 없을 때만 재료를 센다) | `Conv.consult`(객체) · 시작 줄에 `consult_state` · `_apply_end` 가 성공 줄의 `consult.after` 로 객체를 세운다(WP-1) |
| `clinic_chat/consult/material.py`(229줄) | `renumber` · 목록 요약 줄 `summaries`(`:71-130`) · `summary_key`(`:133`) · `judgement_of`(`:211`) · `message`(`:217`) | 객체 조회의 요약 줄(QY3 선택지 · SY4 시너지)을 같은 번호 줄기에 붙이는 함수 · 「앱 판정」 에 `consult` · `ask` · `synergy_lines`(WP-3 ~ WP-5) |
| `clinic_chat/consult/listing.py`(88줄) | `build_list(reads, names)` → `{concerns[{…, modalities[{modality_name, procedures[]}], modality_only[], unreached[]}]}` | 묶음 ① · ③ 을 더한 꼴 · 관심 · 시너지 표지 · 계열 코드(WP-6 — 켠 상태에서만 더한다) |
| `clinic_chat/consult/prompt.py`(107줄) | `SECTION_IDS` 다섯 고정 검사(`:15` · `:55`) · `JEV_KEYS`(`:16`) · `HEADER_KEYS`(`:17`) · `ConsultPrompt` | 0.2 키의 꼴 검사 · 켠 / 끈 상태의 시스템 글 둘(WP-4 — §9a) |
| `clinic_chat/consult/sites.py`(69줄) | `from_response`(`:18`) · `place`(`:44`) · `SITES_FIELD`(`:14` 임시 이름) | **안 고친다** — `from_response` · `place` 를 부르기만(점 기준 = `focus` 고민) |
| `clinic_chat/consult/server.py` · `render.py` · `templates/partials/list.html` · `static/consult.css` | `/` → `303 /c/<id>`(수정 1) · 다시 그리기 = `last_list()` · `last_sites()` | 되읽은 화면이 객체 기준 조각을 그린다 · 새 `data-slot` 다섯(+ 하나 — §3 U5-4) · 표지 스타일(토큰만) |
| `clinic_chat/consult/steps.py` · `prompts/consult.json` 의 `steps` | **수정 1 이 짓는 중**(단계 문구 넷) | 안 고친다 — 객체 기준 조회(L5)는 수정 1 의 「찾기」 단계 안에서 돈다(새 단계 · 새 문구 0) |
| `clinic_chat/consult/templates/_face.svg` · `consult/face_coords.py`(· 수정 1 의 변환 스크립트가 있으면 그것) | 수정 1 · 사용자 | **안 고친다**(§2) |
| `clinic_chat/walk/front.py`(435줄) | `front(…, carry, instr)`(`:197`) — 든 후보를 resolve 후보 뒤에(`:223-228`) · 후보 설명(`:236-240`) · yes 만 `carried`(`:263-274`) · 이번 글 후보 0 이고 든 후보 yes 면 그것으로(`:276-278`) · 아니면 입구 고르기(`:279-`) | 든 후보 항목의 `origin` 을 후보 설명 · `out.carried[]` 로 **넘기는 줄만**(WP-2 — 인자 0) |
| `clinic_chat/walk/jev_requests.py`(98줄) | `_target_instr`(`:64-68` — `carried_from` 이 있으면 `target_carried`) · `ask_front`(`:71`) · `ask_nouls`(`:37`) | `_target_instr` 에 걸린 선택지 가지 하나(WP-2). `ask_nouls` 는 거둠 Noul 이 **부르기만** 한다 |
| `clinic_chat/columns/col_b.py` · `walk/calls.py`(`Call` `:73` · `followup_calls` `:378`) · `walk/breadth.py`(`Read` `:39` · `read_calls` `:61`) · `walk/material.py` · `walk/gate.py` · `clients/hub_rest.py`(`scope` `:186` · `facets` `:192` · `concern_candidates` `:195` · `pair` `:198` · `read_all` `:138`) | 그대로 | **안 고친다** — 객체 기준 조회가 부르기만 한다 |
| `clinic_chat/config.py` | `chat_*` 칸 11(`:69-79`) | 칸 넷(§6 WP-0) |
| `prompts/consult.json`(84줄 + 수정 1 의 `steps`) | `version` `0.1.0-draft` · `system` 다섯 절 · `jev_front` 넷 · `turn_headers` 넷 · `tail_marker` | 키를 **더한다**(`system` 다섯 절의 글자는 안 바꾼다 — §9a) |
| `tests/` | `test_consult_*.py` 아홉 · `consult_fixture.py` · `fake_hub.py` · `fake_jev.py` · `fake_cli/` | 새 `tests/test_state_*.py` · `state_fixture.py` · 가짜는 **더하기만** |

기준선: 0.1 코드 검수 때 `uv run pytest -q` = 282 passed · 1 skipped(`_RESUME` §5). **수정 1 이 시험을 더하므로 WP-0 이 다시 센다.**

## 2. 공통

| 항목 | 이번 판 |
|---|---|
| 시작 조건 | **수정 1 이 끝나고 코디가 알린 뒤**(`_RESUME` §2 11-17 「0.2 까지 진행 … 구현은 수정 1 뒤(같은 앱 워크트리 · 직렬)」). 수정 1 의 미커밋 변경 위에 이어 짓는다 — 되돌리거나 다시 쓰지 않는다 |
| allowed_paths(앱) | 새로: `clinic_chat/consult/{state,plan,blanks,synergy,e5}.py` · `consult/templates/partials/` 의 새 조각 · `tests/test_state_*.py` · `tests/state_fixture.py`. 고침: `consult/{turn,ledger,carry,material,listing,prompt,render,server,probe}.py` · `consult/templates/partials/list.html` · `consult/static/consult.css`(표지 — `--ms-*` 토큰만) · `clinic_chat/config.py`(칸 더하기만) · `clinic_chat/walk/front.py` · `walk/jev_requests.py`(§8 의 줄만) · `prompts/consult.json` · `.env.example`(이름만) · `README.md`(상담 절) · `tests/fake_hub.py` · `fake_jev.py` · `consult_fixture.py`(더하기만) |
| **고치지 않는 것** | **`consult/templates/_face.svg` · `consult/face_coords.py` · 수정 1 의 얼굴 변환 스크립트(있으면)**(사용자가 직접 바꾼다 — 이 판은 좌표표의 **꼴과 키**(`FACE_COORDS[site_code] → {shape, points}` · `DOT_SHAPES`)만 `sites.place()` 를 통해 쓴다) · `consult/sites.py` · `consult/steps.py` · `consult.json` 의 `steps` · 0.1 의 고치지 않는 것 전부(`clinic_chat/web/**` · `llm/**` · `columns/**` · `walk/material.py` · `walk/gate.py` · `walk/calls.py` · `walk/breadth.py` · `prompts/*.md` · `prompts/jev/*.md`) · **0.1 · 수정 1 의 시험 파일**(`tests/test_consult_*.py` · 그 밖 `tests/test_*.py`) |
| allowed_paths(허브) | **없음** — 읽기만 |
| 허브 부위 칸 | SPEC-001 0.7 의 고민 부위 칸이 **없으면 점 0 · 라벨 0 으로 오류 없이 돈다**(0.1 그대로 — `sites.from_response`). 그때 `concern_sites[]` 는 빈 목록이고 BK4 는 서지 않는다. 다른 길(이름 맞춤 · silver CSV)로 메우지 않는다. 단위 시험은 가짜 허브에 임시 이름으로 실어 본다(0.1 T25 꼴) |
| 포트 | **워커 18223**(차 있으면 `lsof` 로 빈 포트) — 띄워 확인한 뒤 스스로 내린다 · **18222 는 코디**(사용자 e2e) · **18105(허브)는 HTTP 읽기만**(띄우기 · 내리기 · 다시 띄우기 금지) · 18220 · 18210 · 18005 · 18432 는 건드리지 않는다 |
| 외부 호출 | 단위 시험은 전부 가짜(CLI · 허브 · Jev). 실물은 WP-8 뿐(허브 읽기 · Jev · 구독 CLI). 환경 파일을 열거나 고치지 않는다(없으면 「못 돌림」 → 코디). 키는 env 이름만 |
| 문구 | 새 템플릿 조각 · `consult/` 새 코드에 사람에게 보일 문장 0(`data-slot` 자리만 — S5-T14). 예외는 0.1 과 같다: 실측 입력 글(`consult/e5.py` — §14) · 시험 자료 |
| 검증 | 단계마다 그 WP 의 시험만(`uv run ruff check .` · `uv run pytest tests/test_state_<이 WP>.py -q`). 함께 쓰는 코드를 고치는 **WP-2** 만 걷기 시험 묶음을 함께 돈다. **전체 `uv run pytest -q` 는 WP-7 에 한 번** |
| 커밋 | 워커는 커밋 · push · PR 을 하지 않는다(코디 몫) |

## 3. 정해진 값 — 사용자 결정 U5 · 코디 W(`_RESUME` §2 11-17 행 그대로)

### 3-1. U5-1 ~ U5-5 = 추천

| # | 결정 | 이 문서 |
|---|---|---|
| U5-1 | **(가)** 허브 맞춤 + Jev Noul + 걸린 선택지. LLM 구조화 출력은 안 한다(`--json-schema` 0) | §7 · §8 |
| U5-2 | **(a)** 관심 대상과 고민이 **둘 다** 잡혔을 때 시너지(SY1 그대로) | §11 |
| U5-3 | **(a)** 리스트 칸 안 묶음 + 리스트 안 상대에 표지 · LLM 은 리스트 안 상대만 짧게 · 리스트 밖 상대는 수와 이름만. 묶음 ①(관심 대상)도 리스트 칸에 새로 생긴다(검수 N-7 — 코디가 사용자에게 함께 알린다) | §11 · §12 |
| U5-4 | **(a1) 표지만** — 보완 줄에 「같은 날 제약 있음」 표지. **회피 · 불가 행의 내용은 물을 때**(걷기가 읽는다). 안전 본문을 먼저 싣는 것 0 | 아래 · §11 |
| U5-5 | **(a)** `g_pair` 보완만 — 패키지는 물을 때(SY8 그대로) | §11 |

**U5-4 (a1) — 표지를 세우는 조회 하나를 어디에 두나.**

| 무엇 | 정한 것 |
|---|---|
| 조회 | `consult/synergy.py` 가 QY4(`pair(a, classes = [보완])`)와 **같은 때에** 조회 하나를 더 부른다 — **QY4b** = `pair(a = 같은 대상, classes = [회피, 간격, 순서])` · `b` 없음 · 쪽 넘김 끝까지 · 대상마다 한 번(QY4 와 같은 `shown.synergy[]` 조건) |
| 왜 그 갈래 셋 | `g_pair` 904 행 가운데 「회피」 갈래 21 행 + `same_day` = 「불가」 25 행이 놓인 갈래가 **회피 19 · 간격 4 · 순서 2** 다(이 워커 재셈 11-17 · `$SM/gold/g_pair.csv`). `pair` 에 `same_day` 거르개가 없으므로(SPEC-001 §4-6 — 거르개는 `classes`) 그 세 갈래를 읽어 앱이 가른다 |
| 앱이 보는 것 | QY4b 의 행에서 **상대 키(표 · 코드)와 두 값만**: `question_class` = 「회피」 인가 · `same_day` = 「불가」 인가. 둘 가운데 하나라도 참인 행이 있는 상대 = 표지 `same_day_caution: true` |
| **싣지 않는 것** | QY4b 의 행은 **LLM 재료에 한 줄도 안 간다** · 「실은 gid」 · `shown.info[]` 에 안 든다 · 화면에 값(글 · 간격 · 사유)을 그리지 않는다. 장부에는 조회 기록(`consult.queries[]` — `rule: "QY4b"` · `total` · `ms`)과 표지를 세운 근거 `gids[]` 만 남긴다(되짚기용 — SPEC-004 AP5 와 같은 뜻) |
| 표지가 가는 곳 | ① 그 상대의 시너지 요약 줄(SY4)에 `same_day_caution: true` ② 화면 묶음 ③ 의 그 상대 · 리스트 안 표지에 `data-caution` ③ 빈 자리 `mark-caution`(문구는 사용자 — 앱은 짓지 않는다). 리스트 **밖** 상대(이름만 보이는 것)에도 ② 를 단다 |
| 프롬프트 | 절 `synergy` 에 한 줄(초안 낱말): 표지가 있는 줄은 「같은 날 제약이 있다 — 물으면 알려 준다」 까지만 · 제약의 내용을 짓지 않는다 · 그 줄에 `same_day` 값이 「가능」 으로 실려 있어도 「가능」 만 말하지 않는다(검수 W-5 ② — `M2`×`M8` 꼴) |
| 손님이 물으면 | 걷기가 그 턴에 `avoid` · `same_day` · `order_interval` 종류로 읽는다(0.1 그대로) — 객체는 시키지 않는다(QY6) |
| 바뀌는 SPEC 규칙 | SY6 · QY4 · QY6 의 「시너지 조회는 `classes = [보완]` 뿐」 → 「**재료로 싣는** 조회는 보완뿐 · 표지용 조회 QY4b 하나가 더 있다」 · S5-T8 「안전 종류 조회 0 번」 → 「안전 종류의 **재료** 0 줄(QY4b 는 표지용 — 재료 0)」 · S5-T11 「`classes` = [보완] 로만 부른다」 → 「QY4 는 보완만 · QY4b 는 세 갈래 · QY4b 의 행이 메시지에 0」(§18 · 되적기 후보 §17 B-12) |
| 양(재셈) | `PRD-416` 의 세 갈래 = 순서 22 · 간격 21 · 회피 2 = 45 행 · 표지가 서는 리스트 안 상대 = 6 가운데 2(`M7` · `M8` — 검수 W-5 ①) |

### 3-2. 코디 W-1 ~ W-9(검수 뒤 — 한 줄씩)

| # | 코디가 정한 것(`_RESUME` 행 그대로) | 이 문서 |
|---|---|---|
| **W-1** | `guess` 는 **사이 값(`uncertain_kept`)만** · no 문턱 아래 `named`(우연 일치 — 「고민입니다」 의 입 등)는 **객체에 안 넣는다**(trace 에만) | §7 · S5-T2 · S5-T17 |
| **W-2** | NQ5 = 앞 턴 `ask` 에 답 안 했으면(걸린 선택지 yes 0) 이번 턴은 묻지 않는다(**새 항목 무관**) · NQ4 는 「모두 두 번까지」 한 꼴 · 예시 고침 | §10 · §13(고친 예시) |
| **W-3** | 계열 대상은 **계열 묶음 머리**에 표지(시술 행엔 안 단다) | §12 · S5-T12 · §13 |
| **W-4** | 같은 턴 동률: BK3 · BK4 가 서면 BK1 은 그 턴 빈 칸이 아니다 · BK3 과 BK4 는 **선택지가 적은 쪽** | §10 · S5-T9 |
| **W-6** | 세 종료 상태(범위 밖 · 입구 없음 · 실행 중단) 턴 = **객체 갱신은 하되 `list` 는 안 보낸다** · SPEC-004 T1 ~ T18 은 **끈 상태**에서 | §5 · §4 · S5-T18 |
| **W-7** | 끈 상태의 시스템 글 = **0.1 그대로** · 로더 검사 변경은 SPEC §9 되적기 | §9a · S5-T15 · S5-T19 |
| **W-8** | 걸린 선택지가 전부 yes 가 아니면 **CR6 뒷절대로 입구 고르기** | §8 · S5-T3 |
| **W-9** | `wishes[]` 는 **조회를 일으키지 않는다**(요약으로만 LLM 에) | §9 · S5-T8 |

(W-5 는 사용자 결정 U5-4 로 닫혔다 — §3-1.)

## 4. `CHAT_STATE` — 끈 상태 · 켠 상태

**끈 상태(`CHAT_STATE=off`) = 0.1 그대로.** 수정 1 이 끝난 코드의 동작 · 이벤트 · LLM 메시지와 같다. SPEC-004 T1 ~ T18 · WORK-011 T19 ~ T26 · 수정 1 이 더한 시험이 **이 상태에서 전부 통과**한다(코디 W-6). 기본값은 SPEC §10-2 대로 `on` 이므로, 0.1 · 수정 1 의 시험 설정(`conftest.make_settings` · `consult_fixture`)이 이 칸을 어떻게 받는지 WP-0 이 확인한다 — 기존 시험 파일은 고치지 않는다(§17 B-1).

| 끈 상태에서 같은 것 | 어떻게 지키나 |
|---|---|
| 시스템 글 | `system` 다섯 절을 이어 붙인 글이 0.1 과 **글자 그대로** 같다 — 0.2 의 절은 `system` 을 고치지 않고 새 키에 둔다(§9a · W-7) |
| 턴 메시지 · 이벤트 순서 · 조각 | `turn.py` 의 0.2 가지를 한 군데 스위치 뒤에 둔다 — 꺼지면 지금 줄 그대로 돈다 |
| 장부 | 0.1 의 칸 그대로 + 시작 줄의 `consult_state: "off"` 하나. `consult` 칸은 없다. 다만 `prompts` 의 sha 는 JSON 파일이 바뀌어 0.1 때와 값이 다르다(S5-T15 의 대조에서 sha · 시각 · id 는 뺀다) |
| 함께 쓰는 코드 | `origin` 칸을 안 주면 `front()` 결과 · trace 가 지금과 같다(0.1 T13 그대로) |

**켠 상태에서 달라지는 것(전부):**

| # | 무엇 | 0.1 | 켠 0.2 | SPEC |
|---|---|---|---|---|
| 1 | 후보 | 이번 글 + 든 후보(앞 턴 대상) | + 걸린 선택지(앞 턴 `ask` 의 `options[]`) | UP4 |
| 2 | Jev 요청 | 걷기의 것 | + 거둠 요청 하나(객체에 항목이 있는 턴) · 걸린 선택지가 한 묶음(32)을 넘기면 대상 요청이 는다 · 걸린 선택지가 전부 떨어지면 입구 고르기 요청 | RV2 · UP4 · W-8 |
| 3 | 허브 조회 | 걷기의 것 | + 거둠용 `resolve` 하나(N-5) + 객체 기준 조회 QY1 ~ QY5 · QY4b + 상대의 리스트 안 · 밖 판정(§11 · B-6) | §3-3 |
| 4 | `list` 를 보내는 턴 | `concern_candidates` 를 읽은 턴 | 묶음 ① · ② · ③ 가운데 하나라도 바뀐 턴(세 종료 상태 턴은 안 보낸다 — W-6) | SC3 |
| 5 | `list` 조각의 안 | 고민마다 리스트 | 묶음 ① 관심 대상 · ② `focus` 고민의 리스트(+ 관심 · 시너지 · 제약 표지) · ③ 시너지 | SC2 · SC4 |
| 6 | `sites` 의 기준 | 이번 턴에 읽은 고민 | `focus` 고민의 `concern_sites[]` | SC5 |
| 7 | `first_list_ms` | 걷기 직후 | 걷기 + 객체 갱신 + 객체 기준 조회 뒤(여전히 첫 `delta` 보다 먼저) | §9 TF3 |
| 8 | 시스템 글 | 다섯 절 | + 절 셋(`consult` · `ask` · `synergy`) | §6-3 |
| 9 | 턴 메시지 | 앱 판정 → 자료 → 질문 | 앱 판정에 `consult` · `ask` · `synergy_lines` · 자료에 선택지 · 시너지 요약 줄 | §6-3 · SY4 |
| 10 | 답의 끝 | 되묻기(`offered`) | `ask` 가 있으면 그 하나를 묻는다 | NQ1 |
| 11 | 장부 | 0.1 칸 | + `consult{diff, after, blanks, ask, options_carried, retract, queries}` · `carried[]` 는 앞 턴 대상만(N-8) | §10-1 |
| 12 | 되읽기 | 재료 장부 · 마지막 리스트 | + 마지막 성공 줄의 `consult.after` 로 객체 | RV9 |
| 13 | 빈 자리 | 0.1 + 수정 1 | + `list-section-interest` · `list-section-synergy` · `list-synergy-outside` · `mark-interest` · `mark-guess` · `mark-caution` | SC6 · U5-4 |

켠 상태에서 0.1 시험이 걸릴 수 있는 곳(알고 가는 것 — 그 시험은 끈 상태의 것이다): T6(`list` 를 보내는 턴 — 위 4) · T12(Jev 요청 수 — 위 2).

## 5. 한 턴 루프 — `turn.py` 에 끼우는 자리(켠 상태)

SPEC §3-1 L1 ~ L9 를 지금 `run_turn` 의 줄에 놓는다. WP 마다 자기 몫의 자리를 채운다.

| L | 자리(지금 줄) | 켠 상태에서 | WP |
|---|---|---|---|
| L1 | `server.py` `post_turn` | 그대로. 시작 줄에 `consult_state` | WP-0 |
| L2 | `:82` 든 후보 | 든 후보(앞 턴 대상 — 장부 `targets[]` 그대로 · SPEC §9 의 CR 행) **뒤에** 걸린 선택지 | WP-2 |
| L3 | `:83-84` 걷기 | **같은 호출**(`walk(question, d, carry=…, instr=…)`). 거둠 요청을 걷기와 **함께** 띄운다(`asyncio.gather` — 걷기를 기다리게 하지 않는다) | WP-2 |
| L4 | 걷기 직후(`:85` 뒤) | `state.update(…)` → diff. **세 종료 상태 턴에도 한다**(W-6). `gold_hash` 가 바뀐 턴(`:95`)은 안 한다 | WP-1 |
| L5 | L4 뒤 · 크기 판정 앞 | `plan.run(…)` — 걷기가 읽지 않은 것만. **세 종료 상태 턴에는 안 한다**(그 턴에 필요해진 조회는 다음 턴이 따라잡는다 — §9) | WP-3 · WP-5 |
| L7 | L5 뒤 · 메시지 짓기 앞 | `blanks.pick(…)` → `ask`(메시지의 「앱 판정」 에 들어가므로 메시지보다 먼저 정한다) | WP-4 |
| — | `:99-106` 재료 · 크기 | 걷기 재료 뒤에 객체 조회의 요약 줄을 같은 번호 줄기로 · 크기 판정은 그 뒤(넘으면 0.1 대로 `FT5` — 그때 `ask` · 시너지 줄도 뺀다) | WP-3 ~ WP-5 |
| L6 | `:107-116` `list` · `sites` | 객체 기준으로 지은 조각 · 바뀐 것이 있을 때만 · 세 종료 상태 턴에는 안 보낸다 | WP-6 |
| L8 | `:119-120` 실행기 | 그대로(한 번) | — |
| L9 | `:142-158` 맺는 줄 | + `consult{…}` · `shown` · `asked` 는 `consult.after` 안 | WP-1 ~ WP-5 |

- **객체는 성공한 턴에만 선다**(RV9): `turn.py` 는 이번 턴의 객체를 **복사본**으로 지어 맺는 줄의 `consult.after` 에 적고, `ledger._apply_end` 가 `error` 가 없는 줄일 때만 `Conv.consult` 로 받는다(0.1 의 재료 셈과 같은 자리 — `ledger.py:154`). 오류 턴의 줄에도 `consult.diff` 는 적되 `not_counted: true` 를 단다(0.1 의 `material.not_counted` 꼴).
- Jev 는 L3 안(걷기)과 거둠 요청에서만 돈다. L4 ~ L7 은 결정론이다(외부 호출은 허브 읽기뿐).

## 6. WP-0 — 시작 확인 · 기준선 · 손잡이 ← **첫 WP(수정 1 뒤)**

**SPEC**: §10-2 · D5-13 · C5-11 · 검수 W-6 · W-7.
**하는 것**:

| 무엇 | 구현 |
|---|---|
| 시작 확인 | 코디의 「수정 1 끝」 알림을 받은 뒤 시작한다. `git -C <APP-WT> status --porcelain` 으로 수정 1 의 변경(`consult/steps.py` · `consult.json` 의 `steps` · `/` → 303)이 있는지 보고, **§1 표의 줄 번호를 다시 확인**해 다른 곳을 보고에 적는다 |
| 기준선 | `uv run pytest -q` 를 **한 번** — 통과 수를 보고에 적는다(WP-7 의 전체 검증이 그 수 + 새 시험이어야 한다) · 0.1 · 수정 1 시험 파일의 sha 목록을 떠 둔다(WP-7 이 「변경 0」 을 대조) · `_face.svg` · `face_coords.py` 의 sha 도 함께(S5-T22) |
| 설정 칸 | `config.py` 에 넷: `CHAT_STATE`(`on`) · `CHAT_ASK_MAX`(`2`) · `CHAT_SYNERGY`(`on`) · `CHAT_RETRACT`(`on`) — SPEC §10-2 그대로 · `.env.example` 에 이름만 |
| 스위치 | `turn.py` 에 켠 / 끈 가지의 자리 하나(아직 켠 가지는 비어 있다 — 꺼진 것과 같다) · 시작 줄에 `consult_state` |
| 대화의 상태는 시작 때 값으로 끝까지 | 대화 첫 턴의 `CHAT_STATE` 를 시작 줄에 적고 그 대화는 그 값으로 돈다(서버를 다시 띄워 값이 바뀌어도 — CLI 의 시스템 글이 첫 턴의 스냅숏이라 중간에 바꾸면 절과 메시지가 엇갈린다 · 0.1 실측 E1 ⑦). **시작 줄에 그 칸이 없는 대화(0.1 로 쓴 줄)는 끈 상태로 끝까지 돈다** — §17 B-2 |

**완료 조건**: 기준선 수 · sha 목록이 보고에 있다 · `CHAT_STATE=off` 와 `on`(빈 가지) 둘 다에서 기존 시험이 통과한다.
**검증**: `uv run ruff check .` · `uv run pytest -q`(기준선 — 이 WP 에서만 전체).

## 7. WP-1 — 객체 · 갱신 · 장부: `consult/state.py` · `ledger.py`

**SPEC**: §2(SL1 ~ SL6 · 칸 · 항목 꼴) · §3-2 UP1 ~ UP3 · UP6 ~ UP9 · §3-4 · §5 RV1 · RV5 ~ RV9 · §10-1 · 검수 W-1 · W-6 · N-6 · S5-T1 · T2 · T4 · T5 · T7 · T13.
**만들 것**: `clinic_chat/consult/state.py` · `ledger.py`(고침) · `tests/test_state_object.py` · `tests/state_fixture.py`.

| 규칙 | 구현 |
|---|---|
| SL1 · §2-2 | 객체 = JSON 으로 그대로 적히는 dict: `concerns[]` · `focus` · `sites[]` · `concern_sites[]` · `subjects[]` · `procedures[]` · `wishes[]` · `shown{lists, info, synergy}` · `asked[]`. 항목 = `{table, code, name, state, source{turn, how, matched, covered_by, noul, decision, from_ask}, history[]}`. `blanks[]` 는 저장하지 않고 턴마다 센다(WP-4) |
| **N-6** | `wishes[]` 의 정보 종류 항목은 `{kind, state, source, history}` 다((표, 코드) 꼴이 아니다 — 값은 SPEC-001 §5-8 의 14 종류 코드뿐 · S5-T1 이 닫힌 목록으로 검사) |
| UP1 | 재료는 **걷기 trace** 뿐: `w.front.trace_front["targets"]`(후보마다 `id` · `name` · `noul` · `decision` · `covered_by`) · `w.front.entries` · `w.front.carried[]` · `w.front.kinds`. 앱이 글에서 낱말을 따로 뽑지 않는다 |
| UP2 | 표 → 칸: `concern` → `concerns[]` · `site` → `sites[]` · `modality` · `procedure` · `procedure_case` · `product` → `subjects[]` · `effect` · `method` · `material` → `wishes[]`(값). 그 밖의 표는 넣지 않는다 |
| UP3 · **W-1** | 걷기 `decision` → 객체: **`target`** → `said` · **`uncertain_kept`** → `guess` · **`named`** → **안 넣는다**(trace 에만) · `dropped` · `overlap` → 안 넣는다 · **`carried`**(든 후보 · 걸린 선택지의 yes) → `said`(이미 있으면 UP6) |
| `wishes[]` 종류 | 이번 턴 걷기가 **읽기로 한 종류**(`trace_front.kinds[]` 의 `decision` = `read` 이고 `by` = `yes`) 가운데 §2-3 표가 바람으로 둔 것(`recovery` · `outcome`)만. 그 밖의 종류는 객체에 안 남긴다(§17 B-3) |
| UP6 | 같은 (표, 코드)는 새로 안 만들고 `history[]` 에 턴을 더한다 · `guess` → 다시 나옴 = `confirmed` · `said` → 다시 나옴 = `confirmed` · `withdrawn` → 다시 말함 = `said` |
| UP7 · RV5 · RV6 · RV7 | 윗고민과 하위 고민은 둘 다 둔다 · `focus` = 가장 최근에 `said` · `confirmed` 로 들어온(다시 말한) 고민 · 한 글에 둘이면 뒤에 나온 것(trace 후보의 `start` 로 가린다 — 같으면 허브 순서) · `focus` 를 거두면 남은 가장 최근 고민 · 없으면 `null` |
| RV1 | `guess` 는 조회 축이 아니다 — `focus` 가 안 되고 `plan` 이 축으로 안 쓴다(함수 하나 `state.axis_items()` 가 `said` · `confirmed` 만 낸다 — 다른 모듈은 그것만 쓴다) |
| UP8 | `procedures[]` · `concern_sites[]` 는 파생 — 근거 항목이 `withdrawn` 이면 빠진다(턴마다 다시 센다 · 채우는 것은 WP-3) |
| UP9 | diff = `[{op, slot, table, code, from, to, why}]` · `op` ∈ `add` · `state` · `withdraw` · `focus` · `shown` · `asked` · 없으면 빈 목록 |
| **W-6** | 종료 상태가 범위 밖 · 입구 없음 · 실행 중단인 턴에도 `update` 는 돈다(그 턴의 trace 에 확정된 것이 있으면 넣고 · 거둠도 받는다). 그 턴에 `list` · `sites` 는 안 보낸다(§5) |
| 장부 | 맺는 줄에 `consult{diff, after}`(나머지 칸은 뒤 WP 가 채운다) · `Conv.consult` · `_apply_end` 가 **`error` 없는 줄**의 `consult.after` 만 받는다 · 되읽기 = 그 대화 마지막 성공 줄(RV9) · 줄에 키 · 홈 경로 없음(0.1 LG5 그대로) |

**완료 조건**: S5-T1(칸 가르기 · 닫힌 목록 · `adverse` · `condition` · `offer` 없음) · S5-T2(확실함 — **`named` 는 객체에 없다** 포함) · S5-T4 의 객체 쪽(계열은 `procedures[]` 에 없다 — 채움은 WP-3) · S5-T5 · S5-T7 · S5-T13(되읽어 같은 객체 · 오류 턴의 diff 는 안 든다) · S5-T18(세 종료 상태 턴 — diff 가 있고 `list` 이벤트 0)이 가짜 셋으로 선다.
**검증**: `uv run pytest tests/test_state_object.py -q`.

## 8. WP-2 — 걸린 선택지 · 거둠: `carry.py` · `state.py` + 함께 쓰는 코드의 몇 줄

**SPEC**: §3-2 UP4 · UP5 · §5 RV2 ~ RV4 · RV8 · §9(ST3 · CR) · 검수 W-8 · N-5 · N-8 · S5-T3 · T6.
**고칠 곳(함께 쓰는 코드 — 인자 0 · 기본 동작 그대로)**: `clinic_chat/walk/front.py` · `clinic_chat/walk/jev_requests.py`.
**만들 것**: `consult/carry.py`(고침) · `state.py`(거둠) · `tests/test_state_carry.py`.

| 규칙 | 구현 |
|---|---|
| ST3 | `walk()` · `front()` 에 **인자를 더 열지 않는다.** 걸린 선택지는 `carry` 목록의 항목에 `origin: "option"` 칸을 달아 보낸다(SPEC §9 ST3 행) |
| UP4 | `carry.py` — 든 후보(앞 턴 대상 · 0.1 그대로 · **장부 `targets[]` 에서**) **뒤에** 걸린 선택지 = `asked[]` 의 **마지막 턴 것**(바로 앞 턴에 준 `ask` 의 `options[]`)을 `{table, code, name, from_turn, origin: "option"}` 로. 같은 (표, 코드)가 든 후보에 이미 있으면 다시 넣지 않는다(그때 그 항목에 `origin` 을 단다 — B-4) |
| `front.py`(약 3 줄) | 든 후보 dict 를 지을 때 `origin` 을 함께 든다(`:227`) · 후보 설명에 `origin` = `option` 이면 `carried_from` 대신 `option_from: <턴>` 을 싣는다(`:238-240`) · `out.carried[]` 의 줄에 `origin` 을 적는다(`:265`). `origin` 이 없으면 지금 글자 그대로다 |
| `jev_requests.py`(약 3 줄) | `_target_instr` — 후보 설명에 `option_from` 이 있고 지시에 `target_option` 절이 있으면 그 절 · 없으면 지금 길(`target_carried` → `target`) |
| yes 만 | 걸린 선택지도 든 후보와 같은 가지(`front.py:263-274`)를 탄다 — yes 만 대상(`by` = `carried`) · 사이 값 · no 는 `dropped` |
| **W-8** | 이번 글의 후보가 0 이고 걸린 선택지(와 든 후보)가 **전부 yes 가 아니면 입구 고르기**로 간다 — 지금 코드의 가지가 이미 그 길이다(`front.py:276-279` · SPEC-004 CR6 뒷절). 그 턴의 Jev 요청은 둘 이상이 된다(맨 앞 판단 + 입구 고르기) — 보고 · 장부에 수를 남긴다 |
| 묶음 | 후보가 한 묶음(`JEV_BATCH_SIZE` 32)을 넘으면 `ask_front` 가 나눠 묻는다(지금 동작) · `coverage` 도 노드가 64 를 넘으면 나뉜다(`hub_rest.py:207`) — 예시 ③ 의 선택지 40 이 그 꼴이다(E5-2 가 잰다) |
| UP5 | 걸린 선택지는 **한 턴만** 산다 — 다음 턴에 yes 가 없으면 `asked[].answered` = `false` 로 남고 후보에서 빠진다 |
| 객체에 드는 꼴 | yes 로 고른 선택지 = `said` · `source.how` = `option` · `from_ask` = 그 `ask` 의 턴 · `asked[].answered` = `true`. BK5(확인)의 선택지가 yes 면 그 `guess` 항목이 `confirmed`(UP6) |
| **N-8** | 장부 0.1 칸 `carried[]` 에는 **앞 턴 대상만**(`origin` 없는 것) · 걸린 선택지의 결과는 `consult.options_carried[{table, code, from_turn, noul, decision}]` 에만 |
| RV2 · **N-5** | 거둠 = `state.retract(…)` — 객체에 `said` · `confirmed` · `guess` 항목이 **하나라도 있는 턴에만**(`CHAT_RETRACT=on`). 상담 쪽이 `hub.resolve(question)` 을 **한 번 더** 부른다(걷기의 `resolve` 는 걷기 안에 있다 — 그래서 그 턴의 허브 조회가 하나 는다 · 「객체가 더하는 조회 0 ~ 3」 셈 **밖**) → 항목 = 객체의 항목 + 이번 글의 후보 가운데 객체 칸에 들 표의 것(UP2) → `jev_requests.ask_nouls(…)` 로 **요청 하나**(32 를 넘으면 묶음 수만큼) · 지시 = `jev_state.retract` |
| RV2 · RV3 | 거둠 Noul 이 yes 문턱 이상인 항목만: 객체에 있으면 `withdrawn` · 이번 글의 후보면 **객체에 넣지 않는다.** 사이 값 · no 는 그대로. 걷기가 그것을 읽는 것은 막지 않는다(O5-2) |
| 함께 띄움 | 거둠 요청은 걷기와 `asyncio.gather` 로 함께 — 걷기의 결과를 기다리지 않고 · 걷기를 기다리게 하지도 않는다. 시간 = `consult.retract_ms` |
| 거둠 요청이 실패하면 | 그 턴은 「거둠 0」 으로 계속 돈다(턴을 오류로 맺지 않는다) · `consult.retract_error{kind}` 를 적는다 — §17 B-5 |
| RV4 · RV8 | 확인 질문에 아니라고 답함 = RV2 의 길 · 대상을 거두면 `procedures[]` 에서 빠지고 화면 묶음 ③ 에서 빠진다(`shown.synergy[]` 는 기록으로 남는다) |

- Jev 지시의 색인 이름: `ask_nouls` 는 항목을 state 의 `candidates` 에 싣는다(`jev_requests.py:50`). SPEC §6-3 의 초안 낱말은 `items[j]` 라 적었으나 **구현은 `candidates[{i}]` 로 쓴다**(함께 쓰는 함수를 안 고치기 위해) — 프롬프트 초안이 그 이름을 쓴다.

**완료 조건**: S5-T3(글자 맞춤 0 인 답에서 선택지가 붙고 yes 만 `how` = `option` · 입구 고르기가 안 돈다 · 한 턴 뒤 빠진다 · **전부 떨어지면 입구 고르기가 돈다**(W-8) · `carried[]` 에 선택지가 안 섞인다(N-8)) · S5-T6(거둠 yes → `withdrawn` · 사이 값 그대로 · 이번 글의 이름이 거둠 yes 면 안 든다 · `focus` 를 거두면 남은 것으로) · S5-T20(`origin` 을 안 주면 `front()` 결과 · trace 가 지금과 같다 — 0.1 T13 그대로 통과) · **걷기 시험 묶음 전부 통과**.
**검증**: `uv run pytest tests/test_state_carry.py tests/test_consult_carry.py tests/test_walk_front.py tests/test_walk_core.py tests/test_covered.py tests/test_columns.py -q`.

## 9. WP-3 — 객체 기준 조회: `consult/plan.py`

**SPEC**: §3-3 QY1 ~ QY6 · §2-2(`concern_sites[]` · `procedures[]`) · §3-4 · 검수 W-9 · N-1 · S5-T4 · T8.
**만들 것**: `clinic_chat/consult/plan.py` · `material.py`(요약 줄) · `tests/test_state_plan.py`.

| 규칙 | 구현 |
|---|---|
| 조건의 꼴 | QY 의 「새로 듦」 을 **「객체에 있는데 아직 안 읽음」** 으로 짓는다(읽은 것 = `shown` · 대화 메모리의 조회 응답). 그래서 세 종료 상태 턴에 미뤄진 조회(§5) · 서버를 다시 띄운 뒤가 다음 턴에 저절로 따라잡힌다 |
| 걷기와 겹침 | 걷기가 이번 턴에 읽은 조회(`w.reads[].call.key()` — 도구 + 입력)는 다시 안 부르고 그 응답을 쓴다 → `consult.queries[]` 에 `skipped: "walk"` |
| QY1 · QY5 | `concern_candidates(concern_code = focus, site = sites[] 의 said · confirmed 가 있으면 그것)` — **걷기의 읽기 함수를 부르기만** 한다(`walk/breadth.read_calls` · `walk/calls.Call` · `followup_calls` — 고치지 않는다): 걷기와 같은 꼴의 `Read`(쪽 넘김 끝까지 + 후보별 profile 이어 조회)를 얻어 0.1 의 `build_list` · 목록 요약 줄(`material.summaries`)이 그대로 받는다. 상담 쪽의 `Verified` · 방문 장부를 **따로** 세운다(걷기의 것에 섞지 않는다 — gate 는 이미 끝났다) |
| `concern_sites[]` | QY1 응답 머리를 `sites.from_response` 로 읽는다(칸이 없으면 빈 목록 — §2) |
| QY2 | `scope(node = 대상)` → `procedures[]` = 시술 holder(시술 = 자기 · 케이스 · 제품 = 「물려받음」 의 시술) + `via{subject, scope_gid}` + 근거 항목의 `state`. **계열 대상은 넣지 않는다** |
| QY3 | 대상이 있고 `concerns[]` 에 `said` · `confirmed` 가 없을 때 `facets(node, facet = indication)`(기본 role) → 서로 다른 `concern_code` · 층(`layer.role`) = BK2 의 선택지. 하위 제품의 적응은 **넣지 않는다**(SPEC 그대로 · 검수 N-1 — §17 O 표) |
| QY4 · QY4b | WP-5 |
| **W-9** | **`wishes[]` 는 조회를 일으키지 않는다** — 그 턴의 걷기만 읽고, 뒤 턴에는 「앱 판정」 `consult.wishes` 의 요약으로만 LLM 에 간다 |
| QY6 | `plan` 이 내는 조회의 도구 · 입력을 닫힌 목록으로 검사한다: `adverse` · `contraindication` · `avoid` 재료 조회 0(QY4b 는 재료 0 인 표지용 — §3-1) |
| 요약 줄 | QY1 = 0.1 의 목록 요약 줄 그대로. QY3 = **선택지 하나에 한 줄** `{n, summary: true, option: true, concern_name, layer, holder, rows(수)}` + 장부 `{n, summary: true, key, rule: "QY3", gids[]}`(O5-8 을 여기서 고정 — 줄 번호는 0.1 과 같은 줄기 `next_n` · 같은 요약은 `Conv.summaries` 의 키로 다시 안 싣는다). **QY3 의 줄은 그 턴에 `ask` 가 BK2 로 나갈 때만 싣는다**(묻지 않는 턴에 선택지 40 줄을 싣지 않는다) |
| `shown.info[]` | 그 대상 × 종류의 줄을 실은 턴(걷기 재료 · 객체 조회 재료 모두) |
| 장부 | `consult.queries[{rule, tool, request, total, ms, skipped}]` |
| 단계 표시 | 객체 기준 조회는 수정 1 의 「찾기」 단계 안에서 돈다 — 새 단계 코드 · 새 문구 0 |

**완료 조건**: S5-T4(제품 → `procedures[]` 에 그 시술과 경유 · 계열은 없다 · 거두면 빠진다) · S5-T8(걷기가 읽은 조회는 `skipped: "walk"` · 대상만 있으면 QY3 · **`wishes[]` 만 바뀐 턴에 조회 0**(W-9) · 안전 종류 재료 0)이 선다.
**검증**: `uv run pytest tests/test_state_plan.py -q`.

## 9a. 프롬프트 JSON 을 어떻게 더하나(W-7) — WP-4 가 쓴다

| 무엇 | 정한 것 |
|---|---|
| `system` 다섯 절 | **글자를 안 바꾼다.** 끈 상태의 시스템 글 = 그 다섯 절을 이어 붙인 것 = 0.1 과 같다(W-7) |
| 새 키 `system_state` | `[{id, lines[]}]` — `id` ∈ `consult` · `ask` · `synergy`(이 순서). 켠 상태의 시스템 글 = `role` · `rules` · `screen` · **`consult` · `ask` · `synergy`** · `material` · `tail`(SPEC §6-3 의 자리 — `screen` 과 `material` 사이) |
| `rules` 6 번의 예외 구절 | `rules` 줄을 고치지 않고 **`synergy` 절의 한 줄**로 둔다(「6 번의 예외 — 시너지 줄은 묻지 않아도 짚는다 · 안전 정보는 그대로 물을 때만」 의 뜻). SPEC §6-3 은 「`rules` 한 줄에 구절」 이라 적었다 — W-7 을 지키려고 자리만 옮겼다(§17 B-7) |
| 그 밖의 새 키 | `jev_front.target_option`(영어) · `jev_state.retract`(영어) · `turn_headers.consult` |
| `version` | `0.2.0-draft` |
| 로더 | `prompt.py` — 0.1 키의 검사는 그대로 · 새 키는 **있으면** 꼴을 검사한다(절 `id` 셋 · 순서 · 빈 값 0). **켠 상태로 시작하는 대화**는 새 키가 다 있어야 한다(없으면 그 대화 시작 실패 — 오류 종류 `prompt`). `ConsultPrompt` 에 `system_text_state`(켠 글) · `jev_state` 를 더하고 `system_text`(끈 글)는 그대로 둔다. `tail_marker` 검사는 두 글 모두에 |
| 수정 1 의 키 | `steps` 등 수정 1 이 더한 키는 건드리지 않는다 |
| 새 대화부터 | JSON 이 바뀌면 sha 가 바뀐다 → **새 대화부터** 쓰인다(0.1 그대로 — 보관본) |

## 10. WP-4 — 빈 칸 · `ask` · 프롬프트 절: `consult/blanks.py` · `prompt.py` · `prompts/consult.json`

**SPEC**: §6-1 BK1 ~ BK5 · §6-2 NQ1 ~ NQ9 · §6-3 · 검수 W-2 · W-4 · W-7 · N-10 · S5-T9 · T10.
**만들 것**: `clinic_chat/consult/blanks.py` · `prompt.py`(고침) · `prompts/consult.json`(키 더하기) · `material.py`(앱 판정) · `tests/test_state_blanks.py`.

| 규칙 | 구현 |
|---|---|
| BK1 ~ BK5 | `blanks.count(state, memory)` → `[{slot, about, options[], options_n, asked_n}]`. BK2 의 선택지 = QY3(층이 가까운 것부터 — 자기 → 케이스 → 시술 → 계열 · 층 안은 허브 순서) · BK3 = QY1 응답 행의 하위 고민 `concern_code`(물은 고민 빼고) · BK4 = 하위 고민들의 `concern_sites[]` 가 둘 이상의 부위로 갈릴 때 그 부위(부위 칸이 없으면 서지 않는다 — §2) · BK5 = `guess` 항목 하나(W-1 로 사이 값만) |
| **W-4** | 같은 턴에 BK3 또는 BK4 가 서면 **BK1 은 그 턴의 빈 칸이 아니다** · BK3 과 BK4 가 함께 서면 **선택지 수가 적은 쪽** · 수가 같으면 BK3(§17 B-8) |
| NQ1 · NQ2 | `blanks.pick(…)` → `ask{slot, about, options[{table, code, name, layer}], why}` 또는 `null` + 까닭. 순서 = ① 이번 턴에 새로 든 항목에 딸린 것 ② 이번 턴의 새 `guess` ③ 앞 턴부터 남은 것 가운데 `focus` · 가장 최근 대상의 것 ④ 그 밖 · 같은 급이면 가장 최근 턴 · 같은 턴이면 W-4. 결정론이다(같은 장부 → 같은 `ask`) |
| **W-2 · NQ4** | 같은 빈 칸(`slot` + `about`)은 **모두 두 번까지**(`CHAT_ASK_MAX`) — 세 번째는 안 준다 |
| **W-2 · NQ5** | 앞 턴에 `ask` 를 줬고 이번 턴에 **걸린 선택지의 yes 가 0** 이면 이번 턴은 `ask` = `null`(**새 항목이 들었는지와 무관**). BK1 처럼 선택지가 없는 `ask` 는 「이번 턴에 `subjects[]` 에 새 항목이 들었나」 로 답을 가린다(§17 B-9) |
| NQ6 · NQ7 · NQ9 | 이번 턴 걷기가 `adverse` · `contraindication` · `avoid` 를 읽었으면 `null` · 세 종료 상태면 `null` · 선택지가 0 인 빈 칸(BK2 인데 적응 0)은 안 준다 |
| NQ3 | 준 `ask` 를 `asked[{slot, about, turn, options[], answered}]` 에 · 그 `options[]` 가 다음 턴의 걸린 선택지(WP-2) |
| NQ8 | LLM 에는 **이름과 층만**(코드는 장부) — 「앱 판정」 의 `ask.options[]` = `{name, layer, n}`(`n` = 그 선택지의 요약 줄 번호 · WP-3) |
| 앱 판정 | `material.judgement_of` 가 켠 상태에서 `consult{concerns[{name, state, focus}], subjects[{name, table, state}], sites[{name}], wishes[{name \| kind}]}` · `ask` · `synergy_lines[]`(WP-5) 를 더한다. 코드 · id 는 안 싣는다 |
| 프롬프트 | §9a 대로 `consult.json` 에 키를 더한다. 절의 글 = SPEC §6-3 표의 「담을 뜻」 을 **옮긴 초안**(새 뜻을 더하지 않는다) + §3-1 의 표지 한 줄. `version` = `0.2.0-draft` |
| 장부 | `consult.blanks[]` · `consult.ask` |

**완료 조건**: S5-T9(같은 장부 → 같은 `ask` · 새 항목의 빈 칸 먼저 · 세 번째는 안 준다 · **앞 `ask` 에 답 안 한 턴은 새 항목이 들어도 `null`**(W-2) · 안전을 물은 턴 `null` · 선택지 0 은 안 준다 · **BK3 · BK4 가 서면 BK1 없음 · 둘이면 적은 쪽**(W-4)) · S5-T10(`ask.options[]` 의 코드가 전부 그 대화의 허브 응답 행에 있다) · S5-T19(끈 상태의 시스템 글 = `system` 다섯 절만 · 0.1 보관본과 글자 대조 · 켠 글에 절 셋이 `screen` 과 `material` 사이 · 새 키가 빠진 JSON 으로 켠 대화 시작 → 실패 · 끈 대화는 됨)가 선다.
**검증**: `uv run pytest tests/test_state_blanks.py tests/test_consult_prompt.py -q`.

## 11. WP-5 — 시너지 먼저 · 같은 날 제약 표지: `consult/synergy.py`

**SPEC**: §7 SY1 ~ SY10 · §3-3 QY4 · §3-4 `shown.synergy[]` · U5-2 (a) · U5-3 (a) · U5-4 (a1) · U5-5 (a) · 검수 W-5 · N-2 · N-9 · S5-T11.
**만들 것**: `clinic_chat/consult/synergy.py` · `material.py`(요약 줄) · `tests/test_state_synergy.py`.

| 규칙 | 구현 |
|---|---|
| SY1(U5-2 (a)) | `subjects[]` 에 `said` · `confirmed` 대상이 있고 `focus` 고민이 있을 때, 그 대상의 시너지를 아직 안 읽었으면(`shown.synergy[]`) 그 턴에 읽는다. 턴 번호 조건 없음. `CHAT_SYNERGY=off` 면 통째로 안 한다 |
| SY2 · QY4 | `pair(a = 대상, classes = [보완])` — `b` 없음 · 쪽 넘김 끝까지(`hub.read_all`). 「순서」 · 「간격」 · 「대안」 · 패키지(SY8 — U5-5 (a))는 먼저 안 보인다 |
| **U5-4 (a1)** | QY4b(§3-1) — QY4 와 함께 한 번. 표지 `same_day_caution` 만 세운다 · 그 행은 재료 0 |
| SY3 | 보완 행의 `same_day` 에 값이 있으면 그 값을 줄에 · 빈칸이면 같은 날에 대해 아무것도 안 싣는다 |
| SY4 | **상대마다 요약 줄 하나** `{n, summary: true, synergy: true, 상대 이름, 상대 층, 내 쪽 층(a_layer.role), 행 수, same_day 값들, goal_effects 값들, same_day_caution}` + 장부 `{n, summary: true, key, rule: "QY4", gids[]}`. 키 이름은 실물 `pair` 응답의 것으로 맞춘다(`tests/test_clients.py` 의 `REAL_KEYS` · WP-8 의 첫 읽기로 대조 — 다르면 지어 맞추지 말고 보고) |
| SY5(U5-3 (a)) | **리스트 안** 상대만 LLM 줄 · 화면 표지. 리스트 밖 상대는 묶음 ③ 아래 수와 이름만. 「리스트 안」 = 상대가 계열이면 그 계열이 `focus` 리스트의 계열 묶음에 있나 · 시술이면 그 시술 행이 있나 · 케이스 · 제품이면 그것이 닿는 시술 · 계열이 있나 — **코드로** 견준다(이름 글자로 견주지 않는다 · §17 B-6) |
| SY6 · QY6 | 시너지가 **재료로** 싣는 것은 보완 행뿐 · 「회피」 · 불가 행의 글 0 |
| SY7 | 상대의 순서 = 허브 `pair` 행 순서에서 상대가 처음 나온 순서 · 앱이 줄 세우지 않는다 |
| SY9 | 한 대상의 `pair` 조회 · LLM 줄은 **한 번**. `focus` 가 바뀌면 화면 묶음 ③ 만 다시 짓는다(허브 재조회 0 — 대화 메모리 · 장부의 상대 목록으로) · `shown.synergy[].by_focus[]` 에 턴을 더한다 |
| SY10 | 대상이 둘 이상이면 대상마다 따로 · 묶음 ③ 도 대상마다 |
| RV8 | 거둔 대상의 묶음은 화면에서 빠진다 |
| 앱 판정 | `synergy_lines[]` = 이번 턴에 새로 실은 시너지 요약 줄 번호 |

**완료 조건**: S5-T11(QY4 의 `classes` = [보완] · 상대마다 한 줄 · 리스트 안 상대만 LLM 줄 · `same_day` 빈칸인 줄에 같은 날 값 없음 · 같은 대상은 한 번 · `focus` 가 바뀌면 화면 묶음만 · 줄 순서 = 허브 순서) · S5-T21(QY4b — 회피 · 불가가 함께 있는 상대에 `same_day_caution` · **턴 메시지 · `shown.info[]` · 「실은 gid」 에 QY4b 의 gid 0** · 보완 `same_day` 가 「가능」 인 상대에도 표지가 선다 · `CHAT_SYNERGY=off` 면 조회 0)이 선다.
**검증**: `uv run pytest tests/test_state_synergy.py -q`.

## 12. WP-6 — `list` 조각 · 표지: `listing.py` · `list.html`

**SPEC**: §3-5 SC1 ~ SC6 · §9(PL7 · PL8 행) · 검수 W-3 · N-7 · S5-T12 · T14.
**만들 것**: `consult/listing.py`(고침) · `templates/partials/list.html`(+ 새 조각) · `static/consult.css` · `render.py` · `server.py`(되읽은 화면) · `tests/test_state_list.py`.

| 규칙 | 구현 |
|---|---|
| SC1 | 칸 · 이벤트 이름 · 받는 자리는 그대로(`list` → `#procedure-list` · `sites` → `#face-marks`). 새 칸 · 새 이벤트 0 |
| SC2 | 장부 `list` = 0.1 의 `{concerns[…]}` 에 **더해서** `{interest[], concerns[], synergy[]}` — ① 관심 대상(`subjects[]` 의 이름 · 표 · 층 · 닿는 시술 — 고민이 없어도 그린다) ② `focus` 고민의 리스트(0.1 `build_list` 의 결과 그대로) ③ 시너지(대상마다 · 안 상대 · 밖 상대). ② 는 그 고민을 **가장 최근에 읽은** 응답으로 그린다(이번 턴에 안 읽었으면 장부의 그 고민 리스트 — 허브 재조회 0) |
| SC3 | ① · ② · ③ 가운데 하나라도 바뀐 턴에 `list` 를 보낸다(직전에 보낸 것과 견준다). 세 종료 상태 턴에는 안 보낸다(W-6) |
| SC4 · **W-3** | 관심 표지 `data-interest`: `procedures[]` 에 든 시술 → 그 **시술 행**에 · **계열 대상 → 그 계열 묶음의 머리**에(시술 행에는 안 단다). 리스트에 없으면 ① 에만 있다(앱이 리스트에 끼워 넣지 않는다) |
| 계열 코드 | 계열 묶음을 코드로 견주려고 켠 상태의 `list` 에 `modality_code` 를 함께 든다(후보 profile 행의 값 — 0.1 이 `modality_name` 을 읽는 그 행). 끈 상태의 `list` 는 0.1 글자 그대로다 |
| 시너지 · 제약 표지 | 리스트 안 상대의 시술 행 · 계열 머리에 `data-synergy` · 제약이 있으면 `data-caution`(§3-1) |
| SC5 | `sites` = `focus` 고민의 `concern_sites[]` 를 `sites.place()` 로(0.1 SI1 ~ SI7 그대로). 손님이 말한 부위(`sites[]`)는 점으로 안 그린다. `focus` 가 `null` 이면 빈 조각 |
| SC6 | 새 빈 자리(글 없음): `list-section-interest` · `list-section-synergy` · `list-synergy-outside` · `mark-interest` · `mark-guess` · `mark-caution` |
| 되읽은 화면 | `GET /c/{conv_id}` 가 마지막 성공 줄의 `list` · `sites` 를 그린다(지금 `last_list()` · `last_sites()` 길 그대로 — 꼴만 는다) |
| 스타일 | `consult.css` 에 표지 · 묶음의 꼴만(`--ms-*` 토큰 · 새 색 0 · 템플릿에 `style=` 0 · 인라인 스크립트 0 — 0.1 T24 그대로) |

**완료 조건**: S5-T12(고민 없이 대상만 있어도 묶음 ① · 관심 표지 = 시술 행 / **계열은 머리**(W-3) · `list` → `sites` → 첫 `delta` 순서) · S5-T14(새 템플릿 조각 · `consult/` 새 코드에 한글 문장 0 — 0.1 T17 과 같은 grep · 예외 = `consult/e5.py` 의 실측 입력 글)이 선다.
**검증**: `uv run pytest tests/test_state_list.py tests/test_consult_page.py -q`.

## 13. WP-7 — 예시 셋 · 끈 상태 대조 · 전체 검증

**SPEC**: §8 · 부록 B · §11-1 S5-T15 · T16 · §11-3 · 검수 W-2 · W-3 · N-2.
**만들 것**: `tests/test_state_examples.py` · `tests/state_fixture.py`(가짜 허브에 부록 B 의 수 · 가짜 Jev 에 §8 의 가정).

**S5-T16 의 기준 = SPEC §8 의 표를 코디 W-1 ~ W-3 으로 고친 것**(코디 W-2 「예시 고침」 — SPEC 은 고치지 않았다 · 되적기 후보). 바뀌는 칸만:

| 예시 · 턴 | SPEC §8 의 칸 | 고친 값 | 까닭 |
|---|---|---|---|
| ② 턴 2 화면 | 「필러 계열 묶음(`PRC-100` 하나)에 관심 표지」 | **필러 계열 묶음의 머리**에 관심 표지 · `PRC-100` 행에는 없다 | W-3 |
| ② 턴 3 화면 | 「`PRC-100` 에 관심 표지」 | 필러 계열 묶음의 **머리**에 · `PRC-100` 행에는 없다 | W-3 |
| ③ 턴 1 diff · `ask` | `sites` + `SITE-051` **`guess`** · 「BK5 도 빈 칸」 | `SITE-051` 은 **객체에 없다**(가짜 Jev 가 no 문턱 아래를 낸다 → `named` → trace 에만) · 빈 칸은 BK2 하나 | W-1 |
| ③ 턴 2 `ask` | BK5 `confirm`(`SITE-051`) | **없음**(빈 칸 0) | W-1 |
| ③ 턴 3 `ask` · 거둠 | 「없음(NQ5)」 · 「걸린 `SITE-051` 확인에 답하지 않음」 | **없음** — 앞 턴에 `ask` 가 없었고 빈 칸도 0 이다(NQ5 가 아니라) | W-1 · W-2 |
| ③ 턴 3 QY4 | 수 없음 | `pair(procedure:PRC-001, [보완])` = 33 행 · 상대 13 · `same_day` 가능 16(검수 재셈 N-2 — 하위 케이스 한 단) | N-2 |

- `guess` → BK5 의 길(사이 값)은 예시에 없으므로 S5-T2 · T5 · T9 가 따로 본다. NQ5(답하지 않은 턴)도 S5-T9 가 따로 본다.
- 예시의 QY4b(표지): 가짜 허브에 `M7`×`M9`(보완 5 · 회피 1) · `M8`×`M9`(보완 1 · 회피 불가 1 · 간격 불가 1) · `M2`×`M8`(보완 가능 1 · 회피 불가 2 · 간격 불가 1)을 싣고(검수 W-5 재셈), 예시 ① 턴 2 의 리스트 안 상대 6 가운데 `M7` · `M8` · 예시 ② 턴 2 의 6 가운데 `M8` 에 표지가 서는지 본다.

**전체 검증(여기서 한 번)**:

```
uv run ruff check .
CHAT_STATE=off uv run pytest -q    # WP-0 의 기준선 수 + 새 시험 · 실패 0 — 0.1 · 수정 1 시험은 이 상태의 것(B-1)
uv run pytest tests/test_state_*.py -q
git -C <APP-WT> status --porcelain  # allowed_paths(§2) 밖의 변경 0
```

| grep · 대조 | 기대 |
|---|---|
| 0.1 · 수정 1 시험 파일의 sha(WP-0 에 뜬 목록) | 그대로(변경 0) |
| `_face.svg` · `face_coords.py` 의 sha(WP-0 에 뜬 값) | 그대로(S5-T22 — 그 사이에 사용자가 바꿨으면 「사용자 변경」 으로 보고하고 되돌리지 않는다) |
| 0.1 의 고치지 않는 파일(`web/` · `prompts/*.md` · `prompts/jev/*.md` · `walk/material.py` · `walk/gate.py` · `walk/calls.py` · `walk/breadth.py` · `llm/*`) | 그대로(0.1 T18) |
| `consult/` 새 코드 · 새 조각의 한글 문장(주석 · `data-slot` 이름 · `e5.py` 입력 글 빼고) | 0(S5-T14) |
| 템플릿의 `style=` · `<script>` 본문 · `on[a-z]+=` | 0 |
| 새 코드 · 템플릿 · `consult.json` 의 키 꼴 · 비밀값 · 홈 경로 · 내부 주소 | 0 |
| `--json-schema`(상담 인자에) · `anthropic` 의존 | 0(U5-1 (가)) |

**완료 조건**: S5-T15(끈 상태에서 이벤트 · 장부(새 칸 · sha · 시각 · id 빼고) · LLM 메시지 · **시스템 글**이 0.1 과 같다 — 같은 가짜 셋으로 끈 상태 턴을 돌려 수정 1 뒤의 기대와 대조 · **SPEC-004 T1 ~ T18 과 지금 시험 전부 통과**) · S5-T16(§8 의 세 대화 — 턴마다 diff · 조회 · `ask` 가 고친 기준과 같다) · S5-T1 ~ T22 전부 통과 · ruff.

## 14. WP-8 — 실물 E5-1 ~ E5-4 · README

**SPEC**: §11-2 · §11-3 · O5-7 · O5-9 · 검수 W-1(E5-4 에 문장 더함) · N-10.
**만들 것**: `clinic_chat/consult/e5.py`(실측 입력 글 — 0.1 `e3.py` 꼴) · `consult/probe.py` 에 `--e5`(서버 없이 한 턴 흐름을 대화마다 — 이벤트를 메모리로) · `README.md` 「상담 화면」 절 · `.env.example`.

| # | 무엇(허브 18105 읽기 · Jev · 구독 CLI) | 보고에 적는 값 |
|---|---|---|
| **E5-1** | §8 의 세 대화(말 아홉) | 턴마다 객체 diff · 객체 기준 조회(`rule` · `total` · `ms` · `skipped`) · `first_list_ms` · `ttft_ms` · `total_ms` · Jev 요청 수(걷기 · 거둠 · 입구 고르기) · 허브 조회 수. **부록 B 의 재셈 수 ↔ 허브 응답의 `total` · `counts`**(다르면 어느 규칙을 잘못 흉내 냈는지 — 계열 끝 `M2` · `M4` 는 하한이라 다를 수 있다 · O5-9) · 리스트 안 · 밖 상대 수 · 표지가 선 상대 |
| **E5-2** | 걸린 선택지 — 예시 ① 턴 2(선택지 21 · 글자 맞춤 0) · ③ 턴 2(선택지 40) | 선택지마다 Noul · 맞는 것이 yes 인가 · 틀린 것이 yes 로 몇 개 드는가 · 32 를 넘을 때 Jev 요청 수 · `coverage` 호출 수 · 시간 |
| **E5-3** | 거둠 — 예시 ② 턴 3 꼴(「주름보다는 …」) + 거두지 않는 말 몇 개 | 항목마다 거둠 Noul · 더 드는 시간(걷기와 함께 띄웠을 때 한 턴 전체가 느는가 — `walk_ms` 와 `retract_ms`) · 거둠용 `resolve` 의 ms |
| **E5-4** | 우연 일치 — 예시 ③ 턴 1 의 「볼」 꼴 · 부록 B-4 의 「이신경」 꼴 · **「…입니다」 꼴**(검수 W-1 의 「고민**입**니다」 — `SITE-057`) | 그 후보의 Noul · 걷기 `decision`(`named` 인가 `uncertain_kept` 인가) · **객체에 안 드는가**(사이 값이면 `guess` 로 들고 리스트를 좁히지 않는가) · 해부 입구가 객체에 안 드는가 · 그 턴 걷기가 그것을 읽어 재료 · 시간이 얼마나 느는가(O5-2 의 재료) |
| 서버로 한 번 | `uv run python -m clinic_chat.consult --port 18223` → `curl` 로 예시 ① 을 한 대화 → **내림**(`lsof` 0 줄) | 이벤트 순서(`list` → `sites` → 첫 `delta` → `done` → `close`) · 조각에 묶음 ① · ② · ③ 이 있는가 |

- **답의 옳고 그름 · 질문의 자연스러움은 기준이 아니다**(E5-5 — 사용자 눈). 수와 배관만.
- 실물 키 이름 대조: `pair` · `scope` · `facets` 응답의 칸 이름이 이 문서 · SPEC 의 글과 다르면 지어 맞추지 말고 보고(§11 SY4).
- 환경 파일이 없거나 Jev · 허브가 안 닿으면 「못 돌림」 으로 보고한다(코디가 돌린다). 18105 는 읽기만.
- `consult/e5.py` 의 한국어 글은 실측 입력(시험 자료)이다 — S5-T14 의 예외로 시험에 명시한다(0.1 `e3.py` 와 같은 길).

**README 「상담 화면」 절에 더할 것**: 손잡이 넷(`CHAT_STATE` · `CHAT_ASK_MAX` · `CHAT_SYNERGY` · `CHAT_RETRACT`) · 대화의 켠 / 끈 상태는 시작 때 값으로 끝까지 · 프롬프트를 고쳤으면 새 대화(0.1 그대로) · 장부의 `consult` 칸 · 실측기 `--e5`.

**E5-5(코디 · 사용자)** — 코디가 18222 를 다시 띄우고 사용자가 본다:

| 볼 것(SPEC §11-2 E5-5 그대로 + 둘) |
|---|
| 시술로 들어왔을 때 고민을 자연스럽게 묻는가 · 한 답에 질문이 하나인가 · 정보만 물을 때 캐묻지 않는가 · 시너지가 묻지 않아도 뜨는가 · 안전 정보가 먼저 붙지 않는가 · 새 빈 자리 여섯(§12) |
| **(N-10)** 답이 선택지에 없는 고민 · 부위 이름을 예로 들지 않는가(프롬프트 규칙이라 단위 시험이 없다) |
| **(U5-4)** 같은 날 제약 표지가 있는 상대에서 답이 제약의 내용을 먼저 말하지 않는가 · 물으면 답하는가 |

## 15. 순서 · 의존 · 실물의 몫

```
[수정 1 끝 · 코디 알림] ─ WP-0(기준선 · 손잡이) ─ WP-1(객체 · 장부) ─ WP-2(걸린 선택지 · 거둠) ─ WP-3(객체 조회)
   ─ WP-4(빈 칸 · ask · 프롬프트) ─ WP-5(시너지 · 표지) ─ WP-6(list 조각) ─ WP-7(예시 셋 · 전체 검증) ─ WP-8(E5-1 ~ E5-4)
   ─ [코디: 18222 · 사용자 E5-5]
[별도 발주: SPEC-001 0.7 → 허브 부위 칸] ·········▶ 오면 점 · BK4 가 켜진다(이 WORK 의 코드 변경 0 — `sites.SITES_FIELD` 한 줄은 0.1 의 몫)
[사용자: 얼굴 SVG · 좌표표] ·········▶ 이 WORK 와 겹치는 파일 0
```

| 무엇 | 근거 |
|---|---|
| WP-0 을 수정 1 뒤에 | 같은 워크트리 · `turn.py` · `server.py` · `consult.json` · 템플릿이 겹친다(`_RESUME` §2 「직렬」) |
| C5-11 의 순서 그대로 | 객체 · 갱신 · 장부 → 객체 조회 → 빈 칸 · `ask` · 프롬프트 절 → `list` 조각 · 시너지 → E5. 「SPEC-004 0.1.1 되적기」 는 코디 몫이라 이 열에 없다 |
| 걸린 선택지(WP-2)를 빈 칸(WP-4)보다 앞에 | 함께 쓰는 코드를 고치는 유일한 WP — 일찍 닫고 걷기 시험 묶음을 돈다. WP-2 의 시험은 `asked[]` 를 손으로 채워 돈다 |
| 한 워커가 차례로 | `turn.py` · 장부 · `material.py` 가 WP 마다 물린다 — 나눠 발주하지 않는다 |

| 실물 | 누가 | 포트 |
|---|---|---|
| E5-1 ~ E5-4 | **워커**(안 되면 코디) | 없음 + 18223 한 번(확인 뒤 내림) · 18105 는 읽기만 |
| E5-5 | **코디가 18222 를 띄우고 사용자가 확인** | 코디 18222 |
| 건드리지 않는 것 | — | 18222 · 18105 · 18220 · 18210 · 18005 · 18432(띄우기 · 내리기 · 다시 띄우기 금지) |

**끝 조건**(SPEC §11-3): ① S5-T1 ~ T16 + 이 문서가 더한 S5-T17 ~ T22 통과 · 끈 상태에서 SPEC-004 T1 ~ T18 과 지금 시험 전부 통과 · ruff ② E5-1 ~ E5-4 의 값이 보고에 있다 ③ E5-5 — 사용자 확인(코디).

## 16. 검수 지적 반영 — WARN 9 · NOTE 10(`review-spec-005.md` §2)

| # | 반영 | 이 문서 |
|---|---|---|
| **W-1** | `guess` = 사이 값(`uncertain_kept`)만 · `named` 는 객체에 안 넣는다 · E5-4 에 「…입니다」 꼴 | §7 · §13 · §14 · S5-T2 · T17 |
| **W-2** | NQ5 = 걸린 선택지 yes 0 이면 안 묻는다(새 항목 무관) · NQ4 모두 두 번까지 · 예시 ③ 고침 | §10 · §13 · S5-T9 |
| **W-3** | 계열 대상의 관심 표지 = 계열 묶음 머리 · 예시 ② 고침 | §12 · §13 · S5-T12 |
| **W-4** | BK3 · BK4 가 서면 BK1 없음 · 둘이면 선택지 적은 쪽 | §10 · S5-T9 |
| **W-5** | 사용자 결정 U5-4 = (a1) 표지만 · 표지용 조회 QY4b · 바뀌는 규칙 · 시험 목록 | §3-1 · §11 · S5-T21 |
| **W-6** | 세 종료 상태 턴 = 객체 갱신은 하되 `list` 안 보냄 · 객체 조회는 다음 턴이 따라잡음 · T1 ~ T18 은 끈 상태 | §4 · §5 · §7 · S5-T18 |
| **W-7** | 끈 상태의 시스템 글 = 0.1 글자 그대로(`system` 다섯 절을 안 고치고 새 키 `system_state`) · 로더 검사 변경 | §9a · S5-T15 · T19 |
| **W-8** | 걸린 선택지가 전부 yes 가 아니면 입구 고르기(지금 코드의 가지) · 그 턴 Jev 요청 수 기록 | §8 · S5-T3 |
| **W-9** | `wishes[]` 는 조회를 일으키지 않는다 | §9 · S5-T8 |
| N-1 | 하위 제품의 적응은 이 판 선택지에 안 넣는다(SPEC QY3 그대로) — 열린 것 한 줄 | §17 O 표 |
| N-2 | 예시 ③ 턴 3 의 QY4 수 = 33 행 · 상대 13 · 가능 16 | §13 |
| N-3 | 오류 이벤트 이름은 구현대로 `turn_error` + `close` 로 읽는다(SPEC §9 의 `error` 는 되적기) | §14 · §17 B-12 |
| N-4 | e2e 지적 6(「볼 주름 → 처짐 때문인가」 · 같은 윗고민 아래 다른 고민의 시술) — 이 판은 구현하지 않는다 · 열린 것 한 줄 | §17 O 표 |
| N-5 | 거둠용 `resolve` 한 번이 객체 조회 셈 밖에 더 든다 — 장부 · 보고에 수를 적는다 | §8 · §14 |
| N-6 | `wishes[]` 의 종류 항목은 `{kind, …}` 꼴(SL1 의 예외) — 닫힌 목록으로 검사 | §7 · S5-T1 |
| N-7 | 묶음 ①(관심 대상)이 리스트 칸에 새로 생긴다 — 코디가 사용자에게 알린다(통보감) | §3-1 U5-3 |
| N-8 | `carried[]` 는 앞 턴 대상만 · 선택지는 `consult.options_carried[]` 에만 | §8 · S5-T3 |
| N-9 | 「보완」 갈래만 먼저 — 그대로 | §11 |
| N-10 | E5-5 의 볼 것에 한 줄(선택지 밖 이름을 예로 들지 않는가) | §14 |

## 17. 열린 것 · 이 문서를 쓰며 본 것(SPEC 은 고치지 않았다)

| # | 무엇 | 본 것 | 제안(본문이 따른 값) |
|---|---|---|---|
| **B-1** | 기본값이 `on` 인데 0.1 · 수정 1 의 시험은 끈 상태의 것이다 | SPEC §10-2 기본 `on` · 코디 W-6 「T1 ~ T18 은 끈 상태」 · 기존 시험 파일은 못 고친다. 켠 채로는 T6 · T12 꼴이 걸릴 수 있다 | 전체 검증을 `CHAT_STATE=off` env 로 돈다(본문) + 새 시험은 설정에서 `on` 을 명시. 기존 시험의 설정 도우미가 프로세스 env 를 안 읽으면 WP-0 이 보고 → 코디가 고른다: (a) 시험 설정 도우미(`tests/conftest.py`)에 `chat_state="off"` 한 줄 (b) 코드 기본값을 `off` 로 두고 실행 env 로 켠다 |
| **B-2** | 0.1 로 쓴 대화를 0.2 가 되읽을 때 | SPEC §10-1 은 「빈 객체에서 시작」 이라 적었다. 그런데 그 대화의 보관 프롬프트에는 0.2 키가 없고 CLI 의 시스템 글도 첫 턴 스냅숏이다 | **그 대화는 끈 상태로 끝까지**(본문 §6). SPEC 과 다르게 받는 곳 — 되적기 후보 |
| **B-3** | `wishes[]` 의 정보 종류를 무엇으로 채우나 | SPEC §2-2 는 「Jev 정보 종류 Noul 이 yes 인 종류」 · §2-3 표가 바람으로 둔 종류는 `recovery` · `outcome` 둘 | yes 로 읽은 종류 가운데 그 둘만(본문 §7). 14 종류 전부를 남기려면 코디가 정한다 |
| **B-4** | 든 후보(앞 턴 대상)가 yes 일 때 객체의 `source.how` | SPEC 의 `how` 는 `text` · `option` · `derived` 셋 — 「앞 턴 대상을 이어 물음」 의 값이 없다. 대부분 이미 객체에 있어 UP6(턴만 더함)이지만, 앞 턴에 `named` 라 객체에 없던 것이 든 후보로 yes 가 되면 새 항목이다 | 새 값 하나 `carried`(걷기의 `by` 와 같은 낱말) — 되적기 후보. 같은 (표, 코드)가 든 후보이면서 걸린 선택지면 `option` 으로 적는다 |
| **B-5** | 거둠 요청이 실패(Jev 오류 · 시간 초과)하면 | SPEC 에 없음. 걷기의 Jev 오류는 그 턴 「실행 중단」 이다 | 거둠은 보조 판단이라 **턴을 죽이지 않고** 「거둠 0」 으로 계속 · `consult.retract_error` 기록(본문 §8). 코디가 다르게 정하면 그 한 줄 |
| **B-6** | 케이스 · 제품 상대의 「리스트 안 · 밖」 판정 | SPEC 부록 B-1 은 `g_profile.modality_code` 로 흉내 냈다(「구현이 정하면 달라질 수 있다」). 앱은 CSV 를 안 읽는다 · `pair` 행에 상대의 계열 칸이 있는지는 실물 응답을 봐야 안다 | 순서대로: ① `pair` 응답 행에 상대 쪽 층 · 경로 칸이 있으면 그것 ② 없으면 그 상대에 `scope` 를 불러 닿는 시술 · 계열을 얻는다(상대 가운데 케이스 · 제품만 — 예시 ① 은 11 가운데 3 이하 · `consult.queries[]` 에 `rule: "SY5"`). 그 조회가 싫으면 「케이스 · 제품 상대는 밖으로」 — 코디가 고른다. **WP-5 첫 걸음에 실물 `pair` 응답 한 건을 읽어 ① 이 되는지 보고한다** |
| **B-7** | `rules` 6 번의 예외 구절의 자리 | SPEC §6-3 은 「`rules` 한 줄에 구절을 더한다」 · 코디 W-7 은 「끈 상태 시스템 글 = 0.1 그대로」 — 둘을 함께 지키려면 `rules` 를 못 고친다 | 예외 구절을 `synergy` 절의 한 줄로(본문 §9a) — 되적기 후보 |
| **B-8** | BK3 과 BK4 의 선택지 수가 같을 때 | 코디 W-4 는 「적은 쪽」 까지 | BK3(고민 먼저) — 시험이 결정론을 요구해 하나를 골라야 한다 |
| **B-9** | 선택지가 없는 `ask`(BK1)에 「답했다」 를 무엇으로 가리나 | 코디 W-2 의 NQ5 는 「걸린 선택지 yes 0」 — BK1 은 선택지가 없다(SPEC BK1) | BK1 은 「이번 턴에 `subjects[]` 에 새 항목이 들었나」 로(SPEC §8-2 턴 2 의 `answered = true(관심이 생김)` 과 같은 뜻) |
| **B-10** | 객체 조회의 응답을 어디에 들고 있나 | `blanks` · 묶음 ③ 다시 짓기가 앞 턴의 QY 응답을 쓴다. SPEC 은 「장부의 행」 이라고만 | 대화 메모리(`Conv`)에 조회 응답을 (도구 · 입력) 키로 들고, 서버를 다시 띄운 뒤에는 필요할 때 허브를 다시 읽는다(허브는 결정론 · 대화의 `gold_hash` 는 고정 — CL14). 장부에는 응답 본문을 안 싣고 `queries[]` · 요약 줄의 `gids[]` · `list` 만 |
| **B-11** | 걸린 선택지가 붙으면 `coverage` 노드 수도 는다 | `front.py:230` 이 후보 전부의 `coverage` 를 함께 읽는다(64 를 넘으면 호출 둘) | 그대로 둔다(함께 쓰는 코드) · E5-2 가 시간을 잰다 |
| **B-12** | **SPEC 되적기 후보(한 줄)** | — | SPEC-005 0.1.1: UP3 의 `guess` 범위(W-1) · NQ4 · NQ5(W-2) · SC4 계열 머리 + §8 예시(W-2 · W-3 · N-2) · NQ2 동률(W-4 · B-8) · SY6 · QY4 · QY6 · S5-T8 · T11 에 QY4b(U5-4 (a1)) · SC6 에 `mark-caution` · L4 · SC3 의 세 종료 상태(W-6) · §6-3 의 `system_state` · 예외 구절 자리 · 로더(W-7 · B-7) · UP4 뒷절(W-8) · §2-3 · QY 표에 `wishes[]` 조회 0(W-9) · SL1 의 종류 항목 예외(N-6) · §10-1 `carried[]` 와 `options_carried[]`(N-8) · 0.1 대화의 되읽기(B-2) · `source.how` 의 `carried`(B-4) · §9 의 이벤트 이름 `turn_error` · `close`(N-3) · `jev_state.retract` 의 색인 이름 `candidates` |

| # | 열린 것(이 판은 구현하지 않는다) | 상태 |
|---|---|---|
| O5-1 ~ O5-10 | SPEC §13 그대로 | O5-8(요약 줄 칸)은 §9 · §11 이 고정 · O5-9 · O5-7 은 E5-1 이 값을 낸다 · O5-2 는 E5-3 · E5-4 가 재료를 낸다 · 나머지는 그대로 열림 |
| O5-11(N-1) | 「왜 받고 싶은가」 선택지에 하위 제품 자신의 적응을 층 밝혀 넣을지(예: 써마지 `PRD-416` 의 하위 `PRD-417` — 직접 적응 11 행) | 이 판은 QY3 = 자기 · 물려받음만. E5-1 · E5-5 를 본 뒤 코디 · 사용자 |
| O5-12(N-4) | e2e 지적 6 — 「볼 주름 → 처짐 때문인가 되묻기 → 처짐 고민으로」 · 같은 윗고민 아래 다른 고민의 시술을 층 밝혀 보일지(`_RESUME` §1) | 상담 쪽에서 정하기로 적힌 것 — 이 판의 빈 칸 다섯에는 없다. 사용자 |

## 18. SPEC-005 절 ↔ WP 대응(미대응 0)

| SPEC-005 | 무엇 | WP |
|---|---|---|
| §0 · §1-1 | 요약 · 목적 | 구현 없음 |
| §1-2 D5-1 ~ D5-13 | 정해진 것 | 아래 절로 흩어짐 — D5-12(CLI · JSON · 세 칸)는 0.1 그대로 · D5-13 은 §2 시작 조건 |
| §1-3 | 범위 밖 | 구현 없음(§2 「고치지 않는 것」 · 누르는 동작 0) |
| §2-1 SL1 ~ SL6 | 객체 원칙 | WP-1(SL5 · SL6 은 「순위 · 담기 칸 없음」 을 S5-T1 이 닫힌 목록으로) |
| §2-2 | 칸 | WP-1(칸 · 항목) · WP-3(`concern_sites[]` · `procedures[]` · `shown.info`) · WP-4(`asked[]` · `blanks[]`) · WP-5(`shown.synergy`) · WP-6(`shown.lists`) |
| §2-3 | 바람 | WP-1(`wishes[]`) · WP-3(조회 0 — W-9 · 부위 거르개는 QY5) |
| §2-4 | 항목 꼴 · 출처 · 확실함 | WP-1(+ W-1) · WP-2(`how` = `option`) |
| §3-1 L1 ~ L9 | 한 턴 루프 | §5 — WP-0(L1) · WP-2(L2 · L3) · WP-1(L4 · L9) · WP-3 · WP-5(L5) · WP-6(L6) · WP-4(L7) · L8 은 0.1 |
| §3-2 UP1 ~ UP9 | 갱신 규칙 | WP-1(UP1 ~ UP3 · UP6 ~ UP9) · WP-2(UP4 · UP5) |
| §3-3 QY1 ~ QY6 | 객체 기준 조회 | WP-3(QY1 ~ QY3 · QY5 · QY6) · WP-5(QY4 · QY4b) |
| §3-4 | `shown` | WP-3 · WP-5 · WP-6 |
| §3-5 SC1 ~ SC6 | 화면 | WP-6 |
| §4 | 갱신 주체 | U5-1 (가) — WP-1 · WP-2((나)는 구현 없음 — WP-7 grep) |
| §5 RV1 ~ RV9 | 확실함 · 되돌림 | WP-1(RV1 · RV5 ~ RV7 · RV9) · WP-2(RV2 ~ RV4 · RV8) |
| §6-1 BK1 ~ BK5 | 빈 칸 | WP-4 |
| §6-2 NQ1 ~ NQ9 | 하나 고르기 | WP-4(+ W-2 · W-4) |
| §6-3 | 프롬프트 JSON 절 | WP-4(§9a — W-7) · `target_option` · `retract` 를 쓰는 곳은 WP-2 |
| §7 SY1 ~ SY10 | 시너지 먼저 | WP-5(SY5 의 화면은 WP-6) |
| §8(§8-1 ~ §8-3) · 부록 B | 예시 셋 · 재셈 | WP-7(S5-T16 — 고친 기준) · WP-8(E5-1 이 허브 값과 맞춤) |
| §9 | SPEC-004 위에 얹는 것 | 행마다: 모듈 자리 = WP-1 · 3 · 4 · 5 / ST3 · TF2 · CR = WP-2 / TF3 = §5 / TF4 · §7 = WP-4 / 이벤트 · PL · SI = WP-6 / LG3 = WP-1 ~ 5 / AP = WP-3 · WP-5 / §9 시험 = WP-7 |
| §10-1 | 장부 칸 | WP-1(`diff` · `after`) · WP-2(`options_carried` · `retract`) · WP-3(`queries`) · WP-4(`blanks` · `ask`) |
| §10-2 | 설정 칸 | WP-0 |
| §11-1 S5-T1 ~ T16 | 단위 시험 | 아래 표 |
| §11-2 E5-1 ~ E5-5 | 실물 | E5-1 ~ E5-4 = WP-8 · E5-5 = 코디 · 사용자(§14 · §15) |
| §11-3 | 끝 조건 | §15 |
| §12-1 U5-1 ~ U5-5 | 사용자 결정 | §3-1(닫힘) |
| §12-2 C5-1 ~ C5-11 | 코디 기본값 | C5-1 = WP-1 · C5-2 = WP-1(+ W-1) · C5-3 · C5-4 = WP-2 · C5-5 = WP-1 · C5-6 · C5-7 = WP-4 · C5-8 = WP-5 · C5-9 = WP-6 · C5-10 = WP-0 ~ WP-5 · C5-11 = §15 |
| §13 O5-1 ~ O5-10 | 열린 것 | §17 O 표 |
| 부록 A | 결정 행 → 줄 | 구현 없음 |

| 시험 | WP | | 시험 | WP |
|---|---|---|---|---|
| S5-T1 · T2 · T5 · T7 · T13 | WP-1 | | S5-T11 | WP-5 |
| S5-T3 · T6 | WP-2 | | S5-T12 · T14 | WP-6 |
| S5-T4 | WP-1(객체) · WP-3(채움) | | S5-T15 · T16 | WP-7 |
| S5-T8 | WP-3 | | **S5-T17** `named` 는 객체에 없다 · BK5 · 거둠 항목에 안 든다(W-1) | WP-1(S5-T2 와 같은 파일) |
| S5-T9 · T10 | WP-4 | | **S5-T18** 세 종료 상태 턴 — diff 있음 · `list` 0 · 조회는 다음 턴에(W-6) | WP-1 · WP-3 |
| **S5-T19** 끈 / 켠 시스템 글 · 로더(W-7) | WP-4 | | **S5-T20** `origin` 없음 = 지금 동작(ST3) | WP-2 |
| **S5-T21** QY4b 표지 · 재료 0(U5-4 (a1)) | WP-5 | | **S5-T22** 얼굴 파일 · 0.1 시험 파일 sha 무변경 | WP-0 · WP-7 |

## 변경 기록

### 0.1.0 (2026-11-17) — 처음 씀

- SPEC-005 0.1.0 의 구현 계획: WP-0(수정 1 뒤 시작 확인 · 기준선 · 손잡이) ~ WP-8 · 시험 S5-T1 ~ T16 + S5-T17 ~ T22 · 실물 E5-1 ~ E5-5 의 몫(워커 18223 · 코디 18222 · 18105 읽기만).
- 사용자 결정 U5-1 ~ U5-5 = 추천 반영 — U5-4 (a1) 은 표지용 조회 QY4b(`pair` 의 회피 · 간격 · 순서 갈래 · 재료 0)를 `consult/synergy.py` 에 둔다.
- 코디 W-1 ~ W-9 한 줄씩(§3-2 · §16) · NOTE 10 처리(§16) · `CHAT_STATE` 끈 / 켠 상태 목록(§4) · S5-T16 의 고친 기준(§13).
- 얼굴 SVG · 좌표표는 고치지 않는다(사용자) · 허브 부위 칸이 없으면 점 0 그대로.
- 열린 것 B-1 ~ B-12 · O5-11 · O5-12(§17).
