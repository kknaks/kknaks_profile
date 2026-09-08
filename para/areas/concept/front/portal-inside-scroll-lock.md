---
type: concept
id: portal-inside-scroll-lock
title: 스크롤 잠금 안의 포탈 오버레이 (Portal inside Scroll Lock)
aliases:
  - 드로어 안 팝오버 스크롤 안 됨
  - react-remove-scroll shards
  - Radix Dialog + Popover 휠
  - portal container
up:
  - 2026-09-08-docs-v1
tags:
  - popover
  - dialog
  - scroll-lock
  - radix
---

# 스크롤 잠금 안의 포탈 오버레이

모달(Dialog · Sheet)이 열리면 스크롤 잠금 라이브러리(react-remove-scroll)가 **잠금 노드 안**의 휠만 통과시키고 나머지는 `preventDefault` 한다. 모달 안에서 연 팝오버는 보통 `body` 로 포탈되므로 잠금 노드 **밖**이 되고, 목록에 `overflow-y: auto` 가 있어도 휠이 안 먹는다. 클릭·키보드는 되고 휠만 안 되는 것이 단서다.

## 정의

1. 증상: 모달 안 셀렉터·시간 목록이 상한 높이까지만 보이고 휠로 못 내린다. 항목이 잘려 「없는 항목」처럼 보인다(9개 중 6개만).
2. 원인: 잠금 라이브러리는 자기 shard(잠금 노드)에 속한 요소의 휠만 허용한다. 포탈된 `PopoverContent` 는 DOM 상 `body` 직계라 shard 밖.
3. 해결은 **한 자리** — 포탈 컨테이너 컨텍스트를 두고, 모달이 자기 콘텐츠 노드를 컨테이너로 실어 준다. 팝오버 부품은 컨텍스트가 있으면 그 안으로 포탈한다. 모달 밖에서는 컨텍스트가 없어 `body` 그대로.
4. 팝오버마다 `onWheel={e => e.stopPropagation()}` 을 심는 것은 자리가 흩어지고 다음 팝오버가 또 빠진다 — 반려.

## 사용 예시

```tsx
// lib/overlay/PortalContainer.tsx
const Ctx = createContext<HTMLElement | null>(null);
export const usePortalContainer = () => useContext(Ctx);
// DrawerFrame — SheetContent 노드를 실어 준다
<Ctx.Provider value={contentEl}>{children}</Ctx.Provider>
// ui/popover.tsx
<PopoverPrimitive.Portal container={usePortalContainer() ?? undefined}>
```

Radix Popper 는 `position: fixed` 이고 드로어에 `transform` 이 남지 않으므로 컨테이너를 옮겨도 위치가 그대로다. `transform` 이 있는 부모 안으로 포탈하면 fixed 기준이 바뀌니 확인한다.

## 왜 중요한가

캡처만으로는 「스크롤 상자가 없다」와 「휠만 막혔다」를 못 가른다. 두 팝오버가 동시에 같은 증상이고 모달 밖에서는 멀쩡하던 부품이면 잠금 쪽을 본다. 같은 수정으로 시간 목록 · 유형/프로젝트 셀렉터 · 연관 업무 후보 목록이 한 번에 풀렸고 업무 드로어는 0줄 수정이었다.

## 경계와 오해

- **`overflow-y: auto` 가 있어도 안 된다** — 스타일 문제가 아니라 이벤트가 막힌 것.
- **[[viewport-aware-overlay]] 와 다른 문제** — 그쪽은 패널이 화면 밖으로 나간 것, 이쪽은 패널이 화면 안에 있는데 휠이 안 먹는 것. 「스크롤이 안 된다」는 보고에 둘 다 후보다.
- **Popover `modal` prop** 으로도 풀리지만 포커스 트랩이 겹쳐 모달 안 모달이 된다. 컨테이너 쪽이 부작용이 적다.

## 함께 보는 개념

- [[viewport-aware-overlay]] — 「스크롤이 안 된다」의 다른 원인

## 출처

- 코드: `app/front/src/lib/overlay/PortalContainer.tsx` · `components/ui/popover.tsx` · `components/shared/DrawerFrame.tsx` · 커밋 `f0d4d46`(kknaks/task_management)
- 브리프: `orchestration/work/_archive/task-management/docs-v1/docs-v1-timepicker-scroll-brief.md`
