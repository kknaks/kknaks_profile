# WORK-013 Phase 3~5 (frontend) — 완료 보고

브랜치 `kknaksss/docs-v1` · 워크트리 `/Users/kknaks/orca/workspaces/task_management/docs-v1` · **커밋·push 하지 않음**(be+fe 한 커밋은 코디가 낸다)

## 변경 파일 (전부 `app/front/`)

**신규 2**
- `src/features/meetings/linePayload.ts` — `payload` 를 읽는 자리 하나(모양 판정 · `compactChanges` · 툴팁 요약)
- `src/features/meetings/components/PayloadDrawerParts.tsx` — 두 드로어가 함께 쓰는 부품(`PayloadField` · `TodoDraftList` · `SUBMIT_LABEL`)

**폐기 1** — `src/features/meetings/components/LineKindSelector.tsx`(MF-60)

**수정 (Phase 3)**
- `components/CreateTaskFromLineDrawer.tsx` → **액션 payload 드로어**(U-10) 전면 재작성
- `components/LinkTaskDrawer.tsx` → **업무 payload 드로어**(U-9) 전면 재작성 · 헤더 업무 셀렉터(스토어)
- `features/tasks/components/RelationPopover.tsx` — **`mode` prop 하나만** 추가(단일 선택) · `features/tasks/index.ts` 배럴 export
- `hooks/useMeetingTaskLink.tsx` — 「넣기」 둘(`insertNewTask` · `applyTaskUpdate`)만 남기고 재작성
- `components/LineTaskButton.tsx` — 세 상태 · **dot** · 툴팁 · 언제나 드로어를 연다
- `openMeetingDrawers.tsx` · `api.ts` · `types.ts`(`ActionLinePayload` · `TaskLinePayload` · `TaskUpdateInput` · `AddLineInput` · `UpdateLineInput`)

**수정 (Phase 4)**
- `components/LineRow.tsx` · `components/AgendaLineTree.tsx` — `onChangeKind` 제거 · 라벨은 라벨로
- `hooks/useMeetingEdit.tsx` — `changeLineKind` 폐기 · **`savePayload`** 신설(낙관적)
- `components/MeetingDetailBody.tsx` — 칩 둘 갈래 · `submitMode` · 「제거」 모달 호출
- `components/shared/ConfirmModal.tsx` · `lib/overlay/OverlayProvider.tsx` · `components/LineDeleteModal.tsx` — `size:"light"`(420 · 한 문장 · 슬롯 없음)
- `styles/tokens.css` · `tailwind.config.ts` — `--tm-modal-light-width: 420px`

**수정 (Phase 5)** — `features/settings/components/{WorkTypePanel,InlineAddRow}.tsx` · `lib/api/workSettings.ts` · `types/api.ts`

**테스트 4** — `MeetingTaskLink.test.tsx`(전면) · `MeetingEditMode.test.tsx` · `WorkTypePanel.test.tsx` · `static.test.ts`(㉓ 신설 7)

`src-tauri/tauri.conf.json` 은 **내가 만진 게 아니다** — 디스패치 전부터 modified 였다.

## Phase 3 — payload 드로어 둘

- **드로어가 보는 것은 `prefill` 이 차 있나뿐이다.** `isAiLine` · `line.track ===` 로 가르는 코드가 0건이고, 정적 검사가 그것을 고정한다.
  AI 가 채운 줄과 사람이 「저장」한 줄이 **같은 드로어 · 같은 값 · 같은 화면**으로 열린다(테스트가 두 경로를 같은 단언으로 지난다).
- **모드가 푸터를 가른다** — `SUBMIT_LABEL[submitMode]` 한 자리에서만 문구가 나오고, 「저장」·「넣기」를 손으로 적은 버튼이 0건이다(정적 검사).
  푸터 버튼은 언제나 **둘**(취소 + 하나).
- **액션(U-10)** — 안건 고정 · 제목 · 유형 · 프로젝트 · 계획 시작~종료 · 설명 · 할일 **일곱**. 「시작 상태」·참고자료·연관·첨부·로그 0건.
  `workTypeId=null` 이면 **저장은 되고 넣기는 비활성**.
- **업무(U-9)** — 헤더 **제목 자리가 셀렉터**다(`RelationPopover mode="single"`). 본문은 내용 + 변경분 일곱이고 상태 셀렉터에 「완료」·「취소」가 없다.
  업무를 안 골랐으면 본문 비활성. 「업무 연결」 같은 앞 단계가 없다.
- **보내는 것은 채워진 키만**(`compactChanges`) — `prefill` 을 그대로 되돌려 보내지 않는다. 업무의 **현재 상태와 같은 `status` 는 싣지 않는다**
  (툴팁에서도 뺀다). MSW 본문 단언으로 `{taskId, dueDate, note}` 만 나가는 것을 고정했다.
- **요청 배치** — 「저장」=`PATCH …/lines/{id}`(있는 줄) / `POST …/lines`(칩 진입 · 한 요청) · 「넣기」=`POST …/lines/{id}/task`(액션) /
  `PATCH …/lines/{id}/task`(업무). 「저장」 경로에서 **업무 API 요청 0**을 테스트가 단언한다.
- **인라인 자동 저장 0** — 값을 고치고 포커스를 벗어나도 요청이 없다(테스트).

## Phase 4 — 편집 모드 · 칩 둘 갈래 · 모달 420

- 편집 모드 줄은 **본문만** 입력 상자다 — 종류 셀렉터가 없고(`LineKindSelector` 파일도 없다) `PATCH` 본문에 `kind` 가 실리지 않는다(테스트).
- 「+ 논의」·「+ 결정」 → U-8 드로어 · 「+ 연관 업무」·「+ 액션 아이템」 → **payload 드로어가 바로** 뜬다(드로어가 연달아 둘 뜨지 않는 것을 단언).
  「저장」이 `POST …/lines` **한 요청**으로 줄 + `payload` 를 만들고 **업무는 안 생긴다** · 「취소」면 줄이 없다.
- 「제거」 → **420 모달**(`data-modal-size="light"`) 「이 줄을 삭제할까요? / 되돌릴 수 없습니다.」 **한 문장** · 경고 슬롯 없음(업무 줄이어도 같다).
  **회의 삭제 모달은 600(`heavy`) 그대로**임을 같은 파일에서 단언했다.

## Phase 5 — 유형 설명

추가 행이 [종류][이름][**설명**][색] 넷이고 설명은 선택(비면 `description` 키를 **보내지 않는다**) · 목록 행 인라인 편집(비우면 `null` · 「설명 없음」) ·
**기본 유형 3종도 설명은 편집된다**(이름·종류는 읽기 전용 · 삭제 버튼 없음) · 저장 실패는 SPEC-002 U-7 규격(토스트 + 「다시 저장」 · 재시도 0).

## 검증

- `npx tsc --noEmit` → **Errors 0**
- `npx vitest run` → **35 files / 340 tests 전부 통과**(0 실패)
- `npx next lint` → **Error 0**
- 정적(직접 grep)
  - `git diff --stat features/tasks/components/TaskCreateDrawer.tsx TaskDetailDrawer.tsx` → **0줄**(업무 탭 드로어 미수정)
  - `isAiLine|line.track ===` · `LineKindSelector|onChangeKind` · `pendingChange|applyPendingChange` · `newTask` → 소스 0건(남은 것은 검사 needle 과 이력 주석뿐)
  - `Dialog` 직접 import → `components/shared/ConfirmModal.tsx` **하나**
- 정적(`static.test.ts` ㉓ 신설 7) — 위 다섯 + 「푸터 문구가 한 자리」 + 「`savePayload` 소유자가 `useMeetingEdit`」
- **업무 탭 회귀** — `features/tasks` 의 기존 테스트가 **한 줄도 안 고친 채 전부 통과**한다(드로어 diff 0 과 함께 이것이 회귀 증거다).

## 계약 준수 · 판단이 필요했던 곳

- **`RelationPopover` 를 `features/tasks` 배럴에 얹었다.** U-9 가 「업무 화면의 부품을 **그대로 재사용**한다(단일 선택 prop 하나만)」고 못박아
  두 벌을 만들 수 없었다. 영역 사이 import 예외 목록(`CROSS_AREA_ALLOWED`)에 이름 하나를 더하고 그 이유를 주석으로 남겼다 — 예외는 여전히 둘뿐이다.
- **U-9 헤더에 화면에 안 보이는 제목**(`sr-only`)을 두었다. 제목 자리가 셀렉터라 드로어에 접근성 이름이 없어져서다(디자인은 그대로).
- **삭제된 업무 줄의 버튼** — 디스패치 §3 은 「버튼 비활성」이라 적었지만 **SPEC-008 U-6 은 「버튼은 「업무 갱신」 그대로(헤더 셀렉터에서 다른 업무로 바꿀 수 있다)」**다.
  SPEC 을 따랐고 캡션 「삭제된 업무」는 옆에 남긴다.

## 미결 · 주의점

- **앱 창 실측 미완 · tauri dev 흰 화면**(WORK-011 · 012 때와 같은 증상 · 내 변경과 무관). `next dev` 는 `/` · `/tasks/` 모두 200 인데
  웹뷰만 빈 화면이다. 캡처 `w013-01-app.png`. 띄웠던 dev 프로세스는 모두 정리했다.
- **업무 payload 드로어의 「현재 값」 두 개가 비어 있다** — 기한 · 상태는 줄의 `task` 요약(또는 후보 목록)에서 현재 값을 그리지만,
  **프로젝트 · 완료 결과는 그 응답에 없다**. 회의록이 업무 상세를 읽는 경로를 새로 열지 않으려고(영역 경계) `payload` 값이 있을 때만 채우고
  없으면 「변경 없음」으로 둔다. 현재 값을 보여 주려면 상세 응답에 그 둘이 필요하다.
- **드로어의 prop 은 「모드를 가르는 둘」(`prefill` · `submitMode`)이고**, 그 밖에 안건 · 회의 프로젝트 · 줄 본문 · 콜백을 받는다.
  AI/사람으로 가르는 prop 은 0이다(계약이 막은 것은 그쪽이다).
- 백·프론트 **같이 배포**해야 한다 — `payload` 모양 · `/lines` · `/lines/{id}/task` 본문이 짝이다.
