# reviewer 코드 검수 4 — 검수 3 반영 + 내부 API 만

원 브리프 `customer-erd-review-brief.md` 규칙 그대로(읽기만 · 리포트 1개 · 커밋 금지 · §9 완료 보고 두 명령 — 이번 dispatch preamble 의 task-id · dispatch-id).

## 대상

- 지시서: `sync-fix-2.md`, `sync-fix-3-internal-only.md`(맨 아래 「추가」 절 포함)
- 앞 리포트: `review-code-3-report.md`(FAIL-1 · WARN-1~5)
- 워커 리포트: `be-2-report.md` 「검수 3 반영」
- 계약: spec 워크트리의 SPEC-002 ㉔ · SPEC-000 §2(「운영 동기화 공개 API 0」 원칙)
- diff: `git -C /Users/kknaks/orca/workspaces/CENTURION_DAY/customer-erd diff origin/dev` + 미추적 파일

## 볼 것 (PASS/WARN/FAIL + 파일:줄)

1. **FAIL-1 이 닫혔나** — 못 푼 티켓을 하루 동안 기억하는지(TTL · 병원별). 「구매 · 티켓 바뀜」이면 다시 큐에 넣는지. 테스트(두 번째 회차는 구매 호출만)가 있는지.
2. **WARN-1** — 오늘 구매 회차가 별도 태스크(.kiq)인지.
   - 일정 태스크의 실행 시간 · DB 세션 · 반환값이 새 동기화 전과 같은지.
   - 입력 전달 방식(메시지 · Redis)이 KOS 호출을 늘리지 않는지.
   - 메시지 유실 · 중복 시 동작.
3. **WARN-2** — `fetch_schedules` 안의 예외 범위가 넓어졌는지. 판 입력이 같다는 테스트가 있는지.
4. **5분 회차 삭제** — 코드 · 스케줄 · Redis 키 · 설정이 남아 있지 않은지(죽은 코드 0).
5. **내부 API 만**
   - 운영 경로(demo 제외)의 `"open"` 호출 0.
   - 공개 토큰 발급 0(테스트로 확인되는지).
   - 구역 내부 경로 · `mapper.zone` 변경이 기존 결과(구역 id · 방)와 같은지.
   - 기존 동기화 테스트가 통과하는지.
6. **메뉴 진료항목 · 기기 · 약물** — `get-products` 안에서 모으는지. id 중복 제거. 「사라짐 ≠ 삭제」가 테스트로 지켜지는지.
7. **기존 운영 코드 변경 범위** — 구역 경로 · 일정 태스크 발행 · 예외 범위 말고 기존 동작이 바뀐 곳이 있는지.
8. **직접 1회 실행**: `cd backend && uv run pytest -q tests/day -k "sale or menu or prepaid or ticket or purchase or zone or emr"` + 워커가 만든 새 테스트 파일. DB 가 필요하면 로컬 compose 만 쓴다. 못 하면 pending.

## 리포트

`/Users/kknaks/orca/workspaces/kknaks_profile/DAY-customer/orchestration/work/customer-erd/review-code-4-report.md`
