# customer-erd BE-4 결과 보고 — 백필 스크립트 별도 PR(dev)

## 상태: done (미커밋 · 브랜치 `kknaksss/customer-erd-backfill` ← origin/dev `945be39b`, 그 뒤 dev 진행 없음)

## 수행 — 파일
참고 패치 `backfill-reference.patch`(→ CENTURION_DAY #261 로 옮김 · 파일 삭제) 를 그대로 `git apply` 한 뒤, 0010 변경분만 되돌려 0011 로 옮겼다.

- 패치 그대로: `common/error_codes.py` · `day/emr/{base,factory,normalized_sale,pacing}.py` · `day/emr/kos/{__init__,client,sale_reads}.py` ·
  `day/public.py` · `day/services/emr_backfill.py` · `runtime/backfill.py`(실행 진입점) ·
  `tests/day/emr/{test_backfill,test_backfill_rules,test_sale_sync_rules}.py`
- `day/models/visit.py` — `Index` 정의는 패치대로. 주석의 migration 번호만 `0010` → `0011`.
- **새** `migrations/versions/20261119_0011_visit_reserved_index.py` — revision `0011_visit_reserved_index`,
  down_revision `0010_sale_tables`. upgrade = `ix_visit_hospital_id_reserved_start_at`
  (`visit (hospital_id, reserved_start_at) WHERE deleted_at IS NULL`) 하나 · downgrade = 그 drop 하나.
- **새** `tests/migrations/test_visit_reserved_index_migration.py` — 0009 테스트 관례(잇기 · upgrade 연산 1개 · downgrade 1개).
- `tests/migrations/test_alembic.py` — `HEAD = "0011_visit_reserved_index"`.
- 되돌림: `20261119_0010_sale_tables.py` · `tests/migrations/test_sale_tables_migration.py` 는 dev 와 byte 동일(0010 미수정).

### 진입점 위치
`backend/runtime/backfill.py`(`python -m runtime.backfill`) 유지. dev/prod 이미지에는 `backend/` 만 있고
`WORKDIR /app/backend` 라 `scripts/` 에 두면 컨테이너에서 못 돈다 — 패치 · be-3 §5 와 같다.

### CONCURRENTLY 를 쓰지 않은 이유
- 레포 migration 에 `CONCURRENTLY` · `autocommit_block` 선례가 없다. 0006 · 0009 모두 일반 `op.create_index` 부분 인덱스.
- CONCURRENTLY 는 트랜잭션 밖이라 실패 시 INVALID 인덱스가 남고 버전 기록과 어긋날 수 있으며, offline `--sql` 출력 테스트 관례와도 안 맞는다.
- migration 접속은 짧은 `lock_timeout`(`MIGRATION_LOCK_TIMEOUT_MS`)으로 잠금 대기를 끊어 운영 쿼리를 줄 세우지 않는다.
  `visit` 는 병원 수 × 방문 수 규모라 일반 `CREATE INDEX` 가 쓰기를 막는 시간은 짧다(be-3 §5 주의와 같음).
  행이 매우 많아지면 그때 별도 판단.

## 검증
- 선택: `scripts/test.sh -q tests/day/emr/test_backfill.py test_backfill_rules.py test_sale_sync_rules.py tests/migrations` — **71 passed**
  (migration HEAD · 한 head · downgrade base → 재 upgrade 왕복(0011 down/up 포함) · upgrade 뒤 `alembic check` 차이 없음 포함)
- `scripts/check.sh --pure` — **통과**(구조 · ruff · format · mypy · taut-audit/check · frontend · 테스트 1482 passed).
  처음에 새 테스트 E501 1건 → 고침. 워크트리에 `scripts/frontend/node_modules` 가 없어 `npm ci --ignore-scripts` 한 번 함(gitignore).
- 전체 `scripts/test.sh -q` — **1857 passed** (격리 PG16 · Redis7, 로컬/공유 DB 안 씀)
- `uv run python -m runtime.backfill --help` — 인자 확인(`--hospital --from [--to] [--stage] [--dry-run] [--resume]`).

## 계약 대조
- 패치 그대로 · 바뀐 것은 visit 인덱스가 0010 → 0011 로 간 것 하나 — 같음.
- 수동 실행 · KOS 1초 1회(`pacing`) · 내부 API 만 · 기본 어제까지 · 표시 `backfill` · 운영 스케줄 미연결 — 패치 내용 그대로(변경 없음).
- 0010 미수정 · 커밋/push/PR 없음 · 서버 접속 없음.

## dev / prod 실행 방법 (be-3 §5 그대로 · 바뀐 점: 0011 필요)
먼저 그 환경에 **migration 0011 이 적용**돼 있어야 한다(dev 는 이 PR 배포 시 · prod 는 migrate-prod).
dev 서버에서 지금 임시 패치로 0010 에 인덱스를 얹었다면 이름이 같아 0011 upgrade 가 "already exists" 로 실패할 수 있다 — 아래 확인.

```sh
docker exec day-dev-api-1 python -m runtime.backfill --hospital <병원 uuid> --from 2026-08 --dry-run
nohup docker exec day-dev-api-1 python -m runtime.backfill --hospital <병원 uuid> --from 2026-08 \
  > ~/backfill-$(date +%Y%m%d-%H%M).log 2>&1 &
docker exec day-dev-api-1 python -m runtime.backfill --hospital <병원 uuid> --from 2026-08 --resume
# 다시 돌려 「씀」 0 확인(멱등). prod 는 컨테이너 이름만 day-prod 프로젝트의 api.
```
종료 코드 `0` 끝 · `1` 인자/연결/기준 정보 없음 · `2` 그 밖 실패.

## 이슈 · 코디가 확인할 것
1. **dev DB 에 임시 패치의 인덱스가 이미 있는지** — 드라이런용으로 패치를 얹으며 수동으로 `ix_visit_hospital_id_reserved_start_at` 를 만들었다면
   0011 배포 전에 drop 해야 한다(0011 은 `IF NOT EXISTS` 를 쓰지 않는다 — 관례 · alembic check 일치). 0010 은 dev 원본 그대로 적용됐으니 0010 에서 생긴 것은 아님.
2. 브랜치 upstream 이 `origin/dev` 로 잡혀 있다(`git switch -c … origin/dev`). push 시 `-u origin kknaksss/customer-erd-backfill` 로.
