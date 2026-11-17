# fix-feedback backend 2루프 결과 — 호출 취소(F-5 · 규칙 38) · 「간호관리」 칸(E3 `systemDoctor`)

## 상태: done

워크트리 `/Users/kknaks/orca/workspaces/CENTURION_DAY/fix-feedback` · 커밋 · push 안 함 · migration 없음 · KOS 쓰기 · 알림 · 푸시 없음(사용자 결정 그대로).

## 변경 파일

| 파일 | 무엇 |
|---|---|
| `backend/day/dtos/board.py` | `BStaff.is_system: bool = False`(끝에 기본값 칸 — 기존 위치 인자 호출 그대로) |
| `backend/day/queries/board.py` | 판 직원 읽을 때 `is_system=s.is_system_account` 채움 |
| `backend/day/services/board_rules.py` | `system_doctor(t)` · `cancel_call_block(v, t)` · `task_view` 에 `"systemDoctor"` 칸 |
| `backend/day/services/board.py` | `cancel_call(...)` (accept 아래 · `_prestart_doctor_chart` 앞) |
| `backend/tests/day/board/test_board_feedback_rules.py` | DB 없음 +3 (호출 취소 줄 판정 · 같은 호출 다른 줄 수락됨 · systemDoctor 참/거짓 + 원장 변경 판정) |
| `backend/tests/day/board/test_board_feedback_service.py` | infra +6 (아래) |

라우터 · 템플릿 · static · styles · 앱 API 안 건드림.

## 계약

- **`board.cancel_call(session, current, task_id: uuid.UUID, now: datetime | None = None) -> ActionResult`** — `undo_home` 과 같은 모양. `result.body = {"ok": True}` · `visit_id` · `version`(commit 뒤) · `queued = 0`.
  - 검사 순서(:756): 404 `NotFound`(다른 병원 · 없는 줄 · 「방 배정」 · KOS 취소 작업 · 판 카드 아닌 방문 — 기존 `_visit_of` + `_task`) → 409 `visit_home` → `call_already_accepted` → `task_not_called` → 취소. (401 · 403 은 라우트 몫.)
  - `call_already_accepted` = 그 줄 상태가 수락 **또는** 그 줄은 호출인데 그 유효 호출이 이미 수락됨(같은 호출 다른 줄 수락 — 동시). `task_not_called` = 준비중 · 진행중 · 완료.
  - 저장(OQ-67 ⓒ 제안 그대로): 그 줄이 든 **열린 호출 전부**의 `doctor_call_task.deleted_at = now` → 그 줄은 유효 호출 없음 = 준비중(앞 열린 호출로 되살아나지 않음). 유효 호출의 받을 시술(`receivable`)이 그 줄뿐이었으면 그 호출 `closed_at = now`(`closed_at IS NULL` 조건부).
  - `event_log` **`call.cancel`**(스펙 제안 이름) 1행 · payload `{taskId, callId, removedFromCallIds, closedCallIds}` · actor = 누른 직원. 한 transaction(`_finish` 1 commit · 방문 advisory lock — accept 와 같은 잠금이라 동시 수락과 직렬화).
  - outbox 0 · 알림 행 0 · 푸시 없음.
- **스냅샷 `tasks[].systemDoctor: bool`** — 웹 · 앱 공통 `task_view`(앱 `GET /api/board` 에도 더한 칸뿐 · 앱은 무시). 참 = `task_doctor(t) is None` + KOS 집도의(`t.doctor_ids`) 중 `BStaff.is_system`. 이때 `doctor` 는 `null`.
- **원장 변경(U-3 :228)** — 서버는 이미 됨: 「바로 시작」 줄은 진행중이라 `doctor_change_block` 통과 · `before=None` ≠ 새 원장 → `_set_task_doctor` 가 시스템 계정 집도의를 지우고 새 원장 · KOS `change-tasks-doctors`. infra 테스트로 확인(변경 뒤 `systemDoctor=false` · `doctor` = 새 원장 · DAY 집도의 = 새 원장 1명). **코드 변경 불필요.** (완료 줄은 원장 줄과 같게 원장 변경 불가 — 규칙 27 그대로.)
- 거절 코드 글자 — `MESSAGES` 에 안 넣음(`task_not_called` 는 비워 둠 · `call_already_accepted` 는 기존 글자).

## 검증

```
uv run pytest -q backend/tests/day/board/test_board_feedback_rules.py backend/tests/day/board/test_board_rules.py
  → 63 passed
DAY_ENV_FILE=/Users/kknaks/git/CENTURION_DAY/deploy/local.env scripts/test.sh -q \
  backend/tests/day/board/test_board_feedback_service.py backend/tests/day/board/test_board_feedback_rules.py
  → 26 passed (infra 19 — 1루프 13 개 포함, 이번에 처음 실제로 돌아 전부 초록 · review-code-1 W1 해소)
DAY_ENV_FILE=… scripts/test.sh -q backend/tests/day/board backend/tests/architecture   (회귀 1회)
  → 207 passed, 3 failed — 3 개 모두 fe 진행 중 파일(아래 「무관」)
uv run ruff check backend --exclude backend/day/routers/board.py → All checks passed · ruff format --check 통과
```

infra 테스트(새 6): 호출 취소 성공(한 줄 취소 → 준비중 · 호출 열림 / 마지막 줄 → 호출 닫힘 · 다시 호출 가능 · KOS outbox 0 · 알림 행 증가 0 · event payload) · 앞 열린 호출로 안 되살아남(열린 호출 둘 다에서 뺌 · 새 호출 닫힘 · 앞 호출 열림) · `call_already_accepted` · `task_not_called`(준비중 · 진행중) · `visit_home` · 404 · `systemDoctor` 참 → 원장 변경 → 거짓.

**무관한 실패 3개(fe 작업 중)**: `test_screen_copy`(새 문구 근거 표) · `test_web_rules` 2개(빌드 CSS sha — `scripts/build-css.sh` 필요). `ruff` 의 `routers/board.py` E501 3건(:145 · :689 · :690)도 fe 파일.

## fe 몫

- fe 가 이미 `routers/board.py:690` 에 `"cancel-call": lambda session, current, task_id, now: board.cancel_call(session, current, task_id, now)` 로 붙이는 중 — 시그니처와 맞음(그냥 `board.cancel_call` 을 표에 바로 넣어도 됨). 응답 = 기존 줄 조작 `_after`(스펙 :595 · 판 다시 받기 아님).
- 「간호관리」 글자: `task.systemDoctor` 가 참일 때 {원장} 자리 · 진행중 줄은 원장 줄과 같은 `doctor_pop`(원장 변경) 열기 — 지금 `board_parts.html` 은 `doctor` 없으면 안 열림.
- 위 E501 3건 · CSS 빌드 · 근거 표.

## E2E 에서 만날 자리

1. 「호출 취소」 뒤 KOS 데스크엔 그 작업이 「호출(WAITING)」로 남음(감수 · 다음 동기화가 DAY 를 되돌리지 않는지 실물 확인 — DAY 쪽은 `doctor_call_task` 만 바꾸므로 동기화가 건드리지 않아야 함).
2. 원장 앱 · 알림함의 그 호출 알림 행은 그대로 남음(호출 취소 알림 없음 — 다음 스펙). 닫힌 호출이면 「수락 대기」에서 빠지지만 알림 행은 남아 원장이 눌러 들어오면 이미 준비중인 줄을 봄.
3. 같은 호출의 다른 줄이 남아 있으면 그 호출은 「수락 대기」에 남고, 원장이 수락하면 남은 줄만 받음.
4. 「간호관리」 줄에서 원장을 고르면 KOS `change-tasks-doctors [그 원장]` 1건 — 시스템 계정 집도의를 덮어씀.

## 이슈 · 코디 확인

- `call_already_accepted` 판정을 「그 줄 수락」 + 「같은 호출 다른 줄 수락(호출 줄)」 둘로 넓게 잡음(스펙 :756 「그 호출이 수락됨」 문장 그대로 읽음).
- `event_log` 이름 `call.cancel`(스펙 제안 그대로).
