# 앱 재검수 1(r2) — 앱 수정 1 뒤(clinic_chat · `kknaksss/phub-gold-jev` · 커밋 없음)

검수자: reviewer_code(read-only) · 2026-11-16 · 대상 = 작업 트리 그대로(파일 수정 · stash · checkout 없음 · `.env` 안 엶 · Jev · claude 실호출 0 · 허브 18105 안 건드림 — GET 도 안 함)
기준: `review-code-app.md`(1차 FAIL 1 · WARN 8) · `app-fix1-instructions.md` · `_RESUME.md` §2 「앱 검수 뒤」 행
공개 레포 규칙: 질문 문장 · 답 · 원장 · gold 값 · 시술 이름은 적지 않는다. 재현은 합성 이름(`AAA` · `M1` …)으로만.

## 0. 판정 — **FAIL**(새 FAIL 1 · 새 NOTE 3) · 1차 지적 11 은 전부 닫힘

| 묶음 | 판정 | 한 줄 |
|---|---|---|
| ① 닫힘 표(F-1 · W-1~W-8 · Q10 · Q25) | **PASS** | 11/11 닫힘 · 시험이 붙어 있음 |
| ② 원칙 grep | **FAIL** | 묻지 않은 안전 정보를 붙이는 자리 0. 단 **W-3 고침이 폭을 줄이는 자리 1 을 새로 만듦(R2-F1)** |
| ③ 새 구멍 | R2-F1 · R2-N1 ~ N3 | 아래 §3 |
| ④ 시험 | **PASS** | `ruff` All checks passed · `pytest -q` **102 passed**(3.89 s · 1차 85 → +17) |
| ⑤ 커밋 후보 grep | **PASS** | 79 파일 · 키 · 홈 경로 · 실제 gid/LCK · 시술 이름 0 |
| ⑥ README e2e | **PASS**(NOTE 1) | 명령 · 인자가 진입점 `argparse` 와 다 맞음 · 1차 §6 헷갈릴 자리 9 개 다 반영 |

FAIL 은 R2-F1 하나다. 고칠 곳은 `entry.py:184-193` 몇 줄이다.

## 1. 닫힘 표

| # | 닫힘 | 자리(파일:줄) | 시험 |
|---|---|---|---|
| **F-1** 짧은 조각 빼기 | **닫힘**: 빼는 동작을 없앴다. 조각마다 개념을 모으고, 포함 관계로는 빼지 않는다 | `clinic_chat/walk/entry.py:10-11 · 47-60` | `tests/test_walk_entry.py:105`(짧은 이름 ⊂ 긴 이름) · `:111`(낱말 경계 아닌 포함) |
| **W-1** 속성 시작 facet | **닫힘(결정대로)**: 기본은 개요 · 적응이다. 부작용 · 금기 · 상품은 그 범위를 읽기로 했을 때만 읽는다(`ATTR_FACETS` ∩ 허용) | `clinic_chat/walk/ranges.py:67-83` · `calls.py:121-124` · 키 쪽도 같은 함수 `evalset/key_calls.py:118 · 170` · depth `calls.py:297-301` | `tests/test_walk_ranges.py:58` |
| **W-2** 대상 + 재료 입구 → K3 중단 | **닫힘**: G7 에서 빼고 `unused[{why: br1_no_attr_filter}]` 로 남긴다 | `walk/gate.py:66-76` · `columns/col_b.py:82` | `tests/test_walk_core.py:201` |
| **W-3** 상품 이름 길 | **닫힘**: B 가 `offer_name` 입구를 만든다. resolve 조각을 질문 자리 순서로 이어 붙인 구를 쓴다 · G7 이 `offer_name_contains` 를 참조로 본다. **R2-F1 참고** | `walk/entry.py:63-90 · 183-186` · `gate.py:26-27` · `calls.py:189-190` | `tests/test_walk_entry.py:118 · 126 · 136` |
| **W-4** FT5 | **닫힘**: `fold_failed` 면 `실행 중단 · FT5 · groups=[]` 로 두고 빈 verified 로 단계 ⑤ 를 부른다 | `columns/col_b.py:127-129 · 177-180` | `tests/test_walk_core.py:216` |
| **W-5** D4 인용 번호 | **닫힘**: `CITE_MARK_RE` · `RAW_CITE_RE` · 줄 머리 목록 번호를 지운 뒤 숫자를 센다 | `quality/checks.py:15-17 · 98` | `tests/test_quality.py:137` |
| **W-6** 보고서 §10 | **닫힘**: 두 벌(전체 / 원장 = silver) · D3 비율 · D7 비율 · `missed_must_rows` · M1 · D9 · `graded_end_state` 일치 · ttft · 호출 · 토큰 · 범위별 · 상태별 · B 전용(D6 · 범위 Choice 정답 · RG 분포 · 입구 고르기 · 깊이 분포 · complete · K 실패 · 쪽>1 · `unused`) · 끔/켬 표 · judge id 는 quality 줄에서 · 「가장 낮은 effort」 문장 | `report.py:96-148 · 173-256 · 259-297` | `tests/test_quality.py:144` |
| **W-7** 시작 표 밖 입구 | **닫힘(최소 꼴)**: `unused[{why: range_start_tables}]` 를 trace 에 남기고 보고서에 수를 낸다. 범위를 더하는 꼴은 SPEC 결정으로 남김 | `walk/gate.py:71-72` · `report.py:230 · 249` | `tests/test_walk_core.py:209` |
| **W-8** draft 확정 · 37 밖 명세 | **닫힘**: `loader --confirm --by` 명령 · `key_calls --from-set` 진입점(같은 `breadth_calls`) · 입구 없는 문항은 `calls=[]` 명세 + 지금 build · README 순서 | `evalset/loader.py:86-114` · `key_calls.py:153-191` · `answer_key.py:246-247` · `README.md:24-25 · 32` | `tests/test_answer_key.py:153` |
| **Q10** (가) 의 상위 펼침 행 | **닫힘**: `counted_rows` 가 `hier.match = 상위` 를 뺀다. B(`end_state.unsettled`)와 키(`answer_key.expected_state`)가 같은 `unsettled_rows` 를 쓴다. 그 행은 폭에 그대로 남는다. 로컬 키 다시 뽑음(19:02): Q10 = 원천 미확정 (가) · 행 18 | `walk/end_state.py:26-50 · 71-76` · `evalset/answer_key.py:27 · 130-135` | `tests/test_walk_core.py:179 · 187` · `tests/test_answer_key.py:112` |
| **Q25** 순서·간격 고정 갈래 | **닫힘**: 갈래는 좁은 그대로(`ranges.py:57`) · BR3 한 줄(`key_calls.py:8-10` · 요약 꼬리말 `answer_key.py:305-306`) · `range_excluded.classes` · `sample_check.out_of_range`. 키 행에는 넣지 않는다. 로컬 Q25: 표본 6 = 키 안 3 + 범위 갈래 밖 3 · missing 0 · N-9 꼬리표도 「좁음」 으로 갈림(`:273-276`) | `evalset/key_calls.py:108-116` · `answer_key.py:5-7 · 180-183 · 194-210 · 273-276` | `tests/test_answer_key.py:121` |

1차 NOTE 중 같이 닫힌 것(코드에서 확인): N-2 해시 대조(`grade.py:52-54`) · N-3 `answer_key_sha_graded`(`grade.py:135`) · N-9 · N-10(README:44 「모르는 이름이면 멈춘다」). 나머지는 이번 범위 밖이라 보지 않았다.

## 2. 원칙 grep

| 원칙 | 결과 | 근거 |
|---|---|---|
| 폭이 Jev 점수 · 상한 · 상위 N · 잘라 내기 · 칸 빼기로 줄어드는 자리 0 | **1 자리 — R2-F1**(새로 생김). 그 밖에 걸린 것은 아래뿐이고 모두 폭이 아니다 | `grep -nE "\[:[0-9a-z_]+\]\|top_?n\|limit\|\.pop\(\|del \|remove\(\|discard\("`(walk · col_b · hub_rest): `gate.py:46 · 103 · 108` `[:50]` = trace 표시만(`_n` 셈은 전체) · `breadth.py:62` 큐 pop · `entry.py:102 · 152` `[:2]` = RG3 · RG6 「두 개 다 읽음」(넓히기) · `hub_rest.py:138` 쪽 크기(`read_all` 은 끝까지) · 오류 글 `[:200/300]` |
| 묻지 않은 안전 정보를 붙이는 자리 0 | **0**: 속성 시작은 `attr_facets` 로 막았고(W-1), depth 의 속성 대상은 읽기로 한 범위의 `breadth_calls` 만 쓴다(`calls.py:297-301`). 안전 facet 을 부르는 자리는 adverse · avoid 범위와 RG8(질문에 사건 · 조건 입구가 있을 때)뿐이다. 프롬프트 `common.md:15` · `judge.md:6 · 9` 는 「묻지 않은 것 붙이지 않음」 을 그대로 지킨다 | `grep -nE "adverse\|contraindication\|금기\|부작용\|안전" clinic_chat/walk clinic_chat/columns prompts` |

## 3. 새 구멍

| # | 파일:줄 | 심각도 | 무엇 · 재현 | 고칠 방향 |
|---|---|---|---|---|
| **R2-F1** | `clinic_chat/walk/entry.py:184-193` · `columns/col_b.py:68-69` · `walk/gate.py:73-74` | **FAIL**(폭 줄임 · BR3 B ≠ 키) | W-3 조건이 「상품 범위인데 상품 시작 표(제품 · 시술 · 케이스 · 상품) 입구가 없으면」 이다. 그래서 **속성 입구만 풀린 질문**(재료 · 부위 + 상품 범위)에도 `offer_name` 입구가 붙는다. 그러면 `attr_start` 가 거짓이 되고(`:192-193`), B 는 속성 시작 길 대신 `breadth_calls("offer")` 를 탄다. 결과: **그 속성의 `offer` · `profile` · `indication` facet 을 하나도 읽지 않는다**. gate 는 그 입구를 `unused · br1_no_attr_filter` 로만 적고 통과한다(멈추지 않음). 합성 재현: `breadth_calls("offer", [material:M1, offer_name:AAA])` → `[offer_name_contains:AAA]` 하나뿐. 키 쪽 `key_calls.build_spec`(같은 문항, 입구 = material)은 `ATTR_START` → `[material:M1 profile, material:M1 offer]`. 부위도 같다(→ profile · indication · offer 셋이 빠짐). 지금 확정 세트에는 이 꼴이 없다(상품 범위 확정 4 문항 = 제품 · 시술 · offer_name). 자유 질문 · 추가 문항(재료 · 부위 시작 묶음)에서 걸린다 | (a) **넓히기만**(추천): `attr_start` 는 `offer_name` 을 빼고 셈하고, 속성 시작 길에 `offer_name` 호출을 덧붙인다(`calls.py` ATTR_START 가지에서 `by_table["offer_name"]` 도 부름). 또는 (b) 속성 입구가 있으면 `offer_name` 을 붙이지 않는다(SPEC 「상품 이름으로**만** 풀리면」 에 더 가까움). 시험: 「재료 입구만 + 상품 범위」 에서 material offer facet 이 B 호출에 있고 B 호출 = 키 호출 |
| R2-N1 | `clinic_chat/walk/end_state.py:30-49` | NOTE | 상위 펼침 행 빼기가 (가) 뿐 아니라 **(나)** 셈에도 걸린다(`counted_rows` 공유). 결정 글은 (가) 만 말한다. 이렇게 하면 「자기 행 전부 못 닿음 + 상위 행은 닿음」 이 (나) 가 된다. 뜻으로는 맞는 쪽(물은 코드 자신의 행)이고 B ↔ 키가 같은 함수라 갈라지지는 않는다 | SPEC-002 0.4.2 되적기 때 (나) 에도 같다고 한 줄 |
| R2-N2 | `clinic_chat/walk/ranges.py:70-71` | NOTE | 속성 시작 + 시술 범위면 `outcome`(효과)도 읽는다. 결정 글은 「대상 + 적응 · 개요만」 인데 시술 범위가 효과를 허용하는 범위라서다. 안전 facet 이 아니라 원칙에는 걸리지 않는다 | 되적기 때 「범위가 시술이면 효과까지」 를 적거나 빼거나 — 코디 확인 |
| R2-N3 | `README.md:32 · 44` | NOTE | 「순서(처음 한 번)」 가 `answer_key --all` 로 시작한다. 37 명세 만들기(`key_calls --from-gold-build <gold-build.py>`)는 표 `:23` 에만 있고 `<gold-build.py>` 자리(로컬 데이터 폴더)도 적혀 있지 않다. `:44` 「B 켬은 `--b-on` 으로」 는 batch 만 맞고 runner 에는 `--b-on` 이 없다(기본 켬 · `--no-b-on` 만) | 순서 첫머리에 `key_calls --from-gold-build`(명세가 없을 때)와 경로 안내 한 줄 · `:44` 를 「batch `--b-on/--no-b-on` · runner 는 `--no-b-on`」 으로 |

## 4. 시험(1 회)

| 명령 | 결과 |
|---|---|
| `uv run ruff check .` | All checks passed! |
| `uv run pytest -q`(`TYPESAFE_API_KEY` · `ANTHROPIC_API_KEY` env 지움) | **102 passed in 3.89s** |
| 합성 재현(`python -I -c` · 레포 파일 안 씀 · 허브 안 부름) | R2-F1 위 값 그대로 |
| 로컬 키 읽기(값 안 옮김) | Q10 = 원천 미확정 (가) · Q25 표본 3 in + 3 out_of_range · missing 0 · `key-summary.md` 키 37 · 걸린 16 |

## 5. 커밋 후보 grep

`git status --porcelain --ignored`: `M .env.example · M README.md · ?? .python-version · clinic_chat/ · prompts/ · pyproject.toml · tests/ · uv.lock` / `!! .env · data/ · runs/ · .venv/ · 캐시`. 커밋 후보 = `git ls-files -m` + `-o --exclude-standard` = **79 파일**(그중 `data/` · `runs/` · `raw/` · `*.jsonl` · `.env` 0).

| 찾은 것 | 식 | 결과 |
|---|---|---|
| 홈 경로 · 계정 | `/Users/\|/home/\|kknaks\|medisolve` | **0** |
| 키 꼴 | `sk-ant\|sk-[A-Za-z0-9]{20,}\|Bearer …\|(API_KEY\|TOKEN\|SECRET)=<값>` | **0** |
| gid · LCK | `\bG[A-Z]{2}-[0-9]{5}\b\|LCK-[0-9]+` | 전부 합성(`G??-9xxxx` · `GXX-00001` · `LCK-8/9/900` 시험 fixture) |
| 시술 · 고민 이름 | 흔한 시술 · 제품 · 고민 낱말 20 개 | **0**(한 줄 걸림 = README 「나온다」 의 글자 겹침 · 거짓 양성) |

## 6. README e2e(명령만 읽음 · 실행 안 함)

표 `README.md:12-30` 의 명령 19 줄을 진입점 `argparse` 와 대조했다(`runner` `--question/--set-id/--columns/--no-b-on/--show-answers` · `batch` `--check/--label/--ids/--bundle/--range/--columns/--b-on/--no-b-on/--resume` · `quality.grade` `--batch/--plumbing` · `evalset.key_calls` `--from-gold-build/--from-set/--ids` · `evalset.answer_key` `--all/--ids/--confirm/--by` · `evalset.loader` `--validate/--confirm/--by` · `prompts` `--confirm/--by` · `report` `--batch` · `runs` `--show/--column/--trace`). **모르는 인자 0.** 결과 자리(`runs/runs.jsonl` · `quality.jsonl` · `reports/<batch_id>.md` · `plumbing/` · `data/eval-set/…`)도 코드와 맞는다. 1차 §6 헷갈릴 자리 9 개는 `README.md:34-45` 에 다 들어갔다(+ 10 「추론 끔 = low effort」). 따라 할 수 있다. 다듬을 것은 R2-N3 하나다.

## 7. 다음(코디)

1. R2-F1 고침 — (a) 넓히기만 / (b) 속성 입구가 있으면 `offer_name` 안 붙임 중 고르기 · 시험 한 꼴. 코드 몇 줄이라 재검수 없이 코디 grep · pytest 로 닫아도 된다.
2. R2-N1 · N2 는 SPEC-002 0.4.2 되적기 때 한 줄씩. R2-N3 은 README 두 줄.
