---
type: work
id: WORK-011
title: "앱 상담 채팅 1판 구현 계획 — CLI 3턴 실측 먼저 · 프롬프트 JSON · 실행기(`--session-id` → `--resume`) · 대화 장부 · 재료 덧붙이기 · 시술 리스트 · htmx 화면(DAY 디자인 킷) · 얼굴 SVG · 이어 묻기 · 실물 E0 ~ E4"
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
    - "orchestration/work/phub-gold-jev/SPEC-004-consult-chat.md (0.1.0 · 검수 PASS — FAIL 0 · WARN 8 · NOTE 7 · review-spec-004.md) ← 계약"
    - "orchestration/work/phub-gold-jev/SPEC-001-hub-gold-mcp.md (0.6.0 — §4-5 `concern_candidates` · 0.7 의 고민 부위 칸은 별도 발주)"
    - "orchestration/work/phub-gold-jev/SPEC-002-chat-eval.md (0.6.0 — 걷기 · 재료 · 종료 상태는 그대로 쓴다)"
  decisions:
    - "orchestration/work/phub-gold-jev/_RESUME.md §2 (2026-11-17 「SPEC-004 U-11~U-13 = 추천 (a)」 · 「상담 프롬프트 = JSON 으로 불러옴」 · 「SPEC-004 검수 뒤 코디」(W-1 ~ W-8) · 「CLI 실행기 = 앱이 직접 띄움」 · 「채팅 조사 뒤 사용자 결정」 · 「이번 세션 목표 = 상담 채팅」 · 「Procedure Hub 데이터는 공개 정보」)"
    - "코디 보충(2026-11-17 · 인박스 「화면 디자인 킷 = CENTURION_DAY」) — 사용자 결정: 상담 화면은 CENTURION_DAY 디자인 킷을 참고"
    - "코디 보충 2(2026-11-17 · 인박스 「medikit 공개 OK」) — 사용자 확인: medikit 은 디자이너가 전체 공개로 배포한 것 · clinic_chat(공개 레포)에 복사 · 벤더링해도 된다"
  related:
    - "orchestration/work/phub-gold-jev/review-spec-004.md (WARN 8 · NOTE 7 — 이 문서 §17)"
    - "orchestration/work/phub-gold-jev/research-chat.md (근거 · 「확인 안 됨」 8)"
    - "orchestration/work/phub-gold-jev/WORK-009-v06.md (앞 계획 — 공통 규칙의 꼴)"
---

# WORK-011 — 앱 상담 채팅 1판 구현 계획

> 경로 접두어: `W` = 이 폴더 · `APP-WT` = `~/orca/workspaces/clinic_chat/phub-gold-jev`(브랜치 `kknaksss/phub-gold-jev` · HEAD `6303e18` · 작업 트리 깨끗 — **그 위에 이어서 짓는다**) · `DAY` = `~/git/CENTURION_DAY`(브랜치 `dev` · `c5045a99` — **읽기만** · 디자인 킷의 본).
> **계약은 SPEC-004 0.1.0 이다.** 이 문서는 「어느 파일을 · 어떤 순서로 · 무엇으로 확인하나」 만 정한다. SPEC 과 다르게 받는 곳은 **둘뿐**이고 둘 다 사용자 결정이다 — 프롬프트 JSON(§3) · 디자인 킷(§4). 그 밖에 SPEC 과 어긋나는 것을 만나면 코드를 맞춰 고치지 말고 보고한다(§18).
> **화면 문구 · 답 문구를 짓지 않는다**(SPEC §4-5 · ST4). 프롬프트는 뼈대를 옮긴 **초안**이고 확정은 사용자다(C-1).
> **사용자 결정은 닫혔다**(`_RESUME` §2 11-17): **U-11** `broken` 이면 그 대화는 끝(새 대화만) · **U-12** 이어 묻기는 앞 턴 **대상**만 · **U-13** 「계열 층만」 · 「그 밖」 은 시술 행 아래 따로 묶음 둘로 전부.
> Procedure Hub 데이터(부위 코드 · 이름)는 공개 정보다(`_RESUME` §2 11-17) — 이 문서 · 앱 레포에 적어도 된다. 비밀값 · 키 · 내부 주소는 그대로 금지.

## 0. 요약

- 상담은 새 패키지 `clinic_chat/consult/` 다. 시험 앱(18220 · 열 · runner · 채점)은 고치지 않는다. 걷기는 같은 `walk()` 를 쓴다(ST1 · ST2).
- **첫 WP 는 코드가 아니라 실측이다** — WP-0 = E1(CLI 3턴) · E2(중단 뒤 resume). `--max-turns 1` 을 이 판 CLI 가 안 받으면 **거기서 멈추고 코디에게 올린다**.
- WP 열: **WP-0** CLI 실측 → **WP-1** 화면 바탕(의존 · 디자인 킷 · 빈 화면 E0) → **WP-2** 프롬프트 JSON · 설정 칸 → **WP-3** 실행기 → **WP-4** 장부 → **WP-5** 재료 덧붙이기 → **WP-6** 시술 리스트 → **WP-7** 한 턴 흐름 · 라우트 · 이벤트 → **WP-8** 부위 · 얼굴 SVG · 좌표표 → **WP-9** 이어 묻기 → **WP-10** 실물 E3 · README · 전체 검증 → **코디** 18222 띄움 · 사용자 E4.
- **허브 의존은 하나**다 — 고민 부위 칸(SPEC-001 0.7 · 별도 발주). 그 칸이 오기 전에는 점 · 라벨 없이 돈다(§12). 이 문서에 허브 WP 는 없다.
- 함께 쓰는 코드에 손대는 곳은 **선택 인자 둘**(`carry` · `instr`)이고 기본값이 지금 동작이다(§13 · §18 B-2). 줄 번호 시작 인자는 **넣지 않는다**(W-1).

## 1. 지금 코드(11-17 확인 — `APP-WT` HEAD `6303e18` · 줄 번호는 그 커밋)

| 파일 | 지금 | 이번에 |
|---|---|---|
| `clinic_chat/llm/cli.py`(367줄) | `DISALLOWED_TOOLS`(`:36`) · `USAGE_KEYS`(`:38`) · `claude_args`(`:78-93` — `--system-prompt <글>` · `--no-session-persistence` 가 박힘 `:80-84`) · `new_result`(`:100-104`) · `ClaudeIngest._init`(`:159` — 세션 id 를 안 읽는다) · `_semaphore`(`:294-298`) · 실행마다 임시 cwd(`:314` · `:331`) | **안 고친다** — 상담은 자기 인자 함수를 갖고 `ClaudeIngest` · 상수만 가져다 쓴다(WP-3) |
| `clinic_chat/llm/cli_process.py`(101줄) | `child_env`(`:29-37` · `SCRUB_ENV` `:20-26`) · `run_cli`(`:54-101` — `start_new_session=True` `:59` · 시간 초과면 그룹째 끝냄 `:83-97`) | 안 고친다 |
| `clinic_chat/llm/auth.py`(63줄) | 구독 확인 · 10분 캐시(`CACHE_S` `:12`) | 안 고친다 |
| `clinic_chat/columns/col_b.py`(459줄) | `TAIL_MARK`(`:42`) · `walk`(`:161-225`) · step ① ~ ④(`:167` · `:179` · `:193` · `:198`) · `judgement`(`:252-269`) · `prompt_pages`(`:272-283` — 머리 글자가 인라인) · `split_tail`(`:286-304`) · `_TailFilter`(`:307-332`) · `b_trace`(`:378-401`) | `walk()` 에 선택 인자 둘(`carry` · `instr`)을 `front()` 로 넘기는 한 줄(WP-9) · 그 밖은 안 고친다 |
| `clinic_chat/walk/front.py`(401줄) | `front`(`:196`) — resolve 후보(`:203-216`) · Jev 지시를 **안에서** 읽음(`prompts.jev_sections("front")` `:222`) · `ask_front` 한 요청(`:227`) · 덮인 조각은 yes 만(`:306-307`) | 선택 인자 `carry` · `instr`(WP-9) |
| `clinic_chat/walk/jev_requests.py`(91줄) | `fill`(`:27`) · `ask_front`(`:64` — 한 요청 = 대상 + 종류 14 + gap · 32 묶음) | 든 후보는 `target_carried` 절을 쓰는 가지 하나(WP-9 — 절이 없으면 지금 동작) |
| `clinic_chat/walk/material.py`(336줄) | `build`(`:160` — 줄 번호 `enumerate(…, 1)` `:167`) · 묶음 꼴 `{group, table, same, marks, lines, rows}` · `unfold`(`:239`) · `to_lines`(`:253`) | **안 고친다**(W-1) — 상담 `consult/material.py` 가 걷기 **뒤에** 옮겨 적는다 |
| `clinic_chat/walk/gate.py`(173줄) | K1 = 줄 번호가 `1 … N`(`:51-52`) | 안 고친다(걷기 안 번호가 그대로라 통과) |
| `clinic_chat/walk/breadth.py` · `calls.py` · `verified.py` | `Read{call, ra, gids}`(`breadth.py:39`) · `followup_calls` — `concern_candidates` 의 `groups` 후보마다 `facets` profile(`calls.py:378-`) · `VRow.followup`(`verified.py:129`) · `Entry.by`(`calls.py:59`) | `Entry.by` 주석에 값 `carried` 하나(WP-9) |
| `clinic_chat/clients/hub_rest.py` | `concern_candidates`(`:195`) · 쪽 밖 목록 `modality_only` · `unreached`(`:33`) · `ReadAll.as_response`(`:92`) | 안 고친다 |
| `clinic_chat/web/server.py`(269줄) | `PORT` 18220(`:32`) · `Live`(`:52-64`) · `to_sse`(`:82-86`) · `resume_from`(`:89-95`) | **안 고친다**(T18) — 꼴만 따른다 |
| `clinic_chat/progress.py` · `timing.py` · `runs.py`(`now_iso` · `app_commit` · `RunStore._append`) · `prompts.py`(`sha256_text`) | 그대로 | 안 고친다 |
| `clinic_chat/config.py`(95줄) | `Settings` — `cli_max_concurrent` 1(`:33`) · `jev_batch_size` 32(`:52`) · `runs_dir`(`:63`) | 상담 칸을 더한다(WP-2 — 지금 칸은 안 바꾼다) |
| `prompts/` | `common.md` · `col_*.md` · `judge.md` · `jev/{front,entry,candidate,answer_ready,value}.md` | **안 고친다**(T18) · 새 파일 `prompts/consult.json` 하나 |
| `pyproject.toml` · `uv.lock` | 직접 의존 6 · `jinja2` 없음 · `python-multipart` 0.0.33 은 딸려 옴 | `jinja2` · `python-multipart` 를 직접 의존에(WP-1) |
| `tests/` | 시험 파일 24 · `fake_cli/` · `fake_hub.py` · `fake_jev.py` · `conftest.py`(`fake_cli` · `stream` · `make_settings`) | WP 마다 새 시험 파일(`tests/test_consult_*.py`) · 가짜 CLI 에 세션 id · 중간 종료 꼴(WP-3) |

기준선: WP-1 첫 걸음에 `uv run pytest -q` 를 **한 번** 돌려 통과 수를 보고에 적는다(SPEC ST3 는 214 건이라 적었다 — 이 문서는 다시 세지 않았다). 끝의 전체 검증(WP-10)이 그 수 + 새 시험이어야 한다.

지금 떠 있는 것(11-17 확인): `127.0.0.1:18105`(허브 — 지금 DB 판) · `18210` · `18220`(시험 화면). 로컬 CLI = 2.1.322.

## 2. 공통

| 항목 | 이번 판 |
|---|---|
| allowed_paths(앱) | `clinic_chat/consult/**`(새로) · `clinic_chat/llm/chat.py` · `chat_cli.py`(새로) · `clinic_chat/config.py`(칸 더하기만) · `clinic_chat/columns/col_b.py` · `clinic_chat/walk/front.py` · `walk/jev_requests.py` · `walk/calls.py`(§13 의 줄만) · `prompts/consult.json`(새로) · `tests/**` · `README.md`(상담 절) · `.env.example`(새 env 이름) · `pyproject.toml` · `uv.lock`(의존 둘) |
| 고치지 않는 것 | `clinic_chat/web/**` · `runner.py` · `batch.py` · `quality/**` · `evalset/**` · `report.py` · `speed.py` · `columns/col_a.py` · `col_c.py` · `llm/cli.py` · `cli_process.py` · `auth.py` · `walk/material.py` · `walk/gate.py` · `prompts/*.md` · `prompts/jev/*.md`(T18 이 sha 로 잡는다) |
| allowed_paths(허브 · DAY) | **없음** — 둘 다 읽기만 |
| 포트 | **18210 · 18005 · 18105 · 18220 은 띄우지도 내리지도 다시 띄우지도 않는다.** 18105(허브)는 **HTTP 로 읽기만** 한다(실행 env `HUB_REST_URL` 은 발주서 값 — 없으면 설정 기본 · §18 B-1). **18222 는 코디 것**(사용자 e2e). 워커는 **18223**(차 있으면 18224 … 빈 포트를 `lsof` 로 확인) 에서 띄워 확인한 뒤 **스스로 내린다** — 보고에 포트 · 내린 것을 적는다 |
| 외부 호출 | 단위 시험은 전부 가짜(CLI · 허브 · Jev). 실물은 WP-0(구독 CLI) · WP-10(허브 읽기 · Jev · CLI)뿐. `.env` 를 열거나 고치지 않는다(없으면 「못 돌림」 으로 보고 → 코디가 돌린다). 키는 env 이름만 적는다 |
| 사용자 홈 | 세션 파일(`~/.claude/projects/…`)을 **지우지 않는다**(CL9-2). 고정 cwd 는 레포 밖(§7) |
| 밑그림 PNG | 읽기만 · 레포에 두지 않는다(그것을 기계로 뽑은 것도) · 앱 레포의 README · 주석에 그 경로를 옮기지 않는다(N-3) |
| 문구 | 템플릿 · `consult/` 코드에 사람에게 보일 문장 0(`data-slot` 자리만). DAY 의 `ui.html` 에서 **매크로 꼴만** 가져오고 그 안의 한글 기본값(예: 검색 안내 글)은 가져오지 않는다 |
| 디스크 | 여유 약 9 GB(11-17). 글꼴 파일 2 MB 하나 말고 큰 파일을 만들지 않는다 |
| 검증 | 단계마다 그 WP 의 시험만: `uv run ruff check .` · `uv run pytest tests/test_consult_<이 WP>.py -q`. **전체 `uv run pytest -q` 는 WP-10 에 한 번**(함께 쓰는 코드를 고치는 WP-9 만 예외 — 그때 걷기 시험 묶음을 함께 돈다) |
| 커밋 | 워커는 커밋 · push · PR 을 하지 않는다(코디 몫) |

## 3. SPEC 과 다르게 받는 곳 ① — 프롬프트는 JSON 한 파일

**결정**: `_RESUME` §2 11-17 「상담 프롬프트 = JSON 으로 불러옴」. SPEC-004 의 CL2(`--system-prompt-file`) · §7-2(`prompts/consult/system.md` · `jev_front.md`) · PM3 · PM5 를 아래 꼴로 **바꿔 받는다**. SPEC 은 고치지 않는다(되적기 후보 — §18 B-12).

| SPEC | 이 판 |
|---|---|
| CL2 `--system-prompt-file <파일>` | `--system-prompt "<글>"` — 앱이 `prompts/consult.json` 의 `system` 절을 이어 붙인 글(지금 시험 앱 꼴 `llm/cli.py:80`). F6 의 `--system-prompt-file` 확인은 **필요 없다**(`--max-turns` 확인은 남는다) |
| §7-2 파일 둘 | `prompts/consult.json` **한 파일**에 상담 지시 · Jev 맨 앞 판단 지시 · 턴 메시지 머리 · 꼬리 표식을 키로 |
| PM5 「초안」 주석 | JSON 에는 주석이 없다 → `version` 칸이 초안 표지(`"0.1.0-draft"`) |
| PM3 · LG3 `prompts{consult, jev_front}` | sha 는 **JSON 파일 전체** 하나 — 장부에 `prompts{consult_at_start, consult_now, changed}`(W-4) |
| SD1 「시스템 지시 파일」 | 인터페이스는 읽은 프롬프트 객체(절 배열 + 이어 붙인 글)를 받는다. CLI 는 이어 붙인 글 · SDK 는 **같은 JSON 의 `system`** 을 쓴다(경계 — 이 판은 CLI 만) |

### 3-1. `prompts/consult.json` 의 꼴

| 키 | 꼴 | 뜻 |
|---|---|---|
| `version` | 문자열 | 프롬프트 판 · 초안 표지(`-draft` 로 끝나면 사용자 확인 전) |
| `system` | `[{id, lines[]}]` — `id` ∈ `role` · `rules` · `screen` · `material` · `tail`(PM1 의 절 ① ~ ⑤ · 이 순서) | 상담 지시. 이어 붙이기 = 절 안은 줄바꿈 하나 · 절 사이는 빈 줄 하나. 시각 · 대화 id · 세션 id · 사용자 정보를 넣지 않는다(PM2) |
| `jev_front` | `{target, target_carried, kind, gap}`(영어 — D10) | 맨 앞 판단 지시. `target` · `kind` · `gap` = 시험 `prompts/jev/front.md` 의 세 절과 같은 자리 채움(`{i}` · `{k}` · `{name}` · `{id}`) · `target_carried` = 든 후보를 읽는 법(CR7) |
| `turn_headers` | `{judgement, material, question, empty}` | 턴 메시지 머리 넷 — 시험 앱의 인라인 글자(`col_b.py:273-277`)와 같은 자리 |
| `tail_marker` | 문자열 | 답 꼬리 표식. **`system` 을 이어 붙인 글 안에 이 글자가 있어야 한다**(로더가 검사 — 없으면 시작 실패) |

- 로더 = `clinic_chat/consult/prompt.py`: 읽기 → 꼴 검사(키 · 절 `id` · 빈 값 0 · `tail_marker` 가 글 안에) → `ConsultPrompt{version, sections, system_text, jev_front, turn_headers, tail_marker, sha256}`. sha = **파일 바이트의 sha256**.
- **대화는 시작할 때 읽은 프롬프트로 끝까지 돈다**(지시 · Jev 지시 · 머리 · 표식 전부 — W-4 ③ 의 「두 프롬프트의 판이 엇갈림」 이 없다). 대화 시작 때 그 JSON 을 `CHAT_DIR/prompts/<sha256>.json` 으로 **보관**한다(gitignore 로컬 · 이미 있으면 안 쓴다) — 서버를 다시 띄워 되살린 대화도 보관본으로 돈다(LG4 · §18 B-3).
- 턴마다 지금 파일의 sha 를 다시 재서 `consult_now` 에 적는다. 시작 값과 다르면 `changed: true` — **표지만** 하고 그 대화의 글은 바꾸지 않는다. 고친 프롬프트는 **새 대화부터** 쓰인다(README · E4 순서에 적는다 — W-4 ①).
- 초안 내용(WP-2 가 쓴다): `rules` · `material` · `tail` 은 SPEC §7-1 「남김」 · 「고침」 표대로 시험 프롬프트(`prompts/common.md` · `col_b.md`)의 해당 줄을 **옮긴 것**이다 — 새 문장을 짓지 않는다. `role` · `screen` 과 「고침」 줄은 SPEC PM1 이 적은 원칙 낱말(「여러 턴 상담」 · 「시술 목록은 화면에 있다 · 이름을 늘어놓지 않는다」 · 「짧게 · 물은 것만 · 되묻기로 끝」 · 「줄 번호가 대화 전체에서 이어진다」 · `seen_lines` · 목록 요약 줄)까지만 옮긴다. `jev_front` 의 세 절은 시험 `front.md` 의 글자 그대로 · `target_carried` 한 절만 새로(영어 · CR3 의 뜻).

## 4. SPEC 과 다르게 받는 곳 ② — 화면은 DAY 디자인 킷 꼴

**결정**: 코디 보충(11-17 · 사용자) — 상담 화면은 CENTURION_DAY 디자인 킷을 참고한다. SPEC D-1 · D-3(Jinja2 + htmx 로컬 파일)과 맞고, SPEC 이 E0 로 넘긴 「htmx 판 · 라이선스 · 조각을 갈아 끼우는 길」 의 답 일부가 여기서 나온다.

따르는 규칙(`DAY/AGENTS.md` 「웹 화면」 절):

| 규칙 | 상담 화면에서 |
|---|---|
| 한 라우트가 `HX-Request` 면 조각 · 아니면 전체 페이지 | `GET /` · `GET /c/{conv_id}` · `GET /face-check` 가 그 꼴 |
| JS 는 한 파일 — 이벤트 위임 + `data-*` · 인라인 스크립트 · `eval` 금지 | `static/consult.js` 하나 · `<meta name="htmx-config">` 에 `allowEval: false` · `allowScriptTags: false`(`DAY/backend/day/templates/base.html` 의 머리 꼴) · 템플릿에 `<script>` 본문 · `on*=` 속성 0 |
| htmx 는 벤더링(CDN 금지) · 라이선스 파일 함께 | 아래 표 |
| 스타일은 medikit 토큰 · `ui.html` 매크로의 클래스만 | 템플릿에 `style=` 속성 0 · 색 · 치수 값을 템플릿에 쓰지 않는다 |
| 빌드된 CSS 는 손으로 고치지 않는다 | 가져온 `medikit.css` 를 **고치지 않는다**(가져올 때의 sha256 을 README 에 적는다) |
| POST 는 CSRF | **걸지 않는다** — 이 판은 로그인 · 세션 쿠키가 없고 `127.0.0.1` 한 사람이다(SPEC §1-3). 배포 전에 닫을 것으로 §18 B-9 |

### 4-1. 가져오는 것 · 새로 짓는 것

| 무엇 | 본(`DAY/backend/day/…`) | 상담(`clinic_chat/consult/…`) | 어떻게 |
|---|---|---|---|
| htmx 2.0.4 | `static/htmx.min.js` + `HTMX-LICENSE.txt`(MIT) | `static/` 같은 이름 | **복사**(벤더링 · 안 고침) |
| htmx SSE 확장 2.2.4 | `static/htmx-ext-sse.js` + `HTMX-EXT-SSE-LICENSE.txt`(BSD Zero Clause) | `static/` 같은 이름 | **복사** |
| medikit × HTMX 키트 CSS | `static/medikit.css`(`ms-*` 클래스 · `--ms-*` 토큰) | `static/medikit.css` | **복사**(벤더링 · 안 고침 — §4-2) |
| medikit 공통 동작 | `static/medikit.js`(진행 표시줄 등) | `static/medikit.js` | **복사**(벤더링 · 안 고침 — §4-2) |
| 글꼴 | `static/PretendardVariable.woff2`(2 MB) + `PRETENDARD-LICENSE.txt`(SIL OFL 1.1) | `static/` 같은 이름 | **복사**(없어도 `--ms-font` 가 시스템 글꼴로 내려간다 — 빼도 된다 · §18 B-8) |
| 머리 꼴 | `templates/base.html`(htmx 설정 meta · `defer` 스크립트 순서 · `#ms-progress`) | `templates/base.html` | **꼴만 따라 새로** — DAY 셸(아이콘 줄 · 헤더 · 로그아웃 · CSRF · `data-product="crm"`)은 가져오지 않는다 |
| 부품 매크로 | `templates/ui.html` 의 **기존 7개 가운데 쓰는 것**(`btn` · `input_box` · `badge` · `chip` · `card`) | `templates/ui.html` | **꼴만 따라 새로** — `ms-*` 클래스만 내는 매크로 · `day-*` 변형(`black` · `m36` …) · 한글 기본값은 뺀다 |
| DAY 전용 스타일 · 빌드 | `styles/{app.css,tailwind.config.mjs,build.mjs,medikit-preset.json}` · `static/day.css` | — | **가져오지 않는다** — Tailwind 빌드 · node 도구를 앱 레포에 들이지 않는다(§18 B-7) |
| DAY 전용 동작 · 조각 | `static/day.js` · `templates/partials/*` · `icons.html` | — | 가져오지 않는다 |
| 세 칸 배치 | — | `static/consult.css` | **새로** — 배치(좌 위 얼굴 · 좌 아래 리스트 · 우 채팅) · 말풍선 · 점. 값은 `--ms-*` 토큰만 참조(새 색 0 · 치수는 이 파일의 `:root` 토큰 블록에만) |
| 화면 동작 | — | `static/consult.js` | **새로** — 이벤트 위임 + `data-*`: 보낸 뒤 입력칸 비우기 · 채팅 끝으로 스크롤 · (E0 결과에 따라) 줄기 닫기 |
| 템플릿 | — | `templates/{page.html,face_check.html}` · `partials/{turn.html,list.html,sites.html,answer.html,step.html,error.html}` · `_face.svg` | **새로** |

- SSE 를 갈아 끼우는 길은 DAY 가 쓰는 꼴이다 — 바깥 요소에 `hx-ext="sse" sse-connect="<줄기 주소>"` · 받는 자리마다 `sse-swap="<이벤트 이름>"` + `hx-target` · `hx-swap`(`DAY/backend/day/templates/board.html:8` · `:17`). SPEC EV2 의 **(가) 이벤트 이름마다 받는 자리**다. E0 는 이 길이 조각 셋 + `delta` 덧붙임에서 서는지를 본다(§6).

### 4-2. 가져올 파일 — 확정(사용자 확인 11-17: medikit 은 공개 배포물)

medikit 은 디자이너가 전체 공개로 배포한 것이라 clinic_chat(공개 레포)에 복사 · 벤더링해도 된다(코디 보충 2). **대기는 닫혔다.** `DAY/backend/day/static/` 에서 `clinic_chat/consult/static/` 으로 **같은 이름 · 글자 그대로** 복사한다 — 아홉 파일:

| # | 파일 | 무엇 | 라이선스 파일 |
|---|---|---|---|
| 1 | `htmx.min.js` | htmx 2.0.4 | 2 `HTMX-LICENSE.txt`(MIT) |
| 3 | `htmx-ext-sse.js` | htmx SSE 확장 2.2.4 | 4 `HTMX-EXT-SSE-LICENSE.txt`(BSD Zero Clause) |
| 5 | `PretendardVariable.woff2` | 글꼴(2 MB) | 6 `PRETENDARD-LICENSE.txt`(SIL OFL 1.1) |
| 7 | `medikit.css` | medikit × HTMX 키트 CSS(파일 머리: medikit 1.3.0 값) | 9 `MEDIKIT-NOTICE.txt`(**새로** — 아래) |
| 8 | `medikit.js` | medikit × HTMX 공통 동작 | 같은 9 |

- 복사한 파일은 **고치지 않는다**. README 「상담 화면」 절에 파일마다 판 · 출처 · sha256 을 적는다(§15).
- **medikit 의 라이선스 글은 본 폴더에 파일이 없다**(`DAY/backend/day/static/` 의 라이선스 파일은 htmx · SSE 확장 · 글꼴 셋뿐이다). 워커가 라이선스 글을 지어 쓰지 않는다 — `MEDIKIT-NOTICE.txt` 에는 **사실만** 적는다: 출처(medikit × HTMX 키트 · CENTURION_DAY 사본) · 판 · 복사한 날 · sha256 · 「디자이너가 전체 공개로 배포(사용자 확인 2026-11-17)」. 배포자가 낸 라이선스 글이 따로 있으면 코디가 줄 때 그 파일로 바꾼다(§18 B-10).
- 가져오지 않는 것은 §4-1 표 그대로다(`day.css` · `day.js` · `styles/*` · `icons.html` · `partials/*`).

## 5. WP-0 — CLI 실측: E1(3턴) · E2(중단 뒤 resume) ← **첫 WP**

**SPEC**: §3-1 F3 · F6 · F7 · F9 · §3-2 CL8 · §9-2 E1 · E2 · §10 O-3 · O-6 · 검수 W-4 ④ · W-5 · N-1.
**만들 것**: `clinic_chat/consult/probe.py`(`uv run python -m clinic_chat.consult.probe --e1` · `--e2`) — `run_cli` · `child_env` · `ClaudeIngest` · `auth.check` 를 그대로 부르는 작은 실측기. CLI 판을 올릴 때마다 다시 돈다(O-5). 결과는 JSON 한 덩이를 터미널에 · `CHAT_DIR/probe/<시각>.json`(gitignore).
**글**: 회사 자료 · 시술 자료가 없는 짧은 영어 글(예: 첫 턴에 낱말 하나를 기억하게 하고 뒤 턴에 되묻는다). 시스템 글도 한두 줄.
**cwd**: 레포 밖 고정 폴더(§7 의 기본 자리) — 실측 전용 하위 폴더 `probe/`.
**인자**: SPEC CL2 에서 `--system-prompt-file` 만 `--system-prompt "<글>"` 로 바꾼 꼴(§3).

| 세션 | 호출 | 보는 것 |
|---|---|---|
| **A** — 같은 인자 3턴 | ① `--session-id <UUID4>` ② · ③ `--resume <같은 UUID>` | **E1 ①** `--max-turns 1` 을 받는가(인자 오류 없이 도는가) + **result 줄의 subtype 이 한도 오류가 아닌가**(N-1) · **②** 둘째 · 셋째 턴이 첫 턴의 낱말을 아는가 · **③** 턴마다 첫 글자 ms · 전체 ms · **④** 턴마다 `cache_read` · `cache_creation` · `input` · `output` 토큰 · **⑤** 세션 파일이 그 cwd 의 프로젝트 폴더에 생겼나(있음 / 없음만 — 경로를 보고에 쓰지 않는다) · **⑥** `thinking_seen` · `observed_model` · init 줄의 세션 id 가 준 값과 같은가(CL7) |
| A 의 넷째 호출 | **다른 cwd** 에서 `--resume <A 의 UUID>` | **W-5** — cwd 가 달라도 이어지는가(F3 실측). 3턴 값을 흐리지 않게 3턴 **뒤에** 한 번 |
| **B** — 2턴 | ① `--session-id` + 시스템 글 X ② `--resume` + **다른** 시스템 글 Y | **E1 ⑦ / F7** — 둘째 턴이 X 를 따르는가 Y 를 따르는가(두 글이 답 끝에 서로 다른 표지 낱말을 붙이게 해서 가린다) |
| **C** — E2 | ① `--session-id` 성공 ② `--resume` 을 띄우고 **답이 흐르는 중에** 프로세스 그룹을 끝냄 ③ `--resume` 다시 | **E2** — ③ 이 도는가 · 오류인가 · ② 의 질문 · 반쪽 답이 대화에 남았나. 결과는 **보고만**(CL10 ② 규칙은 코디가 바꾼다) |

**멈춤 조건**:
- A ① 에서 `--max-turns 1` 을 **안 받거나** 정상 답이 한도 오류로 끝나면 → **구현으로 넘어가지 않고 코디에게 올린다**(결정된 옵션이라 워커가 바꾸지 않는다 — CL8).
- 구독이 아닌 인증이 보이면 멈춘다(`cli.py` 와 같은 검사).
- B 의 결과가 help 글(「첫 요청의 기록을 그대로 보낸다」)과 **다르면** 코디에게 알린다(W-4 ④ — §3 의 「대화는 시작 때 프롬프트로 끝까지」 가 CLI 쪽에서 안 서는 것이므로 턴마다 같은 글을 주는 것으로 충분한지 코디가 본다). 멈춤은 아니다.
- 다른 cwd resume 이 안 되는 것은 멈춤이 아니다(CL9 가 거기에 기대지 않는다) — 보고만.

**완료 조건**: 위 표의 칸이 전부 값으로 채워졌다(호출 9 번 — A 4 · B 2 · C 3) · 세션 파일을 지우지 않았다 · 포트를 열지 않았다.
**검증**: `uv run python -m clinic_chat.consult.probe --e1` → `--e2` · `uv run ruff check clinic_chat/consult/probe.py`.

## 6. WP-1 — 화면 바탕: 의존 · 디자인 킷 · 빈 화면(E0)

**SPEC**: §2-3 · §4-1 · §4-3 EV1 ~ EV5 · §4-5 · §9-2 E0 · D-1 · D-3 · 검수 N-7 · §4(이 문서).
**만들 것**: `pyproject.toml`(직접 의존에 `jinja2` · `python-multipart==0.0.33` — `uv add` 뒤 `uv.lock` 이 고른 `jinja2` 판을 `==` 로 고정 · 이 레포의 의존은 전부 `==` 다) · `clinic_chat/consult/{__init__.py,__main__.py,server.py}` · `consult/static/*`(§4-1) · `consult/templates/*` · `tests/test_consult_page.py`.

| 무엇 | 구현 |
|---|---|
| 앱 | `create_app(settings, *, turn_fn=…)` — 턴을 도는 함수를 갈아 끼울 수 있게(시험 화면 `create_app(run=…)` 꼴 — `web/server.py:108`). `python -m clinic_chat.consult [--port N]` · 호스트는 `127.0.0.1` 고정 · 포트 기본 `CHAT_PORT`(18222) |
| 페이지 | `GET /` 새 `conv_id` 로 세 칸의 빈 틀 · `GET /c/{conv_id}` · `GET /static/…` · `HX-Request` 면 조각(§4). Jinja2 **자동 이스케이프 켬**(EV4) |
| 빈 자리 | SPEC §4-5 의 `data-slot` 이름 전부를 템플릿에 자리로 둔다(글 없음). 자리 수를 시험이 센다 |
| **가짜 턴** | `consult/fake_turn.py` — 외부 호출 0 으로 `step` → `list` → `sites` → `delta` 여럿 → `done` 을 내는 턴(값은 코드 값 · 영문 자리 글자). env `CHAT_FAKE_TURN=1` 일 때만 `turn_fn` 으로 쓰인다 — E0 와 템플릿 시험 전용 |
| 줄기 | `Live` 꼴(이벤트 목록 + 깨우기 · 늦게 붙으면 처음부터 · `Last-Event-ID` 다음부터) · `StreamingResponse` 로 SSE(`sse-starlette` 는 안 쓴다) · 자료는 HTML 조각 한 줄(줄바꿈은 SSE `data:` 줄 여럿으로) |
| 받는 자리 | `#procedure-list`(`sse-swap="list"`) · `#face-marks`(`sse-swap="sites"` — **통째** 바꿈 · EV3) · 이 턴 답 말풍선 본문(`sse-swap="delta"` + `hx-swap="beforeend"` · `sse-swap="done"` 은 통째) · 상태 자리(`sse-swap="step"`) |

**E0 에서 정할 것**(워커가 18223 에서 `curl` 로 줄기를 받고 · 코디가 18222 에서 눈으로 본다):

| # | 확인 | 다르면 |
|---|---|---|
| E0-1 | 이벤트 이름마다 받는 자리(가)가 조각 셋에서 서는가 | (나) `hx-swap-oob` 로 — 이벤트 이름 · 조각 · 받는 자리 id 는 그대로(EV2) |
| E0-2 | `#face-marks` 통째 바꾸기가 SVG 로 그려지는가(SVG 이름 공간) | SVG 를 감싼 `<div>` 통째로(EV3) |
| E0-3 | `delta` 덧붙임 뒤 `done` 이 본문을 통째 바꾸는가 · 다시 붙어도 끝 꼴이 같은가(EV5) | 보고 |
| E0-4 | **줄기 닫기** — 서버가 끝낸 뒤 브라우저가 다시 붙기를 되풀이하지 않는가. SSE 확장의 `sse-close="<이벤트>"` 는 이름 하나를 받는다(`DAY …/htmx-ext-sse.js:235`) | §18 B-4 의 제안으로 |
| E0-5 | 이벤트 이름 **`error`** 가 브라우저 `EventSource` 의 연결 오류 이벤트(`error`)와 겹쳐 확장의 다시 붙기 처리를 건드리는가 | §18 B-4 |
| E0-6 | §4-2 의 아홉 파일이 `static/` 에 있고 본과 sha256 이 같다 | — |

**완료 조건**: T8(이스케이프) · T17(문구 0 — 예외는 §17 W-7) · T24(조각 / 전체 · 인라인 스크립트 0 · `style=` 0 · `data-slot` 자리 수)가 선다 · E0-1 ~ E0-6 이 「됨 / 안 됨(본 것)」 으로 채워졌다(브라우저 눈 확인 칸은 「코디」 로 남긴다) · 18223 을 내렸다.
**검증**: `uv run pytest tests/test_consult_page.py -q` · `CHAT_FAKE_TURN=1 uv run python -m clinic_chat.consult --port 18223` → `curl -N` 으로 줄기 한 번 → 내림.

## 7. WP-2 — 프롬프트 JSON · 설정 칸

**SPEC**: §2-4 · §7(§3 으로 바꿔 받음) · PM1 · PM2 · PM4 · 검수 W-4 · W-5.
**만들 것**: `prompts/consult.json` · `clinic_chat/consult/prompt.py` · `clinic_chat/config.py`(칸) · `.env.example`(이름) · `tests/test_consult_prompt.py`.

설정 칸(SPEC §2-4 표 그대로 + 둘):

| env | 기본 | 비고 |
|---|---|---|
| `CHAT_PORT` · `CHAT_MODEL` · `CHAT_FALLBACK_MODEL` · `CHAT_EFFORT` · `CHAT_TURN_TIMEOUT_SEC` · `CHAT_MAX_TURNS` · `CHAT_CARRY_TURNS` · `CHAT_DIR` | 18222 · `sonnet` · `haiku` · `low` · 120 · 20 · 1 · `RUNS_DIR/consult` | SPEC §2-4 |
| `CHAT_CLI_CWD` | **사용자 캐시 폴더 아래 고정 이름**(W-5): `XDG_CACHE_HOME` 이 있으면 그 아래 · 없으면 macOS 는 홈의 `Library/Caches` · 그 밖은 홈의 `.cache` → `clinic-chat/consult-cli` | `TMPDIR` 과 무관 · 레포 밖(CL9-1) · 없으면 만든다 · 지우지 않는다. 장부에는 경로를 안 적는다(CL9-3) |
| `CHAT_PROMPT_FILE` | `prompts/consult.json` | 시험이 다른 파일을 물리는 자리(§18 B-5) |
| `CHAT_FAKE_TURN` | 꺼짐 | E0 전용(§6) |

**완료 조건**: T19 — JSON 꼴 검사(키 빠짐 · 빈 절 · `tail_marker` 가 글에 없음 → 시작 실패) · 이어 붙인 글이 절 순서대로 · sha = 파일 바이트 · 보관본이 `CHAT_DIR/prompts/<sha>.json` 에 한 번만 · 지금 칸의 기본값이 안 바뀜(`walk_settings()` 꼴 그대로). `system` 글에 시각 · id 자리 채움이 없다(PM2). `jev_front` 의 `target` · `kind` · `gap` 이 시험 `front.md` 의 절과 글자 그대로 같다(시험이 대조).
**검증**: `uv run pytest tests/test_consult_prompt.py -q`.

## 8. WP-3 — 실행기: `llm/chat.py` · `llm/chat_cli.py`

**SPEC**: §3-2 CL1 ~ CL7 · §3-3 CL9 · §3-4 CL10 ~ CL12 · §3-5 · §3-6 SD1 ~ SD5 · T1 ~ T5.
**만들 것**: `clinic_chat/llm/chat.py`(인터페이스 · 결과 꼴) · `clinic_chat/llm/chat_cli.py` · `tests/test_consult_cli.py` · `tests/fake_cli/fake_cli.py`(가지 추가).

| 규칙 | 구현 |
|---|---|
| SD1 · SD2 | `ChatLLM.turn(conv, user_message, prompt, history)` → §3-5 결과. `history`(앞 턴의 user 메시지 · 꼬리째 답 목록)는 CLI 구현이 **쓰지 않는다** · 글자 조각은 `progress.emit("delta")` |
| CL2 · CL3 | `chat_args(conv, prompt, mode)` — 첫 턴 `--session-id <UUID>` · 다음 턴 `--resume <같은 UUID>` 말고는 **글자 그대로 같다**. `--system-prompt <prompt.system_text>`(§3) · `--model` · `--fallback-model` · `--effort` · `--max-turns 1` · 격리 인자는 `cli.py:80-84` 와 같은 꼴에서 `--no-session-persistence` 만 뺀 것. 프롬프트는 stdin |
| CL4 | 인자에 `--no-session-persistence` · `--continue` · `--mcp-config` · `--max-budget-usd` · `--bare` · `--json-schema` 가 없다 |
| CL5 · CL7 | `ClaudeIngest` 로 줄을 읽되 **init 줄을 한 번 더 본다** — 세션 id 가 준 값과 다르면 오류 · 구독이 아니면 `StopRun`. 도구 호출이 보이면 그 턴은 오류(`ClaudeIngest` 가 모은 `tool_calls` 가 비어 있지 않음) |
| CL6 | 세션 UUID(UUID4)와 `conv_id` 는 따로 |
| CL9 | 고정 cwd(`CHAT_CLI_CWD`) — 턴 뒤에 지우지 않는다 |
| CL10 | 상태 `new` · `open` · `broken` — ① `new` 실패 → **새 UUID** · `new` 그대로 ② `open` 에서 띄운 뒤 실패(시간 초과 · 종료 코드 · 도구 호출) → `broken` ③ `open` 에서 띄우기 전 실패(인증) → `open` 그대로 · 그 턴만 오류 |
| CL11 | 한도 = `CHAT_TURN_TIMEOUT_SEC`(`run_cli` 가 그룹째 끝낸다) |
| CL12 | 대화마다 잠금(겹친 턴은 받지 않고 오류) · 앱 전체 세마포어 = `CLI_MAX_CONCURRENT`(`cli.py:294-298` 꼴을 상담 쪽에 둔다 — `_semaphore` 는 밑줄 이름) · 줄 서는 중이면 `step` |
| §3-5 | 결과 = `answer_raw` · `error{kind, stage, detail}` · `tokens`(`USAGE_KEYS`) · `observed_model(s)` · `thinking_seen` · `stop_reason` · `timing{ttft_ms, total_ms}` · `llm{kind, session_id, mode, model, effort, cli_version, returncode}` |
| SD5 | `anthropic` 의존을 더하지 않는다 · 자식 env 는 `child_env()` |

- E1 ⑥ 의 값(WP-0)이 `ClaudeIngest` 가 init 줄에서 세션 id 를 **어느 키로** 주는지 알려 준다 — 그 키를 그대로 쓴다(짐작으로 이름을 짓지 않는다).
- 가짜 CLI: argv 에 `--session-id` · `--resume` 이 있으면 그 값을 init 줄의 세션 id 로 되돌려 주고, env 로 「조각 몇 개 뒤 비정상 종료」 · 「다른 세션 id」 · 「도구 호출 줄」 을 낼 수 있게 한다(지금 가지 `FAKE_CLI_EXIT` · `FAKE_CLI_AUTH` 꼴 — 지금 시험이 쓰는 동작은 그대로).

**완료 조건**: T1 · T2 · T3 · T4 · T5 가 가짜 CLI 로 선다 · 인자 대조 시험이 CL2 의 인자를 낱낱이 센다.
**검증**: `uv run pytest tests/test_consult_cli.py tests/test_cli.py -q`.

## 9. WP-4 — 대화 장부: `consult/ledger.py`

**SPEC**: §5-1 LG1 ~ LG5 · §3-4 CL13 · CL14 · T16 · 검수 W-3 · W-4.
**만들 것**: `clinic_chat/consult/ledger.py` · `tests/test_consult_ledger.py`.

| 규칙 | 구현 |
|---|---|
| LG1 · LG2 | `CHAT_DIR/turns.jsonl` 한 파일 · 덧붙이기만(`RunStore._append` 꼴) · `runs.jsonl` 과 섞지 않는다 |
| **W-3 ①** | 턴마다 줄 **둘**: 띄우기 **전에** 시작 줄 `{conv_id, turn, phase: "start", asked_at, question, llm{session_id, mode}}` · 끝나면(성공 · 오류 모두) 맺는 줄 `{…, phase: "end", …LG3 의 칸}`. LG1 의 「턴 하나에 한 줄」 은 **맺는 줄**이 그 한 줄이다 |
| LG3 | 맺는 줄의 칸 = SPEC §5-1 표 전부. `prompts` 만 §3 대로 `{consult_at_start, consult_now, changed}` 이고 `version` 도 함께 |
| LG4 · **W-3 ①** | 같은 `conv_id` 로 오면 파일에서 되읽어 메모리를 세운다. **시작 줄만 있고 맺는 줄이 없는 턴이 있으면 그 대화는 `broken`**(서버가 턴 도중 죽었다 — CLI 자식은 따로 살아 세션에 턴을 남겼을 수 있다 · `cli_process.py:59`) |
| **W-3 ②** | 「실은 gid → 줄 번호」 · `next_n` · 요약 줄 장부는 **지금 세션에서 성공한 턴**(맺는 줄의 `error` 가 `null`)만 센다 |
| **W-3 ③** | 든 후보(이어 묻기)는 `error` 가 없는 턴에서만 뽑는다(§14) |
| CL13 | 성공한 턴 수가 `CHAT_MAX_TURNS` 에 닿으면 더 받지 않는다 |
| CL14 | 대화 첫 턴의 허브 `build.gold_hash` 를 적는다 · 뒤 턴의 걷기가 낸 `build` 가 다르면 그 대화는 끝(그 턴은 오류로 맺는다) |
| LG5 | 키 · 홈 경로 · 세션 파일 경로 · cwd 경로를 적지 않는다 — 시험이 줄 글자에서 홈 경로 꼴을 찾는다 |

**완료 조건**: T16(굵은 칸 여섯 · 되읽어 `open` · 다음 줄 번호 이어짐) · T20(맺는 줄 없는 턴 → `broken`) · T21(오류 턴의 재료 · 대상이 「실은 gid」 · `next_n` · 든 후보에 안 든다)이 선다.
**검증**: `uv run pytest tests/test_consult_ledger.py -q`.

## 10. WP-5 — 재료 덧붙이기: `consult/material.py`

**SPEC**: §5-3 AP1 ~ AP8 · §4-4 · T14 · T15 · 검수 W-1 · W-2.
**만들 것**: `clinic_chat/consult/material.py` · `clinic_chat/consult/tail.py` · `tests/test_consult_material.py`.

| 규칙 | 구현 |
|---|---|
| **W-1** | **걷기 안의 줄 번호는 1 부터 그대로**다(`build()` · `gate` 를 안 고친다 — K1 이 통과한다). 상담 `material.py` 가 걷기 **뒤에** `Material.groups` 를 복사해 **gid → 대화 줄 번호**로 옮겨 적는다: 새 gid 만 `next_n` 부터 새 번호 · 앞 턴에 실은 gid 는 옛 번호 · 묶음 머리 `lines` 와 표지 `conflict_lines`(짝 줄 번호 — `walk/material.py:195-199`)도 옮긴 번호로(짝이 앞 턴 줄이면 그 옛 번호). 새 줄이 0 인 묶음은 뺀다. 글로 만드는 것은 `to_lines`(안 고침) |
| AP1 · AP3 | 이번 턴 메시지에는 새 gid 의 줄만 · 다시 읽은 앞 턴 줄의 번호는 「앱 판정」 의 `seen_lines[]` 로 |
| AP4 · AP5 | **목록 요약 줄** — `concern_candidates` 조회(`Read.call.tool`)와 그 이어 조회(후보별 profile — `VRow.followup`)에서**만** 온 행은 줄마다 싣지 않고 계열 하나에 한 줄 `{n, modality_name, procedures(수), reach[], concern_match[], mechanism_name[]}` + 머리의 `inherited_from`. 다른 조회에서도 온 gid 는 칸째 싣는다. 장부에 `{n, summary: true, gids[]}` |
| **W-2** | 요약 줄의 `gids[]` 는 **근거 되짚기용**이다 — 「실은 gid」 장부에 **넣지 않는다**. 그래서 뒤 턴이 그 행을 칸째 읽으면 새 줄로 실린다. 같은 요약((고민, 계열) · gid 집합이 같음)은 다시 싣지 않고 그 줄 번호를 `seen_lines` 로(§18 B-6) |
| AP6 · AP7 | 그 밖의 행은 SPEC-002 §3-2a 의 칸 그대로 · 이름 목록(`roster`)은 싣지 않고 `answer_check` 도 안 돈다 |
| AP8 | 한 턴 메시지가 `ANSWER_INPUT_MAX_TOKENS` 를 넘으면 「실행 중단」(사유 `FT5`) — 빈 재료로 LLM 을 부른다(`col_b.py:419-422` 와 같은 길 · 어림은 `fold.est_tokens`) |
| 메시지 | 순서 = 앱 판정(JSON) → 자료 → 질문(질문이 맨 뒤 — `col_b.py:272-283`). 머리 글자는 `prompt.turn_headers`(§3). 앱 판정 = `judgement(w)`(`col_b.py:252`) + `seen_lines[]` + `turn` |
| 꼬리 | `consult/tail.py` — `split_tail(text, mark)` · `TailFilter(mark)`. 표식을 인자로 받는 것 말고는 `col_b.py:286-332` 와 **동작이 같다**(`_TailFilter` 는 밑줄 이름이라 가져다 쓰지 않는다 — SPEC §2-2). 꼬리의 줄 번호는 대화 번호다 |

**완료 조건**: T14(둘째 턴 메시지에 첫 턴 gid 없음 · 번호 이어짐 · 다시 읽은 줄은 `seen_lines` 에만 · **걷기 gate 통과** · `walk/material.py` 의 sha 가 그대로) · T15(시술 이름 줄 없음 · 계열마다 한 줄 · 장부에 `gids[]` · **첫 턴 요약에 든 행을 둘째 턴이 읽으면 칸째 실린다**) · T7 의 꼬리 쪽(표식이 조각 둘에 걸쳐도 안 흘림) · T26(같은 표식에서 상담 꼬리 함수 결과 = `col_b` 의 결과 — 본문 · `answer_lines` · 흘린 글)이 선다.
**검증**: `uv run pytest tests/test_consult_material.py -q`.

## 11. WP-6 — 시술 리스트: `consult/listing.py`

**SPEC**: §6-1 PL1 ~ PL9 · T9 · U-13 = (a) · 검수 N-4.
**만들 것**: `clinic_chat/consult/listing.py` · `consult/templates/partials/list.html` · `tests/test_consult_listing.py`.

| 규칙 | 구현 |
|---|---|
| PL1 | 재료 = 이번 턴 `Walk.reads` 가운데 `call.tool == "concern_candidates"` · `purpose == "read"` 인 조회의 응답(`ReadAll.as_response()`)뿐. LLM 답 · Jev 점수는 닿지 않는다 |
| **N-4** | 같은 고민의 조회가 둘 이상이면(부위로 거른 것 + 안 거른 것 — BR6) **gid 합집합으로 한 리스트**(처음 나온 순서) |
| PL2 · PL3 · PL4 | 행 = 시술(`procedure_code`) · 층 = `reach[]` 합집합(gold 값 그대로) · `concern_match[]` 합집합 · 계열 = 후보 profile 의 `modality_name`(빈 것은 빈 계열 묶음 하나 — 이름을 짓지 않는다) · 순서 = 허브가 낸 순서 |
| PL5(U-13) | `modality_only[]` · `unreached[]` 는 시술 행에 섞지 않고 **아래 따로 묶음 둘로 전부** — 머리 글은 빈 자리(`data-slot="list-section-modality-only"` · `list-section-unreached`) |
| PL6 · PL7 | 윗고민에서 물려받았으면 머리에 값으로 · 고민이 둘 이상이면 고민마다 리스트 하나 |
| PL8 · PL9 | 읽지 않았으면 `list` 를 안 보낸다 · 행에 `data-procedure-code`(누르는 동작 없음) |
| 장부 | `list` = SPEC §6-1 끝의 꼴(행마다 gid) |

- 응답의 키 이름은 실물 꼴로 맞춘다 — `tests/test_clients.py` 의 `REAL_KEYS` 와 허브 응답 한 건(WP-10 의 읽기)으로 대조한다. 키가 SPEC 글과 다르면 지어 맞추지 말고 보고.

**완료 조건**: T9 · T23(같은 고민 두 조회 → 한 리스트 · gid 중복 0)이 가짜 허브로 선다.
**검증**: `uv run pytest tests/test_consult_listing.py -q`.

## 12. WP-7 — 한 턴 흐름 · 라우트 · 이벤트: `consult/turn.py` · `server.py`

**SPEC**: §4-1 · §4-2 TF1 ~ TF6 · §4-3 EV1 ~ EV5 · §4-4 · T6 · T7 · 검수 W-6 · W-8.
**만들 것**: `clinic_chat/consult/turn.py` · `server.py`(라우트) · `tests/test_consult_turn.py`.

| 단계 | 구현 |
|---|---|
| TF1 | `POST /c/{conv_id}/turns`(폼 `text`) — 빈 글 · `broken` · 턴 한도 · 앞 턴 도는 중이면 오류 조각. 아니면 턴 번호를 매기고 **시작 줄을 쓰고**(§9) 곧바로 「내 말풍선 + 빈 답 말풍선」 조각 |
| TF2 | `walk(question, deps, carry=…, instr=prompt.jev_front)`(§14) · 걷기의 `step` 을 줄기로 |
| TF3 | 걷기가 끝나면 LLM 을 기다리지 않고 `list` → `sites` 를 보낸다. 「범위 밖」 · 「입구 없음」 · 「실행 중단」 에서는 둘 다 안 보낸다 |
| TF4 · TF5 · TF6 | 메시지(§10) → 실행기(§8) → `delta` 는 표식 앞까지만 → `done` 은 꼬리 뗀 본문 통째 → 맺는 줄 · 세션 상태 옮김. 걷기가 「실행 중단」 이어도 LLM 을 부른다(빈 재료) |
| **W-6** | **턴은 구독자와 무관하게 끝까지 돈다**(탭을 닫아도 · 새로 고쳐도) — 턴은 서버의 작업으로 돌고 줄기는 `Live` 를 읽기만 한다(시험 화면과 같은 꼴). **이 판에 취소 라우트는 없다** |
| 시간 | `first_list_ms`(받은 뒤 → `list` 보냄) · `ttft_ms`(받은 뒤 → 첫 `delta`) · `total_ms` · `parts{jev_ms, hub_ms, llm_ms}` |
| `GET /c/{conv_id}` | 장부의 턴들(질문 · 답 본문)과 마지막 리스트 · 점을 다시 그린다 |

**W-8 — 사용자 눈에 보이는 기본값 넷(코디 통보감 C-19 ~ C-22)**: 이 WP 가 그대로 짓는다 — **C-19** 턴 한도(20)에 닿으면 그 대화는 더 받지 않는다 · **C-20** 허브 `gold_hash` 가 바뀌면 그 대화는 끝(코디가 18105 를 다시 띄우면 열린 대화가 끝난다) · **C-21** 한 턴 메시지가 한도를 넘으면 「실행 중단」(쪽 나눔 없음) · **C-22** `open` 에서 답 중 실패는 전부 `broken`. 화면은 빈 자리(`turn-limit` · `error-<종류>`)에 종류 코드만 단다.

**완료 조건**: T6(순서 `list` → `sites` → 첫 `delta` → `done` · 「범위 밖」 턴에 `list` · `sites` 없음) · T7(화면 쪽) · T22(구독자가 끊겨도 맺는 줄이 써진다 · CLI 가 끝까지 돈다 · 다시 붙으면 끝 꼴이 같다)가 가짜 셋으로 선다.
**검증**: `uv run pytest tests/test_consult_turn.py -q`.

## 13. WP-8 — 부위 · 얼굴 SVG · 좌표표

**SPEC**: §6-2 SI1 ~ SI7 · §6-3 HN1 ~ HN4 · §8 FC1 ~ FC10 · §8-4 · 부록 B · T10 · T11.
**만들 것**: `clinic_chat/consult/face_coords.py` · `consult/sites.py` · `consult/templates/_face.svg` · `partials/sites.html` · `face_check.html` · `tests/test_consult_sites.py`.

| 무엇 | 구현 |
|---|---|
| 얼굴 그림 | **손으로 새로 그린 SVG**(선 그림 · path · `viewBox="0 0 590 1060"`). 밑그림 PNG 는 눈금을 얹어 **보기만** 한다 — 기계로 뽑은 윤곽을 쓰지 않고 · 레포에 두지 않는다(FC1). 세부(눈동자 · 눈썹 결)는 줄인다. 선 그림 층 + 점 층 `#face-marks` 가 한 SVG 안 |
| 좌표표 | `face_coords.py` — `site_code → {shape, points}`. **부위 60 전부**(부록 B 의 분류 그대로: `point` 17 · `pair` 27 · `area` 8 · `line` 4 · `none` 4) · 좌표는 `point` · `pair` **44 부위(점 71)** · 0 ~ 1 비율. 부위 이름은 주석으로만(FC9). 조사 §3-3 의 예 값은 쓰지 않는다 — **워커가 초안을 찍는다** |
| 점 · 라벨 | `point` → 점 1 · `pair` → 점 2 · `area` · `line` · `none` · **표에 없는 코드** → 얼굴 아래 라벨(이름 = 허브가 낸 값) · 같은 부위는 한 번 · 부위 0 이면 **빈 `sites` 조각**(앞 점을 지운다) · 점에 `data-site-code` · 점 옆 글 없음 |
| `/face-check` | 좌표표의 점을 전부 켜고 점마다 부위 코드를 보이는 확인용 한 장(코드 값 — 문구 아님) |
| **눈 확인** | **워커는 초안까지**다. 화면으로 보는 것은 **코디가 18222 를 띄우고 사용자가** 한다 — 어긋난 부위 코드를 받으면 워커가 **그 코드의 좌표만** 고친다(§8-4 의 차례 1 → 5) |

**허브 의존(계약 한 줄 — 허브 몫은 WP 가 아니다)**: 고민 부위 코드는 **SPEC-001 0.7**(별도 발주)이 `concern_candidates` 응답 머리에 낸다 — (고민 코드, 부위 코드, 부위 이름, 묶임 id) 쌍의 목록(HN1 ~ HN4 · 칸 이름은 0.7 이 정한다).

- 앱은 그 칸을 읽는 곳을 **한 함수**(`sites.from_response`)에 두고 칸 이름을 상수 하나로 든다. **칸이 없으면 점 0 · 라벨 0 으로 오류 없이 돈다** — `sites` 조각은 빈 꼴이다. 다른 길(이름 글자 맞춤 · silver CSV 읽기)로 메우지 않는다(SPEC §6-3).
- 0.7 이 칸 이름을 정하면 상수 한 줄을 맞춘다 → 그때 점이 켜진다. 그 전의 단위 시험은 가짜 허브에 임시 이름으로 실어 돈다(시험이 이름을 인자로 준다).

**완료 조건**: T10 · T11(FC10 — 코드 꼴 · 60 · 꼴별 수 · `points` 길이 · 0 ~ 1 · `pair` 는 x 가 0.5 양쪽) · T25(허브 응답에 부위 칸이 없음 → 빈 조각 · 오류 0 / 있음 → 점 · 라벨)가 선다 · 레포에 PNG · 뽑은 윤곽이 없다(`git status` 로 확인).
**검증**: `uv run pytest tests/test_consult_sites.py -q`.

## 14. WP-9 — 이어 묻기: `consult/carry.py` + 함께 쓰는 코드의 선택 인자

**SPEC**: §5-2 CR1 ~ CR7 · ST3 · T12 · T13 · U-12 = (a) · 검수 W-3 ③ · N-5 · N-6.
**고칠 곳(함께 쓰는 코드 — 전부 기본값이 지금 동작)**: `clinic_chat/walk/front.py` `front(…, carry=None, instr=None)` · `clinic_chat/columns/col_b.py` `walk(…, carry=None, instr=None)`(넘기기만) · `clinic_chat/walk/jev_requests.py` `ask_front`(든 후보의 지시 절) · `clinic_chat/walk/calls.py:59`(`Entry.by` 값 `carried`).
**만들 것**: `clinic_chat/consult/carry.py` · `tests/test_consult_carry.py`.

| 규칙 | 구현 |
|---|---|
| CR1 · **W-3 ③** | 든 후보 = 장부에서 「대상이 있는」 가장 가까운 앞 턴 `CHAT_CARRY_TURNS` 개의 `targets[]`. 종료 상태가 「범위 밖」 · 「입구 없음」 · 「실행 중단」 인 턴과 **`error` 가 있는 턴**은 건너뛴다 |
| CR2 | `front()` 가 resolve 후보 **뒤에** 든 후보를 붙여 한 요청으로 묻는다(coverage 도 함께). 이번 글에서 맞은 것과 같은 (표, 코드)는 다시 넣지 않는다 |
| `instr` | `front()` 는 지금 Jev 지시를 **안에서** 읽는다(`prompts.jev_sections("front")`). 상담은 `prompts/consult.json` 의 `jev_front` 를 써야 하므로 선택 인자 `instr`(기본 없음 = 지금처럼 시험 파일을 읽는다)가 하나 더 든다 — §18 B-2 |
| CR3 | 든 후보의 설명 = `matched: null` · `carried_from: <앞 턴 번호>` · 지시는 `target_carried` 절(절이 없으면 `target`) |
| CR4 | **든 후보는 yes 일 때만 대상** — 사이 값 · no 는 `dropped`. TG2 · TG3 을 걸지 않는다(`front.py:306-307` 의 덮인 조각 가지와 같은 꼴의 가지 하나) |
| CR5 | 대상이 된 든 후보는 `by` = `carried` · `read_as{by: "carry", from_turn}`. `read_as` 값을 닫힌 목록으로 검사하는 곳이 있으면(`walk/gate.py` K4 · `walk/material.py` `llm_marks`) 그 값만 더한다 — 있으면 §13 표에 줄을 더해 보고한다 |
| CR6 | 이번 글의 후보가 0 이고 든 후보만 있으면 든 후보로 같은 요청 · 든 후보가 전부 `dropped` 면 지금의 입구 고르기 길 |
| CR7 | 시험 프롬프트 `prompts/jev/front.md` 는 안 고친다(T18) |
| 하지 않는 것(U-12) | 앞 턴 **리스트의 시술**을 후보에 넣어 좁히는 것 — 0.2 |

**완료 조건**: T12(든 후보가 붙는다 · yes 만 대상 · 사이 값 · no 는 `dropped` · 같은 것은 다시 안 넣음 · **후보 수가 한 묶음(`jev_batch_size` 32) 안이면** Jev 요청 수가 안 늘어난다 — N-5) · T13(`carry` · `instr` 를 안 주면 `front()` 결과 · trace 가 지금과 같다) · **걷기 시험 묶음 전부 통과**.
**검증**: `uv run pytest tests/test_consult_carry.py tests/test_walk_front.py tests/test_walk_core.py tests/test_covered.py tests/test_columns.py -q`.

## 15. WP-10 — 실물 E3 · README · 전체 검증

**SPEC**: §9-2 E3 · §9-3 · CL9-2 · O-11 · 검수 N-6.
**만들 것**: `clinic_chat/consult/probe.py` 에 `--e3`(서버 없이 한 턴 흐름을 세 번 — 줄기 이벤트를 메모리로 받는다) · `README.md` 「상담 화면」 절 · `.env.example`.

**E3**(허브 18105 읽기 · Jev · 구독 CLI — 조사 §5-1 · §5-2 의 세 턴 꼴: 고민 → 그중 한 계열 → 다른 계열과 차이):

| 보는 것 | 값 |
|---|---|
| 턴마다 | `first_list_ms` · `ttft_ms` · `total_ms` · `parts` · 종료 상태 · 새 줄 수 · `seen_lines` 수 · 요약 줄 수 · 토큰(`cache_read` · `cache_creation`) · `thinking_seen` · `observed_model` |
| 든 후보 | 후보마다 Noul · 결정(`carried` / `dropped`) |
| 첫 턴 | 허브 응답 행 수(O-11 — 고민과 부위가 같은 이름으로 함께 잡힐 때) · 리스트의 시술 · 계열 · 「계열 층만」 · 「그 밖」 수 |
| 이벤트 | `list` → `sites` → 첫 `delta` → `done` 의 순서 · 꼬리가 `delta` · `done` 에 없음 |
| **N-6** | 둘째 턴은 앞 리스트로 좁히지 않고 계열 전체로 답한다(U-12 (a) — 알고 가는 어긋남). 보고에 **어긋남으로 표시**하고 실패로 세지 않는다 |

- **답의 옳고 그름은 기준이 아니다**(프롬프트가 초안) — 수와 배관만.
- 줄기 한 번은 실제 서버로도 본다: `uv run python -m clinic_chat.consult --port 18223` → `curl` 로 한 턴 → 내림.
- `.env` 가 없거나 Jev · 허브가 안 닿으면 「못 돌림」 으로 보고한다(코디가 돌린다).

**README 「상담 화면」 절**: 띄우는 법(`uv run python -m clinic_chat.consult` · 포트 18222) · 전제(허브 · `.env` · 구독 CLI) · **대화 글이 사용자 홈의 CLI 세션 파일에 평문으로 남고 앱이 지우지 않는다**(CL9-2) · **프롬프트(`prompts/consult.json`)를 고쳤으면 새 대화**(W-4) · 장부 자리(`CHAT_DIR/turns.jsonl`) · `/face-check` · 실측기(`consult.probe`) · 벤더링한 파일의 판 · 라이선스 · sha256.

**전체 검증(여기서 한 번)**:

```
uv run ruff check .
uv run pytest -q                      # 기준선(WP-1 에 적은 수) + 새 시험 · 실패 0
git -C <APP-WT> status --porcelain    # allowed_paths(§2) 밖의 변경 0 · PNG 0
```

**grep**:

| 무엇 | 기대 |
|---|---|
| `clinic_chat/consult/**` · 템플릿의 한글 문장(주석 · `data-slot` 이름 · §17 W-7 의 예외 빼고) | 0(T17) |
| 템플릿의 `style=` · `<script>` 본문 · `on[a-z]+=` | 0 |
| 상담 코드 · 템플릿 · `prompts/consult.json` 의 키 꼴 · 비밀값 · 홈 경로 · 내부 주소 | 0 |
| `clinic_chat/web/` · `prompts/*.md` · `prompts/jev/*.md` · `walk/material.py` · `walk/gate.py` · `llm/cli.py` 의 sha | 그대로(T18) |
| `anthropic` 의존 · `--no-session-persistence` · `--bare`(상담 인자에) | 0 |

## 16. 순서 · 의존 · 실물의 몫

```
WP-0(E1 · E2) ──[멈춤 조건]──┐
WP-1(화면 바탕 · E0) ────────┼─ WP-7(한 턴 · 라우트) ─ WP-8(부위 · 얼굴) ─ WP-9(이어 묻기) ─ WP-10(E3 · 전체 검증) ─ [코디: 18222 · 사용자 E4]
WP-2(JSON · 설정) ─ WP-3(실행기) ─ WP-4(장부) ─ WP-5(재료) ─ WP-6(리스트) ─┘
[별도 발주: SPEC-001 0.7 → 허브 부위 칸] ·········▶ WP-8 의 상수 한 줄(오면 켜짐)
```

| 무엇 | 근거 |
|---|---|
| WP-0 먼저 | `--max-turns 1` 을 못 받으면 실행기 꼴이 바뀐다(CL8) · E1 ⑥ 이 init 줄의 세션 id 키를 알려 준다(WP-3) · F7 결과가 §3 의 전제다 |
| WP-1 은 WP-0 과 나란히 가능 | 외부 호출 0 · 겹치는 파일 없음 |
| 허브 0.7 을 기다리지 않는다 | SPEC C-18 은 0.7 을 맨 앞에 뒀지만 지시서가 「그 칸이 없으면 점 없이 동작 · 오면 켜지는 꼴」 로 바꿨다 — 앱은 한 줄로 켠다(§13) |
| WP-9 를 뒤에 | 함께 쓰는 코드를 고치는 유일한 WP — 나머지가 선 뒤에 한 번에 |
| 한 워커가 차례로 | `consult/turn.py` · `server.py` · 장부가 서로 물린다 — 나눠 발주하지 않는다 |

| 실물 | 누가 | 포트 | 무엇 |
|---|---|---|---|
| E1 · E2 | **워커** | 없음 | §5 — 구독 CLI 9 번 |
| E0 | **워커**가 짓고 `curl` 로 확인 → **코디**가 띄워 눈으로 | 워커 18223(확인 뒤 내림) · 코디 18222 | §6 — E0-1 ~ E0-6 |
| E3 | **워커**(안 되면 코디) | 없음 + 18223 한 번(내림) · 18105 는 읽기만 | §15 |
| `/face-check` 좌표 | 워커 초안 → **코디**가 18222 → **사용자** 눈 → 워커가 그 코드만 고침 | 코디 18222 | §13 |
| E4 | **코디가 18222 를 띄우고 사용자가 확인** | 코디 18222 | 리스트 · 점이 답보다 먼저 · 답이 리스트를 다시 읊지 않음 · 꼬리가 화면에 없음 · 빈 자리 목록 · **프롬프트를 고쳤으면 새 대화로 본다**(W-4) |
| 건드리지 않는 것 | — | 18210 · 18005 · 18105 · 18220 | 띄우기 · 내리기 · 다시 띄우기 금지 |

**끝 조건**(SPEC §9-3): ① T1 ~ T18 + 이 문서가 더한 T19 ~ T26 통과 · 지금 시험 전부 통과 · ruff ② E0 ~ E3 의 값이 보고에 있다(E1 ① 이 「안 받음」 이면 거기서 멈춤) ③ E4 — 사용자 확인(코디).

## 17. 검수 지적 반영 — WARN 8 · NOTE 7(`review-spec-004.md` §2)

| # | 반영(코디가 닫은 방향 — `_RESUME` §2 11-17 「SPEC-004 검수 뒤 코디」) | 이 문서 |
|---|---|---|
| **W-1** | 줄 번호는 걷기 안 1 부터 그대로 · 상담 material 이 걷기 **뒤** 대화 번호로 옮겨 적는다(충돌 표지도) · `build()` 시작 번호 인자는 안 넣는다 · T14 에 「gate 통과」 | §10 · §1(`walk/material.py` · `gate.py` 안 고침) |
| **W-2** | 요약 줄의 `gids[]` 는 「실은 gid」 가 아니다 · T15 에 「요약에 든 행을 뒤 턴이 읽으면 칸째」 | §10 |
| **W-3** | 턴 시작 줄을 먼저 쓴다 · 맺는 줄 없는 턴이 있으면 `broken` · 「실은 gid」 · `next_n` 은 성공 턴만 · 든 후보는 `error` 없는 턴만 | §9 · §14 · T20 · T21 |
| **W-4** | 장부에 프롬프트 sha 둘(대화 시작 · 이 턴) + `changed` · 프롬프트를 고치면 새 대화(README · E4) · Jev 지시도 같은 JSON 이라 한 sha · E1 ⑦ 이 help 글과 다르면 코디에게 | §3 · §5 · §15 · §16 |
| **W-5** | 고정 cwd = `TMPDIR` 과 무관한 사용자 캐시 폴더 아래 · E1 에 「다른 cwd 에서 resume」 | §7 · §5 |
| **W-6** | 턴은 구독자가 끊겨도 끝까지 · 이 판에 취소 없음 | §12 · T22 |
| **W-7** | T17 의 예외 = LLM 메시지 머리 · 꼬리 표식 · 「(없음)」 표지(사람에게 보일 문장이 아니다). 이 판에서는 그 셋이 **코드가 아니라 `prompts/consult.json`** 에 있다(§3) — 그래서 `consult/` 코드의 한글 문장은 주석 말고 0 이고, 예외는 가짜 턴 · 시험 자료에만 걸린다 | §3 · §15 grep |
| **W-8** | C-19 ~ C-22 로 한 줄씩(턴 한도 · `gold_hash` 바뀌면 대화 끝 · 메시지 한도 넘으면 실행 중단 · 답 중 실패 `broken`) — 코디가 사용자에게 통보 | §12 |
| N-1 | E1 ① 에 「정상 답이 `--max-turns 1` 한도 오류로 끝나지 않는가(result 줄 subtype)」. `--system-prompt-file` 확인은 §3 으로 필요 없어졌다 | §5 |
| N-2 | 조사의 줄 번호가 틀리고 SPEC 이 맞다 — 구현에 닿지 않는다 | — |
| N-3 | 밑그림의 홈 경로를 앱 레포(README · 주석)에 옮기지 않는다 | §2 |
| N-4 | 같은 고민의 응답은 gid 합집합으로 한 리스트 | §11 · T23 |
| N-5 | T12 「Jev 요청 수가 안 늘어난다」 는 후보가 한 묶음(32) 안일 때 | §14 |
| N-6 | E3 둘째 턴은 어긋남으로 표시(실패 아님) | §15 |
| N-7 | htmx 의 두 길 · SVG 통째 바꾸기는 E0 로 — DAY 가 (가) 꼴을 쓰고 있어 그 길부터 본다 | §4-1 · §6 |

## 18. 열린 것 · 이 문서를 쓰며 본 것(SPEC 은 고치지 않았다)

| # | 무엇 | 본 것 | 제안 |
|---|---|---|---|
| **B-1** | **18105 를 「읽기」 해도 되나** | 지시서는 「18210 · 18005 · 18105 · 18220 금지」 · SPEC E3 는 「허브 18105」. 이 문서는 금지를 「띄우기 · 내리기 · 다시 띄우기」 로 읽고 HTTP 읽기는 한다(WORK-009 §2 와 같은 읽기) | 다르면 발주서가 E3 용 허브 주소(`HUB_REST_URL`)를 준다 — 없으면 E3 는 코디가 돌린다 |
| **B-2** | **함께 쓰는 코드의 선택 인자가 둘이다** | W-1 로 줄 번호 인자가 빠져 `carry` 하나가 됐으나, 프롬프트가 JSON 으로 가면서 `front()` 가 안에서 읽던 Jev 지시를 밖에서 줄 인자(`instr`)가 든다 · `ask_front` 에 든 후보용 절 가지 하나 | 본문 그대로(둘 다 기본 = 지금 동작 · T13 이 잡는다). SPEC ST3 「선택 인자 둘뿐」 의 둘이 (`carry` · 줄 번호) → (`carry` · `instr`) 로 바뀐 것 — 되적기 후보 |
| **B-3** | **프롬프트 보관본** | 서버를 다시 띄워 되살린 대화(LG4)는 CLI 쪽 시스템 글이 스냅숏이지만(F7) 앱 쪽 Jev 지시 · 머리 · 표식은 지금 파일을 읽으면 판이 엇갈린다 | 대화 시작 때 JSON 을 `CHAT_DIR/prompts/<sha>.json` 으로 보관하고 그것으로 끝까지(본문). 보관을 안 하려면 「파일이 바뀌었으면 되살린 대화는 끝」 — 더 보수적이나 사용자 눈에 보이는 동작이 하나 는다 |
| **B-4** | **줄기 닫기 · 이벤트 이름 `error`** | SSE 확장의 `sse-close` 는 이벤트 이름 하나다 — `done` 과 `error` 둘 다에서 닫으려면 길이 필요하다. 또 이벤트 이름 `error` 는 브라우저 `EventSource` 의 연결 오류 이벤트와 이름이 같다 | E0-4 · E0-5 에서 본 뒤: 서버가 `done` \| `error` 뒤에 자료 없는 **`close`** 이벤트를 하나 더 보내고 `sse-close="close"` · 겹치면 오류 이벤트 이름을 `turn_error` 로. 둘 다 SPEC §4-3 의 이벤트 표를 건드린다 — **정하는 것은 코디**(되적기 후보) · 정해지기 전에는 E0 결과만 보고 |
| **B-5** | 설정 칸 둘이 SPEC §2-4 에 없다 | `CHAT_PROMPT_FILE` · `CHAT_FAKE_TURN` | 본문 그대로(시험 · E0 전용) · 되적기 후보 |
| **B-6** | 같은 요약 줄을 다시 싣지 않는 규칙 | W-2 로 요약의 gid 가 「실은 것」 이 아니게 되면, 같은 고민을 다시 물은 턴이 같은 요약을 또 싣는다 | (고민, 계열) · gid 집합이 같으면 그 줄 번호를 `seen_lines` 로(본문). SPEC 에 없는 한 줄 — 되적기 후보 |
| **B-7** | Tailwind 빌드를 가져오지 않는다 | DAY 는 `app.css` → `day.css` 를 node 도구로 빌드한다. 앱 레포는 node 가 없다 | `medikit.css`(빌드 없는 순수 CSS) + 손으로 쓴 `consult.css`(`--ms-*` 토큰만 참조)로 간다. 화면이 커져 유틸리티가 필요해지면 그때 빌드를 들인다 |
| **B-8** | 글꼴 파일 2 MB | 공개 라이선스(SIL OFL)라 둘 수 있으나 레포가 2 MB 는다 | 둔다(오프라인 · DAY 와 같은 꼴). 빼도 화면은 선다 — 코디가 고른다 |
| **B-9** | CSRF 를 걸지 않는다 | DAY 규칙은 POST 에 CSRF 다. 이 판은 로그인 · 세션이 없고 `127.0.0.1` 한 사람 | 이 판은 없음 · 배포 전(O-8 과 함께) 닫는다 |
| **B-10** | medikit 의 라이선스 글 | 공개 레포에 두는 것은 **닫혔다**(사용자 확인 11-17 — 디자이너가 전체 공개로 배포). 다만 본 폴더에 medikit 라이선스 파일이 없다 | 사실만 적은 `MEDIKIT-NOTICE.txt` 를 함께 둔다(§4-2). 배포자의 라이선스 글이 있으면 코디가 줄 때 바꾼다 |
| **B-11** | `ClaudeIngest` 가 init 줄의 세션 id 를 안 읽는다 | `cli.py:159-163` · 안 고치는 파일 | 상담 실행기가 줄 콜백을 한 겹 싸서 init 줄을 직접 본다(WP-3). E1 ⑥ 이 키 이름을 준다 |
| **B-12** | **SPEC 되적기 후보(한 줄)** | — | SPEC-004 0.1.1: CL2 `--system-prompt-file` → `--system-prompt` + §7-2 파일 둘 → `prompts/consult.json` 한 파일(§3) · ST3 의 선택 인자(B-2) · §4-3 의 닫는 이벤트(B-4) · §2-4 의 칸(B-5 · `CHAT_CLI_CWD` 기본 자리) · LG1 「턴에 줄 둘」(W-3) · AP 의 요약 줄 다시 안 싣기(B-6) · D-3 에 디자인 킷(§4) |

## 19. SPEC-004 절 ↔ WP 대응(미대응 0)

| SPEC-004 | 무엇 | WP |
|---|---|---|
| §1-2 D-1 ~ D-23 | 정해진 것 | 아래 절로 흩어짐 — D-18(플로우) · D-22(키)는 범위 밖 |
| §1-3 | 범위 밖 | 구현 없음(§2 「고치지 않는 것」) |
| §2-1 ST1 ~ ST5 | 구조 원칙 | WP-1(ST1 · ST4) · WP-9(ST2 · ST3 — B-2) · WP-2(ST5) |
| §2-2 | 모듈 자리 | WP-1 ~ WP-9(자리 그대로 · `consult/prompt.py` · `tail.py` · `probe.py` · `fake_turn.py` 넷이 더 있다) |
| §2-3 | 의존 | WP-1(+ §4 디자인 킷) |
| §2-4 | 설정 칸 | WP-2 |
| §3-1 F1 ~ F9 | 사실 | WP-0(F3 · F6 · F7 · F9 실측) |
| §3-2 CL1 ~ CL8 | 명령 꼴 | WP-3(CL1 ~ CL7 · CL2 는 §3 으로 바꿔 받음) · WP-0(CL8) |
| §3-3 CL9 ~ CL9-3 | cwd · 세션 파일 | WP-2(자리) · WP-3(띄움) · WP-10(README — CL9-2) · WP-4(CL9-3) |
| §3-4 CL10 ~ CL14 | 수명 · 실패 · 한도 | WP-3(CL10 ~ CL12) · WP-4(CL13 · CL14) · WP-7(화면 쪽) |
| §3-5 | 결과 꼴 | WP-3 |
| §3-6 SD1 ~ SD5 | SDK 경계 | WP-3(SD1 · SD2 · SD5) · WP-4(SD3 · SD4 — 장부에 user 메시지 · 꼬리째 답) |
| §4-1 | 라우트 | WP-1(페이지 · static) · WP-7(턴 · 줄기) · WP-8(`/face-check`) |
| §4-2 TF1 ~ TF6 | 단계 | WP-7 |
| §4-3 EV1 ~ EV5 | 이벤트 | WP-1(E0 — EV2 · EV3 · EV5) · WP-7(EV1 · EV4) |
| §4-4 | 근거 꼬리 | WP-5(`tail.py`) · WP-7 |
| §4-5 | 빈 자리 | WP-1 |
| §5-1 LG1 ~ LG5 | 장부 | WP-4 |
| §5-2 CR1 ~ CR7 | 이어 묻기 | WP-9 |
| §5-3 AP1 ~ AP8 | 재료 덧붙이기 | WP-5 |
| §6-1 PL1 ~ PL9 | 시술 리스트 | WP-6 |
| §6-2 SI1 ~ SI7 | 부위 → 점 · 라벨 | WP-8 |
| §6-3 HN1 ~ HN4 | 허브에 필요한 것 | **허브 몫(SPEC-001 0.7 · 별도 발주)** — 앱은 WP-8 의 계약 한 줄 |
| §7-1 ~ §7-3 PM1 ~ PM5 | 프롬프트 기반 | WP-2(§3 으로 바꿔 받음) |
| §8-1 ~ §8-4 FC1 ~ FC10 | 얼굴 SVG · 좌표표 | WP-8(눈 확인 = 코디 · 사용자) |
| §9-1 T1 ~ T18 | 단위 시험 | 아래 표 |
| §9-2 E0 ~ E4 | 실물 | E0 = WP-1 · E1 · E2 = WP-0 · E3 = WP-10 · E4 = 코디 · 사용자(§16) |
| §9-3 | 끝 조건 | §16 |
| §10 O-1 ~ O-11 | 열린 것 | O-3 · O-6 = WP-0 · O-11 = WP-10 · O-2 = 허브 0.7 · 나머지는 이 판 범위 밖(그대로 열림) |
| §11 U-11 ~ U-13 · C-10 ~ C-18 | 결정 · 기본값 | U-11 = WP-3 · WP-7 · U-12 = WP-9 · U-13 = WP-6 · C-18 의 순서는 §16 으로 바뀜 |
| 부록 B | 부위 60 분류 | WP-8 |

| 시험 | WP | | 시험 | WP |
|---|---|---|---|---|
| T1 · T2 · T3 · T4 · T5 | WP-3 | | T14 · T15 | WP-5 |
| T6 | WP-7 | | T16 | WP-4 |
| T7 | WP-5(꼬리) · WP-7(화면) | | T17 | WP-1 · WP-10(grep) |
| T8 | WP-1 | | T18 | WP-10(sha) |
| T9 | WP-6 | | **T19** 프롬프트 JSON 로더 | WP-2 |
| T10 · T11 | WP-8 | | **T20** 맺는 줄 없음 → `broken` · **T21** 오류 턴은 장부 셈 밖 | WP-4 |
| T12 · T13 | WP-9 | | **T22** 구독자 끊겨도 끝까지 | WP-7 |
| **T23** 같은 고민 두 조회 → 한 리스트 | WP-6 | | **T24** 조각 / 전체 · 인라인 0 | WP-1 |
| **T25** 부위 칸 없음 → 빈 조각 | WP-8 | | **T26** 꼬리 함수 동치 | WP-5 |

## 변경 기록

### 0.1.0 (2026-11-17) — 처음 씀

- SPEC-004 0.1.0 의 구현 계획: WP-0(CLI 실측) ~ WP-10 · 시험 T1 ~ T18 + T19 ~ T26 · 실물 E0 ~ E4 의 몫(워커 18223 · 코디 18222).
- SPEC 과 다르게 받는 곳 둘: 프롬프트 JSON(`prompts/consult.json` — §3) · DAY 디자인 킷(§4 — 가져올 파일 아홉 확정 · medikit 공개 레포 가능은 사용자 확인 11-17).
- 검수 W-1 ~ W-8 · N-1 ~ N-7 한 줄씩(§17) · 열린 것 B-1 ~ B-12(§18).
