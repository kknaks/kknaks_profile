# 리뷰 리포트 — strong-hajin-calendar / Phase BE-2 코드 검수 (2026-09-21)

## 판정: **PASS**

**D1 세 자리가 각각 명시적으로 걸렸고, 셋 다 「날짜가 실제로 바뀌었을 때만」 돈다.**
`touch()` 에 걸지 않았고, 닫기와 업무 수정이 **같은 session = 같은 transaction** 안에 있다.

**사유는 둘뿐이다.** 셋째 문자열이 코드 어디에도 없고, 한쪽만 지운 경우가 `out_of_range` 로 간다.

**상태 아홉 경로에 아무것도 더하지 않았다** — `platform/` 무변경이고 그 아홉 함수가 diff 에 **0건**이다.
합의 취소는 `{0, null}` 을 내고 **배정을 닫지 않는다.**

**공유 `TaskMutationResult` 를 안 건드린 판단은 옳다** — 근거까지 확인했다.

**그리고 코디가 짚은 ⑥ — 「시작 전이 `released_count=0`」 테스트는 빈 단언이 아니다.**
**진짜로 뒤집힌 기간을 만들고**(`start_date > due_date` 를 단언) **그 안에 살아 있는 배정을 세워 둔 뒤**
0 을 확인하고 **그 배정이 살아남는 것**까지 본다.

WARN 둘은 **구현 중에 닫아도 되는 것**이고 계약이 갈리는 자리가 아니다.

---

## 검수 범위

BE-1 커밋 `1c15d02` **위의 uncommitted diff** — 수정 8 · 신규 1, 226 insertions.
**테스트는 돌리지 않았다**(지시). **코드도 한 줄 고치지 않았다.**
코디가 확인한 것(allowed_paths · `make test-unit` 356/0 · 대장 112 불변 + added 44→47 ·
`acceptance_evidence` 106 보존)은 다시 세지 않고 **필요한 자리만 교차 확인**했다.

---

## ① D1 세 자리 — **각각 걸렸고, 날짜가 바뀐 때만 돈다**

세 자리 모두 **같은 모양**이다: 날짜를 쓰기 **전에** `dates_before` 를 잡고, 쓴 **뒤에** 부른다.

| 자리 | 날짜 스냅샷 | 호출 | 확인 |
|---|---|---|---|
| ① `update` | `application.py:562` | `:565` | `validate_schedule` 통과 뒤 · `task.version += 1` **앞** |
| ② `transition` | `:1659` | `:1674` | `task.start_date = transition.task.start_date` **직전**에 잡는다 |
| ③ `_apply_proposal` | `:1913` | `:1926` | `if not changed: raise` **뒤** — 적용할 것이 없으면 닫지도 않는다 |

**「날짜가 실제로 바뀌었을 때만」** — `_schedule_release_for`(`:610-619`)의 첫 줄이
`:617` `if (task.start_date, task.due_date) == before:` → `:618` `return _NO_SCHEDULE_RELEASE`.
**저장소를 건드리지 않고** 0 을 낸다. 계약 테스트 `test_task_schedule_release.py:158`
(제목만 바꿈 → `NOTHING`, 배정 그대로)가 그것을 박는다.

**`touch()` 에 걸지 않았다** — `_release_schedules_outside`(`:586`)를 부르는 곳은
`_schedule_release_for` 하나뿐이고, 그것을 부르는 곳은 **위 세 자리뿐**이다(`grep` 3건).
`repository.touch()` 는 diff 에 없다.

**검증과 저장이 한 transaction 인가 — 그렇다.**
`_release_schedules_outside` 는 `self._schedule_repository()` 를 쓰고, 그 저장소는
BE-1 이 `bootstrap/application.py` `_tasks(session)` 에서 **그 session 으로** 조립해 넣은 것이다.
`update_task`·`transition_task`·제안 응답은 각각 `with self._session_factory() as session: … session.commit()`
**하나**에 담긴다. 즉 **닫기와 날짜 쓰기가 같은 session 에서 같은 commit 을 탄다** —
「배정은 닫혔는데 업무 날짜는 안 바뀐」 상태가 남을 자리가 없다.

---

## ② 사유 — **둘뿐이다. 셋째를 만들지 않았다**

- 사유 문자열은 `modules/work/schedule.py:25-26` 의 **둘**뿐이고, 고르는 자리도
  `:74` `return RELEASE_TASK_DATES_CLEARED if span is None else RELEASE_OUT_OF_RANGE` **하나**다.
- `application.py:596` 이 `release_reason_for(span)` 를 받아 그대로 넘긴다 —
  **문자열을 직접 짓는 자리가 없다.**
- `grep released_reason backend/src/` 가 내는 쓰기 자리는 `platform/task_schedules.py:106` 하나뿐.

**한쪽만 지운 경우가 `out_of_range` 로 가는가 (K7·K11)** — 간다.
`task_span` 이 한쪽만 있으면 **`None` 이 아닌 하루 구간**을 내므로 `release_reason_for` 가
`out_of_range` 를 고른다. 테스트 `:144` 가 실물로 박는다 — 3/1·3/5 두 칸에서 시작일만 지우면
**`{released_count: 1, reason: out_of_range}`** 이고 3/5 가 남는다. **셋째 사유가 안 생긴다.**
둘 다 지우면 `:131` 이 `{2, task_dates_cleared}` 를 단언한다.

---

## ③ K3 를 싣는 표면 셋 / 안 싣는 넷 — **옳다.** 공유 타입 판단도 **맞다**

### 싣는 셋 · 안 싣는 넷

| 표면 | `schedule_release` | 근거 |
|---|---|---|
| `PATCH /api/tasks/{task_id}` | **낸다** (`TaskDateMutationResult`) | D1 ① |
| `POST /api/tasks/{task_id}/start` | **낸다** (`http.py:2496`) | D1 ② — **`OPEN→IN_PROGRESS` 만 시작일을 채운다** |
| `POST .../proposals/{pid}/respond` | **낸다** — 동의 `:1843` · 거절 `:1843` · 재전송 영수증 `:1828` | D1 ③ |
| `block` · `resume` · `complete` · `cancel` | **안 낸다** (`TaskMutationResult` 주석 유지) | 날짜를 안 바꾼다 |

**넷이 정말로 날짜를 안 바꾸는지 확인했다** — `lifecycle.py` 의 시작일 채우기는
`task.state is OPEN and target is IN_PROGRESS and start_date is None` 일 때만 돈다.
`resume` 은 `BLOCKED`/`DONE` 에서 오므로 `OPEN` 이 아니고, `block`·`complete`·`cancel` 은 날짜를 안 쓴다.
**그래서 넷은 구조적으로 `{0, null}` 이고, 안 싣는 것이 맞다.** 테스트 `:219` 가
「날짜를 안 옮기는 전이는 옛 응답 모양 그대로」를 박아 이 넷을 고정한다.

### 공유 타입을 안 건드린 판단 — **맞다. 근거를 확인했다**

`task_results.py` 를 열어 보니 **`TaskMutationResult` 를 상속하는 것이 넷**이다:
`TaskDateMutationResult(:100)` · **`TaskListEntry(:193)`** · **`TaskDetailResult(:229)`** ·
`TaskCompletionResult(:324)`.

즉 공유 타입에 `schedule_release` 를 넣었다면 **목록·상세·완료 투영까지 전부** 그 칸을 갖게 되고,
그 투영을 내는 MCP **읽기** 도구(`task_list`·`task_get`·`my_task_list`)의 `output_schema` 가 같이 변한다.
**워커 리포트의 서술이 그대로 사실이다** — 「목록 한 줄이 「배정을 닫았다」를 광고할 이유가 없다」.

새 타입은 그 셋의 **형제**라 읽기 표면에 안 번진다. 실측으로도 확인된다:

- 대장 diff 의 `http_signature` 변경은 **정확히 셋**뿐이다 — `/api/meetings`(from/to) ·
  `PATCH /api/tasks/{task_id}` · `POST .../start`. **`block`·`resume`·`complete`·`cancel` 은 안 바뀌었다.**
- **`tool_count` 129 불변이고 도구 행의 스키마 변경이 0건**이다(대장 diff 에 `tools` 쪽 줄이 없다).
- `http_count` 156→159, `http` 배열 112 불변, `added_operations` 44→47 — **112+47=159** 로 맞는다.
- 새 셋에 `status: excluded` · `policy: E2` · `exclusion.reason` · `reconsider_when` ·
  `target_tools: []` 가 다 있다.

---

## ④ K16 — **두 문이 섰고, 구성원·팀장 둘 다 여전히 통과한다**

- `calendar_tasks` 앞 **`self._require(principal, TASK_READ)`**(`application.py:729`) —
  같은 파일의 다른 읽기 여덟 자리와 같은 문이다.
- `_assignable_task` 앞 **`self._require(principal, TASK_SELF_MANAGE)`**(`:642`) —
  `create_self`(`:258`)·`update`(`:507`)·`transition`(`:1614`)과 같은 문이다.
  생성·시각 변경·영수증 셋이 전부 이 함수를 지난다.

**테스트가 양쪽으로 있다** — 이것이 중요하다.

- **양성** `:356` — `MINA`(구성원)·`JIHO`(팀장) **둘 다** 배정 생성 `201` 과 합본 조회 `200` 을 받는다.
  **기존 동작이 안 바뀌었다**는 회귀다.
- **음성** `:374` — `Principal` 에서 역량을 **하나씩 빼서** 직접 부르면
  `calendar` 도 `create_task_schedule` 도 **`TaskAccessDenied`** 다.
  **문이 실제로 문다**는 증명이라 「추가했지만 아무것도 안 막는」 자리가 아니다.

K5 와 부딪치지 않는다 — 판정은 여전히 `repository.task()` 의 활성 담당 관계이고
역량은 **그 앞의 문**이다. 4차 검수가 WARN 으로 넘긴 자리가 그대로 닫혔다.

---

## ⑤ 상태 아홉 경로 — **아무것도 안 더했다. 쓰기가 끼어들지 않았다**

- **`backend/src/ax_workspace/platform/` 에 변경 파일이 0건**이다 — 영속 계층의 셋
  (`close_request_task`·`decide`·`cancel`)은 손대지 않았다.
- diff 전체에서 `submit_completion` · `accept_delivery` · `request_delivery_changes` ·
  `def reopen` · `close_request_task` · `def decide` · `def cancel` 이 **각각 0건**이다.
- `transition` 이 `DONE`·`CANCELLED` 로 갈 때는 날짜가 안 바뀌므로 `_schedule_release_for` 가
  **저장소를 건드리지 않고** 0 을 낸다 — 종료가 배정을 닫지 않는다.
- **합의 취소**는 `_apply_proposal` 의 `cancellation` 갈래(`:1910`)가
  `return _NO_SCHEDULE_RELEASE` 로 **닫지 않고** 빠진다. 주석이 이유를 적는다 —
  「업무 종료는 쓰기가 아니다(§B) — 합본 조회가 상태로 거른다」.

**업무 종료는 읽기 필터 그대로다.**

---

## ⑥ 조용히 통과하는 자리 — **찾지 못했다.** 특히 시작 전이 테스트는 빈 단언이 아니다

`test_task_schedule_release.py:174` 를 본문까지 읽었다. **0 이 나올 수밖에 없는 상황을 세워 놓고
0 을 확인하는 것이 아니다** — 닫힐 수 있었던 상황을 실제로 만든다.

1. 마감이 **3일 지난** 업무를 만든다(`due_date` 만 있음).
2. **그 지난 날짜에 살아 있는 배정을 실제로 만든다** — `assert kept.status_code == 201`.
   **닫을 것이 존재한다.**
3. 진짜 `POST /api/tasks/{task_id}/start` 를 태운다.
4. `assert body["schedule_release"] == NOTHING`
5. **`assert body["start_date"] > body["due_date"]`** — **기간이 정말로 뒤집혔음을 단언한다.**
6. `assert _slots(...) == [overdue]` — **그 배정이 살아남았음**을 합본 조회로 확인한다.

즉 **뒤집힘이 일어났다는 증거**와 **그럼에도 0 이라는 결론**을 같이 박는다.
docstring 의 구조적 이유(「`[min,max]` 로 읽혀 원래 구간을 포함하는 쪽으로만 넓어진다」)도 정확하다.
`:204` 가 「시작일이 이미 있으면 날짜가 아예 안 바뀐다」는 다른 갈래를 따로 덮는다.

그 밖:

- **빈 단언·`pass`·`skip`·`xfail`·`except Exception` 이 신규 코드·테스트에 0건**이다.
- 닫기 테스트들이 **건수와 사유를 정확히** 단언하고(`{1, out_of_range}` / `{2, task_dates_cleared}`)
  **남은 배정 목록까지** 확인한다 — 「닫혔다」만 보고 지나가지 않는다.
- 제안 테스트(`:270`)는 민아→지호 요청·수락·제안·동의까지 **두 사람의 실제 흐름**을 태운다.
- **기존 테스트가 하나도 약화되지 않았다** — 수정된 테스트 파일은
  `test_local_stack_targets.py` 하나이고 내용은 **단언 두 줄 추가**다(삭제·완화 0).
- local-stack 표지가 **표지와 grep 패턴을 함께** 고쳤고, 테스트가 그 둘을 **각각** 단언한다
  (`to_regclass('task_schedules')` + `task_checklist_items|task_schedules|meeting_transcripts`).
  한쪽만 고쳐 영원히 거절되는 자리를 막았다.

---

## WARN — 구현 중에 닫아도 되는 것

### WARN-1 → **FE Phase 브리프** (낮음)

**제안 재전송 영수증이 `{0, null}` 을 낸다** — `application.py:1828`.
원래 동의에서 닫힌 건수를 **다시 알려 주지 않는다.** 「두 번째 effect 가 없으므로 0」이라는
판단은 합리적이고 **SPEC 이 이 경우를 정의하지 않았다.** 다만 화면이 **영수증 응답으로 알림을
만들면 「N건 해제」를 놓친다.**

**브리프에 실을 한 줄**: 「`schedule_release` 로 알림을 만드는 것은 **첫 응답**이다.
재전송 영수증은 `{0, null}` 이므로 그것으로 알림을 다시 그리지 않는다.」

### WARN-2 → **BE 후속(또는 WP Open Issues)** (낮음)

**`transition()` 은 언제나 `released` 를 계산하는데, 네 라우트의 주석이 `TaskMutationResult` 라
FastAPI 가 그 칸을 걷어낸다.** 지금은 그 넷이 날짜를 안 바꾸므로 **버려지는 값이 늘 0** 이라 맞다.
그러나 **나중에 날짜를 바꾸는 전이 라우트가 생기면 건수가 조용히 사라진다** — 응답 모양이
주석으로만 갈리기 때문이다.

지금 그것을 막는 것은 테스트 `:219` 하나뿐이고, 그 테스트는 **현재의 넷**을 고정할 뿐 새 라우트를 막지 않는다.

**브리프에 실을 한 줄**: 「날짜를 바꾸는 전이를 새로 열면 그 라우트의 반환 주석을
**`TaskDateMutationResult` 로 바꿔야 한다** — 안 바꾸면 `schedule_release` 가 조용히 버려진다.」

---

## 확인한 것 (근거)

- **①** 세 자리의 스냅샷·호출 줄을 각각 짚고(`:562/565` · `:1659/1674` · `:1913/1926`),
  `_schedule_release_for` 의 조기 반환(`:617-618`)과 호출자 3건을 `grep` 으로 셌다.
  transaction 은 `_tasks(session)` 조립과 `WorkflowApplication` 의 session 단위로 확인했다.
- **②** 사유 상수 둘과 선택 지점 하나(`schedule.py:74`)를 확인하고, 쓰기 자리가
  `task_schedules.py:106` 하나뿐임을 `grep` 으로 셌다. K7 경로는 테스트 `:144` 로 확인.
- **③** 라우트 넷의 주석을 각각 확인하고, `lifecycle` 의 시작일 채우기 조건으로 **넷이 날짜를
  안 바꾸는 것**을 논증했다. 공유 타입 판단은 `task_results.py` 의 **상속 넷**을 열어 확인했고,
  대장에서 `http_signature` 변경 셋 · 도구 스키마 변경 0 · 112+47=159 를 실측했다.
- **④** 두 `_require` 줄을 짚고, 양성(`:356` 구성원·팀장)·음성(`:374` 역량 제거 시 거절) 테스트를 읽었다.
- **⑤** `platform/` 무변경과 아홉 경로 함수 diff 0건을 `grep` 으로 셌다. 합의 취소 갈래(`:1910`)를 읽었다.
- **⑥** 시작 전이 테스트(`:174-201`)를 **본문 전부** 읽어 빈 단언이 아님을 확인했다.
  신규 코드·테스트의 조용한 통과 패턴을 `grep` 으로 훑었고, 기존 테스트 약화 0건을 확인했다.
- **테스트를 돌리지 않았다. 코드를 한 줄도 고치지 않았다.** 산출물은 이 리포트 하나.

---

## `git -C /Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-calendar status --short`

```text
 M Makefile
 M backend/src/ax_workspace/bootstrap/application.py
 M backend/src/ax_workspace/entrypoints/http.py
 M backend/src/ax_workspace/modules/work/application.py
 M backend/src/ax_workspace/modules/work/task_results.py
 M backend/tests/architecture/test_local_stack_targets.py
 M docs/domain-model.md
 M docs/unified-operations-inventory.json
?? backend/tests/contract/test_task_schedule_release.py
```

(검수 시작 시점과 **같다** — 읽기만 했다.)
