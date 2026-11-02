# 리뷰 리포트 — meeting-room-workflow / WP-125 backend (2026-08-31)

## 판정: WARN

계약(SPEC-151 §7.9 조합표 4행·source 축·파생 매핑·동기화 분기)이 **코드로 정확히 서 있고**,
allowed_paths·신설 금지 목록·모달 발 무변경·계층 규율 **위반 0**. 재발주가 필요한 FAIL 사유는 없다.
다만 **문면 위반 소지 1건 + 계약 미구현 1건 + 원장 무결성 2건 + P0 후속 미결 1건**을 코디네이터
판단으로 남긴다.

---

## 검수 범위

- diff: 워킹트리(uncommitted) vs `HEAD`(9585efbc) — **수정 7 + untracked 3 = 10 파일**, `+433/−24`
  (untracked 3파일 별도: `meeting_chain.py` 419줄 · `0135_*.py` 89줄 · 테스트 896줄)
- 전량 `back/` 안. `front/`·`mcp/`·`docker-compose*` 무변경 — **allowed_paths 이탈 0**
- 실행한 검사 (**read-only만** — 브리프 지시대로 테스트 미실행, 리포 파일 수정·생성 0):
  - `git status --porcelain` · 파일별 `git diff` 전문 정독 + 신규 3파일 전문 정독
  - `uv run ruff check <변경 10파일>` → `UP042` 2건(`models/meeting_v2.py:38,45`)만.
    **둘 다 선재**(이번 diff 는 같은 파일 71~76행에 주석만 추가) ⇒ **신규 lint error 0**
  - 계약 대조 grep: `MEETING_MODAL_SOURCE`(6곳) · `origin_action_id`(생성처 2곳) ·
    `Subject.workflow_run_id`(서비스 계층 선례) · `ActionRepository(` · alembic head 유일성
  - 소비처 실체 확인: `run_idempotent_steps`/`prior_execution_result`/`fail_execution`/`audit`
    시그니처 ↔ 테스트 대역 `_Ctx` 대조

---

## 위반 (FAIL 사유)

**없음.**

---

## 경미 (WARN) — 6건

### W-1. 예약 실행 결과에 **회의 id 를 담은 result 키**가 신설됐다 ⚠ 계약 문면 위반 소지

- `back/app/services/action_runtime/workflow/meeting/definitions.py:329` (`{**result, "meeting": registration.as_result()}`)
  · `:343` (동일) · `:513` (`{"meeting_sync": outcome.as_result()}`)
  · `back/app/services/action_runtime/workflow/meeting/meeting_chain.py:86-98` (`MeetingRegistration.as_result` → `payload["meeting_id"]`)
  · `:109-117` (`SyncOutcome.as_result` → `payload["meeting_id"]`)
- 근거: **WP-125 §Domain/Schema** — 「예약 원장에 회의 축을 만들지 않는다 — 회의 id 컬럼·payload 키·
  **result 키** 어느 것도 신설하지 않는다」. `complete_execution`/`fail_execution` 이 이 dict 를
  `execution.result` + `action.result`(JSONB) 에 **영속화**하므로, 예약 원장에 회의 id 를 담은 키가
  실제로 선다.
- **반대 근거도 있다(그래서 FAIL 이 아니다)**: SPEC-151 §7.9.7 의 금지는 「**예약 건에서 회의를 찾는**
  새 필드」에 걸려 있고, 코드는 역방향 조회를 끝까지 `by_reservation_run` 하나로만 한다
  (`meeting_chain.py:214,269` — 이 result 키를 **되읽는 코드가 어디에도 없다**). 또 §7.9.4 조합표는
  「원장에 남는 것 = 실패 사유 + 보상 사건」을 **요구**한다. 즉 원장 방향은 뒤집히지 않았고 남는 것은
  **문면 대 구현의 폭 차이**다.
- 권장 수정(코디 판단): ① `as_result()` 에서 `meeting_id`/`title` 만 빼고 `error`·`skipped`·
  `disposition` 만 남긴다(회의 참조는 §7.9.6 이 요구하는 **카드 facts** 에 이미 있다 — `FACT_MEETING`),
  또는 ② WP 문면을 「조회 축을 만들지 않는다」로 좁힌다. **둘 중 하나는 해야 한다.**

### W-2. **채팅 완료 안내 한 줄이 구현되지 않았다** (계약 미구현)

- 해당 코드 없음. `back/app/services/action_runtime/workflow/meeting/const.py:151-161` 에 카드 facts
  문안만 신설되고 채팅 안내 문안은 없다.
- 근거: **SPEC-151 §7.9.6** 「채팅: 완료 안내에 **회의도 등록됐다는 한 줄**이 붙는다. 실패면 같은
  자리에서 사유를 알린다(침묵 종결 금지 — §7.7)」 · **WP-125 §Phase P4** 체크박스 3번.
- 워커가 `wp125-backend-report.md §7-1` 에서 **명시적으로 선언**했고 사유도 댔다(BE 에 예약 완료용
  고정 문자열 템플릿이 없고, 채팅은 카드를 `{action_id}` 참조로만 남겨 facts 가 채팅에 그대로 도달한다
  → 별도 문구 자리를 만드는 것이 「새 표면 0」과 충돌). **은폐가 아니라 사유 있는 미구현**이라 WARN.
- 권장: 코디가 「facts 도달로 §7.9.6 채팅 항목을 만족으로 볼지」를 **명시적으로 판정**하고 P4 완료
  증거에 그 판정을 적는다. 별건 발주가 필요하면 그 발주까지가 이 WP 의 닫힘 조건이다.

### W-3. 체인의 **저장 前 단계에서 난 예외는 보상을 타지 않는다** — 조합표 밖 결말

- `back/app/services/action_runtime/workflow/meeting/meeting_chain.py:209-226` — `run_id_of`(DB) ·
  `by_reservation_run`(DB) · `ReservationPayload.model_validate` · `_resolve_attendees`(DB 2회)가
  **`try` 밖**에 있다. `try`(`:230-245`)가 감싸는 것은 `create_from_reservation` 하나뿐이다.
- `definitions.py:295 _close_reserve_chain` 도 `chain.register_meeting` 호출을 감싸지 않는다.
- 결과(`engine/runtime.py:880-889` 실측): 그 예외는 커널까지 올라가
  **`EXECUTION_FAILED_RETRYABLE` + `ActionStatus.FAILED_RETRYABLE`** 로 닫힌다 ⇒
  ① 외부 예약은 **살아 있는데 보상이 안 돈다**(D 행인데 D 행 로그·facts 가 없다),
  ② 카드가 **재시도 가능**으로 서서 **재시도 명령이 뜬다**.
- 근거: **SPEC-151 §7.9.4** 「회의 생성이 실패하면 그 자리에서 되돌린다 · **재시도는 하지 않는다**」 ·
  「표에 없는 조합은 있을 수 없다」 · **WP-125 §P2 검증** 「재시도 명령 부재」.
- 완화 사실: 재진입하면 `_run_write_step` 이 `external_id` ref 를 재사용해 중복 예약 없이 다시 체인을
  타므로 **자기치유**한다. 발생 조건도 DB 오류·payload 형상 drift 로 좁다. 그래서 WARN.
- 권장 수정: `register_meeting` 본문 전체(또는 `_close_reserve_chain` 의 호출)를 `try` 로 감싸
  **모든 예외를 `MeetingRegistration(error=...)` 로 환원**한다. 한 줄 이동이면 조합표가 전수로 닫힌다.

### W-4. 보상 스텝이 **같은 execution 의 `external_refs` 를 중간에 덮어쓴다**

- `back/app/services/action_runtime/workflow/meeting/definitions.py:265-292 _compensate_reservation`
  → `_run_write_step`(`:230`) → `tools/steps.py:56` `run_idempotent_steps`
- 기계: `run_idempotent_steps` 는 `prior_execution_result(action.id, execution.id)` — **현재
  execution 을 제외한 직전 execution** — 으로 `refs` 를 시드한다(`action_repo.py:270`). 보상이 같은
  execution 에서 두 번째로 이 골격을 타면 첫 실행에서는 `refs = {}` 로 시작하고, 스텝 직후
  `execution.result = {"external_refs": {"compensated": True}}` 로 **재대입**하면서 예약 스텝이 앞서
  적재한 `external_id` 를 **원장에서 지운다**.
- 최종값은 뒤이은 `fail_execution`/`complete_execution` 이 `{"external_refs": refs}`(예약 스텝 refs)로
  덮어 복구되므로 **정상 흐름에서는 관측되지 않는다.** 문제는 그 사이 창이다 — 보상 직후·종결 직전에
  프로세스가 죽으면 원장에 `external_id` 가 없어, 복구 재진입이 `should_run(not refs["external_id"])`
  을 참으로 읽고 **`room.reserve` 를 다시 부른다(이중 예약)**.
- 근거: **WP-125 §Code Surface** 「멱등 스텝 기계가 「이미 성공한 단계를 반복하지 않는다」를 이미
  보증한다(SPEC-151 §5.3.5)」 — 보상이 이 골격을 **두 번째로** 타는 순간 그 보증의 전제(execution 당
  1회 진입)가 깨진다. 또 최종 result 에 `compensated` 앵커가 **남지 않아** 보상 자체도 멱등 앵커가 없다
  (`compensation` 키는 사실 기록이지 스텝 앵커가 아니다).
- 권장 수정: 종결 dict 의 `external_refs` 를 **보상 스텝이 반환한 refs 로 병합**해 적는다
  (`{**refs_reserve, **refs_compensate}`) — 그러면 창이 닫히고 보상도 앵커를 갖는다.

### W-5. `run_id_of` 의 「tenant 바인딩을 가정하지 않는다」가 **바로 옆 호출과 어긋난다**

- `meeting_chain.py:120-133` 은 tenant 바인딩에 기대지 않으려고 `select` 를 직접 조립하고 사유까지
  주석에 적었다(「이 경로가 **실행 tail** 이라 바인딩 유무를 가정할 수 없어서다」).
- 그런데 같은 tail 인 `definitions.py:486` 은 `ActionRepository(ctx.session)` 를 인자 없이 만든다 →
  `action_repo.py:72` `require_tenant(db, None)` → 바인딩이 없으면 `TenantScopeMissing`.
  `_propagate_to_meeting` 의 `try/except`(`:497`)가 그것을 **「파급 실패」로 삼켜** 감사 1건 + fact 1건만
  남기고 지나간다 ⇒ **취소했는데 대기 회의가 살아남는다**(§7.9.5 위반이 조용히 성립).
- 근거: 리뷰어 rules **「재사용·자리 규칙」**(내부 정합) + 코드 자체가 선언한 전제.
  ⚠ **완화**: `tools/steps.py:52` 등 기존 실행 tail 도 이미 같은 방식으로 `ActionRepository(ctx.session)`
  를 쓰므로 **기존 패턴 이탈은 아니다**(그래서 위반이 아니라 WARN).
- 권장 수정: `ActionRepository(ctx.session, action.organization_id)` — 카드가 조직을 들고 있으니 한
  인자로 전제 차이가 사라진다.

### W-6. P0-② 의 **SPEC 환류가 아직 올라가지 않았다** (WP 가 요구한 선행 조건)

- 실측: `workflow/meeting/workflow.py:77-103 active_org_member_query` 가 `User.name`·`User.email` 을
  읽고(조인 범위만 `organization_member`), SPEC-151 §7.2 문면(「이름 = `display_name`, 메일 =
  `work_email`」)과 어긋난다. 코드는 그 사실을 docstring 에 적고 **현행 술어를 그대로 보존**했다 —
  §7.9.3 「코드가 SoT · 발명 금지」에 정확히 부합한다. **코드 쪽 처분은 옳다.**
- 남은 것: **WP-125 §P0 검증** 「② 가 SPEC 문면과 다르면 **SPEC 환류 PR 이 먼저 올라갔다**(또는 그
  필요 없음이 확인됐다)」 — 이 조건이 아직 닫히지 않았다(워커가 `wp125-backend-report.md §6` 에서
  코디 판단으로 올림).
- 권장: planner 에게 §7.2 문면 정정(방향 (a))을 별건 발주. **코드 재작업은 필요 없다.**

---

## 기존 부채 (이번 판정 제외)

- `back/app/models/meeting_v2.py:38,45` — `UP042`(str+Enum → StrEnum) 2건. **선재**이며 이번 diff 는
  같은 파일에 주석만 더했다.
- `MeetingDomain`·`composition.py`·`surface.py` 가 서비스 계층에서 `select()` 를 직접 조립하는
  기존 관례(`composition.py:340` 이 `select(Subject.workflow_run_id)` 를 이미 그렇게 쓴다). 이번
  `meeting_chain.run_id_of` 는 그 관례와 **동형**이라 계층 위반으로 세지 않았다.
- **표시 이름 원천 2축**(예약 = `users.name` / 회의 셀렉터 = `OrganizationDirectory.display_name`).
  이번 diff 가 만든 것이 아니다.

---

## 확인한 것 (PASS 근거) — 브리프 §2 관점별

### 1. 계약 대 코드 — 조합표 A~D ✅

| 행 | 코드 자리 | 확인 |
|---|---|---|
| **A** | `definitions.py:403-470`(선점·대안 0) **무변경** | diff 에 그 블록 없음. WP-119 의 「`EXECUTING → FAILED_TERMINAL` 합법 edge + 실패(종료)」 수리 그대로. 체인 훅은 `refs["external_id"]` **가 있을 때만**(`:398`) 탄다 ⇒ A 는 체인에 도달하지 않는다 |
| **B** | `:326-332` | 체인 성공 후 `complete_execution` 1회. 감사 `EV_MEETING_REGISTERED` |
| **C** | `:349-359` | 보상 성공 → `fail_execution(..., retryable=False)` → `runtime.py:537` 이 `FAILED_TERMINAL` 로 전이(합법 edge) · 판단 축은 **승인**에 머문다(반려 전이 없음) |
| **D** | `:361-372` | 보상 실패 → `complete_execution`(실행 축 **성공 유지**) + `FACT_MEETING_MISSING` 별도 표기 + `log.error("WP-125 조합표 D …")` 에 run 앵커(`action.id`)·`external_id`·회의 실패 사유·보상 실패 사유 **넷 다** |

- **실행 축 기록 시점** ✅ — `_execute_reserve:399` 에서 `complete_execution` 이 **사라지고**
  `_close_reserve_chain` 호출로 바뀌었다. 외부 성공 「시점」에 «성공» 을 적는 자리가 코드에 **없다**.
  ⇒ §5.3.2 표에 없는 «성공 → 실패(종료)» 전이가 구조적으로 불가능하다.
- **보상 대상 정확성** ✅ — `_compensate_reservation:281` `tool_input={"external_id": external_id}`.
  `external_id` 는 `_execute_reserve` 가 받은 **실행 결과의 refs** 그 값이며, 조건 재조회·목록 조회가
  **한 줄도 없다**(파일 전체 grep 확인).
- **bound tool 경유** ✅ — `_bound_tool("room.cancel")` → `_run_write_step` → `run_idempotent_steps`
  (승인 바인딩 `ToolApproval` + `ToolContext` 구성). gateway/`the_connect` 직접 호출 0.
  tool 미바인딩은 `MSG_MEETING_TOOL_UNBOUND` 로 **D 행 처리** — 되돌릴 수단이 없으므로 타당하고,
  워커가 「계약 무언급 자리」로 표기해 두었다.
- **재시도 없음** ✅ — 보상에 루프·재호출 없음. C 는 `retryable=False`.

### 2. source 축 한 자리 ✅

- 정의 1자리: `const.py:37 MEETING_MODAL_SOURCE = "meeting_modal"`.
  `meeting_v2_service.py:88` 은 그 이름을 **재export**(`MEETING_MODAL_SOURCE = MEETING_MODAL_SOURCE_CONST`)
  — 값·문자열 동일, 재선언 아님. grep 결과 문자열 리터럴 `"meeting_modal"` 은 **const.py 한 곳**뿐.
- 판정 1함수: `chain.chain_applies(source)`(`meeting_chain.py:55-61`). 발동(`:206`)과 파급
  가드(`:272`)가 **같은 함수**를 부른다. 테스트가 항등성(`is`)까지 고정(`test_..._exactly_one_place`).
- **P3 가드 2겹 실재** ✅ — `target_meeting:257-274`: ① `by_reservation_run` 로 연결 확인 →
  없으면 None(구 예약 건) ② `chain_applies(origin.source)` → 모달이면 None. **연결이 있어도 배제된다.**
- 🔑 **판정 대상이 amendment 가 아니라 origin 이다** — `surface.py:522,596` 이 취소·변경 카드를
  `source="api"` 로 만들므로, amendment 자신의 source 로 걸었다면 모달 발이 **전부 통과**해 OPEN-031-Y
  가 코드로 닫혔을 것이다. `_propagate_to_meeting:486` 이 `origin_action_id` 로 원 카드를 되읽어
  그 `source` 를 본다 — **계약이 요구한 축이 맞다.**
- 음성 경로 테스트 존재 ✅ — `test_a_modal_origin_meeting_is_not_touched`(soft delete 0 · 연결 유지) ·
  `test_a_modal_origin_meeting_keeps_its_schedule`(예정 일시 불변 · 연결 유지).

### 3. 모달 발 경로 diff 0 ✅

- `meeting_v2_service.py` diff = **① `date` import ② const import ③ `MEETING_MODAL_SOURCE` 재대입
  ④ `create_from_reservation` 신설** 넷뿐. `create_meeting`·`_reserve_room_now`·`_assert_invitable`
  블록은 diff 에 **한 줄도 없다**(리팩토링 이동조차 없다 — 동형이 아니라 **무변경**).
- 상수 이관의 관측 가능 행위 변화 0: 값 `"meeting_modal"` 동일, `meeting_v2_service.py:440
  source=MEETING_MODAL_SOURCE` 호출부 그대로.
- `create_from_reservation` 은 모달 경로를 **부르지도 불리지도 않는다**(양방향 grep 확인).
- 모달 발 run 이 체인에 도달해도 2중 안전: `chain_applies` False(1겹) + `by_reservation_run` 가
  모달이 이미 건 연결을 찾음(2겹).

### 4. 파생 매핑 ✅ (SPEC-151 §7.9.2 전 행)

| 계약 | 코드 |
|---|---|
| 제목 = plan `title` 그대로 | `meeting_chain.py:238 title=payload.title` — 재생성·보정 없음 |
| 예정 일시 = plan `date`/`start`/`end` 그대로 | `:239-241`. **반올림 없음** |
| host = requester | `:221 action.requester_member_id` → `create_from_reservation(host_member_id=...)` |
| 참석자 = `participants` 역해소, host 제외 | `_resolve_attendees:182` (`member_id == host_member_id` → skip) |
| 공개 범위 private | `meeting_v2_service.py` `visibility=MeetingV2Visibility.PRIVATE` |
| 제품 라벨 빈 배열 | `product_tags=[]` (추론 0) |
| 상태 = 회의 도메인 기본 | `repo.create` 기본 `waiting` — 전달 인자 없음 |
| headcount 미저장 | `create_from_reservation` 시그니처에 자리 없음 |
| 30분 슬롯 미적용 | `MeetingV2CreateRequest` 를 지나지 않는다(seam 이 repo 를 직접 부른다). 테스트가 `10:15/11:40` 통과를 고정 |

- **역해소 = 정방향 술어 재사용** ✅ — `workflow.py:77-103 active_org_member_query` 하나를
  `org_members`(정방향)와 `members_for_emails`(역방향)가 **둘 다 호출**한다. 새 술어·새 매칭 규칙
  없음(매칭 축 = 소문자 정규화 이메일, 정방향과 동일). `MeetingDomain` 안에 두어 두 방향이 갈리지
  않게 한 자리 규칙도 지켰다.
- **초대 가능 판정 우회 없음** ✅ — `_resolve_attendees:168,179` 가 `invitable_member_ids` 와 교집합을
  내고, `create_from_reservation` 이 **seam 안에서 다시 한 번** `NotInvitableError` 로 막는다
  (우회 수단 자체가 없다).
- **미해소 = 제외 + 표기, host 미해소만 실패** ✅ — 3사유(정방향 미매칭 / 구성원 미해소 / 계정 미연결)가
  `FACT_MEETING_EXCLUDED` 한 축에 사유와 함께. host 없음만 `MSG_MEETING_HOST_UNRESOLVED` 로 생성 실패.
- **한 트랜잭션** ✅ — `session.begin_nested()`(SAVEPOINT)로 회의 1행 + 참석자 N행 + `link_reservation`
  을 묶는다. 세션 전체 rollback 을 쓰지 않은 사유(바깥에 이번 외부 write 의 감사·실행 원장이 있다)도
  타당하다.
- **payload 무변경** ✅ — `action.payload` 에 대입하는 코드 0(diff 전체 grep).

### 5. migration 0135 ✅

- 부분 유니크 인덱스 1건 = 계약 「예약 건당 회의 최대 1」(§7.9.1)의 **반대 방향**이고, 기존 「회의당
  예약 최대 1」과 혼동되지 않게 `models/meeting_v2.py:74-78` 주석이 두 방향을 갈라 적었다.
- 조건 `reservation_run_id IS NOT NULL AND deleted_at IS NULL` 이 **조회 술어
  `by_reservation_run`(`meeting_v2_repo.py:129-133`)과 글자 그대로 같다** — 「조회는 없다는데 INSERT 는
  걸리는」 자리가 없다. nullable FK 에 대한 partial index 로 구 데이터(NULL 다수)도 안 걸린다.
- soft delete 된 회의가 재등록을 막지 않는다 ✅(테스트 `test_a_closed_meeting_does_not_block_the_run`).
- **다운그레이드 왕복** ✅ — `downgrade()` 가 `drop_index` 하나. 데이터 손실 0, 재적용 가능.
- `revision = "0135_meeting_reservation_uq"` **27자** ≤ `alembic_version.version_num` varchar(32) ✅.
- **head 유일** ✅ — `down_revision = "0134_baseline_publish_agent"` 를 참조하는 파일이 0135 하나
  (grep 확인). 분기 head 없음.
- 배포 시 중복 데이터가 있으면 **멈추는 것이 의도**임을 revision docstring 이 명시하고, 워커 리포트
  §7-3 도 배포 창 재확인을 남겼다.

### 6. 신설 금지 목록 — 전부 0 ✅

| 금지 | 확인 |
|---|---|
| 새 endpoint | diff 에 `routers/` 파일 **0** |
| 새 leaf | diff 에 leaf·MCP 툴 등록 **0** (`mcp/` 무변경) |
| 새 state enum 값 | `models/meeting_v2.py` diff = **주석 5줄뿐**. 테스트가 `["waiting","live","paused","ended"]` 고정 |
| 새 카드 명령 | `const.py` 추가분 = `EV_*` 6 · `FACT_*` 4 · `MSG_*` 7 · `MEETING_MODAL_SOURCE` 1. **CTA·choice kind·명령 0**. 테스트가 `USER_PICKED_CHOICE_KINDS`·`REQUIRED_FACTS` 고정 |
| DELETE 사용자 표면 | 「닫는다」= `repo.soft_delete`(서버 처분). 라우터·스키마 변경 0 |
| 예약 원장 새 컬럼 | migration 은 **인덱스 1건**뿐. 컬럼 추가 0 |

### 7. allowed_paths ✅ — 재확인

`git status --porcelain` 10줄 전부 `back/` 접두. `front/`·`mcp/`·`context/`·spec 리포 **무변경**.

### 8. 테스트가 계약을 고정하는가 ✅ (읽어서 확인 — 실행 안 함)

`tests/services/engine_v2/test_wp125_reservation_meeting_chain.py` 896줄 · 34 케이스(파라미터화 포함).
대역 `_Ctx` 는 **세션이 진짜 DB**이고 `complete_execution`/`fail_execution` 이 실행 원장과 카드 상태를
**둘 다** 옮긴다 — 「실행 축을 언제 적었나」를 `ctx.terminal` **순서 목록**으로 볼 수 있게 만든 설계라
관대한 대역이 아니다.

물고 있는 것:
- **조합표 전수** — A(선점·대안 0 → `FAILED_TERMINAL` + `cancel.calls == []`) · B(회의 1건 + 연결 +
  `EV_MEETING_REGISTERED`) · C(`cancel.calls == [{"external_id": "ext-1"}]` **그 하나만** ·
  `ctx.completed == []` 「성공을 한 번도 적지 않았다」 · `retryable is False`) ·
  D(`terminal == [SUCCEEDED]` · `caplog` 에 「조합표 D」·`ext-1`·`action.id`)
- **실행 축 1회 기록** — `len(ctx.terminal) == 1` **and** `EXECUTION_SUCCEEDED not in ctx.terminal`
  ⇒ 「성공 적고 나서 실패로 덮기」가 되살아나면 즉시 빨개진다. 🔑 이 파일의 최고 가치 단언
- **source 게이트** — 모달 발 이중 생성 0 + `cancel.calls == []`(미발동은 실패가 아니다) ·
  정의 항등성(`is` 비교)
- **멱등** — 재진입 시 회의 id 동일 + `skipped == already_linked`
- **P0-③ 2겹** — DB 가 두 번째 live 행을 `IntegrityError` 로 거절 / soft-deleted 는 재등록 허용
- **역해소 4경계** — 전원 해소(제외 fact 없음) / 일부 미해소(회의는 선다 + 사유 표기 + 정방향
  `unmatched` 도 같은 축) / 계정 미연결(회의 규칙으로 제외) / **host 미해소 = 유일한 생성 실패 → 보상**
- **술어 이중화 금지** — `inspect.getsource` 로 두 메서드가 `active_org_member_query(` 를 **2회 호출**
  하고 조건(`OrganizationMember.status`)을 **다시 쓰지 않음**을 검사. 소스 문자열 검사라 다소 취약하지만
  「두 벌이 되는 순간」을 잡는 목적에는 유효하다
- **동기화 8분기** — 취소 × (대기 soft delete / live·paused·ended 연결만 끊기 ×3 파라미터) ·
  변경 × (대기 reschedule / live·ended 유지 ×2) · 연결 없는 run × (취소/변경) ·
  ⚠ **모달 발 음성 단언 × 2**(연결은 **있는데** 손대지 않음) — 계약이 열어 둔 축이 조용히 닫히면 잡힌다
- **파급 실패** — 예약은 그대로 반영 + `EV_MEETING_SYNC_FAILED` + fact, 회의 무손상
- **표면 5건** — facts +1(회의 참조 · 제목·id) · 명령/enum/choice kind/REQUIRED_FACTS 증가 0 ·
  `{label,value}` 축(FE 새 컴포넌트 0) · JSONB **재대입** 검증 · 재진입 중복 적재 0

**기존 테스트 조정 1건도 타당** — `test_meeting_definitions.py:130-138` 이 `_action()` 기본 `source` 를
모달 발로 고정했다. 그 파일이 보는 것은 예약 **실행 기계**(멱등 스텝·선점 복구·reconcile)이고, 채팅
발로 두면 그 파일의 세션 대역에 원장이 없어 **조합표 D 로 초록이 나** 검증이 무의미해진다 — 사유가
주석으로 남았고 체인 자체는 신규 파일이 고정한다.

**테스트가 못 잡는 것(W-3·W-4 와 짝)**: 체인 저장 前 예외 경로 · 보상 스텝의 `external_refs` 중간
덮어쓰기 · C/D 카드 **명령 목록**에 재시도가 없다는 직접 단언(현재는 `retryable=False` 로 간접 고정).

---

## 코디네이터에게 — 처리 제안

| # | 항목 | 제안 |
|---|---|---|
| W-1 | result 키에 회의 id | **판정 필요.** `as_result()` 에서 `meeting_id`/`title` 제거(1~2줄) 또는 WP 문면 조정. 회의 참조는 카드 facts 에 이미 있으므로 제거해도 §7.9.6 손실 0 |
| W-3 | 저장 前 예외 → 보상 미발동 | **backend 재발주 권장(소).** `register_meeting` 을 통째 `try` 로 감싸면 닫힌다 |
| W-4 | 보상 스텝 refs 덮어쓰기 | **backend 재발주 권장(소).** 종결 dict 의 `external_refs` 를 병합 |
| W-5 | `ActionRepository` tenant 인자 | 선택. `action.organization_id` 를 넘기면 1줄 |
| W-2 | 채팅 완료 안내 | **코디 판정 후 P4 완료 증거에 기록.** 별건이면 별건 발주 |
| W-6 | SPEC-151 §7.2 문면 정정 | **planner 별건 발주.** 코드 재작업 불필요 |

W-1·W-3·W-4·W-5 는 **한 번의 작은 재발주로 묶어서** 처리 가능하다(전부 `definitions.py` +
`meeting_chain.py` 국소 수정, 새 테스트 2~3건). 그 뒤 재검수는 diff 국소라 짧다.
