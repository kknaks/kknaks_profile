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
  - 2026-10-02-strong-hajin-polish
  - 2026-10-03-strong-hajin-polish2
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

## 근거로 묶을 수 있는 것 = 이 턴에 좁혀서 본 것

- 답변 참조는 그 턴의 도구로 **실제로 본 대상**만 묶는다 — 넓게 훑는 개요 도구(그래프 overview 120 노드)로 스친 것은 근거가 아니다. 검색·이웃·단건 조회처럼 좁혀 본 것만
- 참조 종류가 모자라면(예: `project` 없음) 모델이 다른 종류로 우겨 넣어 **턴 전체가 실패**한다 — 종류를 더하고, 읽기 때 권한을 다시 확인해 권한 밖 대상이 새지 않게
- 기억 키를 실행 ID 로 읽을 때 형식을 가정하지 않는다 — 회의 실행 ID(`meeting-batch:<id>`)를 UUID 로 읽다 회의 중 조회 도구가 모두 깨져 있었다

## 근거를 넓혀도 칸의 기준은 섞지 않는다

- AI 가 초안 전에 관련 회의·업무·자료를 찾아 **내용·체크리스트의 근거**로 쓰면, 답변에 출처(회의·업무 이름)를 들게 하고 그 조회는 그 턴의 답변 참조로 묶인다
- 탐색을 열면 근거 기준이 다시 섞인다 — 「ID 와 날짜는 대화·조회 근거」 한 문장이 남아 있으면, 찾은 회의 할 일의 마감 후보가 마감일로, 참석자가 참조자로 옮겨 갈 틈이 생긴다. **ID 문장과 날짜·사람 문장을 물리적으로 나눈다** — 사람은 대화가 이름을 댄 사람만, 조회는 그 이름을 ID 로 확인할 때만

## 함께 보는 개념

- [[strict-json-schema-output]] · [[transcript-segmentation]] · [[two-pass-transcription]]

## 출처

- 2026-09-12-sc-meeting §2 · ax-workspace `modules/meetings/batch.py demote_line` · `application.py batch_input covered_ms` · D47·D49
- [[2026-10-02-strong-hajin-polish]] §2 — Strong Hajin WORK-008 Phase 5(`answer_documents.py` project 종류 · `mcp.py` `_remember` 범위 · `review-p5-report.md`)
- [[2026-10-03-strong-hajin-polish2]] §2 — Strong Hajin WORK-009 E2E-1·E2E-6(SPEC-001 S-9 7·8 · `review-be-p3-report.md` W1 · 커밋 `1d4cd1f`)
