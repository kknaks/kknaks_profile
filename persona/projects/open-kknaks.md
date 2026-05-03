---
type: project
id: P-04
title:
  ko: "open-kknaks"
  en: "open-kknaks"
summary:
  ko: "PTY 기반 Claude Code CLI 태스크 큐 라이브러리 + MCP 서버"
  en: "PTY-based task queue library for Claude Code CLI, with MCP server"
category: cli
status: live
date: "2026.03"
stack:
  - Python
  - Redis
  - MCP
  - Pydantic
  - Typer
  - structlog
visible: true
thumbnail: /assets/projects/P-04/cover.png
links:
  repo: "github.com/kknaks/open_kknaks"
# 포트폴리오 PDF 케이스 스터디 (planning-02 §3.3) — 비면 PDF 에 미표시.
problem:
  ko: ""
  en: ""
approach:
  ko: []
  en: []
impact:
  ko: []
  en: []
learnings:
  ko: []
  en: []
troubles: []
---

# 개요

Claude Code CLI 를 비동기 태스크 큐로 다루는 Python 라이브러리. 프로듀서 (`ClaudeClient`) 가 Redis 에 태스크를 enqueue 하면, 워커 (`ClaudeWorker`) 가 PTY 로 `claude -p ...` CLI 를 실행하고 stream 결과를 dequeue 한다. 라이브러리 + CLI + MCP 서버 3종 인터페이스 제공. PyPI 패키지 (`pip install open-kknaks`), MIT 라이선스, v2.0 안정화 (2026.04).

# 기술스택

**런타임**
- Python ≥3.10 (POSIX 전용 — Linux / macOS. Windows 미지원, PTY 의존)

**핵심 라이브러리**
- **Pydantic v2** — 태스크 / 결과 / 설정 모델
- **Redis** — 태스크 큐 브로커 (publisher/subscriber + DLQ)
- **MCP** (Model Context Protocol) — Claude Code 가 사용할 도구 스키마 노출
- **Typer** — CLI 명령 (`open-kknaks worker / task / queue / dlq`)
- **structlog** — 구조화 로깅 미들웨어

**외부 의존**
- **Claude Code CLI** — PTY 로 child process 실행. `claude login` 또는 OAuth token 필요.

**개발 도구**
- pytest + pytest-asyncio + **fakeredis** — Redis 모킹 테스트
- mypy strict — 타입 체크
- ruff — 린트 / 포맷
- hatchling + hatch-vcs — 빌드 / 버전 관리

# 주요기능

**라이브러리 (`open_kknaks` 패키지)**

- `ClaudeClient.submit(prompt, ...)` — 태스크 제출 (priority, model, max_turns, max_retries, delay, session_id, allowed_tools 등 14개 파라미터)
- `client.result(task_id, timeout=)` — 결과 polling
- `client.stream(task_id)` — 실시간 이벤트 스트림 (text / tool_use / tool_result / cost)
- `ClaudeWorker(broker, config, queues, concurrency, middleware)` — 워커 실행

**미들웨어 6종** (`open_kknaks.middleware`)

- `LoggingMiddleware` — 시작/완료/실패 구조화 로깅
- `RetriesMiddleware` — 실패 시 자동 재시도
- `TimeoutMiddleware` — 태스크 타임아웃
- `CostMiddleware` — 워커 / 글로벌 예산 제한 (USD)
- `RateLimitMiddleware` — 요청 속도 제한
- `CallbackMiddleware` — 완료/실패 콜백

**CLI** (`open-kknaks` entry point)

```
open-kknaks worker run --broker redis://... --queues default
open-kknaks task status / result / cancel
open-kknaks queue size
open-kknaks dlq list / retry / purge
```

**MCP 서버** (`open-kknaks-mcp` entry point)

Claude Code 의 `.mcp.json` 에 등록하면 13개 도구 스키마 노출:
`submit_task` / `get_task` / `get_status` / `get_result` / `cancel_task` / `submit_batch` / `get_batch_status` / `wait_batch` / `queue_size` / `list_dlq` / `retry_from_dlq` / `purge_dlq` / `get_cost`

# 아키텍처

```
ClaudeClient ──enqueue──▶ Redis ◀──dequeue── ClaudeWorker
                                                  │
                                              PTY Executor
                                                  │
                                              claude -p ...
```

**모듈 분리** (`open_kknaks/`):

```
open_kknaks/
├─ task.py · config.py · client.py · batch.py · exceptions.py
├─ broker/        ← Redis broker (base + redis impl)
├─ worker/        ← worker.py + stream_parser.py + line_buffer.py
├─ middleware/    ← 6개 (base + 5 구현)
├─ cli/           ← Typer 기반 5 sub-command
└─ mcp/           ← MCP 서버 (13 tools)
```

**작업 흐름**:

1. Client 가 prompt + options 직렬화 → Redis 에 enqueue (priority queue)
2. Worker 가 polling 으로 dequeue → 미들웨어 체인 통과 → PTY child process spawn
3. `claude -p <prompt> --output-format stream-json` 실행
4. stream parser 가 line buffer 로 chunk 누적 → JSON 이벤트 파싱 → `text` / `tool_use` / `tool_result` / `cost` 분리
5. Worker → Redis 에 progress / 최종 결과 publish
6. Client → `result()` 또는 `stream()` 으로 수신
7. 실패 시 retry → DLQ (Dead Letter Queue) 로 이동 → CLI 로 수동 재처리

# 핵심 구현

**stream parser** (`worker/stream_parser.py`)

Claude CLI 의 `--output-format stream-json` 출력을 line buffer 로 누적 → JSON event 단위로 파싱. v2.0 부터 text 이벤트에 `source` 필드 (`"result" | "assistant" | "delta"`) 추가해 출처 구분.

**미들웨어 체인** — 함수형 wrapping. `MiddlewareBase` 인터페이스로 사용자 확장 가능:

```python
worker = ClaudeWorker(
    broker=broker,
    middleware=[
        LoggingMiddleware(),
        RetriesMiddleware(max_retries=2),
        CostMiddleware(worker_budget_usd=5.0),
    ],
)
```

**examples/ 데모** — Docker Compose 로 Redis + Worker + FastAPI Web UI 통합. 시나리오 7개 (`01_basic` / `02_streaming` / `03_batch` / `04_priority` / `05_session` / `06_multi_queue` / `07_code_review`) 으로 라이브러리 사용법 자체가 e2e 테스트.

# 마주친 문제

(CHANGELOG v2.0 — 실제 fix 기록)

- **stream-json 파서가 result 메시지의 텍스트를 silently drop** — Claude CLI 의 정상 실행에서 `result` 메시지는 cost 와 텍스트를 동시에 담는데, 기존 파서는 cost 가 있으면 텍스트를 무시했다. 그 결과 v1.x 의 `TaskResult.output` 은 사실상 assistant 중간 메시지 모음이었음. v2.0 에서 `result` 메시지의 cost 이벤트 + text 이벤트 (`source="result"`) 모두 emit 하도록 수정.

- **한글 partial chunk 분절 버그** — `--include-partial-messages` 사용 시 `text_delta` 가 chunk 경계마다 `\n` 으로 분절되어 `"안\n녕하세요"` 같이 글자 단위로 쪼개짐. v2.0 에서 `TaskResult.result` 는 result 메시지 텍스트만 사용하도록 분리해 분절 제거. partial 은 여전히 `on_chunk` 콜백과 `stream` 필드에서 흐르되, 깔끔한 결과는 `result` 에서만 받음.

- **breaking change** — `TaskResult.output` 제거 → `TaskResult.result` (최종 텍스트) + `TaskResult.stream` (디버깅용 합본) 으로 분리. 사용자 마이그레이션 필요.

# 회고

> 일부 자동 추론 — 사용자 검토 권장.

- **(자동 추론)** v1.0 (2026.04.06) → v2.0 (2026.04.30) — 약 한 달 만에 메이저 버전. 안정화 직후에도 stream parser 버그 두 개를 발견해 breaking change 동반 v2.0 으로 끊은 결정. 빠르게 release 한 만큼 빠르게 정정한 패턴.
- **(자동 추론)** 한글 분절 버그는 영문 위주 dev 에서는 발견하기 어려운 종류. 본인 한국어 사용 환경이 quality assurance 의 일부로 작동.
- **PTY + POSIX 의존** — Windows 미지원을 받아들인 trade-off. 라이브러리 단순함과 Cross-platform 사이에서 단순함 우선.
- **MCP 서버 동시 노출** — Claude Code 자신이 이 라이브러리를 도구로 호출할 수 있게 만든 self-referential 구조. 동일 라이브러리가 producer 도, consumer 도 됨.
