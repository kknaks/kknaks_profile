---
type: spec
id: SPEC-003
title: "허브 silver · gold 로컬 DB 화 — 테이블 74(gold 15 · silver 57 · 원장 확인 · 빌드 기록) · alembic 1 · 적재 CLI · DB 판 repository(시작 때 읽어 같은 메모리 색인) · 0.2.0 stg 판(gold 를 app.main 에 붙임 · 꺼진 채 기동 · 레포 데이터 폴더 · 적재기 이미지 · 일회성 적재 절차)"
status: draft
product: procedure-hub
feature: phub-gold-jev
version: 0.2.1
created_at: 2026-11-17
updated_at: 2026-11-18
tags:
  - product/procedure-hub
  - feature/phub-gold-jev
  - doc/spec
  - status/draft
links:
  decisions:
    - "orchestration/work/phub-gold-jev/_RESUME.md §2 (2026-11-18 0.2.1 근거 행 — 「SPEC-003 stg 검수 WARN 코디 답」(R-1 ~ R-4) · 「SPEC-003 0.2.0 정할 것 코디 답」(O-S1 ~ O-S3 · O-S5 · O-S6) · 「gold MCP 421 고침」 · 「stg 반입 완료」) · stg-runbook.md (실행 기록) · review-spec-003-stg.md · review-code-hub-stg.md · 허브 `d3d078c` (구현 결과가 정본)"
    - "orchestration/work/phub-gold-jev/_RESUME.md §2 (2026-11-17 맨 위 두 행 — 「DB 화 이번 목표 = 로컬 허브 DB 까지」 · 「채팅보다 DB 설계 먼저」)"
    - "orchestration/work/phub-gold-jev/_RESUME.md §2 (2026-11-16 — 「D2 저장 = DB 없이 … repository 층만 바꾸면 되게」 · 「stg 에 올린다 — 머지 · 배포 · stg 데이터 반입은 각각 별도 승인」 · 「검수 뒤 결정 4」 ② ③ · 「SPEC 0.5.2 사용자 결정」 U-4)"
    - "orchestration/work/phub-gold-jev/spec-db-instructions.md (「정해진 것」 D-1 ~ D-8 — 코디 기본값 · research-db 추천 그대로. 보조 근거 — 위 _RESUME §2 행을 코디가 풀어 적은 지시서)"
    - "orchestration/work/phub-gold-jev/_RESUME.md §2 (2026-11-18 — 「stg gold = app.main 에 붙임(S-4 (b)+(c))」 · 「stg 시드 = 일회성 적재」 · 「이번 판은 여기서 배포로 닫는다」 · 「배포 단계는 승인 없이 이어서 진행」) ← 0.2.0 §11"
    - "orchestration/work/phub-gold-jev/spec-003-stg-brief.md (0.2.0 발주서)"
  sources:
    - "orchestration/work/phub-gold-jev/research-stg-seed.md (0.2.0 — §1-1 ~ §1-7 · §2 반입 절차 초안 · §3 S-1 ~ S-7)"
    - "orchestration/work/phub-gold-jev/SPEC-007-image-data.md (적재기 V13 · 표 76 의 그림 2표)"
    - "PROCEDURE-HUB 워크트리 phub-gold-jev HEAD fdc155b (0.2.0 — backend/app/main.py · app/core/{app_factory,lifespan,app_builder}.py · app/gold_main.py · app/modules/gold/{config,db_inputs,medallion_load,errors}.py · app/router/{gold,health}.py · scripts/load_medallion.py · Dockerfile · .dockerignore · tests/{test_gold_rest,test_public_api_contract}.py · .github/workflows/backend-test.yml · docs/guides/deployment.md · docs/adr/0004-staging-runtime-configuration-and-cutover.md)"
    - "orchestration/work/phub-gold-jev/research-db.md (§0 ~ §7 — 사실 · 셈 · 파일:줄)"
    - "orchestration/work/phub-gold-jev/SPEC-001-hub-gold-mcp.md (0.6.0 — §1-3 · §2 · §3 · §3-1 · §4-8 · §7 · §8 · §9 · §10)"
    - "PROCEDURE-HUB 워크트리 phub-gold-jev (HEAD 85c28af · base release/v1.2.0 = 3750e4c) — backend/app/modules/gold/{repository,memory,inputs,headers,config,service,core,cursor}.py · backend/app/gold_main.py · backend/alembic/env.py · backend/app/model/{base,__init__,legacy_prod}.py · backend/app/core/{db,config}.py · backend/README.md · backend/pyproject.toml · .github/workflows/backend-test.yml · backend/scripts/import_legacy_corpus.py"
    - "orchestration/work/_archive/procedure-hub/phub-ledger-redesign/silver-model/ (gitignore · 로컬 — silver/*.csv 57 · gold/g_*.csv 15 · gold/questions.csv · notes/ledger-check-list.csv · drafts/silver-check/silver-schema.json)"
    - "para/areas/concept/cs/artifact-traceability.md"
  related:
    - "orchestration/work/phub-gold-jev/SPEC-001-hub-gold-mcp.md"
    - "orchestration/work/phub-gold-jev/SPEC-002-chat-eval.md"
---

# SPEC-003 — 허브 silver · gold 로컬 DB 화

경로 접두어: `$W` = 이 폴더 · `$H` = PROCEDURE-HUB 워크트리 `phub-gold-jev`(읽기만) · `$SM` = `orchestration/work/_archive/procedure-hub/phub-ledger-redesign/silver-model`(gitignore · 로컬).
「조사」 = `$W/research-db.md` · 「지시서」 = `$W/spec-db-instructions.md` · 「재셈」 = 이 워커가 `$SM` 의 실제 CSV 와 `silver-schema.json` 으로 다시 센 값(부록 B).
이 문서에는 표 · 칸 이름 · 코드 꼴 · 셈만 있다 — 회사 데이터 본문 · 비밀값 · 호스트 주소는 없다.

> **0.2.0 — §11 「stg 판」 을 더했다.** D-7(stg 진입점)을 닫고, 레포 데이터 폴더 · 적재기 이미지 포함 · stg 반입 절차 · 시험 몫을 정한다. §0 ~ §10 은 0.1.0(로컬 판) 본문이다 — 거기 적힌 **수 74 · 129,527 은 그 판의 수**이고, 지금 판(그림 2표를 더한 SPEC-007 · WORK-015 뒤)은 **표 76 · 130,446행**이다(§11-0). 본문 규칙(R1 ~ R10 · V · L · P · F)은 그대로다.

## 0. 요약

| 무엇 | 이 스펙이 정하는 것 |
|---|---|
| 목표 | **로컬 허브 DB 까지** — 로컬 PostgreSQL 에 silver 57 + gold 15 를 싣고, 허브 `gold_main` 을 DB 판으로 띄워 CSV 판과 **같은 응답**이 나오는 것 |
| 테이블 | 새 테이블 **74** = gold 15(`g_*`) + silver 57(`s_*`) + 원장 확인 1 + 빌드 기록 1 · 전부 `public` · 기존 167 은 건드리지 않고 FK 로 잇지 않는다 |
| 칸 | CSV 칸 하나 = 테이블 칸 하나(이름 · 순서 그대로) · 전부 문자열 · **빈칸 = NULL 하나로**(제안 — U-1) · 표마다 행 순서 칸 `load_seq` 하나만 더한다 |
| 관계 | FK **82** = silver 안 80 + `g_edge` → `g_node` 2(제안 — U-1) · 다형 참조(표 이름 칸 + 코드 칸)는 FK 없음 |
| 판 | 살아 있는 판 하나 · 한 트랜잭션 전체 교체 · 빌드 기록 표가 `gold_hash` · `aux_hash` · 파일별 sha256 · 행 수 · 적재 시각을 든다 |
| 적재 | 로컬 경로(env)의 CSV 묶음을 **적재 CLI** 가 읽어 싣는다 · 검사 실패면 DB 를 건드리지 않는다 · dry-run |
| repository | DB 판 = **시작 때 한 번** DB 에서 읽어 지금 메모리 색인을 그대로 세운다 · 요청은 DB 를 부르지 않는다 · Protocol · service · 도구 9 · MCP 그대로 · `GOLD_REPOSITORY` 로 고른다(기본 `csv`) |
| 완료 조건 | 로컬 DB 에 싣고 18105 를 DB 판으로 띄워 앱 37 답 키 대조 (나) 가 CSV 판과 같다(§7-3) |
| 범위 밖 | stg 반입 · stg 진입점 · stg 권한 · 회사 데이터 범위 · 요청마다 SQL — §9 「다음 범위」 |
| **stg 판(0.2.0)** | **gold 를 `app.main` 에 붙인다 · 표가 비었거나 적재가 틀리면 gold 만 꺼진 채(503) `app.main` 은 정상 기동** · 레포 `data/medallion/` · 적재기를 이미지에(Dockerfile 한 줄) · 같은 이미지 일회성 컨테이너로 dry-run → 적재 → 재시작 · VM 작업은 사용자가 직접 — §11. 남은 범위 밖: stg 권한 · 접근 제어 · prod · 요청마다 SQL |

## 1. 목적 · 범위

### 1-1. 목적

SPEC-001 은 gold 를 CSV 에서 메모리로 읽는다(_RESUME §2 11-16 「D2 저장 = DB 없이」). 11-17 결정으로 그 다음 단을 연다 — **silver · gold 를 허브 DB 테이블로 올리고, 허브가 CSV 대신 DB 에서 읽어도 응답이 같게** 한다(_RESUME §2 11-17 「채팅보다 DB 설계 먼저」 · 「DB 화 이번 목표 = 로컬 허브 DB 까지」). 이번 판은 **로컬**이다.

### 1-2. 정해진 것(다시 묻지 않는다)

지시서 「정해진 것」 을 그대로 옮긴다. 근거 칸의 「조사 추천」 은 `research-db.md` §0-2 의 추천이다.

| # | 정해진 것 | 근거 | 이 문서에서 |
|---|---|---|---|
| D-0 | 목표 = **로컬 허브 DB 까지**. stg 반입 · stg 진입점 · stg 권한 · 시드는 이번 범위 밖 | _RESUME §2 11-17 첫 행 · 지시서 | §1-3 · §9 |
| D-1 | 범위 = **silver 57 전부 + gold 15 + 원장 확인 목록**. 허브 코드가 읽는 범위는 지금 그대로(gold 15 + silver 보조 5표 + 원장 확인) · 나머지 silver 는 올려 두기만 · 원장 JSON 은 DB 에 안 올림 | 지시서 D-1 · 조사 D-1 추천 (b) · §2-3 | §2 · §5-2 |
| D-2 | 자리 = `public` + 접두어 — gold `g_*`(CSV 이름 그대로) · silver `s_*` | 지시서 D-2 · 조사 D-2 추천 (a) · §1-4 · §1-5 | §2-1 |
| D-3 | 칸 = 전부 문자열(CSV 값 그대로) · 빈칸 규칙 하나 · 「담을 칸 없는 값 0」 | 지시서 D-3 · 조사 D-3 추천 (a) · §2-5 | §2-1 · §2-7 |
| D-4 | 판 = 살아 있는 판 하나 · 전체 교체(한 트랜잭션) + 빌드 기록 표 1개 · 원문을 DB 에 통째로 넣지 않음 | 지시서 D-4 · 조사 D-4 추천 (a) · §5 5번 | §2-5 · §4-4 |
| D-5 | (로컬) 로컬 경로의 CSV 묶음을 **적재 CLI** 가 읽어 싣는다 · 경로는 env · 레포에 CSV 커밋 금지 | 지시서 D-5 · SPEC-001 §2-1 | §4 |
| D-6 | 허브 시작 때 DB 에서 전부 읽어 **지금 메모리 색인을 그대로** 세운다(Protocol 동기 그대로 · async 는 시작 때 읽기에만) · 응답 머리 `gold_hash` · `aux_hash` 는 빌드 기록 표 값 — CSV 판과 같은 값 | 지시서 D-6 · 조사 D-6 추천 (a) · §4 | §5 |
| D-8 | 원장 확인 목록은 id · 코드 쌍만 표 하나 | 지시서 D-8 · 조사 D-8 추천 (a) · _RESUME §2 11-16 「검수 뒤 결정 4」 ③ | §2-4 |
| D-9 | 옛 `phub-recommend`(PR #31) 스키마 · revision id 재사용 금지 — 새 revision id 는 옛 브랜치 3개와 겹치지 않게 | 지시서 · _RESUME §2 11-17 둘째 행 「graph/gold 스키마 · 시드는 버림」 · 조사 §5 6번 | §3-2 |
| D-10 | 기존 테이블 167 은 건드리지 않음 · FK 로 잇지 않음 | 지시서 · _RESUME §2 11-17 둘째 행 「기존 stg 테이블은 건드리지 않는 전제」 · 조사 §1-5 | §2-6 |

D-7(stg 에서 gold 가 뜨는 자리)은 0.1.0 에서 열려 있었고(§9 N-1) **0.2.0 에서 닫았다 — gold 를 `app.main` 에 붙이고, 표가 비었거나 적재가 틀리면 gold 만 꺼진 채 `app.main` 은 정상 기동**(§11-1 · §11-2).

### 1-3. 범위 · 범위 밖

| 이 스펙에서 만든다 | 범위 밖(§9 「다음 범위」 에 적는다) |
|---|---|
| 테이블 74 의 정의 · alembic 마이그레이션 1 · 모델 | stg · prod 로 가는 길 전부(진입점 D-7 · 데이터 반입 · 권한 · 접근 제어) |
| 적재 CLI(로컬 CSV → 로컬 DB) | 회사 데이터를 stg 에 어디까지 올리나 |
| DB 판 repository · 고르는 설정 · 두 판 대조 시험 | 요청마다 SQL 로 조회하는 repository(조사 D-6 (b)) · 다른 소비자가 SQL 로 직접 읽는 계약 |
| 로컬 PostgreSQL 띄우는 법 · DB 판 허브 띄우는 법 | 수 타입 · 여러 값 칸 풀기 같은 정규화(조사 §2-5) · 판 쌓기(조사 D-4 (b)) |
| | 허브 브랜치의 push · PR · 머지(각각 별도 승인 — _RESUME §2 11-16 「stg」) |

- **도구 계약은 안 바뀐다.** SPEC-001 §4 의 도구 9 · 응답 필드 · 쪽 넘김 · 오류는 그대로다. 바뀌는 곳은 §8 에 모았다.
- gold · silver 는 **밖에서 지어 온 표**다. 허브(적재기 · repository)는 값을 만들거나 바꾸지 않는다(SPEC-001 §1-3 「gold 빌드 · 검사 — 범위 밖」 · 조사 §5 1번).

## 2. 테이블

### 2-1. 공통 규칙

| # | 규칙 | 근거 |
|---|---|---|
| R1 | **CSV 1 = 테이블 1.** gold 는 CSV 이름 그대로(`g_entry` …) · silver 는 `s_` + CSV 이름(`s_concern` …) · 전부 `public`(스키마 이름을 붙이지 않는다) | D-2 · 조사 §1-4(허브에 스키마를 쓰는 곳 0) · §1-5(silver `modality` · `product` 가 기존 테이블과 같은 이름) · 재셈: 기존 167 가운데 `s_` · `g_` · `medallion` 으로 시작하는 이름 0 |
| R2 | **칸 이름 · 순서 = CSV 헤더 그대로.** 칸 타입은 전부 `TEXT`(길이 제한 없음) | D-3 · `$H/backend/app/modules/gold/inputs.py:3` 「칸은 전부 문자열」 · `:113-114`(헤더 순서까지 대조) |
| R3 | **빈칸 = NULL 하나로**(제안 — U-1). 적재기는 CSV 의 빈칸(`''`)을 NULL 로 싣고, 읽는 쪽은 NULL 을 `''` 로 돌려준다 — 테이블에 `''` 이 든 칸은 0 이어야 한다(시험 DT4 · DE3). 값이 있는 칸은 한 글자도 바꾸지 않는다 | D-3 「빈칸 규칙 하나로」 · 재셈: silver FK 80칸 가운데 **35칸에 빈칸이 있다**(빈 값 12,968) — `''` 로 두면 그 칸에 FK 를 걸 수 없다(§2-6) · CSV 에는 빈칸의 표기가 하나뿐이라(`''`) 왕복에서 잃는 것이 없다 |
| R4 | **표마다 `load_seq`(정수 · NOT NULL) 칸 하나를 더한다** — 그 파일에서의 행 번호(1 부터). 읽을 때 `ORDER BY load_seq` 로 파일 순서를 되살린다. CSV 에 없는 칸은 이것 하나뿐이다 | 응답 순서가 파일 순서다(`$H/backend/app/modules/gold/repository.py:5` · `service.py:136-139`) · cursor 가 순서에 기댄다(`core.py:100-106`) · 조사 §2-4 「행 순서 칸」. 키 있는 표는 지금 「파일 순서 = 키 오름차순」 이지만(재셈 — gold 14표 전부) 그것은 지금 데이터의 성질이고, 글자 정렬은 DB 정렬 규칙(collation)을 타므로 키 정렬에 기대지 않는다 |
| R5 | PK — 키 있는 표는 그 키(gold 12표 `gid` · `g_node.node_id` · `g_edge.edge_id` · silver 55표 `code` 또는 `id`) · **키 없는 표 3(`g_evidence` · `s_alias` · `s_source_ref`)은 `load_seq`** | 조사 §2-1 · §2-2 · 재셈(키 중복 0 · 키 빈칸 0) |
| R6 | NOT NULL 은 PK 칸 · 유일 제약 칸 · `load_seq` · FK 가 걸린 `g_edge.src` / `dst` 에만 건다. 그 밖의 칸은 전부 NULL 허용 | R3(빈칸 = NULL) |
| R7 | **JSON 칸 0 · 판 칸 0 · 원문 통째 칸 0.** 여러 값 칸(` · `)을 배열 · 자식 표로 풀지 않는다 | D-3 · D-4 · 조사 §5 2 · 4 · 5번 · §2-7 |
| R8 | 제약 · 인덱스 이름 — PK · FK 는 `Base.metadata` 이름 규칙 그대로(`pk_<표>` · `fk_<표>_<칸>_<대상 표>`) · **인덱스 · 유일 제약은 직접 짓는다**(`ix_<표>__<칸>_<칸>` · `uq_<표>__<칸>_<칸>`) | `$H/backend/app/model/base.py:8-14` · 규칙이 첫 칸만으로 인덱스 이름을 정해 복합 인덱스끼리 겹친다(조사 §2-4 · §5 7번) · 재셈: FK 이름 최대 **63자**(`fk_s_procedure_relation_effect_relation_id_s_procedure_relation` — PostgreSQL 한도 63 에 딱 맞음 · 중복 0) · 인덱스 이름 최대 47자 |
| R9 | 예약어 칸 `order` 2(`g_pair.order` · `s_procedure_relation.order`) — 칸 이름은 그대로 둔다. 적재기 · repository 는 SQLAlchemy 식으로만 SQL 을 짓는다(따옴표를 알아서 붙인다 · 손 SQL 금지) | 조사 §2-4 「예약어 칸」 · 재셈(`order` 든 표 = `g_pair` · `procedure_relation`) |
| R10 | 새 테이블에서 **기존 167 로 가는 FK 0** · gold → silver FK 0 | D-10 · 조사 §1-5(코드 체계가 다르다 · 대응표 `external_code` 는 0행) |

### 2-2. gold 15표

| 테이블 | 행 | CSV 칸 | PK | 유일 제약 | FK | 인덱스(§2-8) |
|---|---:|---:|---|---|---|---|
| `g_entry` | 2,642 | 10 | `gid` | — | — | (`norm`) · (`entity_table`, `entity_code`) |
| `g_scope` | 4,202 | 13 | `gid` | — | — | (`subject_table`, `subject_code`) · (`holder_table`, `holder_code`) |
| `g_profile` | 739 | 27 | `gid` | (`subject_table`, `subject_code`) | — | (유일 제약이 색인) |
| `g_indication` | 4,866 | 23 | `gid` | — | — | (`target_table`, `target_code`) · (`asked_concern_code`) · (`procedure_code`) · (`concern_code`) |
| `g_outcome` | 1,604 | 26 | `gid` | — | — | (`target_table`, `target_code`) · (`effect_code`) |
| `g_adverse` | 2,923 | 35 | `gid` | — | — | (`target_table`, `target_code`) · (`adverse_code`) |
| `g_adverse_detail` | 3,828 | 17 | `gid` | — | — | (`target_table`, `target_code`) · (`adverse_risk_id`) |
| `g_recovery` | 37 | 12 | `gid` | — | — | (`target_table`, `target_code`) |
| `g_contraindication` | 350 | 19 | `gid` | — | — | (`target_table`, `target_code`) · (`condition_code`) |
| `g_pair` | 904 | 27 | `gid` | — | — | (`from_table`, `from_code`) · (`to_table`, `to_code`) · (`question_class`) |
| `g_package` | 312 | 21 | `gid` | — | — | (`item_table`, `item_code`) · (`package_id`) · (`concern_code`) |
| `g_offer` | 163 | 28 | `gid` | — | — | (`item_table`, `item_code`) · (`offer_id`) · (`procedure_code`) |
| `g_node` | 1,545 | 7 | `node_id` | — | — | — |
| `g_edge` | 10,389 | 7 | `edge_id` | — | `src` → `g_node` · `dst` → `g_node` | (`src`, `edge_type`) · (`dst`, `edge_type`) |
| `g_evidence` | 27,740 | 6 | `load_seq` | (`gold_table`, `gold_id`, `silver_table`, `silver_id`) | — | (유일 제약의 앞 두 칸이 색인) |
| **합** | **62,244** | **278** | | | **2** | |

- 칸 목록은 `$H/backend/app/modules/gold/headers.py:6-41` 의 `GOLD_HEADERS` 가 정본이다(SPEC-001 부록 A · 실제 CSV 헤더와 같다 — 재셈). 여기에 다시 적지 않는다.
- `g_profile` 유일 제약 — 지금 계약이 「유일」 이다(SPEC-001 §3-1 · `memory.py:51` 이 첫 행 하나만 쓴다) · 재셈 739 / 739.
- `g_evidence` 유일 제약 — 네 칸에 빈칸 0 · 27,740 / 27,740 유일(재셈 · 조사 §2-1). 이 표의 `fields` 는 빈칸 25,929 다(NULL 로 들어간다).
- `g_edge` FK — `src` · `dst` 가 `g_node.node_id` 에 없는 행 0 · 빈칸 0(재셈 · 조사 §2-1).

### 2-3. silver 57표

키 · FK 는 `$SM/drafts/silver-check/silver-schema.json` 의 `tables[].key` · `columns[].fk` 를 그대로 읽었다(스키마 57표 = 파일 57 · 헤더 어긋남 0 — 재셈). 「FK 칸」 은 전부 대상 표의 키를 가리킨다(→ 뒤는 접두어 뺀 silver 이름). 「다형 칸」 은 FK 를 걸지 않는다(§2-7).

| 층 | 테이블 | 행 | CSV 칸 | PK | FK 칸(→ 대상) | 다형 칸 |
|---|---|---:|---:|---|---|---|
| ① | `s_adverse` | 188 | 7 | `code` | `parent_code`→adverse | — |
| ① | `s_alias` | 980 | 4 | `load_seq` | — | `target_table` |
| ① | `s_anatomy` | 105 | 7 | `code` | `tissue_code`→tissue | — |
| ① | `s_anatomy_site` | 89 | 3 | `id` | `anatomy_code`→anatomy · `site_code`→site | — |
| ① | `s_concern` | 260 | 7 | `code` | `parent_code`→concern | — |
| ① | `s_concern_site` | 95 | 3 | `id` | `concern_code`→concern · `site_code`→site | — |
| ① | `s_condition` | 151 | 8 | `code` | `parent_code`→condition · `material_code`→material | — |
| ① | `s_effect` | 70 | 7 | `code` | `parent_code`→effect | — |
| ① | `s_external_code` | 0 | 8 | `id` | — | `target_table` |
| ① | `s_material` | 143 | 7 | `code` | `parent_code`→material | — |
| ① | `s_material_spec` | 33 | 5 | `id` | `material_code`→material | — |
| ① | `s_mechanism` | 54 | 6 | `code` | `parent_code`→mechanism | — |
| ① | `s_method` | 49 | 7 | `code` | `parent_code`→method | — |
| ① | `s_modality` | 18 | 5 | `code` | — | — |
| ① | `s_organization` | 202 | 7 | `code` | `current_org_code`→organization | — |
| ① | `s_product` | 315 | 10 | `code` | `parent_code`→product | — |
| ① | `s_product_material` | 390 | 5 | `id` | `product_code`→product · `material_code`→material | — |
| ① | `s_product_method` | 63 | 3 | `id` | `product_code`→product · `method_code`→method | — |
| ① | `s_product_modality` | 317 | 3 | `id` | `product_code`→product · `modality_code`→modality | — |
| ① | `s_product_organization` | 575 | 6 | `id` | `product_code`→product · `org_code`→organization | — |
| ① | `s_site` | 89 | 6 | `code` | `parent_code`→site | — |
| ① | `s_source_ref` | 48,094 | 4 | `load_seq` | — | `target_table` |
| ① | `s_tissue` | 25 | 7 | `code` | `parent_code`→tissue | — |
| ② | `s_case_method` | 107 | 3 | `id` | `case_code`→procedure_case · `method_code`→method | — |
| ② | `s_case_product` | 332 | 3 | `id` | `case_code`→procedure_case · `product_code`→product | — |
| ② | `s_procedure` | 138 | 8 | `code` | `modality_code`→modality · `mechanism_code`→mechanism | — |
| ② | `s_procedure_case` | 268 | 8 | `code` | `procedure_code`→procedure · `tissue_code`→tissue · `anatomy_code`→anatomy · `site_code`→site · `material_code`→material | — |
| ② | `s_procedure_material` | 175 | 3 | `id` | `procedure_code`→procedure · `material_code`→material | — |
| ② | `s_product_procedure` | 81 | 4 | `id` | `product_code`→product · `procedure_code`→procedure | — |
| ③ | `s_adverse_factor` | 732 | 7 | `id` | `adverse_risk_id`→adverse_risk · `condition_code`→condition · `site_code`→site · `anatomy_code`→anatomy | — |
| ③ | `s_adverse_frequency` | 344 | 9 | `id` | `adverse_risk_id`→adverse_risk | — |
| ③ | `s_adverse_guidance` | 3,061 | 9 | `id` | `adverse_risk_id`→adverse_risk | `target_table` |
| ③ | `s_adverse_rating` | 69 | 7 | `id` | `adverse_risk_id`→adverse_risk · `scale_id`→rating_scale | `target_table` |
| ③ | `s_adverse_risk` | 2,840 | 18 | `id` | `adverse_code`→adverse · `site_code`→site | `target_table` |
| ③ | `s_citation` | 63 | 9 | `id` | — | — |
| ③ | `s_citation_link` | 241 | 5 | `id` | `citation_id`→citation | `relation_table` |
| ③ | `s_contraindication` | 350 | 14 | `id` | `condition_code`→condition · `site_code`→site | `target_table` |
| ③ | `s_indication` | 1,705 | 6 | `id` | `concern_code`→concern · `site_code`→site | `target_table` |
| ③ | `s_indication_condition` | 56 | 4 | `id` | `indication_id`→indication · `condition_code`→condition | — |
| ③ | `s_outcome` | 1,604 | 21 | `id` | `effect_code`→effect · `site_code`→site | `target_table` |
| ③ | `s_package` | 119 | 15 | `id` | `concern_code`→concern | — |
| ③ | `s_package_condition` | 3 | 4 | `id` | `package_id`→package · `condition_code`→condition | — |
| ③ | `s_package_item` | 312 | 7 | `id` | `package_id`→package | `target_table` |
| ③ | `s_package_schedule` | 28 | 6 | `id` | `package_id`→package | — |
| ③ | `s_procedure_relation` | 904 | 17 | `id` | — | `from_table` · `to_table` |
| ③ | `s_procedure_relation_effect` | 127 | 4 | `id` | `relation_id`→procedure_relation · `effect_code`→effect | — |
| ③ | `s_rating_scale` | 4 | 6 | `id` | — | — |
| ③ | `s_recovery` | 37 | 8 | `id` | — | `target_table` |
| ③ | `s_statement_translation` | 384 | 4 | `id` | `citation_link_id`→citation_link | — |
| ④ | `s_offer` | 122 | 10 | `id` | `price_list_id`→price_list · `modality_code`→modality | — |
| ④ | `s_offer_concern` | 28 | 4 | `id` | `offer_id`→offer · `concern_code`→concern | — |
| ④ | `s_offer_effect` | 10 | 4 | `id` | `offer_id`→offer · `effect_code`→effect | — |
| ④ | `s_offer_item` | 163 | 6 | `id` | `offer_id`→offer | `target_table` |
| ④ | `s_offer_material` | 17 | 4 | `id` | `offer_id`→offer · `material_code`→material | — |
| ④ | `s_offer_quantity` | 129 | 6 | `id` | `offer_id`→offer | — |
| ④ | `s_offer_site` | 77 | 4 | `id` | `offer_id`→offer · `site_code`→site | — |
| ④ | `s_price_list` | 1 | 5 | `id` | — | — |
| | **합 57표** | **66,936** | **387** | | **80** | **15칸(14표)** |

- 층: ① 사전 23 · ② 조합 6 · ③ 관계 20 · ④ 상품 8(조사 §2-2).
- 칸 목록의 정본은 `silver-schema.json` 의 `columns[].name`(= 실제 헤더)이다. 칸 뜻은 `$SM/notes/silver-tables.md` 가 정본이라 여기에 다시 적지 않는다(조사 §2-4).
- `s_alias` 는 (`target_table`, `target_code`, `name`) 에 **유일 제약**을 건다(980 / 980 · 세 칸 빈칸 0 — 재셈). `g_entry.silver_id` 의 「표|코드|이름」 묶음(831행)이 이 셋으로 행을 지목한다(조사 §2-1).
- `s_source_ref` 는 유일 제약을 걸지 않는다 — 유일한 묶음이 네 칸 전체뿐이고 `ref` 가 최대 222B 다(조사 §2-2). 색인 하나만 둔다(§2-8).
- `s_external_code` 는 0행이다 — 테이블만 만든다.
- **허브가 읽는 silver 는 5표뿐이다**(§5-2) — `s_source_ref` 4칸 · `s_concern` / `s_adverse` / `s_condition` 의 `code` · `parent_code` · `s_concern_site` 3칸. 나머지 52표는 올려 두기만 한다(D-1).

### 2-4. 원장 확인 목록 — `medallion_ledger_check`

| 칸 | 타입 | 뜻 |
|---|---|---|
| `lck_id` | TEXT · NOT NULL | 원장 확인 목록의 `id` |
| `code` | TEXT · NOT NULL | 그 행에서 뽑은 코드 |

- PK (`lck_id`, `code`) · 인덱스 (`code`). 행 = **273쌍**(목록 325행 · 코드 든 행 251 · 서로 다른 코드 218 — 재셈 · SPEC-001 §2-1 X6 과 같다).
- **글 칸은 싣지 않는다**(D-8 · SPEC-001 §2-1 X4 · X5). 원본 16칸 가운데 DB 에 가는 것은 `id` 와 뽑은 코드뿐이다.
- 코드 추출식은 **허브가 지금 쓰는 식 하나**다(`$H/backend/app/modules/gold/inputs.py:37-38` — 접두어 9종 + `-` + 숫자 · `silver_now` · `what` · `name` 세 칸 이음 `:169`). 적재기는 그 상수를 가져다 쓴다 — 식을 두 벌로 두지 않는다.
- `aux_hash` 에 들어가는 것은 **원본 파일 바이트**의 sha256 이다(§2-5). 표 내용(273쌍)과 해시가 1:1 이 아니다(조사 D-8 위험) — 그래서 원본 파일의 sha256 · 행 수(325)를 빌드 기록에 함께 둔다.

### 2-5. 빌드 기록 — `medallion_build`

**한 행 = 적재기가 읽은 파일 하나**(74행 = gold 폴더 16 + silver 57 + 원장 확인 목록 1). 판 전체의 값(`gold_hash` · `aux_hash` · `built_at` · `loader_version`)은 행마다 같은 값으로 든다 — 표를 하나로 두고 JSON 칸을 쓰지 않기 위해서다(D-4 「표 1개」 · R7 · 다른 꼴은 O-3).

| 칸 | 타입 | 뜻 |
|---|---|---|
| `file_name` | TEXT · PK | 파일 이름(`g_entry.csv` · `questions.csv` · `source_ref.csv` · `ledger-check-list.csv` …) — gold 폴더 · silver 폴더 · 원장 확인 목록 사이에 같은 이름 0(재셈) |
| `kind` | TEXT · NOT NULL | `gold`(15) · `hash_only`(1 — `questions.csv`) · `source_ref`(1) · `aux`(5 — `concern` · `adverse` · `condition` · `concern_site` · `ledger-check-list`) · `silver`(52 — 그 밖의 silver). 앞 넷은 지금 `FileRecord.kind` 와 같은 값이다(`inputs.py:46`) |
| `sha256` | TEXT · NOT NULL | 파일 바이트의 sha256 |
| `file_rows` | INTEGER | 파일의 데이터 행 수(`hash_only` 는 NULL — 읽지 않는다) |
| `table_name` | TEXT | 실은 테이블(`hash_only` 는 NULL) |
| `table_rows` | INTEGER | 실은 행 수(원장 확인 목록만 `file_rows` 325 ≠ `table_rows` 273) |
| `gold_hash` | TEXT · NOT NULL | 판의 gold 해시(행마다 같은 값) |
| `aux_hash` | TEXT · NOT NULL | 판의 보조 해시(행마다 같은 값) |
| `built_at` | 시각(시간대 포함) · NOT NULL | 적재 시각(행마다 같은 값) |
| `loader_version` | TEXT · NOT NULL | 적재기 판(행마다 같은 값) |

- 이 표와 §2-4 는 CSV 를 1:1 로 옮긴 표가 아니다 — R2 ~ R4(전부 문자열 · `load_seq`)는 `g_*` · `s_*` 72표의 규칙이다.
- **해시는 지금 식 그대로다**(`inputs.py:64-67` · `:177-178` — 「파일 이름 + 공백 + sha256」 줄을 이름순으로 `\n` 으로 이어 다시 sha256). `gold_hash` = `kind` ∈ {`gold`, `hash_only`} 16 파일 · `aux_hash` = `kind` ∈ {`source_ref`, `aux`} 6 파일. 재셈: `8accbb213ac5327d8675f8156bc57d87c12a3245c383c8239074444da7f6228c` · `6435fe41f3851574729ef7aa7e108afb5cf7601c1764c160496a9e49aa1803a3`(조사 §3-1 · 시험 상수 `SPEC_GOLD_HASH_1116` 과 같다).
- 해시는 **파일 바이트**에서 나오므로 DB 행으로는 다시 못 낸다(조사 §3-1 「DB 로 갈 때」 1). 그래서 적재 때 센 값을 여기 둔다 — 그리고 누구든 이 표의 `file_name` · `sha256` 줄로 같은 식을 돌려 `gold_hash` · `aux_hash` 를 다시 셀 수 있다(허브도 시작 때 그렇게 대조한다 — §5-3).
- `questions.csv` 는 **싣지 않고 sha256 만** 둔다(SPEC-001 §2-3 3 · O-3 로컬 = (a) 그대로).
- 원문(CSV 본문 · 원장 JSON)은 DB 에 통째로 넣지 않는다(D-4 · 조사 §5 5번).
- silver 57 전체에 같은 식을 쓴 값(재셈 `91237618…9c9254`)은 따로 칸을 두지 않는다 — 이 표의 silver 57줄로 다시 셀 수 있다(O-4).

### 2-6. FK

| 무엇 | 수 | 정한 것 |
|---|---:|---|
| silver 안 FK | 80 | **건다**(제안 — U-1). 스키마의 FK 칸 그대로 · 대상은 전부 그 표의 PK · 실제 값으로 깨진 FK 0(재셈 · 조사 §2-2) |
| 그중 자기 참조 | 11 | `parent_code` 10표(`adverse` · `concern` · `condition` · `effect` · `material` · `mechanism` · `method` · `product` · `site` · `tissue`) + `organization.current_org_code` |
| gold 안 FK | 2 | `g_edge.src` · `dst` → `g_node.node_id` |
| gold → silver | 0 | 걸지 않는다(R10). gold 의 코드 칸은 다형 짝이거나 한 칸에 두 값이 든 행이 있다(`g_profile.modality_code` 2행 — 조사 §2-5 A) · `g_adverse_detail.adverse_risk_id` 처럼 silver 키를 가리키는 홑 칸도 이번에는 걸지 않는다(O-5) |
| 새 테이블 → 기존 167 | 0 | D-10 |

- **왜 거나**: D-1 을 (b)(silver 전부)로 정한 근거가 「gold 행 → silver 행 → `source_ref` 가 DB 안에서 닫히고 silver FK 80칸이 전부 걸린다」 였다(조사 §0-2 D-1 · §2-3). FK 를 안 걸면 silver 를 다 올리고도 관계가 글자로만 남는다.
- **빈칸과 묶여 있다**: FK 80칸 가운데 35칸에 빈칸이 있다(재셈). 빈칸을 `''` 로 실으면 그 칸은 FK 를 못 건다(`''` 인 대상 행이 없다) — 그래서 R3 가 「빈칸 = NULL」 이다. 「빈칸 = `''`」 를 고르면 FK 는 0 이 된다(U-1 (b)).
- **전부 `DEFERRABLE INITIALLY DEFERRED`** 로 건다(제안). 전체 교체를 한 트랜잭션에서 하므로(§4-4) 지우는 순서 · 싣는 순서 · 자기 참조 11칸의 행 순서를 따지지 않고 커밋 때 한 번에 검사하게 한다. 이 옵션이 `alembic check` 에서 모델과 어긋나지 않는지는 **확인 안 됨**(DB 를 띄우지 않았다) — WORK 첫 WP 에서 확인하고, 어긋나면 「지연 없이 + 의존 순서대로 싣기」 로 바꾼다(O-6).
- SQLite 는 FK 를 기본으로 검사하지 않는다(시험 기반 — §3-3). FK 위반을 막는 것은 PostgreSQL 에서만 믿는다.

### 2-7. 다형 참조 · 1:1 로 안 맞는 칸

**결론: 칸을 문자열 그대로 옮기므로 담을 칸 없는 값은 0 이다**(D-3 · 조사 §2-5 결론). 아래는 정규화하려 들 때만 걸리는 칸이고, 이 스펙은 **전부 그대로 둔다**.

| 무엇 | 수 | 처리 |
|---|---|---|
| 다형 참조(표 이름 칸 + 코드 칸) | silver 15칸(14표 — §2-3 「다형 칸」) · gold 12짝 + 되짚기 `silver_table` + `silver_id`(13표) · `gold_table` + `gold_id`(2표) | **FK 없음 · 값 그대로.** 가리키는 표가 5 ~ 54가지라 FK 한 줄로 못 건다(조사 §2-5 C). 적재기는 「가리킨 행을 못 찾은 수」 를 **세어 보여 주기만** 하고 막지 않는다(§4-3) — gold · silver 검사는 gold-check · silver-check 책임이다(SPEC-001 §2-3 6) |
| 한 끝이 빈 다형 짝 | `g_pair.from_table` 6 · `to_table` 31 · `g_package.item_table` 47 · `g_offer.item_table` 20(silver 쪽도 같은 수) | 빈칸이 「끝 없음」 이라는 값이다(조사 §2-5 C) — NULL 로 들어가고 읽을 때 `''` 로 돌아온다 |
| 한 칸에 여러 값(` · `) | gold 13칸 | 그대로 한 칸(R7). 사전과 안 맞는 조각이 4칸에 있고 한 칸 안 중복 조각이 35행 있다 — 풀면 값이 달라진다(조사 §2-5 A) |
| 묶음 값(`이름(역할)` · `척도=값` · `수+단위`) | gold 3칸 | 그대로 한 칸(조사 §2-5 B) |
| 묶음 식별자 · 목록(`|` · ` + `) | `g_entry.silver_id` 831행 · `g_evidence.fields` · `evidence_kind` | 그대로 한 칸(조사 §2-5 D) |
| 수 칸 | gold 정수 26 · 소수 2 / silver 정수 29 · 소수 4 | 그대로 문자열(R2). 소수 1값이 float 왕복에서 표기가 달라진다(조사 §2-5 E) — 수 타입으로 바꾸지 않으므로 걸리지 않는다 |
| 예약어 칸 `order` | 2 | R9 |
| 전부 빈 칸 · 0행 표 | gold 1칸 · silver 6칸 + `external_code` | 칸 · 표는 만든다(전부 NULL · 0행) |
| 줄바꿈 · NUL 이 든 값 | 0(재셈 — 72표 1,099,733칸) | 적재기가 NUL 을 만나면 검사 실패로 본다(PostgreSQL 문자열에 못 넣는다 — §4-3) |

### 2-8. 인덱스

D-6 에서 허브는 시작 때 표를 통째로 읽으므로 **허브 자신은 이 인덱스를 쓰지 않는다.** 그래도 「허브 메모리 색인이 쓰는 키」 와 같은 키를 테이블 색인으로 둔다(지시서 · SPEC-001 §3-1 끝 줄 「DB 로 가면 같은 키가 테이블 색인이 된다」) — DB 를 SQL 로 직접 읽을 때 같은 길로 찾게 하기 위해서다. 그 밖의 인덱스는 만들지 않는다.

| 메모리 색인(`memory.py`) | 테이블 색인 |
|---|---|
| `entry_by_norm` `:45` · `entry_by_entity` `:47` · `entry_by_table` `:48` | `g_entry` (`norm`) · (`entity_table`, `entity_code`) — `entity_table` 홑 칸은 뒤 색인의 앞 칸이라 따로 두지 않는다 |
| `scope_by_subject` `:49` · `scope_by_holder` `:50` | `g_scope` 2 |
| `profile_by_subject` `:51` | `g_profile` 유일 제약 |
| `by_target` 6표 `:18,52` | 6표 (`target_table`, `target_code`) |
| `by_value` 12짝 `:20-27,53` | 12(§2-2 표의 홑 칸 색인) |
| `pair_by_from` · `pair_by_to` `:54-55` · `package_by_item` · `offer_by_item` `:56-57` | 4 |
| `edges_out` · `edges_in` `:58-59` | `g_edge` 2 |
| `evidence` `:60` | `g_evidence` 유일 제약(앞 두 칸) |
| `source_ref` `:61-64` | `s_source_ref` (`target_table`, `target_id`) |
| `ledger` `:104` | `medallion_ledger_check` (`code`) |
| `by_key` `:37` | PK |
| 속성 맞춤 색인(` · ` 로 쪼갠 조각) `:67-77` · 계층 자식 목록 `:80-88` · 하위 닫힘(`closure.py`) | **테이블 색인 없음** — 조각 · 닫힘은 메모리에서 세운다(DB 에 파생 표를 만들지 않는다 — 조사 D-6 (c) 위험 「gold 불변과 부딪힌다」) |

수: 직접 지은 인덱스 **30**(gold 28 + `s_source_ref` 1 + `medallion_ledger_check` 1) · 유일 제약 3(`g_profile` · `g_evidence` · `s_alias`). silver 의 나머지는 PK · FK 뿐이다.

### 2-9. 셈(빠짐 0)

| 묶음 | 표 | 행 | 근거 |
|---|---:|---:|---|
| gold | 15 | 62,244 | §2-2 · 재셈 |
| silver | 57 | 66,936 | §2-3 · 재셈 |
| 원장 확인 | 1 | 273 | §2-4 |
| 빌드 기록 | 1 | 74 | §2-5 |
| **합** | **74** | **129,527** | 기존 167 + 74 = `public` 241 |

CSV 칸 665(278 + 387) + `load_seq` 72 + §2-4 의 2 + §2-5 의 10 = 테이블 칸 749. FK 82 · 직접 지은 인덱스 30 · 유일 제약 3.

## 3. 마이그레이션 · 모델

### 3-1. 모델 자리

| 무엇 | 정한 것 | 근거 |
|---|---|---|
| 모델 파일 | `backend/app/model/` 에 새 파일 하나(이름 제안 `medallion.py`) — 74 테이블을 `Base.metadata` 에 올린다 | 모델은 전부 `app/model/*.py` 에 있다(조사 §1-2) |
| 등록 | `backend/app/model/__init__.py` 에 import 한 줄을 더한다 | 「alembic autogenerate 감지용」 으로 전부 import 한다(`$H/backend/app/model/__init__.py:1-60`) |
| 짓는 법 | 72표(`g_*` · `s_*`)는 **헤더 계약 상수에서 기계로** 짓는다 — 표마다 손으로 쓰지 않는다. gold 는 지금 있는 `GOLD_HEADERS`(`headers.py:6-41`) · silver 는 같은 꼴의 새 상수(표 → 칸 목록 · 키 · FK — `silver-schema.json` 에서 이름만 옮긴다) | 칸 665 를 손으로 옮기면 어긋난다 · 계약이 헤더 순서까지 대조한다(`inputs.py:113-114`) |
| 계약의 원천 | **하나.** 모델 · 적재기 · DB 판 repository · 시험이 같은 상수를 읽는다. 마이그레이션 파일만 그 시점의 풀어 쓴 고정본이다 | 「같은 사실을 두 곳에」 두면 한쪽이 낡는다 |
| 타입 | `Text` · `Integer` · 시간대 있는 시각뿐 — PostgreSQL 전용 타입 0 · `schema=` 0 | §3-3 |

상수 · 모델 파일의 이름과 자리는 구현 때 정한다(O-7).

### 3-2. 마이그레이션

| 항목 | 정한 것 | 근거 |
|---|---|---|
| 개수 | **alembic 1개** — 74 테이블 · FK 82 · 인덱스 30 · 유일 제약 3 을 한 revision 에(schema 만 · 데이터 없음) | 한 판이 한 덩어리다. 데이터는 마이그레이션에 넣지 않는다(조사 §3-3 (c) — 컨테이너 시작이 적재를 기다리게 된다 · D-5) |
| revision id | 제안 `b202611170001` · `down_revision = b202610300001`(지금 release 헤드 `legacy_prod_documents`) | 체인이 한 줄이고 헤드가 `b202610300001` 이다(조사 §1-2 · `$H/backend/alembic/versions/b202610300001_legacy_prod_documents.py:10-11`) |
| 옛 브랜치와 겹침 | 옛 `phub-recommend` 의 revision 3(`b202610260001` · `b202610300001` · `b202610310001`)과 **다른 id** | D-9 · 재셈(`git ls-tree origin/kknaksss/phub-recommend backend/alembic/versions/`) |
| 옛 테이블 이름 | 새 74 이름은 옛 브랜치 테이블(`gold_*` 8 · `graph_*` 6)과 하나도 겹치지 않는다 | 조사 §1-5 · 재셈 |
| downgrade | 74 테이블을 지운다(FK 가 있으므로 의존 역순 또는 한꺼번에) | 허브 관례(`…legacy_prod_documents.py:23-24`) |
| 꼴 | 마이그레이션 파일은 `op.create_table` 을 풀어 쓴 고정본이다 — 앱의 계약 상수를 import 하지 않는다 | 상수가 바뀌어도 지난 revision 이 바뀌면 안 된다 |

- **옛 브랜치로 올린 로컬 DB 에는 돌리지 않는다.** 옛 `b202610300001` 과 지금 헤드가 글자만 같고 내용이 다르다(조사 §5 6번) — 그런 DB 는 alembic 이 「이미 헤드」 로 읽어 새 revision 을 어긋난 바탕 위에 얹는다. 로컬 DB 는 **새 빈 DB** 에서 `upgrade head` 로 만든다(§6-1 · 시험 DE1).
- silver · gold 표가 바뀌면(11-16 보강 때 표 1 · 칸 2 가 늘었다 — 조사 D-1 위험) 계약 상수 + 새 revision 이 함께 간다. 적재기는 헤더가 계약과 다르면 싣지 않는다(§4-3).

### 3-3. 깨지지 않는 조건(CI · 기존 시험)

| # | 조건 | 왜 |
|---|---|---|
| C1 | 마이그레이션에 있는 테이블 = 모델에 있는 테이블(74 · 칸 · 제약 · 인덱스까지) | CI 가 빈 PostgreSQL 에 `alembic upgrade head` 뒤 `alembic check` 로 `Base.metadata` 와 DB 를 대조한다(`$H/.github/workflows/backend-test.yml:66-70`) |
| C2 | 모델이 **SQLite 에서 `Base.metadata.create_all` 로 만들어진다** | 기존 시험이 SQLite 메모리에 `create_all` 을 한다(`grep -rn create_all backend/tests` — 재셈 28줄 · 조사 §1-3 2) · CI pytest 는 SQLite 다(`backend-test.yml:76-80`) |
| C3 | PostgreSQL 전용 타입 · 전용 SQL · `schema=` · 부분 인덱스를 쓰지 않는다 | C2 · `alembic/env.py:27-44` 에 `include_schemas` 가 없다(조사 §1-4) |
| C4 | 이름 길이 ≤ 63 · 이름 중복 0 | R8(FK 최대 63 · 인덱스 최대 47 — 재셈) |
| C5 | `ruff check` 통과 | `backend-test.yml:72-74` |
| C6 | 기존 gold 시험(CSV 판)과 그 밖의 기존 시험이 그대로 통과한다 | 이 스펙은 CSV 판을 남긴다(§5-1) |
| C7 | DB 판 repository · 적재기가 **SQLite 에서도 돈다** | CI 에는 실물 데이터도 PostgreSQL pytest 도 없다(조사 §4-4) — SQLite 에서 안 돌면 CI 가 DB 판을 시험하지 못한다 |

확인 안 된 것: 지연 FK(§2-6)가 C1 에서 어긋나는지 · 마이그레이션에만 있고 모델에 없는 테이블을 `alembic check` 가 잡는지(조사 §6 7번) — 둘 다 WORK 첫 WP 에서 로컬 PostgreSQL 로 확인한다(O-6).

## 4. 적재 CLI

### 4-1. 자리 · 입력

| 항목 | 정한 것 | 근거 |
|---|---|---|
| 자리 | `backend/scripts/` 에 새 스크립트 하나(이름 제안 `load_medallion.py`) · `uv run python scripts/<이름>.py` | 허브의 운영 CLI 자리(`$H/backend/README.md` 「폴더 역할」 · 전례 `scripts/import_legacy_corpus.py`) |
| 입력 env | `GOLD_CSV_DIR`(gold 폴더 — 15표 + `questions.csv`) · `GOLD_SILVER_DIR`(silver 폴더 — 57표 · **새 env · 이름 제안**) · `GOLD_LEDGER_CHECK_PATH`(원장 확인 목록) · `GOLD_EXPECTED_HASH`(선택) · `DATABASE_URL`(허브 공용 — alembic 이 읽는 그 값) | D-5 「경로는 env」 · 지금 env(`config.py:19,32-38`) · `alembic/env.py:18`. silver 폴더는 지금 `GOLD_HIERARCHY_DIR` 이 가리키는 폴더와 같다(`backend/README.md` gold 절) — 이름이 「계층」 이라 57표 폴더로는 새 이름을 제안한다(O-7) |
| env 읽는 법 | 지금 gold 설정과 같다 — `envs/.env.gold`(git 제외) 또는 프로세스 env · 프로세스 env 가 앞선다 | `config.py:1-6,25-29` |
| DB 접속 | 적재기 자신의 엔진(요청용 pool 아님 · 15초 쿼리 제한을 물려받지 않는다) | `backend/README.md` 「Alembic 의 NullPool migration 연결과 operator CLI 의 별도 engine 은 API request pool 이 아니다」 |
| 레포 | CSV 를 레포에 두지 않는다 · 적재기는 값 본문을 로그에 찍지 않는다(표 이름 · 행 수 · 해시 · 파일 이름만) | D-5 · SPEC-001 §2-1 |

### 4-2. 순서

```
① env 읽기 → ② 파일 읽기 · 검사(§4-3) → ③ 해시 셈 → ④ 요약 출력
   └ dry-run 이면 여기서 끝(DB 에 접속하지 않는다)
⑤ DB 확인(새 테이블이 있는가) → ⑥ 한 트랜잭션: 지우기 → 싣기 → 빌드 기록 → 되읽어 대조 → 커밋
```

### 4-3. 검사(② — DB 를 건드리기 전)

| # | 검사 | 실패하면 |
|---|---|---|
| V1 | 필수 env 가 있다 · 폴더 · 파일이 있다 | exit 2 |
| V2 | gold 15표 · silver 57표가 **전부 있다** | exit 2 |
| V3 | silver 폴더에 계약 밖 CSV 가 없다(표가 늘었다는 뜻 — 스키마가 먼저 따라가야 한다). gold 폴더의 계약 밖 CSV 는 지금처럼 `hash_only` 로 해시에만 넣는다(`inputs.py:117-120`) | exit 2 |
| V4 | 파일이 UTF-8(BOM 허용)이고 모든 행의 칸 수 = 헤더 칸 수 | exit 2(지금 `_parse` 와 같은 판정 — `inputs.py:76-91`) |
| V5 | **헤더 = 계약**(이름 · 순서) — 72표 | exit 2 |
| V6 | PK 칸에 빈칸 0 · 중복 0 · 유일 제약 3 의 묶음에 중복 0 | exit 2 |
| V7 | FK 82칸 — 빈칸이 아닌 값이 대상 표의 키에 있다 | exit 2(DB 도 커밋 때 막지만 dry-run 에서 먼저 읽을 수 있는 말로 보여 준다) |
| V8 | NUL 이 든 값 0 | exit 2 |
| V9 | `GOLD_EXPECTED_HASH` 가 있으면 센 `gold_hash` 와 같다 | exit 2(없으면 지금처럼 경고만 — `inputs.py:179-183`) |
| V10 | (세기만) 다형 참조가 가리킨 행을 못 찾은 수 · 표별 행 수 · 빈칸 수 | 막지 않는다 — 요약에 찍는다 |

행 수 검사는 두 곳이다 — ② 에서 「파일 행 수」 를 세어 요약에 찍고, ⑥ 에서 「실은 행 수 = 파일 행 수」 를 대조한다(§4-4).

### 4-4. 한 트랜잭션 교체(⑥)

| # | 하는 것 |
|---|---|
| L1 | ⑤ 새 테이블 74 가 없으면(마이그레이션 전) 쓰지 않고 끝낸다 — exit 2 · 「`alembic upgrade head` 먼저」 |
| L2 | 트랜잭션 하나를 연다. 새 테이블 74 의 행을 전부 지운다(기존 167 은 건드리지 않는다) |
| L3 | 72표를 싣는다 — 행마다 `load_seq` = 파일 행 번호 · 빈칸 → NULL · 그 밖의 값은 그대로. 한 번에 보내는 묶음은 (칸 수 × 행 수)가 드라이버의 매개변수 한도를 넘지 않게 나눈다(가장 넓은 표 = `g_adverse` 35칸 + 1) |
| L4 | `medallion_ledger_check` 273쌍 · `medallion_build` 74행을 싣는다 |
| L5 | **커밋 전에 되읽어 대조한다** — 표마다 `count(*)` = 파일 행 수 · `load_seq` 순으로 읽은 행(NULL → `''`) = CSV 행(값 · 순서) · `''` 이 든 칸 0. 하나라도 다르면 롤백 |
| L6 | 커밋. FK 는 이때 검사된다(§2-6) |

- **실패 때 그대로**: L2 ~ L6 어디서 실패해도 롤백되어 DB 는 **옛 판 그대로**다(처음이면 빈 채로). exit 3.
- 멱등: 같은 묶음을 다시 실으면 `built_at` 만 다른 같은 상태가 된다.
- 떠 있는 허브는 다시 실어도 옛 판을 들고 있다 — **적재 → 허브 재시작 → `health` 의 해시 확인**이 한 절차다(조사 §3-2 · SPEC-001 §2-3 1 「바뀌면 재시작」).
- 되돌리기 = 옛 CSV 묶음을 다시 싣는다. DB 안에 옛 판은 없다(D-4 (a) 의 위험 — 조사 D-4). 로컬에서는 `$SM` 이 그 묶음이다.

### 4-5. dry-run · exit code

| | |
|---|---|
| `--dry-run` | ① ~ ④ 만 — **DB 에 접속하지 않고 쓰지 않는다.** 요약 = 표별 행 수 · 빈칸 수 · `gold_hash` · `aux_hash` · 파일별 sha256 · V10 의 셈 · 실을 테이블 수(74) · 실을 행 수(129,527 — 11-16 gold) |
| exit 0 | 성공(dry-run 은 검사 통과) |
| exit 2 | 입력 · 검사 실패(V1 ~ V9 · L1) — **DB 에 쓴 것 0** |
| exit 3 | DB 쓰기 · 대조 실패(L2 ~ L6) — 롤백됨 · 옛 판 그대로 |

exit 0 / 2 는 허브 전례와 같다(`scripts/import_legacy_corpus.py:13` 「0 success, 2 … rejected (nothing written)」). 3 은 제안이다(O-7).

## 5. repository — DB 판

### 5-1. 고르는 설정

| env | 값 | 뜻 |
|---|---|---|
| `GOLD_REPOSITORY`(새 env · 이름 제안) | `csv`(**기본**) | 지금 그대로 — CSV 를 읽는다. 필수 env 넷은 그대로 |
| | `db` | DB 에서 읽는다. `DATABASE_URL` 이 있어야 하고 CSV 경로 env 넷은 필요 없다 |
| | 그 밖의 값 | 시작 실패 |

- 기본을 `csv` 로 둔다 — 지금 동작 · 기존 시험 · README 의 실행 명령이 안 바뀌고, CSV 판이 DB 판의 **대조 기준**으로 남는다(§7). 기본값을 `db` 로 뒤집는 것은 stg 로 갈 때 정한다(§9).
- `GOLD_EXPECTED_HASH` 는 두 판에서 같은 뜻이다 — 주면 다를 때 시작 실패 · 없으면 경고만(`inputs.py:179-183`).
- 갈아 끼우는 자리는 이미 열려 있다 — `GoldState(settings, repository_factory=…)`(`$H/backend/app/modules/gold/service.py:34` · 조사 §4-1).

### 5-2. 시작 때 읽기

```
lifespan(async)
  └ db 판: DB 에서 한 번 읽는다(async) ─▶ LoadedInputs ─▶ GoldMemory(지금 코드 그대로) ─▶ 같은 색인 · 같은 LoadRecord
  └ csv 판: read_inputs(settings)        ─▶ LoadedInputs ─▶ (같음)
요청: 메모리만 읽는다(두 판 모두 · DB 접속 0)
```

| # | 지킬 것 | 근거 |
|---|---|---|
| P1 | **Protocol 은 그대로다** — `GoldRepository` 의 메서드 29 · 전부 동기 · 돌려주는 행 = 읽기 전용 `Mapping[str, str]`. service · 도구 9 · router · MCP 를 고치지 않는다 | D-6 · `repository.py:40-77` · 조사 §4-1 · §4-3 (a) |
| P2 | DB 판은 **CSV 판과 같은 `LoadedInputs`** 를 만들어 **같은 메모리 색인 코드**(`GoldMemory`)에 넘긴다. 색인 · 닫힘 · `integrity` 셈을 DB 판용으로 다시 쓰지 않는다 | 「같은 결과」 를 코드가 같다는 것으로 먼저 보장한다 — 대조할 것이 「두 `LoadedInputs` 가 같은가」 로 줄어든다(§7 DT9). 지금 `CsvMemoryGoldRepository` 는 `read_inputs` 를 생성자 안에서 부른다(`repository.py:83-87`) — 「입력 읽기」 와 「색인 세우기」 를 가르는 것이 구현 일이다 |
| P3 | async 는 **시작 때 읽기에만** 쓴다. 읽고 나면 그 엔진을 닫는다 — 떠 있는 허브는 DB 연결을 들고 있지 않다 | D-6 · 허브에 동기 드라이버가 없다(`pyproject.toml` — asyncpg · aiosqlite 뿐 · 조사 §1-1) · 한 요청이 repository 를 수백 번 부른다(조사 §4-2) |
| P4 | 읽기용 엔진은 적재기처럼 따로 만든다(요청용 pool · 15초 쿼리 제한을 쓰지 않는다) | `backend/README.md` · `core/config.py:53` — 표 하나(48,094행)를 통째로 읽는 시간은 **확인 안 됨**(조사 §4-3) · 시험 DE8 에서 잰다 |
| P5 | **읽는 범위는 지금 그대로다**: gold 15표 전 칸 · `s_source_ref` 4칸 · `s_concern` / `s_adverse` / `s_condition` 의 `code` · `parent_code` **두 칸만** · `s_concern_site` 3칸 · `medallion_ledger_check` · `medallion_build`. 나머지 silver 52표는 읽지 않는다 | D-1 · SPEC-001 §2-1 X2(계층 3표는 두 칸만 — 「읽을 칸을 두 칸만 고르는 쿼리」 로 지킨다 · 조사 §4-3) · 조사 §2-3 |
| P6 | 순서 — gold 15표 · `s_source_ref` 는 `ORDER BY load_seq` | R4 |
| P7 | NULL → `''` · 그 밖의 값은 그대로 | R3 |
| P8 | **한 판만 읽는다** — 읽는 동안 적재기가 커밋해도 섞인 판을 들지 않는다. PostgreSQL 에서는 읽기 전체를 한 스냅숏(트랜잭션 하나 · 반복 읽기 격리)으로 하고, 방언과 무관하게 「처음 읽은 빌드 기록 = 끝에 다시 읽은 빌드 기록」 을 대조한다 | 기본 격리에서는 SELECT 마다 스냅숏이 달라 표 사이에 판이 섞일 수 있다 · SQLite 시험에서도 같은 대조가 돌아야 한다(C7) |
| P9 | `LoadedInputs` 를 채우는 법 — `gold_hash` · `aux_hash` = 빌드 기록 값 · `files` = 빌드 기록의 `kind` ∈ {`gold`, `hash_only`} 16줄(이름순) + {`source_ref`, `aux`} 6줄(지금 순서: `source_ref` → `concern` → `adverse` → `condition` → `concern_site` → 원장 확인 목록 — `inputs.py:129-175,193`) · `rows` = `file_rows` · `ledger_rows` = 원장 확인 목록의 `file_rows`(325) · `ledger_rows_with_code` = `medallion_ledger_check` 의 서로 다른 `lck_id` 수(251) | 그래야 `health.files[]` 22줄 · `health.aux` 가 CSV 판과 같다(`service.py:152-166` · `repository.py:89-102`) |
| P10 | `build.loaded_at` · `health.load_ms` 는 지금 뜻 그대로(이 프로세스가 메모리에 올린 시각 · 걸린 시간) — DB 에 실은 시각(`built_at`)과 다른 값이다 | `repository.py:91-92` · `core.py:108-110` |

### 5-3. DB 판의 시작 실패 조건

「적재 실패 = 시작 실패」 를 그대로 잇는다(SPEC-001 §2-3 5 · 조사 §5 9번 — 「없어도 경고만 하고 뜸」 은 없다).

| # | 조건 |
|---|---|
| F1 | `DATABASE_URL` 없음 · 접속 실패 · 새 테이블 없음 |
| F2 | `medallion_build` 가 0행(실은 적이 없다) |
| F3 | `medallion_build` 의 판 값(`gold_hash` · `aux_hash` · `built_at` · `loader_version`)이 행마다 같지 않다 |
| F4 | 빌드 기록의 `file_name` · `sha256` 줄로 다시 센 `gold_hash` · `aux_hash` 가 기록 값과 다르다 |
| F5 | 읽은 표의 행 수가 빌드 기록의 `table_rows` 와 다르다 |
| F6 | `GOLD_EXPECTED_HASH` 가 있는데 `gold_hash` 와 다르다 |
| F7 | 읽기 처음 · 끝의 빌드 기록이 다르다(P8) |

- 허브는 DB 판에서도 gold 를 **다시 검사하지 않는다** — `health.integrity` 의 네 셈은 같은 메모리 코드가 센다(`memory.py:116-131` · P2).
- 헤더 계약(SPEC-001 §2-3 5 「헤더가 부록 A 와 다름」)은 DB 판에서 **적재기의 V5 와 마이그레이션**이 지킨다 — 테이블 칸이 계약에서 지어지므로 허브가 시작 때 다시 대조할 헤더가 없다.

### 5-4. 두 판이 같은가 — 대조

| 층 | 무엇을 견주나 | 같다의 뜻 |
|---|---|---|
| 입력 | CSV 판 `read_inputs` 의 `LoadedInputs` vs DB 판이 읽은 `LoadedInputs` | `gold`(표 · 행 · 칸 · 값 · 순서) · `source_ref` · `hierarchy` · `concern_site` · `ledger_ids_by_code` · `ledger_rows` · `ledger_rows_with_code` · `files` · `gold_hash` · `aux_hash` 가 전부 같다 |
| 도구 응답 | 같은 요청을 두 판에 | JSON 이 같다 — `build.loaded_at` 만 뺀다(`health` 는 `load_ms` 도) |
| 앱 | 답 키 대조 (나) | CSV 판에서 뽑은 37 키와 DB 판에서 뽑은 37 키가 같다(§7-3) |

## 6. 로컬 실행

DB · 서버를 띄우고 내리는 것은 **코디네이터**가 한다(워커는 사용자 포트 · 프로세스를 건드리지 않는다). 아래 `<…>` 는 자리 표시다 — 접속 값을 문서 · 레포에 적지 않는다.

### 6-1. 로컬 PostgreSQL

| 항목 | 제안 | 근거 |
|---|---|---|
| 무엇으로 | Docker `postgres:16` 컨테이너 하나(U-2) | CI · 리허설이 `postgres:16` 이다(`backend-test.yml:37` · 조사 §1-1). 이 기계에 `docker` 와 Homebrew `postgresql@17` 이 둘 다 있다(재셈 — `which`) |
| 포트 | **`127.0.0.1:18432`** | 금지 18210 · 18005 · 쓰는 중 18105(허브) · 18220(앱) 과 겹치지 않는다. 지금 듣고 있는 18xxx = 18105 · 18106 · 18210 · 18220 이고 54xx 는 없다(재셈 — `lsof -nP -iTCP -sTCP:LISTEN`). 띄우기 전에 다시 확인한다 |
| DB | **새 빈 DB**(새 컨테이너 · 새 볼륨) — 옛 브랜치로 올린 DB 를 다시 쓰지 않는다 | §3-2 |
| 데이터 자리 | 이름 붙인 볼륨 하나(컨테이너를 지워도 남는다 · 레포 밖) | CSV · dump 를 레포에 두지 않는다 |

```bash
# ① 포트 확인
lsof -nP -iTCP:18432 -sTCP:LISTEN
# ② PostgreSQL
docker run -d --name phub-medallion-pg \
  -e POSTGRES_USER=<USER> -e POSTGRES_PASSWORD=<PASSWORD> -e POSTGRES_DB=<DB> \
  -p 127.0.0.1:18432:5432 -v phub-medallion-pg:/var/lib/postgresql/data postgres:16
# ③ 스키마(기존 167 + 새 74) — backend/ 에서
DATABASE_URL=postgresql+asyncpg://<USER>:<PASSWORD>@127.0.0.1:18432/<DB> uv run alembic upgrade head
```

- `DATABASE_URL` 은 프로세스 env 로 준다 — `envs/.env` 에 다른 DB 가 적혀 있어도 프로세스 env 가 앞선다(`backend/README.md` 「실행」). 적재기는 시작 때 **접속 대상(호스트 · 포트 · DB 이름 — 비밀번호 빼고)** 을 찍는다.
- 한 DB 에 기존 167 테이블도 (빈 채로) 생긴다 — alembic 체인이 하나라 가를 수 없다(조사 §1-2). 새 테이블은 그 167 을 읽지도 쓰지도 않는다.

### 6-2. 적재

```bash
# backend/ 에서 — 경로는 로컬 $SM 의 gold · silver · notes
export DATABASE_URL=postgresql+asyncpg://<USER>:<PASSWORD>@127.0.0.1:18432/<DB>
export GOLD_CSV_DIR=<gold 폴더> GOLD_SILVER_DIR=<silver 폴더> GOLD_LEDGER_CHECK_PATH=<ledger-check-list.csv>
export GOLD_EXPECTED_HASH=8accbb213ac5327d8675f8156bc57d87c12a3245c383c8239074444da7f6228c
uv run python scripts/load_medallion.py --dry-run   # 검사 · 요약만
uv run python scripts/load_medallion.py             # 싣기
```

### 6-3. 허브를 DB 판으로

```bash
# backend/ 에서 — CSV 경로 env 넷은 필요 없다
GOLD_REPOSITORY=db \
DATABASE_URL=postgresql+asyncpg://<USER>:<PASSWORD>@127.0.0.1:18432/<DB> \
GOLD_EXPECTED_HASH=8accbb213ac5327d8675f8156bc57d87c12a3245c383c8239074444da7f6228c \
uv run uvicorn app.gold_main:app --host 127.0.0.1 --port <포트>
```

| 언제 | 포트 | 왜 |
|---|---|---|
| 허브끼리 대조(DE6) | 비어 있는 다른 포트(제안 18107 — 띄우기 전 `lsof` 확인) | 18105 의 CSV 판과 **나란히** 띄워 같은 요청을 양쪽에 보낸다 |
| 앱 대조(DE7 · 완료 조건) | **18105** | 앱이 18105 를 본다 — CSV 판을 내리고 같은 포트에 DB 판을 띄운다 |

확인: `…/procedure-hub/gold/health` 의 `build.gold_hash` · `build.aux_hash` 가 §2-5 의 두 값과 같다.

## 7. 시험 · 완료 조건

번호는 SPEC-001 · 002 의 T · E 와 겹치지 않게 `DT`(허브 단위 · 합성 · SQLite — CI 에서 돈다) · `DE`(로컬 실물 — PostgreSQL · `$SM`)로 단다.

### 7-1. 허브 단위(DT)

| # | 시험 | 기대 |
|---|---|---|
| DT1 | 모델 = 계약 | `Base.metadata` 에 새 테이블 74 · 이름 = §2 · 72표의 칸 = `load_seq` + 헤더 계약(순서까지) · 전부 문자열 · PK · FK 82 · 직접 지은 인덱스 30 · 유일 제약 3 · 이름 길이 ≤ 63 · 중복 0 · JSON 칸 0 · 판 칸 0 |
| DT2 | SQLite | `create_all` 이 새 74 를 포함해 성공한다 · 기존 시험 전부 그대로 통과(C2 · C6) |
| DT3 | revision | id 가 옛 3개와 다르다 · `down_revision` = `b202610300001` · 헤드가 하나다 |
| DT4 | 적재(합성) | 합성 fixture(가짜 코드 · 가짜 이름 — `tests/gold_fixture.py` 꼴 + silver 57표)를 SQLite 에 싣는다 → 표별 행 수 = 파일 행 수 · 빈칸 = NULL · `''` 0 · `load_seq` = 1…n · `medallion_build` 74행 · `medallion_ledger_check` = 뽑은 쌍 |
| DT5 | 적재 검사 실패 | V1 ~ V9 를 하나씩 깨뜨린 묶음 → exit 2 · DB 에 쓴 것 0(앞서 실어 둔 판이 그대로 — 빌드 기록 불변) |
| DT6 | 쓰기 중 실패 | 싣는 도중 실패를 넣는다 → exit 3 · 롤백 · 옛 판 그대로 |
| DT7 | dry-run | DB 접속 0 · 쓰기 0 · 요약에 해시 · 표별 행 수 |
| DT8 | 되읽기 | 72표를 `load_seq` 순으로 읽어 NULL → `''` 한 행 = CSV 행(값 · 순서) |
| DT9 | 입력 동치 | 같은 fixture 로 CSV 판 `LoadedInputs` = DB 판 `LoadedInputs`(§5-4 「입력」 줄 전부) |
| DT10 | 도구 응답 동치 | 기존 합성 도구 시험(도구 9 · REST · MCP)을 repository 두 판으로 돌린다 → 응답 JSON 이 같다(`build.loaded_at` 제외) |
| DT11 | DB 판 시작 실패 | F1 ~ F7 을 하나씩 → 시작 실패 |
| DT12 | 설정 | `GOLD_REPOSITORY` 기본 = `csv` · 모르는 값 → 시작 실패 · `db` 면 CSV 경로 env 넷 없이 뜬다 |
| DT13 | 값 불변 | fixture 에 여러 값 칸(` · `) · 칸 안 중복 조각 · 묶음 값 · 끝자리 0 소수 · 한 끝이 빈 다형 짝 · `order` 칸 · 전부 빈 칸 · 0행 표를 넣는다 → 왕복 뒤 글자 그대로 |
| DT14 | 요청 중 DB 0 | DB 판 허브가 시작 뒤 엔진을 닫았다 · 도구 요청을 처리하는 동안 쿼리 0 |
| DT15 | 읽는 범위 | DB 판이 읽는 표 = P5 의 것뿐 · 계층 3표에서 두 칸만 |

- fixture 에 회사 데이터 본문을 넣지 않는다(SPEC-001 §9 끝 줄과 같다).
- `test_gold_load.py:121` 은 `repo._m`(내부 색인)을 직접 본다(조사 §4-4) — P2 로 색인 코드가 같으므로 DB 판에서도 그대로 볼 수 있어야 한다(구현 확인 거리).

### 7-2. 로컬 실물(DE)

| # | 시험 | 기대 |
|---|---|---|
| DE1 | 빈 DB | 새 빈 PostgreSQL 에 `alembic upgrade head` → `alembic check` 통과 · `public` 테이블 241 · `downgrade -1` → `upgrade head` 가 다시 된다 · 지연 FK 가 `alembic check` 에서 어긋나지 않는다(O-6) |
| DE2 | dry-run | 72표 전부 통과 · 행 수 = §2-2 · §2-3 · `gold_hash` = `8accbb21…f6228c` · `aux_hash` = `6435fe41…1803a3` · 못 찾은 다형 참조 수(세기만 — `source_ref` 쪽은 0 · 조사 §2-2) |
| DE3 | 적재 | exit 0 · 74 테이블 행 수 = §2-9(합 129,527) · 되읽기 대조 차이 0 · `''` 0 · FK 위반 0 |
| DE4 | 다시 싣기 · 깨진 묶음 | 같은 묶음을 다시 → 같은 상태 · 헤더 한 칸을 바꾼 사본(레포 밖 임시 폴더) → exit 2 · 빌드 기록 불변 |
| DE5 | DB 판 `health` | `build.gold_hash` · `build.aux_hash` · `files[]` 22줄(`name` · `sha256` · `rows` · `kind`) · `integrity` 네 셈 · `aux` 가 CSV 판과 같다 |
| DE6 | 도구 응답 대조 | CSV 판(18105)과 DB 판(다른 포트)에 같은 요청 묶음을 보낸다 → JSON 이 같다. 요청 묶음 = 기존 gold 실물 시험이 보내는 요청 + 37 문항 답 키의 `calls[]` · 쪽을 끝까지 넘긴다. 기존 실물 pytest(`tests/test_gold_real.py` 등)도 DB 판으로 통과 |
| DE7 | **앱 37 키 대조 (나)** | 18105 를 DB 판으로 띄우고 앱에서 답 키 대조 (나) → **37 / 37 같음**(CSV 판에서 확인된 키와) |
| DE8 | 재기만 | DB 판 `load_ms` · 표별 읽기 시간(가장 큰 표 48,094행) · CSV 판 `load_ms` 와 나란히 기록 — 기준값을 정하지 않는다(조사 §6 4번을 닫는 셈) |

- DE 는 `$SM` 과 로컬 PostgreSQL 이 있어야 돈다 — CI 에는 없다(지금 실물 시험과 같다 · 조사 §4-4).
- DE7 의 앱 쪽 명령은 WORK 에서 앱 README · WORK-009 의 대조 절차를 따라 적는다(「키 (나)」 — _RESUME §5 11-17 「키 (나) 37 같음」).

### 7-3. 완료 조건

1. DT1 ~ DT15 통과 · `ruff` · 기존 시험 전부 통과(CSV 판 그대로).
2. DE1 ~ DE6 통과.
3. **DE7 — 로컬 DB 에 싣고 18105 를 DB 판으로 띄워 앱 37 키 대조 (나) 가 CSV 판과 같다.**
4. 레포에 CSV · dump · 접속 값이 들어가지 않았다(공개 금지 grep).

허브 브랜치의 push · PR · 머지는 완료 조건이 아니다 — 별도 승인이다.

## 8. SPEC-001 을 이렇게 바꿈

SPEC-001(0.6.0)은 이번에 고치지 않는다. 이 스펙이 승인되면 아래가 SPEC-001 의 다음 판에 되적을 목록이다.

| SPEC-001 자리 | 지금 | SPEC-003 뒤 |
|---|---|---|
| frontmatter `title` · §0 | 「메모리 적재」 | 「CSV 또는 DB 에서 읽어 메모리 색인」 |
| §1-2 1 | gold CSV 15 + … 를 시작 때 메모리로 적재 | 같다 — 원천이 CSV(`csv` 판) 또는 DB(`db` 판) |
| §1-3 「DB 적재 · alembic — 다음 범위」 | 범위 밖 | **SPEC-003 의 범위**(로컬). stg 쪽만 범위 밖으로 남는다 |
| §2-1 입력 표 | 파일 4종 | `db` 판의 입력 = §2 의 테이블(읽는 범위는 같다 — P5). X1 ~ X7 은 그대로 |
| §2-2 env | 필수 넷 | + `GOLD_REPOSITORY`(기본 `csv`). `db` 면 필수 넷 대신 `DATABASE_URL` · 적재기 env `GOLD_SILVER_DIR` |
| §2-3 1 | 시작 때 CSV 를 한 번 읽는다 | `db` 판은 DB 에서 한 번 읽는다. 「바뀌면 재시작」 은 같다 — 적재 → 재시작 → `health` 확인 |
| §2-3 2 ~ 4 | 파일마다 sha256 · 행 수를 시작 때 센다 | `db` 판은 **적재 때 센 값**을 빌드 기록에서 읽는다 — 식 · 값은 같다(§2-5) |
| §2-3 5 | 시작 실패 조건(env · 파일 · 헤더 · 기대 해시) | `db` 판 조건 F1 ~ F7 을 더한다. 헤더 대조는 적재기 V5 로 옮겨 간다 |
| §3 그림 「나중: DB 구현으로 교체」 | 열린 자리 | 「`db` 판 = 시작 때 DB → 같은 메모리 색인」 — 요청마다 SQL 이 아니다(D-6) |
| §3-1 끝 줄 「DB 로 가면 같은 키가 테이블 색인이 된다」 | 예고 | §2-8 표 — 속성 맞춤 색인 · 계층 자식 목록 · 하위 닫힘은 테이블 색인이 없다 |
| §4-8 `health` | `files[]` · `integrity` · `aux` | 그대로 + 어느 판인지와 DB 에 실은 시각을 싣는 필드(이름 제안 `repository` · `db_build{built_at, loader_version}` — O-7). `files[]` 는 두 판에서 같은 22줄이다 |
| §7 「DB 스키마 · alembic · 발행 테이블 — 버림(이번)」 | DB 없음(D2) | **옛 스키마는 그대로 버린다.** 새 스키마는 SPEC-003 §2 · §3 이다 |
| §8 stg · §10 O-7 · O-8 · O-11 | 열림 | **그대로 열림** — §9 로 모은다 |
| §9 T1 · T2 | CSV 적재 · 적재 실패 | `csv` 판은 그대로 · `db` 판은 DT4 ~ DT11 |
| §10 O-3 | `questions.csv` 를 해시에 넣는다(로컬 = (a)) | 그대로 — 빌드 기록에 `hash_only` 로 sha256 만(본문은 DB 에 없다) |

결정 기록 쪽: _RESUME §2 11-16 「D2 저장 = DB 없이 … DB화는 시험 뒤 다음 범위」 가 11-17 두 행으로 이어졌다 — CSV 판은 없어지지 않고 기본값 · 대조 기준으로 남는다(§5-1).

## 9. 다음 범위

이번에 만들지 않는다. 정해진 것이 아니라 **남은 질문**이다.

| # | 무엇 | 지금 아는 사실 | 누가 · 언제 |
|---|---|---|---|
| N-1 | **stg 진입점(D-7)** — gold 가 stg 에서 뜨는 자리 | stg 이미지는 `app.main:app` 하나만 띄운다(`Dockerfile:27`) · `gold_main` 은 별개 진입점이다. 테이블만 올리면 stg 에 gold API 는 없다(조사 D-7 · SPEC-001 O-7) · 「시작 때 읽기」 가 어느 lifespan 에 들어가는지가 여기에 달렸다 | **닫힘(0.2.0) — §11-1 · §11-2** — `app.main` 에 붙임 · 꺼진 채 기동 |
| N-2 | **stg 반입(시드)** — 원천 CSV 를 어디서 가져와 싣나 | 선택지 5(조사 D-5 · §3-3) · 허브 전례는 「마이그레이션은 자동 · 데이터는 사람이 gate 를 열고 따로」(조사 §1-6). 로컬에서 만든 적재 CLI 가 그대로 쓰일지는 여기서 정한다 | **닫힘(0.2.0) — §11-5 ~ §11-7** — 레포 `data/medallion/` · 같은 이미지 일회성 컨테이너 · 사용자가 VM 에서 직접 |
| N-3 | **stg 권한** — stg DB 역할이 새 테이블을 만들 수 있나 | 확인 안 됨(조사 §0-2 원천 질문 · §6 2번) | 보류(_RESUME §2 11-17 첫 행) |
| N-4 | **회사 데이터 범위** — silver 설명 글 · 가격 표를 stg 에 어디까지 올리나 | 확인 안 됨(조사 §0-2 원천 질문). D-1 (b) 는 로컬 기준이다 | 보류(같은 행) |
| N-5 | 마이그레이션이 stg · prod 로 가는 것 | 컨테이너가 뜰 때마다 `alembic upgrade head` 가 돈다 · stg → prod 승격 때 prod 에도 빈 테이블 74 가 생긴다 · 헤드를 올린 뒤에는 옛 이미지로 그냥 못 돌아간다 · prod 이름 전환 문서가 지금 헤드를 사전 점검에 박아 두었다(조사 §1-3 4 ~ 6) | stg 쪽은 §11-6 「되돌리기」 · §11-7 에서 다룸 · **prod 쪽은 열림**(§11-9 O-S6) |
| N-6 | 기본값을 `db` 로 · CSV 판을 남길지 | 이번은 기본 `csv`(§5-1) | **닫힘(0.2.0)** — 기본값은 `csv` 그대로 · stg 는 VM env 파일에 `GOLD_REPOSITORY=db` 한 줄(§11-2 · §11-7 ②) · CSV 판은 로컬 · 대조 기준으로 남는다 |
| N-7 | 요청마다 SQL · 다른 서비스가 SQL 로 직접 읽는 계약 | 지금 방식은 DB 를 「보관 · 배포 수단」 으로만 쓴다(조사 D-6 위험) · 코어 전체를 async 로 다시 써야 한다(조사 §4-3 (b)) | 다른 소비자가 생길 때 |
| N-8 | 정규화(수 타입 · 여러 값 칸 · gold → silver FK) · 판 쌓기 | 걸리는 칸 전수는 조사 §2-5 · 판 쌓기는 옛 판이 한 방식(조사 §5 4번) | 필요가 생길 때 |
| N-9 | 접근 제어 | SPEC-001 O-11 그대로 | **열림** — §11-9 O-S5 |
| N-10 | LLM 을 SDK 로 | _RESUME §2 11-16 「D8 … DB화 때 SDK 로」 — 이 스펙은 허브 DB 만 다룬다. 앱 · 채팅 단계의 일이다 | 채팅(상담) 단계 |
| N-11 | `concern_site` 의 근거(`source_ref` 574행)를 되짚는 도구 | 지금 도구로 닿지 않는다(조사 §2-3) — DB 에는 `s_concern_site` 와 그 `s_source_ref` 행이 함께 있다 | 필요가 생길 때 |

## 10. 열린 것

### 10-1. WORK 전 사용자 결정(둘)

「추천으로」 한 마디면 본문 그대로 닫힌다. §1-2 의 「정해진 것」 은 여기 다시 올리지 않았다.

| # | 정할 것 | 선택지 | 추천 | 근거 · 셈 |
|---|---|---|---|---|
| **U-1** | **빈칸을 무엇으로 싣나 — FK 를 거나와 한 묶음이다** | (a) 빈칸 = **NULL** · silver FK 80 + `g_edge` 2 를 건다(본문) (b) 빈칸 = **`''`**(`NOT NULL DEFAULT ''`) · FK 0 — 관계는 글자로만 | **(a)** | FK 80칸 가운데 35칸에 빈칸이 있어(빈 값 12,968) 둘을 따로 고를 수 없다(§2-6). (a) 는 D-1 을 「silver 전부」 로 정한 근거(DB 안에서 관계가 닫힌다)를 실제로 세우고, 깨진 FK 가 지금 0 이라 걸리는 행이 없다. 읽을 때 NULL → `''` 한 줄이 들고 CSV 에는 빈칸 표기가 하나뿐이라 값이 달라지지 않는다(DT8 이 왕복을 대조한다). (b) 는 조사 초안(§2-4)의 꼴이고 서비스 코드의 `""` 비교와 글자가 같지만 silver 를 다 올리고도 DB 가 관계를 모른다 |
| **U-2** | **로컬 PostgreSQL 을 무엇으로 띄우나** | (a) Docker `postgres:16` · `127.0.0.1:18432` · 이름 붙인 볼륨(본문) (b) 이 기계의 Homebrew `postgresql@17` 에 새 DB · 포트는 그쪽 설정대로 | **(a)** | CI · 리허설과 같은 판(16)이고 지우면 흔적이 없다 · 포트를 우리가 고른다. (b) 는 컨테이너가 필요 없지만 판이 17 이고 다른 로컬 작업과 인스턴스를 나눠 쓴다. 띄우는 것은 코디다(§6) |

### 10-2. 열린 것

「추천」 은 이 워커의 추천이고 결정이 아니다. 상태 말은 SPEC-001 §10 과 같다.

| # | 열린 것 | 선택지 | 추천 | 상태 |
|---|---|---|---|---|
| O-1 | `load_seq` 를 어디에 두나(R4) | (a) 72표 전부(본문) (b) 순서가 응답에 쓰이는 표만(gold 15 + `s_source_ref`) + 키 없는 `s_alias` (c) 두지 않고 키로 정렬 | **(a)** — 규칙이 하나이고(적재기 · 모델이 표를 가리지 않는다) 72표 전부를 「DB → CSV 행」 으로 되읽어 대조할 수 있다(DT8). (c) 는 글자 정렬이 DB 정렬 규칙을 타고, 「파일 순서 = 키 순서」 가 계약이 아니다 | 구현 때 정함(본문 = (a)) |
| O-2 | 지울 때 `DELETE` 인가 `TRUNCATE` 인가(§4-4 L2) | `DELETE`(SQLite 에서도 같다 · 읽는 쪽을 막지 않는다) / `TRUNCATE`(PostgreSQL 전용 · 빠르나 읽는 쪽이 기다린다) | `DELETE` — 13만 행이라 비용이 작고 C7 을 지킨다 | 구현 때 정함 |
| O-3 | 빌드 기록의 꼴(§2-5) | (a) 표 1 · 한 행 = 파일 · 판 값은 행마다(본문) (b) 표 2(판 1행 + 파일 n행 — 조사 §2-4 초안) (c) 표 1 · 판 1행 · 파일 목록은 JSON 칸 | **(a)** — 지시서 D-4 「표 1개」 와 R7 「JSON 칸 0」 을 함께 지킨다. 판 값이 행마다 되풀이되는 것은 F3 이 지킨다. (b) 가 더 반듯하지만 표가 75 가 된다 | 구현 때 정함(본문 = (a)) |
| O-4 | silver 57 전체 해시를 따로 기록하나 | 두지 않음(본문 — 빌드 기록 57줄로 다시 셀 수 있다) / 칸을 더한다 | 두지 않음 — 응답 머리 · cursor 의 build 는 (`gold_hash`, `aux_hash`) 그대로다(SPEC-001 §2-3 4). 허브가 읽지 않는 silver 52표가 바뀌어도 응답은 안 바뀐다 | 구현 때 정함 |
| O-5 | gold → silver 홑 칸 FK(`g_adverse_detail.adverse_risk_id` · `*_code` 칸)를 거나 | 걸지 않음(본문) / 값이 한 표만 가리키는 칸만 건다 | 걸지 않음으로 시작 — 어느 칸이 「늘 한 표」 인지는 gold-build 의 약속이지 이 문서가 셈으로 정할 것이 아니다(두 값이 든 코드 칸이 이미 있다 — §2-6). 실은 뒤 SQL 로 깨진 참조를 세어 보고 정한다 | 1회차 뒤 |
| O-6 | 지연 FK 가 `alembic check` · SQLite `create_all` 에서 괜찮은가 · 모델에 없는 테이블을 `alembic check` 가 잡는가 | 지연 FK(본문) / 지연 없이 의존 순서대로 싣기(자기 참조 11칸은 한 문장으로 싣거나 부모 먼저) | 지연 FK — 안 되면 뒤 선택지 | **확인 안 됨** — WORK 첫 WP 에서 로컬 PostgreSQL 로(DE1) |
| O-7 | 이름 — 테이블 `medallion_build` · `medallion_ledger_check` · 칸 `load_seq` · env `GOLD_REPOSITORY` · `GOLD_SILVER_DIR` · 스크립트 `load_medallion.py` · 모델 파일 `medallion.py` · silver 계약 상수 자리 · revision id `b202611170001` · exit 3 · `health` 의 새 필드 | 본문 제안 / 다른 이름 | 본문 그대로 — 기존 167 · 옛 브랜치 이름과 겹침 0(재셈) | 구현 때 정함 |
| O-8 | 표 내용 해시(행을 정규화해 센 값)를 빌드 기록에 더하나 | 두지 않음(본문) / 둔다(허브 전례 — 조사 §3-2) | 두지 않음 — 로컬에서는 L5 의 되읽기 대조가 같은 일을 한다. stg ↔ 로컬을 견줄 때(N-2) 다시 본다 | 뒤 단계 |
| O-9 | 두 적재기가 동시에 도는 것 · 적재 중 허브가 뜨는 것 | 막지 않음(본문 — P8 · F7 이 섞인 판을 막는다) / 잠금을 둔다 | 막지 않음 — 로컬 한 사람이다 | 구현 때 정함 |

## 11. stg 판 — gold 를 `app.main` 에 붙임 · 일회성 적재(0.2.0)

「조사」 = `$W/research-stg-seed.md`(허브 `fdc155b` 기준). 줄 번호는 `$H` `fdc155b` 에서 이 워커가 읽은 것이다(읽기만). 이 절에는 호스트 주소 · 계정 · 접속 값을 적지 않는다 — 명령은 `<…>` 자리표시로만 적는다.

### 11-0. 정해진 것 · 지금 판의 수

| # | 정해진 것 | 근거 | 이 절에서 |
|---|---|---|---|
| S-4 | **stg 의 gold = `app.main` 에 붙임**(조사 S-4 (b) + (c)) — 별도 컨테이너 · Gateway 경로 · 인프라 레포 변경 0 · 표가 비었거나 적재 전이면 gold 만 꺼진 채 `app.main` 은 정상 기동 · 켜기 = 적재 뒤 컨테이너 재시작 | _RESUME §2 11-18 「stg gold = app.main 에 붙임」 | §11-1 ~ §11-4 |
| 시드 | **stg 시드 = 일회성 적재** — 원천은 허브 레포 · stg 는 배포 때 `alembic upgrade head`(새 표 76 · 기존 167 안 건드림) → 적재기 dry-run → 한 트랜잭션 적재 | _RESUME §2 11-18 「stg 시드 = 일회성 적재」 | §11-6 · §11-7 |
| S-1 | 레포 데이터 폴더 = 루트 `data/medallion/` | 같은 행 「코디 기본값」 · 조사 S-1 | §11-5 |
| S-2 | 산출물만 넣는다 — 생성 스크립트는 안 넣음 | 같은 행 · 조사 §1-4 의존 실측 | §11-5 |
| S-3 | 적재기를 이미지에(Dockerfile 한 줄) · 데이터는 안 실음 | 같은 행 · 조사 S-3 (b) | §11-6 |
| S-5 | 원장 JSON 21 을 넣는다 | 같은 행 · 조사 S-5 · _RESUME §2 11-17(공개 정보) | §11-5 |
| S-6 | **VM 작업은 사용자가 직접**(Bastion · 일회성 적재 · 재시작) — 코디는 명령 절차서 | 같은 행 | §11-7 |
| S-7 | 그림 서빙은 다음 스펙 | 같은 행 | 범위 밖 |
| 배포 | 이번 판은 배포로 닫는다 · 단계마다 성공하면 바로 다음 · 막히거나 실패 · 위험할 때만 사용자 | _RESUME §2 11-18 「배포로 닫는다」 · 「승인 없이 이어서」 | §11-7 「멈출 곳」 |

지금 판의 수(§0 ~ §10 의 74 를 대신한다 — SPEC-007 · WORK-015 · `impl-data-v07-report.md` · 이 워커가 `$SM` 으로 다시 셈):

| 무엇 | 값 |
|---|---|
| 새 테이블 | **76** = gold 15 + silver 59(57 + 그림 2표 `s_concept_image` · `s_concept_image_label`) + `medallion_ledger_check` + `medallion_build` |
| 행 | **130,446** = 데이터 130,097(gold 62,244 + silver 67,853) + 원장 확인 273 + 빌드 기록 76 |
| alembic 머리 | `b202611170002`(down `b202611170001` → down `b202610300001` = `origin/stg` 머리 · 갈림 0 — 조사 §1-2) |
| `gold_hash` | `8accbb213ac5327d8675f8156bc57d87c12a3245c383c8239074444da7f6228c`(gold 폴더 16 파일 — 재셈 같음) |
| `aux_hash` | `93ec89fdd7d66781cdf18025c4698cc31a543fe252ebb1f16948fc0876ae0eeb`(보조 6 파일 — 재셈 같음) |
| 적재기 판 | `load_medallion 0.2.0` · `health.files[]` 22 줄 |

### 11-1. D-7 닫음 — 진입점

| # | 정한 것 | 근거 |
|---|---|---|
| E1 | **gold REST · MCP 를 `app.main` 에 붙인다.** 경로는 gold 설정 기본값 그대로 — REST `GOLD_API_PREFIX` = `/procedure-hub/gold`(도구 9 + `health`) · MCP `GOLD_MCP_MOUNT_PATH` = `/procedure-hub/gold-mcp`(끝점 `/procedure-hub/gold-mcp/mcp`). 두 env 로 바꿀 수 있는 것도 그대로다 | `app/modules/gold/config.py`(`GOLD_API_PREFIX` · `GOLD_MCP_MOUNT_PATH` 기본값) · Gateway 는 `/procedure-hub/*` 를 이 컨테이너로 보낸다(조사 §1-1) — 경로 하나 더할 일 0 |
| E2 | **응답은 `gold_main` 과 같다** — 도구 9 · 오류 3 · 쪽 넘김 · `Server-Timing` 머리. 켜진 gold 의 JSON 은 같은 요청이면 두 진입점에서 같다(`build.loaded_at` · `health.load_ms` 제외 — §5-4 와 같은 제외) | SPEC-001 §4 · `gold_main.py:48-92` |
| E3 | **gold 는 `app.main` 의 OpenAPI 에 넣지 않는다** — 하위 앱으로 붙인다. 그래서 공개 계약 시험(`tests/test_public_api_contract.py` — 공개 operation 42 · 해시 · 태그 6)이 **한 글자도 안 바뀐다.** gold 문서 화면은 지금 자리 그대로(`<GOLD_API_PREFIX>/api-docs` · `/redoc` · `/openapi.json`) | `test_public_api_contract.py:229-248`(`app.openapi()` 의 `/procedure-hub/` 경로를 전부 세어 대조 · 태그 집합 대조) · 「기존 API 불변」(_RESUME §2 11-18) |
| E4 | `app.main` 의 기존 것은 **불변** — 기존 라우터 · `/procedure-hub/health` · `/procedure-hub/health/config`(본문 열쇠까지) · 미들웨어 순서 · lifespan 의 DB 확인 · 시작 실패 조건(DB 확인 실패). `app.main` 의 `health` 에 gold 정보를 넣지 않는다 | `app/core/app_factory.py:28-66` · `app/core/lifespan.py` · `app/router/health.py` · CD 가 `health` · `products` 를 본다(조사 §1-1) |
| E5 | `app.main` 의 미들웨어(요청 로그 · CORS)는 붙인 gold 요청에도 걸린다 — 응답 **본문**은 바뀌지 않고 CORS 머리가 더해진다(`gold_main` 에는 CORS 가 없다). 계약 차이로 보지 않는다(O-S9) | `app_factory.py:45-53` · `gold_main.py:62-79` |
| E6 | **`app.gold_main` 은 남긴다** — 로컬 단독 실행용 · 동작 같음(적재 실패 = 시작 실패 그대로 · `GOLD_REPOSITORY` 모르는 값 = 시작 실패 그대로 · DB 연결 없이 뜸). 두 진입점은 **같은 조립 코드**를 쓴다(조립을 두 벌 두지 않는다) — 다른 것은 「적재 실패를 시작 실패로 올리나(gold_main) · 꺼짐으로 받나(app.main)」 하나 | 브리프 · `gold_main.py:1-6` · `tests/test_gold_rest.py:74-78`(`gold_main` 이 `app.core.tx` · `app.core.db` 를 import 하지 않는다 — 그대로 지킨다) |
| E7 | `tests/test_gold_rest.py:81-87` `test_app_main_untouched`(「`app/main.py` · `app/core` 가 release 와 같다」)는 이 결정으로 뜻을 잃는다 → **지운다.** 대신 §11-8 ST5(공개 계약 · 기존 `health` 불변)가 지킨다 | 0.1.0 의 「`app.main` 과 별개」 전제가 바뀌었다 |

### 11-2. 기동 규칙 — 켜짐 · 꺼짐

`app.main` 의 lifespan 순서: **기존(로깅 → DB 확인) → gold 적재 → MCP 세션 관리 시작 → 요청 받음.** gold 적재는 `gold_main` 과 같은 길이다(§5-2 — 시작 때 한 번 · 자기 엔진 · 읽고 닫음 · 요청은 메모리만). **gold 적재에서 무엇이 나든 `app.main` 은 시작 실패하지 않는다** — gold 만 꺼진다.

| `GOLD_REPOSITORY` | 상태 | gold | 꺼짐 이유(§11-3 본문 · 로그) |
|---|---|---|---|
| `db` | `medallion_build` 행 있음 · F1 ~ F7 통과 | **켜짐** | — |
| `db` | `medallion_build` 0행(새 표만 있고 적재 전) | 꺼짐 | `F2 medallion_build 0행 — 적재 먼저` |
| `db` | 새 표 없음 · `DATABASE_URL` 없음 · 접속 · 읽기 실패 | 꺼짐 | `F1 …` |
| `db` | 판 값 어긋남 · 해시 재셈 어긋남 · 행 수 어긋남 · 읽는 동안 바뀜 | 꺼짐 | `F3` · `F4` · `F5` · `F7 …` |
| `db` | `GOLD_EXPECTED_HASH` 가 있는데 `gold_hash` 와 다름 | 꺼짐 | `F6 …` |
| 비었음 · `csv` | CSV 경로 env 넷 있음 · 파일 · 헤더 계약 통과 | 켜짐(CSV 판) | — · **로컬 전용**(stg 이미지에는 CSV 가 없다 — 조사 §1-3) |
| 비었음 · `csv` | CSV 경로 env 없음(stg 에 `db` 를 안 줬을 때 · CI 기본) | 꺼짐 | CSV 판 「필수 env 없음」 문구 그대로 |
| 그 밖의 값 | — | 꺼짐 | `모르는 GOLD_REPOSITORY …`(`gold_main` 은 시작 실패 — 그대로) |
| 무엇이든 | 위에 없는 예외 | 꺼짐 | **예외 종류 이름만**(글은 싣지 않는다 — 접속 값이 섞일 수 있다) |
| 무엇이든 | lifespan 이 아직 안 돌았다(시험의 ASGITransport 꼴 등) | 꺼짐 | `시작 적재 전` |

- **stg 는 `db` 만 쓴다** — VM env 파일에 `GOLD_REPOSITORY=db` 한 줄을 둔다(§11-7 ②). 기본값은 `csv` 그대로다(§5-1 — CSV 판은 로컬 · 대조 기준으로 남는다). 그래서 stg 에 그 한 줄이 없으면 gold 는 꺼진 채 뜬다(기존 허브는 그대로).
- 꺼짐 이유 글은 `GoldLoadError` 문구에서 온다. 그 밖의 예외는 종류 이름만 쓴다(위 표). **0.2.1(검수 R-1)**: F1 문구 끝에는 접속 대상(`· <방언> host=… port=… db=…`)이 붙으므로 **503 본문 · gold `health` 본문에는 F 코드 + 짧은 사유만** 싣고(`assembly.py` `public_reason` — 대상 꼬리를 자르고, 꼴이 바뀌어 `://` · `host=` 가 남으면 첫 낱말인 F 코드만) **대상은 서버 로그에만** 둔다.
- 켜졌을 때의 시작 로그 한 줄은 지금 그대로(`gold repository=db target=<호스트 · 포트 · DB 이름> gold_hash=…` — `gold_main.py:38-45`). 꺼졌을 때 **경고 한 줄** `gold off reason=<이유>` 를 남긴다.
- 적재가 끝나야 요청을 받는다(지금 `gold_main` 과 같다). 로컬 실측 DB 판 `load_ms` 821(DE8 — 모델 import 포함 · `read_db_inputs` 단독 343) · stg(원격 PostgreSQL · TLS) 시간은 **확인 안 됨** — §11-7 ⑦ 에서 잰다(O-S4).
- **0.2.1(검수 R-2) 시간 한도** — `app.main` 쪽 적재는 **lifespan 안(yield 앞)** 에서 `GOLD_LOAD_TIMEOUT_SECONDS`(기본 60 · SPEC-001 §2-2) 한도로 감싼다. 적재는 **데몬 스레드**(자기 이벤트 루프)에서 돌고 메인 루프는 `asyncio.wait_for` 로 기다린다 — 한도를 넘으면 gold 만 꺼짐(이유 `적재 시간 초과(<n>s)`)이고 `app.main` 은 뜬다 · 스레드는 프로세스 종료를 붙잡지 않는다(`assembly.py` `load_soft` · `_in_daemon_thread`). 한도 안에 성공했을 때만 가드를 연다. `gold_main` 에는 한도가 없다(그대로). 한도 동안은 `app.main` 전체가 요청을 받지 않으므로 값은 CD 확인 창보다 짧게 둔다 — stg 는 `30`(§11-7 실측).
- **0.2.1 켜짐 판정 = `GET <GOLD_API_PREFIX>/health` 가 `200`** 이다. 로그만 보지 않는다 — 한도를 넘긴 뒤에도 데몬 스레드의 적재는 끝까지 돌아 `gold repository=db … gold_hash=…` 줄을 찍을 수 있지만 가드는 닫힌 채다(코드 검수 C-2). `gold off reason=` 줄이 있으면 뒤따르는 그 줄은 켜짐이 아니다.
- 시작 때 한 번만 판정한다 — 떠 있는 동안 꺼짐 ↔ 켜짐이 바뀌지 않는다. 바꾸는 길은 재시작뿐이다(§11-4).

### 11-3. 꺼진 gold 의 응답

| 어디 | 꺼졌을 때 | 켜졌을 때 |
|---|---|---|
| REST `<GOLD_API_PREFIX>/*` 전부(**`health` 포함**) | **`503`** · `{"detail": "unavailable: gold 꺼짐 — <이유>"}` — `<이유>` = F 코드 + 짧은 사유만(0.2.1 · R-1 — §11-2) | SPEC-001 §4 그대로 |
| MCP `<GOLD_MCP_MOUNT_PATH>/*` | **HTTP `503`** · 같은 본문(세션 · 도구 목록을 내지 않는다) | SPEC-001 그대로 |
| `app.main` 의 다른 경로 | 그대로 | 그대로 |

- 꼴은 SPEC-001 §4-0 오류 표와 같다 — `{"detail": "<코드 이름>: <사유>"}`(`errors.py:1-5`). **새 코드 `unavailable` · REST `503`** 은 SPEC-001 0.8.2 오류 표 넷째 줄로 되적었다(O-S1 닫힘).
- 왜 `503` 인가 — 경로는 있고 지금 못 낸다. 부르는 쪽(앱)이 「행 0」(`200` · 빈 목록 — SPEC-001 §4-0)과 「gold 가 안 떴다」 를 가를 수 있어야 한다. `404` 는 「그 대상이 gold 에 없다」(`not_found`)와 겹친다.
- 왜 MCP 를 도구 오류가 아니라 HTTP `503` 으로 막나 — 꺼진 상태에는 도구 계약(색인)이 없다. `initialize` 부터 막아 클라이언트가 「붙었다」 고 착각하지 않게 한다(제안 — O-S2).
- 켜짐 확인 = `GET <GOLD_API_PREFIX>/health` 가 `200` 이고 `build.gold_hash` · `build.aux_hash` 가 §11-0 값과 같다(로그 줄로 판정하지 않는다 — §11-2).
- **0.2.1 MCP 허용 호스트** — MCP 는 DNS rebinding 보호를 켠 채 Host · Origin 허용 목록을 쓴다(SPEC-001 §2-2 `GOLD_MCP_ALLOWED_HOSTS` · `GOLD_MCP_ALLOWED_ORIGINS`). 가드(503)가 Host 검사보다 앞이라 꺼짐 때는 Host 와 무관하게 503 이다. 켜진 뒤 목록 밖 Host 는 `421` 이다 — stg 는 **두 값**을 둔다: Gateway 공개 호스트와 `<백엔드 내부 주소>:<포트>`(Gateway 가 Host 를 백엔드 내부 주소로 바꿔 넘긴다 — 공개 호스트만 두면 421 · 실측). 확인 = 컨테이너 로그의 `Invalid Host header`.

### 11-4. 켜기 · 끄기 · 갱신

| 일 | 하는 것 | 주의 |
|---|---|---|
| **켜기** | 적재(§11-6) 뒤 **컨테이너 재시작**(`docker restart <컨테이너>`) | 시작 명령이 `alembic upgrade head` 를 다시 돈다 — 이미 머리라 할 일 0(`Dockerfile:27`) → `app.main` + gold 적재 |
| VM env 파일을 고친 값 | `docker restart` 로는 **안 읽힌다** — env 파일은 컨테이너를 만들 때 읽힌다(조사 §1-1 「`--env-file`」) | 그래서 `GOLD_REPOSITORY=db` 는 **stg 배포(CD)가 컨테이너를 새로 만들기 전에** 넣는다(§11-7 ②). 배포 뒤에 넣었다면 컨테이너를 새로 만들어야 한다(`deploy.sh` — 인프라 스크립트 · 사용자). **0.2.1 실측**: env 를 고친 뒤 재생성 = **Bastion 의 배포 스크립트**(`./deploy.sh procedure-hub stg`) — `docker restart` 아님 |
| **끄기**(gold 만 되돌리기) | VM env 파일에서 `GOLD_REPOSITORY` 줄을 빼고 컨테이너를 새로 만든다 → 꺼짐(CSV env 없음) | 표 · 데이터는 그대로 둔다. 기존 허브 동작으로 돌아가는 가장 짧은 길이다(옛 이미지로 돌아가지 않는다 — §11-6 「되돌리기」) |
| **갱신**(다음 gold 판) | 레포 `data/medallion/` 갱신 PR → 머지(루트 `data/` 는 CD 를 안 돌린다 — 스키마가 같으면 이미지 재배포 0) → VM 반입 폴더에 새 판 → dry-run → 적재 → 재시작 → `health` 해시 | 스키마가 바뀌는 판은 새 revision → stg 배포 → 적재(조사 §1-7) |

### 11-5. 레포 데이터 폴더 — `data/medallion/`

```text
data/medallion/                      ← 레포 루트(backend/ 밖 · assets/procedure-images/ 와 같은 층)
  README.md                          판 · gold_hash · aux_hash · 파일 수 · 행 수 · 만든 곳 · 적재 명령 꼴 · 「손으로 고치지 않는다」
  silver/                            silver CSV 59   (적재기 GOLD_SILVER_DIR)
  gold/                              g_*.csv 15 + questions.csv = 16   (GOLD_CSV_DIR)
  notes/ledger-check-list.csv        원장 확인 목록 1   (GOLD_LEDGER_CHECK_PATH)
  bronze/phub-ledger/                원장 JSON 21 + README.md · CHANGELOG.md · HASHES.txt = 24   (적재기는 안 읽음)
```

| # | 정한 것 | 근거 |
|---|---|---|
| R-D1 | 자리 = 루트 `data/medallion/`. **build context 밖**(루트 `.dockerignore` 가 `**` 로 다 빼고 `backend/` 만 되살린다) · **BE CI · CD 트리거 밖**(`backend/**` 에만 반응) · `.gitignore` 영향 0 · LFS 필요 없음(합 약 13.4MB · 가장 큰 파일 `source_ref.csv` 4.15MB) | 조사 §1-4 · `.dockerignore:1-12` |
| R-D2 | **gold 폴더에는 CSV 16 개만** — `questions.csv` 는 적재하지 않지만 `gold_hash` 식에 들어가므로 같이 둔다(§2-5 · `hash_only`). gold · silver 폴더에 `.py` · `.md` 같은 다른 파일을 두지 않는다(gold 폴더의 계약 밖 CSV 는 해시에 들고 · silver 폴더의 계약 밖 CSV 는 V3 거부) — `README.md` 는 `data/medallion/` 바로 밑에만 | `inputs.py:117-120` · §4-3 V3 · 조사 §1-4 끝 줄 |
| R-D3 | 원천 = 로컬 메달리온 작업 공간의 지금 판(`$SM/silver` · `$SM/gold` 의 CSV · `$SM/notes/ledger-check-list.csv` · 원장 폴더). **바이트 그대로 복사**한다 — 고치면 해시가 바뀐다 | §2-5 「해시는 파일 바이트」 |
| R-D4 | **생성 스크립트는 넣지 않는다**(S-2). `gold-check` · `silver-supplement` · `silver-image` 는 레포 밖(archive · drafts · 시드)에 기대 레포 안에서 돌지 않는다 · `gold-build` 만 넣으면 검사 없는 빌드만 들어온다 | 조사 §1-4 「만드는 스크립트」 표 |
| R-D5 | `README.md` 에 적는 것: 판 이름(silver v07 · gold 11-16 판) · `gold_hash` · `aux_hash` · 폴더별 파일 수 · 표 76 · 행 130,446 · 「만든 곳 = 레포 밖 메달리온 작업 공간(gold-build · silver-check 등)」 · 적재 명령 꼴(§11-6 · 자리표시) · 「값을 손으로 고치지 않는다 — 고침은 원천에서 다시 지어 통째로 바꾼다」 · 그림은 `assets/procedure-images/`. **개인 경로 · 개인 레포 주소 · 접속 값은 적지 않는다** | 조사 §1-4 추천 배치 · 회사 레포 |
| R-D6 | 판은 한 벌만 둔다(`data/medallion/<판>/` 로 쌓지 않음) — DB 에도 한 판뿐이고 옛 판은 git 이력이 가진다 | 조사 §1-4 · D-4 |
| R-D7 | 같이 고칠 문서 두 줄: `backend/README.md` 의 「데이터는 저장소에 넣지 않고 경로를 env 로」(gold 절) → 「레포 `data/medallion/` · 적재기 기본 경로 · 서버 CSV 판은 여전히 env」 · `assets/procedure-images/README.md` 의 대조 표에 데이터 폴더 자리 한 줄 | 조사 §1-4 「문서 충돌」 · D-5 「레포에 CSV 커밋 금지」(0.1.0 로컬 판)는 **이 결정으로 바뀐다**(_RESUME §2 11-18 「원천은 허브 레포」) |

### 11-6. 적재기 — 이미지 포함 · 기본 경로 · 일회성 실행 · 되돌리기

**이미지 포함**(S-3)

| # | 정한 것 | 근거 |
|---|---|---|
| I-1 | `backend/Dockerfile` 의 runtime 단계에 **한 줄** — `COPY backend/scripts/load_medallion.py scripts/load_medallion.py`. **데이터는 싣지 않는다**(`data/` 는 build context 밖) | 조사 §1-3 · `Dockerfile:19-22`(같은 단계의 운영 스크립트 3) · ADR 0004 「startup seed · data-init image 기각」 과 부딪히지 않는다(이미지에 데이터 0 · 시작 때 쓰기 0 — 서버는 읽기만) |
| I-2 | `.dockerignore` 는 **고치지 않는다** — `!backend/` 가 backend 를 통째로 context 에 넣는다(화이트리스트에 없는 `prepare_legacy_prod.py` 를 `Dockerfile:22` 가 이미 COPY 한다). WORK 에서 로컬 빌드로 확인하고, 안 되면 `!backend/scripts/load_medallion.py` 한 줄 | 조사 §1-3 「참고」 |
| I-3 | 적재기가 import 하는 것(`app.modules.gold.*` · `app.model.medallion` · asyncpg · sqlalchemy)은 이미 이미지에 있다 — 더할 의존성 0 | 조사 §0-4 |

**기본 경로**

| # | 정한 것 |
|---|---|
| I-4 | 적재기는 경로 env 셋이 **비었을 때만** 기본값을 쓴다 — 루트 = `backend/` 의 부모 · `GOLD_CSV_DIR` = `<루트>/data/medallion/gold` · `GOLD_SILVER_DIR` = `<루트>/data/medallion/silver` · `GOLD_LEDGER_CHECK_PATH` = `<루트>/data/medallion/notes/ledger-check-list.csv`. env 가 앞선다 |
| I-5 | 로컬(레포)에서는 루트 = 레포 루트 · **이미지 안에서는 `backend/` 가 `/app` 이라 루트 = `/`** → `/data/medallion/…`. 그래서 일회성 컨테이너는 데이터 폴더를 `/data/medallion` 에 읽기 전용으로 꽂으면 경로 env 가 필요 없다 |
| I-6 | `GOLD_IMAGE_DIR` 는 기본값을 두지 않는다 — SPEC-007 그대로(주면 V13 · 없으면 건너뜀 + 요약 한 줄). stg 절차는 명시로 준다(§11-7 ⑤) |
| I-7 | 기본값은 **적재기에만** 둔다. 서버(`GoldSettings` 의 CSV 판)에는 경로 기본값을 두지 않는다(`config.py` 머리말 「경로 기본값을 코드에 두지 않는다」 그대로) |
| I-8 | 요약 첫 줄에 쓴 경로 셋과 그 출처(env · 기본)를 찍는다 — 파일 이름 · 경로만(값 본문 · 접속 값 0) |

**일회성 실행 꼴**(같은 이미지 · `docker run --rm` — 조사 §1-3 ⓑ · `deployment.md` 의 alembic · 반입 CLI 전례와 같은 꼴 · `<IMG>` = `<레지스트리>/procedure-hub-api:stg-<커밋 sha>`)

```bash
# DATABASE_URL 은 VM env 파일에서(GOLD_REPOSITORY 도 들어 있지만 적재기는 읽지 않는다) · 경로 셋은 기본값(I-5)
docker run --rm \
  --env-file <VM env 파일> \
  -v <반입 폴더>/data/medallion:/data/medallion:ro \
  -v <반입 폴더>/assets/procedure-images:/assets/procedure-images:ro \
  -e GOLD_IMAGE_DIR=/assets/procedure-images \
  -e GOLD_EXPECTED_HASH=<§11-0 gold_hash> \
  --entrypoint .venv/bin/python \
  <IMG> scripts/load_medallion.py --dry-run
# 적재는 같은 명령에서 --dry-run 만 뺀다
```

| env | 어디서 | 뜻 |
|---|---|---|
| `DATABASE_URL` | VM env 파일(손으로 치지 않는다) | 적재만 필수 · dry-run 은 접속하지 않는다 |
| `GOLD_EXPECTED_HASH` | `-e` | 주면 V9 — 다르면 exit 2(쓴 것 0) |
| `GOLD_IMAGE_DIR` | `-e` | 주면 V13 — 그림 103 ↔ `s_concept_image` |
| `GOLD_CSV_DIR` · `GOLD_SILVER_DIR` · `GOLD_LEDGER_CHECK_PATH` | 안 줌(기본 경로 — I-5) | 주면 env 가 앞선다 |

exit: **0** 성공(dry-run = 검사 통과) · **2** 입력 · 검사 · 접속 · 표 없음(L1) — DB 에 쓴 것 0 · **3** 쓰기 · 되읽기 · 커밋 실패 — 롤백 · 이전 판 그대로(§4-5 · `load_medallion.py:8-9`).

**되돌리기**

| 상황 | 하는 것 |
|---|---|
| exit 2 | 쓴 것 0 — 원인(데이터 · env · 표 없음)을 고치고 다시 dry-run |
| exit 3 | 트랜잭션 롤백 — **이전 판 그대로**(처음이면 빈 표 그대로 → gold 는 계속 꺼짐 · 기존 허브 영향 0) |
| 판을 되돌림 | 앞 판 `data/medallion/`(git 이력의 앞 커밋)으로 같은 적재를 다시 → 재시작 |
| 스키마 | **`alembic downgrade` 를 쓰지 않는다** — 11-17 로컬 사고(워커 `downgrade -1` 이 표를 내림 · `impl-data-v07-report.md` 사고 1건) |
| 런타임(이미지) | **옛 이미지(`:stg-rollback`)로 돌아가지 않는다** — 옛 이미지는 `b202611170002` 를 몰라 시작 때 `alembic upgrade head` 가 실패할 수 있다(조사 §1-7 · 실물 확인 안 됨). gold 문제면 §11-4 「끄기」 · 코드 문제면 앞으로 고쳐 다시 배포 |

### 11-7. stg 반입 절차서 — 사용자가 VM 에서 직접

전제: 허브 PR 이 `release/v1.2.0` 에 머지됐다(CI = PostgreSQL `alembic upgrade head` + `alembic check` · ruff · pytest SQLite 통과). 아래 `<…>` 는 자리표시다 — 호스트 · 계정 · 비밀번호 · 레지스트리 주소는 이 문서에 적지 않는다(사용자가 갖고 있는 값 · `deployment.md` 의 기존 절차가 쓰는 값). 명령은 VM 에서 · 이미지는 `<IMG>` = `<레지스트리>/procedure-hub-api:stg-<커밋 sha>`.

| # | 무엇 | 명령 꼴 | 확인 지점 | 멈출 곳(→ 코디에게) |
|---|---|---|---|---|
| ① | 반입 전 기록 | `docker run --rm --env-file <VM env 파일> --entrypoint .venv/bin/alembic <지금 :stg 이미지> current` · `docker inspect --format '{{.Image}}' <컨테이너>` · (권장) DB 백업 — 문서 관례의 일회성 `postgres:16` 컨테이너 `pg_dump -Fc`(비밀번호는 `-W` 프롬프트) | `alembic current` = **`b202610300001 (head)`** 기대(`b202609030001` 이면 같은 체인의 앞 판이라 ③ 에서 둘 다 올라간다 — 진행하되 보고) · 이미지 id 기록 · 백업 파일 크기 0 아님 | 그 밖의 revision · 백업 실패 |
| ② | VM env 파일에 한 줄 | `GOLD_REPOSITORY=db` 를 더한다(편집기) · 확인은 키 이름만: `sudo awk -F= '/^[A-Z_][A-Z0-9_]*=/{print $1}' <VM env 파일>` | 키 목록에 `DATABASE_URL` · `GOLD_REPOSITORY` | 파일 권한 · 소유가 바뀜(`deployment.md` 「값을 출력하지 않고 확인」 꼴) |
| ③ | stg 배포 | `release/v1.2.0` → `stg` PR 머지(코디) → CD 자동(verify → 이미지 → 컨테이너 교체 → Gateway `health` · `products`) | CD 성공 · `alembic current` = **`b202611170002 (head)`** · `GET /procedure-hub/health` 200 · `GET /procedure-hub/gold/health` **503** · 본문 `unavailable: gold 꺼짐 — F2 medallion_build 0행 — 적재 먼저` · `docker logs <컨테이너>` 에 `gold off reason=F2…` | CD 실패 · 기존 `health` 실패 · revision 다름 · gold 이유가 F2 가 아님(예: 「필수 env 없음」 = ② 가 안 읽힘 → 컨테이너 새로 만들기 전 멈춤) |
| ④ | 반입 폴더 | `<반입 폴더>` = `/opt/procedure-hub/import/<날짜>/`(전례 자리) 에 **머지 커밋의** `data/medallion/` · `assets/procedure-images/` 를 옮긴다(옮기는 길은 사용자 — Bastion 경유) | 파일 수 silver 59 · gold 16 · notes 1 · 원장 24 · 그림 103 | 수 다름 |
| ⑤ | dry-run | §11-6 꼴 · `--dry-run` | exit **0** · `tables 76 · rows 130,446` · `gold_hash` · `aux_hash` = §11-0 · `image_files 103 checked` · 요약 출력을 그대로 남김 | exit 2 · 수 · 해시 다름 |
| ⑥ | 적재 | ⑤ 에서 `--dry-run` 만 뺀다 | exit **0** · `loaded tables 76 · rows 130446` | exit 2(L1 = 표 없음 → ③ 확인) · exit 3(롤백 · 이전 그대로 — 출력 그대로 보고) |
| ⑦ | 재시작 | `docker restart <컨테이너>` · 재시작부터 `health` 200 까지 걸린 시간을 잰다 | `GET /procedure-hub/health` 200 · `GET /procedure-hub/gold/health` **200** · `build.gold_hash` · `build.aux_hash` = §11-0 · `files[]` 22 · 로그 `gold repository=db … gold_hash=8accbb21…` | gold `health` 503(이유를 보고) · 기존 `health` 실패 |
| ⑧ | 대조 | Gateway 로 같은 요청 몇 개(`health` 열쇠 · `resolve` 목록 꼴 `total` · `concern-candidates` 하나) → 로컬 18105(DB 판 0.8.1)와 견줌(코디) | `build.loaded_at` · `load_ms` 빼고 같음 | 다름 |
| ⑨ | 기록 | ⑤ ⑥ 출력 · ⑦ 시간 · 해시 · 시각 → 코디가 `_RESUME` 에 | — | — |

- 인프라 레포 · `deploy.sh` · Gateway 는 고치지 않는다(_RESUME §2 11-18). ② 는 VM 파일 한 줄이다.
- ⑤ ⑥ 의 컨테이너는 서빙 컨테이너와 별개다 — 서빙 컨테이너에 마운트 · `docker cp` 를 하지 않는다(조사 §1-3 ⓐ 비추천 · `prod-migration.md` 의 「기존 mounts 없음」 검사).
- ③ 의 순간부터 ⑦ 까지 gold 는 503 이고 기존 허브는 정상이다 — 이 사이가 길어져도 서비스 영향은 gold 경로뿐이다.

**0.2.1 — 실행 기록(2026-11-18 · 코디가 Bastion 경유로 · `stg-runbook.md`)** — 수는 실측이다. 호스트 · 접속 값은 적지 않는다.

| 무엇 | 값 |
|---|---|
| ② VM env 파일에 더한 줄 | `GOLD_REPOSITORY=db` · `GOLD_MCP_ALLOWED_HOSTS=<Gateway 공개 호스트>,<백엔드 내부 주소>:<포트>`(두 값 — §11-3) · `GOLD_LOAD_TIMEOUT_SECONDS=30` |
| ① 백업 자리(경로 꼴만) | DB `/opt/procedure-hub/backup/stg-pre-medallion-<날짜>.dump`(custom 꼴 · 반입 전 표 168) · env 파일 사본 `<VM env 파일>.pre-medallion-<날짜>` |
| ③ 배포 | 허브 PR 머지 → CD 성공 · `alembic current` = `b202611170002` · gold `health` 503(F2) |
| ⑥ 적재 | 표 76 · 행 130,446 · **6.3초**(일회성 컨테이너 `--memory 300m`) |
| ⑦ 켜기 | 재시작 뒤 `health` 200 까지 **약 8초** · gold `health` 200 · 해시 = §11-0 |
| 메모리(R-3 · O-S4) | 컨테이너 **154MB → 225MB** · VM 여유 **약 210MB**(전체 약 891MB) · **swap 0** — 다음 판(gold 가 커지거나 prod)에서 주의: 여유가 색인 증가분과 같은 크기다 |
| ⑧ Gateway 경유 | REST `resolve`(이름 하나) → `CON-168` · MCP `tools/list` 9 |
| 고친 길 | MCP 가 처음 `421` — 원인 = Gateway 가 넘기는 Host 가 백엔드 내부 주소 → 허용 목록에 그 값을 더하고 컨테이너 재생성(배포 스크립트) |

### 11-8. 시험 몫

번호는 `ST`(허브 단위 · 합성 · SQLite — CI 에서 돈다) · `SE`(로컬 실물)로 단다. 합성 fixture 는 지금 것(`tests/medallion_fixture.py` · `tests/gold_fixture.py`)을 쓴다 — 회사 데이터 본문 0.

| # | 시험 | 기대 |
|---|---|---|
| ST1 | **빈 표 기동** — 새 표만 있고 행 0 인 SQLite 파일 DB · `GOLD_REPOSITORY=db` 로 `app.main` 을 lifespan 까지 띄움 | `app.main` 시작 성공 · `/procedure-hub/health` 200 · 본문 열쇠 불변 · `<prefix>/health` 503 · `detail` 이 `unavailable: ` 로 시작하고 `F2` 를 담음 · 다른 gold 경로 · MCP 끝점도 503 |
| ST2 | **적재 뒤 기동** — fixture 를 적재기로 실은 SQLite 파일 DB | gold 켜짐 · `<prefix>/health` 200 · `gold_hash` = fixture 값 · 도구 요청 응답 = 같은 설정의 `gold_main` 응답(`build.loaded_at` · `load_ms` 제외 — DT10 꼴) · MCP 도구 호출 1 이상 |
| ST3 | **해시 불일치** — `GOLD_EXPECTED_HASH` 다른 값(F6) · 빌드 기록 `sha256` 한 줄 고침(F4) | 둘 다 gold 꺼짐 · `app.main` `health` 200 · `detail` 에 `F6` · `F4` |
| ST4 | 판 고르기 | `GOLD_REPOSITORY` 비었음 · CSV env 없음 → 꺼짐(「필수 env 없음」) · 모르는 값 → 꺼짐 · **`gold_main` 은 둘 다 지금처럼 시작 실패**(기존 시험 그대로) |
| ST5 | **기존 계약 불변** | `tests/test_public_api_contract.py` 가 고치지 않은 채 통과(operation 42 · 해시 · 태그 6) · `/procedure-hub/health` · `/health/config` 열쇠 불변 · `test_app_main_untouched` 는 지움(E7) |
| ST6 | lifespan 안 돈 꼴 | lifespan 없이 요청(ASGITransport) → gold 경로 503 「시작 적재 전」 · 기존 경로 시험은 지금처럼 |
| ST7 | 그 밖의 예외 | 적재 함수가 다른 예외를 던지게 함 → 꺼짐 · `detail` = 예외 종류 이름만 · 접속 문자열 꼴(`://`)이 `detail` · 로그에 0 |
| ST8 | 적재기 기본 경로 | 경로 env 없이 루트를 임시 폴더로 돌려(fixture 를 `data/medallion/` 꼴로 놓음) dry-run → exit 0 · 요약의 경로 출처 = 기본 · env 를 주면 env 가 앞선다 |
| ST9 | `gold_main` 불변 | 기존 gold 시험(REST · MCP · DB 판 · 적재) 전부 그대로 · `gold_main` import 가 `app.core.tx` · `app.core.db` 를 안 부름(`test_gold_rest.py:74-78` 그대로) |
| **CI** | CD verify 꼴 — SQLite · 데이터 env 없음 | 기존 시험 그대로 통과(`app.main` 을 쓰는 시험은 gold 꺼짐으로 뜬다 — 기존 경로 응답 불변) · `alembic upgrade head` + `alembic check`(PostgreSQL · 새 revision 0 — 이번 판은 스키마 변경 0) · `ruff check .` |
| SE1 | 로컬 빈 DB | 로컬 PostgreSQL 에 **임시 DB 이름**으로 `alembic upgrade head` → `app.main` 을 그 DB 로 띄움 → gold 꺼짐(F2) · `health` 200 · 끝나면 임시 DB 를 지운다 |
| SE2 | 로컬 적재된 DB | `app.main` 을 적재된 로컬 DB(18432)로 띄움 → gold 켜짐 · 같은 요청 묶음을 18105(DB 판 0.8.1)와 견줌 → JSON 같음(`build.loaded_at` · `load_ms` 제외) |
| SE3 | 이미지 | 로컬 `docker build`(runtime) → 이미지 안 `scripts/load_medallion.py` 있음 · `data/` 없음 · 레포 `data/medallion/` · `assets/procedure-images/` 를 §11-6 꼴로 꽂아 `--dry-run`(DB 접속 0) → exit 0 · §11-0 해시 · 76 · 130,446 · `image_files 103 checked` |
| SE4 | 데이터 폴더 | 복사본 파일마다 sha256 = 원천 · 파일 수(59 · 16 · 1 · 24) · 레포 경로로 dry-run 한 해시 = §11-0 |

완료 조건(이 판): ST1 ~ ST9 · CI 꼴 통과 · SE1 ~ SE4 통과 · 레포에 접속 값 · 호스트 주소 0(공개 금지 grep). stg 의 §11-7 은 배포 단계의 일이다(완료 조건 밖 — 코디 · 사용자).

### 11-9. 열린 것(stg 판)

| # | 열린 것 | 추천 | 상태 |
|---|---|---|---|
| O-S1 | 꺼짐 오류 코드 — `unavailable` · REST `503` · 본문 꼴 SPEC-001 §4-0 그대로 | 본문 그대로 · SPEC-001 다음 판 오류 표에 넷째 줄로 되적기 | **닫힘** — 코디 답(_RESUME §2 11-18) · SPEC-001 0.8.2 §4-0 |
| O-S2 | MCP 꺼짐 = HTTP 503(본문) vs 세션은 열고 도구 오류 | HTTP 503 — 꺼진 상태에 도구 계약이 없다 | **닫힘** — 코디 답 · SPEC-001 0.8.2 §4-0 |
| O-S3 | `GOLD_EXPECTED_HASH` 를 VM env 파일에도 둘지 | **두지 않음** — 적재기 `-e` 로만(V9). env 파일을 고치면 컨테이너를 새로 만들어야 해서(§11-4) 판을 갱신할 때마다 인프라 스크립트를 부르게 된다. 서버는 F4(기록 재셈)로 판 안의 어긋남을 막고 `health` 해시를 사람이 본다(⑦) — 대신 서버 로그에 「GOLD_EXPECTED_HASH 미설정」 경고가 남는다 | **닫힘** — 코디 답(적재기 `-e` 로만) |
| O-S4 | stg 시작 시간 · 메모리(gold 색인을 `app.main` 프로세스가 든다) | ⑦ 에서 시작 시간을 재고 로컬 SE2 에서 프로세스 메모리를 재어 둔다 — 기준값은 정하지 않는다 | **잼**(0.2.1 — §11-7 실행 기록: 약 8초 · 154 → 225MB · VM 여유 약 210MB · swap 0) · 기준값은 그대로 안 정함 — 다음 판 주의 |
| O-S5 | 접근 제어 — Gateway `/procedure-hub/*` 는 인증 없이 지난다(`deployment.md` 「Canonical baseline」 절의 주의) → stg 의 gold 도 공개 | 데이터는 공개 정보(_RESUME §2 11-17)지만 접근 제어 결정은 SPEC-001 O-11 그대로 열림 | **닫힘** — 코디 답: stg gold 는 Gateway 인증 없이 공개(기존 허브 API 와 같은 꼴) |
| O-S6 | prod 승격 — 같은 이미지가 prod 로 가면 prod 에도 빈 표 76 이 생기고 gold 는 꺼짐(503)으로 뜬다 | 이번 범위 밖 — prod 반입 · 공개는 따로 | 범위 밖 확정(코디 답) · 열림(다음 작업) |
| O-S7 | `deploy.sh` 가 env 파일의 더한 키를 그대로 넘기나 | 문서상 검사는 `DATABASE_URL` 하나 · `--env-file` 통째(조사 §1-1) — ③ 의 로그 이유(F2 냐 「필수 env 없음」 이냐)로 드러난다 | **확인** — ③ 에서 F2 · 더한 키가 넘어감(실행 기록) |
| O-S8 | VM 으로 파일을 옮기는 길 | 사용자 방법(Bastion) | **닫힘** — Bastion 경유(실행 기록) |
| O-S9 | 붙인 gold 응답에 `app.main` CORS 머리가 더해짐 | 본문 불변 — 계약 차이로 보지 않음 | 본문 그대로 |
| O-S10 | 옛 이미지 롤백 실물(`b202611170002` 를 모르는 이미지의 시작) | 쓰지 않는 길로 정함(§11-6) — 실물은 안 잼 | 확인 안 됨 |

## 부록 A. 결정 → 본문

| 정해진 것 | 본문 |
|---|---|
| D-0 로컬까지 | §1-3 · §6 · §9 |
| D-1 범위 | §2-2 · §2-3 · §2-4 · §5-2 P5 |
| D-2 자리 | §2-1 R1 |
| D-3 칸 | §2-1 R2 · R3 · R7 · §2-7 |
| D-4 판 | §2-5 · §4-4 |
| D-5 적재 | §4 |
| D-6 repository | §5 |
| D-8 원장 확인 | §2-4 |
| D-9 옛 스키마 금지 | §3-2 |
| D-10 기존 167 | §2-1 R10 · §2-6 |
| D-7 stg 진입점(0.2.0 · _RESUME §2 11-18 S-4) | §11-1 ~ §11-4 |
| stg 시드 = 일회성 적재 · S-1 · S-2 · S-3 · S-5 · S-6(0.2.0) | §11-5 ~ §11-7 |

## 부록 B. 재셈

이 워커가 `python3`(표준 라이브러리 `csv` · `json` · `hashlib`) · `grep` · `git`(읽기) · `lsof` · `which` 로 다시 센 것이다. CSV 는 `utf-8-sig` · `newline=''` 로 읽었다. 스크립트는 세션 임시 폴더에만 두었다. DB · 서버 · docker 를 띄우지 않았고 `.env` 를 열지 않았다.

| # | 무엇 | 결과 |
|---|---|---|
| ① | silver 스키마 ↔ 파일 | 스키마 57표 = 파일 57 · 헤더 어긋남 0 · 66,936행 · 387칸 |
| ② | silver 키 · FK | 키 없는 표 2(`alias` · `source_ref`) · 키 중복 0 · 키 빈칸 0 · FK 칸 **80** · 깨진 FK 0 · **빈칸이 든 FK 칸 35**(빈 값 12,968) · 자기 참조 11 · FK 대상은 전부 그 표의 키 |
| ③ | 이름 길이 | `fk_s_<표>_<칸>_s_<대상>` 최대 63(1개가 63) · 중복 0 · `s_` 붙인 표 이름 최대 27자 · 인덱스 30 이름 최대 47자 · 중복 0 |
| ④ | silver 다형 칸 | 14표 15칸(`*_table`) · `order` 칸 = `procedure_relation` 1표 |
| ⑤ | gold | 15표 · 62,244행 · 278칸 · `order` 칸 = `g_pair` · 키 있는 14표 전부 파일 순서 = 키 오름차순 · `g_profile` 대상 739 / 739 유일 · `g_evidence` 네 칸 27,740 / 27,740 유일 · 빈칸 0 · `g_edge` 깨진 끝 0 |
| ⑥ | 키 없는 표 | `alias` 세 칸 980 / 980 유일 · 네 칸 빈칸 0 · `source_ref` 네 칸 48,094 / 48,094 유일 · `field` 빈칸 40,499 |
| ⑦ | 글자 | 72표 1,099,733칸 · 빈칸 308,658 · NUL 0 · 줄바꿈 0 · 공백만 든 칸 0(silver) · 앞뒤 공백 0(gold) |
| ⑧ | 해시 | `gold_hash`(16 파일) `8accbb21…f6228c` · `aux_hash`(6 파일) `6435fe41…1803a3` · silver 57 `91237618…9c9254` — 조사 §3-1 과 같다 |
| ⑨ | 원장 확인 | 325행 · 16칸 · 쌍 273 · 코드 218 |
| ⑩ | 허브 | HEAD `85c28af` · 모델 `__tablename__` 167 · `s_` / `g_` / `medallion` / `gold_` / `silver_` 로 시작하는 기존 이름 0 · `create_all` 28줄(시험) · versions 2 파일 · 옛 브랜치 versions = initial + 3 · `gold_main` 과 `modules/gold` 에 `DATABASE_URL` 참조 0 |
| ⑪ | 로컬 | 듣는 포트 가운데 18xxx = 18105 · 18106 · 18210 · 18220 · 54xx 0 · `docker` 있음 · Homebrew `postgresql@17` 있음 |

## 변경 기록

### 0.2.1 — 2026-11-18 · 마감 되적기 — 검수 R-1 ~ R-4 · stg 실행 기록

근거: `$W/_RESUME.md` §2 2026-11-18 「SPEC-003 stg 검수 WARN 코디 답」 · 「SPEC-003 0.2.0 정할 것 코디 답」 · 「gold MCP 421 고침」 · 「stg 반입 완료」 · `$W/stg-runbook.md` 실행 기록 · `$W/review-code-hub-stg.md`(C-2) · 허브 `d3d078c`(구현 결과가 정본). 새로 정한 것 0.

- §11-2: R-1 — 503 본문 = F 코드 + 짧은 사유만 · 접속 대상은 로그만(「F1 ~ F7 문구는 접속 값을 싣지 않는다」 는 사실과 달라 고쳤다) · R-2 — 시간 한도 `GOLD_LOAD_TIMEOUT_SECONDS`(lifespan 안 · 데몬 스레드 · 넘으면 gold 만 꺼짐) · 켜짐 판정 = gold `health` 200(로그 아님 — C-2).
- §11-3: 503 본문 꼴 한 줄 · O-S1 닫힘 · MCP 허용 호스트 두 값(Gateway 공개 호스트 + 백엔드 내부 주소).
- §11-4: env 재생성 = Bastion 의 배포 스크립트(`docker restart` 아님).
- §11-7: 실행 기록 표 — env 세 줄 · 백업 자리(경로 꼴만) · 적재 6.3초 · 재시작 뒤 health 약 8초 · 컨테이너 154 → 225MB · VM 여유 약 210MB · swap 0(다음 판 주의) · MCP 421 고친 길. R-3(메모리)은 이 실측으로 받는다. R-4(`app.main` import 시험 3 파일)는 WORK-018 시험 묶음 몫이라 본문 변경 없음(코드 검수 전체 pytest 855 통과).
- §11-9: O-S1 · O-S2 · O-S3 · O-S5 · O-S8 닫힘 · O-S4 잼 · O-S7 확인 · O-S6 범위 밖 확정(열림 — 다음 작업).

### 0.2.0 — 2026-11-18 · stg 판(gold 를 app.main 에 붙임 · 일회성 적재)

- **§11 을 더했다** — 정해진 것(_RESUME §2 11-18 「stg gold = app.main 에 붙임」 · 「stg 시드 = 일회성 적재」 · 「배포로 닫는다」 · 「승인 없이 이어서」)을 본문으로 풀었다. 근거 조사 = `research-stg-seed.md`.
- **D-7 닫음**(§11-1 · §11-2): gold REST(`/procedure-hub/gold`) · MCP(`/procedure-hub/gold-mcp`)를 `app.main` 에 하위 앱으로 붙인다 · `app.main` 의 OpenAPI · 공개 계약 시험 · 기존 `health` 불변 · `gold_main` 은 로컬 단독용으로 남김(동작 같음 · 같은 조립 코드). 기동 규칙 = `db` 이고 빌드 기록이 있고 F1 ~ F7 통과면 켜짐 · 그 밖은 전부 **gold 만 꺼짐**(`app.main` 은 정상 기동). `GOLD_REPOSITORY` 기본값은 `csv` 그대로 — stg 는 VM env 파일 한 줄로 `db`.
- **꺼진 gold 의 응답**(§11-3): REST · MCP 모두 `503` · `{"detail": "unavailable: gold 꺼짐 — <이유>"}` · 이유는 로그 경고 한 줄과 gold `health` 본문에. 새 코드 `unavailable` 은 제안(O-S1 — SPEC-001 되적기).
- **레포 데이터 폴더**(§11-5): 루트 `data/medallion/{silver 59, gold 16, notes/ledger-check-list.csv, bronze/phub-ledger 24, README.md}` · 생성 스크립트 안 넣음 · build context · CD 트리거 밖. 0.1.0 D-5 의 「레포에 CSV 커밋 금지」(로컬 판)는 이 결정으로 바뀌었다.
- **적재기 이미지 포함 · 기본 경로**(§11-6): Dockerfile 한 줄(데이터 안 실음) · 경로 env 가 비면 `<backend 의 부모>/data/medallion/…`(이미지 안 = `/data/medallion`) · 일회성 컨테이너 꼴 · exit 0 / 2 / 3 · 되돌리기(롤백 = 이전 판 그대로 · `alembic downgrade` 안 씀 · 옛 이미지로 안 돌아감).
- **stg 반입 절차서**(§11-7) ① ~ ⑨ · 확인 지점 · 멈출 곳. **시험 몫**(§11-8) ST1 ~ ST9 · CI 꼴 · SE1 ~ SE4. **열린 것**(§11-9) O-S1 ~ O-S10.
- 고친 곳: frontmatter(판 · 제목 · 근거) · 머리 안내 한 단락(§0 ~ §10 의 수 74 = 0.1.0 판 · 지금 76) · §0 표 한 줄 · §1-2 D-7 문장 · §9 N-1 · N-2 · N-5 · N-6 · N-9 상태 · 부록 A 두 줄. §0 ~ §10 의 규칙 · 수는 고치지 않았다(76 · 130,446 은 §11-0).
- 이 워커가 정한 「제안」: `unavailable` · 503(O-S1) · MCP HTTP 503(O-S2) · 기대 해시를 VM env 파일에 안 둠(O-S3) · 꺼짐 이유 글의 규칙(§11-2) · 적재기 기본 경로를 적재기에만(I-7) · `.dockerignore` 안 고침(I-2 — 빌드로 확인).

### 0.1.0 — 2026-11-17 · 초안

- 지시서 「정해진 것」 D-0 ~ D-10 을 본문으로 풀었다 — 테이블 74 · 마이그레이션 1 · 적재 CLI · DB 판 repository · 로컬 실행 · 시험 DT 15 · DE 8 · SPEC-001 되적기 목록 · 다음 범위 11.
- 이 워커가 본문에 「제안」 으로 정한 것: 빈칸 = NULL 과 FK 82(U-1) · `load_seq`(O-1) · 빌드 기록 한 행 = 파일(O-3) · 지연 FK(O-6) · 이름들(O-7) · 로컬 PostgreSQL 띄우는 법(U-2).
- 조사와 달라진 수: `create_all` 시험 줄 20 → 28(허브 HEAD 가 gold 구현 커밋 `85c28af` 로 올라갔다) · 빌드 보조 표 「빌드 기록 1 + 빌드 파일 1」 초안 → 표 1(지시서 D-4).
