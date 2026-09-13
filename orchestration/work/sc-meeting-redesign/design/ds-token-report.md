# 구 DS 은퇴 매핑 리포트 — `TheSC AX Design System`

- **조사일** 2026-09-13 · **워커** designer(바퀴 0) · **범위** 조사만, 코드 수정 없음
- **새 DS** `TheSC AX Design System` `7e839512-977c-4142-b4b5-d992df566ffc` → 사본 `design/`
- **구 DS** `SCAX` `8fa54d76-58d6-481a-aed9-743dff9d6c09` → 코드 정본 `frontend/src/styles.css`(1613줄, read-only 로만 읽음)
- **앱** `/Users/kknaks/git/harness_works/ax-workspace/frontend`

> 이 리포트의 수치는 전부 파일에서 읽거나 세어 낸 것이다. 추측한 값은 없다.
> 판단이 갈리는 자리는 「열려 있음」으로 적고 `DS-gaps.md` 로 넘겼다.

---

## 요약 — 다섯 줄

1. **토큰 이름은 하나도 겹치지 않는다.** 새 569 : 구 65, 교집합 **0**. 변수만 놓고 보면 스코프 격리 없이 그냥 같이 실어도 된다.
2. **겹치는 것은 변수가 아니라 전역 element 규칙이다.** `a` · `body` · `button` · `*` 를 양쪽이 다 건드린다. 과도기 격리는 **여기에만** 필요하다.
3. **새 DS 의 「추출 부품」 190여 개는 갈아끼울 수 있는 부품이 아니다.** Figma variant 를 그대로 굳힌 정적 렌더러(`text1`·`icon1`·boolean)라 데이터도 콜백도 받지 않는다. 실제로 쓸 수 있는 것은 **의도적 추가분 7개**(`Icon` `DateField` `DatePicker` `TimeField` `AppShell`/`AppHeader`/`AppBody` `SideNav`)와 **핸드오프 JSX/CSS 의 프리미티브 24종**이다.
4. **`MeetingWorkspace.html` 은 목록과 상세를 합친 한 화면(4칸)이다.** 우리 `MeetingListPage` + `MeetingDetailPage` **둘 다**에 대응한다 — 화면 하나가 없어진다.
5. **구 `styles.css` 는 마지막 바퀴에 통째로 지운다.** 중간 바퀴에서는 덩어리 단위로 줄지 않는다 — 셸·부품·화면이 서로 물려 있어서, 화면 바퀴가 끝나기 전에는 어느 덩어리도 안전하게 빠지지 않는다(§11).

---
## §1 새 토큰 전수

| 파일 | 선언 수 | 고유 변수 이름 | 셀렉터별 선언 수 |
|---|---:|---:|---|
| `tokens/fig-tokens.css` | 504 | 372 | `:root` 372 · `:root[data-theme="dark"], .dark` 112 · `:root[data-mode="mobile"]` 2 · `:root[data-mode="tablet"]` 2 · `:root[data-theme="light"], .light` 2 · `:root[data-mode="small"]` 4 · `:root[data-mode="large"]` 4 · `:root[data-mode="xlarge"]` 4 · `:root[data-mode="desktop"]` 2 |
| `tokens/product.css` | 60 | 60 | `:root` 60 |
| `tokens/scax.css` | 103 | 103 | `:root` 103 |
| `tokens/typography.css` | 30 | 30 | `:root` 30 |
| `tokens/fig-typography.css` | 0 | 0 | — |
| `tokens/scrollbar.css` | 4 | 4 | `:root` 4 |
| `tokens/fonts.css` | 0 | 0 | — |
| **합계(고유)** | | **569** | |

### `tokens/fig-tokens.css` — `:root` 372개

```
  --accent-background-red-orange          --accent-background-violet              --accent-foreground-blue                --accent-foreground-cyan
  --accent-foreground-green               --accent-foreground-light-blue          --accent-foreground-lime                --accent-foreground-orange
  --accent-foreground-pink                --accent-foreground-purple              --accent-foreground-red                 --accent-foreground-violet
  --background-brand-default-2            --background-brand-default              --background-brand-hover                --background-brand-secondary
  --background-brand-tertiary-hover       --background-brand-tertiary             --background-danger-default             --background-danger-hover
  --background-danger-secondary-hover     --background-danger-secondary           --background-default-default-hover      --background-default-default
  --background-default-secondary-hover    --background-default-secondary          --background-default-tertiary-hover     --background-default-tertiary
  --background-disabled-default           --background-elevated-alternative       --background-elevated-normal            --background-neutral-tertiary-hover
  --background-neutral-tertiary           --background-normal-alternative         --background-normal-normal              --background-positive-default
  --background-positive-hover             --background-positive-secondary-hover   --background-positive-secondary         --background-transparent-alternative
  --background-transparent-normal         --background-warning-default            --background-warning-hover              --background-warning-secondary-hover
  --background-warning-secondary          --black-100                             --black-200                             --blue-45
  --blue-50                               --blue-60                               --blue-65                               --blue-80
  --blue-90                               --blue-95                               --blue-99                               --body-font-weight-regular
  --body-font-weight-strong               --body-size-medium                      --body-size-small                       --border-brand-default
  --border-brand-secondary                --border-brand-tertiary                 --border-danger-default                 --border-default-default
  --border-disabled-default               --border-disabled-secondary             --border-neutral-default                --border-neutral-secondary
  --border-width                          --brand-100-2                           --brand-100                             --brand-200
  --brand-300                             --brand-400                             --brand-500                             --brand-600
  --brand-800-2                           --brand-800                             --brand-900                             --brand-b-800
  --color-blue-blue-500                   --color-green-green-500                 --color-grey-grey-100                   --color-grey-grey-200
  --color-grey-grey-300                   --color-grey-grey-400                   --color-grey-grey-500                   --color-grey-grey-50
  --color-grey-grey-800                   --color-grey-grey-900                   --color-primary-primary-100             --color-primary-primary-300
  --color-primary-primary-400             --color-primary-primary-500             --color-primary-primary-50              --color-red-red-500
  --color-white-white-100                 --color-white-white-20                  --color-white-white-70                  --color-white-white-80
  --color-yellow-yellow-500               --common-0                              --common-100                            --cool-neutral-10-2
  --cool-neutral-10                       --cool-neutral-15                       --cool-neutral-17                       --cool-neutral-22
  --cool-neutral-23                       --cool-neutral-25                       --cool-neutral-40                       --cool-neutral-50
  --cool-neutral-5                        --cool-neutral-60                       --cool-neutral-70                       --cool-neutral-7
  --cool-neutral-90                       --cool-neutral-95-2                     --cool-neutral-95                       --cool-neutral-96
  --cool-neutral-97                       --cool-neutral-98                       --cool-neutral-99-2                     --cool-neutral-99
  --corner-radius-buttons-tiny            --cyan-40                               --cyan-50                               --depth-025
  --depth-0                               --depth-100                             --device-width                          --fill-alternative
  --fill-normal                           --fill-strong                           --gray-100                              --gray-200
  --gray-300                              --gray-400                              --gray-500                              --gray-600
  --gray-700                              --gray-800                              --gray-900-2                            --gray-900
  --green-100                             --green-200                             --green-300                             --green-40
  --green-500                             --green-50                              --green-600                             --green-60
  --green-700                             --green-800                             --green-900                             --heading-font-weight
  --heading-size-base                     --icon-brand-default                    --icon-brand-on-brand-tertiary          --icon-brand-on-brand
  --icon-color-icon-accent                --icon-color-icon-black                 --icon-color-icon-error                 --icon-color-icon-grey
  --icon-color-icon-info                  --icon-color-icon-light-grey            --icon-color-icon-success               --icon-color-icon-warning
  --icon-color-icon-white                 --icon-danger-on-danger-secondary       --icon-danger-on-danger                 --icon-default-default-2
  --icon-default-default                  --icon-default-secondary                --icon-default-tertiary                 --icon-disabled-on-disabled
  --icon-large                            --icon-medium                           --icon-positive-on-positive-secondary   --icon-positive-on-positive
  --icon-small                            --icon-warning-on-warning-secondary     --icon-warning-on-warning               --interaction-disable
  --interaction-inactive                  --inverse-background                    --inverse-label                         --label-alternative
  --label-assistive                       --label-disable                         --label-neutral                         --label-normal-2
  --label-normal                          --label-strong                          --leading-leading-tight                 --light-blue-40
  --light-blue-50                         --lime-37                               --lime-50                               --line-normal-alternative
  --line-normal-neutral                   --line-normal-normal                    --line-solid-alternative                --line-solid-neutral
  --line-solid-normal                     --neutral-30                            --neutral-50                            --neutral-60
  --neutral-70                            --neutral-95                            --neutral-99                            --opacity-0
  --opacity-12                            --opacity-16                            --opacity-22                            --opacity-28-2
  --opacity-28                            --opacity-43-2                          --opacity-43                            --opacity-5-2
  --opacity-52                            --opacity-5                             --opacity-61                            --opacity-74-2
  --opacity-74                            --opacity-8-2                           --opacity-88                            --opacity-8
  --orange-39                             --orange-50-2                           --orange-50                             --padding-horizontal
  --padding-lg                            --padding-vertical                      --padding-xs                            --pink-46
  --pink-60                               --primary-normal-2                      --primary-normal                        --purple-40
  --purple-60                             --radius-100                            --radius-200                            --radius-2
  --radius-400                            --radius-full                           --radius                                --red-100
  --red-200                               --red-300                               --red-40                                --red-500
  --red-50                                --red-600                               --red-60                                --red-700
  --red-800                               --red-900                               --red-orange-50                         --red-orange-60
  --scale-02                              --scale-03                              --scale-04                              --scale-05
  --scale-06                              --scale-07                              --scale-08                              --size-text-sm
  --size-text-xs                          --slate-1000                            --slate-100                             --slate-200
  --slate-300                             --slate-400                             --slate-500                             --slate-600
  --slate-900                             --space-050                             --space-100                             --space-1200
  --space-150                             --space-1600                            --space-200                             --space-300
  --space-400                             --space-600                             --space-800                             --space-negative-200
  --spacing-0                             --spacing-1                             --spacing-2                             --spacing-3
  --spacing-4                             --spacing-5                             --spacing-6                             --spacing-system-radius-lg
  --spacing-system-radius-md              --spacing-system-radius-sm              --spacing-system-radius-xs              --spacing-system-radius-xxs
  --spacing-system-spacing-lg             --spacing-system-spacing-md             --spacing-system-spacing-none           --spacing-system-spacing-sm
  --spacing-system-spacing-xl             --spacing-system-spacing-xs             --spacing-system-spacing-xxs            --static-black
  --static-white                          --status-negative                       --status-positive                       --stroke-border
  --subheading-font-weight                --subheading-size-medium                --subtitle-size-base                    --subtitle-size-small
  --surface-color-surface-white           --text-brand-default                    --text-brand-on-brand-tertiary          --text-brand-on-brand
  --text-brand-tertiary                   --text-color-text-accent                --text-color-text-disabled              --text-color-text-error
  --text-color-text-grey                  --text-color-text-info                  --text-color-text-primary-black         --text-color-text-primary-white
  --text-color-text-secondary-dark-grey   --text-color-text-success               --text-color-text-warning               --text-danger-default
  --text-danger-on-danger-secondary       --text-danger-on-danger                 --text-default-default                  --text-default-secondary
  --text-default-tertiary                 --text-disabled-default                 --text-disabled-on-disabled             --text-neutral-default
  --text-neutral-tertiary                 --text-positive-on-positive-secondary   --text-positive-on-positive             --text-warning-on-warning-secondary
  --text-warning-on-warning               --title-page-font-weight                --title-page-size-base                  --value-width-viewport-xl-2
  --value-width-viewport-xl               --violet-45                             --violet-50                             --violet-60
  --violet-70                             --violet-90                             --violet-95-2                           --violet-95
  --weight-bold                           --weight-font-normal                    --weight-regular                        --weight-semibold
  --white-1000-2                          --white-1000                            --white-400                             --white-500
  --yellow-1000                           --yellow-100                            --yellow-200                            --yellow-300
  --yellow-400                            --yellow-500                            --yellow-800                            --yellow-900
```

**스코프 `:root[data-theme="dark"], .dark` — 112개 재정의** (전부 위 `:root` 이름의 재선언, 새 이름 없음)

```
  --accent-background-red-orange          --accent-background-violet              --accent-foreground-blue                --accent-foreground-cyan
  --accent-foreground-green               --accent-foreground-light-blue          --accent-foreground-lime                --accent-foreground-orange
  --accent-foreground-pink                --accent-foreground-purple              --accent-foreground-red                 --accent-foreground-violet
  --background-brand-default-2            --background-brand-default              --background-brand-hover                --background-brand-secondary
  --background-brand-tertiary-hover       --background-brand-tertiary             --background-danger-default             --background-danger-hover
  --background-danger-secondary-hover     --background-danger-secondary           --background-default-default-hover      --background-default-default
  --background-default-secondary-hover    --background-default-secondary          --background-default-tertiary-hover     --background-default-tertiary
  --background-disabled-default           --background-elevated-alternative       --background-elevated-normal            --background-neutral-tertiary-hover
  --background-neutral-tertiary           --background-normal-alternative         --background-normal-normal              --background-positive-default
  --background-positive-hover             --background-positive-secondary-hover   --background-positive-secondary         --background-transparent-alternative
  --background-transparent-normal         --background-warning-default            --background-warning-hover              --background-warning-secondary-hover
  --background-warning-secondary          --border-brand-default                  --border-brand-secondary                --border-brand-tertiary
  --border-danger-default                 --border-default-default                --border-disabled-default               --border-disabled-secondary
  --border-neutral-default                --border-neutral-secondary              --fill-alternative                      --fill-normal
  --fill-strong                           --icon-brand-default                    --icon-brand-on-brand-tertiary          --icon-brand-on-brand
  --icon-danger-on-danger-secondary       --icon-danger-on-danger                 --icon-default-default-2                --icon-default-default
  --icon-default-secondary                --icon-default-tertiary                 --icon-disabled-on-disabled             --icon-positive-on-positive-secondary
  --icon-positive-on-positive             --icon-warning-on-warning-secondary     --icon-warning-on-warning               --interaction-disable
  --interaction-inactive                  --inverse-background                    --inverse-label                         --label-alternative
  --label-assistive                       --label-disable                         --label-neutral                         --label-normal-2
  --label-normal                          --label-strong                          --line-normal-alternative               --line-normal-neutral
  --line-normal-normal                    --line-solid-alternative                --line-solid-neutral                    --line-solid-normal
  --primary-normal-2                      --primary-normal                        --static-black                          --static-white
  --status-negative                       --status-positive                       --text-brand-default                    --text-brand-on-brand-tertiary
  --text-brand-on-brand                   --text-brand-tertiary                   --text-danger-default                   --text-danger-on-danger-secondary
  --text-danger-on-danger                 --text-default-default                  --text-default-secondary                --text-default-tertiary
  --text-disabled-default                 --text-disabled-on-disabled             --text-neutral-default                  --text-neutral-tertiary
  --text-positive-on-positive-secondary   --text-positive-on-positive             --text-warning-on-warning-secondary     --text-warning-on-warning
```

**스코프 `:root[data-mode="mobile"]` — 2개 재정의** (전부 위 `:root` 이름의 재선언, 새 이름 없음)

```
  --border-width                          --device-width
```

**스코프 `:root[data-mode="tablet"]` — 2개 재정의** (전부 위 `:root` 이름의 재선언, 새 이름 없음)

```
  --border-width                          --device-width
```

**스코프 `:root[data-theme="light"], .light` — 2개 재정의** (전부 위 `:root` 이름의 재선언, 새 이름 없음)

```
  --background-brand-default-2            --icon-default-default-2
```

**스코프 `:root[data-mode="small"]` — 4개 재정의** (전부 위 `:root` 이름의 재선언, 새 이름 없음)

```
  --padding-horizontal                    --padding-vertical                      --radius-2                              --radius
```

**스코프 `:root[data-mode="large"]` — 4개 재정의** (전부 위 `:root` 이름의 재선언, 새 이름 없음)

```
  --padding-horizontal                    --padding-vertical                      --radius-2                              --radius
```

**스코프 `:root[data-mode="xlarge"]` — 4개 재정의** (전부 위 `:root` 이름의 재선언, 새 이름 없음)

```
  --padding-horizontal                    --padding-vertical                      --radius-2                              --radius
```

**스코프 `:root[data-mode="desktop"]` — 2개 재정의** (전부 위 `:root` 이름의 재선언, 새 이름 없음)

```
  --value-width-viewport-xl-2             --value-width-viewport-xl
```

### `tokens/product.css` — `:root` 60개

```
  --ax-accent                             --ax-accent-strong                      --ax-accent-soft                        --ax-accent-05
  --ax-accent-08                          --ax-accent-20                          --ax-agent-gradient                     --ax-agent-glow-blur
  --ax-ink-strong                         --ax-ink                                --ax-ink-neutral                        --ax-ink-alt
  --ax-ink-assistive                      --ax-ink-disable                        --ax-ink-inverse                        --ax-ink-nav-idle
  --ax-ink-nav-active                     --ax-surface                            --ax-surface-alt                        --ax-surface-nav
  --ax-surface-nav-active                 --ax-surface-nav-hover                  --ax-surface-inverse                    --ax-line-weak
  --ax-line                               --ax-line-strong                        --ax-fill-weak                          --ax-fill
  --ax-fill-strong                        --ax-danger                             --ax-positive                           --ax-info
  --ax-r-xs                               --ax-r-sm                               --ax-r-md                               --ax-r-lg
  --ax-r-xl                               --ax-r-2xl                              --ax-r-bubble                           --ax-r-pill
  --ax-shadow-card                        --ax-shadow-raised                      --ax-shadow-panel                       --ax-shadow-rail
  --ax-ring                               --ax-ring-weak                          --ax-interaction-light-hover            --ax-interaction-light-focus
  --ax-interaction-light-press            --ax-interaction-normal-hover           --ax-interaction-normal-focus           --ax-interaction-normal-press
  --ax-interaction-strong-hover           --ax-interaction-strong-focus           --ax-interaction-strong-press           --ax-nav-max
  --ax-nav-min                            --ax-header-h                           --ax-inbox-w                            --ax-calendar-w
```

### `tokens/scax.css` — `:root` 103개

```
  --scax-color-accent                     --scax-color-accent-strong              --scax-color-accent-soft                --scax-color-accent-05
  --scax-color-accent-08                  --scax-color-accent-20                  --scax-gradient-agent                   --scax-agent-glow-blur
  --scax-color-ink-strong                 --scax-color-ink                        --scax-color-ink-neutral                --scax-color-ink-alt
  --scax-color-ink-assistive              --scax-color-ink-disabled               --scax-color-ink-inverse                --scax-color-ink-nav-idle
  --scax-color-ink-nav-active             --scax-color-surface                    --scax-color-surface-alt                --scax-color-surface-nav
  --scax-color-surface-nav-active         --scax-color-surface-nav-hover          --scax-color-surface-inverse            --scax-color-line-weak
  --scax-color-line                       --scax-color-line-strong                --scax-color-fill-weak                  --scax-color-fill
  --scax-color-fill-strong                --scax-color-danger                     --scax-color-danger-soft                --scax-color-positive
  --scax-color-info                       --scax-color-warning                    --scax-space-050                        --scax-space-100
  --scax-space-150                        --scax-space-200                        --scax-space-250                        --scax-space-300
  --scax-space-400                        --scax-space-500                        --scax-space-600                        --scax-space-800
  --scax-space-1200                       --scax-radius-xs                        --scax-radius-sm                        --scax-radius-md
  --scax-radius-lg                        --scax-radius-xl                        --scax-radius-2xl                       --scax-radius-bubble
  --scax-radius-pill                      --scax-font-ui                          --scax-font-display                     --scax-fw-regular
  --scax-fw-medium                        --scax-fw-semibold                      --scax-fw-bold                          --scax-text-caption2-size
  --scax-text-caption2-lh                 --scax-text-caption2-ls                 --scax-text-caption1-size               --scax-text-caption1-lh
  --scax-text-caption1-ls                 --scax-text-label2-size                 --scax-text-label2-lh                   --scax-text-label2-ls
  --scax-text-label1-size                 --scax-text-label1-lh                   --scax-text-label1-ls                   --scax-text-body1-size
  --scax-text-body1-lh                    --scax-text-body1-ls                    --scax-text-headline-size               --scax-text-headline-lh
  --scax-text-headline-ls                 --scax-text-title-size                  --scax-text-title-lh                    --scax-text-title-ls
  --scax-shadow-card                      --scax-shadow-raised                    --scax-shadow-panel                     --scax-shadow-rail
  --scax-ring                             --scax-ring-weak                        --scax-state-hover                      --scax-state-focus
  --scax-state-press                      --scax-nav-width                        --scax-nav-width-collapsed              --scax-header-height
  --scax-rail-left-width                  --scax-rail-right-width                 --scax-control-height-sm                --scax-control-height-md
  --scax-control-height-lg                --scax-row-height                       --scax-content-min-width                --scax-table-min-width
  --scax-focus-ring                       --scax-duration-fast                    --scax-easing
```

### `tokens/typography.css` — `:root` 30개

```
  --font-ui                               --font-display                          --fw-regular                            --fw-medium
  --fw-semibold                           --fw-bold                               --t-caption2-size                       --t-caption2-lh
  --t-caption2-ls                         --t-caption1-size                       --t-caption1-lh                         --t-caption1-ls
  --t-label2-size                         --t-label2-lh                           --t-label2-ls                           --t-label1-size
  --t-label1-lh                           --t-label1-ls                           --t-body1-size                          --t-body1-lh
  --t-body1-ls                            --t-headline-size                       --t-headline-lh                         --t-headline-ls
  --t-title-size                          --t-title-lh                            --t-title-ls                            --t-display-size
  --t-display-lh                          --t-display-ls
```

### `tokens/fig-typography.css` — 변수 0개

### `tokens/scrollbar.css` — `:root` 4개

```
  --ax-scrollbar-size                     --ax-scrollbar-thumb                    --ax-scrollbar-thumb-hover              --ax-scrollbar-track
```

### `tokens/fonts.css` — 변수 0개

## §2 구 토큰 전수 — `frontend/src/styles.css`

`:root` 변수 **65개**. (read-only 로만 읽었다.)

| 이름 | 값 |
|---|---|
| `--text-primary` | `#1b1e25` |
| `--text-secondary` | `#5d6472` |
| `--text-tertiary` | `#6d7483` |
| `--text-disabled` | `#979faf` |
| `--border-strong` | `#d4d8e0` |
| `--border-default` | `#e8eaf0` |
| `--border-subtle` | `#eff1f6` |
| `--surface` | `#fff` |
| `--surface-sunken` | `#f6f7fa` |
| `--surface-selected-row` | `#f8faff` |
| `--selected-bg` | `#f1f2fe` |
| `--accent` | `#7181f8` |
| `--action` | `#5467f7` |
| `--action-hover` | `#374df6` |
| `--action-active` | `#1e37f4` |
| `--progress-accent` | `#33aaff` |
| `--progress-text` | `#0079d0` |
| `--progress-tint` | `#eaf4ff` |
| `--danger-accent` | `#e2685b` |
| `--danger` | `#da3c2b` |
| `--danger-hover` | `#c43222` |
| `--danger-tint` | `#fdf0ee` |
| `--status-neutral-tint` | `#f4f5f7` |
| `--shadow-sm` | `0 1px 2px rgba(16, 24, 40, 0.04)` |
| `--shadow-md` | `0 1px 2px rgba(16, 24, 40, 0.04), 0 8px 20px rgba(16, 24, 40, 0.05)` |
| `--shadow-lg` | `0 1px 2px rgba(16, 24, 40, 0.04), 0 12px 30px rgba(16, 24, 40, 0.06)` |
| `--shadow-xl` | `0 16px 40px rgba(0, 0, 0, 0.16)` |
| `--shadow-drawer` | `-24px 0 60px rgba(0, 0, 0, 0.18)` |
| `--shadow-ai` | `0 1px 2px rgba(16, 24, 40, 0.04), 0 10px 24px rgba(89, 105, 214, 0.1)` |
| `--radius-card` | `8px` |
| `--radius-panel` | `16px` |
| `--radius-control` | `8px` |
| `--radius-chip` | `4px` |
| `--radius-popover` | `12px` |
| `--popover-current` | `#f4f5ff` |
| `--graph-node-person` | `#7181f8` |
| `--graph-node-team` | `#7181f8` |
| `--graph-node-project` | `#5a63c9` |
| `--graph-node-work-request` | `#9a78df` |
| `--graph-node-task` | `#33aaff` |
| `--graph-node-material` | `#4da885` |
| `--graph-node-meeting` | `#d89038` |
| `--graph-node-report` | `#d96f8b` |
| `--graph-node-fallback` | `#868e96` |
| `--graph-node-dim` | `#d9dde5` |
| `--graph-edge` | `#c3c9d4` |
| `--graph-edge-dim` | `#edf0f4` |
| `--graph-edge-active` | `#6676f4` |
| `--graph-label` | `#343944` |
| `--graph-edge-label` | `#747d8d` |
| `--ai-border` | `#d5dafb` |
| `--ai-border-hover` | `#c3cbfb` |
| `--ai-border-active` | `#a6b0f7` |
| `--ai-text` | `#4b52a8` |
| `--ai-text-active` | `#3a4194` |
| `--ai-bg-hover` | `#e9ecfd` |
| `--ai-bg-active` | `#dde2fc` |
| `--danger-active` | `#ae2c1e` |
| `--hero-sky-left` | `#dde7ff` |
| `--hero-violet` | `#d6dafb` |
| `--hero-sky-right` | `#d7e2ff` |
| `--ink-hover` | `#2b303a` |
| `--on-fill` | `#fff` |
| `--warning-surface` | `#fff4e5` |
| `--warning-text` | `#8a5300` |

`:root` 밖에서 선언되는 변수 **6개** — 지역 변수라 전역 충돌 대상이 아니다.

| 이름 | 선언 셀렉터 |
|---|---|
| `--columns` | `.work-table` |
| `--task-card-border` | `.action-task-card` |
| `--task-card-edit-border` | `.action-task-card` |
| `--task-card-title` | `.action-task-card` |
| `--task-card-copy` | `.action-task-card` |
| `--task-card-meta` | `.action-task-card` |

## §3 충돌표

비교 기준: 새 DS 의 `:root` 선언 이름(569) ↔ 구 `styles.css` 의 `:root` 선언 이름(65).

| 구획 | 건수 | 내용 |
|---|---:|---|
| 이름 같고 값 같음 | **0** | 없음 |
| 이름 같고 값 다름 | **0** | 없음 |
| 새 것만 | **569** | §1 의 전체 목록 |
| 구 것만 | **65** | §2 의 전체 목록 (+ `:root` 밖 6개) |

**교집합이 공집합이다.** 두 묶음은 접두사부터 갈린다.

| | 접두사 |
|---|---|
| 새 DS | `--accent-*` `--background-*` `--border-*` `--brand-*` `--color-*` `--common-*` `--cool-neutral-*` `--fill-*` `--gray-*` `--icon-*` `--label-*` `--line-*` `--radius-*` `--scale-*` `--slate-*` `--space-*` `--spacing-*` `--text-*` `--weight-*` … 그리고 제품 별칭 `--ax-*`(60) · `--scax-*`(103) · 타입 `--t-*`/`--fw-*`/`--font-*`(30) |
| 구 DS | `--accent` `--action*` `--ai-*` `--border-*` `--danger*` `--graph-*` `--hero-*` `--ink-hover` `--on-fill` `--popover-current` `--progress-*` `--radius-*` `--selected-bg` `--shadow-*` `--status-neutral-tint` `--surface*` `--text-*` `--warning-*` |

접두사가 겹쳐 보이는 셋(`--border-*` · `--radius-*` · `--text-*` · `--shadow-*`)도 **전체 이름은 하나도 안 겹친다**:

| 접두사 | 구 이름 | 새 이름 | 겹침 |
|---|---|---|---|
| `--border-` | `--border-default` `--border-strong` `--border-subtle` | `--border-brand-default` `--border-brand-secondary` `--border-brand-tertiary` `--border-danger-default` `--border-default-default` `--border-disabled-default` `--border-disabled-secondary` `--border-neutral-default` `--border-neutral-secondary` `--border-width` | 0 |
| `--radius-` | `--radius-card` `--radius-chip` `--radius-control` `--radius-panel` `--radius-popover` | `--radius` `--radius-2` `--radius-100` `--radius-200` `--radius-400` `--radius-full` | 0 |
| `--text-` | `--text-disabled` `--text-primary` `--text-secondary` `--text-tertiary` | `--text-brand-*` `--text-color-text-*` `--text-danger-*` `--text-default-*` `--text-disabled-default` `--text-disabled-on-disabled` `--text-neutral-*` `--text-positive-*` `--text-warning-*` | 0 |
| `--shadow-` | `--shadow-ai` `--shadow-drawer` `--shadow-lg` `--shadow-md` `--shadow-sm` `--shadow-xl` | (새 것은 `--ax-shadow-*` / `--scax-shadow-*` 로 접두사가 다르다) | 0 |

**「이름 같고 값 다름」이 0건이므로 전건 나열은 비어 있다.**

### 3-1 변수는 안 겹치지만 **전역 element 규칙은 겹친다**

이것이 실제 충돌 지점이다. 변수만 세면 안전해 보여서 놓치기 쉽다.

| 셀렉터 | 구 `styles.css` | 새 DS | 결과 |
|---|---|---|---|
| `a` | `color: var(--action)` `text-decoration:none` (85~92줄대) | `tokens/product.css` `color:var(--ax-accent)` · `components/shell/shell.css` `color:var(--scax-color-accent)` | **정면 충돌** — 나중에 실린 쪽이 이긴다 |
| `a:hover` | (구에는 없음) | product.css · shell.css 둘 다 `text-decoration:underline` | 새 것이 링크 hover 를 바꾼다 |
| `body` | `margin:0; min-width:320px` | shell.css `background` `color` `font-family` `font-size` `line-height` `letter-spacing` | **정면 충돌** — 앱 전체 바탕·글꼴이 바뀐다 |
| `button` | `cursor:pointer; border:0; background:transparent` | shell.css `font:inherit; color:inherit; margin:0` | 부분 충돌 |
| `button, input, select, textarea` | `font:inherit` 등 | (새 것은 `button` 만) | 구 것이 더 넓다 |
| `h1,h2,h3,h4,p` | (구에는 리셋 없음) | shell.css `margin:0; font-size:inherit; font-weight:inherit` | **새 것이 앱 전체 제목 크기를 죽인다** |
| `*` | `box-sizing:border-box` | shell.css `box-sizing` (동일) + `tokens/scrollbar.css` `scrollbar-width:none` / `::-webkit-scrollbar{width:0}` | box-sizing 은 같은 값 · **스크롤바는 새 것이 앱 전체에서 막대를 없앤다** |

클래스 이름은 안 겹친다 — 구 `styles.css` 에도 `.ax-*` 가 87종 있지만(`.ax-rail` `.ax-turn` `.ax-evidence` … AI 어시스턴트 레일 어휘), 새 DS 의 `.ax-*` 는 `ax-caption1/caption2/label1/label2/label1-strong/body1/headline/headline-strong/title/display` + `ax-scroll-hover/always/gutter` 13종뿐이고 **교집합 0** 이다. 다만 접두사를 공유하므로 다음 바퀴 워커가 새로 `.ax-` 이름을 만들면 그때 부딪친다 — 새 것은 전부 `.scax-` 로 쓴다.

## §4 판정 — 과도기 공존 방식 (한 줄)

> **변수는 스코프 격리가 필요 없다(이름 교집합 0). 대신 새 DS 의 전역 element 규칙 6줄(`a` `a:hover` `body` `button` `h1~h4,p` `*`+스크롤바)만 스코프 안으로 접어 넣으면 두 묶음을 그대로 같이 실을 수 있고, 마지막 바퀴에서 구 `styles.css` 를 지울 때 그 접은 것을 다시 펴면 끝난다.**

구체적으로 과도기 동안:

- `tokens/*.css` 7벌은 **그대로 전역에 싣는다** — 569개 변수가 `:root` 에 얹혀도 구 65개를 건드리지 않는다. `:root[data-theme="dark"]`·`[data-mode="*"]` 재정의도 우리가 그 속성을 안 쓰므로 무해하다.
- `components/shell/shell.css` 는 **element 리셋 블록(맨 위 7줄)을 잘라내고** 싣는다. `.scax-*` 클래스 규칙만 남기면 충돌이 0 이 된다.
- `tokens/product.css` 의 `a`/`a:hover` 2줄도 같이 잘라낸다.
- `tokens/scrollbar.css` 의 `*{scrollbar-width:none}` 은 **마지막 바퀴까지 싣지 않는다** — 구 화면은 스크롤바가 보이는 전제로 그려져 있다. 앱은 이미 `.scroll-hidden` 으로 필요한 자리만 숨긴다.
- 끝 상태(마지막 바퀴)에서는 잘라 둔 리셋을 되살리고 `styles.css` 를 지운다.

**대안(스코프 격리)은 필요 없고, 권하지도 않는다.** 서브트리에 변수를 재정의하는 방식은 겹치는 이름이 있을 때 쓰는 수단인데 여기서는 겹치는 이름이 없다. 굳이 넣으면 캐스케이드만 복잡해진다.


## §5 폰트

| | 값 |
|---|---|
| 새 DS 가 요구하는 것 | `tokens/fonts.css` 의 `@font-face` 2벌 — **`Pretendard JP`**(`--font-ui`, UI 전체) · **`Pretendard`**(`--font-display`, 150px 표지용) |
| 불러오는 곳 | **원격 URL** — `https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/…` (JP: `packages/pretendard-jp/dist/web/variable/woff2/PretendardJPVariable.woff2` · 일반: `dist/web/variable/woff2/PretendardVariable.woff2`) |
| 프로젝트 안에 파일이 있나 | **없다.** `_ds_manifest.json` 의 `fonts[]` 가 `"files": [], "remoteSrc": true` 로 명시한다. 내려받은 사본 어디에도 `.woff2` 가 없다 |
| 앱이 지금 쓰는 것 | `frontend/src/styles.css:78` `font-family: "Pretendard Variable", Pretendard, -apple-system, …` — **시스템 설치 폰트에 기댄다** |
| 앱에 파일이 있나 | 있다 — `.design-sync/fonts/PretendardVariable.woff2` (2,057,688 B). 다만 이건 **claude.ai/design 렌더 전용**이라고 그 CSS 주석이 밝히고, 앱 번들은 이 파일을 싣지 않는다 |

**판정 — 두 개가 열려 있다.**

1. **글꼴 가족이 다르다.** 앱은 `Pretendard Variable`/`Pretendard`, 새 DS 는 `Pretendard JP`. JP 는 일본어 자형을 포함한 별개 빌드다. 그대로 옮기면 한글 자형이 바뀐다(폭·획 굵기가 미세하게 다르다). → `DS-gaps.md` #G-01
2. **파일이 프로젝트 안에 없다.** 그대로 쓰면 앱이 jsDelivr CDN 에 런타임 의존하게 된다. 사내 망·오프라인에서 폰트가 깨진다. 우리는 이미 `PretendardVariable.woff2` 를 갖고 있으므로 **JP 를 쓰기로 정하면 JP woff2 를 따로 받아 `frontend/public` 또는 `src/assets` 에 두고 `@font-face src` 를 로컬로 바꿔야 한다.** → `DS-gaps.md` #G-02

이 둘은 워커가 정할 것이 아니다. 결정 전까지 바퀴 1 은 `tokens/fonts.css` 를 **싣지 않고** `--font-ui`/`--font-display` 만 우리 기존 스택으로 덮어 쓰는 것을 기본값으로 둔다(§11 바퀴 1).

## §6 셸 — 무엇을 감싸고 어떤 어휘를 쓰나

`handoff/shell/js/scax-ui.jsx`(9,629 B) · `handoff/shell/js/nav.js`(907 B) · `components/shell/AppShell.jsx`(1,550 B) · `components/shell/SideNav.jsx`(2,655 B) · `components/shell/shell.css`(10,240 B) 다섯이 한 벌이다. **`AppShell.jsx` 가 `AppShell`·`AppHeader`·`AppBody` 셋을, `SideNav.jsx` 가 `SideNav` 하나를 내보낸다** — `_ds_manifest.json` 의 `shell` 그룹이 4개인 이유다. `AppShell` 은 `nav` 슬롯 하나와 children 을 받아 `.scax-app-shell`(가로 flex, `min-width:1542px`, `height:100vh`, `overflow:hidden`) 안에 내비와 `.scax-app-main` 을 세운다. `AppHeader` 는 `breadcrumb`(배열)·`title`·`actions` 를 받아 60px 고정 높이의 `.scax-page-header` 를 그리고, `AppBody` 는 `railLeft`·`railRight`·children 을 받아 `.scax-page-body` 를 좌 레일 380 / 본문 `min-width:640` / 우 레일 342 세 칸으로 가른다. 레일을 안 넘기면 그 칸이 아예 렌더되지 않아서, 레일 없는 화면은 본문만 남는다. `SideNav` 는 `user`·`items`·`utilityItems`·`activeId`·`collapsed`·`onCollapse`·`logo`·`version` 을 받고, `href` 가 있는 항목만 이동하며(없으면 `aria-disabled="true"`), 접으면 180→65px 로 줄고 라벨이 `display:none` 되며 hover 시 `::after{content:attr(data-label)}` 툴팁이 뜬다. 목록 정본은 `nav.js` 가 `window.NAV_PRIMARY`(알림·설정) / `window.NAV_MAIN`(홈·업무·캘린더·회의·채팅·수신함·진행 현황·자료) 로 물려 준다. `scax-ui.jsx` 는 이 넷을 `window.SCAX_DS` 에서 꺼내 쓰고, 그 위에 **화면이 실제로 쓰는 프리미티브 20종**(`Icon` `Button` `ButtonGroup` `IconButton` `Badge` `Popover` `Select` `SegmentedControl` `Tabs` `Chip` `GutterList` `Empty` `StatusNote` `Skeleton` `AgentBubble` + dev 전용 `StateSwitch`)을 정의해 `window` 로 넘긴다. 스타일은 전부 클래스이고 인라인 스타일·유틸리티 클래스가 없다.

**셸이 쓰는 클래스 어휘** (`components/shell/shell.css`):

```
.scax-app-shell  .scax-app-main
.scax-side-nav   .scax-side-nav--collapsed
  .scax-side-nav__identity  __avatar  __who  __name  __role  __collapse
  .scax-side-nav__group  __divider  __spacer  __footer  __logo  __version
.scax-nav-item   .scax-nav-item--active   .scax-nav-item[aria-disabled="true"]
  .scax-nav-item__glyph  __dot  __label
.scax-page-header  .scax-page-header__lead  __title  __actions
.scax-breadcrumb   .scax-breadcrumb__sep  .scax-breadcrumb__item  __item--current
.scax-page-body    .scax-page-body__rail  __rail--left  __rail--right  __content
.scax-state-switch (dev 전용)  __label  __btn  __btn--on
```

셸 CSS 는 맨 위 7줄이 **전역 element 리셋**(`*,*::before,*::after` · `html,body` · `body` · `button` · `h1,h2,h3,h4,p` · `a` · `a:hover`)이다 — §3-1·§4 에서 잘라내라고 한 그 블록이다.

## §7 화면 2장 ↔ 번들 대조표

### `MyWork.html`

| 종류 | 불러오는 것 |
|---|---|
| CSS | `./styles.css`(= tokens 7벌 + `components/shell/shell.css` + kit-assets/misc `fig-assets.css`) · `./handoff/my-work/css/components.css` |
| 번들 | `./_ds_bundle.js` → `window.SCAX_DS = window.TheSCAXDesignSystem_7e8395` |
| 번들에서 실제로 꺼내 쓰는 부품 | `Icon` · `AppShell` · `SideNav` · `AppHeader` · `AppBody` — **5개뿐** (`scax-ui.jsx` 의 `const { AppShell, SideNav: DSSideNav, AppHeader, AppBody } = window.SCAX_DS;` 와 `Icon` 래퍼). 나머지 196개 부품은 이 화면이 건드리지 않는다 |
| 핸드오프 JS | `handoff/shell/js/nav.js` · `handoff/my-work/js/data.js` · `handoff/shell/js/scax-ui.jsx` · `handoff/shell/js/work-modal.jsx` · `handoff/my-work/js/my-work.v2.jsx` |

### `MeetingWorkspace.html`

| 종류 | 불러오는 것 |
|---|---|
| CSS | `./styles.css` · `./handoff/my-work/css/components.css` · `./handoff/meetings/css/meetings.css` · `./handoff/meetings/css/workspace.css` |
| 번들 | 같음 — `Icon` · `AppShell` · `SideNav` · `AppHeader` · `AppBody` 5개 |
| 핸드오프 JS | `nav.js` · `handoff/meetings/js/data.js` · `handoff/meetings/js/workspace-data.js` · `scax-ui.jsx` · `work-modal.jsx` · `handoff/meetings/js/workspace.v1.jsx` |

### 판정 — `MeetingWorkspace.html` 은 무엇인가

> **셋이 한 화면에 합쳐진 것이다.** 목록·상세·진행 중이 각각 별개 화면이 아니라, **4칸 한 화면**의 서로 다른 칸이거나 같은 칸의 서로 다른 상태다.

근거는 파일 첫 줄이 직접 말한다 — `workspace.v1.jsx:1` 「`「회의」 한 화면 (4칸) — 사이드바 | 회의 목록 | 회의 상세 | 첨부·스크립트. 업무 탭과 같은 틀이다. 목록과 상세를 페이지로 나누지 않는다.`」 그리고 구조가 그대로다:

| 칸 | 컴포넌트 | 폭 |
|---|---|---|
| 1 사이드바 | `SideNav` | 180 / 65 |
| 2 회의 목록 | `MeetingListRail` (`AppBody railLeft`) | 380 — 집중 모드(`focus`)면 `null` 이 되어 사라진다 |
| 3 회의 상세 | `DetailPanel` (`AppBody` children) | min 640 |
| 4 첨부·스크립트 | `SideRail` (`AppBody railRight`) | 342 |

「진행 중」은 네 번째 화면이 아니라 **3칸의 상태**다 — `DetailPanel` 이 `row.status` 로 `scheduled`/`in_progress`/`summarizing`/`done`/`failed`/`cancelled` 여섯을 한 컴포넌트 안에서 갈라 그리고, 「회의 시작」을 누르면 그 자리에서 `scheduled → in_progress` 로 넘어가며 `.scax-live-bar` 가 위에 붙는다.

**우리 앱 대응 — `MeetingListPage` 와 `MeetingDetailPage` 둘 다.**

| 시안 | 우리 |
|---|---|
| 2칸 `MeetingListRail` | `src/meetings/MeetingListPage.tsx` 의 왼쪽 `.meeting-panel`(목록) |
| 3칸 `DetailPanel` | `src/meetings/MeetingDetailPage.tsx` 의 왼쪽 `.meeting-panel`(회의록) + 페이지 머리 |
| 4칸 `SideRail` | `MeetingDetailPage.tsx:1003` 의 오른쪽 `.meeting-panel`(자료와 스크립트) |
| (없음) | `MeetingListPage.tsx:335~369` 의 오른쪽 미리보기 패널 — 시안에서 **사라진다** |

즉 **우리 화면 2장이 시안에서 1장으로 합쳐진다.** `App.tsx` 가 `openMeetingId` 로 두 페이지를 갈라 띄우는 구조(`App.tsx:58`, `App.tsx:469`/`487`)는 시안에서 「목록 칸의 선택 상태」로 내려온다.

### `meetings.css` 와 `workspace.css` 가 둘 다 남아 있는 이유

브리프가 단서로 짚은 그것이다. 확인한 결과 **둘 다 살아 있고, 다만 `meetings.css` 의 일부가 고아다.**

| 파일 | 정의하는 것 | 현재 상태 |
|---|---|---|
| `meetings.css`(8,687 B) | `.scax-meeting-list` `.scax-meeting-section*` `.scax-meeting-card*` `.scax-agenda-block*` | **살아 있다** — `workspace.v1.jsx` 의 2칸·3칸이 그대로 쓴다 |
| `meetings.css` 중 | `.scax-note-panel*`(9종) · `.scax-meeting-placeholder*`(2종) | **고아** — `workspace.v1.jsx` 에서 참조 0건. 2026-09-13 에 지워진 `MeetingList.html` 의 오른쪽 미리보기 패널용이었다 |
| `workspace.css`(11,497 B) | `.scax-detail*` `.scax-live-bar*` `.scax-note*` `.scax-note-line*` `.scax-time-chip` `.scax-add-agenda*` `.scax-side-rail*` `.scax-script-line*` `.scax-drawer*` `.scax-modal--md` `.scax-field-row` | **전부 살아 있다** — 3칸·4칸·드로어·업무 요청 모달 |

→ 다음 바퀴에서 `meetings.css` 를 옮길 때 `.scax-note-panel*` · `.scax-meeting-placeholder*` **11종은 옮기지 않는다.** (사본에는 원격 그대로 남겨 두었다.)


## §8 시안 ↔ 현 화면 레이아웃 차이표

> **레이아웃만 적는다.** 상태 관리·API 호출·권한 판단은 우리 것을 유지하므로 이 표에 없다.
> 레이아웃을 시안대로 그리려면 로직을 건드려야만 하는 항목은 표 아래 「로직이 걸리는 항목」에 따로 모았다.

### 8-A `MyWork.html` ↔ 우리 업무 화면 (`MyWorkPage.tsx` · `WorkViews.tsx` · `App.tsx` 셸)

| 영역 | 시안의 레이아웃 | 현 코드의 레이아웃 (파일:줄) | 차이 |
|---|---|---|---|
| 페이지 틀 | 가로 flex `.scax-app-shell`, nav 180(접으면 65) + main. `min-width:1542px` · `height:100vh` · `overflow:hidden` | `App.tsx:342` `.thesc-shell` = `grid-template-columns:200px minmax(0,1fr)` (`styles.css:102`), `min-height:100vh` 라 페이지가 세로로 스크롤한다 | nav 200→180, 접힘 65 신규 · 페이지 스크롤 → 칸 내부 스크롤 |
| 본문 폭 | `.scax-page-body__content` 가변, `min-width:640px`, 좌우 레일이 폭을 먹고 남은 만큼 | `App.tsx:403` `.canvas` `max-width:1720px; margin-inline:auto; padding:0 40px 152px` (`styles.css:131`) | 가운데 정렬 고정폭 → 레일 사이 가변폭. 하단 152px 여백 사라짐 |
| 머리 | `AppHeader` **60px 한 줄**: h1 「업무」 + 오른쪽 액션. breadcrumb 줄은 두지 않는다(`scax.css` 주석 「디자이너 확정」) | **두 줄이다** — `App.tsx:404` 전역 `.canvas-topbar` 38px(breadcrumb·persona) + `MyWorkPage.tsx:320` 페이지 `.page-head`(h1 + 액션, `min-height:42px`) | **두 줄 → 한 줄로 합침** · breadcrumb 줄 삭제 |
| h1 문구 | 「업무」 | 「내 업무」 (`MyWorkPage.tsx:321`) | 라벨 변경 |
| 머리 액션 | 2개 — `일일보고 생성`(outlined primary) · `업무 만들기`(solid primary) | 1개 — `새 업무 추가`(`.btn.primary`) (`MyWorkPage.tsx:324`) | 1 → 2, 라벨 변경 |
| **좌 레일** | **수신함 380px 고정** — `GutterList`(제목 + count 배지 + 분류 SegmentedControl) 안에 `InboxCard` N장 | **없다.** `.work-layout` 은 `grid-template-columns: minmax(0,1fr)` 단일 열 (`MyWorkPage.tsx:331`, `styles.css:409`) | **레일 신설** |
| 판단할 것의 자리 | 좌 레일 수신함이 그 자리다 | 본문 맨 위 접이식 패널 `.decision-section`(24px 패딩, 16px 라운드 테두리) (`MyWorkPage.tsx:334`, `styles.css:411`) | 본문 위 패널 → 좌 레일로 이동 |
| 본문 탭 | `.scax-tabs` 3개(내 업무 / 보낸 업무 / 완료 업무), 높이 **52px**, 밑줄 2px, 좌우 24px 패딩, `min-width:880px` | `.page-tabs` 3개(할일 / 요청·배정 / 조직 업무), 높이 **44px**, gap 20px (`MyWorkPage.tsx:363`, `styles.css:416~419`) | 높이 44→52 · **탭 구성이 다르다**(아래 로직 항목 3) |
| 필터 줄 | `.scax-chip-bar` — Chip 여러 개가 한 줄로 나열 + `margin-left:auto` 로 오른쪽 끝에 `WBS 보기` | `.list-toolbar` — 왼쪽 탭, 오른쪽 `.toolbar-group`(상태 필터 Popover 1개 + 보기 방식 `.segmented` 3칸) (`MyWorkPage.tsx:362`, `379~421`) | 팝오버 1개 → 칩 나열 · 탭과 필터가 **같은 줄 → 다른 줄**로 분리 |
| 보기 방식 | 자리가 없다 | `.segmented` 목록/칸반/타임라인 (`MyWorkPage.tsx:411`, `MyWorkPage.tsx:68~72`) | 시안에 없음(로직 항목 5) |
| 표 | `div` + CSS grid `.scax-task-table`, 6열 **고정 트랙 `44 / minmax(0,1fr) / 120 / 140 / 120 / 200`**, 머리 35px, 행 min 50px, `min-width:880px`, **본문(`__body`)만 스크롤** | 시맨틱 `<table class="plain-table my-work-task-table">`, th 44px / td 56px, 표 전체가 페이지와 함께 흐른다 (`MyWorkPage.tsx:550`, `styles.css:241~252`) | `<table>` → `div` grid · 머리 고정 + 본문 스크롤 |
| 표 열 | 6열: (별표) · 제목/종류 · 요청자 · 기한 · 상태 · 액션 | 7열: 제목 · 상태 · 시작일 · 담당자 · 기한 · 출처 · 액션 (`MyWorkPage.tsx:550~560`) | 열 수·순서·구성이 다르다. 시작일·출처 열 없음, 별표 열 신규 |
| 별표 | 44px 첫 열 `IconButton` `star`/`star-fill` | 없음 | **신규** |
| 상태 셀 | `Select` 팝오버(작은 알약 트리거 26px, tone 별 배경) | 텍스트 라벨 (`MyWorkPage.tsx:717~719`) | 읽기 → 인라인 편집 컨트롤 |
| 기한 셀 | `.scax-task-table__due` + 초과분 `__due-extra`(빨강 `+1`) | 텍스트 (`MyWorkPage.tsx:721`) | 초과 배지 신규 |
| **우 레일** | **캘린더 342px 고정** — `CalendarRail`(오늘/주간/월간 SegmentedControl + 근무 시간 + `AgendaItem` N) | 없다. 캘린더는 별도 화면 `CalendarPage.tsx` | **레일 신설** |
| AI | `AgentBubble` `position:fixed; right:24px; bottom:24px`, 말풍선 + orb 120×110 | `App.tsx` `AssistantLauncher` → 열면 `ChatDrawer` | 자리는 같고 모양·크기가 다르다 |
| 칸별 상태 | 세 칸이 각각 default / empty / loading / error 를 그린다 | 페이지 단위 (`Skeleton`·`Empty`) | 레일 신설분만큼 상태 표현도 신설 |

**8-A 레이아웃 차이 건수: 19**

### 8-B `MeetingWorkspace.html` ↔ 우리 회의 화면 (`MeetingListPage.tsx` + `MeetingDetailPage.tsx`)

§7 판정에 따라 시안 1장이 우리 2장에 대응한다.

| 영역 | 시안의 레이아웃 | 현 코드의 레이아웃 (파일:줄) | 차이 |
|---|---|---|---|
| 화면 수 | **1장** | **2장** — `App.tsx:469` 상세 / `App.tsx:487` 목록, `openMeetingId` 로 분기 | 2 → 1 (로직 항목 1) |
| 칸 구성 | 4칸: nav 180 / 목록 380 / 상세 가변(min 640) / 첨부 342 | 목록 화면 2칸 `minmax(0,.9fr) minmax(0,1.1fr)` (`MeetingListPage.tsx:168`, `styles.css:1486`) · 상세 화면 2칸 `1.15fr .85fr` (`MeetingDetailPage.tsx:821`, `styles.css:1487`) | 전면 재편 |
| 목록 칸 | 왼쪽 레일 **380 고정**, 카드 세로 나열 | 목록 화면의 왼쪽 열(**가변 0.9fr**), `.meeting-panel` 테두리 상자 안 (`MeetingListPage.tsx:169`) | 가변 → 고정 380 · 패널 테두리 사라짐 |
| 목록의 오른쪽 미리보기 | **없다** | `MeetingListPage.tsx:335~369` 회의록 미리보기 `.meeting-panel` | **삭제** (CSS `.scax-note-panel*` 이 고아로 남은 이유, §7) |
| 상세 칸 | 3칸(본문), 칸 자체가 흰 바탕이고 테두리가 없다 | 별도 페이지의 왼쪽 `.meeting-panel`(1px 테두리 + 16px 라운드) (`MeetingDetailPage.tsx:822`, `styles.css:1489`) | 페이지 → 칸 · 패널 테두리 사라짐 |
| 첨부·스크립트 | 4칸 **342 고정**, 늘 선다. 머리는 `SegmentedControl [자료\|스크립트]` | 상세 페이지 오른쪽 열(**가변 0.85fr**), `rightShown` 일 때만 렌더, 머리는 밑줄 탭 `.meeting-tabs` (`MeetingDetailPage.tsx:1003~1004`) | 가변→고정 · 조건부→상시 · 탭→세그먼티드 |
| 칸 접기 | `focus` 면 **목록 칸**이 사라진다 (nav\|상세\|첨부) (`workspace.v1.jsx` `railLeft={focus ? null : …}`) | `.meeting-columns.detail.single` 로 **첨부 칸**을 접는다 (`styles.css:1488`) | **접는 칸이 반대다** |
| 페이지 머리 | `AppHeader` 60px 하나: h1 「회의」 + `회의 생성`(outlined primary) + `빠른 시작`(solid primary, `play` 아이콘) | 목록: `.page-head` h1 + `빠른 시작`(primary, play) + `회의 예약` (`MeetingListPage.tsx:154~166`) · 상세: 편집 가능한 제목·메타 블록 `.page-head.meeting-head` (`MeetingDetailPage.tsx:625~755`) | 머리 하나로 통합 · 라벨 「회의 예약」→「회의 생성」 · 순서 반대(생성이 왼쪽) |
| 회의 제목 | **3칸 안** `.scax-detail__title` (18px, 한 줄 말줄임) | **페이지 머리** `h1.meeting-page-title` (`MeetingDetailPage.tsx:741`) | 페이지 머리 → 본문 칸 머리로 내려온다 |
| 회의 메타 | 제목 아래 한 줄 `.scax-detail__facts` — 「일시 · 장소 · 참석 N명 · 소요」 | 머리 안 편집 폼 `.meeting-meta-edit`(field 4개) (`MeetingDetailPage.tsx:658~712`) | 편집 폼 → 읽기 한 줄 |
| 상태 배지 | 셋에만 — 정리 중 · 실패 · 취소 (`workspace.v1.jsx` `{settling \|\| failed \|\| cancelled}`) | 상태별 표시 | 배지를 다는 상태가 줄어든다 |
| 진행 바 | `.scax-live-bar` **3칸 맨 위**, accent 5% 바탕 + 하단 1px 선, 각진 전체폭 | `.meeting-live-bar` 페이지 상단 `sticky`, `--selected-bg` 바탕, 라운드 카드 + 아래 12px 여백 (`MeetingDetailPage.tsx:606`, `styles.css:1539`) | 위치·모양 |
| 목적 | `.scax-detail__purpose` 전체 폭 한 줄, 왼쪽 3px accent 세로선, 오른쪽만 라운드 | `.effect-note.meeting-purpose` (`MeetingDetailPage.tsx:813`) | 모양 |
| 회의록 머리 | **한 줄** — 왼쪽 「AI 회의록」 고정, 오른쪽 자리만 상태별(예정 빈칸 / 진행 중 `[메모\|AI 요약]` 세그먼티드 / 완료 `[수정]`) | **두 줄** — `.meeting-note-head`(제목 줄) + `.meeting-tabs`(탭 줄) (`MeetingDetailPage.tsx:823`, `857`) | 두 줄 → 한 줄 · 밑줄 탭 → 세그먼티드 |
| 안건 | `.scax-agenda-block` 흰 바닥, 24px 좌우 패딩, **하단 1px 선으로만** 줄을 가른다 | `src/meetings/AgendaBlock.tsx` | 카드 → 경계선 |
| 근거 시각 | `.scax-time-chip` 이 줄 **오른쪽 끝**에 모여 선다(`.scax-note-line__evidence{justify-content:flex-end}`) | `src/TimeChip.tsx` (`meetings/AgendaBlock.tsx`) | 정렬 위치 |
| 메모 입력 | `.scax-note__composer` 회의록 칸 **하단 고정** 줄 | `src/meetings/MemoComposer.tsx` | 위치 |
| 안건 추가 | `.scax-add-agenda` 본문 흐름 맨 아래(예정 회의만) | `.meeting-add-agenda` (`MeetingDetailPage.tsx:957`) | 위치 유사 |
| 목록 카드 | `.scax-meeting-card` 14px 라운드 카드, 12px 패딩, 예정 회의만 카드 하단에 `수정`/`삭제` 2버튼 1:1 | `.meeting-row` 8px/12px 패딩 목록 행, gap 6px (`styles.css:1398`, `1503`) | 행 → 카드 |
| 목록 구획 | 「예정 N」 / 「지난」 + 맨 아래 가운데 `더 보기` 버튼 | 「예정 N」 / 「지난」 (`MeetingListPage.tsx:186`, `201`) | `더 보기` 신규 |
| 자료 미리보기 | `.scax-drawer` 오른쪽 **520px** 드로어 | `src/meetings/MaterialDrawer.tsx`, `.drawer` 840px (`styles.css:507~`) | 폭 840 → 520 |
| 업무 요청 모달 | `.scax-modal--md` **560px**, 사람·기한이 `.scax-field-row` 로 한 줄에 나란히 | `src/WorkModals.tsx` | 폭·필드 배치 |
| 삭제 확인 | `.scax-modal--sm` **420px** `role="alertdialog"`, 푸터에 위험 버튼 하나만 | `MeetingListPage.tsx:232~` `.modal` 600px | 폭 600 → 420 · 취소 버튼 없음 |
| AI | `AgentBubble` 우하단 고정 | `AssistantLauncher` | 모양 |

**8-B 레이아웃 차이 건수: 23**

### 로직이 걸리는 항목 — 코디 판단거리 (6건)

레이아웃을 시안대로 그리려면 **우리 로직·구조를 건드려야만** 하는 자리다. 워커는 제안하지 않고 올린다.

| # | 항목 | 왜 로직이 걸리나 |
|---|---|---|
| L-1 | **회의 2화면 → 1화면** | `App.tsx:58~72`(`openMeetingId`·`openMeetingTitle`·`closeMeeting`·`registerMeetingLeaveGuard`)·`App.tsx:469~493` 이 「페이지 전환」 전제로 짜여 있다. 한 화면이 되면 이 상태가 「목록 칸의 선택」으로 내려가야 하고, **고치던 것이 있을 때 묻는 이탈 가드**(SCR-106-T11)가 걸 대상이 사라진다 |
| L-2 | **breadcrumb 줄 삭제** | 시안·`tokens/scax.css` 주석이 「브레드크럼 줄은 두지 않는다(디자이너 확정)」라고 못박는다. 그런데 `App.tsx:414~430` 의 breadcrumb 이 **회의 상세에서 목록으로 돌아가는 유일한 경로**(`closeMeeting`)다. 없애면 뒤로 가는 길이 사라진다 |
| L-3 | **업무 탭 구성 변경** | 시안 「내 업무/보낸 업무/완료 업무」 ↔ 현재 「할일/요청·배정/조직 업무」. `조직 업무` 는 `canReadOrganizationWork`, `요청·배정` 은 `canCreateWorkRequests \|\| canAssignTasks \|\| requestsToMe.length>0 \|\| ccRequests.length>0` 로 **envelope 권한에 따라 나타났다 사라진다**(`MyWorkPage.tsx:366`, `372`). 시안 탭에는 그 권한이 붙을 자리가 없다 |
| L-4 | **「판단이 필요한 업무」 → 좌 레일 수신함** | 우리 `actionItems`(`ActionItemCard`)와 시안 `InboxCard`(kind `task`/`notice`, badge·who·source·2버튼)는 **데이터 모양이 다르다**. 같은 자리에 그대로 옮길 수 없고, 무엇을 수신함으로 볼지가 먼저 정해져야 한다 |
| L-5 | **보기 방식(목록/칸반/타임라인) 제거** | 시안 칩 바에 자리가 없다. `view` 상태와 `WorkViews.tsx` 의 칸반·타임라인 렌더가 통째로 갈 곳을 잃는다 |
| L-6 | **`min-width:1542px` · 페이지 스크롤 제거** | `.scax-app-shell{height:100vh;overflow:hidden}` 이라 **모든 화면**이 「칸 내부 스크롤」로 바뀐다. 우리 `MinWidthNotice` 와 1280 단 반응형(`styles.css:826~910`)이 그 전제와 정면으로 충돌한다 |


## §9 부품 은퇴 매핑표

목록은 `.design-sync/config.json` 의 `componentSrcMap` 20개 그대로다. **사용처**는 `frontend/src` 에서 `<Name` 을 센 건수(프로덕션 / 테스트 분리).

> **먼저 읽어야 할 사실.** 새 DS 의 부품 201개 중 **193개는 Figma variant 를 그대로 굳힌 정적 렌더러**다. `.d.ts` 를 열어 보면 props 가 `text1`·`text2`·`icon1`·`className`·`style` 과 boolean/enum variant 뿐이고 **데이터 배열도 콜백도 받지 않는다**(예: `TaskTable` 은 `type:"my"|"request"|"done"` 과 머리글 문자열 4개만 받는다 — 행을 넣을 수 없다). 실제로 갈아끼울 수 있는 것은 **의도적 추가분 8개**(`Icon` · `DateField` · `DatePicker` · `TimeField` · `AppShell` · `AppHeader` · `AppBody` · `SideNav`)와 **핸드오프 JSX/CSS 의 프리미티브**(`scax-ui.jsx` 20종 + `work-modal.jsx` 10종)뿐이다. 아래 「새 DS 의 대응」은 그 구분을 달아 적었다.

| 현 부품 | 소스 | 사용처(prod/test) | 새 DS 의 대응 | 판정 |
|---|---|---:|---|---|
| `Icon` | `src/Icon.tsx` | 79 / 9 | `components/icon/Icon` **(의도적 추가·실물)** — `name`/`size`/`strokeWidth`, 글리프 120종 | **대응은 있는데 props·구조가 다름** — 시그니처는 같으나 viewBox 16→24 그리드, 글리프 **이름 체계가 다르고 우리 30종 중 10종이 새 세트에 없다**(gaps #G-03) |
| `Popover` | `src/Popover.tsx` | 6 / 1 | DS 부품 **없음**(readme 「Popover … 의도적으로 없다」). 핸드오프 `scax-ui.jsx` `Popover({open,onClose,placement})` + `.scax-popover*` | **새 DS 에 없음** — 핸드오프 프리미티브로 대체 가능. 우리 것의 `trigger` 렌더프롭·`label` 은 없다 |
| `Empty` | `src/Empty.tsx` | 29 / 6 | `components/feedback/EmptyPage`(정적, props 는 `className`/`style` 뿐) + 핸드오프 `Empty({icon,title,desc})` + `.scax-empty*` | **대응은 있는데 props·구조가 다름** — DS 부품은 내용 주입 불가. 우리 `variant="error"`·`onAction` 은 핸드오프 `StatusNote` 로 갈라 담아야 한다 |
| `EmptyValue` | `src/Empty.tsx` | 10 / 0 | **없음** — DS·핸드오프 어디에도 인라인 「값 없음」 표시가 없다 | **새 DS 에 없음(구 것을 남겨야 함)** |
| `Skeleton` | `src/Skeleton.tsx` | 16 / 4 | DS 부품 **없음**(readme 「Skeleton … 의도적으로 없다」). 핸드오프 `Skeleton({variant,width})` + `.scax-skeleton*`(text/title/card/agenda, w-40/60/80/full) + `.scax-skeleton-row`·`__stack` | **새 DS 에 없음** — 핸드오프로 대체 가능. 우리 `label`(스크린리더 문구)이 없다 |
| `ProgressBar` | `src/ProgressBar.tsx` | 1 / 4 | **없음** — DS·핸드오프 어디에도 없다. `CircularCircular` 는 무한 스피너라 진행률을 못 그린다 | **새 DS 에 없음(구 것을 남겨야 함)** |
| `Drawer` | `src/Modal.tsx` | 6 / 0 | DS 부품 **없음**. `workspace.css` 에 `.scax-drawer*` 골격(오른쪽 **520px**, head/hint/body/foot/spacer) + `workspace.v1.jsx` `MaterialDrawer` | **새 DS 에 없음** — 골격만 있다. 사다리 ②(껍데기는 DS, 안은 우리 것). 우리 Drawer 는 840px |
| `ConfirmModal` | `src/Modal.tsx` | 3 / 0 | DS 부품 **없음**. `.scax-modal--sm`(**420px**, `role="alertdialog"`, 푸터 위험 버튼 하나) 골격 있음 | **새 DS 에 없음** — 골격만. 사다리 ② |
| `Toast` | `src/Modal.tsx` | 2 / 5 | DS 부품 **없음** — readme 가 명시한다: 「Toast 는 업무 화면에서 필요해 발주본 CSS 에 두었고, DS 컴포넌트로는 아직 올리지 않았다」. `work-modal.jsx` `Toast({message,onDone})` + `.scax-toast`(하단 고정, 3초) | **새 DS 에 없음** — 핸드오프로 대체 가능 |
| `Checkbox` | `src/FormControls.tsx` | 2 / 4 | `components/forms/ControlCheckbox`·`CheckboxField`·`CheckboxResourceControl2`(전부 정적) + 핸드오프 `.scax-checkbox`/`__input`/`__box` | **대응은 있는데 props·구조가 다름** — DS 는 `state:"unchecked"\|"checked"\|"indeterminate"` 문자열 variant 이고 **`onChange` 가 없다**. 핸드오프 것은 네이티브 `<input type=checkbox>` + 가짜 박스라 실물이다 |
| `FieldMessage` | `src/FormControls.tsx` | 6 / 4 | **없음**. 핸드오프 `Field` 의 `.scax-field__hint` 한 톤만 있다(assistive 색 고정) | **새 DS 에 없음** — error/warning 톤 구분이 없다 (gaps #G-05) |
| `DateField` | `src/DateField.tsx` | 11 / 6 | `components/datetime/DateField` **(의도적 추가·실물)** — `value`/`onChange`/`size`/`placeholder`/`invalid`/`marks`/`min`/`max`/`ariaLabel` | **1:1 대응(갈아끼우면 됨)** |
| `MinWidthNotice` | `src/MinWidthNotice.tsx` | **0** / 1 | **없음**. 새 DS 는 `min-width:1542px` 를 전제로 깔고 좁은 폭을 다루지 않는다 | **새 DS 에 없음** — 다만 프로덕션 사용처 0 |
| `TimeChip` | `src/TimeChip.tsx` | 1 / 0 | DS 부품 **없음**. `workspace.css` `.scax-time-chip`(24px, 6px 라운드, tabular-nums, hover accent) + `workspace.v1.jsx` 인라인 버튼 | **새 DS 에 없음** — CSS 골격만. 사다리 ② |
| `TaskCalendar` | `src/WorkViews.tsx` | 1 / 1 | `components/work/WorkCalendar`(정적, `type:"월간"\|"주간"\|"오늘"`·`empty`·`task`·`text1~4`) + 핸드오프 `CalendarRail`/`WeekView`/`MonthView`/`DayCell`/`CalendarNav`/`AgendaItem` | **대응은 있는데 props·구조가 다름** — DS 것은 일정 데이터를 못 넣는다. 핸드오프 것이 실물이다 |
| `DatePicker` | `src/DatePicker.tsx` | 1 / 2 | `components/datetime/DatePicker` **(의도적 추가·실물)** — `value`/`onChange`/`marks`/`min`/`max`, 월요일 시작 월 그리드 | **1:1 대응(갈아끼우면 됨)** |
| `Select` | `src/Select.tsx` | 10 / 10 | `components/forms/SelectSelect`(정적 — `value?:string` 문자열 하나 + boolean variant 14개, **options 배열 없음**) + 핸드오프 `Select({value,options,onChange,tone,ariaLabel})` | **대응은 있는데 props·구조가 다름** — DS 것은 못 쓴다. 핸드오프 것은 실물이나 우리 Select 의 **검색·게스트 추가**(`.popover-guest*`)가 없다 |
| `MultiSelect` | `src/Select.tsx` | 1 / 8 | **없음** — `SelectSelect` 에 `render:"chip"` variant 는 있으나 정적이고, 핸드오프에 다중 선택이 없다(`.scax-person-chips`/`.scax-person-chip` CSS 만 있고 JS 부품 없음) | **새 DS 에 없음** — CSS 골격만 |
| `TimeField` | `src/TimeField.tsx` | 2 / 5 | `components/datetime/TimeField` **(의도적 추가·실물)** — `value`/`onChange`/`size`/`step`/`from`/`to`/`invalid` | **1:1 대응(갈아끼우면 됨)** |
| `TimeRangeField` | `src/TimeField.tsx` | 2 / 7 | **없음** — DS `TimeField` 는 단일 시각이다. 시작·끝 한 쌍을 다루는 부품이 없다 | **새 DS 에 없음(구 것을 남겨야 함)** |

**판정 분포 — 1:1 대응 3 · props·구조가 다름 5 · 새 DS 에 없음 12 · (새 DS 에만 있는 것 193)**

- 1:1 대응 3: `DateField` `DatePicker` `TimeField`
- 다름 5: `Icon` `Empty` `Checkbox` `TaskCalendar` `Select`
- 없음 12: `Popover` `EmptyValue` `Skeleton` `ProgressBar` `Drawer` `ConfirmModal` `Toast` `FieldMessage` `MinWidthNotice` `TimeChip` `MultiSelect` `TimeRangeField`
  - 이 중 **핸드오프 JSX 로 대체 가능** 4: `Popover` `Skeleton` `Toast` (+ `Empty` 계열)
  - **CSS 골격만 있어 사다리 ②** 4: `Drawer` `ConfirmModal` `TimeChip` `MultiSelect`
  - **아무 데도 없음(사다리 ④ → gaps)** 4: `EmptyValue` `ProgressBar` `FieldMessage` `TimeRangeField` (+ `MinWidthNotice`, 사용처 0)

### 새 DS 에만 있는 것 (우리가 안 쓰는 것)

`_ds_manifest.json` 기준 201개. 우리가 쓸 것은 **8개**(shell 4 + `Icon` + datetime 3). 나머지 **193개**는 정적 추출물이라 앱에 들어가지 않는다.

| 그룹 | 개수 | 우리가 쓰나 |
|---|---:|---|
| `actions` | 10 | ✗ (버튼은 핸드오프 `.scax-button*` 로) |
| `avatar` | 11 | ✗ |
| `badges` | 4 | ✗ (`.scax-badge*` 로) |
| `calendar` | 6 | ✗ (`datetime/DatePicker` 로) |
| `cards` | 8 | ✗ |
| `chips` | 10 | ✗ (`.scax-chip*` 로) |
| `datetime` | 3 | **✓ 3개 전부** |
| `feedback` | 19 | ✗ |
| `forms` | 20 | ✗ |
| `glyphs` | 42 | ✗ (readme: 「new work should use `<Icon>`」) |
| `icon` | 1 | **✓** |
| `lists` | 17 | ✗ |
| `misc` | 21 | ✗ |
| `navigation` | 15 | ✗ (`SideNav`·`AppHeader` 가 대신한다) |
| `shell` | 4 | **✓ 4개 전부** |
| `work` | 10 | ✗ (`TaskTable`·`WorkCalendar`·`MODCreateTask` 는 정적. 핸드오프 JSX 가 실물) |

## §10 화면 전수 + 시안 유무

`App.tsx` 는 라우터를 쓰지 않는다 — `surface` 상태(`ProductSurface` 8종)로 갈아 끼운다(`App.tsx:28~48`, `456~513`). 페이지 컴포넌트는 **10개**, 그 위에 전면 오버레이 **3개**가 더 있다.

| # | 화면 | 파일 | 진입 | 시안 | 교체 방식 |
|---:|---|---|---|---|---|
| 1 | 로그인 | `src/LoginPage.tsx` | 세션 없음 (`App.tsx:332`) | ✗ | ③ 토큰·부품만 |
| 2 | 오늘(홈) | `src/TodayPage.tsx` | `surface="today"` | ✗ | ③ |
| 3 | 캘린더 | `src/CalendarPage.tsx` | `surface="calendar"` | ✗ | ③ (+ 새 `WeekView`/`MonthView` 참고 가능) |
| 4 | 회의 목록 | `src/meetings/MeetingListPage.tsx` | `surface="meetings"`, `openMeetingId===null` | **✓ `MeetingWorkspace.html` 2칸** | ① 시안 레이아웃 |
| 5 | 회의 상세 | `src/meetings/MeetingDetailPage.tsx` | `surface="meetings"`, `openMeetingId!==null` | **✓ `MeetingWorkspace.html` 3·4칸** | ① 시안 레이아웃 (4와 **합쳐진다**) |
| 6 | 내 업무 | `src/MyWorkPage.tsx` (+ `WorkViews.tsx` · `WorkModals.tsx`) | `surface="work"` | **✓ `MyWork.html`** | ① 시안 레이아웃 |
| 7 | 일일보고 | `src/DailyReportPage.tsx` | `surface="report"` | ✗ | ③ |
| 8 | 프로젝트 | `src/ProjectPage.tsx` | `surface="project"` | ✗ | ③ |
| 9 | 조직 | `src/OrgPage.tsx` (+ `src/org/` 6벌) | `surface="org"` | ✗ | ③ |
| 10 | 관계 탐색 | `src/RelationGraphPage.tsx` (+ `GraphCanvas.tsx`) | `surface="graph"` | ✗ | ③ (그래프 캔버스는 `--graph-*` 토큰 9종을 따로 쓴다 → gaps #G-06) |
| O1 | AX 채팅 드로어 | `src/chat/ChatDrawer.tsx` (+ `MessageList` · `AssistantMarkdown`) | `isAxOpen` | ✗ (DS `AiChatSidebar` 는 정적) | ③ — **덩치가 크다**(구 CSS 550~825 + 1093~1276 ≈ 460줄, 테스트 CSS 결합 99건) |
| O2 | 액션 센터 | `src/ActionCenter.tsx` (+ `ActionTaskCard` · `ActionMeetingCard` · `ActionProgressBatchCard` · `ActionPreview`) | 드로어 | ✗ | ③ |
| O3 | 어시스턴트 캐릭터 선택 | `src/AssistantCharacterPicker.tsx` | 모달 | ✗ | ③ |

**시안 있음 3(화면 2장으로 합쳐짐) · 시안 없음 10.**

**시안 없는 화면이 토큰·부품 교체만으로 따라오나 — 한 줄 판단:**

> **대체로 따라온다. 다만 두 곳은 손이 따로 간다** — ① **셸**이 바뀌면(`min-width:1542px` · 페이지 스크롤 제거 · `.canvas` 고정폭 삭제) **10장 전부가 한꺼번에 흔들린다**. 이건 부품 교체가 아니라 틀 교체라서 화면마다 스크롤 경계를 다시 잡아 줘야 한다(L-6). ② **AX 채팅 드로어**(O1)는 구 CSS 의 3분의 1(약 460줄)과 테스트 CSS 결합의 절반(99/153)이 몰려 있어 자기 바퀴가 필요하다. 나머지 8장은 `.btn`·`.plain-table`·`.modal`·`.field` 같은 공용 클래스만 쓰므로, 그 공용 클래스가 `.scax-*` 로 갈리면 함께 따라온다.

## §11 교체 순서 제안 + 지우는 시점

목표는 **§10 의 화면 13개(페이지 10 + 오버레이 3)가 하나도 빠지지 않고 새 DS 로 도는 것**이다.
「깨지는 테스트」는 `frontend/src/**/*.test.tsx` **40파일 · `it()`/`test()` 468개** 중 해당 클래스·부품을 grep 한 건수다. 전체적으로 **role/text 질의가 1,472건, CSS 결합(`querySelector`·`toHaveClass`·`className`)이 153건** — 즉 **테스트의 대부분은 레이아웃에 안 묶여 있고, 깨질 위험은 CSS 결합 153건에 몰려 있다.**

| 바퀴 | ① 무엇을 바꾸나 | ② 깨지는 테스트(대략) | ③ 그 바퀴에서 지울 수 있는 `styles.css` 덩어리 |
|---|---|---|---|
| **1 토큰** | `tokens/` 7벌 중 6벌을 앱에 싣는다(**`fonts.css` 제외** — §5 가 열려 있다). `shell.css` 의 element 리셋 7줄과 `product.css` 의 `a`/`a:hover` 2줄은 **잘라내고** 싣는다. `scrollbar.css` 도 **보류**(`*{scrollbar-width:none}`). 아직 아무 화면도 `--scax-*` 를 참조하지 않으므로 **화면은 그대로다** | **0건** — 참조하는 코드가 없다 | **없음.** 구 65개 토큰은 전부 살아 있어야 한다 |
| **2 셸** | `AppShell`/`AppHeader`/`AppBody`/`SideNav` + `.scax-*` 셸 CSS 로 `.thesc-shell`·`.rail`·`.canvas`·`.canvas-topbar` 를 갈아탄다. **13화면 전부가 이 바퀴에서 한 번 흔들린다.** L-2(breadcrumb)·L-6(min-width·스크롤)이 여기서 걸린다 | `App.test.tsx` 4 · 셸 클래스 질의 2 · 각 페이지 테스트의 `.canvas` 전제 (넉넉히 **10건 내외**) | `101~139` **shell** (39줄). `.page-surface`·`.page-head`(140~160)는 페이지가 아직 쓰므로 남긴다 |
| **3 프리미티브** | 핸드오프 `scax-ui.jsx`(20종) + `work-modal.jsx`(10종)를 `src/` 의 기존 자리(`src/*.tsx`, 새 폴더 만들지 않음)로 옮겨 `Button`·`Badge`·`IconButton`·`Select`·`Popover`·`Empty`·`StatusNote`·`Skeleton`·`Chip`·`Tabs`·`SegmentedControl`·`Modal`·`Field`·`TextField`·`Composer`·`AutoComplete`·`Checklist`·`DropZone`·`FileList`·`Toast` 를 갈아끼운다. §9 의 1:1 3개(`DateField`·`DatePicker`·`TimeField`)도 여기서 DS 것으로 바꾼다 | `Modal` 8 · `Checklist` 14 · `Select` 7 · `DatePicker` 4 · `DateField` 4 · `Popover` 3 · `Skeleton` 3 · `TimeField` 1 · `Empty` 1 (**≈45건**) | `161~212` 버튼·상태/배지 · `254~351` 폼 · `507~549` 오버레이(drawer/modal/toast) · `1323~1396` date/select/time/checklist (**≈290줄**) |
| **4 아이콘** | `src/Icon.tsx` 30 글리프 → DS `Icon` 120 글리프. 이름 매핑(`check-square`→`square-check`, `file`→`document`, `refresh`→`reset`, `alert`→`circle-exclamation`, `filter`→`tune`, `list`→`align-justify`)과 **없는 10종**(gaps #G-03) 처리가 이 바퀴의 알맹이 | `Icon.test.tsx` 10 · 아이콘 이름 질의 산재 (**≈12건**) | (아이콘은 CSS 가 없다. `.icon-check` 등 소소한 줄만) |
| **5 화면 A — 업무** | `MyWorkPage` 를 시안 3칸으로 다시 그린다(좌 수신함 레일 · 본문 탭+칩바+grid 표 · 우 캘린더 레일). L-3·L-4·L-5 결정이 **먼저** 닫혀야 한다 | `MyWorkPage` 5 · `ActionTaskCard` 22 · `ActionCenter` 12 · `CreateWork` 1 · `WorkModals` 1 (**≈41건**) | `213~239` 제네릭 표 · `240~253` plain-table · `407~486` my work · `1007~1031` task fields · `1277~1288` checklist cue (**≈150줄**) |
| **6 화면 B — 회의** | `MeetingListPage` + `MeetingDetailPage` → **한 화면 4칸**. L-1·L-2 결정이 먼저 닫혀야 한다. `meetings.css` 를 옮길 때 고아 11종(`.scax-note-panel*`·`.scax-meeting-placeholder*`)은 빼고 옮긴다 | `MeetingList` 11 · `MeetingAfter` 11 · `MeetingLive` 4 · `MeetingDetail`(role 질의 위주) (**≈30건**) | `1289~1295` 후속업무 · `1397~1457` 회의 목록·상세 · `1458~1578` 회의 화면 · `1612~1613` 진행 중 (**≈195줄**) |
| **7 오버레이 — AX 드로어·액션센터** | `ChatDrawer`(+`MessageList`·`AssistantMarkdown`)·`ActionCenter` 를 `.scax-drawer*` 골격 위로 옮긴다. 구 `.ax-*` 87종이 여기 몰려 있다 | `ChatDrawer` **99** · `AssistantCharacter` 6 · `AssistantPreferenceApp` 4 (**≈109건 — 가장 크다**) | `550~825` AX 드로어 · `1049~1065` 요청 타임라인 · `1066~1092` 관계 섹션·자료 상태 · `1093~1276` 드로어 유틸/실행 레일/합의 드로어 · `1294~1295` (**≈500줄**) |
| **8 남은 화면 7장** | 오늘·캘린더·일일보고·프로젝트·조직·관계 탐색·로그인. 대부분 3~7 바퀴로 이미 따라와 있고, 남은 것은 화면 전용 CSS 정리다 | `OrgPage` 5 · `ProjectPage` 4 · 나머지 role 질의 (**≈12건**) | `140~160` page primitives · `352~406` home · `487~498` report · `499~506`+`1032~1048` 조직 · `911~1006` 로그인 · `1296~1300` 관계 그래프 · `826~910` 반응형 (**≈250줄**) |
| **9 은퇴** | 남은 찌꺼기 정리 + 구 정본 제거 | 0 (앞 바퀴에서 다 옮겨졌다면) | **`styles.css` 전체 삭제** |

**합계 — 바퀴 9개.** 3·4 를 한 바퀴로 묶으면 8개가 된다(권장: 나눈다 — 아이콘 이름 매핑에 사용자 컨펌이 걸린다).

### 마지막 바퀴에서 셋은 어떻게 되나

| 대상 | 처분 |
|---|---|
| `frontend/src/styles.css` (1,613줄) | **삭제.** 그 자리는 `src/styles/` 아래 `tokens.css`(DS 토큰 재수출) + `shell.css` + `components.css` 세 벌이 대신한다 — 핸드오프 README 의 「파일 → 이식 위치」 표 그대로다. `main.tsx` 의 import 한 줄만 바뀐다 |
| `docs/design/design-system-v2.dc.html` | **삭제하지 않고 `docs/design/_archive/` 로 내린다.** 구 화면이 왜 그렇게 생겼는지를 설명하는 유일한 문서라 회고·이력이 이걸 참조한다. 코드 정본에서만 물러난다 |
| `.design-sync/` | **`config.json` 의 `projectId` 를 `8fa54d76…` → `7e839512…` 로 바꾸고, `componentSrcMap` 20개를 갈아엎는다.** 새 목록은 §9 에서 살아남은 것(`Icon`·`DateField`·`DatePicker`·`TimeField` + 핸드오프에서 옮긴 프리미티브)이 된다. `cssEntry` 는 새 `src/styles/index.css` 로, `extraFonts` 는 §5 결정에 따른다. **이 바퀴는 Claude Design 에 쓰기가 일어나므로 별도 승인이 필요하다** |

### 이 순서를 쓰는 이유 (한 줄씩)

- **토큰이 먼저인 이유**: 아무것도 안 깨뜨리면서 다음 여덟 바퀴가 참조할 것을 미리 깔아 둔다. 되돌리기도 제일 싸다.
- **셸이 둘째인 이유**: 틀이 바뀌면 13화면이 한 번은 흔들린다. 그 흔들림을 **부품 교체 전에** 겪어야 원인이 섞이지 않는다.
- **부품이 셋째인 이유**: 시안 없는 화면 10장이 여기서 따라온다. 화면 바퀴에 들어가기 전에 공용 어휘를 한 벌로 만든다.
- **화면이 넷째부터인 이유**: 시안이 있는 두 화면만 레이아웃을 다시 그린다. 나머지는 이미 따라와 있어야 정상이고, 안 따라왔으면 그게 바퀴 8 의 목록이다.
- **은퇴가 마지막인 이유**: 위 표의 ③ 열을 보면 **바퀴 8 이 끝나기 전에는 어느 덩어리도 완전히 비지 않는다.** 중간에 지우면 아직 그 클래스를 쓰는 화면이 깨진다.

---

## §12 사본 안에서 서로 어긋나는 값 — 바퀴 2가 부딪힌다

조사 중 DS 사본 내부에서 **같은 값이 문서마다 다른** 자리를 하나 찾았다. 추측이 아니라 파일에서 읽은 것이다.

| 값 | 60px 이라고 적은 곳 | 72px 이라고 적은 곳 |
|---|---|---|
| 페이지 머리 높이 | `tokens/scax.css` `--scax-header-height:60px` (주석: 「kit 의 머리 높이. 브레드크럼 줄은 두지 않는다 (디자이너 확정)」) · `components/shell/shell.css` `.scax-page-header{flex:0 0 var(--scax-header-height);height:var(--scax-header-height)}` · `guidelines/brand-chrome.card.html` 「page header 60px」 · `readme.md` 「Page header \| 60px tall」 | `components/shell/AppShell.d.ts` 「`AppHeader` 는 브레드크럼 + 제목 + 액션(72px)」 · `handoff/my-work/README.md` 「`PageHeader` 72px」 · `design_handoff_my_work/README.md` 「`PageHeader` 72px」 |

**판정: 60px 이 맞다.** 실제로 렌더되는 것은 CSS 와 토큰이고, 72px 은 브레드크럼 2행을 전제하던 옛 규격이 문서에만 남은 것이다 — 같은 `.d.ts` 가 `breadcrumb` prop 에 「더 이상 쓰지 않는다 — 머리는 제목 한 줄이다 (디자이너 확정)」이라고 적어 스스로 모순을 드러낸다. 바퀴 2 워커가 README 를 먼저 읽으면 72px 로 짓게 되니, **발주 브리프에 60px 을 못박아라.**

같은 결로 `handoff/my-work/README.md` 의 토큰 표에는 `--scax-control-height-lg` 가 빠져 있는데 `tokens/scax.css` 에는 있다(47px). 문서가 낡은 쪽이다.
