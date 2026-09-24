# 루프2 Phase BE-3 — 자동 초대 게이트 제거 · 체크리스트 읽기 범위

**allowed_paths**: `backend/` 만. `frontend/` 는 **다음 판(FE-4·FE-5)의 몫이니 건드리지 마라.**
커밋·push 금지. 서버·사용자 포트 금지. `make reset-demo` **금지**(사용자의 데모 데이터가 날아간다).

## 읽을 것

- 역할: `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/orchestration/roles/strong-hajin/backend/role.md` (+ 같은 폴더 `.md`) · 코드 레포 `AGENTS.md`
- **계약**: `.../para/projects/summer-star/strong-hajin/20-spec/spec-005-projects.md` **v0.2.0**
  — §4 의 「체크리스트·업무 내용의 읽기 범위」 절과 자동 초대 절
- **실행 계획**: `.../30-work/work-005-projects.md` **Phase BE-3** (네 몫이다)
- **결정**: `.../10-decision/decision-004-projects.md` — **D-28**(게이트 제거, ~~D-12~~ 를 대체) · **D-29**(읽기 범위)
- 1루프 산출물: `be-impl-report.md`(§6 실물 응답) · `review-be-report.md` · `be-fix-report.md`
- 조사: `loop2-survey-report.md` Q5(게이트 참조 4자리 · 깨지는 테스트 1건)

## 1. 자동 초대의 권한 게이트를 없앤다 (D-28)

- 지금은 **배정한 사람**이 그 프로젝트에서 배정 권한(`may_assign_in`)을 가져야 초대가 돈다
- **바꿀 것**: **배정이 성립하면 받는 사람을 `참여`(member)로 붙인다. 배정한 사람의 권한을 묻지 않는다**
- 붙는 kind 는 **`member` 그대로**. 멱등도 그대로(이미 붙어 있으면 아무 일도 안 일어난다)
- ⚠ **함께 움직이지 «않는» 것**: **업무를 올리는(배정하는) 게이트는 그대로다.**
  배정 자체의 권한 검사를 건드리면 안 된다 — 초대 게이트만 없앤다
- 조사가 센 것: `may_assign_in` 참조 **4자리, 그중 자동 초대는 1자리**.
  **나머지 3자리를 확인하고 손대지 마라.** 깨지는 테스트는 **1건**
  (`test_the_key_is_assigning_in_that_project_not_managing_it` 계열) — 그 테스트는 **이제 거짓이 된
  주장을 지키고 있다.** 지우지 말고 **새 계약을 지키는 테스트로 다시 써라**

## 2. 체크리스트·업무 내용을 프로젝트 구성원에게 연다 (D-29)

- **사용자 결정**: 「모든 프로젝트 구성원이면 서로의 업무 내용·체크리스트 다 보게」 —
  **리드·참여자 구분 없이**
- **지금**: `access` 가 **「활성 배정을 쥐었나」 하나로만** 갈린다
  (`application.py:940-943` → `work_tasks.py:1089`). **리드도 남의 체크리스트를 못 본다**
- **SPEC 이 정한 방식은 ⓑ 다** — **`access` 값을 3분화하지 않고**(그 값은 이미 밖으로 나가는
  계약이라 읽는 곳 전부가 움직인다) **`checklist` 를 싣는 조건만 따로 둔다.**
  SPEC §4 의 그 절을 그대로 구현하라
- **읽기만 연다. 쓰기 가드는 한 줄도 건드리지 마라** —
  `POST/PATCH/DELETE /api/tasks/{id}/checklist` · `POST .../checklist/order`
- `checklist_progress` 도 같은 범위로 (상세에서도 프로젝트 구성원에게)
- `description` 은 **이미 `read_only` 에도 온다** — 확인만 하고 건드리지 마라

## 3. ⚠ FE 가 받을 **실물 응답을 찍어 리포트에 붙여라** (1루프에서 이게 값을 했다)

다음 판 FE 워커가 **추측으로 짜지 않게** 해야 한다. 계약 테스트 하네스(TestClient) 안에서
**서버를 띄우지 않고** 찍어라:

1. `GET /api/tasks/{task_id}` — **내 업무일 때**와 **같은 프로젝트의 남의 업무일 때** 둘 다.
   `access` · `checklist` · `checklist_progress` · `description` 이 각각 어떻게 오는지
2. 자동 초대가 돈 뒤 `GET /api/projects` 가 **초대된 사람 눈에** 무엇을 내는지
3. **틀리기 쉬운 자리**를 1루프 리포트 §6 처럼 **목록으로** 적어라 (FE 가 그걸 보고 짠다)

## 4. 검증 — **기준선이 바뀌었다**

**Phase 0 가 닫혔다. 이제 「기준선 밖 실패 0」이 아니라 「실패 0」이 조건이다**
(코디 실측 2026-09-22 `make verify` exit 0).

- `make test-unit` · `make test-contract`(두 패스) · `make test-postgres` 를 돌려라
- **`@pytest.mark.serial` 규약**: 자식 프로세스를 띄우는 테스트를 **새로 만들면 마커를 달아야 한다.**
  안 달면 `conftest` 걸개가 병렬 패스에서 **즉시 실패**시키고 무엇을 달라고 말해 준다.
  **`-p no:randomly` 는 쓰지 마라**(미설치·무동작). 직렬은 `-n0`
- **실패가 나오면 그것이 네 탓인지 분리해 보고**하되, **이제는 「원래 깨져 있었다」가 없다**
- `tests/architecture` 경계와 operation inventory drift 확인(diff 항목만 패치)

## 5. 범위 제약

- **`frontend/` 0줄** — 다음 판 몫이다
- **SPEC 에 없는 계약을 만들지 마라.** 필요하면 리포트에 「막힌 것」으로 적고 나머지를 해라
- **`bootstrap/demo_work.py` 를 건드리지 마라** — 사용자의 E2E 데이터가 거기 있다
- 커밋·push·PR 금지

## 6. 리포트 (`orchestration/work/strong-hajin-projects/loop2-be-report.md`)

- 바꾼 파일과 **각각이 닫는 인수조건 번호**(SPEC §6 의 L-번호)
- **§3 의 실물 응답**과 「틀리기 쉬운 자리」 목록
- 테스트 수치 · 다시 쓴 테스트가 **무엇을 지키게 됐는지**
- 막힌 것 · 판단이 필요한 것

## 완료 보고 — **문구 변경 금지**

```bash
orca orchestration send \
  --to term_bdba055b-758b-4dc9-85c3-7836d56b615a --from term_1929293d-c8fe-468b-8d71-b889c1d43c99 \
  --type worker_done --task-id <taskId> --dispatch-id <dispatchId> \
  --subject "backend 완료: 루프2 BE-3" \
  --body "바꾼 파일 / 닫은 인수조건 / 실물 응답 찍은 경우 수 / 테스트 수치(실패 0인가) / 막힌 것"

orca terminal send --terminal term_bdba055b-758b-4dc9-85c3-7836d56b615a \
  --text "[worker_done] backend 완료 — 루프2 BE-3. 상세는 인박스." --enter
```
