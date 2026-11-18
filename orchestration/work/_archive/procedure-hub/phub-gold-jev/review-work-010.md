# WORK-010 0.1.0 검수 — 허브 로컬 DB 화 구현 계획

검수: reviewer_doc(read-only) · 2026-11-17 · 대상 `WORK-010-hub-db.md` 0.1.0(442줄) · 계약 `SPEC-003-hub-gold-db.md` 0.1.0 · 허브 `phub-gold-jev` HEAD `85c28af`(작업 트리 변경 0)
지시: `work-db-review-instructions.md` ① ~ ⑥ · 기준: `_RESUME.md` §2 11-17 행(U-1 · U-2 · W-1 ~ W-4 · B-1 ~ B-3) · `review-spec-003.md`

## 판정

**WARN — FAIL 0 · WARN 3 · NOTE 8. 구현 진행 가능.**

WARN 3 은 WORK 를 다시 돌릴 거리가 아니다 — 구현 발주서에 한 줄씩 받으면 닫힌다. **W-1 은 WP-2 를 시작하기 전에 닫는다**(시험이 로컬 PostgreSQL 의 실은 판을 덮을 수 있는 길이다).

- SPEC-003 ↔ WP 대응: 미대응 **1**(W-2 — O-6 의 둘째 물음) · 지어낸 동작 0.
- 코드 인용 표본 30 가운데 틀림 0 · 수 틀림 1(N-3 — 계획에 영향 없음).
- 돌려 보지 않은 것: DB 접속 · alembic · pytest · 서버 띄우기. 접속 값 파일은 **열쇠 이름만** 봤다(값은 열지 않았다). 18105 에는 `health` GET 한 번만 보냈다.

## 1. 지적

| # | 문서:줄 | 심각도 | 무엇 | 근거 | 고칠 방향 |
|---|---|---|---|---|---|
| **W-1** | WORK:81 · 224 · 225 · 253 · 300-302 | WARN | **시험 설정이 프로세스 env 를 물려받는다 — §8-1 ⑤ 를 적힌 대로 돌리면 합성 시험이 로컬 PostgreSQL 로 간다.** `settings_for` 는 일곱 칸만 박고 나머지는 프로세스 env 에서 온다. ⑤ 는 `GOLD_REPOSITORY=db` + PostgreSQL `DATABASE_URL` 을 프로세스 env 에 둔 채 `tests/test_gold_*.py tests/test_medallion_*.py` 를 돈다. ① lifespan 을 도는 합성 시험(아래 16줄)이 fixture 대신 실물 DB 를 읽어 깨진다 — DE6 의 「CSV 판과 같은 통과 · skip 수」 가 안 선다. ② `test_medallion_*` 의 적재 시험이 URL 을 인자로 박지 않은 설정을 한 번이라도 쓰면 **합성 fixture 가 실물 74 테이블을 지우고 실린다**(L2 — 다시 실으면 되지만 DE5 ~ DE7 이 조용히 틀어진다). WORK 는 「`tmp_path` 의 파일 DB 를 쓴다」(:200)까지만 적었고 「프로세스 env 를 물려받지 않는다」 는 줄이 없다. `tests/gold_fixture.py` 는 「고치는 파일」 목록(:75)에 없다 | `tests/gold_fixture.py:308-319`(`GoldSettings(_env_file=None, **kw)`) · 실측: `GOLD_COVERAGE_NODES_MAX=7` 을 프로세스 env 에 두고 `settings_for(...)` → `7`(박지 않은 칸은 env 값) · `create_gold_app` / `lifespan_context` / `GoldSettings(` 줄 = `test_gold_rest.py` 5 · `test_gold_mcp.py` 3 · `test_gold_coverage.py` 3 · `test_gold_holes.py` 3 · `test_gold_load.py` 2 | 발주서에 세 줄: ① `settings_for` 가 `GOLD_REPOSITORY="csv"` · `DATABASE_URL=""` 를 박는다 — `tests/gold_fixture.py` 를 allowed_paths 에 더한다(두 줄 · 5칸 계층 헤더는 그대로) ② `test_medallion_*` 의 설정은 URL 을 **늘 인자로** 준다 + 그것을 보는 시험 하나(프로세스 env 에 다른 URL 을 넣어도 `tmp_path` SQLite 로 간다) ③ ⑤ 에서 `tests/test_medallion_*.py` 를 뺀다(SPEC DE6 은 「기존 실물 pytest 를 DB 판으로」 만 요구한다 — SPEC:563) · ⑤ 뒤에 `medallion_build` 의 `gold_hash` 가 그대로인지 한 번 본다 |
| **W-2** | WORK:90-97 · 432 ↔ SPEC:345 · 643 | WARN | **O-6 의 둘째 물음이 WP-0 에 없다.** SPEC 은 「확인 안 됨」 을 둘 넘겼다 — 지연 FK 와 「마이그레이션에만 있고 모델에 없는 테이블을 `alembic check` 가 잡는가」. Z-1 ~ Z-6 은 앞의 것만 닫는다(Z-2 역검증은 FK 옵션만 뺀다). §12 는 O-6 → Z-2 ~ Z-5 로 적고 「미대응 0」 이라 했다 | SPEC-003:345(「둘 다 WORK 첫 WP 에서」) · WORK 에 「모델에 없는」 · 「마이그레이션에만」 문자열 0 | Z-2 에 역검증 하나 더 — 표본에서 표 하나를 뺀 `MetaData` 로 다시 비교해 `remove_table` 차이가 나오는가. 닫지 않을 것이면 §11 「이번에 안 함」 에 까닭과 함께 적는다 |
| **W-3** | WORK:225 · 229 | WARN | **DT10 의 두 판이 어느 폴더로 도는지 안 닫혔다.** `db` 판은 `medallion_fixture` 폴더(계약 칸 57표)를 싣는다고 적었는데 `csv` 판의 폴더가 없다. `csv` 판을 지금 `write_fixture`(계층 3표 5칸 · silver 5 파일)로 돌리면 보조 파일 바이트가 달라 `aux_hash` · `health.files[].sha256` 이 갈린다 — `aux_hash` 는 **모든 응답 머리**에 나가므로 「같은 요청의 응답 JSON 이 두 판에서 같다」 가 한 건도 안 선다. DT9 에는 N-3 전제(같은 폴더의 같은 파일)가 적혀 있고 DT10 에는 없다 | `tests/gold_fixture.py:297-299`(5칸) · `inputs.py:144,177-178`(`aux_hash` = 파일 이름 + sha256) · SPEC-003:70(응답 머리의 두 해시) | 한 줄 — DT10 의 응답 대조는 두 판 다 `medallion_fixture` 폴더로(`csv` 판의 `GOLD_SOURCE_REF_PATH` · `GOLD_HIERARCHY_DIR` = 그 silver 폴더). 기존 시험 본문의 통과(두 판 매개변수화)와 「두 판 JSON 같음」 대조는 갈라 적는다 |
| N-1 | WORK:253 · 386 | NOTE | B-2 자리 — `calls[]` 명세는 `data/eval-set/calls/`(37 파일)다. `answer-key/` 의 **형제 폴더**이고 `answer-key/calls/` 는 없다. 원소 열쇠 = `tool` · `request` · `kinds` | 앱 워크트리 `ls`(읽기만) | 발주서에 경로 둘을 풀어 적는다 |
| N-2 | WORK:262 ↔ 코디 답 B-3 | NOTE | §7 마감 6 은 「18107 을 띄워 둔 채 알린다」 · B-3 은 「WP-4 끝에 워커가 스스로 내린다」. 본문 끝에 「발주서가 정한다」 가 있어 부딪히지는 않는다 | _RESUME:35 | 발주서에 B-3 대로 — 내린 뒤 `lsof` 0 줄을 보고에 |
| N-3 | WORK:54 | NOTE | 「`app/model/`(파일 60)」 — 실제 `.py` 는 **32**(`__init__.py` 포함) · `__init__.py` 의 import 줄 31. 「마지막 줄 `:205`」 · 「`__tablename__` 167」 은 맞다 | `find app/model -name "*.py"` · `grep -c` | 수만 고친다(계획에 영향 없음) |
| N-4 | WORK:209 ↔ 222 | NOTE | 「모르는 값 = 시작 실패」 를 어디서 판정하나 — `gold_main.py:72` 가 **import 때** `GoldSettings()` 를 만든다. 설정 검증기에서 터뜨리면 import 자체가 실패해 DT12(lifespan 이 `GoldLoadError`)와 꼴이 갈린다. :222 는 lifespan 으로 적었고 :209 가 모호하다 | `app/gold_main.py:72` | 「판정은 lifespan 에서 · 설정 검증기에 두지 않는다」 한 줄 |
| N-5 | WORK:92 | NOTE | Z-1 의 「`public` 테이블 0」 은 WP-0 을 처음 돌릴 때만 맞다(WP-1 뒤는 242). 검수는 DB 에 접속하지 않아 지금 값은 **확인 안 함** | — | 그대로 둬도 된다 |
| N-6 | WORK:252 · 295 | NOTE | DE5 의 `expected_hash_checked` 가 같으려면 두 판 다 `GOLD_EXPECTED_HASH` 를 받아야 한다. 지금 18105 는 `true` 다 — §8-1 ③ 이 18107 에 같은 값을 주므로 맞는다 | 18105 `health`(아래 §3) | 그대로 |
| N-7 | WORK:339 | NOTE | 공개 grep 의 `passw` 는 적재기가 URL 을 가리는 코드의 낱말(`password`)에도 걸린다 — 주석의 「0」 은 「값 0」 으로 읽어야 한다 | `scripts/import_legacy_corpus.py:114`(`hide_password` 전례) | 주석 한 낱말 |
| N-8 | WORK:96 | NOTE | Z-5 를 미리 셌다 — silver FK 80 · 자기 참조 11 을 빼면 **표 사이 순환 0**. 대안(의존 순서 싣기)이 설 수 있고 `downgrade` 의 의존 역순도 선다 | `silver-schema.json` 재셈 | 워커가 다시 세되 기대값으로 쓴다 |

## 2. 볼 것 ① ~ ⑥

| # | 볼 것 | 결과 |
|---|---|---|
| ① | SPEC-003 ↔ WP 대응 · 지어낸 동작 | 대응 ○ — R1 ~ R10 · §2-2 ~ §2-9 · C1 ~ C7 · V1 ~ V10 · L1 ~ L6 · P1 ~ P10 · F1 ~ F7 · DT1 ~ DT15 · DE1 ~ DE8 · O-1 ~ O-9 가 §12 표와 WP 본문에 전부 걸린다. **빠진 것 1 = W-2.** SPEC 에 없는 것 넷(V11 · V12 · 계층 3표 · `concern_site` 의 `load_seq` 순 · 시작 로그 한 줄)은 전부 검수 N-4 · N-5 · W-1 · W-2 ③ 에서 온다 — 지어낸 동작 0. `health` 새 필드는 W-1 (a) 대로 안 넣는다(WORK:38 · 223) |
| ② | W-1 ~ W-4 · NOTE 8 반영 · A-1 | 12 줄 전부 본문에 있다(§10 표의 「어디」 칸을 따라가 확인). **A-1 은 선다** — 아래 §4 |
| ③ | 실행 가능성(경로 · 명령 · 포트) | 경로 · 줄 인용 맞음(§5). 포트 — 듣는 18xxx = 18105 · 18106 · 18210 · 18220 · 18432 · **18107 비어 있음**. 18105 · 18106 은 같은 허브 워크트리에서 `--reload` 없이 떠 있다 — 워커가 파일을 고쳐도 다시 뜨지 않는다. `envs/` 에 `.env` · `.env.gold` 없음. 새 의존 0(asyncpg · aiosqlite 있음 · alembic 1.18.4 · SQLAlchemy 2.0.50). **걸리는 곳 = W-1(§8-1 ⑤) · W-3** |
| ④ | WP-0 이 「확인 안 됨」 을 실물로 닫나 · 대안 | 지연 FK(Z-2 · Z-4) · `load_seq` 시퀀스(Z-3) · 기준선 시간(Z-6) 은 로컬 PostgreSQL 에서 역검증까지 한다. 대안(지연 없이 — 지우기 역순 + 싣기 순서 + 자기 참조 11칸)과 SPEC 되적기 보고(A-9)가 있다. **O-6 둘째 물음만 빠졌다(W-2)** |
| ⑤ | 완료 조건이 실물을 요구 | ○ — DE1(빈 DB `upgrade` → `check` → `downgrade -1` → `upgrade` · 242 / 241 · 시퀀스 0 · 지연 FK 82) · DE2 · DE3(129,527행 · 되읽기 차이 0) · DE5 · DE6(18105 CSV 판 ↔ 18107 DB 판 · 37 `calls[]` · 쪽 끝까지) 은 워커 · DE7(18105 를 DB 판으로 · 앱 37 키)은 코디. 워커가 18105 · 18220 을 건드리지 않는다는 줄이 세 곳에 있다(:40 · 79 · 307) |
| ⑥ | 비밀값 grep | 0 — 아래 §6 |

## 3. 다시 센 것

| 무엇 | WORK | 재셈 | 식 |
|---|---|---|---|
| gold 모듈 줄 수 | 197 · 124 · 54 · 219 · 170 · 16 · 131 · 72 | 같음 | `wc -l` 8 파일 |
| gold 시험 | 8 파일 2,563줄 | 같음 | `wc -l tests/test_gold_*.py` |
| `create_all` | 28 파일 | 같음 | `grep -rn create_all tests` 28줄 · 28 파일 |
| 기존 테이블 | 167 | 같음 | `grep -rn __tablename__ app/model` |
| 모델 파일 | 60 | **32** | N-3 |
| versions · 헤드 | 2 파일 · `b202610300001` | 같음 | `ls` · `:10-11` |
| silver FK | 80 · 자기 참조 11 · 키 없는 표 2 | 같음 | `silver-schema.json` `columns[].fk` |
| 표 사이 순환 | (Z-5 가 셀 것) | 0 | 자기 참조를 뺀 의존 그래프 |
| 파일 이름 겹침(V11) | 0 | 0 | gold 16 + silver 57 + 1 = 74 / 74 유일 |
| 원장 확인 `id`(V12) | 유일 · 빈칸 0 | 325 / 325 · 빈칸 0 | — |
| 18105 `health` | 22줄 · 해시 둘 | `files` 22 · `gold_hash` `8accbb21…` · `aux_hash` `6435fe41…` · `expected_hash_checked` true · 보조 6줄 순서 = `source_ref` → `concern` → `adverse` → `condition` → `concern_site` → 원장 확인 | GET 한 번 |
| 답 키 명세 | 37 | `answer-key/` 37 · `calls/` 37 | N-1 |

## 4. A-1 — `DATABASE_URL` 을 읽는 자리

| 누가 | 읽는 길 | 엉뚱한 DB 로 갈 길 |
|---|---|---|
| alembic | `alembic/env.py:10,18` → `app.core.config`(`envs/.env` + 프로세스 env) | 프로세스 env 를 빼먹을 때뿐 — §8-1 ⓪ 이 같은 길로 읽어 찍고 「아니면 멈춘다」 로 막는다 · 지금은 `envs/.env` 가 없어 자리 표시 URL(`alembic.ini:89`)로 떨어져 접속이 안 된다 |
| 적재기 · `db` 판 | `GoldSettings.DATABASE_URL`(프로세스 env → `envs/.env.gold`) | 없으면 V1 exit 2 / F1 시작 실패 · 지금 `.env.gold` 없음 · 접속 앞에 호스트 · 포트 · DB 이름을 찍는다 |
| 시험 | `settings_for` · `real_settings` | **W-1** — 박지 않은 칸이 프로세스 env 를 물려받는다 |

- `test_entrypoint_imports_no_db`(`test_gold_rest.py:72-76`) — `app.core.db` · `app.core.tx` 만 막는다. `GoldSettings` 에 칸을 더하고 `app.model.medallion` 을 함수 안에서 늦게 import 하면 그대로 통과한다(`app/model` · `app/modules/gold` 에 `app.core.db` · `tx` · `config` import 0 — 재확인). 지금 README 명령의 `DATABASE_URL=sqlite+aiosqlite:///:memory:` 가 `GoldSettings` 에도 들어가지만 기본 `csv` 라 쓰이지 않는다.
- `test_app_main_untouched`(`:79-85`) — `app/core/**` 가 allowed_paths 밖이라 맞는다. alembic `env.py` 를 안 고치는 것과도 맞는다.
- `test_service_layer_uses_repository_only`(`test_gold_tools_synthetic.py:393-398`) — `service.py` 가 `modules.gold.inputs` 를 못 쓴다는 제약을 WORK:235 가 받았다.

## 5. 인용 표본(30 · 틀림 0)

`inputs.py:37-38` · `:41-46` · `:49-61` · `:64-67` · `:70-73` · `:76-91` · `:111-116` · `:117-120` · `:129-175` · `:166-171` · `:182-183` · `:196` / `headers.py:46` · `:48` · `:57-58` · `:60-61` / `config.py:19` · `:20-21` · `:24-29` / `repository.py:24-37` · `:83-102` / `service.py:28` · `:34` · `:39-40` · `:152-166` / `container.py:15` / `gold_main.py:32-37` · `:72` / `model/base.py:8-14` · `model/__init__.py:205` / `alembic/env.py:10,18-20` · `alembic.ini:89` · `core/config.py:40-47` / `scripts/import_legacy_corpus.py:13` · `:114` / `tests/gold_fixture.py:288-305` · `:298-300` · `:308-319` · `gold_support.py:22-30` · `:36-40` · `:43-47` · `test_gold_rest.py:21-30` · `:72-76` · `:79-85` · `test_gold_mcp.py:19-25` · `test_gold_tools_synthetic.py:20-24` · `:393-398` · `test_gold_load.py:114-125` / `README.md:58-64` · `:82-114` · `envs/.env.example:1` · `:11-25` / `backend-test.yml:33` · `:37` · `:66-70` · `:72-74` · `:76-80` / `.gitignore:46-47` · `:59`

## 6. 공개 레포

```
grep -n -i -E "password=|passwd|secret|token|api[_-]?key|https?://|/Users/|postgresql(\+asyncpg)?://[^<…]" WORK-010-hub-db.md
```

걸린 줄 1 — :339(검사 명령의 정규식 자체 · 값 아님). 접속 값 파일 경로 · DB 이름 0 · 사용자 홈 경로 0 · 127.0.0.1 밖 주소 0. 문서에는 표 · 칸 이름 · 셈 · 해시 앞뒤 8자뿐이다(Procedure Hub 데이터는 11-17 결정으로 이 검사에 걸지 않았다).
