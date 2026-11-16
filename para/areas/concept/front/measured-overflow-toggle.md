---
type: concept
id: measured-overflow-toggle
title: 화면 높이로 판정하는 펼치기 (Measured Overflow Toggle)
aliases:
  - 펼치기 판정
  - 더보기 버튼 판정
  - 접힌 글 펼치기
  - line clamp 더보기
up:
  - 2026-11-12-fix-web
tags:
  - 프론트
  - CSS
  - UI
---

# 화면 높이로 판정하는 펼치기 (Measured Overflow Toggle)

**「펼치기」 버튼을 글의 줄바꿈 수가 아니라 화면에 실제로 넘쳤는지(`scrollHeight > clientHeight`)로 켜는 것.** 긴 한 줄은 줄바꿈 없이도 폭에서 접혀 여러 줄이 된다.

## 정의

1. 서버(템플릿)는 버튼을 **늘 두되 숨긴다** — 넘침은 글꼴 · 카드 폭 · 글자 크기에 달려 서버가 알 수 없다.
2. 클라이언트가 그린 뒤 내용 칸의 `scrollHeight > clientHeight` 면 버튼을 보인다.
3. **다시 그릴 때도 잰다** — 조각 교체(HTMX swap) 뒤 · 펼친 상태 복원 뒤.

## 사용 예시

DAY 판 카드 오더 메모는 `text.split('\n')|length > 5` 일 때만 「펼치기」를 그렸다. 글자를 10 → 12px 로 키우자 줄바꿈 없는 긴 상담 메모가 접힌 높이(`max-height` · `overflow: hidden`)에서 잘린 채 버튼이 없었다(리뷰가 잡음). 템플릿은 버튼을 `hidden` 으로 두고 day.js 가 재서 켜도록 바꿨다.

## 왜 중요한가

줄 수 판정은 글자 크기 · 폭이 바뀌는 순간 어긋나고, 어긋나면 **글이 조용히 잘린다** — 사용자는 뒤에 내용이 더 있는 줄 모른다.

## 경계와 오해

- **CSS `line-clamp` 만으로는 버튼을 켤 수 없다** — 자르기는 하지만 「잘렸는지」는 알려 주지 않는다. 판정은 여전히 측정이 필요하다.
- **숨김 상태에선 잴 수 없다** — `display: none` 안의 요소는 높이가 0 이다. 보이는 시점(탭 전환 · 펼침)에 다시 잰다.

## 함께 보는 개념

- [[overflow]] — 이름은 같지만 숫자 범위 넘침(자료형). 여기는 화면 상자 넘침

## 출처

- [[2026-11-12-fix-web]] §2 — DAY 오더 메모 「펼치기」를 줄바꿈 수에서 화면 높이 판정으로(review-code-3 W2)
