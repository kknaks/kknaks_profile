# [frontend] WORK-004 검수 수정 — 상세 헤더 편집 4종 · 캐시 오염 · WARN 7건

너는 **task-management `frontend` 워커**다. 먼저 역할 문서를 읽어라 (**문서 레포 절대경로 — read-only**):

- `/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/orchestration/roles/task-management/frontend/role.md`

작업 워크트리: `/Users/kknaks/orca/workspaces/task_management/docs-v1`
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

**WORK-004 가 검수에서 FAIL 4 · WARN 10 을 받았다.**
**드로어 규격은 네 개 항목 전부 통과했다** — 폭 prop 부재·840 격리·`Sheet` import 단일·전체화면 판정 내장.
`DrawerFooter` 포털도 구멍이 아니라고 판정됐다. **그 부분은 건드리지 마라.**

## 1. SSOT — 먼저 읽을 것

**검수 리포트 — 이번 작업의 출발점**
- `orchestration/work/docs-v1/work-004-review-report.md`
  — **F-1·F-2·F-3·F-4 행과 W-2~W-9 행을 그대로 읽어라.** 무엇이 어긋났고 어떻게 고치라는지가 거기 있다.
  **부품이 이미 있다는 것까지 파일:줄로 적혀 있다** — 새로 만들지 말고 잇기부터 확인해라

**계약(2026-09-06 갱신 — 갱신분이 이번 수정의 근거다)**
- `para/projects/summer-star/task-management/20-spec/spec-003-tasks-crud.md`
  — **U-2·U-3·U-4**(인라인 편집 대상 4종·헤더 구성) · **§4 자식 컬렉션 응답 절**(신설) · **Case Matrix**(`invalid_project` 신설) · **§5 낙관적 표** · **U-8**(하이라이트·글로우)
- `.../40-architecture/frontend/README.md` — **§2 규칙 2**(2026-09-06 예외 둘째 신설) · §3-3(캐시 키·무효화) · §3-6·§11(타입 미러)
- `.../00-design/09-design-tokens.md` — **§색에 검색어 하이라이트·입력 포커스 글로우 등재됨**(신설)

## 2. FAIL — 반드시 고칠 것

### F-1·F-2·F-3 — 상세 헤더가 표시 전용으로 굳었다 **(뿌리가 하나다. 묶어서 고쳐라)**

**상세에서 제목·기한·유형·프로젝트를 하나도 고칠 수 없다.** 인라인 편집이 붙은 곳은 배경·목표·완료 결과 셋뿐이다.
게다가 **드로어에는 업무 제목이 아예 안 보인다** — `DrawerFrame` 헤더에 정적 문자열 「업무 상세」가 들어간다.
**어떤 업무를 보고 있는지가 드로어 안에서 사라진다.**

이 때문에 **SPEC §6 Acceptance 4항목과 WP Phase 6 검증 3항목이 실행 자체가 불가능**하다.
특히 **F-2 를 고치기 전엔 이 work 가 Phase 1 에서 세운 겹침 차단·기한 파생이 화면 어디에서도 검증되지 않는다.**

**부품은 전부 있다** — `Selector`·`DueDateField`·`InlineEditText` 가 이미 `saveFailed` prop 을 받고,
`errors.ts` 가 `schedule_overlap` 을 「토스트 + `field:"due"`」로 이미 분류해 뒀다. **잇는 코드만 없다.**

- **제목**은 헤더가 아니라 **본문 최상단**(`TaskHeaderControls` 안)에 `InlineEditText`(26·700)로 둔다 —
  `openTaskDetailDrawer` 는 id 만 알고 제목은 로드 후에 오기 때문이다.
  **전체 페이지의 `<h1>` 자리와 같은 컴포넌트를 써라** — U-4 「두 표면이 다른 규격을 갖지 않는다」
- `FIELD_LABEL` 에 `title: "제목"` 을 더해 **U-7 실패 표시를 같은 규격으로** 태운다
- 기한은 `DueDateField` 를 붙이고 `onChange` 를 `mutations.update` 로 잇는다.
  **원복은 저절로 된다** — 낙관적 갱신을 안 하므로 값이 애초에 안 바뀐다
- 유형·프로젝트 배지/칩을 `Selector` 로 바꾼다(값 표시는 그대로, 누르면 팝오버)
- **`invalid_project`(422) 가 신설됐다** — 프로젝트 셀렉터 옆 인라인 「삭제된 프로젝트입니다. 다시 골라 주세요」.
  유형(`invalid_work_type`)과 **분기를 갈라라**. 코드를 나눈 이유가 셀렉터가 둘이라서다

### F-4 — 할일 응답 타입이 서버와 다르고 상세 캐시가 오염된다

`addTodo`·`updateTodo` 를 `Promise<TaskDetail>` 로 선언했는데 **서버는 `TodoItem` 을 준다.**
그걸 `putDetail` 로 **`['tasks','detail', <할일 id>]`** 에 써 넣는다 — `apiFetch<T>` 가 `as T` 캐스팅이라
**타입 검사가 못 잡는다.** 새 DB 에서 `task.id=1`·`todo.id=1` 이 겹치면 **TypeError** 가 난다.

**SPEC 을 갱신했다** — 「자식 컬렉션의 쓰기 표면은 전부 갱신된 `TaskDetail` 을 돌려준다. 삭제만 204」.
**백엔드 워커가 지금 같은 워크트리에서 서버를 그 계약에 맞추는 중이다.**

- 네 타입 선언은 **`TaskDetail` 로 두는 게 맞다** — 서버가 그렇게 바뀐다. 붙는 대로 실물로 확인해라
- **`W-7` 도 같다**: `linkRelations` 반환을 `TaskDetail` 로 고쳐라(서버는 이미 그렇게 준다)
- **함께 고쳐라**: `putDetail` 에 「`detail.id` 가 기대한 `taskId` 와 같은가」 가드를 둬라.
  `apiFetch` 가 무검증 캐스팅이라 **이런 불일치가 조용히 지나간다** — 가드가 있으면 다음번엔 즉시 드러난다

## 3. WARN — 함께 고칠 것 7건

- **W-2 낙관적 갱신 3자리** — **문서대로 구현해라**(코드를 문서에 맞춘다).
  SPEC §5 표가 「할일 체크·메모 추가·인라인 텍스트 — **한다** — 거부할 규칙이 없다」이고 U-5 가 「**즉시**」를 요구한다.
  **거부할 서버 규칙이 없는 셋이라 롤백이 단순하다**(상태 전이는 게이트가 거부할 수 있어 낙관적으로 하지 않는다 —
  그 구분이 §5 표의 요점이다). `onMutate` 낙관 반영 + `onError` 롤백을 붙이고,
  **롤백 시 U-7 실패 표시가 그대로 뜨는지** 확인해라. **WORK-005 가 이 파일을 복제한다**
- **W-3** 컴포넌트가 캐시 키 배열 리터럴을 만든다 → `queryKeys.relationCandidates(params)` 를 `queryKeys.ts` 에 추가
- **W-4** U-8 규격 둘 누락 → 제목의 **검색어 하이라이트 `#FFF3B0`**(토큰 신설됨 — `tokens.css` 에 올리고 `<mark>`)
  + 검색 입력 **포커스 글로우**. **글로우는 새 값이 아니라 `--tm-swatch-current-ring` 과 같은 값·같은 규격**이니
  이름을 일반화해 **재사용해라**(디자인 토큰 §색에 그렇게 등재했다)
- **W-5** `TaskDetailBody.tsx:206` 의 `new Date()` → `formatTimestamp` 가 이미 `now` 기본값을 갖는다. 인자를 빼라
- **W-6** `sheet.tsx` — **아키텍처 §2 규칙 2 에 예외를 신설했다**(생성물이 내부에서만 렌더하는 요소는 통로 prop 하나 허용).
  **`overlayClassName` prop 은 그대로 둬도 된다.** 대신 ① **기본 닫기 버튼은 지우지 말고 래퍼에서 숨겨라**
  (`ConfirmModal.tsx:61` 과 같은 방식 — 지우면 재생성 때 되살아나 조용히 두 개가 된다)
  ② **파일 머리의 「단 하나의 손댐」 설명을 사실과 맞춰라**
- **W-8** 시각만 바꾸면 `['schedules']` 무효화가 안 나간다 → 판정을
  `"dueDate" in input || "dueStartTime" in input || "dueEndTime" in input` 으로 넓혀라. **캘린더 work 가 그대로 물려받는다**
- **W-9** 게이트 유도 진입 훅이 DOM id 하나뿐이다 → `useCompletionCardFocus()`(또는 `imperativeHandle`)로
  **스크롤 + 완료 결과 입력 포커스 + 1.5초 강조**를 담아 `features/tasks` 에서 **내보내라**.
  **id 만으로는 「자리」이지 「훅」이 아니고, WORK-005 가 그 셋을 직접 만들면 규격이 그쪽에서 정해진다**

## 4. allowed_paths — 이 밖은 건드리지 마라

- `app/front/` — 전부

**`app/back/` 을 건드리지 마라**(BE 워커가 같은 워크트리에서 작업 중이다). 문서 레포도 **읽기 전용**이다.
**커밋·push·PR 하지 마라.**

## 5. 검증

```
cd app/front && npx tsc --noEmit (네가 만진 파일 0 에러) + npm test. 정적 빌드 제약 자기점검 — 동적 세그먼트 0 · 모든 page 에 'use client' · 컴포넌트 hex 리터럴 0 · Sheet 직접 import 0 · 폭 리터럴 0 · 컴포넌트 new Date() 0 · 컴포넌트 캐시 키 리터럴 0. 전체 빌드 금지, 검증은 1회만
```

**앱 창에서 실물로 확인하고 수치를 보고해라** — 검수가 「실행 불가능」이라 적은 항목들이다:

1. **드로어에 업무 제목이 보이는가.** 고치면 바깥을 클릭했을 때 저장되고 **로그에는 안 남는가**
2. 상세에서 **기한을 바꿀 수 있는가.** 시간까지 넣어 **이미 있는 시간 일정과 겹치게 하면** 저장되지 않고 토스트가 뜨고 **값이 원복**되는가
3. **끝시각 = 다른 일정의 시작시각**이면 **저장되는가**(경계 접촉은 겹침이 아니다)
4. 상세에서 **유형·프로젝트를 바꿀 수 있는가.** **서버를 내린 채** 유형을 바꾸면 트리거 테두리가 실패색이 되고
   그 행 아래에 「유형이 저장되지 않았습니다 · 다시 저장」이 뜨는가
5. **할일 추가·체크가 앱 창에서 도는가** — 검수가 「이 경로는 한 번도 돌지 않았다」고 적은 자리다.
   체크하면 **진행률이 즉시** 바뀌는가(낙관적). 서버를 내리면 **되돌아가고** 실패 표시가 뜨는가
6. 연관업무 검색에서 **검색어가 `#FFF3B0` 으로 하이라이트**되고 입력 포커스에 **글로우**가 보이는가

**5 번은 반드시 앱 창에서 해라.** 자동조작이 입력 포커스를 못 잡으면 **그 사실과 대안 검증을 함께 보고해라** —
「했다」고만 적지 마라.

- 통과할 때까지 고친다. 못 고치면 이유와 함께 보고한다.
- 기존에 이미 깨져 있던 무관한 실패는 "무관"으로 분리해 보고한다.

## 6. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다. preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.

- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_6a4ac855-2a13-4484-b808-4c25182cbb2b --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "frontend 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_6a4ac855-2a13-4484-b808-4c25182cbb2b \
  --text "[worker_done] frontend 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_6a4ac855-2a13-4484-b808-4c25182cbb2b --text "[질문] frontend: <질문>" --enter`
