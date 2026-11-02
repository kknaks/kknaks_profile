# 내부 채팅 — Mattermost 참고 조사 + procedure 에 붙일 자리 (researcher 리포트)

- 조사 날짜: 2026-10-29
- Mattermost: `github.com/mattermost/mattermost` `master` 얕은 클론 · 커밋 `8a53d645decc` (2026-10-28) · 레포 밖 임시 폴더에서 읽음. 아래 `MM:` 경로는 그 레포 루트 기준
- procedure 코드: `/Users/kknaks/git/toy_pr2/cc-prototype/procedure` HEAD `dbf0b53` (2026-10-28 · PR #16 머지) · read-only. 아래 `P:` 경로는 `procedure/` 기준
- SPEC: `para/projects/summer-star/cc-prototype/20-spec/spec-004-procedure-app.md` (아래 `SPEC-004 §`)
- 결정은 하지 않았다. 갈림길은 §6 「정할 것」에 모았고, §5 매핑은 **초안**이다
- 공식 문서 URL 을 직접 확인하지 못한 항목은 「문서 URL 미확인 — 코드 근거만」으로 적었다

---

## 1. Mattermost 라이선스 (사실만)

| 대상 | 라이선스 | 근거 |
|---|---|---|
| 서버 소스(`server/` 중 아래 예외 빼고) | **AGPL v3.0** 또는 상용 라이선스 중 하나 | `MM:LICENSE.txt:9-12` · GitHub API `repos/mattermost/mattermost/license` → `NOASSERTION`(단일 SPDX 아님) · https://github.com/mattermost/mattermost/blob/master/LICENSE.txt |
| `server/public/`(모델 `model/*.go` 가 여기) · `server/templates/` · `server/i18n/` · `webapp/` | **Apache 2.0** | `MM:LICENSE.txt:14-15` |
| AGPL 비강제 약속 | 「Mattermost 플랫폼에 직접 링크하지 않고 Admin Tools·Configuration Files 만 쓰며, 수정·파생본을 만들지 않으면」 copyleft 를 집행하지 않는다 | `MM:LICENSE.txt:17-20` |
| 컴파일된 배포판 | MIT | `MM:LICENSE.txt:5` |
| 모바일 앱(`mattermost/mattermost-mobile`, 별도 레포) | **Apache 2.0** | GitHub API `repos/mattermost/mattermost-mobile/license` → `Apache-2.0` · https://github.com/mattermost/mattermost-mobile/blob/main/LICENSE.txt |
| 상표 | 「Mattermost」 이름 사용은 사전 서면 승인 필요 | `MM:LICENSE.txt:22-26` · https://mattermost.com/trademark-standards-of-use/ |

- 이 조사에서 참고한 **모델 정의**(`Channel` · `ChannelMember` · `Post` · `FileInfo` · 웹소켓 이벤트 이름 · 푸시 모델)는 전부 `server/public/model/` = Apache 2.0 구역에 있다(`MM:server/public/model/channel.go` · `channel_member.go` · `post.go` · `file_info.go` · `websocket_message.go` · `push_notification.go`)
- **흐름**(DM 재사용 · 읽음 · 삭제 · 푸시 판단)은 `server/channels/app/` · `server/channels/store/` = AGPL 구역에 있다. 이 리포트는 그 코드를 옮기지 않고 동작만 요약했다
- 「개념·스키마 모양을 따라 쓰는 것」이 AGPL 파생물에 해당하는지는 **라이선스 문서에 없음** → §6 정할 것 L-1

---

## 2. 데이터 모델 요약 — 우리 범위(1:1 · 그룹 · 텍스트 · 사진 · 안 읽음 · 내 메시지 삭제)에 필요한 것만

### 2.1 `Channel` (`MM:server/public/model/channel.go:85`)

| 필드 | 줄 | 뜻 | 우리 범위 |
|---|---|---|---|
| `Id` | 86 | PK | 필요 |
| `Type` | 91 · 값 28-31 | `O` 공개 · `P` 비공개 · `D` 1:1 · `G` 그룹 DM | `D` · `G`(또는 `P` — §3.3 참고) |
| `Name` | 93 | 유일 이름. **D = 두 user id 를 정렬해 `a__b`**(`channel.go:621-626`) · **G = 정렬한 id 들의 sha1**(`channel.go:645-654`) | 1:1 재사용 키로 필요 |
| `DisplayName` | 92 | 표시 이름. G 는 정렬한 username 을 `, ` 로 이음(`channel.go:628-643`) | 그룹방 이름 — §6 C-1 |
| `CreateAt` · `UpdateAt` · `DeleteAt` | 87-89 | 밀리초 시각 · `DeleteAt` = 보관(archive) | `CreateAt` 필요 · `DeleteAt` §6 C-6 |
| `LastPostAt` | 96 | 마지막 글 시각 — 방 목록 정렬 · 읽음 처리 기준 | 필요 |
| `TotalMsgCount` | 97 | 방 전체 글 수 — 안 읽음 = 이 값 − 멤버 `MsgCount` | 필요(또는 시각 비교로 대체 — §3.6) |
| `CreatorId` | 99 | 만든 사람 | 그룹 방장 여부에 따라 — §6 C-2 |

뺌: `TeamId`(팀 없음) · `Header` · `Purpose` · `Props` · `SchemeId`(권한 스킴) · `GroupConstrained` · `Shared`(원격 공유) · `PolicyID` · `Policy*`(접근 정책) · `BannerInfo` · `AutoTranslation` · `*Root`(스레드 — 스레드 없음) · `Discoverable` · `*CategoryName`(사이드바 분류) — 이유: 팀·권한 스킴·스레드·연합 기능이 범위 밖.
그룹 인원: `ChannelGroupMinUsers = 3` · `ChannelGroupMaxUsers = 8`(`channel.go:38-39`).

### 2.2 `ChannelMember` (`MM:server/public/model/channel_member.go:55`)

| 필드 | 뜻 | 우리 범위 |
|---|---|---|
| `ChannelId` · `UserId` | 복합 키 | 필요 |
| `LastViewedAt` | 마지막으로 본 시각(밀리초) | 필요 — 사용자 기본값 「방마다 `last_viewed_at`」 |
| `MsgCount` | 마지막으로 봤을 때의 방 `TotalMsgCount` | 안 읽음 계산 방식에 따라 — §3.6 |
| `MentionCount` | 안 읽은 멘션 수(앱 배지 원천 — §3.9) | 멘션 없음 → 뺌 후보 |
| `NotifyProps` | 방별 알림 설정(push · desktop · mark_unread 등 · 값 검증 `channel_member.go:211-240`) | 음소거를 넣으면 `push` 한 칸만 — §6 P-3 |
| `Roles` · `SchemeAdmin` | 방 안 역할(방 관리자) | 방장을 두면 필요 — §6 C-2 |

뺌: `MentionCountRoot` · `MsgCountRoot` · `UrgentMentionCount`(스레드·긴급 멘션 없음) · `SchemeGuest` · `SchemeUser` · `ExplicitRoles`(권한 스킴 없음) · `LastUpdateAt`(캐시 무효화용) · `AutoTranslationDisabled`.

### 2.3 `Post` (`MM:server/public/model/post.go:143`)

| 필드 | 줄 | 뜻 | 우리 범위 |
|---|---|---|---|
| `Id` | 144 | PK | 필요 |
| `ChannelId` · `UserId` | 151 · 150 | 방 · 보낸 사람 | 필요 |
| `Message` | 155 | 본문. 최대 길이 `PostMessageMaxRunesV2 = 65535/4`(`post.go:78-79`) | 필요 — 길이 §6 M-1 |
| `CreateAt` · `UpdateAt` | 145-146 | 생성 · 마지막 변경(삭제도 `UpdateAt` 을 올림 — §3.7) | 필요 |
| `DeleteAt` | 148 | 0 이 아니면 지운 글(소프트 삭제) | 필요 |
| `FileIds` | 166 | 붙은 파일 id 배열(JSON 길이 300자 한도 `post.go:74` · 검사 `post.go:619`) | 사진 붙이기에 필요 |
| `Type` | 161 | 빈 값 = 일반 글 · `system_join_channel` · `system_leave_channel` · `system_add_to_channel` · `system_remove_from_channel` 등(`post.go:36-46`) | 참여자 추가·나가기 시스템 글을 남기면 필요 — §6 C-4 |
| `PendingPostId` | 167 | 클라이언트가 만든 임시 id — 같은 값으로 다시 보내면 서버가 중복 생성 안 함(`MM:server/channels/app/post.go:129-167`) | 재전송 중복 방지에 필요 후보 — §6 M-3 |

뺌: `RootId` · `OriginalId` · `ReplyCount`(스레드 없음) · `EditAt` · `MessageSource`(수정 없음) · `IsPinned` · `HasReactions`(반응 없음) · `Hashtags` · `Props`(첨부 카드·웹훅 등 — 단 삭제자 기록이 `Props.deleteBy` 에 들어감 §3.7) · `RemoteId`(연합) · `Metadata`(임베드·미리보기 묶음).

### 2.4 `FileInfo` (`MM:server/public/model/file_info.go:58`)

| 필드 | 줄 | 뜻 | 우리 범위 |
|---|---|---|---|
| `Id` | 59 | PK | 필요 |
| `CreatorId` | 60 | 올린 사람 | 필요(붙이기 권한 검사) |
| `PostId` | 61 | 붙은 글 — 올릴 땐 비어 있고 글을 만들 때 채움(§3.5) | 필요 |
| `ChannelId` | 66 | 방 — 열람 권한 = 방 멤버 | 필요 |
| `CreateAt` · `DeleteAt` | 67 · 69 | | 필요 |
| `Path` · `ThumbnailPath` · `PreviewPath` | 70-72 | 저장 경로 — **응답에 안 싣는다**(`json:"-"`) | 필요(우리도 경로 비공개) |
| `Size` · `MimeType` · `Width` · `Height` | 75-78 | 크기 · 형식 · 픽셀 | 필요(앱이 자리 잡기) |
| `HasPreviewImage` | 79 | 미리보기 있음 | 썸네일 정책에 따라 — §6 F-3 |
| `MiniPreview` | 80 | 아주 작은 흐린 미리보기 바이트(목록 즉시 표시용) | 뺌 후보 — §6 F-3 |

뺌: `Name` · `Extension`(사진만 · 이름 무작위) · `Content`(본문 검색 추출) · `RemoteId` · `Archived` — 이유: 범용 파일·검색·연합 범위 밖.

---

## 3. 동작 흐름 (Mattermost)

### 3.1 1:1 만들기 — 있으면 재사용
- `GetOrCreateDirectChannel` 이 먼저 두 사람의 기존 D 방을 찾고 있으면 그대로 돌려준다(`MM:server/channels/app/channel.go:405-413`). 없으면 `createDirectChannel`(`channel.go:498`) — 이름은 두 id 정렬 `a__b`(`model/channel.go:621-626`)라 같은 쌍은 늘 같은 방
- 새로 만들면 두 사람에게 웹소켓 `direct_added`(`model/websocket_message.go:29`)
- 공식 API: `POST /api/v4/channels/direct` — https://api.mattermost.com/ (문서 URL 의 절 이름은 미확인 — 코드 근거만)

### 3.2 그룹 만들기
- `createGroupChannel`: 인원 3~8 밖이면 400(`channel.go:626-628`) · 이름 = 정렬 id sha1 · 표시 이름 = username 나열 · 타입 G(`channel.go:666-668`) · 저장(`channel.go:672`)
- **같은 사람 묶음이면 기존 G 방을 돌려준다**(저장 충돌 → `ChannelExistsError` → `CreateGroupChannel` 이 그 방 반환 — `channel.go:688-689` · `601-606`)
- 만든 뒤 각 참여자에게 `group_added`(`channel.go:611-616`)

### 3.3 참여자 추가 · 나가기 — **Mattermost 의 G/D 는 멤버가 고정이다**
- 멤버 추가 API 는 D·G 방이면 400 `add_user_to_channel.type`(`MM:server/channels/api4/channel.go:2586-2589`) · 멤버 일괄 설정도 400(`api4/channel.go:2845-2848`)
- 나가기(`LeaveChannel`)도 D·G 면 400 `leave.direct`(`app/channel.go:2911-2914`). 대신 사이드바에서 숨기는 것은 **사용자 설정**(`direct_channel_show` · `group_channel_show` — `model/preference.go:21-22`)이고 멤버는 그대로
- 사람을 더 넣으려면 G → 비공개 채널(P)로 바꾸는 별도 기능(`ConvertGroupMessageToChannel` — `app/channel.go:4346`)
- 추가·나가기가 되는 P 방에서는 시스템 글을 남긴다: `postLeaveChannelMessage`(`channel.go:2934` · 비동기 `2924-2928`) · `PostAddToChannelMessage`(`channel.go:2955`) · `postRemoveFromChannelMessage`(`channel.go:3006`) · 웹소켓 `user_added` · `user_removed`(`websocket_message.go:38` · `42`)
- **→ 사용자 요구(그룹 = 참여자 추가 · 나가기)는 Mattermost 의 G 가 아니라 P 동작에 가깝다.** §6 C-3

### 3.4 보내기
- `POST /api/v4/posts`(`api4/post.go:25`) → `CreatePost`(`app/post.go:172`). `PendingPostId` 가 이미 본 값이면 새로 만들지 않고 이전 글을 돌려준다(`post.go:129-167`)
- 저장 때 방 `LastPostAt` · `TotalMsgCount` 를 올린다(`MM:server/channels/store/sqlstore/post_store.go:325-330`)
- 저장 뒤 `handlePostEvents` → `SendNotifications`(`post.go:760` · `786`) 가 웹소켓 `posted` 와 푸시를 처리
- `posted` 페이로드: 글 JSON + `channel_type` · `channel_display_name` · `channel_name` · `sender_name` · `team_id` · `set_online` · 사진만이면 `image:"true"`(`app/notification.go:706-735`)

### 3.5 사진 올리기 — 두 단계
1. `POST /api/v4/files`(`api4/file.go:34`) — 방 업로드 권한 검사(`api4/file.go:145-146`) → `FileInfo` 행(`PostId` 비어 있음) + 파일 저장(`app/file.go:615` `UploadFile` · `652` `DoUploadFile` · `792` `UploadFileX`)
2. 글 만들 때 `file_ids` 로 붙인다 — `attachFilesToPost`(`app/post.go:580`) → `AttachToPost` 는 **`PostId` 가 비어 있고 `CreatorId` 가 보낸 사람인 파일만** 붙인다(`store/sqlstore/file_info_store.go:435-442`)
- 썸네일·미리보기는 **서버가** 만든다: 썸네일 120×100 · 미리보기 너비 1920 · JPEG(`app/file.go:44-46` · `1009-1014` · `1209-1251`) · 미니 미리보기(`file.go:1253-1260`)
- 열람: `GET /api/v4/files/{id}` · `/thumbnail` · `/preview`(`api4/file.go:35-38`) — 세션 필요
- 한도(설정 기본값): 파일 100MB · 이미지 해상도 7680×4320(`MM:server/public/model/config.go:2025-2031`)

### 3.6 안 읽음 · 읽음 처리
- 안 읽은 수 = `Channels.TotalMsgCount − ChannelMembers.MsgCount`(`store/sqlstore/channel_store.go:933` · `2287`)
- 읽음 처리 API: `POST /api/v4/channels/members/{user_id}/view`(`api4/channel.go:62`) → `ViewChannel`(`app/channel.go:3792`) → `MarkChannelsAsViewed`(`channel.go:3733`)
  - 안 읽은 게 있는 방만 골라(`channel.go:3742`) `UpdateLastViewedAt`: 멤버 `MsgCount = 방 TotalMsgCount` · `LastViewedAt = max(기존, 방 LastPostAt)` · 멘션 수 0(`channel_store.go:2875-2902`)
  - 웹소켓 `multiple_channels_viewed {channel_times}`(본인에게 — `channel.go:3771-3773` · `websocket_message.go:54`) → 같은 계정 다른 기기도 배지를 지운다
  - 그 방 푸시를 기기 알림 센터에서 지우라는 `clear` 푸시(`channel.go:3776-3777` · `app/notification_push.go:416` · `model/push_notification.go:20`)

### 3.7 삭제
- `DELETE /api/v4/posts/{id}`(`api4/post.go:27`). 본인 글 = `delete_post` 권한 · 남의 글 = `delete_others_posts`(`api4/post.go:830-845`)
- **소프트 삭제**: `DeleteAt = UpdateAt = 지금` · `Props.deleteBy` 기록(`store/sqlstore/post_store.go:1022-1025`)
- 붙은 파일도 지움(비동기 · `app/post.go:2282-2287`)
- 웹소켓 `post_deleted {post}`(일반 사용자에겐 가린 글 · 관리자에겐 원문 + `delete_by` — `app/post.go:3728-3737`)
- 지운 글 표시 문구: 문서에 없음(웹앱 영역 — 이번 조사 범위 밖)

### 3.8 페이지네이션
- `GET /api/v4/channels/{id}/posts`(`api4/post.go:34` · 처리 `271`) 쿼리 `since` · `before` · `after` · `page` · `per_page`(`api4/post.go:277-305`)
  - `since`(밀리초) = **그 뒤에 바뀐 글**(새 글 + 지운 글 · `UpdateAt > since` — `post_store.go:1518` · `1570`) → 재연결 뒤 놓친 것 메우기
  - `before` / `after` = 글 id 기준 `CreateAt` 앞/뒤(`post_store.go:1787`) → 위로 스크롤
  - 기본 60개 · 최대 200(`server/channels/web/params.go:19-20`)
- 안 읽은 곳 주변: `GET …/channels/{id}/posts/unread`(`api4/post.go:37` · `397`)

### 3.9 푸시 판단 · 내용
- `ShouldSendPushNotification`(`app/notification_push.go:679-725`): 받는 사람이 봇이면 안 보냄 → 알림 설정(사용자 · 방 `NotifyProps.push`)이 막으면 안 보냄(`727-`) → 상태가 막으면 안 보냄
- 상태 규칙(`notification_push.go:774-795`): 방해금지 · 부재중이면 안 보냄 · **지금 그 방을 보고 있고 최근 활동했으면 안 보냄**(`status.ActiveChannel != channelID` 또는 활동이 오래됨일 때만 온라인에서도 보냄 — `781-786`)
- 그룹 DM 은 사용자 설정이 「멘션만」이어도 모든 글을 알림으로 본다(`notification_push.go:738-740`)
- 내용 3단계(서버 설정 `PushNotificationContents` 기본 `full` — `model/config.go:2392-2393`): `full`(보낸이: 본문) · `generic`(「보낸이 님이 메시지를 보냈어요」류) · `generic_no_channel`(방 이름도 숨김) · `id_loaded`(기기가 서버에서 본문을 받아옴 · 라이선스 필요 — `notification_push.go:806-810`) — 값 정의 `model/config.go:77-82`
- 사진만 보낸 글은 「사진을 보냈어요」류 문구(`notification_push.go:325-331`)
- 페이로드 필드: `type`(`message` · `clear` · `update_badge` — `push_notification.go:19-21`) · `post_id` · `channel_id` · `channel_name` · `sender_name` · `badge` · `category`(`CAN_REPLY` — 알림에서 답장 `push_notification.go:30`) · `sound`(`push_notification.go:82-111`)
- 배지 = 모든 방 안 읽은 멘션 합(`store/sqlstore/user_store.go:1584-1600`)
- 문서: 푸시 내용 설정 공식 문서 URL 미확인 — 코드 근거만

---

## 4. 우리 코드에 붙일 자리 (procedure)

### 4.1 SSE 허브 — **특정 계정 여럿에게 보내기: 이미 거의 된다**
- 지금 모양: 허브가 연결마다 `(account_id, device_id?)` 를 붙여 둔다(`P:back/app/service/stream.py:28-32`). `publish()` = 모든 연결 `board`(49-57) · **`send_to_account(account_id, event, data)` = 그 계정 연결만**(59-61) · `send_to_device`(63-65) · 새 이벤트엔 `id:` 없음 · version 안 올림(1-4 · 24-25)
- `stream()` 이 토큰 검증 계정 · 확인된 기기를 넘긴다(`P:back/app/api/board.py:22-34`)
- 「여럿에게」는 지금 **계정 하나씩 부르는 루프**로 된다. 한 번에 받는 함수(`send_to_accounts`)는 없다 → 채팅 붙일 때 루프로 쓰거나 함수 하나 더 (바뀔 곳)
- 연결 목록은 메모리 · 프로세스 1개(`stream.py:4`)
- 이벤트 배선 예: `notifications.on_new` → `hub.send_to_account(.., "notification", {unread})`(`P:back/app/container.py:57-60`)
- 앱 SSE 파서는 `board` 밖 이벤트를 **`display` · `notification` 두 이름만 통과**시킨다(`P:app/lib/sse/board_stream.dart:157-161`) → 채팅 이벤트 이름을 여기 더해야 한다 (바뀔 곳). 받는 쪽 분기는 `AppState._onStreamEvent`(`P:app/lib/app_state.dart:91-100`)
- **앱은 백그라운드로 가면 SSE 를 닫는다**(`app_state.dart:431-438` · SPEC-004 §7.1 「앱 생명주기」) → 백그라운드 새 메시지는 푸시가 유일한 신호 · 앞으로 오면 놓친 것을 REST 로 메워야 함(Mattermost `since` 와 같은 자리 — §3.8)
- 웹 SSE(`hooks.ts`)는 `board` 만 듣는다(SPEC-004 §7.1) → 이벤트를 더해도 웹은 안 깨짐

### 4.2 APNs — **계정별 발송: 이미 한다**
- 받는 계정 → 그 계정 기기 전부: `tx.devices_of(account_ids)`(`P:back/app/repository/repo.py:368-373`) · 상담사 호출이 「계정 1명 → 기기들」 예(`P:back/app/service/push.py:123-136`)
- 발송 단위 `Delivery`(`push.py:33-48`) · 커밋 뒤 이벤트 루프 태스크(`push.py:175-187`) · 재시도 1회 · 죽은 토큰 삭제 · `push_log` 기기마다 1행(`push.py:224-245` · `151-159`)
- `push_log.kind` 는 `doctor_call | counselor_call | display`(`P:back/app/repository/db.py:152-163` 의 `kind` 열 · SPEC-004 §5-2) → 채팅 kind 를 더해야 함. 열에 `CHECK` 는 없음(TEXT · 기본값만) (바뀔 곳)
- 알림 목록 `notification` 표 · 설정: 종류가 `doctor_call` · `counselor_call` 둘로 고정(`P:back/app/service/notifications.py:16-23` · SPEC-004 §5-4 「종류는 둘뿐」) → 채팅 푸시가 이 목록·종 배지에 들어가는지 §6 P-4
- APNs 요청 헤더가 고정: `apns-push-type: alert` · `apns-priority: 10` · **`apns-expiration: 0`**(`P:back/app/push/apns.py:48-51`). 0 = 기기가 꺼져 있으면 APNs 가 저장하지 않음(늦은 원장 호출은 무의미하다는 기본값 — SPEC-004 §5-1.2). 채팅은 늦어도 의미가 있음 → §6 P-5. `apns-collapse-id` · `thread-id` 를 넣는 자리도 없음 (바뀔 곳)
- 앱 푸시 받기: `kind` 로 분기 · **모르는 kind 는 `doctorCall` 로 보고 `visitId` 가 없으면 버린다**(`P:app/lib/push/push.dart:12` · `25-40`) → 채팅 kind 를 더해야 누르면 방으로 감 (바뀔 곳)
- 앱이 앞에 있을 때 iOS 배너: `display` 말고는 **늘 배너 + 소리**(`P:app/ios/Runner/AppDelegate.swift:141-162`) → 지금 보고 있는 방의 메시지도 배너가 뜬다. 서버가 안 보내거나(Mattermost 방식 — 보고 있는 방을 서버가 앎) 앱이 앞에서 거르거나 §6 P-2 (바뀔 곳)
- 앱 아이콘 배지는 안 쓴다(SPEC-004 §5-1.3 · §5-4 D7-42) → 채팅 배지 §6 P-6

### 4.3 사진 저장 · Bearer 열람
- 폴더 `PROC_PHOTO_DIR`(`P:back/app/config.py:65` · SPEC-004 §2.3) — 비면 사진 저장 끔
- 저장: `PROC_PHOTO_DIR/<token_hex(16)>.jpg` 바로 쓰기 + `id_photo` 행(`P:back/app/service/id_photo.py:49-63`) · 한도 `MAX_BYTES = 5MB`(`id_photo.py:35`)
- 업로드 API: multipart · Content-Length 로 5MB 먼저 거름 · **메모리에서만 읽도록 spool 한도를 프로세스 전역으로 올림**(`P:back/app/api/photos.py:19-20` · `37-44`) — 채팅 업로드도 같은 `MultiPartParser` 전역 값 영향을 받음
- 열람: `GET /api/id-photos/{id}` · Bearer 헤더만(쿠키·`?token=` 없음) · `Cache-Control: no-store` · 열 때마다 `event_log`(`photos.py:54-58` · `id_photo.py:110-125`) · `Authorization` 처리 `P:back/app/api/deps.py:17-24`
- 바뀔 곳: 채팅 사진은 신분증과 성격이 달라(법적 검토 문구 · 열람 로그 · `no-store`) **같은 폴더/표를 쓸지 하위 폴더·새 표인지**, 열람 권한 = 방 멤버 검사 — §6 F-1 · F-4
- 앱: 사진 고르기 패키지 없음(`P:app/pubspec.yaml:30-43` — `image_picker` 류 없음) · `Info.plist` 에 카메라 문구만 있고 **사진 보관함(`NSPhotoLibraryUsageDescription`) 문구 없음**(`P:app/ios/Runner/Info.plist:69-70`) → 앨범 선택을 넣으면 둘 다 더해야 함. multipart 보내기 예 `P:app/lib/api/api.dart:160-162` · Bearer 붙이는 공통 요청 `api.dart:33-36`
- 앱 이미지 표시: 지금은 `Image.memory` 만(`P:app/lib/screens/scan_screen.dart:286`) — Bearer 가 필요해서 `Image.network` 를 그대로 못 씀(헤더를 실을 수는 있음) · 캐시 정책 §6 F-5

### 4.4 표 만드는 방식
- 시작 때 `CREATE TABLE IF NOT EXISTS` 묶음 실행 → `MIGRATIONS`(표·열·타입 목록 — 없는 열만 `ALTER TABLE ADD COLUMN`) → `push_log` 재생성 단계(`P:back/app/repository/db.py:206-218` · 목록 `193-202`)
- 새 표는 `APP_SCHEMA` 같은 묶음 문자열에 더하는 꼴(`db.py:166-190`) · SQLite · 요청 하나 = 트랜잭션 하나(`db.py:222-234`)
- 채팅이 얹히면: 새 표 3~4개(방 · 멤버 · 메시지 · 사진) 를 새 묶음으로 · 기존 표 변경은 없음(단 `push_log.kind` 값 · `notification.kind` 값은 열 추가 없이 값만 늘어남)
- 경로 수 시험이 있다(SPEC-004 §7.3 `test_route_count_49`) → 채팅 API 수만큼 다시 셈 (바뀔 곳)

### 4.5 인증 · 역할
- 토큰 검증 = 서명·만료 + 계정 `active` + 역할·staffId 가 DB 지금 값과 같아야(`P:back/app/service/auth.py:83-101`) · 의존성 `Actor`(`deps.py:17-24`)
- 역할 다섯(`P:back/app/domain/models.py:29-39` · SPEC-004 §3.4 「새 API 는 다섯 역할 모두 ○」)
- **계정 목록 API 가 없다** — `GET /api/auth/accounts` 는 공개 계정 목록 제거로 없앰(SPEC-004 §3.3 · A-16). 채팅 상대 고르기엔 로그인 필요한 계정 목록 API 가 새로 필요 (바뀔 곳)
- **`account` 행에는 로그인 못 하는 계정이 많다**: 의사·상담사는 KOS 직원 한 명당 1행이지만 비밀번호는 PoC 1명씩만 · 나머지는 `password_hash` 없음(SPEC-004 §3.1 · §3.7 · `db.py:42-48`) · 빠진 직원은 `active=false` → 상대 목록에 누구를 보일지 §6 A-1

### 4.6 앱 탭 틀
- 탭 = `enum AppTab { reservations, visits, board, settings }`(`P:app/lib/app_state.dart:20`) · 이름·아이콘 맵(`P:app/lib/screens/shell.dart:14-26`) · 뿌리 화면 `_root`(`shell.dart:67-72`) · 탭마다 자기 Navigator(`shell.dart:35`) · 폰 탭바 `_TabBar`(130) · 태블릿 레일 `_Rail`(163)
- SPEC-004 §6.8: 폰 4칸 · 태블릿 레일 4개 · 공통 헤더(종 배지) · 「모든 역할 같은 4탭」 → 「채팅」을 더하면 5칸 · 순서 · 탭 배지 §6 U-1
- 띄우기 화면 동안 탭·헤더 숨김 규칙(SPEC-004 §6.8 「숨김」)이 채팅 배너에도 적용될지 §6 U-2

---

## 5. 매핑 표 — **초안 (결정 아님)**

| Mattermost | 우리 표 (초안) | API (초안) | SSE 이벤트 (초안) | 푸시 (초안) |
|---|---|---|---|---|
| `Channel` D | `chat_room(id, kind='direct', direct_key='<작은id>:<큰id>' UNIQUE, created_at, last_message_at)` | `POST /api/chat/rooms/direct {accountId}` → 있으면 그 방 | (새 방이면 상대에게) `chat_room` | — |
| `Channel` G(→ 사실상 P) | `chat_room(kind='group', title?, created_by, …)` | `POST /api/chat/rooms {accountIds[], title?}` | `chat_room` | — |
| `ChannelMember` | `chat_member(room_id, account_id, joined_at, left_at?, last_viewed_at, muted?)` PK(room, account) | `GET /api/chat/rooms`(내 방 + 안 읽음 수 + 마지막 메시지) · `POST /api/chat/rooms/{id}/members {accountIds[]}` · `POST /api/chat/rooms/{id}/leave` | `chat_member {roomId, added?, removed?}` | — |
| `Post` | `chat_message(id, room_id, account_id, kind='text'|'photo'|'system', body, photo_id?, client_id? UNIQUE, created_at, deleted_at?)` | `GET /api/chat/rooms/{id}/messages?before=<id>&limit=` · `?since=<시각>`(바뀐 것 — 새 글·지운 글) · `POST …/messages {body?, photoId?, clientId}` · `DELETE /api/chat/messages/{id}` | `chat_message {roomId, message}` · `chat_message_deleted {roomId, messageId}` | 새 메시지 · 그 방 멤버 중 보낸이 빼고 |
| `FileInfo` | `chat_photo(id, account_id, room_id?, message_id?, file_name, bytes, width?, height?, sha256, thumb_file?, created_at, deleted_at?)` | `POST /api/chat/photos`(multipart · 방 id) → `{photoId}` · `GET /api/chat/photos/{id}`(Bearer · 방 멤버만) · `…/thumb`? | — | — |
| view channel | `chat_member.last_viewed_at` 갱신 | `POST /api/chat/rooms/{id}/read` | `chat_read {roomId, lastViewedAt}`(같은 계정 다른 기기 · 다른 사람의 「읽음」 표시는 없음) | (선택) 알림 센터 지우기 — §6 P-7 |
| unread | `COUNT(chat_message WHERE created_at > last_viewed_at AND account_id != 나 AND deleted_at IS NULL)` 또는 `total/msg_count` 카운터 | 방 목록 응답의 `unread` | `chat_message` 를 받으면 앱이 +1 | — |
| push | `push_log.kind = 'chat'` · `chat_message_id?` 열(또는 기존 열 재사용) | — | — | `{aps:{alert:{title:<보낸이 또는 방>, body:<본문 또는 「사진」>}, sound, thread-id:<roomId>}, kind:"chat", roomId, messageId}` |

허브 쪽 초안: 방 멤버 계정 id 들을 읽어 `send_to_account` 루프(§4.1). 앱 쪽 초안: `board_stream.dart:158` 허용 이름에 채팅 이벤트 추가 · `push.dart` `PushKind.chat` · `AppTab.chat`.

---

## 6. 정할 것 (갈림길 — Mattermost 선택 + 코디 기본값 후보 1개)

| # | 갈림길 | Mattermost 의 선택 (근거) | 코디 기본값 후보 |
|---|---|---|---|
| L-1 | Mattermost 를 개념·스키마 모양만 참고하는 것이 라이선스상 괜찮은가 | 모델은 Apache 2.0 구역 · 흐름은 AGPL 구역(§1). 「아이디어 참고」 판단은 라이선스 문서에 없음 | 코드 복사 0 · 이름·필드도 우리 말로 새로 짓는다 · 리포트처럼 출처만 남김 |
| A-1 | 상대 목록에 누구를 보이나 | 팀 멤버 전원(DM 제한 설정 `RestrictDirectMessage` — `app/channel.go:415`) | `active` 이고 **로그인 가능(`password_hash` 있음)** 한 계정만 · 나 빼고 |
| A-2 | 상대 목록 API 의 노출 범위(공개 목록을 A-16 으로 없앤 이력) | 세션 필요 API | 로그인 필요 · `{id, name, role}` 만 |
| A-3 | 계정이 비활성(`active=false`)이 되면 그 사람의 방·메시지 | 비활성 사용자 글은 남음(문서에 없음 — 코드 미확인) | 메시지·멤버 행 유지 · 이름 옆 「(비활성)」 · 새 방 상대에서 빠짐 |
| C-1 | 그룹방 이름 | G 는 참여자 이름 자동 나열(`model/channel.go:628-643`) · P 는 직접 지음 | 만들 때 선택 입력 · 비면 참여자 이름 나열(앱이 그림) |
| C-2 | 방장(관리자)이 있나 | G 는 방장 없음 · P 는 채널 관리자 역할(`SchemeAdmin`) | 방장 없음 — 누구나 추가 가능 · 내보내기(강퇴) 없음 |
| C-3 | 그룹 = G(멤버 고정) 인가 P(추가·나가기) 인가 | G 는 추가·나가기 400(§3.3) | 사용자 요구대로 추가·나가기 되는 방 = P 동작 |
| C-4 | 참여자 추가·나가기를 대화에 남기나 | P 에서 시스템 글(`system_add_to_channel` 등 · §3.3) | 시스템 메시지 1줄(「A 님이 B 님을 초대했어요」 · 「A 님이 나갔어요」) |
| C-5 | 나간 방 기록 — 다시 초대되면 옛 메시지를 보나 · 나간 사람 행을 남기나 | 나가면 멤버 행 삭제 · P 는 다시 들어가면 전부 보임(문서에 없음 — 코드 미확인) | `left_at` 으로 남기고 목록에서 숨김 · 다시 초대되면 전부 보임 |
| C-6 | 같은 사람 묶음으로 그룹을 또 만들면 | G 는 기존 방 반환(`channel.go:601-606`) | 매번 새 방(이름이 다를 수 있으므로) · 1:1 만 재사용 |
| C-7 | 1:1 을 「나가기」 하면 | 나가기 400 · 숨기기 설정만(`preference.go:21-22`) | 목록에서 숨김(내 쪽만) · 새 메시지 오면 다시 보임 |
| C-8 | 마지막 사람이 나간 그룹방 | 문서에 없음 | 행 남김 · 아무 데도 안 보임 |
| C-9 | 그룹 인원 한도 | G 3~8(`model/channel.go:38-39`) | 2~20(내부 인원 규모) — 또는 한도 없음 |
| M-1 | 텍스트 길이 한도 | 16383자(`post.go:78-79`) | 2000자 |
| M-2 | 사진 + 글을 한 메시지에 | 한 글에 파일 여러 개 + 본문(`FileIds`) | 메시지 1개 = 텍스트 **또는** 사진 1장 |
| M-3 | 재전송 중복 방지 | `PendingPostId`(§2.3) | 앱이 만든 `clientId` UNIQUE |
| M-4 | 지운 메시지 표시 | 소프트 삭제 + `post_deleted`(§3.7) · 표시 문구 문서에 없음 | 소프트 삭제 · 자리에 「삭제된 메시지예요」 · 사진 파일도 지움 |
| M-5 | 삭제 시한 | 권한으로만 · 시한 설정은 문서에 없음 | 시한 없음 · 내 메시지만 |
| M-6 | 보존 기간 | 데이터 보존 정책은 엔터프라이즈 기능(`Channel.PolicyID` — `model/channel.go:106`) | 지우지 않음(PoC · `id_photo` D7-55 와 같은 결) |
| M-7 | 페이지 크기 | 기본 60 · 최대 200(§3.8) | 50 · 위로 스크롤 = `before` · 재연결 = `since` |
| F-1 | 사진 저장 자리 | 파일 저장소 + `FileInfo` | `PROC_PHOTO_DIR/chat/` 하위 폴더 + 새 표 `chat_photo`(신분증 `id_photo` 와 분리) |
| F-2 | 원본 크기 제한 | 100MB · 해상도 7680×4320(§3.5) | 앱이 긴 변 2048px JPEG 로 줄여 올림 · 서버 한도 5MB(지금 `MAX_BYTES` 와 같게) |
| F-3 | 썸네일을 서버/앱 어디서 | 서버가 썸네일 120×100 · 미리보기 1920 · 미니 미리보기(§3.5) | 서버 썸네일 없음 — 앱이 줄인 1장만 저장 · 목록은 같은 파일을 작게 그림 |
| F-4 | 사진 열람 권한 · 로그 | 방 멤버(세션) | 방 멤버(나간 사람 제외?) · Bearer · `event_log` 안 남김 |
| F-5 | 앱 캐시 | 문서에 없음(모바일 앱 영역) | 앱 메모리 캐시만 · 디스크 저장 안 함 |
| F-6 | 카메라 사진을 기기 사진첩에 저장하나 | 문서에 없음 | 저장 안 함(여권 스캔과 같은 결) |
| P-1 | 푸시 대상 | 방 멤버 · 보낸이 제외 · 설정·상태 판단(§3.9) | 방 멤버(나간 사람 제외) · 보낸이 제외 · 기기 있는 계정 |
| P-2 | 그 방을 보고 있으면 | 서버가 `ActiveChannel` 로 판단해 안 보냄(`notification_push.go:781-786`) | SSE 가 열려 있고 그 방을 보고 있으면 앱이 앞 배너를 거름(서버는 늘 보냄) — 또는 서버가 「보고 있는 방」을 알게 하기 |
| P-3 | 방별 음소거 | 방 `NotifyProps.push`(§2.2) | 방마다 알림 끄기 1칸 · 기본 켬 |
| P-4 | 채팅 푸시가 알림 목록·종 배지(§5-4 「종류는 둘뿐」)에 들어가나 | 알림 목록 개념 없음 · 방 배지만 | 안 들어감 — 채팅 탭 배지로 따로 |
| P-5 | `apns-expiration` | 문서에 없음(푸시 프록시 영역) | 채팅은 0 이 아니게(예: 1일) · 원장 호출은 그대로 0 |
| P-6 | 앱 아이콘 배지(지금 안 씀) | 안 읽은 멘션 합(§3.9) | 계속 안 씀 · 채팅 탭 배지만 |
| P-7 | 읽으면 다른 기기 알림 센터의 그 방 알림을 지우나 | `clear` 푸시(§3.6) | 안 지움(PoC) |
| P-8 | 잠금 화면 내용 | 기본 `full`(본문까지) · `generic` 선택 가능(§3.9) | 보낸이 이름 + 본문 앞 일부 · 사진은 「사진」 — 고객 정보 우려가 있으면 `generic` 쪽 |
| P-9 | 알림에서 바로 답장 | `CAN_REPLY` 카테고리(§3.9) | 없음 |
| P-10 | 같은 방 알림 묶기 | 문서에 없음 | `thread-id = roomId` |
| U-1 | 탭 위치 · 배지 | (해당 없음) | 5번째 「채팅」(설정 앞) · 탭에 안 읽은 방 합 배지 |
| U-2 | 띄우기(문진·스캔) 화면 중 채팅 배너 | (해당 없음) | 지금 규칙대로 숨김 |
| U-3 | 「읽음」 표시(상대가 읽었나) | 다른 사람 읽음 표시 없음 · 본인 `LastViewedAt` 만 | 없음(사용자 기본값 「메시지별 1 없음」 그대로) |
| U-4 | 타이핑 중 표시 | `typing` 이벤트 있음(`websocket_message.go:17`) | 없음 |
| W-1 | 웹이 나중에 붙을 때 SSE | 하나의 웹소켓에 모든 이벤트 | 지금 `/api/board/stream` 에 채팅 이벤트 같이 · 웹은 `board` 만 들으므로 안 깨짐 — 또는 채팅 전용 스트림 |

---

## 7. 검증

- 모든 사실 줄에 `MM:` 파일:줄 · GitHub 라이선스 URL · `P:` 파일:줄 · `SPEC-004 §` 중 하나를 달았다. 공식 문서 URL 을 확인 못 한 곳은 「문서 URL 미확인 — 코드 근거만」 · 근거가 없는 곳은 「문서에 없음」으로 적었다
- Mattermost 코드 블록은 옮기지 않았다(파일:줄 + 요약)
- 결정 0 — §5 는 초안 표시 · 갈림길 41개는 §6

`git -C /Users/kknaks/orca/workspaces/kknaks_profile/cc-내부채팅 status --short`:

```text
?? orchestration/work/internal-chat/
```

(작업 시작 때도 `orchestration/work/internal-chat/` 는 이미 untracked 였다 — 안에 `_RESUME.md` · `internal-chat-research-brief.md` 가 있었고, 이번에 생긴 것은 `research-mattermost-report.md` 1개.)
