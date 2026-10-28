# 예약 현황 E2E batch 3 — frontend 결과 보고

## 상태: done

기준 = `reservation-e2e-batch3-instructions.md` frontend 칸 · `reservation-e2e-feedback.md` 「# batch 3」. 코드 `09b1edc` 위 · 커밋 안 함. 시술 현황판 코드(`components/procedures` · `procedures/live`) 변경 0.

## 수행 — 파일

- `procedure/front/components/reservations/view.tsx` — 공용 `phaseStyle(main, phase)` · `phaseOfSub(sub)`(부상태 색 규칙 한 곳)
- `components/reservations/ScheduleTable.tsx` — 카드 부상태 칩
- `components/reservations/ResvAside.tsx` — 원내 현황 카드 Badge
- `components/reservations/DetailModal.tsx` — 내원 현황 단계 카드 · 점 · 시각
- `lib/types.ts` — `flow.times`(코디 경유 backend 와 맞춘 이름)

## 처리 여부

| # | 처리 | 내용 |
|---|---|---|
| 1 | 완료 | 지난 단계 = 회색 점(채운 회색) · 회색 제목 · 흰 카드. 「접수 완료」는 상태가 접수일 때만 지금 단계, 다음 단계가 시작되면 회색. 지금 단계만 그 주 상태 색 |
| 2 | 완료(front) | 단계 줄 `[제목][상세] …… [HH:MM]` 의 시각 = `flow.times.{consultation, procedure, home}`(ISO · 없거나 null 이면 비움). 상담은 `times.consultation` 이 없으면 기존 값(진행 중 = 시작 · 그 밖 = 호출 시각). 계약 = 코디 답 「flow.times 그 이름으로」 — 가짜 back 이 이미 이 값을 줘서 시술 완료 15:25 · 귀가 완료 16:00 이 그려지는 것 확인 |
| 3 | 완료 | 규칙 = `phaseStyle(주 상태, 단계)` 하나: **대기** = 연한 배경(100) + 그 색 글자 · 점 ○ / **진행** = 그 색 채움 + 흰 글자 · 점 ●(채운 카드 위라 흰 점) / **완료** = 회색(주 상태 무관) / **아직** = 흰 바탕 · 회색 ○. 주 상태 색: 예약 purple · 접수 yellow · 상담 cons · 시술 primary · 귀가 gray-600 · 취소/부도 red. 적용: 스케줄 표 카드 부상태 칩 · 내원 현황 단계 카드 · 점 · 원내 현황 카드 Badge(부상태 없으면 대기 꼴) |

## 검증

- `npx tsc --noEmit` 0 · `npm run lint` 0 · `npm run build` 성공
- 화면: 임시 front 3790 · back 8790(가짜 모드 · KOS 주소 막음) headless 1920 폭 — 콘솔 오류 0 · 끝나고 종료(포트 비어 있음) · 사용자 포트 안 건드림
  - `fe-shots-reservation/e2e-b3-chips.png` — 카드 칩 3종(顾客 D 상담 대기 = 연한 초록 · 고객 E/G 진행 = 채움 · 고객 I 완료 = 회색) + 원내 현황 Badge
  - `e2e-b3-flow-procedure.png` — 접수 완료 회색 · 상담 진행 중 채움(흰 글자 · 흰 점) · 시술/귀가 아직
  - `e2e-b3-flow-consult-waiting.png` — 상담 대기 = 연한 색 + ○
  - `e2e-b3-flow-home.png` — 전부 지난 단계 회색 · 시각 3개(14:50 · 15:25 · 16:00)

## 코디가 확인할 것

- 진행 단계 카드는 통째로 채움(흰 글자) — 카드 안 [상담사 변경] 버튼은 흰 버튼으로 그대로 보임. 너무 진하면 「카드는 연한 색 + 점 ●」로 낮출 수 있음
- 상단 범례 Badge · 상세 머리 색은 주 상태 색 그대로(부상태 규칙 대상 밖으로 둠)
