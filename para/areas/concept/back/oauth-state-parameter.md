---
type: concept
id: oauth-state-parameter
title: OAuth 일회용 state
aliases:
  - OAuth state
  - state 파라미터
  - OAuth 콜백
  - 사용자 토큰
  - user token
up:
  - 2026-10-07-strong-hajin-inbox
tags:
  - OAuth
  - 인증
  - 연동
  - 데스크톱
---

# OAuth 일회용 state

OAuth 동의 화면으로 보낼 때 서버가 **한 번만 쓰는 무작위 값(state)** 을 만들어 실어 보내고, 콜백에서 돌아온 state 로 **이 콜백이 누구의 어떤 요청에서 시작됐는지**를 찾는 것. 위조 콜백(CSRF)을 막고, 쿠키가 없는 환경에서도 회원을 잇는다.

## 정의

1. 연결 시작 — 서버가 state 를 만들어 (회원 · 채널 · 만료) 와 함께 저장하고, state 를 실은 동의 URL 을 돌려준다
2. 사용자가 상대 서비스에서 동의 → 상대가 `code` 와 `state` 를 붙여 콜백으로 보낸다
3. 콜백 — state 로 저장된 행을 찾아 회원을 정하고 **즉시 지운다**(일회용). 없거나 만료면 거절
4. `code` 를 토큰으로 바꿔 그 회원의 연결로 저장한다

## 사용 예시

데스크톱 앱(웹뷰) 안에서 「연결」을 누르면 동의는 **외부 브라우저**에서 진행된다. 외부 브라우저에는 앱의 세션 쿠키가 없으므로 콜백은 쿠키로 회원을 알 수 없다 — state 가 회원을 찾는 유일한 끈이다.

같은 자리에서 셸이 `/api/` 이동을 가로채 302 를 따라가지 않는 문제가 있었다 → 동의 URL 을 302 대신 **JSON 으로 받아** 셸이 외부 브라우저로 연다 → [[webview-attachment-download]]

## 왜 중요한가

- state 가 없으면 남이 만든 콜백 링크로 **내 계정에 남의 자격이 연결**될 수 있다
- 「사용자 토큰」을 쓰는 이유도 같은 흐름에서 정해진다 — 슬랙 DM·그룹 DM 은 봇이 들어가 있지 않아 봇 토큰으로 못 읽는다. 사람마다 자기 토큰으로 연결해야 그 사람이 보는 것을 읽는다 → [[per-user-fanout]]

## 경계와 오해

- **state ≠ 세션** — 세션은 오래 살고 state 는 콜백 한 번에 쓰이고 사라진다
- **가짜 code 로 비밀값을 검증하지 않는다** — 일부 서비스는 진짜 code 일 때만 Client Secret 을 확인한다. 가짜 code 로 「invalid_code」 가 나오면 비밀값이 맞아서가 아니라 **비밀값을 보기 전에 끝난 것**이다. 비밀값 확인은 실제 동의 흐름 한 번으로만 → [[dev-prod-parity]]
- PKCE 와는 다른 장치다 — PKCE 는 code 가로채기를 막고, state 는 콜백 위조와 요청 식별을 맡는다

## 함께 보는 개념

- [[refresh-token-rotation]] — 연결 뒤 토큰 갱신의 성질
- [[cookie]] — 콜백에서 기대할 수 없는 것
- [[external-api-error-classification]] — 저장한 토큰을 언제 폐기로 볼지

## 출처

- [[2026-10-07-strong-hajin-inbox]] §2·§3 — Strong Hajin WORK-011 슬랙·메일 연결(review-spec-008-009 F-2 · 비밀값 재발급 사고)
