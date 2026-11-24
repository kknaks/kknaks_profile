# delivery-1 결과 보고 — SPEC-007 · 006 ⑫ · 002 ㉘ · 000 ② → Delivery 4판

## 상태: done (Issue 4개 발행 · 승인 대기 — 승인 receipt 는 만들지 않음 · 사용자 몫)

## Delivery Issue (MediSolveAIDev/CENTURION_DAY)

| request | Issue | status | baseline | next_action | plan_digest |
|---|---|---|---|---|---|
| p1-reservation | #275 | created | pending | review-delivery-plan | `sha256:0ca43d0eb9abbd5c65655b42c1c526e0c86d29bd7377003a40b2c61007161a0f` |
| p2-reception | #276 | created | pending | review-delivery-plan | `sha256:0e02fa5909575758a11dc5ce5ff5e0ca479077eba3cd03913ef5fd823c235b02` |
| p3-procedure | #277 | created | pending | review-delivery-plan | `sha256:389096ab4806b0463b980c16ac34912f2824d92c0dac2d05d1463997a3e717e9` |
| p4-discharge | #278 | created | pending | review-delivery-plan | `sha256:62ed31950a3fcd0329d2af88c79d218343edb02e9245c456cef55531277cf3f9` |

- 위험 = 넷 다 **L3**(KOS 외부 쓰기를 새로 엶 · 1 ~ 3판은 migration) → 첫 apply = `delivery-plan:review`. 승인 receipt(`{"decision":"approved","reviewer_type":"human","reviewer":"<사람>","plan_digest":"<위 값>"}`)는 사용자 몫 — 적용 안 함
- baseline = Mediness `origin/main` **`c43633be698e1ebbc06ac9617a16262dacd1fac7`** + `spec-baseline:pending`. SPEC 원천 = PR #961(브랜치 `kknaksss/day-reservation2-spec` · `479d8f46` + 이번 커밋 `54bbeb14`). harness 규칙상 `spec_baseline_revision` = fetch 한 origin/main 이어야 해서(requests.md 첫 줄) 브리프의 「baseline = 479d8f46」은 review_surface 에 SPEC 원천으로 적었다. PR #961 머지 뒤 같은 idempotency key · contract_version 2 · 새 main SHA 로 재결속(결과 계약 같으면 재승인 없음)
- 파일: `delivery/request-*.json` · `plan-*.json` · `apply-*.json` · `*.err` · 생성 스크립트 `delivery/gen/make4.py`(처음 만든 3개 나누기 `gen/make.py` 는 코디 변경으로 버림 — apply 전)

## WP(= Delivery) 나누기 — 판 순서 (코디 변경 반영)

판마다 구현 → 로컬 KOS 데모 지점 e2e → 사용자 화면 확인 → 다음 판. 한 Delivery = 한 Code PR(백엔드 + 화면 함께 — 안에서 병렬). 의존 = 앞 판 머지 + 사용자 화면 확인.

| 판 | Issue | 범위 | KOS 쓰기 새로 엶 | migration | 완료 조건(e2e) | 되돌리기 |
|---|---|---|---|---|---|---|
| 1 예약 | #275 | 예약 등록 창(새 고객 W1 → W2 → W3 · duplicate_token · get-visitor) · 예약 상세 모달 틀(머리 · 고객 · 예약 정보 · 이전 방문 · 의사 지정 · 오른쪽 칸은 3판) · [예약 취소] · [예약 변경] 창 · 우클릭 옮기기 / 취소 / 동행 추가 · 동행 저장 · **끌어 묶기 제거** · **예약 현황 SSE**(폴링 제거) · **쓰기 바닥 + D53 즉시 확인** · 권한 `reservation.detail` | reserve · update-reservation · create-visitor · 공개 cancel-reservation | 0025_detail_permission(**미커밋 일부 있음**) | 새 고객 · 같은 고객 창 · 기존 고객 예약 · 의사 지정 · 변경 창 · 옮기기 · 취소 · 동행 저장 / 풀기 · 두 화면 SSE | revert + 0025 down |
| 2 접수 → 상담 | #276 | [접수] · 신분증 확인 · 의사 지정(접수) · 상담사(상담 기록 W7a / b) · 관리실 · [상담 대기] 묶음 · 상담 대기에서 바로 바꾸기 · 상담 중 귀가(W12) · 귀가 사유 · 귀가 완료 | recept · CONSULTATION_WAITING · COMPLETED · create-consultation · change-consultation-counselors | `visit.discharge_reason`(새) | 신분증 → 접수 → [상담 대기] → 바꾸기 → 귀가(사유) · 상담 진행에서 귀가 | revert + down |
| 3 시술 | #277 | 시술만 진행 · 「오늘」 ✓ · [시술 대기] 묶음(W8 → W9 → W13 · 규칙 28 넓힘) · 오더 메모 · 시술 목록(D44) · 수납 정보 · 할인 전 가격 · 수납 버튼 · 수납 딥링크 · 시술 중 귀가(W14) | add-flow-tasks PROCEDURE + ticketId · change-order-memo | 0024_purchase_base_price(**미커밋 일부 있음**) + 백필 | 시술만 진행 → [시술 대기] → 목록 n/m · 상태 → 수납 중 / 완료 · 딥링크 · 시술 중 귀가 | revert + 0024 down |
| 4 귀가 | #278 | 귀가 대기 [귀가 처리](RP-02 / 03 · W15 한 건) · [처방전 출력] 딥링크 · 귀가 완료 | (COMPLETED 판정만) | 없음 | 귀가 대기 → 처방전 → 미수 경고 / 단순 → 귀가 완료 | revert |

## BE ↔ FE 계약 (각 Issue Target Delta 에 같은 문장 · SPEC-007 §3 인용 · 이름 제안)

- **계약 W(쓰기 바닥)** — 화면 서비스는 `WriteIntent` 로 쓰기 큐에 넣기만 · 경로 · 본문 · expect = `KosWritePlanner` · `write_open` = 경로 + 값만 · 순서 / 단계 조건 = 계획 / 쓰기 큐(SPEC-002 ㉘ 「판정 자리」) · **D53**: 보낸 즉시 `get-schedule-detail` 1초 간격 다시 읽어 expect 확인 · 짧은 상한 넘으면 다음 회차 · 결과 → DAY 사본 → SSE
- **계약 S(SSE)** — `GET /reservations/stream` · `reservation`(version → #reservation-main 다시 받기) · `write_confirmed`({visitId, action} → 모달 다시 받기 · 버튼 잠금 풂 · 성공 알림) · `kos_failed`(공용 토스트 HTML + 「다시 시도」) · `session_expired` · retry 3000 · 15초 ping · 10초 폴링 제거
- **계약 V(화면 값)** — 경로 = SPEC-007 §3 「API 계약」 표 그대로(GET /reservations/visits/{id} · /book · /edit · /customers · POST /reservations · PUT …/schedule · POST …/cancel · …/reception · PUT …/identity · …/doctor · POST …/consultation-waiting · PUT …/counselor · …/room · POST …/procedure-waiting · PUT …/order-memo · POST …/discharge · PUT /reservations/companions/group · POST …/retry). 모달 값 = stage · date_kind · editable 플래그(경계 표 판정 = 서버) · customer · reservation · previous_visits · (2판) identity · consult · discharge_reason · (3판) order_memo · treatments[] · payment — 문구 · 색은 화면이 시안대로 키로 그림

## 같은 커밋(`54bbeb14`)으로 PR #961 에 얹은 것

- `30-work.md` Spec Coverage: SPEC-007 = #275 ~ #278(proposed) · 006 ⑫ · 002 ㉘ · 000 ② 행에 Delivery 표시
- `log.md` 한 줄
- **SPEC 고침 3(코디 정정 · D53 = 이번 판)**: SPEC-007 머리 고침 3 노트 · §1 범위 표 · §3 「KOS 쓰기」 머리 확인 방식 · 「실시간 갱신」 쓰기 확인 줄 · Rule 1 · W13 · OQ-D01 · D 반영 표 / SPEC-002 ㉘ 「확인 방식」 · 이벤트 연쇄 줄 / SPEC-006 ⑫ ⑦ · 실시간 갱신 ② / 20-spec.md · 10-decision.md — 「D53 = 다음 스펙」 문장을 취소선 + 이번 판으로
- lint `--strict` = 0 error · products/day WARN 0

## 막힌 것 · 주의

- 막힌 것 없음. 처음 3개 나누기(BE 바닥 · BE 흐름 · FE)는 코디 변경(판 순서)을 받아 **apply 전에** 버렸다 — GitHub 에 남은 것 없음
- 코드 워크트리 미커밋 변경은 backend 만(0024 · 0025 · purchase 모델 · 매퍼 · snapshot · alembic test). 브리프의 「frontend 화면 일부」는 없었다
- 넷 다 L3 — 사용자가 L2 로 내리고 싶으면 request `risk_level` 만 바꿔 같은 key · version 2 · scope_delta 로 재실행
- 4판은 KOS 쓰기를 새로 열지 않지만 COMPLETED 한 건 판정(외부 쓰기)이라 L3 로 둠
