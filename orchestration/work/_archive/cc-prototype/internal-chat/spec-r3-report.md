# internal-chat spec r3 결과 보고

## 상태: done

## 수행 내용

- `para/projects/summer-star/cc-prototype/20-spec/spec-007-internal-chat.md` — **0.2.0 → 0.3.0**(draft) · 머리 변경 표 0.3.0 줄 · 바뀐 줄 끝 `(r3)` 117곳
- `para/projects/summer-star/cc-prototype/30-work/work-011-internal-chat.md` — 1판 WP 5개 + REVIEW = 「끝 — `0f0d969`」 · 새 WP **BE3 ∥ APP4 → APP5 → REVIEW2 → SIM · INFRA → E2E** · 계약 고정점 r3 6줄 · 병렬 그림 · 주의 4줄
- `20-spec/README.md` · `30-work/README.md` SPEC-007 · WORK-011 행 · `log.md` 한 줄
- SPEC-004 · DEC-009 는 안 고쳤다

### 동기 (1판 코드에 이미 있고 문서만 늦은 것)

| 원천 | SPEC-007 자리 |
|---|---|
| W2-1 (D9-45 들어올 때 읽음) | §4.2 「들어올 때 읽음」 · §13.1 |
| W2-2 (빈 방 · `read {messageId:0}`) | §5 「읽음 — 빈 방」 · OQ-943 · §13.1 |
| W2-3 (예약 상세 호출 자리) | §10.1 숨김 — `reservation_detail_screen.dart:302` · `:310`(0f0d969 에서 다시 잼 · be-brief 의 301-304 · 309-311 과 같은 자리) |
| W2-4 (루트 위 화면 배너 없음) | §10.12 |
| W2-5 (`flutter_image_compress`) | §9.1 앱 패키지 줄 |
| W2-6 (라우트만 보는 grep) | §6.1 |
| CR1:FAIL-1 (`since` 원천) | §5 「`since` 원천」 · §11 · §12.2 R-A6 · §13.2 |
| CR1:WARN-1 (열기 요청 보존) | §11 「계정 바뀜」 · §12.2 R-A8 · §13.2 |
| backend 값: 1:1 비활성 이름 꼴 | §4.5 · OQ-940 (`<이름> (비활성)` · `service/chat.py:36`) |
| backend 값: 혼자 남은 이름 없는 그룹 | §4.5 · OQ-941 (`name = ""` · `service/chat.py:56`) |
| backend 값: 숨긴 1:1 다시 열기 | §4.1 · OQ-942 (내 숨김만 · `chat_room` 나만 · 읽음 그대로 · `service/chat.py:193-195`) |
| backend 값: read 0 | §5 · OQ-943 (`service/chat.py:389-409`) |
| backend 값: 사진 width/height 필수 | §3.4 · §6.2 #13 · OQ-944 (`api/chat.py:124-125`) |
| (덤) 보낸 사람 없는 행 sender 채우기 | §6.1 · OQ-940 (`service/chat.py:80-83`) |

### 새 계약 (D9-46 ~ D9-57)

- **표**: `chat_message.kind` 에 `video` · `edited_at` · `chat_photo` = 첨부(`kind` · `duration_ms` · `thumb_file_name`) · `MIGRATIONS` 4줄 · 표 · 열 이름은 그대로(OQ-945)
- **API +4 → 18 · 경로 65 → 69**: #15 `PATCH /api/chat/messages/{id}` · #16 `POST /api/chat/videos`(multipart 본 파일 + 썸네일) · #17 `GET /api/chat/videos/{id}`(`Range` → 206 · Starlette 1.9.0 `FileResponse` 가 이미 처리 — 설치본 `responses.py:367-392` 확인) · #18 `GET …/thumbnail` · 보내기 `{clientId, videoId}`
- **오류 코드 14 → 20**: `chat_video_not_found` · `chat_not_editable` · `chat_video_invalid` · `chat_video_type` · `chat_video_too_long` · `chat_video_too_large`
- **SSE 5 → 6**: `chat_message_edited {roomId, message}`
- **푸시**: 동영상 본문 「동영상」 · 수정 = 푸시 없음 · 여러 개 = 메시지마다
- **변환 · 한도**: §9.2(앱 · iOS 네이티브 내보내기 · 1280 · 썸네일 0초 · 3분 · 100MB · 300초 · 실패 토스트 · 임시 파일 지우는 때)
- **화면**: §10.4(넓은 입력창 · 동영상 말풍선 · 링크 · 「수정됨」) · §10.5(N개 보내는 중) · §10.6([+] 시트 · 최근 줄 권한 · 여러 개 · 재생 화면) · §10.7(5메뉴 표 · 복사 · 선택 복사 · 공유 저장 뺌 · 수정 모드 · 삭제)
- **시안과 다른 곳** §10.13 #11 ~ #16 = 「D9-47 ~ D9-56 · 사용자 스샷 기준 · 기존 위젯 · 테마로」
- 시험 §13.1 r3 9줄 · §13.2 r3 · 실기기 C13 ~ C17

## 검증

### DEC D-01 ~ D-57 → SPEC (부록 A)

- 부록 A 행 = **57 / 57** (`sed -n '/^## 부록 A/,/^## 부록 B/p' … | grep -oE "^\| D-[0-9]+" | sort -u | wc -l` = 57) · 본문에 D9-01 ~ D9-57 전부 나옴(빠짐 0 — 반복 grep)
- 뒤집힌 줄: D-03(영상 → D-49 · 수정 → D-55) · D-15(1장 → D-50) · D-17(동영상 파일 두 개 · 5메뉴) · D-22(동영상 썸네일 = 앱) · D-24(공유 · 변환 임시 파일 예외) — 부록 A 「뒤집힘」 표시 · 본문은 ~~취소선~~ 또는 「r3 에서 넣음」(§1.2 · §10.4 · §10.6 · §10.7)

### sim-feedback F1 ~ F4 → SPEC (부록 C) = **4 / 4**

### §12 다시 grep (0f0d969 · 코드 워크트리 `/Users/kknaks/orca/workspaces/cc-prototype/internal-chat` · `git log -1` = `0f0d969` · `status` 깨끗)

§12 는 1판 표를 §12.1(dbf0b53 · 이력)로 두고 **§12.2 = r3 자리 41행**(back R-B1 ~ 18 · app R-A1 ~ 22 · web R-W1)을 0f0d969 줄로 새로 썼다. 쓴 명령(`procedure/` 에서):

| # | 명령 | 수 | §12.2 |
|---|---|---|---|
| G1 | `grep -rn '"text", "photo", "system"\|text \| photo \| system\|MsgKind { text, photo, system }' back/app app/lib` | 4 | R-B1(`db.py:212`) · R-B4(`schemas/chat.py:34` · `:74`) · R-A1(`chat_model.dart:33`) |
| G2 | `grep -rn 'kind == "photo"\|MsgKind.photo\|"photo" if' back/app app/lib` | 5 | R-B15(`push.py:38`) · R-B9(`service/chat.py:343`) · R-A9(`chat_view.dart:25` · `:113`) · R-A1(`chat_model.dart:36`) |
| G2b | `grep -rn '\.photo != null\|m\.photo!' app/lib` | 4 | R-A8(`chat_state.dart:428`) · R-A15(`chat_room_screen.dart:226` · `:279` · `:394`) |
| G3 | `grep -rn "chat_message_deleted" back/app app/lib` | 5 | R-B11 · R-A4(`board_stream.dart:158`) · R-A2 · R-A5(`chat_state.dart:362`) · R-A6 |
| G4 | `grep -rn "onLongPress" app/lib/screens/chat_*.dart app/lib/chat` | 1 | R-A13(`chat_room_screen.dart:247`) |
| G5 | `grep -n "Text(text\|Text(m.text" app/lib/screens/chat_*.dart` | 2 | R-A14(`:263` 본문) · `:219` = 시스템 줄(링크 안 함 · 안 바꿈) |
| G6 | `grep -rn "request.form\|spool_max_size" back/app` | 3 | R-B13(`api/chat.py:117`) · R-B14(`api/photos.py:20`) · 신분증 사진 `photos.py` 1(안 바꿈) |
| G7 | `grep -rn "pickImage\|pickMultiple\|pickVideo" app/lib` | 1 | R-A12(`photo_pick.dart:35`) |
| G8 | `grep -n "CHAT_ROUTES\|test_route_count" back/tests/test_order.py` | 2 | R-B17(`:248` · `:256`) |
| G9 | `grep -n "openQrScreen\|openPassportScan\|showQuestionnaireQrHere" app/lib/screens/reservation_detail_screen.dart` | 2 | §10.1(`:302` · `:310` · W2-3) |
| G10 | 패키지 · plist — `sed -n 25,60p app/pubspec.yaml` · `grep -n UsageDescription app/ios/Runner/Info.plist` | 2 · 4 | R-A19(`:44-45`) · R-A20(`:71-72`) |

빠진 자리 확인: 위 grep 에 나온 줄은 모두 §12.2 한 행에 들었거나 「안 바꿈」으로 적었다(G5 `:219` · G6 신분증 1).

### 패키지 (pub.dev · 2026-10-29) — 결정 안 함 · 후보 + 권장 1개 (§9.3)

| 쓰임 | 권장 | 근거 URL |
|---|---|---|
| 최근 줄 | `photo_manager` 3.12.0 | https://pub.dev/packages/photo_manager |
| 갤러리 여러 개 | `image_picker` 1.2.4 `pickMultipleMedia(limit:)` (이미 있음) | https://pub.dev/documentation/image_picker/latest/image_picker/ImagePicker/pickMultipleMedia.html |
| 변환 · 썸네일 | `video_compress` 3.1.4 `Res1280x720Quality` · ⚠ 20개월 전 판 → 실기기 확인 · 안 되면 네이티브 `AVAssetExportSession` | https://pub.dev/packages/video_compress · https://pub.dev/documentation/video_compress/latest/video_compress/VideoQuality.html |
| 재생 | `video_player` 2.14.1 `networkUrl(httpHeaders:)` | https://pub.dev/documentation/video_player/latest/video_player/VideoPlayerController/VideoPlayerController.networkUrl.html |
| 공유 저장 빼기 | `share_plus` 13.3.1 `excludedCupertinoActivities` · `CupertinoActivityType.saveToCameraRoll` 있음 → **플러그인으로 됨 · 네이티브 채널 불필요** | https://pub.dev/documentation/share_plus/latest/share_plus/CupertinoActivityType.html |
| 링크 열기 | `url_launcher` 6.3.3 | https://pub.dev/packages/url_launcher |
| 링크 찾기 | 패키지 없이(정규식) — 대안 `flutter_linkify` 6.0.0(3년 전 · 메일까지 잡음) | https://pub.dev/packages/flutter_linkify |

### 그 밖

- public grep(`sk-` · 키 머리 · 메일 · 전화 · 팀 id) SPEC · WORK = 0
- frontmatter: SPEC `version: 0.3.0` · `sources` 에 sim-feedback · be-brief §0 · review-code-r1 · `0f0d969` · pub.dev 더함 · `status: draft` 그대로
- ⚠ `python3 scripts/lint-pipeline.py --strict` — **이 워크트리에 파일이 없다**(`can't open file … scripts/lint-pipeline.py`) → pending. 코디가 다른 자리에서 돌려 주거나 경로를 알려 주면 다시 돌린다

## 이 문서가 고른 기본값 (전부 §15 OQ · 확정 아님)

OQ-940 ~ OQ-944 = 1판 코드 값 그대로 · OQ-945 표 이름 그대로 · OQ-946 여러 개 = 하나씩 · 실패만 남김 · OQ-947 수정 세부(같은 글 · 비활성 1:1 · 실패 토스트) · OQ-948 동영상 multipart + 전역 spool 그대로(임시 파일) · HEAD 없음 · OQ-949 3분 넘는 것만 빼고 보냄 · OQ-950 변환 패키지 · 썸네일 0초 · 300초 · 임시 파일 · 소리 · OQ-951 미리보기 「수정됨」 없음 · OQ-952 링크 정규식 · OQ-953 입력창 높이 · 재생 조작 · OQ-954 최근 줄 60개 · 권한 문구 · OQ-955 보내는 중 메뉴 없음 · 선택 복사 꼴 · OQ-956 공유 임시 파일

## 미결 · 주의점

1. **OQ-956 공유 임시 파일 ↔ D9-24** — 공유 시트는 파일을 받아야 해서 사진 · 동영상을 잠깐 디스크에 쓴다(시트 닫히면 지움). D9-56 이 공유를 넣었으니 같이 온다고 봤다 — 사용자가 볼 자리. 권장: 이대로
2. **D9-56 의 빈틈** — 공유 시트의 「다른 앱으로」에 사진 · 파일 앱이 있어 저장 비슷한 길이 남는다. D9-56 은 「이미지 저장 · 비디오 저장」만 빼라 했으니 그대로 적고 §10.7 ⚠ 로 표시만 했다
3. **OQ-941 혼자 남은 그룹 제목 = 빈 문자열** — 방 목록 · 대화 머리에 제목이 비어 보인다. 1판 코드 값 그대로 적었다. 바꾸려면 사용자 결정(예: 「(나만 남음)」)
4. **OQ-948 동영상 받기** — 전역 `spool_max_size` 를 안 올리고 Starlette 임시 파일(컨테이너 `/tmp`)을 쓴다. 파드 임시 디스크 여유는 WP-INFRA 에서 PVC 와 같이 봐 달라
5. **`video_compress` 오래됨** — WP-APP4 완료 조건에 실기기 1회(HEVC 4K · 슬로모 · 세로)를 넣었다. 안 되면 네이티브 채널
6. 1판 TestFlight 빌드는 `video` 를 빈 말풍선으로 그린다 → back 배포 = 새 빌드와 같이(WORK-011 주의)
7. lint 스크립트 없음(위)

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
r3 가 손댄 것 = spec-007 · work-011 · 20-spec/README · 30-work/README · log.md · 이 리포트(나머지 줄은 앞 판 · 코디 몫 그대로). SPEC-004 는 이번에 안 건드림(앞 판 3줄 변경이 남아 있는 것).
