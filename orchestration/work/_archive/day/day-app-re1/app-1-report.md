# day-app-re1 app-1 결과 보고 — 직원 앱 차트 = 웹과 같은 기능 (U-23 · Delivery #282)

## 상태: done (커밋 · push · PR 안 함 — 워크트리 `app/` 변경만)

- 코드 워크트리 `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-app-re1`(`kknaksss/day-app-re1` · base `55e60aa4`). `backend/` · `deploy/` 는 건드리지 않음(backend 워커 변경은 그쪽 몫).
- 새 패키지 없음(`pubspec.yaml` · `pubspec.lock` 변경 없음). 실서버 · 로컬 스택 · 시뮬레이터 호출 없음 — 서버는 전부 테스트 더블.

## 수행 — 파일

| 파일 | 무엇 |
|---|---|
| `app/lib/model/chart.dart`(새) | 계약 C1 ~ C3 모델 — `ChartData`(customer · firstTab · tasks[].{assignee\|doctor}{body, staffId, savedAt, logId, base{body, doctorStaffId}} · staffOptions) · `ChartSaved`(saved · lastSavedAt · tasks) · `ChartConflict`(details.conflicts[]) · `PhotoList`(visitId · reread · groups[].items[]{photoId, shotAt, kosSynced} · kosError · rejected). 칸 이름 = 계약 그대로 |
| `app/lib/data/day_api.dart` | `ApiError.details`(공용 오류 본문 `details`) · `getJson` · `postJson(timeout)` · `postMultipart`(직접 짠 multipart — `category` + `file` 여러 개 · 길이 먼저) · `getBytes`(Bearer · 오류 본문 JSON 동일 처리). 공용 `_dispatch` · `_json` 로 나눔(기존 경로 동작 같음) |
| `app/lib/state/chart_controller.dart`(새) | 차트 상태 — 차트 GET 1회 · 탭별 초안 · 바뀐 줄(C20 정규화 비교) · [저장] = 그 탭 바뀐 줄만 `rows[]` 한 요청(15초) · 200 반영 · 409 충돌 반영(서버 글 그대로 · 바뀐 줄로 남김) · 거절 글자 · 사진 목록(탭 고를 때) · `reread` → 5초 뒤 `poll=1` · 보이는 동안 10초 `tick=1`(고르는 중 · 올리는 중 · 받는 중 건너뜀 · 숨김 · 백그라운드 · 닫힘 = 멈춤) · 올리기 · 삭제 · 다시 시도 · 파일 바이트 메모리 캐시 |
| `app/lib/ui/chart_sheet.dart`(다시 씀) | U-23 차트 창 — 세션 Navigator · 폰 전체 화면(MaterialPageRoute) / 아이패드 가운데 창(최대 410×640 · `showGeneralDialog` · 덮개 `Ms.dim`) · 머리(이름 · 발음 · 바이탈 · [✕]) · 탭 셋 · 「최근 저장 : HH:MM」 + [저장] · 시술 줄(시술명 · 담당자 · 차트 내용) · 닫기 표 · 확인 창(`showChartConfirm`) |
| `app/lib/ui/chart_photos.dart`(새) | 시술전후사진 탭 — 두 묶음 · 썸네일 · 올리기(+) · 삭제(✕ → 확인 창) · 「KOS 미반영」(경고 아이콘) + [다시 시도](↻) · 크게 보기(검정 전체 화면 · [닫기] · 세션 Navigator) · 사진 고르기 흐름 |
| `app/lib/ui/session_nav.dart`(새) | 세션(루트) Navigator context 도우미(`chatOverlayContext` 재사용) |
| `app/lib/ui/doctor_picker.dart` | `showPickerSurface` → 세션 Navigator(폰 시트 · 아이패드 팝오버 · 팝오버 덮개 투명 그대로 · 기준 위치 = 세션 Navigator 영역) · 새 `showStaffPicker`(담당자 고르기 — 같은 드로어 · 목록만 · 이름 + 직군 글자 · 고르면 닫힘) |
| `app/lib/ui/room_screen.dart` | 시술 줄 누름 → 새 `showChart` · 확인 시트 / 창(`confirmUndo`) → 세션 Navigator |
| `app/lib/ui/shell.dart` | 세션 Navigator 를 `NavigatorPopHandler` 로 감쌈 — Android 뒤로가 세션 Navigator 위 창(차트 · 시트 · 크게 보기)부터 닫고 없으면 탭 스택으로 |
| `app/lib/ui/theme.dart` | `colorScheme.outlineVariant` · `tabBarTheme.dividerColor` = `Ms.gray300`(까만 줄 원인 = M3 TabBar 구분선이 outlineVariant 기본값 onSurface 검정) · 탭 지시선 · 글자 색 = DAY 주색 · gray700 |
| `app/lib/core/copy.dart` | 웹 `board_messages.py` `MESSAGES` · `UNSET_MESSAGES` 와 맞춤(차트 거절 넷 넣음 · `chart_staff_required` · `staff_not_listed` 를 미정 목록에서 뺌 — 웹이 이미 글자를 정함) · `chartSaveMessage`(차트 저장 `doctor_not_listed` = 「선택할 수 없는 담당자입니다」) · 차트 · 사진 글자(웹 템플릿 · 웹 상수 그대로) |
| `app/lib/chat/screens/chat_attach_sheet.dart` | `photosOnly`(최근 줄 동영상 뺌) · `limit`(null = 한도 없음) — 채팅 기본값 그대로 |
| `app/lib/chat/photo_pick.dart` | `pickChartGallery`(사진만 · 한도 없음 `pickMultiImage` → 같은 JPEG 길 · 임시 파일 지움) |
| `app/ios/Runner/Info.plist` | 카메라 · 사진 보관함 문구 = D15 글자 그대로 |
| 테스트 | 새 `test/ui/chart_test.dart`(26) · `test/state/chart_controller_test.dart`(14) · `test/build/info_plist_test.dart`(2) · `test/support/chart_fixtures.dart` · 갱신 `test/core/board_messages_contract_test.dart`(+2) · `detail_polish_test` · `room_move_test` · `session_race_test`(옛 「차트 API 0건」 · 「간호 관리 차트」 기대를 새 계약으로) |

## 화면 흐름

1. 룸 상세 시술 줄 누름 → 세션 Navigator 에 차트(폰 = 전체 화면이라 하단 탭바가 가려짐 · 아이패드 = 가운데 창 · 레일까지 덮개) → 받는 동안 로딩 원 → `GET /api/visits/{id}/chart` 1회 → 처음 탭 = `firstTab`. 받기 실패 = 그 코드 토스트 + 창 닫힘(OQ-A75).
2. 차트 탭: 시술마다 [시술명 | 담당자 칸 ▾] + 여러 줄 글 칸. 담당자 칸 누름 → 원장 고르기 드로어(폰 바텀 시트 · 아이패드 팝오버)에 그 칸 `staffOptions` → 한 명 고르면 닫힘. 글 · 담당자를 바꾸면 [저장] 켜짐(되돌리면 꺼짐).
3. [저장] → 보내는 동안 [저장] 꺼짐 · 그 탭 칸 잠금 · [✕] · 뒤로 꺼짐 → 200 = 「최근 저장 : HH:MM」(KST) 바뀜 · 창 그대로 · 토스트 없음 / 409 충돌 = 걸린 줄 글이 서버가 이어 붙인 글로 · 담당자 = KOS 값 · 토스트 · [저장] 켜짐 / 그 밖 거절 = 토스트 · 쓴 것 그대로.
4. 시술전후사진 탭: 「시술 전」 · 「시술 후」 묶음 → 썸네일 · (+) → 채팅 첨부 시트(사진만 · 한도 없음: 카메라 칸 = 한 장 찍어 바로 올림 · 최근 줄 고르고 [전송] · 「사진」 = 시스템 고르기 여러 장) → 한 요청 업로드 → 응답 토스트. ✕ → 「사진을 삭제할까요?」 [취소] [삭제]. 경고 아이콘 = KOS 미반영 · ↻ = 다시 시도. 썸네일 누름 = 크게 보기.
5. 닫기: 미저장 없음 = [✕] · Android 뒤로 · 머리 끌어 내림(폰) · 바깥 누름(아이패드) · iOS 가장자리 밀기(폰) 모두 닫힘 / 미저장 = [✕] · Android 뒤로 → 「저장하지 않고 닫을까요?」 [계속 쓰기] [버리고 닫기] · 끌어 내림 · 바깥 누름 = 아무 일 없음 · iOS 밀기 = 막힘(PopScope canPop false → Cupertino 밀기 꺼짐).

## 검증 — 명령과 결과 (`cd app` · fvm Flutter 3.44.8 — PATH 에 flutter 가 없어 `~/fvm/versions/3.44.8/bin` 사용)

| 명령 | 결과 |
|---|---|
| `flutter analyze` | **No issues found** |
| `flutter test` | **+460 · ~81(skip — 기존과 같은 수) · 실패 0**. 시작 전 기준선 = +415 · ~81 · **-1**(`board_messages_contract_test` — 웹 표에 차트 거절 글자 · 예약 미정 코드가 이미 들어가 앱 복제가 뒤처져 있었음 · 이번에 고침) |
| `flutter build ios --no-codesign` | **✓ Built build/ios/iphoneos/Runner.app (20.8MB)** · exit 0(pod install 뒤 추적 파일 변경 없음 · SwiftPM 미지원 플러그인 경고는 기존과 같음 — 무관) |

새 테스트가 덮는 인수 조건: A-51(폰 전체 화면 · 탭바 가려짐 · 아이패드 창 크기 · 레일 안 눌림 · 탭 글자 셋 · firstTab · 머리 · 차트 GET 1회 · 스냅샷 노트 안 보임 · 시술 전 의사차트 보임) · A-52(테마 값 · 차트 탭 구분선 색 · 폰 확인 시트 · 폰 원장 고르기 드로어 · 아이패드 팝오버(투명 덮개) 모두 탭바 · 레일 안 눌림) · A-53 · A-54(요청 본문 · 잠금 · 200 · 409 · 담당자 빈 줄 · 401 세션 끝 → 차트 닫힘) · A-55(닫기 표 전부 — iOS 밀기는 `debugDefaultTargetPlatformOverride` · 보내는 중 닫기 꺼짐) · A-56 · A-57(10초 tick · 다른 탭 · 닫힘 = 0 · 백그라운드 = 단위 테스트) · A-58(앨범 여러 장 한 요청 · 카메라 1장 · 권한 거부 글자 · KOS 미반영 → 다시 시도) · A-59(삭제 확인 · 크게 보기 · 같은 바이트 1회 · Bearer) · A-60(보기 권한) · A-38(차트 GET 을 부름) · A-17(Info.plist 문구 · 권한 키 셋) · 계약 시험(웹 MESSAGES · UNSET · PHOTO_* 상수).

## 계약 대조 — C0 ~ C3 · SPEC

| 항목 | 같음/다름 |
|---|---|
| C1 `GET /api/visits/{id}/chart` 앱이 쓰는 칸 | 같음(`author` 안 씀) |
| C2 요청 `{chart, rows[{taskId, body, staffId, baseLogId, baseBody, baseDoctorStaffId}]}` | 같음 — `baseBody` = `base.body ?? ''` · 간호관리 탭 `baseDoctorStaffId` = null · 빈 담당자 = `staffId: null` 그대로 보냄(서버 409) |
| C2 200 `{saved, lastSavedAt, tasks}` · 409 `details.conflicts[{taskId, body, staffId, base, baseLogId}]` | 같음 — backend 워커 `schemas/board_charts.py` 도 읽어 대조(읽기만) |
| C3 ① ~ ⑤ 경로 · 쿼리(`poll=1` · `tick=1`) · multipart `category` + `file` · 응답 칸 | 같음 — backend `routers/api/board_photos.py` · `schemas/photos.py` 대조(읽기만) |
| 오류 코드 → 글자 | `chart_conflict` · `chart_staff_required` · `staff_not_listed` · 차트 `doctor_not_listed` · `photo_too_large`(413 — 앞단 HTML 413 도) · `photo_disabled` = SPEC 글자 · `not_found` · `forbidden` = 지금 글자 · 401 = 세션 끝 |
| D13 탭 글자 · D15 문구 · D9 · D14 · D6′ · D12 · OQ-A67 · A68 · A70 · A73 · A74 · A75 기본값 | 같음 |
| **다름 ①** 「최근 저장」 · [저장] 자리 | 웹 = 탭 줄 오른쪽 · 앱 = 탭 줄 **바로 아래 오른쪽 띠**. 폰 390 · 아이패드 창 410 폭에 탭 셋 + 「최근 저장 : HH:MM」 + [저장]이 한 줄에 안 들어감(탭이 밀려 눌리지 않았음 — 테스트로 확인). 2루프 E2E 에서 정할 자리 |
| **다름 ②** 크게 보기 | SPEC = 채팅 `chat_photo_screen.dart` 재사용 · 앱 = 같은 꼴(검정 · [닫기])을 차트 쪽에 따로 둠 — 채팅 화면은 `ChatMessage` · 채팅 사진 캐시에 묶여 있어 그대로 못 씀. 보낸 사람 · 시각 줄 없음(차트 사진엔 그 값이 없음) |
| **다름 ③** 사진 고르기 화면 | OQ-A73 기본값대로 채팅 첨부 시트 재사용 — 시트 머리 「최근 사진」 · [전송] · 「사진」 · 「더 고르기」 · 권한 안내 글자는 채팅 글자 그대로(OQ-A78 「채팅 첨부 시트 글자를 쓰면 그대로」) |

## 계약 · SPEC 에서 애매했던 곳(앱이 고른 값 — 코디 확인)

1. **올리기 시간 제한 = 120초** — 원천 없음(차트 저장은 15초 · 채팅 사진 1장 40초). 본문 상한 100MiB 기준 앱 값.
2. **`chart_too_long`** — 글자 미정 · 서버가 안 보냄. 오면 웹 `message_of` 규칙대로 「요청이 올바르지 않습니다」.
3. **400 `photo_type`(요청 전체 거절)** — 글자 원천 없음 → 웹 규칙대로 「요청이 올바르지 않습니다」(장마다 빠진 것은 `rejected` → C36 글자).
4. **충돌 줄의 비교 기준** — 걸린 줄은 「바뀐 줄」로 표시해 둠(SPEC 「[저장] 켜짐」). 그 줄을 KOS 글로 손으로 되돌려도 [저장]은 켜진 채(다음 저장에서 서버가 판단).
5. **`kosSynced` 칸이 없으면** 반영된 것으로 봄(계약상 늘 옴).
6. **아이패드 원장 고르기 팝오버 기준 위치** = 세션 Navigator 영역(셸 전체) 기준으로 옮김(D14 「WORK 에서 맞춘다」).

## 이슈 · 코디가 확인할 것 · 사람 눈에 이상해 보일 자리

- **옆 효과 ① Android 뒤로** — 셸에 `NavigatorPopHandler` 를 더해 Android 뒤로가 세션 Navigator → 탭 스택 순으로 간다. 그전에는 세션 Navigator 위 창(채팅 크게 보기 등)이 Android 뒤로를 받지 못했다(테스트로 확인 — 차트가 안 닫혔음). iOS 앱엔 영향 없음.
- **옆 효과 ② 방 옮기기 시트(U-21)** 도 같은 `showPickerSurface` 라 세션 Navigator 로 올라감(탭바까지 덮음). 통역 시트 둘은 그대로(OQ-A77).
- **카드가 판에서 빠질 때** — 룸 상세는 목록으로 돌아가지만, 세션 Navigator 에 떠 있던 원장 고르기 · 확인 시트는 남는다(전엔 탭 Navigator 라 시트부터 닫혔음). 그 시트로 보내면 서버 `not_found` 토스트. 차트는 OQ-A69 대로 그대로.
- **푸시 · 알림으로 다른 방문 열기** — 셸이 세션 Navigator 를 비우므로(기존 규칙) 열린 차트의 **미저장 글이 확인 없이 버려짐**. SPEC 에 이 길 규칙 없음 — 확인 필요.
- 폰 차트 진입 움직임 = 플랫폼 기본 페이지 전환(iOS = 오른쪽에서 밀려 들어옴 · 가장자리 밀기 닫힘). 「끌어 내림」은 머리 줄에서만 받음(글 칸 스크롤과 겹치지 않게).
- 사진 탭 버튼은 전부 아이콘만(＋ · ✕ · ↻ · 경고) — 접근성 이름도 비움(웹도 미정 · OQ-A78).
- 담당자 칸이 빈칸이면 빈 테두리 상자 + ▾ 만 보인다(웹도 빈 값 · 자리 글자 없음).

## 코디가 시뮬레이터에서 볼 순서(로컬 BE + KOS 데모 · A4)

1. 로그인 → 시술현황 → 카드 → 시술 줄 누름: 폰 전체 화면 · 탭바 가려짐 / 아이패드 가운데 창 · 레일 어둡게. 탭 셋 글자 · 처음 탭 · 머리 바이탈 · 탭 아래 까만 줄 없음.
2. 간호관리차트: 글 고침 → [저장] → 「최근 저장」 바뀜 → KOS 데모에서 같은 줄 고친 뒤 다시 저장 → 충돌 토스트 · 이어 붙인 글.
3. 담당자 칸 → 드로어(폰 시트 · 아이패드 팝오버) · 직군 글자 · 빈 담당자로 저장 → 「담당자를 선택해 주세요」.
4. 미저장 상태에서 ✕ · 끌어 내림 · 바깥 누름 · iOS 가장자리 밀기 · 미저장 없을 때 같은 동작.
5. 시술전후사진: 탭 열림 → KOS 웹에서 올린 사진이 10초 안에 보임 · (+) 카메라 1장 · 앨범 여러 장 → KOS 데모 일정 사진 탭 확인 · 삭제 확인 창 · 크게 보기 · KOS 실패를 만들 수 있으면 경고 · ↻.
6. 보기 권한 계정(코디 · 상담)으로 같은 차트 — 버튼 없음.
7. 룸 상세 [의사 호출] 드로어 · ⋮ → 「시작 취소」 확인 시트가 하단 탭바까지 덮는지(폰) · 아이패드 팝오버 · 창이 레일 위인지.
8. 권한 창 문구(카메라 · 사진 보관함 첫 요청) = D15 글자.

## 실행 못 한 검증 (pending)

- 시뮬레이터 · 기기 · 로컬 BE 실물(A4) — 브리프 §7 대로 코디 몫.
- 서명 · TestFlight — 사용자 몫.
