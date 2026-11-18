---
type: work
id: WORK-002
title: "채팅 3열 비교 시험 구현 계획 — 클라이언트 · A 원장 MCP · B 걷기 · C 직접 · 기록 · 전체 답 키 · 채점 · batch"
status: draft
product: procedure-hub
feature: phub-gold-jev
version: 0.2.0
created_at: 2026-11-16
updated_at: 2026-11-16
tags:
  - product/procedure-hub
  - feature/phub-gold-jev
  - doc/work
  - status/draft
links:
  specs:
    - "orchestration/work/phub-gold-jev/SPEC-002-chat-eval.md (0.4.1 · 검수 PASS r5) ← 계약"
    - "orchestration/work/phub-gold-jev/SPEC-001-hub-gold-mcp.md (0.4.1 — 허브 도구 계약)"
  decisions:
    - "orchestration/work/phub-gold-jev/_RESUME.md §2 (2026-11-16 「SPEC 0.4.1 승인 · WORK → 구현 → 코디 검증(실물 호출 포함)까지」 · 브랜치 = 앱 kknaksss/phub-gold-jev base main)"
    - "orchestration/work/phub-gold-jev/_RESUME.md §2 (2026-11-16 「WORK 검수 뒤(코디)」 — F-1 · W2-1 / 「진행 순서(코디 · WORK-002 §11)」 — C-1 ~ C-3)"
  sources:
    - "orchestration/work/phub-gold-jev/review-work-001-002.md (0.1.0 검수 — WORK-002 FAIL 1 · WARN 6 · NOTE 7 → 0.2.0 에서 반영)"
    - "orchestration/work/phub-gold-jev/review-spec-001-002-r5.md §Z-1 ~ Z-3 (구현 때 한 줄씩)"
    - "para/resources/note/ai/llms.txt (Jev 사용 정본)"
  related:
    - "orchestration/work/phub-gold-jev/WORK-001-hub.md"
---

# WORK-002 — 채팅 3열 비교 시험 구현 계획

> 경로 접두어: `P` = 프로필 워크트리 · `W` = `$P/orchestration/work/phub-gold-jev` · `SM` = `$P/orchestration/work/_archive/procedure-hub/phub-ledger-redesign/silver-model`(gitignore · 로컬 데이터) · `APP-WT` = 앱 새 워크트리 `~/orca/workspaces/clinic_chat/phub-gold-jev`(브랜치 `kknaksss/phub-gold-jev` · base `origin/main` = `240c321` · 11-16 확인 — 이미 만들어져 있고 변경 0) · `APP-OLD` = 옛 워크트리 `~/orca/workspaces/clinic_chat/hub-evals`(커밋 `078ac99` · **읽기만** — `git show HEAD:<경로>` · 미커밋 수정이 있어 작업 트리를 읽지 않는다) · `HUB` = 로컬에 띄운 허브(WORK-001 §2-5 · `127.0.0.1:18105`).
> **계약은 SPEC-002 다**(허브 도구는 SPEC-001). 이 문서는 「어느 파일에 · 어떤 순서로 · 무엇으로 확인하나」 만 정한다. SPEC 에 없는 규칙 · 문턱 · 문구를 만들지 않는다 — 어긋나는 것을 찾으면 코드로 메우지 말고 보고한다.
> 공개 레포 규칙: **질문 문장 · 모범 답 · 답 원문 · 원장 문장 · 가격 값 · 키 · 내부 주소를 코드 · 시험 · 문서 · 커밋에 넣지 않는다.** 이 문서에도 질문 문장은 없다(문항은 id 로만).

## 0. 요약

- 앱 레포 `main` 에는 **파일이 셋뿐이다**(`README.md` · `.gitignore` · `.env.example`). 패키지 · `pyproject.toml` 이 없다 — 새 브랜치에서 **패키지를 처음부터 세운다.** 옛 `hub-evals` 브랜치에서 데이터 무관 배관만 옮겨 쓴다(§1).
- WP 여덟: **WP-1** 뼈대 · 클라이언트(Jev · 허브 REST · CLI LLM) → **WP-2** A 열(원장 로컬 stdio MCP 3) → **WP-3** B 걷기(단계 ① ~ ⑤ · RG1 ~ RG8 · 입구 고르기 · 묶음 표 · 깊이 · 종료 상태 · gate) → **WP-4** C 열 → **WP-5** 기록 → **WP-6** 전체 답 키 스크립트 + 세트 파일 → **WP-7** 채점 두 층 + 보고서 → **WP-8** batch 실행기 + 사용자 e2e 안내.
- **외부 서비스 경로는 실물 호출 1회가 완료 조건이다** — Jev 1 · `claude -p` Sonnet 1(추론 끔 가능 여부 첫 확인) · Haiku 1 · 로컬 허브 1(§2-6).
- **채점은 사용자가 확인한 답 키로만 한다 — 풀어 주는 플래그가 없다**(SPEC-002 §9-5 확인 절차 4). 채점 배관의 실물 확인(E6)은 **합성 키**(가짜 코드 · 가짜 이름)로만 하고 그 결과는 채점 수치가 아니다(§2-6 · §9).
- 답 프롬프트 문구의 사용자 확인 지점이 **SPEC-002 O-9 의 글자(「답 프롬프트 WP 앞」)와 다르다** — 초안으로 구현하고 e2e 보고 때 확인받는다(코디 결정 · §11 C-1). 확인 전 결과에는 「프롬프트 미확정」 이 찍힌다.
- 1회차는 **batch 로만** 돌린다 — 앱 화면 · 서버는 만들지 않는다(SPEC-002 §10). 그래서 앱은 포트를 열지 않는다.

## 1. 실제 레포 구조(확인 결과)

| 확인한 것 | 결과(11-16) | 이 계획에서 |
|---|---|---|
| `git ls-tree -r --name-only origin/main` | `.env.example` · `.gitignore` · `README.md` — **3 파일** | 패키지 · `pyproject.toml` · `uv.lock` · `.python-version` · `prompts/` · `tests/` 를 새로 만든다 |
| `origin/main:.gitignore` | `.env` · `.env.*`(`.env.example` 만 열림) · **`runs/` · `data/` · `raw/` · `*.jsonl`** · 파이썬 캐시 | 세트 파일 · 답 키 · 기록 자리는 전부 이 무시 규칙 안에 둔다(§2-4) — `.gitignore` 는 안 고쳐도 된다 |
| `origin/main:.env.example` | 이름 둘(`ANTHROPIC_API_KEY` · `TYPESAFE_API_KEY`) · 값 빈칸 | 이름만 덧붙인다(§2-5) · 값은 넣지 않는다 |
| `origin/main:README.md` | 실험 앱 한 줄 소개 + 데이터 · 키 규칙 | 「실행 안내」 절을 덧붙인다(WP-8) |
| `APP-OLD` `git ls-tree -r --name-only HEAD` | `clinic_chat/{clients,llm,quality,cases}/` · `runs.py` · `timing.py` · `batch.py` · `report.py` · `prompts/` · `tests/{fake_jev.py,fake_cli/,conftest.py,…}` · `pyproject.toml` | 아래 「옮겨 쓸 것」 표 |
| `APP-OLD pyproject.toml:4-14` | `requires-python >=3.12,<3.13` · `mcp==2.3.0` · `typesafe-sdk==0.7.5` · `pydantic-settings` · `httpx` · `anthropic[mcp]` · `fastapi` · `uvicorn` · `sse-starlette` | `mcp` · `typesafe-sdk` · `pydantic-settings` · `httpx` 만 가져온다. `anthropic`(SDK — D8) · `fastapi` · `uvicorn` · `sse-starlette`(화면 — O-14)는 **넣지 않는다** |

**옛 틀에서 옮겨 쓸 것 / 버릴 것**(SPEC-002 §6-2 · §6-4 · §7 · §2-3 — 파일은 `APP-OLD` 의 `HEAD` 판)

| 옛 파일(줄 수) | 판정 | 새 자리 | 메모 |
|---|---|---|---|
| `clinic_chat/clients/jev_client.py`(33) | **통째** | `clinic_chat/clients/jev_client.py` | `AsyncTypeSafeClient` · timeout 10초 · `CHOICE_MAX = 255` · `choice_stats`(`:28-33`) · `retry` 기본 `None`(`:19-25`) |
| `clinic_chat/clients/hub_rest.py`(104) | 틀만(`:16-41` — `_send` · `_req` · `timed` · 콤마 목록) | `clinic_chat/clients/hub_rest.py` | 도구 메서드는 SPEC-001 §4 의 8 로 새로 · **쪽 넘김 끝까지 읽는 `read_all`** 추가 |
| `clinic_chat/clients/hub_mcp.py`(98) | 틀만(`:1-40` — mcp 2.x import 경로 메모 · `ClientSession`) | `clinic_chat/clients/hub_mcp.py` | 실물 확인 · 시험용(C 열의 도구 호출은 CLI 가 직접 한다) |
| `clinic_chat/llm/cli.py`(664) | Claude 갈래만: `McpAttach`(`:55-62` — `intent_tools` · `tools` 칸 빼고) · `claude_args`(`:73-87`) · stream-json 읽기(`:92-309`) · 동시 실행 조임(`:555-562`) | `clinic_chat/llm/cli.py` | **Codex 갈래(`:330-520`) · `intent_*` 기록은 버린다** |
| `clinic_chat/llm/cli_process.py`(98) | 통째(`child_env` `:26-34` — API 키 지움) | 같은 이름 | Codex 전용 env 이름은 남겨도 무해 |
| `clinic_chat/llm/auth.py`(79) | Claude 구독 확인만 | 같은 이름 | 구독이 아니면 그 열 오류 |
| `clinic_chat/llm/specs.py`(35) | 틀만 | 같은 이름 | 모델 · effort · 타임아웃 설정 → `CliSpec` |
| `clinic_chat/quality/raw_tools.py`(294) · `raw_mcp.py`(51) | **꼴만**(도구 3 · 한도 · 경로 문법 · manifest) | `clinic_chat/raw/raw_tools.py` · `raw/raw_mcp.py` | SPEC-002 §2-3 표가 계약 · `truncated` 를 trace 에 남기게 |
| `clinic_chat/quality/judge.py`(157) | 틀만(`:39-41` 가린 입력 · `:56-60` 실패 근거 검사) | `clinic_chat/quality/judge.py` | 항목 · 입력은 SPEC-002 §8-3 으로 새로 |
| `clinic_chat/runs.py`(140) · `timing.py`(84) | 통째에 가깝게(`runs.py:1-30` 줄 저장 · 커밋 읽기 · `timing.py:12-25` `Clock`) | 같은 이름 | 줄 꼴은 SPEC-002 §7 로 |
| `tests/fake_jev.py`(116) | 틀만(`:1-12 · 22-30` — 실물 SDK 에 `MockTransport`) | `tests/fake_jev.py` | 옛 `INFO_RULES`(`:14-19`) 같은 옛 체계 규칙은 버린다 |
| `tests/fake_cli/`(`claude` 2줄 + `fake_cli.py`) · `tests/conftest.py:17-18`(실물 CLI 막기) | 틀만 | 같은 이름 | 단위 시험이 실물 CLI · 구독을 건드리지 않게 |
| `cases/case1~3.py` · `loop.py` · `walk_*.json` · `server.py` · `web/` · `verify_runs.py` · `rerun_report.py` · `report.py` · `batch.py` · `quality/word_check.py` · `normalize.py` · `pricing.py` · `clients/anthropic_client.py` · `tests/fake_hub/` · `tests/phase*/` · `prompts/*.md` | **버린다** | — | 옛 체계(intent 12 · section · 봉투) · SDK · 화면. `batch.py` · `report.py` 는 새로 쓴다 |

## 2. 공통 — 모든 WP 에 걸리는 것

### 2-1. 하지 말 것

- **사용자 포트 · 프로세스를 건드리지 않는다.** 앱은 포트를 열지 않는다. 허브가 필요하면 WORK-001 §2-5 의 **18105** 에 띄운 것만 쓴다(코디 또는 사용자가 띄운 것 · 이미 떠 있는 다른 포트의 허브를 죽이지 않는다).
- **개발 · 운영 DB 없음.** 이 앱은 DB 를 쓰지 않는다.
- **`.env` 를 열어 읽거나 출력하지 않는다.** 설정은 `config.py`(pydantic-settings)가 읽는다. 키 값은 로그 · 기록 · 보고에 「있음 · 없음」 만 적는다(옛 README 규칙).
- **SDK 로 LLM 을 부르지 않는다**(D8 — CLI 구독만). 자식 프로세스 env 에서 API 키를 지운다(`child_env`).
- 외부 호출은 **§2-6 의 실물 확인 단계와 WP-8 의 실행**에서만 한다. 단위 시험은 전부 모의(모의 Jev · 모의 CLI · 모의 허브 응답)다.
- `APP-OLD` 워크트리의 파일을 고치지 않는다(미커밋 16 — `$W/_RESUME.md` §1).
- 질문 문장 · 모범 답 · 답 키의 행 값 · 원장 확인 목록의 글은 **gitignore 로컬 파일에만** 둔다.
- 커밋 · push · PR 은 코디 몫이다.

### 2-2. 코드 레포 allowed_paths

앱 레포 **전체에서 새로 만드는 것**(main 에 코드가 없다): `pyproject.toml` · `uv.lock` · `.python-version` · `clinic_chat/**` · `prompts/**` · `tests/**`. **덧붙이기만 하는 것**: `.env.example`(이름 추가) · `README.md`(실행 안내 절). **안 고치는 것**: `.gitignore`(지금 규칙으로 충분 — 더 필요하면 묻는다).
gitignore 로컬(커밋 대상 아님): `.env` · `data/**` · `runs/**`.

### 2-3. 새 패키지 구조(제안 — O-11 「이름 · 자리 · 꼴 = 구현 때 정함」)

```
pyproject.toml · uv.lock · .python-version · .env.example · README.md
clinic_chat/
  config.py                     설정(§2-5 env) — pydantic-settings · 레포 루트 .env
  clients/  jev_client.py · hub_rest.py · hub_mcp.py
  llm/      cli.py · cli_process.py · auth.py · specs.py
  raw/      raw_tools.py · raw_mcp.py            A 열 원장 stdio MCP
  walk/     ranges.py        §3-2 범위별 허용 표(고정)
            calls.py         범위 + 입구 → 폭 조회 목록(BR1 ~ BR4) ← B 와 답 키 스크립트가 **같이** 쓴다
            entry.py         단계 ① — resolve · 겹침 규칙 · 범위 확정 RG1 ~ RG8 · 입구 고르기
            jev_requests.py  §3-3 state · 질문 id · 32 묶음
            breadth.py       단계 ② · 방문 장부(§3-5)
            depth.py         단계 ③ · C1 ~ C3
            verified.py      verified 행 모음 · 표지(layer · hier · attr · depth · read_as …)
            fold.py          §3-6 묶음 표 FT1 ~ FT5
            gate.py          단계 ④ K1 ~ K5 · G1 ~ G11
            end_state.py     §5 종료 상태
  columns/  col_a.py · col_b.py · col_c.py       열 하나 실행 → §7-2 꼴
  prompts.py                    프롬프트 파일 읽기 · sha256
  runs.py · timing.py           기록
  runner.py                     질문 하나 × 열(차례 · 순서 섞기)
  batch.py                      세트 실행
  evalset/  loader.py · key_calls.py · answer_key.py · pick.py
  quality/  gold_codes.py · checks.py · judge.py · ledger_diff.py · grade.py
  report.py
prompts/    common.md · col_a.md · col_b.md · col_c.md · judge.md · jev/*.md(영어 instructions)
tests/      conftest.py · fake_jev.py · fake_cli/ · fake_hub.py · test_*.py
```

### 2-4. 로컬 자리(전부 gitignore — `data/` · `runs/` · `*.jsonl`)

| 무엇 | 자리(제안) | 누가 쓰나 |
|---|---|---|
| 세트 파일 **69 문항**(질문 문장 · 기대 · 모범 답 원문) | `data/eval-set/set.jsonl` — 한 문항 한 줄. 칸 = SPEC-002 §9-4(`id` · `bundle` · `range` · `question` · `expected_end_state` · `expected_entries[]` · `expected_scope_gap` · `answer_key` · `ledger_diff` · `source` · `model_answer`) + **`two_readings`**(bool — 낱말 하나가 두 개념으로 읽힐 수 있는 문항 · 사용자 확정 · O-11 범위에서 이 문서가 더한 칸 · `expected_entries[]` 와 겸하지 않는다 — WP-7 Z-2) + `status`(`draft` \| `confirmed` — 추가 32 문항의 사용자 확정 여부) | WP-6(초안) → **사용자 확정** |
| 문항별 호출 명세 | `data/eval-set/calls/<id>.json` — `{id, range, entries[], calls[]{tool, request}, asked_fields[]}` | WP-6 |
| 전체 답 키 | `data/eval-set/answer-key/<id>.json` — SPEC-002 §9-5 「출력」 칸 | WP-6 스크립트 |
| 대조 요약 한 장 | `data/eval-set/key-summary.md` | WP-6 스크립트 → 사용자가 읽는다 |
| 프롬프트 확인 기록 | `data/eval-set/prompts-confirmed.json` — `{files{<프롬프트 파일>: sha256}, by, at}`(§5 「프롬프트 파일」 · §11 C-1) | 사용자 확인 뒤 코디가 명령으로 적는다 |
| 배관 확인 결과(합성 키) | `runs/plumbing/`(E6 — `runs/quality.jsonl` · `runs/reports/` 와 섞이지 않는다) | WP-7 |
| 기록 | `runs/runs.jsonl`(한 질문 한 줄 · 고치지 않음) · `runs/quality.jsonl`(채점 덧붙임) | WP-5 · WP-7 |
| 보고서 | `runs/reports/<batch_id>.md` | WP-7 |
| CLI 임시 cwd | 시스템 임시 폴더(실행마다 새로 — 격리) | WP-1 |

- 37 문항의 질문 문장은 세트 파일에 **복사하지 않는다** — `id` 로 `questions.csv` 를 가리키고(`QUESTIONS_CSV` env) 로더가 실행 때 읽는다(SPEC-002 §9-4). 세트 파일에 문장이 직접 든 것은 추가 32 문항뿐이다.
- 모범 답 원문(`model_answer`)은 SPEC-002 §8-6 꼴의 문항에만 있고 이 파일에만 둔다.

### 2-5. env(이름만 — 값은 앱 `.env`(gitignore) · 문서 · 레포에 값 없음)

| 묶음 | 이름 | 뜻 |
|---|---|---|
| 키 | `TYPESAFE_API_KEY` | Jev. **`ANTHROPIC_API_KEY` 는 쓰지 않는다**(있어도 자식 env 에서 지운다) |
| Jev | `TYPESAFE_DEFAULT_MODEL` | Jev 모델 고정(llms.txt §4) |
| LLM | `ANSWER_MODEL`(Sonnet / Haiku) · `JUDGE_MODEL`(Opus 기본) · `CLAUDE_CLI_EFFORT` · `CLI_TIMEOUT_SEC` · `CLI_MAX_CONCURRENT` · `ANSWER_REASONING`(`off` \| `lowest_effort` — §2-6 확인 결과로 정함) | SPEC-002 §6-1 |
| 허브 | `HUB_REST_URL`(예: `http://127.0.0.1:18105/procedure-hub/gold`) · `HUB_GOLD_MCP_URL`(예: `…/procedure-hub/gold-mcp/mcp`) · `HUB_PAGE_LIMIT` | 로컬 허브 |
| A 열 | `RAW_DIR` = `$P/orchestration/work/phub-recommend/bronze/phub-ledger`(파일 24 = JSON 21 · md 2 · txt 1 — 11-16 `ls` 셈) | SPEC-002 §2-3 |
| 걷기 | `JEV_NOUL_YES_AT`(0.7) · `JEV_NOUL_NO_AT`(0.3) · `RANGE_CONFIDENCE_AT`(0.7) · `RANGE_RATIO_AT`(2.0) · `JEV_BATCH_SIZE`(32) · `WALK_MAX_STEPS`(10) · `ANSWER_INPUT_MAX_TOKENS` | SPEC-002 §3-4 · §3-1 C3 · §3-6 FT4 — 전부 임시값 |
| 세트 · 채점 | `EVAL_SET_DIR`(`data/eval-set`) · `QUESTIONS_CSV`(`$SM/gold/questions.csv`) · `GOLD_CSV_DIR`(`$SM/gold` — **채점 단계만** 읽는다) · `LEDGER_CHECK_PATH`(`$SM/notes/ledger-check-list.csv` — 채점 단계만) | SPEC-002 §8-2 · §8-4 · §9 |
| 기록 | `RUNS_DIR`(`runs`) | SPEC-002 §7 |

`GOLD_CSV_DIR` · `LEDGER_CHECK_PATH` · **`QUESTIONS_CSV` · `EVAL_SET_DIR`**(답 키 · 세트 파일 폴더 — `questions.csv` 에는 `answer` 칸이 있다)은 **답을 만드는 세 열의 프로세스에 주지 않는다**(자식 env 에서 지운다 — A 의 원장 MCP 는 `RAW_DIR` 밖을 못 읽는다 · SPEC-002 §2-3 · §8-4). 문항의 질문 문장은 부모 프로세스(`runner`)가 읽어 프롬프트로만 넘긴다.

### 2-6. 실물 확인 단계(외부 서비스 경로 = 실물 호출 1회가 완료 조건)

단위 시험(모의)이 통과해도 **아래를 실물로 한 번씩 부르기 전에는 그 WP 를 완료로 적지 않는다**(E4 만 WP-1 이 아니라 WP-3 의 진입 조건이다 — 허브 WP-3 뒤에야 돌 수 있다). 키 · 구독은 앱 `.env` · 로컬 로그인에서 읽는다 — 워커가 `.env` 를 열지 않고 명령만 돌린다. 키가 없거나 구독이 아니면 **「못 돌림」 으로 보고**하고 코디에게 넘긴다(모의 결과를 실물인 것처럼 적지 않는다).

| # | 무엇 | 어느 WP | 명령(제안) | 보고에 적을 것 |
|---|---|---|---|---|
| E1 | **Jev 1회** — Choice 하나 + Noul 둘을 한 요청으로(합성 state · 회사 데이터 없음) | WP-1 | `uv run python -m clinic_chat.clients.jev_client --ping` | 응답의 실제 `model` id · `choice` · `confidence` · `probabilities` 키 수 · `noul` 값 · 걸린 ms. 요청 꼴이 llms.txt §1 · §2 와 맞는지 |
| E2 | **`claude -p` Sonnet 1회 + 추론 끔 확인** — **구현 첫 확인 항목**(SPEC-002 O-23) | WP-1 | `uv run python -m clinic_chat.llm.cli --ping --model <Sonnet>` | ① CLI 가 추론을 끄는 설정을 받는가(`claude --help` · CLI 문서 · 실물 stream-json 에 thinking 블록이 없는지로 확인 — 11-16 `claude --help` 에서 보이는 것은 `--effort <level>` 하나다) ② 못 끄면 받는 **가장 낮은 effort** 값 ③ 그 결과로 `ANSWER_REASONING` = `off` 또는 `lowest_effort` ④ 실제 model id · 구독 과금(`billed = subscription`) · ms |
| E3 | **`claude -p` Haiku 1회** | WP-1 | 같은 명령 `--model <Haiku>` | 실제 model id · 같은 격리 인자가 받아들여지나(effort 를 안 받으면 그 사실) · ms |
| E4 | **로컬 허브 1회** — REST `health` + 도구 한 건(쪽 넘김 끝까지) + MCP `list_tools` + 모의 응답 꼴 ↔ 실물 응답 꼴 대조(§11) | **WP-3 진입 조건**(허브 WP-3 뒤 — WP-1 의 완료 조건이 아니다 · WP-6 의 실물도 이 뒤) | `uv run python -m clinic_chat.clients.hub_rest --ping` | `gold_hash` · `total` · 쪽 수 · MCP 도구 수(8) |
| E5 | **세 열 한 질문**(세트 문항 하나 — **37 문항 중 하나** · 부위·고민이 아닌 폭이 작은 문항 · `draft` 문항은 쓰지 않는다 · A · B · C 차례) | WP-8 | §10-2 의 한 질문 명령 | 열마다 종료 · ms · 호출 수 · `runs.jsonl` 한 줄이 SPEC-002 §7 꼴인지 |
| E6 | **채점 배관 1회 — 합성 키**(Opus 실물 호출 1 · 입력은 전부 합성: 가짜 코드 · 가짜 이름으로 만든 질문 · 답 · 답 키. **세트 문항 · 세트 답 키 · E5 의 줄을 쓰지 않는다**) | WP-7 | `uv run python -m clinic_chat.quality.grade --plumbing`(§9 「E6 — 합성 키 배관 확인」) | 구조화 출력이 항목 5 로 오나 · 실패 근거 칸이 있나 · 결과에 「합성 키 — 배관 확인 · 채점 수치 아님」 이 찍혔나. **항목별 통과 / 실패 값은 보고에 채점 수치로 적지 않는다** |

- E1 ~ E4 · **E6** 은 회사 데이터를 실어 보내지 않는다(합성 state · 「한 문장으로 답하라」 꼴의 빈 프롬프트 · E6 은 합성 질문 · 합성 답 · 합성 키). E5 만 세트 문항이 Jev · LLM 으로 나간다 — 옛 README 규칙대로 **환자 정보 없는 질문**뿐이고, **사용자가 확정하지 않은 `draft` 문항은 보내지 않는다**(37 문항 중 하나).
- **실제 채점(세트 문항의 점수)은 실물 확인 단계에 없다.** 사용자가 답 키를 확인한(`confirmed`) 뒤에만 돈다(SPEC-002 §9-5 확인 절차 4 · §8 「사용자 확인 절차」 4).
- `--ping` 진입점은 제안이다 — 같은 확인을 `tests/` 밖의 한 줄 스크립트로 해도 된다. **`pytest` 로는 실물을 부르지 않는다.**

### 2-7. 검증 명령(전 WP 공통 틀 — `APP-WT` 에서)

```bash
uv sync
uv run ruff check .
uv run pytest tests/test_<이 WP 것>.py -q      # 모의만 — 키 · 허브 · 구독 없이 통과해야 한다
```

WP 마다는 그 WP 의 시험만 돌리고, **전체 `uv run pytest -q` 는 WP-8 끝에 한 번** 돌린다. 허브 쪽 검증 명령(README 「검증」 · `DATABASE_URL=sqlite+aiosqlite:///:memory:` · 데이터 env 없으면 skip)은 WORK-001 §2-4 다 — 앱은 DB 를 안 쓰므로 그 env 가 필요 없다. 앱에서 「데이터 env 가 있으면」 하는 것은 **WP-6 의 37 문항 `gold_pointers` 대조**(`sample_check`)다.

## 3. WP-1 — 뼈대 · 클라이언트(Jev · 허브 · CLI LLM)

**목표**: 패키지를 세우고 세 외부 경로(Jev · 허브 · `claude -p`)의 클라이언트를 옛 틀에서 옮긴다. 실물 E1 ~ E3(E4 는 허브 WP-3 뒤 · WP-3 진입 조건).

**SPEC-002 대응**: §6-1(경로 · 모델 · 추론 끄는 법) · §6-2(가져갈 것 · 버릴 것 전 행) · §6-4(Jev 클라이언트) · §2-2(같은 CLI · 같은 격리 옵션) · O-16(Jev 설정 = 옛 값 그대로) · O-23(추론 끔 확인).

**만들 파일**: `pyproject.toml` · `.python-version` · `clinic_chat/__init__.py` · `config.py` · `clients/{jev_client,hub_rest,hub_mcp}.py` · `llm/{cli,cli_process,auth,specs}.py` · `tests/{conftest.py,fake_jev.py,fake_cli/,fake_hub.py,test_clients.py,test_cli.py}` · `.env.example`(이름 추가).

**옛 틀에서**: §1 「옮겨 쓸 것」 표의 `jev_client.py`(통째) · `hub_rest.py:16-41` · `hub_mcp.py:1-40` · `cli.py:55-62 · 73-87 · 92-309 · 555-562` · `cli_process.py:26-34` · `auth.py` · `specs.py` · `tests/fake_jev.py:1-12 · 22-30` · `tests/fake_cli/` · `tests/conftest.py:17-18`.

**구현 메모**

- `hub_rest.py`: 도구 메서드 8 + **`read_all(tool, request)`** — `next_cursor: null` 까지 넘기고 `{total, pages, read, complete, rows…, 쪽 밖 목록}` 을 낸다. 「읽은 쪽 단위 수 ≠ `total`」 이면 `complete = false`(G9 · K1 재료). 응답 `build` 가 도중에 바뀌면 오류. **허브 오류는 본문 문구가 아니라 HTTP 상태(422 · 404 · 400)로 가른다** — 문구 접두(`<코드 이름>: …`)는 SPEC-001 에 아직 없는 꼴이라(WORK-001 §9 H-2) 거기에 기대지 않는다(문구는 기록에만 남긴다).
- `cli.py`: 인자는 옛 `claude_args` 그대로(내장 도구 끔 · 사용자 설정 안 읽음 · `--strict-mcp-config` · 세션 안 남김 · 시스템 프롬프트 갈아 끼움 · 프롬프트 stdin). **추론 설정 인자 하나**를 `CliSpec.reasoning`(`off` \| `lowest_effort` \| `on`)으로 더한다 — 실제 인자는 E2 결과로 채운다.
- `hub_mcp.py` 는 E4 와 시험에서만 쓴다. C 열의 도구 호출은 CLI 가 `--mcp-config`(http)로 직접 한다.
- 모의 허브(`tests/fake_hub.py`)는 **응답 꼴 · 쪽 넘김 · 오류**만 낸다(§11 의 「모의 허브의 한계」).

**완료 조건**

1. `uv sync` · `uv run ruff check .` · WP-1 시험이 키 · 허브 · 구독 없이 통과한다.
2. 모의 CLI 로: 인자에 격리 옵션이 전부 있고 · 프롬프트가 stdin 으로 가고 · 자식 env 에 API 키 · `TYPESAFE_API_KEY` · `GOLD_CSV_DIR` · `LEDGER_CHECK_PATH` · `QUESTIONS_CSV` · `EVAL_SET_DIR` 가 없다.
3. `read_all` 이 모의 허브의 3 쪽 응답을 끝까지 읽고 `read == total` · 중간 오류면 `complete = false` 를 낸다.
4. **E1 · E2 · E3 실물 통과**(§2-6). E4 는 이 WP 의 완료 조건이 아니다 — 허브 WP-3 뒤에 돌리는 **WP-3 진입 조건**이다(`--ping` 진입점 · 모의 허브는 이 WP 에서 만들어 둔다). E2 의 결론(`off` 가능 / `lowest_effort` 와 그 값)을 보고에 적고 `.env.example` 의 `ANSWER_REASONING` 설명에 반영한다.
5. Jev 오류 · 시간 초과가 예외로 올라온다(조용히 빈 값으로 바뀌지 않는다 — SPEC-002 §6-4 「실행 중단」 재료).

## 4. WP-2 — A 열(원장 로컬 stdio MCP 3)

**목표**: 원장 JSON 을 읽는 로컬 stdio MCP 서버(도구 3)와 A 열 실행을 만든다.

**SPEC-002 대응**: §2-1(A 열) · §2-2 · §2-3 전부(지킬 것 넷 · 서버 표 · 도구 3 표 · A 의 trace `paths[]` · `truncated`) · §6-2(A = stdio 붙이기) · §7-3(A trace).

**만들 파일**: `clinic_chat/raw/{__init__,raw_tools,raw_mcp}.py` · `clinic_chat/columns/col_a.py` · `prompts/col_a.md` · `tests/test_raw_tools.py` · `tests/test_col_a.py`.

**옛 틀에서(꼴만)**: `APP-OLD clinic_chat/quality/raw_tools.py:16-26`(파일 목록 · 한도 값) · `:80`(정규화 = 공백 지우기 · 소문자) · `:101-119`(시작 때 읽기 · manifest) · `:136-245`(도구 3) · `:271-292`(입력 꼴) · `raw_mcp.py:14-47`(서버 이름 · `MCPServer` · `run("stdio")` · `RAW_DIR`).

**구현 메모**

- 읽는 파일 = `RAW_DIR` 의 원장 JSON. 옛 틀은 21 파일 이름을 코드에 고정했다(`raw_tools.py:16-22`) — 지금 폴더의 JSON 도 21 개다(그 밖에 md 2 · txt 1 은 읽지 않는다). **이름 목록을 코드에 박지 않고 「`RAW_DIR` 의 `*.json` 전부」 로 두고 manifest(`dir_manifest_sha16` · `files`)에 남긴다**(제안 — 파일 이름이 공개 레포 코드에 안 남는다 · O-11 범위). JSON 이 0 이면 서버 시작 실패.
- gold · silver · `g_entry` 를 import 하지 않는다(기준선).
- 경로 문법이 「파일 이름으로 시작」 이라 폴더 밖을 못 가리킨다 — `..` · 절대 경로 · 모르는 파일 이름은 도메인 오류.
- A 열 trace: 호출마다 `paths[]`(`raw_get` = 입력 `path` · `raw_search` = `hits[].path` · `raw_list` = 빈 목록)와 `truncated`.

**완료 조건**

1. 합성 원장(가짜 JSON 2 파일 · `tmp_path`)으로 도구 3 의 입력 한도 · 출력 꼴이 SPEC-002 §2-3 표와 같다(`depth` 0~3 · `max_bytes` 최대 20,000 · `limit` 1~100 · `snippet_chars` 1~200 · `query` 1~100자).
2. 폴더 밖 경로 · 없는 파일 → tool 오류(서버는 죽지 않는다). `RAW_DIR` 없음 · 파일 0 → 서버 시작 실패.
3. 모의 CLI 로 A 열을 돌리면 `--mcp-config` 가 stdio · `--allowedTools mcp__<서버 이름>` 이고, trace 에 `tool_calls[]{tool, input, output_bytes, paths[], truncated}` 가 남는다.
4. 실물: `RAW_DIR` 을 준 서버가 뜨고 `raw_list` 한 번이 파일 수 · manifest 를 낸다(값 본문은 보고에 적지 않는다 — 파일 수 · sha16 만).

## 5. WP-3 — B 걷기(단계 ① ~ ⑤)

**목표**: B 열 전체 — Jev 경로 → 허브 폭 전부 → Jev 깊이 → 앱 틀린 말 검사 → LLM 답.

**진입 조건(실물 몫)**: 하위 묶음 3-a 와 단위 시험은 허브 없이 시작한다. **실물 걷기는 E4 통과 뒤**다(§2-6 — 허브 WP-3 뒤).

**SPEC-002 대응**: §3-1(흐름 · RG1 ~ RG8 · 입구 고르기 · 폭과 깊이 · BR1 ~ BR4 · 단계별 지킬 것 · C1 ~ C3) · §3-2(범위별 허용 표 전 행 · 아래 불릿) · §3-3(Jev 요청 꼴 · 질문 id · 32 묶음) · §3-4(문턱) · §3-5(방문 장부) · §3-6(FT1 ~ FT5) · §4(G1 ~ G11 · K1 ~ K5 · 답 전) · §5(종료 상태 여섯 · 「원천 미확정」 세 조건) · §6-1(B 단계 ⑤ · 끔/켬) · §6-3(P1 ~ P8 · B 에만 해당하는 것) · O-4 · O-5 · O-20 · O-21.

**만들 파일**: `clinic_chat/walk/{ranges,calls,entry,jev_requests,breadth,depth,verified,fold,gate,end_state}.py` · `clinic_chat/columns/col_b.py` · `prompts/{common,col_b}.md` · `prompts/jev/{range,entity,entry,candidate,answer_ready}.md` · `tests/test_walk_*.py`.

**옛 틀에서**: 걷기 로직은 **가져오지 않는다**(`cases/case3.py` · `loop.py` · `walk_order.json` 은 옛 체계). 가져오는 것은 WP-1 의 Jev 클라이언트 · `choice_stats` · `tests/fake_jev.py` 틀뿐이다.

**하위 묶음(이 순서로)**

| # | 무엇 | SPEC 절 | 파일 | 꼭 시험으로 잡을 것 |
|---|---|---|---|---|
| 3-a | 범위별 허용 표 + 폭 조회 목록 | §3-2 · §3-1 BR1 ~ BR4 | `ranges.py` · `calls.py` | 범위 8 + 속성 시작의 「폭」 칸이 표 그대로(도구 · facet · `roles` · `classes` · `package_kinds` · `hier` 기본) · 입구가 둘 이상이면 필터(`filters.adverse_code` · `filters.condition_code` · `site`) · **그 밖의 좁힘 입력이 없다**(BR2) · 부위·고민은 `groups` 후보마다 `facets` profile(`roles` = `자기` · `물려받음`) · 속성 시작은 그 속성 표의 맞춤 facet 전부(2 · 1 · 2 · 7). **`calls.py` 한 함수를 B 와 답 키 스크립트(WP-6)가 같이 쓴다** — BR3 을 코드 공유로 지킨다. **3-a 는 WP-6 보다 먼저 끝나야 한다**(WP-6 의 6-b 가 이 함수를 쓴다 — §11) · 3-a 는 Jev · LLM · 허브 실물 없이 선다 |
| 3-b | 단계 ①-1 · ①-2 — `resolve` · 겹침 가르기 · 범위 Choice 9 | §3-1 단계표 ①-2 · §3-3 | `entry.py` · `jev_requests.py` | 겹침은 범위 규칙 먼저(semantic-map §1 순서) · Choice 는 하나 고를 때만 · 옵션 9 · 선택지는 앱이 펼친 것뿐 · **(r5 Z-1)** 아래 「Z 한 줄」 |
| 3-c | 단계 ①-3 — 범위 확정 RG1 ~ RG8 | §3-1 RG 표 | `entry.py` | RG2 하나 · RG3 둘 · RG4(입구 있으면 「범위 밖」 으로 안 끝냄 · `scope_gap`) · RG6(두 개념 다) · RG7(합) · RG8(겹침을 가른 **뒤** 남은 입구에 `condition` · `adverse` → 범위 더함 · 다른 표로 갈린 낱말로는 안 더함 · RG6 경유면 `via = RG6` + 표지 — **(r5 Z-2)**) |
| 3-d | 단계 ①-4 — 입구 고르기 | §3-1 「입구 고르기」 표 | `entry.py` · `jev_requests.py` | `resolve` 후보 0 일 때만 · 범위(들)의 입구 목록을 쪽 넘김 끝까지 · 개념 하나로 묶음 · 32 묶음으로 **전부** · 결과 셋(`confirmed` / `ask_back` / `none`) · `entry.by = noul` + 「이 입구로 읽었다」 표지 |
| 3-e | 단계 ② — 폭 전부 · 방문 장부 | §3-1 단계 ② · §3-5 · G9 | `breadth.py` · `verified.py` | 조회마다 `next_cursor: null` 까지 · 쪽 밖 목록 포함 · 읽은 것 **전부** `verified` 에 · 같은 키 두 번 안 읽음 · 못 읽으면 「실행 중단」 |
| 3-f | 단계 ③ — 깊이(재귀) | §3-1 단계 ③ · C1 ~ C3 · §3-2 「깊이」 칸 · §3-4 | `depth.py` | 후보 Noul 32 묶음 전부 · `deepen` / `listed_only` / `uncertain` / `gate_forced` — **깊이만 가른다(목록에서 안 뺀다)** · `answer_ready` 는 `verified` 갱신 **뒤**(③-4) · C2 · 걸음 상한 → 「실행 중단」 · 깊이 칸 「없음」 범위는 ② → ③-4 · **B 는 `neighbors` 를 안 부른다** |
| 3-g | 묶음 표 | §3-6 FT1 ~ FT5 | `fold.py` | 같은 값만 접고 **칸을 빼지 않는다** · 빈칸도 값 · `gid` 전부 · 표지 유지 · 한도 넘으면 묶음 경계에서 쪽 나눔 → 부분 답을 쪽 순서대로 잇기 · 못 실으면 「실행 중단」 · **펼치면 원래 행과 같다**(접기 ↔ 펼치기 왕복 시험) |
| 3-h | 단계 ④ — 틀린 말 검사 | §4 K1 ~ K5 · G1 ~ G11 | `gate.py` | K1(읽은 수 = `total` · `gid` ⊂ `verified_gids` · 전 칸) · K2 · K3(G1 · G3 · G7 `gate_forced`) · K4(표지 — 층 · `polarity` · `same_day` 빈칸 · 충돌 · `evidence_kind` · 케이스 행의 「말할 이름 = `procedure_name`」 · `price_mid_raw` 「계산 · 정렬 금지」) · K5(읽기로 한 범위 밖 행 없음) · 실패 = 「실행 중단」 |
| 3-i | 종료 상태 | §5 표 · 세 조건 | `end_state.py` | 여섯 상태의 조건 그대로 · (가)(나) 는 `ledger_check[]` 로 · (다) 는 1회차에 판정 안 함(facet 단위 required — Q12 가 기대와 어긋날 것을 알고 간다 · O-5 ②) · `scope_gap` 은 상태가 아니라 표지 |
| 3-j | 단계 ⑤ — 답 | §6-1 · §6-3 · §3-6 FT4 | `col_b.py` · `prompts/` | 도구 없음 · 추론 = `ANSWER_REASONING` · 입력 = 공통 답 지시 + B 단락 + 묶음 표 + 종료 상태 + `scope_gap` + 「어느 입구로 읽었나」 · 같은 `verified` 로 「켬」 한 번 더(`columns.b_on`) · **「범위 밖」 · 「입구 없음」 · 「실행 중단」 에서도 부른다 — 입력은 `end_state` + 빈 `verified`**(아래 「단계 ⑤ 를 부르는 범위」) |

**r5 Z 를 여기서 한 줄씩**

- **Z-1**(3-b): 「규칙으로 못 가르는 겹침」 은 **같은 표 안 겹침만이 아니다** — 표 사이 겹침인데 읽는 범위의 시작 표에 **어느 쪽도 없을 때**(예: 고민 ↔ 부작용이 겹친 낱말을 시술 범위에서 읽음)도 범위 규칙이 못 가르므로 entity Choice 로 간다. 불확실하면 RG6(두 개념 다). 이렇게 해야 RG8 이 볼 「남은 입구」 가 늘 정해진다(SPEC-002 §3-1 의 158 · 191 줄과 같은 뜻 — 240 줄 괄호를 넓게 읽는다).
- **Z-2**(3-c · 3-e): RG6 경유로 더한 범위의 `verified` 행에 붙이는 표지의 필드 이름 = **`read_as{by: "rg6", table, code}`**(제안 — 단계 ①-4 의 입구 표지 `read_as{by: "noul", table, code}` 와 같은 꼴 · 한 필드). 답 프롬프트 B 단락은 이 표지가 있으면 「질문의 말을 이 개념으로도 읽었다」 를 밝히게 한다. 채점 쪽 목록은 WP-7 에.
- (Z-3 은 WP-7.)

**프롬프트 파일(문구 — SPEC-002 §6-3 「문구는 WORK 에서」 · O-9)**

- `prompts/common.md` 는 P1 ~ P8 을 **규칙 문장**으로 옮긴다. `col_a.md` · `col_b.md` · `col_c.md` 는 「자료를 얻는 법」 한 단락만 다르다.
- **앱 코드는 사용자에게 보일 고정 문구를 갖지 않는다** — 종료 상태별로 「무엇을 말해야 하나 · 말하면 안 되나」(SPEC-002 §5 표의 두 칸)를 프롬프트에 규칙으로 주고, 문장은 LLM 이 쓴다(`_RESUME.md` §2 11-16 「WORK 검수 뒤(코디)」 — 「앱 문구 지어 넣지 않음」).
- **단계 ⑤ 를 부르는 범위(코디 결정 — §11 C-4)**: 「범위 밖」 · 「입구 없음」 · 「실행 중단」 으로 끝난 질문도 **단계 ⑤ 를 불러 그 상태를 말하게 한다.** SPEC-002 §4 의 글자(「단계 ④ 를 통과해야 단계 ⑤ 로 간다」)와 다른 자리라 조건을 글자로 박는다:
  1. 이 세 상태의 단계 ⑤ 입력 = 공통 답 지시 + B 단락 + **`end_state`** + 사유(앱이 가진 **코드 값**만 — 어느 단계 · 어느 검사 K1 ~ K5 / G 번호 · 오류 종류. 사람에게 보일 문장을 앱이 지어 넣지 않는다) + **빈 `verified`**(행 0 · 묶음 표 0).
  2. **검사(단계 ④)에 실패한 행 · 읽다 만 행 · 쪽을 못 넘긴 조회의 행은 싣지 않는다** — 「실행 중단」 의 `verified` 는 프롬프트에 한 행도 안 간다. 그래서 「검사를 통과하지 못한 자료가 답에 실리지 않는다」 는 SPEC-002 §4 의 뜻은 그대로다.
  3. 「입구 없음」 에서 단계 ①-4 가 `ask_back` 으로 끝났으면 되묻기에 쓸 후보 입구는 **`resolve` · 입구 목록이 낸 이름과 코드 그대로**(행 값 아님 · `verified` 아님) 함께 준다 — 무엇을 되물을지는 SPEC-002 §3-1 「입구 고르기」 표의 결과이고 문장은 LLM 이 쓴다.
  4. **세 열 같은 조건**: A · C 는 처음부터 LLM 이 답을 쓰므로 이 세 상태에서도 답 문장은 세 열 모두 같은 모델 · 같은 공통 답 지시로 나온다. 앱이 B 에만 고정 문구를 넣지 않는다.
  5. **단계 ⑤ 를 부를 수 없는 「실행 중단」**(CLI · 구독 오류 · 시간 초과로 LLM 자체를 못 부름): `answer` 는 **빈 값** · 그 열의 `error` 에 사유를 남긴다. 앱이 대신 문장을 채우지 않는다. Jev · 허브 오류로 난 「실행 중단」 은 LLM 을 부를 수 있으므로 1 의 꼴로 부른다.
  6. 이 세 상태에는 「켬」 한 번 더(`columns.b_on`)를 돌리지 않는다(같은 `verified` 가 비어 있어 비교할 것이 없다 — `b_on` = `null`).
  7. 이 세 상태의 프롬프트 문구(무엇을 말해야 하나의 규칙 문장)는 **답 프롬프트 초안에 넣고 e2e 보고 때 사용자가 확인한다**(C-1).
- **O-9 의 확인 지점이 SPEC 과 다르다(코디 결정 — §11 C-1).** SPEC-002 는 답 문구의 사용자 확인을 「답 프롬프트 WP **앞**」 으로 세 곳에 적었다(§5 끝 불릿 · §11 상태 뜻 표 「뒤 단계에서 사용자 확인」 행 · O-9 행). 이 계획은 **뒤**(e2e 보고 때)로 옮긴다 — 근거 = `_RESUME.md` §2 11-16 「진행 순서(코디 · WORK-002 §11)」 행(C-1). 그래서:
  1. 프롬프트 파일 초안(공통 + 열별 + 채점 + Jev instructions)을 이 WP · WP-7 에서 쓴다.
  2. 코디의 e2e 보고는 **「SPEC-002 O-9 의 확인 지점을 구현 뒤로 옮겼다 · 프롬프트 파일 n 개를 함께 본다」 를 글자로 밝히고** 프롬프트 파일을 함께 보인다.
  3. 사용자가 확인하면 코디가 `uv run python -m clinic_chat.prompts --confirm --by <확인한 사람>` 으로 `data/eval-set/prompts-confirmed.json` 에 그때의 파일별 sha256 을 적는다(§2-4 · 로컬).
  4. **결과의 「프롬프트 미확정」 표시 자리**: 줄 머리의 `prompts{…}` sha256(SPEC-002 §7-1 그대로 — 줄에 칸을 더하지 않는다)을 확인 기록과 견줘, **하나라도 다르거나 기록이 없으면** ① `runner` · `batch` 의 터미널 끝 요약 줄 ② 보고서 머리(프롬프트 sha 곁 — WP-7 7-g) ③ `batch --check` 에 **「프롬프트 미확정(사용자 확인 전)」** 을 찍는다. 프롬프트 파일을 고치면 sha 가 달라져 다시 미확정이 된다.
  5. 다음 SPEC 고침(0.4.2) 때 O-9 의 문구를 이 순서에 맞춘다(§13).
- `prompts/jev/*.md` 는 **영어 instructions**(D10) — `candidates[i]` 로 대상을 가리키고 SPEC-002 §3-3 표의 「instructions 가 가리키는 것」 을 옮긴다. state 는 한국어 이름 + 코드.

**완료 조건**

1. 모의 Jev · 모의 허브로 위 표의 「꼭 시험으로 잡을 것」 이 전부 시험으로 선다. 특히: **어떤 Noul 값을 줘도 폭에서 읽은 `gid` 가 `verified_gids` 에서 빠지지 않는다**(속성 기반 시험 — 무작위 noul) · `answer_ready` 가 1.0 이어도 폭 미완 · required 미충족 · 검사 실패면 「근거 충족」 이 아니다.
2. 종료 상태 여섯이 각각 모의 시나리오 하나 이상으로 난다.
3. Jev 가 낸 문자열이 노드 id · 범위 이름 · 입구 이름으로 쓰이는 코드 경로가 없다 — Jev 응답에서 읽는 것은 `choice`(앱이 준 옵션 키와 대조) · `confidence` · `probabilities` · `noul` 뿐이다(옵션에 없는 `choice` 는 오류).
4. 한 질문의 trace 가 SPEC-002 §7-3 B 표의 필드를 전부 갖는다(WP-5 와 함께 확인).
5. 실물(허브 WP-3 뒤 · E1 · E4 통과 뒤): 세트 문항 하나(37 중 하나)를 B 로 돌려 `end_state` 와 **K1 그대로**(SPEC-002 §4)를 본다 — 폭 조회마다 `read == total`(**그 도구의 쪽 단위** — SPEC-001 §4-0 「`total` 단위」 표) · `complete` 참(`next_cursor: null` 까지) · 그 응답들에 든 `gid` 의 합집합 ⊂ `verified_gids`. **`verified_gids` 수와 `total` 합을 등식으로 견주지 않는다** — `total` 의 단위가 도구마다 다르고(`concern_candidates` 는 묶음 수 · 쪽 밖 목록은 `total` 밖) 조회끼리 같은 행이 겹친다. E5 의 B 몫.
6. 「범위 밖」 · 「입구 없음」 · 「실행 중단」 모의 시나리오마다: 단계 ⑤ 가 **불리고** · 그 프롬프트 문자열에 `verified` 행(`gid` 꼴)이 **하나도 없고** · `end_state` 가 실려 있다. 모의 CLI 가 오류를 내는 「실행 중단」 에서는 `answer` 가 빈 값이고 `error` 가 차 있다. 앱 코드(`clinic_chat/`)에 종료 상태별 한국어 답 문장 상수가 없다(검수 항목 — 문구는 `prompts/` 에만).

## 6. WP-4 — C 열(LLM + 허브 MCP 직접)

**목표**: LLM 이 허브 MCP 도구를 스스로 부르는 열.

**SPEC-002 대응**: §2-1(C 열) · §2-2 · §2-4 · §6-2(C = http 붙이기) · §7-3(C trace `gids[]`) · O-15(= (a) `health` 뺀 7).

**만들 파일**: `clinic_chat/columns/col_c.py` · `prompts/col_c.md` · `tests/test_col_c.py`.

**구현 메모**

- `--mcp-config` = http(`HUB_GOLD_MCP_URL`) · `--allowedTools` 로 **도구 7**(`health` 제외 — CLI 의 허용 목록을 서버 단위가 아니라 도구 이름 7 개로 준다). 도구 설명은 허브가 낸 것 그대로 — 앱이 C 에만 힌트를 더하지 않는다.
- trace 의 `gids[]` = 그 응답에 **든 행**의 `gid`(SPEC-002 §7-3 C 행): `rows[]` · `groups[].rows[]` 안쪽 · 쪽 밖 목록(`modality_only[]` · `unreached[]` · `same_day_packages[]`) · 그 밖에 `gid` 칸을 가진 줄(`candidates[]` · `holders[]`) — 응답 JSON 을 재귀로 훑어 **`gid` 라는 이름의 칸만** 모으는 한 함수(B 의 `verified` 와 같은 함수).
- **`neighbors` 엣지의 `gold_id` 는 `gids[]` 에 넣지 않는다.** 엣지는 속성 행을 가리키기만 하고 그 행의 칸 값을 주지 않는다(SPEC-001 §4-3) — 「읽은 `gid`」 로 세면 C 가 `neighbors` 만 부르고도 D7(폭 누락)이 줄고 D2(읽지 않은 자리 인용)가 풀려 B ↔ C 비교가 C 쪽으로 기운다. 그 값은 따로 **`edge_gold_ids[]`** 에 기록만 한다(D2 · D7 의 재료가 아니다 · 이 문서가 더한 기록 칸 — O-11).
- MCP 결과가 CLI 쪽 한도로 잘리면 그 호출의 `gids[]` 가 준다 — 잘림 여부(`output_bytes` · CLI 가 낸 잘림 표지)를 trace 에 남긴다.

**완료 조건**: 모의 CLI 로 인자(http · 도구 7 · 격리 옵션 A · B 와 같음) · trace 꼴이 맞다 · **모의 `neighbors` 응답 하나에서 `gids[]` 에 엣지의 `gold_id` 가 없고 `edge_gold_ids[]` 에만 있다** · 실물은 E5 의 C 몫(도구 호출 1 이상 · 행을 낸 도구를 불렀으면 `gids[]` 가 비지 않음).

## 7. WP-5 — 기록(runs.jsonl · trace)

**목표**: 한 질문 한 줄.

**SPEC-002 대응**: §7 전부(§7-1 줄 머리 · §7-2 열마다 · §7-3 열별 trace) · §6-1(실제 모델 id · batch 안 고정) · §2-2 · O-11(`columns.b_on` 이름).

**만들 파일**: `clinic_chat/runs.py` · `timing.py` · `runner.py` · `prompts.py` · `tests/test_runs.py` · `tests/test_runner.py`.

**옛 틀에서**: `APP-OLD clinic_chat/runs.py:1-30`(줄 저장 · 고치지 않음 · 커밋 읽기) · `timing.py:12-25`(`Clock`) · `cli.py:92-309` 의 이벤트 → 단계 시간 · 토큰(WP-1 에서 옮긴 것).

**구현 메모**

- `runner.py`: 질문 하나 × 고른 열. **세 열을 동시에 돌리지 않고 차례로** · 순서는 질문마다 섞고 seed 를 `order` 에 남긴다. 한 열이 오류여도 나머지를 돌린다.
- 줄 머리: `run_id` · `asked_at` · `batch_id` · `set_id`(자유 질문 = `null`) · `question` · `build.gold_hash` · `commits{app, hub}`(허브 커밋은 `HUB_COMMIT` env 또는 허브 워크트리 경로 env 로 — 못 읽으면 `null`) · `models{answer, judge, jev}`(**실제** id) · `raw{…}` · `answer_key{sha256, confirmed}` · `prompts{common, a, b, c, judge}` sha256 · `settings`(문턱 넷 · 묶음 크기 · 타임아웃 · 걸음 상한 · 입력 한도 · `answer_reasoning` · effort) · `order`.
- 쓴 줄은 고치지 않는다. 채점은 `runs/quality.jsonl` 에 `run_id` 로 덧붙인다.
- `prompts.py`: 프롬프트 파일 읽기 · sha256 · **확인 기록 대조**(`prompts-confirmed.json` 과 같으면 확정 · 다르거나 없으면 「프롬프트 미확정」 — §5 「프롬프트 파일」 C-1 의 4) · `--confirm` 진입점. 줄 머리에는 SPEC-002 §7-1 의 sha256 만 남긴다(칸을 더하지 않는다).

**완료 조건**

1. 모의 세 열로 한 줄을 쓰면 SPEC-002 §7-1 · §7-2 · §7-3 의 필드가 **전부** 있다(필드 목록을 시험 상수로 두고 대조 — **B trace 는 §7-3 B 표의 필드 목록 그대로**(수를 박지 않는다 — 표의 행을 그대로 옮긴다) · A · C `tool_calls[]` 꼴(C 는 + `edge_gold_ids[]` — WP-4) · `b_on` 의 칸은 §7-2 그대로).
2. `end_state` 는 B 만 값이 있고 A · C 는 `null` 이다.
3. 같은 batch 안에서 실제 model id 가 바뀐 줄이 있으면 batch 요약에 표시된다.
4. 기록 파일이 `git status` 에 안 보인다(`runs/` · `*.jsonl` 무시 확인).
5. 확인 기록이 없을 때 · sha 가 하나 다를 때 `runner` 의 끝 요약 줄에 「프롬프트 미확정(사용자 확인 전)」 이 찍히고, `--confirm` 뒤 같은 프롬프트로 돌리면 안 찍힌다(모의 시험).

## 8. WP-6 — 전체 답 키 스크립트 + 세트 파일

**목표**: 문항마다 허브 도구 길의 **전체 행**을 결정론으로 뽑아 답 키를 만들고, 사용자가 확인할 대조 요약 한 장을 낸다. 시험 세트 69 문항 파일을 세운다.

**SPEC-002 대응**: §8-1(기준 · 표본 ≠ 키) · §9-1 ~ §9-3b(묶음 · 문항 수 · 기대) · §9-4(세트 파일 칸 · 묶음별 답 키) · §9-5 전부(입력 · 출력 칸 · 행 값 읽기 · 키 코드 칸 표 · 분모 규칙 · 기대 종료 상태 계산 · 사용자 확인 절차 1 ~ 5) · §3-1 BR3 · O-10 · O-11 · O-19.

**만들 파일**: `clinic_chat/evalset/{__init__,loader,key_calls,answer_key,pick}.py` · `tests/test_answer_key.py` · (로컬 · gitignore) `data/eval-set/**`.

**하위 묶음**

| # | 무엇 | 메모 |
|---|---|---|
| 6-a | 세트 로더 | `set.jsonl` 을 읽고 37 문항의 `question` 은 `QUESTIONS_CSV` 에서 `id` 로 채운다. 칸 검증(69 줄 · `id` 유일 · 묶음별 수 = SPEC §9 표) |
| 6-b | 37 문항 호출 명세 | `$SM/gold/gold-build.py` 의 `QUESTIONS`(`:939` 부터)가 문항마다 가진 **구조 값**(입구 · 상대 끝 · 사건 · 갈래 · 패키지 갈래 · 상품 이름 · `need_time`)을 읽어 `entries[]` 로 옮긴다 — 이름은 허브 `resolve` 로 코드로 바꾸고(범위 규칙으로 겹침을 가름) **`walk/calls.py` 의 같은 함수**로 `calls[]` 를 편다. `need_time` → `asked_fields = [g_adverse.onset_text, g_adverse.duration_text]`(Q12 하나). BR2 밖의 좁힘(같은 시술 쌍만 보기 등)은 옮기지 않는다. **질문 문장을 해석하지 않는다.** 명세 파일은 로컬(`data/eval-set/calls/`) — 그 목록을 한 번 읽어 옮기는 변환기(`key_calls.py`). **`gold-build.py` 를 실행하지 않는다 — `import` · `exec` · `runpy` · 자식 프로세스 실행 전부 금지.** 그 파일은 돌리면 gold CSV 를 다시 쓴다(gold 해시가 바뀌면 키 전부 무효 — SPEC-001 §2-3). 파일을 글로 읽어 **구문 트리(`ast`)에서 `QUESTIONS` 목록의 리터럴만** 꺼낸다(`ast.literal_eval` 로 값이 되는 것만 · 안 되면 멈추고 보고). 그 목록에는 **질문 문장 칸도 있다 — 명세 파일에 옮기지 않는다**(문항은 `id` 로만 · 구조 값만). 변환 앞뒤로 `$SM/gold` 의 해시가 같은지 확인한다 |
| 6-c | 추가 32 문항(19 + 4 + 4 + 5) | **문항 고르기 재료를 결정론으로 낸다**(`pick.py` — LLM 없음): 묶음마다 gold 에서 조건에 맞는 코드 후보 목록(예: 「보완만 있고 `same_day` 빈칸인 쌍」 · 「같은 쌍 값 엇갈림」 · 「Q10 · Q33 말고 다른 LCK 코드」 · 「역방향 큰 후보 부작용」 · 「`norm` 이 두 표에 겹치는 입구」 · 속성 4표의 행 많은 코드). 워커가 그 후보로 **질문 문장 초안**을 로컬 세트 파일에 쓰고(`status: draft`) `expected_entries[]` · `expected_end_state` · `expected_scope_gap` 을 적는다 → **사용자 확정**. 이름 없는 질문 묶음은 스크립트가 `resolve` 후보가 실제로 0 인지 허브에 물어 대조 요약에 적는다 |
| 6-d | 답 키 스크립트 | 문항마다 `calls[]` 를 허브 REST 로 **끝까지** 넘겨 키 파일을 쓴다 — 칸은 SPEC-002 §9-5 「출력」 표 그대로(`rows[]{gold_table, gid, bucket, layer_role, hier_match, codes[], side_codes[]}` · `codes[]` · `unnamed_codes[]` · `side_codes[]` · `must_rows[]` · `ledger_check[]` · `expected_end_state` · `expected_end_state_by` · `sample_check` · `confirmed` · `build` · `script_sha256` · `calls_sha256`). 키 코드 칸 · 곁 칸은 §9-5 표를 **상수 표**로 옮긴다. **행의 값 칸은 키 파일에 복사하지 않는다.** `g_scope` · `g_entry` 행은 `rows[]` 에 없다. 입구 있는 코드 판정(`codes[]` ↔ `unnamed_codes[]`)은 허브 `resolve` 목록 꼴로 받은 입구 집합으로 |
| 6-e | 기대 종료 상태 계산 | §9-5 순서 1 ~ 5 그대로 · 「상태 안 맞음」 은 값을 지어내지 않고 요약에 올림 |
| 6-f | 행 값 읽기 | 키의 `calls[]` 를 같은 build 로 다시 불러 `gid` 로 고르는 함수 — WP-7 의 D4 · D5 · ② 채점 입력이 쓴다. build 가 다르면 키 무효 |
| 6-g | 대조 요약 | `key-summary.md` — 문항마다: 전체 행 수 · `bucket` 별 수 · 키 코드 수 · `unnamed_codes[]` 수 · `sample_check`(표본 ⊂ 키) · `expected_end_state`(+ `_by`) · `status` 와 맞나 · `ledger_check[]` · BR2 로 키가 표본의 길보다 넓어진 문항 표시 · 이름 없는 질문 묶음의 `resolve` 후보 수. **「걸린 문항」 을 맨 위에 모은다**(§9-5 확인 절차 2 의 다섯 꼴) |

**실행 명령(제안)**

```bash
# 허브가 18105 에 떠 있어야 한다(WORK-001 §2-5)
uv run python -m clinic_chat.evalset.key_calls --from-gold-build "$SM/gold/gold-build.py"   # 37 문항 명세
uv run python -m clinic_chat.evalset.pick                                                   # 추가 묶음 후보 목록(로컬)
uv run python -m clinic_chat.evalset.answer_key --all                                       # 키 + 대조 요약
uv run python -m clinic_chat.evalset.answer_key --confirm Q01,Q02,… --by <확인한 사람>        # 사용자 확인 기록
```

**사용자 확인 절차(SPEC-002 §9-5 그대로 · 결과는 gitignore 로컬)**

1. 워커가 스크립트를 돌려 `data/eval-set/key-summary.md` 를 낸다. 코디가 그 파일 자리와 **걸린 문항 수**만 보고에 적는다(요약의 행 수 · 코드 수는 셈이라 적어도 되지만 질문 문장 · 답 본문은 보고에 적지 않는다).
2. 사용자가 요약을 열어 걸린 문항만 본다. 추가 32 문항은 **질문 문장 · 기대 입구 · 기대 종료 상태**도 이때 함께 확정한다. O-10(문항 ↔ LCK 잇기 = (a)) · O-19(키 코드 칸 / 곁 칸 = 표 그대로) · O-22 ①(층 ↔ `reach`)도 이때 보인다.
3. 고칠 것이 있으면 **호출 명세 · 세트 파일을 고쳐 다시 뽑는다** — 키 파일을 손으로 고치지 않는다.
4. 사용자가 확인하면 `--confirm` 으로 `confirmed{by, at}` 를 적는다. **확인 전 키로는 채점하지 않는다**(WP-7 이 `confirmed` 없는 키를 거부한다 — **풀어 주는 플래그 · env · 설정이 없다** · SPEC-002 §9-5 확인 절차 4 · `_RESUME.md` §2 11-16 「WORK 검수 뒤(코디)」 F-1). 채점 배관의 실물 확인은 세트 키가 아니라 **합성 키**로 한다(§9 「E6 — 합성 키 배관 확인」).
5. `gold_hash` · `aux_hash` · 스크립트 · 명세 중 하나라도 바뀌면 키는 무효다.

**완료 조건**

1. 모의 허브로: 같은 명세 · 같은 build → 바이트까지 같은 키 파일 · 키 파일에 값 칸 없음(칸 이름 목록 대조) · `g_scope` · `g_entry` 행 없음 · 기대 종료 상태 다섯 길(`set` · `(가)` · `(나)` · `(다)` · `status`)이 각각 난다.
2. **실물(데이터 env · 허브 18105)**: 37 문항 키가 나오고 **`sample_check` — `gold_pointers` 표본이 전체 키에 전부 든다**(`missing[]` 이 빈 문항 수 / 37 을 보고 · 안 드는 문항은 id · 안 든 `gid` 수를 보고 — 명세 구멍이거나 SPEC 의 도구 길 구멍이다. 문항별 예외로 메우지 않는다).
3. 실물: Q10 = `(가)` · Q33 = `(나)` · Q12 = `(다)` · 나머지 34 = `status`(근거 충족) — 다르면 「상태 안 맞음」 으로 요약에.
4. 세트 파일 69 줄(37 + 19 + 4 + 4 + 5) · 추가 32 는 `draft` 로 서 있다. **사용자 확정 전임을 보고에 적는다.** `draft` 문항은 사용자 확정 전에 Jev · LLM 으로 보내지 않는다(WP-8 batch 가 건너뛴다).
5. `git status --porcelain` 에 `data/` 아래 파일이 안 보인다.
6. LLM · Jev 호출 0(이 WP 의 코드가 `llm/` · `jev_client` 를 import 하지 않는다).
7. `key_calls.py` 에 `import` · `exec` · `runpy` · `subprocess` 로 `gold-build.py` 를 돌리는 길이 없고(`rg` 로 확인해 보고), 37 문항 명세를 뽑은 앞뒤로 gold 해시가 같다. 명세 파일에 질문 문장 칸이 없다(칸 이름 목록 대조).

## 9. WP-7 — 채점 두 층 + 보고서

**목표**: ① 결정론 검사 D1 ~ D9 · ② LLM 채점(Opus · 가리기) · 「원장 오류 따라감」 · 점수 두 벌 · 보고서.

**SPEC-002 대응**: §8-1 ~ §8-6 전부 · §10 전부(열별 표 · 범위별 · 상태별 · B 전용 · 끔/켬 비교 · 「해당 없음」 · 합격선 없음) · §4 「답 뒤」 · §5(세 열 모두 ② 가 종료 상태를 읽음) · O-7 · O-8 · O-10 · O-17 · O-22.

**만들 파일**: `clinic_chat/quality/{gold_codes,checks,judge,ledger_diff,grade}.py` · `clinic_chat/report.py` · `prompts/judge.md` · `tests/test_checks.py` · `tests/test_judge.py` · `tests/test_report.py`.

**옛 틀에서**: `APP-OLD clinic_chat/quality/judge.py:39-41`(가린 입력 — 질문 + 답만) · `:56-60`(실패 근거 검사) · `cli.py:86-87`(`--json-schema` 구조화 출력).

**하위 묶음**

| # | 무엇 | SPEC 절 | 꼭 잡을 것 |
|---|---|---|---|
| 7-a | gold 코드 집합 | §8-2 「gold 코드 집합」 | 채점 단계에서 로컬 gold CSV 를 직접 읽어 (i) `g_entry` (ii) `g_scope` 두 쪽 (iii) 속성 표의 키 코드 칸 · 곁 칸의 합집합 · 허브 `gold_hash` 와 대조(다르면 채점 중단) |
| 7-b | D1 ~ D9 | §8-2 표 · 아래 불릿 | D1(`gid` 실재 = 허브 `evidence` · 원장 포인터 실재 = 원장 파일) · D2(A: 인용 ⊂ `paths[]` 자신 또는 하위 — `truncated` 호출은 자신만 / B: ⊂ `verified_gids` / C: ⊂ `gids[]`) · D3 ① 빠진 코드 비율(세 열) · ② 지어낸 코드(B · C · A 는 「해당 없음」) · `extra_codes` 는 기록만 · D4 숫자 + 단위 · D5(G1 `must_rows[]` · G5 · G6) · D6(B 전용) · D7(B · C · A 「해당 없음」 · `missed_codes` 는 「읽은 행의 키 코드 칸 어디에도 없는 것」) · D8 `unasked{safety, offer, effect}` 기록만 · D9 `case_names_used[]` · **「고민 하나에 무엇을 하나」 꼴은 `groups` 후보의 빠진 수를 따로 · 케이스 후보는 `procedure:procedure_code` 로 센다** |
| 7-c | 인용 뽑기 · 가리기 | §8-3 · O-8 | 답에서 `gid` · 원장 포인터를 뽑는 정규식 → 채점 입력에서는 중립 표지로 바꿈 |
| 7-d | ② LLM 채점 | §8-3 표 · 항목 5 | 입력 = 질문 + 답(가린 인용) + 전체 답 키(행 값 읽기) + `expected_end_state` + `ledger_check[]` + (걸린 문항) LCK 글 칸 + `questions.csv` `answer`(「잘린 표본 요약」 이라고 밝혀) · **열 이름 · 도구 흔적 · 속도 · 다른 열 답 · B 의 `end_state` 없음** · 순서 섞기 + seed · 열마다 따로 절대 채점 · 항목별 통과 / 실패 / 해당 없음 · 실패 근거(`gid` + 칸) 없으면 무효 · `graded_end_state` · `ends_with_question` 기록 |
| 7-e | 「원장 오류 따라감」 · 두 벌 | §8-4 · §8-5 | `followed_ledger_error` 분류 · LCK 글 칸은 `LEDGER_CHECK_PATH` 에서 채점 단계만 · 문항 ↔ LCK = O-10 (a)(코드 맞춤 — 세트 파일 `ledger_diff`) · 점수 = 전체 / LCK 안 걸린 문항만 |
| 7-f | §8-6 모범 답 기준 | §8-6 M1 ~ M7 · 층 ↔ `reach` 표 | ① 쪽 재료(M1 `groups` 빠진 수 · M2 기대 층 · M3 기전 이름 집합 · M4 D8 · M6 D9 · M7) · ② 쪽 항목 사상 |
| 7-g | 보고서 | §10 | 머리(`gold_hash` · 커밋 둘 · 실제 model id 셋 · 문턱 · 프롬프트 sha + **「프롬프트 미확정(사용자 확인 전)」 여부**(§5 C-1 의 4) · `answer_reasoning` · 답 키 `confirmed` 수 — 미확인 키로 채점한 줄은 있을 수 없다) · 열별 표 × 두 벌 · 범위별 · 상태별 · B 전용 · 끔/켬 비교 · **「해당 없음」 칸을 0 으로 적지 않는다** · 합격선 없음 |

**r5 Z 를 여기서 한 줄씩**

- **Z-2**(7-d): ② 「불확실 표시」 가 묻는 목록에 **「(낱말이 두 개념으로 읽힐 수 있는 문항) 어느 개념으로 읽었는지 밝혔나 — 하나로 읽고 그것을 밝혔으면 통과 · 둘 다로 읽고 그렇게 밝혔어도 통과」** 를 더한다. 세 열에 같은 뜻이 되게 한 문구다 — RG6 은 실행마다 Jev 확률로 갈리고(B 가 확실하게 하나로 읽으면 「그 개념으로도 읽었음」 을 물을 수 없다) A · C 에는 RG6 이 없다. 걸리는 조건은 **세트 파일의 고정 표지 `two_readings`**(§2-4 — 따로 둔 칸 · 사용자 확정)뿐이다 — `expected_entries[]`(이름 없는 질문 묶음 · 오타의 기대 입구 칸 — SPEC-002 §9-4)를 겸해 쓰지 않는다. 표지가 없는 문항에서 이 구절은 「해당 없음」 이다. B 의 `read_as` 표지 · `via = RG6` 를 채점 입력에 주지 않는다(주면 B 가 드러난다 — §8-3 가리기). **RG6 을 실제로 탄 수는 채점이 아니라 Z-3 의 셈으로만 본다.**
- **Z-3**(7-g): 보고서 열별 표의 D8 `unasked` 줄 곁에 **그 문항 중 범위를 RG3 으로 둘 읽은 수 · `via = RG6` 로 더한 수**를 함께 낸다(B 칸에만 · `range_choice` trace 에서). 그 문항의 `unasked.safety[]` 는 B 의 판단(Jev 불확실)으로 폭이 넓어진 결과라 갈라 읽어야 한다 — 재는 것은 그대로다(빼지 않는다).

**E6 — 합성 키 배관 확인**(실물 Opus 1회 · `_RESUME.md` §2 11-16 「WORK 검수 뒤(코디)」 F-1)

- `quality.grade --plumbing` 은 **세트와 떨어진 별도 진입점**이다. 입력을 스스로 만든다 — 시험 fixture 와 같은 생성기로 **가짜 코드 · 가짜 이름**의 질문 한 줄 · 답 한 줄 · 답 키 하나(`synthetic: true`)를 임시 폴더에 쓴다. **`EVAL_SET_DIR` · `runs/runs.jsonl` · `QUESTIONS_CSV` · gold CSV 를 읽지 않는다**(세트 문항 · 세트 키 · 실제 답을 받는 인자가 없다).
- 그 합성 입력으로 ① 결정론 검사 → ② LLM 채점(실물 Opus · 구조화 출력) → 보고서 생성까지 한 번 잇는다. 결과는 `runs/plumbing/` 에만 쓰고 `runs/quality.jsonl` · `runs/reports/` 에 섞지 않는다.
- 결과 파일 머리와 터미널 출력에 **「합성 키 — 배관 확인 · 채점 수치 아님」** 을 찍는다. 이 결과의 통과 / 실패 값은 **채점 수치로 쓰지 않는다**(보고 · 보고서 · 회고 어디에도 점수로 옮기지 않는다 — 본 것은 「구조화 출력이 항목 5 로 왔나 · 실패 근거 칸이 있나」 뿐).
- 반대쪽도 막는다: 일반 채점(`quality.grade --batch …`)은 `synthetic: true` 인 키 · `confirmed` 없는 키를 **둘 다 거부**한다. `--plumbing` 은 세트 키를 못 읽으므로 미확인 세트 키가 채점되는 길이 어느 쪽에도 없다.

**완료 조건**

1. 합성 답 · 합성 키로 D1 ~ D9 가 각각 「걸림 / 안 걸림」 두 경우 이상 시험으로 선다. 세 열에 **같은 검사기 함수**가 돈다(열 이름으로 갈라지는 곳은 D2 의 재료 · D3 ② · D6 · D7 뿐).
2. 채점 입력 문자열에 열 이름 · `gid` 꼴 · 원장 포인터 꼴 · 도구 이름 · `end_state` 가 **없다**(문자열 대조 시험).
3. 미확인 키 · build 가 다른 키 · `synthetic: true` 키로는 일반 채점이 거부된다. **미확인 키를 풀어 주는 플래그 · env · 설정이 코드에 없다**(`rg -n "unconfirmed" clinic_chat` 로 거부 문구 밖의 길이 없음을 보고).
4. 보고서가 합성 기록 6 줄로 생성되고 「해당 없음」 칸이 0 이 아니다.
5. **E6 실물 통과 — 합성 키**(`--plumbing` · Opus 1회 · 구조화 출력 항목 5 · 실패 근거 칸 · 「합성 키 — 배관 확인 · 채점 수치 아님」 표시 · 결과가 `runs/plumbing/` 에만 있음). **세트 문항의 실제 채점은 이 WP 의 완료 조건이 아니다** — 사용자 키 확인 뒤 코디가 돌린다.
6. `--plumbing` 이 `EVAL_SET_DIR` 없이(그 env 를 지우고) 돈다 — 세트 파일 · 세트 키를 읽지 않는다는 것을 모의 시험으로 본다.

## 10. WP-8 — batch 실행기 + 사용자 e2e 실행 안내

**목표**: 세트를 한 바퀴 돌리는 실행기와, 사용자가 직접 돌려 볼 명령 · 결과 자리 안내.

**SPEC-002 대응**: §10(한 batch = 보고서 하나 · batch 로만) · §7-1 `order`(차례 · 순서 섞기) · §6-1(batch 안 고정 · 끔/켬 한 번 더) · §2-2 · O-13 · O-14.

**만들 파일**: `clinic_chat/batch.py` · `README.md`(「실행 안내」 절) · `tests/test_batch.py`.

### 10-1. batch 실행기

- 세트 파일 → 문항마다 `runner` → `runs.jsonl`. 열 고르기(`--columns`) · 문항 고르기(`--ids` · `--bundle` · `--range`) · 이어 돌리기(`--resume <batch_id>` — 이미 쓴 `set_id` 는 건너뜀) · 문항 사이 쉼(구독 한도).
- 시작 때 한 번 확인하고 **하나라도 안 되면 돌리지 않고 무엇이 빠졌는지 말한다**: 허브 `health`(+ `gold_hash`) · Jev 키 「있음」 · CLI 구독 · `RAW_DIR` · 세트 파일 · 답 키(`confirmed` 수).
- **`status: draft` 문항은 돌리지 않는다**(사용자 확정 전 질문 문장을 Jev · LLM 으로 보내지 않는다 — 건너뛴 수를 시작 때 말한다). 37 문항은 `draft` 가 아니다.
- 시작 확인과 끝 요약 줄에 「프롬프트 미확정(사용자 확인 전)」 여부를 찍는다(§5 C-1 의 4 — 돌리는 것을 막지는 않는다).
- 「끔/켬」: `--b-on` 을 주면 B 의 단계 ⑤ 를 같은 `verified` 로 한 번 더(1회차 기본 = 켬).

### 10-2. 사용자 e2e 실행 안내(README 에 같은 내용)

전제: ① 허브가 18105 에 떠 있다(WORK-001 §2-5) ② 앱 `.env` 에 §2-5 의 값이 있다(키 포함) ③ `claude` CLI 가 구독으로 로그인돼 있다 ④ `uv sync`.

| 하고 싶은 것 | 명령(`APP-WT` 에서) | 결과를 보는 곳 |
|---|---|---|
| 연결 확인 | `uv run python -m clinic_chat.batch --check` | 터미널 — 허브 · Jev · CLI · 원장 · 세트 · 답 키의 「됨 / 안 됨」 |
| **한 질문 · 세 열** | `uv run python -m clinic_chat.runner --question "<질문>"` | 터미널에 열마다 답 · 종료 · ms · 호출 수 / `runs/runs.jsonl` 마지막 줄 |
| **한 질문 · 한 열** | `uv run python -m clinic_chat.runner --question "<질문>" --columns b` | 같음(B 는 trace 요약 — 읽은 범위 · 폭 조회 수 · 깊이 결정 분포 · gate) |
| 세트 문항 하나 | `uv run python -m clinic_chat.runner --set-id Q08` | 같음 + 기대 종료 상태 |
| **전체 세트** | `uv run python -m clinic_chat.batch --label <라벨>` | 진행 줄(문항 · 열 · ms) / 끝에 `batch_id` |
| 일부만 | `… batch --ids Q01,Q10,Q33` · `--bundle <묶음>` · `--columns a,c` | 같음 |
| 채점(**답 키를 확인한 뒤에만 돈다** — 미확인 키 문항은 거부하고 그 수를 말한다) | `uv run python -m clinic_chat.quality.grade --batch <batch_id>` | `runs/quality.jsonl` |
| 채점 배관만 확인(합성 키 · 점수 아님) | `uv run python -m clinic_chat.quality.grade --plumbing` | `runs/plumbing/` — 머리에 「합성 키 — 배관 확인 · 채점 수치 아님」 |
| 답 키 확인 기록 | `uv run python -m clinic_chat.evalset.answer_key --confirm <id 목록> --by <확인한 사람>` | `data/eval-set/answer-key/<id>.json` 의 `confirmed` |
| 프롬프트 확인 기록 | `uv run python -m clinic_chat.prompts --confirm --by <확인한 사람>` | `data/eval-set/prompts-confirmed.json` — 그 뒤 「프롬프트 미확정」 이 사라진다 |
| 보고서 | `uv run python -m clinic_chat.report --batch <batch_id>` | `runs/reports/<batch_id>.md` |
| 한 줄 자세히 | `uv run python -m clinic_chat.runs --show <run_id> [--column b --trace]` | 터미널 — 답 · 인용 · trace(`range_choice` · `breadth[]` · `steps[]` · `gates[]`) |

- 자유 질문(`--question`)은 `set_id = null` 이라 **채점되지 않는다**(답 키가 없다) — 기록 · 속도에만 남는다.
- 질문에 환자 정보를 넣지 않는다(질문 · 노드 이름이 Jev · LLM 으로 나간다).
- 전체 세트는 문항 69 × (A + B + B 켬 + C) 의 CLI 호출이라 오래 걸린다 — 처음에는 `--ids` 로 몇 문항만 돌려 본다.

**완료 조건**

1. 모의 세 열로 batch 가 6 문항을 돌고 `--resume` 이 이미 쓴 문항을 건너뛴다 · 순서 seed 가 줄마다 다르다 · 열을 동시에 돌리지 않는다.
2. `--check` 가 빠진 것(허브 없음 · 키 없음 · 답 키 미확인 · 프롬프트 미확정 · `draft` 문항 수)을 각각 가려 말한다.
3. **E5 실물 통과** — 세트 문항 하나(37 중 하나)를 세 열(+ `b_on`)로 돌려 `runs.jsonl` 한 줄이 SPEC-002 §7 꼴로 선다. **그 줄은 여기서 채점하지 않는다**(답 키가 사용자 확인 전이다). 「기록 → 채점 → 보고서」 를 잇는 배관은 **합성 키**(가짜 코드 · 가짜 이름으로 만든 키 — E6 `--plumbing`)로 한 번 이어 보고, 그 결과에 「합성 키 — 배관 확인 · 채점 수치 아님」 이 찍혀 있음을 확인한다 — **채점 수치로 쓰지 않는다.** 실제 채점 · 실제 보고서는 사용자가 답 키를 확인한 뒤다(§8 「사용자 확인 절차」 4 · §11).
4. 전체 `uv run ruff check .` · `uv run pytest -q` 통과(수치 보고).
5. `git status --porcelain` 이 §2-2 안의 파일뿐이고 `data/` · `runs/` · `.env` 가 안 보인다. `grep` 으로 레포에 질문 문장 · 키 · 내부 주소가 없음을 본다.

## 11. 순서 · 의존 · 병행

```
허브(WORK-001):  WP-1 ─▶ WP-2 ─▶ WP-3 ─▶ WP-4
                                    │(18105 에 실물 허브)
앱(WORK-002):    WP-1 ─▶ WP-2 ─▶ WP-5(틀) ─▶ WP-3 의 3-a(ranges.py · calls.py)   ← 여기까지 허브와 병행 가능
                                    │(E4 — 허브 WP-3 뒤)
                                    ├─▶ WP-6 ─▶ [사용자 키 확인] ─────────────┐
                                    └─▶ WP-3(3-b ~ 3-j) ─▶ WP-4 ─▶ WP-7 ─▶ WP-8 ─┴─▶ 실제 채점 · 보고서(코디)
```

- **WP-6 은 WP-3 의 3-a 뒤다.** 6-b 가 `walk/calls.py` 의 함수를 쓰는데(BR3 — B 와 답 키가 한 함수) 그 파일은 3-a 의 산출물이다. 그래서 **3-a 만 먼저 떼어 WP-6 앞에 둔다** — 3-a 는 고정 표와 순수 함수라 Jev · LLM · 허브 실물 없이 서고, 이렇게 하면 답 키의 사용자 확인을 일찍 걸 수 있다. 레포 안은 차례로 가므로 발주 순서 = WP-1 → WP-2 → WP-5(틀) → **WP-3 3-a** → WP-6 → WP-3 나머지 → WP-4 → WP-7 → WP-8.
- WP-7 · WP-8 의 완료는 사용자 키 확인을 기다리지 않는다(E6 = 합성 키 배관). 기다리는 것은 **실제 채점 · 실제 보고서**뿐이다.

**「허브 WP-2 계약이 서면 앱은 모의 허브로 병행 가능한가」 — 제안: 부분만.**

| 앱 WP | 허브 없이 시작 | 근거 |
|---|---|---|
| WP-1(클라이언트 · CLI) · WP-2(A 열) · WP-5(기록 틀) · **WP-3 의 3-a**(범위 표 · 폭 조회 목록) | **가능 — 허브 WP-1 과 동시에** | 허브 도구의 뜻에 기대지 않는다. 허브 클라이언트는 SPEC-001 §4 의 경로 · 입력 이름 · 응답 머리만 알면 되고 그 계약은 0.4.1 로 굳었다(E4 는 허브 WP-3 뒤 — WP-3 진입 조건). 3-a 는 SPEC-002 §3-2 표를 상수로 옮기는 것이라 허브가 필요 없다 |
| WP-3(B 걷기) · WP-4(C 열)의 **단위 시험** | 가능 — 모의 응답으로 | 걷기 로직(문턱 · 쪽 넘김 · 장부 · gate · 묶음 표)은 응답 **꼴**만 있으면 시험된다 |
| WP-6(답 키) · WP-3 · WP-4 의 **실물** · WP-7 의 D1 | **불가 — 허브 WP-3 뒤** | 답 키 = 허브 도구 길의 전체 행 그 자체다. 모의로는 뜻이 없다 |

- **모의 허브의 한계**: 도구 8 의 결정론 규칙(층 펼침 · 계층 자손 · 속성 항목 맞춤 · `ledger_check[]` 겹침)을 모의로 다시 지으면 허브를 두 번 짓는 셈이고, 어긋난 모의가 걷기 결함을 가린다(옛 틀의 `tests/fake_hub/gold.py` 가 528 줄이었다). 그래서 앱의 `tests/fake_hub.py` 는 **정해 둔 응답을 그대로 돌려주는 것**(쪽 넘김 · 오류 · 머리 꼴)까지만 한다 — 규칙을 계산하지 않는다. 응답 예는 SPEC-001 §4 의 필드 표로 손으로 적은 가짜 코드 · 가짜 이름이다.
- 허브 WP-3 이 끝나면 앱 쪽에서 **모의 응답 꼴 ↔ 실물 응답 꼴을 한 번 대조**한다(E4 에 포함 — 필드 이름 · `total` 단위 · 쪽 밖 목록 자리).
- 워크트리가 레포마다 하나라 **레포 안에서는 차례로**, 두 레포는 나란히 갈 수 있다.
- WP-6 의 사용자 키 확인은 WP-3 · WP-4 · WP-7 · WP-8 의 **구현과 완료**를 막지 않는다. 막는 것은 **세트 문항의 채점 실행**뿐이다(미확인 키로는 채점 안 함 — 풀어 주는 길 없음 · 배관 확인은 합성 키).

**코디가 정한 것(사용자 결정이 아니라 진행 순서 · 0.1.0 의 제안을 코디가 받음 — 근거 `_RESUME.md` §2 11-16 의 두 행)**

| # | 무엇 | 정한 값 | 근거 | SPEC 과의 사이 |
|---|---|---|---|---|
| C-1 | 답 프롬프트 문구(O-9) 사용자 확인을 구현 앞에 둘지 뒤에 둘지 | **뒤** — 초안으로 구현하고 e2e 보고 때 프롬프트 파일을 함께 보인다. 확인 전 결과에는 「프롬프트 미확정(사용자 확인 전)」 이 찍힌다(자리 = §5 「프롬프트 파일」 C-1 의 4) | `_RESUME.md` §2 11-16 「진행 순서(코디 · WORK-002 §11)」 행 — 사용자 지시 「코드 작업까지 해서 보고 · e2e」 에서 코디가 끌어낸 순서다(사용자의 직접 문장은 아니다) | **SPEC-002 O-9 의 글자와 다르다** — SPEC 은 「답 프롬프트 WP 앞」(§5 끝 불릿 · §11 상태 뜻 표 · O-9 행). e2e 보고에 이 차이를 글자로 밝힌다 · SPEC 0.4.2 때 O-9 문구 맞춤 |
| C-2 | 추가 32 문항의 질문 문장을 누가 쓰나 | 워커가 `pick.py` 후보로 초안(로컬 · `draft`) → 사용자 확정. `draft` 문항은 확정 전 Jev · LLM 으로 보내지 않는다 | 같은 행 | 안 부딪힘(SPEC-002 §9 는 「문항을 쓰는 것은 세트 파일 작업 · 사용자 확정」 까지) |
| C-3 | 실물 확인(E1 ~ E6)을 워커가 하나 코디가 하나 | 워커가 명령을 돌리고 결과 셈만 보고 — 키 · 구독이 워커 세션에서 안 잡히면 「못 돌림」 으로 넘기고 코디가 돌린다. 「못 돌림」 으로 넘긴 E 가 걸린 WP 는 완료로 적지 않는다 | 같은 행 · `_RESUME.md` §2 「코디 검증(실물 호출 포함)」 | 안 부딪힘 |
| C-4 | 「범위 밖」 · 「입구 없음」 · 「실행 중단」 에서 단계 ⑤ 를 부르나 | **부른다** — `end_state` + 빈 `verified` 를 넘겨 그 상태를 말하게 한다 · 세 열 같은 조건 · 앱이 문구를 지어 넣지 않는다 · 문구는 답 프롬프트 초안에 두고 e2e 보고 때 사용자 확인(C-1). 조건 일곱 줄 = §5 「단계 ⑤ 를 부르는 범위」 | `_RESUME.md` §2 11-16 「WORK 검수 뒤(코디)」 행 W2-1 · 「화면 문구 지어 넣지 않기」 | SPEC-002 에 없는 동작이다(§4 「단계 ④ 를 통과해야 단계 ⑤ 로 간다」 · §5 표는 「무엇을 말해야 하나」 까지). 검사에 실패한 행은 한 행도 프롬프트에 안 가므로 §4 의 뜻은 지킨다 · SPEC 0.4.2 때 §4 · §5 에 되적기 |
| C-5 | 미확인 답 키로 채점하는 길 | **없다** — `--allow-unconfirmed` 를 뺐다. E6 · WP-8 완료 조건 3 의 배관 확인은 합성 키(가짜 코드 · 가짜 이름 · 「채점 수치 아님」 표시)로만 · 실제 채점은 사용자가 확인한 키로만 | `_RESUME.md` §2 11-16 「WORK 검수 뒤(코디)」 행 F-1 · SPEC-002 §9-5 확인 절차 4 | SPEC 그대로 |

## 12. SPEC-002 절 ↔ WP 대응(안 걸린 구현 대상 = 0)

| SPEC-002 절 | 구현 대상 | WP |
|---|---|---|
| §1 목적 · 범위 밖 | — (만들지 않는 것: 상담 설계 · 화면 · DB · SDK — §2-1) | — |
| §2-1 세 열 · §2-2 같은 것 / 다른 것 | ✓ | WP-2(A) · WP-3(B) · WP-4(C) · WP-5(`runner` — 같은 질문 · 같은 설정) · WP-3(공통 답 지시 한 벌) |
| §2-3 A 의 원장 도구 | ✓ | WP-2 |
| §2-4 C 의 도구 | ✓ | WP-4 |
| §3-1 흐름 · RG1 ~ RG8 · 입구 고르기 · 폭과 깊이 · BR1 ~ BR4 · C1 ~ C3 | ✓ | WP-3(3-a ~ 3-f) · BR3 은 WP-6 과 코드 공유 |
| §3-2 범위별 허용 표 | ✓ | WP-3(3-a) |
| §3-3 Jev 요청 꼴 | ✓ | WP-3(3-b · 3-d · 3-f) |
| §3-4 문턱 | ✓ | WP-1(`config.py`) · WP-3 |
| §3-5 방문 장부 | ✓ | WP-3(3-e) |
| §3-6 묶음 표 | ✓ | WP-3(3-g) |
| §4 hard gate — 답 전(K1 ~ K5) | ✓ | WP-3(3-h) |
| §4 hard gate — 답 뒤 | ✓ | WP-7(D5 · D7 · ②) |
| §5 종료 상태 | ✓ | WP-3(3-i · B 앱 판정) · WP-7(② `graded_end_state` — 세 열) |
| §6-1 경로 · 모델 · 추론 | ✓ | WP-1(E2 · E3) · WP-3(3-j · `b_on`) |
| §6-2 옛 `cli.py` 에서 가져갈 것 | ✓ | WP-1 |
| §6-3 답 프롬프트 원칙 | ✓ | WP-3(`prompts/`) |
| §6-4 Jev 클라이언트 | ✓ | WP-1(E1) |
| §7-1 ~ §7-3 기록 | ✓ | WP-5(+ 열별 trace 는 WP-2 · 3 · 4 가 채움) |
| §8-1 기준 | ✓ | WP-6 · WP-7 |
| §8-2 ① D1 ~ D9 | ✓ | WP-7(7-a · 7-b) |
| §8-3 ② LLM 채점 | ✓ | WP-7(7-c · 7-d) |
| §8-4 원장 오류 따라감 · §8-5 두 벌 | ✓ | WP-7(7-e) |
| §8-6 모범 답 기준 | ✓ | WP-7(7-f) · 모범 답 원문은 WP-6 세트 파일(로컬) |
| §9-1 ~ §9-3b 세트 묶음 | ✓ | WP-6(6-a · 6-b · 6-c) |
| §9-4 세트 파일 · 답 키 | ✓ | WP-6 |
| §9-5 전체 답 키 뽑기 · 사용자 확인 절차 | ✓ | WP-6(6-d ~ 6-g) |
| §10 지표 · 보고서 | ✓ | WP-7(7-g) · WP-8(batch) |
| §11 열린 것 | 아래 §13 | — |

## 13. 열린 것 — SPEC-002 §11 이 「구현 때 정함」 으로 넘긴 것(번호 그대로 · 이번에 정할 제안값)

| # | 무엇 | 이번에 정할 제안값 | 어디서 |
|---|---|---|---|
| O-7 | D3 이름 뽑기 · gold 코드 집합 | 이름 = (a) `g_entry.norm` 사전으로 훑기(긴 것 먼저 · 겹치면 전부) / 코드 집합 = (a) 채점 단계에서 로컬 gold CSV | WP-7 |
| O-8 | 채점 입력의 인용 가리기 | 바꿈 — `gid` · 원장 포인터를 `[근거 n]` 꼴의 중립 표지로 | WP-7 |
| O-11 | 이름 · 자리 · 꼴 | 세트 파일 `data/eval-set/set.jsonl` · 호출 명세 `data/eval-set/calls/<id>.json` · 답 키 `data/eval-set/answer-key/<id>.json` · 요약 `data/eval-set/key-summary.md` · A 서버 이름 `clinic-chat-raw` · 도구 `raw_list` · `raw_get` · `raw_search` · env `RAW_DIR` · `LEDGER_CHECK_PATH` · 깊이 결정 `deepen` · `listed_only` · `uncertain` · `gate_forced` · `columns.b_on` · 설정 `RANGE_CONFIDENCE_AT` · `RANGE_RATIO_AT` · `WALK_MAX_STEPS` · `ANSWER_INPUT_MAX_TOKENS` · 묶음 표 표기 = 묶음마다 머리 줄(같은 값 칸) + 행 줄(`gid` + 다른 값 칸)의 JSON Lines · 새 묶음 문항 수 4 · 5 · (이 문서가 더한 이름) `read_as` · `ANSWER_REASONING` · `JEV_BATCH_SIZE` · `EVAL_SET_DIR` · `QUESTIONS_CSV` · A 가 읽는 파일 = `RAW_DIR` 의 `*.json` 전부 · (0.2.0 이 더한 이름) 세트 파일 칸 `two_readings` · `status` · C trace 기록 칸 `edge_gold_ids[]` · 프롬프트 확인 기록 `data/eval-set/prompts-confirmed.json` · 배관 확인 자리 `runs/plumbing/` · 진입점 `quality.grade --plumbing` · 합성 키 표지 `synthetic` | WP-1 ~ 8 |
| O-15 | C 에 주는 도구 수 | (a) `health` 뺀 7 | WP-4 |
| O-22 ① ② | 층 ↔ `reach` 표 · M3 · M4 · M6 의 결정론 검사 꼴 | SPEC 본문 그대로(이름 칸을 글자 그대로 찾기) — ① 은 답 키 확인 때 사용자에게 함께 보인다 | WP-7 |
| O-23 | CLI 로 추론을 끌 수 있는가 | **구현 첫 확인 항목(E2)** — 되면 `off` · 안 되면 `lowest_effort`. 결과는 `settings.answer_reasoning` · 보고서 머리에 | WP-1 |
| (r5) Z-1 | 표 사이 겹침의 「남은 입구」 | 읽는 범위의 시작 표에 어느 쪽도 없는 표 사이 겹침도 entity Choice 로 · 불확실하면 RG6 | WP-3(3-b) |
| (r5) Z-2 | RG6 표지 필드 이름 · 채점 목록 | `read_as{by: "rg6", table, code}` · ② 「불확실 표시」 목록에 한 구절 = 「어느 개념으로 읽었는지 밝혔나 · 하나로 읽고 밝혔으면 통과」 — 걸리는 조건은 세트 파일 `two_readings`(RG6 을 탄 수는 Z-3 셈으로만) | WP-3(3-c) · WP-7(7-d) |
| (r5) Z-3 | 보고서 `unasked` 를 갈라 읽기 | D8 줄 곁에 RG3 · `via = RG6` 문항 수(B 칸) | WP-7(7-g) |

**이번 판에서 정하지 않는 것**(본문 값으로 돌리고 기록만 남긴다): 「1회차 trace 뒤」 — O-4 (나)(다) · O-5 ① ③ · O-16 · O-17 · O-20(문턱 값 · 한계) · O-21(입구 고르기 값 · 한계) · O-22 ③. 「승인됨 — 1회차는 본문 초안으로」 — O-5 ② ④(Q12 의 B 앱 판정이 기대와 어긋날 것을 알고 간다). 「뒤 단계에서 사용자 확인」 — O-9(프롬프트 문구 · §11 C-1 — **확인 지점이 SPEC 의 「답 프롬프트 WP 앞」 이 아니라 e2e 보고 때다**) · O-10 · O-19(답 키 확인 때 — WP-6).

**SPEC 0.4.2 때 되적을 것**(SPEC 은 이번에 안 고친다): ① O-9 의 확인 지점 문구(「WP 앞」 → e2e 보고 때 · C-1) ② 「범위 밖」 · 「입구 없음」 · 「실행 중단」 에서 단계 ⑤ 를 부르는 것과 그 입력(§4 · §5 · C-4) ③ ② 「불확실 표시」 목록의 Z-2 구절과 세트 파일 칸 `two_readings`(§8-3 · §9-4) ④ C trace 의 `edge_gold_ids[]`(§7-3) ⑤ 허브 쪽 — WORK-001 §9 의 N1-1 · H-2 · H-5.

## 14. 이 문서를 쓰며 본 것(SPEC 은 고치지 않았다 — 보고용)

| # | 자리 | 본 것 | 이 계획에서 한 것 |
|---|---|---|---|
| A-1 | SPEC-002 §1 「코드 자리」 · §6-2 | 「clinic_chat 새 브랜치(main 기준) · 새 case 모듈」 이라 적혀 있으나 **`origin/main` 에는 코드가 없다**(파일 3). 「새 case 모듈」 을 더할 기존 패키지가 없다 | 패키지를 새로 세운다(§2-3) — 옛 `hub-evals` 에서 배관만 옮긴다 |
| A-2 | SPEC-002 §2-3 「읽는 파일」 | 옛 틀은 원장 파일 이름 21 개를 코드에 고정했다. `RAW_DIR` 로 정한 폴더는 파일 24(JSON 21 · md 2 · txt 1)라 수는 맞는다 — 다만 이름 목록을 새 코드에 옮길지가 SPEC 에 없다 | 「`RAW_DIR` 의 `*.json` 전부 + manifest 기록」 으로 제안(O-11) — 이름을 코드에 박지 않는다 |
| A-3 | SPEC-002 §9-2 ~ §9-3b | 추가 32 문항의 질문 문장을 **누가 쓰는지** 가 없다(「세트 파일 작업 · 사용자 확정」 까지) | 결정론 후보 목록(`pick.py`) → 워커 초안 → 사용자 확정(§11 C-2) |
| A-4 | SPEC-002 §4 · §5 · §6-3 | 「범위 밖」 · 「입구 없음」 · 「실행 중단」 으로 끝난 질문에서 단계 ⑤ 를 부르는지가 글로는 없다(§6-3 은 「앱이 판정한 종료 상태를 함께 준다」 · §4 는 「단계 ④ 를 통과해야 단계 ⑤ 로 간다」) | **코디 결정으로 닫힘(§11 C-4)** — 부른다 · 입력은 `end_state` + 빈 `verified` · 검사에 실패한 행은 안 싣는다 · 못 부르면 `answer` 빈 값 + `error`(§5 「단계 ⑤ 를 부르는 범위」) |
| A-5 | SPEC-002 §7-1 `commits.hub` | 앱이 허브 커밋을 어디서 읽는지 없다(허브 `health` 에 커밋 칸이 없다 — SPEC-001 §4-8) | env(`HUB_COMMIT` 또는 허브 워크트리 경로)로 받고 못 읽으면 `null` |
| A-6 | SPEC-002 §8-3 ↔ r5 Z-2 | RG6 표지를 채점이 보려면 「그 문항이 RG6 를 탔다」 는 것을 채점 입력에 줘야 하는데, 그대로 주면 B 가 드러난다. 또 RG6 은 실행마다 갈려 세 열에 같은 물음이 못 된다 | 세트 쪽 고정 표지 `two_readings`(따로 둔 칸)로만 걸고, 물음을 「어느 개념으로 읽었는지 밝혔나」 로 바꿨다(§9 「r5 Z」 의 Z-2) — B 의 실행 결과를 채점 입력에 넣지 않는다 |
| A-7 | SPEC-002 §2-4 | C 에 도구 7 만 주려면 CLI `--allowedTools` 를 서버 단위(`mcp__<이름>`)가 아니라 도구 이름 단위로 줘야 한다 — CLI 가 그 꼴을 받는지는 E5 에서 확인 | 안 받으면 서버 단위(8)로 돌리고 그 사실을 보고(O-15 (b) 가 됨) |
| A-8 | SPEC-002 §9-5 확인 절차 4 | (0.1.0 이 `--allow-unconfirmed` 를 보고 없이 더했던 자리 — 검수 F-1) SPEC 은 예외 없이 「확인 전 키로는 채점하지 않는다」 다 | **뺐다(§11 C-5).** 배관 확인은 합성 키로 · 실제 채점은 확인된 키로만 |

## 변경 기록

### 0.2.0 (2026-11-16) — 검수 `review-work-001-002.md` 반영(FAIL 1 · WARN 6 · NOTE 7) + 코디 결정 2

계약(SPEC-002)은 고치지 않았다. 코디 결정 = `_RESUME.md` §2 11-16 「WORK 검수 뒤(코디)」(F-1 · W2-1) · 「진행 순서(코디 · WORK-002 §11)」(C-1 ~ C-3). 그 밖의 「고칠 방향」 은 리포트의 첫 선택지를 따랐다.

| 지적 | 고친 것 | 자리 |
|---|---|---|
| **F-1** | `--allow-unconfirmed` 를 **뺌** — 미확인 키를 푸는 길 없음. E6 = **합성 키** 배관 확인(`--plumbing` · 세트를 안 읽음 · `runs/plumbing/` · 「채점 수치 아님」 표시) · WP-8 완료 조건 3 = E5 줄은 채점하지 않고 배관만 합성 키로 · 실제 채점은 사용자 확인 뒤 | §0 · §2-4 · §2-6 E6 행 · 아래 불릿 둘 · §8 확인 절차 4 · §9 7-g · 「E6 — 합성 키 배관 확인」 · 완료 조건 3 · 5 · 6 · §10 e2e 표 · 완료 조건 2 · 3 · §11 C-5 · §14 A-8 |
| W2-1(코디 결정) | 세 상태에서도 단계 ⑤ 를 부름 — `end_state` + 빈 `verified` · 실패한 행 안 실음 · 못 부르면 `answer` 빈 값 + `error` · 세 열 같은 조건 · 문구는 프롬프트 초안 → e2e 때 확인 | §5 3-j 행 · 「단계 ⑤ 를 부르는 범위」 1 ~ 7 · 완료 조건 6 · §11 C-4 · §14 A-4 |
| W2-2 | C-1 이 SPEC O-9 의 글자와 다름을 명시 · 근거 행 · 「프롬프트 미확정」 표시 자리(터미널 요약 · 보고서 머리 · `--check`) · 확인 기록 파일 · 완료 조건 | §0 · §2-4 · §5 「프롬프트 파일」 O-9 불릿 1 ~ 5 · §7 구현 메모 · 완료 조건 5 · §9 7-g · §10-1 · e2e 표 · 완료 조건 2 · §11 C-1 · §13 |
| W2-3 | 엣지의 `gold_id` 를 `gids[]` 에서 뺌 · `edge_gold_ids[]` 에 기록만 | §6 구현 메모 · 완료 조건 · §7 완료 조건 1 |
| W2-4 | Z-2 구절을 세 열 같은 뜻으로(「어느 개념으로 읽었는지」) · 표지를 `expected_entries[]` 와 가른 칸 `two_readings` 로 · RG6 수는 Z-3 셈으로만 | §2-4 · §9 「r5 Z」 Z-2 · §13 O-11 · Z-2 행 · §14 A-6 |
| W2-5 | WP-3 완료 조건 5 를 K1 그대로(조회마다 `read == total` · `complete` · `gid` 합집합 ⊂ `verified_gids`) — 등식 뺌 | §5 완료 조건 5 |
| W2-6 | 순서 그림 · 표에 「WP-6 은 WP-3 의 3-a 뒤」 · 3-a 를 먼저 뗌 | §5 3-a 행 · §11 그림 · 불릿 · 병행 표 |
| N2-1 | 「11 필드」 수를 뺌 — §7-3 B 표의 필드 목록 그대로 | §7 완료 조건 1 |
| N2-2 | E4 를 WP-3 진입 조건으로 옮김(WP-1 완료 = E1 ~ E3) | §2-6 머리 · E4 행 · §3 목표 · 완료 조건 4 · §5 진입 조건 |
| N2-3 | 자식 env 에서 지울 이름에 `QUESTIONS_CSV` · `EVAL_SET_DIR` | §2-5 아래 · §3 완료 조건 2 |
| N2-4 | `gold-build.py` 실행(`import` · `exec`) 금지 · 구문 트리로 `QUESTIONS` 만 · 질문 문장 칸 안 옮김 | §8 6-b · 완료 조건 7 |
| N2-5 | E5 의 문항 = 37 중 하나 · `draft` 문항은 확정 전 안 보냄 | §2-6 E5 행 · 불릿 · §8 완료 조건 4 · §10-1 · 완료 조건 3 |
| N2-6 · N2-7 | 고칠 것 없음(C-3 에 「못 돌림 → 완료로 안 적음」 한 구절만 옮겨 적음) | §11 C-3 |
| (WORK-001) N1-4 | 앱 `hub_rest` 는 허브 오류를 HTTP 상태로 가른다 | §3 구현 메모 |

### 0.1.0 (2026-11-16)

처음 씀 — WP 8 · SPEC-002 절 대응표 · 열린 것 · A-1 ~ A-7.
