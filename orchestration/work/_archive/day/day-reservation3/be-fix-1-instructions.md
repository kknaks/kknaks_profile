# [backend] 고침 1 — 코드 검수 1차(`review-code-1-report.md` 이 폴더) BE 몫

⚠ 워크트리는 코디가 **origin/dev `3543d8b2`(#298) 위로 옮겼다** — 변경은 그대로 미커밋으로 있다. #298 은 코드 안 SPEC-007 인용 「고침 5 → 고침 6」 번호를 바꿨다(인용 번호는 손대지 마라 · 코디가 spec 머지 때 맞춤). frontend 가 같은 워크트리에서 FE 몫을 동시에 고친다(templates · static · styles · `routers/reservation_requests.py` · tests/day/web) — 건드리지 마라.

코디 기본값(11-26 · 「코디 결정」):
- **F1(BE 쪽)** `read_window` 의 `pending_write_id` = **보내는 중(확인 대기 · 실패 아님)일 때만**. 실패 묶음이면 비우고 `action="failed"` 만.
- **F2** 공용 `retry` · 스레드 retry 의 되살리기 UPDATE 를 **그 event 의 행만**(`event_id`)으로. 공용 길은 `payload.request_id` 있는 event 행을 빼고, 스레드 길은 그 확인 대기 event 만. 「접힌 행 + 같은 방문 다른 실패」 infra 테스트.
- **F3** 리포트 ①~⑤ 서비스 infra 테스트 + ext TestClient E1 · E2 한 줄씩(`X-Day-Client` 400 · 한도 키 · `Idempotency-Key` 빠짐 400 · 구분 값 하나도 없음 400 · `customer_changed`).
- W1 `customer_changed` 판정 = `booked(state)`(확인 대기 포함) · 대기 중 `thread.customer_id` 덮지 않음.
- W2 E4 설명(OpenAPI description)에 「다음 `updated_since` 는 받은 가장 늦은 `updatedAt` 에서 5분 앞으로 겹쳐 읽고, 겹친 것은 `requestId` · `version` 으로 거른다」 — 코드 값은 그대로.
- W6 `grants()` 에서 같은 `hospital_id` 가 둘이면 503 `ext_unavailable` + 로그.
- W7 앱 `NotificationTarget` 새 칸 = `None` 기본 + 응답에서 뺌(앱 계약 그대로).
- W8 `read_list` N+1 제거(한 번에 읽기) + query-count 테스트.
- W9 초진 W1(같은 고객 찾기) = **잠금 전에** 부르고, 잠금 안에서는 판정만 다시.
- W11 「예약 없음 ∧ 답할 버전 `cancel`」 = 스레드 **취소됨**으로 닫고 `reservation_applied`(취소) 남김(링키가 고객에게 알릴 수 있게) — 버튼 없음.
- W13 E2 스레드 찾기를 `_check` 앞으로 · `Idempotency-Key` 범위 = 표마다라고 E1 · E2 · E6 description 에.
- W3 · W4 = 코디 e2e 에서 실물 확인(코드 그대로 · 결과 오면 따로 지시).

검증: `scripts/test.sh` 전체 1회 · `scripts/check.sh --pure` 1회. 완료 보고 = 브리프 §9 두 명령 · subject `backend 완료: 고침 1`.
