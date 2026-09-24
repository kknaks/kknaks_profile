# 루프2 Phase FE-4 **소수정** 결과 보고 — 검수 FAIL 1 · WARN 5 (2026-09-22)

**역할** `@sc-ax-fe` · **task-id** `task_15a1251c3491` · **워크트리**
`/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-projects`

## 상태: done

**커밋 0건** · **`backend/` 0줄** · **개발 서버 0회 기동**(`5173`·`8100` 안 건드렸다) ·
**DS 토큰·공유 CSS 0줄** · **FE-5 몫 0줄**.

**내가 바꾼 파일은 둘뿐이다.**

| 파일 | 무엇 | 닫는 것 |
|---|---|---|
| `frontend/src/features/project/ProjectPage.test.tsx` | `scrollLeft` 단언 셋을 `waitFor` 로 감쌈 · 기대값을 **리터럴**로 박음 · **새 테스트 1건**(왼쪽 밖) | **FAIL-1 · WARN-1 · WARN-2** |
| `frontend/src/styles/projects.css:114` | 완료 바 fill `opacity:.55 → .71` (+ 근거 주석 4줄) | **WARN-3** |

`projectModel.ts` · `ProjectGantt.tsx` 는 **뮤테이션 probe 때문에 mtime 만 움직였고 내용은 백업본과
`diff` 로 바이트 동일**하다(아래 §뮤테이션). 구현 코드는 **한 줄도 안 고쳤다** — 고칠 자리가 테스트와
CSS 한 줄이었다.

---

## FAIL-1 — `waitFor` 로 감쌌다 · **단독 22회 전부 초록**

`ProjectPage.test.tsx` 의 `scrollLeft` 읽기 **셋 전부**를 `await waitFor(...)` 안으로 넣었다 —
검수가 지적한 L-45 하나뿐 아니라 **같은 모양의 「오늘이 축 밖」 단언**도 같이 감쌌다.
둘 다 `findByText` 직후에 **패시브 effect**(`ProjectGantt.tsx` 첫 진입 스크롤)의 값을 읽던 자리다.
L-47 의 읽기는 `fireEvent.click`(동기 act) 뒤라 감싸지 않았다(검수 판정 그대로).

### 실측

| 무엇 | 횟수 | 결과 |
|---|---|---|
| **`vitest run ProjectPage.test.tsx` 단독** (부하 없음) | **12회** | **12회 전부 24건 통과** |
| **`vitest run ProjectPage.test.tsx` 단독** — **전체 스위트를 동시에 돌려 부하를 건 상태** | **10회** | **10회 전부 24건 통과** |
| `make frontend-test` 전체 | **7회** | **이 판의 실패 0회** (아래 §스위트) |

**단독 22회 · 부하 10회 포함 전부 초록.** 검수가 2/8 로 잡은 자리는 재현되지 않는다.
기계에는 사용자 E2E 스택이 계속 떠 있었다(부하 있는 상태).

---

## WARN-1 — 자기참조를 없애고 **기대하는 수를 직접 적었다** · 뮤테이션으로 확인

`GANTT.openLead` 로 되계산하던 기대값 **셋을 전부 리터럴로 박았다.**

| 자리 | 전 | 후 |
|---|---|---|
| L-45 첫 진입 | `(4 - GANTT.openLead) * GANTT.day` | **`68`** (주석: `(4-2)×34`) |
| 오늘이 축 오른쪽 밖 | `(19 - GANTT.openLead) * GANTT.day` | **`578`** (주석: `(19-2)×34`) |
| L-47 가로 자리 유지 | `(4 - GANTT.openLead) * GANTT.day` | **`68`** |

### 뮤테이션 실측 — **이제 잡는다**

| 뮤테이션 | 검수 때(되계산) | **지금(리터럴)** |
|---|---|---|
| `projectModel.ts:35` `openLead: 2 → 0` | ⚠ **23건 전건 통과** | ✅ **4건 빨강** — `expected 136 to be 68` · `expected 646 to be 578` (L-45 · 축 밖 · 왼쪽 밖 · L-47) |
| `openLead: 2 → 4` | `not.toBe(0)` 하나만 잡음 | ✅ **4건 빨강** — `expected +0 to be 68` · `expected 510 to be 578` |

즉 **0·1·3 이 조용히 지나가던 구멍이 닫혔다.** 앞 판 리포트의 「실수치 68 로 잰다」는 검수 지적대로
그때는 **과한 주장**이었고, 지금은 참이다.

---

## WARN-3 — `opacity: .55 → .71` · **고칠 곳은 `projects.css:114` 이 한 줄이다**

```css
.scax-pj-gantt__bar--done .scax-pj-gantt__bar-fill{background:var(--scax-color-positive);opacity:.71}
```

검수 제안 범위 **`.70~.72`** 의 가운데 값을 골랐다 — 합성색 `rgb(69,207,116)` · **채도 0.67**
(accent `.61` · danger `.77` 사이) · 휘도 `≈0.47`. 앞 값 `.55` 는 채도 0.48 로 **셋 중 최저**이고
휘도가 0.55 로 accent(0.216)·danger(0.201)의 **2.5배**였다 — 흰 트랙 위에서 투명도를 낮추면
채도만이 아니라 **밝기가 오른다**는 검수의 계산 그대로다.

**⚠ 최종 판정은 사용자 눈이다.** 줄 번호가 앞 판의 `110` 에서 **`114`** 로 밀렸다(주석 4줄을 더했다).
**더 진하게 하려면 숫자를 내리고(`.70`·`.9`), 더 연하게 하려면 올린다(`.72`~).**
그 한 줄 말고는 색을 건드린 자리가 없다 — **토큰 0줄 · hex 리터럴 0건.**

---

## WARN-2 (「오늘이 축 **왼쪽** 밖」) — **정했다 · 테스트를 더했다 · SPEC 은 코디 몫**

### 우리가 정한 것

> **아직 시작 전 프로젝트는 「기간의 첫날」에서 연다.**

오른쪽 밖(끝난 프로젝트가 마지막 날에서 열린다)의 **대칭**이고, 오늘이 축 밖이니 「오늘이 보이는
위치」가 애초에 없다. 구현은 이미 그렇게 동작한다(`Math.max(0, …)`) — 새로 정한 것은 **문장과 테스트**다.

### ⚠ 코디에게 — **SPEC L-45 의 문면과 어긋난다**

L-45 는 「**첫 진입에 「오늘」이 보이는 위치**로 스크롤돼 있다 — **기간의 첫날에서 시작하지 않는다**」다.
왼쪽 밖 갈래에서는 **정확히 기간의 첫날**에서 연다. 계약 위반이 아니라 **계약의 빈자리**이니
**§2.4 · L-45 에 「오늘이 축 밖이면 가장 가까운 끝」 단서 한 줄**을 얹어 달라.

### 더한 테스트 — **정말 문다**

새 테스트 1건: `아직 시작 안 한 프로젝트는 기간의 «첫날» 에서 연다 — 오늘이 축 왼쪽 밖이다`.

⚠ **첫 렌더에서 `toBe(0)` 을 재면 아무것도 못 잡는다** — jsdom 의 `scrollLeft` 초기값이 이미 0 이라
effect 가 안 돌아도 통과한다. 그래서 **프로젝트를 «전환»한다**: 9월 프로젝트에서 68px 로 열린 화면을
레일 셀렉터로 10월 프로젝트로 갈아타면 **0 을 덮어써야** 통과한다. 전환 선례는 같은 파일의
「프로젝트를 바꾸면 …」 테스트다. 「오늘」 선이 축 밖이라 서지 않는 것(`__now` 가 null)도 함께 잰다.

**뮤테이션으로 확인했다** — 첫 진입 effect 의 의존 `[projectId] → []` 로 바꾸면(= 전환에 되감지
않으면) **이 테스트 하나만 빨강**: `expected 68 to be +0`. 나머지 23건은 통과한다.

**정직하게 적는다**: 축 밖 clamp 제거(검수의 M7)는 **이 테스트가 못 잡는다** — 왼쪽 밖에서는
`max(0, 음수)` 가 그대로 0 이라 결과가 같다. 그 자리를 잡는 것은 **오른쪽 밖 테스트**이고
(clamp 제거 → `expected 1122 to be 578` 빨강) 그것으로 충분하다.

---

## WARN-4 · WARN-5 — **닫지 않았다. 이유를 적는다**

### WARN-4 (스위트가 부하에서 흔들린다) — **이 판 밖이라 손대지 않았다**

지시서의 「고치지 말고 옮겨만 적어라」를 따랐다. 아래 §스위트에 내 7회 실측을 옮겼다.
고치려면 **각 테스트 파일의 소유자**가 대상이고 FE-4 의 6파일과 겹치는 자리가 없다.

### WARN-5 (틀고정·색을 jsdom 이 한 줄도 재지 않는다) — **닫을 수 없다**

`align-self:stretch` 를 지워도 전건 통과한다는 것은 **jsdom 이 CSS 를 적용하지도 레이아웃을
계산하지도 않기** 때문이다. 이 자리를 테스트로 닫는 길은 둘뿐이고 **둘 다 이 판의 몫이 아니다**:

1. **Playwright journey**(`frontend/scripts/*-e2e.mjs`) — 역할 규칙상 **브리프가 지정할 때만** 쓴다.
   그리고 떠 있는 스택이 필요한데 **개발 서버 금지**다.
2. 스타일시트를 jsdom 에 먹이고 `getComputedStyle` 로 재기 — sticky·z-index·stretch 의 **효과**는
   여전히 안 재어진다(선언이 있다는 것만 재어진다). 지금 테스트가 이미 하는 것(요소가 있나·폭이
   한 값인가)보다 **더 가는 것이 없다.**

**그래서 ①~⑤ 와 `opacity:.71` 의 관측자는 사용자 2차 E2E 하나다.** 검수 리포트 §「눈으로만
확인되는 것」 1~6 을 그대로 물려받는다 — 특히 **행 위아래 모서리**(`align-self:stretch` 의 자리)와
**완료 바 톤**.

---

## 스위트 — **기존 실패와 내 실패를 갈라 적는다**

`make frontend-test` **7회**(70파일 · **984건** = 983 + 내 새 테스트 1) + `npx tsc --noEmit`.

| 무엇 | 결과 |
|---|---|
| **이 판(FE-4)의 실패** | **7회 중 0회** ✅ |
| 전건 통과 | **4회** (984/984) |
| 기존 실패 | **3회** — 매번 **한 건씩 · 다른 자리** |
| `npx tsc --noEmit` | **에러 0 (exit 0)** ✅ |
| `ProjectPage.test.tsx` 단독 | **24건**(앞 판 23 + 1) — 22회 전부 통과 |
| `projectModel.test.ts` | **13건 통과** (건드리지 않았다) |

### ⚠ 이 판 밖 flaky — **코디의 flaky 대장(`flaky-baseline-projects.md`) 자리**

내 7회에서 난 실패 3건(전부 FE-4 밖):

| 테스트 | 회수 |
|---|---|
| `MeetingMaterials.test.tsx > 이미 볼 수 있는 사람은 고르는 자리에 안 낸다` | 1 |
| `ActionCenter.test.tsx > keeps the discussion on the judgement without turning it into a control` | 1 |
| `Checklist.test.tsx > task checklist > moves a step with the keyboard and sends the whole order` | 1 |

**검수 리포트와 합쳐 읽을 사실** — 검수는 9회에서 `task checklist`(2) · `task checklist`(span/null) ·
`adjustment and resubmission` · `product surfaces` 를 봤고 **`MeetingMaterials`·`ActionCenter` 는
9회 모두 통과**했다. 내 7회에서는 **그 둘이 다시 흔들렸다.**
→ **흔들리는 자리가 「옮겨간」 것이 아니라, 부하가 걸리면 스위트 전체가 어디서든 한 건씩 흔들린다.**
지금까지 관측된 자리는 최소 **6곳**이다(`task checklist`×2종 · `adjustment and resubmission` ·
`product surfaces` · `MeetingMaterials` · `ActionCenter`). 기계에 사용자 E2E 스택이 떠 있다.

---

## 뮤테이션 — probe 뒤 **원상 복구를 `diff` 로 확인했다**

| # | 무력화한 것 | 결과 | 복구 |
|---|---|---|---|
| A | `projectModel.ts:35` `openLead: 2 → 0` | ✅ **4건 빨강**(WARN-1 닫힘) | ✅ `diff` 동일 |
| B | `openLead: 2 → 4` | ✅ **4건 빨강** | ✅ `diff` 동일 |
| C | `ProjectGantt.tsx` 첫 진입 effect 의존 `[projectId] → []` | ✅ **새 왼쪽밖 테스트 1건만 빨강** | ✅ `diff` 동일 |
| D | `ProjectGantt.tsx` 축 밖 clamp 제거 | ✅ **오른쪽밖 1건 빨강**(왼쪽밖은 못 잡는다 — 위에 적었다) | ✅ `diff` 동일 |

복구 후 `ProjectPage.test.tsx` + `projectModel.test.ts` **37건 통과** · `make frontend-test`
**984/984 통과**로 원상을 다시 확인했다.

---

## 범위 · 다른 팀 영향

- **`backend/` 0줄.** `git status` 의 backend 변경은 전부 **다른 워커(BE)의 것**이고 내가 만진 자리가 없다.
- **FE-5 몫 0줄** — 헤더 생성 버튼·모달 · 우 레일 업무 정보 · 상태 드롭다운 · 좌 레일 헤더 한 줄.
  `ProjectTaskPanel.tsx` · `ProjectManageModal.tsx` · `ProjectSummaryStrip.tsx` · `App.tsx` ·
  `WorkModals.tsx` 는 **mtime 도 안 움직였다**.
- **FE-5 가 알아야 할 것 하나** — `projects.css` 에 주석 4줄이 늘어 **완료 바 규칙이 110 → 114줄**이다.
  선택자로 찾아라(`.scax-pj-gantt__bar--done .scax-pj-gantt__bar-fill`).
  `ProjectRail.tsx` 는 이번 판이 **안 건드렸다** — 앞 판 리포트 §4 의 인수 사항이 그대로 유효하다.
- **BE 영향 0** · **새 API 호출 0** · **새 한국어 문자열 0** · **커밋 0건** (`HEAD = e46ce39`).
- **개발 서버 0회** — `vitest`(jsdom)만 돌렸다.

## 코디에게 남는 것

1. **SPEC §2.4 · L-45** 에 「오늘이 축 밖이면 가장 가까운 끝」 단서 한 줄 (WARN-2).
   왼쪽 밖 = **기간의 첫날**로 정했고 그 테스트가 있다.
2. **완료 바 `opacity:.71`** — 사용자 눈이 최종 판정. 고칠 곳은 `projects.css:114` **한 줄**.
3. **flaky 대장**에 위 6곳(누적). 부하가 걸리면 자리를 가리지 않는다 — FE-4 밖이다.
4. **WARN-5 는 열린 채로 둔다** — 틀고정·색은 사용자 2차 E2E 가 유일한 관측자다.
