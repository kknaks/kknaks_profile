# 검수 리포트 — WORK-007 Phase B-1 · B-2 · B-3 백엔드 (2026-09-28)

검수자: `@sc-ax-reviewer` (read-only). **코드를 한 줄도 고치지 않았다** — 산출물은 이 파일 하나다.

- 워크트리: `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-design` (브랜치 `kknaksss/strong-hajin-design`)
- base: `origin/main` = `b145745`. **`HEAD == origin/main`** — 커밋·push 0건이다(`git rev-parse` 두 값이 같다)
- 기준: SPEC-007 v0.2.0 · WORK-007 Phase B-1(`:236`) · B-2(`:273`) · B-3(`:312`) · DEC-006
- 대조 대상: `be-report.md` (워커 자기보고) — **믿지 않고 diff 로 확인했다**

---

## 0. 판정 (FAIL 0 · WARN 10)

**PASS.** SPEC-007 §3 열두 항목이 **전부 충족**이고, 계약과 다르게 도는 코드를 찾지 못했다.

WARN 열은 (ㄱ) 워커가 자진 신고한 판단 자리 셋, (ㄴ) 검수에서 새로 찾은 상속 부채 둘,
(ㄷ) 검증 수치 불일치 하나, (ㄹ) 테스트 구멍 셋, (ㅁ) 코디가 손을 대야 도는 것 하나다.
**어느 것도 재발주 사유가 아니다** — 전부 코디 판정 또는 후속 작업의 자리다.

---

## 1. 계약 대조표 — 브리프 §3 열두 항목

| # | 항목 | 판정 | 근거 (파일:줄) |
|---|---|---|---|
| 1 | **후행을 저장하지 않는다** — 새 표·새 쓰기 경로·양방향 저장 | **충족** | `platform/persistence.py` diff 는 **`Index(...)` 한 줄**뿐이다(`:1034`). 새 `Base` 표 0건·새 컬럼 0건(`tests/integration/postgres/test_work007_successor_index_postgres.py:64-83` 이 metadata 로 센다). 쓰기는 `release_predecessor_link`(`work_tasks.py:1205`) 하나이고 그것은 SPEC 이 «명령» 한 `released_at` 닫기다 — `replace_predecessors` 와 **같은 두 열**을 쓴다. 역방향 행을 세우지 않는 것을 `test_task_successors.py:88-93` 이 DB 로 센다(행 1개) |
| 2 | **역방향 조회** — `predecessor_task_id` 로 읽나 · 인덱스가 붙었나 | **충족** | `work_tasks.py:1155-1182` `successors_for()` 가 `TaskPredecessorRecord.predecessor_task_id.in_(...)` 로 건다 — `origin/main` 전체에 이 열을 **필터로** 거는 문이 0건이었다. 인덱스는 모델 metadata(`persistence.py:1034`) + 손 적용 `.sql` 쌍(`backend/migrations/manual/2026-09-28-w7-successor-index{,.concurrent}.sql`). **W2 선례(`2026-09-17-w2-indexes.sql`)와 같은 모양**이다. → 실제 DB 적용은 **W-9** |
| 3 | **응답 필드** — `successors` + `hidden_successor_count` | **충족** | `task_results.py:212-228`(`TaskSuccessorView` = `TaskSummaryView` + `version`) · `:261`·`:264`(둘 다 **필수 칸**). 운영 대장의 `task_get.output_schema` 가 그 여섯 칸(`task_id·title·state·due_date·assignee·version`)을 required 로 싣는다. 상세 두 갈래에만 실린다(`application.py:1131`·`:2650`) — `_with_checklist` 의 호출자는 `get()` 하나뿐이다(`application.py:1081`) |
| 4 | **못 읽는 후행은 건수만** — 제목·담당자·기한 누출 · **권한 필터가 실제로 도는가** | **충족** | `application.py:1468-1506` `successor_views()` — 후행마다 `_may_read_predecessor()`(= `may_read_task()`, `:1626-1641`) 를 묻고 못 읽으면 **`continue` 하고 `hidden += 1`**. `task_id` 도 만들지 않는다. **필터가 이름만 있는 것이 아니다**: `test_task_successors.py:167-178` 이 읽는 쪽을 프로젝트에서 빼서 갈래를 실제로 만들고 `assert "지호만 아는 후행" not in str(view)` 로 **응답 전체 문자열**을 센다 |
| 5 | **못 읽는 선행도 건수만이고 미완으로 센다** | **충족(무변경)** | 이 판이 손대지 않았다. `predecessor_views()`(`:1410-1433`) 는 여전히 **자리를 남기고**(`task_id` 는 내고 `title: null`), `_predecessor_gate()`(`:1371-1386`) 는 **선행 전부로 막을지 정하고 이름은 읽을 수 있는 것만** 낸다. 선행=자리, 후행=건수의 반대 규칙(D-10)이 코드에서 실제로 갈려 있다 |
| 6 | **읽기 전용 갈래에도 후행이 실린다** | **충족** | `application.py:1131`(`_related_view` → `access: "read_only"`) 와 `:2650`(`_with_checklist` → `owner`) 이 **같은 `_successor_fields()` 를 부른다** — 갈래별 분기가 없다. `test_task_successors.py:180-195` 가 `access == "read_only"` 에 두 칸이 있고 `references` 는 여전히 없음(SPEC §2.7 그대로)을 함께 센다 |
| 7 | **상위 변경** — `parent_task_id` + `clear_parent` · 검증이 기존 `parent_for()` **재사용**인가 | **충족** | `task_commands.py:57`·`:65`(`TaskEditFields`) · `:138-139`(`TaskUpdateInput`) · `:92`(둘 함께 → 거절). `application.py:661-665` 가 **`parent_for()` 를 그대로 부른다** — `git diff` 에 `parent_for` 본문 변경이 **0줄**이고 `_require_may_hold_children`·`_is_central_task` 도 무변경이다. 순서 차이는 **W-3** |
| 8 | **V-8 파급 거절** — 직속만 · `WORK_CHILDREN_DIRECT_NESTING`(409) 가 기존 코드와 **안 합쳐졌나** | **충족** | `errors.py:47-71` **별도 클래스**(`blocking` 튜플 포함) · `http.py:550` 이 409 튜플에 별도 항목으로 올린다. 판정은 `application.py:691-747`, `self.repository.children_of(task.id)` **하나**만 부른다 — `descendants_of` 를 부르지 않는 것을 `tests/unit/test_task_children_nesting_gate.py:145-156` 이 스텁 저장소로 센다(`descendants_of` 속성이 **없는** 저장소로도 돈다). 문장이 갈리는 것도 계약 층에서 센다: `test_task_parent_change.py:266`(`assert "직접 작업은 중심 업무의 바로 아래에만" not in detail`) |
| 8b | 그 게이트가 **못 읽는 하위까지 세나** | **충족** | `application.py:736-747` — `blocking` 은 `children_of` 전부에서 담당자로만 거르고, `shown` 만 이름을 낸다. `children_of`(`work_tasks.py:475-482`)는 권한을 묻지 않는다. `tests/unit/test_task_children_nesting_gate.py:64-96` 이 읽기 판정을 거짓으로 돌려 **이름이 사라지고 건수만 남고 그래도 막는 것** + `blocking == ()` 을 센다 |
| 9 | **상위 이동 시 자손 전체 프로젝트 파급** | **충족** | `application.py:668-688` — `descendants_of(task.id)`(깊이 무제한) 를 돌고, **게이트를 전부 먼저 건 뒤에** 값을 옮긴다. `clear_parent` 면 `parent is None` 이라 그 블록에 들어가지 않는다 → 프로젝트 그대로. `test_task_parent_change.py:389-433`(손자·증손자 / 새 상위에 프로젝트 없으면 비움) · `:434-466`(자손 하나가 선행 → 이동 전체 409, **아무것도 안 움직임**). 게이트 6 이 7 보다 먼저 도는 것도 센다(`:305-331`) |
| 10 | **후행 해제는 전용 명령** — PATCH 배열 교체 아님 · A 담당자에게 열림 | **충족** | `http.py:1709-1732` `DELETE /api/tasks/{task_id}/successors/{successor_task_id}?expected_version=` · `application.py:1508-1570`. 권한은 `_may_edit_either()`(`:1572-1585`) — `repository.task(id, principal.id)`(= **소유 투영**, `work_tasks.py:1090-1096`)를 A·B 양쪽에 묻는다. `test_task_successors.py:255-310`(A 담당자가 B 를 **고칠 수 없는데도**(먼저 PATCH 404 를 세고) 해제 성공) · `:312-321`(B 담당자) · `:323-334`(둘 다 아니면 403) |
| 10b | 해제의 나머지 계약 | **충족** | 행을 **닫고 지우지 않는다**(`released_at`·`released_by` 를 DB 로 확인, `:300-306`) · **B 의 회차만** 오른다(`:290-295`) · 멱등 아님 → 404(`:337-353`) · 회차 어긋남 409(`:355-368`) · 제안 행 0건(`:306`) · 비공개 후행에는 입구 없음(`:404-424`) |
| 11 | **알림은 범위 밖** — 구현해 버렸나 | **충족** | `modules/work/application.py` 에 notifications import **0건**. 주석 자리만 둘: `:1524-1529`(후행 해제) · `:685-688`(상위 이동의 자손 프로젝트). `test_task_successors.py:428-452` 가 `SqlAlchemyNotificationRepository.emit` 을 monkeypatch 로 걸고 **호출 0건**을 센다 — 「모듈이 없어서 안 불렀다」를 막는 모양이다 |
| 12 | **선행=시작 / 하위=완료** — 두 축이 섞였나 · 오류 코드가 합쳐졌나 | **충족** | `_predecessor_gate`(시작) · `TaskChildrenUnfinished`(완료) · `TaskDirectNesting`(생성 관계) · `TaskChildrenDirectNesting`(이동 파급) 이 **네 자리 그대로 따로**다. `git diff` 에 `_predecessor_gate`·`TaskChildrenUnfinished` 변경 0줄 |

**범위 밖으로 넘긴 것(계약이 그렇게 정했다)**: `TaskVersion` snapshot·diff 에 `parent_task_id`·`project_id` 가 없는 구멍은 그대로다 —
`_DIFFABLE_FIELDS`(`application.py:2861`)가 `("title","description","state","block_reason","start_date","due_date")` 로 무변경이다.
**SPEC-007 §5 보존 ⚠ 가 「이 SPEC 이 그 구멍을 닫지 않는다」로 적었고 WORK-007 Out 에도 있다** → 위반이 아니다.

---

## 2. FAIL

**없다.**

`git diff origin/main` 전수와 새 파일 6개를 읽고, 계약 열두 항목 각각에 대해
「코드가 실제로 그렇게 도는가」를 코드 + 테스트 단언 양쪽으로 확인했다.
계약과 다르게 도는 것을 찾지 못했다.

---

## 3. WARN

### W-1 — `make test-unit` 수치가 워커 보고와 다르다 (둘 다 green)

- 워커 보고(`be-report.md` §4): **381 passed, 1 deselected** — 괄호로 「(새 unit 파일 8건이 **더해진** 수)」
- **내 실측**: `make test-unit` → **389 passed, 1 deselected, exit 0** (12.48s)
- 차이 **8 = 새 파일 `tests/unit/test_task_children_nesting_gate.py` 의 8건**이다.
  즉 워커가 잰 381 은 **그 파일을 만들기 «전»** 의 수이고, 리포트의 괄호 설명이 사실과 어긋난다(381 + 8 = 389).
- **결론이 뒤집히지 않는다** — 양쪽 다 0 failed 다. 수치만 정정한다.

### W-2 — `docs/unified-operations-inventory.json` 이 BE 브리프 §5 allowed_paths 밖이다

- BE 브리프 §5 는 `backend/` · `Makefile` · `docker-compose.yml` · 리포트만 적었다(`strong-hajin-design-be-brief.md:72-78`).
- 그런데 **WORK-007 Phase B-1 작업 목록**이 「운영 대장의 그 행 서명을 갱신한다 — **실패 diff 의 그 항목만 패치**」를 명시하고,
  저장소 `AGENTS.md` 도 같은 말을 한다. **갱신하지 않으면 `tests/architecture/test_operation_inventory.py` 가 깨진다** — 즉 안 고치는 선택지가 없었다.
- **diff 는 정확히 그 둘이다**: `task_get.output_schema`(`TaskSuccessorView` + 두 칸 + required 셋) 와 새 HTTP 행 하나.
  `tool_count: 129` **불변**, `http_count: 159 → 160`. 전체 재작성이 아니다.
- 워커가 자진 신고했다(`be-report.md` §7⑥).
- **역할 `rules.md` #4 를 문자 그대로 읽으면 「allowed_paths 이탈 = 무조건 FAIL」이지만**, 여기서는 브리프 §5 의 **누락**으로 본다 —
  더 위 SoT(WORK-007 · AGENTS.md)가 그 변경을 명령했고 결과도 명령대로다. **코디가 판정할 자리다.**
- 그 밖의 diff 파일은 전부 `backend/` 안이다(`bootstrap/application.py` 의 조립 배선 · `migrations/manual/` 의 `.sql` 둘 포함).

### W-3 — `parent_for()` 안의 실제 검증 순서가 SPEC 표와 다르다

- SPEC-007 §4 표: **1(읽기) → 2(끝난 업무) → 3(담당 미확정) → 4(순환) → 5(V-8)**
- 실제(`application.py:412-427`, **무변경**): **1 → 4 → 2 → 3 → 5** (순환이 「끝난 업무·담당 미확정」보다 먼저)
- **거절의 집합은 같고**, 한 요청에 여럿 걸렸을 때 먼저 말하는 것만 다르다.
- WORK-007 Phase B-2 가 「1~5 는 기존 `parent_for()` 를 **그대로** 쓴다」이므로 **포크하지 않은 것이 옳다** —
  포크하면 V-8 판정이 두 벌이 되고 그것이 이 판이 피하려던 어긋남이다.
- 워커가 자진 신고했다(§7①). **권고: SPEC 표를 실제 순서로 고친다**(문서 소유자 몫).

### W-4 — 회차 어긋남의 상태 코드가 제품 안에서 둘이다 (422 / 409)

- 기존 업무 편집: `InvalidTaskTransition("task version is stale")` → **422** (`application.py:533`)
- 후행 해제: 새 예외 `TaskSuccessorVersionConflict`(`errors.py:191`) → **409** (`http.py:572`)
- **SPEC-007 § Case Matrix 가 이 표면의 `WORK_VERSION_STALE` 을 409 로 고정**했고, 기존 422 를 바꾸는 것은
  이 판이 허가받지 않은 계약 변경이다. 선례도 있다 — `TaskScheduleVersionConflict` 가 같은 모양으로 409 에 따로 서 있다.
- **계약 위반이 아니다.** 다만 「같은 제품에 회차 어긋남 상태가 둘」이 남았다. 워커 자진 신고(§7③). **정리하려면 별도 판정이 필요하다.**

### W-5 — 게이트 7 의 거절 문장이 **막는 «자손» 의 제목**을 낸다 (게이트 6 과 규율이 다르다)

- `_require_project_unlocked()`(`application.py:609-616`) 의 문장: `f"선행업무를 먼저 비워야 프로젝트를 바꿀 수 있습니다: {task.title}"`.
  `_apply_parent_change` 가 이것을 **자손 전체에 대해** 부른다(`:680-681`) — 그 자손을 **부르는 사람이 못 읽어도** 제목이 본문에 실린다.
- **같은 판이 만든 게이트 6 은 같은 자리에서 가린다**(`:740-747`: 읽을 수 있는 것만 이름, 나머지는 건수).
  **두 게이트의 규율이 갈렸다.**
- 다만 이 함수와 문장은 **기존 프로젝트 변경 경로의 것 그대로**이고(`:601-609` 의 기존 블록이 같은 함수를 자손에 돌린다),
  WORK-007 Phase B-2 가 「**기존 코드를 재사용하고 새로 짓지 않는다**」로 명령했다.
- **그래서 위반이 아니라 상속 부채다.** 새로 생긴 것은 **도달 경로**다 — 전에는 「프로젝트를 직접 바꿀 때」만 이 문장이 나왔고, 이제 「상위를 옮길 때」도 나온다.
- 근거: SPEC-007 §4 6번의 「거절 본문은 막는 하위의 «이름»을 낸다. **읽을 수 없는 하위는 이름 없이 건수로**」 — 그 규율이 7번에는 적혀 있지 않다.

### W-6 — 프로젝트 자손 파급이 `project_for()` 의 **읽기 가드를 지나지 않는다**

- `application.py:674` 가 `self.project_for(principal, None, parent)` 를 부른다.
  `project_for`(`:379-392`) 는 **`parent is not None` 이면 그 자리에서 `parent.project_id` 를 돌려주고 끝난다** —
  아래의 「읽을 수 없는 프로젝트에 일을 밀어 넣을 수 없다」 가드(`:389-391`)를 **지나지 않는다**.
- 결과: 상위 P 를 **읽을 수는 있으나 P 의 프로젝트는 못 읽는** 사람이, 자기 업무와 **그 자손 전체**를 그 프로젝트로 밀어 넣을 수 있다.
- **이것은 생성 경로에서 상속된 것이다** — `project_for(…, parent)` 는 생성이 부르는 바로 그 문이고,
  SPEC-007 §4 「왜 따라가나」 이유 1 이 **그 문을 그대로 쓰라고** 명령했다(「생성과 이동이 다른 답을 내면 안 된다」).
- **그래서 위반이 아니다.** 새로 생긴 것은 역시 **도달 범위** — 전에는 새 업무 하나였고 이제 **이미 있는 서브트리 전체**다.
- 덧붙여: 자손의 `project_id` 는 회차 상승도 진행 기록도 없이 바뀐다(`:682-683`). **기존 프로젝트 변경 경로가 이미 그 모양**이다(`:609`).

### W-7 — MCP 도구는 닫혀 있고 **AX 확인 카드는 열렸다** — 새 비대칭 하나

- `entrypoints/mcp.py` **무변경**. `task_update`(`:2015-2034`) 는 `parent_task_id`·`clear_parent` 를 **받지 않는다**.
  상세 도구 `task_get` 은 `TaskDetailResult` 를 돌려주므로 두 칸을 자동으로 실어 나른다(`test_task_successors.py:245-266` 이 도구 이름에 `successor` 0건 + 두 칸을 함께 센다). **새 도구 0건** — 계약대로다.
- 그런데 `clear_parent` 를 `TaskEditFields` 에 둔 결과(`task_commands.py:57`·`:65`), `TaskUpdateCommand(TaskEditFields)` 의 JSON schema 에도 두 칸이 선다.
  **`platform/actions.py:1845-1875` 의 확인 카드 필드 빌더가 schema 를 «일반적으로» 순회**하므로 —
  - `parent_task_id` → `select` 목록(`assignee_id`·`member_id`·`referenced_task_id`·`resource_id`·`output_material_ids`·`project_id`)에 없어 **후보 목록 없는 텍스트 칸**
  - `clear_parent` → **boolean 칸**(`empty_policy` 는 non-nullable bool 이라 `forbid`)
- 즉 **「MCP 손 서명은 닫혀 있는데 위임(AX) 갈래는 열려 있다」.** 워커가 그 사실을 §5① · §7⑧ 로 적었다.
- SPEC-007 §5 가 「`parent_task_id` 를 MCP 쪽에도 여는지는 `30-work/` 가 정한다 **(제안)**」로 이 결정을 보냈으므로 **계약 위반은 아니다.**
  **코디가 「닫은 채로 둔다」를 승인할 자리**이고, 승인한다면 AX 카드의 두 칸 문구·후보 목록이 후속 몫이다.

### W-8 — 테스트 구멍 셋 (전부 경미)

1. **후행의 「섞인」 갈래가 계약 층에 없다** — 읽을 수 있는 후행 + 못 읽는 후행이 **함께** 있을 때
   `successors` 에 앞의 것만 서고 `hidden_successor_count == 1` 인 갈래. `test_task_successors.py` 의 `hidden_successor_count` 단언은 전부 `0` 또는 「전부 가려진 1」이다(`:78`·`:113`·`:175`·`:194`·`:293`·`:423`).
   **게이트 6 의 섞인 갈래는 `tests/unit/test_task_children_nesting_gate.py:98-112` 가 센다** — 후행 쪽만 비어 있다.
2. **「`successors`·`hidden_successor_count` 는 응답 전용」(SPEC § Validation)을 세는 테스트가 0건이다.**
   `TaskUpdateInput`·`TaskEditFields` 의 `extra='forbid'`(`task_commands.py:48`·`:126`)가 구조적으로 보장하지만 **아무도 못질하지 않았다** — 나중에 `extra` 가 풀리면 조용히 열린다.
3. **약한 단언 한 줄** — `test_task_successors.py:177` `assert hidden["task_id"] not in view["successors"]`.
   바로 위 `:174` 가 `view["successors"] == []` 를 확인했으므로 이 줄은 **항상 참**이다(문자열 vs dict 리스트라 애초에 원하는 비교도 아니다).
   실질 검사는 같은 자리 `:178` 의 `assert "지호만 아는 후행" not in str(view)` 하나가 한다 — **그 한 줄이 강해서 결론은 안전하다.**

### W-9 — 인덱스가 **지금 도는 demo DB 에는 아직 없다** (코디가 적용해야 한다)

- `bootstrap/schema_sync.py:27-31` 을 직접 읽어 확인했다: `CreateIndex` 를 내는 갈래는 **「표가 라이브에 없을 때」 하나**이고,
  기존 표는 `:32-43` 이 **컬럼만** 순회한다. → **`make sync-demo-schema` 로는 절대 생기지 않는다.** 워커 §3 의 주장이 사실이다.
- 그래서 사용자의 `ax_demo`(포트 54329)에는 `ix_task_predecessors_predecessor_task_id` 가 **없다**.
  기능은 정상이고 **역방향 조회가 seq scan** 일 뿐이다.
- **코디 몫**: `psql -1 -f backend/migrations/manual/2026-09-28-w7-successor-index.sql` (또는 `make reset-demo`).
  운영은 `.concurrent.sql` 을 **autocommit 으로 사람이** 돌린다.
- `schema_sync` 를 확장하지 않은 판단도 확인했다 — 그 한계를 **계약으로 고정한 테스트**가 이미 있다
  (`tests/integration/postgres/test_task_lifecycle_v2_schema_postgres.py:322` W2 판). 확장은 그 계약을 깨는 일이고 WORK-007 이 허가하지 않았다. **옳은 판단이다.**

### W-10 — 한 `PATCH` 에 `parent_task_id` + `project_id` 를 함께 보내면 422 다 (FE 가 알아야 한다)

- `application.py:545` 가 `_apply_parent_change` 를 **먼저** 돌리므로 그 뒤 `:546-548` 의
  「하위 업무의 프로젝트는 상위 업무를 따릅니다」가 뒤의 `project_id` 를 막는다.
- **순서 자체는 옳다** — 주석대로 `preceding_task_ids` 검사가 **이동 후의 프로젝트**를 봐야 하기 때문이고, `:578-585` 가 실제로 그 값을 읽는다.
- SPEC-007 §2.8.3 · OQ-704 가 「**칸마다 따로 저장한다**」이므로 FE 가 그 순서를 지키면 걸리지 않는다.
- `test_task_parent_change.py:535-552` 가 현행을 못질했다. 워커 자진 신고(§7⑤). **Phase F-3 에 전달할 계약이다.**

---

## 4. 「조용히 통과하는 자리」 — 브리프 §4 전수 (봤고 문제 없는 것도 적는다)

| 자리 | 봤나 | 결과 |
|---|---|---|
| **권한 필터가 이름만 있고 안 거르는가** — 못 읽는 후행의 제목이 응답 어딘가에 실리나 | 봤다 | **문제 없다.** `successor_views`(`:1482-1484`)가 `continue` 로 **행을 만들기 «전»** 에 끊는다 — 못 읽는 후행은 `repository.task_by_id()` 조차 불리지 않는다. 계약 테스트가 응답 **전체 문자열**로 제목 부재를 센다(`test_task_successors.py:178`). 게이트 6 도 같다: `blocking` 튜플에 hidden 이 안 들어간다(`application.py:741`, unit 테스트 `:81-82` 가 `blocking == ()` 을 센다) |
| **빈 단언 / 결과를 안 보는 테스트** | 봤다 | `assert True`·`pass`·bare `...` **0건**. 새 4파일 54건에 단언 191개. **약한 줄 하나만** 찾았다 → W-8③ |
| **폴백이 거절을 삼키나** — 예외를 잡아 빈 배열로 돌려 「막힘 없음」이 되나 | 봤다 | **`except Exception` 0건.** 새 테스트 파일에도 `try/except` 0건. `_may_edit_either`(`:1581-1585`)는 `(TaskNotFound, TaskAccessDenied)` **둘만** 잡고 둘 다 실패하면 **403 을 던진다** — 삼키지 않는다. `may_read_task`(`:1637-1641`)의 같은 모양은 기존 코드다. 하나 눈에 띈 것: `successor_views:1487-1488` 의 `if node is None: continue` 는 **hidden 을 올리지 않고** 조용히 빠진다 — `# pragma: no cover` 이고 **FK 가 그 갈래를 막는다**(`predecessor_views` 도 같은 자리에 같은 모양이 있다). 실질 위험 없음 |
| **개명** — 기존 필드를 이름만 바꿔 계약이 바뀐 것처럼 보이나 | 봤다 | **없다.** diff 에 응답 필드를 지우는 `-` 줄이 0건이다(운영 대장의 `-"predecessors"` → `+"predecessors",` 는 콤마 하나). 유일한 개명은 **private 빗장** `_resolving_predecessor_access` → `_resolving_relation_access`(`:250`) 이고 **선행·후행이 하나를 공유해야** 선행→후행→선행 사슬이 안 열리므로 **필요한 개명**이다 |
| **인덱스가 선언만 되고 실제 DB 에 안 붙나** | 봤다 | 붙는다 — 새 DB 는 `create_all`, 기존 DB 는 `.sql`. **다만 지금 도는 demo DB 에는 아직 없다** → W-9 |
| **`reset_demo` 전용 경로를 벗어난 스키마 변경 · 일반 API startup DDL** | 봤다 | **없다.** 스키마를 건드린 자리는 `persistence.py` 의 모델 선언 한 줄과 `migrations/manual/` 둘뿐이다. `bootstrap/application.py` diff 는 **import 한 줄 + `release_task_successor` 메서드 하나**이고 DDL 이 없다. `entrypoints/http.py` 의 startup 경로에 스키마 코드 0건 |
| **MCP↔HTTP 비대칭** | 봤다 | 새 도구 0건 ✓ · 상세 도구가 두 칸을 자동으로 실어 나름 ✓ · 새 라우트는 운영 대장에 `policy: E2 / status: excluded` 로 **의도적 제외**가 기록됨 ✓. **다만 위임(AX) 카드 쪽이 열렸다** → W-7 |
| **`TaskVersion` snapshot — 상위·프로젝트가 바뀌는데 이력이 못 남기나** | 봤다 | **못 남긴다.** `_DIFFABLE_FIELDS`(`:2861`) 무변경. 그래서 이 판이 연 두 쓰기(상위 이동 · 후행 해제)도 버전 이력에서 복원되지 않는다. **활동 로그에는 남는다** — 상위 이동은 `task.updated` 요약의 `parent_task_id`(`:604-607`), 후행 해제는 B 의 `task.predecessor_released`(`:1557-1562`). **SPEC-007 §5 보존 ⚠ 와 WORK-007 Out 이 이 구멍을 명시적으로 열어 두었다 → 위반 아님** |
| **계층 경계** (역할 `rules.md` backend 항목) | 봤다 | `modules/work/application.py` 에 `fastapi`·`mcp`·`sqlalchemy` import **0건** — 관계 행을 `Any` 로 받는다(`application.py:132`, `work_tasks.py:1187`). `tests/architecture` 가 green |

---

## 5. 범위 이탈 (브리프 §5)

| 물음 | 답 |
|---|---|
| `frontend/` 를 건드렸나 | **아니다.** `git status`·`git diff --stat` 에 `frontend/` **0건** |
| WORK-007 에 없는 단계를 했나 | **아니다.** diff 전수가 B-1(후행 조회·응답 칸·인덱스) · B-2(상위 칸·게이트 6·7) · B-3(해제 라우트) 안에 든다. F-* 는 손대지 않았다 |
| 커밋·push 했나 | **아니다.** `HEAD = origin/main = b1457455…` 로 두 값이 같다. 변경은 전부 워킹 트리에만 있다 |
| allowed_paths 밖 파일이 바뀌었나 | **하나** — `docs/unified-operations-inventory.json`. → **W-2**(브리프 §5 누락 vs WORK-007 명령의 충돌, 코디 판정) |
| 범위 제약(§6) — 알림 구현 / 소급 재배치 / 후행 저장 / 양방향 저장 · 새 표 | **전부 지켰다.** 알림 0건(§4 표) · 소급 재배치 0건(`test_task_parent_change.py:505-534` 가 `application.py` 를 **AST 로 파싱**해 `*.parent_task_id = ` 대입이 **한 곳**이고 그것이 옮겨지는 업무 자신임을 센다) · 새 표 0건 · 역방향 행 0건 |

---

## 6. 검증 재현 결과 — 워커 수치와 대조

**전부 이 워크트리에서 Makefile 타겟으로 직접 다시 돌렸다.** 사용자 포트·프로세스는 건드리지 않았다(`8001`·`5176`·`54329` 무접촉, 죽이거나 재시작한 것 0건).

| 명령 | 워커 보고 | **내 실측** | 일치 |
|---|---|---|---|
| `make test-unit` | 381 passed, 1 deselected | **389 passed, 1 deselected** (12.48s, exit 0) | ✗ → **W-1** (둘 다 0 failed) |
| `make test-contract` 병렬 패스 | 1117 passed, 0 failed (3:52) | **1117 passed** (4:32, 11 workers / 1117 items) | ✓ |
| `make test-contract` 직렬 패스 | 128 passed, 1130 deselected (4:50) | **128 passed, 1130 deselected** (5:02) | ✓ |
| `make test-contract` 전체 | exit 0 | **exit 0** | ✓ |

**내가 돌리지 «않은» 것 — 코디 몫**

| 무엇 | 왜 |
|---|---|
| `make test-postgres` | **격리 PostgreSQL 이 필요하다** — 브리프 §6 이 「돌리지 말고 코디 몫으로 적어라」. 워커는 `ax_test`(= `POSTGRES_TEST_URL` 기본값, 사용자 demo DB `ax_demo` 와 **다르다** — `Makefile:10` vs demo 설정) 에서 **2 passed** 를 보고했다: 인덱스가 `pg_index` 에서 valid·ready 라는 것과, 인덱스를 내린 뒤 `schema_sync` 로는 안 돌아오고 `.sql` 로만 선다는 것 |
| `make test` · `make verify` | 종합 검증은 코디 몫이다. ⚠ **`tests/integration/postgres/test_work007_successor_index_postgres.py` 의 «비 integration» 2건**(`:64` 모델 선언 · `:151` 두 `.sql` 정의 일치)은 `test-unit` 에도 `test-contract` 에도 안 들어간다 — **`make test`(= `verify` 의 첫 타겟)에서만 돈다**(pyproject `testpaths=["tests"]`). 그 둘이 세는 **사실 자체**는 내가 파일을 직접 읽어 확인했다: 인덱스가 metadata 에 있고 열이 `predecessor_task_id` 하나이며 unique 가 아니라는 것(`persistence.py:1034`), 두 `.sql` 이 `CONCURRENTLY` 한 낱말만 다르다는 것(두 파일 직접 대조) |
| 사용자 스택 재시작 · demo DB 인덱스 적용 | W-9 |

---

## 7. 검수 한계

1. **성능을 재지 않았다.** 후행 투영은 후행 하나마다 `may_read_task()` → `get()` 을 부르고 그 `get()` 이 또 전체 상세를 만든다(`:1482` · `:1486`).
   빗장이 **깊이를 2 로 묶지만**(`_successor_fields:1461-1464` 가 안쪽에서 접는다) **폭은 후행 수만큼**이다 — N+1 이다.
   **선행 요약이 이미 그 모양**이고 SPEC 이 상세 하나로 자리를 한정한 이유가 그것이므로 **위반으로 세지 않았다.** 실측은 하지 않았다.
2. **동시성을 실제로 부딪혀 보지 않았다.** 「검사와 저장이 한 덩어리」·「먼저 닫은 쪽이 이긴다」는 코드 경로(`task_by_id(..., lock=True)` · `predecessor_link(..., lock=True)` · 조립층 한 session)와 단일 스레드 테스트로만 확인했다. **SQLite 테스트는 실제 행 잠금 경합을 만들지 않는다** — 진짜 확인은 PostgreSQL 이 필요하고 그것은 코디 몫이다.
3. **FE 쪽 소비를 보지 않았다.** `successors`·`hidden_successor_count` 가 **필수 칸**으로 `TaskDetailResult` 에 들어갔으므로, 기존 FE 가 상세 응답을 엄격히 파싱한다면 영향이 있을 수 있다. 이 검수는 `backend/` 범위다.
4. **`docs/unified-operations-inventory.json` 의 diff 를 «항목 단위» 로만 확인했다** — 두 항목(`task_get.output_schema` · 새 HTTP 행)이 맞고 `tool_count` 가 불변인 것까지 봤다. JSON 100줄의 스키마 문자열 한 글자씩은 대조하지 않았다. `test_operation_inventory.py` 4건이 green 인 것으로 갈음했다.
5. **`be-survey-report.md`(착수 전 코드 상태)를 전수로 읽지 않았다.** 워커가 인용한 관측(「`predecessor_task_id` 를 필터로 거는 문 0건」 등)은 **`origin/main` 에 직접 `git show`·`grep` 을 걸어** 다시 확인했고, 그 방식으로 확인한 것만 근거로 썼다.
6. **W-5 · W-6 은 「상속 부채」로 분류했다** — 둘 다 이 판의 코드가 만든 것이 아니라 **SPEC 과 WORK 가 「재사용하라」고 명령한 기존 함수**의 성질이다. 「재사용이 옳았나」까지는 판정하지 않았다. 새로 생긴 것은 도달 경로/범위뿐이고 그 사실만 적었다.
