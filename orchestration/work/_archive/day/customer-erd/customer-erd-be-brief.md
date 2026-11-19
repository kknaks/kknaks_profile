
# [backend] 1단계 — DB: 마이그레이션 0010(새 테이블 28 · visit_task 칸 3) · 모델 · enum

너는 **day `backend` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/DAY-customer/orchestration/roles/day/backend/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/CENTURION_DAY/customer-erd`
base 브랜치: `origin/dev` → 최종 PR 대상 `dev` (PR 은 코디네이터가 올린다)

너는 맥락이 없다 — 아래 파일이 전부다. 이 워크트리는 너 혼자 쓴다. base = origin/dev `bbd9220a`(코디가 발주 직전 fetch 한 최신). **시작 전에 `git fetch origin dev && git log -1 origin/dev` 로 dev 가 더 나아갔는지 보고, 나아갔으면 rebase 한 뒤 시작해라**(사용자 규칙: 코드 작업 전 dev 최신).

## 1. SSOT — 먼저 읽을 것

- `/Users/kknaks/orca/workspaces/mediness-mediness/customer-erd-spec/products/day/20-spec/spec-000-data-model.md` **§4 새 테이블 칸 표 전부**(+ §2 공통 규칙 · §3 05 `visit_task` 「추가(2026-11-18)」 칸) ← **계약의 SoT.** 표에 없는 칸 · 테이블을 만들지 마라. 이 파일은 mediness PR #952 브랜치(`kknaksss/customer-erd-sync`) 워크트리다 — 2026-11-19 칸 수정(옵션 단위 · 구성 참조 칸 뺌 · enum 추가)이 들어 있는 최신본.
- `/Users/kknaks/orca/workspaces/mediness-mediness/customer-erd-spec/products/day/20-spec/spec-002-procedure-board.md` 개정 ㉔ 「KOS 읽기 — 새 테이블 동기화」 — 이번 단계는 **매핑 표의 enum 값 · `external_ref.entity_type` 새 값만** 소비한다(동기화 코드는 2단계).
- 이 워크트리의 `AGENTS.md` · `docs/development/refactoring-conventions.md` · `backend-reliability.md` · `testing-strategy.md` · `corrections.md` — 구조 · 네이밍 · 테스트 규칙.
- Delivery Issue **MediSolveAIDev/CENTURION_DAY#259**(L3 · 승인됨 · `gh issue view 259 -R MediSolveAIDev/CENTURION_DAY`) — D-1 · D-2 · A1 · A2 · A6 · A7 이 이번 1단계 몫.
- 결정 원장: `/Users/kknaks/orca/workspaces/kknaks_profile/DAY-customer/orchestration/work/customer-erd/_RESUME.md` §2.

**기대는 개념** — 해당 없음.

## 2. 배경 / 무엇을 바꾸나

예약 구현 뒤 DAY 가 고객 · 구매 · 시술권 · 선불카드의 원천이 된다. 그 전에 테이블을 만들고 KOS → DAY 동기화로 채운다. **이번 1단계는 DB 만** — 마이그레이션 · 모델 · enum. 동기화(메뉴 · 오늘 · 5분)는 2단계 발주.

**두 조건(사용자 · 모든 줄의 기준)**
1. **상용 서비스가 이미 나가 있다** (prod 동기화가 10초마다 돈다). 지금 테이블 · 칸의 **이름 · 타입 · 제약을 바꾸지 마라 — 더하기만.** `visit_task` 새 칸 3개는 nullable. 마이그레이션은 기존 데이터를 건드리지 않는다(데이터 이동 · 백필 없음).
2. **나중에 KOS 를 뗀다.** KOS id 칸을 새 테이블에 두지 마라 — 외부 id 는 `external_ref` 에만(기존 규칙). enum 은 DAY 말(소문자 · SPEC-000 값 그대로).
3. **삭제는 소프트 딜리트만** — 새 테이블 전부 `deleted_at` · 유일 제약은 살아 있는 행만(기존 `live_unique` 관례).

## 3. 계약

- 테이블 · 칸 · 타입 · 필수 · FK = SPEC-000 §4 표 그대로. 이름 규칙 · 공통 칸(`id` uuid · `hospital_id` · `created_at` · `updated_at` · `deleted_at`)은 §2 · 기존 모델 관례(`backend/day/models/_columns.py`).
- `external_ref.entity_type` 새 값 · enum 값 = SPEC-002 ㉔ 매핑 표 · SPEC-000 enum.

## 4. 먼저 읽을 핵심 파일

- `backend/day/models/` 전부 · `_columns.py`(uuid_pk · fk · timestamptz · live_unique 등) · `__init__.py`(alembic 이 읽는 import)
- `backend/migrations/versions/` — 마지막 `20261112_0009_consultation_visit.py`. 새 파일은 같은 이름 관례로 `0010`, `down_revision` = 0009.
- `backend/tests/migrations/` — 왕복 · offline SQL 테스트 관례(`test_alembic.py` · `test_offline_sql.py` · 기존 마이그레이션 테스트).
- `backend/day/enums/` · `external_ref` 모델 · entity_type 정의 위치.

## 5. allowed_paths — 이 밖은 건드리지 마라

- `backend/ (frontend 몫 — backend/day/routers/(api 제외) · templates/ · static/ · styles/ — 제외) 중 브리프가 지정한 곳`
- `pyproject.toml · uv.lock (의존성 추가가 브리프에 있을 때만)`
- `deploy/ · scripts/ (브리프가 지정할 때만)`

## 6. 구현 단계

1. `git fetch origin dev` — 나아갔으면 rebase(위).
2. enum 추가(`backend/day/enums/`) — SPEC-000 §4 · SPEC-002 ㉔ 값.
3. 모델 — 주제별 파일(메뉴 · 구매 · 시술권 · 선불카드 · 처방). 기존 파일에 섞지 말고 관례대로. `visit_task` 에 nullable 칸 3개(`treatment_item_id` FK · `ticket_id` FK · `machines` 문자열 배열 — 기존 `medicines` 와 같은 타입).
4. 마이그레이션 0010 — 새 테이블 · FK · 부분 유일 · 인덱스(SPEC 에 있는 것만) · `visit_task` 칸 추가. downgrade 는 역순으로 깨끗이.
5. `external_ref.entity_type` 새 값(문자열 · 제약이 있으면 마이그레이션에 같이).
6. 테스트 — 마이그레이션 왕복(upgrade → downgrade → upgrade) · offline SQL · 모델 메타데이터와 마이그레이션 일치(기존 관례 테스트가 있으면 그것) · 기존 테이블 칸 불변(가능하면).
7. 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/DAY-customer/orchestration/work/customer-erd/be-1-report.md` — 만든 테이블 · 칸 수 · SPEC 표와 다른 곳(있으면 이유) · 기존 테이블 변경 0 증거 · 테스트 수치.

## 7. 범위 제약 — 하지 말 것

- 동기화 코드(`emr/` · `tasks/emr.py`) · KOS 호출 · 화면 · 라우터 — 2단계 몫.
- 기존 테이블 · 칸 · 제약 변경 · 데이터 이동.
- SPEC 에 없는 칸 · 인덱스 · 테이블.
- 커밋 · push · PR. 사용자 포트 · 프로세스 · 공유 DB(STG · PROD) 금지.

## 8. 검증

```
cd backend && uv run pytest -q <네가 만들거나 고친 테스트 파일만> · uv run ruff check <네가 만진 파일> — 각 1회, 통과하면 반복하지 마라. 테스트 DB 는 로컬 compose — 공유 STG·PROD 금지. 사용자 포트·프로세스를 건드리지 않는다. 실행 못 한 검증은 사유와 함께 pending
```

- 통과할 때까지 고친다. 못 고치면 이유와 함께 보고한다.
- 기존에 이미 깨져 있던 무관한 실패는 "무관"으로 분리해 보고한다.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_3d82d3ad-3bc3-4cdc-8cbd-0e98fbc89591 --from term_bbe79944-22d5-4480-8435-1776c9ea2198 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "backend 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_3d82d3ad-3bc3-4cdc-8cbd-0e98fbc89591 \
  --text "[worker_done] backend 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_3d82d3ad-3bc3-4cdc-8cbd-0e98fbc89591 --text "[질문] backend: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
