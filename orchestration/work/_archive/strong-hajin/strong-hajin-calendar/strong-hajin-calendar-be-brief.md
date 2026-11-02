# [backend] 캘린더 시간 배정 — 새 표 `task_schedules` 를 세울 때 걸리는 표면 전수조사 (read-only)

너는 **strong-hajin `backend` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/orchestration/roles/strong-hajin/backend/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)

작업 워크트리: `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-calendar`
base 브랜치: `origin/main` → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

> ⚠ **이번 발주는 조사다. 코드를 한 줄도 고치지 마라.** 산출물은 리포트 파일 하나뿐이다.
> ⚠ 같은 워크트리에 `frontend` 워커가 동시에 조사로 타 있다. 둘 다 read-only 라 충돌하지 않는다 — **그쪽도 파일을 안 고친다.** 네가 고치면 그 전제가 깨진다.

## 1. SSOT — 먼저 읽을 것

- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/reference/2026-09-10-sc-meeting/package 2/handoff/calendar/js/calendar.v1.jsx` ← **확정 시안.** 캘린더가 무엇을 하는지의 SoT
- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/reference/2026-09-10-sc-meeting/package 2/handoff/calendar/js/week.jsx` ← 주별 뷰. 시간 격자·드롭 규칙이 여기 있다
- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/reference/2026-09-10-sc-meeting/package 2/handoff/shared/js/work-data.js` ← 시안이 가정한 데이터 모양

**시안은 목데이터다. 저장 구조의 SoT 가 아니다** — 무엇을 보여주고 무엇을 할 수 있는지만 읽어라.

### 코디네이터가 이미 닫은 결정 (이대로 전제하고 조사하라 — 다시 정하지 마라)

```
D1  업무 기간이 바뀌면 그 업무의 시간 배정을 검증한다
D2  바뀐 기간 밖으로 나간 배정은 소프트 딜리트
D3  기간을 되돌려도 복구하지 않는다 — 사람이 새로 넣는다
D4  업무 상태값의 정본은 백엔드(`TaskState` 6종). 시안의 `status` 5종은 폐기
D5  배정은 업무에 완전히 종속. 업무가 `done`·`cancelled` 로 가면 배정도 같이 접는다
D6  저장은 `meetings`(그대로) + `task_schedules`(새 표). 범용 schedules 표는 만들지 않는다
D7  `task_schedules` 는 task_id FK · 날짜 · 시작시각 · 종료시각만 담는다.
    제목·담당자는 담지 않는다 — 조인으로 끌어온다
D8  같은 업무는 하루에 배정 한 칸 (시안 calendar.v1.jsx 의 addSlot 이 그렇게 동작한다).
    단 D3 때문에 소프트 딜리트된 행은 그 유일성에서 빠져야 한다
```

## 2. 배경 / 무엇을 조사하나

업무는 **날짜 단위**로 산다(`tasks.start_date` · `due_date`, 둘 다 `Date`). 시안은 여기에 **시간 단위**를 하나 더 얹는다 — 월~수짜리 업무에 「월요일 오전 10시, 화요일 오후 2시, 수요일 오전 9시」처럼 그 기간 **안에서** 시간을 배분하는 것이다. 업무 기간 밖(목·금)에는 배정할 수 없다.

지금 레포 90개 표 중 **예정된 시각**을 담는 것은 `meetings.starts_at`/`ends_at` 뿐이다. 나머지 `*_at` 은 전부 「무슨 일이 언제 일어났나」인 감사 기록이다. 그래서 새 표가 필요하다(D6).

**이번 발주는 그 표를 만드는 일이 아니다.** 만들려면 어디를 손대야 하는지, 그리고 D1·D5 를 거는 자리가 몇 군데인지를 **빠짐없이 세는 일**이다. 다음 판의 spec·WP 가 이 리포트를 재료로 쓴다.

## 3. 계약 (다른 워커와 합의됨)

해당 없음 — 조사 단계다. 계약은 이 리포트를 받아 spec 이 쓴다.

## 4. 조사 항목 — 여섯 가지. **목록이 아니라 전수조사다**

각 항목의 답은 **`파일:줄` 근거와 함께** 낸다. "대충 이 근처" 는 답이 아니다.
그리고 **「N개 있다」로 끝내지 마라** — 세는 방법(실제로 돌린 `grep`/`rg` 명령)을 리포트에 그대로 적어라. 다음 사람이 같은 수를 다시 셀 수 있어야 한다.

### 4-1. 새 표 하나를 추가할 때 손대는 자리 전부

`task_schedules` 를 세운다고 할 때, 이 레포에서 **반드시 함께 바뀌는 파일과 절차**를 전부 센다.
최소한 아래는 확인하고, **여기 없는 자리가 더 있으면 그게 이 조사의 핵심 성과다.**

- `backend/src/ax_workspace/platform/persistence.py` — 표 정의가 사는 곳
- `backend/src/ax_workspace/bootstrap/schema_sync.py` — DDL 생성 경로
- `backend/migrations/` (그리고 `migrations/manual/`) — 마이그레이션을 쓰는 규약이 무엇인가
- `backend/tests/architecture/` — 경계 테스트가 새 표/새 모듈에 거는 규칙
- **operation inventory drift** — 이게 무엇이고 새 API 가 늘면 어디를 갱신해야 하나
- `reset_demo` 경로 — AGENTS.md 가 "스키마 변경은 reset_demo 전용 경로, 일반 API startup DDL 금지" 라고 한다. 그 경로가 정확히 어디고 무엇을 하는가

### 4-2. 업무 날짜가 바뀌는 경로 전부 (D1 을 걸 자리)

`tasks.start_date` 와 `tasks.due_date` 를 **쓰는 곳을 전부 grep** 한다. 읽는 곳 말고 **바꾸는 곳**이 몇 개인지가 핵심이다.

- 날짜를 바꾸는 명령·엔드포인트가 하나인가 여럿인가
- 여럿이면 D1 검증을 **한 자리에** 걸 수 있는 공통 지점이 있는가, 아니면 전부에 걸어야 하는가
- 업무 생성 시점에도 날짜가 들어오는가

### 4-3. 업무가 `done`·`cancelled` 로 가는 경로 전부 (D5 를 걸 자리)

`lifecycle.py` 의 `transition_task` 하나만 지나는가? **우회로가 있는지**를 확인하라 — 그 함수를 안 거치고 `tasks.state` 를 바꾸는 코드가 하나라도 있으면 D5 에 구멍이 난다. 배치·데모 시드·관리 스크립트까지 본다.

### 4-4. 소프트 딜리트 선례 (D2 가 따를 모양)

이 레포에 이미 있는 소프트 딜리트 패턴을 **전부** 찾는다 — `removed_at` · `archived_at` · `superseded_at` · `revoked_at` · `discarded_at` 등. 각각 어떤 뜻으로 쓰이고, 조회에서 어떻게 걸러지며, 부분 유니크 인덱스를 쓴 선례가 있는지( `uq_tasks_source_work_request` 가 하나다 ). **그중 무엇을 따르는 게 이 레포의 결대로인지** 근거와 함께 하나를 고른다.

### 4-5. 회의 목록 API 의 실제 계약

캘린더가 회의를 같이 그린다. `GET /api/meetings` 가 지금 내는 것을 **응답 필드 단위로** 적는다.

- 기간(from~to)으로 거를 수 있는가, 아니면 커서 페이징뿐인가
- 응답에 `starts_at`·`ends_at`·`location` 이 나오는가
- 권한 envelope 이 어떤 모양으로 실리는가 — 프론트가 무엇으로 「할 수 있나」를 판단하는가
- **캘린더가 쓰려면 모자란 것**이 무엇인가

### 4-6. 가시성 — 캘린더에 무엇이 보이나

내 업무·내 회의만 보이는가, 조직 단위로 보이는가. 그 판단이 어디서 나오는가(`organization_access` 모듈?). 캘린더가 새 조회를 만들 때 **반드시 통과해야 하는 가드**를 짚는다.

## 5. allowed_paths — 이 밖은 건드리지 마라

- **(read-only) 코드 레포의 어떤 파일도 수정·생성·삭제하지 않는다**
- 쓰기가 허용된 파일은 **아래 리포트 하나뿐**이다:
  `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/orchestration/work/strong-hajin-calendar/be-survey-report.md`

## 6. 진행 단계

1. 역할 문서 → 코드 레포 `AGENTS.md` → 시안 세 파일을 읽는다
2. 4-1 ~ 4-6 을 순서대로 조사한다. 각 항목마다 **실제로 돌린 검색 명령**을 기록한다
3. 리포트를 쓴다. 절마다 「사실(근거) / 해석 / 모르는 것」을 가른다
4. **정하지 못한 것은 Open Questions 로 남긴다.** 임의로 결정하지 마라

## 7. 범위 제약 — 하지 말 것

- **코드를 고치지 마라.** 표도, 마이그레이션도, 엔드포인트도 만들지 않는다
- **설계를 정하지 마라.** "이렇게 하면 된다" 가 아니라 "이 자리가 이렇게 생겼다" 를 낸다.
  선택지가 갈리면 각각의 근거와 대가를 적고 Open Question 으로 남긴다
- D1~D8 을 다시 논의하지 마라. **모순을 발견하면 고치지 말고 리포트에 적어라** — 그게 제일 값진 결과다
- 프론트엔드(`frontend/`)는 보지 마라. 다른 워커가 맡았다
- 테스트를 돌리지 마라 — 고친 게 없으니 돌릴 이유가 없다

## 8. 검증

조사 발주라 테스트 실행이 없다. 대신 리포트가 아래를 만족해야 한다.

- 4-1 ~ 4-6 **여섯 항목이 모두** 답을 갖는다. 못 찾았으면 "못 찾았다 + 어떻게 찾아봤나" 를 적는다
- 모든 주장에 `파일:줄` 근거가 붙는다. 근거 없는 문장은 쓰지 않는다
- 「전부 세라」고 한 항목(4-1·4-2·4-3·4-4)은 **실제로 돌린 검색 명령**이 리포트에 있다
- `git -C /Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-calendar status --short` 가 **비어 있다** (아무것도 안 고쳤다는 증거). 이 명령의 출력을 리포트 끝에 붙여라

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_a9d49810-1ce8-4885-8c5f-b93200c501ac --from term_8d3cb041-0ed1-492c-ace7-2ea1fc902b77 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "backend 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_a9d49810-1ce8-4885-8c5f-b93200c501ac \
  --text "[worker_done] backend 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_a9d49810-1ce8-4885-8c5f-b93200c501ac --text "[질문] backend: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
