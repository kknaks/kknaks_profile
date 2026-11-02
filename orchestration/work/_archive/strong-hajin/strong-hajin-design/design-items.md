# 디자인 수정 항목 — strong-hajin-design

기록 시작: `2026-09-28`
원본: 사용자가 로컬 웹(`http://127.0.0.1:5176`)·Tauri 에서 짚은 것. **이 파일이 이번 작업 범위의 정본이다.**

## 규칙

- 사용자가 말한 것만 적는다. 코디가 화면을 훑어 항목을 늘리지 않는다
- 「원하는 모습」이 비면 비워 둔다 — 추측으로 메우지 않고 `분류` 를 `시안 필요` 로 둔다
- 분류는 셋 중 하나
  - `DS` — 기존 부품·토큰으로 된다 (부품 35종은 `.design-sync/config.json` componentSrcMap)
  - `시안 필요` — 정해진 모습이 없다. DesignSync(프로젝트 `7e839512`) 로 시안 먼저
  - `기능` — 디자인이 아니다. 이번 작업 밖 (새 작업으로 넘긴다)
- `표면` 은 발주 전에 grep 전수조사로 채운다. 항목 접수 시점에는 빈다

## 항목

| # | 화면 · 위치 | 증상 (사용자 말) | 원하는 모습 | 분류 | 표면 | 상태 |
|---|---|---|---|---|---|---|
| 1 | 로그인 `/` — 이메일·비밀번호 입력칸 (`.login-local` > `.scax-textfield`) | 「지금 인풋 박스가 `[ [인풋박스] ]` 이런식으로 돼 있는데 왜 그런걸까?」 | 테두리 한 겹 (DS `.scax-textfield` 껍데기 하나) | DS | 원인 확인됨 → 아래 §원인 1 | 접수 · 원인 확정 · 수정 대기 |
| 2 | 내 업무 → 업무 상세 → 「하위 업무」 구획 | 단추가 둘(「직접 작업 추가」·「하위 요청 보내기」)인데 직접 추가만 인라인 입력칸이다. 인라인은 말이 안 된다 | **단추 하나 「하위 업무 추가」** → 생성 모달. 모달 안 세그먼트(`내 업무`/`요청 업무`)로 갈래를 고르고, 제목은 갈래를 따라 「새 하위 업무 추가」/「새 하위 업무 요청」 | DS(기존 틀 재사용) + BE 한 칸 | 아래 §원인 2 | 설계 확정 · 발주 대기 |

## 원인 기록

### 원인 1 — 항목 #1 로그인 입력칸 이중 테두리

DS 는 **껍데기가 테두리를 갖고 안쪽 `<input>` 은 테두리를 지운다**는 계약이다.

```
frontend/src/styles/components.css:292  .scax-textfield        { border:1px solid var(--scax-color-line); border-radius:…; background:… }
frontend/src/styles/components.css:294  .scax-textfield__input { border:0; outline:0; background:transparent }
```

그런데 DS 이전 시대의 페이지 규칙이 남아 있고, **그쪽이 우선순위에서 이긴다.**

```
frontend/src/styles/screens-a.css:402  .login-local input { height:40px; padding:0 12px; border:1px solid var(--scax-color-line-strong); border-radius:var(--scax-radius-sm); background:…; }
```

- `.login-local input` = 특이도 (0,1,1)
- `.scax-textfield__input` = 특이도 (0,1,0)

그래서 안쪽 `<input>` 이 `border:0` 을 못 받고 자기 테두리·둥근모서리·바탕을 다시 그린다.
껍데기(48px, 테두리 1겹) 안에 다시 40px 테두리 1겹 → `[ [인풋박스] ]`.

`LoginPage.tsx:129·144` 는 이미 DS 껍데기로 옮겨졌는데(`.scax-textfield` + `.scax-textfield__input`),
**같은 이관에서 페이지 규칙 402줄을 걷지 않은 것**이 원인이다. 이관 잔재 한 줄이다.

참고: `components.css:725` 의 전역 폼 기본값은 범인이 아니다 — 선택자가
`input[type="text"], input:not([type]), input[type="date"]` 라서 `type="email"`·`type="password"` 에 안 닿는다.

402줄은 `.effect-note` 와 `.due-text` 사이, kanban 구획 끝에 홀로 끼어 있다 — 로그인 구획(59~116줄)
밖이라 이관할 때 눈에 안 띈 자리다.

**같은 잔재가 다른 자리에도 있을 수 있다** — 발주 브리프에서 「DS 껍데기를 쓰는 자리에 페이지
element 규칙이 겹치는 곳」을 전수조사한다. 402줄만 고치면 목록 밖에서 FAIL 이 난다.

### 원인 2 — 「하위 업무 추가」 단일 입구 (2026-09-28 사용자 확정)

#### 지금

```
WorkModals.tsx:1819  「직접 작업 추가」  → setNewChild("")      → 인라인 입력칸(제목 한 칸)
WorkModals.tsx:1822  「하위 요청 보내기」→ openSubtaskRequest() → 생성 모달(요청 갈래로 잠김)
WorkModals.tsx:1855~ 인라인 본체 `.inline-reason` + input + 「만들기」
WorkModals.tsx:1069  addSubtask() → createDirectTask(title, { parent_task_id }, key)
```

#### 확정 설계

- 단추 **하나** 「하위 업무 추가」 → 생성 모달(`CreateTaskModal`)
- 모달 헤더 세그먼트 `내 업무` / `요청 업무` 로 갈래를 고른다 — **이미 있는 부품이다**
- 모달 제목은 갈래를 따른다: 「새 하위 업무 추가」 / 「새 하위 업무 요청」
  (기존 규칙과 같다 — `WorkModals.tsx:4049` 이 이미 갈래를 따라 이름을 바꾼다. 「하위」만 붙는다)
- 「업무 연결」 탭의 상위 업무는 지금 열린 업무로 채워진 채 뜬다
- 인라인 입력칸은 **지운다**

#### 걸리는 것 — V-8 중심 업무 규칙

```python
application.py:489  if assignee_id == holder and not self._is_central_task(parent):
application.py:491      raise TaskDirectNesting("직접 작업은 중심 업무의 바로 아래에만 둘 수 있습니다")
application.py:464  중심 업무 = 부모가 없다 or 부모를 든 사람 != 이 업무를 든 사람
```

부모가 중심 업무가 아니면 「내 업무」 갈래는 400 이다. 요청 갈래는 언제나 된다.

지금 프론트는 이것을 **너무 넓게** 잠근다 — 부모가 중심 업무여도 요청 전용이 된다.

```js
WorkModals.tsx:3529  const requestOnly = Boolean(initial?.parentTaskId || initial?.supersedesRequestId);
```

`parentTaskId` 만으로 잠그는 부분을 걷고, **부모가 중심 업무인지**로 판정하게 바꾼다.
`supersedesRequestId`(재요청) 쪽 잠금은 그대로 둔다.

#### 결정 — 부모가 중심 업무가 아닐 때 (2026-09-28 사용자 확정)

**「내 업무」 탭을 비활성으로 세우고 이유를 말한다.** 탭을 아예 안 그리지 않는다 —
칸이 통째로 사라지면 「왜 여기만 요청밖에 없지」가 다시 질문이 된다.

문구는 서버 메시지를 그대로 쓴다: 「직접 작업은 중심 업무의 바로 아래에만 둘 수 있습니다」

수락 전 요청이 부모면 **둘 다** 막힌다(`TaskParentUnassigned`) — 그때는 모달을 열지 않고
기존처럼 「수락 후에 다시 시도하세요」를 낸다.

#### 이 항목은 순수 프론트가 아니다

중심 업무 판정은 **부모를 든 사람 != 이 업무를 든 사람**인데, 프론트 타입에 그 값이 없다
(`types.ts`·`api.ts` 에 `central` 류 칸 없음). envelope 에 칸 하나가 필요하다 — backend 워커 몫.
지금 인라인은 눌러보고 에러를 받는 식이라 이 값이 필요 없었다.

#### 발주 브리프에서 전수조사할 것

`setNewChild` · `addSubtask` · `subtaskAttempt` · `openSubtaskRequest` · `requestOnly` 를 쓰는 자리 전부,
그리고 인라인 입력칸·단추 두 개를 겨냥한 테스트. 목록 밖에서 FAIL 이 난다.

## 분류 밖으로 빠진 것

기능 요청이나 이번 작업에서 빼기로 한 것. 잃지 않기 위해 여기 남긴다.

| # | 무엇 | 왜 뺐나 | 어디로 |
|---|---|---|---|
| | | | |

## 아직 안 정한 것

- **항목 2** — envelope 에 실을 칸 이름·모양 (`parent_is_central` 류). backend 워커 브리프에서 정한다

## e2e 피드백 (2026-09-28 · 사용자 실물 확인)

| # | 화면 · 위치 | 증상 (사용자 말) | 원하는 모습 | 상태 |
|---|---|---|---|---|
| 4 | 업무 상세 → 체크리스트 칸 | 「이거 디자인 이상한데?」 | 스크롤 통에 목록만. 빈 상태·입력폼은 통 밖 | **수정됨** (`WorkModals.tsx`) |
| 5 | 업무 상세 → 하위·선행·참고·후행 목록 | 「목록 형태의 디자인이 아니라 그냥 컴포넌트가 이어져 있는 형태야」 | 테두리 통·행 구분선 없이 부품이 이어진다 | **대기 — 칩(가) / 세로 쌓기(나) 미정** |
| 6 | 업무 상세 → 덩어리 순서 | 「이 영역은 연관 업무 전에 나와야 할 거 같은데」 | `업무 정보` → **`진행과 판단`** → `연관 업무` → `자료` → `이력` | 접수 |
| 7 | 업무 상세 → 막힘 사유 | 「막힘사유도 까만색 글씨에」 | `.danger-text`(빨강) → 검정 | 접수 |

#6 근거: 막힘 사유·담당자 변경은 **지금 이 업무의 상태**다. 관계보다 먼저 읽혀야 한다.
#5·#6·#7 은 같은 파일(`WorkModals.tsx`·`task-detail.css`)이라 **한 판에 묶어 발주한다.**
