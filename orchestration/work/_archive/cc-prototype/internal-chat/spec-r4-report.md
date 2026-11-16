# internal-chat planner r4 결과 보고

## 상태: done

## 수행 내용

- `para/projects/summer-star/cc-prototype/20-spec/spec-007-internal-chat.md` **0.3.0 → 0.4.0**(draft 그대로) · 바뀐 줄 끝 `(r4)` · 머리 변경 표 0.4.0 행
- `para/projects/summer-star/cc-prototype/20-spec/spec-004-procedure-app.md` — §6.5 통역 드로어 **높이 한 줄만**(D-65 · 놓인 칸 높이 92% · 상태 표시줄 아래 · 손잡이 끌어 내려 닫기 · 아이패드)
- `para/projects/summer-star/cc-prototype/30-work/work-011-internal-chat.md` — r3 WP 상태 끝 처리(BE3 · APP4 · APP5 · REVIEW2 · SIM · INFRA · E2E 배포) · 계약 고정점 r4 3줄 · **WP-BE4 ∥ WP-APP6 → WP-REVIEW3 → WP-SIM2 → WP-DEPLOY13(빌드 13) → WP-E2E2** · 병렬 그림 · 주의 r4 3줄 · infra r4 = 변경 없음
- `20-spec/README.md` · `30-work/README.md` 행 고침 · `log.md` 한 줄 · DEC-009 안 고침

### 새 계약 — 전달 (SPEC-007 §3 r4 · §5 「전달」 · §6.2 #19 · §10.14)

- **API** `POST /api/chat/messages/{messageId}/forward` · 요청 `{targets:[{roomId, clientId} | {accountId, clientId}]}`(1 ~ 10) · 응답 `{results:[{ok:true, roomId, message} | {ok:false, roomId|null, error}]}` 대상 차례 · **일부 · 전부 실패도 200**(요청 전체 오류만 4xx) · 새 오류 코드 `chat_not_forwardable` 1개 · 한 트랜잭션
  - 근거(§6.2 「#19 모양을 이렇게 고른 근거」): 대상마다 `clientId` = 보내기 규칙(D9-16 · UNIQUE) 그대로 · 실패한 대상만 다시 보내기 / 일부 실패가 전체를 막지 않음 / 원본이 경로 = #11 · #15 와 같은 권한 자리 / 방 · 사람 둘 다 받음 = D9-63 목록 · D9-64 「없으면 만든다」를 요청 1개로
- **권한**: 원본 방 지금 멤버만(나간 사람 404) · 남의 메시지도 됨(D9-54) · 시스템 · 지운 것 400 / 대상별: 멤버 아닌 방 404 · 비활성 상대 1:1 409 · 후보 아닌 사람 400 — 그 대상만 실패
- **첨부 = 대상마다 새 `chat_photo` 행 + 같은 파일**(복사 0) · 파일은 같은 `file_name` 을 가리키는 안 지운 행이 0 일 때만 지움 · 인덱스 `chat_photo_file`
  - 근거(§3 「왜 새 행인가」): 열람 권한이 행의 `room_id` · `message_id` 로 정해짐(D9-23) · `message_id` 1:1 유지 · 삭제가 메시지마다 따로 → **원본을 지워도 전달본은 열린다**(브리프 요구) / 파일 복사 안 함 = D9-64 「같은 파일을 이어 쓴다」 · 볼륨 아낌
- SSE · 푸시 = 보내기와 같음(만든 메시지마다 · 새 이벤트 · 푸시 종류 없음) · 새 1:1 = `chat_room` · 경로 69 → **70** · API 18 → 19 · 오류 코드 20 → 21 · 법적 검토 주석 5 그대로
- **화면** §10.14 전달 시트: 폰 바텀 시트 · 패드 가운데 · 머리 「공유」(사용자 말) · 검색(이름 · 방 · **초성** — 규칙 · 전달 시트에만) · [전체][사람] · 칩 줄 · 「대화방」(내 방 − 비활성 상대 1:1) + 「직원」 · 동그라미 10 · [전송] · 결과 토스트 3가지 · 네트워크 실패 = 시트 남김 + 같은 `clientId` · 「전달됨」 없음
- **걷어냄**: iOS 시스템 공유 · `share_plus` · `chat_share.dart` 공유 부분 · `_share` · `_shareVideo` · `chatVideoDownload` · 공유 시험 — 지우지 않고 ~~취소선~~(D-56 · OQ-956 닫힘)
- D-65: SPEC-007 §10.15 「이 판에서 같이 고침」 + SPEC-004 §6.5 한 줄 · 코드 자리 §12.3 R4-A12

## 검증

### DEC D-01 ~ D-65 → SPEC (부록 A)

- 부록 A 행 = **65 / 65** (`sed -n '/^## 부록 A/,/^## 부록 B/p' spec-007… | grep -oE "^\| (~~)?D-[0-9]+" | grep -oE "D-[0-9]+" | sort -u | wc -l` = 65) · 본문 D9-01 ~ D9-65 각 grep 0 인 것 없음(반복 grep · 「missing」 출력 0)
- 뒤집힌 줄: **D-56 = 행 통째 ~~취소선~~ + 「뒤집힘(r4 · D-62)」** · 본문 §1.2 · §9.1 · §9.3 · §10.7 · §10.13 #16 · C16 · OQ-956 취소선 / 고친 줄: D-36(키보드 · D-61) · D-47(D-60) · D-52(90MB · D-58) · D-17(파일 = 마지막 참조 · D-64) · D-24(공유 임시 파일 예외 없어짐)

### 피드백 F1 ~ F9 → SPEC (부록 C) = **8 / 8**(F8 취소 표시)

### 처분 문서 3개 → SPEC (부록 D) = **23 / 23**

| 문서 | 줄 | SPEC 반영 | D9-62 로 없어진 것 |
|---|---|---|---|
| `r3-dispositions.md` | 13 | 13 | U-4(동영상 공유 흘려 받기) · U-5(「파일에 저장」 알림) |
| `app-fix-r2-instructions.md` | 7 | 7 | W-7(공유 [취소] 시험) |
| `app-fix-r3-instructions.md` | 3 | 3 | — |

### §12.3 다시 grep — 216b154 (코드 워크트리 `/Users/kknaks/orca/workspaces/cc-prototype/internal-chat` · `git rev-parse --short HEAD` = `216b154` · 읽기만)

`procedure/` 에서:

| # | 명령 | 수 | §12.3 |
|---|---|---|---|
| G1 | `grep -n "@router\." back/app/api/chat.py` | 18 | R4-B9(19 로) |
| G2 | `grep -n -A1 "@router\." back/app/api/chat.py \| grep "^[0-9]*-def "` | 0 | 라우트 `async def` 유지 |
| G3 | `grep -rn "unlink(" back/app/service/chat.py` | 2 | R4-B6(`:407` delete) · `:568` = 동영상 올리기 실패 정리(안 바꿈) |
| G4 | `grep -rn "add_chat_photo\|update_chat_photo(" back/app` | 6 | R4-B2(repo 2) · R4-B3 · R4-B6(`:367` · `:400`) · 올리기 2(`:487` · `:562` 안 바꿈) |
| G5 | `grep -rn "def candidate\|tx.add_direct_room" back/app` | 2 | R4-B4 |
| G6 | `grep -n "CHAT_ROUTES\|def test_route_count\|== 18\|== 51" back/tests/test_order.py` | 5 | R4-B10 |
| G7 | `grep -rn "법적 검토 필요: 직원 채팅" back` | 5 | §14 그대로 5 |
| G8 | `grep -rn "share_plus\|SharePlus\|ShareParams\|CupertinoActivityType\|XFile(" app/lib app/pubspec.yaml` | 8 | R4-A1 · R4-A2(→ 0) |
| G9 | `grep -rn "shareText\|sharePhoto\|shareFileIn\|shareDir\|shareExcluded\|shareFailed\|_shareVideo\|chatVideoDownload\|chat-share-" app/lib` | 23 | R4-A1 · R4-A3 · R4-A5(→ 0) |
| G10 | `grep -rn "ChatMenu.share\|share(.공유" app/lib` | 4 | R4-A3(`:501`) · R4-A4(`:859` · `:870` · `:871` 그대로) |
| G11 | `grep -rn "openChatLink" app/lib` | 2 | R4-A1(남김 · `chat_room_screen.dart:983`) |
| G12 | `grep -rn "\.contains(q)" app/lib` | 1 | R4-A9(`chat_new_screen.dart:100` 안 바꿈 · OQ-961) |
| G13 | `grep -n "0.92\|sizeOf(context).height\|SheetHandle" app/lib/widgets/interpret_drawer.dart` | 4 | R4-A12(`:179` · `:192` · `:193` · `:200`) |
| G14 | `grep -rn "InterpretDrawer(" app/lib` | 2 | R4-A12(`room_screen.dart:85` 확인만 · 생성자 `:24`) |
| G15 | `grep -rn "share\|Share" app/test/chat_app5_test.dart` | 39 | R4-A10 |
| G16 | `grep -rn "otherEvents" app/lib/sse/board_stream.dart` | 2 | R4-A11(안 바꿈) |
| G17 | `grep -n "viewInsets" app/lib/screens/shell.dart` · `grep -n "maxInputLines\|keyboardDismissBehavior" app/lib/screens/chat_room_screen.dart` | 2 · 3 | R4-A13(동기 · 안 바꿈) |
| G18 | `grep -rn "maxVideoMs\|VIDEO_MAX_BYTES\|maxVideoBytes" app/lib back/app` | 12 | R4-B12 · R4-A13(동기 · 안 바꿈) |
| G19 | `grep -n "PHPhotoLibraryPreventAutomaticLimitedAccessAlert" app/ios/Runner/Info.plist` · `grep -n "audioSave\|audioFollowSilent\|audioRestore" app/ios/Runner/AppDelegate.swift` | 1 · 5 | R4-A13(동기) |

빠진 자리 확인: 위 grep 에 나온 줄은 모두 §12.3 한 행에 들었거나 「안 바꿈」으로 적었다(G3 `:568` · G4 올리기 2 · G10 메뉴 3 · G14 생성자).

### 그 밖

- 표 칸 수 검사(코드 · `\|` 뺀 `|` 수가 머리와 다른 줄) — SPEC-007 · WORK-011 = 0
- public grep(`sk-` · `AKIA` · 개인 키 머리 · 회사 메일 · 전화 · 팀 id 값) — SPEC-007 · WORK-011 = 0 · SPEC-004 = 2(`APNS_TEAM_ID` **env 이름**만 · 예전부터 · 값 아님)
- frontmatter: SPEC-007 `version: 0.4.0` · `status: draft` · `sources` 에 D-65 · F5 ~ F9 · r3-dispositions · app-fix-r2 · r3 · `a6c4123` = `216b154` 더함 · WORK-011 `sources` 2줄 더함
- ⚠ `python3 scripts/lint-pipeline.py --strict` — **이 워크트리에 파일이 없다**(r3 때와 같음) → pending

## 이 문서가 고른 기본값 (전부 §15 OQ · 확정 아님)

| OQ | 기본값 | 다른 안 |
|---|---|---|
| OQ-957 | 전달 첨부 = 새 행 + 같은 파일 · 마지막 참조에 파일 지움 · 인덱스 1 | (가) 원본 행 공유 → 권한 규칙 바꿔야 · 원본 지우면 전달본도 깨짐 ✗ (나) 서버가 파일 복사 → D9-64 「같은 파일」과 다름 · 볼륨 × 10 |
| OQ-958 | 대상마다 `clientId` · 일부 · 전부 실패 = 200 + 대상별 결과 · 오류 코드 1개 | 요청 `clientId` 하나 + 서버가 대상별로 지어 붙임(64자 한도 · 다시 보내기 규칙이 따로 생김) |
| OQ-959 | 같은 방 두 번 = 한 번만 · 결과 토스트 3가지 · 네트워크 실패 = 시트 남김 · 보낸 뒤 원래 대화에 머묾 | 대상 방으로 옮김(카톡은 머묾) |
| OQ-960 | 시트 꼴(폰 바텀 · 패드 가운데 · 머리 「공유」 · 두 묶음 · 그 사람의 1:1 이 있어도 직원 묶음에 보임 · [공유] 아이콘 `ios_share` 그대로) | 1:1 있는 직원은 직원 묶음에서 숨김 · 아이콘 바꿈 |
| OQ-961 | 초성 검색 = 전달 시트에만 | 새 대화 · 참여자 추가 검색에도 — **사용자 판단 자리**(D-63 은 전달 시트만 말함) |

## 미결 · 주의점

- **D-17 읽는 법(OQ-957)**: D-17 「사진 파일도 지운다」를 「그 메시지 첨부를 지운다 · 파일은 마지막 참조와 함께」로 읽었다. 원본만 지운 사용자는 「내 사진이 서버에 아직 있다」가 된다(전달받은 사람 방에서 계속 보이므로). 사용자 지시(「원본을 지워도 전달본 파일은 남아야」)와 같은 방향이라 기본값으로 뒀다 — DEC 에 한 줄로 올릴지 코디 판단
- 받는 쪽에서 「전달됨」이 없어 **남의 메시지를 전달하면 보낸 사람 = 나**로 보인다(D-64 그대로) — 의도된 것 · E2E C18 에서 사용자가 보게 됨
- 빌드 12 사용자는 back r4 배포 뒤에도 [공유] = 시스템 시트(옛 코드) — 빌드 13 업데이트까지(WORK-011 주의 r4)
- `share_plus` 를 빼면 `ios/Podfile.lock` 이 바뀜 — APP6 커밋 범위에 넣음
- SPEC-004 §6.5 는 브리프대로 줄을 더했고(머리 「(높이 92%)」는 그대로 둠) 다른 곳은 안 고쳤다 — SPEC-004 버전 · 변경 표는 안 올림(이 줄만이라는 지시)
- lint 스크립트 없음 → pending(r3 와 같음)

```text
$ git -C /Users/kknaks/orca/workspaces/kknaks_profile/cc-내부채팅 status --short
```
(아래 「status」 절 참고 — 보고 직전 출력)

## status

```text
 M orchestration/config/projects/cc-prototype.json
 M para/projects/summer-star/cc-prototype/00-baseline/README.md
 M para/projects/summer-star/cc-prototype/10-decision/README.md
 M para/projects/summer-star/cc-prototype/20-spec/README.md
 M para/projects/summer-star/cc-prototype/20-spec/spec-004-procedure-app.md
 M para/projects/summer-star/cc-prototype/30-work/README.md
 M para/projects/summer-star/cc-prototype/deploy.md
 M para/projects/summer-star/cc-prototype/log.md
?? orchestration/roles/cc-prototype/designer/
?? orchestration/work/internal-chat/
?? para/projects/summer-star/cc-prototype/00-baseline/baseline-010-internal-chat.md
?? para/projects/summer-star/cc-prototype/10-decision/decision-009-internal-chat.md
?? para/projects/summer-star/cc-prototype/20-spec/spec-007-internal-chat.md
?? para/projects/summer-star/cc-prototype/30-work/work-011-internal-chat.md
```
