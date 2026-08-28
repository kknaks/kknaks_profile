---
type: decision
id: KDEV-DEC-026
title: "비회원 방문자 식별 — 서버 발급 익명 세션 쿠키"
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
    - "[[decision-027-chat-ai-execution-and-tool-boundary|KDEV-DEC-027]]"
  specs:
    - "[[spec-017-recruiter-chat|KDEV-SPEC-017]]"
  works: []
  releases: []
  related: []
up:
  - http-session
---

# 비회원 방문자 식별 — 서버 발급 익명 세션 쿠키

채용담당자는 로그인 없이 채팅을 쓴다. 첫 방문에 서버가 익명 세션 ID 를 발급해
httpOnly 쿠키로 심고, 대화를 그 세션에 묶는다. IP 는 식별자로 쓰지 않는다.

## Context

- 관련 baseline: [[baseline-008-recruiter-chat|KDEV-BL-008]]
- 「비회원인데 어떻게 구별하지 — 아이피? 세션아이디?」가 출발 질문이다.
- 식별이 필요한 이유를 갈랐더니 셋이었다 — ① 대화 연속성, ② 어뷰징·비용 방어,
  ③ 누가 물어봤는지(분석). **이 결정은 ① 만 다룬다** — owner 가 「1 만 먼저」로
  범위를 잘랐다.

## 근거 개념

- [[http-session]] — 이 결정이 그대로 이 구조다. 상태(대화)는 서버가 갖고,
  클라이언트는 열쇠(세션 ID 쿠키)만 갖는다. 열쇠를 잃으면(쿠키 삭제) 새 손님이
  된다는 성질까지 동일하다.

## Options

| Option | Description | Pros | Cons | Notes |
|---|---|---|---|---|
| A | IP 주소로 식별 | 구현 제로 | 회사 사무실은 NAT — 채용담당자 여럿이 같은 IP. 모바일은 수시로 바뀜 | 기각 |
| B | localStorage 에 클라이언트 발급 ID | 서버 무상태 | SSR 이 첫 렌더에서 못 읽는다. 값 위조 가능 — 신뢰 경계가 클라이언트 | 기각 |
| **C** | **서버 발급 UUID + httpOnly 쿠키** | SSR 즉시 읽음 · 발급/검증이 back 한 곳 · JS 접근 차단 | 쿠키 삭제 시 대화 유실 | **채택** |

## Decision

### D1. 첫 채팅 요청 때 서버가 익명 세션을 발급한다

- back 이 UUID 를 발급, `httpOnly` + `SameSite=Lax` + `Secure` 쿠키로 심는다.
- 사이트 열람만으로는 발급하지 않는다 — **채팅 첫 사용이 발급 시점**이다. 쿠키
  안 쓰는 방문자에게 세션 row 를 만들지 않는다.
- 만료는 30일, 사용할 때마다 연장(sliding).

### D2. 대화는 세션에 묶여 서버 DB 에 남는다

- 새 테이블 셋: `chat_session`(익명 세션) 1:N `conversation`(대화) 1:N
  `chat_message`(메시지). 컬럼 전문은 코드/migration 이 SoT — 여기 안 쓴다.
- 세션과 대화를 가르는 이유: 한 방문자가 대화를 여러 개 만든다
  ([[decision-025-chat-first-home|KDEV-DEC-025]] D2 사이드바 + 새 대화). AI 세션
  참조(`ai_session_id`)는 **conversation 이 갖는다** — 대화 하나가 codex 세션
  하나다.
- 재방문(쿠키 유효) 시 이전 대화 목록이 그대로 보인다. AI 쪽 맥락 연속은
  [[decision-027-chat-ai-execution-and-tool-boundary|KDEV-DEC-027]] D2(세션 매핑)가 받는다.
- 대화 기록은 어드민에서 열람한다 — 무엇이 질문됐는지가 운영 데이터다.

### D3. 신원 파악은 하지 않는다

- 어느 회사의 누구인지 묻지도, 추정하지도 않는다. 소속 입력란 같은 마찰을 두지
  않는다. 남기는 것은 대화 내용과 시각뿐이다.

### 기각·보류

- IP 식별(A) · localStorage(B) 기각.
- **어뷰징·비용 방어(레이트리밋)는 이 결정 밖이다** — 쿠키는 지우면 그만이라 세션
  ID 는 방어 단위가 못 되고, IP+세션 이중 제한은 별도 결정으로 미룬다(OQ-1).
  단 **공개 배포 전에는 있어야 한다** — LLM 호출이 비용이다.

## Rationale

- **판단 기준**: 신뢰 경계가 서버에 있는가, SSR 과 맞물리는가, 로그인 없는 UX 를
  해치지 않는가.
- **C 인 이유**: 식별자 발급·검증·만료가 전부 back 한 곳이고, 프론트는 쿠키를
  만질 코드가 아예 없다. 계층 규약(신뢰는 아래층)과도 맞다.
- **리스크**: 쿠키 삭제·시크릿 모드 → 대화 유실. 비회원 채팅에서 수용한다 —
  복구 수단(로그인)을 만드는 것이 더 큰 마찰이다.

## Scope

- In: 세션 발급/검증(back) · `chat_session` · `conversation` · `chat_message` · 쿠키 계약
- Out: 레이트리밋(OQ-1) · 방문 분석 · 관리자 인증(별개 축, SPEC-006)

## Open Questions

| ID | Question | Owner | Next |
|---|---|---|---|
| OQ-1 | 레이트리밋 설계 — 세션+IP 이중 제한 · 대화당 메시지 상한 · 입력 길이 상한 | kknaks | 별도 결정. **공개 배포 전 필수** |
| OQ-2 | 쿠키 고지 — 필수 기능 쿠키라 동의 배너까지는 불요라고 보는데, 표기는 할지 | kknaks | spec 전에 확정 |
| OQ-3 | 오래된 세션·대화의 보존 기한(정리 배치) | kknaks | 운영 데이터가 쌓인 뒤 판단 |

## Resulting Spec

| Spec | Action | Notes |
|---|---|---|
| [[spec-017-recruiter-chat\|KDEV-SPEC-017]] | create — **작성됨 (2026-08-28, v0.0.1)** | 세션 쿠키 계약 · 대화 연속성 시나리오 포함 |
