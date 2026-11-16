# be-3 — #245 W6 · 점유 이동 이벤트 연쇄의 상세 결과를 판 작업 행에 바로 반영

워크트리 `prod-deploy-re1` · 커밋 안 함(변경만 남김).

## 원인(코디 확인과 같음)

`_chain_room_assign` 이 받은 예약 상세(`adapter.fetch_visit_tasks`)를 outbox 확인
(`confirm_room_assign_added` · `confirm_visit_tasks`)에만 썼다. 새 「방 배정」 작업 행(VisitTask)은 10초
일정 조회만 만들었다. 그래서 `follow_room_assign` 의 방 update 가 0행이 됐고, 첫 신호 뒤 판 조회에는
점유 띠(`holdRoom`)가 없었다.

## 고친 것

| 파일 | 내용 |
|---|---|
| `backend/day/emr/sync.py` | `apply_visit_tasks(session, hospital, vendor, visit_id, visit_external_id, NVisitTasks, now, room_assign_etc_task_id)` 를 새로 뒀다. 10초 일정 조회가 쓰는 **`_apply_tasks` 를 그대로** 부른다. 방문 잠금(`lock_visits`)과 반영 대기 칸 보호(`pending_guards` → `Guard`)도 같다. 작업 id 는 외부 id 연결(`Refs.link`, `ON CONFLICT`)로 정해진다. 방문 칸(카드 방 · 단계)은 건드리지 않는다(10초 조회 몫). `_apply_tasks` 의 인자 타입은 `TaskSource` Protocol 로 넓혔다(`NVisit` 과 새 `DetailVisit` 둘 다 받는다). 동작은 바뀌지 않는다. |
| `backend/day/services/emr_sync.py` | 연쇄에서 상세 결과를 **두 번 모두** 반영한다(`_apply_detail`). ① 새 「방 배정」을 찾은 상세 → 같은 transaction 에서 반영 → `confirm_room_assign_added` → `follow_room_assign` → commit. 이제 새 행이 있으므로 원래 방 update 가 맞는다. 옮길 작업 방은 아직 확인 전인 「방 배정」 만들기 쓰기의 `moving` guard 라서 덮이지 않는다. ② 마지막 확인 상세 → 반영 → `confirm_visit_tasks` → commit. 그다음 `_signal` 이 나간다(신호 순서는 그대로). `taken_by_poll` 이면 rollback 한다(일정 조회가 이미 반영 · 확인). 상세 조회 실패 · 못 찾음 · 업체 미지원이면 반영하지 않는다(지금처럼 10초 조회가 잇는다). |

범위 밖은 건드리지 않았다. 10초 주기, 다른 경로(이동 · 복귀 · 「방 배정」 있는 점유), 웹, 문구는 그대로다.
board_rules.py 도 바꾸지 않았다.

## 시험

새 파일 `backend/tests/day/board/test_board_room_chain.py`(infra · 앱 전체 · 가짜 KOS):

- `test_연쇄_신호_직후_판에_새_방배정_행과_점유가_보인다`: 점유 이동 API → `run_outbox` 한 회차(일정 조회
  없음 · 가짜 어댑터의 `fetch_schedules` 는 부르면 실패). 판 신호를 낸 바로 뒤의 `GET /api/board` 카드에
  `holdRoom = 원래 방` · `canReturnRoom = true` 가 있다. 새 「방 배정」 행은 (4, 원래 방). 연쇄 결과는
  `confirmed`, KOS 호출은 add → detail → room → room → detail.
  - 고친 것을 끈 채로 돌리면(`_apply_detail` no-op) 이 시험이 실패하는 것을 확인하고 원래대로 돌렸다
    (새 「방 배정」 행 없음).
- `test_일정_반영과_겹쳐도_작업_행은_한_번만_생긴다`: 같은 반영 경로를 동시에 2번 + 1번 더 돌려도 작업 행은
  새 「방 배정」 1개만 는다(1 · 2 · 3 은 그 행 그대로).

검증: 격리 스택(`day-be245` · 11142/11143)에서 관련 파일만 1회 돌렸다(test_board_room_chain ·
test_room_move_chain · test_room_move_chain_rules · test_board_room_api · test_emr_sync_service · test_outbox ·
test_sync · tests/architecture). 결과는 **93 passed**. `uv run ruff check backend` 통과, 바꾼 파일 format 통과.
스택은 `down -v` 했다. 사용자 11040 · `day-local` 은 건드리지 않았다.

## 데모 실물 — 2회 실행 · 결론: 띠는 연쇄가 그린다(10초 조회 전)

로컬 11040(코디가 이 워크트리 코드로 재빌드 · 01:56:05Z 시작)에 HTTP 만 보냈다. 데모 지점이고, 계정은
local.env 값을 썼다(출력하지 않음).

1. 오늘 데모 판이 비어 있었다(카드 0). `scripts/seed_demo_board.py --count 1` 을 1회 돌려 **[TEST] 방문
   1건**을 만들었다(데모 테넌트 가드 · 11:00 KST 칸 · 시술 대기). 지우지 않았다. 10초 조회 뒤 판에 카드
   1장이 보였다.
2. 측정 스크립트(점유 이동 → 0.1초마다 `GET /api/board` → [복귀하기])를 돌렸다. 쓰기까지 간 것은 2회다.
   01:58:38 시도 1회는 카드가 아직 점유 상태라 판 조회만 하고 멈췄다(쓰기 없음 · 아래 「관찰」).

### 1회차(판정 못 함)

| 시각(UTC) | 일 |
|---|---|
| 01:57:18.356 | 10초 일정 조회 회차 끝(앞 회차) |
| 01:57:27.212 | 클릭(`room-move hold`, 52ms 에 200) |
| 01:57:28.131 | **10초 일정 조회 회차 끝** |
| 01:57:28.147 | 띠(`holdRoom` = 원래 방) 처음 보인 GET — 클릭 뒤 0.93초 |
| 01:57:28.172 | [복귀하기] 200 |
| 01:57:28.820 | 발송 회차 끝 `{sent: 1, chain: {confirmed: 1}}` = 연쇄 확인 |
| 01:57:38.461 | 발송 회차 `{sent: 3}`(복귀 쓰기 complete=false · DELETE · 방) · 실패 없음 |

worker 로그는 `docker logs day-local-worker-1` 로 읽기만 했다(시각 · 일 · 건수만 옮김 · 병원 id 지움).

**판정 보류:** 연쇄 자체는 실물에서 끝까지 갔다(`confirmed`). 하지만 띠가 처음 보인 GET(28.147)이
10초 일정 조회 회차 끝(28.131) 16ms 뒤다. 그래서 이번 1회로는 띠를 연쇄의 첫 반영(add 응답 → 상세 → 반영 · commit)이
그렸는지, 일정 조회가 그렸는지 가를 수 없다. 연쇄 회차의 끝(28.820)은 띠보다 뒤인데, 첫 반영 commit 은
follow 보내기 · 마지막 상세 확인 앞이라 이 시각만으로는 알 수 없다.

### 2회차(코디 승인 · 조회 끝 직후 클릭 · 같은 [TEST] 카드)

| 시각(UTC) | 일 |
|---|---|
| 02:01:08.216 | 10초 일정 조회 회차 끝 — 클릭 **전** |
| 02:01:08.692 | 클릭(`room-move hold` · api 로그 08.720 · 32ms 에 200) |
| **02:01:09.475** | **띠(`holdRoom` = 원래 방) 처음 보인 GET — 클릭 뒤 0.78초** |
| 02:01:10.188 | 발송 회차 끝 `{sent: 1, chain: {confirmed: 1}}` = 연쇄 확인 |
| 02:01:10.560 | 카드 반영 중(`reflecting`) 끝남 → [복귀하기] 200(10.583) |
| 02:01:10.805 | 발송 회차 `{sent: 3}`(복귀 쓰기) · 실패 없음 |
| (≈02:01:18.2) | 다음 10초 일정 조회 회차 끝 — **띠보다 약 8.7초 뒤** |

**결론:** 띠가 처음 보인 GET(09.475)은 다음 일정 조회(≈18.2)보다 **먼저**다. 앞 조회(08.216)는 클릭 전에
끝났으므로 새 「방 배정」을 볼 수 없었다. 그러므로 띠는 연쇄의 첫 상세 반영이 그렸다. 연쇄 확인(10.188)은
그 뒤다. 첫 반영 commit 은 follow 보내기 · 마지막 확인 상세보다 앞서고, 그 반영 뒤 카드 GET 에서 띠가
보였다. 일정 조회 회차 시각은 worker 로그(`docker logs day-local-worker-1`, 읽기만)에서 땄다.
2회차 뒤 카드는 처음 상태다(띠 없음 · 반영 중 아님 · 점유 이동 가능 · 실패 로그 0).

### 관찰 — 연쇄 도중 [복귀하기](1회차 · 코디 판단용)

1회차에서 측정 스크립트는 띠를 보자마자 [복귀하기]를 눌렀다(28.172). 이때 연쇄는 아직 끝나지 않았다(28.820).
- 그 뒤 카드는 **띠 · 반영 중(`reflecting`)이 남은 채** 01:59:4x 까지 갔다.
- 같은 시각 KOS(읽기만)는 남은 작업이 모두 한 방이었다. 「방 배정」은 지워졌거나 CANCELED 였다.
- 01:59:43–52 에 웹 판에서 누군가(내 스크립트 아님 · api 로그 `/board/visits/…/room-move` · `room-return` 두
  번) 이 카드를 다시 조작했다. 그 뒤 02:00:11 에 풀렸다.

추정 원인(확인 안 함): 연쇄의 follow ①(새 「방 배정」 → 원래 방 · expect `room`)이 [복귀하기]의 DELETE 와
엇갈렸다. 그 작업이 사라지면 room 확인은 맞을 수 없다. DELETE 의 expect 는 `absent`(→ `status` 칸)라서
`_superseded` 로 닫히지 않는다. 그래서 `sent` 로 남아 방 guard 를 잡고, stale(180초)까지 갔을 수 있다.

W6 덕에 띠 · [복귀하기]가 연쇄 도중(~1초 안)에 켜지므로 이 엇갈림이 전보다 쉬워진다. 고칠 방향 후보는
둘이다. (a) `absent` 확인이 같은 sequence 의 다른 칸 확인도 닫게 한다. (b) 그 방문에 반영 대기 쓰기가
있으면 [복귀하기]를 끈다. 범위 밖이라 손대지 않았다. 코디가 정한다.
2회차는 스크립트가 반영 중이 끝난 뒤에 복귀를 눌렀고, 엇갈림 없이 풀렸다.

원상복구: 복귀 뒤 카드는 처음 상태다(방 있음 · 점유 이동 가능 · 띠 없음 · 복귀 버튼 없음). 복귀 쓰기 3건은 실패 없이
보내졌다. 만든 [TEST] 방문 1건(시드 1회)은 남겼다.

스크립트: `/private/tmp/claude-501/-Users-kknaks-orca-workspaces-CENTURION-DAY-prod-deploy-re1/bac6de18-22bc-4c1f-b42c-da2ca725ce19/scratchpad/demo_band_check.py`
