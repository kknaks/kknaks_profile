
# 재개 노트 — day-reservation2 (day)

**지금**: **마감(2026-11-24)** — 코드 CENTURION_DAY#280 dev `55e60aa4` · dev 배포 성공(migration head 0028 · 에러 0) · 스펙 mediness #961(`ea283f0c`) · #962 SPEC-007 stable · #963 Delivery 마감 · Delivery #275 ~ #278 재결속 v2 · conformant · CLOSED · 회고 `para/projects/company/day/log/2026-11-24-day-reservation2.md` · 개념 보강 3 · 로컬 스택 · DB · env 사본 삭제 · 워크트리 2 · 워커 터미널 6 정리 · 아카이브. 남은 것 = 회고 §7(B42 SSE 연결 한도 · day.js 분리)
**⚠ PR 올리기 전 반드시 CENTURION_DAY `origin/dev` fetch → rebase**(사용자 11-24 「dev 움직일 거라 rebase 까먹으면 안 돼」 · migration 번호 · alembic head 이어지는지 확인)
**다음**: planner 완료 → reviewer_doc 검수 발주(묻지 않고) → 통과면 planner WORK → be · fe

세팅: `scripts/new-work.sh day day-reservation2` · 설정 SSOT `config/projects/day.json`
코디handle: `term_cd5ea51a-31a7-4f34-9cf7-ec53af90a280` · Run `run_d7fa3faac7f9`(재시작 뒤 `orca orchestration run-use --id`)

프로젝트·회고·당시 문서의 탐색은 이 폴더의 작업 목차(`README.md`)가 맡는다.
`sync-work-links.py`로 생성하며, 종료 후에도 프로젝트에서 같은 작업을 찾을 수 있어야 한다.

## 워크트리

- `spec`: `/Users/kknaks/orca/workspaces/mediness-mediness/day-reservation2-spec` (branch `kknaksss/day-reservation2-spec` · base `origin/main` `c43633be`)
- `code`: `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-reservation2` (base `origin/dev` `4bf0b4a1` → PR `dev`)
- 코디 = 이 워크트리(`kknaks_profile/day-reservation2` · 브랜치 `kknaksss/day-reservation2`). spec · code 워크트리는 SPEC 단계에서(code 는 CENTURION_DAY origin/dev 최신 fetch 뒤 — 11-24 `4bf0b4a1`)


## 1. 지금

열린 것만 둔다. 닫히면 지우고 §5 이력으로 내린다.

- [x] planner SPEC — 결정 파일 `reference/2026-11-24-reservation-detail/reservation-detail-decisions.md`(D1 ~ D48 · 와이어)
- [ ] reviewer_doc 검수 → WORK(30-work) → be · fe 병렬 → reviewer(code) → 로컬 e2e(사용자) → **dev rebase** → PR

## 2. 결정 (SoT)

| 날짜 | 결정 | 근거 |
|---|---|---|
| 2026-11-24 | 이번 작업 = 예약 현황 카드를 누르면 뜨는 **예약 상세 모달**(시안 v9 `20261124_예약현황_시연.html` `detailV6Html` · 머리 = 단계). 앞 작업 R2 「상세 모달 뺀다」를 이번에 넣음 | 사용자 「이런 모달을 이제 만든다고」 |
| 2026-11-24 | 순서 = 작업 폴더 → 읽기 전용 조사(칸 · 버튼 원천 전수) → 범위 결정 → SPEC | 사용자 「그렇게 하자」 |
| 2026-11-24 | 시안 「예약 카드 만들기」 = **예약 등록 창**(시안 `openBook` · 기존 고객 / 새 고객 [저장 후 예약 등록]) — 예약 단계 논의에 넣음. 논의는 예약 → 귀가 대기 단계 순서로 하고(구현 순서 아님) 다 닫은 뒤 최종 SPEC 발주 | 사용자 「우리 논의를 하자 · 실제 kos 에 등록되는지 논의하고 최종 스펙 발주」 |
| 2026-11-24 | KOS 쓰기 = DAY 내부 API 모듈(`emr/kos/client.py` `internal()`) 위에 cc 경로 · 본문을 가져와 연다(**ext = 외부 연동 · 고려 대상 아님** — 사용자 11-24) · 확인은 데모 지점 실물(SPEC-002 OQ-23 · `writes.py` 머리) — HAR 필수 아님 | 사용자 「우리 내부 api 로 쓸거고 별도 모듈 있잖아」 |
| 2026-11-24 | 예약 등록 창 「열」 = **예약 그룹**(`reservation_group` · 예약 현황 세로 열과 같음 R6) — KOS `reserve` 본문 `reservationGroup.reservationGroupId` | 사용자 「열은 예약그룹으로 하자」 |
| 2026-11-24 | 초진 / 재진 = KOS 가 정함(`reserve` 본문에 칸 없음 · 응답 `visitor.isNew` → `visit.is_new`). 등록 창은 새 고객일 때만 「초진」 배지(시안) · DAY 가 따로 판정하지 않음 | 코디 확인(cc `reservations.py` `create` 본문 · DAY `mapper.py:602`) · 사용자 질문 답 |
| 2026-11-24 | 예약 등록 「담당자」 = **로그인한 직원**(예약하는 사람) — KOS `reserve` 본문 `reservationAssignee` = 그 직원의 KOS 직원 id(시스템 계정 아님). 칸은 그 직원으로 채워 보여 줌 · 바꾸기 없음(코디 기본) | 사용자 「로그인 한 사람이 예약하니까 그 사람이 담당자」 |
| 2026-11-24 | 새 고객 = **[저장 후 예약 등록]: KOS 에 고객을 먼저 만들고 그 KOS 고객 id 로 예약을 만든다.** 순서(cc `create` · `_new_visitor`) = ① `visitor/v1/queries/find-duplicated-visitor`(같은 고객 있으면 멈추고 그 고객 제시) ② `v1/visitor/commands/create-visitor`(이름 · 발음 · 성별 · 국적 · 생년월일 · 연락처 · SNS 한 번에) ③ DAY `customer` 사본 ④ `schedule/reservation/v2/commands/reserve`(visitorId) ⑤ 그 일정 다시 읽어 DAY `visit` 사본. ② 뒤 ④ 실패 = 고객은 남음 → 다시 시도는 예약만(코디 기본) | 사용자 「저장 후 예약 만들기가 맞고 kos 에 새 고객 등록 · 그거 가지고 예약」 |
| 2026-11-24 | 예약 등록 `reserve` 본문 = 담당자(로그인 직원) · 시간(끝 = 시작 + 그룹 간격) · 예약 그룹 + 구역(자리 남은 첫 구역 — cc) · 유입 경로(`funnel` · `funnelDetail`) · 예약 메모. ~~지정 의사 = KOS 에 빈 값(`doctors: []`)~~ → (같은 날 뒤집음) **지정 의사 = 칸 보임 · 목록 = 직원 중 의사 · 고르면 KOS 에 실어 보냄 · 「지정 안 함」이면 빈 값**(사용자 「리스트는 보여주니까 의사 있으면 넣어서 kos 에 줘야지」). 실을 자리 = KOS 읽기에 둘 — `reservation.doctor`(DAY `requested_doctor_id` · `mapper.py:581`) · `occupiedResources[].reservationGroup.doctors` — 어느 쪽이 들어가는지 데모 실물로 정함(cc 는 늘 빈 값이라 근거 없음). **희망 시술/예산 = 이번엔 뺌**(예약 메모에 같이 씀) | 사용자 「지정 의사는 빈 값으로 · 희망 시술/예산은 예약 메모에 다 같이 쓰니까 일단 빼자」 |
| 2026-11-24 | KOS 데모 실물 확인을 워커로(새 고객 · 예약 만들기 · 의사 두 자리 · 변경 · 취소) · 쓰기 경로 = 쓰기 큐 · 예약 취소 = 공개 API(추천 승인) · 그동안 논의는 다음 단계로 | 사용자 「워커 보내서 확인해 보고 우리는 다음으로 가자」 |
| 2026-11-24 | 접수 = **오늘 예약** 카드를 눌러 예약 상세 → [접수](KOS 내부 `schedule/v1/commands/recept`) · 앞날 예약엔 [접수] 없음(시안 `today`) | 사용자 「오늘 예약 중에 카드 클릭해서 접수」 |
| 2026-11-24 | [문진 QR] · [여권 스캔] = 이번엔 **버튼 자리만 · 비활성**(동작은 다음 스펙 = 앱) · 안내 문구 짓지 않음 | 사용자 「버튼은 만들어 줘 · 다음 스펙이 앱 배포」 · 「응」 |
| 2026-11-24 | 상담사 · 관리실 = 예약 · 접수에선 화면에 담았다가 [상담 대기] 때 한 번에 KOS · **상담 대기에선 고르면 바로 KOS**(상담사 = `update-reservation` `counselor` · 관리실 = `change-tasks-room`) · **상담 진행부터 잠금(보기만)** | 시안 L2341 · L2345 · 사용자 「응」 |
| 2026-11-24 | 상담사 목록 = **목록만**(「다음 차례」 배지 · 순번 = 다음 스펙). 「상담중」 흐림도 이번엔 없음(코디 기본 — 사용자 「리스트만」) | 사용자 「상담사 다음 턴은 다음 스펙 · 상담사 리스트만 보여주자」 |
| 2026-11-24 | **실물 확인 1 결과(데모 지점 · DAY `KosClient`)**: 같은 고객 찾기 · 새 고객(9/9 칸) · 예약 만들기 · 예약 변경(날짜 · 다른 날 · 그룹 · 의사) · 예약 취소 **전부 들어감**. 지정 의사 자리 = `occupiedResources[].reservationGroup.doctors`(최상위 `doctor` 는 200 주고 버림) · 연락처 = `countryCode` 숫자만 · 앞 0 없음 · 취소 `reason` = `CANCELED` enum · reserve 직후 담당자 · 유입은 수 초 늦게 보임(확인 조건에 기다림 필요) · 취소는 `reservation.status` 에만 드러남 | `be-probe-1-report.md` |
| 2026-11-24 | ⚠ DAY 동기화가 지정 의사를 `reservation.doctor`(`mapper.py:581` → `visit.requested_doctor_id`)에서 읽음 — KOS 는 `reservationGroup.doctors` 에 둠 → 읽는 자리 고칠 것(SPEC 에 넣음) · 의사 목록 = 직무 태그 `doctor`(데모 활성 원장은 면허 번호 없음 — 면허로 거르지 않음) | 실물 확인 1 §이슈 2 · 3 |
| 2026-11-24 | 상담사 목록 = 직무 태그 `counselor` 만(활성 · 시스템 계정 뺌) | 사용자 「상담사 목록 → 상담」 |
| 2026-11-24 | 관리실 목록 = **비어 있는 방부터**(그 방에 지금 있는 오늘 방문 수 적은 순 · 시안 「빈 방 위」) · 정원 숫자는 안 보임 | 사용자 |
| 2026-11-24 | 신분확인 · 초진 문진 · 건강정보 = **줄은 두고 값은 비움**(다음 스펙에서 채움) — 단 **내국인 「신분증 확인」 체크는 이번에 동작**(DAY 기록 `identity_check` · KOS 쓰기 없음) | 사용자 「줄은 두고 값을 비울거야」 · 「신분확인 버튼 누르면(한국인)은 되니까」 |
| 2026-11-24 | [상담 대기] 켜는 조건 = **시안 그대로 신분확인 + 상담사 + 관리실**(빠지면 회색 · 누르면 빠진 칸 깜빡임). 외국인 여권 스캔은 다음 스펙 | 사용자 「일단 다 있는 걸로 · 바로 다음 스펙」 |
| 2026-11-24 | [상담 대기] 쓰기 = 시술 현황 방 배정과 같은 쓰기 큐 연쇄(방 배정 작업 → 방 지정 → `change-flow-step` `CONSULTATION_WAITING` — 이 값 새로 엶) · 실패 = 「다시 시도」 · 시술 현황과 같은 토스트 / 접수 취소(되돌리기) 없음 | 사용자 「5번 · 6번 그렇게」 |
| 2026-11-24 | 외국인 신분확인(여권 스캔 전 [상담 대기] 막힘) = **사용자가 처리** · 코디가 이번 판에서 다루지 않음 | 사용자 「내가 처리할거야 걱정 ㄴㄴ」 |
| 2026-11-24 | 내국인 「신분증 확인」 = **확인 true / false 만** 남김(번호 · 사진 없음) · **체크해도 접수로 안 바뀜 — 접수는 [접수] 버튼을 눌러야만**(시안 자동 접수 안 따름) | 사용자 「확인이라고 tf 만 보내는 거야 · 접수 버튼을 명시적으로 눌러야 접수」 |
| 2026-11-24 | **실물 확인 2 결과**: 접수(`recept` · status → `IN_PROGRESS`) · 「방 배정」 작업 · 방 지정(→ READY) · `CONSULTATION_WAITING`(지금 `write_open` 이 막음 → 열 것) · 상담사 바꾸기(`update-reservation {counselor}` — 다른 칸 안 지움) · 관리실 바꾸기 **전부 들어감**. **귀가 `COMPLETED` 는 열린 「방 배정」 작업이 있으면 내부 · 공개 다 400**(`procedures NotAvailable`) → 작업 닫기(`cancel-flow-tasks` CANCEL / DELETE) 뒤 내부 `{id, COMPLETED}` 200. `change-tasks-complete` 는 상담 단계에서 400. **접수 뒤 예약 취소 = KOS 가 막음**(`status NotAvailable`). API 로 `CONSULTATION` 에 넣어도 상담 기록은 안 생김(상담은 차티 · KOS [상담 시작] 몫) | `be-probe-2-report.md` |
| 2026-11-24 | 상담 대기 · 상담 진행 [귀가 처리] = **「방 배정」 작업 취소(`cancel-flow-tasks` CANCEL) → 내부 `change-flow-step {id, COMPLETED}`**(`write_open` 에 COMPLETED 를 이 동작 한정으로 엶) · 귀가 사유 = DAY 에만 저장 · 귀가 완료 화면 「귀가 사유」 칸에 보임 · 상담 진행 중 귀가 허용 · 접수 뒤 [예약 취소] 숨김(KOS 가 막음 · 시안도 예약 상태만) | 사용자 「취소로 가자 · 나머지는 추천으로」 |
| 2026-11-24 | 예약 상세 오른쪽 **「시술 목록」 디자인 바뀜 예정** → 새 시안 받을 때까지 줄 단위 · 진행/미진행 규칙 정하지 않음(열림) | 사용자 디자인 피드백 「이거 디자인을 좀 바꿀거야」 |
| 2026-11-24 | 시술 목록 = 줄은 **이번 방문 수납(구매) 항목 전체**(상품 → 구성) · **「오늘」 칸 = 오늘 받을 시술에 파란 체크 표시만**(체크박스 아님 · 읽기 전용) · **「상태」 = 시술 진행 상태**(시술 현황 `visit_task` 값 · 「오늘」과 따로) · **「[할인] 지인 할인」 같은 할인 줄은 뺌** | 사용자 「오늘 받을 거는 체크 · 상태는 시술 진행 상태 · 파란색 체크 표시만 · 지인 할인은 뺄 거야」 · 줄 범위는 아래 행(지난 시술권 + 이번 구매)으로 넓힘 |
| 2026-11-24 | 「오늘」 연결 키 = **`visit_task.ticket_id` → `ticket` → `ticket_set`(진료항목 = 구성) → `ticket_bundle.purchase_item_id`**. HAR `수납시술추가.har`: KOS 는 수납(`add-pending-purchase-items` · `register-purchase`) 뒤 시술권 묶음이 `purchaseItemId` 를 갖고, 오늘 시술(`add-flow-tasks`)은 `ticketConfiguration.ticketId` 로 그 시술권을 가리킴. DAY 는 이미 `visit_task.ticket_id` 를 채움(`sync_schedule_sales.py`) — 새 동기화 불필요 | 코디 확인(HAR · DAY 모델 `ticket.py` · `task.py`) |
| 2026-11-24 | 시술 목록 「상태」 = **전 / 중 / 후 / 미진행** — 오늘 받는 줄: 시작 전 = 전 · 진행중 = 중 · 완료 = 후 / 오늘 안 받는 줄(오늘 작업 없음) = 미진행. 화면 글자 = **「시술 전」 · 「시술 중」 · 「시술 후」 · 「미진행」**(사용자 11-24) | 사용자 「전중후 미진행으로 가면 되는 거 아니야」 |
| 2026-11-24 | 예약 상세 수납 정보 = **원내 현황 카드 금액 그대로**(같은 계산 `policies/reservation_amounts.py`): 총 수납 금액 = 「총 합계」(결제총액 R51) · 수납 완료 = 수납(R49) · 수납 필요 = 미수(R50) · 경고 · 「수납 완료」 배지 = R42 · R55 그대로. 상품 합계 · 할인 금액 = 사용자 HAR 로 할인 원천 확인 뒤 정함 | 사용자 「원내 현황 사이드에 있는 거 그대로 아니야」 |
| 2026-11-24 | 오늘 시술이 시술 현황에서 **취소**된 줄 = 「미진행」(「오늘」 ✓ 도 빠짐) | 사용자 「취소도 미진행으로」 |
| 2026-11-24 | 할인 HAR(`할인.har`) 확인: KOS 할인 = `purchase/v1/commands/adjust-purchase-price {purchaseId, adjustmentId, adjustment{method FIXED_AMOUNT / PERCENTAGE, value}}` · 취소 `cancel-purchase-price-adjustment` · 결제 때 항목별로 나눠짐(`source DISTRIBUTED`). 구매 조회 = 항목 `basePrice`(원가) · `priceV2`(할인 뒤) · `priceAdjustments[]`. **DAY 저장: `purchase_item.price_amount` = `priceV2`(할인 뒤)만 · 원가 `basePrice` 안 받음 · `purchase_price_adjustment` 는 관계 칸만(방식 · 값 없음) · `adjusted_amount` 는 환불용(할인 아님)** → 할인 금액을 보이려면 원가를 새로 받아야 함 | 코디 확인(HAR · `mapper_purchase.py:125` · `models/purchase.py:165`) |
| 2026-11-24 | **할인 전 가격을 저장한다** — 구매 동기화가 항목 `basePrice`(amount · 필요하면 supplied · taxFree · vat)를 `purchase_item` 새 칸으로 받음(migration 1 · 매퍼 · 동기화). 수납 정보 **상품 합계 = 이번 방문 살아 있는 구매 항목 할인 전 가격 합 · 할인 금액 = 할인 전 합 − 할인 뒤(`price_amount`) 합**. 이미 받은 구매는 다음 동기화 · 백필로 채워짐(빈 동안 처리는 SPEC 에서) | 사용자 「우리도 그걸 저장하면 계산 가능한 거 아니야」 · 11-24 「추천으로 가자」 — 메뉴 정가(`product_option.price_amount` · 지금 값) 조인이 아니라 **구매 스냅샷에 할인 전 가격 추가**로 확정 |
| 2026-11-24 | [n원 수납] = **KOS 웹 딥링크**(cc `reservations.py` `_links`): `{KOS_WEB_BASE}/{tenant}/reservation/schedule/?visitorId=…&scheduleId=…&tab=purchase` 새 창 · KOS 쓰기 없음. 같은 방식 [처방전 출력] = `tab=etceteraWork` 후보(귀가 대기에서 정함). 수납 버튼 상태 = 아래 행 | 사용자 「cc 에 수납하기 하면 kos 웹 열어 주는 거 있지 않아」 |
| 2026-11-24 | 수납 버튼 상태 = **KOS 상태 동기화로 모든 직원에게 같게**: 이번 방문에 KOS 「수납 중」 구매(`purchase.status = initialized` ∧ `process = pending` — HAR 두 개에서 확인: 담아 둠 = INITIALIZED · PENDING · 결제 끝 = ACCEPTED · NOT_IN_PROCESS) 있으면 **「KOS에서 수납 중」 비활성** / 없고 미수 > 0 = **[n원 수납]**(KOS 웹 수납 탭) / 미수 0 ∧ 결제총액 > 0 = **수납 완료**. 수납 중이 결제 없이 끝나면 다시 수납 버튼. 다시 수납도 **시안 문구 [n원 수납] 그대로**(금액 = 남은 미수 · 「다시 수납하기」 안 씀) · 완료 = 버튼 사라지고 수납 정보 「수납 완료」 배지 · 「수납 중」이 KOS 에 남으면 그대로 보임(KOS 에서 정리) | 사용자 「동료가 봤을 때 수납 중인지 알 수 있어야 하고 비활성 · 동기화로 수납 완료 / 다시 수납」 · 코디 HAR 확인 |
| 2026-11-24 | 시술 대기 · 시술 진행 [귀가 처리] = 확인 창(시안 `s5Pop` — 귀가 대기 전 = 사유 필수 · 미수 있으면 경고) **뒤에만** 안 끝난 시술 작업 취소 → `COMPLETED`(실물 확인 3) · 확인 창 문구 = 시안 그대로만(귀가 대기 전 = 사유 필수 · 미수 = 경고) · 「시술이 취소돼요」 안내 추가 없음(사용자 11-24) | 사용자 「귀가 처리에서 취소하기 전에 모달 필요할 듯」 |
| 2026-11-24 | ~~[처방전 출력] = 이번에 못 함~~(코디 오독) → **[처방전 출력] = KOS 웹 딥링크(cc 와 같음) `…/reservation/schedule/?visitorId=…&scheduleId=…&tab=etceteraWork` 새 창** — 처방은 KOS 에서 함(DAY 가 처방을 만들지 않음) | 사용자 「처방은 KOS 에서 한다니까 · KOS 띄우라고 cc 처럼」 |
| 2026-11-24 | 귀가 대기 [귀가 처리] = 확인 창(사유 없음 · 미수면 경고) → 바로 내부 `COMPLETED`(작업은 시술 현황 [귀가 대기]가 이미 닫음 — 실물 확인 3) | 사용자 「2번도 그렇게 해」 |
| 2026-11-24 | 시술 목록 줄 = **고객의 지난 시술권 중 남은 것 + 이번 방문 구매(상담하며 추가)** — 동기화로 계속 갱신. 같은 구매 항목은 한 줄(`ticket_bundle.purchase_item_id` 로 겹침 제거). **재진 접수 때 이 목록에서 「오늘」을 체크**(접수 단계만 누를 수 있음) · 체크가 있으면 오더 메모 칸 나타남 · 그 뒤 단계는 읽기 전용 ✓. 시안의 시술권 카드 대신. 수납 정보 숫자는 이번 방문 구매만(R49 ~ R51 그대로) | 사용자 「재진 접수할 때 시술 목록에 띄워 주고 오늘에 체크 · 체크되면 오더 메모」 · 「지난 시술권 남은 거 + 이번에 상담받으면서 추가한 걸로 계속 업데이트」 |
| 2026-11-24 | **「시술만 진행」 체크는 남김(명시적으로 켬)**: 켜면 시술 목록 「오늘」을 접수 단계에서 누를 수 있고 아래 버튼 = [시술 대기] · 끄면 「오늘」 읽기 전용 · 버튼 = [상담 대기]. 시안의 시술권 카드는 시술 목록 「오늘」 체크로 대신(카드 없음) · 오늘 체크 · 오더 메모는 [시술 대기] 누를 때 한 번에 KOS(`add-flow-tasks` 시술 작업 + 시술권 id · `change-order-memo`) | 사용자 「시술만 진행 버튼을 명시적으로 체크해야」 · 「3번은 추천」 |
| 2026-11-24 | 시술 목록 상품명 오른쪽 끝 = **「{n/m회}」**(시술권 있는 줄) — m = 그 시술권 묶음 전체 회차(`ticket` 중 `canceled` 뺀 수) · n = 쓴 회차(`used` + `in_use` — `in_use` = 오늘 작업에 잡힌 것 · 코디 기본) | 사용자 「상품명 - {n/m회} · 오른쪽 끝에 회차」 |
| 2026-11-24 | 「시술현황 차트 일부 기능 수정」 = **다른 사람 몫 · 이번 범위 밖** | 사용자 「이거 다른 사람이 해」 |
| 2026-11-24 | 시술 목록 = **코디 와이어(오늘 합의)가 정본**으로 만든다(지난 시술권 + 이번 구매 · 오늘 ✓ · 상태 · `n/m회`) | 사용자 「시술 목록은 일단 너가 만들어 봐」 |
| 2026-11-24 | 우클릭 메뉴 = **시안 동작 그대로**(예약 변경 = 점선 옮기기 모드 → 끌어 다른 칸 · 예약 취소 = 확인 창 · 동행 추가 = 예약 상세 열고 「동행」 체크 목록 — 같은 열 · 같은 시작 시각 · 묶음 통째 저장 · 예약 변경으로 옮기면 동행에서 빠짐). 켜짐 조건 = 시안(L2898). **동행 = 시안 기준 · 카드 위 끌어 놓기 묶기(R66 입구) 없앰** — 끌기는 옮기기 모드에서만(사용자 11-24 「시안 기준으로 갈 거야」) | 사용자 「시안 동작으로 동행 우클릭 반영해야 해」 |
| 2026-11-24 | (기본값 · 사용자 이의 없음) 권한 = 새 키 하나(`reservation.detail` edit · 모든 직무 · 데이터 migration) · 지난 날 = 보기만 · 노쇼 = 머리 「노쇼」 빨강 · 버튼 없음 · 특이사항 = `customer_notes` · 이전 방문 = 재진만 · DAY DB · 이름 누르기 = 「준비중입니다」 · 예약메모 = 보기만 | 코디 기본 11-24 |
| 2026-11-24 | **실물 확인 3 결과**: 시술권 오늘 작업(`add-flow-tasks` PROCEDURE + `ticketConfiguration` — 시술권 AVAILABLE → IN_USE) · 오더 메모(`change-order-memo`) · **방 배정 없이** `PROCEDURE_WAITING` · 시술 중 귀가 = 안 끝난 작업 CANCEL(시술권 IN_USE → AVAILABLE 되돌아감) → `COMPLETED` · 귀가 대기 → `COMPLETED` **전부 O**. 미확인: 다회권 `round{total,current}` 값(ticket 에 회차 칸 없음 · 워커가 순서로 지어 넣음 → 다회권 HAR 필요) · `change-tasks-complete` 되는 조건(시술 현황 몫 · 이번 범위 밖). `writes.py` 새로 열 것 = `recept` · 시술권 `add-flow-tasks` · `change-order-memo` · `CONSULTATION_WAITING` · `COMPLETED`(작업 취소 뒤 순서 묶음) | `be-probe-3-report.md` |
| 2026-11-24 | 시술권 오늘 작업 `round` **확정**(HAR `시술권사용.har` · 세라핏 3회권): `total` = 시술권 장 수(3) · 고르는 시술권 = 목록 순서 첫 `AVAILABLE` · **`current` = 이미 쓰는 중 / 쓴 회차 + 1**(1회차 `469735eb` IN_USE 뒤 2번째 = `9bf521e8` · `current 2`). 한 요청에 시술권 여러 개(다른 묶음) 같이 보낼 수 있음 | 코디 확인(HAR #15 · #21 · #28) |
| 2026-11-24 | **상담사 = 상담 기록의 상담사**(OQ-D08 닫음): KOS 「상담사 지정」 = `consultation/v1/commands/create-consultation {consultationId(새 uuid), visitorId, scheduleId, consultationStartedDateTimeUtc, content{text:""}, counselorIds[]}`(HAR `상담사 지정.har`) → DAY `consultation.counselor_id` · R48 · R57 원천 그대로 맞음. ~~`update-reservation {counselor}`~~ 로 쓰지 않음. 상담 대기에서 바꾸기 · 차티 [상담 시작]과 겹침 · 단계 영향은 실물 확인 4 | 사용자 「상담 기록에 상담사인데」 + HAR |
| 2026-11-24 | **시술만 진행 [시술 대기] = 관리실 배정 포함**(OQ-D09 닫음): 「방 배정」 작업 + 방 지정 + 「오늘」 ✓ 시술권 작업들(방 지정) + 오더 메모 → `PROCEDURE_WAITING`. 관리실 필수 | 사용자 「시술만 진행하면 바로 관리실 하나 배정 · 방 배정 + 시술들 넣어 줘야지」 |
| 2026-11-24 | 할인 전 가격이 빈 지난 구매 = **상품 합계 · 할인 금액 칸 비움**(OQ-D15 닫음 · 지난 것은 어쩔 수 없음) | 사용자 「추천으로 가자」 |
| 2026-11-24 | ~~쓰기 결과 = 이벤트 확인 엔드포인트 1초 폴링 · 화면 10초 폴링 유지~~ → **예약 현황도 SSE(시술 현황 `/board/stream` 방식)** — 10초를 기다리지 않는다: 쓰기를 보내면 서버가 KOS 에 보낸 즉시 그 일정을 다시 읽어 확인(쓰기 큐 확인 · 시술 현황 방 배정 연쇄처럼)하고, 확인 · 실패 · 판 바뀜을 SSE 로 바로 밀어 줌 → 그 화면 · 다른 직원 화면 모두 바로 갱신 · 실패 = 공용 토스트 + 「다시 시도」 · 누른 버튼은 결과 전까지 잠금. 예약 현황 10초 조각 폴링(R41) → SSE 로 바꿈 | 사용자 「예약 현황도 SSE 로 해 · 10초마다 기다리라고?」(11-24) |
| 2026-11-24 | **실물 확인 4 결과**: 상담사 지정 = `create-consultation` → 단계 그대로(`CONSULTATION_WAITING`) · 상세 `consultations[]` · `consultation.counselor` 에 바로 보임 · **바꾸기 = `consultation/v1/commands/change-consultation-counselors {consultationId, counselorIds}`**(기록 하나 유지 · 새로 만들면 기록이 둘 됨 → 바꿀 땐 꼭 change). 시술만 진행 연쇄(방 배정 작업 · 방 · 시술권 작업 · 시술 작업에 같은 방 → READY · 오더 메모 · `PROCEDURE_WAITING`) 전부 O | `be-probe-4-report.md` |
| 2026-11-24 | 접수 뒤(`IN_PROGRESS`) 지정 의사 바꾸기 = **O**(`update-reservation occupiedResources items` · 다른 칸 그대로) → 의사 지정 고치기 = 시안대로 오늘 예약 · 접수 · 검수 W3 닫힘 | be-probe-4 「접수 뒤 의사 지정」 |
| 2026-11-24 | KOS 통신 폴링 + 이벤트(쓰기 즉시 다시 읽기 확인 일반화 · D53) = **다음 스펙**. 이번 판 쓰기 확인 = 지금 쓰기 큐 방식 · 화면 = SSE(D52) | 사용자 「이거는 다음 스펙에서 할 거고」 |
| 2026-11-24 | 코드 먼저 시작 — **실물로 굳은 바닥(KOS 쓰기 계획 · 허용 목록 · 할인 전 가격 · 권한 키)을 SPEC 검수와 나란히** · 화면 · 흐름 · SSE 는 SPEC 2차 검수 뒤 WORK 로 | 사용자 「코드 언제 작업할 거야」 |
| 2026-11-24 | **순서대로**: 스펙 검수 통과 → WORK → 구현. 스펙 검수 중 나란히 띄운 backend 기반 1 · frontend 기능 1 은 멈춤(코디 오독 — 재촉 ≠ 순서 건너뛰기) | 사용자 「스펙 쓰고 순서대로 해야 할 거 아니야」 |
| 2026-11-24 | **구현은 단계 순서로 판을 나눈다**(한 번에 다 하지 않음): 1판 예약(등록 창 · 상세 틀 · 예약 버튼 · 우클릭 · SSE) → 2판 접수 → 상담 → 3판 시술(시술만 진행 · 시술 목록 · 수납) → 4판 귀가 대기 → 귀가. 판마다 구현 → e2e → 사용자 화면 확인 → 다음 판 | 사용자 「왜 한 번에 다 끝내려고 해 · 어차피 한 번에 못 끝내는 스펙」 |
| 2026-11-24 | **D53(쓰기 즉시 확인 · KOS 다시 읽기) = 이번 판** — 다음 스펙으로 미룬 건 코디 오독. 즉시 확인 없으면 SSE 가 10초를 기다림 | 사용자 「SSE 를 안 하겠다고? 이게 말이냐」 |
| 2026-11-24 | 시안 = 생김새 · 문구 정본 · 동작은 결정 > 시안 > cc(앞 작업 규칙 이어받음) | `reservation-board-decisions.md` |

뒤집힌 결정은 지우지 않는다. ~~취소선~~ 을 긋고 같은 행에 뒤집은 날짜와 사유를 남긴다 —
지우면 왜 그렇게 갔는지가 사라져서 같은 논의를 다시 한다.

## 3. 발주 (살아 있는 것만)

| 워커 | handle | task_id | dispatch_id | 브리프 | 상태 |
|---|---|---|---|---|---|
| planner | `term_37ac7485-be74-4e85-aaf6-c43c0ffd8f03` | `task_3db54e5d848d` | `ctx_2ff64fc9bb77` | `planner-fix-1-instructions.md` | 고침 1 완료 · retain (남은 OQ = D07 · D22 ~ D25 · 첫 판 `task_a28b758bbb72` — SPEC-007 draft(686줄 · OQ-D01 ~ D21) · 006 ⑫ · 002 ㉘ · 000 ② · lint 0 · 미커밋 |
| reviewer_doc | `term_bcd28eb4-3117-4aa1-ba3d-68c3f3073547` | `task_50bbe6f30442` | `ctx_bada948d34d6` | `review-doc-2-instructions.md` | 2차 진행 (1차 FAIL 3 · WARN 12 — `review-doc-1-report.md`) |
| backend · 1판 | `term_4c5128f0-981e-4cc0-bdcb-5392c9635a20` | `task_18918d64a9ce` | `ctx_1bbb70d61eb7` | `be-p1-instructions.md` → `be-p1-fix-1` | 1판 완료(990 passed) → 고침 1(다른 날짜 최신화 = 예약 스트림에만 reservation 신호) 진행 |
| frontend · 1판 | `term_a0519d50-d55f-45ae-b9cd-0e5d8682ac98` | `task_5b68f1a75567` | `ctx_f04351ae5243` | `fe-p1-instructions.md` → `fe-p1-fix-1` | 고침 1(book_view group_text) 진행 · 1판 완료 — `fe-p1-report.md`(pytest 529 · node 125) · backend 에 detail_editable · web_errors 요청 |
| (멈춤 · 옛) frontend | `term_9e29e1a2-3f76-45d9-9965-54b71d752552` | `task_9ac7d95a6953` | `ctx_e894a9cad6d2` | `fe-feat-1-instructions.md` | 기능 1 진행 — 등록 창 · 상세 모달 · 우클릭 · 시술 목록 · SSE 화면 |
| backend(코드) | `term_e985290c-4bd8-496a-9f3e-ed9ce7c108d2` | `task_d66b0bfe1eda` | `ctx_95e3bb6f6594` | `be-found-1-instructions.md` | 기반 1 진행 → 끝나면 기능 1(`be-feat-1-instructions.md` · task `task_d94e805eaa92` 만들어 둠 — dispatch 대기: 터미널에 기반 1 dispatch 살아 있음) |
| backend(실물 확인) | `term_ed3a1728-5b0e-455f-b9f2-fb76c72fd39c` | `task_138d69a7ac49` | (dispatch) | `be-probe-4-instructions.md` | 4차 진행 — 상담사 지정 create-consultation · 시술만 진행 관리실 연쇄 (1 ~ 3 완료) |
| researcher | `term_ab4b9a17-9d28-489c-a70c-908b47c4cf7b` | `task_cb3bef1723b9` | `ctx_a26d34ba9791` | `day-reservation2-research-brief.md` | 완료 · retain |

핸들은 세션 재연결로 바뀐다. 바뀌면 **덮어쓴다.** 워커 보고는 dispatch preamble 의 값을 따르므로
여기 옛 핸들을 남겨 두면 어느 것이 산 것인지 판단이 안 된다.

## 4. 산출물

- spec PR: https://github.com/MediSolveAIDev/mediness/pull/961 (draft · `479d8f46` · 머지 전 — 구현 끝난 뒤)
- Delivery: CENTURION_DAY#275(1판 · plan-approved) · #276 ~ #278(2 ~ 4판 · 승인 대기)
- code PR: <링크>
- 리포트: `<review-*-report.md>` · `<research-*.md>`
- 커밋: `<sha>` — <한 줄>

## 5. 이력 (최신이 위)

- `2026-11-24` 사용자 #275 승인 → receipt 적용 · 1판 be · fe 발주
- `2026-11-24` Delivery 4판 #275 ~ #278 발행
- `2026-11-24` 3차 PASS · spec 커밋 · PR #961 · planner Delivery 1 발주
- `2026-11-24` 2차 WARN 8 → planner 고침 2 발주(구현은 멈춘 채)
- `2026-11-24` planner 고침 1 완료 · reviewer_doc 2차 발주
- `2026-11-24` backend 기반 1 발주(code 워크트리 · dev `4bf0b4a1` = 최신)
- `2026-11-24` 실물 확인 4 완료 · 결정 D49 ~ D52 · planner 고침 1 발주
- `2026-11-24` reviewer_doc 1차 FAIL 3 · WARN 12
- `2026-11-24` planner SPEC 완료 · reviewer_doc 1차 발주
- `2026-11-24` 결정 파일(D1 ~ D48) · spec 워크트리 · planner 발주
- `2026-11-24` 실물 확인 3 완료
- `2026-11-24` 실물 확인 3 발주
- `2026-11-24` 실물 확인 2 완료(시험 예약 A · B 귀가 완료로 정리)
- `2026-11-24` 실물 확인 2 발주(같은 터미널)
- `2026-11-24` 실물 확인 1 완료(예약 단계 쓰기 전부 O)
- `2026-11-24` backend 실물 확인 1 발주(code 워크트리 생성)
- `2026-11-24` Run 생성 · researcher 발주
- `2026-11-24` slug 세움(`new-work.sh day day-reservation2 --workers researcher`) · 조사 브리프 작성

이 절은 **재개에 필요한 만큼만** 쓴다. 회고·배운 것은 `SUMMARY.md` 몫이다.
