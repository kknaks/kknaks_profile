# 재검수 리포트 — strong-hajin-polish / frontend Phase 2 fix1 (2026-10-01)

## 판정: WARN

- **FAIL-1(늦은 응답의 누설)은 닫혔다.** 기억을 쓰는 33경로가 모두 세대 검사라는 같은 문을 지나고, 타입이 그 문을 강제한다.
- 앞 WARN 다섯 가운데 넷이 닫혔다. 나머지 하나(WARN-4)는 **리뷰어의 오판**이었다 — 워커 말이 맞다.
- fix1이 새로 만든 문제는 WARN 셋이다.
  - **갱신 잠금이 «진입 effect의 성공»에서만 풀린다.** 그래서 갱신이 한 번 실패하면, 그 뒤 다른 경로로 다시 읽기에 성공해도 홈·업무·캘린더·보고 단추가 잠긴 채 남는다.
  - 업무 레일 effect의 의존성에 잠금 값이 빠졌다.
  - 조직 화면에는 잠금이 없다.
- 셋 다 데이터가 새거나 잘못 실행되는 문제가 아니라 **눌러야 할 단추가 잠기는** 문제라 FAIL로 두지 않는다.

## 검수 범위

- `frontend/`만 본다. 수정 15개 + 신규 3개(`lib/screenCache.ts` · `lib/screenCache.test.tsx` · `features/today/TodayPage.test.tsx`). `backend/`는 제외한다.
- 실행한 검사
  - diff 정독
  - grep: `rememberScreenValue(` · `useRemembered` · `useScreenEpoch` · `*Fresh` · `actionItems`
  - `App.tsx` 세션 흐름 재추적
  - 직렬 vitest: `screenCache` · `TodayPage` · `MyWorkPage` · `CalendarPage` · `MeetingList` · `OrgPage` · `ProjectPage` · `DailyReportPage` · `App` · `Checklist` → **10파일 265/265**. 워커가 말한 Checklist 플레이크는 이번에는 재현되지 않았다.
  - 전체 1144 직렬은 다시 돌리지 않았다(워커 보고: 기준선 5 + 플레이크 1).

## 1. 앞 지적 닫힘표

| # | 앞 지적 | 결과 | 근거 |
|---|---|---|---|
| FAIL-1 | 늦은 응답이 바뀐 주인의 기억에 써진다 | **닫힘** | `lib/screenCache.ts` `epoch`를 둔다. `scopeScreenCache`·`forgetScreenCache`가 세대를 올린다. `rememberScreenValue(key, value, requestedAt)`는 `requestedAt !== epoch`이면 기억하지 않는다. `useRemembered`는 마운트 세대(`useScreenEpoch`)를 잡는다. 테스트 `screenCache.test.tsx:58`(직접 쓰기) · `:69`(언마운트된 setter) |
| WARN-1 | 기억한 envelope로 갱신 전 명령이 눌린다 | **닫힘 — 새 WARN-A·C 남음** | 홈 `todayFresh`, 업무 `workFresh`→`listBusy`, 캘린더 `commandsFresh`(구간별), 프로젝트 `projectFresh`, 회의 `listFresh`→`locked`, 보고 `reportFresh` |
| WARN-2 | 재진입 테스트가 업무 하나뿐 | **닫힘** | 홈(신규 `TodayPage.test.tsx`) · 캘린더 · 회의 · 조직 · 프로젝트 · 보고에 재진입 테스트를 더했다(+298줄) |
| WARN-3 | 키가 끝없이 쌓인다 | **닫힘** | `SCREEN_CACHE_KEYS_PER_PREFIX = 20`. `:` 접두사마다 가장 오래 쓰지 않은 칸부터 버린다(`delete` 후 `set`으로 최근 순서를 지킨다). 접두사 없는 키는 정해진 수라 상한이 필요 없다 |
| WARN-4 | 업무 화면 판단 행이 늦게 끼어든다 | **해당 없음 — 리뷰어 오판** | `MyWorkPage.tsx:211` `actionItems`는 **선언만 있고 읽지도 쓰지도 않는 죽은 상태**다. HEAD(`:206`)에서도 같다. 업무 화면의 판단 행은 이 상태에서 오지 않는다. 앞 리포트의 WARN-4를 철회한다 |
| WARN-5 | 보고 「생성 중」이 복원돼 비친다 | **닫힘** | `DailyReportPage.tsx:71-72` `restoredStatus`가 `queued`·`running`을 `null`로 복원한다(`:90` · `:213`). 실제 상태는 갱신 응답이 세운다 |

## 2. 세대 토큰 — 쓰기 경로 재계수

| 경로 | 수 | 문 |
|---|---|---|
| `useRemembered` 호출(setter가 세대 검사) | **26** | 홈 5 · 업무 9 · 회의 1 · 조직 6 · 프로젝트 4 · 보고 1 |
| `rememberScreenValue` 직접 호출 | **7** | 캘린더 `:170` · 조직 `:166` · `:243` · 보고 `:175` · `:183` · `:195` · `:279`. 모두 `useScreenEpoch()`로 잡은 마운트 세대를 넘긴다 |
| 합계 | **33** | 워커 계수와 같다 |

- `requestedAt`는 **필수 인자**다. 세대 없이 기억을 쓰는 코드는 tsc가 막는다. 앞으로 쓰기 경로가 늘어도 같은 문을 지난다.
- **세대를 잡는 시점이 맞다.**
  - `App`은 렌더 중 `scopeScreenCache(personaId)`를 부른다. 그래서 자식 화면의 `useState(currentScreenEpoch)`는 **주인을 정한 뒤의 세대**를 잡는다.
  - 로그인은 `resetWorkspace`(forget → +1) → `setSession` → 렌더 중 scope(+1) → 화면이 새로 서는 순서다. 로그아웃은 세션 `null` → 렌더 중 scope(`null`, +1) → 화면이 내려간다. 늦게 온 A의 응답은 세대가 달라 버려진다.
- **세대는 마운트 동안 고정이다.** 마운트 중에 세대가 바뀌는 길은 `resetWorkspace` 뒤 곧바로 세션이 바뀌어 화면이 내려가는 경우뿐이다. 그래서 「마운트 세대 = 요청 세대」 가정이 성립한다.

### 언마운트 때 주인을 내리던 effect를 지운 것

| 상황 | 결과 |
|---|---|
| StrictMode 이중 effect | 지운 이유 그대로다. 남겨 두면 개발 모드에서 세대가 어긋나 아무것도 기억하지 못한다. 지운 것이 맞다 |
| 로그아웃 · 세션 만료 · 다른 사람 로그인 | 주인은 **렌더 중 scope**와 `resetWorkspace`의 forget이 내린다. 언마운트 effect에 기대지 않는다 → **누설 없음** |
| 탭(창) 닫기 · 새로 고침 | 모듈이 통째로 사라진다. 새 앱은 `useState(() => forget + scope(null))`로 비우고 시작한다 → **누설 없음** |
| 남는 것 | **테스트 환경만.** 한 테스트 파일 안에서 `App`을 그렸다 내린 뒤 **같은 파일에서 `App` 없이 화면을 그리면** 이전 주인이 살아 있어 기억이 켜진다. 지금 그런 파일은 없다(`App.test`는 `App`만 그린다). 각 테스트 파일은 `afterEach(scopeScreenCache(null))`를 쓰고 있다. 참고로만 남긴다 |

## 3. 새 지적 (fix1이 만든 것)

### WARN-A 잠금이 진입 effect의 성공에서만 풀린다 → 갱신이 한 번 실패하면 계속 잠긴다

| 화면 | 잠금 해제 자리 | 다른 다시 읽기(셸 refresh · 쓰기 뒤 `reload`)가 풀어 주나 |
|---|---|---|
| 홈 `TodayPage.tsx:91` | `:126-129` 진입 effect `.then`만 | **아니다.** `onRegisterRefresh(reload)`(`:160`) · `:210`·`:228`·`:242`·`:462`의 `await reload()`는 `setTodayFresh`를 부르지 않는다 |
| 업무 `MyWorkPage.tsx` `workFresh` | 진입 effect `.then`만 | **아니다.** 셸 refresh · `TaskQuickActions onChanged=reload`는 풀지 않는다 |
| 캘린더 `CalendarPage.tsx:163-164` | `:186` 진입 effect `.then`만 | **아니다.** 단, 구간을 바꾸면 effect가 다시 돌아 풀린다 |
| 보고 `DailyReportPage.tsx:95` | `:218` 진입 effect `.then`만 | **아니다.** `refreshReport`(`:267`)는 풀지 않는다 |
| 프로젝트 `ProjectPage.tsx:90` | `:131` `reload` **안** | 그렇다 — 어떤 `reload`든 성공하면 풀린다 |
| 회의 `MeetingListPage.tsx:62` | `:76` `reload` **안** | 그렇다 |

- **시나리오**: 기억한 값으로 홈에 들어온다(잠금). 그 순간 서버가 잠깐 끊겨 진입 갱신이 실패한다(배너). 서버가 돌아와 셸이 refresh하면 목록은 새 값으로 바뀐다. 그런데 **판단 카드와 「시작」은 계속 잠겨 있다.** 탭을 나갔다 와야 풀린다.
- 잠금이 걸리는 것은 「기억한 값으로 시작한 마운트」뿐이다. 첫 진입 실패는 잠그지 않는다(`!remembered`가 초깃값).
- **권장**: 프로젝트·회의처럼 해제를 각 화면의 `reload` **성공 지점 안**으로 옮긴다. 테스트 한 줄: 진입 갱신 실패 → 셸 refresh 성공 → 단추 활성.

### WARN-B 업무 레일 effect의 의존성에 잠금 값이 없다

- `MyWorkPage.tsx:984-1016`: 레일을 등록하는 effect가 받은 요청 칸에 `busy={listBusy}`를 넘긴다(`:990`). 그런데 의존 배열(`:1016`)에는 `busy`만 있고 `listBusy`·`workFresh`는 없다.
- `setWorkFresh(true)`는 진입 effect `.then`에서 `reload`의 setter들과 **다른 시점**에 올 수 있다. `reload` 안에 await가 여럿이라 마지막 setter 뒤에 한 번 더 await가 있으면 다른 렌더가 된다.
- 그때 다른 의존값이 함께 바뀌지 않으면 레일의 수락·거절 단추가 **잠긴 클로저로 남는다.** 다음에 `tasks`·`inboxItems` 등이 바뀌어야 풀린다.
- 지금 테스트는 이것을 잡지 않는다. 권장: 의존 배열에 `listBusy`를 넣는다.

### WARN-C 조직 화면에는 갱신 전 잠금이 없다

- `OrgPage.tsx:88` `administers`는 **기억한 `org.profile`의 capabilities**에서 나온다.
- 재진입 직후 갱신 전에도 관리 배지 · `canManageAccess`(`:400`) · 활동 표(`:408`)가 기억한 권한으로 선다.
- 실제 회수·부여는 상세에서 새로 읽은 값으로 하고 서버가 판정하므로, 잘못 실행되지는 않는다. 다만 WARN-1의 기준(갱신된 응답으로 권한을 판단한다)으로 보면 이 화면만 빠졌다.
- 권한이 그새 바뀐 경우(관리 권한 회수)에만 「보였다 사라지는」 일이 생긴다. 코디가 판단할 일이다: 조직도 잠글지, 권한 변경은 드물어서 그대로 둘지.

## 4. 화면 확인 목록 (갱신)

1. **탭 두 바퀴**: 둘째 바퀴에 스켈레톤 0. 재진입 직후 홈 판단 카드 · 「시작」 · 업무 행 단추 · 회의 행 메뉴 · 보고 저장·제출·생성이 **잠깐 비활성 → 활성**으로 바뀌는지 본다. 그 잠깐이 눈에 거슬리는지도 본다.
2. **갱신 실패 뒤 잠김**(WARN-A): 홈을 한 번 연 뒤 서버를 잠깐 멈춘다 → 업무 탭 → 홈 재진입(배너) → 서버 재가동 → 셸 새로 고침. 판단 카드가 **계속 잠겨 있는지** 본다(현재 코드로는 잠겨 있다).
3. **업무 레일 받은 요청**(WARN-B): 재진입 뒤 갱신이 끝났는데도 레일의 수락·거절이 비활성으로 남는지 본다.
4. **캘린더 드래그**: 재진입 직후(갱신 전) 업무 카드를 끌어도 움직이지 않고, 갱신 뒤 움직이는지 본다. 본 적 있는 달로 넘기면 그 구간도 잠깐 잠기는지 본다.
5. **로그아웃 → 다른 계정**: 모든 탭이 스켈레톤부터 서고 이전 사람의 값이 비치지 않는지 본다(동기 경로. 늦은 응답 경로는 단위 테스트가 지킨다).
6. **조직**(WARN-C): 관리자 배지·관리 칸이 재진입 직후 기억한 권한으로 바로 서는지 본다. 권한을 바꾼 계정으로 확인할 수 있으면 함께 본다.
7. **보고**: 생성 중이던 날로 돌아와도 「생성 중」이 기억에서 비치지 않는지 본다. 갱신 뒤 실제 상태가 서는지 본다.
8. **프로젝트·회의**: 갱신 실패 뒤 셸 새로 고침이 성공하면 잠금이 풀리는지 본다(이 둘은 풀려야 정상).

## 확인한 것

- 세대 검사 33/33 ✔ · 타입 강제 ✔ · 렌더 중 주인 설정 → 자식이 세대를 잡는 순서 ✔
- 언마운트 effect 제거로 생긴 누설: 운영 경로 0 ✔(테스트 환경 주의만)
- `api.ts` 밖 fetch 0 · 새 의존성 0 ✔
- 직렬 vitest 10파일 265/265 ✔ · 전체 1144는 재실행 안 함(워커 보고)
