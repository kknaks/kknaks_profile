---
type: decision
id: DEC-005
title: "배포 = 내부 공유용 데모 — Vercel + 홈서버, 가드는 공유 비밀번호 하나"
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
    - "[[spec-003-api-and-chat-contract|SPEC-003]]"
    - "[[spec-004-three-screens|SPEC-004]]"
  works: []
  releases: []
  related: []
up:
  - container
  - reverse-proxy
---

# 배포 = 내부 공유용 데모 — Vercel + 홈서버, 가드는 공유 비밀번호 하나

이 데모를 **내부 공유용**으로 배포한다. 프론트는 Vercel(기존 profile 배포에 포함), 백엔드 +
redis + open-kknaks codex 워커는 홈서버(docker + NPM 서브도메인). 접근 가드는 공유 비밀번호
하나뿐이고, 배포 DB 사본은 홈서버 볼륨(레포 밖)에 둔다.

> baseline의 날것 입력을 spec으로 내리기 전에 적용 방향을 정하는 문서.
> 기능 계약 상세는 `20-spec/`, 실제 작업 순서는 `30-work/`에 둔다.

## Context

- 관련 baseline: [[baseline-001-demo-agent-app|BASE-001]]
- [[decision-004-web-three-pages-in-front|DEC-004]] 로 화면이 `app/front/` 안으로 들어갔다 —
  프론트는 기존 profile 배포 경로(Vercel)를 그대로 탄다.
- [[decision-003-llm-via-open-kknaks-mcp|DEC-003]] 로 실행 경로에 redis 와 codex 워커가
  붙는다 — Vercel 에 올릴 수 없는 상주 프로세스다.
- [[decision-002-pii-masking-boundary|DEC-002]] 는 **내부 공유용이라는 전제** 위에 서 있다.
  그 전제를 확정하는 것이 이 결정이다.
- 결정이 필요한 이유: 「누구에게 열리는가」가 정해져야 가드의 수준과 DB 사본의 위치가 정해진다.

## Options

| Option | Description | Pros | Cons | Notes |
|---|---|---|---|---|
| A | 로컬 전용 — 배포하지 않고 화면 공유로만 보여 준다 | 노출 위험 0 · 배포 작업 없음 | 남에게 눌러 보게 할 수 없다 — 데모의 목적이 반감 | 기각 |
| **B** | **내부 공유용 배포 — Vercel(프론트) + 홈서버(백·redis·워커), 공유 비밀번호 하나** | 링크 하나로 눌러 보게 한다 · 기존 배포 경로 재사용 | 가드가 얇다(비밀번호 하나) — 링크가 퍼지면 그대로 열린다 | **채택** |
| C | 외부 공개 — 가드 없이 열고 rate limit·토큰 상한 등으로 방어 | 포트폴리오 표면이 된다 | PII 전제(DEC-002)가 바뀐다 · 비용·남용 가드를 전부 만들어야 한다 — 이번 범위 아님 | 기각 |

## Decision

### D1. 배포 표면 — 프론트 Vercel · 백 홈서버

- **프론트**: Vercel — 기존 profile 배포에 포함한다(별도 배포 경로를 만들지 않는다).
- **백엔드 + redis + open-kknaks codex 워커**: 홈서버, docker + NPM 서브도메인.

### D2. 접근 가드는 공유 비밀번호 하나

- 내부 공유용이므로 **공유 비밀번호 하나**로 막는다.
- 채팅 rate limit · 토큰 상한 등 **추가 가드는 두지 않는다.**

### D3. 배포 DB 사본은 홈서버 볼륨 — 레포 밖

- 배포용 DB 사본은 홈서버 볼륨에 둔다. 원천 데이터·DB 는 gitignore 정책을 그대로 유지한다.

### D4. 「실시간」 표방 금지

- 원천이 일 배치이므로 갱신 주기는 일 1회다. 화면·카피에서 「실시간」이라고 하지 않는다.

### 기각

- 배포 없음(A) · 외부 공개(C).

## Rationale

- **판단 기준**: 남이 눌러 볼 수 있는가, 노출 범위에 맞는 가드인가, 기존 배포 경로를 쓰는가.
- **B 인 이유**: 이 데모의 목적은 「과정 전체가 탐색 가능함」을 보여 주는 것이라 눌러 보게
  해야 의미가 있다. 동시에 데이터가 실데이터(마스킹해도 실적 수치)라 외부 공개는 다른 문제다 —
  내부 공유가 그 사이의 자리다.
- **가드를 하나로 둔 이유**: 보는 사람이 한정된 내부 공유에서 rate limit·토큰 상한까지 만들면
  이번 범위(데모 구축)를 넘는다. 가드를 늘려야 할 때는 **공개 범위가 바뀔 때**이고, 그때는
  [[decision-002-pii-masking-boundary|DEC-002]] 도 같이 재검토 대상이다.
- **리스크**
  - 비밀번호가 퍼지면 그대로 열린다 — 외부 공개 전환 시 DEC-002·이 결정을 함께 다시 본다.
  - 가드가 없으므로 LLM 호출 비용이 사용량을 그대로 따라간다.
  - 홈서버 의존 — 홈서버가 내려가면 채팅·API 가 전부 멈춘다(프론트만 살아 있다).

## 근거 개념

- [[container]] — 백·redis·워커를 docker 로 묶어 홈서버 한 대에 올리는 구성의 근거.
- [[reverse-proxy]] — NPM(Nginx Proxy Manager) 서브도메인으로 도메인·인증서·포트를 앞단에서
  정리하고 애플리케이션은 안쪽 포트만 보게 하는 배치가 이 개념 그대로다.

## Scope

- In: Vercel 프론트 배포 편입, 홈서버 docker 구성(백·redis·워커), NPM 서브도메인,
  공유 비밀번호 가드, 배포 DB 사본 위치
- Out: rate limit · 토큰 상한 · 계정 체계(두지 않기로 함), 외부 공개 전환,
  수집 자동화·알림 발송
- 영향을 받는 spec 후보: 배포 구성, 접근 가드

## Open Questions

| ID | Question | Owner | Next |
|---|---|---|---|
| ~~OQ-1~~ | 비밀번호 가드를 어디에 두나(프론트 미들웨어 · 백 API · NPM 중 어디) | kknaks | **닫힘 (2026-09-02 확정)** — env 난수 비밀번호 1개(값은 배포 시 주입) · 가드는 **프론트 미들웨어 + 백 API 양쪽**. NPM Basic Auth 는 쓰지 않는다(폴링·쿠키와 어긋난다). 계약은 SPEC-003 §4·§5, 화면은 SPEC-004 U-2 |

## Resulting Spec

| Spec | Action | Notes |
|---|---|---|
| [[spec-003-api-and-chat-contract\|SPEC-003]] | create — **작성됨 (2026-09-02, v0.0.2 ready)** | 접속 게이트 계약(env 비밀번호 1개 · 세션 `ontology_demo_sid` 30일) · rate limit 부재 명시 |
| [[spec-004-three-screens\|SPEC-004]] | create — **작성됨 (2026-09-02, v0.0.1 draft)** | 접속 게이트 **화면**(U-2) |
