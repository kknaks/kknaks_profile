# day-reservation backend 기능 3 — 공지 수정 + KOS 공지 동기화 (R58 ~ R62 · 계약 v3 + 보충 1)

## 상태: done (실물 1회만 막힘 — 아래)

- 커밋 · push 없음. 스택(11040 · docker · .run)은 건드리지 않았다.
- 템플릿 · JS · CSS는 frontend 몫이라 건드리지 않았다.
- 작업 중에 보충 둘이 와서 반영했다(note-1 R62, 계약 보충 1 `notice.id` · `notice_id`).
- 코디 ask 결정도 하나 반영했다: KOS 장애 = **503** `kos_unavailable`.

## 1. EmrAdapter 공지 (업체 경계 지킴)

**`emr/base.py` 기본 메서드** — 지원하지 않는 업체는 None을 주거나 `WriteNotSupportedError`를 낸다.
- `fetch_notices(start, end)`: 동기화 · 시스템 계정
- `staff_notices(token, start, end)`
- `create_notice(token, content, released_at) → 새 외부 id`
- `change_notice(token, id, content)`
- `delete_notice(token, id)`

**KOS 구현** `emr/kos/notices.py`(`KosNotices` mixin) + `mapper_notice.py`:
- 경로(조사 표 2):
  - `meta/notice/v1/queries/get-notices {startDateTimeUtc, endDateTimeUtc, deleted:false}`
  - `meta/notice/v1/commands/create-notice {content, releaseDateTimeUtc}`
  - `meta/notice/v1/commands/change-content {id, content}`
  - `meta/notice/v1/commands/delete-notice {id}`
- 응답에서 지운 공지는 뺀다.
- 직원 토큰 호출은 기존 `KosStaffWriter`를 따른다: 브라우저 UA · Origin · `kos-client-uri=<web>/<tenant>/reservation`, 401 = `StaffTokenRejected`, 시스템 계정이나 재시도를 쓰지 않는다. 응답 JSON이 필요해서 `call()`을 새로 두고 `send()`는 그것을 부르게 했다.
- 업체 경계는 taut 규칙대로다. `notices.py`는 `client` · `staff_client`를 import하지 않고 Protocol로만 받는다(`sale_reads`와 같은 방식).
- `identifiers.ExternalNoticeId`, `emr/normalized_notice.NormalizedNoticeData`를 새로 뒀다.

## 2. `PUT /reservations/notice` (`routers/reservations.py` + `services/reservation_notice.py`)

**폼**: urlencoded `date` · `content` · `notice_id`(보충 1, 빈 값 허용) · `csrf_token`. 모르는 칸은 400이다.

**순서**:
1. 401
2. CSRF(`writable_session`)
3. 403: `reservation.notice` edit
4. 400:
   - 날짜 꼴(빈 값도 400)
   - `notice_id`가 uuid 아님
   - trim 길이 2,000 초과
5. 409 `notice_past_date`: 병원 현지 오늘 앞이면 KOS를 부르지 않는다
6. 연결 없음 → 503
7. 직원 토큰: **이 세션의** `external_session`, 만료 안 된 것. 없으면 401 `session_expired`(다른 직원 토큰은 쓰지 않는다)
8. 저장 직전 그 날짜를 **직원 토큰으로** 다시 읽는다
9. 대상 고르기(R62 ② · 보충 1): 폼 `notice_id`(DAY id) → `external_ref` KOS id가 목록에 있으면 그것, 없으면 첫 번째
10. 분기(cc 표 1 + R62 ③ ④):
    - 대상 없음 + 빈 값(공백만 포함) → 호출 없음 · 기록 없음
    - 대상 없음 + 값 → create(**trim 값** · 그 날 00:00 KST)
    - 대상 + 값 → change-content(**trim 값**)
    - 대상 + 빈 값 → delete
11. 성공 뒤 다시 읽어 `emr/sync_notices.apply_notices`로 DAY `notice` + `external_ref(entity_type='notice')`를 맞추고 commit한다.
    - **다시 읽기만 실패**(R62 ⑤): 방금 저장한 글로 응답하고 사본도 그것으로 맞춘다. create의 새 id도 모르면 사본은 다음 회차에 맞춘다.
12. event_log:
    - 성공: `notice_save {date, op, length(trim), noticeId(KOS id)}`
    - 실패: `kos_rejected {op, httpStatus, kosError}`
    - 본문 글은 남기지 않는다(시험이 확인).

**응답 (frontend용)**

200 = 조각 템플릿 이름 **`partials/reservations_notice.html`**(frontend가 만든다). 넘기는 값:
- `date`
- `weekday`
- `notice{id, content, editable:true, date}`: 다시 읽은 값

여기에 `HX-Trigger: {"day:notice-saved": {"message": "공지를 저장했어요"}}`가 붙는다. 헤더라 한글은 JSON `\u` 이스케이프다.

오류(화면 규약):

| 경우 | 응답 |
|---|---|
| 409 `notice_past_date` · `kos_rejected` · 503 `kos_unavailable` | **본문 없음** + `X-Day-Error: <code>` + `HX-Reswap: none` → 화면은 칸 안 「저장하지 못했습니다 · 다시 시도」 |
| 400 `invalid_request` | 기존 `board_error_handler`(토스트 조각 + `X-Day-Error` + `HX-Reswap: none`) |
| 403 권한 | 권한 없음 조각 |
| CSRF | 200 토스트 + `HX-Reswap: none` |
| 401 | 204 + `HX-Redirect: /login?reason=session_expired` |
| 직원 토큰 401 | 그 세션 `expires_at`을 지금으로 당기고 위 401과 같다 |

- `/api/` 경로였다면 JSON `{detail, code, field}`였을 것이다(해당 없음).
- **503 결정**: taut 규칙(코드 하나 = 업무 예외 하나) 때문에 `kos_unavailable`은 기존 `KosUnavailable`(503)을 재사용한다(코디 ask 답 A). 로그인 화면 처리에 영향이 없도록 이 라우트 안에서만 `notice_error_handler`로 돌린다.

## 3. 공지 동기화 R60 · R62 ①

- 오늘 10초 일정 회차(`services/emr_sync.run_schedules`)와 날짜 회차(`services/emr_date_sync.run_reservation_date`)가 그 창의 `fetch_notices`를 붙여 같은 transaction에서 `apply_notices`를 한다.
- `apply_notices`는 그 날짜 창을 통째로 맞춘다: 넣고 · 고치고 · 이번에 없던 연결 공지는 `deleted_at` · 같은 KOS id가 돌아오면 되살림 · 창 밖 무시.
- **공지 읽기 실패는 회차와 뗐다**(`fetch_notices_isolated`): 경고 로그 `emr notices skipped: <예외 이름>`을 남기고 이전 사본을 그대로 둔다. 회차는 `done`이다. 날짜 회차에서는 `skipped.notice.unavailable = 1`로 센다.
- 10초 회차의 KOS 호출이 공지 1회만큼 는다.

## 4. 권한 `reservation.notice` edit + migration 0020

- `policies/permissions.NOTICE_KEY`를 두고 기본 표 full · view 둘 다에 edit를 넣었다(모든 직무 · R61). 기존 시드가 새 직무에 넣는다.
- `migrations/versions/20261123_0020_notice_permission.py`(revision `0020_notice_permission`, down `0019_purchase_task_visit_index`):
  - upgrade: 살아 있는 직무에 `ON CONFLICT DO NOTHING`
  - downgrade: 그 키 행 삭제
  - `alembic heads`는 하나다.
- ⚠ 처음 이름 `0020_reservation_notice_permission`(34자)은 `alembic_version.version_num varchar(32)`를 넘어 upgrade가 깨졌다. 그래서 이름을 줄였고, **모든 revision ≤ 32자** 재발 방지 시험을 넣었다.

## 5. 보기 모델 (계약 v3 + 보충 1)

- `notice{id, content, editable, date}`:
  - `id` = 첫 공지의 DAY `notice.id`(없으면 null)
  - `content` = 그 날짜 첫 공지(`released_at` 순 · 없으면 null)
  - `editable` = date ≥ 오늘(KST) ∧ `reservation.notice` edit
- 일반 · 조각 · poll 응답 모두 같다(`board_view`).
- 예전 `notice.items`는 없어졌다(frontend 템플릿이 계약 v3로 옮김).
- 권한 확인 쿼리가 1개 붙어 `board_view` 쿼리 단언을 고쳤다: 12→13, 오늘+방문 15→16, 다른 날짜 12→13.

## 6. 시험

새 시험:
- `tests/day/board/test_reservation_notice.py`(실 PG · 앱 전체 · 가짜 KOS · 11개):
  - 분기 4 · trim · 직원 토큰 · DAY 사본 · external_ref · event_log 본문 없음 · 성공 헤더
  - 앞날 OK · 지난 날 409(KOS 안 부름)
  - KOS 400 → 409 · 500 · 연결 → 503(글 · 사본 그대로)
  - 토큰 거절 → 세션 끝 + 204 HX-Redirect
  - 권한 403 · 길이 2001 → 400 · trim 2000 OK · 날짜 · 모르는 칸 400
  - CSRF(KOS 안 부름)
  - R62 대상(폼 `notice_id` → 그 공지 · 사라졌으면 첫 번째 · uuid 아님 400) · 공백만 = 지우기 · 다시 읽기 실패 = 방금 저장한 글
- `tests/day/emr/test_kos_notices.py`(MockTransport · 4개):
  - 매핑
  - 동기화 읽기: 시스템 계정 · 하루 창 · deleted:false · 지운 것 뺌
  - 저장 경로 · 본문 · 직원 Bearer · 브라우저 헤더 · 시스템 sign-in 0
  - 401 / 4xx 상태 · 이름
- `tests/day/emr/test_notice_sync.py`(실 PG · Redis · 2개): 창 통째 맞춤 · 되살림 · 창 밖 무시. 10초 회차 반영. 공지 실패에도 `done` · 이전 사본 · 경고 로그.
- `tests/day/test_reservation_notice_view.py`(값 · 6개): 첫 공지 + id · 없음 null · editable 오늘 / 앞날 / 지난 날 / 권한.
- `tests/migrations/test_reservation_notice_permission_migration.py`: 본문 · up / down / up · 고친 행 · 지운 직무 · revision 길이.

바꾼 시험:
- `test_default_permissions` · `board/test_board_default_view`: 기본 표에 새 키
- `test_reservation_rules` · `test_reservation_queries` · `test_reservation_inhouse_queries`: 공지 모양 · 쿼리 수
- `tests/migrations/test_alembic.py`: HEAD 0020

결과:
- 관련 묶음(`./scripts/test.sh -q`): reservation 시험 전부 · `tests/day/board` · `tests/day/web` · `tests/day/emr` · `tests/migrations` · default_permissions → **897 passed**. 마지막 고침 뒤 다시 돌린 묶음은 **115 passed**다.
- architecture **317 passed**
- **`./scripts/check.sh --static` All requested checks passed**(ruff · format · mypy · taut audit / check · frontend 정적)
- 전체 `check.sh`(infra 전체)는 돌리지 않았다.

## 7. 실물 1회 — **막힘** (우회하지 않음)

- 데모 테넌트에서 오늘+1일 공지 create → change → delete를 돌리려 했다.
  - `deploy/kos-demo.env`는 스크립트가 값을 읽기만 했고 출력은 상태만 했다.
  - 공지 전용 직원 계정이 없어서 시스템 계정 이메일로 **직원 로그인 경로**(`KosStaffAuthenticator.sign_in`)를 썼다.
- 결과: **sign-in에서 `HTTP 401 SignInLimitExceeded`** — 그 계정의 동시 로그인 수가 차 있다. 로컬 스택 · worker가 쓰는 세션으로 보인다.
- 공지 명령(get / create / change / delete)은 **한 번도 나가지 않았다.** HTTP 상태: sign-in 401, 그 밖 호출 0.
- 기존 세션을 해제하는 방법(`active_sign_ins` / `revoke_sign_in`)은 스택이 쓰는 세션을 끊을 수 있어 쓰지 않았다(브리프 「우회 금지」).
- 다시 하려면: 스택을 멈춘 때나 다른 직원 계정으로 같은 스크립트를 1회 돌리면 된다. 스크립트 위치: 스크래치 `notice_live.py`. 내일 날짜에 공지가 이미 있으면 손대지 않고 멈추도록 해 두었다.

## 8. 코디 · frontend가 확인할 것

1. **frontend**:
   - 조각 템플릿 `partials/reservations_notice.html`(넘기는 값 §2)
   - 저장 form에 `notice_id` = `notice.id`
   - 성공 이벤트 `day:notice-saved`
   - 실패 판단 = status ≥ 400 + `X-Day-Error`(409 · 503은 본문 없음)
2. **계약 · SPEC 문구**: 502 → **503** `kos_unavailable`(코디 결정 A).
3. **실물**: 위 §7 — 직원 토큰 쓰기 허용 여부, 같은 날 둘째 create 거절 여부는 아직 확인 못 했다.
4. **배포**: migration 0020은 deploy의 migrate 단계에서 적용된다. api · worker를 다시 띄워야 동기화 · 저장이 반영된다(재기동은 코디).
5. 10초 회차마다 KOS `get-notices` 호출이 1회 는다.
