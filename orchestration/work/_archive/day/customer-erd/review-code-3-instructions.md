# reviewer 코드 검수 3 — 2단계 동기화 전체 (+ 실물 발견 반영)

원 브리프 `customer-erd-review-brief.md` 규칙을 그대로 따른다(읽기만 · 리포트 1개 · 커밋 금지 · §9 완료 보고 두 명령 — 이번 dispatch preamble 의 task-id · dispatch-id).

## 대상

- 발주서 `customer-erd-be-2-brief.md`(지킬 것 1~4 · §3 계약 · §6 단계) · 지시서 `sync-fix-1.md`(F-1~F-5) · OQ-71 코디 답(`_RESUME.md` §2).
- 워커 리포트 `be-2-report.md`(그대로 믿지 말고 diff 로 본다).
- 계약: spec 워크트리 SPEC-002 개정 ㉔ 전부 · SPEC-000 §4(2026-11-19 개정 포함).
- diff: `git -C /Users/kknaks/orca/workspaces/CENTURION_DAY/customer-erd diff origin/dev` + 미추적 파일.

## 축 — 각 PASS/WARN/FAIL + 파일:줄

1. **기존 동기화 격리(가장 중요)** — 새 메뉴 · 오늘 · 5분 회차가 실패 · 지연 · 예외를 내도 기존 일정 10초 · 기준 정보 1시간 결과가 같은가.
   - 볼 곳: 잠금 · 트랜잭션 · 타임아웃 · 상한.
   - 기존 함수의 동작 · 반환 · 호출 수가 바뀌었나(더하기만인가).
   - 같은 일정 응답을 재사용하는가 — KOS 호출이 늘지 않는가.
2. **㉔ 대조** — 루프 · 원천(내부/공개) · 경로 · 요청 키 · 바뀐 것만 · upsert/사라짐 · 번들 순서 · 매핑 표 · entity_type 이 SPEC 과 같은가.
   - 지어낸 경로 · 필드가 0 인가.
   - 5분 회차는 공개 통계를 id 나열에만 쓰는가.
3. **소프트 딜리트** — 물리 DELETE 0 · 되살림 처리 · `mark_absent(within=…)` 범위가 맞는가.
4. **실물 발견 F-1~F-5 · OQ-71**
   - F-1 외부 id `chargingId:주머니` 와 거래 연결
   - F-2 nullable(마이그레이션 · 모델 · SPEC 일치)
   - F-3 enum
   - F-4 pending → items 같은 행
   - F-5 두 번 조회
   - OQ-71 퇴사 직원 포함 · 건너뜀 카운트
5. **0010 변경** — FK 인덱스 7개는 새 테이블에만 있나 · 기존 테이블 변경 0 · 왕복.
6. **보안 · 개인정보** — 로그 · 예외 · 테스트 픽스처에 실명 · 전화 · KOS id · 토큰 · 계정 값이 0 인가.
   - 테스트 계정 경로가 코드에 박혀 있지 않은가(로컬 확인 전용인가).
7. **부하** — 회차당 호출 수 · 상한(20명 · 20장) · Redis 키 만료.
8. **테스트** — 격리 테스트가 실제로 「새 부분 예외 → 기존 결과 같음」을 검증하는가.
   - 직접 1회 돌린다: `cd backend && uv run pytest -q tests/day -k "sale or menu or prepaid or ticket or purchase"` + 워커가 만든 격리 테스트 파일. DB 가 필요하면 로컬 compose 만 쓰고 사용자 포트는 쓰지 않는다. 못 하면 pending.
9. **직원이 실물에서 만날 자리** — 판 · 앱에서 달라지는 것(없어야 함).

## 리포트

`/Users/kknaks/orca/workspaces/kknaks_profile/DAY-customer/orchestration/work/customer-erd/review-code-3-report.md` — 전체 판정 · FAIL 고칠 곳 · 사용자 판단.
