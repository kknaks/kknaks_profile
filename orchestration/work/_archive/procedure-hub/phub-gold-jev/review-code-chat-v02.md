# [reviewer_code] 상담 채팅 수정 1 + 0.2(WORK-012) — 코드 검수

2026-11-17 · reviewer_code(read-only) · 워크트리 `clinic_chat/phub-gold-jev`(HEAD `6303e18` 위 미커밋 — 0.1 + 수정 1 + 0.2 · 공개 레포).
계약 = `app-chat-fix1-instructions.md`(수정 1) · SPEC-005 0.1.0 · WORK-012 0.1.0 · `review-spec-005.md` · `review-work-012.md` · 발주서 `impl-chat-v02-instructions.md` W-1 ~ W-8 · `_RESUME` §2 11-17 행(U5-1 (가) · U5-2 (a) · U5-3 (a) · U5-4 (a1) · U5-5 (a) · SPEC 검수 뒤 W-1 ~ W-9 · WORK B-1 ~ B-11).
구현 보고 = `app-chat-fix1-report.md` · `impl-chat-v02-report.md`.

## 판정: **PASS(WARN 2)** — FAIL 0 · WARN 2 · NOTE 8

계약 대조에서 코드가 SPEC · WORK · 코디 값과 어긋난 곳은 없다. WARN 2 는 ① SPEC 규칙(UP6)을 글자대로 따른 결과 우연 일치 추정이 두 번 나오면 거르개가 되는 구멍(SPEC 쪽) ② 사용자가 18222 에서 **옛 대화 탭을 이어 쓰면 0.2 가 안 보이는** 실물 자리(운영 안내)다.

## 0. 직접 돌린 것

| 무엇 | 결과 |
|---|---|
| `uv run ruff check .` | All checks passed |
| `uv run pytest -q`(1 회 · `CHAT_STATE` env 없이 = 끈 상태 기본) | **333 passed · 1 skipped**(14.9s) — 보고 값과 같다 |
| `git diff --stat HEAD -- tests/` | `tests/fake_cli/fake_cli.py` +21 하나뿐(0.1 그대로) |
| 0.1 · 수정 1 시험 파일 mtime | `test_consult_*` · `consult_fixture` ≤ 18:43(수정 1 끝) · `conftest` 11-16 · `test_state_*` · `state_fixture` 19:18 — **0.2 가 기존 시험을 건드리지 않음** |
| `_face.svg` · `face_coords.py` sha256 | `b3e4af94…` · `034130b7…` = 구현 보고의 WP-0 값 — 0.2 중 안 바뀜(검수 대상 아님) |
| 마크다운 XSS 직접 시험(`render.md`) | `<script>` · `<img onerror>` · 표 칸 안 HTML → 글자로 이스케이프 · `javascript:` · `JaVaScRiPt:` · `vbscript:` · `data:` 링크 → 링크 안 됨 · 그림 끔 · `Render.rejected` 의 손님 글도 이스케이프 |
| 공개 grep(커밋 후보 82 파일 — `uv.lock` · woff2 · 벤더 JS/CSS · 라이선스 빼고) | `/Users/` · `/home/` · 계정 이름 · 회사 도메인 · `sk-ant` · `sk-…` · `Bearer` · 메일 꼴 **0** · `https?://` 2(SVG xmlns · 시험의 `http://x/i.png` — 둘 다 무해) |
| `git status --porcelain --ignored` | 커밋 후보 = 고친 10 + 새(`consult/` · `llm/chat*.py` · `prompts/consult.json` · 시험) · gitignore = `.env` · `runs/` · `data/` · 캐시 |
| 18222(GET 만) | 아래 §8 |

실물 호출(Jev · CLI) · POST · 서버 띄우기/내리기 안 함. `.env` 열지 않음.

## 1. 수정 1 계약(사용자 e2e · 코드 검수 W-1)

| 항목 | 근거(파일:줄) | 판정 |
|---|---|---|
| 클로드 채팅 꼴 · 빈 첫 화면 문구 0 · 입력창 | `templates/partials/{main,turn}.html` · `static/consult.js`(인라인 스크립트 0 — 18222 전체 페이지 `<script` 4 개 전부 `src=`) | 맞음 |
| 서버 마크다운 · 안전 이스케이프 | `consult/render.py:17-21` — `MarkdownIt("commonmark", {"html": False, "linkify": False, "breaks": True}).enable("table").disable("image")` · Jinja `autoescape=True` · `|md` 는 `delta.html` · `answer.html` 두 곳만 · 그 밖 `|safe` 0 | 맞음 · XSS 없음(§0) |
| 근거 꼬리 화면 0 | `turn.py:91-101` `delta` = `progress.gate(TailFilter)` 를 지난 글 누적 · `turn.py:171-179` `done` = `split_tail` 뒤 `body` · 장부 `answer` = 꼬리 뗀 것 | 맞음 |
| 스피너 · 단계 줄 | `turn.html:8-9`(답 자리 첫 내용 = `cs-spin`) · `consult/steps.py` · `partials/steps.html` · 문구 = `prompts/consult.json` `steps` 네 키(앱 코드 한글 0 — T17/S5-T14) | 맞음 |
| `steps` 키 | `prompt.py` 선택 키 · 서버 시작 때 지금 파일에서 읽음(`server.py:58`) · LLM 에 안 감 | 맞음 |
| `GET /` → `303 /c/<새 id>` | `server.py:108-112` · 실측 `/ 303 → /c/cbd32990…` → 200 | 맞음 |

## 2. 0.2 상담 객체 대조

| 항목 | 근거(파일:줄) | 판정 |
|---|---|---|
| 값 = 데이터 코드만 · 재료 = 걷기 trace 뿐(UP1 · SL1) | `state.py:81-108` `observe` — `trace_front.targets[]` 의 `id`(표:코드) · `decision` · `noul` · `resolve_candidates` 의 조각만. 글에서 낱말 뽑기 0 · 칸 가르기 `SLOT_OF`(UP2 — adverse · condition · anatomy · offer · package 0) | 맞음 |
| 지어낸 값 0 · 선택지 = 허브 행 | BK2/BK2s = `plan.concern_options`(facets indication 행의 `concern_code`) · BK3 = cc 행 `concern_match`=「하위 고민」 · BK4 = 하위 고민들의 고민 부위 · BK5 = 객체 항목 자신(`blanks.py:35-68`) · NQ9 선택지 0 이면 안 줌(`:101`) · S5-T10 시험 | 맞음 |
| **guess 는 사이 값만 · named 0**(코디 W-1) | `state.py:70-78` — `target`→said · `uncertain_kept`→guess · `named` · `dropped` · `overlap` → 넣지 않음. 실물 E5-4 「이신경」 0.04 · 「입」 0.09 객체 0 | 맞음 — 다만 **WARN-1**(guess 반복 → confirmed) |
| UP3 · UP6 · UP8 · UP9 | `state.py:111-177` · `plan.py:206-235`(파생은 축 항목만 · 계열은 `procedures[]` 안 넣음 · 다시 셈) · diff `op` 닫힌 목록 | 맞음 |
| RV1 축 = said · confirmed | `state.axis_items` 하나 — `plan` · `synergy` · `blanks` · `_focus` 가 이것만 씀 | 맞음 |
| RV2 · RV3 거둠(함께 띄움 · 실패해도 턴 계속) | `turn.py:109` `asyncio.gather(walk, retract)` · `state.py:250-273`(resolve 한 번 + `ask_nouls` · 예외 → 거둠 0 · `retract_error`) · `update` 가 거둠 yes 를 넣지 않고 있으면 withdrawn(`:131` · `:150-157`) | 맞음 |
| UP4 · UP5 걸린 선택지 · W-8 | `carry.with_options`(바로 앞 턴 `asked` 만 · `origin: "option"` · 든 후보와 겹치면 표지만) · `front.py` CR6 가지(전부 no 면 입구 고르기로 감 — `test_w8_*`) · N-8 장부 `carried[]` 는 앞 턴 대상만(`turn.py:375-380`) | 맞음 |
| **NQ4 두 번 · NQ5 · 이름으로 답한 선택지(W-4)** | `blanks.py:96-100`(`asked_n < ask_max` · `ask_max` 기본 2) · NQ5 = 앞 턴 ask `answered is False` 면 새 항목 무관 `null`(코디 W-2) · `state.mark_answered`(`:207-224`) — 걸린 선택지 yes **또는** `observe` 가 이번 글 `target` 이 선택지면 `from_ask` 채움(`:101-102`) · BK1 은 subjects 새 항목 | 맞음 |
| **부위만 대상 = 고민 선택지 질문**(발주 W-1 (가)) | `plan.py:197-201` QY7 = `focus` 없고 짝 고민 없는 축 부위 → `facets(site, indication)` · `blanks.py:45-49` BK2s(`slot=concern` · `about`=부위) · `focus` 있으면 안 섬 · 실물 「이마가 신경 쓰여요」 선택지 16 · list 안 보냄 | 맞음 |
| **같은 이름 고민/부위 짝 거르개**(발주 W-2) | `state._pair_sites`(같은 `matched`+`start` 의 축 고민 코드 → `source.pair_concern`) · `state.filter_sites`(짝이 없거나 짝이 `focus` 일 때만) · QY7 은 짝 있는 부위 건너뜀 · 실물 ② 3 턴 QY1 site 없음 | 맞음 |
| **시너지 U5-2 (a)** — 둘 다 잡혔을 때 | `synergy.py:111-114` — `focus` 없으면 0 · 축 대상마다 · `shown.synergy` 에 없을 때만 읽음 | 맞음 |
| **U5-3 (a)** 리스트 칸 묶음 · 안/밖 | `synergy.inside`(코드로 — 계열 · 시술 · 케이스/제품은 `scope` reach) · LLM 줄은 안 상대 · 첫 읽기 턴만(SY9) · 밖 상대는 `list_synergy.html` 이름만 · 표지 `data-synergy` | 맞음 |
| **U5-4 (a1) 표지만 · 안전 본문 먼저 0** | QY4b = `pair(classes=[회피, 간격, 순서])`(`synergy.py:28` · `:123`) → `caution()` 은 `question_class` · `same_day` 두 값만 보고 `caution` 불과 근거 gid 만 남김. QY4b 행은 `add_summaries` 에 안 감(재료 줄 = 보완 상대의 `same_day` · `goal_effects` · `same_day_caution` 불) · `shown.info` 는 `tm.new_lines` 의 걷기 줄만 · 화면은 `data-caution` · 빈 자리 `mark-caution` 뿐 · 프롬프트 `synergy` 절 「물으면 알려 준다 까지만」 · S5-T21 | 맞음 |
| **U5-5 (a)** pair 보완만 · 패키지 0 | `synergy.py` 에 `package` 조회 0 · `plan.ALLOWED` 닫힌 목록(QY6) | 맞음 |
| 안전 종류 재료 0 · NQ6 | `plan.ALLOWED` = cc · scope · facets(indication) · pair 뿐 · `assert allowed` · `blanks.pick` 이 걷기 kinds 에 adverse · contraindication · avoid 가 있으면 `null` | 맞음 |
| **wishes 조회 0**(W-9) | `plan.run` · `synergy.run` 이 `wishes` 를 읽지 않음 · 바람은 `consult_view` 요약으로만 · `test_w9_*` | 맞음 |
| W-6 세 종료 상태 = 갱신만 · list 0 | `turn.py:263-268`(terminal 이면 `derive` 만) · `:141`(`NO_B_ON` 이면 screen 안 함) · 다음 턴 따라잡음(S5-T18) | 맞음 |
| RV9 · 성공 턴만 객체 | `turn.py:389`(`after` = err 없을 때만) · `ledger.py:173-175` | 맞음 |
| 「앱 판정」 · 「상담 상태」 코드 0 | `material.consult_view`(이름 · 상태 · focus 불만) · `ask_view`(이름 · 층 · 줄 번호) | 맞음 |

## 3. `CHAT_STATE` · 끈 상태 = 0.1

| 항목 | 근거 | 판정 |
|---|---|---|
| 코드 기본 `off` | `config.py` `chat_state: Literal["on","off"] = "off"` | 맞음 |
| 켜는 값은 프로세스 env | `.env.example` 에 `CHAT_STATE` 줄 **없음**(주석으로 「이 파일에 두지 말고 프로세스 env 로만」) · README 같음. 코드가 `.env` 의 값을 막지는 않는다(NOTE-3) | 맞음 |
| 끈 상태 = 0.1 | `turn.py:104-107` · `:128-129` · `:149-160` 0.1 줄 그대로 · 시스템 글 = `system` 다섯 절(0.1 sha 대조 — `test_s5_t15_off_state_is_0_1`) · 장부 칸 0.1 + 시작 줄 `consult_state` 하나 · `list` 에 `modality_code` 없음 · Jev 후보에 `option_from` 0 · 기존 시험 214 + 0.1/수정 1 시험이 env 없이 통과 | 맞음 |
| **0.1 대화 되읽기 = 끈 상태** | `ledger.py:117-119`(시작 줄에 칸 없으면 `off`) · `state_at_start` · 서버 값이 바뀌어도 첫 턴 값으로 끝까지(`test_on_state_system_text_and_conv_keeps_state`). **실물에서 확인**: 재시작 전 대화 `e3f90bfd…` 의 6 턴(19:25 「써마지 받고 싶어요」)이 `consult_state: "off"` 로 돌아 ask · 시너지 없음 → WARN-2 | 맞음(계약대로) |
| 켠 대화 시작 조건 | `server.py:128-134` — 켠 대화인데 0.2 키 없으면 `rejected("prompt")` | 맞음 |

## 4. 함께 쓰는 코드(front · jev_requests) — 줄 수 · 무변경

| 파일 | HEAD 대비(0.1 + 0.2) | 0.1 때(보고) | 0.2 증분 | 판정 |
|---|---|---|---|---|
| `walk/front.py` | +43 / −4 | +39 | 약 +4 ~ +8(`_from_key` 5 줄 · `origin` 칸 · `option_from` 키 · `out.carried[].origin`) | `origin` 이 없으면 글자 그대로(`_from_key` → `carried_from` · `origin` 칸 안 붙음) — S5-T20 · 걷기 시험 통과 |
| `walk/jev_requests.py` | +11 / −1 | +8 | +3(`target_option` 가지) | 지시에 `target_option` 이 없거나 항목에 `option_from` 이 없으면 0.1 길 |
| `columns/col_b.py` · `walk/calls.py` | 0.1 그대로(인자 넘기기 · 주석) | — | 0 | — |

인자 수는 0.1 의 선택 인자 둘(`carry` · `instr`) 그대로 — ST3 지킴. WORK 의 「약 3 줄」 보다 front 가 조금 많은 것은 보고 §1 에 적혀 있다(NOTE-2).

## 5. 조회 열쇠 = 걷기 Call · skipped

- `plan.qy1_calls`(`plan.py:87-95`) = 걷기 `calls._value_calls`(`calls.py:254-265`)의 `Call("concern_candidates", {"concern_code": …[, "site": <부위 이름 글자>]})` 와 같은 `request` → `Call.key()`(= 도구 + `request` JSON) 같음. `Reader.get`(`plan.py:57-84`)이 걷기의 이번 턴 `reads` 에 같은 키가 있으면 부르지 않고 `skipped: "walk"`(profile 이어 조회도 함께 넘김). `test_w7_query_key_equals_walk_call_key`.
- 실물(18222 새 대화 `7c356e51…` 1 턴): `queries` = QY2 5(skipped null) · QY3 27(null) — 걷기가 안 읽은 것만 불렀다. 보고 E5 14 턴 합 skipped 13.

## 6. 시험 · ruff

§0 그대로 — ruff 통과 · pytest 333 passed · 1 skipped(env 없이). 새 시험 7 파일 43 개가 S5-T1 ~ T21 · 발주 W-1 ~ W-8 꼴을 하나씩 짚는다(목록은 보고 §1 · `tests/test_state_*.py`).

## 7. 지적

| # | 심각도 | 파일:줄 | 근거 | 내용 | 고칠 방향 |
|---|---|---|---|---|---|
| W-1 | **WARN**(SPEC 구멍) | `consult/state.py:118-122` `_again` | SPEC-005 UP6 · RV1 · E5-4 | UP6 「guess → 다시 나옴 = confirmed」 를 글자대로 따라, **사이 값(`uncertain_kept`) 그대로 두 번 걸린 우연 일치도 `confirmed`(축)이 된다.** 직접 확인: 「볼」 0.33 을 두 턴 넣으면 `filter_sites` 에 `SITE-051` 이 들어 QY5 거르개가 된다(예: 「리쥬란 맞아 볼까」 → 「필러도 해 볼까요」). RV1 · E5-4 가 막으려던 「우연 일치가 리스트를 좁힘」 이 다시 열린다. 시험 S5-T2 는 SPEC 대로 이 꼴을 기대한다 | 코디 결정: 다시 나온 관찰이 `said`(target) · 걸린 선택지 yes · BK5 답일 때만 `confirmed` · guess 로 다시 나오면 `history` 만 더함. SPEC-005 0.1.1 되적기(UP6 한 구절) + S5-T2 기대 고침 |
| W-2 | **WARN**(사용자가 만날 자리) | `ledger.py:117-119` · `server.py:108-128` | B-2 · W-3 | 18222 는 19:23 에 `CHAT_STATE=on` 으로 다시 떴다(프로세스 env 확인). 그러나 **재시작 전에 연 대화 주소(`/c/<옛 id>`)를 새로 고침해 이어 쓰면 끈 상태로 끝까지 돈다** — 실물 `e3f90bfd…` 6 턴(19:25)이 그 꼴로 ask · 시너지 · 관심 묶음 없이 0.1 답을 냈다. 계약대로지만 사용자는 「0.2 가 안 된다」 로 본다 | 코디가 사용자에게 「E5-5 는 `http://127.0.0.1:18222/` 로 새 대화를 열어서」 한 줄. 코드 변경 불필요(원하면 끈 대화 화면에 빈 자리 표지 하나 — 문구는 사용자) |
| N-1 | NOTE | `plan.py:233-234` | SPEC §2-4 · WORK WP-1 | `concern_sites[]` 항목의 `state` 가 `"derived"` — `STATES` 닫힌 목록 밖이고 SPEC 은 「파생은 근거 항목의 state 를 따른다」(`procedures[]` 는 그렇게 함) | `focus` 고민의 `state` 를 싣기(장부 꼴만) |
| N-2 | NOTE | `walk/front.py` · `jev_requests.py` | WORK §8 「약 3 줄」 | 0.2 증분 front 약 +4~8 · jev_requests +3 — 보고에 적힘 · 동작은 `origin` 있을 때만 | 받아들임 |
| N-3 | NOTE | `config.py:23` | 발주 W-3 | pydantic 이 `.env` 를 읽으므로 누가 `.env` 에 `CHAT_STATE=on` 을 두면 켜진다 — 막는 장치는 문서뿐 | 받아들임(또는 `chat_state` 만 `.env` 무시 — 과함) |
| N-4 | NOTE | `prompts/consult.json` `version` | WORK §9a | `0.1.0-draft` 그대로(기존 시험이 박아 둠 — 보고 §6-1) | 코디가 시험 한 줄 고친 뒤 `0.2.0-draft` |
| N-5 | NOTE | `render.py:17` | 수정 1 ② | `http(s)` 마크다운 링크는 그대로 링크가 된다(`rel` · `target` 없음). 스크립트 주소는 막힘. LLM 이 바깥 주소를 낼 일은 드묾 | 배포 전 `rel="noopener noreferrer"` 렌더 규칙 또는 링크 끔 |
| N-6 | NOTE | `server.py:108-112` | 수정 1 W-1 | `GET /` 마다 메모리에 빈 `Conv` 하나(디스크 0) — 한 사람 로컬에선 무해 | 배포 전 |
| N-7 | NOTE | `turn.py:251-288` | B-5 | `after_walk` 의 `try` 밖(`cst.update` · `blanks`)에서 예외가 나면 턴 전체가 `turn_error internal`(서버 `drive` 가 받음) — 객체 조회는 감쌌고 갱신은 순수 함수라 실제 위험 낮음 | 받아들임 |
| N-8 | NOTE | `turn.py:272` · `:276` | 효율 | 켠 상태에서 `build_list(..., codes=True)` 를 한 턴에 두 번(시너지 안/밖 판정 · `state_list`) | 받아들임 |

## 8. 「사용자가 실물에서 만날 자리」(18222 GET 만)

| 무엇 | 본 것 |
|---|---|
| 서버 상태 | 18222 PID 84242 · 시작 19:23:29 · 프로세스 env `CHAT_STATE=on` · 코드 마지막 수정(19:11) 뒤에 떴음 → 0.2 반영됨 |
| `/` | `303 → /c/<새 id>` · 대화 페이지 200(50.8 KB) · `HX-Request` 면 `<main id="consult">` 조각 · `/static/consult.{css,js}` 200 · `/face-check` 200 · 없는 줄기 204 |
| 새 대화 실물 한 턴(코디가 친 `7c356e51…` 「써마지 받고 싶어요」 — 장부 읽기만) | 시작 줄 `consult_state: "on"` · `list` = `{interest 1, concerns 0, synergy 0}`(묶음 ① 만) · `ask` = BK2 `concern` 선택지 21 · 답 끝에 질문 하나(「어떤 고민 때문에 … 피부 탄력 저하나 모공, 볼처짐 같은 쪽인가요?」 — 선택지 안의 이름 · 층을 밝힘) · first_list 490ms · ttft 1.8s · total 4.4s |
| **옛 대화 탭** | WARN-2 — 재시작 전 대화를 이어 쓰면 끈 상태(0.1). E5-5 는 `/` 로 새 대화부터 |
| 헷갈릴 수 있는 것 | ① 단계 문구 넷은 「…하고 있어요」 꼴이라 체크된 뒤에도 같은 글(수정 1 보고 §3 — 사용자 확인 거리) ② 관심 묶음 · 시너지 묶음 · 표지 머리 글은 전부 빈 자리(`data-slot` — 문구 사용자 몫)라 화면에서 **제목 없는 묶음**으로 보인다 ③ 시너지는 고민이 잡힌 뒤에만 뜬다(U5-2 (a)) — 「써마지」 한마디엔 안 뜨는 것이 정상 ④ 「같은 날 제약」 은 표지 자리만 있고 글이 없다(U5-4 (a1)) |

## 9. 남은 것

- WARN-1: 코디 결정(UP6 한 구절) — 고치면 `state._again` 한 곳 + S5-T2.
- WARN-2: 코디가 사용자 안내 한 줄(새 대화로 E5-5).
- NOTE-4: `consult.json` version 올림(시험 한 줄).
