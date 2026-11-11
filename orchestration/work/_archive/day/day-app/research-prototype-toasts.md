# 프로토타입 상태 변경 토스트 정적 조사

- 대상(읽기 전용): 프로토 `/Users/kknaks/git/toy_pr2/cc-prototype/procedure/app` (아래 `P/` = `.../procedure/app/lib/`), 현재 앱 `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-app/app` (아래 `A/` = `app/lib/`, HEAD 0b776e90).
- 방법: **정적 확인만**(grep · 소스 읽기). 실행 · 빌드 · 서버 · 로그인 없음. 표의 동작은 모두 코드에서 읽은 것이며 실행으로 확인하지 않았다.
- 문구는 소스 원문 그대로 인용(`${…}` 는 코드 보간식).

## 1. 결론 요약

- 프로토는 **상태 변경(조작) 성공 시 토스트를 쓴다.** 공통 경로는 `AppState.run(action, okMessage, actionLabel, onAction)` (`P/app_state.dart:414-427`) → `Toaster.show` (`P/widgets/ui.dart:162-173`) → `ToastLayer` (`P/widgets/ui.dart:195-249`) 한 곳.
- 사용자 캡처 「A-룸1 · 써마지 FLX 300shot 종료」 + 「되돌리기」 = **`runFinish`** (`P/widgets/undo_sheet.dart:23-24`)
  `'${c.room.title} · ${p.title} 종료'` + `'되돌리기'` → `runUndo(…, UndoKind.finish)`. 호출 지점은 룸 상세 [종료] 버튼 `P/screens/room_screen.dart:427`.
  모양(어두운 반투명 둥근 상자 · 흰 글자 · 오른쪽 파란 계열 버튼 글자 · 화면 위쪽)은 `ToastLayer` 와 일치.
- **되돌리기 버튼이 붙는 토스트는 [시작] · [종료] 성공 두 개뿐.** 나머지 성공 토스트는 글자만.
- 현재 DAY 앱은 **성공 토스트가 없다**(오류 · 안내만). 되돌리기는 줄의 ⋮ 메뉴(「시작 취소」 · 「완료 취소」)로만 있고 토스트 [되돌리기] · 확인 시트는 없다.

## 2. 프로토 토스트 엔진 (`P/widgets/ui.dart`)

| 항목 | 내용 | 근거 |
|---|---|---|
| 상태 보관 | `Toaster extends ChangeNotifier` — `text` · `action` · `onAction` 한 칸 | ui.dart:156-160 |
| 표시 시간 | 버튼 없으면 **2600ms**, 버튼 있으면 **5000ms**(주석: 웹 `UNDO_TOAST_MS`) | ui.dart:158 · 169 |
| 중복 처리 | 한 번에 하나. 새 `show` 가 이전 것을 **덮어씀**, 타이머 취소 후 재시작, 세대 번호 `_n` 로 늦은 타이머 무시. 큐 없음 | ui.dart:162-173 |
| 버튼 표시 조건 | `onAction` 이 null 이면 `action` 도 null(글자만 있으면 버튼 안 보임) | ui.dart:164 |
| 버튼 탭 | `tapAction` = 먼저 `hide()` 후 콜백 실행 | ui.dart:182-186 |
| 장착 위치 | `MaterialApp.builder` 안 `ToastLayer` — Navigator 밖, 모든 화면 위 | main.dart:38 |
| 위치 | `Positioned(left:16, right:16, top: safeArea.top + 68)` — 화면 위, 머리 아래(주석 E2E A3) 가운데 정렬 | ui.dart:207-210 · 219 |
| 모양 · 색 | 배경 `Color(0xE6222222)`(90% 어두운 회색) · 모서리 10 · 그림자 `0x29000000` blur 12 offset(0,4) · padding 16×10 | ui.dart:222-227 |
| 글자 | 본문 `Typo.body500` 흰색(가운데) · 버튼 `Typo.body600` `Ms.primary300` · 간격 16 | ui.dart:230-236 |
| 애니메이션 | `AnimatedOpacity` 180ms | ui.dart:213-215 |
| 터치 | 버튼 없을 때는 `IgnorePointer`(아래 화면 터치 통과) | ui.dart:211-212 |
| 주석 표기 | 155행 주석은 「아래 쪽에 2.6초」지만 실제 코드는 위쪽(206행 주석 · 210행) | ui.dart:155 vs 206-210 |

## 3. 공통 조작 함수 `AppState.run` (`P/app_state.dart:412-427`)

- 성공 → `okMessage` 가 있으면 `toaster.show(okMessage, action:, onAction:)` (417).
- `ApiError` 401 → `logout(message: '로그인이 풀렸어요 — 다시 로그인하세요')` → 로그아웃 후 그 글자 토스트(420 · 408).
- 그 밖의 `ApiError`(주석: 403 · 409) → **서버 `message` 를 그대로** 토스트(423). 서버 본문에 message 없으면 `'요청을 처리하지 못했어요'` (`P/api/api.dart:57`).
- 성공 시 화면 갱신은 SSE 에 맡김(주석 412). 중복 탭 방지(in-flight) 없음 — 호출 시트 `_sending` 만 예외(call_sheet.dart:145).
- `ApiError` 아닌 예외(네트워크 끊김 등)는 잡지 않음 → 토스트 없음(정적 판단, 미실행).

## 4. 시술 현황 상태 변경 토스트 (룸 상세 · 판)

| 조작 | 성공 문구(원문) | 되돌리기 | 호출 API | 표시/허용 조건 | 근거 |
|---|---|---|---|---|---|
| 시술 [시작] | `'${c.room.title} · ${p.title} 시작'` | **있음** `'되돌리기'` → `runUndo(start)` · 5초 | `POST /api/procedures/{id}/start` | 버튼은 `p.state == 'wait'` 에서 보임 · `p.canStart` 일 때만 활성 | undo_sheet.dart:21-22 · room_screen.dart:421-424 · api.dart:92 |
| 시술 [종료] (캡처) | `'${c.room.title} · ${p.title} 종료'` | **있음** `'되돌리기'` → `runUndo(finish)` · 5초 | `POST /api/procedures/{id}/finish` | `doing` 에서 보임 · `p.canFinish` 일 때 활성 | undo_sheet.dart:23-24 · room_screen.dart:425-428 · api.dart:93 |
| 시작 되돌리기 | `'${c.room.title} · ${p.title} 시술 대기로 되돌림'` | 없음 | `POST /api/procedures/{id}/undo-start` | (a) 토스트 버튼 → 바로 실행, 확인 시트 없음 (b) 줄 되돌리기 아이콘(`doing && p.canUndoStart`) → 확인 시트 「시술 대기로 되돌리겠습니까?」 [취소]/[되돌리기] → 실행 | undo_sheet.dart:14-18 · 27-65 · room_screen.dart:420 · api.dart:95 |
| 종료 되돌리기 | `'${c.room.title} · ${p.title} 시술 중으로 되돌림'` | 없음 | `POST /api/procedures/{id}/undo-finish` | (a) 토스트 버튼 (b) 아이콘(`done && p.canUndoFinish`) → 시트 「시술 중으로 되돌리겠습니까?」 | undo_sheet.dart:14-18 · room_screen.dart:418 · api.dart:96 |
| 마취 시작 | `'${c.room.title} 마취 시작'` | 없음 | `POST /api/visits/{visitId}/anesthesia/start` | `a.canStart` 일 때 버튼 | room_screen.dart:457-464 · api.dart:80 |
| 마취 종료 | `'${c.room.title} 마취 종료'` | 없음 | `POST /api/visits/{visitId}/anesthesia/end` | `a.canEnd` | room_screen.dart:466-467 · api.dart:81 |
| 원장 호출 | `'${c.room.title} ${picks.length}개 시술 · $label'` — label = `'모든 의사 호출'` 또는 `'$toName 호출'` | 없음 | `POST /api/visits/{visitId}/calls` | 호출 시트 전송, 성공 시 시트 닫힘 · 실패 시 다시 활성 | call_sheet.dart:144-155 · api.dart:82 |
| 수락(지정 원장/의사 본인) | `'${c.room.title} $who수락'` — who = 관리자면 `'${docName} '` · 의사 본인이면 빈칸 | 없음 | `POST /api/calls/{id}/accept` (doctorId) | 관리자 + 전체 호출이면 아래 원장 고르기로 | accept.dart:18-29 · api.dart:88 |
| 수락(관리자 원장 고르기) | `'${c.room.title} ${docName(b, id)} 수락'` | 없음 | 위와 같음 | 시트 버튼 `'${docName} 수락 · $n건'` 누른 뒤 시트 닫고 실행 | accept.dart:105-113 |
| 다른 원장에게(전체 호출로) | `'${c.room.title} 전체 호출로 바꿈'` | 없음 | `POST /api/calls/{id}/reassign-all` | 두 곳(레이아웃별) | room_screen.dart:299 · 320 · api.dart:91 |
| 귀가 대기 | `'${c.room.title} ${c.customer.name} 귀가 대기'` | 없음 | `POST /api/visits/{visitId}/home` | 버튼 무조건 표시(서버 거절 시 message 토스트) | room_screen.dart:343-344 · api.dart:97 |
| (실패 공통) | 서버 `error.message` 원문 / 없으면 `'요청을 처리하지 못했어요'` / 401 = `'로그인이 풀렸어요 — 다시 로그인하세요'` | 없음 | — | 위 모든 조작 | app_state.dart:418-425 · api.dart:57 |

- **「각 취소」**: 프로토 시술 현황에는 시작/종료의 「취소」 조작이 따로 없고 위 `undo-start` · `undo-finish`(되돌리기)가 그 역할이다. 호출 취소 · 수락 취소 · 마취 취소 API 는 프로토 `api.dart` 에 없다(api.dart:80-97).
- **권한**: 토스트 [되돌리기] 버튼은 `canUndoStart/Finish` 를 다시 보지 않고 바로 API 를 부른다(undo_sheet.dart:22 · 24). 권한 · 시간 판단은 서버 몫, 거절이면 서버 message 토스트. 줄 아이콘은 스냅샷 `canUndo*` 로만 보임(undo_sheet.dart:2 주석 · room_screen.dart:418 · 420).
- 「호출함」 칩 · 원장 상태 등은 토스트 없음(SSE 반영).

## 5. 시술 현황 밖 상태 변경 토스트 (예약 · 접수 등)

| 조작 | 성공 문구(원문) | 되돌리기 | 근거 |
|---|---|---|---|
| 신분 확인 / 미확인 | `'저장했어요'` | 없음 | reservation_detail_screen.dart:254 · 260 |
| 신분증 사진 삭제 | `'사진을 지웠어요 · KOS 사진도 지움'` / `'사진을 지웠어요 · KOS 에는 없었어요'` / `'사진을 지웠어요'` | 없음 | reservation_detail_screen.dart:286-292 |
| 예약 취소 / 부도 | `'예약 취소'` / `'예약 부도'` (`reason == 'NO_SHOW'`) | 없음 | reservation_detail_screen.dart:518 |
| 접수 | `'접수 완료 · ${room?.title ?? ''}'` | 없음 | reservation_detail_screen.dart:566 |
| 상담 추가 | `'상담 추가'` | 없음 | reservation_detail_screen.dart:670 |
| 실장 호출 | `'${pick.name} 실장 호출'` | 없음 | reservation_detail_screen.dart:695 |
| 귀가 완료 | `'${d.customer.name} 귀가 완료'` | 없음 | reservation_detail_screen.dart:737 |
| 태블릿에 문진 표시 | `'${pick.name}에 표시 중'` | 없음 | launchers.dart:77 |
| 기기 이름 변경 | `'기기 이름을 바꿨어요'` | 없음 | app_state.dart:382 |
| 알림 설정 · 읽음 처리 | 성공 문구 없음(okMessage 미지정) · 실패만 토스트 | — | settings_screen.dart:53 · notifications_screen.dart:53 · 61 |

예약 화면의 `_write` 는 `app.run` 을 감싸고 끝나면 다시 불러옴(reservation_detail_screen.dart:95-100).

## 6. 상태 변경이 아닌 토스트(안내 · 오류)

| 영역 | 문구(원문) | 조건 | 근거 |
|---|---|---|---|
| 로그인/세션 | `'로그인이 풀렸어요 — 다시 로그인하세요'` | 조작 중 401 → 로그아웃 뒤 표시 | app_state.dart:420 · 408 |
| 딥링크 | `'로그인하면 고객 입력 화면을 열어요'` | 로그아웃 상태에서 `ccc://display` 링크 | app_state.dart:159 |
| QR claim | 서버 `e.message` | claim 실패 | app_state.dart:149 |
| 판 | `'호출이 끝났거나 방이 비었어요'` | 푸시로 열 방문이 판에 없음 | board_screen.dart:54 |
| 룸 상세 | `'${_roomTitle ?? '이 방'} 고객이 판에서 빠졌어요'` | 열린 방 카드가 판에서 사라짐 → 목록으로 | room_screen.dart:105-112 |
| 예약 상세 | `'예약을 찾을 수 없어요'` · `'여권 스캔을 열 수 없어요'` · `'시술 현황에서 방을 찾지 못했어요'` · 서버 message | 각 실패 | reservation_detail_screen.dart:87 · 303 · 763 · 404 |
| 문진 QR | `'문진 QR 을 받지 못했어요'` · 서버 message | 응답 이상/실패 | launchers.dart:24 · 92 · 96 · 110 · 121 |
| 여권 스캔 | 서버 message | 실패 | scan_screen.dart:198 |
| **통역** | `'이 기기에 ${langName(widget.langCode)} 음성이 없어요'` | 빠른 말하기 TTS 음성 없음 | interpret_bar.dart:30 · interpret_drawer.dart:368 |
| **통역** | WS 오류 `msg` | `kind == InterpErrorKind.auth` 일 때만 토스트(그 밖은 드로어 안 오류) | interpret_drawer.dart:131-133 |

## 7. 현재 DAY 앱과의 차이 (정책 결정 아님 — 사실만)

| 항목 | 프로토 | 현재 DAY 앱 | 근거(현재) |
|---|---|---|---|
| 엔진 | `Toaster` + `ToastLayer` | `ToastBus` + `ToastHost` | A/state/board_controller.dart:11-31 · A/ui/widgets.dart:105-175 |
| 성공 토스트 | 조작마다 있음(§4) | **없음** — `BoardController.run` 은 성공 시 토스트 안 함 | board_controller.dart:134-155 |
| 실패 토스트 | 서버 `message` 원문 | 403 = `forbiddenMessage`, 그 밖 = `actionMessage(e.code)`(코드 → 앱 내 원천 글자 표, 없으면 코드만). 세션 끝은 로그인 화면 | board_controller.dart:143-149 · A/core/copy.dart:18-50 |
| 되돌리기 | 토스트 [되돌리기](시작 · 종료, 5초) + 줄 아이콘 → 확인 시트 | 줄 ⋮ 팝업 메뉴 「시작 취소」/「완료 취소」 하나 → **확인 없이** `undo-start`/`undo-finish`. 토스트 버튼 없음. 메뉴는 `me.canEditBoard` + `canUndoStart/Finish` | A/ui/room_screen.dart:440-485 |
| 시간 | 2.6초 / 버튼 있으면 5초 | 3초 고정 | widgets.dart:136 |
| 위치 | top = safe + 68 | top = safe + 12, maxWidth 520 | widgets.dart:149-154 |
| 모양 · 색 | 어두운(0xE6222222) · 흰 글자 · 모서리 10 | **흰 배경** · elevation 4 · 모서리 8 · 글자 빨강(오류)/기본 · 그림자 red300/primary300 | widgets.dart:155-166 |
| 애니메이션 · 터치 | 180ms 페이드 · 버튼 없으면 터치 통과 | 페이드 없음 · IgnorePointer 없음(정적 판단) | widgets.dart:144-172 |
| 중복 | 덮어쓰기 + 세대 번호 | 덮어쓰기 + id(`dismiss(id)` 가 다른 id 무시) | board_controller.dart:18-30 |
| 중복 탭 | 없음(호출 시트만) | 키별 in-flight 차단(A-11) | board_controller.dart:133-137 |
| 추가 토스트 | — | KOS 반영 실패 `'$who — KOS 반영 실패 — 데스크에서 KOS 를 확인하세요'`(SSE) | board_controller.dart:115-131 · copy.dart:44 |
| 같은 원문 | `'호출이 끝났거나 방이 비었어요'` · `'… 고객이 판에서 빠졌어요'` · 통역 음성 없음 | 같은 글자(출처 주석 프로토 board_screen.dart:54 · room_screen.dart:111) | copy.dart:55-56 · board_screen.dart:75 · room_screen.dart:111 · interpret_widgets.dart:76 · 262 |
| API 경로 | `/api/procedures/{id}/…` · `reassign-all` | `/api/tasks/{id}/{start·finish·undo-start·undo-finish}` · `/api/calls/{id}/recall`(재호출 대상 지정) | board_controller.dart:162-174 |

## 8. 확인 못한 것

- 실행 화면 확인 안 함(정적만). 캡처의 실제 픽셀(색 · 글꼴 크기)은 코드값으로만 대조했다.
- 캡처의 「A-룸1」 · 「써마지 FLX 300shot」 은 `c.room.title` · `p.title` 의 데이터 값으로 보이며 소스 문자열이 아니다 — 데이터 출처는 확인 안 함.
- 웹 프로토(`UNDO_TOAST_MS` · `run(…, undoOf)` 언급, undo_sheet.dart:20 · ui.dart:158)는 조사 범위 밖이라 열지 않았다.
- 서버가 돌려주는 실패 `message` 실제 문구는 프로토 백엔드를 보지 않아 모른다.
- `Typo.body500/600` 의 실제 글자 크기 · `Ms.primary300` 실제 색값은 토큰 파일을 열지 않았다.
- ApiError 아닌 예외(네트워크) 경로의 실제 동작은 실행 확인 안 함.
