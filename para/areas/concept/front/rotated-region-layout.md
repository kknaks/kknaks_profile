---
type: concept
id: rotated-region-layout
title: 마주 보는 화면 — 레이아웃 한 벌 + 영역째 회전 (Rotated Region Layout)
aliases:
  - 마주 보는 화면
  - 영역 회전
  - 180도 회전
  - 뒤집힌 화면
  - 포탈은 회전을 못 받는다
  - face-to-face UI
up:
  - 2026-10-27-interpret-pwa-poc
tags:
  - 레이아웃
  - css transform
  - portal
  - 통역
---

# 마주 보는 화면 — 레이아웃 한 벌 + 영역째 회전

폰 하나를 가운데 두고 두 사람이 마주 보고 쓰는 화면은, 반대편 사람 몫의 영역을 **바로 선 기준으로 한 번만 짜고 그 영역을 통째로 180° 돌린다.** 「뒤집힌 화면」 을 따로 짜지 않는다. 대신 그 영역 밖에 그려지는 것(포탈 오버레이)은 회전을 받지 못한다.

## 정의

1. **한 벌만 짠다** — 외국어 영역도 상담사 영역과 같은 컴포넌트 · 같은 배치로 짜고 `rotate(180deg)` 만 건다. 말풍선은 「보는 사람 기준 내 말은 오른쪽」 이므로 회전하면 자동으로 맞는다
2. **회전은 DOM 조상에게서 상속된다** — `transform` 은 그 요소의 **하위 DOM** 에만 걸린다. `body` 로 포탈되는 팝오버 · 목록 · 토스트는 회전 영역 밖이라 **바로 선 채** 펼쳐진다
3. **포탈을 끌 수 없으면 영역 안 자체 목록** — 통키는 medikit ComboBox 가 목록을 Popover portal 로 body 에 붙이고 끄는 prop 이 없어서, 외국어 카드 안에 자체 목록을 만들었다. 높이는 카드 안 남은 높이(`offsetTop` — 회전과 무관한 레이아웃 값)까지, 넘으면 목록 안 스크롤
4. **가운데 공용 줄은 돌리지 않는다** — 원 · 모드 단추처럼 양쪽이 같이 보는 것은 회전 없이 둔다

## 사용 예시

```tsx
<main className="flex h-dvh flex-col">
  <section className="flex-1 rotate-180">   {/* 손님 쪽 — 같은 컴포넌트 */}
    <ConversationPane side="guest" />
    <LangSelect inline />                   {/* 포탈 없이 카드 안 목록 */}
  </section>
  <CenterControls />                        {/* 회전 없음 */}
  <section className="flex-1">
    <ConversationPane side="me" />
  </section>
</main>
```

## 왜 중요한가

- 두 벌로 짜면 한쪽만 고쳐지는 순간 두 모드가 어긋난다. 회전 한 줄이면 화면 수정은 한 곳이다
- 포탈 함정은 **데스크톱 미리보기에서 잘 안 보인다** — 실기기에서 목록이 바로 선 채 펼쳐져 손님이 뒤집힌 글자를 읽게 됐다

## 경계와 오해

- **포탈이 조상의 맥락을 벗어나는 같은 뿌리** — [[portal-inside-scroll-lock]] 은 스크롤 잠금을, 여기는 `transform` 을 벗어난다. 포탈 컨테이너를 회전 영역 안으로 옮길 수 있으면 그게 같은 해법이다(그 경우 `position: fixed` 기준이 transform 조상으로 바뀌는 것을 확인)
- **회전 ≠ 기기 방향 전환** — 화면 방향(orientation)은 전체가 돈다. 여기는 화면의 절반만 돈다
- [[proportional-ui-scale]] 과 다르다 — 크기가 아니라 방향 문제

## 함께 보는 개념

- [[portal-inside-scroll-lock]] — 포탈이 조상 맥락을 벗어나는 다른 경우
- [[viewport-aware-overlay]] — 오버레이 위치를 남은 자리로 정하기
- [[ios-input-auto-zoom]] — 같은 실기기 피드백에서 나온 iOS 입력 함정
- [[design-system]] — 부품의 portal 을 끄는 prop 이 DS 요청 후보

## 출처

- [[2026-10-27-interpret-pwa-poc]] §2 — 외국어 영역 180° · 말풍선 · medikit ComboBox 목록이 body 포탈이라 회전을 못 받아 카드 안 자체 목록(`front/components/interpret/LangSelect.tsx` · `InterpretScreen.tsx` · `fix-phone3-fe-report.md` · DEC-001 D-08 · D-24 · D-31)
