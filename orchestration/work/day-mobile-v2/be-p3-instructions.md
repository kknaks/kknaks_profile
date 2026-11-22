# [backend] P3 — 호출 취소 알림(doctor_call_cancel) + P1 남은 것 2개

같은 워크트리 · 브리프 `/Users/kknaks/orca/workspaces/kknaks_profile/day-mobile-v2/orchestration/work/day-mobile-v2/day-mobile-v2-be-brief.md` 의 역할 · 규칙 · 검증 · 금지 그대로(allowed_paths 만 아래로). P1 `a7868dc6` · P2 `e96b0718` 커밋됨. ⚠ mobile 이 `app/` 작업 중 · reviewer 가 P2 를 읽는 중 — `app/` 금지 · git 읽기만(커밋은 코디).

## A. 호출 취소 알림 (P3)
정본(PR 브랜치 스펙):
- `/Users/kknaks/orca/workspaces/mediness-mediness/day-mobile-v2-spec/products/day/20-spec/spec-005-notifications.md` 2026-11-20 개정 전부 — 종류 `doctor_call_cancel` · **그 호출이 완전히 닫힐 때만**(남은 줄 0 · `doctor_call.closed_at` 이 채워질 때) 한 번 · 받는 사람 · 제목 「호출 취소」 · 본문 「{방} · 호출 취소」(방 없으면 「방」) · 원래 원장 호출 알림 닫기(서버 `read_at` · 범위 = OQ-N17 · 재호출 사슬) · 일부 줄 취소 = 알림 없음 · iOS APNs 푸시 · `unread` · 웹 OS 알림(`backend/day/static/day.js` NOTIFY_KIND 넓힘 · 웹 OS 알림 `tag` 닫기)
- `/Users/kknaks/orca/workspaces/mediness-mediness/day-mobile-v2-spec/products/day/20-spec/spec-000-data-model.md` enum migration(`notification_kind` · `push_kind`)
- `/Users/kknaks/orca/workspaces/mediness-mediness/day-mobile-v2-spec/products/day/20-spec/spec-002-procedure-board.md` 규칙 38(호출 취소 — 개정 표시된 새 문장)
- 코드: `backend/day/services/board_calls.py` `cancel_call` · `services/notifications.py` · `enums/notification.py` · `adapters/apns.py` · migration 은 기존 `backend/migrations/versions/` 꼴 · alembic head 이어지게
- **FCM(Android)은 이번 아님**(F1 따로).

## B. P1 검수 남은 것
- `/Users/kknaks/orca/workspaces/kknaks_profile/day-mobile-v2/orchestration/work/day-mobile-v2/review-code-p1-report.md` W-1: 통키 세션 시험 중 경쟁 · 시간 초과 경로(9c cancel 3초 · audio_start in-flight 멈춤 · 새 스트림 cancel · next_turn · 14 · 17b · 21/22/24 · 3 · 19)를 DAY 시험으로 옮긴다(코드 수정 없이 시험만 — 시험이 깨지면 멈추고 보고).
- 통역 동시 상한 3(사용자 결정): `deploy/config/dev.env` · `prod.env` 에 `DAY_INTERPRET_MAX_SESSIONS=3`(주석 「Soniox 조직 TTS 3 · 2026-11-20 사용자」).

## allowed_paths
- A: `backend/day/services/board_calls.py` · `services/notifications.py` · `enums/` · `models/`(필요 칸) · `adapters/apns.py` · `backend/migrations/versions/`(새 파일 1) · `backend/day/static/day.js`(NOTIFY_KIND · tag 닫기 부분만 — 웹 쪽은 이 한 곳 예외) · `schemas/` · `dtos/` 필요 칸 · 관련 테스트
- B: `backend/tests/day/interpret/` · `deploy/config/dev.env` · `deploy/config/prod.env`
- 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day-mobile-v2/orchestration/work/day-mobile-v2/be-p3-report.md`

## 검증
관련 테스트 + migration up/down(테스트 스키마) · ruff 1회씩. 로컬 실물: 테스트 스키마에서 호출 → 줄 전부 취소 → 알림 행 · 원래 행 read_at 확인(목 APNs). 리포트에 A · B 따로.

완료 보고는 dispatch preamble 의 worker_done 그대로. 커밋 · push · PR 금지.
