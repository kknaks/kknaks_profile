# 리뷰 리포트 — strong-hajin-work / v2 BE·FE 통합 구현 (2026-09-17)

## 판정: **WARN — 계약 위반을 찾지 못했다. 막는 것은 없다.**
## 다만 **현재 트리를 덮는 실행이 하나도 없다** — 그 공백을 통과로 읽지 않는다.

브리프가 이름으로 짚은 **필수 회귀 전부와 추가 확인 전부**를 코드·테스트 실물로 확인했고
**전부 구현·검증돼 있었다.** 새 계약 결함은 **0건**이다. 남는 것은 **증거 공백 둘**(E-1·E-2)이고
둘 다 **코디의 통합 1회**로 닫힌다.

## 검수 범위와 실행한 검사

- 기준선: `v2-code-baseline/manifest.json` (HEAD 차이가 아니라 baseline↔현재).
- 대조한 보고: `v2-backend-implementation-report.md` · `v2-contract-tests-report.md` ·
  `v2-postgres-report.md` · `v2-frontend-cancel-reason-report.md`.
- **실행 0건** — 보존 로그와 `/tmp/w2logs/` 를 열어 읽기만 했다. 제품·문서·DB 무수정.
- FE 자체 검수는 `review-v2-frontend-report.md` 에서 닫혔으므로 **그 이후 변경(취소 사유)과 BE 연결만** 봤다.

---

## E-1. 증거 공백 — **어느 실행도 지금 트리를 덮지 않는다** (비차단, 코디 몫)

수치를 실제로 열어 확인했다. **각 실행 시각과 마지막 코드 변경 시각을 맞춰 보면 이렇다.**

| 실행 | 시각 | 결과 | 지금 트리를 덮나 |
|---|---|---|---|
| `make test-contract` **전량** (`contract-4`) | 18:08 | **104 failed / 872 passed · rc 2** | ✗ (가장 최근 «전량» 이고 빨강이다) |
| 기존 계약 **준전량** (`-k 'not …v2'`, `narrow-15`) | **19:08** | **2 failed / 975 passed · rc 2** | ✗ — 이후 `assignments.py` 가 19:13:53 에 바뀜 |
| v2 신규 33건 전량 (`run22`) | 18:40 | 31 passed · rc 0 | ✗ — 계약 워커 스스로 「**정정 후 33건 전량은 재실행하지 않았다**」고 적었다 |
| 정정분만 (`changed2`) | 18:53 | 5 passed · rc 0 | 부분 |
| `make test-postgres` 전량 (`final-full-01`) | **19:06** | **77 passed · rc 0** | ✗ — 그 뒤 `platform/actions.py` · `command_contracts.py` · `modules/work/assignments.py` · PG 테스트 파일 **넷이 바뀌었다**(내가 `find -newermt` 로 셌다) |
| `make test-unit` (`unit-final2`) | 19:12 | 328 passed · rc 0 | ✗ — 19:13:53 변경 전 |
| 마지막 좁힌 라운드 (`narrow-20`) | **19:14** | 54 passed · rc 0 | **○ — 지금 트리를 덮는 유일한 실행이고 54건뿐이다** |
| FE `make frontend-test` | 18:58 | **53 파일 · 713 passed · rc 0** | **○** — 18:58 이후 `frontend/src` 변경 **0건**(확인함) |
| FE `tsc --noEmit` · `frontend-build` | 18:57~18:58 | rc 0 · rc 0 | ○ |

- **BE 워커의 보고는 정직하다** — 「전량 `make test-contract` 1회는 아직 돌리지 않았다 · 코디네이터가
  통합 1회로 모으기로 했다」를 본문에 적었다. 계약 워커도 「정정 후 전량 미실행」을 적었다.
  **감춘 것이 아니라 아직 안 한 것**이고, 그것이 정확히 코디의 통합 검증 몫이다.
- **경과는 실물로 확인된다**: 400 → 104 → …(narrow) → `narrow-15` 975 passed/2 failed → 16~20 에서 rc 0.
- **코디의 `make verify` 는 아직 돌지 않았다.** `make frontend-build` 는 FE 쪽만 rc 0 이 있다.
- **최소 조치 (코디)**: 지금 트리에서 `make test-contract` · `make test-unit` · `make test-postgres` 를
  **각 1회** 돌린다. 특히 **PG 는 `actions.py`·`assignments.py` 가 바뀐 뒤 한 번도 안 돌았다** —
  잠금 수정이 든 모듈이라 이 한 번이 가장 값지다.

## E-2. 핵심 로그가 **휘발 영역에만** 있다 (비차단, 코디 몫)

`narrow-1~20` · `unit-final*` · `contract-1~4` 가 **`/tmp/w2logs/`(37개)** 에만 있다.
그중 **증거로서 가장 무거운 `narrow-15`(975 passed)·`narrow-20`(현재 트리 유일)·`unit-final2`** 가
`orchestration/work/strong-hajin-work/` 의 보존 디렉토리에 **없다.** (FE·PG·계약 쪽은 보존됐다.)
→ 그 셋만 `v2-backend-verification/` 으로 복사하면 된다. 앞선 FE 검수에서 같은 일이 한 번 있었다.

---

## 브리프가 이름으로 짚은 것 — 전부 확인, 전부 구현됨

### 「구현 중 발견한 필수 회귀」 여섯

| 항목 | 확인 결과 |
|---|---|
| FastAPI 응답모델이 `derived`·시간·`child_progress`·`child.derived` 를 잘라내던 결함 | **실제 HTTP 로 검증된다.** `detail()`(`test_task_lifecycle_v2_support.py:40-43`)가 `client.get(...).json()` 이고, 그 위에서 `["derived"]["approval"]`·`["children"][0]["derived"]["assignment"]`(`:118`)·`child_progress`(12곳)·`started_at`/`accepted_at`/`completed_at`(`:75·87·186·197·527`)를 단언한다 |
| 재배정 대기에서 `task.assignment` 가 `pending` 을 현재 담당처럼 내지 않는다 | ✓ `:186`·`:820` 이 `assignment.status == "active"` 를 못 박고, BE 보고의 「재배정 직후 `['superseded','pending']` → **`['active','pending']`**」 매핑과 맞는다 |
| 일반 구성원 수신자도 수락/거절, 제3자는 못 답한다 | ✓ 역량에 `work_request.decide` 추가 · `..._only_the_recipient_answers_...` 가 거절을 못 박는다 |
| 신규 요청자 조상 읽기는 `requester_id`/`promoted_by` **본인 한정**, CC 로 확장 안 함 | ✓ `application.py:274-304` `_requested_ancestor` — 두 항만 보고, 주석이 「**수신자·참조자(cc)는 여기 들어가지 않는다** · 부모 요청 자체의 기존 cc 읽기는 그대로 살아 있다 · 다른 권한으로 읽히는 하위는 무관하게 읽힌다」를 명시 |
| 완료보고 하위 `reason` 은 `awaiting_approval` | ✓ `application.py:659`·`836` 구현, `test_task_lifecycle_v2.py:596` 이 단언 |
| `my_work` 에 요청했다는 이유로 타인 업무가 섞이지 않는다 | ✓ `:110`·`:144`·`:854` 부정, `:190`·`:824` 수락 후 긍정 — 양쪽으로 단언 |

### 「추가 확인」 둘

- **요청자 관계 읽기 역량 회수 후 목록/상세/자료가 같은 경계** — ✓ `WORK_REQUEST_READ` 한 역량이
  **세 자리에서 같이** 걸린다: `_requested_ancestor`(`:288`) · 목록 `_list`(`:455`) · 자료 축(`:1509`).
  계약 워커도 `..._the_requesters_reading_closes_everywhere_at_once_when_it_is_revoked` 로 A5 에 붙였다.
- **승인 후 재개의 시간 비교(naive/aware)** — ✓ `_as_utc()`(`application.py:1822`)가 naive 를 UTC 로 올리고
  **비교 양쪽에 모두** 쓰인다(`:642-643`·`:904-905`). 규칙은 「승인 행이 전부 `reopened_at` 이전이면
  완결이 아니다」 — **과거 승인이 다시 유효해지지 않는다.**

### 재전송(영수증) — 브리프의 네 조건을 모두 만족한다

- **원래 `expected_version` 과 같은 본문 그대로** 재시도한다: `test_task_lifecycle_v2.py:1319`
  (수락을 `expected_version: 1` 로 두 번), `:1041-1044`(제안 응답을 `answered_at_version` 으로).
  **최신 version 을 다시 읽어 보내지 않는다.**
- **`== 200` 으로 단언**하고(`!= 200` 아님) 회차·담당 행 불변까지 본다 —
  `assignment` 행이 `["active"]` 하나임을 DB 로 확인(`:1325-1329`·`:1341-1345`).
- **합의취소로 담당이 `ended` 여도 영수증이 먼저다**: `respond_to_proposal`(`application.py:1236-1269`)이
  ① 읽기 권한 재검사(K-2)를 **가장 먼저**, ② 그다음 **저장된 답**(같은 사람·같은 답·`record.task_version`)으로
  영수증을 가르고, ③ **회차 검사(`:1270`)와 담당자 검사보다 앞**에 둔다. 주석이 「합의 취소 뒤에는 담당
  관계까지 끝나 있어서 담당자 검사도 막는다」로 그 이유를 적었다.
- **다른 답은 충돌**: `:1264-1269` → `WORK_PROPOSAL_NOT_PENDING` 409, 테스트 `:1051-1058` 이 409 를 단언.

### 취소 사유 필수 — **모든 입구가 닫혔다**

| 입구 | 확인 |
|---|---|
| REST `POST /api/tasks/{id}/cancel` | ✓ `http.py:2313` 이 `TaskCancelInput`(`task_commands.py:142-159`, `min_length=1` + 공백 거절 validator)을 받는다 |
| MCP `task.transition` · AX `task.transition` | ✓ `TaskTransitionInput`(`task_commands.py:118-135`)이 `cancelled`·`blocked` 에 사유를 요구하고 **공백 문자열도 거절**한다 |
| AX 확인 payload | ✓ `command_contracts.py:58-62` 가 `reason` 의 empty policy 를 **`forbid`** 로 둔다 — 「사유가 사라진 확인은 사유를 요구한 적이 없는 것과 같다」 |
| FE 상세 | ✓ `WorkModals.tsx:1868-1885` — `confirmCancel` 이 「취소 사유를 남겨 주세요」 입력 프롬프트다 |
| FE 오늘·캘린더 | ✓ 둘 다 **같은 `TaskDetailDrawer`** 를 쓰고 `transitionDirectTask(..., reason)` 으로 넘긴다 (`TodayPage.tsx:168·376` · `CalendarPage.tsx:71·113`). 별도 빠른 취소 경로 없음 |
| 사유 저장·이력 | ✓ `record_activity(..., reason=...)` 로 진행 기록에 남는다. FE 표시는 `cancelReasonLabel`(`WorkModals.tsx:1719`) |

### `GET /api/work-requests/inbox` — 닫혔다

- **경로 충돌 없음**: `http.py:1913` 의 `inbox` 가 동적 `{request_id}`(`:1923`)보다 **먼저 선언**된다 —
  FastAPI 는 선언 순서로 매칭하므로 가려지지 않는다.
- **인벤토리 반영**: `docs/unified-operations-inventory.json` 에 `GET /api/work-requests/inbox` 와
  MCP `work_request_inbox` 가 둘 다 있다(전체 재작성이 아니라 항목 추가).
- 계약 테스트는 `tests/contract/test_task_creation_contract.py` 가 갖고 있다.

### PostgreSQL write skew — 수정도 시험도 제대로다

- **잠금 순서**: `reopen`(`application.py:1155·1173`)이 **하위 → 상위**를 `lock=True`(`FOR UPDATE` +
  `populate_existing=True`)로 잡고, 완료 경로(`transition`, `:1071`)는 **자기 한 행만** 잡는다.
  주석이 「한쪽이 둘, 다른 쪽이 하나라 서로를 기다리는 고리가 생기지 않는다 — **모순을 deadlock 으로
  바꾸지 않는다**」로 이유를 적었다.
- **fresh 재검사**: `transition()` 이 **잠금을 잡은 뒤에** `blocking_children(task)` 를 읽는다(`:1071` → `:1076`).
  READ COMMITTED 에서 상대 커밋 뒤의 상태를 본다.
- **테스트가 진짜로 겹친다**: `test_task_lifecycle_v2_postgres.py` 가 `task_by_id` 의 **잠금 직전 지점**을
  monkeypatch 로 붙들고 `Event`/`Barrier` 로 교차시키며, **겹치지 못하면 timeout 으로 시험이 깨지게**
  해 두었다(`:71` 주석 · `:477`·`:488` 의 `assert ... wait(timeout=...)`).
- **경합 승자를 뭉개지 않는다**: `completed.status_code == 200` · `reopened.status_code == **409**` +
  본문에 「상위 업무가 완료」까지 단언(`:501-503`). **`!=200`·400·404·5xx 를 통과로 받지 않는다.**
  그 위에 `_no_open_child_under_a_settled_parent()` 불변식이 한 줄 더 있다.
- 수치: `baseline-full-01` **2 failed/63 passed · rc 2** → `final-full-01` **77 passed · rc 0**.

### A1~C2 21건 · K-1~K-11 · 테스트 변경 방식

- **21건 전수 추적됨.** 함수 이름은 17개지만 `a7_a8_a9_…`·`b1(·B2)`·`b3_b4_…` 로 **묶어** 닫았고
  docstring 에 ID 가 박혀 있다(`:210`·`:504`·`:571`·`:789`·`:802`). 계약 리포트 §1 의 표와 일치한다.
- **삭제·skip·빈 단언 0건**: BE 리포트가 「이전 보장 → 대체 보장」 12행 매핑표로 근거(SPEC 절)를 달았고,
  내가 표본으로 확인한 자리(`completion_submitted`→`done+awaiting_review`, `child_progress` 확장,
  422→409, 재배정 `['active','pending']`, 요청자 `/materials` 403·404→200)가 전부 **계약 변경에 따른 재작성**이지
  약화가 아니다. `make_request_look_pending()` 도 「업무만 지우고 회차는 제품이 연 것을 쓴다」로 옮겼다.
- **멱등 키 범위**: 브리프 정정대로 **생성·발송에만** 요구하고, 새 상태 명령에는 `expected_version` +
  상태 가드 + 권한 재검사 + 중복 effect 없음으로 닫았다(`c2` 테스트가 네 명령의 422·stale 을 전수로 본다).
  **키가 없다는 이유로 결함을 올리지 않았다.**

### FE ↔ BE 연결 (앞선 FE 검수 이후분만)

- **취소 사유 정정**: FE `make frontend-test` **713 passed(53 파일) · rc 0** · `tsc` rc 0 ·
  `frontend-build` rc 0. 첫 실행 3 failed 는 같은 판에서 재실행 rc 0 으로 닫혔다(둘 다 보존됨).
  706 → 713 = **+7**. 18:58 이후 `frontend/src` 변경 **0건**이라 **이 수치가 현재 FE 트리를 덮는다.**
- `started_at`/`accepted_at` 분리(UX-U3)는 BE 응답 회귀로 닫혔다(`:197-198`) — 앞선 검수의 **B-3 해소**.
- `GET /api/tasks/{id}/children` 실재 — 앞선 검수의 **B-1 해소**. `children[].derived` 도 HTTP 로 단언 — **B-2 해소.**
- **목록정리 가드**: `requests.py:857-879` — 요청자(+`promoted_by`)만(`:867-871`), 그리고
  `_CLEANABLE_REQUEST_STATES = {rejected, withdrawn, cancelled_by_agreement}`(`:1019`)라
  **진행 중 요청은 거절**된다. **합의취소 후 목록정리 종단이 그 집합으로 닫힌다.**
- `viewModels` 의 `| string` 확장은 **기존 집 규칙**이고(앞선 검수 W-7) 이번 판에서 BE 불일치를 감춘
  새 자리를 찾지 못했다 — `derived`·`children[].derived`·시간 넷이 실제 응답으로 단언되기 때문이다.
- **브라우저 E2E 는 실행하지 않았다.** UX-U1~U-15 의 「표시·자리」 칸과 E-1~E-12 는 사용자 몫이다.
- 선행/후행 관계는 사용자가 v2 완료 후 보기로 했으므로 **이번 범위에 넣지 않았다.**

### 미정의 보존

- **OQ-203** — 제출에 하위 검사를 더하지 않은 **현행 보존**이고 새 정책 확정 표시가 없다.
- **OQ-206** — 승격 요청 완료 확인자는 **미정 그대로**다. seed 에서 승격 경로를 지우지도,
  자동 승인을 만들지도 않았다(BE·FE 양쪽 확인). 새 사용자 답은 오지 않았다.

---

## 결론

**v2 직접 계약 위반: 0건.** 브리프가 짚은 필수 회귀·추가 확인·재전송·취소 사유·inbox·write skew가
**전부 실물로 구현·검증돼 있었고**, 몇 자리(영수증 순서, 잠금 순서, 조상 읽기 범위)는 주석이 이유까지
적어 두어 다음 사람이 되돌리기 어렵게 해 두었다.

**남는 것은 증거뿐이다** — E-1(현재 트리를 덮는 실행이 `narrow-20` 54건과 FE 713건뿐) ·
E-2(핵심 로그 셋이 `/tmp` 에만 있음). **둘 다 코디의 통합 1회와 복사 한 번으로 닫힌다.**
**이 검수로 v2 완료를 주장하지 않는다** — `make verify` 미실행, 브라우저 E2E 미실행이 그대로다.
