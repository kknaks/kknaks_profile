---
type: concept
id: server-rendered-fragments
title: 서버 렌더 HTML 조각 — 웹은 조각 라우트, JSON 은 앱 전용 (Server-rendered Fragments · HTMX)
aliases:
  - HTMX
  - Jinja2 + HTMX
  - HTML 조각 라우트
  - 서버 렌더 웹
  - 하이퍼미디어
  - 웹 · 앱 API 가르기
up:
  - 2026-11-09-day-data-architecture
tags:
  - frontend
  - 서버 렌더
  - htmx
  - api 경계
---

# 서버 렌더 HTML 조각 — 웹은 조각 라우트, JSON 은 앱 전용

웹 화면을 JSON API + 클라이언트 렌더로 짓지 않고, 서버가 **화면 조각(HTML)을 그려 돌려주고** 브라우저는 그 조각을 제자리에 갈아 끼우기만 하는 방식. HTMX 가 대표 도구다. 같은 서비스에 모바일 앱이 따로 있으면 **JSON API 는 앱 전용**으로 두고 웹은 화면 라우트를 따로 둔다.

## 정의

1. **화면 라우트가 HTML 조각을 준다** — 버튼 · 폼이 `hx-get` · `hx-post` 로 서버를 부르고, 응답 HTML 이 지정한 자리(`hx-target`)를 갈아 끼운다. 템플릿(Jinja2)이 상태 · 권한 표시를 서버에서 다 결정한다
2. **JSON `/api/*` 는 앱 계약이다** — 앱(Flutter)이 쓰는 계약을 웹 사정으로 흔들지 않는다. 둘은 같은 service 를 부르고 표현 계층만 갈린다 → [[layered-architecture]]
3. **서버가 밀어야 할 때는 SSE 가 조각을 보낸다** — 갱신 신호가 오면 조각을 다시 받거나, 이벤트에 실린 조각을 끼운다 → [[server-sent-events]]
4. **폼이 쿠키 세션으로 가므로 CSRF 를 막는다** — 숨은 폼 칸과 헤더로 토큰을 싣는다. DAY 는 사내 기존 관리자 앱과 같은 방식을 그대로 썼다 → [[cookie]] · [[html-form]]

## 사용 예시

DAY 웹(시술 현황 · 로그인):

```text
GET  /board                 → 판 전체 HTML
POST /board/cards/{id}/call → 그 카드 조각 HTML(상태 · 버튼이 바뀐 채)
GET  /api/...               → 앱 전용 JSON(웹은 안 씀)
```

## 왜 중요한가

- **화면 상태와 권한 표시가 서버 한 곳에 남는다** — 앱과 웹이 같은 JSON 을 쓰려 하자, 「이 사람에게 이 버튼을 보일까」 「이 카드는 지금 어떤 모양인가」 를 클라이언트마다 다시 판단해야 했다. 조각을 서버가 그리면 그 판단은 템플릿 한 곳이다 → [[server-authoritative-transition]]
- **빌드 도구 · 클라이언트 상태 관리가 없다** — 사내 컴포넌트 묶음(HTMX 용)을 그대로 쓰고, 화면 하나가 템플릿 하나다

## 경계와 오해

- **SPA 를 대신하는 만능이 아니다** — 오프라인 · 복잡한 클라이언트 상호작용(끌어 놓기 계산 같은)은 여전히 JS 몫이다. DAY 도 카드 끌어 놓기는 작은 스크립트로 둔다 → [[script-loading]]
- **조각을 갈아 끼우는 자리는 서버 계약이다** — 응답 조각의 바깥 요소 id 가 바뀌면 화면이 조용히 깨진다. JSON 스키마만큼 조각 경계도 계약으로 다룬다
- **서버 렌더라도 출력 이스케이프는 템플릿이 한다** — 자동 이스케이프를 끄는 자리가 XSS 의 입구다 → [[output-escaping]]
- **[[rest-api]] 를 버리는 것이 아니다** — 앱 계약은 그대로 JSON 이다. 가른 것은 「누가 쓰는 표면인가」 다

## 누른 카드만 갈아 끼우기 — version 과 OOB

버튼 응답이 판 전체 조각을 다시 그리고 실시간 신호로 한 번 더 그리면, 다른 카드까지 깜빡이고 메뉴가 늦게 뜬다. 응답 = 누른 카드 조각 + OOB(숫자 · 사이드) + 판 version, 실시간 신호는 version 만. 받는 쪽은 **자기 조작으로 받은 version 만** 건너뛴다 — 응답 version 을 「다 봤다」로 쓰면 그보다 작은 남의 변경 신호를 놓친다. 앱이 같은 version 을 소비하면 뜻(판이 바뀔 때만 오름 · 같은 값은 받음)을 한 번에 맞춘다.

## 함께 보는 개념

- [[server-sent-events]] — 조각을 밀어 보내는 통로
- [[server-authoritative-transition]] — 화면이 규칙을 따로 들지 않는다는 같은 축
- [[layered-architecture]] — 웹 · 앱 표현 계층이 같은 service 를 부른다
- [[html-form]] — 조각 요청의 기본 단위
- [[cookie]] — 웹 세션이 실리는 곳, CSRF 가 생기는 이유

## 출처

- [[2026-11-09-day-data-architecture]] §2 — DAY 웹 = Jinja2 + HTMX + SSE · 화면 라우트 HTML 조각 · JSON `/api/*` 는 앱 전용 · CSRF 는 사내 기존 관리자 앱 방식(코드 `9c7376ca` · `3cbb2e08` · 결정 2026-11-06)
- [[2026-11-11-day-procedure-board-2]] §2 — DAY 시술 현황 #236 v3 · 로컬 확인 F7 · F8 · 리뷰 W1 · 앱 스펙과 version 뜻 맞춤(`review-236v3-report.md` · `review-doc-merge921-report.md` F1)
