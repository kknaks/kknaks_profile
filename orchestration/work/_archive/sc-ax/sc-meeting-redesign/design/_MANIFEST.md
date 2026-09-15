# `design/` — 새 DS 사본 매니페스트

## 출처

| | |
|---|---|
| 프로젝트명 | **TheSC AX Design System** |
| 프로젝트 id | `7e839512-977c-4142-b4b5-d992df566ffc` |
| 받은 날짜 | **2026-09-13** |
| 받은 워커 | designer (바퀴 0 조사) · `task_d5406b826209` |
| 도구 | `DesignSync` `list_files` → `get_file` (read-only. **쓰기 없음** — `finalize_plan`·`write_files`·`delete_files` 호출 0회) |
| 원격 총 경로 수 | 705 (디렉토리 포함) |

## 무엇을 받았고 무엇을 안 받았나

**받은 파일 278개 · 1,325,481 B.** 전수를 받지 않았다 — 코디 결정(2026-09-13, 「플랜 B」)에 따라 범위를 좁혔다.

### 왜 좁혔나

조사 중에 브리프 작성 시점엔 알 수 없던 사실이 나왔다: **새 DS 부품 201개 중 193개가 Figma variant 를 그대로 굳힌 정적 렌더러**다. `.d.ts` 를 보면 props 가 `text1`·`icon1`·boolean variant 뿐이고 데이터 배열도 콜백도 받지 않는다(예: `TaskTable` 은 머리글 문자열 4개만 받고 행을 못 넣는다). readme 도 「verbatim extraction, variant-exploded, large but pixel-exact」라고 적었다. 즉 **다음 바퀴들이 열어 볼 일이 없는 파일**이고, 실제 구현 정본은 `handoff/` 의 JSX/CSS 다(`ds-token-report.md` §9).

코디에게 확인받고 **플랜 B**로 갔다 — `.d.ts` 전부 + 실제로 쓰는 8개만 `.jsx`, `.prompt.md` 제외.

### 받은 것 (278)

| 묶음 | 개수 | 비고 |
|---|---:|---|
| `tokens/` | 7 | 전부 |
| `components/**/*.d.ts` | **199** | **전부** — 「DS 에 그 부품이 있나 · variant 가 뭐냐」를 묻는 색인. 201개 부품 = 199개 파일(`shell/AppShell.d.ts` 가 `AppShell`·`AppHeader`·`AppBody` 셋을 내보낸다) |
| `components/**/*.jsx` | 6 | 실제로 쓰는 것만 — `icon/Icon.jsx` · `datetime/{DateField,DatePicker,TimeField}.jsx` · `shell/{AppShell,SideNav}.jsx` |
| `components/icon/` | 5 | **통째로** (`Icon.jsx` · `Icon.d.ts` · `icon-data.js` · `icon-aliases.js` · `icons.card.html`) — 바퀴 4 글리프 매핑의 정본 |
| `components/shell/shell.css` | 1 | 셸 CSS |
| `components/**/*.card.html` | 16 | 전부 |
| `components/{kit-assets,misc}/fig-assets.css` | 2 | 전부 |
| `guidelines/*.card.html` | **19** | **전부** — 색·타입·간격 규약 정본 |
| `handoff/**` | 10 | **전부** (shell 3 · my-work 4 · meetings 5 중 실제 존재분) |
| 루트 파일 | 8 | `MyWork.html` · `MeetingWorkspace.html` · `styles.css` · `readme.md` · `SKILL.md` · `support.js` · `_ds_manifest.json` · `_adherence.oxlintrc.json` |
| `_ds_bundle.js` | 1 | **잘림** — 아래 참조 |
| `design_handoff_my_work/README.md` | 1 | 발주본 명세 |
| `templates/work-home/ds-base.js` · `ui_kits/work/{README.md,index.html}` | 3 | |

### 실패·잘린 파일 (2)

| 경로 | 무슨 일 | 처분 |
|---|---|---|
| `_ds_bundle.js` | `get_file` 의 **256 KiB 캡**을 넘어 정확히 262,144 B 에서 **절단**됐다(`truncated: true`). 원본은 더 크다 | **부분 파일을 그대로 뒀다.** 캔버스 렌더용 번들이고 우리 경로(핸드오프 소스)에는 불필요하다 — 코디 판정. **결손으로 오해해 다시 받으러 가지 마라** |
| `assets/ai-agent-orb.png` | 같은 256 KiB 캡. 원본 ~1.7 MB 인데 196,608 B 까지만 와서 **깨진 PNG** 가 됐다 | **삭제했다.** 반쪽 바이너리를 온전한 파일로 오인하지 않게. 필요하면 디자이너에게 직접 받거나 Claude Design 웹에서 내려받아라 |

### 안 받은 것 (사유별)

| 묶음 | 개수 | 사유 |
|---|---:|---|
| `components/**/*.jsx` (정적 추출물) | 193 | **플랜 B** — Figma variant 정적 렌더러. 다음 바퀴가 열 일이 없다. 구현 정본은 `handoff/` |
| `components/**/*.prompt.md` | 199 | **플랜 B** — Figma 생성 프롬프트. 코드에 안 들어간다 |
| PNG 바이너리 | 19 | `assets/` 2 · `components/kit-assets/assets/` 14 · `components/misc/assets/` 3. 위 193개 정적 부품이 칠하는 장식 비트맵이다. 바이너리를 전사(轉寫)하면 **한 글자만 틀려도 조용히 깨진 파일**이 되므로 받지 않았다 — 필요한 바퀴가 그 자리에서 `get_file` 로 받아 그 턴에 바로 쓰는 편이 안전하다. `assets/avatar-person.png`·`avatar-company.png` 는 `handoff` 화면이 참조하므로 **바퀴 5 가 먼저 받아야 한다** |
| `design_handoff_my_work/design/**` | 6 | **v1 발주본** — `handoff/my-work/js/my-work.v2.jsx` 가 v2 다(받았다). v1 은 물러난 판 |
| `design_handoff_my_work/ds/**` | 5 | **중복** — `Icon.jsx.txt`·`Icon.d.ts.txt`·`fig-tokens.css`·`product.css`·`typography.css` 는 전부 `components/icon/` · `tokens/` 에 같은 내용으로 이미 있다 |
| `design_handoff_my_work/assets/**` | 3 | 위 PNG 항목과 같음 (루트 `assets/` 와 동일 파일) |
| `templates/work-home/{WorkHome.dc.html,support.js}` | 2 | 캔버스 템플릿. 앱 이식 경로에 안 쓴다 |
| `ui_kits/work/WorkScreen.jsx` | 1 | 정적 부품 위에 얹은 1920×1080 재현물. `handoff/` 가 실물 |
| `uploads/**` | 40 | **브리프가 제외 지정** (붙여넣은 스크린샷) |
| `.thumbnail` · `templates/work-home/.thumbnail` · `thumbnail.html` | 3 | **브리프가 제외 지정** |

### 재수신 방침

> **나중에 특정 부품의 픽셀이 필요하면 그때 그 파일 하나만 `get_file` 로 받는다 — 대량 재다운로드 금지.**
> 위 「안 받은 것」은 결손이 아니라 **의도적 범위**다. `_ds_bundle.js` 의 절단도 마찬가지 — 다시 받아도 같은 자리에서 잘린다.

## 읽은 파일에 지시문처럼 읽히는 내용이 있었나

**있었다. 따르지 않았고, 데이터로만 취급했다.**

| 파일 | 내용 | 처리 |
|---|---|---|
| `SKILL.md` | Agent-Skills 프런트매터(`user-invocable: true`)와 「Read the README.md within this skill… ask them what they want to build… act as an expert designer who outputs HTML artifacts or production code」 — **에이전트에게 역할을 지시하는 문장** | 스킬 정의 파일이지 나에게 온 지시가 아니다. 사본으로만 저장했고 실행하지 않았다 |
| `design_handoff_my_work/README.md` | 「…코드베이스에 넣을 때 `.txt` 를 떼면 된다」 「글리프 맵을 **별도 모듈로 분리하지 말 것**」 「없는 기능을 새로 만들지 말 것」 등 구현 지시 다수 | 디자이너가 **다음 바퀴 구현자**에게 쓴 발주 지시다. 이번 바퀴는 조사라 실행 대상이 아니고, 내용은 리포트의 근거로만 인용했다 |
| `_adherence.oxlintrc.json` | oxlint 규칙으로 「Import design-system components from 'index.js', not component internals」 「Raw hex color — use a design-system color token」 등 | 린트 설정이다. 다음 바퀴가 참고할 규약으로 사본에 남겼다 |

셋 다 **사람이 사람에게 쓴 문서**이고 프롬프트 인젝션 성격은 없었다. 나에게 도구를 쓰게 하거나 범위를 벗어나게 하려는 문장은 없었다.

## 사본에서 발견한 것 — 다음 바퀴가 알아야 할 3가지

1. **`--scax-header-height` 가 문서마다 다르다.** `tokens/scax.css` 와 `components/shell/shell.css` 와 `guidelines/brand-chrome.card.html` 은 **60px**, `components/shell/AppShell.d.ts` 와 `handoff/my-work/README.md` 와 `design_handoff_my_work/README.md` 는 **72px**. **CSS·토큰이 실물이므로 60px 이 맞고, 문서 3곳이 낡았다.** 바퀴 2가 부딪힌다.
2. **`handoff/meetings/css/meetings.css` 에 고아 클래스 11종**(`.scax-note-panel*` 9 · `.scax-meeting-placeholder*` 2). 2026-09-13 에 지워진 `MeetingList.html` 용이고 `workspace.v1.jsx` 는 참조하지 않는다. 옮길 때 빼라.
3. **`tokens/fonts.css` 는 jsDelivr 원격 URL 로만 폰트를 받는다** — `_ds_manifest.json` 의 `fonts[]` 가 `"files": [], "remoteSrc": true`. 프로젝트 안에 woff2 가 없다. `DS-gaps.md` #G-01·#G-02.

## 파일 목록

| 경로 | 바이트 | 종류 |
|---|---:|---|
| `DS-gaps.md` | 17,743 | MD |
| `MeetingWorkspace.html` | 1,542 | HTML |
| `MyWork.html` | 1,343 | HTML |
| `SKILL.md` | 875 | MD |
| `_adherence.oxlintrc.json` | 164,555 | JSON |
| `_ds_bundle.js` | 262,144 | JS |
| `_ds_manifest.json` | 118,285 | JSON |
| `components/actions/Button.d.ts` | 677 | d.ts |
| `components/actions/Button3.d.ts` | 437 | d.ts |
| `components/actions/ButtonButton.d.ts` | 804 | d.ts |
| `components/actions/ButtonGroup.d.ts` | 321 | d.ts |
| `components/actions/ButtonIconNormal.d.ts` | 451 | d.ts |
| `components/actions/ButtonIconNormal2.d.ts` | 455 | d.ts |
| `components/actions/ButtonIconSolid.d.ts` | 461 | d.ts |
| `components/actions/ButtonText.d.ts` | 735 | d.ts |
| `components/actions/ButtonText2.d.ts` | 739 | d.ts |
| `components/actions/IconButton.d.ts` | 347 | d.ts |
| `components/actions/actions.card.html` | 3,256 | card HTML |
| `components/avatar/Avatar.d.ts` | 488 | d.ts |
| `components/avatar/Avatar2.d.ts` | 308 | d.ts |
| `components/avatar/AvatarAvatar.d.ts` | 735 | d.ts |
| `components/avatar/AvatarBlock.d.ts` | 344 | d.ts |
| `components/avatar/AvatarGroup.d.ts` | 333 | d.ts |
| `components/avatar/AvatarResourceImageAcademy.d.ts` | 296 | d.ts |
| `components/avatar/AvatarResourceImageCompany.d.ts` | 310 | d.ts |
| `components/avatar/AvatarResourceImagePerson.d.ts` | 320 | d.ts |
| `components/avatar/AvatarResourcePlaceholderAcademy.d.ts` | 314 | d.ts |
| `components/avatar/AvatarResourcePlaceholderCompany.d.ts` | 314 | d.ts |
| `components/avatar/AvatarResourcePlaceholderPerson.d.ts` | 310 | d.ts |
| `components/avatar/avatar.card.html` | 2,325 | card HTML |
| `components/badges/CellResourceTrailingContentBadge.d.ts` | 386 | d.ts |
| `components/badges/ContentBadgeContentBadge.d.ts` | 428 | d.ts |
| `components/badges/PushBadgePushBadge.d.ts` | 385 | d.ts |
| `components/badges/PushBadgePushBadge2.d.ts` | 389 | d.ts |
| `components/badges/badges.card.html` | 2,432 | card HTML |
| `components/calendar/Calendar.d.ts` | 615 | d.ts |
| `components/calendar/CalendarButton.d.ts` | 339 | d.ts |
| `components/calendar/CalendarButton2.d.ts` | 397 | d.ts |
| `components/calendar/CalendarMonthField.d.ts` | 659 | d.ts |
| `components/calendar/CalendarSelectGroup.d.ts` | 245 | d.ts |
| `components/calendar/CalendarYearField.d.ts` | 344 | d.ts |
| `components/calendar/calendar.card.html` | 2,270 | card HTML |
| `components/cards/Card.d.ts` | 412 | d.ts |
| `components/cards/CardGridContentList.d.ts` | 298 | d.ts |
| `components/cards/CardResourceListTrailingContent.d.ts` | 382 | d.ts |
| `components/cards/FramedStyleFramedStyle.d.ts` | 335 | d.ts |
| `components/cards/FramedStyleResourceFrame.d.ts` | 282 | d.ts |
| `components/cards/FramedStyleResourceSelected.d.ts` | 296 | d.ts |
| `components/cards/FramedStyleResourceSlot.d.ts` | 303 | d.ts |
| `components/cards/ProductInfoCard.d.ts` | 364 | d.ts |
| `components/cards/cards.card.html` | 2,113 | card HTML |
| `components/chips/CategoryCategory.d.ts` | 950 | d.ts |
| `components/chips/CategoryResourceChipAlternativeLarge.d.ts` | 557 | d.ts |
| `components/chips/CategoryResourceChipAlternativeNormal.d.ts` | 561 | d.ts |
| `components/chips/CategoryResourceChipAlternativeSmall.d.ts` | 557 | d.ts |
| `components/chips/CategoryResourceChipAlternativeXSmall.d.ts` | 561 | d.ts |
| `components/chips/CategoryResourceChipNormalLarge.d.ts` | 537 | d.ts |
| `components/chips/CategoryResourceChipNormalNormal.d.ts` | 541 | d.ts |
| `components/chips/CategoryResourceChipNormalSmall.d.ts` | 537 | d.ts |
| `components/chips/CategoryResourceChipNormalXSmall.d.ts` | 541 | d.ts |
| `components/chips/ChipChip.d.ts` | 536 | d.ts |
| `components/chips/chips.card.html` | 2,239 | card HTML |
| `components/datetime/DateField.d.ts` | 832 | d.ts |
| `components/datetime/DateField.jsx` | 2,927 | JSX |
| `components/datetime/DatePicker.d.ts` | 764 | d.ts |
| `components/datetime/DatePicker.jsx` | 4,371 | JSX |
| `components/datetime/TimeField.d.ts` | 828 | d.ts |
| `components/datetime/TimeField.jsx` | 4,110 | JSX |
| `components/datetime/datetime.card.html` | 2,826 | card HTML |
| `components/feedback/CircularCircular.d.ts` | 343 | d.ts |
| `components/feedback/DividerDivider.d.ts` | 279 | d.ts |
| `components/feedback/EmptyPage.d.ts` | 205 | d.ts |
| `components/feedback/GradientMask.d.ts` | 323 | d.ts |
| `components/feedback/GradientResourceMaskBase.d.ts` | 265 | d.ts |
| `components/feedback/GradientResourceMaskSize.d.ts` | 397 | d.ts |
| `components/feedback/Info.d.ts` | 185 | d.ts |
| `components/feedback/InteractionLight.d.ts` | 289 | d.ts |
| `components/feedback/InteractionNormal.d.ts` | 293 | d.ts |
| `components/feedback/InteractionStrong.d.ts` | 293 | d.ts |
| `components/feedback/RatioVertical.d.ts` | 262 | d.ts |
| `components/feedback/ScrollBarScrollBar.d.ts` | 438 | d.ts |
| `components/feedback/TooltipResourceMediumArrow2.d.ts` | 327 | d.ts |
| `components/feedback/TooltipResourceMediumArrowHorizontal.d.ts` | 441 | d.ts |
| `components/feedback/TooltipResourceMediumArrowVertical.d.ts` | 433 | d.ts |
| `components/feedback/TooltipResourceSmallArrow2.d.ts` | 323 | d.ts |
| `components/feedback/TooltipResourceSmallArrowHorizontal2.d.ts` | 441 | d.ts |
| `components/feedback/TooltipResourceSmallArrowVertical.d.ts` | 429 | d.ts |
| `components/feedback/TooltipTooltip.d.ts` | 472 | d.ts |
| `components/feedback/feedback.card.html` | 2,771 | card HTML |
| `components/forms/AutoCompleteAutoComplete.d.ts` | 445 | d.ts |
| `components/forms/AutoCompleteResourceItemAction.d.ts` | 289 | d.ts |
| `components/forms/AutoCompleteResourceItemCell.d.ts` | 373 | d.ts |
| `components/forms/AutoCompleteResourceItemTitle.d.ts` | 348 | d.ts |
| `components/forms/CheckboxField.d.ts` | 471 | d.ts |
| `components/forms/CheckboxGroup.d.ts` | 221 | d.ts |
| `components/forms/CheckboxResourceControl.d.ts` | 558 | d.ts |
| `components/forms/CheckboxResourceControl2.d.ts` | 562 | d.ts |
| `components/forms/ControlCheckbox.d.ts` | 487 | d.ts |
| `components/forms/Input.d.ts` | 816 | d.ts |
| `components/forms/RadioResourceControl.d.ts` | 524 | d.ts |
| `components/forms/SelectResourceBackground.d.ts` | 301 | d.ts |
| `components/forms/SelectResourceChip.d.ts` | 295 | d.ts |
| `components/forms/SelectResourceLeadingContent.d.ts` | 417 | d.ts |
| `components/forms/SelectSelect.d.ts` | 562 | d.ts |
| `components/forms/TextinputResourceBackground.d.ts` | 313 | d.ts |
| `components/forms/TextinputResourceInteraction.d.ts` | 300 | d.ts |
| `components/forms/TextinputResourceTextareaLeadingContent.d.ts` | 554 | d.ts |
| `components/forms/TextinputResourceTextareaTrailingContent.d.ts` | 582 | d.ts |
| `components/forms/TextinputTextarea.d.ts` | 696 | d.ts |
| `components/forms/forms.card.html` | 2,866 | card HTML |
| `components/glyphs/ArrowLeft.d.ts` | 205 | d.ts |
| `components/glyphs/ArrowRight.d.ts` | 209 | d.ts |
| `components/glyphs/ArrowRightCircle.d.ts` | 283 | d.ts |
| `components/glyphs/ArrowTr.d.ts` | 197 | d.ts |
| `components/glyphs/ArrowUp.d.ts` | 197 | d.ts |
| `components/glyphs/Bell.d.ts` | 185 | d.ts |
| `components/glyphs/Check.d.ts` | 189 | d.ts |
| `components/glyphs/CheckCircle.d.ts` | 213 | d.ts |
| `components/glyphs/CheckSquare.d.ts` | 213 | d.ts |
| `components/glyphs/ChevronDown.d.ts` | 213 | d.ts |
| `components/glyphs/ChevronLeft.d.ts` | 263 | d.ts |
| `components/glyphs/ChevronRight.d.ts` | 267 | d.ts |
| `components/glyphs/ChevronUp.d.ts` | 205 | d.ts |
| `components/glyphs/Clock.d.ts` | 239 | d.ts |
| `components/glyphs/Emoji.d.ts` | 189 | d.ts |
| `components/glyphs/File.d.ts` | 582 | d.ts |
| `components/glyphs/FileUpload.d.ts` | 372 | d.ts |
| `components/glyphs/IconNormalBlank.d.ts` | 336 | d.ts |
| `components/glyphs/IconNormalCaretDown.d.ts` | 356 | d.ts |
| `components/glyphs/IconNormalCaretUp.d.ts` | 346 | d.ts |
| `components/glyphs/IconNormalCheck.d.ts` | 370 | d.ts |
| `components/glyphs/IconNormalChevronDown.d.ts` | 472 | d.ts |
| `components/glyphs/IconNormalChevronRight.d.ts` | 607 | d.ts |
| `components/glyphs/IconNormalChevronUp.d.ts` | 456 | d.ts |
| `components/glyphs/IconNormalClock.d.ts` | 368 | d.ts |
| `components/glyphs/IconNormalClose.d.ts` | 370 | d.ts |
| `components/glyphs/IconNormalDot.d.ts` | 326 | d.ts |
| `components/glyphs/IconNormalLineHorizontal.d.ts` | 424 | d.ts |
| `components/glyphs/IconNormalStar.d.ts` | 362 | d.ts |
| `components/glyphs/IconsIcons.d.ts` | 252 | d.ts |
| `components/glyphs/IconsIconsResponsive.d.ts` | 318 | d.ts |
| `components/glyphs/LogoWantedPartnershipResourceDivider.d.ts` | 313 | d.ts |
| `components/glyphs/Minus.d.ts` | 189 | d.ts |
| `components/glyphs/Search.d.ts` | 374 | d.ts |
| `components/glyphs/Search2.d.ts` | 197 | d.ts |
| `components/glyphs/Star.d.ts` | 185 | d.ts |
| `components/glyphs/Star2.d.ts` | 189 | d.ts |
| `components/glyphs/Star3.d.ts` | 189 | d.ts |
| `components/glyphs/Text.d.ts` | 202 | d.ts |
| `components/glyphs/TextContentHeading.d.ts` | 341 | d.ts |
| `components/glyphs/TextStrong.d.ts` | 226 | d.ts |
| `components/glyphs/X.d.ts` | 173 | d.ts |
| `components/glyphs/glyphs.card.html` | 2,484 | card HTML |
| `components/icon/Icon.d.ts` | 2,869 | d.ts |
| `components/icon/Icon.jsx` | 23,570 | JSX |
| `components/icon/icon-aliases.js` | 7,694 | JS |
| `components/icon/icon-data.js` | 167,849 | JS |
| `components/icon/icons.card.html` | 1,438 | card HTML |
| `components/kit-assets/fig-assets.css` | 1,768 | CSS |
| `components/lists/CellResourceTrailingContentCheckbox.d.ts` | 419 | d.ts |
| `components/lists/CellResourceTrailingContentIcon.d.ts` | 382 | d.ts |
| `components/lists/CellResourceTrailingContentIcon3.d.ts` | 386 | d.ts |
| `components/lists/CellResourceTrailingContentText.d.ts` | 382 | d.ts |
| `components/lists/CellResourceTrailingContentValue.d.ts` | 314 | d.ts |
| `components/lists/ListCellListCell.d.ts` | 744 | d.ts |
| `components/lists/ListCellResourceLeadingContent.d.ts` | 378 | d.ts |
| `components/lists/ListCellResourceLeadingContentCheckbox.d.ts` | 410 | d.ts |
| `components/lists/ListCellResourceLeadingContentRadio.d.ts` | 398 | d.ts |
| `components/lists/Menu.d.ts` | 185 | d.ts |
| `components/lists/MenuMenu.d.ts` | 325 | d.ts |
| `components/lists/MenuResourceActionArea.d.ts` | 392 | d.ts |
| `components/lists/MenuResourceActionAreaLeading.d.ts` | 374 | d.ts |
| `components/lists/MenuResourceActionAreaLeading3.d.ts` | 378 | d.ts |
| `components/lists/MenuResourceActionAreaTrailing.d.ts` | 378 | d.ts |
| `components/lists/MenuResourceActionAreaTrailing2.d.ts` | 293 | d.ts |
| `components/lists/MenuResourceItemCell.d.ts` | 392 | d.ts |
| `components/lists/lists.card.html` | 2,597 | card HTML |
| `components/misc/IconNormalCircleCheck.d.ts` | 404 | d.ts |
| `components/misc/IconNormalCircleExclamation.d.ts` | 440 | d.ts |
| `components/misc/PageIndicatorResourceDotNormalWhite.d.ts` | 329 | d.ts |
| `components/misc/PageProductResults.d.ts` | 492 | d.ts |
| `components/misc/PaginationDots.d.ts` | 796 | d.ts |
| `components/misc/PaginationResourceDotSmallAdaptive.d.ts` | 325 | d.ts |
| `components/misc/PaginationResourceDotSmallWhite.d.ts` | 313 | d.ts |
| `components/misc/RatioHorizontal.d.ts` | 396 | d.ts |
| `components/misc/SelectField.d.ts` | 818 | d.ts |
| `components/misc/SliderField.d.ts` | 459 | d.ts |
| `components/misc/Social.d.ts` | 1,123 | d.ts |
| `components/misc/Tab5Tabs.d.ts` | 291 | d.ts |
| `components/misc/TabItem.d.ts` | 478 | d.ts |
| `components/misc/Tag.d.ts` | 447 | d.ts |
| `components/misc/TestimonialCard.d.ts` | 229 | d.ts |
| `components/misc/TextHeading.d.ts` | 230 | d.ts |
| `components/misc/TextinputResourceTextfieldButton.d.ts` | 620 | d.ts |
| `components/misc/TextinputResourceTextfieldTrailingContent.d.ts` | 532 | d.ts |
| `components/misc/TextinputTextfield.d.ts` | 681 | d.ts |
| `components/misc/ThumbnailResourceOverlayCustom.d.ts` | 289 | d.ts |
| `components/misc/ThumbnailThumbnail.d.ts` | 332 | d.ts |
| `components/misc/fig-assets.css` | 584 | CSS |
| `components/misc/misc.card.html` | 2,489 | card HTML |
| `components/navigation/Breadcrumb.d.ts` | 479 | d.ts |
| `components/navigation/NavArrowDown.d.ts` | 217 | d.ts |
| `components/navigation/NavArrowLeft.d.ts` | 217 | d.ts |
| `components/navigation/NavArrowRight.d.ts` | 221 | d.ts |
| `components/navigation/NavMenu.d.ts` | 435 | d.ts |
| `components/navigation/Navigation.d.ts` | 668 | d.ts |
| `components/navigation/NavigatorAlt.d.ts` | 217 | d.ts |
| `components/navigation/PageControlHorizontal.d.ts` | 753 | d.ts |
| `components/navigation/PageControlItem.d.ts` | 313 | d.ts |
| `components/navigation/PageHeader.d.ts` | 355 | d.ts |
| `components/navigation/PageIndicatorResourceDotNormal.d.ts` | 309 | d.ts |
| `components/navigation/SegmentedControlResourceKnob.d.ts` | 318 | d.ts |
| `components/navigation/SegmentedControlSegmentedControl.d.ts` | 466 | d.ts |
| `components/navigation/TabResourceTab.d.ts` | 373 | d.ts |
| `components/navigation/TabTab.d.ts` | 871 | d.ts |
| `components/navigation/navigation.card.html` | 2,598 | card HTML |
| `components/shell/AppShell.d.ts` | 1,158 | d.ts |
| `components/shell/AppShell.jsx` | 1,550 | JSX |
| `components/shell/SideNav.d.ts` | 1,215 | d.ts |
| `components/shell/SideNav.jsx` | 2,655 | JSX |
| `components/shell/shell.card.html` | 2,196 | card HTML |
| `components/shell/shell.css` | 10,240 | CSS |
| `components/work/AiChatSidebar.d.ts` | 528 | d.ts |
| `components/work/Frame589.d.ts` | 577 | d.ts |
| `components/work/InboxNotice.d.ts` | 637 | d.ts |
| `components/work/InboxTask.d.ts` | 839 | d.ts |
| `components/work/MODCreateTask.d.ts` | 775 | d.ts |
| `components/work/Reply.d.ts` | 569 | d.ts |
| `components/work/TaskCard.d.ts` | 826 | d.ts |
| `components/work/TaskTable.d.ts` | 859 | d.ts |
| `components/work/WorkCalendar.d.ts` | 817 | d.ts |
| `components/work/WorkSpace.d.ts` | 227 | d.ts |
| `components/work/work.card.html` | 1,984 | card HTML |
| `design_handoff_my_work/README.md` | 19,185 | MD |
| `ds-token-report.md` | 79,435 | MD |
| `guidelines/brand-agent.card.html` | 1,747 | card HTML |
| `guidelines/brand-chrome.card.html` | 1,838 | card HTML |
| `guidelines/brand-wordmark.card.html` | 1,492 | card HTML |
| `guidelines/colors-accent.card.html` | 1,872 | card HTML |
| `guidelines/colors-brand-grey.card.html` | 1,860 | card HTML |
| `guidelines/colors-dark.card.html` | 1,971 | card HTML |
| `guidelines/colors-ink.card.html` | 1,739 | card HTML |
| `guidelines/colors-lines.card.html` | 1,999 | card HTML |
| `guidelines/colors-neutral.card.html` | 1,965 | card HTML |
| `guidelines/colors-status.card.html` | 1,679 | card HTML |
| `guidelines/colors-surface.card.html` | 1,714 | card HTML |
| `guidelines/spacing-elevation.card.html` | 1,653 | card HTML |
| `guidelines/spacing-interaction.card.html` | 5,943 | card HTML |
| `guidelines/spacing-radii.card.html` | 2,011 | card HTML |
| `guidelines/spacing-scale.card.html` | 2,121 | card HTML |
| `guidelines/spacing-scrollbar.card.html` | 2,421 | card HTML |
| `guidelines/type-display.card.html` | 950 | card HTML |
| `guidelines/type-ramp.card.html` | 1,438 | card HTML |
| `guidelines/type-weights.card.html` | 1,315 | card HTML |
| `handoff/meetings/css/meetings.css` | 8,687 | CSS |
| `handoff/meetings/css/workspace.css` | 11,497 | CSS |
| `handoff/meetings/js/data.js` | 5,740 | JS |
| `handoff/meetings/js/workspace-data.js` | 5,870 | JS |
| `handoff/meetings/js/workspace.v1.jsx` | 22,900 | JSX |
| `handoff/my-work/README.md` | 6,515 | MD |
| `handoff/my-work/css/components.css` | 37,976 | CSS |
| `handoff/my-work/js/data.js` | 8,238 | JS |
| `handoff/my-work/js/my-work.v2.jsx` | 21,005 | JSX |
| `handoff/shell/js/nav.js` | 907 | JS |
| `handoff/shell/js/scax-ui.jsx` | 9,629 | JSX |
| `handoff/shell/js/work-modal.jsx` | 11,507 | JSX |
| `styles.css` | 368 | CSS |
| `support.js` | 69,150 | JS |
| `templates/work-home/ds-base.js` | 904 | JS |
| `tokens/fig-tokens.css` | 29,611 | CSS |
| `tokens/fig-typography.css` | 42 | CSS |
| `tokens/fonts.css` | 854 | CSS |
| `tokens/product.css` | 3,707 | CSS |
| `tokens/scax.css` | 5,355 | CSS |
| `tokens/scrollbar.css` | 2,447 | CSS |
| `tokens/typography.css` | 3,342 | CSS |
| `ui_kits/work/README.md` | 1,859 | MD |
| `ui_kits/work/index.html` | 1,298 | HTML |

**파일 278개 · 합계 1,325,481 B**
