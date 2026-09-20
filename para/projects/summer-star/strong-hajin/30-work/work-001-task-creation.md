---
type: work
id: WORK-001
title: "W1 — 업무 생성과 타인 즉시 배정"
status: review
product: strong-hajin
work_type: new-feature
owner: kknaks
roles:
  pm: kknaks
  design: kknaks
  fe: kknaks
  be: kknaks
  qa: kknaks
  ops: kknaks
progress: 90
created_at: 2026-09-15
updated_at: 2026-09-16
tags:
  - product/strong-hajin
  - doc/work
  - status/review
links:
  baselines:
    - "[[baseline-001-work-page|BASE-001]]"
  decisions:
    - "[[decision-001-work-page|DEC-001]]"
  specs:
    - "[[spec-001-work-management|SPEC-001]]"
    - "[[spec-002-action-item-review|SPEC-002]]"
  works: []
  releases: []
  related: []
---

# W1 — 업무 생성과 타인 즉시 배정

한 번의 명시적 생성 명령으로 업무가 실재하게 만든다 — 본인 것이든 남에게 보낸 것이든,
명령이 성공하면 담당자가 정해진 업무가 그 사람의 목록에 **수락 없이** 즉시 선다.
**만들지 않는 것**: 완료·승인 상태 전환, 문의·회신 대기, 반복·수신함, 업무 페이지 축 개편.

> 1 파일 = 1 work = **빌드 계획**. SPEC 의 외부 계약 본문은 복제하지 않고 절 이름으로 가리킨다.
> **이 문서는 착수 전 초안이다.** 모든 phase 가 `TODO` 이고 코드는 한 줄도 쓰지 않았다.

## Meta

- Baseline: BASE-001
- Covers spec: SPEC-001 §2 U-6 · §3 S-1·S-2·S-3·S-9·S-10 · §4 API Contract(생성·배정·후보) ·
  §5 멱등성·권한·수락 명령의 존치 · §6 W1 인수조건 / SPEC-002 §2.2 종류 표 · §3 S-6·S-7
- Depends on work: 없음 — **이 work 가 첫 실행 단위다**
- Parallel work: 없음. W2 는 이 work 의 생성 경로 위에 선다
- Follow-up work: W2(완료·승인·기한 두 값·상태 메모·문의 1건 흐름) · 업무 페이지 축 개편 ·
  수신함 · 반복 · 다시 요청·지연 신호
- External dependency: 없음. 외부 API·credential 을 새로 붙이지 않는다

**착수를 막는 미결이 없다.** 재검수 리포트의 WP 독립성 판정대로 W1 이 필요로 하는 계약은
전부 확정이다 — 수신자 인자 · 허용 후보 권한 · 즉시 활성 담당 · 수락 gate 부재 ·
**신규 경로의 거절 명령 부재**(DEC-001 D-4, 원문 확정 제외) · 멱등 키(신규·필수) ·
활성 담당 유일성(신규) ·
승격 동일 경로. OQ-A · D2 · 위임전결 값은 **이 work 에 닿지 않는다**.

## 실행 현황 — 2026-09-16

사용자가 W1 전체 구현과 코디 자동 검증을 승인하고 **E2E는 직접 수행**하기로 했다. 아래 원래 실행 체크리스트의 E2E 수행 주체는 이 지시가 우선한다. 구현·자동 검증 결과는 `orchestration/work/strong-hajin-work/verification-and-e2e.md`에 기록했다. F1/W1~7 해소, 마지막 재검수2차 PASS, R1~4 해소 및 R1a 문구 정정 완료. 코드 미커밋, 미배포. 아래 체크리스트는 원래 계획을 보존하며 단계 상태와 완료 증거가 현재 결과를 나타낸다. E2E·배포 항목은 미수행이다.

## Work Summary

| Field | Value |
|---|---|
| Type | new-feature |
| Owner | kknaks |
| Status | review |
| Progress | 90% |
| Branch/PR | `kknaksss/strong-hajin-work` (기존 브랜치 계속 사용 — 새 워크트리·브랜치를 만들지 않는다) |
| Blocker | 없음 |
| Next | 사용자 E2E 확인 |

## Role Assignment

1인 작업이지만 책임은 역할별로 가른다. 한 사람이 두 역할을 겸할 때 **판정은 역할 기준으로** 한다.

| Role | Assignee | Responsibility | Status |
|---|---|---|---|
| PM | kknaks | 범위 경계 유지 — W2·문의·수신함을 끌어오지 않는다 | todo |
| Design | kknaks | 생성 창의 담당 필드와 문구(승인자는 W2). 기존 부품(`Tabs`·`Chip`·`Select`)만 쓴다 | todo |
| FE | kknaks | 생성 창 · 즉시 반영 · 수락 카드 제거 | todo |
| BE | kknaks | 도메인·영속·권한·멱등·표면 정렬 | todo |
| QA | kknaks | 인수조건 대조와 실패·재시도·권한 테스트 | todo |
| Ops | kknaks | 로컬 스택 검증. **배포는 이 work 에 없다** | todo |

## Scope

**포함**

- 본인 업무 생성 — 기존 경로 유지 + 입력 계약 확장
- **일반 구성원의 타인 생성** — 같은 명령에 수신자 인자. 관리자 배정 권한을 요구하지 않는다
- **관리자 직접 배정** — 기존 권한·조직 범위 검사를 그대로 유지한 채 **즉시 활성 담당**으로
- **회의 후속 승격** — 위 생성 명령·권한·멱등성을 그대로 쓴다. 우회 adapter 를 남기지 않는다
- **신규 수락 gate 제거** — 신규 생성이 수락용 판단 항목 · 수락 대기 배정 · 재상신 회차를
  만들지 않는다. **거절 명령도 신설하지 않는다**
- **멱등 키(생성 명령마다 필수) · 활성 담당 유일성 · 생성 원자성** (전부 신규 계약)
- 표면 한 slice — application · REST · MCP · AX · seed/fixture · 권한 · 도메인 · 영속 · FE
- 승인자 — **내부 저장 자리(nullable) 하나만 먼저 둔다.** W1 은 승인자를 **입력으로 받지 않고
  화면에도 내지 않는다.** 받아서 무시하는 API 를 만들지 않는다 (§ 최소 호환 경계)

**제외** (제품 차수 제외가 아니라 **다음 실행 단위**)

| 제외 | 어디로 |
|---|---|
| 완료 명령이 항상 `done` · 승인 대기 파생 · 보완 요청 · 승인 뒤 되돌리기 | W2 |
| **승인자의 입력 수용(API)과 화면 노출** — 저장 자리만 W1 | W2 — 완료 승인 경로와 **같은 단위로** 연다 |
| `completion_submitted` · `blocked` 제거 | W2 (상태 모델 전환) |
| 문의·결정 요청 발송 · 회신 대기 · 상태 메모 · 진행 기록 추가 API | W2 |
| 계획·실제 기한 두 값 | W2 |
| 업무 페이지 축 셋 · 축별 칩 · 행 액션 하나 · 상세 구획 재배치 | 업무 페이지 work |
| 수신함 · 반복 · 다시 요청 · 지연 신호 · 오늘/캘린더 | 각자의 slice |
| 기존 pending 요청/배정 **데이터**의 전환·호환 adapter | #7 D4 면제 — 하지 않는다 |
| 체크리스트·하위 업무·참고 업무·프로젝트 연결의 1차 UI 강제 | 하지 않는다. **기존 API·데이터는 보존** |

**이 work 가 끝나도 #7 은 완료가 아니다.** W1 한 slice 만 닫힌다.

## Code Surface

- Repo / module: `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-work`,
  branch `kknaksss/strong-hajin-work`, base `origin/main`, 기준 `8973791`
- 전수 목록의 원장은 **BASE-001 § 계약이 닿는 표면**이다. 아래는 **W1 에 닿는 후보**만 추린 것이고,
  착수할 때 같은 검색을 다시 돌려 표면을 다시 센다 — 목록 밖에서 실패가 난다.

| 경로 후보 | 역할 |
|---|---|
| `backend/src/ax_workspace/modules/work/task_creation.py` | 생성 입력 계약. `TaskCreateInput`·`TaskAssignmentInput`. **`extra='forbid'` 라 본문으로 받을 새 필드는 여기서 열어야 한다** — 수신자가 그 경우다. **멱등 키는 본문이 아니라 헤더로 오므로 여기에 열지 않는다** |
| `backend/src/ax_workspace/modules/work/task_values.py` | 공통 값 정규화(제목·일정) |
| `backend/src/ax_workspace/modules/work/application.py` | `create_self_task` 계열. `my_work` 가 활성 배정만 나열하는 규칙 |
| `backend/src/ax_workspace/modules/work/assignments.py` | 배정 application. docstring 이 수락 전제를 못 박고 있어 함께 바뀐다 |
| `backend/src/ax_workspace/modules/work/requests.py` · `request_lifecycle.py` · `request_commands.py` | 수평 요청 경로. 즉시 배정으로 갈리는 지점 |
| `backend/src/ax_workspace/modules/work/drafts.py` | AX 초안 정규화 필드 집합. 생성 필드가 늘면 같이 움직인다 |
| `backend/src/ax_workspace/platform/work_tasks.py` | 생성·배정·요청 수락의 영속. `causation_key` 재조회 자리 |
| `backend/src/ax_workspace/platform/persistence.py` | `tasks.origin_kind` · `task_assignments.assignment_kind`/`status` · 인덱스 |
| `backend/src/ax_workspace/platform/action_center.py` | 판단 항목 종류 등록. 수락 두 종류를 신규에서 끊는 자리 |
| `backend/src/ax_workspace/modules/actions/policy.py` · `confirmation.py` · `payloads.py` | 허용 명령 · AX 확인 대상 action type |
| `backend/src/ax_workspace/modules/meetings/followups.py` | 후속 승격. 생성 경로를 직접 호출한다 |
| `backend/src/ax_workspace/modules/organization_access/catalog.py` · `domain.py` | 역량 카탈로그·역할 template. **수평 요청 수신자 허용 판정** |
| `backend/src/ax_workspace/entrypoints/http.py` | REST. 생성·배정·요청·수락·거절·후보·승격 라우트 |
| `backend/src/ax_workspace/entrypoints/mcp.py` | MCP 명령→권한 표와 도구 |
| `backend/src/ax_workspace/bootstrap/application.py` | 위 application 조립 |
| `backend/src/ax_workspace/bootstrap/seed.py` · `scenario_csv.py` · `dataset_import.py` | seed·fixture. `scenario_requests`/`scenario_assignments` 의 `accept` 열 |
| `frontend/src/lib/api.ts` · `viewModels.ts` · `labels.ts` | FE 호출·타입·문구 |
| `frontend/src/features/work/WorkModals.tsx` | 생성 창(`CreateWorkModal`) |
| `frontend/src/features/work/MyWorkPage.tsx` | 목록 즉시 반영·수락 카드 자리 |
| `frontend/src/features/action/ActionCenter.tsx` · `shell/InboxRail.tsx` | 판단함 — 수락 종류가 사라진 뒤의 빈 상태 |

- Domain / schema note: **새 열이 생긴다**(멱등 원장, 수신자 지정 생성의 출처 구분, 승인자 저장 자리).
  활성 담당 유일성은 **DB 제약**으로 세운다. 실제 schema 의 SoT 는 **모델 metadata**
  (`backend/src/ax_workspace/platform/persistence.py`) 이고, 그것을 데이터베이스에 세우는 자리는
  `entrypoints/reset_demo` 하나다 — **이 레포에 migration 도구는 없다**(아래 § 스키마를 어디에 세우나).
  **기존 데이터 전환·backfill 은 하지 않는다**(#7 D4).

## Domain / Schema

| Entity | 역할 |
|---|---|
| Task | 업무 한 건. 생성 출처를 갖는다. 승인자는 **열만 있고 W1 에서 값이 들어오지 않는다** |
| TaskAssignment | 담당 관계. **활성은 업무당 0 또는 1** |
| 멱등 원장 | (**행위자 · 명령 종류 · 키**) → 만들어진 업무 + payload 지문. 같은 키 재전송은 같은 결과를 돌려주고 다른 payload 는 충돌이다. **같은 모양이 이미 레포에 있다** — `meeting_room_creation_attempts`(`persistence.py:337-350`: `UniqueConstraint("owner_id","request_key")` + `payload_fingerprint`) |
| WorkRequest | 수평 요청의 **출처 행**. 신규 경로도 이 행을 세우고 업무가 `source_work_request_id` 로 그것을 가리킨다. 출처 상태는 **`assigned`(즉시 배정됨)** 이고, 만들지 않는 것은 **판단 대기 상태와 판단 회차**다 |
| 판단 항목 | 완료 승인·AX 확인은 남고, 수락 두 종류는 신규에서 생성되지 않는다 |

**상태 / invariant**

1. 생성 명령이 성공하면 업무 하나 + 활성 담당 하나가 **같은 transaction** 안에 선다.
   둘 중 하나만 남는 중간 상태가 없다.
2. **한 업무의 활성 담당은 언제나 0 또는 1.** DB 제약(부분 unique 인덱스)으로 세우고
   application 검사로 낮추지 않는다. **세우고 검증하는 자리는 목표 스키마가 선 빈 격리 DB** 다 —
   이미 데이터가 있는 데이터베이스에 이 제약을 얹는 일은 이 work 밖이다(아래 § 스키마를 어디에 세우나).
3. **논리적 생성 명령마다 멱등 키가 필수다.** 키 없는 생성 명령은 거부된다.
4. 같은 (행위자 · 명령 종류 · 키) 의 두 번째 요청은 **새로 만들지 않고** 첫 결과를 돌려준다.
5. 같은 키에 **다른 payload** 가 오면 성공으로 위장하지 않는다 — 충돌로 거절한다.
   거꾸로 **서로 다른 키에 같은 내용**인 두 명령은 **둘 다 선다** — 내용이 같다는 이유로
   두 업무를 하나로 합치지 않는다.
6. 영수증을 돌려주기 전에 **지금도 그 사람이 그 업무를 읽을 수 있는지 다시 검사한다.**
   권한을 잃었으면 영수증 대신 **존재를 숨긴다** — 관계자 밖에는 존재도 알리지 않는다.
7. 신규 생성 경로는 수락용 판단 항목·수락 대기 배정·재상신 회차를 **생성하지 않는다.**
8. 회의 후보 하나는 업무 하나로만 승격된다. **키가 달라도** 같은 후보는 한 건이다.
9. 요청자·담당자·행위자·출처·시각과 그 회차의 근거는 **보존한다.** 수락 gate 제거가 이력을
   지우지 않는다. **수평 요청 출신 업무는 `source_work_request_id` 를 계속 갖는다** —
   기존 완료 승인이 이 값에서 나온다(§ 최소 호환 경계).

**스키마를 어디에 세우나 — migration 을 새로 들이지 않는다**

| 사실 | 근거 |
|---|---|
| migration 프레임워크가 **없다** | `backend/` 에 alembic·`migrations/` 가 없다. 스키마를 만드는 자리는 `bootstrap/reset.py:20` `Base.metadata.create_all(engine)` 하나뿐이고, `Makefile` 에도 migration 타겟이 없다(`reset-demo`·`sync-demo-schema`·`reset-catalog` 가 전부) |
| 스키마 변경은 `reset_demo` **하나가 소유**한다 | `tests/architecture/test_architecture.py:64-69` `test_application_startup_never_mutates_schema` 가 "schema mutation belongs exclusively to `ax_workspace.entrypoints.reset_demo`" 를 단언한다 |
| `sync-demo-schema` 는 **제약을 만들지 못한다** | `bootstrap/schema_sync.py:19-47` 이 내는 DDL 은 `CreateTable`(표가 아예 없을 때)과 `ALTER TABLE … ADD COLUMN` 둘뿐이다. `UniqueConstraint` 를 다루는 코드가 없고 `CreateIndex` 도 새 표일 때만 붙는다(`:30`). 그 파일 자신이 "**a development convenience, not a migration tool**"(`:6-7`)이라고 적는다 |

**그래서 이 work 가 하는 것**

- 컬럼·원장·부분 unique 제약을 **모델 metadata 에만** 더한다. 스키마 소유는 `reset_demo` 그대로다.
- DB 수준 활성 담당 유일성은 **이 work 전용으로 만든 빈 격리 테스트 데이터베이스**에 목표 스키마를
  세워 검증한다(§ 검증 환경). DB 제약을 application 검사로 낮추지 않는다.
- **기존 DB 에 `sync-demo-schema` 가 이 제약을 더할 수 있다고 적지 않는다** — 못 한다.
- **기존 데이터베이스의 적용·전환은 이 실행 범위 밖이다.** 별도 gated work 다. 실제 사용자 데이터가
  든 데이터베이스를 reset 하지 않고, 이 work 의 어떤 검증도 그 DB 에서 돌지 않는다.
- 기존 행의 backfill·전환은 하지 않는다(#7 D4).

**SPEC 에 환류해야 하는 외부 변경**: 없을 것으로 본다. 구현 중 외부에 드러나는
resource/status/enum 이 SPEC 과 달라지면 **코드를 맞추지 말고 SPEC 개정을 먼저 올린다.**

## Dependency

| Consumer | Interface | 설명 |
|---|---|---|
| W2 (완료·승인) | 생성 명령이 세운 **활성 담당**, 수평 요청 출신 업무의 **`source_work_request_id`**, 승인자의 **내부 저장 자리** | 완료 판정이 담당자를 여기서 읽는다. **승인자는 W2 가 입력·화면과 함께 연다** — W1 은 열을 만들 뿐 값을 받지 않는다 |
| W2 (문의·회신 대기) | 업무 식별자와 관계자 집합(담당자·요청자·승인자) | 문의 발송 권한이 이 집합에서 나온다 |
| 업무 페이지 work | 생성 결과의 투영 필드와 `내 업무`/`보낸 업무` 구분 | 축 개편이 이 투영 위에 선다 |
| 회의 slice | 승격이 호출하는 **같은 생성 명령** | 후보 선정·출처 표시는 회의 쪽, 생성 계약은 여기 |

**최소 호환 경계** — W1 만 먼저 나가도 기존 완료·승인이 그대로 돈다.
**W1 이 최종 승인자 계약을 충족한다는 뜻이 아니다** — 승인자는 W2 에서 열린다.

- 완료·승인 흐름은 **현행 그대로 둔다.** `completion_submitted` 제거는 W2 다. W1 은 그 상태를
  만들지도 없애지도 않는다.
- **완료 승인의 연속성은 출처에서 나온다.** 현행 코드가 그렇게 읽는다 —
  `modules/work/application.py:502-504` `requires_completion_review(task)` =
  `task.source_work_request_id is not None`, `:529`·`:638-642` 가 확인자를 그 요청의
  `requester_id` 로 삼는다. 그래서 신규 수평 요청 경로도 **WorkRequest 행과
  `source_work_request_id` 를 계속 세운다**(Phase 4). 세우지 않으면 요청 업무의 완료 승인이
  통째로 사라진다 — #7 W2.0 이 "기존 TaskDelivery/완료 승인 ActionItem 은 유지·활용"이라고
  못 박은 자리다.
- **승인자는 W1 에서 보이지 않는다.** 지금 확인자는 언제나 요청자이므로, 사람이 고른 승인자를
  받아 두고 무시하면 **조용히 어긋나는 약속**이 된다. W1 은 nullable 열만 만들고
  **API 수용도 FE 노출도 하지 않는다.** 둘 다 W2 의 완료 경로와 같은 단위로 켠다.
- 판단함에서 **수락 두 종류가 신규로 생기지 않을 뿐**, 완료 승인과 AX 확인은 그대로 뜬다.
- 과거에 만들어진 수락 대기 항목은 **손대지 않는다.** 읽기 경로의 코드를 지우지 않는 것이
  이 work 의 제약이다(과거 모양의 행을 만드는 fixture 는 #7 D4 가 면제했다).
- 업무 페이지는 현행 축·칩 그대로다. 생성 결과가 **수락 없이** 목록에 서는 것만 달라진다.

## Internal Interface Contract

SPEC 의 외부 API 계약을 복제하지 않는다. 여기 고정하는 것은 **후속 work 가 의존하는 내부 입출력**뿐이다.

**생성 결정 (application 내부)**

하나의 결정 함수가 세 경로(본인 · 수평 요청 · 관리자 배정)를 같은 모양으로 받는다.

- 입력: 행위자 · 수신자(없으면 본인) · 업무 값 · **멱등 키(필수)** · 출처(직접 · 회의 후속).
  **승인자는 입력에 없다** — W1 은 값을 받지 않는다(§ 최소 호환 경계)
- 출력: 만들 업무 값 + **활성 담당 하나** + 필요한 권한 검사 종류
- 실패: 인증·역량 · 대상 부적격 · 멱등 키 누락 · 멱등 키 충돌 — 넷을 다른 오류로 가른다

**세 경로의 권한 검사 — 현행을 보존한다**

| 종류 | 기본 역량(현행 유지) | 수신자 대상 검사 |
|---|---|---|
| `self` | `task.self_manage` — `modules/work/application.py:155` `self._require(principal, TASK_SELF_MANAGE)` | **없다** (대상이 본인이다) |
| `horizontal` | `work_request.create` — `modules/work/requests.py:247` `self._require(principal, WORK_REQUEST_CREATE)` | 허용 후보 판정 (아래) |
| `managed` | `task.assign` — `modules/work/assignments.py:101` | `_may_put_on` 의 조직 범위 검사 (`assignments.py:111`) **그대로 유지** |

> `self` 가 "검사 없음"이 아니다. **수신자 대상 검사만 없다.** 세 경로 모두 인증과 위 기본 역량을
> 그대로 지난다. 결정 함수를 새로 쓰면서 `_require` 를 빠뜨리면 **인증·역량 우회**가 된다.
> 반대로, 리뷰 권고를 근거로 **원래 없던 역량을 다른 경로에 더하지도 않는다.**

> **경로별로 다른 결정 함수를 만들지 않는다.** 지금 생성이 세 곳에 흩어져 있어 한 곳만 고치면
> 나머지가 조용히 어긋난다. 후속 승격도 이 함수를 지나간다.

**멱등 키 — 논리적 생성 명령마다 필수**

- 키는 **호출자가 준다. 없거나 빈 값이면 거부한다.** 키가 없으면 서버에 "같은 명령"을 식별할
  근거가 없고, 일부러 만든 두 건과 네트워크 재시도를 가를 수 없다.
- **키의 범위**: (행위자 · 명령 종류)다. 조직/tenant 경계가 있으면 그 경계를 포함한다.
  전역 키를 쓰지 않는다 — 전역이면 A 가 B 의 키로 재전송했을 때 **B 의 업무가 영수증으로
  돌아간다.** (현행 `tasks.causation_key`·`work_requests.causation_key` 는 전역 unique 이고
  payload 를 비교하지 않는다 — `persistence.py:943` · `:1510`, `work_tasks.py:881-886`.
  그래서 그 열을 그대로 새 계약의 자리로 쓰지 않는다.)
- 같은 키 + **같은 payload 정규화 해시** → 첫 결과를 그대로 돌려준다(**영수증**).
- 같은 키 + **다른 payload** → 충돌로 거절한다. 조용히 첫 결과를 돌려주지 않는다.
- **다른 키 + 같은 내용** → 별개 명령이다. **둘 다 만든다.** 내용 해시·시간창으로 의도적인
  두 업무를 합치지 않는다.
- 영수증을 돌려주기 **전에** 지금 그 사람의 열람·실행 권한을 **다시 검사한다.** 잃었으면
  영수증 대신 존재를 숨긴다.
- **레포에 이미 같은 모양이 있다** — 회의실 예약이 `Idempotency-Key` 헤더를 **필수**로 받고
  (`bootstrap/application.py:1092-1096`), `(owner_id, request_key)` unique 원장에
  `payload_fingerprint` 를 함께 두어 다른 payload 를 충돌로 거절한다
  (`persistence.py:337-350` · `bootstrap/application.py:1168-1184`). 새 원장은 이 모양을 따른다.

**호출자가 키를 어떻게 만드나** — 재시도가 새 키가 되면 멱등성이 무의미해진다.

| 호출자 | 키의 출처 | 근거 |
|---|---|---|
| FE | **한 번의 생성 의도에서 한 개**를 만들어 두고(`frontend/src/lib/idempotency.ts` `createIdempotencyKey()`), 응답 유실·재시도·버튼 연타 동안 **같은 키를 다시 보낸다.** 생성이 확정된 뒤 **새로 만드는 업무는 새 키**다 | 이미 대화 전송(`lib/api.ts:455`) · 요청 댓글(`:711-717`) · 회의 생성(`:925-931`)이 그렇게 한다 |
| REST(그 밖의 호출자) | `Idempotency-Key` 헤더. **누락·빈 값은 거부** | 위 세 라우트와 같은 헤더 이름 |
| MCP | **도구가 `idempotency_key` 를 명시적 인자로 받는다. 누락·빈 값은 거부.** 호출자가 한 생성 의도에서 키를 만들어 **재시도마다 같은 값**을 다시 보내고, 다른 생성 의도에는 새 키를 쓴다. **서버가 호출 시점에 임의 키를 채우지 않는다** | 같은 모양이 이미 있다 — `create_current_meeting` 도구가 `idempotency_key` 를 인자로 받는다(`entrypoints/mcp.py:694-704`) |
| AX 컨텍스트의 도구 호출 | 위와 같다 — **AX 런타임도 논리적 도구 호출마다 안정 키를 실어 보낸다.** turn 식별자 하나로 만들지 않는다 | `AX_MCP_CAUSATION_ID` 는 turn 을 가리킬 뿐 생성 의도를 가리키지 않는다(`mcp.py:627-632`) |
| AX 확인 실행 | 확정된 action 하나가 의도 하나다 — `causation_key=str(action.id)` 는 **그 action 의 재실행 식별**로 그대로 보존한다 | `platform/actions.py:705`·`:816`·`:838` |
| 회의 후속 승격 | 후보 identity(회의 · 요약 · 발언 index)에서 만든 **안정 키**. 재시도해도 같은 값이다 | `modules/meetings/followups.py:21` 이 후보를 이미 그 셋으로 집는다 |

- **서버가 키를 만들어 주는 fallback 을 어느 표면에도 두지 않는다.** 키는 의도가 서는 자리 —
  즉 **호출자** — 에서만 만들어진다. 서버가 호출 시점에 채우면 응답을 잃은 호출자의 재시도가
  새 업무가 되어 「재전송은 영수증」이 성립하지 않는다.
- **대화 turn 하나 = 생성 의도 하나가 아니다.** 한 turn 에서 같은 종류의 업무를 두 건 만들 수
  있고, 그 둘은 **서로 다른 키**를 갖는다. 같은 turn·같은 operation 이라는 사실만으로 두 호출을
  한 건으로 합치지 않는다. payload 는 키 재료가 아니라 **충돌 검사용 지문**이다.
- **고치는 범위는 W1 생성 경로뿐이다.** 여러 mutation 이 함께 쓰는 공용 키 helper
  (`entrypoints/mcp.py:627-632` `_mutation_key`)를 **일괄로 바꾸지 않는다** — 그 helper 는
  일일보고 초안(`:252`)과 회의 예약 fallback(`:704`)도 쓴다. **W1 전용 key resolver 를 따로 두거나
  적용 범위를 명시적으로 W1 생성 도구로 한정**해서, 비 W1 mutation 의 기존 멱등 의미를 건드리지 않는다.
- 회의 후속 승격에는 **두 층**이 있다 — 후보 잠금(`modules/meetings/followups.py:20-27`
  `followup_candidate(..., lock=True)` → `already_promoted`)과 생성 층의 멱등 키.
  **키가 달라도 같은 후보는 한 건**이어야 하므로 두 층을 다 남기고, 코드에 다른 층임을 적는다.

**수신자 허용 판정**

- "내가 이 사람에게 업무를 보낼 수 있나"를 답하는 **하나의 판정**이 있고,
  생성 명령과 후보 목록이 **같은 판정**을 쓴다. 목록과 판정이 갈리면 화면에 뜬 사람에게
  보냈는데 거절되는 모양이 된다.
- 이 판정은 **관리자 배정 권한과 다른 것**이다. 일반 구성원에게 배정 권한(`task.assign`)을
  주는 방식으로 구현하지 않는다.
- **판정의 내용은 정해져 있다** — 현행 `platform/organization_access.py:851-866`
  `work_request_assignee_candidates` 에서 **`work_request.decide` 필터 한 줄(`:861`)을 걷는다.**
  그 역량은 팀장 계열에만 있고(`modules/organization_access/catalog.py:99-118`) 구성원에는
  없어서(`:77-95`), 그대로 두면 **일반 구성원에게는 후보가 한 명도 뜨지 않는다** — #7 W1.5 가 깨진다.
  남는 세 줄은 그대로 재사용한다: **로그인 가능**(`_can_answer`, `:856`) · **본인 제외**(`:856`) ·
  **조직 범위 교집합**(`:863`). 새 역량을 만들지 않고 다른 검사를 더하지도 않는다.
- 명령 쪽은 같은 함수를 지난다 — `modules/organization_access/application.py:210`
  `is_work_request_assignee` 가 이 후보 목록을 그대로 쓰므로 **목록과 판정이 갈리지 않는다.**
- 후보 판정을 고쳐도 **기존 판단 명령의 권한은 그대로**다 — 과거 pending 행의 수락·거절·조정은
  여전히 `work_request.decide` 를 요구한다(`modules/work/requests.py:290`·`:305`·`:327`).

## Execution

각 Phase 의 상태는 `TODO / IN_PROGRESS / DONE / BLOCKED / SUPERSEDED` 중 하나다.
Phase 별 `검증` + `완료 증거`가 완료 조건이다.

**검증 명령** (계획이다. **이 문서를 쓰는 단계에서는 하나도 실행하지 않았다.**)

백엔드 테스트는 **항상 Makefile 타겟**으로 돈다 — `AGENTS.md` 「테스트」가
`cd backend && uv run pytest …` 직접 호출을 금지한다(병렬 옵션이 빠진다).

| 명령 | 무엇 |
|---|---|
| `make test-unit` | `tests/unit` + `tests/architecture` (operation inventory·DDL 소유 테스트가 여기 있다) |
| `make test-contract` | `tests/contract` |
| `make test` | 백엔드 스위트. `backend/pyproject.toml` `addopts` 가 `integration`·`release`·`scale` 을 **제외**한다 — 「전량」이 아니다 |
| `make frontend-test` | 프론트엔드 단위 |
| `make test-postgres` | 실제 PostgreSQL 통합(`-m integration`). `POSTGRES_TEST_URL` 이 `DATABASE_URL` 과 같으면 **실행을 거부한다**(`Makefile:52-54`) |
| `make verify` | `test test-scale test-release frontend-test frontend-assets frontend-build` — 최종 게이트(`Makefile:65`) |
| `make acceptance-e2e` | 브라우저 journey. **자기 DB(`ACCEPTANCE_DATABASE_URL`)를 스스로 reset 하고 돈다**(`Makefile:328-329`) |

**검증 환경 — 이 work 전용 빈 격리 데이터베이스**

```
make postgres-up                                    # Makefile:80-84
docker compose exec -T postgres psql -U ax -d postgres -c "CREATE DATABASE ax_test_w1"
make reset-demo DATABASE_URL=postgresql+psycopg://ax:ax@localhost:54329/ax_test_w1
make test-postgres POSTGRES_TEST_URL=postgresql+psycopg://ax:ax@localhost:54329/ax_test_w1
```

- 이름이 `ax_test_…` 여야 한다 — `entrypoints/reset_demo.py:15` `_SAFE_POSTGRES_DATABASE`
  가 `ax_demo`·`ax_test*` 만 통과시키고 그 밖은 연결 전에 거부한다.
- 통합 테스트는 스스로 `reset_database(AX_POSTGRES_TEST_URL)` 을 부른다
  (`tests/integration/postgres/test_postgres_integration.py:16`·`:212`) — **빈 DB 에 목표 스키마를
  세우는 그 경로**가 새 제약이 실제로 서는지 보는 자리다.
- **사람이 쓰는 `DATABASE_URL`(`ax_demo`)을 이 work 의 어떤 명령도 건드리지 않는다.**
  로컬 사용자 DB 에서 돌려 놓고 「격리에서 돌렸다」고 적지 않는다.
- **환경을 확인하지 못한 것은 required test 의 면제 사유가 아니다.** 위 네 줄이 환경을 세우는
  전부이고, 검증이 끝나지 않으면 그 phase 는 완료가 아니다.
- **DB reset·실제 데이터 삭제·배포는 이 work 에 없다.** 위 reset 은 **일회용 DB** 에서만 돈다.

**머지 단위** — 권한 없이 타인 생성이 열리는 중간 상태를 만들지 않는다.

| 단위 | phase | 규칙 |
|---|---|---|
| MU-A | 1 · 2 · 3 | 입력·멱등·권한 판정이 **한 덩어리로** 머지된다. Phase 3 이 서기 전에 수신자 인자가 어느 표면에도 열리지 않는다 |
| MU-B | 4 · 5 | 수락 gate 제거와 승격 정렬 |
| MU-C | 6 · 7 | 표면 공개(REST·MCP·AX·seed)와 FE. **REST 요청 모델이 `assignee_id` 를 받기 시작하는 것도 여기다** — 라우트가 그 값을 실제로 소비하는 자리와 같은 단위다. 타인 생성이 밖에서 보이는 것은 여기서 처음이고, 그때 권한 판정은 이미 MU-A 에 있다 |
| MU-D | 8 | 회귀·문서 동기화 |

### Phase 1 — 생성 입력 계약과 결정 함수

- **Status**: DONE
- **설명**: 세 경로가 같은 입력·같은 결정을 지나가게 만든다. 여기가 안 서면 나머지 phase 가
  경로마다 다른 규칙을 갖게 된다. 생성 입력 모델이 `extra='forbid'` 라 **본문으로 받을 필드를
  여기서 열지 않으면 REST 가 아예 거부한다** — 수신자가 그 경우다. **멱등 키는 본문 필드가 아니라
  `Idempotency-Key` 헤더**이므로 입력 모델에 열지 않는다.
- **작업**:
  - [ ] **내부** 생성 입력에 **수신자**를 연다. 기존 필드의 뜻을 바꾸지 않는다
  - [ ] **멱등 키는 REST 본문이 아니라 `Idempotency-Key` 헤더에서 받아** application 인자로 넘긴다.
        생성 요청 본문 모델에 `idempotency_key` 필드를 **열지 않는다**(`extra='forbid'` 가 계속
        거부한다). MCP 는 도구의 명시적 인자로 같은 값을 받는다(Phase 6)
  - [ ] **내부 입력 모델과 외부 REST 요청 모델을 가른다** — 내부 결정 함수는 수신자를 받지만,
        **MU-A·MU-B 동안 REST 요청 모델은 `assignee_id` 를 받지 않는다.** 라우트가 그 값을
        실제로 소비하는 **MU-C 에서 함께 연다** — 받아 두고 무시하는 중간 상태를 만들지 않는다
  - [ ] 수신자가 없거나 본인이면 본인 업무, 다르면 타인 배정으로 가르는 **결정 함수**를 세운다
  - [ ] 검사 종류 셋(`self` · `horizontal` · `managed`)을 결정 함수가 돌려주게 한다.
        **세 경로의 기본 역량 검사는 현행 그대로 남긴다**(§ Internal Interface Contract 의 표)
  - [ ] 승인자는 **내부 nullable 열만** 더한다. 입력 모델에 열지 않고 응답에도 싣지 않는다 —
        W1 에서 작동하는 public 필드로 표시하지 않는다
  - [ ] 기존 본인 생성 호출부가 새 입력으로 그대로 통과하는지 확인한다
- **검증**:
  - [ ] 수신자 없음 / 본인 / 타인 세 입력이 각각 맞는 검사 종류를 낸다 (단위)
  - [ ] **세 경로 모두 인증·역량 없는 principal 을 거부한다** — `self` 도 `task.self_manage` 를 지난다
  - [ ] 알 수 없는 필드는 여전히 거부된다 (입력 모델의 기존 성질 유지). **승인자 필드도
        본문 `idempotency_key` 도 보내면 거부된다** — 승인자는 W1 이 받지 않고, 키는 헤더로 온다
  - [ ] **MU-A·MU-B 시점의 REST 생성 요청에 `assignee_id` 를 실으면 명시적으로 거부된다**
        (조용히 무시되지 않는다). 허용은 MU-C 와 함께다
  - [ ] 멱등 키 헤더가 없거나 빈 값이면 거부된다
  - [ ] 제목 길이·일정 검증 등 기존 규칙이 그대로 산다
  - [ ] `make test-unit`
- **완료 증거**: BE 계약/권한/원자성·출처 검증 및 코드 재검수2차 PASS. backend-report.md, backend-review-fix1-report.md, backend-review-fix2-report.md의 해당 Phase/지적별 증거; 코디 BE1297·PG65 통과.

### Phase 2 — 멱등 키·활성 담당 유일성·원자성

- **Status**: DONE
- **설명**: **전부 신규 계약이다.** 지금 REST 재전송은 중복 업무를 만들고 활성 담당 유일성을
  막는 제약이 없다. 기존 AX 키 재조회 경로는 REST 를 덮지 않는다.
- **작업**:
  - [ ] 멱등 원장을 세운다 — (행위자 · 명령 종류 · 키) unique + payload 지문.
        `meeting_room_creation_attempts`(`persistence.py:337-350`) 와 같은 모양
  - [ ] 같은 키 + 같은 payload → 첫 결과 반환. **돌려주기 전에 현재 열람 권한을 다시 검사**하고,
        잃었으면 존재를 숨긴다
  - [ ] 같은 키 + **다른 payload** → 충돌 거절. 성공으로 위장하지 않는다
  - [ ] 업무 + 활성 담당을 **한 transaction** 으로 만든다
  - [ ] 활성 담당 유일성을 **DB 제약**(부분 unique 인덱스)으로 모델 metadata 에 세운다.
        application 검사로 낮추지 않는다
  - [ ] 기존 전역 `causation_key` 열(`persistence.py:943`·`:1510`)과의 관계를 정하고 근거를 남긴다 —
        **뜻이 다르므로 새 원장을 쓰고 기존 열의 동작은 바꾸지 않는다**가 기본값이다
  - [ ] **migration 을 새로 들이지 않는다.** 스키마 소유는 `reset_demo` 그대로다(§ 스키마를 어디에 세우나)
- **검증**:
  - [ ] 같은 키 재전송 N 회 → 업무 1건, 응답 동일 (**영수증**)
  - [ ] 같은 키 + 다른 payload → 충돌 오류. 업무가 만들어지지 않는다
  - [ ] **다른 키 + 같은 내용** 두 명령 → 업무 2건 (합치지 않는다)
  - [ ] 키 누락·빈 값 → 거부. 업무 0건
  - [ ] 영수증 경로에서 **권한을 잃은 호출자**는 결과 대신 존재 은닉을 받는다
  - [ ] **같은 키의 동시 실행 두 건 → 업무 1건** (격리 PostgreSQL)
  - [ ] 활성 담당을 둘로 만들려는 직접 시도가 **DB 층에서** 막힌다 (격리 PostgreSQL)
  - [ ] transaction 중간 실패 시 업무만 남거나 담당만 남지 않는다
  - [ ] `make test-contract` · 전용 빈 DB 에서 `make test-postgres`
- **완료 증거**: BE 계약/권한/원자성·출처 검증 및 코드 재검수2차 PASS. backend-report.md, backend-review-fix1-report.md, backend-review-fix2-report.md의 해당 Phase/지적별 증거; 코디 BE1297·PG65 통과.

### Phase 3 — 권한 경계

- **Status**: DONE
- **설명**: 일반 구성원이 동료에게 보낼 수 있어야 하되, **관리자 배정 권한을 주는 방식으로는
  안 된다.** 신규 요청 권한과 기존 업무 재배정 권한은 계속 갈린다.
- **작업**:
  - [ ] `work_request_assignee_candidates`(`platform/organization_access.py:851-866`)에서
        **`work_request.decide` 필터(`:861`)를 걷는다.** 나머지 세 줄(로그인 가능 `:856` ·
        본인 제외 `:856` · 조직 범위 교집합 `:863`)은 **그대로 둔다**
  - [ ] 명령과 목록이 같은 판정을 쓰는지 확인한다 —
        `modules/organization_access/application.py:210` `is_work_request_assignee` 가 같은 함수를 지난다
  - [ ] 그 판정을 **관리자 배정 권한과 분리**한다. 일반 구성원 역할에 `task.assign` 을 추가하지 않는다
  - [ ] 행위자 쪽 역량은 **경로별 현행 검사를 유지**한다 (`work_request.create` 등)
  - [ ] 관리자 직접 배정의 조직 범위 검사를 **그대로 유지**한다
  - [ ] 기존 업무의 담당자 변경은 **별도 명령·별도 권한**으로 남긴다
  - [ ] 관계자 밖에는 업무의 **존재도 알리지 않는** 현행 열람 경계를 유지한다
- **검증**:
  - [ ] **배정 역량(`task.assign`)도 판단 역량(`work_request.decide`)도 없는 구성원이
        같은 구성원에게 보내면 성공한다** — #7 W1.5 가 여기서 선다
  - [ ] 후보 목록에 **그런 일반 구성원이 뜬다** (필터를 걷은 결과가 목록에도 보인다)
  - [ ] 같은 사람이 **허용 후보 밖**에게 보내면 거절된다
  - [ ] 같은 사람이 **타인의 기존 업무**를 수정·재배정하려 하면 거절된다
  - [ ] 관리자 배정이 **조직 범위 밖** 대상에 대해 여전히 거절된다
  - [ ] 후보 목록에 뜬 사람에게 보낸 것이 거절되지 않는다 (목록 ↔ 판정 일치)
  - [ ] 일반 구성원 역할의 역량 집합에 배정 권한이 **추가되지 않았다**
  - [ ] 과거 pending 요청의 수락·거절·조정은 **여전히 `work_request.decide` 를 요구한다**
        (후보 판정 변경이 그 명령의 권한을 넓히지 않았다)
  - [ ] 권한 밖 대상·조직 범위 위반이 각각 다른 오류로 구분된다
  - [ ] `make test-unit` · `make test-contract`
- **완료 증거**: BE 계약/권한/원자성·출처 검증 및 코드 재검수2차 PASS. backend-report.md, backend-review-fix1-report.md, backend-review-fix2-report.md의 해당 Phase/지적별 증거; 코디 BE1297·PG65 통과.

### Phase 4 — 신규 수락 gate 제거

- **Status**: DONE
- **설명**: 신규 생성이 수락용 판단·수락 대기 배정·재상신 회차를 만들지 않게 한다.
  **완료 승인과 AX 실행 확인은 그대로 남는다** — 걷는 대상을 잘못 잡으면 승인까지 사라진다.
  경계는 SPEC-002 §2.2 종류 표다.
- **작업**:
  - [ ] 생성·배정·수평 요청이 수락용 판단 항목을 만들지 않게 한다 — 신규 경로에서
        `DecisionItemRecord(kind="work_request.acceptance")` · `SubmissionRecord` ·
        `ReviewAssignmentRecord(status="pending")` 세 줄을 만들지 않는다
        (`platform/work_tasks.py:939-963` 이 지금 만드는 자리다)
  - [ ] **수평 요청은 WorkRequest 행과 `source_work_request_id` 를 계속 세운다.**
        걷는 것은 **수락 대기 상태와 판단 회차**뿐이다. 업무·활성 담당·출처는 한 transaction 에 선다
  - [ ] **사람이 하지 않은 판단을 기록하지 않는다** — 신규 경로는 `record_decision(…, "accept")`
        도 `work_request.accepted` 감사도 남기지 않는다(`modules/work/requests.py:288-301`).
        담당 행의 `accepted_at` 은 현행 본인 생성과 같은 뜻(담당이 선 시각, `work_tasks.py:358`)으로만 쓴다
  - [ ] **요청 출처 상태값은 `assigned`(즉시 배정됨)다** (DEC-001 D-3c). `pending` 으로 두면
        아무도 기다리지 않는데 「판단 대기」로 읽히고 수신함(`work_tasks.py:1370`
        `state.in_(("pending","negotiating"))`)에 서며, `accepted` 로 두면 **사람이 하지 않은
        수락을 기록**하는 것이 된다. `assigned` 는 **판단 없이 업무와 활성 담당이 섰다는 사실만**
        말한다. 기존 다섯 값(`pending`·`negotiating`·`accepted`·`rejected`·`withdrawn`)의 뜻은
        바꾸지 않는다. **이것은 출처 상태이고 업무의 수행 상태(`open`…)와 다른 축이다**
  - [ ] `assigned` 를 쓰고 읽는 자리를 **전수로 센다** — **쓰기** `platform/work_tasks.py:901`
        (`create_request` 가 지금 `state="pending"` 을 박는 자리) · **읽기** `work_tasks.py:1370`
        (수신함) · `platform/action_center.py:302`(`request_state` 재전송 판정) ·
        `modules/work/requests.py:808`(`_decision_target`) · `request_lifecycle.py:133`·`:147`·`:190`
        (수정·재상신·철회 가드) · `frontend/src/lib/viewModels.ts:459`(union) ·
        `frontend/src/lib/labels.ts:22-34`(라벨·톤). 목록 밖에서 실패가 난다
  - [ ] 재상신 회차를 신규 경로에서 열지 않는다
  - [ ] **신규 경로에 거절 명령을 신설하지 않는다** (DEC-001 D-4 — 원문 확정 제외).
        과거 행을 위해 존재하는 기존 endpoint(`entrypoints/http.py:1392` 배정 거절 ·
        `:1982` 요청 거절)를 **지우는 것이 아니다** — 신규 경로가 그 명령을 열지 않는다는 뜻이다
  - [ ] 완료 승인·AX 확인 종류가 계속 등록되는지 확인한다
  - [ ] 과거 수락 항목의 **읽기 경로(목록·상세·이력) 코드를 지우지 않는다.**
        (과거 모양의 행을 만드는 fixture 는 #7 D4 가 면제했다 — 만들지 않는다)
  - [ ] 요청자·담당자·행위자·출처·시각과 근거 보존을 확인한다
- **검증**:
  - [ ] 본인 생성 / 구성원 타인 생성 / 관리자 배정 세 경로 모두 수락 판단 **0건** 생성
  - [ ] 세 경로 모두 상대 목록에 **즉시** 서고 바로 시작할 수 있다
  - [ ] 그 경로에 **본인 업무 선생성·관리자 재배정·상대 수락**이 요구되지 않는다
  - [ ] 완료 승인 항목과 AX 실행 확인 항목이 **여전히 생성되고 뜬다**
  - [ ] **완료 연속성 — 생성 타입별로 본다**
        · 본인 생성 → `source_work_request_id` 없음 → 완료 보고 없이 바로 완료(현행 그대로)
        · **신규 수평 요청 생성 → `source_work_request_id` 있음 → 완료 보고가 열리고
        확인자가 그 요청의 요청자다** (`application.py:502-504`·`:529`·`:638-642` 경로가 그대로 돈다)
        · 관리자 배정 → 현행 그대로
        · 회의 후속 승격 → 두 갈래(업무 승격 · 요청 승격) 각각
  - [ ] 신규 경로가 만든 요청의 출처 상태가 **`assigned`** 이고, 거기에 **판단 명령(수락·거절·조정)이
        걸리지 않는다** — `_decision_target` 이 판단 대기가 아닌 상태를 거부한다
  - [ ] 과거 행의 다섯 상태값이 **뜻도 화면 표시도 그대로**다
  - [ ] 신규 경로가 만든 요청이 **수신자의 수신함에 서지 않는다**
  - [ ] AX 제안은 사람 확인 전 effect 가 없다
  - [ ] **신규 생성 경로에** 거절 명령이 노출되지 않는다 (과거 행용 기존 endpoint 는 그대로 있다)
  - [ ] 생성 이력에 요청자·담당자·행위자·시각·출처가 남고 **진행 기록에서 읽힌다**
  - [ ] `make test-contract`
- **선택 검증**(필수 아님 — fixture 를 새로 만들지 않는다): 과거 수락 행이 남아 있는 DB 에서
  목록·상세 조회가 깨지지 않는다
- **완료 증거**: BE 계약/권한/원자성·출처 검증 및 코드 재검수2차 PASS. backend-report.md, backend-review-fix1-report.md, backend-review-fix2-report.md의 해당 Phase/지적별 증거; 코디 BE1297·PG65 통과.

### Phase 5 — 회의 후속 승격 정렬

- **Status**: DONE
- **설명**: 승격이 이미 생성 경로를 직접 호출한다. 생성이 바뀌면 승격 동작도 같이 바뀐다 —
  추적이 아니라 **영향**이다. 우회 adapter 를 남기지 않는다.
- **작업**:
  - [ ] 승격이 Phase 1 의 **결정 함수**를 지나가게 한다
  - [ ] 담당을 지정한 승격이 **수락 없이** 그 사람의 업무가 되게 한다
  - [ ] 승격 권한 + 생성 권한을 함께 검사한다
  - [ ] 승격에도 **멱등 키**를 실어 생성 층에서 중복을 막는다. 키는 **후보 identity
        (회의 · 요약 · 발언 index)에서 만든 안정 값**이라 재시도해도 같다 — 기존 승격 기록 층
        (`modules/meetings/followups.py:20-27`)의 중복 방지와 **다른 층**임을 코드에 남긴다
  - [ ] **자동 승격을 만들지 않는다.** 사람의 명시적 행동만 승격한다
  - [ ] 만들어진 업무가 출처 회의로 돌아갈 수 있는지 확인한다
- **검증**:
  - [ ] 같은 회의 후보를 **여러 번 승격**해도 업무는 1건
  - [ ] **같은 후보의 동시 승격 두 건 → 업무 1건.** 키가 서로 달라도 후보 identity 로 1건이다
        (격리 PostgreSQL)
  - [ ] 담당을 지정한 승격이 상대 목록에 즉시 선다
  - [ ] 승격 권한만 있고 생성 권한이 없으면 거절된다
  - [ ] 승격된 업무에서 원본 회의로 갈 수 있다
  - [ ] 승격 전용 우회 생성 경로가 코드에 남아 있지 않다
  - [ ] 자동으로 승격되는 경로가 없다
  - [ ] `make test-contract` · 전용 빈 DB 에서 `make test-postgres`
- **완료 증거**: BE 계약/권한/원자성·출처 검증 및 코드 재검수2차 PASS. backend-report.md, backend-review-fix1-report.md, backend-review-fix2-report.md의 해당 Phase/지적별 증거; 코디 BE1297·PG65 통과.

### Phase 6 — 표면 정렬 (REST · MCP · AX · seed)

- **Status**: DONE
- **설명**: 네 표면이 **같은 application 계약**을 쓰게 한다. 표면마다 다른 규칙을 두면
  한쪽에서만 수락 gate 가 살아남는다.
- **작업**:
  - [ ] REST 생성·배정·요청·후보 라우트를 새 계약에 맞춘다 — **이 단위에서 생성 요청 모델의
        `assignee_id` 를 열고, 같은 커밋에서 라우트가 그 값을 소비한다**(MU-A·MU-B 의 거부 가드를
        여기서 걷는다)
  - [ ] REST 에서 **수락·거절 라우트의 처분**을 정한다 — 신규가 만들지 않는다는 것은 이미
        계약이고, 과거 행을 위해 남길지는 Open Issues 를 닫은 뒤 반영한다
  - [ ] MCP 도구와 명령→권한 표를 맞춘다. **일반 구성원 경로에 배정 권한을 요구하지 않는다**
  - [ ] AX 확인 대상 action type 을 유지한다. 제안 확정 전 effect 없음을 확인한다
  - [ ] AX 초안 정규화 필드 집합에 새 생성 필드를 반영한다
  - [ ] REST 생성 라우트가 **`Idempotency-Key` 헤더를 필수로** 받게 한다 — 누락·빈 값은 거부.
        헤더 이름은 레포가 이미 쓰는 것과 같다(`entrypoints/http.py:620`·`1085`·`1785`)
  - [ ] **W1 MCP 생성 도구에 `idempotency_key` 인자를 연다** — `create_self_task`(`mcp.py:609`) ·
        `create_work_request`(`:328`) · `assign_task`(`:1028`) · `promote_current_meeting_todo`(`:756`).
        **누락·빈 값은 거부**하고, 서버가 대신 만들어 채우지 않는다.
        `create_current_meeting`(`:694`·`:704`)이 이미 같은 인자를 받는다 — 모양을 따르되
        **fallback 은 두지 않는다**
  - [ ] **그 인자의 설명과 도구 스키마에 규칙을 적는다** — 「한 생성 의도에 키 하나 ·
        재시도는 같은 키 · 새 생성 의도는 새 키」. 외부 호출자는 스키마만 보고 부르므로,
        설명이 없으면 매 호출 새 키를 만들어 계약이 깨진다
  - [ ] **공용 `_mutation_key`(`mcp.py:627-632`)를 일괄로 바꾸지 않는다.** W1 전용 key resolver 를
        따로 두거나 적용 범위를 W1 생성 도구로 명시적으로 한정한다 — 그 helper 를 쓰는
        일일보고 초안(`:252`)·회의 예약 fallback(`:704`)의 **기존 멱등 의미는 그대로 둔다**
  - [ ] AX 실행이 이미 안정적인 `causation_key=str(action.id)`(`platform/actions.py:705`·`816`·`838`)를
        **새 키 자리에 그대로 실어 보내게** 한다
  - [ ] **operation inventory drift 를 패치한다** — `tests/architecture/test_operation_inventory.py`
        가 `docs/unified-operations-inventory.json` 과의 차이를 잡는다. **diff 난 항목만** 고치고
        전체 재작성은 하지 않는다(`AGENTS.md`)
  - [ ] **승인자는 어느 표면에도 열지 않는다** — REST·MCP·AX 초안 어디에도 입력 필드가 없다
  - [ ] seed·fixture 를 새 모델로 바꾼다 — 시나리오의 **수락 여부 열**이 더는 필요 없다
  - [ ] seed 가 수락 대기 배정·수락 판단을 만들지 않는지 확인한다
- **검증**:
  - [ ] REST·MCP·AX 세 표면에서 같은 입력이 같은 결과를 낸다
  - [ ] MCP 권한 표에 일반 구성원 타인 생성이 배정 권한으로 걸려 있지 않다
  - [ ] AX 제안 → 사람 확인 → 실행 경로가 그대로 돈다
  - [ ] AX 확인 전에는 업무가 생기지 않는다
  - [ ] seed 실행 결과에 수락 대기 배정 0건, 수락 판단 0건
  - [ ] seed 가 만든 데이터로 세 생성 경로가 전부 동작한다
  - [ ] 세 표면 모두 **멱등 키 누락·빈 값을 거부**한다 (MCP 는 **명시 인자**로 받는다)
  - [ ] 같은 키 + 같은 payload 로 다시 부르면 **1건**, 같은 키 + 다른 payload 는 **충돌**
  - [ ] **같은 대화 turn · 같은 도구 · 다른 명시 키** 두 호출 → **생성 2건**
  - [ ] 응답을 잃은 호출자가 **같은 키로 다시 부르면 1건**이다
  - [ ] **다른 행위자 · 다른 조직 범위의 같은 키가 서로 섞이지 않는다**
  - [ ] 조회·제안만으로는 업무가 생기지 않고 **AX 실행 확인이 그대로 남는다**
  - [ ] **비 W1 mutation(일일보고 초안·회의 예약)의 멱등 동작에 회귀가 없다**
  - [ ] `test_operation_inventory` 통과 (`make test-unit` 에 포함)
  - [ ] `make test`
- **완료 증거**: BE 계약/권한/원자성·출처 검증 및 코드 재검수2차 PASS. backend-report.md, backend-review-fix1-report.md, backend-review-fix2-report.md의 해당 Phase/지적별 증거; 코디 BE1297·PG65 통과.

### Phase 7 — 프론트엔드

- **Status**: DONE
- **설명**: 생성 창에 담당 필드를 세우고, **수락하면 그 사람의 업무가 된다**는 현행 문구를
  걷는다. 업무 페이지의 축·칩 개편은 이 work 가 아니다.
- **작업**:
  - [ ] 생성 창에 담당 필드를 연다. 기본값은 나, 후보는 **Phase 3 의 판정이 낸 목록**
  - [ ] 보낼 수 있는 사람이 없으면 담당 필드 자체를 세우지 않는다
  - [ ] 문구를 바꾼다: 타인 지정 시 **"상대의 수락 없이 바로 그 사람의 업무가 됩니다"**
  - [ ] 「수락하면 그 사람의 업무가 됩니다」류 문구를 전부 걷는다
  - [ ] 요청 출처 상태 **`assigned`** 를 FE 타입(`lib/viewModels.ts:459`)과 라벨·톤
        (`lib/labels.ts:22-34`)에 더한다. 문구는 **「즉시 배정됨」** 계열로, 「수락됨」과 섞지 않는다.
        기존 다섯 값의 라벨은 건드리지 않는다
  - [ ] **생성 의도 하나에 멱등 키 하나**를 만들어 두고(`lib/idempotency.ts` `createIdempotencyKey()`),
        재시도·연타 동안 **같은 키**를 다시 보낸다. 성공한 뒤 새로 만드는 업무는 **새 키**다
  - [ ] 제출 중 버튼 비활성 — 화면에서도 두 건이 만들어지지 않는다
  - [ ] 생성 성공 후 내 목록/보낸 목록에 즉시 반영한다
  - [ ] 판단함에서 수락 카드가 더는 생기지 않는 것을 반영하고 **빈 상태 문구**를 손본다
  - [ ] 기존 부품만 쓴다 — 새 부품을 만들지 않는다
- **검증**:
  - [ ] 타인 지정 생성 → 성공 토스트가 **누구의 업무가 되었는지** 말한다
  - [ ] 화면 어디에도 「수락」 대기 문구가 남아 있지 않다
  - [ ] 보낼 수 있는 사람이 없는 계정에서 담당 필드가 안 뜬다
  - [ ] **생성 창에 승인자 필드가 없다** — W2 에서 완료 경로와 함께 연다
  - [ ] 제출 버튼 연타로 두 건이 만들어지지 않는다 (**같은 키 재전송**)
  - [ ] 판단함 빈 상태 문구에서 「동료의 요청, 관리자의 배정」이 빠졌다
  - [ ] `make frontend-test` · `npx tsc --noEmit` · `npx vite build`
- **완료 증거**: FE645·타입검사·자산·빌드 코디 통과(Node20.20.0), F1 회귀7건 및 코드 재검수2차 PASS.

### Phase 8 — 회귀와 문서 동기화

- **Status**: IN_PROGRESS
- **설명**: 바뀐 외부 동작마다 테스트가 있는지 확인하고, 현행을 서술한 제품 문서를 맞춘다.
- **작업**:
  - [ ] SPEC-001 §6 의 **W1 인수조건**을 한 줄씩 대조하고 테스트로 덮인 자리를 표시한다
  - [ ] 덮이지 않은 인수조건에 테스트를 더한다
  - [ ] 코드 레포의 제품 문서에서 **수락 전제 서술**을 갱신한다
        (README 업무 절 · 도메인 모델 · 운영 문서). **→ allowed_paths 밖이라 코디 담당**
  - [ ] 배정 application 의 docstring 등 수락 전제를 못 박은 주석을 고친다
  - [ ] W2 가 소비할 경계를 인수인계 메모로 남긴다 — 활성 담당 · `source_work_request_id` ·
        **아직 열리지 않은 승인자 저장 자리**(입력·화면은 W2 가 켠다) · 관계자 집합
- **검증**:
  - [ ] SPEC-001 §6 W1 인수조건 전 항목에 대응 테스트가 있다
  - [ ] **`make verify`** (`test test-scale test-release frontend-test frontend-assets frontend-build`)
  - [ ] **전용 빈 DB 에서 `make test-postgres`**
  - [ ] **핵심 acceptance journey** — `make acceptance-e2e`(자기 DB 를 스스로 reset 한다).
        최소한 W1 이 닿는 journey 는 전부 돈다: `e2e-task-lifecycle` · `e2e-task-origin` ·
        `e2e-work-request` · `e2e-work-relations` · `e2e-ax-task-request` · `e2e-action-item` ·
        `e2e-access-roles`
  - [ ] 완료·승인 기존 흐름이 깨지지 않았다 (W2 전 최소 호환)
  - [ ] 제품 문서에 수락 필수 서술이 남아 있지 않다
- **완료 증거**: 코드 리뷰 PASS 및 자동 검증 단계별 통과. 마지막 scoped84 통과 보고. 사용자 지시에 따라 E2E는 사용자 수행 대기이며 미실행. 단일 make verify green 아님; 실행 환경과 로그는 verification-and-e2e.md.

## Pre-deploy Check

**이 work 에 배포는 없다.** 아래는 나중에 이 변경이 실제 환경으로 나갈 때 보는 항목이다.

- [ ] 기존 완료·승인 흐름에 영향 없음 — W2 전이라도 제품이 돈다
- [ ] 과거 수락 대기 데이터가 **그대로 남아 있고** 읽힌다
- [ ] 새 credential·env 노출 없음 (외부 연동을 붙이지 않았다)
- [ ] 생성 응답에 관계자 밖에게 새는 필드가 없다
- [ ] **기존 데이터베이스에 새 열·새 제약을 어떻게 세울지의 절차는 아직 없다.**
      `sync-demo-schema` 는 컬럼은 더해도 **제약은 만들지 못한다**(`schema_sync.py:19-47`).
      그 절차를 만드는 것은 **별도 gated work** 이고 이 work 는 하지 않는다

## Rollback

- 되돌리기의 단위는 **코드·모델**과 **일회용 검증 환경**이다. migration 이 없으므로
  **downgrade 도 없다** — 있지도 않은 downgrade 와 「데이터 무손실」을 발명하지 않는다.
  검증에 쓰는 DB 는 버릴 수 있는 것이고, 되돌린 모델로 다시 `reset-demo` 하면 그만이다.
  **이미 데이터가 든 데이터베이스에서 열·제약을 내리는 절차는 이 work 에 없다.**
- 부분 revert 는 **머지 단위**로 한다(§ Execution 의 MU 표). MU-A(Phase 1·2·3)를 쪼개
  되돌리지 않는다 — 권한 판정만 빠진 중간 상태가 생긴다.
- MU-B(Phase 4·5)만 되돌리면 수락 gate 가 되살아나므로 **MU-B 는 MU-A 보다 먼저 되돌린다.**
- MU-C 를 되돌리면 표면과 생성 창이 함께 예전으로 돌아간다. **멱등 키가 필수**이므로
  되돌린 FE 가 키를 싣지 않는다면 BE 도 함께 되돌린다 — FE 만 따로 되돌릴 수 있다고
  적지 않는다(새 필드가 「선택」이던 전제는 더 이상 성립하지 않는다).

## 인수조건 추적

SPEC-001 §6 의 **W1 인수조건** 열두 줄이 어느 phase 의 검증으로 닫히는지. Phase 8 이 이 표를
한 줄씩 다시 대조한다. **표에 없는 줄이 생기면 그 phase 의 검증을 늘린다.**

| SPEC-001 §6 W1 인수조건 | 닫는 자리 |
|---|---|
| 본인 생성 한 건 · 수락 카드 없음 | Phase 4 |
| 배정 권한 없는 구성원의 한 번 명령 → 상대 목록에 즉시 · 바로 시작 | Phase 3 · Phase 4 |
| 선생성·재배정·상대 수락 불요 | Phase 4 |
| 수락용 판단 항목 · 수락 대기 배정 · 재상신 회차 미생성 | Phase 4 |
| 신규 생성 경로에 배정 거절 명령이 없음 | Phase 4 · Phase 6 |
| 신규 요청 권한으로 타인 기존 업무 수정·재배정 불가 | Phase 3 |
| 관리자 직접 배정의 조직 범위 검사 유지 | Phase 3 |
| 권한 밖 담당 지정 거부 | Phase 3 |
| 멱등 키 필수 · 재전송 1건 · 같은 키 동시 실행 중복 업무 0 · 중복 활성 담당 0 | Phase 2 |
| 요청자·담당자·출처·행위자·시각 보존 · 진행 기록에서 읽힘 | Phase 4 |
| 화면·REST·MCP·AX 같은 계약 · AX 확인 존치 · 확인 전 effect 없음 | Phase 6 · Phase 7 |
| 회의 후속 승격의 동일 명령·권한·멱등성 · 재승격 1건 · 원본 회의 복귀 | Phase 5 |

**W2 인수조건(13번째 줄부터)은 이 work 가 닫지 않는다.**

## Done Criteria

- [ ] 모든 Phase 가 `DONE` 또는 `SUPERSEDED` 다.
- [ ] SPEC-001 §6 의 **W1 인수조건**이 전부 검증 항목에 반영됐다.
- [ ] 멱등·동시성·권한·승격 테스트가 전부 있다.
- [ ] product `log.md` 와 `30-work/README.md` 가 갱신됐다. **→ allowed_paths 밖이라 코디 담당**
- [ ] **#7 전체를 완료로 표시하지 않는다.** W1 slice 만 닫는다.

## Open Issues

개발 내부 이슈다. 사용자 결정이 필요해지면 decision 으로 승격한다.

1. **멱등 원장을 새 표로 둘지 기존 행에 붙일지.** 계약(행위자 scope · payload 지문 · 충돌)은
   정해졌고 남은 것은 저장 모양이다. 기존 전역 `causation_key` 열은 **뜻이 다르므로 그대로 둔다**
   가 기본값이다. Phase 2 가 정하고 근거를 남긴다.
2. **과거 수락 항목에 답하는 명령을 남길지 걷을지.** 신규가 만들지 않는다는 것은 이미 계약이다.
   #7 D4 가 데이터 전환을 면제했으므로 과거 행은 남고, **읽기 경로 코드를 지우지 않는다.**
   답하는 명령의 존치는 Phase 6 에서 정한다 — 사용자 결정이 아니다.
3. **「관리자」가 두 뜻으로 쓰인다.** 업무 취소 권한의 관리자와 조직 단면으로 들어온 읽기 전용
   관리자가 다른 사람이다. 원문도 같은 긴장을 갖는다(재검수 리포트 참고 항목).
   **W1 에는 취소가 없어 이번 구현을 막지 않지만**, 권한 판정을 세울 때 두 낱말을 갈라 적는다.
4. **수평 요청의 기존 조정·재상신 기능을 어떻게 하나.** 신규 요청이 즉시 배정으로 가면
   조정 회차가 생기지 않는다. 기존 기능 코드를 지울지 남길지는 Phase 4 에서 정한다 —
   **기존 데이터는 지우지 않고 기존 코드를 무단으로 지우지 않는다.**

> **닫힌 것** — 수평 요청 허용 판정(후보에서 `work_request.decide` 한 줄을 걷는다, Phase 3) ·
> integration 실행 환경(`make postgres-up` + 전용 `ax_test_w1` 생성, § Execution) ·
> **요청 출처 상태값 `assigned`**(DEC-001 D-3c) · **MCP 키는 명시 인자, 서버 fallback 없음**(§ 멱등 키).
> 넷 다 더는 열린 질문이 아니다. FE 라벨 문구만 Phase 7 의 일이다.

## Related

- SPEC: frontmatter `links.specs` 참조
- Work: 없음 — 이 work 가 첫 실행 단위다
