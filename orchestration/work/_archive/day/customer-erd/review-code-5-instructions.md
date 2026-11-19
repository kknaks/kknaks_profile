# reviewer 코드 검수 5 — 3단계 백필 + 검수 4 WARN 정리

원 브리프 `customer-erd-review-brief.md` 규칙 그대로(읽기만 · 리포트 1개 · 커밋 금지 · §9 완료 보고 두 명령 — 이번 dispatch preamble 의 task-id · dispatch-id). backend 워커가 같은 워크트리에서 로컬 확인 조회 중이다 — 코드는 바꾸지 않으므로 diff 는 안정적이다.

- 대상: 발주서 `customer-erd-be-3-brief.md`(§0 WARN-A·B·D · 지킬 것 1~5 · §3 계약) · 리포트 `be-3-report.md` · diff `git -C /Users/kknaks/orca/workspaces/CENTURION_DAY/customer-erd diff origin/dev` + 미추적.
- 볼 것:
  1. **운영 격리** — 백필이 운영 스케줄 · 오늘 창을 건드리지 않나. `--to` 오늘 이상 거부. 운영 client 동작 불변(PacedTransport · KosPacer 가 백필에만).
  2. **1초 1회** — 재시도 · 토큰 · 세션 해제 호출까지 모든 KOS 요청이 간격 안. 테스트가 그걸 보나.
  3. **세션** — 표시 `backfill` · 기기 제한 자동 해제가 운영 · 사람 세션에 안 닿음 · 끝에 자기 세션만 해제.
  4. **쓰기** — 운영 `apply_*` 재사용 · 소프트 딜리트만 · 멱등(두 번째 실행 0) · 진행 위치(Redis) · resume · dry-run DB 쓰기 0.
  5. **빈 본문 수정**(2단계 오늘 회차에도 닿음) — 빈 본문 2xx = 0건 처리가 「사라짐 → 소프트 딜리트」를 잘못 일으키지 않나(빈 본문이 진짜 0건인지 · 오류인지 구분). 운영 영향.
  6. **WARN-A · B · D** — 닫혔나. B 의 「오래된 메시지 버림」이 정상 메시지를 버릴 위험.
  7. **0010 `visit` 인덱스** — 기존 테이블 인덱스 추가 하나 · 부분 · 왕복.
  8. **개인정보** — 로그 · 출력 · 테스트에 이름 · 전화 · id · 토큰 0.
  9. 직접 1회: `cd backend && uv run pytest -q` 로 새 · 고친 테스트 파일(리포트 목록) + `-k "backfill or sale or emr"`.
- 리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/DAY-customer/orchestration/work/customer-erd/review-code-5-report.md`
