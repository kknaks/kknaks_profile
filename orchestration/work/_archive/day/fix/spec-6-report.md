# fix-spec-6 결과 보고 — 문서 리뷰 4판 나머지 지적(정정 2)

## 상태: done

근거 = `fix/correction-read-2.md` 「스펙(planner)이 반영할 것」 W2 ~ W9 + `review-doc-2-report.md` 해당 지적 · 「조용히 통과하는 자리」. F1 · W1 은 정정 1(5판)로 이미 닫힘 — 이번에 W1 의 남은 한마디(「빼기는 max 와 따로」)만 더함. 커밋 · push 0.

## 지적별 고친 자리 (SPEC-004 = `products/day/20-spec/spec-004-internal-chat.md`)

| 지적 | 고친 자리 | 내용 |
|---|---|---|
| W2 | SPEC-004 `:187` · OQ-C17 `:642` · C-A25 `:607` | U-2 새 줄 「보고 있는 방에서는 내 숫자를 바로 뺀다」 — 보고 있는 방에서 화면에 그린 메시지까지 나를 읽은 사람으로 셈(읽음 요청 전에도 · 방을 열 때도) · 아니면 내 `lastReadSeq` · 서버 계약 그대로. **코디 기본값 — 카톡과 같은 겉보기 · 사용자 통보 · 뒤집을 수 있음**으로 표시 · OQ-C17 기본값에 포함(뒤집으면 1초 남짓 깜빡임) |
| W3 | SPEC-004 `:67` · `:342` | 「이벤트 6종」 → 7종(`chat_member_read` 포함) |
| W4 | SPEC-004 `:373`(읽음 표시 계약) · C-A24 `:606` · `wp-plan.md:163` · `:206` | 「`Room` 을 돌려주는 모든 HTTP · 이벤트 — #2 · **#3 1:1 열기** · #4 · #5 · #22 · `chat_room`」으로 묶음 · 시험에 각각 |
| W5 | C-A23 `:605` · `wp-plan.md:177`(셸 줄) · `:185`(시험) | C-A23 에 대화 화면(키보드 닫힘) 입력줄 = 안전 영역 위 · 홈 표시줄과 안 겹침 · 탭 숨기는 다른 화면 맨 아래 요소 · 아래 inset 기기 캡처 1장 / WP 셸 줄에 본문 아래 padding 빼는 자리(`removePadding(removeBottom: true)`) |
| W6 | SPEC-004 `:438`(실시간 표 `chat_member_read`) | 방 기준 부하 ≈ (N−1)² 발행/초 · N ≤ 20(많아야 약 361 · 예 342) · 받아들임 · 줄이려면 다음 판(지금은 서버 묶음 없음 — Non-Goals) |
| W7 | SPEC-004 `:170`(`ChatState.watching`) · `:202`(`_menu` 의 `findRenderObject` → `localToGlobal`) · `wp-plan.md:176` · `:177` · `:180` | 줄 번호 → 함수 · 이름 기준 |
| W8 | `wp-plan.md:180`(WP-APP-3 `chat_state.dart`) | 「덮기」 낱말 0(grep 0건) — 메시지를 받는 모든 길(`case 'chat_message'` · 목록 · 메우기 · 전달) = 보낸 사람 max · `Room.members[]` 가 오는 모든 길(`case 'chat_room'` · 목록 · 재연결 · 응답) = 멤버마다 max 로 합치기 · 빠진 멤버는 목록 · `active` 로 · 정정 2 보고 있는 방 셈 |
| W9 | C-A25 `:607` · `wp-plan.md:185` | 정정 2 갈래(보고 있는 방 깜빡임 0 · 보고 있지 않으면 뜸 · 방 열 때 · `chat_member_read`(B=12) 뒤 옛 `chat_room`(B=9) · 작은 seq 늦게) · **가짜 서버가 이벤트 순서를 일부러 바꿔 보냄** |
| W1 남은 것 | SPEC-004 `:186` | 「멤버를 빼는 것(나감 · 비활성)은 max 와 따로 — 받은 `members[]` 에 있느냐 · `active` 로」 |
| 조용히(C-A24) | C-A24 `:606` · `wp-plan.md:163` | 동시 읽음 = 같은 값 `chat_member_read` 중복 허용 · 값이 내려가지 않음으로 시험 |

그 밖: SPEC-004 머리 개정 ④ `:30` 에 「정정 2」 한 줄 · `wp-plan.md` §3 새 줄 「보고 있는 방 표시」 `:210` · WP-APP-3 제목 · `log.md` 6판 1줄.

## 못 고친 것

없음. (앱 쪽 W2 · W5 · W9 구현과 서버 W4 확인은 정정 2 의 mobile · backend 몫 — 스펙 · 계획에 적기만 함.)

## Delivery #241

손대지 않음 — 범위(Target Delta 9 · 10) · 수용 항목 뜻(C-A23 · C-A24 · C-A25)은 그대로이고 갈래 · 확인 항목만 늘었다. W2 는 표시 규칙(서버 계약 · 범위 변화 없음).

## 검증

`python3 scripts/lint-pipeline.py --strict` → exit 0 · 0 error, 263 warning · `products/day/` 줄 0.
