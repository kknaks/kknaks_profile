---
type: concept
id: css-specificity
title: CSS 명시도와 cascade — 동률이면 뒤가 이긴다
aliases:
  - 명시도
  - CSS 명시도
  - specificity
  - cascade
  - 캐스케이드
  - 선택자 우선순위
up:
  - 2026-10-03-strong-hajin-polish2
tags:
  - frontend
  - css
  - design-system
---

# CSS 명시도와 cascade — 동률이면 뒤가 이긴다

한 요소에 같은 속성을 정하는 규칙이 여럿이면 브라우저는 **명시도(선택자의 무게)가 높은 쪽**을 고르고, **명시도가 같으면 나중에 선언된 쪽**을 고른다. 「덮어썼는데 어떤 상태에서만 옛 색이 나온다」는 버그는 대개 **그 상태에서만 덮어쓰기가 빠지고, 남은 둘이 동률이 되어 순서로 갈린 것**이다.

## 정의

- 명시도는 `(id, class·속성·가상 클래스, 요소)` 세 자리 수로 센다. `.a:hover` = (0,2,0), `.scope .a:hover` = (0,3,0)
- `:not(X)` 는 그 자체로 세지 않고 **안에 든 선택자의 무게만큼** 더한다 — `.a:hover:not(:disabled)` = (0,3,0)
- 비교 순서: 중요도(`!important`) → 명시도 → **선언 순서(나중이 이긴다)**. 순서는 **스타일시트 로드 순서**까지 포함한다

## 사용 예시

채팅 서랍 안 사람 행동 단추를 검정으로 덮었는데 「등록 중…」이 파랗게 보였다. 덮어쓰기는 `.scax-drawer--chat .scax-button--solid-primary:not(:disabled)` — 비활성에는 안 걸린다. 진행 중이라 비활성 + 포인터가 위에 있으면 DS 의 두 규칙만 남는다.

| 규칙 | 명시도 | 결과 |
|---|---|---|
| `.scax-button:disabled` | (0,2,0) | 회색 |
| `.scax-button--solid-primary:hover` (`:not(:disabled)` 없음) | (0,2,0) | 파랑 |

동률이라 **뒤에 선언된 hover 가 이겼다.** 포인터를 치우면 회색이 되므로 「가끔 파랗다」로 보인다. DS 원본을 고치면 앱 전체가 바뀌므로 **서랍 스코프(0,3,0)로 비활성·hover 상태까지 덮고**, DS 의 결함(hover 에 `:not(:disabled)` 가 없음)은 별도 미결로 남겼다.

## 왜 중요한가

- 상태 조합(비활성 × hover × 포커스)마다 이기는 규칙이 달라진다. **기본 상태만 보고 「덮었다」고 판정하면** 조합 하나에서 새는 것을 못 본다 — 상태 × 규칙 표를 그려야 보인다
- 디자인 시스템 위에 화면별 예외를 얹는 구조에서는 **원본을 안 건드리고 더 무거운 스코프로 덮는 것**이 기본 수단이고, 그 무게 계산이 이 규칙이다 → [[design-system]]

## 경계와 오해

- **「나중 파일이 이긴다」는 동률일 때만 참이다** — 명시도가 높으면 먼저 선언돼도 이긴다
- **jsdom 은 CSS 를 적용하지 않는다** — 단위 테스트로는 계산된 색을 못 본다. 테스트는 규칙 원문·명시도 계산·렌더된 클래스로 단언하고, 실제 색은 실브라우저(Playwright)에서 `getComputedStyle` 로 찍어 확인한다
- **`!important` 로 이기는 것은 해결이 아니다** — 다음 덮어쓰기도 `!important` 를 요구하게 만든다

## 함께 보는 개념

- [[design-system]] · [[design-token]]

## 출처

- [[2026-10-03-strong-hajin-polish2]] §2 — Strong Hajin WORK-009 E2E-3(`fe-survey-report.md` §3 상태 × 규칙 표 · `review-fe-p2a2-report.md` · 커밋 `d1bb87d`), DS 결함은 OQ-901
