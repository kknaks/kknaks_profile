# 리뷰 리포트 — internal-chat / doc r3 (2026-10-29)

대상: SPEC-007 0.3.0(`para/projects/summer-star/cc-prototype/20-spec/spec-007-internal-chat.md`) · WORK-011 r3(`30-work/work-011-internal-chat.md`) · `spec-r3-report.md`
대조 원천: DEC-009 D-45 ~ D-57 · `sim-feedback.md` F1 ~ F4 · 1판 코드 `/Users/kknaks/orca/workspaces/cc-prototype/internal-chat` `0f0d969`(`git log -1` 확인 · 읽기만)
코디 기본값 OQ-940 ~ OQ-956 은 받은 값으로 두고 FAIL 로 잡지 않았다(OQ-956 포함).

## 판정: FAIL (2 · 둘 다 문장 한두 줄 고치면 닫힘)

대조 수치
- DEC D-45 ~ D-57 → SPEC: **13 / 13** 옮겨짐(부록 A 행 · 본문 자리 확인). 뒤집힌 D-03 · D-15 · D-17 · D-22 · D-24 는 부록 A 「뒤집힘」 · 본문 취소선 · 「r3 에서 넣음」으로 표시됨
- F1 ~ F4 → SPEC: **4 / 4**(부록 C)
- 옛 문장 남음: 「영상 없음」 0 · 「1장」 0(취소선 · 「사진 1장」 = 메시지 하나 규칙 뜻으로만 남음 §5:252) · 「수정 없음」 0 · **「남의 메시지 메뉴 없음」 1(FAIL-1)** · 수 낡음 5(WARN-1)
- §12.2 r3 자리 **41 / 41** 을 `0f0d969` 에서 직접 열어 확인: 줄 · 지금 모양 맞음 39 · 이름 틀림 1(WARN-2 `showChatPhoto`) · r3 표시 줄인데 dbf0b53 줄 번호 1(WARN-2 `api.dart:31`) · 빠진 자리 1(WARN-3 보내는 중 말풍선)
- 새 계약(PATCH · 동영상 올리기 · Range · 썸네일 · SSE `chat_message_edited` · 오류 코드 20 · 경로 69): 필드 · 타입 · 한도 · 권한 · 시험이 다 있음 — 빈칸 0(경계 해석 WARN 2)
- Starlette 1.9.0(`back/uv.lock:555-556`) · `FileResponse` Range 처리(`.venv/.../starlette/responses.py:379-382` 416 · `:439-473` 206) 확인 — §6.2 #17 · §9.2 의 근거가 맞다

## FAIL

### FAIL-1 · §13.3 C8 에 뒤집힌 옛 동작이 완료 조건으로 남음
- 자리: `spec-007-internal-chat.md:784` C8 「… · **남의 메시지 길게 = 메뉴 없음** · …」
- 근거: D9-54(남의 텍스트 = 복사 · 선택 복사 · 공유 · 남의 사진 · 동영상 = 공유) · §10.7 표(`:523-527`) · C16(`:792` 「남의 글 = 복사 · 선택 복사 · 공유」). `:796` 은 「C8 의 [삭제] 하나 → 5메뉴의 [삭제]」만 고치고 이 구절은 그대로 뒀다
- 왜 FAIL: 실기기 E2E 에서 맞게 구현된 앱이 C8 을 못 넘고(메뉴가 뜬다) C16 과 서로 부딪힌다. 브리프 볼 것 1 「옛 문장이 남아 있으면 FAIL」에 해당
- 고칠 것: C8 의 그 구절을 「남의 메시지 길게 = [삭제] 없음(복사 · 선택 복사 · 공유만 — C16)」으로

### FAIL-2 · 비활성 상대 1:1 에서 [수정] 이 어떻게 보이는지 두 줄이 부딪힘
- 자리: `:489` §10.4 「비활성 상대 1:1: **입력줄 대신** 회색 안내 한 줄 … 지우기는 됨」 ↔ `:534` §10.7 「수정 → 입력창이 수정 모드」 · `:523` 표 「내 텍스트 = 수정 ○」(예외 없음) ↔ `:257` §5 · OQ-947 「비활성 상대 1:1 도 고칠 수는 있다」(서버)
- 왜 FAIL: 서버 값은 OQ-947 로 정해졌는데 앱은 ① [수정] 을 메뉴에서 뺄지 ② 입력줄이 없는 화면에서 수정 모드 입력창만 띄울지 고를 근거가 없다 — mobile 워커가 추측으로 메운다. 시험(§13.2 r3 「수정 모드」)도 이 경우를 정하지 않는다
- 고칠 것(한 줄): §10.4 비활성 줄에 「수정 모드일 때만 입력창(수정 줄 + [저장])이 보인다」 또는 §10.7 표에 「비활성 1:1 = 수정 없음」. 서버가 이미 받는 쪽(OQ-947)이라 ① 이 결과와 맞다 — 고르는 건 코디

## WARN

| # | 자리 | 무엇 | 근거 |
|---|---|---|---|
| W-1 | `:752` §13.1 SSE 「다섯 이벤트에 `id:` 없음」 · `:766` §13.2 「SSE 파서가 채팅 이벤트 5개를 통과」 · `:816` OQ-902 「§14 주석 4곳」 · `:495` §10.5 「[보내기] →」 · WORK `:52` Meta 「완료 = … C1 ~ C12」 | r3 뒤 수가 낡음(이벤트 6 · 주석 5 · 버튼 [전송] · 완료 C1 ~ C17). 같은 문서 r3 줄(§7 `:354` 「여섯 이벤트」 · §14 `:809` 5 · §10.4 `:487` [전송] · WP-E2E C1 ~ C17)이 이기므로 워커는 안 막히지만, WORK Meta 의 완료 정의는 코디 · 사용자가 보는 줄이다 | §7 · §14 · D9-47 · WORK WP-E2E |
| W-2 | `:514` §10.6 · `:719` R-A17 `showChatPhoto`(`chat_photo_screen.dart:57`) · `:498` §10.5 (r3) 「`api.dart:31`」 | `0f0d969` 에 `showChatPhoto` 가 없다 — 실제는 `openPhotoViewer`(`chat_photo_screen.dart:55`) + `ChatPhotoViewer`(`:60`). `_timeout` 은 `0f0d969` `api.dart:33`(31 은 dbf0b53 줄 · 머리말 「r3 줄 = 0f0d969」와 어긋남) | grep `showChatPhoto` = 0 · `api.dart:33` |
| W-3 | §12.2 (빠진 자리) | **보내는 중 · 실패 말풍선 위젯** `chat_room_screen.dart:290-340`(`p.isPhoto` `:294` · `Image.memory(p.photoBytes!)` `:302` · `:330` · `:334`)이 R-A 어느 행에도 없다. 동영상 「바꾸는 중…」 · 썸네일 · 진행률 · 「N개 보내는 중」 줄(§10.5 `:496-497`)이 그려질 자리 — R-A3(모델)만 있고 화면 줄이 없다. WP-APP4 대상 파일에 `chat_room_screen.dart` 는 들어 있어 막히지는 않음 | grep `isPhoto` · §10.5 |
| W-4 | `:313` §6.2 #10 오류 칸 | `chat_message_empty`(「`text` · `photoId` 둘 다 없음」) · `invalid_request`(「`text` · `photoId` 둘 다」) 에 `videoId` 가 빠짐 — 같은 칸 끝 「셋 중 둘 이상 = invalid_request」 · R-B9 가 메워 주지만, 지금 코드 `service/chat.py:321` 이 `photo_id is None and …` 라 `videoId` 만 보낸 요청이 `chat_message_empty` 로 떨어지는 길을 그대로 둘 수 있다. §13.1 「동영상 보내기」 에 「`{clientId, videoId}` 만 = 200」 이 있어 시험이 잡는다 | `service/chat.py:319-322` |
| W-5 | `:257` §5 「수정」 · `:318` #15 · `:323` 검사 순서 | **남의 사진 · 동영상 · 남의 지운 메시지**를 PATCH 하면 403 `chat_not_yours` 인지 400 `chat_not_editable` 인지 — 검사 순서 줄은 400 을 「요청 모양」으로만 둬서 정하지 않는다. 1판 `delete` 꼴(`service/chat.py:371-374` 403 먼저)을 따르면 403. 앱은 남의 것에 [수정] 이 없어 사용자 표면은 같다 — 시험 기대만 갈림 | `service/chat.py:364-376` |
| W-6 | `:265` §5 「`since` 원천」 ↔ `:708` R-A6 | §5 는 「내가 지운 · **고친** 메시지는 HTTP 응답 뒤 화면만 바꾸고 `updatedAt` 은 SSE 가 넣을 때까지 원래 값」, R-A6 은 「`edit()` 은 HTTP 응답 `Message` 의 서버 `updatedAt` 을 써도 됨」. 둘 다 서버 값이라 안전하지만 한 쪽으로 맞추면 리뷰 기준이 하나가 된다 | CR1:FAIL-1 |
| W-7 | WORK `:88` WP-APP4 계약 칸 · `:724` R-A22 | APP4 가 입력줄(R-A10 · `chat-photo` 키)을 바꾸는데 1판 시험의 그 키(`test/chat_app*` 10곳)를 고치는 R-A22 는 APP5 에만 있다 → APP4 완료 명령 `flutter test test/chat_app*_test.dart` 가 R-A22 없이 빨강. 워커가 같이 고치겠지만 APP4 계약 칸에 R-A22 를 더하는 게 맞다 | `grep -c "chat-photo\|chat-send\|chat-delete-menu" test/*.dart` = 10 |
| W-8 | `:506` §10.6 카메라 칸 | 「찍으면 그 한 장을 **바로** 보냄」 — 최근 줄에서 이미 동그라미로 몇 개 고른 상태에서 카메라 칸을 누르면 고른 것은 어떻게 되는지(같이 보냄 · 남김 · 버림) 없음. 앱 워커가 고를 자리 — 기본값 한 줄 권장 | D9-48 |

## 사용자가 실물에서 만날 자리

| # | 자리 | 무엇 | 근거 · 확인 |
|---|---|---|---|
| U-1 | §9.2 「크기 한도」 `:404` · #16 `:319` · WP-INFRA `:92` | **운영 앞단 Cloudflare 의 요청 본문 한도.** 운영 API 는 Cloudflare 를 지난다(`deploy.md:75` 「Cloudflare 가 기본 python UA 를 403 으로」). Cloudflare 요청 본문 한도는 요금제에 따라 100MB(Free · Pro)인데, 서버 한도는 본 파일 100MB + 썸네일 ≤ 5MB + 64KB(R-B13 `:697`)라 100MB 근처 동영상은 서버에 닿기 전에 Cloudflare 413(앱은 JSON 오류가 아니어서 「보내지 못했어요」+ [다시 보내기] 반복). 시뮬레이터 · 로컬 compose 에서는 안 보이고 TestFlight 에서만 보인다. WP-INFRA 는 PVC 만 본다 → **WP-INFRA 에 「앞단(Cloudflare · ingress) 본문 한도 · 시간 한도 · 파드 `/tmp`(OQ-948 임시 파일) 여유」를 더하고**, C15 에 90MB 이상 동영상 1개를 넣을 것을 권장 | `deploy.md:75` · spec-r3-report 미결 4 |
| U-2 | §9.2 「길이 한도」 · 「크기 한도」 | D9-52 「3분 · 100MB」 두 한도 중 실제로는 100MB 가 먼저 걸릴 수 있다 — 1280×720 H.264 내보내기 비트레이트가 수 Mbps 대라 3분 영상이 100MB 를 넘는 경우가 생긴다(변환 패키지 · 원본마다 다름). 그때 사용자는 「3분 이하」 안내를 지킨 영상에서 「동영상이 100MB 를 넘어요」를 본다. 결정을 뒤집을 일은 아니고, C15 에 **2분 50초 안팎 영상 1개**를 넣어 실제 크기를 기록하면 D9-52 를 사용자가 판단할 수 있다 | D9-52 · OQ-950 |
| U-3 | §9.3 `:425` · OQ-952 · §10.4 `:484` | 링크 정규식 `https?://\S+` 는 공백 전까지 잡는다 — 한국어 글에서 흔한 「https://example.com에서 봐 주세요」 는 「에서」까지 링크가 돼 Safari 가 없는 주소를 연다. 끝 문장부호만 빼는 규칙으로는 안 막힌다. OQ-952 는 코디 기본값이라 FAIL 아님 — §13.2 링크 시험에 「주소 뒤 한글 붙음」 한 줄(링크 = ASCII 주소 문자까지)을 더할지 코디가 볼 자리 | D9-46 · OQ-952 |
| U-4 | §10.7 공유 `:532` | 동영상 공유 = 「#17 을 Bearer 로 내려받아 임시 파일로」 — 최대 100MB 를 받는 동안 「준비하는 중…」만 있고 취소 · 실패 문구가 없다(실패 시 토스트 꼴 미정). 사용자는 셀룰러에서 오래 기다리게 된다. 받는 방식(파일로 흘려 쓰기 — 메모리에 다 올리지 않기)도 한 줄이 있으면 좋다(§9.2 「변환 파일」은 100MB 를 메모리에 들지 않으려 한다고 적었는데 공유 쪽은 말이 없다) | D9-56 · OQ-956 |
| U-5 | C16 `:792` | 공유 시트에 「이미지 저장」 · 「비디오 저장」이 빠져도 「파일에 저장」 · 다른 앱이 남는다(`:533` ⚠ 로 이미 적힘) — 사용자가 E2E 때 「저장이 되네?」로 볼 수 있는 자리. D9-56 그대로라 지적 아님 · E2E 때 코디가 미리 말해 둘 것 | D9-56 |

## 조용히 통과하는 자리

- **W-4** — `videoId` 만 보낸 요청이 1판 빈 검사(`service/chat.py:321`)에 걸려 `chat_message_empty`. 서비스를 직접 부르는 시험이 `video_id=` 로 바로 넣으면 초록 · HTTP 경로로는 빨강일 수 있다 → §13.1 「동영상 보내기」는 **HTTP 로** 단언할 것(「푸시 대상」 줄과 같은 원칙)
- **R-B9 사진 갈래 `kind == "photo"` 검사** — 이 검사 없이도 1판 사진 시험은 모두 초록이다(동영상 행이 없으니). §13.1 r3 「동영상 id 를 `photoId` 로 = `chat_photo_invalid`」 · 「사진 id 로 동영상 열기 = 404」 가 이걸 잡는다 — 빠뜨리지 말 것
- **R-B13 413 `Content-Length` 기준** — 앱 스트림 요청이 `Content-Length` 를 안 실으면(청크) 먼저 거르기가 건너뛰어지고 100MB 넘는 파일을 다 받은 뒤에야 413. 1판 사진 올리기는 실었다(`api.dart:241-288`) · 동영상도 같은 꼴이어야 한다
- 수정 = 푸시 0 은 「가짜 APNs 요청 0」 으로 단언(§13.1 `:758`) — 서비스 직접 호출이면 원래 0 이라 의미가 없다. HTTP 경로로

## 참고(기존 부채 · 이번 FAIL 아님)

- `spec-r3-report.md` 미결 7: `scripts/lint-pipeline.py --strict` 이 이 워크트리에 없다 — 이 검수도 돌리지 못했다
- `chat_state.dart:428` `_onDeleted` 는 지운 사진의 메모리 캐시만 지운다 — 동영상 썸네일 캐시(R-A8 「키를 사진 id 와 섞지 않게」)를 지울 줄이 R-A6 「안 바꿈」 과 같이 있다. 지운 말풍선은 썸네일을 안 그리므로 사용자 표면은 같다
- SPEC-004 §7.3 49 ↔ 코드 51(OQ-920) 그대로

## §12.2 확인 표 (0f0d969 · 41행)

| 행 | 결과 |
|---|---|
| R-B1 `db.py:195-225` · `:212` · `:219-223` | ○ |
| R-B2 `db.py:227-237`(끝 `:238` 닫는 괄호) | ○ · `MIGRATIONS` 는 `CHAT_SCHEMA` 실행 뒤(`db.py:249-251`)라 새 DB · 옛 DB 둘 다 된다 |
| R-B3 `repo.py:667-771` · `:731` · `:755-759` · `_insert` `:132` · `_update` `:138` | ○ |
| R-B4 `schemas/chat.py:29-37` · `:34` · `:69-79` · `:74` | ○ |
| R-B5 `schemas/chat.py:119-124` | ○ |
| R-B6 `service/chat.py:30-38` | ○ |
| R-B7 `:85-93` · `:88` · `_messages` `:95-96`(첨부 행을 `photo_id` 로 읽음 — 동영상도 같은 길) | ○ |
| R-B8 `:109-117` · `:114` | ○ |
| R-B9 `post` `:317-362` · `:343` | ○ (W-4) |
| R-B10 · R-B11 `delete` `:364-387` · 파일 `:377-384` | ○ |
| R-B12 `upload` `:415-437` · `photo` `:439-459` | ○ |
| R-B13 `api/chat.py:45-134` · `:110-126` · `:129-134`(라우트 14 모두 `async def` · 도우미 `_int` `:38`) | ○ |
| R-B14 `api/photos.py:19-20`(`:18-21`) | ○ |
| R-B15 `push.py:35-42` · `:38` | ○ |
| R-B16 `push.py:164-193`(`kind == "system"` 만 거름 `:173` → 동영상 그대로 받음) | ○ |
| R-B17 `test_order.py:248-277` | ○ |
| R-B18 `container.py:129-131` | ○ |
| R-A1 `chat_model.dart:33-38` | ○ |
| R-A2 `:151-195`(`asDeleted` `:191`) | ○ |
| R-A3 `:198-210` | ○ |
| R-A4 `board_stream.dart:158` | ○ |
| R-A5 `chat_state.dart:357-385` | ○ |
| R-A6 `:96-107` · `:423-431` · `:516-519` | ○ (W-6) |
| R-A7 `:468-480` · `_deliver` `:485-513` | ○ |
| R-A8 `:562-576` · `clear` `:580-594` | ○ |
| R-A9 `chat_view.dart:19-26` · `:112-114` · `chat_ui.dart:71` | ○ |
| R-A10 `chat_room_screen.dart:399-423`(`_inputBar` `:400` · `:404` `chat-photo` · `maxLines: 5` `:412`) | ○ |
| R-A11 `:132-145` · `chat_photo_screen.dart:14-35`(함수는 `:14-50`) | ○ |
| R-A12 `photo_pick.dart:30-65` · `:35` | ○ |
| R-A13 `:224-251` · `:234` · `:247` | ○ |
| R-A14 `:254-264` · `:263` | ○ |
| R-A15 `:278-` · `:226` · `:394` | ○ |
| R-A16 `_deleteMenu` `:350-386` · `_bubbleCopy` `:388-397` | ○ |
| R-A17 `chat_photo_screen.dart:57-90` `showChatPhoto` | **이름 틀림** — `openPhotoViewer` `:55` · `ChatPhotoViewer` `:60` (W-2) |
| R-A18 `api.dart:232-233` · `:241-288` · `:289-` | ○ |
| R-A19 `pubspec.yaml:30-45` · `:44-45` | ○ |
| R-A20 `Info.plist:71-72` | ○ |
| R-A21 `app_state.dart:233` | ○ |
| R-A22 `test/chat_app1~3_test.dart` · `chat_fixture.dart` | ○ (W-7) |
| R-W1 `front/lib/hooks.ts:77` | ○ |
| 그 밖 r3 본문 줄: `service/chat.py:36` · `:56` · `:80-83` · `:147-156` · `:193-195` · `:389-409` · `chat_state.dart:15-26` · `:28-56` · `:287` · `app_state.dart:291` · `:432` · `reservation_detail_screen.dart:302` · `:310` · `Info.plist:69-72` | ○ |
| **빠진 자리** | `chat_room_screen.dart:290-340` 보내는 중 말풍선(W-3) |

## WORK-011 r3

- 순서 · 병렬: BE3 ∥ APP4(가짜 응답) → APP5(같은 mobile 워커 — 겹치는 파일 맞음) → REVIEW2 → SIM → (INFRA) → E2E. 계약 고정점 r3 6줄이 SPEC §3 · §6 · §7 · §8 · §9.2 와 같다 ○
- 대상 파일: R-A 22행 · R-B 18행 모두 BE3 · APP4 · APP5 중 하나에 들어감(R-A21 · R-B16 · R-B18 · R-W1 = 안 바꿈) ○ · W-7
- 완료 조건 · 검증 명령: BE3 `-k "chat or route_count or migration or push or photo"` ○ · APP4 `test/chat_app*_test.dart` ○ · APP5 `test/sse*` = `sse_parser_test.dart` 1개 — `otherEvents` 단언이 있는 `chat_app1_test.dart` 는 `chat_app*` 로 잡힘 ○
- WP-INFRA: PVC 만 — U-1(앞단 본문 한도 · 파드 `/tmp`)을 더하길 권장
- 실기기 E2E = 사용자 표면(TestFlight) ○ · C13 ~ C17 추가 ○ · FAIL-1(C8)

## public

SPEC · WORK 에서 키 머리 · 메일 · 전화 · 팀 id 꼴 grep 0.

```
$ git -C /Users/kknaks/orca/workspaces/kknaks_profile/cc-내부채팅 status --short
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
(이 검수가 만든 것 = `orchestration/work/internal-chat/review-doc-r3.md` 하나 — `internal-chat/` 가 통째로 untracked 라 위 목록에 따로 안 보인다)
