# Handoff: 조직 화면 (Org screen)

> 출처: Claude Design 프로젝트 「SCAX」(8fa54d76-58d6-481a-aed9-743dff9d6c09) `design_handoff_org_screen/README.md` — 2026-09-07 DesignSync `get_file` 로 내려받은 사본. 원본이 SoT.

## Overview
한 명의 구성원을 **여섯 축**(계층 · 소속 · 직책 · 직급 · 직무 · 권한)으로 읽고, 그중 권한만이 실제 접근을 바꾼다는 것을 화면 구조로 드러내는 관리 화면. 3분할(조직 tree → 구성원 목록 → 6축 상세) + 하단 변경 기록, 소속 변경은 Drawer 로 처리한다.

## About the Design Files
`prototype/` 안의 파일은 **HTML 로 만든 디자인 레퍼런스**다. 그대로 배포할 프로덕션 코드가 아니다. 목표는 이 화면을 **ax-workspace-frontend(React) 코드베이스 안에서 기존 패턴으로 다시 구현**하는 것이다. 프로토타입은 이미 그 저장소에서 동기화된 SCAX 디자인 시스템(`styles.css` / `_ds_bundle.js`)만 쓰고 있으므로, 클래스 이름과 컴포넌트 이름은 코드베이스에 그대로 존재한다 — 새 CSS 를 쓸 일은 원칙적으로 없다.

- `prototype/OrgChart.dc.html` — 화면 전체(마크업 + 상태 로직)
- `prototype/ds-base.js` — 프로토타입이 DS 를 불러오는 방식(구현 시 불필요)

## Fidelity
**High-fidelity.** 색·타이포·간격·라운드는 모두 SCAX 시맨틱 토큰과 클래스에서 온 값이고 임의로 만든 값이 없다. 눈에 보이는 그대로 구현하면 된다. 단, 데이터는 전부 더미다(사람 이름, 사번, 인원수, 날짜).

## Screens / Views

### 1. 조직 (관리자 관점) — 기본
사용자: 조직 관리 권한 보유자. 사람을 찾아 6축을 확인하고, 소속·직책·권한을 변경한다.

레이아웃 (데스크톱 전용, 1280 하한 / 1920 기준):
- 셸: `.thesc-shell` = 사이드바 200 + 본문. 본문은 `.canvas` (max 1640 + 좌우 여백 40, 1440 에서 80, 1280 에서 48).
- `.canvas-topbar` (h38): breadcrumb `더에스씨 › 조직`.
- `.page-head`: h1 「조직」(28/Bold). 우측 `.page-head-actions` 에 권한 배지 1개.
  - 관리자 = `<span class="badge ai">조직 관리 권한 있음</span>`
  - 직원 = `<span class="badge outline">읽기 전용</span>`
- 3분할 그리드: `grid-template-columns: minmax(300px,392px) minmax(380px,1fr) minmax(440px,600px)`, `gap 24`, 높이 `calc(100vh - 300px)` / min 560. 1920 에서는 392 · 600 · 600 = 1640 이 된다.
- 각 패널: `border 1px var(--border-strong)` · `border-radius var(--radius-panel)` (16) · `background var(--surface)` · 내부 스크롤(`overflow:auto`), 헤더는 고정.
- 하단 `변경 기록`: `.surface-card` (padding 0, overflow hidden) + h44 헤더 + `.plain-table`.

패널 ① 조직 tree (392)
- 헤더: padding 16/24, `h3` 16px Bold 「조직 tree」 + 우측 `.t-meta` 12px 「읽기 전용」, 아래 검색 `input.search-input-box` (h34) placeholder 「사람 이름 검색」.
- 행: `display:flex; gap:9; padding:8px 12px; border-radius:8`. 구성 = chevron(`Icon` 12, 접힌 노드는 `chevron-right`) · 이름(`.t-item` 14 Bold) + 노드 종류(11px tertiary) · 카운트(`.t-meta.tabular` 12px 「직접 n · 전체 n」) · 리더 `avatar xs`.
- 자식 단계는 `padding-left:16`.
- 선택 행: `background var(--selected-bg)` + 이름 `color var(--action)`.

패널 ② 구성원 목록 (1fr)
- 헤더: 「제품기획팀 구성원」 + `.t-meta.tabular` 「직접 소속 12명」.
- 행 높이 **68**, `padding 0 20`, `border-bottom 1px var(--border-subtle)`, 커서 pointer.
  - 사번 40px `.t-meta.tabular` 12px → `avatar sm` → 이름(`.t-item`) + 소속 요약(12px tertiary, 「제품기획팀 (주) · 디자인팀 (겸직)」) → 직급 13px secondary → 행 메뉴 `button.btn.ghost.icon.h30` (관리자만).
- 선택 행: `background var(--surface-selected-row)`.
- hover 는 DS 기본(`--surface-sunken`)을 따른다.

패널 ③ 6축 상세 (600)
- 헤더 padding 12/24: `avatar lg` + 이름 20px Bold + 사번 12px tertiary(tabular), 아래 `badge neutral` 「재직」 · 「로그인 계정 있음」 + 11px tertiary 「재직과 계정은 다른 축입니다」.
- 축 행(5개): `display:flex; gap:12; padding:8px 0; border-bottom 1px var(--border-subtle)`. 왼쪽 라벨 36px 13px Bold tertiary(계층/소속/직책/직급/직무), 가운데 값 14px + 보조설명 12px tertiary, 오른쪽 `btn ghost h30` 「이력」, 변경 가능한 축(소속·직책)만 `btn h30` 「변경」 추가.
- 빈 값은 `EmptyValue` 컴포넌트(직책 행).
- 권한 행만 강조 박스: `background var(--selected-bg)`, `border-radius 8`, `padding 16`, 값 `.t-item`, 액션은 「이력」 + `btn primary h30` 「변경」. 그 아래 「회수된 권한」 목록(11px Bold tertiary 헤더 + 12px 행, 우측 기간 tabular) + `btn link h30` 「2건 더 보기」. 구분선 `1px var(--ai-border)`.

하단 변경 기록 (관리자만)
- `.plain-table` — th h44 / td h56. 컬럼: 시각 120(tabular) · 변경 280(`td.title-cell`, 최신 행만 `.t-item` Bold) · 축 80(`badge neutral` 조직/소속, `badge ai` 권한) · 사유(가변) · 기록자 120(`.end`).
- 빈 상태: `Empty variant="filter" title="이 세션에서 만든 변경이 없습니다"`.
- 한 임명이 조직/권한 두 줄로 남는다 — 같은 시각의 두 행이 그 예시다.

### 2. 조직 (직원 관점)
구조 동일, 차이만:
- 헤드 배지가 `badge outline` 「읽기 전용」
- 모든 「변경」 버튼 없음, 행 메뉴 없음
- 하단 변경 기록 섹션 전체 렌더 안 함

### 3. 소속 변경 — Drawer (840)
DS 규약: 편집·상세는 `Drawer`(840), 단일 결정은 `ConfirmModal`(600). 참고했던 원본이 모달로 그렸던 것을 **Drawer 로 옮겼다.**
- `Drawer label="소속 변경" kicker="유하람 · 2417 · 선임" title="소속 변경"`.
- 필드 순서: 현재 소속(읽기 전용 행, `border 1px var(--border-default)`, r8, 우측 `btn ghost h30` 「겸직 해제」) → 옮길 조직(`select`) · 적용일(`input`) 2열 → 소속 종류(`.segmented` 주소속/겸직) → 미리보기 → 딸린 권한 체크박스 → 사유(`textarea`).
- 미리보기 박스: `border 1px var(--accent)`, r8, padding 16. before(`--surface-sunken`) → `Icon arrow-right 16` → after(`--selected-bg`, `.t-item`). 그 아래 위험 문구 13px `var(--danger-hover)`, 그리고 「직급 · 직무 · 직책은 이 변경으로 바뀌지 않습니다.」 13px secondary.
- 체크박스: `Checkbox` (라벨은 **children**, `label` prop 없음) — 「새 조직의 표준 역할을 함께 부여」, 들여쓴 자식 「이전 소속에서 받은 역할을 함께 회수」 + `.field-help` 「주소속을 옮길 때만 고를 수 있습니다」.
- 푸터: 사유 미입력 시 `.t-meta` 「사유를 적어야 저장할 수 있습니다」 + `btn ghost h40` 취소 + `btn primary h40` 저장(disabled).

## Interactions & Behavior
- tree 노드 클릭 → 해당 조직 선택, 패널 ② 갈아끼움. chevron 클릭 → 접기/펼치기(선택과 별개).
- 구성원 행 클릭 → 패널 ③ 갈아끼움(선택 행 `--surface-selected-row`).
- 「변경」 → 해당 축의 Drawer. 소속 종류 = 겸직이면 「이전 소속 역할 회수」 체크박스 disabled + 강제 false.
- 사유(trim) 가 비면 저장 disabled.
- 주소속 교체처럼 되돌리기 어려운 저장은 `ConfirmModal`(destructive, 사유 필수)로 한 번 더 확인 — 프로토타입에는 미포함, 구현 시 붙일 것.
- 저장 성공 → `Toast tone="success"`, 실패 → `tone="error"`. **Drawer 위에 모달을 겹치지 않는다**(DS 규칙, ConfirmModal 은 Drawer 를 닫은 뒤).
- 로딩: 각 패널은 실제 행 수만큼 `Skeleton`. 실패: 패널 안 `Empty variant="error"`.
- 반응형: 1440 여백 80, 1280 여백 48, 1280 미만은 화면을 접고 `MinWidthNotice` — DS 기본 동작 그대로. (프로토타입에만 좁은 창 미리보기용 예외 CSS 가 있다. **구현에 옮기지 말 것.**)

## State Management
- `selectedOrgId`, `expandedOrgIds: Set`, `selectedMemberId`
- `drawer: { axis: 'affiliation' | 'position' | 'permission' | null }`
- Drawer 폼: `targetOrgId`, `effectiveDate`, `kind: 'primary' | 'concurrent'`, `grantStandardRole: boolean`(기본 true), `revokePrevRole: boolean`(기본 false, kind=primary 일 때만 활성), `reason: string`
- 파생: `saveBlocked = !reason.trim()`, `revokeDisabled = kind !== 'primary'`
- 데이터: 조직 트리(직접/전체 인원 카운트 포함), 조직별 구성원, 구성원 6축 상세 + 권한 이력(회수분 포함), 변경 기록 목록(페이징)

## Design Tokens
전부 SCAX 시맨틱 토큰. 하드코딩 금지, 아래는 확인용 값이다.
- 글자: `--text-primary` #1b1e25 · `--text-secondary` #5d6472 · `--text-tertiary` #6d7483 · `--text-disabled` #979faf · `--on-fill` #fff
- 보더: `--border-strong` #d4d8e0 (패널 외곽) · `--border-default` #e8eaf0 (내부 구분) · `--border-subtle` #eff1f6 (행)
- 면: `--surface` #fff · `--surface-sunken` #f6f7fa · `--surface-selected-row` #f8faff · `--selected-bg` #f1f2fe
- 액션/상태: `--action` #5467f7 · `--accent` #7181f8 · `--danger` #da3c2b · `--danger-hover` #c43222 · `--ai-border` #d5dafb
- 라운드: 패널 16 · 컨트롤/카드 8 · 배지 4 · 팝오버 12
- 간격 스케일: 4 · 8 · 12 · 16 · 20 · 24 · 32 · 48 (라벨–필드 7 예외)
- 타이포: Pretendard Variable, line-height 145%, letter-spacing −2%. h1 28 / 패널 h3 16 / 이름 20 / 항목 14 Bold(`.t-item`) / 메타 13(`.t-meta`) / 캡션 12 · 11
- 높이: 컨트롤 40 · 34 · 30 · 입력 38 · 리스트 행 68 · 테이블 헤드 44 / 행 56 · nav 36
- 그림자: 정의된 6개만(`--shadow-sm/md/lg/xl/drawer/ai`). 새 그림자 만들지 않음.

## Assets
이미지·아이콘 에셋 없음. 아이콘은 DS 의 `Icon` 26종만 사용(이 화면: `chevron-down`, `chevron-right`, `arrow-right`, `list`). 아바타는 `.avatar` 이니셜(실제 프로필 이미지가 들어오면 교체).

## Files
- `prototype/OrgChart.dc.html` — 화면 마크업 + 상태 로직 (디자인 시스템 프로젝트의 `templates/org-chart/OrgChart.dc.html` 사본)
- `prototype/ds-base.js` — 프로토타입용 DS 로더
- 구현 시 진실의 출처: 저장소의 `styles.css`(클래스·토큰)와 `components/general/<Name>` (Drawer · ConfirmModal · Checkbox · Empty · EmptyValue · Icon · Skeleton · Toast · Popover · MinWidthNotice)
