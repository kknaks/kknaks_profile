# planner 4차 — KOS0 결과 고침 줄 (SPEC-008 0.4.3)

원 브리프 제약 그대로. 근거 = `kos0-report.md`(같은 폴더 · backend 워커 · 데모 실호출 · 키 · 꼴 · 건수만). SPEC 판 **0.4.3**(변경 이력 1행) · DEC-012 고침 줄 · WORK-014 KOS0 행 상태 = 완료.

## 코디 기본값 (DEC-012 에 D 번호로 · 근거 = KOS0)

| # | 정함 |
|---|---|
| ① 판정 | **D-16 그대로.** D-17 대안은 쓰지 않음(DEC D-17 에 「KOS0 2026-11-16 — 쓰지 않음」 고침 줄. 대안 관련 절 · T73 은 지우지 말고 취소선 또는 「쓰지 않음」 표시) |
| ② `eventType` | 단계 변경 = `eventType` 의 **마지막 `.` 뒤 조각이 `FlowStepChanged`**(실물 `protos.schedule.event.FlowStepChanged`) |
| ③ `flowStep` | **문자열 enum 이름**(`CONSULTATION_WAITING`) — 숫자 대응표 없음. 「숫자 enum 대응은 KOS0 확인 값」 문구 바꾸기 |
| ④ 시각 | 원소 `raisedDateTimeUtc` 를 쓴다(payload 안 값 아님) · 차례가 섞여 오므로 **최솟값**(지금 규칙 그대로 · 근거 추가) · 소수 자릿수 가변(파싱 문제 — 계약 아님) |
| ⑤ `daysOff` | 원소 = **`{startDate, endDate}`** — KST `YYYY-MM-DD` 둘(끝 = `endDateTime` 직전 시각의 KST 날짜 · 하루 휴무면 둘이 같음 · 여러 날 휴무는 한 원소). KOS 에 이름 칸이 없으므로 `name` 은 빼고 지어 채우지 않는다. §6.16 예시 · T66 · Swagger 줄 맞추기 |
| ⑥ 선불카드 | 금액 객체 `{value, currency}` 확인 → §4.4 고침 없음 · 근거 칸에 KOS0 ③ 추가 |
| ⑦ 내부 시술권 | 다 쓴 · 다 취소된 묶음을 준다(KOS0 ④) → §4.3 「우리가 거른다」 근거를 「확인함」으로 · T50 가짜 응답 그대로 |
| ⑧ T57 가짜 응답 | 원소 6키 · 전체 이름 `eventType` · 문자열 `flowStep` · `payload` JSON 문자열 · 차례 섞임 · 같은 단계 반복 원소 둘 |

## 보고
고친 곳 표 · public grep. 새 질문은 결정하지 말고 모음. 두 채널로.
