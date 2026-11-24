# [planner · 고침 1] SPEC-007 · 006 ⑫ · 002 ㉘ · 000 ② — 1차 검수 FAIL 3 · WARN 12 + 새 결정 D49 ~ D52 + OQ 기본값

같은 터미널이면 앞 맥락 그대로. 새 터미널이면 먼저 `day-reservation2-spec-brief.md`(같은 폴더) 전부를 읽고 시작. 워크트리 `/Users/kknaks/orca/workspaces/mediness-mediness/day-reservation2-spec` · allowed_paths `products/day/` · 커밋 · push 금지 · 화면 문구 짓지 않기 그대로.

## 읽을 것

- 검수: `/Users/kknaks/orca/workspaces/kknaks_profile/day-reservation2/orchestration/work/day-reservation2/review-doc-1-report.md` — **F1 ~ F3 · W1 ~ W12 전부 고친다**(「고칠 방향」대로 · 아래 코디 답이 있으면 그것 우선)
- 결정 **D49 ~ D52 새로**: `/Users/kknaks/orca/workspaces/kknaks_profile/day-reservation2/reference/2026-11-24-reservation-detail/reservation-detail-decisions.md` 맨 아래
- 실물 확인 4: `…/day-reservation2/be-probe-4-report.md`(상담사 지정 · 바꾸기 · 시술만 진행 연쇄) · HAR `…/reference/2026-11-24-reservation-detail/상담사 지정.har`

## 새 결정 반영 (D49 ~ D52)

1. **D49 상담사** = 상담 기록(`create-consultation` / 이미 있으면 `change-consultation-counselors`). SPEC-007 W 표의 상담사 쓰기 행 · U · 케이스 · 읽는 칸을 바꾸고, `update-reservation {counselor}` 는 뺀다(SPEC-002 ㉘ `write_open` 표에서도). R48 · R57 원천 그대로라 표 카드 「상담사 미정」 문제 없음 → OQ-D08 닫음. 두 경로 모두 `write_open` 새 행
2. **D50 시술만 진행** = 방 배정 작업 → 방 → 시술권 작업들 → 시술 작업에 같은 방 → 오더 메모 → `PROCEDURE_WAITING` · 관리실 필수 · [시술 대기] 조건 = 신분확인 + ✓ 1개 이상 + 관리실 → OQ-D09 닫음 · be-probe-4 Q5 근거
3. **D51 할인 전 가격 빈 구매** = 상품 합계 · 할인 금액 칸 비움 → OQ-D15 닫음
4. **D52 예약 현황 갱신 = SSE**(시술 현황 `/board/stream` 방식) — SPEC-006 의 R41 「10초 조각 폴링」을 개정 ⑫ 에서 뒤집는다(취소선 + 근거). 쓰기 뒤 서버가 KOS 에 보낸 즉시 그 일정을 다시 읽어 확인(쓰기 큐 확인 — SPEC-002 방 배정 연쇄 방식 인용)하고 확인 · 실패 · 판 바뀜을 SSE 이벤트로 바로 보냄 · 누른 버튼은 결과 전까지 잠금 · 실패 = 공용 토스트 + 「다시 시도」 → OQ-D01 닫음 · W12 닫음. SSE 이벤트 이름 · 스트림 경로는 이름 제안(시술 현황 스트림을 본뜸 — `routers/board_streams.py` 인용)

## 검수 지적 — 코디 답 (「고칠 방향」과 다르거나 정해야 하는 것만)

- **F3**: `write_open` = 경로 + 값만. 순서 · 단계 조건(작업 취소 뒤 `COMPLETED` · 귀가 대기 ∧ 열린 작업 없음)은 **계획(planner 쪽 — `WritePlanner`) / 쓰기 큐 순서 묶음**에서 판정한다고 SPEC-002 ㉘ 에 한 줄로 못 박고, W15(귀가 대기 → `COMPLETED` 단독)는 「귀가 대기 ∧ DAY 사본 기준 열린 작업 없음」으로 따로
- **W1**: 같은 고객 찾기(W1)를 화면 요청 안에서 KOS 로 부르는 것 = **R39 예외로 연다**(코디 결정 · 읽기 · 새 고객 저장 요청 안에서만). SPEC-006 Rule 7 예외 목록에 추가
- **W2**: KOS id 를 브라우저로 왕복하지 않는다 — 서버가 같은 고객 찾기 결과를 짧게 들고 있는 토큰(이름 제안)으로. DAY 사본이 없으면 그 KOS 고객 상세(`get-visitor`)로 사본을 먼저 만든 뒤 예약
- **W3**: 접수 뒤(`IN_PROGRESS`) 지정 의사 바꾸기는 실물 확인 중 — 리포트(`be-probe-4-report.md` 「접수 뒤 의사 지정」 행)가 있으면 그대로, 없거나 X 면 **의사 지정 고치기 = 예약 상태만 · 접수부터 보기만**(시안 `recvArea` 와 다른 곳 표에 한 줄)
- **W4**: 시술권 작업 본문 = **보낼 때(쓰기 큐 계획 단계 · 서버 중앙) KOS `get-ticket-bundles {visitorId}` 를 읽어 그 묶음에서 키를 채운다**(be-probe-3 ⓐ 그대로 · DAY 사본으로 짓지 않음). 「빈 오더 메모 글은 보내지 않음」은 OQ 로
- **W5**: 관리실 꺼짐 = **없음**(정원 원천이 없다 · 꽉 찬 방 판정 불가) — 「시안과 다른 곳」 표에 근거와 함께
- **W6 · W7 · W8 · W9 · W10**: 「고칠 방향」대로
- **W11**: 앞 작업 Delivery(#267 ~ #269)는 마감 때 닫혔다 — 이번 판은 **새 Delivery**(SPEC-007 + 006 ⑫ · 002 ㉘ · 000 ②). Spec Coverage 006 행에 「⑫ 는 day-reservation2 새 Delivery」 표시
- **W12**: D52 로 닫음

## OQ 기본값 (코디 · 사용자 이의 없을 때) — OQ 에서 빼고 결정(코디 기본)으로 적어라

- OQ-D02 [예약 변경] 창의 유입 · 메모 = 보기만
- OQ-D03 모달에 담은 값 = 닫으면 버림 · 쓰기 결과(SSE) 때 다시 그림
- OQ-D04 접수 뒤 시술만 여부 = 그 방문 단계 이력에 상담 대기가 없으면 「시술 정보」
- OQ-D05 국적 빈 고객 = 내국인으로 보지 않음(신분 확인 칸 비움 · 배지 없음) · `is_new` null = 배지 없음
- OQ-D06 통역 = 안 보임 · OQ-D07 연락처 = KOS 꼴 그대로 보임 · SNS 종류 = 실물 `kakaotalk` 만 확정, 나머지는 OQ 유지
- OQ-D10 · D11 = 뺌(그대로)
- OQ-D12 이전 방문 = 취소 · 노쇼 뺌 · DAY DB 백필 범위
- OQ-D13 시술 목록 순서 = ① 지난 시술권(구매 시각 순) ② 이번 구매(구매 항목 순)
- OQ-D14 한 줄을 오늘 작업 여럿이 가리키면 = 가장 앞선 상태(시술 중 > 시술 전 > 시술 후) · 시술권 없는 작업 = 이번 구매 항목 줄에 진료항목으로 붙임(못 붙이면 미진행)
- OQ-D16 = W9 대로 KOS id 없을 때 버튼 꺼짐만
- OQ-D17 새 오류 토스트 글자 = 빈 문구(공용 처리) 그대로
- OQ-D18 = KOS 결과대로 · 시간 목록 = 그 그룹 간격
- OQ-D19 = `ticket.created_at` → id 순 · W10 대로 가격 나누기 뺌
- OQ-D20 = 그 방문 날짜의 마지막 행 · 값 이름 `confirmed` / `unconfirmed`
- OQ-D21 = F2 대로 삭제
- 남겨도 되는 OQ: 실물 · 결정 근거가 정말 없는 것만(빈 오더 메모 등)

## 검증 · 보고

`python3 scripts/lint-pipeline.py --strict` → products/day 0 error. 보고 본문에 F1 ~ F3 · W1 ~ W12 처리표(고친 자리 파일:줄) · D49 ~ D52 반영 자리 · 남은 OQ 목록. 완료 보고는 앞 브리프 §9 두 명령 그대로(subject 「planner 완료: 고침 1」 · task-id · dispatch-id 는 이번 dispatch 값).
