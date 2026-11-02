---
type: concept
id: proportional-ui-scale
title: 비율로 키우는 화면 — 고정 px 대신 배율 하나 (Proportional UI Scale)
aliases:
  - 반응형 글자 배율
  - 글자 배율
  - textScaler
  - 태블릿 배율
  - 컨테이너 쿼리 단위
  - cqh
  - px 하드코딩
up:
  - 2026-10-22-myeongdong-poc-v2
tags:
  - 반응형
  - flutter
  - css
  - 태블릿
---

# 비율로 키우는 화면 — 고정 px 대신 배율 하나

디자인 시스템의 px 값(캡션 13 등)은 **그 시스템이 상정한 화면 크기**에서만 맞다. 더 큰 기기에서 같은 px 를 쓰면 글자 · 버튼이 상대적으로 작아진다. 화면 크기에서 **배율 하나**를 계산해 글자 · 높이 · 최소 폭에 같이 곱하고, 「판의 절반」 같은 크기는 px 가 아니라 **부모 크기의 비율 단위**로 쓴다.

## 정의

1. **배율은 기기 짧은 변에서 하나** — 폰 = 1, 태블릿 = 짧은 변 / 700 을 1.15 ~ 1.3 으로 자른다. 가로 · 세로 회전에 흔들리지 않게 짧은 변을 쓴다
2. **모든 글자에 한 번에** — Flutter 는 앱 루트에서 `MediaQuery` 의 `textScaler` 를 배율로 바꿔 모든 `Text` 가 따라오게 한다. 위젯마다 크기를 고치지 않는다
3. **글자만이 아니다** — 버튼 높이 · 격자 최소 폭도 같은 배율. 글자만 키우면 버튼 안에서 넘친다
4. **웹 카드의 「화면의 절반」 은 비율 단위로** — `100cqh`(컨테이너 쿼리 높이)의 절반처럼 부모 기준으로 쓴다. 「2줄 고정 + 최소 360px」 로 박으면 화면이 바뀌면 안 맞는다

## 사용 예시

```dart
// 앱 루트
// 모양만 — 폰/태블릿 판정 기준은 코드(`tokens.dart`)를 따른다
final short = MediaQuery.sizeOf(context).shortestSide;
final scale = isTablet ? (short / 700).clamp(1.15, 1.3) : 1.0;
MediaQuery(
  data: MediaQuery.of(context).copyWith(textScaler: TextScaler.linear(scale)),
  child: child,
);
```

```css
/* 판 = container-type: size, 카드 = 판 높이의 절반 */
.card { height: calc(100cqh / 2); }
```

## 왜 중요한가

- 웹 디자인 시스템 px 를 아이패드에 그대로 옮기자 「글자가 작다 · 반응형 고려해서 비율로 했어?」 가 나왔다. 값 하나하나를 키우는 대신 배율 하나로 닫혔다
- px 를 박으면 「이 화면에서 맞음」 만 확인된다. 다음 기기 · 다음 해상도에서 같은 지적이 다시 온다

## 경계와 오해

- **사용자 글자 크기 설정과 겹친다** — `textScaler` 를 덮으면 OS 의 접근성 글자 크기를 지울 수 있다. 곱해서 합칠지는 따로 정할 몫
- **배율 ≠ 레이아웃 분기** — 폰과 태블릿에서 구조가 다르면(목록 vs 격자) 그건 브레이크포인트로 가른다. 배율은 같은 구조의 크기만 맞춘다
- **[[design-token]] 을 버리는 것이 아니다** — 토큰 값은 기준 크기에서의 값으로 두고, 기기에서 곱한다. 토큰을 기기마다 따로 만들면 시스템이 둘이 된다
- **[[viewport-aware-overlay]] 와 다르다** — 그쪽은 남은 자리를 보고 위치 · 방향을 정하는 것, 이쪽은 크기를 화면에 비례시키는 것

## 함께 보는 개념

- [[design-token]] — 곱해지는 기준 값
- [[design-system]] — px 값의 출처
- [[viewport-aware-overlay]] — 화면 크기를 보고 정하는 다른 배치 문제

## 출처

- [[2026-10-22-myeongdong-poc-v2]] §2 — 시술실 앱 태블릿 글자 배율 · 웹 카드 높이 `100cqh`(`app/lib/theme/tokens.dart` · `procedures/live/page.tsx` · `e2e-device-feedback-batch-1.md` T1 ~ T4 · E2E-12)
