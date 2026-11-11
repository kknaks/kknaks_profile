# 알림 v8 서버 리뷰 W1 정정 — 채팅 푸시 시험의 알림 행 단언 범위

## 상태: done — 시험 파일 1개 · 한 구절 · 제품 코드 변경 0 · 커밋 · push 없음

| 항목 | 값 |
|---|---|
| 파일 | `backend/tests/day/chat/test_devices_push.py`(diff hunk 1개 · `notification-backend-fix-logs/diff.txt`) |
| 전 sha256(HEAD) | `cdc4d2c7326b71007aef69b2c602c00034cafd145013350a4fe32e337c42a39d` |
| 후 sha256 | `2a262e63b46a6444c6482769d9aede842f44b87cb72c338f9f1a92ab60988163` |
| 바꾼 구절 | `select(Notification)`(테이블 전체) → `select(Notification).where(Notification.hospital_id.in_([world.a, world.b]))` + 이유 주석 2줄 |

- 보장은 그대로다: 「채팅 푸시는 알림함에 행을 쓰지 않는다」.
  - 이 시험의 두 병원은 시험마다 새로 만든다. 그 병원들의 알림 행이 `== []` 인지 같은 강도로 본다.
  - 단언을 지우거나 약하게 하지 않았다.
  - 다른 시험(알림 E2E 의 커밋 뒤 훅)이 남긴 행에는 영향받지 않는다.
- 제품 코드 · 모델 · migration · app · spec · env 변경 0. 이번 작업은 위 시험 파일 하나만 고쳤다.

## 검증

| 명령 | 결과 |
|---|---|
| 실행 전 다른 pytest 프로세스 | 없음 |
| `DAY_ENV_FILE=…/deploy/local.env scripts/test.sh -q backend/tests/day/notifications backend/tests/day/chat/test_devices_push.py`(리뷰가 실패를 재현한 역순 — 알림 먼저) | **32 passed** · 8.4s(`reverse-order.txt`) · day_test 스키마 · Redis db15 만 · env 값 출력 0 |
| `ruff check` · `ruff format --check` 그 파일 | All checks passed · already formatted(`ruff.txt`) |

- 전체 787 은 브리프대로 다시 돌리지 않았다. 옛 단언이 같은 역순에서 실패하는 것은 리뷰 로그(`notification-backend-review-logs/focused-infra.txt`)가 이미 재현했다. 이번에 옛 파일로 되돌려 다시 실패시키지는 않았다.
