# WORK-001 WP3 검수 리포트 — 1층 적재 스크립트

- 검수자: consult-analysis `reviewer` (read-only)
- 날짜: 2026-11-16
- 대조 기준: SPEC-001 0.2.0 (accepted) · WORK-001 WP3 ①~⑦ · 수용 기준 1~9 · DEC-001 D-01 ~ D-15
- 대상: `scripts/load_layer1.py` (495줄) · `scripts/verify_layer1.py` (453줄) · `scripts/tests/test_load_layer1.py` (348줄) · `data/layer1.sqlite`
- 이 리포트에는 고객 이름 · 본문 · 폴더명 · 계정명을 쓰지 않는다(D-10). 수치와 구조만.

## 판정: **PASS** (FAIL 0 · WARN 3 · INFO 3)

수용 기준 1 ~ 9 전부 충족. WARN 은 이번 원본에는 해당이 없는(0건) 경계 경로다 — 2층 착수를 막지 않는다.

---

## 1. 직접 돌린 명령 · 결과

스크래치 경로 = 세션 스크래치(리포 밖). 리포의 `data/layer1.sqlite` 는 읽기만 했다.

| # | 명령 | 결과 |
|---|---|---|
| 1 | `python3 -I scripts/load_layer1.py --source reference/2026-11-16-linky-data --db <스크래치>/l1.sqlite` | 종료 0 · stderr 0바이트 · conversation 511/1405/1916 · customer 510/1405/1915 · message 7094/21612/28706 · attachment 699/2762/3461 · reaction 123/236/359 (IG/FB/합) |
| 2 | `python3 -I scripts/verify_layer1.py --source … --db <스크래치>/l1.sqlite` | 종료 0 · **칸 274개 · 일치 274 · 불일치 0** · stderr 0바이트 |
| 3 | 같은 명령으로 두 번째 DB `<스크래치>/l1b.sqlite` 적재 | 종료 0 |
| 4 | 세 DB(스크래치 2개 + 리포 `data/layer1.sqlite`) 비교 | 테이블별 행 수 · min/max id **전부 같음**(5 테이블 모두 1 ~ 행 수) · `message_id ↔ (conversation_id, source_idx)` 해시 같음 · **`iterdump()` 전체 해시까지 같음** · `sqlite_master` 같음 |
| 5 | 원본 폴더 적재 전/후 | 파일 5,288 → 5,288 · 총 1,878,881,336 바이트 → 같음 · 스크립트보다 새로 바뀐 파일 0 |
| 6 | `python3 -m unittest discover -s tests -v` (scripts/ 에서) | **28 tests OK** (0.20s) |
| 7 | 음성 시험 — 스크래치 DB 복사본에서 `is_owner = 0` 메시지 1건의 `customer_id` 를 NULL 로 바꾼 뒤 verify | 종료 **1** · M-05 IG · 합 두 칸 불일치(272/274) → verify 가 실제로 DB 를 읽어 잡는다 |
| 8 | 행 단위 교차 대조(검수자가 따로 짠 스크립트 · 원본 재읽기 + 복원) — 1,916방 · 28,706 메시지의 `title` · `thread_path` · `source_idx` · `sender_name` · `timestamp_ms` · `content` · `call_duration` · `share.*` 5칸 · 첨부(kind · item_idx · uri · creation_timestamp) · 반응(item_idx · actor · reaction) | **불일치 0** |

---

## 2. 항목별 결과

### ① 스키마 = SPEC §2 — PASS

DB `sqlite_master` · `PRAGMA table_info / foreign_key_list / index_list` 로 직접 대조(`load_layer1.py:272-336`).

| 테이블 | 칸 · 순서 · 타입 · NOT NULL | PK | UNIQUE | FK | CHECK |
|---|---|---|---|---|---|
| conversation | 12칸 §2.1 과 같음 · NULL 허용 = `is_pending` · `joinable_mode` · `joinable_link` 만 | `conversation_id` | (`channel`,`thread_path`) · `source_file` | — | `channel` 2값 · `box` 3값 |
| customer | 4칸 §2.2 같음 | `customer_id` | (`conversation_id`,`participant_seq`) | → conversation | — |
| message | 18칸 §2.3 같음 · NULL 허용 = `customer_id` · `content` · `call_duration` · `share_*` 5 | `message_id` | (`conversation_id`,`source_idx`) · (`conversation_id`,`seq`) | → conversation · → customer | — |
| attachment | 7칸 §2.4 같음 · NULL 허용 = `created_at_s` · `created_at` | `attachment_id` | (`message_id`,`kind`,`item_idx`) | → message | `kind` 6값 |
| reaction | 6칸 §2.5 같음 | `reaction_id` | (`message_id`,`item_idx`) | → message | — |

- 테이블 정확히 다섯 · 뷰 0 · 트리거 0 (수용 기준 9 · D-02 · D-12).
- `PRAGMA foreign_keys = ON` 으로 적재(`load_layer1.py:423`) · 적재 뒤 `foreign_key_check` 0건(`:431`) · 검수자 재확인도 0건.
- `uri` 에 UNIQUE 없음(SPEC §9.4 대로).

### ② 원본 키 43개 전부 처분 · 모르는 키는 G-1 — PASS

- 코드 대응표(`load_layer1.py:57-86` `MESSAGE_SPEC` · `ROOM_SPEC`)에서 키 경로를 뽑으면 **43개**, 원본 1,916방에서 실제로 나오는 키 경로도 **43개**, 차집합 양쪽 0 (SPEC §3.6).
- `walk()` 의 객체 분기(`:122-137`)가 모든 키를 대응표와 대조해 없는 키면 G-1(`:126-128`). 통과시키는 `else` 없음 — 미지의 스펙 꼴은 `AssertionError`(`:138`).
- `build_rows()` 의 `.get()`(`:359` · `:364-365` · `:387` · `:391` · `:393` · `:400` · `:405`)은 전부 `walk()` 검사를 통과한 뒤의 **선택 키 꺼내기**다 — 버려지는 키가 아니다(대응표가 그 키를 이미 칸에 매핑). 조용히 버리는 경로 없음.
- 버림 2개(`magic_words` · `sticker.ai_stickers`)는 `empty_list` 꼴로 비어 있지 않으면 G-9(`:112-117`).

### ③ G-1 ~ G-12 전부 · 우리 계정 채널별 · 계정명 코드에 없음 — PASS

| 규칙 | 코드 | 시험(실제로 그 조건을 만들어 `L.load` 가 그 규칙 번호로 멈추는지 확인) |
|---|---|---|
| G-1 | `:126-128` | `test_g1_unknown_message_key` · `_nested_key` · `_gifs_creation_timestamp` · `_unknown_room_key` |
| G-2 | `:99-124` · `:132-134` | `test_g2_share_is_list` · `_sticker_is_list` · `_timestamp_is_string` |
| G-3 | `:89-94` | `test_g3_restore_fails`(U+0100) · `test_g3_invalid_utf8`(단독 0xFF) |
| G-4 | `:200-207` · `:346-351` | `test_g4_thread_path_mismatch` · `_loose_wrong_box` · `_duplicate_thread_path` |
| G-5 | `:174-177` | `test_g5_two_files` · `test_g5_no_file` |
| G-6 | `:232-252` | `test_g6_no_common_owner` · `test_g6_owner_not_top_sender` |
| G-7 | `:214-221` · `:383-386` | `test_g7_sender_not_participant` · `_actor_not_participant` |
| G-8 | `:223-227` | `test_g8_not_descending` |
| G-9 | `:115-116` | `test_g9_magic_words` · `test_g9_ai_stickers` |
| G-10 | `:195-198` | `test_g10_empty_share` |
| G-11 | `:209-212` | `test_g11_duplicate_participant` |
| G-12 | `:152-161` | `test_g12_unknown_box` · `test_g12_missing_root` |

- 모든 Stops 시험(`test_load_layer1.py:202-223`)이 ⓐ 예외의 규칙 번호 일치 ⓑ `main` 종료 코드 ≠ 0 ⓒ stderr 에 규칙 번호 ⓓ 출력에 자리표시 고객명 없음 ⓔ 이전 `<db>` 바이트 그대로 ⓕ `.tmp` 남지 않음 — 여섯 가지를 함께 본다(§6.2 바꿔치기까지 시험됨).
- 우리 계정은 채널별로 「모든 방 공통 이름 정확히 1개 + 채널 최다 발신자와 같음」(`:232-252` · SPEC §4.3). 계정명 리터럴은 코드 · 시험에 없다(⑥ grep 참고). 자리(`participants[]` 순서)로 판별하지 않음.

### ④ `verify_layer1.py` 독립성 — PASS

- `import` 는 `argparse · datetime · json · os · sqlite3 · statistics · sys` 뿐(`verify_layer1.py:11-17`). `load_layer1` 을 불러 쓰지 않는다(파일 안 `load_layer1` 문자열은 주석 `:6` 하나).
- 기준값은 `LINES`(`:282-398`)에 SPEC §7 숫자 리터럴로 박혀 있고 DB 에서 베끼지 않는다. 검수자가 §7 표 전 줄과 대조 — 값 다름 0. 원본 재집계는 `normalize_source()`(`:99-154`)가 원본을 따로 읽고 따로 복원한다.
- 판정은 `기준 == 원본 재집계 == DB` 세 값 모두(`:442`). E-04 의 DB 칸만 「—」(원본에서만 셀 수 있는 값 · `:438-440`).
- §7 의 합쳐 쓴 줄(C-07 · C-08 괄호 조건 · M-05 「전부 NULL 아님」 · R-02 「메시지당 1개」 · A-13 「= 행 수」)을 하위 줄로 풀어 함께 본다 — 274칸.

### ⑤ WP2 재실행 · 재현성 — PASS

§1 표 1 ~ 4. 274/274 일치 · 종료 0. 리포 DB 와 스크래치 DB 2개가 덤프 해시까지 같다(수용 기준 6).

### ⑥ 고객 정보 0 — PASS

방법: 원본 두 채널의 `participants[].name` 전체(1,868종 · 우리 계정 2 포함) · 방 폴더명 · 폴더 밖 JSON 파일명 · `thread_path` 뒤 마디(1,917종)를 **메모리에만** 올리고, 아래 파일 본문과 부분 문자열 대조.

| 대상 | 4자 이상 일치 | 3자 이하 일치(오탐) |
|---|---|---|
| `load_layer1.py` | 0 | 5 — 전부 1 ~ 2자(영문 1자 3 · 영문 2자 1 · 한글 1자 1) |
| `verify_layer1.py` | 0 | 5 — 같은 성격 |
| `test_load_layer1.py` | 0 | 4 — 같은 성격 |
| 적재 출력(stdout · stderr · 두 번째 적재) | 0 | 1 — 영문 1자 |
| 대조 출력(stdout · stderr) | 0 | 3 — 영문 1자 2 · 한글 1자 1(표 머리 「합」 같은 일반 글자) |

- 3자 이하 일치는 전부 1 ~ 2자짜리 표시 이름이 코드 · 표 머리의 일반 글자와 우연히 겹친 것이다 — 오탐으로 분류. 보관함 이름(`inbox` 등)은 대조 목록에서 뺐다(SPEC §1 의 구조 이름).
- 출력은 건수 · 규칙 번호 · 채널 · 보관함 · 방 순번만(`load_layer1.py:173` · `:485-489` · `verify_layer1.py:422-424`). 예기치 않은 예외도 종류 이름만 찍는다.
- 시험은 `<고객N>` · `<우리IG>` 자리표시 + `example.invalid` 만 쓴다. 원본 복사 없음.
- `data/` 는 `.gitignore:151` 로 무시 · `git status --ignored` 에 `!!` 로만 보임(수용 기준 5).

### ⑦ 2층 값이 1층에 없다 — PASS

언어 · 국적 · 문의 유형 · 단계 · 자동응답 칸 0 · 뷰 0 · 트리거 0 · SPEC §2 밖 칸 0 (수용 기준 8 · D-01 · D-05).

### 추가 확인

| 항목 | 결과 |
|---|---|
| 대체 키 순서 §4.5 | `conversation_id` = (`channel`,`thread_path`) 바이트 오름차순 전 행 일치 · FB 1 ~ 1,405 · IG 1,406 ~ 1,916(표본: 1 = FB `filtered_threads` · 1,405 = FB `inbox` · 1,406 = IG `inbox` · 1,916 = IG `message_requests`) · customer (conv, participant_seq) · message (conv, seq) · attachment (message, 종류 순서 photos→sticker, item_idx) · reaction (message, item_idx) — 전 행 정렬 일치 |
| `seq` 규칙 §4.4 | `seq ≠ 방 메시지 수 − source_idx` 0행 · `seq` 증가에 시각 역행 0 |
| 시각 §5.2 | `sent_at` 형식 위반 0 · SQLite 로 다시 만든 값과 다름 0 · `created_at` 형식 위반 0 |
| 고객 문의 연결(⑩) | `is_owner = 0` 인데 `customer_id` NULL **0** / 8,726 · `is_owner = 1` 인데 NULL 아님 0 · `customer.name ≠ sender_name` 또는 다른 방 customer 를 가리킴 0 · `is_owner` ≠ (`sender_name = owner_name`) 0 · 반응 `is_owner` 불일치 0 |
| `sticker` | 115행 전부 `item_idx = 0` |
| 원본 쓰기 · 외부 패키지 | 원본 파일 수 · 크기 · mtime 변화 0 · `import` 전부 표준 라이브러리(수용 기준 2 · 7) |

---

## 3. 지적

### WARN

| # | 위치 | 내용 | 근거 | 권고 |
|---|---|---|---|---|
| W-1 | `load_layer1.py:180` | 보관함 바로 아래의 **폴더도 `.json` 도 아닌 보통 파일**(숨김 아님)은 아무 규칙 없이 건너뛴다. 이번 원본엔 0건이지만, 모르는 꼴을 조용히 지나가는 유일한 자리다 | SPEC §4.1 은 「폴더」 · 「`*.json`」 두 꼴만 정의 · §1 은 숨김 파일만 무시 · WORK 수용 기준 3 「조용히 버리는 경로가 없다」 | 멈춤(G-12 또는 G-5 로 분류)으로 바꾸거나, SPEC 에 「무시」를 명시. SPEC 해석이 필요한 자리라 코디네이터 판단 |
| W-2 | `load_layer1.py:191-192` · `:487-489` | 원본 파일에 비 ASCII 바이트가 있거나 JSON 이 깨지면 G-번호 없이 「예기치 않은 오류」(종료 2)로 멈춘다. 멈추고 DB 를 남기지 않는 것은 맞지만, §5.4 끝줄의 「채널 · 보관함 · 몇 번째 방」 위치가 안 찍힌다 | SPEC §5.1(원본 바이트 전부 ASCII 전제) · §5.4 끝줄 | 읽기 실패를 `Stop(…, where)` 로 감싸 위치를 남긴다(규칙 번호는 G-3 또는 새 번호 — SPEC 판단) |
| W-3 | `test_load_layer1.py` | 시험이 안 닿는 분기 — ⓐ G-6 의 최다 발신자 동률(`load_layer1.py:249` 두 번째 조건) ⓑ G-6 「채널에 방 0개」(`:237-238`). (`stickers_used/` · 메시지 루트 바로 아래 JSON 을 방으로 안 읽는 경로 `:156-159` 는 픽스처 `test_load_layer1.py:118-121` 로 매 시험 지나간다 — 닿음) | WORK WP3 ③ (G 전부 · 시험이 각 규칙을 실제로 건드림 — 규칙 단위로는 전부 충족, 분기 단위 누락) | 두 경우 시험 추가 권장 |

### INFO

| # | 위치 | 내용 |
|---|---|---|
| I-1 | `verify_layer1.py:69-70` | 메시지 루트가 없으면 조용히 건너뛴다. 대조 스크립트라 건수 불일치로 반드시 드러나므로 문제는 아니다 |
| I-2 | `verify_layer1.py` 전체 | §7 은 집계 대조라 값 단위(본문 · 이름 등) 동등성은 보지 않는다 — 검수자가 따로 행 단위 교차 대조를 돌려 28,706건 불일치 0 을 확인했다(§1 표 8). SPEC 범위 밖이라 지적 아님 |
| I-3 | `scripts/__pycache__/` · `scripts/tests/__pycache__/` | 시험을 돌리면 리포 안에 생긴다(검수 전부터 있었음 · 검수자 시험 실행으로 갱신됨). `.gitignore:24` 로 무시돼 커밋에는 안 들어간다 |

### FAIL

없음.

---

## 4. 수용 기준 대조

| # | 기준 | 결과 |
|---|---|---|
| 1 | §7 전 줄 · IG/FB/합 각 칸 일치 | ✅ 274/274 |
| 2 | 표준 라이브러리만 · `python3 -I` | ✅ |
| 3 | 담을 칸 없는 키 0 · 조용히 버림 없음 | ✅ (키 43/43 · W-1 은 키가 아닌 파일 꼴) |
| 4 | 출력에 고객 정보 0 | ✅ (오탐 1 ~ 2자만) |
| 5 | 레포에 고객 정보 0 · `data/` gitignore | ✅ |
| 6 | 다시 돌려도 같다 | ✅ 덤프 해시 동일 |
| 7 | 원본을 건드리지 않는다 | ✅ |
| 8 | 판단이 섞이지 않았다 | ✅ |
| 9 | 테이블 다섯 · `channel` 2값 · NULL 0 | ✅ FB 1,405 · IG 511 |
