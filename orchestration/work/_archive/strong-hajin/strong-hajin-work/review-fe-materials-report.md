# [reviewer] WORK-003 FE 요청 자료 연결 — read-only 검수

작성: 2026-09-20 · 워크트리 `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-work`
(브랜치 `kknaksss/strong-hajin-work`, 미커밋) · **소스와 diff만 읽었다. 코드·테스트·문서를 한 줄도
고치지 않았고 테스트·빌드·DB·E2E 를 실행하지 않았다.**

## 0. 판정

| # | 검수 항목 | 판정 |
|---|---|---|
| 1 | 생성 payload 는 기존 것만 · 돌아온 `request_id` 로 5 route 사용 · 자료 키 없음 | **PASS** |
| 2 | 파일/링크 성공·건별 실패·재시도가 실제 동작 · 성공분 재업로드 없음 · 내 업무 흐름 보존 | **PASS** |
| 3 | `REQUEST_MATERIALS_SAVED`·낡은 경고가 **일반 요청 갈래에서만** 걷혔고 실패를 저장됐다고 말하지 않음 | **PASS** |
| 4 | 테스트가 좁고 회의 승격 `request_id` blocker 가 숨기거나 우회되지 않고 분리됨 | **PASS** (테스트 미고정 — W-2) |
| 5 | allowed path · 이번 FE 분기에 무관한 backend 변경 없음 | **PASS** |

**전체 판정: PASS.** FAIL 0 · WARN 5. 두 단계 계약(만들고 → 돌아온 식별자로 붙인다)이 화면에서
실제로 구현돼 있고, 지난 BE 검수에서 확인한 서버 계약과 이름·순서가 어긋나지 않는다.

---

## 1. 항목 1 — 생성 payload 와 `request_id` 사용 · **PASS**

### 1-1. 생성 payload 에 자료 축이 없다

- 요청 생성 호출은 `frontend/src/features/work/WorkModals.tsx:3955-3979` 한 곳이고, 실리는 키는
  `description` · `start_date` · `due_date` · `cc_member_ids` · `checklist` · `reference_task_ids` ·
  `project_id` · `parent_task_id`(조건부) · `preceding_task_ids` · `approver_id` ·
  `supersedes_request_id`(조건부) 뿐이다. **`material_ids`·`attachments`·`material_draft_ids` 가 없다.**
- `frontend/src/lib/api.ts:505-541` 의 `createWorkRequest` 타입에도 자료 키가 없다. 예전에 있던
  `material_draft_ids` 칸은 주석으로만 남아 **왜 지웠는지**를 적어 둔다(`api.ts:529-535`).
- 전수 grep: `frontend/src` 안의 `material_draft_ids`·`material_ids` 출현은 전부 **주석 또는 테스트
  단언 문자열**이고, 남은 `output_material_ids` 는 완료보고 계약(`api.ts:163`)으로 이 건과 무관하다.

### 1-2. 돌아온 `request_id` 로 다섯 route 를 쓴다

`frontend/src/lib/api.ts:544-597` 이 다섯을 그대로 감싼다:

| 서버 route | FE 함수 | 줄 |
|---|---|---|
| `GET …/materials` | `getWorkRequestMaterials` | `api.ts:556-558` |
| `POST …/materials` (multipart, `kind=input`) | `uploadWorkRequestMaterial` | `api.ts:561-575` |
| `POST …/materials/links` | `attachWorkRequestMaterialLink` | `api.ts:578-586` |
| `GET …/materials/{id}/content` | `workRequestMaterialContentUrl` | `api.ts:589-591` |
| `DELETE …/materials/{id}` | `detachWorkRequestMaterial` | `api.ts:593-595` |

- `kind` 는 `"input"` 으로 고정해 보낸다(`api.ts:563`, `api.ts:583`) — 서버가 `input` 하나만 받는
  것과 맞고(`_require_material_role`), 화면이 산출물을 만들 길을 두지 않는다.
- 붙이는 자리는 **생성 응답의 식별자**다: `attachTo({ kind: "request", id: request.request_id }, …)`
  (`WorkModals.tsx:3990`). 추측한 id 나 목록 재조회로 찾아낸 id 가 아니다.
- `uploadWorkRequestMaterial` 이 공용 `request()` 대신 bare `fetch` 를 쓰는 것은 **집안 관례와 같다** —
  `kind` form 필드가 필요해 `uploadFile()`(`api.ts:1016-1025`)을 못 쓰는 `uploadTaskMaterial`
  (`api.ts:269-279`)과 같은 모양이고, `credentials: "same-origin"` · `ApiError` 변환까지 동일하다.
- 댓글 첨부·evidence 입구를 쓰지 않는다(§2-3 테스트가 이것을 단언한다).

---

## 2. 항목 2 — 성공·건별 실패·재시도 · **PASS**

### 2-1. 실패한 것만 돌아온다

`WorkModals.tsx:3730-3755` `attachTo(host, files, links)`:

- 파일과 링크를 각각 순회하며 `try/catch` 로 **건별로** 실패를 모은다(`:3736-3744`, `:3745-3753`).
- 반환값은 `{ files: failedFiles, links: failedLinks }` — **성공한 것은 돌아오지 않는다.**
- 업무/요청은 `host.kind` 한 곳에서만 갈린다(`:3738-3740`, `:3748-3749`) — 두 갈래가 같은 걸음을 걷는다.

### 2-2. 다시 눌러도 생성이 반복되지 않고 성공분을 두 번 올리지 않는다

- 부분 실패 시 `setCreated({ host, title, failed, message, assignedToOther })`
  (`WorkModals.tsx:3997-4003`)로 **만들어진 것**을 붙들고 모달을 닫지 않는다.
- `submit()` 첫 줄이 `if (created) { await retryAttach(); return; }`
  (`WorkModals.tsx:3792-3796`) — **생성 경로로 되돌아갈 길이 없다.**
- `retryAttach()`(`WorkModals.tsx:3757-3786`)는 `created.failed` 만 `attachTo` 에 넘긴다 →
  이미 성공한 파일·링크는 재업로드 대상이 아니다. 남은 것이 0 이면 `onCreated` 로 「모두 올렸습니다」를
  알리고 상태를 비운 뒤 닫는다(`:3766-3773`).
- `submitAttempt.current = null` 을 부분 실패 직전에 둔다(`WorkModals.tsx:3996`) — 멱등 키가 다음
  의도로 넘어가지 않는다.

### 2-3. 테스트가 이 셋을 실제로 고정한다 (내용만 읽었고 실행하지 않았다)

`frontend/src/features/work/CreateWorkAttach.test.tsx`:

- `:246-266` — 생성 payload 를 직렬화해 `material`·`attachment`·`draft`·링크 주소가 **한 글자도
  없음**을 단언하고, `uploadTaskMaterial`·`attachTaskMaterialLink`·`uploadCommentAttachment`·
  `uploadRequestEvidence` 가 **불리지 않음**까지 함께 못 박는다(우회 금지).
- `:268-288` — 파일 두 건이 `["req-7","req-7"]` 로 **돌아온 식별자**에 올라간다.
- `:290-308` — 링크가 같은 두 단계로 `["req-7", {url,label}]` 에 붙는다.
- `:311-341` — 링크 1건 실패 → 「보냈다」를 먼저 알리고 닫지 않음 → 「첨부 다시 시도 (1)」 →
  `createWorkRequest` **1회 유지**, `uploadWorkRequestMaterial` **1회 유지**(성공분 재업로드 없음).

### 2-4. 내 업무(task) 흐름 보존

- 업무 갈래는 `attachTo({ kind: "task", id: madeTask.task_id }, …)` 로 기존
  `uploadTaskMaterial(…, "input", …)` · `attachTaskMaterialLink(…, "input", …)` 를 그대로 지난다
  (`WorkModals.tsx:3738`, `:3748`, `:3903`).
- `attachSupported = kind === "task" && ownerRoute === "self"`(`WorkModals.tsx:3701`)가 그대로 —
  관리자 배정·수평 생성에서는 예전처럼 붙이지 않는다.
- 기존 업무 테스트가 남아 있다: `CreateWorkAttach.test.tsx:119`·`:139`·`:155`·`:179`·`:347`·`:370`·`:379`.
- 「업무 열기」는 `created.host.kind === "task"` 일 때만 선다(`WorkModals.tsx:4164`) — 보낸 요청에는
  아직 열 업무 상세가 없다는 사실을 그대로 말한다.

---

## 3. 항목 3 — 경고 제거 범위와 문구 정직성 · **PASS**

- `REQUEST_MATERIALS_SAVED` 와 `REQUEST_MATERIALS_GAP_TEXT` 는 `frontend/src` 전체에서 **사라졌다**
  (전수 grep 0건). 지난 BE 검수 시점에 `WorkModals.tsx:3358` 에 있던 `= false` 상수가 없어졌다.
- 대신 갈래를 가르는 값 하나가 섰다:
  `const requestMaterialsSupported = kind === "request" && !onSubmitRequest;`
  (`WorkModals.tsx:3714`) → `materialsSaved = kind === "task" ? attachSupported : requestMaterialsSupported`
  (`:3715`).
  **즉 일반 요청 갈래에서만 경고가 걷혔고, 회의 승격(`onSubmitRequest` 가 있는 경우)에는 그대로 남는다.**
- 경고는 `!materialsSaved` 일 때만 그린다(`WorkModals.tsx:4641-4644`, `FieldMessage error=` 로 **경고
  톤**). 일반 요청에서는 서지 않는다 — `CreateWorkAttach.test.tsx:225-237` 이 경고·「저장되지
  않습니다」 배지가 **없음**을 단언한다.
- **실패를 저장됐다고 말하지 않는다**: 행의 `reason` 이 세 갈래로 갈린다
  (`WorkModals.tsx:4667-4671`, `:4726-4730`) — 실패한 건은 `"올리지 못했습니다"`/`"붙이지 못했습니다"`,
  저장 안 되는 갈래는 `"저장되지 않습니다"`, 나머지는 `null`.
- 힌트 문구도 갈래를 따른다(`WorkModals.tsx:4649-4656`): 요청은 「요청을 보낸 직후 참고 자료로 함께
  붙습니다」, 저장 안 되는 갈래는 「지금은 고르기까지이고 이 요청과 함께 저장되지 않습니다」.
- 부분 실패 때 사용자에게 가는 문장이 사실과 맞는다: 성공 0건이면 알림에 자료 문구를 **붙이지
  않고**(`WorkModals.tsx:3993`), 별도로 `onError("요청은 보냈지만 첨부 N건을 올리지 못했습니다…")`
  (`:4005-4007`)를 낸다.

---

## 4. 항목 4 — 테스트 범위와 승격 blocker 분리 · **PASS** (W-2)

### 4-1. blocker 는 숨기지도 우회하지도 않았다

- 승격 갈래는 `else if (onSubmitRequest)` 하나이고(`WorkModals.tsx:3925-3954`), 그 안에서
  **`attachTo` 를 부르지 않는다** — 없는 `request_id` 를 추측해 다른 요청에 붙이는 길이 없다.
- 일반 요청 입구로 새지도 않는다: `CreateWork.test.tsx:305-324` 가 승격에서
  `api.createWorkRequest` 가 **불리지 않음**을 단언한다(그쪽으로 가면 출처 두 열이 빠진다).
- 사용자에게 사실을 그대로 말한다 — `PROMOTION_MATERIALS_GAP_TEXT`
  (`WorkModals.tsx:3360-3361`): 「승격 응답이 요청 식별자를 돌려주지 않습니다. 여기서 고른 파일과
  링크는 저장되지 않고, 창을 닫으면 사라집니다.」 **원인과 결과를 같이** 적었고 「나중에」로
  뭉뚱그리지 않았다.
- 고칠 자리도 코드 주석이 지목한다: 승격 입구의 **응답**(`WorkModals.tsx:3355-3358`, `:3936-3941`).
  이 분기에서 backend 를 건드리지 않겠다고 명시했고 실제로 건드리지 않았다(§5).

> 참고 — 지난 BE 검수에서 확인한 사실과 일치한다: 승격 route 는 `link_promoted_todo` 의 뷰를
> 돌려주고 `request_id` 를 payload 의 `linked.work_request_id` 안쪽에만 담는다. FE 어댑터
> (`MeetingDetailPage`)가 문장 하나만 돌려주도록 되어 있어 화면까지 오지 않는 것이 맞다.

### 4-2. 테스트는 좁다

- 신규/변경 테스트는 `CreateWorkAttach.test.tsx` 의 요청 갈래 5건(`:215`·`:225`·`:246`·`:268`·`:290`·`:311`)
  으로, **브리프의 흐름당 1건**이고 전수 조합이 없다.
- 기존 업무 갈래 테스트는 문구 수정 외에 살아 있다.

### 4-3. **W-2 (WARN)** — 승격 blocker 를 고정하는 테스트가 없다

`CreateWork.test.tsx` 의 `origin="meeting"` 묶음(`:255-352`)에는 자료 판에 대한 단언이 없다. 즉
**「승격에서는 경고가 서고 업로드를 부르지 않는다」를 고정하는 시험이 한 건도 없다.**
`requestMaterialsSupported` 의 `!onSubmitRequest` 조건이 미래에 지워져도 잡히지 않는다 —
그때 화면은 승격에서 `attachTo` 를 부르고, `host.id` 로 넘길 식별자가 없어 조용히 어긋난다.
코드와 문구로는 분리가 명확하므로 FAIL 로 세지 않는다.

---

## 5. 항목 5 — allowed path · backend 무변경 · **PASS**

- 이번 FE 분기의 변경은 `frontend/src/**` 안이다. 파일 수정 시각이 갈래를 그대로 보여 준다:
  `frontend/src/lib/api.ts` 11:25 · `frontend/src/features/work/WorkModals.tsx` 11:27 ↔
  `backend/src/ax_workspace/modules/work/requests.py` 01:00 ·
  `docs/unified-operations-inventory.json` 01:00 ·
  `backend/tests/unit/test_request_material_ax_mapping.py` 01:01 (전부 **직전 BE 수정 분기**의 것).
- `find backend docs -newermt "2026-09-20 02:00"` 에 걸리는 소스 파일이 **0건**이다
  (`backend/.pytest_cache/*` 두 개만 — 테스트 실행 산물이고 소스가 아니다).
- 새 서버 API·새 payload 키를 만들지 않았고, 기존 다섯 route 만 썼다(§1-2).

---

## 6. WARN 목록

- **W-1 — 워커가 보고한 테스트 수치는 이 검수가 재현하지 않았다.** 브리프가 테스트를 금지했으므로
  `make frontend-test` 를 포함해 아무것도 실행하지 않았다. 위의 테스트 인용은 **파일 내용을 읽은
  것**이고 통과 여부가 아니다 — 보고된 모든 수치는 **미검증**으로 기록한다.
- **W-2 — 승격 blocker 를 고정하는 테스트가 없다** (§4-3).
- **W-3 — `attachTo` 가 모든 실패를 한 가지로 취급한다** (`WorkModals.tsx:3736-3744`의 맨 `catch`).
  25MB 초과(422) · 이미 답한 요청(409) · 권한 없음(403) 처럼 **다시 눌러도 달라지지 않는 실패**도
  「첨부 다시 시도」로 안내된다. 게다가 `created` 가 서면 행의 「빼기」가 비활성이라
  (`WorkModals.tsx:4673`, `:4732`) 그 건을 목록에서 뺄 수 없다. 출구는 있다 — 「나중에 붙이기」가
  두 갈래 모두 선다(`WorkModals.tsx:4160-4162`) — 그래서 막다른 길은 아니지만, 고칠 수 없는 실패에
  같은 단추를 반복해 권하는 자리다. 서버가 낸 `ApiError.status` 를 이미 들고 있으므로(`api.ts:63-72`)
  가르는 데 새 정보가 필요하지도 않다.
- **W-4 — 요청 생성 payload 가 예전보다 넓어졌다** (`WorkModals.tsx:3955-3971`): `start_date` ·
  `project_id` · `preceding_task_ids` · `approver_id` 가 함께 나간다. 지난 BE 검수에서
  `WorkRequestApplication.create` 가 넷 다 받는 것을 확인했으므로 **결함이 아니다.** 다만 브리프의
  「기존 payload 만」을 글자 그대로 읽으면 넓어진 것이 맞아 사실로 남긴다. 자료 키가 아니라는 점이
  핵심이고, 그것은 §1-1 대로 없다.
- **W-5 — 승격 갈래에서 고른 파일은 제출 순간 조용히 버려진다** (`WorkModals.tsx:3925-3954`).
  경고를 **고르기 전에** 보여 주고 문구가 「창을 닫으면 사라집니다」까지 말하므로 거짓말은 아니다.
  제출 시점의 재확인은 없다 — 의도된 설계 결정으로 읽고 기록만 한다.

---

## 7. 이 검수가 확인하지 못한 것

- **테스트 실행 0.** 워커 보고 수치 전부 미검증(W-1). 위 인용은 소스 독해다.
- 실제 브라우저 동작(멀티파트 업로드·드래그앤드롭·모달 포커스)은 확인하지 않았다 — 정적 독해뿐이다.
- 지난 BE 검수의 미해결 위험(기존 contract 4 failed · checkout 사고 · W-2~W-7)은 이번 범위 밖이라
  열지 않았고 그대로 남아 있다.
