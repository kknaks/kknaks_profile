# 리뷰 리포트 — reservation-update-mcp / backend(code) (2026-08-31)

## 판정: **PASS** (WARN 5 — 전부 진행 가능. FAIL 사유 0)

WP-128 P1·P2·P3 이 계약대로 착지했다. **위반 0** — 툴은 thin wrapper 로 남았고(판정 0벌 추가), 무조건
제약·무한정 `from now` 두 문장이 실제로 사라졌으며, 되묻기 결정이 워크플로 선택 **앞**에 갈렸고,
인벤토리 62 는 실측 +1 로 정합한다. WARN 5건은 **계약이 허용한 선택의 부수 성질**(W1)과 **테스트가
덜 문 자리**(W2·W5), **문면이 예시에 기대는 자리**(W3), **이 워커 범위 밖 잔여**(W4)다.

## 검수 범위

- diff: working tree vs HEAD(`d9ff01e1`) — 수정 8 + untracked 3 = **11 파일 · +169/−23**. 전부 `back/`·`mcp/`.
- 실행한 검사(read-only — 브리프 지시대로 **수정·테스트 실행 0**):
  - `git diff` 전문 정독(provider.py · service.py · server.py · 인벤토리 4파일 · 테스트 3파일)
  - 신설 2파일 + 동형 표본 2파일 전문 대조(`reservation_update_request.py` ↔ `reservation_cancel_request.py`, 각 테스트)
  - SSOT 대조: WP-128 전문 · SPEC-151 §6.2·§6.2b·§7.10 전문
  - back 실물 확인: `action_runtime_v2.py:2051` (`attach_update_ep`) · `meeting/surface.py:550-590` (`attach_update_amendment` 의 date 판정)
  - 인벤토리 **정적 실측**: `grep -c '^@mcp.tool' mcp/app/server.py` = **62**, `_wrap_write_tool(` 호출부 **23** − 미등록 `decision_register_tool`(server.py:967, `@mcp.tool` 없음) **1** = write **22** ⇒ read **40**
  - 감사 프롬프트 무개정: `git diff -U0` hunk 좌표가 `build_prompt`(~215) 다음 `__all__`(353)로 건너뛴다 — 규칙 6(provider.py:304)은 hunk 밖

## 위반 (FAIL 사유)

**없음.**

## 관점별 판정

### ① 툴이 정말 thin wrapper 인가 — **PASS**

- **cancel 동형**: `reservation_update_request.py:83-130` 이 `reservation_cancel_request.py:68-100` 과 **구조·순서·변수명까지 동형**이다 — `require_uuid` → `POST` → `raise_for_error` → `card`/`action_id`/`surface` → lines 조립 → `structured{data, action_id, workflow_run_id, plan_version?}`. 등록부(`server.py:1737-1774`)도 취소 형제(1714-1734)와 같은 `access(...)` 배치·같은 줄바꿈 형태다(⚠ `meta=access(taint_policy=…,` 의 어색한 개행은 **표본 그대로**이지 새 편차가 아니다).
- **선언**: `taint_policy=TAINT_SELF_LEDGER` · `capability="action.runtime.basic"` · `needs=("reservation_list_tool","reservation_get_tool")` — SPEC-060 예고 ④(spec-060:185)가 못 박은 값과 **문자 그대로 일치**. 툴 전용 leaf 0.
- **409/404**: back 에러를 `raise_for_error` 가 번역하고 툴은 **404 안내 문구만** 자기 것으로 준다(`_NOT_FOUND`, :62-65 — cancel 과 문면까지 동일). 409 는 「재시도하지 말고」를 실은 채 `ValidationError` 로 나간다(테스트 :123-148 이 고정).
- **오염 등급**: `test_wp116_taint_policy.py:111` `test_the_real_server_declares_every_write_tool` 이 신규 write 를 자동으로 덮고, `test_the_beyond_caller_set_is_pinned`(:210)이 등급 오분류를 잡는다.
- **감사 문구**: `server.py:295-301` — 「예약 **변경 요청 접수** — 승인 대기」. 집행 선언(「변경됐다」) 없음. 테스트 :262-272 가 `"변경됨" not in summary` 로 고정.
- **새 REST·leaf·카드 유형 0**: `back/` diff 0(P1 파일 목록이 `mcp/` 뿐) · 새 `@router` 0 · 카드 type 은 선재 `meeting_room.update`.
- 🔑 **date 를 툴이 판정하지 않는다** — `:87-91` 은 `is not None` 필터만 걸고 `date` 를 **그대로** 실어 보낸다. 판정은 `back/…/meeting/surface.py:569-571`(`revision["date"] != previous.date` → 422)이 단독 소유한다. 테스트가 **양쪽**을 고정한다: 불일치 422(:168-192, body 에 `date` 가 실려 나간 것까지 단언) · **동치 통과**(:194-213). SPEC-151 §6.2 「무조건 거절이 아니다」와 정합.

### ② 규칙 재작성 — **PASS**

- **금지 구절 2개 부재**: `TIME_RESOLUTION_RULE`(provider.py:32-45)에 `must start in the future` 없음 · `from now` 없음. 테스트가 **둘 다** 단언(`test_time_resolution_askback.py:73-74, 85`) — WP §P2-A 의 「하나만 지우면 나머지가 그 일을 계속한다」 규율 충족.
- **R-1~R-4 가 규칙 문면에 선다**: R-1 `AS SPOKEN` + 실측 사례(15:08 / TODAY 15:00-16:00) · R-2 `its END time has passed` + 「시작만 지난 것은 R-1」 · R-3 `INSIDE the given date` · R-4 `Only when NO date was given`. 각각 :91-119 가 단언.
- **now-상대가 «날짜 없는 요청» 한정**: `choosing the nearest upcoming one when no date was given` — 두 갈래(`when no date was given` / `INSIDE the given date`)가 **문면에 함께** 있고 테스트 :87-88 이 둘 다 단언한다. WP §P2-A 의 「두 갈래를 명시해야 한다」 충족.
- **기존 예시 2개 보존**: `"10시반" today means 22:30` · `"3시" means 15:00` 이 그대로 살아 있고(:106-107 단언), 신규 `"9월 3일 3시" means 15:00 on 9월 3일` + `it never moves the date` 로 R-1↔R-3 동시 성립을 문면에 세웠다(:118-119). **새 해석 축 0.**

### ③ 되묻기 배선 — **PASS**

- **결정이 워크플로 선택 «전»**: `service.py:686-704` 의 `clarification` 분기가 `tool_calls` 실행 루프(:745~)보다 **위**에 있고 `return` 으로 턴을 끝낸다. §7.10 「되묻기는 워크플로를 «고르기 전» 에 갈려야 한다」 충족. 산출 축은 `CatalogTurn.clarification`(provider.py:78)이고 `build_prompt` 가 3번째 선택지로 배선(:188).
- **되묻는 턴 카드 0**: 워크플로 미선택 = Action 미생성. 런타임 테스트가 실물로 고정 — `test_the_ask_back_turn_answers_and_stands_no_card…:302` `assert await _actions(db) == []`.
- **감사 규칙 6 무개정**: `git diff -U0` hunk 가 `build_prompt`(+215) 다음 `__all__`(+353)로 건너뛰어 `build_final_audit`/`build_audit_prompt` 본문과 규칙 6(provider.py:304 `Use clarification only when required input is genuinely missing…`)이 **diff 밖**임을 확인. 테스트도 역방향으로 단언(`ASK_BACK_RULE not in audit`, :136-139).
- 🔑 **「감사 스코프 밖으로 내보냄」이 §7.10 의 출구/결정 분리와 맞는가 — 맞다.** §7.10 은 되묻기가 「채팅이 이미 되묻기를 내보내는 자리와 **같은 출구**」로 나갈 것을 요구한다. 구현은 `_finalize(session, job, user, thread, clarification, executed, focused, untrusted_origin=…, absorbed_message_ids=…)`(:700-704)로 나가는데, 이는 감사 경로의 `_finalize` 호출(:731-742)과 **인자 목록까지 동일**하다 — 우회로가 아니라 **같은 출구**다. 갈린 것은 그 앞의 `_audit` 통과 여부뿐이고, 그것이 정확히 §7.10 이 계약으로 못 박은 「감사는 이 되묻기를 억제하지 않는다」의 구현이다. WP §P2-C 가 제시한 두 수단 중 「정형 응답 축으로 내보내기」를 골랐고 **규칙 6 은 손대지 않았다** — 지정된 선택지 안이다.

### ④ 인벤토리 실측 +1 — **PASS**

- **62 = 40 + 22 가 실측이다.** 정적 대조로 독립 확인: 등록 `@mcp.tool` **62**개 · write seam 호출 **23**개 − 미등록 `decision_register_tool` **1** = **22** ⇒ read **40**. `EXPECTED_READ=40` / `EXPECTED_WRITE=22` / `EXPECTED_TOTAL=62`(test_tool_inventory.py:34-36)와 정확히 일치.
- **test_tool_inventory 규율 준수**: read/write 를 **seam**(`_wrap_write_tool`)으로 세는 파일 머리 규율 유지 · 주석이 「착수 시점 실측 61 + 1」임을 명시하고 「SPEC-060 표의 예고 숫자(read 39 + write 18)를 옮겨 적지 않았다」를 기장(:31-33). WP §P1-D 규율 충족.
- `EXPECTED_WRITE_TOOLS` 에 이름 1개 추가 · 예약 write 를 7 로 정정(요청·승인·거절·수정·철회·취소요청·변경요청 = 7 — 실물과 일치).
- **부수 4파일 = 수치 동기뿐**: `test_read_file_offset.py` 61→62 · `test_wp116_tools_list_filter.py` 61→62 ×2 · `test_wbs_tools.py` 61→62 + 주석. 로직·단언 축 변경 0.
  - ⚠ 참고: `test_wbs_tools.py:723` 주석은 `write 20`→`write 22`(**+2**)다. HEAD 에서 그 주석이 이미 총계 61(=40+21)과 어긋나 있던 **선재 드리프트**를 함께 맞춘 것이며, 주석 숫자 외 변경은 없다. 같은 성격의 정정이 `test_tool_inventory.py` 의 「예약 5 → 예약 7」에도 있다.

### ⑤ 테스트가 계약을 무는가 — **PASS** (WARN 2 동반)

WP §검증 체크리스트 대조:

| WP 검증 항목 | 무는 테스트 | 판정 |
|---|---|---|
| P1 성공(action_id 최상위·workflow_run_id·「아직 변경되지 않았다」) | `test_reservation_update_request.py:62-82` | ✅ |
| P1 409 + 재시도 금지 안내 | :123-148 | ✅ |
| P1 404 + `run_id` 축 안내 | :150-166 | ✅ (`action_id` 오투입은 UUID 형태가 같아 back 처분이 동일 — 안내 문구를 `workflow_run_id` 로 단언) |
| P1 422 `update_date_forbidden` | :168-192 (+ body 전달까지) | ✅ |
| P1 **date 동치 통과** | :194-213 | ✅ |
| P1 익명 `service:*` 거부 | :252-260 | ⚠ **W5** — seam 존재 단언(표본 동일) |
| P1 인벤토리 3자 중 코드 2자 | `test_tool_inventory.py` · `test_wbs_tools.py`(`/health` == `len(registered)`) | ✅ (SPEC 표는 **W4**) |
| P1 즉시형 0 | :274-280 (금지 이름 3개 부재) | ✅ |
| P2 **R-1 고정** | 문면 :91-99 + 런타임 `test_yes_books_exactly_what_was_spoken…:305-338`(완전히 지난 창으로 카드 payload date/start/end 가 **그대로** 남는지 실물 Action 으로) | ✅ |
| P2 되묻기 — 지난 시각 → 질문·카드 0 | :268-302 | ✅ |
| P2 질문 2사실 | :142-152 (ⓐ `has already passed` + `naming the exact date and time` ⓑ `whether to book it exactly as spoken`) | ✅ 「고정 문구 템플릿 0」과 양립(문자열 일치가 아니라 규율의 존재를 단언) |
| P2 **감사 포함 회귀** | :268-302 — 감사를 **끄지 않고 「되돌리는」 감사(`allowed=False`+clarification)를 배선한 채** 돌려 `audited == []` 와 결정 축 질문의 통과를 단언 | ✅ WP 가 요구한 「그 층을 덮어야 한다」 충족 |
| P2 「잡아 달라」 → 말한 그대로 + 승인 게이트 평소대로 | :305-338 (`status == needs_approval`) | ✅ |
| P2 「아니」 → 카드 0 · 예약 건 0 | :341-356 | ✅ |
| P2 R-3·R-4 무회귀 | :102-109 | ✅ |
| P2 R-1↔R-3 동시 | :112-119 | ✅ |
| P2 **21:57 「오늘 3시」 합성** | 부분 — 구성 요소(R-3 예시·R-2 경계·「정확한 일시 특정」)는 각각 단언되나 **순서 적용 문면 자체는 미단언** | ⚠ **W2** |
| P2 되묻기 무남용 | :155-167 (`never for R-4`) + `test_a_normal_turn_is_still_audited:359-377` | ✅ |
| P2 금지 구절 부재 | :66-88 | ✅ |
| P2 산출 3분기 배타성 | :170-183 (도구>되묻기>final · 빈 문자열 흡수) + provider 파싱 :186-195 | ✅ |

**빠진 분기 없음** — 3분기(질문/예/아니)가 전부 런타임 테스트로 서 있고, 되묻기가 아닌 턴이 여전히
감사를 탄다는 **짝 테스트**까지 있다(스코프를 넓히지 않았음을 반증). 신규 테스트가 실배선 순서
(`claim_job` → `process`, :229-243)를 밟아 선재 함정을 피한 것도 확인.

### ⑥ allowed_paths · 무관 실패 분리 — **PASS**

- **diff 가 `back/`·`mcp/` 만이다**: `git status --porcelain` 의 11개 경로 중 그 밖 **0**. migration 0 · FE 0 · `context/` 0 · docker-compose 0. WP §Code Surface 표 안으로 한정된다.
- spec 레포(`mediness-mediness/reservation-update-mcp-spec`)에도 변경이 있으나 **이 워커의 산출이 아니다**(planner 계열 — 30-work.md·log.md·spec 2종). backend 워커는 브리프상 spec 레포 수정 금지였고 실제로 손대지 않았다.
- **pre-existing 14건 주장의 근거**: 리포트에 ⓐ 대조 방법(`git stash` 로 HEAD 대조 — 「내 변경 전후 실패 목록이 완전히 같다」) ⓑ 건수 분해(`test_chat_audit.py` 12 + `test_fe_contract_fixes.py` 2) ⓒ 공통 원인(`AttemptOwnershipLost` — `claim_job` 없이 pending 전표로 `process()` 호출, `absorb_followers` 의 running+attempts 소유권 검사)까지 **적혀 있다.** 원인 서술이 실제 코드 배선과 정합하고, 신규 테스트가 그 함정을 피한 방식(:229-243)이 같은 진단을 뒷받침한다. ⚠ 다만 **원문 출력은 리포트에 첨부되지 않았다** — 재현 확인은 코디의 독립 실행분(52+46 passed)에 의존한다. 브리프상 테스트 실행 금지라 본 검수에서 재실행하지 않았다.

## 경미 (WARN)

- **W1** `back/app/services/action_runtime/chat/service.py:686-704` — **감사 면제 채널이 «모델이 고르는» 축으로 바뀌었다.** 기존 정형 응답(파편 되묻기)은 `service.py:576` 에서 **코드가 LLM 없이** 만드는 것이라 모델이 그 축을 선택할 수 없었다. 신설 `clarification` 은 **모델이 라벨을 붙이면** 그대로 L2 감사를 건너뛴다 — R-2 한정은 프롬프트 문장(`Use clarification ONLY for R-2`, provider.py:62) 하나뿐이고 런타임 강제가 없다.
  - 근거: SPEC-151 §7.10 「되묻기 턴의 계약」 + WP-128 §P2-C(「되묻기를 정형 응답 축으로 내보내 감사 스코프 밖에 두기」를 **허용 수단으로 명시**). ⇒ **계약이 고른 선택지 안이므로 위반이 아니다.** 다만 §7.10 이 면제한 것은 「완전히 지난 명시 시각의 되묻기」이지 「모델이 되묻기라 부른 모든 답변」이 아니다.
  - 권장(코디 판단): 배포 후 확인 축에 **되묻기 오발동 빈도**(WP §배포 후 확인 축에 이미 있다)를 그대로 싣고, 잦으면 그때 런타임 조건(해석된 창이 종료까지 지났는가)을 붙일지 판단.
- **W2** `back/app/services/action_runtime/chat/provider.py:33` / `back/tests/services/engine_v2/test_time_resolution_askback.py:63-119` — **합성 순서 문면이 미단언이다.** 규칙 첫 줄 `Time resolution (apply in this order; …)` 가 21:57 「오늘 3시」 합성(R-3→R-1→R-2)을 성립시키는 유일한 문장인데, 이 구절을 무는 단언이 없다. R-1·R-2·R-3·R-4 와 「정확한 일시 특정」은 각각 단언돼 있어 회귀 위험은 낮지만, 순서 구절만 사라져도 붉어지지 않는다.
  - 근거: SPEC-151 §7.10 「세 규칙은 «합성» 되며… 새 규칙이 아니라 위 셋의 순서 적용이다」 · WP-128 §P2 검증 「⚠ 명시 날짜 + 모호 시각이 «둘 다 지난» 조합」.
  - 권장: `assert "apply in this order" in rule` 한 줄.
- **W3** `back/app/services/action_runtime/chat/provider.py:41-44` — **R-3 산문이 예시에 기대는 자리 1곳.** 「날짜가 주어졌고 오전/오후 **둘 다 그 날짜 안에** 있을 때」의 선택 기준이 산문에 없다(`pick am or pm INSIDE the given date` 까지만). 보존한 예시 `at 21:57 "10시반" today means 22:30` 이 정확히 그 조합이라 **예시가 규칙을 대신하고 있다.**
  - 근거: WP-128 §P2-A 가 「기존 예시 2개는 그대로 쓸 수 있다」를 **명시 승인**했으므로 위반이 아니다. 기장만 한다 — 나중에 예시를 줄이면 그 조합이 답을 잃는다.
- **W4** (범위 밖 · 잔여) SPEC-060 `products/mediness/20-spec/spec-060-mcp-surface.md:185` — **인벤토리 3자 일치 미완.** 코드 실측은 62(read 40 + write 22)인데 SPEC-060 표에는 **⏳ 예고 ④ 가 그대로 있고 행이 없다.** WP-128 §P1-D·§P3(「예고가 행이 되면 예고에서 지운다」·「3자 일치」)의 미충족분이다.
  - 근거: WP-128 §P1-D · §P3 검증. ⚠ **이 워커의 결함이 아니다** — 브리프가 spec 레포 수정을 금지했고 실제로 손대지 않았다. **planner 축에 남은 일**로 코디가 배분할 자리다.
- **W5** `mcp/tests/test_reservation_update_request.py:252-260` — **익명 `service:*` 거부가 행동이 아니라 seam 문자열로 고정됐다**(`inspect.getsource(...)` 에 `_wrap_write_tool` 이 있는지). 익명 토큰이 back 호출 **전에** 거부되는 것을 직접 돌려 보지 않는다.
  - 근거: WP-128 §P1 검증 「익명 거부 — `service:*` 는 back 호출 전에 거부된다」. ⚠ 다만 `test_reservation_cancel_request.py:191-199` 와 **바이트 동일한 표본 패턴**이라 「표본을 따르는 것이 이 phase 의 일」(WP §P1 설명)에는 부합한다 — **표본 자체의 한계**이지 이번 diff 가 만든 편차가 아니다. 고칠 자리는 write 툴 공통 축이지 이 파일이 아니다.

## 기존 부채 (이번 판정 제외)

- `mcp/app/server.py` 파일 말미 import 로 인한 **ruff E402 8건** — HEAD 에 선재. 이번 diff 가 늘리지도 줄이지도 않았다.
- `test_chat_audit.py` 12 + `test_fe_contract_fixes.py` 2 = **14건 실패** — `AttemptOwnershipLost`(테스트가 `claim_job` 없이 pending 전표로 `process()` 호출). HEAD 동일, 이번 변경과 무관.
- SPEC-060 인벤토리 표의 **선재 드리프트**(표 머리 read 39 + write 18 = 57 ↔ 실측 62). WP-128 §Open Issues 가 「소급 정정하지 않는다·정정 주체는 별건」으로 기장했다.
- 선재 부채 2건(변경·취소 접수의 **소유 판정 부재** · **재요청 멱등 가드 부재**) — 이번 등재가 **늘리지도 줄이지도 않는다**. 툴 docstring(:53-55)이 그 사실을 인계 문구로 남겼다. WP §Open Issues 가 「2026-08-11 부터 참조만 순환한다」로 기장 중.

## 확인한 것 (PASS 근거) — 체크리스트별 한 줄

- **계층/자리 규칙**: `mcp/` 는 툴 함수 ⟂ 등록부 분리 유지 · `back/` 변경은 프롬프트 상수(provider)와 턴 조립(service) 두 자리뿐 — 라우터·리포지토리·모델 무변경. ✅
- **재사용**: `runtime_common.raise_for_error`·`require_uuid` 재사용, 신설 헬퍼 0 · `_finalize` 기존 출구 재사용, 새 출구 0 · 카드 본문을 `review_surface.facts`/`diff`/`preview` 로 읽어 **재조립 0**(상태 이중화 금지). ✅
- **스키마 경계**: 툴 출력이 `{content, structured}` 2필드 공통 shape 유지, 새 shape 발명 0. ✅
- **마이그레이션**: `models/` 변경 0 ⇒ alembic 리비전 불요. ✅
- **테스트 존재·의미**: 신규 툴 14케이스 + 시각 해석/되묻기 14케이스. 프롬프트 계약 축(문면)과 런타임 축(실물 Action) **둘 다** 덮었다. ✅
- **diff 범위**: WP §Code Surface 표 안 · allowed_paths 이탈 0. ✅
- **확인 안 한 것(숨기지 않음)**: ⓐ 테스트 **실행 0**(브리프가 read-only·실행 금지로 지정 — green 은 코디 독립 확인분 52+46 passed 에 의존) ⓑ 모델이 실제로 R-1~R-4 를 따르는지(프롬프트 계약 테스트의 원리적 한계 — 워커도 리포트 §미결 3 에 명시) ⓒ Pre-deploy 3건(THE CONNECT 과거 시작 dev smoke · 실사용 1건 · 되묻기 실사용 1건 — 배포 축, 미수행).
