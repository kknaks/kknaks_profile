# 리뷰 리포트 — day-data-architecture / code · Delivery #230 시술 현황 ① 백엔드 (2026-11-06)

대상: 워크트리 `CENTURION_DAY/day-data-architecture` — #224 ~ #229 커밋(`9c7376ca`) 위 미커밋 #230.
`templates/` · `static/` 변경은 #231 몫이라 판정에서 뺐다(자리 템플릿 4개 포함).
읽기 전용으로 봤다. KOS 호출은 하지 않았다. **compose 는 건드리지 않았다.** 테스트는 `-m "not infra"` 만 돌렸고, 전체 385 는 코디 확인 수치를 따른다.
기준: Issue #230(v5) · DAY-SPEC-002 · SPEC-000 · SPEC-001 · 원천 `procedure-board-decisions.md` · 발주서 · 구현 리포트 · #226 검수 W7.
범위가 커서 「SPEC 대조」와 「outbox · KOS 쓰기 · 동기화 · SSE」 두 갈래를 나눠 읽었다. 아래 지적은 모두 파일:줄을 다시 열어 확인했다.

## 판정: FAIL

규칙 · API · KOS 쓰기 범위 · outbox W7 · migration · 병원 경계는 대체로 단단하다.
- Functional Rule 1 ~ 25 와 API 짝 11 + 11 이 모두 있다.
- 열린 KOS 쓰기는 (경로 + 값) 6가지뿐이다.

FAIL 은 두 가지다.
- **앱 SSE 가 로그아웃 · 만료 뒤에도 환자 이름이 든 판 전체를 계속 보낸다**(F1).
- **N+1 query-count 테스트가 없다**(F2). 코드 문서는 있다고 적고 있다.

## 직접 돌린 수치

| 명령 | 결과 |
|---|---|
| `uv run pytest -q -m "not infra"` | **255 passed · 130 deselected / 3.1s**(구현 리포트 255 와 같음) |
| `uv run ruff check backend scripts` | All checks passed |
| 이번 테스트(전체 / DB 없이) | `test_board_rules` 20/20 · `test_kos_board_contract` 15/15 · `test_board_api` 19/0 · `test_board_sse` 4/0 |
| 비밀값 대조(`deploy/local.env` 의 키 · 테넌트 id · 시스템 이메일 · 비밀번호 ↔ 추적 · 미추적 파일 + 구현 리포트) | 0 |
| 실데이터(`명동` · `세라미크` · 전화번호 꼴) | 코드 0(금지 문구 · 부정 단언만) |
| `DAY_ADMIN_EMAILS` | `local.env.example` · compose 에 **이름만**. `deploy/local.env` 에 줄 없음(워커가 값을 넣지 않았다) |
| `emr/kos/client.py`(시스템 계정 경로) | diff 0 |

## FAIL

### F1. 앱 SSE 스트림이 세션을 처음 한 번만 보고, 로그아웃 · 만료 뒤에도 판 스냅샷을 계속 보낸다 — `routers/api/board.py:97-113` · `routers/board.py:191-221`
- 근거: `stream` 은 연결 때 `current_session` · `_allowed` 를 한 번 본다. 그다음 `snapshot_for` 는 쥐고 있던 `current` 로 **10초마다 · 신호마다** `board.board(own, current, …)` 를 새로 읽어 보낸다. 세션이 살아 있는지 다시 보지 않고, 스트림 수명 상한도 없다.
- 그래서 로그아웃(`revoked_at`) · 만료(`expires_at` — KOS 401 로 당겨진 경우 포함) · 권한 회수 뒤에도, 열린 연결은 **고객 이름 · 시술 · 메모가 든 스냅샷 JSON** 을 무기한 받는다. SPEC-001 규칙 「로그아웃 뒤 그 세션은 401 unauthorized」와 어긋나고, L3 인증 경계다.
- 웹 스트림은 본문이 빈 `board` 신호뿐이라 다음 `GET /board` 가 세션을 다시 본다. 다만 `kos_failed` 토스트 HTML(고객 이름 · 방)은 끊긴 세션에도 계속 간다.
- 고칠 방향:
  - 스트림 루프에서 tick 마다(10초) 그 `login_session` 이 아직 사는지(`check_alive` — 해시로 한 줄 조회) 본다. 죽었으면 `event: session_expired`(또는 그냥 닫기)로 끝낸다.
  - 권한도 같은 때 다시 본다.
  - 스트림 최대 수명(예: `expires_at` 까지)을 둔다.
  - 테스트(infra) 1개: 스트림을 연 뒤 로그아웃 → 다음 tick 에 스트림이 끝난다.

### F2. N+1 query-count 테스트가 없다 — `queries/board.py:4`
- 근거: 독스트링은 「쿼리 수는 방문 · 작업 수와 상관없이 같다 — `tests/day/board/test_board_queries.py` 가 센다」인데, **그 파일이 없다**(`tests/day/board/` = conftest · api · rules · sse). AGENTS.md 「백엔드 안전 기준」은 「목록 조회의 관계는 eager load · N+1 위험 경로는 query-count 테스트로 막는다」다. 시술 현황은 10초마다 · SSE 신호마다 병원 판 전체를 읽는 가장 뜨거운 경로다.
- 고칠 방향: infra 1개 — 방문 1개와 10개(작업 · 직원 · 호출 · 상담 포함)로 `load_world` 를 돌려 SQLAlchemy `before_cursor_execute` 수를 세고 같은지 본다. 또는 독스트링을 사실대로 고친다. 앞의 것을 권한다.

## WARN

### W1. 전체 권한 계정이 「권한 검사 한 곳」을 벗어난 자리에서 빠진다 — `routers/login.py:169` · `session.py:112`
- `require_permission`(`sessions.py:146-157`)은 맞다 — 한 곳 · 권한 행으로 못 통과할 때만 보고 · 로그에는 `account_id` 만(이메일 없음).
- 그런데 다른 자리 둘이 권한을 따로 본다.
  - `/` 는 `if not view.permissions: raise Forbidden`(`login.py:169`)이라 **권한 행이 0인 전체 권한 계정이 `/` 에서 권한 없음 화면**을 본다. dev 가 아닌 서버에서는 로그인 직후가 바로 거기다.
  - `WebView.permissions` · `/api/auth/me` 의 권한 목록은 `permissions_of` 그대로라 전체 권한이 드러나지 않는다. **#231 이 이 목록으로 버튼을 숨기면 관리자에게도 숨겨진다.**
- 고칠 방향: `/` 의 검사를 `require_permission(…, "board", VIEW)` 같은 한 길로 바꾼다. `WebView`/`me` 에 `is_admin`(또는 「모든 권한」 표시)을 실어 화면이 그것으로 판단하게 한다. 조각 계약(A9)에도 한 줄 적는다.

### W2. 「확인 필요」 칸 정렬이 SPEC 과 다르다 — `services/board_rules.py:520`
- SPEC · docstring 은 「넘긴 시간 긴 순」인데, 코드는 `need.since` 오름차순(먼저 시작한 순)이다. 기준이 다른 둘(마취 20분 · 호출 5분)이 섞이면 순서가 갈린다. 예: 마취 21분(1분 넘김)이 호출 9분(4분 넘김)보다 앞에 온다.
- 고칠 방향: `need` 에 `over`(넘긴 초)를 싣고 그 내림차순으로. DB 없는 테스트 1개.

### W3. 스냅샷 `sync.lastOkAt` 이 늘 null · `lastError` 고정 None — `services/board_rules.py:530` · `dtos/board.py:108`
- `sync_last_ok_at` 을 채우는 곳이 없다(grep 0). SPEC 「스냅샷 모양」의 `sync{lastOkAt, lastError}` 는 화면이 「KOS 동기화가 멈췄다」를 알릴 근거다. #231 이 이 값을 그리면 늘 「모름」이다.
- 고칠 방향: 일정 회차가 `done` 일 때 시각을, `error` 일 때 오류 이름을 Redis(병원별)에 두고 `load_world` 가 읽는다. 1차에 안 할 거면 조각 계약 표에 「항상 null — 자리」라고 적는다.

### W4. KOS 쓰기 의도가 기록 없이 빠지는 길이 셋 — `services/board.py:267-268 · 381-384 · 545-551`
- 방문 외부 id 가 없을 때(`_intent_base` None), 호출 1단계에서 방 외부 id 가 없을 때, 수락에서 의사 외부 id 가 없을 때는 op 도 `payload.kos` 기록도 없다. AGENTS.md 「조용히 건너뛰지 않는다」 · A5 「드러난다」.
- 지금 데이터(전부 KOS 동기화로 들어옴)에서는 거의 못 닿는다. dev 의 비데모 병원(`_vendor` None)도 이 길이라 의도된 생략이 섞여 있다.
- 고칠 방향: 각 자리에서 `payload.kos = [{write, status: "skipped", reason: "no_external_id"}]` 와 로그 한 줄.

### W5. outbox — 남은 작은 틈 둘 (`emr/outbox.py`)
- (a) **토큰이 없는 pending 은 만료가 없다**(`:455-458`). 그 방문의 뒤 쓰기와 동기화 가드(`expect` 칸 보호)도 같이 묶인다. 예: 수락한 의사의 `external_session` 이 끝나 다시 로그인하지 않는 경우. 그 칸은 DAY 값으로 무기한 고정되고 KOS 값을 따르지 않는다. → 토큰 대기 상한(예: 30분) 뒤 `failed`(+ `kos_failed`).
- (b) **보내는 중 재전송**: `sent` 로 잡은 뒤 KOS 반영이 20초보다 늦으면 조회 2번 「안 맞음」으로 `pending`(attempts+1)이 된다. 그러면 다음 회차가 같은 요청을 다시 보낸다(`:254`). 요청 시간 상한이 15초라 드물다. A8(첫 실제 쓰기) 때 `call-tasks-doctors` 재전송이 KOS 에서 어떻게 되는지 같이 볼 것.
- 사소: `_block_later`(`:291-299`)가 `deleted_at` 을 거르지 않는다.

### W6. 테스트가 계약 문장을 다 잠그지 못한다(「조용히 통과」 — 아래 표)
A2 「409 순서」 · A5 「닫힌 쓰기는 드러난다」 · A3 「웹과 앱 둘 다」를 테스트가 일부만 본다. 각 줄은 표에.

### W7. 일정 동기화는 조작의 advisory lock 을 잡지 않는다 — `emr/sync.py`(가드 읽기) · `services/board.py`(조작 lock)
- 조작이 commit 하기 전에 동기화가 outbox 를 읽으면, 반영 대기 op 이 아직 안 보여 그 칸(예: `flow_step`)을 KOS 옛 값으로 덮는다. 열린 쓰기는 op 이 남아 있어 다음 회차부터 가드가 지키고, KOS 반영 뒤 맞춰진다. 그래서 몇 초 깜빡임으로 끝난다.
- 「방문당 진행 중 마취 하나」 · 「(호출, 시술)당 수락 하나」는 lock 으로만 지키고 DB 제약이 없다(AGENTS 「사전 조회만으로 보호하지 않는다」 — lock 이 있으니 기준은 충족). 낮음.

## 조용히 통과하는 자리

| 자리 | 왜 |
|---|---|
| `test_board_rules.py:158` 「시작 검사 순서」 | `task_not_waiting`(진행 중) 과 `call_not_accepted` 가 겹치는 경우(진행 중인데 수락 안 된 호출에 묶인 시술)가 없다. `board_rules.py:200-204` 두 검사 순서를 바꿔도 통과한다 → 순서를 잠그려면 둘이 겹치는 시술 1개를 더한다 |
| `test_board_rules.py:208-210` `nothing_to_accept` | `task(v, 9, started_at=NOW)` 를 월드에 넣지 않는다(`*[t for t in []]` 는 빈 값). 그래서 「이미 시작함」이 아니라 「목록에 없음」으로 통과한다 → task 9 를 `rules_of` 작업 목록에 넣는다 |
| `test_board_api.py` 닫힌 쓰기(`:309` 부근) | `payload.kos = not_supported` 를 **시작 취소에서만** 본다. 완료 취소 · 귀가 대기는 「op 0개」만 보므로 의도를 아예 안 만들어도(조용한 생략) 통과한다 → 셋 다 `payload.kos` 단언 |
| `test_board_api.py:400` 웹 CSRF | 토스트 문구 · `hx-reswap` 만 본다. 상태(403 / HTMX 200)와 `csrf_failed` 를 보지 않는다 |
| A3 웹 오류 | 웹 라우트는 409 한 종류 · CSRF 만. 400 · 404 의 `X-Day-Error` 조각 계약은 앱 쪽 테스트에만 있다 |
| 매트릭스 줄에 테스트 없음 | 401 `session_expired`(보드) · 404(판 카드가 아닌 방문 · KOS 취소 작업) · `visit_home` 이 빠진 동작(종료 · 되돌리기 · 마취 종료 · 재호출 · 수락) · 수락의 `call_closed` · 재호출의 `doctor_not_listed` · 카드 0장 200 |
| 웹 폼 모르는 칸 | JSON 은 `extra=forbid` 로 400. 웹 폼(`routers/board.py:133-137`)은 모르는 칸을 그냥 둔다. 매트릭스 「모르는 칸 400」은 앱에만 걸린다 |
| `DAY_ADMIN_EMAILS` | 로그 줄과 `board.accept` 통과를 테스트하지 않는다(`test_board_api.py:100` 은 view/edit 만) |

## 맞게 된 것 (확인)

- **KOS 쓰기 (경로 + 값) 6가지**:
  - 계획 `emr/kos/writes.py:74-128` 과 보내기 직전 `write_open`(`:54-64`)이 같은 표로 두 번 막는다.
  - backend 전체의 `commands/` 경로는 이 6개 + 토큰 발급(sign-in · exchange-token) + 쓰이지 않는 상수 하나뿐이다.
  - 닫힌 쓰기 넷(시작 취소 `PROCEDURE_WAITING` · 완료 취소 `complete=false` · 귀가 대기 · WAITING 재호출 3단계)은 `WriteNotSupportedError` → `event_log.payload.kos = not_supported` 로 남고 op 은 없다.
  - 그 뒤 폴링이 KOS 값으로 되돌리는 것은 계약이 감수한 결과다(A5 · Target Delta 「감수」). 지적하지 않는다.
- **직원 토큰 쓰기**:
  - `staff_client.KosStaffWriter.send`(`:162-179`) — 그 직원 본인 토큰 · 브라우저 헤더 · 401 은 재-sign-in · 재시도 없이 `StaffTokenRejected`.
  - outbox 는 그 세션의 `expires_at` 을 당기고 op 을 pending 으로 둔다(`outbox.py:360-370 · 469-476`).
  - 토큰이 없으면 `no_token` · pending · attempts 그대로.
- **outbox W7**:
  - (a) pending → sent 조건부 UPDATE 로 먼저 잡고 commit 한 뒤에 보낸다(`:460-464`). 잡은 뒤 죽으면 확인 2번이나 오래된 sent 가 거둔다.
  - (b) 오래된 sent(180초) → failed. 토큰 대기 pending 은 대상이 아니다(`:386`).
  - (c) 빈 `expect` 는 `ValueError`(`:140-141`).
  - 전이는 순수 함수(`decide_after_send` · `decide_stale` · `decide_on_poll`) → `_apply`.
- **migration 0004**: `doctor_call.closed_at` NULL 허용 + `uq_external_outbox_visit_id_seq`(부분 · `deleted_at IS NULL`) = 모델 `live_unique`. downgrade 순서가 맞다. 적재는 max(seq)에 지운 행을 포함해 seq 가 계속 증가하므로 충돌 없다.
- **동기화가 반영 대기 칸을 덮지 않음**: 방문 단계(`sync.py:892-895` · 이력 줄도 생략) · 작업 상태 · 완료 시각 · 방 · 담당자 · 의사(`:1340-1352`). failed 뒤에는 가드에서 빠져 KOS 값을 따른다(`:1243`). mapper 가 뺀 작업은 `held_back` 으로 사라짐에서 빠진다(`:1393-1407` — #226 W1 과 같은 방식).
- **병원 경계**:
  - task · call id 는 `_visit_of`(`board.py:139-147`)가 방문의 병원을 확인하고, 아니면 404 다.
  - 다른 병원 의사는 `doctor_not_listed`. 순서 저장은 병원 판 안에서만.
  - 다른 병원 404 테스트가 있다.
  - 새 작업 · 상담 upsert 는 병원 범위 `Refs` 다.
- **동시성**:
  - 조작마다 방문 advisory lock(순서는 병원 lock) · 한 transaction · event_log 1 · op 0 ~ 3 · commit 뒤 신호.
  - transaction 안에서 KOS 를 부르지 않는다.
- **[시작] 409 순서 코드**: `visit_home → task_not_waiting → call_not_accepted → no_doctor`(`board_rules.py:193-205`) = SPEC.
- **SSE**:
  - 병원별 채널 하나. 연결 전에 요청 DB 세션을 닫는다(`api/board.py:103`).
  - 연결 끊김 확인 · 15초 ping · `retry: 3000` · `id:` 없음.
  - `kos_failed` 는 조건부 이동이 성공할 때 한 번 · commit 뒤 publish.
- **누출**:
  - 로그 · 오류는 상태 · 오류 이름뿐(`_error_of` · `type(exc).__name__`). `outbox.failed` payload 는 id · 경로 · 오류 이름이다.
  - 토큰은 `Authorization` 헤더와 `EncryptedText` 에만 있다.
  - 전체 권한 로그는 `account_id` 만 남긴다.
- **테스트 규칙**: 규칙 20 · 쓰기 표 15 는 DB 없이 돈다. infra 는 API 끝에서 끝까지 · SSE · 제약 · 동기화 반영이다(2026-11-06 규칙에 맞음).

## A9 조각 계약 — #231 이 기댈 만한가

**대체로 그렇다.** 라우트 · 조각 이름 · 넘기는 값 · 오류(`X-Day-Error` + `HX-Reswap: none` + oob 토스트) · SSE(`board` 빈 신호 / `kos_failed` HTML) · 앱 SSE 모양이 코드(`routers/board.py` 첫 docstring)와 같다. #231 이 알아야 할 빈칸 셋:
1. `snapshot.sync.lastOkAt` 은 지금 늘 null(W3).
2. 화면의 「권한으로 버튼 숨김」은 `WebView.permissions` 에 전체 권한이 안 실려 관리자에게 틀린다(W1).
3. htmx 가 4xx 를 끼우게 하는 `day.js`(`htmx:beforeSwap`) 처리는 #231 몫이다 — 계약 표에 적혀 있다.

## 「계약에 없어 구현이 정한 것」 1 ~ 10 판정

| # | 판정 |
|---|---|
| 1 오류 본문 `{detail, code, field}`(SPEC 은 `{error:{code,message}}`) | **받아들임 · SPEC 개정 필요** — 한 서버 두 모양보다 낫다. SPEC-002 §3 을 #227 모양으로 고칠 것(코디) |
| 2 완료된 시술 [종료] = `task_not_doing` | 받아들임 · SPEC 매트릭스에 한 줄 더할 것 |
| 3 확인 필요 둘이면 넘긴 비율 큰 쪽 하나 | 받아들임 — 단, 정렬은 W2 |
| 4 sending 상태 없이 pending → sent 잡기 | 받아들임(W7(a) 닫힘) |
| 5 오래된 sent 180초 | 받아들임 |
| 6 `expect` 모양 · Guard | 받아들임 — 업체를 모르는 우리 형식 |
| 7 `doctorAssignedDateTimeUtc` 받음 | 받아들임 · SPEC 표 고칠 것(응답에 있음) |
| 8 KOS 401 세션 끝내기를 outbox 안에서 | 받아들임 — 같은 transaction 이유가 맞다. `sessions.end_session_on_kos_401` 과 중복 구현이라 한쪽으로 모으면 좋다(낮음) |
| 9 일정 지문으로 SSE 신호 | 받아들임 |
| 10 `DAY_ADMIN_EMAILS` 한 곳 · 로그 | `require_permission` 은 맞음 — W1(다른 두 자리) |

`PROCEDURE_WAITING` HAR 근거(`방배정.har`)는 사용자 결정 대상으로 잘 드러냈다. 닫아 둔 것은 W6 결정대로라 맞다.

## 직원이 실물에서 만날 자리

- (W1) dev 가 아닌 서버에서 전체 권한 계정이 로그인하면 `/` 가 권한 없음 화면이다. `/board` 는 열린다.
- (W5 a) 수락한 원장이 DAY 에 다시 로그인하지 않으면 그 시술의 「반영 대기」가 풀리지 않고, KOS 쪽 값이 판에 안 보인다.
- (계약 감수) 시작 취소 · 완료 취소 · 귀가 대기는 DAY 에서 바뀌었다가 다음 10초 폴링이 KOS 값으로 되돌린다. 귀가 대기 카드가 판에 다시 나타난다. 화면이 「KOS 에 반영되지 않는 동작」이라고 미리 알려 줄 문구가 필요하다(#231).
- (W2) 「확인 필요」 맨 위가 가장 급한 카드가 아닐 수 있다.
