---
type: baseline
id: BASE-002
title: "추출한 카톡 대화 AI 요약 (방·날짜 선택 + 사용자 프롬프트)"
status: accepted
product: mykakao
source:
  type: idea
  ref: "사용자 구두 요청 2026-06-15"
links:
  baselines:
    - "[[baseline-001-kakao-message-extraction]]"
  decisions:
    - "[[decision-002-ai-summary-approach]]"
  specs: []
  works: []
  releases: []
  related: []
created_at: 2026-06-15
updated_at: 2026-06-15
tags:
  - product/mykakao
  - doc/baseline
  - status/accepted
---

# 추출한 카톡 대화 AI 요약 (방·날짜 선택 + 사용자 프롬프트)

추출된 카톡 대화에서 채팅방 1개와 날짜 1일치를 골라, 사용자가 직접 쓴 프롬프트와 합쳐 LLM으로 요약해 화면에 보여준다.

> 아직 결정하지 않은 날것의 입력이다. 정리보다 보존이 우선이다.

## Raw

- 추출된 카톡 대화 중 **채팅방 1개 + 날짜 1일치**를 선택한다.
- 사용자가 **요약 프롬프트(system prompt 성격)** 를 직접 작성한다.
- 선택한 방·그 날짜의 메시지를 프롬프트와 합쳐 **codex(LLM)** 에 보낸다.
- 결과를 화면에 **렌더링**한다.
- 데모 페이지를 2개로 구성: (1) 채팅방 목록(현재 데모 유지) → (2) AI 요약 화면.

## Context

- BASE-001/DEC-001/SPEC-001/WORK-001로 **메시지 추출까지는 완료**된 상태다 ([[baseline-001-kakao-message-extraction]]). 추출된 대화방·메시지가 이미 로컬에 있다.
- mykakao 코드 레포: `/Users/kknaks/git/toy_pr2/mykakao` (FastAPI backend + 바닐라 JS frontend, 포트 8765). 현재 데모는 채팅방 목록 + 실시간 SSE 스트림까지 보여준다.
- LLM 호출 큐 라이브러리(참고): `/Users/kknaks/git/library/claude_code_pty/open_kknaks` — codex/claude 호출 큐 라이브러리, `CodexRunnerAdapter` = `codex exec --json`.
- kknaks_profile 본진은 이미 `open_kknaks` 패키지로 LLM을 호출한다 (`app/back/service/jobs/llm.py`의 `from open_kknaks import ...`). 동일 패턴을 mykakao에도 적용할 후보.

## Why It Matters

- 추출은 끝났지만 "그래서 이 대화에서 뭐가 중요했나"를 사람이 다시 읽어야 하는 비용이 남아 있다. 요약이 그 다음 가치 단계다.
- BASE-001의 최종 목표("추출 → 일정 파싱 → 캘린더")로 가는 길에서, 자유 프롬프트 기반 요약은 일정 파싱 같은 구조화 추출의 일반화된 선행 형태다. 프롬프트만 바꾸면 요약·일정 추출·할 일 추출로 확장 가능한 진입점.
- 추출된 데이터를 LLM에 흘려보내는 첫 체인이라, 이후 LLM 활용 플로우(파싱/분류)의 기반이 된다.

## Possible Direction

- LLM 호출: 직접 subprocess 대신 `open_kknaks` 라이브러리(패키지 + env 설정 + codex provider 워커). 본진 패턴 재사용.
- 컨텍스트 범위: 단일 방 × 단일 날짜로 묶어 토큰 폭증을 막는다.
- 출력: mykakao backend에 이미 있는 `/api/stream` SSE 인프라를 재사용해 스트리밍 렌더.
- provider: codex.
- 데모: 목록 / 요약 2뷰.
- 확정 결정은 [[decision-002-ai-summary-approach]]에서. 구체 구현(모델 옵션·프롬프트 템플릿·token cap·2뷰 파일 구성)은 spec/work 단계로 미룬다.
