# [backend] Delivery #225 — DAY v2 데이터 모델(1차 테이블 모델 + 첫 migration)

너는 day backend 워커다. 역할 문서: `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/roles/day/backend/`(role · rules · skills · tools · workflow).
작업 워크트리: `/Users/kknaks/orca/workspaces/CENTURION_DAY/day-data-architecture` — 브랜치 `kknaksss/day-data-architecture`, #224 가 커밋돼 있다(Code PR #228 · 사용자 결정: 화면까지 PR 하나). **그 위에 이어서.** 다른 워커 없음.

## 1. SSOT

- **계약 = Delivery Issue #225** — `gh issue view 225 -R MediSolveAIDev/CENTURION_DAY` (바뀌는 것 · 하지 않는 것 · 완료 조건 A1 ~ A5). 사용자가 2026-11-05 구현을 지시했다.
- **테이블 정본 = DAY-SPEC-000** `/Users/kknaks/orca/workspaces/mediness-mediness/day-data-architecture-spec/products/day/20-spec/spec-000-data-model.md` §2 공통 규칙 · §3 1차 테이블 · §6 Open Questions. ERD 그림 `/Users/kknaks/orca/workspaces/mediness-mediness/day-data-architecture-spec/products/day/40-architecture/erd.md`. 원천(사용자 결정 기록) `/Users/kknaks/orca/workspaces/kknaks_profile/day/reference/2026-11-03-cc-day/erd/` 01 ~ 07 — SPEC 과 원천이 다르면 **원천이 맞다** · 리포트에 적어라.
- 레포 규칙 `AGENTS.md` · 코드 구조 `/Users/kknaks/orca/workspaces/mediness-mediness/day-data-architecture-spec/products/day/40-architecture/code-structure.md`.
- 본(모양만): centurion `git -C /Users/kknaks/git/centurion show origin/main:<경로>` — `backend/crm/db.py` · `models.py` · `enums.py` · `backend/common/crypto.py`.

## 2. 테이블 목록 — 숫자를 믿지 말고 세어라

Issue 는 「51 테이블」이라 적었다. **SPEC-000 §3 의 테이블 머리(`#### \`이름\`` · `#### 이름 · …`) 와 표(02 코드 테이블처럼 표 한 줄 = 테이블 하나)를 전부 grep 으로 세어** 목록을 만들고 51 과 다르면 리포트에 차이를 적는다. 04-1(§4 1차 범위 밖) 은 만들지 않는다(A2).

## 3. 코디 결정 (기본값 — 이대로)

1. `product_option_id` — uuid 칸만, **FK 없음**(1차는 메뉴 테이블 없음 · 「참조 + 스냅샷, 1차는 스냅샷만」 사용자 결정). 칸 주석에 「04-1 생기면 FK」.
2. enum — **정해진 enum** 은 SPEC 값 목록 그대로 DB 에서도 막는다(저장 방식 = PG native enum 이냐 varchar + CHECK 냐는 centurion `crm` 선례를 확인해 따르고 리포트에 근거). **열린 enum**(§6 OQ — gender 등 「값 확인 뒤」) 은 varchar · 제약 없음 · 주석에 OQ 번호.
3. 07 알림 · 접수 · 채팅 — SPEC 대로 만든다(원천 「바로 적용」 · ESC-001 은 사용자가 값 그대로 승인).
4. 보류 칸(OQ-03-1 `purchase_ids` · `prescription_ids` · `reactions`) — 만들지 않는다. 대조표에 「보류 · 안 만듦」.
5. 암호화(A4) — centurion `common/crypto.py` 모양(Fernet · TypeDecorator)으로 `backend/common/crypto.py`. **키가 없으면 기동 실패**(dev 포함 — 평문 폴백 없음). 키는 env(`*.env.example` 에 자리표시자만). 테스트는 테스트용 키를 fixture 로 생성.
6. #224 검수에서 넘어온 것 — **W6** DB 쿼리 timeout(`command_timeout` 또는 `statement_timeout` 을 설정값으로) · **in-process 테스트 스키마**: 세션 시작 때 `day_test` 를 만들고 `create_all`/migration, 끝날 때 DROP 하는 fixture(`day_dev` 는 절대 안 건드림 — #224 의 `test_테스트_프로세스는_day_dev_를_쓰지_않는다` 유지).

## 4. 구현 순서 — Issue 「실행 정보」

1 · 01 · 02 모델 → 2 · 03 · 04 → 3 · 05 · 06 → 4 · 07 → 5 · 첫 migration(autogenerate 뒤 손으로 검토, 빈 `DB_SCHEMA` 에 upgrade · downgrade) → 6 · 대조표 · 제약 테스트.
모델은 `backend/day/models/<주제>.py` 기능별 파일 · `models/__init__.py` 가 전부 import. enum 은 `backend/day/enums/`. 단계마다 그 단계 테스트만, 전체는 끝에 한 번.

## 5. allowed_paths

`backend/day/models/` · `backend/day/enums/` · `backend/day/db.py` · `backend/common/crypto.py` · `backend/common/config.py`(암호 키 · timeout 설정) · `backend/common/db/session.py`(timeout) · `backend/migrations/versions/` · `backend/tests/` · `deploy/local.env.example` · `pyproject.toml` · `uv.lock`(cryptography 추가). AGENTS.md 는 고치지 마라.

## 6. 하지 말 것

Issue 「이번에 하지 않는 것」 전부 — 서비스 · 라우터 · 동기화 · 로그인 · 데이터 채우기 · 화면. §6 OQ 를 결정하지 마라. SPEC 에 없는 칸 · 테이블 · 인덱스 발명 금지(필요해 보이면 리포트 「제안」으로). 커밋 · push · PR 금지. 포트 11040 · 11042 · 11043 만, 끝나면 `down`. KOS 호출 없음.

## 7. 검증 · 보고

`scripts/test.sh -q` · `uv run ruff check backend` 각 1회 · 실제 PG 에서 migration upgrade → downgrade → upgrade · 유일 · 복합 PK 제약 위반이 실제로 막히는 테스트 · 암호화 칸이 DB 에 암호문으로 들어가는지(raw SELECT) · 아키텍처 테스트.
**대조표**: 테이블마다 SPEC 칸 수 · 모델 칸 수 · 타입 · 필수 · 제약 — 스크립트로 뽑아 리포트에 붙인다(손으로 쓴 표 금지).
리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/day/orchestration/work/day-data-architecture/backend-225-report.md` — 테이블 목록(센 방법 · 51 과의 차이) · 대조표 · 코디 결정 1 ~ 6 처리 · SPEC ↔ 원천 차이 · 수치 · 남은 것. 완료는 preamble 의 worker_done 절차대로.
