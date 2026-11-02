# [frontend] REDRAW-08 — 첨부·연관 버튼이 안 눌린다 외 3건

너는 **task-management `frontend` 워커**다. 역할 문서: `/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/orchestration/roles/task-management/frontend/role.md`

작업 워크트리: `/Users/kknaks/orca/workspaces/task_management/docs-v1`

> **포트 3000 을 쓰지 마라.** `PORT=3100` 으로 띄우고 3100 만 정리해라.

---

## ⛔ C-1. 「+ 자료 첨부」·「+ 업무 연결」이 **안 눌린다** — 기능이 통째로 막혀 있다

**원인** — `features/tasks/components/TaskDetailBody.tsx` **L324** 의 `BlockAddRow` 가 **`label` 하나만 받는다.**

```jsx
function BlockAddRow({ label }: { label: string }) {   // ← onClick·ref 없음
  return <button type="button" className="…">          // ← 아무것도 안 붙는다
```

이걸 `AttachmentPopover`·`RelationPopover` 의 `trigger` 로 넘기는데(L228 · L257), **팝오버가 트리거에 붙이는 `onClick`·`ref`·`aria-*` 가 전달되지 않는다.** 그래서 눌러도 아무 일이 없다.

**REDRAW-07 에서 「점선 박스 → 테두리 없는 행」으로 바꾸며 새로 만든 컴포넌트다.** 시각만 재고 **클릭을 검증하지 않아 놓쳤다.**

**고칠 것**
- `BlockAddRow` 가 **버튼 props 를 전부 전달**받게 한다 — `React.ComponentPropsWithoutRef<"button">` 를 펼쳐 넣고, 팝오버가 `ref` 를 요구하면 **`forwardRef`** 로 감싼다
- **드로어와 확장 페이지 둘 다** 확인해라. 같은 컴포넌트를 쓰는 자리를 전수로 찾아라
- **첨부 팝오버의 「자료함 문서 / URL 링크」 두 갈래가 실제로 열리는지** 확인해라(`AttachmentPopover.tsx` L87~88 에 세그먼트가 있다)

**⚠ 이 브리프의 모든 항목은 「눌러서 동작하는지」까지 확인해야 완료다.** 실측만으로 끝내지 마라.

## C-2. 「+ 자료 첨부」 아래에 **빈 여백**이 생긴다

**원인** — `TaskDetailBody.tsx` **L205** 가 `grid grid-cols-1 gap-4 wide:grid-cols-2` 인데 **`items-start` 가 없다.** grid 기본이 `stretch` 라 **짧은 카드가 긴 카드 높이로 늘어난다** — 늘어난 부분이 「+ 자료 첨부」 아래 빈 공간으로 남는다.

**시안**(`업무 화면 정의서.dc.html` **L1948**)은 `display:flex; gap:16px` + 각 카드 `flex:1` 이고 **높이는 각자 내용만큼**이다. 사용자가 시안 캡처로 지적한 자리다.

**고칠 것** — 2열 컨테이너에 **`items-start`** 를 넣는다(또는 시안대로 `flex gap-4 items-start` + 카드 `flex-1`).
**확장 페이지에도 같은 자리가 있는지 확인**하고 있으면 같이 고쳐라.

## C-3. 「+ 프로젝트」 칩이 **실선 박스**로 보인다

프로젝트가 없을 때 헤더의 `[+ 프로젝트]` 가 채운 박스처럼 나온다.
**정한 규격** — h22 · r4 · **`border 1px dashed #D9D9D9`** · `#9EA2AE` · 12/400 · 배경 없음(REDRAW-03 H-3b).
실측해서 맞는지 보고, 다르면 고쳐라.

## C-4. 「+ 프로젝트」·유형 배지·일정 칩이 **눌러서 바뀌는지** 확인

REDRAW-03 H-3·H-3b·H-5 가 「배지·칩을 누르면 팝오버」로 정했다. **C-1 과 같은 원인으로 안 눌릴 수 있다.**
- 유형 배지 → 유형 팝오버
- 프로젝트 칩(또는 「+ 프로젝트」) → 프로젝트 팝오버
- 일정 칩 → 달력 팝오버
- 상태 칩 → 상태 드롭다운

**넷 다 눌러서 열리는지 확인하고, 안 되면 고쳐라.**

---

## 검증 — **클릭까지 확인해야 완료다**

```bash
cd app/front && npx tsc --noEmit   # 0 에러. 1회만
```

**playwright 로 실제 클릭을 재현해라**(합성 이벤트로 충분하다). 확인할 것:

1. 드로어 「+ 자료 첨부」 클릭 → **팝오버 열림 + 세그먼트 2개(자료함 문서 / URL 링크) 보임**
2. 드로어 「+ 업무 연결」 클릭 → **팝오버 열림 + 검색 입력 보임**
3. 확장 페이지에서 같은 둘
4. 유형 배지 · 프로젝트 칩 · 일정 칩 · 상태 칩 **각각 클릭 → 팝오버/드롭다운 열림**
5. 2열 카드가 **서로 다른 높이**다(짧은 쪽이 안 늘어난다)

**열리지 않는 것이 있으면 전부 고치고, 고친 뒤 다시 확인해라.**

**캡처 3장** — ① 첨부 팝오버 열린 상태 ② 2열 카드(높이 다름) ③ 「+ 프로젝트」 점선 칩

## 지킬 것

1. **C-1~C-4 만 고친다.** 다른 자리를 손대지 마라
2. **「적용했다」가 아니라 「눌러봤고 열렸다」로 보고해라**
3. 컴포넌트 hex 리터럴 0개 · **`app/back/` 금지**
4. **커밋·push 하지 마라**
5. 막히면 물어라 — `orca terminal send`. `orca orchestration ask` 는 답이 안 닿는다

## Done Criteria

- [ ] **첨부·연관 팝오버가 드로어·확장 둘 다에서 열린다**(클릭 재현으로 증명)
- [ ] 첨부 팝오버에 **「자료함 문서」·「URL 링크」 세그먼트가 보인다**
- [ ] 유형·프로젝트·일정·상태 **네 트리거가 전부 열린다**
- [ ] 2열 카드 높이가 **서로 독립**이다(빈 여백 없음)
- [ ] 「+ 프로젝트」가 **점선**이다
- [ ] `npx tsc --noEmit` 0 에러 · 캡처 3장

## 완료 보고 — 문구 변경 금지

```bash
orca orchestration send \
  --to term_6a4ac855-2a13-4484-b808-4c25182cbb2b --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId> --dispatch-id <이 태스크의 dispatchId> \
  --subject "frontend 완료: 첨부·연관 클릭 복구 외" \
  --body "C-1~C-4 각각 / 클릭 재현 결과(무엇을 눌러 무엇이 열렸나) / 같은 원인이 남은 자리 / tsc / 캡처 경로"

orca terminal send --terminal term_6a4ac855-2a13-4484-b808-4c25182cbb2b \
  --text "[worker_done] frontend 완료 — 클릭 복구. 상세는 인박스." --enter
```
