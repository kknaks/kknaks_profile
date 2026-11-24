import json, os, sys
OUT = sys.argv[1]
MAIN = sys.argv[2]
SRC = "479d8f46a84fa87377a3525f6ccb45d69c399ce4"
RS_PENDING = (f"SPEC 원천 = DAY-SPEC-007(새 · draft · 검수 3차 PASS) + DAY-SPEC-006 개정 ⑫ · DAY-SPEC-002 개정 ㉘ · DAY-SPEC-000 2026-11-24 개정 ② — Mediness PR #961 커밋 {SRC}(브랜치 kknaksss/day-reservation2-spec · 머지 전). "
              "main 에 아직 없어 spec-baseline:pending 으로 시작한다. PR #961 이 main 에 들어가면 같은 idempotency key · contract_version +1 · 새 origin/main SHA 로 재실행해 spec-baseline:ready 로 재결속한다(결과 계약 의미가 같으면 재승인 없음 — requests.md)")
E2E = ("실물 e2e 1회(로컬 · KOS 데모 지점 · check_open_key_is_demo 통과 뒤만): 빈 칸 → 새 고객 [저장 후 예약 등록](같은 고객 찾기 → 새 고객 → 예약) · 기존 고객 예약 · 우클릭 예약 변경(옮기기) · 예약 취소 · "
       "오늘 예약 [접수] → [상담 대기](상담사 = 상담 기록 · 관리실) → [귀가 처리](사유) / 재진 시술만 진행 → 「오늘」 ✓ → [시술 대기](방 배정 · 시술권 작업 · 같은 방 · 오더 메모) → [귀가 처리] / "
       "귀가 대기 → [귀가 처리] · 수납 · 처방전 딥링크가 KOS 웹 탭을 엶 · 동행 저장 · 두 번째 브라우저에 SSE 로 바로 반영 — 각 단계 KOS 상세 다시 읽기로 expect 확인. 순서 조건: ① · ② · ③ 이 다 들어간 뒤 마지막 머지 Issue 에서 1회 · 결과를 세 Issue 에 남김")
COMMON_NON = [
  "문진 · 여권 스캔 · 신분 확인 자동 접수 · 외국인 신분확인 · 상담사 순번 · 고객 차트 · 처방 만들기 · 수납 항목 넣기 · 예약 요청 · 고객 등록 창 · 예약메모 덧붙이기(DAY-SPEC-007 §1 Out Of Scope)",
  "KOS 쓰기를 보낸 즉시 1초 간격으로 다시 읽어 확인하는 일반화(D53 — 다음 스펙 · 이번 판 확인 = 지금 쓰기 큐 확인 그대로 · 예외 = 규칙 28 이벤트 연쇄를 시술권 작업에 넓힌 것만)",
  "「시술현황 차트 일부 기능 수정」(D43 — 다른 사람 몫)",
]
CONTRACT_W = ("계약 W(쓰기 의도 — ① 제공 · ② 소비 · 이름 제안): ② 서비스는 `WriteIntent`(`emr/base.py`)로 쓰기 큐에 넣기만 하고 경로 · 본문 · expect 는 ① `KosWritePlanner` 가 짓는다. 새 intent kind = "
              "`reserve` · `update_schedule`(items 통째 · 일정 · 그룹 · 지정 의사) · `cancel_reservation`(open · CANCELED) · `create_visitor` · `recept` · `flow_step`(값에 CONSULTATION_WAITING · COMPLETED 더함) · "
              "`set_counselor`(계획 단계에서 KOS 상세 consultations[] 를 읽어 create-consultation / change-consultation-counselors · consultationId = 큐에 넣을 때 uuid) · `add_ticket_tasks`(계획 단계에서 KOS get-ticket-bundles {visitorId} 로 본문 · 2xx 뒤 상세 조회로 새 seq → 같은 방 change-tasks-room 이어 쌓기) · `order_memo`(빈 글이면 안 쌓음 D56) · "
              "기존 `add_room_assign` · `assign_room` · `cancel_room_tasks`. 순서 묶음(SPEC-007 §3 「KOS 쓰기」 W1 ~ W17 · [상담 대기] · [시술 대기] · 귀가) = ② 가 한 버튼에 intent 여러 개를 순서대로 · `COMPLETED` 판정 = 계획 / 쓰기 큐(SPEC-002 ㉘ 「판정 자리」)")
CONTRACT_E = ("계약 E(쓰기 결과 신호 — ① 제공 · ② 소비): 쓰기 큐 op 이 confirmed / failed 로 바뀌는 순간 hospital 단위 이벤트(`board_events` 와 같은 Redis pub/sub · 이름 제안 `reservation_events`)에 {visitId, action, opIds, result} 를 싣는다 — ② SSE 가 `write_confirmed` · `kos_failed` · `reservation` 으로 내보냄")
CONTRACT_V = ("계약 V(화면 값 · 조각 — ② 제공 · ③ 소비 · 이름 제안 · SPEC-007 §3 「API 계약」 · 「화면이 읽는 칸」 그대로): 조각 `#reservation-detail`(예약 상세 모달) · 등록 창 조각 · 고객 찾기 목록 조각 · RB-11 같은 고객 창 조각 · `#reservation-main`(기존 · 우클릭 · 옮기기 data-* 추가). "
              "경로 = GET /reservations/visits/{id} · GET /reservations/book?date&group_id&start · GET /reservations/visits/{id}/edit · GET /reservations/customers?q · POST /reservations · PUT /reservations/visits/{id}/schedule · POST …/cancel · …/reception · PUT …/identity · …/doctor · POST …/consultation-waiting · PUT …/counselor · …/room · POST …/procedure-waiting · PUT …/order-memo · POST …/discharge · PUT /reservations/companions/group · POST …/retry · GET /reservations/stream. "
              "모달 값 = stage(10 값 · U-2 판정 = ②) · date_kind(today|future|past) · editable 플래그(칸 · 버튼마다 — 단계 × 날짜 경계 표 판정 = ② · ③ 은 그대로 그림) · customer{name, passport_name, contact(KOS 꼴), birth, age, gender, nationality, is_domestic, notes} · identity{checked} · reservation{assignee, start, end, funnel, memo, doctor{id,name}|null, companions[]} · consult{mode(consult|procedure_only), counselor, room, order_memo, missing[]} · treatments[](U-7 줄 · n/m · today · status 4 키) · payment{base_total|null, discount|null, total, paid, due, warn, done, button(in_progress|pay|none), links{purchase, prescription}|null} · previous_visits[] · discharge_reason · 문구 · 색은 ③(시안) 이 키로 그림")
CONTRACT_S = ("계약 S(SSE — ② 제공 · ③ 소비): `GET /reservations/stream` · 이벤트 `reservation`(data = version → `hx-trigger=\"sse:reservation\"` 로 #reservation-main 다시 받기) · `write_confirmed`(data = {visitId, action} → 열린 모달이 그 방문이면 모달 다시 받기 · 잠금 풂 · 성공 알림) · `kos_failed`(data = 공용 토스트 HTML 조각 + 「다시 시도」 → sse-swap) · `session_expired` · retry 3000 · 15초 ping(시술 현황 /board/stream 과 같음). 10초 조각 폴링(`poll=1` · hx-trigger every)은 없앤다(D52)")
reqs = {}
reqs["be-found"] = {
 "idempotency_key": "day/day-spec-007/be-found",
 "title": "DAY 예약 상세 ① 백엔드 바닥 — KOS 쓰기 계획 · write_open 새 행 · 할인 전 가격 · 권한 키 · 지정 의사 원천 (DAY-SPEC-007 · 002 ㉘ · 000 ②)",
 "risk_level": "L3",
 "target_specs": ["DAY-SPEC-007", "DAY-SPEC-002", "DAY-SPEC-000"],
 "target_delta": [
  "`emr/kos/writes.py` write_open 새 행(SPEC-002 ㉘ 「예약 상세가 여는 경로 · 값」 표 그대로): recept · change-flow-step CONSULTATION_WAITING · COMPLETED(값만) · add-flow-tasks PROCEDURE + ticketConfiguration.ticketId · change-order-memo · reserve(최상위 doctor 막음) · update-reservation(items 통째 · counselor 칸 막음) · create-visitor(countryCode 숫자 · 앞 0 없음) · create-consultation · change-consultation-counselors(빈 배열 막음) · open cancel-reservation(reason CANCELED · open 받는 유일 경로)",
  "`KosWritePlanner` 새 intent 와 expect(SPEC-007 W1 ~ W17 확인 조건 · 지연) · 계획 단계 KOS 읽기 둘(상세 consultations[] → W7a/W7b · get-ticket-bundles → W13 본문 · D48 round) · 규칙 28 이벤트 연쇄 예외를 시술권 작업에 넓힘(2xx 뒤 상세 조회로 새 seq → 같은 방) · COMPLETED 판정 = 계획 / 쓰기 큐(작업 취소 뒤 묶음 · 귀가 대기 ∧ DAY 사본 열린 작업 없음 한 건) · expect 새 모양(reservation_status · visitor · tasks.ticket · order_memo · consultation counselors)",
  "할인 전 가격 — migration `0024_purchase_base_price`(purchase_item.base_price_amount · base_supplied/tax_free/vat_amount · 통화 넷) · 구매 매퍼가 KOS 항목 basePrice.* 를 받음 · 다음 동기화 · 백필로 채움(D33 · D34 · SPEC-000 ②) — **코드 워크트리에 미커밋으로 일부 있음**(0024 · models/purchase.py · mapper_kos_keys_sale.py · column snapshot · alembic test) → 이어서 함",
  "권한 키 `reservation.detail` edit — 데이터 migration `0025_detail_permission`(모든 직무 기본 행 · 되돌리면 그 키 행 삭제 · 키 목록 policies/permissions.py · default_permissions) — **미커밋으로 일부 있음** → 이어서 함 · 귀가 사유 칸 `visit.discharge_reason`(migration 하나 · DAY 에만 · D26)",
  "지정 의사 원천 — 예약 상세 읽기가 visit_occupied_resource_doctor(KOS occupiedResources[].reservationGroup.doctors · 이미 동기화됨)를 쓰게 query 하나 · visit.requested_doctor_id 는 그대로(KOS 가 버려 늘 빔 — SPEC-000 ②) · identity_check status 값 confirmed / unconfirmed",
  CONTRACT_W, CONTRACT_E,
 ],
 "acceptance": [
  "A1: write_open 단위 테스트 — SPEC-002 ㉘ 표 각 행의 허용 · 막힘 본문(최상위 doctor · counselor 섞임 · 빈 counselorIds · reason 자유 글자 · api open 의 다른 경로 · COMPLETED 단독 값은 열리지만 계획이 묶음 밖에서 안 짓는지)",
  "A2: planner 테스트 — intent 마다 경로 · 본문 키 · expect 가 SPEC-007 W 표 · be-probe-1 ~ 4 모양과 같음 · W7a/W7b 판정 · W13 본문 키가 HAR 시술권사용.har 와 같음 · round current 계산(D48) · 빈 오더 메모 안 쌓음(D56) · 이벤트 연쇄로 새 seq 를 찾아 같은 방 op 을 쌓음",
  "A3: migration 업 · 다운(alembic test) · 구매 동기화가 basePrice 를 받음(fixture = HAR 할인.har 키 모양) · reservation.detail 행이 모든 직무에 · discharge_reason 칸",
  "A4: 쓰기 결과 신호(계약 E)가 confirmed · failed 때 한 번씩 · 기존 시술 현황 쓰기 · 동기화 회귀 없음(전체 pytest)",
  "A5: " + E2E,
 ],
 "non_goals": COMMON_NON + ["라우트 · 화면 · SSE 스트림(Delivery ② · ③)"],
 "review_surface": [RS_PENDING, "KOS 외부 쓰기를 새로 여는 범위(write_open 행 하나하나) — L3", "migration 3개(0024 · 0025 · discharge_reason) · 되돌리기", "계약 W · E 이름"],
 "execution": {
  "code_surface": ["backend/day/emr/kos/writes.py", "backend/day/emr/base.py(WriteIntent kind)", "backend/day/dtos/emr_writes.py", "backend/day/services/emr_sync.py(_chain_room_assign 넓힘 · 결과 신호)", "backend/day/emr/kos/mapper_kos_keys_sale.py · mapper_purchase.py", "backend/day/models/purchase.py · visit.py · reception.py", "backend/day/policies/permissions.py · services/default_permissions.py", "backend/migrations/versions/20261124_0024_purchase_base_price.py · 0025_detail_permission.py(미커밋 일부 있음) · discharge_reason(새)"],
  "domain_candidates": [],
  "dependencies": ["없음(바닥) — ② 는 계약 W · E 만 맞추면 병렬"],
  "phases": ["P1 미커밋 migration 0024 · 0025 · 매퍼 이어서 + discharge_reason", "P2 write_open 새 행 · planner intent · expect", "P3 계획 단계 KOS 읽기(consultations · ticket bundles) · 이벤트 연쇄 넓힘 · COMPLETED 판정", "P4 결과 신호 · 회귀 · 실물 e2e(마지막 머지 때)"],
  "verification": ["backend pytest(writes · planner · mapper · migration)", "로컬 KOS 데모 지점 실물 e2e 1회"],
  "predeploy": ["prod migration 0024 · 0025 · discharge_reason 순서 확인 · 백필로 base_price 채움"],
  "rollback": ["Code PR revert + migration downgrade(0024 칸 · 0025 키 행 · discharge_reason 칸 삭제)"],
  "open_questions": ["DAY-SPEC-007 OQ-D25(여러 세트 묶음 round.total)"],
 },
}
reqs["be-flow"] = {
 "idempotency_key": "day/day-spec-007/be-flow",
 "title": "DAY 예약 상세 ② 백엔드 흐름 — 예약 등록 · 상세 읽기 · 단계 쓰기 · 우클릭 · 동행 저장 · 예약 현황 SSE (DAY-SPEC-007 · 006 ⑫)",
 "risk_level": "L3",
 "target_specs": ["DAY-SPEC-007", "DAY-SPEC-006"],
 "target_delta": [
  "라우트(SPEC-007 §3 「API 계약」 표 그대로 · 이름 제안) — 예약 상세 · 등록 창 · 변경 창 · 고객 찾기(DAY 사본만) · 예약 등록(W1 같은 고객 찾기 = 저장 요청 안 R39 예외 · duplicate_token · DAY 사본 없으면 get-visitor 사본 · 새 고객 순서) · 일정 변경(창 · 옮기기 · 같은 날만) · 예약 취소 · 접수 · 신분증 확인(identity_check · DAY 만) · 의사 지정 · 상담 대기(순서 묶음) · 상담사 · 관리실(상담 대기) · 시술 대기(D50 순서 묶음 · 관리실 필수) · 오더 메모 · 귀가(사유 · W12/W14/W15) · 동행 저장(묶음 통째 · R73 검사 · 끌어 놓기 PUT 두 경로 없앰) · 다시 시도",
  "상세 읽기 — 단계 판정(U-2) · 단계 × 날짜 경계 표 editable 판정 · 시술 목록(U-7 · 연결 키 visit_task.ticket_id → ticket → ticket_set → ticket_bundle.purchase_item_id · 상태 4 · n/m · 순서 · 여러 작업) · 수납 정보(visit_amounts + base_price · D51 칸 비움 · 경고 R42 · 배지 R55) · 수납 버튼 셋(D36) · 딥링크(kos_web_base · external_ref) · 상담사(R48 원천) · 이전 방문(재진 · 취소 · 노쇼 뺌) · 지정 의사(visit_occupied_resource_doctor) · 신분확인(그 날 마지막 행)",
  "권한 — 보기 = reservation view · 쓰기 = reservation.detail edit · 동행 = reservation.companion edit · 지난 날 409 reservation_past_date · 단계 바뀜 409 visit_stage_changed · 검사 순서 401 → 403 → 400 → 404 → 409(SPEC-007 케이스 매트릭스)",
  "예약 현황 SSE `GET /reservations/stream`(routers/board_streams.py 를 본뜸 · stream_guard · reservation_events 구독) — 10초 조각 폴링 없앰(D52 · SPEC-006 개정 ⑫) · 날짜 최신화 · 3초 기다림(R43) · 오늘 10초 동기화(R40)는 그대로",
  CONTRACT_W, CONTRACT_E, CONTRACT_V, CONTRACT_S,
 ],
 "acceptance": [
  "A1: 라우트 테스트 — SPEC-007 케이스 매트릭스 줄마다(권한 · 지난 날 · 앞날 접수 · 단계 바뀜 · 같은 고객 창 · 토큰 만료 · 사본 없음 get-visitor · 빠진 칸 · 외국인 상담 대기 회색 · 사유 없음 · 동행 조건) · KOS id 가 응답에 없음(딥링크만 예외)",
  "A2: 쓰기 동작마다 쌓이는 intent 순서가 SPEC-007 W 표 순서 묶음과 같음([상담 대기] W8 → W9 → W10 → W7a/b · [시술 대기] W8 → W9 → W13 ① → ④ → ② → ③ · 귀가 셋) · 화면 요청에서 KOS 를 부르는 곳 = W1 · get-visitor 둘뿐",
  "A3: 상세 값 테스트 — 단계 × 날짜 경계 표 칸마다 · 시술 목록 fixture(지난 시술권 + 이번 구매 · 겹침 제거 · n/m · 취소 = 미진행) · 수납 정보(R52 실측 fixture + 할인 전 빈 칸) · 수납 버튼 넷",
  "A4: SSE — 첫 접속 reservation 1개 · 쓰기 confirmed → write_confirmed · failed → kos_failed 토스트 조각 · 세션 만료 · 권한 없음 끊김 · 다른 병원 이벤트 안 옴",
  "A5: " + E2E,
 ],
 "non_goals": COMMON_NON + ["KOS 쓰기 계획 · write_open · migration(Delivery ①) · 템플릿 · day.js(Delivery ③)"],
 "review_surface": [RS_PENDING, "화면 요청 안 KOS 호출 예외 둘(W1 · get-visitor) — R39", "SSE 로 갈아탐(R41 뒤집음) · 폴링 제거 회귀", "계약 V · S 이름 · 값 모양"],
 "execution": {
  "code_surface": ["backend/day/routers/reservations.py · routers/reservation_streams.py(새 · 이름 제안)", "backend/day/services/reservation_detail*.py · reservation_book*.py(새)", "backend/day/queries/reservations*.py · reservation_inhouse.py", "backend/day/presentation/reservations*.py", "backend/day/dtos/reservation_views.py", "backend/day/policies/reservation_amounts.py(재사용)"],
  "domain_candidates": [],
  "dependencies": ["① 계약 W · E(이름만 먼저 · 구현 병렬 — ① 머지 전엔 가짜 planner 로 테스트)", "③ 와는 계약 V · S"],
  "phases": ["P1 상세 읽기 · 값 · 권한", "P2 예약 등록 · 변경 · 취소 · 고객 찾기", "P3 단계 쓰기 · 동행 저장 · 다시 시도", "P4 SSE · 폴링 제거 · 실물 e2e"],
  "verification": ["backend pytest(라우트 · 값 · SSE)", "로컬 KOS 데모 지점 실물 e2e 1회"],
  "predeploy": [],
  "rollback": ["Code PR revert(폴링 경로가 같이 돌아옴)"],
  "open_questions": ["DAY-SPEC-007 OQ-D07(국가번호 목록 · kakaotalk 밖 SNS 값 create-visitor · etc 이름)"],
 },
}
reqs["fe"] = {
 "idempotency_key": "day/day-spec-007/fe",
 "title": "DAY 예약 상세 ③ 화면 — 예약 등록 창 · 예약 상세 모달 · 우클릭 · 시술 목록 · 수납 정보 · SSE 연결 (DAY-SPEC-007 · 006 ⑫)",
 "risk_level": "L2",
 "target_specs": ["DAY-SPEC-007", "DAY-SPEC-006"],
 "target_delta": [
  "예약 등록 창(RB-01 ~ RB-13 · U-1) · 예약 상세 모달(RD-01 ~ RD-14 · U-2 ~ U-9) · 확인 창(RP-01 ~ RP-05 · U-10 · 시안 문구 그대로) · 우클릭 메뉴 · 옮기기 모드(RC-01 ~ RC-03 · U-11) — 시안 v9 가 정본 · 「뺌」 요소는 그리지 않음 · 문구 짓지 않음 · 시술 목록은 D44 와이어",
  "카드 클릭 = 상세 · 빈 칸 = 등록(지난 날 빼고) · 우클릭 = 메뉴 · **카드 끌어 다른 카드에 놓아 묶기 · 띠 밖 풀기 제거**(D45 · SPEC-006 ⑫) · 띠 표시는 그대로",
  "SSE 연결(계약 S) — 10초 조각 폴링 제거 · sse:reservation 으로 #reservation-main · write_confirmed 로 모달 다시 받기 · 누른 버튼 잠금 · kos_failed 토스트 + 「다시 시도」 · 공지 편집 칸 · 끄는 중에는 안 덮음",
  CONTRACT_V, CONTRACT_S,
 ],
 "acceptance": [
  "A1: SPEC-007 「화면 구성」 넣음 요소가 시안과 같은 모양 · 문구 · 「뺌」 요소 없음 · 시술 목록 = D44 와이어(오늘 ✓ 파란 표시 · 상태 4 문구 · n/m회)",
  "A2: 인라인 스크립트 0 · 손 CSS 0 — static/day.js 이벤트 위임 + data-* · medikit 토큰 · ui.html 매크로(AGENTS.md 「웹 화면」) · 같은 기능 조각 = partials/reservations_*.html",
  "A3: 템플릿 렌더 테스트 — 계약 V 가짜 값으로 단계 × 날짜 경계 표 칸마다(보이는 칸 · 버튼 · 잠금) · 빠진 칸 깜빡임 · 확인 창 다섯 · 우클릭 켜짐 조건 · 수납 버튼 넷 · 할인 전 빈 칸",
  "A4: 끌어 놓아 묶기가 없어졌고 옮기기 모드 끌기만 남음 · 폴링 요청 0(SSE 만)",
  "A5: " + E2E,
 ],
 "non_goals": COMMON_NON + ["백엔드 라우트 · 값 · KOS 쓰기(Delivery ① · ②)"],
 "review_surface": [RS_PENDING, "시안과 모양 · 문구 · CSP · medikit", "계약 V · S"],
 "execution": {
  "code_surface": ["backend/day/templates/partials/reservations_detail*.html · reservations_book*.html · reservations_ctx*.html(새)", "backend/day/templates/partials/reservations_main.html · reservations_parts.html · reservations.html", "backend/day/static/day.js", "backend/day/templates/ui.html(매크로가 모자라면)"],
  "domain_candidates": [],
  "dependencies": ["② 계약 V · S 만 맞추면 가짜 값으로 병렬 · 실물 e2e 만 ① · ② 뒤"],
  "phases": ["P1 예약 상세 모달 틀 · 머리 · 왼쪽 칸", "P2 시술 목록 · 수납 정보 · 아래 버튼 · 확인 창", "P3 예약 등록 창 · 같은 고객 창 · 우클릭 · 옮기기 · 끌어 묶기 제거", "P4 SSE 연결 · 폴링 제거 · 실물 e2e"],
  "verification": ["템플릿 렌더 테스트(pytest) · CSP 검사", "로컬 실물 e2e · 시안 대조"],
  "predeploy": [],
  "rollback": ["Code PR revert"],
  "open_questions": [],
 },
}
for k, r in reqs.items():
    r = {"product_id": "day", "document_root": "products/day", "contract_version": 1, "spec_baseline_revision": MAIN, **r}
    json.dump(r, open(os.path.join(OUT, f"request-{k}.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("ok")
