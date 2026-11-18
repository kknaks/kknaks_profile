---
type: work
id: WORK-003
title: "채팅 3열 시험 화면 — 옛 hub-evals 화면 꼴 · 새 runner 위에 새로"
status: draft
version: 0.1.0
created_at: 2026-11-16
links:
  decisions: ["_RESUME.md §2 11-16 「화면 = 옛 화면 꼴 · 새로 짓기」"]
  spec: ["SPEC-002 §2 · §5 · §7 · O-14(batch 만 → 화면 추가로 바뀜)"]
---

# WORK-003 — 시험 화면(빠른 e2e 용)

## 목적

사용자가 e2e 를 **화면으로 빠르게** 한다. 보이는 꼴 = 옛 `hub-evals` 화면(질문 → 세 열 답 나란히 · 스트리밍). **코드는 새로** — 옛 `server.py` · `web/` 은 옛 case 이벤트 체계라 가져오지 않고, 꼴(배치 · 열 카드 · 색)만 참고한다(`git -C /Users/kknaks/orca/workspaces/clinic_chat/hub-evals show HEAD:web/index.html` · `web/style.css` · `web/app.js` — 읽기만).

## 범위

**서버** — `clinic_chat/web/server.py`(FastAPI · **127.0.0.1:18220 만** · 18210 은 사용자 것 — 쓰지 마라)
- 실행: `uv run python -m clinic_chat.web` (README e2e 절에 추가)
- `POST /api/ask {question | set_id, columns[], b_on}` → `{run_id}` — **CLI `runner.run_question` 과 같은 함수**를 부른다(화면 전용 걷기 · 답 로직 0). 기록은 같은 `runs.jsonl`.
- `GET /api/runs/{run_id}/events`(SSE): 열마다 `start` · `delta`(답 글 조각 — CLI stream-json 부분 메시지) · `step`(B 걷기 단계 ①~⑤ 진행 · 선택) · `done`(종료 상태 · ms · Jev/허브/도구 호출 수 · 모델 id · effort · 오류).
- `GET /api/runs?limit=` 최근 기록 · `GET /api/runs/{run_id}` = `runs --show` 와 같은 내용(trace 포함).
- `GET /api/set` = 세트 문항 id · 범위 · 상태(draft/confirmed) **— 질문 문장은 로컬 세트 파일에서 읽어 화면에만**(커밋되는 코드 · 시험에 넣지 않음).
- 정적 파일 `clinic_chat/web/static/`(빌드 없는 HTML · CSS · JS).

**화면** — 한 페이지
- 위: 질문 입력 · 「세트 문항」 고르기(draft 는 고를 수 없음 표시) · 열 고르기(A · B · C · B 켬) · 보내기.
- 가운데: **열 카드 나란히**(A 원장 · B gold+Jev · C gold MCP · B 켬은 켰을 때만). 카드마다 답 스트리밍 · 끝나면 종료 상태 · 총 ms · 호출 수 · 모델 · effort.
- B 카드: 「trace」 펼치기 — 고른 경로(범위 · 입구) · 읽은 폭(도구 호출 · 행 수) · 깊이 판단(Noul 결정) · 검사(gate) 결과 · `entry.unused[]`.
- 아래/옆: 최근 기록 목록(누르면 그 기록 다시 보기).
- 화면 상단 고정 표시: 「프롬프트 미확정(사용자 확인 전)」(확인 전일 때) · 「추론 끔 = effort low」 · 허브 gold_hash 앞 8 자리.
- **문구는 지어 넣지 마라** — 라벨은 위에 적은 말 · SPEC-002 의 용어(종료 상태 6 이름 · 열 이름) · 옛 화면에 있던 말만. 빈 상태 · 안내 문장을 새로 쓰지 않는다.
- 채점(Opus)은 이번 화면 범위 밖(답 키 확인 전엔 어차피 안 돎) — 기록 다시 보기에서 채점 결과가 있으면 보여 주기만.

## 완료 조건

1. `uv run ruff check .` · `uv run pytest -q`(서버 시험은 모의 runner · 모의 SSE — 실호출 0) 통과.
2. 실물 1회: 서버를 18220 에 띄워 「한 질문 · B 열」 을 브라우저 없이 `curl` 로 `POST /api/ask` → SSE `delta` 가 오고 `done` 의 종료 상태가 CLI runner 와 같은 꼴 → 서버 내림. 코디가 브라우저로 다시 본다.
3. 공개 레포 — 커밋될 파일에 키 · 회사 데이터 본문 · 홈 경로 0(grep).
4. README e2e 절에 화면 실행 한 줄 · 포트.

## 하지 말 것

- 옛 `server.py` · `web/` · 옛 case 코드 import · 복사(꼴만 참고).
- 화면 전용 걷기 · 답 · 판정 로직(전부 runner 를 탐).
- 18210 · 18005 · 18105(허브 — 코디 것, 띄우거나 내리지 마라) 건드리기.
