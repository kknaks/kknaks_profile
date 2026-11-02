# FE 재수정 결과 보고 — 검수 FAIL 1 · WARN 7 · 2026-09-22

## 상태: done

한 줄. **FAIL-1 은 닫혔고, 「흔들리지 않는다」를 시점이 아니라 «불변식» 으로 바꿔 못 박았다** —
검사가 마지막 상태가 아니라 **등록된 모든 프레임**을 본다. 그래서 가드를 빼면 3/3 빨갛고(RED),
넣으면 **격리 27회(파일 12회 + 그 검사 단독 15회) 전부 초록**이다. WARN 은 **다섯을 고치고 둘은
코디 지시대로 유지**했다.

---

## 1. FAIL-1 — 프로젝트 0개인 사람에게 3레일이 먼저 서던 것

**원인** — `noProjects = projects !== null && …` 는 첫 렌더에서 반드시 거짓이라, 등록 effect 가
**목록을 알기 전에** 좌·우 레일을 셸에 꽂았다. `listProjects()` 가 `[]` 로 온 **뒤에야** 지워진다.

**고친 것** — `ProjectPage.tsx`
```ts
const listUnknown = projects === null && loadState !== "error";
…
if (noProjects || listUnknown) { onRegisterRails({}); return; }
```
`listUnknown` 을 deps 에 실었다.

**`loadState !== "error"` 한 조각을 더한 이유** — 수정안 그대로 `projects === null` 만 걸면
**적재 실패까지** 레일이 안 서고, 그러면 `ProjectRail` 의 **「다시 시도」 손잡이가 사라진다**
(`ProjectRail.tsx:48-56`, 실패 메시지는 `App.tsx` 의 토스트라 그 안에 재시도가 없다).
실패는 «모르는 것» 이 아니라 «알아내지 못한 것» 이라, 그때는 레일이 서서 손잡이를 낸다.
**첫 적재 중(loading)에만** 아무것도 세우지 않는다 — D-22 가 겨눈 자리는 그곳 하나다.

**검사도 고쳤다 (이게 흔들림의 뿌리)** — 기존 검사는 빈 상태가 뜬 **뒤에** `rail-left` 가 없는지만
봤다. 그건 **플러시 순서에 걸린 관찰**이라 2/11 로 빨갰다. Harness 가 등록을 전부 `railLog` 에 남기고,
검사가 **지나간 프레임까지** 본다:
```ts
expect(railLog.length).toBeGreaterThan(0);
expect(railLog.every((rails) => !rails.left && !rails.right)).toBe(true);
```
→ 「한 프레임도 서지 않았다」가 **시점과 무관한 불변식**이 된다.

**근거 (실측)**

| 무엇 | 회차 | 결과 |
|---|---|---|
| `ProjectPage.test.tsx` 격리 | **12회** | **12 pass · 0 fail** (18 tests 전부) |
| 그 검사 단독 (`-t "읽을 수 있는 프로젝트가 0개면"`) 격리 | **15회** | **15 pass · 0 fail** |
| **가드를 도로 뺀 채** 같은 검사 (RED 확인) | 3회 | **3회 전부 fail** — 우연히 초록이던 자리가 사라졌다 |

---

## 2. WARN 일곱 — 한 줄씩

| # | 처리 | 무엇을 했나 |
|---|---|---|
| **WARN-1** | **닫음** | `ProjectPage.tsx:289` 빈 상태 섹션 `aria-label` 을 `projectScreen.manage`(「프로젝트 관리」) → **`noProjectsTitle`**(「담당 프로젝트가 없습니다」). 보조기술이 그 화면의 이름을 바르게 읽는다 |
| **WARN-2** | **유지 (코디 지시)** | 접힌 가지 **안쪽** 선은 지금대로 **셈**(`__folded` 배지 + `title`)으로 낸다. 자기를 가리키는 화살표는 뜻이 없다. 코드 **0줄** 손대지 않았고 계약 문구 정정은 문서 몫이다 |
| **WARN-3** | **유지 (코디 지시)** | 모수 0 일 때 전체 진행률은 **「—」** 그대로(`projectModel.ts:161` · `ProjectSummaryStrip.tsx:39`). D-02 의 결과 같다. 코드 **0줄** |
| **WARN-4** | **닫음** | 담당 없음을 **「비운다」 쪽으로 통일**했다. 우 레일이 내던 `"—"` 를 없애고 **담당 dt/dd 쌍 자체를 안 만든다**(`ProjectTaskPanel.tsx:91-98`) — 좌 레일 카드(`meta: []`)·간트 이름줄(`owner: ""`)·하위 카드(`.filter(Boolean)`)와 **네 자리가 한 방식**이다. 반대 방향(좌 레일에 「—」 넣기)은 SPEC §6 「담당 없는 업무는 그 칸이 **비어 있다**」와 그 검사를 깨뜨려 고를 수 없었다. 소비처가 사라진 `.scax-pj-facts__none` 규칙도 지웠다 |
| **WARN-5** | **닫음** | `GanttFlatRow` 에 **`expandable`** 을 새로 뒀다 — 「접으면 실제로 사라질 행이 있는가」(`hasPlacedDescendant()`, 재귀). twisty 와 `open` 은 이것을 보고, **`hasChildren` 은 그대로** 바 규격(상위 14px · % 없음)과 「하위 N」을 맡는다. **둘은 다른 말이라 나눴다** — 하위가 전부 기간 없는 업무여도 「하위가 있다」는 참이다. 죽은 손잡이만 사라진다 |
| **WARN-6** | **닫음** | `projects.css` 에서 `--child` 를 **먼저**, `--parent` 를 **뒤에** 뒀다(같은 명시도 → 나중이 이긴다). 「상위이면서 하위」인 중간 깊이 바가 **14px** 이고 연함(.92)은 남는다. **jsdom `getComputedStyle` 로 실측**: `parent 14px` · `child 18px · .92` · **`both 14px · .92`** |
| **WARN-7** | **닫음** | 강조용 marker **`#pj-arrow-on`** 을 따로 뒀고 촉의 색을 CSS 클래스(`__arrow` / `__arrow--on`)로 준다. marker 내용은 참조하는 `<path>` 가 아니라 **자기 문맥**에서 상속하므로 `currentColor` 로는 닿지 않는다 — `context-stroke` 대신 이 길을 골랐다(구형 브라우저에서 조용히 회색으로 남지 않는다). 쓸모를 잃은 `color:` 선언 둘도 지웠다 |

**WARN-5 와 SPEC §6 의 관계** — 인수조건은 「twisty 가 **자식이 있는** 모든 깊이에 선다」다.
간트에 **설 수 없는** 하위만 가진 마디에서 손잡이가 사라지므로, 글자 그대로는 한 칸 좁아진다.
코디 지시(「펼칠 것이 실제로 있을 때만」)를 따랐고 **기록으로 남긴다** — 문구 정정이 필요하면 문서 몫이다.

---

## 3. 새로 쓴 검사 넷

- `ProjectPage.test.tsx` — ① 담당 없음의 통일(WARN-4: 「담당」 칸 자체가 없고 `—`·「미정」도 없다 /
  담당이 있으면 칸이 선다) ② 강조선의 `marker-end` 가 `#pj-arrow-on` 으로 바뀐다(WARN-7)
  ③ 하위가 전부 기간 없는 상위는 **「하위 1」은 내되 twisty 는 빈칸**이다(WARN-5)
- `projectModel.test.ts` — WARN-5 를 값으로: `hasChildren=true · childCount=2 · expandable=false`,
  그 아래 손자에 기간이 생기면 `expandable=true` 로 뒤집히고 접으면 그 행이 사라진다

---

## 4. 테스트 · tsc — 내가 잰 수치

| 명령 | 회차 | 결과 |
|---|---|---|
| `make frontend-test` | **4회** | **3회 초록** — `70 passed (70)` · **`978 passed (978)`** |
| ″ | (그중 1회) | `1 failed | 69 passed` — **`features/meetings/MeetingMaterials.test.tsx`** |
| `npx vitest run src/features/project/ProjectPage.test.tsx` | **12회** | **12회 전부 18 passed** |
| ″ `-t "읽을 수 있는 프로젝트가 0개면"` | **15회** | **15회 전부 1 passed** |
| `cd frontend && npx tsc --noEmit` | 2회 | **exit 0 · 에러 0** |

### 실패 하나의 귀속 — **이 판 밖이다**

`MeetingMaterials.test.tsx:361`. **`git diff --stat -- frontend/src/features/meetings/` 가 비어 있다**
(diff **0줄**) — 이 판이 한 글자도 안 건드렸다. **단독 3회 전부 통과**(15 passed ×3).
앞 판이 `ActionCenter.test.tsx` 에서 본 것과 **같은 병렬 부하 흔들림**이고, 이번 4회 동안
`ActionCenter` 는 **한 번도 안 흔들렸다** — 부하가 어느 파일에 떨어지느냐만 바뀐다. **기존 부채**다.

---

## 5. 만진 파일 — **전부 `frontend/`**

- `src/features/project/ProjectPage.tsx` — FAIL-1 가드 · WARN-1
- `src/features/project/ProjectTaskPanel.tsx` — WARN-4
- `src/features/project/projectModel.ts` — WARN-5 (`expandable` · `hasPlacedDescendant`)
- `src/features/project/ProjectGantt.tsx` — WARN-5 · WARN-7
- `src/styles/projects.css` — WARN-6 · WARN-7 · 죽은 규칙 정리
- `src/features/project/ProjectPage.test.tsx` · `projectModel.test.ts` — 검사

`backend/`·`docs/`·`Makefile`·`src/ds/`·`AppShell` **0줄**(현재 남아 있는 backend 변경 17건은 BE 워커 몫).
**커밋 0건** — `git log` 머리가 `e46ce39` 그대로다. **개발 서버 안 띄웠다.**

## 6. 다른 팀 영향

- BE 에 필요한 envelope·응답 변경 **없음**
- 문서 몫으로 남는 것 **셋**: WARN-2 계약 문구(「선 + 셈의 합」) · WARN-3 분모 0 규칙 기록 ·
  WARN-5 로 좁아진 §6 twisty 문구. **셋 다 코디 판단 자리**라 손대지 않았다

## 7. 이슈/블로커

- 없음. 다만 **`make frontend-test` 1회 초록을 통과 근거로 쓰지 않기**를 권한다 —
  병렬 부하 흔들림이 파일을 갈아타며 남아 있다(이번엔 meetings, 앞 판엔 action). 이 판 밖이다
