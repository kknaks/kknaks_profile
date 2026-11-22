# 코드 검수 — P3 호출 취소 알림(9162ee18) + 통역 시험(bd93b559)

워크트리 `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-mobile-v2` · 읽기만(수정 · 커밋 없음).
정본 = SPEC-005 2026-11-20 개정 §3 「알림 행 만들기 — 호출 취소」(271~280행) · OQ-N15~N19 · SPEC-000 enum(1063 · 1086행) · SPEC-002 규칙 38.

## 판정: **PASS(조건부) — FAIL 0 · WARN 4 · INFO 4**

스펙 문장은 모두 구현과 맞는다. 테스트 · ruff 도 통과한다. WARN 은 스펙 밖의 경쟁 · 롤백 위험과 시험 빈자리다. 머지를 막지는 않는다.

## 실행

- `scripts/test.sh -q backend/tests/day/notifications backend/tests/migrations backend/tests/day/web/test_board_feedback.py backend/tests/day/interpret` → **398 passed**(45 s · 격리 인프라)
- `uv run ruff check backend` → All checks passed · `ruff format --check backend` → 425 files already formatted
- 통키 원천 = `/Users/kknaks/git/toy_pr2/interpret-pwa` `56e43a0:back/tests/test_turn.py`(P1 검수와 같은 커밋)

---

## 1. 동작 — 스펙 맞대기

| 항목 | 판정 | 근거 |
|---|---|---|
| 완전히 닫힐 때만 한 번 | PASS | `board_calls.py:325-332` 받을 시술이 그 줄뿐일 때만 `closed` · `:350-351` 그때만 훅 · `notification_cancel.py:119` 닫히지 않은 호출은 None |
| 일부 줄 취소 = 알림 없음 · 원래 알림 그대로 | PASS | 위와 같음 · 시험 `test_notification_cancel.py` 첫 취소에서 행 0 · `read_at` 그대로 · 발행 0 |
| 재호출 사슬 | PASS(지금 코드 사실) | `cancel_call` 은 유효 호출 하나만 닫음(스펙 272행 N-3). `after_cancel` 은 id 목록을 받음. 앞 호출의 원래 알림은 그 호출이 이번에 닫히지 않으니 그대로(스펙 275행 · S-2 「앞 행 유지」와 맞음) |
| 받는 사람 = 원래 `doctor_call` 행 계정 · 비활성 · 멤버십 잃음 · 설정 끔 제외 · 원래 행 없으면 안 만듦 | PASS | `notification_cancel.py:127-153`(`_members :71` · `_switched_off :93`) |
| 제목 「호출 취소」 · 본문 「{방} · 호출 취소」 · 방 없으면 「방」 | PASS | `notification_cancel.py:55-61` · 시험 둘 다 |
| 원래 행 `read_at`(목록엔 남음) | PASS | `:170-182` 닫힌 호출의 `doctor_call` 행 중 빈 것만 · 설정 끈 · 비활성 계정 행도 닫음(스펙 275 ①) |
| `unread` 실시간 | PASS | `:209` 쓴 계정 + 닫은 계정 `announce_unread` |
| 푸시 본문 · 카테고리 없음 · 만료 0 · `push_log.kind` | PASS | `:224-271` · 시험이 본문 전체를 그대로 비교 |
| 한 계정 한 번 · 원자성 | PASS | 호출 행 `FOR UPDATE`(`:111-117`) 안에서 있는 행을 보고 없는 계정만. 취소 트랜잭션은 그대로 · 커밋 뒤 따로 |

## 2. 커밋 뒤 훅 · worker 태스크

- PASS — 훅 실패 · 시간 초과(`HOOK_TIMEOUT_SECONDS`)가 나도 취소는 200이다. 발행은 그래도 일어나고 worker 가 `ensure_cancel_rows` 로 메운다(시험 있음).
- PASS — 두 번 보내지 않는다. Redis 표지 `day:notify:call-cancel:{id}`(`:293`)가 막고, 표지를 지워도 `push_log` 가 막는다(`:241-247`). 표지를 지운 세 번째 발송까지 시험한다.
- PASS — 태스크 `day.notifications.call_cancel_push`(`tasks/notifications.py`)가 이름 상수 하나를 공유한다. 시험이 이름 글자를 고정한다.

### WARN-1. 원래 원장 호출 푸시가 취소 뒤에 나갈 수 있다 — `services/notifications.py:513-545` · `:454-511`

- `send_call_push` 와 `call_deliveries` 는 호출의 `closed_at` 도, 행의 `read_at` 도 보지 않는다. 그래서 worker 가 `call_push` 를 늦게 처리하면 이미 취소된 호출에 「원장 호출」 푸시가 나간다. 수락 권한이 있으면 `CALL`[수락] 카테고리도 붙는다.
- 이런 때 생긴다. 호출 직후에 취소하거나, 배포 · 재시작으로 worker 가 밀렸거나, `call_push` 와 `call_cancel_push` 를 동시에 처리할 때다. 행 보장 단계만 호출 행 잠금으로 줄을 서고, 보내는 단계는 잠금 밖이다.
- 같은 뿌리의 다른 경우도 있다. 원장 호출 훅이 실패한 채로 호출이 취소되면, 취소 훅은 원래 행이 0이라 취소 행을 만들지 않는다. 그 뒤 worker 의 `ensure_call_rows`(`notifications.py:325-`)가 닫힌 호출에 **안 읽은** `doctor_call` 행을 새로 쓰고 푸시까지 보낸다. 두 태스크 순서에 따라서는 취소 알림이 아예 나가지 않는다.
- 권고(코디 판단): 원장 호출 쪽 보장 · 발송에서 「취소로 닫힌 호출」을 건너뛴다. `closed_at` 만으로는 안 된다 — 재호출의 `_close_moved`(`board_calls.py:96-107`)도 같은 칸을 채우기 때문이다. 이번 범위(allowed_paths)에는 `services/notifications.py` 가 들어 있다.

### INFO-1. 표지를 먼저 잡고 보낸다 — `notification_cancel.py:293`

- worker 가 표지를 잡은 뒤 `push_log` 를 쓰기 전에 죽으면, 1일 동안 다시 보내지 않는다.
- `send_call_push` 와 같은 틀이라 새 위험은 아니다.

## 3. migration 0012

- PASS — 체인: `0012_doctor_call_cancel_kind` ← `0011_visit_reserved_index`, head 하나다. `test_alembic` HEAD 를 갱신했고, 실제 PG 에서 up → down(-1) → up 을 시험한다.
- PASS — upgrade: `ADD VALUE IF NOT EXISTS` 두 줄이다. search_path 가 `DB_SCHEMA` 라 스키마 없이 써도 된다(`env.py:117`). 같은 체인 안에서 새 값을 쓰는 뒤 리비전이 없어 트랜잭션 제약에도 걸리지 않는다.
- PASS — downgrade: 새 값을 쓰는 `push_log` 와 `notification` 행을 지우고 타입을 다시 만든다. 다만 시험은 빈 테이블에서만 돈다. 행이 있을 때 DELETE 가 도는 경로는 시험하지 않는다(INFO).
- PASS — prod 순서: `deployment.md:32-35 · 130-133` 를 보면, deploy-prod 는 DB head 가 맞지 않으면 멈춘다. 그래서 migrate-prod 가 먼저 돈다. api · worker · scheduler 는 이미지 하나로 같이 뜨니(`compose.yaml`) 태스크 이름이 api 와 따로 나가지 않는다. api 만 먼저 떠도 발행 메시지는 큐에 남는다.

### WARN-2. 롤백한 이전 이미지가 새 enum 값을 읽으면 500이 난다 — `models/_columns.py:23-30` · `models/notification.py:51 · 77`

- `pg_enum(..., validate_strings=True)` 는 ORM 이 행을 읽을 때 모르는 값에 `LookupError` 를 던진다.
- migration 은 forward-only 다. `rollback` 은 이미지만 0012 앞으로 되돌린다(`deployment.md:24 · 37-38` 「이전 이미지가 새 스키마에서 돌 수 있게」). 그 상태에서 `doctor_call_cancel` 행이 하나라도 있으면 그 원장 계정의 `GET /api/notifications`(`notifications.py:172` `select(Notification)`)가 500이 된다.
- 권고: 문서 규칙과 어긋난다는 사실을 코디가 확인한다. 롤백 절차에 「0012 앞 이미지로 되돌리면 취소 알림 행을 지운다」를 적거나, 받아들인다고 기록한다. 지금 고칠 수는 없다 — 문제는 이전 이미지 쪽 코드에 있다.

## 4. 웹 `day.js`

- PASS — `day.js:1836` `NOTIFY_KIND` 가 배열이 됐고 `:1893` `.includes` 로 거른다. 그 밖의 조건(`seen` · `readAt` · 권한 · 첫 목록 「본 것」 · 판 스트림)은 그대로다. 바뀐 줄은 `:1834-1870 · :1893` 뿐이다.
- PASS — `:1856-1870` 이 탭이 띄운 `doctor_call` OS 알림을 `callId` 로 모아 두었다가, 취소 행이 오면 `close()` 한다. 권한 검사보다 먼저 닫는다. 스펙 275 ③ 「다른 탭 · 닫힌 탭 못 닫음」과 맞는다. 호출과 취소가 한 목록에 같이 오면 원래 행은 이미 `readAt` 이라 띄우지 않으니, 문제가 없다.

### WARN-3. JS 동작 시험에 새 동작이 없고 시험 픽스처가 옛 모양이다 — `scripts/frontend/tests/controllers.test.mjs:50`

- 픽스처가 `NOTIFY_KIND: "doctor_call"`(문자열)을 넣는다. 문자열 `.includes` 는 부분 문자열 검사라 지금 시험은 우연히 통과한다. 이 픽스처로는 `doctor_call_cancel` 이 걸러진다(`"doctor_call".includes("doctor_call_cancel") === false`). 그래서 취소 행 띄우기 · 원래 알림 닫기는 JS 로 한 번도 실행되지 않는다.
- 파이썬 쪽 `test_board_feedback.py:309-310` 은 글자만 단언한다.
- 권고: 픽스처를 배열로 바꾸고, 「doctor_call 띄움 → 같은 callId 의 doctor_call_cancel → 앞 알림 close 1 · 취소 알림 띄움」 시험 1건을 더한다. 이번 allowed_paths 밖이라 워커가 손대지 않은 것은 맞다.

### INFO-2. 웹은 취소 행이 이미 읽힌 채로 오면 원래 OS 알림을 닫지 않는다 — `day.js:1893`

- 원장이 앱에서 취소 알림을 먼저 읽었으면, 웹에서는 `readAt` 때문에 `show` 에 들어가지 않는다. 그래서 `closeCall` 도 불리지 않는다.
- 스펙 문장 밖의 작은 빈틈이라 막지 않는다. `shownByCall` 은 탭이 열려 있는 동안 지워지지 않는 호출의 참조를 쥐고 있다(양은 작음).

## 5. bd93b559 — 옮긴 15건

- **PASS** — 15건을 통키 `test_turn.py` 원본과 줄 단위로 맞댔다. 시나리오 · 시각(`tick(2.9)` / `0.2`, `1.5` 밀림 0, `3*CH+0.05`) · 단언이 모두 같다. 대상: 3 · 9c · 14 · 17 · 19 · 21 · 22 · 24 · next_turn ×2 · in-flight ×2 · 새 스트림 cancel · 되울림 로그 · 덤 `Echo.on_pause` 1건.
- 다른 곳은 모양 맞춤뿐이다. `t.queue` 가 id 대신 객체라 `[u.id for u in t.queue]` 로 바꿨다(test_3). 통키의 `"".join(c for _, c in chars)` 는 `h.agent()` 로 같은 값을 본다(test_14).
- 하네스 손잡이 3개(`FakeTts.timestamps` · `term_on_cancel` · `FakeClient.block`)는 통키와 같은 이름 · 같은 의미다. 기본값을 두어 기존 시험 동작은 그대로다(`test_interpret_turn.py:242-243 · 256-257 · 265-266 · 280-288`).
- 덮는 코드 자리(`speaker.py` 잠금 · 3초 시간 초과 · `_play.cut()` · 새 스트림 cancel)는 P1 검수 W-1 표와 같다. 리포트가 말한 대로 `test_15` · `test_20` 은 해당하지 않는다.
- `deploy/config/dev.env:39-40` · `prod.env:40-41` 에 `DAY_INTERPRET_MAX_SESSIONS=3` 과 주석을 넣었다. 비밀값이 아니다.

## 6. 시험 빈자리(그 밖)

### WARN-4. 재호출 뒤 취소 시험이 없다

- 재호출로 생긴 새 호출을 취소할 때를 보는 시험이 없다. 확인할 것은 셋이다. 그 호출 행을 받은 계정만 받는지, 앞 호출의 원래 알림이 그대로인지, `closed_at` 이 이미 채워진 앞 호출에 취소 알림이 생기지 않는지.
- 사슬 문장이 「코드가 바뀔 때의 규칙」이라 지금 결함은 아니다. 다만 WARN-1 을 고치면 꼭 필요해진다.

### INFO-3. 동시 호출 취소는 이번 커밋 밖이다

- `cancel_call` 은 상태를 읽어 판정하고, 그 앞에서 잠그지 않는다. 그래서 두 줄을 동시에 취소하면 호출이 열린 채로 남을 수 있다(둘 다 「다른 줄이 남음」으로 판정). 이번 커밋이 바꾼 동작은 아니다. 남으면 알림도 나가지 않는다.
- 확인 범위 밖이라 사실만 적는다.

### INFO-4. 바뀐 파일 범위

- allowed_paths 밖에 바뀐 파일은 다음과 같다: `services/notification_cancel.py` · `tasks/notifications.py`(코디 허용), `tests/day/conftest.py` · `tests/migrations/test_alembic.py`(관련 시험).
- `notification_cancel.py` 는 302줄로 700줄 상한 안이다.

---

## 요약

| 등급 | 건 | 파일:줄 |
|---|---|---|
| FAIL | 0 | — |
| WARN-1 | 취소 뒤 원래 원장 호출 푸시 · 행이 생길 수 있음(순서 경쟁) | `services/notifications.py:454-545 · 325-` |
| WARN-2 | 롤백 이미지가 `doctor_call_cancel` 행에서 `LookupError`(목록 500) | `models/_columns.py:23-30` · `notifications.py:172` |
| WARN-3 | JS 픽스처가 문자열 `NOTIFY_KIND` · 취소 닫기 동작 시험 0 | `scripts/frontend/tests/controllers.test.mjs:50` |
| WARN-4 | 재호출 뒤 취소 시험 없음 | `tests/day/notifications/test_notification_cancel.py` |
| PASS | 스펙 동작 전부 · 훅 · 중복 0 · migration up/down · head · prod 순서 · 웹 무변경 · 옮긴 시험 15건 동일 · 테스트 398 · ruff | 위 각 절 |
