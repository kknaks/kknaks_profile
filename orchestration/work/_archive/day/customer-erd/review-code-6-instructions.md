# reviewer 코드 검수 6 — 백필 스크립트 레포 PR(브랜치 kknaksss/customer-erd-backfill)

원 브리프 `customer-erd-review-brief.md` 규칙 그대로(읽기만 · 리포트 1개 · 커밋 금지 · §9 완료 보고 두 명령 — 이번 dispatch preamble 의 task-id · dispatch-id).

- 대상: `git -C /Users/kknaks/orca/workspaces/CENTURION_DAY/customer-erd diff origin/dev` + 미추적(브랜치 `kknaksss/customer-erd-backfill`) · 발주서 `customer-erd-be-4-brief.md` · 리포트 `be-4-report.md`.
- 이 코드는 `backfill-reference.patch`(→ CENTURION_DAY #261 로 옮김 · 파일 삭제) 로 이미 검수(be-3 브리프 · 검수 5 는 백필 제외였다)와 DEMO 3회 실행을 거쳤다. 이번엔 **백필 자체를 처음으로 판정**한다:
  1. 운영 격리 — 운영 스케줄 · 오늘 창 미접촉 · `--to` 오늘 이상 거부 · 운영 KOS client 동작 불변(1초 간격 래퍼는 백필 어댑터에만).
  2. 1초 1회 — 재시도 · 토큰 · 세션 해제 호출 포함 · 테스트가 증명하나.
  3. 세션 — 표시 `backfill` · 자동 해제가 이 표시에만 · 끝에 자기 세션만 해제.
  4. 쓰기 — 운영 apply 재사용 · 소프트 딜리트만 · 멱등 · dry-run DB 쓰기 0 · resume.
  5. **0011** — down_revision 0010 · 기존 `visit` 테이블 인덱스 하나 · 부분 인덱스 · 왕복 · 운영 잠금(일반 CREATE INDEX · lock_timeout) 위험.
  6. 개인정보 — 출력 · 로그 · 테스트에 이름 · id · 토큰 0.
  7. 직접 1회: `cd backend && uv run pytest -q` 백필 · 0011 테스트 파일(리포트 목록).
- 리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/DAY-customer/orchestration/work/customer-erd/review-code-6-report.md`
