# fix-spec-4 결과 보고 — 피드백 8 · 9 · 10 + 작업 계획 · Delivery #241 v2

## 상태: done

- 스펙: `mediness-mediness/fix-spec`(브랜치 `kknaksss/fix-app-re1-spec` · 1 ~ 3판 미커밋 위) · `products/day/` 만 · 커밋 · push · PR 0.
- 코드는 읽기만(`CENTURION_DAY/fix` · `kknaksss/fix-app-re1` · 미커밋 69파일 그대로).

## 바꾼 문서 · 절 (고친 뒤 줄)

| 문서 | 자리 |
|---|---|
| `20-spec/spec-004-internal-chat.md` | 머리 개정 ④ `:30` · 범위 「넣음」 읽음 표시 `:65` · 와이어 `:107`(숫자 `{n}` · 대화 화면 하단 4메뉴 없음) · U-2 하단 4메뉴 숨김 `:167` · U-2 메시지별 읽음 표시 `:181` · U-4 자리가 맞아야 한다 `:200` · §3 `Member` `:348` · 규칙 「읽음」 · 「읽음 표시 계약」 `:371` · 실시간 표 `chat_member_read` `:436` · 연결 직후 메우기 줄 · 케이스 매트릭스 3줄 `:475~` · 프로토와 다른 곳 2줄 `:554` · C-A11(7종) `:589` · C-A16 `:594` · 새 C-A22 ~ C-A25 `:600-603` · 새 OQ-C16 ~ C18 `:637-639` · OQ 절 머리 |
| `20-spec/spec-003-mobile-app.md` | 머리 개정 ⑩ `:53` · Placement 셸 줄 · U-2 「하단 메뉴 … 같은 4개」 예외 `:223` |
| `20-spec/spec-000-data-model.md` | 머리 2026-11-11 개정 ② `:31` · 07 `chat_member.last_read_seq` `:1130` · `from_seq` `:1131` |
| `log.md` | 1줄(4판) |

### 8 · 9 · 10 이 들어간 방식

- **8 길게 누르기(버그)** — U-4 에 **맞아야 하는 결과만**: 복사본 · 메뉴는 화면이 다시 잡힌 뒤(키보드가 닫힌 뒤 등) 그 말풍선의 실제 자리에 붙고, 메뉴는 안전 영역 밖으로 안 나감 · 키보드를 닫은 채 누른 지금 모양이 기준. 방법은 구현 몫. 코드 사실만 적음: 앱은 길게 누른 순간 자리를 한 번 재서 고정(`chat_room_screen.dart:446-448` · 다시 재지 않음). 원인 추측 없음. 수용 C-A22(실기기 = 그림 8 재현 안 됨).
- **9 하단 4메뉴(확정 변경)** — U-2 「하단 4메뉴는 그대로 보인다(프로토 탭바 유지)」 취소선 · 대체: 폰은 채팅 목록에서만 보이고 대화 화면(키보드 유무 무관)에서 숨김 · 아이패드 레일 그대로. 대화 위 채팅 화면(방 정보 · 모아보기 · 크게 보기 · 재생) · 목록 위 새 대화 · 초대까지 숨김 = **코디 · planner 기본값 OQ-C16**. 영향 자리 확인: 「보고 있는 방」 — 앱 `watching` 은 `chatTabActive`(지금 메뉴 = 채팅) 값으로 판정하고 탭 표시와 무관(`chat_state.dart:486-487`) → 그대로 선다고 적음 · 앱 안 배너(셸 맨 위 층) · 푸시로 들어오기 · 탭 배지 값 그대로(숨긴 동안 안 보일 뿐) · 키보드가 열리면 숨기는 지금 셸 동작(`shell.dart:302`)은 그대로 · SPEC-003 U-2 예외 한 줄 · C-A16 · 새 C-A23 · 와이어 · 프로토와 다른 곳.
- **10 읽음 표시(기능 추가)** — 사용자 확정(카톡식 · 안 읽은 사람 수 · 0 이면 사라짐)과 코디 기본값(내 · 남의 메시지 · 1:1 같음 · 세는 사람 = 볼 수 있는 지금 멤버 중 보낸 사람 빼고 · 나간 · 비활성 안 셈 · 시스템 · 지운 없음 = **OQ-C17**)을 구별해 U-2 에. 자리 · 색(시각 칸에서 시각 위 · `Ms.primary`) = **planner 기본값 OQ-C18**. 멤버 변동(초대 = 앞 메시지 안 셈 · 나가기 · 비활성 = 빠짐 · 비활성 전환은 다음 `GET /rooms` 때) · 재연결(`GET /rooms` 의 `members[]` 로 다시 셈) · 바꾸지 않는 것(목록 Badge · 탭 배지 · 푸시 · 배너 · #15 규칙)까지.

## 읽음 계약 — 어느 방식 · 왜

**앱이 센다 · 서버는 멤버 읽은 자리만 준다.**

- `Room.members[]` 의 `Member` 에 `lastReadSeq` · `fromSeq`(그 멤버의 기존 `chat_member.last_read_seq` · `from_seq`) — `Room` 이 나오는 모든 곳(목록 · 만들기 · 초대 · 이름 바꾸기 · `chat_room`).
- 새 이벤트 **`chat_member_read {roomId, accountId, lastReadSeq}`** 하나 — 읽음 #15 가 **실제로 올렸을 때만** · 커밋 뒤 · 그 방 지금 멤버 중 읽은 사람 아닌 계정(읽은 사람은 기존 `chat_read`). 묶기 = 앱 읽음 요청이 이미 방마다 1초 묶음 + 서버는 오를 때만 → 멤버당 많아야 초당 1번(서버 타이머 없음).
- 앱: 메시지마다 지금 멤버(≤ 20)를 훑어 셈 — 한 화면 메시지 × 20 이하.
- **다른 안을 안 고른 이유**: ㉠ 서버가 메시지마다 수 — 읽음 한 번에 그 방 여러 메시지의 고친 모양을 멤버마다 보내야 해 바꾸는 곳이 크다 ㉡ 읽음마다 `chat_room` — 받는 사람마다 `Room` 전체를 다시 만든다(최대 20명) ㉢ 기존 `chat_read` 재사용 — 「나만 · 내 `unreadRooms`」 이벤트라 뜻이 다르다. 고른 안은 **이미 있는 칸 · 쿼리(멤버 줄을 이미 읽음)에 칸 둘 + 작은 이벤트 하나**.
- **migration 없음**(칸이 이미 있음 · SPEC-000 은 설명만).

## 정할 것 (사용자 몫만)

새로 사용자에게 물을 것은 없다 — 8 · 9 · 10 의 핵심은 사용자 확정이고, 나머지는 기본값으로 적용해 통보만 한다:

| OQ | 기본값(뒤집을 수 있음) | 후보 |
|---|---|---|
| SPEC-004 OQ-C16 | 대화 + 그 위 채팅 화면 + 새 대화 · 초대 모두 하단 4메뉴 숨김 · 목록에서만 보임 | 대화 화면만 숨김 |
| SPEC-004 OQ-C17 | 내 · 남의 메시지 모두 · 1:1 같음 · 지금 활성 멤버만 셈 | 내 메시지에만 · 나간 사람도 셈 등 |
| SPEC-004 OQ-C18 | 시각 칸 시각 위 · `Ms.primary` | 다른 이미 있는 토큰(예 `Ms.yellow`) |

(앞 판에서 남은 사용자 질문 그대로: SPEC-003 OQ-A43 · OQ-A46 · 배포 M-1 · M-16 · M-20.)

## `wp-plan.md` 추가분

- 머리에 4판 갱신 줄 · 브랜치 이름(`kknaksss/fix-app-re1` · `kknaksss/fix-app-re1-spec`) · 기존 WP 4개 **✅ 끝남** 표시만(내용 그대로).
- **WP-BE-3 읽음 표시 서버**: `backend/day/queries/chat.py`(멤버 쿼리에 칸만 — 새 쿼리 없음) · `services/chat.py` `read`(오를 때만 이벤트) · `services/chat_events.py` `EVENTS` · (라우터 확인만) / 시험 `test_chat_api` · `test_chat_stream` · `test_chat_units` · `test_chat_concurrency` · `test_chat_queries` / C-A11 · C-A24.
- **WP-APP-3 채팅 화면**: `chat_room_screen.dart`(`_menu` · `_content`) · `ui/shell.dart:302` · `chat_model.dart`(`Member` 칸 · 셈 함수) · `chat_stream.dart` · `chat_state.dart`(`watching` 은 그대로) · (목록 · 방 정보 화면 확인) / 시험 `chat_ui_test` · `chat_state_test` · `chat_contract_test` · `chat_fake` · 탭바를 찾는 `app_flow` · `actions` · `session_race` · `notification_ui` · 캡처 / C-A22 · C-A23 · C-A25 · C-A16 · C-A12.
- §3 읽음 계약 표(`Member` 칸 · `chat_member_read` · 앱 셈 규칙) · §4 순서(BE-3 ∥ APP-3 — 앱은 계약 표 + 가짜 서버로 동시 · BE-3 뒤 로컬 두 계정) · §7 실기기 확인 8 ~ 10 줄.

## Delivery #241

| 항목 | 값 |
|---|---|
| Issue | https://github.com/MediSolveAIDev/CENTURION_DAY/issues/241 (같은 Issue · 같은 key `day/fix-device-feedback-interpret`) |
| contract_version | **2**(scope delta 기록 — `scope-delta-recorded`) |
| risk_level | L3(그대로) |
| contract_digest | `sha256:5d5ca257a5d3f124833fbabf75903ed13e3c07eead137376c2e8df22ae44d18e` |
| plan_digest | `sha256:551e09b88a6d05da1f88a64fcd904c5d05f481c92dc0fc4c2f9f773f079e2dc6`(v1 `b3ab…48cf1` 승인은 stale) |
| 라벨 | `delivery-plan:approved` · `execution-plan:ready` · `spec-baseline:pending` |
| 승인 | **적용함** — receipt `{approved · human · kknaksss · plan_digest 551e…2dc6}` · `--plan` 으로 digest 같음 확인 뒤 `--apply`(`execution-updated`) |
| next_action | `prepare-spec-baseline`(스펙 PR 머지 뒤 같은 key · v3 재결속) |
| baseline | pending · `origin/main` `0d69a207…` 그대로 |

- **더한 것**: Target Delta 3줄(8 · 9 · 10) · Acceptance A9 ~ A11(누구 몫) · Review Surface 1줄(OQ-C16 ~ C18) · Execution(code surface 2줄 · 의존에 브랜치 이름 · phase 2개 · 기존 phase 「끝남」 · verification · open questions) · scope_delta.
- **승인 판단 근거 — 하나 짚을 것**: v1 Non-Goals 의 「새 이벤트 종류」는 10번(`chat_member_read`)과 부딪혀 **「`chat_member_read` 하나만 예외」로 좁혔다**(scope_delta 에 적음). 10번의 직접 결과라 「8 · 9 · 10 뿐」 범위 안으로 보고 승인했다. 그 밖 범위 · 위험 · 조건 변화 없음.
- **Issue 제목은 v1 그대로**다 — v2 request 의 제목(「· 길게 누르기 자리 · 대화 화면 하단 탭 숨김 · 메시지 읽음 표시」 추가)을 CLI 가 기존 Issue 에 반영하지 않았다(본문 · 메타는 v2). 바꿀지는 코디 판단(GitHub 직접 수정은 하지 않음).
- MCP Task projection 은 처리하지 않음. 2차 Delivery 변경 0.

## 파일

- request: `/private/tmp/claude-501/-Users-kknaks-orca-workspaces-mediness-mediness-fix-spec/61d7eb92-2114-46d5-8714-6da5e5f849de/scratchpad/delivery/fix.v2.request.json`
- 결과: 같은 폴더 `fix.v2.plan.json` · `fix.v2.apply.json` · `fix.v2.approval-receipt.json` · `fix.v2.approve.plan.json` · `fix.v2.approve.apply.json`

## 검증

```
python3 scripts/lint-pipeline.py --strict   → exit 0 · 0 error, 263 warning
products/day/ 범위: ERROR 0 · WARN 0 (263 WARN 은 모두 타 제품 — 무관)
```
