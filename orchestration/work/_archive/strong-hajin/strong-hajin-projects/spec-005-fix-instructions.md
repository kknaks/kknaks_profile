# SPEC-005 재수정 지시 — 검수 FAIL 4 · WARN 5 를 닫는다

**읽을 것**: `orchestration/work/strong-hajin-projects/review-spec-005-report.md` (검수 리포트 전문)
**고칠 것**: `para/projects/summer-star/strong-hajin/20-spec/spec-005-projects.md` **이 파일 하나뿐**

리포트의 지적을 그대로 따른다. **다만 FAIL-1 은 코디가 방향을 정했다 — 아래대로 고쳐라.**

## FAIL-1 — 상태 어휘 (코디 결정)

**스펙은 계약을 새로 만들지 않는다.** 「외부 5종」이라는 확정을 **지우고** 이렇게 쓴다:

- **외부 계약은 넷**이다 — `open` · `in_progress` · `done` · `cancelled`
  (`SPEC-003:204·888` · `application.py:2496` · `viewModels.ts:110`)
- **`blocked` 는 M-6 으로 「발행하지도 없애지도 않고 들어온 그대로 내보내는」 값**이다.
  계약이 아니라 **통과값**이다. 그 사실을 그대로 적는다
- **화면은 받은 값을 그린다** — `blocked` 가 오면 `labels.ts:20-26` 의 「막힘 / danger」로 렌더하고
  간트 바도 `--blocked` 규격을 쓴다. **이것은 렌더 사실이지 계약 확장이 아니다.** 그렇게 명시하라
- **D-06 은 「백엔드 `TaskState` 가 정본」만 정했다.** 그 이상을 D-06 근거로 달지 마라

## FAIL-2 — 오류 갈래

`_require_project_unlocked`(`application.py:579-586`)가 던지는 것은
**`TaskProjectLockedByPredecessors` = `WORK_PROJECT_LOCKED_BY_PREDECESSORS`(409, `errors.py:140`)** 다.
`PredecessorsUnfinished` 는 **`open→in_progress`/`done` 전이 게이트**라 다른 자리다. 표를 고치고,
기존 어휘 수를 **일곱**으로 바로잡아라.

## FAIL-3 — 떼는 자리 누락

**직접 배정·담당 교체 제안의 철회**가 빠졌다. `assignments.py:301` `cancel()` 이
`assignment_kind=direct` 를 철회하고, 그 kind 는 `assign`(`work_tasks.py:2461`)과
`reassign`(`:2569`) 둘 다 만든다. 표면은 `action_center.py:619-623` 의 `cancel_assignment`.
**떼는 자리 표에 넣고 개수를 다시 세어라.**

## FAIL-4 — 없는 근거를 단 세 자리

`:235`·`:520`(지연·기한 경과) · `:337`(체크리스트 읽기 전용) · `:206`(카드 재사용)에서
**DEC-004 가 정한 적 없는 것에 `(확정 — D-NN)`** 을 달았다. 결정 번호를 **떼고**,
실제 출처로 바꿔라 — 기한 경과는 `SPEC-001:200`, 카드 재사용·체크리스트는 BASE-004 의 관측이다.
**결정이 아닌 것을 결정으로 만들지 마라.**

## WARN 다섯 — 전부 닫는다

- **WARN-1**: OQ-601 을 **닫아라.** 라우트가 코드에 있다 — `POST /api/work-requests`(`http.py:1992`) ·
  `/withdraw` · 게이트 예외 이름(FAIL-2 의 그것). §7 에서 OQ-601 을 「닫힘 — 근거」로 바꾼다
- **WARN-2**: §5 Implementation Rules 에 **「거는 자리는 application 메서드이지 entrypoint 가 아니다」**
  한 줄을 넣어라. 같은 명령이 HTTP · MCP(`mcp.py:187·204·215`) · action-center 로도 들어온다.
  entrypoint 에 걸면 **조용히 빠지는 경로가 생긴다**
- **WARN-3**: `:878` 의 관측 불가한 인수조건을 **관측 가능한 문장**으로 다시 써라
- **WARN-4**: 깊이 정책을 SPEC-003 과 **화해시키는 한 줄** — 「SPEC-003 의 두 단계는 **업무 상세 화면**의
  규칙(F-1)이고, 프로젝트 화면은 `tasks_in()` 이 `WHERE project_id` 뿐이라 깊이와 무관하게
  전부 받는다(D-16)」
- **WARN-5**: 남아 있는 표 이름 하나(`task_schedules`)를 지워라 — 저장 구조는 WORK-005 몫이다

## 하지 말 것

- **새 계약·새 결정을 만들지 마라.** 필요하면 §7 Open Questions 로 올린다
- 이 파일 밖을 건드리지 마라. 색인·log 금지. **커밋·push 금지**
- 첨부(material)·Phase 0 는 이번 범위 밖이다

## 검증

- FAIL 4건 각각이 **어떻게 닫혔는지** 완료 보고에 한 줄씩
- WARN 5건도 전부 닫힘
- `git status --porcelain` 이 **스펙 파일 하나만** 바뀐 것을 보인다
