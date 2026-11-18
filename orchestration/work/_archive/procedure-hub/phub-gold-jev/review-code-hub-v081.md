# 코드 검수 — 허브 WORK-016 resolve 0.8.1

- 검수 대상: `/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-gold-jev`(HEAD `d97a9ad` 위 미커밋 · 수정 16 · 삭제 1)
- 계약: SPEC-001 0.8.1(§3-1 · §4-1 · §5-1 R1 ~ R9 · 부록 A) · WORK-016 0.1.0 · 지시서 `impl-hub-v081-instructions.md`(R-1 · R-6 반영)
- 검수자: reviewer_code(read-only · 2026-11-18) — 파일 고침 · stash · checkout 0 · 서버 띄움 0(18105 는 GET 만)

## 판정: **PASS**(Low 3 · Info 3 — 막는 것 없음)

계약 조항과 어긋나는 코드는 없습니다. 맞춤 꼴은 `entries_by_norm(norm(text))` 하나로 찾고, `matched = {span}` 만 싣습니다. 줄임 색인과 메서드는 두 판에서 함께 지워졌습니다. 목록 꼴은 0.7.2 와 글자까지 같고, 머리 `request.abbr` 칸만 없어졌습니다. `abbr` 은 `resolve.py` 한 곳에서 거절해 REST 와 MCP 가 같은 오류를 냅니다. 남은 지적은 모두 주석 · 문서 몫입니다.

## 1. 범위(볼 것 1)

| 확인 | 결과 |
|---|---|
| `git status --porcelain` | 17 개 모두 `backend/` 안(수정: `README.md` · `app/modules/gold/{headers,mcp_server,memory,repository,resolve}.py` · `app/router/gold.py` · `app/swagger_docs/gold.py` · `tests/` 8 / 삭제: `tests/test_gold_v07_resolve.py`) · 새 파일 0 · CSV · dump · db 0 |
| 다른 도구 코드(`concern` · `descend` · `facets` · `pairs` · `coverage` · `core` · `cursor` · `kinds` · `ledger` · `ranges` · `closure` · `main.py` · `core/`) | diff 0 |
| `service.py` | **diff 0 맞음** — `abbr` 은 그대로 `_resolve` 로 넘어가고, 검사는 `resolve.py:28-29` 한 곳 |
| 손대지 않을 시험(`test_gold_holes` · `_v07_descend` · `_v07_site` · `_load` · `_rest`) | diff 0 |

## 2. SPEC-001 0.8.1 대조(볼 것 2)

| SPEC | 코드 | 판정 |
|---|---|---|
| §4-1 · R1 `norm` 식 그대로 | `headers.norm` 은 docstring 만 바뀌고 식은 같다 | ✓ |
| R2 정확 일치 | `resolve.py:46` `ctx.repo.entries_by_norm(q)` — 부분 문자열 훑기(`entry_norms()` 반복) 지움 | ✓ |
| R5 후보 0 = 200 · 빈 목록 | 문장 · 조사 · 일부 · 이어 쓴 글 → `total 0`(합성 · 실물 37 문장 시험) | ✓ |
| R6 · R8 겹침 전부 · `ambiguous` | `:47` 개념 2 이상 · 고르지 않음 | ✓ |
| 순서 = `in_range` → 표 순서 → 「이름」 → `gid` | `:48` 정렬 키에서 길이 · `how` 키 지움 · `_order_key` 그대로 | ✓ |
| 같은 개념 한 번 | `:49-54` `seen` 그대로 | ✓ |
| `matched` = `{span}`(= 입력 norm) · `start` · `covered_by` · `how` · `full` 없음 | `:55` · `headers.MATCHED_FIELDS = ("span",)` | ✓ |
| R7 · R9 지움 · §3-1 줄임 열쇠 색인 없앰 · §5-11 「두 판」 | `memory.py` 의 `abbr_keys_of` · `entry_by_abbr` · `abbr_keys` 지움 · `repository.py` Protocol 과 구현에서 두 메서드 지움 · `ABBR_*_MIN` 지움 | ✓ |
| 부록 A NM 줄 지움 | `headers.NM_ENTRY_COLUMNS` · `MATCHED_HOW` · `MATCHED_ABBR_FIELDS` 지움(R-1 ⓒ) | ✓ |
| `abbr` 주면 `invalid_argument`(O-32 (a) · A-3) | `resolve.py:28` 이 맞춤 꼴 · 목록 꼴 둘 다 막는다 · REST 쿼리와 MCP 인자는 남기고 설명은 「없앰」 | ✓ |
| 목록 꼴 불변 · `request.abbr` 없음 | `_listing` 에서 `abbr` 키만 빠졌다 · **실물 E4**(§5)에서 글자까지 같음 | ✓ |
| T29 도구 설명 문장 | `mcp_server.py:35-36` 에 SPEC 문장 그대로 · 부분 · 덮임 · 줄임 · `covered_by` 문장 지움 · 「고르지 않고」 남김 | ✓ |
| 오류 꼴 | `GoldInvalidArgument("abbr 는 0.8.0 에서 없앴다 — 주지 않는다")` → `invalid_argument: …` · 다른 입력 오류와 같은 접두 · REST 422(ERRORS 표) | ✓ |

## 3. 남은 흔적 grep(볼 것 3)

`rg -n "abbr|줄임|covered_by|HOW_|MATCHED_|NM_" backend/app`:
- 허용 줄만 남았다: `resolve.py:7` (docstring) · `:27-29` (서명 · 거절) · `router/gold.py:54,57` · `mcp_server.py:41,153,155` · `swagger_docs/gold.py:15` · `service.py:63-64`(넘기기만) · `headers.py:109 MATCHED_FIELDS`. **허용 밖 0.**

`backend/tests` 에서 남은 줄은 전부 「없음」 단언(`_no_key` · `hasattr` 부정 · T29 의 `not in`) · `abbr` 거절 표 · 스키마에 `abbr` 이 남는다는 단언(`test_gold_v07_compat.py:92` — A-3 그대로)이다. 다만 **주석 · docstring 둘이 옛 뜻 그대로다**(L-1 · L-2).

## 4. 시험(볼 것 4)

### 4-1. 돌린 것(WORK-016 §7 의 10 파일만 · 전체 pytest 안 돌림)

| 판 | 명령 | 결과 |
|---|---|---|
| 합성(데이터 env 없음) | `DATABASE_URL=sqlite+aiosqlite:///:memory: uv run pytest <10 파일> -q -rs` | **299 passed · 36 skipped**(skip = `@needs_gold` 실물) |
| 데이터 env(`$SM` gold · silver · ledger + `medallion-pg.env` 를 `set -a; .; set +a`) | 같은 10 파일 | **335 passed · 0 skipped** · 33s |
| `ruff check` 고친 파일 16 | | All checks passed |

파일: `test_gold_tools_synthetic` · `test_gold_contract` · `test_gold_mcp` · `test_gold_v07_compat` · `test_medallion_repo` · `test_gold_coverage` · `test_gold_real` · `test_gold_v07_descend` · `test_gold_v07_site` · `test_gold_rest`.

### 4-2. 지운 시험 = 계약 변경 몫만인가

`HEAD` 와 지금의 `test_` 함수 이름을 파일마다 견줬다:

| 파일 | 지움 | 새 이름(고침) |
|---|---|---|
| `test_gold_v07_resolve.py` | 16(파일째 · 전부 T26 NM) | — |
| `test_gold_tools_synthetic.py` | `test_resolve_overlap_all_and_order` · `test_resolve_one_per_entity_longest_span` · `test_T15_covered_only_when_every_occurrence_covered`(H-8) | `test_T15_resolve_wide_candidates` → `test_T15_resolve_exact_name`(H-9) · 새 `test_T26_abbreviated_name_no_candidate`(옮겨 온 남는 확인) |
| `test_gold_v07_compat.py` | `test_T27_resolve_abbr_off_06_shape`(H-4) · 상수 `TEXTS` · `MATCHED_06` · `RESOLVE_REQUEST_06`(R-6 ⓒ) | — |
| `test_gold_coverage.py` | — | `test_T15_real_concepts_per_question` → `test_T15_real_exact_name`(H-15) |
| 그 밖 6 파일 | 0 | 0 |

**지움 20 = 16 + 3 + 1**(WORK 셈과 같음). 지운 것은 모두 부분 일치 · 덮임 · 줄임 · `abbr=off` 규칙의 시험이다. 계약과 무관한 시험을 지운 자리는 없다. 36 의 「겹침 → `PRC-902` · `CON-904` · `ambiguous`」 는 `test_T15_resolve_exact_name` 이 다시 본다.

### 4-3. 고친 기대값의 출처

| 자리 | 새 기대 | 출처 |
|---|---|---|
| H-9 `test_T15_resolve_exact_name` | 이름 · 별칭 → 1 후보 · `matched == {span: norm(text)}` · 문장 · 조사 · 일부 · 이어 쓴 글 → 0 · 겹침 2 + `ambiguous` · 표 순서 | §4-1 · R1 · R2 · R5 · R6 · `_brute` = `norm == q` |
| H-15 `test_T15_real_exact_name` | norm 마다 직접 센 개념 집합 = 후보 · `len(by_norm) == 2541` · `overlap == 99`(`_same_build` 일 때) · 37 문장 → 0 | SPEC §5-1 R7 「2,541」 · §4-1 「norm 99개」 — 시험이 낸 수가 아니라 SPEC 의 수다. 지금 데이터 해시 `8accbb21…` = `SPEC_HASH_PREFIX` 라서 **이 단언이 실제로 돌았고 통과했다** |
| H-14 | `name` → PRD-416 · `name + "께서"` → 0 | R5 |
| H-11 · ERRORS | `abbr` = on · off · x · 목록 꼴 + off → 422 | O-32 (a) · 기존 `invalid_argument` 상태 코드 |
| H-12 `SAME_V07_PATHS[0] = ("total", 1)` | 이름 하나 → 후보 1 | §4-1 |
| H-17 · R-1 | `SYN_CALLS[0]` = 「겹침」 · `V07_CALLS[0..1]` = 이름 하나 · **비어 있지 않음 단언을 더함**(`test_gold_contract.py:208,218`) — 빈 검사로 통과하는 것을 막았다 | R-1 ⓑ |
| H-1 | 앞 8 문항 가운데 `entry_text` 가 있는 것만(이 검수가 셈: **뺀 문항 0**) | WORK H-1 |

### 4-4. `SECOND_END`(H-16 · Q21) 대 gold 근거

`test_gold_real.py:54` `SECOND_END = {"Q21": ("스킨부스터",)}` 를 실물로 확인했다:
- `g_entry.csv` `GEN-00004,스킨부스터,스킨부스터,modality,M4,…,이름` — 주석과 같다. `resolve(text="스킨부스터", range="동시 가능")` → `modality:M4` 1 후보 · `in_range` 참.
- `g_package.csv` `GPK-00151 ~ 153`(`PKG-0034` · 같은 날 조합)의 item 은 `procedure:PRC-311` · `modality:M8` · `modality:M4` 다. 주석과 같다.
- **`SECOND_END` 를 비우고 T4 를 돌리면 실패한다**(`Q21 missing GPK-00151/152/153` · 이 검수가 세션 임시 스크립트로 import 해서 돌림 · 파일은 안 고침). 상수가 Q21 하나를 정확히 메운다.

H-16 에서 「문장 쪽만 내던 입구 수를 먼저 센다」 를 이 검수가 다시 셌다. 18105(0.7.2)의 `entry_text ∪ question` `in_range` 합집합과 0.8.1 `entries()` 를 견줬다. **19 문항에서 문장 쪽 입구가 빠졌다**(Q03 · 05 · 06 · 09 · 10 · 12 · 13 · 14 · 18 · 19 · 20 · 22 · 23 · 25 · 30 · 31 · 33 · 36 · 37). 그래도 T4(37 문항 pointers ⊂ 도구 길 행)는 Q21 말고는 그대로 선다. 빠진 입구는 대부분 부분 일치로 끼어든 것이다(예: `PRC-001` · `M1` · `MAT-200`). → I-2.

## 5. 실물 — 18105(0.7.2) GET 과 이 판(in-process) 대조(볼 것 5)

서버는 띄우지 않았다. 이 판은 데이터 env 로 `real_tools()` 를 써서 in-process 로 불렀고, 18105 에는 GET 만 보냈다.

| # | 확인 | 결과 |
|---|---|---|
| E1 | `gold_hash` | 18105 = in-process = `8accbb21…` |
| E4 | `tables=concern,site,modality,procedure,product` 를 `limit=500` 으로 끝까지 | 두 쪽 모두 3 쪽 · `counts.entities` **820**(SPEC 수와 같다) · `build.loaded_at` · `request.abbr` · cursor 값을 빼면 **모든 쪽이 글자까지 같다** · 새 판 `request` 에 `abbr` 없음 |
| E2 | 다섯 표의 서로 다른 norm 1,122 마다 행 `text` 로 맞춤 꼴 → 0.7.2 의 「`span == norm`」 후보 집합과 견줌 | **다른 것 1**: 「피부 손상」 — 0.7.2 는 `concern:CON-222` 를 `how=줄임` · `full=피부장벽손상` 으로 더 냈다. 0.8.0 에서 지운 줄임 맞춤이라 **계약대로**다. 그 밖 1,121 은 같다 |
| T15(실물 시험 안) | 전체 norm 2,541 · 겹침 99 · 37 문장 → 0 | 통과 |

## 6. 비밀값(볼 것 6)

`git diff HEAD -U0 | grep -iE "postgresql(\+asyncpg)?://[^<]|passw|secret|token|api[_-]?key"` → **0**. 접속 값은 `set -a; . 파일; set +a` 로만 썼고, 화면 · 이 파일에 찍지 않았다.

## 7. 지적 표

| # | 파일:줄 | 심각도 | SPEC 절 | 무엇 | 고칠 방향 |
|---|---|---|---|---|---|
| L-1 | `backend/tests/gold_fixture.py:10-12` · `:56` · `:60-67` | Low | §5-11 NM 지움 · §3-1 | `v07` 판 머리말과 행 주석이 아직 0.7 줄임 뜻이다(「줄임 열쇠가 서는 …」 · 「줄임 열쇠는 NM1 식으로 시험이 따로 짓는다」 — 그 시험 파일은 지워졌다 · 「같은 조각이면 부분이 앞」). H-13 은 5 행만 고쳤다. 표본 행 자체는 B-3 대로 남기는 게 맞다 | 「0.7.2 까지 줄임 꼴 표본 — 0.8.0 에서는 『줄인 글 → 후보 0』 재료(`test_T26_abbreviated_name_no_candidate`)」 로 한 줄. 행 주석의 「부분이 앞」 은 지운다 |
| L-2 | `backend/tests/test_medallion_repo.py:157` | Low | §5-11 | `test_dt10_tool_responses_equal_v07` docstring 의 「(줄임 · filter 짝 …)」 — 자리 0 은 이제 「이름 하나 → total 1」 이다 | 「줄임」 → 「이름 하나」 |
| L-3 | `backend/tests/test_gold_mcp.py:48` | Low | §4-1 T29 | 「없어야 할 조각」 에 영어 낱말 `how` 가 있다. 설명 어디에든 `how` 가 들어가면(예: 다른 도구 문장 · `_COMMON`) 잘못 걸린다. 지금은 통과 | `"matched.how"` · `"how ="` 처럼 좁히거나 `"how"` 를 뺀다(`covered_by` · `줄임` 으로 충분) |
| I-1 | `backend/app/modules/gold/repository.py:45,112-114` · `memory.py:46` | Info | §3-1 · SPEC-003 §5 P1 | `entry_norms()` 는 이제 `app/` 어디서도 안 쓴다(부분 일치용이었다). WORK 가 지우라고 하지 않았고, 지우면 Protocol 메서드 수가 또 바뀐다(A-1) | 남겨도 계약 위반은 아니다. A-1 되적기 때 −2 로 둘지, `entry_norms` 까지 −3 으로 할지 코디가 정한다 |
| I-2 | `backend/tests/test_gold_real.py:54-67` | Info | §4-1 · O-33 | 문장 쪽 입구가 19 문항에서 빠졌다(§4-4). T4 는 서지만 `entries()` 가 내는 입구가 0.7.2 보다 좁다. 특히 **Q33 `entry_text` 「코그 실 리프팅」 은 0.8.1 에서 후보 0** 이다(`offer_name_contains` 로만 pointers 가 닿는다). 「이마 주름」 · 「턱선 처짐」 · 「볼 주름」 은 복합 고민 하나로만 풀리고 부위 · 단일 고민 입구는 빠진다 | 시험은 고치지 않아도 된다. 시험 앱 답 키(O-33) · 상담 목록 꼴이 이 꼴의 `entry_text` 를 어떻게 다루는지의 재료로 넘긴다 |
| I-3 | `backend/app/modules/gold/resolve.py:28` | Info | O-32 (a) | 검사가 `abbr is not None` 이라 REST `?abbr=`(빈 값)와 MCP `""` 도 거절한다. MCP `null` 은 통과한다. SPEC 「주면 거절」 과 맞고 REST · MCP 가 같다 | 없음(기록만) |

## 8. 코디 몫(이 검수 밖)

- 허브 브랜치 커밋 · 18105 재시작(앱 0.4 와 같이 · 시험 앱 옛 허브 자리 먼저 — R-7).
- SPEC 되적기 후보: A-1(Protocol −2 · I-1 을 함께 정함) · A-3 「스키마에 남고 설명은 『없앰』」 · A-5 ★ 수(H-17 을 넣어 ★ 7).
- L-1 ~ L-3 은 커밋 전에 한 번에 고치거나 다음 판으로 미룬다(동작 영향 0).
