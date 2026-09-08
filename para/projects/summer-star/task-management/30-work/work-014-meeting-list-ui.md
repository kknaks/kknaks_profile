---
type: work
id: WORK-014
title: "목록 · 상세 UI — breadcrumb 링크 · 「←」 · 미리보기 패널 · 헤더 순서"
status: done
product: "task-management"
work_type: refactor
owner: ""
roles:
  pm: ""
  design: ""
  fe: ""
  be: ""
  qa: ""
  ops: ""
progress: 0
created_at: 2026-09-07
updated_at: 2026-09-07
tags:
  - product/task-management
  - doc/work
  - status/todo
links:
  baselines: [BASE-003]
  decisions: [DEC-003]
  specs: [SPEC-006, SPEC-008]
  works: [WORK-006, WORK-008]
  releases: []
  related: [SPEC-007, SPEC-003, WORK-013]
---

# 목록 · 상세 UI — breadcrumb 링크 · 「←」 · 미리보기 패널 · 헤더 순서

**돌아갈 길과 들어갈 길이 없다.** breadcrumb 이 전부 `<span>` 이라 상세에서 목록으로 돌아갈 어포던스가 없고(F-5), 미리보기 CTA 가 상태와 무관하게 「상세보기」이며, 패널이 회의를 고르면 화면 밖으로 넘어가 잘렸고, 헤더가 「제목 → 부제」 순서다. 이 work 는 **화면의 뼈대 넷**을 고친다 — 다른 WP 와 겹치지 않는 **독립 WP** 다.

> 1 파일 = 1 work = **빌드 계획**. dev 가 이 문서만 보고 PR 분리 / 일정 / 작업 시작이 가능해야 한다.
> SPEC 의 외부 계약 본문은 복제하지 않고 frontmatter `links.specs` 와 index 에서 연결한다.
> **결정 원본은 `reference/2026-09-06-task-management-app/Meeting flow.md`** — **MF-5 · 6 · 7 · 8**. 계약과 부딪히면 그쪽이 이긴다.

## Meta

- Baseline: BASE-003 #1(목록) · #2(시작 전)
- Covers spec
  - **SPEC-006 U-1**(목록 골격 — breadcrumb 의 「홈」은 **링크** · 목록이라 「←」 없음) · **U-4**(시작 전 — **「←」 + breadcrumb** · 헤더 **① 배지 줄 → ② 제목 → ③ 메타 한 줄**) · **U-6**(반응형 — **미리보기 패널은 빈 상태 크기에 고정 · 넘치면 패널 안 스크롤 · 뷰포트 밖으로 안 나간다**) · **U-8**(미리보기 패널 — **CTA 라벨 상태별 표 4행** · 본문 트리는 상세와 **같은 컴포넌트를 compact 밀도로**)
  - **SPEC-007 U-1 Placement**(회의 중 헤더도 배지 줄 → 제목 · 「일시정지 · 회의 종료」는 배지 줄 우측 액션 자리) · **§6 AC 「헤더가 배지 줄 → 제목 → 「MM월 DD일 …」 순서이고 breadcrumb 「홈」·「회의록」이 링크이며 「←」로 목록에 간다」**
  - **SPEC-008 U-3 헤더 1~4**(「←」 + breadcrumb → 배지 줄(우측 삭제 · 상태 칩) → 제목 → 메타 한 줄)
  - **FE §2 규칙 7**(같은 구조를 다른 밀도로 그릴 때 컴포넌트를 쪼개지 않고 `props` 로만 가른다) · **§6-3 상세 화면 헤더 규약 3행**(breadcrumb 은 링크 · 상세에 「←」 · 헤더 순서는 업무 헤더가 정본) · **§7-1 반응형**
- Depends on work: 계약상 **없다**(독립). 다만 **`AgendaLineTree.tsx` 를 WORK-013 과 함께 만진다** — 013 이 `onChangeKind` 를 걷어내고 이 work 가 `density` 를 더한다. **머지 순서는 013 → 014**
- Parallel work: 없음 — **코드 워커는 한 번에 하나**
- Follow-up work: 없음
- **External dependency**
  - **시안 없음**(반응형 · 「←」 · 밀도). 규격은 **FE §6-3 · §7-1 · [09] 트리 규격**으로 조립한다
  - **업무 화면은 안 고친다.** 「←」·breadcrumb 링크는 **공용 부품**(`components/shared/AppShell.tsx`)을 고치는 것이라 업무·설정 화면이 **덤으로 따라온다** — 그것이 MF-7 의 뜻이다(「회의록만 고치면 업무·설정에 같은 것이 남는다」). 그 밖에 `features/tasks` 를 수정하지 않는다

## Work Summary

| Field | Value |
|---|---|
| Type | refactor |
| Owner |  |
| Status | todo |
| Progress | 0% |
| Branch/PR | `kknaksss/docs-v1` |
| Blocker | 없음 |
| Next | Phase 1 — `Breadcrumb` 링크 + `backTo` |

## Role Assignment

| Role | Assignee | Responsibility | Status |
|---|---|---|---|
| PM |  | SPEC-006 §6 · SPEC-007 §6 · SPEC-008 §6 의 헤더·패널 관련 5항목 대조 | todo |
| Design |  | **시안 없음** — 디자인 시스템 규격대로인지 확인만 | — |
| FE |  | Phase 1~3 전부 | todo |
| BE |  | 해당 없음 — **백엔드 변경 0** | — |
| QA |  | 링크 0건 아님 · 키보드 도달 · 패널이 뷰포트 밖으로 안 나감 · CTA 라벨 4행 · 헤더 순서 3화면 | todo |
| Ops |  | 해당 없음 | — |

## Scope

포함:

- **`Breadcrumb` 을 링크로**(MF-7) — 마지막 항목만 `<span>`, 앞 단계는 전부 `<a>`. hover·focus 표시 · **키보드로 닿는다**. `trail` 이 문자열 배열이라 **경로를 함께 받는 모양으로 바꾼다**
- **「←」 = 부모 라우트로**(MF-7) — `router.back()` 이 **아니다**. 회의록 상세 → `/meetings/` · 업무 상세 → `/tasks/`. **목록 화면에는 없다**
- **`PageHeader`(S-02)는 아직 없다** — `AppShell.tsx` 안에 **`backTo` 를 받는 상세 헤더 자리**를 만든다(신설 파일을 만들지 않고 `AppShell` 이 breadcrumb 슬롯 옆에 「←」를 그린다). 상세 화면은 `backTo` 를 **반드시** 넘긴다
- **미리보기 CTA 라벨 상태별**(MF-5) — `scheduled`·`recording` 「**회의 입장**」 / `generating`·`ended` 「**상세보기**」
- **미리보기 패널 크기 고정 · 패널 안 스크롤**(MF-6) — 빈 상태(회의 0건)일 때의 크기가 기준. 본문이 넘치면 **패널이 밀려나는 게 아니라 패널 안에서 세로 스크롤**. **어느 구간에서도 뷰포트 밖으로 나가지 않는다**
- **`AgendaLineTree` 에 `density` prop**(FE §2 규칙 7) — `"default" | "compact"`. **미리보기용 트리 컴포넌트를 따로 만들지 않는다**
- **헤더 순서 세 화면**(MF-8) — 시작 전(`MeetingScheduledPage`) · 회의 중(`MeetingLiveView`) · 종료 후(`MeetingClosedPage`)가 전부 **① breadcrumb 줄(+「←」) → ② 배지 줄(유형 · 프로젝트 · 우측 액션) → ③ 제목 → ④ 메타 한 줄**
- 테스트 — FE §11 규약대로(역할·라벨로 조작). 링크 · 「←」 · CTA 라벨 · 밀도 · 헤더 순서

제외:

- **업무 화면 · 캘린더 · 문서함 · 설정** — 공용 `Breadcrumb`·「←」가 덤으로 좋아지는 것 외에 **손대지 않는다**
- **미리보기 패널의 본문 내용**(최종 회의록 트리 · 한 줄 요약 바 카운트) → **WORK-012**(카운트 다섯) · 이 work 는 **밀도와 크기**만
- **줄 버튼 · 편집 · 드로어** → WORK-013
- **줄 시각 제거 · 슬래시** → WORK-011
- **`MeetingDetailDrawer`(U-4 드로어)의 헤더** — 이미 배지 줄 → 제목 순서라 MF-8 에 맞다(SPEC-008 U-4). 확인만 하고 고치지 않는다

## Code Surface

- Repo / module: `github.com/kknaks/task_management` — **`app/front` 만**

| 경로 | 신규 / 수정 / 폐기 | 설명 |
|---|---|---|
| `app/front/src/components/shared/AppShell.tsx` `Breadcrumb`(L28~46) | 수정 | `trail: readonly {label, href?}[]` — **`href` 가 있으면 `<a>`**, 마지막은 항상 `<span>`(색만 진하게). hover·focus 링. `TRAIL` 상수(L56~62)도 같은 모양으로 |
| 〃 `DetailHeaderBar`(신규 · 같은 파일) | **신규** | `backTo?: string` 을 받아 breadcrumb 왼쪽에 **「←」**(부모 라우트 `<a href>`)를 그린다. **`PageHeader.tsx` 를 새로 만들지 않는다** — FE §2 목록에 이름만 있고 파일이 없다. `AppShell` 이 이미 breadcrumb 슬롯을 갖고 있어 그 자리에 둔다 |
| 〃 `AppShell` props | 수정 | `breadcrumb` 슬롯은 그대로. 상세 화면이 `<DetailHeaderBar backTo=… trail=…/>` 를 넘긴다 |
| `app/front/src/features/meetings/components/MeetingScheduledPage.tsx`(L101~115 부근) | 수정 | `<Breadcrumb trail={["홈","회의록","시작 전"]}/>` → `<DetailHeaderBar backTo="/meetings/" trail=[홈(/), 회의록(/meetings/), <제목>]/>`. 헤더를 **배지 줄 → 제목 → 메타 한 줄** 순서로. 「회의 시작」·`⋯` 은 배지 줄 **우측 액션** 자리 |
| 〃 `MeetingLiveView.tsx`(L241~279) | 수정 | 같은 교체. 「일시정지」·「회의 종료」가 배지 줄 우측 액션 자리(SPEC-007 U-1 Placement) |
| 〃 `MeetingClosedPage.tsx`(L40~60) | 수정 | 같은 교체. 「삭제」 + 상태 칩이 배지 줄 우측 |
| 〃 `MeetingMetaInline.tsx` | 수정 | `MeetingMetaLine` 이 **일시 · 소요만** 그리도록(유형 · 프로젝트는 배지 줄로 올라간다). `MeetingWorkTypeInline` · `MeetingProjectInline` 은 `variant="badge"` 로 배지 줄에서 쓴다 — **컴포넌트는 그대로 쓰고 배치만 바꾼다** |
| 〃 `MeetingPreviewPanel.tsx`(L105~170) | 수정 | ① 헤더 CTA **라벨 상태별 4행** + 가는 곳 ② 패널 **크기 고정 + 본문 `overflow-y-auto`** ③ 본문 트리에 `density="compact"` |
| 〃 `MeetingsScreen.tsx` | 수정(최소) | 좌 목록 / 우 패널 폭 규칙(§7-1) — **패널이 뷰포트 밖으로 나가지 않게** `min-w-0` · `flex-1` 정리. `position:absolute` 를 쓰지 않는다 |
| 〃 `AgendaLineTree.tsx` | 수정 | `density?: "default" \| "compact"` — 글자 · 여백 · 라벨 폭만 가른다. **구조 · 배지 · 펼침 규칙은 하나** |
| 〃 `AgendaHeader.tsx` · `LineRow.tsx` | 수정(최소) | `density` 를 받아 클래스만 가른다 |
| 〃 `MeetingPreviewPanel.test.tsx` · `MeetingScheduledPage.test.tsx` · `MeetingLiveView.test.tsx` · `MeetingClosedPage.test.tsx` · `AgendaLineTree.test.tsx` | 수정 | 아래 검증 |
| `app/front/src/components/shared/AppShell.test.tsx` | **신규** | breadcrumb 링크 · 「←」 |

- Domain / schema note: **리비전 0건 · 백엔드 변경 0건 · API 변경 0건**

## Domain / Schema

| Entity | 역할 |
|---|---|
| — | **없다.** 이 work 는 화면만 만진다 |

- 상태 / invariant: 없음
- Migration 필요 여부: **없음**
- SPEC 에 환류해야 하는 변경: 없음

## Dependency

| Consumer | Interface | 설명 |
|---|---|---|
| 업무 · 설정 · 캘린더 화면 | `Breadcrumb` · `DetailHeaderBar` | **공용 부품이라 함께 좋아진다.** 업무 상세는 `backTo="/tasks/"` 를 넘기게 된다 — 그 한 줄 외에 `features/tasks` 를 고치지 않는다 |
| **WORK-013** | `AgendaLineTree.tsx` | 013 이 `onChangeKind` 를 걷어낸다 — **013 이 먼저 머지**. 이 work 는 같은 파일에 `density` 를 더한다 |
| **WORK-012** | `MeetingClosedPage.tsx` · `MeetingStatusBar` | 012 가 생성중·실패·카운트를, 이 work 가 **헤더 순서**를 만진다. 같은 파일이라 **012 → 014** 순으로 머지 |

## Internal Interface Contract

외부 계약(헤더 순서 · CTA 표 · 패널 규칙)은 **SPEC-006 U-1 · U-4 · U-6 · U-8 · SPEC-008 U-3 · FE §6-3** 이 정본이다. 여기는 부품 접점만 고정한다.

| 접점 | 계약 |
|---|---|
| **`Breadcrumb` trail** | `readonly { label: string; href?: string }[]`. **마지막 항목은 `href` 를 무시하고 `<span>`** 으로 그린다. 그 앞은 `href` 가 있으면 `<a>` — **`<a>` 가 0건이면 반려**(FE §6-3 강제 항목) |
| **`DetailHeaderBar({ trail, backTo })`** | `backTo` 가 있으면 breadcrumb 왼쪽에 「←」 `<a href={backTo}>`. **`router.back()` 을 쓰지 않는다**(딥링크·새로고침에서 갈 곳이 없어도 목록으로). 목록 화면은 `backTo` 를 넘기지 않는다 |
| **헤더 순서** | ① breadcrumb 줄(+「←」) → ② **배지 줄**(좌: 유형 배지 · 프로젝트 칩 / 우: 그 화면의 액션 + 상태 칩 — **같은 높이**) → ③ **제목** → ④ 메타 한 줄. **제목이 배지 줄 위에 오면 반려** |
| **미리보기 CTA** | `scheduled`→「회의 입장」 · `recording`→「회의 입장」 · `generating`→「상세보기」 · `ended`→「상세보기」. 가는 곳은 **넷 다 `/meetings/detail?id=`** 이고 화면이 상태로 갈린다 |
| **패널 크기** | 패널 컨테이너가 **높이를 고정**하고(빈 상태 기준 = 본문 영역이 뷰포트 안) 본문이 `overflow-y-auto`. **`position:absolute` 금지**(FE 금지 목록 5). 1280~1439 는 좌 목록 400 고정 + 우 유동, ≥1440 은 좌 500 고정 + 우 유동 — **둘 다 화면 안** |
| **`density`** | `AgendaLineTree` **한 컴포넌트**가 `"default"`(상세) · `"compact"`(미리보기)를 가른다. **미리보기 전용 트리 컴포넌트를 만들면 반려**(FE §2 규칙 7). 가르는 것은 **글자 크기 · 여백 · 라벨 폭**뿐 — 구조 · 배지 · 펼침 규칙은 하나 |

## Execution

### Phase 1 — `Breadcrumb` 링크 · 「←」 (프론트 · 공용 부품)

- **Status**: TODO
- **설명**: MF-7. **공용 부품이라 한 번에 고친다** — 회의록만 고치면 업무·설정에 같은 것이 남는다.
- **작업**:
  - [ ] `Breadcrumb` trail 타입 변경 · 마지막 외 `<a>` · hover/focus
  - [ ] `DetailHeaderBar` 신설(같은 파일) · `TRAIL` 상수 갱신
  - [ ] 회의록 세 화면 · 업무 상세에 `backTo` 전달
  - [ ] `AppShell.test.tsx`
- **검증**:
  - [ ] 회의록 상세에서 breadcrumb 「홈」·「회의록」이 **링크**이고 마지막(제목)만 링크가 아니다. **`<a>` 개수 ≥ 1**(테스트 단언)
  - [ ] **키보드 `Tab` 으로 닿고 `Enter` 로 이동**한다. focus 표시가 보인다
  - [ ] 「←」를 누르면 **`/meetings/`** 로 간다. 새 탭에서 상세를 직접 열어도(히스토리 없음) 목록으로 간다 — `router.back()` 이 아니다(정적 검사: `router.back(` 0건)
  - [ ] **목록 화면(`/meetings/`)에는 「←」가 없다**
  - [ ] 업무 상세에도 같은 「←」·링크가 생겼고 **그 밖의 업무 화면 코드가 안 바뀌었다**(`git diff --stat features/tasks` 가 `backTo` 한 줄 수준)
  - [ ] `vitest` 전체 통과
- **완료 증거**: 미작성

### Phase 2 — 헤더 순서 세 화면 (프론트)

- **Status**: TODO
- **설명**: MF-8 · FE §6-3 「헤더 순서는 업무 헤더가 정본 — 회의록이 업무를 따라간다」.
- **작업**:
  - [ ] `MeetingScheduledPage` · `MeetingLiveView` · `MeetingClosedPage` 헤더 재배치
  - [ ] `MeetingMetaInline.MeetingMetaLine` 을 일시·소요만으로 · 유형/프로젝트는 배지 줄에서 `variant="badge"`
  - [ ] 각 화면 테스트
- **검증**:
  - [ ] 세 화면 모두 **① breadcrumb(+「←」) → ② 배지 줄 → ③ 제목 → ④ 메타 한 줄** 순서다(DOM 순서 단언)
  - [ ] 시작 전 배지 줄 우측에 `⋯`(삭제) + 「회의 시작」, 회의 중은 「일시정지」·「회의 종료」, 종료 후는 「삭제」 + 상태 칩 — **배지와 같은 높이**
  - [ ] 메타 한 줄에 **유형 · 프로젝트가 없다**(② 로 올라갔다). 종료 후는 「MM월 DD일 (요일) HH:MM – HH:MM · n분」
  - [ ] 배지를 눌러 유형 · 프로젝트를 **인라인으로 바꿀 수 있다**(기존 동작 유지 · `PATCH /api/meetings/{id}`)
  - [ ] 상세 드로어(`MeetingDetailDrawer`)의 헤더는 **이미 이 순서**라 안 바뀌었다(회귀 확인)
  - [ ] `vitest` 전체 통과
- **완료 증거**: 미작성

### Phase 3 — 미리보기 패널 CTA · 크기 · 밀도 (프론트)

- **Status**: TODO
- **설명**: MF-5 · 6 · FE §2 규칙 7. 실측에서 **회의를 고르면 패널이 오른쪽으로 넘어가 잘렸다**.
- **작업**:
  - [ ] `MeetingPreviewPanel` CTA 라벨 4행
  - [ ] 패널 높이 고정 + 본문 `overflow-y-auto` · `MeetingsScreen` 폭 규칙 정리
  - [ ] `AgendaLineTree` · `AgendaHeader` · `LineRow` 에 `density`
  - [ ] `MeetingPreviewPanel.test.tsx` · `AgendaLineTree.test.tsx`
- **검증**:
  - [ ] CTA 가 `scheduled`·`recording` 에서 「**회의 입장**」, `generating`·`ended` 에서 「**상세보기**」다(4행 전부 테스트)
  - [ ] 줄이 많은 회의를 골라도 **패널이 뷰포트 밖으로 나가지 않고** 패널 **안에서** 세로 스크롤한다. 빈 상태와 **바깥 크기가 같다**
  - [ ] 1280 · 1439 · 1440 · 1920 네 폭에서 패널이 화면 안에 있다(수동 확인 캡처)
  - [ ] 미리보기 트리 글자가 상세보다 **작고**, **같은 컴포넌트**를 쓴다(정적 검사: `features/meetings` 에 트리 컴포넌트가 `AgendaLineTree` **하나**)
  - [ ] `position:absolute` 로 패널을 배치하지 않는다(grep · FE 금지 목록 5)
  - [ ] 미리보기는 **읽기 전용**이다 — 줄 버튼 · 편집 · 근거 칩 클릭이 없다(기존 동작 유지)
  - [ ] `vitest` 전체 통과
- **완료 증거**: 미작성

## Pre-deploy Check

- [ ] **백엔드 변경 0** — API · 리비전 · env 없음. 프론트만 배포하면 된다
- [ ] `next build` 가 `out/` 을 만들고 동적 세그먼트가 없다(FE §11 8 — 라우트를 안 바꿨지만 링크가 늘어 확인)
- [ ] 업무 · 설정 화면의 breadcrumb 이 깨지지 않았는지 눈으로 한 번(공용 부품을 고쳤다)

## Rollback

- **프론트 단독 revert 로 끝난다** — 스키마 · API · env 가 없다
- 되돌리면 breadcrumb 이 다시 `<span>` 이 되고 「←」가 사라진다. **다른 WP 가 이 work 에 기대는 것이 없다**
- 부분 revert 시: Phase 3(패널)만 되돌려도 나머지가 돈다. Phase 1(공용 부품)을 되돌리면 **업무·설정의 링크도 함께 사라진다** — 그 사실을 알고 되돌린다

## Done Criteria

- [x] 모든 Phase 가 `DONE` 또는 `SUPERSEDED` 다
- [ ] **AC 대조** — SPEC-007 §6 「헤더가 배지 줄 → 제목 → 「MM월 DD일 (요일) HH:MM 시작」 순서이고, breadcrumb 「홈」·「회의록」이 링크이며 「←」로 목록에 간다」 · SPEC-008 §6 「헤더가 「←」 + breadcrumb → 배지 줄 → 제목 → 메타 순서다」 · SPEC-006 U-8 CTA 표 4행 · U-6 「패널이 화면 밖으로 나가지 않는다」 — **실측 캡처로** 완료 증거에 있다
- [ ] 정적 검사 4종(`Breadcrumb` 의 `<a>` ≥1 · `router.back(` 0 · 트리 컴포넌트 하나 · `position:absolute` 0)
- [x] `vitest` 전체 통과 · `Errors` 줄 0. **백엔드 `make test` 는 이 work 로 바뀌지 않는다**(그래도 한 번 돌려 확인)
- [x] `30-work/README.md` 갱신

> 2026-09-08 — 커밋 `5c72c25`. 검수 `orchestration/work/docs-v1/work014-review-report.md` FAIL 0 · WARN 2(네 폭 실측 · 「홈」 라우트 — 사용자 결정 대기). tsc 0 · vitest 360. **미완: 앱 창 네 폭 캡처는 사용자(아침) — jsdom 은 레이아웃을 계산하지 않아 테스트로 못 닫는다**. WORK-013 검수 W-2(파일 이름 둘)를 Phase 0 으로 닫음

## Open Issues

- **`PageHeader.tsx` 는 아직 없다.** FE §2 디렉토리 목록에 이름은 있지만 파일이 없고(grep 확인), `AppShell.tsx` 가 이미 breadcrumb 슬롯을 갖고 있다. **이 work 는 `AppShell` 안에 `DetailHeaderBar` 를 둔다** — 새 공용 파일을 세우는 것은 이 work 의 범위가 아니다. 파일로 떼어낼지는 나중에 화면이 더 늘 때 판단한다
- **업무 상세의 `backTo` 한 줄** — 「업무 화면은 안 고친다」의 예외로 볼 수 있으나, **공용 부품이 `backTo` 를 요구**하므로 넘기지 않으면 업무 상세에 「←」가 없다. MF-7 이 「공용 부품이라 한 번에 고친다」로 이미 답했다. 새 결정이 아니다
- **미리보기 패널의 한 줄 요약 바 카운트 다섯** → **WORK-012** 가 만든다. 이 work 는 밀도·크기만
- OQ-10 · 11 · 12 는 이 work 와 무관하다

## Related

- SPEC: SPEC-006 U-1 · U-4 · U-6 · U-8 · SPEC-007 U-1 Placement · §6 · SPEC-008 U-3 · U-4 · U-11
- Architecture: `frontend/README.md` §2 규칙 7 · §6-3 · §7-1 · §11 금지 목록 5 · §11 테스트 8
- Work: WORK-012 · WORK-013(같은 파일 — 머지 순서 012 → 013 → 014)
