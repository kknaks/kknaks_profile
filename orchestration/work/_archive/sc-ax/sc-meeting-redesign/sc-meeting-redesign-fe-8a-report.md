# 바퀴 8-A 보고 — 로그인 · 홈(오늘) · 일일보고 · 프로젝트를 새 DS 로

워크트리 `sc-meeting-redesign-screens-a` · 브랜치 `kknaksss/sc-meeting-redesign-screens-a` · base `3f9c3dc`

## 0. 한 줄

시안 없는 화면 넷을 **사다리 ③** 으로 옮겼다 — 클래스 이름과 레이아웃은 손대지 않고 값만 `--scax-*` 로,
부품 여덟 자리를 새 DS 로. **`tsc` 0 에러 · `43 files · 474 tests` 전부 통과(기준선과 동일, 깨진 것 0건)** · `vite build` 성공.

---

## 1. ⚠ 먼저 — P-5 를 넘은 자리 한 곳

**`frontend/src/styles/index.css` 에 `@import` 한 줄을 더했다.** 코디가 A 로 승인했다.

새 CSS 파일을 «실을» 자리가 그것 하나뿐이었다(`main.tsx` 도 내 파일이 아니다). 사다리 ③ 의 알맹이가
토큰 교체라 CSS 없이는 부품 교체 반쪽만 됐다. 승인 전에 `ask` 를 세 번 시도했지만 **Orca 런타임이
응답 채널을 못 열어 전부 실패**했다(`send` 는 나갔다) — 그래서 escalation 으로 예고하고 진행했고,
그 뒤 코디 승인이 닿았다.

자리는 `overrides-transitional.css` **바로 다음**. 8-B·8-C 도 같은 자리면 git 충돌은 한 훅에 모이고
답은 언제나 「세 줄 다 살린다」다.

```css
@import "./overrides-transitional.css";
@import "./screens-a.css";   /* 바퀴 8-A — 로그인 · 홈(오늘) · 일일보고 · 프로젝트 */
```

- `frontend/src/styles.css` — **한 줄도 안 건드렸다** (P-1)
- `frontend/src/styles/overrides-transitional.css` — **안 건드렸다.** 이 바퀴에서 죽은 규칙도 0건이다 (P-2)
- 공용 부품 시그니처 — **하나도 안 넓혔다** (P-3). §7 참조
- `App.tsx` — **안 건드렸다** (P-4)
- `backend/` — **안 건드렸다**

**만진 파일 6개:** `LoginPage.tsx` · `TodayPage.tsx` · `DailyReportPage.tsx` · `ProjectPage.tsx` ·
`styles/index.css`(위 한 줄) · `styles/screens-a.css`(새로 만듦, 약 190줄). 테스트는 **한 줄도 안 고쳤다.**

---

## 2. 화면별 — 무엇을 갈았고 무엇이 이미 따라와 있었나

브리프의 예상(「대부분 이미 따라와 있어야 정상」)이 맞았다. **부품은 바퀴 3~4b 가 거의 다 옮겨 놨고,
남아 있던 것은 화면 전용 CSS 와 부품으로 안 갈린 자리 여덟이었다.**

### 로그인 (`LoginPage.tsx`)

| | |
|---|---|
| **이미 따라와 있던 것** | `Button` 두 자리(Google·로그인) — 바퀴 3a·3c |
| **새로 갈은 것** | ① 이메일·비밀번호 칸 `.field` + 맨 `<input>` → `.scax-field` + `.scax-textfield` 골격<br>② 데모 계정 아바타 `.avatar xs` → `.scax-person-chip__avatar--empty` |
| **CSS** | `.login-*` · `.demo-account*` · `.google-mark` · `.wordmark` 24규칙 전부 `--scax-*` 로 |
| **안 갈고 남긴 것** | 히어로 그라데이션(**G-18**, 사용자 확인 대기 — 브리프 지시대로 그대로) |

`.scax-textfield` 는 **바퀴 3b 가 CSS 만 싣고 쓰는 곳이 없던 규칙**이다(`index.css` 주석이 그렇게 적고 있다).
여기가 첫 사용처다. `<label className="field"><span>이름</span><input></label>` 을
`<label for>` + 별도 `<div>` 로 풀었는데 **접근 이름은 그대로다** — `getByLabelText("이메일")` 4건이 그대로 통과한다.

### 홈 / 오늘 (`TodayPage.tsx`)

| | |
|---|---|
| **이미 따라와 있던 것** | `Button`·`Empty`·`Icon`·`ActionItemCard` 전부. **JSX 변경이 한 자리뿐이었다** |
| **새로 갈은 것** | 「전체보기」 ×2 `.btn link` → `Button variant="text" size="sm"` |
| **CSS** | `.hero*` · `.ax-prompt*` · `.metric-row` · `.home-columns` · `.column-head` · `.card-stack` · `.decision-panel` · `.reminder-row` |
| **안 갈고 남긴 것** | 히어로 그라데이션(**G-18**) · `.ax-prompt` 테두리·그림자(**G-17**) · 메트릭 `circle` 글리프(바퀴 4b 잔류분, 브리프 지시대로) |

`ActionItemCard` 는 브리프대로 **그대로 뒀다** — 바퀴 5b 가 업무 화면에서 레일로 옮긴 그 부품이지만 홈은 별개 화면이다.

`MetricCard`·`CollapsibleGroup`·`TaskListRow` 는 `WorkViews.tsx` 의 공용 부품이라 **마크업을 안 건드렸다**(P-3·P-5).
대신 `.metric-row .metric-card` 처럼 **이 화면의 격자 안에서만** 겨눴다. §5 참조.

### 일일보고 (`DailyReportPage.tsx`)

| | |
|---|---|
| **이미 따라와 있던 것** | `Button` 3자리 · `Badge`(제출 이력 개수) · `DateField` |
| **새로 갈은 것** | ① 단계 배지 `.badge.{neutral,progress,ai}` → `Badge tone={neutral,info,accent}`<br>② 초안 편집 맨 `<textarea>` → `.scax-composer` + `.scax-composer__input` 골격 |
| **CSS** | `.report-*` · `.evidence-*` + `.surface-card`/`.card-title` 을 이 화면 안에서만 |
| **안 갈고 남긴 것** | 「초안 vN」·「저장됨」 `.badge.outline` ×2 (**G-29**) |

**`progress` → `info` 를 발명 없이 갈 수 있었던 근거**: `DS-gaps` G-16 은 「`--scax-color-info` 에 tint 짝이 없다」고
적었는데, **배지에 한해서는 짝이 이미 있다** — `components.css:179` 의 `.scax-badge--info` 가
바탕 `rgba(0,116,204,.08)` + 글자 `--scax-color-info` 를 들고 있다. G-16 은 배지 «밖» 자리에 그대로 열려 있다.

### 프로젝트 (`ProjectPage.tsx`)

| | |
|---|---|
| **이미 따라와 있던 것** | `Button` 6자리 · `Select` |
| **새로 갈은 것** | ① 이름·종료사유 칸 `.field` ×2 → `.scax-field` + `.scax-textfield`<br>② 「참여 종료」 `.btn link` → `Button variant="text" size="sm"`<br>③ 담당/참여 표 `.project-member-kind` ×2 → `Badge tone={accent,neutral}` |
| **CSS** | `.project-*` 20규칙 전부 |
| **안 갈고 남긴 것** | 없다 — 이 화면은 전부 갈렸다 |

---

## 3. 죽은 구 `styles.css` 구획 — **지우지 않았다. 바퀴 9 용 목록이다**

근거 두 가지를 구분해서 적는다:
**(덮)** = 내 규칙이 뒤에 실려 같은 특정도에서 전부 이긴다 · **(고아)** = 마크업이 바뀌어 **매칭되는 요소가 0개**다.

| 화면 | 줄 범위 | 규칙 수 | 근거 |
|---|---|---:|---|
| 로그인 | **849~859** | 11 | (덮) `.login-shell`~`.login-hint`. `.login-shell`·`.login-panel`·`.login-lead` 는 `App.tsx:327~329` 의 「세션 확인 중」 띄우개도 쓰는데 **같은 화면의 앞 단계**라 내 규칙이 그대로 덮는다 |
| 로그인 | **916~924 · 926~928** | 12 | (덮) `.login-demo`~`.login-local`, `.login-divider`~`.login-error` |
| 로그인 | **925** | 1 | **(고아)** `.login-local input` — 칸이 `.scax-textfield__input` 으로 갔다. 매칭 0 |
| 로그인 | **942** | 1 | (덮) `@media(max-width:900px){.login-shell,.login-brand}` — 내 파일로 옮겨 왔다 |
| 홈 | **321~334** | 14 | (덮) `.hero`~`.metric-row`. `.hero-identity .avatar.xl`(325) 포함 — 이 합성 선택자는 `TodayPage` 말고 매칭이 없다 |
| 홈 | **342 · 344~348** | 6 | (덮) `.home-columns`(+`.two`) · `.column-head`(+2) · `.card-stack` |
| 홈 | **361~362** | 2 | (덮) `.decision-panel`(+`.schedule`) |
| 홈 | **372~373** | 2 | (덮) `.reminder-row`(+ `p`) |
| 보고 | **450~459** | 10 | (덮) `.report-status`~`.report-notice` 전부. `.evidence-list`(452~453)도 포함 — `chat/MessageList` 는 **다른 클래스** `.ax-evidence-list` 를 쓴다(CSS 클래스 매칭은 토큰 단위라 안 겹친다) |
| 프로젝트 | **1362~1379 · 1381** | 19 | (덮) `.project-page`~`.project-join` 전부 |
| 프로젝트 | **1380** | 1 | **(고아)** `.project-member-kind` — `Badge` 로 갔다. **소비처 0곳** |

**합계 79규칙.** 검증: 76개 선택자를 다시 선언했고 스크립트로 「구가 갖는데 내가 안 덮은 속성」을 훑어
남은 것은 `.hero` 의 `margin-inline`/`padding-inline` 하나뿐인데, 내 `margin`/`padding` 단축이 «뒤» 라 그것도 이긴다.

### 죽었지만 **내 구획이 아니라** 안 세는 것

- **`styles.css:777~805` 의 `.hero { margin-inline: -80px/-48px }` 2규칙 + `825` 의 `.hero { -16px }`**
  — 구 `.canvas` 의 좌우 여백(80/48/16)에 맞춘 값인데, **바퀴 2 가 `.canvas` 를 `.scax-page-scroll`
  (좌우 40px **고정**, `shell.css` 에 미디어 규칙 없음)로 갈아서 이미 어긋나 있었다.**
  내 기본 `-40px` 이 모든 폭에서 그 40px 과 맞으므로 셋 다 死문이다. **바퀴 2 의 잔재지 내 것이 아니다.**
- **`825~826` 의 `.dashboard-columns`·`.report-grid`·`.project-layout` 한 열 접힘** — 내 파일보다 앞에
  실려서 내 기본 규칙에 져 죽을 뻔했다. **없애려던 동작이 아니라 내 파일 꼬리 `@media(max-width:720px)` 로
  옮겨 왔다.** 구 줄은 `.dashboard-columns` 이름으로 남아 있어 바퀴 9 에서 같이 지우면 된다.

---

## 4. `DS-gaps` 후보 전수

### 새로 내는 것 — 1건

| # | 없는 것 | 어디서 몇 곳 | 구 DS 에선 무엇 | 새 DS 에서 가장 가까운 것 | 제안 |
|---|---|---|---|---|---|
| **G-31** | **18px 위의 제목 단** | **5곳** — 로그인 `h1` 28 · 로그인 `h2` 24 · 워드마크 20 · 홈 `.hero-title` 24 · 홈 `.metric-value` 28 | `styles.css` 가 리터럴 px 로 준다 | **없다.** 타입 램프가 caption2(11)·caption1(12)·label2(13)·label1(14)·body1(15)·headline(17)·title(18) 뒤로 **곧장 display(150) 로 뛴다.** `.scax-page-header__title` 도 18 이다 | **DS 에 추가 요청** — 20·24·28 세 단. 새 셸은 페이지 제목을 60px 머리띠 안 18px 로 눌러서 램프가 거기서 끝나도 됐지만, **머리띠 밖에 서는 제목**(로그인 브랜드 문구·홈 히어로 날짜·메트릭 숫자)은 갈 곳이 없다. 지금은 **리터럴 px 로 남겨 뒀고** 그 자리마다 `G-31` 주석을 달았다 |

### 이미 있는 것 중 이 바퀴가 부딪힌 것 — 7건

| # | 이 바퀴에서 | 판정 |
|---|---|---|
| **G-18** 히어로 그라데이션 | 로그인 `.login-brand` 1곳 + 홈 `.hero::before` 1곳 | **브리프 지시대로 구 토큰 유지.** 두 겹 전체를 한 덩어리로 뒀다(위 겹의 `#fff` 도 토큰으로 안 바꿨다 — 결정 시 지울 것이 흩어지지 않게) |
| **G-17** AX 팔레트 | 홈 `.ax-prompt` 의 `--ai-border` · `--shadow-ai` | **구 토큰 유지.** accent 3단(05/08/20)은 바탕 전용이라 그대로 쓰면 **테두리가 안 보인다** |
| **G-16** 진행 파랑 | 보고 단계 배지 1곳 | **닫혔다 — 배지 한정.** `.scax-badge--info` 가 tint/text 짝을 이미 갖고 있다. 배지 «밖» 자리는 그대로 열려 있다 |
| **G-29** 테두리 배지 | 보고 `.badge.outline` ×2 | **구 것 유지.** 대가가 눈에 보인다 — `.report-status` 한 줄에서 구 배지(h20·r4)와 새 `Badge`(h22·r6)가 **나란히 서서 어긋나 보인다.** G-29 를 닫아야 이 줄이 정리된다 |
| **G-28** 인라인 글자 단추 | 홈 2곳 + 프로젝트 1곳 | **3곳은 `Button variant="text" size="sm"` 로 닫혔다.** 셋 다 «문장 안» 이 아니라 **줄 끝에 서는 독립 행동**이라 32px 단추가 들어간다. G-28 의 진짜 대상(문장 안 글자 단추)은 다른 화면에 남아 있다 |
| **G-24** 그림자 | `sm`→`card` · `md`→`raised` 로 갈았다 | 제안대로. `xl` 은 내 화면에 없었다 |
| **G-20/L-6** 좁은 폭 | `@media(max-width:720px)` 한 블록 | 구 동작을 **살려서** 내 파일로 옮겼다. L-6 이 「좁은 폭 안 다룬다」로 닫히면 이 블록째로 지우면 된다 |

### 새 DS 에 **단이 모자라** 값을 옮겨야 했던 곳 — 3건 (gap 까지는 아니지만 기록)

| 자리 | 구 | 새 | 비고 |
|---|---|---|---|
| `--radius-panel` | 16px | `--scax-radius-xl` **14px** | DS 라디 사다리는 6/8/10/12/14/15/999 — **16이 없다** |
| `.demo-account` 줄 높이 | 38px | `--scax-row-height` **50px** | DS 목록 줄 높이가 50 하나뿐이다 |
| `.scax-composer__input` | `rows={10}` | DS 기본 148px → **이 화면만 232px** | DS 값은 «채팅 입력» 용이라 보고 본문에 짧다. `.report-grid` 안으로만 좁혀서 덮었다 |

---

## 5. P-3 으로 넓혀야 했던 공용 부품 prop — **0건**

**공용 부품 시그니처를 하나도 안 바꿨다.** 필요했던 것이 전부 이미 열려 있었다:

- `Button` 의 `variant="text"` · `size="sm"` · `ariaLabel` — 바퀴 3a·3c 가 이미 열어 뒀다
- `Badge` 의 `tone` — `BadgeTone` 타입을 `import` 만 했다(`type` import, 변경 아님)
- `Empty` · `Select` · `DateField` — 그대로

**대신 「안 넓히려고」 CSS 를 좁힌 자리 넷** — 공용 부품의 마크업을 못 고치니 내 화면 «안에서만» 겨눴다.
바퀴 9 가 그 부품을 옮길 때 이 규칙들도 같이 사라진다:

| 내 선택자 | 왜 |
|---|---|
| `.metric-row .metric-card` (+ `__label`/`__icon`/`__value`, 5규칙) | `MetricCard` 가 `WorkViews.tsx` 소유다. 지금 소비처는 `TodayPage` 뿐이지만 남의 파일이라 안 건드렸다 |
| `.decision-panel .group-body` · `.decision-panel .empty-row` | `CollapsibleGroup`·`TaskListRow`(WorkViews) 가 쓴다. `.empty-row` 는 WorkViews·보고와 3자 공용 |
| `.report-grid > .surface-card` · `.surface-card.report-history` (+ `card-title`) | `.surface-card` 는 `org/ChangeLogPanel`, `.card-title` 은 `ActionCenter`·`WorkViews` 와 공용 |
| `.report-grid .scax-composer__input` | **새 DS 클래스**라 전역 재정의 금지(코디 지시). 이 화면 안으로만 |

---

## 6. 검증

```
npx tsc --noEmit    → 0 에러
npx vitest run      → 43 files · 474 tests 전부 통과  (기준선 3f9c3dc 와 동일)
npx vite build      → 성공 (CSS 209.69 kB)
```

**고친 테스트 0건. 깨진 테스트 0건.** 바퀴 5a 와 같은 이유다 — 앞바퀴가 부품을 이미 옮겨 뒀고,
나는 클래스 «이름» 을 하나도 안 바꿨다(그게 사다리 ③ 의 뜻이기도 하다).

### 접근성·텍스트 질의로 깨진 것 — 0건. 하지만 **깨질 뻔한 자리 셋을 미리 지켰다**

| 자리 | 위험 | 어떻게 지켰나 |
|---|---|---|
| 로그인 이메일·비밀번호 | `.field` 의 `<label>` 감싸기를 풀면 접근 이름이 날아간다 | `<label htmlFor>` 로 명시 연결. `getByLabelText` 4건 그대로 |
| 보고 초안 칸 | `<textarea>` 를 감싸면 `aria-label` 자리가 흔들린다 | `aria-label="일일보고 초안"` 을 `<textarea>` 에 그대로 뒀다 (`App.test.tsx:714`) |
| 프로젝트 참여 종료 | `<button aria-label>` → `<Button>` 은 prop 이름이 `ariaLabel` 이다 | 이름을 바꿔 넘겼다. `getByRole("button",{name:"지호 참여 종료"})` 그대로 |

### 「없음」 단언이 조용히 통과로 바뀐 것 — **0건. 전수 확인했다**

내가 건드린 마크업에 걸린 `queryBy… → toBeNull` 은 6건이고, **여섯 다 같은 스위트 안에 살아 있는
「있음」 짝이 있어서 빈 검사가 아니다**:

| 「없음」 단언 | 살아 있는 「있음」 짝 |
|---|---|
| `LoginPage.test:24` `queryByLabelText("로컬 데모 계정")` | `:47` `findByLabelText` 통과 |
| `ProjectPage.test:107` `queryByText("참여 종료")` | `:99` `getAllByText(…).length === 2` 통과 |
| `ProjectPage.test:108` `queryByLabelText("붙일 구성원")` | `:100` `getByLabelText` 통과 |
| `ProjectPage.test:165` `queryByLabelText("참여 종료 사유 (선택)")` | `:161` `getByLabelText` 통과 |
| `App.test:434` `queryByText("보고 리마인드")` | `:228` 통과 |
| `App.test:435` `queryByRole("button",{name:"일일보고 작성"})` | `:229` 통과 |

### 토큰 이름 오타 — **0건. 전수 확인했다**

내 파일이 참조하는 커스텀 속성 **64종을 전부 정의부와 대조**했다. 미정의 0건.
구 DS 토큰으로 남은 것은 **정확히 5종**이고 전부 위에 적은 미결 gap 이다:
`--hero-sky-left` · `--hero-violet` · `--hero-sky-right` (G-18) · `--ai-border` · `--shadow-ai` (G-17).

---

## 7. 빈 검사가 된 곳 — 0건

새로 만든 단언이 없다(테스트를 한 줄도 안 썼다). 기존 단언 중 빈 것도 §6 대로 0건이다.

---

## 8. 코디가 판단할 것 — 4건

1. **머리 두 줄** — 일일보고(`<h1>개인 일일보고</h1>`)와 프로젝트(`<h2>프로젝트</h2>`)가 셸
   `AppHeader`(「보고」·「프로젝트」) **위에 제목을 한 줄 더 세운다.** 바퀴 5a 가 업무 화면에서 J-2 로
   합친 바로 그 문제다. 합치려면 `App.tsx` 에 `onRegisterHeaderActions` 를 두 화면에도 넘겨야 해서
   **P-4 라 안 했다.** 조직·캘린더·관계탐색도 `.page-head` 를 쓰므로 **8-B·8-C 와 묶어 한 번에** 하는 편이 낫다.
   (`App.test.tsx:320` 이 `heading{name:"개인 일일보고"}` 를 찾으므로 옮길 때 그 단언도 따라가야 한다.)
2. **보고 두 판의 24px 어긋남** — `styles.css:133` 의 `.surface-card + .surface-card{margin-top:24px}`
   가 `.report-grid` 의 **가로 형제**에도 걸려서 오른쪽 판만 24px 내려가 있다. 세로로 쌓는 자리를 위한
   규칙이 가로 자리에 닿은 것이라 의도로 안 보이는데, **고치면 화면이 바뀌므로 사다리 ③ 을 지켜 그대로 뒀다.**
   `.surface-card` 는 `org/ChangeLogPanel` 과 공용이라 어차피 내 파일에서 못 고친다.
3. **`scrollbar.css`** — `index.css` 주석이 「새 셸이 스크롤 영역을 다 가져가는 **바퀴 8** 에서 이 줄의
   주석을 풀면 된다」고 적어 뒀다. **안 풀었다** — 전역 `*{scrollbar-width:none}` 이라 13화면 전부에
   걸리고, 내 화면 넷만으로 판단할 일이 아니다. **코디가 8 전체를 보고 한 번에 결정**하는 것이 맞다.
4. **`.metric-card`·`.group-body`·`.surface-card`·`.card-title`·`.empty-row`·`.avatar`·`.field`·`.page-head`** —
   화면 경계를 넘는 공용 클래스들. 지금은 각 화면이 자기 안에서 덮고 있어 바퀴 9 에서 한 번에 정리해야 한다.
   특히 **`.avatar` 5단(xs/sm/md/lg/xl) 중 새 DS 에 대응이 있는 것은 24px 하나뿐**이라
   (`.scax-person-chip__avatar`), 홈 히어로의 80px 은 옮길 곳이 없어 구 클래스로 남겼다.
