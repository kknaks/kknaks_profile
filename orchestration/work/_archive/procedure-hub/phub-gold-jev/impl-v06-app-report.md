# 앱 0.6 구현 보고 — WORK-009(SPEC-002 0.6.0)

- 워커: app · 워크트리 `APP-WT`(`~/orca/workspaces/clinic_chat/phub-gold-jev` — 0.5.2 + 수정 1 미커밋 위에 이어서) · 커밋 · push 없음
- 정본: `_RESUME.md` §2 맨 위 세 행(W-1 ~ W-7 · B-1 ~ B-3 · U-5 ~ U-9) · `review-work-v06.md`
- 이 보고에는 세트 id · run id · 셈 · 파일:줄만 적었다(질문 문장 · 답 · 이름 없음).

## 0. 요약

| 항목 | 결과 |
|---|---|
| WP | WP-0 ~ WP-9 전부(37 batch E11 은 코디 몫 — 명령은 WORK §12 그대로) |
| 검증 | `ruff check .` 통과 · `pytest -q` **213 passed · 1 skipped**(기준선 190 · 1 → 새 시험 23 · 고친 시험 4) · `loader --validate` 85 줄 · draft 48 · 오류 0 · `batch --check` 전부 됨(답 키 37 · confirmed **0** — B-2 대로 코디가 잇는다) |
| 답 키 (나) | BR5 넣기 전 **37 / 37 같음**(행 집합 + `codes` · `unnamed_codes` · `side_codes` · `kinds_met` · 기대 종료(+`_by`) · `sample_check`) · 명세 `calls_sha256` 37 같음 · 갈래 합 **입구 41 · 값 706 · 층 173**(§9 의 수와 같다) |
| 답 키 (다) | **Q12 · Q13 · Q14 만 다름** — `g_adverse` 23 · 20 · 8 그대로 · `g_adverse_detail` 464→**34** · 330→**9** · 90→**36** · `only_now` 0 · 기대 종료 · `kinds_met` · 표본 그대로 · 나머지 34 같음 |
| 동결 | WP-8 뒤 `evalset/answer_key.py` · `walk/calls.py` · `walk/keycodes.py` **바뀌지 않음**(sha256 아래 §3) |
| 실물(18221 · effort low · B · C 동시 · 1 회씩) | 대표 6 + 곁 1 다 돌림 · 18221 내림 · 18105 · 18220 · 18106 안 건드림 |

## 1. WP 별

### WP-0 — 허브 입력 셋(18105 · 읽기만)

| # | 확인 | 결과 |
|---|---|---|
| H1 | `scope(node)` 의 `holders[]` 에 `role` · `holder_table` · `holder_code` · 자손 전부 | **됨** — 제품 노드 = 자기 1 · 물려받음 2 / 계열 노드 = 자기 1 · 하위 시술 3 · 하위 제품 32 · 하위 케이스 15(손자까지) |
| H2 | `adverse` + `filters.adverse_code` 행에 `silver_table` · `silver_id` · `adverse_detail` 이 `filters.adverse_risk_id` 를 받나 · 같은 칸 두 번 | **됨** — 행 전부 두 칸 있음(`adverse_risk`) · 받음 · 두 번 = **422 invalid_argument** · id 마다 조회 수 Q12 **23** · Q13 **20** · Q14 **4**(id 4 · 행 8) · id 마다 상세 합 34 · 9 · 36(필터 없음 464 · 330 · 90) |
| H3 | `resolve` 목록 꼴 줄의 `norm` | **됨**(목록 543 줄 전부) |

### WP-1 — KD9 · KD10 · KD11(U-5 = (a))

- `config.py` `jev_kind_read_at`(기본 0.5 · env `JEV_KIND_READ_AT` · `walk_settings()` · trace `front.thresholds.kind_read`) · `.env.example` 한 줄.
- `walk/front.py` `_decide_kinds` — 차례 **KD5 → KD10 → KD9 → KD6 → RG1 · KD3(+KD11)**. KD5 를 KD9 · KD10 앞에 둬 입구가 이름 댄 종류가 `entry`(required)로 남게 했다. KD11 은 KD6 가지(`kinds_by` = `default`)에서는 돌지 않는다. `READ_BY` 에 `kd9` · `kd10` · `REQUIRED_BY` 그대로. KD11 로 남긴 종류는 `offered[].by` = `kd11` · `front.kinds[].decision` = `offered`.
- 시험: T26 · T27(+ 설정 0.6 경계 이동) — `tests/test_walk_front.py`. 기존 시험 넷을 0.6 규칙에 맞게 고침: `test_walk_core.py::test_ok_procedure_reads_only_read_kinds_no_depth`(개요 yes → 원리 yes 로 · KD9 가 돌면 「읽기로 한 것만」 의 뜻이 바뀌어서) · `test_walk_front.py::test_kinds_yes_between_no` · `::test_w1_no_applicable_kind_falls_back_to_kd6_defaults`(사이 값 0.5 → 0.45 — KD10 문턱 아래) · `test_walk_entry.py::test_attr_entry_plus_offer_keeps_attr_start_and_key_same_calls`(KD11 로 기본 묶음 개요 · 어디에 쓰나가 `offered`).

### WP-2 — 무리 · 짝 조회(PR1 ~ PR5 · BR7 · W-4 · B-3)

- 새 `walk/groups.py` — `scope_links`(대상마다 `scope` 한 번 · 장부 `calls_done` 에 안 넣고 `visited` 꼴 줄 `purpose` = `group` 만 돌려줌 — 검수 W-4) · `group_targets`(PR1 (i) 같은 `span` · `start` / (ii) holder 가 `물려받음` · `하위 *` → 합집합) · `yes_group`(N-3 — yes 아닌 무리가 아닌 것).
- `walk/calls.py` — `Entry.start` · `Entry.norm` · `_pairs(targets, groups)`: 무리 하나 → 대상마다 한 끝 / 둘 이상 → 다른 무리끼리 두 끝 / yes 아닌 무리가 끼면 두 끝(표지) + yes 무리 한 끝(`widened` = `w4`) / yes 무리 0 → 무리마다 한 끝(`b3` — **B-3 코디 결정대로**). `plan_calls(…, groups=)` — 안 주면 (i) 만.
- B: `front` 가 대상 둘 이상일 때만 무리 판정(`front.groups` · `front.links` · trace `front.groups[]{members, by}`) → `col_b` 가 `plan_calls(…, groups)` · 판정용 조회도 같은 무리. 키: `key_calls.entry_groups` → `spec_calls(…, groups)`(무리 판정 `scope` 는 명세 `calls[]` 밖).
- PR5: `required.call_side` 는 이미 한 끝 조회 행을 그 대상 것으로 센다 — 고치지 않음(T29 로 확인).
- 시험 `tests/test_v06_groups.py`: T28 (a) ~ (e) · N-1(두 끝 일부만) · T29 · **검수 W-4(무리 판정 scope 가 `lineup` 읽기를 가리지 않음)** · 키 명세가 같은 무리 함수. 모의 허브에 기본 `scope` 길(`{"holders": []}`)을 더함(`tests/fake_hub.py` — 길을 안 준 옛 시험).

### WP-3 — BR6(U-9) · BR5(U-8 · B-1 (a))

- BR6: `filter_entries` 의 둘째 값 = `uncertain_kept` **또는 `named`**(`WEAK_BY`). 거른 조회에 `meta.mark` = `narrowed`(안 거른 조회를 함께 낼 때만) → `verified` 표지 합침. yes 떨어진 입구 = 거른 조회만 · 덮인 조각 그대로.
- BR5: 사건 필터 조회가 있으면 필터 없는 `adverse_detail` 을 내지 않음(BR6 의 안 거른 조회가 함께면 그 쪽은 전부) · `followup_calls` 에 가지 — 응답 `silver_table` = `adverse_risk` 의 서로 다른 `silver_id` 오름차순마다 `adverse_detail` + `filters.adverse_risk_id`(같은 `node` · `roles` · 부위 필터 · `meta.followup` · `from_risk`). B 와 키가 같은 `followup_calls` · 판정용은 `follow=False` 그대로 · B-11(깊이 상세) 그대로.
- 시험 `tests/test_v06_filters.py`: T30 · T34(**B 가 읽은 조회 집합 = 키 `read_rows` 가 읽은 조회 집합** · 허브에 간 상세 필터 순서까지 같음). `test_covered.py` · `test_holes.py` · `test_answer_key.py` 그대로 통과.

### WP-4 — EN1 · VP1 ~ VP3(U-7 = (a))

- EN1: `front` 가 상품 이름 구마다 `facets offer` + `offer_name_contains` 를 `limit 1` 로 한 번 물어 **맞았을 때만**(B-8) 그 구의 글자 범위(`entry.offer_name_spans`) 안에 든 후보 가운데 yes 아닌 것을 `dropped`(`covered_by` = 구 · `by` = `offer_name`). 읽은 뒤 `col_b.offer_picks` 가 맞은 상품을 `entry.picked[]{id: offer:<id>, by: offer_name}` 로.
- VP: 새 `walk/value_pick.py` · `prompts/jev/value.md`(`JEV_FILES` 에 더함 — 프롬프트 해시가 바뀜 · 「미확정」 그대로). 도는 조건 = required(`by` yes · top) 값 종류 × 그 값 표 입구 없음 × 대상 있음. 후보 = 읽은 행의 값 코드(`keycodes.VALUE_KIND`) · Noul `value_{i}` 32 묶음. yes → `picked[].by` = `value_pick` · 행 표지 「질문이 가리킨 값」. VP3 = yes 값의 `g_entry.norm` 이 거르개 입구(부위 · 사건 · 조건)의 `norm` 을 품으면 그 거르개를 걷은 `plan_calls` 로 다시 읽음.
- **W-7(B-4 대로)**: VP 가 `adverse` 에 돌면 계획의 `adverse_detail` 을 VP 뒤로 미룸 → yes 사건이 있으면 그 사건 행의 위험 id 로(`adverse_detail_by_risk`) · 못 내면 미룬 조회 전부. 걷힌 거르개로 건 미룬 상세는 버리고 걷은 꼴로. 「걸기 전」 수 = `coverage`(adverse) 셈 → trace `entry.value_pick.br5{risk_ids, calls, before_rows_coverage_adverse, after_detail_rows}`.
- 시험 `tests/test_v06_material.py`: T31(맞은 상품 · 덮인 조각 dropped · yes 는 대상 · 0 행이면 덮지 않음) · T32(요청 · 표지 · 거르개 걷힘 · 다시 읽힘 · 위험 id 로만 / yes 없으면 전부 / 값 입구 있으면 요청 0 / required 아니면 요청 0).

### WP-5 — 이름 목록 · P9 / P11 · answer_check · SD1 · 표지

- `walk/material.py` `roster` — verified 행의 키 코드(`keycodes.key_codes` — 답 키 · D3 와 같은 함수) · 갈래(`keycodes.classify` — 그 행을 낸 조회의 쪽) · 이름(키 코드 칸의 이름 칸) → 기록 `{entry, value, layer: [{code, name}]}`. `roster_text` = LLM 꼴 `{"value": {입구 표: [이름…]}, "layer": {…}}`(이름뿐 · 이름 하나는 한 번 · 값 쪽 먼저 · verified 순서). `col_b.prompt_pages` 가 **첫 쪽 머리에 전부**(`## 이름 목록`) · 쪽 크기 셈 overhead 에 목록 길이 넣음.
- `answer_check` — 단계 ⑤ 뒤 이름 글자 대조(공백 · 대소문자 무시 · 재료의 이름 목록 자신으로 — 채점 env 없음) → `{roster{entry, value, layer}, said{value, layer}, missing{value[], layer[]}, missing_codes{…}}` · gate 아님(답 · 종료 상태 그대로 · 보충 호출 없음 — U-6).
- SD1 `col_b.same_day_marks` — `same_day` 를 읽고 대상 둘 이상일 때, `package_kind` = 같은 날 조합 패키지의 항목이 두 대상(자신 또는 `front.links` 의 윗층 · 하위) 모두에 닿으면 그 항목 행에 「같은 날 근거(패키지)」 · 항목이 윗층 · 하위면 `same_day_layer`[{of: 대상 이름, layer: scope role}]. `same_day_blank` 그대로.
- 표지 셋(`MARK_KO` — SPEC O-32 ④ 의 말 그대로) → `llm_marks` · **K4 가 붙었나 봄**(`gate.py`) · 기록 `verified_lines[].marks06`(실물 셈용 — 되적기 후보 R-6).
- 시험: T24 · T25(값만 빠진 꼴 / 층만 빠진 꼴 · gate 아님 — 모의 CLI) · T33.

### WP-6 — 키 · 채점(DU1 · DU2 · T35)

- 새 `walk/keycodes.py` — `KEY_CODE` · `_codes` · `key_codes` · `key_names` · `value_side` · `classify` · `by_class` · `VALUE_KIND`. `answer_key.py` · `quality/gold_codes.py` 가 여기서 import.
- 키 `codes_by_class{entry, value, layer}`(`answer_key.key_classes` — 입구 = 세트 기대 대상(`upper_of` · `lower_of` 키 전용 대상 뺌) · 쪽 = 그 행을 낸 조회의 시작 입구 · 입구 > 값 > 층). `codes[]` · `unnamed_codes[]` · `side_codes[]` 그대로.
- D3(`quality/checks.py`): 갈래가 있는 키면 주 지표 = 값 코드 · `layer_missing` · `layer_codes` 따로 · 값 코드 0 → `na` = 해당 없음 · 고민 꼴 케이스 빼기 그대로 · 옛 키는 지금 식.
- 대조 「같음」(**검수 W-3 · 코디 W-3**): `diff_keys` 의 `same` = 행 집합 + `SAME_FIELDS`(`codes` · `unnamed_codes` · `side_codes` · `kinds_met` · `expected_end_state` · `_by` · `sample_check`) · `differs[]` · 명세 `calls_same`(`calls_sha256`) · 갈래 수. `--no-br5` 인자는 만들지 않았다(W-3 ③ — WP-3 앞에 한 번 뽑아 (나)).
- 시험 `tests/test_v06_keyclass.py`: 갈래 · 우선 · T35(세 열 같은 분모 · 해당 없음 · 옛 키) · 대조 「같음」.

### WP-7 — 기록 · 보고서 · 되적기 확인

- trace 새 칸: `front.groups[]` · `front.kinds[].by`(`kd9` · `kd10`) · `front.offered[].by` = `kd11` · `front.thresholds.kind_read` · `entry.picked[].by`(`offer_name` · `value_pick`) · `entry.value_pick{…}` · `answer_check` · `breadth[]` 의 `mark` · `widened` · `from_risk` · `value_pick` · `visited[]` 의 `purpose` = `group` · `verified_lines[].marks06`.
- 보고서(`report.py`): 열 표에 「① D3 값 빠짐 합 / 값 코드 합(0.6 주 지표)」 · 「① D3 해당 없음 문항」 · 열 표 밑 「층 빠짐(따로)」 한 줄 · 「B 전용」 에 0.6 줄 10(기대 종류 `by` 별 · W-3 기대 밖 kd9 · kd10 · KD11 · W-2 BR6 · W-4 / B-3 · 무리 · 값 고르기(N-2) · 답 확인 값 / 층 · EN1).
- 옛 줄: 0.5.2 batch `20261117-115258-v052-37-a7df` 를 **scratch 로** 렌더(기존 `runs/reports/…md` 는 덮지 않음) — 죽지 않고 0.6 줄 = 「—」 · D3 새 줄 = 해당 없음. 합성 trace 로 0.6 줄이 채워지는 시험 1.
- 되적기 확인(§16 「이미 있음」 — 전부 있음 · 전부 시험 있음): 덮인 조각 `walk/front.py:307` · `walk/calls.py:111-136` · `tests/test_covered.py` / v052 W-1 `walk/required.py:81-99` / W-2 `walk/calls.py:125-136`(WP-3 이 `named` 로 넓힘 · T30) / W-3 `clients/hub_rest.py:90` → `walk/breadth.py:44-50`(`tests/test_covered.py:125`) / W-4 `walk/verified.py:202-` / `counted_rows` `walk/end_state.py:33-37`(`tests/test_holes.py:97`) / `expected_kinds_by_entry` `evalset/loader.py:25` · `:32-` / `HOLE_EXPECT` `evalset/pick.py:147` = 한 단 9 · 두 단 4(SPEC 글과 같음).
- README 「실행 안내」: 답 키 대조 명령 한 줄 · `JEV_KIND_READ_AT` 한 줄.

### WP-8 — 답 키(자세한 수 §2)

(가) `data/eval-set/_v06a/`(calls · answer-key · key-summary · key-table · set.jsonl — 1.5 MB) → (나) WP-2 · WP-6 뒤 · BR5 앞: `key_calls --from-gold-build` → `answer_key --all` → `--diff _v06a --diff-out key-diff-v06-pre-br5.md` → (다) WP-3 뒤: 같은 셋 → `--diff-out key-diff-v06.md` → `key_table --prev _v06a`. `_v06b` 는 만들지 않음. `--confirm` 안 함.

### WP-9 — 실물(§4) · 마감

`batch --check` 전부 됨(답 키 confirmed 0) · `loader --validate` 오류 0 · 커밋 후보 grep §6.

## 2. 답 키 대조

| 걸음 | 같음 | 다름 | 명세 같음 | 갈래 합(입구 · 값 · 층) | gold / aux hash |
|---|---|---|---|---|---|
| (나) BR5 앞 | **37** | 0 | 37 | 41 · 706 · 173 | 앞 = 뒤 |
| (다) 최종 | **34** | Q12 · Q13 · Q14 | 34 | 41 · 706 · **141** | 앞 = 뒤 |

(나) 의 `pair` 15 문항(한 끝 7 · 두 끝 8) 명세가 앞 판과 바이트까지 같다 — SPEC 이 안 본 아홉 포함. (다) 의 「같음」 34 = 행 집합 + `SAME_FIELDS` 전부 같은 문항(코디가 `--confirm` 으로 이을 목록): **Q01 ~ Q11 · Q15 ~ Q37**.

| 문항 | 행 | `g_adverse` | `g_adverse_detail` | `codes` | `unnamed` | 갈래(입구 · 값 · 층) | 명세 조회 | 다른 칸 | 기대 종료 | `kinds_met` | 표본 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Q12 | 487 → 57 | 23 → 23 | 464 → **34** | 43 → 22 | 5 → 1 | 2 · 0 · 20 | 2 → 24 | codes · unnamed | 원천 미확정 (다) → 같음 | 같음(self · self) | 4/4 → 4/4 |
| Q13 | 350 → 29 | 20 → 20 | 330 → **9** | 30 → 19 | 10 → 2 | 2 · 0 · 17 | 2 → 21 | codes · unnamed | 근거 충족(status) → 같음 | 같음 | 5/5 → 5/5 |
| Q14 | 98 → 44 | 8 → 8 | 90 → **36** | 4 → 4 | 0 → 0 | 2 · 0 · 2 | 2 → 5 | (행 집합만) | 근거 충족 → 같음 | 같음 | 6/6 → 6/6 |

- `only_now` 0(준 것뿐) · `key-table.md` 「바뀜」 칸은 Q12 · Q13 · Q14 셋만.
- SPEC §3-7-5 의 「층 대상 47 → 22 · 39 → 20 · 3 → 3」 과 이 키의 층 코드 수(41 → 20 · 28 → 17 · 2 → 2 — `codes` 기준 · 입구 뺌)는 셈 단위가 다르다(SPEC 은 unnamed 포함 어림으로 보임) — 줄어드는 방향은 같다.
- `key-summary.md` 걸린 꼴이 30 → 31: Q13 에 「0.4.1 키보다 줄어듦(213 → 29)」 이 새로 걸림 · Q12 · Q14 는 같은 표지의 수만 바뀜(BR5 로 준 몫 — 기대한 것).
- 갈래 층 173 → 141 = Q12 · Q13 의 층 코드가 준 몫(41 → 20 · 28 → 17).

## 3. 동결(W-6)

WP-8 (다) 뒤 sha256 — 마감 때 다시 대조해 **같음**:

```
55ed3dbf471d53766a8a2aaf3a56bf9670686982fa1b8fa2d7988d03e2550d2f  clinic_chat/evalset/answer_key.py   (= 키의 script_sha256)
c7b6bdba519a7f7cce37c3b23c7d68bc75c542e49cbd2fa1b9038e2e0c18a2aa  clinic_chat/walk/calls.py
c47d9d93f525e1c7e0bacdd22f0c5b9a70f8ae7e90ec40d9f9e2037889c00ff0  clinic_chat/walk/keycodes.py
```

WP-4 · WP-5 가 쓰는 것(`NARROWED_MARK` · `adverse_detail_by_risk` · `risk_ids` · `VALUE_KIND` · `key_names` · `value_side`)은 (다) 전에 넣었다. 37 batch 앞 「한 번 더 뽑아 이어지는지」 는 코디 몫(W-6).

## 4. 실물 확인(E7 ~ E10 — 18221 속도 탭 API · effort low · B · C 동시 · 문항마다 1 회 · **trace 수만** — W-5 · D3 · D7 · ② 는 E11)

단건이라 편차가 크다. ms 는 화면 기준(누른 순간 → 첫 글자 · 열 동시)이라 0.5.2 batch(차례로)의 ms 와 직접 견줄 수 없다.

| # | 세트(새 run · 0.5.2 run) | 원인 · 시험 | 0.6 실물 | 0.5.2 batch(같은 문항) | 기대와 |
|---|---|---|---|---|---|
| R1 | Q10(`3a1d9df1d615` · `c885850807de`) | A1 · E7 | 재료 281 줄 · 이름 목록 값 97 코드(이름 73) · 층 0 · **`answer_check.missing.value` 26 이름**(said 47) · 층 0 · 입력 73.3 KB · 출력 3,378 토큰 · 첫 글자 B 12.4 s / C 19.7 s · 근거 충족 | 281 줄 · 71.7 KB · 출력 1,528 · D3 빠짐 20(값 · 층 갈래 전) | 출력이 2.2 배 — 목록을 더 댄다. 「빠짐 20 → 26」 은 **식이 다른 두 수**(D3 = 이름 → 코드 · gold `g_entry` 이름 전부 · `answer_check` = 재료 이름 글자 그대로 — 검수 N-2) · D3 는 E11 |
| R2 | Q03(`3e3d3d023497` · `23ac16a2faa9`) | A2 · E8 | 기대 종류 5 / 5 `read`(개요 yes · 원리 · 어디에 쓰나 kd10 · 효과 · 하위 목록 kd9) · 무리 1(대상 4 · span · scope) · 재료 **520 줄** · 129.2 KB · 이름 목록 값 72 · 층 41 | 기대 종류 1 / 5 · 45 줄 · 29.3 KB | 기대대로(전부 read). **단 B 답이 「두 시술 비교는 다루지 않는다」 로 맺어 이름 0 개(said 0)** — 답 프롬프트 P5 · G11(근거 없는 비교) 쪽 행동 · 재료와 무관 · 1 회 단건(§5 주의 1) |
| R3 | Q18(`16dc8c9e1318` · `98b3cf499fee`) | A2(KD10) + BR6 · E8 · E9 | `combo` = `read`(kd10 · 0.52) · 한 글자 부위 `named` → 거른 조회 2(표지 · 0 행) + 안 거른 조회 2(125 · 29 행) · 재료 **156 줄**(0 아님) · 두 끝 1(2 행 · 무리 2 — 둘 다 혼자) · **근거 충족** · KD11 `offered` 2(개요 56 · 패키지 39 행) · VP(어디에 쓰나 — required · 고민 입구 없음) 후보 62 · 요청 2 · yes 0 | combo `offered` · 0 줄 · 원천 미확정 (가) | 기대대로. VP 가 이 꼴에서도 돌아 Jev 요청 +2(R-3) |
| R4 | Q37(`2480a474e2d3` · `819c5ea4d7a2`) | A3 · E9 | 무리 **1**(대상 4 · span · scope) · 두 끝 **0** · 한 끝 4(30 · 33 · 31 · 33 행) · required 4 전부 충족(self 2 · inherited 2) · **근거 충족** · 재료 33 줄 | 두 끝 6 전부 0 · required 미충족 4 · 후보 소진 | 기대대로 |
| R5 | Q13(`1305fe9fa602` · `6a08a296c168`) | A4 · VP · BR5 · E10 | 대상 4(조각 하나의 셋 = 무리 1 + 부위 yes) · VP 후보 1 · 요청 1 · **yes = 기대 사건 입구**(기대 입구 2 / 2) · 부위 거르개 걷힘 1 → 안 거른 `adverse` 3 다시 읽음(299 · 105 · 299) · 미룬 상세 3 → 위험 id 20 × 대상 3 = **상세 조회 60 · 25 행**(coverage adverse 셈 703) · 재료 **308 줄** · 허브 호출 96 · 근거 충족 | 사건 입구 놓침 · `adverse` 1 행 · 상세 0 · 재료 1 줄 | 기대대로 선다. 상세 조회 60 번(대상 셋 × id 20 · 대부분 0 행)은 B-1 (a) 의 값 — E11 에서 시간 볼 것(R-1) |
| R6 | Q33(`1a75bea121c7` · `ac4b37df75de`) | A4 · EN1 · W-3 · E10 | `picked` 에 `offer_name` 1(**기대 입구 1 / 1**) · 상품 이름 구 안의 조각 1 `dropped`(`by` offer_name) · 계열 대상은 yes(0.85)라 그대로 · 개요 `read` 는 **kd10**(0.6 대 — 1위가 상품이라 KD9 안 돎) → profile 48 행 · 상품 13 + 1 · 재료 **52 줄** · 32.9 KB | 입구 놓침 1 · 52 줄 · 32.3 KB | 입구 일치는 섰다. W-3 어림(KD9 로 약 480 행)은 이 run 에서 **일어나지 않음**(KD9 대신 KD10 으로 개요만 · +48 행 = 0.5.2 와 같은 재료) |
| 곁 1 | Q21(`58a6d940ece7` · `bd2e0ce1b774`) | SD1 · E10 | 무리 2(혼자 · 혼자) → 두 끝 1(13 행) · 패키지 행 3 가운데 「같은 날 근거(패키지)」 **2** · 층 표지 **1**(재료만 다시 걸은 확인 — LLM 없이 `col_b.walk` 1 회 · Jev 2 · 허브 5) · K4 통과 · 근거 충족 · 재료 16 줄 | 16 줄 · 표지 없음 | 표지가 붙는다. 답이 그것을 근거로 말했나는 ② — E11 |

## 5. 주의 · 보고(고치지 않음)

1. **R2 의 B 답(비교 거절)** — 재료는 기대 5 종류 520 줄인데 답이 「비교는 다루지 않는다」 로 맺었다(P5 · 공통 5 번 · G11). 0.5.2 batch 에서는 같은 문항을 답했다. 1 회라 우연일 수 있다 — E11 의 ② · `answer_check` 로 보고, 반복되면 프롬프트 확인(C-1) 때 「차이 질문 = 두 대상 각각을 빠짐없이 + 견주지 않음」 꼴을 사용자에게 물을 자리다(이 판에서 문구를 고치지 않았다).
2. **EN1 뒤 종류 · 범위를 다시 세지 않는다** — 상품 이름 구가 덮어 뺀 조각의 표로 끌린 범위 · 기본 묶음은 그대로 남는다(`required` 셈 대상에서는 빠짐). R6 에서는 차이 없음. 다시 세야 하면 `_decide_kinds` 를 한 번 더 부르면 된다(되적기 R-5).
3. **EN1 확인 조회 1 회** — 맞았는지 보려고 `front` 가 `offer_name_contains` 를 `limit 1` 로 한 번 더 부른다(② 에서 같은 조회를 다시 읽음 · 허브 호출 +1).
4. **VP 가 `indication` 에도 돈다**(R3) — SPEC VP1 글자 그대로(required 값 종류 · 값 입구 없음). 어디에 쓰나를 1위로 물은 시술 질문마다 후보가 수십(R3 62)이라 Jev 요청 +1 ~ 2. 오발은 R3 에서 0(yes 0).
5. **BR5 상세 조회 수** — R5 60 번 · Q12 꼴(대상 하나 · id 23) 23 번. 대상이 한 무리여도 대상마다 따로 부른다(무리 판정은 짝 조회에만 쓰는 규칙이라).
6. **`answer_check` ≠ D3** — 재료 이름 글자 그대로 대조(D3 는 gold 이름의 다른 꼴까지) — 같은 답에서 `answer_check` 가 더 엄격하다(검수 N-2).
7. N-2 지표의 「걸기 전」 = `coverage`(adverse) 셈 = **`g_adverse` 행 수**(상세 행이 아님 — coverage 에 상세 종류가 없다). 보고서 「줄어든 행」 은 단위가 다른 두 수의 차다(코디 W-7 대로 · 되적기 R-7).
8. 무리 판정 `scope` 는 대상 둘 이상인 모든 문항에서 돈다(짝 종류가 없어도 — SD1 층 판정 재료와 `front.groups` 기록 때문). R2 · R5 에서 +4 · +3 호출.

## 6. 커밋될 것 / gitignore

- 바뀐 · 새 파일(커밋 후보 — 코디 몫): `.env.example` · `README.md` · `clinic_chat/config.py` · `clinic_chat/walk/{front,calls,entry,breadth,verified,material,gate}.py` · **새** `clinic_chat/walk/{groups,keycodes,value_pick}.py` · `clinic_chat/columns/col_b.py` · `clinic_chat/evalset/{answer_key,key_calls}.py` · `clinic_chat/quality/{checks,gold_codes}.py` · `clinic_chat/report.py` · `clinic_chat/prompts.py` · `prompts/common.md` · `prompts/col_b.md` · **새** `prompts/jev/value.md` · `tests/fake_hub.py` · `tests/{test_walk_core,test_walk_front,test_walk_entry}.py` · **새** `tests/test_v06_{groups,filters,keyclass,material}.py`(레포 자체가 아직 미커밋 — `git status` 는 `clinic_chat/` · `prompts/` · `tests/` 를 통째 `??` 로 보인다).
- gitignore 에 새로 생긴 것: `data/eval-set/_v06a/` · `data/eval-set/key-diff-v06-pre-br5.{md,json}` · `data/eval-set/key-diff-v06.{md,json}` · 다시 쓴 `data/eval-set/{calls,answer-key}/` · `key-summary.md` · `key-table.md` · `runs/runs.jsonl` 에 실물 7 줄. `_v06b` 없음. 옛 `_v0*` · 옛 runs 줄 · `runs/reports/` 안 건드림. 디스크 여유 17 GB(이 판에서 3 MB 안쪽 씀).
- 커밋 후보 grep(바뀐 · 새 111 파일): 실제 코드 꼴(시술 · 제품 · 고민 · 사건 · 케이스 · 부위 등 `XXX-숫자`) **0**(시험의 `ZZ…` · 옛 시험의 `CSI-9001` 가짜 뿐) · 실제 `gid`(9 로 시작 안 하는 것) **0** · LCK id **0** · 홈 경로 **0** · 키 꼴 **0** · 질문 문장 · 이름 0(시험 이름은 「가짜…」).

**바뀐 프롬프트 줄(C-1 — 사용자 확인 전 초안 그대로 · 「프롬프트 미확정」 표시 남음)**

- `prompts/common.md` 10 번: 「짧게 답한다 — 계열로 묶고 …」 → 「**모범 답 꼴을 따른다** — 계열로 묶고 · 시술 이름으로 말하고 · 원리는 한 줄 · 물은 것만 말하고 · 끝은 되묻기로 맺는다. …(뒤 그대로)」(P9)
- `prompts/common.md` 12 번(새): 「목록을 줄이지 않는다 — 받은 자료가 커도 물은 것에 해당하는 이름은 전부 말한다: 계열 · 갈래별로 묶어 이름만이라도 댄다. 「대표 몇 개 + 등」 으로 줄이지 않는다. 설명 · 수치는 물은 것에만 붙이고 나머지는 이름만 댄다.」(P11 — 세 열 공통 원칙만 · 검수 N-1)
- `prompts/col_b.md` 새 불릿 둘: ① 「이름 목록」 — `value` 이름은 **전부** 답에 · `layer` 는 층을 밝히는 재료(전부 댈 필요 없음) · 값은 자료 줄에서만 ② 0.6 표지 `narrowed` · `value_pick` · `same_day_package` · `same_day_layer` 읽는 법.
- `prompts/jev/value.md`(새 · 영어): VP1 「질문이 이 값을 말하나」.

## 7. 결정 반영 줄

| 결정 | 반영 |
|---|---|
| W-1(B-3 본문 · T28 (e)) | `calls._pairs` 의 `b3` 가지 · `test_t28_e_b3_no_yes_group_one_end_per_group` · 보고서 「W-4 · B-3」 줄이 둘을 갈라 셈 |
| W-2(표지는 두 끝 = 좁힌 쪽 · BR6 말 그대로) | 두 끝 조회 `meta.mark` = `narrowed` → 「그 부위(사건 · 조건)로 좁힌 것」(`calls.NARROWED_MARK`) · 새 말 없음 |
| W-3(`same` 칸 · 명세 해시 · (나) / (다)) | `answer_key.SAME_FIELDS` · `calls_same` · (나) = WP-3 앞 한 번 · (다) = 뒤 |
| W-4(무리 판정 scope 가 lineup 을 가리지 않음 + 시험) | `walk/groups.py`(장부 밖 · `visited` 만) · `test_w4_review_group_scope_does_not_hide_lineup` |
| W-5(실물은 trace 수만) | §4 — D3 · D7 · ② 는 E11 |
| W-6(동결 · 37 batch 앞 다시 뽑기) | §3 sha256 · 바뀜 없음 · 다시 뽑기는 코디 |
| W-7(B-4 대로 · 「걸기 전」 = coverage) | `value_pick.deferred` · `run` 의 BR5 가지 · T32 · trace `br5{before_rows_coverage_adverse, after_detail_rows}` |
| B-1 (a) id 마다 조회 | `calls.adverse_detail_by_risk` · H2 · R5 60 번 |
| B-2 34 잇기 = 코디 · 재확인 = Q12 · Q13 · Q14 | `--confirm` 안 함 · 「같음」 34 목록 §2 |
| B-3 yes 무리 0 → 무리마다 한 끝 | W-1 줄과 같음 |
| U-5 KD9 · KD10(0.5) · KD11 · 칸 그대로 | WP-1 · `llm_columns` 안 고침 |
| U-6 기록만 | `answer_check`(gate 아님 · 보충 없음) |
| U-7 VP | WP-4 |
| U-8 D3 갈래 + BR5 | WP-6 · WP-3 · (다) |
| U-9 BR6 = yes 아닌(named 포함) 떨어진 부위는 둘 다 · yes 는 거르개 그대로 | `calls.WEAK_BY` · T30 |
| 검수 W-1(P11 「전부」 = 값 쪽만 · answer_check 값 / 층) | 재료 `value` / `layer` 머리 갈림 · `col_b.md` 는 값 쪽만 「전부」 · `answer_check` 값 / 층 · T25 층 꼴 |
| 검수 W-4(두 끝 + yes 무리 한 끝 · T28) | T28 (d) |

## 8. 되적기 후보(SPEC · WORK 에 적을 것 — 코디)

| # | 무엇 | 자리 |
|---|---|---|
| R-1 | BR5 상세 조회는 대상마다 · id 마다(무리여도) — R5 60 번 | SPEC §3-7-5 · B-1 |
| R-2 | `front.groups[].by` 는 묶은 까닭이 둘이면 「span · scope」 로 함께 적는다 · 혼자 무리는 `null` | §7-3 |
| R-3 | VP 가 `indication` 1위 시술 질문에도 돈다(후보 수십 · 요청 +1 ~ 2) | §3-7-4 VP1 · O-35 |
| R-4 | `entry.value_pick{kinds, candidates, requests, per_candidate[], picked[], uncovered_filters[], reread_calls, deferred_detail_calls, deferred, br5}` 자리 · 이름 | §7-3 · B-5 |
| R-5 | EN1 뒤 종류 · 범위를 다시 세지 않음 · EN1 확인 조회(`limit 1`) 1 회 | §3-7-4 EN1 |
| R-6 | 새 trace 칸 `verified_lines[].marks06` · `breadth[].mark` · `widened`(`w4` · `b3`) · `from_risk` · `visited[].purpose` = `group`(B-7) · `front.offered[].by` = `kd11` · `front.thresholds.kind_read` | §7-3 |
| R-7 | N-2 「걸기 전」 = coverage(adverse) = `g_adverse` 행 수(상세 아님) | §10 · W-7 |
| R-8 | 이름 목록의 LLM 꼴 = `{"value": {입구 표: [이름]}, "layer": {…}}`(verified 순서 · 값 쪽 먼저 · 이름 중복 0) · 기록 `answer_check{roster{entry, value, layer}, said, missing, missing_codes}` | O-32 ② · §7-3 |
| R-9 | SD1 층 표지 꼴 `same_day_layer[{of: 대상 이름, layer: scope role}]` · 「두 대상」 = 대상마다 자신 또는 `scope` 의 물려받음 · 하위 * 항목이 하나라도(한 항목이 둘을 겸해도 됨) | §3-7-5 SD1 |
| R-10 | KD 차례 = KD5 → KD10 → KD9 → KD6 → RG1 · KD3(KD11) | §3-1 · §3-7-2 |
| R-11 | 키 갈래 셈 — (다) 갈래 합 41 · 706 · 141(Q12 · Q13 층이 준 몫) · SPEC 「층 대상 47 → 22 · 39 → 20 · 3 → 3」 과 셈 단위가 다름 | §3-7-5 · §3-7-6 |
| R-12 | 무리 판정 scope 는 대상 둘 이상인 모든 문항에서(짝 종류 없어도) | §3-7-3 · N-7 |

## 9. 남은 것(코디 · 사용자)

1. 코디: `key-diff-v06.md` · `key-table.md` 로 Q12 · Q13 · Q14 사용자 재확인(U-8) → `--confirm Q12,Q13,Q14` → 34 잇기(`--confirm <§2 의 34> --by <사용자>`) → `batch --check` 37 / 37.
2. 코디: 18220 을 새 앱 코드로 다시 띄운 뒤 37 batch(E11 — WORK §12 명령) · 그 앞에 명세 → 키를 한 번 더 뽑아 확인이 이어지는지(W-6).
3. 사용자: 프롬프트 초안(§6 바뀐 줄) 확인(C-1) — §5 주의 1 함께.
