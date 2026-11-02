# 리뷰 리포트 — strong-hajin-work / planner (WORK-001 W1 구현 계획, 2026-09-15)

## 판정: FAIL

문서 규율은 깨끗하다 — allowed_paths 이탈 0, 양식 충족, 8 phase 전부 `TODO`,
「완료 증거」 8개 전부 `미작성`, SPEC→WORK 역참조 0, 실행하지 않은 테스트를 통과로 적은 곳 0.

FAIL 사유는 **계획이 전제한 것이 이 레포에 없거나, 계획이 스스로와 어긋나는 자리 여섯**이다.
그대로 사용자에게 올리면 "migration 을 쓴다"·"멱등하다"·"승인자를 지정한다"를 할 수 있는
것으로 읽는다. 셋 다 지금 코드에서는 성립하지 않는다.

문서는 **거의 다 왔다.** 아래 필수 수정 여섯은 전부 범위가 좁고 계획 안에서 닫힌다 —
새 제품 결정이 필요한 것은 하나(F-3 의 선택지)뿐이고 그것도 세 안 중 하나를 고르는 일이다.

## 검수 범위

- 대상: `30-work/work-001-task-creation.md`(493줄, 신규) + R-1~6 정정이 들어간
  `baseline-001-work-page.md`(359줄) · `decision-001-work-page.md`(319줄) ·
  `spec-001-work-management.md`(813줄, v0.2.1) · `spec-002-action-item-review.md`(500줄, v0.2.1).
- 코디 소유 `30-work/README.md`(75줄, 신규) · `log.md` · 단계 index 는 **ID·링크 정합만** 확인.
- `git status --porcelain` 이 내는 `reference/2026-09-10-sc-meeting/task.md` 와 `temp.md` 는
  브리프 §4 지시대로 **제외**했다.
- 실행한 검사
  - 린트 — **실행 불가.** `scripts/lint-pipeline.py` 가 두 레포에 없다(`project.md:263` 기존 미결).
    `project.md` §3.2~3.5 와 `templates/projects/30-work/work.md` 수동 대조로 대신했다.
  - 코드 — 워크트리 `8973791…` read-only. `Makefile` · `AGENTS.md` · `backend/pyproject.toml` ·
    `bootstrap/reset.py` · `bootstrap/schema_sync.py` · `modules/work/application.py` ·
    `modules/work/task_creation.py` · `platform/organization_access.py` ·
    `modules/meetings/followups.py` · `entrypoints/http.py` ·
    `tests/architecture/{test_architecture,test_operation_inventory}.py` 직접 열람.
  - **테스트·빌드·DB 는 돌리지 않았다**(reviewer `tools.md` 금지, 브리프 §7).

## 필수 수정 (FAIL 사유)

### F-1. 이 레포에 migration 이 없다 — Phase 2·Rollback·Pre-deploy 가 없는 도구를 전제한다

- `work-001-task-creation.md:171` — "**Migration 필요 여부**: 필요하다(신규 컬럼 + 유일성 제약)"
- `:274` — "migration 을 쓴다. 기존 행 backfill·전환은 하지 않는다"
- `:281` — "migration 이 기존 데이터를 지우거나 옮기지 않는다 (**reset 없이** 적용 확인)"
- `:428` · `:432` — Pre-deploy 와 Rollback 이 "migration revert" 를 전제

근거 — 코드 워크트리 `8973791`:

1. **migration 프레임워크가 없다.** `backend/` 에 alembic·`migrations/` 디렉토리가 없고
   (`ls backend/` → `pyproject.toml scripts src tests uv.lock`), 스키마를 만드는 자리는
   `backend/src/ax_workspace/bootstrap/reset.py:20` `Base.metadata.create_all(engine)` **하나**뿐이다.
2. 기존 DB 를 모델에 맞추는 유일한 경로는 `make sync-demo-schema` →
   `bootstrap/schema_sync.py` 이고, 그 파일 자신이 `:6-7` 에서 이렇게 말한다 —
   "**It is a development convenience, not a migration tool: production schema change is a
   separate, gated piece of work.**"
3. **그 도구는 제약을 못 만든다.** `schema_sync.plan()`(`:19-47`)이 내는 DDL 은
   `CreateTable`(테이블이 아예 없을 때) 과 `ALTER TABLE … ADD COLUMN` **둘뿐**이다.
   `UniqueConstraint` 를 다루는 코드가 없고, `CreateIndex` 도 **새 테이블일 때만**(`:30`) 붙는다.
   → WORK-001 이 invariant 2 로 세운 "**활성 담당 유일성을 DB 제약으로**"(`:163` · `:272` · `:279`)는
   **기존 DB 에 적용할 길이 지금 없다.** 새로 `reset-demo` 한 DB 에서만 선다.
4. `make` 타겟에도 migration 이 없다(`Makefile:102` `reset-demo` · `:107` `sync-demo-schema` ·
   `:110` `reset-catalog` 가 전부).
5. 아키텍처 테스트가 DDL 자리를 못 박고 있다 —
   `backend/tests/architecture/test_architecture.py:64-69`
   `test_application_startup_never_mutates_schema` 가 `create_all` 호출을 막고
   "schema mutation belongs exclusively to `ax_workspace.entrypoints.reset_demo`" 를 단언한다.
   reviewer `rules.md` 의 backend 체크리스트도 같은 말이다.

**무엇을 고치나** — 셋 중 하나를 골라 계획에 적는다. 셋 다 새 제품 결정이 아니다.

| 안 | 내용 | 비용 |
|---|---|---|
| (a) 레포의 실제 경로를 쓴다 | 신규 **컬럼**은 `make sync-demo-schema` 로 더한다. **유일성 제약은 이 work 에서 DB 제약으로 세우지 않고** application + 부분 인덱스 대신 **`reset-demo` 한 환경에서만 검증**한다. 제약 도입은 별도 gated work 로 올린다 | 가장 작다. 다만 invariant 2 의 강도가 내려간다 — 그 사실을 계획에 적어야 한다 |
| (b) 이 work 에서 migration 도구를 도입한다 | alembic 등을 붙이고 `reset_demo` 전용 DDL 규칙·아키텍처 테스트를 함께 바꾼다 | W1 범위를 크게 넘는다. **권하지 않는다** |
| (c) `schema_sync` 를 제약까지 다루게 넓힌다 | `plan()` 에 `UniqueConstraint`·`Index` 처리를 더한다 | 중간. 이것도 별도 phase 로 세우고 "dev convenience" 경계를 다시 적어야 한다 |

어느 안이든 `:171` · `:274` · `:281` · `:428` · `:432` 의 「migration」 이라는 낱말을
**레포에 실제로 있는 이름**으로 바꿔야 한다. Rollback 은 "migration revert" 대신
"추가한 컬럼을 모델에서 빼고 `sync` 는 지우지 않으므로 컬럼이 남는다"는 사실을 적어야 한다 —
`schema_sync` 는 **더하기만 하고 지우지 않는다**(`:1` · `:44-45`).

### F-2. 테스트 명령이 이 레포가 금지한 형태다. #7 이 요구한 두 게이트가 빠졌다

- `work-001-task-creation.md:234` — "BE: `cd backend && uv run pytest -n auto --dist worksteal`"

근거 — `AGENTS.md`(`CLAUDE.md` 가 import 하는 저장소 공통 규칙) 「테스트」 절:

> 백엔드 테스트는 **항상 Makefile 타겟으로 실행한다.** `cd backend && uv run pytest ...`처럼
> **직접 호출하지 않는다** — 병렬 실행(`-n auto --dist worksteal`)이 빠지면 …

WP 브리프 §4 가 그 명령을 준 것은 사실이고 writer 는 브리프를 따랐다. 하지만 **그 레포에서
테스트를 어떻게 돌리는지의 SoT 는 그 레포의 `AGENTS.md`** 다. 계획서에 남으면 구현 세션이
그대로 따라 하고 hook·규율에 걸린다.

두 번째 문제 — **「전량」이 무엇인지 정의되지 않았고, 실제로 전량이 아니다.**

- `backend/pyproject.toml` `[tool.pytest.ini_options]` `addopts = "-m 'not integration and not
  release and not scale'"` → `make test` 는 integration·release·scale 을 **처음부터 제외**한다.
- 진짜 전량은 `make verify`(= `test test-scale test-release frontend-test frontend-assets
  frontend-build`, `Makefile:65`)이고, PostgreSQL 통합은 `make test-postgres`(`Makefile:52`)다.
- `source-issue-7.md` 인수조건이 **명시적으로** 요구한다 — "변경된 public behavior에 focused test와
  **PostgreSQL 통합 test**, 핵심 브라우저 journey를 추가한다. **`make verify`, 관련
  `make test-postgres`** 및 격리 DB의 acceptance journey로 검증한다."
- WORK-001 에 `make verify` 도 `make test-postgres` 도 **한 번도 나오지 않는다**(grep 0건).

**무엇을 고치나**: `:234-235` 를 `make test` · `make test-unit` · `make test-contract` ·
`make frontend-test` · `make verify` · `make test-postgres` 로 바꾸고, phase 별 검증에는
**그 phase 가 실제로 건드린 묶음**을 적는다(아래 W-4 참조). Phase 8 에 `make verify` 와
`make test-postgres` 를 최종 게이트로 세운다.

### F-3. 멱등성이 계획 안에서, 그리고 SPEC 과 함께 자기모순이다

- `work-001-task-creation.md:213` — "키는 **호출자가 준다.** **없으면 멱등 보장 없이** 평소대로 만든다"
- `work-001-task-creation.md:278` — Phase 2 검증 "**키 없는** 같은 명령의 **동시 실행** →
  중복 업무 0, 중복 활성 담당 0"
- `work-001-task-creation.md:454` — 인수조건 추적 "멱등 키 재전송 1건 · 동시 실행 중복 업무·중복 활성 담당 0"
- `spec-001-work-management.md:626` — "같은 명령의 **동시 실행이 중복 업무나 중복 활성 담당을
  만들지 않는다**"
- `spec-001-work-management.md:705-706` — AC "**키 없이도** 같은 명령의 동시 실행이 중복 업무나
  중복 활성 담당을 만들지 않는다"

**모순의 정확한 자리**: 키가 없으면 서버에는 "같은 명령"을 식별할 근거가 없다.
같은 사람이 같은 내용으로 **일부러 두 건**을 만드는 것과 네트워크 재시도가 **구별되지 않는다.**
`:213` 이 그 사실을 스스로 적어 두고, `:278` 이 그 상태에서 「중복 0」을 요구한다.
**두 줄이 같은 문서 안에서 반대 말을 한다.**

「중복 활성 담당 0」은 키와 무관하게 성립한다 — 한 업무당 활성 담당 0/1 은 업무별 invariant 다.
성립하지 않는 것은 **「중복 업무 0」** 한 조각이다.

**SPEC 도 같은 모순이다**(`:626` · `:705-706`). 그리고 그 뿌리는 원문이다 —
`source-issue-7.md` 인수조건 "권한 밖 요청/배정은 거부하며 **같은 명령 재시도·동시 실행은
중복 업무/활성 담당을 만들지 않는다.**" 원문도 "같은 명령"의 식별 근거를 주지 않았다.

**수정 범위** — 세 안. **어느 것을 고를지는 코디·사용자의 몫이고 이 리뷰가 정하지 않는다.**

| 안 | 계약 | 고쳐야 할 자리 |
|---|---|---|
| (a) **키를 필수로** | 생성 명령이 키 없이는 거부된다. "같은 명령"의 정의가 서고 AC 가 그대로 성립 | SPEC-001 `:403`(선택 → 필수) · `:489`(Validation) · `:624-626` · `:705-706` / WORK-001 `:213` · `:250` · `:278`. 모든 호출자(REST·MCP·AX·승격·FE)가 키를 실어야 한다 |
| (b) **서버 파생 자연 키** | 행위자+수신자+정규화 내용+시간창으로 서버가 키를 만든다 | 위와 같은 자리 + **부작용을 계약에 적어야 한다** — 같은 내용 두 건을 의도적으로 만들 수 없게 된다 |
| (c) **AC 를 좁힌다** (가장 작다) | 키 있는 재전송·동시 실행만 「중복 업무 0」을 보장한다. 키 없는 동시 실행은 **「중복 활성 담당 0」만** 보장하고, 화면의 이중 제출은 제출 중 버튼 비활성(`spec-001:630`)이 막는다. 원문 인수조건과의 차이를 미결로 적는다 | SPEC-001 `:626` · `:705-706` / WORK-001 `:213`(그대로 둠) · `:278` · `:454` |

(c) 는 새 제품 규칙을 만들지 않고 이미 있는 두 장치(키·FE 비활성)로 덮는다.

**추가로 빠진 것 — 키의 scope 와 권한 재검증.** `:211-217` 과 Phase 2 `:269` 어디에도
**키가 누구 것인지**가 없다. 키가 전역이면 A 가 B 의 키로 재전송했을 때 B 의 업무가
영수증으로 돌아온다 — 관계자 밖에 **존재를 알리지 않는다**는 계약(`spec-001:662`)이 깨진다.
내부 계약에 "키는 **행위자 scope** 안에서만 유효하고, 영수증을 돌려주기 전에 **지금도 그 사람이
그 업무를 읽을 수 있는지 다시 검사한다**" 두 줄을 넣어야 한다.

### F-4. 「최소 호환」이 승인자에 대해 성립하지 않고, 수평 요청의 갈림길이 계획에 없다

WORK-001 은 승인자 필드를 W1 에서 **저장하고 화면에 노출**한다 —
`:98`(Scope) · `:253`(Phase 1) · `:385`(Phase 7 "생성 창에 승인자 필드를 둔다") ·
`:396`(검증 "승인자를 비운 채 생성이 된다").
동시에 완료 경로는 **현행 그대로 둔다** — `:188-189` "완료·승인 흐름은 현행 그대로 둔다."

현행 코드가 무엇을 하는지(`8973791`):

- `modules/work/application.py:502-504` `requires_completion_review(task)` =
  `getattr(task, "source_work_request_id", None) is not None` — **요청 출신 Task 만** 승인을 요구한다.
- `:520-521` `submit_completion` 은 `requires_completion_review` 가 거짓이면
  "이 업무는 완료 보고 없이 바로 완료 처리합니다" 로 **거부**한다.
- `:529` `reviewer_id = self._requester_of(task)` / `:638-642` `_requester_of` 는
  `source_work_request_id` 로 WorkRequest 를 찾아 **`requester_id`** 를 돌려준다.

따라서 W1 만 적용한 상태에서:

1. **본인 생성 + 승인자 지정** → `source_work_request_id` 가 없다 → 완료 보고 자체가 거부되고
   바로 `done` 이 된다. **지정한 승인자는 아무 효과가 없다.**
2. **수평 요청 생성 + 요청자와 다른 승인자 지정** → 완료 확인은 여전히 `_requester_of`,
   즉 **요청자**에게 간다. 화면에서 고른 승인자와 **다른 사람**이 판정한다.
3. 두 경우 모두 사용자에게는 "승인자를 골랐다"로 보이고 제품은 그 선택을 **무시한다.**
   이것이 "최소 호환"이 아니라 **조용히 어긋나는 약속**이다.

**그리고 계획에 없는 갈림길 하나** — 수평 요청이 즉시 배정으로 바뀔 때
**`task.source_work_request_id` 를 계속 세우는가?**

- 세우면: 기존 완료 승인 의미가 유지된다(요청 출신 Task 는 완료 보고 필요).
  다만 승인자는 계속 요청자로 고정된다(위 2).
- 세우지 않으면(= WorkRequest 행 없이 Task 를 직접 만들면): `requires_completion_review` 가
  **전부 거짓**이 되어 **요청 업무의 완료 승인이 통째로 사라진다.** #7 W2.0 이
  "기존 TaskDelivery/완료 승인 ActionItem 은 **유지·활용**"이라고 못 박은 것과 정면으로 부딪친다.

WORK-001 Phase 4 `:314` 는 "수평 요청이 **판단 대기 상태 없이** 즉시 활성 담당을 세우게 한다"
까지만 적고 WorkRequest 행·`source_work_request_id` 의 처분을 말하지 않는다.
**이 한 줄이 기존 완료 승인의 존폐를 가른다.**

**무엇을 고치나** — W1 범위를 넓히지 않는 안전한 경계:

1. Phase 4 에 "**수평 요청 경로는 WorkRequest 행과 `source_work_request_id` 를 계속 세운다.
   수락 대기 상태만 걷는다**"를 **명시한다.** 그래야 완료 승인이 그대로 산다.
   (다르게 가려면 그건 W2 의 완료 모델 변경이므로 W1 이 아니다.)
2. 승인자는 **W1 에서 저장만** 하고 **화면에 노출하지 않는다** — `:385` · `:396` 의
   FE 작업을 W2 로 내린다. 저장·API 필드는 W1 에 남겨 W2 가 소비한다(`:181` Dependency 그대로).
   노출을 유지하려면 "지금은 완료 확인이 요청자에게 간다"는 사실을 UX 문구와 계획에 적어야 한다 —
   그편이 더 나쁘다. **저장만 권한다.**

### F-5. 기존 수평 요청 후보 목록을 그대로 쓰면 W1.5 가 깨진다 — Open Issue 1 의 세 안이 동등하지 않다

- `work-001-task-creation.md:473-475` Open Issue 1 — "새 역량을 만들지, 기존 조직 관계로 판정할지,
  **기존 수평 요청 후보 목록을 그대로 쓸지.** … Phase 3 에서 근거와 함께 정한다."

현행 후보 목록이 무엇인지 — `platform/organization_access.py:851-866`
`work_request_assignee_candidates`:

```
if member_id == str(principal.id) or not self._can_answer(member_id):   # :856  로그인 가능·본인 제외
if "work_request.decide" not in candidate.capabilities:  continue       # :861  ← 여기
if not principal.organization_scope.intersection(candidate.organization_scope): continue  # :863
```

`:861` 이 **`work_request.decide` 를 가진 사람만** 후보로 남긴다. 그 역량은
`modules/organization_access/catalog.py:99-118`(팀장) 계열에만 있고
`:77-95`(구성원)에는 **없다**(BASE-001 § 현행 코드 관측 W1.5 가 적은 그대로다).

→ **이 목록을 그대로 쓰면 일반 구성원은 후보에 한 명도 안 뜬다.** 그러면
Phase 3 검증 `:297` "배정 권한이 없는 구성원이 **허용 후보에게** 보내면 성공한다"는
후보가 팀장뿐인 상태로도 **공허하게 통과**하고, #7 W1.5(구성원 ↔ 구성원 수평 요청)는 깨진다.

**무엇을 고치나**: Open Issue 1 을 세 안 병렬로 두지 말고, **`:861` 의 `work_request.decide`
필터를 걷어야 한다는 사실**을 제약으로 못 박는다. 나머지 두 줄(`_can_answer` = 로그인 가능,
`organization_scope` 교집합)은 **그대로 재사용 가능한 판정**이고 `task.assign` 과 무관하다 —
즉 "개발자가 처음부터 정해야 하는 것"이 아니라 **한 줄을 빼는 일**이다.
Phase 3 검증에 "후보 목록에 **배정 권한도 판단 역량도 없는 일반 구성원이 뜬다**"를 더한다.

### F-6. "`self` 는 검사 없음" — 그대로 구현하면 인증 검사가 사라진다

- `work-001-task-creation.md:205` — "필요한 권한 검사 종류 (`self` 는 **검사 없음** ·
  `horizontal` 은 허용 후보 판정 · `managed` 는 배정 권한 + 조직 범위)"

현행은 검사가 있다 — `modules/work/application.py:155`
`create_self(...)` 첫 줄이 `self._require(principal, TASK_SELF_MANAGE)` 다.
 `spec-001-work-management.md:643` 도 "본인 업무 생성 | 로그인한 구성원 전원"으로
**로그인과 역량을 전제**한다.

지금 문장은 "이 경로엔 아무 검사도 필요 없다"로 읽힌다. 결정 함수를 새로 쓰면서 그대로 옮기면
`_require` 가 빠질 수 있고, 그러면 **인증·역량 검사 우회**가 된다.

**무엇을 고치나**: `:205` 를 "`self` 는 **수신자 대상 검사가 없다**(기본 역량 검사
`task.self_manage` 는 세 경로 모두 그대로 지난다)" 로 고친다. Phase 1 검증에
"세 경로 모두 역량 없는 principal 을 거부한다" 한 줄을 더한다.

## 구현 중 선택 가능 (WARN — 판정에 넣되 착수를 막지 않는다)

### W-1. 「배정 거절 명령이 어느 표면에도 없다」가 Open Issue 를 미리, 제거 방향으로 닫는다

- `spec-001-work-management.md:701` — AC "**배정 거절 명령이 어느 표면에도 없다.**"
- `work-001-task-creation.md:326` · `:450` — 같은 문장을 phase 검증과 인수조건 추적으로 옮겼다

반면 같은 문서들의 **계약 본문**은 전부 「신설하지 않는다」로 좁혀 있다 —
`decision-001-work-page.md:92`(D-4) · `spec-001:670` · `work-001:95` · `:316`.

현행 표면에는 거절 라우트가 실제로 있다 — `entrypoints/http.py:1392`
`POST /api/task-assignments/{id}/decline` · `:1982` `POST /api/work-requests/{id}/reject`.
「어느 표면에도 없다」를 글자대로 읽으면 **그 둘을 지워야** 하고, 그러면
`work-001:478-480` Open Issue 3("과거 수락 항목에 답하는 명령을 남길지 걷을지는 Phase 6 에서
정한다")이 **제거 쪽으로 미리 닫힌다.** 게다가 과거 행은 #7 D4 가 면제한 영역이다.

- 권장 수정: `spec-001:701` · `work-001:326` · `:450` 을 "**신규 생성 경로에** 배정 거절 명령이
  없다" 로 좁힌다. 나머지 네 자리가 이미 쓰는 표현과 같아지므로 새 결정이 아니다.
- **1차 재검수(이 리포트 앞 절)에서 `spec-001` 의 이 줄을 짚지 못했다.** v0.2.0 에도 같은 문장이
  있었다.

### W-2. 과거 수락 행의 읽기 검증은 D4 가 「요구하지 않는다」고 한 자리다

- `work-001-task-creation.md:318` — 작업 "과거 수락 항목의 **읽기**가 그대로 동작하는지 확인한다"
- `:327` — 검증 "과거 수락 행이 남아 있어도 목록·상세 조회가 깨지지 않는다"
- `:425` — Pre-deploy "과거 수락 대기 데이터가 그대로 남아 있고 읽힌다"

`source-issue-7.md` 인수조건 — "**기존 데이터 전환용 fixture·호환 처리는 요구하지 않는다.**"
D4 도 같다. `:327` 을 **필수 검증**으로 두면 옛 모양의 행을 만드는 fixture 가 필요해지고,
그게 D4 가 면제한 바로 그 작업이다.

- 권장: `:327` 을 필수 검증에서 **선택**으로 내리고, 대신 **작업 제약**으로 표현한다 —
  "읽기 경로(목록·상세·이력)의 코드를 지우지 않는다". fixture 없이 만족되고 의도도 같다.
  `:425` Pre-deploy 는 배포 직전 체크라 그대로 두어도 된다.

### W-3. Phase 3(권한)이 Phase 1~2(수신자 인자) 뒤에 있다

Phase 1 `:250` 이 수신자 인자를 열고, 허용 후보 판정은 Phase 3 `:291` 이 세운다.
`:434-436` Rollback 이 "Phase 1·2 만 되돌리면" 처럼 **phase 를 되돌릴 수 있는 단위**로 다루므로
Phase 1+2 만 머지된 중간 상태가 실재할 수 있다 — 그 상태는 **허용 판정 없이 타인 배정이 되는**
창이다.

- 권장(둘 중 하나): ① Phase 3 을 Phase 1 과 **같은 머지 단위**로 묶는다. ② Phase 1 에
  "**수신자 인자는 Phase 3 판정이 설 때까지 거부한다**"는 가드를 작업으로 넣고 그 가드 제거를
  Phase 3 작업에 적는다.

### W-4. phase 마다 「BE 테스트 전량」은 과하고, 정작 필요한 게이트가 없다

「전량 통과」가 네 자리에 있다 — `:260`(Phase 1) · `:282`(Phase 2) · `:374`(Phase 6) ·
`:415`(Phase 8, BE+FE). Phase 7 `:399` 는 FE 삼종.

F-2 에서 본 대로 그 「전량」은 실제로 `make test`(integration·release·scale 제외)다.
단계마다 같은 묶음을 네 번 돌리는 것보다, **그 phase 가 건드린 묶음 + 마지막 통합 1회**가
더 빨리 더 정확하게 깨진 자리를 가리킨다.

- 권장 배치 — 새 요구를 더하지 않고 있는 타겟에 나눠 담는다.

| Phase | 그 자리에서 | 근거 |
|---|---|---|
| 1 (입력·결정 함수) | `make test-unit` | 순수 도메인·입력 모델 |
| 2 (멱등·유일성·원자성) | `make test-contract` + 격리 DB 의 `make test-postgres` | 제약·동시성은 실제 DB 에서만 드러난다 |
| 3 (권한) | `make test-unit` + `make test-contract` | |
| 4·5 (수락 gate·승격) | `make test-contract` | |
| 6 (표면) | `make test` **+ 아래 W-5** | MCP·HTTP 시그니처가 움직인다 |
| 7 (FE) | `make frontend-test` + `npx tsc --noEmit` + `npx vite build` | |
| 8 (회귀) | **`make verify` + `make test-postgres`** | #7 인수조건이 지정한 최종 게이트 |

- **integration 을 환경 미확인으로 빼지 않아도 된다.** `Makefile:80-84` `postgres-up` 이
  `ax_test` · `ax_test_acceptance` 를 만들고, `:52-54` `test-postgres` 는
  `POSTGRES_TEST_URL` 이 `DATABASE_URL` 과 같으면 **실행을 거부**한다. 즉 격리 가드가
  이미 레포에 있다. `work-001:487-488` Open Issue 6 의 "확인 못 하면 BLOCKED" 는
  실제로는 `make postgres-up` 한 줄이다 — 그 명령을 계획에 적으면 닫힌다.

### W-5. MCP·HTTP 시그니처를 바꾸는데 operation inventory drift 작업이 없다

`AGENTS.md` — "MCP 도구·HTTP 시그니처를 바꿨다면 `tests/architecture/test_operation_inventory.py`
가 `docs/unified-operations-inventory.json` 과의 drift 를 잡아낸다 — 실패하면 실제/캡처된
스키마를 비교해 **diff 난 항목만** 패치한다(전체 재작성 금지)."

Phase 6 `:359-366` 이 REST 라우트와 MCP 도구·권한 표를 바꾸는데, WORK-001 전체에
`inventory` · `unified-operations` 가 **한 번도 나오지 않는다**(grep 0건).
그 테스트는 실재하고 baseline JSON 은 1.9MB 다(`docs/unified-operations-inventory.json`).

- 권장: Phase 6 작업에 "inventory drift 를 **diff 난 항목만** 패치한다" 한 줄,
  검증에 "`test_operation_inventory` 통과" 한 줄.

### W-6. 동시 승격 검증이 빠졌다

Phase 5 검증 `:345` 는 "같은 회의 후보를 **여러 번** 승격해도 업무는 1건" — 순차만 본다.
현행에는 이미 잠금이 있다(`modules/meetings/followups.py:20`
`followup_candidate(..., lock=True)` → `:21-27` `already_promoted`). 생성 층에 키가 들어오면
**두 층이 함께** 동작하므로 동시 승격을 한 줄로 검증할 수 있다.

- 권장: `:345` 옆에 "같은 후보의 **동시** 승격 두 건 → 업무 1건" 을 더한다.

### W-7. 코디 소유 index 의 열 하나가 frontmatter 와 어긋난다

`30-work/README.md:32` Work List 의 `Covers Spec` 이 **SPEC-001** 뿐인데,
`work-001` frontmatter `links.specs` 는 SPEC-001·SPEC-002 둘이다(`:28-30`).
바로 아래 `:40-41` Spec Coverage 는 둘 다 적는다. **코디 소유**라 판정에 넣지 않는다.

## R-1 ~ R-6 정정 확인 — 전부 해소

| # | 1차 지적 | 해소 | 근거 |
|---|---|---|---|
| R-1 | D2·N값이 「회사 결정 대기」로 묶임 | ✔ | `decision-001:290` OQ-B · `:292` OQ-D 가 **사용자 결정** 표로 옮겨졌고 "회사 기획이 미확정이라는 것은 **출처 사실**이고, 이 제품에서 닫는 사람은 **현재 사용자**다 — 회사 승인을 기다리지 않는다". 외부 의존(OQ-E·F·G)은 `:294-300` 에 그대로 남았다 — 옳은 분리 |
| R-2 | 위임전결 값이 「미조사」로 표기 | ✔ | `baseline-001:296` 이 "**조사로 닫히지 않는다** … PLAN-005(고정 revision 496줄)에 값이 없다 — 「전결」 0건 · `X-72` 0건 … 개인 프로젝트에서는 **사용자가 정할 값**". `:343` C-8 · `decision-001:291` OQ-C 도 같다. 내가 1차에서 확인한 사실과 **일치** |
| R-3 | 상세의 `open → done` 전이 부재 | ✔ | `spec-001:571` `open --> done: 완료 (상세 상단에서만)`. 행 액션과 구분됐고 원문 `SCREENDEF-004:1682`(담당자·시작 전 상단 고정 `[시작]·[완료]`)과 맞는다 |
| R-4 | `reply` 복수 규칙이 확정처럼 적힘 | ✔ | `spec-002:322` "**복수 분기를 지금 구현하지 않는다.** 「하나라도 남으면 `waiting` 을 유지한다」는 **안이 있으나** …" — 권고/미확정으로 내려왔다 |
| R-5 | 진행 기록 추가가 권한표에만 있고 API 없음 | ✔ | `spec-001:415` `POST /api/tasks/{id}/history` — "**진행 기록 추가 — 신규**. … 추가만 되고 고치거나 지우는 경로는 없다". 원문 `PLAN-001:205`(생성·조회) 및 `SCREENDEF-004:1492`(「구두로 받음 · {준 사람}」)·`:918`(`X-36`)과 맞는다 |
| R-6 | `INQUIRY_ALREADY_ANSWERED` 중복 | ✔ | 이제 `spec-002:350` **한 곳**뿐. SPEC-001 에서 걷혔다(grep 0건) |

**새 계약 모순 없음** — R-1~6 정정이 서로, 그리고 W1 계약과 부딪치는 자리를 찾지 못했다.
**W1 밖 미결이 gate 로 들어오지도 않았다** — `work-001:56-59` 가 "착수를 막는 미결이 없다"
라고 적고 OQ-A·D2·위임전결 값을 "이 work 에 닿지 않는다"로 갈랐다. 확인한 결과 맞다.

## 확인한 것 (PASS 근거)

체크리스트 항목별. 건너뛴 것은 이유를 적었다.

- **린트** — **확인 안 함(실행 불가).** `scripts/lint-pipeline.py` 부재. 수동 대조로 대체.
- **frontmatter·양식** — `templates/projects/30-work/work.md` 의 절 구성을 전부 갖췄고
  순서도 같다. `type: work` · `id: WORK-001` · `status: todo` · `progress: 0` ·
  `work_type: new-feature` · `owner` · `roles` 6종 · `tags` 3종 · `links` 6키.
  `project.md:180` 의 work 상태값(`todo`)과 맞고 `:184-187` 의 「전부 TODO 면 `todo`」 규칙과도 맞는다.
- **phase 상태** — `- **Status**: TODO` **8건**, `### Phase` **8건**,
  `완료 증거**: 미작성` **8건**. 셋이 정확히 일치한다. 브리프 §8 요구 충족.
- **실행하지 않은 것을 통과로 적지 않았다** — `:232` "검증 명령 (계획이다. **이 문서를 쓰는
  단계에서는 실행하지 않았다.**)". 완료 증거 8개 전부 미작성. **거짓 통과 주장 0건.**
- **SPEC → WORK 역참조 0** — `grep 'WORK-001\|work-001'` 을 BASE·DEC·SPEC 둘에 돌려 **0건**.
  `project.md:143-147` 단방향 규정 준수. 추적은 `30-work/README.md` 의 derived view 가 맡는다.
- **allowed_paths** — 이번 diff 의 신규/수정 파일이 WP 브리프 §5 다섯 경로와
  코디 소유 index 3건이다. **이탈 0.**
- **W1 한 slice 로 닫는가** — 브리프 §3 이 나열한 열세 표면이 전부 있다:
  생성(`:90`) · 일반 타인 요청(`:91`) · 관리자 배정(`:92`) · 회의후속승격(`:93` · Phase 5) ·
  수락제거(`:94` · Phase 4) · 권한(Phase 3) · 멱등(Phase 2) · 영속(`:131` · `:145-147`) ·
  REST·MCP·AX·seed(Phase 6) · FE(Phase 7). **누락 0.**
- **완료 승인·AX 확인 보존** — Phase 4 `:317` · `:324-325`, Phase 6 `:363` · `:370-371`.
  SPEC-002 §2.2 종류 표를 경계로 지목한다(`:311`) — 올바른 참조.
- **OQ-A·D2 임의 확정 없음** — WORK-001 에 OQ-A·D2 를 확정하는 문장이 없고
  `:59` 가 "이 work 에 닿지 않는다"로만 적는다. **계약 준수.**
- **D4 준수(데이터 전환)** — `:110`(Scope 제외) · `:147` · `:171-172` · `:274` ·
  `:433` 이 전환·backfill·DB reset·데이터 삭제를 전부 배제한다. W-2 한 자리만 경계에 걸린다.
- **운영 DB 적용을 착수 gate 로 넣지 않았다** — `:420-422` Pre-deploy 가 "**이 work 에 배포는
  없다.** 아래는 나중에 … 볼 항목이다"로 명확히 분리했다. 브리프 §6-3 의 우려는 **기우다.**
- **인수조건 추적** — `:439-459` 가 SPEC-001 §6 의 W1 인수조건 **열두 줄**을 phase 에 매핑하고
  "W2 인수조건(13번째 줄부터)은 이 work 가 닫지 않는다"로 경계를 적었다.
  SPEC-001 `:696-710` 과 대조 — **열두 줄 전부 대응되고 누락 0.**
- **BE/FE 경계** — Phase 1~6 BE, Phase 7 FE, Phase 8 양쪽. FE 가 Phase 3 의 후보 판정을
  소비한다는 의존을 `:383` 이 적는다. 경계 자체는 옳다(W-3 은 순서 문제이지 경계 문제가 아니다).
- **실제 파일 후보** — `:122-143` 의 22개 경로를 워크트리에서 확인했다. **전부 실재한다.**
  `task_creation.py`(`extra='forbid'` 설명도 맞다 — `:12-13`) · `organization_access.py` ·
  `meetings/followups.py` · `catalog.py` · `http.py` · `mcp.py` · `ds/` 부품 포함.
  누락된 자리는 W-5 의 inventory JSON 하나다.
- **코드 테스트·빌드·DB** — **돌리지 않았다.**
- **못 확인한 것**
  - 각 phase 의 **작업량·기간** — 계획에 산정이 없고(`README.md:24` "미산정") 나도 추정하지 않았다.
  - 멱등 키 저장 자리(새 표인지 기존 컬럼인지)의 구체안 — 계획이 Phase 2 로 미뤘고 그건 타당하다.
  - `dataset_import.py`·`scenario_csv.py` 의 `accept` 열 실제 구조 — 파일 존재만 확인했다.
  - FE 부품(`Tabs`·`Chip`·`Select`)이 필요한 변형을 지원하는지 — 존재만 확인했다.

## 기존 부채 (이번 판정 제외)

- `para/projects/project.md:263` — 문서 파이프라인 검증기·pre-commit 미이관. 이번에도 린트를
  돌리지 못한 직접 원인이다.
- 코드 레포에 migration 도구가 없다는 사실 자체(F-1 의 근거)는 이번 작업이 만든 부채가 아니다.
  **F-1 이 지적하는 것은 그 부채가 아니라, 없는 도구를 있는 것으로 적은 계획 문장**이다.

## 재검수 시 볼 것

필수 여섯 중 **F-2 · F-5 · F-6 은 문장 몇 줄**로 닫힌다(명령 교체 · 필터 한 줄 제약 명시 ·
검사 문구 정정). **F-1 · F-4 는 안을 고르는 일**이고(각각 세 안 / 두 안), 고른 뒤에는
계획 안에서 닫힌다. **F-3 만 SPEC-001 을 함께 고쳐야 한다**(`:626` · `:705-706`) —
writer 의 allowed_paths 안이므로 재발주로 처리 가능하다.

WARN 일곱은 전부 착수를 막지 않는다. W-1 은 SPEC 한 줄을 함께 좁히는 것이라
F-3 수정과 같은 턴에 하면 된다.

---

# 재검수 (1차) — WORK-001 수정본 · SPEC-001 v0.2.3 · SPEC-002 v0.2.2 (2026-09-15)

> 위 「판정: FAIL」과 F-1~6 · W-1~7 은 **최초 리뷰**의 판정이고 그대로 보존한다.
> 아래는 WP 필수 수정 + 두 추가 정정(fix1 · fix2) 뒤의 **재검수**이고, 판정도 따로 낸다.

## 재검수 판정: FAIL — 남은 자리는 **하나**다

최초 FAIL 여섯(F-1~6)과 WARN 일곱(W-1~7)은 **전부 해소됐다.** 요구가 축소된 자리는 없다 —
F-3 은 리뷰가 제시한 세 안 중 **가장 강한 (a) 키 필수**로 닫혔고, F-4 는 「저장만」이 아니라
**API 수용·FE 노출을 W2 와 같은 단위로** 내렸다. 둘 다 최초 리뷰가 요구한 것보다 강하다.

FAIL 사유는 **수정이 만든 새 계약 모순 한 자리**다 — **필수가 된 멱등 키가 REST 에서
본문 필드인지 헤더인지 문서가 두 말을 한다.** 고칠 줄은 셋이다(§ RF-1).
그 셋 말고 착수를 막는 것은 없다.

## 재검수 범위

- 대상 5문서: `work-001-task-creation.md`(722줄, +229) · `spec-001-work-management.md`(843줄, v0.2.3) ·
  `spec-002-action-item-review.md`(501줄, v0.2.2) · `decision-001-work-page.md`(380줄) ·
  `baseline-001-work-page.md`(359줄). 코디 소유 `30-work/README.md` · `log.md` ·
  `orchestration/config/projects/strong-hajin.json` 은 **정합만** 확인.
- 코드 대조: 워크트리 `8973791` read-only. 이번에 **새로 인용된 근거 줄을 전수로** 열었다 —
  `Makefile` · `bootstrap/{schema_sync,application}.py` · `entrypoints/{reset_demo,http,mcp}.py` ·
  `platform/{persistence,work_tasks,organization_access,actions,action_center}.py` ·
  `modules/work/{application,assignments,requests,request_lifecycle,task_creation}.py` ·
  `modules/organization_access/{catalog,application}.py` ·
  `tests/architecture/test_architecture.py` · `tests/integration/postgres/test_postgres_integration.py` ·
  `frontend/src/lib/{idempotency,api,viewModels,labels}.ts` · `features/work/{WorkModals,MyWorkPage}.tsx`.
- **테스트·빌드·DB 는 이번에도 돌리지 않았다**(reviewer `tools.md`, 브리프 §7). 린트는 여전히
  실행 불가(`scripts/lint-pipeline.py` 부재 — 기존 부채).
- `temp.md` · `reference/2026-09-10-sc-meeting/task.md` 는 브리프 §4 지시대로 제외.

## F-1 ~ F-6 — 전부 해소

| # | 최초 요구 | 해소 | 근거 (수정본 · 코드) |
|---|---|---|---|
| **F-1** | 없는 migration 을 전제하지 마라 | ✔ | `work-001:184-201` 「스키마를 어디에 세우나 — migration 을 새로 들이지 않는다」 표가 세 사실을 각각 코드 줄로 못 박는다. 내가 재확인: `schema_sync.py:6-7` "development convenience, not a migration tool" · `plan()` 이 내는 DDL 은 `CreateTable`·`ADD COLUMN` 둘뿐(`:28-45`) · `test_architecture.py:64-69` 가 `create_all` 을 `reset_demo` 에 묶는다. `:653-658` Rollback 이 "migration 이 없으므로 downgrade 도 없다"로 바뀌었고 「데이터 무손실」 발명이 사라졌다. `:641-651` Pre-deploy 도 "이 work 에 배포는 없다 + 기존 DB 절차는 별도 gated work". **DB 제약을 application 검사로 낮추지 않았다**(`:168-170` invariant 2) — 요구 축소 아님 |
| **F-2** | 레포가 금지한 `uv run pytest` · 빠진 두 게이트 | ✔ | `:330-343` 검증 명령표가 전부 make 타겟이고 `AGENTS.md` 「테스트」를 근거로 적는다. `grep 'uv run pytest'` **0건**. `make verify`(:631) · `make test-postgres`(:632) · `make acceptance-e2e`(:633-636)가 Phase 8 최종 게이트로 섰다. `:339` 가 "`make test` 는 「전량」이 아니다"를 `pyproject.toml addopts` 근거로 적는다 — 내가 확인: `addopts = "-m 'not integration and not release and not scale'"`(`backend/pyproject.toml:40`) |
| **F-3** | 멱등성 자기모순 | ✔ (가장 강한 안) | 세 안 중 **(a) 키 필수**. `work-001:171` invariant 3 · `:262-266` · SPEC-001 `:628-629` · AC `:727-728`. 최초 리뷰가 지적한 「키 없이도 중복 0」 문장이 SPEC 에서 **사라졌다**(`grep '키 없이' → :727 「키 없이 거부된다」 한 곳뿐`). 빠졌던 **키 scope 와 권한 재검사**도 들어왔다 — `:266-270`(행위자+명령 종류, 전역 아님) · `:275-276`·invariant 6(`:176-177`) · SPEC `:633-634`·`:528` |
| **F-4** | 「최소 호환」이 승인자에 성립하지 않음 · 수평 요청 갈림길 부재 | ✔ (요구보다 강함) | ① 갈림길이 닫혔다 — `:469-470` Phase 4 "**수평 요청은 WorkRequest 행과 `source_work_request_id` 를 계속 세운다. 걷는 것은 수락 대기 상태와 판단 회차뿐**". `:219-225` 가 그 근거로 `application.py:502-504`·`:529`·`:638-642` 를 인용하고, 내가 세 줄 다 확인했다. ② 승인자는 「저장만」이 아니라 **API 수용·FE 노출 둘 다 W2**(`:99-100` · `:107` · `:226-228` · `:385-386` · `:391-392` · `:567` · `:611`). **받아서 무시하는 API 0** — Phase 1 검증이 "승인자 필드를 보내면 거부된다"까지 적는다. `:215` 가 "W1 이 최종 승인자 계약을 충족한다는 뜻이 아니다"로 표현을 걷었다 |
| **F-5** | 후보 목록 세 안이 동등하지 않음 | ✔ | Open Issue 에서 내려와 **제약으로** 박혔다 — `:314-319` · Phase 3 `:433-435`. `work_request.decide` 필터 한 줄만 걷고 나머지 셋은 유지. 내가 재확인: `organization_access.py:851-866` 의 `:856`(`_can_answer`·본인 제외) · `:861`(decide 필터) · `:863`(scope 교집합), 그리고 `catalog.py:77-95` 구성원에 `work_request.decide` **없음** · `:99-118` 팀장에 있음. 검증 `:444-446` 이 "배정 역량도 판단 역량도 없는 구성원이 성공한다 + 후보 목록에 뜬다" 두 줄로 섰다. `:322-323`·검증 `:452-453` 이 **과거 판단 명령의 권한은 안 넓힌다**까지 막았다(`requests.py:290`·`:305`·`:327` 확인) |
| **F-6** | 「`self` 는 검사 없음」 | ✔ | `:249-257` 표 + 인용문. "`self` 가 「검사 없음」이 아니다. **수신자 대상 검사만 없다**". 세 경로 기본 역량을 코드 줄로 고정 — `application.py:155`(`TASK_SELF_MANAGE`) · `requests.py:247`(`WORK_REQUEST_CREATE`) · `assignments.py:101`(`TASK_ASSIGN`)·`:112`(`_may_put_on`), **전부 확인**. Phase 1 검증 `:390` 에 "세 경로 모두 인증·역량 없는 principal 을 거부한다". `:257` 이 "원래 없던 역량을 다른 경로에 더하지도 않는다"로 반대 방향도 막았다 |

## W-1 ~ W-7 — 전부 해소

| # | 최초 지적 | 해소 | 근거 |
|---|---|---|---|
| W-1 | 「어느 표면에도 없다」가 Open Issue 를 미리 닫음 | ✔ | SPEC-001 `:720` 이 "**신규 생성 경로에** 배정 거절 명령이 없다. (과거 행에 답하는 기존 명령을 지우라는 뜻이 아니다)" 로 좁혀졌다. WP `:485-487` · `:508` · `:677` 도 같은 표현이고, `http.py:1392`·`:1982` 를 **남기는 것**이라고 명시한다 |
| W-2 | 과거 수락 행 읽기 검증이 D4 면제 영역 | ✔ | 필수 검증에서 내려가 `:511-512` **선택 검증**이 됐고, `:489-490` 이 "읽기 경로 코드를 지우지 않는다"는 **작업 제약**으로 표현했다. fixture 를 만들지 않는다고 괄호로 덧붙였다 |
| W-3 | Phase 3(권한)이 Phase 1·2 뒤 | ✔ | `:365-372` **머지 단위 표** 신설. MU-A = Phase 1·2·3 한 덩어리. Rollback `:659-660` 도 "MU-A 를 쪼개 되돌리지 않는다"로 맞췄다 (단 § RW-1 참고) |
| W-4 | phase 마다 「전량」 4회 | ✔ | 사라졌다. phase 별로 `test-unit`(:395) · `test-contract`+격리 `test-postgres`(:424) · `test-unit`+`test-contract`(:455) · `test-contract`(:510·:538) · `make test`(:585) · `frontend-test`+`tsc`+`vite build`(:614) · `verify`+`test-postgres`+acceptance(:631-636). W-4 표와 사실상 같은 배치다. Open Issue 6(「환경 확인 못 하면 BLOCKED」)도 `:345-363` 실행 절차로 닫혔다 |
| W-5 | operation inventory drift 작업 없음 | ✔ | Phase 6 작업 `:564-566`("**diff 난 항목만**", `AGENTS.md` 근거) + 검증 `:584`("`test_operation_inventory` 통과"). 그 테스트는 `backend/tests/architecture/test_operation_inventory.py` 로 실재하고 `make test-unit` 에 포함된다(`Makefile:41`) |
| W-6 | 동시 승격 검증 없음 | ✔ | Phase 5 검증 `:531-532` "**같은 후보의 동시 승격 두 건 → 업무 1건.** 키가 서로 달라도 후보 identity 로 1건" (격리 PostgreSQL). invariant 8(`:179`)·`:303-305` 가 두 층을 갈라 적는다 |
| W-7 | README 열이 frontmatter 와 어긋남 | ✔ | `30-work/README.md:31` `Covers Spec` 이 `SPEC-001 · SPEC-002` 로 고쳐졌다 (코디 수정) |

## fix2 두 정정 — 문서 전반에 일관되게 들어갔다

- **`assigned` 출처 상태**: DEC-001 `:121-125`(D-3c) → SPEC-001 `:611` Data Contract ·
  `:689-691` Implementation Rules · AC `:735` → WP `:161` · `:474-479` · Phase 7 `:598-600`.
  **수행 상태와 다른 축**이라고 세 문서가 같은 말로 적고, 기존 다섯 값의 뜻을 바꾸지 않는다고
  못 박는다. 가짜 accept 금지도 코드 줄과 함께 섰다 — `:471-473`(`record_decision(…,"accept")`·
  `work_request.accepted` 감사 없음, `accepted_at` 은 `work_tasks.py:358` 본인 생성과 같은 뜻).
- **MCP 명시 키 · 서버 fallback 없음**: DEC-001 `:103-116` → SPEC-001 `:639-641` · AC `:732-733`
  → WP `:288-302` · Phase 6 `:555-561`. `AX_MCP_CAUSATION_ID` 하나로 키를 만드는 서술이
  **전부 사라졌고**(`:289` 가 "turn 을 가리킬 뿐 생성 의도를 가리키지 않는다"로 뒤집었다),
  `:296-298` 이 "같은 turn 에서 두 건은 서로 다른 키 · payload 는 키 재료가 아니라 지문"을 적는다.
  W1 resolver 범위 제한도 `:299-302` · `:559-561` 에 두 번 적혀 있다.

## 이번 판정의 필수 수정

### RF-1. **필수가 된 멱등 키가 본문 필드인지 헤더인지, 문서가 두 말을 한다**

같은 SPEC 안에서 정반대다.

- `spec-001-work-management.md:449` — `POST /api/tasks` **요청 필드 표**의 한 행:
  `| `idempotency_key` | ✔ | **신규·필수.** … 없거나 빈 값이면 거부된다 |`
  같은 표의 나머지 다섯 행(`content`·`assignee_id`·`due_date`·`approver_id`·`source`)은 전부
  진짜 **본문 필드**다. 그 자리에 있으면 본문 필드로 읽힌다.
- `spec-001-work-management.md:493` Validation 표도 같은 이름으로 한 행.
- `spec-001-work-management.md:639` — "**키는 표면마다 호출자가 싣는다** … REST 는
  **`Idempotency-Key` 헤더**, MCP 생성 도구는 `idempotency_key` 를 명시적 인자로 받는다".

WP·DEC 는 **헤더 쪽 한 말**이다 — `work-001:287`(REST 호출자 표) · `:553-554`(Phase 6 작업,
`http.py:620`·`1085`·`1785` 를 근거로) · `decision-001:105`. `grep '헤더'` 결과 다섯 자리가
전부 헤더를 말하고, **본문/헤더 우선순위나 불일치 처리를 적은 자리는 어디에도 없다.**

**왜 그냥 두면 안 되나** — 이 레포에서 그 두 선택은 **같은 것이 아니다.**

1. `POST /api/tasks` 의 요청 본문 모델은 **모듈 입력 모델 자신**이다 —
   `entrypoints/http.py:58` `from …task_creation import TaskCreateInput as CreateTaskRequest`,
   `:1251-1252` 가 그것을 그대로 body 로 받는다.
2. 그 모델은 `extra='forbid'` 다(`modules/work/task_creation.py:13`). 그래서
   **헤더로 가면 `idempotency_key` 를 본문에 넣는 순간 422 로 거부**되고,
   **본문으로 가면 헤더는 아무도 읽지 않는다.** 둘 다 되는 중간은 없다.
3. WP 자신도 이 긴장을 안고 있다 — Phase 1 작업 `:381` 은 "**생성 입력에 수신자·멱등 키를 연다**"
   이고, 같은 phase 설명 `:378-379` 가 그 「생성 입력」이 곧 REST 본문 모델이라고 적는다.
   그런데 `:287`·`:553` 은 REST 를 헤더로 못 박는다. **Phase 1 과 Phase 6 이 서로 다른 자리에
   같은 필수 값을 놓는다.**

**최소 diff — 세 줄. 새 결정이 아니다** (헤더는 DEC-001 D-3b 가 이미 정했다):

- `spec-001:449` — 행 이름을 `Idempotency-Key`(헤더)로 바꾸고 뜻에 "**본문이 아니라 요청 헤더로
  싣는다**" 를 붙인다. (표 제목이 「필드」이므로 행을 표 밖 한 줄로 빼도 된다.)
- `spec-001:493` — 같은 한 마디를 덧붙인다.
- `work-001:381` — "생성 입력에 **수신자**를 연다. **멱등 키는 `Idempotency-Key` 헤더로 받아
  결정 함수에 넘긴다 — 본문 필드로 열지 않는다**(`task_creation.py:13` `extra='forbid'`)" 로 고친다.
  Phase 1 검증 `:393`(키 누락 거부)은 그대로 성립한다.

이 셋 말고 F/W 잔여는 없다.

## 이번 판정의 경미 (WARN — 착수를 막지 않는다)

### RW-1. MU-A 가 머지되는 순간 `assignee_id` 는 이미 밖에서 보인다 — `:371` 과 어긋난다

- `work-001:371` — "MU-C … **타인 생성이 밖에서 보이는 것은 여기서 처음**이고, 그때 권한 판정은
  이미 MU-A 에 있다"
- 그런데 Phase 1(=MU-A)이 여는 그 모델이 곧 REST 본문이다(`http.py:58`·`:1251-1252`).
  MU-A 가 머지되면 `POST /api/tasks` 는 **그 시점에** `assignee_id` 를 받기 시작하고,
  라우트는 Phase 6(MU-C)까지 그 값을 application 에 넘기지 않는다(`http.py:1252-1262` 가
  이름을 하나씩 짚어 넘긴다) — 즉 **받아서 무시하는 창**이 MU-A~MU-B 동안 열린다.
- 권한 구멍은 아니다(판정이 MU-A 안에 있다). 다만 같은 문서가 `:100` 에서 "**받아서 무시하는
  API 를 만들지 않는다**"를 승인자에 대해 규율로 세웠으므로, 같은 규율을 스스로 어긴다.
- 권장(한 줄): MU-A 표에 "**REST 라우트가 `assignee_id` 를 실제로 읽는 것은 MU-C 다. 그 전까지
  본문에 오면 거부한다**" 를 적거나, `:371` 의 "밖에서 보이는 것은 MU-C 가 처음" 을
  "**밖에서 동작하는 것은** MU-C 가 처음" 으로 정확히 고친다.

### RW-2. `assigned` **전수 목록에 「쓰는 자리」와 판단함 한 자리가 빠졌다**

- `work-001:480-483` 이 세는 자리: `work_tasks.py:1370` · `requests.py:808` ·
  `request_lifecycle.py:133`·`:147`·`:190` · `viewModels.ts:459` · `labels.ts:22-34`.
  **일곱 다 실재하고 정확하다**(전부 열어 확인).
- 빠진 둘:
  - `platform/work_tasks.py:901` `state="pending"` — **신규 경로가 `assigned` 로 바꿔야 하는
    바로 그 줄**이다(`create_request`, `:878~`). 목록이 「읽는 자리」라 빠진 것은 이해되지만,
    쓰는 자리가 계획 어디에도 이름으로 없다.
  - `platform/action_center.py:302` `request_state=str(request.state)` — `is_work_request_replay`
    로 들어가는 읽기 자리. 신규 경로가 판단 항목을 안 만드니 `assigned` 가 여기 닿을 일은
    없어 보이지만, 「전수」를 표방한 목록 밖이다.
- 권장: 두 줄을 목록에 더한다. `:123` 이 "착수할 때 같은 검색을 다시 돌린다"고 적어 두어
  실제 위험은 낮다.

### RW-3. AX 표면의 「안정 키」를 레포 안에서 보장하는 작업이 없다

- `work-001:289` — "**AX 런타임도 논리적 도구 호출마다 안정 키를 실어 보낸다**".
  이것은 **호출자(모델·외부 클라이언트) 쪽 계약**이고, Phase 6 작업에는 도구 인자를 여는 줄
  (`:555-558`)은 있으나 **도구 설명·스키마로 그 규칙을 호출자에게 알리는 줄이 없다.**
- 서버 쪽 검증(`:580` 「응답을 잃은 호출자가 같은 키로 다시 부르면 1건」)은 서버만 본다.
  호출자가 재시도마다 새 키를 만들면 계약은 조용히 무너지는데, 그 실패는 서버 테스트에 안 잡힌다.
- **승인된 방향(명시 키·fallback 금지)을 다시 열자는 말이 아니다.** 그 방향을 지키려면
  Phase 6 작업에 "`idempotency_key` **인자 설명에 「한 생성 의도에 한 개, 재시도에는 같은 값」을
  적는다**" 한 줄이면 된다.

### RW-4. 근거 표기의 사소한 어긋남 둘 (내용은 맞다)

- `work-001:288`·`:558` — "`create_meeting` 도구가 `idempotency_key` 를 인자로 받는다
  (`mcp.py:695`·`:704`)". 실제 메서드 이름은 `create_current_meeting`(`mcp.py:694`)이고
  인자는 `:695`, fallback 은 `:704` — **줄은 맞고 이름만 다르다.**
- `work-001:286` — "대화 전송·회의실 예약이 그렇게 한다(`lib/api.ts:455`·`:715`·`:928`)".
  `:455` 대화 · `:928` 회의는 맞고, `:715` 는 **요청 댓글**(`/api/work-requests/{id}/comments`)이다.
  셋 다 `Idempotency-Key` 헤더를 싣는 것은 사실이라 주장은 서지만 이름이 하나 어긋난다.

## 브리프 §6 검수 항목별 결과

1. **F/W 해소·잔여** — 위 두 표. **요구가 축소된 자리 0.** F-3·F-4 는 오히려 최초 요구보다
   강하게 닫혔다. 잔여는 RF-1 하나.
2. **`assigned` 의 연결** — 저장(`:161`·`:469-470`) → 조회(`:480-483`) → FE(`:598-600`) →
   완료 승인(`:497-501`)이 한 줄로 이어진다. **가짜 수락·판단 회차 없는 경로가 실제로 가능하다** —
   `create_accepted_task`(`work_tasks.py:1221-1268`)가 이미 `open_decision_item`/`current_submission`
   의 **None 을 견디게** 짜여 있고(`:984-996` 이 None 을 돌려준다, `:1241-1242`·`:1262-1263` 이
   `… if item else None`), `assignment_kind="request_effect"` · `status="active"` ·
   `accepted_at=now` · `source_work_request_id=request.id` 를 그대로 세운다. 판단 항목 세 줄
   (`:939-963`)만 건너뛰면 **완료 승인 연속성이 그대로 산다.** `_decision_target`(`requests.py:808`)이
   `{pending, negotiating}` 밖을 거부하므로 `assigned` 에 판단 명령이 안 걸린다는 주장도 성립한다.
   FE 는 `workRequestStateLabel: Record<WorkRequest["state"], string>`(`labels.ts:21`)라
   union 에 `assigned` 를 더하면 **타입이 라벨 누락을 강제로 잡는다**(`WorkModals.tsx:1949` ·
   `MyWorkPage.tsx:934`). **승인자를 받아서 무시하는 중간 상태는 없다**(§ F-4). 빠진 것은 RW-2 둘.
3. **MCP 네 도구·호출자 재시도·동일 turn·권한 재인가·payload 충돌·동시 승격·resolver 범위** —
   네 도구가 실재한다: `create_self_task`(`mcp.py:609`) · `create_work_request`(`:328`) ·
   `assign_task`(`:1028`) · `promote_current_meeting_todo`(`:756`). 명시 인자·누락 거부(`:555-557`),
   동일 turn 다중 의도(`:296-298`·검증 `:579`), 재시도(`:580`), 권한 재인가(`:406-407`·`:420`),
   payload 충돌(`:408`·`:417`·`:578`), 동시 회의 후보(`:531-532`), actor/조직 격리(`:581`)가
   전부 닫혔다. **W1 resolver 가 다른 mutation 에 번지지 않는다** — `:299-302`·`:559-561`·`:583` 이
   공용 `_mutation_key`(`mcp.py:627-632`)를 일괄 변경하지 않는다고 두 번 적고, 그 helper 를 쓰는
   일일보고 초안(`mcp.py:252`)·회의 예약 fallback(`:704`)을 이름으로 짚는다. 남은 것은 RW-3.
4. **wire 계약 일치** — **여기서 갈렸다. § RF-1.** W1→W2 public 필드 경계는 **명시됐다** —
   승인자는 WP 일곱 자리(`:99-100`·`:107`·`:209`·`:228`·`:385-386`·`:567`·`:611`)에서 W2 로
   갈렸고, SPEC 은 최종 계약이라 §6 AC 가 W1/W2 를 나눠 적는다(`:716` · `:742`).
5. **격리 DB · 안전 가드 — 실제로 가능하다. 기존 사용자 DB 에 작용하지 않는다.**
   `work-001:347-352` 네 줄을 명령·코드로만 검증했다(실행하지 않음):
   `make postgres-up`(`Makefile:80-84`, `ax_test`·`ax_test_acceptance` 생성) →
   `CREATE DATABASE ax_test_w1` → `make reset-demo DATABASE_URL=…/ax_test_w1`
   (`Makefile:102-103` 이 `DATABASE_URL` 을 그대로 넘긴다) →
   `make test-postgres POSTGRES_TEST_URL=…/ax_test_w1`(`Makefile:52-54`, `AX_POSTGRES_TEST_URL` 로 전파).
   이름 `ax_test_w1` 은 `reset_demo.py:15` `_SAFE_POSTGRES_DATABASE`
   = `^ax_(?:demo|test)(?:_[a-z0-9_]+)?$` 를 **통과**하고, host 도 `localhost` 라
   `_LOCAL_POSTGRES_HOSTS` 안이다. 통합 테스트는 `AX_POSTGRES_TEST_URL` 이 없으면 **skip**
   (`test_postgres_integration.py:198-201`)이고 있으면 스스로 `reset_database`(`:54`·`:212`) 한다.
   사람이 쓰는 기본 `DATABASE_URL`(`Makefile:1`, `ax_demo`)은 이 네 줄 어디에도 등장하지 않고,
   `Makefile:52` 가 `POSTGRES_TEST_URL == DATABASE_URL` 이면 **실행을 거부**한다.
   acceptance 도 자기 DB 다 — `ACCEPTANCE_DATABASE_URL`(`Makefile:13`, `ax_test_acceptance`)을
   `Makefile:329` 가 스스로 reset 한다. **기존 사용자 DB 에 작용하는 경로를 찾지 못했다.**
6. **MU 머지 단위** — 논리 phase 와 배포 단위를 혼동하지 않았다. MU-A 가 입력·멱등·권한을
   한 덩어리로 묶어 W-3 의 창을 닫고, Rollback `:659-661` 이 MU 단위·역순까지 적는다.
   **필수 키·권한·생성 public 표면이 따로 깨지는 배치는 없다.** 다만 「밖에서 보이는 시점」의
   표현이 코드와 어긋난다 — § RW-1.
7. **보고** — 아래 두 절.

## 사용자에게 리뷰 가능한 구현 범위 (다섯 줄)

1. **한 번의 생성 명령으로 남의 목록에 업무가 선다** — 본인·동료 수평 요청·관리자 배정·회의 후속
   승격 넷이 **같은 결정 함수**를 지나고, 상대의 수락 없이 `내 업무`에 즉시 서서 바로 시작된다.
2. **일반 구성원이 동료에게 보낼 수 있다** — 관리자 배정 권한을 주지 않고, 후보 판정에서
   `work_request.decide` 필터 한 줄을 걷어서만 연다. 기존 조직 범위·본인 제외·재직 검사는 그대로다.
3. **생성은 멱등이다** — 모든 생성 명령이 키를 필수로 받고, 같은 키 재전송은 영수증,
   같은 키·다른 내용은 충돌, 다른 키·같은 내용은 별개 두 건. 한 업무의 활성 담당은 DB 제약으로 0/1.
4. **기존 완료 승인이 그대로 산다** — 수평 요청은 출처 행(`assigned`)과 `source_work_request_id`
   를 계속 세우므로 완료 확인자가 요청자로 이어진다. 사람이 하지 않은 「수락」은 기록하지 않는다.
5. **승인자·완료 모델·문의·업무 페이지 개편은 이 단계가 아니다** — 승인자는 저장 자리만 만들고
   입력·화면 모두 W2 에서 완료 경로와 **같이** 켠다. 이 work 는 #7 을 끝내지 않는다.

## 남은 비차단 사항 (RF-1 을 고친 뒤에도 남는 것)

- RW-1~RW-4 넷. 전부 한 줄 이하의 문장 수정이고 착수를 막지 않는다.
- **일정·작업량 산정이 없다**(`30-work/README.md:24` "미산정"). 이번에도 추정하지 않았다.
- Open Issues 넷(`:700-711`)은 전부 **구현 중 결정**으로 남았고 사용자 결정이 아니다.
  OQ-A · D2 · 위임전결 값은 이번에도 **확정되지 않았다** — 확인 결과 그대로다.

## 확인한 것 / 못 확인한 것

- **allowed_paths** — 수정된 다섯 문서가 fix1 §5 · fix2 §5 안이다. **이탈 0.**
  `temp.md` · `reference/…/task.md` 는 손대지 않았다(`git status` 상 untracked 그대로).
- **양식·phase 규율** — `### Phase` 8 · `- **Status**: TODO` 8 · `완료 증거**: 미작성` 8.
  셋이 정확히 일치한다. **실행하지 않은 검증을 통과로 적은 곳 0**(`:330` 이 "하나도 실행하지
  않았다"를 명시).
- **SPEC → WORK 역참조 0** — `grep 'WORK-001\|work-001'` 을 SPEC 둘 · DEC · BASE 에 돌려 **0건**.
- **코디 index/config 정합** — `30-work/README.md:31`(W-7 수정 확인) · `:40-41` Spec Coverage ·
  `log.md:15`(SPEC-001 0.2.3 · 재검수) · `orchestration/config/projects/strong-hajin.json`
  backend/frontend `verify` 가 Makefile 타겟 기준으로 정정됐다. **문서와 어긋나는 자리 없음.**
- **인용 근거 전수 대조** — 이번 수정본이 새로 인용한 코드 줄 **40여 자리를 전부 열어 확인했다.**
  어긋난 것은 RW-4 의 이름 둘뿐이고, **줄 번호가 틀린 자리는 없었다.**
- **테스트·빌드·DB** — **돌리지 않았다**(브리프 §7 · reviewer `tools.md`). 5번 항목의 격리 검증은
  **명령·코드 읽기로만** 판단했다.
- **린트** — **확인 안 함(실행 불가).** `scripts/lint-pipeline.py` 가 두 레포에 없다(기존 부채,
  `project.md:263`). 양식은 `templates/projects/30-work/work.md` 수동 대조로 대신했다.
- **못 확인한 것**
  - 멱등 원장을 새 표로 둘지 기존 행에 붙일지 — Phase 2 로 미뤄졌고 그건 타당하다(Open Issue 1).
  - `dataset_import.py` · `scenario_csv.py` 의 `accept` 열 실제 구조 — 존재만 확인했다.
  - AX 런타임(레포 밖)이 실제로 안정 키를 실을 수 있는지 — **확인 불가.** § RW-3.
  - `docs/unified-operations-inventory.json`(1.9MB)의 실제 drift 규모 — 열지 않았다.

## 기존 부채 (이번 판정 제외 — 최초 리뷰와 동일)

- `para/projects/project.md:263` — 문서 파이프라인 검증기 미이관. 이번에도 린트를 못 돌린 원인.
- 코드 레포에 migration 도구가 없다는 사실 자체. **이번 수정은 그 사실을 계획에 정확히 반영했다.**

---

# 재검수 (2차) — RF-1 · RW-1~4 최소 diff (2026-09-15)

> 최초 리뷰(F-1~6 · W-1~7)와 재검수 1차(RF-1 · RW-1~4)의 판정은 위에 그대로 둔다.
> 이번은 **fix3 최소 정정만** 본다. 이미 해소 확인한 항목은 재개방하지 않았고,
> 전체 재조사도 하지 않았다.

## 재검수 2차 판정: PASS — **사용자 리뷰로 넘길 수 있다**

RF-1 과 RW-1~4 **다섯 전부 해소**됐다. 수정이 만든 새 모순은 찾지 못했다.
비차단 관찰 한 건만 아래에 적는다(착수를 막지 않는다).

## 검수 범위

- 대상: `spec-001-work-management.md`(846줄, **v0.2.4**) · `work-001-task-creation.md`(738줄).
  fix3 §5 allowed_paths 두 경로 그대로 — **이탈 0.**
- 확인 방법: 키 관련 표현 **전수 grep** + 해당 절 직접 열람 + 새로 인용된 코드 줄 재확인.
- **테스트·빌드·DB 는 돌리지 않았다.** 실행하지 않은 것을 통과로 적지 않았다.

## 항목별

| # | 판정 | 근거 (파일:줄) |
|---|---|---|
| **RF-1** REST 키는 헤더로 일원화 | **해소** | `spec-001:442-444` — 본문 표 **위**에 "멱등 키는 `Idempotency-Key` 헤더로 받는다. **JSON 본문의 필드가 아니다** … 본문에 `idempotency_key` 를 실어 보내는 것은 **허용하지 않는다**". `:445-451` 본문 필드 표에서 **`idempotency_key` 행이 사라졌다**(남은 다섯은 전부 진짜 본문 필드). `:496` Validation 이 "**REST 는 `Idempotency-Key` 헤더**(본문 필드가 아니다), **MCP 는 생성 도구의 명시적 인자**" 로 두 표면을 갈랐다. `:544` sequence 가 `body: assignee_id / header: Idempotency-Key`. `:642-643` §5 원문과 일치. WP 쪽도 같다 — `work-001:379-380`(Phase 1 설명) · `:383-385`(작업: 본문 모델에 열지 않는다) · `:399`(검증: 본문 `idempotency_key` 를 보내면 거부) · `:127`(Code Surface). **두 문서 전체 grep 결과 「본문 필드」로 읽히는 자리 0.** MCP 명시 인자 계약은 그대로 유지됐다(`spec-001:643`·`:735`, `work-001:288`·`:568-572`) |
| **RW-1** 받아서 무시하는 창 제거 | **해소** | `work-001:386-388` 작업 — "**내부 입력 모델과 외부 REST 요청 모델을 가른다** … **MU-A·MU-B 동안 REST 요청 모델은 `assignee_id` 를 받지 않는다.** 라우트가 그 값을 실제로 소비하는 **MU-C 에서 함께 연다** — 받아 두고 무시하는 중간 상태를 만들지 않는다". 검증 `:400-401` — "MU-A·MU-B 시점의 REST 생성 요청에 `assignee_id` 를 실으면 **명시적으로 거부된다**(조용히 무시되지 않는다)". 반대편도 닫혔다 — Phase 6 작업 `:558-560` 이 "**이 단위에서 생성 요청 모델의 `assignee_id` 를 열고, 같은 커밋에서 라우트가 그 값을 소비한다**(MU-A·MU-B 의 거부 가드를 여기서 걷는다)". MU 표 `:371` 도 "REST 요청 모델이 `assignee_id` 를 받기 시작하는 것도 여기다 — 라우트가 그 값을 실제로 소비하는 자리와 같은 단위다" 로 정정됐다. **여는 자리와 걷는 자리가 같은 줄로 맞물린다** |
| **RW-2** `assigned` 전수 목록 | **해소** | `work-001:489-494` 가 「읽는 자리」에서 「**쓰고 읽는** 자리」로 바뀌었고, **쓰기** `platform/work_tasks.py:901`("`create_request` 가 지금 `state="pending"` 을 박는 자리")와 **읽기** `platform/action_center.py:302`(`request_state` 재전송 판정)가 들어왔다. 기존 일곱(`work_tasks.py:1370` · `requests.py:808` · `request_lifecycle.py:133`·`:147`·`:190` · `viewModels.ts:459` · `labels.ts:22-34`)은 그대로다. 두 줄 다 코드에 실재함을 1차에서 확인했고 이번에 재확인했다 |
| **RW-3** MCP 키 인자 설명 | **해소** | Phase 6 작업 `:573-575` 신설 — "**그 인자의 설명과 도구 스키마에 규칙을 적는다** — 「한 생성 의도에 키 하나 · 재시도는 같은 키 · 새 생성 의도는 새 키」. 외부 호출자는 스키마만 보고 부르므로, 설명이 없으면 매 호출 새 키를 만들어 계약이 깨진다". 1차 RW-3 이 요구한 그대로이고 승인된 방향(명시 인자·fallback 금지)을 바꾸지 않는다 |
| **RW-4** 근거 이름 정정 | **해소** | `work-001:288` · `:571` — `create_meeting` → **`create_current_meeting`**(`entrypoints/mcp.py:694-704` · `:694`·`:704`). `:286` — "대화 전송(`lib/api.ts:455`) · **요청 댓글**(`:711-717`) · 회의 생성(`:925-931`)". 세 자리 모두 코드와 일치한다(`api.ts:713-717` = `/api/work-requests/{id}/comments`, `:926-930` = `/api/meetings`) |

## 새 모순 좁은 확인 — 없음

- 키를 **본문**으로 읽히게 하는 잔재 0(두 문서 전수 grep).
- MCP 명시 인자·서버 fallback 금지·키 scope·W1 전용 resolver 한정은 **한 글자도 안 바뀌었다**
  (`work-001:288`·`:576-578`, `spec-001:642-643`).
- 승인된 나머지(DB 검증 격리·`assigned` 출처·완료 승인 연속성·권한 판정·MU 구성)도 그대로다.
- **phase 규율 유지** — `### Phase` 8 · `- **Status**: TODO` 8 · `완료 증거**: 미작성` 8.
- SPEC 버전이 `0.2.4` 로 갱신됐다(`spec-001:7`).

## 비차단 관찰 하나 (이번 판정에 넣지 않는다)

- **키 헤더 「필수」가 켜지는 시점과 FE 가 키를 싣기 시작하는 시점이 다른 머지 단위다.**
  Phase 1(=MU-A) 작업 `:383` 이 라우트에서 헤더를 받게 하고 검증 `:402` 가 "헤더가 없거나 빈 값이면
  거부된다"를 세우는데, FE 가 키를 싣는 작업은 Phase 7(=MU-C) `:618-619` 다.
  MU-A~MU-B 동안 기존 생성 화면은 헤더 없이 부르게 된다.
- **fix3 가 만든 문제가 아니다** — 정정 전에도 키는 Phase 1 에서 필수였다. Rollback `:679-681` 이
  "FE 가 키를 싣지 않는다면 BE 도 함께 되돌린다"로 둘이 같이 움직여야 함을 이미 적고 있다.
- RW-1 을 닫으며 세운 원칙(**여는 자리와 소비하는 자리를 같은 단위에 둔다**, `:371`·`:386-388`)을
  키 헤더에도 적용할지 한 줄로 적으면 닫힌다. **새 기술 대안을 제안하지 않는다** — 문서가
  이미 쓰고 있는 원칙을 한 자리에 더 적을지의 문제다. 착수를 막지 않는다.

## 확인한 것 / 못 확인한 것

- **allowed_paths** — 수정은 fix3 §5 두 경로 안. 리뷰 리포트 외 다른 파일을 나는 건드리지 않았다.
- **OQ-A · D2** — 이번에도 확정되지 않았다. 확인만 했고 판단하지 않았다.
- **테스트·빌드·DB·린트** — 돌리지 않았다(브리프 §4 금지 · reviewer `tools.md`).
  린트는 여전히 `scripts/lint-pipeline.py` 부재로 실행 불가(기존 부채).
- **못 확인한 것** — 1차와 같다(멱등 원장 저장 모양 · `accept` 열 구조 · 레포 밖 AX 런타임의
  실제 키 전달 · inventory JSON 의 drift 규모). 이번 정정과 무관하다.
