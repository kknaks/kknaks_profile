# [app] 상담 채팅 0.1 수정 1 보고 — 사용자 e2e(채팅 UI · 스피너 · 단계 · / 리다이렉트)

2026-11-17 · app 워커 · 워크트리 `clinic_chat/phub-gold-jev`(미커밋 0.1 위 · **커밋 안 함**).

## 0. 요약

- 2 ~ 5번 끝. **1번(얼굴 SVG 트레이싱 · 좌표)은 코디 보충대로 하지 않음**: 트레이싱을 한 번 돌려 `_face.svg` 를 덮었으나 곧바로 0.1 판 글자 그대로 되돌림(이 세션 출력에 남은 원문으로 복원 · 1,431 B) · 변환 스크립트 · 자른 패널 PNG 삭제 · `face_coords.py` 는 손대지 않음 · `/face-check` 나란히 보기 안 함. 그 뒤 그림 담당 세션이 `_face.svg` 를 바꿨다(지금 sha `e3556a08…` — 내 손 아님).
- `ruff` 통과 · `pytest` **290 passed · 1 skipped**(0.1 의 282 + 새 8) · 기존 시험 24 파일 214 passed · 1 skipped 그대로 · `git diff HEAD -- tests/` 는 0.1 그대로(`fake_cli.py` +21 뿐).
- 실물: 18223 에서 가짜 턴 1회 · **구독 CLI 실물 한 턴 1회**(「팔자주름이 고민이에요」 · 허브 18105 읽기) → 18223 내림(`lsof` 0). 다른 포트 손대지 않음.

## 1. 바뀐 파일

| 무엇 | 파일 |
|---|---|
| 새 | `clinic_chat/consult/steps.py`(단계 넷 상태) · `templates/partials/steps.html` · `tests/test_consult_chat_ui.py`(8) |
| 고침 | `consult/render.py`(마크다운 `md` 필터 · `steps()` · 단계 문구 받음) · `consult/turn.py`(단계 줄 · `delta` = 지금까지 전체) · `consult/fake_turn.py`(같은 꼴) · `consult/server.py`(`GET /` → 303 · 단계 문구 로드) · `consult/prompt.py`(선택 키 `steps`) · `templates/partials/{main,turn,answer,delta,rejected}.html` · `static/consult.css` · `static/consult.js` · `prompts/consult.json`(`steps` 키 추가 · version 그대로 `0.1.0-draft`) · `README.md`(303 한 줄) · `pyproject.toml` `markdown-it-py==4.3.0`(+ `mdurl`) · `uv.lock` |
| 고친 시험(0.1 새 시험) | `tests/test_consult_page.py::test_e0_fake_turn_stream_order_and_close` — 단계 줄이 단계마다 다시 오므로 순서 검사를 「step 뺀 순서 = list → sites · 끝 step → done → close」 로 |

## 2. 무엇을 어떻게

- **채팅 꼴**: 손님 말 = 오른쪽 말풍선 · 답 = 왼쪽 본문(말풍선 · 테두리 없이 칸 폭 전체). 입력 = 칸 아래 고정 `textarea`(글 따라 늘어남 · 최대 200px) + 아이콘 단추(글 자리 `send-label` 은 화면 밖 `span`). Enter 전송 · Shift+Enter 줄바꿈 · 한글 조합 중 Enter 무시 · 보내는 중 잠금(POST ~ 그 턴 줄기 `close` 까지 — `data-busy` · 단추 흐림) · 보낸 뒤 비움 · 포커스 유지 · 새 말/글자 오면 자동 스크롤(사용자가 위로 올려 읽는 중이면 안 끌어내림). 빈 대화 = 빈 칸(문구 0 · 채팅 머리 제목이 비면 머리 숨김).
- **스트리밍**: 0.1 도 글자는 화면에 붙었다(조각 `<span>` 덧붙임). 수정 1 은 `delta` 가 **지금까지 받은 꼬리 앞 글 전체를 서버에서 마크다운으로 그린 조각**이고 답 자리 `innerHTML` 을 바꾼다 — 흐르는 중에도 목록 · 굵게가 바로 보이고, 다시 붙기(Last-Event-ID)도 끝 꼴이 같다. 실측: 실물 턴에서 120ms 간격 폴링 48 번 중 답 길이 **23 가지**(0 → 373 자 · 약 5.9 초에 걸쳐 늘어남).
- **마크다운**: `markdown-it-py` commonmark · `html: False`(날 HTML 은 글자로) · 그림 끔 · 자동 링크 끔 · 링크는 주소 검사(javascript: 거절) · 표 켬 · 줄바꿈 = `<br>`. 근거 꼬리는 그리기 전에 떼어진 그대로(`TailFilter` · `split_tail` — 실물 페이지에 `<<<` 0).
- **스피너**: medikit 에 없어 `consult.css` 에 CSS 만(`.cs-spin` · 색은 `--ms-*` 토큰). 답 자리 첫 내용 = 스피너 → 첫 `delta` 에 사라짐.
- **단계 줄**: 진행 중 = 작은 스피너 + 문구 · 끝남 = 체크(CSS 만). 단계가 바뀔 때만 줄 전체를 `step` 이벤트로 다시 그림 · `done`/`turn_error` 직전에 모두 체크. 문구는 `prompts/consult.json` `steps`(앱 코드 한글 0 — T17 통과). 문구는 서버 시작 때 지금 파일에서 읽는다(대화 보관본과 무관 · LLM 에 안 감).
- **`GET /` → `303 /c/<새 id>`**(W-1): 새로 고침 = 같은 대화 · 서버를 다시 띄운 뒤 같은 주소 = 장부 되읽기(시험 `test_reload_and_restart_reach_same_conversation` · 실물 페이지 다시 GET 에서 답 보임).

## 3. 걷기 단계 → 화면 단계 대응

| 화면 키 | 문구(초안 · 사용자 확인) | 걷기 · 실행기의 실제 단계 | 언제 |
|---|---|---|---|
| `understand` | 질문을 이해하고 있어요 | `front`(① Jev 입구 · 대상 · 종류 판정 · 허브 resolve) | 진행 → 다음 단계가 오면 체크 |
| `search` | 관련 시술을 찾고 있어요 | `hub`(② 허브 읽기) · `depth`(③ 깊이 — Jev) · `gate`(④ 검사 · 재료) | 진행 → 목록 보낼 때 체크 |
| `list` | 시술 목록을 정리했어요 | `list` 이벤트를 보낸 순간(LLM 전) | 바로 체크로 붙음 · 목록이 없는 턴(범위 밖 · 입구 없음 · 실행 중단)은 안 나옴 |
| `answer` | 답변을 작성하고 있어요 | `llm_wait`(동시 한도 대기) · `llm`(⑤ 구독 CLI) | 진행 → `done`/`turn_error` 에서 체크 |

진행 중 문구가 「…하고 있어요」 꼴이라 끝난 뒤(체크)도 같은 글이 남는다 — 끝난 꼴 문구가 따로 필요하면 키를 나눌 자리(사용자 확인 거리).

## 4. 확인

| 무엇 | 결과 |
|---|---|
| `uv run ruff check .` | All checks passed |
| `uv run pytest -q` | 290 passed · 1 skipped |
| 기존 시험만(`test_consult_*` 뺀 24 파일) | 214 passed · 1 skipped |
| 새 시험 | `tests/test_consult_chat_ui.py`: 303 리다이렉트 · 새로고침/재시작 되읽기 · 단계 대응/상태 · 단계 문구 = JSON · `steps` 키 검사 · 마크다운 안전 · 가짜 줄기(단계 · 스피너 · 누적 마크다운 · 이스케이프) · 입력 꼴/빈 대화 |
| 공개 grep(바뀐 · 새 파일 전부) | 홈 경로 · 사용자 이름 · 회사 도메인 · 키 꼴 0 |
| 포트 | 18223 띄웠다 내림(`lsof -iTCP:18223` 0) · 18222 · 18105(GET 만) · 18220 · 18210 · 18005 · 18432 손대지 않음 |

### 스크린숏(레포 밖)

`S=/private/tmp/claude-501/-Users-kknaks-orca-workspaces-clinic-chat-phub-gold-jev/733484bb-4ad5-4f9b-ace2-971efa681b78/scratchpad`

- 실물 턴: `$S/real/real-1-empty.png`(빈 화면) · `$S/real/real-2-progress.png`(단계 「질문을 이해」 스피너 + 답 자리 스피너) · `$S/real/real-3-streaming.png`(답 흐르는 중 · 단계 셋 체크 + 「답변 작성」 스피너) · `$S/real/real-4-done.png`(끝 — 단계 넷 체크 · 마크다운 목록 · 시술 리스트)
- 가짜 턴: `$S/fake/fake-{1-empty,2-progress,3-streaming,4-done}.png`(fake 의 체크 줄 어긋남은 클래스 이름 겹침 — `.cs-check` → `.cs-tick` 로 고친 뒤 실물 턴 스크린숏에서 바로잡힌 것 확인)
- `/face-check` 나란히 스크린숏: 1번 취소로 없음.

## 5. 남은 것 · 주의

- 코디: **18222 재시작 필요**(정적 파일 · 템플릿 · 프롬프트 JSON · 새 의존 `markdown-it-py` — `uv sync` 뒤).
- 단계 문구 넷 · 끝난 꼴 문구 따로 둘지 — 사용자 확인.
- `prompts/consult.json` 바이트가 바뀌어 sha 가 새로 잡힌다(새 대화부터 새 보관본 · 열린 대화는 `prompts.changed` 표지).
- 실물 턴 장부는 `$S/real/chat/`(레포 밖).
