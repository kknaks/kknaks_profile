# cc-procedure-map — 시술현황 시안 컴포넌트 세트 OpenPencil 결과 보고

## 상태: done — 26 세트 · 120 variant · 파일 저장(headless) · 린트 남은 것은 전부 시안 값(사용자 결정 대기)

- 대상: `reference/2026-11-12-open-pencil/medikit/medikit.fig` 「components」 페이지(앱 모드 · 활성 문서)
- 생김새 정본: `reference/2026-11-03-cc-day/screen/시술현황_프로토타입 (1).html`(3차 v11). 「시안 근거」 열의 숫자는 이 HTML 의 줄 번호다
  - CSS 블록 ① 25–292행(공통) · ② 293–653행(화면) · ③ 654–712행(body.crm 최종 모양) — 같은 선택자는 **뒤 블록이 이긴다**(값은 이긴 값)
  - 마크업 = 788–1826행 스크립트의 템플릿 함수(`procRow3` · `roomCard3` · `inboxCard` · `a1Rows` · `recallPopHtml` · `chartModalHtml` · `moveMenuHtml` · `doneRoomCard` …)

## 인벤토리

시안 마크업에 실제로 반복해 나오는 단위만 올렸다. 클래스가 CSS 에만 있고 v11 마크업에 안 나오는 것(`.combo` · `.combo-opt` · `.btn-xs` · `.cbadge.warning` · `.cbadge.outline.red`)과 한 번만 나오는 화면 틀(`.rail` · `.header` · `.page-controls` · `.seg`)은 뺐다. `:hover` · `:active` 는 상태로 만들지 않았다(클래스 상태 · `:disabled` · 입력의 `:focus` 만).

색 이름 = 변수 이름(컬렉션 `medikit`). `a%` = 칠 불투명도.

| 컴포넌트 | variant 축 | 상태 | 시안 근거 | 크기 · 여백 · 모서리 · 글자 · 색 |
|---|---|---|---|---|
| **Checkbox** | state | default · checked · mixed · off | `.checkbox` 138 · 571 · `.is-mixed` 212 · `.is-off` 552 · `procRow3` | 16×16 · r4 · 테두리 1 gray/300 · 면 white / checked·mixed = primary 면·테두리 + 흰 체크 12(`check-white`) · mixed = 흰 막대 10×1.5 r1 · off = gray/200 면 · gray/300 테두리 |
| **SelectAll** | state | default · mixed · checked · disabled | `.sel-all` 455 · `selAll()` | 높이 24 · 여백 0 2 · 간격 6 · r4 · Checkbox + 「전체 선택」 12/400 lh1.3 gray/700 · disabled = 체크박스 off |
| **Search** | size · state | ss(헤더 28) · m(36) · m-left(팝오버 · 아이콘 왼쪽) / default · focus | `.search` 110 · `.header .search` 107 · `.pop-search .search` 231 · `.dn-search` 520 | ss: 200×28 · 여백 0 16 · 간격 16 · r4 / m: 200×36 · 여백 7 16 · 간격 16 · r8 / m-left: 224×36 · 여백 7 12 · 간격 8 · r8 · 테두리 1 gray/300 · 면 white · 글자 14/400 lh1.5 · placeholder gray/600 · 아이콘 `search` 16 · focus = 테두리 primary |
| **Textarea** | state | default · focus | `.cm-ta` 598 | 폭 378(모달 안) · 최소 높이 90 · 여백 16 · 테두리 1 gray/300 · r8 · 14/400 lh1.6 · placeholder 「내용을 입력해 주세요」 gray/600 · focus 테두리 primary |
| **Badge** | kind · color | solid·primary · solid·red · solid·gray · outline·primary · solid·going-wait | `.cbadge` 176 · 241–247 · 665 · `.going-wait` 556 · `anesChip` · `a1Rows` · `doneRoomCard` | 여백 3 6 · r6 · 11/500 lh14 · 자간 0.34 · solid 면 = 글자색 8% · primary 글자 primary · red 글자 red · gray 글자 gray/700 + 면 crm/badge-gray 8% · going-wait 글자·면 status/going-wait(면 8%) · outline = 면 없음 + 테두리 1 글자색 43% |
| **Avatar** | kind · tone | doctor·0 · doctor·1 · doctor·2 · none | `.avatar` 328 · 473–475 · `docAvatar` · `recallPopHtml` | 24×24 · r12 · doctor 10/500 lh1.3 · tone0 면 primary/100 글자 primary 테두리 crm/doctor-blue-border · tone1 purple/100 · purple · crm/doctor-purple-border · tone2 crm/doctor-green-100 · crm/doctor-green · crm/doctor-green-border · none = 면 gray/300 테두리 gray/200 + `user` 16 |
| **Tooltip** | — | default | `.ftip` 576 · 652 · `[data-tip]` 187 | 여백 5 8 · r6 · 최소 폭 36 · 면 hover-dark 70% · 글자 white 12/500 lh1.3 · 꼬리 14×6 위 가운데 |
| **Notify** | — | default | `.notify` 287 · `crmNotify` | 알약 r100 · 여백 14 16 · 간격 8 · 면 white · 그림자 0 1 6 primary 30% · 글자 13/500 primary · 아이콘 18(primary 원 + 흰 체크) · 문구 「저장되었어요」 |
| **Button** | kind · size · state | solid · filled · filled-gray · outlined-gray · outlined-black / l · m · m-dialog · s · ss · xs / default · disabled | `.btn` 150 · 129 · 674 · `.proc3 .btn` 430 · `.pop-foot .btn` 245 · `.held-actions .btn` 634 · `.cm-foot .btn` 606–607 · `.dn-empty .btn` 527 | l 44 · 여백 0 16 · r8 · 16/500 / m 36 · 0 16 · r8 · 14/500 / m-dialog 36 · 0 12 · r6 · 14/500 / s 33 · 0 12 · r6 · 14/500 / ss 28 · 6 8 · r4 · 12/500 lh1.3 / xs 24 · 4 8 · r4 · 12/500 · solid = primary 면 white 글자 · filled = primary/100 면 primary 글자 · filled-gray = gray/200 면 gray/700 글자 · outlined-gray = white 면 gray/300 테두리 gray/600 글자 · outlined-black = white 면 gray/500 테두리 black 글자 · disabled = gray/200 면 gray/600 글자 |
| **IconButton** | icon | grip · more · close · close-24 · maximize | `.icon-btn` 315 · `.proc-more` 439 · `.pop-close` 228 · `.cm-close` 585 · `.memo-more` 541 · 569 | 16×16 r4(close-24 = 24×24) · grip gray/500 · more gray/600 · close gray/700 · close-24 · maximize gray/600(SVG 색) · memo-more 면 white |
| **Tab** | kind · state | header · inbox · modal / default · active | `.tab` 102 · `.ib-tab` 170 · 669–670 · `.cm-tabs .ib-tab` 588 | header 14/500 lh1.5 gray/600 · 아래 여백 4 · active primary + 밑줄 3 r3 primary / inbox 14/400 gray/600 · 아래 여백 4 · active 600 primary + 밑줄 2(아래 -1) / modal 16/400 gray/600 · 아래 여백 8 · active 500 primary + 밑줄 3 |
| **MenuRow** | state | default · disabled | `.more-pop` 208 · `.menu-row` 209 · `renderMorePop` | 폭 188(팝오버 200 − 여백 6×2) · 높이 36 · 여백 0 10 · 간격 10 · r8 · 14/400 lh1.5 black · disabled gray/600 · 문구 「시작 취소」 · 「완료 취소」 |
| **ProcRow** | status · state | wait(default · checked) · called(default · late) · ready · progress(default · menu) · done | `.proc3` 420 · 464 · 547 · 566 · `procRow3` · `liveTime` | 폭 256 · 여백 4 8(done 2 8) · 간격 6 · 면 white(menu = primary/100) · 왼쪽 Checkbox(wait) / Checkbox off(그 밖) / `st-done-gray` 16(done) · 이름 14/400 lh1.5 black(done = lh1.6 gray/700) · 메타 12/400 lh1.3 간격 2: 원장 gray/700 + 상태(준비중 gray/700 · 호출 primary · 늦은 호출 red · 수락 · 진행중 primary) · 시간 칸 12 gray/700 간격 2 + `clock3-12`(late = red) · 버튼 xs(called·수락 outlined-black · ready·시작 solid · progress·종료 outlined-black) · menu = more 16 보임 · done = 이름 옆 차트 아이콘 16(간격 2) |
| **CardRow** | kind | proc-link · call-proc | `.card-row` 700 · `.card-row.is-link` 461 · 560 · `.cl-proc` 399 · 678 | proc-link: 여백 4 6 · 간격 6 · r6 · 점 3 + 이름 12/400 lh1.3 black + 차트 아이콘 2개(간격 4) / call-proc: 여백 2 · 간격 6 · 점 3 + 이름 12 black |
| **RoomCard** | state | default · active · active-late · selection · going · linked · held · empty | `.room` 309 · 488–505 · `roomCard3` · `heldRoomCard` · `emptyRoomCard` | 폭 256 · 높이 448(--room-height) · r6 · 테두리 없음 · 면 white · 그림자 0 2 4 -2 6% · 제목 줄 31 이상 · 여백 5 10 · 간격 6 · 면 crm/surface-head · 손잡이 grip + (late `warn-fill`) + 방 이름 12/500 black + 오른쪽 마취 Badge · 고객 여백 8: 이름 14/600 lh1.6 + 한글 이름 12/500 gray/800 · vital 12/400 gray/700 간격 4 + 막대 1×10 gray/300 · 메모 여백 12 8 · 왼쪽 선 2 gray/500 · 여백 0 22 0 6 · 10/400 lh1.3 gray/800 · 목록 머리 여백 8 8 0 + SelectAll · ProcRow 들 · done 목록 위 선 1 gray/200 · active = 테두리 1 primary + 번짐 4 primary 30% · active-late = red + red 20% · selection/going = 아래 호출 칸(여백 28 8 8 · 흰 그라데이션) Button m · linked = 제목 아래 LinkBar · held = 몸 30% + 가운데 Button filled-gray s 둘 · empty = 면 gray/100 · 제목 줄만 |
| **LinkBar** | — | default | `.link-bar` 620 · `linkBar` | 여백 1 8 · 간격 6 · 면 primary · `link-2-white-16` · 방 이름 12/500 white · 버튼 2개 여백 2 4 r4 면 primary 12/500 white(「연결 풀기」 · 「돌아가기」) |
| **InboxCard** | kind · state | now · now-late(재호출) · call-wait(수락) · call-accepted · done-chart / default · active · active-late | `.inbox-card` 268 · 663 · 692–704 · `a1Rows` · `inboxCard` · `renderCallsTab` · `doneRoomCard` | 폭 256 · r6 · 테두리 1 gray/300 · 면 white · 그림자 0 2 4 6% · 머리 여백 4 8 · 최소 24 · 면 crm/surface-head · 방 이름 12/500 black + 시간 Badge · 몸 여백 8 간격 4: 고객 줄 `user-round-12` + 이름 12 black + 한글 12/500 gray/700 · 원장 줄 `stethoscope` + 이름 + 호출 +mm:ss gray/700(late red) / 수락 primary · 버튼 줄 여백 0 8 8(재호출 outlined-gray ss · 수락 solid ss) · active = 테두리 primary + 번짐 3 primary 30% · active-late = red · done-chart 머리 = 시간 12 gray/700 + Badge(귀가 대기 going-wait / 귀가 solid gray) |
| **InboxSectionHead** | icon | late · going · wait · none | `.ib-head` 261 · 709 · `renderSide4` · `renderCallsTab` | 최소 22 · 간격 5 · 아이콘 16(`warn-fill` · `circle-check-brand` · `circle-minus`) + 제목 14/500 lh1.6 gray/800(「확인 필요」 · 「시작 가능」 · 「시술 대기」 · 「수락 대기 2」) + `chevron-down-20c` 20 |
| **PopOption** | kind · state | doctor · all / default · on | `.pop-opt` 234 · `recallPopHtml` | 폭 224 · 높이 32 · 여백 0 6 · 간격 6 · r6 · Avatar + 이름 12/500 black + 보조 10 gray/700 + 꼬리표 10/500 primary(「처음 호출」 · 「호출」) · on = 면 primary/100 · 이름 primary |
| **Popover** | mode | recall · accept | `.pop` 219 · `recallPopHtml` | 폭 240 · r8 · 면 white · 그림자 0 0 4 gray/500 · 머리 여백 10 12 · 아래 선 1 gray/200 · 제목 14/600 + close · 검색 여백 8 8 0(Search m-left) · 라벨 10/500 gray/600 여백 8 4 4 · PopOption 들 · 발 여백 8 · 위 선 1 gray/200 · Button s solid |
| **ComboOption** | state | default · on · disabled | `.combo-opt-m` 638 · `moveMenuHtml` | 폭 200 · 높이 44 · 여백 11 16 · 간격 16 · 14/400 lh1.5 black · on = 면 primary/100 · 500 primary + `check` 16 · disabled gray/600 |
| **MoreMenu** | kind | menu · combo | `.more-pop` 208 · 636 · `renderMorePop` · `moveMenuHtml` | menu: 폭 200 · 여백 6 · r12 · 그림자 pop-over · MenuRow / combo: 폭 200 · r8 · ComboOption 들 + 발(Button m solid 「방 옮기기」 · 여백 8 · 위 선 1 gray/200) |
| **ChartModal** | — | default | `.cm-box` 582 · `chartModalHtml` | 폭 410 · r14 · 면 white · 그림자 float · 머리 여백 14 간격 10 · 제목 18/500 lh1.5 black + close-24 · 탭 줄 여백 8 16 간격 16(Tab modal) · 섹션 여백 12 16 간격 4: 시술 이름 14/400 + 메타(`pencil-12` · 이름 · 막대 · 시각) 12 gray/700 + Textarea · 발 여백 8 16 간격 8 오른쪽 정렬: 「Ctrl + Enter」 14/400 gray/700 + Button l solid 「저장」 |
| **ConfirmDialog** | — | default | `.cm-confirm > div` 610 · `renderConfirm` | 폭 280 · 여백 20 · r14 · 면 white · 그림자 float · 제목 16/500 black · 본문 14/400 lh1.6 gray/700(위 4) · 발 위 20 · 간격 8 오른쪽: Button m-dialog outlined-gray 「취소」 + solid 「닫기」 |
| **EmptyState** | — | default | `.dn-empty` 525 | 간격 20 · 가운데 · 최소 높이 380 · 제목 18/600 lh1.5 black 「조건에 맞는 고객이 없어요」 + Button m-dialog outlined-gray 「조건 지우기」 |
| **Icon** | name | 시안 아이콘 26 | 1·8행 자산 표 · 788행 `ICON` · `CHECK16` · `crmNotify` | SVG 그대로 · 색 = 변수(primary · gray/500 · 600 · 700 · red · white · gray/300) |

시안 문구는 모두 시안 데이터(`state` 788행~)에서 가져온다(예: 방 「시술실 A」 · 고객 「[TW] CHOU YU WEN」 「저우위원」 · 시술 「써마지 900샷」 · 원장 「김도윤 원장」).

## 그룹 분할 · 서브에이전트

1차(기본 세트 · 서로 의존 없음)와 2차(합성 세트 · 1차 세트를 `inst()` 인스턴스로 씀)로 나눴다. 서브에이전트 공통 지침 = 리드 스크래치 `SUBAGENT.md`(계약 · 이름 · 바인딩 · 린트 기준).

| 그룹 | 세트(스크립트) | 서브에이전트 산출 | 렌더 |
|---|---|---|---|
| G1 기본 입력류 | Icon 26 · Checkbox 4 · SelectAll 4 · Search 6 · Textarea 2 | 스크립트 5 · draft/G1 시험 · 삭제함 | ✅ components |
| G2 배지 · 아바타 · 알림 | Badge 5 · Avatar 4 · Tooltip 1 · Notify 1 | 스크립트 4 · draft 시험 중 앱 고장 | ✅ components |
| G3 버튼 · 탭 · 메뉴 줄 | Button 12 · IconButton 5 · Tab 6 · MenuRow 2 | 스크립트 4 · draft 시험 중 앱 고장 | ✅ components |
| G4 방 카드 | ProcRow 8 · LinkBar 1 · RoomCard 8 | 스크립트 3 · 정적 검토(가짜 figma 로 실행 · 노드 97 / 11 / 507) | ✅ |
| G5 인박스 | CardRow 2 · InboxSectionHead 4 · InboxCard 6 · EmptyState 1 | 스크립트 4 · 정적 검토(노드 ~11 / 23 / 115 / 4) | ✅ |
| G6 팝오버 · 모달 | PopOption 3 · Popover 2 · ComboOption 3 · MoreMenu 2 · ChartModal 1 · ConfirmDialog 1 | 스크립트 6 · 정적 검토(node --check) | ✅ |

경과: 1차를 병렬 서브에이전트가 각자 draft 페이지에 eval 하다가 앱 eval 이 고장(Out of bounds memory access) → 코디가 앱 재시작. 이후 규칙(코디): **eval 은 리드만 한 번에 하나** · 서브에이전트는 스크립트 작성 · 정적 검토만. 2차는 그 규칙으로 작성 완료, 리드가 G4 첫 eval 을 보내려는데 `documents list` 부터 RPC 시간 초과 — 코디 대기 지시. 재시작 뒤 직렬로 26세트 전부 앱에 렌더 · 단계별 저장까지 됐으나, 멱등 확인용 run-all 2회차에서 앱 eval 이 또 고장(직렬 · 세 번째) — 코디 지시로 **앱 모드를 버리고 headless(`eval <파일> -w`)로 전환**. 최종 산출은 headless 로 만든 디스크 파일이다(백업: `medikit.before-headless.fig` = 전환 직전 디스크).

공통 파일(`components/`): `_icons.js`(시안 SVG 26 · 생성물) · `_lib.js`(box · text · icon · makeSet · inst · TARGET_PAGE) · `_vars.js`(시안 변수 추가) · `_reset.js`(페이지는 두고 비움) · `run-one.sh`(eval 한 번에 스크립트 하나) · `run-all.sh`(순서 계약). 앞 판의 키트 스크립트(Accordion · Banner · ComboBox · Command · custom · Divider · Input · RadioGroup · Table · Tabs …)는 지웠다(시안에 없는 키트 컴포넌트 · 폐기된 방향).

## 만든 것 — 컴포넌트 세트 · variant 수

「components」 페이지 = 섹션 26(`section/<Name>` = 이름표 + 세트) · **26 세트 · 120 variant** · 노드 1208. 「medikit」 토큰 페이지 노드 257 · 「Page 1」 비어 있음 · 옛 「시술현황 맵」 페이지 없음. 미바인딩 색 0(모든 스크립트 `unbound: 0`).

| 그룹 | 세트 (variant 수) |
|---|---|
| G1 | Icon 26 · Checkbox 4 · SelectAll 4 · Search 6 · Textarea 2 |
| G2 | Badge 5 · Avatar 4 · Tooltip 1 · Notify 1 |
| G3 | Button 12 · IconButton 5 · Tab 6 · MenuRow 2 |
| G4 | ProcRow 8 · LinkBar 1 · RoomCard 8 |
| G5 | CardRow 2 · InboxSectionHead 4 · InboxCard 6 · EmptyState 1 |
| G6 | PopOption 3 · Popover 2 · ComboOption 3 · MoreMenu 2 · ChartModal 1 · ConfirmDialog 1 |

합성 세트(G4~G6)는 1차 세트를 인스턴스로 쓴다(Checkbox · Button · IconButton · Badge · Avatar · Search · Textarea · Tab · MenuRow · SelectAll + ProcRow · LinkBar · CardRow · PopOption · ComboOption). 인스턴스 135.
글자 자리: 주 글자 `label`, 여럿이면 `label/<역할>`(예 ProcRow `label/doctor` · `label/status` · `label/time` · RoomCard `label/name` · `label/memo` · InboxCard `label/customer` · `label/call`).

변수(컬렉션 `medikit`): 29 → **64**. 추가 35 = `status/*` 시안 고객 상태색 24(consult-wait · consult · proc-wait · proc · going-wait · gone × DEFAULT/100/300/500 · 접수 = primary 라 뺌) + `status/*-8` Badge 합성 면 4 + `crm/*` 7(surface-head · badge-gray · 원장 아바타 tone 테두리 · 연두). 기존 29개 값은 그대로.

## 린트 — 전 / 후

전(시작 시점 · 앱 lint 도구 · 페이지별):

| 페이지 | 오류 | 경고 | 정보 | 규칙(오류·경고) |
|---|---|---|---|---|
| Page 1 | 0 | 0 | 0 | — |
| medikit | 0 | 60 | 242 | min-text-size 60 |
| components(앞 판) | 15 | 5 | 10 | color-contrast 15 · min-text-size 5 |

후(최종 · headless `lint medikit.fig --json` · 문서 전체):

| 페이지 | 오류 | 경고 | 정보 |
|---|---|---|---|
| Page 1 | 0 | 0 | 0 |
| medikit | 0 | 2 | 3 |
| components | 55 | 31 | 354 |
| **합** | **55** | **33** | **357** |

정보 중 `no-default-names` 0 · `no-hardcoded-colors` 0 · `no-groups` 0. 나머지 정보는 시안 여백 · 모서리가 척도 밖(consistent-spacing 161 · radius 7) · 줄높이 반올림 · 가운데 정렬로 생긴 소수 위치(pixel-perfect 58) · 깊은 중첩(98 · 합성 세트 인스턴스) · 효과 스타일 없음(24 · 0.16.0 에 effect style API 없음) · SVG 아이콘 프레임(prefer-auto-layout 9).

**오류 · 경고는 전부 시안 값 그대로라 남은 것 — 코디 지시로 색 · 크기를 바꾸지 않았다(사용자 결정 대기).**

color-contrast 55(대비 → 건수 · 세트):
| 대비 | 조합 | 건수 | 세트 |
|---|---|---|---|
| 3.39:1 | primary 글자 on white / white 글자 on primary | 20 | Button 6 · Tab 3 · ProcRow 3 · LinkBar 3 · InboxCard 3 · Badge 1 · Notify 1 |
| 2.65:1 | gray/600 on white(placeholder · 기본 탭 · disabled · 팝오버 라벨) | 19 | Search 6 · Popover 4 · Tab 3 · Textarea 2 · Button 2 · MenuRow 1 · ComboOption 1 |
| 3.14:1 | primary on primary/100(선택 줄 · tone0 · filled) | 6 | PopOption 2 · Avatar 1 · Button 1 · ProcRow 1 · ComboOption 1 |
| 3.25:1 | red on white(늦은 호출) | 3 | ProcRow 2 · InboxCard 1 |
| 3.17:1 | primary on crm/surface-head(link-to) | 1 | RoomCard |
| 3.11 · 2.96 · 2.12:1 | Badge 글자 on 합성 면(primary · red · going-wait) | 3 | Badge |
| 2.39:1 | gray/600 on gray/200(disabled) | 1 | Button |
| 3.71 · 2.71:1 | purple on purple/100 · doctor-green on green-100 | 2 | Avatar |

min-text-size 24: 10px — RoomCard 메모 7 · Popover 라벨 4 · Avatar 3 · PopOption 3 · 키트 typo/meta-sm 2 / 11px — Badge 5.
touch-target-size 9: ProcRow 체크박스 16×16 6 · Popover 닫기 16×16 2 · RoomCard held link-to 72×16 1(시안의 실제 누르는 크기).
코디 결정으로 이미 없앤 것: Icon 이름 오탐 2(→ `icon/chain-white-16` · `icon/clear-20`) · RoomCard `link-bar` 이름 오탐 1(→ `moved-from-bar`) · Badge 8% 면 거짓 대비 4(→ 합성 단색).

## run-all 두 번 — 노드 수

headless(`components/run-all.sh` 기본 = `eval medikit.fig -w`):
| 회 | 걸린 시간 | 결과 | `info` |
|---|---|---|---|
| 1 | 58초(eval 28번 · 각 1~3초) | 26 섹션 · 노드 1208 | 3 pages · 1465 nodes(components 1208 · medikit 257 · Page 1 0) |
| 2 | 같음 | 26 섹션 · 노드 1208 | 3 pages · 1465 nodes — **같음(멱등)** |

순서(계약): `_vars.js` → `_reset.js` → Icon Checkbox SelectAll Search Textarea · Badge Avatar Tooltip Notify · Button IconButton Tab MenuRow · ProcRow LinkBar RoomCard · CardRow InboxSectionHead InboxCard EmptyState · PopOption Popover ComboOption MoreMenu ChartModal ConfirmDialog. 토큰 페이지는 `../import-medikit.js`(따로 · 같은 headless 꼴).

## 시안과 다르게 만든 곳 · 시안에 없음 · 코디가 확인할 것

- **Badge solid 면**: 시안 = 글자색 8%(rgba / color-mix). → 흰 바탕 합성 불투명 단색 `status/badge-primary-8 #edf6ff` · `badge-red-8 #fff1f1` · `badge-gray-8 #f4f4f5` · `going-wait-8 #f3faef`(코디 지시). 흰 바탕이 아닌 곳에 놓이면 시안과 달라진다.
- **Icon 이름**: variant `name=icon/<키>`. `link-2-white-16` → `icon/chain-white-16` · `input-delete` → `icon/clear-20`(린트가 link · input 낱말로 오인 · 코디 ③). SVG 는 그대로.
- **시안에만 있는 비상태 색**은 `status/` 대신 `crm/` 접두로 넣었다(surface-head 등) — 브리프는 `status/<이름>` 만 적었다. 코디 확인 필요.
- **줄높이**: 시안 배수(1.3 · 1.5 · 1.6 · 1.273)를 px 로 반올림(12/1.3 → 16 등). `line-height: normal` 은 ×1.193 추정(Notify 13 → 16 · PopOption 12 → 14 · 10 → 12) — G6 이 확인 요청.
- **hover · active(:pressed) 상태는 안 만들었다** — 클래스 상태 · :disabled · 입력 :focus 만.
- 그림자 · 번짐(active 링) 색은 효과라 변수 바인딩 불가 → 값으로.
- Checkbox mixed 막대 8×1.5(시안 left/right 3 기준) · SelectAll 왼쪽 여백 3(padding 2 + checkbox margin 1).
- 효과 이외 하드코딩 색 0 · 미바인딩 0(렌더된 1차 기준).
- 2차 세부(서브에이전트 보고): RoomCard 호출 칸 그라데이션 → 흰 단색 · held 버튼은 늘 보이게 · 시술 줄 3~4줄로 줄임 · ChartModal 제목은 템플릿 꼴 「CHOU YU WEN 저우위원」 · Popover 「전체」 원장 2줄 · InboxCard `.ib-actions` margin -4 → 몸 아래 여백 4 · `inst()` 글자 자리 탐색이 안쪽 인스턴스 label 과 겹칠 수 있어 done-chart 는 label/time · label/customer 로 나눔.
- 뺀 것: `.combo` · `.combo-opt` · `.btn-xs` · `.cbadge.warning` · `.cbadge.outline.red`(CSS 에만 있고 v11 마크업에 없음) · 화면 틀(rail · header · page-controls · seg — 한 번만 나옴 · 필터/보기 바꾸기는 결정 문서가 1차에서 뺌).
- 앱: 「시술현황 맵」 옛 페이지는 지웠다(저장 전). 앱이 보고 있는 페이지를 지우면 CLI 가 사라진 id 를 붙잡아 eval 이 전부 실패 → `documents activate tab-1 --page-id 0:3` 으로 복구. `_reset.js` 는 그래서 페이지를 지우지 않고 비운다.
- **앱 모드 eval 은 쓰지 않는다**: 병렬 1회 · 직렬 2회 「Out of bounds memory access」(앱 WASM 메모리 · 같은 세션에서 생성 · 삭제 반복). 최소 재현은 못 좁혔다 — headless 에서는 run-all 2회 연속(eval 56번)도 오류 없음. 사용자는 앱 탭을 저장 없이 닫고 디스크 파일을 다시 열어야 한다(앱의 옛 상태가 파일을 덮지 않게).
- `import-medikit.js` 변경: 컬렉션을 지우지 않고 변수를 맞추기만(지우면 components 바인딩 · 시안 변수가 끊김) · 페이지 흰 배경 · 모든 레이어 이름 · 라벨 12px · 글자 · 테두리 색 바인딩 · 견본은 컬렉션 변수 전부(64).
