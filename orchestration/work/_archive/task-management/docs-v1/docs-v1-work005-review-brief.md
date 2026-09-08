# [reviewer] WORK-005 검수 — 상태 전이·완료 게이트·리스트/칸반 Phase 1~4

너는 **task-management `reviewer` 워커**다. **read-only.** 먼저 역할 문서를 읽어라 (**문서 레포 절대경로**):

- `/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/orchestration/roles/task-management/reviewer/role.md`

작업 워크트리: `/Users/kknaks/orca/workspaces/task_management/docs-v1`
base 브랜치: `origin/main`

**완료 게이트가 이 제품의 규칙이다.** 여기가 새면 회의록(WORK-008)이 그 구멍으로 들어온다.

## 1. 검수 대상

**WORK-005 커밋만** 본다 (WORK-001~004 는 이미 검수했다). `c6ba429` **다음부터 HEAD 까지**:

- `46fe87a` — **Phase 1·2**(backend): 상태 전이·완료 게이트·실행취소·소프트 딜리트·목록/집계 + **마이그레이션 `0003`**
- 그 뒤 커밋 — **Phase 3·4**(frontend): 리스트 뷰·상태 팝오버·컨텍스트 메뉴·취소/삭제 모달·완료 토스트·칸반·DnD

범위 산정: `git diff c6ba429...HEAD --stat` + `git log c6ba429..HEAD`.
**작업 트리는 clean 하다** — 커밋된 것이 전부다.

## 2. SSOT — 판정 기준 (전부 문서 레포, **읽기 전용**)

경로 기준: `/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/para/projects/summer-star/task-management/`

| 층 | 문서 |
|---|---|
| **정책** | `10-decision/decision-002-tasks.md` — 완료 게이트 · **취소는 상태** · DnD · 소프트 딜리트 |
| **아키텍처** | `40-architecture/backend/README.md`(**§8-2 코드 표** · §7 · §10 · §12) · `frontend/README.md`(§1-2 · §3-3 · **§5-2 Ink** · §11) · `database/domains/task.md`(**T-8-a·T-8-b 신설**) |
| **SPEC** | `20-spec/spec-004-tasks-status-views.md` — §4 API·Case Matrix · **§5 낙관적 표** · **§6 Acceptance 18항목** |
| **WP** | `30-work/work-005-tasks-status-views.md` — Phase 1~4 + **§Internal Interface Contract** + **§Done Criteria** |

**판정은 문서 기준이다.** 취향으로 지적하지 마라.

## 3. 이 검수에서 특히 볼 것

### 게이트가 한 곳인가 — 이 검수의 핵심

- **`task.status` 에 값을 대입하는 코드가 몇 곳인가.** 백엔드 워커는 「ORM 대입은 `update_status()` 한 곳,
  호출자는 판정을 지난 두 경로(`change_status`·`undo`)뿐」이라고 보고했다 — **직접 grep 해서 확인해라**
- **`TaskCompletionBlockedError` 를 던지는 곳이 1곳**인가
- **`PATCH /api/tasks/{id}/status` 를 호출하는 프론트 코드가 `useTaskStatus.ts` 하나**인가.
  **세 진입점이 같은 경로·같은 본문을 낸다는 캡처 3장이 완료 증거에 있는가**(Done Criteria)
- **일반 `PATCH` 로 상태를 보내면 422** 인가 — 스키마 층에서 막히는가(§10)
- **`task_log` 를 DELETE 하는 곳이 실행취소 하나**인가(T-8-b)

### 실행취소

- 조건 셋(마지막 로그가 전이 · 그 뒤 다른 변경 없음 · **4초**)이 전부 있는가
- **직전 상태 복원 + 그 로그 삭제가 한 트랜잭션**인가
- **게이트를 다시 태우지 않는가**(완료에서 되돌리는 건 게이트와 무관하다)
- 백엔드가 **실제로 5초를 기다려** 409 를 확인했다고 보고했다 — 테스트가 시간을 목으로 때우고 있지 않은지 보라

### 마이그레이션 `0003` — WP 를 벗어난 추가다

**WP 는 「스키마 변경이 없다」였는데 리비전이 하나 생겼다.** 코디가 근거를 검토해 승인하고 ERD 에
T-8-a·T-8-b 로 반영했다(2026-09-06). **네가 볼 것은 「승인 여부」가 아니라 「구현이 그 근거대로인가」**다:

- 전이 로그**만** `from_status`·`to_status` 를 갖고 나머지는 둘 다 `NULL` 인가 — **CHECK 로 강제되는가**
- 기존 리비전을 고치지 않고 새 리비전으로 올렸는가. **downgrade 가 되는가**
- `cancelledAt` 이 **취소 전이 로그 시각에서 파생**되는가(`task` 에 별도 컬럼을 만들지 않았는가 —
  만들었으면 로그와 어긋날 수 있는 두 번째 사실이 생긴다)

### 낙관적 갱신의 방향이 **반대**인지

WORK-004 는 세 자리(할일 체크·메모·인라인 텍스트)를 **낙관적으로** 만들었다.
**이 work 는 정반대다** — 상태 전이는 게이트·전이 그래프가 **거부할 수 있어** 낙관적으로 하지 않는다(§5).

- 칸반이 **놓은 뒤 응답까지 로딩(불투명도 0.6)** 을 유지하는가. 먼저 옮겨 놓고 실패 시 되돌리지 않는가
- **드롭 차단 vs 서버 판정** — 전이 그래프로 막히는 컬럼은 **드롭을 막고**,
  **완료 컬럼은 드롭을 허용하고 서버가 판정**하는가. 결과자료 유무를 **화면이 미리 판단해 막으면 서버와 어긋난다**
- **같은 컬럼에 다시 놓으면 요청이 0건**인가(서버는 같은 상태에 409 를 낸다 — 요청을 내면 사용자가
  아무것도 안 했는데 에러 토스트를 본다)

### 목록·집계

- **`typeCounts` 가 유형 탭 자신을 반영하지 않고** 상태·프로젝트 필터는 반영하는가
- **0건 유형은 응답에 행이 없다** — **화면이 0 을 그리는가**(탭을 감추면 안 된다)
- 기한 없는 업무가 `due_asc` 에서 **맨 아래**인가(NULLS LAST)
- **`EXPLAIN` 에 `schedule` 이 없는가** — 완료 증거의 출력을 확인해라(BE §12 5-a)
- 「지연」이 **저장되지 않고 조회 시 파생**되는가(T-4). **화면이 다시 계산하지 않는가**
- 소프트 딜리트된 업무가 목록에 없고 **DB 에는 자식까지 남는가**(T-11)

### 규약 일반

- 계층 · `schema`/`dto` 분리 · `commit()` 부재 · **`except Exception` 부재** · `persist_changes` 남용 부재
- **쿼리 파라미터에 `Query(alias=...)`** — 이번엔 필터가 6개 이상이다(§3 규칙 7).
  빠지면 **조용히 무시되고 200** 이 난다. 각 파라미터가 **실제로 먹는지** 확인된 증거가 있는가
- 정적 빌드 제약: 동적 세그먼트 0 · 모든 `page` 에 `'use client'` · 컴포넌트 hex 0
- **화면당 `--tm-ink` 는 유형 탭 하나** — **뷰 토글이 Ink 를 쓰지 않는가**(FE §5-2)
- 조건이 전부 `?` 에 남는가. **뷰를 바꿔도 기간·유형이 유지되고 새로고침해도 그대로**인가
- 거부 토스트의 「결과 입력」이 **WORK-004 가 내보낸 `useCompletionCardFocus()`** 를 부르는가 —
  **새로 만들었으면 규격이 둘이 된 것이다**

## 4. 알려진 미결 — 여기에 시간을 쓰지 마라

1. **취소를 되돌리면 사유가 복원되지 않는다** — T-7 CHECK 때문에 취소를 떠날 때 비운다.
   백엔드가 보고했고 **취소는 마지막 로그가 「취소 사유 기록」이라 애초에 undo 대상이 아니다.** 결함이 아니다
2. **`overdueDays` 는 목록 응답에만 있다** — SPEC-003 상세 계약에 없어 상세는 그대로 뒀다. **문서 공백으로 분류해라**
3. dev DB 에 검증용 데이터가 남아 있다(`WORK005 …`·`검수수정 …`·`scope-검증 …` 접두사). **결함이 아니다**

## 5. 산출물

`/Users/kknaks/orca/workspaces/kknaks_profile/task-management-app/orchestration/work/docs-v1/work-005-review-report.md` 에 쓴다.

- **네 층(정책·아키텍처·SPEC·WP) 각각 PASS/WARN/FAIL** 판정
- **FAIL 은 파일:줄 + 무엇이 어긋났는지 + 고치는 방향**까지. 재현 가능한 것은 재현 방법도
- **문서 공백**은 **따로 분리**해라 — 코디가 닫는다
- **SPEC-004 §6 Acceptance 18항목**과 **WP §Done Criteria** 를 **하나씩 대조**해 어느 것이 확인됐고 어느 것이 안 됐는지 적어라
- 판정 못 한 것은 **「확인 못 함」으로 적어라.** 추측으로 PASS 주지 마라

**read-only 다 — 코드도 문서도 고치지 마라. 커밋하지 마라.**

## 6. 완료 보고 — **문구 변경 금지**

> **⚠ 핸들은 dispatch preamble 의 값을 믿어라.** preamble 의 코디네이터 핸들과 아래 값이 다르면 **preamble 이 맞다.**

```bash
orca orchestration send \
  --to term_6a4ac855-2a13-4484-b808-4c25182cbb2b --from <네 워커handle> \
  --type worker_done \
  --task-id <이 태스크의 taskId> --dispatch-id <이 태스크의 dispatchId> \
  --subject "reviewer 완료: WORK-005 검수 — FAIL n · WARN n · 공백 n" \
  --body "층별 판정 / FAIL 목록 / WARN 목록 / 문서 공백 / Acceptance 18항목 대조 / 확인 못 한 것"

orca terminal send --terminal term_6a4ac855-2a13-4484-b808-4c25182cbb2b \
  --text "[worker_done] reviewer 완료 — WORK-005 검수 FAIL n · WARN n · 공백 n. 상세는 인박스." --enter
```

- 막히면 **`orca orchestration ask` 를 쓰지 말고** 같은 방식으로 물어라:
  `orca terminal send --terminal term_6a4ac855-2a13-4484-b808-4c25182cbb2b --text "[질문] reviewer: <질문>" --enter`
