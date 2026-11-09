# planner-spec002-feedback 결과 보고 — done (미커밋)

`products/day/20-spec/spec-002-procedure-board.md` 개정 ⑥ · `log.md` 한 줄 · lint `--strict` 0 error.

| F | 고친 곳 |
|---|---|
| **F3** 다시 호출 | U-3 체크박스 = 대기 줄(준비중 · 호출 · 수락) · U-4 · 용어 「유효 호출」 = 가장 최근 호출(D-25 · D-27) · 호출 상태도(수락됨 → 닫힘) · 닫힘 = 그 호출을 유효 호출로 갖는 시술이 없을 때 · 규칙 5(대기 시술 · 다시 호출 시 앞 수락 무효 · 앞 호출 closed_at) · 6(재호출 = 같은 규칙) · 7(유효 = 가장 최근 · 새 수락이면 KOS 담당 의사 새로) · 매트릭스 `task_not_pickable` = 진행중 · 완료 · 「cc 와 다른 곳」 호출 대상 줄 → 「cc 와 같음」 |
| **F4** 줄 순서 | U-3: 진행중(시작 순 · 같으면 오더) → 준비중 · 호출 · 수락(오더 순) → 완료(완료 시각 순) — cc `rules.py` · SPEC-003 §5.9 |
| **F5** 귀가 대기 | U-1 판 조건 = `procedure_waiting` · `procedure` 만 · U-2 · U-9 · S-5 · 방문 단계 상태도 · 표 · 규칙 1 · 17 · 18 · 마취 줄 · 매트릭스 `visit_home` 문구 · 「cc 와 다른 곳」 새 줄 — 판에서 바로 빠지고 「시술 완료」 탭에만 · `visit.room_id` 는 마지막 방 |
| **F6** E09 · E10 | 화면 구성 표 「셸 — 뺌」 새 줄(자리도 안 그림) · E06 · E08 은 자리만 그대로 · 1차 범위 표 |
| **F7** 국적 | 바이탈 줄 = 성별 \| 만 나이 \| 국적(`customer.nationality` 그대로 · 없으면 안 그림 · OQ-02-1) · 입실 안 보임 · 판 · 인박스 · 시술 완료 탭 같은 줄 · 스냅샷 `customer.nationality` |
| **F10** 토큰 | 규칙 9 · 24 = **누른 사람 토큰**(대리 수락은 누른 간호사 · KOS `doctorIds` = 수락한 의사 · DAY 에 남기는 건 수락한 의사뿐) · 수락 KOS 행 · 닫은 OQ-05 바로잡음(로그인 안 한 의사 → 뒤 쓰기 멈춤 결과 삭제) |
| **F10** 쓰기 열기 | KOS 쓰기 표 시작 취소 · 완료 취소 · 귀가 대기 1 · 2 = 「cc 구현 근거로 연다」(cc `domain/kos_ops.py` · 실호출 K2 · K4) · 규칙 13 · 14 · 17 · S-5 · S-6 의 W6 「닫음 · 되돌림 감수」 걷음 · HAR 요청에서 OQ-08 · OQ-10 걷고 「닫은 것」에 OQ-08 · 10 줄 |

## 주의 · 새 OQ

- **방배정.har 에 `PROCEDURE_WAITING` 없음** — 원천 「결정 — KOS 쓰기」는 근거로 「방배정.har 의 PROCEDURE_WAITING」을 들었지만, `시술현황_방배정.har` 의 commands 는 `change-tasks-room` 하나뿐이다(확인). SPEC 의 근거는 cc 코드(`kos_ops.py`)와 cc 실호출(K4)로 적었다. 또 cc 는 단계 변경을 **공개** `schedule/open/v1/commands/change-flow-step {scheduleId, step}` 로 보냈고, DAY 표는 HAR 로 확인된 **내부** `schedule/v1/commands/change-flow-step {id, step}` 에 그 값을 싣는다 — 데모 실물 확인에서 같이 본다.
- **재호출 재전송(OQ-09)은 여전히 닫힘** — 결정은 귀가 대기 · 시작 취소 · 완료 취소만 열었다. F3 로 「이미 호출 · 수락된 시술을 다시 호출」이 생겼으므로 KOS 에는 방 · 담당자만 반영되고 KOS 호출은 처음 그대로다(수락하면 `change-tasks-doctors` 로 담당 의사는 바뀜). cc 는 보냈었다 — 열려면 사용자 결정.
- **OQ-21(새 · 코디 확인)** — 누른 사람 토큰을 쓰려면 outbox 가 보낼 직원을 알아야 한다. 수락은 `event_log.actor_staff_id` 가 수락한 의사(U4)라 그 칸으로 찾을 수 없다. 제안: `external_outbox` 에 보낼 직원 칸(예 `sender_staff_id`) — DAY-SPEC-000 변경이라 이번엔 하지 않았다.
- 개정 ⑤(W6) 머리말 줄은 이력으로 두고 개정 ⑥ 이 그것을 바꾼다고 적었다. #230 계약(v5)의 W6 문구는 아직 「닫음」이다 — 다음 계약 판에서 맞춰야 한다.
