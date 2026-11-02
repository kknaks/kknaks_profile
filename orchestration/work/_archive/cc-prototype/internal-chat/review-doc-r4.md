# 리뷰 리포트 — internal-chat / doc r4 (2026-10-29)

대상: SPEC-007 0.4.0(`(r4)` 줄) · SPEC-004 §6.5 한 줄 · WORK-011 r4(BE4 ∥ APP6 → REVIEW3 → SIM2 → DEPLOY13 → E2E2) · `spec-r4-report.md`
기준: DEC-009 D-58 ~ D-66 · 운영 코드 `/Users/kknaks/orca/workspaces/cc-prototype/internal-chat` HEAD `216b154`(읽기만 · 직접 grep) · 처분 문서 3개
OQ-957 ~ 961 = 코디 기본값으로 받음 → FAIL 대상 아님(브리프)

## 판정: WARN

코드 워커가 추측으로 메워야 하는 빈칸 = **0**. 전달 계약 · D-66 파일 지우기 · 시스템 공유 걷어냄 · 처분 23줄 · D-65 · §12.3 이 모두 구현 가능하게 적혀 있다. 아래 WARN 5건은 가리킴 · 표기 · 시험 자리 보강이다.

대조 수치
- DEC D-58 ~ D-66 → SPEC: **8 / 9**(D-66 은 내용은 들어갔으나 번호 가리킴 0 — WARN-1)
- 처분 23줄 → SPEC 실제 위치: **23 / 23 들어감**(그중 1줄 가리킴이 틀림 — WARN-3)
- §12.3 코드 자리(R4-B1 ~ B12 · R4-A1 ~ A13 · R4-W1 = 26행) 216b154 직접 확인: **26 / 26** 맞음(줄 끝 2곳 몇 줄 어긋남 — 참고)
- planner grep G1 ~ G19(21개 수): **21 / 21** 같은 수
- 시스템 공유 · `share_plus` 남은 살아 있는 문장: **0**

## FAIL

없음.

## WARN

### WARN-1 · D-66 이 SPEC · WORK 에 번호로 없다 (추적)
- `spec-007-internal-chat.md:28` sources 「D-01 ~ D-65」 · `:71` 「D9-01 ~ D9-65」 · `:978` 부록 A 「65 / 65」 · `:973` OQ-957 = 「기본값」 그대로 · `work-011-internal-chat.md:103` REVIEW3 「부록 A(D-58 ~ D-65)」 — `grep -c "D9-66\|D-66"` SPEC-007 = 0 · WORK-011 = 0
- 근거: `decision-009-internal-chat.md:165` D-66(「D-17 을 읽는 법 … 파일은 마지막 메시지가 지워질 때」 — 근거 칸 「spec-r4 OQ-957」). DEC 가 planner 뒤(16:46 > SPEC 16:43)에 더해짐
- 내용은 같다: SPEC §5 「삭제」 `:276` · §3.4 `:205` · §9.2 「지우기」 `:435` · R4-B6 · §13.1 「첨부 · 지우기」 `:858` 가 D-66 과 한 글자도 어긋나지 않음 → 워커는 막히지 않음
- 권장: 부록 A 에 D-66 행(→ §3 r4 · §5 「삭제」 · §9.2 · R4-B6 · §13.1 · C18) · 「66 / 66」 · OQ-957 칸 「닫힘 → D9-66」 · sources · WORK REVIEW3 「D-58 ~ D-66」

### WARN-2 · §6.2 #19 행이 표 밖으로 떨어져 있다
- `spec-007-internal-chat.md:343` 빈 줄 → `:344` `| 19 | POST …/forward` 가 머리 · 구분 줄 없는 새 덩어리가 됨 → 렌더하면 #19 가 경로 표의 행이 아니라 문단으로 보인다. planner 「칸 수 검사 = 0」은 칸 수만 봐서 못 잡음
- 원문(md)을 읽는 워커는 막히지 않음 · 사람이 렌더본(GitHub · Obsidian)으로 볼 때 놓치기 쉬움
- 권장: `:343` 빈 줄 지움

### WARN-3 · 부록 D.1 #7 가리킴이 틀림 — 없는 키
- `spec-007-internal-chat.md:1111` 「§12.3 R4-A13(키 `chat-plus` · `chat-input` · `chat-send`)」 — R4-A13 행(`:817`)에 키 글자 없음 · 216b154 `grep -rn "'chat-plus'\|'chat-input'\|'chat-send'" app/lib` = 0
- 처분 원문(`r3-dispositions.md` W-7)은 「입력줄 키를 바꾸면 1판 시험을 APP4 에서 같이」 — 이미 끝난 일이라 R-A22(`:783`)만 가리키면 됨
- 권장: 키 이름 괄호 지움 또는 216b154 실제 키로

### WARN-4 · 전달 요청 단위 오류 차례가 한 줄로 안 정해짐
- `spec-007-internal-chat.md:345` 공통 차례 「401 → 400(요청 모양) → 404 → 403 → 409」 · `:344` #19 오류 칸은 400 `chat_not_forwardable`(의미 400) · 404 `chat_message_not_found` 를 나열만
- 나간 사람이 지운 메시지를 전달하면 404 인가 400 인가가 공통 줄만으로는 「400 먼저」로 읽힐 수 있다. §5 「전달」 ①(`:275`)은 원본 권한을 먼저 적고, OQ-903(존재는 멤버에게만)과 216b154 `delete`(`service/chat.py:388-395` — 404 → 403 → 지움 검사) 꼴로는 **404 먼저**가 맞음
- 권장: #19 에 「`invalid_request`(모양) → 404(원본 · 멤버) → 400 `chat_not_forwardable` → 409 `photo_disabled`」 한 줄. §13.1 「권한 · 모양」 `:855` 에 「나간 사람 + 지운 메시지 = 404」 한 칸
- 같은 결: 결과 `{ok:false, roomId|null}` — 방 대상 실패 = 요청한 `roomId` · 사람 대상 실패 = `null` 로 읽히나 명시 없음(`:313`) — 앱은 이 값을 쓰지 않아 막히지 않음

### WARN-5 · 앱 시험 픽스처가 §12.3 · WORK 대상에 없다
- 216b154 `app/test/chat_fixture.dart:86` `FakeChat` 이 채팅 경로를 손으로 흉내 냄(`:116-157` — rooms · people · direct · photos · videos · PATCH …) · `/forward` 가지 없음
- §12.3 R4-A10(`:814`)은 `chat_app5_test.dart` 만 · WORK APP6 대상(`work-011-internal-chat.md:102`)은 `test/`(새 전달 · 드로어 시험)로 넓게만 — r1 리뷰 때 「시험 픽스처」를 빠진 자리 갈래로 둔 것과 같은 자리
- 권장: R4-A10 · APP6 대상에 `test/chat_fixture.dart`(`FakeChat` 에 `POST /api/chat/messages/{id}/forward` · 대상별 결과 · 요청 기록) 한 줄. 같은 김에 `test/chat_app2_test.dart:399` · `chat_app4_test.dart:523` 의 「공유 없음」 단언(크게 보기 · 재생 화면 — 그대로 맞음)은 안 바뀐다는 확인 한 줄

## 볼 것별 결과

### 1. 전달 계약 `POST /api/chat/messages/{id}/forward` — PASS
| 항목 | 자리 | 판정 |
|---|---|---|
| 요청 `{targets:[{roomId,clientId}|{accountId,clientId}]}` 1 ~ 10 · 중복 roomId · accountId · clientId · 둘 다 · 둘 다 없음 · 모르는 키 = 400 | §6.1 `:311` · #19 `:344` · R4-B8(`schemas/chat.py:8-10` `_Req extra="forbid"` · `:133` `clientId Field(8,64)` 꼴 그대로) | PASS |
| 응답 대상 차례 · 일부 · 전부 실패 = 200 · `Result` 꼴 | `:312-313` · `:344` | PASS(WARN-4 끝 줄) |
| 권한: 원본 방 지금 멤버 · 남의 것 됨 · 대상 방 멤버 아님 404 · 비활성 1:1 409 · 후보 아님 400 | §5 ① ~ ③ `:275` · §13.1 `:855-856` | PASS(WARN-4 차례) |
| 1:1 새로 만들기 | §5 ② · R4-B4 — `open_direct` `:191-215` · `add_direct_room`(`repo.py:672-677` INSERT OR IGNORE → 같은 tx 안에서 안전) | PASS |
| `clientId` 대상마다 · 다시 보내기 | §5 ④ ⑤ · `post` `:353-355` `chat_message_by_client` 꼴 · `repo.py:726` | PASS |
| 첨부 새 행 + 같은 파일 · 인덱스 | §3 `:143-146` · §3.4 `:200` · `:205` · R4-B1 · B5 · `_attachment`(`:493-512`) 안 바꿈이 맞음(권한 = 행의 room_id · message_id) | PASS |
| **D-66 파일 지우기 ↔ 216b154 `delete`** | R4-B6: 216b154 `delete`(`service/chat.py:384-410`)는 tx 안에서 첨부 행 `deleted_at`(`:398-400`) → tx 밖 `:403-407` 에서 `file_name` · `thumb_file_name` 바로 `unlink`. SPEC = 「행 `deleted_at` 뒤 tx 안에서 `chat_photo_live_refs(file_name) == 0` 셈 → 커밋 뒤 0 일 때만 unlink(본 · 썸네일)」 — 지금 꼴(tx 안에서 읽고 tx 밖에서 지움)에 셈 1줄만 얹으면 됨 · 서비스 동기 + `async def` 한 스레드(§3 `:148`)라 셈과 지움 사이에 전달이 끼지 않음 · 썸네일은 전달본이 `thumb_file_name` 을 짝으로 복사(§3 `:143`)해 `file_name` 셈 하나로 충분 · 다른 지움 자리: `:568`(올리기 실패 — 새 이름만 · 안 바꿈 맞음) · `id_photo.py:176`(신분증 폴더 · 무관) — 216b154 `grep unlink\|rmtree\|os.remove back/app` 3곳 전부 확인 | **PASS** |
| SSE · 푸시 | §7 `:371` · `:374` · §8 `:390` · R4-B11(`push.py:167` · `:222` · `container.py:130-131` 확인) | PASS |
| 경로 70 | §6.4 `:362` · R4-B10(`test_order.py:248-278` · CHAT_ROUTES 18 · `== 69` 확인) | PASS |
| 오류 코드 21 · 문구 | §6.3 `:355` | PASS |

### 2. 전달 시트 화면 · 아이패드 — PASS
§10.14 `:628-648`: 틀(폰 바텀 · 패드 가운데 · [✕] · 「공유」 · [전송 N]) · 검색 · 초성 규칙(음절 → 초성 식 · 겹자음 · 이어진 자리 · 예 2개) · 칩 [전체][사람] · 고른 것 줄 · 「대화방」(#2 items − 비활성 1:1 = D-63 「나간 · 숨긴 빼고 · 최근 순」 + D-64 「비활성 1:1 뺌」과 같음) · 「직원」(#1 = D-05) · 10곳 · [전송] 요청 · 결과 토스트 3 + 요청 실패(4xx · 네트워크 · 401) · 보낸 뒤 머묾 · 「전달됨」 없음 · 보고 있는 방 아님. 아이패드 §10.11 `:591` · C18 `:892`. D-63 [최근 공유] · 아래 줄 없음 = `:637` · §10.13 #17 `:625`.

### 3. 시스템 공유 · share_plus 걷어냄 일관성 — PASS
`grep "공유 시트\|저장 빼\|share_plus\|saveToCameraRoll\|excludedCupertino\|파일에 저장\|준비하는 중\|팝오버"` 전 줄 확인 — 살아 있는 문장은 전부 「없음 · 걷어냄 · 뒤집힘」 뜻(§1.2 `:115` · §9.1 `:415` · §9.3 `:448` · §10.7 `:560-562` · §10.11 `:591` · §10.12 `:602` · §10.13 #16 · C16 · OQ-956 닫힘 · 부록 A D-56 행 취소선). §12.2 R-A16 · R-A19(`:777` · `:780`) · R-B13 「100MB」(`:756`)는 머리 `:738` 에 「이력」 표시가 있어 PASS. 크게 보기 · 재생 「저장 · 공유 버튼 없음」(`:541-542`)은 D-24 그대로라 맞음.

### 4. 처분 23줄 — 23 / 23 들어감
| 문서 | 줄 | 실제 자리 확인 |
|---|---|---|
| `r3-dispositions.md` | 13 | D-58 · 59 90MB · `Content-Length`(§1.1 · #16 `:340` · §6.3 · §9.2 `:429-430` · §13.1 `:851`) · FAIL-1 C8 `:882` · FAIL-2 §10.7 `:551` · W-4 `:852` · W-5 §5 `:274` · #15 `:339` · §13.1 `:850` · W-6 §5 `:283` · #15 · **W-7 = R-A22 에만 있음(WARN-3)** · W-8 §10.6 `:534` · U-3 §9.3 `:450` · §10.4 · U-4 취소선 `:560` · U-1 · U-2 C15 `:889` · U-5 C16 취소선 · W-1 ~ W-3 §12.3 실제 이름 |
| `app-fix-r2-instructions.md` | 7 | W-1 §9.2 `:426` · §10.6 · W-2 `:433` · W-3 · W-6 `:434` · W-4 `:432` · W-5 §9.1 `:419` · §10.6 `:537` · W-7 R4-A10 지움 |
| `app-fix-r3-instructions.md` | 3 | 알약 §10.4 · 수정 모드 알약 안 · 키보드 §10.1 · §10.4 · 시험 §13.2 r4 `:865` |

### 5. D-65 통역 드로어 — PASS
SPEC-004 §6.5 한 줄(`spec-004-procedure-app.md:654` — 놓인 칸 92% · 상태 표시줄 아래 · 손잡이 누름/끌어 내림 · 아이패드) · SPEC-007 §10.15 `:650-652`(`interpret_drawer.dart:179` · `:192-193`) · R4-A12 `:816`(216b154 `:179` `MediaQuery.sizeOf(context).height` · `:192` `-h * 0.92` · `:193` `h * 0.92` · `:200` `GestureDetector(onTap: _close, child: SheetHandle())` · 부르는 곳 `room_screen.dart:85` · 생성자 `:24` — 전부 일치) · 완료 조건 §13.2 r4 `:865` 통역 드로어 줄 · 스크린샷 `:866` · C19 · WORK APP6 대상 `lib/widgets/interpret_drawer.dart` · 검증 명령 `<새 드로어 시험>`(지금 드로어 시험 파일 없음 — 새로 만드는 것이 맞음).

### 6. §12.3 216b154 직접 grep — 26 / 26
R4-B1(`db.py:195-229` CHAT_SCHEMA · 인덱스 없음 · `MIGRATIONS` `:231-244`) · B2(`repo.py:761-769`) · B3(`post` `:329-382`) · B4(`:191-215` · `candidate` `:48` · `:199`) · B5 · B6(`:384-410` · unlink `:407`) · B7(`:493-512`) · B8(`schemas/chat.py:130-160`) · B9(`api/chat.py:107-111` · `@router.` 18) · B10 · B11 · B12(`api/chat.py:145-168` · `VIDEO_MAX_BYTES` `:40`) · A1(`openChatLink` `:22` · 쓰는 곳 `chat_room_screen.dart:983`) · A2(`pubspec.yaml:49` · `:50`) · A3(`:16` · `:501-502` · `_share` `:512` · `_shareVideo` `:526`) · A4(`:856-871`) · A5(`api.dart:375` · 쓰는 곳 = `_shareVideo` 뿐 — lib grep 1) · A6 · A7(`chat_state.dart:141` · `:400`) · A8 · A9(`chat_new_screen.dart:100`) · A10(`chat_app5_test.dart:90` · `:126` · `:225` · `:268-269`) · A11(`board_stream.dart:158`) · A12 · A13(`shell.dart:127` · `:139` · `:147` · `chat_room_screen.dart:37` · `:253` · `:633` · `Info.plist:71` · `AppDelegate.swift:344` · `:380` · `photo_pick.dart:133` · `:154` · `video_pick.dart:13` · `:73` · `:82` · `api.dart:306` · `:409-413`) · W1. G1 ~ G19 수 다시 셈 = planner 와 같음(18 · 0 · 2 · 6 · 2 · 5 · 5 · 8 · 23 · 4 · 2 · 1 · 4 · 2 · 39 · 2 · 2/3 · 12 · 1/5).

빠진 자리: `test/chat_fixture.dart`(WARN-5). `ios/Runner/GeneratedPluginRegistrant.m` · `ios/Flutter/ephemeral/…` 에도 `share_plus` 가 있으나 **git 추적 밖**(빌드 생성물 — `git ls-files` 0)이라 빠진 자리 아님. 추적되는 `pubspec.lock` · `ios/Podfile.lock` 은 R4-A2 · WORK 주의 `:144` 에 있음.

### WORK-011 r4 — PASS
WP 순서 BE4 ∥ APP6 → REVIEW3 → SIM2 → DEPLOY13 → E2E2(`:101-106` · 그림 `:119-120`) · 병렬 근거 = 계약 고정점 r4 3줄(`:80-82`) · 대상 파일 · 완료 조건 = §13.1 r4 4줄 · §13.2 r4 · 검증 명령 부분(`-k "chat or route_count …"` — 새 `test_chat_r4.py` 도 「chat」에 걸림) · 완료 = TestFlight 실기기 C1 ~ C20(사용자 표면) · infra 변경 없음 근거(`:49` — 파일 복사 0 · env · Secret · 경로 0 · D-59 배포 끝)가 SPEC §9.2 「볼륨」 `:436` 과 맞음.

### 보안 · 권한 — PASS
나간 사람 원본 전달 404 · 대상 방 멤버 아님 404 · 전달본 첨부 = 대상 방 멤버만(원본 방에만 있는 사람 404 — §13.1 `:858`) · 원본 지워도 원본 첨부 404 · Bearer 헤더만(#14 · #17 그대로) · 로그 id 만(R4-B5). 고객 정보가 전달로 더 퍼지는 것은 OQ-902(법적 검토 주석 5 그대로)에 이미 묶임.

### public — PASS
SPEC-007 · WORK-011 · SPEC-004 에 `sk-` · `AKIA` · 개인 키 머리 · 회사 메일 · 전화 · 팀 id 값 grep = 0 · 0 · 0.

## 조용히 통과하는 자리 (시험은 초록인데 계약이 깨질 수 있는 곳)
- **파일 지우기 셈을 서비스 시험만으로 보면** 「전달본까지 다 지움 → 파일 없어짐」이 통과해도, 썸네일만 남거나(셈을 `thumb_file_name` 으로 따로 하다 어긋남) 원본 지움에 전달본 썸네일이 지워지는 경우를 못 잡는다 — §13.1 `:858` 은 「본 파일 + 썸네일」을 같이 적었으니 REVIEW3 에서 **동영상 전달본으로** 시험했는지 볼 것
- **FakeChat 에 `/forward` 가 없으면** 앱 시험이 `chatForward` 를 따로 가짜로 바꿔 끼워 요청 본문(대상 차례 · 대상마다 `clientId` · 다시 보낼 때 같은 `clientId`)을 단언하지 않고 통과할 수 있다(WARN-5)
- **#19 SSE · 푸시 시험이 서비스 직접 부르기면** 216b154 의 「`async def` 아니면 푸시 0」 함정을 못 잡는다 — §13.1 `:857` 은 「HTTP 경로로」라고 적어 막아 둠 · REVIEW3 에서 확인

## 고객(사용자)이 실물에서 만날 자리
- 남의 메시지를 전달하면 받는 쪽에는 **보낸 사람 = 전달한 나**로 보이고 「전달됨」이 없다(D-64 그대로 · C18)
- 원본을 지운 사람에게는 전달본이 남아 있는 한 「내 사진이 서버에 아직 있다」(D-66 그대로)
- 일부 실패 토스트 「N곳에 보내지 못했어요」는 **어느 곳**인지 말하지 않고 시트가 닫힌다 — 다시 보내려면 처음부터 다시 고른다(OQ-959)
- 빌드 12 사용자는 back r4 배포 뒤에도 [공유] = 옛 시스템 시트(WORK 주의 `:142`)

## 사용자 판단 후보 (제품 동작이 눈에 보이게 갈리는 것)
| OQ | 지금 기본값 | 다른 안 | 왜 사용자 몫 |
|---|---|---|---|
| OQ-961 | 초성 검색 = 전달 시트에만 | 새 대화 · 참여자 추가 검색에도 | 같은 앱의 검색 세 곳이 다르게 동작 — planner 도 사용자 판단 자리로 표시 |
| OQ-960 | 1:1 이 있는 직원도 「직원」 묶음에 같이 보임(함께 고르면 하나로) | 1:1 있는 직원은 직원 묶음에서 숨김 | 시트에 같은 사람이 두 번 보임 |
| OQ-959 | 일부 실패 = 시트 닫고 「N곳에 보내지 못했어요」 | 실패한 곳만 남긴 채 시트 유지 | 실패한 곳을 사용자가 알 길이 없음 |

## 참고 (기존 부채 · 워커 영향 없음)
- R4-A1 `chat_share.dart:1-50` → 파일은 48줄 · R4-A3 `_share` · `_shareVideo` `:512-575` → 실제 끝 `:579` (지울 범위는 함수 단위라 영향 없음)
- `scripts/lint-pipeline.py` 이 워크트리에 없음 → pending(planner 리포트와 같음)

```text
$ git -C /Users/kknaks/orca/workspaces/kknaks_profile/cc-내부채팅 status --short
```
(아래 — 보고 직전 출력)

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
