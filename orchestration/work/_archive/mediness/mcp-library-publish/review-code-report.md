# 리뷰 리포트 — mcp-library-publish / backend 리뷰 (2026-08-28)

## 판정: PASS (경미 3건 · 위반 0건)

WP-123 4 phase 전량이 계약대로 착지했다. **웹 발행 3 endpoint 는 바이트 단위로 무변경**이고, 신규 라우트·툴 어느 쪽도 화이트리스트·slug·frontmatter·`publish_lock`·git 을 재구현하지 않았다. 계약값(leaf 이름 · `system_admin` 단독 · 256 KiB 경계 · `upload|update` · 400 코드 재사용 · `delete` 부재)은 6/6 일치. migration 0134 는 선례 0095 와 동형이고 down_revision 이 실측 head 와 맞다. 경미 3건은 전부 판정 제외 수준이며 수정 재발주 사유가 아니다.

---

## 검수 범위

- **diff**: `git diff origin/dev...HEAD` = **빈 diff** — 작업은 **워크트리에 미커밋 상태**로 남아 있다(워커 브리프 §9 「커밋 금지」대로). 따라서 실제 검수 범위는 `git diff`(수정 12) + `git status --porcelain`(untracked 5) = **17파일** — back 9 · mcp 8. 브리프 예상치와 일치.
  - back(9): `app/routers/baseline_publish.py` · `app/schemas/baseline_publish.py` · `app/services/publish/baseline_form.py` · `alembic/versions/0134_baseline_publish_agent.py`(신규) · `tests/api/test_baseline_agent_publish.py`(신규) · `tests/migrations/test_0134_baseline_publish_agent.py`(신규) · `tests/api/test_capability_catalog.py` · `tests/api/test_capability_resolver.py` · `tests/api/test_me_capabilities.py`
  - mcp(8): `app/tools/baseline_publish.py`(신규) · `app/server.py` · `tests/test_wp123_baseline_publish_tool.py`(신규) · `tests/test_tool_inventory.py` · `tests/test_wp116_taint_policy.py` · `tests/test_wp116_tools_list_filter.py` · `tests/test_read_file_offset.py` · `tests/test_wbs_tools.py`
- **allowed_paths 대조**: 17파일 전부 `back/` 또는 `mcp/` 안. `docker-compose.yml`·`docker-compose.local.yml` 은 무변경(허용 범위였으나 손대지 않음). **이탈 0 → rules.md 공통 4번 FAIL 조건 미해당.**
- **실행한 검사** (전부 read-only — 브리프 지시대로 **테스트 미실행**)
  - `git diff` / `git status --porcelain` / `git show HEAD:<file>` 로 원본 대조
  - 웹 3 핸들러 **바이트 대조**: `git show HEAD:back/app/routers/baseline_publish.py` 에서 `@router.post("/baseline/publishes")` 이후 전량을 잘라 현재본과 `diff` → **차이 0줄**(후행 공백줄 2개는 슬라이싱 산물)
  - 계층 위반 grep: 신규 라우터에 `session.execute` / `select(` 직접 호출 부재 확인
  - 인벤토리 상수 grep: `grep -rn "== 60\|== 61\|len(tools) ==\|len(registered) ==\|\"tools\": 6" mcp/tests mcp/app` → 잔존 `60` **0건**
  - back 쪽 MCP 툴 카운트 하드코딩 grep → **없음**(갱신 대상 아님)
  - alembic head 실측: `alembic/versions/*.py` 의 `revision`/`down_revision` 전수 → head = `0133_landing_turn_taint`
  - 선재 실패 원인 정적 대조: `grep -rn "action.runtime.read_all" back/alembic/versions back/tests/api/test_capability_{catalog,resolver}.py`
  - **미실행**: `ruff check`(두 리포 모두 `ruff` 바이너리 미설치 — `command not found`). 다만 `pyproject.toml` 양쪽 모두 `ignore = ["E501"]` 이라 장문 라인은 애초에 위반이 아니고, `F`(미사용 import)·`I`(isort)는 눈으로 대조해 문제 없음(아래 «확인한 것» ⑨).

---

## 위반 (FAIL 사유)

**없음.**

---

## 경미 (WARN)

### W-1. `content` 전문이 `audit_log.params` 에 그대로 적재된다 — 워커 자신이 적은 규범과 어긋난다

- `mcp/app/server.py:668-680` — `_wrap_write_tool("mediness.baseline_publish", {... "content": content ...}, ...)`
- 경로: `_wrap_write_tool` → `_wrap_tool`(`server.py:485`) → `_audit_fire_and_forget(tool_name, params, ...)`(`server.py:357-373`) → `push_audit(params=params)`(`mcp/app/audit.py:13-35`) → back `audit_log.params`(`back/app/models/audit_log.py:21`, `JSONB NOT NULL`). **params 는 어디서도 절삭·마스킹되지 않는다** — `result_summary` 만 `[:500]` 으로 잘린다.
- ⇒ 발행 1건마다 **최대 256 KiB 의 문서 전문**이 `audit_log` 에 복제된다.
- 근거: 같은 diff 의 `mcp/app/server.py:222-225` 에 워커가 직접 적은 규범 — 「⚠ **본문은 넣지 않는다** — 감사 원장에 문서 전문을 쌓지 않는다(기존 관례)」. 그 규범을 `result_summary` 에만 적용하고 `params` 에는 적용하지 않았다. 리포 선례로는 `mcp/app/audit.py:56-64`(`push_taint_decision`) 이 「params 를 싣지 않는다 — 사유이지 payload 덤프가 아니다」로 같은 결을 명문화하고 있다.
- ⚠ **단정하지 않는 이유**: SPEC-013 §3 ▸ 감사는 audit 통로가 남기는 것을 「`sub`·tool 명·**params**·result_summary·latency」로 **명시**하고 있어, params 적재 자체는 계약이 요구한 동작이다. 「본문만 빼라」는 조항은 어디에도 없다. 즉 **계약 위반이 아니고, 규범 충돌**이다.
- 권장: 판단은 코디네이터/planner 몫. 손댄다면 `mcp/app/server.py` 의 params 조립에서 `content` 만 길이 요약(`{"content_bytes": len(...)}`)으로 치환하는 한 줄이고, 이는 **SPEC-060 §4 audit 규약을 건드리는 변경**이라 WP-123 범위 밖으로 보는 것이 타당하다. → **후속 별건 발주 후보**로 기장 권고.

### W-2. 256 KiB 판정 위치가 WP-123 §Code Surface 표와 다르다 (문서 쪽이 부정확)

- `back/app/routers/baseline_publish.py:289-293` 에서 판정하고, 상수 `AGENT_CONTENT_MAX_BYTES` 는 `back/app/services/publish/baseline_form.py:30`.
- WP-123 §Code Surface `back/app/schemas/baseline_publish.py` 행은 「**256 KiB 판정 자리**」라고 적었다. 같은 표의 `baseline_form.py` 행은 「**상한 상수도 여기**」라고 적어 **표 자체가 두 자리를 가리킨다**.
- 구현이 라우터를 고른 근거는 `back/app/schemas/baseline_publish.py:36-38` 에 명시돼 있다 — 「enum 을 `Literal` 로 박지 않는다 — 계약이 「그 외 값 → **400**」인데(§3 Validation) pydantic 이 걸면 **422** 가 나간다」. 상한도 pydantic `max_length` 로 두면 같은 이유로 422 가 된다. **계약(400)이 schema 층 판정을 배제하므로 현 위치가 옳다.**
- 근거: SPEC-013 §3 Validation `content`(agent 경로) 행 + 케이스 매트릭스 `CONTENT_TOO_LARGE` = 400.
- 권장: 코드 수정 **불필요**. WP-123 Code Surface 의 schema 행 문구(「256 KiB 판정 자리」)를 planner 가 정정하는 쪽이 맞다. → **planner 후속 항목**.

### W-3. `_parse_error` / `_raise_for_error` 가 `wbs_common.py` 와 거의 축자 중복 — 다만 **리포 기존 패턴**이라 위반으로 세지 않는다

- `mcp/app/tools/baseline_publish.py:52-114` ↔ `mcp/app/tools/wbs_common.py:47-110`(`parse_error`·`_required_capability`·`raise_for_error`). 401/403/404/400·422/기타 분기 구조와 `detail` 조립이 사실상 동형이다.
- 다만 `mcp/app/tools/runtime_common.py:82` 에도 **또 하나의 독립 사본**이 있고, 각 사본의 409 처리·401 메시지·not_found 문구가 도메인 SPEC 의 에러 번역표에 따라 다르다. 즉 **도메인별 사본이 이 리포의 기존 관행**이다(선례 2건). 이 툴의 409 는 「항상 `ValidationError`」로 wbs 의 「코드 화이트리스트 조건부」와 실제로 다르므로 `wbs_common.raise_for_error` 를 그대로 부를 수도 없다.
- 근거: reviewer `rules.md` backend §재사용 vs 리포 기존 패턴 — **패턴 쪽이 우세.** 위반으로 세지 않는다.
- 권장: 없음. 사본이 4개째가 되면 그때 공통화가 별건 후보다(현재 3개).

---

## 특별 검수 항목 (브리프 §특별 검수 1~6)

### 1. 웹 발행 무변경 계약 — **통과 (diff 0 을 바이트로 실증)**

- `upload_baseline`(`:177-205`) · `update_baseline`(`:208-232`) · `delete_baseline`(`:235-257`) — HEAD 판과 **한 글자도 다르지 않다.** 시그니처·`_Capability` 의존·`_publish_form(...)` 호출 인자·`try/except`·응답 모두 동일.
- 어댑터 추출의 동작 보존성:
  - 구 `_publish_form` 본문 = `raw = await file.read()` → `prepare_upload(..., raw_content=raw, filename=file.filename)` → `publisher.publish(...)` → `_last_publish_row`.
  - 신 `_publish_bytes`(`:96-141`) 는 그 본문에서 **첫 줄만 빠진 것**이고, 신 `_publish_form`(`:144-174`) 이 `raw=await file.read(), filename=file.filename` 을 채워 넘긴다. 전부 keyword-only 인자라 순서 영향 없음.
  - `prepare_upload` 는 `filename` 을 **확장자 추출에만** 쓴다(`baseline_form.py:262` `_ext_from_filename(filename)`) — stem 은 사용처가 없다. 따라서 agent 경로의 `f"agent.{format}"` 합성이 웹과 동일 분기를 탄다.
  - `except AppError: raise` / `except GitError: _git_error_to_http(exc)` 순서·의미 불변.
- ⇒ **동작 변화 지점 0.** FAIL 근거 없음.

### 2. 재구현 부재 — **통과**

- **back 라우트**: 신규 핸들러(`:260-307`)가 하는 일은 ① `operation`·`format` enum 판정 ② UTF-8 인코딩 + 상한 판정 ③ `filename` 합성 — 이 셋뿐이고 그 뒤는 `_publish_bytes` 로 들어간다. 화이트리스트 regex·slug·frontmatter·`publish_lock`·git 코드가 라우터에 **한 줄도 없다**. `baseline_publisher.py` · `base_publisher.py` · `git_client.py` 는 **diff 자체에 없다**(무변경 확인).
- **`baseline_form.py`**: 추가된 것은 상수 1개 + `AppError` 서브클래스 1개뿐(`:23-30`, `:81-90`). `prepare_upload` 본문 무변경 — diff 의 해당 hunk 가 파일 상단·에러 정의부에만 걸린다.
- **MCP 툴**: 상한 숫자·경로 규칙이 **숨어 있지 않다.** `mcp/app/tools/baseline_publish.py` 전문을 읽어 확인했고, 신규 테스트가 이를 AST 로 못박는다 — `tests/test_wp123_baseline_publish_tool.py:267-281` 이 docstring·주석을 제거한 소스에서 `262144` · `256 * 1024` · `len(content)` 부재를 단언한다. 화이트리스트 regex·`00-baseline` 부모 검사·존재 검증(409)도 툴에 없고 back 응답을 옮기기만 한다(`:283-292`, `:315-323`).
- 툴의 선검증은 **필수 필드 presence + enum** 뿐(`_require`·`_require_enum`, `:117-128`) — WP-123 P3 이 명시적으로 허용한 범위.
- 값 왜곡 없음: `_require` 가 `.strip()` 한 값을 보내지만, `prepare_upload`/`slugify`(`baseline_form.py:101`)가 이미 `title.strip()`·`version.strip()` 을 하므로 **두 문의 결과가 갈리지 않는다**(확인함).

### 3. 계약값 일치 — **6/6 통과**

| 계약값 | SoT | 코드 | 판정 |
|---|---|---|---|
| leaf 이름 `baseline.publish.agent` | SPEC-013 §3 권한 표 | `0134_...py:_CAPABILITY_KEY` · `routers/baseline_publish.py:79` · `server.py:647` — **세 자리 모두 동일 문자열** | ✅ |
| `system_admin` 단독 부여 | SPEC-013 §3 역할 매트릭스(6역할 중 O 1개) | migration 의 `_ROLE_KEY = "system_admin"` 1행만. 테스트 3중 고정 — `test_0134:56-60`(migration 층) · `test_capability_resolver:369-383`(resolver 층, 5역할 음성 단언) · `test_baseline_agent_publish:494-509`(DB 원장 층 `roles == {"system_admin"}`) | ✅ |
| 256 KiB **경계 포함** | SPEC-013 §3 ▸ 본문 전달과 상한 | `AGENT_CONTENT_MAX_BYTES = 256 * 1024`, 판정 `if len(raw) > ...`(`:290`) — `>` 이지 `>=` 아님. 경계 테스트 있음: `test_baseline_agent_publish:381-387`(정확히 상한 = 200) + `:370-379`(초과 = 400) | ✅ |
| `upload`\|`update` 만 | SPEC-013 §3 ▸ operation 범위 | `_AGENT_OPERATIONS = ("upload", "update")`(`:83`) · 툴 `OPERATIONS`(`tools/baseline_publish.py:44`) | ✅ |
| 400 코드 재사용(신규 발명 0) | SPEC-013 §3 케이스 매트릭스 | enum 위반 → 기존 `ValidationError`(`core/errors.py:294-297`, `VALIDATION_ERROR`/400) 재사용. **신규 코드는 `CONTENT_TOO_LARGE` 하나뿐이고 그것은 계약이 신설을 명시한 코드**다. MCP 403 도 기존 `PERMISSION_DENIED` 재사용 — OPEN-060-C 우회용 도메인 코드 발명 **없음**(`tools/baseline_publish.py:64-79` 주석이 그 판단을 명기) | ✅ |
| `delete` 부재 | SPEC-013 §3 ▸ operation 범위 | enum 부재 + `DELETE` 라우트 부재. 회귀 테스트 `test_baseline_agent_publish:225-229`(405) · 툴 쪽 `test_wp123:216-232`(`operation="delete"` 는 back 에 도달조차 못 함) | ✅ |

### 4. migration 0134 — **통과**

- **선례 동형**: `0095_landing_chat_usage_read.py`(revision id `0086_landing_chat_usage_read`)와 나란히 놓고 대조 — 모듈 상수 이름(`_CAPABILITY_KEY`/`_DOMAIN`/`_RESOURCE`/`_ACTION`/`_NAME`/`_DESCRIPTION`/`_ROLE_KEY`) · `op.execute` 2회 구조 · SQL 문면까지 동형. autogenerate 흔적(`op.create_table` 등) 없음 — 수동 작성.
- **ON CONFLICT**: `capability` 는 `ON CONFLICT (key) DO NOTHING`, `access_role_capability` 는 `ON CONFLICT (access_role_id, capability_id) DO NOTHING` — 선례와 동일한 두 자리 모두 적용. 멱등 테스트 `test_0134:85-109` 가 실제 재삽입으로 고정.
- **downgrade 역순**: 매핑 삭제(`DELETE ... USING capability`) → capability 삭제. upgrade 의 역순이 맞다. `test_0134:73-82` 가 왕복 후 `_leaf_rows == []` · `_roles == set()` + **웹 leaf 불변**까지 단언.
- **down_revision 정확성**: `"0133_landing_turn_taint"` — `alembic/versions/` 전수 조사 결과 `0133_landing_turn_taint` 를 down_revision 으로 갖는 다른 리비전이 **없다**(= 실측 head). ✅ 분기 없음.
- **revision id 길이**: `"0134_baseline_publish_agent"` = **27자** ≤ 32 ✅ (워커 보고의 「26자」는 오기이나 판정에 무영향).
- `member` 무접촉 · `baseline.publish.basic` 매핑 무접촉 — SQL 에 해당 키가 등장하지 않고, `test_0134:63-70` 이 upgrade 전후 `basic` 의 역할집합이 `{"member"}` 로 불변임을 단언한다.
- ℹ 참고: 타입 어노테이션이 `down_revision: str | None`(선례 0095 와 동일)이고 최근 리비전들(0129~0133)은 `str | Sequence[str] | None` 을 쓴다. 둘 다 유효하며 선례를 따른 것이므로 지적 아님.

### 5. 테스트 상수 일괄 갱신 — **통과 (누락 0)**

- **61 계열 4파일 + 소스 1자리**: `mcp/app/server.py:1844`(`"tools": 61`) · `tests/test_read_file_offset.py:220` · `tests/test_wbs_tools.py:733` · `tests/test_wp116_tools_list_filter.py:168`·`:186` · `tests/test_tool_inventory.py:80-81`(`EXPECTED_WRITE 20→21`, `EXPECTED_TOTAL` 은 파생이라 자동).
- **누락 검증**: `grep -rn "== 60\|== 61\|len(tools) ==\|len(registered) ==\|\"tools\": 6\|tools\] == 6" mcp/tests mcp/app` → 잔존 `60` **0건**. back 쪽에도 MCP 툴 카운트 하드코딩 **없음**(grep 확인).
- **`EXPECTED_WRITE_TOOLS` 집합**: `"mediness.baseline_publish"` 추가됨(`test_tool_inventory.py:79-83`). write 판별은 `_wrap_write_tool` seam 으로 세므로 실제 등록과 대조된다.
- **beyond_caller 2종**: `test_wp116_taint_policy.py:210-224` — 테스트명이 `test_only_reservation_approve_is_beyond_caller` → `test_the_beyond_caller_set_is_pinned` 로 바뀌고 `beyond == ["baseline_publish_tool", "reservation_approve_tool"]`(정렬 순서 정확). 각 원소의 사유 주석 동반.
- **capability 목록 3파일**: `test_capability_catalog.py`(`_BASELINE_AGENT_LEAF_KEYS` 신설 후 `_ALL_SEEDED_KEYS` 합집합 편입) · `test_capability_resolver.py`(`_DOMAIN_LEAF_KEYS` +1) · `test_me_capabilities.py`(system_admin 전수 목록 +1, 알파벳 순 위치 정확 — `agent.status.basic` 다음 `baseline.publish.basic` 앞). **이 세 곳 외에 `baseline.publish` 를 열거하는 back 테스트**를 grep 으로 훑었고(`test_general_services_capability` · `test_department_space_*` · `test_baseline_publish` · `test_baseline_publisher` · `test_baseline_form`) 전부 `basic` 만 참조하거나 부분집합 단언이라 갱신 대상이 아니다.

### 6. 선재 실패 6건 분리 — **재현 가능 · 정적으로 교차 검증됨 (코디 재확인 불필요, 다만 «수»는 미검증)**

- 워커 보고(msg_7bf85a48b149)가 남긴 근거: 「`git stash` 후 **HEAD 에서 같은 6건이 동일하게 실패**함을 실측했다. 원인은 leaf `action.runtime.read_all`(WP-108 착지분)이 `test_capability_catalog._ALL_SEEDED_KEYS` 와 `test_capability_resolver._DOMAIN_LEAF_KEYS` 에 반영되지 않은 선재 인벤토리 드리프트다.」 — **재현 절차(stash→HEAD 대조)와 원인 키가 명시된 형태**로 남아 있다.
- **테스트를 돌리지 않고 코드 상태만으로 교차 검증했다**:
  - `back/alembic/versions/0122_action_runtime_read_all_capability.py:1` — leaf `action.runtime.read_all` 을 `plan`·`system_admin` 2행으로 **시드한다**(WP-108 P1).
  - `grep -n "action.runtime.read_all" back/tests/api/test_capability_catalog.py back/tests/api/test_capability_resolver.py` → **0 hit.**
  - `test_capability_catalog.py:194` 는 `assert await _keys(db) == _ALL_SEEDED_KEYS` — **전수 일치 단언**이다. 시드된 키가 목록에 없으면 반드시 실패한다.
  - ⇒ **이 diff 와 무관하게 HEAD 에서 실패한다**는 워커 주장은 코드 상태로 성립한다.
- 이 diff 는 반대로 **자기 신규 leaf 를 두 목록에 정상 반영**했으므로(§5) 드리프트를 늘리지 않았고, WP-123 §비목표에도 없는 남의 부채라 손대지 않은 것이 맞다.
- ⚠ **남는 미검증 1점**: 「실패가 정확히 6건」이라는 **수** 자체는 실행 없이 확인할 수 없다. → **코디네이터 검증 단계(지목 테스트 재실행)에서 HEAD baseline 과 대조 확인 권고.** 원인·무관성은 위 정적 근거로 이미 성립하므로 「코디 재확인」 표기가 필요한 것은 **건수뿐**이다.

---

## backend 리뷰 체크리스트 (rules.md)

| 항목 | 결과 |
|---|---|
| **계층 방향** (Router 는 HTTP 만) | ✅ 신규 핸들러는 enum 판정·인코딩·상수 비교·서비스 호출뿐. `session.execute`/`select()` 직접 호출 **없음**(grep 확인). 발행 오케스트레이션은 `BasePublisher.publish` 소유 그대로 |
| **DB 접근 위치** | ✅ 조회는 기존 `BaselinePublishRepository`(`_last_publish_row`) 경유. 신규 raw 쿼리 **0**. migration SQL 은 alembic 자리라 해당 없음 |
| **자리 규칙** | ✅ 비즈니스 로직이 라우터로 올라오지 않았고(`_publish_bytes` 는 기존 함수 유지), `HTTPException` 이 repository/service 로 내려가지 않았다. 에러 정의는 `services/publish/baseline_form.py` 의 기존 `AppError` 서브클래스 패턴 그대로. 스키마 변환은 `schemas/` 안 |
| **재사용** | ✅ 발행 서비스 계층·응답 모델(`BaselinePublishResponse` 재사용, 새 shape 0)·에러 클래스(`ValidationError` 재사용)·MCP write seam(`_wrap_write_tool`)·오염 등급 선언(`access(...)`)·allowlist 필터(`filter_tools`) 전부 기존 것을 썼다. 유일한 중복 후보는 W-3(리포 기존 패턴) |
| **스키마 경계** | ✅ 응답은 `BaselinePublishResponse.model_validate(rows[0])` — SQLAlchemy 모델 직노출 없음. 요청은 신규 `BaselineAgentPublishRequest`(Pydantic) |
| **마이그레이션** | ✅ `models/` 변경 없음(테이블·컬럼 불변). capability 시드 additive 1건만, 대응 리비전이 diff 에 있음 |
| **테스트** | ✅ 신규 라우터 = `test_baseline_agent_publish.py`(37 케이스 규모, 두 층·동형·경계·무회귀 4축) · 신규 툴 = `test_wp123_baseline_publish_tool.py`(노출 층·선언 3축·어댑터·2차 게이트 부재·에러 번역) · migration = `test_0134_...py`(왕복·매트릭스·멱등). **음성 단언이 존재**한다(비관리자 목록 부재 / `member` 해소에 agent leaf 부재 / 상한 숫자 소스 부재) |

---

## 확인한 것 (PASS 근거 — 위에 안 적은 것)

① **두 층 차단이 각각 독립 테스트로 있다** — ① 노출 층은 back `compute_tool_allowlist`(`test_baseline_agent_publish.py:235-293`)와 MCP 실 `tools/list`(`test_wp123:106-125`) **양쪽에서** 각각, ② 실행 층은 `test_baseline_agent_publish.py:172-215`(5역할 403 + leaf key 정확 + 「게이트가 발행 코드보다 먼저 선다」단언)에서. 합쳐 놓지 않았다 — WP-123 P4 검증 요구 그대로.

② **웹이 안 좁혀졌다는 양성 단언이 짝으로 있다** — `test_baseline_agent_publish.py:194-208`(같은 member 세션이 agent 문 403 / 웹 문 200) · `:477-492`(`basic` 의 역할집합 `{"member"}` 불변) · `test_capability_resolver.py:381-382`(`"baseline.publish.basic" in capabilities`). 「좁힌 것이 아니라 다른 문을 냈다」가 원장·resolver·HTTP 세 층에서 고정됐다.

③ **선언 3축이 한 자리에** — `server.py:647` 한 줄에 `capability` · `needs=("product_list_tool",)` · `taint_policy=TAINT_BEYOND_CALLER`. `needs` 값이 함수명 규약(`*_tool`)을 따르며 기존 17개 선언과 동형(grep 대조). `emits_untrusted` 는 **의도적으로 미선언** — 이 툴의 출력은 back 이 만든 path/sha 이지 외부 텍스트가 아니라 기본값 `False` 가 참이다.

④ **등급 누락이 안전한 방향으로 틀린다** — `test_wp123:156-166` 이 소스에서 `taint_policy=` 만 제거한 문자열을 만들어 `write_tools_without_taint(...) == ["baseline_publish_tool"]` 을 단언한다. `assert_write_tools_declare_taint` 기동 게이트가 실제로 이 툴을 잡는다는 뜻.

⑤ **`structured.action_id` 미발명** — `tools/baseline_publish.py:178` 이 back 응답 `data` 를 그대로 싣고, `test_wp123:168-174` 가 `"action_id" not in structured` 를 단언. 승인 카드가 생기지 않는 툴이라 규약 대상 아님(SPEC-060 §4 경계) — 계약대로.

⑥ **에러 봉투가 실제로 맞물린다** — back `AppError` 핸들러(`back/app/main.py:258-263`)가 내는 `{"error": {"code", "message", "required_capability"}}` 형태와 툴의 `_parse_error`·403 분기(`tools/baseline_publish.py:52-98`)가 정확히 대응한다. `required_capability` 가 봉투 **안**에 있는 것까지 일치. (502 `GIT_PUSH_FAILED` 만 `HTTPException` 경로라 `{"detail": ...}` 봉투이고, 툴은 그 경우 `UpstreamError` 로 떨어뜨린다 — docstring 이 그렇게 명시했고 재시도가 답인 축이라 타당.)

⑦ **`format` 을 본문에서 추론하지 않는다** — WP §Open Issues 가 경고한 유혹. 라우터·툴 어디에도 `<!doctype` 검사가 없다(전문 확인). `filename = f"agent.{format}"` 합성 한 줄이 전부.

⑧ **웹/agent 동형이 테스트로 못박혀 있다** — `test_baseline_agent_publish.py:300-320` 이 Fake publisher 가 붙든 **바이트를 직접 비교**한다(`agent["content"] == web["content"]`, 같은 조립 path). html 분기도 `:322-335`(`<!doctype html>\n<!--\n---\n` 시작) 로 별도 고정.

⑨ **lint 정적 대조** — `ruff` 미설치로 실행 못 했으나: 양 리포 `pyproject.toml` 이 `select = ["E","F","I","W","UP"]` / `ignore = ["E501"]` 이라 장문 라인(`server.py:647` 등)은 위반 아님. `F`(미사용 import) — back 라우터의 `ValidationError`·`AGENT_CONTENT_MAX_BYTES`·`ContentTooLargeError`, 툴의 `Any`·`NotFoundError`, 테스트의 `ast`·`pathlib` 전부 사용처 확인. `I`(isort) — `server.py` 의 `app.tools.baseline_publish` 가 `app.tools.briefing` 앞(사전순 ✅), 라우터의 두 다중 import 블록도 사전순 ✅.

⑩ **WP §Code Surface 의 `test_tool_access_declaration.py` 미수정은 결함이 아니다** — 그 파일은 등록 툴을 **전수 순회**하는 구조라(`:33-62`) 신규 툴이 자동 포함되고, leaf 가 3단계 키인지도 자동 검사된다(`baseline.publish.agent` ✅). WP 가 요구한 「3축 선언 회귀」는 신설 파일 `test_wp123_baseline_publish_tool.py:131-144` 가 소유한다 — 자리만 다르고 커버는 됐다.

⑪ **WP §비목표 전건 미착수** — `delete` 미개방 ✅ · 카드형(Action Runtime) 배선 0 ✅ · `baseline_publishes` 스키마/commit message 무변경(diff 에 해당 파일 없음) ✅ · 웹 UI/endpoint/leaf 0 ✅ · MCP 공통 에러 enum 무수정(OPEN-060-C 우회 없음) ✅ · leaf 부여 확대 0 ✅ · FE diff 0 ✅ · 스펙/WP 문서 무수정(app 리포만 변경) ✅.

---

## 기존 부채 (이번 판정 제외)

- **`action.runtime.read_all` capability 인벤토리 드리프트** — migration `0122_action_runtime_read_all_capability.py` 가 시드하는 leaf 가 `back/tests/api/test_capability_catalog.py::_ALL_SEEDED_KEYS` 와 `test_capability_resolver.py::_DOMAIN_LEAF_KEYS` 에 없다. 두 파일의 전수 일치 단언을 HEAD 에서 이미 깨뜨린다(§특별6). **WP-108 소관 별건.**
- **SPEC-060 Tool 인벤토리 표 드리프트** — 문서는 read 39·write 18·57, 실측은 이번 착지 후 read 40·write 21·**61**. WP-123 §Open Issues 가 「실측이 정본 · 해소는 SPEC-060 별건」으로 기장했고, 이 리포도 그대로 둔다. **착지 갱신은 planner 후속**(문서 리포는 이번 워커 allowed_paths 밖).

---

## 코디네이터에게 (판정과 별개)

1. **작업이 미커밋 상태다** — `git diff origin/dev...HEAD` 가 비어 있고 변경은 워크트리에만 있다(워커 지시대로). PR 전 커밋 필요.
2. **검증 단계 권고** — 지목 테스트 재실행 시 ⓐ HEAD baseline 과 대조해 **선재 실패가 정확히 6건**인지 확인(§특별6 의 유일한 미검증 항목) ⓑ `ruff` 는 이 환경에 미설치라 별도 확인 필요.
3. **배포 순서** — migration(0134) → 카탈로그 sync → 앱. 워커 보고와 WP §Pre-deploy Check 가 같은 순서를 요구하며, 뒤집히면 `system_admin` 도 403 이라 「좁게 열었다」와 「고장났다」가 구분되지 않는다.
4. **후속 발주 후보 2건** — W-1(audit params 에 문서 전문 적재, SPEC-060 §4 audit 규약 소관이라 별건) · W-2(WP-123 Code Surface schema 행 문구 정정, planner 소관).
