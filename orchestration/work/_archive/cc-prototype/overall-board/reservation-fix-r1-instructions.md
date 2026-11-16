# 코드 수정 r1 — reviewer 코드 r1 반영 (backend · frontend)

원천: `/Users/kknaks/orca/workspaces/kknaks_profile/예약현황-poc/orchestration/work/overall-board/reservation-review-code-r1.md`. 코디 처분:

| # | 몫 | 할 것 |
|---|---|---|
| F1 | frontend | `DetailModal.tsx:944` 상담 카드 「{이름} 실장 호출됨 · HH:MM」의 {이름} = `cons.counselor?.name`. 호출한 계정은 보이려면 「· 데스크 {calledBy}」 따로 |
| W1 | backend | **코디 확인: addendum W4 는 「부도를 연다」만 뜻했다** — 메모 저장 = `main ≠ canceled` **그리고 `flow_step ≠ COMPLETED`**(SPEC §5.14 조건 되살림 · `reservation_rules.py:279` · `service/reservations.py:909` · 시험 1줄) |
| W2 | backend · frontend | 간격 경계 기준점을 하나로: **줄 시작 = 축 시작을 그 칸 간격으로 내림**(`a0 - a0 % iv`, 자정 기준 경계와 같아짐). back `lines`(`reservation_rules.py:129-133`) · front `rowAt` · 줄 그리기(`ScheduleTable.tsx:184-188`) 같이 · back 시험 1줄(60분 칸 + 축 09:30) |
| W3 | backend | 예약 등록 검사 순서 = 400 → 404 → 409(정원은 `kos_write` 직전) — `service/reservations.py:689-726` |
| W4 | backend | `can.unconfirmIdentity` 를 409 `identity_locked` 판정(고객 단위 — 그 고객의 오늘 예약 중 접수 뒤가 있으면 끔)과 같은 식으로 |
| W7 | backend | `domain/errors.py` 의 `NotReady` 지우기(쓰는 곳 0 확인) |
| W5 · W6 | 코디 | E2E #8 에서 확인 · WORK 대상 파일 기록 |

- 검증: backend `cd procedure/back && uv run ruff check . && uv run pytest -q` · frontend `cd procedure/front && npx tsc --noEmit && npm run lint`(build 는 코디가)
- 사용자 포트 · KOS 쓰기 · 커밋 금지 그대로. 끝나면 앞 판과 같은 방식으로 `term_fa2737b7-e69a-40e1-9fac-019199b9dad3` 에 보고(처리 여부 줄마다)
