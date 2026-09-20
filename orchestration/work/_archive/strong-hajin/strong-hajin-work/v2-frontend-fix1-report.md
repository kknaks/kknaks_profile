# WORK-002 v2 frontend — 검수 정정 1차 결과

- 작성: `@sc-ax-fe` (task `task_a1e5068c1c80` · dispatch `ctx_686cf46a6cb3`)
- 입력: `review-v2-frontend-report.md` (F-1 · W-1 · W-3 · W-4 · W-5 · W-6) · SPEC-003 · WORK-002
- 워크트리 변경만. **커밋·push·PR 없음.** `backend/` · 문서 스펙 미접촉.

## 상태

| 항목 | 결과 |
|---|---|
| **F-1** (막는 것) | **닫았다** — 제안·직접취소·재개를 **서버의 자리 판정**과 맞췄고 네 경로 회귀를 더했다 |
| **W-1** | 닫았다 — 죽은 분기를 지우고 주석을 실제 동작으로 맞췄다 |
| **W-3** | 닫았다 — 첫 실패에서 경고가 나고, 성공한 일반 목록은 살아 있다 |
| **W-5** | 닫았다 — 회차 표를 원본 로그로 정정, 로그 없는 681 은 근거에서 뺐다 |
| **W-6** | 닫았다 — 82/82 가 착수 시점 값임을 본문에 명시 |
| **Phase 7-A 첨부** | **본인 업무 갈래만 구현.** 나머지 셋은 **기존 자료 쓰기 권한 계약 때문에 막혀 있다**(아래 §4). **첨부 기능 완료라고 주장하지 않는다** |

---

## 1. F-1 — 「내 자리」를 세션 역량으로 읽던 것을 서버 판정으로 바꿨다

### 무엇이 틀렸나

제안 두 단추의 게이트가 `canManage`(= `canManageOwnTasks`, **세션 역량**) + `requestTaskAccepted`
(요청 업무이고 담당이 섰다) 뿐이었다. **「이 업무에서 내가 누구인가」가 없었다.** 그래서 담당자 —
그 드로어의 가장 흔한 사용자 — 에게도 단추가 서고, 누르면 403 이다.

### `origin.actor` 로 고치지 않은 이유 (브리프의 대조 지시)

검수가 제안한 한 줄은 `task.origin?.actor?.member_id === personaId` 였다. **BE 실물을 열어 보니
그 값으로는 한 갈래가 틀린다.**

- 서버 판정은 `_is_request_owner`(`modules/work/application.py`)이고, 내용은
  **`principal.id ∈ {request.requester_id, request.promoted_by_member_id}`** 다
  (`modules/work/requests.py:797` 의 요청자 전용 조작 판정과 같은 모양 · BASE-002 O-31).
- 그런데 `_origin_projection` 이 `origin.actor` 자리에 싣는 값은 **`fact["request_requester_id"]`** 다.
  **회의 승격 요청은 `requester_id` 가 `system:meeting`** 이고 누른 사람은 `promoted_by_member_id`
  에만 있다. 즉 `origin.actor` 로 판정하면 **승격을 누른 본인이 자기 요청에서 빠진다.**
- 담당 여부로 요청자를 추정하지도 않았다 — 둘은 다른 자리다.

### 어떻게 고쳤나

`workRows.ts` 에 **서버와 같은 두 항을 읽는** 판정 하나를 두고, 요청 원장 행에서 답을 얻는다.

```ts
export function isRequestOwner(request, personaId) {
  if (!request || !personaId) return false;
  return request.requester_id === personaId || request.promoted_by_member_id === personaId;
}
```

- `MyWorkPage` 가 `lineage.source_work_request_id`(없으면 `origin.source.id`)로 **이미 읽어 둔
  요청 목록**에서 그 행을 찾아 `viewerIsRequester` 로 넘긴다. **새 조회를 열지 않았다** — 요청 행을
  읽을 권한은 업무와 다른 자리라, 드로어가 스스로 부르면 권한 밖에서 404 를 맞는다.
- 못 찾으면 `false` 다. 내가 요청자라면 그 요청은 내 목록에 있다(`getWorkRequests` 가 요청자·수신자·
  참조자 관계로 낸다). **모르면 없는 권한을 그리지 않는다.**
- `viewModels.WorkRequest` 에 `promoted_by_member_id`·`requester_kind`·`source_meeting_id` 를 더했다 —
  **BE 가 이미 내고 있던 값**이고(`requests.py:953` 의 `_view`) FE 타입에만 없었다.

### 함께 닫은 짝 — 직접 취소와 재개

같은 축이라 한 벌로 맞췄다. 근거는 전부 서버 코드다.

| 명령 | 서버가 여는 사람 | 근거 | 화면 |
|---|---|---|---|
| 취소 제안 · 조건 변경 제안 | **요청자**(또는 승격을 누른 사람) | `_is_request_owner` | `viewerIsRequester` |
| 직접 취소 · 시작 · 완료 · 막힘 | **활성 담당** | `transition()` → `repository.task(id, principal)` → `_held_by` | `viewerDrives` |
| 재개 | 요청 업무는 **요청자**, 본인·배정은 **담당자** | `_require_may_reopen` | `reviewed ? viewerIsRequester : viewerDrives` |

`viewerDrives` 는 **아무도 들지 않는 업무**(수락 전 요청 Task — 담당이 `null` 인 것이 그 모습이다)와
**남이 드는 업무**를 가른다. 검수가 짚은 「수락 전 요청 Task 에 수신자에게도 「업무 취소」가 선다」가
그 자리였고, 그것은 403 이 아니라 **404** 다(전이가 `_held_by` 로 가므로 드는 사람이 없으면 조회부터 실패).

**요청자 본인의 정상 기능은 보존했다** — 제안 둘, 재개, 응답 대기 제안의 철회가 그대로 선다.
담당자 쪽도 좁아진 것은 «요청자의 것» 뿐이고 완료 보고·시작·막힘·응답(동의/동의하지 않음)은 그대로다.

### 회귀 (`TaskLifecycleV2.test.tsx` · `workRows.test.ts`)

- 자리별: **요청자**(제안 둘 보임 · 직접취소 없음) · **담당자**(제안 없음 · 완료 보고는 있음) ·
  **제3자**(아무것도 없음) · **본인 업무**·**관리자 배정 업무**(직접취소 보임).
- **수락 전 요청 Task**: 수신자에게도 직접취소 없음.
- 재개: 승인 대기 → 없음 · 승인 완료 요청 업무 → **요청자만** · 본인 업무 → **드는 사람**.
- `personaId` 를 넘기지 않는 화면(오늘·캘린더)에서 **본인 업무 취소가 그대로 선다** — 모른다는 이유로
  있던 길을 닫지 않는다.
- `isRequestOwner`: 요청자 본인 ✓ · 담당자 ✗ · **승격은 누른 사람 ✓** · 행이나 보는 사람을 모르면 ✗.

## 2. W-1 — 죽어 있던 보수 분기를 지우고 주석을 동작에 맞췄다

`isChildSettled` 의 마지막 줄 `!("origin" in child && isRequestTask(child) && !child.derived)` 는
**`TaskChild` 에서 실행될 수 없었다** — 하위 투영에 `origin` 도 `lineage` 도 없다. 주석은 「승인 축을
모르는 요청 업무만 보수적으로 미완결」이라 약속했는데 코드는 언제나 완결로 셌다.

분기를 지우고 규칙을 **한 줄로** 만들었다 — **승인 값 하나만 읽는다.**
`awaiting_review`·`awaiting_revision` 이면 미완결, 그 밖(`approved`·`null`·부재)은 `done` 이면 완결.
**없는 값에서 요청 업무를 발명하지 않는다.**

안전한 이유를 주석에 적었다: **이 함수는 원장이 아니다.** 상위 완료를 막을지는 서버가 정하고
(`derived.blocking_children` · `child_progress` · 완료 명령의 409), 화면은 그 값을 **먼저** 쓴다
(`blockingChildrenOf`·`childProgressOf` 가 서버 값이 있으면 그대로 반환한다). 이 셈은 서버가 그 값을
주지 않았을 때의 **표시용**이다. 회귀도 그 뜻으로 다시 썼다.

## 3. W-3 — 첫 실패에서 말한다. 성공한 목록은 버리지 않는다

```
getWorkRequests(true)                      → 성공: 플래그 해제
  .catch(() => getWorkRequests()           → 일반 목록은 그대로 살린다
      .then(rows => { 플래그 = true; return rows })
      .catch(() => []))                    → 기존 부채(둘 다 실패)만 빈 목록
```

- **일반 목록이 성공한 «첫» 실패에서 경고가 난다** — 둘 다 실패해야 경고하는 형태가 아니다.
- 경고 문구: 「숨긴 항목까지 읽지 못했습니다 — 「숨긴 항목 보기」가 이 세션에만 적용됩니다.」
- **성공 한 번에 지워지지 않는다.** 명령이 끝나면 지금까지 `onError(null)` 로 배너를 비웠는데,
  그러면 이 경고가 수락 한 번에 사라진다. `settleError()` 를 두어 **아직 참인 경고는 남기고**
  그 밖에는 예전처럼 비운다(호출부 6곳).
- 회귀 둘: ① 일반 목록은 서 있고 경고가 난다 ② 그 뒤 요청 수락이 성공해도 경고가 남는다.

## 4. Phase 7-A 첨부 — 실물 확인 결과와 구현 범위

### 실물 확인 (구현 전에 BE 를 열어 보았다)

업무 자료 업로드는 `POST /api/tasks/{id}/materials` → `materials.attach` → `_upload_task` →
`work_tasks.task(task_id, principal)` 로 가고, **그 조회는 활성 담당에게만 연다**(`_held_by`).
그래서 갈래마다 답이 다르다.

| 생성 갈래 | 만든 직후 활성 담당 | 기존 API 로 붙나 |
|---|---|---|
| **본인 업무** (`POST /api/tasks`) | **나** | **된다** — 응답 `task_id` 로 두 단계 |
| 관리자 배정 (`POST /api/tasks/assign`) | 상대 | **안 된다** (404) |
| 요청 발송 (`POST /api/work-requests`, v2) | **아무도 없음**(수락 전) | **안 된다** (404) |
| 회의 승격 | 같음 | **안 된다** (404) |

인접한 유일한 경로는 `POST /api/work-requests/{id}/evidence` 인데 그것은 **Submission 의 «근거»
원장**이라 저장도 뜻도 다르다 — 모달의 「첨부파일」을 거기로 보내면 사용자가 붙인 파일이 **업무 자료에
없다.** 코디에 근거와 함께 물었고 **(A) 로 확정**받았다: 새 권한을 만들지도, evidence 로 바꾸지도 않는다.

### 구현한 것 (본인 업무 갈래)

- 시안의 여섯째 칸을 DS `DropZone` + `FileList` 로 세웠다(**둘 다 이미 있던 부품** — 신설 아님).
- **두 단계**: `createDirectTask` → 응답 `task_id` → `uploadTaskMaterial(taskId, "input", file)`.
  새 서버 API·새 권한 **없음**.
- **생성 성공 뒤 업로드 실패가 재생성으로 가지 않는다.** 만들어진 업무를 `created` 에 붙들고,
  같은 단추를 다시 눌러도 `submit()` 이 **업로드 재시도로 분기**한다. 모달은 닫지 않고
  「첨부 다시 시도 (N)」 · 「업무 열기」 · 「나중에 붙이기」 세 길을 준다. 만들어진 사실은 **먼저**
  `onCreated` 로 알려 목록이 그 업무를 들게 한다.
- 실패한 파일만 다시 올린다 — 성공한 것을 두 번 올리지 않는다.

### 구현하지 않은 것 — 그리고 그 이유 (완료라고 적지 않는다)

관리자 배정 · 요청 발송 · 회의 승격 세 갈래는 **DropZone 대신 권한 경계를 말한다**:

> 「자료는 **담당자가** 업무 상세에서 첨부할 수 있습니다 — 요청은 **상대가 수락해 담당자가 된 뒤**입니다.」
> (배정이면 「배정한 업무는 **그 담당자**입니다.」)

「생성 뒤 상세에서 붙인다」로만 쓰면 **보내는 사람도 할 수 있는 것처럼 읽혀 틀리므로** 누가 붙일 수
있는지를 문장에 넣었다.

**고른 파일을 조용히 버리지 않는다**: 파일을 고른 뒤 담당을 남으로 바꾸면 파일은 **그대로 남고**
「이 경로로는 함께 붙지 않습니다 — 담당을 나로 되돌리면 그대로 다시 섭니다」가 뜬다. 담당을 되돌리면
고른 파일이 다시 선다. 그 갈래로 보내도 **업로드를 성공한 척 부르지 않는다**(회귀로 단언).

**이 세 갈래는 첨부 기능이 완료된 것이 아니다.** 막는 것은 화면이 아니라 **기존 자료 쓰기 권한
계약**이고, 열려면 새 계약(예: 요청 발송이 실은 자료를 요청 축에 매다는 길, 또는 생성자에게 한시적
쓰기)이 필요하다 — 이 work 의 범위가 아니다.

### Composer 200자

**하드 캡을 새로 걸지 않았다.** SPEC-003 이 본문 계약을 보존하고 서버도 더 긴 내용을 받으므로,
화면이 상한을 만들면 붙여넣은 글이 조용히 잘린다. **카운터는 유지**한다(현행 그대로).
이 해석을 WORK 에 적는 것은 코디 몫이다 — **FE 가 스펙·WORK 를 고치지 않았다.**

## 5. 검증 (실제 exit code · 로그 보존)

| 명령 | exit | 결과 |
|---|---|---|
| `make frontend-test` | **0** | **53 파일 · 704 테스트 전부 통과** |
| `cd frontend && npx tsc --noEmit` | **0** | 오류 0 (로그 0바이트) |

- 직전 판이 **52 파일 · 683 테스트**였으므로 **+1 파일 · +21 테스트**가 이번에 더한 회귀다.
  **삭제·skip·단언 약화 0.**
- 로그: 세션 scratchpad 의 `fix1-frontend-test-1.log`(첫 실행 exit 2 — 아래) ·
  `fix1-frontend-test-2.log`(exit 0) · `fix1-tsc.log` 와 각 `.exit` 파일.
- **첫 실행 exit 2 는 내 테스트의 실수였다**(부하 아님): ① 첨부 칸을 요청 갈래 JSX 안에 두어
  본인 업무 갈래에서 렌더되지 않았다 ② W-3 테스트가 `renderPage` **뒤에** 모킹해 기본 mock 에 덮였다.
  둘 다 고치고 재실행해 exit 0 이다. **같은 검증을 이유 없이 반복하지 않았다** — 실행은 두 번뿐이다.
- `make frontend-build` 와 전체 `make verify` 는 **코디 몫**이라 돌리지 않았다.
- 검수가 남긴 부하 민감 테스트(`App`·`OrgPage`·`MeetingList`·`RelationGraph`)는 이번 두 실행에서
  뜨지 않았다(load ~13). **그 성격이 사라졌다고 주장하지 않는다** — 이번 범위에서 손대지 않았다.

## 6. 변경 파일

**제품 코드 (4)**

- `frontend/src/lib/viewModels.ts` — `WorkRequest` 에 `promoted_by_member_id`·`requester_kind`·`source_meeting_id` · `DirectTask` 최상위 `accepted_at` 제거
- `frontend/src/features/work/workRows.ts` — `isRequestOwner` 추가 · `isChildSettled` 정리(W-1)
- `frontend/src/features/work/MyWorkPage.tsx` — `requestOf`/`viewerIsRequester` 배선 · W-3 경고와 `settleError` · `onOpenTask`
- `frontend/src/features/work/WorkModals.tsx` — 자리 게이트 3종 · 첨부 DropZone 과 두 단계 업로드 · 실패 복구 푸터

**테스트 (4)**

- 신규 `frontend/src/features/work/CreateWorkAttach.test.tsx` (첨부 8건)
- `frontend/src/features/work/TaskLifecycleV2.test.tsx` (자리별 회귀 추가)
- `frontend/src/features/work/workRows.test.ts` (`isRequestOwner` 4 · W-1 정정)
- `frontend/src/features/work/MyWorkPage.test.tsx` (W-3 회귀 2 · 목록 mock 을 갈래로)

**덧붙여 고친 것 (통합 계약 중계 반영)**

- `viewModels.DirectTask` 에서 **최상위 `accepted_at` 을 뺐다.** 서버는 수락 시각을 담당 관계에 싣는다
  (`assignment.accepted_at` · `TaskAssignmentSummary`) — 최상위에 두면 **서버가 내지 않는 키**를 타입이
  약속한다. 제품 사용처는 없었고(확인함) **새 표시를 늘리지 않았다.** U-3 은
  `assignment.accepted_at` ↔ `started_at` 으로 읽는다. **최상위 `accepted_at` 을 받았다고 주장하지 않는다.**
- `MyWorkPage.tsx` 끝의 빈 줄 하나 정리(`git diff --check` 0건).

**문서 (2 · 허용 범위)**

- `v2-frontend-implementation-report.md` §0·§5 정정 (W-5·W-6)
- 이 파일

## 7. 남은 범위 · 주의점

- **W-4 의 나머지**: 첨부는 본인 업무 갈래만 섰고 **세 갈래는 계약 때문에 열리지 않았다.**
  Phase 7-A 를 「전부 완료」로 읽으면 안 된다. WORK 에 이 경계를 적는 것은 코디 몫이다.
- **B-1~B-3 (BE 연결과제)** 는 그대로 열려 있다 — `GET /api/tasks/{id}/children` 부재,
  `children[]` 의 `derived` 동반 여부, `started_at`/`accepted_at` 분리. **FE 회귀로 섞지 않았다.**
- **브라우저 E2E 미실행** — UX-U1~U-15 의 표시·자리 칸과 E-1~E-12 는 사용자 몫이다.
- `viewerIsRequester` 는 **요청 목록을 읽을 수 있을 때만** 참이 된다. 요청 읽기 권한이 없는
  관계자에게는 제안 단추가 서지 않는데, 그것은 서버도 같은 답을 내는 자리다(제안은 요청자의 것).
  다만 **목록이 실패하면**(기존 부채인 `.catch(() => [])`) 요청자에게도 잠시 안 보일 수 있다 —
  없는 권한을 그리는 것보다 안전한 쪽으로 닫았고, 목록 실패 자체는 W-3 과 같은 부채 축이다.
