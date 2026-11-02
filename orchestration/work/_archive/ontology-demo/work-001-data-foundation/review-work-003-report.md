# WORK-003 에이전트·채팅 검수 보고

- 검수자: `@kknaks-reviewer` (read-only)
- 대상: `app/ontology-agent/agent/` 7파일 · `api/chat_router.py` · `config.py` · `main.py` ·
  테스트 4파일 + `app/back/docker-compose.yml`(+42/−0)
- 기준: `roles/ontology-demo/backend/rules.md` · SPEC-005 v0.0.4 · SPEC-003 v0.0.9 · SPEC-002
- 코디 검증치(364 passed/5 skipped · 라이브 게이트 4·5 워커 실측)를 전제로 **구조·계약**만 본다.
  테스트는 돌리지 않았다.

## 판정: **WARN** — 차단 0건 · 경고 5건 · nit 5건

S-001·ADR-04·codex 제출 안전·채팅 계약·PII·compose 는 전항 통과다. 게이트 5 검증기는
**우회 분기 없이 구조로 강제된다** — `done` 으로 저장되는 유일한 경로가 검증 통과 뒤다.
경고 5건 중 W1(SPEC-005 OQ-5 재시도 미구현)과 W2(citation `period` 생략 시 대조 창 확대)가
값이 크고, 나머지 셋은 잔여 리스크 표기다.

---

## 1. S-001 · ADR-04 — 통과

### 프롬프트에 관계·도메인 지식 0건 ✓

`agent/prompt.py` 전문을 읽었다. 노드 id·엣지·판정값·KPI 이름·계산식이 **한 건도 없다.**
도구 이름 4종과 답변 객체 **필드 이름**만 있고, 필드 예시조차 값이 아니라 자리표시자다
(`"<trace_ontology 응답의 edge_id 그대로>"`) — 파일 머리 주석이 그 이유를 스스로 적어 뒀다(`:21-22`).

검사도 실재한다 — `tests/test_w003_submission.py:128-141` 이 노드 id 10종 · 판정 5종 ·
한글 지표명 7종 · `부터 ÷` · **`→`** 를 포함한 24개 needle 로 `SYSTEM_PROMPT` 를 훑는다.
`→` 를 금지어에 넣은 것이 특히 정확하다 — 관계 지식이 새는 가장 짧은 형태가 화살표다.
반대 방향 방어(`:144-149`, 빈 프롬프트로 통과하지 못하게 도구·필드 존재를 요구)도 있다.

### 워커가 추가한 2규칙 — **경계 안이다** ✓

| 규칙 | 위치 | 판단 |
|---|---|---|
| `bronze` 가 원본, `silver` 는 변환값 — 「원본 N건」류는 `bronze`, `limit` 을 요청 건수로 | `prompt.py:31-33` | **도구 선택 규칙**이다. 메달리온 계층의 정의는 SPEC-001 의 **도구 표면 속성**이지 「어떤 KPI 가 어떤 KPI 의 원인인가」가 아니다. 이미 도구 docstring 이 같은 층위의 안내를 담고 있다(`tools/server.py:111-121`) |
| 전제 교정으로 끝내지 말고 교정 후 1번(관계 추적)을 그대로 수행 | `prompt.py:47-49` | **루프 행동 규칙**이다. 도메인 문자열이 0건이고, SPEC-005 §3 의 「교정 후 이어간다」를 문장으로 옮긴 것뿐이다 |

둘 다 S-001 이 막으려는 것(관계 지식을 프롬프트에 실어 도구 없이 답이 나오게 하는 것)을
전혀 열지 않는다. **경계 안으로 판정한다.**

### ADR-04 ✓

`tests/test_w003_submission.py:159-176` 이 `APP.rglob("*.py")` 전건을 **AST 로** 훑어
`anthropic`·`openai`·`google.generativeai`·`cohere`·`mistralai` import 0건을 고정한다.
문자열 grep 이 아니라 import 노드를 보므로 주석·문서 오탐이 없다. 실행은 open-kknaks
`AgentClient`+`RedisBroker` 경유뿐이고(`runtime.py:64`, `consumer.py:213`) 그 import 는
**lazy** 다 — `:179-189` 가 「top-level 에 없고 함수 안에는 있다」를 둘 다 단언한다.

---

## 2. 게이트 5 검증기 구조 — 통과 (경고 2건 동반)

### 우회 경로 점검 — 요청받은 세 축

**① 검증기 스킵 분기: 없다.**
`done` 상태가 저장되는 경로는 `consumer.py:160-175` `finalize_done` **하나뿐**이고,
그 안에서 `extract_answer_object` → `validate(ontology_conn, obj)` → `store.update_message(...
STATUS_DONE)` 순서다. `validate` 는 문제가 하나라도 있으면 예외를 던지므로 **검증을 건너뛴 채
`result` 가 저장되는 경로가 존재하지 않는다.** `finalize_failed` 는 `result` 를 쓰지 않는다
(`:177-183`). 따라서 폴링이 돌려주는 `result` 는 **정의상 게이트 5 통과본**이다.

**② 예외 삼킴: `done` 을 만드는 삼킴은 없다.** 세 곳의 광범위 catch 를 전부 확인했다 —
`_consume:236-238`(`AnswerSchemaError` → `finalize_failed`), `run_consumer:205-207`(→ AI_FAILED),
`start_turn:97-102`(제출 실패 → failed). **전부 `failed` 로 떨어지는 방향**이라 검증을 통과하지
못한 답변이 정상처럼 보이는 경로가 없다. 유일한 조용한 skip 은 `_check_pii` 의
`except sqlite3.Error: return`(`answer.py:396-397`) — W3 으로 따로 적는다.

**③ 부분 검증: 없다.** `validate_evidence:211-214` 가 네 검사를 **전부 부르고** 문제를 한
리스트에 모아 마지막에 한 번 던진다(`:216-217`). 중간에 `return` 하는 분기가 없어 앞선 검사가
실패해도 뒤 검사가 건너뛰이지 않는다. 각 검사 안의 `continue` 는 문제를 **적은 뒤** 다음
항목으로 가는 것이라 누락이 아니다.

### SPEC-005 Validation 표 전건 대응 ✓

| spec Validation | 구현 | 위치 |
|---|---|---|
| `used_edges[]` 가 `ontology_edges` 에 존재 | DB 재조회 후 부재면 「지어낸 엣지」로 거부 | `answer.py:224-237` |
| `used_edges[].verdict` 채택·자동 확정·선언만 | `CAUSAL_VERDICTS` 밖이면 거부 + **정본 표기와 다르면도 거부** | `:239-246` |
| `citations[].value` 재조회 일치(오차 0) | `_requery` 후 단일값·합계·행값 셋 중 하나여야 통과 | `:277-289`, `_eq` 는 1e-9 |
| `citations[].source` tool·table·column 전부 | 스키마 단계에서 강제 | `:184-186` |
| `drilldown.rows[]` 마스킹 뷰 산출 | `view != spec.relation` 이면 거부 | `:358-360` |
| `followups[]` 0~3 | `MAX_FOLLOWUPS=3` | `:29,163-164` |
| `premise_correction` corrected:true 3필드 | 강제 | `:149-152` |
| PII 원값 0건 (`answer`·`citations`) | 브론즈 원값 집합과 대조 (+ `drilldown.rows` 까지) | `:369-409` |

**정량 추정 차단이 성립하는 근거**: `citations[].value` 를 숫자로 강제하고(`:270-274`,
`"3.69억"` 같은 문자열은 거부) 실제 컬럼에서 재조회한 값 집합과 맞춘다. 곱셈으로 만든 수치는
그 집합에 없으므로 걸린다. `_is_allowed_relation`(`:332-336`)이 출처를 allowlist 의 `relation`
으로 한정해 원 테이블 출처도 막는다. 검증 결과를 `ValidationReport` 로 남겨 「예외가 안 났다」가
아니라 **무엇을 어떻게 맞췄는지**를 재현 가능하게 한 설계(`:57-68`, `citation_matches`)가 좋다.

**구조가 못 잡는 것(설계 한계, 결함 아님)**: 본문 산문이 근거 없이 인과를 서술하는 경우.
`used_edges` 가 비면 ②는 공허하게 통과한다. **SPEC-005 §4 Case Matrix 마지막 행이 이 경우를
「회귀에서 잡는다」로 이미 배정**했고, `tests/test_w003_regression.py:193-224`(R-1, `used_edges`
빈 배열 단언)·`:276-287`(게이트 5 라이브) 이 그 자리를 맡는다. 정확한 역할 분담이다.

---

## 3. codex 제출 안전 — 통과 (요구 4항 전건이 테스트로 고정)

| 요구 | 구현 | 고정 테스트 |
|---|---|---|
| `approval_mode` **per-tool 4줄** | `submission.py:85-88` 이 `TOOL_ALLOWLIST` 를 돌며 `tools.<name>.approval_mode="approve"` | `test_w003_submission.py:44-45` |
| **서버 기본 아님** | 서버 기본 줄을 만들지 않는다 | **`:47-48` 이 「`mcp_servers.ontology.approval_mode` 로 시작하는 줄이 없다」를 단언** — 부재를 검사한 것이 핵심이다 |
| `features.apps=false` | `:94` | `:55` |
| shell / web_search off | `:90-91` | `:56-57`(+ `image_generation` `:58`) |
| `sandbox="read-only"` | `:37,123` | `:87` |

추가로 `enabled_tools` 가 **비지 않음**을 정확한 문자열로 고정하고(`:61-68` — 빈 배열이면
툴 0개가 되는 fail-closed 계약), `server_key` 가 URL·allowlist 두 곳에서 같은지를 정규식으로
확인한다(`:71-77` — 갈리면 에러가 아니라 조용히 툴 0개). `approval_policy="never"` 가 허용이
아니라 「안 물어보고 실패」라는 함정을 주석·테스트 양쪽에 남긴 것(`:35-39`)도 정확하다.
**이 항목은 요구 이상이다.**

로그 위생 `redact_config_overrides`(`:137-146`)는 지금 헤더를 싣지 않는데도 미리 뒀다 —
근거를 주석에 적어 뒀고 테스트도 있다(`:115-121`).

---

## 4. SPEC-003 채팅 계약 · SPEC-005 필드 — 통과

- **엔드포인트 5종** 전부 존재하고 `Depends(require_session)` 으로 게이트 뒤에 있다
  (`chat_router.py:21-23,56,74,80,86,108`).
- **1,000자·빈 질문** — trim 후 검사, 422 `QUESTION_TOO_LONG` / `EMPTY_QUESTION`(`:33-39`).
- **`CONVERSATION_BUSY` 409** — `has_pending` 로 선차단(`:94-96`, `store.py:157-162` 「pending 최대 1」).
- **180초** — `asyncio.wait_for(..., settings.ai_timeout_sec)` 로 이벤트가 아예 안 와도 끊긴다
  (`consumer.py:197-204`) → `AI_TIMEOUT`.
- **`error_code`** — `AI_FAILED`/`AI_TIMEOUT` 두 코드가 `failed` 일 때만 실린다
  (`store.py:30-32`, 성공 시 `None` 으로 덮는다 `consumer.py:170`).
- **폴딩** — 부분 텍스트·`steps` 가 이벤트마다 적재되고(`:101-136`) 폴링이 읽는다.
  `tool_use_id` 멱등 upsert(`:138-149`)로 재부착 재생에도 단계가 늘지 않는다.
  `duration_ms` 를 서버가 재고(`:132-134`) AI 신고에 기대지 않는다 — SPEC-003 「기록 주체는 백엔드」 ✓.
- **재시도 = 재제출** — 같은 행을 되살리고 새 줄을 만들지 않는다(`chat_router.py:124-127`).
  되살릴 질문을 **그 답변 바로 앞의** user 메시지로 고른 것(`:134-143`)이 정확하다 — 대화
  마지막 질문을 쓰면 다른 턴을 재제출하게 된다.
- **`ai_session_id` 비노출** — `_row_to_conversation` 이 응답에서 뺀다(`store.py:100-106`) ✓
  SPEC-003 Data Contract.
- **SPEC-005 답변 객체 필드** — `answer`·`premise_correction`·`used_edges`·`excluded_edges`·
  `citations`·`drilldown`·`followups`·`unknowns` 전건이 프롬프트 지시와 스키마 검증 양쪽에 있다.
  필수/선택 구분도 spec 표와 일치한다(필수 4종은 배열이라도 존재 강제 `answer.py:154-156`).

---

## 5. 채팅 DB 분리 · PII — 통과

- **파일 분리** — `config.py:87` `chat_db_path` + `resolved_chat_db_path`(`:111-116`)가 온톨로지
  DB 옆 `ontology_chat.db` 로 떨어진다. 근거(재빌드 때 대화가 날아간다)를 주석에 남겼다.
- **read-only 를 깨지 않는다** — `store.connect()` 는 자기 경로로만 열고(`store.py:71-83`)
  온톨로지 DB 는 검증 시점에 `connect_ro()` 로만 열린다(`consumer.py:233-240`, `finally` 로 닫힌다).
  채팅 저장소가 온톨로지 DB 를 여는 코드 경로가 **없다.**
- **`args_summary` 에 값이 없다** — `summarize_args`(`consumer.py:61-81`)가 싣는 것은 지표명·
  `grain`·`layer`·`table`·`node`·`direction`·`term` 과 **필터 개수**뿐이고 `filters` 의 **값은
  싣지 않는다**(`:77-79`). 120자 상한(`:39,81`)도 있다. SPEC-003 「인자 원문 비노출」 ✓.
- 답변 본문·인용·드릴다운 행의 PII 는 게이트 5 가 브론즈 원값 집합과 대조해 막는다(§2).

---

## 6. compose — 통과 (기존 서비스 diff 0 실증)

`git diff -- app/back/docker-compose.yml` 이 **+42/−0** 이고 삭제 줄이 한 건도 없다.
`worker`(:66)·`chat-worker`(:114)·`mcp`(:101)·`back`·`redis`·`postgres` 블록은 diff 에
**등장조차 하지 않는다** — 추가 hunk 하나가 `chat-worker` 헬스체크 뒤부터 시작하고,
`volumes:` 섹션도 항목 추가뿐이다.

격리 설계도 맞다 — 전용 큐(`AI_QUEUE: ontology`, config 기본값과 일치) · 전용 네임스페이스 ·
전용 `CODEX_HOME=/root/.codex-ontology` · 전용 볼륨 `ontology-codex-sessions`. **원장 마운트가
없다**는 것을 주석으로 못 박아 데이터가 MCP 도구로만 오게 했다. 레플리카 1 고정 근거(세션이
워커 로컬 파일)도 적혀 있다.

---

## 7. 경고 (WARN)

### W1. SPEC-005 OQ-5 「1회 재시도 후 실패」가 구현되지 않았다 — 그런데 세 곳이 있다고 적는다

- **spec**: OQ-5 **확정(2026-09-02 승인)** — *"스키마 위반 시 처리 — 1회 재시도 후 실패 표시"*.
- **구현**: `consumer.py:236-238` 이 `AnswerSchemaError` 를 받으면 **곧바로**
  `finalize_failed(CODE_AI_FAILED)` 한다. 재제출·재파싱 경로가 없다.
- **그런데** `config.py:83` 에 `ai_schema_retry: int = 1` 이 「SPEC-005 OQ-5 — 1회 재시도 후 실패」
  주석과 함께 선언돼 있고 **어디서도 읽히지 않는다**(grep 실측: 선언 1건뿐). 독스트링 세 곳도
  재시도가 있다고 적는다 — `answer.py:12`(「호출자가 재시도 또는 실패로」) · `:38`(「1회 재시도 후
  failed(SPEC-005 OQ-5)」) · `consumer.py:163`. **문서·설정이 없는 동작을 있다고 말한다.**
- **완화 요인**: 방향이 fail-closed 라 잘못된 답변이 나가지는 않는다. OQ-6 이 「재시도 횟수는
  실측 후 조정」으로 **아직 열려 있어** 확정값이 흔들릴 여지도 있다.
- **코디 판단 필요**: (a) `ai_schema_retry` 를 실제로 물려 1회 재파싱/재제출을 넣거나,
  (b) OQ-5 를 「사용자 `/retry` 로 갈음한다」로 개정한다. 어느 쪽이든 **죽은 설정과 세 독스트링은
  지금 정리해야 한다** — 다음 사람이 재시도가 있다고 믿는다.

### W2. `citations[].period` 가 없으면 재조회 창이 **테이블 전체**로 넓어진다

- `validate_schema` 는 citation 에 `value` 와 `source.{tool,table,column}` 만 요구한다
  (`answer.py:174-186`). `period`·`metric`·`grain`·`row_count` 는 검사하지 않는다 —
  **SPEC-005 Validation 표와는 일치**하므로 계약 위반은 아니다.
- 그런데 `_requery`(`:309-322`)는 `period` 가 dict 이고 start·end 가 **둘 다 있을 때만** WHERE 를
  붙인다. 없으면 **컬럼 전체**를 읽고, `_match_rule` 의 `row_value`(어느 한 행과 같으면 통과)와
  `sum`(전 기간 합계)이 그만큼 헐거워진다. 235행짜리 일별 컬럼이면 우연 일치 확률이 크게 오른다.
- 즉 **모델이 `period` 를 빠뜨리면 게이트 5-①이 스스로 약해진다.** 프롬프트는 `period` 를
  지시하지만(`prompt.py:87`) 검증이 강제하지 않아, 지시를 어긴 응답이 더 느슨한 검사를 받는
  역전이 생긴다. 테스트 픽스처는 전부 `period` 를 채우고 있어 이 경로가 **한 번도 검사되지 않았다**.
- **닫는 법**: `period` 를 필수로 올리거나(`row_count` 와 함께 — SPEC-005 §4 필드 계약에 이미 있다),
  `period` 가 없으면 `sum`·`row_value` 규칙을 끄고 `single_row` 만 허용한다.

### W3. `_check_pii` 가 `sqlite3.Error` 를 삼키고 **조용히 통과**시킨다

- `answer.py:396-397` — `except sqlite3.Error: return`. 브론즈 조회가 실패하면 PII 대조가
  통째로 생략되고, `validate` 는 그대로 통과한다. 주석은 「브론즈가 없는 DB(단위 테스트)」라 적었다.
- 운영 경로에서는 `connect_ro(require_build=True)` 가 전 게이트 통과 DB 만 열어 주므로 브론즈가
  반드시 있다 — 현재는 도달 불가에 가깝다. 다만 **검증기 안의 유일한 조용한 skip** 이고,
  `ValidationReport.pii_scanned_fields` 는 그때도 값이 채워져 있어 리포트만 보면 검사한 것처럼 보인다.
- **닫는 법**: 단위 테스트용 분기를 예외 삼킴이 아니라 「브론즈 존재 여부를 먼저 보고, 없으면
  리포트에 `pii_scanned_fields=0` 과 skip 사실을 남긴다」로 바꾼다.

### W4. `has_pending` 검사와 삽입이 원자적이지 않다

- `chat_router.py:94-101` 이 같은 커넥션에서 검사 후 삽입하는데 `store.connect()` 는
  `isolation_level=None`(autocommit)이라 트랜잭션이 없다(`store.py:75`). 동시 요청 둘이 모두
  검사를 통과해 `pending` 두 건이 생길 수 있다.
- SPEC-003 은 FE 선차단 + 409 백스톱 구조이고 내부 데모라 실현 가능성은 낮다. `BEGIN IMMEDIATE`
  로 감싸면 닫힌다.

### W5. compose 가 `ontology-mcp` 를 정의하지 않는데 `mcp_url` 이 그 이름을 가리킨다

- `config.py:86` 기본값 `http://ontology-mcp:28081/mcp` 인데 `docker-compose.yml` 에 그 서비스가
  없다(서비스 목록 실측: postgres·redis·back·worker·mcp·chat-worker·ontology-worker).
  `ontology-agent`(FastAPI) 컨테이너도 없다.
- WORK-003 범위가 워커까지인 것은 이해되나, **지금 상태로 `docker compose up` 하면 워커가 도구
  서버를 못 찾는다.** 배포 WP 로 넘길 항목임을 브리프에 명시할 것을 권한다.

---

## 8. nit

1. `prompt.py:9` 가 `tests/test_w003_prompt.py` 를 가리키는데 그 파일은 없다 — 실제 검사는
   `tests/test_w003_submission.py:137-141` 에 있다. 경로만 고치면 된다.
2. `chat_router.py:119-120` — 이미 `done` 인 메시지에 retry 하면 409 `CONVERSATION_BUSY` 가
   나간다. 바쁜 것이 아니라 「재시도할 실패가 아님」이라 코드 의미가 어긋난다(SPEC-003 Case
   Matrix 에 해당 코드가 없어 차선을 고른 것으로 보인다).
3. `answer.py:292-299` `_match_rule` 이 `row_value` 를 허용해 「구간 안 어느 행과 같으면 통과」가
   된다. W2 와 겹치는 느슨함이고, `metric`/`grain` 을 함께 대조하면 좁힐 수 있다.
4. `consumer.py:135` 가 `steps[].is_error` 를 넣는데 SPEC-003 `step` 계약
   (`{tool, args_summary, duration_ms, called_at}`)에 없는 필드다. 가산적이라 무해하나 FE 가
   모르는 키다.
5. `store.py:173` `update_message` 가 f-string 으로 컬럼을 조립한다. 호출부가 전부 내부 리터럴
   dict 이라 현재는 안전하지만, 허용 키 화이트리스트를 두면 그 전제가 코드로 남는다.

---

## 9. 결론

세 축(프롬프트 S-001 · 게이트 5 검증기 · codex 제출 안전) 모두 **주장이 아니라 구조와 테스트로**
서 있다. 특히 「`done` 이 되는 유일한 경로가 검증 뒤」라는 배치와, 승인 축이 둘이라는 함정을
per-tool 4줄 + **서버 기본 부재 단언**으로 고정한 것은 이 WP 에서 가장 잘 된 부분이다.
`app/back/docker-compose.yml` 은 +42/−0 으로 기존 서비스 무변경이 실증된다.

**WARN.** W1(OQ-5 재시도 — 죽은 설정과 세 독스트링 포함)과 W2(`period` 생략 시 게이트 5 자기
약화)는 코디 판단이 필요하고 둘 다 국소 수정이다. W3~W5 와 nit 5건은 차기 WP 에 얹어도 된다.
차단 사항이 없으므로 재검수는 W1·W2 처리 후 해당 부분만 보면 된다.
