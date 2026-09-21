
# 재개 노트 — strong-hajin-calendar (strong-hajin)

**지금**: **1루프 완료.** Phase 넷(BE-1·BE-2·FE-1·FE-2) 전부 구현·검수 PASS·커밋. 코드 워크트리 깨끗.
**다음**: E2E 통과했다. 남은 것 둘 — ① **2루프(시안 대조)** 할지 ② **PR** 올릴지. 그 뒤 `archive-work.sh`.

세팅: `scripts/new-work.sh strong-hajin strong-hajin-calendar` · 설정 SSOT `config/projects/strong-hajin.json`
코디handle: `term_a9d49810-1ce8-4885-8c5f-b93200c501ac`

## 워크트리

- `code`: `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-calendar` (branch `kknaksss/strong-hajin-calendar`, base `origin/main` → PR `main`)

## 1. 지금 — 밤사이 1루프 완료 (2026-09-21 03:30)

- [x] 조사 2건 · BASE-003 · DEC-003(증보 **K1~K18**)
- [x] SPEC-004 v0.2.4 — 검수 **4회** PASS (지적 13→3→1→0)
- [x] WORK-004 756줄 — 검수 PASS
- [x] **BE-1** `1c15d02` — `task_schedules` · 배정 CRUD · 합본 조회 — 검수 PASS
- [x] **BE-2** `2a85176` — D1 세 자리 · `schedule_release` · 운영 대장 · K16 — 검수 PASS
- [x] **FE-1** `c5b109d` — 3분할 · 레일 · 월/주 뷰 — 검수 PASS(K18 수정 후)
- [x] **FE-2** `aa8576b` — 상호작용 넷 · 금지 문구 · K17 — 검수 **PASS, 지적 0건**
- [x] **(사용자) E2E 통과** (2026-09-21) — 스택 `127.0.0.1:5176` / API `8001` / DB `ax_demo`(54329 기존 컨테이너 재사용, `COMPOSE_PROJECT_NAME=strong-hajin-work`). 사용자 확인: 「다 통과했어」
- [ ] **(사용자) 2루프** — 시안 대조 정정
- [ ] PR (문서/코드 분리) · `archive-work.sh`

### 최종 검증 수치 (코디 실물 확인)

```
backend   test-unit 356p/0f · test-contract 1117p/2f · test-postgres 89p/0f
frontend  69파일 914 passed / 0 failed · tsc exit 0
          test-scale 13p · test-release 1p · frontend-assets/build 통과
```

**`make verify` 는 한 명령으로 exit 2 다** — 막는 것은 `material_worker_recovery` 2건이고
**기존 flaky** 다(코디가 직렬로 돌려 5 passed 확인, 병렬 `-n auto` 에서만 난다).
FE-2 diff 는 `frontend/` 밖 0건이라 인과가 없다. 구성 타겟은 전부 따로 통과했다.

### 2루프에서 볼 것 (리뷰어가 모은 관찰 3건 — 지적 아님)

1. **세로 손잡이 끝이 23:30 까지만** 간다. `defaultSlot` 은 23:59 를 만들 수 있어
   하루 끝 배정의 끝을 손잡이로 되돌릴 수 없다. 눈금 규칙의 자연스러운 결과이고 계약 위반은 아니다
2. **입력 모델이 둘이다** — 카드→격자는 HTML5 DnD, 손잡이는 Pointer.
   터치·보조기술 경로는 자동 검증이 안 닿는다
3. **픽셀·간격·문구·시안 대조** — WP 가 처음부터 2루프로 보낸 항목

### 시안 띄우는 법

```bash
cd "reference/2026-09-10-sc-meeting/package 2" && python3 -m http.server 8000
```

## 2. 결정 (SoT)

| 날짜 | 결정 | 근거 |
|---|---|---|
| 2026-09-20 | **시안이 정본이다** — `reference/2026-09-10-sc-meeting/package 2/` 의 Calendar 화면 레이아웃으로 간다 | 사용자 지시 |
| 2026-09-20 | D1 업무 기간이 바뀌면 그 업무의 시간 배정을 검증한다 | 사용자 지시 |
| 2026-09-20 | D2 바뀐 기간 밖으로 나간 배정은 소프트 딜리트 | 사용자 지시 |
| 2026-09-20 | D3 기간을 되돌려도 복구하지 않는다 — 사람이 새로 넣는다 | 사용자 지시 |
| 2026-09-20 | D4 업무 상태값 정본은 백엔드 `TaskState` 6종. 시안 `status` 5종은 폐기. 시안에 없는 `completion_submitted` 는 미완으로 취급해 캘린더에 낸다 | 사용자 지시 — "상태값 정본은 우리 백엔드가 가지고 있는 거야. 디자이너가 상태값에 대한 이해가 없어서" |
| 2026-09-20 | D5 배정은 업무에 완전히 종속. `done`·`cancelled` 로 가면 배정도 같이 접는다 | 사용자 지시 — "스케쥴은 그렇게 중요한 게 아니야, 업무가 중요해서 종속된 개념" |
| 2026-09-20 | **시안은 「레이아웃 정본」이다. 기능·모달 항목·데이터·상태 어휘는 우리 것이 정본.** 디자이너가 없으므로 시안에 있고 우리에게 없는 부품은 우리가 만든다 | 사용자 정정 — "시안은 디자인 레이아웃만 보고 기능이 이런게 있다는거지 / 실제 기능 / 모달 항목 등은 우리가 가지고 잇는걸로" |
| 2026-09-20 | **구현은 2루프다.** 1루프는 계약 구현, 2루프는 사용자 E2E + 시안 대조 정정 | 사용자 지시 — "이게 다되면 시안이랑 우리 구현이랑 e2e 비교 하면서 두번 째 루프에서 정정하면 되잖아" |
| 2026-09-20 | **Q2 → D5 를 「읽기」로 건다.** 캘린더 조회가 `tasks.state` 를 조인해 거른다. D2(기간 밖)만 쓰기(소프트 딜리트) — 「되돌려도 복구 안 함」은 행에 흔적이 있어야 표현된다 | 사용자 결정 |
| 2026-09-20 | **Q1 → D5 의 「done」은 내부 `DONE` 만.** `COMPLETION_SUBMITTED` 는 미완으로 보고 배정을 살린다 | 사용자 결정 (D4 와 일관) |
| 2026-09-20 | **Q8 → 가시성은 「내 것만」** — 업무 `my_work` · 회의 `board` | 사용자 결정 |
| 2026-09-20 | BASE-003 · DEC-003 작성. 조사 OQ 24건 중 20건 닫고 4건 남김 | 코디 |
| 2026-09-20 | ⚠ **D5 의 구현 전제가 조사로 뒤집혔다** — 「`transition_task` 한 자리」가 아니다. 상태를 바꾸는 길이 아홉인데 lifecycle 을 지나는 건 하나뿐이고, `CANCELLED` 로 가는 길 다섯 · `DONE` 으로 가는 길 둘. 셋(`work_tasks.py:1855`·`:2658`·`:2715`)은 **영속 계층**이고 하나(`accept_delivery` `application.py:1296`)는 **요청 업무의 정상 완료 경로**다 | `be-survey-report.md` §4 + 코디 표본 검증 |
| 2026-09-20 | D6 저장은 `meetings`(그대로) + `task_schedules`(새 표). 범용 schedules 표는 만들지 않는다 | 코디 조사 — 90개 표 중 예정 시각을 담는 건 `meetings.starts_at/ends_at` 뿐. `meetings` 에 task_id 를 뚫으면 거기 FK 건 표 5개에 빈 가지가 생긴다 |
| 2026-09-20 | D7 `task_schedules` 는 task_id FK·날짜·시작·종료만. 제목·담당은 조인 | 시안 목데이터가 제목을 복사해 들고 있으나 그러면 업무 제목 변경 시 캘린더가 조용히 낡는다 |
| 2026-09-20 | D8 같은 업무는 하루 배정 한 칸. 단 소프트 딜리트 행은 유일성에서 빠진다(부분 유니크 인덱스) | 시안 `calendar.v1.jsx:221` addSlot 이 같은 taskId+day 를 덮어쓴다 / D3 와 충돌하지 않게 하려면 partial index. 선례 `uq_tasks_source_work_request` |
| 2026-09-20 | D9 회의가 캘린더로 돌아온다 (탭: 전체·회의·업무) | 시안. 현 `CalendarPage.tsx` 주석의 "이 화면은 업무만 낸다" 결정을 뒤집는다 |

뒤집힌 결정은 지우지 않는다. ~~취소선~~ 을 긋고 같은 행에 뒤집은 날짜와 사유를 남긴다 —
지우면 왜 그렇게 갔는지가 사라져서 같은 논의를 다시 한다.

## 3. 발주 (살아 있는 것만)

**진행 중인 발주 없음.** 워커 넷이 대기 중이고 **맥락이 전부 살아 있다** —
2루프 정정은 브리프를 새로 쓰지 않고 `orca terminal send --enter` 로 지시만 보내면 된다.

| 워커 | handle | 맥락 |
|---|---|---|
| frontend | `term_85cb39e1-727f-4765-9aa3-e320e5c979f6` | FE-1·FE-2 를 짰다 — **2루프 정정의 주력** |
| backend | `term_ee28966a-c2c7-4501-8817-a079517e8425` | BE-1·BE-2 |
| reviewer | `term_a881668d-7491-4cca-b8a2-7dbdc04d6372` | 검수 7판 전부 |
| writer | `term_95d88d2b-e9e6-4e4a-a031-3b247f4d99b1` | SPEC·WORK |

긴 지시는 **파일로 주고 메시지엔 포인터만** — 3126 bytes 메시지가 잘린 적이 있다.

핸들은 세션 재연결로 바뀐다. 바뀌면 **덮어쓴다.** 워커 보고는 dispatch preamble 의 값을 따르므로
여기 옛 핸들을 남겨 두면 어느 것이 산 것인지 판단이 안 된다.

## 4. 산출물

- spec PR: (아직)
- code PR: (아직)
- 문서: `para/projects/summer-star/strong-hajin/00-baseline/baseline-003-calendar.md` (235줄) · `10-decision/decision-003-calendar.md` (249줄) — **미커밋**
- SPEC 검수 리포트: `review-spec-004-report.md` (1219줄 — 1~4차 전부 보존). 4차 절에 **「WP 로 넘길 것」** 목록
- 리포트: `be-survey-report.md` (764줄) · `fe-survey-report.md` (727줄) — 둘 다 코드 변경 0건, Open Questions 각 12건
- 커밋: (아직)

## 5. 이력 (최신이 위)

- `2026-09-21` **BE-2 PASS · 커밋 `2a85176`** — 공유 TaskMutationResult 를 피한 워커 판단이 옳았다(읽기 투영 둘이 상속해서 MCP 도구 스키마까지 번질 뻔). K16(역량 문 두 겹)을 코디가 더하기로 정함. FE-1 발주
- `2026-09-21` **BE-1 PASS · 커밋 `1c15d02`** — 계약 열 자리 전부 코드로 확인. 선행 점검이 실제 drift 를 찾았다(실행 PG 부분 unique 여덟/모델 아홉, task_predecessors 표 없음)
- `2026-09-21` WORK-004 발주 (`task_d93f3bd55eef`) — 검수 이월 4건을 브리프에 실었다
- `2026-09-21` SPEC-004 **검수 4회 PASS** 후 커밋 `e749116`. 구멍 8건 중 셋(K5·K10·K14)이 「불변식을 화면에 맡긴」 같은 모양이었고, 둘(K7·K11)이 「되돌릴 수 없는 소멸」이었다. K11 은 **리뷰어 권장을 뒤집은 것** — 권장안의 대가가 D3 과 겹쳐 제품이 못 쓰게 된다
- `2026-09-20` SPEC-004 검수 발주 (`task_6ca55ece5504`)
- `2026-09-20` 코디가 SPEC 미결 4건을 K1~K4 로 결정 → DEC-003 증보 → writer 반영 (1116→1209줄)
- `2026-09-20` BASE-003·DEC-003 커밋(`e6af151`) 후 `writer` 발주 — SPEC-004
- `2026-09-20` 조사 2건 완료·검증. 코드 워크트리 `git status` 비어 있음 확인. 표본 검증으로 BE 의 「우회로 여덟」 주장 확인(`accept_delivery` 가 `task.state = TaskState.DONE` 직접 대입 · `close_request_task` 가 영속 계층에서 `CANCELLED`)
- `2026-09-20` 조사 2건 병렬 발주 (task_9f39aaed8cb9 · task_693a67e08a51)
- `2026-09-20` 코드 조사 브리프 2장 작성. writer 스켈레톤은 지웠다 — 스펙 단계에서 `new-work.sh … --workers writer` 로 다시 깐다
- `2026-09-20` 코디 브랜치를 `kknaksss/strong-hajin-calendar` 로 새로 땄다. 직전 `kknaksss/strong_hajin` 은 squash merge 되어 `origin/main` 6fc0687 에 들어가 있었다 (`git log` 로는 ahead 3 으로 보이지만 트리 차이 0)
- `2026-09-20` `new-work.sh strong-hajin strong-hajin-calendar --workers writer,backend,frontend` — 코드 워크트리 생성

이 절은 **재개에 필요한 만큼만** 쓴다. 회고·배운 것은 `SUMMARY.md` 몫이다.

## 6. 검증 환경 (밤샘 1루프용)

- postgres: `strong-hajin-work-postgres-1` (앞 작업이 남긴 컨테이너, 4일째 healthy, 포트 `54329`)
  — 새 워크트리의 compose 는 안 띄웠다. 이걸 재사용한다
- 이번 작업 test DB: **`ax_test_calendar`** (작업마다 하나 파는 관례 — `ax_test_w1`·`ax_test_v2_pg`·`ax_test_work003` 이 선례)
- `make test-postgres POSTGRES_TEST_URL=postgresql+psycopg://ax:ax@127.0.0.1:54329/ax_test_calendar`
  (`DATABASE_URL` 과 달라야 타겟이 통과한다 — `Makefile:53`)
- ⚠ 포트 `5432` 는 **task-management 프로젝트**가 쓰고 있다. 건드리지 않는다
