# cc 시술현황 — 화면 목록 · 메디킷 컴포넌트 전수조사

- 조사일: 2026-11-12 · 작성: cc-prototype researcher (task_4d48405c425c)
- 원천: 기획안 `cc-기획안-시술현황.md`(738줄) · 용어 확인 `cc-개요.md` · `cc-개발확인.md` · 메디킷 `harness_works/medikit/src/ui/`(package.json v1.4.0) · `medikit.css`(클래스 정의)
- 정정 1 반영: 기존 시술현황 구현(DAY board 템플릿 · cc-prototype 코드)은 **열지 않았고 근거로 쓰지 않았다.** §6-4 「DAY `.ms-*` 사용처」 열은 삭제했다.

**요약**

1. **화면 56행** — 시술현황 탭 1차 52(화면 1 · 패널 12 · 팝업 11 · 모달 6 · 토스트 2 · 상태 19 · 확인 안 됨 1) + CC 모바일 3(이 탭 밖, 참고) + 고도화 1(1차 범위 밖).
2. **들여올 메디킷 컴포넌트 22종 · 조합 61개**(아이콘 7 포함. 아이콘 빼면 15종 · 54조합).
3. **메디킷에 없는 요소 10개**(§4 끝 「메디킷에 없음」 표). 기획안에 화면 정의가 없는 것 1개(변경 이력)는 따로 「정할 것」으로 뺐다.

**약어**

- `P:L123` = 기획안 `/Users/kknaks/git/ax-clinic-project/para/projects/clinic-myeongdong-ax/phase-1/clinic-os/cc/cc-기획안-시술현황.md` 123줄
- `OV:L123` = 같은 폴더 `cc-개요.md`
- `MK:<경로>:L` = `/Users/kknaks/git/harness_works/medikit/src/ui/<경로>`
- `CSS:L` = `/Users/kknaks/orca/workspaces/kknaks_profile/open-pencil/reference/2026-11-12-open-pencil/medikit/medikit.css`
- 「추정」 = 기획안이 컴포넌트·색·크기를 말하지 않아 내가 고른 것. 근거를 옆에 적었고 확정은 §6.

---

## 1. 화면 목록

`screenId` 는 기획안 절 구조를 따른다: 시술현황 탭 `procedure/…`, 시술 줄 상태 `procedure/treatment-line/…`, CC 모바일 `mobile/…`.

| # | screenId | 이름 | 종류 | 절 | 줄 |
|---|---|---|---|---|---|
| 1 | `procedure/board` | 시술 현황 화면 | 화면 | ## 화면 구성 · 1-1 | P:L5-15, L63-67 |
| 2 | `procedure/board/out-of-hours` | 「조회 시간 밖」 | 상태 | 1-1 예외 1 | P:L172 |
| 3 | `procedure/room-slot` | 관리실 칸(침대 둘 이상이면 침대마다 칸) | 패널 | 1-1 | P:L68 |
| 4 | `procedure/room-slot/occupied` | 「점유 중 · {고객 이름}」 칸 | 상태 | 1-1 · 2-1 | P:L69, L311, L328 |
| 5 | `procedure/customer-card` | 고객 카드 | 패널 | 1-1 | P:L10, L70-77 |
| 6 | `procedure/customer-card/status-waiting` | 카드 상태 「시술 대기 HH:MM」 | 상태 | 1-1 | P:L85 |
| 7 | `procedure/customer-card/status-in-progress` | 카드 상태 「시술 진행」 | 상태 | 1-1 | P:L86 |
| 8 | `procedure/customer-card/status-discharge-wait` | 카드 상태 「귀가 대기 HH:MM」 | 상태 | 1-1 · 5-1 | P:L87, L651-656 |
| 9 | `procedure/customer-card/order-memo` | 고객 카드 오더 메모 | 패널 | 1-1 | P:L72, L110-122 |
| 10 | `procedure/customer-card/anesthesia-idle` | 마취 「마취 시작」 | 상태 | 2-2 | P:L365 |
| 11 | `procedure/customer-card/anesthesia-running` | 마취 「마취중 mm:ss」 · 「마취 종료」 | 상태 | 2-2 | P:L352, L366 |
| 12 | `procedure/treatment-line/waiting` | 시술 줄 대기 | 상태 | 1-1 · 4-1 | P:L74, L516 |
| 13 | `procedure/treatment-line/calling` | 시술 줄 호출 중(전체/지정) | 상태 | 3-1 · 4-1 | P:L402, L517 |
| 14 | `procedure/treatment-line/accepted` | 시술 줄 수락 | 상태 | 3-2 · 4-1 | P:L440, L471, L518 |
| 15 | `procedure/treatment-line/not-proceeding` | 시술 줄 시술 미진행(확인 전) | 상태 | 1-1 · 4-1 | P:L141, L519 |
| 16 | `procedure/treatment-line/in-progress` | 시술 줄 진행 중 | 상태 | 4-1 | P:L520 |
| 17 | `procedure/treatment-line/done` | 시술 줄 완료 | 상태 | 1-1 · 4-1 | P:L135, L505, L521 |
| 18 | `procedure/customer-card/line-changed` | 「변경」 · 카드 머리 「변경 n건」 | 상태 | 1-1 | P:L139, L144 |
| 19 | `procedure/customer-card/new-lines` | 구분선 뒤 새 시술 줄 | 상태 | 1-1 | P:L135, L140 |
| 20 | `procedure/customer-card/call-bar` | 시술 선택 · 원장 호출(「전체 선택」 · 「전체 호출 · n개」 · 「지정 호출 · n개」 · 「지정 원장 · {원장}」) | 패널 | 1-1 · 3-1 | P:L75-76, L386, L417 |
| 21 | `procedure/customer-card/confirm-flag` | 고객 카드의 「확인할 일」 글자 | 상태 | 1-3 | P:L245, L262 |
| 22 | `procedure/search` | 고객 검색 | 패널 | 1-2 | P:L176-187, L195 |
| 23 | `procedure/search/results` | 검색 결과 | 팝업 | 1-2 | P:L196, L199-207 |
| 24 | `procedure/search/empty` | 「검색 결과 없음」 | 상태 | 1-2 | P:L186, L197 |
| 25 | `procedure/confirm-needed` | 「확인 필요」 | 패널 | 1-3 | P:L239, L255 |
| 26 | `procedure/confirm-needed/card` | 확인 필요 카드(상황 6종) | 패널 | 1-3 | P:L256-261, L268-275 |
| 27 | `procedure/toast/alert` | 시술 현황 화면 알림(확인 필요 · 원장 수락 · 바뀐 시술) | 토스트 | 1-1 · 1-3 | P:L162-163, L281 |
| 28 | `procedure/room-move/menu` | 관리실 이름 누름 →「점유 이동」 · 「다른 관리실로 이동」 · 「원래 관리실로 복귀」 | 팝업 | 2-1 | P:L297, L325 |
| 29 | `procedure/room-move/list` | 관리실 이동 목록(빈 관리실 · 「A-룸2 (1/2)」) | 팝업 | 2-1 | P:L298, L326-327 |
| 30 | `procedure/room-move/list-empty` | 「빈 관리실 없음」 | 상태 | 2-1 | P:L327 |
| 31 | `procedure/toast/room-full` | 「그 관리실에 자리가 없습니다」 | 토스트 | 2-1 예외 1 | P:L342 |
| 32 | `procedure/doctor-list/designate-call` | 원장 목록 — 지정 호출 | 팝업 | 3-1 | P:L389, L418 |
| 33 | `procedure/doctor-list/start-pick` | 원장 목록 — 전체 호출 중 「시작」 | 팝업 | 4-1 | P:L502, L541, L543 |
| 34 | `procedure/doctor-list/reassign` | 원장 목록 — 원장 이름 눌러 담당 원장 바꾸기 | 팝업 | 3-2 | P:L443, L471-472 |
| 35 | `procedure/treatment-line/more-menu` | 줄 「⋯」 더보기(「시작 취소」 · 「완료 취소」) | 팝업 | 4-1 | P:L493, L545-546 |
| 36 | `procedure/customer-card/more-menu` | 카드 「⋯」 더보기(「귀가 대기 취소」) | 팝업 | 5-1 | P:L493, L656 |
| 37 | `procedure/confirm/cancel-start` | 확인 창 「{시술} 시작을 취소할까요?」 | 모달 | 4-1 | P:L545, L547 |
| 38 | `procedure/confirm/cancel-complete` | 확인 창 「{시술} 완료를 취소할까요?」 | 모달 | 4-1 | P:L506, L546-547 |
| 39 | `procedure/chart` | 시술 차트 | 모달 | 4-2 | P:L14, L586-599 |
| 40 | `procedure/chart/order-memo` | 시술 차트 오더 메모(펼치기 · 접기 · 마지막 고친 시각) | 패널 | 4-2 | P:L589 |
| 41 | `procedure/chart/doctor-chart` | 「의사 차트」(담당자 · 글 칸) | 패널 | 4-2 | P:L592, L605 |
| 42 | `procedure/chart/nursing-chart` | 「간호관리차트」(직원 칸 · 「칸 지우기」) | 패널 | 4-2 | P:L593-594, L606 |
| 43 | `procedure/chart/author-picker` | 「작성자 추가」 직원 목록 | 팝업 | 4-2 | P:L576, L593 |
| 44 | `procedure/chart/apply-all-confirm` | 「전체 시술에 내용 적용」 확인 창(적용 수 · 제외 수) | 모달 | 4-2 | P:L577, L617 |
| 45 | `procedure/chart/discard-confirm` | 확인 창 「저장하지 않고 닫을까요?」 | 모달 | 4-2 | P:L579, L596-598 |
| 46 | `procedure/chart/conflict-notice` | 「다른 직원이 먼저 저장한 줄은 저장하지 않았습니다」 | 상태 | 4-2 예외 1 | P:L631 |
| 47 | `procedure/chart/past-visits` | 지난 방문 기록 | 패널 | 4-2 | P:L599 |
| 48 | `procedure/chart/change-history` | 변경 이력 | 확인 안 됨 | 1-1 · 1-3 | P:L135, L144, L261 |
| 49 | `procedure/room-log` | 관리실 기록 창 | 모달 | 6-1 | P:L15, L676-692 |
| 50 | `procedure/room-log/date-calendar` | 날짜 · 「이전 날」 · 「다음 날」 · 달력 | 팝업 | 6-1 | P:L677, L687 |
| 51 | `procedure/room-log/room-select` | 관리실 고르기(「모든 관리실」) | 팝업 | 6-1 | P:L678, L688 |
| 52 | `procedure/room-log/room-group` | 관리실 묶음(고객 줄 · 시술 줄) | 패널 | 6-1 | P:L689-691, L694-710 |
| 53 | `mobile/call-accept` | CC 모바일 의사 호출 알림 · 「수락」 | 화면(탭 밖) | 3-2 | P:L13, L469-470 |
| 54 | `mobile/toast/taken` | 「다른 원장이 먼저 받았습니다」 | 토스트(탭 밖) | 3-2 예외 1 | P:L486 |
| 55 | `mobile/toast/canceled` | 「취소된 호출입니다」 | 토스트(탭 밖) | 3-2 예외 2 | P:L487 |
| 56 | `procedure/consultant-call` | 관리실별 상담실장 호출(고도화 · 1차 범위 밖) | 범위 밖 | 7-1 | P:L734-738 |
| — | `procedure/_glossary` | 용어(화면 아님 · 맵에 붙일 참조) | 참조 | ## 용어 | P:L17-42 |

- 48 `change-history`: 「시술 차트의 변경 이력」(P:L135)·「바뀐 줄의 변경 이력을 연다」(P:L144, L261)라고만 하고, 시술 차트 화면 구성(P:L586-599)에 칸이 없다 → 종류·위치 **확인 안 됨**, §6 #2.
- 53-55: 화면 구성 표(P:L13)에 있지만 본 화면은 CC 모바일(CC-24) 몫이다. 맵에 붙일지는 §6 #3.
- `OV:L132`: 시술 현황은 「의국 화면」과 「관리실별 화면」 두 개라고 한다. 시술현황 기획안은 7-1(고도화, P:L738)에서만 둘을 나눈다 → §6 #4.

**절 커버리지(검증 — 빠진 절 0)**

| 기획안 절 | 줄 | 1의 행 |
|---|---|---|
| ## 화면 구성 | P:L5 | 1 |
| ## 용어 | P:L17 | `_glossary` |
| ## 1. 시술 현황 보기 / ### 1-1 | P:L46 / L48 | 1-21 |
| ### 1-2 | P:L174 | 22-24 |
| ### 1-3 | P:L237 | 21, 25-27 |
| ## 2. 시술 준비 / ### 2-1 | P:L287 / L289 | 4, 28-31 |
| ### 2-2 | P:L344 | 10-11 |
| ## 3. 호출 / ### 3-1 | P:L376 / L378 | 13, 20, 32 |
| ### 3-2 | P:L430 | 14, 34, 53-55 |
| ## 4. 시술 진행 / ### 4-1 | P:L489 / L491 | 12-17, 33, 35, 37-38 |
| ### 4-2 | P:L562 | 39-47 |
| ## 5. 귀가 대기 / ### 5-1 | P:L635 / L637 | 8, 36 |
| ## 6. 관리실 기록 보기 / ### 6-1 | P:L666 / L668 | 49-52 |
| ## 7. 고도화 / ### 7-1 | P:L732 / L734 | 56 |

---

## 2. 화면별 정책 위치(줄 범위만)

| screenId | 정책 · 예외 · 상태 규칙 줄 |
|---|---|
| `procedure/board` | P:L156-166(1-1 정책 3 · 7 · 8) · L52-61(흐름) |
| `procedure/board/out-of-hours` | P:L168-172 |
| `procedure/room-slot` · `/occupied` | P:L160(정책 3) · L305-311 · L313-319 · L330-336(2-1 정책 1-3) |
| `procedure/customer-card` · `status-*` | P:L79-100(카드 상태 · 바뀌는 때) · L161 · L164 · L166(정책 4 · 8 · 11) · L102-108(고객 정보 값) |
| `procedure/customer-card/order-memo` | P:L110-122 · L165(정책 10) |
| `procedure/customer-card/anesthesia-*` | P:L355-359 · L368-372(2-2 정책 2) |
| `procedure/treatment-line/*` | P:L124-131 · L133-142 · L146-154 · L510-534 · L549-560(4-1 정책 1-8) |
| `procedure/customer-card/line-changed` · `new-lines` | P:L133-144 · L162(정책 6) |
| `procedure/customer-card/call-bar` | P:L146-154 · L396-410 · L421-428(3-1 정책 1 · 3 · 5 · 8) |
| `procedure/customer-card/confirm-flag` · `procedure/confirm-needed` · `/card` | P:L264-275(확인할 상황) · L277-283(1-3 정책 1-3) |
| `procedure/toast/alert` | P:L163(1-1 정책 7) · L162(정책 6) · L281(1-3 정책 1) |
| `procedure/search` · `/results` · `/empty` | P:L199-218(값 · 검색 기준) · L220-229(정책) · L231-235(예외) |
| `procedure/room-move/*` · `procedure/toast/room-full` | P:L305-319 · L330-342 |
| `procedure/doctor-list/*` | P:L396-403 · L426(3-1 정책 3) · L474-480(3-2 정책) · L553(4-1 정책 1) |
| `procedure/treatment-line/more-menu` · `procedure/confirm/*` | P:L523-534 · L556-559(4-1 정책 4 · 6 · 7) |
| `procedure/customer-card/more-menu` | P:L641-649(흐름) · L658-662(5-1 정책 2) |
| `procedure/chart` · 하위 | P:L601-606(차트 칸) · L608-625(4-2 정책) · L627-631(예외) |
| `procedure/room-log` · 하위 | P:L694-710(값) · L712-720(남는 때) · L722-728(6-1 정책) |
| `mobile/*` | P:L456-463 · L474-487 |
| `procedure/consultant-call` | P:L736-738(정책 미정 — 「다음 스펙에서 정한다」) |

---

## 3 · 4. 화면별 UI 요소 → 메디킷 대응

3(요소와 기획안 근거)과 4(메디킷 대응)를 한 표로 합쳤다. 정정 1에 따라 DAY `.ms-*` 사용처 열은 없다. 메디킷 HTMX 클래스판에 같은 클래스가 있으면 「CSS」 열에 정의 줄을 적었다.

공통 근거(아래 표에서 줄만 적는다)

- Button: variant `solid|filled|outlined|text|icon|fillOutlined` MK:button/button.tsx:L107-113 · color `blue|red|yellow|black|gray` L114 · size `xl|l|m|s|ss` L117 · disabled L78 · L312 · 색 맵 L140-190
- Badge: variant `neutral|primary|warning|danger|purple` MK:badge/badge.tsx:L4 · size `md|sm` L5 · `dot` L16
- Checkbox: `disabled` · `data-[state=checked]` MK:checkbox/checkbox.tsx:L18-19
- Card: `interactive` · `selected` · `indicator` · `padding` MK:card/card.tsx:L12-25
- Popover: `side` · `align` MK:popover/popover.tsx:L15-35
- Command: List L75 · Empty L87 · Item L126 · item disabled L133 (MK:command/command.tsx)
- RadioGroup: MK:radio/radio.tsx:L6 · L18 · disabled L28
- ConfirmModal: variant `check|success|warning|caution|error|loading` MK:modal/confirm-modal.tsx:L44-50 · leftButton L59 · rightButton L61
- BaseModal: `title` · `onClose` · `hasCloseButton` · `shouldCloseOnBackdropClick` MK:modal/base-modal.tsx:L11-15
- Notify: variant `success|error` · size `default|sm` MK:notify/notify.tsx:L10-11 · 컨테이너 top-center MK:notify/notify-container.tsx:L30
- Banner: variant `primary|warning|danger|neutral` MK:banner/banner.tsx:L12 · action L19 · onClose L21

| screenId | UI 요소 | 기획안 근거 | 메디킷 컴포넌트 | 필요한 variant · size · state | 소스 근거 | CSS |
|---|---|---|---|---|---|---|
| `procedure/board` | 현황 메뉴의 탭 줄(예약 현황 · 원내 현황 · 시술 현황) | P:L1, L21 | Tabs | 선택 탭 1 · 기본 | MK:tab/tab.tsx:L10-15 | CSS:L119-125 |
| `procedure/board` | 「관리실 기록」 버튼 | P:L67, L686 | Button | outlined · gray · s(추정) | 공통 | CSS:L36-37, L48 |
| `procedure/board` | 관리실마다 칸을 둔 판 | P:L68 | **메디킷에 없음**(보드 그리드) | — | src/ui 40종에 보드 · 칸 레이아웃 없음(ls 확인) | — |
| `procedure/board/out-of-hours` | 「조회 시간 밖」 | P:L172 | Banner(추정) | neutral | MK:banner/banner.tsx:L12 | CSS:L93 · 빈 상태면 `.ms-empty` CSS:L105 |
| `procedure/room-slot` | 침대별 칸 | P:L68 | **메디킷에 없음**(보드 칸) | — | 위와 같음 | — |
| `procedure/room-slot/occupied` | 「점유 중 · {이름}」(누르면 복귀) | P:L69, L328 | **메디킷에 없음**(칸 자리표시). 누르는 부분만 Button 으로 대체 가능 | 대체안 filled · gray · s(추정) | MK:button/button.tsx:L149-155 | CSS:L42-43 |
| `procedure/customer-card` | 카드 틀 | P:L70-77 | Card | padding sm · 기본 / 「잠깐 강조」 때 selected + indicator none(추정) | MK:card/card.tsx:L14, L18, L25 | CSS:L96-98 |
| `procedure/customer-card` | 관리실 이름(누르면 이동 메뉴) | P:L70, L325 | Button | text · black · s · 귀가 대기 카드에선 눌러도 아무 일 없음 → disabled(추정) | 공통 | CSS:L44-45 |
| `procedure/customer-card` | 고객 이름(누르면 시술 차트) | P:L71 | Button | text · black · s | 공통 | CSS:L44-45 |
| `procedure/customer-card` | 국적 · 담당 상담실장 글자 | P:L71 | 텍스트 토큰(컴포넌트 아님) | — | — | CSS:L25-30 |
| `procedure/customer-card` | 「통역 필요 {언어}」 | P:L71, L107 | Badge | purple · sm(추정) | 공통 | CSS:L79, L83 |
| `procedure/customer-card/status-waiting` | 「시술 대기 HH:MM」 | P:L85 | Badge | neutral · sm(추정) | 공통 | CSS:L78-79 |
| `procedure/customer-card/status-in-progress` | 「시술 진행」 | P:L86 | Badge | primary · sm(추정) | 공통 | CSS:L80 |
| `procedure/customer-card/status-discharge-wait` | 「귀가 대기 HH:MM」 | P:L87, L656 | Badge | warning · sm(추정) | 공통 | CSS:L81 |
| `procedure/customer-card/status-discharge-wait` | 「귀가 대기 취소」 | P:L87(카드 상태 옆) · L656(「⋯」 안) | Button 또는 메뉴 항목 | 위치가 두 줄에서 다르다 → §6 #5 | — | — |
| `procedure/customer-card/order-memo` | 오더 메모 항목 7종(「자가세안 x」 · 「OUT TIME」 · 결제 표시 · 「지정 {원장}」 · 전체 요청 · 「특이사항 · {글}」 · 「임플란트 O」) | P:L114-122 | Badge 또는 Chip(읽기 전용) | Badge neutral · sm(추정) / Chip xs(onRemove 없이) | MK:badge/badge.tsx:L4-5 · MK:chip/chip.tsx:L6, L13-16 | CSS:L78-79 · L84 |
| `procedure/customer-card/anesthesia-idle` | 「마취 시작」 | P:L365 | Button | outlined · blue · ss(추정) | 공통 | CSS:L36, L49 |
| `procedure/customer-card/anesthesia-running` | 「마취중 mm:ss」(초 단위로 셈) | P:L352, L366 | **메디킷에 없음**(타이머) | — | src/ui 에 타이머 없음 | — |
| `procedure/customer-card/anesthesia-running` | 「마취 종료」 | P:L366 | Button | outlined · gray · ss(추정) | 공통 | CSS:L38-39, L49 |
| `procedure/treatment-line/*` | 2단 줄(윗단 [이벤트] · 시술명 · 괄호 · 줄 버튼 / 아랫단 상태 글자) | P:L74 | **메디킷에 없음**(줄 행) | — | src/ui 에 리스트 행 없음. Table 행으로 근사 가능(MK:table/table.tsx:L94) | — |
| `procedure/treatment-line/*` | 「[이벤트]」 | P:L128 | Badge(추정) — 기획안은 「시술명 앞 [이벤트]」 글자만 말함 | primary · sm | 공통 | CSS:L80 |
| `procedure/treatment-line/waiting` | 체크박스(고를 수 있음) | P:L150, L516 | Checkbox | unchecked · checked | MK:checkbox/checkbox.tsx:L19 | CSS:L69-71 |
| `procedure/treatment-line/waiting` | 「시작」 | P:L516, L540 | Button | solid · blue · ss(추정) | 공통 | CSS:L34-35, L49 |
| `procedure/treatment-line/calling` | 체크박스 비활성 | P:L151, L517 | Checkbox | disabled | MK:checkbox/checkbox.tsx:L18 | CSS:L74 |
| `procedure/treatment-line/calling` | 「호출 중 n분」 · 「{원장} 호출 중 n분」 | P:L402, L517 | **메디킷에 없음**(경과 시간 표시 — 타이머와 같은 항목) | — | — | — |
| `procedure/treatment-line/calling` | 「시작」 · 「재호출」 | P:L419, L517, L541 | Button | 시작 solid · blue · ss / 재호출 outlined · gray · ss(추정) | 공통 | CSS:L34-39, L49 |
| `procedure/treatment-line/accepted` | 「{원장} 수락 완료 HH:MM」 · 원장 이름(간호사 계정만 눌림) | P:L471, L518 | Button(이름 부분) | text · black · ss · 원장 계정이면 disabled(추정) | 공통 | CSS:L44-45 |
| `procedure/treatment-line/accepted` | 「시작」 · 체크박스 없음 | P:L518 | Button | solid · blue · ss | 공통 | CSS:L34-35 |
| `procedure/treatment-line/not-proceeding` | 비활성 「시술 미진행」 줄 | P:L141, L519 | **메디킷에 없음**(비활성 줄). 글자 부분만 Badge neutral 로 대체 가능(추정) | — | — | — |
| `procedure/treatment-line/in-progress` | 「{원장} · 진행 mm:ss」 | P:L520 | **메디킷에 없음**(타이머) · 원장 이름은 Button text | — | — | — |
| `procedure/treatment-line/in-progress` | 「종료」 | P:L520, L544 | Button | outlined · blue · ss(추정) | 공통 | CSS:L36-37 |
| `procedure/treatment-line/in-progress` · `/done` | 「⋯」 더보기 | P:L520-521, L545-546 | Button + MoreIcon | icon · gray · ss | 공통 · MK:icons/index.ts:L24 | CSS:L44-45 |
| `procedure/treatment-line/done` | 완료 체크 표시(눌리지 않음) · 회색 글자 · 「{원장} · n분」 | P:L135, L154, L521 | Checkbox | checked + disabled | MK:checkbox/checkbox.tsx:L18-19 | CSS:L71, L74 |
| `procedure/customer-card/line-changed` | 줄의 「변경」 | P:L139 | Badge | warning · sm(추정) | 공통 | CSS:L81 |
| `procedure/customer-card/line-changed` | 카드 머리 「변경 n건」(누르면 변경 이력) | P:L144 | Button 또는 Badge(눌림) | Button filled · yellow · ss(추정) | MK:button/button.tsx:L149-155 | CSS:L42-43 |
| `procedure/customer-card/new-lines` | 기존 줄 아래 구분선 | P:L135, L140 | Divider | horizontal | MK:divider/divider.tsx:L10-15 | — |
| `procedure/customer-card/call-bar` | 「전체 선택」(대기 줄 없으면 비활성) | P:L75 | Button(또는 Checkbox+글자) | text · blue · ss · disabled | 공통 | CSS:L44-45 |
| `procedure/customer-card/call-bar` | 「전체 호출 · n개」 | P:L76, L417 | Button | solid · blue · s(추정) | 공통 | CSS:L34-35, L48 |
| `procedure/customer-card/call-bar` | 「지정 호출 · n개」 | P:L76, L417 | Button | outlined · blue · s(추정) | 공통 | CSS:L36-37, L48 |
| `procedure/customer-card/call-bar` | 「지정 원장 · {원장}」 | P:L386, L417 | Badge(추정) | primary · sm | 공통 | CSS:L80 |
| `procedure/customer-card` | 「귀가 대기」 | P:L77, L655 | Button | solid · blue · s(추정) | 공통 | CSS:L34-35 |
| `procedure/customer-card/confirm-flag` | 「대기 n분째」 · 「호출 n분째」 · 「시술 변경 n건」 등(누르면 확인 필요 카드 강조) | P:L262 | Badge(눌림 — Button 으로 감싸기, 추정) | danger · sm(추정) | 공통 | CSS:L82 |
| `procedure/search` | 검색어 칸 | P:L195 | Input | size m · icon SearchIcon · allowClear(「검색어를 지우면 닫힌다」 P:L187) | MK:input/input.tsx:L15-18, L28, L34, L36 | CSS:L58-59 |
| `procedure/search/results` | 결과 목록(행: 이름 · 국적 · 최근 방문일 · 관리실 · 시술 이름 · 「외 n건」) | P:L196, L228 | Popover + Command(List · Item) | 기본 · hover | MK:popover/popover.tsx:L15 · MK:command/command.tsx:L75, L126 | — (CSS 판에 없음) |
| `procedure/search/results` | 결과 한 행의 5값 배치 | P:L196 | **메디킷에 없음**(Command Item 은 한 줄 글자) | — | MK:command/command.tsx:L126-145 | — |
| `procedure/search/empty` | 「검색 결과 없음」 | P:L197 | Command Empty | — | MK:command/command.tsx:L87 | CSS:L105(`.ms-empty`) |
| `procedure/confirm-needed` | 카드 묶음 영역(오래된 순) | P:L255, L283 | 레이아웃(컴포넌트 아님) | — | — | — |
| `procedure/confirm-needed/card` | 카드 틀 · 「잠깐 강조」 | P:L255-256, L262 | Card | padding sm / 강조 = selected + indicator none(추정) | MK:card/card.tsx:L14, L18 | CSS:L96 |
| `procedure/confirm-needed/card` | 관리실 이름 · 고객 이름(누르면 고객 카드 강조) | P:L256 | Button | text · black · s | 공통 | CSS:L44 |
| `procedure/confirm-needed/card` | 「재호출」 · 「다시 알림」 · 「귀가 대기」 · 「변경 확인」 | P:L258-261 | Button | outlined · blue · ss(추정) | 공통 | CSS:L36, L49 |
| `procedure/confirm-needed/card` · `procedure/customer-card` | 「잠깐 강조」 효과 | P:L256, L262 | **메디킷에 없음**(일시 강조 모션) | — | — | — |
| `procedure/toast/alert` | 「{관리실} {이름} {확인할 일}」 알림 · 원장 수락 · 바뀐 시술 알림 | P:L163, L281 | Notify — **정보형 variant 없음**(success · error 뿐) | — | MK:notify/notify.tsx:L10 | — (CSS 판에 없음) |
| `procedure/room-move/menu` | 「점유 이동」 · 「다른 관리실로 이동」 · 「원래 관리실로 복귀」 메뉴 | P:L297, L325 | **메디킷에 없음**(드롭다운 메뉴. Menu 는 사이드 내비 `aside`). 대체: Popover + Button text 세로 목록 | text · black · s | MK:menu/menu.tsx:L22-35, L60 · MK:popover/popover.tsx:L15 | — |
| `procedure/room-move/list` | 빈 관리실 목록 · 「A-룸2 (1/2)」 · 바깥 누르면 닫힘 | P:L327 | Popover + Command(List · Item) | 기본 · hover · (자리 없는 관리실은 목록에서 빠지므로 disabled 불필요 P:L334) | MK:command/command.tsx:L75, L126 | — |
| `procedure/room-move/list-empty` | 「빈 관리실 없음」 | P:L327 | Command Empty | — | MK:command/command.tsx:L87 | — |
| `procedure/toast/room-full` | 「그 관리실에 자리가 없습니다」 | P:L342 | Notify | error · default | MK:notify/notify.tsx:L10-11 | — |
| `procedure/doctor-list/designate-call` | 그날 근무 원장 목록(지정 원장이 맨 위에 골라진 채) · 「호출」(고르기 전 비활성) · 바깥 누르면 닫힘 | P:L389, L418 | Popover + RadioGroup + Button | Radio checked/unchecked · Button solid · blue · s · disabled | MK:radio/radio.tsx:L6, L18 · 공통 | CSS:L72-73 · L34 |
| `procedure/doctor-list/start-pick` | 원장 목록(본인 → 지정 원장 순) · 고르면 바로 시작 | P:L543 | Popover + Command(List · Item) | 기본 · hover | MK:command/command.tsx:L126 | — |
| `procedure/doctor-list/reassign` | 원장 목록 · 고르면 담당 원장 바뀜 | P:L472 | Popover + Command(List · Item) | 기본 · 현재 원장 표시(CheckIcon, 추정) | MK:command/command.tsx:L126 · MK:icons/index.ts | — |
| `procedure/treatment-line/more-menu` | 「시작 취소」 / 「완료 취소」 항목 | P:L545-546 | **메디킷에 없음**(드롭다운 메뉴) — 대체 Popover + Button text | text · black · s | 위 room-move/menu 와 같음 | — |
| `procedure/customer-card/more-menu` | 「귀가 대기 취소」 항목 | P:L656 | 위와 같음 | text · black · s | 같음 | — |
| `procedure/confirm/cancel-start` | 「{시술} 시작을 취소할까요?」 · 「시작 취소」 · 「닫기」 | P:L545, L547 | ConfirmModal | variant caution(추정) · leftButton 「닫기」 · rightButton 「시작 취소」 | MK:modal/confirm-modal.tsx:L44-50, L59, L61 | CSS:L108-115 |
| `procedure/confirm/cancel-complete` | 「{시술} 완료를 취소할까요?」 · 「완료 취소」 · 「닫기」 | P:L546-547 | ConfirmModal | 위와 같음 | 같음 | CSS:L108-115 |
| `procedure/chart` | 창 틀 · 「닫기」 · 창 바깥(쓴 것 있으면 무시) | P:L596 | BaseModal | hasCloseButton false(「닫기」는 버튼, 추정) · shouldCloseOnBackdropClick 조건부 | MK:modal/base-modal.tsx:L11-15 | CSS:L108-115(폭 560 고정) |
| `procedure/chart` | 한국어 발음 · 차트 번호 · 「주의 · 불만」 | P:L588 | 텍스트 + Badge | danger · sm(추정) | 공통 | CSS:L82 |
| `procedure/chart` | 시술 줄마다 시술 이름 · 진행한 관리실 · 담당 원장 | P:L590 | 텍스트 / Table(추정) | — | MK:table/table.tsx:L13, L94, L132 | CSS:L99-104 |
| `procedure/chart` | 마취 회차 · 이번 방문 관리실 기록 | P:L591 | Table(추정) | — | 같음 | CSS:L99-104 |
| `procedure/chart` | 「저장」(고친 것 있을 때만) | P:L595 | Button | solid · blue · l · disabled | 공통 | CSS:L34, L46 |
| `procedure/chart` | 「닫기」 | P:L596 | Button | outlined · gray · l | 공통 | CSS:L38, L46 |
| `procedure/chart` | 「고객 차트」 | P:L598 | Button | text · blue · s(추정) | 공통 | CSS:L44 |
| `procedure/chart/order-memo` | 「오더 메모」 · 「마지막 고친 시각」 · 펼치기/접기(처음 펼침) | P:L589, L613 | Accordion | size md · open/closed | MK:accordion/accordion.tsx:L12, L21 | — |
| `procedure/chart/doctor-chart` | 담당자 고르기 | P:L592, L605 | ComboBox(single) | size m · hasAllOption false · 빈 값 placeholder | MK:combobox/combobox.tsx:L25, L48, L50, L58, L67 | CSS:L62, L65(select) |
| `procedure/chart/doctor-chart` | 글 칸(예시 글 placeholder) | P:L592, L605 | Textarea | 기본 · placeholder | MK:textarea/textarea.tsx:L11-15 | — |
| `procedure/chart/doctor-chart` · `nursing-chart` | 「전체 시술에 내용 적용」 | P:L592, L594 | Button | outlined · gray · ss(추정) | 공통 | CSS:L38, L49 |
| `procedure/chart/nursing-chart` | 「작성자 추가」 | P:L593 | Button + PlusIcon | text · blue · s | 공통 · MK:icons/ (plus-icon.tsx) | CSS:L44 |
| `procedure/chart/nursing-chart` | 직원 이름 · 글 칸 | P:L594 | Label + Textarea | — | MK:label/label.tsx:L10-15 · MK:textarea/textarea.tsx:L11 | CSS:L56 |
| `procedure/chart/nursing-chart` | 「칸 지우기」(저장 전 칸만) | P:L594 | Button + DeleteIcon(추정 — 기획안은 문구 「칸 지우기」) | icon · gray · ss | 공통 · MK:icons/ (delete-icon.tsx) | — |
| `procedure/chart/author-picker` | 오늘 근무 간호사 · 피부관리팀 이름 목록 | P:L593, L625 | Popover + Command(List · Item) · 이미 있는 사람 disabled(「한 줄에 같은 사람 칸은 하나」 P:L625, 추정) | 기본 · disabled | MK:command/command.tsx:L126, L133 | — |
| `procedure/chart/apply-all-confirm` | 적용 수 · 제외 수 확인 창 | P:L577, L617 | ConfirmModal | check(추정) · 좌우 버튼(문구 기획안에 없음 → §6 #7) | MK:modal/confirm-modal.tsx:L44-61 | CSS:L108-115 |
| `procedure/chart/discard-confirm` | 「저장하지 않고 닫을까요?」 · 「계속 쓰기」 · 「버리고 닫기」 | P:L579, L597 | ConfirmModal | warning(파괴적, 추정) · leftButton 「계속 쓰기」 · rightButton 「버리고 닫기」 | MK:modal/confirm-modal.tsx:L44-61 | CSS:L108-115 |
| `procedure/chart/conflict-notice` | 창 안 알림 글 | P:L631 | Banner | warning | MK:banner/banner.tsx:L12 | CSS:L91 |
| `procedure/chart/past-visits` | 날짜 · 시술 · 의사 차트 · 간호관리차트 / 켜기 전은 날짜 · 시술 · 원장 | P:L599, L614 | Table(추정) | — | MK:table/table.tsx:L13 | CSS:L99-104 |
| `procedure/chart/change-history` | 확인 안 됨 | P:L135, L144 | 확인 안 됨 | — | — | — |
| `procedure/room-log` | 창 틀 · 「닫기」 · 창 바깥 | P:L680, L692 | BaseModal | shouldCloseOnBackdropClick true · 「닫기」 Button outlined gray l | MK:modal/base-modal.tsx:L11-15 | CSS:L108-115 |
| `procedure/room-log/date-calendar` | 날짜 · 달력 | P:L687 | DatePicker(+Calendar) | size m | MK:date-picker/date-picker.tsx:L15, L25-31 · MK:calendar/calendar.tsx:L7-10 | — |
| `procedure/room-log/date-calendar` | 「이전 날」 · 「다음 날」(오늘이면 다음 날 비활성) | P:L687 | Button + ChevronIcon | icon · gray · m · disabled | 공통 · MK:icons/ (chevron-icon.tsx) | — |
| `procedure/room-log/room-select` | 「모든 관리실」 · 관리실 이름 목록 | P:L688 | ComboBox(single) | size m · hasAllOption true | MK:combobox/combobox.tsx:L48, L58 | CSS:L62, L65 |
| `procedure/room-log/room-group` | 관리실 → 고객 줄 → 시술 줄 3단 묶음 | P:L689-691 | **메디킷에 없음**(묶음 리스트). Table 로 근사 가능 | — | MK:table/table.tsx:L13 | CSS:L99-104 |
| `procedure/room-log/room-group` | 고객 이름(누르면 그날 시술 차트) | P:L690 | Button | text · black · s | 공통 | CSS:L44 |
| `procedure/room-log/room-group` | 「체류 중」 · 「진행 중」 · 「시작한 시술 없음」 | P:L690, L708 | Badge(추정) | primary · sm / neutral · sm | 공통 | CSS:L79-80 |
| `mobile/call-accept` | 호출 알림 카드 · 「수락」 | P:L469 | Card + Button | solid · blue · l(추정) | 공통 | — |
| `mobile/toast/taken` · `canceled` | 「다른 원장이 먼저 받았습니다」 · 「취소된 호출입니다」 | P:L486-487 | Notify | error · sm | MK:notify/notify.tsx:L10-11 | — |
| `procedure/consultant-call` | 「상담실장 호출」(관리실별 화면만) | P:L738 | 1차 범위 밖 — 조사 안 함 | — | — | — |

**메디킷에 없음(10)**

| # | 요소 | 쓰는 화면 | 근거 | 대체 가능성 |
|---|---|---|---|---|
| 1 | 보드 그리드(관리실 칸 · 침대별 칸) | board · room-slot | P:L68 / src/ui 40종 목록 | 없음 |
| 2 | 점유 칸 자리표시 「점유 중 · {이름}」 | room-slot/occupied | P:L69 | 누르는 부분만 Button filled |
| 3 | 타이머 · 경과 시간(「마취중 mm:ss」 · 「진행 mm:ss」 · 「호출 중 n분」) | anesthesia-running · calling · in-progress | P:L352, L517, L520 | 텍스트 토큰 |
| 4 | 드롭다운 메뉴(「⋯」 더보기 · 관리실 이름 메뉴) | treatment-line/more-menu · customer-card/more-menu · room-move/menu | Menu 는 사이드 내비(MK:menu/menu.tsx:L60) | Popover + Button text |
| 5 | 시술 줄 2단 행 | treatment-line/* | P:L74 | Table 행 근사 |
| 6 | 비활성 줄(「시술 미진행」) | treatment-line/not-proceeding | P:L141 | 회색 텍스트 + Badge neutral |
| 7 | 정보형 토스트(Notify 는 success · error 뿐) | toast/alert | MK:notify/notify.tsx:L10 | 없음(색 결정 필요) |
| 8 | 검색 결과 다값 행 | search/results | MK:command/command.tsx:L126 | Command Item 안에 텍스트 배치 |
| 9 | 「잠깐 강조」 모션 | confirm-needed/card · customer-card | P:L256, L262 | Card selected 를 잠깐 켜기 |
| 10 | 관리실 → 고객 → 시술 3단 묶음 리스트 | room-log/room-group | P:L689-691 | Table 근사 |

---

## 5. 들여올 컴포넌트 목록(합계)

조합 = 위 표에 실제로 나온 variant × color × size × state. 「추정」 표시를 단 값은 §6 #1 결정에 따라 바뀔 수 있다. 화면 수는 §1 행 기준(53-55 모바일 포함, 56 고도화 제외).

| # | 컴포넌트 | 필요한 조합 | 조합 수 | 쓰는 화면 수 |
|---|---|---|---|---|
| 1 | Button | solid·blue·{ss, s, l} · solid·blue·{s, l}·disabled · outlined·blue·{ss, s} · outlined·gray·{ss, s, l} · filled·gray·s · filled·yellow·ss · text·blue·{s, ss} · text·blue·ss·disabled · text·black·{s, ss} · text·black·s·disabled · icon·gray·{ss, m} · icon·gray·m·disabled | 22 | 26 |
| 2 | Badge | neutral·sm · primary·sm · warning·sm · danger·sm · purple·sm | 5 | 11 |
| 3 | Popover | bottom 기본 1 | 1 | 9 |
| 4 | Icons | MoreIcon · SearchIcon · PlusIcon · DeleteIcon · ChevronIcon · CheckIcon · CloseIcon(BaseModal 안) | 7 | 8 |
| 5 | Command(List · Item · Empty) | Item 기본 · Item disabled · Empty | 3 | 7 |
| 6 | Checkbox | unchecked · checked · disabled · checked+disabled | 4 | 4 |
| 7 | ConfirmModal | caution · warning · check(각 좌우 버튼) | 3 | 4 |
| 8 | Card | padding sm 기본 · selected+indicator none | 2 | 3 |
| 9 | Table | 기본 | 1 | 3 |
| 10 | Notify | error·default · error·sm | 2 | 3 |
| 11 | BaseModal | 기본(제목 · 바깥 닫힘 조건) | 1 | 2 |
| 12 | Textarea | 기본(placeholder) | 1 | 2 |
| 13 | ComboBox | single·m·hasAllOption false · single·m·hasAllOption true | 2 | 2 |
| 14 | Banner | warning · neutral | 2 | 2 |
| 15 | RadioGroup | checked · unchecked | 2 | 1 |
| 16 | Label | 기본 | 1 | 1 |
| 17 | Tabs | 기본(선택 탭) | 1 | 1 |
| 18 | Input | m·SearchIcon·allowClear | 1 | 1 |
| 19 | Divider | horizontal | 1 | 1 |
| 20 | Accordion | md·open · md·closed | 2 | 1 |
| 21 | DatePicker(+Calendar) | m | 1 | 1 |
| 22 | Chip(대체안 — Badge 로 정하면 빠짐) | xs·읽기 전용 | 1 | 1 |

- 합계: 22종 · 조합 61(Button 22 + Badge 5 + Popover 1 + Command 3 + Checkbox 4 + ConfirmModal 3 + Card 2 + Table 1 + Notify 2 + Radio 2 + BaseModal 1 + Textarea 1 + ComboBox 2 + Banner 2 + Label 1 + Tabs 1 + Input 1 + Divider 1 + Accordion 2 + DatePicker 1 + Chip 1 + Icons 7).
- 「화면 수」는 §3·4 표에서 그 컴포넌트가 나온 screenId 를 센 값이다(같은 화면 여러 번은 1, 「대체안」 · 「확인 안 됨」 행은 빼고, `treatment-line/*` 공통 행은 1).
- HTMX 클래스판(`medikit.css`)에는 Popover · Command · Notify · Textarea · Accordion · DatePicker · Divider 클래스가 **없다**(CSS:L20 의 `textarea` 리셋만 있음). OpenPencil 로 들일 때는 src/ui 원본이 기준이 된다.

---

## 6. 정할 것

| # | 무엇 | 왜 열려 있나(근거) | 추천 |
|---|---|---|---|
| 1 | 버튼 · 배지의 variant · color · size 짝 | 기획안은 문구와 동작만 말하고 시각 위계를 말하지 않는다(예: P:L76, L540, L544). §3·4 의 「추정」 값 전부가 여기 걸림 | 주 행동(시작 · 전체 호출 · 귀가 대기 · 저장) solid blue, 보조 outlined, 이름 링크 text — 카드 안은 ss, 카드 아래 행동은 s |
| 2 | 변경 이력 화면 | 「시술 차트의 변경 이력」(P:L135) · 「변경 이력을 연다」(P:L144, L261)뿐이고 시술 차트 화면 구성(P:L586-599)에 칸이 없음 | 기획안 담당자에게 위치(시술 차트 안 패널인지 별도 창인지) 확인 전엔 맵에 「확인 안 됨」 자리만 둔다 |
| 3 | CC 모바일 3행(53-55)을 이 맵에 넣을지 | 화면 구성 표엔 있으나(P:L13) 본 화면은 CC-24(모바일 기획안) 몫 | 맵 가장자리에 「CC 모바일(참고)」 묶음으로만 두고 컴포넌트 범위에서는 뺀다 |
| 4 | 의국 화면 / 관리실별 화면 구분 | OV:L132 는 두 화면이라 하고, 시술현황 기획안은 7-1(P:L738)에서만 나눈다 | 1차 맵은 의국 화면 하나로 그리고, 관리실별 화면은 7-1 과 같이 고도화로 둔다 |
| 5 | 「귀가 대기 취소」 위치 | P:L87 은 카드 상태 옆 표시 항목으로, P:L656 은 「⋯」 더보기 안 항목으로 적음 | P:L656(화면 구성 표, 더 구체적)을 따라 「⋯」 더보기 안으로 |
| 6 | 오더 메모 항목 · 「[이벤트]」 표현(Badge vs Chip vs 글자) | P:L114-122 는 「화면 표시」 글자만, P:L128 은 「[이벤트]」 글자만 적음. Chip 은 닫기 버튼 있는 입력 칩(MK:chip/chip.tsx:L8-11) | Badge neutral sm 하나로 통일(Chip 조합 1개는 빠짐) |
| 7 | 「전체 시술에 내용 적용」 확인 창 문구 · 버튼 문구 | 적용 수 · 제외 수를 보인다(P:L617)만 있고 제목 · 버튼 문구 없음 | 문구는 지어 넣지 않고 비워 둔 채 기획안 담당자에게 문구 요청 |
| 8 | 화면 알림(toast/alert)의 색 | Notify 가 success · error 뿐(MK:notify/notify.tsx:L10), 알림 성격(경고/정보)은 기획안에 없음(P:L163, L281) | 메디킷에 info variant 를 요청하기 전까지 Banner primary 축소형으로 대체하지 말고 「메디킷에 없음」 자리표시로 둔다 |
| 9 | 원장 목록 세 갈래의 선택 방식 | 지정 호출은 「골라진 채 + 「호출」」(P:L418), 시작 · 담당 변경은 「고르면 바로 반영」(P:L472, L543) | 지정 호출은 RadioGroup + 버튼, 나머지 둘은 Command Item 클릭 — 기획안 문장대로 둘로 나눈다 |
| 10 | 「의사 차트」 담당자 고르기 목록의 원천 | 「담당자를 고른다」(P:L605)만 있고 목록 범위(근무 원장? 전 원장?)가 없음 | 원장 목록(그날 근무)과 같은 원천으로 — 기획안 담당자 확인 |
| 11 | 타이머 · 경과 시간 표시 | 메디킷에 없음 #3 | 컴포넌트를 새로 만들지 않고 텍스트 토큰(`typo-caption`)으로 그린다 |
| 12 | 보드 그리드 · 줄 행 · 묶음 리스트 | 메디킷에 없음 #1 · #5 · #10 | OpenPencil 맵에서는 메디킷 바깥 「레이아웃 프레임」으로 표시하고 손 그림 컴포넌트로 만들지 않는다 |
