# UI kit — 업무 (Work home)

A recreation of the one fully designed product surface in the source Figma file: node `2001:21626` ("업무_네비게이션 min 사이즈") and its three sibling 1920×1080 variants.

## Files

- `index.html` — mounts the screen at its design size (1920×1080). Tagged as both a Design System card and a Starting Point.
- `WorkScreen.jsx` — the shell: `WorkHeader`, `InboxRail`, `AgentButton`, `CreateTaskModal`, `WorkScreen`.

Everything below the shell comes from the component library — `Navigation`, `TaskTable`, `WorkCalendar`, `InboxTask`, `InboxNotice`, `AiChatSidebar`, `MODCreateTask`, `ButtonButton`, `SegmentedControlSegmentedControl`, `Icon`. Nothing is re-implemented locally except the page header and inbox-rail chrome, which are not components in the source (they are raw frames), so their padding, hairlines and shadows are transcribed inline.

## What is interactive

| Click | Result |
| --- | --- |
| Navigation rail | toggles 180px (`size="max"`) ↔ 65px (`size="min"`) |
| 요청 업무 / 내 업무 / 완료 | switches `TaskTable type` between `request` / `my` / `done` |
| 업무 만들기 | opens the `MODCreateTask` modal; click the scrim to dismiss |
| The agent orb | swaps the 342px calendar rail for `AiChatSidebar` and hides the prompt bubble |
| The inbox segmented control | flips its filter state |

Everything else is cosmetic — this is a recreation, not a working app.

## Fidelity notes

- The frame is fixed at 1920×1080, matching the source. It does not reflow.
- The task-table tab row above `TaskTable` is a small addition so the three `type` variants are reachable; the source renders one type per frame with the tab strip living *inside* `Task_table`.
- The nav rail's brand slot renders the literal string `LOGO`, exactly as the source does. There is no logo in the file.
