# 코드 검수 — 앱 0.5.2(WORK-008) + app-key-fix1

- 날짜 2026-11-17 · reviewer_code(read-only) · task_988a294937b1
- 대상 워크트리 `clinic_chat/phub-gold-jev`(미커밋 · base `origin/main` 240c321 — 앱 코드 전부 untracked 라 git diff 없음 → 보고서가 적은 바뀐 파일을 직접 읽음)
- 계약: SPEC-002 0.5.2 · WORK-008 0.1.0 · review-work-v052 A-1 ~ A-4 · `_RESUME` §2 11-17 행(B-1 · U-1 · U-2 · 답 키 검토)
- 실호출: Jev · LLM 0. 허브는 **18106 GET 만**(답 키 다시 뽑기 재현 2 회 — 출력은 스크래치 폴더, 워크트리 · `data/` 안 씀). 18105 · 18106 · 18220 띄우거나 내리지 않음. `.env` 안 열음.

## 판정: **WARN**(FAIL 0 · WARN 4 · NOTE 8)

WP-1 ~ WP-6 의 완료 조건과 A-1 ~ A-4 는 섰다. 키 쪽은 깨끗하다 — 키 전용 기준 대상은 B · C 에 안 가고, `expected_kinds_by_entry` 를 따라야 하는 곳은 다 따르며, (다) 답 키는 **바이트까지 같게** 재현됐다. 고칠 것은 B 걷기의 일반 규칙 둘(F2 · F3 원인 — W-1 · W-2)과 기록 하나(W-3)다. 셋 다 0.5.2 가 새로 만든 것이 아니라 0.5.2 실물에서 드러난 앞 판의 규칙이다.

## 1. WP · A 완료 조건

| WP / A | 결과 | 근거(직접 확인) |
|---|---|---|
| WP-1 세트 칸 | 통과 | `_v052a` ↔ `_v052b` ↔ 본 세트를 칸 단위로 대조: a→b 는 키 전용 칸 셋(Q03 · Q12 `key_lower_entries` · Q10 `key_upper_entries`)만 빠짐 · b→c 는 Q03 · Q05 만(`expected_kinds` + `key_fix1` + Q03 `expected_kinds_by_entry{procedure_case:CAS-016: [overview, mechanism, indication, outcome]}`). `loader --validate` → `{"lines": 85, "errors": []}`. `loader.py:25 · 31-39 · 59-68` 선택 칸 꼴 검증 |
| WP-2 허브 응답 받기 | 통과(W-3 · N-3) | `required.py:24-36` 머리 `inherited_from` → `UPPER` 표지 · `layer_bucket` 이 그 표지로 `inherited`(`hier.match` 로 가르지 않음 — B-5) · `inherited_via` 기록(`:104-106 · 124-126`). 표지 `layer_depth`(늘) · `layer_via`(얻었을 때만) · `site_match`(BR1 두 말 그대로 — `material.py:25`) · `inherited_fill`(`material.py:28-31`) · K4(`gate.py:107-117`). `csi_ids` · `inherited_from` 코드 · 이름 못 얻은 via 는 `verified_lines` 에만(`material.py:177-181`) |
| WP-3 다시 뽑기 · 대조 | 통과 | 아래 §2 ② |
| WP-4 구멍 꼴 | 통과(N-6) | `pick-holes.json` `question` 비움 · `set.jsonl` 밖 · `BUNDLE_COUNTS` 85 그대로(`loader.py:27-28`) |
| WP-5 되적기 확인 | 통과 | `judge.md` §8-3 문장 · `pick.py:9` 주석 · N-5 단언(`test_walk_core`) |
| WP-6 실물 · 마감 | 통과(N-5 · N-7) | runs 4 줄 `efforts {b: low, c: low}` 확인. 화면 F2 확인은 안 함(보고에 밝힘) |
| **A-1** | 닫힘 | `expected_kinds` 읽는 곳 전수(grep): 대상별로 따르는 곳 = `key_calls.build_spec`(`:236-240`) · `spec_from_item`(`:305-309`) · `narrow_by_entry`(`:140-155`) · `answer_key.kinds_met`(`:180`) · `build_key`(`:294-295`) · `key_table`(`:76` 합집합을 돌되 줄은 `kinds_met`). 합집합 그대로 = `report.py:229`(종류 지표) · `quality/checks.py:201`(D11 — 「물었나」 문항 단위라 맞음) · `walk/calls.py:273-278`(좁혀진 `c.kinds` 를 받음). 빠진 곳 0 |
| **A-2** | 닫힘 | `_v052a/` 복사본 존재(set · calls · answer-key · summary · table) · (나) = `_v052b` 사본 · (다) 에서 본 세트의 키 전용 칸 지움 — 위 칸 대조로 확인 |
| **A-3** | 닫힘 | K4 는 `layer_depth` 만 요구(`gate.py:111-113`) · 이름은 같은 응답 depth 1 holder(`verified.py:165-169`) → 없을 때만 `label` 조회 + `label_for: layer_via`(`col_b.py:78-91`) |
| **A-4** | 닫힘 | F1 ~ F4 runs 줄 `efforts` = low/low(속도 탭 API) |

## 2. 키

**① 키 전용 기준 대상을 B · C 에 안 줌 — 통과.** B · C 는 질문 글만 받는다(`runner.py:205-216` — `--set-id` 도 `item["question"]` 만). 세트 · 명세의 대상 목록을 읽는 곳은 `spec_entries`(`loader.py:142-146` — `upper_of` · `lower_of` 뺌) · `report.py:217`(세트 `expected_entries` — 키 전용 칸은 다른 칸) · `key_table.py:54` 뿐. 0.5.2 (다) 세트에서는 키 전용 칸 자체가 0.

**② `expected_kinds_by_entry` 를 따라야 하는 곳 — 전부 따름**(A-1 표). 명세는 읽기 호출만 좁히고(케이스 `lineup` `scope` 빠짐) 판정용 호출은 범위 나머지 그대로(`key_calls.py:161-166`) — SPEC §5 (가) 의 「그 범위 조회 전체」 와 맞다. 칸이 없는 문항은 `_by_entry` 가 빈 dict → 명세 바이트 그대로(`test_no_by_entry_is_byte_identical_spec`).

**③ (나) · (다) 재현 — 바이트 같음.** 스크래치에 세트 사본을 두고 `EVAL_SET_DIR=<사본> HUB_REST_URL=…18106… answer_key --all`:

| 걸음 | 결과 |
|---|---|
| (다) 본 세트 | `diff -r` **차이 0**(37 키 전부 바이트 같음 · gold_hash `8accbb21…f6228c`) |
| (나) `_v052b` | 37 키 전부 **`script_sha256` 한 줄만 다르고 그 밖 0 줄**(N-1) |

(가)→(나)→(다) 셈도 다시 냈다(`(gold_table, gid)` 집합): (나) 다름 5 = Q12 483→487(+4 `g_adverse_detail`) · Q19 24→28 · Q20 9→12 · Q25 5→6 · Q27 7→9(+ 전부 `g_pair` · only_prev 0) · 기대 종료 앞뒤 같음 · 표본 같음. (다) 다름 2 = Q03 45→434 · Q05 3→75(+ `g_indication` · `g_outcome` 만 · only_prev 0) · 「상태 안 맞음」 → 「근거 충족」 · 표본 1/7 → 7/7. 보고서 수와 같다.

## 3. end_state `counted_rows` 를 HG1 표지로 넓힌 것 — SPEC (가) 와 부딪치나

**부딪치지 않는다(코드 맞음) · 단 SPEC 본문 두 줄이 서로 어긋나 되적기 한 줄이 필요하다(N-2).**

- 실물: Q10 키 행 263 = `g_indication` 181 이 **전부 `hier.match = 상위` + `inherited_from = CON-008`** · `g_profile` 82. 0.5.1 식(상위 행 빼기)만 두면 셀 행 0 → `ledger_check` 있음 → **(가)** 로 떨어진다.
- SPEC-002 §3-2 RQ1 0.5.2 불릿(372 행)은 「이 꼴은 원천 미확정 (가) 가 아니다 — 행이 0 이 아니다」 로 못 박았다. 그래서 넓힘은 SPEC 이 요구한 동작이다.
- 반면 §5 불릿(598 행)은 「(가) · (나) 를 셀 때 상위 고민 펼침 행(`hier.match = 상위`)은 뺀다」 를 예외 없이 적는다. 이 줄은 0.4.2 때 **facets package 값 쪽의 윗고민 패키지**를 빼려고 들어온 것이다(_RESUME 11-16 「앱 검수 뒤」 Q10).
- 코드는 둘을 머리 `inherited_from` 표지로만 가른다(`end_state.py:33-37` — `UPPER` 있으면 셈 · 없고 `상위` 면 뺌). package 쪽 `상위` 행은 머리 표지가 없어 그대로 빠진다(`test_hg1_self_concern_counts_self_and_package_upper_stays_out`). B 와 키가 같은 함수(`answer_key.py:34 · 120 · 133 · 245`).
- 판정 식(`unsettled_rows`)은 안 바뀌었다 — 셀 행만 넓어졌다. 덧붙여 Q10 키의 「근거 충족」 은 `expected_end_state_by = set` 이다(csv status 「원장 확인」 은 `STATUS_MAP` 밖 → (가) 가 안 나면 세트 값). 앞 판(`_v052a`)도 같다.

## 4. 미결 F2 · F3 — 원인과 고칠 방향(고치지 않음)

### W-1 · F3(Q12 B 「후보 소진」) — 필터로 쓴 입구에 required 를 따로 세운다

- **원인**: 대상이 둘 이상이면 사건 입구는 자기 조회 없이 다른 대상 조회의 **필터**가 된다(BR1 — `calls.py:154` `{"adverse_code": a.code}` · `:183` `not has_targets` 면 자기 조회 없음). 그런데 required 는 대상 × 종류마다 서고(`front.applicable` `front.py:66-68` 은 표 × 종류만 봄 → `adverse:ADV-051 × adverse` = 적용), 셈은 조회의 `node` · `a` · `b` · `concern_code` 로만 대상을 잇는다(`required.py:81-101`). 필터 칸(`filters.adverse_code`)은 안 본다 → ADV-051 줄은 행 0 → `met_by None` → 「후보 소진」. 실물 trace 에 그대로 찍혀 있다: `required` `adverse:ADV-051` self 0 · `coverage_mismatch {coverage: self 29, read: 0}` · 같은 행이 `modality:M2` 줄에는 `self 1 · lower 22` 로 잡힘(run `a804a471de82`).
- **키와 B 가 갈린다**: 키 `kinds_met`(`answer_key.py:184-195`)은 맞는 조회가 없으면 `hit = False` → 그 줄을 **건너뛴다**. Q12 키 `kinds_met` = `modality:M2.adverse=self` 한 줄. B 만 그 줄을 미충족으로 세운다 — 「B 와 키가 같은 함수」(N-2 · WORK-008 §4 완료 조건 5)가 이 꼴에서 깨진다.
- **고칠 방향**(일반 규칙): `target_rows` 가 조회 `request.filters` 의 `{표}_code`(`adverse_code` · `condition_code`)가 그 대상의 코드인 조회도 그 대상의 조회로 센다(필터 조회의 행은 정의상 그 사건의 행 · 좁힘이라 `coverage` 대조는 그대로 건너뜀). 키 `kinds_met` 도 같은 매칭을 쓰게 — 가능하면 `kinds_met` 이 `required.target_rows` 의 매칭 함수를 그대로 부르게 묶는다. 다른 길(필터로 쓰인 입구는 required 에서 뺌 — KD4 처럼 건너뜀)은 「물은 대상의 그 종류」 기록이 사라져 권하지 않는다.
- **고쳐도 Q12 B 는 「원천 미확정 (다)」 가 안 된다** — (다) 는 1회차 B 판정 밖(SPEC §5 600 행 · O-5 ②). 고친 뒤 기대는 「근거 충족」(알고 가는 어긋남). WORK-008 §8 F3 의 기대 「원천 미확정 (다) 그대로」 는 키 기대이지 B 기대가 아니다 — 보고서 미결 5 의 답.

### W-2 · F2(볼 주름 묶음 2) — 불확실해서 **넓히려고** 남긴 조각이 **필터**로 걸려 폭을 좁힌다

- **원인**: Jev 대상 판단(run `ba0678ffec2a`) = `concern:CON-012 볼 주름` 0.94 target · `concern:CON-001 주름` 0.56 · `site:SITE-051 볼` 0.37 — 뒤 둘은 사이 값 → **TG2 「넘김 쪽」 `uncertain_kept`**(`front.py:220-221`), 둘 다 `covered_by` = 「볼주름」(CON-012 이름의 덮인 조각). 그런데 부위 입구가 하나라도 있으면 고민 조회는 **부위마다 `site` 를 건 조회로 바뀐다**(`calls.py:175-180` — 부위 없는 조회는 내지 않음). 그래서 CON-012 는 `concern_candidates(CON-012, site=볼)` 2 후보로 좁아지고, 기대한 `concern_candidates(CON-012)`(키 Q10 = 65 후보 · 윗고민 CON-008 행 181)는 **불리지 않았다**. `required` 는 그래도 `inherited 7 · via CON-008` 로 서서 「근거 충족」 — 빠짐이 종료 상태에 안 보인다.
- **원칙과 부딪친다**: TG2 의 뜻은 「확신 없으면 남겨 넓게」(SPEC §3-1 · _RESUME 「원칙: 빠지는 정보가 있으면 안 된다」 · r3 A-5 「불확실 · 두 범위면 둘 다 읽음」)인데, 여기서는 남긴 조각이 AND 필터가 되어 폭을 줄였다. 덮인 조각(`covered_by` ≠ null)인 「볼」 은 이미 CON-012 이름 안에 든 말이라 필터로 다시 걸 근거도 없다.
- **고칠 방향**(일반 규칙 · 하나 고름):
  (a) **필터는 더하기만** — 부위를 건 조회를 낼 때 부위 없는 조회도 늘 함께 낸다(폭 = 합집합 · 부위 표지는 `site_match` 로 이미 행마다 붙는다). 가장 단순하고 원칙(폭 줄임 0)에 바로 맞는다. 다만 「이마 주름」(F1) 같이 부위가 진짜 좁힘인 질문에서도 행이 는다 — 깊이 · LLM 칸 규칙으로 다룰 몫.
  (b) **필터로 쓸 입구를 가린다** — `site`(및 사건 · 조건) 입구가 `uncertain_kept` 이거나 `covered_by` 가 같은 질문의 다른 대상 이름이면 필터로 걸지 않고 자기 범위 입구로만 읽는다(부위 시작 조회). TG2 의 「넘김 쪽」 뜻을 지키면서 F1 의 좁힘은 그대로 둔다.
  권고 = **(b) + 판정 기록**: 필터를 건/안 건 까닭을 `front.targets[]` 에 한 칸으로 남김. 어느 쪽이든 SPEC §3-1 BR1 · TG6 에 한 줄 필요(「부위 · 사건 필터는 확정 대상 입구만」 또는 「필터 조회 + 필터 없는 조회」) — 코디 결정.
- 같은 꼴이 사건 · 조건 필터에도 있다(`calls.py:154` `adverse_code` · contraindication `condition_code`) — 규칙을 정할 때 셋 함께.

## 5. 원칙 · 안전 · 기록

| 볼 것 | 결과 |
|---|---|
| 행 안 뺌 | 통과 — verified 행마다 줄 하나 · K1 `lines_ok` · 묶음은 같은 값만 머리로(`material.py:183-209`). 새 코드에 행을 거르는 곳 0(`narrow_by_entry` 는 **키 명세**의 종류만 좁힘 · B 걷기 무관) |
| LLM 에는 필요한 칸만 | 통과 — 새 표지는 사람 말(`site_match` 두 말 · `layer_via` 이름 · `inherited_fill` True). 코드(`inherited_from` · `csi_ids` · via 코드)는 `verified_lines` 에만. K4 `leak` 4 항목 실물 3 run 모두 false |
| 빠짐없이 | **W-2**(필터가 폭을 줄임) · W-1(셈) 외 새 위반 0 |
| 안전 강제 첨부 0 | 통과 — 이번 판 `kinds.py` · 기본 묶음 손대지 않음. `gate_forced` 는 G7 명시 대상 깊이(`depth.py:96`) · G1 은 **읽은 폭 안의** 금기 행만 확인(`gate.py:69-71`) — 조회를 더하지 않음 |
| **W-3** `ledger_check` 가 runs 에 없다 | SPEC-002 372 행 「`ledger_check[]` 는 그대로 기록된다」 · WORK-008 §4 완료 조건 1 · §8 F2 기대 「`LCK-010` 이 trace 에」. 모의 시험은 메모리의 `reads_lc`(`test_holes.py:59`)만 본다 — 남는 trace(`breadth[]` = `ReadAll.summary()` `hub_rest.py:86-89`)에 `ledger_check` 칸이 없어 F2 · F1 · F3 runs 줄 어디에도 0. (가) 판정 · HG1 의 근거를 runs 만으로 되짚을 수 없다. 고칠 방향: `summary()` 에 `ledger_check`(코드 · lck_ids · on) 를 더하거나 B trace `end_check` 에 합 `lc` 를 남김 |

## 6. 시험 · 커밋 후보

- `uv run ruff check .` → All checks passed! · `uv run pytest -q` → **181 passed, 1 skipped**(7.08s · 보고서 수와 같음).
- 커밋 후보 102 파일(`git ls-files -o -m --exclude-standard`) grep:
  - 홈 경로(`/Users/` · `/home/`) **0**
  - 키 꼴(`sk-…` · `Bearer …` · `api_key|token|secret = "…"`) **0**
  - 코드 꼴(`[A-Z]{2,4}-숫자`)은 문서 이름(SPEC- · WORK-)과 시험의 가짜 코드(9xxxx · LCK-900 · CSI-9001 · ZZ…)뿐 · 실제 시술 · 고민 이름(필러 · 보톡스 · 주름 · 볼 등) 0. `.env` · `data/` · `runs/` 는 gitignore(`!!`)

## 7. 지적 표

| # | 파일:줄 | 심각도 | 근거 | 고칠 방향 |
|---|---|---|---|---|
| W-1 | `walk/required.py:81-101` · `walk/front.py:66-68` · `evalset/answer_key.py:184-195` | WARN | 필터로 쓴 사건 입구(ADV-051)가 required 미충족 → B 「후보 소진」(F3) · 키는 그 줄을 건너뜀 → B ≠ 키(N-2 · WORK §4 완료 5) | §4 W-1 — 필터 칸 코드도 대상 매칭에 · 키와 같은 매칭 함수 |
| W-2 | `walk/calls.py:175-180`(· `:97-101` · `:154`) | WARN | `uncertain_kept` · 덮인 조각인 부위가 AND 필터로 고민 조회를 좁힘(F2 — 기대 65 후보 대신 2) · 원칙 「폭 줄임 0」 · TG2 넘김 쪽 · A-5 「불확실하면 둘 다」 | §4 W-2 (b) 권고 · SPEC BR1 · TG6 한 줄(코디 결정) |
| W-3 | `clients/hub_rest.py:86-89` · `columns/col_b.py`(trace) | WARN | SPEC-002 372 행 · WORK-008 §4 완료 1 · §8 F2 — `ledger_check` 가 남는 trace 에 없음 | `breadth[]` 줄 또는 `end_check` 에 `ledger_check` |
| W-4 | `walk/verified.py:152-161` | WARN(낮음) | 같은 gid 가 두 조회에서 오면 첫 조회의 표지만 남는다 — 자기 행 조회(예: 윗고민 CON-008 을 직접 물음 · 자손 펼침의 조상 고민)가 먼저 읽히면 같은 행의 `inherited_from` 표지가 안 붙고 `inherited_fill` 을 K4 가 요구하지도 않는다(조용히 빠짐 · 읽은 차례에 따라 다름). F2 실물은 차례가 맞아 안 났다 | 겹칠 때 `inherited_from` · `site_match` 표지를 합치거나(행 하나 · 표지는 조회별) K4 가 `required.inherited_via` 대상의 행을 기준으로 보게 |
| N-1 | `_v052b/answer-key/*.json` | NOTE | (나) 키의 `script_sha256` 이 지금 `answer_key.py` 와 다르다(내용 같음 — 재현 diff 는 그 줄뿐). (나) 뒤에 WP-1 `kinds_met` 이 바뀐 흔적 | 보고에 「(나) 는 WP-1 코드 앞 스크립트 · 지금 스크립트로도 내용 같음」 한 줄 |
| N-2 | SPEC-002 §5 598 행 ↔ 372 행 | NOTE(되적기) | §3 — 「상위 행 뺌」 에 「단 머리 `inherited_from` 응답의 행(HG1)은 셈」 예외 | SPEC 0.6 되적기 한 줄(보고서 미결 6) |
| N-3 | `walk/material.py:28-31` | NOTE | `inherited_kinds` 가 질문 전체의 종류 집합 — 대상별이 아니다. 두 고민이 같은 종류를 하나는 self · 하나는 inherited 로 채울 때도 표지는 행의 `inherited_from` 으로 갈려 지금은 맞다(F2 실물: 7 행만 표지) | 그대로 · 대상이 셋 이상인 시험 하나 권함 |
| N-4 | `answer_key.py:241-262` | NOTE | Q10 키 「근거 충족」 은 `by = set`(csv 「원장 확인」 이 `STATUS_MAP` 밖). (가) 가 안 나는 것은 코드로 서지만, 기대 상태는 세트 값이 정한다 | 사용자 key-table 확인 때 「Q10 = 세트 값」 이 보이는지만 |
| N-5 | 보고서 WP-6 F1 | NOTE | WORK 기대 「재료 73 행 · 묶음 16」 ↔ 실물 verified 98 행 · 시술 6 — 차이 설명 없음(기대 수는 허브 셈 · 실물은 Jev 대상 · 종류 판단을 거침) | F1 의 대상 · 종류 · 조회를 기대 셈과 나란히 한 줄 |
| N-6 | `pick-holes.json` · SPEC §9-3d | NOTE | HG1 13 전부 한 단 → H02((ii) 두 단) 후보 0 · SPEC 「9 + 4」 와 다름(보고서 미결 2) | SPEC 셈 근거 다시 보기 — 코디 |
| N-7 | WORK-008 §8 마감 | NOTE | 18221 화면 F2 확인(정확도 탭 · 옛 줄 다시 보기) 안 함 — `test_web` 통과로 대신(보고에 밝힘) | 코디 바꿔 끼우기 때 18220 에서 한 번 |
| N-8 | 키 Q12 (나) +4 | NOTE | `g_adverse_detail` GAX 4 행(M2 → 제품 → 하위 제품 · depth 2)이 옛 키 전용 하위 시술 셋으로는 못 닿던 길 — KF2 대로 손으로 안 맞추고 보고한 것 맞음. 허브 쪽이 맞다는 판단은 코디 | 사용자 key-table 확인 때 Q12 행 수 바뀜 함께 |

## 8. 사용자 e2e 에서 만날 자리

1. 「볼 주름」 류(부위 글자가 든 고민 이름) 질문은 B 가 좁게 읽고도 「근거 충족」 으로 끝난다(W-2) — 답이 짧으면 그 까닭이다.
2. 「필러 혈관 폐색」 류(계열 + 사건) 질문은 B 가 「후보 소진」 으로 끝난다(W-1) — 행은 다 읽었고 답 재료도 있다.
3. runs · 화면 trace 에서 원장 확인(LCK) 항목을 찾을 수 없다(W-3).
4. 공통 답 지시가 0.5.1 runs 와 다르다(O-29 ④) — 앞 판 run 과 답 길이 · 시간을 견줄 때 주의.
