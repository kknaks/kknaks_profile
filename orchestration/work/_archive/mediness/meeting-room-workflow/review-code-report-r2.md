# 재검수 리포트 R2 — meeting-room-workflow / WP-125 backend (2026-08-31)

## 판정: PASS

코디 판정 4건(W-1·W-3·W-4·W-5)이 **전부 해소**됐다. 넷 다 원 리뷰가 적은 **권장 수정 그대로**
들어갔고, 넷 다 **되돌아가면 빨개지는 테스트**가 함께 섰다(신규 5클래스 · 테스트 파일 896→1101줄).
고친 자리 주변에서 **신규 문제 0** — 모달 발 경로 diff 는 여전히 **0**이고, `ruff check` 는 변경
3파일 전부 통과(`All checks passed!`). 남는 것은 W-2·W-6 **캐리 2건**과 nit 1건뿐이다.

> 재검수 범위 한정 — 전면 재리뷰가 아니다. R1 이 PASS 로 확인한 축(조합표 A~D · source 축 ·
> 파생 매핑 · migration 0135 · 신설 금지 목록 · allowed_paths)은 다시 세지 않았다. 이번에 본 것은
> **바뀐 자리와 그 이웃**이다.

---

## 검수 방법

- 워크트리 **read-only** — 수정·stash·checkout **0**, 테스트 실행 **0**(코디가 74 passed 독립 확인).
  리포 파일 수정·생성 0(이 리포트 1개만 신설).
- `git status --porcelain` = R1 과 동일한 **10파일**(수정 7 + untracked 3), `+465/−24`
  (R1 `+433` 대비 **+32** — 수리분).
- 실행한 것: 파일별 `git diff` 전문 정독 · `meeting_chain.py`(461줄) 전문 재독 ·
  `tools/steps.py run_idempotent_steps` 기계 재확인 · `tenancy.require_tenant` 실측 ·
  `ActionEvent` 소비처 grep · `uv run ruff check`(3파일).

---

## 항목별 판정

### W-1 — 실행 result 의 회의 id 키 → **해소 ✅**

**회의 참조가 result 에서 완전히 빠졌다.** 원 리뷰 권장 ①(「`as_result()` 에서 `meeting_id`/`title`
만 빼고 `error`·`skipped`·`disposition` 만 남긴다」) 그대로다.

- `meeting_chain.py:101-108` — `MeetingRegistration.as_result()` 가 싣는 것은
  `excluded`/`error`/`skipped` **셋뿐**. `meeting_id`·`title` 대입 코드 없음.
- `meeting_chain.py:121-126` — `SyncOutcome.as_result()` 는 `disposition`/`error` **둘뿐**.
- 두 dataclass 는 `meeting_id`·`title` 필드를 **여전히 갖지만**(`:73-74`, `:115`) 그 값이 가는
  곳은 **카드 facts 한 자리**다(`registration_facts:417-420` → `FACT_MEETING`) — §7.9.6 이 요구한
  자리이고 §7.9.7 이 금지한 자리가 아니다. **잃은 것 0**.
- 고정 테스트 3건 — `test_the_execution_result_carries_no_meeting_reference`(종결 dict 를 `repr`
  통째로 훑어 회의 id·`meeting_id`·`title` 부재 + facts 에는 **있음**을 같이 단언) ·
  `test_the_sync_result_carries_only_the_disposition` · `test_as_result_keeps_only_reasons_and_events`
  (`tests/…/test_wp125_reservation_meeting_chain.py:903-945`).

**감사 이벤트의 `meeting_id` 는 원장 방향과 충돌하지 않는다 ✅** — 별도로 실측했다.

- 자리: `definitions.py:348-351` — `EV_MEETING_REGISTERED` payload 에
  `{"meeting_id": ..., "excluded": [...]}`.
- `runtime.py:585-605 audit()` → `AuditRepository.add_action_event(ActionEvent(...))` — **append-only
  사건 기록**이고 `execution.result`/`action.result`(JSONB) 와 **다른 테이블**이다.
- §7.9.7 이 막는 것은 「**예약 건에서 회의를 찾는** 새 필드」다. 실측: `ActionEvent.payload` 를
  **조회 술어로 쓰는 코드가 0**이다(grep — `event.payload` 히트는 전부 `WorkflowEvent`(명령 봉투)
  소비처이고 `ActionEvent` 가 아니다). 「이 예약의 회의」를 묻는 경로는 끝까지
  `by_reservation_run` **하나**다(`meeting_chain.py:255,311`).
- ⇒ **조회 축 신설 0**. 사건이 일어난 사실을 사건 기록에 적은 것이고, 이건 §7.9.4 가 「원장에 남는
  것」으로 **요구**한 방향이다.

### W-3 — 저장 前 예외의 조합표 밖 결말 → **해소 ✅**

**경계가 함수 전체로 옮겨졌고, 저장 前 4단계가 전부 그 안에 들어왔다.**

- `meeting_chain.py:241-245` — `register_meeting` 이 `try` / `except Exception` 으로
  `_register_meeting` **전체**를 감싼다 ⇒ 모든 예외가 `MeetingRegistration(error=...)` 로 환원.
- 저장 前 4단계가 전부 `_register_meeting`(`:248-291`) 안 = `try` 안이다:
  `run_id_of`(`:250`) · `by_reservation_run`(`:255`) · `ReservationPayload.model_validate`(`:266`) ·
  `_resolve_attendees`(`:267`). ⇒ 원 리뷰가 지목한 **네 자리 전부** 보상 경로로 들어왔다.
- 호출부(`definitions.py:340`)는 이제 `registration.failed` 하나만 본다 — 실패 단계로 결말이
  갈리지 않는다. `_close_reserve_chain` 을 별도 `try` 로 감쌀 필요가 없어진 이유다.
- 🔑 **SAVEPOINT 도 함께 넓혔다**(`:242 async with session.begin_nested()`). 저장 前 DB 오류가
  트랜잭션을 abort 로 남기면 **보상이 쓰는 원장 조회·감사도 연쇄 실패**한다 — 바깥 SAVEPOINT 가
  그 자리를 되돌려 보상이 실제로 돌 전제를 만든다. 이건 원 리뷰가 「한 줄 이동」으로 적은 것보다
  **한 겹 더 나간 수리**이며, 없으면 W-3 수리가 D 행 기록에서 다시 깨졌을 자리다.
- 게이트(`chain_applies`, `:239`)만 `try` 밖 — DB 를 타지 않으므로 미발동이 트랜잭션 경계를
  만들지 않는다. 타당하다.
- 안쪽 SAVEPOINT(`:272`)는 그대로 남아 「**제외 표기를 함께 실어 보내는**」 역할을 지킨다
  (`:285-287` — 저장만 되돌리고 `excluded` 를 살려 반환).

**FAILED_RETRYABLE 노출 잔존 0 ✅** — 체인 진입 이후 경로를 추적했다.

- `_compensate_reservation` 의 DB 접촉은 전부 `try`(`definitions.py:302-311`) 안이다
  (`_bound_tool:300` 은 순수 dict 조회). ⇒ 보상 실패도 예외가 아니라 **사유 문자열**로 나온다.
- 남는 것은 `ctx.audit`/`complete_execution`/`fail_execution` 자체의 실패뿐인데, 그건 **모든 실행
  경로에 공통인 선재 조건**이고 이번 diff 가 만든 자리가 아니다.
- 고정 테스트 4건(`:947-1022`) — `test_a_failure_before_the_save_still_compensates`
  (`_resolve_attendees` 폭파 → `cancel.calls == [{"external_id": "ext-1"}]` · `FAILED_TERMINAL` ·
  `retryable is False`) · `test_a_failure_before_the_save_without_compensation_is_row_d` ·
  `test_register_meeting_never_raises`(**함수 경계 계약**을 직접 단언) ·
  `test_the_session_survives_a_database_error_so_compensation_can_run`(payload 파손 후 세션이
  살아 있음을 `ActionRepository(db, org).get` 성공으로 확인 — SAVEPOINT 확대를 정확히 문다).

### W-4 — 보상 스텝의 `external_refs` 덮어쓰기 → **해소 ✅, 크래시 창 닫혔다**

원 리뷰 권장(「종결 dict 의 `external_refs` 를 보상 refs 와 **병합**」)보다 **한 겹 더** 갔다 —
종결 dict 뿐 아니라 **execution 행에도 즉시 되돌려 적는다**.

- `definitions.py:299 merged = dict(refs)` — 예약 스텝 refs 를 복사(호출부 dict 를 변형하지 않는다).
- 성공: `:312-314` `merged.update(compensation_refs)` → `execution.result = {"external_refs": merged}`
  → `(None, merged)` 반환.
- 실패: `:309-311` — 골격이 이미 덮었을 수 있으므로 `execution.result = {"external_refs": merged}`
  로 **원 `external_id` 를 되돌려 적고** `(사유, merged)` 반환.
- 호출부: `:361-372` — 반환된 `refs`(=merged)가 종결 dict 의 `external_refs` 로 들어가고, C 행
  `fail_execution`(`:381`)·D 행 `complete_execution`(`:400`) 둘 다 그 값을 적는다.

**창이 실제로 닫혔는지** — 기계로 확인했다. `steps.py:63` 의 중간 persist
(`execution.result = {"external_refs": dict(refs)}`)와 `definitions.py:313` 의 재대입 사이에는
**`await` 가 하나도 없다**(`run_idempotent_steps` 반환 → `_run_write_step` 반환 → `merged.update`
→ 재대입). 세션은 동시 사용되지 않으므로 그 사이에 **flush·commit 이 끼어들 수 없다** ⇒ 원장에
`external_id` 가 빠진 스냅샷이 **DB 에 도달하는 순간 자체가 없다.** 복구 재진입이
`should_run(not refs["external_id"])` 을 참으로 읽는 경로가 사라졌다 = **이중 예약 시나리오 종결**.

- 덤: `compensated` 앵커가 **최종 원장에 남는다** ⇒ 보상 자체도 멱등 앵커를 갖는다(원 리뷰가
  「없다」고 지적한 것).
- 고정 테스트 3건(`:1025-1077`) — `test_the_terminal_ledger_keeps_both_anchors`(종결 dict 에
  `external_id` **와** `compensated` 둘 다) · `test_the_execution_row_never_loses_the_external_id_mid_flight`
  (**보상 직후·종결 직전** 의 `execution.result` 스냅샷을 직접 본다 — 창을 정조준) ·
  `test_a_failed_compensation_also_keeps_the_external_id`.

### W-5 — `ActionRepository` tenant 인자 → **해소 ✅, 테스트가 tail 을 정확히 문다**

- `definitions.py:521` — `ActionRepository(ctx.session, action.organization_id).get(origin_action_id)`.
  원 리뷰 권장 1줄 그대로. diff 로 확인(`ActionRepository` 히트 2줄 = import + 이 줄).
- 기계 확인: `tenancy.py:129-140 require_tenant` 는 「명시 인자 > 세션 바인딩 > 에러」 ⇒ 인자가
  들어오면 바인딩 유무와 **무관**하게 통과한다. `TenantScopeMissing` 이
  `_propagate_to_meeting` 의 `except`(`:526`)에 「파급 실패」로 삼켜지는 경로가 사라졌다.
- **고정 테스트가 그 tail 을 문다 ✅** — `test_the_propagation_tail_does_not_need_a_session_binding`
  (`:1097-1108`): `bind_tenant(db, None)` 로 바인딩을 **끄고** `_propagate_to_meeting` 을 직접 호출한 뒤
  ① `meeting.deleted_at is not None`(파급이 실제로 돌았다) ② `EV_MEETING_SYNC_FAILED not in ctx.audits`
  (**삼켜지지 않았다**) ③ `disposition == closed` 를 단언한다.
  🔑 인자를 되돌리면 `require_tenant(db, None)` → `TenantScopeMissing` → ①②③ 이 **동시에** 빨개진다.
  파급 tail 만 떼어 부른 설계도 옳다 — 앞단 골격(`steps.py:56` `ActionRepository(ctx.session)`)까지
  태우면 재는 것이 W-5 가 아니라 선재 배선이 된다(테스트 docstring 이 그 사유를 적어 뒀다).
- **선재 형제 자리 재확인** — `definitions.py:191`(`_execute_update` 게이트) ·
  `:643`(`_reconcile_cancel`)도 인자 없이 만들지만 둘 다 **fail-closed**(원본을 못 읽으면 통과시키지
  않거나 `unknown` 으로 닫는다)라 W-5 가 지적한 **조용한 삼킴이 성립하지 않는다.** 이번 diff 무변경
  이고, 같은 부류의 잔존 구멍은 없다.

---

## 신규 문제 — **0건**

고친 자리 주변만 봤다.

| 확인 | 결과 |
|---|---|
| **모달 발 경로 diff 0 유지** | `meeting_v2_service.py` hunk **여전히 3개**(`@@ -8,2 +8,3`, `@@ -64,2 +65,5`, `@@ -78,3 +82,66`) = ① `date` import ② const import ③ 재export + `create_from_reservation`. `create_meeting`·`_reserve_room_now`·`_assert_invitable` 블록 diff **0줄** |
| 다른 5파일 회귀 | `models`(+5) · `repo`(+58) · `const`(+44) · `workflow`(+81/−17) · `test_meeting_definitions`(+9) — R1 검수분 그대로, 수리는 `meeting_chain.py`·`definitions.py`·신규 테스트에만 들어갔다 |
| refs 별칭 오염 | `merged = dict(refs)`(`:299`) — 호출부 `result["external_refs"]` 를 제자리 변형하지 않는다 ✅ |
| SAVEPOINT 이중 중첩 | 바깥(`:242`) + 안쪽(`:272`). 안쪽 rollback 후 정상 return 이면 바깥은 RELEASE — 저장분은 이미 되돌아간 뒤라 **되살아나지 않는다** ✅ |
| 보상 skip 경로 | 재진입으로 `compensated` 가 prior refs 에 이미 있으면 골격이 스텝을 skip → `merged.update` 는 같은 값 ⇒ 부작용 0 ✅ |
| lint | `ruff check meeting_chain.py definitions.py test_wp125_…py` → **All checks passed!** (신규 error 0) |
| allowed_paths | 10파일 전부 `back/` 접두. `front/`·`mcp/`·spec 리포 무변경 ✅ |

### nit 1건 (판정 아님 — 기록만)

`definitions.py:352-354` — B 행에서 `{**result, "meeting": registration.as_result()}` 를 무조건
싣는다. 깨끗한 성공(제외 0)이면 `as_result()` 가 `{}` 라 종결 result 에 `"meeting": {}` 라는
**빈 키**가 남는다. 회의 축이 아니므로 W-1 재발이 아니고 소비처도 없다. 다만 같은 파일
`:534`(`_propagate_to_meeting`)는 이미 「비면 키 자체를 만들지 않는」 패턴
(`{...} if outcome.as_result() else {}`)을 쓰므로 **두 자리의 관례가 갈렸다.** 한 줄이면 맞출 수
있으나 재발주 사유는 아니다.

---

## 캐리 (이번 재검수 대상 아님 — R1 에서 이월)

| # | 항목 | 상태 |
|---|---|---|
| **W-2** | 채팅 완료 안내 한 줄(SPEC-151 §7.9.6 · WP-125 P4-3) | **코디가 「facts 도달로 만족」 처리** — 코드 무변경. 그 판정을 P4 완료 증거에 남기는 것까지가 닫힘 조건 |
| **W-6** | SPEC-151 §7.2 문면 정정(`display_name`/`work_email` ↔ 코드의 `User.name`/`User.email`) | **planner 별건.** 코드 처분은 옳다(§7.9.3 「코드가 SoT」) — 재작업 불필요. `workflow.py:77-103` 무변경 확인 |

---

## 코디네이터에게

- **재발주 불필요.** W-1·W-3·W-4·W-5 전부 닫혔고, 넷 다 회귀 테스트를 동반한다.
- 다음 단계(사용자 리뷰 / PR)로 진행 가능하다. 남은 닫힘 조건은 **W-2 판정 기록**과
  **W-6 planner 별건 발주** 둘뿐이며, 둘 다 `back/` 코드와 무관하다.
