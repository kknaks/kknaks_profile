---
type: decision
id: MK-DEC-002
title: "AI 요약 방식 — open_kknaks(codex) + 단일 방·단일 날짜 + SSE 스트리밍 + 2뷰 데모"
status: accepted
product: mykakao
created_at: 2026-06-15
updated_at: 2026-06-15
tags:
  - product/mykakao
  - doc/decision
  - status/accepted
links:
  baselines:
    - "[[baseline-002-ai-conversation-summary]]"
  decisions: []
  specs:
    - "[[spec-002-ai-conversation-summary]]"
  works: []
  releases: []
  related: []
---

# AI 요약 방식 — open_kknaks(codex) + 단일 방·단일 날짜 + SSE 스트리밍 + 2뷰 데모

추출된 대화를 요약하는 첫 LLM 체인의 호출 방식·컨텍스트 범위·출력 방식·provider·데모 구성을 확정한다.

> baseline의 날것 입력을 spec으로 내리기 전에 적용 방향을 정하는 문서.
> 기능 계약 상세는 `20-spec/`, 실제 작업 순서는 `30-work/`에 둔다.

## Context

- 관련 baseline: [[baseline-002-ai-conversation-summary]]
- 문제/기회: 추출된 대화(BASE-001/DEC-001 체인 완료)에서 "이 방·이 날짜에 뭐가 중요했나"를 LLM으로 요약하는 첫 체인을 연다.
- 결정이 필요한 이유: LLM을 어떻게 부르고(직접 vs 라이브러리), 한 번에 얼마를 보내고(범위), 결과를 어떻게 그리고(출력), 어떤 provider로, 데모를 어떻게 구성할지를 spec으로 내리기 전에 고정해야 한다.

## Options

| Option | Description | Pros | Cons | Notes |
|---|---|---|---|---|
| 호출-A. 직접 subprocess | mykakao 코드가 `codex exec`를 직접 spawn | 의존성 적음 | 큐/재시도/env 표준화 직접 구현, 본진과 패턴 분기 | 기각 |
| 호출-B. open_kknaks 라이브러리 | 패키지로 받아 env(REDIS_URL 등) 설정 + codex provider 워커로 호출 | kknaks_profile 본진(`app/back/service/jobs/llm.py`)과 동일 패턴, 큐/워커 재사용 | 라이브러리·Redis 의존 추가 | **채택** |
| 범위-단일 | 단일 방 × 단일 날짜(하루치) | 토큰 폭증 방지, 단발 요약 목적에 부합 | 방 전체 맥락은 못 봄 | **채택** |
| 범위-전체 | 방 전체 / 멀티데이 | 더 넓은 맥락 | 토큰 폭증, 비용·지연 | 기각 |
| 출력-SSE | `/api/stream` SSE로 스트리밍 렌더 | mykakao에 이미 SSE 인프라 존재, 점진 렌더 | — | **채택** |
| provider | codex / claude | — | — | **codex 채택** (claude 아님) |
| 데모 | 2뷰(목록/요약) | 기존 데모 유지 + 요약 화면 추가 | — | **채택** |

## Decision

사용자가 확정한 5개:

1. **LLM 호출 = `open_kknaks` 라이브러리 채택.** 직접 subprocess 호출이 아니라 패키지로 받아 env 설정(REDIS_URL 등) + codex provider 워커로 호출한다. kknaks_profile 본진과 동일 패턴(`app/back/service/jobs/llm.py`가 `open_kknaks`를 import해 LLM 호출). 라이브러리는 `CodexRunnerAdapter`(= `codex exec --json`)를 제공한다.
2. **컨텍스트 범위 = 단일 채팅방 × 단일 날짜(하루치).** 방 전체/멀티데이 아님. 토큰 폭증 방지 + 단발 요약 목적.
3. **출력 = SSE 스트리밍 렌더.** mykakao backend에 이미 `/api/stream` SSE 인프라(`StreamingResponse`, `text/event-stream`)가 있으므로 재사용한다.
4. **provider = codex.** (claude 아님)
5. **데모 = 2뷰 구성.** (1) 채팅방 목록(현재 데모 유지) → (2) AI 요약 화면.

- 채택: 위 5개.
- 기각: 직접 subprocess 호출(호출-A), 방 전체/멀티데이 범위(범위-전체), provider claude.
- 보류: 아래 Open Questions의 구현 상세 — spec/work 단계에서 결정.

## Rationale

- 판단 기준: 본진 패턴 재사용 + 토큰/비용 통제 + 기존 인프라 활용.
- 대안 대비 이유:
  - open_kknaks는 본진이 이미 쓰는 LLM 호출 표준이라 큐·워커·env 패턴을 그대로 가져온다. 직접 subprocess는 그 표준을 재구현하게 된다.
  - 단일 방·단일 날짜는 단발 요약 목적에 충분하고, 하루치로 끊으면 토큰이 예측 가능하다.
  - SSE는 mykakao에 이미 구축돼 있어 출력 채널을 새로 만들 필요가 없다.
- 리스크:
  - 하루치라도 메시지가 매우 많은 방은 여전히 token cap이 필요할 수 있음 → OQ-3.
  - open_kknaks/Redis/codex 런타임 의존이 추가됨(본인 기기·개인용 전제는 BASE-001과 동일).

## Scope

- In: LLM 호출 방식(open_kknaks/codex), 요약 컨텍스트 범위(단일 방×단일 날짜), 출력 방식(SSE), 데모 2뷰 구성 — 이 4개의 방향 결정까지.
- Out: codex 모델/옵션 구체값, 프롬프트 조립 템플릿, token/size cap 처리, 2뷰 파일 구성(토글 vs 별도 html) — **spec/work 단계에서 결정**. (이번 태스크는 BASE-002 + DEC-002까지만; spec(20)·work(30)·코드는 다음 태스크.)
- 영향을 받는 spec 후보: (예정) AI 요약 기능 spec — DEC-002 확정 후 별도 태스크에서 생성.

## Open Questions

이번 결정에서 의도적으로 발명하지 않은 항목. **4건 모두 사용자 결정으로 closed** (SPEC-002에 반영, PLAN-002-T-002).

| ID | Question | Owner | Status | Resolution |
|---|---|---|---|---|
| OQ-1 | codex 모델/옵션 구체값 | kknaks | closed | model = `gpt-5.5` (tunable). codex provider. → SPEC-002 §BE LLM 호출 계약 |
| OQ-2 | 프롬프트 조립 템플릿 (구분선 포맷 등) | kknaks | closed | `{프롬프트}\n\n---\n[{방}/{date}]\n{HH:MM} {발신자}: {본문}…` 한 줄=한 메시지, 비텍스트 placeholder. → SPEC-002 §Data Contract |
| OQ-3 | 하루치 메시지 과다 시 size/token cap | kknaks | closed | 상한 초과 시 오래된 것부터 truncate + `…(일부 생략됨, 총 N개 중 M개 표시)` 고지. 상한값은 work tunable. → SPEC-002 §Case Matrix/Data Contract |
| OQ-4 | 2뷰: 단일 파일 토글 vs 별도 html | kknaks | closed | 별도 html 2개(`index.html` 목록 → `summary.html` 요약). → SPEC-002 §UX Contract |

## Resulting Spec

| Spec | Action | Notes |
|---|---|---|
| [[spec-002-ai-conversation-summary]] | create | DEC-002 확정 5개 + OQ-1~4 closed 값을 user flow/FE/BE/API/Data 계약으로 구체화. |
