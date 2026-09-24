# 주 뷰 드롭 계측 보고서

## 계측 목적

임시 fallback이나 pointer 저장 경로를 추가하지 않고, 기존 HTML5 `dragstart` → `dragover`(고스트 표시) → `drop`(저장) 체인의 실제 단절 지점을 확인한다.

## 계측 위치

- `frontend/src/features/calendar/calendarDndDebug.ts` 신규 dev-only 계측기
- `ScheduleCard`: `dragstart` 직후
- `MonthGrid`: `dragover`, `drop`
- `WeekGrid`: 종일 칸과 시간 칸의 `dragover`, `drop`

각 기록에는 다음이 들어간다.

- `stage`: `dragstart` / `dragover` / `drop`
- `types`: `DataTransfer.types`
- `plain`: `getData("text/plain")`
- `text`: `getData("text")`
- timestamp

콘솔에는 `[calendar-dnd]` prefix로 출력하고, Tauri Web Inspector에서 다음 값을 읽을 수 있게 한다.

```js
window.__SCAX_CALENDAR_DND_LOG__
```

최근 30개만 보존한다. `import.meta.env.DEV`가 false인 빌드에서는 기록·콘솔 출력이 없다. 계측기는 task id를 보충하거나 drop을 승인하지 않는다.

## 자동 검증

- `npx tsc --noEmit`: 통과
- `npx vitest run src/features/calendar/CalendarInteractions.test.tsx src/features/calendar/CalendarPage.test.tsx --reporter=dot`: **48 passed**
- 계측 회귀 테스트에서 `dragstart → dragover → drop` 3단계와 각 단계의 `text/plain = flip`을 확인했다.
- 테스트 출력 예:

```text
[calendar-dnd] { stage: 'dragstart', types: [ 'text/plain' ], plain: 'flip', text: 'flip' }
[calendar-dnd] { stage: 'dragover', types: [ 'text/plain' ], plain: 'flip', text: 'flip' }
[calendar-dnd] { stage: 'drop', types: [ 'text/plain' ], plain: 'flip', text: 'flip' }
```

## 실제 Tauri 확인 방법

코드 레포 루트에서 다음을 실행한다.

```bash
cd /Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-projects
make local-stack
make tauri-local 2>&1 | tee /tmp/strong-hajin-tauri.log
```

`/tmp/strong-hajin-tauri.log`에는 Rust 셸의 boot/nav/load 로그가 남는다. 프론트 DnD 계측은 Tauri Web Inspector 콘솔의 `[calendar-dnd]` 로그와 아래 전역 버퍼에서 확인한다.

```js
window.__SCAX_CALENDAR_DND_LOG__
```

주 뷰에서 레일 업무 카드를 시간 칸으로 끌어 놓은 뒤 다음을 확인한다.

- `dragstart`가 없으면: 카드/HTML5 drag 시작 문제
- `dragstart`만 있으면: Tauri WebView가 dragover/drop을 전달하지 않는 문제
- `dragstart`·`dragover`는 있고 `drop`이 없으면: drop 허용/전파 문제
- 세 단계 모두 있고 `plain` 또는 `text`가 비면: DataTransfer payload 문제
- 세 단계와 payload가 모두 있고 저장이 없으면: `dropSlot` 이후 API/가드 문제

현재 환경에서는 GUI 자동 조작 권한이 없어 실제 마우스 드래그 결과 로그를 코디네이터가 직접 수집하지 못했다. 이번 변경은 계측만 추가했으며, 저장 의미·고스트 UX·drop 경로는 바꾸지 않았다.

## 보존한 계약

- pointerup 즉시 저장 경로 없음
- React task id fallback 없음
- HTML5 `draggable`, `dragover` 고스트, `drop` 저장 유지
- `text/plain` canonical payload 유지, `text` alias는 관측/호환 목적
- 운영 origin, 로그인, 배포 설정 변경 없음
