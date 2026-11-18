# WORK-010 구현 보고 — 허브 로컬 DB 화(WP-0 ~ WP-4) · backend

워크트리 `PROCEDURE-HUB/phub-gold-jev`(HEAD 85c28af 위 · **커밋 안 함**) · 2026-11-17. 접속 값은 `set -a; . 파일; set +a` 로만 올렸다(내용을 찍지 않음). 18105 · 18106 · 18220 · 18210 · 18005 · PG 컨테이너는 건드리지 않았다(18105 에는 GET 조회만).

## 변경 파일(`git status --porcelain` — 전부 `backend/` · allowed_paths 안)

새 파일 10: `app/model/medallion.py` · `app/modules/gold/{silver_contract,medallion_load,db_inputs}.py` · `alembic/versions/b202611170001_medallion_tables.py` · `scripts/load_medallion.py` · `tests/medallion_fixture.py` · `tests/test_medallion_{model,load,repo}.py`
고친 파일 13: `app/model/__init__.py`(import 1줄) · `app/modules/gold/{config,inputs,repository,service}.py` · `app/gold_main.py` · `tests/{gold_fixture,gold_support,test_gold_mcp,test_gold_rest,test_gold_tools_synthetic}.py` · `envs/.env.example` · `README.md`
무시 파일 새로 0 · CSV · dump · db 파일 0.

## WP-0 — 결정 = 지연 FK(대안 안 감)

| # | 결과 |
|---|---|
| Z-1 | 127.0.0.1 18432 phub_medallion · public 0 |
| Z-2 | 같은 표본 `compare_metadata` = `[]` · 역검증(FK 옵션 뺀 판) = diff 6(remove_fk/add_fk) · **W-2**: 모델에서 표 하나 뺀 판 = `remove_table` 잡힘 |
| Z-3 | `autoincrement=False` → 시퀀스 0 · default 없음 / 빼면 시퀀스 1(`nextval`) |
| Z-4 | SQLite `create_all` OK · DDL 에 DEFERRABLE |
| Z-5 | 표 사이 순환 0 · 자기 참조 11 |
| Z-6 | 데이터 없이 592 passed / 48 skipped 32.3s · 있이 638 / 2 · 34.9s · public 다시 0 |

## WP-1 — DT1 ~ DT3 · DE1

- 새 74 · FK 82(전부 deferrable/deferred) · 인덱스 30 · 유일 3 · 칸 749 · 이름 189개 최대 63 · 중복 0 · 옛 이름 겹침 0 · 기존 167 ↔ 새 74 FK 0.
- 마이그레이션 = autogenerate 후 굳힌 고정본(create_table 74 · create_index 30 · 앱 import 0) · heads = `b202611170001` 하나.
- **DE1**: upgrade head → check「No new upgrade operations」 · public **242**(alembic_version 빼면 **241**) · new 74 · 새 테이블 시퀀스 0 · FK 82/82/82 → downgrade -1 → 168(167+1) → upgrade → 242 → check 통과. 적재 **뒤** check 도 통과.
- 시간: WP-1 직후(모델만 추가) 40.2s(1.24배).

## WP-2 — 적재기(DT4 ~ DT8 · DT13) — 30 passed

- exit 0/2/3 · 접속 실패 = 2 · V11(파일 이름 겹침) · V12(원장 id 유일 · 빈칸 0) · 파일마다 1회 읽기(시험이 74 파일 × 1 셈) · 멱등 · 출력에 값 본문 · 비밀번호 · 사용자 이름 0(시험).
- A-6: `executemany` 꼴 + 묶음 = 30,000 ÷ 칸 수(asyncpg 한도 안). 가장 큰 표 `s_source_ref` 48,094행 354ms · 전체 싣기 1.58s · 프로세스 2.95s.
- V10 다형 셈은 silver 15칸만(gold 다형 짝은 세지 않음 — SPEC V10 을 silver 로 읽음).

## WP-3 — DB 판(DT9 ~ DT12 · DT14 · DT15) — 23 passed

- `MemoryGoldRepository(inputs, started)` 몸통 + `CsvMemoryGoldRepository(settings)` 하위(A-3 · 부르는 꼴 그대로) · `GoldState.load_from` · lifespan `load_state`(모르는 값 = lifespan 에서 `GoldLoadError` — N-4) · 시작 로그 한 줄(`uvicorn.error` 로거: 판 · host/port/db · gold_hash) · health 새 필드 0.
- `DATABASE_URL` 읽는 자리 = `GoldSettings` 하나(A-1). `app.core.{db,tx,config}` import 0(grep).
- DT10: 같은 medallion 폴더로 SAME 11 요청 REST+MCP · 쪽 넘김 4개 끝까지 → 두 판 같음 · health 열쇠 집합 같음.
- `memory.py` · 도구 코드 · router · mcp_server · swagger diff 0 · `app/core` · `app/main.py` diff 0.

## WP-4 — 실물

| # | 결과 |
|---|---|
| DE2 | exit 0 · gold_hash `8accbb21…f6228c` · aux_hash `6435fe41…1803a3` · 실을 행 **129,527** · 다형 못 찾음 15칸 전부 0 · DB 접속 0 |
| DE3 | exit 0 · gold 62,244 · silver 66,936 · 원장 확인 273 · 빌드 74 · `''` 0 · 커밋 통과(지연 FK 위반 0) |
| DE4 | 다시 싣기 exit 0(built_at 만 바뀜) · 헤더 한 칸 바꾼 사본(세션 임시 폴더) → exit 2 「V5」 · 빌드 기록 불변 |
| DE5 | 18107(db) vs 18105(csv) health — loaded_at · load_ms 빼고 같음 · 열쇠 같음 · files 22 · expected_hash_checked true/true |
| DE6 | 답 키 `calls/` 37 파일 55 호출(69 쪽 끝까지) REST 차이 **0** · MCP 60 호출(도구 9 전부) 차이 **0** · gold_hash 8accbb21 · 실물 pytest `tests/test_gold_*.py`: CSV 판 291 passed / 0 skip = DB 판(GOLD_REPOSITORY=db + PG URL) 291 passed / 0 skip · 뒤 PG 빌드 기록 그대로 |
| DE8 | load_ms CSV 243 · DB 821(18107 첫 시작 — 모델 import 222ms 포함 · A-11) · `read_db_inputs` 단독 343ms · 표 읽기 s_source_ref 110ms · g_evidence 32 · g_edge 40 |
| 18107 | 스스로 내림 — `lsof -nP -iTCP:18107 -sTCP:LISTEN` **0 줄** |

## 마감 검증

- `ruff check .` 통과 · `alembic heads` = b202611170001.
- 전체 pytest(SQLite): 데이터 없이 **739 passed / 49 skipped 74.4s** · 있이 **786 passed / 2 skipped 75.0s**(기준선 592/48 32.3s · 638/2 34.9s).
- **시간(A-10 · 고치지 않음)**: 2.3배. 원인은 새 시험(+147 — DB 판 매개변수화로 합성 · REST · MCP 시험이 두 번 돌고 판마다 fixture 적재). 기존 시험만(csv 판 · medallion 제외) 36.2s. 모델 74 추가분만 재면 1.24배. CI 15분 제한에는 멀다.
- 공개 grep(§9) 0 · 홈 경로 0 · `app.core.*` grep 0.

## 바뀐 기존 시험 fixture(본문 0 줄)

| 파일 | 줄 | 까닭 |
|---|---|---|
| `tests/gold_fixture.py` `settings_for` | `GOLD_REPOSITORY="csv"` · `DATABASE_URL=""` 2줄 | W-1 — 프로세스 env 를 물려받지 않게 |
| `tests/gold_support.py` | `real_settings` 2줄 · `make_state` 새 함수 · `real_state` 가 그것을 부름 | 실물 시험을 DB 판으로도(env 없으면 지금과 같음) |
| `test_gold_tools_synthetic.py` `svc` | `params=["csv","db"]` | DT10 두 판 |
| `test_gold_rest.py` `fx` | 같음 | 〃 |
| `test_gold_mcp.py` `running` | autouse `_repo_kind` 매개변수 + `running` 한 줄 | 〃 |

## 공개 이름 · 그 밖

- `inputs.py`: `_read_bytes` → `read_bytes` · `_parse` → `parse`(동작 그대로).
- 기존 가드 `test_no_score_rank_inputs` 가 적재기의 변수 이름 `rank` 를 잡아 `group` 으로 바꿨다.

## §11 A · NOTE 정한 값

A-1 GoldSettings 하나 · A-2 이름 제안 그대로(+ `MemoryGoldRepository` · `load_state` · `medallion_specs()` 는 `medallion.py` 머리) · A-3 위 · A-4 계층 · concern_site 도 load_seq 순 · A-5 표마다 0 ~ 2행 · `s_external_code` 0행 · A-6 위 · A-7 V11 · V12(SPEC 되적기 후보) · A-8 기본 csv · 접속 실패 exit 2 · health 새 필드 없음 · A-9 대안 안 감(SPEC §2-6 그대로) · A-10 위 · A-11 모델 import 222ms. N-3 수는 검수 대로 모델 .py 32. N-5 · N-6 · N-7 · N-8 WORK 그대로.

## 남은 것(코디 몫)

DE7(18105 를 db 판으로 · 앱 37 키 대조) · 커밋 · SPEC 되적기(V11 · V12 · A-1 · A-4 · 기본 csv · V10 범위).
