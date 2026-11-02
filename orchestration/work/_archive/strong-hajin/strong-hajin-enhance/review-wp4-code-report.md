# 코드 검수 — WORK-012 WP4 (BE + FE) + SHELL 011

- 검수자: reviewer(read-only) · 2026-10-07
- 대상: 코드 워크트리 `strong-hajin-enhance` 의 **WP3 커밋 `cfc2e1c` 뒤 미커밋 변경 전부**
  - 수정 41파일(+1414/−59) · 새 파일 6(SQL 2 · `message_context.py` · 시험 3)
- 리포트 경로: 지시서 본문은 `review-wp1-code-report.md` 지만 코디 메시지대로 `review-wp4-code-report.md` 에 쓴다
- 계약
  - WORK-012 「Phase WP4-BE」·「Phase WP4-FE」·「Phase SHELL」(011)
  - SPEC-008 v0.6.0 §2.8 · §2.9 · §4.4 · §4.8 · §5
  - `wp4-contract-fixed.md` 1
- 워커 리포트: `be-wp4-report.md` · `fe-wp4-report.md` · `fe-shell-report.md`
- 한 일: diff 핵심 경로 읽기 · `rg` 재확인. **시험·빌드·cargo·실물은 돌리지 않았다** — 워커 수치:
  - BE contract 462+15 · postgres 51
  - FE 21파일 461/464(실패 3 = 기준선)
  - cargo 72 · 91
  - `shell-verify-strict` 통과
- 지시서 물음 3·4 는 WP1 문구 그대로라 WP4 축으로 답하고, WP1 영역은 「건드렸나」 만 본다(§4).
- 약어: `B/` = `backend/src/ax_workspace/` · `F/` = `frontend/src/` · `S/` = `frontend/src-tauri/src/`

---

## 0. 판정 — **WARN**

체크박스는 BE 6/6 · FE 6/6 · SHELL 011 1/1 모두 구현됐다. 계약 고정 1(`turn_id`·`label`)은 양쪽이 같다.
특히 볼 것으로 꼽힌 항목도 모두 맞다:
- 참고 자료 나열 지점 다섯 · 남의 메시지 404 · 100줄 경계 · 스레드 전체 · 메일 안전본 글자
- `inbox.message_updated` 커밋 뒤
- 나간 방은 그 회원만 · 보관·삭제는 전부
- 호버 막대 규칙
- 셸 판정 순서

**FAIL 0 · WARN 6.** 가장 무거운 둘:
1. **업무 출처를 「그 대화의 가장 최근 메시지 참고 자료」 로 정한다**(시간·턴 제한 없음). 같은 대화에서 한참 뒤 만든 **다른 업무**도 그 메시지를 출처로 갖고 「업무 만듦」 수에 들어간다.
2. **운영 SQL 이 한 파일에 섞였다.** 운영 필수(칸 셋)와 운영 금지(트랜잭션 안 인덱스)가 한 파일이라, 통째로 돌리면 `tasks` 쓰기가 막힌다.

---

## 1. 계약 체크박스 — 구현 위치

### WP4-BE (6/6)

| 계약 | 구현 | 판정 |
|---|---|---|
| `inbox_message` 참고 자료 · 나열 지점 다섯 · 해석기 | 명령 모델 `B/modules/ax_execution/conversation_commands.py:20` · HTTP `B/entrypoints/http.py:438` · 해석기 `B/platform/conversations.py:1035-1061`(`_inbox_message` — 잘못된 id·남의 것·지운 방/연동 = `ConversationNotFound` → 404 · 판 ≠1 = 422 · `summary` 고정 글자) · 도구 설명 `tool_catalog.py:54` · FE `viewModels.ts:1041`<br>다시 셈: BE 나열 넷 + FE 하나 = 다섯 · 손 나열은 더 없음 | PASS |
| 맥락 조합 함수 하나 | `B/modules/external_channels/message_context.py` `MessageContextComposer.compose` — HTTP·대화를 모름<br>— 위아래 `AROUND_LINES=100` `:42` · 스레드 `:256`(상한 1000) · 이웃 조회 `:262`<br>— 줄 모양 + `target` · 원문 JSON 제외 · `render_slack_text` · 삭제/수정 표지<br>— 메일 = `safe_html_text` `B/modules/external_channels/inbox_html.py:368~`(소독본 `text_content` → **글자만** · `<details>`·`<style>`·`<script>` 제외 · 2만 자 — `<img>` 는 글자가 없어 원격·추적 이미지 주소가 실리지 않는다) | PASS |
| 프롬프트에 덩어리로 | 실행 직전 조합 → `context` `B/platform/conversations.py:335` → Codex `codex_cli.py:594` · Claude `claude_cli.py:360`(기존 한 줄 요약과 별도) · `label` 저장·응답 `:850` · `conversation_results.py:58` | PASS |
| 업무 출처 · `origin.message` · `made_task_count` | 칸 `persistence.py:939,974` · 기록 `B/platform/actions.py:729-767`(`_record_message_origin`) · 투영 `B/modules/work/application.py:196,2494,2522` · 수 = 업무만 `:269` → `inbox.py:585,622,649` · 이름 노출 = 메시지 주인이고 살아 있을 때만(BE 미결 2 — 배정받은 사람에게 채널 이름이 새지 않음) | PASS(W-1) |
| `inbox.message_updated` 커밋 뒤 | `B/bootstrap/application.py:1771-1801` — `_after_session_commit` 훅 → 새 세션에서 NOTIFY · 받는 사람 = 그 메시지 연동 주인 | PASS |
| 012 나간 방 | `B/modules/external_channels/sync.py:186-200,255-286~`<br>— 나감 = `member_left_channel` 은 `event.user`, `channel_left`·`group_left` 는 `authorizations[0].user_id` → **`slack_user_id` 가 같은 방만**<br>— 누구인지 모르면 무시 · 보관·삭제 = 그 `(team, channel)` 의 모든 방<br>— `set_room_access(ok=False)` → 즉시 `paused` + `integration.changed` · 같은 실행 재확인이 되살리지 않게 `_verified_this_run`<br>— 보강 `is_archived` `:514` | PASS(§3) |

### WP4-FE (6/6)

| 계약 | 구현 | 판정 |
|---|---|---|
| 호버 막대 | `F/features/inbox/RoomView.tsx` `MessageBar` `:147-160`(DS `IconButton` 아이콘만 · `role="toolbar"` · 툴팁 `data-tip`+CSS) · 로컬 줄 없음 · 막대가 있으면 행 `tabIndex=0`(`:focus-within`) · 슬랙 셋/카톡 둘 `:703` · 패널 안 AX 둘(스레드 아이콘 없음) `:533` | PASS |
| 답글 0개 스레드 | `rowActions.onThread` 조건 없음 `:703` | PASS |
| 메일 머리 | `MailView.tsx:366-375` | PASS |
| 서랍 + 참고 자료 | `App.tsx:313` `askAx(text, context)` → `chat.start()`(새 대화) → 보내기 · `InboxPage.tsx:221-230` `askFrom`(본문 넷 · `inbox_message` 판 1) | PASS |
| 출처 링크 · 「업무 만듦」 | 출처 행 `WorkModals.tsx:2176~` · 통로 `App.tsx:320,405` · 짚기 `RoomView.tsx:716~`(위로 3쪽까지) · 표지 `RoomView.tsx:374,378` · `MailView.tsx:366` · 사건 구독 `:648,528` · `MailView.tsx:297` | PASS(W-4) |
| 참고 자료 한 줄 | `F/features/chat/MessageList.tsx:251-269` — `inbox_message` · 같은 `turn_id` · `label` 있을 때만 · 서버 글자 그대로 · 합치기 키 `useConversations.ts:84` | PASS |

### SHELL 011

| 계약 | 구현 | 판정 |
|---|---|---|
| `about:blank`·`about:srcdoc` 허용 · 외부 차단·`/api/` 가로채기 그대로 | 판정 함수 `S/guard.rs` `navigation_verdict` — 셸 화면 → **빈 프레임 문서(`about` + `blank`/`srcdoc` 둘뿐)** → 허용 목록 밖 취소(http(s) 면 외부 열기) → 앱 origin `/api/` 가로채기 → 허용 · 창 훅 `S/lib.rs:435-462` 가 판정대로만 한다 | PASS — 옛 훅과 줄 단위로 대조했다. 다른 것은 ② 하나와 허용 로그 문구뿐. `about:config`·`data:` 는 여전히 취소(시험) |
| 주 프레임 `about:blank` 허용의 안전 근거(`fe-shell-report.md` §2) | 근거 넷 확인:<br>① 빈 문서라 외부 내용이 없다<br>② `about:` 문서는 `remote.urls`(운영 origin 하나)와 맞지 않아 커맨드 권한이 없다 — tauri ACL 이 원격 origin 으로 판정<br>③ 메일 iframe 은 `allow-top-navigation`·`allow-scripts` 없는 샌드박스라 최상위를 옮길 수 없다<br>④ 우리 웹은 주 프레임을 `about:` 로 보내지 않는다 | PASS(W-5 — 남는 비용 기록) |

---

## 2. Code Surface WP4 · SHELL — 다시 센 것

| 행 | 다시 센 것 | 판정 |
|---|---|---|
| 참고 자료 나열 지점 | BE `Literal[…]` 둘(`conversation_commands.py:20` · `http.py:438`) · 해석기 분기 · 도구 설명 · FE 타입 하나 — 다섯 다 닿음. `meetings/commands.py:116` 등 무관 자리는 그대로 | PASS |
| 프롬프트 자리 | `Context references authorized` 근처 Codex·Claude 두 곳에 메시지 덩어리 절 | PASS |
| 서랍 열며 보내기 | `askAx` 시그니처 · 메시지함 연결 · 오늘 화면 입구(참고 자료 없음) 그대로 | PASS |
| 메시지 행·스레드 | `Message`(막대·표지·강조) · `toLine`(`madeTaskCount`) · 패널 · `inbox.css` · 메일 머리 | PASS |
| 메시지 응답 | `inbox.py` 메일·방 메시지 뷰 `made_task_count` · 저장소 내부 함수 넷(공개 API 아님) | PASS |
| 업무 출처 | 확정 경로 · 투영 · 결과 타입 · 화면 출처 행 · 서랍 prop 셋 화면(내 업무·오늘·캘린더 — 표 밖, 맞음). 요청 상세 링크 없음(SPEC 은 업무 상세만) | PASS |
| 012 나간 방 | `sync.py` · `sync_store.py:133`(`slack_channel_rooms`) · `RoomState.slack_user_id` — 봉투 무변경 | PASS |
| SHELL 이동 허용 | `lib.rs` 훅 · `guard.rs` 판정 · 시험 `lib.rs:992-998` 개정 | PASS |
| 운영 인벤토리 | 8항목 패치(워커) | PASS |

---

## 3. 특히 볼 것 — 확인

| 물음 | 본 것 | 판정 |
|---|---|---|
| 맥락 모양 SPEC §4.8 | 줄 = `{at(+09:00), sender, text, attachments(이름), thread_reply_count}` + 고른 줄만 `target` · `{label, source, room, range, lines}` · blocks·reactions 없음(시험) | PASS |
| 메일 = 안전본 글자 | 위 표 — HTML·추적 이미지 주소 없음 | PASS |
| 운영 SQL ↔ ORM | 칸 셋 타입(UUID · UUID · VARCHAR(300)) · 부분 인덱스 이름·조건(`postgresql_where`) 일치 · FK 없음(의도 — 메시지는 소프트 딜리트) | PASS(파일 구성은 W-2) |
| `inbox.message_updated` 커밋 뒤 | 커밋 뒤 훅 · 롤백이면 안 나간다 | PASS |
| 나간 방이 다른 회원에게 새나 | 나감은 `slack_user_id` 가 나간 사람과 같은 방만 내린다. 다른 회원의 방은 그대로 팬아웃을 받는다(시험: 두 회원 대역 · 다음 이벤트는 남은 사람에게만)<br>**되살아남 걱정**(BE 미결 5): 실행마다의 재확인은 공개 채널에서 `is_member` 를 본다(`sync.py:519-522`) → 나간 사람의 방은 「보인다」 로 되살아나지 않는다. 비공개는 `conversations.info` 가 거절한다 | PASS |
| 호버 막대 | 로컬 줄 없음 · `:focus-within` · 패널 안 스레드 아이콘 없음 · 누를 때마다 `chat.start()` | PASS |
| SHELL | §1 | PASS |

---

## 4. 회귀 — WP1~3 영역

| 자리 | WP4 diff | 판정 |
|---|---|---|
| 받기·미리보기 주소 · `download=1` | `MailView.tsx`·`RoomView.tsx` 의 첨부 주소·`Thumb`·`downloadOf` 줄은 바뀌지 않았다(머리 단추·막대·표지만) | PASS |
| SVG · `_download` | `inbox_html.py` 는 `safe_html_text` 를 **더했을 뿐** 소독 규칙 무변 | PASS |
| `integration.changed` | 나간 방이 기존 `set_room_access` → `_changed` 를 탄다(모양 같음 · 1초 묶기 대상) | PASS |
| 회의·기한·「빠른 회의」 | diff 없음 | PASS |
| 셸 `/api/` 가로채기(앱 받기) | 판정 ④ 가 같은 `is_api_request(url, app_origin)` · 시험에 `?download=1` 가로채기 | PASS |

---

## 5. 시험이 계약을 잡나

| 시험 | 판정 | 비고 |
|---|---|---|
| `T/contract/test_inbox_message_context.py`(19) | 강함 | 404 넷 · 422 · 201줄 경계(가운데 `target`) · 첫머리·끝 · 답글 본문 제외 · 스레드 전체 · 메일(인용·HTML·스크립트 제외) · 멘션 풀기 · 출처·`made_task_count`·사건 · 요청+업무 · 메시지 없는 대화 |
| | **빈틈** | 같은 대화에서 **나중에 다른 업무**를 만들 때 출처가 붙는지(W-1)를 고정한 시험이 없다 |
| `test_external_sync.py` +9 | 강함 | 두 회원 팬아웃 · 같은 실행 재확인 · `authorizations` · 보관·삭제 넷 · `is_archived` |
| postgres 3 | 강함 | 운영 SQL 이 옛 DB 에 칸·인덱스(재적용) |
| FE `InboxPage.test.tsx` +12 · `App.test.tsx` +1 · `MessageListReferences.test.tsx` 3 · `TaskDetailDates.test.tsx` +3 | 강함 | 막대 아이콘·툴팁·tabindex · 0개 스레드 · 패널 안 · 로컬 줄 · 서랍 POST 본문+`context` · 사건 → 표지 · 짚기 · 한 줄 위치 |
| `S/guard.rs` 6 · `lib.rs` 정적 1 | 강함 | 순서·결과 · 비슷한 이름 origin · `data:`·`about:config` 취소 |

---

## 6. 사람 눈에 이상해 보일 자리

| # | 자리 | 무엇이 걸리나 |
|---|---|---|
| H-1 | **엉뚱한 업무의 「원래 메시지」** | 메시지로 연 대화에서 요약을 받은 뒤 같은 대화로 「다른 일 하나 만들어 줘」 → 그 업무 상세에도 「원래 메시지 · 슬랙 #…」 가 서고 그 메시지의 「업무 만듦」 이 는다(W-1) |
| H-2 | **참고 자료 한 줄이 늦게 선다** | `label` 은 **실행 직전 조합** 때 생긴다 → 보낸 직후 말풍선 아래가 비었다가 답이 오며 선다. 접수 직후에는 「무엇을 넘겼나」 가 안 보인다(계약대로 — `label` 없으면 줄 없음) |
| H-3 | **출처 링크로 갔는데 「찾을 수 없음」** | 짚기는 첫 페이지 + 위로 3쪽까지 — 오래된 메시지면 링크가 실패처럼 보인다(FE 미결 4) |
| H-4 | **오래 위로 올려 본 메시지의 「업무 만듦」** | 사건을 받으면 최신 페이지만 다시 읽는다 — 위에 읽어 둔 옛 메시지 표지는 방을 다시 열 때 선다(FE 미결 2) |
| H-5 | **툴팁이 DS 와 다른 모양** | DS 툴팁 부품이 없어 CSS `::after` — 다른 화면의 툴팁(있다면)과 글꼴·지연이 다를 수 있다 |
| H-6 | **나간 방 줄이 설정에 「접근 잃음」 으로 남음** | 사람이 다시 고를 때까지 되살아나지 않는다(SPEC 대로) — 다시 들어간 채널도 손으로 다시 골라야 한다 |
| H-7 | **(dmg) 주 프레임이 빈 문서가 되면** | 창이 하얗게 되고 절전 방지 점유가 풀린다 — 우리 웹이 그 길을 쓰지 않아 실제로는 드물다(W-5) |

---

## 7. FAIL / WARN 목록(재발주용)

### FAIL — 없음

### WARN (6)

| # | 팀 | 자리 | 무엇 | 권장 |
|---|---|---|---|---|
| W-1 | BE(+코디 판정) | `B/platform/actions.py:741-767` `_record_message_origin` | 출처 = 「제안 턴까지 그 대화의 가장 최근 `inbox_message` 참고 자료」 — 시간·턴 제한이 없어, 같은 대화에서 나중에 만든 무관한 업무도 그 메시지를 출처로 갖고 「업무 만듦」 수가 는다(BE 미결 1 · H-1) | 코디 판정: ① 참고 자료를 실은 턴 **이후 같은 「업무 생성」 흐름**(그 턴 ~ 제안 턴 사이에 다른 제안 확정이 없을 때)만 · 또는 ② 참고 자료 턴부터 N턴 이내 · 또는 ③ 지금대로(대화를 메시지마다 새로 여니 대개 맞다). 정한 뒤 시험 1 |
| W-2 | BE(운영) | `backend/migrations/manual/2026-10-07-inbox-message-origin.sql` | 운영 필수(칸 셋)와 운영 금지(트랜잭션 안 `CREATE INDEX` on `tasks`)가 **한 파일**이다. 머리 주석은 「운영에는 앞 세 줄만」 이지만 `psql -1 -f` 로 통째로 돌리면 `tasks` 쓰기가 막힌다. 앞 판들의 관례(`2026-09-28-w7-successor-index.sql` = 격리판은 「운영에는 쓰지 않는다」 · 칸 파일과 분리)와도 다르다 | 칸 파일(운영) · 인덱스 격리판 · `.concurrent.sql` 셋으로 가른다 — 또는 이 파일에서 인덱스 줄을 빼고 격리판을 따로 |
| W-3 | 코디(운영) | 슬랙 앱 이벤트 구독 7개 · scope | 운영 앱에 구독을 더해야 나간 방 이벤트가 온다. `channels:read`·`groups:read` 가 사용자 토큰에 없으면 재동의 | 반영 단계 체크리스트(BE 리포트 §2) |
| W-4 | FE | `RoomView.tsx` 사건 → 최신 페이지만 다시 읽기 · 짚기 3쪽 한도 | H-3 · H-4 | 2루프(경미) |
| W-5 | 문서·코디 | SHELL I-1 | 주 프레임 `about:*` 도 허용(프레임 구분 불가) — 근거 확인했다. 남는 비용 = 그 경우 창 빈 화면 + 점유 해제 | SPEC-006 「이동 허용」 개정에 「프레임 무관 허용 · 근거 넷」 기록(planner) |
| W-6 | BE | `B/platform/conversations.py:1048,1052` | 메시지 못 찾음을 `ConversationNotFound` 로 올려 404. 화면 쪽 말풍선 실패 문구가 「대화를 찾을 수 없습니다」 류면 사용자는 대화가 사라진 줄 안다(메시지가 지워졌는데) | 404 `detail` 에 메시지 쪽 문구 · 또는 FE 가 참고 자료 실패를 가려 보이기(경미 · 확인 필요) |

### 확인한 것 / 확인 안 한 것

- **확인한 것**
  - 계약 고정 1 양쪽 · 해석기·조합·기록·사건·나간 방·재확인 코드
  - 운영 SQL↔ORM
  - 셸 훅을 옛 코드와 줄 단위로 대조
  - 호버 막대·참고 자료 한 줄·`askFrom`
- **확인 안 한 것**
  - 시험·빌드·cargo 실행 · 실물 슬랙(나간 방 이벤트가 어느 쪽으로 오는지)·Gmail 글자 · dmg
  - 말풍선 실패 문구의 실제 모양(W-6)
