# [app] 상담 채팅 1판 구현 보고 — WORK-011 WP-0 ~ WP-10 (SPEC-004 0.1.0)

2026-11-17 · app 워커 · 워크트리 `clinic_chat/phub-gold-jev`(HEAD 6303e18 위 · **커밋 안 함**).

## 0. 요약

- WP-0 ~ WP-10 워커 몫 전부 끝. `uv run ruff check .` 통과 · `uv run pytest -q` **282 passed · 1 skipped**(기준선 214 passed · 1 skipped + 새 시험 68) · 실물 E1 · E2 · E3 · E0(headless Chrome) · 실제 서버 한 턴.
- 포트: 워커 18223 만 띄웠다 내림(`lsof -iTCP:18223` 0 줄). 18105 는 HTTP 읽기만. 18222 · 18220 · 18210 · 18005 · 18432 손대지 않음.
- 남은 것: 코디 18222 띄움 → 사용자 E4 · `/face-check` 좌표 눈 확인 · 화면 문구(빈 자리) · 프롬프트 초안 확인(C-1) · 허브 0.7 부위 칸(오면 `sites.SITES_FIELD` 한 줄).

## 1. 바뀐 파일

| 무엇 | 파일 |
|---|---|
| 새 패키지 | `clinic_chat/consult/`: `__init__` · `__main__` · `server` · `turn` · `ledger` · `material` · `tail` · `listing` · `sites` · `face_coords` · `carry` · `prompt` · `render` · `live` · `fake_turn` · `probe` · `e3` · `templates/{base,page,ui,face_check}.html` · `_face.svg` · `partials/{main,turn,answer,delta,step,error,rejected,list,sites}.html` · `static/`(벤더링 8 + `MEDIKIT-NOTICE.txt` + `consult.css` · `consult.js`) |
| 실행기 | `clinic_chat/llm/chat.py` · `clinic_chat/llm/chat_cli.py` |
| 프롬프트 | `prompts/consult.json`(0.1.0-draft) |
| 설정 | `clinic_chat/config.py`(칸 더하기만 — `chat_*` 11 + `default_chat_cli_cwd`) · `.env.example`(이름만) |
| 함께 쓰는 코드 | `walk/front.py`(+39줄) · `walk/jev_requests.py`(+8) · `columns/col_b.py`(선택 인자 둘 넘기기 · 2줄) · `walk/calls.py:59`(주석 `carried`) |
| 의존 | `pyproject.toml` `jinja2==3.1.6` · `python-multipart==0.0.33` · `uv.lock` |
| 시험 | 새 `tests/test_consult_{page,prompt,cli,ledger,material,listing,sites,turn,carry}.py` · `tests/consult_fixture.py` · `tests/fake_cli/fake_cli.py`(더하기만 +21 — 세션 id 되돌림 · `FAKE_CLI_DIE_AFTER` · `FAKE_CLI_SLEEP`) |
| README | 「상담 화면」 절 |

`git diff --stat tests/` = `tests/fake_cli/fake_cli.py` 하나(+21 · 0 삭제). **기존 `tests/test_*.py` 24 · `conftest.py` · `fake_hub.py` · `fake_jev.py` 변경 0**(W-4).

## 2. WP-0 실측(E1 · E2 — CLI 2.1.322 · 구독 · `claude-sonnet-5-5`)

| 칸 | 값 |
|---|---|
| E1 ① `--max-turns 1` | 받음 — 9 호출 전부 rc 0 · result subtype `success`(한도 오류 아님) |
| ② 기억 | 2턴 `PELICAN` · 3턴 `NACILEP` — 이어짐 |
| ③ 첫 글자 / 전체 ms | 1턴 1,332 / 2,185 · 2턴 2,361 / 2,907 · 3턴 3,671 / 4,234 |
| ④ 토큰 cache_read / creation | 1턴 0 / 576 · 2턴 0 / 602 · 3턴 602 / 23(셋째부터 앞 대화 캐시 읽힘) |
| ⑤ 세션 파일 | 고정 cwd 의 프로젝트 폴더에 생김(있음) · 지우지 않음 |
| ⑥ thinking · 모델 · init 세션 id | thinking 0 · `claude-sonnet-5-5` · init 키 `session_id` = 준 값(CL7 키는 `session_id` — `chat_cli.SESSION_KEY`) |
| 다른 cwd resume(W-5) | **됨** — 기억 이어짐(세션 파일은 처음 cwd 폴더에만) |
| ⑦ F7 스냅숏 | help 글대로 — 2턴에 다른 시스템 글(Y)을 줘도 X 의 표지 `[ALPHA]` 를 따름 |
| E2 답 중 kill → resume | 됨(rc 0 · 숫자 기억 O) · 끊긴 턴의 **질문은 세션 파일에 남고 반쪽 답은 안 남음** — 3턴 답이 「앞 질문(세기)은 안 했다」 고 인지. CL10 ② `broken` 은 보수적이다(규칙은 그대로 · 코디 판단 재료) |

## 3. E0(가짜 턴 · 18223 · headless Chrome dump-dom · 스크린샷)

| # | 결과 |
|---|---|
| E0-1 (가) 이벤트 이름마다 받는 자리 | **됨** — `list` → `#procedure-list` · `sites` → `#face-marks` · `delta` 덧붙임 · `done` / `turn_error` 통째(숨은 `sse-swap` 요소 + `hx-target` — DAY board 꼴) |
| E0-2 SVG 통째 바꾸기 | **됨 — 단 「SVG 를 감싼 div 통째」 꼴(EV3 의 대안)로 지었다**: `#face-marks` = div(같은 viewBox 의 점 `<svg>` + 얼굴 아래 라벨). 선 그림 SVG 와 겹쳐 그린다. 라벨이 HTML 이라 FC3 「한 SVG 안」 대신 이 꼴 — 점이 그려지는 것을 스크린샷으로 확인 |
| E0-3 delta 뒤 done 통째 · 다시 붙기 | 됨 — 끝 꼴 같음 · `Last-Event-ID` 다음부터(시험) · 앞 공백 · 줄바꿈 조각은 `<span>` 으로 싸서 보존(N-9) |
| E0-4 줄기 닫기 | 됨 — `close` 이벤트(`data: close`) · `sse-close="close"` · 서버 로그상 턴당 events GET 1 회(재접속 0) |
| E0-5 이벤트 이름 | `turn_error` 로 지음(W-3 ①) — 겹침 없음 · 오류 가짜 턴도 재접속 0 |
| E0-6 벤더링 8 sha | 본과 같음(시험 `test_e0_6`) · `MEDIKIT-NOTICE.txt` 사실만 · `consult.css` 에 `@font-face`(W-5) |

브라우저 눈 확인(18222)은 코디 몫으로 남김.

## 4. E3(실물 3턴 — 허브 18105 읽기 · Jev · 구독 CLI · `probe --e3`)

질문: 「팔자주름이 고민이에요」 → 「그중 필러는 어떤 시술이에요?」 → 「보톡스랑은 뭐가 달라요?」. 답의 옳고 그름은 기준 아님.

| 턴 | first_list / ttft / total ms | parts(jev · hub · llm) | 종료 | 새 줄 · 요약 줄 · seen | cache_read / creation | 든 후보 |
|---|---|---|---|---|---|---|
| 1 | 629 / 1,929 / 5,911 | 429 · 139 · 5,278 | 근거 충족 | 0 · 9 · 0 | 0 / 5,247 | — |
| 2 | — / 3,062 / 8,401 | 453 · 59 · 7,865 | 근거 충족 | 425 · 0 · 0 | 4,927 / 57,870 | CON-009 0.31 dropped · SITE-046 0.34 dropped |
| 3 | — / 3,116 / 9,699 | 411 · 101 · 9,150 | 근거 충족 | 514 · 0 · 0 | 62,797 / 60,870 | M2 0.67 dropped(사이 값) |

- 이벤트 순서: 1턴 `step… → list → sites → step → delta… → done` · 꼬리가 `delta` · `done` 에 0(세 턴). thinking 0 · 모델 `claude-sonnet-5-5` · 2 · 3턴 `resume`.
- **O-11**: 「팔자주름」 = 고민 CON-009 + 부위 SITE-046 둘 다 대상(target). `concern_candidates` 37 묶음 · 74 행 → 리스트 시술 15 · 계열 6 · 「계열 층만」 7 · 「그 밖」 2. 부위 점 0(허브 부위 칸 없음 — 0.7 전 · 오류 0).
- **N-6 어긋남(실패 아님)**: 2턴 「그중 필러」 는 resolve 가 필러 계열(M2)을 바로 잡아 계열 전체(425 줄 · 57,870 토큰)로 답했다 — 앞 리스트로 좁히지 않음(U-12 (a)). Jev 는 든 후보(고민 · 부위)를 0.31 · 0.34 로 떨궜다.
- 재료가 턴마다 크게 쌓인다(3턴 입력 캐시 합 12 만 토큰대) — CL13 한도 20 · AP8 한도는 턴 단위라 대화 누적은 막지 않는다(참고).
- 실제 서버(18223)로도 한 턴: `step×4 → list → sites → step → delta×70 → done → close` · 꼬리 0 · 내림.

## 5. 검수 WARN 닫은 것

| # | 어떻게 |
|---|---|
| W-1 | 든 후보는 `concepts` 와 따로 — 겹침 묶음 · 상품 이름 덮임 · 입구 고르기 재료에 안 듦 · yes 만 `carried`(사이 · no → `dropped`). 시험 T12(든 후보 둘 · 표 다름 → 둘 다 대상 · overlap 0 · Jev 요청 1). G7 이 든 대상에 안 걸림은 받아들임(gate 안 고침). **손댄 줄이 「가지 하나」 보다 많다**: `front.py` +39(든 후보 목록 · coverage 함께 · 후보 설명 · noul 나눔 · 결정 · CR6 가지 · `FrontResult.carried` 칸) · `jev_requests.py` `_target_instr` +8 |
| W-2 | 최종 코드에서 `walk(question, deps, carry=…, instr=…)` · `sites` 채움 · T6 은 전체 묶음에서 다시 돔 |
| W-3 | `turn_error` · `close`(data 줄 있음) · 빈 `sites` = 빈 요소 · 가짜 턴 오류 꼴 · T6 · T10 · E0 시험에 「조각 글자 > 0」 |
| W-4 | 기존 시험 파일 변경 0 · 가짜는 더하기만 |
| W-5 | `consult.css` `@font-face`(본 `day.css:108-113` 꼴 · 같은 폴더) |

## 6. SPEC · WORK 와 다르게 지은 곳 · 알릴 것

1. **EV3 / FC3** — `#face-marks` 를 선 그림 SVG 안 `<g>` 가 아니라 **div(점 svg + 라벨)** 로(위 E0-2). SPEC 이 허락한 대안.
2. **T17 예외 하나** — `consult/e3.py` 의 실측 질문 세 줄(한국어 시험 입력)을 W-7 예외(시험 자료)로 시험에 명시. 그 밖 `consult/` 코드 · 템플릿 한글 0.
3. 장부 맺는 줄에 칸 더함: `session_next{session_id}`(새 UUID 로 바뀐 것) · `conv_end`(`broken` · `build_changed`) · `llm.answered` · `llm.error` · `prompts.version` · 시작 줄에 `prompts.consult_at_start`. 턴 한도는 `llm.answered` 로 센다(N-5).
4. 요약 줄 장부에 `key`(고민|계열|gid 집합 해시 — B-6 다시 안 싣기용) · `concern_code` · `modality_name`. 「그 밖(unreached)」 행은 이름 없는 계열 줄 하나로 요약(AP4 에 자리 규정 없음).
5. `GET /c/{conv}/turns/{n}/events` — 서버를 다시 띄워 줄기가 없으면 204(브라우저가 다시 붙지 않게).
6. 오류 종류 코드(`data-error` · 빈 자리 `error-<종류>`): `empty` · `busy` · `broken` · `turn_limit`(자리 `turn-limit`) · `build_changed` · `prompt` · `auth` · `exit` · `timeout` · `session_mismatch` · `tool_call` · `not_subscription` · `rate_limit` · `cli_result` · `spawn` · `internal`. 대화가 끝난 종류에는 새 대화 링크(자리 `error-new-conversation`). 단계 코드(`step-<코드>`): `front` · `hub` · `depth` · `gate` · `llm_wait` · `llm`.
7. 설정 기본: `CHAT_DIR` = `runs/consult`(gitignore) · `CHAT_CLI_CWD` = 사용자 캐시 폴더 아래 `clinic-chat/consult-cli`(TMPDIR 무관).
8. 허브 부위 칸 이름은 임시 `concern_sites`(쌍 키 `concern_code` · `site_code` · `site_name` · `csi_id`) — 0.7 이 정하면 `sites.SITES_FIELD` · `PAIR_KEYS` 를 맞춘다.

## 7. 프롬프트 초안(`prompts/consult.json` 0.1.0-draft) — 시험 프롬프트에서 바꾼 줄

- `role`: `common.md` 머리 줄의 「질문 하나에 한 번 답하는 역할이다」 → 「여러 턴에 걸쳐 상담하는 역할이다」.
- `rules`: common 1 ~ 11 옮김 · 5 끝 「각각 빠짐없이」 → 「각각 말하되 깊이는 단계대로」 · 6 은 앞 문장만(뒤 「그 폭을 빠짐없이」 뺌 — 긴 목록 자리는 U-10) · 10 에 「짧게 · 」 · 12 뺌.
- `screen`(새): `## 화면` · 「시술 목록은 화면에 있다 · 이름을 늘어놓지 않는다.」 · 「짧게 · 물은 것만 · 되묻기로 끝.」
- `material`: `col_b.md` 3 줄에 「여러 턴에 걸쳐 자료가 온다.」 · 새 줄 셋(줄 번호 대화 전체에서 이어짐 · `seen_lines` 뜻 · 목록 요약 줄 `summary` 는 계열 하나에 한 줄) · 이름 목록 줄은 「목록에 있다고 그 이름의 값을 지어 말하지 않는다 — 값은 자료 줄에서만.」 한 문장만 · 4 · 6 · 7 · 8 ~ 15 그대로.
- `tail`: `col_b.md` 「답 꼬리」 그대로. `jev_front` target · kind · gap = `front.md` 글자 그대로(시험이 대조) · `target_carried` 새(영어).

## 8. 공개 · 비밀 확인

- 커밋될 파일 64 개(새 + 고침)에 홈 절대 경로 · 사용자 이름 · 키 꼴 · 내부 URL grep 0 건(127.0.0.1 · 라이선스 URL 제외). README 에 CLI 세션 폴더 · DAY · 앱 워크트리 홈 상대 경로를 옮기지 않음(N-11).
- PNG · 뽑은 윤곽 0(얼굴은 손 SVG path 18 줄). 실측 기록 · 장부는 `runs/consult/`(gitignore). `.env` 열지 않음.
- `git status --porcelain --ignored`: 커밋될 것 = 위 §1 · gitignore = `.env` · `runs/` · `data/` · 캐시.
