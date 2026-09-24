# BE 재수정 — 검수 WARN 다섯을 닫는다 (FAIL 0, 계약은 이미 맞다)

**읽을 것**: `orchestration/work/strong-hajin-projects/review-be-report.md`
**allowed_paths**: `backend/` 만. **`frontend/` 는 FE 워커가 동시에 작업 중이다 — 건드리지 마라.**
커밋·push 금지. 서버 기동 금지.

검수 판정은 **FAIL 0** 이다. 계약은 맞게 돈다. 아래는 **무르게 선 자리**를 굳히는 일이다.

## WARN-2 — 빈 단언을 진짜 단언으로 (**가장 중요**)

`test_after_the_move_no_descendant_keeps_a_predecessor_in_the_old_project`(`:503-521`)의
핵심 단언이 **공집합 비교라 항상 참**이다. 트리에 선행이 하나도 없어서 **아무것도 증명하지 않는다.**

**고칠 것**: 그 테스트가 **실제로 선행을 가진 자손**을 세우게 하라.
- 프로젝트 P 안에 조부모 → 부모 → **손자** 를 만들고, **손자에 같은 프로젝트의 선행**을 건다
- 조부모를 프로젝트 Q 로 옮기려 하면 **게이트에 걸려 거절**되는지 (`WORK_PROJECT_LOCKED_BY_PREDECESSORS`)
- 선행을 푼 뒤 옮기면 **손자까지 Q 로 따라오는지**
- 그리고 **옛 프로젝트에 남은 선행이 0건**인지를 **비지 않은 집합으로** 확인한다

「구조적으로 자명하다」면 **그 자명함이 깨지는 경로**를 테스트가 지켜야 한다.

## WARN-6 — `getattr(…, 'auto_project_join', False)` 를 없앤다

`assignments.py:366` · `requests.py:740` 두 자리가 **문자열 이름으로** 흔적을 읽는다.
**이름이 바뀌면 떼는 자리 넷이 조용히 전부 무동작**이 된다 — 오류도 안 난다.

**고칠 것**: 속성을 **직접 참조**하거나(레코드 타입이 그 칸을 갖는다), 한 자리에 모아
**모듈 수준 상수·헬퍼**로 읽어라. `getattr` 기본값 폴백을 남기지 마라.
테스트로 **그 칸이 없으면 실패하는** 것을 보여라.

## WARN-5 — 기준선 기록 파일을 실제로 만든다

WP 가 이름 지은 `flaky-baseline-projects.md` 가 **없다.** 수치는 `be-impl-report.md` §1·§2 에 있다.
**내일 사용자가 Phase 0 를 그 파일로 시작한다** — 그러니 만들어라:

`orchestration/work/strong-hajin-projects/flaky-baseline-projects.md`
- 회차 0(착수 전) ~ 최종 회차의 **passed/failed 수치**
- **회차마다 어느 파일의 어느 건이 넘어졌는지** (검수가 「2→1→1→1 로 바뀐다」를 관측했다)
- `test_material_worker_recovery.py` 만 **직렬로 돌리면 5 passed·exit 0** 이라는 증명
- **이번 판이 만든 실패는 0건**이라는 결론과 그 근거
- ⚠ **`-p no:randomly` 는 쓰지 않았다**(미설치라 무동작) — 직렬화는 `-n0` 였음을 명시.
  reference 문서가 그 플래그로 직렬 증명을 했다고 적지만 **그 전제는 다시 재야 한다**

## WARN-7 — 떼는 자리 #4 테스트가 표면을 지나게

지금 application 메서드를 직접 부른다. **`cancel_assignment` 표면을 지나** 같은 결과가 나오는지
확인하는 테스트로 바꿔라 — 세 입구가 같은 메서드로 모이는 것이 이 판의 전제다.

## WARN-8 — 두 가지 정리

- `project_results.py:49-52` 의 **상태 주석이 `title` 위에** 붙어 있다. 맞는 필드 위로 옮겨라
- **`TaskPredecessorSource` alias 참조 0건** — 안 쓰면 지워라

## 검증

- `make test-contract` · `make test-unit` · 직렬 `-n0` · `make test-postgres` 를 **다시 돌려라**
  (**`-p no:randomly` 금지** — 미설치라 무동작)
- **기존 실패(`test_material_worker_recovery.py`)와 분리 보고.** 새 실패 0건이어야 한다
- WARN 다섯 각각이 **어떻게 닫혔는지** 한 줄씩
