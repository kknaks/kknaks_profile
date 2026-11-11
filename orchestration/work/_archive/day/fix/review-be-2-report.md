# 리뷰 리포트 — fix 서버 검수 2: 수정 1 재확인 + WP-BE-3 읽음 표시 / code (2026-11-11)

대상: `CENTURION_DAY/fix` `app/` 밖 — 앞 서버 검수(`review-be-report.md`) 뒤 바뀐 것. 근거 SoT: mediness `fix-spec` SPEC-004 개정 ④ + 정정 1 · 2(`:183-188` U-2 읽음 표시 · `:372-373` 규칙 · `:438` `chat_member_read`) · `correction-read-1/2.md` · `wp-plan.md` WP-BE-3. read-only · 서버 호출 0.

## 판정: PASS

FAIL 0 · WARN 0 · 참고 3.
- 수정 1(W1 · R1 · R2 · R3 · R4 · R6)은 모두 풀렸다.
- WP-BE-3 은 「실제로 올랐을 때만」 · 받는 사람 · 커밋 뒤 발행 · `Room` 한 곳 생성 · 쿼리 수 유지가 스펙 `:372 · :373 · :438` 과 같다.

## 수정 1 재확인

| # | 결과 | 자리 · 근거 |
|---|---|---|
| W1 | 풀림 | `common/logs.py:31-53` `DropQueryString` 을 `uvicorn.access` · `uvicorn.error` **로거**에 하나씩 건다(재호출 안전) · `configure_logging` 끝(`:92`)에서 부른다 → api factory(`runtime/main.py:46`) · worker(`runtime/worker.py:15`) 진입점. uvicorn 은 `Config` 를 만들 때(factory 를 부르기 **전**) `dictConfig` 를 하고, `dictConfig` 는 로거 핸들러만 걷고 필터는 지우지 않는다 → 순서상 날아가지 않는다. 바꾸는 것은 「`/` 로 시작하고 `?` 가 든 str 인자」뿐이라 client 주소 · 상태 · 쿼리 없는 경로는 그대로다(시험 `tests/common/test_logs.py` 2건). 다른 자리 grep(`request.url` · `query` · `path_with` 를 로그에 싣는 곳): `day/web_errors.py:43` `request.url.path`(쿼리 없음 · 로그 아님) 뿐. `httpx` 는 WARNING 이상만(쿼리 든 요청 줄 안 나감) |
| R1 | 풀림 | `services/interpret/session.py:416-440` — 두 연결을 지역 변수로 떼어 `try STT 닫기 / finally try TTS 닫기 / finally 앱 소켓` · 바깥 `finally` 에서 자리 반납 한 번 · 시험 `test_tts_closes_even_if_cancelled_while_closing_stt` |
| R2 | 풀림 | `common/config.py:173` `Field(default=6, ge=1, le=50)` |
| R3 | 풀림 | `dtos/glossary.py` import = `dataclasses` 뿐 · `entry_counts(self, langs)` · `service.py` 가 `APP_LANGS` 를 넘김 |
| R4 | 풀림 | `tests/architecture/test_import_boundaries.py:205-245` — `day/routers` 의 `day.public` import + 이름 `run_interpret_session` 문자열을 모두 잡고, 검사 자체 시험(잡히는 예)도 있다 |
| R6 | 풀림 | `services/chat.py:651` `actor()` 가 길이 검사 앞 |

## WP-BE-3 읽음 표시

### 「실제로 올랐을 때만」 — `services/chat.py:949-1001`
- 경계가 먼저다: `actor()`(활성 직원 · 403) → `_room_for(lock=False)`(세션 병원 · 지금 멤버 · `left_at` 없음, 아니면 404 · `:211-224`). 나간 멤버 · 다른 병원은 UPDATE 전에 걸린다.
- `seq > 0` 일 때만 `UPDATE chat_member SET last_read_seq = least(seq, 방 last_seq), last_viewed_at = now WHERE … AND last_read_seq < least(…) RETURNING last_read_seq`.
  - PostgreSQL READ COMMITTED 에서 같은 행의 동시 UPDATE 는 앞 트랜잭션 커밋 뒤 WHERE 를 **다시 평가**한다 → 같은 seq N번은 한 번만 행을 돌려받는다. 섞인 seq 는 오를 때마다만 행을 받고 끝값은 최댓값이다(단조).
  - 안 오르면 `last_viewed_at` 만 갱신 — 앞 동작(`greatest(...)` + `last_viewed_at`)과 결과가 같다. `seq == 0` = 아무것도 안 바꿈(스펙 `:372`).
- #15 응답(`ok · lastViewedAt · lastReadSeq · unreadRooms`) · 나에게 가는 `chat_read`(seq>0) 모양은 앞과 같다.
- 시험(infra): `test_chat_concurrency.py:220` 같은 seq 6번 → 멤버마다 1번 · 섞인 seq(5,7,6,5,7) → 끝값 7 · 값 중복 없음. `test_chat_stream.py:338` 오를 때만 · 같은/낮은/0 = 0 · 나간 멤버 · 다른 병원 채널 · 방 끝으로 잘림.

### `chat_member_read` 받는 사람 — `:987-1000`
- 받는 사람 = `_current_members`(`left_at` · `deleted_at` 없음 · `:242-253`) − 읽은 사람. 채널 = 방 병원(`room.hospital_id`). `_Out` → `_finish` 가 **커밋 뒤** 발행. 읽은 본인(다른 기기 포함)은 `chat_read` 만 받는다 — 스펙 `:438` 「읽은 사람 자신은 `chat_read` 를 받음」과 같다.
- **작성자 물음 2(비활성 직원 멤버도 받는 사람에 포함) 판정 — 그대로 둔다.**
  - 스펙 `:438` 글자 = 「지금 멤버 중 읽은 사람 아닌 계정의 그 방 병원 세션 연결」 — 활성 조건이 없다. 같은 절의 `chat_message`(`:432`)도 활성 조건 없이 「볼 수 있는 지금 멤버」다(일관).
  - 정보 경계: 실리는 값은 `roomId · accountId · lastReadSeq` 뿐이다. 그 멤버는 이미 그 방 메시지를 볼 수 있는 사람이라 새로 새는 정보가 없다.
  - 스트림 주장은 사실이다: `routers/api/chat.py:537` 연결 전 `actor()`(비활성 = 403) · `:516-523` `chat_guard` 가 매번 `still_active` 로 다시 확인한다. 비활성 계정에는 새 연결이 없고, 있던 연결도 다음 확인에서 끊긴다.
  - 셈에서 비활성을 빼는 것은 앱 몫(스펙 `:183` ③ `Member.active`)이다.

### `Room.members[]` 두 칸 — `queries/chat.py:246-264 · 297-306`
- 직접 grep: `"members"` 키를 만드는 곳 = `queries/chat.py:337` 하나 · `room_views(` 호출 = `services/chat.py:262`(`_room_events` — `chat_room`) · `:456`(`_room_view` — #3 · #4 · #5 · #22) · `:470`(#2 목록) 셋뿐 → **`Room` 은 `room_views` 한 곳에서만 나온다.** 작성자 전수 표와 같다.
- #3 1:1 열기는 `_room_view` 를 지나고, 시험 `test_chat_api.py:647 test_1대1_열기_응답의_Room_members_에도_읽은_자리와_경계`가 있다(문서 리뷰 W4 풀림).
- 쿼리 수: 기존 멤버 쿼리에 `from_seq` · `last_read_seq` 칸만 더했다(새 쿼리 0) · 시험 `test_chat_queries.py:54` + 기존 「방 수와 무관」.
- 다른 멤버의 `fromSeq` 를 내보내는 것: 경계 규칙은 「그 멤버가 `fromSeq` 이전 **메시지를** 못 본다」이고 `fromSeq` 숫자 자체는 메시지 내용이 아니다. 스펙 `:373` 이 명시적으로 요구한다 — 부딪히지 않는다.

### 정정 1 전제
- 보내기 · 전달은 `_insert`(`:312-350`) 안에서 보낸 사람 `m.last_read_seq = message.seq`(방 잠금 안 · 그 방 최대 seq 라 단조 유지) · 이벤트는 `chat_message` 만 — `chat_member_read` 를 내지 않는다. 시험 `test_chat_stream.py:382 test_보내기는_chat_member_read_를_내지_않고_보낸_사람_읽음은_다음_Room_에`로 굳었다(infra).
- **문서 리뷰 W1(「`chat_room` 의 `Room` 이 커밋 전에 만들어져 옛 `lastReadSeq` 를 실을 수 있다」) — 서버에서 사실이다.** `_room_events`(`:256-266`)는 각 `work()` 안 · 커밋 **전**에 `room_views` 로 `Room` 을 만든다. READ COMMITTED 라 그 문장 뒤 다른 멤버의 읽음이 커밋되면, 늦게 발행되는 `chat_room` 은 그보다 옛 `lastReadSeq` 를 싣는다(그 반대 순서로 `chat_member_read` 가 먼저 도착할 수 있음). 앱은 늘 max 로 합치므로(스펙 `:186` ②) 서버는 그대로 둔다 — 확인만.

### 작성자 「다른 곳」 1 — 시스템 줄은 누구의 읽은 자리도 올리지 않음
- `_join`(`:281-306`)은 들어올 때 `last_read_seq = from_seq = 그 순간 방 last_seq`, 그 뒤 시스템 줄이 seq 를 하나 올린다. 그래서 만든 사람 · 초대된 사람 모두 `lastReadSeq = fromSeq = 시스템 줄 seq − 1` 로 시작한다.
- 숫자가 영원히 남는 경우를 따졌다 — **없다.**
  - 시스템 줄에는 숫자가 없다(스펙 `:183` · 앱 셈 제외).
  - 방을 만든 직후 첫 메시지(seq = 시스템 줄 + 1): 보낸 사람 = 그 seq(서버 · 앱 정정 1 ①) · 다른 멤버 = 그 방을 보면 #15 의 `least(seq, 방 last_seq)` 가 시스템 줄을 넘어 올려 준다 → 줄어 사라진다.
  - 초대된 멤버: `fromSeq` = 초대 직전 `last_seq` → 그 이전 메시지에서는 세지 않는다(`fromSeq < seq` 조건) · 이후 메시지는 읽으면 줄어든다.
  - 마지막으로 그린 메시지가 시스템 줄이어도 그 seq 로 읽음 요청이 가니 앞 메시지까지 덮는다.
  - 안 읽은 멤버가 계속 안 열면 숫자가 남는다 — 그것은 카톡식 의도대로다(나감 · 비활성이면 앱이 뺀다).

## 범위 · migration

- migration 0(`backend/migrations` 무변경 · 칸 `from_seq` · `last_read_seq` 는 기존).
- 앞 검수 뒤 바뀐 파일 = `common/logs.py` · `config.py` · `interpret/session.py` · `dtos/glossary.py` · `interpret/service.py` · `services/chat.py` · `chat_events.py` · `queries/chat.py` · `routers/api/chat.py`(주석) + 시험.
- `deploy/` · `scripts/` · `pyproject.toml` diff 는 앞 검수 때와 같은 줄 수(+2 · +3 · +3 · +5 · +6 · +2)라 이번에 바뀐 것은 없다. `app/` · `.github/` 무변경.

## 조용히 통과하는 자리

1. **WP-BE-3 시험 전부가 `infra`** — `test_chat_stream` · `test_chat_concurrency` · `test_chat_api` · `test_chat_queries` 는 `pytestmark = infra` 라 내 실행(`-m "not infra"`)에서 deselect 됐다. 실행 확인은 작성자 격리 스택뿐이다.
2. **수치 한 건 차이**: 내 실행 = 848 passed + **300** deselected = 1148, 작성자 = 848 + 299 · 전체 1147. 작성자 보고에 「W4 시험(#3)을 전체 실행 **뒤**에 추가하고 `test_chat_api.py` 만 다시 돌림(20 passed)」이 있어 그 1건으로 설명된다 — 못 믿을 근거는 아니다. 다만 **지금 트리 전체를 격리 스택에서 한 번 돈 기록은 없다** → 머지 전 `scripts/test.sh -q` 한 번.
3. `test_chat_concurrency.py:278` `to_nurse[-1] == 7` 은 발행 **순서**를 단정한다. 발행은 각 요청의 커밋 뒤라, 6 으로 올린 요청의 발행이 7 의 발행보다 늦게 끝날 수 있다(드물게 흔들릴 수 있음). 앱은 max 로 합치므로 동작 문제는 아니다. 단정을 `max(to_nurse) == 7` 로 바꾸면 안전하다(참고).

## 참고

- C1. 위 「조용히 통과」 3 — 순서 단정 → `max`.
- C2. 문서 리뷰 W1 은 서버에서 사실이고, 앱 max 합치기가 막는다. 서버를 바꿀 필요 없음.
- C3. 받는 사람에 비활성 멤버 포함 — 스펙 글자 그대로라 유지(물음 2 판정).

## 돌린 명령 · 수치(각 1회)

| 명령 | 결과 |
|---|---|
| `cd backend && uv run pytest -q -m "not infra"` | **848 passed, 300 deselected**, 1 warning(기존) · exit 0 |
| `cd backend && uv run ruff check . ../scripts` | All checks passed! |
| infra | 돌리지 않음(지시) |
