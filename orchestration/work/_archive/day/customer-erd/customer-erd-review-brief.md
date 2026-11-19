# [reviewer] 코드 검수 1 — DB 1단계(마이그레이션 0010 · 모델 · enum)

너는 **day `reviewer` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/DAY-customer/orchestration/roles/day/reviewer/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/CENTURION_DAY/customer-erd`
base 브랜치: `origin/dev` → 최종 PR 대상 `dev` (PR 은 코디네이터가 올린다)

<같은 워크트리를 다른 워커와 공유하면 여기에 경고를 적는다. 예: "BE 워커가 `back/` 에서 병렬 작업 중 — 건드리지 마라.">

## 1. SSOT — 먼저 읽을 것

- 계약: `/Users/kknaks/orca/workspaces/mediness-mediness/customer-erd-spec/products/day/20-spec/spec-000-data-model.md` §4 새 테이블 칸 표 · §3 05 `visit_task` 추가 칸 · `spec-002-procedure-board.md` 개정 ㉔ 매핑 표 · entity_type (mediness #952 브랜치 = 최신 계약)
- Delivery Issue: `gh issue view 259 -R MediSolveAIDev/CENTURION_DAY` — 이번 몫 D-1 · D-2 · A1 · A2 · A6 · A7
- 발주서: `/Users/kknaks/orca/workspaces/kknaks_profile/DAY-customer/orchestration/work/customer-erd/customer-erd-be-brief.md` · 워커 리포트 `/Users/kknaks/orca/workspaces/kknaks_profile/DAY-customer/orchestration/work/customer-erd/be-1-report.md`(그대로 믿지 말고 diff 로)
- 코드 규칙: 워크트리 `AGENTS.md` · `docs/development/*`
- 기준: `git -C /Users/kknaks/orca/workspaces/CENTURION_DAY/customer-erd diff origin/dev` + 미추적 파일 · prod/dev 모델(`git show origin/dev:backend/day/models/…`)

## 2. 배경

DAY 가 고객 · 구매 · 시술권 · 선불카드 원천이 되기 전 단계 — 테이블부터 만든다. **상용 서비스 중**(더하기만) · **KOS 뗄 것**(KOS id 는 `external_ref` 만) · **삭제는 소프트 딜리트만**.

## 3. 계약

해당 없음(위 SPEC).

## 4. 먼저 읽을 핵심 파일

- `backend/migrations/versions/20261119_0010_sale_tables.py` · `backend/day/models/{menu,purchase,ticket,prepaid_card,prescription}.py` · `models/task.py` · `backend/day/enums/*` 새 파일 · `identifiers.py` · 테스트 새 파일.

## 5. allowed_paths

- 리뷰 리포트 1개만: `/Users/kknaks/orca/workspaces/kknaks_profile/DAY-customer/orchestration/work/customer-erd/review-code-1-report.md`

## 6. 할 일 — 축마다 PASS/WARN/FAIL + 파일:줄

1. **SPEC 대조** — 28 테이블 · 칸 · 타입 · 필수 · FK · enum 값이 SPEC-000 §4 와 같은가(빠진 것 · 다른 것 · 없는 것 만든 것). 전수 표.
2. **상용 운영** — 기존 테이블 · 칸 · 제약 · 인덱스 변경 0(origin/dev 대비) · `visit_task` 3칸 nullable · 마이그레이션이 기존 데이터를 안 건드림 · 0009 다음 · downgrade 깨끗 · 큰 테이블 잠금 위험(`visit_task` ALTER).
3. **KOS 제거 · 소프트 딜리트** — 새 테이블에 KOS id 칸 0 · `deleted_at` 전부 · 유일 제약은 살아 있는 행만 · enum 이 DAY 말.
4. **범위 밖 변경 2곳** — `emr/kos/demo/kos_board.py` 이름 · 타입 변경(동작 불변인가) · `taut.toml` 등록 — 필요한가 · 안전한가.
5. **1:0..1 유일 제약** — ERD 그림 `purchase_item ||--o| ticket_bundle` · `purchase_item |o--o| prepaid_card` · `ticket |o--o| visit_task` 를 부분 유일로 막아야 하는지(워커는 SPEC 표 표기가 없어 안 걸었다). 동기화 · KOS 재생성 경우에 막혀 깨질 위험까지 보고 **권고만**(결정 금지 · 「사용자 판단」).
6. **테스트** — 왕복 · alembic check · 새 테스트가 무엇을 지키는가. 직접 1회 실행: `cd backend && uv run pytest -q tests/day/test_models.py tests/day/test_column_snapshot.py tests/day/test_sale_entity_types.py tests/migrations/test_sale_tables_migration.py`(마이그레이션 테스트가 DB 필요하면 로컬 compose 만 · 사용자 포트 금지 · 못 하면 pending).
7. **직원이 실물에서 만날 자리** — 해당 없으면 「없음」.

리포트 끝: 전체 판정 · FAIL 고칠 곳 목록.

## 7. 범위 제약

- 파일 수정 · 커밋 금지. 결정 금지(사용자 판단으로 모음).

## 8. 검증

- 위 6 의 실행 결과 수치.

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_3d82d3ad-3bc3-4cdc-8cbd-0e98fbc89591 --from term_899c29c1-703c-4f8e-8075-5087502b7b0e \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "reviewer 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_3d82d3ad-3bc3-4cdc-8cbd-0e98fbc89591 \
  --text "[worker_done] reviewer 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_3d82d3ad-3bc3-4cdc-8cbd-0e98fbc89591 --text "[질문] reviewer: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
