# day-app mobile — 프로토타입 시술현황 탭 조사 결과 보고

## 상태: done

- 대상: `~/git/toy_pr2/cc-prototype/procedure/app` · 브랜치 `main` · HEAD `dbf0b53`(작업트리 깨끗)
- 방식: **정적 조사만.** flutter 실행 · 서버 실행 · 시뮬레이터/기기 조작 · 외부 API 호출은 하지 않았다. 아래 동작은 전부 코드에서 읽은 것이고 **실제 실행으로 확인하지 않았다.**
- 경로 표기: `lib/…` = `procedure/app/lib/…`, `ios/…` = `procedure/app/ios/…`, `back/…` = `procedure/back/app/…`
- 구분 표시: **[화면]** = 화면에 노출됨 · **[모델/API만]** = 모델 필드나 API 메서드는 있는데 시술현황 화면에서 안 씀 · **[DAY 결정과 다름]** = 원천 `reference/2026-11-03-cc-day/screen/procedure-board-decisions.md`(이하 「결정」) 와 동작이 다름. 다름 표시는 사실 대조일 뿐, 채택 · 제외는 사용자가 정한다.

---

## ① 화면 진입 · 폰/태블릿 구성

- 앱은 탭 4개(예약 현황 · 내원 현황 · **시술 현황** · 설정)이고, 첫 탭은 예약 현황이다 — `lib/app_state.dart:19-20`, `lib/app_state.dart:73`, `lib/screens/shell.dart:14-19`. [화면]
- 시술 현황 탭 루트는 `BoardScreen` — `lib/screens/shell.dart:67-72`.
- 폰/태블릿 기준은 짧은 변 600 — `lib/screens/board_screen.dart:17`, `lib/widgets/header.dart:103`.
  - 폰: 아래 탭바 4칸 — `lib/screens/shell.dart:115-123`, `:129-160`
  - 태블릿: 왼쪽 레일 92px, 위에 「Céramique」 글자 — `lib/screens/shell.dart:106-113`, `:162-214`
  - 탭마다 Navigator 스택을 따로 두고, 같은 탭을 다시 누르면 맨 위로 돌아간다 — `lib/screens/shell.dart:35`, `:74-80`, `:89-100`
- 태블릿은 글자를 짧은 변/700 배율(1.15~1.3)로 키운다 — `lib/theme/tokens.dart:95-101`, 적용 `lib/main.dart:33-40`.
- 탭 공통 틀 = 헤더 한 줄([Céramique][탭 이름][종]) + 연결 끊김 줄 + 본문 — `lib/screens/shell.dart:216-237`, `lib/widgets/header.dart:11-38`.
- 다른 진입 경로: 원장 호출 알림을 누르면 시술 현황 탭으로 바꾸고 `openVisit` 에 값을 넣는다 → `BoardScreen` 이 그 방 룸 상세를 연다 — `lib/app_state.dart:189-194`, `lib/screens/board_screen.dart:45-58`. 카드가 없으면 토스트 「호출이 끝났거나 방이 비었어요」 — `:53-55`. 알림 목록에서 눌러도 같은 길이다 — `lib/app_state.dart:211-215`.

## ② 목록 카드 — 정보 · 필터 · 정렬 · 타이머

### 본문 첫 줄
- 「확인 N」(폰은 빨간 알약, 태블릿은 「확인 필요 N」). 0이면 줄이 없다. 값은 `counts.need` — `lib/widgets/header.dart:147-169`, `lib/screens/board_screen.dart:71`. [화면]
- 이 줄에서 시계는 뺐다(`header.dart:147` 주석). 시계는 룸 상세 머리에만 있다(③).

### 필터 칩 [화면]
- 칩: 전체 · (의사/관리자만) 수락 대기 · 확인 · 대기 · 마취 · 호출 · 진행 · 귀가. 줄이 넘치면 가로로 스크롤된다 — `lib/screens/board_screen.dart:81-105`, 이름 `lib/view/view.dart:15-27`.
- 숫자는 스냅샷 `counts` 를 쓰고, 귀가와 수락 대기만 앱이 센다 — `lib/view/view.dart:46-56`.
- 거르는 규칙 — `lib/view/view.dart:59-68`. 필터 상태는 화면 안에만 있고 저장하지 않는다(`board_screen.dart:26`).
- **[DAY 결정과 다름]** 「결정」 「화면을 보고」 표에 따르면 웹 1차에서 [필터](E09) · 보기 바꾸기(E10)를 뺐다. 다만 이건 페이지 머리의 필터 버튼 얘기이고, 프로토 앱의 칩 줄과 같은 것인지는 사용자가 판단해야 한다.

### 정렬
- 카드는 스냅샷 `cards[]` 순서 그대로 보여 주고 앱이 다시 정렬하지 않는다(back 이 정렬하고, 귀가 대기는 맨 뒤) — `lib/view/view.dart:78-79`. [화면]
- 카드 안 시술 순서 = 진행 → 대기(sequence) → 완료(완료 시각) — `lib/view/view.dart:84-92`.
- 드래그로 순서 바꾸기는 **앱에 없다**(⑦). back 에는 `PUT /api/board/order` 가 있다 — `back/api/board.py:16`.

### 배치
- 폰: 한 줄에 1장(ListView) — `lib/screens/board_screen.dart:113-120`
- 태블릿: 최소 폭 270×배율 격자(Wrap) — `lib/screens/board_screen.dart:121-142`
- 빈 판: 「시술 중인 방이 없어요」 — `:107-108`
- 스냅샷이 오기 전에는 로딩 표시 — `:72`

### 카드 내용 (`RoomCard` `lib/screens/board_screen.dart:150-284`) [화면]
- 첫 줄: 방 이름 · 고객 이름 + 한글 발음(있을 때만) · 상태 배지 — `:190-208`
  - 배지 우선순위: 확인 필요(빨강) > 마취 중(보라) > 「시술 · 대기/진행」·「귀가 · 대기」 — `lib/view/view.dart:166-173`
  - 확인 필요 문구 — `lib/view/view.dart:176-183`
- **태블릿만** 둘째 줄: 국적 태그 · 첫내원/재내원 — `board_screen.dart:209-215`. 폰 카드에는 국적이 **없다**.
  - **[DAY 결정과 다름]** 「결정」은 카드 고객 줄에서 「입실」을 빼고 「국적」을 넣는다고 정했다. 프로토 카드에 입실은 없지만, 폰 카드에는 국적도 없다.
- 「지금」 상자: 제목 · 부제 · 오른쪽 타이머 — `board_screen.dart:216-231`
  - 표시 순서: 귀가 대기 > 진행(경과 mm:ss) > 모두 완료 > 호출 수락 대기(경과 분, 기준 넘으면 빨강) > 마취 중(경과 분, `long` 이면 빨강) > 시술 대기(담당의) — `lib/view/view.dart:185-222`
  - 색 — `board_screen.dart:169-175`
- 진행 막대(시술 수만큼 칸) · 「n / m」 · 「다음 <시술> · <원장>」 — `board_screen.dart:232-263`, `lib/view/view.dart:231-247`
- 의사/관리자 계정이고 나에게 온 호출이 있으면 호출마다 한 줄씩 「전체 호출 / 나를 지정 / <원장> 지정 · N건」 + [수락] — `board_screen.dart:264-278`
- 테두리: 확인 필요 = 빨강 2px, 진행 = primary — `:187`
- 귀가 대기 카드는 투명도 0.55로 흐리게 남는다 — `:177-178`
  - **[DAY 결정과 다름]** 「결정」 U8: 귀가 대기는 판에서 바로 빠지고 사이드바 「시술 완료」 탭에만 남는다.
- 카드를 탭하면 룸 상세로 간다 — `:181`

### 타이머
- `Ticker` 가 1초마다 다시 그린다 — `lib/widgets/ui.dart:252-272`
- 서버와 기기 시각 차이(`skewMs`)를 보정한다 — `lib/screens/board_screen.dart:111`, 계산 `lib/sse/board_stream.dart:141-142`
- 표시 시각은 KST 고정 — `lib/view/time.dart:9-17`
- 기준(분)은 스냅샷 `limits.callMin · anesMin` — `lib/model/board.dart:43-47`

## ③ 룸 상세 — 정보와 모든 조작 (`lib/screens/room_screen.dart`)

### 구성
- 머리: [‹ 시술 현황] 「룸 상세」 — `:67`
- 룸 정보 머리:
  - 폰 — `:116-157`
  - 태블릿 한 줄 72px — `:160-203`
  - 내용: 다른 룸 확인 수(빨강) · 방 · 고객 · 국적 · 첫/재내원 · **입실 HH:MM** · 수납 필요(노랑 태그) · KOS 반영 중/실패 · 배지 · **시계** — `:117-152`, `:174-200`, KOS 문구 `lib/view/view.dart:251-256` [화면]
- 본문:
  - 폰 한 열: 호출 상자 → 완료 상자 → 오더 메모 → 마취 → 시술 — `:205-215`
  - 태블릿 두 열: 왼쪽 = 오더 메모(늘어남) + 마취, 오른쪽 = 호출/완료(위 절반까지) + 시술 — `:220-250`
- 바닥: 통역 바 — `:75-81`(⑤)
- 카드가 판에서 사라지면 토스트 「<방> 고객이 판에서 빠졌어요」를 띄우고 목록으로 돌아간다 — `:48-51`, `:106-114`
- 버튼이 보이는지 · 켜지는지는 스냅샷 값만 보고 정한다(`:2` 주석, `lib/view/view.dart:2` 주석)

### 조작 전체 — 화면 → 위젯 → API 대조

| 조작 | 화면 위치 · 켜지는 조건 | 위젯 | API (`lib/api/api.dart`) | back 경로 |
|---|---|---|---|---|
| 마취 시작 | 마취 상자 · `anesthesia.canStart` | `room_screen.dart:457-464` | `anesStart` `:80` → `POST /api/visits/{id}/anesthesia/start` | `back/api/actions.py:18` |
| 마취 종료 | 마취 상자 · `canEnd` | `room_screen.dart:465-468` | `anesEnd` `:81` | `actions.py:24` |
| 의사 호출 | 시술 상자 바닥 · `canCall`(아니면 꺼진 「호출할 대기 시술 없음」) | `room_screen.dart:369-373` → `openCallSheet` | `createCall` `:82-85` → `POST /api/visits/{id}/calls {procedureIds, target}` | `actions.py:30` |
| 수락 | 호출 상자 · 카드 줄 · `isMine` | `room_screen.dart:284-304`, `board_screen.dart:275` → `acceptCall` | `accept` `:88-90` → `POST /api/calls/{id}/accept` (+`X-Accept-Source: app`) | `actions.py:37` |
| 다른 원장에게 | 지정 호출(`kind=one`) 상자 | `room_screen.dart:291-300`, `:313-321` | `reassignAll` `:91` → `POST /api/calls/{id}/reassign-all` | `actions.py:53` |
| 다른 의사 호출(재호출) | 내 호출이 아닌 호출 상자 | `room_screen.dart:306-312` → 호출 시트에 그 호출의 시술을 미리 체크 | `createCall` | `actions.py:30` |
| 시작 | 대기 시술 줄 · `canStart` | `room_screen.dart:421-424` → `runStart` `undo_sheet.dart:21-22` | `startProcedure` `:92` | `actions.py:58` |
| 종료 | 진행 시술 줄 · `canFinish` | `room_screen.dart:425-428` → `runFinish` `undo_sheet.dart:23-24` | `finishProcedure` `:93` | `actions.py:63` |
| 시작 되돌리기(=시작 취소) | 진행 줄 아이콘 · `canUndoStart` · 시작 성공 토스트 [되돌리기] | `room_screen.dart:420`, `undo_sheet.dart:21-22` | `undoStart` `:95` | `actions.py:69` |
| 종료 되돌리기(=완료 취소) | 완료 줄 아이콘 · `canUndoFinish` · 종료 토스트 [되돌리기] | `room_screen.dart:418`, `undo_sheet.dart:23-24` | `undoFinish` `:96` | `actions.py:75` |
| 귀가 대기 | 「시술 모두 완료」 상자 · `canHome` | `room_screen.dart:331-347` | `goHome` `:97` → `POST /api/visits/{id}/home` | `actions.py:82` |

### 표시만 하는 정보 [화면]
- 시술 줄 둘째 줄:
  - 완료 = 「원장 · HH:MM~HH:MM」
  - 진행 = 「원장 · HH:MM 시작」 + 경과 mm:ss
  - 수락됨 = 「<원장> 수락 · 시작 가능」
  - 호출됨 = 「… · 수락 전」 + 「호출함」 배지
  - 그 밖 = 담당의 / 「담당의 미정」
  - 근거: `lib/view/view.dart:110-126`, `room_screen.dart:378-433`
- 「방 배정」 작업(`isRoomTask`)은 그리지 않는다 — `lib/view/view.dart:81-82`.
- 호출 상자: 「전체/<원장> 지정 호출 · 수락 대기」 · 「HH:MM 호출 · 시술 N건 · 기준 N분(넘음)」 · 큰 숫자 「N분」 — `room_screen.dart:257-282`
- 마취 상자: 「마취 중」 + 경과 분 · 「HH:MM 시작 · 기준 N분(넘음)」 / 「완료 N분」(마지막 회차) / 「안 함」 — `room_screen.dart:436-456`
- 오더 메모: 없으면 「오더 메모 없음」. 상담 메모는 없다 — `room_screen.dart:475-487`. 「결정」 F8(오더 메모만)과 같다.
- 조작이 성공하면 토스트, 실패(403·409 등)면 back 의 message 를 그대로 토스트로 띄운다. 401 이면 로그아웃한다 — `lib/app_state.dart:412-427`. 응답은 `{ok}` 뿐이고 화면은 이어서 오는 SSE board 로 바뀐다 — `lib/api/api.dart:79`, `app_state.dart:412`.

## ④ 의사 호출 · 수락 · 재호출 · 되돌리기

### 호출 시트 (`lib/widgets/call_sheet.dart`) [화면]
- 폰 = 바텀 시트(높이 88%), 태블릿 = 가운데 다이얼로그(560×640) — `:12-36`
- 머리: 「의사 호출」 + 방(태블릿은 방 · 고객) — `:76-87`
- 「호출할 시술」: `pickable` 인 것만 켜진다 · [전체 선택] · 고를 게 없으면 「호출할 대기 시술이 없어요」 — `:66-107`, `:157-173`, `:259-261`
- 「누구에게」: 「모든 의사」(ALL · 「먼저 수락한 원장」) + 원장 줄(비어 있는 원장이 먼저 · 「<방> 시술 중」/「비어있음」). 하나만 고르고, 다시 누르면 풀린다 — `:109-121`, `:227-256`
- 기본 선택은 없다. 버튼은 「의사를 선택하세요」(꺼짐) → 「<대상> 호출 · N건」 — `:49`, `:71-73`, `:134-136`
- 보내기 — `:144-155`
- **[DAY 결정과 다름]**
  - 모양: 「결정」 「화면 참고 — 의사 호출 창」은 **누른 버튼 바로 아래 팝오버(덮개 없음)** · 왼쪽 고르기(검색 · 「추천」 묶음) / 오른쪽 「선택됨 · 호출할 시술 N개」를 정했다. 프로토는 덮개 있는 시트 한 열이고 검색 · 추천 묶음이 없다.
  - 재호출 기본 선택: OQ-04 는 「처음 호출 대상」을 기본으로 고른다. 프로토 재호출([다른 의사 호출])은 시술만 미리 체크하고 대상은 고르지 않는다 — `room_screen.dart:311`.

### 수락 (`lib/widgets/accept.dart`)
- 누가 누르나 — `lib/app_state.dart:44-48`, `lib/view/view.dart:139-152`, `lib/model/account.dart:33-35`
  - 의사 계정: 내게 온 호출(전체 또는 나를 지정)에 [수락 · N건]. 본문에 doctorId 를 싣지 않는다(자기 자신으로 수락) — `accept.dart:16`, `api.dart:86-90`
  - 관리자 묶음(admin · coordinator · counselor): 모든 호출에 수락 버튼이 보인다. 지정 호출은 지정 원장으로 수락하고, 전체 호출은 원장 고르기 시트에서 고른다(「누구로 수락할까요 · <방>」) — `accept.dart:12-29`, `:32-120`, `room_screen.dart:284-304`
  - **간호사(nurse)는 `Me.none` 이라 수락 버튼이 없다** — `app_state.dart:44-48`, `view.dart:144-145`
  - **[DAY 결정과 다름]** 「결정」 U4 와 권한 표: 수락은 의사 본인 또는 간호사가 대리로 한다(간호 · 피부관리 · 마취과 · 원장 · 관리자 = 수락 ✓, 코디 · 상담 = 보기만). 프로토는 간호사가 수락할 수 없고 코디 · 상담사가 수락한다.
- 알림에서 바로 수락: ⑤ 참고.

### 재호출
- 화면 두 가지:
  - [다른 의사 호출]: 새 호출을 만든다(`createCall`) — `room_screen.dart:306-312`
  - [다른 원장에게]: 지정 호출을 전체 호출로 바꾼다(`reassign-all`) — `room_screen.dart:294-300`, `:313-321`
- 「앞 호출을 닫는다 / 앞 수락을 무효로 한다」는 앱 코드에 없다. 앱은 스냅샷의 `calls[]` · `procedure.call` 을 그대로 그린다 — `lib/model/board.dart:100-120`, `:260-295`. 그 규칙은 back 소관이다(앱 규칙 「서버 값만」과 같음).
- 확인 필요의 [재호출] 버튼은 따로 없다. 「확인」은 필터와 빨간 표시로만 나온다(②).
- **[DAY 결정과 다름]** 「확인 필요」 이유는 `need.why` = `home | anes | call` 이고, 「시술 모두 완료 · 귀가 대기 전」 문구가 있다 — `lib/model/board.dart:179`, `lib/view/view.dart:182`. 「결정」 U12 는 마취 20분 초과와 호출 5분 무응답만 둔다. 이 값은 back 이 주므로 DAY back 이 home 을 안 주면 앱에서도 안 나온다.

### 되돌리기 (`lib/widgets/undo_sheet.dart`) [화면]
- 아이콘을 누르면 확인 창이 뜬다. 폰은 바텀 시트, 태블릿은 가운데 다이얼로그 — `:26-66`
  - 문구: 「시술 대기로 되돌리겠습니까?」/「시술 중으로 되돌리겠습니까?」 — `:13-15`
  - 버튼: [취소] [되돌리기]
- [시작] · [종료] 성공 토스트에 [되돌리기] 버튼이 붙는다 — `:20-24`, `lib/app_state.dart:413-417`
- 켜지는 조건은 스냅샷 `canUndoStart · canUndoFinish` 만 본다 — `lib/model/board.dart:137-138`
- 계약 §3 「시작 취소 버튼은 유지」 → 프로토의 시작 되돌리기가 그 버튼에 해당한다. KOS 에 쓸지는 앱과 관계없다(백엔드 소관).

## ⑤ 실시간 갱신 · 푸시 · 통역 등 연결 기능

### 실시간 (`lib/sse/board_stream.dart`)
- 연결: `GET /api/board/stream?token=<토큰>&deviceId=` 를 http 스트림으로 직접 읽는다(EventSource 패키지 없음) — `:1-6`, 주소 `lib/api/api.dart:195-197`, back `back/api/board.py:22`
- 첫 화면은 연결 직후 오는 board 이벤트로 그린다. `GET /api/board`(`back/api/board.py:11`)는 앱이 부르지 않는다 **[모델/API만 — back 에만]**
- `version` 이 지금 값 이하면 버리고, 새 연결의 첫 이벤트는 무조건 받는다 — `:16-21`, `:137-139`
- 다시 연결: 3s → 6s → … 최대 30s. 45초 동안 바이트가 없으면 끊긴 것으로 본다 — `:23-32`, `:47`, `:165-177`
- 401 이면 로그아웃(「로그인이 풀렸어요」) — `:113-119`, `lib/app_state.dart:85`
- 앱이 백그라운드로 가면 끊고, 앞으로 오면 다시 붙는다 — `lib/app_state.dart:429-443`
- 끊긴 동안은 「연결 끊김 · 다시 연결 중」 노란 줄을 띄우고 값은 마지막 스냅샷 그대로 둔다 — `lib/widgets/header.dart:171-189` [화면]
- board 말고 `notification`(종 배지) · `display`(띄우기) 이벤트도 같은 스트림으로 받는다 — `:157-163`, `lib/app_state.dart:92-104`. display 는 예약 쪽 기능이다.

### 푸시 (APNs 직접 · Firebase 없음)
- 로그인 직후 알림 권한을 요청한다 → 기기 토큰 `POST /api/devices {token, name, kind, installId}` → 응답 deviceId 로 SSE 를 다시 연다 — `lib/app_state.dart:266-269`, `:307-359`, `lib/api/api.dart:101-105`
- 로그아웃할 때 `DELETE /api/devices/{token}` 을 먼저 부른다 — `lib/app_state.dart:388-396`
- MethodChannel `procedure/push` 로 네이티브와 주고받는다 — `lib/push/push.dart:52-84`
- 원장 호출 payload `{visitId, callId}` 를 누르면 그 방 룸 상세가 열린다(①) — `lib/push/push.dart:14-41`, `ios/Runner/AppDelegate.swift:164-185`
- 앱이 앞에 있을 때도 배너와 소리를 낸다 — `AppDelegate.swift:157-161`
- 알림 액션 [수락](카테고리 `CALL` · 액션 `ACCEPT`) — `AppDelegate.swift:10-11`, `:27-29`, `:171-173`, `:187-214`, 키체인 `:282`
  - 앱을 열지 않고 네이티브가 키체인의 서버 주소 · 토큰으로 `POST /api/calls/{callId}/accept`(`X-Accept-Source: push` · doctorId 없음 = 의사 자기 자신)를 보낸다
  - 결과는 로컬 알림 「수락했어요 · <방>」/「수락 못 함 · <사유>」
- 알림 목록 · 읽음 · 알림 설정(종 · 설정 탭)은 예약 쪽과 같이 쓰는 기능이다 — `lib/api/api.dart:109-118`, `lib/screens/shell.dart:239-261`
- README 에 시뮬레이터 가짜 푸시 절차가 있다 — `README.md` 「원장 호출 푸시」

### 통역 (룸 상세 바닥) [화면]
- 통역 바 — `lib/widgets/interpret_bar.dart:88-173`
  - 「빠른 말하기 · <언어>」(태블릿은 「통역 · <언어>」)
  - 문장 칩 6개: 누르면 **기기 TTS**(flutter_tts)가 고객 언어로 읽는다. back 은 거치지 않는다 — `lib/interpret/quick_speech.dart:1-37`
  - [통역하기]
  - 「마지막 통역 HH:MM · N문장」 — `room_screen.dart:34`, `:94-97`
- 언어는 국적으로 자동으로 고르고(`autoLang`, 모르면 en) 드로어에서 바꿀 수 있다 — `lib/interpret/langs.dart:31-34`, `room_screen.dart:56-58`, `interpret_drawer.dart:262`
- 통역 드로어(높이 92%) — `lib/widgets/interpret_drawer.dart`
  - 마이크 권한(거부면 안내 문구 `:100`) → WebSocket `ws(s)://<서버>/api/interpret`, 헤더 `Authorization: Bearer` — 주소 `lib/config/server.dart:27-33`, 연결 `lib/interpret/interpret_client.dart:1-6`, `:36-42`, back `back/api/interpret.py:50`
  - PCM 16kHz로 올리고 번역 음성 24kHz를 재생한다. 반이중이라 재생 중에는 마이크를 보내지 않는다 — `interpret_client.dart:2-5`
  - 자막: 의료진/고객 양쪽, 원문 + 번역
  - 상태: 듣는 중 · 멈춤 · 연결 안 됨 · [다시 연결]
  - 닫거나 백그라운드로 가면 대화를 지우고 요약 한 줄만 남긴다 — `:85`, `:168-175`
- 통역에 필요한 패키지 · 권한: `record` · `audio_session` · `flutter_pcm_sound` · `flutter_tts`(`pubspec.yaml`), 마이크 문구 `ios/Runner/Info.plist:71-72`
- DAY SSOT(작업 요약 · AGENTS.md · 「결정」 · mobile-deployment)에는 통역에 대한 결정이 **없다**. mobile-deployment §5-3 은 권한을 「그 기능이 앱 범위에 들어올 때만」 넣자고 [제안]한다.

## ⑥ 로그인 · 컬러 · 브랜딩 — DAY 로 바꿀 자리

프로토에서 확인한 사실과 DAY 쪽 근거만 나란히 둔다. DAY 쪽 앱 설계값(번들 id · flavor 등)은 mobile-deployment 에서도 [제안]/[미결] 상태다.

| 항목 | 프로토(사실) | DAY 쪽 근거 |
|---|---|---|
| 로그인 요청 | `POST /api/auth/login {id, password}` · 아이디 + 비밀번호 — `lib/api/api.dart:67-71`. 자동 로그인 = `GET /api/auth/me` Bearer — `api.dart:73-77`, `app_state.dart:238-254` | AGENTS.md 예시: `POST /api/auth/login {email, password, client:"app"}` · 앱은 Bearer(DAY-SPEC-001). mobile-deployment §1 [확정] — **본문 키가 다르다(id ↔ email · client)** |
| 로그인 화면 | 로고 「Céramique」 · 제목 「예약 · 시술 현황」 · 아이디/비밀번호 · 401/429 문구 — `lib/screens/login_screen.dart:12-18`, `:193-248`, `:261-276` | 「결정」 문구 결정(11-08): 「MediSolve AI」 · 「DAY」(로그인 카드) · 「병원 선택」 · 「처음으로」는 그대로 둔다(웹 기준). 앱 로그인 화면 시안은 이번 SSOT 에 없다 |
| 서버 주소 입력칸 | debug 빌드만 「서버 주소」 + [연결 확인](`GET /api/health`). release 는 `API_BASE` 고정 — `lib/config/server.dart:1-65`, `login_screen.dart:149-175`, `:198`, `api.dart:65` | AGENTS.md: 주소는 `--dart-define` 으로. mobile-deployment §4 [제안]: 로컬 덮어쓰기는 dev flavor 에서만 |
| 토큰 보관 | iOS 키체인(flutter_secure_storage · first_unlock_this_device) · 아이디만 기억 — `lib/api/session_store.dart:1-52`, `app_state.dart:261` | mobile-deployment §5-3 [제안] 키체인 — 같은 방향 |
| 역할 | 역할 5개(admin · doctor · nurse · coordinator · counselor), 수락 묶음은 앱이 역할로 정한다 — `lib/model/account.dart:5-45` | 「결정」 권한 표: 권한 키 `board` 보기/수정 · `board.accept`(KOS 직무 태그 매핑). **앱 역할 모델과 권한 모델이 다르다** — 앱이 받을 권한 값의 모양은 SPEC 소관 |
| 색 | ceramique primary `#2498BD` + medikit 회색 · 빨강 · 노랑 · 보라 토큰 — `lib/theme/tokens.dart:4-40`, 테마 `:65-93` | DAY 웹은 medikit 토큰(AGENTS.md 「웹 화면」). DAY 앱 색 · 시안은 이번 SSOT 에 없다 |
| 글꼴 | Pretendard(OFL) 번들 — `pubspec.yaml` fonts | 근거 없음 |
| 앱 이름 · 헤더 글자 | `MaterialApp.title` 「Céramique」 `lib/main.dart:28` · 헤더 `lib/widgets/header.dart:29` · 레일 `lib/screens/shell.dart:178` · `CFBundleDisplayName` Céramique `ios/Runner/Info.plist:9-10` · `CFBundleName` procedure_app `:17-18` | mobile-deployment §3 [제안] `DAY Dev` / `DAY` |
| 아이콘 | ceramique 「C」 로고 — README 「앱 아이콘」 | 근거 없음(§3 [제안] dev 아이콘에 띠) |
| 딥링크 스킴 | `ccc://display?t=`(예약 띄우기) — `ios/Runner/Info.plist:87`, `lib/app_state.dart:139-163` | 시술현황과 관계없음 |
| 기타 문구 | 마이크 거부 안내 「설정 → 시술 현황 → 마이크」 `interpret_drawer.dart:100` · 로컬 네트워크 문구 `Info.plist:73-74` | 앱 이름이 바뀌면 같이 바뀌는 자리 |

## ⑦ 조사 범위에서 발견되지 않은 기능

`lib/` 전체를 grep 했다(이동 · move · chart · 차트 · reorder · Draggable · LongPress).

- **방 옮기기 · 방 연결: 없음.** 화면 · API 메서드 · 모델 어디에도 없다. `Room` 모델에는 `id · title · order` 만 있다 — `lib/model/board.dart:49-55`. 「결정」에서도 U5 는 다음 스펙이다.
- **차트(간호 · 의사) 작성: 없음.** 남은 흔적은 `Customer.chartNumber` 필드 하나인데 **[모델/API만]** 화면에서 쓰지 않는다 — `lib/model/board.dart:62`, `:69`. 「결정」 U11 도 다음 스펙이다.
- **카드 순서 드래그(D&D): 앱에 없음.** back 에는 `PUT /api/board/order` 가 있다 — `back/api/board.py:16`. 「결정」 U6 은 D&D 로 자리를 바꾼다고 정했다(웹 #231 구현).
- **판 안 「시술 완료」 사이드바(인박스): 없음.** 귀가 대기는 판에 흐리게 남는다(②).
- **수납 처리: 없음.** 「수납 필요」 태그 표시만 있다 — `room_screen.dart:149`, `:189`.
- **보기 바꾸기(의사별 · 구역): 없음.**
- **[모델/API만] 화면에 안 쓰는 스냅샷 필드**
  - `Board.sync`(lastOkAt · lastError · inWindow) — `lib/model/board.dart:12-18`, `:318`
  - `Procedure.kosStatus` · `kind`(`isEtc`) — `:124`, `:128`, `:157`
  - `KosState.failed[]` 상세 — `:190-202`. 화면은 status 문구만 쓴다.
  - `Room.order` — `:52`
  - `Need.since · limitMin` — `:180-181`
  - `ProcCall.acceptedAt` — `:106`
  - `OpenCall.customerName · customerNationality` — `:264-265`
  - `Doctor.busy · busyRoom` 은 호출 · 수락 시트에서만 쓴다.

## ⑧ 기능 범위 논의용 목록

다음 표는 채택 · 제외를 정하라는 게 아니라 **사용자가 고를 단위**를 묶은 것이다. 「DAY 근거」 칸은 SSOT 에 있는 것만 적었고, 없으면 「근거 없음」이다.

| # | 묶음 | 프로토에 있는 것 | DAY 근거 |
|---|---|---|---|
| 1 | 판 목록 | 카드(방 · 고객 · 발음 · 배지 · 지금 상자 · 진행 막대 · 내 호출 [수락]) · 폰 1열 / 태블릿 격자 | 「결정」 U6 · U7 · 국적 줄 · 오더 메모만 |
| 2 | 필터 칩 | 전체 · 수락 대기 · 확인 · 대기 · 마취 · 호출 · 진행 · 귀가 | 웹 1차는 머리 필터(E09)를 뺌 — 앱 칩도 같은 판단인지 미정 |
| 3 | 「확인 N」 줄 | `counts.need` | U12(마취 · 호출만) |
| 4 | 귀가 대기 카드 처리 | 판에 흐리게 남음 | U8 판에서 빠짐 · 시술 완료 탭 — 앱에 그 탭을 둘지는 근거 없음 |
| 5 | 카드 순서 D&D | 앱에 없음(back 에만) | U6 D&D |
| 6 | 룸 상세 정보 | 머리(입실 · 수납 필요 · KOS 반영 · 시계 · 다른 룸 확인 수) · 오더 메모 · 마취 · 시술 줄 | 「입실 빼고 국적」은 카드 · 인박스 결정 — 룸 상세의 입실은 근거 없음 |
| 7 | 마취 시작/종료 | 있음 | 권한 표 「수정」 · U10 |
| 8 | 의사 호출 창 | 바텀/가운데 시트 · 한 열 · 기본 선택 없음 | U2 · 「호출 창」 팝오버 두 칸 · 검색 · 추천 |
| 9 | 재호출 | [다른 의사 호출](새 호출) · [다른 원장에게](reassign-all) | U3 · D-25~27 · OQ-04 기본 = 처음 대상 — reassign-all 에 해당하는 결정은 근거 없음 |
| 10 | 수락 주체 | 의사 본인 · 관리자 묶음(코디 · 상담 포함) · 간호사 불가 | U4 · 권한 표(간호 · 원장 수락, 코디 · 상담 보기만) |
| 11 | 시작 · 종료 · 시작 되돌리기 · 종료 되돌리기 | 확인 창 + 토스트 [되돌리기] | 계약 §3 시작 취소 유지 · 권한 표 「수정」 |
| 12 | 귀가 대기 버튼 | `canHome` 상자 | 권한 표 「수정」 · U8 |
| 13 | 실시간 SSE | version · 다시 연결 · 끊김 줄 · 백그라운드 끊기 | 작업 요약 「서버 렌더 웹(+SSE)」 · JSON `/api/*` 는 앱 전용 — 앱 스트림 계약은 근거 없음 |
| 14 | 원장 호출 푸시 | 권한 요청 · 기기 등록/해제 · 눌러서 룸 상세 · 알림 [수락](네이티브 키체인) | mobile-deployment §1 [확정] 서버가 APNs 직접 · F20 「의사 계정 수락 = 본인(앱 · 기기 구분 정할 때)」 보류 |
| 15 | 알림 목록 · 종 배지 · 알림 설정 | 있음(예약 쪽과 공용) | 근거 없음 |
| 16 | 통역 · 빠른 말하기 | 통역 바 · 드로어 · WS · 마이크 · TTS | 근거 없음 · mobile-deployment §5-3 권한 최소화 [제안] |
| 17 | 로그인 · 브랜딩 | ⑥ 표 | DAY-SPEC-001 · 문구 결정 · mobile-deployment §3 [제안] |
| 18 | 탭 셸 | 4탭(예약 · 내원 · 시술 · 설정) · 태블릿 레일 | 첫 기능 = 시술현황(브리프 §2) — 나머지 탭은 근거 없음 |

## 검증

- 방법: 화면 → 위젯 → `Api` 메서드 → 프로토 back 라우터를 줄 단위로 대조했다(③ 표).
  - 읽은 파일: `screens/board_screen · room_screen · shell · login_screen`, `widgets/call_sheet · accept · undo_sheet · interpret_bar · interpret_drawer · header`, `view/view · state · time`, `api/api · session_store`, `sse/board_stream`, `theme/tokens`, `model/board · account`, `app_state`, `push/push`, `config/server`, `interpret/*` 일부, `ios/Runner/AppDelegate.swift · Info.plist` 일부, `back/app/api/*.py` 라우트 grep
- 조작 11개 모두 화면 진입점 · `Api` 메서드 · back 경로가 하나씩 이어지는 것을 확인했다.
- `analyze · test · build` 는 브리프 §8(정적 조사만)에 따라 **돌리지 않았다.** 실행 검증: **없음.**
- 무관한 실패: 해당 없음(아무것도 실행하지 않음).

## 계약 대조

- 새 계약을 만들지 않았다. 프로토 경로(`/api/visits/…` · `/api/calls/…` · `/api/board/stream` · `/api/interpret`)는 참고용으로만 적었다. DAY API 와 같다고 가정하지 않았다.
- DAY backend · 조사 대상 레포 · day-procedure-board-2 기록은 건드리지 않았다. 쓴 파일은 이 보고서 하나다.

## 이슈 · 코디가 확인할 것

1. **역할/권한 모델이 다르다**
   - 프로토: 앱이 역할로 수락 묶음을 정한다(간호사 불가, 코디 · 상담 가능).
   - DAY: 권한 표상 간호사가 수락하고 코디 · 상담은 보기만 한다.
   - DAY 앱이 받을 권한 값(`board` · `board.accept`)의 JSON 모양은 SPEC 이 정해야 한다.
2. **로그인 본문 키가 다르다.** 프로토는 `{id, password}`, DAY 는 `{email, password, client:"app"}`(AGENTS.md 예시) — 앱 로그인 화면 시안이 필요하다.
3. **앱용 판 스냅샷 · 스트림 계약이 SSOT 에 없다.** 작업 요약은 「JSON `/api/*` 는 앱 전용」까지만 말한다. 프로토 화면은 거의 전부 스냅샷의 `can*` · `pickable` · `need` · `counts` · `limits` 에 기대고 있다.
4. 「결정」과 다른 프로토 동작 6건 — 귀가 대기 흐리게 남음 · 호출 창 모양 · 재호출 기본 대상 · 확인 필요 `home` · 폰 카드 국적 없음 · D&D 없음. 이건 프로토를 그대로 옮기지 말아야 할 자리 후보다.
5. 통역 · 알림 목록 · 알림 [수락] 액션은 DAY SSOT 에 근거가 없다. 넣는다면 마이크 · 알림 권한과 심사 문구가 같이 따라온다.
