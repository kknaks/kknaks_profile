# [reviewer] WORK-007 Phase B-1·B-2·B-3 — 백엔드 구현 검수

너는 **strong-hajin `reviewer` 워커**다. 역할 문서를 먼저 읽어라:

- `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱하진-디자인/orchestration/roles/strong-hajin/reviewer/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

읽을 워크트리: `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-design` (브랜치 `kknaksss/strong-hajin-design`)

## 0. 읽기 전용이다

코드를 **한 줄도 고치지 마라.** 산출물은 리포트 한 장이다.

- 쓰기: `/Users/kknaks/orca/workspaces/kknaks_profile/스트롱하진-디자인/orchestration/work/strong-hajin-design/review-be-report.md` ← 이 파일 하나만

## 1. 무엇에 비추어 보나

| 기준 | 경로 |
|---|---|
| **계약 SoT** | `.../para/projects/summer-star/strong-hajin/20-spec/spec-007-task-detail.md` (v0.2.0) |
| **단계·Acceptance** | `.../30-work/work-007-task-detail.md` Phase B-1(:236) · B-2(:273) · B-3(:312) |
| 왜 그렇게 정했나 | `.../10-decision/decision-006-task-detail.md` |
| 워커 리포트 | `.../orchestration/work/strong-hajin-design/be-report.md` |
| 착수 전 코드 상태 | `.../orchestration/work/strong-hajin-design/be-survey-report.md` |

**SPEC-007 §7.2 가 SPEC-001·003·005 의 여섯 줄을 대체한다.** 기존 계약을 근거로 지적하기 전에 §7.2 를 먼저 봐라.

## 2. 진단 — `git diff origin/main` 으로 시작한다

워커 리포트를 **믿지 말고** diff 로 확인해라. 리포트가 말한 것과 코드가 하는 것이 다를 수 있다.

## 3. 계약 대조 — 이것들이 어긋나면 FAIL

1. **후행을 저장하지 않는다** — 새 표·새 쓰기 경로·양방향 저장이 생겼나
2. **역방향 조회** — `predecessor_task_id` 로 읽나. 인덱스가 실제로 붙었나
3. **응답 필드** — `successors` + `hidden_successor_count` 가 계약대로인가
4. **못 읽는 후행은 건수만** — 제목·담당자·기한이 새어 나가나. **권한 필터가 실제로 도는가**
5. **못 읽는 선행도 건수만이고 미완으로 센다**
6. **읽기 전용 갈래에도 후행이 실린다**
7. **상위 변경** — `parent_task_id` + `clear_parent`. 검증이 기존 `parent_for()` 를 **재사용**하나, 새로 짰나
8. **V-8 파급 거절** — 직속 하위만 본다. `WORK_CHILDREN_DIRECT_NESTING`(409) 가 기존 `WORK_DIRECT_NESTING` 과 **합쳐지지 않았나**
9. **상위 이동 시 자손 전체 프로젝트 파급**
10. **후행 해제는 전용 명령** — PATCH 배열 교체로 대신하지 않았나. A 담당자에게 열려 있나
11. **알림은 범위 밖** — 구현해 버렸나 (주석 자리만이어야 한다)
12. **선행=시작 / 하위=완료** — 두 축이 섞였나. 오류 코드가 합쳐졌나

## 4. 특히 볼 자리 — 「조용히 통과하는 자리」

테스트가 초록인데 계약이 깨진 곳을 따로 본다.

- **권한 필터가 이름만 있고 안 거르는** 곳. 못 읽는 후행의 제목이 응답 어딘가에 실려 나가나
- **빈 단언** — `assert True` 류, 또는 결과를 안 보는 테스트
- **폴백이 거절을 삼키는** 곳. 예외를 잡아 빈 배열로 돌려 「막힘 없음」이 되나
- **개명** — 기존 필드를 이름만 바꿔 놓고 계약이 바뀐 것처럼 보이나
- **인덱스가 선언만 되고 실제 DB 에 안 붙는** 곳 (Alembic 부재·`schema_sync` 한계)
- **`reset_demo` 전용 경로를 벗어난 스키마 변경**, 일반 API startup DDL
- **MCP↔HTTP 비대칭**이 새로 생겼나 (WORK-007 이 안 시킨 것을 고쳤거나, 시킨 것을 한쪽만 했거나)
- **`TaskVersion` snapshot** — 상위·프로젝트가 바뀌는데 이력이 그것을 못 남기나

## 5. 범위 이탈

- `frontend/` 를 건드렸나 (금지였다)
- WORK-007 에 없는 단계를 했나
- 커밋·push 했나 (금지였다)
- allowed_paths 밖 파일이 바뀌었나

## 6. 검증 재현

워커가 보고한 검증 수치를 **직접 다시 돌려 확인해라.**

```
make test-unit · make test-contract  (필요한 것만)
```

- **사용자 포트·프로세스를 건드리지 마라** — `8001`·`5176`·`54329` 가 떠 있다. 죽이거나 재시작 금지
- 격리 PostgreSQL 이 필요한 것은 돌리지 말고 「코디 몫」으로 적어라
- 워커 수치와 다르면 **둘 다** 적어라

## 7. 판정

- **FAIL** — 계약과 다른 것이 돈다
- **WARN** — 물어야 할 만큼 모호하다
- **PASS**

각 지적에 **파일:줄 + 근거**. 근거 없는 지적은 쓰지 마라.

## 8. 리포트 형식

```
## 0. 판정 (FAIL n · WARN n)
## 1. 계약 대조표 (§3 열두 항목 각각 충족/불충족 · 파일:줄)
## 2. FAIL — 각각 무엇이 계약과 다른가 · 어떻게 재현하나
## 3. WARN
## 4. 조용히 통과하는 자리 (§4) — 봤고 문제 없으면 그것도 적는다
## 5. 범위 이탈 (§5)
## 6. 검증 재현 결과 — 워커 수치와 대조
## 7. 검수 한계
```

## 9. 완료 보고 — **문구 변경 금지**

```bash
orca orchestration send \
  --to term_e622370a-1f3b-4861-b759-daa3584eace0 --from <네 워커handle> \
  --type worker_done \
  --task-id <dispatch context 의 taskId> \
  --dispatch-id <dispatch context 의 dispatchId> \
  --subject "reviewer BE 검수 완료: FAIL n · WARN n" \
  --body "리포트 경로 / FAIL 요약 / 계약 대조 불충족 / 검증 재현 결과 / 검수 한계"

orca terminal send --terminal term_e622370a-1f3b-4861-b759-daa3584eace0 \
  --text "[worker_done] reviewer BE 검수 완료 — FAIL n · WARN n. review-be-report.md" --enter
```
