# WORK-004 검수 리포트

- 검수 대상: `aec6222`(BE Phase 1~3) · `70924d7`(후보 컬렉션 표면 전환) · `7550e1b`(FE Phase 4~6) · `9897ff5`(scope·total) · `99a45e7`(필터 칩 3·카운트) — `git diff 5bfe012...HEAD` 기준 **57파일 / +8730 −18**
- 워크트리: `/Users/kknaks/orca/workspaces/task_management/docs-v1` · 작업 트리 clean(`git status --porcelain` 무출력, untracked 0)
- 판정 기준: DEC-002 · SPEC-003 · `40-architecture/{backend(§3 규칙 7·§7·§8), frontend(§6-2), database/domains/task}` · WORK-004
- 검수자는 **코드·문서를 하나도 고치지 않았고 테스트·빌드를 돌리지 않았다.**

---

## 판정 요약

| 층 | 판정 | 근거 |
|---|---|---|
| **정책**(DEC-002) | **PASS** | 완료 게이트·상태 전이를 **서버에도 화면에도 만들지 않았다**(WORK-005 몫이 정확히 비어 있다) · `projectId` N:1 0..1 무소속 허용 · 소프트 딜리트에 복원 경로 0건 · **메모는 로그가 아니다**(서버가 로그를 안 남기고 테스트가 잡는다) · 로그는 시스템 기록뿐(사용자 쓰기 표면 없음) |
| **아키텍처 — 백** | **PASS** | 계층·ORM 경계·schema/dto·`commit()` 위치·`except Exception` 0건·`persist_changes` 여전히 `RefreshTokenReuseError` 하나. **`schedule` 쓰기가 `schedule_service` 하나로 격리**(SCH-1 grep 0건) · 생성이 한 트랜잭션 · 겹침이 원본 쓰기 **앞**에 · 남의 업무 404 · **§3 규칙 7 쿼리 alias 4종 전부 명시** |
| **아키텍처 — 프론트** | **FAIL** | 드로어 규격(폭 단일 소유·`Sheet` 격리·전체화면 판정 내장)은 **문서보다 강하게** 잠갔고 테스트로 고정했다. 그러나 **할일 응답 타입 오류로 상세 캐시가 오염된다**(FAIL-4) — TS 가 못 잡는 종류이고 그 경로가 앱 창에서 한 번도 안 돌았다 |
| **SPEC**(SPEC-003) | **FAIL** | API 12표면·Validation·Case Matrix·후보 검색(`scope`·`total`·라우트 순서·404)이 표 그대로다. 그러나 **상세에서 제목·기한·유형·프로젝트를 고칠 수 없다**(FAIL-1·2·3) — U-2 인라인 편집의 절반과 §6 Acceptance 4항목이 성립하지 않는다 |
| **WP**(WORK-004) | **FAIL** | Phase 1~5 는 체크리스트대로다(범위 밖 침범 0건 — 백 커밋은 `app/back` 만, 프론트 커밋은 `app/front` 만). **Phase 6 작업 「인라인 편집 — 제목·…」과 검증 3항목**(제목 저장 · 기한 낙관적 갱신 없음 실측 · 유형 팝오버 실패 표시)**이 미충족**이다 |

**드로어 규격 축 — PASS(이 검수의 핵심 통과).** `DrawerFrame` 이 폭을 **prop 으로 받지 않고**, `840` 리터럴이 `tokens.css` 밖에 없으며, `Sheet` import 가 그 한 파일뿐이고, 전체화면 판정(`useFullscreenDrawer`)이 프레임 안에 있다. 셋 다 **테스트로 고정**돼 있어 다음 work 가 깨면 빨간불이 뜬다(`DrawerFrame.test.tsx:34·45·54·135`). **`DrawerFooter` 포털은 구멍이 아니다** — 아래 「확인한 것」에 판정 근거를 적었다.

**완료 게이트 축 — PASS.** 서버에 상태 전이 경로가 **없고**(`TaskUpdate` 에 `status` 필드 없음 + `extra="forbid"` → 422), 화면 컨트롤 셋은 `disabled` 이며 **`onClick` 자체가 없다**. 뒷문 0건.

---

## FAIL — 반드시 고쳐야 하는 것

| # | 파일:줄 | 무엇이 어긋났나 | 어긋난 문서 절 | 어떻게 고치나 |
|---|---|---|---|---|
| **F-1** | `features/tasks/components/TaskDetailParts.tsx:30-73`(헤더에 제목 자리가 없다) · `features/tasks/openTaskDrawers.tsx:40`(`title: "업무 상세"`) · `features/tasks/components/TaskDetailPage.tsx:52`(`<h1>` 정적 텍스트) · `TaskDetailBody.tsx:45-49`(`FIELD_LABEL` 에 `title` 없음) | **상세에서 제목을 고칠 수 없다.** 인라인 편집이 붙은 곳은 배경(`TaskDetailBody.tsx:114`)·목표(`:125`)·완료 결과(`:476`) 셋뿐이고 **제목은 어디에도 편집 컨트롤이 없다.** 게다가 **드로어에는 업무 제목이 아예 표시되지 않는다** — `DrawerFrame` 헤더에 정적 문자열 「업무 상세」가 들어가고 `TaskHeaderControls` 는 배지·칩·상태·기한만 그린다. 어떤 업무를 보고 있는지가 드로어 안에서 사라진다 | **SPEC-003 U-2** 「**제목**·배경·목표·완료 결과에 적용한다」 · **U-3 문구·구성** 「헤더: … / **제목 26·700** / …」 · **§6 Acceptance** 「상세에서 **제목을 고치고** 바깥을 클릭하면 저장 버튼 없이 저장되고, 로그에는 남지 않는다」 · **S-2 2** · **WORK-004 Phase 6 작업**(「인라인 편집 — **제목**·배경·목표·완료 결과」)과 **검증 2번째 항목** | ① 드로어의 `title` 을 업무 제목으로 바꾼다 — `openTaskDetailDrawer` 는 id 만 알고 제목은 로드 후에 오므로, **제목을 헤더가 아니라 본문 최상단**(`TaskHeaderControls` 안)에 `InlineEditText`(26·700)로 두는 편이 구조에 맞는다(전체 페이지의 `<h1>` 자리와 같은 컴포넌트를 쓰면 U-4 「두 표면이 다른 규격을 갖지 않는다」도 지켜진다). ② `FIELD_LABEL` 에 `title: "제목"` 을 더해 U-7 실패 표시를 같은 규격으로 태운다. **백엔드는 이미 준비돼 있다** — `PATCH {title}` 이 동작하고 로그를 남기지 않는 것을 `test_patch_changes_only_what_was_sent_and_writes_no_log` 가 확인한다 |
| **F-2** | `features/tasks/components/TaskDetailParts.tsx:45-48`(기한이 `formatDue` 읽기 전용) · `DueDateField` 사용처가 `TaskCreateDrawer.tsx:170` **하나뿐** | **상세에서 기한을 바꿀 수 없다.** 그 결과 이 work 가 Phase 1 에서 세운 겹침·파생이 **화면 어디에서도 검증되지 않는다** — 생성 시점에만 기한을 넣을 수 있고, 만든 뒤에는 손댈 길이 없다. §6 Acceptance 의 겹침 2항목(겹치면 토스트+원복 / 경계 접촉은 저장)과 WP Phase 6 의 「낙관적 갱신을 하지 않는 것의 실측」이 **실행 불가능**하다 | **SPEC-003 S-2 4**(「상세에서 고친다」 시나리오 안) · **S-3 전체** · **§6 Acceptance** 「기한에 시간을 넣어 이미 있는 시간 일정과 겹치게 하면 저장되지 않고 … 토스트가 뜨며 값이 원복된다」·「끝시각 = 다른 일정의 시작시각이면 **저장된다**」 · **§5 낙관적 표**(「기한 변경 — 하지 않는다」) · **WORK-004 Phase 6 검증** | `TaskHeaderControls`(또는 본문 첫 블록)에 `DueDateField` 를 붙이고 `onChange` 를 `mutations.update` 로 잇는다. **부품은 전부 있다** — `DueDateField` 는 `saveFailed` prop 을 이미 받고, `errors.ts:31-33` 이 `schedule_overlap` 을 「토스트 + `field:"due"`」로 이미 분류해 두었으며 서버도 409 를 낸다. **원복은 저절로 된다**(낙관적 갱신을 안 하므로 값이 애초에 안 바뀐다). 잇는 코드만 없다 |
| **F-3** | `features/tasks/components/TaskDetailParts.tsx:33-38`(유형 배지·프로젝트 칩이 표시 전용) · `Selector` 사용처가 `TaskCreateDrawer.tsx:142·153` **둘뿐** | **상세에서 유형·프로젝트를 바꿀 수 없다.** `PATCH` 계약에 `workTypeId`·`projectId` 가 있고 서버도 받는데(`test_patch_to_a_deleted_work_type_is_rejected`·`test_patch_can_clear_the_project`) 화면에 셀렉터가 없다. 그래서 Case Matrix 의 `invalid_work_type` 행이 지정한 **표시 위치(「유형 셀렉터」)가 존재하지 않고**, WP 가 명시적으로 요구한 「팝오버형 컨트롤의 실패 표시」 검증도 돌릴 수 없다 | **SPEC-003 §4 PATCH** 「또는 background / goal / completionResult / **workTypeId / projectId**」 · **§4 Case Matrix** `invalid_work_type` 행의 표시 위치 「**유형 셀렉터**」 · **§5 낙관적 표** 「유형·프로젝트 변경 — 하지 않는다」 · **WORK-004 Phase 6 검증** 「**서버를 내린 채 유형을 바꾸면**(팝오버형 컨트롤) 트리거 테두리가 실패색이 되고 그 행 아래 인라인 자리에 「유형이 저장되지 않았습니다 · 다시 저장」이 뜬다」 | 헤더의 배지·칩을 `Selector` 로 바꾼다(값 표시는 그대로, 누르면 팝오버). 실패 배선은 F-1 과 같은 `save()`·`rowFailures` 를 재사용하면 되고 `Selector` 는 `saveFailed` prop 을 **이미 받는다**(`Selector.tsx:42·92·98`). **F-1·F-2·F-3 은 뿌리가 하나다** — 헤더가 「표시 전용」으로 굳어 편집 대상 4종이 통째로 빠졌다. 한 발주로 묶어 고치는 편이 낫다 |
| **F-4** | `features/tasks/api.ts:30`·`:34-38`(`addTodo`·`updateTodo` 를 `Promise<TaskDetail>` 로 선언) ↔ `app/back/api/task_router.py:149-153`·`:168-170`(실제 응답은 **`TodoItem`**) · 소비처 `hooks/useTaskMutations.ts:82-90` → `:46-49` `putDetail` | **할일 응답 타입이 서버와 다르고, 그 결과 상세 캐시가 오염된다.** 서버는 할일 추가·수정에 **할일 한 건**(`TodoItem`)을 돌려주는데 프론트는 이를 `TaskDetail` 로 선언하고 `putDetail(client, detail)` 로 **`['tasks','detail', <할일 id>]` 에 써 넣는다.** `apiFetch<T>` 가 `as T` 로 캐스팅만 하므로 **TypeScript 가 잡지 못한다.**<br>**재현**: 새 DB 에서 업무를 하나 만들면 `task.id = 1`, 그 업무에 할일을 하나 넣으면 `task_todo.id = 1`. 그 상세를 연 채로 할일을 **체크**하면 → `setQueryData(['tasks','detail',1], {id:1,text,done,dueDate})` 가 실행되고 → 열려 있는 `TaskDetailDrawer` 가 그 객체를 `TaskDetail` 로 렌더해 **`task.todoProgress.done` 에서 TypeError** 가 난다(뒤이은 `invalidateTask` 재조회가 오기 **전에** 한 번 렌더된다). id 가 안 겹쳐도 매 조작마다 엉뚱한 키에 쓰레기 캐시가 쌓인다 | **`frontend/README.md` §3-6** 「**`types/api.ts` 가 백엔드 schema 의 미러**이고, 여기 없는 필드를 컴포넌트가 지어내지 않는다」 · **§11** 「타입 — 백엔드 계약의 미러다. **응답 형태가 흔들리면 여기서 먼저 깨져야 한다**」 · **WORK-004 Internal Interface Contract**(캐시 키 `['tasks','detail',id]`) | 둘 중 하나. **① 서버를 맞춘다(권장)** — `POST/PATCH /{task_id}/todos` 의 `response_model` 을 `TaskDetail` 로 바꾼다. 메모·첨부·연관이 **이미 그렇게** 하고 있어 일관되고, 파생값(`todoProgress`·`dDay`)이 응답에 함께 와 화면이 다시 세지 않아도 된다. **② 프론트를 맞춘다** — `addTodo`/`updateTodo` 반환을 `TaskTodo`(이미 `types.ts:28` 에 있다)로 고치고 `onSuccess` 를 `removeTodo` 처럼 `invalidateTask(client)` 만 하게 바꾼다.<br>**함께**: `apiFetch` 가 무검증 캐스팅이라 이런 불일치가 조용히 지나간다 — 최소한 `putDetail` 에 「`detail.id` 가 기대한 taskId 와 같은가」 가드를 두면 다음번엔 즉시 드러난다. **이 경로는 앱 창에서 한 번도 돌지 않았다**(브리프 §4-1) — 테스트도 `TaskDetailBody.test.tsx` 가 `PATCH /api/tasks/{id}` 하나만 목으로 세우고 픽스처의 `todos` 가 `[]` 다 |

---

## WARN — 규약에서 벗어났으나 동작하는 것

| # | 파일:줄 | 무엇이 어긋났나 | 어긋난 문서 절 | 어떻게 고치나 |
|---|---|---|---|---|
| **W-1** | `service/task_service.py:369-383` `_resolve_due` | **기한 없는 업무에 시각만 보내면 조용히 200 이 난다.** `{"dueStartTime":"14:00","dueEndTime":"15:00"}` 만 보내면 `due_date` 가 `None` 이라 `_Due(None,None,None)` 으로 접히고, `_validate_due` 는 그 **접힌 결과**를 보므로 통과한다 → `due_changed=False` → 아무것도 안 바뀌고 **200**. 계약은 422 다. 「실패가 안 보이는」 종류라 §3 규칙 7 이 경고한 것과 같은 결 | **SPEC-003 §4 Validation** 「`dueStartTime`·`dueEndTime` — 둘 다 있거나 둘 다 없다. **있으면 `dueDate` 도 있어야** 하고 `end > start`」 · **T-1-b** | `_resolve_due` 앞에서 **요청 자체**를 먼저 검사한다 — 「보낸 시각이 있는데 최종 `due_date` 가 없으면 422」. 지금은 화면이 항상 세 값을 함께 보내(`DueDateField` 가 날짜를 지우면 시각도 함께 `null` 로 만든다) 도달하지 않지만, **F-2 를 고치면 상세에서 시각만 보내는 경로가 생긴다** |
| **W-2** | `hooks/useTaskMutations.ts:1-15`(선언) · `:82-99`(할일 체크·메모 추가) | **낙관적 갱신을 세 자리 모두 하지 않는다.** 파일이 「이 파일은 낙관적 갱신을 하지 않는다」로 선언하고 서버 응답을 캐시에 얹는 방식만 쓴다. 그런데 문서는 **할일 체크·메모 추가·인라인 텍스트는 낙관적으로 한다**로 못박았다. 체크박스가 `todo.done` 으로 제어되므로 느린 회선에서는 **눌러도 잠깐 안 눌린 채**로 있다가 응답이 와야 바뀐다 — U-5 가 「즉시」를 요구한 이유가 그것이다 | **SPEC-003 §5 낙관적 표** 「할일 체크·메모 추가·인라인 텍스트 — **한다** — 거부할 규칙이 없다」 · **U-5 기대 결과** 「체크하면 진행률이 **즉시** 바뀌고(**낙관적** — §5)」 · **WORK-004 Internal Interface Contract** 낙관적 갱신 행 | 세 자리에 `onMutate` 낙관 반영 + `onError` 롤백을 붙이거나, **문서를 바꾼다**(「응답이 상세 전체라 왕복 한 번이면 충분하다」가 사실이면 §5 표의 그 줄을 「하지 않는다」로 정정). **어느 쪽이든 지금은 코드와 문서가 어긋나 있고, WORK-005 가 이 파일을 복제한다** |
| **W-3** | `features/tasks/components/RelationPopover.tsx:90-99` | **컴포넌트가 캐시 키 배열 리터럴을 직접 만든다** — `["tasks","relationCandidates",{...}]`. 키를 만드는 곳은 `lib/api/queryKeys.ts` 하나여야 한다 | **`frontend/README.md` §3-3** 「키를 만드는 곳은 **`lib/api/queryKeys.ts` 하나**다. 컴포넌트가 배열 리터럴을 직접 쓰지 않는다」 | `queryKeys.relationCandidates(params)` 를 `queryKeys.ts` 에 추가하고 컴포넌트는 그것만 부른다. (동작은 정상이다 — `['tasks', …]` 로 시작해 `invalidateTask` 에 함께 걸린다) |
| **W-4** | `features/tasks/components/RelationPopover.tsx:190-192`(제목을 그대로 렌더) · `:121-127`(검색 입력) | **U-8 의 규격 두 가지가 빠졌다** — ① 제목의 **검색어 하이라이트 `#FFF3B0`** 가 없다(제목을 평문으로 그린다) ② 검색 입력의 **포커스 시 테두리 `#7181F8` + 3px 글로우**가 없다(기본 `Input`). SPEC §7 이 「연관업무 검색 결과 규격은 U-8 에서 확정(**하이라이트 `#FFF3B0`**·빈 결과 문구·후보 20건)」이라고 닫음 항목으로 못박은 값이다 | **SPEC-003 U-8 상태** · **§7 이 spec 이 닫은 것**(DEC-002 OQ-3 「검색 결과」) | 하이라이트는 `#FFF3B0` 토큰을 `tokens.css` 에 신설하고(컴포넌트에 hex 를 넣으면 §11 금지 4 위반) 제목을 `keyword` 로 잘라 `<mark>` 로 감싼다. 글로우는 `--tm-swatch-current-ring` 과 같은 방식으로 토큰화한다. **문서공백 G-4 와 함께** 처리 |
| **W-5** | `features/tasks/components/TaskDetailBody.tsx:206` `const now = new Date();` | **컴포넌트에서 `new Date()` 를 만든다.** 포맷 자체는 `lib/datetime.ts` 가 하지만, WP 가 「컴포넌트에서 `new Date()` 로 포맷하는 코드 **0건**」을 정적 검사 항목으로 걸어 두었고 그 검사가 실패한다 | **`frontend/README.md` §11 금지 목록 8** · **WORK-004 Phase 4 검증**(정적 검사) · **Done Criteria** 정적 검사 6종 | `formatTimestamp` 가 이미 `now` 를 기본값으로 갖는다(`datetime.ts:56`) — 인자를 빼면 끝난다. 한 렌더 안에서 기준 시각을 통일하고 싶으면 `lib/datetime.ts` 에 `nowRef()` 를 두고 그것을 부른다 |
| **W-6** | `components/ui/sheet.tsx:60-85`(`overlayClassName` prop 신설 · 생성물의 `SheetPrimitive.Close` 삭제) | **shadcn 생성물을 구조적으로 고쳤다.** 파일 머리는 「단 하나의 손댐 — 「토큰 변수 이름을 맞추는 className 조정」」이라 적었는데 실제로는 ① 스크림 className ② **prop 신설** ③ **기본 닫기 버튼 삭제** 셋이다. ②·③ 은 「className 조정」이 아니다. 같은 레포의 `ConfirmModal.tsx:61` 은 같은 문제를 **래퍼에서**(`[&>button:last-child]:hidden`) 흡수했으므로 방식이 갈렸다 | **`frontend/README.md` §2 규칙 2** 「`components/ui/` 는 shadcn CLI 가 만든 그대로 둔다. 규격 차이는 **`components/shared/` 의 래퍼에서** 흡수한다 …(예외: **토큰 변수 이름을 맞추는 `className` 조정**은 허용)」 | ③ 은 `ConfirmModal` 과 같이 래퍼에서 숨기면 되돌릴 수 있다. ② 는 오버레이가 `SheetContent` 안에서만 렌더돼 래퍼가 손댈 길이 없으므로 **규칙의 예외를 문서에 등록해야 한다**(문서공백 G-3). 최소한 **파일 머리의 「단 하나」 설명을 사실과 맞춰라** — 다음 사람이 이 파일을 「거의 생성물 그대로」로 믿는다 |
| **W-7** | `features/tasks/api.ts:141-146`(`linkRelations` → `Promise<TaskRelation[]>`) ↔ `api/task_router.py:267-269`(`response_model=TaskDetail`) | **연관 연결 응답 타입도 서버와 다르다.** 반환값을 아무도 안 써서(`onSuccess: () => invalidateTask`) 지금은 무해하지만 F-4 와 같은 종류의 거짓말이고, SPEC 은 또 다른 제3의 형태(「200 **갱신된 연관 목록**」)를 적어 두었다 — **세 곳이 서로 다르다** | **`frontend/README.md` §3-6 · §11**(미러 규칙) · **SPEC-003 §4** `POST /api/tasks/{id}/relations` 행 | 서버가 `TaskDetail` 을 주는 쪽으로 통일하고(메모·첨부와 같다) FE 타입을 `TaskDetail` 로 고친 뒤 **SPEC §4 문구도 함께** 정정한다(문서공백 G-5) |
| **W-8** | `hooks/useTaskMutations.ts:79` | **시각만 바꾸면 `['schedules']` 가 무효화되지 않는다.** `"dueDate" in variables.input` 으로만 판정하는데, 날짜는 그대로 두고 `dueStartTime`/`dueEndTime` 만 보내면 `schedule` 행은 **종일 → 시간 일정**으로 바뀌는데 무효화가 안 나간다 | **`frontend/README.md` §3-3 무효화 표** 「업무 생성·수정·상태·삭제 → `['tasks', …]` 전부 + **기한이 바뀌었으면 `['schedules']`**」 · **WORK-004 Internal Interface Contract** 캐시 키 행 | 판정을 `"dueDate" in input \|\| "dueStartTime" in input \|\| "dueEndTime" in input` 으로 넓힌다. **지금은 읽는 화면이 없어 no-op** 이지만 캘린더 work 가 그대로 물려받는다 |
| **W-9** | `features/tasks/components/TaskDetailBody.tsx:448`(`id="task-completion-card"` 뿐) | **게이트 유도 진입 훅이 「노출」되지 않았다.** WP 는 「스크롤 + 포커스 + 1.5초 강조를 **WORK-005 가 부를 수 있게 노출**」하라고 했는데 실제로는 **DOM id 하나**뿐이다 — 스크롤 대상 ref 도, 완료 결과 입력에 포커스를 주는 길도, 1.5초 강조 상태도 없다. WORK-005 가 그 셋을 직접 만들면 규격이 그쪽에서 정해진다 | **SPEC-003 U-6 상태** 「*게이트 유도 진입*: … 이 카드로 스크롤하고 **완료 결과 입력에 포커스**가 잡힌다. 카드 테두리가 **1.5초 동안** `#7181F8`」 · **WORK-004 Phase 6 작업** | `useCompletionCardFocus()` 같은 훅(또는 `imperativeHandle`)을 `features/tasks` 에서 내보내고 그 안에 스크롤·포커스·1.5초 클래스 토글을 담는다. **id 만으로는 「자리」이지 「훅」이 아니다** |
| **W-10** | `service/task_service.py:570-577` `unlink_relation` | 없는 연관을 해제해도 **204** 다(삭제문이 0행을 지우고 끝난다). 이 spec 의 Case Matrix 는 「없는 항목 → 404」를 원칙으로 두는데 이 표면만 예외다 | **SPEC-003 §4 Case Matrix** `not_found` 행 · **§5** 「소유 검사가 먼저다. 남의 업무는 404」 | 멱등을 의도한 것이면(로그아웃과 같은 결) **그 사실을 SPEC 에 한 줄 적어라**(문서공백 G-6). 아니면 대상 유무를 확인해 404 를 낸다. **판정 보류가 아니라 문서가 안 정한 쪽에 가깝다** — 지적 강도를 낮춰 둔다 |

---

## 문서 공백 — 코드가 아니라 문서를 고쳐야 하는 것

| # | 무엇이 비었나 | 어느 문서 어느 절 | 무엇을 적어야 하나 |
|---|---|---|---|
| **G-1** | **`invalid_work_type` 코드가 §8-2 표에 없다**(SPEC-003 S003-OQ-2). 배치 ①·②의 `duplicate_name`·`invalid_color_token`·`not_found` 와 **같은 미결이 세 번째로 쌓였다** — 표가 계속 뒤처진다 | **`backend/README.md` §8-2** 코드 표 | 한 번에 네 개를 더한다 — `invalid_work_type` \| 422 \| 유형이 없거나 삭제됐거나 남의 것 \| SPEC-003 §4 (+ WORK-003 검수 G-1 의 세 개). **그리고 표 머리에 「spec 이 새 코드를 정하면 그 work 의 검수에서 이 표에 반영한다」를 적어 절차로 만들어라** — 지금은 매 검수가 같은 공백을 다시 올린다 |
| **G-2** | **프로젝트가 삭제됐을 때의 코드가 없다.** `_require_usable_project`(`task_service.py:139-153`)가 「Case Matrix 에 프로젝트 전용 코드가 없어 `validation_error` 로 낸다 — 코드를 발명하지 않는다」라고 적고 그렇게 했다. **판정: 발명하지 않은 것이 옳다.** 다만 화면은 유형(`invalid_work_type`)과 프로젝트를 **구분할 수 없다** | **SPEC-003 §4 Case Matrix** | 둘 중 하나를 적는다 — ① `invalid_project`(422) 행 신설, 프론트 표시 위치는 「프로젝트 셀렉터」 ② 또는 「프로젝트는 `validation_error` 로 합류한다 — 유형과 달리 필수가 아니라 셀렉터를 비우면 되기 때문」이라고 명시. **F-3 을 고치면 화면에 셀렉터가 생기므로 그 전에 정해야 한다** |
| **G-3** | **`components/ui/` 예외 범위가 「className 조정」뿐이라 오버레이에 손댈 근거가 없다.** shadcn `SheetContent` 는 오버레이를 자기 안에서 렌더해 래퍼가 스크림을 끌 길이 없는데, SPEC-003 U-11 은 전체화면에서 **스크림을 걷으라**고 한다. 워커는 prop 하나를 신설해 풀었다(W-6) | **`frontend/README.md` §2 규칙 2** 괄호 안 예외 | 예외를 하나 더 등록한다 — 「**생성물이 내부에서만 렌더하는 요소**(예: `Sheet` 의 오버레이)에 규격을 적용해야 하면 **통로 prop 하나**를 더하는 것까지 허용한다. 값은 여전히 `components/shared/` 가 정한다」. 함께: 생성물의 **기본 닫기 버튼**을 지울지 래퍼에서 숨길지도 한 줄로 통일해라(지금 `dialog` 는 숨기고 `sheet` 는 지웠다) |
| **G-4** | **연관업무 하이라이트 색 `#FFF3B0` 과 검색 입력 포커스 글로우에 토큰이 없다.** SPEC-003 U-8 이 값을 직접 적었는데 `09-design-tokens.md` §색에 그 자리가 없어 구현이 통째로 빠졌다(W-4) | **`00-design/09-design-tokens.md` §색** | 「**검색어 하이라이트** `#FFF3B0`」을 §색에 등록한다. 포커스 글로우는 WORK-003 이 만든 `--tm-swatch-current-ring` 과 **같은 값·같은 규격**이므로 「입력 포커스 글로우」로 이름을 일반화해 재사용하도록 적어라 — 지금처럼 두면 화면마다 새 hex 가 생긴다 |
| **G-5** | **자식 컬렉션 응답 형태가 SPEC 에 통일돼 있지 않다.** `POST /relations` 만 「**갱신된 연관 목록**」이라 적혀 있고 메모·첨부·할일은 응답 형태를 안 적었다. 구현은 넷 중 셋이 `TaskDetail`, 할일만 `TodoItem` 이다(F-4·W-7 의 뿌리) | **SPEC-003 §4 Request / Response** 자식 컬렉션 절 | 한 문장으로 못박아라 — 「**자식 컬렉션의 쓰기 표면은 전부 갱신된 `TaskDetail` 을 돌려준다**(로그·진행률·파생값이 함께 바뀌므로 부분 응답은 화면이 다시 조립해야 한다). 삭제만 204」. 그러면 F-4·W-7 이 「구현이 문서를 어긴 것」으로 명확해지고 WORK-005 이후가 같은 실수를 안 한다 |
| **G-6** | **없는 자식을 지우는 요청의 응답이 정해져 있지 않다.** 할일·첨부는 404 를 내고(`task_service.py:476-481`·`:528-541`) 연관 해제는 204 를 낸다(W-10). 셋 다 「이미 없는 것을 지운다」인데 답이 다르다 | **SPEC-003 §4 Case Matrix** | 「**멱등 삭제**(이미 없어도 204)인가 **404** 인가」를 자식 3종에 대해 한 줄로 정해라. SPEC-001 이 로그아웃을 「이미 무효여도 성공」으로 정한 전례가 있으니 그 결을 따를지도 함께 적으면 이후 work 가 안 헤맨다 |
| **G-7** | **첨부 「자료함 문서」 갈래가 SPEC 계약과 일시적으로 어긋난다** — 서버가 `kind='doc'` 을 `validation_error` 로 거부하고(`task_service.py:163-164`), 팝오버는 「자료함이 아직 없습니다」 스텁이다. **WP Open Issues 가 이미 「코디 확인이 필요하다」로 올려 둔 사안**이고 구현은 그 임시 계약을 정확히 따랐다 | **WORK-004 §Open Issues** · **SPEC-003 §4 Validation**(첨부 `kind=doc` 행) · **§6 Acceptance**(「첨부한 문서를 누르면 문서함 상세로」) | **판정: 코드가 임시 계약대로다. 문서 쪽에 기한을 박아라.** ① SPEC-003 §4 에 「`kind=doc` 은 **문서함 work 전까지 422** 다」를 각주로 달고 ② Done Criteria 의 Acceptance 이월 1건을 **문서함 work 의 검증 절에 복사**해 넣어라(WORK-003 검수 G-6 과 같은 처방 — 안 옮기면 아무도 안 본 채 닫힌다). ③ 거부 코드가 `validation_error` 인데 Case Matrix 에는 `unsupported_file_type` 이 있다 — 어느 쪽인지 정해라 |

---

## 확인한 것 (PASS 근거)

**범위 산정** — `git diff 5bfe012...HEAD --stat`(57파일) + `git log`(5커밋) + `git status --porcelain`(무출력). 커밋별 `--name-only`: `aec6222`·`70924d7`·`9897ff5` 는 `app/back/**` 만, `7550e1b`·`99a45e7` 는 `app/front/**` 만. **백↔프론트 교차 0건.**

**드로어 규격**(이 검수의 핵심)
- **폭이 한 곳에서만 정해진다** — `DrawerFrame.tsx:110-113` 이 유일한 자리이고, `840` 리터럴은 `tokens.css:86`(`--tm-drawer-width`)뿐이다. `DrawerFrameProps`(`:56-66`)에 `width`·`size`·`className` 이 **없다**. `DrawerRequest`(`OverlayProvider.tsx:16-24`)에도 없다.
- **`Sheet` import 는 `DrawerFrame.tsx:33` 하나**(`ConfirmModal` 의 `Dialog` 는 모달 쪽 규격 소유자로 별개).
- **전체화면 판정이 프레임 안**(`useFullscreenDrawer`, `:43-54`) — 호출부가 폭을 재는 코드 0건. 경계 `FULLSCREEN_BELOW = 1440` 이 §7-1 세 구간(<1280 은 `MinWidthGuard` 가 덮는다)과 맞다.
- 헤더 72 / 전체화면 74(`:117-122`) · 푸터 76(`:173-176`) · `Esc`·스크림(`:97-102`)·×(`:156-165`) 셋 다 닫힌다 · 전체화면에서는 스크림을 걷고 좌측 `←` 가 닫는 길(`:114-134`) · `expandTo` 는 `onClose()` 후 `router.push`(`:85-92` — **승격은 한 방향**).
- **네 가지가 전부 테스트로 고정돼 있다** — `DrawerFrame.test.tsx:34`(Sheet 격리) `:45`(폭 리터럴 격리) `:54`(폭 prop 부재) `:135`(판정이 프레임 안).
- **`DrawerFooter` 포털 판정 — 구멍이 아니다.** 포털 대상은 `DrawerFrame` 이 직접 그린 `<footer className="h-[76px] … border-t px-6 empty:hidden">`(`:173-176`)이고, 자식은 **그 안의 내용만** 넣는다 — 높이·구분선·패딩·정렬을 바깥에서 바꿀 길이 없다. 폭·레이아웃 소유권은 프레임에 그대로 있다. 이 장치가 푼 문제도 실재한다(오버레이 스택이 `content` 를 스냅숏으로 들어 상태를 가진 폼의 CTA 가 폼 안에 살아야 한다 — `TaskCreateDrawer.tsx:302-310`). **판정: 승인.**

**완료 게이트가 아직 붙지 않았다**(정답 상태)
- 서버에 **상태 전이 표면이 없다** — `task_router.py` 에 `/status` 라우트 0건이고 `test_there_is_no_status_transition_or_schedule_surface` 가 그것을 고정한다.
- **본체 PATCH 로 상태를 바꿀 수 없다** — `TaskUpdate`(`schemas/task.py:160-202`)에 `status`·`cancelReason` 필드가 없고 `_TaskRequest` 가 `extra="forbid"`(`:62`)라 보내면 **422 validation_error** 다(`test_patch_rejects_status`). `_changed_columns`(`task_service.py:386-408`)가 만드는 컬럼 목록에도 `status` 가 없다. **뒷문 0건.**
- 화면 셋(`TaskDetailParts.tsx:56-71`)은 `disabled` 이고 **`onClick` 자체가 없다** — 눌러도 요청이 나갈 코드가 존재하지 않는다. `TaskDetailBody.test.tsx:137` 이 「상태를 바꾸는 컨트롤이 본문에 없다」를 고정한다.
- **숨기지 않았다** — 「상태 변경」·「완료 처리」·`⋯` 가 그대로 그려지고 `title="다음 배치에서 연결됩니다"` 가 붙는다.

**연관업무 후보 표면**
- **표면이 하나뿐이다** — `GET /api/tasks/relations/candidates` 만 있고 옛 `/{task_id}/relations/candidates` 는 없다(`test_the_old_per_task_candidates_route_is_gone`).
- **라우트 선언 순서** — `list_relation_candidates` 가 `task_router.py:48` 로 `GET /{task_id}`(`:121`)보다 **앞**이고, 그 사실을 `test_the_candidates_route_is_matched_before_the_task_id_route` 가 고정한다.
- **`Query(alias=...)` 가 넷 다 붙어 있다** — `excludeId`(`:57`)·`projectId`(`:58`)·`dueDate`(`:59`)·`scope`(`:61-63`). `keyword`(`:56`)는 camel==snake 라 alias 가 필요 없다(§3 규칙 7). 프론트가 보내는 키(`api.ts` `search.set("excludeId"…)`)와 정확히 일치한다.
- **`scope` 가 자르는 필터다** — `_resolve_scope`(`task_service.py:638-652`)가 `project`→`Task.project_id == …`, `recent30`→`Task.updated_at >= now-30d`, `all`→조건 없음으로 풀고 `_candidate_filters`(`task_repository.py:163-187`)가 **총계·목록 두 쿼리에 같은 조건**을 건다. 세 값이 실제로 다른 결과를 낸다(`test_scope_project_keeps_only_the_same_project` · `test_scope_all_returns_more_than_scope_project` · `test_scope_recent30_drops_tasks_untouched_for_over_a_month`).
- **기준 프로젝트가 없으면 `project` 가 `all` 처럼 답한다** — `_resolve_scope` 가 `project_id=None` 을 그대로 넘겨 그 축으로 자르지 않는다(`test_scope_project_without_a_reference_behaves_like_all` · `…without_any_hint…`). **화면도 이중 방어** — `RelationPopover.tsx:134` 가 「이 프로젝트」 칩을 비활성으로 내리고 `:72·78-88` 이 기본 선택을 「전체」로 내린다(그리고 폼에서 프로젝트가 생기면 되돌린다).
- **`total` 이 `len(items)` 가 아니다** — `count_relation_candidates`(`task_repository.py:190-217`)가 별도 count 쿼리다. `test_total_is_not_the_page_size_when_there_are_more_than_twenty` · `test_total_follows_the_scope_not_the_whole_table` · `test_total_respects_keyword_and_exclusions` 셋이 고정한다. 프론트도 `api.ts` 가 「`total` 을 `items.length` 로 대신하지 않는다」를 지키고 `RelationPopover.test.tsx:111` 이 그것을 본다.
- **`excludeId` 가 남의 것·없는 것이면 404** — `list_relation_candidates`(`task_service.py:606-612`)가 `_require_task` 를 먼저 태운다(`test_exclude_id_of_another_account_is_404` · `test_exclude_id_that_does_not_exist_is_404`). 403 이 아니다.
- 정렬은 **같은 프로젝트(0) → 기한 ±7일(1) → 그 밖(2)**, 그 안에서 최근 수정순(`task_repository.py:250-271`). `exclude_id` 가 있으면 **그 업무의 값이 쿼리 힌트를 이긴다**(`task_service.py:609-610` · `test_exclude_id_wins_over_the_query_sort_hints`).

**아키텍처 — 백엔드**(정적 검사)
- `except Exception`/bare `except` **0건** · `.commit()` 은 `api/deps.py:40,42`(요청 경계)와 `seed/seed.py:132` 뿐 · service·repository 에서 `fastapi`·`schemas` import **0건** · `from models` 가 `repository/`·`models/`·`alembic/`·`seed/`·`tests/` 밖에 **0건** · repository 가 ORM 모델을 반환하는 함수 **0건**(전부 `_row_to_dto`/`_to_dto` 를 지난다).
- **`persist_changes` 를 새로 켠 예외가 없다** — 여전히 `RefreshTokenReuseError` 하나(`core/exceptions.py:44`). 이 work 가 만든 `ConflictError`(겹침)·`ValidationError`·`NotFoundError` 는 전부 기본 False(=롤백)다(§7).
- **SCH-1 격리** — `schedule_repository` 를 import 하는 곳이 `service/schedule_service.py` **하나뿐**(grep). 겹침 검사와 파생이 둘 다 그 파일에 있다.
- **생성이 한 트랜잭션** — `create_task`(`task_service.py:241-315`)가 검증 → **겹침 검사(원본 쓰기 전)** → 본체 → 자식(할일·첨부·연관) → 로그 → 일정 파생을 한 세션에서 하고, 중간에 예외가 나면 `get_db` 가 통째로 롤백한다. `test_a_bad_child_prevents_the_whole_task` · `test_a_doc_attachment_in_creation_blocks_the_whole_task` 가 「본체도 안 만들어진다」를 확인한다.
- **겹침이 원본을 못 바꾸게 한다** — `update_task:348-355` 가 쓰기 **전에** 검사하고, `test_an_overlapping_due_time_is_409_and_nothing_is_written` 이 DB 행까지 확인한다. 판정식 `start_at < :end AND end_at > :start`(`schedule_repository.py:60-63`)라 **경계 접촉은 통과**(`test_a_touching_boundary_is_saved` · `test_touching_boundaries_are_not_an_overlap`). 종일·취소·소프트딜리트 원본은 검사에서 빠진다(`_inactive_task_source`).
- **소프트 딜리트** — `find_active` 계열이 전부 `deleted_at IS NULL` 로 좁히고, 삭제분은 후보에서도 빠진다(`test_candidates_never_include_another_account_or_deleted_tasks`). 행은 남는다(`test_a_soft_deleted_task_is_404_but_the_row_survives`). **복원 표면 0건.**
- **참조 표시(A-6)** — `_with_refs`(`task_repository.py:60-82`)가 유형·프로젝트를 **삭제 여부로 거르지 않고** 조인해 `isDeleted` 로 실어 보낸다(`test_a_deleted_work_type_still_shows_its_name_and_color`).
- **남의 업무는 404**(403 아님) — `find_active` 가 남의 것과 없는 것을 똑같이 `None` 으로 돌린다(`test_another_accounts_task_is_404` · 자식 표면도 `test_another_accounts_todo_is_404` · `test_a_todo_of_another_task_is_404`).
- **로그가 남는 자리와 안 남는 자리** — 쓰는 곳은 `task_service` 하나. 생성·할일 완료·첨부·연관 연결에만 남고 **본체 PATCH·메모 등록에는 안 남는다**(`test_patch_changes_only_what_was_sent_and_writes_no_log` · `test_a_memo_is_registered_without_a_log` · `test_a_todo_text_can_be_edited_without_a_log`). 되돌려도 로그는 안 지워진다(`test_unchecking_lowers_the_progress_but_keeps_the_log`), 재완료해도 안 늘어난다(`test_recompleting_the_same_todo_does_not_duplicate_the_log`).
- **연관은 무방향 1행 · 양방향** — `create_relations` 가 `low<high` 로 정규화하고 이미 있는 쌍을 건너뛴다, `list_related_ids` 가 **두 컬럼을 모두** 본다(`test_relations_are_bidirectional` · `test_relinking_the_same_pair_does_not_grow` · `test_the_reverse_direction_is_also_deduplicated`). 자기 자신·남의 업무는 422.
- 테스트 총량: `test_task.py` 27 · `test_task_children.py` 45 · `test_schedule_derive.py` 23 ≈ **95건**. BE §12 필수 3·5·5-a·9 가 전부 있다(겹침 / 파생 / **`schedule` 조인 없는 정렬** / **고아 없음**).

**아키텍처 — 프론트**(정적 검사)
- 동적 세그먼트 **0개**(상세는 `/tasks/detail/?id=` — `openTaskDrawers.tsx:42`) · `app/api/**` 없음 · `middleware.ts` 없음 · Server Action 없음 · 모든 `page.tsx` 7개에 `'use client'`. `useSearchParams` 는 `Suspense` 로 감쌌다(`detail/page.tsx:16`) — 정적 빌드 규약.
- **쿼리 파싱은 영역 훅 하나**(`useTasksViewParams.ts`) · 전역 상태 라이브러리 **0건** · `retry:false` 전역 유지 · 직접 `fetch` **0건**.
- **컴포넌트 hex 리터럴 0건**(styles 제외 grep 무출력) · **색을 인라인 `style` 로 넣은 곳 0건**(유일한 인라인 `style` 은 `ProgressBar.tsx:40` 의 `width: ${ratio}%` 로, 런타임 비율이라 Tailwind 클래스로 만들 수 없고 §11 금지 4 는 **색 hex** 를 대상으로 한다 — 위반 아님).
- **드로어와 전체 페이지가 같은 본문을 쓴다** — `TaskDetailBody`/`TaskMainBlocks`/`TaskAsideBlocks` 하나이고, 두 표면의 차이는 **감싸는 껍데기와 ⑤⑥ 의 배치뿐**이다(`TaskDetailDrawer.tsx:38-43` ↔ `TaskDetailPage.tsx:56-63`). 본문은 부모를 모른다.
- **U-7 자동 저장 실패가 WORK-003 규격 그대로다** — `saveFailed`·`onRetry` 가 **prop** 이고 소유자는 블록(`TaskDetailBody.tsx:72·96-107`), 표시는 공용 `AutoSaveFailureNotice` 를 재사용한다. **업무에서 새로 만들지 않았다.** `TaskDetailBody.test.tsx:85·100·112` 가 「토스트와 인라인이 **함께**」·「자동 재시도 없음」·「「다시 저장」은 정확히 1건」을 고정한다 — WORK-003 검수 F-1 이 지적한 구멍이 닫혔다.
- **파생값을 화면이 다시 계산하지 않는다** — `dDay`·`isOverdue`·`todoProgress` 를 서버 값 그대로 그린다.
- 생성 드로어(U-1) — 열자마자 제목 포커스(`TaskCreateDrawer.tsx:68-70`) · 제출 조건 「제목 1자 + 유형 선택」(`:73`) · 제출 중 비활성 · **상태 필드 없음** · **「임시저장」 배지 없음** · 실패 시 **드로어가 닫히지 않고 입력이 남는다**(`:110-121`) · 블록 6 순서와 ⑥⑦ 안내 문구가 U-1 그대로 · 첨부 팝오버 문서 갈래는 「자료함이 아직 없습니다」 스텁(`AttachmentPopover.tsx:97-102`) · `Selector` 프로젝트 갈래에 「+ 새 프로젝트」 인라인 행(WORK-003 팔레트 재사용).
- 상세 — 로딩 스켈레톤(애니메이션 없음) · 「없는 업무입니다」 + 「목록으로」로 **리다이렉트하지 않는다**(`TaskDetailPage.tsx:69-79`) · 기한 없으면 「기한 없음」 · 연관은 최근 5 + 「전체 n 보기」 · 메모는 등록만(수정·삭제 표면 없음) · 로그 최신 1건만 dot 강조.
- 임시 진입(`TasksEntryScreen`)은 **리스트·칸반·상태 UI 를 만들지 않았다** — WORK-005 범위 선점 0건.

---

## 확인 못 함 (추측으로 PASS 주지 않는다)

| # | 무엇 | 왜 못 했나 |
|---|---|---|
| **U-1** | **`pytest` 95건이 실제로 통과하는지** | read-only 라 실행하지 않았다. 코드를 읽어 판단한 범위에서는 통과할 형태다 |
| **U-2** | **`npm run test`(FE 테스트)·`typecheck`·`build` 결과** | 같은 이유. 특히 **FAIL-4 는 `typecheck` 를 통과한다**(`apiFetch<T>` 가 `as T` 로 캐스팅한다) — 빌드가 녹색이어도 그 결함은 그대로다 |
| **U-3** | **드로어 안 「할일 추가」·체크의 실제 화면 동작** | 브리프 §4-1 이 밝힌 대로 워커도 실측하지 못했고, 검수도 코드로만 봤다. **FAIL-4 가 정확히 그 경로에 있다** — 사람 손으로 「업무 생성 → 상세 열기 → 할일 추가 → 체크」를 한 번 밟아 확인이 필요하다(재현 절차는 FAIL-4 에 적었다) |
| **U-4** | **1280~1439 전체화면 전환의 실제 렌더**(스크림이 걷히는지·`←` 가 보이는지) | 컴포넌트 테스트(`DrawerFrame.test.tsx:120`)가 `window.innerWidth` 를 바꿔 확인하지만 **실제 레이아웃(2열→1열 쌓임 포함)은 창에서 봐야 한다** |
| **U-5** | **마이그레이션 `0002_task_domain` 의 `downgrade` 왕복**(WP Phase 1 검증) | DB 를 건드리지 않았다. 파일에 `downgrade` 가 있는 것은 확인했으나 왕복 실행은 코디 몫 |

---

## 코디 실행 요청

1. **`cd app/back && uv run pytest`** — 95건 통과 확인(U-1). 특히 `test_there_is_no_status_transition_or_schedule_surface`·`test_the_old_per_task_candidates_route_is_gone` 두 개가 이 work 의 「만들지 않았다」를 지키는 자물쇠다.
2. **`cd app/front && npm run test && npm run typecheck && npm run build`** — U-2. **FAIL-4 는 여기서 안 잡힌다**는 것을 전제로 결과를 읽어라.
3. **FAIL-4 앱 창 재현**(5분, 최우선): 새 DB 에서 업무 1건 생성 → 상세 드로어 열기 → 할일 추가 → **체크**. 화면이 깨지거나(id 충돌 시) 콘솔에 TypeError 가 나면 확정이다. 안 깨져도 React Query devtools 에서 `['tasks','detail',<할일 id>]` 키가 생기는 것으로 확인된다.
4. **`make migrate` → `alembic downgrade -1` → `upgrade head`** 왕복(U-5).
5. **재발주 묶음 제안** — **F-1·F-2·F-3 은 한 발주**(상세 헤더를 「표시 전용」에서 「편집 가능」으로 바꾸는 한 가지 일이고 `Selector`·`DueDateField`·`InlineEditText`·`saveFailed` 부품이 전부 이미 있다), **F-4 는 별도 발주**(백엔드 `response_model` 통일 + 프론트 타입 정정 — G-5 결정이 선행돼야 한다). W-1 은 F-2 와 함께 고쳐라(F-2 를 붙이면 W-1 이 도달 가능해진다).
6. **문서 수정 우선순위**: **G-5**(자식 응답 형태 통일 — F-4·W-7 의 판단 근거) → **G-1**(§8-2 표, 세 work 연속 미결) → **G-2**(F-3 착수 전 필요) → G-7(문서함 이월 기한) → 나머지.

---

## 자기 점검

- [x] **네 층 전부에 판정을 냈다** — 정책 PASS / 아키텍처-백 PASS / 아키텍처-프론트 FAIL / SPEC FAIL / WP FAIL (+ 드로어 규격·완료 게이트 두 축 별도 총평).
- [x] **모든 FAIL·WARN 에 파일:줄 + 어긋난 문서 절이 붙었다** — FAIL 4건, WARN 10건 전부. 재현 가능한 것(F-4)에는 재현 절차를 적었다.
- [x] **문서 공백을 지적과 분리했다** — 별도 절 7건. 그중 G-7 은 「코드가 임시 계약대로다」로 **판정을 명시**했고, G-1 은 세 work 연속으로 같은 공백이 쌓이는 것을 절차 문제로 올렸다.
- [x] **판정 못 한 것을 「확인 못 함」으로 적었다** — 5건. 실행이 필요한 것은 코디 실행 요청으로 넘겼고, **추측으로 PASS 를 주지 않았다**(특히 U-3 은 브리프가 미결로 넘긴 항목이고 거기서 FAIL-4 를 코드로 찾아냈다).
- [x] **코드·문서를 하나도 고치지 않았다** — `git status --porcelain` 무출력. 리포트는 문서 레포의 `orchestration/work/docs-v1/` 에만 썼다. 테스트·빌드·마이그레이션을 돌리지 않았다.
- [x] **취향으로 지적하지 않았다** — 규약에 조문이 없는 것(`ProgressBar` 의 인라인 width, `ilike` 의 `%` 미이스케이프, `unlink_relation` 의 소유 재검증, 후보 목록에 완료·취소 업무가 섞이는 것)은 제외했다. WORK-005 이후의 미구현(리스트·칸반·상태 전이·삭제)을 FAIL 로 잡지 않았고, WORK-001~003 커밋은 다시 보지 않았다.
