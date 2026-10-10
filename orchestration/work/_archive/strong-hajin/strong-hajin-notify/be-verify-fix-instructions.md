# [backend] 전체 시험 1건 실패 — 수동 SQL 과 모델 어긋남

코디가 E2E 전 `make verify` 를 한 번 돌렸다: **1 failed · 1991 passed**(로그 `/Users/kknaks/orca/workspaces/kknaks_profile/beluga/orchestration/work/strong-hajin-notify/verify-1.log`).

- 실패: `tests/architecture/test_external_channel_schema.py::test_manual_sql_is_the_compiled_model_for_every_external_channel_table` — **`external_messages`** 의 모델(이번에 `from_me` 등 칸이 늘었다)의 `CREATE TABLE` 이 외부 채널 수동 SQL(WORK-011 판) 안에 그대로 없다
- 고칠 것: 이 저장소가 **앞서 칸을 더할 때 쓴 선례**(예: `migrations/manual/` 의 inbox-message-origin 같은 개정)를 먼저 확인하고 그 방식대로 — 처음 까는 DB 용 `CREATE TABLE` 과 운영에 이미 있는 DB 용 `ALTER`(`notifications-v2.sql`)가 **둘 다 맞게**. 시험을 고쳐 통과시키지 마라(시험이 정본이다) — 시험이 정말 틀렸다고 보면 [질문]
- **같은 종류의 어긋남이 다른 표(알림 표 · `notification_settings` 등)에도 있는지** 같은 시험 계열(`tests/architecture/`)로 확인
- 검증: 그 시험 파일 + `tests/architecture/` 관련 파일만(`make test-contract-serial FILES="…"`) · 전체는 코디가 다시 돈다
- 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/beluga/orchestration/work/strong-hajin-notify/be-verify-fix-report.md` · 완료 보고 앞 브리프 §7 두 명령 — subject 「backend 완료: verify 실패 손질」 · text 「[worker_done] backend verify 실패 손질 완료 — <한 줄>」 · 코디handle `term_aa9fb9af-eed1-45ee-baad-95e52082321d`
