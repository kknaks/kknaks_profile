---
type: review
target: WORK-003-web (시험 화면)
worktree: /Users/kknaks/orca/workspaces/clinic_chat/phub-gold-jev (미커밋 · read-only 검수)
created_at: 2026-11-16
verdict: WARN
---

# review-code-web — 시험 화면 검수

## 판정: **WARN** (FAIL 0 · MED 2 · LOW 4 · INFO 4)

계약은 지켰다. 화면 전용 걷기 · 답 · 판정 로직이 없고, CLI · batch 동작도 그대로다. 바인딩은 127.0.0.1:18220 만 하고, 공개 레포에 넣을 것도 깨끗하다. ruff · pytest 도 통과했다.
WARN 은 화면 쪽 두 가지 때문이다. 사용자가 실제로 겪는다. ① 세트 문항을 고른 뒤 질문 칸을 고쳐도, 보내지는 것은 세트 질문이다 ② 끝난 뒤에도 카드 답이 기록된 답으로 바뀌지 않는다.

## ① 화면 전용 로직 0 · CLI/batch 동작 불변 — 통과

- `web/server.py:113` `POST /api/ask` → `runner.run_question` 을 그대로 부른다(기본값 `run=run_question` · `deps_factory=Deps.from_settings`) · 기록은 같은 `RunStore(runs_dir)` · 검증 문구와 draft 막기는 `runner.main` 과 같은 꼴이다(`server.py:131-139` ↔ `runner.py:141-149`).
- `progress.py` — sink 가 없으면 `emit` 이 바로 돌아간다(`:43-45`). sink 예외는 삼킨다(`:49`). 쓰는 것은 ContextVar 라 화면 task 마다 따로 놀고, batch · CLI 는 `listen` 을 하지 않으니 무동작이다.
- `runner.py` 바뀐 곳: `run_id` 인자를 받을 수 있게 됨(없으면 예전처럼 uuid · `batch.py:96` 은 넘기지 않음) · 열마다 `progress.column` 안에서 `start` · `column_done` 을 emit(값 계산은 `d.spec(...).effort_arg()` 뿐이라 부작용 없음) · `run_done`. 열 순서 섞기 · 오류 격리 · 줄 꼴은 그대로다.
- `llm/cli.py:188` — `text_delta` 에서 `emit("delta")` 한 줄만 늘었다. 답을 쌓는 방식(`res["answer"] +=`)은 그대로다.
- `columns/col_b.py` — 단계 ①~⑤ `emit("step")`(`:59,72,75,80,181`) · B 켬 앞에서 B `column_done` 을 먼저 알림(`:200-202`) · B 켬을 `progress.column("b_on")` 으로 감쌈(`:205`). 판정 · 종료 상태 · verified · 쪽 나눔 · NO_B_ON 분기는 건드리지 않았다. 서버는 `done_cols` 로 B 중복 알림을 하나로 줄인다(`server.py:102`).
- `runs.py` — `show_view` 를 함수로 뺐다. CLI `--show` 와 `GET /api/runs/{id}` 가 같은 함수를 쓴다(`runs.py:86` · `server.py:182`).

## ② 바인딩 — 통과

`server.py:29-30` HOST=127.0.0.1 · PORT=18220 · `main()` 기본값 · `__main__` 은 인자 없이 `main()`. 띄워 둔 프로세스를 `lsof` 로 보면 `127.0.0.1:18220 (LISTEN)` 이다(띄우거나 내리지 않음). 시험은 `test_port_is_18220_local_only`. 18105(허브)도 127.0.0.1 LISTEN 이고 손대지 않았다.

## ③ 지어 넣은 문구 — 대체로 통과(LOW 1)

화면 라벨을 하나씩 대조했다.
- WORK-003 에 있는 말: 보내기 · 세트 문항 · A 원장 / B gold+Jev / C gold MCP / B 켬 · trace · 고른 경로(범위 · 입구) · 읽은 폭(도구 호출 · 행 수) · 깊이 판단(Noul 결정) · 검사(gate) 결과 · `entry.unused[]` · 「추론 끔 = effort …」 · gold_hash.
- 옛 hub-evals 화면에 있는 말(`git show HEAD:web/*` grep): 도는 중 · 오류 · 질문 기록 · 채점 · 시각 · 질문.
- 코드 값을 그대로 보이는 것: 종료 상태 이름 · `end_reason` · llm/tool/hub/jev · 표 머리 tool/range/total/read/pages/complete/error.
- 「프롬프트 미확정(사용자 확인 전)」은 `prompts.status()` 의 기존 mark 다.
- 빈 상태 · 안내 문장은 새로 쓰지 않았다(빈 곳은 「–」).

API 오류 글 전수(`server.py`):

| 줄 | 글 | 출처 |
|---|---|---|
| 127 | `columns 는 a,b,c 중에서 — 받은 것 …` | runner CLI `--columns` 오류 글을 줄인 것 |
| 129 | `question 또는 set_id 하나` | **새 글**(L-4) |
| 134 | `세트에 없는 id: …` | runner CLI 와 같음 |
| 136 | `… 는 draft(사용자 확정 전) — Jev · LLM 으로 보내지 않는다` | runner CLI 와 같음 |
| 139 | `… 질문 문장 없음` | **새 글**(L-4) |
| 151 · 180 | `run_id 없음: …` | runs CLI 와 같음 |

## ④ 공개 레포 — 통과

- `git status --porcelain --ignored`: 커밋될 것 = `.env.example` · `README.md` · `.python-version` · `clinic_chat/` · `prompts/` · `pyproject.toml` · `tests/` · `uv.lock`. gitignore 된 것 = `.env` · `data/` · `runs/` · 캐시들. 세트 · 기록은 gitignore 자리에만 있다.
- 커밋될 파일 88개를 `grep -nE "/Users/|kknaks|sk-ant|ANTHROPIC_API_KEY=.+|TYPESAFE[A-Z_]*=.+|medisolve"`(uv.lock 빼고) 로 훑었다 → 0건.
- `clinic_chat/web/**` 에서 `/Users/|http(s)://|localhost|18xxx` 를 grep 했다 → 포트 상수와 docstring 의 `127.0.0.1:18220` 만 나온다. 정적 파일에 데이터는 없다. 질문 문장은 `/api/set` 이 실행할 때 로컬 세트에서 읽는다.
- `tests/test_web.py` 의 질문은 「가짜 질문」 · 범위 「시술」/「고민」 같은 일반 말뿐이다. 회사 데이터 본문은 없다.
- README e2e 표 14행에 화면 실행 한 줄과 포트 18220 이 있다(완료 조건 4).

## ⑤ 시험 — 통과

- `uv run ruff check .` → `All checks passed!`
- `uv run pytest -q` → **109 passed in 3.74s**. 실호출은 0이다(test_web 3건: 모의 runner · 모의 SSE · 진짜 runner + 모의 CLI/허브/Jev).
- 띄워 둔 서버에 GET 만 했다: `/api/meta` → prompts_mark 「프롬프트 미확정(사용자 확인 전)」 · answer_reasoning=`lowest_effort` · lowest_effort=`low` · gold_hash 있음. `/` → 200.

## ⑥ 사용자가 화면에서 만날 자리 · 지적 표

| # | 파일:줄 | 심각도 | 무엇 | 고칠 방향 |
|---|---|---|---|---|
| M-1 | `web/static/app.js:55-58,140-153` | MED | 세트 문항을 고르면 질문 칸에 그 문장이 들어간다. 그 뒤 칸을 고치거나 새로 써도 `set_id` 가 남아 있어 **세트 질문이 그대로 간다**(서버는 `set_id` 우선). 그런데 위 `current` 줄에는 고친 글(`$("q").value`)이 보여서, 화면에 적힌 질문과 실제로 보낸 질문이 다르다. | 질문 칸 `input` 때 세트 고르기를 비우거나, 세트를 고른 동안 질문 칸을 readonly 로. `current` 는 서버가 돌려준 값으로 |
| M-2 | `app.js:115,176-181` | MED | `end` 뒤 `openRun(runId, false)` 은 카드 답을 기록 답으로 갈아 끼우지 않는다. ⓐ B 가 여러 쪽이면 기록은 `"\n\n".join`(`col_b.py:152`) 인데 화면은 쪽 사이 구분 없이 이어 붙인다. ⓑ 쪽 중간에 CLI 오류가 나면 기록 answer 는 `""` 인데 화면에는 부분 답이 남는다(오류 뱃지는 뜸). 「질문 기록」에서 다시 열면 그제서야 맞게 보인다. | `end` 때 `row.columns[k].answer` 로 카드 답을 덮기(또는 `done` 에 answer 실어 보내기) |
| L-1 | `app.js:121,125-131,167` | LOW | delta 가 올 때마다 카드 전체를 다시 그리고 답 칸을 맨 아래로 내린다. 스트리밍 중에는 위로 올려 읽을 수도, 글을 고를 수도 없다. 열어 둔 `<details>` 도 다시 그려질 때 닫힌다(trace · 채점은 끝난 뒤 붙으니 주로 스트리밍 중 문제). | 답 노드만 `textContent +=` 로 고치기 · 사용자가 위로 올렸으면 자동으로 내리지 않기 |
| L-2 | `server.py:153-159` · `app.js:163,184` | LOW | EventSource 는 연결이 끊기면 저절로 다시 붙는데, 서버는 다시 붙은 구독자에게 이벤트 0번부터 다시 보낸다. 그래서 화면 답이 **두 번 붙는다**. | 이벤트에 `id:` 를 붙이고 `Last-Event-ID` 부터 보내기(또는 클라이언트가 재연결 때 카드 리셋) |
| L-3 | `col_b.py:200-202` · `server.py:102` | LOW | B 본 꼴 `done` 은 col_b 가 먼저 낸 것만 쓴다. 그 뒤(B 켬 도중) col_b 가 예외로 끝나면 runner 는 B 를 오류로 기록하는데, 화면은 앞선 정상 done 을 보인다. 지금 `answer()` 가 오류를 안에서 받아서 이런 길은 거의 없다. | 지금은 둠 · 기록 다시 보기가 진실 |
| L-4 | `server.py:129,139` | LOW | 새로 지은 API 오류 글 2개(위 ③ 표). 화면에서는 `current` 줄에 그대로 뜬다. | CLI 글 꼴(argparse 의 상호 배타 오류 등)로 맞추거나 코드 값만 |
| I-1 | `app.js:115` · `style.css .answer` | INFO | 답은 `white-space: pre-wrap` 날 글이라 **마크다운(`**` · `#` · 표)이 기호째 보인다**. 옛 hub-evals 화면도 렌더러 없이 날 글이었으니 「꼴」과는 맞다. | 원하면 코디/사용자가 결정(렌더러를 넣으면 cdn · 의존 늘어남) |
| I-2 | `runner.py:56-62` · `app.js:100` | INFO | 열은 **차례로** 돈다(SPEC-002 · 순서는 질문마다 섞음). 처음부터 모든 카드에 「도는 중」이 붙어서, 기다리는 열과 실제로 도는 열이 구분되지 않는다. 카드 배치는 A·B·B켬·C 로 고정이고 실제 순서는 `order.columns` 에만 있다. | 「도는 중」을 `start` 받은 뒤에만 붙이기(새 문구 없이) |
| I-3 | `server.py:86,141` | INFO | `live` 에 실행 이벤트가 쌓이기만 하고 지워지지 않는다(서버가 떠 있는 동안 늘어남 · 시험용이라 실해 작음). 서버를 다시 띄우면 지난 run 의 `/events` 는 404 이고 기록 다시 보기는 된다. | 끝난 지 N분 지난 것 지우기(선택) |
| I-4 | `server.py:186-188` · `app.js:52` | INFO | `/api/set` 은 draft 문항의 질문 문장도 내려 준다(option title · 고르기는 막힘). 로컬 화면에만 뜨고 커밋되지 않으며, 보내기는 서버가 400 으로 막는다. | 그대로 둬도 됨 |

## 남은 것

- 실물(브라우저 · 실제 B 열 스트리밍)은 코디 몫이다. 검수자는 실호출하지 않았고 `POST /api/ask` 도 부르지 않았다.
- M-1 · M-2 는 app 워커 한 판이면 고친다(app.js 만).
