# WORK-002 검수 최소정정 1회차 — 보고 (2026-09-17)

대상 한 파일: `para/projects/summer-star/strong-hajin/30-work/work-002-task-lifecycle-v2.md`
(1001줄 → 1148줄). **SPEC·BASE·DEC·index·log·코드·디자인 변경 0건. 실행 0건**(테스트·DB·빌드 없음).
**모든 Phase 가 `Status: TODO` · 「완료 증거: 미작성」 아홉 그대로**이고 `status: todo` · `progress: 0` 도 그대로다.

## 막는 결함 다섯 — 전후

### F-1 `derived` 생산 줄 신설
- **전**: `derived.*`·`overdue_days` 를 Dependency·I-1·Phase 7·UX 추적에서 **소비만** 했다. 내는 줄이 없었다.
- **후**: Phase 2 작업에 **투영 신설 한 줄**(`_view()` · `_list()` · `_hierarchy_view`/`_related_view` ·
  `task_results.py`) + **키·생산 단계 한 줄** + **FE 타입 동시 정합 한 줄**, Phase 2 검증에 한 줄,
  Phase 4 의 `child_progress`/`blocking_children` 을 **같은 묶음에** 싣도록 한 줄 보강.
- **SPEC 실제 Data Contract 를 누락 없이 옮겼다** — `assignment`·`approval`·`proposal`·`blocking_children`·
  **`reply`·`status_note`**·`overdue_days` 일곱 전부. 생산 단계를 못 박았다:
  Phase 2 = `assignment`·`overdue_days` / Phase 4 = `blocking_children`·`child_progress` /
  Phase 5 = `approval`·`proposal` / **`reply`·`status_note` 는 원장(문의·회신 대기·상태 메모)이
  코드에 0건이라 이 work 가 값을 만들지 않고 키만 두고 `null` 고정** — SPEC-001 문의·메모 구현(후속)의 몫.
  (근거: BE 에 `derived`·`overdue_days`·`status_note`·`inquir`·`reminder` grep 0건. 읽기만 했다.)

### F-2 `open → done` 명시 구현 · A9 우회 제거
- **전**: 환류 후보 2(「한 줄 판정을 받는다」) + Open Issues 의 「A9 를 `in_progress` 경유로 쓰면 막히지 않는다」.
- **후**: **환류 후보 2 행 삭제.** Phase 5 작업에 `_ALLOWED_TRANSITIONS[OPEN] += DONE`(`lifecycle.py:67`),
  **요청 Task 거부 가드(`:82-83`)와 하위 완결 검사(`:84-86`) 보존**, `started_at` 은 빈 채로.
  Phase 5 검증에 **`open`·`in_progress` 두 경로 각각 A9** + **요청 Task 직접 완료 거부 회귀**.
  Phase 7-C 에 **상세 상단 `[시작]`+`[완료]` 동시 노출**(행 액션은 `[시작]`만).
  A9 추적 행의 「환류 후보 2 주의」를 「두 경로 각각」으로 교체. Open Issues 에서 우회 문장 삭제.
  **사용자 판정 요청은 남기지 않았다.**

### F-3 내부 enum 유지 + 외부 투영 매핑
- **전**: 환류 후보 1 이 (b)「표면 값이 `completion_submitted` 임을 인정」을 밀었고, 완결 판정이 **state 값 둘**을 읽는 흡수안.
- **후**: **환류 후보 1 행 삭제.** Phase 5 작업 다섯 줄 —
  ① 내부 `COMPLETION_SUBMITTED` 유지, 투영만 `state="done"`+`derived.approval="awaiting_review"`
  (승인 가드 `:556-558`·제출 가드 `:536` 은 내부 값을 읽으므로 손대지 않는다) ·
  ② **완결·권한 판정을 투영 묶음(`state` 문자열·`derived.*`)에서 읽지 않는다 — 내부 원장에서 판정** ·
  ③ **요청 Task 완결 = 「지금 완료 회차에 유효한 `accept` 판단 행」** — **아무 과거 승인 하나로 충분하지 않다.**
  보완으로 회차가 올랐거나 `reopen` 이 있었으면 그 이전 승인은 무효이고, **승인이 없으면 확실히 미완결**로 판정 ·
  ④ **FE 소비 동시 정합**(`viewModels.ts:110`·`labels.ts:7,16`·`MyWorkPage.tsx:85,757`·`WorkViews.tsx:475`·
  `WorkModals.tsx:635` 에서 `completion_submitted` 제거, 「완료 확인 대기」는 `derived.approval`).
  검증에 **전 표면 `completion_submitted` 0건** + **보완/재개 후 이전 승인이 남아도 미완결** 역검증 추가.

### F-4 회의 일정 — SPEC 범위로 되돌림
- **전**: Phase 7-D 「이번 판에서 싣는다」 · 환류 아닌 것 목록에 포함 · M-23 행 「이번에 싣는다」 ·
  「이번 인수조건이 아닌 것」에서 **「회의 일정」이 빠져 있었다**.
- **후**: 7-D 를 「**업무 기한만 싣는다 — 회의 일정은 이번에 싣지 않는다**」로. **기술 가능성은 기록으로**
  (`GET /api/meetings` 실재 = 새 BE 계약 불필요) 남기되 **범위 승인과 다른 축**임을 명시.
  환류 아닌 것 목록에서 제거하고 「SPEC 이 이번 범위에서 뺐다」로 대체. M-23 행을 「둘 다 안 그린다 /
  회의 일정은 BE 계약 불필요만 기록 · 싣는 것은 **후속 계약**」으로. §6 인용에 **「회의 일정」 복원**.
  **원문 시안의 남은 요구를 후속 계약으로 명시**하고 「확정 시안 전체 완료로 읽지 않는다」를 Scope·인수조건 양쪽에 박았다.

### F-5 인덱스 — 재현·재적용·회복이 서는 단일 기술안
- **전**: Rollout ③ 「CREATE INDEX CONCURRENTLY, 사람이 실행」 한 줄. DDL 없음 · 격리 재현 없음 ·
  중복 미검사 · INVALID 회복 없음.
- **후**: **파일 둘로 분리**(리뷰 제안의 「한 파일에 두 판을 나란히」 함정을 피했다 — 통째로 돌리면
  중복 생성이거나 `CONCURRENTLY` 가 트랜잭션 안에서 죽는다):
  - `backend/migrations/manual/2026-09-17-w2-indexes.sql` — **격리 검증용**, `CREATE INDEX IF NOT EXISTS`
  - `…-w2-indexes.concurrent.sql` — **운영 적용용**, `CREATE INDEX CONCURRENTLY IF NOT EXISTS`, autocommit
  정의는 두 파일에서 같고 머리에 용도를 적는다. **Phase 1 이 만든다 — 「이미 있다」고 쓰지 않았다.**
  **alembic·migrations 체계가 없다는 사실을 다시 못 박고 「migration 체계를 세웠다」 금지**를 넣었다.
  Phase 0 에 **부분 유일 인덱스 중복 SELECT**(존재 여부만 세지 않는다. 0건 아니면 사용자에게).
  Phase 1 검증에 **결손 인위 재현**(DROP → `--sync` 해도 안 생김 확인 → `.sql` 적용 → `pg_indexes` 재확인 →
  **재적용해도 실패 없음**) + **INVALID(`indisvalid=false`) 회복 절차**.
  Rollout ③ 를 **③-a 격리 검증(에이전트) / ③-b 운영 적용(사람)** 으로 갈랐고 Pre-deploy·Rollback 도 맞췄다.

## 비차단 여섯

| # | 전 → 후 |
|---|---|
| N-1 | `TaskTable`(6열) → **기존 `.scax-task-table--nostar` 5열 유지**(시안 6열에서 별표만 빠진다 · M-21 · `MyWorkPage.tsx:593-601`·`components.css:401-405` 의 결정과 이유 인용) · 「별표 열을 되살리지 않는다」 |
| N-2 | **SPEC 의 U 번호는 그대로 둔다.** 이 work 안의 참조만 `UX-U1`~`UX-U15`(SPEC-003 §6) / `BASE U-1`~`U-7`(BASE-002) 로 갈랐다 — UX 추적 표 15행·표 머리·Phase 7 검증·검증 경계 문장, 그리고 BASE 쪽 U-1·U-2·U-4·U-5·U-6 참조 전부. 라벨 주의 문단을 표 앞에 넣었다 |
| N-3 | 「W1 유지 회귀 **5종**」 3곳 → **7종(K-1~K-6·K-11)** (Phase 8 작업 · 절 머리 · Done Criteria) |
| N-4 | 「`manual` 목록이 비어 있다」 3곳 → **「이번에 더한 컬럼·표가 `manual` 에 없다」**(`plan()` 이 모델에 없는 기존 컬럼도 `manual` 에 넣는다 · `schema_sync.py:44-45`) |
| N-5 | Phase 4 에 **EU-6·EU-7 미정 한 줄** — 수락 전 자료 접근·재분해 알림을 **넓히지도 막지도 않는다(현행 보존)**. 합치는 대상은 기존 두 답의 불일치뿐 |
| N-6 | 환류 후보 3(수신 시각) 행 삭제 → **M-22 후속**으로. 근거 정정(「값이 없다」가 아니라 **「계약에 싣지 않았다」**)을 M-22 행과 7-D 줄에 옮겼다 |

**N-7(index/log 표 깨짐)은 손대지 않았다** — 코디네이터 몫이고 allowed_paths 밖이다.

## 사용자 미답 둘

- **OQ-203**: 제출을 여는 것은 **현행 보존**이고 **새 선택의 확정이 아니다**로 바꿨다(착수 표 · Phase 5 · Open Issues 셋).
  **답 전에 정책 확정으로 표시 금지**(문구·주석·테스트 이름 포함)를 명시하고 **조건별 검증 계획**을 남겼다 —
  「막지 않는다」면 현 계획대로(승인에서 막힘 · A7), 「막는다」면 `submit_completion()` 검사 한 줄 +
  `WORK_CHILDREN_UNFINISHED` 회귀 한 줄 + §6 한 줄. 바뀌는 자리는 그 둘뿐이다.
- **OQ-206**: **의존을 좁게** 적었다(「요청자가 `system:meeting` 인 요청 Task 의 완료 승인을 누가 부르는가」 하나).
  **seed 에서 승격 경로를 빼서 감추지 않는다** — 그대로 두고 **「미답으로 막히는 경로 · 미검증」**을
  seed 주석과 Phase 8 인계 문서에 적게 했다(Phase 6 한 줄). 미정 밖 독립 범위는 그대로 완성돼 있다.

## Phase 0 기준선 — 코디 실행 증거로 정정 (2회차)

처음에는 W1(2026-09-16) 증거 재사용으로 4종 전량 반복을 없앴는데, **코디네이터가 현재 코드에서
4종을 직접 돌려 전부 green** 이었다. 그 사실에 맞춰 다시 고쳤다.

- **계획 원문의 4종을 그대로 유지**한다 — `make test-unit` · `make test-contract` ·
  `make frontend-test` · `make test-postgres`.
- 그 옆에 **이미 실행된 현재 코드의 수치**를 완료 증거 참조로 달았다 —
  **322 / 976 / 645 / 65 passed · 넷 다 exit 0**(Node 20.20.0 ·
  `PYTEST_XDIST_AUTO_NUM_WORKERS=4` · 격리 `localhost:54329/ax_test`).
  증거는 `v2-phase0-verification.md` 와 `v2-phase0-{test-unit,test-contract,frontend-test,test-postgres}`
  의 `.log`/`.exit`. **baseline 82 파일 sha 가 일치하는 동안만 유효**하고 어긋나면 다시 돌린다.
- **W1 의 1289/2-failed 수치는 더 이상 기준선이 아니다** — 과거 W1 수치가 아니라 **현재 코드의 수치**다.
- **Phase 0 는 여전히 `Status: TODO` · 「완료 증거: 미작성」이다.** 증거는 이 보고서와 계획 본문의
  참조로만 있고, **체크박스를 채우거나 phase 를 DONE 으로 올리지 않았다.**
- **기준선 ≠ v2 통과** — Phase 1~8 수치는 전부 이번 판 새 실행이어야 한다(P-7).
  **`ax_demo` 가 빈 DB 이므로 데이터 이관 검사를 했다고 쓰지 않는다**는 한 줄도 함께 넣었다.
- Phase 0 검증 줄은 「변경 전 4종의 수치와 exit 코드가 로그와 함께 남아 있다 · 그 수치를 v2 통과로
  쓰지 않는다」로 맞췄다.

## 남은 것 · 주의

- **N-7**(`30-work/README.md` Status Board·Work List 표 끊김 · `Type` 이 `spec-up` 인데 frontmatter 는
  `new-feature` · Blocker 불일치) — 코디네이터.
- 이 문서는 여전히 **착수 전 초안**이다. 정정은 전부 **문구·phase 배치·추적 정합**이고 실행 증거가 아니다.
