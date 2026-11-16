# SPEC-001 · WORK-001 검수 리포트 (reviewer_doc)

> 2026-10-26 · 대상 `SPEC-001.md` · `WORK-001.md` · 기준 `DEC-001.md` · `_RESUME.md` §2
> 사실 확인: 코드 `PROCEDURE-HUB` `release/v1.2.0` @ `5b9af03`(read-only) · stg GET 21개 각 1회(2026-10-26 21시 KST, 전부 200) ·
> MCP SDK 문서(`py.sdk.modelcontextprotocol.io/run/` · `/run/asgi/` · `/get-started/testing/`) · PyPI `mcp` 2.3.0
> 수치 대조: stg 응답 10개에 SPEC 규칙을 스크래치 스크립트로 그대로 적용해 다시 셌다(레포에 남기지 않음)

## 종합 판정: **FAIL**

DEC 이탈은 없다. 모델 호출 0, 레거시 · canonical 미접근, 큐레이션 비병합, 완전 일치만 쓰는 매칭 모두 지켰다.
MCP · 별도 진입점 · migration 판단도 맞다. 기대 수치도 대부분 stg 에서 그대로 재현됐다.
다만 **문서에 적히지 않은 규칙에 기대는 기대값**과 **문서끼리 어긋나는 곳**이 있다. 백엔드 워커가 문서대로 구현하면
`graph_e2e_check.py` 가 FAIL 을 내거나 틀린 엣지가 소리 없이 생긴다. 아래 FAIL 7건을 고친 뒤 발주해야 한다.

| # | FAIL | 위치 |
|---|---|---|
| F1 | `procedure_relation` 106쌍 · 충돌 7건이 **적히지 않은 규칙 3개**를 써야만 나온다 | SPEC:160 · 171-177 · 197 · 501 · 528 |
| F2 | `coverage_gap` 두 종류의 정의와 기대값이 서로 다르다(26 · 521) | SPEC:165 · 198 · 517 · 520 |
| F3 | `treats` 엣지 단위(행마다 / 쌍마다)와 `edge_id` 의 「원천 키」가 정의되지 않았다 | SPEC:146 · 149 · 159 |
| F4 | `products.energy_device.category_id` 가 **배열**인데 SPEC 은 단일 값으로 쓴다 | SPEC:132 · 162 |
| F5 | CC → 고민 항목 매칭이 4건에서 후보 2개로 갈리는데 고르는 규칙이 없다 | SPEC:159 ③ · 210 |
| F6 | 부분 그래프의 엣지 방향이 정의되지 않았다. S-1 결과 · 크기가 방향에 따라 달라진다 | SPEC:305-314 · 477 |
| F7 | import 경계: WORK 가 `BaseRepository` 상속을 지시하는데 같은 WORK 의 경계 테스트가 그걸 금지한다 | WORK:98 · 103 · 153 · SPEC:435 |

---

## 1. DEC 이탈

**PASS.** 지적 없음.

- D-12 · D-05 모델 호출 없음: 빌드 · 검색 · tool 전부 결정론이다(SPEC:87 · 184 · 281-289). 경계 테스트도 LLM 클라이언트 import 를 금지한다(WORK:188)
- D-13c: graph 모듈은 레거시 · canonical 모델 · repository · service 를 import 하지 않고, 테이블은 `graph_` 접두다(SPEC:435-436). 브론즈는 stg JSON 에서 받는다(SPEC:98-100)
- D-13e: 큐레이션 3종이 원천마다 따로 엣지가 된다(SPEC:159). 제품 두 원장도 합치지 않는다(SPEC:136)
- D-13d: 동의어는 정규화 완전 일치만 쓴다(SPEC:164 · 184). 실측 9건 · 미연결 16/25 가 SPEC 과 같다
- D-13b: 충돌 값을 전부 보존한다(SPEC:176)
- D-06: 상세 · 이웃 · 부분 그래프에 `safety` 와 `graph_version` 이 붙는다(SPEC:250-251)

WARN 1건(→ W1): 검색 · 목록에서 `safety` 를 빼는 해석(SPEC:252)이 D-06 「시술 노드를 내보낼 때 **항상**」보다 좁다. OQ-S04 로 열어 둔 것은 맞다.

## 2. 구현 가능성 · 원천 필드 경로

### F1 — `procedure_relation` 쌍 수 · 충돌 수가 적히지 않은 규칙에 기댄다 (FAIL)

SPEC 규칙을 글자 그대로 적용하면 **108쌍 · 충돌 12건**이 나온다. SPEC 이 적은 **106 · 7**(SPEC:160 · 197 · 528)은
아래 세 규칙을 **전부** 더했을 때만 재현된다(실측으로 확인).

1. **제품으로 풀린 끝점**: §3.3.1 사전에는 제품 이름이 들어 있다(SPEC:183). 그래서 synergy 끝점 5개가 `product` 노드로 풀린다 —
   `M11-시크릿`→`product:M11-P-2` · `M11-인트라셀`→`product:M11-P-1`(각 2회) · `M8-피코웨이`→`product:M8-P-1`.
   그런데 `procedure_relation` 의 끝점은 「시술군 또는 시술 항목」뿐이다(SPEC:160). 106 이 나오려면 제품으로 풀린 끝점을
   `*_category` 시술군으로 되돌려야 한다. 이 규칙은 SPEC 에 없다. 두 원장에 같은 정규화 이름의 제품이 57쌍 있는데,
   제품끼리 갈릴 때 무엇을 고르는지도 정해져 있지 않다(SPEC:183 은 시술 항목 동률만 다룬다)
2. **자기 자신과의 쌍**: 1번을 적용하면 `M11-시크릿 → M11-인트라셀` 이 `procedure_group:M11 ↔ procedure_group:M11` 이 된다.
   106 이 나오려면 이 쌍을 버려야 한다. 이 규칙도 SPEC 에 없다
3. **`sequence_order` 를 붙이는 범위**: SPEC:174 「두 끝 시술군이 서로 다른 `session_phase_order`」는 시술 항목 끝점이면
   그 항목의 시술군으로 읽힌다. 그렇게 읽으면 시술 항목이 낀 쌍 7개(`procedure:M3-1-1`↔`procedure_group:M9` 등)에서
   충돌이 더 생겨 12건이 된다. 7건은 **양 끝이 모두 `procedure_group` 노드인 쌍에만** 붙일 때만 나온다

결과: 워커가 문서대로 구현하면 S-6 `source_conflict` 와 S-4 가 FAIL 이 된다. WORK:242 는 「숫자를 맞추려고 규칙을 바꾸지 않는다」고
하므로 워커가 스스로 고칠 수도 없다. 세 규칙을 SPEC §3.3 · §3.3.1 에 적어야 한다.

### F2 — `coverage_gap` 정의와 기대값이 다르다 (FAIL)

- `concern_item_without_treats` 기대 26(SPEC:198 · 517): 정의는 「treats 엣지 없는 고민 항목」이다. 하지만 ③ problem-packages 가
  `concern_item → procedure_group` treats 를 만든다(SPEC:159). 그래서 **어떤 원천이든 treats 가 없는 항목은 1개뿐**이다(실측).
  26 은 ① taxonomy `modality_ref` 만 셀 때의 값이다(빈 `modality_ref` 26 실측). 정의에 「taxonomy 원천만」을 적거나, 기대값을 1 로 바꿔야 한다
- `procedure_without_concern` 기대 521(SPEC:198 · 520) · 「고민 → 시술 항목 엣지 0」(SPEC:165): ④ treatment-optimization 은
  `opt_concern →` **시술 항목**으로 풀린 treats 를 만든다(SPEC:159 ④). 실측으로 26행 중 12행이 시술 항목으로 풀리고, 서로 다른 시술 항목은 8개다
  (S-2 4번의 `procedure:M8-1-2` · `procedure:M8-3-1` 이 그 예다 — SPEC:485). 문서대로 구현하면 513 이 나온다. SPEC:165 의 「0」과 S-2 4번은
  같은 문서 안에서 서로 어긋난다

### F3 — `treats` 엣지 단위와 `edge_id` 원천 키 (FAIL)

- `edge_id` = hash(타입 · 양끝 · **원천 키**)(SPEC:146)인데 「원천 키」가 엣지 타입마다 무엇인지 적혀 있지 않다
- `treats` 기대 개수 ② 63 · ③ 254 · ④ 26(SPEC:159)은 **원천 행 수**다. 실측으로 (from, to) 쌍 수는 ② 32 · ③ 241 · ④ 19 다.
  problem-combos 는 tier 셋이 같은 시술군을 반복해서 차이가 크다. 「엣지 하나 + claims 여러 개」(SPEC:149 「원천별 주장 목록」)로 읽으면 32 · 241 · 19 가 나오고,
  「행 하나 = 엣지 하나」로 읽으면 63 · 254 · 26 이 나온다. S-2 4번 「엣지 4개 — 피코토닝(경미 · 중등도 2건)」(SPEC:485)은 행 단위로 쓰여 있다.
  원천 키(예: `json_path`)와 집계 단위를 정해야 노드 · 엣지 id 결정론 테스트(SPEC:443 · WORK:187)도 닫힌다

### F4 — `products` 분류의 `category_id` 가 배열이다 (FAIL)

stg `products.energy_device.category_id = ["M8", "M9", "M11"]` 이다(제품 18개). 나머지 7개 분류는 문자열이다. SPEC 은 단일 값을 전제한다 —
노드 키 `products:<category_id>:<정규화 name>`(SPEC:132), `has_product` ②(SPEC:162), 제품 동의어 「같은 시술군 안에서」(SPEC:136).
배열일 때 노드 키 · has_product 엣지 수 · 동의어 판정을 어떻게 할지 정해야 한다. 참고로 ② 제품 수는 59(합계 118)다. 「59 + ②」(SPEC:132 · 162 · 164)도 숫자로 닫을 수 있다.
배열을 펴서 셀 때 제품 동의어 쌍은 57 이다.

### F5 — CC → 고민 항목 동률 (FAIL)

③ 「CC `cc` 를 같은 P 아래 `concern_item.name` 과 정규화 일치로」(SPEC:159)를 쓰면 P9 의 CC 4건이 후보 2개로 갈린다(실측).

| CC `cc` · `cc_group` | 후보(하위 분류 label) |
|---|---|
| 니들RF · 여드름흉터 | `auto-132`(여드름흉터) · `auto-139`(튼살) |
| 니들RF · 튼살 | 같음 |
| 프락셔널레이저 · 수술흉터/화상흉터 | `auto-136`(수술흉터/화상흉터) · `auto-138`(튼살) |
| 프락셔널레이저 · 튼살 | 같음 |

고르는 규칙이 없어 워커마다 다르게 고른다. 잘못 고르면 「튼살」 CC 의 시술이 「여드름흉터」 항목에 소리 없이 붙는다. SPEC:210 「0 / 115」도
이 동률을 보이지 않는다. D-12 는 「안 맞는 것은 검증 리포트에」를 요구한다. 그런데 `cc_group` 과 하위 분류 `label` 이 4건 모두 같아서 결정론으로 가를 단서는 원천에 있다.
규칙(또는 동률 이슈 코드)을 SPEC 에 적어야 한다.

### F6 — 부분 그래프 방향 (FAIL)

SPEC:305-314 는 「너비 우선」만 적었다. 엣지를 `from→to` 로만 따라가는지, 양방향으로 따라가는지가 없다. `neighbors` 에는 `direction` 이 있는데(SPEC:300) subgraph 에는 없다.
S-1 2번(`start=concern:P7&hops=3&edge_types=has_child,treats`, SPEC:477)으로 실측했다.

- 정방향만 따라가면 노드 172개다. 시술군은 M1 · M4 · M5 · M8 · M9 · M11 이고, 이 중 **시술 항목이 156개**다 — problem-combos 의 `concern:P7 → 시술군`(1홉) 다음에 `has_child` 가 시술군 아래 항목을 전부 끌어온다
- 양방향이면 노드 325개다. 기본 `max_nodes=300` 에 걸려 `truncated=true` 가 되고, 시술군 16개 · 다른 고민 항목 92개가 섞인다

S-1 기대값(「M11 · M8 · M5 · M4 · M1 포함」)은 두 경우 모두 참이다. 하지만 응답 크기와 내용이 크게 달라 e2e_check 가 비교할 기준이 없다. 방향을 적어야 한다.

### 원천 필드 경로 — 실측과 맞는 것 (PASS)

다음 경로는 stg 실물과 같다. taxonomy `modality[]`(`id` · `category` · `category_en` · `group` · `subcategories[].items[]` · `products[]` · `extracted.contraindications.absolute/relative`) ·
`problem[].subcategories[].items[].modality_ref`(합계 105 · 빈 칸 26) · problem-combos `combos[].packages[].procedures[]`(M 코드 문자열, 63) ·
problem-packages `problems[].complaints[].{cc, cc_group, procedures[].{name, category, role}, combos[].combo[]}`(115 · 254 · 277) ·
synergy `links[].{from, from_category, to, to_category, type, reason, timing, target}`(115 · 끝점 접두 = `*_category` 230/230) ·
contraindications `rules[].{from, from_name, to, to_name, level, interval, note}`(27) ·
treatment-sequence `sequence_order[].categories` · `minimum_intervals[].{from, to, min_days|min_months}` · `incompatible_same_day[].pair`(원소 1개 1건) ·
treatment-optimization `by_concern[].severity_levels[].{level, optimal_combo, evidence_level, rationale}`(74) ·
complications `categories[].{id, complications[]}`(10 · 65 · 같은 시술군 안 이름 중복 0) · anatomy-danger-zones `zones[].{id, name_ko, name_en, danger_level, botox_specific, filler_specific}`(11).

**실측으로 재현된 기대값**: 노드 941(= 882 + 제품 ② 59) · 중복 id 0 · 검색 S-1(5) · S-2(2) · S-3(1, 「쳐짐」 6) ·
S-2 2~4번 엣지 · M1↔M2 claims 6개(contraindications `first=M1` · sequence_order `first=M2` · synergy 4) · safety gaps(M1 `[]` · M4 `no_complication` · M13 둘 다) ·
`unresolved_by_source` 67/230 · 48/74 · 66/254 · 23/35 · `combo_not_in_procedures` 36/277 · synonym 9 · `unlinked_vocabulary` 16/25 ·
`concern_without_curated_package` 6 · `procedure_group_without_concern` 1(M13) · 금기 규칙 없는 시술군 6 · 합병증 없는 시술군 7 · `site_caution` 22 · `session_phase_order` 시술군 10.

### WARN

- **W2 이름 원천 필드**(SPEC:117 · 125-134): `name` 을 어느 필드에서 가져오는지 표에 없다. 실물 기준으로는 고민 대분류 `category`, 하위 `label`, 시술군 `category`(`name` 과 같은 값), 부위 `name_ko` 다.
  검색 기대값이 이 선택에 달려 있다. `names.en` 을 `*_en` 에서 채우는지도 안 적혀 있다(지금은 「동의어」 열에만 있다)
- **W3 `?build=latest`**(SPEC:337): 검증 API 파라미터 표(SPEC:330-334)에 `build` 가 없다. `build_id` 는 응답 필드 목록(SPEC:336)에 없고 본문에만 나온다
- **W4 `limit=0`**(SPEC:512): S-6 은 `limit=0` 으로 부른다. 쪽 나눔 범위(SPEC:321 · 334 「0 · 100(최대 1000)」)는 0 이 offset 기본값인지 limit 하한인지 모호하다. 워커가 `ge=1` 로 두면 S-6 이 422 가 된다

## 3. 기존 코드와의 충돌

**별도 진입점 판단 PASS.** `tests/test_public_api_contract.py:18` 이 `app.main.app` 을 직접 import 한다. `:228-246` 은 `/procedure-hub/` 아래 operation 집합 ·
semantic 수(read 32 · write 9 · conditional-write 1) · 해시를 동결하고, `:249-` 는 태그 집합 6개를 동결한다. 기존 앱에 붙이면 둘 다 깨진다. `app/graph_main.py` 는 이 테스트에 잡히지 않는다.

**migration 공존 PASS.** 기존 revision 은 하나(`b202609030001`, `down_revision=None`)라 `down=b202609030001` 로 단일 head 가 된다. `alembic/env.py:22-24` 는
`app.model.base` 를 import 하면서 패키지 `app/model/__init__.py` 를 실행한다. 그래서 import 한 줄로 autogenerate · `alembic check` 가 graph 테이블을 본다.

**`app/model/__init__.py` 영향 PASS(조건부).** 기존 앱과 SQLite 테스트의 `Base.metadata.create_all`(`tests/test_publication_application.py:34`)에 graph 테이블이 함께 생긴다.
JSON 컬럼을 `JSON().with_variant(JSONB(), "postgresql")` 로 두면(WORK:131, 선례 `app/model/canonical_publication.py:32`) SQLite 에서도 문제없다. 테이블 수를 세는 기존 테스트는 없다.

### F7 — import 경계가 WORK 안에서 서로 어긋난다 (FAIL)

- WORK:98 은 `app/modules/graph/repository.py` 가 `app/repository/base.py` `BaseRepository` 를 상속하라고 한다
- WORK:153 경계 테스트는 `app.repository` import 를 금지 대상에 넣었다 → Phase 1 테스트가 Phase 3~5 구현을 막는다
- SPEC:435 의 허용 목록(`app/core/config` · `tx` · `exceptions` · `app_builder` · `app/model/base`)에는 `app.repository.base` 와 `app.schema.base` 가 없다.
  그런데 WORK:103 은 `app/schema/base.py` 의 `ItemBase` · `ResponseBase` 를 쓰라고 한다. graph 앱 lifespan 이 쓸 `app.core.lifespan` · `app.core.logging` 도 목록에 없다

허용 목록과 경계 테스트 금지 목록을 같은 내용으로 맞춰야 한다.

### WARN

- **W5 ruff 범위**(WORK:156 외 전 Phase): WORK 는 `ruff check app tests scripts` 를 돈다. CI 는 `uv run ruff check .` 라서 새 migration `alembic/versions/…` 까지 검사한다(`.github/workflows/backend-test.yml` 「Ruff」 단계). 로컬 통과 ≠ CI 통과
- **W6 인덱스 이름 충돌**(WORK:126-127): `Base` naming convention 이 `ix_%(column_0_label)s`(`app/model/base.py:8-14`)라 이름이 첫 컬럼만으로 정해진다. `graph_edge` 에 `(build_id, from)` · `(build_id, to)` 처럼 같은 컬럼으로 시작하는 인덱스를 두 개 두면 이름이 `ix_graph_edge_build_id` 로 겹쳐 migration 이 실패한다. 인덱스에 이름을 명시하라고 적어 두면 좋다

## 4. MCP 결정

**PASS.** 근거 URL 이 결정을 실제로 뒷받침한다(2026-10-26 확인).

- `from mcp.server import MCPServer` · Streamable HTTP: `/run/` 에 「SSE was superseded by Streamable HTTP in the 2025-03-26 protocol revision」이 있다. PyPI 최신은 `mcp` 2.3.0 · `requires_python >=3.10` · `pydantic>=2.12` · `starlette>=0.27` 이고, `uv.lock` 의 pydantic 2.13.0 · starlette 1.0.0 과 충돌하지 않는다
- `stateless_http=True` · `json_response=True`: `/run/` 이 두 옵션과 `NoBackChannelError` 를 SPEC:400 대로 설명한다. 이 옵션은 생성자가 아니라 `run()` / `streamable_http_app()` 키워드로 준다(「Transport options go to run(), not to MCPServer(...)」 · `/run/asgi/` 「streamable_http_app() takes the same keyword arguments as mcp.run("streamable-http", ...)」). WORK Open Issues(WORK:268)의 의문은 이것으로 풀린다
- 마운트: `/run/asgi/` 「Mount the app and that built-in lifespan is dead code」 · `RuntimeError: Task group is not initialized` 가 SPEC:402 와 같다. `Mount("/prefix", app=mcp.streamable_http_app())` + 기본 `/mcp` = `/prefix/mcp` 도 문서 예시(`/notes/mcp`)와 같다 → `/procedure-hub/graph-mcp/mcp` 로 구현할 수 있다
- localhost 기본값 · 421: 문서와 같다. 로컬 `127.0.0.1:18005` 에서는 문제없다
- 테스트: `/get-started/testing/` 의 `Client(mcp)` in-memory 로 WORK:227 을 구현할 수 있다. 다만 문서 예시는 `pytest.mark.anyio` 이고 레포는 `asyncio_mode = "auto"`(`pyproject.toml`)다. 섞어 쓸 때 주의할 정도라 지적하지 않는다

## 5. E2E 시나리오

F1(S-4 · S-6 충돌 수) · F2(S-6 두 칸) · F6(S-1 응답)이 해당한다. 그 밖에:

- **W7 S-4 1번 문구**(SPEC:496): 「M1 ↔ M2 엣지 1개」라고 쓰여 있지만 `procedure_group:M1` 의 `procedure_relation` 이웃은 실측 17개다. 「그중 M1↔M2 엣지가 하나」라는 뜻이면 그렇게 써야 사용자가 「엣지 1개」를 기대하고 놀라지 않는다
- **W8 S-7 과 「stg 1회」**(SPEC:533 · WORK:51 · 239 · 237): e2e_check 가 S-7 을 확인하려면 `graph_ingest` 를 다시 돌려야 한다. http 모드로 돌리면 stg 를 두 번째로 부른다 — WORK:51 「Phase 7 에서 1회만」과 어긋난다. 워커 실측은 `--from-dir <저장한 원본>` 으로 하라고 적는 것이 맞다(해시가 같으므로 `unchanged` 가 나온다). e2e_check 가 CLI 를 부르는지, S-7 만 수동인지도 WORK:237 에 없다
- 명령 · 경로 PASS: SPEC:456-465 순서(compose → alembic → ingest → build → uvicorn), Swagger `/procedure-hub/api-docs`(`app/core/app_factory.py:39-41` 규칙과 같음), MCP 주소 · `claude mcp add --transport http` 예시가 다 있다. 21개 엔드포인트 모두 stg 에서 200 · `application/json` 이다(실측)

## 6. WORK Phase

**PASS(F7 · W5 · W8 제외).**

- Phase ↔ SPEC: 1=§5.2 · 2=§3.1 · 3=§3.2-3.3 · 4=§3.4 · 5=§4 · 6=§5.1 · 7=§5.4-§6 이 1:1 로 이어진다. Phase 마다 관련 테스트만 돌리고 전체 검증은 마지막 한 번이다(WORK:243)
- 테스트가 stg 를 부르지 않는다: fixture 디렉토리 · `httpx.MockTransport`(WORK:170) · 스냅샷 통합 테스트는 env 가 있을 때만 · `tests/integration` 은 CI 제외(WORK:114 · 238)
- 포트: 55434 · 18005 는 사용자 포트(3700 · 3800 · 8700 · 8800 · 54329)와 겹치지 않는다. 2026-10-26 현재 두 포트 모두 LISTEN 이 없다. 정리 단계(WORK:240)도 지정 포트만 건드린다
- env: `envs/graph.env.example` 은 루트 `.gitignore:46` `.env*` 에 걸리지 않으니 추적되고, `envs/.env.graph` 는 무시된다 — SPEC:427 판단이 맞다

## 7. 사용자가 실물에서 만날 자리 (막히진 않지만 이상해 보일 곳)

- **응답이 크다**: S-1 2번 부분 그래프는 정방향만 따라가도 시술 항목 156개를 담는다. 시술 항목마다 시술군 `safety`(이웃 relation 엣지 전체 + claims)를 상속해서 붙인다(SPEC:263-264). 그래서 Swagger 응답이 수 MB 가 될 수 있고, MCP 로 받는 LLM 컨텍스트에도 부담이 된다. 시나리오대로 하면 사용자가 처음 보는 화면이 이것이다
- **`safety.procedure_relations` 에 시너지 엣지가 섞인다**: 포함 조건에 `first`(SPEC:264)가 있다. synergy `다음에`와 sequence_order 도 `first` 를 만들기 때문에, 금기와 상관없는 시너지 엣지까지 「안전」 칸에 들어간다
- **같은 이름 제품이 둘씩 나온다**: 제품 두 원장에서 57쌍의 이름이 같다. 「보톡스」를 검색하면 `product:M1-P-0` 과 `product:products:M1:보톡스` 가 같은 점수로 나란히 나온다. 의도한 동작(D-13e)이지만 처음 보면 중복으로 보인다
- **「이소트레티노인」이 시술 항목으로 풀린다**: treatment-sequence 의 약물명 「이소트레티노인」이 시술 항목 `procedure:auto-M15-1775361878302` 과 완전 일치한다(실측). 시술 노드 목록에 약물이 섞여 있다는 뜻이고, 원천 데이터 그대로다
- **M2↔M7 순서 누락**: contraindications note 「실 먼저 → 필러」는 `to_name`(「실리프팅」)과 글자가 달라 `first` 로 읽히지 않는다. OQ-S05 가 말한 한계가 실제로 생기는 자리다
- **고민 항목 id 가 전부 `auto-…` 다**: 117개 전부 `auto-<n>-<timestamp>` 형식이라 Swagger 에서 손으로 치기 어렵다. 검색 결과에서 복사해야 한다

## 무관

없음. 문서만 검수했고 코드 · 테스트는 돌리지 않았다.
