# backend 고침 1 — 목록 밖 enum 값 한 번에 추가 · external_updated_at 왕복 (코디 2026-11-20)

사용자 결정: 로컬 DEMO 결과까지 다 본 뒤 **목록 밖 enum 값을 0012 에 한 번에 추가**(0012 는 아직 머지 전 — 새 마이그레이션 만들지 말고 0012 안에서). 같은 워크트리 · 같은 범위 · 커밋 금지.

1. **enum 값 추가**(DEMO 로그 전부 — 백필 · 업데이트 뒤에도 이 9줄이 전부였다):
   - `task_urgency_level` + `urgent`(KOS `URGENT`)
   - `etc_work_status` + `canceled`(KOS `CANCELED`)
   - `requested_procedure_repetition` + `once_per_reservation`(KOS `ONCE_PER_RESERVATION`) — reservation_rule · reservation_rule_component 두 칸 모두 이 enum
   - `reservation_rule_event_type` + 5값 — KOS `protos.schedule.{ReservationRuleCreatedEvent, ReservationRuleActivatedEvent, ReservationRuleDeactivatedEvent, ReservationRuleRuleSetChangedEvent, DefaultReservationRuleSetEvent}` → DAY 말 `created` · `activated` · `deactivated` · `rule_set_changed` · `default_rule_set`(KOS 문자열은 매핑에만)
   - 매핑 표 · enum 라벨 테스트(`test_enum_labels.py`) · 0012 왕복 갱신.
2. **`external_ref.external_updated_at` 왕복** — 리포트 §7-10. `sync_references.Refs.link` 가 연결을 쓸 때 `external_updated_at` 을 덮지 않게(값이 주어질 때만 쓰기). 기존 반영의 다른 동작 · 반환 · 호출 수는 그대로(더하기 원칙 안에서 이 한 줄 — 코디 허용). 테스트: 같은 회차 두 번 → `external_ref` 쓴 행 0.
3. 검증: 바꾼 테스트 파일만 pytest · ruff 1회. 로컬 DEMO 는 **동기화 두 회차만** 다시(목록 밖 경고 0 · 두 번째 회차 external_ref 쓴 행 0) — 세션은 local 하나만 쓰고 끝에 해제.
4. 리포트 `be-1-report.md` 끝에 「## 고침 1」 절 · 브리프 §9 두 명령(subject 「backend 완료: 고침 1」).
