# 리뷰 리포트 — strong-hajin-polish / frontend Phase 2 · B-01 (2026-10-01)

## 판정: FAIL

**FAIL 1 · WARN 5.**
- 계약의 뼈대는 맞게 섰다: 재진입하면 이전 데이터를 즉시 보이고 뒤에서 갱신한다. 스켈레톤은 첫 진입에만 뜬다. 활성 메뉴 7개를 모두 적용했다. 로그아웃·로그인 때 기억을 버린다.
- 다만 **늦게 도착한 응답이 «바뀐 주인»의 기억에 써지는 경로**가 남아 있다. 이전 사람의 데이터가 다음 사람의 화면에 비칠 수 있다. 확률은 낮지만 브리프 §3-2 「누설 경로가 하나라도 있나」에 해당하므로 FAIL로 둔다.
- 고치는 길은 작다(세대 토큰 한 줄, 아래 권장).

## 검수 범위

- diff: `frontend/`만 본다. 수정 9개 + 신규 2개(`lib/screenCache.ts` · `lib/screenCache.test.tsx`). `backend/` diff는 대상이 아니다(Phase 3a 진행 중).
- 기준: WORK-008 Phase 2 계약 다섯 줄 · P-2 · P-3 / `strong-hajin-polish-fe-p2-brief.md` / `fe-survey-report.md` §7
- 실행한 검사
  - diff 정독
  - `App.tsx` 세션 흐름 추적: `resetWorkspace` · `LoginPage` · `onSessionLost`
  - grep: 메뉴 · 쓰기 경로 · `rememberScreenValue` 호출 자리 · `fetch(`
  - 직렬 vitest 두 번
    - `screenCache.test` · `MyWorkPage.test` · `App.test`: **74/74**
    - `DailyReportPage` · `ProjectPage` · `CalendarPage` · `OrgPage` 테스트: **101/101**
  - tsc · build는 다시 돌리지 않았다(워커 보고: tsc 0 · build 성공).

## 1. 계약 대조

| 계약 (WP Phase 2) | 결과 | 근거 |
|---|---|---|
| 재진입하면 이전 데이터를 즉시 보이고 뒤에서 갱신 | **PASS** | `lib/screenCache.ts` `useRemembered`는 기억한 값으로 시작한다. 각 화면의 진입 effect는 그대로 돌아 같은 setter로 갈아 끼운다. 테스트: `MyWorkPage.test.tsx` 「다시 들어오면 이전 목록이 바로 서고 뒤에서 받은 값으로 바뀐다」(서버 응답을 보류한 상태에서 단언) |
| 스켈레톤은 데이터가 하나도 없는 첫 진입에만 | **PASS** | 업무 `workShown`·`inboxShown`(`MyWorkPage.tsx`), 캘린더 `hasScreenValue(rangeKey)`, 프로젝트 `projectsRemembered`, 회의 `listRemembered`, 조직(`null` 초깃값을 기억 값으로 대체). 받은 적 없는 빈 초깃값은 기억하지 않는다(`useRemembered` 주석과 테스트) |
| 사이드 메뉴 화면 **전부** | **PASS** | `App.tsx` `navigation`을 다시 셌다. 활성 7개(홈·업무·캘린더·프로젝트·회의·조직·보고)에 모두 적용했다. 비활성 2개(자료함·관계 탐색)는 메뉴에서 닫혀 있다. 회의 상세·AX를 뺀 이유는 워커 보고에 있다 |
| 쓰기 뒤 그 화면 데이터 갱신, 옛 데이터가 남지 않음 | **PASS** | 쓰기 뒤의 다시 읽기는 모두 같은 setter(또는 캘린더 `reload`의 `rememberScreenValue`)를 지나 기억도 바뀐다. 캘린더의 `setEntries` 호출은 `reload`(`:161`)와 기억값 복원(`:169`) 둘뿐이고, 쓰기 경로 여덟(`:265`·`:387`·`:433`·`:555`·`:576`·`:670` 등)은 모두 `await reload()`다. 보고는 저장·제출·생성 뒤 `rememberReport`. 테스트: 「쓰기 뒤의 다시 읽기가 기억도 바꾼다」 |
| envelope 판단은 갱신된 응답 기준 | **WARN-1** | 갱신이 오면 갈아 끼우는 것은 맞다. 다만 갱신이 오기 **전**에는 기억한 envelope(`allowed_commands`)의 단추가 눌린다 |
| (브리프) 로그아웃·사용자 전환 때 폐기 | **조건부 PASS → FAIL-1** | `resetWorkspace`가 `forgetScreenCache()`, 렌더 중 `scopeScreenCache(personaId)`, 세션이 없으면 주인 `null` → 비움. 동기 경로는 막혔다. 비동기 경쟁이 남았다 |

## 위반 (FAIL)

### FAIL-1 늦은 응답이 바뀐 주인의 기억에 써진다 → 이전 사람의 화면 데이터가 다음 사람에게 비칠 수 있다

`rememberScreenValue`(`lib/screenCache.ts:45-47`)는 **지금의 주인**만 본다(`owner !== null`). 값을 요청한 마운트가 **어느 주인 때 시작했는지**는 보지 않는다.
그래서 A가 띄운 요청이 A 로그아웃 → B 로그인 **뒤에** 도착하면, 그 값이 B의 기억에 같은 키로 들어간다.

**확실한 경로 (React 내부 동작과 무관)**
- **캘린더** `features/calendar/CalendarPage.tsx:159-163` `reload`
  - `await getCalendar(...)` 다음에 `rememberScreenValue(...)`를 **무조건** 부른다.
  - 진입 effect의 `cancelled` 검사(`:166-`)는 `reload()`가 끝난 **뒤** `.then`에만 있다. 언마운트된 뒤 도착한 A의 일정도 그대로 기억에 들어간다.
  - B가 같은 구간(이번 달)으로 캘린더에 들어오면 `useState` 초깃값(`:156`)으로 **A의 일정이 먼저 그려진다.** B의 응답이 오면 바뀌고, B의 응답이 실패하면 A의 일정이 그대로 남는다(`:183` 「받아 둔 값이 보이고 있으면 지우지 않는다」).
- **보고** `features/report/DailyReportPage.tsx:297-300` · `:320-322`: 저장·제출 뒤 `await getDailyReportHistory` 다음의 `rememberReport`에 마운트·주인 검사가 없다.

**같은 성격, React 갱신 경로에 기대는 자리**
- `useRemembered`의 setter는 기억 쓰기를 `setValue` 업데이터 **안에서** 한다(`screenCache.ts:62-67`).
- React는 큐가 빈 fiber의 `setState`를 **즉시(eager) 계산**한다. 언마운트된 컴포넌트에 늦게 온 setter 호출도 업데이터가 돌 수 있다.
- 해당 자리
  - 업무 `MyWorkPage`: `reload` 안에서 setter를 부르고 `cancelled` 검사는 그 뒤 `.then`에 있다
  - 회의 목록 `MeetingListPage.tsx:69-74` `reload`
  - 프로젝트 `ProjectPage.tsx` `reload`·`loadProject`
  - 오늘 `TodayPage` `reload`
- 조직의 구성원(`OrgPage.tsx` `cancelled` 뒤 기록)과 보고 `loadReport`(`shouldApply` 뒤 기록)는 막혀 있다.

**현실성**
- 창은 「A의 요청이 걸려 있는 시간 > A 로그아웃부터 B 로그인 완료까지」다. 사람이 로그인하는 데 수 초가 걸리므로 드물다.
- 하지만 업무·홈 진입은 최대 9콜이고 서버에 N+1이 남아 있다(OQ-802). 같은 기기를 두 사람이 쓰는 자리(공용 PC, 데모)에서는 일어날 수 있다.
- 테스트는 이 경쟁을 보지 않는다. `MyWorkPage.test` 「다른 사람으로 바뀌면 버린다」는 A의 요청이 **끝난 뒤** 주인을 바꾼다.

**권장 수정(작다)**
- `screenCache`에 세대 번호를 둔다. `scopeScreenCache`·`forgetScreenCache`가 올린다.
- `useRemembered`는 마운트 때 세대를 잡고, 세대가 다르면 기억하지 않는다. 직접 부르는 `rememberScreenValue`는 세대를 인자로 받거나 `useScreenEpoch()`로 잡는다.
- 테스트 한 줄: 응답을 보류한 채 주인을 바꾸고, 응답을 풀고, 새 주인 재진입에서 이전 값이 없음을 단언한다.

## 경미 (WARN)

- **WARN-1 기억한 envelope로 단추가 눌린다**
  - 홈 `TodayPage`의 `today.actionItems`(`ActionItemEnvelope.allowed_commands`, `lib/viewModels.ts:788`), 업무 목록의 행 액션, 프로젝트 `project.selected`는 갱신 전까지 **기억한 envelope로 단추를 그린다.**
  - 이미 처리된 판단에 다시 답하면 서버가 회차로 거절한다(`expected_version`). 그래서 잘못 실행되지는 않는다. 다만 사람은 「눌렀는데 오류」를 만난다.
  - WP 「권한(envelope) 판단은 갱신된 응답 기준이다」를 엄격히 읽으면 갱신 전 명령 단추는 잠가야 한다.
  - 코디가 판단할 일이다: (a) 갱신 전 명령을 비활성으로 둔다, (b) 서버 거절을 정상 응답으로 받는 지금 선례를 그대로 둔다.
- **WARN-2 재진입 테스트가 업무 화면 하나뿐이다**
  - 홈·캘린더·프로젝트·회의·조직·보고 여섯은 「다시 들어오면 기억한 값 → 뒤에서 갱신」 테스트가 **없다.**
  - 기존 화면 테스트는 주인이 없는 상태로 그리므로 `useRemembered`가 `useState`와 똑같이 돈다(`screenCache.ts` 주석: 주인이 없으면 기억하지 않는다). 그래서 이 여섯의 새 분기는 **테스트를 한 번도 지나지 않는다.** 캘린더 구간 키·조직 구성원 키·보고 날짜 스냅샷처럼 키가 갈리는 화면일수록 필요하다.
  - `App.test`도 주인 연결(렌더 중 `scopeScreenCache`)을 탭 전환으로 확인하는 단언이 없다.
- **WARN-3 기억이 끝없이 쌓일 수 있다(세션 동안)**
  - 캘린더 `calendar.entries:${from}|${to}`(`CalendarPage.tsx:155`): 달·주를 넘길 때마다 한 칸씩 쌓이고 지우지 않는다.
  - 조직 `org.members:${unit}`·`org.activity:${unit}`, 보고 `report.day:${date}`도 같다.
  - 세션당 사람이 넘겨 본 만큼이라 실용상 작다. 다만 상한이 없으므로 「최근 N개」 상한이나 「현재 키만」을 권한다.
- **WARN-4 업무 화면의 판단 행(`actionItems`)은 기억하지 않는다**
  - `MyWorkPage.tsx` `actionItems`는 `useState` 그대로다. 재진입하면 업무 목록은 바로 서고 「답하면 끝나는 행」은 응답 뒤에 **끼어든다.** 깜박임은 아니지만 줄이 밀린다(화면 확인 목록 3).
  - 의도(envelope를 늘 새로 받으려는 것)라면 리포트에 이유를 남기면 된다.
- **WARN-5 보고 화면의 「진행 중」 상태를 기억에서 복원한다**
  - `DailyReportPage.tsx` 스냅샷의 `status`가 `queued`·`running`이면, 재진입한 순간 생성 중 표시가 서고 폴링 effect가 다시 돈다.
  - 그새 끝났다면 갱신 응답이 와서 바뀌므로 동작에는 해가 없다. 「생성 중」이 잠깐 비치는 자리다.

## 2. 누설 점검 — 경로별

| 경로 | 결과 |
|---|---|
| 주인 설정 타이밍 | **안전.** `App` 렌더 중 `scopeScreenCache(personaId)`(자식의 `useState` 초깃값보다 먼저). 첫 마운트 `useState(() => forget + null)`. 언마운트 effect가 `null` |
| 로그아웃 | **안전(동기).** `resetWorkspace` → `forgetScreenCache` → 세션 `null` → 렌더 중 주인 `null` → `store.clear` |
| 다른 사람 로그인·같은 탭 재로그인 | `LoginPage.onLoggedIn` → `resetWorkspace` → 새 주인. **동기는 안전, 늦은 응답은 FAIL-1** |
| 세션 만료(`onSessionLost`) | 로그아웃과 같은 길 |
| StrictMode 이중 effect | `App` 언마운트 effect가 주인을 `null`로 만들어 한 번 비우고, 재마운트 effect가 다시 세운다. 시작 시점이라 무해하다 |
| 탭 사이 | 모듈 Map은 탭(창)마다 따로라 공유되지 않는다 |

## 3. 키 설계

| 화면 | 키 | 섞임 |
|---|---|---|
| 홈 | `today.*` 다섯 | 없음 |
| 업무 | `work.*` 아홉 | 없음 |
| 캘린더 | `calendar.entries:from\|to` | 구간마다 나뉜다. 섞임은 없고 쌓임은 있다(WARN-3) |
| 프로젝트 | `project.list` · `project.selected` · `project.history` · `project.directory` | 고른 프로젝트 하나. 재진입하면 `resumeProjectId`로 그 프로젝트를 다시 읽고, 목록에서 빠졌으면 첫 프로젝트로 간다(`ProjectPage.tsx` `rows.some`) |
| 회의 | `meetings.list` | 없음 |
| 조직 | `org.*` + `org.members:unit` · `org.activity:unit` | 조직마다 나뉜다 |
| 보고 | `report.evidence`(날짜 무관 — 근거는 `getTasks`) · `report.day:date` | 날짜마다 나뉜다 |

## 4. P-2 · 프론트 규율

- 새 모양 · 새 토큰 · 새 라이브러리 0.
- `api.ts` 밖 fetch 0. 서버 호출은 모두 기존 `lib/api.ts` 함수다.
- 권한 판단 로직은 바뀌지 않았다(WARN-1은 갱신 전 표시의 문제다).
- 공용 장치를 `lib/` 한 파일로 두고 일곱 화면이 같은 훅을 쓴다. 화면마다 따로 구현하지 않았다.

## 5. 화면 확인 목록 (코디용)

1. **탭 왕복**: 홈 → 업무 → 캘린더 → 프로젝트 → 회의 → 조직 → 보고를 두 바퀴 돈다. 둘째 바퀴에 스켈레톤이 **한 번도** 뜨지 않는지 본다.
2. **갱신 갈아 끼우기**: 다른 창(또는 AX)에서 업무를 하나 만들고 업무 탭으로 돌아온다. 옛 목록 → 새 목록으로 **조용히 바뀌는지**, 줄이 튀지 않는지 본다.
3. **업무 화면 판단 행**: 재진입 직후 「답하면 끝나는 행」이 늦게 끼어들며 줄이 밀리는지 본다(WARN-4).
4. **홈 판단 카드**: 다른 곳에서 이미 처리한 판단이 홈 재진입 직후 잠깐 남아 눌리는지 본다. 눌렀을 때 오류 문구가 자연스러운지도 본다(WARN-1).
5. **로그아웃 → 다른 계정 로그인**: 모든 탭이 **스켈레톤부터** 서고 이전 사람의 목록이 한 번도 비치지 않는지 본다. 특히 캘린더 이번 달을 본다(FAIL-1은 느린 응답에서만 재현되므로, 화면 확인만으로 통과했다고 닫지 않는다).
6. **캘린더 달 넘기기**: 본 적 있는 달로 돌아가면 즉시 서고, 처음 가는 달은 레일 스켈레톤이 뜨는지 본다.
7. **조직**: 펼쳐 둔 트리와 고른 조직이 재진입 후 그대로인지 본다. 다른 조직을 고르면 그 조직의 구성원이 스켈레톤이나 기억한 값으로 뜨는지 본다.
8. **프로젝트**: 보던 프로젝트로 다시 열리는지 본다. 간트 첫 진입 스크롤(오늘 보이게)이 재진입 때도 맞는지 본다.
9. **보고**: 초안을 편집하다 저장하지 않고 탭을 옮겼다 오면 편집이 사라진다. Phase 2 전과 같은 동작이지만 사용자가 기대할 수 있는 자리다. 생성 중이던 보고는 「생성 중」이 잠깐 비치는지 본다(WARN-5).
10. **오류 배너**: 서버를 잠깐 끊고 재진입하면, 기억한 목록은 남고 배너만 뜨는지 본다(빈 오류 화면으로 덮지 않는다).

## 기존 부채 (이번 판정 제외)

- 서버 성능(N+1 · 요청마다 인증 재계산)은 WP 범위 밖이다(OQ-802). FAIL-1의 창을 넓히는 요인이다.
- `CreateWork.test.tsx` 등 기준선 날짜 의존 실패 5건(`flaky-baseline-evidence.md`). 이번에 돌린 파일에는 없었다.

## 확인한 것

- envelope: 갱신 응답으로 갈아 끼운다 ✔, 갱신 전 표시는 WARN-1
- `api.ts` 밖 fetch 0 ✔ · 새 의존성 0 ✔ · 기존 setter와 effect를 재사용 ✔
- 테스트 직렬 실행 175/175 ✔. tsc · build는 **재실행 안 함**(워커 보고)
