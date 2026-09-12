---
type: concept
id: websocket-relay
title: 서버 소유 스트림 중계 (WebSocket Relay)
aliases:
  - WS 중계
  - STT 릴레이
  - upstream / subscribe
  - 브라우저 직결 금지
up:
  - 2026-09-12-sc-meeting
tags:
  - websocket
  - streaming
  - stt
  - realtime
---

# 서버 소유 스트림 중계

브라우저가 외부 실시간 API(STT 등)에 직접 붙지 않고, **서버가 외부 세션을 소유**하고 브라우저와는 서버 소켓으로만 말하는 구조. 외부 키가 클라이언트에 나가지 않고, 같은 자원을 보는 창 여러 개가 **한 세션의 결과를 나눠 받는다**.

## 정의

1. 클라이언트 → 서버 WS 하나. 첫 프레임에 **역할**을 선언한다 — `upstream`(오디오를 올리는 창, 자원당 하나) / `subscribe`(읽기만 하는 창, 여럿).
2. 서버는 자원당 외부 세션을 하나만 열고, 확정·잠정 결과와 서버 쪽 사건(요약 갱신·메모 줄·안건 추가·종료)을 **같은 소켓으로 broadcast** 한다. 구독 창이 따로 폴링하지 않는다.
3. 인증은 앱의 세션 쿠키 그대로(같은 오리진). 거절은 close 코드로 말한다(4401 인증 · 4404 없음 · 4409 상태/중복).
4. 외부 세션의 생명주기는 서버 몫 — 무음 keepalive, 종료 프레임 뒤 **드레인 대기**, 재연결 없음(끊김을 그대로 드러낸다).

## 사용 예시

회의 상세: 주최자 창이 `upstream` 으로 마이크 청크를 올리고, 참석자 창은 `subscribe` 로 붙어 `transcript.partial/final` · `ai.batch` · `memo.line` · `agenda.added` 를 받는다. 서버는 Soniox 세션 하나를 잡고 20초 무음이면 keepalive, `/end` 뒤 8초 드레인 뒤 닫는다.

## 왜 중요한가

- 외부 API 키·과금이 서버에 머문다.
- 「같은 회의를 보는 창」이 몇 개든 외부 세션은 하나 — 비용과 일관성.
- 참석자 실시간을 폴링으로 흉내 내면 갱신 종류마다 폴링이 늘고 순서가 깨진다. 한 채널이 답이다.

## 경계와 오해

- 「참석자는 소켓을 안 쓴다」와 「참석자는 마이크를 안 쓴다」는 다르다 — 후자가 맞다.
- 드레인을 안 기다리면 마지막 발화가 유실된다. 종료는 「보내기 끝」이 아니라 「받기 끝」이다.
- 컨테이너 포맷(webm/opus)은 길이 헤더가 있어 외부가 끝을 안다. raw pcm 은 없다 — 직접 테스트는 pcm 으로.

## 함께 보는 개념

- [[no-silent-fallback]] — 외부 단계가 끊겼을 때를 상태로 드러내기
- [[two-pass-transcription]] — 실시간 결과를 화면용으로만 쓰는 이유
- [[idempotency]]

## 출처

- 2026-09-12-sc-meeting §2 · ax-workspace `modules/meetings/stream.py`·`stream_service.py` · SCAX-SPEC-004 §5.3 · D41
