# WORK-010(허브) 작성 지시서 — SPEC-003 0.1.0 로컬 DB 화 구현 계획

**너는 앞 판의 맥락이 없다.** `work-write-instructions.md`(같은 폴더)의 역할 · 제약 · 검증 · 완료 보고 꼴 그대로(핸들은 preamble 값). allowed_paths = **`WORK-010-hub-db.md` 새 파일 하나만**. 11-17 사용자 결정: Procedure Hub 데이터(원장 · silver · gold)는 공개 정보 — 「회사 데이터 본문 0」 제약은 이 데이터에 걸지 않는다(비밀값 · 접속 문자열 · 내부 URL 금지는 그대로).

`W=/Users/kknaks/orca/workspaces/kknaks_profile/프로시저허브-데이터-메달리온/orchestration/work/phub-gold-jev` · 허브 `H=/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-gold-jev`(읽기만 · HEAD 85c28af · 구현은 여기서 이어서)

## 읽을 것

1. `$W/_RESUME.md` §2 11-17 행 전부 — 특히 **U-1 (a) 빈칸 NULL + FK 82** · **U-2 (a) Docker postgres:16 · 127.0.0.1:18432**(코디가 이미 띄움 · 새 빈 DB · 접속 값은 레포 밖 파일 — 워커는 열지 않는다) · **검수 뒤 코디 W-1 ~ W-4**
2. `$W/SPEC-003-hub-gold-db.md` 전체 ← 계약
3. `$W/review-spec-003.md` WARN 4 · NOTE 8
4. 앞 WORK 꼴: `$W/WORK-007-hub-v052.md`
5. 지금 코드: `$H/backend/app/modules/gold/*` · `$H/backend/app/gold_main.py` · `$H/backend/alembic/` · `$H/backend/app/model/` · `$H/backend/tests/` · `$H/backend/README.md` · `$H/AGENTS.md`(첫 줄 무시) · `$H/.github/workflows/backend-test.yml`

## 쓸 것

- SPEC-003 절 ↔ WP 대응표(미대응 0) — 테이블 74 · 모델 · alembic 1 · 적재 CLI(V1~V10 · L1~L6 · dry-run · exit) · DB 판 repository(GOLD_REPOSITORY 기본 csv) · 시험 DT1~DT15 · DE1~DE8.
- **첫 WP = 확인**(W-4): 지연 FK 를 모델 · 마이그레이션 양쪽에 같게 → `alembic check` 통과 · `load_seq` `autoincrement=False`(PK 3표) · SQLite `create_all` 28 파일 pytest 시간 앞뒤 · `public` 테이블 셈(alembic_version 포함 242) · 안 되면 대안(의존 순서 싣기 · 지우기 역순 — N-6).
- 검수 반영 한 줄씩: W-1 health 새 필드 **안 넣음** · W-2 `DATABASE_URL` 읽는 자리 하나 명시 + alembic 명령은 프로세스 env 붙인 꼴만 + 적재기 · alembic 전에 접속 대상(호스트 · 포트 · DB 이름, 비밀번호 빼고) 찍기 · W-3 접속 실패 exit 2 · 필수 env dry-run / 적재 나눔 · 파일은 한 번 읽기 · NOTE 1~8 처리(N-1 정렬은 파이썬 · N-2 expected_hash_checked · N-4 이름 겹침 V · N-5 id 유일 · 빈칸 0 등).
- 실물 확인 순서(코디 몫과 워커 몫 갈라 적기): 워커 = 로컬 PG(18432)에 `alembic upgrade head` → dry-run → 적재 → 18107 에 DB 판 허브 → 18105(CSV 판 · 코디 것)와 같은 요청 대조(DE6). 코디 = 18105 를 DB 판으로 바꿔 앱 37 키 대조(DE7 · 완료 조건). 워커는 18105 · 18220 · 18210 · 18005 를 내리거나 띄우지 않는다.
- 완료 조건 · 검증 명령(ruff · pytest · alembic check · grep) 앞 WORK 꼴.

## 검증

대응표 · WARN/NOTE 반영 줄 · 경로 실재 · 공개 grep(비밀값 · 접속 문자열 0).
