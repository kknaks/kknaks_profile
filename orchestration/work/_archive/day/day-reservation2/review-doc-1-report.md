# 리뷰 리포트 — day-reservation2 / doc 1차 (2026-11-24)

- 대상: 워크트리 `mediness-mediness/day-reservation2-spec` 미커밋 변경 — `spec-007-reservation-detail.md`(새 · draft · 686줄) · SPEC-006 개정 ⑫ · SPEC-002 개정 ㉘ · SPEC-000 2026-11-24 개정 ② · `20-spec.md` · `30-work.md` · `10-decision.md` · `log.md`
- 대조: 결정 D1 ~ D48(`reservation-detail-decisions.md`) · 앞 결정 R1 ~ R75 · 시안 v9(base64 뺀 사본으로 grep) · be-probe-1 · 2 · 3 · HAR `시술권사용.har` · `할인.har`(본문 키 모양) · CENTURION_DAY `origin/dev` = `4bf0b4a1`
- read-only. 리포 파일 수정 · stash · 커밋 없음(검수 뒤 `git status` = 검수 전과 같음)
- lint: `python3 scripts/lint-pipeline.py --strict` → **0 error · 263 warning · exit 0** · **products/day 범위 0 error · 0 warning**(warning 263 건은 전부 다른 제품 — 무관)

## 판정: **FAIL** (FAIL 3 · WARN 12)

| # | 등급 | 파일:줄 | 무엇이 | 근거 | 고칠 방향 |
|---|---|---|---|---|---|
| F1 | FAIL | `spec-006-reservation-board.md:97` · `:116` · `:141` · `:196` · `:292` · `:295` · `:335` · `:570` ~ `:572` · `:698` · `:725` | 개정 ⑫ 가 「끌어 놓아 묶기 · 띠 밖 풀기 없앰」(:289)·「카드 클릭 = 상세」(:50)를 적었지만 **취소선 없이 살아 있는 옛 문장이 남음**: :97 개요 「끌어 겹쳐 한 묶음」 · :116 범위표 「끌어 겹쳐 묶기 · 띠 밖에 놓아 풀기」 · :141 RV-46 카드 끌기(묶기 · 풀기) = **「넣음」** · :196 「마우스 모양 · 포커스도 누르는 것처럼 보이지 않게」(카드는 이제 누름) · :292 **「카드에 다른 누르는 동작은 없다(R2 그대로 — 끌기만)」** · :295 끌기 켜짐 조건(끈 카드 · 놓은 카드) · :335 S-8 끝 **「잘못 묶었으면 카드를 띠 밖 빈 곳에 놓아 뺀다」** · :570 ~ :572 케이스 매트릭스 끌어 놓기 3행(200 묶임 · 옮김 · 409) · :698 · :725 「표에서 끌어 묶는」 | D2(R2 뒤집음) · D45(「카드 위 끌어 놓기 묶기(R66 입구) 없앰 — 끌기는 옮기기 모드에서만」) | 각 줄에 취소선 + 「→ 개정 ⑫」 또는 삭제. :292 · :196 은 「누르면 예약 상세 · 우클릭 메뉴」로, RV-46 은 「뺌(D45)」, 케이스 3행은 DAY-SPEC-007 「동행 저장」 케이스로 넘긴다고 표시 |
| F2 | FAIL | `spec-007-reservation-detail.md:633` | **OQ-D21**(접수 뒤 단계에서 「오늘」 ✓ 를 다시 켜고 끌지)은 이미 결정됨 | D40 「접수 단계만 누를 수 있음 · … **그 뒤 단계는 읽기 전용 ✓**」 · D41 「끄면 『오늘』 읽기 전용」 | OQ-D21 삭제 · U-7 :242 「그 뒤 단계는 읽기 전용 ✓(D40)」 그대로 두면 됨 |
| F3 | FAIL | `spec-007-reservation-detail.md:490` · `:496` · `spec-002-procedure-board.md:1024` | **`COMPLETED` 단독 금지 계약이 문서 안에서 어긋남**: :496 「`COMPLETED` 는 순서 묶음으로만 — 단독으로 보내지 않는다(**W12 · W14 · W15** …)」인데 W15(귀가 대기) 는 `change-flow-step COMPLETED` **한 건만** 보낸다. SPEC-002 :1024 는 「순서 묶음 안에서만 · **또는** `PROCEDURE_DONE` ∧ 열린 작업 없음 · 단독으로 열지 않음」— 지금 `write_open(api, path, body)`(`writes.py:72`)는 본문만 보므로 「앞 쓰기 확인 뒤」 · 「방문 단계 · 열린 작업 없음」을 판정할 수 없다 → 워커가 게이트 방식을 추측으로 정해야 함 | D26 · D39 · D47 · be-probe-3 §「공통 — 안 끝난 작업이 남은 상태에서 단독으로 보내지 않게, 순서를 outbox 에서 묶어야 함」 · `writes.py:72 ~ 83` | 「순서 묶음만」을 W12 · W14 로 한정하고 W15 는 「귀가 대기 ∧ 열린 작업 없음(DAY 사본 기준 · 계획 단계에서 확인)」으로 따로 적는다. 판정 자리(= `write_open` 은 경로 + 값만 · 순서 · 단계 조건은 계획(planner) / outbox 쪽)를 SPEC-002 ㉘ 에 한 줄로 못 박는다 |
| W1 | WARN | `spec-007-reservation-detail.md:48` · `:476` · `spec-006-reservation-board.md` Rule 7 | W1 같은 고객 찾기를 **화면 요청 안에서 KOS 를 바로 부름** = R39(「화면 요청은 KOS 를 부르지 않는다」) 예외. 결정 D 에 이 예외 문장은 없다(R59 공지 저장은 결정으로 연 예외) | R39 · R59 · D9(멈추고 그 고객 제시 — 동기 판정이 사실상 필요) | 코디가 「R39 예외 = W1(읽기 · 저장 요청 안)」을 결정 행으로 확인 · SPEC-006 Rule 7 예외 목록에 W1 추가 |
| W2 | WARN | `spec-007-reservation-detail.md:439` · `:447` | RB-11 [이 고객으로 예약] 요청이 form `kos_visitor_id` 로 **KOS id 를 브라우저에 왕복** — 같은 절 :439 「응답에 KOS id 를 싣지 않는다 · 예외 = 딥링크」와 어긋남. 또 같은 고객이 DAY `customer` 사본에 아직 없을 때(다른 지점 · 동기화 전) DAY 사본을 언제 만드는지 비어 있음 | D9 ①(「같은 고객 있으면 멈추고 그 고객 제시」) · :439 | 예외에 RB-11 을 더하거나 서버 쪽 임시 토큰(이름 제안)으로 바꿈 · 「DAY 사본 없음 → W3 전에 사본(get-visitor)」 한 줄 또는 OQ |
| W3 | WARN | `spec-007-reservation-detail.md:491` · `:198` · `:315` · `:317` | W16 의사 지정을 「오늘 예약 · **접수**」에서 바로 KOS 로 보낸다고 적고 근거를 be-probe-1 §5-3 으로 듦 — 실물 5-3 은 **`RESERVED`(앞날 예약)** 에서만 확인. 접수 뒤(`reservation.status IN_PROGRESS`)의 `update-reservation occupiedResources` 는 실물 확인 없음 | be-probe-1 §5(앞날 11-27 예약) · be-probe-2 #6(접수 뒤엔 `counselor` 만 확인) · 머리 :28 「실물에서 보지 않은 칸은 『확인 안 됨』 · §5 OQ」 | W16 에 「접수 뒤 = 실물 확인 안 됨」 표시 + OQ 하나(또는 실물 확인 4 에 넣음) |
| W4 | WARN | `spec-007-reservation-detail.md:488` | W13 ① 본문의 값 원천 = 「시술권 묶음 사본(옵션 · 세트 · 시술 항목 스냅샷)」이라 했지만 DAY 사본에 HAR 키 전부가 있지 않다 — `medicines[{id,name}]` · `procedure.createDate` · `productOptionConfiguration.optionId`(ticket_bundle 에 옵션 FK 없음 → `purchase_item.product_option_id` 조인) 매핑이 비어 워커가 추측해야 함. ② 「글이 비면 보내지 않음」은 결정 · 실물 근거 없음 | HAR `시술권사용.har` #15 · #28 본문 모양(본 리뷰가 키만 뽑아 확인 — be-probe-3 ⓐ 와 같음) · `models/ticket.py:30 ~ 66` · `models/_snapshot.py:45 ~ 67`(medicines 없음 · `TreatmentItemMedicine` 은 현행 마스터) · be-probe-3 ⓐ 「값은 `get-ticket-bundles` 묶음에서」 | 키별 원천 표(DAY 칸 / 현행 마스터 조인 / 보낼 때 KOS `get-ticket-bundles` 읽기) 또는 OQ · 「빈 글 안 보냄」은 OQ 로 |
| W5 | WARN | `spec-007-reservation-detail.md:213` · `:567` | 관리실 「**꺼짐 없음**」(꽉 찬 방도 고를 수 있음)은 결정에 없음 — D19 는 「비어 있는 방부터 · 정원 숫자는 안 보임」만. 시안은 꽉 찬 방을 끔 | D19 · 시안 `combo` · :567 표 자체 「관리실 n (k/2) · 꽉 찬 방 꺼짐」 | 「꺼짐 여부」를 OQ 로 두거나 코디 기본값으로 결정 행에 올림 |
| W6 | WARN | `spec-007-reservation-detail.md:303` | 우클릭 켜짐 조건을 시안보다 넓혀 적음 — 「동행 추가」 에 **노쇼 아님** · 모든 줄에 **권한 꺼짐** 추가. D45 는 「켜짐 조건 = 시안(L2898)」(시안 `alive = st !== '취소' && day >= 0`) | D45 · 시안 L2897 | 권한 꺼짐은 D46 근거로 남기되 「노쇼 아님」은 R66 · R67 근거임을 「시안과 다른 곳」 표에 한 줄로(지금 :562 ~ :585 표에 없음) |
| W7 | WARN | `spec-007-reservation-detail.md:190` | [여권 스캔] · [문진 QR] 보이는 조건을 planner 가 바꿈 — 시안 [여권 스캔] = 외국인 ∧ ¬`kept`(1년 안 재진) ∧ `s.id === 'idle'` · [문진 QR] = `d.health === 'none'` 일 때만. SPEC = 「원천이 없어 빼고 늘 보임」. D13 은 「자리만 · 비활성」 · D20 은 값 비움만 정함 | 시안 L2146 · L2148 · D13 · D20 | 「시안과 다른 곳」 표에 행 추가 + 근거를 「원천 없음 — planner 기본(OQ)」으로 표시 |
| W8 | WARN | `spec-007-reservation-detail.md:277` ~ `:281` | 수납 버튼 표가 **미수 0 ∧ 결제총액 0**(구매 없음 · 상담 전 시술 단계)을 다루지 않음 — 워커가 「버튼 없음」을 추측 | D36(세 경우만 정함) · 시안 `need ? … : ''`(필요 없으면 버튼 없음) | 넷째 줄 「그 밖 = 버튼 없음(시안)」 추가 |
| W9 | WARN | `spec-007-reservation-detail.md:628` · `:284` | **OQ-D16** 의 「`KOS_WEB_BASE` 설정 이름 · 값이 없을 때」는 코드에 답이 있음 — DAY 에 이미 `kos_web_base`(env `KOS_WEB_BASE`)가 있고 `require()` 가 비면 KOS 호출 자체를 막음(필수). 남는 것은 「고객 · 일정 KOS id(`external_ref`)가 없을 때」뿐 | `emr/kos/client.py:84` · `:106 ~ 113` | :284 「이름 제안 · cc `kos_web_base`」 → 「DAY `KosEndpoints.kos_web_base`(있음)」 · OQ-D16 은 KOS id 없음만 |
| W10 | WARN | `spec-007-reservation-detail.md:631` | OQ-D19 에 「다회권 가격 나누기」가 들어 있음 — 이 화면은 수납 항목을 넣지 않는다(D35 · 범위 밖) | D35 · be-probe-3 ⓐ-1(시험 준비용 수납에서 생긴 문제) | OQ-D19 에서 빼고 「목록 순서 · 여러 세트 묶음 `round.total`」만 |
| W11 | WARN | `spec-006-reservation-board.md:1`(status `stable`) · `30-work.md:49` | **stable SPEC-006 이 동작을 바꿈**(R2 · R66 입구) — 열린 Delivery #267 · #269(`spec-baseline:ready` · baseline = main `32b83390` · ③ 화면 = 「끌어 놓기」 포함)가 이 개정 전 계약으로 구현 중. 또 stable 문서(006 · 002 · 000)가 draft SPEC-007 에 기대는 계약을 담음 | `30-work.md:49` · `:83` ~ `:85` · `rules/delivery-workflow.md`(exact revision baseline) | 코디가 PR 전에 Delivery #269 와의 관계(이번 판에 끌어 놓기 묶기 제거를 같이 할지 · 새 Delivery)를 정하고 Spec Coverage 006 행에 표시 |
| W12 | WARN | `spec-007-reservation-detail.md:173` · `:550` · `:613` | OQ-D01(쓰기 큐 결과를 예약 화면에 알리는 길 · 새 예약 DAY 행이 KOS id 전 없음)은 **구현을 막는 빈칸**인데 기본안이 「정하지 않음」 — 등록 성공 알림 · 반짝임 · 실패 토스트 · 다시 시도 경로(`/retry` :459)가 모두 여기에 걸림 | D22(「시술 현황과 같은 토스트 · 다시 시도」) · R71(예약 현황 실패 알림 = oob 토스트) | 코디 기본값으로 닫을 후보 — 「쓰기 응답 = 큐에 넣음까지 · 결과는 10초 폴링 조각에 oob 토스트(R71 같은 길)」 등 하나를 결정 행으로 |

## 직원이 실물에서 만날 자리

- [상담 대기] 로 고른 상담사는 KOS `reservation.counselor` → DAY `visit.requested_counselor_id` 에 들어가는데, 예약 표 카드 「상담사」(R57)와 원내 현황(R48)은 `consultation.counselor_id` → `consultation_info_counselor_id` 를 읽는다 → **상담 대기 카드에 「상담사 미정」**(SPEC 은 OQ-D08 로 정확히 짚음 — 사용자 질문 필요)
- 외국인 고객은 이번 판에 [상담 대기]가 늘 회색(D21 · D23 — 사용자 몫으로 결정됨). 데스크 문의가 생길 자리
- 시술만 진행으로 보낸 시술 작업은 방이 없어 `NOT_STARTED` — 시술 현황에서 방을 지정해야 [호출] 가능(be-probe-3 ⓑ)
- 상담 단계 [귀가 처리] 는 「방 배정」 작업만 취소(D26). 그 사이 차티 · KOS 가 시술 작업을 붙였으면 `COMPLETED` 400 → 쓰기 큐 `failed`(W12 · 케이스 :525 에 있음)
- 할인 전 가격 백필 전 구매는 할인 0 으로 보임(OQ-D15 기본안)
- 시술 중 귀가 = 시술권 회차가 `AVAILABLE` 로 되돌아감(be-probe-3 ⓒ-4 · 미결 3 「제품 의도와 맞는지」) — n/m회가 귀가 뒤 줄어듦

## 참고(기존 부채 · 지적 아님)

- `30-work.md:50` 에 DAY-SPEC-007 Spec Coverage 행이 생김 — 브리프 「30-work 는 쓰지 않는다」와 다르지만 lint(SPEC 파일 ↔ Spec Coverage 동기 = ERROR) 때문에 필요한 한 줄. WORK 본문 · Delivery 는 없음
- `log.md:16` PR 칸 = 「(PR 전 · 코디가 PR)」 — 앞 행들과 같은 관례. PR 번호로 바꿀 것
- SPEC-000 `identity_check.status · method` 칸 꼴이 「enum」으로 적혀 있으나 코드는 `String`(OPEN_ENUM · `models/reception.py:59 ~ 60`) — 개정 전부터
- SPEC-000 :1628 `base_currency` 하나 — 기존 칸은 `currency · supplied_currency · tax_free_currency · vat_currency` 넷(`models/purchase.py:111 ~ 114`). 이름 제안이니 WORK 에서 맞추면 됨
- W3 · W5 지연 「≈3s」(취소)는 실물이 3초 뒤 한 번 읽은 값(실제 지연 아님) · W4 「≈2s」도 같음 — 확인 조건의 기다림 설계엔 문제없음

---

## D 대조 표 (D1 ~ D48)

| D | 최종 유효 결정(요지) | SPEC 반영 자리 | 판정 |
|---|---|---|---|
| D1 | 시안 = 생김새 · 문구 · 동작 = 결정 > 시안 > cc | 007 :27 · 「시안과 다른 곳」 | O (W6 · W7 은 표에 빠진 행) |
| D2 | 카드 클릭 = 예약 상세 · R2 뒤집음 | 007 :74 · 006 ⑫ :50 | O · **006 남은 옛 문장 F1** |
| D3 | 진행 순서 | (계약 아님) | O |
| D4 | 예약 등록 창(기존 · 새 고객) | 007 U-1 · 006 ⑫ ② | O |
| D5 | KOS 쓰기 = 내부 API 모듈 · ext 아님 | 007 :48 · :472 | O |
| D6 | 열 = 예약 그룹 · `reservationGroupId` | U-1 :168 · W3 | O |
| D7 | 초진 = KOS 판정 · 새 고객일 때만 배지 | U-1 :165 · U-3 :189 | O |
| D8 | 담당자 = 로그인 직원 KOS id · 바꾸기 없음 | U-1 :166 · W3 | O |
| D9 | 새 고객 = 같은 고객 찾기 → 만들기 → 사본 → reserve → 사본 · 예약만 다시 시도 | U-1 :172 · W1 ~ W3 · :495 · S-1 · S-2 · S-9 | O (W1 · W2 지적) |
| D10 | (뒤집힌 뒤) 지정 의사 칸 보임 · 고르면 실음 · 희망 시술 뺌 · 끝 = 시작 + 그룹 간격 · 자리 남은 첫 구역 | U-1 :170 · W3 · RB-08 | O — 취소선 쪽(`doctors: []` 고정)으로 적은 곳 없음 |
| D11 | 실물 확인 · 쓰기 큐 · 취소 = 공개 API | :472 · W5 · SPEC-002 :1030 | O |
| D12 | 접수 = 오늘 예약만 | U-9 · W6 · 경계 표 | O |
| D13 | [문진 QR] · [여권 스캔] 자리만 · 비활성 · 문구 없음 | U-3 :190 | 부분 — 보이는 조건 바꿈(W7) |
| D14 | 상담사 · 관리실 = 예약 · 접수 화면에 담음 → [상담 대기] 때 · 상담 대기 = 바로 KOS · 상담 진행부터 잠금 | U-5 :214 · W7 · W11 · 경계 표 | O |
| D15 | 상담사 목록만 · 배지 · 흐림 없음 | U-5 :212 · RD-07 | O |
| D16 | 실물 1 결과(의사 자리 · 연락처 꼴 · CANCELED · 지연 · 취소 = status) | W1 ~ W5 · W16 | O (W16 접수 뒤 = W3) |
| D17 | 지정 의사 읽는 자리 고침 · 의사 목록 = 태그 `doctor` · 면허로 안 거름 | U-4 :198 · Rule 9 · 10 · SPEC-000 :503 | O — 코드 확인: `mapper.py:385 ~ 387` 이 `reservationGroup.doctors` 를 읽고 `sync_schedules.py:609 ~ 623` 이 `visit_occupied_resource_doctor` 를 채움(주장 맞음) · `visit.requested_doctor_id` 는 `mapper.py:579` `reservation.doctor` |
| D18 | 상담사 = 태그 `counselor` · 활성 · 시스템 계정 뺌 | U-5 :212 · 읽는 칸 :424 | O (`JobRoleTag.COUNSELOR` · `staff.is_system_account` 있음) |
| D19 | 관리실 = 빈 방부터 · 정원 숫자 안 보임 | U-5 :213 | 부분 — 「꺼짐 없음」 추가(W5) |
| D20 | 줄은 두고 값 비움 · 내국인 신분증 체크는 동작 | U-3 · RD-03 | O |
| D21 | [상담 대기] 조건 = 신분확인 + 상담사 + 관리실 | U-9 :273 | O |
| D22 | [상담 대기] = 방 배정 작업 → 방 지정 → `CONSULTATION_WAITING` · 실패 = 다시 시도 · 되돌리기 없음 | W8 ~ W10 · :494 · :499 | O (알림 길 = W12) |
| D23 | 외국인 신분확인 = 사용자 몫 | U-9 :273 · 케이스 :524 | O |
| D24 | 신분증 = true/false · 체크해도 접수 안 됨 | U-3 :192 · Rule 4 | O |
| D25 | 실물 2 결과 | W6 ~ W12 · 상태 그림 | O |
| D26 | 상담 단계 귀가 = 「방 배정」 CANCEL → COMPLETED · 사유 DAY 저장 · 접수 뒤 취소 숨김 | W12 · Rule 5 · RD-10 · SPEC-000 :516 | O |
| D27 | (D44 로 대체) | U-7 | O |
| D28 | 줄 · 오늘 ✓ · 상태 · 할인 줄 뺌 | U-7 | O |
| D29 | 연결 키 `visit_task.ticket_id → ticket → ticket_set → ticket_bundle.purchase_item_id` | U-7 :241 | O (`task.py:123` · `ticket.py:40 · 58 · 75` 확인) |
| D30 | 상태 4 문구 | U-7 :243 | O |
| D31 | 수납 정보 = 원내 현황 금액(`reservation_amounts.py`) | U-8 | O (`visit_amounts` · `:69 ~ 95` 확인) |
| D32 | 취소된 작업 = 미진행 · ✓ 빠짐 | U-7 :241 · :243 | O |
| D33 | 할인 원천 · `price_amount` = `priceV2`(할인 뒤) | U-8 · SPEC-000 :1626 | O (`mapper_purchase.py:125` `priceV2` 확인) |
| D34 | 할인 전 가격 저장 · 빈 동안 = SPEC 에서 | U-8 · SPEC-000 :1627 · OQ-D15 | O |
| D35 | [n원 수납] = KOS 웹 딥링크 `tab=purchase` | U-9 :284 | O (W9) |
| D36 | 수납 버튼 상태 셋 | U-9 :277 ~ :283 | 부분 — 넷째 경우 빈칸(W8) · enum `PurchaseStatus.INITIALIZED` · `PurchaseProcess.PENDING` 있음 |
| D37 | 시술 단계 귀가 = 확인 창 뒤 안 끝난 작업 CANCEL → COMPLETED · 문구 시안만 | U-10 · W14 | O (시안 `s5Pop` L2270 문구 일치) |
| D38 | (뒤집힌 뒤) [처방전 출력] = `tab=etceteraWork` 딥링크 | U-9 · :573 | O — 취소선 쪽(「못 함」) 없음 |
| D39 | 귀가 대기 귀가 = 확인 창 → COMPLETED | RP-02 · RP-03 · W15 | O (단독 금지 문장과 충돌 = F3) |
| D40 | 줄 = 지난 시술권 남은 것 + 이번 구매 · 접수 단계만 ✓ · 그 뒤 읽기 전용 | U-7 · U-5 | O · **OQ-D21 은 이미 답(F2)** |
| D41 | 「시술만 진행」 명시 · [시술 대기] 때 한 번에 | U-5 :210 · W13 | O |
| D42 | `{n/m회}` = (used + in_use) / (canceled 뺀 수) | U-7 :240 | O (`TicketStatus` 4값 확인) |
| D43 | 시술현황 차트 수정 = 범위 밖 | §1 범위 | O |
| D44 | 시술 목록 = 코디 와이어 정본 | U-7 :228 ~ :236 | O |
| D45 | 우클릭 = 시안 동작 · 동행 = 체크 목록 · 같은 열 · 같은 시작 시각 · 통째 저장 · 옮기면 빠짐 · 끌어 묶기 없앰 | U-4 · U-11 · 006 ⑫ ③ ④ | 부분 — 006 옛 문장(F1) · 켜짐 조건 넓힘(W6) |
| D46 | 권한 새 키 · 지난 날 보기만 · 노쇼 · 특이사항 · 이전 방문 · 준비중 · 메모 보기만 | 권한 :464 · U-2 · U-3 · U-6 · SPEC-002 :620 · SPEC-000 | O (마이그레이션 끝 `0023_companion_permission` 확인) |
| D47 | 실물 3 결과 · 새로 열 것 5 | W13 ~ W15 · SPEC-002 ㉘ | O |
| D48 | `round.total` = 장 수 · 첫 AVAILABLE · `current` = 쓰는 중/쓴 + 1 · 여러 개 한 요청 | W13 :488 | O |

반영 안 된 D 번호: 없음(D3 은 계약 아님).

## W 대조 표 (KOS 쓰기 W1 ~ W17)

| W | 경로 · api | 본문 키 | 값 조건 | 확인 조건 · 지연 | 순서 묶음 | 실물 근거와 맞나 |
|---|---|---|---|---|---|---|
| W1 | `visitor/v1/queries/find-duplicated-visitor` internal | `name · phone{countryCode, phoneNumber} · snsInfo{snsType, accountId} · birthDateUtc` = be-probe-1 §1 | KOS 꼴 | `data` 있음 / `{}` = §1 「없음 = data 키 없음」 | 새 고객 맨 앞 | **O** (요청 안 동기 호출 = W1 지적) |
| W2 | `v1/visitor/commands/create-visitor` internal | §2 키 9개 그대로 | `82` · 앞 0 없음 · `YYYY-MM-DD 00:00:00.000Z` · gender 3값 · ISO 2자 · 소문자 sns | `data.id` → `get-visitor` | W1 뒤 | **O** |
| W3 | `schedule/reservation/v2/commands/reserve` internal | §3 키 그대로(`doctors[{id,name}]` 포함) | 자원 1 · `RESERVATION_GROUP` · 최상위 `doctor` 안 실음(§4ⓐ) · `counselor` · `desiredDischargeDateTimeUtc` 안 넣음(§3) | `scheduleId` → 상세 · 담당자 · 유입 ≈1s(be-probe-2 #1 「약 1초」 · be-probe-1 「수 초」) | W2 뒤 | **O** · `funnelDetail` 빈 글은 시안에 유입 상세 칸 없음(L2502) — 근거 맞음 |
| W4 | `update-reservation` internal | §5 `{scheduleId, occupiedResources{items[…]}}` | items 통째 · 자원 id 그대로 | §5 2초 뒤 한 번에 맞음 | — | **O** |
| W5 | `schedule/open/v1/commands/cancel-reservation` **open** | `{scheduleId, reason}` | `CANCELED` enum · 접수 뒤 400 `status NotAvailable`(be-probe-2 #12) | `reservation.status = CANCELED` · `flowStep` 그대로(§6) | — | **O** |
| W6 | `schedule/v1/commands/recept` internal | `{scheduleId}` | 오늘 · RESERVED | `RECEPTION` ∧ `IN_PROGRESS` · ≤0.1s(be-probe-2 #2) | — | **O** (`ReservationStatus.RECEIVED` = KOS `IN_PROGRESS` 확인) |
| W7 | `update-reservation` internal | `{scheduleId, counselor{id,name}}` | 둘만 | `reservation.counselor.id` · 다른 칸 그대로 · ≈1s(#6 · ⓒ) | [상담 대기] 끝 | **O** |
| W8 | `add-flow-tasks` internal(「방 배정」 ETCETERA) | 기존 계약 | 이미 열림(`writes.py:96 ~ 104`) | ≈1s(#3) | [상담 대기] ① | **O** |
| W9 | `schedule/flow/v1/commands/change-tasks-room` | `{scheduleId, sequences, roomId}` | 이미 열림 | `NOT_STARTED → READY` · ≤0.1s(#4) | ② | **O** |
| W10 | `change-flow-step` internal `{id, step}` | | `CONSULTATION_WAITING` 새로(지금 `OPEN_STEPS` 에 없음 — `writes.py:58 ~ 65` 확인) | ≈1s(#5) | ③ | **O** |
| W11 | `change-tasks-room` | 「방 배정」 seq | 이미 열림 | `READY` 유지 · ≈1s(#7) | — | **O** |
| W12 | `cancel-flow-tasks` → `change-flow-step` | `{scheduleId, sequences, reason}` → `{id, step}` | `CANCEL`(D26) → `COMPLETED` | `canceled` → `completed` ∧ status `COMPLETED`(정리 A) | 작업 취소 → 귀가 | **O** (계약 문장 F3) |
| W13 | `add-flow-tasks` → `change-order-memo` → `change-flow-step` | HAR #15 · #28 키와 **한 글자씩 같음**(`translsMap` 철자 포함) | PROCEDURE + `ticketId` · 여러 개(D48) · 방 배정 없이(ⓑ) | ① ≈1.1s · 시술권 `IN_USE` ② 즉시 ③ ≈1s | 시술권 작업 → 메모 → 시술 대기 | 키는 **O** · 값 원천 빈칸 · 「빈 글 안 보냄」 근거 없음(W4) |
| W14 | `cancel-flow-tasks` → `COMPLETED` | W12 와 같음 | 안 끝난 작업 전부 CANCEL | 시술권 되돌아감(ⓒ-4) | 작업 취소 → 귀가 | **O** |
| W15 | `change-flow-step COMPLETED` | `{id, step}` | `PROCEDURE_DONE` ∧ 열린 작업 없음(be-probe-3 #9) | `completed` | **한 건** | 실물 O · **「단독 금지」 문장과 어긋남(F3)** |
| W16 | `update-reservation`(items · doctors) | W4 와 같음 | W4 | ≈2s | — | 앞날 `RESERVED` 만 실물 O · **접수 뒤 확인 없음(W3)** |
| W17 | `change-order-memo` | `{scheduleId, orderMemo}` | 글 전체 | 즉시(be-probe-3 #3) | — | **O** |

- 실물에 없는 칸 · 값을 지어낸 곳: 없음(W13 ② 「빈 글이면 안 보냄」 한 줄은 정책 추가 — W4).
- SPEC-002 ㉘ 표(:1016 ~ :1035)는 SPEC-007 W 표와 경로 · 값이 같다. 「확인 조건 새 모양」을 이름 제안 · WORK 로 둔 것도 맞음.

## OQ 분류 표 (OQ-D01 ~ D21)

| OQ | 분류 | 이유 · 제안 |
|---|---|---|
| D01 쓰기 큐 결과 알림 길 · 새 예약 DAY 행 | **코디 기본** | R71(oob 토스트) · D22 를 이어 코디가 닫을 수 있음 — 구현을 막으므로 WORK 전에 닫을 것(W12) |
| D02 예약 변경 창에서 유입 · 메모 쓰기 | 코디 기본 | 실물 없음 → 「보기만」 기본안 유지 · 쓰고 싶으면 실물 확인 4 |
| D03 담은 값 · 열린 모달 다시 그리기 | 코디 기본 | 「닫으면 버림 · 쓰기 응답 때만」 그대로 |
| D04 접수 뒤 「시술 정보」 / 「상담 정보」 가르기 | **사용자 질문** | 시술만 여부가 저장되지 않음 — DAY 칸을 둘지 · 단계 이력으로 볼지 |
| D05 국적 빈 고객 · `is_new` null | 코디 기본 | SPEC-000 OQ-02-1 과 함께 |
| D06 「통역필요」 판정 | 코디 기본 | 안 보임 유지(`customer.language` 는 있으나 판정 규칙 없음) |
| D07 연락처 보이는 꼴 · SNS 종류 · 국가번호 목록 | 코디 기본 | 실물 `kakaotalk` 하나 — 나머지 값은 KOS openapi 로 확인 |
| D08 상담사 원천(R48 · R57 과 다름) | **사용자 질문** | R 결정을 다시 여는 일 — 「직원이 만날 자리」 첫 줄 |
| D09 시술만 진행의 관리실 · [시술 대기] 조건 | **사용자 질문** | D21 은 [상담 대기]만 · D41 · D47 이 관리실을 정하지 않음 |
| D10 시술메모 뺌 | 코디 기본 | 원천 없음 — 뺌 유지 |
| D11 안내 띠 뺌 | 코디 기본 | 판정 원천 없음 — 뺌 유지 |
| D12 이전 방문 취소 · 노쇼 포함 · 백필 | 코디 기본 | cc `previous_visits` 따르기 |
| D13 시술 목록 줄 순서 | 코디 기본 | 구매 시각 · 생성 순 같은 기본값 |
| D14 한 줄을 작업 여럿이 가리킴 · `ticket_id` 없는 작업 | 코디 기본 | DAY-SPEC-002 시술 줄 상태 규칙을 이어 정할 수 있음 |
| D15 할인 전 가격 빈 항목 | 코디 기본 | D34 가 「SPEC 에서」로 넘김 — planner 기본안(할인 0) 채택 가능 |
| D16 딥링크 설정 · KOS id 없음 | **이미 답 있음(절반)** | 설정 = DAY `kos_web_base`(필수 · `client.py:84`) — KOS id 없음만 코디 기본(꺼짐) (W9) |
| D17 새 오류 코드 토스트 글자 | 코디 기본 | R72 방식(빈 문구 = 공용) |
| D18 정원 찬 칸 · 지난 시각 · 30분 아닌 간격 · 구역 | 코디 기본 | 「KOS 결과대로」 · 끝 = 시작 + 그룹 간격(D10)은 이미 답 |
| D19 회차 목록 순서 · 여러 세트 `round.total` · 다회권 가격 나누기 | 코디 기본(앞 둘) · **범위 밖(가격 나누기)** | W10 |
| D20 `identity_check` 방문 칸 없음 · 값 이름 | 코디 기본 | 코드 확인 — `customer_id` 만 있고 `visit_id` 없음(`reception.py:58`) · `method` NOT NULL 이라 값 하나 정해야 함 |
| D21 접수 뒤 ✓ 다시 켜고 끄기 | **이미 답 있음** | D40 「그 뒤 단계는 읽기 전용 ✓」 (F2) |

사용자에게 물을 것 = OQ-D04 · D08 · D09(셋). 이미 답 있음 = D21(전부) · D16(절반). 나머지는 코디 기본값으로 닫을 수 있다.

## 범위 (브리프 §7 대조)

1차 범위 표(007 :54 ~ :62) Out Of Scope = 문진 · 여권 스캔 · 신분 확인 자동 접수 · 외국인 신분확인 · 상담사 순번 · 「상담중」 흐림 · 수납 항목 넣기 · 처방 만들기 · 예약 요청 · 고객 차트 · 「시술현황 차트 일부 기능 수정」 · 고객 등록 창 · 근무표 · 희망 시술/예산 · 예약메모 덧붙이기 — 브리프 §7 목록을 **모두 포함**, 더한 것은 전부 결정 · R 근거 있음. 기획안 · 다른 제품 폴더 수정 없음 · 사람 이름 · 전화 · id 원문 예시 없음(S-4 「아쿠아필링 10회권」은 코디 와이어 예시 문구). **O**
