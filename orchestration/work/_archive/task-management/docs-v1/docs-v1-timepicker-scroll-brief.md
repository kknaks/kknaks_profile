# [frontend] 실물 버그 2 — 새 회의록 드로어의 시간 팝오버가 스크롤되지 않는다

너는 **task-management `frontend` 워커**다. 사용자가 앱에서 본 버그다.
역할 문서: `/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/orchestration/roles/task-management/frontend/role.md`

## 0. 어디서

**코드 워크트리** — `/Users/kknaks/orca/workspaces/task_management/docs-v1` (브랜치 `kknaksss/docs-v1`, HEAD `1ca243e`). 미커밋은 `tauri.conf.json`(사용자 것)뿐.

> ⚠ **사용자 앱이 `:3000` dev 서버를 물고 있다(`tauri dev`). 그 포트의 프로세스를 내리거나 next dev 를 새로 띄우지 마라.** 검증은 `tsc` · `vitest` 로만. 지난번 네가 :3000 을 내렸다 다시 띄워 사용자 화면이 깨졌다.

## 1. 증상

새 회의록 드로어(`MeetingCreateDrawer` 쪽) → 일시 → 시작 시간 `11:00` 을 누르면 팝오버가 열리고 00:00 · 00:30 · … 목록이 보이는데 **휠·트랙패드로 스크롤이 안 된다.** 목록은 `max-h-56 overflow-y-auto` 라 스크롤 상자는 맞다(`features/meetings/components/MeetingDateTimeField.tsx:135`). 캡처: `/var/folders/_z/ldzs6w2525zbx_49m1zzsx_00000gn/T/orca-paste-1788832681045-fabd3ba3-8bd6-4e29-8af6-050ac5e5f5af.png`(있으면).

**예상 원인** — 이 팝오버(`@/components/ui/popover` · Radix)가 **Sheet(Radix Dialog · modal) 안**에서 열린다. Dialog 의 스크롤 잠금(react-remove-scroll)이 자기 콘텐츠 밖의 휠 이벤트를 막는데, Popover 콘텐츠는 `body` 로 포탈되므로 「밖」이 된다. 같은 구조의 다른 팝오버(날짜 `CalendarGrid` 는 스크롤 없음 · 업무 드로어의 셀렉터 · `RelationPopover`)도 같은 문제를 가질 수 있다 — **드로어 안에서 열리는 스크롤 있는 팝오버를 전부 세라**(grep `overflow-y-auto` × `PopoverContent`). **확인된 두 번째 사례** — 같은 드로어의 프로젝트 셀렉터(`components/shared/Selector.tsx:188` · `max-h-64`): 프로젝트가 9개인데 6개까지만 보이고 그 아래 「ax 프로젝트」(id 10)에 못 닿아, 사용자가 같은 이름을 추가하려다 「이미 있습니다」를 받았다.

## 2. 고칠 것

원인을 실물로 확인하고(브라우저 `next dev` 는 **다른 포트**로 띄워도 된다 · `PORT=3100`) 고치는 자리는 **하나**여야 한다 — `components/ui/popover.tsx` 의 `PopoverContent` 가 드로어 안에서도 휠을 받게(예: Popover `modal` prop 을 드로어 안에서는 켜거나, RemoveScroll 의 `shards`/`allowPinchZoom` 처럼 팝오버 콘텐츠를 잠금 예외로 등록, 또는 Sheet 쪽 `DrawerFrame` 이 팝오버 포탈 컨테이너를 자기 안으로). 팝오버마다 `onWheel stopPropagation` 을 심는 식으로 **여러 자리에 흩뿌리면 반려.**

- 시간 목록의 현재 값이 보이도록 열릴 때 선택 항목으로 `scrollIntoView` 가 있는지 확인 — 없으면 이 발주에서 한 줄(11:00 이 열렸는데 00:00 부터 보이는 것도 캡처에 있다).
- 업무 드로어의 팝오버도 같은 수정으로 같이 풀리는지 확인만(그쪽 파일 수정 0).
- **기본값 확인(사용자 지적)** — SPEC-006 U-2 L160: 날짜 = 오늘 · **시작 = 현재 시각을 30분 단위로 올림** · 종료 = 시작 + 1시간. `MeetingCreateDrawer.tsx` 주석은 그렇게 적혀 있다 — 실물에서 그대로 나오는지(앱 시간대 기준 · 캘린더에서 고른 시각으로 들어온 경로 · 드로어를 닫았다 다시 열 때 옛 값이 남지 않는지) 확인하고 어긋나면 고친다. 열릴 때 목록이 선택값(예: 11:00) 자리에 와 있어야 한다 — 지금은 00:00 부터 보인다

## 3. 하지 마라
- `:3000` 프로세스 · 사용자 앱 건드리지 마라. `app/back/` 금지. 드로어 구조 · 필드 · 폭 변경 0. hex 리터럴 금지.

## 4. 검증
```bash
cd /Users/kknaks/orca/workspaces/task_management/docs-v1/app/front && npx tsc --noEmit && npx vitest run 2>&1 | tail -6   # Errors 0
```
휠 스크롤은 jsdom 이 못 보니 **원인·수정 자리를 보고에 적고**, 가능하면 다른 포트의 브라우저로 실측(캡처). 앱 창 확인은 사용자.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.**

- **커밋·push·PR 하지 마라.**

```bash
# (1) 인박스 적재
orca orchestration send \
  --to term_98a33032-2134-4bf9-ac48-e9df737f9b8f --from term_1c173ed7-8c1c-4b28-9b4c-f7817cc54ec8 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "frontend 완료: 시간 팝오버 스크롤" \
  --body "원인 / 고친 자리(하나) / 같이 풀린 팝오버 목록 / tsc · vitest 수치 / 실측 여부"

# (2) 직접 주입
orca terminal send --terminal term_98a33032-2134-4bf9-ac48-e9df737f9b8f \
  --text "[worker_done] frontend 완료 — 시간 팝오버 스크롤. 상세는 인박스." --enter
```

- 막히면 `orca terminal send --terminal term_98a33032-2134-4bf9-ac48-e9df737f9b8f --text "[질문] frontend: <질문>" --enter`
