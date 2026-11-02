---
type: concept
id: two-pass-transcription
title: 2-pass 전사 — 실시간은 화면용, 최종은 비동기 재전사 (Two-pass Transcription)
aliases:
  - 재전사
  - 2-pass
  - 실시간 전사 vs 최종 전사
  - 화자 분리 재전사
up:
  - 2026-09-12-sc-meeting
tags:
  - stt
  - diarization
  - soniox
  - pipeline
---

# 2-pass 전사

실시간 STT 는 저지연을 위해 화자 분리·문장 경계가 부정확하다. 그래서 **실시간 결과는 회의 중 화면용**으로만 쓰고, 회의를 닫으면 **저장된 음원 전체를 비동기 API 로 다시 전사**(화자 분리 포함)해 원문을 통째로 갈아 끼운 뒤, 그 위에서 최종 정리를 만든다.

## 정의

1. 회의 중: 실시간 세션 결과를 원문 테이블에 적재하고 화면에 민다. 원본 오디오는 서버가 그대로 보관한다.
2. 종료: 업로드 → 전사 생성(화자 분리·언어 힌트) → 상태 폴링 → 결과 토큰. 결과를 실시간과 **같은 블록 경계 규칙**으로 잘라 원문을 전량 교체(seq 1부터).
3. 시각 보정: 파일의 0초는 회의의 0초가 아니다. `base_ms = 녹음 시작 − 회의 시작` 만큼 밀어 근거 시각을 회의 기준으로 되돌린다.
4. 그 뒤에야 합성이 원문을 읽는다 — 순서가 뒤집히면 합성이 옛 원문을 읽는다.

## 사용 예시

Charty 실제 회의 녹음 6분: 실시간 확정 81줄 → 재전사 39블록·화자 2명. 최종 회의록 줄 9개가 전부 재전사 구간을 근거로 딛는다.

## 왜 중요한가

- 화자가 어긋난 원문으로 만든 회의록은 고치는 것이 새로 만드는 것보다 비싸다.
- 실시간과 최종을 분리하면 실시간 쪽은 저지연에, 최종 쪽은 정확도에 각각 최적화할 수 있다.

## 경계와 오해

- 「실시간 전사가 정본」이라는 결정을 「재전사 폐기」로 읽으면 안 된다 — 정본은 최종 원문이고 실시간은 그것이 오기 전의 화면이다.
- 재전사가 실패했을 때 실시간 원문으로 조용히 넘어가면 안 된다 → [[no-silent-fallback]].
- 결과 GET 은 멱등이라 재시도해도 되지만 업로드·전사 생성은 다시 하지 않는다 → [[idempotency]].

## 함께 보는 개념

- [[websocket-relay]] · [[transcript-segmentation]] · [[evidence-binding]]

## 출처

- 2026-09-12-sc-meeting §2 · ax-workspace `modules/meetings/retranscribe.py`·`platform/soniox.py`·`finalize_service.py` · task-management `integrations/soniox.py`(원형) · D44
