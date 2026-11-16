---
type: spec
id: SPEC-006
title: "hub-evals 실험 앱 — 원장 MCP vs 골드 MCP vs 골드 + Jev · 로컬 프론트 질문 → 세 갈래 동시 실행 · 속도 · 품질 두 층 · 기록"
status: draft
product: procedure-hub
feature: phub-recommend
version: 0.3.1
created_at: 2026-10-30
updated_at: 2026-11-01
tags:
  - product/procedure-hub
  - feature/phub-recommend
  - doc/spec
  - status/draft
links:
  decisions:
    - "orchestration/work/phub-recommend/_RESUME.md §2 (10-30 「원장도 MCP 로」 · 「hub-evals 결정」 Q-1~Q-8 · 「최종 목표」 · 「hub-evals 는 골드 완성 뒤」 · DEC-001 D-08 · D-11)"
  sources:
    - "reference/2026-10-30-hub-evals/README.md"
    - "orchestration/work/phub-recommend/jev-research.md"
    - "orchestration/work/phub-recommend/SPEC-005.md §5 · §5-12"
  work:
    - "orchestration/work/phub-recommend/WORK-004.md"
    - "orchestration/work/phub-recommend/WORK-006.md"
  evals:
    - "reference/2026-10-30-hub-evals/build-out/fail-triage2.md §2 · §5(case2 잘림 100/614 · intent 2.1%)"
    - "orchestration/work/phub-recommend/cli-research.md · phub-recommend-jev-walk-addendum.md(11-01 사용자 결정)"
---

# SPEC-006 — hub-evals 실험 앱

> 검수 반영 2026-10-30(F-1 · W-1~W-7) — `review-spec006-report.md` · R-1~R-10 사용자 승인(10-30) · U-1 · U-2 사용자 완료 · 레포 세팅 사실(10-30)
> **v2.1 2026-11-01(0.3.1) — 검수 반영(`review-spec006-v2-report.md` F-1~F-3 · W-1~W-5)**: §3-5 표(50,000 자 → 실물 코드 상수로 특정 · Codex 마커 실물 후보 5 · Claude 변형 3) · 전달 보장 정의(마커 = WP-0 가 고정하는 상수 `TRUNCATION_MARKERS`) · §3-6 `intent_passed` 값 규칙(`none` 처리) · §4-4 · §7-6 C 비율 열 · §7-7 W-1 · W-2(v3.2 발주 보충 2 로 전달 확인) · WORK-006 시험 경로 · 코드 표면 표
> **v2 2026-11-01(0.3.0) — 실험 앱 공정성(B-1) + case3 교체(사용자 결정 11-01)**: §2-5 provider 층(CLI 판 — 「SPEC-006 과 다른 점」 본문 반영) · §3-5 도구 결과 전달 보장 · §3-6 intent 전달 · **§3-4 case3 = Jev 재귀 탐색으로 교체**(보충 `phub-recommend-jev-walk-addendum.md` 우선) · §3-7 공정성 원칙 · §4-2 기록 칸(`delivered_bytes` · `truncated` · `intent_passed` · `walk`) · §4-4 기록 검증 스크립트 · §7-6 v2 끝 조건 · §7-7 아직 안 정한 것. v1(0.2.0)은 `SPEC-006.v1.md` 보관. 근거 = `fail-triage2.md` §2 · §5 · `cli-research.md` · 11-01 실물 조사(§3-5 표)

근거는 아래 정본만이다. 결정은 다시 논의하지 않는다. 이 스펙이 고른 값 R-1~R-10 은 10-30 사용자 승인으로 결정됐다(§7-3). 남은 열린 것은 §7-5 에만 둔다.

| 정본 | 이 스펙에서 |
|---|---|
| `reference/2026-10-30-hub-evals/README.md` | 세 케이스 · 속도 칸 · 품질 두 층 · 화면 와이어 · 기록 꼴 · 열린 것 O-1~O-9 |
| `jev-research.md` | Jev = TypeSafe System One(MCP 없음 · Choice 선택지 255 한도 · confidence · Python SDK) · Claude 로컬 MCP = Anthropic SDK + MCP 클라이언트 |
| `_RESUME.md` §2 10-30 | 원장도 MCP · Q-1~Q-8 · 최종 목표 · 레포 공개 · 데이터 · 키 env |
| `SPEC-005.md` | 허브 골드 도구 9(§5) · 원장 도구 3(§5-12) · 포트 · 경로 — **계약**. 허브는 아직 구현 중이라 실물 대조는 허브 완성 뒤 |
| `quality-eval-set.json` | 나중 회귀용 참고만 — 실험 질문은 사용자가 그때그때 입력(README §1) |

## 0. 요약

- 사용자가 로컬 화면에 질문 하나를 넣으면 case1(원장 MCP + Sonnet) · case2(골드 MCP + Sonnet) · case3(허브 사전 → Jev Choice 슬롯 → 골드 도구 → Sonnet 1회)가 **같은 시각에** 돈다
- 열마다: 속도(ttft · total · 단계별 · LLM 왕복 · 토큰) · 답 스트리밍 · 도구 호출 / Jev 슬롯 / 허브 경로 · ① 단어 검사(원장 대조 결정론) · ② Opus 채점(항목별 통과 · 실패 · 근거 인용 · 가리기) · 사람 확인 표시 · 기록 한 줄(jsonl)
- 앱은 공개 레포 `kknaks/clinic_chat` · 로컬 실행. 허브(SPEC-005)는 따로 떠 있는 서버이고 이 앱은 그 MCP · REST 를 부르기만 한다
- **v2**: 실험은 CLI 판(Claude CLI Sonnet · Codex CLI terra · 구독 인증)으로 돈다(§2-5). case2 가 받는 허브 바이트를 허브 응답 전체로 보장(§3-5 — 2차 분류: Claude CLI 가 도구 결과 100/614 를 약 2KB 로 잘라 넘김 · 실패 56/131 이 잘린 문항) · 허브 호출마다 `intent` 를 넘김(§3-6 — 지금 2.1%) · 세 케이스 공정성 원칙 한 조항(§3-7) · **case3 는 Jev 재귀 탐색(peek → Choice → expand · 걸음 4 · 예산 20KB · 되돌아가기 = 의도 묶음 1회)으로 교체**(§3-4 · 11-01 사용자)

| 절 | 내용 |
|---|---|
| §1 | 범위 · 경계 |
| §2 | 구성 · 레포 구조 · env |
| §3 | 세 케이스 흐름 · 같은 조건 |
| §4 | 속도 측정 · 기록 꼴 |
| §5 | 품질 두 층 |
| §6 | 화면 |
| §7 | 열린 것 처리표(README O-1~O-9 · Jev Q-1~Q-8 · R-1~R-10 결정 · 사용자 몫 · 남은 열린 것 · **§7-6 v2 끝 조건 · §7-7 v2 아직 안 정한 것**) |
| §8 | 사용자 실행 절차 |

---

## 1. 범위 · 경계

| 안 | 밖 |
|---|---|
| 실험 앱(서버 + 로컬 화면) · 세 케이스 실행 · 측정 · 채점 · 기록 | 허브 자체(SPEC-005 · 별도 서버) |
| 단건 질문(대화 이어가기 없음) | 여러 턴 · 얼굴 지도 패널 · 병원 상품(KOS) · 운영 지연 예산 판정(README §8) |
| 로컬 실행 | 배포 · 외부 공개 서버 · 허브를 밖으로 노출(jev-research §4 — Messages API MCP connector 안 씀) |

- **LLM 키는 env 로만**(D-11 · 10-30 「Claude 는 API 키 별도」). 문서 · 레포 · 기록 · 로그에 키를 쓰지 않는다
- **공개 레포 규칙**(10-30 「레포 kknaks/clinic_chat 공개 · 데이터 · 키는 env」): 레포에 원장 json · 시맨틱 · 실버 · 골드 파일 · 실행 기록(jsonl) · 허브 응답 캐시 · `.env` 를 넣지 않는다. 경로는 env 로 받는다. `.gitignore` 에 `.env` · `runs/` · `*.jsonl` · 캐시 폴더
- **환자 정보 금지**(10-30): 실험 질문에 환자 정보를 넣지 않는다 — 화면 입력칸 위에 안내 한 줄. Jev(TypeSafe · 미국)로 질문 + 노드 이름이 나간다는 사실도 같은 줄에(jev-research B-4)
- 허브 쪽 계약: 골드 MCP `http://127.0.0.1:18005/procedure-hub/gold-mcp/mcp` · 원장 MCP `…/procedure-hub/raw-mcp/mcp` · REST `…/procedure-hub/gold/*`(SPEC-005 §1-3 · §5-1 · §5-12). 도구 입력 · 출력 스키마는 SPEC-005 §5-2~§5-10 · §5-12 그대로 쓴다

## 2. 구성

### 2-1. 실험 서버

| 항목 | 값 | 근거 |
|---|---|---|
| 언어 | Python 3.12 · `uv` | jev-research §5 · 허브와 같은 도구 |
| Claude | 공식 Anthropic Python SDK(`anthropic[mcp]`) — **직접 루프**(Agent SDK · Messages API MCP connector 안 씀) | 10-30 Q-2 |
| 허브 MCP 연결 | 공식 MCP Python SDK `ClientSession` + Streamable HTTP 클라이언트 transport(정확한 import 경로는 고정한 SDK 버전 문서로 확인 — jev-research §4) · 도구 변환은 `anthropic.lib.tools.mcp.async_mcp_tool` 또는 같은 꼴의 직접 변환 | jev-research §4 · claude-api 스킬 `python/claude-api/tool-use.md` 「MCP Tool Conversion Helpers」 |
| Jev | `typesafe-sdk` `AsyncTypeSafeClient` · 모델 `jev-1.14.0` 고정 | 10-30 Q-6 · jev-research §1 |
| 웹 | FastAPI · uvicorn · SSE(서버 → 화면 스트림) · 127.0.0.1 에만 바인딩 | §7-3 R-1(결정됨) |
| 설정 읽기 | `pydantic-settings` — `config.py` 가 레포 루트 `.env` 를 직접 읽는다(`uv run` 은 `.env` 를 저절로 읽지 않으므로 `--env-file` 대신 이 방식 하나) · 환경 변수가 있으면 그것이 앞섬 | 검수 W-4 |
| 동시 실행 | `asyncio` — 세 케이스를 `gather` 로 같은 `t0` 에서 시작 | README §3 |

### 2-2. 프론트(로컬)

- **결정(R-1): 빌드 없는 정적 페이지 하나**(HTML + 바닐라 JS + `EventSource` · 서버가 정적 파일로 냄)
- 이유: 화면 하나(3열 + 기록 목록)뿐이고 로컬 실험용이다 · Node 빌드 체인이 없으면 실행 명령이 서버 하나로 끝난다 · SSE 는 브라우저 기본 `EventSource` 로 충분하다 · 공개 레포에 의존성이 적다
- 나중에 바꿀 경우(React · Vite 등)도 화면 계약(§6 · SSE 이벤트 §4-3)이 같으면 서버는 그대로

### 2-3. 레포 `kknaks/clinic_chat` 구조

10-30 실물(레포 세팅 끝): GitHub 공개 레포 · main `240c321`(「레포 시작」 — `README.md` · `.gitignore` · `.env.example` 만 있음).

| 자리 | 경로 |
|---|---|
| canonical(main) | `/Users/kknaks/git/clinic_chat` |
| 작업 워크트리 | `/Users/kknaks/orca/workspaces/clinic_chat/hub-evals` · 브랜치 `kknaksss/hub-evals`(main `240c321` 에서) |

- main 의 `.gitignore` 는 이미 `.env` · `.env.*`(`!.env.example`) · `runs/` · `data/` · `raw/` · `*.jsonl` · Python 캐시를 막는다 — Phase 1 은 `.cache/` 한 줄만 더한다
- main 의 `.env.example` 은 키 두 개(`ANTHROPIC_API_KEY` · `TYPESAFE_API_KEY`) 빈칸뿐 — Phase 1 이 §2-4 나머지 이름을 더한다

```
clinic_chat/
  .env.example            env 이름 · 키 값 빈칸 · 사용자 홈 경로 없음(§2-4)
  .gitignore              (main 에 있음) + .cache/
  pyproject.toml · uv.lock
  README.md               (main 에 있음) + 실행 절차(§8) · 데이터 · 키 규칙
  prompts/                common.md · case1.md · case2.md · case3.md · judge.md · extract.md (판 = 파일 sha 앞 12자)
  clinic_chat/
    config.py             env 읽기(pydantic-settings · 루트 .env)
    clients/anthropic_client.py · jev_client.py · hub_mcp.py(골드 · 원장 ClientSession) · hub_rest.py
    cases/case1.py · case2.py · case3.py · loop.py(case1 · 2 공통 도구 루프)
    timing.py             t0 · stages[] 기록기(perf_counter)
    quality/word_check.py · judge.py · normalize.py(resolve_rules.normalize) · raw_tools.py(채점용 로컬 원장 도구 R1~R3)
    runs.py               jsonl 쓰기 · 읽기 · human_checks
    server.py             FastAPI · SSE · 정적 파일
  web/index.html · app.js · style.css
  tests/                  모의 허브 MCP · 모의 Anthropic 스트림 · 모의 Jev(키 없이 도는 시험)
```

### 2-4. env(`.env` · git 제외 · 예시는 `.env.example`)

`.env.example` 규칙: **키 두 개(`ANTHROPIC_API_KEY` · `TYPESAFE_API_KEY`) 값은 빈칸 · 사용자 홈 경로(`/Users/…`)는 쓰지 않음**(사용자 경로 칸은 빈칸). 그 밖의 예시 값(모델 id · 허브 URL · `./runs` · 포트 · 상한 · 문턱)은 적는다. 키는 사용자가 워크트리 `.env` 에 직접 넣는다(U-1 · U-2 완료 10-30).

| 이름 | 뜻 | 예시 값(.env.example) |
|---|---|---|
| `ANTHROPIC_API_KEY` | Claude API 키(사용자) | 빈칸 |
| `TYPESAFE_API_KEY` | Jev 키(사용자) | 빈칸 |
| `TYPESAFE_DEFAULT_MODEL` | Jev 모델 | `jev-1.14.0` |
| `ANSWER_MODEL` · `JUDGE_MODEL` · `EXTRACT_MODEL` | 답 · 채점 · 이름 뽑기 모델 | `claude-sonnet-5-5` · `claude-opus-5-5` · `claude-opus-5-5`(R-4) |
| `HUB_GOLD_MCP_URL` · `HUB_RAW_MCP_URL` · `HUB_REST_URL` | 허브 주소 | `http://127.0.0.1:18005/procedure-hub/gold-mcp/mcp` · `…/raw-mcp/mcp` · `…/procedure-hub/gold` |
| `RAW_DIR` | ① 단어 검사 · ② 채점 원장 도구(§5-2)가 읽는 원장 21 폴더(레포 밖) | 빈칸(사용자 경로 — `.env` 에서 `…/PROCEDURE-HUB/phub-stg-2026-10-26` 꼴로 채움) |
| `SEMANTIC_JSON` | ① 정규화 규칙 · 표기 차이 확인용 시맨틱 사전(레포 밖) | 빈칸(사용자 경로 — `…/orchestration/work/phub-recommend/semantic.json` 꼴) |
| `RUNS_DIR` | 기록 폴더(레포 밖 또는 ignore 된 `runs/`) | `./runs` |
| `CLINIC_CHAT_PORT` | 실험 서버 포트 | `18210`(사용자 포트 3700 · 3800 · 8700 · 8800 · 54329 · 허브 18005 와 안 겹침) |
| `CASE_TOOL_LOOP_MAX` | case1 · 2 도구 루프 상한 | `12`(R-2) |
| `JEV_CONFIDENCE_MIN` | 낮은 신뢰 표시 문턱 | `0.3`(10-30 Q-5) |

### 2-5. provider 층 — SDK 판 · CLI 판(v2 · 「SPEC-006 과 다른 점」 본문 반영)

10-30 사용자 결정 「실험은 CLI · 배포는 SDK」 · 「CLI provider 결정」 · 「채점 방식 바꿈」 · 「밤새 일괄 실험」 과 `cli-research.md` §6 · 구현(`clinic_chat/llm/cli.py` · `cli_process.py` · `specs.py` · `batch.py`)을 v2 본문으로 올린다. v1 의 SDK 판 조항(§2-1 · §3-1 · §3-2 R-2 · R-3)은 **SDK 판에만** 남는다.

| 항목 | SDK 판(`provider=sdk`) | CLI 판(`claude-cli` · `codex-cli` — **실험 기본**) | 근거 |
|---|---|---|---|
| LLM 호출 층 | Anthropic SDK 직접 루프(§2-1 · `loop.py`) | `claude -p --output-format stream-json --verbose --include-partial-messages`(stdin 프롬프트) · `codex exec --json` — 앱은 JSONL 이벤트를 `CaseTimer` · 기록 꼴로 옮기기만(`cli.py` `ClaudeIngest` · `CodexIngest`) | cli-research §1 · §6-1 |
| provider 고르기 | 질문마다 화면 옵션(`POST /api/ask {question, provider}`) · 기본 `DEFAULT_PROVIDER=claude-cli` · 세 케이스 모두 같은 provider · 기록 `provider` · `versions.answer_provider` | 10-30 「질문에 옵션으로 클로드 / 코덱스 선택」 |
| 모델 · effort | Sonnet 5.5 · effort `high`(R-3) | Claude `claude-sonnet-5-5` · Codex `gpt-5.6-terra` · **effort `medium` 둘 다**(`--effort` · `-c model_reasoning_effort`) · 세 케이스 같음 | 10-30 CLI provider 결정 |
| thinking | `between_tools`(Q-3) | **CLI 기본값**(끌 수 없음 · 기록 `settings.thinking: "cli-default"` · `thinking_seen` · 바퀴마다 `thinking_ms` 따로) — ttft 는 thinking 제외 첫 글자 | cli-research §3-3 |
| 인증 · 과금 | API 키(env) | **구독만** — 자식 env 에서 `ANTHROPIC_API_KEY` · `ANTHROPIC_AUTH_TOKEN` · `*_BASE_URL` · `CODEX_API_KEY` · `OPENAI_API_KEY` · `TYPESAFE_API_KEY` 를 지움(`child_env`) · 실행 앞 `auth.check`(Claude `apiKeySource` 없음 · Codex 로그인) 아니면 그 열 오류 · 기록 `cost.billed: "subscription"` · `usd_estimate`(CLI 추정 · 청구 아님) | 10-30 「ANTHROPIC_API_KEY 는 .env 에서 뺌」 · cli-research §4-1 |
| 격리 | — | Claude `--setting-sources ""` · `--tools ""` · `--allowedTools mcp__hub` · `--strict-mcp-config` · `--disable-slash-commands` · `--no-session-persistence` · `--system-prompt`(Claude Code 기본 프롬프트 갈아 끼움) · `--permission-mode bypassPermissions` · 임시 cwd(레포 밖) / Codex 전용 `CODEX_HOME`(auth.json 링크만) · `--ignore-user-config` · `--ignore-rules` · `--ephemeral` · `-s read-only` · 셸 · exec · 웹검색 · 플러그인 · 스킬 끔 · `model_instructions_file` · `project_doc_max_bytes=0` · `shell_environment_policy.inherit="none"` | cli-research §5 |
| 도구 루프 상한 | `CASE_TOOL_LOOP_MAX` 12 · 닿으면 `tool_choice none`(R-2) | **없음**(CLI 에 칸 없음 · D-3) — `CLI_TIMEOUT_SEC` 600 · Claude `--max-budget-usd` 1.0 · 도구 호출 수 기록 · `tool_loop_max: null` · `loop_capped` 는 CLI 판에서 늘 false | cli-research B-2 |
| 입력(도구 결과) 상한 | `TOOL_RESULT_MAX_BYTES` 20,000(`cap_text`) | **셋 다 없음**(CLI 가 직접 받음 · case3 도 안 넣음 · 기록 `settings.input_cap_bytes: null`) → v2 §3-7 원칙으로 정리 · **SDK 판도 상한을 없앤다**(v2 — 두 판 같게 · `TOOL_RESULT_MAX_BYTES=0` = 없음) | 10-30 결정 · cli-research B-3 |
| ttft | 첫 `text_delta`(토큰) | Claude = 첫 `text_delta`(토큰) · Codex = 첫 `agent_message` 완료(메시지 단위 · 글자 델타 없음) → 기록 `timing.ttft_kind: "token"\|"message"` · 케이스 사이 비교는 같은 provider 안에서만 | cli-research §2 |
| CLI 단계 정의 | `claude#n` · `tool:<이름>#n` | `cli_boot`(spawn → `system/init`) · `cli_queue`(동시 상한 `CLI_MAX_CONCURRENT` 6 에 막혀 기다린 시간) · Claude `claude#n`(`status:requesting` → 그 바퀴 마지막 이벤트) · Codex `codex#n`(턴을 도구 호출로 나눔) · `tool:<이름>#n` · 「(측정 밖)#k」(어느 단계도 안 덮은 구간 — 덮인 합 + 빈틈 = total) · `thinking_ms` · `ttft_ms_ex_boot` · `total_ms_ex_boot` · `cli_boot_ms` | cli-research §2-1 · 10-30 피드백 |
| 채점(① · ②) | SDK Opus(수동 버튼 `AUTO_QUALITY`) | **Claude CLI Opus 자동** · `JUDGE_PROVIDER=claude-cli` · effort `medium`(① 뽑기 `low`) · `JUDGE_MAX_BUDGET_USD` 3.0 · 채점용 원장 도구 3 은 stdio 로컬 MCP(`quality/raw_mcp.py` · R-10 계약 그대로) | 10-30 「채점은 오퍼스로 자동 · cli 는 부담 없잖아」 |
| 채점 방식 | 세 답 묶어 비교(v1 §5-2 가리기 A · B · C) | **열마다 절대 채점** — 한 열 답이 끝나면 그 열 ① → ② 를 바로(세 열 기다리지 않음) · 답 하나씩 같은 기준 · 가리기 유지(case 이름 · 도구 흔적 · 속도 안 보임) · 기록 `judge.mode: "absolute"` · `judge_order` · `judge_seed` 는 남김(섞기 기록) | 10-30 「채점을 왜 한 번에 · 답변 먼저 나온 거 채점 먼저」 |
| 직렬 처리 | — | **없음** — 채점과 다음 질문이 서로 안 막음(서버 직렬 큐 없음 · CLI 동시 상한만) | 10-30 같은 결정 |
| 한도 | — | Claude `rate_limit_event`(status · rateLimitType · utilization · resetsAt · unifiedWindows) 기록 · rejected 면 그 열 오류 · `api_retry` 기록 / Codex 「usage limit」 문구 판정 | cli-research §4-3 · §6-4 |
| 일괄 실행 | — | `clinic_chat.batch` — 계획 파일 `RUNS_DIR/batches/<batch_id>.json` · 질문 × provider 순차(Q1 claude · Q1 codex · Q2 …) · 간격 `BATCH_GAP_SEC` · 재시도 `BATCH_RETRIES` + `BATCH_RETRY_BACKOFF_SEC` · 한도 `BATCH_LIMIT_WAIT_SEC` · 이어 가기 `--resume` · `--label` · `--questions-file` · 질문 세트 `QUESTION_SET_JSON`(239문항) · 값은 사용자가 정함(10-30 전체 실행: 간격 15초 · 재시도 2) · 기록 `batch_id` · `batch_item` · `question_no` · `src_id` · `topic` · `reference_answer`(기록만 · 채점 기준 아님) | 10-30 「전체 질문 실행」 · 「밤새 일괄 실험」 |
| 기록 위치 | `RUNS_DIR` | `RUNS_DIR` = 프로필 레포 `reference/2026-10-30-hub-evals/runs/`(사용자가 봄 · `.gitignore` · 커밋 안 함) — L-1 닫힘 | 10-30 「실험 기록 저장 위치」 |
| 보고서 | — | `clinic_chat.report`(전체 실행) · `rerun_report`(전후 비교 — 통과율 182 · 239 환산 · 통과 수 · 「정보 없음」류 · 오류 · 시간 · 허브 바이트 · 나빠진 문항) · 출력은 레포 밖 `build-out/` | 10-30 「모아 두기만」 |

- v1 의 `.env.example` 표(§2-4)에 더해진 이름: `DEFAULT_PROVIDER` · `CLAUDE_CLI_BIN` · `CLAUDE_CLI_MODEL` · `CLAUDE_CLI_EFFORT` · `CODEX_CLI_BIN` · `CODEX_CLI_MODEL` · `CODEX_CLI_EFFORT` · `CODEX_SERVICE_TIER` · `CLI_TIMEOUT_SEC` · `CLI_MAX_BUDGET_USD` · `CLI_MAX_CONCURRENT` · `JUDGE_PROVIDER` · `JUDGE_CLI_EFFORT` · `EXTRACT_CLI_EFFORT` · `JUDGE_MAX_BUDGET_USD` · `AUTO_QUALITY` · `BATCH_*` 4 · `QUESTIONS_MD` · `QUESTION_SET_JSON` — 값은 `config.py` 기본값(10-30 결정)과 같다. **v2 가 더하는 이름**: `MCP_RESULT_MAX_CHARS`(§3-5 · 기본 200000) · `WALK_MAX_STEPS`(§3-4 · 4) · `WALK_BYTE_BUDGET`(20000) · `WALK_ENOUGH_MIN`(§3-4 · 0.5 추천 · §7-7) · `TOOL_RESULT_MAX_BYTES=0`

## 3. 세 케이스 흐름

### 3-1. 같은 조건(세 케이스 공통)

| 항목 | 값 | 근거 |
|---|---|---|
| 답 모델 | `claude-sonnet-5-5` · 세 케이스 같음 | README §1 |
| thinking | **끔** = `thinking: {"type": "between_tools"}`(Sonnet 5.5 에서 `disabled` 는 400 — 가장 낮은 설정이 `between_tools` · 다른 칸 같이 보내면 400) | 10-30 Q-3 · claude-api 스킬(Sonnet 5.5 breaking change 1) |
| effort | `output_config.effort = "high"`(Sonnet 5.5 기본값을 명시 · `between_tools` 는 high 이하만 받음) · 세 케이스 같음 | R-3(결정됨) |
| tool_choice | `auto`(Sonnet 5.5 · Opus 5.5 는 강제 `any` · `tool` 이 400) | claude-api 스킬 |
| 폴백 | 쓰지 않음 — 폴백 모델이 답하면 「세 케이스 같은 모델」이 깨진다. `stop_reason == "refusal"` 이면 그 열에 거절로 기록 | README §1 「세 케이스 같은 모델」 |
| 프롬프트 | 공통부(`prompts/common.md` — 답 문장 지시) 같음 + 케이스별 부분(데이터 · 도구 설명만 다름) | README O-2 선택지 → R-5(결정됨) |
| 시작 | 같은 `t0` 에서 동시 시작 | README §3 |
| 스트리밍 | Sonnet 호출은 전부 `messages.stream` | — |
| 단건 | 대화 이어가기 없음 · 매 질문 새 대화 | README §1 |

### 3-2. case1 — 원장 MCP + Sonnet

- 도구 = 원장 MCP 3(`raw_list` · `raw_get` · `raw_search` — SPEC-005 §5-12) 그대로. 골드 · 시맨틱에 기대지 않음(10-30 「원장도 MCP 로」 · Q-1)
- 루프(`loop.py`): Sonnet 스트림 → `tool_use` 면 MCP 호출(병렬 호출은 모아 한 user 메시지로 결과 반환) → 다시 Sonnet → … `end_turn` 까지. 상한 `CASE_TOOL_LOOP_MAX` 번 Sonnet 호출 — 닿으면 `tool_choice: {"type": "none"}`(강제 금지 대상 아님 — none 은 허용)로 마지막 답 호출 1번 · 기록 `loop_capped: true`
- `trace.context` = 도구 호출 목록(README §6 의 「넣은 자료 설명」 자리)

### 3-3. case2 — 골드 MCP + Sonnet

- 도구 = 골드 MCP 9(SPEC-005 §5-1 T1~T9) 그대로 · 같은 `loop.py`
- `trace.tool_calls[]{tool, input, output_bytes, node_ids[], ms}` — `node_ids` = 결과 JSON 안의 정본 id(`{kind}:{키}` 꼴) 전부(README §6)
- 골드 응답의 `claude_contract`(SPEC-005 §5-0 · O-3)는 도구 결과에 들어 있는 그대로 Sonnet 에 간다(이 앱이 따로 덧붙이지 않음)
- **v2**: CLI 판은 CLI 가 허브 MCP 를 직접 붙인다(앱 `hub_mcp.py` 를 안 거침 · `--mcp-config {"hub": {"type":"http","url":…}}` / Codex `mcp_servers.hub.url`) — 도구 결과 전달은 §3-5 · `intent` 는 §3-6 · 기록 `tool_calls[]` 칸은 §4-2

### 3-4. case3 — Jev 재귀 탐색(v2 · 11-01 사용자 결정 · **교체**)

> 보충 `phub-recommend-jev-walk-addendum.md` 가 우선한다. v1 의 「Jev 슬롯 1회 → 허브 경로 1회 → 의도 묶음 · 동봉 전부 → Sonnet」 은 잘못된 설계(허브가 「뭐가 필요할지 몰라 다 주는」 구조 — 2차 분류 case3 허브 결과 중앙 46,539B · p95 170,989B · C 10%)로, **되돌아가기(fallback) 경로로만** 남는다(§3-4-3). 허브 쪽 `peek` · `expand` 응답 꼴은 SPEC-005 v3.2(다른 planner)가 정한다 — 이 스펙은 앱이 그 계약에서 쓰는 칸만 §3-4-2 에 적는다(§7-7 W-1).

#### 3-4-1. 흐름

```
t0 ─▶ ① hub_resolve: T1 resolve(질문 전체)                                   [허브 REST · 결정론]
      ② jev#0: 의도 Choice 12 + 시작 노드 Choice(① 후보 ≤ 255 · 「해당 없음」)  [Jev 1회]
      ③ 걸음 k = 1..N(기본 N = 4 · WALK_MAX_STEPS):
           hub_peek#k: peek(node) — slim 카드 + 이웃 목록 + 섹션 목록 + 안전 요약 · ≤ 2KB     [허브 REST]
           jev#k: Choice「펼칠 것」(섹션 이름 ∪ 이웃 id · ≤ 255 · 「없음」) + Noul「답하기에 충분한가」 [Jev 1회]
           충분(≥ WALK_ENOUGH_MIN) 이면 멈춤 · 아니면 hub_expand#k: expand(node, 고른 섹션 | 이웃 id) [허브 REST]
           바이트 예산 B(기본 20,000 · WALK_BYTE_BUDGET)를 넘기면 멈춤(마지막 expand 는 예산 안에서 잘라 넣지 않고 **통째로 뺀다** · 기록 `budget_hit`)
      ④ claude: Sonnet 1회 — 입력 = 질문 + 걸음마다 모은 fact(id · 원문) + 안전 요약 + claude_contract(모은 fact id 합집합)   [스트리밍]
```

| 단계 | 규칙 | 근거 |
|---|---|---|
| 시작 노드 | ① `candidates` 가 비면 Jev 가 vocab(계열 · 고민 · 부위)에서 시작 노드 하나를 고른다 · 그래도 없으면 §3-4-3 되돌아가기 | Q-4 · 11-01 |
| 걸음 | 한 걸음 = `peek` 1 + Jev 1 (+ `expand` 1). 이웃을 고르면 다음 걸음의 `peek` 대상이 그 이웃(여럿이면 Choice 는 하나 · 짝 Noul ≥ 0.5 인 것까지 · 걸음당 이웃 ≤ 3) · 섹션을 고르면 같은 노드에서 `expand(sections)` | 보충 「펼칠 것(섹션 · 이웃 ≤255)」 |
| 멈춤 조건 | ⓐ Jev 「충분」 Noul ≥ `WALK_ENOUGH_MIN` ⓑ 걸음 N 소진 ⓒ 예산 B 소진 ⓓ 고를 것 없음(이웃 · 섹션 비어 있음) — 어느 것이든 기록 `walk.stop: enough\|steps\|budget\|empty` | 보충 |
| 의도 | 걸음 중 허브 호출에 `intent`(②)를 넘긴다 — 단 **의도 기본 묶음 · 동봉 자동 첨부는 case3 걸음 경로에서 쓰지 않는다**(`sections=none` 꼴 · peek/expand 가 Jev 가 고른 것만 냄) · 되돌아가기 경로만 의도 묶음 | 보충 「case3 는 peek/expand 로 크기를 Jev 가 정하므로」 |
| 안전(G13) | peek 의 안전 요약은 걸음마다 받되 Sonnet 입력엔 노드마다 한 번 · 걸음이 끝나도 안전 요약은 예산 밖에서 늘 포함(허브 결정 10-26 「안전은 늘」) | SPEC-005 G13 |
| Jev 선택지 | 섹션 이름(≤ 17) + 이웃 id(라벨 = peek 의 한 줄 라벨) 를 한 Choice 로(합이 255 넘으면 이웃을 `kind` 로 먼저 고르는 2단) · 「없음(충분)」 선택지 · 순서 seed 섞기(R-7) · confidence · p_max · 1·2위 비 기록(Q-5) | jev-research §2-3 · R-6 · R-7 |
| Sonnet 입력 | 걸음 순서대로 `{step, node, picked, facts[]{id, text, section}}` + `safety{}` + `claude_contract{allowed_fact_ids = 모은 fact id 전부}` · 걸음에서 안 받은 것은 넣지 않음(「정보 없음」은 Sonnet 이 말함) | README §2 |

#### 3-4-2. 앱이 쓰는 허브 계약(SPEC-005 v3.2 peek · expand — 정해지면 그대로 따름)

| 호출 | 앱이 넘기는 것 | 앱이 읽는 칸(최소) |
|---|---|---|
| `peek(node, intent?)` | 정본 id 하나 · intent | slim 카드 · 이웃은 **SPEC-005 §5-16 꼴을 따름(`neighbors_by_kind` · 종류별 `items[:8]` · intent 받음)** · `sections[]{name, n_facts, bytes}` · 안전 요약 · 응답 바이트(≤ 2KB 중앙 — 허브 끝 조건) |
| `expand(node, sections[] \| neighbor_ids[], intent?)` | 고른 섹션 이름 또는 이웃 id | `facts[]{id, text, section}` · 이웃의 slim 카드 · `claude_contract` |

- 새 도구인지 기존 도구(T3 `sections=` · T8 neighbors)의 모드인지는 SPEC-005 v3.2 가 실물 보고 정한다 — 앱은 `hub_rest.py` 에 `peek` · `expand` 두 함수만 두고 안이 바뀌어도 §3-4-1 은 그대로(§7-7 W-1)
- 걸음 예산 B 는 **`expand` 응답 바이트의 합**(peek · 안전 요약 · resolve 는 예산 밖) — 기록 `walk.bytes_total` · 걸음마다 `bytes`

#### 3-4-3. 되돌아가기(fallback) — v1 case3 경로 1회

Jev 가 시작 노드를 못 고르거나(②) · 첫 걸음 `peek` 가 실패하거나 · 걸음이 끝났는데 모은 fact 가 0 이면 **의도 기본 묶음 1회** = v1 §3-4 경로(의도 → 도구 표 · SPEC-005 §6-1 · `intent` 포함 · 의도 기본 묶음 · 동봉 그대로)를 한 번 부르고 Sonnet 에 넘긴다. 기록 `walk.fallback: true` · `fallback_reason` · 되돌아간 판은 비교 보고에서 따로 센다. 그 밖(걸음이 돌았고 fact ≥ 1)엔 되돌아가지 않는다 — Jev 가 고른 만큼만 답한다(설계의 뜻).

#### 3-4-4. 기록 · 측정

- `trace.walk{start_node, intent, steps[]{k, node, peek_bytes, peek_ms, jev{picked[], enough, confidence, p_max, ratio, ms, usage}, expand{sections[], neighbors[], bytes, ms, fact_ids[]}}, stop, steps_n, bytes_total, budget_hit, fallback, fallback_reason, jev_calls, jev_ms_total, hub_calls, hub_ms_total, fact_ids[]}` · `trace.hub` 는 되돌아간 판에만
- `stages[]`: `hub_resolve` · `jev#0` · `hub_peek#k` · `jev#k` · `hub_expand#k` · `claude`(되돌아가면 `hub_path`) — 첫 글자(`ttft_ms`)에 걸음이 주는 영향 = `claude` 시작 시각 − `t0`(걸음 합) · Jev 0.3초 × 걸음이 그대로 보임
- 비교 기준: 전 case3(10-31 rerun-v3 · 182문항 · `batch_id b202610311552-d39a4d`)과 **같은 182문항 · 같은 채점**(Claude CLI Opus 절대 · 같은 프롬프트 판) → `rerun_report` 전후 비교(통과율 · 「정보 없음」류 · 첫 글자 · 허브 바이트 — case3 허브 바이트 = `walk.bytes_total` + peek 합)

#### 3-4-5. (v1 경로 — 되돌아가기에서만 쓰는 정의)

```
t0 ─▶ ① hub_resolve: T1 resolve(질문 전체)                      [허브 REST · 결정론]
      ② jev: 의도 Choice + 슬롯 Choice(한 요청에 병렬)           [Jev 1회 · 255 넘는 슬롯만 2단]
      ③ hub_path: 의도별 골드 도구 경로 1번                       [허브 REST]
      ④ claude: Sonnet 1회(③ 결과 + 낮은 신뢰 슬롯 표시)         [스트리밍]
```

| 단계 | 규칙 | 근거 |
|---|---|---|
| 시작 때 1회 | T9 vocab(고민 · 부위 · 목적 · 확인 조건 · 기법 · 계열 · 의도 · 메뉴)을 받아 캐시 · 질문당 단계에서 뺌(기록엔 `hub_list: "cache"`) | 10-30 Q-7 · SPEC-005 §5-10 |
| ① 사전 검색 | T1 resolve(질문 전체) → `candidates` · `menu_candidates` · `unmatched`. **질문마다 늘 부른다** — 시술 · 제품 슬롯(255 넘음)은 ① 후보 없이는 Choice 선택지를 만들 수 없고, 질문이 시술 슬롯을 말하는지는 ① 을 해 봐야 안다(Q-4). 255 이하 슬롯만 쓰는 질문에도 부르므로 그 시간은 `stages[]` 의 `hub_resolve` 로 따로 남겨 `jev` · `hub_path` · `claude` 와 나눠 비교한다(검수 W-7) | SPEC-005 §5-2 · 10-30 Q-4 |
| ② 의도 | Choice 하나 — 선택지 = 의도 12(SPEC-005 §5-1 의도 열 · gold-research 의도 I-01~I-12) · `criteria` 설명 = 의도 이름 · 예시 질문 | D-08 · gold-research §3 |
| ② 슬롯 | 슬롯마다 Choice 하나 — 슬롯 = T9 vocab 종류(고민 · 부위 · 목적 · 확인 조건 · 기법 · 계열 · 메뉴) + 시술 · 제품. **중증도 슬롯은 없다** — 허브 vocab(SPEC-005 §5-10)에 중증도 종류가 없고, 7단계가 중증도를 하위 고민으로 옮겼다(R18 · J12 — 주름 초기 · 경미 → P2-3 잔주름 · 중기 · 중등도 · 심화 · 중증 → P2-2 깊은주름 · `step7-concerns.md`) — D-08 의 「중증도」는 고민 슬롯이 덮는다(검수 W-6). 선택지 = vocab 노드(이름 + 동의어 몇 개를 설명으로 · 한국어만). **선택지가 255 를 넘는 슬롯**(시술 · 제품: 단위 시술 162 + 제품 354 + 계열 27)은 ① 의 후보로 줄인 뒤 Choice(10-30 Q-4) · 「해당 없음」 선택지 + 짝 Noul(「질문이 이 슬롯 값을 말하나」) | 10-30 Q-4 · jev-research §2-3 |
| ② 여러 고민 | Choice 는 하나만 고른다 → R-6(① 후보 고민마다 Noul) | jev-research §2-3 |
| ② 선택지 순서 | 섞고 seed 기록(앞쪽 기울기) | jev-research §2-3 「순서 또는 seed 기록」 → R-7 |
| ② 신뢰도 | 슬롯 · 의도마다 `confidence` · `p_max` · 1·2위 비 기록 · `confidence < 0.3` 이면 `low_confidence` 표시 | 10-30 Q-5 · jev-research §2-2 |
| ③ 경로 | **의도 → 도구 = SPEC-005 §6-1 의도 → 도구 대응 그대로**(① T1 은 이미 부름). 이 스펙에 옮겨 적은 꼴: I-01 → T2 recommend(`concerns` · `site` · `cc` — T1 `candidates` 의 concern · site 만) · I-02 · I-03 · I-04 · I-05 · I-10 → T3 procedure_card(의도별 `sections`) · I-06 → T6 compare · I-07 · I-08 → T4 pair_check(**I-07 자기 쌍 = 같은 id 두 번** — SPEC-005 §5-5) · I-09 → T5 check_conditions(**확인 조건 노드가 안 잡히는 질문(「통증 민감」 꼴)은 T3 `sections=overview,ops`**) · I-11 → T7 combos(`menu_candidates` 는 여기만 · 질문 말이 라벨이면 `menu` · 아니면 `concern`) · I-12 가격 → 허브 도구 없음(연결 층 · 이 실험 밖 — Sonnet 에 「가격 정보 없음」만 줌). SPEC-005 §6-1 이 바뀌면 그쪽을 따른다(검수 W-2) | SPEC-005 §6-1 · §5-1 · §5-5 · gold-research §3 |
| ③ 필수 슬롯 없음 | 그 의도의 필수 슬롯(SPEC-005 도구 필수 입력)이 비면 도구를 부르지 않고 「되묻기 필요」로 Sonnet 에 넘김 | D-08 「신뢰도 낮은 슬롯은 되묻기」 |
| ④ Sonnet | 1회 · 도구 없음 · 입력 = 질문 + ③ 결과 JSON + 슬롯 표(낮은 신뢰 표시 포함) | README §2 |

- 기록 `trace.jev{model, intent{choice, confidence, p_max, ratio}, slots{…}, noul{…}, option_order_seed, usage}` · `trace.hub{resolve, path, tool, input, node_ids[]}`
- Jev 실패(401 · 422 · 429/529 재시도 끝 · 시간 초과): 그 열을 오류로 기록하고 다른 두 열은 계속(jev-research §2-4)

### 3-5. 도구 결과 전달 보장(v2 · B-1)

**문제(2차 분류 `fail-triage2.md` §5)**: case2(Claude CLI) 200 응답 614 중 100 호출이 모델에겐 전체보다 작게 전달됐다 — 기록 `output_bytes` 중앙 1,815B vs 허브 전체 중앙 88,671B · 도구별 check_conditions 47 · procedure_card 23 · pair_check 17 · compare 7 · recommend 6 · 잘린 호출이 든 case2 실패 행 56/131(B 35 · C 7). rerun-v3 기록(182문항 · 672 호출)에서 `output_bytes` 1,700~2,300B 가 93건(1,774B 19건 · 1,795B 8건 …)으로 뭉친다 = CLI 가 넘긴 **미리보기** 크기.

**실물 조사(11-01 · 설정까지 · 호출은 WORK-006 WP-0 확인 시험)**:

| 쪽 | 자르는 규칙(실물 · 문서) | 올리는 설정 | 출처 |
|---|---|---|---|
| Claude CLI 2.1.284 | ① MCP 도구 결과 10,000 토큰 넘으면 경고 · **25,000 토큰 기본 상한**(`MAX_MCP_OUTPUT_TOKENS`) ② 그와 **별개로 성공 텍스트 결과가 저장 문턱(글자 수)을 넘으면 파일로 저장**하고 모델에는 약 2KB 미리보기만 — 바이너리(2.1.284)에서 확인된 것: env `MAX_MCP_OUTPUT_TOKENS` · 기본 상수 `P=25000` · 도구 `_meta` 키 `anthropic/maxResultSizeChars` · `persistenceThresholdCeiling` 칸 · 저장 경로 `tool-results/mcp-<name>-blob-…` · 마커 「Output too large (」 · 「). Full output saved to:」 · 「exceeds maximum allowed tokens. Output has been saved to」 · 「Preview (first」 + 변형 3 「Output truncated (… KB total). The full output could not all be saved to」 · 「(… KB total): later output was discarded because this session writes no files」(**`--no-session-persistence` 일 때 — 저장 자체가 안 됨**) · 「Output exceeded the persist limit; only the first … were saved to」. 문턱 「약 50,000 자」 · 「250,000 자까지」 는 공식 문서 · #97622 인용값이고 바이너리에서 숫자를 특정하지 못함 → **WP-0 실측 표 「문턱 실측값」 열로 닫는다**(W-3) · 글자 수 기준 · `MAX_MCP_OUTPUT_TOKENS` 로 안 올라감(문서) ③ **서버가 도구 정의 `_meta["anthropic/maxResultSizeChars"]` 를 주면 그 도구의 저장 문턱이 그 값으로 올라감**(250,000 자까지 실측 보고) | ①: 자식 env `MAX_MCP_OUTPUT_TOKENS` · ③: 허브 MCP 도구 meta(서버 쪽 · `mcp` 2.3 `MCPServer.tool(meta=…)` 지원 확인 11-01) | 공식 문서(code.claude.com/docs/en/mcp 「Unless the server raises a tool's own limit, successful text results longer than 50,000 characters are saved to a file regardless of this variable」) · anthropics/claude-code #97622(2.1.283 실측) · #45770 |
| Codex CLI 0.166.0 | 도구 결과를 **토큰 예산**으로 자른다(바이너리에 `tool_output_token_limit` · `output_token_limit` 키 있음). 잘림 표시 **실물 후보 5(0.166 바이너리 문자열)**: 「Warning: truncated output (original token count:」 · 「<truncated omitted_approx_tokens=」 · 「omitted_due_to_size_limit (overage_bytes=」 · 「 bytes omitted ...」 · 「 tokens truncated」 + 구조 칸 `_codex_executed_tool_call_truncated{original_bytes, max_bytes, omitted_calls}`. 옛 이슈의 「[... output truncated to fit」 · 「[... omitted k of n lines」 는 0.166 에 **없음**(쓰지 않는다). 어느 것이 실제로 나오는지는 WP-0 에서 한도를 일부러 작게 한 호출로 받아 고정 | `-c tool_output_token_limit=<n>`(전체) · `-c mcp_servers.hub.tools.<도구>.output_token_limit=<n>`(도구별 · 20% 직렬화 여유 앞 값 · 0.152+) | 공식 config 참조(learn.chatgpt.com config-reference) · openai/codex #5913 · #14206 |
| 앱(관찰) | rerun-v3 case2 에 `bash` 호출 10건(Q078 · Q105 · Q150 · Q161 · Q165 · Q166 · Q170 · Q171 · Q174 · Q202 — 전부 저장된 `tool-results` 파일을 `grep` · `jq` · `cd` 로 읽으려 함 · 전부 `is_error` · 68B) — `--tools ""` 로 Bash 가 꺼져 있어도 모델이 미리보기의 파일 경로를 보고 시도했다. 공정성 · 격리 둘 다에 흔적을 남긴다 | §4-2 `stray_tool` 기록 · 끝 조건 0 | rerun-v3 기록 |

**결정 — (a) 설정으로 한도를 올려 허브 응답 전체를 모델에 그대로 넘긴다.** 세 후보 중 하나:

| 후보 | 판정 | 근거 |
|---|---|---|
| **(a) CLI · 도구 한도 설정** | **채택** | 모델이 받는 바이트 = 허브 응답 전체(10-30 결정 「입력 상한 셋 다 없음」과 같은 뜻) · 두 CLI 모두 공식 설정이 있다(Claude = 도구 meta + env · Codex = config 키) · 앱에 새 부품 없음 · case3 가 프롬프트로 전체를 받는 것과 같은 조건. 조건: 허브 MCP 도구 12(골드 9 · 원장 3)에 `_meta["anthropic/maxResultSizeChars"] = MCP_RESULT_MAX_CHARS`(SPEC-005 §5-0 · §5-12 한 줄 — v3.2 planner 에 전달 · §7-7 W-2) · 자식 env `MAX_MCP_OUTPUT_TOKENS`(같은 값을 토큰으로 — 200,000) · Codex `tool_output_token_limit`(200,000) · **WP-0 확인 시험**(실물 호출 1회씩 · 코디 승인)에서 잘림 0 이어야 채택이 선다 — FAIL 이면 escalation(자동으로 (b) 로 가지 않음) |
| (b) 앱 쪽 MCP 프록시가 결과를 나눠 `page=` 로 이어 주기 | 닫음 | 모델이 다음 페이지를 **부를지 말지 고르게** 된다 → 「전체를 받는다」 보장이 모델 행동에 기댐 · 왕복 · 비용 증가 · case3(프롬프트로 한 번에) 와 조건이 달라짐 · 새 부품(프록시 · 캐시) · 페이지마다 50,000 자 · 25,000 토큰 둘 다 아래여야 해 한국어 JSON 이면 페이지 수가 큼. (a) 가 확인 시험에서 서면 필요 없다 |
| (c) 모델에 Read 도구 허용(저장 파일 경로) | 닫음 | Claude 전용(Codex 에 같은 경로 없음 → 두 provider 조건 불일치) · 모델이 읽을지 말지 고름 · 파일 도구 = 격리 깨짐(위 `bash` 10건이 바로 이 길) · `--no-session-persistence` 때 저장 경로 보장 없음 |

- **전달 보장 정의**: 허브 호출마다 `delivered_bytes`(모델이 받은 도구 결과 바이트 = 지금 `output_bytes` 의 뜻을 이 이름으로 명확히 · `output_bytes` 는 호환 칸으로 같은 값) = `hub_bytes`(같은 입력으로 허브가 돌려준 전체 바이트 — §4-4 검증 스크립트가 재호출로 셈 · 결정론) 이고 `truncated: false`. `truncated` 판정은 **마커 목록 = 설정 상수 `TRUNCATION_MARKERS`**(provider 별 문자열 목록 · 위 표의 Claude 4 + 변형 3 을 넣고 시작 · Codex 는 실물 후보 5 를 넣고 시작 · **WP-0 확인 시험이 실제로 나온 문자열로 고정** — 상수는 `config.py` · 기록 `settings.truncation_markers_sha`)로 앱이 결정론으로 매긴다 · 판정 뒤 `delivered_bytes < hub_bytes` 인데 마커가 없으면 `truncated: "unknown"`(끝 조건에선 잘림으로 셈)
- 원장 MCP 3(case1)도 같은 meta · 같은 env — `raw_get` 의 `max_bytes` 20,000(SPEC-005 §5-12) 은 허브 쪽 응답 규칙이라 그대로(모델이 더 읽으려면 offset 으로 — 그건 「자른 것」이 아니라 「도구 계약」)
- SDK 판: `TOOL_RESULT_MAX_BYTES=0`(없음)으로 두 판을 같게(§2-5)

### 3-6. intent 전달(v2 · B-1)

- 2차 분류: case2 허브 호출 662 중 Claude 가 `intent` 를 넘긴 호출 **14(2.1%)** · case3 는 앱이 전부(159/159). 허브 v3 는 `intent` 가 없으면 도구 기본 의도로 묶음 · 동봉을 붙이므로(SPEC-005 §5-0) case2 는 질문 의도와 다른 묶음을 받고 있었다
- **규칙**: ① `prompts/case2.md` 에 한 줄 — 「허브 도구를 부를 때마다 `intent` 를 반드시 넘긴다 · 의도 표: I-01 고민 → 추천 · I-02 시술 설명 · I-03 주의 · 사후관리 · I-04 부작용 · 합병증 · I-05 회복 · 효과 기간 · I-06 비교 · I-07 같이 · 순서 · 간격 · I-08 이전 시술 뒤 가능? · I-09 나한테 해도 되나(확인 조건) · I-10 용량 · 회차 · 제품 · I-11 추천 조합 · I-12 가격」(SPEC-005 §5-1 의도 열 그대로 · 프롬프트 판 sha 바뀜 → `versions.prompts.case2`) ② 허브 MCP 도구 설명 · 스키마의 `intent` 를 「선택」에서 「반드시 넘김 · 의도 표」로(스키마 자체는 허브 — SPEC-005 §5-0 · v3.2 planner 에 전달 · §7-7 W-2 · 필수(required)로 만들지는 허브가 정함 — 앱 끝 조건은 비율로) ③ case1 원장 도구 3 은 `intent` 가 없다(해당 없음) ④ Codex 판도 같은 프롬프트 줄
- **기록**: `tool_calls[].intent_passed: true|false|null` — 스키마에 `intent` 가 있는 도구만 true/false · 없으면 null · **true 는 값이 I-01~I-12 에 들 때만**(`"none"` · 빈 값 · 그 밖 문자열은 false — rerun-v3 의 14 중 2 가 `"none"` 이었고 허브는 모르는 값을 4xx 로 냄 · W-5) · 틀린 값은 `intent_values{}` 에 그대로 셈 · 판마다 `trace.intent_ratio = passed / 해당 호출` · `intent_values{}` · 보고서(`report` · `rerun_report`)에 「intent 전달 비율」 열(케이스 · provider 별)

### 3-7. 공정성 원칙(v2)

세 케이스 · 두 CLI · SDK 판이 **모델에 주는 허브 자료의 양과 전달**을 같은 규칙으로 한다. 10-30 「입력 상한 CLI 판 셋 다 없음」 을 이 조항으로 정리한다.

| 원칙 | 값 | 어디서 |
|---|---|---|
| 허브 바이트 상한 | **없음**(세 케이스 · 두 판 같음) — 양은 허브 응답 규칙(SPEC-005 slim · sections · 상한)과 모델의 선택(case1 · 2 도구 호출 · case3 Jev 걸음)이 정한다 · 앱은 자르지 않는다 | §2-5 · `TOOL_RESULT_MAX_BYTES=0` · `input_cap_bytes: null` |
| 전달 보장 | 허브가 돌려준 바이트 = 모델이 받은 바이트(§3-5) · 세 케이스 · 두 CLI · SDK 판 전부 | §3-5 설정 · §4-4 검증 |
| intent | 허브 호출마다 의도를 넘긴다 — case2 는 모델이(프롬프트) · case3 는 앱이(Jev 의도) · case1 해당 없음 | §3-6 |
| 모델 · effort · thinking · 프롬프트 공통부 · 시작 `t0` | 같음(§3-1 · §2-5) | — |
| 걸음 예산(case3 걸음) | B 는 **Jev 가 고르는 양의 상한**이지 잘라 내는 상한이 아니다 — expand 를 통째로 넣거나 뺀다(§3-4-1) · 비교 보고에 `bytes_total` 을 case1 · 2 도구 결과 합과 나란히 | §3-4 |
| 격리 | 모델이 허브 도구 밖 도구를 부른 호출(`stray_tool`)은 0 이어야 함 · 있으면 그 판은 「격리 깨짐」 표시 | §4-2 · §7-6 |

## 4. 속도 측정 · 기록 꼴

### 4-1. 속도 칸

| 칸 | 정의 |
|---|---|
| `t0` | 서버가 질문을 받은 시각(세 케이스 같은 값 · `perf_counter` 기준) |
| `ttft_ms` | `t0` → 그 케이스 Sonnet 스트림의 **첫 `text_delta`** 도착(thinking 델타 제외 · 어느 바퀴든 처음 나온 글자) — 10-30 Q-3 |
| `ttft_answer_ms` | `t0` → 마지막 Sonnet 호출(답 바퀴)의 첫 `text_delta` — case2 는 도구 바퀴 앞 글이 있을 수 있어 같이 남김 |
| `total_ms` | `t0` → 답 스트림 끝 |
| `stages[]` | `{name, start_ms, end_ms, tokens?}` — case1 · 2: `claude#n` · `tool:<이름>#n` / case3: `hub_resolve` · `jev` · `hub_path` · `claude` (`start_ms` · `end_ms` 는 `t0` 기준) |
| `llm_round_trips` | Sonnet 호출 수(+ case3 는 `jev_calls` 따로) |
| `tokens` | 단계별 Anthropic `usage`(input · output · cache_creation · cache_read) · Jev `usage.input_tokens` |

- 단건 값은 편차가 크다 — 결론은 쌓인 기록의 경향으로 본다(README §3). 「같은 질문 다시」 버튼(§6 · R-8)

### 4-2. 기록 꼴(한 질문 = `runs/runs.jsonl` 한 줄)

README §6 꼴에 아래를 더한다.

```json
{
  "run_id": "…", "asked_at": "…", "question": "…",
  "versions": {
    "answer_model": "claude-sonnet-5-5", "judge_model": "claude-opus-5-5", "extract_model": "…",
    "jev_model": "jev-1.14.0",
    "prompts": {"common": "<sha12>", "case1": "…", "case2": "…", "case3": "…", "judge": "…", "extract": "…"},
    "gold_build_hash": "<골드 응답 머리 build.build_hash>",
    "raw_manifest_sha16": "<원장 MCP 응답 머리 raw.dir_manifest_sha16>",
    "app_commit": "<clinic_chat git sha>"
  },
  "settings": {"thinking": "between_tools", "effort": "high", "tool_loop_max": 12, "jev_confidence_min": 0.3, "jev_option_order_seed": 0},
  "cases": {"case1": {"answer": "…", "stop_reason": "…", "loop_capped": false, "error": null,
                      "timing": {"ttft_ms": 0, "ttft_answer_ms": 0, "total_ms": 0, "stages": [], "llm_round_trips": 0},
                      "tokens": {}, "trace": {}, "word_check": {}, "judge": {}}, "case2": {}, "case3": {}},
  "judge_order": ["case2", "case1", "case3"], "judge_seed": 0
}
```

- **v2 칸**: `provider` · `versions.answer_provider · answer_effort · cli_version · auth_kind · judge_provider` · `settings{thinking, effort, tool_loop_max, max_budget_usd, service_tier, timeout_sec, input_cap_bytes: null, mcp_result_max_chars, walk_max_steps, walk_byte_budget, walk_enough_min}` · case1 · 2 `trace.tool_calls[]{tool, input, delivered_bytes, output_bytes(같은 값 · 호환), hub_bytes?(§4-4 가 채움), truncated: false|true|"unknown", intent_passed, ms, is_error, node_ids[], stray: bool}` · `trace.intent_ratio` · `trace.stray_tools: int` · `trace.cli{…}`(§2-5 · `rate_limits` · `api_retries` · `session_tools` · `mcp_servers` · `observed_model` · `api_key_source` · `num_turns` · `cli_ttft_ms`) · case3 `trace.walk{…}`(§3-4-4) · `timing.ttft_kind · cli_boot_ms · thinking_ms · ttft_ms_ex_boot · total_ms_ex_boot` · `cost{usd, usd_estimate, billed}` · `judge.mode: "absolute"` · 배치 칸(§2-5)
- 사람 확인은 `runs/human_checks.jsonl` 에 따로 덧붙임(`{run_id, case, verdict: "맞음|틀림", item?, note, at}`) — 기록 줄은 고치지 않는다
- 기록에 키 · 환경 변수 값을 넣지 않는다

### 4-3. 서버 ↔ 화면 계약(SSE)

`POST /api/ask {question}` → `{run_id}` · `GET /api/runs/{run_id}/events`(SSE) 이벤트: `stage{case, name, start_ms, end_ms}` · `text{case, delta}` · `trace{case, …}` · `case_done{case, timing, tokens}` · `word_check{case, …}` · `judge{cases…}` · `run_done{run_id}` · `error{case?, message}` / `GET /api/runs?limit=` 기록 목록 · `POST /api/runs/{run_id}/human_check` · `POST /api/runs/{run_id}/rerun`

### 4-4. 기록 검증 스크립트(v2 · 결정론)

`clinic_chat/verify_runs.py`(레포 안 · 출력은 레포 밖 `build-out/verify-<batch>.{md,json}`): 배치 하나(또는 run_id 목록)를 읽어 **판단 없이** 센다 · 두 번 돌리면 바이트 같음(시간 칸은 머리 하나).

| 항목 | 셈 | 끝 조건에 쓰는 값 |
|---|---|---|
| 잘림 | case1 · 2 `tool_calls[]` 마다 `truncated`(마커) · `hub_bytes` = **같은 입력으로 허브 재호출**(REST · `intent` 포함 · 결정론 · 허브 빌드 해시가 기록과 같을 때만 · 다르면 「대조 불가」) · `delivered_bytes ≠ hub_bytes` 셈 | 잘린 호출 수 · 대조 불가 수 |
| intent | 스키마에 `intent` 있는 도구 호출 중 `intent_passed` 비율(케이스 · provider · 도구별) | ≥ 95% |
| 격리 | `stray_tools` 합 · 허브 MCP 밖 도구 이름 목록 | 0 |
| case3 걸음 | `walk.steps_n` · `bytes_total` · `stop` 분포 · `fallback` 수 · Jev 호출 수 · ms 합 · peek 바이트 중앙 | 보고 · 되돌아간 판 수 |
| 공정성 | 케이스별 모델이 받은 허브 바이트 합(case1 · 2 `delivered_bytes` 합 · case3 `bytes_total` + peek 합) 중앙값 나란히 | 보고 |
| C 비율 | 채점 실패 행마다 fail-triage2 §2 와 같은 셈 — 그 문항의 허브 응답(도구 결과 · 걸음 fact) `facts[].text` 정규화 문자열 ∋ 인용 → C · 케이스 · provider 별 C 건수 · 비율(실패 행 대비) | 보고(교체 동기 「C 10%」 대조 · W-2) |

## 5. 품질 두 층

세 열이 모두 끝나면 ① → ② 순서로 자동(README §5).

### 5-1. ① 단어 검사(결정론 판정)

| 단계 | 규칙 | 근거 |
|---|---|---|
| 이름 뽑기 | LLM 추출(R-4 — `claude-opus-5-5` · effort `low` · 구조화 출력 `output_config.format` 으로 `{names: [{text, kind: 시술\|제품\|장비\|부위\|성분}]}`) · 답 원문만 입력 · **시맨틱 사전 · 원장을 주지 않음**(지어낸 이름을 놓치지 않게) | README §4 ① 1 · O-4 |
| 정규화 | **`semantic.json` `dictionary.resolve_rules.normalize` 그대로** — NFKC → 라틴 악센트 접기(NFKD 결합 부호 제거 · NFC) → 입력 접기 `fold`(「쳐짐」 → 「처짐」) → 공백 제거 → 괄호 `strip_chars`(`()[]`) 지움(안 글자는 남김) → **전부 소문자**. 답에서 뽑은 이름 · 원장 문자열 · 사전 `expr` · `variants` 에 **같은 함수 하나**를 쓴다(`fold` · `strip_chars` 는 `SEMANTIC_JSON` 에서 읽음 — 문서 = 코드). 「영문으로 시작하면 소문자」(README §4 ① 2 · 3단계 lexicon 문구)는 쓰지 않는다 — 한글로 시작하고 영문 대문자가 섞인 원장 문자열(실물 290개 · 예 「필러(HA/CaHA)」 · 「…Nd:YAG)」)이 소문자로 안 바뀌어 거짓 「없는 이름」이 나기 때문(검수 F-1) | `semantic.json` `dictionary.resolve_rules`(note: 사전은 이 규칙 하나) · `semantic.md` §4 · `semantic-build.py:55-63` |
| 대조 | 원장 21 파일의 모든 문자열 값(정규화 뒤)에 그 이름이 부분 문자열로 있나 → 없으면 시맨틱 사전 `dictionary.expressions[].expr · variants[]`(정규화 뒤)와 같은가 | README §4 ① 3 |
| 출력 | 이름마다 `{name, norm, found, where[] (원장 파일 · 경로 · 최대 3), via: "원장\|사전"}` · 열마다 `not_found` 수 | README §4 ① 4 |
| 결정론 | 대조는 결정론 · 뽑기 결과(LLM)는 기록에 그대로 남겨 다시 대조 가능 | — |

- 2자 미만 이름은 대조에서 뺌(부분 일치 거짓 「있음」 방지) — R-4
- 원장은 `RAW_DIR` 로컬 파일을 직접 읽는다(허브 원장 MCP 를 부르지 않음 — 채점 경로가 실험 대상 서버에 기대지 않게) · 시작 때 21 파일 해시를 기록 `raw_manifest_sha16` 과 같은 식으로 셈

### 5-2. ② Opus 채점

| 항목 | 묻는 것 | 값 |
|---|---|---|
| 정확성(관계 · 숫자) | 시술 ↔ 부위 ↔ 고민 관계 · 간격 · 용량 숫자가 원천과 맞나 | 통과 · 실패 · 해당 없음 |
| 안전 정보 | 추천한 시술의 금기 · 주의를 같이 말했나(10-26) | 〃 |
| 후보 처리 | 뜻이 갈리는 말을 단정하지 않고 고르거나 되물었나(10-27) | 〃 |
| 불확실 표시 | 근거 약 · 정보 없음을 「안전함」 · 「확실함」처럼 말하지 않았나 | 〃 |
| 질문에 답함 | 물은 것에 답했나 · 새지 않았나 | 〃 |

- 항목 = README §4 ② 5개 그대로(O-5 → R-9 「5개 그대로 시작」). 「지어낸 말」은 ① 몫
- **가리기**: 세 답을 seed 로 섞어 A · B · C 로만 보여 줌 · case 이름 · 도구 흔적 · 속도 안 보임 · `judge_order` · `judge_seed` 기록
- **기준 자료(O-3 → R-10 = B 원장)**: Opus 에 원장 도구 3(`raw_list` · `raw_get` · `raw_search`)을 준다 — 원장 전체를 넣지 않고 필요한 곳만 찾아 읽음(README 의 B 「크기 문제」를 도구로 풂) · 골드 결과는 주지 않음(C 는 case2 · 3 에 유리)
- **원장 도구는 앱 안 로컬 구현**(`quality/raw_tools.py`): SPEC-005 §5-12 R1~R3 과 같은 이름 · 입력 · 출력 계약 · `RAW_DIR` 로컬 원장 파일을 읽는다 · 허브 원장 MCP 를 부르지 않는다 — ① 과 같은 이유(채점 경로가 실험 대상 서버에 기대지 않게 · 기준 하나 · 검수 W-3). case1 이 쓰는 허브 원장 MCP 와 계약이 같은지는 WORK-004 Phase 7 실물 대조에서 확인
- **근거 인용 필수**: 실패마다 `{item, answer: A|B|C, claim, evidence: {file, path, quote}}`. 앱이 `quote` 가 그 경로 원문에 실제로 있는지 원장 로컬 파일로 확인 → 없으면 그 실패는 `invalid`(무효 · 화면에 회색)
- 호출: `claude-opus-5-5` · thinking 기본(Opus 5.5 는 못 끔) · effort `medium` 명시(기본값) · `tool_choice: auto` · 도구 루프(상한 `CASE_TOOL_LOOP_MAX`) 뒤 마지막 응답을 구조화 출력(`output_config.format`)으로 받음
- **사람 확인**: 열마다 「맞음 · 틀림」 + 메모(README §4 「처음 몇 건은 사용자가 채점관 검수」) — §4-2 `human_checks.jsonl`

## 6. 화면

README §5 와이어 그대로 + 질문 기록 목록.

```
┌────────────────────────────────────────────────────────────┐
│ ⚠ 환자 정보 넣지 말 것 · 질문과 노드 이름이 Jev(미국)로 나감   │
│ 질문 [                                          ] [보내기] │
├──────────────────┬──────────────────┬──────────────────────┤
│ case1 원장 MCP   │ case2 골드 MCP   │ case3 골드 + Jev     │
│ ⏱ 첫 글자 / 전체 │ ⏱ 첫 글자 / 전체 │ ⏱ 첫 글자 / 전체     │
│ ▓▓ ▓ ▓▓ 왕복     │ ▓▓ ▓ ▓▓ ▓▓ 왕복  │ ▏hub ▓ jev ▏hub ▓▓ claude │
├──────────────────┼──────────────────┼──────────────────────┤
│ [답변 스트리밍]  │ [답변 스트리밍]  │ [답변 스트리밍]      │
├──────────────────┼──────────────────┼──────────────────────┤
│ ▸ 원장 도구 N    │ ▸ 도구 호출 N    │ ▸ Jev 의도 · 슬롯    │
│   입력 · 결과    │   입력 · 결과    │   confidence(낮음 ⚠) │
│   토큰 수        │   쓴 노드 id     │ ▸ 허브 경로 · 노드 id│
├──────────────────┼──────────────────┼──────────────────────┤
│ ① 없는 이름 N    │ ① 없는 이름 N    │ ① 없는 이름 N        │
│ ② 항목별 ●/✕     │ ② 항목별 ●/✕     │ ② 항목별 ●/✕         │
│   (실패 근거)    │                  │                      │
│ [사람 확인 ✓✗]   │ [사람 확인 ✓✗]   │ [사람 확인 ✓✗]       │
└──────────────────┴──────────────────┴──────────────────────┘
  [같은 질문 다시 ×3]
  ↓ 질문 기록 — 한 줄씩: 시각 · 질문 · 열별 total_ms · 없는 이름 수 · ② 통과 수 · 사람 확인 · 판(골드 해시 앞 8자)
```

- 단계 막대 = `stages[]` 를 `t0` 기준 가로 시간축으로(열마다 같은 눈금)
- 기록 줄을 누르면 그 질문의 3열을 기록에서 다시 그림(다시 호출 안 함)
- 얼굴 지도 패널 없음(README §5)

## 7. 열린 것 처리표

### 7-1. README 열린 것 O-1~O-9

| # | 무엇 | 처리 | 근거 · 값 |
|---|---|---|---|
| O-1 | case1 원장 넣는 방식 | **결정됨** — 원장 MCP 도구 3 | 10-30 Q-1 · 「원장도 MCP 로」 |
| O-2 | 세 케이스 시스템 프롬프트 | **결정됨** — R-5 | README 선택지 「답 문장 지시는 같게 · 데이터 · 도구 설명만 다르게」 |
| O-3 | Opus 기준 자료 | **결정됨** — R-10(B 원장 — 앱 안 로컬 원장 도구로) | README 「논의에선 B 기본」 |
| O-4 | ① 이름 뽑기 방법 | **결정됨** — R-4(LLM 추출 · Opus 5.5) | README 선택지 |
| O-5 | 품질 항목 최종 목록 | **결정됨** — R-9(5개 그대로) | README §4 ② |
| O-6 | Jev 호출 꼴 | **결정됨** — 이 스펙 §3-4(의도 12 · 슬롯 = SPEC-005 vocab · 도구 입력) · 세부 값 R-6 · R-7 | SPEC-005 §5 · Q-4 · Q-5 · Q-7 |
| O-7 | 허브 도구 목록 · 의도별 경로 | **결정됨** — SPEC-005 §5(도구 9 · 경로) · §5-12(원장 3) | SPEC-005 |
| O-8 | 화면 · 실행 위치 | **결정됨** — 레포 `kknaks/clinic_chat`(공개 · §2-3 경로) · 스택 R-1 | 10-30 |
| O-9 | 모델 키 | **결정됨** — 사용자 보유 · env 로만 · Claude 는 API 키 별도 | D-11 · 10-30 |

### 7-2. Jev 조사 Q-1~Q-8(10-30 사용자 「응」 — 전부 결정됨)

| # | 결정 | 이 스펙 |
|---|---|---|
| Q-1 | case1 = 원장 MCP | §3-2 |
| Q-2 | Anthropic Python SDK + MCP 클라이언트 직접 루프 | §2-1 |
| Q-3 | ttft = 첫 텍스트 델타 · thinking 끔(세 케이스 같게) | §3-1 · §4-1 |
| Q-4 | 255 넘으면 허브 사전 검색으로 후보 줄인 뒤 Choice | §3-4 |
| Q-5 | 되묻기 문턱 0.3 시작 · 기록 보고 조정 | §3-4 · env `JEV_CONFIDENCE_MIN` |
| Q-6 | `jev-1.14.0` 고정 | §2-1 · env |
| Q-7 | 노드 목록 앱 시작 1회 캐시 | §3-4 |
| Q-8 | 영어 병기 안 함(처음) | §3-4 슬롯 설명 한국어만 |

### 7-3. R-1~R-10 — 결정됨(10-30 사용자 승인)

이 스펙이 추천한 값을 사용자가 10-30 한 번에 승인했다. 다시 논의하지 않는다(값 조정은 기록을 보고 사용자가 정함).

| # | 무엇 | 결정 | 이유 |
|---|---|---|---|
| R-1 | 서버 · 화면 스택 | FastAPI + SSE + 빌드 없는 정적 페이지 | 화면 하나 · 로컬 · 실행 명령 하나 · 의존성 적음 |
| R-2 | case1 · 2 도구 루프 상한 | Sonnet 호출 12번 · 닿으면 `tool_choice none` 으로 마지막 답 1번 + `loop_capped` | 무한 루프 · 비용 막기 · 셈은 기록으로 조정 |
| R-3 | Sonnet effort | `high`(모델 기본값 명시) · 세 케이스 같음 | `between_tools` 가 high 이하만 받음 · 기본값이면 따로 고른 것이 없음 |
| R-4 | ① 이름 뽑기 | `claude-opus-5-5` · effort low · 구조화 출력 · 2자 미만 제외 | 이미 정해진 채점 모델 — 새 모델을 들이지 않음 · 답 모델(Sonnet)과 달라 자기 답 편들기 없음 |
| R-5 | 프롬프트 | 공통부 같음 + 케이스별 데이터 · 도구 설명만 | README O-2 선택지 |
| R-6 | 여러 고민 슬롯 | 고민 Choice 1 + ① 후보 고민마다 Noul(0.5 이상이면 더함) | Choice 는 하나만 고름(jev-research §2-3 문서 패턴) |
| R-7 | Jev 선택지 순서 | seed 로 섞고 기록 | 앞쪽 기울기(jev-research §2-3) |
| R-8 | 같은 질문 다시 | 버튼 · 3회 · 중간값 표시 | README §3 「필요하면 재실행 버튼(중간값)」 |
| R-9 | 품질 항목 | README 5개 그대로 시작 | O-5 |
| R-10 | Opus 기준 자료 | B 원장 — 원장 도구 3 을 Opus 에 줌 · **도구는 앱 안 로컬 구현**(SPEC-005 §5-12 R1~R3 과 같은 계약 · `RAW_DIR` 로컬 원장 파일 · 허브 원장 MCP 안 부름) | README 「B 기본」 · 크기 문제를 도구 조회로 풂 · C 는 골드 쪽에 유리 · ① 과 같이 채점이 실험 대상 서버에 기대지 않게(검수 W-3 · 코디 판단) |

### 7-4. 사용자 몫

| # | 무엇 | 왜 사용자만 |
|---|---|---|
| U-1 | Jev 콘솔 접근 · 키 발급(`console.typesafe.ai`) · 조직 rate limit 확인 | **완료(10-30)** — 키 받음 · 사용자가 워크트리 `.env` 에 직접 넣음 |
| U-2 | Anthropic API 키를 `.env` 에 넣기(충전된 API 키 · 구독 아님) | **완료(10-30)** — 키 받음 · 사용자가 워크트리 `.env` 에 직접 넣음 |
| U-3 | R-1~R-10 승인 · 바꿈 | **완료(10-30)** — 승인(§7-3) |
| U-4 | 실험 중 사람 확인 표시 · 문턱(0.3) 조정 판단 | README §4 · 10-30 Q-5 「기록 보고 조정」 — 실험하면서 |

### 7-5. 남은 열린 것

| # | 무엇 | 선택지 | 지금 |
|---|---|---|---|
| L-1 | 실험 기록(`runs.jsonl` · `human_checks.jsonl`) 저장 위치 | (가) 레포 안 `runs/` 폴더 · 커밋 안 함 / (나) 레포에 커밋 | **닫힘(10-30 사용자)** — `RUNS_DIR` = 프로필 레포 `reference/2026-10-30-hub-evals/runs/`(사용자가 봄 · 프로필 `.gitignore` 에 `runs/` · 커밋 안 함) · 앱 레포에도 안 들어감(§2-5) |

### 7-6. v2 끝 조건(측정)

| 항목 | 재는 법 | 통과 |
|---|---|---|
| **잘린 호출 0** | WP-0 확인 시험(Claude · Codex 각 실물 1회 · 큰 결과 도구 — check_conditions 계열 · procedure_card `sections=all`) 뒤, **case2 182문항 재실행**(rerun-v3 와 같은 문항 · 같은 채점 · 코디 발주)의 §4-4 검증 | `truncated` true · unknown 합 **0** · 대조 불가 0 |
| **intent 전달 ≥ 95%** | 같은 재실행 · §4-4 | 스키마에 `intent` 있는 호출 중 ≥ 95%(케이스 · provider 별 각각) |
| **격리** | §4-4 `stray_tools` | 0 |
| **case3 교체 비교** | case3 걸음 판 182문항 재실행(SPEC-005 v3.2 peek/expand 완성 뒤 · 코디 발주) → `rerun_report` 전후(rerun-v3 case3 기준) | 보고(통과율 · 「정보 없음」류 · **C 건수 · 비율**(§4-4 · 전 10%) · 첫 글자 · `bytes_total` 중앙 · 되돌아간 판 수 · Jev 호출 수 · 시간) — 통과 기준은 사용자가 보고 뒤 정함(§7-7 W-4) |
| **기록 검증 결정론** | `verify_runs.py` 두 번 | 바이트 같음 |
| **기존 시험 전부** | `uv run pytest -q` · ruff · 레포 규칙 시험(`test_repo_rules.py`) | 통과 · 회귀 0 |

### 7-7. v2 아직 안 정한 것(추측으로 메우지 않음)

| id | 무엇 | 추천(본문에 쓴 값) | 누가 |
|---|---|---|---|
| W-1 | `peek` · `expand` 의 정확한 응답 꼴 · 새 도구인지 기존 도구 모드인지 — **SPEC-005 v3.2 §(peek · expand) 의존**(코디가 v3.2 발주 보충 2 로 전달 · 11-01 확인) | 앱은 §3-4-2 최소 칸만 기대 · `hub_rest.py` 두 함수로 감쌈 | SPEC-005 v3.2 planner |
| W-2 | 허브 쪽 두 줄 — MCP 도구 12 의 `_meta["anthropic/maxResultSizeChars"]` · `intent` 설명 「반드시 넘김 · 의도 표」(required 여부) — **SPEC-005 v3.2 §5-0 · §5-12 의존**(보충 2 로 전달 · 확인) | required 는 허브 판단 · 앱 끝 조건은 비율 | SPEC-005 v3.2 planner |
| W-3 | `WALK_ENOUGH_MIN`(「충분」 Noul 문턱) · 걸음당 이웃 수 3 · 2단 Choice 꼴 | 0.5(R-6 과 같은 값) · 3 · kind → id | 사용자(기록 보고 조정 · Q-5 와 같은 방식) |
| W-4 | case3 교체 뒤 통과 기준(전 case3 대비 얼마면 되나) | 보고 뒤 사용자 | 사용자 |
| W-5 | `MCP_RESULT_MAX_CHARS` 200,000 · `MAX_MCP_OUTPUT_TOKENS` 200,000 · Codex `tool_output_token_limit` 200,000 — 허브 최대 응답(2차 분류 p95 171KB · 최대 281KB)을 덮는 값. Codex 0.166 실물 마커 · 한도 동작은 WP-0 에서 확인 | 200,000 · WP-0 뒤 조정 | WP-0 결과 · 코디 |
| W-6 | `bash` 10건의 원인(`--tools ""` 인데 모델이 Bash 를 냄 — 모델 환각인지 CLI 가 내장 도구를 남기는지) | WP-0 에서 `system/init.tools` 로 확인 · `--disallowedTools Bash,Read,Grep,Glob,Edit,Write` 를 더해 둘 다 막음 | WP-0 |


## 8. 사용자 실행 절차

전제: 허브 골드(SPEC-005 · WORK-003)가 완성돼 로컬에서 뜬다 · U-1 · U-2 끝(10-30 — 키는 사용자가 워크트리 `.env` 에 직접).

```bash
# 1) 허브(18005) — SPEC-005 코드 레포
cd /Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-recommend/backend
docker compose -f graph-local.compose.yml up -d
uv run --env-file envs/.env.gold uvicorn app.graph_main:app --host 127.0.0.1 --port 18005
curl -s 127.0.0.1:18005/procedure-hub/gold/health          # 발행 빌드 id · 원장 manifest 21/21

# 2) 실험 앱(18210) — clinic_chat 작업 워크트리(브랜치 kknaksss/hub-evals)
cd /Users/kknaks/orca/workspaces/clinic_chat/hub-evals
cp .env.example .env        # .env 가 이미 있으면 건너뜀 · ANTHROPIC_API_KEY · TYPESAFE_API_KEY · RAW_DIR · SEMANTIC_JSON 채움(.env 는 커밋 안 됨)
uv sync
uv run python -m clinic_chat.server   # config.py(pydantic-settings)가 루트 .env 를 읽음 — --env-file 필요 없음

# 3) 화면
open http://127.0.0.1:18210
```

- v2 env: `.env` 에 `MCP_RESULT_MAX_CHARS=200000` · `WALK_MAX_STEPS=4` · `WALK_BYTE_BUDGET=20000` · `WALK_ENOUGH_MIN=0.5` · `TOOL_RESULT_MAX_BYTES=0`(기본값이면 생략) · 허브는 SPEC-005 v3.2(도구 meta · peek/expand) 빌드로 재시작
- 첫 질문: 환자 정보 없는 일반 질문 하나를 넣고 [보내기] — 세 열이 같이 흐르고, 셋 다 끝나면 ① → ② 가 자동으로 붙고, 아래 기록 목록에 한 줄이 생긴다
- 서버 기동 때 확인 줄: 허브 골드 · 원장 MCP 연결 · vocab 캐시 셈 · 모델 id(`client.models.list()` 로 한 번 — jev-research §4) · 키가 없으면 그 케이스만 「키 없음」으로 비활성
