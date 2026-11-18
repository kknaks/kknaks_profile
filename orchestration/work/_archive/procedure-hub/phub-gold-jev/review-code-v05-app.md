# 코드 검수 — 앱 v05(WORK-006 · SPEC-002 0.5.1 구현분)

- 검수: reviewer_code · 2026-11-16 · read-only · 대상 `APP-WT`(clinic_chat 워크트리 · branch `kknaksss/phub-gold-jev` · 미커밋)
- 계약: `SPEC-002-chat-eval.md` 0.5.1 · `WORK-006-app-v05.md` 0.1.0 · `_RESUME.md` §2 맨 위 행(W-1 ~ W-5 · B-1 · A-1 · B-2) · `review-work-v05.md` · `kd8-jev-check-report.md`
- 경로 접두어: `APP-WT` = 앱 워크트리 · `$W` = 이 폴더. 질문 문장 · 시술 이름 · 실제 코드 · gid 는 이 문서에 없다.

## 판정: **WARN** (FAIL 0 · WARN 4 · NOTE 9)

주 경로(맨 앞 판단 → 대상 × 종류 읽기 → RQ1 → 싣는 칸 · 줄 번호 → gate → 답 꼬리)는 SPEC 대로 섰고, 실물 다섯(E7 ~ E11)도 기대대로 났다. 다만 **폭이 줄거나 빈손이 되는 가장자리 둘**(W-1 · W-2)이 코드로 재현된다 — 둘 다 SPEC 이 직접 막지 않은 자리라 코디 결정이 필요하다. W-3 · W-4 는 세트 칸 · README 고침이다.

## 1. 시험(직접 한 번 · 실호출 없음)

| 명령 | 결과 |
|---|---|
| `uv sync` | 0 |
| `uv run ruff check .` | All checks passed |
| `uv run pytest -q` | **149 passed · 1 skipped**(5.3 s) — 기준선 138 대비 +11(시험 함수 142 개). skip 1 = `tests/test_walk_ranges.py:130` 「데이터 env 없음」 |
| 데이터 env 판: `GOLD_CSV_DIR=<로컬 데이터 폴더>/gold uv run pytest -q tests/test_walk_ranges.py` | **13 passed**(§3-2a 13 줄의 싣는 칸이 gold CSV 헤더에 다 있음 — 헤더 밖 칸 0) |
| 허브 GET(건드리지 않음) | 18105 · 18106 둘 다 `health` 같은 `gold_hash`(8accbb…) · `coverage` 경로 응답(가짜 노드 → 404 not_found = 경로 있음) — 18105 는 이미 새 허브다 |

- 검수 중 **모의 시험 파일을 `tests/` 에 잠깐 만들었다 지웠다**(W-1 재현용 두 번 · 실행 뒤 바로 삭제 · `git status` 그대로). 파일을 고친 것은 없다.

## 2. WP 마다 완료 조건 · 계약 대조

| WP | 판정 | 근거(파일:줄) |
|---|---|---|
| WP-0 KD8 | 맞음 | `prompts/jev/front.md` 의 `kind` 문구 = KD8 고친 판(이름을 글자로) · `target` · `entry` · `candidate` 도 `"{name}"` + `{id}` 함께(`walk/jev_requests.py:27-34`). 시험 `test_walk_front.py` |
| WP-1 허브 · 모의 · C 도구 8 | 맞음 | `clients/hub_rest.py:206-216`(64 씩 나눔 · build 바뀌면 오류) · `--ping` 이 맞춤 꼴 · coverage 키 집합을 냄(`:260-279`) · `particle` 낱말 0 · 시험 `test_coverage_splits_over_64_and_keeps_order` |
| WP-2 맨 앞 판단 | 맞음(W-1 가장자리) | `walk/front.py:148-152`(KD1 · KD2) · `:192-212`(TG3 겹침 = 범위 규칙 먼저 · 속성 표는 시작 표 다음) · `:213-234`(yes = target · 사이 = uncertain_kept · 덮이지 않은 no = named · 덮인 no = dropped) · `:246-251`(KD5 · TG2 면 `via`) · `:253-259`(KD6) · `:261-271`(RG1 → KD3 · offered) · 입구 고르기는 `if not concepts` 안에서만(`:160`) · Jev 요청 1(실물 E7 ~ E11 전부 `jev_requests` = 1) |
| WP-3 읽기 · RQ1 · 종료 | 맞음 | `walk/calls.py:205-246` `plan_calls` 하나를 B(`col_b.py:116`) · 답 키(`evalset/key_calls.py:121-131`) · (가) 판정용(`col_b.py:168`)이 함께 씀 · roles = 자기 · 물려받음 · 하위 셋(`ranges.py:16`) · 제품 offer = 자기 · 하위 제품(`calls.py:162`) · RQ1 네 줄(`walk/required.py:53-60`) · overview/mechanism 은 칸 값으로(`kinds.py:197-203`) · `coverage_mismatch` 는 좁힘 없는 조회에서만(`required.py:101-106` · W-2 결정 그대로) · 판정용 행은 verified 밖(`breadth.py:87-88`) · 상위 펼침 제외(`end_state.py:32-35`) |
| WP-4 싣는 칸 · 줄 번호 · gate | 맞음 | `kinds.py:133-169` = SPEC §3-2a 표 13 줄과 칸까지 같음(데이터 env 시험 통과) · 줄마다 `n` · `verified_lines`(`material.py:98-118`) · 재료에 gid · silver · price_mid_raw 없음을 K4 가 봄(`gate.py:123-125`) · K5(`:128-133`) · G12(`:136-138`) · N-1 표지용 조회 `purpose=label` · verified 밖(`col_b.py:72-90` · B-1 그대로) |
| WP-5 답 프롬프트 · 꼬리 | 맞음 | `prompts/common.md` P2 · P9(10번) · P10(11번) · `col_b.md` 「답 꼬리」 · 표식 `<<<근거>>>`(`col_b.py:41`) · 떼기 · 깨지면 `null`(`:210-228`) · 스트리밍 표식 뒤 안 흘림(`:231-256`) · `answer_tail_chars`(`:319`) |
| WP-6 열 정리 · 화면 | 맞음 | `b_slim` · `select_ms` · `selection` 낱말 0(옛 줄 비움 처리 `web/static/app.js:78` 한 줄만 `range_choice` 언급) · `ALL_COLS` 에 `b_full`(`runner.py:31`) · 화면 B 켬 기본 끔(`web/server.py:48`) · 속도 탭 열 b · c · b_full(`speed.py:18`) · 화면 새 글자는 SPEC 용어 · trace 필드 이름 · 옛 화면 말뿐 |
| WP-7 세트 · 답 키 | 일부(W-3) | 세트 85 줄 · 묶음 수 맞음 · `loader --validate` → `{"lines": 85, "draft": 48, "errors": []}` · `expected_kinds` 81(빈 4 = 범위 밖 · 이름 없음) · 키 37 다시 뽑음(`key-summary.md` 걸린 33) · `_v041/` 옮김 · Q10 (가) · Q33 (나) · Q12 (다) 그대로. **`expected_entries[]` 가 66 문항에서 빈 목록**(37 전부) |
| WP-8 채점 · 보고서 | 맞음 | D1 · D2(B = 꼬리 줄 번호 ⊂ `verified_lines.n` — `quality/checks.py:60-75`) · D10(`:169-181` · A 는 「해당 없음」) · 미확인 키 거부 그대로(`quality/grade.py:48` · 풀어 주는 플래그 없음) · 「B 전용」 맨 앞 판단 줄(`report.py:195-260`) |
| WP-9 실물 · 마감 | 맞음(단건) | 아래 표 — `runs.jsonl` 의 0.5 줄 9(같은 문항 되돌림 포함) |

**실물 다섯(runs.jsonl · effort low · 단건이라 편차 큼)**

| # | B 종료 | 대상 · 종류 | required(`met_by`) | B 입력 | 첫 답 글자 B / C |
|---|---|---|---|---|---|
| E7 | 근거 충족 | 제품 1(target) · 개요(default) + 효과(yes) | 효과 = **lower**(자기 0 · 하위 4 · 물려받음 19) | 12.1 KB | 6.6 s / 9.5 s |
| E8 | 근거 충족 | — | 원리 = **inherited** | 4.9 KB | — |
| E9 | 근거 충족 | 고민 1 target · 같은 조각 부위 = overlap(규칙) · 덮인 조각 2 dropped | 적응 = self(74) | **36.5 KB**(0.4.1 110 KB) · `b_full` 40.9 KB | 8.5 s / 10.4 s |
| E10 | 근거 충족 | 개요 | 개요 = self | 5.7 KB | — |
| E11(Q22) | 근거 충족 | 대상 4(부분 일치 포함 · 전부 yes) · 덮인 효과 조각 dropped | 동시 가능 4 = self | 8.9 KB | **1.7 s** / 9.7 s(기준선 2.2 s) |

- 다섯 다 `coverage_mismatch` 0 · `answer_lines` 섬 · 쪽 1 · `entry.unused` 0.

## 3. 원칙 · 안전 · 지어낸 동작

| 볼 것 | 결과 |
|---|---|
| 대상 × 필요한 정보 안에서 빠짐없이 | 주 경로는 섬 — 쪽 넘김 끝까지 · 못 읽으면 실행 중단(`breadth.py:85-86`) · 깊이 Noul 은 깊이만(`depth.py:95-103`) · 대상은 뒤에서 안 빠짐(G7 · `gate.py:85-86`). **예외 W-2**(부위 둘 이상이면 첫 부위만 필터) |
| 행 안 뺌 · LLM 에는 필요한 칸만 | 줄 수 = verified 수 = `verified_lines` 수를 K1 이 봄(`gate.py:48-53`) · 칸은 종류가 정함 · `listed_only` 줄도 같은 칸(`material.py:99`) · 쪽 나눔만 있고 잘라 내기 없음(`fold.py`) |
| 안전 강제 첨부 0 | 기본 묶음에 안전 종류 없음(`kinds.py:67-71` · 시술 · 부위·고민 · 속성 시작) · 속성 시작은 읽기로 한 종류의 facet 만(`calls.py:214-219`). 안전 종류가 읽히는 길은 yes · 1위 · KD5 · 그 범위의 기본(KD3)뿐 = SPEC 그대로. `b_full` 은 14 종류 전부(안전 포함)지만 채점 밖 측정 열(review-work N-7 · README 에 밝힘) |
| 지어낸 동작 | SPEC 밖 이름은 WORK §15 가 「제안」 으로 둔 것뿐(`b_full` · `answer_tail_chars` · `coverage_mismatch` · `purpose=label` — B-1 받음). 작은 어긋남은 NOTE N-2 · N-3 · N-7 |
| Jev 는 앱이 펼친 선택지 안에서만 | Jev 응답에서 읽는 것은 `noul` 뿐(`jev_requests.py:56-60` · `:87-90`) · Choice 는 E1 연결 확인에만(N-1) |

## 4. 지적

### WARN

| # | 파일:줄 | 무엇 | 근거 | 고칠 방향 |
|---|---|---|---|---|
| W-1 | `walk/front.py:252-268` · `walk/gate.py:85-86` | **읽을 종류가 0 이 되는 질문이 있다 → 「실행 중단(gate:K3)」.** 속성 입구만 풀린 질문(예: 부위 하나)에서 Jev 가 그 속성 표에 조회가 없는 종류(`recovery` · `lineup` …)만 yes 로 내면: `by` 가 비지 않아 KD6 이 안 돌고 · 그 종류는 `applicable` 아님(KD4 건너뜀) · 범위 0 → 기본 묶음도 0 → `kinds = []` · 조회 0. 그러면 G7(명시 대상이 재료에 없음)로 K3 실패 → 실행 중단 · 답은 「끝까지 확인하지 못했다」. **모의로 재현**: 부위 대상 + `recovery` 0.9 → `kinds []` · `end 실행 중단 gate:K3` · verified 0 / 재료 대상 + `lineup` 0.9 · 개요 0.5 → `kinds []` · 개요는 `offered` 로만 | SPEC §3-1 KD4(건너뜀) · KD6(「전부 no 이하」 일 때만) · KD6 근거 「빈손으로 끝내지 않는다」 · §5 「실행 중단」 은 오류 · 시간 초과 자리. SPEC 이 이 꼴을 직접 정하지 않았다(구멍) | 코디 결정 — 추천: 「읽기로 한 종류가 대상의 표에 전부 없으면(KD4 로 다 건너뜀) KD6 처럼 그 대상 표의 기본 묶음을 읽는다(`kinds_by` = `default`)」 를 한 줄로 · SPEC 되적기 후보. 고치면 B · 답 키가 같은 `front` 결과를 쓰므로 함께 바뀐다 |
| W-2 | `walk/calls.py:97-101` · `:171-174` | **부위 입구가 둘 이상이면 첫 부위만 필터로 건다** — 둘째 부위에 맞는 행은 읽히지 않고, 그 부위 입구는 `entry.unused[]` 에 `br1_no_attr_filter`(필터 길이 없다는 까닭 — 실제 까닭과 다름)로 남는다. 사건 · 조건은 입구마다 조회를 나눈다(`:146-148` · `:156-157`)와 갈림. 확인: 시술 1 + 부위 2 → `filters.site_name` = 첫 부위 하나만 | SPEC §3-1 BR1(질문이 이름 댄 입구로 필터) · 원칙(대상 × 필요한 정보 안에서 빠짐없이) · TG6(필터 없는 입구만 unused) | 부위도 사건 · 조건처럼 **부위마다 조회를 나눈다**(`concern_candidates` 의 `site` 도 같은 식). `plan_calls` 한 곳이라 키 명세도 함께 바뀐다. 0.4.1 부터 있던 꼴인지는 코디가 확인 |
| W-3 | 로컬 `data/eval-set/set.jsonl` · `report.py:215-224` | **`expected_entries[]` 가 85 중 66 문항에서 빈 목록이다**(37 전부 · 추가 18 · 범위 밖 4 · 속성 시작 4 · …). 보고서 「B 전용 — 대상 일치」 는 `expected_entries` 가 있는 문항만 세므로 37 에서는 대상 일치가 안 잡힌다(`named` 가운데 기대 아님 수도 0 으로 셈). 37 의 기대 입구는 명세(`calls/<id>.json` 의 `entries`)에만 있다 | WORK-006 WP-7 1(「`expected_entries[]` 는 모든 문항에」) · WP-8 5 | 37 은 명세 `entries` 를 세트 칸에 옮기거나(결정론 · 같은 값), 보고서가 세트 칸이 비면 명세 `entries` 를 읽게. 범위 밖 · 이름 없음은 빈 목록이 맞는 값이면 그대로 |
| W-4 | `README.md` 「실행 안내」 표 · 「헷갈릴 자리」 9 · 11 · 「검증」 | 사용자가 따라 할 때 헷갈릴 자리 셋: ① 9 는 「`--columns` 는 `a,b,c` 중」 · 11 은 「`a,b,c,b_full`」 — 서로 다름 ② 표의 「한 질문 · B · C · B 전체(속도)」 줄은 `runner` 로 돌리는데 `runner` 에 effort 인자가 없어 B `low` · C `medium` 이다(review-work W-1) — 속도 비교는 화면 속도 탭으로만 같은 조건이라는 말이 없다 ③ 「검증」 줄에 데이터 env 판(`GOLD_CSV_DIR=… pytest tests/test_walk_ranges.py`)이 없다 — 지금은 skip 1 이 왜 나는지 README 로 못 안다 | SPEC-002 §10-1 「속도 탭 조건 맞춤」 · 결정 「화면은 열 동시 실행」 | 9 를 11 에 맞추고 · 그 줄에 「effort 가 열마다 다르다 — 같은 조건 비교는 속도 탭」 한 마디 · 「검증」 에 데이터 env 한 줄 |

### NOTE

| # | 파일:줄 | 한 줄 |
|---|---|---|
| N-1 | `clients/jev_client.py:105-123` | `Choice` 낱말이 `clinic_chat/` 에 남았다 — E1 연결 확인(`--ping`)의 합성 요청에만 쓰고 걷기에는 없다. WP-2 완료 8 은 글자 그대로는 안 맞음 |
| N-2 | `walk/front.py:180` · `:187` · `walk/entry.py:119-120` | 입구 고르기로 확정한 입구의 trace `entry.by` = `entry_pick`(SPEC §3-1 입구 고르기 「지킬 것」 은 `noul`) · 대상 길은 `noul`. 값 이름만 다름 — 보고서 · 화면이 둘을 갈라 읽는지 맞춰 둘 것 |
| N-3 | `columns/col_b.py:122` | `timing.stages[]` 에 `depth` 가 하나 더 있다(WP-6 5 의 이름 목록 밖) · 깊이의 Jev 시간이 이 단계에 섞인다 |
| N-4 | `report.py:207-208` | 보고서의 Noul 띠(yes · 사이 · no)가 0.7 · 0.3 고정 — 설정 문턱을 바꾸면 보고서 띠와 앱 판정이 갈린다 |
| N-5 | `walk/material.py:181-185` | 묶음 머리에 `"table": "g_…"`(gold 표 이름)이 LLM 에 간다 — id 는 아니지만 SPEC §3-2a 「기록에만 두는 칸」 의 `gold_table` 이다. 1회차 trace 뒤 O-28 때 함께 |
| N-6 | `walk/material.py:102-109` | 허브 행에 없는 싣는 칸을 `""` 로 싣는다(「빈칸」 과 「칸이 응답에 없음」 이 같게 보임 · `absent_columns` 에만 기록). 지금 실물 다섯에서는 영향 없음 |
| N-7 | `walk/front.py:184-185` | 「범위 밖」 이면 `scope_gap` 을 끈다 — SPEC 에 없는 동작이지만 `gap` 값은 그대로 기록돼 무해 |
| N-8 | `columns/col_b.py:155-176` | (가) 판정은 늘 조회로 한다(`by: query` · `coverage_zero` 는 기록만) — N-6 의 「SPEC 본문대로 조회」 쪽이라 안전하나, Q10 · 고민 대상에서 coverage 셈 ↔ 조회 셈 대조 수는 시험 · 보고에 없다 |
| N-9 | 로컬 `key-summary.md` | 키 37 가운데 걸린 문항 33 — 대부분 `expected_kinds` 초안 확인(B-3 개요/원리 둘 다 · `g_scope` 층 길) 꼴. 사용자 답 키 확인 부담이 크다 |

## 5. 커밋 후보 grep(공개 레포)

- `git status --porcelain --ignored`: 커밋 후보 = `.env.example` · `README.md`(수정) · `.python-version` · `clinic_chat/**` · `prompts/**` · `tests/**` · `pyproject.toml` · `uv.lock`(새 파일 98) / gitignore = `.env` · `data/` · `runs/` · 캐시(`.gitignore:2 · 7 · 8`).
- 커밋 후보 98 파일에서: 실제 꼴 gid(`G[A-Z]{2}-[0-8]\d{4}`) **0** · LCK id(시험용 `LCK-900` 밖) **0** · 홈 경로 · 사용자 이름 **0** · 키 꼴(`sk-…` 등) **0** · 실제 코드 꼴(`PRD-` 등) **0** · 메일 **0** · gold 한국어 이름(`g_node` · `g_profile` · `g_offer` · `g_package` 의 이름 1335 개 중 3 글자 이상) **0** · 세트 질문 문장 조각(문장 있는 48) **0**. 영어 짧은 이름 셋(`LED` · `EMS` · `Body`)은 `LEDGER` · `ITEMS` · FastAPI `Body` 낱말 속 우연 일치.
- `.env.example` 은 이름만(값 빈칸) · `RANGE_*` 둘 빠짐.

## 6. 사용자가 실물에서 만날 자리

1. **부위 · 재료 이름만 든 질문에 회복 · 하위 목록 같은 것을 물으면 「끝까지 확인하지 못했다」 로 답한다**(W-1 — 원인은 실행 오류가 아니라 읽을 종류가 0). trace 의 `end_reason` = `gate:K3` · `front.kinds[]` 에 `skipped` 만.
2. **부위 둘을 함께 말한 질문**은 둘째 부위 행이 빠진 채 「근거 충족」 으로 끝날 수 있다(W-2) — `entry.unused[]` 에 그 부위가 `br1_no_attr_filter` 로 보인다.
3. 부분 일치가 대상으로 늘어난다 — E11 은 대상 4(이름 두 개를 말한 질문)라 쌍 조회가 6 이 된다. 답은 맞았지만 `front.targets[]` 를 보면 「왜 넷이냐」 로 읽힌다(TG1 · TG3 그대로의 동작).
4. **화면 정확도 탭은 B 켬이 기본 꺼짐 · CLI · batch 는 기본 켬** — 같은 질문의 열 수가 화면과 CLI 에서 다르다(README 9 에 있음).
5. **CLI 로 잰 속도는 열마다 effort 가 다르다**(B low · C medium) — 같은 조건은 화면 속도 탭뿐(W-4 ②).
6. 「B 전체」 카드는 묻지 않은 안전 종류까지 읽은 답이다 — 품질 근거가 아니다(README 에 「채점 대상 아님」).
7. 답 꼬리를 모델이 안 쓰거나 꼴이 깨지면 `answer_lines` 가 `null` 이고 화면에는 아무 표시가 없다(답은 그대로) — 근거 추적이 비었는지는 trace 로만 안다.
8. 프롬프트를 한 글자라도 고치면 「프롬프트 미확정(사용자 확인 전)」 이 다시 뜬다 · 답 키 33/37 이 「걸린 문항」 이라 확인 목록이 길다(N-9).
9. 기대 대상 일치 지표는 지금 세트로는 19 문항에서만 셈이 선다(W-3).
