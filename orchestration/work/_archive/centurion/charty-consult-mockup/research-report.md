# 조사 리포트 — 차티 · 메디킷 · 피부 리포트 (read-only)

- 작성: researcher 워커 · 2026-10-21
- 기준: 메디킷 `main`(55c14a2) · 차티 `origin/stg`(461a48e, v1.8.0-rc.3) · 원본 리포트 저장본 + HAR
- 표기: 메디킷 경로는 `/Users/kknaks/git/medikit` 기준 상대경로, 차티는 `stg:<path>:줄`, 원본은 `ref:<file>`
- ⚠ HAR 의 실명·생년월일·회원번호·리포트 hash·스캐너 시리얼은 옮기지 않았다. 예시 값은 `홍○○` / `****` 로 가렸다.
  측정 수치(점수 등)는 구조 설명용으로만 일부 인용했다.

---

## ⚠ 먼저 알아야 할 것 — 메디킷 버전 불일치

| | 버전 | 근거 |
|---|---|---|
| 로컬 메디킷 `main`(55c14a2) | **0.3.0** | `package.json:3`, 태그는 `v0.1.0` 하나뿐, 원격 브랜치도 `main`·`medi-620`·`medi-646`·`medi-747` 모두 0.3.0 계열 |
| 차티 `origin/stg` 이 쓰는 버전 | **1.4.0** | `stg:frontend/package.json:22` (`"^1.4.0"`), `stg:frontend/pnpm-lock.yaml:11-13,383` (resolved 1.4.0) |

**로컬 체크아웃(main)은 차티가 실제로 쓰는 1.4.0 이 아니다.** 1.4.0 에는 main 에 없는 컴포넌트(Badge·Card·Chip·Progress·Accordion·
Banner·AppTabs·PlanCard 등)와 토큰(yellow 계열)이 있다. 1.4.0 소스 레포 위치는 **확인 안 됨**.
보충으로, 로컬 디스크의 설치본 1.4.0(`/Users/kknaks/orca/workspaces/cc-prototype/myeongdong-poc-v2/procedure/front/node_modules/@medisolve-ai/medikit/dist`,
`package.json` version 1.4.0, repository 동일 `MediSolveAIDev/medikit`)의 `dist/index.d.ts`·`dist/styles/base.css` 를 읽었다.
아래 A 절은 **main 을 기준으로 쓰고, 1.4.0 에서 다른 부분은 「1.4.0」 표시로 따로 적었다.**

---

## A. 메디킷

### A-1. 패키지 정체

| 항목 | 값 | 근거 |
|---|---|---|
| 이름 | `@medisolve-ai/medikit` | `package.json:2` |
| 설명 | 메디솔브AI 공통 UI 라이브러리 (Radix UI + Tailwind, shadcn 패턴, 전 컴포넌트 forwardRef) | `package.json:4`, `CLAUDE.md:7-10` |
| 버전 | main 0.3.0 / 차티 사용 1.4.0 | 위 표 |
| 빌드 | tsup — 엔트리 `src/index.ts`·`src/tailwind.ts`, ESM+CJS, d.ts, `onSuccess` 에서 `src/styles/base.css` → `dist/styles/base.css` 복사 | `tsup.config.ts:10-22` |
| exports | `.`(컴포넌트·훅·유틸) · `./styles`(base.css) · `./tailwind`(preset) | `package.json:9-32` |
| peer | react ≥18, react-dom ≥18, tailwindcss ≥3 | `package.json:46-50` |
| 배포 | `prepublishOnly: pnpm build` → npm 레지스트리 publish(`pnpm publish`). 레지스트리 종류(공개/사설)는 **확인 안 됨** — 차티 `.npmrc` 는 `engine-strict=true` 한 줄뿐 | `package.json:42`, `CLAUDE.md:19-21`, `stg:frontend/.npmrc:1` |
| 차티의 소비 | npm 의존 `^1.4.0` + tailwind preset + base.css import (아래 B-3) | `stg:frontend/package.json:22`, `stg:frontend/tailwind.config.ts:3,9,11`, `stg:frontend/src/styles/index.css:1` |

### A-2. 토큰

**위치**: CSS 변수 `src/styles/base.css:12-103`, Tailwind 매핑 `src/tailwind.ts:10-80`, 타이포 `src/styles/texts.ts`(28개 토큰).
규칙: 색 하드코딩 금지, `var(--ms-*)` 만 (`CLAUDE.md:8`).

#### 색

| 그룹 | 토큰(main) | 값 | 근거 |
|---|---|---|---|
| Primary(기본 Centurion) | `--ms-primary` / `-100` / `-300` / `-500` / `-shadow` | #476cff / #f0f4ff / #dde6ff / #97b5ff / rgba(71,108,255,.3) | `base.css:14-18` |
| **Primary — Charty** | `[data-product="charty"]` | **#6f21ff** / #f4f3ff / #e9e6ff / #a290ff | `base.css:91-96` |
| Red(공통·에러) | `--ms-red` / `-100` / `-300` / `-500` / `-shadow` | #ff4e51 / #ffefef / #ffe1e1 / #ffc4c5 / rgba(255,78,81,.2) | `base.css:21-25` |
| Success | `--ms-success` | = primary | `base.css:28` |
| Purple(공통) | `--ms-purple` / `-100` / `-500` | #ac47ff / #f8f0ff / #bf71ff | `base.css:31-33` |
| Hover | `--ms-hover-dark` | `34 41 67`(rgb 채널값, alpha 지원) — README 는 `#222943` 로 적혀 있어 표기 다름 | `base.css:36`, `tailwind.ts:55`, `README.md:1129` |
| Base | `--ms-white` / `--ms-black` / `--ms-overlay` | #fff / #000 / rgba(0,0,0,.6) | `base.css:39-41` |
| Gray | `--ms-gray-100…800` | #fbfbfb #f3f3f3 #e3e3e3 #d6d6d6 #cfcfcf #9f9f9f #6e6e6e #3e3e3e | `base.css:44-51` |
| 시맨틱 텍스트 | primary/secondary/disabled/placeholder | black / gray-800 / gray-600 / gray-600 | `base.css:59-62` |
| 시맨틱 보더 | default / focus | gray-300 / primary | `base.css:65-66` |
| 시맨틱 배경 | page / subtle / muted | white / gray-100 / gray-200 | `base.css:69-71` |
| 기타 제품 | say #5442ff · bay #23a0ff · watch #2cd1ff | | `base.css:77-103` |
| **1.4.0 추가** | `--ms-yellow` #fd9400 / -100 #fff7ec / -300 #ffe4c0 / -500 #fdc16f (경고, red 보다 완만) · `--ms-black` 이 `0 0 0`(채널값)으로 변경 · selly/linky/studio 테마 추가 · watch 값 변경(#00ace2) | | 1.4.0 `dist/styles/base.css` diff |

**상태(경고/위험) 색은 main 기준 red 하나뿐**이다. 「주의(노랑)」 단계는 1.4.0 의 yellow 로만 있다.
초록/성공 전용 색은 없다(success = primary).

#### 타이포 — `text-typo-{category}-{size}-{weight}`

| 카테고리 | px / LH | weight | 근거 |
|---|---|---|---|
| headline-lg / md | 40 / 32 · 130% | 400·500·600 | `texts.ts`, `README.md:1191-1202` |
| title-lg / md / sm | 24 / 20 / 18 · 140%·140%·150% | 400·500·600 | 동 |
| heading-md / sm | 16 / 14 · 150% | md 400·500·600 · sm 400·500 | 동 |
| body | 14 · 160% | 400·500·600 | 동 |
| caption-md / meta-sm | 12 / 10 · 130% | caption 400·500·600 · meta 400·500 | 동 |

폰트: Pretendard Variable 우선 스택 (`base.css:105-123`). 차티는 woff2 를 자체 번들(`stg:frontend/src/styles/index.css:7-14`).

#### 간격 · radius · shadow

- **간격 토큰 없음.** Tailwind 기본 스케일 + 임의값(`gap-[42px]`, `h-[57px]` 등)을 그대로 쓴다. `Spacing` 컴포넌트(px 지정 빈 div)가 있다 (`src/ui/spacing/spacing.tsx`).
- **radius 토큰 없음.** 컴포넌트 실사용 빈도: `rounded-[8px]` 25회, `rounded-full` 12회, 그 외 `[4px]`·`[3px]`·`[20px]`·`[100px]` (src/ui 전수 grep). 1.4.0 Card 는 `rounded-xl`.
- **shadow**: preset 에 `shadow-pop-over`(`0 0 4px #CFCFCF`), `shadow-pop-over-more`(`0 2px 10px rgba(189,189,189,.5)`) 두 개 (`tailwind.ts:25-28`). 버튼은 `shadow-[0_1px_6px_var(--ms-primary-shadow)]` 류 임의값.

### A-3. 컴포넌트 목록

main(0.3.0) export 기준 (`src/ui/index.ts`). 「1.4.0」 은 main 에 없고 1.4.0 에만 있는 것.

| 분류 | 이름 | 용도 한 줄 | 파일 |
|---|---|---|---|
| **카드** | (main 없음) | — | — |
| | **Card** 「1.4.0」 | `interactive`·`selected`·`indicator`·`corner`·`padding(none/sm p-3/md p-5/lg p-6)`. `rounded-xl border bg-ms-white`, 선택 시 primary 테두리 | 1.4.0 `index.d.ts:124-`, `index.js:~949` |
| | PlanCard 「1.4.0」 | 결제 플랜 카드(빌링 전용) | 1.4.0 |
| **탭** | Tabs | `tabs[{id,name}]`·`selectedTab`·`onSelectTab`. 텍스트 탭 + 하단 primary 인디케이터, 탭 간격 42px | `src/ui/tab/tab.tsx:21,59` |
| | AppTabs 「1.4.0」 | 제품 전환 탭(헤더 위) | 1.4.0 |
| **배지/칩** | (main 없음) | — | — |
| | **Badge** 「1.4.0」 | variant `neutral/primary/warning/danger/purple`, size `md(h-7)/sm(h-6)`, `dot`, `rounded-full` | 1.4.0 `index.d.ts:109-122` |
| | **Chip** 「1.4.0」 | size `lg/md/xs`, `onRemove` | 1.4.0 `index.d.ts:583-587` |
| **점수/게이지** | (main 없음) | — | — |
| | **Progress** 「1.4.0」 | 막대형. `value`/`max`, tone `primary/danger/neutral`, size `sm/md`, `lowAt`(임계치 이하 자동 danger). **「잔량 모델(쓸수록 줄어듦)」으로 설계됨** — 크레딧용 | 1.4.0 `index.d.ts:145-160` |
| | 원형 게이지·레이더 | **없음** (main·1.4.0 둘 다) | — |
| **차트** | — | **없음.** 차트 라이브러리 의존도 없음 (`package.json:51-66`) | — |
| **이미지 뷰어** | — | **없음** | — |
| **모달** | Modal | Portal, `isOpen`, backdrop, body 스크롤 잠금 | `src/ui/modal/modal.tsx` |
| | BaseModal | Modal + 제목·설명·닫기 X | `src/ui/modal/base-modal.tsx` |
| | ConfirmModal | 확인/취소 + warning/check 아이콘 | `src/ui/modal/confirm-modal.tsx` |
| | Dialog* | Radix Dialog 조합형 | `src/ui/dialog/dialog.tsx` |
| | Popover* · HoverCard* · Tooltip* | Radix 기반 오버레이 | `src/ui/popover`, `hover-card`, `tooltip` |
| **테이블** | Table·TableHeader·Body·Footer·Row·Head·Cell·Caption·ScrollArea(Viewport/Empty) | 헤더 `bg-primary-100` 행높이 50px, 본문 행 52px·hover gray-100 | `src/ui/table/table.tsx:38,53` |
| | Pagination | 중앙 정렬·말줄임 | `src/ui/pagination/pagination.tsx` |
| **레이아웃** | Menu | 좌측 사이드바 274px(접힘 76px), localStorage 접힘 저장, 활성 `bg-primary-100 text-primary` | `src/ui/menu/menu.tsx:120-123,190-194` |
| | Header | 상단 57px, 로고·메뉴·시계·지점명·사용자·로그아웃 내장 | `src/ui/header/header.tsx:94-95` |
| | Footer | 회사 정보 푸터 | `src/ui/footer/footer.tsx` |
| | Divider · Spacing | 구분선 · 간격 div | `src/ui/divider`, `spacing` |
| | Accordion* 「1.4.0」 | size `lg/md` | 1.4.0 `index.d.ts:24-` |
| | Banner 「1.4.0」 | variant `primary/warning/danger/neutral` 상단 배너 | 1.4.0 `index.d.ts:167` |
| 폼 | Button(variant solid/filled/outlined/text/icon/fillOutlined · color blue/red/black/gray · size lg/md/sm) · ActionButton · ResetButton · Input · Textarea · Label · Checkbox · RadioGroup · Toggle · ComboBox · InfiniteComboBox · Command* · Calendar · DatePicker · DateRangePicker | | `src/ui/*` |
| 피드백 | Loading · Notify/NotifyContainer · AsyncBoundary · DeferredComponent | | `src/ui/*` |
| 아이콘·로고 | ArrowIcon·ChevronIcon·CloseIcon·SearchIcon·CheckIcon·CalendarIcon·ResetIcon·MoreIcon · Logo(service/mode) | ⚠ main 의 `src/ui/index.ts` 는 CheckCircleIcon·WarningIcon·ErrorIcon 을 **re-export 하지 않는다**(README 는 쓸 수 있다고 적음). 1.4.0 은 export 함 | `src/ui/icons/index.ts`, `src/ui/index.ts` 끝 |

### A-4. HTML 목업에 쓸 수 있는 형태

| 형태 | 있나 | 근거·메모 |
|---|---|---|
| 빌드 CSS (CSS 변수) | **있음** — `dist/styles/base.css`. 단 파일 첫머리가 `@tailwind base/components/utilities` 지시문이라 **Tailwind 를 거쳐야** 완성된다. 순수 `<link>` 로 넣으면 `:root` 변수·`data-product` 테마만 살고 유틸리티 클래스는 없다 | `base.css:7-9` |
| Tailwind preset | **있음** — `@medisolve-ai/medikit/tailwind` 의 `medikitPreset` (색·fontSize(typo)·boxShadow·keyframes) | `src/tailwind.ts:10-80` |
| 스토리북 | **설정 있음, 배포본 없음** — `.storybook/main.ts`(react-vite, `src/**/*.stories.tsx`), `pnpm storybook` 은 로컬 6006. 배포된 스토리북 URL 은 **확인 안 됨** | `.storybook/main.ts`, `package.json:43-44` |
| 미리 빌드된 컴포넌트 CSS | 없음 (컴포넌트 스타일은 JS 안 Tailwind 클래스 문자열) | `tsup.config.ts` |
| 참고 | 로컬에 메디킷을 HTML 로 옮긴 선례 파일이 보인다: `~/orca/workspaces/cc-prototype/myeongdong-poc-v2/cc/design/_ds/medikit-*`, `…/medikit-patches.css`, `~/Desktop/Medikit Design System.md`, `~/Desktop/Medikit Brand Palettes.html` — **내용은 읽지 않았다**(브리프 범위 밖) | 파일 존재만 확인 |

---

## B. 차티 (origin/stg)

### B-1. 프론트 스택 · 라우팅 · 화면 목록

**스택** (`stg:frontend/package.json`): React 19 · Vite 6 · TypeScript · react-router-dom 7(`BrowserRouter`) · TanStack Query 5 · zustand 5 ·
Tailwind 3.4 + `@tailwindcss/typography` · medikit 1.4.0 · lucide-react(아이콘) · zod · axios · Sentry · Toss 결제 SDK · react-markdown · Playwright/Vitest.
**차트 라이브러리 없음.**

**라우트** (`stg:frontend/src/app.tsx:69-198`, 상수 `stg:frontend/src/routes/routes.tsx:1-38`)

| 경로 | 화면 | 한 줄 | 셸 |
|---|---|---|---|
| `/` | ConsultationPage | **상담 화면(메인)** — 실시간 녹음·전사·차트 생성. `/consultation` 경로는 따로 없다 | AuthGuard + AppLayout (`app.tsx:136-145`) |
| `/account` | AccountPage | 관리 — 탭: 계정/결제/시술(+차트 양식). staff 는 `/` 로 리다이렉트 | AuthGuard + AppLayout (`app.tsx:146-155`) |
| `/pricing/preview` | PricingPreviewPage | 가격표 업로드 미리보기(풀스크린) | AuthGuard, AppLayout 없음 |
| `/billing/onboarding` · `/billing/callback` · `/billing/credit-history` | 결제 온보딩 · 결제 콜백 · 크레딧 내역 | 결제·구독 | AuthGuard + AppLayout |
| `/product-intro/:product` | ProductIntroPage | 미구독 제품 소개 iframe | AuthGuard + ProductIntroLayout |
| `/login` · `/logged-out` · `/login/legacy` · `/auth/complete` · `/auth/sso/link` · `/logout` | 로그인/SSO 계열 | 통합로그인·SLO | — |
| `/demo` | DemoPage | 데모 | — |
| 정책 경로들 | PolicyPage(lazy) | 약관 공개 페이지 | — |

### B-2. 상담 · 고객(환자) · 차트 관련 화면

**상담 화면은 있다(`/`), 고객(환자) 화면은 없다.**

- **상담 화면 레이아웃** (`stg:frontend/src/pages/consultation/consultation-desktop.tsx:42-121`), 위→아래:
  1. `BillingBanners` (게이팅 배너, 최상단) `:46`
  2. `Header` (서비스 전환 탭 + 50px 헤더) `:47`
  3. 세션 설정 바 — `bg-ms-gray-100 border-b`, `SessionSettings` + `UtilityButtons` `:49-56`
  4. `ConsultationProgress` `:58` · 목표시간 초과 경고 줄(빨강) `:60-65`
  5. **좌우 리사이즈 분할** `HorizontalSplit` `:67-121`
     - 좌: 상단 72px 녹음 컨트롤(`TranscriptView`) + 하단 `LeftBottomPanel`(좌 `PricingPanel` 가격표 · 우 `ChartyRecommendation` 시술 추천, 다시 좌우 리사이즈) (`left-bottom-panel.tsx:56-`). 통역 모드면 상하 분할 `VerticalSplit` `:74-93`
     - 우: `ChartyPickBanner` + `ChartPreview`(탭 3개 **체크리스트 / 차트 / 상담 텍스트**) + `GenerationOverlay` `:113-120`, 탭 정의 `stg:frontend/src/features/chart/components/chart-toolbar.tsx:4,30-33`
  - 640px 미만은 `ConsultationCompact` 로 교체 (`page.tsx:69`)
- **고객 식별 데이터 필드** — 고객 테이블·고객 화면이 없다. 있는 것은 **외부 식별자 두 개**뿐:
  - 시술관제 딥링크 `/?customerId=&counselorId=` 를 캡처해 store 에 보관 후 URL 에서 제거 (`stg:frontend/src/features/session/hooks/use-external-consultation-context.ts:9,36-44,46-60`)
  - 차트 생성 요청에 `customerId`·`counselorId` 를 실음 (`stg:frontend/src/features/chart/chart-types.ts` `ChartGenerateRequest`)
  - BE 저장: `chart_history.external_customer_id` · `external_counselor_id` (`stg:backend/app/model/chart_history.py:30-31`). 조회 API 는 「Track B, 약관 개정 후」로 미구현이라 주석에 적혀 있음
- **차트 데이터 필드**(`chart_history`, `stg:backend/app/model/chart_history.py:14-33`): `transcript_text`, `chart_text`(자유 텍스트), `consultation_type`, `chart_style`, `chart_template_id`, `model`, `created_at` 등. **구조화된 피부 소견 필드는 없다.**
- 상담 이력 API: `GET /consultation-history`, `GET /consultation-history/{id}` (`stg:backend/app/router/consultation_history.py:42,67`) — 화면 연결 여부는 **확인 안 됨**(프론트 라우트엔 없음)

### B-3. 메디킷 사용 실태

- **소비 방식**: tailwind preset 등록 + content 에 `node_modules/@medisolve-ai/medikit/dist/**` (`stg:frontend/tailwind.config.ts:3,6-11`),
  `src/styles/index.css:1` 에서 base.css 를 상대경로 `@import`, 그리고 **`:root` 에서 Charty primary 를 직접 덮어쓴다**(`index.css:16-25`) —
  `data-product="charty"` 속성은 쓰지 않는다(git grep 결과 0건). 추가 토큰: `--ms-primary-hover: #5a1acc`, `--doctor-color`/`--patient-color`/`--warning-color`.
  body 배경은 `bg-slate-50`(Tailwind 기본 팔레트, medikit 아님) `index.css:33-35`.
- **import 예**
  - `stg:frontend/src/app.tsx:4` — `import { Loading, NotifyContainer } from "@medisolve-ai/medikit";`
  - `stg:frontend/src/pages/account/page.tsx:2` — `Tabs` (관리 상단·서브 탭 `:117-121,146-150`)
  - `stg:frontend/src/features/billing/billing-status-badge.tsx:30` — `Badge, formatDateOnly`
  - `stg:frontend/src/layouts/service-switcher.tsx:1-6` — `AppTabs, APP_TABS_PRODUCTS`
- **사용 빈도**(origin/stg 전수, import 문 기준 파일 수): Button 40 · Loading 13 · formatNumber 11 · formatDateOnly 9 · Modal 8 · Input 7 · cn 7 · ComboBox 5 · Badge 5 · Table* 4 · Tooltip* 4 · Banner 3 · Toggle 3 · Pagination 2 · Checkbox 2 · Textarea 2 · Tabs 1 · BaseModal 1 · AppTabs 1 · Footer 1 …
  **안 쓰는 것**: medikit `Header`·`Menu`·`Card`·`Chip`·`Progress`·`Accordion`·`Dialog` 0건.
- **비율**: tsx 97개 중 medikit import 파일 71개, lucide-react import 24개.
- **자체 컴포넌트**
  - 셸은 전부 자체: `layouts/header.tsx`, `service-switcher.tsx`, `split-pane.tsx`, `page-container.tsx`, `footer.tsx`(medikit Footer 래핑)
  - 상담 화면 내부 탭은 medikit `Tabs` 가 아니라 **자체 버튼 탭**(`border-b-2`, 활성 `text-primary border-primary`) `chart-toolbar.tsx:58-66`
  - `src/components/ui/card.tsx`·`badge.tsx`·`empty-box.tsx` 는 자체 구현인데 **import 하는 곳이 0건**(사용 안 됨). 이 파일들이 쓰는 `shadow-card`·`text-font-20-600` 클래스도 config 에 정의 없음
  - 헤더 pill·버튼은 대부분 Tailwind 임의값 인라인(`text-[11px] px-[9px] rounded-md` 등) `header.tsx:211-256`
  - tailwind 자체 색: `clinic-50…900`(fuchsia 계열), `doctor` #3b82f6, `patient` #10b981, `warning` #ef4444 `tailwind.config.ts:24-40`

### B-4. 화면 공통 골격 · 「피부 상담」이 붙을 후보 (결정 아님)

- **골격**: `AppLayout` = 콘텐츠 + 화면 아래 Footer 만 (`stg:frontend/src/layouts/app-layout.tsx:9-15`).
  헤더는 각 페이지가 직접 `<Header/>` 를 렌더한다(`consultation-desktop.tsx:47`, `account/page.tsx:96`).
  Header = `ServiceSwitcher`(제품 전환 탭: linky·charty·watch) + 50px 흰 헤더(로고 · 선택적 `screenName`/`center` 슬롯 · 시계 · [관리] · 병원명 · 이름 pill · 결제상태·크레딧 배지 · 사용 가이드 · 로그아웃) (`header.tsx:43-47,176-257`).
  **좌측 사이드바·전역 메뉴는 없다.** 화면 이동은 헤더의 [관리]/[상담 화면] 버튼뿐 (`header.tsx:211-227`).
- 일반 페이지 컨테이너: `PageContainer`(p-6, `max-w-4xl` 중앙) + `PageNavHeader`(뒤로가기 + `text-typo-title-md-600` 제목) (`stg:frontend/src/layouts/page-container.tsx:20-23,47-76`) — 관리·크레딧 내역이 이 문법.
- **붙을 자리 후보**
  1. 새 라우트(예: `/skin-consult`) + `AuthGuard`+`AppLayout`+`Header(screenName=…)` — 관리 페이지와 같은 문법. 헤더에 진입 버튼을 추가해야 함
  2. 상담 화면 우측 `ChartPreview` 탭(체크리스트/차트/상담 텍스트)에 탭 하나 추가
  3. 상담 화면 좌하단 `LeftBottomPanel`(가격표 | 시술 추천) 칸 중 하나로
  4. 상담 화면 위 모달/오버레이(medikit `Modal`·`BaseModal`)
  5. 딥링크 진입(`?customerId=`)과 연계 — 시술관제가 이미 이 방식으로 고객 맥락을 넘김

### B-5. 백엔드 피부 분석 · 외부 스캐너 연동 흔적

`git grep -iE "m3d|migamedi|미가|skin_?anal|skin_?scan|피부 ?(분석|진단|스캔)|3d ?scan|스캐너" origin/stg` — **연동 흔적 없음.**

- `skin`·`scan` 히트는 무관: `scanned`(빌링 배치 카운터 `reconcile_batch.py:60`), `HEADER_SCAN_ROWS`(가격표 파서 `pricing_normalize.py:73`), `skinbooster`(시술명 테스트)
- 「피부」 관련은 **LLM 프롬프트 문구뿐**: 차트 작성 프롬프트가 「진단 대신 피부 분석/현재 상태로 표현」, 고민 카테고리(주름·탄력·색소·모공/피부결·트러블·홍조) 정의 (`stg:backend/app/service/chart/prompts.py:20-45`, 34행)
- 테스트 스크립트에 「피부 진단 리포트 카톡 발송」 대사 (`stg:backend/scripts/pricing-test-scripts/script-30min.md:242`) — 기능 아님
- 모델 목록(`backend/app/model/*`)에 피부·스캔·고객 테이블 없음

---

## C. 원본 리포트 (M3D / 미가메디)

### C-1. 화면 섹션 순서 (HTML 저장본)

저장본은 Vue SPA 의 렌더 결과로, 본문이 `ref:테스트 보고서.html:189` **한 줄**에 들어 있다(줄번호 인용이 의미 없어 순서로 적는다).
`테스트 보고서_files/` 폴더는 함께 저장되지 않아 이미지·폰트 링크는 깨진 상태. 원 URL `…/h5?hash=****&type=1002&enable_history=1&show_detail=1` (HTML 2행 주석).

| # | 섹션 | 보여 주는 것 | 시각 요소 |
|---|---|---|---|
| 0 | 헤더 | 고객 이름(`홍○○`) · 측정 일시 `YYYY/MM/DD HH:mm` · 얼굴 썸네일(`icon.jpg`) · **「3D영상 보기」** 버튼 | 아이콘 SVG, 사진 1장 |
| 1 | **종합분석** | 4개 대분류(염증&민감 · 피부톤 · 피부결 · 노화) 레이더. 안내문 「중심점에 가까울수록 증상의 정도가 더 심함」, **「85점 이상 건강, 70–85 경도, 60–70 중등도, 60 이하 중도」** | `<canvas>`(레이더) |
| 2 | **염증&민감** | 대분류 점수 + 「주요 핵심요인」(레드존 76 · 포르피린 -1) → 항목별 카드: 항목 점수 · 하위 측정치 행(이름 · ⓘ툴팁 · 정도 배지 · 측정값 · 점수) · 분포 막대그래프(백분율 축) | canvas(대분류 게이지 `mycanvas`) + canvas(분포) |
| 3 | **피부톤** | 색소 · 밝기 카드(위와 동일 문법) + **팬톤 스킨톤 코드**(색 이름·코드·설명) + **LAB 피부톤**(톤 이름, L/A/B 값, 파운데이션 조언 문구, Lab 컬러 위치 좌표도, 밝기 L 바, 「Lab 피부 팬톤칩」 12칩 중 해당 칩 강조, 「열기」 토글) | canvas 다수 |
| 4 | **피부결** | 모공(크기 피크 μm · 깊이 피크 μm · 확장 모공 비율 · 깊은 모공 비율 · 크기 분포 · 깊이 분포) · 피문(깊은/극심한 피문 비율 · 분포) | canvas |
| 5 | **노화** | 「주요 핵심요인」 잔 주름 · 굵은 주름 → 접이식 그룹(「숨기기/열기」): 잔 주름(코뿌리·미간·눈밑·눈가·이마), 굵은 주름(눈물고랑·팔자·광대고랑 — **좌/우 각각** 길이비율·곡률 행) | canvas(곡률 분포) |
| 6 | 푸터 | 로고 이미지(`log_en2`) | img |

- **정도 배지 4색** (HAR CSS `index-MBBKsitd.css`): `bg01` 표준 #29b99f · `bg02` 경도 #99bb62 · `bg03` 중등도 #ffa943 · `bg04` 중도 #ff6161
- 이 저장본(type=1002) 에는 **광원별 이미지 갤러리(atlas/images)가 렌더되어 있지 않다.** 실제 사진 `<img>` 는 썸네일 1장뿐이다. HAR 에도 S3 이미지 요청은 `icon.jpg` 하나뿐(HAR entry 23).
  3D 는 「3D영상 보기」 버튼 뒤에 있고, 번들에 `OBJLoader` 문자열이 1회 나온다(HAR entry 2) — 뷰어 구현 상세는 **확인 안 됨**.

### C-2. API 3개 응답 구조

모두 `GET https://m3d-api.migamedi.co.kr/api/skin/...?hash=<리포트 해시>` · 응답 봉투 `{code:0, msg:"success", data:{…}}`.
(HAR entry 18 · 20 · 21)

#### (1) `report/render.v3` — 리포트 메타 · 이미지 · 3D

| 필드 | 형 | 의미/예(마스킹) |
|---|---|---|
| `id`, `hash` | int, str | 리포트 id · 공유 해시 (`****`) |
| `icon` | url | 얼굴 썸네일 (S3 presigned) |
| `date`, `created_time` | str, epoch ms | 측정일 |
| `user{id,name,gender,birthday,age,unique,display_unique}` | obj | **개인정보** — `홍○○`, gender 1, `YYYY-MM-DD`, age, 회원번호 `****` |
| `version`, `edition`, `shape_analyze`, `report_analyze`, `color_scheme`, `copy_time` | int | 리포트 버전·플래그 |
| `scanner_unique_tag`, `scanner_version`, `camera_type`/`display_camera_type`(P2), `camera_port` | str | 장비 식별 (`P2********`, 2.0.2) |
| `zips{obj,thumb,shape_ai,hd_ai}` | `{type:"ZIP",flag,url}` | 리소스 묶음 ZIP (presigned) |
| `options{aesthetic_design,light_enhancement,volume_comparison,vector_tracing,precise_measure,…}` | 0/1 | 기능 토글 |
| `atlas[20]` | `{flag,name,type}` | 이미지 모드 사전. **type 0 = 광원 사진 13종**(냉광 rgb_cool · 자연광 rgb · 모세혈관확장 · 증강레드 · 표준레드 · 염증 히트맵 · 표준브라운 · 색소 히트맵 · 증강브라운 · 자외선 · UV스팟 · 평행편광 · 교차편광), **type 1 = 분석 레이어 7종**(밝기 gray · 등고선 · 모공 · 피문 · 잔주름 · 굵은주름 · 함몰) |
| `images[11]` | `{flag, mapping_flag→atlas.flag, title, detail(모드 설명문), filename:"zip://thumb/…_Middle_T.jpg"}` | 광원 모드 썸네일 + 설명 |
| `three_dimensional.obj` | `"zip://obj/Rgb.obj"` | 3D 메시 |
| `three_dimensional.default` | url | 기본 텍스처(냉광) |
| `three_dimensional.mappings[13]` | `{flag,title,url,filename,thumb_filename}` | 3D 에 입힐 광원별 텍스처 |
| `three_dimensional.extras[1]` | `{flag:"old",title:"노화 시뮬레이션",…}` | 노화 시뮬레이션 이미지 |
| `three_dimensional.masks[21]` | `{flag, filename:"zip://mask/…"}` | 문제 마스크(주름·UV·모공·다크·여드름·유분 T/U·민감·충혈·부위별 주름 6종 등). ⚠ `zips` 에 `mask` 키가 없어 이 경로를 어디서 푸는지 **확인 안 됨** |

#### (2) `measure/results/render?measure_version=2` — 측정 수치 (점수 체계의 원본)

```
data
├─ id, id_str, type(7), hash, version("0.8.0"), results_version("0.25.2")
├─ categories[4]   대분류
│    {id:"basic_247", name:"염증&민감", features:["Red","Porphyrin"],   ← feature id 참조(문자열 배열)
│     score:76, level:1, result:1.6, degree:"경도"}
└─ features[10]    항목
     {id:"Red", name:"레드존", score, level, result, degree,
      measures[ {id, title, deduced, degree, score,
                 results[ {id:"red_max", title:"극값", type, value, unit, degree, score, describe,
                           (분포형만) level[5], result[4], narrow, (색상형만) group} ] } ]}
```

| 대분류(categories) | features | 대분류 score/level/degree 예 |
|---|---|---|
| 염증&민감 `basic_247` | Red(레드존), Porphyrin(포르피린) | 76 / 1 / 경도 |
| 피부톤 `basic_246` | Pigment(색소), Grayscale(밝기), Pantone(팬톤 스킨톤 코드), SeasonColor(LAB 피부톤) | 68 / 2 / 중등도 |
| 피부결 `basic_245` | Pore(모공), Dermatograin(피문) | 71.2 / 1 / 경도 |
| 노화 `basic_244` | basic_241 잔 주름(measures 5: 코뿌리 BG·미간 MJ·눈밑 YD·눈가 YW·이마 TT), basic_242 굵은 주름(measures 3: 눈물고랑 LG·팔자 FL·광대고랑 QJ) | 68.3 / 2 / 중등도 |

- **점수 3층**: category.score ← feature.score ← measure.score ← result.score. 각 층에 `degree`(수치, 0~4 스케일) 와 `score`(0~100) 가 같이 있다. category·feature 의 `result` 는 measure 의 `degree` 수치와 같다(예 Red 1.6).
- `level` ↔ `degree`(문자): 0 무/없음/건강 · 1 경도 · 2 중등도 (3 중도 는 본 샘플 상위층엔 없음). HTML 의 배지는 result.score 로 표준/경도/중등도/중도 4단계.
- **점수 없음 표기**: `score:-1, level:0, degree:"무"` — Porphyrin·Pantone·SeasonColor (색상형이거나 산출 안 됨). HTML 은 이걸 「-1」 그대로 노출.
- `results[].type` 분포: curvature 24 · length 15 · rgb 13 · extremum 12 · lab 12 · ratio 11 · distribution 11 · average 5 · str 4 · intensity 3 · color_code 2 · range 2 · count 1
- `distribution` 의 `value` = `{bar_colors[], ratios[], steps[], step, min_value, unit, ratio_title, step_title}` + 형제 필드 `level[5]`(구간 경계) · `result[4]`(구간 이름, 예 `["페일레드","라이트레드","레드","다크레드"]`)
- 관찰된 품질 이슈(값 근거):
  - 일부 `title`·`ratio_title` 이 **중국어 미번역**(`描述词`, `rgb值`, `原始平均rgb值`, `红度`, `比例` 등) — Pantone·SeasonColor·distribution
  - 굵은 주름의 좌우 표기가 id 와 반대: `wrinkles_lg_right_length_ratio` 의 title 이 「좌측 …」
  - ratio 형 `unit:"%"` 인데 값은 0~1 소수(0.1523 → HTML 15.23%) 혹은 1(→100%)

#### (3) `basic/analyze/results/render?measure_version=2` — 분석 인스턴스 (설명문·조언·참고 이미지)

```
data
├─ id, type, results_version, edition, camera_type, display_camera_type
├─ comprehensive {name:"염,톤,결,노", atlas[4]:[rgb_cool, red, brown, gray]}   ← 종합분석 레이더 축/대표 이미지
└─ instances[6]
     {id:247, name:"염증&민감", type(1|2), commonly_used, parent_id, is_child,
      atlas[]  ← 이 분류에서 볼 이미지 모드(atlas.flag 참조)
      thumb    ← 분류 대표 썸네일 (공용 업로드 경로 manage/uploads)
      describe, treatment_process, interpret  (본 샘플 전부 null)
      related[] (노화 244 → 241·242 자식)
      result, original_result, level, degree, options{show_physical_values},
      render_images[] (본 샘플 전부 빈 배열)
      features[ {id:801, original_number:"p1_010", name:"레드존", part_id, result, level, degree,
                 label_id, approved, corrected, ai_usage, stat, interpret,
                 detail{content, reason, care_advice, treatment_advice, points, images[],
                        physical_id → measure feature id, physical_deduced, physical_values[] (= measure results 사본)} } ]}
```

| instance | 자식/부모 | atlas(이미지 모드) | features |
|---|---|---|---|
| 247 염증&민감 | — | red · red2_face · red2_heat · red2_ex_face · rgb_cool · uv | 레드존(801) · 포르피린(505) |
| 246 피부톤 | — | rgb · rgb_cool · brown · brown_heat · brown_enhanced · plv · uv | 색소 · 밝기 · 팬톤 · LAB |
| 245 피부결 | — | gray · rgb_cool · plh · dermatograin · pore | 모공(495) · 피문(807) |
| 244 노화 (type 2) | related → 241, 242 | gray · rgb_cool · plh · wrinkles · wrinkles_thick | (없음, 자식으로) |
| 241 잔 주름 | parent 244 | gray · rgb_cool · wrinkles | 코뿌리·미간·눈밑·눈가·이마 |
| 242 굵은 주름 | parent 244 | gray · rgb_cool · wrinkles_thick | 눈물고랑·팔자·광대고랑 |

#### 세 API 의 관계

| 연결 | 키 |
|---|---|
| measure `categories[].id`(`basic_247`) ↔ analyze `instances[].id`(247) | 접두어 `basic_` 차이 |
| measure `features[].id`(`Red`) ↔ analyze `features[].detail.physical_id`(`Red`) | 같은 문자열. 노화만 measure 쪽이 `basic_241/242` 로 묶고, analyze 쪽은 measure 단위(`Wrinkles_BG` 등)로 연결 |
| analyze `instances[].atlas[].flag` / `comprehensive.atlas` → render `atlas[].flag` → render `images[].mapping_flag` · `three_dimensional.mappings[].flag` | 분류별로 어떤 광원 이미지를 보여 줄지 |
| render `three_dimensional.masks[].flag` ↔ 각 문제 항목 | 이름 유사성만 있고(예 `pore_face`↔Pore) 명시 키는 **없음** |
| 점수/degree | measure 가 원천, analyze 는 `result`(=score)·`original_result`(=degree 수치)·`physical_values`(=measure results 사본)로 **중복 보관** |

### C-3. 상담에 쓸 만한 데이터 vs 장식에 가까운 데이터 (필드 근거)

**판정 기준**: 이 고객 개인의 값이 담겼는가(개인값) / 모든 리포트에 공통인 문구·이미지인가(공통) / 값이 비어 있나(비어 있음).

| 데이터 | 필드 | 성격 | 근거 |
|---|---|---|---|
| 대분류 4개 점수·등급 | measure `categories[].score/level/degree` | **개인값** | 4개 모두 값 있음 |
| 항목 점수·등급 | measure `features[].score/level/degree` | **개인값** | 10개 중 7개 값, 3개 -1 |
| 하위 측정치(값·단위·점수) | measure `features[].measures[].results[]` (extremum·ratio·length·count 등) | **개인값** · 물리량(μm, mm, %) | 예 모공 크기 피크 450μm |
| 부위별 주름 점수, 좌/우 | measure `basic_241/242 → measures[]` | **개인값** · 부위 단위 | 8개 부위, 굵은 주름은 좌/우 분리 |
| 분포 히스토그램 | `type:"distribution"` 의 `ratios/steps/level/result` | **개인값**이나 해석 난도 높음 | 11개 |
| 피부톤 코드 | Pantone `Skin_ID`·`Skin_description`, SeasonColor `Skin_ID`·L/a/b | **개인값**, 점수 없음(-1) | 파운데이션 추천 `Skin_foundation` 은 제품명 나열 |
| 색 원시값 | SeasonColor `raw_/remap_ rgb/lab mean/min/max/median/dominant` 20여 개 | **개인값**이나 HTML 에도 대부분 안 나옴, title 중국어 | measure results |
| 개인 이미지 | render `icon`, `images[]`(광원 11종), `three_dimensional.mappings[]`·`obj`·`masks[]`·`extras(노화 시뮬레이션)` | **개인값** — 단 본 저장본 화면엔 썸네일 1장만 노출 | HAR 이미지 요청 1건 |
| 항목 설명문 | analyze `detail.content` · `reason` · `care_advice` | **공통 문구** | 레드존 `content`=「얼굴의 붉은 색소 분포.」, 미간·눈가·이마 등 동일 문구 반복형. ⚠ 포르피린의 `content`·`reason` 이 「피부 결」 설명으로 들어가 있어 **내용 불일치** |
| 치료 조언 | analyze `detail.treatment_advice`, `instances[].treatment_process` | **비어 있음** | 전 항목 `""` / `null` |
| 해석 | `instances[].interpret`, `features[].interpret`, `instances[].describe` | **비어 있음** | 전부 `null` |
| 참고 이미지 | analyze `detail.images[]`, `instances[].thumb` | **공통(교육용) 이미지** | 경로 `…/manage/uploads/images/2024-11-05/…png` — 측정 경로(`xiaofu/uploads/<측정일>/<리포트id>/`)와 다름 |
| 광원 모드 설명 | render `images[].detail` | **공통 문구** | 모드마다 고정 설명 |
| 렌더 이미지 | analyze `render_images[]` | **비어 있음** | 6개 모두 `[]` |
| 장비·버전 메타 | `scanner_*`, `camera_*`, `version`, `edition`, `options`, `color_scheme` | 장비 정보 | 상담 내용과 무관 |

---

## 정할 것 (워커가 정하지 않음)

1. **목업 기준 메디킷 버전** — 로컬 main(0.3.0)인가, 차티가 쓰는 1.4.0 인가. 1.4.0 이면 Card·Badge·Chip·Progress·Accordion 을 쓸 수 있고, 0.3.0 이면 없다. 1.4.0 소스 레포 위치도 확인 필요
2. **HTML 목업의 스타일 수단** — medikit preset 을 Tailwind(CDN/빌드)로 돌릴지, base.css 의 CSS 변수만 가져와 손으로 쓸지 (base.css 는 `@tailwind` 지시문 포함)
3. **Charty 테마 적용 방식** — `data-product="charty"` 인가, 차티처럼 `:root` 직접 덮어쓰기(`--ms-primary-hover` 포함)인가
4. **메디킷에 없는 부품** — 원형/레이더 게이지, 분포 막대그래프, 이미지(광원) 뷰어·비교, 3D 뷰어, 4단계 등급 배지(표준/경도/중등도/중도 — medikit 상태색은 red, 1.4.0 yellow 뿐)를 어떻게 그릴지. 원본 4색(#29b99f/#99bb62/#ffa943/#ff6161)을 쓸지 medikit 팔레트로 옮길지
5. **「피부 상담」 화면의 자리** — B-4 후보 5개 중 무엇인가 (새 라우트 / 차트 패널 탭 / 좌하단 패널 / 모달 / 딥링크 연계)
6. **고객 식별** — 차티엔 고객 모델이 없고 외부 `customerId` 만 있다. 목업에서 고객 맥락(이름·나이 등)을 어디서 받는 것으로 그릴지
7. **화면에 올릴 데이터 범위** — C-3 의 개인값 중 무엇을(대분류 4 · 항목 10 · 하위 측정치 · 분포 · 피부톤 코드 · 이미지) 보이고, 공통 문구·빈 필드(`treatment_advice`·`interpret` 등)를 어떻게 처리할지
8. **원본의 품질 이슈 처리** — 중국어 미번역 title, 좌/우 반전 title, 포르피린 설명 불일치, `-1` 점수 노출을 목업에서 그대로 재현할지 보정할지
9. **목업 데모 데이터** — HAR 은 실존 인물 데이터다. 목업에 넣을 값을 가명화한 HAR 수치로 할지, 새로 만든 가짜 값으로 할지
10. **이미지 소스** — 저장본에 광원 이미지가 없고(`_files` 폴더 미저장) presigned URL 은 만료된다. 목업용 피부 이미지를 무엇으로 할지

## 확인 안 됨 목록

- 메디킷 1.4.0 소스 레포/브랜치 위치, npm 레지스트리 종류(공개/사설), 배포된 스토리북 URL
- 차티 상담 이력 API(`/consultation-history`)의 프론트 사용처
- M3D 3D 뷰어 구현(three.js 여부 — `OBJLoader` 문자열 1회만 확인), `zip://mask/…` 를 푸는 ZIP 출처
- `degree` 수치(0~4)와 `level`·배지 4단계의 정확한 변환 규칙(HTML 문구 「85/70/60」 기준만 확인)
