# [reviewer_code] WORK-010 허브 로컬 DB 화 — 코드 검수

- 대상: `PROCEDURE-HUB/phub-gold-jev` · HEAD `85c28af` 위 미커밋(고친 파일 13 · 새 파일 10 — 전부 `backend/`)
- 기준: SPEC-003 0.1.0 · WORK-010 0.1.0 · review-spec-003 · review-work-010 · impl-db-hub-instructions · impl-db-hub-report · _RESUME §2 11-17
- 방법: 읽기 전용. 파일 수정 · stash · checkout 0. 18105 · 18106 · 18220 · PG 18432 접속 0. `.env` · 접속 값 파일 안 열었음. 직접 돌린 것: ruff · pytest 1회(SQLite · README 범위) · scratchpad 스크립트 1개(마이그레이션을 SQLite 메모리에 올려 모델과 대조 — 레포 밖)
- 2026-11-17

## 판정 — **PASS**(FAIL 0 · WARN 0 · NOTE 8)

계약 수(테이블 74 · 칸 749 · FK 82 전부 지연 · 인덱스 30 · 유일 3 · 이름 ≤ 63 · 중복 0 · JSON 칸 0)를 모델과 마이그레이션 **양쪽에서 직접 다시 셌고** 둘 다 맞다. 적재기의 exit 0/2/3 · 한 트랜잭션 교체 · dry-run 때 DB 접속 0 · 파일 한 번 읽기 · DB 판 = CSV 판 같은 `LoadedInputs` 는 코드와 시험 양쪽에서 확인했다. 기존 코드(`app/core` · `app/main.py` · `memory.py` · router · MCP · swagger)는 diff 0이고, 기존 시험에서 기대값을 낮춘 곳도 0이다. NOTE 8개는 커밋을 막을 거리가 아니다 — 다만 NOTE-1 · NOTE-2는 사용자가 DB 판을 처음 띄울 때 바로 만날 수 있는 자리라 커밋 전에 한 줄씩 손보길 권한다.

## 직접 돌린 수치

| 무엇 | 결과 |
|---|---|
| `uv run ruff check app tests scripts` | All checks passed |
| `DATABASE_URL=sqlite+aiosqlite:///:memory: uv run pytest -q --ignore=tests/integration --durations=15`(데이터 env 0) | **739 passed · 49 skipped · 70.88s**(보고 739/49 · 74.4s와 같다) |
| 그중 `[db…]` 매개변수 시험 | 85(collect) |
| 마이그레이션 `upgrade()`를 SQLite 메모리에 → 모델 74표만 `compare_metadata` | 테이블 74 = 모델 74 · **diff 0** · `downgrade()` 뒤 0표 |
| 모델 셈(`ALL_TABLES`) | FK 82 · 그중 `deferrable` + `INITIALLY DEFERRED` 82 · 인덱스 30 · 유일 3 · 칸 749 · 이름 263개 최대 63 · 중복 0 · JSON 칸 0 · 새→기존 167 FK 0 · 기존→새 FK 0 |
| 마이그레이션 파일 | `create_table` 74 · `create_index` 30 · `deferrable=True` 82 · import = `alembic.op` · `sqlalchemy`뿐(앱 상수 import 0) · `revision b202611170001` / `down_revision b202610300001`(지금 헤드와 맞음) |
| 전체 pytest를 `--ignore` 없이 | `tests/integration` 17 collection error(`No module named 'app'`) — README · CI 범위 밖이고 이번 변경과 무관 |

SQLite 대조는 지연 FK 옵션을 비교하지 않는다. PostgreSQL `alembic check`의 지연 FK 일치(W-2 포함)는 구현 보고 Z-2 · DE1 실측에 기댄다(검수는 PG에 접속하지 않았다).

## 볼 것 ① ~ ⑨

| # | 결과 | 근거 |
|---|---|---|
| ① WP-0~4 · SPEC 계약 | ○ | 위 셈. R5 PK(키 없는 3표 = `load_seq`) · R6 NOT NULL(PK · 유일 칸 · `load_seq` · `g_edge.src/dst`) `medallion.py:109-116` · R8 이름 `:76-81` · `load_seq` `autoincrement=False` `:110` · 빈칸 → NULL `medallion_load.py:262` · 읽을 때 NULL → `''` `db_inputs.py:43-44` |
| ② 적재 CLI | ○ | 한 트랜잭션(`medallion_load.py:334-350` — 지우기 → 싣기 → 빌드 기록 → L5 되읽기 → 블록 끝 커밋). 실패하면 `begin()`이 롤백하고 exit 3(`:351-354`). L1 · 접속 실패는 exit 2(`:319-331`). dry-run은 `read_bundle` 뒤 바로 return(`:368-370`)하고 엔진을 만들지 않는다(시험 `test_dt7_dry_run_no_db`가 `make_engine`을 터뜨리게 걸어 확인). 파일 한 번 읽기 = `test_each_file_read_once`(74 파일 × 1). 출력에 접속 값 0 — `describe_target`은 호스트 · 포트 · DB만 내고(`:239-247`) 예외는 타입 이름만(`:320,326`). 시험 `test_connection_failure_message_hides_url` |
| ③ DB 판 = CSV 판 | ○ | 같은 `GoldMemory`(P2 — `repository.py` 몸통 분리). 파일 줄 정렬은 파이썬 `sorted`(`db_inputs.py:158`) · 해시 재셈은 `combined_hash` 그대로(`:139-142`) · `expected_hash_checked` `:180` · health 열쇠 집합이 같다(`test_dt10_health_same_keys_no_new_field`가 7열쇠를 못박음). `ledger_rows_with_code` = 서로 다른 `lck_id` 수(`:176`)는 V12(id 유일 · 빈칸 0)가 있어야 CSV 판 셈과 같다 — 적재기가 V12로 막는다(`medallion_load.py:150-152`). DT9가 `LoadedInputs` 필드 전부를 대조한다 |
| ④ 기존 무변경 | ○ | `git diff origin/release/v1.2.0 -- app/main.py app/core` 0 · `memory.py` · `router/gold.py` · `mcp_server.py` · `swagger_docs` 0 · gold · model · 적재기에서 `app.core.{db,tx,config}` import 0. 기존 시험 변경 = 보고서 표와 같다. `settings_for` 2줄(W-1), 나머지 3파일은 `params=["csv","db"]`만. **단언문 변경 0** · `test_gold_load.py` · `test_gold_real.py` diff 0. `inputs._read_bytes/_parse` → 공개 이름으로 바뀌었고 옛 이름을 쓰는 곳 0 |
| ⑤ alembic | ○ | id · down_revision · 헤드 하나(DT3). downgrade는 autogenerate 의존 역순(자식 → `g_edge` → `g_node` …)이고 SQLite에서 끝까지 돈다. 고정본 꼴(앱 import 0) |
| ⑥ 시간 | NOTE-5 | 70.9s(기준 32s). CI 15분과는 거리가 멀다 |
| ⑦ ruff · pytest | ○ | 위 표 |
| ⑧ 커밋 후보 grep | ○ | `*.csv` · `*.dump` · `*.db` · `*.sqlite` · `.env` 0. 이번 diff와 새 파일에서 `postgresql://…` · `passw` · `secret` · 키 · `/Users/` · `/home/` · `18432` · `phub_medallion` 0. 걸린 2줄(README:30 · `.env.example:1`)은 이전부터 있던 자리 표시 · 예시다. 시험의 가짜 URL은 이어 붙인 문자열이다(포트 1 · 없는 계정) |
| ⑨ 실물에서 만날 자리 | NOTE-1 · 2 · 3 | 아래 |

## 지적

| # | 파일:줄 | 심각도 | 내용 | 근거 | 고칠 방향 |
|---|---|---|---|---|---|
| NOTE-1 | `app/modules/gold/db_inputs.py:97` · `config.py:7-10` | NOTE(실물) | **`GOLD_REPOSITORY=db`인데 `DATABASE_URL`이 `envs/.env`에만 있으면** 「F1 DATABASE_URL 없음(GOLD_REPOSITORY=db)」으로 시작이 실패한다. 허브의 다른 부분과 alembic은 `envs/.env`를 읽으므로 사용자는 「값을 넣었는데?」 하고 헷갈린다. 반대로 `envs/.env.gold`에만 넣으면 alembic은 `envs/.env` 쪽 DB로 간다. README가 「프로세스 env를 붙인 꼴로만」 · 「접속 대상 찍기」로 막아 두었고 적재기도 `target host= port= db=` 줄을 찍으므로 사고로 이어지지는 않는다 | SPEC §4-1 「`DATABASE_URL` 허브 공용 — alembic이 읽는 그 값」 ↔ A-1(읽는 자리는 GoldSettings 하나) | F1 문구에 읽는 곳을 붙인다: 「(프로세스 env 또는 envs/.env.gold — envs/.env는 읽지 않음)」 |
| NOTE-2 | `envs/.env.example:19-22` | NOTE(실물) | gold 덩어리에 `GOLD_REPOSITORY=` · `GOLD_SILVER_DIR=`는 더했지만 `DATABASE_URL` 자리가 없다(1줄의 `DATABASE_URL`은 `envs/.env`용 예시다). gold 덩어리만 `.env.gold`에 옮기면 db 판이 NOTE-1 메시지로 떨어진다 | README gold DB 판 절 | gold 덩어리에 `# DATABASE_URL=   # db 판 · 적재기만 — 프로세스 env 권장` 주석 한 줄 |
| NOTE-3 | `app/modules/gold/db_inputs.py:102,107,116` | NOTE | 허브 시작이 실패할 때 `GoldLoadError(...) from exc`로 원래 예외를 이어 둔다. uvicorn은 lifespan 실패를 traceback으로 남기므로 원래 드라이버 예외 글(예: asyncpg 인증 실패 시 `password authentication failed for user "<사용자>"`, 접속 실패 시 호스트 · 포트)이 로그에 나온다. **비밀번호와 URL 전체는 나오지 않는다**(SQLAlchemy 2.0.50 · asyncpg 예외 글에 DSN 없음). 적재기는 메시지만 찍어서 해당 없음 | 지시 ② 「접속 값이 로그에 안 찍힘」 | 사용자 이름까지 감추려면 `from None`으로 끊고 타입 이름만 남긴다(지금 메시지 꼴 그대로). 그대로 둬도 된다 |
| NOTE-4 | `app/modules/gold/medallion_load.py:363-378` | NOTE | 계약 밖 예외는 exit 1 + traceback으로 끝난다. 예: `csv.Error`(칸 하나가 131,072자를 넘을 때 — `inputs.parse`가 잡지 않음) · 파일 권한 오류 · glob 뒤 읽기 전에 파일이 사라졌을 때의 `GoldLoadError`. DB에 쓰기 전 단계라 쓴 것은 0이다. 실물 DE2 · DE3은 통과했다 | SPEC §4-5 exit 0/2/3 | `read_bundle` 둘레에서 `GoldLoadError` · `OSError` · `csv.Error`를 `LoadInputError`(exit 2)로 바꾼다 |
| NOTE-5 | `tests/test_gold_{tools_synthetic,rest,mcp}.py` · `tests/medallion_fixture.py:170-184` | NOTE | 시간 32 → 71s. 시간은 `[db]` 매개변수 시험마다 `build_db`가 fixture 쓰기 + `create_all` + 적재(별 스레드 새 루프)를 다시 하는 데서 나온다(setup 0.3s × 수십). CI 15분 안이고 기능에는 문제가 없다 | `--durations` 상위가 전부 `[db]` setup 0.31~0.35s | 줄이려면 세션 범위로 템플릿 SQLite 파일 하나를 만들고 시험마다 `shutil.copy`하거나, 읽기만 하는 시험(synthetic · rest)은 모듈 범위 fixture로 둔다 |
| NOTE-6 | `app/modules/gold/medallion_load.py:212-225` | NOTE | V10 「다형 못 찾음」을 silver 15칸만 센다. gold 12짝 · 되짚기 짝은 세지 않는다. SPEC §4-3 V10은 범위를 적지 않았다. 구현 보고가 이미 「SPEC 되적기」 후보로 올렸다 | SPEC §2-7 · §4-3 | SPEC 되적기에서 범위를 「silver 15」로 닫으면 끝 |
| NOTE-7 | `app/modules/gold/medallion_load.py:120-123`(V11) · `:150-152`(V12) | NOTE | SPEC에 없는 검사 둘(V11 세 원천 사이 같은 파일 이름 · V12 원장 id 유일 · 빈칸 0)이 더해졌다. 둘 다 CSV 판과 DB 판이 같은 결과를 내기 위한 전제다(V12가 없으면 `ledger_rows_with_code`가 갈릴 수 있다). 지어낸 동작이 아니다 | review-work-010 · 보고 §11 A-7 | SPEC 되적기 목록 그대로 |
| NOTE-8 | `app/modules/gold/db_inputs.py:79` | NOTE | `medallion_ledger_check`를 `ORDER BY` 없이 읽는다. 결과(`ledger_ids_by_code`는 정렬 · 개수는 집합)가 순서와 무관하므로 맞다. 같은 이유로 F5 대조도 순서와 상관없다 | P6(순서는 gold · `s_source_ref`만 요구) | 그대로 |

## 사용자가 실물에서 만날 자리(⑨)

| 상황 | 지금 동작 | 판단 |
|---|---|---|
| `GOLD_REPOSITORY=db` · `DATABASE_URL` 빠짐 | lifespan에서 `GoldLoadError("F1 DATABASE_URL 없음(GOLD_REPOSITORY=db)")`로 시작 실패 | 맞음. 읽는 곳 안내는 NOTE-1 |
| `DATABASE_URL`이 `envs/.env`에만 있음 | 위와 같음 | NOTE-1 · NOTE-2 |
| 모르는 값(`sql` · `DB` 대문자 · `postgres`) | 앱 만들기는 되고 lifespan에서 「모르는 GOLD_REPOSITORY: 'sql' (csv \| db)」 | 맞음(N-4 · DT12). 앞뒤 공백은 `strip`, 빈 값은 `csv` |
| 빈 DB(마이그레이션 전) | 「F1 새 테이블 없음 — alembic upgrade head · 적재 먼저」 | 맞음. 다음에 할 일이 글에 있다 |
| 마이그레이션 뒤 적재 전 | 「F2 medallion_build 0행 — 적재 먼저」 | 맞음 |
| 접속 실패 | 「F1 DB 접속 실패(<예외 타입>) · <driver> host= port= db=」 | 맞음. traceback 쪽은 NOTE-3 |
| 적재 뒤 허브 재시작 안 함 | 옛 판 그대로(`test_reload_needs_restart`). README에 「재시작 → health 해시 확인」이 있다 | 맞음 |
| CSV 경로 env 넷 없이 db 판 | 뜬다(DT12) | 맞음 |
| 적재기를 테이블 없는 DB(stg 등)에 잘못 겨눔 | L1에서 exit 2 · 쓴 것 0 · 쓰기 전에 `target` 줄을 먼저 찍는다 | 맞음 |

## 남은 것(코디 몫 — 검수 범위 밖)

- DE7(18105를 db 판으로 · 앱 37 키 대조 (나)) — 검수는 실서버를 건드리지 않았다.
- PG에서의 `alembic check`(지연 FK) · DE1~DE6 수치는 구현 보고의 실측을 믿었다(재현하지 않음).
- SPEC 되적기: V11 · V12 · A-1 · A-4 · 기본 `csv` · V10 범위(NOTE-6 · 7).
- 커밋 전 권장: NOTE-1 · NOTE-2(문구 · 주석 한 줄씩). NOTE-4는 선택.
