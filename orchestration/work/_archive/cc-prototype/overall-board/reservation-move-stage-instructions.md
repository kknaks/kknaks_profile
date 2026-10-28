# backend — 단계별 이동: KOS 그대로 (E2E batch 5 #1 · 코디 · 2026-10-27)

사용자: 상담 대기 카드가 안 끌린다 → 「KOS 에서도 안 되는 거 맞아?」 → 「일단 그렇게 해」(KOS 가 받는 단계는 연다).
지금 `domain/reservation_rules.py:163` `draggable(main)` = 예약 · 접수만 — **KOS 근거 없는 planner 기본값**(SPEC-005 OQ-714). KOS 확인은 `RESERVED` · `RECEPTION` 뿐(`reservation-move-cancel-report.md:31 · :143`).

## 1. 데모 실호출 (허가된 쓰기 — 이동만)
- 데모 테넌트 assert(`.env` 값 출력 금지) · 운영 키 `KOS_API_tenent` 금지
- 단계마다 일정 하나: **상담 대기 · 상담 중 · 시술 대기 · 시술 중 · 귀가 대기 · 귀가 완료 · 취소 · 부도**(+ 확인용 예약 · 접수 1개씩). 그 단계 일정이 데모에 없으면 시험 고객으로 **새 일정을 만들어 공개 `changeFlowStep` 으로 그 단계까지 보낸다**(날짜 = 2026-11-12 KST · 시험 표시 `[ccc 시험]`)
- 각 일정을 ccc 와 같은 길(내부 `update-reservation` — 지금 이동 코드 그대로)로 **같은 날 빈 시각으로 옮기기 → 받으면 원래 시각으로 되돌리기**. 다른 칸(그룹) 이동도 한 번
- 표: 단계 | flowStep · status | 이동 응답(상태 · 오류 className) | 바뀐 필드(시각 · 그룹 외에 바뀐 게 있나 — 특히 flowStep · 작업 · 방 · 상담) | 되돌림
- 이전 날짜(지난 날) 일정 이동도 한 번(받는지만)

## 2. 코드
- `draggable` 을 **KOS 가 받은 단계 = 끌 수 있음 · 거절한 단계 = 막음**으로(main 만으로 모자라면 sub · flowStep 까지 받게). 이동 API(`…/move`)의 같은 검사(`service/reservations.py:926`)도 같은 규칙. front 는 `card.draggable` 만 보므로 front 변경 없음(확인만)
- 시험 고침 · 더함 · `ruff` · `pytest`

## 3. 보고 · 금지
- 보고서 `orchestration/work/overall-board/reservation-move-stage-report.md`(위 표 · 바뀐 파일 · 검증 수치 · **남긴 데모 흔적 목록**) — 값 · id · 이름 금지
- 커밋 금지 · 사용자 포트 3700 · 8700 · 프로세스 금지 · front 금지
- 완료: 앞 브리프와 같은 두 명령(코디 `term_678ac61d-2472-4a9b-ba73-61883337b957`) · 막히면 `[질문]`
