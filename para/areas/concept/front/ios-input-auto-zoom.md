---
type: concept
id: ios-input-auto-zoom
title: iOS 입력 포커스 확대 — 16px 미만이면 화면이 커진다 (iOS Input Auto-zoom)
aliases:
  - iOS 확대
  - 입력 16px
  - 포커스 확대
  - Safari 자동 확대
  - maximum-scale
up:
  - 2026-10-27-interpret-pwa-poc
tags:
  - ios
  - safari
  - 입력
  - 접근성
---

# iOS 입력 포커스 확대 — 16px 미만이면 화면이 커진다

iOS Safari 는 글자 크기가 **16px 미만인 입력 칸**에 포커스하면 화면을 자동으로 확대한다. 확대된 채로 남아 레이아웃이 밀린다. 답은 입력 칸 글자를 16px 이상으로 두는 것이고, 확대 자체를 잠그지 않는다.

## 정의

1. **조건은 계산된 `font-size` < 16px** — `input` · `textarea` · `select`. 디자인 시스템 기본 입력이 14px 이면 모든 입력이 걸린다
2. **입력 칸만 16px** — 화면 전체 글자를 키울 필요 없다. 통키는 로그인 두 칸에만 16px 클래스를 얹었다. 검색 끈 콤보박스처럼 입력 칸이 없는 단추는 대상이 아니다
3. **덮어쓰기가 실제로 이기는지 확인** — 클래스 병합(tailwind-merge)으로 기본 14px 클래스가 빠지고 16px 만 남는지, 빌드 CSS 에 그 값이 있는지 본다

## 왜 중요한가

- 데스크톱 · 개발자 도구 에뮬레이션에서는 재현되지 않는다. 폰에서 로그인 칸을 누르는 순간 처음 보인다

## 경계와 오해

- **`maximum-scale=1` · `user-scalable=no` 로 막지 않는다** — 확대가 멈추지만 사용자가 손가락으로 키우는 것까지 막혀 저시력 사용자에게 접근성 문제가 된다
- **[[proportional-ui-scale]] 과 다르다** — 그쪽은 화면 크기에 맞춰 키우는 것, 여기는 브라우저가 멋대로 키우는 것을 피하는 최소값이다
- [[design-token]] 의 입력 크기를 바꿀지는 DS 의 몫 — 화면에서 덮을 때는 입력에만

## 함께 보는 개념

- [[rotated-region-layout]] — 같은 실기기 피드백 묶음
- [[design-token]] — 입력 기본 글자 크기가 오는 곳

## 출처

- [[2026-10-27-interpret-pwa-poc]] §2 — 로그인 입력 포커스 때 화면 확대 → 입력 16px · 확대 잠금은 접근성 때문에 안 씀(`front/app/login/page.tsx` · `fix-phone1-fe-report.md` · DEC-001 D-27)
