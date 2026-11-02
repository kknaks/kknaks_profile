---
type: concept
id: deferred-stream-error
title: 늦게 터지는 스트림 오류 — 원인과 증상이 다른 메시지에 붙는다 (Deferred Stream Error)
aliases:
  - 지연 오류
  - 다음 요청에서 터지는 오류
  - keepalive 형식 오류
  - Missing stream_id
  - stray error
  - 외부 오류 로그 채널
up:
  - 2026-10-27-interpret-pwa-poc
tags:
  - websocket
  - 오류 처리
  - 로그
  - 외부 연동
---

# 늦게 터지는 스트림 오류 — 원인과 증상이 다른 메시지에 붙는다

한 연결 위로 여러 요청(스트림)이 오가는 프로토콜에서, 서버는 잘못된 메시지에 **오류 응답만 보내고 연결은 유지**한다. 클라이언트가 그 소켓을 다음 요청 때에야 읽으면, 앞 메시지가 만든 오류가 **다음 요청의 실패로** 나타난다. 증상(다음 발화 실패)과 원인(몇십 초 전 keepalive)이 떨어져 있어 로그에 채널 · 메시지 · 직전 상태가 없으면 찾을 수 없다.

## 정의

1. **조건 셋이 겹치면 생긴다** — ① 서버가 검증 오류에 연결을 안 끊는다 ② 클라이언트가 소켓을 요청 때만 읽는다 ③ 오류를 「어느 스트림 것인가」 보지 않고 올린다
2. **오류를 스트림 id 로 가른다** — 자기 스트림(또는 id 없음 = 연결 전체) 오류만 그 요청을 실패시킨다. 다른 id(빈 문자열 포함)의 오류는 경고 로그 1줄 뒤 계속한다. 서버가 연결을 유지한다는 계약과 맞추는 것이다
3. **제어 메시지는 공식 형식 그대로** — 통키는 TTS keepalive 로 `{}` 를 보냈다(원형 코드에서 복사). Soniox 는 그것을 stream_id 없는 스트림 메시지로 보고 `Missing stream_id` 를 쌓아 뒀다가, **TTS 뒤 20초 이상 쉬고 다음 발화**가 오면 그 TTS 에서 터뜨렸다. 공식 형식은 `{"keep_alive": true}`. 같은 서비스라도 STT · TTS 의 keepalive 형식이 다르다
4. **외부 오류 로그에는 처음부터 채널 · 메시지 · 상태** — `channel=tts error_type=… request_id=… message=… paused=… speaking=… stt_last=audio 0.0s ago tts_last=text …`. 오류 종류만 있으면(`invalid_request`) 어느 연결의 어떤 메시지 뒤였는지 모른다. 값 · 키 · 발화 원문은 남기지 않고 종류 · 길이 · 몇 초 전만

## 왜 중요한가

- 운영에서 「연결 50초 뒤 · 언어 무관 · 한도와 무관」 하게 끊겼다. 로그에 오류 종류만 있어 처음엔 context 한도 · 번체 경로를 의심했다. 채널 · 직전 메시지를 남기게 하고 재현 시나리오(발화 → 멈춤 35초 → 발화)를 만들자 47.4초에 같은 장애가 났다
- 스트림 id 로 가르는 방어가 있으면 **같은 종류 실수가 다시 생겨도** 세션이 죽지 않는다(옛 keepalive + 새 처리 = 경고만 남고 통과)

## 경계와 오해

- **「오류가 난 요청 = 원인」 이 아니다** — 지연 보고 프로토콜에서는 직전 메시지들의 이력이 원인 후보다. 그래서 로그에 「마지막으로 보낸 것 · 몇 초 전」 을 남긴다
- **다른 스트림 오류를 삼키는 것이 아니다** — 경고로 드러낸다 → [[no-silent-fallback]]
- [[external-api-error-classification]] 은 응답 **종류**로 처리를 가른다. 여기는 응답이 **어느 요청에 속하나**를 가른다

## 함께 보는 개념

- [[websocket-relay]] — 외부 두 연결(STT · TTS)을 서버가 들고 있는 구조
- [[websocket]] — 한 연결에 메시지가 섞여 오는 통로
- [[external-api-error-classification]] — 오류 종류에 따른 처리

## 출처

- [[2026-10-27-interpret-pwa-poc]] §2 · §3 — 운영 통역 50초 끊김: TTS keepalive `{}` → `Missing stream_id` 가 다음 발화 TTS 에서 터짐 · 공식 `{"keep_alive": true}` · 다른 stream_id 오류는 경고만 · 오류 로그에 채널 · 메시지 · 상태(`soniox.py` · `session.py` · `d35-be-report.md` 장애 절 · `live-check-d35-2026-10-27.json` 재현 · 코드 #6)
