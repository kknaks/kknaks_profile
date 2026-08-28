---
type: baseline
id: KDEV-BL-008
title: "채용담당자 채팅 — 홈에서 질문하면 이력 데이터가 대답한다"
status: accepted
product: kknaks-dev
source:
  type: idea
  ref: ""
links:
  baselines: []
  decisions:
    - "[[decision-025-chat-first-home|KDEV-DEC-025]]"
    - "[[decision-026-anonymous-visitor-session|KDEV-DEC-026]]"
    - "[[decision-027-chat-ai-execution-and-tool-boundary|KDEV-DEC-027]]"
  specs: []
  works: []
  releases: []
  related: []
created_at: 2026-08-28
updated_at: 2026-08-28
tags:
  - product/kknaks-dev
  - doc/baseline
  - status/accepted
---

# 채용담당자 채팅 — 홈에서 질문하면 이력 데이터가 대답한다

포트폴리오 홈을 대화형으로 전면 재구성한다. 채용담당자가 로그인 없이 「이 사람 FastAPI
실무 경험 있나요?」를 치면, 사이트의 이력 데이터(career · projects · problem)가 근거가
되어 대답한다.

> 아직 결정하지 않은 날것의 입력이다. 정리보다 보존이 우선이다.

## Raw

- 핵심 컨셉: **채용담당자가 나에 대해 질문하면 대답해 주는 것.** 페이지를 돌아다니며
  찾는 대신 물어보게 한다.
- 참고 UI 는 회사에서 만든 AX 어시스턴트다 — 흰 화면 중앙에 인사말
  (「안녕하세요, 이건학님」) 하나와 큰 입력창 하나. 그 임팩트 구조를 가져오되 톤은
  이 사이트의 다크 터미널을 유지한다.
- 처음 안은 별도 페이지·플로팅 위젯이었는데 논의 중에 **홈 전면 재구성**으로 커졌다 —
  「홈에서 질문하면 임팩트 있을 것 같은데」.
- 스크롤로 기존 About · Career · Projects … 프리뷰 섹션은 아래에 그대로 잇는다.
- 기술은 준비돼 있다 — open-kknaks 워커(codex + resume)가 이미 파이프라인에서 돌고
  있고, 세션 승계도 [[decision-024-stage-session-inheritance|KDEV-DEC-024]] 로 검증됐다.
- 시각 시안(인터랙티브 목업): `21-html/chat-home-mockup.html` —
  아이들(히어로) · 대화 · /chat 빈 페이지 세 상태를 오간다.

## Context

- 지금 홈은 히어로 터미널(`whoami` 데모) + 프리뷰 섹션이다. 읽는 사람이 원하는 답
  (경험 유무 · 문제 해결 사례)을 찾으려면 스스로 돌아다녀야 한다.
- 이 레포의 파이프라인이 쌓는 데이터 — 특히 `problem`(막혔던 것, 이력서의 알맹이) —
  가 정확히 채용담당자 질문의 답 재료인데, 표면에는 목록으로만 있다.
- 회사에서 AX 어시스턴트(채팅 + 승인 카드)를 만들며 같은 계열 UI 를 이미 다뤄 봤다.

## Why It Matters

- **차별화** — 포트폴리오 사이트에서 본인 이력 데이터로 대답하는 채팅은 그 자체가
  포트폴리오다(백엔드 · AI 파이프라인 · tool calling 을 실물로 보여 준다).
- 쌓아 온 데이터 파이프라인의 **출구**가 생긴다 — 지금까지는 넣는 쪽(캡처 · 잔디 ·
  problem)만 있었다.
- tool calling 을 실전 제약(비회원 · 노출 경계) 아래에서 설계해 보는 학습 목적.

## Possible Direction

- 홈 첫 화면(100vh)을 채팅 히어로로, 아래는 기존 프리뷰 섹션 유지 → DEC-025
- 비회원 식별은 서버 발급 익명 세션 쿠키, IP 는 식별자로 안 쓴다 → DEC-026
- AI 는 기존 open-kknaks 워커 재사용(전용 큐), tool 은 MCP 로 노출하고 경계는
  어드민 옵트인 플래그가 정한다 → DEC-027
