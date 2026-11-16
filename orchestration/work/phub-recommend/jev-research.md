# Jev(TypeSafe) · Claude SDK MCP 가능성 조사

작성 2026-10-30 · researcher(read-only) · **키 사용 · API 호출 없음 — 공식 문서만 읽었다**
브리프 `phub-recommend-jev-research-brief.md` · 실험 설계 `reference/2026-10-30-hub-evals/README.md` · 결정 DEC-001 D-08 · D-11

표기: 출처는 줄 끝 `[S#]`(§8). 「추정」은 문서에 직접 쓰여 있지 않고 문서에서 미루어 본 것이다. 결정하지 않고 §7 「정할 것」에 모았다.

---

## 0. 요약 — 세 질문의 답

| 질문 | 답 | 근거 |
|---|---|---|
| Jev 가 MCP · 도구 호출을 쓰나 | **안 쓴다.** Jev 는 글을 생성하지 않는 판단 모델이다. 도구 호출 · 스트리밍 · 대화가 없고, 「state + 질문 → 정해진 꼴의 답」 HTTP 호출 하나뿐이다. MCP 클라이언트 기능은 문서 어디에도 없다 | [S3] [S1] |
| 그러면 case3 은 | README 설계(「앱 서버가 Jev 슬롯으로 허브 호출」)가 **Jev 를 쓸 수 있는 유일한 꼴**이다. 다만 Jev 는 선택지를 요청 본문에 받아야 하므로 **앱 서버가 Jev 앞에서 허브 노드 목록을 먼저 가져와야 한다**(허브 → Jev → 허브 → Claude) | [S5] [S6] |
| Claude 에 로컬 허브 MCP(127.0.0.1)를 붙일 수 있나 | **Messages API MCP connector 는 못 붙인다** — 서버가 「HTTP 로 공개 노출」되어야 한다(연결을 Anthropic 서버가 한다). **Python SDK + MCP 클라이언트 헬퍼(우리 프로세스가 연결)** 또는 **Claude Agent SDK(`type: "http"`)** 는 붙일 수 있다 | [S12] [S13] [S14] |
| 실험 레포 추천 | Anthropic Python SDK + 공식 MCP Python SDK 로 **우리가 루프를 직접 돈다**(단계마다 시간을 잴 수 있음). Agent SDK 는 Claude Code 하네스(내장 도구 · 도구 검색 · 권한)가 끼어 속도 비교가 흐려진다 | §4 · §5 |
| 막히는 것 | **7건** — Jev 접근(early access) · Jev 한국어 정확도 · 선택지 255개 한도 · 외부 전송 데이터 정책 · 허브 골드 MCP 미완 · case1 입력 방식 불일치 · Messages connector 로컬 불가 | §6 |

---

## 1. Jev 정체

| 항목 | 내용 | 출처 |
|---|---|---|
| 제공사 | TypeSafe AI. 2026-09-15 블로그로 「System One 모델」 · Jev 를 **early access** 로 공개(「waitlist 에서 개발자를 빼내는 중」) | [S10] |
| 성격 | 「System One model」 — **텍스트를 생성하지 않는다.** 질문마다 확률 분포와 정해진 꼴의 값만 돌려준다. 코딩 에이전트의 LLM 대체품이 아니라고 문서가 직접 말한다 | [S1] [S3] |
| 모델 | `jev-1.14.0`(2026-10-14 공개, 최신) · `jev-1.13.0`. 별칭 `jev-latest` → 1.14.0 · `jev-preview` → 1.14.0(지금 같음). 별칭은 새 릴리스 때 옮겨가므로 문턱값을 맞춘 뒤에는 버전 id 고정 권장 | [S4] |
| 엔드포인트 | `POST https://api.typesafe.ai/v1/systemone` 하나(모든 모델). `GET /v1/models` 목록 | [S4] [S7] |
| 인증 | `Authorization: Bearer $TYPESAFE_API_KEY`. 키는 콘솔 `console.typesafe.ai/keys` 에서 발급 | [S4] [S2] |
| SDK | Python `typesafe-sdk`(sync `TypeSafeClient` · async `AsyncTypeSafeClient`) · JS/TS `@typesafe-ai/sdk`. Python env: `TYPESAFE_API_KEY` · `TYPESAFE_BASE_URL` · `TYPESAFE_DEFAULT_MODEL` · 기본 timeout 10초 · 429/529 자동 재시도 | [S2] [S8] |
| 질문 종류 | Choice(목록에서 하나) · Score(순서 있는 등급) · Noul(예/아니오 확률 0–1) · Box(이미지 위치) | [S1] [S11] |
| 가격 | 입력 토큰만 과금 **$0.042 / 1M 토큰**($42 / 10억), 출력 무료 | [S4] [S10] |
| 컨텍스트 | 요청당 64k · 질문당 32k 토큰(state + 질문 하나). 헤더 `TypeSafe-Danger-Zone-Long-Context: true` 로 둘 다 262k — 더 느리고 덜 정확 | [S4] |
| 요청 한도 | 본문 32 MiB · 중첩 64단 · 유한한 숫자만(id 는 문자열로) · 질문 수 제한 없음(컨텍스트 안이면) | [S7] [S4] |
| 속도 한도(rate) | 조직별 · 초당 토큰 · 초당 요청. **수치는 콘솔에서만 보인다**(문서에 없음) | [S4] |
| 지연(공식) | 블로그: 「End-to-end 70ms–500ms」(제공사 자체 측정, 미국 서부에서 잰 값이라고 명시). 쿡북 실측: 질문 13개 한 번에 0.27초 · 스킬 고르기 0.09–0.31초 | [S10] [S9] [S15] |
| 언어 | **영어가 주 학습 언어.** 「CJK 포함 다른 언어는 받지만 정확도가 낮다 — 비영어 작업은 자기 데이터로 시험하고 confidence 를 잘 봐라」 | [S4] [S16] |
| 알려진 약점(1.13) | 숫자 · 날짜 · 셈 약함 · 이중부정/여러 단계 추론 약함 · **state 에 무관한 내용이 많으면 정확도 하락(context rot)** · **Choice 선택지 순서에 영향 — 앞쪽으로 기움** · 생성 불가 | [S16] |
| 데이터 | 고객 요청으로 학습하지 않는다. ZDR 은 enterprise 만 | [S4] [S17] |

## 2. 정해진 꼴 출력 — 슬롯을 허브 노드 id 로

### 2-1. 꼴

요청 = `{model, state, questions: {<내가 정한 id>: {type, instructions, criteria}}}`. Choice 의 `criteria` 는 `{선택지 이름: 설명}` 맵이고, 답 `choice` 는 **반드시 그 키 중 하나**다(형 오류가 구조상 불가 — 지어낸 id 가 나올 수 없다) [S5] [S10].

Choice 답 = `choice` · `probabilities`(선택지마다, 합 1) · `confidence`(0–1). Score 답 = `score` · `probabilities` · `confidence`. **Noul 은 `noul`(0–1 확률)만 — confidence 없음** [S1] [S11].

### 2-2. 신뢰도 값 — 「되묻기」에 쓸 숫자

- Choice confidence = `(p_max − 1/n) / (1 − 1/n)` — 균등 분포 0, 한 곳 몰림 1. 문서는 `p_max` · 1위/2위 비(`p_max / p_second`)도 같이 써 보라고 권한다(「많은 실제 판단이 상위 두 후보 싸움」) [S6].
- 문서 예: `department` 0.42(두 팀에 걸친 티켓) → 코드가 「confidence < 0.3 이면 사람에게」로 분기 [S5]. D-08 의 「신뢰도 낮은 슬롯은 Claude 가 되묻기」가 이 패턴(Confidence-gated routing) 그대로다.
- **문턱값은 문서에 정답이 없다** — 자기 데이터로 맞추라고 한다. 별칭이 옮겨가면 분포가 바뀌므로 버전 고정 [S4]. → OQ-113 과 같은 질문.

### 2-3. 허브 노드 수백~천 개를 선택지로 넣는 법

**한도: Choice 하나에 선택지 최대 255개**(OpenAPI `criteria.maxProperties: 255`) [S5] [S18]. 문서가 제시하는 넘는 방법:

| 방법 | 문서 사례 | 우리 쪽에 맞춰 보면(추정) |
|---|---|---|
| **2단(묶음 → 안)** | 줄 검색 쿡북: 「255줄 넘으면 두 번 — 하나는 구간 고르기, 하나는 구간 안에서」 [S19] | 고민 대분류 → 소분류 노드. 허브 트리 꼴(taxonomy)이 묶음을 준다 |
| **계층 + beam search** | 계층 분류 쿡북: 단계마다 Choice 확률로 상위 K 경로 유지 [S20] | 고민 · 부위 트리가 깊으면. 단계 수만큼 Jev 왕복 |
| **넓게 훑고 좁혀 재확인(2 요청)** | 스킬 제안 쿡북: 182개 한 줄씩 Choice → 상위 3개 긴 설명으로 다시 Choice + 후보마다 Noul, 0.30 미만이면 버림 [S15] | 1차는 이름만 · 2차는 상위 후보에 설명(동의어 · 정의) |
| **허브 사전으로 후보 먼저 줄이기** | 「regex · 생성 모델로 후보를 뽑고 Jev 는 고르기만」 [S16] | 허브 결정론 노드 검색(D-12)으로 후보를 줄인 뒤 Choice. 허브에 모델이 없다는 결정과 맞는다 |
| 쪼개서 여러 Choice 를 한 요청에 | 질문은 병렬 · 독립 평가, 개수 늘려도 시간 거의 그대로 [S1] [S9] | 255개씩 끊은 Choice 여러 개를 한 요청에 — 단 각 Choice 가 「자기 묶음 안 최선」을 고를 뿐이라 묶음 간 비교는 코드 몫 |

여러 개를 고르는 슬롯(고민이 둘 이상): Choice 는 **하나만** 고른다. 「복수 선택」 꼴은 없다. 문서 패턴은 `probabilities` 상위를 코드에서 읽거나, 후보마다 Noul(「이 발화가 X 를 말하나」)을 거는 것 [S5] [S15]. 「해당 없음」 선택지는 잘 안 들을 수 있어 **짝 Noul**(「목록 중 하나라도 말하나」)을 권한다 [S5].

선택지 순서 기울기 [S16] 가 있으니 실험 기록에 선택지 순서(또는 섞은 seed)를 남기는 것이 안전하다(추정).

### 2-4. 실패 처리

| 상황 | 응답 |
|---|---|
| 본문 규칙 위반 · `max_tokens_exceeded`(컨텍스트 초과) | 400 |
| 키 없음/틀림 | 401 |
| 32 MiB 초과 | 413 |
| 검증 실패(필드 누락 · 질문 꼴 틀림 — 예: 선택지 256개) | 422(어느 필드인지 본문에) |
| 속도 한도 · 과부하 | 429 · 529 — SDK 가 지수 백오프로 자동 재시도, `retry-after` 따름 |

[S7]. 답 자체는 형이 보장되므로 「파싱 실패」는 없다. 남는 실패는 **틀린 답을 높은 신뢰도로 내는 것**뿐이고, 이건 confidence 문턱과 실험 ②(Opus 채점)로만 잡힌다.

## 3. 도구 호출 · MCP

- **Jev 는 tool calling · MCP 클라이언트를 지원하지 않는다.** 문서: 「Coding agents rely on an LLM that streams text, calls tools… Jev does none of that」 [S3]. 문서 전체(llms.txt 색인 · API 레퍼런스 · OpenAPI)에 MCP 클라이언트 · 원격/로컬 MCP 연결 항목이 없다 [S0]. 「Function calling」 쿡북은 Jev 가 함수를 부르는 게 아니라 **함수 이름 · 인자를 Choice 로 고르고 호출은 코드가 한다**는 내용이다 [S21].
- 반대 방향(Jev 를 MCP 서버로 감싸 Claude 에 주기)도 공식 제공은 없다. 「Agent skill」은 코딩 에이전트가 Jev 연동 코드를 잘 쓰게 하는 문서 묶음일 뿐이다 [S3].

**case3 이 「앱 서버가 Jev 슬롯으로 허브 호출」로 충분한가 — 충분하다, 단 한 단계가 더 있다.**

```
질문 ─▶ 앱 서버 ─① 허브: 노드 목록/스키마 (선택지 재료)  ← Jev 는 선택지를 요청에 받아야 한다
                ─② Jev: 의도 + 슬롯 Choice/Noul (한 요청에 병렬)
                ─③ 허브: 슬롯 노드 id 로 의도별 탐색 1번
                ─④ Sonnet: 탐색 결과로 답 문장 1번 (신뢰도 낮은 슬롯은 되묻기)
```

- ① 은 허브 MCP 의 「노드 목록/스키마」 도구(D-08 「Jev 의 선택지는 Hub 의 노드 목록/스키마 tool 로 만든다」)를 앱 서버가 MCP 클라이언트로 부르거나, 같은 조회 계층의 REST 로 부른다. 노드 목록은 질문마다 바뀌지 않으므로 **앱 서버가 시작할 때 한 번 받아 캐시**하는 게 자연스럽다(추정 — 그러면 질문당 단계는 ②③④).
- 255개를 넘는 노드면 ② 가 2단(§2-3)이 되어 Jev 왕복이 2번이 될 수 있다. README §2 의 「Jev 1 + Sonnet 1」은 노드 수에 따라 「Jev 1~2 + Sonnet 1」이 된다.

## 4. Claude 쪽 — 로컬 허브 MCP 붙이기

허브 MCP = `http://127.0.0.1:18005/procedure-hub/gold-mcp/mcp` · `…/raw-mcp/mcp`(Streamable HTTP · stateless · JSON).

| 방식 | 127.0.0.1 붙나 | 근거 · 메모 |
|---|---|---|
| **Messages API MCP connector**(`mcp_servers` + `tools: [{type: "mcp_toolset"}]`, beta `mcp-client-2026-09-15` / `mcp-client-2025-11-20`) | **안 됨** | 「The server must be publicly exposed through HTTP (Streamable HTTP · SSE)」 · 「MCP 스펙 중 tool call 만」 · ZDR 대상 아님 [S12]. 연결을 Anthropic 서버가 하므로 우리 맥의 127.0.0.1 은 닿지 않는다. 붙이려면 허브를 터널 등으로 **공개 노출**해야 함 — 원장 데이터가 밖으로 열리는 일이라 권하지 않음 |
| **Anthropic SDK + MCP 클라이언트 헬퍼**(Python `pip install "anthropic[mcp]"` · `anthropic.lib.tools.mcp` 의 `async_mcp_tool` 등 · TS 는 `@anthropic-ai/sdk` + `@modelcontextprotocol/sdk`) | **됨** | 공식 문서: 「로컬 서버 · prompts · resources 가 필요하면 클라이언트 헬퍼를 써라」 [S12] [S13]. 우리 프로세스가 MCP `ClientSession` 으로 허브에 연결 → 도구 목록을 Claude 도구로 변환 → tool runner 나 직접 루프. 문서 예시는 stdio 이고, Streamable HTTP 클라이언트는 공식 MCP Python SDK 의 transport 를 쓴다 — **정확한 import 경로는 SDK 버전마다 달라 구현 때 그 버전 문서로 확인**(이번 조사에서 확정 못 함) |
| **Claude Agent SDK**(`claude-agent-sdk` / `@anthropic-ai/claude-agent-sdk`) | **됨(추정)** | `mcp_servers={"hub": {"type": "http", "url": "…"}}` · 도구 이름 `mcp__hub__<tool>` · `allowed_tools` 로 허용 [S14]. 연결 주체가 로컬 Claude Code 프로세스라 127.0.0.1 이 닿는다 — 문서 예시는 공개 URL 만이고 localhost 를 직접 말하진 않아 「추정」. 단 **Claude Code 하네스 전체가 따라온다**: 내장 도구(Read/Bash/WebSearch…) · MCP 도구 검색(기본 켜짐 — 도구 정의를 미뤄 싣는다) · 첫 턴 MCP 연결 대기(기본 30초 한도) · 25,000 토큰 넘는 도구 결과는 파일로 빼 버림 [S14] |

### 실험 레포에서 쓸 방식 — 추천: **Anthropic Python SDK + MCP 클라이언트(직접 루프)**

이유:
1. README §3 이 요구하는 `stages[]`(Claude 왕복마다 · 도구 호출마다) · `llm_round_trips` · 단계별 토큰을 **우리가 루프 안에서 직접 찍을 수 있다.** tool runner 를 쓰더라도 턴마다 훅이 있다.
2. case2 와 case3 이 **같은 클라이언트 · 같은 Sonnet 설정**을 쓴다 — 차이가 「누가 말을 해석하나」만 남는다. Agent SDK 를 case2 에만 쓰면 하네스 오버헤드(시스템 프롬프트 · 도구 검색 · 내장 도구)가 case2 에만 붙어 속도 · 품질 비교가 흐려진다.
3. 허브를 공개할 필요가 없다.

Agent SDK 를 쓸 이유는 「실제 상담 앱이 Agent SDK 꼴이 될 것」이 정해졌을 때뿐이다(지금 미정 — §7).

### 모델 id(2026-10-30 기준 — `claude-api` 스킬 캐시 2026-09-25 + 공식 MCP connector 문서 지원 모델 목록과 일치)

| 역할(README §1) | 모델 id | 실험에 걸리는 점 |
|---|---|---|
| 답변 — Sonnet | `claude-sonnet-5-5` | `thinking: {type: "disabled"}` 는 400. 생각을 끄려면 `{type: "between_tools"}`(effort high 이하). effort 기본 high. **강제 `tool_choice`(any/tool) 400** — `auto` 로만 |
| 채점 — Opus | `claude-opus-5-5` | 생각을 끌 수 없음 · effort 기본 **medium**(명시 권장). 강제 `tool_choice` 400 |

- 세 케이스 공정성: thinking · effort 설정이 TTFT 를 크게 바꾼다 — **세 케이스 Sonnet 설정을 같게**(README O-2 와 같은 줄). 생각을 켜 두면 첫 글자 전에 thinking 블록이 먼저 흐른다(기본 display 는 빈 텍스트).
- 모델 id 는 실험 시작 때 `client.models.list()` 로 한 번 확인 권장(캐시된 표라서).

## 5. 실험 레포 구성 추천 (`kknaks/clinic_chat` · 공개 레포)

### 5-1. 공개 레포 규칙

- `.env`(ANTHROPIC_API_KEY · TYPESAFE_API_KEY · 허브 URL · 원장 경로)는 `.gitignore`, `.env.example` 만 커밋(값 없이) — D-11
- 원장 json(`phub-stg-2026-10-26/`) · 실행 기록(jsonl) · 허브 응답 캐시는 레포 밖 경로를 env 로 받는다. `runs/` 같은 출력 폴더도 ignore
- Jev 요청에 들어가는 것 = 사용자 질문 + 허브 노드 이름/설명 → TypeSafe(미국) 로 나간다. 같은 사실이 OQ-112(데이터 정책)

### 5-2. 꼴(추정 — 구현 때 정할 것)

```
clinic_chat/
  .env.example         키 · URL · 경로 이름만
  app/
    clients/           anthropic · typesafe · hub_mcp(MCP ClientSession, 골드/원장 둘)
    cases/case1.py     원장 → Sonnet
    cases/case2.py     Sonnet ⇄ 골드 MCP 루프
    cases/case3.py     허브 목록(캐시) → Jev → 허브 탐색 → Sonnet
    timing.py          stages[] 기록기 (perf_counter 기준)
    judge/             ① 단어 검사 · ② Opus 채점
    server.py          3열 화면 + SSE 스트리밍
```

### 5-3. 케이스별 호출 흐름 · 재는 자리

공통: 세 갈래 같은 시각 시작(asyncio.gather), 시계는 질문 접수 시각 `t0` 하나 기준.
`ttft_ms` = 스트리밍에서 **첫 `text` 델타**가 도착한 시각 − t0(thinking 델타는 제외 — 사용자가 보는 첫 글자 기준. 이 정의는 §7 에 열어 둠).

| case | 단계(stages[].name) | 왕복 |
|---|---|---|
| case1 | `claude`(스트림 시작 → 끝) | Sonnet 1 |
| case2 | `claude#1` → `tool:<이름>#1` → `claude#2` → … → `claude#n`(마지막만 답 글자) | Sonnet n + 도구 n−1. 도구마다 입력 · 결과 크기 · 노드 id 기록(README §6 `trace.tool_calls[]`) |
| case3 | (`hub_list` — 캐시면 시작 때 1회, 질문당 기록은 0 또는 「캐시」) → `jev`(1~2) → `hub_explore` → `claude` | Jev 1~2 + Sonnet 1. Jev 응답의 `usage` · `model`(버전) · 슬롯별 confidence 기록 |

- 토큰: Anthropic `usage`(input · output · cache read), Jev `usage.input_tokens`(과금은 입력만)
- case2 의 첫 글자는 마지막 왕복에서야 나온다 — 그래서 case2 의 TTFT 는 「도구 왕복을 다 마친 시간」이 섞인다. case3 와 TTFT 를 비교할 때 이 구조 차이가 바로 측정 대상이다
- Jev 지연은 우리 쪽 네트워크(한국 → 미국 서부) 가 더해진다 — 블로그 70–500ms 는 서부 기준 [S10]. 실측은 `jev` 단계 시간으로만 판단(추정)

## 6. 막히는 것 · 사용자가 해야 할 것

| # | 막히는 것 | 왜 | 사용자가 할 것 / 풀 방법 |
|---|---|---|---|
| B-1 | **Jev 접근** | 2026-09-15 기준 early access · waitlist [S10]. 지금도 대기인지 문서로는 모름 | `console.typesafe.ai` 가입 → 키 발급(`/keys`) 가능한지 확인 · 조직 rate limit 은 콘솔 `/rate-limits` 에서 확인 |
| B-2 | **Jev 한국어 정확도** | 공식: 영어 주력, CJK 정확도 낮음 [S4] [S16]. 우리 발화 · 노드 이름이 전부 한국어 | 실험 자체가 이 질문의 답(case3 ↔ case2 노드 정확도). 노드 설명에 영어 병기를 넣을지는 §7 |
| B-3 | **선택지 255개 한도** | 고민 · 부위 노드가 255 넘으면 Choice 하나에 못 넣음 [S18] | 골드 노드 수가 정해지면 2단/계층/사전 후보 줄이기 중 택(§2-3) — 골드 설계 결과에 기댐 |
| B-4 | **외부 전송 데이터 정책** | Jev 로 발화 + 노드 목록이 나감 · ZDR 은 enterprise 만 [S17]. Anthropic MCP connector 도 ZDR 대상 아님 [S12](우리는 안 씀) | OQ-112 결정. 실험은 사용자가 직접 입력한 질문만 쓰므로 환자 정보는 넣지 않는다는 규칙만 정하면 됨(추정) |
| B-5 | **허브 골드 MCP 미완** | README §1: 실험은 골드 완성 뒤. 골드 도구 목록이 정해져야 case2 도구 · case3 경로가 정해짐 | 골드 완성 대기(메인 코디 진행) |
| B-6 | **case1 입력 방식이 문서끼리 다름** | 브리프는 「case1 원장 MCP + Claude」(raw-mcp, SPEC-005), README §2 는 「원장 json 21개를 Sonnet 에 넣는다 · 넣는 방식 O-1 미정」 | §7 Q-1 — 사용자 결정 |
| B-7 | **Messages API MCP connector 로 로컬 허브 불가** | 공개 HTTP 필요 [S12] | 우회 불필요 — SDK + MCP 클라이언트(§4 추천)로 감. 공개 노출은 하지 않는다 |
| — | Anthropic 키 | D-11 사용자 보유 | `.env` 에만. 키 · 실명 기록 없음 |

## 7. 정할 것 (결정하지 않음)

| # | 질문 | 갈래 | 관련 |
|---|---|---|---|
| Q-1 | case1 은 원장 **MCP**(raw-mcp 를 Sonnet 이 도구로 호출) 인가, 원장 **json 을 통째/일부 넣기** 인가 | 브리프 문구 vs README §2 · O-1 | B-6 · README O-1 |
| Q-2 | 실험 클라이언트: SDK 직접 루프(추천) vs Agent SDK | 실제 상담 앱 꼴과 맞출지 | §4 |
| Q-3 | `ttft_ms` 의 「첫 글자」 = 첫 text 델타 vs 첫 바이트(thinking 포함) · Sonnet thinking 켜고/끄고(`between_tools`) · effort | 세 케이스 같게 | README O-2 |
| Q-4 | 255 넘는 노드의 Jev 선택지 구성(2단 / 계층 beam / 허브 사전으로 후보 줄이기) | 골드 노드 수 확정 뒤 | §2-3 · B-3 |
| Q-5 | 슬롯별 confidence 문턱(되묻기 기준) · `p_max` / 1·2위 비 중 무엇을 쓰나 | 실험 기록으로 보고 정함 | OQ-113 |
| Q-6 | Jev 모델 고정 — `jev-1.14.0` 고정 vs `jev-latest` | 별칭 이동 시 분포 바뀜 | [S4] |
| Q-7 | 허브 노드 목록 캐시 — 앱 시작 1회 vs 질문마다 | case3 단계 정의 | §3 |
| Q-8 | 노드 설명 영어 병기 여부(Jev 정확도용) | 한국어 정확도 | B-2 |

## 8. 출처 (모두 2026-10-30 열람)

| # | 출처 |
|---|---|
| S0 | TypeSafe 문서 색인 https://docs.typesafe.ai/llms.txt |
| S1 | Introduction https://docs.typesafe.ai/introduction.md |
| S2 | Quick start https://docs.typesafe.ai/introduction/quickstart.md · Python SDK https://docs.typesafe.ai/sdk/python.md |
| S3 | Jev with coding agents https://docs.typesafe.ai/introduction/coding-agents.md |
| S4 | Models(가격 · 컨텍스트 · rate limit · 별칭 · 언어 · 데이터) https://docs.typesafe.ai/models.md |
| S5 | Choice https://docs.typesafe.ai/primitives/choice.md |
| S6 | Confidence https://docs.typesafe.ai/confidence.md |
| S7 | Request rules and errors https://docs.typesafe.ai/api/errors.md |
| S8 | Python SDK constants https://docs.typesafe.ai/sdk/python/api/constants.md |
| S9 | Parallel questions 쿡북 https://docs.typesafe.ai/cookbooks/parallel_questions.md |
| S10 | TypeSafe 블로그 「Introducing System One Models & Jev」(2026-09-15) https://typesafe.ai/blog/introducing-system-one-models-and-jev |
| S11 | Primitives https://docs.typesafe.ai/primitives.md |
| S12 | Claude MCP connector https://platform.claude.com/docs/en/agents-and-tools/mcp-connector (Limitations · Client-side MCP helpers · beta 헤더 · ZDR) |
| S13 | `claude-api` 스킬 `python/claude-api/tool-use.md` 「MCP Tool Conversion Helpers」(Claude Code 2.1.284 번들) |
| S14 | Claude Agent SDK — Connect to external tools with MCP https://code.claude.com/docs/en/agent-sdk/mcp |
| S15 | Skill suggestion 쿡북 https://docs.typesafe.ai/cookbooks/skill_suggestion.md |
| S16 | Jev 1.13 jaggedness https://docs.typesafe.ai/model-jaggedness/jev-1.13.md · State https://docs.typesafe.ai/concepts/state.md |
| S17 | Legal https://docs.typesafe.ai/legal.md |
| S18 | System One API 레퍼런스(OpenAPI · `criteria maxProperties: 255`) https://docs.typesafe.ai/api/system-one.md |
| S19 | Line-by-line search 쿡북 https://docs.typesafe.ai/cookbooks/semantic_find.md |
| S20 | Hierarchical classification 쿡북 https://docs.typesafe.ai/cookbooks/hierarchical_classification.md |
| S21 | Function calling 쿡북 https://docs.typesafe.ai/cookbooks/function_calling.md |
| — | 참고(2차): Simon Willison 「Jev」 2026-09-21 https://simonwillison.net/2026/Sep/21/jev/ — 가격 · 질문 종류가 1차 출처와 일치 |
