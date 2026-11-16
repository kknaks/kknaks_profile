# planner-delivery-board 결과 보고 — done (human gate · 승인 안 함)

방법은 앞 Delivery 와 같다(`start-delivery` · 이 워크트리 `tools/harness` · code repo = CENTURION_DAY v2-dev 로컬 clone). mediness origin/main = `d93b9210…`(SPEC-002 는 `3c14633b` 에 커밋 · PR #909 미머지 → `spec-baseline:pending`). 요청 · 결과 = `delivery/v2-board-backend*.json` · `v2-board-screen*.json`.

## Issue

| | Issue | key | 위험 | plan_digest |
|---|---|---|---|---|
| ① 백엔드 | [CENTURION_DAY#230](https://github.com/MediSolveAIDev/CENTURION_DAY/issues/230) | `day/v2-board-backend` | **L3** | `sha256:f2d64dc02308bded0be1127b7a0d69fbc4ded674a3f84a4e314a5429790d10e0` |
| ② 화면 | [CENTURION_DAY#231](https://github.com/MediSolveAIDev/CENTURION_DAY/issues/231) | `day/v2-board-screen` | L2 | `sha256:aa03c1ea033a7112b3d6c08728ff1820300cb9ba98dc840e872e7044b063b81a` |

둘 다 라벨 `delivery-plan:review` · `execution-plan:ready` · `spec-baseline:pending` · `next_action = review-delivery-plan`(human_gate).

## ① 백엔드 #230 요약

- **Target Delta**: 작업 · 작업 직원 · 상담 동기화 추가분(반영 대기 보호 · `visit.room_id` 규칙을 #226 과 맞춤) · 동작 서비스(Functional Rule 1 ~ 25 · service 한 곳) · 웹 라우트(조각 이름 · 값을 **먼저 고정** — 템플릿은 ②) + 앱 JSON · 케이스 매트릭스(+ `csrf_failed`) · **첫 실제 KOS 쓰기** — `SUPPORTED_WRITES` = HAR 확인 6(change-tasks-room · assignees(시스템 계정) · call-tasks-doctors · change-tasks-doctors · change-flow-step PROCEDURE · change-tasks-complete true) · **#226 W7 outbox 구멍**(중복 발송 · SENT 정체 · 빈 expect) + `(visit_id, seq)` 유일 migration · 토큰 규칙 24 · SSE(board · kos_failed sse-swap) · 「먼저 계약 → 화면」.
- **Acceptance A1 ~ A8**: mapper fixture · **도메인 규칙은 DB 없는 단위 테스트**(AGENTS.md 「테스트」 2026-11-06) · 케이스 매트릭스 · event_log/outbox 적재 · 닫힌 쓰기는 지원 여부로 드러냄 · outbox W7 · SSE · **실물 확인은 데모 지점에만 · 사용자 허락 뒤**(호출 → 수락 → 첫 시작 → 종료 1회).
- **Non-Goals**: 템플릿(②) · HAR 미확인 쓰기(귀가 대기 · 시작/완료 취소 · WAITING 재호출 — OQ-08 · 09 · 10) · OQ-03 · 12 · 13 · 방 옮기기 · 차트 작성 · 앱 화면 · 실제 병원 쓰기 · prod.
- **Review Surface**: baseline pending · HAR 6 요청 · L3 근거(첫 KOS 쓰기 · migration · 직원 토큰) · **HAR 전 [귀가 대기] · 되돌리기 · 재호출의 1차 처리(사용자 판단 — HAR 먼저 / 버튼 끄기 / 다음 조회에 되돌아감 감수)** · 의존 #226 · #227(#227 승인 전) · 대리 수락 결과(OQ-05).
- **의존**: #226 · #227.

## ② 화면 #231 요약

- **Target Delta**: #229 매크로만으로 조립(새 색 · 치수 · 매크로 밖 패턴 금지) · 판 · 인박스 3탭 · 의사 호출 창(원천 「화면 참고」) · 재호출 · 수락 창 · 되돌리기 메뉴 · 차트 읽기 · ① 이 고정한 라우트 · 조각 · SSE 에 붙임 · day.js(경과 · D&D · 팝오버 · 혼합 체크 · 메모) · 빈 방 · 반영 중 안 그림 · 실패 토스트만.
- **Acceptance A1 ~ A5**: 화면 구성 「넣음/뺌」 요소 대응표 · 손 CSS · 인라인 스크립트 · #229 밖 컴포넌트 0 · 상태별 스크린샷 · 두 화면 SSE 동기 · 호출/재호출/수락 창.
- **Non-Goals**: 백엔드 · 새 매크로(#229 로 되돌림) · E06/E09/E10 · 방 옮기기 · 차트 작성 · 앱 · prod.
- **의존**: #229 · ①(#230) — 「먼저 계약 → 화면」.

## 다음 (사용자)

1. #230 · #231 결과 계약 승인 receipt(위 digest).
2. #230 Review Surface — HAR 전 [귀가 대기] · 되돌리기 · 재호출의 1차 처리. (HAR 6개를 먼저 받으면 사라지는 질문)
3. #230 데모 지점 실물 KOS 쓰기 허락(구현 뒤).
