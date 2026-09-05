# Frontend Architecture

규칙: `para/projects/project.md`

> Next.js 정적 번들의 라우트·디렉토리·데이터·스타일 규약. **여기 적힌 것은 「이렇게 한다」다** —
> 코드 워커는 이 문서만 읽고도 같은 방식으로 화면을 만들 수 있어야 하고, 리뷰어는 이걸 기준으로 판정한다.
> **선택지를 남기지 않는다.**
>
> 근거 표기: `DEC-00x §y` = `10-decision/`, `F-xx·P-xx·C-xx·S-xx·Q-xx` = `orchestration/work/docs-v1/docs-v1-design-report.md`,
> `§A/§B/§C` = `orchestration/work/docs-v1/design-requests.md`, 파일명 = `00-design/`.

관련 문서 — `../system/README.md`(구성·흐름) · `../backend/README.md`(**§10 API 표면이 이 문서의 입력**) · `../database/README.md`.

## 0. 이 문서를 지배하는 다섯 제약

| # | 제약 | 무엇이 따라오나 | 근거 |
|---|---|---|---|
| FE-C1 | **정적 빌드** `output: 'export'` | 서버 컴포넌트 런타임 페칭·Route Handler·미들웨어·Server Actions **전부 없다.** 데이터는 100% 클라이언트에서 FastAPI 로 간다 | §C Q-28 |
| FE-C2 | **웹 우선, Tauri 는 마지막 포장** | 브라우저에서 개발하고, 셸에 의존하는 것(토큰 보관·파일 선택창)은 **추상화 뒤에 숨겨** 교체가 파일 하나로 끝나게 한다 | §C-4 · §C-5 |
| FE-C3 | **shadcn/ui + Tailwind**, 토큰은 CSS 변수 | 컴포넌트 매핑은 C-01~49 를 따른다(그대로 28 / 커스텀 21) | §C Q-33 |
| FE-C4 | **유동 레이아웃** | 1920 실측 좌표는 **비율·최소폭의 참고값**이다. `position:absolute` 로 박지 않는다 | §C Q-34 · §A-13 |
| FE-C5 | **인증은 Bearer** | 쿠키 없음. 헤더 부착·refresh 재시도를 프론트가 한다 | DEC-001 §4 · §C-5 |

## 1. 라우트 트리 — 확정

리포트 §3.2 의 **제안을 확정으로 승격**하되, v1 정책과 정적 빌드 제약에 맞게 셋을 바꿨다.
바꾼 것: ① 회원가입·비밀번호 찾기 라우트 제거(DEC-001 §1) ② 홈·채팅 라우트 제거(정책서 없음 — §10) ③ **동적 세그먼트 전부 제거**(FE-C1 — 아래 1-2).

```text
app/
├── layout.tsx                       # 폰트 · 토큰 CSS 변수 · QueryClientProvider · OverlayProvider · Toaster(S-24)
│
├── (auth)/
│   ├── layout.tsx                   # 셸 없음 — F-1. 브랜드 그라디언트 패널
│   └── login/page.tsx               # P-04
│
└── (app)/
    ├── layout.tsx                   # S-01 AppShell · 세션 가드 · 최소 폭 가드(P-02) · 햄버거 오버레이(P-03)
    │
    ├── tasks/
    │   ├── layout.tsx               # S-02 PageHeader + S-03 PeriodStepper + 뷰 토글 + 「새 업무」 — F-8
    │   ├── page.tsx                 # P-18 리스트 / P-19 칸반   ?view=list|board
    │   └── detail/page.tsx          # P-23 업무 상세 전체 페이지  ?id=  ← 드로어 ⤢ 의 목적지(F-5)
    │
    ├── meetings/
    │   ├── page.tsx                 # P-33 목록 + 우측 프리뷰
    │   └── detail/page.tsx          # P-35/37/40 상태로 갈린다(F-10)  ?id=
    │
    ├── calendar/page.tsx            # P-47/48/49  ?view=month|week|day&date=YYYY-MM-DD
    │
    ├── library/
    │   ├── layout.tsx               # S-26 DirectoryTree — 목록·상세·편집 공통(F-9)
    │   ├── page.tsx                 # P-56 파일 목록  ?folder=
    │   └── doc/page.tsx             # P-57 상세 / P-58 편집  ?id=&tab=read|edit|source (F-9)
    │
    ├── messages/page.tsx            # P-71/72 — 상세는 우측 패널, 별도 라우트 아님(F-12). v1 은 비활성(DEC-006)
    │
    └── settings/
        ├── layout.tsx               # 좌 메뉴 카드 260 + 로그아웃·계정 삭제·버전 캡션 — F-11
        ├── page.tsx                 # P-05 개인 설정
        ├── work/page.tsx            # 유형·프로젝트 관리 (§B-1 디자인 대기)
        └── integrations/page.tsx    # P-06 연동 관리 — v1 비활성(DEC-001 §v2)
```

**로그인 후 기본 진입은 `/tasks`** 다. 홈이 v1 에 없다(§10).

### 1-1. 오버레이는 라우트가 아니다 — Q-29 확정

**드로어·모달·팝오버에 URL 을 주지 않는다. 클라이언트 상태로 둔다.**

근거 셋.
1. **정적 빌드와 상성이 나쁘다.** Parallel/Intercepting Routes(`@drawer` + `(.)tasks/[id]`)는 빌드 시 경로 조합을 알아야 하는데, 업무·회의 id 는 런타임에 생긴다(FE-C1).
2. **부모가 3곳이다.** 같은 드로어가 tasks·calendar·meetings 에서 열린다(F-4) → intercept 규칙이 3벌 필요하다.
3. **딥링크를 쓸 상대가 없다.** 단일 사용자 데스크톱 앱이라 URL 공유가 없다(DEC-001 §2). 딥링크가 필요한 표면(⤢ 로 승격되는 상세)은 **이미 실제 라우트**(`/tasks/detail?id=`)로 있다 — F-5 가 요구하는 것은 그것뿐이다.

받는 비용 — 드로어가 열린 상태에서 브라우저 뒤로가기를 누르면 이전 화면으로 간다(드로어만 닫히지 않는다). **`Esc`·`×`·스크림 클릭 세 가지로 닫는 길을 항상 열어 둔다.**

### 1-2. 동적 세그먼트를 쓰지 않는다 — 정적 빌드 규칙

**`[id]` 세그먼트를 만들지 않는다. 리소스 식별은 전부 쿼리스트링이다.**

`output: 'export'` 는 빌드 시점에 모든 경로를 산출물로 구워야 한다. 동적 세그먼트를 쓰면 `generateStaticParams` 로 id 목록을 내야 하는데, 업무·회의·문서 id 는 **런타임에 생긴다** — 낼 수 있는 목록이 없다. 쿼리는 산출물 하나로 모든 id 를 처리한다.

| 규칙 | 내용 |
|---|---|
| 식별 | `?id=` (숫자 — PK 가 bigint) |
| 뷰 전환 | `?view=` — 캘린더 `month\|week\|day`(Q-31 확정) · 업무 `list\|board`(Q-32 확정) · 문서 `?tab=read\|edit\|source` |
| 왜 쿼리인가 | 라우트로 쪼개면 정적 산출물이 뷰마다 생기고 상태 공유가 끊긴다. `useState` 로 두면 새로고침·뒤로가기에서 잃는다. **쿼리는 정적 빌드와 양립하면서 뒤로가기가 산다** — 디자인이 뷰 전환을 「현재 위치」(`#1E1E1E`)로 취급하는 것과도 맞다 |
| 읽는 법 | `useSearchParams()`. **쿼리 파싱은 영역 훅 하나**(`useTasksViewParams` 등)에 모으고 컴포넌트가 직접 파싱하지 않는다 |
| 없는 id | 서버가 404 → 「없는 항목입니다」 화면. 리다이렉트하지 않는다 |

### 1-3. `next.config` 로 고정하는 것

| 설정 | 값 | 왜 |
|---|---|---|
| `output` | `'export'` | FE-C1 |
| `trailingSlash` | `true` | 정적 파일 서빙에서 `/tasks/` 가 `tasks/index.html` 로 안정적으로 떨어진다 |
| `images.unoptimized` | `true` | 이미지 최적화 서버가 없다 |

**만들지 않는 것** — `app/api/**`(Route Handler) · `middleware.ts` · Server Action · `next/headers`·`cookies()` 사용. 있으면 빌드가 깨지거나 조용히 죽는다.

**모든 `page.tsx` 는 `'use client'` 다.** 데이터가 전부 런타임 fetch 라 서버 컴포넌트가 할 일이 없다 — 「어떤 건 서버, 어떤 건 클라이언트」로 갈리는 판단을 없앤다.

## 2. 디렉토리 구조 · 명명

```text
src/
├── app/                         # 라우트 껍데기만. page.tsx 는 features 의 화면 컴포넌트 하나를 렌더한다
│
├── components/
│   ├── ui/                      # shadcn CLI 생성물 — 아래 규칙
│   └── shared/                  # 공용 컴포넌트 S-01~34 (두 영역 이상이 쓰는 것만)
│       ├── AppShell.tsx  Sidebar.tsx  PageHeader.tsx  PeriodStepper.tsx
│       ├── DrawerFrame.tsx  ConfirmModal.tsx  Selector.tsx  StatusDropdown.tsx
│       ├── StatusDot.tsx  TypeBadge.tsx  FilterChipBar.tsx  UnderlineTabs.tsx
│       ├── DataTable.tsx  TaskCard.tsx  InlineAddRow.tsx  InlineEditText.tsx
│       ├── AttachmentList.tsx  LogRow.tsx  ProgressBar.tsx  EmptyState.tsx
│       └── V2Gate.tsx           # §9
│
├── features/                    # 영역 하나 = 폴더 하나
│   ├── auth/  tasks/  meetings/  calendar/  library/  settings/  messages/
│   │   ├── components/          # 그 영역 전용 (칸반 보드·캘린더 그리드·스크립트 패널 …)
│   │   ├── hooks/               # useTasksQuery · useTaskMutations · useMeetingStream …
│   │   ├── api.ts               # 이 영역의 엔드포인트 호출 함수만
│   │   └── types.ts             # 이 영역의 응답·요청 타입
│
├── lib/
│   ├── api/
│   │   ├── client.ts            # fetch 래퍼 — Bearer 부착 · 401 refresh 재시도 · 에러 변환
│   │   ├── queryKeys.ts         # 캐시 키를 만드는 유일한 곳
│   │   └── errors.ts            # ApiError · code 상수
│   ├── auth/
│   │   ├── tokenStore.ts        # ★ 교체 지점 — 래핑 시 여기만 바꾼다(§4)
│   │   └── session.ts           # 로그인·갱신·로그아웃 상태
│   ├── overlay/OverlayProvider.tsx   # §6
│   ├── datetime.ts              # KST ↔ UTC · D-day · 표시 포맷
│   └── env.ts                   # NEXT_PUBLIC_* 를 읽는 유일한 곳
│
├── styles/
│   ├── tokens.css               # 09-design-tokens → CSS 변수 (§5)
│   └── globals.css              # Tailwind + shadcn 테마 연결
│
└── types/api.ts                 # 백엔드 schema 계약의 미러 (camelCase)
```

### 규칙 여섯

1. **`app/` 에 로직을 두지 않는다.** `page.tsx` 는 `features/<영역>/components/<Screen>.tsx` 하나를 렌더한다. 라우트 파일이 화면 코드가 되면 §1-2 의 쿼리 파싱과 뒤섞인다.
2. **`components/ui/` 는 shadcn CLI 가 만든 그대로 둔다.** 규격 차이는 **`components/shared/` 의 래퍼에서** 흡수한다 — 생성물을 직접 고치면 재생성 때 사라진다. (예외: 토큰 변수 이름을 맞추는 `className` 조정은 허용)
3. **`components/shared/` 에는 두 영역 이상이 쓰는 것만** 둔다(S-01~34 의 판정 기준). 한 영역 전용은 `features/<영역>/components/`.
4. **영역 사이 import 금지.** `features/tasks` 가 `features/calendar` 를 부르지 않는다. 공유가 필요하면 `components/shared/` 나 `lib/` 로 올린다. **단 하나의 예외**: 업무·회의 상세/생성 드로어는 캘린더·회의록이 재사용한다(F-4·F-7·DEC-005 §2) — 이 드로어들은 **소유 영역에 두고 `features/<소유영역>/components/` 에서 직접 import** 한다. 소유는 업무 드로어=`tasks`, 회의 드로어=`meetings`(DEC-005 §2 「회의록이 소유하고 캘린더가 재사용」).
5. **`fetch` 를 직접 부르지 않는다.** 모든 호출은 `lib/api/client.ts` 를 지난다.
6. **파일명은 컴포넌트 PascalCase, 훅·유틸 camelCase.** 폴더는 kebab 없이 소문자 단어.

## 3. 데이터 페칭 · 상태

### 3-1. 라이브러리 — TanStack Query v5 하나

**서버 상태는 TanStack Query, UI 상태는 URL 쿼리 + 컴포넌트 로컬 상태.** 전역 상태 라이브러리(Redux·Zustand 등)를 **두지 않는다.**

근거 — ① 이 앱의 상태는 사실상 전부 서버 상태다(단일 사용자·오프라인 없음 — SYS-8). ② 자동 저장·캘린더 드래그·상태 변경이 있어 **mutation·무효화·낙관적 갱신 API 가 명시적인 쪽**이 필요하다(SWR 보다 이 축이 두껍다). ③ 전역으로 남는 UI 상태는 **오버레이 스택 하나뿐**이고 그건 Context 로 충분하다(§6).

### 3-2. 전역 옵션 — 「설계한 실패만 처리한다」를 클라이언트에도

| 옵션 | 값 | 왜 |
|---|---|---|
| `retry` | **`false`** | DEC-001 §7 「자동 재시도를 두지 않는다 — 실패를 가린다」. 재시도는 **백엔드가 설계한 두 곳**(회의 배치·통합)에만 있고 클라이언트에는 없다 |
| `refetchOnWindowFocus` | `false` | 데스크톱 앱이라 포커스 전환이 잦고, 자동 저장 중 되감기는 사고다 |
| `staleTime` | 목록 30초 / 상세 0 | 목록은 잠깐 재사용, 상세는 열 때마다 새로 |
| `throwOnError` | `false` | 에러는 화면이 표면화한다(§3-5). ErrorBoundary 로 통째로 날리지 않는다 |

### 3-3. 캐시 키 규약

키를 만드는 곳은 **`lib/api/queryKeys.ts` 하나**다. 컴포넌트가 배열 리터럴을 직접 쓰지 않는다.

```text
['tasks', 'list', { view, filters, period }]     ['tasks', 'detail', id]
['meetings', 'list', { filters, period }]        ['meetings', 'detail', id]
['schedules', { from, to }]                      ['workTypes']  ['projects']
['documents', { folderId }]                      ['documents', 'content', id]
['folders']                                      ['jobs', id]
```

**무효화 표 — 이 표에 없는 무효화를 하지 않는다.**

| 변경 | 무효화 대상 |
|---|---|
| 업무 생성·수정·상태·삭제 | `['tasks', …]` 전부 + **기한이 바뀌었으면 `['schedules']`** |
| 회의 생성·수정·일시·삭제 | `['meetings', …]` 전부 + **일시가 바뀌었으면 `['schedules']`** |
| 유형·프로젝트 변경 | `['workTypes']`/`['projects']` + `['tasks']` + `['meetings']`(배지 이름·색이 딸려 있다) |
| 문서·폴더 변경 | `['documents']` · `['folders']` |
| 회의 job 완료 | `['meetings', 'detail', id]` |

**`schedules` 는 절대 직접 쓰지 않는다** — 읽기 전용 쿼리다(`../backend/README.md` §10). 캘린더에서 옮겨도 mutation 은 `tasks`/`meetings` 로 나가고 `['schedules']` 는 무효화로만 갱신된다(DEC-005 §3).

### 3-4. 낙관적 갱신 — 쓰는 자리를 못박는다

> **원칙: 서버가 거부할 수 있는 변경은 낙관적으로 하지 않는다.**
> 거부가 정상 경로인 곳에서 낙관적 갱신을 하면 「됐다가 되돌아가는」 화면이 자주 뜬다.

| 자리 | 낙관적? | 왜 |
|---|---|---|
| 할일 체크 · 즐겨찾기 · 메모 추가 · 인라인 텍스트 편집 | **한다** | 서버가 거부할 규칙이 없다 |
| **상태 변경(→ 완료)** | **하지 않는다** | **완료 게이트**가 거부할 수 있다(DEC-002 §4). 서버 200 을 받고 반영한 뒤 완료 토스트+실행취소(S-24)를 띄운다 |
| 상태 변경(그 외 전이) | 하지 않는다 | 전이 그래프 위반이 `409` 로 온다. 완료와 같은 코드 경로를 쓰는 편이 단순하다 |
| **캘린더 드래그** | **하지 않는다** | **겹침 차단**이 거부할 수 있다(DEC-005 §7). 즉각성은 **드래그 고스트**가 이미 준다 — 놓는 순간 서버 응답까지 그 자리를 로딩으로 유지한다 |
| 업로드 | 하지 않는다 | 파일별 성공/실패가 갈린다(DEC-004 §7) |

**드롭 자체를 막는 것은 별개다.** 겹치는 자리는 애초에 드롭되지 않고, 놓으면 원위치한다(DEC-005 §7) — 클라이언트가 이미 받은 `['schedules']` 로 미리 판정한다. 그래도 **정본은 서버 검사**이고, 드물게 통과된 드롭이 `409 schedule_overlap` 으로 돌아오면 토스트로 사유를 알린다.

### 3-5. 에러 표면화 — `code` 로 갈린다

`lib/api/client.ts` 가 응답의 `{ detail, code }`(`../backend/README.md` §8-2)를 `ApiError` 로 바꾼다. **화면은 `code` 로 분기하고 `detail` 문구로 분기하지 않는다.**

| code | 화면 처리 |
|---|---|
| `token_expired` | client 가 삼킨다 — refresh 1회 후 재시도(§4). 화면은 모른다 |
| `invalid_credentials` | 로그인 폼 인라인 에러. **횟수를 세거나 잠그지 않는다**(DEC-001 §4) |
| `task_completion_blocked` | **안내 토스트** + 완료 결과 입력으로 유도. 상태는 그대로 둔다(DEC-002 §4 · §B-2 디자인 대기) |
| `invalid_status_transition` | 토스트. 드롭다운은 원래 값으로 |
| `schedule_overlap` | **겹침 토스트 + 원위치**(DEC-005 §7 · §B-5 디자인 대기) |
| `work_type_locked` · `folder_not_empty` | 해당 항목 옆 인라인 안내 |
| `unsupported_file_type` | 업로드 드로어의 **그 파일 카드에만** 실패 표시. 성공분은 유지(DEC-004 §7) |
| `meeting_stream_disconnected` | 녹음 중지 상태로 전환 + 배너. **자동 재연결하지 않는다**(§8) |
| 그 밖 / 5xx / 네트워크 | **가리지 않는다.** 실패 토스트 + 그 자리에 재시도 버튼. 조용한 기본값·빈 목록으로 대체하지 않는다(DEC-003 §7) |

**자동 저장 실패는 전 영역 공통 규격**이다 — 토스트 + **해당 필드에 실패 상태 표시**, 자동 재시도 없음(DEC-001 §7). `InlineEditText`(S-20)·`Selector`(S-06) 등 자동 저장 컴포넌트가 **실패 상태 prop 을 공통으로 갖는다.** 화면마다 다르게 만들지 않는다. (규격 자체는 §B-6 디자인 대기)

### 3-6. 응답 형태 소비

- 목록은 `{ items: [...] }` 로 온다(`../backend/README.md` §10). **`items` 를 꺼내는 것은 `features/*/api.ts` 까지**이고, 훅 위로는 배열이 올라간다.
- 키는 camelCase 라 그대로 쓴다. **`types/api.ts` 가 백엔드 schema 의 미러**이고, 여기 없는 필드를 컴포넌트가 지어내지 않는다.
- **id 는 number** 다(PK 가 bigint). 02-data-model 의 `id: string` 표기는 디자인 표기이고 계약이 아니다.
- **시각은 UTC ISO 문자열**로 오고 **KST 변환은 `lib/datetime.ts` 하나**가 한다(G-2). 컴포넌트가 직접 `new Date()` 로 포맷하지 않는다.
- **업무 기한은 `dueDate`(날짜) + `dueStartTime`/`dueEndTime`(시각)** 이다. `schedule` 이 아니라 업무가 소유한다(DEC-005 §3, 2026-09-05 개정) — 리스트 정렬·D-day 는 이 필드로 그린다.

## 4. 인증 연동

### 4-1. 토큰 저장소 추상화 — 교체 지점 하나

`lib/auth/tokenStore.ts` 가 **refresh 토큰을 다루는 유일한 파일**이다. 인터페이스는 셋 — `get()` · `set(token, persist)` · `clear()`.

| 단계 | 구현 |
|---|---|
| **웹 개발 중(지금)** | `persist=true` → 브라우저 저장소 · `persist=false` → 메모리 변수 |
| **Tauri 래핑 후** | `persist=true` → **OS 키체인** · `persist=false` → 메모리 변수 |

**교체는 이 파일 하나로 끝나야 한다**(§C-5). 다른 파일이 `localStorage`·`sessionStorage`·Tauri 플러그인을 직접 부르면 리뷰 반려다.

- **access 토큰은 저장소에 넣지 않는다.** 메모리에만 둔다(DEC-001 §4). 새로고침하면 사라지고, 그때 refresh 로 다시 받는다.
- `persist` 는 로그인 폼의 **「로그인 상태 유지」 체크값**이다. 미체크면 앱(탭)을 닫는 순간 사라져 로그아웃된다.

### 4-2. 요청 파이프라인

`lib/api/client.ts` 하나가 전부 한다.

1. `Authorization: Bearer <access>` 부착. access 가 없으면 먼저 refresh 를 시도한다.
2. `401 token_expired` → **`POST /api/auth/refresh` 1회** → 새 토큰 저장 → **원 요청 1회 재시도**.
3. 재시도도 401 이거나 refresh 자체가 실패하면 → 토큰 전부 `clear()` → **`/login` 으로**. **무한 갱신 루프를 만들지 않는다**(`../system/README.md` §흐름 ①).
4. 동시에 여러 요청이 401 을 받으면 **refresh 는 한 번만** 나간다(진행 중인 refresh Promise 를 공유). 나머지는 그 결과를 기다린다.
5. 성공 응답은 그대로, 실패 응답은 `ApiError{status, code, detail}` 로 던진다.

**WS 는 헤더를 못 붙인다** — 연결 직후 **첫 텍스트 프레임으로 access 토큰**을 보낸다(`../backend/README.md` §5-1). 그 규약도 `lib/api` 안에 둔다.

### 4-3. 세션 가드

`(app)/layout.tsx` 가 유효 세션을 확인하고, 없으면 `/login` 으로 보낸다. **미들웨어를 쓸 수 없으므로**(FE-C1) 가드는 레이아웃 컴포넌트다. 로그인 화면만 셸 밖이다(F-1).

## 5. 토큰 → CSS 변수 → shadcn 테마

### 5-1. 두 층으로 나눈다

```text
styles/tokens.css   :root { --tm-*  }        ← 09-design-tokens 원시값. 여기가 정본
styles/globals.css  :root { --primary: var(--tm-primary); … }   ← shadcn 시맨틱 변수에 연결
```

**원시 토큰(`--tm-*`)을 컴포넌트가 직접 쓰지 않는다.** shadcn 시맨틱 변수나 Tailwind 유틸을 쓴다 — 디자인이 값을 바꿀 때 고칠 자리가 `tokens.css` 하나로 남는다.

| 축 | 변수 | 값 |
|---|---|---|
| 액션·완료 | `--tm-primary` / `--tm-primary-hover` | `#7181F8` / `#5F71F5` |
| **위치** | `--tm-ink` | `#1E1E1E` |
| 본문 계열 | `--tm-fg` `--tm-fg-muted` `--tm-fg-meta` `--tm-fg-caption` | `#1E1E1E` `#5F6470` `#757575` `#9EA2AE` |
| **선택** | `--tm-select-bg` / `--tm-select-fg` | `#F1F2FE` / `#4B52A8` |
| 면·선 | `--tm-hover` `--tm-row-hover` `--tm-border` `--tm-divider` `--tm-row-divider` `--tm-canvas` | 09-design-tokens §색 그대로 |
| 상태 dot 5색 | `--tm-status-{todo,progress,done,cancelled,overdue}` | `#9EA2AE` `#33AAFF` `#7181F8` `#B3B3B3` `#E2685B` |
| 형태 | `--tm-radius-{card,control,chip}` · `--tm-shadow-{card,drawer,modal,popover}` | 09-design-tokens §형태 |

**타입** — Pretendard Variable, `letter-spacing: -0.02em` 기본. 타이포 계단(페이지 타이틀 28/700/-0.03 … 캡션 12)은 **Tailwind 유틸 프리셋**으로 고정하고 컴포넌트가 임의 크기를 쓰지 않는다.

### 5-2. 「검정은 위치, 보라는 선택」을 구조로 지킨다

디자인 시스템의 규칙(`09-design-tokens.md`)을 **컴포넌트 캡슐화로** 강제한다.

- `--tm-ink` 를 쓰는 컴포넌트는 **셋뿐**이다 — `Sidebar` 활성 pill · 뷰 토글(`ToggleGroup`) 선택 · `UnderlineTabs` 선택 밑줄. 그 밖의 컴포넌트에서 이 변수를 쓰면 반려.
- **화면당 Ink 는 하나**다. 리뷰 체크 항목으로 남긴다.
- 필터 칩·체크·선택 카드는 `--tm-select-bg` + `--tm-primary`.
- 토스트 배경은 예외로 Ink 를 쓴다(오버레이 서피스).

### 5-3. 동적 유형 색 — 토큰이 아니라 런타임 값

유형·프로젝트 색은 **설정에서 사용자가 고른 값**이라 빌드 타임 토큰이 아니다(DEC-001 §3 · §A-1). 하지만 **자유 색상이 아니라 「디자인 시스템 허용 팔레트 중 선택」**이다 — DB 가 드는 것은 hex 가 아니라 **팔레트 토큰명**(`work_type.color_token`).

그래서 처리는 이렇다.

1. `tokens.css` 에 **허용 팔레트 전체를 미리 정의**한다 — 토큰명마다 `--tm-palette-<name>-bg` / `-fg` 쌍.
2. 배지·칩·캘린더 블록은 `data-color-token="<name>"` 속성을 받고, CSS 가 그 속성으로 변수 쌍을 고른다.
3. **인라인 `style={{ background: hex }}` 를 쓰지 않는다.** hex 가 컴포넌트에 들어오는 순간 팔레트 제약(DEC-001 §3)이 코드에서 사라진다.
4. 팔레트에 없는 토큰명이 오면(삭제된 유형의 옛 값 등) **중립 색으로 떨어뜨리고 조용히 숨기지 않는다.**

`TypeBadge`(S-09)의 **고정 4종은 폐기**됐다(§A-1). 「취소」도 유형이 아니라 상태다(§A-2) — 취소 표시는 제목 취소선·회색·캘린더 점선 칩으로만.

## 6. 오버레이 3종 — 공통 프레임

| | 폭 | 스크림 | 용도 | shadcn |
|---|---|---|---|---|
| **Drawer** | 840 | `rgba(30,30,30,0.32)` | **값을 여러 개 넣는 편집** | `Sheet side="right"` (C-01) |
| **Modal** | 600 | `rgba(30,30,30,0.36)` | **되돌리기 어려운 결정 하나** | `AlertDialog`/`Dialog` (C-02) |
| **Popover** | 200–400 | 없음 | **고르기** | `Popover` (C-03) |

### 6-1. `OverlayProvider` 하나가 연다

전역 UI 상태는 이것뿐이다(§3-1). `lib/overlay/OverlayProvider.tsx` 가 **스택**을 들고, API 는 셋이다.

```text
openDrawer({ key, title, badge?, expandTo?, content })   // 편집
openConfirm({ title, summary, warning?, onConfirm })      // 결정
// Popover 는 트리거 옆에서 열리므로 전역 스택에 넣지 않는다 — Radix 에 맡긴다
```

**함수 이름이 곧 용도 규칙이다.** 「편집은 드로어, 결정은 모달」이 API 두 개로 갈려 있어 잘못 쓰기 어렵다. `Sheet`·`Dialog` 를 컴포넌트가 **직접 import 하지 않는다** — 그러면 규격(840/600·스크림·헤더 72·푸터 76)이 화면마다 갈린다.

### 6-2. 강제하는 규칙 넷

| 규칙 | 강제 방법 |
|---|---|
| **드로어 위에 모달을 겹치지 않는다**(09-design-tokens) | Provider 가 스택을 본다. 드로어가 열린 상태에서 `openConfirm` 이 오면 **개발 모드에서 throw**, 운영에서는 드로어를 먼저 닫고 연다 |
| 드로어는 **뒤 화면이 보인다**(F-3) | 스크림 불투명도를 `DrawerFrame`(S-04)이 고정한다. 화면이 덮어쓰지 못한다 |
| 같은 드로어가 **여러 부모에서 열린다**(F-4) | 드로어 컴포넌트는 **부모를 모른다.** 부모가 `openDrawer` 를 부르고 콜백으로 결과를 받는다 |
| **⤢ 는 전체 페이지로 승격**된다(F-5) | `expandTo` 에 라우트를 준다(`/tasks/detail?id=`). 드로어가 닫히고 그 라우트로 이동한다 |

드로어는 **동시에 하나**만 연다. 드로어 안에서 다른 드로어를 열어야 하면 **같은 드로어의 단계 전환**으로 만든다.

## 7. 유동 반응형

**1920 실측 좌표는 비율·최소폭의 참고값이다.** `position:absolute` 로 박지 않는다(§C Q-34 · §A-13). 기준은 `08-responsive.md` — 본문 유동, 좌우 여백만 줄인다.

### 7-1. 세 구간

| 구간 | 사이드바 | 좌우 여백 | 드로어 | 리스트 | 칸반 |
|---|---|---|---|---|---|
| **< 1280** | — | — | — | **최소 폭 안내 화면(P-02)** | — |
| **1280 ~ 1439** | 숨김 + 햄버거 오버레이(P-03) | 48 | **전체 화면** | 시작일 컬럼 숨김 | 컬럼 **320 고정 + 가로 스크롤** |
| **≥ 1440** | **200 고정** | 80 → 240 으로 **연속 보간** | 840 | 전체 컬럼 | 4컬럼 `1fr` |

- **본문은 최대폭 제한이 없다.** 여백만 `clamp()` 로 이어 준다 — 1440 에서 80, 1920 에서 240 이 되도록.
- Tailwind `screens` 를 이 표에 맞춰 재정의한다 — `desk: 1280px` · `wide: 1440px` · `ultra: 1920px`. 기본 브레이크포인트(sm/md/lg)를 쓰지 않는다.
- **사이드바에 아이콘 축소형을 만들지 않는다.** 200 이 아니면 숨김이다(`08-responsive.md` L16 · C-27).
- **칸반은 컬럼을 좁히지 않는다.** 기본 320, 최소 240, 안 들어가면 가로 스크롤하고 **리스트로 자동 전환하지 않는다.**
- 1280 구간 상세는 좌(유동) + 우(400 고정) 2단.

> **F-6 의 「1280 미만에서 드로어가 전체 화면」은 부정확하다.** 1280 미만은 안내 화면이라 드로어가 뜰 자리가 없다.
> `08-responsive.md` 표가 정본이고, **전체 화면 구간은 1280 ~ 1439** 다. 전환되면 스크림이 사라지고 헤더 좌측에 `←` 가 생긴다(헤더 74 한 줄).

### 7-2. 최소 폭 가드 — Q-30 확정

**안내 화면(P-02)으로 처리한다.** Tauri 창 `minWidth` 로 막지 않는다.

근거 — 웹 우선 개발이라 개발 내내 셸이 없다(§C-4). 창 크기로만 막으면 브라우저에서는 아무 보호가 없고 래핑 후에만 생겨 두 환경이 갈린다. 화면으로 두면 양쪽이 같다. (래핑 시 `minWidth` 를 **추가로** 걸지는 그때 정한다 — FE-OQ-3)

## 8. 실시간 처리 — 회의 스트림

`features/meetings/hooks/useMeetingStream.ts` 하나가 WS 를 소유한다. 컴포넌트가 `WebSocket` 을 직접 만들지 않는다.

| 단계 | 규약 |
|---|---|
| 연결 | `WS /api/meetings/{id}/stream` → **첫 텍스트 프레임으로 access 토큰**(§4-2) |
| 마이크 | **웹 `getUserMedia`**(§C-7). Tauri 웹뷰 확인은 래핑 시점이다 — 지금 코드는 브라우저 API 만 쓴다 |
| 포맷 | **특정 포맷에 묶지 않는다**(§C-8). 캡처·인코딩은 훅 안의 함수 하나로 격리해 구현 시점에 고른다 |
| 업로드 | 오디오 청크를 그대로 보낸다. **Soniox 주소도 키도 프론트가 모른다**(DEC-003 §STT) |
| **잠정 토큰** | 받을 때마다 **마지막 잠정 블록을 통째로 교체**(리셋 렌더)한다. 회색으로 그린다 |
| **확정 토큰** | **append 한다.** 지우거나 다시 쓰지 않는다. 화자 전환마다 블록을 나눈다(익명 「화자 1/2」 — DEC-003 §2) |
| **AI 증분** | 오는 즉시 AI 탭에 반영한다. **버퍼링하지 않는다.** 함께 오는 **배치 회차**로 「배치 2회 → 3회 → 종결」을 표시한다(DEC-003 §4, 2026-09-05) |
| **AI 안건** | AI 안건은 **AI 탭에만** 그린다. 회의 중 사람 회의록 탭에 섞지 않는다(2026-09-05) |
| **끊김** | **자동 재연결하지 않는다.** 녹음 중지 상태로 전환하고 배너로 드러낸다 — 조용히 되살리면 오디오가 빈 구간이 가려진다(DEC-003 §7) |
| 종료 | `POST /api/meetings/{id}/end` → `202 {jobId}` → **WS 닫고 job 폴링**(2초). `succeeded`/`failed` 에서 멈추고, 완료 후 회의 상세를 다시 읽는다(`../backend/README.md` §6) |
| 실패 표시 | `status='ended'` + `integrationState='failed'` 이면 **「통합 정리 실패 · 다시 생성」 배너**. 「다시 생성」은 **이 조합에서만** 보인다(DEC-003 §4) |

**AI 요약 탭은 「안건 > 줄」 트리**다(§A-8) — 회의록 탭과 같은 구조에 근거 칩이 붙는다. 근거 칩을 누르면 스크립트 패널이 해당 구간으로 스크롤·하이라이트한다(C-37). **트리 렌더 규격은 §B-3 디자인 대기**이고, 데이터 구조(트랙별 안건·줄·`evidence`)는 이미 닫혀 있다.

## 9. v2 스코프 표시 — 공통 컴포넌트 하나

**v2 기능의 UI 는 v1 에서 그대로 그린다.** 숨기지 않고, 비활성 처리하고, 조작하면 「v2에서 제공됩니다」 토스트를 띄운다(DEC-001 §v2 스코프 — 전 영역 공통).

`components/shared/V2Gate.tsx` 가 이걸 **혼자** 한다.

- children 을 감싸 `aria-disabled` 를 붙이고 **포인터·키보드 이벤트를 가로채** 토스트만 띄운다.
- **children 을 바꾸지 않는다** — 원래 컴포넌트를 그대로 그린다. 회색 처리는 게이트가 얹는 한 겹이다.
- 화면마다 `disabled` prop 을 흩뿌리지 않는다. **감싸는 것 하나**로 통일해야 v2 에서 걷어내기가 쉽다.

**적용 대상** — 소셜 로그인 버튼 · 목소리 패널과 드로어 · 연동 관리 화면 · 계정 삭제 · 「다른 기기 모두 로그아웃」(DEC-001) · AI 색인 상태 · 문서 버전 카드 · 문서 검색 · 휴지통(DEC-004) · **메시지함 전체**(DEC-006 — 사이드바 메뉴는 정상 노출·정상 진입하고, 들어가면 필터 카드·목록·빈 상태가 비활성으로 보인다).

**서버에는 v2 엔드포인트가 없다**(`../backend/README.md` §8-2). 게이트가 새서 실제 호출이 나가면 `501 v2_not_available` 로 돌아온다 — 정상 경로가 아니라 안전망이다.

## 10. 사이드바 8메뉴 vs v1 6영역

사이드바는 8메뉴를 요구하는데(P-01 — 홈·채팅·캘린더·내 업무·회의록·자료함·메시지·설정) **v1 정책서는 6영역뿐**이다. 홈·채팅은 BASE/DEC 문서가 없다(Q-37·Q-38).

**결정 — 홈·채팅은 라우트를 만들지 않고, 사이드바 항목은 `V2Gate` 로 그린다.**

근거 — ① 정책서가 없는 영역의 화면 구조를 아키텍처가 발명할 수 없다(역할 규약). ② DEC-001 §v2 가 「숨기지 않는다」를 전 영역 공통으로 못박았으므로 메뉴를 지우는 것은 정책 위반이다. ③ DEC-006 이 메시지함에 쓴 방식(메뉴 노출 + 비활성 화면)과 같은 결이다.

메시지함과 다른 점 하나 — 메시지함은 **화면이 그려져 있어 진입한다.** 홈·채팅은 화면 원본이 없으므로(`홈화면.dc.html` 이 워크트리에서 삭제됨 — 리포트 §0-B) **진입하지 않고 토스트만** 띄운다. 정책서가 생기면 그때 라우트를 연다(FE-OQ-1).

## 11. 테스트 · 품질 규약

| 항목 | 규약 |
|---|---|
| 러너 | **Vitest + React Testing Library**. 컴포넌트를 사용자 관점(역할·라벨)으로 조작한다 |
| 네트워크 | **MSW** 로 `lib/api/client.ts` 아래에서 가로챈다. 훅·컴포넌트를 목으로 바꾸지 않는다 |
| 타입 | `types/api.ts` 가 백엔드 계약의 미러다. **`any` 를 쓰지 않는다** — 응답 형태가 흔들리면 여기서 먼저 깨져야 한다 |
| 린트 | 아래 「금지 목록」을 가능한 것부터 ESLint 규칙으로 옮긴다. 규칙으로 못 옮기는 것은 리뷰 체크리스트 |

**반드시 있어야 하는 테스트** — 없으면 리뷰 반려다.

1. **완료 게이트** — `422 task_completion_blocked` 를 받으면 **상태 셀이 바뀌지 않고** 안내 토스트가 뜬다(낙관적 갱신을 안 하는 것의 증명 — DEC-002 §4).
2. **겹침 차단** — `409 schedule_overlap` 을 받으면 일정이 **원위치**하고 사유 토스트가 뜬다(DEC-005 §7).
3. **자동 저장 실패** — 실패 응답에 **토스트 + 그 필드의 실패 표시**가 함께 뜨고 **재시도가 나가지 않는다**(DEC-001 §7).
4. **401 갱신** — 만료 → refresh 1회 → 원 요청 재시도. **두 번째 401 이면 로그인으로 가고 루프가 없다**(§4-2).
5. **토큰 저장소 격리** — `persist=false` 로 로그인하면 저장소에 아무것도 남지 않는다. **`tokenStore` 밖에서 저장소 API 를 부르는 코드가 없다**(정적 검사 — §C-5).
6. **오버레이 규칙** — 드로어가 열린 상태에서 `openConfirm` 이 개발 모드에서 throw 한다(§6-2).
7. **v2 게이트** — 감싼 요소를 조작하면 **네트워크 요청이 나가지 않고** 토스트만 뜬다(DEC-001 §v2).
8. **정적 빌드 산출** — `next build` 가 `out/` 을 만들고, `app/api/**`·`middleware.ts` 가 없으며, **동적 세그먼트 디렉토리(`[…]`)가 없다**(FE-C1 · §1-2).

**하지 않는 것 — 명시적으로 안 한다.**

- **픽셀 스냅샷 테스트를 만들지 않는다.** 유동 레이아웃이라 폭마다 값이 달라 의미가 없고, 1920 좌표를 다시 못 박는 결과가 된다(§C Q-34).
- **E2E(Playwright 등)를 v1 에 넣지 않는다.** 회의 STT·codex 가 붙는 흐름이라 비용이 크다. 그 구간은 백엔드 테스트가 덮는다(`../backend/README.md` §12).
- **접근성 전수 검사를 하지 않는다.** 단일 사용자 데스크톱 도구다. 키보드로 닫기(`Esc`)·포커스 트랩 같은 **오버레이 기본기만** 지킨다.

### 금지 목록 (리뷰 반려 사유)

1. `fetch` 직접 호출 (§2-5)
2. `localStorage`/`sessionStorage`/Tauri API 를 `tokenStore.ts` 밖에서 호출 (§4-1)
3. `Sheet`/`Dialog` 를 컴포넌트에서 직접 import (§6-1)
4. 인라인 `style` 로 색 hex 지정 (§5-3)
5. `position: absolute` 로 레이아웃 배치 (§7)
6. 동적 세그먼트 라우트 `[id]` (§1-2)
7. `catch` 후 빈 배열·기본값으로 대체 (§3-5 · DEC-003 §7)
8. 컴포넌트에서 직접 `new Date()` 포맷 (§3-6)

## 12. 결정 요약 — 근거 색인

| # | 결정 | 근거 |
|---|---|---|
| FE-1 | 라우트는 리포트 §3.2 를 확정 승격. 홈·채팅·회원가입 제외 | DEC-001 §1 · §10 |
| FE-2 | **오버레이에 URL 을 주지 않는다**(Q-29 확정) | FE-C1 · F-4 · F-5 |
| FE-3 | **동적 세그먼트 금지, 식별·뷰는 쿼리**(Q-31·Q-32 확정) | FE-C1 |
| FE-4 | 모든 page 는 `'use client'`. Route Handler·미들웨어·Server Action 없음 | §C Q-28 |
| FE-5 | 서버 상태 = TanStack Query, 전역 상태 라이브러리 없음 | §3-1 |
| FE-6 | **`retry: false`** — 클라이언트 자동 재시도 없음 | DEC-001 §7 · DEC-003 §7 |
| FE-7 | **낙관적 갱신은 서버가 거부할 수 없는 변경에만** | DEC-002 §4 · DEC-005 §7 |
| FE-8 | `schedules` 는 읽기 전용. 캘린더 변경은 `tasks`/`meetings` 로 | DEC-005 §3 (2026-09-05) |
| FE-9 | **토큰 저장소 추상화 한 파일** — 래핑 시 여기만 교체 | §C-5 |
| FE-10 | 토큰은 `--tm-*` → shadcn 시맨틱 변수 2층. 동적 유형 색은 **미리 정의된 팔레트 변수 + `data-color-token`** | §C Q-33 · DEC-001 §3 |
| FE-11 | 오버레이는 Provider API 두 개(`openDrawer`/`openConfirm`)로 용도를 강제 | 09-design-tokens §오버레이 |
| FE-12 | 유동 3구간(1280 미만 안내 / 1280–1439 / 1440+), absolute 금지 | §C Q-34 · §A-13 |
| FE-13 | 최소 폭은 **안내 화면**으로 막는다(Q-30 확정) | §C-4 |
| FE-14 | v2 표시는 **`V2Gate` 하나**. 숨기지 않는다 | DEC-001 §v2 |
| FE-15 | 실시간은 WS 훅 하나. **자동 재연결 없음**, AI 증분 즉시 반영 + 배치 회차 표시 | DEC-003 §4·§7 (2026-09-05) |

## 디자인 대기 — 구조는 확정, 화면만 비어 있다

`design-requests.md §B` 의 미설계 화면은 **이 문서의 구조 결정을 막지 않는다.** 화면 규격이 도착하면 채울 자리만 표시한다.

| 자리 | 무엇이 없나 | 구조는 |
|---|---|---|
| 완료 결과 입력 UI | 입력 위치·거부 토스트 문구(§B-2) | 게이트 판정·`code` 분기는 확정(§3-5) |
| 칸반 DnD 규격 | 하이라이트·플레이스홀더(§B-2) | 컬럼 320/240·가로 스크롤은 확정(§7-1) |
| AI 요약 탭 트리 · 「생성중」 화면 | 렌더·스피너·실패 배너(§B-3) | 트랙별 데이터·job 폴링은 확정(§8) |
| 캘린더 드래그 시각 규격 | 드롭 가능/불가·고스트(§B-5) | 낙관적 갱신 금지·원위치 처리는 확정(§3-4) |
| 자동 저장 실패 표시 | 필드 실패 상태의 생김새(§B-6) | 공통 prop·재시도 없음은 확정(§3-5) |
| 업무 설정 화면 | 유형·프로젝트 관리(§B-1) | 라우트 `/settings/work` 확정(§1) |
| 1280 반응형(회의록·설정·캘린더·문서함) | 영역별 규격(§B-6) | 세 구간 규칙은 확정(§7-1) |

## Open Questions

| ID | Question | Owner | Next |
|---|---|---|---|
| FE-OQ-1 | **홈·채팅 영역의 정책서**(Q-37·Q-38) — 사이드바가 8메뉴를 요구하는데 BASE/DEC 가 6개뿐이다. 지금은 `V2Gate` 로 그리고 라우트를 만들지 않았다(§9). 정책서가 생기면 라우트를 연다 | 사용자 | v1 이후 |
| FE-OQ-2 | **브라우저 하한**(Q-41) — `:has()`·container query·`dvh`·subgrid 를 쓸 수 있는지가 정해지지 않았다. **지금은 이 넷을 쓰지 않는 선에서 짠다** — 래핑 후 WKWebView·WebView2 확인에서 하한이 정해지면 완화한다 | 코디 | 래핑 단계 |
| FE-OQ-3 | **Tauri 창 `minWidth` 추가 여부** — 최소 폭은 안내 화면으로 막기로 확정했다(§7-2). 래핑 시 창 크기 제한을 **덧붙일지**는 그때 정한다 | 사용자 | 래핑 단계 |
| FE-OQ-4 | **문서 편집기 선택**(C-34) — 마크다운 소스 편집(문법 기호 흐리게 + 서식 툴바)을 어느 에디터로 세울지는 화면 규격과 함께 정한다. 구조(3열 레이아웃·탭·자동 저장)는 확정 | 코디 | spec |
