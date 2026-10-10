# verify 실패 손질 — 수동 SQL ↔ 모델

## 실패

- `tests/architecture/test_external_channel_schema.py::test_manual_sql_is_the_compiled_model_for_every_external_channel_table`
- 원인: `external_messages` 모델의 `CREATE TABLE` 에 WP2-BE 가 더한 `from_me BOOLEAN` 이 있는데, `migrations/manual/2026-10-06-external-channels.sql` 의 정의에는 없다
- 칸 차이는 그 하나뿐이다. 다른 칸 · 제약 · 인덱스는 같다

## 선례 확인

- `2026-10-07-inbox-message-origin.sql`(WORK-012)은 **기존 표**(`tasks` · `work_requests` · `conversation_context_references`)에 `ADD COLUMN IF NOT EXISTS` 만 쓴다. 그 표들에는 「모델 = 수동 SQL `CREATE TABLE`」 시험이 없다
- `external_*` 표는 **그 시험이 「처음 까는 DB 의 정의 = 모델」을 지킨다**. 그런데 10-06 파일은 그 뒤 한 번도 개정된 적이 없다(커밋 1개). 이 표에 칸을 더한 선례가 없다
- 그래서 둘 다 맞게 했다

| 경우 | 쓰는 파일 |
|---|---|
| 처음 까는 DB | `2026-10-06-external-channels.sql` 의 `CREATE TABLE external_messages` 에 `from_me BOOLEAN` 한 줄을 모델 컴파일 순서대로 더했다(`raw` 다음 · `safe_html` 앞) |
| 이미 표가 있는 운영 DB | `CREATE TABLE IF NOT EXISTS` 가 건너뛴다. 칸은 `2026-10-08-notifications-v2.sql:79` 의 `ALTER TABLE external_messages ADD COLUMN IF NOT EXISTS from_me BOOLEAN` 이 더한다(그대로) |

- 두 파일을 어느 순서로 돌려도 결과가 같다. 10-06 파일 머리 주석에 이 개정과 그 관계를 적었다
- **시험은 고치지 않았다**

## 같은 종류의 어긋남 — 다른 표

- `tests/architecture/` 가운데 수동 SQL 을 모델과 대조하는 시험은 **이 파일 하나**(외부 채널 표 아홉)다. 알림 표에는 그런 시험이 없다
- 그래서 같은 방식(모델을 postgresql 로 컴파일해 정규화 비교)으로 직접 확인했다 — **어긋남 없음**
  - `notification_settings` — `CREATE TABLE IF NOT EXISTS` 가 `2026-10-08-notifications-v2.sql` 안에 그대로 있다
  - `notifications` 인덱스 둘 — `ix_notifications_recipient_created`(v2) · `ix_notifications_recipient_seq`(`-index.sql` / `.concurrent.sql`) 그대로 있다
  - `notifications` 칸 — 이 표는 마이그레이션 파일이 없던 표라 v2 가 옛 정의 `CREATE TABLE IF NOT EXISTS` + `ADD COLUMN IF NOT EXISTS` 열 개로 선다. 모델의 칸 전부가 v2 에 있다
  - 적용 뒤 모양이 모델과 같다는 것은 PG 시험 `test_the_v2_sql_numbers_old_rows_and_sync_adds_a_missing_sequence` 가 「SQL 적용 뒤 `schema_sync.plan` 이 빈 목록」으로 지킨다(WP2 판에서 통과)
- 그 밖의 `external_*` 표 여덟은 이번 판에 바뀌지 않았다(시험 통과)

## 검증

`make test-contract-serial FILES="tests/architecture/test_external_channel_schema.py tests/architecture/test_local_stack_targets.py tests/architecture/test_operation_inventory.py tests/architecture/test_architecture.py tests/architecture/test_test_pyramid.py"` → **30 passed** · 0 failed

- 앞 판에서 「시험 줄 밖이라 안 돌림」으로 남겼던 `test_local_stack_targets` · `test_architecture` · `test_test_pyramid` 도 여기서 통과했다

## 고친 파일

- `backend/migrations/manual/2026-10-06-external-channels.sql`(칸 한 줄 + 머리 주석)

작업 중 실수로 워크트리 밖(`orca/workspaces/`)에 빈 파일 하나를 만들었다가 바로 지웠다. 남은 것은 없다.
