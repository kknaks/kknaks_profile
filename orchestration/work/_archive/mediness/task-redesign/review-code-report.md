# 리뷰 리포트 — task-redesign / reviewer_code (WP-125 코드 검수, BE+MCP+FE 전량) — 2026-08-31

## 판정: **WARN** (차단 0 · FAIL 0 · WARN 7)

계약(결정 SoT · `domains/runtime_task.md` · WP-125 Phase 명세)은 **전 항목 착지**했다.
아래 WARN 7건은 전부 «진행 가능» 등급이고, 그중 **W1·W3 두 건은 코디네이터의 조치가 필요**하다
(W1 = 사용자 확인 대상, W3 = 문서 레포 정정 — 둘 다 워커 allowed_paths 밖이다).

## 검수 범위

- diff: `origin/dev`..worktree(미커밋 · staged 포함) — **117 파일**
  - BE `back/` 81 · MCP 7 · FE `front/` 36 (`git diff --stat` 기준 114 + untracked 3)
  - untracked 3건 전량 검수: `back/alembic/versions/0135_task_status_five_value_cutover.py` ·
    `back/app/services/action_runtime/workflow/round_eval.py` ·
    `back/tests/migrations/test_0135_task_status_five_value.py`
- 실행한 검사 (전부 read-only — 코드 수정 0 · 테스트 실행 0, 브리프 지시대로)
  - `git diff origin/dev` 전문 정독 (핵심 26 파일) + `git show origin/dev:<path>` 로 이관 전후 대조
  - 어휘 grep 0 확인: `accept_pending` · `accepted_at` · `decline`(전 형태) · `수락 대기` ·
    `canDecline` · `declined` — back/·mcp/·front/ 전역
  - 계약 대조: WP-125 Phase 0~9 작업·검증 항목 전수 · `runtime_task.md` §Enum/§State Machine/
    §착수/§합성 전이/§재배정/§스탬프/§TaskEvent/§Invariant/§마이그레이션 · `_RESUME.md` §2 결정 18행
  - 호출 사슬 추적: 완료 표면 4개 → seam · 합성 전이 3경로 → 공유 헬퍼 · slack 완료 경로 수렴

---

## 위반 (FAIL 사유)

**없음.**

---

## 경미 (WARN)

### W1. 「재배정 요청 자격 = 담당자 본인」이 **워크플로 계열 웹 표면에는 열리지 않았다**

- `back/app/services/action_runtime/tasks/manual_surface.py:523-527`
  ```python
  "canReassignTask": (
      can_edit and not is_workflow_task_type(task.task_type)
      and task.status not in TERMINAL_STATUSES
  ),
  ```
  이 세 줄은 **`origin/dev` 와 byte 동형**이다 — WP-125 P2 「재배정 요청 자격에 **담당자 본인** 포함
  (Policy 층)」에 대응하는 코드 변경이 없다. 갱신된 것은 같은 함수의 docstring(:486-487)뿐이다.
- 결과: `decision.*`·`incident.*` 태스크의 담당자는
  ① decline endpoint 3곳이 사라졌고(정상) ② `canReassignTask=false` 라 상세 `[⋯]` 에 「재배정 요청」이
  뜨지 않으며 ③ run 하위 재배정은 **대응 총괄/admin 전용**이다
  (`back/app/services/action_runtime/workflow/incident/workflow.py:123` ·
  `back/app/services/action_runtime/workflow/decision/surface.py:582`).
  → 「내가 이 일을 못 한다」의 **웹 동선이 이 계열에서 비었다.**
- **완화(실재 확인)**: 채팅·MCP `ax_task.reassign` 은 `resolve_own_task`(**본인 담당 task 만**,
  task_type 제약 없음 — `back/app/services/action_runtime/workflow/task_draft/surface.py:140-156`)를
  타므로 **모든 계열에서 담당자 본인이 재배정 확인 카드를 낼 수 있다.** `→ blocked`(사유 필수)도
  전이표에 그대로 열려 있다.
- 근거: `domains/runtime_task.md` §재배정 「요청 자격 — **담당자 본인 포함.** 「내가 이 일을 못
  한다」는 옛 거절의 대체 통로다」 · WP-125 P2 마지막 작업 항목 · `_RESUME.md` §1 이월 검증 ①.
- 권장 수정: 계약이 「**요청** 자격 ⟂ **변경** 자격」을 갈라 놓았으므로(같은 표의 마지막 행), 웹에도
  열려면 `canReassignTask`(=변경 가능) 를 넓히는 것이 아니라 **별도 «요청» 축**이 필요하다.
  → 코디가 사용자에게 「워크플로 태스크의 웹 재배정 «요청» 동선을 이번 라운드에 낼지 / 채팅 통로로
  충분한지」를 확인하고, 낸다면 WP-125 재발주가 아니라 별건으로 세우는 편이 안전하다.

### W2. P0 실측이 수행되지 않았고 **배포 시점 `RAISE` 가드로 대체**됐다

- `back/alembic/versions/0135_task_status_five_value_cutover.py:97-123`(`_guard_orphan_accepted_at`)
  — `accepted_at IS NOT NULL` 인데 대응 `task_accepted` 이벤트가 없는 행이 1건이라도 있으면
  `TASK_ACCEPTED_AT_ORPHAN_ROWS` 로 upgrade 를 세운다.
- 브리프 §6-2 는 「이벤트 없이 스탬프만 있는 행이 존재하면 drop 을 **멈추고 §9 질문 채널로 보고**」
  였다. 워커가 prod·stage DB 에 닿지 못해 판정 시점을 **배포 시점으로 미룬 것**이고, 규율 자체는
  `0094` 선례(사전 `RAISE`)와 동형이라 **설계는 적정**하다.
- 남는 리스크: 실측 없이 배포하면 이 가드가 stage/prod upgrade 를 실패시키는 형태로 처음 발화한다.
  그때가 OI-6(「컬럼을 남기고 쓰기만 중단」 선택지)의 판단 시점이 된다.
- 권장 수정: WP §Pre-deploy 「stage 에서 upgrade→downgrade→upgrade 왕복 먼저」를 **실 데이터가 있는
  stage** 에서 태워, 가드가 세우는지 여부로 P0 실측을 회수한다. 세우면 사용자에게 OI-6 를 올린다.

### W3. SPEC-060 인벤토리 **3자 일치 미달** — WP 수치가 stale (문서 레포 정정 필요)

- `mcp/app/server.py:1817-1826` — `/health` **61 → 60**, 오염 등급 주석 `write 21 → 20`.
- WP-125 P5 는 「write **18→17** · `/health` **57→56**」로 적고 있다. 그 사이 `decision_register`
  영구 비활성(-1)과 WP-123 도서관 발행 툴(+1)이 들어와 **코드 실물이 61 이었다.**
  WP 가 스스로 「⚠ **먼저 내리지 않는다** — 그 표는 `/health` 실물의 거울이다」라고 못박았으므로
  **코드가 맞고 문서 수치가 틀렸다.**
- 등록 해제 자체는 정확히 착지: `mcp/app/tools/task_decline.py` 삭제 ·
  `mcp/app/server.py:76,322,1390` 의 import·요약·툴 정의 제거 · `test_tool_inventory.py` 갱신.
- 권장 수정: **코디**가 `spec-060-mcp-surface.md` §Tool 인벤토리 표 행 제거 + 머리 카운트·§5 AC 를
  **61→60 / write 21→20** 으로 내리고, WP-125 P5 의 「18→17 · 57→56」 두 수치를 같은 값으로 정정.
  (BE/FE 워커 allowed_paths 밖이라 워커 책임 아님.)

### W4. 알림 발송량 관측 축이 합쳐졌다 — Pre-deploy 점검을 요약으로 할 수 없다

- `back/app/services/version_wbs_scheduler.py:213-218` — `notified` 하나에
  「시작일 도래」와 「overdue」 발송 수가 **합산**된다.
- WP §Pre-deploy 는 「overdue Slack DM **발송량이 변하지 않는지** 확인 (P4 가 새 알림 종을 하나
  더한다)」를 요구한다. 지금 요약으로는 두 종을 가를 수 없어 그 확인이 불가능하다.
- 권장 수정: `notified_start_due` / `notified_overdue` 로 분리(`notified` 는 합으로 유지).

### W5. 주석이 코드와 어긋난다 — 3건 (문체가 아니라 **사실 오기**)

후속 독자가 그대로 믿으면 오판하는 자리들이다.

- `back/app/services/version_wbs_scheduler.py:73-75` — 「판정은 구 자동전환(`should_auto_start`)과
  **글자 그대로 같다** … **모수도** 술어도 바뀌지 않았다」.
  술어는 같지만 **모수는 좁아졌다**: 구 `auto_transition_tasks` 는 `VersionWbsTask` 전 행(phase 포함 ·
  버전 상태 무관 · origin 없는 행도 `axis.resolve` 폴백으로 포함)을 훑었고, 신
  `find_start_due_work_items`(`back/app/repositories/version_wbs_repo.py:420-435`)는
  `task_kind = work_item` ∧ `origin_task_id` 조인 필수 ∧ `ProductVersion.status IN 활성` 이다.
  **좁힌 것 자체는 WP P4 「수신자·활성 버전 한정·환경 게이트는 overdue 와 같은 축」 지시대로**라
  코드가 맞고 주석이 틀렸다.
- `back/app/models/meeting_v2.py:516` — 「**빈 문자열** = 대응 태스크를 못 찾은 신규 제안 행」.
  실제 미연결 행의 값은 `todo` 다(`back/app/services/meeting_v2_minutes_form.py:83`
  `_UNLINKED_ACTION_STATUS = RuntimeTaskStatus.TODO.value`, 소비처 :428·:645·:744).
  빈 문자열을 쓰는 경로가 코드에 없다.
- `back/app/services/action_runtime/tasks/machine.py:44` — 「합법 **9** · 불법 **16**, 대각선 제외」.
  5×5 − 대각선 5 = 20 이므로 불법은 **11** 이다(합법 9 는 정확 · 정본 표와 일치).
  ⚠ 같은 축의 문서 오기: **WP-125 P2 검증칸의 「합법 12·불법 13」** 도
  `domains/runtime_task.md` §State Machine 표(합법 9)와 어긋난다 — **문서 레포 정정 대상**.

### W6. `tasks_surface.patch_task` 의 **죽은 인자 4개**가 호출부에서 계속 넘어온다

- `back/app/services/action_runtime/workflow/tasks_surface.py:344-355` — `runner` ·
  `round_task_types` · `round_done_event` · `round_eval_statuses` 를 **받되 쓰지 않는다**(docstring 이
  「도메인 호출부 시그니처를 이 라운드에 함께 흔들지 않기 위한 잔여 슬롯」이라 명시).
- 호출부는 여전히 값을 싣는다: `back/app/services/action_runtime/workflow/incident/surface.py:167`
  (`round_task_types=C.PREVENTION_TASK_TYPES`) · `.../decision/surface.py:558` 계열.
- 의도된 유예라 이번 판정에 넣지 않지만, 남겨 두면 「넘기면 도는 줄」 아는 새 호출부가 생긴다.
- 권장 수정: WP-126(라운드 판정 1벌 수렴) 라운드에서 시그니처와 함께 제거.

### W7. import 순서 — isort 위반 가능

- `back/app/services/meeting_v2_minutes_form.py:66` — `from app.models.action_runtime import
  RuntimeTaskStatus` 가 `from app.models.meeting_v2 import (...)`(:52-65) **뒤**에 있다.
  알파벳 순서상 `action_runtime` < `meeting_v2`.
- ⚠ **실측 못 함** — 이 환경에 `ruff` 가 없다(`ruff`/`python3 -m ruff` 둘 다 미설치).
  CI 가 `ruff check --select I` 를 돈다면 이 한 줄이 걸린다. 코디가 `back` 가상환경에서 1회 확인 권장.

---

## 기존 부채 (이번 판정 제외)

- `back/app/services/version_wbs_status.py:154-156` — `write_checklist_status` 가 `origin is None` 인
  work_item 에서 `write_status` 를 부르고, 그 함수는 phase 가 아니면 `RuntimeError` 로 죽는다.
  `origin/dev` 에도 있던 경로이고 이번 diff 가 만들지 않았다.
- `back/app/services/action_runtime/tasks/lifecycle.py` 의 `apply_derived_transition`(체크리스트 파생)에
  자격 검사가 없다 — WP-125 OI-2 가 이미 기장한 기존 축이고, 이 라운드는 **범위를 넓히지 않았다**
  (round_eval 훅을 파생 경로에 걸지 **않은 것**이 그 실물 — `round_eval.py:20-25`).

---

## 확인한 것 (PASS 근거 — 체크리스트 항목별)

### 1. 결정 SoT 준수 — **전 항목 착지**

| 결정 | 착지 | 좌표 |
|---|:--:|---|
| 5값 enum, 두 축 **동시** cutover | ✅ | `alembic/versions/0135_…py:71-74,126-137` — `_AXES` 한 루프가 `runtime_task_status`·`version_wbs_task_status` 를 같은 migration 에서 재생성. 두 enum 이 다른 테이블·컬럼에 쓰이지 않음을 grep 으로 확인(`DROP TYPE …_old` 안전) |
| 기존 `accept_pending` 행 → `todo` (실패시키지 않음) | ✅ | 같은 파일 :127-129 (캐스트 **앞**) · 테스트 `test_0135…py:148-171` |
| `accepted_at` drop + **`RAISE` 가드** | ✅(W2) | :97-123, :137 · 모델 `models/action_runtime.py:656` |
| decline 축 **완전 제거** | ✅ | 기계(`machine.py` — `decline()`·`TaskDeclineReasonRequired` 소멸) · 표면 3(`manual_surface.decline_task`·`tasks_surface.decline_task`·`task_draft/surface.apply_decline`) · REST 4(`routers/action_runtime_v2.py` canonical·incident·decision·`/task-declines`) · 스키마 2 · 에러/문구 4 · 알림 1(`notify_task_declined`) · leaf/카탈로그(`AX_TASK_DECLINE`) · MCP 툴 1 · BFF 3 · FE CTA·배지·사유줄. **잔존 grep 0**(코드 기준 — 남은 hit 는 전부 주석·부정 단언 테스트) |
| 재배정 = `todo` 리셋 + `started_at` 클리어 | ✅ | `machine.py:180-183` |
| terminal 가드 유지(BUG-023) | ✅ | `machine.py:175-178` — **첫 쓰기 앞**, override 인자 없음 |
| 담당자 본인 재배정 요청 | ⚠ | **W1** (비워크플로 ✅ · 워크플로 웹 ✖ · 채팅/MCP ✅) |
| 생성 초기값 **전부 `todo`** | ✅ | 6 표면 전수 — incident fanout 2(`incident/definitions.py:105,317`) · incident 추적 카드(:141) · decision bootstrap(`decision/task_service.py:170`) · 수동(`manual_surface.py:197`) · run 하위(`tasks_surface.py:444`) · WBS(`version_wbs.py:1162`). `_INITIAL_STATUS = _TODO`(`version_wbs.py:615`) |
| 착수 = **명시 시작만** (자동전환 0 · 즉시 in_progress 0) | ✅ | 스케줄러 자동전환 삭제(`version_wbs_scheduler.py` — `auto_transition_tasks`·`lifecycle` import 소멸) · 즉시 in_progress 2곳이 **`todo` 생성 + 시스템 명시 전이**로(`incident/definitions.py:164-167` · `decision/task_service.py:93-104,180`) — `task_created` + `task_started` **2 이벤트** |
| 회의록 canonical 어휘 | ✅ | `meeting_v2_minutes_form.py:74-83` (`_ACTION_STATUSES` = RuntimeTaskStatus 5값 파생) · `models/meeting_v2.py:517` server_default 제거 · migration :140-141 (`open` → `todo` + DROP DEFAULT). **박제 성격 유지** — 연결 행은 스냅 시점 원장값, 미연결 행만 `todo` |
| P7 = **라우트 등록 해제(주석 비활성)까지만** | ✅ | `routers/decisions.py:139-150` — `@router.get` 데코레이터만 제거, 핸들러·서비스·스키마 존치. 레거시 행 삭제 0 |

### 2. invariant — **5건 전부 유지**

- **두 enum 값 동형** — 같은 migration + 테스트가 문자열 집합을 직접 단언
  (`test_0135…py:33,113-131` — `_EXPECTED_VOCAB` 를 모델에서 **파생시키지 않는** 리터럴).
- **`done`⟂`canceled` 재배정 불가** — `machine.py:175-178`, `reassign()` 첫 쓰기 앞 · FE 도 같은 축
  (`TaskHeaderActions.tsx:132-134` · `CanonicalTaskDetail.tsx:288`이 `isTerminalTaskStatus` 재사용).
- **삭제⟂취소 배제 앵커 무효화 없음** — 신규 `runtime_task_repo.list_active_tasks_in_run`
  (`:441-465`)이 `_scoped()` 와 **같은 2겹 술어**(`task_run_not_deleted()` + `active_task_predicate()`)를
  건다. 빠진 것은 tenant 술어 하나뿐이고 그 자리는 `run_id` 가 좁힌다(docstring 이 근거 명시).
- **`done` ⇒ 모든 체크 항목 done** — `complete_open_check_items` 가 seam 안쪽에 그대로.
  `complete_as_system` 이 손코딩에서 seam 위임으로 옮겨오며 이 규칙을 **더** 타게 됐다
  (`decision/task_service.py:106-119`).
- **과거 `task_accepted`·`task_declined` 행 보존** — migration 이 `task_events` 를 **읽기만** 한다
  (`:103-123` 의 `NOT EXISTS` 서브쿼리, DELETE 0). 소비 쪽도 원장을 존중:
  `runs_projection.py:296-306` 이 폐기 어휘의 **표시 순위를 남겨** 과거 타임라인이 미등재(50)로
  밀리지 않게 했고, `front/lib/incident.ts:512-521` 은 사전에서 빼되 「지어낸 문장으로 덮지 않는다」로
  `default` 폴백.

### 3. P8 seam — **완료 표면 4개 전부 같은 seam · 판정 규칙 미변경**

- 훅 위치: `lifecycle.apply_user_transition` 끝(`lifecycle.py:192-197`) → `round_eval.evaluate_after_transition`.
- 4 표면 전수 추적 ✅
  - incident PATCH `/{run}/tasks/{id}` → `incident/surface.patch_task` → `tasks_surface.patch_task:378`
    → `lifecycle.apply_user_transition` (**구 자리의 직접 호출은 삭제** — 중복 발화 0)
  - canonical `/tasks/{id}/transition` → `manual_surface.transition_task:875` → 같은 seam
  - `/task-completions` → `task_draft/surface.apply_complete` → `_chain` → `apply_transition_chain` → 같은 seam
  - MCP `task_done` → `/task-completions` (같은 문)
  - (+ WBS 칩도 `version_wbs._transition_linked_task` → `apply_transition_chain` 으로 같은 seam)
- **판정 규칙 미변경 확인** — `origin/dev:tasks_surface.round_complete`(전량 terminal) 과
  `round_eval._round_complete`(`:129-142`)가 술어 동형. 파라미터도 이관 전 값 그대로:
  decision `round_done`/`{done,canceled}`(`decision/const.py:195`) · incident `task_done`(구 기본값,
  `git show origin/dev:…tasks_surface.py:408` 대조)/`{done}`/`PREVENTION_TASK_TYPES`.
  **WP-126 소관(라운드 판정 1벌 수렴) 침범 0.**
- 파생 전이 제외 결정이 코드·문서 양쪽에 명시(`round_eval.py:20-25` · `lifecycle.py:194-196`) —
  OI-2 「파생이 닿는 범위를 넓히지 않는다」 준수.
- 관찰(위반 아님): `_round_complete` 는 판정 술어의 **4번째 구현**이다. docstring 이 그 사실과
  OI-3 소관을 명시하고 있어 이번 라운드의 규율 위반은 아니다 — WP-126 이 수렴할 자리.
- 관찰 2: `complete_as_system`(부트스트랩 강제완료)이 seam 을 타면서 **이제 round_eval 을 지난다**
  (구 형태는 안 지났다). 부트스트랩 `task_type` 은 판정 모수 밖이고 `notify_event` 가 현 스테이지
  `on_event` 를 지나므로 이미 넘어간 스테이지에서 연쇄가 서지 않는다 — 중복 발화 위험 낮음.

### 4. 합성 전이 통합 — **1곳 + 표면별 경로표 · 구 3중 구현 잔존 0**

- 공유 헬퍼: `lifecycle.apply_transition_chain`(`:216-262`) — 같은 `now` 전 사슬 · **낙관적 잠금은
  첫 걸음만**(`expected_updated_at if index == 0 else None`) · 걸음마다 기계 통과(표 우회 0) ·
  0걸음이면 `None`(멱등). `plan_transition_steps`(`:199-209`)가 「표에 없으면 한 걸음」.
- 경로표 3벌(정책만 표면이 소유):
  - `lifecycle.SYSTEM_SYNTHETIC_PATHS`(`:266-271`) — `todo→done` 만
  - `version_wbs._WBS_SYNTHETIC_PATHS`(`version_wbs.py:1348-1354`) — `todo→done` 만
    (`blocked→done` 은 **의도적으로 안 푼다** — 칩 한 번 = 한 의사표시)
  - `task_draft/surface._CHAT_SYNTHETIC_PATHS`(`:555-566`) — `todo→done` **+ `blocked→done`**
    (발화는 사실 선언이라 해제를 함의) → **자가보고 ② 「채팅 blocked→done 합성 보존」 확인 ✅**
    (구 `_advance_to_in_progress` 의 `blocked→in_progress→done` 과 행위 동형)
- 구 구현 3벌 **전부 삭제** 확인: `version_wbs._transition_steps` · `task_draft/surface._advance_to_in_progress` ·
  `task_draft/surface.apply_complete` 인라인 체인 · `decision/task_service.complete_as_system` 손코딩.

### 5. allowed_paths — **교차 침범 0**

- diff(미커밋 + staged + untracked) 전체가 `back/` · `mcp/` · `front/` 안에 있다.
  세 접두어 **밖 파일 0건** — 문서 레포·`docker-compose*.yml` 포함 미변경.
- ⚠ 한계 명시: 워크트리가 **미커밋 통합 상태**라 「BE 워커가 front/ 를 만졌나」의 워커별 귀속은
  diff 만으로 가를 수 없다. 확인한 것은 **합집합이 브리프 두 장의 allowed_paths 합집합 안**이라는 것.

### 6. BE↔FE 계약 정합 — **6항 전부 일치**

| 계약 | BE | FE |
|---|---|---|
| 5값 어휘 | `models/action_runtime.py:99-106` | `lib/tasks/canonical-task.ts:26-31` · `lib/wbs.ts:39`(canonical 별칭 — 값 재선언 0) |
| `allowed_transitions` 가 유일 전이 축 | `tasks/projection.py:292-300` — `LEGAL_TRANSITIONS` 를 그대로 읽어 **전이표 변경이 자동 전파**. `blocked→done` 이 새 표에 없어 응답에서 자동 소멸 → **이월 검증 ② 확인 ✅** | `TaskHeaderActions.tsx` 가 `task.allowed_transitions` 만 소비 |
| `declined`/`decline_reason`/`declined_at` 파생 제거 | `tasks_surface.project_tasks`(:76-152) — 인자·필드·`declined_by_task`·`standing_decline`·`_fold_standing_declines` 전부 삭제 · 소비처 5곳 제거 | `lib/incident.ts` `MyTask`·`IncidentTask` 필드 제거 · `mapMyTask.canDeclineTask` 제거 |
| decline BFF↔REST 짝 | REST 4문 제거 | BFF 3건 삭제(`app/api/ax/{decisions,incidents}/…/decline/route.ts` · `app/api/ax/tasks/…/decline/route.ts`) — **짝 정확** |
| 라벨 사전 1벌 | 채팅 라벨 `task_draft/const.py:233` (`todo` = **대기**) | `canonical-task.ts:48-84` **단일 사전 + `taskStatusChip`/`taskStatusLabel` 폴백 입구 1개**. 소비처 8 표면 전수 확인(칸반·상세 3·incident·decision·landing-chat·meeting-v2 2) — `lib/incident.TASK_STATUS_LABELS` 삭제. 「대기/예정/할 일」·「중단/차단/막힘」 혼재 해소 |
| `TRANSITION_LABEL` 새 edge | `TASK_UNBLOCKED` 신설(`tasks/const.py:15`) | `TaskHeaderActions.tsx:44-51` — `accept_pending->todo` 제거 · `blocked->done` 제거 · **`blocked->todo` = 「차단 해제」 신설** · `todo->blocked` 추가 → 합법 엣지(취소 제외) **전수**. 폴백 상태명 누수 0 |

- 칸반 **4열 · 순서 「대기·진행 중·완료·중단」** ✅ (`task-kanban.tsx:89-100` — 라벨을 적지 않고
  키만, 사전 이중화 0). SPEC-230 §U-7 랜딩 칩 `수락 대기`→`대기` ✅ (`WorkPanel.tsx:78-82` —
  문구를 적지 않고 `taskStatusLabel("todo")` 호출).
- MCP `wbs_common.STATUSES` 6→5 ✅ (`mcp/app/tools/wbs_common.py:41`).

### 7. 회귀 위험 — **전이표 축소로 죽는 호출부 0**

- `accept_pending` 을 값으로 참조하던 코드 경로 전수 제거 확인(위 grep). 남은 hit 는 주석과
  **부정 단언 테스트**(`__tests__/lib/wbs-status-options.test.ts:63-119` 등)뿐이다.
- `blocked → done` 을 기대하던 자리 2곳 모두 처리: FE `TRANSITION_LABEL` 삭제 · 채팅은 합성 2단 보존.
- **마이그레이션 왕복** — `downgrade()` 가 6값 복원 + `accepted_at` 재생성(NULL) + meeting default 복원.
  `test_0135…py:215-229` 가 upgrade→downgrade→upgrade **왕복을 실제로 태운다**.
  `_swap_enum` 이 `server_default` 를 먼저 떼고 캐스트 후 다시 붙여 0108 선례의 함정을 피한다.
- **WP-114 착지분 회귀 0** — 칸반 「완료 앞 · 중단 뒤」 사용자 결정 순서 유지(`task-kanban.tsx:91-99`
  주석 그대로) · `blocked_reason` 파생 축(`blocked_by_task`) 무손상 · WP-122 overdue 수신자 축소가
  `resolve_task_recipients` 로 이름만 바뀌고 술어 동일(`version_wbs_scheduler.py:151-168`).
- **0094 마이그레이션 테스트 회귀 없음** — `alembic_revision("0094_wbs_status_vocab", …)` 으로
  리비전 고정이라 그 시점의 6값 단언이 그대로 유효하다(`tests/migrations/test_0094…py:21`).
- **`/incidents/slack/complete` 폐쇄 + 실경로 수렴 확인 ✅** — 라우트·스키마 제거 후
  `back/app/routers/slack.py:415` 의 공용 `POST /api/v1/slack/interact`(서명 검증 있음)가
  `incident_surface.complete_from_slack` 을 그대로 부른다. 기능 소실 0.

### 8. 워커 자가보고 미결 5건 — **처리 적정성**

| # | 자가보고 | 판정 |
|---|---|---|
| ① | RAISE 가드로 P0 실측 대체 | **적정 · 조건부** — 설계는 0094 선례 동형. 다만 실측이 stage 왕복으로 회수돼야 한다 → **W2** |
| ② | 채팅 `blocked→done` 합성 보존 | **적정** — `_CHAT_SYNTHETIC_PATHS` 에 명시 선언, 구 행위와 동형. 「칩과 정책이 다른 것이 의도」를 두 자리 주석이 상호 참조 |
| ③ | 알림 ⑧ 결번 | **적정** — `decision/notify.py:82-85` 가 결번 사유를 남기고 새 종을 만들지 않았다. WP §Scope 제외(「알림 신설은 범위 밖」) 준수. ⑤ 재배정형이 새 담당자 통보를 이미 갖는다 |
| ④ | SPEC-060 수치 실측 차이 | **적정 · 후속 필요** — 코드 실물(61→60)을 따른 것이 WP 의 「먼저 내리지 않는다」 지시와 정확히 일치. 문서 정정만 남음 → **W3** |
| ⑤ | OI-4 미착수 | **적정** — OI-4 는 WP 본문에서 이미 「해소(2026-08-31) — 대상 없음」으로 닫힌 항목이다(`is_required` 는 0066 이 drop 완료 · `scope_slug` 는 살아 있는 계약). **착수할 것이 없는 것이 맞다.** 코드도 `scope_slug` 를 그대로 보존(`models/action_runtime.py:654`) |

---

## 실행하지 않은 것 (숨기지 않는다)

- **테스트 미실행** — 브리프가 read-only·no-test 를 명시. 테스트 파일은 **내용**으로만 검수했다
  (`test_0135…py` 6단언 · `test_task_machine.py:186-191` decline 소멸 단언 ·
  `test_tasks_surface.py:79` 파생 4필드 부재 단언 · `test_ax_task_immediate.py:468-476` 심볼 소멸).
- **린트 미실행** — 이 환경에 `ruff` 없음 → W7 은 육안 관찰이며 실측이 아니다.
- **워커별 파일 귀속 미검증** — 미커밋 통합 워크트리라 diff 로 가를 수 없다(§5 한계 명시).
