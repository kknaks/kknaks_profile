# review-code-v052-hub — 허브 0.5.2 코드 검수(WORK-007 구현분)

- 검수 워크트리: `PROCEDURE-HUB/phub-gold-jev`(미커밋 · gold 파일 전부 untracked — 0.5.1 판과의 git diff 는 없다. 코드는 현재 판을 계약에 직접 대조했다)
- 읽은 것: WORK-007 · SPEC-001 0.5.2(§4-2 · §4-4 · §4-5 · §4-6 · §4-9 · §5-5 H5 · H6 · §5-9 HG1 ~ HG3) · review-work-v052(H-1 · H-2) · impl-v052-hub-report · _RESUME §2 11-17(U-3 (a)(가) · U-4 (a))
- 손대지 않음: 파일 수정 0 · stash · checkout 0 · `.env` 안 열었다 · 18105 · 18106 · 18220 띄우거나 내리지 않음(18106 은 GET 만)

## 판정: **PASS**(WARN 0 · NOTE 6)

FAIL 0 · WARN 0. 계약 위반 · 폭을 줄이는 자리 · 기대값을 구현에 맞춰 내린 시험은 찾지 못했다. NOTE 는 코드에 막힌 것은 아니고 앱 · SPEC 되적기 · 다음 판 몫이다.

## 1. 검증(직접 1회)

| 무엇 | 명령 | 결과 |
|---|---|---|
| ruff | `uv run ruff check app tests scripts` | All checks passed |
| pytest(데이터 env · README · WORK-001 §2-4 대로 `$SM/gold` · `$SM/silver` · `$SM/notes/ledger-check-list.csv`) | `DATABASE_URL=sqlite+aiosqlite:///:memory: uv run pytest --ignore=tests/integration -q -rs -p no:cacheprovider` | **638 passed · 2 skipped**(37.4 s) — 보고 수와 같다. skip 은 둘 다 gold 무관(`test_db_resilience.py:119` 격리 PostgreSQL URL 필요 꼴) |
| 18106 이 지금 코드인가 | 프로세스 시작 11:29:26 · gold 코드 마지막 수정 11:28:28(`headers.py`) | 현재 코드로 떠 있다. health: gold_hash `8accbb21…` · aux_hash `6435fe41…` · files 22 · expected_hash_checked true · integrity 넷 0 · aux.concern_site {95, 85, 51} |

## 2. WP 마다 완료 조건 · 계약 대조

| WP | 완료 조건 | 코드 근거 | 판정 |
|---|---|---|---|
| WP-1 보조 ③ | 세 칸 읽기 · 없음/칸 없음 = 시작 실패 · aux 6 파일 · gold 해시 불변 · 22 줄 | `inputs.py`(concern_site 블록 — `_read_bytes` 실패 · `lack` → `GoldLoadError` · `FileRecord(…, "aux")`) · `gold_hash` 는 `files`(gold 15 + questions)만으로 — aux 는 `aux_hash` 만. 18106 gold_hash = 11-16 값 · aux_hash 달라짐 | 통과 |
| WP-2 HG2 | 닫힘 함수 하나 · 네 자리 · descend · depth/via · 한 holder 한 번 · 순환 끝 | `closure.py` `lower_closure` / `target_holders` 를 `service.scope` · `facets._target` · `pairs._holders` · `coverage._target`(lineup) 가 공유. 시작은 대상의 「하위 *」 행뿐(`one_step(…, follow)`) · 따라가는 role = 요청 role ∩ 하위 셋 · 너비 우선 + 단마다 gid 정렬 + `seen`(대상 포함) | 통과 |
| WP-3 HG1 | 행 0 고민만 · 가장 가까운 하나 · 같은 행 전부 · hier · ledger 요청 코드만 · coverage 같은 함수 | `concern.py:110-128` `concern_rows` — `asked_rows` 가 1 이상이면 그대로(쪽 밖 목록 포함 → 「묶음만 0」 고민은 안 바뀐다 · U-3 (a)) · `parent_of` 한 단씩 · 첫 행 있는 윗고민에서 return · 순환 가드 `seen`. `ledger_check(ctx.repo, [code])`(`:101`) · `coverage._value` 가 `concern_rows` 를 그대로 부름(`coverage.py:128`) | 통과 |
| WP-4 HG3 | 글자 ∪ 묶임(+ 자손) · site_match · by_site_match · 부위 계층 안 넓힘 · resolve 손 안 댐 | `concern.py:49-65` — 행 집합은 `all_rows` 에서 (i) 또는 (ii) 로만 걸러진다(0.5.1 의 (i) 행은 전부 남는다 = 넓어지는 쪽만). `bound_concerns`(`:131-142`) = 이름이 글자 그대로 같은 site 입구 → `concern_site_by_site` → 고민 + `descendants("concern")`. 부위 쪽 `descendants("site")` 호출 없음(HG3-5). `resolve.py` 는 11-16 뒤 안 바뀜(mtime) | 통과 |
| WP-5 | T3 · tool_list · 다시 센 수 · e2e 꼴 · README · 커밋 grep | `test_gold_holes.py` 40 시험 · README gold 절 보조 입력 · 새 입력 줄 · `.env.example` 한 줄. 다시 센 수는 §6 | 통과 |

**H-1**(N-3 13 짝의 `via[]`): `test_T21_real_via_product_path`(`tests/test_gold_holes.py:485`) — 실물에서 마지막 거침이 product 인 길 한 건을 찾아 `facets` profile 응답에서 `layer.depth ≥ 2` · `via[-1]` = 그 제품 · 그 제품의 `하위 제품` 행이 holder 를 가리킴을 단언. 반영됨.
**H-2**(「4 단」): `test_gold_holes.py:476-481` — 그래프 셈(하위 role 행을 직접 이은 가장 긴 길)만 `== 4` 로 단언하고 응답 `depth` 최댓값(2)은 보고만. 반영됨.

## 3. 원칙 셈 — HG2-2 형제 섞임 · HG1 · HG3

**HG2-2 형제 섞임 0 — 셈 한 건(내가 실물로 직접)**: 물려받음 holder(그 시술)에서 `하위 제품` 으로 내려가면 닿는 형제 제품이 가장 많은 제품 `PRD-356`(형제 holder 82)을 골라 `facets(roles = 자기 · 물려받음 · 하위 제품)` 를 끝까지 넘겼다.

| facet | 응답 total | 응답에 든 형제 holder | 형제 쪽에서 내려갔다면 더 붙었을 행 | 응답 depth 최댓값 |
|---|---|---|---|---|
| profile | 5 | **0** | 82 | 1 |
| adverse | 71 | **0** | 337 | 1 |
| indication | 65 | **0** | 583 | 1 |

전 대상 858 · role 다섯 전부로 `target_holders` 를 돌린 셈: depth ≥ 2 holder 가 그 대상의 하위 그래프 자손이 아닌 것 **0** · depth 1(자기 · 물려받음 등)로 닿은 holder 가 depth ≥ 2 로 다시 나온 것 **0**.

**HG1**: `asked_rows` 가 1 이상이면 곧장 그대로 돌아가므로 자기 행이 있는 고민에 윗고민 행이 섞일 길이 없다(H6). 18106 실물: `CON-002`(표정주름) self 176 → `inherited_from: null`. `CON-012` → `CON-008` steps 1 · 묶음 65 · 행 181 · `LCK-010`(요청 코드의 것) · `upper=none` 이면 total 0 + `LCK-010`. 「가장 가까운 하나」 는 첫 hit 에서 `return` 하는 구조로 선다.

**HG3**: 넓어지는 쪽만 — 18106 `CON-001` × `이마`: 73 행 · 묶음 16 · by_site_match {column 24 · concern_site 54}(겹침 5) · unfiltered_rows 524. 시험 `test_T22_real`(97 짝 전부 0.5.1 집합 ⊂ 0.5.2)이 단언한다.

## 4. 고친 기존 시험 9 곳 — 계약 변경 때문인가

| # | 시험 | 바뀐 것 | 근거 | 기대값을 내렸나 |
|---|---|---|---|---|
| 1 ~ 4 | `test_hash_formula_and_record_synthetic` · `test_T1_real_load_counts_and_hash` · `test_gold_tools_synthetic::test_health` · `test_gold_rest::test_health_and_tools` | files 21 → 22(T1 은 aux 6 줄 단언 더함) | SPEC §2-3 4 · WORK-007 §3 완료 조건 3 | 아니다(늘었다) |
| 5 | `test_T16_modality_lower_holders`(`test_gold_coverage.py:84`) | adverse (1,3,2,0) → (1,4,3,0) · lineup (0,2,2) → (0,3,3) — 0.5.1 값을 주석에 남김 | HG2 — §4-9 lower · §5-9 HG2-5 | 아니다(늘었다) |
| 6 | `test_T16_value_and_attr_nodes`(`:93`) | 고민 indication.inherited None → 0 | HG1-6 · §4-9 `inherited` | 아니다(null → 수) |
| 7 | `tool_counts`(`:150` — T16 불변식 헬퍼) | 고민 노드를 `self_rows` · 물려받은 응답의 `counts.rows` 로 | HG1-6 — 공개 도구로 세는 식 유지(안쪽 함수 안 씀) | 해당 없음(셈 식) |
| 8 | `test_gold_contract.py` `ROW_COMPUTED` 등 | 계산 필드 depth · via · site_match · inherited_from · counts 꼴 허용 | 부록 A 0.5.2 계산 필드 | 아니다(허용 필드 추가) |
| 9 | `test_T4_Q10_empty_pointers_is_zero_with_ledger`(`test_gold_real.py:181`) | `upper=none` → total 0 + LCK-010 · 기본값 → inherited_from · total > 0 · self_rows 0 · LCK-010 | WORK-007 §5 완료 조건 4 그대로 | 아니다 — 0.5.1 단언(total 0)은 `upper=none` 으로 살아 있다 |

목록 밖 기존 시험 변경: 주석만(T23 표지 · item_* 15 · 11 = HG2 앞 수 주석). `test_T16_real_counts_reproduce_spec` · `test_T16_real_invariant_all_target_nodes` 는 손 안 대고 통과(보고 · 내 실행 일치). **기대값을 구현에 맞춰 내린 것 0.**

## 5. gold 불변 · aux_hash · 지어낸 동작

- gold 15표 · gold 해시: 바뀌지 않는다(`gold_hash` 식에 aux 파일 없음 · 18106 · `test_aux3_changes_aux_hash_not_gold_hash`).
- aux_hash: `source_ref` + 계층 3 + `concern_site` + 원장 = 6 파일(이름순 결합식 그대로) · 옛 cursor 는 build 묶임으로 `cursor_invalid`.
- 지어낸 동작 — SPEC 에 없지만 WORK §10 「구현 때 정함」 범위 안인 것만 있다: A-2 `health.aux.concern_site{rows, concerns, sites}` · A-4 `unfiltered_rows` = 이 응답이 site 없이 낼 행 수 · A-5 `{"by": …}` · A-7 holder 순서 · A-8 roles 없음 = 하위 셋 · 같은 depth 동점 = 마지막 단 `g_scope.gid` · 방문 집합에 대상 포함. 전부 보고서 「SPEC 되적기 후보」 에 올라 있다. 폭을 줄이는 결정은 없다.

## 6. 다시 센 수(W-2) — SPEC 되적기 필요(코드 문제 아님)

| 수 | SPEC | 다시 셈(구현 보고 · 시험이 직접 셈) |
|---|---|---|
| 케이스 끝 `g_pair` | 129 | 서로 다른 gid **100** · 계열마다 더함 **104** |
| 97 짝 행 합 | 289 → 1,700 | 289 → **1,722**(검수 셈과 같다) |
| M2 adverse(하위 셋) | Q12 줄 +188 | adverse_detail 276 → 464(+188) · adverse 206 → 246 — 18106 GET 으로 같은 값 확인 |

## 7. NOTE

| # | 파일:줄 | 무엇 | 고칠 방향 |
|---|---|---|---|
| N-1 | `app/modules/gold/closure.py:85-89` `target_holders` | 한 단(`자기` · `물려받음` 등) holder 와 닫힘 depth ≥ 2 holder 의 겹침을 막는 장치가 없다 — 같은 holder 가 두 layer 로 두 번 나올 수 있다. 실물 0(내 셈) · HG2-3 은 닫힘 안의 「한 번」 이라 계약 위반은 아니다 | 다음 판에 `seen` 을 base holder 로 시작하거나 시험 한 줄(실물 0 단언) |
| N-2 | `app/modules/gold/memory.py` 보조 ③ 색인(`if not (c and st): continue`) | 빈 코드 행은 말없이 빠지는데 `n_concern_site`(health rows)는 전체 행 수다. 실물 95 행은 모두 채워져 있어 지금은 무해 | 빈 칸 행을 시작 실패나 health 수로 드러내기(SPEC 에 없음 — 되적기 때) |
| N-3 | `app/modules/gold/coverage.py:127-128` | 고민 노드에서 `asked_rows` 를 두 번 센다(`concern_rows` 안에서 한 번 더) — 값은 같고 성능만 | 정리 몫 |
| N-4 | REST 목록 입력(기존 꼴) | `roles=a&roles=b` 처럼 키를 되풀이하면 **마지막 값 하나만** 먹고 오류 없이 답한다(쉼표 `roles=a,b` 가 맞는 꼴). 이번 검수에서 내가 처음 이 꼴로 불러 M2 adverse 를 150(실제 246)으로 잘못 읽었다 — 사람이 REST 로 확인할 때 만날 함정 | `invalid_argument` 로 막거나 README · api-docs 에 「쉼표」 한 줄(0.5.1 부터의 꼴 — 이번 판 지적 아님) |
| N-5 | SPEC §5-9 · SPEC-002 §9-3d | W-2 수 둘(129 · 1,700)이 다시 나오지 않는다 | 코디 되적기 — 100 · 104 / 1,722 |
| N-6 | 앱 쪽 | 기본 roles(자기 · 물려받음)로 M2 adverse 를 부르면 `ADV-051` 행이 1 행뿐이다(하위 셋을 줘야 23 — 0.5.1 W-4 의 설명이 이것을 말한다) | 앱 실물 확인(WORK-008 WP-6)에서 「필러 혈관 폐색」 이 하위 셋으로 불리는지 본다 |

## 8. 커밋 후보 grep(공개 레포)

대상 = `backend` 에서 `git ls-files -mo --exclude-standard` 가운데 gold · README · env.example(36 파일).

| grep | 결과 |
|---|---|
| `/Users/` · 사용자 이름 · 회사 메일 도메인 · `sk-ant` · 긴 `sk-…` 키 · `GOLD_EXPECTED_HASH=값` | **0**. 걸린 것은 gold 해시 `8accbb21…`(`test_gold_load.py:18` · `test_gold_holes.py:379` · `test_gold_coverage.py:260`) — SPEC §2-3 3 에 적힌 내용 해시라 키 · 데이터 본문이 아니다(0.5.1 판부터 있던 꼴) |
| 5 자리 gid 글자(`G..-0000n`) | `gold_fixture.py:190 · 242-248` · `test_gold_contract.py:138 · 191` — 전부 합성 fixture 의 가짜 행(이름 「사건뿌리」 · 「시술가」 · 코드 `PRC-901` 꼴)이다. 실물 gid 박힘 0(실물 시험은 `questions.csv` 에서 읽는다) |
| 시험 문자열의 시술 · 고민 · 부위 이름 | 0 — `test_gold_holes.py` 의 한글 문자열 상수는 「파일 없음」(오류 문구) 하나. 실물 단언은 SPEC 에 적힌 코드(`CON-…` · `SITE-…` · `CSI-…` · `LCK-…` · `M2`)와 수만 쓴다. 부위 이름은 시험이 `g_entry` 에서 읽는다 |
| ignored | `.pytest_cache` · `.ruff_cache` · `.venv` · `__pycache__` 만 — 데이터 · `.env.gold` 는 저장소 밖 경로 |

참고: 이 검수 중간에 디스크가 한 번 가득 찼다(ENOSPC — Claude 임시 폴더 볼륨). 잠시 뒤 풀려 grep 은 돌렸다. 18106 · 18105 쪽에 영향이 있었는지는 보지 않았다.

## 9. 사용자가 실물에서 만날 자리(18106 GET)

| 질문 꼴 | resolve | 허브 응답(0.5.2) | 만날 것 |
|---|---|---|---|
| 「이마에 주름」 | `CON-001` 주름 · `SITE-014` 이마 | `concern_candidates(CON-001, site=이마)` → 묶음 16 · 행 73 · by_site_match {column 24, concern_site 54} · unfiltered 524 · inherited_from null(upper auto/none 같음) | 0.5.1 의 24 행(글자만)에서 73 행 — e2e 4 구멍이 막혔다. 행마다 `site_match[]` 로 「부위 칸으로 맞음」 / 「묶인 고민으로 맞음(CSI-0001)」 이 갈린다 — 앱이 이 표지를 답에 밝히는지는 앱 몫 |
| 「볼 주름」 | `CON-012` 볼 주름(「주름」 · 「볼」 은 `covered_by` 볼주름) | 기본 → `inherited_from {CON-008, steps 1}` · 묶음 65 · 행 181 · self_rows 0 · `LCK-010` · 모든 행 `hier.match = 상위` / `upper=none` → 0 + `LCK-010` / (볼을 따로 걸면) 7 행 · column 7 · concern_site 0 | 0.5.1 에서 0 이던 Q10 이 윗고민 깊은 주름으로 답할 재료를 얻었다. 행의 `asked_concern_code` 는 `CON-008` 그대로라 앱이 머리 `inherited_from` 을 놓치면 「볼 주름 전용」 으로 읽을 수 있다 — 앱이 층을 밝히는지 확인 |
| 「필러 혈관 폐색」 | `M2` 필러 · `ADV-051` 혈관 폐색 | `facets(M2, adverse)` 기본 roles total 33(ADV-051 1 행) / 하위 셋 roles total 246(ADV-051 23 행 · depth 1 · 2) — `descend=one` 이면 206 · 21 행 / 값 쪽 `adverse:ADV-051` total 29 / coverage M2 adverse (33, 213, 45, 0) | 하위 셋을 줘야 23 행이 나온다(N-6). 응답이 커진다(adverse_detail 464) — 자르지 않는 계약(O-26)이라 앱 · LLM 쪽 길이 확인 |
| 「표정주름」 | `CON-002` 표정주름(「주름」 은 covered) | 묶음 21 · 행 176 · self 176 · inherited_from null | 자기 행이 있어 0.5.1 과 같다(HG1 안 걸림 — U-3 (a) 그대로) |

## 10. 남은 것

- 디스크 여유 확인(검수 중 ENOSPC 한 번 — 앱 실물 · runs 를 쓰기 전에).
- SPEC 되적기: A-2 · A-4 · A-5 · A-7 · A-8 · 동점 규칙 · W-2 수 셋(§6).
- 앱 실물(WORK-008 WP-6): 볼 주름의 층 밝힘 · 필러 혈관 폐색 하위 셋 · 이마 site_match 읽기.
