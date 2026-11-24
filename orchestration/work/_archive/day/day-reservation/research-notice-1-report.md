# research-notice-1 — 공지 「수정하기」 + KOS 동기화 (조사 · 읽기 전용)

- 조사일 2026-11-23 · task_f9313d7ac84b
- 원천:
  - cc-prototype `origin/main` `0553173`(`git show`)
  - DAY 워크트리 `day-reservation` `431c081b`
  - mediness `products/day/`
  - 시안 `20261113_예약현황_시연 (1).html`
  - 앞 조사 `코러스-악보/…/cc-prototype/overall-board/reservation-notice-report.md`(2026-10-27). 데모 HAR, KOS 웹 JS, 데모 실호출로 확인한 것이다. 아래에서는 「앞 조사」로 줄인다.
- `ax-clinic-project` 에는 KOS 공지 문서가 없다(grep 0). openapi 도 없다. 그래서 KOS 모양의 근거는 앞 조사, cc 코드, cc 가짜 KOS 셋이다.
- 고친 것 0, 커밋 0, KOS 호출 0. `.env` 는 읽지 않았고 고객 정보도 없다.

## 물음 1 ~ 7 요약

| # | 물음 | 답 | 그대로 / 가공 / 없음 |
|---|---|---|---|
| 1 | cc 동작 | 제자리 편집이다. [수정하기]를 누르면 다시 읽은 뒤 textarea 를 연다. textarea 밑에 글자 수를 보이고 [취소] · [저장] 이 있다. 저장 직전에 KOS 를 다시 읽어 첫 공지를 대상으로 정한다. 대상과 내용에 따라 create, change, delete 셋으로 가른다(표 1). 지난 날짜는 409, 2000자를 넘으면 400 이다. 실패하면 편집 상태와 쓴 글을 그대로 둔다. event_log 에 `notice_save` · `kos_rejected` 를 남긴다 | **가공** — 분기 · 검사 · 기록은 그대로 쓸 만하다. 화면은 React 라 Jinja2 + HTMX 로 다시 만든다 |
| 2 | KOS 명령 | `get-notices {startDateTimeUtc, endDateTimeUtc, deleted?}` → `{data:[{id, content, releaseDateTimeUtc, deleted}]}`(표 2)<br>`create-notice {content, releaseDateTimeUtc}` → `{data: Notice}`<br>`change-content {id, content}` → `{}`<br>`delete-notice {id}` → `{}` — 소프트 삭제다<br>공지는 날짜당 하나다(KOS 웹 기준). released 시각 = 그 날 KST 00:00 의 UTC 이고, 이것이 공지의 「날짜」다 | **그대로**(경로 · 본문 모양) |
| 3 | DAY 쓰기 경로 | DAY 의 KOS 쓰기는 모두 `external_outbox` 큐를 탄다. 넣은 뒤 바로 보내고, 일정 동기화에서 `expect` 로 확인한다. 이 큐는 **방문 단위**다: `visit_id` 가 NOT NULL 이고 `(visit_id, seq)` 가 유일하다. 확인도 방문 · 작업 동기화 값으로만 한다. 공지는 방문이 없고 동기화도 없어서 **이 큐에 그대로는 못 태운다**. 로그인 sign-in 처럼 **요청 안에서 직접 부르는 길**은 이미 있다 | 큐는 **없음**(공지에 맞지 않음). 직접 호출은 **가공**(KOS 어댑터에 공지 메서드를 더해야 함) |
| 4 | DAY 공지 저장 · 동기화 | `notice` 테이블은 `id · hospital_id · content · released_at` 뿐이고 KOS id 칸이 없다. **KOS → DAY 공지 동기화 코드는 하나도 없다**(`get-notices` grep 0 · 쓰는 곳 0). 그래서 지금 공지 칸은 늘 비어 있다(SPEC-006 R16). 화면은 10초 폴링마다 DB 를 읽는다 | 동기화 **없음** — 새로 만들어야 한다 |
| 5 | 시안 | 공지 칸에 「수정하기」가 없다(`renderSide` 주석 「고치기는 설정에서(C2)」). 같은 시안 안에 쓸 모양은 있다: 오더 메모 제목 옆의 파란 글자 버튼 `btn-xs-text` 「수정」과, 그 뒤의 textarea + [취소](filled-gray) · [저장](solid) + 알림 「…저장했어요」 | 공지 「수정하기」는 **없음**. 모양은 **가공**(오더 메모 패턴을 빌림) |
| 6 | 권한 | cc 는 로그인한 모든 계정이 고칠 수 있었다(역할 검사 없음 · 가짜 보드만 403). KOS 웹 공지 코드에도 역할 검사가 없다. 기획 1-3 은 「모든 직무가 어느 날짜든 쓴다」고 한다. DAY 키는 지금 `reservation` view 하나다 | **가공** — 키는 코디가 정한다(물음 7) |
| 7 | 코디가 정할 것 | 아래 §7. 편집 UI · 쓰기 방식 · 실패 표시 · 권한 · 과거 날짜 · 동기화 · KOS id 칸 | — |

---

## 1. cc-prototype 동작 (근거 file:line)

**경로와 원천**

- route `procedure/back/app/api/reservations.py:227-259` 는 `PUT /api/reservations/notice` 다. dependencies 는 `write = [Depends(require_real_board)]`(L38) 이다.
- 동작 문서는 L230-248 에 있다.
- KOS 쓰기는 동기로 한다. 응답은 KOS 200 뒤에 오고 SSE 는 없다(L44-48 `WRITE_COMMON`).

**service** — `procedure/back/app/service/reservations.py:1016-1058`

- 경로 상수는 L92-94 에 있다.
- 보드 응답의 `noticeEditable = day >= today` 는 L365-366 에서 정한다.

**schema** — `procedure/back/app/schemas/reservations.py`

- `Notice{id: ccc 행 id(int), content, releasedAt}`: L157-161
- `notices`(front 는 첫 번째만 씀) · `noticeEditable`: L231-235
- `NOTICE_MAX = 2000` · `NoticeRequest{date, noticeId, content}` · `NoticeResponse{ok, notice|null}`: L746-768

**화면** — `procedure/front/components/reservations/ResvAside.tsx:4, 28-29, 110-198` · `lib/api.ts:144-145`

### 표 1 — cc 공지 저장

| 항목 | cc 동작 | 근거 |
|---|---|---|
| 편집 UI | **제자리 편집**이고 모달이 아니다. 머리 「공지사항」 오른쪽에 버튼이 있다. 평소에는 [수정하기](outlined gray)이고, 편집 중에는 [취소](text gray) + [저장](outlined blue)이다. 본문은 `Textarea` 로 바뀌며 autoFocus 가 걸린다. 오른쪽 아래에 `n / 2,000` 이 있고, 넘으면 빨강이 되며 [저장]이 막힌다 | ResvAside L152-190 |
| 문구 | 「공지사항」 · 「수정하기」 · 「불러오는 중…」 · 「취소」 · 「저장」 · 「저장 중…」<br>placeholder 「이 날짜 공지를 적어 주세요 · 비우고 저장하면 공지가 지워져요」<br>빈 상태 「이 날짜 공지가 없어요」 · 알림 「공지를 저장했어요」 | L157-198 · L141 |
| [수정하기] 누름 | 보드를 다시 읽고 `notices[0]` 로 편집을 시작한다(KOS 웹과 같음). 응답 전에 날짜가 바뀌었으면 결과를 버린다 | L118-131 |
| 폴링과 편집 | 편집 중에는 10초 폴링이 공지 칸을 덮지 않는다. 저장 직후에는 응답 공지를 다음 보드 응답이 올 때까지 보인다 | L111-113 · L154 |
| 대상 고르기 | 저장 직전에 KOS `get-notices` 를 캐시 없이 읽는다. 화면이 보낸 `noticeId`(ccc 행 → `kos_id`)가 그 목록에 있으면 그것을, 없으면 **첫 공지**를, 그것도 없으면 대상 없음 | service L1028-1036 |
| 분기 | 대상 없음 + 빈 값 → 호출 없음 · 기록 없음 · `notice:null`<br>대상 없음 + 값 → `create-notice{content: trim 한 값, releaseDateTimeUtc: 그 날 00:00 KST}`<br>대상 있음 + 값 → `change-content{id, content: trim 안 한 원래 값}`<br>대상 있음 + 빈 값 → `delete-notice{id}`(지우기) | L1037-1045 · api L238-243 |
| 과거 날짜 | `date < 오늘(KST)` 이면 409 `notice_past_date` 「지난 날짜 공지는 고칠 수 없어요」. 화면은 `noticeEditable` 이 false 면 버튼을 숨긴다 | L1025-1026 · L366 · ResvAside L114, L167 |
| 길이 | `content.strip()` 이 2000자를 넘으면 400 `invalid_request`. 날짜가 비었거나 꼴이 틀려도 400 | L1021-1024 · schema L746 |
| 같은 글 다시 저장 | 비교하지 않고 다시 `change-content` 를 보낸다 | api L248 |
| 실패 처리 | KOS 4xx 는 409 `kos_rejected`, 네트워크 · 5xx · 401 은 502 `kos_unavailable`. 화면은 공통 `onError`(토스트)를 띄우고 **편집 상태와 쓴 글을 그대로 둔다** | service L715-726 · ResvAside L133-146 |
| 기록 | 성공하면 event_log `notice_save{date, op, noticeId(저장 뒤 ccc id), requestedNoticeId, length}` 를 남긴다. 실패하면 `kos_rejected{op, httpStatus, kosError}` 를 남긴다. 본문 글은 기록하지 않는다 | L1053-1055 · L722-723 |
| 저장 뒤 | 그 날짜 캐시를 비우고(`after_write`) KOS 를 다시 읽어 사본을 맞춘다(`ensure_day`). 응답 = 다시 읽은 공지다. 지웠거나 못 찾으면 null | L1049-1058 |
| 동기화(읽기) | 날짜 조회 회차마다 `get-notices` 를 그 날 하루 범위와 `deleted:false` 로 부른다. 결과로 사본을 통째로 바꾼다(`replace_notices`). 범위 밖 · `released_at` null 은 버린다 | `app/kos/reservation_sync.py:30, 351-357` |
| 토큰 | cc 는 시스템 계정 하나로 보냈다(`client.internal`) | service L1029 · L1048 |

## 2. KOS 공지 명령

근거:
- 앞 조사 §0 · §1.1 · §2 — 데모 HAR, 웹 JS, 2026-10-27 데모 실호출 9번이 모두 200 이었다.
- cc 가짜 KOS `procedure/back/tests/fake_kos.py:162, 288-293, 361-362, 409-425`.

### 표 2 — KOS 공지 명령

| 명령(내부 `/tenants/{t}/…`) | 요청 | 응답 | 비고 |
|---|---|---|---|
| `meta/notice/v1/queries/get-notices` | `{startDateTimeUtc, endDateTimeUtc, deleted?:bool}` | `{data:[{id:str(24), content, releaseDateTimeUtc, deleted}]}` | `deleted` 를 빼면 지운 것도 같이 온다. 시작이 끝보다 늦으면 `InvalidTimeRange` |
| `meta/notice/v1/commands/create-notice` | `{content, releaseDateTimeUtc}` | `{data: Notice}`(새 id) | 빈 내용은 `content Required`, 지난 날짜는 `releaseDateTimeUtc NotAvailable` 로 거절한다 |
| `meta/notice/v1/commands/change-content` | `{id, content}` | `{}` | 빈 내용은 거절한다(`content Required`). 2000자를 넘으면 `content TooLong`. 버전 칸이 없어 나중에 저장한 쪽이 덮는다 |
| `meta/notice/v1/commands/delete-notice` | `{id}` | `{}` | **소프트 삭제**다(`deleted:true` 로 남는다). 완전히 없애는 명령은 없다 |

- **날짜당 공지 수**:
  - KOS 웹은 날짜 키 하나에 공지 하나다(`dateToNoticeKey = yyyy-MM-dd` · 다시 읽은 결과의 첫 번째만 씀).
  - 서버가 같은 날 둘째 create 를 막는지는 **확인 안 됨**(앞 조사 Q-138).
  - 날짜를 바꾸는 명령은 없다.
- **released 시각** = `releaseDateTimeUtc`. 그 날 KST 00:00 의 UTC 이고(`…T15:00:00Z`, 전날 날짜) 공지가 「어느 날」인지를 정한다. 게시 예약 시각이 아니다.
- **반영**: 데모에서 세 쓰기 모두 바로 다음 읽기(수십 ms 뒤)에 보였다.
- **권한**: 시스템 계정으로 셋 다 200 이었다. 직원 토큰(DAY 방식)이 막히는지는 **확인 안 됨**.

## 3. DAY 쓰기 경로 — 큐인가 직접인가

**지금 길**

- 조작을 하면 `enqueue` 가 `external_outbox` 에 행을 넣고 commit 한다. 이어서 `send_now` 가 그 병원 발송 태스크를 바로 발행하고, 10초 주기 발송이 다시 보낸다.
- 그 뒤 일정 동기화가 `expect` 와 맞으면 confirmed 로 바꾼다.
- 근거:
  - `backend/day/services/outbox_kick.py:1-10`
  - `emr/outbox_persistence.py:161-188`
  - `emr/outbox_rules.py:68-` · `emr/outbox_confirmation.py:19-`
  - `tasks/emr.py:203` · `common/config.py:121`(10초)

**공지를 이 큐에 그대로 못 태우는 이유(근거)**

1. 큐가 방문 단위다.
   - `external_outbox.visit_id` 는 NOT NULL 이고 `live_unique(visit_id, seq)` 가 걸려 있다(`models/task.py:303-326`).
   - 적재 잠금도 `outbox:{visit_id}` 다(`outbox_persistence.py:184`).
   - SPEC-000 §3 `external_outbox` 표도 「방문별 보낼 순서」를 필수로 둔다(`spec-000-data-model.md:880-889`).
2. 확인할 길이 없다.
   - `expect` 는 방문 · 작업 칸만 읽는다(`emr/kos/writes.py:41-45` 형식 · `outbox_rules.expect_met`).
   - DAY 에는 공지 동기화가 없어 확인이 끝내 맞지 않는다. 결국 stale → failed 가 된다(`enqueue` 는 빈 `expect` 를 거절한다 L181).
3. 허용 목록에 없다. `write_open` 이 정해 둔 경로만 연다(`writes.py:72-101`). 공지 경로를 열려면 여기도 바꿔야 한다.
4. create 의 새 id 를 받을 수 없다. 큐 발송 `writer.send` 는 응답을 버린다(`emr/kos/__init__.py:236-241` · `staff_client.py:201-`). 그래서 `create-notice` 가 준 id 를 DAY 에 남길 수 없다.

**직접 호출의 선례**

- 로그인이 요청 안에서 KOS sign-in 을 직접 부른다(`services/auth.py:1-25`). 이 호출은 업체 어댑터를 거친다(`emr/base.py:212-` `StaffAuthenticator`).
- 업무 코드는 업체 패키지를 직접 import 하면 안 된다(`tests/architecture/test_emr_vendor_boundary.py`). 그러니 직접 호출을 하려면 `EmrAdapter` 에 공지 메서드(읽기 · 만들기 · 고치기 · 지우기)를 더해야 한다.

**SPEC · 결정 근거**

- SPEC-002 L572: 「조작 응답은 KOS 를 기다리지 않는다」. 다만 시술 현황 조작의 규칙이고 공지에는 정해진 것이 없다.
- SPEC-002 규칙 24 · L1034 · OQ-05: KOS 쓰기는 **누른 직원의 토큰**으로 보낸다. 이것이 사용자 2026-11-06 「결정 — KOS 쓰기」다.
- SPEC-006 L77 · L88 · L531: 공지 쓰기는 이번 판에 없다(R1). L90: 공지 「수정하기」는 다음 피처다(R44).
- SPEC-000 L97: 원장 전환 전에는 KOS → DAY 동기화로 채우고, 전환 뒤에 DAY → KOS(`external_outbox`)로 간다.

**판단(추천)**: 직접 호출이 맞다.

- 저장할 때 KOS 를 다시 읽어 대상을 정해야 한다.
- create 의 id 를 받아야 한다.
- 성공과 실패를 그 자리에서 보여야 한다(기획 1-3 예외 1 「저장하지 못했습니다 · 다시 시도」).
- 큐는 방문 단위라 맞지 않는다.

## 4. DAY 공지 저장 · 동기화 · 화면

| 항목 | 지금 | 근거 |
|---|---|---|
| 테이블 | `notice(id uuid, hospital_id, content, released_at, created_at, updated_at, deleted_at)` — **KOS id 칸이 없다**. 다른 KOS id 는 `external_ref(entity_type, entity_id, vendor, external_id)` 에 둔다 | `models/notification.py:93-101` · migration `20261105_0002…py:532-` · `models/customer.py:115-135` · SPEC-000 L1220-1229 |
| 동기화 | **없다.** `backend/day` 와 tests 에서 `get-notices` · `notice/v1` grep 은 0 이다. `notice` 를 쓰는 코드도 없고 테스트 fixture 만 있다 | grep 결과 · SPEC-006 L214(「동기화가 없어 비어 있다」 · R16 · R17) · SPEC-000 OQ-07-2(L2381) |
| 읽는 곳 | 그 병원 · 그 날짜(KST 하루)의 살아 있는 행 중 `released_at` 이 null 이 아닌 것을 `released_at, id` 순으로 읽어 `items[{content}]` 로 넘긴다. 템플릿은 모든 항목을 `<p>` 로 그린다 | `queries/reservations.py:167-182` · `presentation/reservations.py:54` · `templates/partials/reservations_parts.html:127-137` |
| 화면에 보이는 때 | 10초 조각 폴링 때 DB 를 읽는다(SPEC-006 R39 · R41 — 요청은 KOS 를 부르지 않는다). 고친 뒤 DAY `notice` 행을 바로 맞추면 저장 응답 조각 또는 다음 폴링(≤10초)에 보인다. 다른 데스크도 같다(기획 1-3 순서 3). KOS 웹에서 고친 것은 **공지 동기화를 만들기 전에는 DAY 에 보이지 않는다** | 위 · `common/config.py:119`(일정 동기화 10초) · `138`(다른 날짜 캐시 10초) |
| 동기화 붙일 자리(후보) | 오늘은 일정 회차 `sync_schedules`(10초)가 자리다. 다른 날짜는 `emr_date_sync.run_reservation_date`(R40)다. cc 는 날짜 조회 회차에 `get-notices` 를 같이 불렀다 | `tasks/emr.py:187` · `services/emr_date_sync.py:164-` · cc `reservation_sync.py:311` |

## 5. 시안

- 공지 칸은 `renderSide` 안의 `nt-in` 이다. 날짜 머리(아이콘 20 + `YYYY.MM.DD (요)`), 근무, 「일정」 묶음이 있다.
- **「수정하기」 · 편집 · 저장 문구는 없다.** 주석은 「고치기는 설정에서(C2)」라고 한다.
- 근거: 시안 L1804-1816(L1809 주석 · L1813 `nt-in` · `nt-d`) · CSS L487-498.
- 사용자 요청 「날짜 오른쪽 파란 수정하기」에 가장 가까운 시안 모양은 오더 메모다.
  - 제목 옆 `<button class="btn-xs-text">수정</button>`(L2146). `.btn-xs-text` 는 12px · 500 · `color: var(--primary)` 로 파란 글자다(L898).
  - 편집하면 `textarea` + `[취소] btn-filled-gray` · `[저장] btn-solid` 가 되고(L2142), 저장하면 `crmNotify('…저장했어요')` 알림을 띄운다(L1456 · L2318).
  - 시안 글자는 「수정」이고 「수정하기」가 아니다. 문구는 짓지 않으므로 사용자 요청 글자 「수정하기」 또는 시안 「수정」 중 코디가 고른다.
- 기획 1-3 은 다르게 말한다(`00-baseline/planning/데이(CC)-기획안-·-예약-현황-·-예약.md:203-234`).
  - 칸을 눌러 바로 쓰고, 멈추면 저장되며, 저장 버튼이 없다(순서 2).
  - 고친 직원 · 시각을 보인다.
  - 실패하면 「저장하지 못했습니다」(문구 안)와 「다시 시도」를 보인다(예외 1).
  - 「어느 날짜든」 쓴다(정책 1).
- 사용자 요청(버튼)은 기획(자동 저장)과 다르다. SPEC 의 「기획안과 다른 곳」 줄이 필요하다.

## 6. 권한

| 쪽 | 누가 고치나 | 근거 |
|---|---|---|
| cc | 로그인한 모든 계정(admin · doctor · nurse · coordinator · counselor). 역할 검사가 없고, 가짜 보드일 때만 403 | `api/reservations.py:41`(`WHO`) · `api/deps.py:27-31` |
| KOS 웹 | 공지 코드에 역할 검사가 없다. 서버 쪽 직원 권한은 확인 안 됨 | 앞 조사 §4 |
| 기획 | 「모든 직무가 어느 날짜든 쓴다」 | 기획 1-3 정책 1 |
| DAY 지금 | 키 `reservation` = view 한 줄이고 모든 직무에 있다(R31). `board` 처럼 view/edit 두 단계(`PermissionLevel.VIEW · EDIT`)를 쓸 수 있다 | `policies/permissions.py:13, 27-34` · `enums/staff.py:16-18` · `services/default_permissions.py:11, 21` |

DAY 키 후보:

- ⓐ `reservation` 을 edit 으로 올린다. 모든 직무에 주면 기획과 같아진다.
- ⓑ 새 키 `reservation.notice` edit 을 둔다. `board.accept` 처럼 따로 끄고 켤 수 있다.
- 어느 쪽이든 이미 있는 직무에 키를 넣는 것은 **데이터 migration** 이다(`default_permissions.py:21` 「`reservation` view = 0017」 선례).

## 7. 코디가 정할 것 (추천 포함)

| # | 정할 것 | 갈래 | 추천 · 이유 |
|---|---|---|---|
| D1 | 편집 UI | ① 제자리 편집 — 날짜 머리 오른쪽에 파란 글자 버튼, 누르면 textarea + [취소] · [저장] + 글자 수(cc · 시안 오더 메모 모양)<br>② 모달(KOS 웹)<br>③ 기획처럼 자동 저장 | **①**. 사용자 요청(날짜 오른쪽 파란 버튼)과 시안 패턴(L2142-2146)이 맞는다. 기획 자동 저장(순서 2)과 다른 점은 「기획안과 다른 곳」에 적는다. 편집 중에는 폴링이 공지 칸을 덮지 않게 한다(cc L154) |
| D2 | 쓰기 방식 | ① 요청 안 직접 호출(누른 직원 토큰 · 동기 · 응답 = KOS 결과)<br>② `external_outbox`(visit_id 없는 행을 허용하는 migration + 공지 확인 동기화 + create id 받기가 필요) | **①**. §3 의 네 이유. KOS 어댑터에 공지 메서드를 더하고(업체 경계 테스트 지킴), 토큰은 규칙 24 대로 누른 직원 것을 쓴다. 대상 고르기 · 분기는 cc 표 1 그대로 한다(저장 직전 다시 읽기 · 첫 공지 · 빈 값 = 지우기) |
| D3 | DAY 사본 맞추기 · KOS id | ① 저장 성공 뒤 같은 요청에서 그 날짜 `get-notices` 를 다시 읽어 DAY `notice` 를 맞춘다. KOS id 는 `external_ref(entity_type='notice')`<br>② `notice.external_id` 칸 migration | **①**. 외부 id 는 `external_ref` 하나라는 원칙(`models/customer.py:116` 「외부 CRM id 를 담는 유일한 테이블」)과 맞고 migration 이 필요 없다(`entity_type` 은 열린 문자열). 공지 **동기화**(KOS 웹에서 고친 것 받기)를 같이 넣을지는 따로 정한다. 추천은 오늘 일정 회차 + 다른 날짜 회차에 `get-notices` 를 붙이는 것이다(cc 방식 · R16 을 뒤집는 SPEC 결정) |
| D4 | 실패 표시 | ① 쓴 글을 그대로 두고 오류 알림을 띄운다(cc)<br>② 기획의 「저장하지 못했습니다」(문구 안) + 「다시 시도」 | **①+②**. 편집 상태와 글을 두고 칸 안에 실패 줄을 보인다. 기획 예외 1 이 근거다. 문구는 기획이 「(문구 안)」이라 사용자 확정이 필요하다. 오류 코드는 cc 의 409 `kos_rejected` · 502 `kos_unavailable` 꼴을 따른다. event_log 는 `notice_save` · `kos_rejected` 를 남기고 본문 글은 남기지 않는다 |
| D5 | 권한 | ⓐ `reservation` edit<br>ⓑ `reservation.notice` edit | **ⓑ**. 보기 권한과 따로 끌 수 있고 `board.accept` 선례가 있다. 기본값은 모든 직무 edit 이다(기획 정책 1 · cc). 데이터 migration 이 필요하다 |
| D6 | 과거 날짜 | ① 오늘 · 앞날만(cc · KOS 웹 — 지난 날 버튼 숨김 + 409)<br>② 어느 날짜든(기획 정책 1) | **①**. KOS 가 지난 날짜 create 를 거절한다(`releaseDateTimeUtc NotAvailable`). 지난 날짜 change 를 KOS 가 막는지는 확인 안 됐다. 기획과 다른 점은 「기획안과 다른 곳」에 적는다 |
| D7 | 같은 날 여러 공지 · 표시 | ① 첫 번째 하나만 보이고 고친다(cc 0.4.0 · KOS 웹)<br>② 지금 DAY 처럼 전부 보이고 첫 번째만 고친다 | **①**. 지금 SPEC-006 U-7 · DAY 템플릿은 「여러 행이면 `released_at` 순」으로 전부 보인다(L213). 이것을 첫 번째로 줄이는 것도 SPEC 개정이다 |
| D8 | 고친 직원 · 시각(기획 1-3) | 보일지 | 기획에는 있지만 KOS 응답에 고친 사람 · 시각 칸이 없다(표 2). DAY event_log 로만 알 수 있다. 추천은 **이번엔 안 보임**(cc · SPEC-006 L531 과 같음) |
| D9 | 길이 · 공백 | 2000자(trim 길이) · 만들기는 trim · 고치기는 원래 값 | **cc · KOS 웹 그대로** |

### 확인 안 된 것 (데모 실호출 허가가 있어야 함)

- 직원 토큰으로 공지 쓰기가 되는지. 앞 조사는 시스템 계정으로만 확인했다.
- 같은 날 둘째 `create-notice` 를 서버가 막는지.
- 지난 날짜 `change-content` · `delete-notice` 를 서버가 막는지.
