# planner-spec002-fix3 결과 보고

## 상태: done (미커밋)

lint `--strict` → 0 error · products/day 경고 0.

## 고친 곳 (`products/day/20-spec/spec-002-procedure-board.md`)

| 항목 | 고친 곳 |
|---|---|
| 머리말 | 개정 ③ 한 줄 |
| **M1** 실패 토스트 | 규칙 22 — 기본값: op 이 `failed` 로 **바뀌는 순간** worker 가 `event_log`(`outbox.failed` · payload = 실패 op · `blockedOpIds`)를 쌓고 웹 SSE 신호 `kos_failed`(id = event_log.id)를 한 번 보냄 → 화면이 `GET /board/toasts/{event_id}` 로 토스트 조각. 판 조각(`GET /board`)엔 실패 칸이 없어 10초 신호 · 조작 뒤에 다시 뜨지 않음 · 그 순간 연결 안 된 화면은 못 봄 · 「보는 화면」 = 그 병원 시술 현황 화면 전부 · 앱 짝 = `/api/board/stream` `kos_failed {eventId, visitId, action}`. API 표에 `GET /board/toasts/{event_id}` 행 · SSE 표 이벤트 · 웹이 받는 법 줄 |
| **M2** 멈춘 op | KOS 쓰기 재전송 줄 — 실패 뒤 같은 방문의 뒤 op 도 `failed`(`last_error` = 「앞 op 실패로 보내지 않음」) · `blockedOpIds`(cc r2 N2) · `failed` 는 반영 대기가 아니라 다음 조회부터 KOS 값으로 덮임 → OQ-07 「KOS 에서 고치면 폴링이 맞춤」 성립. 새 줄: **토큰 없음(규칙 24)은 `pending` 그대로 · attempts 안 올림** — 다른 경우 |
| **M3** | 닫은 OQ-11 「DAY-SPEC-000 변경 없음」 → 「새 칸 없음 — `is_system_account` 설명만 맞춤」. SPEC-000 설명(앞 지시에서 고친 것)에 리뷰어 문구대로 「KOS 담당자(`assigneeIds`)로 쓴다 · 규칙 19 · 25 · 다른 사람 아닌 계정은 1차에 켜지 않는다」를 맞춤 · log 줄에 DAY-SPEC-000 |
| **E51 의사 호출 창** | U-4 에 원천 「화면 참고」 그대로: 모달 · 머리(「의사 호출」 + 방 · 고객 · X) · 왼쪽(검색 → 추천 → 「모든 의사」 ALL · 「콜 잡은 원장이 집도」 → 원장 줄 아바타 · 이름 · 상태) · 오른쪽(선택됨 · 호출할 시술 N개 목록) · 아래 버튼(고르기 전 꺼진 「의사를 선택하세요」) · 판 [n개 호출]이 엶 · 재호출 같은 창 · 기본 = 처음 대상. 시안 E51(팝오버 240)과 다른 곳은 원천을 따른다고 명시. 화면 구성 표 팝업 줄에 U-4 참조 |
| OQ-16 | 닫음 — 403 `csrf_failed`(DAY-SPEC-001 「CSRF (웹)」). 케이스 매트릭스 CSRF 줄 코드도 `csrf_failed` |
| 새 OQ-20(기본값) | 「추천」 묶음 기준 · 원천 상태 글자 「대기」와 규칙 19 세 상태의 대응 — 원천에 기준 없음. 추천 = 비어 있는 원장(cc D-24)으로 두고 글자는 디자인이 맞춤. 사용자 결정 아님 |

## 그 밖

- `products/day/log.md` 2026-11-06 `spec-change` DAY-SPEC-002 · DAY-SPEC-000 한 줄.
- `products/day/20-spec/spec-000-data-model.md` — `staff.is_system_account` 설명 문구만 맞춤(새 칸 없음).
- 사용자 결정 OQ 는 여전히 0 · HAR 요청 6.
