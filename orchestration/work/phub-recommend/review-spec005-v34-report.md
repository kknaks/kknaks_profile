# 검수 보고서 — SPEC-005 v3.4(0.3.5) · WORK-010

작성 2026-11-01 · 검수자 reviewer 워커(읽기 전용 · 대상 문서 수정 없음) · 대조 = `SPEC-005.v3.3.md`(바뀐 줄 전부 diff) · `step9-explanations.json`(sha `5d394f87dca53602`) · `step9-decisions.json` · `step9-effect.json` · `semantic.json`(`6c43231e82939a44`) · 골드 export b031371c · 허브 **2ca8094**(깨끗) · 앱 1218d7f · SPEC-006 0.3.5

## 판정 — **FAIL 1** · WARN 5

숫자는 실물과 전부 맞는다. 결정표(D-13b) · 스키마(alembic 없음)도 성립한다. FAIL 은 하나다. G20 이 합병증 관리 · 예방 54 fact 를 `safety.complications` 에서 빼내는데, case3 의 I-04 고정 섹션(SPEC-006 §3-4-1-1 · 앱 `config.py:80`)은 `safety.side_effects` · `safety.complications` 만 받는다. 그래서 v3.4 빌드에서 case3 I-04 가 지금 받던 관리 · 예방을 잃는다. 005 · 010 은 이것을 「006 몫(더할지)」 으로만 적었고, 영향을 재는 끝 조건이 없다.

| 기준 | 판정 | 요지 |
|---|---|---|
| 1 실버 9단계 숫자 | PASS(W-2 · W-3) | 아래 표 전부 재셈 일치 |
| 2 D9-3 ② = resolved 하나 + alternatives id 메타 = D-13b | PASS(W-2) | ② 196 칸 전부 `resolved` 있음 · alternatives 레코드가 emit 에 든 것 0 · alternatives 343 전부 정본 노드 쪽 |
| 3 허브 코드 실물 · alembic 없이 | PASS | 아래 §2 |
| 4 SPEC-006 §3-4-1-1 와 I-04 영향 | **FAIL(F-1)** | |
| 5 WORK-010 순서 · grep · 끝 조건 | PASS(W-4 · W-5) | grep 8줄 재실행 36 파일 = 표 안 27 + v1 그래프 9(「영향 없음」 행의 glob · `tests/graph_support.py` · `app/modules/graph/validation.py` 는 이름이 glob 밖) · 끝 조건 (a)~(j) 는 모두 잴 수 있음 |
| 6 추측 자리(V-19~21 밖) | PASS | 없음(W-2 의 「숫자」 정의만 비어 있음) |

## 1. 숫자 재셈(기준 1)

| SPEC | 재셈 | |
|---|---|---|
| semantic inputs 12 · 실물 sha 12/12 같음 · step9 sha 5d394f87 · semantic sha 6c43231e | 같음 | ○ |
| node_slots 2,946 · emit 5,312 · alternatives 343 · records 5,847 · section_map 435 · 값 사전 8 · open 0 · human_check 0 | 같음 | ○ |
| 9단계 fact **5,273**(overview 3,735 · recovery 902 · method 634 · disclosure 2) · 안 실음 **39**(overview 27 · recovery 8 · method 4 · 노드 4 = M1-P-10 · auto-M16-1775363074847 · auto-M3-1775364775145 · auto-M9-1775361909628) | b031371c export 노드(1,071)에 있는지로 셈 · 같음 · 매핑이 필요한 노드는 0(꼴이 같음) · fact id 유일 · 최대 133자 | ○ |
| CX 이동 54(management 27 · prevention 27) — 지금 export section = `safety.complications` 54 | 같음 | ○ |
| SE 새 fact 205 = safety.management 75(management 38 · prevention 37) + safety.side_effects 130(incidence · mechanism · onset 각 38 · risk_factors 13 · duration 3) | section_map 기준 같음(W-3) | ○ |
| section_map 435 = 합병증 230(complications 176 + management 54) + SE 205 | 같음 | ○ |
| 새 fact 합 5,486 = 5,273 + 205 + 8 · safety.management 129 | 같음 | ○ |
| 값 사전 8(reaction_levels 4 → timeline · severity_levels 4 → safety.complications) · 지금 export globals 에 value_dictionary 없음 · `scope:all#…#value_dictionary` fact 0 | 같음 | ○ |
| A 닫힘 2차 **51/54**(39 · 11 · 1 · alternatives 2 · 안 닫힘 1) · v5a **25/30**(19 · 6 · alternatives 1 · 안 닫힘 4) | `step9-effect.json` tally 같음 · 「9단계로 닫힘」 행 중 비활성 제품 4 노드에만 기대는 행 0(골드가 안 싣는 39 fact 와 무관) | ○ |

## 2. 허브 코드(2ca8094 · 기준 3)

- `gold_fact`: id `String(400)`(9단계 최대 133) · section `String(32)`(`safety.management` 17자) · `source` JSON(jsonb) · `attached_to` jsonb. 메타를 `source.meta` 에 싣는 길은 이미 있다(export 의 기존 fact `source.meta{attached_by, …}`) → **alembic 없이 된다**
- `gold_global(id String(120), kind String(48), payload JSON)` → kind `value_dictionary` 행 추가에 스키마 변경이 필요 없다
- section 상수는 `facts.py:15 SECTIONS`(17) 하나 · `tools.py:46 INTENT_SECTIONS` · `:79 UNIT_LEVEL_SECTIONS` · `:31 CARD_SECTIONS` — WORK-010 Scope 의 facts.py · tools.py 행이 덮는다. `safety.management` 를 `UNIT_LEVEL_SECTIONS` 에 넣을지는 SPEC 에 없다(SE 는 계열 owner · 단위 펼침 G9 길 — 지금 `safety.complications` 와 같은 대우면 넣지 않음 · 그 뜻을 한 줄로 적으면 좋다)

## 3. FAIL

### F-1 · G20 의 CX section 이동이 case3 I-04 고정 섹션에서 관리 · 예방을 빼낸다 — §5-16 끝 문장 · §6-8 · WORK-010 비목표/Open Issues(기준 4)

근거:
- G20: `CX-…#management` · `#prevention` 54 fact 의 section `safety.complications` → `safety.management`(id 그대로). 지금 export 에서 이 54 는 `safety.complications` 에 있다(재셈)
- SPEC-006 0.3.5 §3-4-1-1 규칙 3: 「I-04 safety.side_effects · safety.complications — 첫 걸음에 고정으로 받음」. 앱 1218d7f `clinic_chat/config.py:80` `I-04:safety.side_effects+safety.complications` 도 같다
- 결과: v3.4 를 발행하면 앱이 바뀌지 않아도 case3 I-04 고정 섹션이 관리 · 예방 54 를 더는 받지 않는다. 새로 생기는 SE 관리 · 예방 75 도 받지 않는다. 이 둘이 v3.4 가 I-04 에 더하려는 바로 그 몫이다(§8 Q189 c3 · 2차 A 11 · v5a A 6 중 case3 몫). case2 는 I-04 묶음에 `safety.management` 가 들어가므로 닿는다. 하지만 case3 는 v3.3 보다 오히려 줄어든다
- 005 §5-16 은 「006 에 더할지는 006 몫」, WORK-010 은 「코디(006)」 로만 적었다. §6-8 (h) walk3 재생은 옛 Jev 선택을 다시 돌릴 뿐 §3-4-1-1 고정 섹션을 재지 않는다. 그래서 이 회귀를 잡는 끝 조건이 없다

방향(하나를 고른다 · 결정은 코디 · 사용자):
- **(가)** 006 §3-4-1-1 I-04 고정 섹션에 `safety.management` 를 더하는 개정을 WORK-010 발행 전에 짝으로 건다. 005 §5-16 · WORK-010 순서 표에 「발행 → 006 개정 · 앱 config 같이」 를 의존으로 적는다
- **(나)** 005 에 「v3.4 발행 뒤 case3 I-04 고정 섹션이 받는 fact 수 ≥ v3.3」 을 §6-8 끝 조건 한 행으로 넣는다. 재는 법은 rerun-v5a 의 I-04 판 시작 노드 × `expand(sections=[side_effects, complications(, management)])` 의 줄 수 비교다
- 어느 쪽이든 「006 몫」 한 줄을 「v3.4 가 006 I-04 를 바꾸는 영향(54 이동 · 75 새로)」 으로 고쳐 적는다

## 4. WARN

| # | 곳 | 무엇 | 방향 |
|---|---|---|---|
| W-1 | 머리 「바뀐 조항」 | 「§2-1(입력 12 · 해시 가드 12)」 인데 본문은 「입력 = 13 파일(semantic + 12)」 이고 WORK-010 도 13 이다 | 머리를 13 으로 |
| W-2 | G22 가드 「② fact 마다 **숫자 있는** emit 이 정확히 1」 | 「숫자」 정의가 없다. `\d` 로 세면 5 칸이 0 이 된다(`product:M9-1-8` · `unit_procedure:U5-022` · `U5-097` · `U5-098` · `U5-122` mechanism — resolved 원문에 숫자 없음). 9단계는 `step9-decisions conflict_resolution`(numeric_regex · zero_words · range · 시간 단위)의 `numset` 으로 정했다. 시험이 `\d` 로 짜이면 실물에서 깨진다 | 가드를 「resolved ∈ emit · alternatives ∩ emit = ∅ · emit ∖ {resolved} 는 step9 `numset` 빈 것」 으로(9단계 정의를 그대로 씀) |
| W-3 | G20 SE 원문 = `step8 safety.side_effects[].{field}` | step8 의 비지 않은 prevention 은 38 인데 section_map 은 37 이다. SE-M16-06 의 값 `"-"` 를 9단계가 뺐다. step8 칸으로 만들면 206, 가드(section_map)는 205 가 된다 | 「section_map 행마다 하나 · 값은 step8 칸(배열은 `[i]`)」 으로 행 기준을 명시 |
| W-4 | WORK-010 WP-4 4 · `$E/fail-triage-scripts/walk3.py:40` | walk3 에 section 17 이름 상수가 박혀 있다(676 이 닿은 쌍 셈에만 씀 · 옛 호출엔 management 가 없어 결과 영향 없음). WORK-010 은 walk3 를 「실행만」 이라 둔다 | (h) report 에 「walk3 SECTIONS 17 그대로 · 영향 없음」 한 줄 |
| W-5 | WORK-010 Scope 「영향 없음」 행 | glob(`tests/test_graph_*` · `scripts/graph_*`) 밖인 `tests/graph_support.py` · `app/modules/graph/validation.py` 가 grep 에 잡힌다(v1 그래프 · `read_dir` 다른 뜻) | 두 이름을 행에 더함 |
