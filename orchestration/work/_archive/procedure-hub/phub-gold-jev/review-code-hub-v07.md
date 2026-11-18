# 허브 0.7.2 코드 검수 — WORK-013 0.2 구현(NM · DP · CS · SP)

- 대상: 허브 워크트리 `phub-gold-jev` · HEAD `daa54e3` 위 미커밋 변경(`backend/` — 고침 17 · 새 5)
- 계약: `SPEC-001-hub-gold-mcp.md` 0.7.2 · `WORK-013-hub-v07.md` 0.2 · `review-work-013.md`(W-1 · W-2 · N-1 ~ N-6) · `impl-hub-v07-instructions.md` · 구현 보고 `impl-hub-v07-report.md` · `_RESUME.md` §2 11-17 맨 위 행들
- 방식: read-only. 코드 · 시험은 직접 읽고 diff 를 대조했다. 시험은 **gold 묶음만** 돌렸다(아래 §3 — 전체 pytest 안 돌림). 실호출은 **18105 GET 만** · 18107 · PG 는 건드리지 않았다. `.env` · 접속 값 파일은 열지 않았다. 응답 dump 는 세션 scratchpad(레포 밖)에 두었다.

## 0. 판정

**PASS — FAIL 0 · WARN 0 · NOTE 5.** 커밋해도 된다. 그 뒤 코디가 18105 를 다시 띄우면 된다.

- WP-1 ~ WP-4 완료 조건은 코드와 시험으로 확인된다. SPEC 0.7.2 의 NM1 ~ NM6 · DP1 ~ DP9 · CS1 ~ CS6 · SP1 ~ SP8 과 어긋나는 곳은 0 이다.
- 기존 필드 · `gold_hash` · `aux_hash` 는 그대로다. CSV 판 = DB 판(DT10 · v07 판까지) · REST = MCP · 도구 설명 문장 셋도 확인했다.
- 고친 기존 시험 7 파일의 변경은 전부 계약 변경(§2 ⓐ ~ ⓖ) 때문이다. **기대를 구현에 맞춰 내린 곳은 0** 이다.
- gold 묶음 **501 passed · 0 skip**(실물 env 넷 + `GOLD_EXPECTED_HASH`) · ruff 통과.
- 18105 는 이미 0.7.2 코드다(응답에 `matched.how` · `site_applied` 가 있다). 실물 네 자리의 값이 SPEC · WORK 수와 같다.

## 1. 볼 것 ① ~ ⑦ — 결과

| # | 볼 것 | 결과 |
|---|---|---|
| ① | WP-1 ~ 4 · SPEC 대조 | **PASS** — 아래 표 1-1 |
| ② | 기존 필드 · 해시 불변 · CSV = DB · REST = MCP · 도구 설명 | **PASS** — 표 1-2 |
| ③ | 고친 기존 시험이 계약 변경 때문인가 | **PASS** — 표 1-3(내린 기대 0) |
| ④ | 표지 1,617 / 497 = 646 + 971 | **PASS** — `test_gold_v07_site.py:249-251` 이 두 묶음을 따로 세어 합을 단언한다. 160 고민 14,240 짝은 표지 646 행 · 232 짝, 밖 부위 8,709 짝은 971 행 · 265 짝이다. 합은 1,617 · 497 로 SPEC-001:930 과 같고 `review-work-013.md` §4 의 CSV 재셈과도 같다. 이번 실행에서 통과했다 |
| ⑤ | 시험(바뀐 파일 관련만) · ruff | **PASS** — §3 |
| ⑥ | 커밋 후보 grep | **PASS** — §4 |
| ⑦ | 사용자가 실물에서 만날 자리(18105 GET) | 값은 전부 맞다. 앱이 알아야 할 것은 §5 에 모았다 |

### 1-1. SPEC 대조(WP 별)

| WP | SPEC | 코드 | 판정 |
|---|---|---|---|
| WP-1 NM | NM1 줄임 열쇠: 낱말 2 이상 · 끝 낱말 통째 · 앞 낱말 접두 ≥ 2(통째 포함) · 한 글자 낱말은 통째 · R1 · 자기 `norm` 뺌 · 길이 ≥ 4 | `memory.py` `abbr_keys_of` 한 곳(`ABBR_PREFIX_MIN` 2 · `ABBR_KEY_MIN` 4 — `headers.py`). `norm` 은 `headers.py` 로 옮겼고 `resolve.norm` 으로 다시 내보낸다(식 한 벌) | 맞음. 시험이 열쇠 집합을 따로 짓는다(`test_gold_v07_resolve.py:76-90`). 실물 2,881 · 533 |
| | NM2 · NM5 · `ambiguous` | `resolve.py:86-95` — 부분 후보의 개념은 줄임으로 다시 내지 않는다. 한 열쇠가 (거른 뒤) 개념 둘 이상이면 `ambiguous` | 맞음 |
| | NM4 덮임 · 순서(같은 길이면 부분 먼저) · `full` 은 줄임만 · `abbr` | `resolve.py:97-113` · 정렬 키 `(-len(span), how != 부분, …)` · 목록 꼴은 `abbr` 을 검사해 `request` 에 싣기만 한다(A-3) | 맞음. 덮임은 SPEC 보다 조금 넓다 — **N-1** |
| WP-2 DP | DP1 이 응답의 `modality_only` ∪ `unreached`(site 거른 뒤) · DP2 길 · DP3 시술 holder 만 · DP5 `path` · DP7 순서 · DP8 `none` 이면 두 열쇠 없음 · DP9 못 내린 행 | `descend.py` — repo 만 읽는다. `procedures[]` 는 `_holders(modality, 하위 시술, ("procedure",))` 뿐이다 → **메뉴 · 패키지 · 제품 코드가 시술 자리에 들어가는 길은 0**. 그 이름은 `from[].path[]` 에만 나온다. `groups` 는 손대지 않는다(`in_groups` 로만 알린다). `concern.py:122-124` · `:137-138` 은 첫 쪽에서만 내고 `none` 이면 열쇠를 뺀다 | 맞음. 시험이 DP2 를 따로 따라간다(`test_gold_v07_descend.py:57-133`) |
| | 계열 단위 표지 | `unit` = `계열` 고정. `lands` = `procedure` 면 그 시술의 계열 묶음에 넣고 `procedures[]` 는 계열 전부를 낸다. 좁힘은 `procedure_codes[]` 로 한다 | 맞음(SPEC-001:531) |
| WP-2 CS | CS1 직접 + 자손 · CS2 꼴 · CS3 물은 고민 기준 · CS4 site 무관 · CS5 순서 | `concern.py:167-180` `concern_sites` — 새 메서드 0. 물려받은 응답에서도 `code` 를 기준으로 쓴다 | 맞음. 시험이 `concern_site.csv` 로 따로 센다(`my_sites`). 실물 100(85) · 23(18) |
| WP-3 SP | SP1(0.7.2) 물은 부위 코드 ∈ `sites[].site_code` 면 `filter` · 아니면 `prefer`(입구에 없는 글자 포함) · SP7 `site_mode=filter` 면 늘 거름 | `concern.py:72` — `sm == "filter" or codes & {sites 의 site_code}` · `codes` = `site_codes()`(`bound_concerns` 와 같은 표 · 같은 식) · `sites` 는 CS 함수 하나 | 맞음 |
| | SP2 행 전부 · SP3 표지 뜻(글자 ∪ 묶임 — O-30 (a)) · N-2 false 행에 `site_match` 없음 · SP4 순서 그대로 · SP5 표지 0 도 그대로 | `concern.py:76-89` — 같은 판정 코드로 `match` 를 만든다. `prefer` 면 모든 행에 `site_prefer` 를 달고, `site_match` 는 true 행에만 단다. 행 순서는 바꾸지 않는다 | 맞음 |
| | SP6 `filter` 짝 = 0.7.0 응답 + `site_applied` · `counts.site_prefer` = `null` | `site_prefer` · `n_site_prefer` 열쇠 없음 | 맞음(`check_filter` 가 `site_mode=filter` 응답과 통째로 견준다) |
| WP-4 | 0.6 꼴 동치 · DT10 표본(N-3 · W-2) · ERRORS 셋 · T3 부록 A 여섯 줄 · swagger · README | `test_gold_v07_compat.py` · `test_medallion_repo.py:107-160`(DT9 · DT10 v07 판 — `how = 줄임` · `filter` · `prefer` · `descended = M97` 를 단언한 뒤 대조) · `SAME_V07` 은 판마다 따로 둔다(N-1) | 맞음 |

### 1-2. 불변 · 두 판 · 두 입구

| 무엇 | 근거 | 결과 |
|---|---|---|
| 손대지 않는 파일 | `git diff HEAD --stat -- coverage closure facets pairs inputs db_inputs gold_main` | 비었다 |
| `app/main.py` · `core/` · `alembic/` · `pyproject.toml` · `uv.lock` | `git status` | 이번 변경 0. origin 대비 diff 는 앞 커밋 `daa54e3` 몫이다 |
| 해시 | 18105 `health.build` — `gold_hash` 8accbb21… · `aux_hash` 6435fe41… = 구현 보고 E1 · 그 값으로 `GOLD_EXPECTED_HASH` 를 준 실물 시험 통과 | 그대로 |
| 0.6 꼴 | `test_T27_real_hash_and_06_shape` — 260 고민 `auto` = `none` 응답에서 0.7 열쇠를 빼면 0.6 머리 · `abbr=off` 37 문항 `matched` = 0.6 열쇠 | 통과 |
| CSV = DB | DT9(색인 9 · `entry_by_abbr` 포함 · v07 판은 비어 있지 않음을 단언) · DT10(기본 판 + v07 판 · 쪽 끝까지) | 통과 |
| REST = MCP | `test_gold_mcp.py` `SAME` 셋 · `ERRORS` 셋(새 enum 밖 값) · `test_T27_tools_list_and_rest_equals_mcp` | 통과. MCP 실서버 호출은 POST 라 하지 않았다(제약) |
| 도구 설명 | `mcp_server.py:34-48` · `:79-101` — ① 「글자 그대로 맞은 것이 아니라」 ② 「계열 단위」 · 「시술 하나하나가」 ③ 「부위로 거르지 않은 응답」. 끝 문장은 「site_applied = filter 일 때 … 0 그대로」로 바뀌었다. 옛 조각(「고르지 않고」 · 「부분 문자열」 · 「조사를 떼지 않는다」 · `inherited_from` · `hier`)은 남아 있다 | 맞음. 시험 셋(`T24` · `T26` · `T28` `tool_description_and_schema` · `T27_descriptions_three_sentences`)이 `DESCRIPTIONS` 와 `tools/list` 양쪽을 본다 |

### 1-3. 고친 기존 시험 — 계약 변경 때문인가

| 파일 | 바뀐 것 | 까닭(WORK §2) | 기대를 내렸나 |
|---|---|---|---|
| `test_gold_tools_synthetic.py:71-73` · `:87` | `matched` dict 에 `"how": "부분"` | ⓐ 새 필드 | 아니다 — 값은 그대로고 칸만 늘었다 |
| `test_gold_tools_synthetic.py:279` · `:281` | `site_mode="filter"` | ⓑ 기본 판 `CON-901` 은 `sites[]` = `[]` 라 `prefer` 가 된다. 0.6 기대(2 행 · 0 그대로)를 거름 길에서 그대로 지킨다 | 아니다 |
| `test_gold_holes.py:302` · `:305` · `:317` | `site_mode="filter"` | ⓖ 밖 부위 · 입구에 없는 글자는 0.7.2 에서 `prefer` 다. 단언은 그대로 둔다 | 아니다 |
| `test_gold_contract.py` | `ROW_COMPUTED` + `site_prefer` · `matched` 꼴 두 가지 · `counts` 꼴 두 가지(N-2) · 0.7 열쇠 꼴 · v07 응답 · 부록 A 여섯 줄 | ⓓ | 아니다 — 단언이 늘기만 했다 |
| `test_medallion_repo.py` | 색인 목록 + `entry_by_abbr` · DT9 · DT10 v07 · `PAGED` 에 concern | ⓔ · W-2 · N-3 | 아니다 |
| `test_gold_mcp.py` | `SAME` 셋 · `ERRORS` 셋 · `SAME_V07` | WP-4 표 | 아니다(더하기만) |
| `gold_fixture.py` · `medallion_fixture.py` | `v07` 인자 · `V07_*` 상수 | A-7 | 기본 판 · `holes` 판의 코드 경로는 그대로다(`gold_rows()` · `gold_rows(True)`). `NAME` 에 V07 이름이 늘었지만 찾아보기 표일 뿐이다 |

- 지운 단언은 0 이다. 바뀐 단언은 전부 같은 값에 열쇠를 더했거나 더 엄격한 꼴로 바꾼 것이다.
- ⓒ(`test_T22_with_inherit`) · `test_T22_real` · `test_e2e_shapes_052_real` 은 손대지 않았고 통과한다.

## 2. 지적

| # | 파일:줄 | 심각도 | 무엇 | 근거 SPEC 절 | 고칠 방향 |
|---|---|---|---|---|---|
| N-1 | `backend/app/modules/gold/resolve.py:91` · `:97` | NOTE | NM4 덮임 집합이 SPEC 보다 조금 넓다. 문장에 든 줄임 열쇠는 그 개념이 이미 `부분` 후보라서(NM5) `줄임` 후보로 다시 나오지 않아도 「맞은 조각」으로 덮임에 들어간다. 그래서 이름 전체와 줄인 꼴을 한 문장에 함께 말하면, 줄인 꼴 안의 짧은 `부분` 조각이 `covered_by` 를 얻는다. SPEC 은 「줄임으로 맞은 조각(`span`)」이라고만 적었다 | SPEC-001 §5-11 NM4 · §4-1 · 변경 기록 「예외 하나」(SPEC-001:1291) | 구현 보고가 정한 것으로 밝혔고, 37 문항 차이 0 · E2 차이 0 이다. 동작은 그대로 두고 SPEC NM4 에 「NM5 로 다시 내지 않은 줄임 열쇠도 덮임에 든다」를 되적는다(코디 몫) |
| N-2 | `backend/tests/test_gold_v07_compat.py:124-126` | NOTE | 실물 해시 시험은 `gold_hash` 만 단언하고 `aux_hash` 는 보지 않는다. 지금은 E1(18105 대조)과 내가 본 18105 값(6435fe41…)이 메운다 | WORK-013 §6 「해시 불변」(`gold_hash` · `aux_hash`) | 다음에 시험을 손볼 때 `aux_hash` 기대값을 env 또는 18105 값으로 한 줄 더한다. 커밋을 막지 않는다 |
| N-3 | `backend/tests/test_gold_v07_site.py:61-81` | NOTE | T28 의 「표지 행 = `site_mode=filter` 응답 행」 단언은 같은 판정 코드의 두 길을 견준다. 표지 판정 자체가 맞는지는 기존 T22(합성 · 실물)와 SPEC 재셈 수(646 · 971 — 따로 셈)가 받친다. SP1 기준의 `sites[]` 도 시험은 응답에서 읽지만, T25 가 그 `sites[]` 를 CSV 로 따로 맞춘다 | WORK §5 완료 조건 2 | 그대로 둔다 — 독립 근거가 겹으로 있다. 기록만 한다 |
| N-4 | `backend/app/modules/gold/resolve.py:96-99` | NOTE | 순서가 「긴 조각 먼저」라서 줄임 후보가 짧은 `부분` 후보보다 앞에 온다. 실물 「턱살 지방 주사 효과」에서 `M18`(줄임 · 4 글자)이 `CON-168` 턱살(부분 · 2 글자)보다 앞이다 | SPEC-001 §4-1 순서 · NM3 ⑦ · R6(허브는 고르지 않음) | 계약대로다. 앱 쪽에 「첫 후보 = 대상」으로 읽지 말고 `how` 를 보고 고르라고 알리면 된다(§5) |
| N-5 | SPEC 되적기 후보(코드 아님) | NOTE | 구현 때 정한 것: Protocol 메서드 29 → 31(SPEC-003 §5 P1) · 목록 꼴 `abbr` 은 무시하고 `request` 에만 싣기(A-3) · `부분` 후보에 `full` 없음(A-4) · `site_prefer` = false 행에 `site_match` 없음(A-5) · 머리 순서 `inherited_from · site_applied · counts` | WORK-013 §10 A · 구현 보고 「구현 때 정한 것」 | SPEC-001 §4-1 · §4-5 · SPEC-003 §5 P1 에 되적는다(코디 몫) |

## 3. 시험 · ruff(직접 돌림)

```
# backend/ 에서 · 실물 env 넷(GOLD_CSV_DIR · GOLD_SOURCE_REF_PATH · GOLD_HIERARCHY_DIR · GOLD_LEDGER_CHECK_PATH — 로컬 $SM 경로)
# + GOLD_EXPECTED_HASH(18105 health 값) · DATABASE_URL=sqlite+aiosqlite:///:memory:
uv run pytest tests/test_gold_*.py tests/test_medallion_repo.py tests/test_medallion_load.py -q -rs
→ 501 passed in 44.81s · skip 0
uv run ruff check app/modules/gold app/router/gold.py app/swagger_docs/gold.py tests/test_gold_*.py tests/test_medallion_repo.py tests/gold_fixture.py tests/medallion_fixture.py
→ All checks passed!
```

- 돌린 파일(14): `test_gold_{contract,coverage,holes,load,mcp,real,rest,tools_synthetic,v07_compat,v07_descend,v07_resolve,v07_site}.py` · `test_medallion_repo.py` · `test_medallion_load.py`(`medallion_fixture.py` 를 고쳤으므로 넣었다). B-1 이 허락한 가장 넓은 범위이고, 그 밖의 파일과 전체 pytest 는 돌리지 않았다.
- 수가 구현 보고(WP-4 501 passed · 0 skip)와 같다.

## 4. 커밋 후보 grep

| 검사 | 결과 |
|---|---|
| `git status --porcelain` | 고침 17 · 새 5 — 전부 WORK §2 allowed_paths 안이다. `*.csv` · `*.json` dump · `*.db` 는 0 |
| 비밀값 · 접속 문자열(`postgresql://` · `passw` · `secret` · `token` · `api_key`) — `git diff HEAD` + 새 파일 5 를 직접 grep(WORK 검수 N-3) | 0 |
| 홈 경로(`/Users/` · `/home/`) | 0 |
| URL | 1 건 — 시험의 ASGI `base_url="http://127.0.0.1"` 이다(포트 없는 로컬 transport). 문제없다 |
| 데이터 본문 하드코딩 | 실물 시험은 env 경로로 읽는다. 하드코딩된 것은 코드 · 수(`CON-168` · `M18` · `PRC-123`~`128` · 2,881 등)뿐이다. Procedure Hub 데이터는 공개(11-17)라 문제없다. 합성 fixture 이름은 전부 가짜다 |

## 5. 사용자가 실물에서 만날 자리(18105 GET · 0.7.2 코드로 떠 있음)

| 자리 | 호출 | 18105 응답 | 앱 · 다른 서비스가 알아야 할 것 |
|---|---|---|---|
| **턱살** | `concern-candidates?concern_code=CON-168` | `total` 0 · `descended` = `M18` 지방분해 주사 1 묶음 · 시술 6(`PRC-123` ~ `PRC-128`) · `path` = 패키지 `PKG-0040` 「V라인주사」 → 계열 `M18` · `counts.descended` `{rows 1, modalities 1, procedures 6, new_procedures 6, undescended 0}` · `sites` = `SITE-072` 턱(`CSI-0054`) | `groups` 는 0 그대로다. 시술 리스트는 `descended[]` 에서 읽어야 한다. V라인주사는 `path` 에만 나오고 시술 자리에는 없다(DP3). 묶음 머리는 「계열 단위」 문구로 보여 준다(`unit`) |
| **「볼 + 탄력 저하」** | `CON-048` · `site=볼`(`SITE-051`) | `site_applied` = `prefer` · 105 행 · 묶음 55 · `counts.site_prefer` `{rows 0, groups 0}` · `sites` = `[]` / `site_mode=filter` → 0 행 · `unfiltered_rows` 105 | 0.6 까지는 0 이었고 이제 행 전부가 나온다. **표지가 0 이라 「볼」 쪽으로 앞에 둘 것이 없다**(SP5 · O-31 ② — concern_site 보강 뒤에야 생긴다). 앱은 「볼에 한정된 시술」이라고 말하면 안 된다(도구 설명 ③) |
| **「이마주름 + 볼」** | `CON-005` · `site=볼` | `prefer` · 54 행 · 묶음 15 · 표지 0 · `sites` = `SITE-014` 이마 / `filter` → 0 · `unfiltered_rows` 54. `site=이마` → `filter` 54 · 15 · `by_site_match` `{column 5, concern_site 54}` | 0.7.2 가 새로 연 길이다(O-31 ① 닫힘). 이마주름의 부위는 이마라서 볼로는 거르지 않는다. 앱은 `sites[]` 로 「이마주름은 이마 고민」을 짚어 줄 수 있다 |
| **줄임 「지방 주사」** | `resolve?text=지방 주사 맞고 싶어`(붙여 쓴 꼴 같음) | `M18` 지방분해 주사 `how` = `줄임` · `span` 지방주사 · `full` 지방분해주사 / `CON-137` 「주사」(고민) `부분` · `covered_by` = 지방주사 · `ambiguous` false. `abbr=off` → `CON-137` 만 · `covered_by` null | 줄임 후보는 Jev 확인 대상이다(NM3 ⑦). 「턱살 지방 주사 효과」에서는 줄임 `M18` 이 `CON-168` 보다 앞에 온다(N-4) — 첫 후보를 대상으로 읽으면 안 된다 |
| 오류 | `abbr=x` · `range=x` | `invalid_argument` 문장 | REST 는 422 다(ERRORS 시험과 같다) |

- `to_procedure=none` → `descended` 열쇠가 없고 `counts` 에서도 빠진다(실물 확인).
- 내가 18105 로 확인한 수는 전부 WORK-013 §4 · §5 · E3 · E4 · E5 와 같다.

## 6. 끝

- 쓴 파일: 이 리포트 1 개. 허브 레포 · SPEC · WORK 는 건드리지 않았다.
- **PASS — 커밋 가능.** 코디 몫으로 남은 것: 커밋 → 18105 재시작은 **이미 0.7.2 로 떠 있다**(이 검수가 본 것). 앱 답 키 37 다시 뽑기와 SPEC 되적기(N-1 · N-5)도 코디 몫이다. N-2 는 다음에 시험을 손볼 때 한 줄 더하면 된다.
