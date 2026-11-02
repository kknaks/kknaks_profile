# [backend] Phase BE-1 — `task_schedules` · 배정 CRUD · 합본 조회

너는 **strong-hajin `backend` 워커**다. 먼저 역할 문서를 읽어라 (이 워크트리엔 없다 — 절대경로):

- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/orchestration/roles/strong-hajin/backend/role.md` (+ 같은 폴더 `rules.md` · `skills.md` · `tools.md` · `workflow.md`)
- 그 다음 코드 레포 루트의 `AGENTS.md`

작업 워크트리: `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-calendar`
base 브랜치: `origin/main` (= `1b40f83`) → 최종 PR 대상 `main` (PR 은 코디네이터가 올린다)

> ⚠ **이번엔 코드를 쓴다.** 앞 두 발주(조사)와 다르다.
> ⚠ **커밋·push 하지 마라.** 워크트리에 변경만 남긴다. 검증·커밋·PR 은 코디네이터 몫이다.
> ⚠ 이 워크트리에 **다른 워커는 없다.** BE-1 이 닫히기 전에 FE 를 태우지 않는다.

## 1. SSOT — 먼저 읽을 것. **전부 커밋돼 있다**

- `/Users/kknaks/orca/workspaces/kknaks_profile/strong_hajin/para/projects/summer-star/strong-hajin/30-work/work-004-calendar-scheduling.md` ← **네 작업 지시서.** `## Execution` 의 **Phase BE-1** 이 작업 9개와 완료 판정을 이미 적어 뒀다. **그대로 따라라.**
- `…/20-spec/spec-004-calendar-scheduling.md` (1544줄 v0.2.3) ← **계약.** 검수 4회 PASS. §4 Interface Contract · §5 Implementation Rules · §6 Verification
- `…/10-decision/decision-003-calendar.md` ← 채택 §A~§J · 증보 **K1~K14**. **왜 그렇게 정했는지**가 여기 있다
- `orchestration/work/strong-hajin-calendar/be-survey-report.md` (764줄) ← **네가 앞서 쓴 조사다.** 닿는 자리·D1 세 자리·상태 아홉 경로·reset_demo·운영 대장이 파일:줄로 있다

**WORK-004 의 `## Domain / Schema` 가 `task_schedules` 의 실제 모양을 확정했다.** 새로 설계하지 마라.

## 2. 이 Phase 의 범위

WORK-004 `Phase BE-1` 그대로다 — **작업 1~9 · 완료 판정 그대로.** 여기서 다시 쓰지 않는다.
한 줄로: **`task_schedules` 를 세우고 배정 생성·시각 변경·합본 조회 셋을 연다.**
「배정이라는 것이 존재한다」까지가 이 Phase 다.

**이 Phase 가 아닌 것** — D1 세 자리 검증 · `schedule_release` 응답 · 운영 대장 등록은 **BE-2** 다.
당겨서 하지 마라. FE 는 손대지 마라.

## 3. 계약에서 틀리기 쉬운 자리 — **검수가 네 판 돌며 닫은 것들이다**

여기를 틀리면 되돌리는 값이 크다. 각각 SPEC 의 해당 절을 열어 확인하라.

- **K10 · `POST` 는 생성 전용이다.** `expected_version` 을 **받지 않는다.** 그 날에 살아 있는 배정이
  이미 있으면 **`409`**. 시각 변경은 `PATCH` 가 하고 거기서 `expected_version` 은 **무조건 필수**다.
- **K12 · 영수증이 `409` 보다 먼저다.** 같은 멱등 키의 재전송은 **`200` 영수증**이다. `409` 는
  **다른 키**인데 그 날이 찬 경우에만. 순서를 바꾸면 드래그 연타가 깨진다.
- **K8 · `expected_version` 은 배정 자신의 회차다.** 업무 회차가 아니다. 업무 `version` 을 올리면
  다른 화면의 낙관적 잠금이 멋대로 깨진다.
- **K7·K11 · 기간을 읽는 법은 네 경우다.** 둘 다 있음 / **한쪽만 → 그 날 하루** /
  **뒤집힘(`start > due`) → `[min, max]` 로 정규화** / 둘 다 없음 → 기간 없음.
  뒤집힌 기간은 **실재한다** — `validate_schedule` 은 호출자 셋 중 `update` 에만 걸린다.
- **K14 · 합본 조회가 `span_from`·`span_to` 를 싣는다.** 그 값은 위 네 경우를 **서버가 적용한 결과**다.
  화면이 다시 계산하지 않게 하는 것이 목적이다.
- **K5 · 권한 판정은 「그 업무의 활성 담당 관계」다.** `task.self_manage` capability 봉투가 아니다 —
  그건 전역 비트라 남의 업무에도 통과한다.
- **K6 · 읽을 수 있으나 담당이 아니면 `403`.** 읽을 수 **없는** 업무만 `404` 로 숨긴다.
- **K13 · 합본 조회 업무 행에 `is_active_assignee` 를 싣지 않는다.** 축이 `my_work` 라 항상 참이다.
- **§C · `COMPLETION_SUBMITTED` 는 남긴다.** 미완으로 취급한다. 거르는 것은 `DONE`·`CANCELLED` 뿐.

## 4. 검수가 이 Phase 로 넘긴 것 — **둘. 반드시 받아라**

WP 검수 리포트(`review-work-004-report.md`)가 BE-1 브리프에 실으라고 한 것이다.

### 4-1. `meetings_visible_to` 를 무조건 고치지 마라 — **소비처가 셋이다**

WORK-004 Code Surface #10 이 「`meetings_visible_to` 에 시각 조건 추가(또는 호출부 필터)」로
**두 선택지**를 준다. 그런데 그 함수 소비처를 세면 **셋**이다:

```
application.py:180  my_meetings      ← MCP my_meeting_list
application.py:198  readable_rows    ← 자료 검색
application.py:218  board            ← 우리가 쓸 자리
```

같은 문서 Code Surface #9 가 **「`my_meetings` 는 건드리지 않는다」**고 못 박았다. 첫 선택지를
무조건 필터로 짜면 `my_meetings` 와 `readable_rows` 가 **같이 바뀐다.**

> **시각 조건은 선택적 인자(기본 없음)로 넣거나 `board()` 호출부에서 거른다.
> 그리고 `my_meetings`·`readable_rows` 의 결과가 안 바뀌는 것을 테스트로 남긴다.**

### 4-2. 완료 판정의 M 묶음은 `test-postgres` 만으로 안 닫힌다

WORK-004 인수조건 추적 M 행이 확인 방법을 `make test-postgres` 단독으로 적었는데, M 7줄 중
마지막(**API startup 경로에 스키마 생성이 끼지 않는다**)은 **`make test-unit`** 이 닫는다
(`test_architecture.py` 의 `test_application_startup_never_mutates_schema`).
완료 판정이 `test-unit` 을 이미 요구하므로 구멍은 아니다 — **둘 다 돌려라.**

## 5. allowed_paths — 이 밖은 건드리지 마라

- `backend/`
- `docker-compose.yml`
- `Makefile`

**문서 경로(`para/`·`orchestration/`)는 코디 소유다. 절대 건드리지 마라** — WORK 문서의
Phase Status 도 네가 갱신하지 않는다(보고로 대신한다). `frontend/` 도 이번 Phase 가 아니다.

## 6. 검증 — WORK-004 `Phase BE-1` 의 완료 판정 그대로

```
make test-unit
make test-contract
make test-postgres POSTGRES_TEST_URL=postgresql+psycopg://ax:ax@127.0.0.1:54329/ax_test_calendar
```

- `ax_test_calendar` 는 **이번 작업 전용 DB** 다(코디가 팠다). 포트 `54329` 는 앞 작업이 남긴
  컨테이너이고 healthy 다. **포트 `5432` 는 다른 프로젝트가 쓰고 있다 — 건드리지 마라.**
- **부분 unique 증명 넷**이 각각 한 건씩 남아야 한다 — ① 있고 valid ② 술어가 「닫히지 않은 행만」
  ③ 같은 (업무, 날)에 살아 있는 배정 둘을 넣으면 거절 ④ 닫힌 날에 재배정이 선다.
  **「선언했다」를 근거로 쓰지 마라.** 살아 있는 PostgreSQL 에 묻는다.
- 단계별 전량 반복 금지. 변경 단계에 맞게 돌린다.
- **기존에 이미 깨져 있던 무관한 실패는 「무관」으로 분리해 보고한다.** 기준선을 먼저 재라.
- `tests/architecture` 경계와 operation inventory drift 를 확인하되, **운영 대장 등록 자체는 BE-2** 다.
  BE-1 이 라우트를 열면 `test_operation_inventory` 가 깨질 수 있다 — **그러면 그 사실을 보고하고
  BE-2 에서 닫는 것으로 남겨라.** 지금 대장을 고치지 마라.

## 7. 범위 제약 — 하지 말 것

- **계약을 다시 정하지 마라.** SPEC-004 는 검수 4회 PASS 로 닫혔다. 모순을 발견하면 **고치지 말고
  코디에게 물어라** — 코디가 정하고 DEC-003 에 증보로 남긴다. **조용히 정하지 마라**
- **BE-2·FE 를 당겨 하지 마라**
- **상태 변경 아홉 경로에 아무것도 더하지 마라** — 이번 판은 읽기 필터다 (DEC-003 §B)
- **`_is_past`·`my_meetings` 를 건드리지 마라** (§4-1)
- 스키마 변경은 `reset_demo` 전용 경로. **일반 API startup DDL 금지**
- 커밋·push·PR 금지

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
