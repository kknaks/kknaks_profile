# [writer] WORK-004 — SPEC-004 를 실행 계획으로 내린다

너는 **strong-hajin `writer` 워커**다. 역할 문서는 앞 발주에서 읽었다 — 바뀐 것 없다.
(`/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/orchestration/roles/strong-hajin/planner/`)

작업 워크트리: `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin` ← **코디 워크트리 탑승**
base 브랜치: `origin/main` → 최종 PR 대상 `main`

> ⚠ **SPEC-004 는 검수를 통과했다.** 계약은 닫혔다 — **다시 열지 마라.**
> ⚠ 네가 앞서 쓴 SPEC-004 를 **이번 발주에서 고치지 마라.** 이번 산출물은 WORK 문서 하나다.
> ⚠ 커밋·push 금지.

## 1. SSOT

- `para/projects/summer-star/strong-hajin/20-spec/spec-004-calendar-scheduling.md` ← **계약.** 네가 썼다
- `para/projects/summer-star/strong-hajin/10-decision/decision-003-calendar.md` ← 채택 A~J · 증보 K1~K4 · 기각 · 보류
- `orchestration/work/strong-hajin-calendar/review-spec-004-report.md` ← **검수 리포트.** 여기 WARN 이 있으면 WP 가 그 자리를 어떻게 닫는지 적어라
- `orchestration/work/strong-hajin-calendar/be-survey-report.md` ← **실행 계획의 뼈대가 여기 있다.** 새 표를 세울 때 닿는 자리·D1 세 자리·상태 변경 아홉 경로·reset_demo·운영 대장
- `orchestration/work/strong-hajin-calendar/fe-survey-report.md` ← FE 지형·DS-gaps 8건·상호작용 명세

**형식의 본보기**: `para/projects/summer-star/strong-hajin/30-work/work-002-task-lifecycle-v2.md`
(절 구성 `Meta / Work Summary / Role Assignment / Scope / Code Surface / Domain / Schema /
Dependency / Internal Interface Contract / Execution / 검증 계획 / 인수조건 추적 /
Pre-deploy Check / Rollback / Done Criteria / Open Issues / Related`)
및 `30-work/README.md`.

## 2. 무엇을 쓰나

`para/projects/summer-star/strong-hajin/30-work/work-004-calendar-scheduling.md` 한 장.
**BE 워커와 FE 워커가 이 문서만 읽고 각자 구현에 들어갈 수 있어야 한다.**

## 2-1. 검수가 WP 로 넘긴 것 — **네 개를 WP 가 받아야 한다**

SPEC-004 는 **검수 4회 PASS** 다(지적 13 → 3 → 1 → 0). 리뷰어가 「WP 로 넘길 것」으로
정리한 목록이 `review-spec-004-report.md` 의 4차 절에 있다. **그것을 WP 가 닫는다.**

1. **WARN-A — 뒤집힌 업무에서 띠의 끝과 손잡이가 안 적혔다.** K14 가 그리기·드롭 가드를
   `span_from`/`span_to` 로 통일했는데, 날짜를 쓰는 상호작용 둘(R1 「길이를 유지」·R3
   「start 손잡이는 `min(끈 날, 마감)`」)은 여전히 **raw 필드 말**이다. 뒤집힌 업무에서는
   띠의 왼쪽 끝이 `due_date`, 오른쪽 끝이 `start_date` 가 되므로 **「어느 화면 끝이
   start 손잡이인가」와 「길이가 span 길이인가 raw 차이인가」가 미정**이다.
   FAIL 이 아닌 이유 — 서버는 한 값이고(어느 매핑이든 K11 한 규칙으로 닫힌다) 할 수 있는
   일도 같다. **FE Phase 에서 한 줄로 정하고 인수조건 한 줄을 달아라.**
2. **배정 삭제 없음의 구멍** (DEC-003 보류) — 월요일 배정만 빼고 기간은 유지하고 싶을 때
   길이 없다. **이번 판에 열지 않는다.** WP 는 그 사실을 `Open Issues` 에 적기만 한다.
3. **착수 전 조사 ①** — `_ds_bundle.css`/`_ds_bundle.js` 의 토큰 **값**이 저장소와 같은지.
   참조 이름만 맞췄고 값은 안 봤다. **FE Phase 착수 전 한 줄로 끝낸다.**
4. **착수 전 조사 ②** — 실행 PostgreSQL 의 **실제 제약**. ORM 선언과 같다고 전제하지 않는다.
   **BE Phase 의 검증에 넣는다.**

## 3. 이 WP 가 반드시 담아야 하는 것

### 3-1. `Domain / Schema` — SPEC 이 일부러 안 쓴 것이 여기 온다

`20-spec/README.md` § Data / Domain Boundary 가 column·index·FK·ORM 모델·repository 구조를
**WORK 로 보냈다.** `task_schedules` 의 실제 모양을 여기서 확정하라.

- DEC-003 §A 가 정한 것: `task_id` FK · `on_date`(Date) · `starts_at`/`ends_at`(Time) ·
  `released_at` · `released_reason` · 부분 unique `(task_id, on_date) WHERE released_at IS NULL`
- `released_by` 는 **두지 않는다**(§J)
- 30분 눈금은 **CHECK 로 박지 않는다**(§J)
- 선례 — `persistence.py:1015-1022`(`task_predecessors`) · `:1506-1515`(`task_references`) 의
  `released_at` + 부분 unique 를 **글자 그대로** 따른다

### 3-2. `Code Surface` — 손대는 자리를 **전부** 센다

`be-survey-report.md` §2 가 이미 세어 뒀다. 그것을 실행 목록으로 옮겨라. 최소:

- `platform/persistence.py` — 새 레코드 클래스
- **D1 세 자리** — `application.py:518-520`(`update`) · `:1443`(`transition`) · `:1679`(`_apply_proposal`)
- `entrypoints/http.py` — 새 라우트들, `GET /api/meetings` 의 `from`/`to`
- `docs/unified-operations-inventory.json` — **행 3 + `http_count` 156→159 · `tool_count` 불변**
  (`status: excluded` · `policy: E2` · `exclusion.reason` · `reconsider_when`)
- `Makefile:170` + `tests/architecture/test_local_stack_targets.py:28-40` — local-stack 표지에 표 추가
- `tests/architecture/test_test_pyramid.py` `PURE_DOMAIN_MODULES` — 새 순수 도메인 파일을 만들면 등재
- FE — `features/calendar/` 재작성, 새 부품들, `lib/api.ts`, `lib/viewModels.ts`

### 3-3. `Execution` — **BE 먼저, FE 나중. 직렬이다**

코디네이터가 이 순서로 발주한다. Phase 를 그 경계에 맞춰 끊어라.

```
Phase BE-1  스키마 + 배정 CRUD + 합본 조회
Phase BE-2  D1 세 자리 검증 + K3 released_count + 운영 대장
Phase FE-1  화면 골격 — 3분할 · 좌측 레일 · 월/주 뷰
Phase FE-2  상호작용 넷 — 드롭 · 손잡이 · 시간 배정 · 금지 문구
```

**Phase 마다 「무엇이 돌면 끝인가」를 적어라.** BE 가 닫히기 전에 FE 를 태우지 않는다.

### 3-4. DS-gaps 8건을 **우리가 만든다**

`fe-survey-report.md` §5 의 G-CAL-01~08. 디자이너가 없다(DEC-003 정정).
**무엇을 만들고 어디에 두는지**를 FE Phase 에 배치하라. `GutterList` 는 이름이 이미 쓰이고 있으니
**새 이름**을 준다(DEC-003 §J).

### 3-5. `검증 계획` — 무엇을 언제 돌리나

- `make test-unit` · `make test-contract` — 변경 단계에 맞게. **단계별 전량 반복 금지**
- `make frontend-test` + `cd frontend && npx tsc --noEmit`
- **`make test-postgres POSTGRES_TEST_URL=postgresql+psycopg://ax:ax@127.0.0.1:54329/ax_test_calendar`**
  ← 이번 작업 전용 DB 다. 부분 unique 가 **실제로 선다**를 여기서 증명한다(SPEC §6)
- 최종 `make verify`
- **백엔드 커밋이 들어가면 API 를 다시 띄운다** (config `rules.restart_api_after_backend_commit`)

### 3-6. FE 선행 검증 항목

`_ds_bundle.css`(4069줄)·`_ds_bundle.js`(1862줄)의 토큰 **값**이 저장소와 같은지 — 참조 이름만
맞췄고 값은 안 봤다(DEC-003). **결정이 아니라 확인 작업**이므로 FE Phase 착수 전 한 줄로 끝낸다.

### 3-7. `인수조건 추적` — 어느 Phase 가 SPEC 의 어느 줄을 닫나

SPEC §6 의 인수조건을 Phase 에 **전수 매핑**하라. 닫는 Phase 가 없는 인수조건이 있으면
그것이 이 WP 의 구멍이다.

## 4. allowed_paths

쓰기가 허용된 파일은 **둘뿐**이다.

- `para/projects/summer-star/strong-hajin/30-work/work-004-calendar-scheduling.md` ← **새로 만든다**
- `para/projects/summer-star/strong-hajin/30-work/README.md` ← 한 줄 추가

**건드리지 마라**: `20-spec/` · `10-decision/` · `00-baseline/` · `log.md` · `orchestration/` · 코드 레포

## 5. 범위 제약 — 하지 말 것

- **계약을 다시 정하지 마라.** SPEC-004 가 닫혔다. 모순을 발견하면 고치지 말고 `Open Issues` 에 적어라
- **코드를 쓰지 마라.** 계획이다. 예시 코드 조각은 계약을 설명할 때만, 짧게
- **시안을 기능 기준으로 쓰지 마라** — 레이아웃 정본일 뿐이다
- **코드 레포 워크트리를 열지 마라.** 조사 리포트 둘이 파일:줄로 이미 떠 왔다
- 커밋·push 금지

## 6. 검증

- `work-002` 와 **같은 절 구성·frontmatter**
- SPEC §6 인수조건이 **전부** Phase 에 매핑됐다. 빠진 것이 없다
- `Code Surface` 가 `be-survey-report.md` §2 가 센 자리를 **빠짐없이** 옮겼다 (운영 대장·local-stack
  표지·test_pyramid 등재 포함)
- DS-gaps 8건이 **전부** Phase 에 배치됐다
- Phase 마다 **완료 판정 기준**이 있다
- `git status --short` 에 **위 두 파일만** 뜬다(코디가 고친 `10-decision/` 제외).
  출력을 완료 보고에 붙여라

## 9. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** 아래 명령에 박힌 코디handle 은 **브리프 작성 시점** 값이라 오래됐을 수 있다 — 세션이 재연결되면 핸들이 바뀐다(2026-07-28·29 두 번 겪음). preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.** 두 곳에 다 보내지 말고 preamble 쪽으로만 보내라.


- **커밋·push·PR 하지 마라.** 워크트리에 변경만 남긴다. 검증·PR 은 코디네이터가 한다.
- 끝나면 **아래 두 명령을 모두** 실행한다. 하나만 하면 안 된다.

```bash
# (1) 인박스 적재 — 태스크 완료 처리·영구 기록. 코디네이터를 깨우지 않는다.
orca orchestration send \
  --to term_a9d49810-1ce8-4885-8c5f-b93200c501ac --from term_95d88d2b-e9e6-4e4a-a031-3b247f4d99b1 \
  --type worker_done \
  --task-id <이 태스크의 taskId — dispatch 로 받은 context 에 들어 있다> \
  --dispatch-id <이 태스크의 dispatchId — dispatch 로 받은 context 에 들어 있다> \
  --subject "writer 완료: <한 줄>" \
  --body "변경 파일 목록 / 구현 요약 / 검증 결과(수치) / 계약 준수 / 미결·주의점"

# (2) 직접 주입 — 코디네이터 세션에 유저 메시지로 꽂혀 자동으로 깨운다.
orca terminal send --terminal term_a9d49810-1ce8-4885-8c5f-b93200c501ac \
  --text "[worker_done] writer 완료 — <한 줄 요약>. 상세는 인박스." --enter
```

- 막히면 30분 이상 혼자 헤매지 말고 같은 (2) 방식으로 물어라:
  `orca terminal send --terminal term_a9d49810-1ce8-4885-8c5f-b93200c501ac --text "[질문] writer: <질문>" --enter`
  (`orca orchestration ask` 는 채널이 닫혀 답이 안 닿는 경우가 많다.)
