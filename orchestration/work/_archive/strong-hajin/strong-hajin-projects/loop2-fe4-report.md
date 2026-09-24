# 루프2 Phase FE-4 결과 보고 — 간트 셋 (2026-09-22)

**역할** `@sc-ax-fe` · **task-id** `task_8aefb1f7c8fc` · **워크트리**
`/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-projects`

## 상태: done

**커밋 0건** (워크트리에 변경만 남겼다) · **`backend/` 0줄** · **개발 서버 0회 기동**
(`5173`·`8100` 은 손대지 않았다) · **DS 토큰·공유 CSS 0줄** (`src/ds/` · `components.css` ·
`shell.css` · `scax.css` · `product.css` 전부 diff 0).

---

## 1. 바꾼 파일과 닫는 인수조건

| 파일 | 무엇 | 인수조건 |
|---|---|---|
| `frontend/src/styles/projects.css` | 이름 칸 `sticky`·`z-index`·`background`(+`align-self:stretch`) · 머리줄 `__axis-pad` 규칙 신설 · 완료 바 fill 투명도 | **L-42 · L-43 · L-44 · L-36** |
| `frontend/src/features/project/ProjectGantt.tsx` | 머리줄 **스페이서 요소 1개**(`paddingLeft` 를 대체) · 스크롤 컨테이너 `ref` · 첫 진입 `scrollLeft` · **선택된 행으로** `scrollIntoView` · `projectId` prop | **L-44 · L-45 · L-47** |
| `frontend/src/features/project/ProjectRail.tsx` | 목록에 `ref` · 선택된 **카드로** `scrollIntoView({block:"nearest"})` | **L-46** |
| `frontend/src/features/project/projectModel.ts` | `GANTT.openLead = 2` 한 값 신설(첫 진입에 오늘 앞으로 남길 날 수) | L-45 |
| `frontend/src/features/project/ProjectPage.tsx` | `ProjectGantt` 에 `projectId` 를 내린다 (1줄 + 주석) | L-45 |
| `frontend/src/features/project/ProjectPage.test.tsx` | 새 단언 **5건** + `getTask` 호출수 단언의 순서 의존 제거 | L-44~L-47 |

**좌표계는 한 줄도 안 움직였다** — `anchorIndex()` · `barGeometry()` · `depPath`/`DepLines` ·
행 `top` · `ganttRows`/접힘 · `positions` 맵 전부 그대로다. **두 열로 가르지 않았다**(D-36 기각안).
**L-48**(1루프 간트 회귀)은 기존 간트 단언 **전건이 그대로 통과**하는 것으로 확인했다.

---

## 2. 「고쳐야 할 넷」 — 하나씩

| # | 무엇 | 했나 | 어디 |
|---|---|---|---|
| ① | `position:sticky; left:0` | **했다** | `projects.css` `.scax-pj-gantt__name-cell` |
| ② | `z-index` 양수 (`z-index:2`) | **했다** | 같은 줄. 같은 행에서 `__bar` 가 DOM 뒤라 이것이 없으면 **막대가 이름을 덮는다** |
| ③ | `background:var(--scax-color-surface)` | **했다** | 같은 줄. 격자·오늘선·의존선 SVG 가 글자 밑으로 지나가지 않는다 |
| ④ | 축(머리줄)의 200px 자리를 덮을 sticky 요소 | **했다** | `ProjectGantt.tsx` 의 `<span class="scax-pj-gantt__axis-pad">` + `projects.css` 규칙 1줄. **`paddingLeft:200` 인라인은 제거**했다 — 남겨 두면 400px 가 된다 |

### ⚠ 넷 말고 **하나가 더 필요했다** — `align-self:stretch`

③ 만으로는 부족하다. `.scax-pj-gantt__row` 가 `align-items:center` 라서 이름 칸의 높이가
**글자 높이뿐**이고, 행 40px 중 남는 위아래로 **격자가 그대로 샌다**. 배경이 행을 다 덮어야
③ 이 실제로 성립한다. 조사 Q1 이 세지 않은 자리이고, `projects.css` 주석에 그 이유를 적어 뒀다.

**격자가 이름 칸을 지나는 근거**: `.scax-pj-gantt__grid` 는 `left:200px` 이라 **캔버스 좌표**
200 부터다. 가로로 밀면 뷰포트 왼쪽 200px 가 보여 주는 것은 캔버스 좌표
`scrollLeft ~ scrollLeft+200` 이고 그 구간은 전부 격자 영역이다 — 그래서 배경이 필요하다.

### L-36 (완료 바 색 · D-35 의 한 줄)

`.scax-pj-gantt__bar--done .scax-pj-gantt__bar-fill` 에 **`opacity:.55`** 를 얹었다.
다른 바는 `opacity:.9`(accent over accent-20 · danger over danger-soft)인데 완료 초록만
`positive` 원색이라 혼자 쨍했다. **`--scax-color-positive` 토큰은 안 건드렸다** — 그 값은
요약 스트립(`.scax-pj-summary__cell[data-tone="positive"]`)·배지 등 다른 자리가 함께 쓴다.
**`.55` 라는 수치 자체는 근거가 없다 — 눈으로 봐야 정해진다**(§5).

---

## 3. 계약에 없어 **내가 정한 것** (판단이 필요한 자리)

| 자리 | SPEC 이 말한 것 | 내가 정한 것 | 왜 |
|---|---|---|---|
| **첫 진입 스크롤의 재적용 시점** | 「**첫 진입**에 오늘이 보이는 위치」(§2.4 · L-45)만 있고 프로젝트 전환은 없다 | **첫 진입 + 프로젝트 전환** | 지시서의 기본값을 따랐다. `ProjectGantt` 에 `projectId` 를 내리고 effect 의 의존이 **그 값 하나**다 — 자료가 갱신될 때마다 되감으면 **사람이 민 자리를 화면이 도로 빼앗는다** |
| **오늘 앞에 남길 여백** | 없음 | **2일**(`GANTT.openLead`) | 0 이면 오늘이 고정된 이름 칸에 딱 붙어 「어제까지 무엇이 있었나」가 잘린다 |
| **오늘이 축 밖일 때** | 없음 | **가장 가까운 끝으로 접는다** | 이미 끝난 프로젝트·아직 시작 전 프로젝트에서 **없는 날로 스크롤하지 않는다.** 끝난 프로젝트를 열면 **마지막 날**이 보인다 |
| **자동 스크롤의 강도** | 「선택 표시만 서고 카드가 뷰포트 밖에 남지 않는다」 | **`block:"nearest"`** (양방향) | **이미 보이는 것은 안 움직인다.** 간트에서 고르면 그 행은 이미 보이므로 간트는 가만있고 좌 레일만 따라온다 — 그 반대도 같다 |
| **L-47 이 맞추는 대상** | 「간트가 **그 행이** 보이는 위치로 온다」 | **행**(`.scax-pj-gantt__row`)에 `inline:"nearest"` | 행은 `left:0;right:0` 이라 늘 스크롤 폭 전체를 차지한다 → **가로로는 계산이 붙지 않아** 첫 진입에 맞춰 둔 「오늘」 자리를 빼앗지 않는다. 세로(`.scax-pj-view`)만 최소로 움직인다. **「바가 보이게」로 해석하면 가로가 튄다** — 그러면 L-45 와 싸운다 |

---

## 4. **다음 판(FE-5)이 이어받을 구조 변경**

`ProjectRail.tsx` · `projects.css` 를 FE-5 도 만진다. **무엇이 달라졌는지 전부 적는다.**

### `ProjectRail.tsx`

1. **`import { Fragment }` → `import { Fragment, useEffect, useRef }`.**
2. 컴포넌트 본문 **맨 앞**에 `const list = useRef<HTMLDivElement|null>(null)` 와
   `useEffect(..., [taskId])` 한 덩이가 섰다 (`let body` 앞).
3. **`<div className="scax-gutter-list__body">` 에 `ref={list}` 가 붙었고 여러 줄로 펴졌다.**
   → FE-5 가 **레일 헤더 한 줄**(`__header--sub` → 한 줄)을 고칠 때 **`__body` 는 건드리지 마라.**
   자동 스크롤이 그 `ref` 로 카드를 찾는다.
4. 카드의 **`data-task-id` 가 이제 «조회 키»** 다 — 선택자
   `.scax-inbox-card[data-task-id="..."]` 로 찾는다. **그 속성을 지우거나 이름을 바꾸면 L-46 이 죽는다.**
   (`ProjectTaskCard` 자체는 한 줄도 안 바뀌었다.)

### `projects.css`

5. `.scax-pj-gantt__name-cell` 한 줄에 **선언 5개**가 늘었다
   (`align-self` · `position` · `left` · `z-index` · `background`). 앞에 **주석 6줄**이 붙었다.
6. **`.scax-pj-gantt__axis-pad` 규칙이 신설**됐다 (`__axis` 바로 아래, 주석 2줄 포함).
7. `.scax-pj-gantt__bar--done .scax-pj-gantt__bar-fill` 에 **`opacity:.55`** 와 주석 2줄.
   → FE-5 의 **우 레일 색 손질(D-35 의 나머지 둘: `ink-strong` · 메타 표)** 은 이 줄들과
   **겹치지 않는다** — 간트 블록(`§② 간트 + ③ 의존선`)과 우 레일 블록(`§우 레일: 업무 상자`)이
   파일 안에서 갈려 있다.
8. **줄 번호가 밀렸다** — 파일이 **171 → 182줄**이고 `.scax-pj-side` 가 **116 → 127줄**
   (이후 전부 **+11**). 조사 리포트의 줄 번호를 그대로 믿지 말고 선택자로 찾아라.

### `projectModel.ts` · `ProjectGantt.tsx` · `ProjectPage.tsx`

9. **`GANTT.openLead: 2`** 가 늘었다. `GANTT` 는 `as const` 라 값만 읽는다 — 좌표 계산은 이 값을 안 쓴다.
10. **`ProjectGantt` 의 prop 이 하나 늘었다 — `projectId: string` (필수).**
    `ProjectPage.tsx` 가 `selected?.project_id ?? ""` 로 내린다.
    → FE-5 가 `ProjectPage` 의 이른 반환·헤더 `actions` 를 고칠 때 **이 prop 을 빠뜨리면 tsc 가 잡는다.**
11. `GanttCanvas` 안에 **effect 3개**(ref 갱신 · 첫 진입 스크롤 · 행 스크롤)와
    **`scroller` ref** 가 생겼다. 머리줄 JSX 는 `paddingLeft` 인라인 스타일을 잃고
    **첫 자식이 `__axis-pad`** 다.

### `ProjectPage.test.tsx`

12. `GANTT` 를 `./projectModel` 에서 **import** 한다 (기하 상수를 테스트가 다시 적지 않는다).
13. **`captureScrollIntoView()` 헬퍼**가 파일 상단에 있다 — jsdom 에 없는 함수를 세워
    **대상 요소까지** 잰다. `afterEach` 가 `delete Element.prototype.scrollIntoView` 로 걷는다.
14. ⚠ **`renderPage()` 가 `vi.mocked(api.getTask).mockClear()` 를 한다.**
    「우 레일은 선택된 하나에만 상세를 부른다」 단언이 **호출 «횟수»** 를 재는데,
    그 mock 은 테스트 사이에 안 걷혀서 **앞 테스트가 고른 업무가 뒤 테스트의 수에 섞였다**(순서 의존).
    내 새 테스트 2건이 업무를 고르는 순간 그 단언이 `1` 대신 `3` 으로 깨졌다 —
    **기존 단언을 약하게 만들지 않고** 매 렌더에서 카운터를 털어 고쳤다.
    → FE-5 가 호출 수를 재는 단언을 더한다면 같은 함정을 기억해라.

---

## 5. 테스트 — **수치**와 **무엇을 실제로 지키나**

### 수치

| 무엇 | 결과 |
|---|---|
| `make frontend-test` | **70 파일 · 983 테스트 전건 통과** (16.43s). 실패 0 |
| 그중 프로젝트 화면 | `ProjectPage.test.tsx` **23건**(1루프 18 + 이번 **5**) · `projectModel.test.ts` 13건 |
| `npx tsc --noEmit` (`frontend`) | **에러 0** |
| `npm run build` | **성공** (`✓ built in 1.48s`). 청크 크기 경고는 이 판 이전부터 있던 것 |

**기존 실패와 내 실패의 분리** — **기존 실패는 0건이었고 내 실패도 0건이다.**
1루프에 흔들린 적 있는 `MeetingMaterials`·`ActionCenter` 는 이번 실행에서 **둘 다 통과**했다
(이 판 밖이라 손대지 않았다). 도중에 **한 번 깨진 것은 단 하나** —
위 §4-14 의 `getTask` 호출수 단언이고, **내 테스트가 드러낸 기존 순서 의존**이라 그 자리를 고쳤다.

### 테스트로 **잡은 것** (jsdom 이 실제로 재는 것)

| 단언 | 무엇을 지키나 |
|---|---|
| `axis.style.paddingLeft === ""` · `.scax-pj-gantt__axis-pad` 존재 · `pad.style.width === 이름 칸 폭` · `axis.firstElementChild === pad` | **머리줄의 그 자리를 «요소가» 덮는다.** 「비운 padding」으로 되돌아가면 깨진다. 스페이서와 이름 칸의 **폭이 한 값**이라는 불변도 함께 — 한쪽만 바꾸면 깨진다 |
| `scroll.scrollLeft === (4 - openLead) × day` · `not.toBe(0)` | **첫 진입이 기간의 첫날이 아니다.** jsdom 은 대입한 `scrollLeft` 를 그대로 들고 있어 **실수치로** 잰다 (선례 `CalendarPage.test.tsx:268`) |
| 오늘이 축 밖인 프로젝트에서 `scrollLeft === (19 - openLead) × day` | **축 밖으로 밀지 않고 가장 가까운 끝으로 접는다** |
| 간트 이름을 눌렀을 때 **그 `data-task-id` 의 좌 레일 카드**가 `scrollIntoView({block:"nearest"})` 로 굴렀다 | L-46. **어느 요소가** 굴렀는지까지 본다 — 「불리기만 했다」면 남의 요소를 굴려도 통과한다 |
| 좌 레일 카드를 눌렀을 때 **그 간트 행**이 `{block:"nearest", inline:"nearest"}` 로 굴렀고, **`scrollLeft` 가 첫 진입 값 그대로**다 | L-47 + **가로 자리를 빼앗지 않는다**(L-45 와 싸우지 않는다) |
| 클릭 **전** `calls.length === 0` | 첫 렌더에 아무것도 굴리지 않는다 |
| 기존 간트 단언 전건 | **L-48 회귀** — 손자 행 · 접어도 남는 선 · % 규칙 · 들여쓰기 · 취소 바 |

### **눈으로만 확인되는 것** — 사용자 2차 E2E 가 볼 자리

**jsdom 은 CSS 를 적용하지 않고 레이아웃도 계산하지 않는다.** 아래는 **테스트가 못 잡는다**:

1. **L-42 — 가로로 밀어도 이름이 실제로 남는가.** `position:sticky` 가 먹는지는 브라우저만 안다.
2. **L-43 — 고정된 칸 위로 막대·격자·오늘선·의존선이 비치지 않는가.**
   `z-index:2` 와 `background` 와 `align-self:stretch` **셋이 다 맞아야** 성립한다.
   ⚠ **특히 행 위아래 모서리** — `align-self:stretch` 가 빠지면 그 틈으로 격자가 샌다. 거기를 봐 달라.
3. **L-44 — 머리줄 날짜 숫자가 이름 칸 위로 안 올라오는가.** 요소가 있다는 것까지가 테스트다.
4. **L-36 — 완료 바가 다른 바와 «톤이 맞는가».** **`opacity:.55` 는 내가 눈 없이 고른 값이다.**
   더 낮추거나 올릴 필요가 있으면 `projects.css` 의 그 한 줄이다.
5. **L-45·L-46·L-47 의 «자연스러움»** — 값과 호출은 잤지만, 2일 여백이 충분한지 ·
   `nearest` 점프가 거슬리지 않는지는 손으로 밀어 봐야 안다.

---

## 6. 막힌 것 · 다른 팀 영향

- **막힌 것 없음.** 조사 Q1 의 판정대로 **CSS 쪽**이었고 간트를 다시 조립하지 않았다.
- **BE 영향 0** — 새 필드·새 호출 0건.
- **SPEC 과 어긋난 지점 없음.** §3 의 다섯 가지는 **계약에 문장이 없는 자리**를 지시서의 지침대로
  메운 것이고, planner 가 뒤집고 싶다면 바꾸는 곳은 전부 한 파일 안의 한두 줄이다.
- **FE-5 몫은 한 줄도 안 건드렸다** — 헤더 생성 버튼·모달 · 우 레일 「업무 정보」 블록 ·
  상태 드롭다운 · 좌 레일 헤더 한 줄. `ProjectTaskPanel.tsx` · `WorkModals.tsx` · `App.tsx` ·
  `ProjectManageModal.tsx` · `ProjectSummaryStrip.tsx` 는 **내가 바꾼 줄 0**이다.
- **완료 보고에 `--dispatch-id` 를 싣지 못했다** — 이 판에 dispatch 가 없다
  (`orca orchestration dispatch-show --task task_8aefb1f7c8fc` → `dispatch: null`,
  인박스 0건). **`--task-id` 만** 실어 보낸다.
