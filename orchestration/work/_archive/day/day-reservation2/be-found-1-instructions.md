
# [backend · 기반 1] KOS 쓰기 허용 목록 · 계획 + 할인 전 가격 스냅샷 + 권한 키 — 예약 등록 · 상세의 바닥

너는 **day `backend` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/day-reservation2/orchestration/roles/day/backend/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-reservation2`
base 브랜치: `origin/dev` → 최종 PR 대상 `dev` (PR 은 코디네이터가 올린다)

**너는 앞 맥락이 없다.** 이 코드 워크트리는 지금 너 혼자 쓴다(origin/dev `4bf0b4a1` · 깨끗함). 같은 KOS 데모 실물 확인을 한 다른 backend 터미널이 있었지만 코드는 안 만졌다.

## 1. SSOT — 먼저 읽을 것

- 결정: `/Users/kknaks/orca/workspaces/kknaks_profile/day-reservation2/reference/2026-11-24-reservation-detail/reservation-detail-decisions.md`(D1 ~ D53 · **아래 행이 위를 덮음 · 취소선 = 뒤집힘 · D53 = 다음 스펙**)
- **KOS 실물 근거(경로 · 본문 · 값 · 확인 · 지연 — 이것만 믿어라)**: `/Users/kknaks/orca/workspaces/kknaks_profile/day-reservation2/orchestration/work/day-reservation2/be-probe-1-report.md` · `be-probe-2-report.md` · `be-probe-3-report.md` · `be-probe-4-report.md`(각 리포트 끝 「DAY `writes.py` 에 열 때 필요한 것」 표) · 시험 스크립트 `/private/tmp/day-probe-1 ~ 4/`(본문 모양 참고 · 비밀값 없음) · HAR `/Users/kknaks/orca/workspaces/kknaks_profile/day-reservation2/reference/2026-11-24-reservation-detail/*.har`(파이썬 `-I` 로 JSON 만)
- SPEC(진행 중 draft · 고침 1 중 — 바닥 계약은 위 실물과 같다): `/Users/kknaks/orca/workspaces/mediness-mediness/day-reservation2-spec/products/day/20-spec/spec-007-reservation-detail.md`(§ KOS 쓰기 W 표) · `spec-002-procedure-board.md` 개정 ㉘ · `spec-000-data-model.md` 개정 ② — **읽기만**. SPEC 과 실물 리포트가 다르면 실물이 맞고, 다른 곳을 보고에 적어라
- 레포 `AGENTS.md` · `backend/day/emr/kos/writes.py` 머리 주석(쓰기 원칙 · 「(경로 + 값) 단위로 연다」)

## 2. 배경 / 무엇을 바꾸나

예약 등록 창 · 예약 상세 모달(SPEC-007)의 화면 · 흐름 구현은 SPEC 검수가 끝난 뒤 따로 발주한다. 그 전에 **계약이 실물로 이미 굳은 바닥**만 먼저 만든다:

1. **KOS 쓰기 계획 · 허용 목록**(`emr/kos/writes.py` `write_open` · `KosWritePlanner` · `emr/base.py` `WriteIntent` 종류): 새 쓰기를 쓰기 큐(outbox)로 보낼 수 있게. 대상(실물 O 만):
   - 접수 `schedule/v1/commands/recept {scheduleId}`
   - 단계 `change-flow-step` 값 `CONSULTATION_WAITING` · `COMPLETED` 추가(내부 `{id, step}`). **`write_open` 은 경로 + 값만 본다** — `COMPLETED` 의 「열린 작업 없을 때만 · 작업 취소 뒤」 순서는 계획 / 쓰기 큐 순서 묶음에서 지킨다(작업 CANCEL → COMPLETED 를 한 묶음으로 계획하는 API 를 둬라)
   - 시술권 오늘 작업 `add-flow-tasks` `type=PROCEDURE` + `procedureConfiguration{productOptionConfiguration, ticketConfiguration{ticketId, round{total, current}}, medicalServiceConfiguration}` — **본문 값은 보낼 때(계획 단계 · 서버) KOS `ticket/v1/queries/get-ticket-bundles {visitorId}` 를 읽어 채운다**(be-probe-3 ⓐ · D48 round 규칙: total = 장 수 · 목록 순서 첫 AVAILABLE · current = 쓰는 중 / 쓴 회차 + 1). 지금 「방 배정」 ETCETERA 만 여는 판정과 나란히
   - 오더 메모 `schedule/v1/commands/change-order-memo {scheduleId, orderMemo}`
   - 상담사 `consultation/v1/commands/create-consultation {consultationId(uuid4), visitorId, consultationStartedDateTimeUtc, scheduleId, content{text:""}, counselorIds}` · 이미 기록이 있으면 `consultation/v1/commands/change-consultation-counselors {consultationId, counselorIds}`(D49 · be-probe-4)
   - 예약 만들기 `schedule/reservation/v2/commands/reserve`(be-probe-1 §3 본문 · 지정 의사는 **`occupiedResources[].reservationGroup.doctors` 에만** · 최상위 `doctor` 는 `write_open` 이 막는다)
   - 예약 변경 `schedule/reservation/v2/commands/update-reservation`(`occupiedResources.items[]` 통째 · 기존 자원 id)
   - 예약 취소 **공개** `schedule/open/v1/commands/cancel-reservation {scheduleId, reason ∈ CANCELED|NO_SHOW}` — 지금 `write_open` 은 internal 만 받는다 → 이 경로 하나만 open 허용
   - 새 고객 `v1/visitor/commands/create-visitor`(연락처 KOS 꼴: `countryCode` 숫자만 · 앞 0 없음 — be-probe-1 §2) · 같은 고객 찾기 `visitor/v1/queries/find-duplicated-visitor`(읽기 · 쓰기 큐 밖 · 클라이언트 함수만)
   - 작업 취소 `cancel-flow-tasks` CANCEL 은 이미 열림 — 귀가 묶음에서 재사용
   - 각 쓰기의 **확인 조건(expect)** = 실물 리포트의 다시 읽기 칸(늦게 보이는 칸 ≈1s 는 지금 쓰기 큐 확인 방식 그대로 — 10초 회차가 확인. 즉시 다시 읽기 일반화는 D53 = 다음 스펙이라 하지 마라). 지금 expect 형식(`emr.outbox.expect_met` · `emr.sync.guard_of`)에 없는 칸(예: `flow_step` 값 `consultation_waiting` · `completed` · 예약 상태 · 상담 기록 상담사 · 작업 시술권 id · `order_memo`)은 그 형식을 넓혀라
2. **할인 전 가격 스냅샷**(D33 · D34 · D51): 구매 동기화가 항목 `basePrice`(amount · supplied · taxFree · vat · 통화 — HAR `할인.har` 의 `items[].basePrice` 모양)를 `purchase_item` 새 칸으로 받는다(migration — 지금 head `20261123_0023` 다음 번호 · 칸 이름은 SPEC-000 개정 ② 이름 제안을 따르되 기존 `currency · supplied_currency …` 꼴에 맞춰라 — 검수 참고 메모). 빈 값 허용(지난 구매)
3. **권한 키**(D46): `reservation.detail` edit · 모든 직무 기본 — 데이터 migration(앞 작업 `0021_notice_permission` · `0023_companion_permission` 방식 그대로)

## 3. 계약

위 §2 가 계약. 경로 · 본문 · 값 · 확인은 be-probe 리포트 그대로 — 지어내지 마라. 함수 · 클래스 이름은 기존 `writes.py` · `emr/base.py` 관례.

## 4. 먼저 읽을 핵심 파일

`backend/day/emr/kos/writes.py` 전체 · `emr/base.py`(`WriteIntent` · `PlannedWrite` · `WritePlanner`) · `emr/outbox*.py` · `emr/sync.py`(`guard_of`) · `services/emr_sync.py`(`_chain_room_assign` — 이번엔 고치지 않음 · 참고) · `emr/kos/client.py`(`internal` · `open`) · `emr/kos/mapper_purchase.py:125` · `emr/sync_purchases.py` · `models/purchase.py` · `migrations/versions/20261123_0021_notice_permission.py` · `_0023_companion_permission.py` · 테스트 `tests/day/emr/test_kos_board_contract.py` · `test_outbox*.py` · `test_kos_client.py`(계약 테스트 모양)

## 5. allowed_paths — 이 밖은 건드리지 마라

- `backend/day/emr/` · `backend/day/models/purchase.py` · `backend/day/enums/`(필요할 때) · `backend/migrations/versions/`(새 파일 2개 — 칸 · 권한) · `backend/tests/day/emr/` · `backend/tests/day/`(새 테스트 파일)
- 라우터 · 서비스(화면 흐름) · 템플릿 · static 은 **만들지 마라** — 다음 발주

## 6. 구현 단계

1. `writes.py` 새 행 + `write_open` 판정 + 계획 함수 + expect · 계약 테스트(경로 + 값마다 열림 / 막힘 — 최상위 `doctor` · `COMPLETED` 단독 계획 금지 등)
2. 시술권 작업 계획: KOS 묶음 읽기 → 본문 · round 계산 단위 테스트(be-probe-3 · 4 · HAR `시술권사용.har` 의 실제 모양을 고정 입력으로 — id · 이름 값은 가짜로 바꿔라)
3. 할인 전 가격: migration + 모델 + 매퍼 + 동기화 + 테스트(HAR `할인.har` 모양)
4. 권한 키 데이터 migration + 테스트
5. §8 검증

## 7. 범위 제약 — 하지 말 것

- KOS 를 실제로 부르지 마라(테스트는 가짜 클라이언트 · 실물은 이미 확인됨). `deploy/*.env` 읽기 금지
- 커밋 · push · PR 금지. 로컬 스택 · 사용자 포트 · 프로세스 건드리지 마라
- 화면 · 라우터 · SSE · 서비스 흐름은 이번에 없음. D53(쓰기 즉시 확인)도 없음
- 결정에 없는 정책을 만들지 마라 — 막히면 아래 질문 명령

## 8. 검증

```
cd backend && uv run pytest -q <네가 만들거나 고친 테스트 파일만> · uv run ruff check <네가 만진 파일> — 각 1회, 통과하면 반복하지 마라. 테스트 DB 는 로컬 compose — 공유 STG·PROD 금지. 사용자 포트·프로세스를 건드리지 않는다. 실행 못 한 검증은 사유와 함께 pending
```

- 통과할 때까지 고친다. 못 고치면 이유와 함께 보고한다.
- 기존에 이미 깨져 있던 무관한 실패는 "무관"으로 분리해 보고한다.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_cd5ea51a-31a7-4f34-9cf7-ec53af90a280 --from term_e985290c-4bd8-496a-9f3e-ed9ce7c108d2 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "backend 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_cd5ea51a-31a7-4f34-9cf7-ec53af90a280 \
  --text "[worker_done] backend 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_cd5ea51a-31a7-4f34-9cf7-ec53af90a280 --text "[질문] backend: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
