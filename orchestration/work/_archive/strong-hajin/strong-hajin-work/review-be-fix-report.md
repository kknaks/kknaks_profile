# [reviewer] WORK-003 BE F-1/F-2 수정 재검수 (read-only)

작성: 2026-09-20 · 워크트리 `/Users/kknaks/orca/workspaces/Strong_hajin/strong-hajin-work`
(브랜치 `kknaksss/strong-hajin-work`, 미커밋) · **소스와 diff만 읽었다. 코드·테스트·문서·inventory 를
한 줄도 고치지 않았고 테스트·빌드·DB·E2E 를 실행하지 않았다.**

## 0. 판정

| # | 항목 | 판정 |
|---|---|---|
| 1 | F-1 — 요청 자료 업로드 행의 `verified` 철회 · override 잔재 없음 · 기존 evidence intent 미확대 | **PASS** |
| 2 | F-2 — 레거시 첨부 열기가 링크에서 500 대신 기존 client error · 파일 내려받기 불변 · 회귀 테스트 존재/범위 | **PASS** |
| 3 | allowed path · 테스트 범위 | **PASS** (수치는 미검증 — W-1) |
| 4 | 남은 기존 위험 기록 | **WARN** (W-1 · W-2 · W-3) |

**전체: PASS.** 지난 리뷰의 FAIL 2건은 **둘 다 닫혔다.** 새로 생긴 FAIL 은 없다.

---

## 1. F-1 — AX 매핑 · **PASS**

### 1-1. inventory 행이 E2 `excluded` 로 내려왔다

`docs/unified-operations-inventory.json` 의 `POST /api/work-requests/{request_id}/materials` 행:

- `"policy": "E2"`, `"status": "excluded"`, `"target_tools": []` — 지난 리뷰의
  `verified` + `["file_attachment_request"]` 가 사라졌다.
- `exclusion` 4필드가 모두 채워져 있고 **사실과 맞는다**: 사유가 「`file_attachment_request` 의 intent
  목록에 `request_material` 이 없고 work_request 대상 업로드는 `request_comment_attachment` 가 아니면
  전부 `add_evidence` 로 떨어진다」로, 내가 지난 리뷰에서 읽은 코드 경로와 같은 말이다.
- `reconsider_when` 이 되돌릴 조건을 **검증 가능하게** 적었다: 「`BrowserFileRequest` 에
  `request_material` intent 가 생기고 `authorize`·`upload` 가 요청 자료 서비스로 연결·인가될 때」.
- `acceptance_evidence` 는 `excluded` 행이므로 요구되지 않는다
  (`backend/tests/architecture/test_operation_inventory.py:206`).

### 1-2. override 잔재 없음

- `backend/src/ax_workspace/bootstrap/operation_inventory.py` 에 `work-requests/.../materials` 항목이
  **없다**(전수 grep 결과 남은 `materials` override 는 meetings 2 · material-folders 1 · tasks 1 뿐,
  `operation_inventory.py:16,22,24,36,52`).
- 이 파일은 `git status` 의 변경 목록에서 아예 빠졌다 — 즉 `HEAD` 와 동일해졌고, 이번 수정이
  **추가했던 한 줄만** 되돌렸다. 기존 WORK-003 override 두 줄(`POST /api/tasks`,
  `GET /api/tasks/{task_id}/children`)은 HEAD 에 이미 있어 그대로다.
- architecture 테스트의 `HTTP_TOOL_TARGET_OVERRIDES.keys() <= routes(verified)`
  (`test_operation_inventory.py:232`)는 override 와 행이 **함께** 내려갔으므로 그대로 성립한다.

### 1-3. 기존 evidence intent 를 넓히지 않았다

- `BrowserFileRequest.intent` 는 그대로다 —
  `Literal['task_material','meeting_material','meeting_material_replace','folder_material',
  'request_evidence','request_comment_attachment','action_material']`
  (`backend/src/ax_workspace/modules/ax_execution/browser_interactions.py:42`). `request_material` 을
  **만들지 않았다**(브리프 범위 밖의 확장을 하지 않은 것이 맞다).
- 업로드 분기도 그대로다(`backend/src/ax_workspace/bootstrap/browser_interactions.py:143-146`):
  `request_comment_attachment` → `attach_to_comment`, 그 외 work_request → `add_evidence`.
- `POST /api/work-requests/{request_id}/evidence` 행은 `verified` +
  `target_tools: ["file_attachment_request"]` 로 **손대지 않았다** — 그 행은 intent 가 실제로 있으므로
  여전히 참이다. override 도 그대로다(`operation_inventory.py:59`).

### 1-4. 한쪽만 고치는 길을 닫는 가드 테스트가 새로 있다

`backend/tests/unit/test_request_material_ax_mapping.py` (신규 1함수):

- intent 가 **없는 동안**에는 그 행이 `excluded` · `target_tools == []` · `reconsider_when` 존재임을
  단언한다(`:39-45`).
- intent 가 **생기면** 같은 시험이 「이제 `verified` 로 되돌려라」를 단언한다(`:35-38`) — 코드와
  inventory 가 갈라지는 순간 실패한다. 지난 리뷰가 지적한 「override 가 자기 자신을 증명한다」는
  공백을 **실제 런타임 enum 으로** 메운다(`get_args(BrowserFileRequest.model_fields["intent"])`).
- 「evidence 로 떨어진다」는 사실 자체도 함께 못 박는다(`:46-47`).

### 1-5. inventory 전체 정합(정적 대조, 테스트 실행 아님)

지난 리뷰와 같은 AST 대조식(`test_operation_inventory.py::test_inventory_includes_each_declared_http_operation`
· `::test_final_inventory_has_no_implicit_or_unverified_product_surface` 의 검사 내용)을 그대로 재현:

```
routes(런타임 AST) 156 · inventory rows 156 · 키 156
runtime-only: []   inventory-only: []   field mismatches: 0
http_count == 156 ✓
verified 행 필수필드 누락: []   excluded 행 exclusion 4필드 누락: []
tool_acceptance == registered tools (129 == 129) ✓   tool_count == 129 ✓
```

→ **drift 0.** 행이 `verified`→`excluded` 로 바뀌었어도 `http_count`·`tool_count` 는 그대로다
(도구를 만들지도 지우지도 않았으므로 맞다).

---

## 2. F-2 — 레거시 첨부 열기 · **PASS**

### 2-1. 가드가 들어갔고, 새 경로와 **같은 예외**다

`backend/src/ax_workspace/modules/work/requests.py:1045-1051`:

```
if attachment is None:
    raise MaterialNotFound("attachment was not found")
# (주석: 요청 자료가 이 목록에 서면서 링크도 닿게 됐고, 링크의 source_ref 는 주소이지 storage key 가 아니다)
if attachment.source_kind != "file":
    raise MaterialError("only file attachments have downloadable content")
return _attachment_view(attachment), self._storage.get(attachment.source_ref)
```

- `open_material`(`requests.py:866-867`)이 쓰는 문구·예외와 **글자까지 같다** → 두 입구가 같은 사실을
  같은 코드로 말한다.
- `MaterialError` 는 `TaskError` 하위(`modules/work/material_values.py:18`)라
  `_runtime_error` 에서 **422** 로 나간다(`backend/src/ax_workspace/entrypoints/http.py:555`).
  `MaterialNotFound`(404) 분기가 그보다 위에 있어 순서도 그대로다(`http.py:516`).
- **기존 client error 를 쓴다** — 새 예외 타입이나 새 매핑 분기를 만들지 않았다. `_runtime_error`
  변경 0.

### 2-2. 파일 내려받기는 그대로다

- 가드는 `source_kind != "file"` 만 거른다. `store_file` 이 만든 첨부(요청 자료 파일 · 댓글 첨부 ·
  evidence)는 전부 `source_kind == "file"` 이므로 영향이 없고, `return` 줄은 손대지 않았다
  (`requests.py:1051`).
- purged 자료는 `material_bindings` 가 이미 걸러 이 자리에 오지 않는다(`requests.py:1033-1034`).

### 2-3. 회귀 테스트가 있고 범위가 좁다

`backend/tests/contract/test_work_request_materials.py:158-181`
(`test_a_request_link_opened_through_the_legacy_attachment_path_is_refused_not_a_server_error`,
신규 1함수) 가 세 줄을 한 번에 고정한다:

1. 링크를 레거시 경로로 열면 **422**(`:176-177`) — 500 이 아니다.
2. 같은 요청의 **파일은 200 + 원본 바이트**(`:179-180`) — 가드가 내려받기를 막지 않았다.
3. 새 요청 자료 경로도 같은 422(`:181`) — 두 입구가 갈리지 않는다.

기존 4함수는 diff 없이 그대로이고, 전수 조합·중복 케이스를 늘리지 않았다.

---

## 3. allowed path · 테스트 범위 · **PASS** (수치 미검증)

- 이번 수정이 닿은 파일: `backend/src/ax_workspace/modules/work/requests.py`(가드 1곳),
  `backend/src/ax_workspace/bootstrap/operation_inventory.py`(override 1줄 제거 → HEAD 와 동일),
  `docs/unified-operations-inventory.json`(행 1개 상태 전환),
  `backend/tests/contract/test_work_request_materials.py`(+1함수),
  `backend/tests/unit/test_request_material_ax_mapping.py`(신규). **전부 허용 경로 안이다.**
- `frontend/`·`para/`·`orchestration/`·`docs/domain-model.md`·migration 변경 0. 새 테이블·스키마 변경 0.
- 새 테스트는 브리프가 말한 **두 초점 회귀 + inventory 가드** 정확히 그 셋이다. 그 밖의 테스트를
  늘리거나 고치지 않았다.
- **W-1 (WARN)** — 워커가 보고한 통과 수치는 **이 리뷰가 재현하지 않았다.** 이 검수는 테스트를 한 건도
  실행하지 않았으므로 모든 수치는 **미검증**으로 기록한다. 위 §1-5 의 대조는 테스트 실행이 아니라
  inventory JSON 과 `http.py` AST 의 정적 비교다.

---

## 4. 남은 기존 위험 (재개 아님 · 기록만)

- **W-2 — 기존 contract 4 failed 는 그대로 미해결이다.** `test_material_worker_recovery` 2 ·
  `test_material_search` 2. 이번 수정은 이 넷을 건드리지 않았고, 지난 리뷰가 코드로 좁힌 결론
  (「요청을 한 건도 만들지 않는 시험이라 이번 변경 때문일 가능성은 낮다 — 그러나 배제하지 못했다」)이
  그대로 유효하다. 확정에는 여전히 baseline 비교가 필요하다.
- **W-3 — checkout 사고는 사실로 남는다.** 복구는 지난 리뷰에서 현재 파일로 확인했고, 이번 §1-5 의
  drift 0 이 그 상태가 유지됨을 다시 보여 준다. 다만 **MCP 도구 스키마 전수 일치**
  (`test_inventory_schemas_match_the_actual_registered_tools`)는 런타임 기동이 필요해 이번에도
  확인하지 않았다 — 여전히 미검증이다.
- 지난 리뷰의 W-2~W-7(요청당 +4 쿼리 N+1 · 자료 경로만 행 잠금 없음 · 입양이 task version/활동
  미기록 · 승격 확인경로 테스트 공백 · 보고서 문구 2곳 · 죽은 코드
  `WorkRequestMaterialLinkCommand`)은 **이번 브리프 범위 밖**이라 열지 않았다. 코드상 그대로 남아 있다.

---

## 5. 이 리뷰가 확인하지 못한 것

- 테스트 실행 0. 워커 보고 수치는 전부 미검증(W-1).
- MCP 도구 스키마 런타임 대조 미실시(W-3).
- 기존 4 failed 미재현(W-2).
