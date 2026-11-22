# planner 고침 1 — SPEC-000 §4A 검수 FAIL 반영 (코디 2026-11-20)

검수 리포트: `/Users/kknaks/orca/workspaces/kknaks_profile/day-cc-mig/orchestration/work/day-cc-mig/review-spec-000-4a-report.md` 를 먼저 읽어라. 같은 워크트리 · 같은 3파일 · 같은 범위 제약. 커밋 금지.

- **F1** — `visit.reservation_group_id` 뒤집음을 본문 `:605` · `:912-913` · `:2311` 에도 반영(취소선 + 「2026-11-20 — KOS 예약 단위 사본은 `visit.reservation_group_id · reservation_zone_id`(§4A.3 · OQ-4A-7). 점유는 그대로 `visit_occupied_resource`」). 그 밖에도 같은 칸을 「두지 않는다」고 쓴 줄이 있으면 grep 으로 전부.
- **F2** — 규칙 「enum 은 DAY 말」을 지킨다(예외 만들지 않음 · 코디 기본값). 리포트가 든 칸 전부(그리고 §4A 에서 같은 꼴인 칸을 grep 으로 전부): **관찰된 KOS 값은 DAY enum(소문자 DAY 말)으로 정의**하고 KOS 문자열은 「외부(KOS)」 열 · 매핑에만. TI `treatment_item_status` 는 원본 `treatment_item.status` 와 같은 enum. **목록에 없는 KOS 값이 오면: 행은 버리지 않고 그 칸만 null + 동기화 경고 기록**(CARD 처럼 행째 빠지는 일을 막는다) — §4A 공통에 한 줄. 값 목록을 다 못 본 것은 OQ-4A-9 에 「관찰 값 외 추가는 enum 값 추가 마이그레이션」으로.
- **W1** — KOS `hospitalId` 는 `external_ref(entity_type = hospital)` 로 옮긴다(data_rules 그대로). `hospitalNationality` 는 `hospital.nationality` 와 합칠지 OQ-4A-8 에 맞춰 정리. 나머지 KOS 전용 값(`mode` · `namespace` · `hospitalCode`)은 `crm_connection.tenant_info` 유지.
- **W2** — `treatment_id · treatment_name` 은 한 칸 · 한 원천(TI 묶음 쪽)으로. 다른 경로는 「같은 값으로 보임 — 첫 실값에서 확인」 + 다르면 OQ.
- **W3** — 고객: `created_at` = KOS `createdDateTimeUtc`(§2 규칙 그대로) · `registered_at`(prod 칸)도 같은 키로 받는다고 한 줄(두 칸 같은 값 · prod 칸이라 남김).
- **W4** — `:1814` 표시 고침: `medicines` = prod · `machines` · `medicine_and_machine_names` = dev 에만.
- **W5** — 그대로(설명 유지).

끝나면 lint --strict products/day ERROR 0 확인 · 고친 줄 목록과 함께 브리프 §9 두 명령으로 보고(subject 「planner 완료: 고침 1」).
