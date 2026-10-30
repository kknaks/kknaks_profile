# 리뷰 리포트 — internal-chat / code r2 (2026-10-29)

대상: `/Users/kknaks/orca/workspaces/cc-prototype/internal-chat` `0f0d969` 이후 미커밋 변경(back BE3 · app APP4 · APP5 · 30 파일)
SSOT: r3-dispositions.md > SPEC-007 0.3.0 (r3) · WORK-011 WP-REVIEW2 · DEC-009 > review-doc-r3 · sim-feedback F1 ~ F4
읽기 목적 실행: `uv run pytest -q tests/test_chat_r3.py` = **15 passed**(전체 515 · flutter test 210 은 코디 수치 그대로 믿음 — 다시 안 돌림). 파일 생성 · 수정 · 서버 · 시뮬레이터 실행 0.

## 판정: WARN (FAIL 0 · WARN 7)

계약(이름 · 타입 · 꼴) 양쪽 대조는 전부 맞고, r3 처분 12행 모두 코드에 있다. 남은 것은 실기기 · 경계에서 사용자가 보는 자리다 — 3분 경계 · 진행률 · 연달아 보내기 · 무음 스위치 · limited 자동 알림.

## FAIL

없음.

## WARN

| # | 자리 | 무엇 | 근거 |
|---|---|---|---|
| W-1 | `app/lib/chat/video_pick.dart:64` · `app/lib/chat/photo_pick.dart:178` · `:130` · `app/lib/chat/chat_state.dart:602` ↔ `back/app/service/chat.py:533` | **3분 경계가 앱 · 서버에서 다르다.** 앱은 변환 뒤 길이를 `> 180000 + 999` 로 봐 주고(`:64`), 최근 줄 길이는 photo_manager 가 **초로 반올림**(`lround` — `PMConvertUtils.m:12`)한 값 × 1000 이라 180.4초 영상 = 180000 → 흐리지 않음. 그런데 앱은 **변환 뒤 실제 ms**(`p.durationMs`)를 올리고 서버는 `> 180000` 이면 400. → 사진 앱에서 「3:00」로 보이는 영상(180.0 ~ 180.49초)이나 변환이 몇십 ms 늘린 영상은 **바꾸기 + 90MB 근처 올리기를 다 마친 뒤** 토스트 「3분 이하 동영상만 보낼 수 있어요」. 고칠 자리 하나: 앱이 `min(durationMs, 180000)` 을 보내거나(봐 준 범위를 서버와 맞춤) 봐 주기를 없애고 최근 줄을 `> 180000` 대신 원본 ms 로 보기. 갤러리 길(`probe` = AVURLAsset ms)은 이미 엄격해서 두 길이 서로 다르게 군다 | §9.2 「길이 한도」 · D9-52 · OQ-949 |
| W-2 | `app/lib/api/api.dart:341-351` (1판 `:267` 꼴 그대로) | **동영상 진행률 = 「읽은 바이트」이지 「보낸 바이트」가 아니다 · 90MB 가 메모리에 쌓일 수 있다.** `req.sink.add` 는 되밀기(backpressure)가 없고 `Future.delayed(Duration.zero)` 는 네트워크를 기다리지 않는다 → 파일을 읽는 속도로 `StreamedRequest` 버퍼에 다 들어가 진행률이 금방 100% 근처로 가고, 실제 업로드는 그 뒤에 진행. 로컬 back(시뮬레이터)에서는 안 보이고 셀룰러 실기기에서 「올리는 중 100%」로 오래 서 있다. 사진(5MB)은 1판에서 문제가 아니었지만 90MB 에서는 주석 「메모리에 다 올리지 않음」과도 어긋남. 권장: `await req.sink.addStream(file.openRead().map(...진행률...))`(addStream 은 받는 쪽 pause 를 원천에 넘김) | §9.2 「올리기 시간 한도 · 진행률」(보낸 바이트) · 「변환 파일」(100MB 를 메모리에 들지 않으려고) |
| W-3 | `app/lib/screens/chat_room_screen.dart:151-152` · `app/lib/chat/photo_pick.dart` `PhotoManagerMedia.clearFiles` | **두 묶음을 연달아 보내면 뒤 묶음이 깨질 수 있다.** 묶음 A 가 끝나면 `PhotoManager.clearFileCache()` 로 photo_manager 사본 **전부**를 지운다. 그때 묶음 B(시트를 다시 열어 보낸 것 · `sendMany` 는 묶음마다 따로 돈다)가 최근 줄 동영상을 변환 중이면 원본 사본이 지워져 내보내기 실패 → 「동영상을 보내지 못했어요」. 변환은 수십 초라 사용자가 첫 동영상이 「바꾸는 중…」일 때 다른 것을 더 보내는 흐름에서 생긴다. 권장: 항목마다 받은 사본을 변환 뒤 그 파일만 지우거나, 진행 중 묶음 수가 0 일 때만 `clearFileCache` | §9.2 「변환 파일」 · D9-50 |
| W-4 | `app/lib/screens/chat_video_screen.dart:75` | **재생이 무음 스위치를 따르지 않는다(실기기).** video_player_avfoundation 2.12.1 은 플레이어를 만들 때 오디오 세션을 `.playback` 으로 올린다(`VideoPlayerPlugin.swift:153`) — `.playback` 은 무음 스위치를 무시. SPEC 은 「소리 = 기기 음량 · 무음 스위치를 따른다」. 진료실에서 무음으로 둔 폰에서 동영상을 열면 소리가 난다. 플러그인은 카테고리를 낮추지 않으므로 네이티브 채널(`.ambient`/`.soloAmbient`)이 필요하거나, OQ-950 기본값을 「소리 남」으로 바꾸는 코디 판단 | §9.2 「재생」 · OQ-950 |
| W-5 | `app/ios/Runner/Info.plist` · `app/lib/chat/photo_pick.dart:159` | **「선택한 사진만」(limited)을 고르면 iOS 가 앱을 켤 때마다 「더 많은 사진 선택 / 현재 선택 유지」 알림을 스스로 띄운다** — `PHPhotoLibraryPreventAutomaticLimitedAccessAlert` 가 없음. 앱에 이미 [더 고르기]가 있으므로 `true` 한 줄이면 됨. 시뮬레이터에서 사용자가 limited 를 고르면 바로 보인다 | §10.6 「권한」 · D9-48 |
| W-6 | `app/ios/Runner/AppDelegate.swift:364-365` | `probe` 가 `AVURLAsset(url:).duration` 을 **메인 스레드에서 동기로** 읽는다(iOS 16 deprecated · 로드가 끝날 때까지 막음). 로컬 파일이라 보통 짧지만 갤러리에서 고른 동영상마다 한 번씩. `convert` 는 `exportAsynchronously` 완료 쪽(배경)에서 썸네일까지 만들어 괜찮다. 권장: `probe` 도 `DispatchQueue.global` 에서 읽고 `main.async { result }` | 브리프 「메인 스레드 막힘」 |
| W-7 | `app/test/chat_app5_test.dart:225-266` | 동영상 공유 [취소](U-4)가 **시험에 없다** — 「준비하는 중…」 · [취소] 가 보이는 것만 단언하고 누르지 않는다. 코드(`chat_room_screen.dart:515-` · `api.dart:402`)는 취소 = 다음 조각에서 멈춤 → 파일 지움 · 토스트 없음으로 맞게 되어 있으나 회귀 잠금이 없다 | r3 처분 U-4 · §13.2 r3 |

## 사용자가 시뮬레이터에서 만날 자리 (지금 코디가 올린 빌드)

| # | 무엇 | 왜 · 무엇을 말해 둘지 |
|---|---|---|
| S-1 | [+] 시트 **카메라 칸을 누르면 「사진을 불러오지 못했어요」** | 시뮬레이터에는 카메라가 없다 — image_picker 가 오류 → `_camera` 의 catch(`chat_room_screen.dart:166-`)가 1판 문구로 토스트. 버그 아님(실기기에서 확인) · 사용자에게 미리 말할 것 |
| S-2 | 처음 [+] 을 누르면 **사진 보관함 권한 창** · limited 를 고르면 W-5 알림이 다음 실행부터 뜸 | `requestPermissionExtend` 가 시트를 열 때마다 불림(이미 정한 뒤엔 창 없음) |
| S-3 | 최근 줄에 **동영상이 없다** | 시뮬레이터 사진 앱 기본 항목은 사진뿐 — 동영상을 시뮬레이터 창에 끌어 놓아야 「m:ss」 칸 · 3분 흐림 · 변환을 볼 수 있다. 3분 경계(W-1)를 보려면 3:00 근처 영상 1개 |
| S-4 | 동영상 「바꾸는 중…」 동안 진행 막대가 0 에 서 있다 | 변환은 진행률을 안 준다(SPEC 도 요구 안 함) · 4K 원본이면 시뮬레이터에서 수십 초 |
| S-5 | 「올리는 중 N%」가 금방 끝난다 | 로컬 back 이라 빠름 — W-2 는 여기서 안 보이고 실기기 셀룰러에서 보인다 |
| S-6 | 「사진」(갤러리)에서 큰 동영상을 고르면 시트가 닫힌 뒤 **잠깐 아무것도 안 보인다** | `pickMultipleMedia` 가 고른 파일을 앱 임시 폴더로 복사한 뒤에야 돌아와 보내는 중 말풍선이 붙는다(최근 줄 길은 바로 붙음) |
| S-7 | 공유 시트에 「이미지 저장」 · 「비디오 저장」은 없지만 **「파일에 저장」 · 다른 앱은 있다** | D9-56 그대로(U-5) — 미리 말할 것 |
| S-8 | 링크 누르면 Safari 로 앱을 떠남 · 「https://example.com에서」 는 `https://example.com` 까지만 밑줄 | D9-46 · U-3 대로 |
| S-9 | 아이패드: [+] 시트 · 선택 복사가 **가운데 대화상자** · 공유 = 말풍선에서 팝오버 | §10.11 · `sharePositionOrigin` = 말풍선 rect |
| S-10 | 변환 중 다른 앱으로 나갔다 오면 그 동영상이 「동영상을 보내지 못했어요」로 빠질 수 있다 | `AVAssetExportSession` 은 앱이 백그라운드로 가면 중단된다 → 변환 실패 = 말풍선 지움(§9.2 대로 · 다시 보내기 없음) |

## 양쪽 대조 (back 구현 ↔ app 소비)

| 계약 | back | app | 결과 |
|---|---|---|---|
| #10 `{clientId, videoId}` | `SendRequest.videoId: StrictInt\|None` · `post(... video_id)` 셋 중 둘 이상 = `invalid_request` · 빈 검사에 첨부 포함(`service/chat.py` `post`) | `chatSend(videoId:)` `'videoId': ?videoId` | ○ · W-4 HTTP 시험 `test_chat_video_send_open` |
| #15 `PATCH /messages/{id} {text}` → `Message` | `EditRequest{text}`(extra forbid) · `edit()` `:412` | `chatEdit` → `_onEdited(r)`(응답 서버 `updatedAt` · W-6) | ○ |
| #16 multipart `roomId · video · thumb · width · height · durationMs` → `{videoId}` | `api/chat.py:146` `max_files=2` · `_int` · `VideoUploadResponse` | `chatUploadVideo` 같은 6칸 · `Content-Length` 실음(`req.contentLength`) · 300초 | ○ (진행률 = W-2) |
| #17 `GET videos/{id}` Range | `FileResponse`(starlette 1.9.0) · `video/mp4` · `no-store` · `inline` | `VideoPlayerController.networkUrl(httpHeaders: Bearer)` · 공유 = `chatVideoDownload` 파일로 흘림 | ○ · 206 · 416 · `Accept-Ranges` 시험 있음 |
| #18 `GET videos/{id}/thumbnail` | `image/jpeg` · 같은 권한 | `chatVideoThumb` → `PhotoCache` 키 `thumbKey(id)`(사진 id 와 안 섞임 · R-A8) | ○ |
| `Message.video {id, width, height, durationMs}` · `editedAt` · `kind "video"` | `schemas/chat.py` `VideoRef` · `Message.video` · `editedAt` · `Literal[... "video" ...]` | `VideoRef` · `ChatMessage.video` · `editedAt` · `MsgKind.video` · 모르는 kind = text | ○ |
| `Preview.kind "video"` · `text` null | `_room` `kind in ("photo","video")` → null | `previewOf` 「동영상」 + `videocam` 아이콘 | ○ |
| SSE `chat_message_edited {roomId, message}` | 커밋 뒤 지금 멤버(`chat_members` = `left_at IS NULL`) · 같은 글 = 안 냄 · `id:` 없음 | `otherEvents` 6개 · `_onEdited`(더 옛 `updatedAt` 은 안 덮음 · 미리보기 글만 · 배지 그대로) | ○ |
| 푸시 본문 「동영상」 · 수정 = 푸시 0 | `chat_body` `video` 갈래 · `edit()` 가 `self.push` 안 부름 | 배너 `bodyHead` 「동영상」 | ○ · 가짜 APNs 요청 0 을 HTTP 로 단언 |
| 오류 코드 r3 6개 | `chat_video_not_found` · `chat_not_editable` · `chat_video_invalid` · `chat_video_type` · `chat_video_too_long` · `chat_video_too_large` | 4xx = `e.message` 토스트(`_deliver` · `_saveEdit`) | ○ |
| 한도 90MB(D-58) | `VIDEO_MAX_BYTES` · `Content-Length > 90MB + 5MB + 64KB` = 413 · 조각 복사 중 넘으면 멈추고 지움 | `maxVideoBytes` 90MB · 문구 「동영상이 90MB 를 넘어요」 | ○ |

수치: API 18 · 경로 69(`test_route_count_69` · 채팅 밖 51 그대로) · SSE 6 · 오류 코드 20 · 법적 검토 주석 `grep -rn "법적 검토 필요: 직원 채팅" procedure/back` = **5** · 라우트 핸들러 `def` 0(`test_chat_route_handlers_async`).

## r3-dispositions 대조 (12행)

| 처분 | 코드 | 결과 |
|---|---|---|
| D-58 · D-59 90MB · `Content-Length`(청크 금지) | 위 표 · `chat_app4_test.dart:325` 단언 | ○ |
| FAIL-1 남의 메시지 = 복사 · 선택 복사 · 공유 | `chatMenuOf` `chat_room_screen.dart:804` | ○ |
| FAIL-2 비활성 1:1 = [수정] 숨김 | `chatMenuOf(peerInactive:)` | ○ |
| W-4 `{clientId, videoId}` = 200 · HTTP | `test_chat_video_send_open` | ○ |
| W-5 남의 것 403 먼저 · 내 사진 · 동영상 · 지움 · 시스템 줄 = 400 | `edit()` 검사 차례 · `test_chat_edit_not_yours_not_editable` | ○ (시스템 줄 = 400 은 처분대로 · SPEC §5 「403」은 처분이 이김) |
| W-6 응답 `updatedAt` 써도 됨 · 앱 시각 금지 | `edit()` → `_onEdited(r)` · `DateTime.now()` 안 씀 | ○ |
| W-7 1판 시험 키 같이 고침 | `chat_app1/2_test.dart` `chat-photo` → `chat-plus` · 단언 약해짐 없음(확인) | ○ |
| W-8 카메라 칸 = 바로 보냄 · 고른 것 남김 | `_camera` 가 시트를 안 닫음 · `chat_app2_test` 「시트는 그대로」 | ○ |
| U-3 ASCII 주소 문자만 | `chat_view.dart:129` · 「https://example.com에서 봐요」 시험 | ○ |
| U-4 공유 = 파일로 흘림 · 진행률 · [취소] · 실패 토스트 · 지움 | `_shareVideo` · `chatVideoDownload` | ○ (취소 시험 없음 = W-7) |
| U-1 · U-2 · U-5 | 코디 몫(E2E) | — |
| W-1 · W-2 · W-3 | 실제 이름 사용 · 보내는 중 말풍선 「바꾸는 중…」 · 진행률 · 「N개 보내는 중 · k/N」(`_pendingRow` · `_batchLine`) | ○ |

## 브리프 지정 항목

**네이티브 변환 채널 (`AppDelegate.swift:348-` `VideoConverter`)**
- 실패 → Dart: `FlutterError(convert_failed)`(세션 없음 · 내보내기 실패 · 썸네일 실패) → `VideoChannel.convert` 가 null → `MediaRejected(videoFailed)` → 그 말풍선만 빠지고 토스트 ○
- 임시 파일: 실패 때 만들다 만 `chat-video-<UUID>.mp4` 지움 ○ · 성공 파일은 Dart 가 보내기 끝 · 4xx · 401 · 로그아웃 · 방 빠짐 때 지움(`_deliver` · `_drop` · `clear` · `_remove`) ○ · 갤러리 원본 사본 = `deleteSource: true` ○ · 최근 줄 사본 = `clearFileCache`(W-3)
- 메인 스레드: `convert` 는 배경 완료 핸들러 · 결과만 `main.async` ○ · `probe` 동기(W-6)
- 동시 호출: 상태를 갖지 않고 출력 이름이 UUID — 겹쳐도 안전 ○
- HEVC · 세로: `AVAssetExportPreset1280x720` = H.264 · 업스케일 없음 · 원본 `preferredTransform` 을 트랙에 그대로 둠 → AVPlayer 가 세로로 그림 · 썸네일 `appliesPreferredTrackTransform = true` 라 `width/height` = 보이는 방향(720×1280) ○ · `shouldOptimizeForNetworkUse` = moov 앞 → Range 재생에 맞음 ○. HDR(돌비 비전) 원본은 SDR H.264 로 나옴(실기기 C15 에서 색 확인 권장)

**공유**: `excludedCupertinoActivities: [saveToCameraRoll]` 텍스트 · 사진 · 동영상 모두 ○ · 임시 폴더 = 시트가 닫힌 뒤(`SharePlus.share` 완료) 통째로 지움 ○ · 취소 = 다음 조각에서 멈춤 · 파일 지움 · 토스트 없음 ○ · 아이패드 `sharePositionOrigin` = 말풍선 ○

## 1판 회귀

- back: 채팅 밖 경로 51 단언 그대로 · `api/photos.py` 주석 한 줄만(전역 spool 그대로 — 시험이 값 단언) · `push.py` = `chat_body` 갈래만 · `db.py` = 열 더하기 + MIGRATIONS 4줄(옛 DB 시험 `test_chat_migration_r3`) · 원장 · 상담사 호출 · 띄우기 · 여권 · 알림 목록 코드 변경 0
- app: `AppDelegate` 기존 `procedure/push` · `procedure/scan` 채널 그대로(새 채널 하나 더함) · `Info.plist` 사진 보관함 문구만(쓰기 문구 없음 ○) · `pubspec.lock` = 새 패키지 추가만 · 기존 패키지 판 바뀜 0 · iOS 15.0 그대로
- 1판 채팅: 1판 시험은 키 이름만 바뀌고 단언은 그대로거나 늘었다(FAIL-1 반영)
- 기능 독립: 변경 30 파일 모두 `procedure/` 안 ○

## 조용히 통과하는 자리 (review-doc-r3 4개)

- `videoId` 만 보내기 — HTTP 로 단언(`test_chat_video_send_open`) ○
- 사진 갈래 `kind == "photo"` — 「동영상 id 를 photoId 로 = chat_photo_invalid」 · 「사진 id 로 동영상 열기 = 404」 둘 다 HTTP ○
- `Content-Length` 먼저 거르기 — back 은 머리만 큰 요청으로 413 단언 · app 은 `contentLength` 단언 ○
- 수정 = 푸시 0 — HTTP + 가짜 APNs 요청 0 ○
- 새로 찾은 것: W-1(3분 경계 — 시험은 앱 · 서버를 따로 단언해 각각 초록, 이어 붙이면 갈림) · W-2(진행률 시험은 가짜 클라이언트라 되밀기가 없어도 초록)

## 참고(기존 부채)

- `chatUploadPhoto`(1판 `api.dart:267`)도 W-2 와 같은 꼴 — 5MB 라 사용자 표면은 작음
- `_load` 가 `restart` 중 다른 로드가 돌고 있으면 그 restart 를 버림(`chat_attach_sheet.dart:94`) — [더 고르기] 직후 줄이 안 바뀌어 보일 수 있는 드문 경우
- 로그아웃 중 `sendMany` 가 `thread(roomId)` 로 빈 스레드를 하나 다시 만든다(`chat_state.dart:554` · 다음 항목은 보내지 않고 건너뜀 — 표면 영향 없음)
