# [backend+frontend] WORK-008 Phase 5 — 업무 연동 (완료 게이트의 네 번째 진입점)

너는 **task-management 코드 워커**다. **이 Phase 는 백엔드와 프론트를 한 워커가 함께 한다** — 한 요청이 두 층을 지난다.

**코드 워크트리** — `/Users/kknaks/orca/workspaces/task_management/docs-v1` (브랜치 `kknaksss/docs-v1`).
WORK-006·007 전부와 WORK-008 Phase 1~4·6 이 들어와 있다.

```
/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/para/projects/summer-star/task-management/
  30-work/work-008-meeting-close.md      ← **Phase 5 만**
  20-spec/spec-008-meeting-close.md      ← §4 · U-6 · U-9 · U-10 · Acceptance
  20-spec/spec-004-tasks-status-views.md ← 완료 게이트 · 전이 그래프 · 같은 상태 409
  20-spec/spec-003-tasks-crud.md         ← 업무 생성 규칙 · U-7
  10-decision/decision-003-meeting-notes.md §4 L102(pendingChange 3필드) · §5 L116
  10-decision/decision-002-my-tasks.md   ← 완료 게이트
  30-work/work-005-tasks-status-views.md ← **L137 · L147 · L294 를 반드시 읽어라**
```

## ⛔ 1. 이 Phase 의 존재 이유 — **회의록 쪽에 판정 코드가 하나도 없어야 한다**

```
work-005 L137   회의록의 「업무 갱신」이 상태를 완료로 보낼 때
                PATCH /api/tasks/{id}/status 와 그 뒤의 task_service.change_status()
                **이 하나를 지난다** — 회의록 쪽에 판정 코드를 두지 않는다(BE §8-3)
work-005 L147   task.status 를 대입하는 코드는 change_status() 안에만 있다
work-005 L294   완료 게이트의 네 번째 진입점은 WORK-008 이 붙인다.
                우회하지 않는지를 **WORK-008 이 검증 항목으로** 확인한다
work-004 L156   회의록의 「업무 생성」·「업무 갱신」이 task_service 를 그대로 부른다
```

**`task_service.py` 를 고치지 마라.** `create()` · `update()` · `change_status()` · `add_memo()` 를 **그대로 부른다.**
같은 트랜잭션에서 부를 수 있게 세션을 넘기는 시그니처만 확인해라.

**회의록 서비스에 이런 게 있으면 FAIL 이다** — 완료 가능 여부 판정 · 전이 그래프 · `TaskCompletionBlockedError` 를 잡아 다르게 처리 · `task.status` 대입.

## 2. 백엔드

```
meeting_task_link_service.create_task_from_line()
    task_service.create()(SPEC-003 규칙) + 줄 kind='task' · task_id — **한 트랜잭션**

meeting_task_link_service.apply_pending_change()
    ① status  현재와 **다를 때만** task_service.change_status()
              (같으면 부르지 마라 — SPEC-004 L478 「같은 상태 전이는 409」가 사용자에게 보인다)
    ② dueDate task_service.update()
    ③ note    add_memo()
    ④ pending_change 를 비운다 — **한 트랜잭션**

표면
    POST  …/lines/{id}/task      액션 줄 → 업무 생성
    PATCH …/lines/{id}/task      업무 줄 → 갱신
    POST  …/lines 의 taskId / newTask 갈래   ← Phase 2 의 501 스텁을 교체한다

pendingChange 검증
    허용 키 3개뿐 — 기한 · 상태 · note (DEC-003 §4 L102)
    cancelled 거부 · 네 번째 키 거부 → 422
    삭제된 업무 → 404
```

**완료 게이트가 거부하면 아무것도 안 바뀌어야 한다** — `task.status` · `due_date` · 메모 수 · `pending_change` 전부 그대로. **한 트랜잭션이니 자연히 그렇게 된다. 테스트로 고정해라.**

## 3. 프론트

```
LineTaskButton (U-6)        「업무 생성」 / 「업무 갱신」(툴팁 = pendingChange 키, 같은 상태 제외)
                            / 「갱신 완료」 / 「삭제된 업무」 · generating 잠금 · 드로어 모드 숨김
LinkTaskDrawer (U-9)        프로젝트 셀렉터 + 검색 + 후보(GET /api/tasks/relations/candidates)
                            + 기한/상태/메모 · 「연결하고 갱신」 = 줄 추가 → 변경 있으면 갱신
CreateTaskFromLineDrawer    제목 프리필 · 유형/프로젝트 · 기한 · 메모(→ description)
  (U-10)                    **「시작 상태」 셀렉터 없음**(시안 L2850~2851 제외)
                            **「연관 업무로 바꾸기」 토글 없음**(L2863~2866 제외)
useMeetingTaskLink          생성·갱신 뮤테이션 각 하나
                            게이트 거부 토스트(WORK-005 규격 + 「결과 입력」 유도 훅)
                            완료 성공 시 WORK-005 완료 토스트/실행취소
```

**「업무 갱신」 한 번에 요청이 하나여야 한다** — `PATCH …/lines/{id}/task` 하나. **업무 API 를 나눠 부르지 마라.**

**공용 부품 재사용** — `DrawerFrame 840` · `Selector` · `TypeBadge` · `ItemRow` · `EmptyState` · `AgendaLineTree`(props 로만) · `lib/` 훅.

## ⛔ 4. 검증 — **앱 창 E2E 는 하지 마라**

```bash
cd app/back  && uv run pytest -q <네가 만들거나 고친 테스트만>
cd app/front && npx tsc --noEmit && npx vitest run
```

**⚠ 통과 판정 규칙 — 이번 work 에서 두 번 놓쳤다. 코디가 둘 다 잡았다**

```
① 마지막에 반드시 `make test`(전체)를 돌려라
   Phase 1·2 워커가 단독 실행만 보고 「507 passed」라고 했는데
   전체 스위트에서 1건이 깨졌다(순서 의존)

② `npx vitest run` 출력의 **`Errors` 줄이 0** 인지 확인해라
   Phase 3·4·6 워커가 「283 passed」라고 했는데
   Unhandled Rejection 1건이 함께 났다.
   vitest 가 「This might cause false positive tests」라고 직접 경고한다
   — `passed` 숫자만 보지 마라
```

**뮤테이션이 실패를 던질 때 그걸 받는 자리가 있는지 반드시 확인해라.** 재시도 클로저가 `void` 로 부르는
경로에서 두 번째 실패가 unhandled 로 샌다 — 방금 그 자리를 고쳤다(`useMeetingEdit`).

**완료 게이트 우회 0건 — 정적 검사 3종. grep 결과를 완료 증거에**

```
① task.status 에 값을 대입하는 코드가 task_service.change_status() 안에만
   (WORK-005 검사의 재실행)
② meeting_* 서비스에서 TaskCompletionBlockedError 를 잡아 처리하는 코드 0
③ 전이 그래프·완료 조건 판정이 meeting_* 에 0
```

**테스트로 고정할 것**

```
게이트 거부   결과자료·완료 결과 없는 업무 줄에 status='done' → 422 task_completion_blocked
              **task.status · due_date · 메모 수 · pending_change 전부 그대로**
게이트 통과   결과자료 붙인 뒤 같은 요청 → 200 · done · task_log 전이 1줄 · pending_change NULL
같은 상태     이미 done 인데 status:'done' → **409 없이 200**, 기한·메모만 · 전이 로그 없음
검증 실패     cancelled · 네 번째 키 → 422 / 삭제된 업무 → 404
업무 생성     액션 줄 → 201 · 「시작전」 · 로그 「업무 생성」 · 줄이 kind='task'
              유형 없으면 422 · 삭제된 유형이면 invalid_work_type 이고 **줄이 안 바뀐다**
요청 수       「업무 갱신」 한 번에 PATCH …/lines/{id}/task **1건**(fetch 스파이)
```

**테스트로 못 덮은 것은 「실물 확인 필요」로 보고에 남겨라.** 통과 처리하면 리뷰에서 FAIL 이다.

## 5. 지킬 것

1. **`task_service.py` 를 고치지 마라**
2. **Phase 3·4·6 이 만든 화면을 갈아엎지 마라** — 줄 버튼과 드로어 둘만 더한다
3. **문서를 고치지 마라** · **커밋·push 하지 마라**
4. **WP Phase 5 범위 밖을 하지 마라.** 발견하면 보고에 적어라
5. **기획·정책에 없는 기능을 만들지 마라** — 「시작 상태」 셀렉터 · 「연관 업무로 바꾸기」 토글은 시안에 있어도 안 그린다
6. 막히면 물어라 — `orca terminal send --terminal term_6a4ac855-2a13-4484-b808-4c25182cbb2b --text "..." --enter`

## 6. Done Criteria

- [ ] WP Phase 5 작업 항목이 전부 구현됐다
- [ ] **정적 검사 3종이 0** — grep 결과가 완료 증거에
- [ ] 게이트 거부 시 **아무것도 안 바뀐다**는 DB 전후 비교가 있다
- [ ] 같은 상태로 보내도 **409 가 사용자에게 안 보인다**
- [ ] 「업무 갱신」 요청이 **1건**
- [ ] 「시작 상태」 · 「연관 업무로 바꾸기」가 화면에 **0건**
- [ ] `make test`(전체) 통과 · `tsc` 0 · `vitest` 통과 · 앞선 work 회귀 없음
- [ ] `task_service.py` 변경 0 · 커밋 없음

## 7. 완료 보고 — 문구 변경 금지

```bash
orca orchestration send \
  --to term_6a4ac855-2a13-4484-b808-4c25182cbb2b --from term_b3b88f67-95f5-4315-85ca-b5d8bc2934cc \
  --type worker_done \
  --task-id <taskId> --dispatch-id <dispatchId> \
  --subject "WORK-008 Phase 5 완료" \
  --body "만든 표면·화면 / **정적 검사 3종 grep 결과** / 게이트 거부 시 DB 전후 비교 / 같은 상태 처리 / 요청 1건 증거 / make test(전체) 결과·tsc·vitest / **실물 확인 필요 목록** / task_service 미변경 확인 / 범위 밖이라 안 한 것"

orca terminal send --terminal term_6a4ac855-2a13-4484-b808-4c25182cbb2b \
  --text "[worker_done] WORK-008 Phase 5 완료. 상세는 인박스." --enter
```
