# reviewer_code — WP-130 코드 검수 리포트 (BE+FE 미커밋 diff)

- 일시: 2026-09-01
- 워크트리: `/Users/kknaks/orca/workspaces/mediness-app/task-improve` (branch `kknaksss/task-improve`)
- 범위: **미커밋 diff 만** — `git diff` 33 파일 + untracked 24 파일(+ `node_modules/`). 직전 커밋 `5b98247a`(WP-129)는 검수 통과분으로 제외.
- 방식: read-only. 코드 수정·테스트 실행 없음. 「기존 실패의 diff 무관성」은 **호출 사슬 추적**으로 판정했다.

## 판정: **FAIL**

계약(§4.8·§4.19·domains) 위반은 없다 — 3객체 migration·422 술어·storage·2단 셸·모달 단일성은 전부 계약대로다.
**막는 것은 셋**이다: ① 이 diff 가 **기존 테스트를 깨뜨렸는데 그것을 「diff 무관 선행 실패」로 잘못 보고**했고(P8 「신규 실패 0」 직접 위반) ② 컴포저 **다중 파일 첨부가 유실**되며 ③ **수정 카드 첨부 경로가 미구현인 채 스키마·정리 훅만 서 있어** 엉뚱한 태스크에 파일이 붙는 창이 생겼다.

| # | 등급 | 체크리스트 | 요지 |
|---|---|---|---|
| F-1 | FAIL | 10 · P8 | WBS `status=done` PATCH 테스트 2파일이 이 diff 로 새로 깨진다 (26건의 실체) |
| F-2 | FAIL | 6 | 파일 여러 개 동시 선택 시 마지막 1건만 태스크에 붙는다 |
| F-3 | FAIL | 6 | 수정 카드 첨부 미구현 + Redis 바인딩 오소비 → 다른 태스크에 첨부 |
| W-1 | WARN | 4 | `description` fallback 규칙이 BE·FE 두 벌 (BE `body` 필드는 FE 미사용) |
| W-2 | WARN | 4 · 배포 | 기존 decision·incident 태스크는 배경이 통째로 빈다 |
| W-3 | WARN | 3 | 25MB 검사가 **전량 수신 뒤** — 자기 docstring 과 어긋남 |
| W-4 | WARN | 6 | `draft_id` 소유자 바인딩 0 (방어 = UUID4 추측 불가 하나) |
| W-5 | WARN | 5 | 「메타 스트립 diff 0」 계약과 달리 `TaskMetaPanel` 통째 삭제·재작성 |
| W-6 | WARN | 1 · 10ⓑ | `size_bytes` — 코드가 맞고 **문서 환류 대상** |
| W-7 | WARN | 10ⓐ | §6.1 「그 턴에 카드를 세우지 않는다」 — 코드가 맞고 **스펙 환류 대상** |
| W-8 | WARN | 8 | 레포 루트 untracked `node_modules/`(vitest 캐시) — .gitignore 부재 |
| W-9 | WARN | 3 | denylist 주석 오타 (코드 정상) |

---

## FAIL 상세

### F-1. 「기존 실패 26건은 diff 무관」 판정이 틀렸다 — 이 diff 가 깨뜨린 것이다

새 근거 검사가 **사람 액터의 `→ done` 전부**에 걸리는데(`back/app/services/action_runtime/tasks/lifecycle.py:141-175`), WBS 상태 칩 경로도 그 seam 을 지난다(`back/app/services/version_wbs.py:1309-1313` → `_transition_linked_task` → `apply_transition_chain`). `completionNote` 를 안 보내고 산출물도 없으면 **422** 다.

diff 가 갱신하지 않은 두 파일이 정확히 그 요청을 보내고 200 을 기대한다:

- `back/tests/api/test_version_wbs_checkitem.py:318-320` — `PATCH /versions/{v}/wbs/tasks/{wid} {"status":"done"}` → `.json()["data"]` 로 트리를 읽는다. 422 면 `KeyError`.
- 같은 파일 `:511` (`_patch_status(..., "done")` — `test_force_done_autochecks_all_todos`), `:329`·`:343`·`:371`·`:454` 등 다수.
- `back/tests/services/test_version_progress.py:218` · `:262` · `:296` — 같은 형태.

diff 는 done 전이를 쓰는 **다른** 테스트 6파일(`test_wp104_w10_bug020_task_lifecycle.py`·`test_wp104_w5_task_canonical.py`·`test_wp104_w7_legacy_cleanup.py`·`test_wp104_w10_bug023_terminal_reassign.py`·`test_wp129_task_request_axis.py`·`test_decision_workflow_e2e.py`)은 갱신했다 — **WBS 축 두 파일만 빠졌다.** 「26건 version_wbs_checkitem」이라는 숫자와 파일명이 그 사실을 그대로 가리킨다.

⇒ **WP-130 P8 검증 「전체 테스트 통과, 신규 실패 0」 위반.** BE 보고의 「447 passed / 0 failed」는 이 두 파일을 포함하지 않은 부분 실행으로 보인다.
⇒ 조치: 두 파일의 done PATCH 에 `completionNote` 를 싣거나(WBS 표면의 새 계약과 동형), 산출물을 세워 준다. `tests/services/test_wp109_minutes_proposal.py:193`·`tests/services/engine_v2/test_runs_surface.py:149` 는 문자열 리터럴이라 무관하다(확인함).

### F-2. 컴포저에서 파일을 **한 번에 여러 개** 고르면 마지막 1건만 붙는다

`front/components/landing-chat/LandingChatClient.tsx` `pickFiles`:

```ts
staged.forEach((chip, i) => {
  void uploadLandingChatAttachment(picked[i], pickFilesRef.current)   // ← 전부 같은 값(첫 배치엔 null)
```

`forEach` 가 도는 동안 어떤 promise 도 아직 resolve 되지 않아 `pickFilesRef.current` 는 **N번 모두 같은 값**이다. `draft_id` 가 null 이면 서버 `stage_file` 이 파일마다 새 UUID 를 발급하고(`back/app/services/action_runtime/workflow/task_draft/attachments.py:61`), `setDraftId` 는 **마지막에 resolve 된 하나**만 남긴다. 나머지 N-1 개는 다른 `drafts/{id}/` 에 고아로 남아 승인 시 귀속되지 않는다(회수 배치가 지운다).

`front/components/landing-chat/Composer.tsx` 의 file input 에 `multiple` 이 있어 **정상 동선**이다. 계약 「같은 발화의 첨부가 한 초안에 묶인다」(`landing-chat.ts` `uploadLandingChatAttachment` 주석) 위반.
⇒ 조치: 첫 파일 업로드를 await 해 `draft_id` 를 확정한 뒤 나머지를 그 값으로 올리거나(직렬 1건 + 병렬 N-1), 클라이언트가 배치 단위로 서버에 「같은 초안」임을 알리는 한 번의 호출로 접는다.

### F-3. 수정 카드 첨부 경로가 미구현인데 스키마·정리 훅만 서 있다 → 첨부가 **다른 태스크**에 붙는다

- `back/app/schemas/action_runtime.py:103-105` — `TaskUpdateCreateRequest.draft_id` 신설(주석: 「수정 카드도 같은 스테이징을 탄다(OI-4)」).
- 그런데 `back/app/routers/action_runtime_v2.py:1748-1770` `create_task_update_ep` 는 `body.draft_id` 를 **읽지 않고**, `back/app/services/action_runtime/workflow/task_draft/surface.py:201-210` `start_task_update` 에는 파라미터 자체가 없다.
- `definitions.py` `_execute_update`(:258~)는 `attachments.attach_to_task` 를 **부르지 않는다**. 반면 `UPDATE_DEFINITION.on_reject=_discard_staged_attachments`(:503~)는 달려 있다 — payload 에 `draft_id` 가 실릴 일이 없어 **죽은 훅**이다.

부작용이 죽은 필드에 그치지 않는다. `back/app/services/landing_chat/turns.py:170` 이 **모든 발화**에 대해 Redis 바인딩을 심고(TTL 30분), 소비자는 `POST /task-drafts` **하나뿐**이다(`action_runtime_v2.py:1482-1487`). 그래서:

> 파일 첨부 → 「이 태스크 수정해줘」(모델이 `task_update` 툴 호출) → 바인딩이 소비되지 않고 살아남음 → **30분 안의 다음 «생성» 발화**가 그 파일들을 소비해 **엉뚱한 새 태스크에 붙인다**.

같은 이유로 「파일만 올리고 말한 뒤 초안을 안 만든」 경우도 다음 생성 발화에 딸려 들어간다.
⇒ 조치: 최소한 소비 조건을 좁히거나(바인딩에 발화 turn id 를 묶어 1발화 1소비), OI-4 를 실제로 착지시킨다(`start_task_update` → payload → `_execute_update` 의 `attach_to_task`). 미착지로 둘 거라면 `TaskUpdateCreateRequest.draft_id` 와 `UPDATE_DEFINITION.on_reject` 를 함께 걷어야 한다.

---

## WARN 상세

**W-1 · fallback 규칙 두 벌** — BE 는 `back/app/services/action_runtime/tasks/body.py:42-66` 한 곳에서 판정하고 상세·목록 응답에 `body` 를 싣는다(`manual_surface.py` `task_detail`·`decorate_task_rows`). 그런데 FE 는 그 필드를 **쓰지 않고** `front/components/tasks/detail/CanonicalTaskDetail.tsx:395-396` 에서 `current.background ?? (current.goal ? null : current.description)` 로 다시 파생한다. BE 는 공백뿐인 값을 「없음」으로 접지만(`_clean`) FE 는 `??` 라 접지 않아, `background=" "` 인 행에서 두 판정이 갈린다. WP-130 P2 「fallback 렌더 규칙 한 곳 · 표면마다 분기하지 않는다」와 어긋난다. (WBS·채팅 스냅샷은 BE `render_body` 를 쓴다 — 갈리는 것은 FE 하나다.)

**W-2 · 기존 워크플로 태스크의 배경이 빈다** — FE 라이브 렌더가 폐지되고(`DecisionSourceProvider.tsx`·`IncidentSourceProvider.tsx`에서 `background` 슬롯 제거) BE 스냅샷은 **신규 생성분에만** 저장된다. 그 태스크들은 `description` 도 NULL 이라(구 생성 경로가 그 컬럼을 쓰지 않았다) fallback 도 걸리지 않는다 ⇒ 배포 즉시 **기존 decision·incident 태스크 전부가 빈 배경**이 된다. backfill 금지는 계약이므로 코드 결함은 아니나, WP-130 §Pre-deploy 의 공지 항목에 「기존 행은 배경이 사라진다(원문은 참고자료 첫 줄 출처 링크로)」가 **없다** — 추가 필요.

**W-3 · 크기 검사 시점** — `back/app/routers/action_runtime_v2.py` `add_task_reference_ep`·`stage_task_draft_attachment_ep` 가 `content=await upload.read()` 로 전량을 읽은 뒤 서비스가 `guard_size` 를 부른다. `back/app/services/task_reference_storage.py:102-105` docstring 은 「**읽기 전에** 크기를 아는 자리에서 부른다(메모리에 다 올린 뒤가 아니라)」라고 적어 두었다. 25MB 상한이 **저장**은 막지만 **수신**은 막지 못한다(starlette 스풀 파일로 디스크에 떨어진다). 계약 위반은 아니고 자기 문서와의 불일치 + 자원 노출.

**W-4 · `draft_id` 소유자 바인딩 0** — 스테이징 endpoint 는 폼의 `draft_id` 를, `POST /task-drafts` 는 body 의 `draft_id` 를 **검증 없이** 받는다. `attachments.py:9-14` 모듈 docstring 은 「클라이언트가 지어낸 id 를 받지 않는 이유는 그것이 곧 남의 스테이징 디렉터리를 지목할 수 있는 입력이기 때문」이라고 적었는데, 실제 코드는 받는다(두 번째 파일부터 필요해서). 실효 방어는 UUID4 추측 불가 하나다. `draft_id` 는 action payload 에 들어가지만 `runs_projection.py:182` 가 payload 를 통째로 노출하지 않아 **확인된 유출 경로는 없다** — 그래서 FAIL 이 아니라 WARN 이다. 문서 문장을 사실에 맞추거나(권장) 소유자 대조를 붙인다.

**W-5 · 메타 스트립** — WP-130 P5 는 「메타 스트립의 요청자 행은 만지지 않는다 · 메타 스트립 diff 0」이었으나, WP-129 P4 가 요청자 행을 넣은 `front/components/tasks/detail/TaskMetaPanel.tsx`(525줄)가 **삭제**되고 `TaskDetailHeaderMeta.tsx` 로 재작성됐다. 기능은 보존(`TaskDetailHeaderMeta.tsx:138-141` — `task.is_request` 게이트 + `requester_name ?? "미확인"`)이나 라벨이 「요청자」→「요청」으로 바뀌었다. v1 시안이 패널을 스트립으로 대체하므로 재작성 자체는 불가피 — OI-1 소유 조정 결과를 문서에 반영하고 라벨 변경을 확인받으면 된다.

**W-6 · `size_bytes` (미결 ⓑ 판정)** — **코드가 옳다.** migration `0138` docstring:34-40 이 근거를 적었고(다운로드 카드 크기 표시가 §4.8 계약 · 조회 시 `stat` 은 N+1 IO 이며 볼륨 미장착 시 거짓 0), 「객체 총계 3」은 그대로다(테이블 내부 컬럼). domains 문서가 스스로 「schema 전문은 코드 SoT」라고 선언했으므로 위반이 아니다. ⇒ **문서 환류 대상**: `domains/runtime_task.md` §`task_references` 표에 `size_bytes | bigint | nullable | 업로드 시점 바이트 수(표시용)` 한 행 추가.

**W-7 · §6.1 「그 턴에 카드를 세우지 않는다」 (미결 ⓐ 판정)** — **코드가 옳다.** `back/app/services/action_runtime/workflow/task_draft/workflow.py:681-689` 가 판단을 명시했다: 이 도메인의 네 경로(생성·재생성·수정·fallback)가 전부 카드를 세우는 구조이고 「어느 입구로 들어왔느냐에 따라 카드가 서기도 안 서기도 하면 그것이 계약 위반」(§6.10a)이다. 그래서 **버전 되묻기와 같은 형태**(`content["body_error"]` → `FACT_BODY` fact)로 착지했고, 유실 금지(fallback 본 면제)도 지켰다. ⇒ **스펙 환류 대상**: SPEC-155 §6.1 의 「그 턴에 카드를 세우지 않고 질문으로 돌려준다」를 「카드에 되묻기 fact 를 실어 그 턴에 이어 채우게 한다(버전 되묻기 동형)」로 정정.

**W-8 · 레포 위생** — 레포 루트에 untracked `node_modules/`(내용은 `.vite` 캐시뿐)가 생겼고 루트 `.gitignore` 에 항목이 없다(현재 `.playwright-mcp/` 한 줄뿐). allowed_paths(`back/`·`front/`·`mcp/`) 밖이고 `git add -A` 로 딸려 들어간다. `.gitignore` 에 `node_modules/` 추가 권장.

**W-9 · 주석 오타** — `back/app/services/task_reference_storage.py:51` 「소문자 비교이고 **마지막 확장자만 보지 않는다**」는 이어지는 설명(`a.exe.txt` 는 통과, `a.txt.exe` 는 차단)과 코드(`os.path.splitext(...)[1]`)가 말하는 **마지막 확장자만 본다**의 반대다. 코드는 정상.

---

## PASS 근거 (체크리스트 항목별)

**1. migration 3객체 · 스키마 일치 — PASS**
`back/alembic/versions/0138_task_body_and_references.py:71-110` — `add_column("tasks","background")`·`add_column("tasks","goal")`·`create_table("task_references")` **정확히 3**. 인덱스 신설 0(0137 이 WP-129 몫). `downgrade` 대칭(:113-116). 스키마가 domains 표와 일치: `role`×`kind` Text + 앱 enum(`models/action_runtime.py` `TASK_REFERENCE_ROLES`/`KINDS`), `task_id` FK CASCADE, `created_by_member_id` NOT NULL·FK 없음(커널 분리), `deleted_at` soft delete, `kind ↔ url/file_path` 정합을 **DB CHECK** 가 지킨다(`ck_task_references_kind_path`). 잠입 스키마 변경 0. 회귀 테스트 `back/tests/migrations/test_0138_task_body_and_references.py`(총계·왕복·backfill 부재).

**2. 완료 422 술어 — PASS**
`lifecycle.py:141-175` `guard_completion_evidence` — 근거 = 완료기록 **또는** `role=deliverable` 1건(`task_reference_repo.has_deliverable`, `LIMIT 1`). 검사 순서가 계약대로다(`lifecycle.py:230-245`): `guard_stale_write` → `machine.precheck`(쓰지 않는 자격·합법성 — `machine.py:132-159` 신설, `transition()` 도 같은 함수를 지나 두 벌이 안 된다) → **근거 검사** → `machine.transition`(스탬프·상태) → `complete_open_check_items`. ⇒ 422 로 거절된 전이는 상태·스탬프·체크 항목을 **하나도** 건드리지 않는다. 시스템 면제는 `TaskMachine._event` 와 **같은 축**(`actor.id is None`)이라 이벤트의 `actor_kind` 와 판정이 갈리지 않는다. `canceled` 는 `target is DONE` 가드로 제외. 파생(`apply_derived_transition`)은 OI-2 기본 제안대로 면제이고 근거를 docstring 에 남겼다.
사람 경로 전수: 웹 상세(`manual_surface.transition_task:976` `completion_note=comment`) · run 하위(`tasks_surface.patch_task:390` 동일) · WBS 칩(`version_wbs.py:1312` `req.completionNote`) · 채팅/MCP(`task_draft/surface.py:756-765` → `TaskCompletionEvidenceRequired` 422 문장 번역, `mcp/app/tools/task_lifecycle.py:52-62` 문서화). **우회 경로 없음** — 전부 같은 seam 을 지난다. `map_machine_error`(`lifecycle.py:77-87`)가 미지 예외를 그대로 돌려주므로 `map_errors=True` 에서도 422 가 보존된다.

**3. storage — PASS**
`back/app/services/storage_guard.py` 는 `department_space_storage` 의 판정을 **그대로 들어낸 것**이고(diff 상 로직 동일), 부서 문서 모듈은 `_safe_abs_path = safe_abs_path(_root(), ...)` 위임 + 이름 재수출만 남는다 ⇒ **신규 구현 0**. `UnsafePathError` 가 `DepartmentSpaceStorageError` 하위에서 빠졌으나 그것을 base 로 잡는 호출부는 없다(전수 확인). 25MB(`MAX_FILE_BYTES`) · denylist 39종(OI-3 확정) · 다운로드 `Content-Disposition: attachment` **상수 고정** + `Content-Type: application/octet-stream` 고정(`action_runtime_v2.py` `download_task_reference_ep`) — 이미지도 예외 없음. DB 에는 상대경로만(`references.py:190-191`), `project()` 는 `file_path` 를 응답에 **싣지 않는다**. 출처 행 저장 0(테이블에 쓰는 자리 없음 — 화면이 `referenceSource` 로 그린다). 회귀 테스트 `test_wp130_task_detail_unification.py:460-536`(denylist·크기·traversal·NFC·symlink 무관 판정).

**4. 원장 렌더 폐지 대체 — PASS (W-1·W-2 단서)**
decision 은 흐름별 슬롯 표(`decision/body_snapshot.py:42-62` — `instruction` 의 `why_blocked` 를 **목표** 자리로 보내는 자리가 정확하다), incident 는 추적/fanout 두 자리(`incident/body_snapshot.py`). 형식 규칙은 `tasks/snapshot.compose` **한 벌**. 체크리스트는 종전대로 `checklist_items` 로 실제 항목이 저장된다(라이브 렌더 대상이 아니었다). FE 라이브 렌더는 양쪽 provider 에서 제거됐고 출처는 참고자료 첫 줄 링크로 대체.

**5. FE 상세/보드 — PASS**
2단 셸 `TaskDetailShell.tsx:135-157`(본문 `flex-1 min-w-0` · 레일 `lg:w-[320px] shrink-0` · 각자 스크롤 · <1024 단일 컬럼), 레일에 전이 조작 없음(`TaskDetailRail.tsx` — `sourceRow`/자료/일정만). 완료 모달 활성 조건 `TaskCompletionModal.tsx:93` `summary.trim() || deliverables.length > 0` — **서버 술어와 동형**, `*` 표식 없음, 미체크 경고는 `role="status"` 문구일 뿐 버튼을 막지 않는다. 사유 모달 공용화 — 보드의 로컬 모달이 삭제되고 `components/tasks/TaskReasonModal` 한 벌로 수렴(kanban diff). 월 필터는 **프론트 파생**(`task-kanban.tsx` `tasksInColumn` — `done` 만 걸고 `completed_at` 없는 레거시는 어느 월에서도 숨기지 않음, API 파라미터 신설 0). 드롭다운 모집단은 서버 `allowed_transitions` 그대로. 출처 마커 5값 유지(시안 2값으로 접지 않음). D-3 파생은 `front/lib/tasks/task-due.ts` **한 곳**을 보드·테이블·헤더 pill 이 공유하고 응답에 `overdue`/`urgent` 필드 없음. 인라인은 이미지 확장자 allowlist 만(`task-references.ts:66-72`, 서버 `is_inline_image` 와 동형). `/ax/tasks` 에 요청 축 진입 0(`scope=requested` 소비처 없음). 역할별 게이팅 0 — `canAddReference`/`canDeleteReference` 는 `manual_surface._task_permissions` 에서 **쓰기 가시성 하나**로 같은 값을 낸다(키만 미리 세움).

**6. 채팅 — PASS(필수 채움·매핑) / FAIL(첨부 — F-2·F-3)**
필수 채움: 프롬프트 `REQUIRED` + `provider.missing_body_fields` 판정 → `body_error` fact(카드 되묻기), fallback 본은 면제. `purpose` → `goal` 개명이 산출 스키마·프롬프트·diff 키·카드 슬롯 전부에 반영됐고, **구 키 읽기 호환**이 남아 있다(`front/lib/ax-task.ts` `TASK_DIFF_KEYS`/`TASK_DIFF_LABELS` 에 `purpose` 유지 — 개명 전 카드가 아무것도 안 그리는 결함을 막는다). `description` 합침(`compose_description`)·역파싱(`split_description`) 둘 다 제거됐고 `_target_as_proposal` 은 기계 분할 없이 두 자리를 그대로 읽는다. `extra="forbid"` 보존 확인(`schemas/landing_chat.py:38`), 첨부 없으면 `draft_id` 키 자체를 안 싣는다. 승인 귀속은 `_execute_draft` 의 **같은 SAVEPOINT**(`attach_to_task` → 이동 실패 시 태스크까지 롤백), 거절은 `on_reject` 정리, 재생성은 스테이징을 건드리지 않는다.

**7. WBS 완료 모달 — PASS**
`WbsGanttEmbed.tsx` `onStatusChange` — `status === "done" && task.originTaskId` 일 때만 모달을 지나고(phase·canonical 미연결 legacy 행은 그대로 `sendStatusChange`), 모달은 상세·보드와 **같은 컴포넌트**다. `completionNote` 는 canonical 전이의 `comment` 와 **같은 축**(`schemas/version_wbs.py` `WbsTaskPatchRequest.completionNote` → `version_wbs.py:1312` → seam). 값이 비면 키를 안 보내 산출물 단독 완료가 그대로 통과한다.

**8. allowed_paths · 계층 — PASS (W-8 단서)**
코드 변경은 `back/`·`mcp/`·`front/` 안에만 있다. `back/app/repositories/` 에서 `app.services` 를 import 하는 자리 **0건**(WP-129 W1 재발 없음). 새 repo(`task_reference_repo.py`)는 models·repositories 만 의존하고, tenant 는 부모 `tasks` 조인으로 전이 스코프(`_scoped()` 3겹: tenant · 태스크 삭제 2겹 · 자료 삭제)라 앵커가 한 곳이다.

**9. 상태 축 불변 — PASS**
새 상태·새 `TaskEvent` 값 0 — 완료기록은 `task_completed` payload(`COMPLETION_NOTE_KEY`), 자료 추가·삭제는 기존 `task_edited` 축에 `cause` 로만 갈린다(`references.py:51-52`, `_audit`). 게이트 재도입 0(수락·검수 어휘 신설 없음). 자동 cc 0.
※ 사소: `tasks_surface.create_task` docstring 에 「**수락 게이트가 있는 상태로 태어난다**」 문장이 남아 있다 — 이 diff 이전부터 있던 stale 주석(WP-126 잔재)이고 코드와 무관하다. 지나는 김에 정리 권장.

---

## 요약 조치 목록

1. **(필수)** `back/tests/api/test_version_wbs_checkitem.py` · `back/tests/services/test_version_progress.py` 의 `status=done` PATCH 를 새 계약(`completionNote` 또는 산출물)에 맞춰 갱신하고, 전체 스위트를 다시 돌려 「신규 실패 0」을 실증한다.
2. **(필수)** `LandingChatClient.pickFiles` 다중 선택 경합 수정 — 첫 업로드로 `draft_id` 를 확정한 뒤 나머지를 그 값으로 올린다.
3. **(필수)** 수정 카드 첨부: OI-4 를 착지시키거나(`start_task_update` ~ `_execute_update`), 미착지로 두고 `TaskUpdateCreateRequest.draft_id` + `UPDATE_DEFINITION.on_reject` 를 걷는다. 어느 쪽이든 **Redis 바인딩이 다음 «생성» 발화에 오소비되지 않게** 소비 조건을 좁힌다.
4. (권장) FE 가 BE `body` 를 소비하도록 바꿔 fallback 판정을 한 벌로 되돌린다(W-1).
5. (권장) Pre-deploy 공지에 「기존 decision·incident 태스크의 배경이 빈다」 추가(W-2).
6. (문서) `domains/runtime_task.md` §`task_references` 에 `size_bytes` 행 추가(W-6) · SPEC-155 §6.1 되묻기 문장 정정(W-7).
7. (위생) 루트 `.gitignore` 에 `node_modules/`(W-8) · `task_reference_storage.py:51` 주석 오타(W-9) · `tasks_surface.create_task` stale 주석.

---

# «R2 재검수» — FAIL 3건 정정분 (targeted)

- 일시: 2026-09-01
- 범위: **정정분만** — `backend-130-fix-report.md` + FE(다중첨부 직렬화 · fallback 한 벌 · 인라인 폼 공유 · 헤더 배지 한 줄). read-only, 테스트 실행 없음.
- 방식: 정정 코드를 **직접 읽어** 계약과 대조하고, 「고쳤다」는 주장마다 **그 사실을 고정하는 테스트가 실재하는지**를 파일·함수명으로 확인했다.

## 판정: **PASS**

FAIL 3건이 전부 해소됐고, **정정이 계약을 건드리지 않았다** — 422 술어·전이 순서·migration 총계·상태 축은 R1 이 PASS 로 확인한 그대로다. WARN 처리분 3건(25MB 선검사·fallback 한 벌·인라인 폼 공유)도 실재한다. 남은 것은 전부 문서·배포·위생 축이다.

| # | R1 | R2 | 근거 |
|---|---|---|---|
| F-1 | FAIL | **해소** | 두 파일 갱신 + 422 계약 테스트 신설 |
| F-2 | FAIL | **해소** | 직렬 사슬 + 회귀 테스트 5케이스 |
| F-3 | FAIL | **해소** | 바인딩 3겹 + 수정카드 잔재 제거 + 테스트 5건 |
| W-3 | WARN | **처리** | `guard_declared_size` 선검사 + 테스트 |
| W-1 | WARN | **처리** | FE 가 서버 `body` 를 그대로 렌더 |
| W-9 | WARN | **처리** | 주석 오타 정정 |
| W-2·5·6·7·8 | WARN | **미처리** | 문서·배포·위생 축 (아래 §5) |

---

## 1. F-1 해소 — 새 422 계약이 테스트에 반영됐다

**갱신 확인.**
- `back/tests/api/test_version_wbs_checkitem.py:84-90` — `_status_body(status)` 가 `done` 일 때만 `completionNote` 를 싣는다. `_create_then_status`(:102) · `_patch_status` · 직접 PATCH(:361, :549) **세 자리 전부** 이 헬퍼를 지난다. 파일 전수 grep 결과 헬퍼를 우회하는 `{"status":"done"}` PATCH 는 **:568 하나뿐**이고, 그것이 아래 신설 테스트의 「근거 없는 완료」다.
- `back/tests/services/test_version_progress.py:154` — `_DONE_BODY` 상수, done PATCH 3자리(:226·:270·:304) 전부 소비. 우회 0.
- `_assign`(:49-55)이 `department_org_unit_id=unit.id` 를 명시로 채운다 — 형제 파일(`test_wp104_w3_status_axis`)과 **같은 모양**이고 새 관용을 만들지 않았다.

**「근거 없는 done = 422 + 상태 불변」 계약 테스트 실재.**
`test_done_without_evidence_is_422_and_changes_nothing`(:552-578)이 셋을 한 번에 고정한다: ① 422 ② `error.detail.code == TASK_COMPLETION_EVIDENCE_REQUIRED` ③ **거절 뒤 트리를 다시 읽어** work·phase 가 둘 다 `todo` — 즉 **상태·부모 rollup 이 하나도 안 바뀐다**. 마지막 줄이 「완료기록을 실으면 통과한다」로 닫아 **막는 것이 «완료» 가 아니라 «근거 없는 완료»** 임을 함께 고정한다. 이것이 R1 이 요구한 「WBS 축이 실제로 같은 seam 을 지난다」의 실증이다.

**대조 확인** — 에러 봉투 `error.detail.code` 는 `app/main.py:271` 의 관례와 일치하고 형제 테스트들이 이미 쓰는 모양이다. 상수는 `lifecycle.py:115 COMPLETION_EVIDENCE_REQUIRED = "TASK_COMPLETION_EVIDENCE_REQUIRED"` — 문자열 하드코딩이 아니라 **값이 실제로 같다**.

**BE 의 「20건은 선행 실패」 재분류에 동의한다.** 실패 지점이 `create_task`(생성)이고 이 diff 의 `version_wbs.py` 변경은 `patch_task`·`_transition_linked_task` 둘뿐이라는 사실을 diff 로 확인했다. 다만 **분류가 어떻든 조치는 같았고**(두 파일 안에서 전부 고침) R1 의 요구 — 「이 두 파일이 새 계약으로 지나가게 하라」 — 는 충족됐다. R1 판정 중 「26건 전부가 이 diff 의 신규 실패」라는 부분은 **6건이 맞다**로 정정한다. 「447 passed 가 부분 실행이었다」는 판정은 유지된다.

⚠ 단서: 전체 스위트는 이 라운드에서도 돌지 않았다(영향 파일 163 passed / 1 skipped). **「신규 실패 0」의 최종 실증은 CI 몫**이고, BE 가 §5 에 올린 선행 실패 4건(`test_version_wbs_crud.py` 15건 등)은 CI 가 빨간불이 될 때 **이 라운드와 무관하다는 근거**로 쓰일 좌표다.

## 2. F-2 해소 — 다중 첨부가 한 초안에 묶인다

`front/components/landing-chat/LandingChatClient.tsx:355-424`.

- `runBatch`(:410-422) — 초안 id 가 **확정되기 전에는 `await` 로 한 건씩**, 확정된 뒤에는 남은 전부를 같은 `draft_id` 로 **병렬**. 대기 시간이 첫 한 건에만 붙어 정상 동선을 늦추지 않는다.
- `uploadChainRef`(:358, :423) — **배치 사이에도 사슬**이다. 첫 배치가 resolve 되기 전에 두 번째 선택이 들어와도 겹치지 않는다(R1 이 지적하지 않았던 인접 경합까지 닫았다).
- `uploadOne` 은 **던지지 않는다**(:392-401) — 실패가 그 칩 자리에 사유로 남고 사슬을 끊지 않아, 한 파일의 실패가 나머지를 유실시키지 않는다.
- 전송 성공 시 `setDraftId(null)`(:301) — 발화마다 초안이 갈린다. 「같은 발화 = 한 초안」 계약의 반대편이 맞게 서 있다.

**회귀 테스트 실재** — `front/__tests__/wp130-composer-multi-attach.test.tsx`(230줄, 5케이스). 업로드 스텁이 **서버 규칙을 흉내내고**(`draft_id` 가 오면 재사용, 없으면 새로 발급) `mintedCount()` 로 **발급된 초안 수**를 센다 — 즉 「몇 개의 초안이 생겼나」로 병을 직접 측정한다. 스텁이 `setTimeout(10)` 으로 resolve 를 미뤄 **경합이 실제로 재현되는 조건**을 만든다(0ms 면 이 테스트는 병을 못 잡는다). 5케이스: 2개 동시 · 3개(직렬 1 + 병렬 2) · 연속 두 배치 · 중간 실패 · **첫 건 실패**(그 다음 건이 초안을 세운다). `vitest.config.ts:138` 에 등록돼 **실제로 돈다**(이 레포는 include 화이트리스트라 등록 누락이 곧 미실행이다 — 확인했다).

## 3. F-3 해소 — 바인딩 3겹 + 수정카드 잔재 제거

**① 소유자 fail-closed** — `attachment_binding.claim_owner`/`owner_of`/`owns`(:87-124).
- `owns` 는 `member_id` 가 없거나 기록이 없으면 **False**(:120-124).
- `remember`(:153-156)는 **소유가 확인된 값만** 바인딩으로 세운다 — 기록 없음(TTL 만료·Redis 부재)도 세우지 않는다. 「첨부 0 이 남의 파일보다 낫다」가 코드로 성립한다.
- 업로드 문(`action_runtime_v2.py:1584-1590`)은 **다른 사람 것만** 404(존재 은닉)로 막고 **기록 없음은 통과**시킨다 — 두 자리가 `None` 을 다르게 읽는 것이 의도적이고 docstring(:108-110)이 그 이유를 적었다. 정상 사용자의 두 번째 파일을 막지 않는다.
- ⇒ `attachments.py` 모듈 docstring 의 「클라이언트가 지어낸 id 를 받지 않는다」가 **사실이 됐다**(R1 W-4 해소).

**② room + 발화 교체** — 바인딩 값이 `{"draft_id", "room_id"}` JSON(:158-162). `remember` 호출이 **방 확정 뒤**로 옮겨졌고(`turns.py:186-192`) 403 참조로 접수가 막힌 발화는 바인딩도 안 남긴다. `clear_if_absent=active_turn_id is None`(:190) — 첨부 없는 발화가 앞 바인딩을 지워 오소비 창이 **30분 → 한 발화**. 대기 조각만 예외이고 그 이유(같은 turn 으로 합쳐지므로 지우면 방금 붙인 파일이 사라진다)가 코드·주석 양쪽에 있다.

**③ 생성 흐름 한정 1회성 consume** — `consume`(:167-199)은 `room_id` 가 `None` 이면 **소비하지 않고**, 방이 다르면 **소비도 삭제도 하지 않는다**(그 바인딩은 자기 방에서 쓰일 자격이 있다). 방은 `action_runtime_v2.py:1509-1514` 에서 **MCP 토큰의 turn** 으로 얻는다 — `taint.turn_for_token_jti`(`taint.py:74-85`)는 `mcp_access_jti` 조회일 뿐 **새 식별 축이 아니다**(D19 계약 재사용). body 에 `draft_id` 가 있으면 바인딩을 아예 보지 않는다(「명시가 이긴다」).

**수정카드 잔재 제거 확인.**
- `schemas/action_runtime.py:92-107` — `TaskUpdateCreateRequest` 필드는 `task_id`·`utterance`·`thread_id` **셋뿐**, `draft_id` 없음. docstring 이 왜 없는지·v2 에서 열 때 무엇을 함께 세워야 하는지를 남겼다(반쪽 배선 재발 방지).
- `definitions.py:508` — `UPDATE_DEFINITION` 에 `on_reject` 없음(주석이 이유 명시). `DRAFT_DEFINITION`(:500)의 `on_reject=_discard_staged_attachments` 는 **그대로** — 그쪽은 실제로 payload 에 `draft_id` 가 실리므로 살아 있어야 맞다.
- 호출자 영향 0 — `mcp/app/` 전수 grep 결과 `draft_id` 0건, `front/` 에서 `task-updates` 호출 0건. 필드 제거로 깨지는 호출부가 없다.

**테스트 실재** — `tests/services/engine_v2/test_ax_task_draft.py`: `..._is_remembered_then_consumed_once`(:1256) · `..._refuses_a_draft_owned_by_someone_else`(:1278, victim/attacker 두 축 + 기록 없음 케이스) · `..._is_not_consumed_across_rooms`(:1305, 다른 방 · 방 없음 · 자기 방 세 갈래) · `test_attachment_free_utterance_clears_a_stale_binding`(:1327) · `test_task_update_request_has_no_attachment_field`(:1384).

## 4. 정정이 새 위반을 만들지 않았다

정정 diff 안에서만 확인했다.

- **422 술어 불변** — `guard_completion_evidence`(`lifecycle.py:127-172`)는 R1 이 PASS 로 읽은 그대로다: 근거 = 완료기록 **또는** `role=deliverable` 1건, 시스템 액터 면제 축이 `TaskMachine._event` 와 동일(`actor.id is None`), `canceled` 제외(`target is DONE` 가드). `back/app/services/action_runtime/tasks/lifecycle.py` 는 **+109/-0 순수 additive**.
- **검사 순서 불변** — `apply_user_transition:228-247`: `guard_stale_write` → `machine.precheck` → **근거 검사** → `machine.transition` → `complete_open_check_items`. 422 가 상태·스탬프·체크 항목을 건드리지 않는 순서가 유지되고, 신설 테스트가 그 사실을 밖에서 고정한다.
- **합성 전이** — `todo → in_progress → done` 에서 근거 검사는 `DONE` 다리에만 걸린다. 중간 다리가 422 를 만들지 않는다.
- **migration 총계 불변** — untracked alembic 파일은 `0138` **하나**. 정정 라운드에서 늘지 않았다.
- **상태·이벤트 축 불변** — 새 상태·새 `TaskEvent` 값 0(모델 diff 확인).
- **신규 leaf 0** — 라우터 diff 에 capability/leaf 추가 0. `get_redis`·`person_axis` 는 이미 그 라우터가 쓰던 것이고 `person_axis.resolve`(:228-236)는 미해소 시 **예외 없이 `None`** 이라 새 실패 경로를 만들지 않는다.
- **W-3 선검사가 상한을 대체하지 않는다** — `guard_declared_size`(`task_reference_storage.py:113-130`)는 값이 없거나 숫자가 아니면 **통과**시키고 실제 바이트는 종전 `guard_size` 가 잡는다. multipart 봉투 여유를 둬 정확히 25MB 인 파일이 boundary 때문에 거절되지 않는다. 두 업로드 문 모두 `request.form()` **앞**에서 부른다(`:717-718`, `:1568-1569`).

**관찰 2건(비차단, 정정이 만든 것 아님)**
- **N-1** 대기 조각이 자기 `draft_id` 를 가지면 앞 바인딩을 **덮어쓴다**. 두 발화가 같은 turn 으로 합쳐지는데 바인딩 슬롯은 하나라, 앞 발화의 파일이 고아가 될 수 있다. ⚠ 정정 **이전에도 슬롯은 하나**였으므로 새 위반은 아니고, 창은 R1 대비 좁아졌다. v2 에서 「한 turn = 한 초안」으로 합칠 때 볼 자리.
- **N-2** `remember` 가 큐 상한 거절(`TurnInFlightError`)보다 **앞**이라 거절된 조각도 바인딩을 남긴다. 같은 사람·같은 방이라 **오귀속은 아니고**, 그 파일은 다음 발화에 정상 귀속된다.

## 5. WARN 처리분 확인 · 남은 것

**처리 확인**
- **W-3 (25MB 선검사)** — 위 §4 참조. `test_declared_size_is_checked_before_the_body_is_read`(`test_wp130_task_detail_unification.py:489-504`)가 4개 통과 케이스 + 1개 거절 케이스를 고정한다.
- **W-1 (fallback 한 벌)** — **해소**. `lib/tasks/canonical-task.ts:210-222` 에 `body:{background,goal,source}` 가 서고, :394-408 이 서버 `body` 를 **그대로 옮긴다**(구 배포 응답에는 두 컬럼을 비추기만 하고 **fallback 을 재유도하지 않는다**). `CanonicalTaskDetail.tsx:396·418` 이 `current.body.*` 를 렌더한다 — `background ?? description` 자리가 사라져 공백뿐인 값(`" "`)에서 BE `strip()` 과 FE `??` 가 갈리던 창이 닫혔다. `description`·`background`·`goal` 원장 값은 **수정 폼 전용**으로 남고 그 사실이 타입 주석에 적혀 있다. BE 는 상세·목록 두 자리에서 `render_body` 를 싣는다(`manual_surface.py:624`·`:1261`).
- **인라인 폼 공유 한 벌** — `components/tasks/TaskReferenceList.tsx:198` `TaskReferenceAdder` **한 컴포넌트**를 레일(`TaskDetailRail.tsx:179`)과 완료 모달(`TaskCompletionModal.tsx:211`)이 함께 쓴다. 별도 모달 0(모달 위의 모달이 되지 않는다). 25MB 사전 판정도 그 한 곳(`TASK_REFERENCE_MAX_BYTES`)이고 「정본은 서버」가 주석에 명시됐다.
- **헤더 배지 한 줄** — `TaskDetailHeaderMeta.tsx` 메타 스트립이 **한 줄**이고 값이 없는 항목은 **자리 자체가 없다**(`if (orgs)`·`if (dueInfo)`·`if (task.is_request)`). 요청자 행은 서버 파생 `is_request` 하나로 판정하고 `requester_name ?? "미확인"` 폴백이 보존됐다(WP-129 소유 경계 유지).
- **W-9 (주석 오타)** — `task_reference_storage.py:50-52` 「마지막 확장자만 **본다**」로 정정, 이어지는 설명·코드와 일치.
- **stale 주석** — `tasks_surface.create_task` 의 「수락 게이트」 문장 제거 확인.

**남은 것 (전부 비차단 · 코드 밖)**
- **W-2** Pre-deploy 공지에 「기존 decision·incident 태스크의 배경이 빈다」 — 미추가. **배포 전 필수**.
- **W-5** 메타 스트립 재작성(OI-1 소유 조정) 문서 반영 + 라벨 「요청자」→「요청」 확인받기.
- **W-6** `domains/runtime_task.md` 에 `size_bytes` 행 추가 · **W-7** SPEC-155 §6.1 되묻기 문장 정정 — 둘 다 **코드가 옳고 문서를 고치는** 쪽.
- **W-8** 루트 `.gitignore` 에 `node_modules/` — **미처리**(현재도 `.playwright-mcp/` 한 줄뿐이고 `node_modules/` 가 untracked 로 남아 있다). `git add -A` 사고를 막는 한 줄.

## 6. 결론

R1 이 막았던 세 가지 — **깨진 계약 테스트 · 첨부 유실 · 첨부 오귀속** — 이 전부 닫혔고, 각각을 **밖에서 고정하는 테스트**가 실재한다. 정정은 계약을 넓히지 않았고(422 술어·전이 순서·migration·상태 축·leaf 전부 불변) 새 실패 경로를 만들지 않았다. **PASS.**

⚠ 병합 전 두 가지: ① **전체 스위트 CI 한 번**(「신규 실패 0」의 최종 실증 — 이 라운드도 영향 파일만 돌았다) ② **W-2 배포 공지**.
