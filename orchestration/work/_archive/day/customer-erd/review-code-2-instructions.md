# reviewer 재검수 — 메뉴 키 보강분

원 브리프 `customer-erd-review-brief.md` 규칙 그대로(읽기만 · 리포트 1개 · 커밋 금지 · §9 완료 보고 두 명령 — 이번 dispatch preamble 의 task-id · dispatch-id).

- 대상: `menu-keys-addition.md` 지시대로 바뀐 0010 · 모델 · 테스트(be-1-report.md 「보강」 절) + spec 워크트리 SPEC-000 「2026-11-19 추가」 11칸 · `ticket_bundle` 유일.
- 볼 것:
  1. 11칸이 지시서 표와 같은가(이름 · 타입 · nullable · 테이블).
  2. SPEC-000 표와 모델 · 마이그레이션이 일치하는가.
  3. 유일 제약은 `ticket_bundle.purchase_item_id WHERE deleted_at IS NULL` 하나뿐인가 — 나머지 셋은 안 걸렸나.
  4. 기존 테이블 변경 0 이 그대로인가.
  5. 1차 리포트 PASS 항목이 깨지지 않았나.
  6. 직접 1회: `cd backend && uv run pytest -q tests/day/test_models.py tests/day/test_column_snapshot.py tests/migrations/test_sale_tables_migration.py`(DB 필요 테스트는 로컬 compose 만 · 못 하면 pending).
- 리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/DAY-customer/orchestration/work/customer-erd/review-code-2-report.md`
