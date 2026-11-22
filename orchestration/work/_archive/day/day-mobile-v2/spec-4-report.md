# day-mobile-v2-spec 4차 결과 보고 — 검수 3차 잔재 N-1 ~ N-3

## 상태: done (미커밋 · Issue 수정 없음)

이번에 바꾼 파일은 `products/day/20-spec/spec-005-notifications.md` 하나다(줄 번호 = 수정 뒤).

| # | 위치 | 무엇 |
|---|---|---|
| N-1 | S5:458(OQ-N16 행) | 「줄마다 취소하면 알림은 취소 횟수만큼 온다」에 취소선을 그었다. 그 자리에 「→ OQ-N17(닫음): 그 호출이 완전히 닫힐 때만 한 번 · 일부 줄 취소 = 알림 없음」을 달았다 |
| N-2 | S5:473(§5 모델 대조) | 「이번엔 호출 취소 알림을 쓰지 않음 · migration 없음」에 취소선을 그었다. 그 자리에 「→ 2026-11-20 개정: `doctor_call_cancel` 을 `notification_kind` · `push_kind` 에 더함 = migration(DAY-SPEC-000)」을 달았다 |
| N-3 | S5:272(알림 받는 사람 줄 끝) | 지금 코드 사실을 한 줄로 적었다. `cancel_call` 은 그 줄의 유효 호출 하나만 `closed_at` 을 채운다(`services/board_calls.py`). 그래서 지금은 여러 호출이 함께 닫히지 않고, 알림 행 `doctor_call_id` 는 닫힌 그 호출 하나다. 사슬 문장은 코드가 바뀔 때의 규칙으로 남겨 두었다 |

## 검증

- `python3 scripts/lint-pipeline.py --strict` → **0 error, 263 warning** · `products/day/` 줄 **0**(ERROR · WARN 모두). 263 WARN 은 다른 제품이라 무관하다.

## 남은 막는 OQ

3차 보고 그대로다. K18 · 77 · 78(이름) · A50 · A51 은 기본값으로 착수할 수 있고, A52 · A54 는 시안을 기다린다. #262 · #263 의 v2 재결속 목록은 spec-2 · spec-3 리포트에 있다.
