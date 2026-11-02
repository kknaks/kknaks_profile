# strong-hajin-work v2 통합 구현 계획(WORK-002) 결과 보고

## 상태: done

작성한 것은 **WORK-002 문서 하나**다. **코드는 한 줄도 쓰지 않았고, 테스트·DB 조회·빌드도 0건**이다.
아래 「코드에서 확인한 것」은 전부 **읽기만 한 결과**다.

## 수행 내용

### 변경 파일 — 둘

| 경로 | 무엇 |
|---|---|
| `para/projects/summer-star/strong-hajin/30-work/work-002-task-lifecycle-v2.md` | **신규.** WORK-002 (1001줄) |
| `orchestration/work/strong-hajin-work/v2-work-plan-report.md` | **신규.** 이 보고서 |

그 밖에 아무것도 고치지 않았다 — SPEC·BASE·DEC·index·log·reference·코드·디자인 전부 그대로다.
커밋·push·PR·DB·테스트·빌드·새 워커 발주 없음.

### 문서 구조

`templates/projects/30-work/work.md` 양식 그대로. `status: todo` · `progress: 0` ·
**Phase 0~8 아홉 개가 전부 `TODO`**. `links` 는 BASE-002 · DEC-002 · SPEC-003/001/002 · WORK-001.

Phase 는 작업계획서 v2 §4 의 단계 0~7 을 이 레포에 구체화하고 FE 를 하나 더 세웠다 —
0 기준선·읽기 전용 점검 / 1 관계·스키마·migration / 2 요청 발송·수락·거절·협의·철회·재요청 /
3 담당 변경 / 4 재귀 하위·권한·자료 / 5 완료·승인·취소 합의·재개 / 6 REST·MCP·AX·회의·seed·인벤토리 /
7 FE 시안 + v2 흐름 / 8 자동 통합 회귀와 사용자 E2E 인계.

## 코드에서 직접 확인한 근거 — 계획이 서 있는 자리

브리프가 준 목록을 믿지 않고 **직접 grep·읽기로 셌다.** 계획을 바꾼 것들만 적는다.

### 1. 하위 관계와 담당 교체는 스키마가 거의 이미 있다

- `tasks.parent_task_id` 가 **이미 있고 인덱스도 있다** (`platform/persistence.py:937`).
  재귀 저장은 **스키마 변경이 아니라 애플리케이션 제한 제거**(O-6)다.
- `task_assignments` 에 `status`·`accepted_at`·`declined_at`·`superseded_at`·`decline_reason`·
  `supersedes_assignment_id` 가 **이미 있다** (`:1578-1594`). 담당 변경 v2 는 **행동 변경**이다.
- 새로 필요한 것은 **nullable 컬럼 다섯 + 새 표 둘**뿐이고, 전부 additive 로 닫힌다.

### 2. 읽기 권한이 **이미 두 갈래로 갈려 있다** — 이것이 Phase 4 의 핵심

- `TaskApplication._may_read()` 는 `get()` 을 불러 **`_related_view` 성공까지 True** 로 친다
  (`modules/work/application.py:453-458`). 요청자는 상세를 연다.
- 그런데 자료가 쓰는 `may_read_task()` 는 **`readable_task_ids()`(= `_list()`)** 로 답하고
  (`bootstrap/application.py:653-659`), **`_list()` 에는 요청 관계 길이 아예 없다**
  (`application.py:303-349` — 보유 + 조직 범위 + 프로젝트 범위 셋뿐).
- **그래서 지금도 「요청자가 상세는 여는데 그 업무의 자료는 못 연다」가 성립한다.**
  DEC-002 C-10 이 경고한 자리가 **이미 현실**이다.
- 다행히 **자료 표면이 한 곳으로 모인다**: 목록·본문/다운로드(`materials.open`)·검색
  (`bootstrap/material_sources.py:sources()`)·미리보기가 **전부 `readable_tasks()`/`may_read_task()`** 를
  지난다. **한 자리를 고치면 네 표면이 함께 열린다** — U-5 의 전수를 문서 § 입구 전수에 표로 실었다.

### 3. `POST /api/tasks` 는 입구를 건드릴 필요가 없다

`decide_task_creation()`(`modules/work/creation.py:59-87`)이 타인 지정을 `horizontal` 로 갈라
`WorkRequestApplication.create()` 를 부른다. `_refuse_unsupported_horizontal_fields`
(`creation_commands.py:157-173`)가 `start_date`·`parent_task_id`·`project_id` 를 거절한다.
**v2 가 바꾸는 것은 그 요청의 응답 단계뿐**이라는 SPEC 판단이 코드와 맞는다.

### 4. 완료 축 — 「승인 차단」은 이미 있고, 새로 닫는 것은 완결 판정 하나

- `submit_completion()`(`application.py:517-552`)에 **하위 검사가 없다**.
- `accept_delivery()`(`:556-562`)에 **`_require_children_finished()` 가 이미 걸려 있다**(`:558`).
- `open_children_of()`(`platform/work_tasks.py:473-475`)가 **`state` 만 본다** → **O-20 이 새로 닫는 자리**.
- SPEC-003 의 「승인에서 막는다를 신규 구현으로 적지 않는다」가 코드와 맞는다.

### 5. migration 도구의 실제 한계 — 있다고 쓰지 않았다

- **alembic 도 migrations 디렉토리도 없다** (레포 전체 검색 0건).
- `make sync-demo-schema` → `schema_sync.apply()` 는 **없는 표를 만들고(인덱스 포함) 없는 컬럼을 더한다.**
  **기존 표에 인덱스를 더하는 경로가 없고 `manual` 에도 올리지 않는다**(O-24) —
  **조용히 지나간다.**
- `NOT NULL` + `server_default` 없음이면 실행하지 않고 사람에게 올린다(O-25).
- `make reset-demo` 는 `ax_demo`/`ax_test*` 이름과 로컬 호스트로 **guard 되어 있다**.
- **그래서 기술안은 하나로 적었다** — 「additive 모델 변경 + `--sync` + **기존 표 인덱스는
  `CREATE INDEX CONCURRENTLY` 로 사람이**」, rollout 6단계, rollback 은 **컬럼·표를 되돌리지 않는 것이 기본**.
- **여기서 새로 찾은 선행 항목 하나**: W1 이 `tasks`(기존 표)에 부분 유일 인덱스
  `uq_tasks_source_work_request` 를 더했는데(`persistence.py:900-908`), **`schema_sync` 는 그것을
  만들지 못한다.** 실행 DB 에 그 인덱스가 실재하는지 **Phase 0 에서 반드시 본다**고 적었다.

### 6. 시안은 분석 보고서가 아니라 **코드 트리를 직접 읽었다**

`.design-sync/screens/` **12파일 전수**를 열었다 — `MyWork.html` · `styles.css` ·
`_ds_bundle.css` · `_ds_bundle.js` · `fonts/fonts.css` · `handoff/my-work/{css/components.css,
js/data.js, js/my-work.v2.jsx}` · `handoff/shared/js/work-data.js` ·
`handoff/shell/js/{nav.js, scax-ui.jsx, work-modal.jsx}`.

직접 확인한 사실:

- **시안 모달에 담당자 지정 자리가 없다** — 필드 여섯(업무 명·기한·내용·확인받을 사람·
  체크리스트·첨부파일)이 전부다(`work-modal.jsx:194-249`). SPEC §2.7 의 「미설계」가 맞다.
- **시안 화면 파일은 `MyWork.html` 하나**다. `nav.js` 가 가리키는 `Calendar.html`·
  `MeetingWorkspace.html` 은 **그 디렉토리에 없다**.
- **`StateSwitch` 는 시안 스스로 dev 전용**이라 적었다 → 제품 제외.
- 표 세 벌·칩 세 벌·수신함 카드·캘린더 3범위의 실제 열·값·단추를 확인해 FE 작업으로 옮겼다.

### 7. 「부재」를 추정하지 않고 **읽어서 갈랐다** — M-20~M-24 와 수신함 항목

| 요구 | 실제 | 이번 판 |
|---|---|---|
| **회의 일정을 캘린더에** | **기술적으로 해소된다.** `GET /api/meetings` 가 `MeetingRow{title, starts_at, ends_at, location, status}` 를 **이미 낸다**(`viewModels.ts:843-854`) | **싣는다.** 새 계약 불필요 |
| **수신함 카드 수신 시각** | **데이터는 있다** — `DecisionItemRecord/ActionItemRecord.created_at` 이 정렬에 쓰이고 회차가 `submitted_at` 으로 낸다. **봉투(`ActionItemEnvelope`)에 없을 뿐** | **SPEC 환류 후보**로 올림. 닫히기 전엔 안 그림 |
| **별표** | `starred` 가 **백엔드·프론트 어디에도 없다**(grep 0건) | 안 그림 |
| **근무 시간** | 개념이 **어디에도 없다**(grep 0건) | 안 그림 |
| **미읽음** | 판단 항목에 읽음 상태가 **없다**. `notifications.read_at` 은 **다른 도메인** | 안 그림 |
| **아바타** | 필드 없음 | 안 그림 |
| **수신함 「업무/참고」 분류 축** | 계약 축은 **종류 칩 둘**, 코드 축은 **상태 축** — **대응하지 않는다** | 현재 상태 축 유지. 새 계약 안 만듦 |
| **「답장」·「원문 확인하기」** | **계약이 없다** | 안 그림 — 없는 명령을 부르는 단추를 만들지 않는다 |

### 8. OQ-202(목록 정리)는 기존 BE 계약 안의 기술 UX 선택으로 구체안을 냈다

**「숨기기」 + 「숨긴 항목 보기」 토글.** 「삭제」는 로그가 남는 사실과 어긋나고,
「보관」은 새 보관함 화면을 요구한다. **사용자 질문으로 올리지 않았다.**

## SPEC 환류가 필요한 최소 부분 — 셋

| # | 무엇 | 왜 |
|---|---|---|
| **1** | **요청 Task 의 제출 직후 표면 상태값** | SPEC-003 §4·§6 은 「제출이 성공하면 밖으로는 `state=done` + `approval=awaiting_review`」인데 **코드는 `state=COMPLETION_SUBMITTED` 를 내고**(`application.py:546`) `accept_delivery()` 가 **그 상태여야만** 승인한다(`:556-558`). 같은 SPEC 이 그 enum 정리를 **W2 범위로 미뤘다.** 둘을 동시에 만족할 수 없다 |
| **2** | **`open → done` 전이** | SPEC-001 §4 State(`:602`)와 SPEC-003 §4 State 가 **둘 다 `open --> done` 을 그린다.** 코드 `_ALLOWED_TRANSITIONS` 는 `OPEN → {IN_PROGRESS, CANCELLED}` 뿐(`lifecycle.py:64-70`). **A9** 에서 상위가 `open` 이면 계약대로면 되고 코드대로면 안 된다. **v2 가 만든 어긋남이 아니라 W1 에서 넘어온 것** |
| **3** | **판단 항목 봉투의 수신 시각** | 위 7번. 「값이 없다」가 아니라 **「계약에 싣지 않았다」**. M-22 의 근거를 그렇게 정정해야 한다 |

**둘 다 착수를 막지는 않는다.** 1 은 완결 판정 함수가 두 값을 다 읽게 쓰면 어느 답이든 흡수되고,
2 는 A9 테스트가 `in_progress` 를 거쳐 완료하게 쓰면 판정 전까지 막히지 않는다 — 문서에 그렇게 적었다.

## 남은 사용자 질문의 영향

| 질문 | 막는 범위 | 이 계획의 처분 |
|---|---|---|
| **OQ-203** — 완료 보고 제출도 하위로 막나 | **Phase 5 의 작업 한 줄 + §6 인수조건 한 줄** | **기본값 안 B(제출은 열고 승인에서 막는다)로 구현.** 뒤집히면 `submit_completion()` 에 검사 한 줄을 더한다. 본인·배정 업무는 어느 안이든 결과가 같다 |
| **OQ-206** — 승격 요청의 완료 확인자 | **승격 경로의 완료 승인 한 조각** | **구현 대상에서 뺐다.** 새 자동 승인을 만들지 않고 확인자를 임의로 바꾸지도 않는다. **일반 요청 축 A1~C2 는 전부 선다.** 승격 요청의 수정·재상신·철회는 **미정이 아니다**(O-31, 기존 동작 보존) |

## 검증 계획의 요지

- **BE 는 Makefile 타겟으로만.** `uv run pytest` 직접 호출 금지(AGENTS.md · P-6).
  Phase 별 적정 범위(`test-unit`/`test-contract`/`test-postgres`), **전량 `make verify` 는 Phase 8 한 번**.
- **FE 는 Node 20**(W1 검증에서 Node 25 가 `localStorage` 로 깨졌다) · `npx tsc --noEmit` 는 `frontend/` 에서.
- **자료 worker 3초 lease 시간 전제 부채는 제품 버그와 가른다.** W1 검증 기록(「높은 CPU 부하에서
  불안정 · 병렬 4 는 완화이지 해결이 아니다」)을 근거로 적었고, **skip·단언 약화 금지**를 명시했다.
- **W1 유지 회귀(K-1~K-6·K-11 + 배정 축 현행 둘)와 v2 새 계약 검증을 별도 표로 갈랐다.**
- **자동 검증은 에이전트, 브라우저 E2E 는 사용자.** **E2E 미실행을 통과라고 쓰지 않는다**를 명시했고,
  사용자 인계용 시나리오 **E-1~E-12(조작 + 눈으로 볼 기대 결과)** 를 문서에 실었다.
- 인벤토리는 **diff 난 항목만 패치**(전체 재작성 금지).

## 병행·통합 구조

- Phase 0·1 은 BE 단독. 그동안 FE 는 **글리프 9종 추가와 표 뼈대(목데이터)** 를 병행한다.
- **통합 단위 I-1~I-8** 을 표로 고정했다 — BE 가 내는 것과 FE 가 쓰는 것이 **같은 단위에서 닫힌다**.
- **I-3(멱등 키)** 를 따로 못 박았다: 서버 필수화와 FE 전송 시작이 갈리면 그 사이 화면이
  **전부 422** 이거나 **재시도가 새 업무**가 된다.
- 공유 파일은 **소유자를 한 칸에 하나만** 적었다(`api.ts`·`viewModels.ts`·`labels.ts` = FE,
  `unified-operations-inventory.json`·BE 테스트 = BE).

## 자체 점검

- [x] 템플릿 절 전부 존재(Meta·Work Summary·Role Assignment·Scope·Code Surface·Domain/Schema·
      Dependency·Internal Interface Contract·Execution·Pre-deploy Check·Rollback·Done Criteria·
      Open Issues·Related).
- [x] frontmatter YAML 파싱 성공. `status: todo` · `progress: 0` · `tags` 에 `status/todo`.
- [x] **Phase 0~8 아홉 개가 전부 `TODO`** — `**Status**:` 값의 집합이 `{TODO}` 하나.
- [x] `links` 의 다섯 문서가 **실재**한다(BASE-002·DEC-002·SPEC-003·SPEC-001·SPEC-002·WORK-001).
      Meta 의 서술과 `links` 가 일치한다.
- [x] **A1~C2 21건 전수**와 **U-1~U-15 전수**가 「닫는 Phase」와 함께 표로 추적된다.
- [x] SPEC 본문을 복사하지 않았다 — 절 이름으로만 가리킨다. **전체 스키마를 문서에 복사하지 않았다.**
- [x] 구현한 것처럼 표시한 곳이 없다. 문서 머리에 **「테스트·DB 조회 0건」**을 명시했다.

**린트**: `skills.md` 가 말하는 `python3 scripts/lint-pipeline.py --strict` 는 **이 레포에 없다**
(`scripts/` 디렉토리 자체가 없다 — 리뉴얼로 아직 안 올라온 것으로 보인다). 대신 있는 훅은
`rules/hooks/pre-commit`(개념 ↔ 맵 정합)이고 **개념 파일을 건드리지 않았으므로 해당 없다.**

## 미결·주의점

1. **SPEC 환류 3건**(위) — 1·2 는 착수 전에 한 줄 판정을 받는 것이 가장 싸다. 받지 못해도 진행된다.
2. **U-1(실행 스키마 미확인)** 이 그대로 남아 있다. Phase 0 의 읽기 전용 점검이 닫는다.
   **ORM = 실행 DB 를 전제한 설계는 인덱스·FK 에서 깨진다.**
3. **`uq_tasks_source_work_request` 인덱스가 실행 DB 에 없을 수 있다** — W1 이 기존 표에 더했고
   `schema_sync` 는 그것을 만들지 못한다. Phase 0 의 확인 항목으로 넣었다.
4. **U-6 점검(승인 판단 행 없이 `done` 인 요청 하위)** 은 Phase 0 의 읽기 전용 SELECT 다.
   **0건이 아니면 그때 사용자에게 올린다** — 그 전에는 사용자 질문이 아니다.
5. **W1 미커밋 변경이 계속 움직인다**(U-4). 착수 시 `v2-code-baseline/manifest.json` 의 sha256 과
   대조하고, 다르면 그 파일을 먼저 보고하도록 Phase 0 에 넣었다.
6. **화면 기본값 넷은 뒤집힐 수 있다** — 「참조된 업무·조직 업무」의 자리(M-20) · 칩 바 오른쪽 끝(M-24) ·
   「다시 요청 = 재요청」 · 목록 정리 = 「숨기기」. 전부 **뒤집히면 그 자리만 바뀌게** 적었다.
7. **리뷰어 검수는 코디네이터가 후속 발주**한다. 이 보고서는 검수를 대신하지 않는다.
