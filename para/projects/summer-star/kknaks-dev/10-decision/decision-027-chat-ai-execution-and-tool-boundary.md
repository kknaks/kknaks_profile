---
type: decision
id: KDEV-DEC-027
title: "채팅 AI 실행 경로와 tool 노출 경계 — 전용 큐 · MCP · chat_exposed 옵트인"
status: accepted
product: kknaks-dev
created_at: 2026-08-28
updated_at: 2026-08-28
tags:
  - product/kknaks-dev
  - doc/decision
  - status/accepted
links:
  baselines:
    - "[[baseline-008-recruiter-chat|KDEV-BL-008]]"
  decisions:
    - "[[decision-025-chat-first-home|KDEV-DEC-025]]"
    - "[[decision-026-anonymous-visitor-session|KDEV-DEC-026]]"
    - "[[decision-024-stage-session-inheritance|KDEV-DEC-024]]"
  specs:
    - "[[spec-017-recruiter-chat|KDEV-SPEC-017]]"
  works: []
  releases: []
  related: []
up:
  - ai-agent
---

# 채팅 AI 실행 경로와 tool 노출 경계 — 전용 큐 · MCP · chat_exposed 옵트인

채팅 AI 는 기존 open-kknaks 워커(codex + resume)를 전용 큐로 재사용한다. 데이터 접근은
쉘·파일이 아니라 **MCP 로 정의한 read-only tool** 로만 하고, tool 이 보여 주는 범위는
어드민의 노출 플래그(`chat_exposed`)가 매 호출 실시간으로 정한다.

## Context

- 관련 baseline: [[baseline-008-recruiter-chat|KDEV-BL-008]]
- 실행 재료는 이미 있다 — `service/ai_service.py` 의 submit → result 패턴,
  `result_session_id` resume([[decision-024-stage-session-inheritance|KDEV-DEC-024]] 검증),
  `Dockerfile.worker`(codex 런타임 마운트).
- 그런데 기존 워커 계약을 그대로 쓰면 안 되는 지점이 둘이다.
  ① 워커는 `queue=default` · `CONCURRENCY=1` — 파이프라인과 채팅이 서로 줄을 세운다.
  ② 워커는 `danger-full-access` 쉘 + **원장 전체 `/ledger` ro 마운트** — 파이프라인은
  입력이 owner 라 괜찮았지만, 채팅은 **익명 방문자의 입력이 쉘 가진 에이전트로
  들어간다.** 프롬프트 인젝션이면 개인 지식(resources) · 회사 기록까지 읽힌다.
- 노출 제어 요구: 「제품 표면은 보여줘도 상세 스펙·환경설정은 노출하면 안 된다」,
  그리고 **그 경계를 어드민에서 제어할 수 있어야 한다.**
- owner 의 학습 목적이 명시됐다 — 「api tool 을 써보면서 공부하고 싶다」.
- **레퍼런스**: `~/git/harness_works/mediness-app` 의 landing-chat — 같은 스택
  (open-kknaks + codex + MCP)의 사내 검증 구현. D5 · D6 의 개정(2026-08-28)이
  여기서 확인된 실측 계약을 채택한 것이다.

## 근거 개념

- [[ai-agent]] — tool calling 그 자체다. 모델에게 쉘(범용 손)이 아니라 **정의한
  tool(용도가 새겨진 손)** 만 쥐여 준다는 이 결정의 골격이 이 개념이고, tool
  이름·설명·파라미터 스키마가 모델의 tool 선택 품질을 정한다는 설계 감각도
  여기서 온다.

## Options

### 실행 경로

| Option | Description | Pros | Cons | Notes |
|---|---|---|---|---|
| A | LLM API 직접 호출 | 단순 · 스트리밍 쉬움 | ADR-04 위반(SDK 직접 금지) · 세션 관리 재발명 | 기각 |
| **B** | **기존 open-kknaks 워커 재사용 + 전용 큐** | 검증된 resume · 인프라 그대로 | 스트리밍 없음 · 큐 왕복 지연 | **채택** |
| C | 채팅용 실행기 신규 | 채팅에 최적화 | 실행기 둘 유지 · lockstep 축 증가 | 기각 |

### 데이터 접근

| Option | Description | Pros | Cons | Notes |
|---|---|---|---|---|
| a | 원장 마운트 그대로 + 프롬프트로 제한 | 변경 제로 | 지시는 경계가 아니다 — 인젝션에 뚫린다 | 기각 |
| b | 공개 문서만 export 한 번들을 마운트 | 물리 격리가 가장 강함 | 어드민 토글 → export 반영이 배치. tool calling 학습도 안 됨 | 기각 |
| **c** | **back 의 chat-tool API 를 MCP 로 노출** | 매 호출 DB 판정 = 어드민 실시간 제어 · tool 정의 학습 | 경계가 물리에서 API 레벨로 내려간다 → D5 가 보강 | **채택** |

## Decision

### D1. 전용 큐 · 전용 워커

- 채팅 태스크는 `queue=chat` 으로 제출한다. `default` 큐(캡처·잔디 파이프라인)와
  서로 줄 세우지 않는다.
- compose 에 채팅 워커 서비스를 추가한다 — 이미지 · 기동 방식은 기존
  `Dockerfile.worker` 그대로, environment(큐 · CODEX_HOME)만 다르다.

### D2. 대화 연속은 codex 세션 매핑으로

- `conversation.ai_session_id` 에 `result_session_id` 를 저장하고, 그 대화의 다음
  질문 제출 때 resume 으로 넘긴다 — 파이프라인의 문서→개념 승계와 같은 배선이다.
  대화 하나 = codex 세션 하나(DEC-026 D2).
- **같은 conversation 은 한 번에 한 태스크만** 돌린다(back 에서 직렬화). 같은 codex
  세션을 동시에 resume 하는 상황을 만들지 않는다. 다른 대화끼리는 병렬이어도 된다.
- 세션이 없거나 만료면 새 세션으로 시작한다 — 실패시키지 않는다
  ([[decision-024-stage-session-inheritance|KDEV-DEC-024]] D4 와 같은 태도). 대화 기록은
  DB 에 있으므로(DEC-026 D2) 최근 몇 개 메시지를 프롬프트로 동봉해 맥락을 잇는다.

### D3. tool 은 표면 단위 read-only 로만 정의한다

**원칙: 공개 API 가 이미 보여 주는 것 = tool 이 보여 줄 수 있는 것의 상한.**
범용 tool(`run_sql` · `read_file(path)` · 쉘)은 만들지 않는다. md 접근은 반드시
slug 경유 — 서버가 `detail_path` 를 해석하고 공개 문서 루트 밖이면 거부한다.
AI 가 파일 경로를 직접 넘기는 일이 없다.

| tool | 주는 것 | 안 주는 것 |
|---|---|---|
| `get_profile` | 이름 · 위치 · focus · stack · email | — |
| `list_career` / `get_career` | 기간 · 직함 · 조직 · 요약 + 노출 승인된 상세 md | 회사 내부 업무 상세 |
| `list_projects` / `get_project` | 제품 **표면**(제목 · 요약 · 스택 · 상태) + 노출 승인된 showcase | 스펙 · 환경설정 · 배포 구성 · 코드 |
| `list_problems` / `get_problem` | 노출 승인된 problem | 승인 전 problem · 게이트 이력 |
| `search_notes` / `get_note` | 공개 학습노트 | resources · persona (개인 지식) |
| `list_contents` / `list_algorithms` | 공개 목록 | — |

tool 을 만들지 않는 것: `git_token` · `user`/auth · `gate` · `queue` · `company` ·
`daily` 원천(커밋 메시지 · 회고 원문) · 어드민 표면 전부.

### D4. 노출 여부는 `chat_exposed` 옵트인 플래그가 정한다

- 상세 문서를 가진 행(career · project · problem, **+product** — 2026-08-28 개정:
  회사 제품은 `product` 표에 살아 tool 표면에 없던 것이 fix3 조사로 드러났다.
  전용 tool 2종과 함께 옵트인 축을 product 로 확장)에 `chat_exposed` 를 둔다.
  **기본 false** — 어드민에서 켠 것만 tool 응답에 실린다.
- 판정은 **매 tool 호출마다** DB 에서 한다 — 어드민 토글이 실시간으로 먹는다.
  export · 캐시 없음. 꺼진 행은 목록에서 빠지고 상세는 404 다 — AI 에게는
  「존재하지 않는 문서」다.

### D5. 에이전트 표면은 MCP 하나로 좁힌다 — 쉘을 통째로 끈다

*(2026-08-28 개정 — 레퍼런스 `harness_works/mediness-app` landing-chat 의 검증된
계약을 채택. 원안은 stdio 브릿지 + 「마운트 없음으로 방어」였다)*

- **MCP 는 별도 HTTP 서버**(전용 컨테이너)로 둔다 — tool 스키마 정의 + back
  chat-tool API 중계. codex 에는 제출 단위 `-c` 오버라이드로 URL · **turn 전용
  Bearer 토큰** · tool allowlist · 툴별 `approval_mode="approve"` 를 싣는다.
  태스크별 설정 파일이 없고 토큰은 프로세스 인자로만 흐른다.
- **쉘을 끈다**: `features.shell_tool=false` + `web_search="disabled"` +
  `features.apps=false` + `sandbox=read-only`. 쉘이 없으니 컨테이너 bwrap 문제
  자체가 없고, 인젝션이 부릴 손이 MCP tool 뿐이다 — 「마운트 없음」(유지)보다
  한 단계 앞에서 막는다.
- turn 토큰은 제출 때 발급하고 turn 마감 때 폐기한다(best-effort). MCP 서버는
  토큰 없는 호출을 거부한다 — chat-tool API 가 공개 데이터만 준다는 것과 별개로,
  「지금 도는 turn」 만 tool 을 부를 수 있게 한다.
- `CODEX_HOME` 은 기존 워커와 분리 — 파이프라인 세션을 채팅이 resume 하는 사고
  축을 없앤다. **open-kknaks 는 건드리지 않는다**(전부 제출 옵션 · compose 소관).

### D6. 실시간은 상주 소비자 + 이벤트 폴딩으로 — 프론트는 폴링

*(2026-08-28 개정 — 원안 「v1 스트리밍 없음」의 전제(`client.result()` 완료 대기뿐)가
레퍼런스에서 틀렸음이 확인됐다. open-kknaks 는 태스크 이벤트 스트림 구독을 지원한다)*

- back 이 제출 직후 **태스크 전용 상주 소비자**를 띄워 이벤트 스트림(`init` ·
  `text` · `tool_use` · `tool_result` · `result`)을 구독하고 DB 에 폴딩한다 —
  부분 텍스트 누적, tool 호출은 `tool_use_id` 멱등 upsert(+latency), 최종 result 로
  본문 교체. 중복 수신은 정상 경로다(재구독 시 처음부터 다시 온다).
- **프론트는 2초 폴링 유지**(owner 확정, 2026-08-28) — 폴딩된 DB 를 그대로 읽으므로
  부분 텍스트와 tool 단계가 2초 단위로 자라난다. WS 인프라 이식은 하지 않는다.
  체감이 부족하면 WS/SSE 승격은 후속(폴딩 구조는 그대로라 이식 비용이 작다).
- `init` 이벤트의 세션 id 로 `conversation.ai_session_id` 를 확정한다(D2 와 연결).

### 기각

- LLM API 직접 호출(A) · 신규 실행기(C) · 프롬프트 지시만으로 제한(a) ·
  공개 번들 export(b — 어드민 실시간 제어가 안 되고 tool calling 학습 목적에도 안 맞다).

## Rationale

- **판단 기준**: 검증된 것을 재사용하는가, 경계가 지시가 아니라 구조인가, 어드민이
  실시간 제어하는가, owner 가 tool calling 을 배우는가.
- **B+c 인 이유**: 실행은 이미 검증된 것(워커 · resume)을 그대로 쓰고, 새로 설계하는
  힘은 전부 tool 경계에 쓴다 — 이 기능에서 실제로 새로운 문제가 그것뿐이다.
- **D4 를 옵트인으로 한 이유**: 이 레포의 게이트 철학과 같다 — 자동화(AI)가 볼 수
  있는 것은 사람의 승인을 거쳐 생긴다. 실수의 방향이 「덜 보여줌」이지
  「새어 나감」이 아니게 된다.
- **리스크**:
  - codex 세션도 컨테이너 `/tmp` 에 산다면 배포마다 사라진다(DEC-024 OQ-5 와 같은
    축). 채팅은 D2 폴백(DB 기록 동봉)이 받아 주므로 파이프라인보다 관대하다.
  - tool 왕복이 많으면 응답이 길어진다 — tool 설명을 잘 써서 불필요한 호출을
    줄이는 것이 학습 과제 그 자체다.
  - 큐 왕복 + codex 기동으로 첫 응답이 느릴 수 있다 — 실측 후 판단(OQ-2).

## Scope

- In: chat 제출 서비스(back) · MCP 브릿지 · chat-tool API · `chat_exposed` 플래그와
  어드민 토글 · compose 채팅 워커
- Out: 스트리밍(D6 재검토 축) · 레이트리밋(DEC-026 OQ-1) · 기존 파이프라인 워커 변경

## Open Questions

| ID | Question | Owner | Next |
|---|---|---|---|
| OQ-1 | `chat_exposed` 의 단위 — 행 단위로 충분한가, 문서 안 절 단위 마스킹이 필요한가 | kknaks | 행 단위로 시작. 실데이터에서 「반만 보여주고 싶은 문서」가 나오면 재론 |
| ~~OQ-2~~ | 응답 지연 실측 — 큐 왕복 + codex 기동 + tool 왕복의 합 | kknaks | **닫힘 (2026-08-28 로컬 실측)** — 첫 질문(콜드, tool 6회) **~15초** · resume 후속(tool 2회) **~20초**. timeout 180초 충분, 웜 워커·스트리밍 재론 불요 |
| OQ-3 | 시스템 프롬프트에 상시 주입할 요약의 범위(프로필 + 커리어 개요?) | kknaks | spec 에서 확정 |
| ~~OQ-4~~ | 1인칭(「저는」)이냐 비서 톤(「건학님은」)이냐 | kknaks | **닫힘 (2026-08-28)** — **1인칭.** 사이트 컨셉(「제 기록이 직접 대답합니다」)과 일치 |
| ~~OQ-5~~ | codex 모델 · 태스크당 비용 상한 | kknaks | **닫힘 (2026-08-28)** — 모델은 **`gpt-5.6-terra`**(정식 표기 — 레퍼런스 실측: 축약형 `terra` 는 metadata 조회 실패로 400), timeout **180초**. 모델을 바꾸면 `model_reasoning_effort` 허용값도 그 모델 기준으로 다시 잰다 |

## Resulting Spec

| Spec | Action | Notes |
|---|---|---|
| [[spec-017-recruiter-chat\|KDEV-SPEC-017]] | create — **작성됨 (2026-08-28, v0.0.1)** | chat API · tool 계약(스키마) · 세션 매핑 · 노출 판정 시나리오 |
