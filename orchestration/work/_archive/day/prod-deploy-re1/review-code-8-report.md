# 리뷰 리포트 — prod-deploy-re1 / code 8 · #245 W6 연쇄 상세 → 판 작업 행 (2026-11-12)

대상: 워크트리 미커밋(HEAD `88210079` 위) — `backend/day/emr/sync.py` · `backend/day/services/emr_sync.py` · 새 시험 `backend/tests/day/board/test_board_room_chain.py`.
근거: be-3-report.md · e2e-feedback.md W6 · review-code-6/7.

## 판정: PASS

FAIL 0 · WARN 0 · 참고 3. 리포트의 「관찰 — 연쇄 도중 [복귀하기]」는 **원래 있던 결함**이다. 이번 변경으로 드러나기 쉬워졌다(참고 1).

## 검증 (각 1회)

| 명령 | 결과 |
|---|---|
| 격리 스택(`docker compose -p day-rv8` · 127.0.0.1:11152/11153 · env 는 scratchpad 의 임시 값) + `scripts/test.sh` — test_board_room_chain · test_room_move_chain · test_room_move_chain_rules · test_board_room_api · test_emr_sync_service · test_outbox · test_sync · tests/architecture | **93 passed** (be-3 와 같은 수) |
| `uv run ruff check backend` | All checks passed |
| `ruff format --check` (바뀐 2 파일 + 새 시험) | already formatted |
| 스택 `down -v` 뒤 `docker ps` | day-local-* 다섯만 남음 — 11040 · day-local 손대지 않음 |

「고친 것을 끄면 새 시험이 실패한다」는 be-3 의 확인이다. 이 리뷰는 코드를 바꿀 수 없어서 다시 확인하지 않았다.

## 볼 것 — 항목별

| 항목 | 판정 | 근거 |
|---|---|---|
| 10초 일정 조회와 같은 반영 경로 | PASS | `emr/sync.py:1416` `apply_visit_tasks` → `_apply_tasks`(`:1452` · 일정 조회 `:981` 과 같은 함수). 잠금 → guard 순서도 일정 조회(`:910-911`)와 같다(`:1435-1436` `lock_visits` → `pending_guards`). KOS 상세는 일정 조회와 같은 작업 mapper `task()` 를 쓴다(`kos/mapper.py:541-558`). 그래서 담당자 · 차트 · 상태 칸이 빈 값으로 덮이지 않는다. `_apply_tasks` 인자를 `TaskSource` Protocol 로 넓힌 것은 타입뿐이다. 본문은 바뀌지 않았다 |
| 반영 순서 = 일정 조회 회차와 같음 | PASS | 일정 조회 회차(`services/emr_sync.py:192-203`)는 한 transaction 에서 반영 → `outbox.confirm` → `follow_room_assign` 순이다. 연쇄 ①(`:316-322`)도 반영 → `confirm_room_assign_added` → `follow_room_assign` → commit 순이다. 그래서 `follow_room_assign`(`board.py:1549-1557`)의 방 update 가 이제 새 행에 맞는다(전엔 0행) |
| 반영 대기 칸 보호 | PASS | 연쇄 ① 반영 때 만들기 쓰기는 아직 `sent` 다. 그래서 `guard_of` 의 `moving` → 옮길 작업 `room` 을 덮지 않는다(`sync.py` `guard_of`). 마지막 확인 반영(`:350`) 때는 follow ① ② 가 `sent` 라 그 칸이 guard 다. 그 뒤 `confirm_visit_tasks` 를 부른다 |
| 겹칠 때 행 두 번 안 생김 | PASS | 작업 id 는 `Refs.link` 의 `ON CONFLICT (hospital_id, vendor, entity_type, external_id) WHERE deleted_at IS NULL`(`sync.py:146-190`)로 정해진다. 그 link 도 방문 advisory lock 뒤에서 돈다. 그래서 일정 조회와 연쇄가 같은 방문을 차례로 처리한다. 차트 이력(`kos_chart_changed`)도 뒤에 오는 쪽이 앞의 결과를 `before` 로 보므로 두 번 쌓이지 않는다. 시험 `test_일정_반영과_겹쳐도_작업_행은_한_번만_생긴다` — 동시 2회 + 1회에서 새 행은 1개 |
| 일정 조회가 먼저 확인했을 때 | PASS | 일정 조회가 잠금을 먼저 잡고 commit 했다고 하자. 연쇄는 잠금 뒤 guard 를 읽는데, 만들기 쓰기가 이미 `confirmed` 라 `moving` guard 가 없다. 그래도 `confirm_room_assign_added` 가 False 를 돌려준다. 그러면 commit 없이 `async with` 를 나가 반영까지 rollback 된다(`:319-320` · 일정 조회 값 그대로). 반대 순서면 일정 조회가 연쇄 commit 뒤 guard(follow ① ② pending)를 읽어 덮지 않는다 |
| 실패 · 못 찾음 → 10초 조회 | PASS | `detail_error`(`:306`) · 업체 미지원 `None`(`:308`) · 새 「방 배정」 못 찾음(`:313`)은 모두 반영(`:318`) **전에** 돌아간다. 마지막 확인에서 상세가 실패하거나 None 이면 `break` 로 반영 없이 `follow_sent` 가 된다. 연쇄 예외는 기존 `chain_error`(review-7)라 신호가 그대로 나가고 rollback 된다 |
| 신호 순서 | PASS | 첫 반영 commit → … → `run_outbox` 의 `_signal`. 신호는 반영 commit 뒤다. 시험 1이 `_signal` 직후 판 조회에서 `holdRoom` · `canReturnRoom` 을 단언한다 |
| 범위 밖 변경 없음 | PASS | `git diff --stat` = 두 파일뿐이다. 주기(`Settings` 두 10초) · `send_pending` · 이동 · 복귀 · 「방 배정」 있는 점유 · board_rules · 웹(템플릿 · day.js) · 문구 · migration 은 바뀌지 않았다. 방문 칸(카드 방 · 단계)은 연쇄가 쓰지 않는다(`apply_visit_tasks` docstring · 코드 모두). review-7 의 아키텍처 시험(DELETE 경로 · 10초 고정)은 통과했다 |

## 판정 — 「관찰: 연쇄 도중 [복귀하기]」 엇갈림

**원래 있던 결함이다. 이번 변경으로 새로 생긴 것은 아니다. 다만 드러나기 쉬워졌다.**

- 원인 줄은 둘 다 HEAD(`88210079`)에 이미 있다.
  - `outbox.py:93` `"absent": "status"` 때문에 [복귀하기]의 DELETE(expect `absent`)와 follow ①(expect `room_external_id` → `room`)은 `touched` 가 겹치지 않는다. 그래서 `_superseded`(`:703`)로 follow ① 이 닫히지 않는다.
  - 새 sequence 가 사라지면 `tasks_met` 는 맞을 수 없다. 그래서 follow ① 은 `sent` 로 남아 그 방문 guard 를 잡는다. 그 뒤 `decide_on_poll` 이 「안 맞음」을 세어 재전송하거나 failed 로 보내거나, `fail_stale` 로 간다.
  - `board_rules.py:645-649` `room_return_block` 은 반영 대기 쓰기를 보지 않는다. 띠(`hold_room`)만 있으면 [복귀하기]가 열린다.
- 이번 변경 전에도 같은 엇갈림이 생기는 길이 있었다. 일정 조회가 만들기를 확인한 경우(연쇄 `detail_error` · `not_found` · `taken_by_poll` · `follow_not_sent` 뒤)다. 일정 조회는 새 행 반영과 follow ① ② 쌓기를 한 transaction 에서 commit 한다(`services/emr_sync.py:192-203`). 그래서 띠와 [복귀하기]가 follow 가 pending 인 채 다음 발송 회차까지(≤10초) 보였다.
- 이번 변경으로 **정상 연쇄 길에도** 그 틈이 생겼다. 첫 반영 commit 부터 follow 확인까지 약 1초다(be-3 1회차 실측 28.147 → 28.820). 전에는 정상 연쇄에서 띠가 일정 조회 때 나왔고, 그때 follow 는 대개 이미 confirmed 였다.
- 고칠 방향은 be-3 의 (a) · (b)와 같다. 코디가 정할 일이고 이번 범위 밖이다. (b) 「그 방문에 반영 대기 쓰기가 있으면 [복귀하기]를 끈다」는 연쇄 길과 일정 조회 길을 함께 닫는다. (a) `absent` 확인이 같은 sequence 의 다른 칸 확인도 닫게 하면 이미 쌓인 follow ① 이 남는 문제를 닫는다.

## 참고

- 참고 1: 위 판정이다. 사용자가 띠를 보자마자 [복귀하기]를 누르는 일은 실물에서 흔할 수 있다(be-3 1회차에서 스크립트가 25ms 만에 눌렀고, 그 뒤 01:59 대에 사람이 다시 조작했다). 그러면 카드가 「반영 중」으로 최대 stale(180초)까지 남을 수 있다. 이번 PR 과 같이 다룰지는 코디가 판단한다.
- 참고 2(시험 공백): 반영 뒤 `taken_by_poll` rollback 을 직접 걸어 보는 시험이 없다. 반영이 rollback 되지 않으면 일정 조회 값 위에 옛 상세가 commit 될 수 있다. 지금은 `async with` 를 commit 없이 나가므로 맞다. 시험 1 · 2 와 기존 `test_room_move_chain` 의 `taken_by_poll` 시험은 상태 값만 본다.
- 참고 3: 상세 반영은 `mark_absent` 까지 일정 조회와 같다. 상세 응답에 없는 작업은 그 방문에서 사라짐 처리된다. 상세가 그 일정의 작업 전부를 준다는 전제(mapper docstring · HAR)에 기댄다. 이 전제가 틀리면 일정 조회와 상세가 행을 번갈아 지우고 살리게 된다. 실물 2회에서는 문제가 없었다(be-3).
