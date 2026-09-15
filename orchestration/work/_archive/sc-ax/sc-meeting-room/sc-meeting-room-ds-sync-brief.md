# [designer] `.design-sync` 를 새 프로젝트로 재지정하고 우리가 만든 것을 DS 에 올린다

너는 **sc-ax 디자인 워커**다. 역할 문서는 따로 없다 — 이 브리프가 전부다.

작업 워크트리: **`/Users/kknaks/orca/workspaces/ax-workspace/sc-meeting-room`**
(branch `kknaksss/sc-meeting-room`, base `origin/main` = `75360fe`)

## 1. 배경 — 왜 지금인가

2026-09-13~14 에 앱 전체를 새 DS(`TheSC AX Design System`)로 옮기고 구 DS 를 은퇴시켰다
(PR #12 → `main` `75360fe`). 그 과정에서 **새 DS 에 없는 것 46건을 우리가 코드에 만들었다** —
안 그랬으면 구 `styles.css` 1313줄을 못 지웠다.

**그런데 그것들이 아직 Claude Design 에 없다.** 앱과 DS 의 부품 목록이 어긋난 상태다.
이 작업이 그 간극을 메운다.

**먼저 읽어라** (코디 워크트리, read-only):
`/Users/kknaks/orca/workspaces/kknaks_profile/sc-meeting-redesign/orchestration/work/sc-meeting-room/ds-gaps-status.md`
— 46건이 코드 어디에 어떻게 착지했는지, 무엇이 아직 안 닫혔는지, 올리는 순서까지 정리돼 있다.

## 2. 할 일 A — `.design-sync/config.json` 재지정

지금 **구 프로젝트**를 가리킨다:

```
projectId: 8fa54d76-58d6-481a-aed9-743dff9d6c09   ← 구 SCAX
```

**새 프로젝트로 바꾼다**: `7e839512-977c-4142-b4b5-d992df566ffc` (`TheSC AX Design System`)

같이 손봐야 하는 것 — **바퀴 10 이 `src/` 를 도메인 구조로 옮겨서 경로가 전부 바뀌었다**:

- `entry` — `./frontend/ds-entry.tsx` 가 아직 옛 경로를 import 할 것이다
- `componentSrcMap` — 20개 전부 `src/Icon.tsx` 꼴이다. **지금은 `src/ds/Icon.tsx`** 다
- `cssEntry` — `src/styles.css` 를 가리킬 텐데 **그 파일은 삭제됐다.** 지금은 `src/styles/index.css`
- `dtsPropsFor` — **손으로 쓴 props 사본**이다. 바퀴 11 이 문구를 prop 으로 올려 **시그니처가 바뀐 부품이 많다**

`.design-sync/NOTES.md` 에 지난 동기화의 함정이 적혀 있다. **먼저 읽어라** — 프리뷰·폰트·렌더 검사 환경이 거기 있다.

## 3. 할 일 B — 부품 목록을 지금 것으로 맞춘다

`frontend/src/ds/` 에 **22종**이 있다(테스트 제외). 구 목록 20개와 다르다:

**새로 생긴 것**: `Avatar` · `DataTable` · `Chip`(+`ChipBar`·`ChipRow`·`ChipToggle`) · `SegmentedControl`(+`Tabs`) ·
`Button`(+`ButtonGroup`·`IconButton`) · `Badge` · `StatusNote` · `GutterList` · `DropZone` · `FileList` · `Composer`

`componentSrcMap` 과 `ds-entry.tsx` 를 **지금 `ds/` 에 있는 것 기준으로** 다시 만들어라.

## 4. 할 일 C — `/design-sync` 실행

`/design-sync` 스킬을 써서 **새 프로젝트에 올린다.** `ds-gaps-status.md` 의 「올리는 순서」를 따라라 —
여러 화면이 쓰는 것(`Avatar`·`DataTable`)부터.

## 5. 경계

| | |
|---|---|
| **앱 코드를 고치지 마라** | `.design-sync/` 와 `frontend/ds-entry.tsx` 만이다. `src/` 안의 부품·화면은 **읽기만** |
| **부품 시그니처를 바꾸지 마라** | `dtsPropsFor` 가 안 맞으면 **소스에 맞춰 문서를 고쳐라.** 반대가 아니다 |
| **`backend/` 금지** | 한 줄도 |
| **구 프로젝트(`8fa54d76`)에 쓰지 마라** | 읽는 것도 필요 없다. 새 프로젝트만 |
| **커밋하지 마라** | 코디가 검증하고 커밋한다 |

## 6. 검증

```
cd frontend && npx tsc --noEmit     → 0 (ds-entry 를 고치면 여기서 잡힌다)
```

`/design-sync` 의 렌더 검사·프리뷰 캡처가 끝까지 돌아야 한다. **경고가 나면 삼키지 말고 보고**해라.

## 7. 보고

- `config.json` 에서 바꾼 것 전수 (`projectId` · `entry` · `cssEntry` · `componentSrcMap` · `dtsPropsFor`)
- **올린 부품 목록**과 Claude Design 에서 확인되는지
- `dtsPropsFor` 를 소스와 대조하며 **틀렸던 항목**
- 렌더 검사 경고
- **`ds-gaps-status.md` 의 46건 중 실제로 DS 에 올라간 것**을 번호로
- 막힌 것
