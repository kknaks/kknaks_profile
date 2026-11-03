# CC(`clinic_chat` 실험 앱) HTTP API

확인일: 2026-11-02. 기준: `clinic_chat/hub-evals`의 현재 `clinic_chat/server.py`, `runner.py`, `runs.py`, `batch.py` 코드. **CC 서버가 화면에 제공하는 API**만 정리한다. 기본 주소는 `http://127.0.0.1:18210`이고, 경로는 `/api`로 시작한다. 요청 본문은 JSON이다. 이 문서는 코드에서 확인한 계약이며 실제 서버 호출 결과는 아니다.

**인증 경계:** 현재 CC의 인바운드 HTTP API에는 사용자 로그인, 세션, Bearer 토큰, API 키 검사, 인증 미들웨어가 없다. 로컬 주소(`127.0.0.1`)에만 바인딩하는 것이 접근 범위 제한이다. 따라서 이 서버에 접속할 수 있는 클라이언트라면 실행 기록 조회, 질문 실행, 채점, 배치 시작·중지 API도 호출할 수 있다. `/api/providers`와 질문 실행 중의 CLI 인증 검사는 **CC가 외부 답변 제공자를 사용할 수 있는지** 확인하는 로직이며, CC API 호출자를 인증하지 않는다.

## 한눈에 보기

| 용도 | 메서드 · 경로 | 요청 | 응답 |
|---|---|---|---|
| 기동 상태 | `GET /api/status` | 없음 | 연결·설정 점검 결과 |
| 사용 가능한 답변 제공자 | `GET /api/providers` | 없음 | provider별 모델·인증 상태 |
| 질문 실행 | `POST /api/ask` | 질문, 선택적 provider | `run_id` |
| 실시간 진행 | `GET /api/runs/{run_id}/events` | 경로의 run ID | SSE 이벤트 스트림 |
| 실행 목록 | `GET /api/runs?limit=50` | 선택적 limit | 실행 요약 배열 |
| 실행 상세 | `GET /api/runs/{run_id}` | 경로의 run ID | 답변·시간·비용·채점 포함 기록 |
| 사람 판정 | `POST /api/runs/{run_id}/human_check` | case, verdict, note, item | 저장한 판정 한 건 |
| 채점 실행 | `POST /api/runs/{run_id}/quality` | 없음 | 채점을 합친 실행 상세 |
| 같은 질문 3회 재실행 | `POST /api/runs/{run_id}/rerun` | 없음 | 새 run ID 3개, 질문 |
| 질문 세트 | `GET /api/questions` | 없음 | 배치용 질문 배열 |
| 배치 목록 | `GET /api/batches` | 없음 | 배치 요약, 부족한 설정 |
| 배치 계획 생성 | `POST /api/batches` | providers, 선택적 질문 번호 | 계획 요약 |
| 배치 상세 | `GET /api/batches/{batch_id}` | 경로의 batch ID | 계획 요약, 항목, 최근 로그 |
| 배치 시작 | `POST /api/batches/{batch_id}/start` | 없음 | 시작된 batch ID |
| 배치 중지 요청 | `POST /api/batches/{batch_id}/stop` | 없음 | 중지 요청한 batch ID |

## 1. 상태와 provider

### `GET /api/status`

요청 없음. 기동 시 만든 점검 정보를 돌려준다. 주요 필드는 아래와 같다. 연결 실패는 HTTP 오류 대신 해당 필드에 이유 문자열로 표시될 수 있다.

```json
{
  "keys": {"anthropic": true, "typesafe": true},
  "cases": {"case1": null, "case2": null, "case3": null},
  "default_provider": "claude-cli",
  "hub_health": {"build": "...", "build_hash": "...", "raw": "..."},
  "gold_mcp": 11,
  "raw_mcp": 1,
  "section_tools": ["..."],
  "intent_tools": ["..."],
  "vocab": {"...": 10},
  "models": {"claude-sonnet-5-5": true},
  "raw_store": "...",
  "semantic": "있음"
}
```

위 값은 **형태 예시**다. `gold_mcp`, `raw_mcp`, `models`, `vocab` 등은 연결 상태에 따라 문자열이나 생략된 필드가 될 수 있다. 키의 **값은 응답에 나오지 않고 존재 여부만** 나온다.

### `GET /api/providers`

요청 없음. 응답은 `providers`, `default`, `judge`를 준다.

```json
{
  "providers": [
    {"provider": "sdk", "model": "claude-sonnet-5-5", "effort": "high", "billed": "api", "available": true, "reason": null},
    {"provider": "claude-cli", "model": "claude-sonnet-5-5", "effort": "medium", "billed": "subscription", "service_tier": null, "available": true, "reason": null, "auth_kind": "subscription", "cli_version": "..."},
    {"provider": "codex-cli", "model": "...", "effort": "medium", "billed": "subscription", "service_tier": null, "available": false, "reason": "...", "auth_kind": "...", "cli_version": "..."}
  ],
  "default": "claude-cli",
  "judge": {"provider": "claude-cli", "model": "claude-opus-5-5"}
}
```

`available`은 호출 시점의 키 또는 CLI 구독 인증 점검 결과다. 모델명과 effort는 설정에 따라 달라진다.

## 2. 단건 질문과 실행 기록

### `POST /api/ask`

```json
{"question": "질문 내용", "provider": "claude-cli"}
```

| 필드 | 조건 |
|---|---|
| `question` | 필수 문자열, 1~2000자. 서버는 양끝 공백을 제거한다. |
| `provider` | 선택. `sdk` · `claude-cli` · `codex-cli`; 생략하면 서버 기본 provider. |

응답: `{"run_id":"..."}`. **답변은 이 응답에 없다.** 서버가 실행을 시작한 다음 SSE로 진행 상황을 보내고, 완료 기록은 상세 조회에서 읽는다. 유효하지 않은 provider 또는 본문은 `422`다. 현재는 공백만 있는 질문이 길이 검사를 통과할 수 있으며, 서버에서 공백 제거 후 빈 문자열로 실행될 수 있다.

### `GET /api/runs/{run_id}/events`

요청 본문 없음. `Content-Type: text/event-stream`으로 이벤트를 보낸다. **현재 서버 프로세스 메모리에 있는 run만** 구독할 수 있다. 서버 재시작 뒤 저장된 run은 상세 조회로 읽어야 하며 여기서는 `404`다. 구독 시 이미 쌓인 이벤트부터 순서대로 재생한다.

| 이벤트 | data의 주요 필드 | 뜻 |
|---|---|---|
| `provider` | `provider`, `model`, `effort`, CLI면 `auth` | 이번 질문의 실행 설정 |
| `stage` | `case`, `name`, `start_ms`, `end_ms`, `tokens` | 단계별 시간 갱신 |
| `text` | `case`, `delta` | 답변 글자 조각 |
| `trace` | `case` 및 도구·탐색 추적 필드 | 해당 case의 내부 진행 결과 |
| `case_done` | `case`, `timing`, `tokens`, `error`, `stop_reason`, `loop_capped`, `refusal`, `cost` | 한 case 완료 |
| `cost` | `cases`, `answers_usd`, `quality_usd`, `total_usd`, `billed`, `pricing_as_of` | 답변 비용 집계 |
| `answers_done` | `run_id`, `auto_quality` | 세 답변 완료·기록 저장. 채점은 계속될 수 있음 |
| `case_quality_start` / `case_quality_done` / `case_quality_error` | `case`; 완료 시 `cost_usd`, 오류 시 `message` | case별 채점 상태 |
| `word_check` | `case`, `names`, `not_found` 또는 `error` 등 | 이름 검사 결과 |
| `judge` | `case`, `items`, `pass_count`, `failures` 또는 `error` 등 | Opus 채점 결과 |
| `quality_done` | `run_id` | 자동 채점 완료 |
| `error` | `case`와 `message`, 또는 전역 `message` | 실행 오류 |
| `run_done` | `run_id` | 스트림 종료 |

SSE 한 메시지 예시:

```text
event: text
data: {"case":"case3","delta":"답변 조각"}
```

### `GET /api/runs?limit=50`

`limit`은 선택적 정수다. 서버에서 1~100000으로 제한한다. 최신 기록부터 반환한다.

```json
{
  "runs": [{
    "run_id": "...", "asked_at": "...", "question": "...", "provider": "claude-cli",
    "model": "...", "effort": "...", "question_no": null, "topic": null,
    "batch_id": null, "gold": "빌드 해시 앞 8자 또는 null",
    "cases": {"case1": {"total_ms": 1000, "error": null, "not_found": null, "judge_pass": null, "human": null, "cost_usd": 0.0}},
    "rerun_of": null, "cost": {}, "graded": false, "grading": false
  }]
}
```

`cases`에는 실제로 `case1`, `case2`, `case3`가 들어간다. 목록은 답변 전문이 아닌 요약이다. `question_no`, `topic`, `batch_id`는 배치 실행 때 채워질 수 있다.

### `GET /api/runs/{run_id}`

요청 본문 없음. 없는 기록은 `404`.

```json
{
  "record": {
    "run_id": "...", "asked_at": "...", "question": "...", "provider": "claude-cli",
    "versions": {"answer_model": "...", "gold_build_hash": "...", "app_commit": "..."},
    "settings": {"walk_max_steps": 4},
    "cases": {
      "case1": {"answer": "...", "timing": {"ttft_ms": 1000, "total_ms": 2000, "stages": []}, "tokens": {}, "trace": {}, "error": null, "cost": {}, "word_check": {}, "judge": {}},
      "case2": {}, "case3": {}
    },
    "cost": {"cases": {}, "answers_usd": 0.0, "quality_usd": null, "total_usd": 0.0},
    "judge_mode": "absolute"
  },
  "human_checks": []
}
```

위 `record`는 **주요 필드만 보인 축약 예시**다. 실제 각 case에는 `answer`, `stop_reason`, `loop_capped`, `refusal`, `error`, `timing`, `tokens`, `trace`, `cost`, `word_check`, `judge` 등이 담긴다. 채점 결과는 별도 `quality.jsonl`의 가장 최근 값을 합쳐 반환한다. `human_checks`의 각 행은 `run_id`, `case`, `verdict`, `item`, `note`, `at`을 갖는다.

### `POST /api/runs/{run_id}/human_check`

```json
{"case":"case3","verdict":"맞음","note":"근거 확인","item":null}
```

`case`는 `case1` · `case2` · `case3`, `verdict`는 `맞음` · `틀림`만 허용한다. `note`는 생략 시 빈 문자열, `item`은 생략 시 `null`이다. 응답은 저장한 행 그대로다.

```json
{"run_id":"...","case":"case3","verdict":"맞음","item":null,"note":"근거 확인","at":"..."}
```

잘못된 case/verdict는 `422`. 현재 구현은 해당 run ID가 저장돼 있는지 확인하지 않고 판정 행을 추가한다.

### `POST /api/runs/{run_id}/quality`

요청 본문 없음. 답이 있고 오류가 없는 case 중 아직 채점 기록이 없는 case를 채점한다. 응답은 `{"record": ...}`로, 위 상세의 `record`와 같은 형태다. 없는 run은 `404`, 같은 run의 채점이 진행 중이면 `409`. 모든 case가 이미 채점됐다면 새 채점 없이 현재 기록을 반환한다. SDK 실행은 기본적으로 수동 채점이며 CLI 실행은 자동 채점이다.

### `POST /api/runs/{run_id}/rerun`

요청 본문 없음. 원래 질문과 provider로 3개 run을 새로 시작하고 곧바로 ID를 반환한다.

```json
{"run_ids":["...","...","..."],"question":"원래 질문"}
```

각 답은 새 ID의 SSE 또는 상세 조회에서 확인한다. 없는 원본 ID는 `404`. 코드상 세 실행은 각각 백그라운드 작업으로 시작한다.

## 3. 배치 API

### `GET /api/questions`

요청 없음. 설정된 `QUESTION_SET_JSON` 또는 `QUESTIONS_MD`를 읽어 반환한다.

```json
{"questions":[{"n":1,"text":"질문", "meta":{"question_no":1,"topic":"..."}}]}
```

`meta`는 JSON 질문 세트를 쓸 때 붙고, Markdown 질문 파일이면 없을 수 있다. 질문 파일 설정이 없거나 파일이 없으면 `409`.

### `GET /api/batches`

요청 없음.

```json
{"batches":[{"batch_id":"...","created_at":"...","updated_at":"...","state":"planned","providers":["claude-cli"],"progress":{"total":1,"done":0,"failed":0,"todo":1,"running":0}}],"config_missing":[]}
```

`config_missing`은 배치 시작에 필요한 설정 중 비어 있는 이름 목록이다.

### `POST /api/batches`

```json
{"providers":["claude-cli"],"questions":[1,3]}
```

`providers`는 필수 문자열 배열이며 각 값은 `sdk` · `claude-cli` · `codex-cli` 중 하나여야 한다. `questions`는 선택적 번호 배열이고, 생략하면 설정된 전체 질문을 계획한다. **계획만 만들고 실행하지 않는다.** 질문 파일이나 provider 설정이 잘못되면 `409`.

```json
{"batch_id":"...","state":"planned","progress":{"total":2,"done":0,"failed":0,"todo":2,"running":0},"now":null,"paused":{},"failed":[]}
```

### `GET /api/batches/{batch_id}`

요청 본문 없음. 없는 배치는 `404`.

```json
{
  "batch_id":"...", "state":"planned", "progress":{"total":1,"done":0,"failed":0,"todo":1,"running":0},
  "now":null, "paused":{}, "failed":[],
  "items":[{"key":"1:claude-cli","n":1,"question":"...","provider":"claude-cli","status":"todo","attempts":0,"run_id":null,"error":null,"meta":{}}],
  "log":[]
}
```

`log`는 최근 20개만 반환한다. 항목 상태는 `todo` · `running` · `done` · `failed`다.

### `POST /api/batches/{batch_id}/start`

요청 본문 없음. 설정 검사가 통과하면 백그라운드에서 배치를 시작한다. 응답은 `{"started":"<batch_id>"}`. 필수 배치 설정이 비었거나 다른 배치가 실행 중이면 `409`. 없는 ID는 계획 파일 읽기에서 발생하는 `FileNotFoundError`를 이 라우트가 별도로 `404`로 바꾸지 않는다.

### `POST /api/batches/{batch_id}/stop`

요청 본문 없음. 응답은 `{"stopping":"<batch_id>"}`. 현재 실행 중인 항목이 끝난 뒤 다음 항목을 시작하지 않도록 전역 중지 플래그를 세운다. 이 라우트는 전달된 batch ID의 존재 여부나 현재 실행 배치와의 일치를 검사하지 않는다.

## 오류 응답과 읽는 순서

FastAPI 검증 오류는 일반적으로 `{"detail":[...]}`와 HTTP `422`, 코드에서 직접 발생시킨 오류는 `{"detail":"..."}` 형태다. 실행 중 case별 실패는 HTTP 오류가 아니라 SSE `error` 및 상세 기록의 `cases.<case>.error`에 남을 수 있다.

화면 흐름은 `POST /api/ask` → 반환된 `run_id`로 SSE 구독 → `answers_done` 뒤 다음 질문 가능 → `run_done` 뒤 `GET /api/runs/{run_id}`로 완성 기록 확인 순서다. 저장된 과거 질문은 `GET /api/runs` → 상세 조회로 읽는다.

## 코드 근거

- 라우트와 요청 모델: `clinic_chat/hub-evals/clinic_chat/server.py`
- 실행 기록과 SSE 데이터: `clinic_chat/hub-evals/clinic_chat/runner.py`
- 기록 조회·사람 판정·채점 병합: `clinic_chat/hub-evals/clinic_chat/runs.py`
- 질문 세트·배치 계획/상태: `clinic_chat/hub-evals/clinic_chat/batch.py`
- 화면의 API 사용 및 이벤트 처리: `clinic_chat/hub-evals/web/app.js`, `web/state.js`

확인 시 CC 작업트리에 미커밋 수정이 있었다. 이 문서는 **2026-11-02 현재 파일 상태**를 기준으로 한다.
