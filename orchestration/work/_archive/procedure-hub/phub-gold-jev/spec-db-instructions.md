# SPEC-003 0.1 — 허브 silver · gold 로컬 DB 화(테이블 · 마이그레이션 · 적재 · repository)

**너는 앞 판의 맥락이 없다.** 먼저 `phub-gold-jev-write-brief.md`(같은 폴더) 전체를 읽어라 — 역할 · SSOT · 제약(공개 레포 · 외부 API · .env · 코드 레포 변경 금지) · §8 검증 · §9 완료 보고 그대로(핸들은 preamble 값). **이번 allowed_paths = `$W/SPEC-003-hub-gold-db.md` 새 파일 1개만.** SPEC-001 · 002 는 고치지 않는다(SPEC-001 과 닿는 곳은 「SPEC-001 §x 를 이렇게 바꿈」 목록으로 SPEC-003 안에 적는다).

`W=/Users/kknaks/orca/workspaces/kknaks_profile/프로시저허브-데이터-메달리온/orchestration/work/phub-gold-jev` · 허브 `H=/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-gold-jev`(읽기만) · `SM=…/orchestration/work/_archive/procedure-hub/phub-ledger-redesign/silver-model`

## 읽을 것

1. `$W/_RESUME.md` §2 — 11-17 맨 위 두 행(「DB 화 이번 목표 = 로컬 허브 DB 까지」 · 「채팅보다 DB 설계 먼저」) ← 정본
2. `$W/research-db.md` 전체 ← 조사 근거(사실 · 셈 · 파일:줄). 여기 없는 사실을 지어내지 마라
3. `$W/SPEC-001-hub-gold-mcp.md` §1-4 · §2 · §3-1 · §6 · §7 · §9 · §10
4. `$H/backend/app/modules/gold/{repository,memory,inputs,headers,config}.py` · `$H/backend/alembic/env.py` · `$H/backend/app/model/base.py` · `$H/backend/app/core/db.py` · `$H/backend/README.md` · `$H/AGENTS.md`(첫 줄 `/Users/marin/...` 무시) · `$H/docs/guides/design.md`

## 정해진 것(코디 기본값 · research-db 추천 그대로 — 다시 묻지 마라)

- **목표 = 로컬 허브 DB 까지.** stg 반입 · stg 진입점(D-7) · stg 권한 · 시드(stg 로 가는 데이터 반입 방식)는 **이번 범위 밖** — 「다음 범위」 로만 적는다.
- D-1 범위 = **silver 57 전부 + gold 15 + 원장 확인 목록**. 허브 코드가 읽는 범위는 지금 그대로(gold 15 + silver 보조 5표 + 원장 확인), 나머지 silver 는 올려 두기만. 원장 JSON(bronze)은 DB 에 안 올림.
- D-2 자리 = `public` + 접두어: gold `g_*`(CSV 이름 그대로) · silver `s_*`(63자 FK 이름 한도 확인).
- D-3 칸 = 전부 문자열(CSV 값 그대로 · 빈칸 규칙 하나로 — `''` vs NULL 중 하나를 정해 적재기가 지킴). 「담을 칸 없는 값 0」.
- D-4 판 = 살아 있는 판 하나 · 전체 교체(한 트랜잭션) + 빌드 기록 표 1개(gold_hash · aux_hash · 파일별 sha256 · 표별 행 수 · 적재 시각). 원문을 DB 에 통째로 넣지 않음(research-db §5 5번).
- D-5(로컬) = 로컬 경로의 CSV 묶음을 **적재 CLI** 가 읽어 싣는다. 경로는 env. 레포에 CSV 커밋 금지.
- D-6 = 허브 시작 때 DB 에서 전부 읽어 **지금 메모리 색인을 그대로** 세운다(Protocol 동기 그대로 · async 는 시작 때 읽기에만). 응답 머리 gold_hash · aux_hash 는 빌드 기록 표 값 — 지금 CSV 판과 **같은 값**이 나와야 한다(8accbb21… 재현).
- D-8 = 원장 확인 목록은 id · 코드 쌍만 표 하나.
- 옛 `phub-recommend`(PR #31) 스키마 · revision id 재사용 금지 — 새 revision id 는 옛 브랜치 3개와 겹치지 않게.
- 기존 테이블 167 은 건드리지 않음 · FK 로 잇지 않음.

## 할 것

1. 표 → 테이블 대응 전부(gold 15 · silver 57 · 원장 확인 · 빌드 기록): 테이블 이름 · PK(키 없는 표 3 의 처리) · silver 안 FK(80칸) 거나 안 거나 · 다형 참조 처리 · 예약어 칸 `order` · 인덱스(허브 메모리 색인이 쓰는 키만). research-db §2 셈을 근거로.
2. 마이그레이션: alembic 한 개(또는 나눔) · 모델 파일 자리 · SQLite `create_all` 시험 기반과 CI `alembic check` 에서 깨지지 않는 조건.
3. 적재 CLI: 입력(경로 env) · 검사(헤더 · 행 수 · 해시) · 한 트랜잭션 교체 · 실패 때 그대로 · exit code. dry-run.
4. repository: DB 판 클래스 · 메모리 판과 고르는 설정(env) · 시작 때 읽기 · DB 판과 CSV 판이 **같은 결과**인지 대조하는 시험(해시 · 도구 응답 동일).
5. 로컬 실행: 로컬 PostgreSQL 을 어떻게 띄우나(포트는 18210 · 18005 금지 · 지금 18105 허브 · 18220 앱과 겹치지 않게) · 허브 `gold_main` 이 DB 판으로 뜨는 명령.
6. 시험 기준(T/E 번호) · 완료 조건 = 로컬 DB 에 실고 18105 를 DB 판으로 띄워 앱 37 키 대조(나) 가 CSV 판과 같음.
7. 「다음 범위」 표: stg 진입점(D-7) · stg 반입(시드) · 권한 · 회사 데이터 범위.
8. version 0.1.0 · 변경 기록 · 열린 것 표 · **WORK 전 사용자 결정 목록**(추천 붙임 — 최소로, 위 「정해진 것」 은 다시 올리지 마라).

## 검증

- 표 72 + 2 전부 대응됐는지 셈(빠짐 0) · 결정 행 → 문서:줄 표 · 공개 레포 grep(회사 데이터 본문 0 · 비밀값 0).
