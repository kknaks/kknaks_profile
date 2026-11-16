# 리뷰 리포트 — internal-chat / doc (2026-10-29 · r1)

검수 대상: `20-spec/spec-007-internal-chat.md` 0.1.0 (아래 `S7:Ln` = 그 파일 줄) · `30-work/work-011-internal-chat.md` (`W11:Ln`) · SPEC-004 바뀐 3줄 (`S4:Ln`) · `spec-report.md`
대조 기준: DEC-009 D-01 ~ D-37 (`D9-nn`) · 확정 시안 r2 (`DS:Sn` · sha `7148eb3fc0e0` 다시 확인) · `design-chat-report.md` · `research-mattermost-report.md` §4 (`R§4`) · SPEC-004 0.4.2 · 코드 `/Users/kknaks/git/toy_pr2/cc-prototype/procedure` HEAD `dbf0b53` (깨끗한 작업 트리 · 읽기만 · 경로는 `procedure/` 기준)

## 판정: FAIL

FAIL 4 · WARN 17. FAIL 은 넷 다 **워커가 추측으로 메워야 하거나, 시험은 초록인데 계약이 깨지는 자리**다. DEC 를 뒤집거나 넓힌 곳은 없고, 좁힌 곳이 1개(D9-34)다.

### 대조 수치

| 대조 | 결과 |
|---|---|
| DEC D-01 ~ D-37 → SPEC 절 | **37 / 37 대응** · 뒤집음 0 · 넓힘 0 · **좁힘 1(D9-34 → F-4)**. D9-19 · D9-20 은 옮긴 글은 맞지만 고른 방식이 같은 초의 메시지를 잃는다(F-2) |
| 시안 장면 → §10 | **24 / 24 대응**. 시안과 어긋나거나 SPEC 에 빠진 요소가 있는 장면 = S1 · S2 · S13a ~ S13d 머리(F-1) · S10a 참여자 순서(W-11) · S13a 대화 칸 머리(F-1) |
| §12 코드 자리 | **39 / 39 를 직접 열어 확인**(B1 ~ B18 · A1 ~ A20 · W1). 지금 모양 맞음 39 · 줄 범위 어긋남 2(A2 · B9 → W-8) · 「앱에 없다」가 틀린 곳 1(A19 → W-7) |
| R§4 · §12 둘 다에 없던 자리 | **10**: 핸들러 `async def`(F-3) · 시각 정밀도(F-2) · 공통 헤더 · `TabScaffold`(F-1) · 직접 여는 QR · 스캔(F-4) · `main.dart` 배너 자리 · `_onStreamChange` · `logout` · `login` 계정 바뀜 · `Api._timeout` · 앱 시험 `MockClient` (W-9) |
| OQ-903 ~ OQ-931 (29) | DEC 와 부딪힘 **0**. 사용자에게 물을 무게 = 아래 「사용자 판단 후보」 |
| public grep | 시안 가짜 이름 10개 = 0 · 비밀 패턴(`BEGIN PRIVATE` · `sk-` · `eyJ` · 32자 이상 16진 · 전화 · 메일 · `TEAM_ID=` · `password=` · 10자 대문자 id) = 0 (걸린 2건은 `CHAT_SCHEMA` · `MIGRATIONS` 오탐) · KOS id 0 · Apple 팀 id 0. `W11:L76` 운영 주소는 레포 49개 파일에 이미 있다 → **PASS** |

---

## FAIL

### F-1 채팅 탭 머리가 지금 앱 헤더와 다르다 — 워커가 둘 중 하나를 골라야 한다 (시안 · 코드)

- **SPEC**: `S7:L374` 「위 = 공통 헤더(가운데 「Céramique」 · 오른쪽 종 + 알림 배지 — S4§6.8) · 그 아래 「채팅」 + [새 대화] 한 줄」 · `S7:L439` 「방 목록 칸 머리 = 「채팅 · [새 대화]」」
- **시안**: DS:S1 · S2 = 가운데 「Céramique」 + 종(10-28 이전 꼴). **DS:S13a ~ d (아이패드) 에는 「Céramique」가 아예 없고**, 레일 오른쪽 **전체 폭 윗줄 하나**가 「채팅 · [새 대화] · 종 + 배지」다. 대화 칸 머리에는 「‹ 채팅」이 없다(「4층 시술실 · 6명 · ⓘ」만)
- **지금 코드**: `app/lib/widgets/header.dart:1-2 · 11-38` `AppHeader` = **[Céramique 왼쪽][지금 탭 이름 가운데][종]**(사용자 2026-10-28) · 폰 · 태블릿 같음. 탭 루트는 모두 `app/lib/screens/shell.dart:216-237` `TabScaffold` 로 이 헤더를 쓴다(`settings_screen.dart:88` · `visits_screen.dart:147` · `board_screen.dart:68` · `reservations_screen.dart:165`). 태블릿 레일도 위에 「Céramique」를 그린다(`shell.dart:177-180`)
- **왜 FAIL**: 워커가 `TabScaffold` 를 쓰면 폰에 「채팅」이 두 번(헤더 가운데 + 그 아래 줄) 나오고 「Céramique」 자리가 시안과 다르다. 안 쓰면 이 탭만 다른 헤더가 된다. 아이패드는 종 자리 · 「Céramique」 유무 · 대화 칸 「‹ 채팅」 유무가 SPEC 에 없다. D9-36 「헤더 아래 「채팅 · [새 대화]」 줄」은 받았지만, 그 위 헤더가 10-28 에 바뀐 것을 SPEC 이 반영하지 않았다
- **고칠 것**: §10.2 · §10.11 에 「폰 = `AppHeader`(지금 꼴 그대로 / 가운데 제목을 비움 / …) + 그 아래 줄」 · 「아이패드 = 시안 S13a 윗줄(`AppHeader` 를 안 씀) / `AppHeader` + 목록 칸 머리」 중 하나를 적고, 대화 칸 머리(뒤로 없음)를 적는다 → **사용자 판단 후보 1**

### F-2 시각이 초 단위라 `since` · 안 읽음 경계에서 같은 초의 메시지를 잃는다 (D9-19 · D9-20 · 조용히 통과)

- **SPEC**: `S7:L107` 「시각은 UTC ISO 문자열」 · `S7:L143` `updated_at` = `since` 기준 · `S7:L228` 안 읽음 = `created_at > last_viewed_at` · `S7:L230` · `S7:L270` `since` = `updated_at > since` · `S7:L471` 「받은 것 중 가장 늦은 updatedAt」
- **코드**: `back/app/domain/clock.py:28-30` `to_db` = `isoformat(timespec="seconds")`(DB 저장) · `clock.py:23-25` `iso()` = 화면용 **KST 오프셋 · 초**
- **깨지는 곳**
  1. 같은 초에 두 메시지(빠른 연속 입력 · 그룹 동시 입력)가 생기고 첫 것만 받은 뒤 SSE 가 끊기면, 다시 연결 때 `since=<그 초>` + `>` 라서 둘째가 **영영 안 온다**(앱은 「다 받았다」로 안다)
  2. 방을 읽은 같은 초에 온 메시지는 `created_at > last_viewed_at` 가 거짓이라 **안 읽음에 안 잡힌다**. 보낸 사람 `last_viewed_at = 그 메시지 시각`(`S7:L224`)도 같은 문제
  3. API 가 내보내는 `createdAt` · `updatedAt` 이 KST 인지 UTC 인지, `since` 쿼리를 어떤 꼴로 받는지(문자열 비교인지 `parse` 뒤 비교인지) SPEC 에 없다 — DB 는 UTC 문자열이라 KST 문자열을 그대로 비교하면 9시간이 어긋난다
- 시험은 가짜 시계를 초 단위로 넘기면 초록이다 → 조용히 통과
- **고칠 것**: 기준을 정한다. 예: `since` 를 `>=` 로 받고 앱이 `id` 로 겹침을 지운다, 또는 채팅 시각만 밀리초로 저장한다, 또는 `since` 대신 `afterId` + 지운 것용 커서를 둔다. 안 읽음도 같은 기준. API 시각 꼴(KST `iso()` 인지)과 `since` 를 파싱하는지도 적는다

### F-3 채팅 API 가 `async def` 가 아니면 푸시가 조용히 빠진다 — §12 에 없는 자리 (D9-25 · D9-26 · 조용히 통과)

- **코드**: `back/app/service/push.py:175-187` `_dispatch` 는 `asyncio.get_running_loop()` 가 없으면 **「푸시 건너뜀(이벤트 루프 없음)」 경고 한 줄만 남기고 끝난다**. `back/app/service/stream.py:59-75` `send_to_account` 는 `asyncio.Queue.put_nowait` 라 스레드풀에서 부르면 스레드에 안전하지 않다. 지금 푸시 · SSE 를 내는 핸들러는 모두 `async def` 다(`api/actions.py:19-83` · `api/reservations.py` · `api/photos.py:34`). 그런데 **`api/notifications.py` 의 핸들러 4개 · `api/photos.py:55` 는 `def`(동기)** — 워커가 따라 할 선례가 섞여 있다
- **SPEC**: `S7:L237` 「router 새 파일 `api/chat.py`」 · `S7:L278` 「SSE · 푸시는 커밋 뒤」 · §12 B14 `S7:L495` — 핸들러가 `async def` 여야 한다는 줄이 없다
- 시험이 `PushService.notify_*` 를 직접 부르면 초록이지만, 경로를 거친 실제 발송은 0 이다. 실기기에서는 「푸시가 안 온다」로만 보인다
- **고칠 것**: §6.1 에 「SSE · 푸시를 내는 경로(3 ~ 8 · 10 · 11 · 12)는 `async def`(`api/actions.py` 와 같게)」 한 줄 · §12 에 `push.py:175-187` · `stream.py:59-75` 자리를 더한다 · §13.1 「푸시 대상」에 「HTTP 경로로 보내서 가짜 APNs 에 닿음」을 단언으로

### F-4 D9-34 를 `_showing` 하나로 좁혔다 — 예약 상세에서 바로 연 QR · 스캔 위에 채팅 배너가 뜬다 (DEC 좁힘)

- **DEC**: D9-34 「띄우기(문진 QR · 스캔) 화면 중에는 탭 · 헤더 · 채팅 배너를 숨긴다」 · SPEC-004 §6.8 「숨김」(D7-45)
- **SPEC**: `S7:L370` · §12 A7 `S7:L506` 「`shell.dart:37` `_showing` 동안」 · `S7:L449`
- **코드**: `_showing` 은 띄우기 대기열을 `_next()` 로 열 때만 참이다(`app/lib/screens/shell.dart:37 · 54-65`). 같은 화면이 **대기열 밖에서도 열린다** — 예약 상세 [이 기기에 QR 보이기] `app/lib/screens/launchers.dart:86-98`(`showQuestionnaireQrHere` → `openQrScreen`) · [여권 스캔] `launchers.dart:103`(`openPassportScan`). 둘 다 `rootNavigator` 전체 화면이다(`qr_show_screen.dart:17-21` · `scan_screen.dart:26-30`). 토스트 층은 `main.dart:33-38` `MaterialApp.builder` 에 있어 **모든 경로 위**에 그려진다 — 배너를 같은 자리에 두면 고객이 보는 QR 위에 직원 대화가 뜬다
- 배너를 어디(셸 안 · 루트 층)에 그리는지도 SPEC 에 없다
- **고칠 것**: 「숨김」을 `_showing` 이 아니라 「QR · 스캔 화면이 열려 있는 동안(어느 길로 열었든)」으로 적고, 배너 자리를 정한다(예: 셸 안에 두면 전체 화면 경로가 저절로 가린다). §12 에 `launchers.dart:86-98 · 103` · `main.dart:33-38` 를 더한다. §13.2 「배너 거름」에 「예약 상세에서 연 QR 중」을 더한다

---

## WARN

| # | 자리 | 무엇 | 근거 |
|---|---|---|---|
| W-1 | `S7:L367` 배지 갱신 | 「`chat_message`(남이 보낸 · 안 보는 방이면 +)」 — **시스템 줄도 남이 「보낸」 것**(`S7:L138` 시스템 줄 `account_id` = 그 일을 한 계정)이라 앱이 + 한다. §5 `S7:L228` 은 시스템 줄을 안 센다 → `kind ≠ system` 을 이 줄에도 | §5 · OQ-913 |
| W-2 | `S7:L263` #2 `unreadRooms` | 어느 방 집합 위의 수인지 없다. 숨긴 1:1 에 숨기기 전 안 읽음이 남아 있으면 셈하나? 숨기기가 `last_viewed_at` 을 올리나? → 「`items` 에 든 방만」 등으로 | D9-13 · D9-20 |
| W-3 | `S7:L271` #10 오류 · `S7:L222` · `S7:L396` | ① 「둘 다 없음」 = `chat_message_empty` 인지 `invalid_request` 인지 ② 「`invalid_request`(… 길이)」 가 무엇의 길이인지(`clientId` 8 ~ 64?) ③ 2001자를 pydantic `max_length` 로 막으면 `main.py:107-111` 이 `invalid_request` 로 바꿔 `chat_message_too_long` 이 안 나온다 → 서비스에서 검사한다고 적기 ④ 「2000자」의 단위 — 서버 `len`(코드 포인트) · Flutter 입력 한도(글자 묶음)가 이모지에서 갈린다 | D9-15 |
| W-4 | `S7:L275` #14 오류 | `PROC_PHOTO_DIR` 이 빈 서버에서 열기 = ? 지금 선례는 409 `photo_disabled`(`service/id_photo.py:116-118`) — 표에는 404 만 있다. 행은 있는데 파일이 없을 때 코드도 | D9-23 |
| W-5 | `S7:L153-155` · `S7:L275` 보안 | 올렸지만 아직 안 보낸 사진(`message_id` null)도 「그 방 지금 멤버」면 열 수 있고 id 가 순번이다 → 붙기 전에는 올린 사람만 · 붙은 뒤 방 멤버 | D9-23 · OQ-926 |
| W-6 | 근거 · 기본값 표시 없는 규칙 | `S7:L403` 「15초」(앱 `Api._timeout` = 12초 `app/lib/api/api.dart:31` 과도 다름) · `S7:L403` 「4xx 면 토스트 + 말풍선 지움」 · `S7:L225` 「이미 지운 것 = 200(멱등)」 · `S7:L262` 「이름 순」(DS:S3a 목록은 이름 순이 아니다) · `S7:L142` `clientId` 8 ~ 64자. `S7:L472-474` 「기본값」 3줄은 OQ 번호가 없다(§15 에 없음) | 브리프 §4-3 |
| W-7 | `S7:L355` · §12 A19 | 「Toggle · Chip … 앱에 같은 위젯이 없다」 — 설정 알림 칸이 이미 `Switch.adaptive`(`app/lib/screens/settings_screen.dart:191-202` `_SwitchRow`)를 쓰고, 칩은 `widgets/resv_ui.dart:36` `MiniChip` · `:162` `StatusChip` 이 있다. 새로 만들면 같은 앱에 켬/끔이 두 모양이 된다 → 재사용 또는 안 쓰는 이유 | DS r2 §2 · 코드 |
| W-8 | §12 줄 범위 | A2 `_onStreamEvent` 는 `app_state.dart:92-104`(91-100 아님) · B9 는 `_send`(`service/push.py:254-259` — 257 `client.send(token, payload)`)까지 `expiration` 을 넘겨야 한다(224-252 밖) | 코드 |
| W-9 | §12 · R§4 둘 다 빠진 자리(F 밖) | ① `app_state.dart:165-173` `_onStreamChange` — SSE 가 다시 붙을 때 메우는 지금 훅(§11 `S7:L472` 「첫 `board`」 대신 이것) ② `app_state.dart:388-410` `logout` · `:262` 계정 바뀜 — §11 `S7:L473-474` 비우기 자리 ③ `main.dart:33-38` 배너 층 ④ `api.dart:31` 시간 한도 ⑤ 앞으로 올 때 · 시작 때 채팅 읽기 실패는 조용히(`refreshUnread` `app_state.dart:176-185` 와 같게) — `test/boot_device_test.dart:33-39` 등 `MockClient` 24곳이 모르는 경로를 받는다 | §11 · 코드 |
| W-10 | `S7:L229` · `S7:L448-449` 「보고 있는 방」 | 탭바가 대화 화면에 남아(D9-36) 대화를 연 채 다른 탭으로 갈 수 있다(`shell.dart:89-100` `IndexedStack` · 스택 유지). 그때도 「열어 둔 방」이라 읽음 처리 · 배너 거름을 하나? 정의 없음 → 「채팅 탭이 지금 탭이고 그 대화가 맨 위일 때만」 등 | D9-28 · D9-36 → 사용자 판단 후보 4 |
| W-11 | `S7:L422` · `S7:L244` | 참여자 행 · `Room.members` 순서가 없다. DS:S10a 는 「나」가 맨 위, 나머지는 가나다 순이 아니다 | DS:S10a |
| W-12 | `S7:L332-333` · OQ-924 | `image_picker` iOS 는 PNG 원본(스크린샷)에 `imageQuality` 를 적용하지 않고 PNG 로 돌려준다고 알려져 있다(패키지 문서 — 실기기 확인 필요). 그러면 `FF D8 FF` 검사(`S7:L333`)에 걸려 400 이다 → 앱이 늘 JPEG 로 다시 인코딩한다고 적거나, C5 에 「앨범 스크린샷 1장」을 더한다 | D9-22 |
| W-13 | `S7:L576` · §6.1 로그 | 서버 로그에 메시지 본문 · 이름 · 푸시 제목을 남기지 않는다는 줄이 없다(지금 푸시 실패 로그 꼴 `service/push.py:236`). OQ-902(고객 정보)라 한 줄 필요 | OQ-902 |
| W-14 | `W11:L70` WP-BE1 완료 조건 | 「§13.1 상대 목록 ~ 페이지」 안에 BE2 기능이 섞였다 — 「권한」의 사진 올리기 · 열기 404, 「중복 방지」의 SSE 1 · 푸시 1, 「삭제」의 사진 파일 · 지운 사진 열기 404. BE1 만으로는 못 통과한다 → 줄 단위로 나눈다 | WORK |
| W-15 | `W11:L72-74` 대상 파일 | WP-APP2 사진 진행률 올리기에 `lib/api/api.dart` 가 없다(APP1 에만). `http.MultipartRequest`(`api.dart:162`)는 올린 바이트를 알려 주지 않아 다른 요청 꼴이 필요하다(A16 은 이것을 「예」로만 듦). WP-APP3 에 `lib/main.dart`(배너 층) · `lib/screens/launchers.dart`(F-4) · `lib/widgets/header.dart`(F-1) 가 없다 | WORK · 코드 |
| W-16 | `W11:L45` · OQ-931 | 「infra 변경 없음」인데 PVC 크기(OQ-931)는 열려 있고, WP-E2E 에 그것을 닫는 단계가 없다 → WP-E2E 첫 줄에 「OQ-931 확인 · 바꾸면 infra PR」 | WORK |
| W-17 | `S4:L690` · `S4:L697` (SPEC-004 바뀐 3줄 검수) | 새 행 「채팅 탭 … 5번째 칸으로 더한다」를 넣었는데 같은 표의 「아래 탭바 **4칸** · 메뉴 **4개**」(L690) · 「모든 역할 같은 **4탭**」(L697)이 그대로라 한 표 안에서 어긋난다 → 두 줄에 「(채팅 더해 5 — SPEC-007)」 | D9-33 |

---

## 조용히 통과하는 자리 (시험은 초록 · 계약은 깨짐)

1. **동기 핸들러 → 푸시 0**(F-3) — 서비스 함수를 직접 부르는 시험만 있으면 초록
2. **같은 초 메시지 유실 · 안 읽음 누락**(F-2) — 가짜 시계를 초 단위로 넘기는 시험은 초록
3. **`_showing` 만 보는 배너 거름**(F-4) — 대기열로 연 띄우기 시험은 초록, 예약 상세에서 바로 연 QR 은 시험 밖
4. **2001자 → `invalid_request`**(W-3) — 「400 이면 됨」 단언이면 초록
5. **시스템 줄이 탭 배지를 올림**(W-1) — 앱 시험에 시스템 줄 경우가 없으면 초록
6. **PNG 스크린샷 400**(W-12) — 시뮬레이터 · JPEG 사진으로만 보면 초록
7. **경로 수 65** — 지금 시험은 수와 집합을 같이 단언(`back/tests/test_order.py:247-256`)하므로 이건 안전하다(확인만)

## 사용자가 실물에서 만날 자리

1. 채팅 탭 헤더에 「채팅」이 두 번이거나, 이 탭만 헤더 모양이 다름(F-1)
2. 아이패드 채팅 탭에서 종이 어디 있는지 · 「Céramique」가 있는지(F-1)
3. 빠르게 주고받은 메시지 하나가 앱을 다시 열어도 안 보임 · 안 읽음 배지가 하나 덜 셈(F-2)
4. 실기기에서 채팅 푸시가 아예 안 옴(F-3)
5. 고객에게 보여 주는 문진 QR 위에 직원 대화 배너가 뜸(F-4)
6. 앱이 앞에 있을 때 다른 방 메시지는 **소리 없이** 위 배너만(OQ-922)
7. 대화를 연 채 「예약 현황」 탭을 보는 동안 그 방 메시지가 배너 없이 읽음 처리됨(W-10)
8. 스크린샷을 보내면 「JPEG 아님」 오류(W-12)
9. 비행기 모드에서 쓴 메시지가 앱을 닫으면 사라짐(OQ-929)
10. 이모지가 섞인 긴 글이 입력칸에서는 들어가는데 보내면 400(W-3 ④)

## 참고 (기존 부채 — 이번 판에서 고칠 것 아님)

- SPEC-004 §6.8 `S4:L691` 「가운데 「Céramique」」는 10-28 헤더 변경(`header.dart:1` 「한 줄 [Céramique][메뉴명][알림]」)이 반영되지 않은 글이다 — F-1 의 뿌리
- SPEC-004 §7.3 경로 수 49 ↔ 코드 51(`test_route_count_51`) — OQ-920 그대로
- `api/notifications.py` · `api/photos.py:55` 의 동기 핸들러는 SSE · 푸시를 내지 않아 지금은 문제없다(F-3 의 선례로만 위험)

---

## 사용자 판단 후보 (제품 동작이 눈에 보이게 갈리는 것)

| # | 무엇 | 문서 기본값 · 지금 상태 | 왜 사용자에게 |
|---|---|---|---|
| 1 | **채팅 탭 머리 모양**(F-1) — 폰: 지금 헤더(가운데 탭 이름) 위에 「채팅 · [새 대화]」 줄을 또 둘지, 이 탭만 시안처럼 가운데 「Céramique」로 둘지, 헤더 가운데 「채팅」 + 오른쪽에 [새 대화]로 합칠지 · 아이패드: 시안 S13a 의 전체 폭 윗줄(「Céramique」 없음 · 종 여기)을 따를지 | SPEC 에 없음(시안은 10-28 이전 헤더 꼴) | 10-28 사용자가 바꾼 헤더와 10-29 확정 시안이 서로 다르다. 코디 · 워커가 고를 수 없다 |
| 2 | **앞에서 받은 채팅 = 소리 없는 앱 안 배너**(OQ-922) | iOS 배너 · 소리 끔(`completionHandler([])`) · 앱 안 Banner 만 | 원장 · 상담사 호출은 앞에서도 배너 + 소리(SPEC-004 §5-1.3). 채팅만 조용해진다 |
| 3 | **실패 말풍선이 앱을 닫으면 사라짐**(OQ-929) | 기기에 저장 안 함 | 쓴 글이 말없이 없어진다 |
| 4 | **「보고 있는 방」 = 채팅 탭이 지금 탭일 때만?**(W-10) | 정의 없음 | 탭바 유지(D9-36) 때문에 생긴 갈림. 읽음 · 배너가 달라진다 |
| 5 | 비활성 상대와의 1:1 에 계속 보낼 수 있음(OQ-904) | 막지 않음 · 받는 사람 없음 | 보낸 글이 아무에게도 안 간다 |
| 6 | 다시 초대되면 빠진 동안의 메시지는 안 읽음 0(OQ-911) | 초대 시각으로 읽음 | 그동안 온 글을 못 알아챌 수 있다 |
| 7 | 다 나가고 혼자 남은 그룹도 그대로 · 보낼 수 있음(OQ-912) | 그룹 유지 | 받는 사람 없는 방이 목록에 남는다 |

코디 몫(사용자 아님): OQ-920(경로 수) · OQ-931(PVC 크기) · OQ-905 · 925 · 926 · 930.

---

## 확인한 코드 자리 (§12 39개 · 전부)

| # | 결과 | # | 결과 | # | 결과 |
|---|---|---|---|---|---|
| B1 `db.py:152-163` · `:160` | 맞음 | B14 새 파일 | 없음 확인(`grep chat` 0) | A8 `push.dart:12` · `23-41` | 맞음 |
| B2 `db.py:193-202` | 맞음 | B15 `main.py:17-28` · `117-119` | 맞음 | A9 `app_state.dart:189-208` | 맞음 |
| B3 `db.py:166-190` · `210-213` | 맞음 · `_rebuild_push_log` `237-254` 와 순서 문제 없음(ADD COLUMN 뒤 재생성은 옛 열만 복사) | B16 `deps.py:17-24` | 맞음 | A10 `push.dart:70-73` | 맞음(지금은 `onTap` 으로 보냄 — 채팅은 분기 필요) |
| B4 `repo.py:368-373` | 맞음(`live_devices` 거름 · 비활성 거름은 없음 → 서비스가) | B17 `test_order.py:247` | 맞음(수 + 집합 단언) | A11 `AppDelegate.swift:141-162` | 맞음 |
| B5 `stream.py:59-61` | 맞음 | B18 `main.py:87-92` | 맞음(PUT · DELETE · `*`) | A12 `AppDelegate.swift:149` · `176` | 맞음 |
| B6 `container.py:57-61` · `113` | 맞음 | A1 `board_stream.dart:157-161` · `127` | 맞음 | A13 `app_state.dart:430-443` | 맞음 |
| B7 `apns.py:48-51` | 맞음(가짜 APNs 는 `httpx.MockTransport` 라 시그니처 바뀌어도 시험 픽스처 안 깨짐 · `test_push.py:155` 가 `"0"` 단언 = 회귀 시험 자리) | A2 `app_state.dart` | **92-104**(W-8) | A14 `pubspec.yaml:30-43` | 맞음(사진 패키지 0) |
| B8 `push.py:33-48` | 맞음 | A3 `app_state.dart:20` | 맞음 | A15 `Info.plist:69-70` | 맞음 |
| B9 `push.py:151-159` · `224-252` | **+254-259**(W-8) | A4 `shell.dart:14-26` | 맞음 | A16 `api.dart:33-36` · `162` | 맞음(진행률 없음 → W-15) |
| B10 새 함수 | — | A5 `shell.dart:67-72` | 맞음 | A17 `scan_screen.dart:286` | 맞음(`Image.network` 0) |
| B11 `notifications.py:16-23` · `schemas/actions.py:100` | 맞음 | A6 `shell.dart:130-` · `163-` · `141` · `182` | 맞음 | A18 `shell.dart:240-261` | 맞음 |
| B12 `photos.py:19-20` · `37-44` | 맞음 | A7 `shell.dart:37` | 맞음(범위가 좁음 → F-4) | A19 `ui.dart:15` · `98` · `156` | 위치 맞음 · 「없다」는 틀림(W-7) |
| B13 `id_photo.py:35` · `49-63` | 맞음 | A20 새 폴더 | — | W1 `front/lib/hooks.ts:77` | 맞음(`addEventListener('board')` 하나 · `onmessage` 없음 → 웹 안 깨짐 근거 맞음) |

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

이 워커가 만든 것: `orchestration/work/internal-chat/review-doc-r1.md` 1개(`internal-chat/` 는 시작 때부터 untracked). 문서 · 코드 수정 0 · canonical 레포 checkout · pull 0(HEAD `dbf0b53` · 작업 트리 깨끗함 확인).
