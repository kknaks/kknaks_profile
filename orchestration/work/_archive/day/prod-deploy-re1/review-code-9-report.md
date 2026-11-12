# 리뷰 리포트 — prod-deploy-re1 / code 9 · W6 후속 (b) 반영 대기 중 [복귀하기] 끔 (2026-11-12)

대상: 워크트리 미커밋 중 be-4 몫이다.
- `backend/day/services/board_rules.py` `room_return_block`
- `backend/tests/day/board/test_board_room_api.py`(시험 두 개를 늘림)
- `test_board_room_chain.py` 의 새 시험 1개

be-3(sync.py · emr_sync.py)은 review-code-8 에서 봤으므로 이번엔 보지 않았다.
근거: be-4-report.md · 사용자 결정 (b) · 스펙 보충 ⑥(spec 워크트리 미커밋 `spec-002-procedure-board.md` 규칙 29 · U-15 · 스냅샷 `canReturnRoom`).

## 판정: PASS

FAIL 0 · WARN 0 · 참고 4.

## 검증 (각 1회)

| 명령 | 결과 |
|---|---|
| 격리 스택(`docker compose -p day-rv9` · 127.0.0.1:11152/11153 · scratchpad 임시 env) + `scripts/test.sh` — test_board_room_api · test_board_room_chain · test_board_rules · test_room_move_chain_rules · test_room_move_chain · test_board_api · tests/architecture | **168 passed** (be-4 와 같은 수) |
| `uv run ruff check backend` | All checks passed |
| `ruff format --check` (board_rules.py · 두 시험 파일) | already formatted |
| 스택 `down -v` 뒤 `docker ps` | day-local-* 다섯만 남음 — 11040 · day-local 손대지 않음 |

be-4 의 음성 확인(새 조건을 끄면 3개 실패)은 다시 하지 않았다. 코드를 바꿀 수 없어서다.

## 볼 것 — 항목별

| 항목 | 판정 | 근거 |
|---|---|---|
| 어디서 계산해도 같은 판정 | PASS | 판정은 `board_rules.py:645-657` 한 곳이다. `canReturnRoom` = `room_return_block(v) is None`(`:843`)이고 다른 계산처가 없다(grep). 판 GET · 조작 응답 · 신호 뒤 스냅샷 모두 `load_world` → `BoardRules` → 같은 카드 dict 를 거친다. `reflecting` 은 `load_world` 의 outbox 조회 하나에서 채운다(`queries/board.py:266-288` · status `pending`·`sent` · `deleted_at IS NULL`). 스냅샷의 `reflecting`(`board_rules.py` `"reflecting"`)과 같은 집합이라 「반영 중」 표시와 엇갈리지 않는다 |
| 복귀 API 도 같은 거절 | PASS | `services/board.py:1452-1453` `room_return` 은 `_world`(방문 잠금 `board:<visit_id>` 뒤 `load_world` · `:147-152`)에서 같은 함수로 `_check` 해 409 `conflict` 를 낸다. 연쇄의 follow 쌓기와 일정 조회의 follow 쌓기는 같은 방문 잠금 안에서 commit 한다. 만들기 쓰기는 그 commit 까지 `sent` 다. 그래서 「반영 대기 0」으로 보이는 틈이 없다. 시험: 연쇄 도중 409(`test_board_room_chain.py:208-231`) · 일정 조회 길과 점유 이동 직후 409/false(`test_board_room_api.py`) |
| 반영 끝나면 다시 켜짐 | PASS | 조건이 「pending·sent 행이 있음」뿐이다. 그래서 confirmed · failed · 지움(`deleted_at` — outbox 에 별도 취소 status 는 없다) 어느 쪽으로 끝나도 다음 `load_world` 에서 켜진다. 시험은 confirmed 뒤 true 를 세 군데에서 단언한다(연쇄 · 일정 조회 길 · 점유 이동) |
| failed 가 영영 막지 않음 | PASS | `failed` 는 조회 조건 밖이다. 남은 pending · sent 도 끝이 정해져 있다: `sent` 는 `fail_stale` 180초(`outbox_sent_stale_seconds`). 토큰이 없는 `pending` 은 `decide_token_wait` 1800초 → failed(`outbox.py:285-293`). 앞 쓰기가 failed 면 `_block_later` 가 뒤 pending 을 함께 failed 로 둔다(`:354-367`). 보낸 뒤 안 맞음은 `MISS_LIMIT` → 재전송 → 3번째에 failed |
| 순서 · 기존 코드 | PASS | `visit_not_on_board` → `room_not_held` → `conflict` 순이다. 점유가 아니면 예전과 같은 코드를 낸다. 새 코드 · 새 문구는 없다(기존 `conflict` · 기존 공용 토스트) |
| 범위 밖 없음 | PASS | be-4 diff 는 `room_return_block` 한 함수뿐이다. (a) absent 확인(`outbox.py:93`) · `canMoveRoom` · `canHoldMove` · rooms 쪽 · 템플릿 · day.js · 문구 · 주기는 바뀌지 않았다. 앱(`app/lib`)은 `canReturnRoom` · room-return 을 쓰지 않는다(grep) |
| 화면 | PASS | 템플릿은 그대로다. 띠의 [복귀하기](`board_parts.html:167`)와 팝오버 [복귀하기](`:305`)가 모두 `canReturnRoom` 을 본다. 그래서 띠는 남고 버튼만 숨는다(스펙 ⑥ 「보이지 않음」 그대로) |
| 쿼리 비용 | PASS | 새 쿼리가 없다. `reflecting` 은 판 전체 방문을 `visit_id IN (…)` 하나로 이미 읽던 값이다. 판정은 메모리 set 확인(`v.id in self.w.reflecting`)이라 카드마다 N+1 이 없다 |
| 스펙 대조 | PASS | 규칙 29 「그 방문에 KOS 반영 대기 쓰기(`pending` · `sent` op)가 없을 때만」 · 스냅샷 `canReturnRoom` 문장과 같다 |

## 참고

- 참고 1(스펙 미결과 코드): 스펙 수정 2 「정하지 않은 것」에는 「숨김 중 room-return 요청을 거절할지 · 그 이름」이 남아 있다. 코드는 409 `conflict`(기존 코드)로 거절한다. 코디가 스펙 오류 매트릭스나 규칙 29 에 이 결정을 한 줄 적으면 코드와 맞는다. API 오류 계약은 외부 계약이다(AGENTS.md).
- 참고 2(be-4 주의와 같음): 조건이 「그 방문의 반영 대기 쓰기 전부」다. 그래서 차트 자동 저장 · 단계 같은 무관한 쓰기가 반영 대기여도 [복귀하기]가 몇 초 숨는다. 차트를 쓰는 동안 자동 저장이 이어지면 숨김이 반복될 수 있다. 스펙 ⑥ 문장 그대로이므로 결함이 아니다. 실물에서 불편하면 코디가 판단한다.
- 참고 3(오래 숨는 경우): 그 직원의 KOS 토큰이 없어 쓰기가 pending 으로 기다리면 최대 1800초(30분) 숨는다. 다만 그때는 그 방문 쓰기 전체가 「반영 중」이라 같은 신호가 화면에 이미 있다. 영영 막히지는 않는다.
- 참고 4: 점유 + 반영 대기면 `canMoveRoom` · `canReturnRoom` 이 둘 다 false 다. 그래서 방 이름 버튼(`board_parts.html:155`)도 팝오버 없이 글자만 남는다. 스펙 U-15 「점유 중이면 [복귀하기]만 · 반영 대기면 그것도 안 보임」의 귀결이다.
