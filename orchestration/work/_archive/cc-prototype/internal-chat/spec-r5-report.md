# internal-chat planner r5 결과 보고

## 상태: done

## 수행 내용

- `para/projects/summer-star/cc-prototype/20-spec/spec-007-internal-chat.md` **0.4.0 → 0.5.0**(draft 그대로) · 바뀐 줄 끝 `(r5)` · 머리 변경 표 0.5.0 행 · frontmatter `sources` 에 D-01 ~ D-69 · F10 ~ F14 · 처분 문서 4개 · `b988f21` / `3ed1089` 더함
- `para/projects/summer-star/cc-prototype/30-work/work-011-internal-chat.md`: r4 WP 상태 끝 처리(BE4 · APP6 · REVIEW3 · SIM2 · DEPLOY13 = 끝 · E2E2 = 진행 중 → r5) · 계약 고정점 r5 4줄 · **WP-BE5 ∥ WP-APP7 → WP-REVIEW4 → WP-SIM3 → WP-DEPLOY14(빌드 14) → WP-E2E3** · 병렬 그림 · 주의 r5 4줄 · infra r5 = 변경 없음
- README · log · DEC · SPEC-004 **안 고침**(브리프 「할 것 3」)

### 동기(코드에만 있던 것 → SPEC)

| 원천 | SPEC 자리 |
|---|---|
| `r4-dispositions.md` 7줄(D-66 · W-3 ~ W-5 · OQ-959 ~ OQ-961) | 부록 A D-66 · §10.3 · §10.14(초성 세 곳 · 한 사람 한 번 · 일부 실패 = 시트 남김) · §15 OQ-959 · 960 · 961 **닫힘** · 부록 D.4 |
| `app-fix-r4`(W3-1 공용 `showAppSheet` · W3-3 보내는 중 안 닫힘) | §10.0 「공용 바텀 시트」 · §10.14 「틀」 · 「[전송]」 · 부록 D.5 |
| `be-fix-r4`(W3-2 전달 원본 확인 = 쓰기 잠금 안) | §5 「전달」 ① · §12.3 「r4 결과」 · §13.1 「전달 — 잠금」 · 부록 D.6 |
| `app-fix-r5`(F10 정렬) | §10.0 「머리 · 줄 정렬」 · §10.14 「틀」 · 부록 C F10 · 부록 D.7 |

또 고친 것: §6.2 표에서 #18 과 #19 사이 빈 줄 때문에 표가 끊겨 있던 것(r4 결함)을 붙였다.

### 새 계약

- **D-67 모아보기**: 새 API #20 `GET /api/chat/rooms/{roomId}/attachments?before=&limit=`(1 ~ 60 · 기본 60) → `{items:[Message], hasMore}`. 사진 · 동영상만, 최근 것이 위(커서 = 메시지 id), 지운 것과 경계 안의 것은 뺀다. 파일은 #14 · #17 · #18 로 연다. 방 정보 「사진 · 동영상」 줄은 §10.8, 격자 화면은 §10.16(3열 · 빈 상태 · 실패 · SSE 반영 · 아이패드는 방 정보 시트 안 · 메뉴 없음)
- **D-68 초대**: 이름을 [초대]로 바꿨다. **1:1 [초대]는 지금 쓰는 `POST /api/chat/rooms` 그대로**이고 새 경로를 만들지 않는다(근거 §4.7 ① ~ ⑤ · 다른 안 (가) 새 경로 (나) `fromRoomId`). 문구는 「A님이 B님을 초대했습니다」. 새 그룹에도 만든 사람의 초대 줄 하나가 붙는다. 옛 행은 그대로 둔다. 1:1 안내 줄은 없앴다(§4.4 · §4.7 · §10.9 · §10.17)
- **D-69 들어온 뒤 대화만**: 멤버 행에 **새 열 `from_message_id`** 를 둔다. 값은 들어올 때 방의 마지막 메시지 id이고, 그 멤버는 `id > from_message_id` 인 메시지만 본다(§3 r5 · §3.2 · §4.6). `joined_at` = 처음 · 다시 초대 · 방 만들 때 모두 그때 시각이다. 옛 DB는 열이 생기는 부팅에 한 번 `joined_at` 기준으로 채운다
  - **같은 밀리초**: 시각이 아니라 id로 가른다. 같은 밀리초에 먼저 커밋된 메시지는 숨고, 초대 줄은 보인다(§3 「왜 id 인가」 · 시험 §13.1)
- API 19 → **20** · 경로 70 → **71** · SSE 6 그대로(`chat_message_edited` · `chat_message_deleted` 받는 사람만 좁힘) · 오류 코드 21 그대로 · 법적 검토 주석 5 그대로

## 검증

### DEC D-01 ~ D-69 → SPEC (부록 A)

- 부록 A 행 = **69 / 69**(`sed -n '/^## 부록 A/,/^## 부록 B/p' spec-007… | grep -oE "^\| (~~)?D-[0-9]+" | grep -oE "D-[0-9]+" | sort -u | wc -l` = 69)
- 본문 D9-01 ~ D9-69 / D-01 ~ D-69 각각 grep 했을 때 0인 것 = **없음**(반복 grep · 「missing」 출력 0)
- 뒤집힘 · 고침 표시:
  - **D-12** 「다시 초대 = 옛 메시지」: 부록 A 칸에 ~~취소선~~ + 「일부 뒤집힘(r5 · D-69)」. §4.2 「다시 초대」 · §10.10 대화상자 · §13.1 「추가 · 나가기」 · C7 에 취소선
  - **D-11** 문구: 부록 A 「문구 고침」. §4.4 옛 줄은 통째 ~~취소선~~ 하고 새 줄 2개를 더했다
  - **D-02** 1:1 안내 줄: 부록 A 「일부 고침」. §10.8 1:1 안내 줄 ~~취소선~~
  - D-36 r5 줄 · OQ-913 「만들기 줄 없음」 ~~취소선~~

### 피드백 F1 ~ F14 → SPEC (부록 C) = **12 / 12**(F8 취소 · F12 안 함 표시 · 표 14줄)

### 처분 문서 → SPEC (부록 D) = r4 23 + **r5 14 / 14**(D.4 7 · D.5 2 · D.6 1 · D.7 4)

### D-69 읽기 길 전수 (SPEC §4.6 V1 ~ V12 · §12.4 R5-B1 ~ B17)

코드 워크트리 `/Users/kknaks/orca/workspaces/cc-prototype/internal-chat`(`git rev-parse --short HEAD` = `3ed1089` · 읽기만) · `procedure/` 에서:

| # | 명령 | 수 | 처리 |
|---|---|---|---|
| G1 | `grep -rn "FROM chat_message\|FROM chat_photo\|JOIN chat_message\|JOIN chat_photo" back/app` | **7** | 방 단위 질의 3개(`repo.py:743` · `:759` · `:765`) = R5-B4 · B3 · B8 · id 한 행 질의 4개는 호출 쪽(G2)에서 판정 |
| G2 | `grep -rn "\.chat_messages(\|\.last_chat_message(\|\.chat_unread(\|\.chat_message(\|\.chat_photo(\|\.chat_message_by_client(" back/app` | **23** | 서비스 21 + `push.py` 3 → R5-B3 · B4 · B6 · B8 ~ B10 · B12 · B14 · B15 각 행 |
| G3 | `grep -n '"chat_message"\|"chat_message_edited"\|"chat_message_deleted"\|"chat_room"\|"chat_read"\|"chat_room_removed"' back/app/service/chat.py` | **9** | `:527` · `:557` = R5-B13(받는 사람 좁힘) · `:154` = R5-B7 · `:275` · `:296` · `:368` = R5-B14(안 바꿈) · `:294` · `:308` · `:579` = 내용 없음 |
| G4 | `grep -n "@router\." back/app/api/chat.py` | 19 | → 20(R5-B16) |
| G5 | `grep -rn "joined_at\|from_message_id" back/app` | 3 | R5-B1 · B2 |
| G6 | `grep -rn "을 초대했어요\|참여자 추가\|그룹을 만들어요\|다시 초대받으면" back/app app/lib` | 14 | 문구 5(R5-B5 · A1 · A2 · A3) · 주석 · 로그 9 |
| G7 | `grep -n "test_route_count\|CHAT_ROUTES\|== 51" back/tests/test_order.py` | 4 | R5-B16 |
| G8 | `grep -rn "chatAddMembers\|addMembers(\|ChatPeopleScreen(" app/lib` | 8 | R5-A3 · A4 |
| G9 | `grep -rn "법적 검토 필요: 직원 채팅" back` | 5 | §14 5 그대로 |
| G10 | `grep -rn "초대했어요\|참여자 추가" app/test back/tests` | 8 | R5-B17(`test_chat.py:137` 「옛 메시지 보임」 단언 = 뒤집힘) · R5-A9 |

읽기 길 판정(V1 ~ V12 — 걸러야 할 곳 **8** · 안 바꿈 **4**):

| V | 길 | 판정 |
|---|---|---|
| V1 · V2 | 메시지 목록(처음 · `before`) · `since` | 거름(`id > from`) |
| V3 | 방 목록 미리보기 · SSE `chat_room` | 거름(`lastMessage` null) |
| V4 | 안 읽음 · `unreadRooms` | 안 바꿈 — 불변식 `last_read ≥ from`(시험) |
| V5 | 사진 · 동영상 · 썸네일 열기 | 거름(404) |
| V6 | 전달 원본 | 거름(404) |
| V7 | 모아보기 #20 | 처음부터 거름 |
| V8 | 내 옛 메시지 고치기 · 지우기 | 거름(404 · OQ-969) |
| V9 | SSE `chat_message_edited` · `chat_message_deleted` | 거름(받는 사람) |
| V10 | SSE `chat_message` · 푸시 | 안 바꿈 — 새 id 는 늘 경계 뒤 |
| V11 | 같은 `clientId` 다시 | 안 바꿈 — 내 UUID · 내 메시지 |
| V12 | 읽음 · 방 이름 · 멤버 · 열기 · 숨기기 · 알림 · 나가기 | 안 바꿈 — 내용 없음 |

**SSE 는 이미 멤버만인가?** 그렇다. 모든 채팅 이벤트는 `tx.chat_members()`(지금 멤버)에게만 간다. 다만 **지금 멤버여도 경계 안 메시지의 수정 · 삭제 이벤트가 간다**(V9 — 고친 본문이 샌다). 그래서 이 두 줄은 받는 사람을 좁혔다.

### 그 밖

- 표 칸 수 검사(코드 · `\|` 를 뺀 `|` 수가 머리와 다른 줄): SPEC-007 · WORK-011 = **0**
- public grep(`sk-` · `AKIA` · 개인 키 머리 · 회사 메일 · 전화 · `TEAM_ID=`): SPEC-007 · WORK-011 = **0**
- frontmatter: SPEC-007 `version: 0.5.0` · `status: draft` · WORK-011 `status: draft` · `sources` 더함
- ⚠ `scripts/lint-pipeline.py` 는 이 워크트리에 없다(r3 · r4 와 같음) → pending

## 이 문서가 고른 기본값 (전부 §15 OQ · 확정 아님)

| OQ | 기본값 | 다른 안 |
|---|---|---|
| OQ-962 | 경계 = 메시지 id 열 `from_message_id` · 옛 DB = 첫 부팅 한 번 `created_at < joined_at` 의 마지막 id | `created_at >= joined_at` 시각 비교(같은 밀리초에 샘) · 옛 행 0(옛 멤버는 계속 전부 봄) |
| OQ-963 | 1:1 [초대] = 기존 #4 · **[새 대화] 그룹에도 초대 줄 하나** | (가) 새 경로 `rooms/{directId}/invite` (나) `fromRoomId` 필드 — **[새 대화] 그룹에 줄을 둘지가 사용자 판단 자리** |
| OQ-964 | 옛 「…초대했어요」 행은 그대로 | 마이그레이션으로 문구 바꿈 |
| OQ-965 | #20 = `Message` 재사용 · 최근 위 · 60 · 개수 없음 | 전용 `Attachment` 모양 · 전체 수 |
| OQ-966 | 모아보기 화면 = 알림 아래 줄 · 3열 · 날짜 묶음 없음 · 메뉴 없음 · SSE 반영 · 아이패드 시트 안 | 날짜 묶음 · 개수 표시 · 아이패드 가운데 창 |
| OQ-967 | 1:1 [초대] = 초대 화면 재사용 · 비활성 상대 = 숨김 · 만든 뒤 새 그룹으로 감 | 1:1 에 머묾 |
| OQ-968 | 나가기 문구 「… 다시 초대받아도 지금까지의 대화는 볼 수 없어요.」 | 옛 문구 그대로(D-69 와 어긋남) |
| OQ-969 | 다시 들어온 사람의 **자기 옛 메시지**도 안 보임 · 404 | 내 것은 늘 보임 |

## 미결 · 주의점

- **OQ-963 은 사용자 판단 후보**: D-68 「새 그룹은 만든 사람이 초대한 줄 하나」를 **[새 대화] 그룹에도** 적용했다(서버가 출처를 모르게 하려고). [새 대화] 그룹에서 줄을 빼려면 `fromRoomId` 같은 신호가 필요하다(§4.7 (나))
- **OQ-969 · 옛 DB 채우기(OQ-962)**: 운영 DB 에서 예전에 다시 초대된 사람은 배포 첫 부팅 뒤 옛 대화가 안 보이게 된다(D-69 의도와 같은 방향). 배포 전 WP-SIM3 에서 옛 compose 볼륨으로 1회 확인하도록 WORK 에 넣었다
- 나가기 대화상자 옛 문구가 뒤집힌 D-12 를 약속하고 있어서 바꿨다(OQ-968 · DEC 에는 문구가 없다)
- §4.5 미리보기 거르기는 지금 길로는 생기지 않는 경우다(들어올 때 초대 줄이 늘 경계 뒤에 붙음). 그래도 규칙과 코드 한 줄로 막아 두었다
- lint 스크립트 없음 → pending

## status

```text
$ git -C /Users/kknaks/orca/workspaces/kknaks_profile/cc-내부채팅 status --short
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
(이 판에서 고친 파일 = `spec-007-internal-chat.md` · `work-011-internal-chat.md` · 이 리포트 — 셋 다 미추적 상태)
