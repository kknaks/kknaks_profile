---
type: concept
id: viewport-aware-overlay
title: 뷰포트 기준 오버레이 배치 (Viewport-aware Overlay)
aliases:
  - 팝오버 배치
  - 오버레이 뒤집기
  - flip / clamp
  - 뷰포트 안에서 잘리지 않는 팝오버
up:
  - 2026-09-08-sc-design-system
tags:
  - popover
  - overlay
  - layout
  - viewport
---

# 뷰포트 기준 오버레이 배치

팝오버·드롭다운처럼 트리거에 붙어 뜨는 오버레이는 **뷰포트 전체가 아니라 트리거 기준으로 남은 자리**를 재서 열 방향과 최대 높이를 정해야 한다. 그러지 않으면 트리거가 아래쪽에 있을 때 패널이 화면 밖으로 나가고, 밖으로 나간 부분에 스크롤 트랙과 마지막 항목이 들어가 「스크롤이 안 된다」로 보인다.

## 정의

1. 열릴 때 트리거의 `getBoundingClientRect()` 로 **아래 남은 자리**(`viewportHeight - rect.bottom - 여백`)와 **위 남은 자리**(`rect.top - 여백`)를 잰다.
2. 넓은 쪽으로 연다(flip). 기본은 아래.
3. 패널 `max-height = clamp(하한, 그쪽 남은 자리, 상한)` 을 인라인으로 준다. 본문은 `overflow: auto`, 헤더가 있으면 `position: sticky` 로 고정.
4. `resize` 와 `scroll`(capture) 마다 다시 잰다. 내용이 늦게 도착해 높이가 바뀌면 다시 재야 한다 — 제대로는 `ResizeObserver`.
5. `overscroll-behavior: contain` 으로 휠이 뒤 페이지로 새지 않게 하고, 키보드 스크롤을 위해 패널에 `tabIndex=-1`.

## 사용 예시

```ts
// Popover.tsx — 열릴 때·resize·scroll 마다
const rect = trigger.getBoundingClientRect();
const below = window.innerHeight - rect.bottom - EDGE;   // EDGE = 8
const above = rect.top - EDGE;
const openUp = above > below && below < MIN;             // MIN = 160
const room = openUp ? above : below;
panel.style.maxHeight = `${Math.max(MIN, Math.min(room, MAX))}px`; // MAX = 420
```

`MIN`·`MAX`·`EDGE` 세 상수만 디자인 규칙에 맞춰 바꾼다. 디자인 시스템 v2 `14 — OVERLAY` 는 폭(200–400)만 정하고 높이는 정하지 않아 상한 420 은 구현이 정한 값이다.

## 왜 중요한가

`max-height: 60vh` 처럼 뷰포트만 보는 상한은 트리거가 화면 위쪽에 있을 때만 맞는다. 트리거가 아래로 내려갈수록 패널이 화면 밖으로 밀리는데, 패널 자체는 스크롤이 되므로 개발자 도구로는 정상으로 보인다. 사용자는 「목록 끝이 안 보이고 스크롤도 안 된다」고 보고한다. 실측에서 최대 114px 이 화면 밖에 있었다.

## 경계와 오해

- **패널 스크롤 ≠ 패널이 보임** — `overflow: auto` 가 있어도 패널이 뷰포트 밖이면 스크롤 트랙이 밖에 있다. 「스크롤이 안 된다」는 보고는 먼저 패널 위치를 재라.
- **flip 판단 ≠ 「위에 다 들어가는가」** — 패널 높이 전체가 위에 들어가는지로 판단하면 위도 아래도 애매한 자리에서 안 뒤집는다. 「어느 쪽이 더 넓은가」로 판단한다.
- **부모의 `overflow: hidden`** 은 별개 문제다 — 패널이 뷰포트 안에 있어도 부모 패널에 잘린다. 폭이 부모보다 크면 정렬(`right: 0`)이나 폭 축소로 푼다.

## 함께 보는 개념

- [[design-token]] — 상한·하한·여백 값이 디자인 규칙에서 와야 하는 이유

## 출처

- [[2026-09-08-sc-design-system]] — 팝오버 「스크롤 안 됨」 보고의 원인이 60vh 상한이었던 것, 수정 규칙과 상수 3개
