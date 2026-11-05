# [backend] #225 검수 WARN 반영(fix1) — W1 · W2 · W3 · W4 · W5 · W6

너는 day backend 워커다. 같은 워크트리 · #225 미커밋 변경 그대로 이어서. 앞 브리프 `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/backend-225-brief.md` 의 규칙 그대로.
읽을 것: 검수 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/review-225-report.md` W1 ~ W6.
allowed_paths: 앞 브리프 + `backend/migrations/env.py` · `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/backend-225-spec-compare.py`(W4).

## 고칠 것 (리뷰어 권장 방향 — 코디 결정)

1. **W1** — infra 테스트: upgrade 한 테스트 스키마의 `pg_enum` 라벨(타입별 · 순서 포함)이 모델 enum 과 같다. 새 의존성(alembic-postgresql-enum) 넣지 마라.
2. **W2** — `EncryptedJSONB`: 민감 키의 값이 `str` 이 아니면 `TypeError`(값은 메시지에 넣지 않음) · 최상위가 아닌 곳에 민감 키 이름이 나오면 거절. 테스트 2개(비문자열 · 중첩).
3. **W3** — migration 접속은 서비스용 `statement_timeout` 을 쓰지 않는다: `MIGRATION_STATEMENT_TIMEOUT_MS`(기본 0 = 없음) + `lock_timeout`(설정값, 짧게). 테스트로 alembic 접속의 값 확인.
4. **W4** — 대조 스크립트: 「모델에만 있는 칸」을 불일치로 센다(§2 `deleted_at` 예외 3 은 목록으로 명시). 레포에는 **칸 이름 스냅샷 테스트**(테이블 → 칸 목록) — 칸이 조용히 늘거나 빠지면 실패.
5. **W5** — offline(`--sql`) 분기 맨 앞에 `CREATE SCHEMA IF NOT EXISTS <DB_SCHEMA>` · `SET search_path TO <DB_SCHEMA>, public`. 테스트: `--sql` 출력에 두 줄이 `CREATE TYPE` 보다 앞에 있다.
6. **W6** — alembic 은 `ENCRYPTION_KEY` 없이 돈다. 키 필수 검사는 api · worker · scheduler 기동(또는 암호화 칸 첫 사용)으로 옮긴다 — **평문 폴백 없음은 그대로**(키 없이 암호화 칸 읽기/쓰기 = 오류). compose `migrate` 서비스는 키를 안 받아도 되면 빼라(그 한 줄만). 테스트: 키 없이 `alembic upgrade` 성공 · 키 없이 api 기동 실패.

## 하지 말 것

W7 · W8 · 「조용히 통과」 5 · 6(UNIQUE 와 소프트 딜리트 · `direct_key`) — **사용자 결정 대기**, 손대지 마라(따로 지시가 갈 수 있다). 커밋 금지. 포트 11040 · 11042 · 11043 만.

## 검증 · 보고

`scripts/test.sh -q` · ruff · 대조 스크립트 1회 · compose(migrate 키 없이 · api · worker 키 있음) 1회.
리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/backend-225-fix1-report.md` — W 별 고친 곳(파일:줄) · 수치. 완료는 preamble 의 worker_done 절차대로.
