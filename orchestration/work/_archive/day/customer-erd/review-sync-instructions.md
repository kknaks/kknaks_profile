# reviewer_doc — 동기화 스펙 검수 (SPEC-002 개정 ㉔ + SPEC-000 칸 수정)

원 브리프 `customer-erd-review-doc-brief.md` 규칙 그대로(읽기만 · 리포트 1개 · 커밋 금지 · §9 완료 보고 두 명령 — 이번 dispatch preamble 의 task-id · dispatch-id).

- 대상: `git -C /Users/kknaks/orca/workspaces/mediness-mediness/customer-erd-spec diff origin/main -- products/day/`
- 대조 기준:
  - 발주서 `customer-erd-spec-2-brief.md` §3 결정 1~10
  - 범위 변경 `spec-2-scope-change.md`: 백필 절 없음 · OQ-00-3 메모만
  - 삭제 규칙 `spec-2-delete-log.md`
  - 사실 원천 `kos-sync-research-report.md`
  - planner 리포트 `spec-sync-report.md`
- 축 (각 PASS/WARN/FAIL + 파일:줄):
  1. 결정 1~10 반영 — 빠진 것 · 다르게 쓴 것 · 결정에 없는 정책을 만든 것. OQ 로 열어 둔 기본값 4건이 정말 열려 있나.
  2. 사실 대조 — 경로 · 요청 키 · 공개/내부 구분 · 매핑 값이 조사 리포트와 같은가. 지어낸 경로 · 필드 0.
  3. 백필 — 절차 · 안전 규칙 절이 없고, OQ-00-3 이 열린 채 메모만 있나.
  4. 삭제 — 물리 삭제 문구 0 · 소프트 딜리트 + `event_log`(record.delete · record.restore · payload 키) · 기존 테이블은 OQ.
  5. SPEC-000 수정 — 결정 6 · 7 · 5 만 · prod 칸 · 타입 변경 0(prod 모델 대조) · version 0.0.1.
  6. 범위 · 개인정보 — `products/day/` 밖 변경 0 · 테넌트 · 이름 · id 0 · lint --strict products/day ERROR 0.
- 리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/DAY-customer/orchestration/work/customer-erd/review-sync-report.md`
