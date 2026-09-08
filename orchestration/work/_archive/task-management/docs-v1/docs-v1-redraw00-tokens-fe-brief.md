# [frontend] REDRAW-00 — 토큰 층을 시안대로 되돌린다

너는 **task-management `frontend` 워커**다. 먼저 역할 문서를 읽어라 (**문서 레포 절대경로 — read-only**):

- `/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/orchestration/roles/task-management/frontend/role.md`

작업 워크트리: `/Users/kknaks/orca/workspaces/task_management/docs-v1`
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

> **앞선 REDRAW-01 브리프는 폐기됐다.** 「처음부터 그려라」가 잘못이었다.
> 삭제됐던 화면 84개는 **전부 복구됐고 `tsc --noEmit` 0 에러**다.
> **동작은 이미 다 짜여 있다. 우리가 고치는 것은 시각뿐이다.**
> 네가 만들었던 `components/ui/{Button,Toast,Checkbox,Input}.tsx` · `styles/tokens.css` ·
> `app/globals.css` · `tailwind.config.ts` 는 코디가 이미 지웠다. 다시 만들지 마라.

---

## 0. 왜 이 work 이 있나

지난 파이프라인은 시안 `.dc.html` 을 한 번도 열지 않고, 디자이너가 **글로 요약한
`00-design/09-design-tokens.md`** 만 보고 토큰을 만들었다. 그래서 값이 어긋났고 화면이 전부 틀어졌다.

**증거가 파일 첫 줄에 있다:**

```
원시 디자인 토큰 — `00-design/09-design-tokens.md` 의 값을 그대로 옮긴 곳.
```

**요약본이 정본으로 박혀 있다.** 이 문장부터 고친다.

---

## ⛔ 1. 정본

| 순위 | 무엇 | 어디 |
|---|---|---|
| 1 | **사용자 승인 정정** | `orchestration/work/docs-v1/design-requests.md` §A |
| 2 | **시안 — 시각 정본** | `00-design/*.dc.html` |
| 3 | **SPEC — 동작 정본** | `20-spec/` |

**이 work 은 시각만 다룬다. 동작은 건드리지 않는다.**

### 반드시 열 파일 (절대경로 · 읽기 전용)

```
/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/para/projects/summer-star/task-management/00-design/디자인 시스템.dc.html
```

**`00-design/*.md` 요약본(특히 `09-design-tokens.md`)은 열지 마라.** 그것이 사고의 원인이다.

---

## 2. 범위 — 파일 3개뿐

| 파일 | 무엇 |
|---|---|
| `src/styles/tokens.css` | 값 정정 + 누락 토큰 추가 |
| `src/styles/globals.css` | `--background` 매핑 정정 |
| `tailwind.config.ts` | 새로 생긴 토큰 연결 |

**하지 않는 것**
- **화면·컴포넌트 파일을 하나도 건드리지 마라.** `components/` · `features/` · `app/` 전부 손대지 않는다
- 토큰을 지우지 마라. 값만 고치고 없는 것만 더한다
- **팔레트 8종(`--tm-palette-*`)은 그대로 둬라.** 정정 A-1 로 유형이 동적이 된 뒤 SPEC-002 §4 가 정한 값이고 시안 소관이 아니다
- 아래 §3 에 없는 토큰은 건드리지 마라 (`--tm-current-bg` · `--tm-row-hover` · `--tm-row-add-bg` · `--tm-drop-placeholder-*` 등은 시안과 일치한다)

---

## 3. 고칠 것 — 7건

시안 `디자인 시스템.dc.html` 의 **01 COLOR · 03 TYPE · 04 LAYOUT · 05 SURFACE · 07 OVERLAY** 를 열고 대조해라.
아래는 코디가 뽑은 값이다. **시안과 다르면 시안이 맞다.**

### F-1. 배경 — 회색 사고의 원인

```css
/* tokens.css */
--tm-canvas: #f4f5f7;   →   --tm-canvas: #F9FAFB;
```

시안 01 COLOR 의 Canvas 는 **`#F9FAFB`** 다. `#F4F5F7` 은 **취소 배지 bg**·**개인 업무 일정블록 bg** 로만 쓰이는 값이고 배경 토큰이 아니다.

```css
/* globals.css */
--background: var(--tm-canvas);   →   --background: var(--tm-surface);
```

**body 는 흰색이다.** 근거 둘 —
- 시안 10 RULES 「그라디언트는 홈만」: **「앱 안쪽 화면은 흰 배경 + breadcrumb + 타이틀로 시작합니다」**
- 모든 화면 `.dc.html` 의 `<section>` 이 `background:#FFFFFF` 다

**이 두 줄이 지난 사고의 전부다.** `--tm-canvas` 는 정의만 남기고 body 에 쓰지 마라.

> **보고할 것**: `--tm-column: #f9fafb` 가 정정 후 `--tm-canvas` 와 같은 값이 된다. **중복이지만 지우지 마라** — 어느 쪽이 칸반 컬럼 배경인지는 `업무 화면 정의서.dc.html` 을 봐야 하고 그건 다음 work 이다. **완료 보고에 한 줄로 남겨라.**

### F-2. radius — 시안은 둘이다

```css
--tm-radius-card: 16px;   /* 하나로 뭉개져 있다 */
```

시안 05 SURFACE —
- **Card · r8 · border `#D9D9D9`**
- **Panel · r16 · border `#D9D9D9`**

둘로 나눠라: `--tm-radius-card: 8px` · `--tm-radius-panel: 16px`
`--tm-radius-control: 8px` · `--tm-radius-chip: 4px` 는 그대로 둔다.

> `--tm-radius-card` 를 8 로 내리면 **지금 그 변수를 쓰는 화면의 모양이 바뀐다.** 그게 이 work 의 목적이다. 화면 파일은 고치지 말고, 어떤 파일이 이 변수를 쓰는지 `grep` 해서 **완료 보고에 목록만** 남겨라.

### F-3. 그림자 — 시안은 4종

지금은 `--tm-shadow-card` 하나에 뭉쳐 있고 값도 어느 쪽과도 안 맞는다. 시안 05 SURFACE 그대로 넷으로 나눠라.

| 토큰 | 값 |
|---|---|
| `--tm-shadow-card` | `0 1px 2px rgba(16,24,40,0.03)` |
| (panel) | **그림자 없음** — 토큰을 만들지 마라 |
| `--tm-shadow-metric` | `0 1px 2px rgba(16,24,40,0.04), 0 8px 20px rgba(16,24,40,0.05)` |
| `--tm-shadow-floating` | `0 1px 2px rgba(16,24,40,0.04), 0 12px 30px rgba(16,24,40,0.06)` |
| `--tm-shadow-ai` | `0 1px 2px rgba(16,24,40,0.04), 0 10px 24px rgba(89,105,214,0.10)` + border `#DDE1F6` |

### F-4. 모달 그림자

```css
--tm-shadow-modal: 0 32px 80px rgba(0,0,0,0.28);
   →                0 16px 40px rgba(0,0,0,0.28);
```
시안 07 OVERLAY 의 Modal 값이다.

### F-5. 브랜드 그라디언트 — 지어낸 값이다

지금 radial 2겹이 **흰색 `0.72` + 보라 `0.16`** 인데 시안엔 그런 값이 없다.
시안(`로그인 · 계정 · 프로필.dc.html` 24~25줄, 좌측 브랜드 패널)은 이것이다:

```css
--tm-brand-gradient:
  radial-gradient(58% 60% at 18% 8%,  rgba(146,155,245,0.28) 0%, rgba(146,155,245,0) 62%),
  radial-gradient(60% 70% at 92% 78%, rgba(160,190,255,0.34) 0%, rgba(160,190,255,0) 66%),
  linear-gradient(160deg, #DCE6FB 0%, #E7EDFC 34%, #F5F8FE 68%, #FFFFFF 100%);
```

색·위치·크기·정지점이 전부 다르다. **그대로 갈아끼워라.**
(홈 화면의 Hero Gradient 는 `180deg` 로 각도가 다르지만 홈은 v1 범위 밖이라 만들지 않는다.)

### F-6. 없는 색 5개

시안 01 COLOR 에 있는데 토큰에 없다.

```css
--tm-hero-top: #DCE6FB;
--tm-sky-200: #BACFFF;
--tm-violet-300: #929BF5;
--tm-row-selected: #F8FAFF;   /* 01 COLOR 「Row Selected」 */
--tm-success: #3BA776;         /* 07 Password Strength 충족 체크 · 목소리 「등록됨」 */
```

### F-7. 없는 스케일 2종

시안 03 TYPE · 04 LAYOUT 에 있는데 토큰에 없다. 지금은 화면들이 숫자를 직접 쓰고 있다.

**타이포** — 전역 `letter-spacing -0.02em`(있음), 큰 제목만 `-0.03em`

| 역할 | 크기 / 굵기 | 비고 |
|---|---|---|
| page-title | 28 / 700 | `-0.03em` |
| hero-date | 24 / 700 | `-0.03em` |
| panel-title | 16 / 700 | |
| section | 15 / 700 | |
| group-header | 14 / 700 | |
| item | 14 / 600 | |
| body | 15 / 400 | line-height 1.65 |
| meta | 13 | `#757575` |
| caption | 12 | `#9EA2AE` |
| metric | 28 / 700 | |

**스페이스** — `4 · 8 · 12 · 16 · 24 · 32 · 48`

둘 다 `tailwind.config.ts` 에 연결해서 화면이 유틸로 쓸 수 있게 해라. **이번 work 에서 화면을 고쳐 적용하지는 않는다.**

### F-8. 파일 헤더 주석

`tokens.css` 첫 줄의 정본 표기를 바꿔라.

```
`00-design/09-design-tokens.md` 의 값을 그대로 옮긴 곳
   →  `00-design/디자인 시스템.dc.html`(시각 정본)에서 뽑은 값.
      요약본 `09-design-tokens.md` 를 참조하지 않는다 — 값이 어긋나 화면을 전부 버린 적이 있다.
```

본문 중간의 다른 주석에도 `09-design-tokens.md` 를 근거로 든 곳이 여러 군데 있다.
**그 근거 표기만 `디자인 시스템.dc.html` 로 바꿔라. 설명 문장은 지우지 마라.**

---

## 4. 검증

```bash
cd app/front && npx tsc --noEmit   # 0 에러. 전체 빌드 금지, 1회만
```

**캡처 2장**
1. `npm run dev` 로 `/login` — **배경이 흰색**이고 좌측 브랜드 패널이 **보랏빛**이다(흰 얼룩이 아니다)
2. `/tasks` — 배경이 흰색이다

> 화면이 시안과 다르게 보이는 것은 **정상이다.** 이 work 은 토큰만 고친다. 화면 정정은 다음 work 이다.
> **캡처를 예쁘게 만들려고 화면 파일을 고치지 마라.**

---

## 5. 지킬 것

1. **파일 3개만 고친다.** `git status` 에 그 셋 말고 다른 게 뜨면 잘못한 것이다
2. **시킨 것만 한다.** 토큰을 지우지 말고, 화면을 고치지 말고, 범위 밖 파일을 만들지 마라
3. **막히면 물어라** — `orca terminal send` 로. `orca orchestration ask` 는 답이 안 닿는다
4. **임의로 정하지 마라.** 시안에 없으면 물어라
5. **커밋·push 하지 마라**

## 6. Done Criteria

- [ ] `--tm-canvas` 가 `#F9FAFB` 이고 `--background` 가 `--tm-surface` 다 → **body 흰색**
- [ ] radius 가 card 8 / panel 16 둘로 갈렸다
- [ ] 그림자가 card · metric · floating · ai 넷이고 값이 시안과 같다
- [ ] `--tm-shadow-modal` 이 `0 16px 40px rgba(0,0,0,0.28)` 이다
- [ ] 브랜드 그라디언트가 시안의 보라 `.28` + 파랑 `.34` 조합이다
- [ ] 없던 색 5개와 타이포·스페이스 스케일이 추가되고 tailwind 에 연결됐다
- [ ] `tokens.css` 헤더가 `디자인 시스템.dc.html` 을 정본으로 가리킨다
- [ ] `npx tsc --noEmit` 0 에러
- [ ] `git status` 에 파일 3개만
- [ ] 캡처 2장
- [ ] **보고에 포함**: `--tm-column` 중복 건 · `--tm-radius-card` 를 쓰는 파일 목록

---

## 7. 질문하는 법 — **`orca orchestration ask` 를 쓰지 마라**

```bash
orca terminal send --terminal term_6a4ac855-2a13-4484-b808-4c25182cbb2b \
  --text "[질문] frontend: <질문>" --enter
```

## 8. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.**

```bash
orca orchestration send \
  --to term_6a4ac855-2a13-4484-b808-4c25182cbb2b --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId> --dispatch-id <이 태스크의 dispatchId> \
  --subject "frontend 완료: <한 줄>" \
  --body "변경 파일 / 시안 대조 결과(F-1~F-8 각각) / tsc 결과 / --tm-column 중복 / --tm-radius-card 사용처 목록"

orca terminal send --terminal term_6a4ac855-2a13-4484-b808-4c25182cbb2b \
  --text "[worker_done] frontend 완료 — <한 줄 요약>. 상세는 인박스." --enter
```
