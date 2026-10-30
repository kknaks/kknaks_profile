# internal-chat SPEC-007 · WORK-011 r2 결과 보고 (리뷰 r1 처분)

## 상태: done

## 수행 내용

- `para/projects/summer-star/cc-prototype/20-spec/spec-007-internal-chat.md` **0.1.0 → 0.2.0** · draft · 머리에 「변경」 표(49행) · 바뀐 줄 끝 `(r2)` 124곳 · 694 → 760줄
- `para/projects/summer-star/cc-prototype/30-work/work-011-internal-chat.md` — SPEC 0.2.0 · 계약 고정점 3행(시각 · 셈 기준 · 핸들러) · BE1 / BE2 완료 조건 줄 단위 · 대상 파일 · WP-E2E 첫 단계 OQ-931
- `20-spec/spec-004-procedure-app.md` — §6.8 「4칸」(690) · 「4탭」(697) 두 줄에만 「(채팅 더해 5 — SPEC-007)」. 앞 판 3줄 말고 다른 곳은 안 고침
- `20-spec/README.md` SPEC-007 판 0.2.0 · `log.md` r2 한 줄(27)
- DEC-009 · 코드 레포 · 다른 파일 수정 0 · 커밋 · push · PR 0 · lint 스크립트(`scripts/lint-pipeline.py`)는 이 워크트리에 없어 못 돌림(리뉴얼 레포에 `scripts/` 없음)

### 처분 대조표 — FAIL 4 · WARN 17 (`S7:n` = SPEC-007 0.2.0 줄 · `W11:n` = WORK-011 줄)

| 지적 | 처분 | 고친 곳 |
|---|---|---|
| **F-1** 탭 머리 | D9-38: 폰 · 아이패드 = `TabScaffold` → `AppHeader`[Céramique][채팅][종] · 아래 제목 없는 [새 대화](오른쪽) · 아이패드 = 방 목록 칸 위 [새 대화] · 폰 대화 = `DetailHeader` 「‹ 채팅」(Céramique · 종 없음) · 아이패드 대화 칸 = 뒤로 없음 · 시안과 다른 곳 #9 | S7:43 · 377(§10.0) · 395(§10.2) · 412(§10.4) · 461-463(§10.11) · 491(§10.13 #9) · 556-557(§12 A21 · A22) · 601(§13.2) · 610(C1) |
| **F-2** 시각 | 채팅 표만 **UTC 밀리초**(새 `to_db_ms` — `to_db` · 기존 표 그대로) · API = **KST 밀리초**(새 `iso_ms` — `iso()` 는 KST · 초라 안 씀) · `since` = `clock.parse` 뒤 `to_db_ms` 로 바꿔 비교(문자열 그대로 금지 · `%2B`) · **`updated_at >= since`** · 앱이 `id` 로 겹침 지움 · 안 읽음 = **`last_read_message_id`**(id 기준) · 읽음 `{messageId}` · 늘기만 | S7:118(§3 머리) · 141(§3.2) · 147 · 151(§3.3) · 238 · 244 · 245(§5) · 254(§6.1) · 288 · 291(§6.2) · 529(B19) · 588(§13.1 「시각 경계」 — 같은 밀리초 · 같은 초) |
| **F-3** async | §6.1 「SSE · 푸시 · 사진 경로 `async def`」 + 이유 두 가지 · `notifications.py` · `photos.py:55` 는 선례 아님 · §12 B20(`push.py:175-187`) · B21(`stream.py:59-75`) · B25(`actions.py:19-83`) · §13.1 「HTTP 경로 → 가짜 APNs」 단언 | S7:253 · 296 · 530 · 531 · 535 · 591 · W11:59 · 73 · 77(REVIEW grep) · 98(주의) |
| **F-4** 숨김 | D9-44: 「QR · 스캔 화면이 떠 있는 동안 — 어느 길로 열었든」 · `_showing` 으로 판정 안 함 · **배너 층 = 셸 안**(`main.dart:33-38` 토스트 층 아님 — QR 이 `rootNavigator` 라 셸을 덮음) + `showQrScreen` · `showPassportScan` 이 열린 수를 올리고 내림 · 가려진 동안 온 배너는 버림 · §12 A7 · A23 · A24(`launchers.dart:86-98 · 103`) · §13.2 세 길 | S7:391(§10.1) · 476(§10.12) · 492(§10.13 #10) · 542 · 558 · 559 · 601 · 610(C1) · W11:76 |
| W-1 | 배지 갱신에 `kind ≠ system` · `deletedAt` · 보고 있는 방 | S7:388 · 601 |
| W-2 | `unreadRooms` = 응답 `items` 방만 · 숨기기는 읽음을 안 바꿈 | S7:281 · 588 위 「안 읽음」 |
| W-3 | ① 둘 다 없음 = `chat_message_empty` · 둘 다 = `invalid_request` ② `clientId` 8 ~ 64 ③ 길이는 서비스 검사(`main.py:107-111`) ④ 코드 포인트(`len` · `runes.length`) | S7:234-235 · 289 · 418(입력줄) · 532(B22) · §13.1 「메시지」 |
| W-4 | 폴더 없음 409 `photo_disabled` · 파일 없음 404 (`id_photo.py:116-121` 선례) | S7:292 · 533(B23) |
| W-5 | 붙기 전 = 올린 사람만 · 붙은 뒤 = 방 멤버 | S7:164-165 · 292 · 354 · §13.1 「사진」 |
| W-6 | 15초 → `Api._timeout` 12초 · 사진 40초(`api.dart:31 · 174`) · 4xx = OQ-934 · 멱등 = OQ-935 · 이름 순 = OQ-936 · `clientId` = OQ-937 · §11 「기본값」 3줄 → 코드 자리(`_onStreamChange` · `logout` · `login:262`) 근거로 바꿈 | S7:355 · 425-426 · 241(삭제) · 107 · 151 · 500-503 |
| W-7 | Toggle = 기존 `Switch.adaptive`(`settings_screen.dart:191-202`) · Chip = `StatusChip` + ✕ · 「이미 참여 중」 = `MiniChip` · 새로 만드는 목록에서 뺌 | S7:374-376 · 445 · 484(§10.13 #2) · 554(A19) · 563-564(A28 · A29) |
| W-8 | A2 → `92-104` · B9 → `254-259` `_send` 까지 | S7:537 · 519 |
| W-9 | ① `_onStreamChange` ② `logout` · `login:262` ③ `main.dart` 배너 층 ④ `api.dart:31` ⑤ 실패 조용히 + `MockClient(` 24곳 기대 고침 | S7:500-503 · 558 · 560-562 · 565 |
| W-10 | D9-40 「보고 있는 방」 정의 | S7:243-244 · 474 · 566(A31) · 613(C4) |
| W-11 | 참여자 = 「나」 맨 위 + 가나다 · `Room.members` 차례 | S7:262 · 445 · OQ-936 |
| W-12 | 앱이 늘 JPEG 로 다시 인코딩 · C5 「앨범 스크린샷(PNG) 1장」 | S7:350 · 359 · 422 · 614 · W11:75 |
| W-13 | 로그에 본문 · 이름 · 제목 없음 · id 만 · B24 · §13.1 「로그」 | S7:255 · 534 · 592 |
| W-14 | BE1 완료 조건을 줄 단위로 · SSE · 푸시 · 사진 줄은 BE2 · §13.1 에 「중복 방지 — SSE · 푸시」 · 「삭제 — 사진」 줄을 따로 | W11:72 · 73 · S7:§13.1 |
| W-15 | APP1 + `resv_ui.dart` · `settings_screen.dart` · 기존 시험 · APP2 + `api.dart` · `header.dart` · APP3 + `main.dart`(확인만) · `launchers.dart`(확인만) · `qr_show_screen.dart` · `scan_screen.dart` · `header.dart` | W11:74 · 75 · 76 |
| W-16 | WP-E2E 첫 단계 「OQ-931 확인 · 바꾸면 infra PR」 | W11:78 · S7:OQ-931 |
| W-17 | SPEC-004 §6.8 두 줄 「(채팅 더해 5 — SPEC-007)」 | S4:690 · 697 |

처분 못 한 것 **0**.

### 사용자 판단 후보 · 코디 몫

| 후보 | 처분 | SPEC |
|---|---|---|
| 1 탭 머리 | D9-38 | F-1 위 |
| 2 앞 채팅 소리 없음 | D9-39 · OQ-922 **닫힘** | §8 · §10.12 · C4 |
| 3 실패 말풍선 | D9-41 · OQ-929 **닫힘** | §10.5 · §11 |
| 4 보고 있는 방 | D9-40 | §5 |
| 5 비활성 1:1 | D9-42 · OQ-904 **닫힘(뒤집음)** — 앱 입력 막음 + 안내 · 서버도 409(OQ-939 기본값) | §2 · §5 · §6.2 #10 · §10.4 |
| 6 · 7 다시 초대 · 혼자 남은 그룹 | D9-43 · OQ-911 · OQ-912 **닫힘** | §4.2 |
| OQ-920 | SPEC-007 = 코드 51 기준 그대로 · SPEC-004 §7.3 안 고침(열린 채로) | OQ-920 |
| OQ-931 | WORK-011 WP-E2E 첫 줄 | W11:78 |

## 검증

- **DEC D-01 ~ D-44 → SPEC** = 44 / 44(부록 A 44행 · D9-38 ~ D9-44 는 본문에 각 3 ~ 11곳). 뒤집음 0 · 넓힘 0 · 좁힘 0(D9-34 는 D9-44 대로 풀어 씀)
- **시안 24장 → §10** = 24 / 24 그대로(부록 B 안 바뀜). 시안과 다른 곳 #9(헤더 · D9-38) · #10(배너 층 · D9-44)을 더함
- **리뷰 FAIL 4 · WARN 17** → 위 대조표 21 / 21 · 못 한 것 0
- **r2 에 더한 코드 자리 전수 grep**(canonical `dbf0b53` · 작업 트리 깨끗함 · 읽기만): 18개 명령 결과 `scratchpad/grep-r2.txt` 와 같음 —
  `clock.py` `def iso|to_db|parse` 23 · 28 · 33 / `push.py` `get_running_loop` 181 · 「이벤트 루프 없음」 183 / `stream.py` `put_nowait` 56 · 74 / 동기 핸들러 `notifications.py` 4 · `photos.py` 2(그중 핸들러 1 — `:55`) / `actions.py` `async def` 10 / `rootNavigator: true` push = `qr_show_screen.dart:18` · `scan_screen.dart:27` / QR · 스캔 여는 호출 8 / `ToastLayer(` `main.dart:38` / `_onStreamChange` 88 · 167 / `Switch.adaptive` 앱 전체 1 / `MiniChip` 36 · `StatusChip` 162 / `MockClient(` 24곳 · 10파일 / `_timeout` 31 · 40초 174 / `invalid_request` `main.py:111` / `photo_disabled` `id_photo.py:118` · 190 / `TabScaffold(` 5 / `DetailHeader` 71 / `client.send(token, payload)` `push.py:257`. §12 는 B1 ~ B25 · A1 ~ A31 · W1 = 57행(r1 39 + r2 18)
- **public grep**: 시안 가짜 이름 10개(SPEC-007 · WORK-011 · SPEC-004) = 0 · 비밀 패턴(`BEGIN PRIVATE` · `sk-` · `eyJ` · 32자 이상 16진 · 전화 · 메일 · `TEAM_ID=` · `password=`) = 0 · KOS id · Apple 팀 id 0
- 표 칸 수 검사: 어긋남 0(걸린 3줄은 r1 부터 있던 `\|` 이스케이프)
- OQ 표 39행 · 번호 겹침 0
- frontmatter: SPEC-007 `version: 0.2.0` · `sources` 에 D-01 ~ D-44 · review-doc-r1 · WORK-011 변경 없음(필드 그대로)

## 이 판이 고른 기본값 (새 OQ — 확정 아님)

| OQ | 무엇 | 왜 이렇게 |
|---|---|---|
| OQ-932 | 안 읽음 = 메시지 id(`last_read_message_id`) · 읽음 요청 `{messageId}` · 늘기만 | 브리프가 「검토」로 연 자리. 밀리초로 바꿔도 같은 밀리초 경계는 남는다 — id 는 단조(행을 지우지 않음 · `INTEGER PRIMARY KEY`)라 경계가 아예 없다. D9-20 「마지막으로 본 시각」을 「본 때의 마지막 메시지」로 읽었고 `last_viewed_at` 은 밀리초로 남겼다. **DEC 의 말과 셈 방식이 달라 코디 확인 필요** |
| OQ-933 | 배너 층 = 셸 안 + QR · 스캔 열린 수 · 가려진 동안 온 배너는 버림 · 폰 알림 목록 · 사진 크게 보기 위에서도 안 보임 | 셸 안이면 `rootNavigator` 전체 화면이 길과 상관없이 덮는다. 열린 수는 시험 · 「닫은 뒤 몰려 뜸」을 막는 용도. 부작용(알림 목록 · 사진 위 배너 없음)은 D9-34 보다 넓게 가린다 — 코디 확인 |
| OQ-934 | 보내기 4xx(401 빼고) = 토스트 + 말풍선 지움 · 401 = 로그아웃 | 다시 보내도 같은 답 · `run()` 선례 |
| OQ-935 | 이미 지운 메시지 삭제 = 200 | 두 기기 · 다시 누르기 |
| OQ-936 | 상대 목록 가나다 · 참여자 「나」 맨 위 + 가나다 | 시안 S3a · S10a 차례는 규칙이 없다(가나다도 id 도 아님 — 확인함) |
| OQ-937 | `clientId` 8 ~ 64 · 앱 UUID v4 | r1 값에 근거 표시만 |
| OQ-938 | 배너 원천 = SSE · 앞 푸시 중 먼저 온 것 · `messageId` 한 번 | OQ-922 가 D9-39 로 닫히며 남은 부분을 나눔 |
| OQ-939 | 비활성 1:1 보내기를 서버도 409 `chat_peer_inactive` | D9-42 는 앱 입력을 막는다 — 같은 이유를 서버에도. 새 오류 코드 1(§6.3 14개) |
| OQ-924(넓힘) | 늘 JPEG 다시 인코딩 = `flutter_image_compress` | iOS 네이티브 · HEIC · PNG 둘 다. 패키지는 mobile 이 근거 있으면 바꿀 수 있게 기본값 |

## 미결 · 주의점

1. **OQ-932(id 기준 안 읽음)** — D9-20 문구와 셈 방식이 다르다. 권장: 이대로(같은 밀리초도 안 잃음). 아니면 `last_viewed_at`(밀리초) `>=` 셈으로 되돌리고 같은 밀리초 겹침은 감수
2. **OQ-933 부작용** — 셸 안 배너는 폰 알림 목록 · 사진 크게 보기 위에서도 안 보인다. 권장: 이대로(그 화면은 직원이 잠깐 보는 곳 · 탭 배지는 갱신). 아니면 배너 층을 루트에 두고 열린 수로만 거름(QR 위에 뜰 위험이 셈 실수 하나에 달림)
3. **새 오류 코드 `chat_peer_inactive`(409)** — WORK 계약 고정점 「오류 코드 14개」가 바뀌었다
4. 읽음 요청에 `{messageId}` 가 생겼다(r1 은 본문 없음) — 계약 고정점 「셈 기준」 행에 적음
5. `scripts/lint-pipeline.py` 가 이 워크트리에 없어 lint 를 못 돌렸다(역할 문서 `skills.md` 는 있다고 적음 — 리뉴얼 뒤 낡은 줄로 보임)

## git status --short

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

이 판이 고친 것: SPEC-007 · WORK-011(둘 다 untracked) · SPEC-004 두 줄 · `20-spec/README.md` 한 칸 · `log.md` 한 줄 · 이 리포트. 시작 때와 같은 목록(새 경로 0).
