# cc-procedure-map — 시술현황 화면 정의서 맵 OpenPencil 결과 보고

## 상태: done — 「시술현황 맵」 페이지 · 화면 56/56 · 엣지 79(고아 0) · 메모 173 · 멱등 확인 · 린트(3규칙 제외) 오류 · 경고 0

- 대상: `reference/2026-11-12-open-pencil/medikit/medikit.fig` 새 페이지 「시술현황 맵」(headless `eval -w` 만 · 앱 안 엶 · 앱 모드 eval 0회)
- 백업: `medikit/medikit.before-map.fig`(맵 그리기 전 디스크 상태 · run-map.sh 가 없을 때만 만든다)
- 다른 페이지 · 변수: 「components」 1208 · 「medikit」 257 · 「Page 1」 0 노드 — 실행 전과 같음(변수 64 그대로 · 세트 스크립트 수정 0)

## 만든 것

| 파일 | 무엇 |
|---|---|
| `cc-procedure-map/screens.json` · `edges.json` · `notes.json` | 데이터 원본(앞 판 재사용 · 아래 「데이터 고친 것」) |
| `cc-procedure-map/gen-layout.py` → `layout.json` | 섹션 영역 · 화면 슬롯(w×h) · 메모 슬롯 좌표(메모 높이는 글 길이로 셈) |
| `cc-procedure-map/_maplib.js` | `unit()`(캡션 + `screen/<id>` + 마커 + 메모 카드) · `inst2` · `detach` · `custom` · 다른 페이지 새 노드 정리(stray) |
| `cc-procedure-map/sections/*.js` 14개 | 1-1a · 1-1b · 1-2 · 1-3 · 2-1 · 2-2 · 3-1 · 3-2 · 4-1 · 4-2 · 5-1 · 6-1 · 7-1 · M (서브에이전트 6명 작성 · 리드 실행 · 리드 수정 2곳) |
| `cc-procedure-map/edges.js` | 화살표(곡선 + 화살촉 + 「트리거 · 출처 줄」 라벨) · 마지막 |
| `cc-procedure-map/run-section.sh` · `run-map.sh` | 섹션 하나 = eval 하나(직렬 · 각 3~6초) / 백업 → 페이지 지움 → 섹션 순서 → edges → 노드 수 |
| (지움) `render.js` · `build.sh` | 와이어판 — 브리프대로 버림 |

캔버스 구조: `section/1`~`7` · `section/M`(「CC 모바일(참고)」, 오른쪽 가장자리) → 각 섹션 안에 화면마다 `caption/<id>` · `screen/<id>`(디자인 + `marker/<id>/<no>`) · `notes/<id>`(`note/<noteId>` 카드) · 페이지 맨 위 `edge/<from>→<to>`(같은 쌍 둘째부터 `#2`).

- 마커 = 보라 원(맵 주석 색, 세트 테두리와 같음 · 제품 색 primary/red 와 겹치지 않게) · 메모 카드 머리에 같은 번호
- 메모 카드 = 종류(정책 / 기획 메모 / 기획 담당자 확인 필요) + 기획안 원문 + `cc-기획안-시술현황 · P:L…`. open-question = 빨간 테두리 2
- 엣지 종류: nav 이동(파랑 실선 67) · contains 포함(회색 점선 9) · event 바깥 사건(보라 점선 2) · ref 참조(회색 점선 1)

## 검증

| 항목 | 결과 |
|---|---|
| 화면 | 56 / 56 맵에 있음(아래 대조표) · 슬롯 넘침 0 |
| 마커 | 151 = screens.json elements 151 · 빠진 마커 0 |
| 엣지 | 79(앞 판 66 + 추가 13) · 고아 0(끝 화면 없음 0) · 연결 없는 화면 0 |
| 메모 | 173 = 정책 162 · 기획 메모 7 · open-question 4 — 전부 `source` 줄 있음 · 기획안 원문 대조(공백 · 표 기호 · `<br>` 무시) 불일치 0 |
| 인스턴스 | 맵 INSTANCE 노드 437(중첩 포함) · `inst()` 호출 266 · 합성 인스턴스 detach 45(안쪽 인스턴스는 남음) |
| custom 요소 | 64 이름(아래 목록) |
| run-map 두 번 | 1회 5053 노드 · 2회 5053 노드(마지막 고친 뒤 다시 두 번 · 같음) — `{nodes 5053, instances 437, screens 56, markers 151, notes 173, edges 79}` · 문서 4 pages 6518 |
| 미바인딩 색 | 0(모든 섹션 `unbound: 0`) · 다른 페이지에 남은 노드(stray) 0 |
| 린트 | 문서 전체 오류 597 · 경고 364 · 정보 2564 — **color-contrast · min-text-size · touch-target-size 를 빼면 오류 0 · 경고 0**. 맵 페이지: color-contrast 542 · min-text-size 295 · touch-target-size 36(전부 세트 인스턴스의 시안 값) · 정보만 나머지(consistent-spacing 922 · pixel-perfect 407 · no-deeply-nested 348 · consistent-radius 277 · prefer-auto-layout 142 · effect-style-required 70 · no-hidden-layers 33 · no-empty-frames 8) |
| headless PNG | 섹션 · 화면별로 겹침 · 화살표 확인(글자 굵기 판정엔 안 씀). 유닛끼리 겹침 0. 다른 섹션으로 가는 긴 화살표는 섹션을 가로지른다(아래 「확인할 것」) |

## 데이터 고친 것(시안 · 기획안 대조)

- notes 3건 원문 복원: `procedure.customer-card#3`(L71) · `#7`(L74) — 원문 `<br>` 자리 · `procedure.treatment-line.in-progress#2`(L553) — 「…」로 잘려 있던 끝을 원문대로
- edges 13 추가(연결 없던 화면 9 → 0): board→room-slot · board→confirm-needed · confirm-needed→card · customer-card→order-memo · customer-card→new-lines · chart→chart/order-memo · chart→past-visits · chart→doctor-chart · chart→nursing-chart (포함 · L68 L67 L255 L72 L135 L589 L599 L592 L593) / board→toast/alert(사건 · L163 L281) · treatment-line/waiting→not-proceeding(사건 · L534 상담실장이 시술 미진행으로) / room-slot→consultant-call(참조 · L738 고도화) / treatment-line/calling→calling 「재호출」(이동 · L419 L517 · 자기 고리)
- 모든 엣지에 `kind` 필드. 화면 56 · 마커 요소 번호는 앞 판 그대로(기획안 절 커버리지 빠진 절 0 — research §1)

## 화면 대조표

| # | 절 | screenId | 이름 | 종류 | 마커 | 메모 | 연결 | 맵 |
|---|---|---|---|---|---|---|---|---|
| 1 | 1-1 | `procedure/board` | 시술 현황 화면 | 화면 | 5 | 5 | 6 | 있음 |
| 2 | 1-1 | `procedure/board/out-of-hours` | 「조회 시간 밖」 | 상태 | 1 | 1 | 1 | 있음 |
| 3 | 1-1 | `procedure/room-slot` | 관리실 칸 | 패널 | 2 | 2 | 2 | 있음 |
| 4 | 1-1 | `procedure/room-slot/occupied` | 「점유 중 · {고객 이름}」 칸 | 상태 | 1 | 3 | 2 | 있음 |
| 5 | 1-1 | `procedure/customer-card` | 고객 카드 | 패널 | 12 | 12 | 10 | 있음 |
| 6 | 1-1 | `procedure/customer-card/status-waiting` | 카드 상태 「시술 대기 HH:MM」 | 상태 | 1 | 3 | 2 | 있음 |
| 7 | 1-1 | `procedure/customer-card/status-in-progress` | 카드 상태 「시술 진행」 | 상태 | 1 | 2 | 3 | 있음 |
| 8 | 1-1 | `procedure/customer-card/status-discharge-wait` | 카드 상태 「귀가 대기 HH:MM」 | 상태 | 2 | 4 | 5 | 있음 |
| 9 | 1-1 | `procedure/customer-card/order-memo` | 고객 카드 오더 메모 | 패널 | 7 | 2 | 1 | 있음 |
| 10 | 1-1 | `procedure/treatment-line/waiting` | 시술 줄 대기 | 상태 | 4 | 5 | 4 | 있음 |
| 11 | 1-1 | `procedure/treatment-line/not-proceeding` | 시술 줄 시술 미진행(확인 전) | 상태 | 1 | 2 | 1 | 있음 |
| 12 | 1-1 | `procedure/treatment-line/done` | 시술 줄 완료 | 상태 | 3 | 4 | 2 | 있음 |
| 13 | 1-1 | `procedure/customer-card/line-changed` | 「변경」 · 카드 머리 「변경 n건」 | 상태 | 2 | 3 | 1 | 있음 |
| 14 | 1-1 | `procedure/customer-card/new-lines` | 구분선 뒤 새 시술 줄 | 상태 | 2 | 2 | 1 | 있음 |
| 15 | 1-1 | `procedure/customer-card/call-bar` | 시술 선택 · 원장 호출 | 패널 | 4 | 4 | 4 | 있음 |
| 16 | 1-1 | `procedure/chart/change-history` | 변경 이력 | 확인 안 됨 | 0 | 2 | 2 | 있음 |
| 17 | 1-2 | `procedure/search` | 고객 검색 | 패널 | 1 | 5 | 3 | 있음 |
| 18 | 1-2 | `procedure/search/results` | 검색 결과 | 팝업 | 2 | 4 | 2 | 있음 |
| 19 | 1-2 | `procedure/search/empty` | 「검색 결과 없음」 | 상태 | 1 | 1 | 1 | 있음 |
| 20 | 1-3 | `procedure/customer-card/confirm-flag` | 고객 카드의 「확인할 일」 글자 | 상태 | 3 | 4 | 1 | 있음 |
| 21 | 1-3 | `procedure/confirm-needed` | 「확인 필요」 | 패널 | 2 | 3 | 2 | 있음 |
| 22 | 1-3 | `procedure/confirm-needed/card` | 확인 필요 카드 | 패널 | 6 | 7 | 7 | 있음 |
| 23 | 1-3 | `procedure/toast/alert` | 시술 현황 화면 알림 | 토스트 | 1 | 3 | 1 | 있음 |
| 24 | 2-1 | `procedure/room-move/menu` | 관리실 이동 메뉴 | 팝업 | 3 | 4 | 4 | 있음 |
| 25 | 2-1 | `procedure/room-move/list` | 관리실 이동 목록 | 팝업 | 2 | 3 | 6 | 있음 |
| 26 | 2-1 | `procedure/room-move/list-empty` | 「빈 관리실 없음」 | 상태 | 1 | 1 | 1 | 있음 |
| 27 | 2-1 | `procedure/toast/room-full` | 「그 관리실에 자리가 없습니다」 | 토스트 | 1 | 1 | 1 | 있음 |
| 28 | 2-2 | `procedure/customer-card/anesthesia-idle` | 마취 「마취 시작」 | 상태 | 1 | 1 | 2 | 있음 |
| 29 | 2-2 | `procedure/customer-card/anesthesia-running` | 마취 「마취중 mm:ss」 · 「마취 종료」 | 상태 | 2 | 3 | 2 | 있음 |
| 30 | 3-1 | `procedure/treatment-line/calling` | 시술 줄 호출 중 | 상태 | 5 | 5 | 8 | 있음 |
| 31 | 3-1 | `procedure/doctor-list/designate-call` | 원장 목록 — 지정 호출 | 팝업 | 2 | 3 | 2 | 있음 |
| 32 | 3-2 | `procedure/treatment-line/accepted` | 시술 줄 수락 | 상태 | 2 | 3 | 4 | 있음 |
| 33 | 3-2 | `procedure/doctor-list/reassign` | 원장 목록 — 담당 원장 바꾸기 | 팝업 | 1 | 3 | 2 | 있음 |
| 34 | 4-1 | `procedure/treatment-line/in-progress` | 시술 줄 진행 중 | 상태 | 4 | 5 | 8 | 있음 |
| 35 | 4-1 | `procedure/doctor-list/start-pick` | 원장 목록 — 전체 호출 중 「시작」 | 팝업 | 1 | 2 | 2 | 있음 |
| 36 | 4-1 | `procedure/treatment-line/more-menu` | 줄 「⋯」 더보기 | 팝업 | 2 | 3 | 4 | 있음 |
| 37 | 4-1 | `procedure/confirm/cancel-start` | 확인 창 「{시술} 시작을 취소할까요?」 | 모달 | 3 | 2 | 4 | 있음 |
| 38 | 4-1 | `procedure/confirm/cancel-complete` | 확인 창 「{시술} 완료를 취소할까요?」 | 모달 | 3 | 2 | 2 | 있음 |
| 39 | 4-2 | `procedure/chart` | 시술 차트 | 모달 | 10 | 12 | 10 | 있음 |
| 40 | 4-2 | `procedure/chart/order-memo` | 시술 차트 오더 메모 | 패널 | 3 | 2 | 1 | 있음 |
| 41 | 4-2 | `procedure/chart/doctor-chart` | 「의사 차트」 | 패널 | 4 | 4 | 2 | 있음 |
| 42 | 4-2 | `procedure/chart/nursing-chart` | 「간호관리차트」 | 패널 | 6 | 3 | 4 | 있음 |
| 43 | 4-2 | `procedure/chart/author-picker` | 「작성자 추가」 직원 목록 | 팝업 | 1 | 1 | 2 | 있음 |
| 44 | 4-2 | `procedure/chart/apply-all-confirm` | 「전체 시술에 내용 적용」 확인 창 | 모달 | 1 | 2 | 2 | 있음 |
| 45 | 4-2 | `procedure/chart/discard-confirm` | 확인 창 「저장하지 않고 닫을까요?」 | 모달 | 3 | 1 | 2 | 있음 |
| 46 | 4-2 | `procedure/chart/conflict-notice` | 「다른 직원이 먼저 저장한 줄은 저장하지 않았습니다」 | 상태 | 1 | 1 | 1 | 있음 |
| 47 | 4-2 | `procedure/chart/past-visits` | 지난 방문 기록 | 패널 | 2 | 2 | 1 | 있음 |
| 48 | 5-1 | `procedure/customer-card/more-menu` | 카드 「⋯」 더보기 | 팝업 | 1 | 2 | 2 | 있음 |
| 49 | 6-1 | `procedure/room-log` | 관리실 기록 창 | 모달 | 6 | 4 | 3 | 있음 |
| 50 | 6-1 | `procedure/room-log/date-calendar` | 날짜 · 「이전 날」 · 「다음 날」 · 달력 | 팝업 | 1 | 1 | 1 | 있음 |
| 51 | 6-1 | `procedure/room-log/room-select` | 관리실 고르기 | 팝업 | 2 | 1 | 2 | 있음 |
| 52 | 6-1 | `procedure/room-log/room-group` | 관리실 묶음 | 패널 | 8 | 6 | 2 | 있음 |
| 53 | 7-1 | `procedure/consultant-call` | 관리실별 상담실장 호출(고도화 · 1차 범위 밖) | 범위 밖 | 1 | 2 | 1 | 있음 |
| 54 | M | `mobile/call-accept` | CC 모바일 의사 호출 알림 · 「수락」 | 화면(탭 밖) | 2 | 3 | 4 | 있음 |
| 55 | M | `mobile/toast/taken` | 「다른 원장이 먼저 받았습니다」 | 토스트(탭 밖) | 1 | 1 | 1 | 있음 |
| 56 | M | `mobile/toast/canceled` | 「취소된 호출입니다」 | 토스트(탭 밖) | 1 | 1 | 1 | 있음 |

## custom 요소(세트에 없거나 detach 해 고친 것 · 이름 `custom/<이름>`)

- 화면 틀: rail · header · page-controls · queue · board · banner-out-of-hours · mobile-frame · room-fragment · card-fragment · placeholder(변경 이력)
- 방 카드 detach: room-card(판 8장) · customer-card · room-card-call-bar · room-card-line-changed · room-card-new-lines · room-card-confirm-flag · room-card-anesthesia-idle · room-card-anesthesia-running · call-area-going
- 시술 줄 detach: proc-row-waiting · proc-row-not-proceeding · proc-row-done · proc-row-changed · proc-row-new · proc-row-calling-all · proc-row-calling-designate
- 배지 · 버튼: badge-interpreter(보라) · badge-warning(노랑 「변경」) · button-change-count(노랑 「변경 n건」) · button-outlined-blue(「지정 호출 · n개」) · text-button(고객 차트 · 작성자 추가 · 칸 지우기 · 오더 메모 접기)
- 인박스 카드 detach: inbox-card-anes-late · inbox-card-call-late · confirm-card-recall · confirm-card-renotify · confirm-card-going · confirm-card-change · mobile-call-card
- 팝업 detach: room-move-menu · room-move-list · room-move-list-empty · doctor-designate-call · doctor-reassign · doctor-start-pick · author-picker · room-select-list · room-select-trigger · select(담당자 콤보)
- 차트 · 기록: chart-modal · customer-info · order-memo · proc-table · anesthesia-table · room-log-table · doctor-chart · nursing-chart · past-visits · past-visits-cc · past-visits-kos · conflict-banner · search-results · search-results-empty · room-log-modal · calendar

세트에 있었으면 custom 이 줄었을 것(코디 판단용): Button outlined-blue · outlined-gray l/s · 텍스트 버튼 / Badge 노랑(warning) · 보라 / Notify 오류형 · 정보형 / 콤보 박스(select) · 배너 · 표 · 달력 / Icon: 레일 아이콘 6 · 병원 꺾쇠 · pc-chevron 좌우(시안 자산 · 세트에 없음 → 글자만)

## 시안 ↔ 기획안 ↔ 결정 — 다른 곳과 따른 쪽

원칙: 화면 · 요소 목록 · 문구 = 기획안 / 모양 · 배치 · 샘플 값 = 시안 / 둘이 다르고 결정 문서가 정한 것 = 결정. 화면별 세부는 각 `sections/*.js` 맨 위 `// DIFF:` 87줄.

| 무엇 | 시안 | 기획안 | 따른 쪽 |
|---|---|---|---|
| 의사 호출 버튼 | 「n개 호출」 한 버튼 + 고르기 팝오버(결정 U2 「모든 의사」 \| 원장) | 「전체 호출 · n개」 · 「지정 호출 · n개」 + 「지정 원장 · {원장}」 | **기획안**(customer-card · call-bar). 지정 호출 원장 목록도 기획안대로 원장만(「모든 의사」 줄 없음) — **U2 와 다름, 코디 확인** |
| 대기 줄 | 체크박스 + 「준비중」 · 버튼 없음 | 「대기」 글자 없이 체크박스 · 「시작」 | 기획안 + 결정 U1 |
| 호출 중 줄 버튼 | 「수락」 | 「시작」 · 「재호출」 | 기획안(문구) · 시안(줄 모양) |
| 수락 · 진행 중 줄 글 | 「김도윤 원장 수락」 · 「진행중」 + 시계 「8분」 | 「{원장} 수락 완료 HH:MM」 · 「{원장} · 진행 mm:ss」 | 기획안 |
| 완료 표시 | st-done-gray 아이콘 | 체크된 체크박스 | 시안(모양) · 「{원장} · n분」 · 「⋯」는 기획안 |
| 마취 | 방 머리 배지 하나(시작 → +mm:ss → 완료 n분) | 「마취 시작」 · 「마취중 mm:ss」 · 「마취 종료」 | 문구 = 기획안 · 모양 = 시안 배지(「마취 종료」 버튼 추가 · 「마취 완료 n분」 안 그림) |
| 카드 상태 · 통역 · 담당 상담실장 · 오더 메모 칩 · 「변경」/「변경 n건」 · 「시술 미진행」 · 새 줄 구분선 | 없음(메모는 글 덩어리) | 있음 | 기획안 요소를 시안 토큰으로 더함(detach) |
| 고객 줄 「입실 HH:MM」 | 있음 | 국적 | **결정**(입실 빼고 국적) — 시안 데이터에 국적 값이 없어 자리표시 「{국적}」(판 카드는 비움). 6-1 서브에이전트가 [TW]→「대만」으로 바꾼 것은 결정(변환 금지)에 어긋나 리드가 「{국적}」으로 고침 |
| 확인 필요 | 인박스 사이드바(현황 · 호출 · 시술 완료 탭 / 확인 필요 · 시작 가능 · 시술 대기) · 기준 = 결정 U12(마취 20분 · 호출 5분) | 「확인 필요」 영역 · 상황 6종(마취 40분 …) · 카드 버튼 4종 | 판 · confirm-needed = 시안 사이드바 + U12 / confirm-needed/card = 기획안 버튼 4종. 메모는 기획안 원문(마취 40분) — **U12 와 기획안 기준이 다름, 코디 확인** |
| 귀가 대기 뒤 카드 | 판에서 빠지고 「시술 완료」 탭(결정 U8) | 같은 관리실에 그대로(5-1 흐름 2) · 「⋯」 「귀가 대기 취소」 | 기획안(화면 목록이 기획안) — **U8 과 다름, 코디 확인** |
| 빈 관리실 | 결정 U6 「빈 방은 보이지 않는다」 | 정책 3 「사용을 켠 관리실마다 칸」 | 판 = U6(빈 방 안 그림) |
| 관리실 이동 | 방 이름 → 방 고르기 콤보 → 「방 옮기기」 · 「연결 풀기 · 돌아오기」 | 「점유 이동」 · 「다른 관리실로 이동」 · 「원래 관리실로 복귀」 · 고르면 바로 옮김 | 기획안(문구 · 흐름) · 시안(MoreMenu 모양). 점유 칸은 시안 held 카드 + 기획안 「점유 중 · {이름}」(시안 버튼 둘 남김) |
| 시술 차트 | 410 모달 · 「간호 관리 차트 / 의사 차트」 탭 · 「Ctrl + Enter」 | 줄마다 두 차트 · 오더 메모 · 표 · 지난 방문 · 「고객 차트 · 닫기 · 저장」 | 기획안(탭 없앰 · 560 폭) · 모양은 시안 모달 |
| 확인 창 문구 | 「쓴 내용은 사라져요.」 · 「취소」/「닫기」 | 「계속 쓰기」 · 「버리고 닫기」 · 「닫기」 · 「시작 취소」/「완료 취소」 | 기획안 |
| 토스트 | Notify(성공 체크 · primary) | 오류 · 정보 알림 | 세트 그대로(뜻 다름 — 오류형 세트 없음). 모바일 토스트는 체크 아이콘 숨김 |
| 색 | `--secondary #000a14` · `--surface-board #e3e3e5` | — | 변수 없음 → `black` · `gray/300` |

## 비워 둔 것 · open-question · 확인할 것

- open-question 4장(빨간 테두리): 변경 이력 위치(`change-history#1` · `#2` — 화면은 빈 점선 자리 「변경 이력」만 · 마커 없음) · 「전체 시술에 내용 적용」 확인 창 문구(`apply-all-confirm#2` — 제목 · 버튼 글자 비움 · 본문 「{적용 수} · {제외 수}」 자리) · 「의사 차트」 담당자 목록 원천(`doctor-chart#2` — 콤보 값 비움)
- 문구가 기획안에 없어 비운 제목: 원장 목록(start-pick · reassign) · 관리실 기록 창 · 모바일 머리
- 샘플이 없어 자리표시: `{국적}` · `{상담실장}` · `{차트 번호}` · `{주의 · 불만}` · `{직원}` · 지난 방문 표 칸 · `{검색어}` · 마취 시작 `HH:MM`
- 리드 판단으로 넣은 샘플: 관리실 칸 「A-룸2 (1/2)」 · 「(2/2)」(기획안 예시 형식을 이어 씀) · 확인할 일 「대기 6분째」 · 「수락 5분째」(기준 분)
- 다른 섹션으로 가는 화살표(예: 고객 카드 → 시술 차트 · 확인 필요 카드 → 모바일)는 긴 곡선이 섹션을 가로지른다 — 섹션 배치를 바꿀지는 코디 · 사용자 판단
- 앱: 지금 앱에 열린 탭이 있으면 저장 없이 닫고 디스크 파일을 다시 열어야 맵이 보인다(앱 옛 상태가 파일을 덮지 않게)
- 다시 그리기: `cc-procedure-map/run-map.sh`(약 60초 · eval 16번 직렬). 레이아웃만 바꿀 땐 `gen-layout.py` → `run-map.sh`
