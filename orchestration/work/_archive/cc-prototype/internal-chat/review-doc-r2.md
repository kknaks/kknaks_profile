# 리뷰 리포트 — internal-chat / doc (2026-10-29 · r2)

검수 대상: `20-spec/spec-007-internal-chat.md` 0.2.0 (`S7:Ln`) · `30-work/work-011-internal-chat.md` (`W11:Ln`) · SPEC-004 §6.8 바뀐 줄(`S4:Ln` · `git diff`) · `spec-r2-report.md`(대조표는 믿지 않고 줄을 직접 열어 봄)
대조 기준: DEC-009 D-01 ~ D-44 (`D9-nn`) · 확정 시안 r2 · `review-doc-r1.md`(`R1:`) · 코드 `/Users/kknaks/git/toy_pr2/cc-prototype/procedure` HEAD `dbf0b53`(작업 트리 깨끗함 · 읽기만)
코디 기본값으로 받은 것: OQ-932 · OQ-933 · OQ-939 — 이 셋은 지적 대상이 아니라 SPEC 이 그 뜻대로 적었는지만 봤다(셋 다 맞음)

## 판정: WARN

**FAIL 0 · WARN 6.** r1 FAIL 4 는 모두 닫혔다. 새 WARN 은 모두 한 줄 고침이거나 워커가 주의만 하면 되는 자리로, 코드 워커가 막힐 빈칸은 없다 → **코드 발주 가능**. 다만 W2-1(처음 추가된 사람의 안 읽음 시작점)은 사용자 눈에 보이는 동작이라 발주 전에 한 줄로 정하는 게 좋다.

### 대조 수치

| 대조 | 결과 |
|---|---|
| r1 FAIL 4 · WARN 17 (21) | **닫힘 20 · 덜 닫힘 1(W-12 → W2-5) · 안 닫힘 0**. F-4 는 닫혔지만 「부르는 곳」 줄이 하나 틀렸다(W2-3) |
| DEC D-01 ~ D-44 → SPEC | **44 / 44**. D-38 ~ D-44 각각 본문에 있음(아래 표) · 뒤집음 0 · 넓힘 0 · 좁힘 0 |
| 코디 기본값 OQ-932 · 933 · 939 | SPEC 반영 3 / 3 (`S7:141 · 242 · 244 · 291` / `S7:476 · 492 · 672` / `S7:110 · 236 · 289 · 301`) |
| 새 §12 자리 18(B19 ~ B25 · A21 ~ A31) | **18 / 18 직접 열어 확인** · 줄 · 지금 모양 맞음 18 · 「부르는 곳」 목록이 덜한 곳 1(A24 → W2-3) · §5 보다 좁게 적은 곳 1(A31 → W2-4) |
| `async def` 경로 목록 | `S7:253` = #1 ~ #14 **전부**(SSE · 푸시 9 + 사진 올리기 1 + 읽기 4). 빠짐 0 |
| public grep | 비밀 패턴 · 메일 · 전화 · 32자 이상 16진 · `TEAM_ID=` · `password=` = 0(걸린 4건은 `CHAT_SCHEMA` · `MIGRATIONS` 오탐) → **PASS** |

---

## r1 지적 하나씩 (SPEC · WORK 줄을 직접 열어 봄)

| r1 | 판정 | 본 줄 |
|---|---|---|
| F-1 탭 머리 | **닫힘** | `S7:395` 폰 = `TabScaffold(tab: AppTab.chat)` → `AppHeader` [Céramique][채팅][종] + 아래 제목 없는 [새 대화] · `S7:412` 폰 대화 = `DetailHeader` 「‹ 채팅」 · `S7:461-463` 아이패드 · `S7:556-557` A21 · A22 · `S7:610` C1. 코드: `shell.dart:229` `AppHeader(title: tabName[tab]!)` → 「채팅」이 헤더 가운데에 한 번만 나온다(맞음) |
| F-2 시각 | **닫힘** | `S7:118` `to_db_ms` · 같은 폭 문자열 · `S7:141` `last_read_message_id` · `S7:242` `id >` 셈 · `S7:244` 읽음 `{messageId}` · `max(지금, min(messageId, 마지막 id))` · `S7:245` · `S7:288` `updated_at >= since` · `S7:254` `iso_ms` · `parse` → `to_db_ms` · `%2B` · `S7:588` 경계 시험. 코드: `clock.py:33-41` `parse` 가 `Z` · 오프셋 · 밀리초 · 오프셋 없음(UTC)을 받음 · 못 읽으면 `None` → 400 으로 이어짐(맞음) |
| F-3 async | **닫힘** | `S7:253` · `S7:296` · `S7:530-531 · 535` · `S7:591`(HTTP 경로 → 가짜 APNs) · `W11:59 · 77 · 98`. 코드: `actions.py:19-83` 모두 `async def` · `notifications.py:18 · 24 · 29 · 35` · `photos.py:55` 는 `def`(SPEC 이 「선례 아님」으로 적음 — 맞음) |
| F-4 숨김 | **닫힘**(줄 하나 → W2-3) | `S7:391` 어느 길이든 · `S7:476` 셸 안 층 + 열린 수 · `S7:542 · 558 · 559` · `S7:601` 세 길 시험 · `S7:610` C1 두 길 · `W11:76`. 코드: `showQrScreen`(`qr_show_screen.dart:16-21`) · `showPassportScan`(`scan_screen.dart:26-30`) 둘 다 `rootNavigator: true` push 이고 앱 안 다른 `rootNavigator: true` push 는 `shell.dart:241`(알림 목록)뿐 → 열린 수를 이 두 함수에서 세면 모든 길이 지난다(맞음) |
| W-1 | 닫힘 | `S7:388` `kind ≠ system` · `deletedAt` · 보고 있는 방 |
| W-2 | 닫힘 | `S7:281` `items` 방만 · 숨기기는 읽음 안 바꿈 |
| W-3 | 닫힘 | `S7:234-235` ①③④ · `S7:289` ② · `S7:417` · `S7:584` |
| W-4 | 닫힘 | `S7:293` 409 `photo_disabled` · 파일 없음 404 — 코드 `id_photo.py:116-121` 와 같은 꼴 |
| W-5 | 닫힘 | `S7:165 · 167 · 293 · 354 · 590` |
| W-6 | 닫힘 | `S7:355 · 425` 12초 · 40초(코드 `api.dart:31 · 174` 맞음) · OQ-934 ~ 937 · `S7:500-503` |
| W-7 | 닫힘 | `S7:374-375 · 484 · 563-564` (코드 `settings_screen.dart:191-202` · `resv_ui.dart:36 · 162` 맞음) |
| W-8 | 닫힘 | `S7:537` A2 `92-104` · `S7:519` B9 `254-259`(코드 맞음) |
| W-9 | 닫힘 | `S7:500-503 · 558 · 560-562 · 565` |
| W-10 | 닫힘 | D9-40 → `S7:243` · `S7:474` · `S7:566` · C4 |
| W-11 | 닫힘 | `S7:262 · 445` · OQ-936 |
| W-12 | **덜 닫힘** | `S7:350 · 359` 는 다시 인코딩 + `flutter_image_compress` 인데 §12 A14 `S7:549` 는 `image_picker` 만 → W2-5 |
| W-13 | 닫힘 | `S7:255 · 534 · 592` |
| W-14 | 닫힘 | `W11:72-73` 줄 단위 · `S7:583 · 586` |
| W-15 | 닫힘 | `W11:74-76` (APP2 `api.dart` · `header.dart` · APP3 `main.dart` · `launchers.dart` · `qr_show_screen.dart` · `scan_screen.dart`) |
| W-16 | 닫힘 | `W11:78` WP-E2E ① OQ-931 |
| W-17 | 닫힘 | `S4:690` · `S4:697` 「(채팅 더해 5 — SPEC-007)」 · 새 행 698 |

## D-38 ~ D-44 반영

| D | SPEC 줄 | 판정 |
|---|---|---|
| D-38 헤더 = `AppHeader` · 아래 [새 대화]만 · 아이패드 목록 칸 위 | `S7:377 · 395 · 412 · 461-463 · 491 · 556-557 · 610` | 맞음 |
| D-39 앞 = 앱 안 배너만 · 소리 없음 · 호출은 그대로 | `S7:342 · 473 · 613` | 맞음 |
| D-40 보고 있는 방 = 채팅 탭 + 그 대화 맨 위 | `S7:243 · 244 · 474 · 566 · 601 · 613` | 맞음(A31 은 좁게 적음 → W2-4) |
| D-41 실패 말풍선 저장 안 함 | `S7:427 · 490 · 502` | 맞음 |
| D-42 비활성 1:1 입력 막고 안내 | `S7:110 · 236 · 418` (+ 서버 409 = OQ-939) | 맞음 · 앱 판정 근거 `Member.active`(`S7:262`) 있음 |
| D-43 다시 초대 = 그때까지 읽음 · 혼자 남은 그룹 그대로 | `S7:201 · 203 · 581 · 584 · 587` | 맞음(처음 추가는 → W2-1) |
| D-44 띄우기 숨김 = 어느 길로 열었든 | `S7:391 · 476 · 492 · 542 · 559 · 601 · 610` | 맞음 |

---

## FAIL

없음.

## WARN

### W2-1 처음 추가된 사람의 안 읽음 시작점이 없다 — 그룹 이력 전체가 안 읽음이 된다 (r2 가 만든 자리 · D9-43 옆)

- **SPEC**: `S7:141` `last_read_message_id` = 「… 없으면 0」 · `S7:201` 다시 초대만 「= 그 방 마지막 메시지 id」 · `S7:200` 참여자 추가(처음)에는 값이 없다
- **깨지는 곳**: 대화가 쌓인 그룹에 처음 추가된 사람은 행을 만들 때 열 기본값 0 → `id > 0` 인 남의 메시지 전부가 안 읽음 → 방 배지 「99+」 · 탭 배지 +1. 같은 사람이 나갔다 다시 초대되면 0 이 된다(D9-43) — 처음 추가 쪽이 더 많이 센다
- r1 은 시각 기준이라 「언제부터 셀지」가 `last_viewed_at` 초기값에 숨어 있었고, r2 가 id 로 바꾸면서 드러났다. 워커는 막히지 않고 0 을 넣을 것이므로 **조용히 지나가는 자리**다
- **고칠 것**: §4.2 「참여자 추가」 줄에 「처음 추가 = 다시 초대와 같게 `last_read_message_id` = 그 방 마지막 id · `last_viewed_at` = 지금」(D9-43 과 같은 이유) 또는 「0 — 옛 메시지 전부 안 읽음」 중 하나를 적고, §13.1 「추가 · 나가기」에 단언 한 줄. → 코디 몫(D9-43 을 넓히는 기본값)

### W2-2 메시지가 0개인 방의 `since` · 읽음 값

- `S7:245 · 499` `since` = 「받은 것 중 가장 늦은 `updatedAt`」 — 받은 게 없는 방(막 만든 1:1 · 그룹)은 기준이 없다. `S7:291` `{messageId}` 도 그린 메시지가 없으면 무엇을 보내는지(0 허용인지 · 400 인지) 없다
- 깨지지는 않는다(`min(0, 0)` = 0). 앱 · back 이 다르게 고르면 빈 방을 열 때마다 400 토스트가 뜰 수 있다
- **고칠 것**: 「받은 게 없으면 `since` 없이 처음 읽기」 · 「`messageId` = 0 이상 정수 · 0 허용」 두 줄

### W2-3 「예약 상세」 길의 실제 호출 자리가 다르고, 시험 이음새를 적지 않았다 (F-4 줄)

- **SPEC**: `S7:391` 「[여권 스캔] `launchers.dart:103`」 · A24 `S7:559` 부르는 곳 = `launchers.dart:82-83 · 86-98 · 103 · 106-`
- **코드**: `launchers.dart:103` 은 바꿔 끼울 수 있는 **변수 정의**(`ScanOpener? openPassportScan = showPassportScan;`)다. 예약 상세에서 실제로 부르는 곳은 `screens/reservation_detail_screen.dart:301-304`(`_scan` → `openPassportScan`) · `:309-311`(`_questionnaireHere` → `showQuestionnaireQrHere`)이다. 열린 수를 `showQrScreen` · `showPassportScan` 안에서 세면 이 길도 지나므로 **동작은 맞다**
- **시험 이음새**: 지금 시험이 `openQrScreen` · `openPassportScan` 을 가짜로 바꿔 끼운다(`test/qr_show_test.dart:143 · 160` · `test/e2e_batch1_test.dart:130`). 가짜는 `show*` 를 안 거치므로 열린 수가 오르지 않는다 → §13.2 「세 길 모두 배너 없음」 시험(`S7:601`)을 그 가짜 위에 쓰면 배너가 떠서 깨지거나, 거꾸로 수를 직접 올리는 가짜로 쓰면 실제 길을 안 본다
- **고칠 것**: A24 부르는 곳에 `reservation_detail_screen.dart:301-304 · 309-311` 을 더하고 `launchers.dart:103` 은 「변수 정의(시험이 바꿔 끼움)」로 적는다. §13.2 에 「세 길 시험은 실제 `showQrScreen` · `showPassportScan` 을 거친다(가짜 `ScanChannel` 등) — `openQrScreen` · `openPassportScan` 을 가짜로 바꾼 시험으로 대신하지 않는다」 한 줄

### W2-4 A31 「보고 있는 방」 판정이 §5 보다 좁다 — 루트 Navigator 위 화면이 안 잡힌다

- **SPEC**: §5 `S7:243` = 채팅 탭 · 그 대화가 맨 위 · **그 위에 방 정보 · 참여자 추가 · 사진 크게 보기 · 시트 · 대화상자가 없음** / A31 `S7:566` = 「지금 탭이 채팅 · 그 대화가 채팅 Navigator 맨 위일 때만」
- **코드**: 대화상자 · 바텀 시트는 기본이 루트 Navigator(`showDialog` · `showModalBottomSheet` 기본값)이고, 사진 크게 보기는 SPEC 이 `rootNavigator` 전체 화면으로 적었고(`S7:492`), 아이패드 방 정보 시트는 알림 목록 꼴(`shell.dart:240-261` · `showGeneralDialog(useRootNavigator: true)`)이다. 이것들은 **채팅 Navigator 스택에 안 들어가므로** A31 대로 「채팅 Navigator 맨 위」만 보면 그 화면이 떠 있어도 보고 있는 방으로 잡힌다 → 읽음이 나가고 배너가 걸러진다(§5 와 다름)
- **고칠 것**: A31 에 「루트 Navigator 위에 채팅이 올린 화면(크게 보기 · 대화상자 · 시트 · 아이패드 방 정보)이 있으면 아님 — 예: 루트에 `RouteObserver` · 또는 그 화면을 열고 닫을 때 상태를 바꿈」 한 줄

### W2-5 §12 A14 에 `flutter_image_compress` 가 없다 (r1 W-12 덜 닫힘)

- `S7:350 · 359 · 663` 과 `W11:75` 는 `image_picker` + `flutter_image_compress` 두 패키지인데 `S7:549` A14 「바뀜」은 `image_picker` 만. WORK 에 있어 워커는 막히지 않는다 → A14 에 하나 더

### W2-6 WP-REVIEW 의 `async def` 검사 명령이 도우미 함수에도 걸린다

- `W11:77` `grep -n "^def " procedure/back/app/api/chat.py` = 0. 지금 router 파일은 경로 아닌 도우미도 맨 앞 `def` 로 둔다(`api/photos.py:23` `def _int` · `api/actions.py:42` `def accept_source`). 채팅 router 에 도우미가 하나라도 있으면 경로가 다 `async def` 여도 검사가 0 이 아니다
- **고칠 것**: 「`@router.` 바로 아래 줄이 모두 `async def`」(예: `grep -A1 "@router\." … | grep -c "^def "` = 0)로

---

## 조용히 통과하는 자리 (시험은 초록 · 계약은 깨짐)

1. **처음 추가된 사람의 안 읽음 99+**(W2-1) — §13.1 에 처음 추가 경우 단언이 없어 0 기본값으로 초록
2. **세 길 배너 시험을 바꿔 끼운 가짜 위에 씀**(W2-3) — 수를 직접 올리는 가짜면 초록, 실제 `show*` 는 안 봄
3. **보고 있는 방 = 채팅 Navigator 맨 위만**(W2-4) — 시험이 채팅 Navigator 안 화면(방 정보 폰 · 참여자 추가)만 보면 초록, 루트 위 크게 보기 · 대화상자 · 아이패드 시트는 시험 밖
4. **`async def` 검사 grep 오탐**(W2-6) — 이건 반대로 거짓 FAIL 쪽
5. (확인만 — 안전) `since >=` 경계 · `iso_ms` · `%2B` 는 `S7:588` 이 같은 밀리초 고정 · KST · `Z` · 밀리초 없음 · 못 읽음까지 단언하므로 F-2 는 시험이 잡는다. 푸시는 `S7:591` 이 HTTP 경로로 단언하므로 F-3 도 시험이 잡는다

## 사용자가 실물에서 만날 자리

1. 오래된 그룹에 처음 초대받으면 그 방 배지가 「99+」(W2-1 — 정하기 전 기본 동작)
2. 아이패드에서 방 정보 시트 · 알림 목록 시트 · 대화상자가 떠 있을 때 온 다른 방 배너가 **어둡게 깔린 막 아래**에 보이고 눌리지 않는다(셸 안 층 · OQ-933 의 부작용 — 폰 전체 화면은 아예 안 보임)
3. 사진 크게 보기 · 알림 목록(폰)을 보는 동안 온 채팅은 배너 없이 4초가 지나간다 — 탭 배지 · 방 목록만 바뀜(OQ-933 · 코디가 받은 값)
4. 앱이 앞에 있어도 Dart 가 준비되기 전 아주 짧은 순간(막 켠 직후)에 온 채팅은 iOS 배너 + 소리로 뜬다(A11 「준비 전이면 지금처럼 배너」 `S7:546` — 띄우기와 같은 지금 꼴. D9-39 의 예외로 한 줄 알아 두면 됨)
5. 비활성 상대 1:1 은 입력줄 대신 「비활성 계정이에요」(D9-42 · 사용자 결정대로)

## 참고 (기존 부채 — 이번 판에서 고칠 것 아님)

- `shell.dart:216` `TabScaffold` 주석은 「[메뉴명][Céramique][알림]」인데 `header.dart:1` 과 실제 그리기는 [Céramique][메뉴명][알림] — 코드 주석만 낡음
- SPEC-004 §7.3 경로 수 49 ↔ 코드 51 — OQ-920 그대로(코디 처분대로)
- `spec-r2-report.md` 미결 5 — `scripts/lint-pipeline.py` 가 리뉴얼 레포에 없음(역할 `skills.md` 낡은 줄)

---

## 사용자 판단 후보 · 코디 몫

| # | 무엇 | 지금 | 누구 |
|---|---|---|---|
| 1 | 처음 추가된 사람의 안 읽음 시작점(W2-1) | SPEC 에 없음 → 열 기본값 0 = 이력 전부 안 읽음 | **코디 몫**(D9-43 과 같은 이유로 「추가 시각 = 읽음」을 권함). 사용자에게 물을 무게는 아님 — 같은 결정(D9-43)의 짝 |
| 2 | W2-2 ~ W2-6 | 한 줄 고침 | planner(발주 전) 또는 코드 발주 브리프에 「주의」로 |

새 「사용자 판단 후보」는 없다(r1 후보 7 은 D9-38 ~ D9-43 으로 모두 닫힘).

---

## 확인한 새 코드 자리 (§12 r2 18개 · 전부)

| # | 자리 | 결과 |
|---|---|---|
| B19 | `domain/clock.py:23-25` `iso` · `28-30` `to_db` · `33-41` `parse` | 맞음(`parse` = `Z` → `+00:00` · 오프셋 없음 = UTC · 실패 `None`) |
| B20 | `service/push.py:175-187` `_dispatch` | 맞음(183 「푸시 건너뜀(이벤트 루프 없음)」 · return) |
| B21 | `service/stream.py:59-75` `send_to_account` · `_send` | 맞음(59-61 · 71-75 `put_nowait`) |
| B22 | `main.py:107-111` `validation_error` | 맞음(400 `invalid_request`) |
| B23 | `service/id_photo.py:116-121` | 맞음(116-118 409 `photo_disabled` · 119-121 404) |
| B24 | `service/push.py:236` | 맞음(무엇 · `_tail(token)` · status · reason) |
| B25 | `api/actions.py:19-83` | 맞음(경로 10개 모두 `async def` · 42 `accept_source` 는 도우미 `def` → W2-6) |
| A21 | `widgets/header.dart:11-38` `AppHeader` · `shell.dart:216-237` `TabScaffold` | 맞음(클래스 12-38 · `TabScaffold` 가 `AppHeader(title: tabName[tab]!)` · `ConnectionLine`) |
| A22 | `widgets/header.dart:71-` `DetailHeader` | 맞음(71-100) |
| A23 | `main.dart:33-38` `builder` · `ToastLayer` | 맞음 |
| A24 | `qr_show_screen.dart:16-21` · `scan_screen.dart:26-30` · `launchers.dart:82-83 · 86-98 · 103 · 106-` | 두 함수 · `rootNavigator` 맞음 · 부르는 곳 덜함(`reservation_detail_screen.dart:301-304 · 309-311`) · 103 은 변수 정의 → W2-3 |
| A25 | `app_state.dart:165-173` `_onStreamChange` | 맞음(167 · 끊김 → 붙음 = `refreshUnread` · `refreshDisplays`) |
| A26 | `app_state.dart:388-410` `logout` · `:262` | 맞음(`unread` · `displays` 비움 · 262 계정 바뀜 `_setDeviceId(null)`) |
| A27 | `api/api.dart:31` · `:162` · `:174` | 맞음(12초 · `MultipartRequest` · 40초) |
| A28 | `settings_screen.dart:191-202` `_SwitchRow` | 맞음(202 `Switch.adaptive` · `activeTrackColor: Ms.primary`) |
| A29 | `widgets/resv_ui.dart:36` `MiniChip` · `:162` `StatusChip` | 맞음 |
| A30 | `test/boot_device_test.dart:33-39` · `MockClient(` 24곳 · 10파일 | 맞음(모르는 경로 = `{"ok":true,"unread":0,"items":[]}` 200 · 요청 기록 단언) |
| A31 | `shell.dart:89-100` `IndexedStack` · 탭마다 `Navigator` | 줄 맞음(89) · 판정이 §5 보다 좁음 → W2-4 |

함께 다시 본 것: A7 `shell.dart:37` `_showing` · `106-123` `Scaffold`(지금 `Stack` 없음 → 새로 감쌈 · SPEC 「바뀜」 그대로 가능) · A13 `app_state.dart:431-441`(434-436 · 437-441 맞음) · `app_state.dart:420-421` `run()` 401 → `logout`(OQ-934 근거 맞음).

## git status --short (작업 후)

```text
 M orchestration/config/projects/cc-prototype.json
 M para/projects/summer-star/cc-prototype/00-baseline/README.md
 M para/projects/summer-star/cc-prototype/10-decision/README.md
 M para/projects/summer-star/cc-prototype/20-spec/README.md
 M para/projects/summer-star/cc-prototype/20-spec/spec-004-procedure-app.md
 M para/projects/summer-star/cc-prototype/30-work/README.md
 M para/projects/summer-star/cc-prototype/log.md
?? orchestration/roles/cc-prototype/designer/
?? orchestration/work/internal-chat/
?? para/projects/summer-star/cc-prototype/00-baseline/baseline-010-internal-chat.md
?? para/projects/summer-star/cc-prototype/10-decision/decision-009-internal-chat.md
?? para/projects/summer-star/cc-prototype/20-spec/spec-007-internal-chat.md
?? para/projects/summer-star/cc-prototype/30-work/work-011-internal-chat.md
```

이 워커가 만든 것: `orchestration/work/internal-chat/review-doc-r2.md` 1개(`internal-chat/` 는 시작 때부터 untracked). 문서 · 코드 수정 0 · canonical 레포 checkout · pull 0(HEAD `dbf0b53`).
