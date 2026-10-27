---
type: concept
id: push-to-talk
title: 누르고 말하기 — 소음은 필터가 아니라 입력 구간으로 막는다 (Push-to-talk)
aliases:
  - 누르고 말하기
  - PTT
  - 길게 눌러 말하기
  - 자동 듣기
  - noiseSuppression
  - 주변 노래 입력
up:
  - 2026-10-27-interpret-pwa-poc
tags:
  - 오디오
  - 실시간
  - 통역
  - 입력 모드
---

# 누르고 말하기 — 소음은 필터가 아니라 입력 구간으로 막는다

마이크를 계속 여는 **자동 듣기**는 주변의 다른 말소리(매장 노래 · 옆 사람)도 받아쓴다. 브라우저 소음 제거나 음량 문턱으로 거르지 않고, **단추를 누르고 있는 동안만 보내는** 모드를 둔다. 사람이 「지금 말한다」 를 직접 알려 주는 것이다.

## 정의

1. **누름 = 송신 재개 · 뗌 = 송신 멈춤 + 확정** — 통키는 기존 WS 메시지를 그대로 썼다: 누름 = `resume`, 뗌 = `pause` → back 이 `finalize` 로 그 발화를 확정. 서버는 바뀌지 않는다
2. **누르는 동안을 놓치지 않게** — `pointerdown` 에서 pointer capture 를 잡아 손가락이 원 밖으로 미끄러져도 뗄 때까지 유지(`pointerup` · `pointercancel` · `lostpointercapture` 로 끝). 키보드 Space · Enter 도 누름/뗌. iOS 길게 누름의 텍스트 선택 · 확대 · 메뉴는 `touch-action:none` · `user-select:none` · `-webkit-touch-callout:none` · `contextmenu` 막기로
3. **자동 듣기와 나란히 고르게** — 조용한 곳은 자동이 편하다. 모드는 기기에 기억한다
4. **멈춤 중에도 출력은 나온다** — 뗀 순간 `finalize` 로 확정된 발화의 번역 · TTS 가 그 뒤에 온다. 그래서 화면 상태 판정은 「출력 중」 이 「멈춤 · 안 누름」 보다 위다(시작 전 > 오류 > 연결 중 > 출력 중 > 누르고 말하기 안 누름 > 멈춤 > 듣는 중)
5. **다시 누르면 남은 재생을 비운다** — TTS 재생 중 누르면 재생 큐를 지우고 송신을 연다. 멈춘 뒤 도착하는 앞 발화의 TTS 조각은 다음 `audio_start` 까지 버린다(코드 리뷰 FAIL-1)

## 왜 중요한가

- `getUserMedia({ noiseSuppression: true })` 는 **일정한 소음**(팬 · 에어컨)을 지운다. 노래는 말소리라 그대로 통과해 가사가 받아써지고 번역됐다
- 음량 문턱은 「큰 음악 · 작은 목소리」 에서 양쪽 다 틀린다 — 음악은 넘고 손님 목소리는 못 넘는다. 사람이 구간을 정하면 문턱이 필요 없다

## 경계와 오해

- **[[half-duplex-echo-suppression]] 과 다른 문제** — 반이중은 **우리 스피커 소리**를 막는 것(자동, 재생 신호로 판정), 누르고 말하기는 **바깥 말소리**를 막는 것(사람이 판정). 같은 「송신 게이트」 를 쓰고 둘이 겹친다 — 누르고 있어도 TTS 가 재생 중이면 반이중이 송신을 막는다
- **대가: 말 끝 잘림 · 손이 하나 필요** — 떼는 순간이 말 끝보다 빠르면 마지막 음절이 빠진다. 실기기 감각으로 확인할 몫
- 소음 제거를 끄라는 뜻이 아니다 — 일정한 소음에는 여전히 유효하다. 말소리 소음에 안 될 뿐이다

## 함께 보는 개념

- [[half-duplex-echo-suppression]] — 같은 송신 게이트의 자동 판정 쪽
- [[websocket-relay]] — `resume` · `pause` · `finalize` 가 오가는 중계
- [[nondeterministic-stt-output]] — 들어간 소리는 받아써진다

## 출처

- [[2026-10-27-interpret-pwa-poc]] §2 — 주변 노래가 받아써져 「누르고 말하기」 모드(누름 = `resume` · 뗌 = `pause` → finalize · back 무변경) · 「출력 중」 을 「멈춤」 위로(문서 리뷰 FAIL-2) · 멈춘 뒤 TTS 조각 버림(코드 리뷰 FAIL-1)(`front/lib/ptt.ts` · `Circle.tsx` · `d36-fe-report.md` · `review-doc-report.md` · `review-code-report.md` · DEC-001 D-36)
