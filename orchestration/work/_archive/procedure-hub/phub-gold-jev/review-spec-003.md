# SPEC-003 0.1.0 검수 — 허브 silver · gold 로컬 DB 화

검수: reviewer_doc(read-only) · 2026-11-17 · 대상 `SPEC-003-hub-gold-db.md` 0.1.0(687줄) · 허브 `phub-gold-jev` HEAD `85c28af`
지시: `spec-db-review-instructions.md` 1 ~ 8 · 기준: `spec-db-instructions.md` 「정해진 것」 · `_RESUME.md` §2 11-17 행

## 판정

**PASS — FAIL 0 · WARN 4 · NOTE 8.**
**U-1 · U-2 가 정해지면 WORK 진행 가능.** WARN 4 는 스펙을 다시 돌릴 거리가 아니라 WORK 에 한 줄씩 받아 적으면 닫힌다(W-1 만 코디가 둘 중 하나를 골라야 한다).

- 재셈은 전부 스펙과 같다(다른 수 0 — §2).
- 「정해진 것」 D-0 ~ D-8 · 옛 스키마 금지 · 기존 167 불가침 위반 0.
- 돌려 보지 않은 것: DB · docker · 서버 · alembic · pytest(전부 읽기와 CSV 셈만). `.env` 는 열지 않았다.

## 1. 지적

| # | 문서:줄 | 심각도 | 무엇 | 근거 | 고칠 방향 |
|---|---|---|---|---|---|
| W-1 | SPEC-003:595 · 644 ↔ 87 · 469 · 544 · 562 | WARN | §8 이 `health` 에 새 필드(`repository` · `db_build{built_at, loader_version}`)를 싣겠다고 적었는데, §1-3 은 「도구 9 · 응답 필드 그대로」 이고 §5-4 · DT10 · DE5 는 두 판 JSON 이 `build.loaded_at`(+ `load_ms`) 만 빼고 같다고 한다. `repository` 값은 판마다 달라 두 계약이 서로 깨진다. 본문 §5 에는 이 필드 정의가 없다(§8 과 O-7 에만 있다) | `service.py:152-166`(지금 health 필드) | 둘 중 하나 — (a) 이번 판에는 새 필드를 안 넣는다(계약 불변 유지 · 추천: 「같은 응답」 이 완료 조건이다) (b) 넣으려면 §5 에 필드를 정의하고 §5-4 제외 목록 · DT10 · DE5 · SPEC-001 부록 A 대조 시험에 더한다. (b) 는 도구 계약 변경이라 코디 결정으로 올린다 |
| W-2 | SPEC-003:354-355 · 418 · 493 · 558 | WARN | `DATABASE_URL` 을 **어느 설정이 읽는지**가 안 닫혔다. alembic 은 `envs/.env`(`app/core/config.py:41,47` → `alembic/env.py:18`)에서, gold 설정은 `envs/.env.gold`(`modules/gold/config.py:26`)에서 읽는다. §4-1 은 적재기 env 를 「지금 gold 설정과 같다 — `.env.gold`」 라고 하면서 `DATABASE_URL` 은 「alembic 이 읽는 그 값」 이라 한다 — 파일이 둘이다. `db` 판 허브(§5-1)가 어디서 읽는지도 없다. 프로세스 env 를 빼먹으면 `alembic upgrade head` · DE1 의 `downgrade -1` 이 `envs/.env` 에 적힌 DB 로 간다(그 값이 로컬인지는 확인 안 됨 — `.env` 를 열지 않았다). 로컬이 아니면 D-0(로컬까지) · N-5 를 넘는다 | 왼쪽 파일:줄 · `gold_main` · `modules/gold` 에 `DATABASE_URL` 참조 0(재확인) | WORK 에 한 줄씩: ① 적재기 · `db` 판이 `DATABASE_URL` 을 읽는 자리 하나를 명시 ② §6 · DE1 의 alembic 명령은 전부 프로세스 env 를 붙인 꼴로만 적는다(§6-1 ③ 은 이미 그렇다 · DE1 에는 없다) ③ 적재기처럼 alembic 을 돌리기 전에도 접속 대상을 눈으로 확인하는 절차 |
| W-3 | SPEC-003:371 · 388 · 404-407 | WARN | 적재 CLI 계약 구멍 셋. ① ⑤ 단계의 **DB 접속 실패**에 exit code 가 없다(2 = V1 ~ V9 · L1 / 3 = L2 ~ L6 — 접속 실패는 어느 쪽에도 없다). ② V1 「필수 env」 목록이 없어 **dry-run 에서 `DATABASE_URL` 이 필수인지** 안 정해진다(「DB 에 접속하지 않는다」 · DT7 과 맞추려면 dry-run 은 없어도 통과여야 한다). ③ 검사 · 해시 · 적재가 **한 번 읽은 같은 바이트**로 도는지 적혀 있지 않다 — 파일을 두 번 읽으면 그 사이 바뀐 파일의 해시와 실린 행이 어긋난다 | `inputs.py:111-115`(지금은 `data` 한 번 읽어 해시 · 파싱에 같이 쓴다) | WORK 에 한 줄씩: ① 접속 실패 = exit 2(쓴 것 0 이다) 또는 3 중 하나로 ② 필수 env 를 dry-run / 적재로 나눠 열거 ③ 「파일은 한 번 읽는다」 |
| W-4 | SPEC-003:100 · 253 · 338 · 345 · 558 · 643 | WARN | WORK 첫 WP 확인 목록(O-6)에 넣을 것이 더 있다. ① 지연 FK — alembic 1.18.4 는 FK 의 `deferrable` · `initially` 를 세 상태 값으로 묶어 비교한다(`alembic/ddl/_autogen.py:278-304`). **모델과 마이그레이션 양쪽에 같은 옵션**을 주면 맞고 한쪽만 주면 `alembic check` 가 깨진다(읽기만 · 돌리지 않음). ② `load_seq` 를 PK 로 쓰는 3표(`g_evidence` · `s_alias` · `s_source_ref`)는 정수 단일 PK 라 SQLAlchemy 가 자동 증가로 본다 — PostgreSQL 에 시퀀스 3 이 생긴다. `autoincrement=False` 를 양쪽에(R4 「CSV 에 없는 것은 `load_seq` 하나」). ③ 기존 시험 28 파일이 `create_all` 을 테스트마다 돈다(`scope="function"` — `tests/test_synergy_models.py:16-22`). 테이블 74 · 인덱스 30 · FK 82 가 매번 더 만들어지므로 pytest 시간을 앞뒤로 잰다(CI 제한 15분 — `backend-test.yml:33`). ④ DE1 「`public` 테이블 241」 은 `alembic_version` 을 세면 242 다 — 세는 식을 적는다 | 왼쪽 파일:줄 | WORK 첫 WP 에 네 줄 |
| N-1 | SPEC-003:235 · 444 · 456 | NOTE | 「이름순」 은 파이썬 글자 순(`inputs.py:66,121` 의 `sorted`)이다. `files[]` 16줄 순서 · F4 의 해시 재셈 · `ledger_ids_by_code` 의 id 순을 DB `ORDER BY` 로 하면 DB 정렬 규칙을 탄다(R4 가 키 정렬에 대해 스스로 적은 위험과 같다). SQLite 시험은 못 잡고 DE5 에서만 드러난다. 지금 16 이름에서 실제로 갈리는지는 확인 안 함 | `inputs.py:66,121,189` | 「정렬은 파이썬에서 · `combined_hash` 를 그대로 쓴다」 한 줄 |
| N-2 | SPEC-003:444 · 468 | NOTE | `LoadedInputs.expected_hash_checked` 가 P9 · §5-4 「입력」 목록에 없다. `health` 응답에 나가는 값이다 | `inputs.py:62` · `service.py:157` | DB 판도 env 유무로 정한다고 한 줄 · DT9 목록에 더함 |
| N-3 | SPEC-003:354 | NOTE | 적재기는 `GOLD_SOURCE_REF_PATH` · `GOLD_HIERARCHY_DIR` 없이 `GOLD_SILVER_DIR` 하나로 읽는다. `aux_hash` 는 **파일 이름**을 넣어 세므로(`inputs.py:128,177-178`) CSV 판의 두 env 가 같은 폴더의 같은 파일을 가리킬 때만 두 판 해시가 같다. 지금 로컬은 그렇다 | 재셈 `aux_hash` 재현 | 대조 전제로 한 줄(DE5 가 잡는다) |
| N-4 | SPEC-003:223 · 371-379 | NOTE | `medallion_build.file_name` 이 PK 인데 세 원천 사이 이름 겹침 검사가 V1 ~ V9 에 없다. 겹치면 L4 에서 터져 exit 3 이 된다(입력 문제인데 2 가 아니다). 지금 겹침 0(재셈 74 / 74) | 재셈 | V 에 한 줄 |
| N-5 | SPEC-003:444 | NOTE | `ledger_rows_with_code` = 서로 다른 `lck_id` 수는 원장 확인 목록의 `id` 가 유일 · 빈칸 0 일 때만 CSV 판(행 수로 센다 — `inputs.py:170-171`)과 같다. 지금은 그렇다(325 유일 · 빈칸 0) | 재셈 | 적재기 검사에 「id 유일 · 빈칸 0」 한 줄 |
| N-6 | SPEC-003:253 · 389 · 643 | NOTE | 지연 FK 가 안 될 때의 대안이 「의존 순서대로 싣기」 만 적혀 있다 — 지우기(L2)도 역순이어야 한다 | — | O-6 대안에 한 줄 |
| N-7 | SPEC-003:417-421 · 686 | NOTE | 기본값 `csv` 는 본문이 정했는데 변경 기록의 「이 워커가 제안으로 정한 것」 목록에 없다. 근거(지금 동작 · 대조 기준)는 타당하고 뒤집기는 N-6 에 있다 — 사용자 결정으로 올릴 것은 아니다 | 지시서 할 것 4 | 변경 기록 또는 O-7 에 한 줄 |
| N-8 | SPEC-003:373 | NOTE | 계약 밖 CSV 처리가 폴더마다 다르다(silver = exit 2 · gold = `hash_only`). 이유는 본문에 있고 gold 쪽은 지금 동작 그대로다 | `inputs.py:117-120` | 그대로 둬도 된다 |

## 2. 지시 「할 것」 1 ~ 8 → 문서:줄

| # | 지시 | SPEC-003 | 닫힘 |
|---|---|---|---|
| 1 | 표 → 테이블 대응(74) · PK · 키 없는 표 3 · silver FK 80 · 다형 참조 · `order` · 인덱스 | §2 L90-303(R5 L100 · §2-2 L109-126 · §2-3 L137-196 · §2-6 L243-254 · §2-7 L260-270 · R9 L104 · §2-8 L276-291) | ○ |
| 2 | 마이그레이션 · 모델 자리 · SQLite `create_all` · `alembic check` | §3 L305-345(C1 ~ C7 L337-343) | ○(W-4) |
| 3 | 적재 CLI — env · 검사 · 한 트랜잭션 · 실패 때 그대로 · exit code · dry-run | §4 L347-409 | ○(W-3) |
| 4 | repository — DB 판 · 고르는 env · 시작 때 읽기 · 두 판 대조 | §5 L411-470 | ○(W-1 · W-2) |
| 5 | 로컬 실행 — PostgreSQL · 포트 · `gold_main` DB 판 명령 | §6 L472-525 | ○ |
| 6 | 시험 기준 · 완료 조건(18105 DB 판 · 앱 37 키 (나)) | §7 L527-577(DT 15 · DE 8 · 완료 조건 L572-575) | ○ |
| 7 | 「다음 범위」 표 | §9 L603-619(N-1 ~ N-11) | ○ |
| 8 | version · 변경 기록 · 열린 것 · WORK 전 사용자 결정 | L8 · L681-687 · §10-2 L632-646 · §10-1 L623-630 | ○ |

「정해진 것」 대조 — 위반 0.

| 정해진 것 | 본문 | 결과 |
|---|---|---|
| 로컬까지 · stg 는 범위 밖 | L64 · L79-85 · §9 | ○ |
| D-1 silver 57 + gold 15 + 원장 확인 · 읽는 범위 그대로 · 원장 JSON 안 올림 | L65 · L203 · P5 L440 | ○ |
| D-2 `public` · `g_*` · `s_*` · 63자 확인 | R1 L96 · R8 L103 | ○(재셈 최대 63) |
| D-3 전부 문자열 · 빈칸 규칙 하나 | R2 · R3 L97-98 · §2-7 | ○(U-1) |
| D-4 판 하나 · 한 트랜잭션 교체 · 빌드 기록 표 1 · 원문 통째 0 | §2-5 L219-239 · §4-4 L388-398 | ○ |
| D-5 적재 CLI · 경로 env · CSV 커밋 금지 | §4-1 L353-357 | ○ |
| D-6 시작 때 DB → 같은 메모리 색인 · Protocol 동기 · 해시는 빌드 기록 값 | P1 ~ P10 L436-445 | ○ |
| D-8 id · 코드 쌍 표 하나 | §2-4 L207-215 | ○ |
| 옛 스키마 · revision id 재사용 금지 | §3-2 L324-326 · L330 | ○ |
| 기존 167 불가침 · FK 0 | R10 L105 · L249 · L389 | ○ |

## 3. 재셈(스펙과 다른 수 0)

`$SM` 의 실제 CSV · `silver-schema.json` 을 `python3`(표준 `csv` · `json` · `hashlib` · `utf-8-sig` · `newline=''`)로 다시 셌다. 스크립트는 세션 임시 폴더에만 있다.

| 무엇 | 스펙 | 재셈 | 세는 식 |
|---|---|---|---|
| 표 대응 72 + 2 | 74 · 빠짐 0 | **같음** | §2-2 · §2-3 표의 줄을 정규식으로 뽑아 표마다 행 · 칸 · PK · FK 목록 · 다형 칸을 실제 파일 · 스키마와 대조 — 72 / 72 일치 · 어긋남 0. 층 23 · 6 · 20 · 8 |
| gold | 15표 · 62,244행 · 278칸 | 같음 | 표별 행 · 칸도 §2-2 와 전부 같음 · 헤더 = `GOLD_HEADERS` 15 / 15 |
| silver | 57표 · 66,936행 · 387칸 | 같음 | 스키마 57 = 파일 57 · 헤더 어긋남 0 |
| 합 | 129,527행 · 칸 749 | 같음 | 62,244 + 66,936 + 273 + 74 · 665 + 72 + 2 + 10 |
| silver FK | 80칸 · 깨짐 0 · 자기 참조 11 · 대상 전부 키 | 같음 | 스키마 `columns[].fk` 가 있는 칸 |
| 빈칸 든 FK 칸 | 35칸 · 빈 값 12,968 | 같음 | 80칸마다 `''` 인 행 수 > 0 인 칸 수 · 그 합 |
| 키 없는 표 | 3(`g_evidence` · `alias` · `source_ref`) | 같음 | 스키마 `key` 없음 2 + gold 1 |
| 유일 제약 3 | 739 / 739 · 27,740 / 27,740 · 980 / 980 · 빈칸 0 | 같음 | 묶음 칸의 서로 다른 조합 수 |
| `g_edge` 끝 | 깨짐 0 | 같음 | `src` · `dst` ∉ `g_node.node_id` |
| FK 이름 길이 | 최대 63(1개) · 중복 0 | 같음 | `fk_s_<표>_<칸>_s_<대상>` |
| 인덱스 | 직접 지은 30(gold 28 + 2) | 같음 | §2-2 표 줄별 합 2+2+0+4+2+2+2+1+2+3+3+3+0+2+0 · `VALUE_INDEX` 12(`memory.py:20-27`)와 짝 맞음 |
| 다형 칸 · `order` | silver 15칸(14표) · `order` 2표 | 같음 | `*_table` 칸 · 헤더에 `order` |
| 글자 | 1,099,733칸 · 빈칸 308,658 · NUL 0 · 줄바꿈 0 | 같음 | 72표 전 칸 |
| `gold_hash` | `8accbb21…f6228c` | **재현** | gold 폴더 `*.csv` 16(15 + `questions.csv`) · `inputs.py:64-67` 식 |
| `aux_hash` | `6435fe41…1803a3` | **재현** | `source_ref` + `concern` · `adverse` · `condition` · `concern_site` + 원장 확인 목록 6 파일 |
| silver 57 해시 | `91237618…9c9254` | 재현 | 같은 식 |
| 원장 확인 | 325행 · 16칸 · 코드 든 행 251 · 쌍 273 · 코드 218 | 같음 | `inputs.py:37-38` 식 · 세 칸 이음 |
| 빌드 기록 | 74행(16 + 57 + 1) · 이름 겹침 0 | 같음 | 파일 이름 74 / 74 유일 |
| 기존 테이블 | 167 · 새 접두어와 겹침 0 | 같음 | `grep __tablename__ backend/app/model` 167 · `s_` · `g_` · `medallion` · `gold_` · `silver_` 로 시작 0 |
| `create_all` | 28 | 같음 | `grep -rn create_all backend/tests` 28줄 · 28 파일 |
| 옛 브랜치 | revision 3 · 테이블 `gold_*` 8 · `graph_*` 6 | 같음 | `git ls-tree origin/kknaksss/phub-recommend backend/alembic/versions/` · `git show` 의 `create_table` 14 — 새 74 이름과 겹침 0 |
| revision id | `b202611170001` | 겹침 0 | 이 레포의 로컬 · 원격 참조 전부의 versions 파일 이름에 `b20261117` 0(fetch 안 함 — 지금 받아 둔 참조 기준) |
| 포트 | 18432 · 18107 비어 있음 | 같음 | `lsof` — 듣는 18xxx = 18105 · 18106 · 18210 · 18220 · 54xx 0 |

## 4. DB 판 = CSV 판(지시 3)

`inputs.py` 가 읽는 것 전부(197줄 전수)와 DB 판의 자리.

| `inputs.py` 가 읽는 것 | 줄 | DB 판 | 닫힘 |
|---|---|---|---|
| gold 15표 전 칸 · 헤더 순서 대조 | 109-115 | `g_*` 15 · `load_seq` 순 · 헤더는 적재기 V5 | ○ |
| gold 폴더의 다른 CSV(해시만) | 117-120 | 빌드 기록 `hash_only` | ○ |
| `source_ref` 4칸 | 124-129 | `s_source_ref` · `load_seq` 순 | ○ |
| 계층 3표 `code` · `parent_code` | 132-146 | P5 두 칸만 | ○(순서는 결과에 안 쓰인다 — `memory.py:88` 이 자식을 정렬한다) |
| `concern_site` 3칸 | 149-156 | P5 | ○(`memory.py:93` 이 정렬한다) |
| 원장 확인 — id · 뽑은 코드 · 행 수 · 코드 든 행 수 | 159-175 | `medallion_ledger_check` + 빌드 기록 `file_rows` | ○(N-5) |
| 파일별 sha256 · 행 수 · `kind` · 순서 | 115 · 120-121 · 128 · 145 · 155 · 175 · 193 | P9 | ○(N-1 · N-3) |
| `gold_hash` · `aux_hash` | 177-178 | 빌드 기록 값 + F4 재셈 | ○ |
| `GOLD_EXPECTED_HASH` | 179-183 | F6 | ○ |
| `expected_hash_checked` | 62 · 195 | **적힌 곳 없음** | N-2 |

- 값 왕복 — R3(빈칸 → NULL → `''`) · L5 되읽기 · DT8 · DT13. CSV 의 빈칸 표기가 하나뿐이라 잃는 것이 없다는 주장은 맞다(72표 공백만 든 칸 · NUL 0 재확인).
- 행 순서 — R4 `load_seq` · P6. 키 있는 gold 14표가 지금 「파일 순서 = 키 오름차순」 인 것도 재확인했다.
- 해시 — 파일 바이트에서 나오므로 적재 때 값을 기록하고 허브가 F4 로 다시 센다. 실은 뒤 누가 SQL 로 행을 고치면 허브는 모른다(F5 는 행 수만) — O-8 에 이미 열려 있다.
- 도구 응답 동일 — DT10(합성) · DE6(실물) · DE7(앱 37). W-1 만 풀면 계약이 닫힌다.
- 메모리 색인으로 가는 길에서 **빠지는 입력은 `expected_hash_checked` 하나**다(N-2).

## 5. alembic · 모델 · 시험(지시 4)

- revision — `b202611170001` · `down_revision = b202610300001` 은 지금 헤드와 맞다(`…legacy_prod_documents.py:10-11`). 옛 브랜치의 `b202610300001`(`_gold_schema`)이 글자만 같은 문제는 L330 이 「새 빈 DB 에서만」 으로 막았다.
- CI — `alembic upgrade head` → `alembic check`(`backend-test.yml:66-70`) → pytest 는 SQLite(`:76-80`). C1 ~ C7 이 이 셋을 덮는다.
- 지연 FK(O-6) — 「WORK 첫 WP 에서 로컬 PostgreSQL 로 확인 · 어긋나면 지연 없이 의존 순서」 로 막혀 있다(L253 · L345 · L643 · DE1 L558). 더할 것은 W-4.
- SQLite — `Text` · `Integer` · 시각뿐이고 `schema=` 0 이라 `create_all` 이 깨질 타입은 없다(C3). `PRAGMA foreign_keys = ON` 을 켜는 시험이 있어도 테이블 만들기에는 영향이 없다.
- `test_gold_load.py:121` 의 `repo._m` 직접 참조는 L552 가 구현 확인 거리로 적었다.

## 6. 적재 CLI(지시 5)

- 한 트랜잭션 교체 — L2 ~ L6(L389-393). 커밋 전 되읽기 대조(L5)로 「실은 것 = 파일」 을 같은 트랜잭션 안에서 본다.
- 실패 때 그대로 — L395(롤백 · 옛 판 · 처음이면 빈 채). DT5 · DT6 · DE4 가 시험한다.
- exit code — 0 / 2 / 3(L405-407). 2 는 허브 전례(`scripts/import_legacy_corpus.py:13`)와 같다.
- dry-run — ① ~ ④ 만 · DB 접속 0(L404 · DT7).
- 구멍은 W-3 의 셋 · N-4.

## 7. 로컬 실행(지시 6)

- 포트 — 18432(PostgreSQL) · 18107(허브끼리 대조)은 금지 18210 · 18005 와 쓰는 중 18105 · 18220 · 18106 어디와도 안 겹친다. 지금 둘 다 비어 있다.
- 기존 167 을 건드리는 명령 0 — `docker run`(새 컨테이너 · 새 볼륨) · `alembic upgrade head`(새 빈 DB 에 167 + 74 를 만든다 — 데이터 0) · 적재기(새 74 만 지우고 싣는다 — L389) · `uvicorn`. DE1 의 `downgrade -1` 은 새 74 만 지운다(L327). **단 이 전부가 `DATABASE_URL` 이 새 로컬 DB 를 가리킬 때의 말이다 — W-2.**
- 띄우고 내리는 것은 코디(L474) — 워커 제약과 맞다.

## 8. U-1 · U-2 · 숨은 결정(지시 7)

| | 추천 | 결정 · 원칙과 맞나 |
|---|---|---|
| U-1 빈칸 = NULL + FK 82 | (a) | 맞다. D-3 은 「`''` 와 NULL 중 하나를 정해 적재기가 지킨다」 까지만 정했고 고르는 것이 열려 있었다. FK 80칸 중 35칸에 빈칸(12,968)이 있어 빈칸 규칙과 FK 가 한 묶음이라는 근거는 재셈으로 맞다. `g_edge` 2 는 지시서의 「80칸」 밖에서 더한 것인데 U-1 안에 밝혀 두었고 깨진 끝 0 이다. 기존 167 로 가는 FK 0 · gold → silver FK 0 이라 D-10 과 부딪히지 않는다 |
| U-2 Docker `postgres:16` · `127.0.0.1:18432` | (a) | 맞다. CI 와 같은 판이고 포트 제약을 지킨다. 코디가 띄운다 |

숨은 사용자 결정 — **0.** 다만 W-1 의 (b)(health 새 필드)를 고르면 도구 계약이 바뀌므로 그때는 코디 결정으로 올려야 한다. 기본값 `csv`(N-7) · silver 계약 밖 CSV = exit 2(N-8) · exit 3 · 이름들(O-7)은 구현 선에서 닫을 수 있다.

## 9. 인용 표본(20 · 틀림 0)

| 인용 | 결과 |
|---|---|
| `inputs.py:3` 「칸은 전부 문자열」 | ○ |
| `inputs.py:37-38` 접두어 9종 · 추출식 | ○ |
| `inputs.py:46` `FileRecord.kind` 넷 | ○ |
| `inputs.py:64-67` 해시 식 | ○ |
| `inputs.py:76-91` `_parse` 판정 | ○ |
| `inputs.py:113-114` 헤더 대조 | ○ |
| `inputs.py:117-120` `hash_only` | ○ |
| `inputs.py:169` 세 칸 이음 | ○ |
| `inputs.py:177-178` · `:179-183` | ○ |
| `memory.py:45 ~ 64` · `:67-77` · `:80-88` · `:104` · `:116-131` 색인 | ○(§2-8 표 전 줄) |
| `repository.py:40-77` Protocol 메서드 29 | ○(4 + 3 + 5 + 4 + 3 + 3 + 6 + 1) |
| `repository.py:83-87` · `:89-102` · `:91-92` | ○ |
| `service.py:34` `repository_factory` | ○ |
| `service.py:152-166` health | ○ |
| `core.py:100-106` · `:108-110` | ○ |
| `config.py:19,32-38` · `:25-29` | ○ |
| `model/base.py:8-14` 이름 규칙 | ○ |
| `alembic/env.py:18` · `:27-44` | ○(`include_schemas` 없음) |
| `…legacy_prod_documents.py:10-11` · `:23-24` | ○ |
| `backend-test.yml:37` · `:66-70` · `:72-74` · `:76-80` · `Dockerfile:27` · `import_legacy_corpus.py:13` · `core/config.py:53` · `test_gold_load.py:121` | ○ |

## 10. 공개 레포

```
grep -n -i -E "password=|passwd|secret|token|api[_-]?key|https?://|@<도메인>|/Users/|<회사 이름>|<IPv4>" SPEC-003-hub-gold-db.md   (127.0.0.1 제외)
```

걸린 줄 1 — L490 `POSTGRES_PASSWORD=<PASSWORD>`(자리 표시 · 값 아님). 비밀값 0 · 내부 호스트 / URL 0 · 실명 0 · 사용자 홈 경로 0. Procedure Hub 데이터 본문은 11-17 결정으로 이 검사에 걸지 않았다(문서에는 표 · 칸 이름 · 셈뿐이다).
