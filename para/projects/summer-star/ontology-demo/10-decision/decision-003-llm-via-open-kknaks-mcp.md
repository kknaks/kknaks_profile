---
type: decision
id: DEC-003
title: "LLM 경로 — open-kknaks 경유 실행 + 조회 도구 4종을 MCP 로 노출한다"
status: accepted
product: ontology-demo
created_at: 2026-09-02
updated_at: 2026-09-02
tags:
  - product/ontology-demo
  - doc/decision
  - status/accepted
links:
  baselines:
    - "[[baseline-001-demo-agent-app|BASE-001]]"
  decisions:
    - "[[decision-002-pii-masking-boundary|DEC-002]]"
    - "[[decision-004-web-three-pages-in-front|DEC-004]]"
  specs:
    - "[[spec-002-mcp-tools-contract|SPEC-002]]"
    - "[[spec-005-agent-loop-and-gates|SPEC-005]]"
    - "[[spec-003-api-and-chat-contract|SPEC-003]]"
  works: []
  releases: []
  related:
    - "[[decision-027-chat-ai-execution-and-tool-boundary|KDEV-DEC-027]]"
up:
  - ai-agent
  - prompt-injection
---

# LLM 경로 — open-kknaks 경유 실행 + 조회 도구 4종을 MCP 로 노출한다

LLM SDK 를 직접 import 하지 않는다. 실행은 open-kknaks(AgentClient + RedisBroker) 경유이고,
provider 는 codex(`gpt-5.6-terra`)다. 조회 도구 4종은 `app/ontology-agent/tools/` 의 FastMCP
(Streamable HTTP) 서버로 내보내고, codex 가 MCP 클라이언트로 붙는다.

> baseline의 날것 입력을 spec으로 내리기 전에 적용 방향을 정하는 문서.
> 기능 계약 상세는 `20-spec/`, 실제 작업 순서는 `30-work/`에 둔다.

## Context

- 관련 baseline: [[baseline-001-demo-agent-app|BASE-001]] — 기록 09 §3 6단계가 「LLM 경로는
  착수 시 ADR-04 확인이 첫 작업」으로 남겨 둔 자리다.
- ADR-04 의 실체는 이 레포에 이미 있다 —
  [[decision-027-chat-ai-execution-and-tool-boundary|KDEV-DEC-027]](kknaks-dev 채용담당자 채팅):
  LLM API 직접 호출은 기각, 실행은 open-kknaks 워커, 데이터 접근은 쉘·파일이 아니라 MCP
  read-only tool. 그 결정은 배포·운영까지 통과한 검증된 계약이다.
- 이 제품이 지켜야 할 명제도 같은 계열이다 — **S-001 관계는 Instruction 이 아니라 데이터에
  있다**, **S-002 Agent 는 판단만 하고 집계·조회는 명세된 View 가 한다**(BASE-001 아키텍처
  결정 5).
- 결정이 필요한 이유: 이 두 명제는 프롬프트로 지킬 수 없다. 에이전트가 무엇을 쥐는지가
  구조로 정해져야 「관계 지식을 프롬프트에 넣지 않았다」가 증명된다.

## Options

### 실행 경로

| Option | Description | Pros | Cons | Notes |
|---|---|---|---|---|
| A | LLM SDK 직접 import (Anthropic/OpenAI SDK) | 단순 · 의존성 하나 | **ADR-04 위반** · LLM 교체가 코드 수정이 된다 · 세션/큐를 재발명 | 기각 |
| **B** | **open-kknaks(AgentClient + RedisBroker) 경유, provider 는 codex** | ADR-04 현행 유지 · 검증된 실행 경로 재사용 · LLM 교체 가능 | 큐 왕복 지연 · redis·워커 컨테이너가 배포에 붙는다 | **채택** |

### 데이터 접근

| Option | Description | Pros | Cons | Notes |
|---|---|---|---|---|
| a | 자유 SQL 도구(`run_sql`) 하나로 무엇이든 조회 | 도구 설계 비용 0 · 질문 대응 범위 최대 | **S-002 위반** — 집계를 Agent 가 하게 된다 · 마스킹 뷰 우회(DEC-002 와 충돌) | 기각 |
| b | 관계 지식을 시스템 프롬프트에 넣고 답하게 | 도구 없이 동작 | **S-001 위반** — 관계가 데이터가 아니라 Instruction 이 된다. 데모의 명제 자체를 잃는다 | 기각 |
| **c** | **파라미터화된 조회 도구 4종을 MCP 로 노출** | 집계는 View, 관계는 edges 조회 · 프로토콜이 경계를 강제 | 도구가 못 답하는 질문이 생긴다(도구 설계가 곧 능력) | **채택** |

## Decision

### D1. 실행은 open-kknaks 경유 — SDK 직접 import 금지

- LLM SDK 를 애플리케이션 코드에서 직접 import 하지 않는다(ADR-04 현행 유지).
- 실행은 **open-kknaks 의 AgentClient + RedisBroker** 를 지난다.
- provider 는 **codex(`gpt-5.6-terra`)**.

### D2. 조회 도구 4종은 FastMCP 서버로

- 위치는 `app/ontology-agent/tools/`, **FastMCP(Streamable HTTP)** 서버로 띄운다.
  codex 가 MCP 클라이언트로 붙는다. 모범 구현은 이 레포의 `app/mcp/`.
- 도구 4종은 BASE-001 이 등재한 것 그대로다 — `query_kpi`(골드 read-only) ·
  `query_layer`(실버·브론즈 마스킹 뷰 — 드릴다운) · `trace_ontology`(판정 구분 반환, 기각 사유
  포함) · `get_definition`(글로서리).
- **전부 파라미터화된 조회다. 자유 SQL 도구는 만들지 않는다.** 브론즈·실버 접근은
  [[decision-002-pii-masking-boundary|DEC-002]] 의 마스킹 뷰를 지난다.

### D3. 채팅 UX 는 기본 클로드형 자유 대화

- 정해진 질문 버튼·폼이 아니라 자유 입력 대화가 기본형이다.

### 기각

- SDK 직접 호출(A) · 자유 SQL 도구(a) · 관계 지식의 프롬프트 주입(b).

## Rationale

- **판단 기준**: S-001·S-002 가 지시가 아니라 구조로 지켜지는가, ADR-04 를 유지하는가,
  LLM 을 교체할 수 있는가.
- **B+c 인 이유**: 실행 경로는 이미 검증된 것(KDEV-DEC-027 의 계약)을 그대로 쓰고, 새로
  설계하는 힘은 전부 **도구 경계**에 쓴다. 이 제품에서 실제로 새로운 문제는 그것뿐이다 —
  「어떤 조회를 도구로 열 것인가」가 곧 데모가 증명하는 것의 범위다.
- **자유 SQL 을 막은 이유**: 열어 주는 순간 집계 주체가 Agent 로 넘어가고(S-002 붕괴),
  마스킹 뷰도 우회된다(DEC-002 붕괴). 두 결정이 한 도구에서 동시에 무너진다.
- **리스크**
  - 도구 4종이 못 받는 질문은 답이 안 나온다 — 도구 파라미터 설계가 spec 의 핵심 과제다.
  - 큐 왕복 + codex 기동으로 첫 응답이 느릴 수 있다(KDEV-DEC-027 OQ-2 의 실측: 콜드 ~15초).
  - MCP 서버가 마스킹 뷰만 본다는 보장은 서버 구현에 달려 있다 — DEC-002 게이트로 역검증.

## 근거 개념

- [[ai-agent]] — tool calling 그 자체다. 모델에게 범용 손(자유 SQL·쉘)이 아니라 **용도가
  새겨진 손(도구 4종)** 을 쥐여 준다는 골격, 그리고 도구 이름·설명·파라미터 스키마가 모델의
  선택 품질을 정한다는 설계 감각이 여기서 온다.
- [[prompt-injection]] — 지시는 경계가 아니라는 전제. 「관계를 프롬프트에 넣지 마라」·「원값을
  말하지 마라」를 문장으로 걸지 않고 도구 표면 자체를 좁힌 이유가 이 개념이다.

## Scope

- In: open-kknaks 제출·소비 경로, FastMCP 서버와 도구 4종, codex 접속 설정, 자유 대화 UX
- Out: 도구별 파라미터·응답 스키마 상세(spec), 응답 스키마 `used_edges` 와 그래프 하이라이트
  연결 방식([[decision-004-web-three-pages-in-front|DEC-004]] OQ), 레이트리밋·토큰 상한
  ([[decision-005-internal-demo-deploy|DEC-005]] — 두지 않기로 함)
- 영향을 받는 spec 후보: 에이전트 실행·응답 계약, 조회 도구 계약, 채팅 화면

## Open Questions

| ID | Question | Owner | Next |
|---|---|---|---|
| ~~OQ-1~~ | 도구 4종의 파라미터·응답 스키마 (특히 `trace_ontology` 의 판정 구분 표현) | kknaks | **닫힘 (2026-09-02 승인)** — [[spec-002-mcp-tools-contract\|SPEC-002]] §4 확정(v0.0.2 ready). `grain=monthly` 는 골드 월 View 조회, `lag` 는 `<정수>d`, 응답에 `edge_id` |

## Resulting Spec

| Spec | Action | Notes |
|---|---|---|
| [[spec-002-mcp-tools-contract\|SPEC-002]] | create — **작성됨 (2026-09-02, v0.0.1)** | 도구 4종 파라미터·응답·에러 · 자유 SQL 부재 |
| [[spec-005-agent-loop-and-gates\|SPEC-005]] | create — **작성됨 (2026-09-02, v0.0.1)** | 루프 3단계 · 응답 스키마(`used_edges`·`citations`) · 게이트 5종 · 회귀 3본 |
| [[spec-003-api-and-chat-contract\|SPEC-003]] | create — **작성됨 (2026-09-02, v0.0.1)** | 채팅 API · 진행 표시 · 실행 경로 배선 |
