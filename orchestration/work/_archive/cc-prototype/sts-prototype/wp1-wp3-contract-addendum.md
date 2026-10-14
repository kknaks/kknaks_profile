# WP1 ↔ WP3 계약 보충 (코디 결정 2026-10-13)

SPEC-001 §5.2 · §5.5 에 필드 세부가 없어 frontend 가 `cc/front/lib/types.ts` 에 먼저 적었다. **이 파일을 계약으로 삼는다.**

- **backend**: 응답 모양을 `cc/front/lib/types.ts` 에 맞춘다(읽기만 — 고치지 마라). 이미 다르게 짠 곳이 있거나 맞추기 어려운 필드가 있으면 `[질문]` 으로. 모양을 바꾸는 쪽은 frontend 가 아니라 이 파일 기준
- **since** = epoch ms(숫자) 하나로 통일. ISO 안 씀
- **현장 접수**: `POST /api/board/check-in {scheduleId: null, name, order}` 허용 — back 이 로컬 일정 id(`walkin-<n>`)를 만들어 고객 · 예약 목록에 넣는다. KOS 참조 데이터는 없음(환자 상세는 이름 · 오더만)
- **보유 시술권**: `GET /api/patients/{scheduleId}` 응답의 `tickets[]`(이름 · left · total · 만료 · 담당 직군 · 수면 여부) — 원천 캡처 `getTicketBundlesQuery`(AVAILABLE). 없으면 빈 배열
