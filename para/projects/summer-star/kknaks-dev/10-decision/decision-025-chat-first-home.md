---
type: decision
id: KDEV-DEC-025
title: "홈 전면 재구성 — 채팅 퍼스트 히어로와 /chat 페이지"
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
    - "[[decision-026-anonymous-visitor-session|KDEV-DEC-026]]"
    - "[[decision-027-chat-ai-execution-and-tool-boundary|KDEV-DEC-027]]"
  specs:
    - "[[spec-017-recruiter-chat|KDEV-SPEC-017]]"
  works: []
  releases: []
  related: []
up: []
---

# 홈 전면 재구성 — 채팅 퍼스트 히어로와 /chat 페이지

홈 첫 화면을 채팅 입력 하나로 재구성한다. 질문을 보내면 `/chat` 으로 이동해 대화가
시작되고, 스크롤하면 기존 프리뷰 섹션이 그대로 이어진다.

## Context

- 관련 baseline: [[baseline-008-recruiter-chat|KDEV-BL-008]]
- 처음 논의는 「어디에 채팅을 넣나」였다 — 별도 페이지 · 플로팅 위젯 · 히어로 연동이
  후보였는데, owner 가 홈 전면 재구성으로 방향을 키웠다.
- 시안을 인터랙티브 목업으로 만들어 세 상태(히어로 · 대화 · /chat 빈 페이지)를
  확인하고 확정했다 — `21-html/chat-home-mockup.html`.

## 근거 개념

- 없음 — UI 구성 판단이라 기대는 개념이 없다. 시안 확인으로 결정했다.

## Options

### 채팅의 자리

| Option | Description | Pros | Cons | Notes |
|---|---|---|---|---|
| A | 별도 페이지(`/chat`)만 · 네비 메뉴 추가 | 홈 무변경 | 발견성이 낮다 — 탭 하나로는 안 눌러 본다 | 기각 |
| B | 플로팅 위젯 (우하단 버튼) | 모든 페이지에서 접근 | 상담봇처럼 보인다. 임팩트 없음 | 기각 |
| **C** | **홈 첫 화면 전체를 채팅 히어로로** | 첫인상이 곧 기능 시연. 참고 UI(AX)의 임팩트 구조 | 기존 히어로 터미널을 대체한다 | **채택** |

### 히어로 아래

| Option | Description | Pros | Cons | Notes |
|---|---|---|---|---|
| a | 홈 = 채팅뿐 | 가장 강한 임팩트 | 첫 방문자가 다른 콘텐츠의 존재를 놓친다 | 기각 |
| **b** | **스크롤로 기존 프리뷰 섹션 유지** | 채팅을 안 쓰는 방문자의 기존 동선 보존 | 히어로가 정확히 100vh 여야 한다 | **채택** |

## Decision

### D1. 홈 첫 화면 = 채팅 히어로 한 화면

- 인사말(「안녕하세요, 이건학입니다. 무엇이든 물어보세요.」) + 터미널 스타일 입력창
  (`~/kknaks — ask`, `$` 프롬프트) + 하단 `scroll ↓` 큐.
- 추천 질문 칩은 두지 않는다 — OQ-2 에서 owner 가 뺐다(2026-08-28). 입력창 하나가
  초점이다. placeholder 예시 질문이 유도 역할을 대신한다.
- 기존 히어로 터미널(`whoami` 데모)은 **폐기한다** — 터미널 컨셉은 입력창이 계승한다.
- 스크롤하면 기존 `LandingPreview` 섹션(01 About ~ 05 Contents)이 그대로 이어진다.
  섹션 자체는 이번 범위에서 바꾸지 않는다.

### D2. 대화는 `/chat` 페이지에서 한다 — 사이드바 + 새 대화

- 홈에서 질문을 보내면 `/chat` 으로 이동하며 첫 질문이 바로 전송된다(새 대화 생성).
- 네비에 채팅 탭을 추가한다(`00 Ask`). 탭으로 직접 들어가면 빈 채팅 페이지 —
  히어로와 같은 구성(인사말 + 입력창)이되 스크롤 섹션은 없다.
- **대화는 여러 개다** — 좌측 사이드바에 「+ 새 대화」와 이 방문자(세션)의 대화
  목록을 둔다(OQ-1 닫힘, 2026-08-28). 주제별로 갈라 물을 수 있다. 대화 제목은
  첫 질문에서 딴다.
- 대화 뷰: 질문은 `$ ask "…"` 커맨드 줄, 답변은 출력 블록, 답변 끝에 **근거 카드**
  (AI 가 실제로 읽은 career · project · problem 의 페이지 링크).

### D3. 톤은 기존 디자인 토큰을 그대로 계승한다

- `globals.css` 토큰(다크 배경 · 그린 액센트 · 모노스페이스) 외에 새 색 · 새 폰트를
  들이지 않는다. 참고 UI(AX)에서 가져오는 것은 「중앙 인사말 + 큰 입력창」 구조뿐이다.

### 기각

- 별도 페이지만(A) · 플로팅 위젯(B) · 홈에서 섹션 제거(a).
- 히어로 터미널과 채팅 입력창을 병존시키는 절충안 — 첫 화면에 초점이 둘이 된다.

## Rationale

- **판단 기준**: 첫인상에서 기능이 보이는가, 채팅을 안 쓰는 방문자의 동선이 남는가.
- **C 인 이유**: 이 채팅은 부가 기능이 아니라 사이트의 셀링 포인트다 — 본인 이력
  데이터로 대답하는 채팅 자체가 포트폴리오라서, 숨겨 두면 만든 의미가 없다.
- **리스크**: 첫 화면에서 정적 소개(스택 · 커리어 요약)가 사라진다 — 스크롤 섹션과
  입력창 placeholder 예시 질문이 그 역할을 나눠 받는다.

## Scope

- In: 홈(`app/front/app/page.tsx` · `components/home/`) 재구성 · `/chat` 페이지 신설 ·
  네비(`components/shell/topnav.tsx`) 탭 추가
- Out: 프리뷰 섹션 내용 변경 · About 등 다른 페이지 · 어드민 화면(DEC-027 쪽)

## Open Questions

| ID | Question | Owner | Next |
|---|---|---|---|
| ~~OQ-1~~ | 대화 이력을 사이드바로 보여줄지, 한 세션 = 한 스레드로 갈지 | kknaks | **닫힘 (2026-08-28)** — 사이드바 + 새 대화. D2 에 반영. `conversation` 이 세션과 분리된다(DEC-026 D2) |
| ~~OQ-2~~ | 추천 질문 칩을 하드코딩할지 DB 로 둘지 | kknaks | **닫힘 (2026-08-28)** — **칩 자체를 뺀다.** 질문의 전제(어디서 관리하나)가 무효. D1 에 반영 |
| ~~OQ-3~~ | 모바일 레이아웃 — 사이드바·문서 패널 | kknaks | **닫힘 (2026-08-28)** — 왼쪽 햄버거(사이드바 드로어) + 오른쪽 드로어(문서 패널). spec v0.0.13 U-4 |

## Resulting Spec

| Spec | Action | Notes |
|---|---|---|
| [[spec-017-recruiter-chat\|KDEV-SPEC-017]] | create — **작성됨 (2026-08-28, v0.0.1)** | 홈 히어로 · /chat · 대화 뷰의 UX Contract 와 시나리오 |
