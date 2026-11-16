# internal-chat 결과 보고 (planner — SPEC-007 · WORK-011)

## 상태: done

## 수행 내용

- **새** `para/projects/summer-star/cc-prototype/20-spec/spec-007-internal-chat.md` — SPEC-007 0.1.0 · draft
  - §1 범위(In · Out = D9-03 · D9-37 「없음」 그대로) · §2 사람 · 권한 · §3 표 4개(`chat_room` · `chat_member` · `chat_message` · `chat_photo`) + `push_log.kind = chat` · `chat_message_id` · §4 방 규칙 · §5 메시지 규칙 · §6 API 14(요청 · 응답 · 오류 · 권한 · 경로 65) · §7 SSE 5 · §8 푸시 · §9 사진 · §10 앱 화면(24장 · 시안과 다른 곳 8) · §11 생명주기 · §12 바뀌는 코드 자리 39 · §13 검증(back · 앱 · 실기기 C1 ~ C12) · §14 법적 검토 주석 4곳 · §15 OQ-901 ~ OQ-931 · 부록 A(DEC) · 부록 B(장면)
- **새** `para/projects/summer-star/cc-prototype/30-work/work-011-internal-chat.md` — WORK-011 · draft · WP-BE1 · BE2 ∥ WP-APP1 ~ APP3 · REVIEW · E2E · **infra 변경 없음**
- **고침(최소)** `20-spec/spec-004-procedure-app.md` 3줄 — frontmatter `links.specs` SPEC-007 · §5-4 「종류는 둘뿐」 뒤 「채팅 푸시도 목록 · 종 배지에 안 들어간다(SPEC-007 §8)」 · §6.8 표에 「채팅 탭 → SPEC-007 §10.1」 행
- `20-spec/README.md` · `30-work/README.md` 행 1씩 · `log.md` 한 줄. DEC-009 는 안 고침

## 검증

### 대조 수치

| 대조 | 결과 |
|---|---|
| DEC-009 D-01 ~ D-37 → SPEC 절(부록 A) | **37 / 37 · 빠짐 0**. 본문에도 `D9-01` ~ `D9-37` 37개 전부 나옴(grep `D9-nn` 하나씩) |
| 시안 장면 → 화면 절(부록 B) | **24 / 24 · 빠짐 0**(폰 20 · 아이패드 4 — 시안 `data-screen-label` 25개 중 1개는 캔버스 머리 「채팅」) · 시안 sha256 앞 12 = `7148eb3fc0e0` 다시 확인 |
| R§4 「바뀔 곳」 → SPEC §12 | 아래 표 **빠짐 0** + 다시 grep 으로 R§4 에 없던 자리 1개 찾음(A12 `AppDelegate.swift:149` · `176` 넘기는 키 목록 — 안 고치면 누른 채팅 푸시의 `roomId` 가 Dart 로 안 간다) |
| OQ | OQ-901 · 902(DEC) + 이 문서 기본값 OQ-903 ~ OQ-931(29) = 표 31행 |
| 실명 · 키 grep | SPEC-007 · WORK-011 에서 시안 가짜 이름 10개 = 0 · 비밀 패턴(`BEGIN PRIVATE` · `sk-` · `eyJ` · 32자 이상 16진 · 전화 · 사내 메일 · `TEAM_ID=` · `password=`) = 0 |
| frontmatter | 두 새 문서 최소셋(type · id · title · status · product · feature · created/updated · tags · links · sources) 채움 · draft |

### R§4 「바뀔 곳」 → SPEC-007 §12

| R§4 | 바뀔 곳 | §12 |
|---|---|---|
| 4.1 | 여럿에게 보내기 = `send_to_account` 루프 또는 새 함수 | B5 · B6 |
| 4.1 | 앱 SSE 파서 허용 이름(`board_stream.dart:157-161`) | A1 |
| 4.1 | 받는 쪽 분기 `_onStreamEvent`(`app_state.dart:91-100`) | A2 |
| 4.1 | 백그라운드 = SSE 닫힘 → 앞으로 오면 REST 로 메우기(`app_state.dart:431-438`) | A13 · §11 |
| 4.1 | 웹 `hooks.ts` 는 `board` 만(안 깨짐) | W1 · §7 |
| 4.2 | `push_log.kind` 에 채팅 값(`db.py:152-163`) | B1 · B2 |
| 4.2 | 알림 목록 종류 둘 고정(`notifications.py:16-23`) | B11(안 바꿈 — D9-30) |
| 4.2 | `apns-expiration: 0` 고정 · `thread-id` 자리 없음(`apns.py:48-51`) | B7 · B8 · B9 |
| 4.2 | 앱 모르는 kind 버림(`push.dart:12` · `25-40`) | A8 · A9 · A10 |
| 4.2 | 앞에 있을 때 늘 배너(`AppDelegate.swift:141-162`) | A11 |
| 4.2 | (발송 길 재사용) `devices_of`(`repo.py:368-373`) · `push.py` 발송 | B4 · B10 |
| 4.3 | 하위 폴더 · 새 표 · 방 멤버 열람 | B13 · B14 · §9 |
| 4.3 | 멀티파트 전역 한도(`photos.py:19-20` · `37-44`) | B12 |
| 4.3 | 사진 고르기 패키지 없음(`pubspec.yaml:30-43`) | A14 |
| 4.3 | 사진 보관함 문구 없음(`Info.plist:69-70`) | A15 |
| 4.3 | multipart · Bearer 예(`api.dart:33-36` · `160-162` → 지금 `162-165`) | A16 |
| 4.3 | 이미지 표시 `Image.memory` 만(`scan_screen.dart:286`) | A17 |
| 4.4 | 새 표 묶음(`db.py:166-190` · `206-218`) | B3 |
| 4.4 | 경로 수 시험(SPEC-004 §7.3) | B17 · §6.4 |
| 4.5 | 계정 목록 API 없음 → 로그인 필요 목록 | B16 · §6.2 #1 |
| 4.5 | 로그인 못 하는 계정 많음 | §2 |
| 4.6 | `AppTab`(`app_state.dart:20`) · 이름 · 아이콘 맵(`shell.dart:14-26`) · `_root`(`67-72`) · Navigator(`35`) · `_TabBar`(`130`) · `_Rail`(`163`) | A3 · A4 · A5 · A6 |
| 4.6 | 띄우기 숨김 규칙이 채팅 배너에도 | A7 |
| (새로 찾음) | `AppDelegate.swift:149` · `176` 넘기는 키 목록 | A12 |
| (새로 찾음 · 확인만) | `main.py:90-91` CORS 이미 `PUT` · `DELETE` · `*` · `main.py:17-28 · 119` router 붙이기 · `shell.dart:240-254` 태블릿 시트 · `ui.dart` 위젯 · `container.py:57-61 · 113` 배선 | B18 · B15 · A18 · A19 · B6 |

### R§4 전수 — 다시 grep 한 명령과 결과 수 (`/Users/kknaks/git/toy_pr2/cc-prototype/procedure` · HEAD `dbf0b53` = research 와 같은 판)

| 수 | 명령 | 읽은 것 |
|---|---|---|
| 2 | `grep -rn "event != 'board'\|event != 'display'" app/lib` | `board_stream.dart:127` · `158` — 허용 이름 자리 하나뿐 |
| 15 | `grep -rn 'PushKind' app/lib` | `push.dart` · `app_state.dart` 두 파일만 |
| 1 | `grep -rn 'apns-expiration\|thread-id\|apns-collapse' back/app` | `apns.py:51` 한 곳 |
| 30 | `grep -rn 'AppTab\.' app/lib` | 칸 수를 늘리는 곳 = `enum` · 맵 2 · `_root` · `values` 루프 3(141 · 182 · 92) — 루프라 칸은 저절로 5 · `settings_screen.dart:89` 는 탭 이름만 |
| 7 | `grep -rn 'spool_max_size\|MAX_BYTES' back/app` | 전역 한도 1(`photos.py:20`) · `MAX_BYTES` 정의 1(`id_photo.py:35`) |
| 1 | `grep -rn 'route_count' back/tests` | `test_order.py:247` **`test_route_count_51`**(SPEC-004 의 49 와 다름 → OQ-920) |
| 2 | `grep -n 'for key in \[' app/ios/Runner/AppDelegate.swift` | **149 · 176 — R§4 에 없던 자리(A12)** |
| 8 | `grep -rn 'KINDS\|NotificationKind' back/app` | 알림 종류 고정 3곳(`notifications.py:16` · `18` · `schemas/actions.py:100`) — 안 바꿈 확인 |
| 4 | `grep -rn 'AppLifecycleState\.' app/lib` | `app_state.dart:434` · `437`(+ 예약 화면 2 = 폴링 앞 확인 · 채팅과 무관) |
| 0 | `grep -rn 'image_picker\|ImagePicker' app/lib app/pubspec.yaml` | 패키지 없음 확인 |
| 3 | `grep -n 'UsageDescription' app/ios/Runner/Info.plist` | 카메라 · 마이크 · 로컬 네트워크 — 사진 보관함 없음 확인 |
| 4 | `grep -rn 'send_to_account\|send_to_device' back/app` | 정의 2 · 배선 2(`container.py:60` · `113`) |
| 2 | `grep -rn 'Image.memory\|Image.network' app/lib` | `scan_screen.dart:286` · `qr_show_screen.dart:145` — `Image.network` 0 |
| 1 | `grep -rn "addEventListener('board'" front/lib` | `hooks.ts:77` — 웹은 `board` 만 |
| 3 | `grep -rn 'include_router\|allow_headers\|allow_methods' back/app/main.py` | 90 · 91 · 119 |
| 2 | `grep -rn 'onForeground' app/lib app/ios/Runner` | `push.dart:70` · `AppDelegate.swift:153` |
| 4 | `grep -rn '_showing' app/lib` | `shell.dart:37` · `55` · `58` · `62` |
| 1 | `grep -rn "kind TEXT NOT NULL DEFAULT .doctor_call." back/app` | `db.py:160` |
| 1 | `grep -rn 'MultipartRequest' app/lib` | `api.dart:162` |
| 3 | `grep -rn 'devices_of' back/app` | `repo.py:368` · `push.py:111` · `130` |

research 리포트의 줄 번호는 같은 HEAD 라 거의 그대로였고, 바뀐 것은 `api.dart` multipart(160-162 → 162-165) 하나다.

### infra

- **변경 없음** — 사진은 기존 `PROC_PHOTO_DIR`(배포 = PVC · `.env.example:57-58` · SPEC-004 §2.3 · WORK-009 WP-INFRA) 하위 `chat/` 폴더를 back 이 만든다. 새 env · Secret · 마운트 0
- 열린 것 1: 채팅 사진이 신분증과 같은 PVC 에 보존 기한 없이 쌓인다 — PVC 크기(WORK-009 「작게」)는 이 워커가 infra 레포를 보지 않아 **확인 못 함**(OQ-931)

## 이 문서가 고른 기본값 (확정 아님 — SPEC-007 §15 에 같이 올림)

| OQ | 기본값 |
|---|---|
| 903 | 멤버 아닌 사람에게 방 · 메시지 · 사진 = 404(있음을 숨김) · 검사 순서 401 → 400 → 404 → 403 → 409 |
| 904 | 비활성 계정 = 푸시 대상 아님 · 그 사람과의 1:1 에 보내기는 막지 않음 |
| 905 | 가짜 판에서도 채팅 됨(KOS 안 닿음) |
| 906 | 그룹 이름 1 ~ 40자 |
| 907 | 지운 메시지 본문을 DB 에서 비움(행은 남김) |
| 908 | 사진 = JPEG 만 · `width` · `height` 는 앱이 보냄 |
| 909 | 채팅은 `event_log` 에 안 남김 |
| 910 | 숨긴 1:1 을 [새 대화]로 다시 열면 다시 보임 |
| 911 | 다시 초대 때 `last_viewed_at` = 초대 시각 |
| 912 | 그룹 만들기 = 다른 사람 2 ~ 19명 · 줄어도 그룹 유지(D9-10 「2 ~ 20」 · DS:S3a · S3b 를 이렇게 읽음) |
| 913 | 시스템 줄 = 추가 · 나가기만 · 푸시 · 안 읽음 없음 · 못 지움 · 그때 이름으로 저장 |
| 914 | 이름 없는 그룹 = 보는 사람 뺀 지금 멤버 가나다 순 |
| 915 | 미리보기 · 푸시 본문 앞 100자 |
| 916 | 열어 둔 방 읽음 1초 묶음 |
| 917 | 방 목록 페이지 없음 |
| 918 | `since` 50 넘으면 `hasMore` → 최근 50 다시 |
| 919 | 사진 응답 `no-store` |
| 920 | (열림) SPEC-004 §7.3 경로 49 ↔ 코드 51 — 이 문서는 51 + 14 = 65 |
| 921 | SSE 이벤트 이름 · 모양 5개(`chat_room_removed` 더함) |
| 922 | 앞에서 받은 채팅 푸시 = iOS 배너 끄고 앱 안 배너(SSE · 푸시 먼저 온 것 · `messageId` 한 번) |
| 923 | 나간 방 푸시 누름 = 토스트 「대화방을 찾을 수 없어요」 |
| 924 | `image_picker` · 품질 85 · 권한 문구 2개 · 거부 토스트 · HEIC → JPEG 실기기 확인 |
| 925 | 앱 사진 메모리 캐시 100장 |
| 926 | 올리고 안 보낸 사진 남김 |
| 927 | 말풍선 사진 가로 240 · 「올해 전」 시각 · 새 메시지 따라 내려가기 |
| 928 | 탭 아이콘 = 말풍선 |
| 929 | 실패 말풍선은 앱을 닫으면 사라짐 |
| 930 | 앱 안 배너 4초 |
| 931 | (열림) PVC 크기 |

## 미결 · 주의점

- **OQ-920 경로 수**: SPEC-004 §7.3 은 49 인데 코드는 `test_route_count_51`(WORK-010 뒤 E2E batch 3 이 사진 삭제 · 유입 채널 2개를 더함). SPEC-007 은 코드 51 기준 65 로 적었다. SPEC-004 를 51 로 고칠지는 코디 몫(이 판 allowed 는 3줄뿐이라 안 고침) — 권장: 다음 SPEC-004 손볼 때 한 줄
- **OQ-922 앞 배너**: D9-28 은 「앱이 앞 배너를 거른다」만 말하고, 시안 S11 은 iOS 배너가 아니라 **앱 안 Banner** 를 그렸다. 그래서 앞에서 받은 채팅 푸시는 iOS 시스템 배너를 끄는 쪽(`willPresent` → `[]`)을 골랐다. 시스템 배너를 그대로 두면 앱 안 배너와 두 번 뜬다
- **A12(새로 찾은 자리)**: `AppDelegate.swift` 가 Dart 로 넘기는 키를 이름으로 고른다 — `roomId` · `messageId` 를 더하지 않으면 채팅 푸시를 눌러도 방이 안 열린다. WORK-011 WP-APP3 대상 파일에 넣었다
- 옛 TestFlight 빌드는 `kind:"chat"` 푸시를 버린다(`push.dart` 모르는 kind) — 배포와 새 빌드를 같이(WORK-011 「주의」)
- 시안 장면 문구의 가짜 이름은 SPEC 에 옮기지 않고 `<보낸 사람>` 꼴로 적었다(public)
- 코드 · 커밋 · push · PR · 서버 · 앱 · docker 실행 0. canonical 레포는 읽기만(checkout · pull 0)

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

이 워커가 만든 것: `20-spec/spec-007-internal-chat.md` · `30-work/work-011-internal-chat.md` · `orchestration/work/internal-chat/spec-report.md`(이 파일 — `internal-chat/` 는 시작 때부터 untracked) · 고친 것: `20-spec/README.md` · `20-spec/spec-004-procedure-app.md`(3줄) · `30-work/README.md` · `log.md`. 그 밖 `M` · `??` 는 시작 때 gitStatus 와 같은 코디 변경이다.
