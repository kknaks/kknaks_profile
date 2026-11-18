# [reviewer_code] WORK-011 상담 채팅 1판 — 코드 검수

2026-11-17 · reviewer_code(read-only) · 워크트리 `clinic_chat/phub-gold-jev`(HEAD `6303e18` 위 미커밋 · 공개 레포).
계약 = SPEC-004 0.1.0 + WORK-011 0.1.0 + `_RESUME` §2 11-17 행(프롬프트 JSON · DAY 킷 · U-11~13 (a) · W-1~W-8 · WORK B 답) + 발주서 W-1~W-5.

## 판정: **PASS** — FAIL 0 · WARN 1 · NOTE 9

계약 대조에서 어긋난 곳은 없다. WARN 1 은 계약 위반이 아니라 「실물에서 사용자가 만날 자리」(새로 고침하면 대화가 사라진다)다.

## 0. 직접 돌린 것

| 무엇 | 결과 |
|---|---|
| `uv run ruff check .` | All checks passed |
| `uv run pytest -q`(1 회) | **282 passed · 1 skipped**(11.3s) — 보고 값과 같다 |
| 기존 시험만(`tests/test_*.py` 24 개 · `test_consult_*` 뺌) | **214 passed · 1 skipped** — 기준선 그대로 |
| `git diff --stat HEAD -- tests/` | `tests/fake_cli/fake_cli.py` +21 · 0 삭제 하나뿐(W-4) |
| pytest 앞뒤 `git status --porcelain --ignored` | 같음 — 시험이 레포 안에 파일을 만들지 않는다 |
| 벤더링 8 파일 sha256 ↔ DAY 원본 | 8/8 같음(htmx 2.0.4 · SSE 확장 · Pretendard · 라이선스 셋 · medikit.css · .js) |
| 좌표표 ↔ SPEC 부록 B(꼴별 코드 집합) | 60 · 17/27/8/4/4 · 점 71 · 꼴별 코드 집합 차이 0 · `pair` 는 모두 x 가 0.5 양쪽 |
| 18222(GET 만) | `/` 200 · `/face-check` 200 · `/static/*` 200 · `/c/<없는 id>` 200(빈 대화) · `/c/<없는 id>/turns/1/events` 204 · `HX-Request` 면 `<main>` 조각만 |

실물 호출(Jev · CLI) · POST · 서버 띄우기/내리기는 하지 않았다. `.env` 열지 않음.

## 1. WP-0 ~ 10 · SPEC-004 계약 대조

| 항목 | 근거(파일:줄) | 판정 |
|---|---|---|
| CLI 명령 꼴 CL2 · CL3 · CL4 | `llm/chat_cli.py:49-57` `chat_args` — 첫 턴 `--session-id` · 다음 턴 `--resume`(머리 둘만 다름) · `--max-turns 1` · `--system-prompt <JSON 이어 붙인 글>`(WORK §3 대로) · 격리 인자 `cli.py` 꼴 · `--no-session-persistence` · `--continue` · `--mcp-config` · `--max-budget-usd` · `--bare` · `--json-schema` 없음. 시험 T1 · T2 가 인자를 낱낱이 센다 | 맞음 |
| CL7 init 줄 대조 | `chat_cli.py:90-113` `InitWatch` — 키 `session_id`(E1 ⑥ 실측 값) · 다르면 `StopRun` → `session_mismatch` | 맞음 |
| 세션 new / open / broken(CL10 ①②③) | `chat_cli.py:193-204` `_move` — 성공 → open · new 실패 → **새 UUID**(state new) · open 에서 띄운 뒤 실패 → broken · 띄우기 전 실패(auth · spawn) → open 그대로 · busy/broken 은 안 건드림 | 맞음 |
| 고정 cwd(CL9 · W-5) | `config.py:131-142` — `XDG_CACHE_HOME` → macOS `~/Library/Caches` → `~/.cache` 아래 `clinic-chat/consult-cli` · `TMPDIR` 무관 · 레포 밖 · 지우지 않음 | 맞음 |
| 장부 시작 줄 / 맺는 줄(W-3 ①) | `consult/ledger.py:125-140` — 띄우기 전 `phase: start` · 끝에 `phase: end` · 되읽기에서 맺는 줄 없는 턴 → `broken`(`:119-121`) | 맞음 |
| 「실은 gid」 · `next_n` · 요약 키 = 성공 턴만(W-3 ②) | `ledger.py:143-166` `error is None` 일 때만 · `turn.py` 는 오류 턴 material 에 `not_counted` 표지 | 맞음 |
| 든 후보 = 오류 없는 턴만(W-3 ③) | `consult/carry.py:20-31` — `error` · 범위 밖 · 입구 없음 · 실행 중단 건너뜀 | 맞음 |
| 이벤트 순서 `list` → `sites` → 첫 `delta` → `done` | `consult/turn.py:98-121` — 걷기 · 재료 · **크기 판정(FT5) 뒤** list · sites 를 보내고 그다음 LLM. 범위 밖 · 입구 없음 · 실행 중단이면 둘 다 안 보냄(`NO_B_ON`) | 맞음 |
| `turn_error` · `close` data 줄 · 빈 `sites` 요소 | `consult/live.py:13-31` — `close` 자료 `close` · 빈 자료 push 는 ValueError(W-3 ⑤) · `partials/sites.html` 은 부위 0 이어도 `<div id="face-marks">` 통째 | 맞음 |
| 근거 꼬리 | `consult/tail.py` — 표식 인자 말고 `col_b` 와 같음(T26 이 대조) · `delta` 는 `progress.gate(TailFilter)` · `done` · 다시 그리기는 꼬리 뗀 `answer` | 맞음(화면 0) |
| 재료 덧붙이기(W-1 · W-2 · B-6 · AP8) | `consult/material.py:126-201` — 걷기 번호 1 부터 그대로 · 걷기 뒤 대화 번호로 옮김 · 충돌 표지도 옮김 · 요약 `gids` 는 「실은 gid」 아님 · 같은 요약은 `seen_lines` · 크기 넘으면 FT5 | 맞음 |
| 리스트(PL1 ~ PL9 · N-4 · U-13 (a)) | `consult/listing.py` — `concern_candidates`·`read` 만 · 시술 행 · 계열 묶음(빈 이름 그대로) · reach/concern_match 합집합 · 허브 순서 · gid 합집합 · `modality_only` · `unreached` 따로 둘 | 맞음 |
| 부위(SI1 ~ SI7 · HN 없을 때) | `consult/sites.py` — 칸 이름 상수 하나(`SITES_FIELD` 임시) · 칸 없으면 점 0 · 라벨 0(오류 0) · 다른 길로 메우지 않음 | 맞음 |
| CL13 · CL14 · C-19 ~ C-22 | `ledger.blocked` · `turn.py:95-96`(gold_hash 바뀜 → `build_changed` · 대화 끝) | 맞음 |

## 2. 함께 쓰는 코드(4 파일 · 약 50 줄)

| 파일 | 바뀐 것 | 판정 |
|---|---|---|
| `columns/col_b.py:161-169` | `walk(..., carry=None, instr=None)` 를 `front()` 에 넘기기만 | 기본값 = 지금 동작 |
| `walk/front.py:197-356` | `carry` · `instr` 선택 인자 · 든 후보를 `concepts` 와 **따로**(겹침 묶음 `by_span` · EN1 상품 이름 덮임 · `pick_entries` 재료에 안 듦 — W-1) · resolve 후보 **뒤에** 붙여 같은 요청(coverage 도 함께) · yes 만 `carried` · 사이/no → `dropped` · CR6 가지 · `FrontResult.carried` | W-1 범위 안. 「가지 하나」 보다 줄이 많은 것은 구현 보고 §5 에 이미 보고됨 |
| `walk/jev_requests.py:64-85` | `_target_instr` — `carried_from` 이 있고 `target_carried` 절이 있을 때만 그 절 · 아니면 `target` | 기본값 = 지금 동작 |
| `walk/calls.py:59` | **주석 한 줄**(`Entry.by` 값 목록에 `carried` 를 적음) — 동작 변경 0. WORK §14 가 「`Entry.by` 값 `carried`」 자리로 이 줄을 allowed_paths 에 둔 것이고 실제 값은 `front.py` 가 넣는다 | 문서 변경뿐 |

- `carry=None` 이면 `c_noul` 이 빈 목록 · `t_noul` 그대로 · `carried_entries` 빈 목록 — 기존 길과 글자 그대로 같다. 기존 시험 214 통과로 확인(T13).
- `walk/gate.py` `EXPLICIT` 에 `carried` 가 없다 → G7 이 든 대상에 안 걸림. 발주서 W-1 「받아들임(gate 동결)」 그대로.
- 동결 파일(`web/` · `prompts/*.md` · `jev/*.md` · `walk/material.py` · `gate.py` · `llm/cli.py` · `cli_process.py` · `auth.py`)은 `git diff` 에 없다(T18).

## 3. 프롬프트 JSON

- `prompts/consult.json` `0.1.0-draft` · 절 `role → rules → screen → material → tail` · `jev_front{target, target_carried, kind, gap}` · `turn_headers` 넷 · `tail_marker` `<<<근거>>>`. 로더(`consult/prompt.py`)가 키 · 절 순서 · 빈 값 · 표식이 글 안에 있는지를 검사하고, 틀리면 앱 시작이 실패한다(`server.py:58`).
- **보관본**: 대화를 시작할 때 `CHAT_DIR/prompts/<sha256>.json`(있으면 안 씀) · 되살린 대화는 보관본으로 돈다(`server.py:77-85`). 실물 18222 의 보관본 이름 `66c112c5…aa726` = 지금 파일의 sha256.
- **sha 둘**: 시작 줄 `prompts.consult_at_start` · 맺는 줄 `prompts{version, consult_at_start, consult_now, changed}`(`turn.py:154-155`). 표지만 하고 그 대화의 글은 바꾸지 않는다(W-4).
- `system` 에 시각 · id 자리가 없다(PM2 시험) · `jev_front` 셋은 `front.md` 와 글자 그대로(시험이 대조).

## 4. 화면 — DAY 규칙 · 문구 · 꼬리

| 규칙 | 본 것 |
|---|---|
| HX-Request 조각 | `GET /` · `/c/{id}` — 헤더 있으면 `partials/main.html` · 없으면 `page.html`(실물 GET 으로 확인) |
| JS 한 파일 · 인라인 0 | 앱 JS = `static/consult.js` 하나(이벤트 위임 + `data-cs-*`) · `<script>` 는 `src` 만 · 템플릿에 `style=` · `on*=` 0 · htmx-config `allowEval:false` · `allowScriptTags:false` |
| htmx 벤더링 + 라이선스 | htmx 2.0.4 · SSE 2.2.4 · 라이선스 파일 · README 에 판 · sha256 표 |
| medikit 토큰만 | `consult.css` 에 색 리터럴(#hex · rgb) 0 — 색은 `var(--ms-*)` · 치수만 `:root` 의 `--cs-*` |
| `@font-face` | `consult.css:4-9`(같은 폴더 상대 주소 — W-5) |
| 문구 지어 넣은 것 0 | 템플릿 · `consult/*.py` 의 한글은 주석 · 독스트링 · `e3.py` 실측 질문 셋(W-7 예외로 시험에 명시)뿐. 자리는 전부 `data-slot` 빈 요소 |
| 근거 꼬리 화면 0 | `delta`(TailFilter) · `done`(split_tail 본문) · `GET /c/{id}` 다시 그리기(장부 `answer` = 꼬리 뗀 본문) 셋 다 |

## 5. 얼굴 SVG · 좌표표

- `_face.svg` = 손으로 쓴 path 18 줄(밑그림 경로 · PNG · 뽑은 윤곽 0) · `viewBox 0 0 590 1060`.
- `#face-marks` 는 선 그림 SVG 안 `<g>` 가 아니라 **div(점 svg + 라벨)** 로 통째 바꾼다 — EV3 · WORK E0-2 가 허락한 대안이고 보고 §6-1 에 적혔다.
- 분류 · 짝 두 점 · 표 밖 코드(몸 부위) → 라벨 `why: off_face` · `area/line/none` → 라벨 · 같은 부위 한 번 — `place()` 를 직접 돌려 확인. 허브 부위 칸이 없으면 점 0 · 라벨 0(실물 E3 · T25).

## 6. 커밋 후보 grep(커밋될 64 파일 — woff2 뺌)

| 무엇 | 결과 |
|---|---|
| 홈 절대 경로 · 사용자 이름(`/Users/` · `/home/` · 계정 이름 · 회사 도메인) | 0 |
| 키 꼴(`sk-ant` · `sk-…` · `api_key=` · private key · password/token 값) | 0 |
| URL | `127.0.0.1` 기본값(앞 판과 같은 것) · 라이선스 출처 둘 · `uv.lock` 의 PyPI 뿐 — 내부 주소 0 |
| `~/` 경로 | `config.py:132` 독스트링 하나(일반 경로 꼴 — 사용자 특정 아님) |
| PNG · jpg · jsonl · 세션 파일 · 장부 · 실측 기록 | 0 — 전부 `runs/consult/`(gitignore) · CLI 세션 파일은 레포 밖 캐시 폴더 |
| 실물 장부(`runs/consult/turns.jsonl`)에 홈 경로 | 없음(`_scrub_home` 확인) |

## 7. 지적

| # | 심각도 | 파일:줄 | 근거 | 무엇 · 고칠 방향 |
|---|---|---|---|---|
| W-1 | WARN | `consult/server.py:108-111` · `partials/main.html` | SPEC §4-1 · LG4 | `GET /` 가 새 `conv_id` 를 만들지만 **브라우저 주소가 `/` 그대로**다(`hx-push-url` · 리다이렉트 없음 · 화면에 대화 링크 없음). 새로 고침 = 새 빈 대화이고, 앞 대화로 돌아갈 길(`/c/<id>`)을 사용자가 알 수 없다 → LG4(서버를 다시 띄운 뒤 되읽기)가 화면에서 닿지 않는다. 방향: `GET /` → `303 /c/<새 id>` 또는 첫 응답에 `HX-Push-Url`/폼 응답에 push-url. SPEC 표를 건드리므로 코디가 정한다 |
| N-1 | NOTE | `server.py:139-145` · `partials/turn.html` | §4-1 끝 줄 | 서버를 턴 도중 다시 띄우면 그 턴 줄기가 204 → 말풍선이 **빈 채로 멈춘다**(오류 표시 없음). `/c/<id>` 로 다시 열어야 `broken` 오류가 보인다 — W-1 과 겹친다 |
| N-2 | NOTE | `partials/main.html` · `error.html` | D-17 | 빈 자리 그대로라 실물에서 **글 없는 보내기 단추 · 글 없는 「새 대화」 링크(보이지 않음) · 단계 표시 없음**이다. 계약대로이고 E4 의 빈 자리 목록으로 채울 것 |
| N-3 | NOTE | `consult/render.py:30-31` | — | 받지 않은 턴 조각이 `n="x"` 라 `id="answer-x"` 가 여러 번 생길 수 있다(중복 id). 지금 동작에 닿는 곳은 없다 |
| N-4 | NOTE | `server.py:71-75` · `:108-111` | — | `GET /` · `GET /c/<아무 id>` 마다 메모리에 대화가 하나씩 남는다(지우지 않음). 로컬 한 사람이라 문제는 작다 |
| N-5 | NOTE | `server.py:77-85` | B-3 | 보관본(`runs/consult/prompts/<sha>.json`)을 지우면 그 대화는 매 POST 마다 `prompt` 로 거절된다(새 대화만 됨). README 에 「`runs/consult/prompts` 를 지우지 말 것」 한 줄이면 충분 |
| N-6 | NOTE | `consult/turn.py:127-132` | §4-2 끝 줄 | 걷기 오류(실행 중단)인데 LLM 이 답한 턴은 화면에 `done`(정상 말풍선) · 장부는 `error` 있음(재료 · 든 후보에 안 셈)이다 — SPEC 대로이나 화면에서 둘이 구분되지 않는다(`data-end-state` 만 다름) |
| N-7 | NOTE | `consult/material.py:52-63` | AP4 | 앞 턴에 칸째 실은 gid 가 이번 턴 `concern_candidates` 에서만 다시 나오면 요약 줄 `gids` 에 다시 든다(되짚기용이라 해는 없다 · 시술 이름 줄은 여전히 0) |
| N-8 | NOTE | `walk/front.py:263-276` | W-1 | 든 후보의 trace 행(`targets_tr`)이 이번 글 후보보다 **앞에** 쌓인다 — carry 가 있을 때만이고 T13 과 무관. trace 를 읽는 사람이 순서에 기대지 않으면 그만 |
| N-9 | NOTE | 구현 보고 §4 | CL13 · AP8 | E3 3턴 입력 캐시 합 12 만 토큰대 — 턴 한도 20 · AP8 은 턴 단위라 대화 누적을 막지 않는다(보고에 이미 있음 · 0.2 재료) |

## 8. 사용자가 실물(18222)에서 만날 자리

1. **빈 화면**: 제목 · 입력 안내 · 보내기 단추 글이 전부 비어 있다(N-2). 단추는 모양만 있고 글이 없다. 리스트 · 얼굴 칸도 처음엔 빈 자리(`list-empty` · `face-empty`).
2. **점이 안 뜬다**: 허브 0.7 부위 칸 전이라 고민을 물어도 점 0 · 라벨 0 이 정상이다(오류 아님). `/face-check` 에서만 점 71 개 + 코드가 보인다 — 좌표 눈 확인은 여기서.
3. **새로 고침 = 새 대화**(W-1): 주소가 `/` 그대로라 F5 하면 앞 대화가 화면에서 사라진다. 앞 대화는 장부에 남지만 `/c/<conv_id>` 를 알아야 연다(`<main data-conv-id>` 속성에만 있다).
4. **오류 턴**: 오류 말풍선은 `data-error="<종류>"` 빈 요소라 **글 없이 빈 말풍선**으로 보인다. `broken` · `build_changed` · `turn_limit` 이면 새 대화 링크가 붙지만 글이 비어 보이지 않는다 — 사용자는 주소창에서 `/` 로 가야 한다.
5. **이어 묻기**: 「그중 필러」 는 앞 리스트로 좁히지 않고 필러 계열 전체로 답한다(U-12 (a) · E3 2턴 425 줄) — 알고 가는 어긋남. 둘째 턴부터 리스트 · 점은 바뀌지 않는다(PL8 — 그 턴에 `concern_candidates` 를 안 읽으면 앞 것 그대로).
6. **서버를 다시 띄울 때**: 열어 둔 탭에서 다음 질문을 보내면 장부를 되읽어 같은 세션으로 잇는다(정상). 단 턴이 도는 중에 내리면 그 대화는 `broken` 이 되고 그 말풍선은 빈 채로 멈춘다(N-1). 18105 를 다시 띄워 `gold_hash` 가 바뀌면 열린 대화는 다음 턴에서 끝난다(C-20).
7. **프롬프트를 고쳤을 때**: 열린 대화는 시작 때 보관본으로 계속 돈다 — 고친 글을 보려면 새 대화(README 에 있음).
8. CLI 세션 파일(대화 평문)은 사용자 홈의 Claude CLI 폴더에 쌓이고 앱이 지우지 않는다(README 에 있음).

## 9. 남은 것

- W-1 처리 여부(코디) · E4 사용자 확인 · `/face-check` 좌표 눈 확인 · 빈 자리 문구 · 프롬프트 초안 확인(C-1) · 허브 0.7 부위 칸(`sites.SITES_FIELD` 한 줄).
- SPEC-004 0.1.1 되적기 후보(구현 보고 §6 · WORK B-2 · B-4 · B-5 · B-6): 선택 인자 둘 = (carry · instr) · `turn_error` / `close` · 설정 칸 둘 · 요약 줄 다시 안 싣기 · `#face-marks` = div · 맺는 줄 추가 칸(`session_next` · `conv_end` · `llm.answered`) · 204 줄기.
