# Delivery Issue v1 발행 결과 — customer-erd

- 작성: day `planner` · 2026-11-19 · task `task_00a32dc3a0b7` · dispatch `ctx_d02e4d586b94`
- 지시서: `delivery-start-instructions.md`

## 상태: done

| 항목 | 값 |
|---|---|
| Issue | **MediSolveAIDev/CENTURION_DAY#259** — https://github.com/MediSolveAIDev/CENTURION_DAY/issues/259 (OPEN) |
| 제목 | 메뉴 · 구매 · 시술권 · 선불카드 · 처방 테이블(마이그레이션) + KOS → DAY 동기화 |
| idempotency_key | `day/customer-erd-2026-11-19` · contract_version 1 · risk_level **L3** |
| 상태 라벨 | `spec-baseline:ready` · `delivery-plan:approved` · `execution-plan:ready` |
| target_specs · baseline | `DAY-SPEC-000` · `DAY-SPEC-002` @ mediness origin/main `4585fb59cdfb1203ad6285d53b64edd11363a5f3` |
| plan_digest | `sha256:19b48a8faabdfc49fafc4141930fd506bea9607d8d632516239fc55ac057ae02` |
| contract_digest | `sha256:690841907938d4e4bc2d44597f6ffad56ebf8e5c4ae7b4a11a8f063764f33215` |
| 승인 | receipt `{decision: approved, reviewer_type: human, reviewer: kknaksss, plan_digest: 위}` — 사용자 2026-11-19 「이슈 발행하고 db 만들자」 |
| 다음 action | **`implement-and-open-code-pr`**(human_gate false) → Code PR 뒤 `review-delivery` |
| Task projection | `degraded` · reason `authentication-required-or-expired`. 이 세션에는 mediness MCP 가 `authenticate` 도구뿐이라 `task_draft_request` 를 부를 수 없다. canonical Issue 는 롤백되지 않으며 apply 결과는 `partial: true` 다. 인증 뒤 성공 receipt 가 같은 슬롯을 복구한다 |

## 실행 순서 · 파일 (`delivery/`)

CLI 는 `uv run --project tools/harness mediness start-delivery --mediness-repo <customer-erd-delivery> --code-repo /Users/kknaks/orca/workspaces/CENTURION_DAY/customer-erd --github-repo MediSolveAIDev/CENTURION_DAY` 다. 실행 직전 fetch 한 `origin/main` = `4585fb59` 이다.

1. `cerd.v1.request.json` → `--plan`(`cerd.v1.plan.json`): baseline ready · execution ready · `review-delivery-plan` 이 나왔다.
2. `--apply`(`cerd.v1.apply.json`): Issue #259 가 생성됐다(`delivery-plan:review` · task projection blocked).
3. `cerd.v1.approval-receipt.json` 으로 `--plan`(`cerd.v1.approve.plan.json`) → `--apply`(`cerd.v1.approve.apply.json`): `plan-approved` · `implement-and-open-code-pr` 가 나왔다.
4. `cerd.v1.task-projection-failure.json` 으로 `--apply`(`cerd.v1.projection.apply.json`): status `current` · projection degraded 로 기록됐다.

두 워크트리(`mediness-mediness/customer-erd-delivery` · `CENTURION_DAY/customer-erd`)는 파일 수정 · 커밋 · push 0 이다(`git status` clean). uv 가 gitignore 된 `tools/harness/.venv` 만 만들었다.

## baseline 판단 — ready(지금 main)

- **CLI 규칙**: `spec-baseline:pending` 은 target SPEC 이 baseline revision 에 없거나 `stable` 이 아닐 때만 나온다(`tools/harness/src/mediness_harness/surfaces.py` — `missing` 목록). `DAY-SPEC-000` · `DAY-SPEC-002` 는 main `4585fb59` 에서 둘 다 `stable` 이다. 그래서 「pending 으로 시작」은 이 CLI 로 표현할 수 없다(요청 값으로 고르는 칸이 없다).
- **workflow 규칙**(`rules/delivery-workflow.md`): 「이미 Stable SPEC 이 있는 기능 고도화는 현재 계약을 baseline 으로 고정하고 목표 변화는 Target Delta 에 둔 뒤, 구현으로 확인된 durable 변화만 merge 후 SPEC 에 반영」. 이번 일이 그 경우다.
  - 새 테이블 28개는 #951 로 main 에 있다.
  - 동기화 계약(SPEC-002 개정 ㉔)과 SPEC-000 2026-11-19 칸 수정은 #952(미머지 · head `4fe24e4b15a8d86d9bac1b273f78a514ef12ae37`)에 있다. 사용자 결정은 「머지는 코드와 한 번에」다. #952 내용은 Target Delta D-1 · D-2 에 #952 head SHA 와 함께 적었다.
- 그래서 **ready @ 4585fb59** 로 결속했다. Review Surface 첫 줄에 이 판단과 대안을 적었다. 대안은 「#952 를 먼저 머지하면 같은 key v2 로 재결속」이다. 결과 계약 의미가 같으면 baseline 갱신만으로는 재승인이 필요 없다(Skill 규칙).

## 확정된 execution

- **code_surface**(코드 워크트리 `bbd9220a` 에서 실제 확인한 경로):
  - `backend/migrations/versions/`(새 `20261119_0010_*` — head = `0009_consultation_visit` 확인)
  - `backend/day/models/`(새 모듈 · `task.py` · `__init__.py`)
  - `backend/day/emr/kos/client.py` · `mapper.py` · `mapper_values.py`
  - `backend/day/emr/normalized.py` · `base.py`
  - `backend/day/emr/sync_master.py` · `sync_schedules.py` · `sync_tasks.py` · `sync_references.py` · `sync_persistence.py` · `sync_tables.py` · `sync.py` — dev 는 prod 와 달리 동기화가 이 파일들로 나뉘어 있다
  - `backend/day/tasks/emr.py` · `backend/common/config.py`(주기 설정)
  - `backend/tests/migrations/`(`test_alembic.py` · 새 0010 테스트) · `backend/tests/day/test_column_snapshot.py` · `column_snapshot_data.py` · `backend/tests/day/emr/`(fixtures · `test_kos_mapper.py` · `test_sync.py` · `test_emr_sync_service.py`) · `backend/tests/day/board/`
- **phases**:
  - P1 DB(migration 0010 · 모델 · 칸 스냅샷)
  - P2 메뉴 동기화(1시간)
  - P3 오늘 동기화(10초)
  - P4 병원 전체 변경 5분 회차
- **verification**:
  - pytest 해당 파일
  - migrations 왕복(upgrade → downgrade → upgrade · head 하나 · alembic check)
  - DEMO 로컬 실물
  - 물리 DELETE grep 0 · ruff · architecture
- **rollback**: `alembic downgrade 0009_consultation_visit` · Code PR revert
- **dependencies**: 사용자 plan 승인(완료) · DEMO 테넌트 KOS 연결
- **open_questions**: DAY-SPEC-002 OQ-69 ~ 75 · DAY-SPEC-000 OQ-08-9 · 08-10 · OQ-10-3

## Acceptance · Non-goals · Review Surface (지시서 그대로)

- A1 ~ A7 은 지시서와 같다. A3 에는 데모 건수를 적었다: 카테고리 15 · 상품 103 · 옵션 326 · 시술 804 · 시술 항목 226 · 기기 302 · 약물 349 · 선불카드 상품 8 · 시술 외 품목 11 · 기타 작업 10. 출처는 조사 리포트 실호출 표다.
- Non-goals:
  - 백필(OQ-00-3)
  - DAY → KOS 쓰기 · 원장 전환
  - 화면
  - 결제 · 환불 감사 로그
  - prod 배포
  - 실 명동점 호출(DEMO 테넌트만)
- Review Surface:
  - baseline 판단
  - L3 무중단(더하기만)
  - 내부 API 의존(브라우저 UA)
  - enum 매핑(`REFUND` → `revoke` · 5분 회차 구매 항목 통계)
  - 기본값 OQ-69 ~ 75

## 주의

- 요청 · Issue 본문에는 비밀값 · 이메일 · 테넌트 id 가 없다. 경로 · 키 이름 · 건수 · SHA 만 있다.
- 구현 워커는 #952 head `4fe24e4b` 의 SPEC-002 ㉔ 절과 SPEC-000 2026-11-19 개정을 계약으로 읽어야 한다(main 에는 아직 없음).
