# 앱 코드 검수 — WORK-002 구현(clinic_chat · `kknaksss/phub-gold-jev` · 커밋 없음)

검수자: reviewer_code(read-only) · 2026-11-16 · 대상 = 작업 트리 그대로(파일 수정 · stash · checkout 없음 · `.env` 안 엶 · Jev · claude 실호출 없음 · 허브 18105 건드리지 않음)
기준: SPEC-002 0.4.1 · SPEC-001 §4 · WORK-002 0.2.0 · `_RESUME.md` §2 · llms.txt · 구현 보고 `app-report.md`
공개 레포 규칙: 이 리포트에는 질문 문장 · 답 · 원장 · gold 값 · 시술 이름이 없다. 재현은 합성 이름(`AAA` · `P1` …)으로만 했다.

## 0. 판정 — **FAIL**(FAIL 1 · WARN 8 · NOTE 10)

| 묶음 | 판정 | 한 줄 |
|---|---|---|
| 1 범위 · 공개 레포 | **PASS** | 커밋 후보 79 파일에 키 · 홈 경로 · 실제 gid/LCK · 시술 이름 0. 세트 · 답 키 · runs 는 gitignore 자리에만 |
| 2 원칙 | **FAIL** | 폭 · 종료 · Jev 선택지는 지켜짐. 단 **입구 빠짐 1(F-1)** · **묻지 않은 안전 · 상품을 읽는 자리 1(W-1, SPEC 이 낸 것)** |
| 3 SPEC-002 대조 | **WARN** | RG1~RG8 · FT1~FT4 · K1~K5 · 종료 6 · 세 열 같은 조건 · 가리기 · 미확인 키 거부 · 합성 키 배관은 맞음. 빠진 것: 상품 이름 길(W-3) · FT5 종료(W-4) · 보고서 §10(W-6) · D4 편향(W-5) |
| 4 미결 ①~⑤ | 판정 아래 §4 | ① 맞음 ② **SPEC 구멍** ③ **SPEC 구멍(좁아지는 쪽)** ④ **폭을 줄인다 → F-1** · 패키지 이름 맞음 ⑤ 막는 길 맞음 · 확정 뒤 길이 없음(W-8) |
| 5 시험 | **PASS** | `uv sync` OK · `ruff` All checks passed · `pytest -q` **85 passed**(3.39 s · 실호출 없음) |
| 6 e2e | §6 | 따라 할 수 있다. 헷갈릴 자리 9 |

FAIL 은 F-1 하나다 — 고칠 곳이 함수 하나(`entry.py:43-58`)라 작다. W-1 · Q10 · Q25 는 코드가 SPEC 글자를 따른 결과라 **코디 · 사용자 결정**이 먼저다.

## 1. 범위 · 공개 레포

```
git status --porcelain --ignored
 M .env.example · M README.md · ?? .python-version · ?? clinic_chat/ · ?? prompts/ · ?? pyproject.toml · ?? tests/ · ?? uv.lock
 !! .env · !! data/ · !! runs/ · !! .venv/ · !! 캐시(__pycache__ · .pytest_cache · .ruff_cache)
```

- 커밋 후보 = `git ls-files -m` + `git ls-files -o --exclude-standard` = **79 파일**(위 8 묶음 밖 0). `.gitignore` 안 고침 · `data/` · `runs/` · `raw/` · `*.jsonl` · `.env*`(`.env.example` 제외) 규칙 그대로.
- grep(79 파일 · `xargs /usr/bin/grep`):

| 찾은 것 | 식 | 결과 |
|---|---|---|
| 홈 절대 경로 · 계정 | `/Users/\|/home/\|kknaks\|medisolve` | **0** |
| 키 꼴 | `sk-ant\|sk-[A-Za-z0-9]{20,}\|Bearer …\|API_KEY=<값>` | **0**(`.env.example` 은 이름만 · 값 빈칸) |
| gid · LCK | `\bG[A-Z]{2}-[0-9]{5}\b\|LCK-[0-9]+` | 전부 합성(`GIN-9000x` · `GPF-91000` · `GEN-99001` · `LCK-900` · 예시 `GXX-00001`) — 실제 값 0 |
| 시술 · 고민 이름 | 흔한 시술 · 제품 · 고민 낱말 15 개 | **0**. 시험 fixture 의 한국어는 `가짜시술` · `가짜고민` 꼴뿐 |

- 세트(`data/eval-set/set.jsonl` 69 줄 · `calls/` · `answer-key/` · `key-summary.md` · `pick-candidates.json`) · `runs/runs.jsonl` · `runs/plumbing/` 는 전부 `!!`(무시) 자리.
- 원장 파일 이름도 코드에 박지 않았다(`raw_tools.py:3` — `RAW_DIR` 의 `*.json` 전부).

## 2. 원칙 대조

| 원칙 | 결과 | 근거 |
|---|---|---|
| B 폭을 Jev 점수 · 상한 · 상위 N · 잘라 내기 · 칸 빼기로 줄이는 자리 0 | **폭(단계 ②) 자체는 0** — `read_calls` 는 `next_cursor` 끝까지 · 못 읽으면 `BreadthError` → 실행 중단(`breadth.py:55-80` · `hub_rest.py` `read_all`) · Noul 은 `decisions` 에만 적고 `verified` 를 건드리지 않음(`depth.py:100-117`) · 묶음 표는 같은 값만 머리로 올리고 칸을 빼지 않음 · K1 이 `unfold(fold(x)) == x` 를 확인(`fold.py:56-96` · `gate.py:42`). **그러나 입구 단계에서 빠지는 자리 1 — F-1**(입구가 빠지면 그 입구의 폭 조회가 아예 생기지 않는다) | 시험 `test_any_noul_never_drops_breadth_gids` 통과 |
| 종료 = 폭 다 읽음 + 깊이 판단 끝 + 검사 · `answer_ready` 단독 종료 없음 | **맞음** — `es.decide` 는 `answer_ready` 를 입력으로 받지도 않는다(`end_state.py:48-62`). `answer_ready` 는 ③-3 뒤에 묻고 C1 최솟값(`jev_requests.py:100-102` · `depth.py:147-153`). required 미충족이면 yes 여도 C2 가 돈다(`depth.py:159-160`) | `test_answer_ready_high_but_required_missing_is_not_ok` |
| 묻지 않은 안전 정보를 붙이는 자리 0 | **1 자리 — W-1**: 속성 시작(부위 · 해부 입구만 풀린 질문)이 범위 Choice 와 무관하게 `adverse` · `adverse_detail` · `contraindication` · `offer` facet 을 읽어 답 재료에 싣는다. SPEC-002 §3-2 「속성 시작」 행 · WORK 3-a 가 「맞춤 facet 전부(부위 7)」 로 적은 그대로라 **SPEC 안의 충돌**이다. 그 밖의 범위 표에는 묻지 않은 안전 facet 이 없다(`calls.py:122-187`) · gate 는 붙이지 않는다(`gate.py` 는 확인만) | — |
| Jev 는 앱이 펼친 선택지 안에서만 | **맞음** — Choice 답이 옵션 키에 없으면 `JevError`(`jev_requests.py:40-46`) · 옵션은 범위 9(`ranges.py:77-81`) · 겹친 개념은 허브 `resolve` 후보(`entry.py:102-111`) · 입구 후보는 `resolve` 목록 꼴 끝까지(`entry.py:176-194`). Jev 가 낸 문자열을 id 로 쓰는 길 없음 | `test_choice_outside_options_is_error` |
| Choice 는 하나 고를 때만 · 후보 관련성 = Noul fan-out | **맞음** — Choice 는 `range` · `entity_k` 둘뿐 · 입구 · 깊이 후보는 Noul 32 묶음 전부(`jev_requests.py:79-103`) | — |

## 3. SPEC-002 대조

| 항목 | 결과 | 자리 |
|---|---|---|
| RG1 확실 = conf ≥ 0.7 그리고 1/2 비 ≥ 2.0(설정) | 맞음 | `jev_requests.py:30-33` · `config.py` |
| RG2 · RG3 · RG4 · RG5(`scope_gap`) | 맞음 — 불확실이면 두 범위 · 「범위 밖」 이 2위 안이면 남은 실제 범위 + `scope_gap` · 확실한 「범위 밖」 도 입구 있으면 실제 1위 범위 | `entry.py:61-74` |
| RG6 · RG8(`via=RG6` · `read_as` 표지) · 겹침은 범위 규칙 먼저 · Z-1 | 맞음 | `entry.py:97-150` |
| RG7 범위마다 폭 · 같은 조회 한 번 · `verified.range` | 대체로 맞음 — 두 범위가 같은 조회를 내면 첫 범위 이름만 붙는다(N-5) | `breadth.py:63-64` · `verified.py:92-95` |
| 입구 고르기 ①-4(후보 0 일 때만 · 범위 입구 끝까지 · 개념 묶음 · 32 묶음 · confirmed / ask_back / none) | 맞음 | `entry.py:130-219` |
| BR1 ~ BR4 · B 와 키가 같은 함수 | 맞음(`calls.py` `breadth_calls` 를 `key_calls.py:105` 가 그대로 씀). 예외 = 상품 이름 길(W-3) | — |
| FT1 ~ FT4 | 맞음 — 묶음 키 · 같은 값만 머리 · gid 전부 · 표지 칸 · 쪽 나눔(묶음 경계 → 행 경계) | `fold.py` |
| FT5 「못 실으면 실행 중단」 | **어긋남 — W-4** | `col_b.py:121-128` |
| K1 ~ K5 | K1 · K2 · K3 · K4 있음. K3 의 G7 이 속성 입구를 「안 읽음」 으로 잡아 정상 질문을 중단시킴(W-2). K5 는 구조상 늘 통과(N-6) | `gate.py` |
| 종료 상태 6 · (가) · (나) · (다) 1회차 미판정 | 맞음(승인된 꼴) | `end_state.py` |
| 세 상태(범위 밖 · 입구 없음 · 실행 중단)에도 단계 ⑤ · 빈 verified · `b_on` 안 돌림 | 맞음 | `col_b.py:96-97 · 171-193` · `test_stage5_called_for_three_states_without_rows` |
| 세 열 같은 조건 | 맞음 — 질문 문자열 같음(A · C 는 질문만 · B 는 앱 판정 + 자료 + 같은 질문) · 같은 `ANSWER_MODEL` · 같은 타임아웃 · 같은 격리 인자 · 공통 지시 `common.md` 글자 그대로 + 열별 「자료를 얻는 법」 한 단락(`base.py:38-39`) · A · C · B 켬 = `--effort <batch effort>` · B 본 꼴만 가장 낮은 effort | `cli.py:76-92` · `col_a.py:39` · `col_c.py:43` · `col_b.py:175 · 190` |
| D1 ~ D9 | D1 · D2 · D3(①②) · D5 · D6(B 전용) · D7(A 「해당 없음」) 맞음. **D4 가 A 인용의 배열 번호를 숫자로 셈(W-5)** · D8 표별 판정이 SPEC 보다 좁음(N-7) · D9 의 「질문이 이름 댄 케이스 빼기」 미배선(N-8) | `checks.py` |
| 가리기(열 이름 · 도구 흔적 · 속도 · 다른 열 · B end_state 없음 · 인용 중립 표지 · 순서 섞기 · 실패 근거 필수) | 맞음 | `judge.py:41-90` · `grade.py:112-138` |
| 미확인 키 채점 금지 | 맞음 — 없음 · `synthetic` · 미확인 · build 다름 전부 거부 · 푸는 플래그 · env 없음 | `grade.py:39-50` · `test_key_rejection_no_unlock` |
| 합성 키 배관 | 맞음 — 세트 · runs · CSV 안 읽음 · 결과 `runs/plumbing/` 만 · 머리 표지 | `grade.py:143-194` |
| §10 보고서 꼴 | **대부분 빠짐 — W-6** | `report.py:37-93` |

## 4. 구현 보고 미결 ①~⑤ 판정

| # | 판정 | 까닭 · 고칠 방향 |
|---|---|---|
| ① 추론 끔 불가 → `--effort low` 기본 | **SPEC · 결정과 맞음**(SPEC-002 §6-1 「끌 수 없으면 가장 낮은 effort」 · O-23 (b) · `_RESUME` 11-16 「흐름」). 기록 `settings.answer_reasoning = lowest_effort` · 쪽마다 `thinking_seen` · 보고서 머리에 `answer_reasoning` 이 찍힌다(`report.py:49`) | 알아 둘 것: 1회차 「끔 / 켬」 비교는 실제로는 **low ↔ medium effort** 비교다 — 보고서 머리 문구로 밝히는 것(§10 끝 단락)이 지금은 값 하나(`lowest_effort`)뿐이다(W-6 과 함께 문장으로). `off` 꼴(낮은 effort + 끔 설정 둘)은 `lowest_effort` 의 상위 꼴이라 원하면 그쪽으로 돌려도 기록이 거짓이 되지 않는다 — 사용자 선택 |
| ② Q10 「상태 안 맞음」 | **SPEC 구멍**(구현 문제 아님). SPEC-002 §5 (가) 는 부위·고민의 「행 0」 을 `concern_candidates` + `facets` package **전부 0** 으로 적고 Q10 을 (가) 의 예로 든다. 그런데 SPEC-002 §3-2 끝 불릿이 「앱은 `hier` 기본값(`expand`)으로 부른다」 고 하고, SPEC-001 §4-4 「계층 펼침」 표는 package 값 쪽을 「그 고민 + **상위 고민 전부**」 로 넓힌다. 실물에서 Q10 키의 18 행이 **전부 `hier_match = 상위`**(로컬 키 파일 확인) — 두 절이 같이 서지 않는다. 구현이 문항별 예외를 넣지 않은 것은 맞다 | B 는 지금 Q10 을 「후보 소진」 으로 끝낸다(required `g_indication` 이 비어서). SPEC 에 한 줄 정하면 된다 — 추천: (가) 의 「행 0」 은 **`hier.match` 가 `상위` 인 행을 세지 않는다**(물은 코드 자신의 행이 0). 고칠 자리는 `end_state.py:24-31` 과 `answer_key.py:127-131` **둘 다 같은 식으로**(지금 두 곳이 따로 셈 — 공유 함수로 두면 B ↔ 키가 갈라지지 않는다). 상위 고민 패키지 행은 폭에 그대로 둔다(층 표시 `hier.match` 와 함께 — 빼면 원칙 위반) |
| ③ Q25 표본 3/6 | **SPEC 구멍(좁아지는 쪽)** — SPEC-002 §3-2 순서·간격 행이 갈래를 「순서 · 간격 · 재시술 간격」 으로 고정했고(BR1 (i)) 구현은 그것을 지켰다(`ranges.py:57` · `key_calls.py:101-103`). gold-build 표본의 빠진 3 은 전부 `g_pair` 행이다. BR3 은 「키가 표본보다 **넓어질** 수 있다」 만 예상했지 좁아지는 경우를 적지 않았다 | 추천: **좁은 쪽 유지 + SPEC 에 한 줄**(「범위 표의 고정 갈래가 gold-build 보다 좁으면 표본이 키에 안 들 수 있다 — 대조 요약에 올린다」). 회피 갈래를 순서·간격에 더하면 「묻지 않은 안전 정보를 붙이지 않는다」 결정과 부딪친다. 덧붙여 대조 요약의 꼬리표가 이 경우에도 「BR2 로 키가 표본보다 **넓어짐**」 으로 찍힌다(`answer_key.py:247-248`) — 사용자 확인 때 거꾸로 읽힌다(N-9) |
| ④ resolve 짧은 조각 빼기 · 패키지 이름 | **짧은 조각 빼기 = 폭을 줄인다 → F-1.** 패키지 이름 `raw_ledger/` = **맞음**(`.gitignore` 의 `raw/` 가 `clinic_chat/raw/` 를 통째로 무시하므로 이름을 바꾼 것이 공개 레포 규칙을 지키는 쪽 · WORK §2-3 이름은 O-11 「구현 때 정함」 제안) | F-1 참고 |
| ⑤ draft 32 문항 | **막는 길은 맞음** — `batch` 가 `status: draft` 를 건너뛰고(`batch.py`) `runner --set-id` 는 거부한다(`runner.py`). Jev · LLM 으로 안 간다 | 확정 뒤의 길이 없다 — draft → confirmed 로 바꾸는 명령이 없고(손으로 `set.jsonl` 고침), 37 밖 문항의 호출 명세를 만드는 진입점도 없다(`key_calls` 는 gold-build `QUESTIONS` 전용). N01 · N05 는 `resolve` 후보가 0 이 아니라 「이름 없음」 묶음 꼴이 아니다(보고대로 문장 고칠 것) → W-8 |

## 5. 지적 표

심각도: **FAIL** = 원칙 · 결정 위반 / **WARN** = SPEC 어긋남 · 잘못된 결과가 나는 결함 / **NOTE** = 작게 고칠 것 · 기록

| # | 파일:줄 | 심각도 | 근거 SPEC 절 | 무엇 · 재현 | 고칠 방향 |
|---|---|---|---|---|---|
| **F-1** | `clinic_chat/walk/entry.py:43-58`(56-57 줄) | **FAIL** | 원칙(폭 · 입구) · SPEC-002 §4 G7 「명시 대상을 빠뜨림」 · RG6 「불확실하면 버리지 않는다」 · SPEC 에 없는 동작 | 짧은 조각이 더 긴 조각의 **문자열 안에 들기만 하면** 그 조각의 개념을 전부 뺀다. 위치 · 낱말 경계를 보지 않는다(허브 `matched` 에 위치가 없다). 합성 재현: 후보 `AAA`(P1) · `BB AAA`(P2) → 결과 `{BB AAA: [P2]}` — 질문이 「AAA 와 BB AAA」 처럼 짧은 이름을 **따로도** 말했으면 P1 이 입구에서 사라진다. 낱말 경계 없음: `XY`(부위) · `XYZ`(고민 — 붙여 쓴 한 낱말) → `XY` 가 빠진다. 빠진 입구는 `entries` 에 없으니 G7 · K3 도 못 잡는다 · trace 에도 「뺐다」 가 안 남는다 | (a) 빼기를 없애고 두 조각을 다 입구로 둔다(폭을 넓히는 쪽 — RG6 과 같은 꼴) 또는 (b) 질문에서 짧은 조각이 나오는 **횟수**가 긴 조각들 안의 횟수와 같을 때만 빼고, 뺀 것을 `trace_entry.dropped_spans[]` 에 남긴다. 어느 쪽이든 SPEC-002 §3-1 에 한 줄(코디 결정). 시험: 「짧은 이름이 따로도 나온 질문」 · 「낱말 경계 아닌 포함」 두 꼴 |
| **W-1** | `clinic_chat/walk/ranges.py:61-66` · `calls.py:118-121` | WARN(**SPEC 충돌 · 결정 필요**) | `_RESUME` 11-16 「안전 정보를 처음부터 붙이지 않는다」 · SPEC-002 §3-2 「표의 어느 범위에도 묻지 않은 안전 facet 이 없다」 ↔ 같은 표 「속성 시작」 행 「맞춤 facet 전부(부위 7)」 · §4 K5 | 부위만 · 해부만 이름 댄 질문은 범위 Choice 가 무엇이든 `adverse` · `adverse_detail` · `contraindication` · `offer` 행을 폭으로 읽어 단계 ⑤ 에 넣는다. 키도 같은 함수라 키 `codes[]` 에 그 표 코드가 들어가 **D8 「묻지 않은 것」 에도 안 잡힌다**(측정에서 보이지 않는다). K5 는 `range = attr_start` 라 통과 | 추천: 속성 시작의 facet 을 **고른 범위(단계 ①-3)가 허용하는 facet 과의 교집합**으로 — 예: 범위가 부작용이면 adverse · adverse_detail, 회피면 contraindication, 상품이면 offer, 그 밖은 profile · indication · outcome. 「질문에 그 범위가 있으면 그 폭으로 빠짐없이」 는 그대로 선다. SPEC-002 §3-2 · WORK 3-a 의 「부위 7 · 해부 2」 를 고치는 결정이 먼저(코디 · 사용자) |
| **W-2** | `clinic_chat/walk/gate.py:21-29 · 63-64` | WARN | SPEC-002 §3-2 「속성 시작 — 대상 · 값 입구가 함께 풀렸으면 속성은 필터로 곁들인다(BR1 — 부위는 `site`)」 · §4 G7 · §5 실행 중단 | 대상 입구 + 재료 · 방법 · 해부 입구가 함께 풀린 질문: BR1 에 재료 · 방법 · 해부 필터가 없어 그 입구를 어느 조회도 참조하지 않는데, G7 검사는 속성 4표를 늘 「시작 표」 로 보고 「참조 안 됨」 → **K3 실패 → 실행 중단**. 합성 재현: `[procedure:P1, material:M1]` · 범위 시술 → `g7_missing = ['material:M1']`. 흔한 꼴(재료 이름 + 계열 이름)이라 정상 질문이 중단된다 | G7 대상에서 「BR1 이 필터를 두지 않는 속성 입구(material · method · anatomy)가 대상 입구와 함께 있을 때」 를 빼고 trace 에 `unused_entries[]` 로 남긴다(지어 붙이지 않음). 또는 SPEC 에서 그 속성의 필터 길을 정한다. 시험 한 꼴 |
| **W-3** | `clinic_chat/walk/calls.py:180-187` | WARN | SPEC-002 §3-2 상품 행 「상품 이름으로만 풀리면 `offer_name_contains`」 · BR3(B 와 키가 같은 입력) · §8-2 D7 「B 기대값 0」 | `offer_name` 입구는 키 명세(`key_calls.py:98-99`)만 만든다 — B 의 단계 ① 은 이 입구를 만드는 길이 없다. Q33(키 = `offer_name_contains` 한 호출 · 기대 (나))을 B 는 다른 입구 · 다른 조회로 걷게 되어 D7 ≠ 0 · (나) 판정이 어긋날 수 있다 | B 에 길을 둔다: 범위가 상품이고 대상 · offer 입구가 없을 때(또는 `resolve` 0 일 때 ①-4 앞에) 질문의 조각으로 `offer_name_contains` 를 부르는 규칙 — 어느 조각을 쓸지는 SPEC 에 없으니 코디 결정. 1회차 전 Q33 한 번으로 D7 확인 |
| **W-4** | `clinic_chat/columns/col_b.py:121-128 · 175-187` | WARN | SPEC-002 §3-6 FT5 · §5 실행 중단 · WORK-002 §5 「세 상태에도 단계 ⑤」 | 묶음 하나의 행 하나가 `ANSWER_INPUT_MAX_TOKENS` 보다 크면 `FoldTooLarge` → 답 빈 값 + `error` 인데 **`end_state` 는 걷기 결과(예: 근거 충족) 그대로**이고 단계 ⑤ 를 안 부른다. 기록이 「근거 충족 · 답 없음」 으로 남는다 | `FoldTooLarge` 면 `w.end_state = 실행 중단` · 사유 `FT5` · `groups = []` 로 바꾸고 빈 verified 로 단계 ⑤ 를 부른다(다른 세 상태와 같은 길). 시험 한 꼴 |
| **W-5** | `clinic_chat/quality/checks.py:14 · 94-95` | WARN | SPEC-002 §8-2 D4 · §2-2 「같은 검사기 · 열 사이 편향 없음」 | 숫자 뽑기가 gid · 코드만 가리고 **A 의 원장 인용 `[파일.키[0].칸]` 의 배열 번호**를 답 숫자로 센다. 합성 재현: A 답 `… [x.items[0].note] [x.items[12].x]` → `violations ['0','12']` · 같은 내용의 C 답 → `[]`. 목록 번호(`1.` · `2.`)도 세 열 모두 위반으로 센다 | D4 전에 인용 꼴 전체(`RAW_CITE_RE` · `[gid]` · `[근거 n]`)를 지우고, 줄 머리 목록 번호(`^\s*\d+[.)]`)를 뺀다. 시험에 A 인용 꼴 한 줄 |
| **W-6** | `clinic_chat/report.py:37-93` | WARN | SPEC-002 §10 · WORK-002 7-g | 있는 것: 머리 · ② 통과 수 · D1 · D2 · D4 · D5 · D3 지어낸 · D7 빠진 행 · D8 문항 수 · RG3/RG6 · 원장 오류 따라감 · total_ms · 오류 수. **없는 것**: 점수 두 벌(전체 / 원장 = silver — §8-5) · D3 빠진 코드 비율 · D7 비율 · `missed_must_rows` · M1 빠진 수 · D9 · **종료 상태 일치 수(`graded_end_state`)** · ttft · 호출 수 · 토큰 · 범위별 표 · 상태별 표 · **B 전용**(D6 · 범위 Choice 정답 · RG 분포 · 입구 고르기 · 깊이 결정 분포 · `complete` 수 · K1~K5 실패 · `llm_pages` > 1) · 끔/켬 비교 표(지금은 열 하나). 머리의 judge model 은 runs 줄에서 읽어 늘 `None`(실제 id 는 `quality.jsonl` 에 있음) | 1회차 batch 전에 §10 표를 다 채운다(데이터는 runs · quality 에 이미 다 있다 — 표만 없음). judge id 는 quality 줄에서. 「추론 끔 불가 → 가장 낮은 effort」 문장을 머리에 |
| **W-7** | `clinic_chat/walk/calls.py:74-78` · `entry.py:155-156` · `gate.py:63-64` | WARN | SPEC-002 §4 G7 · llms.txt §4 「명시 대상을 낮은 점수만으로 삭제하지 않는다」 · 원칙 | 입구의 표가 읽기로 한 범위의 시작 표에 없으면(예: 범위 Choice 가 확실하게 고른 범위와 다른 표의 입구) 그 입구는 **어느 조회에도 안 쓰이고** G7 검사 대상에서도 빠진다 — 범위 Choice(Jev 확률)가 명시 대상을 조용히 떨어뜨리는 길. trace 에 「안 쓴 입구」 가 없다 | 최소: `trace_entry.unused[]`(입구 · 까닭)를 남기고 보고서 B 전용 표에 수를 낸다. 더 나아가 「안 쓴 입구가 있으면 그 입구의 표를 시작 표로 가진 범위를 더한다」(RG3 · RG8 과 같은 「넓히기만」 꼴) — SPEC 결정 |
| **W-8** | `clinic_chat/evalset/loader.py` · `key_calls.py` · `README.md` | WARN | SPEC-002 §9-4 · WORK-002 C-2 | draft 32 문항을 확정한 뒤 할 일(① `status` 바꾸기 ② 37 밖 문항의 호출 명세 만들기 ③ 키 뽑기 · 확인)의 명령이 없다. `key_calls` 는 gold-build `QUESTIONS` 만 읽는다 | 세트 확정 명령(`loader --confirm <ids> --by`)과 세트 파일의 `entries` · `range` 로 명세를 쓰는 진입점(같은 `breadth_calls`)을 더하고 README 에 순서를 적는다 |
| N-1 | `clinic_chat/walk/depth.py:89` · `verified.py:109-118` | NOTE | SPEC-002 §3-6 「Jev state 가 64k · 32k 를 넘으면 대상별 한 줄로 더 접는다」 | 더 접는 길이 없다 — 큰 폭(역방향 최대 525 후보)에서 Jev 한도 초과 → `JevError` → 실행 중단 | 요청 전에 state 크기를 어림해 넘으면 대상별 한 줄로 접기 |
| N-2 | `clinic_chat/quality/grade.py:39-50` | NOTE | SPEC-002 §9-5 확인 절차 5 | 키 거부 조건이 build 만 본다 — `script_sha256` · `calls_sha256` 이 지금 파일과 달라도(명세를 고치고 다시 안 뽑음) 확인된 옛 키로 채점된다 | 지금 스크립트 · 명세 해시와 대조해 다르면 거부 |
| N-3 | `clinic_chat/evalset/answer_key.py:194-200 · 286-295` · `grade.py:120` | NOTE | SPEC-002 §7-1 `answer_key.sha256` · §9-5 ⑤ | `--confirm` 이 키 파일을 다시 써 sha 가 바뀐다 → 「batch → 확인 → 채점」 순서면 runs 줄의 sha(확인 전 파일)와 채점에 쓴 키의 sha 가 다르고, quality 줄은 runs 줄의 sha 를 옮겨 적는다 | sha 를 `confirmed` 를 뺀 내용으로 셈하거나, 채점 때 쓴 키의 sha 를 quality 줄에 따로 남긴다 |
| N-4 | `clinic_chat/walk/end_state.py:24-31` | NOTE | SPEC-002 §5 (가) 「그 범위의 폭 조회 전체에서」 · RG7 | 두 범위를 읽을 때 (가) 를 범위마다가 아니라 전부 합쳐 본다 — SPEC 글이 범위 단위인지 질문 단위인지 열려 있음 | ② 결정 때 함께 한 줄로 |
| N-5 | `clinic_chat/walk/breadth.py:63-64` · `verified.py:92-95` | NOTE | SPEC-002 §3-1 RG7 「`verified` 행에는 어느 범위의 폭인지」 | 같은 조회가 두 범위에서 나오면 첫 범위 이름만 붙는다 — required 셈(`depth.py:51`)이 둘째 범위에서 「missing」 으로 볼 수 있다 | `VRow.range` 를 집합으로 |
| N-6 | `clinic_chat/walk/gate.py:93-96` | NOTE | SPEC-002 §4 K5 | `verified.range` 가 늘 호출의 범위라 K5 는 구조상 실패하지 않는다(W-1 같은 경우도 통과) | K5 를 「행의 표 ∈ 그 범위가 허용한 표」 로 보면 W-1 을 코드가 스스로 잡는다 |
| N-7 | `clinic_chat/quality/checks.py:132` | NOTE | SPEC-002 §8-2 D8 「키 `codes[]` 에 **그 표의** 코드가 하나도 없는 문항에서」 | adverse 코드는 키에 adverse **또는** condition 이 있으면 안 셈 — 회피 문항 답이 묻지 않은 부작용을 늘어놓아도 안 잡힌다 | 표마다 따로 |
| N-8 | `clinic_chat/quality/checks.py:49 · 145` · `grade.py:125-127` | NOTE | SPEC-002 §8-2 D9 「질문이 케이스를 이름 댄 문항은 뺀다」 | `named_cases` 인자를 채점이 넘기지 않는다 | 세트 항목의 입구(케이스)를 넘긴다 |
| N-9 | `clinic_chat/evalset/answer_key.py:247-248` | NOTE | SPEC-002 §9-5 확인 절차 2 | 좁힘을 옮기지 않은 문항에 늘 「키가 표본보다 넓어짐」 꼬리표 — Q25 처럼 범위 표 갈래가 더 좁은 경우도 같은 말 | `classes` 차이는 「범위 표 갈래와 다름(좁/넓)」 으로 따로 |
| N-10 | `clinic_chat/runner.py:128` · `batch.py:132` | NOTE | — | `--columns` 의 모르는 이름(`A` · `b_on` · 오타)을 말없이 버린다 — 빈 목록이면 열 없이 한 줄을 쓴다 | 모르는 이름이면 오류로 멈춤 |

## 6. 사용자가 e2e 에서 만날 자리

README 「실행 안내(e2e)」 표의 명령 13 줄은 전부 실제 진입점 · 인자와 맞는다(`runner` · `batch` · `quality.grade` · `evalset.key_calls` · `evalset.answer_key` · `prompts` · `report` · `runs` 의 `argparse` 대조). 결과 자리(`runs/runs.jsonl` · `runs/quality.jsonl` · `runs/reports/<batch_id>.md` · `runs/plumbing/` · `data/eval-set/key-summary.md`)도 맞다. 헷갈릴 자리:

1. **답 글이 터미널에 안 나온다** — `runner` 요약 줄은 종료 · ms · 호출 수 · 답 글자 수뿐이다. 답을 보려면 `--show-answers`(README 에 없음) 또는 `runs --show <run_id>`(요약 줄에 찍힌 `run_id`).
2. **A · C · B 켬 줄의 `end=None`** — SPEC 상 앱 판정은 B 만 하므로 정상이다(오류 아님). README 에 한 줄 필요.
3. **Q10 의 `expected_end_state=상태 안 맞음`** — 종료 상태 6 에 없는 값이 기대값으로 찍힌다(§4 ②). B 는 「후보 소진」 으로 끝난다. Q12 는 기대 「원천 미확정」 인데 B 는 「근거 충족」(승인된 1회차 꼴) · Q25 는 표본 3/6.
4. **채점이 「rejected」 만 낸다** — 답 키 37 이 전부 미확인이라 `quality.grade --batch` 는 첫 판에 `graded 0` 이다. 순서: `key-summary.md` 의 걸린 17 확인 → `answer_key --confirm Q01,Q02,… --by <이름>`(쉼표 · 공백 없음) → `grade`. 확인하면 키 파일 sha 가 바뀐다(N-3).
5. **「프롬프트 미확정(사용자 확인 전)」** 이 runner · batch · 보고서에 계속 찍힌다 — `prompts --confirm --by` 뒤 사라진다. 프롬프트 한 글자만 고쳐도 다시 뜬다.
6. **보고서가 SPEC §10 보다 얇다**(W-6) — 상태별 · 범위별 · B 전용 · 두 벌 점수를 보려면 지금은 `runs --show <id> --column b --trace` 로 줄마다 봐야 한다.
7. **B 「실행 중단」 의 까닭** — 터미널엔 `error=있음` 만. 까닭은 `runs --show <id> --column b --trace` 의 `end_reason`(`gate:K3` · `hub_breadth` · `C3` …). W-2 꼴(대상 + 재료 이름 질문)은 `gate:K3` 로 나온다.
8. **draft 32** — `--set-id N01` 은 거부되고 batch 는 「draft 건너뜀 32」 를 찍는다. 확정하는 명령이 없다(W-8).
9. **`--b-on` 은 기본이 켬** — 끄려면 `--no-b-on`. 전체 세트는 문항 × CLI 4 회(A · B · B 켬 · C) + 채점 문항 × 4 회(Opus)라 길다 — README 대로 `--ids` 몇 개부터.

## 7. 검증(직접 한 것)

| 명령 | 결과 |
|---|---|
| `uv sync` | Resolved 46 · Audited 42 |
| `uv run ruff check .` | All checks passed! |
| `uv run pytest -q`(`TYPESAFE_API_KEY` · `ANTHROPIC_API_KEY` env 지움 · 시험은 `.env` 안 읽음 · CLI bin 막음 — `conftest.py:14-32`) | **85 passed in 3.39s** |
| 합성 재현(scratchpad · 레포 파일 안 씀 · 실호출 없음) | F-1 · W-2 · W-5 위 표의 값 그대로 |
| 로컬 키 · 명세 파일 읽기(값 안 옮김) | Q10 키 18 행 전부 `hier_match = 상위` · Q25 표본 6 중 3 이 키 밖(전부 `g_pair`) · Q33 명세 = `offer_name_contains` 한 호출 · Q12 `asked_fields` 2 |

허브 18105 는 부르지 않았다(GET 도 안 함). Jev · claude 실호출 0.

## 8. 다음(코디)

1. F-1 고침(작음) — 방향 (a) 또는 (b) 고르기.
2. 결정 셋: W-1(속성 시작 facet ↔ 안전 결정) · Q10 (가) 의 `hier = 상위` 행 · Q25 좁아지는 키 — SPEC-002 §3-2 · §5 · BR3 에 한 줄씩.
3. W-2 ~ W-6 은 1회차 batch 전에 고칠 것(W-3 은 상품 이름 조각을 고르는 규칙이 SPEC 에 없어 결정 하나 필요) · W-7 · W-8 · NOTE 는 같은 판에 함께 또는 1회차 trace 뒤.
