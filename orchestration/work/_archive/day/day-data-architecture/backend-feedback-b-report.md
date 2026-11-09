# 화면 피드백 2차분 — F3 · F4 · F5 · F7 · F10 (백엔드)

## #231 영향 (먼저 읽을 것)
라우트 · 조각 이름은 그대로다. 넘기는 값이 바뀌었다.

| 값 | 바뀐 점 | 화면 |
|---|---|---|
| `snapshot.cards` | 귀가 대기(`procedure_done`) 방문이 **빠진다**(F5). 그 방문은 `doneTab` 에만 있다. `card.state` 에 `"home"` 이 더는 오지 않는다 | 판에서 「흐린 귀가 대기 카드」 분기를 지워도 된다 |
| `card.tasks` 순서 | 진행중(시작 순) → 대기(오더 순) → 완료(완료 시각 순)(F4) | 배열 순서대로 그리면 된다 |
| `task.pickable` | 준비중 · 호출 · 수락 줄 모두 true(F3 · cc D-26). 진행중 · 완료 · 귀가 대기는 false | 체크박스 켜짐이 넓어진다 |
| `customer.nationality` | 새 칸(F7) — 판 카드 · `doneTab[].customer` 둘 다. 값 그대로, 없으면 null | 바이탈 줄 「국적」 · 없으면 칸을 안 그린다 |
| `card.inAt` | 그대로 실린다(정렬 · 인박스 「시술 대기」 순서에 쓰임) | **고객 줄에 「입실 HH:MM」을 쓰지 않는다**(F7) |
| 호출 상태 | 다시 호출하면 앞 수락은 그 시술에 무효 → 그 줄은 다시 「호출」 · [수락] 이 필요하다 | 서버 값 그대로 |

## 1. F3 다시 호출(cc D-25 ~ D-27)
- **유효 호출 = 그 시술이 들어간 가장 최근 호출**이다. 그 호출이 닫혀 있으면 유효 호출은 없다(`board_rules.__init__`).
  - 앞 호출의 수락은 그 시술에 무효다(`accept_of(effective_call)` 만 본다).
- **호출 대상 = 대기 줄 전부**(준비중 · 호출 · 수락). 진행중 · 완료 줄은 `task_not_pickable` 이다.
- **앞 호출을 닫는 때** = 그 호출을 유효 호출로 갖는 시술이 하나도 안 남을 때만(`rules.calls_to_close` · `services.board._close_moved`).
  - 호출 · 재호출 둘 다 이 규칙을 따른다.
  - 재호출이 수락된 시술이 남은 앞 호출을 닫던 버그도 이것으로 고쳤다.
  - `call.create` payload 에 `closedCallIds` 를 남긴다.
- **KOS**: 고른 시술 중 이미 호출된 것이 있으면 `call-tasks-doctors` 를 다시 보낸다(OQ-09). 이것은 cc 근거 쓰기라 아래 「데모 연결만」 규칙을 따른다.

## 2. F4 카드 안 줄 순서
- `board_rules.ordered_tasks` — 진행중(`started_at` · 같으면 `sort_order`) → 대기(`sort_order`) → 완료(`completed_at`).

## 3. F5 귀가 대기
- `BOARD_STEPS` 에서 `procedure_done` 을 뺐다. 판 카드 · 순서 · 호출 탭에서 빠지고 `doneTab` 에만 남는다.
- 조작은 그대로 **409 `visit_home`** 이다(404 아님). `rules.is_target` 이 귀가 대기 방문도 조작 대상으로 찾는다.

## 4. F7 국적
- `BVisit.nationality` ← `customer.nationality`(값 그대로 · 변환 · 추정 없음).
- 스냅샷 `customer.nationality` 에 싣는다(판 카드 · 시술 완료 탭).

## 5. F10 KOS 쓰기 = 누른 사람 토큰 · cc 근거 쓰기 열기
- **migration `0005_outbox_sender`**: `external_outbox.sender_staff_id`(uuid · FK staff · NULL 허용 — 옛 행). 근거는 SPEC-000 §3 05 · OQ-21.
- 조작이 op 을 만들 때 `sender_staff_id` = 요청 세션 직원이다. **수락도 누른 사람**이다(대리 수락이면 그 간호사).
  - `event_log.actor_staff_id` 는 그대로 수락한 의사다.
  - KOS 본문 `doctorIds` 는 수락한 의사다.
- 보낼 때 토큰 = `sender_staff_id` 의 만료 안 된 `external_session` 이다. 칸이 빈 옛 행만 event actor 로 찾는다(`outbox.staff_token`).
- **cc 구현 근거 쓰기**(HAR 없음):

  | 쓰기 | 경로 · 값 | 확인 조건 |
  |---|---|---|
  | 다시 호출 | `call-tasks-doctors` | 작업 `status = waiting` |
  | 시작 취소 | `change-flow-step {id, step: PROCEDURE_WAITING}` | `flow_step` |
  | 완료 취소 | `change-tasks-complete {complete: false}` | **`status_not = done`**(새 확인 키 · cc K2 — 실 KOS 는 READY) |
  | 귀가 대기 ① | `schedule/v1/commands/cancel-flow-tasks {scheduleId, sequences, reason: CANCEL}` | `status = canceled` |
  | 귀가 대기 ② | `change-flow-step {step: PROCEDURE_DONE}` | `flow_step` |

  - 단계 쓰기는 HAR 로 확인된 **내부** 경로 · 본문(`{id, step}`)에 값만 바꿨다. cc 는 공개 경로 `{scheduleId, step}` 로 보냈다 — 이 차이가 데모 실물로 확인할 부분이다.
- **운영 연결엔 막는 설정**: 이 다섯 가지는 `crm_connection.is_demo` 연결에만 열린다.
  - 운영 연결은 env `KOS_TRIAL_WRITES_ON_LIVE=true`(기본 false)일 때만 열린다.
  - 계획(`KosWritePlanner(trial=)`)과 보내기 직전(`write_open(..., trial=)` · `KosAdapter.trial_writes`) 두 곳에서 같은 기준으로 막는다. 닫힌 연결에서는 `payload.kos = not_supported` 로 드러난다.

## 6. 멈춘 로컬 outbox 행
- 새 코드를 올리기 전에 이미 #230 fix1 의 토큰 대기 상한(30분)이 정리했다. **pending 0** 이다.

  | 상태 | 건수 |
  |---|---|
  | confirmed(방 · 담당자 · 호출) | 6 |
  | failed `no staff token in time`(수락 — 로그인 안 한 직원) | 2 |
  | failed `blocked`(그 뒤 첫 시작 · 완료 · 수락) | 11 |

- failed 라 동기화 가드가 풀려 그 칸은 KOS 값을 따른다. 새 규칙으로 다시 보내지 않았다 — 옛 행에는 누른 사람이 없다(수락 actor = 의사). 같은 조작을 화면에서 다시 누르면 새 규칙으로 나간다.

## 7. 실물(데모 지점 KOS 쓰기 · 사용자가 화면에서 누름 · 16:34 ~ 16:45 KST)
새 코드에서 쌓인 op 전부가 **누른 사람 토큰**(`sender_staff_id` 있음)으로 나가 **전부 confirmed** 다. failed 0 · pending/sent 0 이다(상태 · 건수만 · 값 없음).

| 쓰기 | confirmed | 비고 |
|---|---|---|
| `change-tasks-room` | 1 | 호출 1단계 |
| `change-tasks-assignees` | 5 | 호출 2단계 |
| `call-tasks-doctors` | 5 | 처음 호출 + **다시 호출**(이미 WAITING/READY — OQ-09 실물 확인) |
| `change-tasks-doctors` | 3 | 수락 — 누른 사람 토큰 |
| `change-flow-step PROCEDURE` | 1 | 첫 시작 |
| `change-tasks-complete true` | 7 | 종료 |
| `change-tasks-complete false` | 1 | **완료 취소 — 실물 확인**(`status_not = done` 확인) |
| `cancel-flow-tasks` | 2 | **귀가 대기 ① — 실물 확인** |
| `change-flow-step PROCEDURE_DONE` | 2 | **귀가 대기 ② — 실물 확인**(내부 경로 `{id, step}`) |

- **「시작 취소」 `PROCEDURE_WAITING` 은 실물로 나가지 않았다.**
  - 이번 시작 취소 1회는 그 고객에 다른 진행/완료 시술이 남아 `flowStepChanged = false` 였다. 규칙 13 대로 DAY 만 바뀌었다.
  - 확인하려면 고객의 **유일한 진행 시술**을 시작 취소해야 한다. 남은 것에 둔다.
- 옛 코드 때 귀가 대기 2회(16:10 이전)는 `not_supported` 로 남았다. 새 코드의 2회는 op 2개씩 confirmed 다.

## 남은 것
- 「시작 취소」로 고객이 시술 대기로 돌아가는 경우(`PROCEDURE_WAITING`) 실물 1회.
- 운영 연결에 열기(`KOS_TRIAL_WRITES_ON_LIVE`) — 위 실물 결과로 코디 · 사용자 결정. 「시작 취소」 실물 확인 뒤에 켜기를 권한다.
- SPEC: 완료 취소 확인 조건 `status_not = done`(cc `statusNot`) · `sender_staff_id` 옛 행 = event actor 로 대신 찾음 — planner 반영 여부 확인.

## 검증
| 명령 | 결과 |
|---|---|
| `uv run pytest -q -m "not infra"` | 292 passed |
| `scripts/test.sh -q` | 446 passed |
| ruff check · format --check | 통과 |
| compose | down 안 함 · `--profile app up -d --build --wait api worker scheduler` → migration `0005_outbox_sender` 적용 |

새 · 바뀐 테스트:
- DB 없이:
  - 규칙 — 다시 호출 · 앞 수락 무효 · 앞 호출 닫기 · 재호출이 수락 남은 앞 호출을 안 닫음 · 줄 순서 · 국적 · 귀가 대기 판 밖/시술 완료 탭 · 대기 줄 전부 호출 대상.
  - 계약 — trial 쓰기 다섯 가지 계획 · 보내기 직전 가르기 · `status_not` 확인 · 가드.
- infra:
  - 수락된 시술 다시 호출 → 앞 수락 무효 + KOS 호출 다시 + 앞 호출 열림 유지.
  - 대리 수락 op sender = 간호사 · `doctorIds` = 수락 의사.
  - sender 토큰만 쓴다.
  - 데모 연결에서 시작 취소 · 완료 취소 · 귀가 대기 op 적재.
  - 재호출 KOS 호출 다시.
  - 컬럼 스냅샷 · alembic head.
