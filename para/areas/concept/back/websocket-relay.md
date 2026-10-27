---
type: concept
id: websocket-relay
title: 서버 소유 스트림 중계 (WebSocket Relay)
aliases:
  - WS 중계
  - STT 릴레이
  - upstream / subscribe
  - 브라우저 직결 금지
  - 통역 중계
  - STT + TTS 중계
  - keepalive
  - TTS keepalive
up:
  - 2026-09-12-sc-meeting
  - 2026-10-14-sts-prototype
  - 2026-10-27-interpret-pwa-poc
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

통역(cc-prototype): 브라우저 WS 하나 뒤에서 서버가 Soniox **두 연결**을 잡는다 — STT(two_way 번역, 원문 · 번역 토큰이 섞여 옴) → 확정 발화(`<end>`)마다 번역문을 TTS 로 → `audio_start` · PCM · `audio_end` 를 같은 WS 로 돌려준다. 고객 국적이 통역 언어를 정하고(TW · HK 는 `zh`), 번체는 **자막만** 서버가 바꾼다(TTS 는 간체만 바르게 읽는다 — 번체를 넣으면 오류 없이 발음이 깨졌다). 닫기 · stop · 오류 · 브라우저가 그냥 닫는 어느 경우든 **외부 두 연결을 모두 닫는다.** 재생 중 마이크 되먹임은 클라이언트가 반이중으로 막는다 → [[half-duplex-echo-suppression]]

통역(통키 — 같은 구조를 새 레포로): 멈춤 · 누르고 말하기로 **말이 없는 시간이 길어지자** 외부 연결의 idle 끊김(40초)이 문제가 됐다. 두 연결 모두 keepalive 가 필요한데 **형식이 연결마다 다르다** — STT 는 `{"type":"keepalive"}`, TTS 는 `{"keep_alive": true}`. TTS 에 `{}` 를 보내자 오류가 소켓에 쌓였다가 다음 발화 TTS 에서 터져 운영 통역이 50초 만에 끊겼다 → [[deferred-stream-error]]. 멈춤(`pause`) 중에도 STT 연결은 유지하고 `finalize` 로 마지막 발화를 확정한다 → [[push-to-talk]]

## 왜 중요한가

- 외부 API 키·과금이 서버에 머문다.
- 「같은 회의를 보는 창」이 몇 개든 외부 세션은 하나 — 비용과 일관성.
- 참석자 실시간을 폴링으로 흉내 내면 갱신 종류마다 폴링이 늘고 순서가 깨진다. 한 채널이 답이다.

## 경계와 오해

- 「참석자는 소켓을 안 쓴다」와 「참석자는 마이크를 안 쓴다」는 다르다 — 후자가 맞다.
- 드레인을 안 기다리면 마지막 발화가 유실된다. 종료는 「보내기 끝」이 아니라 「받기 끝」이다.
- 컨테이너 포맷(webm/opus)은 길이 헤더가 있어 외부가 끝을 안다. raw pcm 은 없다 — 직접 테스트는 pcm 으로.
- **keepalive 는 외부의 공식 제어 메시지로** — 원형 코드에서 복사한 「빈 메시지」 는 어떤 서비스에선 무시되고 어떤 서비스에선 검증 오류다. 연결마다 문서의 형식을 확인하고, 다른 스트림의 오류가 지금 요청을 죽이지 않게 가른다
- 외부 세션이 둘이면 **수명도 둘**이다 — 한쪽만 닫히면 과금 · 동시 한도가 남는다. 세션 단위로 묶어 함께 닫고, 그걸 시험으로 확인한다. 외부 API 의 「오류 없음」 은 「맞음」 이 아니다 — 실물 왕복(TTS → STT)으로 확인한다

## 함께 보는 개념

- [[no-silent-fallback]] — 외부 단계가 끊겼을 때를 상태로 드러내기
- [[two-pass-transcription]] — 실시간 결과를 화면용으로만 쓰는 이유
- [[idempotency]]
- [[half-duplex-echo-suppression]] — 같은 기기에서 재생과 수음이 겹칠 때
- [[deferred-stream-error]] — 한 연결 위 오류가 다음 요청에서 터질 때
- [[push-to-talk]] — 송신 구간을 사람이 정하는 모드

## 출처

- 2026-09-12-sc-meeting §2 · ax-workspace `modules/meetings/stream.py`·`stream_service.py` · SCAX-SPEC-004 §5.3 · D41
- [[2026-10-14-sts-prototype]] §2 — cc-prototype 통역: STT(two_way) + TTS 두 연결 중계 · 국적 → 언어 · 번체는 자막만(`wp2-be-report.md` 실물 호출 4건)
- [[2026-10-27-interpret-pwa-poc]] §2 — 통키: TTS keepalive `{}` → `{"keep_alive": true}` · 다른 stream_id 오류는 경고만(`back/app/service/interpret/soniox.py` · `session.py` · `d35-be-report.md` 장애 절 · 코드 #6)
