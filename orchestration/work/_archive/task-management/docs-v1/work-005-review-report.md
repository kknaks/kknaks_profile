# WORK-005 검수 리포트

- 검수 대상: **`46fe87a`**(BE Phase 1·2 + 리비전 `0003`) · **`ad2d4a5`**(FE Phase 3·4)
- 워크트리: `/Users/kknaks/orca/workspaces/task_management/docs-v1` · 작업 트리 clean(`git status --porcelain` 무출력)
- 판정 기준: DEC-002 · SPEC-004 · `40-architecture/{backend(§3 규칙 7·§7·§8-2·§10·§12), frontend(§1-2·§3-3·§5-2·§11), database/domains/task(T-4~T-11·T-8-a·T-8-b)}` · WORK-005
- 검수자는 **코드·문서를 하나도 고치지 않았고 테스트·빌드·마이그레이션을 돌리지 않았다.**

> **범위 산정 주의 — 브리프의 base 가 한 커밋 늦다.** 브리프는 「`c6ba429` 다음부터」라고 적었지만
> `46fe87a`(백엔드 Phase 1·2)는 **`c6ba429` 보다 앞**이라 `git diff c6ba429...HEAD` 로는 잡히지 않는다
> (`git log c6ba429..HEAD` 는 `ad2d4a5` 한 건뿐이다). 브리프가 `46fe87a` 를 **이름으로 지정**했으므로
> 그 커밋을 포함해 검수했다. 사이의 `c6ba429`(「첨부·연관 네 자리에 U-7 실패 표시」)는 **WORK-004 검수 후속**이라 제외했다.
> 다음 브리프에서는 base 를 `b46771d` 로 잡아야 범위가 명령과 일치한다.

---

## 판정 요약

| 층 | 판정 | 근거 |
|---|---|---|
| **정책**(DEC-002) | **PASS** | 완료 게이트가 「결과자료 ≥1 **또는** 완료 결과」로 **한 곳**에서 판정된다 · 전이 그래프에 `done→cancelled` 가 없다 · **취소는 상태**(유형 축에 없다, 제목 취소선) · 삭제는 소프트이고 복원 표면 0건 · 로그는 서비스만 쓰고 실행취소만 지운다 |
| **아키텍처** | **WARN** | 계층·`commit()` 부재·`except Exception` 0건·`persist_changes` 신규 0건·쿼리 alias 8개 전부 명시·§8-2 코드 3종 등록·리비전 `0003` 이 새 리비전 + `downgrade` 완비 — 전부 통과. 다만 **Tailwind 관용구 `current` 를 색 이름으로 덮어 shadcn 생성물의 `text-current` 의미가 바뀌었다**(W-1) |
| **SPEC**(SPEC-004) | **FAIL** | 게이트·전이·실행취소·집계·DnD 규칙이 계약대로다. 그러나 **기간 경계를 프론트가 서버와 다르게 보낸다 — 말일 기한 업무가 목록·칸반·집계에서 통째로 빠진다**(F-1). U-4 삽입 가이드선·U-2 취소일 등 규격 4건 누락(W-3~W-6) |
| **WP**(WORK-005) | **FAIL** | Phase 1·2 는 체크리스트를 넘어선다(정적 검사 4종 내가 직접 재현 확인). Phase 4 의 「리스트와 **같은 기간·필터**를 본다」가 깨졌다 — **칸반이 그 달의 앞 12건만 그린다**(F-2). Done Criteria 6항목 중 **캡처 3장·문서 갱신 2건 미충족** |

**게이트 단일화 축 — PASS(이 검수의 핵심 통과).** 내가 직접 grep 으로 넷을 재현했다:
`task.status` ORM 대입 **1곳**(`task_repository.py:311`) · `TaskCompletionBlockedError` 던지는 곳 **1곳**(`task_service.py:786`) ·
`task_log` DELETE **1곳**(`task_child_repository.py:208`, 호출은 `undo_last_status` 하나) ·
`PATCH /{id}/status` 를 부르는 곳 **1곳**(`api.ts:193`, 그 소비자는 `useTaskStatus.ts` 하나).
**일반 `PATCH` 로 상태를 보내면 422** 다 — `TaskUpdate` 에 `status` 필드가 없고 `extra="forbid"` 가 잡는다.

**낙관적 갱신 방향 — PASS.** WORK-004 와 정반대로 **어디서도 낙관적으로 옮기지 않는다.**
칸반은 놓은 뒤 `pendingId` 로 불투명도 0.6 을 유지하고, 실패해도 「되돌릴」 필요가 없다(애초에 안 옮겼다).
드롭 차단은 **전이 그래프만**이고 **완료 컬럼은 언제나 열려 있다** — 결과자료 유무를 화면이 미리 판단하지 않는다.
**같은 컬럼 재드롭은 요청 0건**이다(`useKanbanDnd.ts:110-112`, 테스트로 고정).

---

## FAIL — 반드시 고쳐야 하는 것

| # | 파일:줄 | 무엇이 어긋났나 | 어긋난 문서 절 | 어떻게 고치나 |
|---|---|---|---|---|
| **F-1** | `features/tasks/hooks/useTasksViewParams.ts:123-129` `monthRange()` ↔ `repository/task_repository.py:339-354` `_period_filter()` (소비 `TasksScreen.tsx:54`) | **프론트가 보내는 기간 경계가 서버 계약과 다르다 — 말일 기한 업무가 그 달 목록에서 사라진다.**<br>서버는 끝 경계를 **열어 둔다**(`due_date < to_date`, 주석에도 「끝 경계는 **열려 있다**」). 서버 자신의 기본값(`current_month_bounds()`)과 백엔드 테스트 헬퍼(`test_task_list.py:30-37`)는 그래서 `to` = **다음 달 1일**을 보낸다. 그런데 `monthRange` 는 `to` = **이번 달 마지막 날**(`Date.UTC(year, mon, 0)`)을 보낸다 → **8월 31일이 기한인 업무는 8월 목록·칸반·`total`·`typeCounts` 어디에도 없다.**<br>같은 함수에 둘이 더 있다 — ② **타임존이 없는 날짜 문자열**(`"2026-08-01"`)을 보내 서버가 naive `datetime` 으로 파싱하고 `.astimezone()` 이 **시스템 로컬**을 가정한다(G-2 「기간 조회는 **UTC 경계**로 보낸다」 위반, 컨테이너 TZ 에 따라 경계가 흔들린다) ③ **KST 달 경계가 아니라 UTC 달 경계**를 만들어, 기한 없는 업무의 `created_at` 축이 9시간 어긋난다 — 그 달 1일 00:00~09:00 KST 에 만든 무기한 업무가 빠진다(T-1-a).<br>**백엔드 테스트가 못 잡는다** — 테스트는 올바른 경계를 스스로 만들어 보내기 때문이다 | **SPEC-004 §4** 「쿼리: `from`·`to`(**달 경계**, UTC)」 · **§4 Data Contract** 「기간 조회는 **UTC 경계**로 보낸다(G-2)」 · **T-1-a**(기한 없는 업무는 생성일 기준 달) · **§6 Acceptance 14**(필터 결과 카운트) · **WP §Internal Interface Contract** 목록 쿼리 행 | `monthRange` 를 **서버의 `current_month_bounds()` 와 같은 규칙**으로 고친다 — ① 끝을 **다음 달 1일**(배타)로 ② **KST 달 경계**를 만들고 ③ **UTC ISO(오프셋 포함)** 문자열로 보낸다. 기준 구현이 `task_service.py:current_month_bounds()` 와 `test_task_list.py:_month_bounds()` 에 이미 있으니 그대로 옮기면 된다.<br>**재현**: 이번 달 **마지막 날**을 기한으로 업무를 하나 만들고 `/tasks` 를 연다 → 목록·칸반에 없고 하단 카운트에도 안 잡힌다. 기한을 하루 당기면 나타난다.<br>**함께**: 프론트 통합 테스트가 이 축에 하나도 없다 — MSW 로 「보낸 `from`·`to` 가 서버 기본값과 같은 형태인가」를 한 줄 잡아 두면 재발이 막힌다 |
| **F-2** | `features/tasks/components/TasksScreen.tsx:55-64`(`size: TASKS_PAGE_SIZE` 를 뷰와 무관하게 고정) · `:200`(페이지네이션을 `view === "list"` 로 한정) · `KanbanBoard.tsx:46`(`doneCount` 를 `items` 에서 센다) | **칸반이 그 달의 앞 12건만 그린다.** 목록 쿼리는 언제나 `size=12`·`page=1` 인데 **페이지네이션 UI 가 리스트 전용**이라, 칸반에서는 13번째 업무부터 **화면에 나타날 길이 없다.** 사용자는 그 달 업무가 12건뿐이라고 읽는다.<br>같은 뿌리로 **완료 컬럼 헤더 「8월 12」와 하단 「8월 완료 12건」이 틀린 수를 적는다** — `doneCount` 가 「그 달 완료 건수」가 아니라 **현재 페이지 안의 완료 건수**다. U-2 는 그 자리를 「**월 기준**」이라고 못박았다 | **SPEC-004 U-2 기대 결과** 「리스트와 **같은 기간·필터**를 본다」 · **U-2 상태** 「*완료 컬럼*: 헤더에 건수 대신 「8월 12」(**월 기준**), 하단에 「8월 완료 12건」」 · **WP Phase 4 작업**(완료 컬럼 헤더·캡션) | 칸반일 때 **페이지를 쓰지 않는다** — `size` 를 뷰로 갈라 보내거나(칸반은 상한을 크게), 칸반에 「더 보기」를 두거나, 서버에 컬럼별 상한을 둔다. **어느 쪽이든 SPEC 에 규격이 없다**(문서공백 G-3) — 코디가 U-2 에 한 줄 정한 뒤 고치는 편이 낫다.<br>완료 건수는 **응답의 `total` 축**에서 와야 한다. 지금 응답에는 「상태별 총계」가 없으므로 그것도 G-3 과 함께 정해야 한다.<br>**재현**: 한 달에 업무를 13건 이상 만들고 `?view=board` 로 연다 → 12건만 보인다 |

---

## WARN — 규약에서 벗어났으나 동작하는 것

| # | 파일:줄 | 무엇이 어긋났나 | 어긋난 문서 절 | 어떻게 고치나 |
|---|---|---|---|---|
| **W-1** | `tailwind.config.ts:44-45`(`current: { DEFAULT, foreground }`) → 영향 `components/ui/checkbox.tsx:22` `text-current` | **Tailwind 내장 관용구 이름을 덮었다.** `current` 는 Tailwind 기본 색으로 **`currentColor`** 이고 `text-current`·`fill-current`·`border-current` 는 「상속색을 그대로 쓴다」는 표준 관용구다. `extend.colors.current` 를 정의하는 순간 그 의미가 **`#F4F5FF` 고정**으로 바뀐다. 실제로 shadcn 생성물 `checkbox.tsx:22` 의 `text-current`(체크 표시가 부모 색을 물려받는 자리)가 그 영향을 받는다 — 지금은 `#F4F5FF` 와 `--primary-foreground`(흰색)가 둘 다 거의 흰색이라 **눈에 안 보이지만**, 앞으로 추가되는 shadcn 컴포넌트가 `fill-current`·`stroke-current` 를 쓰는 순간 조용히 틀린 색이 된다 | **`frontend/README.md` §2 규칙 2** 「`components/ui/` 는 shadcn CLI 가 만든 그대로 둔다 … 규격 차이는 **래퍼에서** 흡수한다」 — 생성물을 고치지 않았지만 **바깥에서 의미를 바꿨다** · **§5-1**(원시 토큰 → 시맨틱 변수 2층) | 색 키 이름을 관용구와 겹치지 않게 바꾼다 — 예 `pick`/`current-value` → `bg-pick`·`text-pick-foreground`. 쓰는 자리는 넷뿐이다(`TasksScreen.tsx:149` · `TasksFilters.tsx:67` · `TaskContextMenu.tsx:94` · `StatusPopover.tsx:78`). **값·규격은 그대로 두고 이름만 바꾸면 된다** |
| **W-2** | `features/tasks/hooks/useTasksViewParams.ts:101` `router.replace(...)` | **조건을 바꿔도 히스토리가 남지 않아 뒤로가기가 안 산다.** 뷰 토글·기간 스테퍼·필터가 전부 `replace` 라, 리스트↔칸반을 오간 뒤 뒤로가기를 누르면 **이전 뷰가 아니라 페이지를 떠난다.** 쿼리로 조건을 남기기로 한 이유 중 하나가 그것이다 | **`frontend/README.md` §1-2** 「`useState` 로 두면 새로고침·뒤로가기에서 잃는다. **쿼리는 정적 빌드와 양립하면서 뒤로가기가 산다**」 · **SPEC-004 §2 Placement** 「뷰 전환은 쿼리(`?view=list|board`)로 남아 **뒤로가기가 산다**」 | 최소한 **뷰 전환만이라도 `router.push`** 로 바꾼다. 필터·기간까지 push 하면 히스토리가 시끄러워지므로 축을 갈라도 된다 — 어느 축이 히스토리를 남기는지는 §1-2 에 한 줄 적어 두는 편이 낫다. **§6 Acceptance 15(새로고침 유지)는 지금도 통과한다** — 깨진 것은 뒤로가기뿐이다 |
| **W-3** | `features/tasks/components/KanbanBoard.tsx:56-66`(컬럼)·`:96-99`(플레이스홀더) | **삽입 가이드선이 없다.** U-4 는 드롭 가능 컬럼에 「컬럼 배경 `#F1F2FE` + 1px `#7181F8` 테두리」와 함께 **「삽입 위치에 2px `#7181F8` 가이드선」**을 요구한다. 앞의 둘은 있고(`border-primary bg-secondary`) **가이드선만 없다** — 여러 장이 쌓인 컬럼에서 어디로 들어가는지 보이지 않는다 | **SPEC-004 U-4 상태**(드롭 가능 컬럼) · **S-4 2** 「컬럼이 선택 색으로 바뀌고 **삽입 가이드선이 보인다**」 · **WP Phase 4 작업·검증** | 카드 사이 `onDragOver` 위치를 잡아 2px `bg-primary` 선을 끼운다. 지금 구조(컬럼 단위 `onDragOver`)에 카드 단위 핸들러를 더하면 된다. **정렬이 서버 정렬을 그대로 물려받아 「삽입 순서」가 저장되지는 않으므로**, 가이드선을 넣을지 U-4 에서 뺄지는 코디 판단일 수도 있다(문서공백 G-3 과 함께 보라) |
| **W-4** | `features/tasks/components/KanbanBoard.tsx:142-145` · `features/tasks/types.ts:147`(`cancelledAt` 은 타입에만 있다) | **칸반 취소 카드에 취소일이 없다.** U-2 는 「취소 컬럼: 카드에 **취소일과 사유**를 함께 적는다」인데 사유만 그린다. 서버는 `cancelledAt` 을 **취소 전이 로그에서 파생해 이미 내려주고 있다**(`task_repository.py:404-414`) — 리비전 `0003` 을 추가한 근거 둘 중 하나가 그것인데 **화면이 쓰지 않는다.** 프론트 전체에서 `cancelledAt` 을 읽는 코드가 0건이다 | **SPEC-004 U-2 상태**(취소 컬럼) · **§4 Data Contract**(목록 항목 `cancelledAt`) · 리비전 `0003` 의 근거 ② | `DueCell` 옆에 `formatTimestamp(task.cancelledAt)` 한 줄을 더한다. `lib/datetime.ts` 에 이미 포맷이 있다 |
| **W-5** | `features/tasks/hooks/useKanbanDnd.ts:72-77`(`onDragStart` 에 `setDragImage` 없음) | **드래그 고스트가 브라우저 기본이다.** U-4 는 고스트를 「원래 크기 유지, **그림자 `0 16px 40px rgba(0,0,0,0.16)`**(팝오버 그림자), 살짝 기울이지 않는다」로 규정했다. 회전 없음은 지켜지지만(기본 고스트는 안 기운다) **그림자 규격은 적용되지 않는다** | **SPEC-004 U-4 상태**(*드래그 시작*) · **WP Phase 4 작업** | `setDragImage` 로 `shadow-popover` 를 얹은 복제 노드를 쓰거나, U-4 에서 「고스트는 브라우저 기본을 쓴다」로 규격을 낮춘다. **후자가 합리적일 수 있다** — HTML5 DnD 의 기본 고스트는 스타일을 온전히 못 싣는다 |
| **W-6** | `features/tasks/components/TasksScreen.tsx:300` | **빈 상태 캡션이 규격 문구가 아니다.** U-9 는 「필터 결과 없음」 캡션을 「유형·상태 필터를 지우면 **n건이** 보입니다」로 정했는데 코드는 「유형·상태 필터를 지우면 **더 많은 업무가** 보입니다」다. `n` 을 알려면 필터를 뺀 카운트가 필요한데 지금 응답에 그 값이 없다 | **SPEC-004 U-9**(빈 상태 3종 표) | 「전체」 탭의 `typeCounts` 값(=유형 필터를 뺀 수)으로 근사할 수 있지만 **상태·프로젝트 필터는 여전히 반영된 값**이라 정확하지 않다. 서버에 「필터 없는 총계」를 하나 더 낼지, U-9 문구를 지금 구현대로 낮출지 **코디가 정해야 한다**(문서공백 G-3 묶음) |
| **W-7** | `features/tasks/hooks/useTasksViewParams.ts:40-43`(`currentMonth`)·`:123-142`(`monthRange`·`shiftMonth`·`formatMonth`) | **날짜 변환·포맷이 `lib/datetime.ts` 밖에 있다.** 「2026년 8월」 포맷과 달 경계 계산이 영역 훅 파일에 산다. `currentMonth()` 는 **디바이스 로컬 시간**(`getFullYear`/`getMonth`)을 쓰는데 서버는 `APP_TIMEZONE`(KST)을 쓴다 — KST 가 아닌 기기에서 「이번 달」 판정이 갈릴 수 있다 | **`frontend/README.md` §3-6** 「시각은 UTC ISO 문자열로 오고 **KST 변환은 `lib/datetime.ts` 하나**가 한다(G-2)」 · **§11 금지 목록 8** | 네 함수를 `lib/datetime.ts` 로 옮기고 KST 기준으로 통일한다. **F-1 을 고칠 때 같은 파일을 만지므로 함께 하는 편이 싸다** |

---

## 문서 공백 — 코드가 아니라 문서를 고쳐야 하는 것

| # | 무엇이 비었나 | 어느 문서 어느 절 | 무엇을 적어야 하나 |
|---|---|---|---|
| **G-1** | **`overdueDays` 가 상세 계약에 없다.** SPEC-004 §4 목록 항목에는 있는데 SPEC-003 §4 상세 응답에는 없어, 상세는 `isOverdue` 만 받고 「n일 지남」을 못 그린다. 백엔드가 상세를 안 건드린 것은 **계약을 지킨 것**이다(브리프 §4-2 지정) | **SPEC-003 §4 Request/Response**(`GET /api/tasks/{id}`) · **SPEC-004 U-10** 「상세: 헤더 기한 옆에 같은 문구」 | U-10 이 **상세에도** 「n일 지남」을 요구하므로 상세 응답에 `overdueDays` 를 더해야 앞뒤가 맞는다. SPEC-003 §4 예시 JSON 과 Data Contract 표에 `overdueDays` 한 줄을 넣고, **그 구현은 어느 work 몫인지**(WORK-005 후속 수정인지 다음 work 인지)까지 적어라 |
| **G-2** | **실행취소 조건 ②의 「다른 변경」이 실제로는 「로그를 남기는 변경」이다.** `find_last_transition` 은 **마지막 로그**가 전이인지만 본다(`task_child_repository.py:180-206`) — 제목·배경 인라인 편집처럼 로그를 안 남기는 변경은 감지하지 않는다. undo 가 되돌리는 것이 `status` 하나뿐이라 실질 피해는 없다 | **SPEC-004 §4**(`undo` 조건 ②) · **`backend/README.md` §8-2** `undo_not_available` 행 | 「② 그 뒤에 **로그를 남기는** 다른 변경이 없으며」로 문구를 좁혀라. 구현이 그렇고 그게 옳다 — 지금 문구대로면 「제목을 고치면 실행취소가 막혀야 하나?」를 다음 work 가 다시 묻는다 |
| **G-3** | **칸반의 데이터 범위 규격이 없다.** SPEC-004 는 리스트에만 페이지네이션을 두고 칸반에는 아무 말이 없다. 그래서 구현이 리스트 페이지 크기를 그대로 물려받아 **F-2** 가 됐다. 함께 비어 있는 것 둘 — ① 완료 컬럼 「8월 12」의 **12 가 어디서 오는 수인지**(응답에 상태별 총계가 없다) ② U-9 「필터를 지우면 **n건이** 보입니다」의 **n 을 어디서 얻는지**(필터 없는 총계가 응답에 없다) | **SPEC-004 U-2**(칸반) · **§4 Request/Response**(목록 응답 필드) · **U-9** | 셋을 한 번에 정해라 — 「**칸반은 그 달 전체를 그린다**(페이지를 쓰지 않는다)」인지 「칸반도 컬럼별 상한 n 건 + 「더 보기」」인지. 어느 쪽이든 **응답에 `statusCounts`(상태별 총계) 또는 `unfilteredTotal` 을 추가**해야 완료 컬럼 캡션과 U-9 의 `n` 이 성립한다. **F-2·W-6 이 이 결정을 기다린다** |
| **G-4** | **`typeCounts` 에 「0건 유형」 행이 없다는 사실이 계약에 없다.** 서버는 `Task JOIN WorkType` 집계라 그 기간에 업무가 없는 유형은 **행 자체가 안 온다**(`task_repository.py:498-533`). 화면은 유형 목록을 따로 읽어 없는 유형에 **0 을 그린다**(`TasksScreen.tsx:105-112`) — 옳은 처리이고 U-1 의 「유형 탭은 동적 유형 전체」와도 맞는다. 그런데 **그 계약이 어디에도 안 적혀 있다** | **SPEC-004 §4**(`typeCounts` 설명) · **WP §Internal Interface Contract** `typeCounts` 행 | 「`typeCounts` 는 **그 기간에 업무가 있는 유형만** 담는다 — 탭 목록은 화면이 유형 목록에서 그리고 **없는 유형은 0 으로 표시한다**(탭을 감추지 않는다)」를 적어라. 안 적으면 다음 사람이 「탭이 사라지는 버그」로 오해하거나 서버에서 0 행을 만들어 넣는다 |
| **G-5** | **「같은 상태로 다시 보내기」의 계약이 두 곳에서 다르다.** 서버는 전이 그래프에 자기 자신이 없어 **409 `invalid_status_transition`** 을 낸다(`test_staying_on_the_same_status_is_rejected`). 화면은 그걸 「사용자가 아무것도 안 했는데 에러를 보는 자리」로 보고 **요청을 내지 않는다**(칸반 같은 컬럼 재드롭 · 팝오버 현재 값 `disabled`). 둘 다 맞지만 **Case Matrix 에 이 경계가 없다** | **SPEC-004 §4 Case Matrix** · **§4 Validation**(전이 표) | 「**같은 상태로의 전이는 그래프 밖이다**(409). 화면은 그 요청을 애초에 내지 않는다 — 현재 값 항목은 비활성이고 같은 컬럼 재드롭은 요청 0건이다」를 Validation 이나 Case Matrix 에 한 줄. **WORK-008 의 회의록 경로가 이걸 모르면 「이미 완료인 업무를 완료로」 요청해 409 를 사용자에게 보인다** |
| **G-6** | **「현재 값」 색 축(`#F4F5FF`)이 디자인 토큰 문서에 없다.** SPEC-004 §2 가 뷰 토글을 「현재 값 배경 `#F4F5FF` + `#4B52A8`」로 정했고 U-3 도 상태 팝오버 현재 값에 같은 색을 쓴다. 구현이 `--tm-current-bg` 를 신설했는데 `09-design-tokens.md` §색에는 **선택(`#F1F2FE`)만 있고 「현재 값」 축이 없다** | **`00-design/09-design-tokens.md` §색** · SPEC-004 §2 · S004-OQ-2 | 「**현재 값 배경** `#F4F5FF`(전경 `#4B52A8`)」를 §색에 등록하고 **선택(`#F1F2FE`)과 다른 축**임을 한 줄로 구분해라. 지금은 SPEC 본문에만 값이 있어 화면마다 새로 적힌다. S004-OQ-2 의 디자인 원본 정정과 같이 처리하면 된다 |
| **G-7** | **칸반 드롭 플레이스홀더 두 색(`#C9D1FB`·`#F8FAFF`)도 토큰 문서에 없다.** U-4 가 값을 직접 적었고 구현이 `--tm-drop-placeholder-*` 로 신설했다. 코드 주석은 「새 색을 만들지 않는다」라고 적었지만 **실제로는 hex 두 개가 새로 생겼다**(SPEC 이 정한 값이라 코드 문제는 아니다) | **`00-design/09-design-tokens.md` §색** · SPEC-004 U-4 | 두 값을 §색에 등록하거나, 기존 팔레트에서 대체값을 지정해라. 등록하면 U-4 의 「새 색을 만들지 않는다」 문장과 실제가 일치한다 |

---

## SPEC-004 §6 Acceptance 18항목 대조

> 나는 **read-only** 라 앱 창을 띄우지 못했다. 아래 「코드상」은 **코드를 읽어 그 동작이 성립하는지**를 본 것이고,
> 「실측」은 사람이 앱 창에서 확인해야 하는 몫이다. 실측 증거(캡처)는 완료 증거 파일에 없다.

| # | 항목 | 코드상 | 근거 / 비고 |
|---|---|---|---|
| 1 | 리스트 셀 「진행중」 → 셀 변경 + 로그 「상태 시작전 → 진행중」 | **성립** | `StatusPopover` → `setStatus` → `PATCH /status`. 로그 문구는 서버가 `_STATUS_LABELS` 로 만든다(`task_service.py:800-806`) |
| 2 | 리스트 셀 완료 거부 + 규격 문구 토스트 | **성립** | 서버 `_COMPLETION_BLOCKED` 문구가 SPEC 과 글자까지 같다. 화면은 `error.detail` 을 그대로 띄운다(6초) |
| 3 | 상세 드롭다운도 **같은 문구로** 거부 | **성립** | `TaskDetailParts` 가 **같은 `StatusPopover`·같은 `useTaskStatus()`** 를 쓴다. FE 테스트 `useTaskStatus.test.tsx:111` 이 「같은 경로·같은 본문」을 잡는다 |
| 4 | 칸반 완료 컬럼 드롭 → 원래 컬럼 복귀 + 같은 문구 | **성립** | 낙관적으로 안 옮기므로 「복귀」가 자동이다. `blockedReason` 이 완료 컬럼을 막지 않는다 |
| 5 | 거부 토스트 「결과 입력」 → 상세 열림 + 완료 결과 포커스 | **성립** | `onEnterCompletion` → `openTaskDetailDrawer(…, {focusCompletion:true})` → **WORK-004 의 `useCompletionCardFocus()`**. 새로 만들지 않았다 |
| 6 | 완료 후 「완료 처리했습니다 · 실행취소」 4초 | **성립** | `DONE_TOAST_MS = 4000` |
| 7 | 실행취소 → 직전 상태 + 완료 로그 삭제 | **성립** | 서버 테스트 `test_undo_restores_the_previous_status_and_removes_that_log` |
| 8 | 4초 뒤 「되돌릴 수 있는 시간이 지났습니다」 | **성립** | 서버 테스트 `test_undo_is_unavailable_after_four_seconds`(로그 시각을 5초 전으로 옮겨 검증 — 아래 「확인 못 함」 U-3 참조) |
| 9 | 완료 카드 취소 컬럼 드롭 불가 + 우클릭 「취소」 비활성 | **성립** | `useKanbanDnd` + `statusTransitions`. FE 테스트 `:179` 가 잡는다 |
| 10 | 진행중 → 「취소」 모달 600 + 사유 없으면 확인 비활성 | **성립** | `CancelModal` + `ConfirmModal` 의 `setCanConfirm` 슬롯 |
| 11 | 취소 업무 취소선 + 취소 컬럼 + **목록에 남는다** | **성립** | 리스트·칸반 모두 `line-through`. 취소는 소프트 딜리트가 아니라 상태다 |
| 12 | 우클릭 삭제 → 「v1 에는 복원 화면이 없습니다」 + 목록에서 사라짐 | **성립** | `TasksScreen.tsx:85-94` 문구가 U-8 과 같다. 서버는 소프트 딜리트 |
| 13 | 「n일 지남」 붉게 + 상태는 진행중 | **성립** | `TaskMeta`/`OverdueBadge` 가 **서버 파생값을 그대로** 그린다(다시 계산하지 않는다) |
| 14 | 유형 탭 + 상태 필터 AND + 「조건에 맞는 업무가 없습니다 · 필터 지우기」 | **부분** | AND 는 성립(서버 `test_each_filter_actually_narrows_the_result`). **캡션 문구가 규격과 다르다(W-6)**, 그리고 **결과 집합이 F-1 로 말일 업무를 빠뜨린다** |
| 15 | 칸반 전환에도 기간·유형 유지 + 새로고침 유지 | **성립** | 조건이 전부 `?` 에 남는다. **단 뒤로가기는 안 산다(W-2)** |
| 16 | 첫 로딩 스켈레톤 + 필터 변경 시 이전 결과 유지 | **성립** | `isPending` 에만 스켈레톤, `keepPreviousData` + 얇은 진행 바 |
| 17 | 1280~1439 메모 컬럼 숨김 · 칸반 320 고정 + 가로 스크롤 | **성립** | `TaskListView` `hidden … wide:table-cell`, `KanbanBoard` `w-kanban-col shrink-0` + `overflow-x-auto`. 리스트로 자동 전환하지 않는다 |
| 18 | 서버 내린 채 목록 → 빈 목록이 아니라 실패 표시 + 「다시 시도」 | **성립** | `TasksBody` `query.isError` 갈래. `retry:false` 라 「다시 시도」가 한 번만 나간다 |

**요약 — 18항목 중 17항목 코드상 성립, 1항목(14) 부분.** 다만 **F-1 이 기간 축 전체에 얹혀 있어** 1·14·15 가 보는 데이터 집합이 계약과 다르고, **F-2 로 칸반의 4·9·15·17 은 12건 안에서만 성립한다.** 전 항목 **실측 미확인**.

---

## WP §Done Criteria 대조

| # | 항목 | 판정 | 근거 |
|---|---|---|---|
| 1 | 모든 Phase 가 `DONE`/`SUPERSEDED` | **미충족** | `work-005-tasks-status-views.md` 의 Phase 1~4 **Status 가 전부 `TODO`**, 완료 증거 4곳 모두 「미작성」. 코드는 다 있으므로 **문서 갱신 누락**이다(코디 소관) |
| 2 | Acceptance 18개 전부 확인 | **부분** | 위 표 — 코드상 17 성립·1 부분, **실측 증거 없음** |
| 3 | **세 진입점 같은 요청 캡처 3장** | **미충족(대체 증거 있음)** | 캡처 파일이 없고 커밋 메시지에도 언급이 없다. 대신 **FE 테스트 `useTaskStatus.test.tsx:111`** 이 「리스트 셀·상세 드롭다운·칸반 드롭이 같은 경로·같은 본문을 낸다」를 코드로 고정한다 — **캡처보다 강한 증거**지만 Done Criteria 문구는 캡처를 요구한다. 코디가 문구를 테스트로 바꾸거나 캡처를 받아야 한다 |
| 4 | 정적 검사 4종 결과 | **충족(내가 재현)** | ① 상태 대입 1곳 ② 게이트 예외 1곳 ③ 전이 호출 1곳(`useTaskStatus.ts`) ④ **Ink 하나** — `bg-ink`/`border-ink` 를 쓰는 컴포넌트는 `UnderlineTabs`(유형 탭)와 `Sidebar`(다른 축)뿐이고 **뷰 토글은 Ink 가 아니다**(`bg-current`). grep 결과는 이 리포트에 담았다 |
| 5 | BE §12 1·2 + FE §11 1 통과 | **충족(코드상)** | BE 1 = `test_completing_without_any_result_is_blocked_and_the_status_stays` · BE 2 = `test_done_cannot_go_to_cancelled` · FE 1 = `useTaskStatus.test.tsx:75`. **실행은 안 했다** |
| 6 | `log.md` · `30-work/README.md` 갱신 | **미충족** | `log.md` 최신 항목이 **2026-09-03** 이고 WORK-004·005 기록이 없다. `30-work/README.md` 에 **WORK-004·005 행이 없다**. 코디 소관 |

---

## 확인한 것 (PASS 근거)

**게이트·전이·실행취소**(브리프 핵심 축)
- **`task.status` ORM 대입 1곳** — `task_repository.py:311` `row.status = status`. 그 함수(`update_status`)를 부르는 곳은 **판정을 지난 둘뿐**(`task_service.py:788` `change_status` · `:832` `undo_last_status`). 그 밖의 `status=` 히트는 전부 DTO 조립이다.
- **`TaskCompletionBlockedError` 1곳** — `task_service.py:786`. 판정식은 `completion_result.strip()` **또는** `count_deliverables ≥ 1`(`role='deliverable'` 만 센다).
- **`task_log` DELETE 1곳** — `task_child_repository.py:208-215`, 호출은 `undo_last_status` 하나(T-8-b).
- **일반 PATCH 로 상태 불가** — `TaskUpdate` 에 `status` 필드가 없고 `_TaskRequest` 가 `extra="forbid"` → **422 `validation_error`**(`test_the_general_patch_refuses_status`).
- **전이 그래프**가 T-6 그대로이고 `done→cancelled` 가 없다. 서버·화면이 **같은 표**를 보되(`_TRANSITIONS` ↔ `statusTransitions.ts`) 화면 쪽 파일이 「이 표는 편의다, 정본은 서버」라고 스스로 못박았고 **완료 게이트는 화면 표에 없다**.
- **실행취소 조건 셋** — ① `find_last_transition` 이 **마지막 로그가 전이일 때만** 돌려준다 ② 그래서 뒤에 다른 로그가 있으면 `None` ③ `_UNDO_WINDOW = 4초`. **직전 상태 복원 + 그 로그 삭제가 한 트랜잭션**이고 **게이트를 다시 태우지 않는다**. 테스트 5건이 각 조건과 「두 번 undo 는 거부」까지 덮는다.
- **취소 사유** — `cancelled` 로 갈 때만 필수(1~500자), 다른 상태에 얹으면 거부, 떠나면 비운다(T-7). `logCancelReason` 기본 참.

**마이그레이션 `0003`**(WP 를 벗어난 추가)
- **새 리비전으로 얹었다** — `down_revision = "0002_task_domain"`, `0002` 를 고치지 않았다.
- **`downgrade()` 가 완비**돼 있다(제약 3개 → 컬럼 2개 역순).
- **CHECK 3개** — `(from_status IS NULL) = (to_status IS NULL)`(전이 로그만 두 값을 갖는다) + 각 컬럼의 값 집합. 「전이 로그만」을 DB 가 알 방법은 이 짝 제약뿐이므로 **강제 형태가 맞다**. `models/task.py:181-196` 이 같은 제약을 선언해 드리프트가 없다.
- **`cancelledAt` 이 로그에서 파생**된다 — `_cancelled_at()` 이 `to_status='cancelled'` 로그의 `max(created_at)` 을 스칼라 서브쿼리로 읽고, `task` 에 컬럼을 만들지 않았다(G-7). 취소 상태가 아니면 `None` 으로 지운다(`test_cancelled_at_is_carried_only_while_cancelled`).

**목록·집계**
- **`typeCounts` 가 유형 탭 자신을 반영하지 않는다** — `count_by_work_type` 이 `work_type_id=None` 으로 `_list_filters` 를 부른다. 상태·프로젝트는 반영한다(`test_type_counts_ignore_the_work_type_tab_but_follow_other_filters`).
- **0건 유형은 응답에 행이 없고 화면이 0 을 그린다** — `TasksScreen.tsx:105-112` 가 유형 목록을 기준으로 탭을 만들고 카운트를 찾아 붙인다(없으면 `?? 0`). **탭을 감추지 않는다.**
- **NULLS LAST** — `_SORTS` 가 `due_asc`·`due_desc` 둘 다 `.nullslast()` 를 명시한다(Postgres 의 DESC 기본이 NULLS FIRST 라서). 테스트 2건.
- **`EXPLAIN` 에 `schedule` 이 없다** — 주장이 아니라 **테스트로 고정**돼 있다: `test_the_list_query_never_joins_schedule`(`test_task_list.py:432`)와 `test_the_period_filter_never_touches_schedule`(`:453`)이 실제로 `EXPLAIN` 을 돌려 확인한다. WORK-004 의 `test_schedule_derive.py:393` 도 같은 축.
- **「지연」은 저장되지 않는다** — `_to_list_item` 이 `today` 와 상태로 파생하고, 화면(`TaskMeta`)은 **다시 계산하지 않고** `isOverdue`·`overdueDays`·`dDay` 를 그대로 그린다.
- **소프트 딜리트** — 목록에서 빠지고 **행과 자식이 DB 에 남는다**(`test_delete_is_soft_and_keeps_the_row_and_children`). 삭제된 업무는 상태 전이도 못 한다. **복원 표면 0건**(`test_there_is_no_restore_endpoint`).
- **쿼리 alias 8개 전부 명시** — `from`·`to`·`workTypeId`·`status`·`projectId`·`sort`·`page`·`size`(`task_router.py:107-114`). `test_each_filter_actually_narrows_the_result` 가 **각 파라미터가 실제로 결과를 좁히는지**를 확인한다(§3 규칙 7 이 경고한 「조용히 무시되고 200」을 잡는 테스트다).

**규약 일반**
- `except Exception`/bare `except` **0건** · `.commit()` 은 `deps.py`(요청 경계)·`seed.py` 뿐 · service·repository 에 `fastapi`/`schemas` import **0건** · **`persist_changes` 를 새로 켠 예외 0건**(여전히 `RefreshTokenReuseError` 하나이고, `TaskCompletionBlockedError` 는 「실패가 쓰기를 뜻하지 않는다」를 docstring 에 적어 두었다).
- 신규 예외 3종이 §8-2 계층 그대로다 — `TaskCompletionBlockedError(ValidationError)` → 422 · `InvalidStatusTransitionError(ConflictError)`·`UndoNotAvailableError(ConflictError)` → 409. **§8-2 표에도 셋 다 등록돼 있다**(코디가 닫았다).
- 프론트: 동적 세그먼트 **0** · 모든 `page.tsx` 에 `'use client'` · **컴포넌트 hex 리터럴 0건** · 직접 `fetch` 0건 · `retry:false` 유지 · 무효화는 `['tasks']` 뿐이고 **`['schedules']` 를 건드리지 않는다**(기한이 안 바뀌므로 — FE §3-3 표).
- **화면당 Ink 하나** — 내 업무 화면에서 Ink 를 쓰는 것은 **유형 탭 밑줄**(`UnderlineTabs.tsx:50`)뿐. 뷰 토글·필터 칩·상태 팝오버 현재 값은 전부 「현재 값/선택」 축이다.
- **조건이 전부 `?` 에 남는다** — `useTasksViewParams` 가 기간·유형·상태·프로젝트·정렬·뷰·페이지를 파싱하고, 컴포넌트가 자체 상태로 들지 않는다. 조건이 바뀌면 **1페이지로 돌아간다**(3페이지에서 필터를 걸어 빈 화면이 되는 것을 막는다).
- **거부 토스트의 「결과 입력」이 WORK-004 의 훅을 부른다** — `features/tasks/index.ts` 가 내보낸 `useCompletionCardFocus()` 를 `TaskDetailDrawer` 가 쓴다. **규격이 둘이 되지 않았다.**

**테스트** — 백엔드 `test_task_status.py` 26 · `test_task_list.py` 20 = **46건**(전이·게이트·취소·undo 5조건·소프트 딜리트·필터 각각·집계·정렬·파생값·EXPLAIN·세션 게이트·소유 404). 프론트 `useTaskStatus.test.tsx` **9건**(게이트 거부·전이 거부·세 진입점 동일 요청·취소 본문·같은 컬럼 재드롭 0건·전이 차단·완료 컬럼 개방).

---

## 확인 못 함 (추측으로 PASS 주지 않는다)

| # | 무엇 | 왜 못 했나 |
|---|---|---|
| **U-1** | **`pytest` 46건 + 전체 291건이 실제로 통과하는지** | read-only 라 실행하지 않았다. 커밋 메시지가 「291 passed」를 주장하지만 나는 확인하지 못했다 |
| **U-2** | **`npm run test`·`typecheck`·`build` 결과** | 같은 이유. **F-1·F-2 는 타입 검사·빌드를 통과한다** — 값의 의미 차이라서 |
| **U-3** | **실행취소 4초 창을 「실제 시간」으로 확인한 결과** | 테스트는 로그의 `created_at` 을 **5초 전으로 옮겨** 검증한다(`test_task_status.py:359-366`, 테스트 주석이 그 사실을 밝힌다). **이 방식 자체는 옳다** — 조건식 `now - created_at > 4s` 를 정확히 태우고 5초 sleep 을 넣지 않는다. 커밋 메시지는 curl 로 **실제 5초를 기다려** 409 를 봤다고 적었으나 **그 출력이 파일로 남아 있지 않아** 나는 확인하지 못했다 |
| **U-4** | **세 진입점 실측 캡처 3장** | Done Criteria 가 요구하는 캡처가 어디에도 없다. FE 테스트가 같은 사실을 코드로 잡지만 캡처와는 다른 증거다 |
| **U-5** | **`EXPLAIN` 실제 출력** | 테스트가 `EXPLAIN` 을 돌려 `schedule` 부재를 단언하는 것은 코드로 확인했다. **그 테스트가 통과하는지**는 U-1 에 걸린다 |
| **U-6** | **앱 창에서의 시각 규격** — DnD 고스트·가이드선·컬럼 색·1280~1439 레이아웃·스켈레톤·토스트 수명 | 브라우저 없이 판정할 수 없다. W-3·W-5 는 **코드에 그 코드가 없다**는 사실만으로 잡은 것이고, 나머지 시각 규격은 클래스 이름까지만 확인했다 |
| **U-7** | **마이그레이션 `0003` 의 upgrade/downgrade 왕복** | DB 를 건드리지 않았다. `downgrade()` 가 존재하고 역순인 것은 읽어서 확인했다 |

---

## 코디 실행 요청

1. **`cd app/back && uv run pytest`** — U-1. 특히 `test_the_list_query_never_joins_schedule`·`test_the_period_filter_never_touches_schedule` 가 §12 5-a 를 대신하는 자물쇠다.
2. **`cd app/front && npm run test && npm run typecheck && npm run build`** — U-2.
3. **F-1 재현(2분, 최우선)**: 이번 달 **마지막 날**을 기한으로 업무를 하나 만들고 `/tasks` 를 연다 → 목록·칸반·하단 카운트 어디에도 없다. 기한을 하루 당기면 나타난다. `?from=`·`?to=` 를 서버 기본값(다음 달 1일, UTC ISO)으로 직접 붙여 호출하면 다시 보인다 — 그게 프론트가 보내야 할 값이다.
4. **F-2 재현(3분)**: 한 달에 업무를 13건 이상 만들고 `?view=board` → 12건만 보이고 완료 컬럼 캡션이 페이지 기준 수를 적는다.
5. **문서 결정 선행**: **G-3**(칸반 데이터 범위 + 상태별 총계 + U-9 의 `n`)을 먼저 닫아야 **F-2·W-6** 을 고칠 수 있다. 그다음 G-1(상세 `overdueDays`) → G-5(같은 상태 재전송 — **WORK-008 이 밟는다**) → G-2·G-4·G-6·G-7.
6. **재발주 묶음 제안**: **F-1 + W-7** 한 발주(같은 파일 `useTasksViewParams.ts` 를 만지고, 날짜 함수를 `lib/datetime.ts` 로 옮기면서 경계를 고친다) · **F-2 + W-6** 한 발주(G-3 결정 이후) · **W-1 + W-2 + W-3 + W-4 + W-5** 는 화면 마감 묶음.
7. **Done Criteria 3·6** — 캡처 요구를 FE 테스트로 대체할지 정하고, `log.md`·`30-work/README.md` 에 WORK-004·005 를 올려라(두 work 연속 누락이다).

---

## 자기 점검

- [x] **네 층 전부에 판정을 냈다** — 정책 PASS / 아키텍처 WARN / SPEC FAIL / WP FAIL (+ 게이트 단일화·낙관적 갱신 두 축 별도 총평).
- [x] **모든 FAIL·WARN 에 파일:줄 + 어긋난 문서 절이 붙었다** — FAIL 2건, WARN 7건 전부. 둘 다 **재현 절차**를 적었다.
- [x] **문서 공백을 지적과 분리했다** — 별도 절 7건. 그중 G-3 은 **F-2·W-6 의 선행조건**이라 우선순위를 명시했다.
- [x] **Acceptance 18항목과 Done Criteria 6항목을 하나씩 대조**했다 — 표 두 개. 코드상 성립/부분/미충족을 갈랐고 **실측은 전부 미확인**으로 적었다.
- [x] **판정 못 한 것을 「확인 못 함」으로 적었다** — 7건. 특히 브리프가 물은 **실행취소 5초 실측**은 「테스트는 시각을 옮긴다(그리고 그게 옳다), 실시간 확인은 커밋 메시지에만 있어 검증 못 함」으로 갈라 적었다.
- [x] **코드·문서를 하나도 고치지 않았다** — `git status --porcelain` 무출력. 리포트는 문서 레포에만 썼다.
- [x] **취향으로 지적하지 않았다** — 규약에 조문이 없는 것(`TaskContextMenu` 의 커서 좌표 인라인 `style`, `ProgressBar` 의 width `%`, 드롭 불가 컬럼에서 네이티브 툴팁 대신 컬럼 안 캡션을 쓴 선택)은 제외했다. 마지막 것은 **드래그 중 네이티브 툴팁이 안 뜬다는 실물 관찰에 근거한 개선**이라 오히려 PASS 근거로 적었다.
