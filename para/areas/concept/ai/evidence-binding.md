---
type: concept
id: evidence-binding
title: 근거 결박 — LLM 출력 줄을 원문 구간에 묶기 (Evidence Binding)
aliases:
  - 근거 구간
  - evidence span
  - 타임칩
  - grounding to transcript
up:
  - 2026-09-12-sc-meeting
tags:
  - llm
  - grounding
  - validation
---

# 근거 결박

LLM 이 낸 정리 줄마다 **어느 원문 구간(시각 범위)에서 나왔는지**를 붙이게 하고, 서버가 그 구간이 **실재하는지** 검증해 실재하지 않으면 그 줄의 근거만 뗀다(줄은 산다). 화면은 근거를 칩으로 내고 누르면 원문의 그 자리로 간다.

## 정의

1. 출력 스키마에 `evidence: [{start_ms, end_ms}]`(최대 N)를 required 로 둔다.
2. 검증 구간은 **지금까지 적재된 원문 전체**(`0 ~ 마지막 end_ms`)다. 「이번 배치가 읽은 구간」이 아니다 — 배치가 매번 전체를 다시 쓰면 앞 회차 근거가 매번 떨어져 나간다.
3. 구간 밖 근거는 그 근거만 강등(제거), 줄 본문은 유지.
4. 화면 점프는 「구간과 **겹치는** 원문 줄」을 켠다 — 줄 시작이 구간 안일 필요는 없다.

## 사용 예시

회의 중 AI 요약 30줄 중 25줄의 시간 칩이 사라졌다. 원인은 검증 구간이 이번 배치 창이었기 때문. 회의 전체로 바꾸자 전부 살았다. 칩 03:42 가 03:29 줄을 켜는 것은 그 줄(블록)이 51초라서였다 → [[transcript-segmentation]].

## 왜 중요한가

- 근거 없는 정리는 검증할 수 없다. 근거가 있으면 사람이 한 클릭으로 원문을 확인한다.
- 검증은 「존재하지 않는 구간을 인용할 수 없다」이지 「인용 범위를 제한한다」가 아니다.

## 경계와 오해

- 구간이 실재하는지만 본다 — 그 줄과 어울리는지는 보지 않는다(그건 모델 몫).
- 근거가 여러 개면 전부 낸다. 첫 것 하나만 내면 나머지 데이터가 죽는다.

## 함께 보는 개념

- [[strict-json-schema-output]] · [[transcript-segmentation]] · [[two-pass-transcription]]

## 출처

- 2026-09-12-sc-meeting §2 · ax-workspace `modules/meetings/batch.py demote_line` · `application.py batch_input covered_ms` · D47·D49
