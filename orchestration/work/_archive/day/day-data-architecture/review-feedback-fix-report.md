# 리뷰 리포트 — day-data-architecture / code · 피드백 묶음 WARN 수정 재검수 (머지 전 · 2026-11-06)

대상: 커밋 `4c2cebab` 이후 미커밋 변경(15 파일). 근거 문서는 `backend-feedback-fix-report.md` · `frontend-feedback-fix-report.md`, 앞 리포트는 `review-feedback-batch-report.md` 다.
읽기 전용으로 봤다. KOS 호출은 하지 않았다. **compose 는 건드리지 않았다.** 테스트는 `-m "not infra"` 만 돌렸다.

## 판정: PASS — **PR #228 커밋 가능**

W1 ~ W6 이 닫혔다. W2 의 확인 조건을 좁히는 일은 데모 실물 뒤로 넘겼고, 그 사이 안전한 쪽으로 넓혀 두었다. 아래 「조용히 통과」 하나와 「참고」는 커밋을 막지 않는다.

## 직접 돌린 수치

| 명령 | 결과 |
|---|---|
| `uv run pytest -q -m "not infra"` | **303 passed · 157 deselected / 4.9s**(두 수정 리포트 303 과 같음) |
| `uv run ruff check backend scripts` | All checks passed |
| grep(`templates/**` · `day.js`) | `hx-on` 0 · `style=` 0 · `innerHTML`/`eval`/`new Function` 0 |

## W 별 확인

| | 판정 | 근거 |
|---|---|---|
| **W1 바로 보내기 시간 상한** | **닫힘** | `services/outbox_kick.py` — `kiq` 를 `asyncio.timeout(OUTBOX_KICK_TIMEOUT_SECONDS)`(`config.py` 기본 **1.0초** · `0 < x ≤ 10`)로 감쌌다. `TimeoutError` → 로그(`outbox kick timed out hospital=… after 1.0s` · id 와 시간만) + `False`. 그 밖 예외도 전처럼 삼킨다. `board._finish` 는 commit · `board_changed` 뒤에 부르고 결과를 쓰지 않으므로 **조작 응답은 늘 성공이고 최대 1초만 늦는다.** 테스트(DB 없이): 멈추는 가짜 broker → `send_now(timeout=0.2)` 가 1초 안에 False · `_finish` 도 상한 안에 결과를 돌려줌(commit 1 · 발행 0) |
| W2 다시 호출 확인 조건 · 줄 의사 | **닫힘(조건 좁히기는 넘김)** | 다시 호출의 `call-tasks-doctors` 확인 = `status_in: [waiting, ready]`(`writes.py`). 수락된 READY 를 KOS 가 유지해도 stale → failed 로 뒤 쓰기를 막지 않는다. 처음 호출은 `status = waiting` 그대로. 새 키 `status_in` 은 outbox `TASK_KEYS`(`outbox.py:60`) · `_task_met`(`:545`) · 동기화 가드 칸 대응(`sync.py:1174` → `status`)에 모두 들어갔다. 줄 의사 `task_doctor`(`board_rules.py`) = 유효 호출이 있으면 그 호출의 수락 의사(없으면 null), 없을 때만 KOS 집도의 — 다시 호출 뒤 KOS 에 남은 앞 의사가 안 보인다. `start_block` 은 바뀌지 않았다. 데모 실물(수락된 시술 다시 호출)로 KOS 상태를 본 뒤 조건을 좁히는 것은 코디 몫 |
| W3 섞어 고르기 | **닫힘** | `_call_intents(again=rules.called_ids(tasks))` — `call_doctors` 를 처음 호출분(`fresh`) · 다시 호출분(`repeat`, `recall=True`)으로 나눠 계획한다. 운영 연결(trial 꺼짐)에서는 다시 호출분만 `not_supported`, 처음 호출분은 나간다. 재호출(창)은 `again = 고른 전부`(전부 다시) — 맞다 |
| W4 F11 재현 · 새로 읽기 장치 | **닫힘** | 재현 증명: 옛 day.js(`3cbb2e08`)를 Playwright 로 끼워 사용자 증상 넷(왼쪽 위 · 0개 · 판이 덮여 빈 회색 · X 안 됨)을 그대로 재현했다. 새 day.js 에서는 넷 다 맞다(스크린샷 · 스크립트 남김). 「판 사라짐」 = 640×500 창이 (12,12)에 떠 유일한 카드를 덮은 것이라는 설명이 맞다. `asset_v` = 정적 파일 4개 **내용 sha256 앞 12자리**(`web.py`) — 레플리카 · 이미지 mtime 차이로 새로 읽기를 되풀이하지 않는다. mtime 이 바뀔 때만 다시 계산한다. 테스트 `test_정적_파일_판은_내용_해시다`(mtime 만 바뀜 → 같음 · 내용 바뀜 → 다름). 사용자 새 탭 확인은 코디 몫 |
| W5 조용히 통과(앞 표) | **닫힘** | F5 화면 테스트 `order == [V2, V1, V3, V4]` + V5 는 시술 완료 탭에만 · 잠긴 카드 없음 단언 / kick 순서 = 발행 순간 commit 수 `[1]` / trial 계약 테스트 `[1:]` 제거 · 다시 호출 본문 · 확인 조건 단언 / 운영 연결 API 경로 `test_운영_연결은_다시_호출분만_닫히고_처음_호출분은_나간다`(`trial_writes` → True 로 바꾸면 깨짐) / 섞어 고르기 데모 테스트. day.js 동작 회귀는 브라우저 재현 스크립트로 대신 — 앞 리뷰에서 받아들임 |
| W6 낮음 | **닫힘** | 팝오버 스크롤 따라가기(capture scroll → 다시 배치) · Tab 으로 밖에 나가면 닫힘(day.js · 브라우저 확인) · 옛 주석(`board.py` 시작 취소 · 귀가 대기 → 「cc 근거 쓰기 — 데모 연결에만」 · `test_board_page.py` E09/E10) · 테스트 이름(`…시술_현황으로_간다…`). `cancel-flow-tasks` `reason=CANCEL` 은 데모 실물 2회 confirmed 로 KOS 수용을 확인했고 HAR 은 여전히 없다(trial 이라 받아들임) |

## 조용히 통과하는 자리

| 자리 | 왜 · 고칠 방향(낮음 · 커밋을 막지 않음) |
|---|---|
| `outbox._task_met` 의 `status_in` 판정(`outbox.py:545`) | 계획 쪽(`writes.py` · 계약 테스트 · API 테스트)은 `status_in` 이 **실리는지**만 본다. 다음 조회에서 KOS `READY`/`WAITING` 이 **맞음으로 판정되는지**(그리고 `DONE` 이면 안 맞는지)는 테스트가 없다. `:545` 줄을 지워도 모든 테스트가 통과하고, 그때 `status_in` 확인은 늘 「맞음」이 된다. `test_outbox_rules.py` 에 DB 없는 `expect_met` 한 줄(READY · WAITING → True / DONE → False)을 더하면 잠긴다 |

## 참고 (판정 밖)

- **같은 워크트리에서 두 워커가 `scripts/test.sh` 를 동시에 돌리면 `day_test` 스키마를 서로 지운다**(두 수정 리포트 모두 첫 회차 오류 → 다시 돌려 통과). 코드 결함은 아니지만, 동시 작업이 계속되면 AGENTS 「테스트」 절의 「워커마다 테스트 스키마(`DB_SCHEMA`)」를 지금 적용할지 코디가 정할 것.
- `asset_v` 는 mtime 이 바뀌면 렌더 경로에서 정적 파일 4개(약 수백 KB)를 동기로 읽는다. 배포 뒤 한 번 · 개발 중 수정 때뿐이라 받아들임.
- 남은 데모 실물(코디 · 사용자 허락 뒤):
  - 수락된 시술 다시 호출 → KOS 상태 → W2 조건 좁히기
  - 시작 취소 `PROCEDURE_WAITING` 1회
  - 사용자 새 탭 확인(F11)
