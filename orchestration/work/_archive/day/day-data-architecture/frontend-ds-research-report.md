# 시술 현황 시안: medikit 대조 (DS gap 조사)

- 작성: day frontend 워커 · 2026-11-05 · task_e281fee9db7c
- 성격: 읽기 전용 조사. 코드 · 문서 · 시안은 고치지 않았다.
- 상태: done

## 0. 대조 기준 (먼저 읽을 것)

| 기준 | 위치 · 버전 | 비고 |
|---|---|---|
| 시안 | `reference/2026-11-03-cc-day/screen/시술현황_프로토타입 (1).html` (1828줄). 화면 안 버전 표기는 「3차 v11」 | 아래 `L숫자`는 이 파일의 줄 번호다. data URI만 지운 사본에서도 줄 번호가 같다. |
| medikit React (**실제 대조 기준**) | `@medisolve-ai/medikit` **1.4.0** 배포본: `~/orca/workspaces/agency-settlement/agency-settlement/front/node_modules/@medisolve-ai/medikit/dist/index.{d.ts,js}` · `styles/base.css` | cc-prototype `procedure/front/package.json` 이 쓰는 버전과 같다. 아래 `mk.js:줄`, `mk.d.ts:줄`은 이 dist 파일의 줄 번호다. |
| medikit 원본 레포 | `/Users/kknaks/git/medikit` (main `55c14a2`, **package 0.3.0**) | **오래됐다.** Badge · Chip · Card · Banner · Accordion · Progress 가 없고, Button 크기도 lg50/md48/sm33뿐이다. 브리프가 가리킨 레포지만 기준으로 쓰지 않았다(§6). |
| HTMX 키트 | centurion `origin/main` `5f150c0`: `docs/development/medikit-htmx-kit/{README.md,medikit.css,medikit.js}` · `medikit-htmx-design-guide.md` | 키트는 「medikit 1.3.0 기준」이라고 적혀 있다. |
| admin 매크로 | centurion `origin/main:backend/admin/templates/ui.html` (74줄) | `btn` · `input_box` · `badge` · `chip` · `banner` · `card` · `table`만 있다. |

시안 머리 주석(L24, L26)에 따르면 시안 값의 출처는 **Figma 메디킷**(「Brand = crm 모드」, Tab List, More Menu Panel, EmptyState, ComboBox 78:1301)이다. 시안이 「메디킷 ○○」이라고 부르는 부품 상당수는 **Figma 에만 있고 코드 medikit(1.4.0)과 HTMX 키트에는 없다.** 이 리포트의 「없음」은 코드 기준이다.

## 1. 요약

화면 구성 요소는 E01~E56, 56개다(E57 은 E12 와 같아서 세지 않았다). 프로토타입 확인 도구 2개(관점 선택 · 버전 상자, L477-483 · L769-781)는 「디자인 일부 아님」(L477)이라 뺐다.

| 판정 | 개수 | 뜻 |
|---|---|---|
| ○ 있음 | **7** | medikit 컴포넌트 · 키트 클래스를 그대로 쓰면 된다 |
| △ 비슷 | **20** | 가까운 컴포넌트는 있지만 치수 · 모양 · 동작이 다르다(차이를 표에 적었다) |
| ✗ 없음 (DS gap) | **20** | 대응하는 것이 없다. 요소 20개가 gap 17종(§3 G1~G17)으로 묶인다 |
| ― 조합 | **9** | 컴포넌트가 필요 없다. 토큰(글자 · 색 · 간격) 조합으로 만든다 |

판정은 React 1.4.0 기준이다. React 에는 있고 HTMX 에만 없는 것은 「△(React) / HTMX ✗」처럼 적고 React 쪽 판정으로 셌다.

**HTMX 에서 따로 빠지는 것:** React 1.4.0 에서는 ○ · △ 이지만 HTMX 키트 · `ui.html` 에는 없는 것이 6개 있다.
Tooltip, Popover(더보기 메뉴 · 의사 고르기 · 방 고르기), ComboBox 목록, Accordion(접는 칸), Notify(토스트), Checkbox 혼합 상태.
키트 README L45 · 가이드 §10 은 「Radix 기반 Popover · Select · Accordion 은 옮기지 않았다, 네이티브로 대신한다」고 적고 있다. 그래서 DAY 에서는 이 6개도 **새로 만들어야 한다.**

**가장 큰 gap:**

1. **CRM 브랜드 · 상태 색.** medikit 1.4.0 의 `[data-product]` 에 crm 이 없다. 고객 상태 7색 × 4단계 팔레트(L36-42)도 없다.
2. **CRM 셸.** 아이콘 줄 46px · 헤더 44px · 페이지 머리 줄이 medikit 셸(274px 사이드바 · 57px 헤더)과 치수가 전혀 다르다.
3. **밀집 카드 계열.** 방 카드 · 인박스 카드 · 시술 행 · 사각 상태 배지에 맞는 것이 없다.
4. **실시간 타이머.** `+mm:ss` 를 1초마다 다시 그린다(L1784-1787).
5. **팝오버류 전부.** HTMX 키트에 없다.

## 2. 요소별 표

열 설명: **React** = medikit 1.4.0 컴포넌트(props) · **HTMX** = 키트 클래스 / `ui.html` 매크로 · **판정** ○/△/✗/― · gap 번호는 §3.

### 2-1. 화면 틀 (셸)

| # | 요소 · 위치 · 상태 | 시안 근거 | React 1.4.0 | HTMX 키트 / ui.html | 판정 |
|---|---|---|---|---|---|
| E01 | 앱 틀: 네이비(#000a14) 바탕 위에 흰 main(왼쪽 모서리 8). 최소 1280×720 | L83, L95, L657-662 | 없음. `Menu`(사이드바)·`Header` 는 따로 있다 | `ms-app` · `ms-body` · `ms-main` (흰/회색 바탕, 모서리 없음) | ✗ **G1** |
| E02 | 아이콘 줄(rail) 46px: 항목 38×38, 아이콘 16 + 글 10/500. 기본은 흰 42% 투명, 현재 메뉴만 100%. 메뉴는 홈·예약·고객·시술·매출·설정 | L86-93, L657-659, L718-722 | `Menu` (open=false 면 폭 76 · 항목 40×40 · 아이콘만 · 현재 메뉴 bg-primary-100) mk.js 메뉴부 / 0.3.0 `menu.tsx:120-231` | `ms-side`(274) · `ms-nav__item`(40h) | ✗ **G1** |
| E03 | 헤더 바 44px: 좌우 16 · 간격 24 · 구분선 없음 | L97-98 | `Header` (57h · px42 · 메뉴 간격 70 · 아래 선) 0.3.0 `header.tsx:94-130` | `ms-header` (57h · px42) | △ 높이 · 간격 · 구성이 다르다 → G1 |
| E04 | 병원 이름 + 꺾쇠 12 (12/500 secondary). 지점 바꾸기 트리거로 보이지만 동작은 없다 | L99, L724 | 없음(`ChevronIcon` 만 있음) | 없음 | ― 조합 (동작은 시안에 없다) |
| E05 | 헤더 탭(예약 현황/원내 현황/시술 현황): 14/500 gray-600. 선택 탭은 primary + 밑줄 3(모서리 3) · 간격 16 · 아래 4 | L100-104, L669-670, L725 | `Tabs{tabs,selectedTab,onSelectTab,disabled}`: 16px(heading-md 400→500) · 간격 42 · 아래 16 · 밑에 1px 회색 선 (mk.js:4637-4690) | `ms-tab` (브라우저 탭 모양, 32h, 위 모서리 14) | △ 같은 밑줄 탭이지만 글자 14 · 간격 16 · 아래 4 · 바닥선 없음 → G2 |
| E06 | 헤더 고객 검색 200×28 (모서리 4, 돋보기 오른쪽) | L106-108, L110-120, L726 | `Input{size:'xl'50|'l'44|'m'36, icon, allowClear}` (mk.d.ts:186-207). **28 없음** | `ms-input--m` 36 / `ui.input_box('m')` 36 | △ 28 높이 없음(시안 주석에도 「차이표 ②」 L106) |
| E07 | 페이지 머리 줄: 「시술 현황 \| 2026-10-26 (월)」 16/600 secondary, 세로 구분선 1×12 gray-300, min-h 32 | L122-124, L729-738, L760 | `Divider{direction:'vertical'}` (mk.d.ts:241-247) + `text-typo-heading-md-600` | `ms-page__head` (20/700, 패딩 24/28, 세로 배치), 맞지 않음 | △ Divider + typo 조합으로 된다. 키트 page head 는 맞지 않는다 |
| E08 | 날짜 이동: 꺾쇠 20 아이콘 버튼 + [오늘]. **이 화면에서는 꺼져 있다**(dateNav=false, L760) | L125-127, L731-736 | `Button variant=icon` + `ChevronIcon`; [오늘] = `Button variant=outlined color=black size=ss` | `ui.btn(?, 'ss')`. outlined-black 변형이 **없다** | △ (이 화면은 날짜 글자만 쓴다) |
| E09 | [필터] 아이콘 버튼 28×28 (Outlined Black SS, 깔때기 12) + 툴팁 「필터」 | L129-131, L760 | `Button outlined black ss` + 폭 28 (default ss 는 px8 · 정사각 프리셋 없음. circle ss 는 둥글다) | `ms-btn--ss`. outlined black 없음 · 아이콘 전용 없음 | △ 정사각 아이콘 버튼 프리셋 없음 |
| E10 | 보기 바꾸기 세그먼트 164×28: 의사별 / 4층 / 미사용. 바탕 gray-200, 고른 칸은 흰 면 + 그림자, 12px. 거르는 동작은 아직 없다(L1821) | L132-136, L760, L1821-1825 | **없음**(시안은 「메디킷 Tab List」라 부르지만 Figma 에만 있다) | 없음(`ms-chip` 은 36h 알약이라 다르다) | ✗ **G2** |
| E11 | 툴팁(CSS `[data-tip]` · 떠 있는 `.ftip`): 여백 5/8 · 모서리 6 · 12/500 흰 글자 · 면 rgba(34,41,67,.7) · 꼬리 14×6 · 0.1초 지연 | L184-196, L575-577, L652, L1807-1820 | `Tooltip/TooltipContent`: px16 py10 · 14px(heading-sm-400) · 면 `ms-hover-dark/70` · **꼬리 없음** (mk.js:1855-1868) | 없음 | △(React) / HTMX ✗ → **G3** |
| E12 | 알림 토스트: 위 가운데 흰 알약 · primary 글자 + 체크 18 · 13/500 · 그림자 primary 30% · 2초 | L286-290, L739-748, L1330 | `Notify{variant:'success', size:'sm'}` gap8 · px16 py14 · 13px (0.3.0 `notify.tsx:21-42`). `notify.success()`(react-toastify, top 103) | **없음**(`ui.banner` 는 화면 안 띠다) | ○(React) / HTMX ✗ (CSS 는 Notify sm 을 옮기면 된다) |
| E13 | 포커스 링 2px primary | L247 | 각 컴포넌트 focus 스타일 | `.ms-btn:focus-visible` 2px primary (medikit.css:52) | ○ |
| E14 | 스크롤바 5px | L77-81 | base.css (thumb gray-300) | 없음 | △ thumb 이 rgba(0,0,0,.1)/.2 로 다르다 (시안 주석은 「base.css 그대로」라고 적었지만 값이 다르다) |

### 2-2. 왼쪽: 인박스 (현황 · 호출 · 시술 완료)

| # | 요소 · 위치 · 상태 | 시안 근거 | React 1.4.0 | HTMX | 판정 |
|---|---|---|---|---|---|
| E15 | 인박스 칸: 폭 280 · 흰 바탕 · 오른쪽 선 · 세로 스크롤 | L248-249, L369 | ― | `ms-side` 274 비슷 | ― 조합 (레이아웃) |
| E16 | 인박스 탭: 현황 / 호출 n / 시술 완료 n. 14/400, 고르면 600 primary, 밑줄 2 · 간격 24 · sticky. `.tab-dot`(빨간 점)은 CSS 만 있고 쓰지 않는다 | L170-174, L259, L669, L982-988 | `Tabs` (16px · 간격 42 · 밑줄 3) | 없음 | △ → G2 (밑줄 2 · 14px · 600) |
| E17 | 접는 칸 머리: 아이콘 16(warn-fill / circle-check / circle-minus) + 제목 14/500 secondary + 꺾쇠 20(접으면 -90°). 칸은 0fr↔1fr 로 220ms 접힌다. 호출 탭은 「수락 대기 n · 수락함 n」(아이콘 없음), 시술 완료 탭은 방 이름 + 개수(disabled 색) | L254-258, L261-267, L294, L518, L706-710, L998-1004, L1054-1060, L1449-1455 | `Accordion/AccordionItem/Trigger/Content` (size lg/md, Radix) mk.d.ts:24-35 | 없음 (가이드 §10: `<details>` 로 대신) | △(React) / HTMX ✗ → **G4** |
| E18 | 인박스 카드(crm-card): 머리 면 줄(#f7f7f8, 방 이름 12/500 + 시간 배지) + 본문(패딩 8). 테두리 gray-300 · 모서리 6 · 그림자. 상태: 기본 / hover 1px 뜸 + 테두리 gray-500 / **선택** 1px primary + 3px 번짐 / **선택+늦음** 빨강 번짐 / **새로 늦음** 1.2초×2 빨강 깜빡임 / 다른 방 선택 시 흐려짐 0.88 | L268-276, L365-366, L385-397, L492-502, L663-664, L672-673, L692-703, L962-981 | `Card{interactive,selected,indicator,corner,padding}`: 모서리 12 · 테두리 gray-300 · 선택은 primary 면 + 체크 배지 (mk.js:915-950) | `ms-card` (모서리 12 · p20) / `ui.card` | ✗ **G5** (머리 면 줄 · 6 모서리 · 번짐 선택 · 깜빡임이 없다) |
| E19 | 카드 줄: 아이콘 16 + 고객 이름 12 + 현지 발음 12/500 tertiary | L277-281, L696-698, L960 | ― | ― | ― 조합 |
| E20 | 원장 줄: 청진기 16 + 원장 이름(없으면 「전체 의사」) + 상태 글자(「수락」 brand / 「호출 +mm:ss」, 5분 넘으면 빨강) + 「· 재호출 +mm:ss」 | L370-375, L530-532, L950-957 | ― | ― | ― 조합 (시간 글자는 G13) |
| E21 | 「○○ 응답 없음」 줄 (disabled 색) | L374, L532, L957 | ― | ― | ― 조합 |
| E22 | 카드 안 [재호출] 버튼 (Outlined Gray SS, 응답 없는 호출 카드에만) | L161-162, L966-976 | `Button outlined gray ss` | `ui.btn('gray','ss')` | ○ |
| E23 | 호출 탭 카드: 방 > 고객 > 시술 점 목록(3px 점) > 원장 줄 + [수락](Solid SS) | L398-400, L678-679, L1034-1053 | 버튼은 `Button solid blue ss` | `ui.btn('primary','ss')` | ○ (버튼) · 점 목록은 ― 조합 |
| E24 | 시간 배지(cbadge): 11/500 · 자간 .34 · 패딩 3/6 · 모서리 6 · tabular-nums. **solid**(면 8%): primary(마취 진행) / red(넘김) / gray(대기 · 귀가) / going-wait(귀가 대기 초록). **outline**(테두리 43%): primary(마취 시작) | L175-183, L200-206, L454, L556, L665, L949, L953, L1438 | `Badge{variant: neutral|primary|warning|danger|purple, size md 28 / sm 24, dot}`: **알약(rounded-full)** · 12/10px · 면 = -100 단계 (mk.js:834-870) | `ui.badge(variant,size)` 같은 값 · `ms-badge` | ✗ **G6** (사각 · 11px · 22h · 8% 면 · outline 변형 · 상태 색이 없다) |
| E25 | 시술 완료 탭 검색: Input m + 입력 지우기(X) + 돋보기 · sticky | L520-523, L1446 | `Input{size:'m', allowClear, icon}` | `ui.input_box('m')`. 지우기 버튼 없음 | ○(React) / HTMX △ (X 버튼을 손으로) |
| E26 | 찾은 글자 표시 `<mark>` (yellow-300 면 · 모서리 2) | L521, L1429-1432 | 없음 (토큰 `--ms-yellow-300` 은 있다) | 없음 (키트 css 에 yellow-300 없음, 가이드 §4-1 에는 있음) | ✗ **G7** (작다, 토큰만으로 된다) |
| E27 | 빈 상태: 「조건에 맞는 고객이 없어요」 18/600 + 20 + [조건 지우기] Outlined Gray M(36). 바탕 · 테두리 없음 · min-h 380 | L524-527, L1447 | `TableScrollAreaEmpty` (표 전용) | `ms-empty` (테두리 · 패딩 48 · 회색 글자) | △ 시안은 Figma EmptyState: 테두리 없음 · 제목 + 버튼 |
| E28 | 시술 완료 카드: 머리 = 「입실-귀가」 시간 + 배지(귀가 = gray / 귀가 대기 = going-wait). 본문 = 이름 + 시술 줄들. 차트 열림 중이면 선택 테두리 | L517-519, L557-564, L1433-1441 | Card | ms-card | ✗ → G5 · G6 |
| E29 | 시술 링크 줄: 점 + 시술 이름(말줄임) + 차트 아이콘 2개. hover subtle 면 · 모서리 6. 누르면 차트 모달 | L460-463, L559-564, L1435 | ― | ― | ― 조합 (아이콘은 G8) |
| E30 | 차트 아이콘: 간호(square-pen) · 의사(stethoscope) on(파랑)/off 16, 툴팁 「간호관리차트」·「의사차트」 | L1465-1471, `assets/chart-*-on/off.svg` (L8) | 없음 | 없음 | ✗ **G8** |

### 2-3. 오른쪽: 보드 · 방 카드

| # | 요소 · 위치 · 상태 | 시안 근거 | React 1.4.0 | HTMX | 판정 |
|---|---|---|---|---|---|
| E31 | 보드: 바탕 #e3e3e5, 그리드 auto-fill(최소 256, 한 줄 최대 5) · 간격 8 · 패딩 10 | L250, L304-308, L668, L704 | ― | ― | ― 조합 (레이아웃, 바탕 색은 §4) |
| E32 | 방 카드(room3): 모서리 6 · 테두리 없음 · 그림자 0 2 4 -2 · 높이 = max(320, (100dvh−117)/2). 상태: 기본 / hover 1px 뜸 / **선택**(1px primary + 4px 번짐, 연결 방은 둘 다) / **선택+늦음**(빨강) / **다른 방 선택 시 0.7** / **드래그 중**(z3 + 0 6 16 그림자) / **has-selection** · **is-going**(아래 바 공간 56) / **빈 방** / **연결 원래 방(held)** | L309-312, L343, L355-363, L385-395, L404-408, L466-467, L488, L498-514, L628-633, L1199-1232, L1790-1793 | `Card` | `ms-card` | ✗ **G5** |
| E33 | 방 머리 줄: #f7f7f8 면 · min-h 31 · 패딩 5/10 · 간격 6. [손잡이 16][경고 16][방 이름 버튼 12/500 → 방 옮기기]……[마취 칩] | L313-314, L340, L377-382, L409, L453, L505, L615-617, L1213-1215 | ― | ― | ✗ → G5 (카드 머리 면 줄) |
| E34 | 방 순서 손잡이(grip-vertical 16, gray-500→tertiary) + **끌어서 순서 바꾸기**(pointer, 놓기 전 자리 미리 바뀜, 260ms 잠금) + 화살표 키 | L315-321, L401-405, L792-793, L1722-1762 | 아이콘 버튼은 `Button variant=icon`. 끌기 동작은 없음 | 없음 (medikit.js 에 끌기 없음) | ✗ **G9** |
| E35 | 경고 아이콘 16 (warn-fill: 빨간 원 + 흰 !) · 「확인 필요」 칸 머리 · 늦은 방 이름 앞 | L489-490, L1012, L1214 | `WarningIcon` (모양 확인 안 함) | `ui.banner` danger 의 원형 ! svg (빨강/red-300) | △ 비슷한 아이콘은 있다. 같은 그림인지 확인 못 함(§6) |
| E36 | 마취 칩 버튼(한 버튼 세 상태): ① outline primary 「마취 시작」 → ② solid primary 「마취 +mm:ss」(20분 넘으면 red, 툴팁 「마취 종료」) → ③ solid gray 「마취 완료 nn분」(툴팁 「마취 재시작」). hover 면 · 누르면 0.97 | L412-413, L453-454, L1180-1190, L1706-1709 | 없음 (Badge 는 span, 버튼 아님) | 없음 | ✗ → G6 + G13 |
| E37 | 고객 줄 버튼: 이름 14/600 + 현지 발음 12/500 secondary. hover 면 gray-200(바깥 4px). 누르면 차트 화면(아직 없음) | L297-300, L383, L444-447, L506, L537, L1218, L1671-1672 | `Button variant=text` 비슷 | `ui.btn('text')` (패딩 0, hover 글자색만) | ― 조합 (hover 면 링크) |
| E38 | 바이탈 줄: 성별 \| 만 나이 \| 입실 hh:mm (12 tertiary, 구분선 1×10) | L301-302, L536, L1219 | `Divider{direction:'vertical'}` | ― | ― 조합 |
| E39 | 오더 메모(읽기 전용): 왼쪽 2px gray-500 선 · 10px(meta-sm-400) · pre-line · **5줄(67px) 넘으면 잘리고** 오른쪽 아래 [크게 보기 maximize-2 16] → 제자리 펼침 | L333-338, L415-417, L538-542, L568-569, L1221, L1704-1705 | 없음 | 없음 | ✗ **G10** |
| E40 | 전체 선택: 체크박스 + 「전체 선택」 12 tertiary. 상태: 비선택 / **혼합(−)** / 전체 / **꺼짐**(고를 시술 없음) | L138-147, L212-213, L450-457, L570-571, L1191-1198 | `Checkbox` (Radix; checked/disabled. 혼합 표시는 CheckIcon 만 그려서 없다, mk.js:2671-2690) | `ms-checkbox` (`:checked` · `:disabled` 만) | △ 혼합(−) 상태 없음 → **G11** |
| E41 | 시술 줄(proc3): [상태 칸 16][이름 14 + 메타 12(원장 · 상태 글자)][시간 칸][액션 버튼][더보기]. 모서리 0 · 패딩 4/8. 상태: **준비중**(체크박스) / **호출**(꺼진 체크박스 · 「호출」 brand, 늦으면 red) / **수락** / **진행중** / **완료**(아래 칸, 회색 완료 아이콘 · 이름 tertiary · 「⏱ nn분」, 시작-끝 title). hover · 메뉴 열림 = primary-100 면. 누르면 차트 모달(버튼 · 체크박스 제외) | L418-432, L543-555, L565-574, L1127-1165, L1606-1611 | 없음 | 없음 | ✗ **G12** |
| E42 | 꺼진 체크박스(준비중이 아닌 줄) | L552, L1141 | `Checkbox disabled` | `ms-checkbox:disabled` | ○ |
| E43 | 시간 칸: 시계 12 + 「30초」·「nn분」(진행중 · 호출 · 완료). 호출 5분 넘음 · 재호출 = red (아이콘은 CSS filter 로 빨갛게) | L433-437, L553-555, L1166-1179 | 없음 | 없음 | ✗ **G13** |
| E44 | 줄 액션 버튼 **24h**: [종료] Outlined Black / [시작] Solid / [수락] Outlined Black | L430, L1156-1158 | `Button` 최소 ss 28 | 최소 `ss` 28 | △ 24 높이 없음 (패딩 4/8) |
| E45 | 더보기 버튼(ellipsis-vertical 16): 평소 폭 0 → 줄 hover · 포커스 · 메뉴 열림이면 오른쪽에서 밀며 나타남. 진행중 · 완료 줄만 | L438-443, L796-797, L1142-1143 | `MoreIcon` (아이콘만) | ― | △ 아이콘 ○ · 나타남 동작은 G12 |
| E46 | 방 아래 호출 바: 흰 그라데이션 위 [n개 호출](Solid M) 또는 [귀가 대기](Filled M). 고르면 아래에서 8px 올라옴(160/220ms) | L342-356, L1207-1209, L1227-1230 | 버튼은 `Button solid/filled size m` | `ui.btn('primary'|'filled','input')` (36) | 버튼 ○ · 떠오르는 바는 ✗ **G14** |
| E47 | 옮겨 온 방 연결 줄(link-bar): primary 면 · 흰 글자 12/500 · link 아이콘 16 · 원래 방 이름 · [연결 풀기][돌아가기](primary 면 소형 버튼 2/4, hover rgba(0,0,0,.12)) | L618-624, L1366 | 없음 | `ui.banner` 는 연한 면 · 화면 안 알림용이라 다르다 | ✗ **G15** |
| E48 | 연결 원래 방(held): 제목 줄 「시술실 A → 레이저실 1」(화살표 brand 링크) · 고객 · 메모 30% 흐림 · hover 하면 가운데 [연결 풀기][돌아오기](Filled Gray S 33) | L625-634, L1367-1382 | `Button variant=filled color=black` (gray-200 면 · 검정 글자) | `ui.btn` 에 filled-gray 없음 | ✗ → G15 (버튼은 △: 글자 gray-700 · disabled 처리 다름, L674-676) |
| E49 | 빈 방: 머리 줄만, 바탕 subtle | L465-467, L504, L1404-1411 | Card | ms-card | ✗ → G5 상태 |

### 2-4. 떠 있는 것 (팝오버 · 모달 · 확인 창)

| # | 요소 | 시안 근거 | React 1.4.0 | HTMX | 판정 |
|---|---|---|---|---|---|
| E50 | 더보기 메뉴(More Menu Panel): 폭 200 · 모서리 12 · 패딩 6 · 메뉴 줄 36(14/400, 모서리 8, hover subtle) · 구분선. 항목은 「시작 취소」/「완료 취소」 하나 | L207-215, L1233-1248 | `Popover/PopoverContent`(모서리 8 · shadow-pop-over · p16); `ActionButton`(줄 43h × 57w, 상세/삭제 고정) | 없음 | △(React) / HTMX ✗ → **G16** |
| E51 | 재호출 / 수락할 원장 팝업: 폭 240 · 최대 380 · 모서리 8 · 그림자 0 0 4 #cfcfcf. 머리(14/600 + X 16) · 검색 · 라벨 「선택됨」·「전체」 10/500 · 옵션 줄 32(아바타 24 + 이름 12/500 + 상태 10 「비어 있음」(primary)/「○○ 시술 중」 + 꼬리표 「처음 호출」·「호출」 10/500 primary) · 선택 줄 primary-100 · 하단 [재호출]/[수락] Solid M(33) 꽉 참, 안 고르면 꺼짐 | L217-245, L1064-1101, L1627-1634, L1656-1662 | `ComboBox{hasSearch, renderOption}` · `Command*`: 트리거가 붙은 드롭다운이다. 머리 · 하단 버튼이 있는 창은 아님 | 없음 | △(React) / HTMX ✗ → G16 |
| E52 | 의사 아바타(이니셜 2자 · 24 원 · 10/500): tone 0 primary / 1 보라 / 2 연두 + 한 단계 옅은 테두리. 「전체 호출」은 회색 원 + 사람 아이콘 | L328-331, L471-475, L886-891, L1078 | 없음 | 없음 | ✗ **G17** |
| E53 | 방 옮기기 목록(ComboBox M 펼친 목록): 폭 200 · 최대 높이 220 · 옵션 44(패딩 11/16 · 14) · hover gray-100 · **꺼진 줄**(사람 있는 방) · **선택 줄** primary-100 + 500 + 오른쪽 체크 16 · 고르면 아래에서 [방 옮기기]/[돌아가기] Solid M 올라옴(200ms) | L635-649, L1383-1393, L1635-1644 | `ComboBox{size:'m', options[{disabled}], hasCheckIcon}`: 트리거 36 · 옵션 min-h 50 p15 (mk.js:2031) | 없음 (네이티브 `<select>`) | △(React: 옵션 44가 아니라 50, 하단 버튼 없음) / HTMX ✗ → G16 |
| E54 | 확인 창(작은 창): 280 · 모서리 14 · 패딩 20 · 제목 16/500 · 설명 14 tertiary · [취소] Outlined Gray / [확인] Solid (36, 모서리 6). 쓰는 곳: 저장 안 하고 닫기 · 진행 중 방 옮기기 · 연결 풀기 | L608-613, L650-651, L1290-1291, L1394-1403, L1643, L1653 | `ConfirmModal{title,description,variant,leftButton,rightButton}`: min-w 444 · 모서리 20 · p26 · 제목 title-sm-600 · 버튼 lg (mk.js:1777-1830) | `ms-modal` 560 · 모서리 16 | △ 크기 · 모서리 · 글자 · 버튼 크기가 다르다 |
| E55 | 차트 모달: 410 · 최대 min(640, 100dvh−48) · 모서리 14 · 그림자 float. 머리(18/500 「이름 발음」 + X 24) · 직무 탭(간호 관리 차트 / 의사 차트, 16 · 밑줄 3 · ←→ 키) · 시술마다 섹션(제목 14 + 메타 「✎ 작성자 \| hh:mm 작성/수정」 12) + Textarea · 누른 시술 섹션은 2.4초 primary-100 두 번 깜빡임 · 하단 「Ctrl + Enter」 + [저장] Button L(44) | L578-607, L1265-1331, L1680-1690, L1770-1777 | `Modal`(모서리 20 · p26) / `Dialog*` + `Tabs` + `Textarea` | `dialog.ms-modal`(560 · 모서리 16 · 머리/본문/하단) | △ 틀은 ms-modal 을 고치면 된다. 모서리 14 · 폭 410 · 그림자 · 깜빡임이 다르다 |
| E56 | 차트 글 칸(Textarea): 모서리 8 · gray-300 · 패딩 16 · body-400 · **높이 90→150 자동으로 늘어남**(`field-sizing: content`) | L597-600 | `Textarea` (p-4 · 모서리 8 · body-400) | 키트에 textarea 클래스 없음 (input 만) | ○(React) / HTMX △ (자동 높이는 Chromium 계열에서만 됨, §6) |
| E57 | 「저장되었어요」 토스트 | L1330 | E12 와 같음 | E12 와 같음 | (E12 에 포함, 세지 않음) |

> 세는 법: E57 은 E12 와 같은 것이라 세지 않았다. E46 · E23 처럼 「버튼 ○ + 틀 ✗」인 칸은 **판정이 낮은 쪽**으로 셌다(E46 = ✗, E23 = ○: 점 목록은 조합이다).

## 3. DS gap 상세

「토큰만으로」 열의 뜻: **예** = medikit 토큰(색 · typo · 그림자)만으로 그릴 수 있다 / **아니오** = 새 색 · 치수 · 글자 크기가 필요하다.

### G1. CRM 셸 (아이콘 줄 46 · 헤더 44 · 둥근 main) — E01 · E02 · E03
- **생김새**: 왼쪽 46px 네이비(#000a14) 아이콘 줄. 항목은 38×38, 아이콘 16 + 글 10/500(meta-sm-500), 흰색 42% · 현재 100%. 오른쪽 main 은 흰 면에 왼쪽 위 · 아래 모서리 8, 그림자 -2 0 12 -4 rgba(0,0,0,.03). 헤더는 44, 병원 이름 · 탭 · 오른쪽 도구(검색 28 + 버튼 SS).
- **동작**: 메뉴 이동만. 시안의 다른 탭은 링크를 지웠다(L16).
- **쓰는 곳**: 모든 CRM 화면 공통(시안 L714-715 「화면마다 같은 자리에」).
- **토큰만으로**: 아니오. `--secondary #000a14` 가 medikit 에 없다. 46 · 38 · 44 · 28 치수도 프리셋에 없다.
- **확장 가능성**: `Menu`(collapsed 76) · `ms-side` 를 줄이는 것보다 **CRM 셸 부품을 새로 만드는 쪽이 맞다.** 구조가 다르다(글 붙은 아이콘 · 어두운 바탕).

### G2. 소형 탭 · 세그먼트 — E05 · E10 · E16 (+E55 탭)
- **생김새**: 밑줄 탭은 세 벌이고 크기가 다 다르다.
  - 헤더: 14/500 · 밑줄 3
  - 인박스: 14/400→600 · 밑줄 2 · 간격 24
  - 차트 모달: 16/400→500 · 밑줄 3 · 아래 8 · 간격 16
  - 세그먼트: 164×28 · 바탕 gray-200 · 고른 칸 흰 면 + drop-shadow · 12/400→500.
- **동작**: 탭 바꾸기. 인박스 탭 라벨에 개수를 붙인다(「호출 2」). 차트 탭은 ←→ 키로 바꾼다.
- **토큰만으로**: 밑줄 탭은 거의 예(색 · typo 토큰 안. 밑줄 2px · 간격 16/24 만 새 값). 세그먼트는 아니오(28h · 164w · 그림자 새 값).
- **확장 가능성**: `Tabs` 에 size(sm) · 바닥선 끄기를 더하면 밑줄 탭 셋을 덮는다. 세그먼트는 새 컴포넌트다(Figma 「Tab List」).

### G3. 작은 툴팁 (꼬리 있음) — E11
- **생김새**: 여백 5/8 · 모서리 6 · min-w 36 · 12/500 흰 글자 · 면 `ms-hover-dark/70` · 위쪽 꼬리 14×6.
- **동작**: hover/focus 0.1초 뒤 나타남. 카드가 넘침을 잘라서 `position:fixed` 하나를 옮겨 쓴다(L575, L1807-1820).
- **쓰는 곳**: 필터 버튼, 마취 칩(종료/재시작), 방 이름(방 옮기기), 차트 아이콘.
- **토큰만으로**: 색은 예(hover-dark/70 이 그대로다). 치수(5/8 · 14×6 꼬리)는 새 값. 시안 주석은 모양을 「원티드 Tooltip Small」에서 가져왔다고 적었다(L184).
- **확장 가능성**: React `TooltipContent` 에 size=sm + 꼬리를 더하면 된다. **HTMX 는 CSS + medikit.js 에 새로 넣어야 한다.**

### G4. 접는 칸 (Accordion) — E17
- **생김새 · 동작**: 머리 버튼(아이콘 + 제목 + 꺾쇠 회전) · 0fr↔1fr 220ms 접기 · `aria-expanded`.
- **쓰는 곳**: 인박스 세 탭 전부(확인 필요 / 시작 가능 / 시술 대기, 수락 대기 / 수락함, 방별 묶음).
- **토큰만으로**: 예.
- **확장 가능성**: React `Accordion` 이 있다. HTMX 는 `<details>/<summary>` 에 같은 모양을 입히면 된다(가이드 §10). 다만 `<details>` 는 높이 애니메이션이 안 되고, 시안의 220ms 전환은 CSS grid 방식이다.

### G5. 밀집 카드 (머리 면 줄 카드) — E18 · E28 · E32 · E33 · E49
- **생김새**: 모서리 6. 머리 면 줄(#f7f7f8, 12/500)과 본문으로 나뉜다. 인박스 카드는 테두리 gray-300 + 그림자 0 2 4 .06, 방 카드는 테두리 없이 그림자 0 2 4 -2 .06.
- **상태**: 기본 · hover(1px 뜸 + 0 3 6 .07) · 선택(1px primary + 번짐 3~4px `primary-shadow`) · 선택+늦음(red + `red-shadow`) · 새로 늦음 깜빡임(red-100) · 다른 카드 흐림(.88/.7) · 빈 방(subtle) · 연결 원래 방 · 드래그 중.
- **동작**: 카드를 누르면 방 선택이 반대쪽(인박스↔보드)에도 표시되고 그쪽으로 스크롤된다(L1795-1804). 연결된 두 방은 둘 다 선택된다.
- **토큰만으로**: 일부. 번짐은 `--ms-primary-shadow` · `--ms-red-shadow` 를 그대로 쓴다(L671). 아니오인 것은 머리 면 #f7f7f8 · 그림자 3종 · 모서리 6이다.
- **확장 가능성**: `Card` 와는 모서리 · 선택 표현(면 + 체크)이 달라서 **확장보다 새 부품(CRM card)이 낫다.** 인박스 · 시술 완료 · 방 카드를 한 부품의 변형으로 묶을 수 있다.

### G6. 사각 상태 배지 · 칩 버튼 — E24 · E36 (+E28)
- **생김새**: 11/500 · 자간 .34 · 패딩 3/6(≈22h) · 모서리 6 · tabular-nums.
  - solid 는 면 = 글자색 8%: primary / red / gray rgba(112,115,124,.08) / going-wait(color-mix).
  - outline 은 테두리 = 글자색 43%(::before).
- **동작**: 마취 칩은 버튼이고 상태 셋을 돈다(시작 → 진행 +mm:ss → 완료 nn분). hover 면 · 누르면 0.97.
- **쓰는 곳**: 인박스 카드 머리(마취 · 대기 시간), 방 머리(마취), 시술 완료 카드(귀가/귀가 대기).
- **토큰만으로**: 아니오. 11px 는 typo 토큰에 없다(최소는 10 · 12). 8% · 43% 투명도 단계도 없다(medikit 은 -100 단계 면을 쓴다). going-wait 초록은 팔레트에 없다.
- **확장 가능성**: `Badge` 에 shape=square · size=xs · tone=outline 을 더하는 확장이 가능하다. `className` 덮어쓰기도 문서로 허용돼 있다(mk.d.ts:111-118 주석). 상태 색이 들어오려면 **G-color(§4 상태 팔레트) 결정이 먼저다.**

### G7. 찾은 글자 표시 — E26
- `<mark>`, yellow-300 면, 모서리 2, 글자색 그대로. **토큰만으로**: 예(`--ms-yellow-300` 은 1.4.0 base.css:30 · 가이드 §4-1 에 있다. 키트 css 에는 빠져 있다). 클래스 하나면 된다.

### G8. 도메인 아이콘 세트 — E30 · E41 (+E35)
- 시안 자산(L8): `st-*`(accepted · called · called-late · done · done-gray · progress · ready), `chart-doctor/nurse-on/off`, `stethoscope`, `circle-check-brand`, `circle-minus`, `warn-fill`, `link-2-white-16`, `arrow-right-brand-16`, `maximize-2`, `clock3-12`, `pencil-12`, `pc-funnel-12`, `rail-*` 6종, `flag-jp/tw` 외.
- medikit 아이콘(1.4.0: Arrow · Chevron · Close · Search · Check · CheckCircle · Calendar · Reset · More · Warning · Error · Eye · Delete · Plus …)에는 이것들이 없다. 키트는 「lucide 인라인 SVG」 방식이다(README L46). 시안의 다수(grip · user-round · ellipsis · x · link · maximize · stethoscope · pencil · funnel · clock)는 lucide 라서 같은 방식으로 들어간다. **lucide 가 아닌 것**(st-* 상태 아이콘 · chart on/off · warn-fill · rail 아이콘)은 svg 원본을 받아야 한다.
- **토큰만으로**: 예(currentColor). 다만 시안은 늦은 시계를 `filter: invert…hue-rotate` 로 빨갛게 칠한다(L555). 이건 currentColor 아이콘으로 바꾸는 게 맞다.

### G9. 끌어서 순서 바꾸기 — E34
- **동작**: 손잡이를 pointerdown 하면 다른 방 위로 갈 때 자리가 미리 바뀐다(260ms 잠금). 드래그 중 커서는 grabbing, 끄는 방은 떠 있는 그림자. 키보드는 ←↑→↓.
- **토큰만으로**: 그림자 0 6 16 rgba(0,0,0,.12) 가 새 값이다.
- **확장 가능성**: medikit 에는 끌기 동작이 없다. HTMX 에서는 바닐라 JS + 순서 저장 요청(hx-post)이 필요하다. **순서를 서버에 저장하는지는 시안에 없다**(§6).

### G10. 접히는 메모 블록 — E39
- **생김새**: 왼쪽 2px gray-500 선 · 패딩 0 22 0 6 · 10/400 secondary · pre-line · max-h 67(5줄) · 오른쪽 아래 16px [크게 보기] 아이콘 버튼(흰 면, hover gray-200).
- **동작**: 5줄이 넘을 때만 아이콘이 보이고, 누르면 제자리에서 펼친다(L540, L1221). 기준은 줄 수다(`split('\n').length > 5`).
- **토큰만으로**: 예(meta-sm-400 · gray-500).
- **확장 가능성**: 없음. 새 부품이다.

### G11. 체크박스 혼합(−) 상태 — E40
- **생김새**: 면 primary · 흰 가로줄(left/right 3 · 두께 1.5).
- **확장 가능성**: React `Checkbox` 는 Radix 라 `checked="indeterminate"` 를 받는다. 다만 표시가 CheckIcon 하나뿐이라 − 아이콘을 더해야 한다. HTMX `ms-checkbox` 는 `:indeterminate` 스타일을 더하면 된다(JS 로 `el.indeterminate=true`). **토큰만으로**: 예.

### G12. 시술 행 — E41 · E45
- **생김새**: 열 다섯 개.
  1. 상태 칸 16: 체크박스 / 꺼진 체크박스 / 완료 아이콘
  2. 이름 14/400(말줄임) + 메타 12(원장 · 상태 글자)
  3. 시간 칸(G13)
  4. 액션 버튼 24h
  5. 더보기 16
  - 줄 모서리 0 · 패딩 4/8 · hover primary-100.
  - 완료 줄은 따로 아래 묶음에 들어간다(이름 tertiary · 1.6 · 패딩 2/8).
- **동작**:
  - 줄 아무 데나 누르면 차트 모달이 열린다. 버튼 · 체크박스는 제외(L1606-1611).
  - 체크는 체크박스로만 한다.
  - 더보기는 hover · focus 때 폭 0→16 으로 밀며 나타난다.
  - 상태 글자 색: 진행중 · 수락 = brand, 호출 = brand(늦으면 red), 준비중 = tertiary.
- **토큰만으로**: 거의 예. 24h 버튼 높이만 새 값이다(E44).
- **확장 가능성**: 표 행(`TableRow`)과는 성격이 달라서 새 부품이다. 24h 버튼은 `Button` 에 size=xs 가 필요하다(1.4.0 은 ss 28 이 최소).

### G13. 실시간 경과 시간 — E20 · E24 · E36 · E43
- **생김새**:
  - 배지 · 줄 글자: `+mm:ss`(분 두 자리, L943-947)
  - 시간 칸: `⏱ 30초` · `⏱ nn분`
  - 완료: `⏱ nn분` + title 「hh:mm-hh:mm」
- **동작**: 1초마다 다시 그린다(L1784-1787). 넘으면 색이 바뀐다(마취 20분, 호출 5분 또는 재호출). 새로 「확인 필요」가 된 카드는 깜빡인다(L1115-1123).
- **토큰만으로**: 예(tertiary / brand / red).
- **확장 가능성**: medikit 에는 타이머가 없다(`formatDuration` 유틸만 있다). **HTMX 에서는 서버가 시작 시각(data-since)을 내려주고 클라이언트 JS 가 1초마다 글자 · 색만 바꾸는 방식이 필요하다.** 1초 폴링으로 서버 조각을 다시 받는 건 맞지 않는다. 기준 시간(20분 · 5분)은 시안 상수(L804, L879)이고, 도메인 값인지는 정해지지 않았다(§6).

### G14. 선택 시 떠오르는 하단 액션 바 — E46 (+E53 하단 버튼)
- **생김새**: 카드 바닥에 붙는 흰 그라데이션(0→흰 45%) + 꽉 찬 버튼 M(36). 나타날 때 본문 아래에 56 여백을 둔다.
- **동작**: 준비중 시술을 고르면 [n개 호출]이 올라오고, 다 끝나면 [귀가 대기]. 사라지는 동안 글자가 바뀌지 않게 마지막 개수를 붙들어 둔다(L1207-1209). 방 옮기기 목록의 [방 옮기기]도 같은 「고르면 올라오는」 패턴이다(L644-649).
- **토큰만으로**: 예.
- **확장 가능성**: 없음, 새 부품(작다).

### G15. 방 연결 표시 — E47 · E48
- **생김새**:
  - 옮겨 온 방: primary 면 띠(패딩 1/8) + 흰 글자 12/500 + 소형 버튼 2개(패딩 2/4, primary 면, hover 어둡게).
  - 원래 방: 제목 옆 「→ 새 방」 brand 링크 + 본문 30% 흐림 + hover 하면 가운데 Filled Gray S 버튼 2개.
- **동작**: 연결 풀기는 확인 창을 거친다. 돌아가기/돌아오기는 바로 실행.
- **토큰만으로**: 일부. primary 면 위의 흰 글자 · 소형 버튼 패딩 2/4 · hover rgba(0,0,0,.12) 는 새 값이다. Filled Gray 버튼(gray-200 면 + gray-700 글자)은 1.4.0 filled black(gray-200 + 검정)과 다르다.
- **참고**: 시안 L35 규칙 「흰 글자 금지 — 칩 = 네모 + 검정 글자」와 이 띠의 흰 글자가 충돌한다. 칩에만 해당하는 규칙인지 확인이 필요하다(§6).

### G16. 팝오버 + 메뉴/목록 (HTMX) — E50 · E51 · E53
- **생김새**:
  - 더보기 메뉴: 200 · 모서리 12 · 줄 36 · 구분선
  - 의사 고르기: 240 · 모서리 8 · 머리 / 검색 / 라벨 / 줄 32 / 하단 버튼
  - 방 고르기: 200 · 줄 44 · 최대 220 · 꺼진 줄 · 선택 체크 · 하단 버튼 올라옴
  - 공통: 흰 면 · `shadow-pop-over` · 나타날 때 -4px · 0.95 → 1(150ms).
- **동작**: 트리거 아래에 위치를 계산한다(화면 밖이면 12px 안으로, L1097-1100 · L1245-1247). 바깥 mousedown 이나 Esc 로 닫힌다. Esc 로 닫으면 포커스를 트리거로 돌려준다(L1778).
- **토큰만으로**: 예(pop-over 그림자 · primary-100 · gray-100). 치수 일부(모서리 12 · 줄 32/36/44)는 Figma 값이다.
- **확장 가능성**: React 는 `Popover` + `Command`/`ComboBox` 로 상당 부분을 덮는다(△). **HTMX 는 바탕부터 없다**(가이드 §10). 위치 계산 · 바깥 클릭 · 포커스 복귀를 medikit.js 에 새로 넣어야 한다. 선택지 하나는 `<dialog>`(비모달) · Popover API 다(§6).

### G17. 의사 아바타 — E52
- **생김새**: 24 원 · 이니셜 2자(「김도윤 원장」→「도윤」, L886) · 10/500.
  - tone-0 primary-100/primary
  - tone-1 purple-100/purple + 테두리 #eedcff
  - tone-2 #eef8e7/#5aa832 + 테두리 #dcf0cd
  - 없음 = 회색 원 + 사람 아이콘
- **동작**: 색은 의사 목록 순서 % 3. 정하는 규칙은 시안의 가짜 데이터 기준이다.
- **토큰만으로**: 아니오. 연두 계열이 없다(시안 주석 「메디킷에 없음, 차이표 ① 후보」 L471). 테두리 단계(#e3f0ff · #eedcff)도 토큰에 없다.
- **확장 가능성**: 없음, 새 부품이다. 색 규칙(의사 ↔ 색)이 도메인에 있는지는 확인되지 않았다.

## 4. medikit 토큰 밖 값

비교는 medikit 1.4.0 `styles/base.css` · `tailwind` preset 기준이다. 「토큰 같음」은 이름만 다르고 값은 토큰과 같다는 뜻이다.

### 4-1. 색

| 값 | 쓰는 곳 | 시안 근거 | 판정 |
|---|---|---|---|
| `--primary #1d8bff` · 100 `#eff7ff` · 300 `#dbecff` · 500 `#99cbff` | 브랜드 전부 | L28-31, L668 | **밖.** 1.4.0 `[data-product]` 는 say · bay · charty · watch · selly · linky · studio 뿐이다(base.css:85-138). crm 오버라이드가 필요하다. `--ms-primary-shadow` 짝(rgba(29,139,255,.3))은 L672 `--glow` 에 이미 있다 |
| `--text-brand #1d8bff` (= primary) | 선택 탭 · 상태 글자 | L668 | primary 와 같다(새 토큰 아님) |
| `--secondary #000a14` | 아이콘 줄 · 앱 바탕 | L32, L657, L661 | **밖** |
| 고객 상태 7색 × default/100/300/500 (`--st-reception` … `--st-gone`) | 이 화면에서는 `--st-reception`(link-bar) · `--st-going-wait`(귀가 대기 배지)만 쓴다 | L36-42, L556, L620 | **밖** (KOS 색, L34). 접수 = primary |
| `--surface-head #f7f7f8` | 카드 · 방 머리 면 줄 | L505, L668, L693 | **밖** (gray-100 #fbfbfb 와 gray-200 #f3f3f3 사이) |
| `--surface-board #e3e3e5` | 보드 바탕 | L668, L704 | **밖** (gray-300 #e3e3e3 와 거의 같은 푸른 회색) |
| `--text-tertiary #6e6e6e` | 보조 글자 전반 | L52 | 토큰 같음(gray-700). 다만 1.4.0 에 **text-tertiary 시맨틱 이름은 없다** |
| `#fd9400` (`.cbadge.warning`, 쓰는 곳 없음) | ― | L183 | 토큰 같음(`--ms-yellow`) |
| `#ffc4c5` · `#ffefef` · `#ffe4c0` · `#ffe1e1` | 선택+늦음(앞 버전), 늦음 깜빡임, 찾은 글자, outlined red 테두리 | L363, L366, L396, L168, L521, L167 | 토큰 같음(red-500 · red-100 · yellow-300 · red-300) |
| `rgba(34,41,67,.7)` | 툴팁 면 | L190, L194, L576 | 토큰 같음(`ms-hover-dark/70`) |
| `rgba(29,139,255,.3)` · `rgba(255,78,81,.2)` | 선택 번짐 | L672 | 토큰 같음(primary-shadow · red-shadow) |
| `rgba(0,0,0,.04)` | gray 배지 면(앞 단계) · 칩 hover | L205, L454 | 토큰 같음(`ms-black/[0.04]`, Chip) |
| `rgba(112,115,124,.08)` | gray 배지 면(crm 최종) | L665 | **밖** |
| `rgba(29,139,255,.08)` · `rgba(255,78,81,.08)` · `color-mix(…8%)` | solid 배지 면 | L201-202, L206, L556 | **밖** (medikit 은 -100 단계 면을 쓴다) |
| 테두리 43% (`currentColor` + opacity .43) | outline 배지 | L180 | **밖** |
| 아바타: `#e3f0ff` · `#eedcff` · `#eef8e7` · `#5aa832` · `#dcf0cd` | 의사 아바타 | L473-475 | **밖** (`#f8f0ff` · `#ac47ff` 는 purple-100 · purple 토큰 같음) |
| 빨간 아이콘 `filter: invert(42%)…hue-rotate(335deg)` | 늦은 시계 | L555 | **밖** (색 대신 필터. currentColor svg 로 바꿀 것) |
| `#fbfbfb` | 콤보 hover | L641 | 토큰 같음(gray-100) |

### 4-2. 그림자 · 반투명

| 값 | 쓰는 곳 | 근거 | 판정 |
|---|---|---|---|
| `0 2px 4px rgba(0,0,0,.06)` / 방은 `0 2px 4px -2px …` | 카드 기본 | L61, L499 | 밖 |
| `0 3px 6px rgba(0,0,0,.07)` | 카드 hover | L387-391, L496, L509-510 | 밖 |
| `0 6px 16px rgba(0,0,0,.12)` | 드래그 중 방 | L405 | 밖 |
| `-2px 0 12px -4px rgba(0,0,0,.03)` · `-2px 0 8px …` | main 왼쪽 | L95, L662 | 밖 |
| `0 2px 6px rgba(0,0,0,.08), 0 10px 28px rgba(0,0,0,.14)` 「shadow/float」 | 차트 모달 · 확인 창 | L582, L610 | 밖 (1.4.0 은 pop-over · pop-over-more 뿐) |
| `0 0 4px #cfcfcf` | 팝오버 · 콤보 목록 | L221, L687 | 토큰 같음(`shadow-pop-over`) |
| `0 1px 6px rgba(29,139,255,.3)` | 토스트 | L287 | Notify sm 값과 같음 |
| `drop-shadow(0 0 2px rgba(0,0,0,.1))` | 세그먼트 고른 칸 | L136 | 밖 |
| 흐림 opacity .88 · .7 · .3 · 흰 그라데이션 45% | 선택 시 나머지 · 연결 원래 방 · 호출 바 | L393, L513, L630, L347 | 밖 (동작 값) |

### 4-3. 글자

| 값 | 쓰는 곳 | 근거 | 판정 |
|---|---|---|---|
| 글꼴 Pretendard(가변 45-920, woff2 를 data URI 로 넣음) | 전체 | L23, L69 | medikit 과 같은 글꼴(base.css 「Pretendard Variable」). **파일은 DAY 가 따로 둬야 한다**(키트 README L19) |
| **11px**/500, lh 1.273, 자간 .34 | 배지 · btn-xs | L178, L198 | **밖** (typo 는 10 · 12) |
| 13px/500 | 토스트 | L287 | Notify sm 과 같음(medikit 자체가 typo 밖 값을 씀) |
| 14/600 lh 1.5 | 팝업 제목 · 인박스 탭 선택 | L172, L227 | **밖** (heading-sm 은 500/400 만, body-600 은 lh 1.6) |
| 12 lh 1.5 | `.memo-box` 기본 (최종은 10/1.3 로 덮임 L417) | L336 | 밖이지만 최종 화면에서는 쓰지 않음 |
| 16/400·500 lh 1.5, 18/500, 16/600, 10/500, 12/400·500 lh 1.3, 14/400·500 lh 1.5·1.6 | 나머지 | ― | 토큰 안 (heading-md · title-sm-500 · heading-md-600 · meta-sm-500 · caption-md · heading-sm · body) |

### 4-4. 치수 (medikit 프리셋에 없는 것)

| 값 | 쓰는 곳 | 근거 | 가장 가까운 medikit |
|---|---|---|---|
| 아이콘 줄 46 · 항목 38 | 셸 | L87-89 | Menu collapsed 76 · 항목 40 |
| 헤더 44 | 셸 | L98 | Header 57 |
| 입력 28h · 모서리 4 | 헤더 검색 | L107 | Input m 36 |
| 버튼 **24h**(패딩 4/8) · **22h**(btn-xs, 정의만 있고 쓰는 곳 없음) | 시술 줄 액션 | L430, L198 | Button ss 28 |
| 링크 띠 버튼 패딩 2/4 | link-bar | L623 | ― |
| 세그먼트 164×28 · 패딩 2/4 | 보기 바꾸기 | L133 | ― |
| 카드 모서리 **6** | 인박스 카드 · 방 카드 · 배지 | L177, L271, L488 | Card 12 · ms-card 12 |
| 모달 모서리 **14** · 폭 410 / 280 | 차트 모달 · 확인 창 | L582, L610 | Modal 20 · ms-modal 16 · ConfirmModal min-w 444 |
| 팝오버 모서리 12 · 폭 200/240 · 줄 32/36/44 | 메뉴 · 의사 고르기 · 방 고르기 | L208-209, L220, L235, L638 | Popover 모서리 8 · ComboBox 옵션 min-h 50 |
| 툴팁 여백 5/8 · 꼬리 14×6 | 툴팁 | L189, L193 | TooltipContent 10/16 |
| 칸 폭 280 · 방 최소 256 · 방 높이 max(320, (100dvh−117)/2) | 레이아웃 | L249, L64, L408 | ― (레이아웃 값) |
| 아바타 24 | 의사 | L328 | ― |

## 5. 비슷(△)한 것: 무엇을 고치면 맞나 (한 줄씩)

- E03 헤더 · E05 헤더 탭 · E16 인박스 탭: Tabs 에 size=sm 과 바닥선 끄기를 더한다. 헤더 셸은 G1.
- E06 헤더 검색: Input 에 28 크기(ss)를 더한다.
- E07 페이지 머리: `Divider vertical` + `heading-md-600` 조합으로 된다. 키트 `ms-page__head` 는 쓰지 않는다.
- E08 · E09 버튼: Button outlined black 을 HTMX `ui.btn` 에 더하고(키트에 없다), 정사각 아이콘 ss 프리셋을 둔다.
- E14 스크롤바: thumb 색을 base.css(gray-300) 로 맞출지, 시안 값(rgba .1)을 따를지 정해야 한다.
- E27 빈 상태: 테두리 없는 EmptyState 변형(제목 + 버튼).
- E35 경고 아이콘: WarningIcon 과 시안 warn-fill 이 같은 그림인지 대조해야 한다.
- E40 혼합 체크: G11.
- E44 24h 버튼: Button size=xs.
- E54 확인 창: ConfirmModal 소형(280 · 모서리 14 · 버튼 M), 또는 ms-modal 에 sm 변형.
- E55 차트 모달: ms-modal 에 폭 410 · 모서리 14 · 그림자 float.
- E56 Textarea: 키트에 textarea 클래스를 더한다. 자동 높이는 `field-sizing` 에 맡기거나 JS 로 한다.

## 6. 확인 못 한 것 · 코디가 정할 것

1. **medikit 기준 버전.**
   - 브리프가 가리킨 `/Users/kknaks/git/medikit` 은 0.3.0(main `55c14a2`)이고, Badge · Chip · Card · Accordion 이 없다.
   - 대조는 cc-prototype 이 쓰는 1.4.0 배포본(다른 워크스페이스의 node_modules)으로 했다.
   - HTMX 키트는 「1.3.0 기준」이다.
   - 원본 레포를 최신으로 받을 수 있는지는 확인하지 않았다(fetch 하지 않음).
   - **DAY 의 medikit 기준 버전을 정해야 한다.** (참고: CENTURION_DAY 의 node_modules 에 medikit 0.3.0 이 있다는 경로만 봤다. 워크트리는 열지 않았다.)
2. **Figma 메디킷 ↔ 코드 medikit 차이.** 시안이 「메디킷 ○○」이라 부르는 Tab List · More Menu Panel · EmptyState · ComboBox M 펼친 목록 · Button 24 · Tooltip Small 은 코드에 없다. Figma 원본(817:8278 · 1004:6082 · 1014:9855 · 1066:25353 · 1068:26115)은 열어 보지 않았다. 시안 주석의 「차이표 ①②」(L106, L218, L471)와 `docs/design-rules.md`(L26)도 이 레포 · 시안 파일 안에서는 찾지 못했다.
3. **브라우저 렌더링.** 브라우저로 열어 보지 않고 HTML · CSS · JS 를 읽었다. hover · 애니메이션 · 실제 높이는 코드 값이고, 눈으로 확인한 것은 아니다.
4. **cc-prototype 이전 구현**(`procedure/front/components/procedures/*`)은 import 목록만 봤다(Badge · Button · Popover · Tabs · Textarea · Tooltip · ConfirmModal 사용). 이 시안(3차 v11)과 화면 구성이 다른 이전 버전이라 요소별 대조에는 쓰지 않았다.
5. **WarningIcon ↔ warn-fill**, **st-\* 아이콘 원본**: svg 를 열어 같은 그림인지 대조하지 않았다(data URI 안에 있다).
6. **시안에 없는 결정**(화면을 만들 때 막힐 곳, 추측으로 채우지 않았다):
   - 방 순서를 서버에 저장하는지(G9)
   - 마취 20분 · 호출 5분 기준이 도메인 값인지(G13)
   - 의사 ↔ 아바타 색 규칙(G17)
   - 세그먼트(의사별 / 4층 / 미사용)가 무엇을 거르는지. 시안 L1821 이 「정하기 전」이라고 적었다.
   - 고객 이름을 누르면 가는 차트 화면(L1671-1672 「아직 없음」)
   - 필터 버튼을 누른 뒤의 동작(시안에 없음)
   - link-bar 흰 글자와 L35 「흰 글자 금지」 규칙의 관계
7. **HTMX 동작 재현.** 시안은 1초 전체 다시 그리기 + morph + FLIP(L1491-1558)로 카드가 칸 사이를 미끄러지듯 옮겨 간다. HTMX swap 으로 이 전환을 어디까지 살릴지는 이번 조사 범위 밖이다(구현 때 정할 것).
