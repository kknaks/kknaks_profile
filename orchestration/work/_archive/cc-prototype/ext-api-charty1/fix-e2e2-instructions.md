# e2e 2번째 발견 — 상담 메모는 KOS 에서 비울 수 없다 (backend 5차 · planner 7차)

원 브리프 제약 그대로. 코디 로컬 e2e(데모 KOS · 시험 고객 example.com 의 시험 예약 2건 · 끝나고 직원 API 로 취소함) 결과.

## 실물
- 공개 `update-schedule-consultation-info {scheduleId, consultationMemo}`: 값이 있으면 바뀐다(200). **`""` · `null` 을 보내면 200 인데 KOS 값이 그대로다**(비워지지 않음). `" "` 은 공백 한 칸으로 저장된다.
- 오더 메모(`change-order-memo`)는 `""` 로 비워진다(정상).
- 상담 메모를 쓴 뒤 같은 일정의 상담사 · 의사 칸은 그대로(쓰기 전 · 뒤 비교). 상담 전(예약 상태) 일정에 써도 200.
- 언어 쓰기 → KOS 반영 · 다른 개인 칸 변화 0 · 원래 값으로 되돌림 확인.
- 새 예약 직후 상세: 1번은 KOS 404 → `reservation_gone`, 다시 부르면 200(다른 1번은 0.4초 만에 바로 200). KOS 쪽 반영 지연으로 보인다.

## 코디 기본값
1. **상담 메모 빈 값 = `400 invalid_request`**(앞뒤 공백 지운 뒤 빈 문자열). message `body.consultationMemo: KOS 는 상담 메모를 비울 수 없어요` 꼴. KOS 를 부르지 않는다. 200 인데 안 바뀌는 것보다 낫다. 오더 메모는 빈 값 = 비움 그대로.
2. 예약 직후 404 는 코드로 막지 않는다(재시도 로직 없음) — Swagger 상세 description 에 「예약을 만든 직후에는 KOS 반영이 늦어 `reservation_gone` 이 잠깐 날 수 있다 · 다시 부르면 된다」 한 줄.

## backend 5차 (4차 끝낸 뒤 이어서)
- 위 1 · 2. 시험: 상담 메모 `""` · `"  "` → 400 · KOS 호출 0 · `event_log` 0. 기존 「빈 값 = 비움」 상담 메모 시험이 있으면 바꾼다(오더 메모 쪽은 그대로).
- 검증: `uv run pytest -q tests/test_ext_write.py` → 전체 1번 · ruff. 4차 · 5차를 한 보고로 묶어도 된다.

## planner 7차
- DEC-012 에 코디 기본값 D 번호(근거 = 이 파일) · Q13 「빈 값 = 비움」을 상담 메모만 고친다는 고침 줄 · SPEC 0.4.6(§6.15 · T64 · §8 Swagger 줄 · 상세 description 한 줄 · 실물 확인 ④ 결과 칸). 값 · id 금지.
