---
type: review
target: "PROCEDURE-HUB 워크트리 phub-gold-jev (branch kknaksss/phub-gold-jev · base origin/release/v1.2.0 = 3750e4c · 커밋 없음 — 작업 트리)"
contract: "SPEC-001 0.4.1 · WORK-001 0.2.0 · _RESUME §2"
reviewer: reviewer_code (read-only)
date: 2026-11-16
verdict: WARN
---

# 허브 코드 검수 — WORK-001 구현

## 0. 판정

**WARN** — FAIL 0 · WARN 2 · NOTE 10.

- 범위: allowed_paths 밖 변경 0 · 기존 코드(`app.main` · `core/` · `alembic/` · `Dockerfile`) 변경 0 · CSV 0.
- SPEC 계약(도구 8 · 부록 A 헤더 · 오류 3 · cursor · 응답 머리 · 계층 · LLM 없음 · 폭 자르기 없음)은 코드와 시험 양쪽에서 맞다.
- 시험: 데이터 env 없이 **97 passed · 25 skipped**(skip 은 실물 시험뿐). 데이터 env 로 **122 passed · skip 0**. 기존 전체 **529 passed · 27 skipped**. ruff 통과.
- 실서버 18105(코디가 띄운 것): health · REST 오류 8건 · MCP `tools/list` 와 `tools/call` 2건 확인. 서버는 띄우거나 내리지 않았다.
- WARN 둘:
  - **W-1** offer 대상 쪽의 행 되풀이와 넓어짐. SPEC 문구대로라면 맞지만, SPEC 이 `total` 의 뜻과 상품 쪽 role 을 정하지 않았다. 코디 · 사용자가 정할 일이다.
  - **W-2** `.env.example` 의 빈 선택 값을 복사하면 import 때 앱이 죽는다.

## 1. 범위 산정(볼 것 1)

| 확인 | 결과 |
|---|---|
| `git diff --stat origin/release/v1.2.0` | 수정 4: `backend/README.md` +33 · `backend/envs/.env.example` +12 · `backend/pyproject.toml` +1(`mcp>=2.3,<3`) · `backend/uv.lock` +471/−3 |
| 미추적 | 소스 22(`app/modules/gold/` 19 · `router/gold.py` · `swagger_docs/gold.py` · `gold_main.py`) · 시험 8(`tests/gold_fixture.py` · `gold_support.py` · `test_gold_{contract,load,mcp,real,rest,tools_synthetic}.py`). `__pycache__` 는 gitignore 됨 |
| allowed_paths(WORK §2-2) 밖 | **0** — `git status --porcelain --untracked-files=all` 가 전부 `backend/` 아래이고 WORK 표 안에 든다 |
| 기존 코드 | `app/main.py` · `app/core/**` · `alembic/` · `Dockerfile` · `frontend/` · `docs/` · `.github/` diff **0** |
| CSV | 추적 · 미추적 모두 **0**. 합성 fixture 는 `tmp_path` 에 생성된다(`tests/gold_fixture.py`) |
| `envs/.env.gold` | 없음. `.gitignore:46` `.env*` 로 막힌다(`git check-ignore` 확인) |

## 2. SPEC-001 계약 대조(볼 것 2)

| 계약 | 코드 | 판정 |
|---|---|---|
| §2-1 · §2-3 적재 · 해시 | `inputs.py:93-176`. gold 해시 = 폴더 `*.csv` 이름순 「이름 + 공백 + sha256」 줄을 다시 sha256(`gold-check.py:46-50` 와 같은 식). `questions.csv` = `hash_only` · `rows=null`. aux 해시 = 5 파일. 헤더 다름 · 칸 없음 · 기대 해시 다름 → `GoldLoadError` | 맞음. 실서버 `gold_hash` = `8accbb21…228c` |
| X2 · X4 · X5 보조 입력 | 계층은 `code→parent_code` 만(`inputs.py:136`). 원장 확인은 `id` 와 코드만 남기고 글 칸은 버린다(`:150-156`). 추출식 = `gold-build.py:648-651` 과 같다(접두어 9 · `\b…-\d+\b`) | 맞음. health `aux` = 260/188/151 · 325/251/218 = SPEC X6 |
| §3 계층 | router · MCP → `GoldToolService` → 도구 모듈(`facets` · `pairs` · `concern` · `resolve`) → `GoldRepository` Protocol(`repository.py:39-73`). 도구 모듈은 `memory` · `inputs` 를 import 하지 않는다(시험 `test_service_layer_uses_repository_only`) | 맞음. 남은 이음매는 N-5 |
| §4-0 응답 머리 | `core.py:108-113` `build{gold_hash, aux_hash, loaded_at}` · `request` · `total` · `next_cursor`. `ledger_check[]` 는 세 도구의 첫 쪽에만 | 맞음(`request` 의 기본값 표기는 N-3) |
| §4-0 오류 | `errors.py` 422/404/400 · 문구 `<code>: <사유>`. MCP 는 같은 문구의 `isError` 결과(`mcp_server.py:79-83`) | 맞음. 실서버에서 REST `detail` = MCP text(「invalid_argument: node 는 필수다」). 예외는 N-1 |
| §4-0 cursor | `cursor.py`. build(`gold_hash` · `aux_hash` 앞 32) · 도구 · 입력 서명(`cursor` · `limit` 은 서명에서 뺌)에 묶인다. 어긋나면 `cursor_invalid` | 맞음. 실서버 `cursor=abc` → 400 |
| §4-0 `total` 단위 · 쪽 밖 목록 | resolve `candidates` · scope `holders` · neighbors `items` · facets `rows` · concern `groups` · pair `rows` · evidence = 편 줄(0 이면 1 줄). 쪽 밖 목록은 `offset == 0` 일 때만 실린다 | 맞음. T6 실물 6 도구에서 「끝까지 넘긴 합 = `total`」 |
| §4-1 ~ §4-8 도구 8 | 입력 이름 · 기본값 · 맞춤 규칙 표 · 계층 세 자리(자손 전부) · 속성 쪽(항목 단위 · `site_code` 만 코드 · 「—」 = 422) · `offer_name_contains` · `pair` 규칙 1 ~ 5 · `evidence` 잇기 규칙 | 맞음. 차이는 W-1 · N-2 · N-4 |
| 부록 A | `headers.py` = 부록 A. T3 이 실물 헤더와 양방향으로 대조하고 응답 필드 ⊂ 헤더 ∪ 계산 필드를 기계로 본다 | 맞음 |
| 허브에 LLM 없음 | gold 모듈 · 라우터 · 진입점의 import 에 LLM · DB 라이브러리 0(`app.core.app_builder` · `exceptions` · `dependency_injector` · `fastapi` · `mcp.server` · `pydantic_settings` 뿐). 시험이 `app.core.tx` · `app.core.db` 가 import 되지 않음을 본다 | 맞음 |
| **폭이 줄어드는 자리 0** | `limit` = 쪽 크기(1 ~ `GOLD_PAGE_LIMIT_MAX`) · 상한 아님. `rg "score\|rank\|top_n\|distance"` 결과 0(`resolve.py` 의 `tokens` 는 낱말 자르기 변수 · `headers.py` 의 `adverse_top_name` 은 헤더 칸). `[0]` 쓰는 곳 셋: `concern.py:43`(묶음 머리 칸) · `facets.py:242`(속성 코드 → 이름, 코드마다 하나) · `pairs.py:104`(패키지 머리 칸). 셋 다 행을 버리지 않는다. 겹치는 키를 접는 곳: `profile_by_subject` · `by_key` · `pairs._holders`. 실물에서 `g_profile` subject 중복 0 · 15표 키 중복 0 · (subject, holder) 중복 0 이라 지금 잃는 행은 0 | 맞음. 앞으로의 위험만 N-2 |

## 3. 구현 보고 주의점 대조(볼 것 3)

브리프에 적힌 다섯 줄을 ② ~ ⑥ 으로 읽었다. **⑦ ~ ⑩ 의 원문은 받지 못했다.** 구현 보고 본문이 이 워커에게 오지 않았고, 프로필에도 그 글이 없다(`grep` 0). 그 넷은 이 리포트에서 따로 보지 않았다.

| # | 주의점 | SPEC 과 부딪히나 | 판정 |
|---|---|---|---|
| ② | T4 입구를 `entry_text ∪ question` 으로 잡음. WORK §6 단계 1 은 「`entry_text`(안 풀리면 `question`)」 | SPEC §9 T4 는 입구를 어디서 얻을지 정하지 않았다(WORK H-3). 합집합은 입구를 **넓히기만** 하고 「표본 ⊂ 도구 길」 판정을 느슨하게 할 뿐 좁히지 않는다. 모든 문항에 같은 규칙이라 문항별 예외도 아니다(`test_gold_real.py:50-61`) | 부딪히지 않음. WORK 문구만 되적기(N-8) |
| ③ | mcp 2.3.0 에서 `ToolError` 를 던지지 않고 `isError` 결과를 직접 돌려줌 | SPEC §4-0 「같은 문구의 tool 오류」 가 목적이다. `ToolError` 를 쓰면 SDK 가 「Error executing tool …:」 를 앞에 붙여 문구가 달라진다. 실서버에서 같은 문구임을 확인했다 | 부딪히지 않음(맞는 선택). 단 SDK 단계의 타입 오류는 N-1 |
| ④ | 쪽 밖 목록은 첫 쪽에만 | SPEC §4-0 표와 불릿 1 이 그대로 그렇게 정했다(`ledger_check[]` 포함) | 맞음. 쓰는 쪽 주의는 §6 U-3 |
| ⑤ | offer 대상 쪽 행 중복(layer 다름) | **SPEC 규칙상 맞다 — 접으면 안 된다.** §4-4 offer 맞춤 규칙이 holder 마다 길을 정하고, 순서가 「holder `g_scope.gid` → 행 `gid`」 이다. 그래서 holder 가 여럿이면 같은 행이 holder 마다 한 번씩 나온다. 한 줄로 접으면 `layer` 하나를 **고르게** 된다. 그러면 S3(행마다 layer) · 원칙(허브는 고르지 않는다)과 부딪힌다. 다만 SPEC 은 이 경우의 `total` 뜻(holder × 행)과 상품 쪽 role 을 적지 않았고, 실물에서 규모가 크다 | **W-1** |
| ⑥ | `GOLD_MCP_RESULT_MAX_CHARS` 1,000,000 | WORK O-6 이 「가장 큰 한 쪽을 실물에서 재고 정해 보고」 하라고 했다. 412,265 자(limit 500)를 재고 여유를 둔 값이라 계약 안이다. 이 값은 클라이언트에 주는 힌트(meta)일 뿐이다 | 부딪히지 않음. 소비 쪽 위험은 N-6 |

## 4. 시험(볼 것 4) — 직접 돌린 수치

| 명령(`backend/` 에서) | 결과 |
|---|---|
| `env -u GOLD_* DATABASE_URL=sqlite+aiosqlite:///:memory: uv run pytest -q tests/test_gold_*.py -rs` | **97 passed · 25 skipped** · 1.97 s. skip 25 = `test_gold_real.py` 와 실물 몫 전부. 사유 「실물 gold env 없음」 |
| README 「gold 로컬 실행 · 검증」 데이터 env 판(필수 env 넷 + `GOLD_EXPECTED_HASH`) `… pytest -q tests/test_gold_*.py -rs` | **122 passed · skip 0** · 3.18 s. 가장 느린 것 0.43 s(`test_entrypoint_imports_no_db`) |
| `uv run ruff check app tests scripts` | All checks passed |
| (덤) README 「검증」 전체 `pytest --ignore=tests/integration -q` | **529 passed · 27 skipped** · 31.4 s. 구현 보고의 기존 529 와 같다. base 의 skip 수는 이 워커가 재지 않았다(작업 트리를 바꿀 수 없음) |

- 시험 함수 52. T1 ~ T14 가 이름에 드러난다. T4 는 37 문항 중 포인터가 있는 문항 **전부**에서 표본 ⊂ 도구 길이다(빠진 문항 0 — 시험이 0 이 아니면 실패하게 짜였다).
- T12 실물은 속성 4표의 전 코드 × 맞춤 facet(143·2 + 49·1 + 105·2 + 89·7 = 1,168 조회)을 다 본다. 각 `total` = 직접 센 수다.
- 시험 방법의 한계: T7(REST = MCP)과 오류 문구 대조는 합성 fixture 로만 돈다. 실물 REST = MCP 는 이 워커가 실서버에서 한 건 봤다(§5).

## 5. 실서버 확인(볼 것 5 — 코디가 띄운 18105 · 읽기만)

| 호출 | 결과 |
|---|---|
| `GET /procedure-hub/gold/health` | `gold_hash` = `8accbb213ac5…6228c`(SPEC §2-3 값) · `aux_hash` = `b7249e38…aff62` · `files[]` 21 줄(gold 15 + `hash_only` 1 + `source_ref` 1 + `aux` 4) · `integrity` 셋 모두 0 · `aux` = 260/188/151 · 325/251/218 · `load_ms` 251.4 · **`expected_hash_checked` = false**(N-9) |
| `GET /resolve`(입력 없음) | 422 `invalid_argument: text 가 없으면 range 또는 tables 가 필수다` |
| `GET /scope` · `/facets?facet=offer` | 422 `invalid_argument: node 는 필수다`. FastAPI 기본 목록 꼴이 아니다 |
| `GET /scope?node=procedure` | 422 `…표:코드 꼴이어야 한다` |
| `GET /resolve?range=xx` | 422 enum 밖 |
| `GET /pair?a=procedure:NOPE` | 404 `not_found: … (g_scope)` |
| `GET /scope?node=…&cursor=abc` | 400 `cursor_invalid` |
| `GET /facets?node=material:X&facet=recovery` | 422(「—」 조합) |
| MCP `initialize` · `tools/list` | 도구 8 · 전부 `readOnlyHint` · `inputSchema.required` 없음 · `outputSchema` 있음 · `_meta.anthropic/maxResultSizeChars` = 1,000,000 |
| MCP `tools/call scope {node, limit:5}` | `isError` false · `structuredContent` = 같은 REST 응답과 **글자까지 같음**(`total` 45) |
| MCP `tools/call scope {}` | `isError` true · text = `invalid_argument: node 는 필수다`(REST 와 같음) |
| MCP `tools/call scope {roles:"자기"}` | `isError` true · text = `Error executing tool scope: 1 validation error for scopeArguments …`. **REST 문구와 다르다**(N-1) |
| 크기 | `concern-candidates?concern_code=CON-001` 기본 쪽(limit 100) = 299,014 자 · `total` 114. limit 500 = 313,302 자 |

규모 셈(실서버 REST · 대상 4표 515 노드 × facet 7 · 끝까지 넘김): 되풀이 행은 `offer` 에만 있다. 3,999 행 중 서로 다른 `gid` 는 1,938 이고, 노드 207 / 515 에서 되풀이가 난다. adverse · indication · outcome · contraindication · package · profile 은 되풀이 0 이다. `g_scope` 의 (subject, holder) 중복은 0 · 목록 값(role · question_class · package_kind · edge_type)에 쉼표 0 이다(REST 콤마 목록과 안 부딪힘).

## 6. 지적 표

| # | 파일:줄 | 심각도 | 근거 SPEC 절 | 무엇 | 고칠 방향 |
|---|---|---|---|---|---|
| **W-1** | `backend/app/modules/gold/facets.py:183-191` · `:198-215` | **WARN** | §4-4 offer 맞춤 규칙 · §4-0 「`total` 단위」 · §5-2 상품 행 role 「제품은 + 하위 제품」 · §5-3 S3 | ① 상품 · 시술 노드의 `facets offer`(기본 role `자기` · `물려받음`)에서 같은 offer 행이 holder 마다 되풀이된다. 제품 노드는 `물려받음/procedure` 1 + `물려받음/procedure_case` N 으로 같은 행이 최대 12 번 나온다(조합 상위: 2 번 810 · 3 번 99 · 4 번 53 · 10 번 30 · 12 번 22). 그래서 `total` 이 서로 다른 행의 약 2.06 배다(3,999 / 1,938). ② 제품 노드에서 나온 행 중 3,221 행은 **그 제품이 아닌 상품**이다(item 이 다른 제품 · 시술 · 케이스로 물려받은 행). gold-build 시범 `ans_offer`(`gold-build.py:881-883`)는 제품이면 item = 그 제품(+ 하위 제품)만 본다. 둘 다 SPEC 문구 그대로의 결과다. SPEC 은 「holder × 행」 을 `total` 로 센다는 것도, 상품 범위에서 제품의 `물려받음` 을 펼칠지도 적지 않았다 | **구현자가 정할 일이 아니다 — 코디 · 사용자 결정 → SPEC 0.4.2.** 행을 접지는 않는다(접으면 layer 를 고르게 된다). 선택지: (a) 지금 꼴 + 계산 `counts.distinct_rows` 추가 + `total` = holder × 행임을 §4-0 에 적기 (b) gid 당 한 줄 + `layers[]`(holder 전부) — 행 필드 꼴이 바뀌어 앱 · 다른 서비스 영향 (c) 상품 범위 role 을 「제품 = `자기` + `하위 제품`」 으로 §5-2 에 못 박기(gold-build 시범과 같게 · 앱이 role 을 준다). 이 워커의 추천은 (a) + (c) |
| **W-2** | `backend/envs/.env.example:17-21` · `backend/app/modules/gold/config.py:33-39` · `backend/app/gold_main.py:72` | **WARN** | §2-2 「선택 · 없을 때 제안 기본값」 | `.env.example` 은 「실제 값은 `envs/.env.gold`」 라고 안내하면서 선택 값을 **빈 값**으로 둔다(`:16-21`). 이 덩어리를 `.env.gold` 로 옮기면 `GOLD_PAGE_LIMIT_DEFAULT=` · `GOLD_PAGE_LIMIT_MAX=` · `GOLD_MCP_RESULT_MAX_CHARS=` 의 빈 문자열이 int 로 안 바뀌어, **import 때**(`app = create_gold_app(GoldSettings())`) pydantic `ValidationError` 로 죽는다(재현: `GOLD_PAGE_LIMIT_DEFAULT= … GoldSettings()` → `int_parsing`). 문구도 gold 의 시작 실패 문구가 아니다. `GOLD_API_PREFIX=` · `GOLD_MCP_MOUNT_PATH=` 가 비면 경로가 루트로 간다. 본 앱(`app/core/config.py:43` `extra="ignore"`)은 영향 없다 | 빈 값이면 안 되는 선택 5 줄(`:17-21`)을 주석으로(`# GOLD_PAGE_LIMIT_DEFAULT=100` 꼴 · 기본값을 적어) 두거나, `config.py` 에서 빈 문자열 → 기본값으로 받기. 필수 넷은 지금처럼 빈 값 |
| N-1 | `backend/app/modules/gold/mcp_server.py:96-131` | NOTE | §4-0 「MCP 는 같은 문구의 tool 오류」 · WORK WP-3 「지킬 것」 1 | MCP 입력 타입(`list[str] \| None` · `int \| None` · `bool \| None`)을 SDK 가 코어보다 먼저 검사한다. 목록 자리에 문자열을 주면 `Error executing tool scope: 1 validation error …` 가 나간다(실서버 확인). `invalid_argument:` 접두가 없고 REST 와 문구가 다르다. WORK 는 `required` 만 빼라고 했지 타입은 다루지 않았다 | 입력을 `Any`(또는 `str \| list[str] \| None`)로 받아 코어의 `str_list` · `limit` · `flag` 가 검사하게. C 열 LLM 이 문자열 하나를 줄 일이 잦으니 앞당기면 좋다 |
| N-2 | `backend/app/modules/gold/pairs.py:24-29` | NOTE | §4-6 `a_layer` · `b_layer` · §5-3 S3 | `pair` 는 holder 마다 첫 `g_scope` 행 하나만 남긴다(`setdefault`). `facets` 는 scope 행마다 따로 낸다. 같은 (subject, holder) 에 scope 행이 둘이면 다른 경로의 layer 가 조용히 빠진다. 지금 실물은 그런 짝이 0 이라 잃는 것은 0 | gold 가 바뀔 때를 대비해 적재 때 「(subject, holder) 중복 0」 을 `health.integrity` 에 세거나, `a_layer` 를 목록으로. SPEC 0.4.2 때 한 줄 |
| N-3 | `backend/app/modules/gold/service.py:65` · `pairs.py:41` · `resolve.py:82` | NOTE | §4-0 `request` = 「기본값을 채운 입력 그대로」 | 기본값이 「전부」 인 입력(`scope.roles` · `pair.classes`)은 `request` 에 `null` 로 돌아온다. 기본값이 채워져 보이지 않는다 | `null` = 전부임을 swagger · 도구 설명에 적거나, 실제 값 목록을 채우기. SPEC 0.4.2 에 한 줄 |
| N-4 | `backend/app/modules/gold/concern.py:31` | NOTE | §4-5 `site` 정확 일치 · §4-0 `invalid_argument` | `?site=`(빈 문자열)가 오면 `site_name` · `case_site_name` 이 **빈 행**과 맞는다. 다른 입력은 빈 값을 `invalid_argument` 로 막는다(`text` · `offer_name_contains`) | 빈 `site` 는 `invalid_argument` 로 |
| N-5 | `backend/app/modules/gold/service.py:32` · `container.py:15` · `facets.py:139` · `repository.py:52` | NOTE | §3 「DB 로 갈 때 repository 만 갈아 끼운다」 | ① 기본 repository 팩토리(`CsvMemoryGoldRepository`)가 service 생성자 기본값에 박혀 있다. container 가 팩토리를 주입하지 않으니, DB 로 바꿀 때 service.py 나 container 한 줄을 고쳐야 한다 ② `offer_name_contains` 는 `rows_all("g_offer")` 을 받아 service 에서 `norm` 부분 일치로 훑는다. DB 구현에서는 전 표 읽기가 된다 | ① container 에 `repository_factory` provider 를 두기 ② `offers_by_name_contains(norm)` 같은 repository 메서드로 내리기. 둘 다 계약 영향 없음 |
| N-6 | `backend/app/modules/gold/config.py:39` · `mcp_server.py:90` | NOTE | O-6(1회차 trace 뒤) | `maxResultSizeChars` 는 클라이언트 힌트다. 기본 쪽 하나가 이미 299,014 자다(`concern-candidates CON-001`). C 열 CLI 가 이 meta 를 따르는지 · 그 크기를 LLM 문맥에 그대로 넣는지는 **확인 안 함** | 앱 1회차 trace 에서 C 열 응답이 잘리는지 본다. 잘리면 폭 누락이니, 한도가 아니라 쪽 크기로 맞춘다(O-6) |
| N-7 | `backend/pyproject.toml:11` · `backend/uv.lock` | NOTE | §8 stg(Backend CD = `backend/**`) | `mcp 2.3.0` 이 새 패키지 18 개(`cryptography` · `pyjwt` · `httpx2` · `sse-starlette` …)를 끌어온다. `idna` 는 3.11 → 3.20 으로 올라간다. pyproject 를 함께 쓰므로 `app.main` 이미지에도 들어간다. 로컬 전체 시험 529 통과라 회귀는 못 봤다 | stg PR 때 의존 변화로 적기. 배포 승인 범위 |
| N-8 | `backend/tests/test_gold_real.py:50-61` | NOTE | WORK-001 §6 단계 1 · SPEC §9 T4 | 주의점 ②. 입구 = `entry_text ∪ question`. WORK 문구와 다르지만 넓히는 쪽이다. 독스트링에 까닭(Q21 은 `entry_text` 만으로 한 끝만 풀림)이 있다 | WORK 0.2.x 에 되적기. 앱 쪽 시사점은 §7 U-4 |
| N-9 | (실서버 운영) | NOTE | §2-2 `GOLD_EXPECTED_HASH` · O-12 ① | 18105 는 `GOLD_EXPECTED_HASH` 없이 떠 있다(`expected_hash_checked` = false). 해시 값은 맞다 | 사용자 e2e 용으로 다시 띄울 때 기대 해시를 주면, gold 가 바뀐 채 뜨는 일을 막는다 |
| N-10 | `backend/app/router/gold.py:43-126` | NOTE | (be-reviewer — 실행 경로) | `async def` 핸들러가 동기 코어를 바로 부른다. 쪽마다 결과 전체를 다시 계산한 뒤 자르므로, 큰 조회의 쪽 넘김 비용은 「쪽 수 × 전체」 이고 그동안 이벤트 루프를 막는다. 로컬 단일 사용자는 문제없다(T12 1,168 조회 0.25 s) | stg 동시 호출 전에 `def` 핸들러(스레드풀)로 바꾸기. 계약 영향 없음 |

## 7. 사용자가 실물에서 만날 자리(볼 것 6)

앱(WORK-002) · 다른 서비스가 이 허브를 부를 때 헷갈릴 것.

| # | 자리 | 무엇 | 어디서 다루나 |
|---|---|---|---|
| U-1 | `facets offer`(제품 노드) | 같은 상품 행이 layer 만 바꿔 최대 12 번 나온다. 대부분(3,221 행)은 그 제품이 파는 상품이 아니라 물려받은 시술 · 케이스의 상품이다. `total` 을 「상품 수」 로 읽으면 틀린다. 앱은 `gid` 로 묶어 세고, `layer.role` = `물려받음` 인 행을 「이 제품의 상품」 으로 말하면 안 된다(hard gate 4 「하위 일반화」 의 반대 방향) | W-1 |
| U-2 | MCP 입력 타입 | LLM 이 `roles: "자기"` 처럼 문자열 하나를 주면 SDK 문구의 오류가 온다. `invalid_argument:` 로 가르는 앱 · LLM 은 이것을 못 알아본다 | N-1 |
| U-3 | 쪽 밖 목록 | `ledger_check[]` · `modality_only[]` · `unreached[]` · `same_day_packages[]` 는 **첫 쪽에만** 있다. 2 쪽부터 그 필드는 빠져 있다(빈 목록이 아니라 키가 없음). 쪽마다 덮어쓰는 클라이언트는 그 재료를 잃는다 — SPEC 그대로다 | SPEC §4-0 · 앱 클라이언트 |
| U-4 | 두 끝 질문 | Q21 꼴은 `entry_text` 만 resolve 하면 한 끝만 풀린다. 앱의 입구 고르기(Jev)가 질문 문장 전체에서 두 끝을 다 잡아야 `pair(a, b, package_kinds)` 길이 선다 | N-8 · SPEC-002 §3-1 |
| U-5 | 큰 응답 | 기본 쪽 하나가 30 만 자 가까이 된다(고민 후보). C 열(LLM 이 MCP 로 직접 묻기)에서 문맥 · 결과 잘림이 생기면, 허브는 다 냈는데 LLM 이 못 본 「폭 누락」 이 된다 | N-6 |
| U-6 | `request` 의 `null` | `scope.roles` · `pair.classes` 가 `null` 이면 「전부」 다. 「안 줬음 = 아무것도 아님」 으로 읽으면 안 된다 | N-3 |
| U-7 | 오류 꼴 | 본문은 `{"detail": "<code>: <사유>"}` 하나뿐이다. 코드 칸이 따로 없으니 HTTP 상태(422 · 404 · 400)로 가르거나 접두로 가른다(WORK H-2 — SPEC 0.4.2 되적기 대기) | WORK §9 H-2 |
| U-8 | `.env.gold` 만들기 | `.env.example` 의 gold 덩어리를 그대로 옮기면 앱이 import 때 죽는다 | W-2 |

## 8. 비밀값 · 회사 데이터(볼 것 7)

- `grep -nEi 'api[_-]?key|secret|token|password|sk-…|Bearer|https?://|/Users/|kknaks|medisolve|typesafe|ANTHROPIC'` 을 새 · 고친 파일 31 에 돌렸다. 걸린 것은 `mcp_server.py:90` 의 meta 키 이름(`anthropic/maxResultSizeChars`)과 `resolve.py:49-53` 의 변수 `tokens` 뿐이다. **비밀값 0 · 절대 경로 0 · 외부 URL 0**(README 의 `127.0.0.1` 만).
- 가격(`…원` · `price_*` 숫자 값) 0.
- 합성 fixture 의 한글 값은 전부 가짜 이름(「시술가」 · 「재료가나」 · 「가짜 설명」 · 「고민손자」 …)이거나 SPEC 이 싣는 표 값 이름(role · reach · polarity · question_class 값)이다. 시술 설명 · 원장 문장 · 질문 문장은 없다.
- 실물 시험(`test_gold_real.py`)에 박힌 값은 코드 · id(`PRC-001` · `CND-002` · `CON-001` · `GSC-00001` · `LCK-010` · `LCK-308` · Q 번호)와 SPEC §5-2 의 셈뿐이다. 문항 · 포인터는 실행 때 로컬 `questions.csv` 에서 읽는다(`gold_support.py:63-67`). 공개 레포 규칙(SPEC 머리 「표 · 칸 이름 · 코드 · 셈 · 질문 id 만」) 안이다.

## 9. be-reviewer 기준 요약(볼 것 6)

| 기준 | 판정 |
|---|---|
| 책임 경계 | router · MCP 는 입력을 넘기기만 한다. 입력 검사 · 규칙은 service 의 도구 모듈, 조회는 repository Protocol. 맞음(이음매 둘은 N-5) |
| 트랜잭션 | 해당 없음 — 쓰기 · DB 없음. 적재는 lifespan 한 번 · Singleton 상태 · 요청마다 Factory 서비스 |
| 예외 | 도메인 오류는 `DomainError` 하위 셋이고 공용 핸들러를 그대로 쓴다. 공용 `exceptions.py` 는 고치지 않았다. 적재 실패는 `GoldLoadError` → lifespan 예외 → 시작 실패(옛 「경고만 하고 뜸」 없음). 맞음 |
| 의존 | `mcp>=2.3,<3` 하나(+ lock). 본 앱 이미지 영향은 N-7 |
| 공개 API | 새 표면 = REST `GET` 8 · MCP 도구 8 · 오류 본문 꼴 · 쿼리 꼴(콤마 · `칸=값` 되풀이). 기존 API 변경 0. 다른 서비스 영향은 §7 |
| 배포 | `Dockerfile` · `app.main` 은 그대로다. stg 진입점(O-7 stg 쪽) · 데이터 반입(O-8) · 접근 제어(O-11)는 열린 채다. **이 브랜치를 stg 에 올려도 gold 는 뜨지 않는다**(이미지는 `app.main:app` 만 띄움) — SPEC §8 그대로 |

## 10. 확인하지 못한 것

- 구현 보고 주의점 ⑦ ~ ⑩ 원문(§3 첫 줄).
- base(`3750e4c`)의 전체 시험 skip 수. 이 워커는 작업 트리를 바꿀 수 없어, 지금 수(529 · 27)만 쟀다.
- C 열 CLI 가 `anthropic/maxResultSizeChars` 를 따르는지(N-6).
- 실물 데이터로 REST = MCP 를 도구 8 전부 대조하지 않았다(실서버 `scope` 한 건 + 합성 T7).
