---
type: work
id: WORK-006
title: "앱 0.5.1 구현 계획 — 맨 앞 판단(TG · KD · RG) · 대상 × 종류 읽기(RQ1) · 싣는 칸 · 줄 번호 · 답 프롬프트 · 열 정리 · 답 키 다시 뽑기"
status: draft
product: procedure-hub
feature: phub-gold-jev
version: 0.1.0
created_at: 2026-11-16
updated_at: 2026-11-16
tags:
  - product/procedure-hub
  - feature/phub-gold-jev
  - doc/work
  - status/draft
links:
  specs:
    - "orchestration/work/phub-gold-jev/SPEC-002-chat-eval.md (0.5.1 · 재검수 PASS — review-spec-v051.md) ← 계약"
    - "orchestration/work/phub-gold-jev/SPEC-001-hub-gold-mcp.md (0.5.1 — 허브 도구 계약)"
  decisions:
    - "orchestration/work/phub-gold-jev/_RESUME.md §2 (2026-11-16 「끝까지 진행」 · 「SPEC 0.5.0 검수 뒤 결정 3」 · 「LLM 에는 필요한 것만」 · 「길 찾기 재설계 진행」)"
  related:
    - "orchestration/work/phub-gold-jev/WORK-005-hub-v05.md (허브 쪽 — 나란히 돈다 · §4 가 coverage 응답 꼴)"
    - "orchestration/work/phub-gold-jev/kd8-jev-check-report.md (KD8 결과 — KD2 · KD3 본문 그대로 · instructions 에 이름 직접)"
    - "orchestration/work/phub-gold-jev/review-spec-v051.md (§7 NOTE 6)"
    - "orchestration/work/phub-gold-jev/WORK-002-app.md · WORK-003-web.md · WORK-004-speed-tab.md · app-report.md (0.4.1 구현)"
---

# WORK-006 — 앱 0.5.1 구현 계획(길 찾기 재설계의 앱 쪽)

> 경로 접두어: `P` = 프로필 워크트리 · `W` = `$P/orchestration/work/phub-gold-jev` · `SM` = 로컬 데이터 폴더(WORK-005 와 같음) · `APP-WT` = `~/orca/workspaces/clinic_chat/phub-gold-jev`(브랜치 `kknaksss/phub-gold-jev` · **0.4.1 구현 + 화면 + 속도 탭이 미커밋으로 올라가 있다 — 그 위에 이어서 고친다 · 새로 쓰지 않는다**).
> **계약은 SPEC-002 0.5.1 이다.** 이 문서는 「어느 파일을 · 어떤 순서로 · 무엇으로 확인하나」 만 정한다. SPEC 에 없는 동작 · 화면 문구를 만들지 않는다 — 어긋나는 것은 코드를 맞춰 고치지 말고 보고한다(§15).
> 하지 말 것 · 로컬 자리 · env · 검증 명령의 틀은 **WORK-002 §2 그대로**다(§2 에 바뀐 것만).
> **질문 문장 · 시술 이름은 이 문서에 없다.** 실물 확인 문항 다섯은 꼴과 코드로만 적고, 문장은 `$W/work-v05-instructions.md` 「쓸 것」 · 로컬 세트 파일에서 읽는다.

## 0. 요약

- B 의 순서를 뒤집는다: **맨 앞에서 Jev 가 대상 · 정보 종류를 판단**(단계 ① — 한 요청) → 허브는 고른 대상 × 종류만 끝까지 읽음(하위 층 자기 행 포함 · 단계 ②) → 깊이 · 검사는 유지 → LLM 에는 **행 전부 · 그 종류의 싣는 칸만**(줄 번호로 기록과 이음).
- WP 열: **WP-0** KD8 결과 고정 → **WP-1** 허브 클라이언트 · 모의 · C 도구 8 → **WP-2** 단계 ① 맨 앞 판단 → **WP-3** 단계 ② 읽기 · RQ1 · 종료 상태 → **WP-4** 답 재료(싣는 칸 · 줄 번호 · 표지 · gate) → **WP-5** 답 프롬프트 · 답 꼬리 → **WP-6** 열 정리 · 속도 탭 · 화면 · 기록 → **WP-7** 세트 · 답 키 다시 뽑기 → **WP-8** 채점 · 보고서 → **WP-9** 실물 확인 · 마감.
- WP-1 ~ WP-6 · WP-8 은 **모의 허브**로 돈다(WORK-005 §3 의 `matched` 꼴 · §4 의 `coverage` 꼴만 본다). 새 허브가 필요한 것은 WP-7 의 실물 뽑기와 WP-9 다.
- 사용자 확인 지점은 늘지 않는다: 답 프롬프트 문구(C-1 — 초안으로 구현 · e2e 보고 때) · 추가 문항(C-2 — 이번에 길 찾기 16 이 더해진다) · 답 키 37 확인.

## 1. 지금 코드(11-16 확인 — `APP-WT`)

| 파일 | 지금(0.4.1) | 이번에 |
|---|---|---|
| `clinic_chat/walk/entry.py`(265) | 단계 ① = resolve → 겹침 가르기 → 범위 Choice(`ask_range`) → RG1 ~ RG8 → entity Choice → 입구 고르기 · `matched.particle` 을 읽음(`:70`) | WP-2 — 입구 고르기(①-4)와 상품 이름 길만 남기고 나머지는 `walk/front.py` 로 대신한다 |
| `clinic_chat/walk/jev_requests.py`(103) | `ask_range` · `ask_entity`(Choice) · `ask_nouls`(32 묶음) | WP-2 — Choice 둘 삭제 · `ask_front`(한 요청) 더함 |
| `clinic_chat/walk/ranges.py`(118) | 범위 표 · role 상수(`ROLES_BASE` · `ROLES_ADVERSE` · `ROLES_PAIRLIKE` · `ROLES_PRODUCT_OFFER` = 자기 · 물려받음 · 하위 제품) · Choice 옵션 | WP-3 — role 을 §3-2 표로(하위 * 포함 · 제품 offer = 자기 · 하위 제품) · Choice 옵션 삭제 |
| `clinic_chat/walk/calls.py`(308) | `breadth_calls(range, entries)` — 범위의 폭 전부 · `key_calls` · `depth_candidates` · `depth_calls` | WP-3 — 조회 계획을 **대상 × 종류**로(`plan_calls`) · B 와 답 키가 같은 함수(BR3 그대로) |
| `clinic_chat/walk/depth.py`(169) | `required_status` = facet 단위 · 깊이 걷기 | WP-3 — required = 종류 단위 + RQ1 `met_by` · 시술 범위 깊이 없음 |
| `clinic_chat/walk/end_state.py`(93) | 여섯 상태 · (가) = 읽은 폭 전체 0 | WP-3 — RQ1 로 「근거 충족」 / 「후보 소진」 · (가) 판정용 조회 |
| `clinic_chat/walk/verified.py`(145) · `fold.py`(145) | 행 전 칸 · 묶음 표(`gid` 를 줄에 실음) | WP-4 — 싣는 칸만 · 줄 번호 `n` · `verified_lines[]` |
| `clinic_chat/walk/gate.py`(131) | K1 ~ K5 · G1 ~ G11 | WP-4 — K1 · K4 · K5 고침 · G12 |
| `clinic_chat/walk/select.py`(215) · `columns/col_b_slim.py`(66) | 속도 탭 「B 선별」 — 다 읽은 뒤 묶음 Noul | WP-6 — **없앤다**(새 B 가 선별이다 — O-26 ②) |
| `clinic_chat/columns/col_b.py`(221) | `walk` = ① → ② → ③ → ④ · `prompt_pages` · `answer` · `b_trace` | WP-2 ~ WP-6 — 흐름 · 재료 · trace 고침 |
| `clinic_chat/columns/col_c.py`(51) | `TOOLS7`(`health` 뺌) | WP-1 — 8(`coverage` 포함 — O-15 (a)) |
| `clinic_chat/clients/hub_rest.py`(275) | 도구 8 메서드 | WP-1 — `coverage()` |
| `clinic_chat/config.py`(96) | `range_confidence_at` · `range_ratio_at` | WP-2 — 둘 삭제 |
| `clinic_chat/prompts.py`(105) · `prompts/` | `JEV_FILES` = range · entity · entry · candidate · answer_ready · bundle / `common.md` · `col_a.md` · `col_b.md` · `col_c.md` · `judge.md` | WP-2 · WP-5 — Jev 파일 갈이 · 답 프롬프트 초안 |
| `clinic_chat/runner.py`(230) · `speed.py`(113) · `web/**` | 열 `a` · `b` · `c` · `b_slim` · 화면 기본에 B 켬 · 속도 탭 = `b_slim` · `c` · 고르면 `b` | WP-6 |
| `clinic_chat/evalset/*.py` | 세트 69 · 명세 = 범위 길 · 키 37(미확인 · 걸린 17) | WP-7 |
| `clinic_chat/quality/checks.py`(154) · `report.py`(323) | D1 ~ D9 · 「B 전용」 | WP-8 |
| `clinic_chat/experiments/kd8_kind_check.py` | KD8 확인 스크립트(다른 워커 것) | **손대지 않는다** — 문구만 가져다 쓴다(WP-0) |
| `tests/`(18 파일) | 기준선 **pytest 138 passed**(11-16 코디 검증 — C 측정 보정 뒤) | WP 마다 그 WP 의 시험 · 전체는 WP-9 에 한 번 |

## 2. 공통 — WORK-002 §2 에서 바뀐 것만

| 항목 | 이번 판 |
|---|---|
| allowed_paths | `clinic_chat/**`(새 `walk/front.py` · `walk/kinds.py` · `walk/required.py` · `walk/material.py` 포함 — 이름은 제안) · `prompts/**` · `tests/**` · `.env.example`(이름 빼고 더함) · `README.md`(실행 안내 절). `pyproject.toml` · `uv.lock` · `.gitignore` 는 안 고친다. gitignore 로컬 = `.env` · `data/**` · `runs/**` |
| 포트 | **18220(화면) · 18105(허브)는 코디 것** — 죽이거나 다시 띄우지 않는다. 화면 확인은 **18221**, 새 허브는 허브 워커 또는 코디가 띄운 **18106** 만 쓴다(`HUB_REST_URL` · `HUB_GOLD_MCP_URL` 을 그 실행의 프로세스 env 로 준다 — `.env` 를 고치지 않는다) |
| 외부 호출 | 단위 시험은 전부 모의(모의 Jev · 모의 CLI · 모의 허브). 실물은 WP-7 의 허브 호출(Jev · LLM 없음)과 WP-9 뿐 |
| 옛 기록 | `runs/runs.jsonl` 의 옛 줄은 고치지 않는다. 화면 「기록 다시 보기」 가 옛 줄(`front` 없음 · `b_slim` 있음)에서 깨지지 않아야 한다(WP-6) |
| 검증 | `uv run ruff check .` · `uv run pytest tests/test_<이 WP 것>.py -q` · 전체 `uv run pytest -q` 는 WP-9 에 한 번 |

**env 바뀜**(이름만 — `.env.example`): 뺌 `RANGE_CONFIDENCE_AT` · `RANGE_RATIO_AT` / 그대로 `JEV_NOUL_YES_AT`(0.7) · `JEV_NOUL_NO_AT`(0.3) · `JEV_BATCH_SIZE`(32) · `WALK_MAX_STEPS` · `ANSWER_INPUT_MAX_TOKENS`. 새 문턱 · 새 손잡이는 두지 않는다(대상 · 종류에 깊이용과 같은 문턱 — SPEC §3-4 · O-24 ①).

## 3. WP-0 — KD8 결과를 구현 지시로 고정(코드 없음 · 읽기)

**SPEC**: §3-1 KD8 · O-24 ④ ⑤. **결과**: `$W/kd8-jev-check-report.md`(11-16 · Jev 만 32 요청).

| KD8 이 낸 것 | 이 계획에서 |
|---|---|
| 「하나만」 5 문항 — 물은 종류 1위 · yes 5 / 5 · 「둘 함께」 9 / 10 · KD3 본문으로 기대 종류를 다 덮은 것 12 / 13 · 사이 상위 n 이 필요한 경우 0 | **KD2 · KD3 은 SPEC 본문 그대로 구현한다.** 「사이 값 가운데 위에서 n 개」 대안은 짓지 않는다(설정 손잡이도 두지 않는다) |
| 남은 실패 하나 — 색인만 쓴 instructions(`kinds_catalog[k]`)에서 목록 끝의 종류가 옆 종류 값을 따라감. **instructions 에 종류 이름을 직접 적으면** 고쳐짐(3 문항 · 한국어 판만 확인) | **`kind_{k}` 의 instructions 에 종류의 영어 이름(§3-2a)을 글자로 넣는다** — 꼴: ``Is the information kind "<name>" (`kinds_catalog[k]`) needed to answer `question`? …``(문구는 KD8 스크립트의 고친 판을 그대로 가져온다). SPEC §3-3 이 문구를 구현 때 정한다고 했으므로 SPEC 고침은 없다 |
| `target_{i}` · `entry_{i}` · `candidate_{i}` 도 색인만 쓰면 같은 밀림이 있을 수 있다(**미확인**) | 같은 꼴로 **후보의 이름(과 `표:코드`)을 instructions 에 함께 적는다**. 이름은 앱 · 허브가 gold 에서 낸 것 그대로다 — Jev 가 이름을 만드는 것이 아니다(llms.txt §3-1 그대로). **1회차 trace 로 다시 확인할 것**으로 §15 에 남긴다 |
| 한국어는 원인이 아니다(영어 풀이를 붙여도 같음 · 사이 값만 조금 늠) | state 의 `question` 은 한국어 그대로 · 영어 풀이를 붙이지 않는다 |
| 한계 — 실제 ①-2 요청은 `target_{i}` · `gap` 이 함께 들어 state 가 길다(그때의 밀림은 안 봄) | WP-9 의 실물 다섯에서 `front.kinds[]` · `front.targets[]` 의 값을 보고에 적는다 |

**완료 조건**: WP-2 의 instructions 조립 시험이 「질문 id 마다 그 대상의 이름이 instructions 글 안에 있다」 를 본다(종류 14 · 후보 · 입구 · 깊이 후보 넷 다).

## 4. WP-1 — 허브 클라이언트 · 모의 · C 도구 8

**SPEC**: SPEC-001 §4-1 · §4-9(응답 꼴) · SPEC-002 §2-4 · O-15 (a) · §3-1 CD1 ~ CD3.

| 고칠 것 | 어디 | 내용 |
|---|---|---|
| `coverage()` | `clients/hub_rest.py` | `coverage(nodes, kinds=None)` — 쪽 넘김 없음. 후보가 64 를 넘으면 **앱이 64 씩 나눠 부른다**(허브는 잘라 내지 않고 `invalid_argument` — SPEC-001 §4-9). `--ping`(E4)에 `coverage` 한 건을 더한다 |
| `matched` 새 꼴 | `walk/entry.py` · `evalset/key_calls.py:81` | `span` · `start` · `covered_by` 를 읽는다 · `particle` 을 읽는 줄(`entry.py:70`)을 없앤다. 상품 이름 길(`offer_name_phrases`)은 조각의 `start` 와 길이로 질문 안 자리를 잇는 식으로 바꾼다(뜻은 그대로 — 질문 글 그대로 · 낱말을 지어내지 않음). 키 명세의 「조각 전체 맞춤」 은 `span` = 이름의 `norm` 으로 본다 |
| 모의 허브 | `tests/fake_hub.py` · `tests/walk_fixture.py` | `coverage` 응답(WORK-005 §4 의 꼴 — `kinds[]` 는 `kind` 코드로 찾고 순서에 기대지 않는다) · `resolve` 의 `matched{span, start, covered_by}` · 「하위 *」 role 을 준 `facets` 가 `layer.role` = 그 role 행을 냄 |
| C 도구 | `columns/col_c.py` | `TOOLS7` → 8(`coverage` 더함 · `health` 는 그대로 뺌). 머리글 주석의 「도구 7」 고침 |

**완료 조건**: 모의로 `coverage` 를 64 넘는 후보에 불러 호출이 나뉘고 결과가 후보 순서대로 이어진다 · `particle` 낱말이 `clinic_chat/` 에 0 · C 의 허용 도구 이름 8.
**검증**: `uv run pytest tests/test_clients.py tests/test_columns.py tests/test_walk_entry.py -q`.

## 5. WP-2 — 단계 ① 맨 앞 판단(CD · TG · KD · RG · 입구 고르기)

**SPEC**: §3-1 흐름 ①-1 ~ ①-5 · CD1 ~ CD4 · TG1 ~ TG6 · KD1 ~ KD7 · RG1 ~ RG8 · 입구 고르기 표 · §3-2a(종류 표 · 기본 묶음) · §3-3(state · 질문 id) · §3-4(문턱) · §7-3 `entry` · `entry_pick` · `front`.

**파일**: 새 `walk/kinds.py`(정보 종류 14 의 고정 표 — 코드 · 영어 이름 · 대상의 표 → 범위 · 기본 묶음 · 읽는 조회 · 싣는 칸. SPEC-001 §5-8 과 같은 표다) · 새 `walk/front.py`(단계 ① 전체) · `walk/jev_requests.py` · `walk/entry.py`(입구 고르기만 남김) · `prompts/jev/front.md`(새 — `target` · `kind` · `gap` 세 문구 · 영어) · `prompts/jev/entry.md` · `candidate.md`(이름을 함께 적는 꼴로) · `prompts/jev/range.md` · `entity.md` · `bundle.md`(**삭제**) · `prompts.py` `JEV_FILES` · `config.py`.

| # | 구현 | SPEC |
|---|---|---|
| 1 | ①-1: 질문 문장 **그대로** `resolve` → 개념 (`entity_table`, `entity_code`) 하나 = 후보 하나(빼지 않는다) → 후보 전부를 `coverage` 에 | CD1 ~ CD3 |
| 2 | ①-2: **Jev 한 요청** = `target_{i}`(후보 수) + `kind_{k}`(14) + `gap`(1) · Choice 없음. state = `question` · `candidates[]{id, name, table, matched, rows}`(`rows` = `coverage` 의 종류별 `{self, lower, inherited}` 가운데 0 이 아닌 것) · `kinds_catalog[14]{code, name}` · `build`. 후보가 32 를 넘으면 둘째 요청부터 `target_{i}` 만. 후보 0 이면 `target` 없이 `kind` · `gap` 만(CD4) | §3-3 · WP-0 |
| 3 | ①-3 **KD 먼저**: yes(≥ 0.7) = 읽음(KD1) · 1위는 사이여도 읽음(KD2 — 전부 no 이하면 KD6) | KD1 · KD2 |
| 4 | ①-3 **TG**: 같은 `norm` 의 겹침은 KD 가 끌어낸 범위의 시작 표로 먼저 가른다(나머지 = `entry.overlaps[]`) · 시작 표에 든 개념이 0 이거나 둘 이상이면 안 갈린 것 — 덮이지 않은 조각은 전부 대상. 덮이지 않은 일치(`covered_by` = `null`)는 Noul 과 무관하게 대상(yes = `target` · 사이 = `uncertain_kept` · no 이하 = `named`) · 덮인 조각만 no 이하면 `front.dropped[]` · 사이면 둔다(TG2). 대상은 그 뒤 어떤 점수로도 안 빠진다(TG5) | TG1 ~ TG5 · RG6 |
| 5 | ①-3 **KD5 → KD3 → RG1**: 대상 개념의 표가 `condition` · `adverse` · `offer` · `package` · `concern` · `effect` 이면 그 종류를 더함(겹침이 다른 표로 갈린 낱말로는 안 더함 · TG2 개념이면 `via` = `TG2`) → 범위 = 읽기로 한 (대상의 표, 종류) 짝의 범위 합집합(결정론) → 그 범위의 기본 묶음을 합집합 · 기본 묶음 밖의 사이 종류 = `offered`(읽지 않음 · 종류 이름 + `coverage` 행 수를 답 재료 표지로) · no = `no`. 대상의 표에 없는 짝 = `skipped`(KD4) · 대상은 있는데 종류가 전부 no 이하이고 KD5 도 없으면 그 표의 기본 묶음만(`kinds_by` = `default` — KD6) · 묻지 않은 안전 종류는 기본 묶음에 없다(KD7 — 표가 그렇게 돼 있는지 시험이 본다) | KD3 ~ KD7 · RG1 ~ RG3 · RG7 · RG8 |
| 6 | `gap` ≥ yes → `scope_gap` 켬(사이는 기록만). 「범위 밖」 은 입구 0 일 때만 | RG4 · RG5 |
| 7 | TG6: 대상 입구와 함께 풀린 재료 · 방법 · 해부 입구 · 읽는 범위의 시작 표에 없는 입구 → `entry.unused[]`(까닭과 함께) | TG6 |
| 8 | ①-4 **입구 고르기는 후보 0 일 때만**(TG4): 범위 = 종류에서 끌어낸 것(대상이 없어 표를 못 정하면 그 종류가 속한 범위 전부) · 종류 전부 no 이하이면 `gap` yes → 「범위 밖」 / 아니면 가장 높은 종류의 범위 → `resolve` 목록 꼴 끝까지 → 개념마다 `entry_{i}` 32 묶음 → yes = 확정(`entry.by` = `noul` · 「질문의 말을 이 입구로 읽었다」 표지) / 사이만 = 「입구 없음」(되묻기 재료 = 그 후보의 이름 · 코드) / 전부 no = `gap` yes 면 「범위 밖」 · 아니면 「입구 없음」 | 입구 고르기 표 · §5 |
| 9 | ①-5 조회 계획 = 대상 × 읽기로 한 종류 → WP-3 의 `plan_calls` | BR1 ~ BR3 |
| 10 | 없애는 것: `ask_range` · `ask_entity` · `_pick_ranges` · `range_options` · `OUT_OF_SCOPE` Choice 옵션 · 설정 두 값 · trace `range_choice` | RG1 · §3-3 표의 지운 줄 |
| 11 | trace `front{coverage, targets[]{id, noul, decision, covered_by}, dropped[], kinds[]{code, noul, decision, by}, kinds_by, gap, scope_gap, ranges[], required[], 문턱, Jev 요청 수}` · `entry{resolve 후보 전부(조각 · 자리 · covered_by), 고른 것, by, overlaps[], unused[]}` · `entry_pick`(돌았을 때만) | §7-3 |

**완료 조건**(모의 Jev · 모의 허브 — 가짜 이름)
1. 후보가 있고 대상 Noul 이 **전부 no 이하**여도 입구 고르기가 돌지 않고 가장 긴 덮이지 않은 일치가 `named` 로 읽힌다(TG3 · TG4 — e2e 4 의 꼴).
2. 덮인 조각: no 이하 → `dropped`(읽지 않음 · 기록) / 사이 → 대상(`uncertain_kept` · 표지).
3. 짧은 이름과 긴 이름을 **둘 다 따로** 말한 질문 → 둘 다 대상.
4. 같은 `norm` 이 두 표에 있을 때: 시작 표로 갈리면 하나 + `overlaps[]` / 안 갈리면 둘 다.
5. 종류: yes 둘 → 둘 다 읽음 · 전부 사이 → 1위 + 기본 묶음 · 기본 묶음 밖 사이 = `offered` · 전부 no → 기본 묶음(`default`) · 안전 종류(`adverse` · `recovery` · `contraindication` · `avoid`)가 묻지 않은 질문의 읽는 종류에 **없다**.
6. 대상이 `condition` 개념이면 Jev 값과 무관하게 `contraindication` 이 읽힌다(KD5).
7. Jev 요청 수: 후보 ≤ 32 이고 후보 ≥ 1 인 질문에서 단계 ① 의 요청이 **1**.
8. `Choice` · `ask_range` · `ask_entity` · `range_confidence` 낱말이 `clinic_chat/` 에 0 · Jev 응답 문자열을 노드 id · 종류 코드로 쓰는 길이 없다(읽는 것은 `noul` 뿐).
9. WP-0 의 instructions 시험.

**검증**: `uv run pytest tests/test_walk_front.py tests/test_walk_entry.py tests/test_walk_ranges.py -q`(새 파일 이름은 제안).

## 6. WP-3 — 단계 ② 읽기 · RQ1 · 종료 상태

**SPEC**: §3-1 단계 ② · 「폭과 깊이」 표 · BR1 ~ BR4 · 지킬 것 표의 ② 행 · C1 ~ C3 · §3-2 표(role · 깊이 칸) · RQ1 네 줄 · §3-2a 「읽는 조회」 칸 · §3-5 · §5 표 · 세 조건 · 불릿.

| # | 구현 | 어디 | SPEC |
|---|---|---|---|
| 1 | `plan_calls(targets, kinds, …)` — (대상의 표, 종류)마다 §3-2a 「읽는 조회」 의 호출을 낸다. 「폭」 칸에 있어도 읽기로 하지 않은 종류의 조회는 **내지 않는다**. 입력은 표가 고정한 것 + 단계 ① 의 대상뿐(BR1 · BR2) · 순서·간격은 회피 갈래를 읽지 않는다 · 상품 이름 길은 **더한다**(BR3). **B 와 답 키 스크립트가 이 함수 하나를 쓴다** | `walk/calls.py` | BR1 ~ BR3 · §3-2a |
| 2 | 대상 쪽 조회의 `roles` = `자기` · `물려받음` · `하위 시술` · `하위 케이스` · `하위 제품`(종류 `offer` 의 제품 노드만 `자기` · `하위 제품`) · 부위·고민의 후보별 `facets` profile 은 `자기` · `물려받음` 그대로 | `walk/ranges.py` · `calls.py` | §3-1 ② 행 · §3-2 표 |
| 3 | 속성 시작: 그 속성을 가진 대상의 개요 · 적응 + **읽기로 한 종류의 맞춤 facet 만**(효과도 `outcome` 을 읽기로 했을 때만) | `calls.py` · `ranges.py` `attr_facets` | §3-2 속성 시작 행 |
| 4 | 읽기로 한 종류는 `coverage` 셈이 0 이어도 조회한다(KD4) · 조회마다 `next_cursor: null` 까지 · 쪽 밖 목록 포함 · 전부 `verified` 에 · 행마다 `range` · `kind`(같은 조회가 두 범위 · 두 종류에서 나오면 둘 다) · 방문 장부로 한 번만 | `walk/breadth.py` · `verified.py` | G9 · RG7 · §3-5 |
| 5 | **RQ1** — required = 읽기로 한 종류 가운데 `by` 가 `yes` · `top` · `entry` 인 것(기본 묶음으로만 더한 것은 required 아님). (대상, 종류)마다 **읽은 행으로** `self` · `lower` · `inherited` 를 센다 — `layer.role` 로 가르고 서로 다른 `gid` · `overview` · `mechanism` 은 그 종류의 칸에 값이 있는 profile 행만 · 적응은 허브 맞춤 그대로. 네 줄 → `met_by` = `self` \| `lower` \| `inherited` \| `null`. 값 쪽 · 속성 쪽은 행이 있으면 충족 · `offer` 의 제품 노드는 셋째 줄 없음 | 새 `walk/required.py`(세는 함수 하나 — 답 키 스크립트도 이것을 쓴다) · `depth.py` `required_status` 를 이것으로 대신 | §3-2 RQ1 · 불릿 |
| 6 | RQ1 의 셈 = 단계 ①-1 의 `coverage` 셈과 같아야 한다 — **다르면 그 (대상, 종류)를 `front.required[].coverage_mismatch` 로 기록**한다(판정은 읽은 행으로 · 조용히 맞추지 않는다 — 허브 T16 이 지키는 불변식을 앱 trace 에서도 보이게) | `required.py` | SPEC-001 §4-9 불변식 |
| 7 | 깊이: 시술 범위 = 「없음」(하위 층은 단계 ② 로 올라갔다) → ② → ③-4. 나머지 범위의 깊이 칸 · C1 ~ C3 은 그대로이되 다음 홉의 조회는 「읽기로 한 종류의 조회를 그 대상으로」(속성 시작 · §3-2 표) · 깊이 후보 설명에 `coverage` 셈(`rows`)을 싣는다 | `calls.py` `depth_candidates` · `depth_calls` · `depth.py` | §3-2 깊이 칸 · §3-3 `candidates` |
| 8 | 종료: 「근거 충족」 = 다 읽음 + 깊이 끝 + required 전부 RQ1 로 충족 + K1 ~ K5 / 「후보 소진」 = 어느 required 가 넷째 줄(세 조건에 안 걸림) | `end_state.py` `decide` | §5 표 |
| 9 | **(가) 판정용 조회**: 읽은 조회가 전부 0 이고 그 `ledger_check[]` 합이 비지 않을 때만 — 그 대상의 그 범위의 나머지 조회(§3-2 「폭」 칸)를 불러 전부 `total: 0` 인지 본다. 그 행은 **`verified` 에 넣지 않고** `breadth[].purpose` = `end_state` 로 기록. 상위 고민 펼침 행(`hier.match` = 상위)은 셈에서 뺀다 · 읽은 범위 전부를 합쳐 본다. **B 와 답 키가 같은 함수** | `end_state.py`(`unsettled_rows` 를 넓힘) · `breadth.py` | §5 (가) 행 · 불릿 |
| 10 | (나) · (다) 는 0.4.1 그대로((다) 는 1회차 판정 안 함 — O-5 ②) · 세 상태(범위 밖 · 입구 없음 · 실행 중단)에서도 단계 ⑤ · `b_on` 은 안 돌림 · 묶음 하나가 입력 한도보다 크면 「실행 중단」 사유 `FT5` | `end_state.py` · `col_b.py` | §5 불릿 |

**NOTE 한 줄(N-6)**: (가) 의 판정용 조회는 **먼저 단계 ①-1 의 `coverage` 셈으로 견준다** — 그 범위의 나머지 종류의 `self` · `lower` · `inherited` 가 전부 0 이면 허브를 더 부르지 않아도 된다. 다만 `coverage` 는 상위 고민 펼침 행을 빼지 않으므로(「Q10 결정」 과 다른 수가 날 수 있다) **Q10 과 고민 대상 몇 개에서 조회로 센 값과 같은지 시험으로 대조하고, 한 건이라도 다르면 SPEC 본문대로 조회로 판정한다.** 어느 쪽으로 정했는지와 대조한 수를 보고한다(O-5 ③ (iii)).

**완료 조건**(모의)
1. 자기 0 · 하위 n · 물려받음 m 인 (대상, 종류) → 하위 층 행이 `verified` 에 있고 `met_by` = `lower` · 「근거 충족」. 같은 꼴에서 Jev 깊이 Noul 을 0 으로 줘도 결과가 같다(Jev 가 못 바꾼다 — e2e 3 의 꼴).
2. 자기 0 · 하위 0 · 물려받음 n → `met_by` = `inherited` · 「근거 충족」 · 그 묶음에 「물려받은 값으로 채움」 표지(WP-4). 원리 칸이 빈칸뿐인 자기 profile 행은 `mechanism` 의 `self` 로 안 세어진다.
3. 세 층 모두 0 → 「후보 소진」(원장 확인 항목이 걸리고 판정용 조회도 0 이면 「원천 미확정」 (가)).
4. 읽기로 하지 않은 종류의 조회가 `breadth[]` 에 `purpose` = `read` 로 **하나도 없다** · 판정용 조회의 행이 `verified_gids` 에 없다.
5. `plan_calls` 를 B 와 답 키 스크립트가 같은 객체로 import 한다(시험이 본다) · 제품 노드 `offer` 호출의 `roles` 에 `물려받음` 이 없다.
6. 시술 범위에서 ③-1 ~ ③-3 이 돌지 않는다(Jev 요청 = 단계 ① 1 + `answer_ready` 1).

**검증**: `uv run pytest tests/test_walk_core.py tests/test_walk_ranges.py tests/test_walk_required.py -q`.

## 7. WP-4 — 답 재료: 싣는 칸 · 줄 번호 · 표지 · gate

**SPEC**: §3-2a 「LLM 에 싣는 칸」 표(13 줄) · 「기록에만 두는 칸」 · 「모든 줄에 늘 싣는 것」 · gate 표(G1 ~ G12) · §3-6 FT1 ~ FT7 · §4 G1 ~ G12 · K1 ~ K5 · §6-3 「B 에만 해당하는 것」 · §7-3 `verified_gids[]` · `verified_lines[]` · `gates[]` · `llm_input_bytes` · `llm_pages`.

| # | 구현 | 어디 |
|---|---|---|
| 1 | 싣는 칸 표 13 줄을 `walk/kinds.py` 에 상수로(gold 헤더 이름 그대로 · (표, 종류) → 칸 목록). 같은 profile 행을 `overview` · `mechanism` 이 함께 읽으면 칸을 합친다 · 부위·고민의 후보별 profile 은 넷째 줄(이름 · 계열 · 시술 · 원리 이름) | `walk/kinds.py` |
| 2 | 묶음 표: 묶음 키 = (`gold_table`, 대상 칸, `layer.role`) · 같은 값 칸은 머리에 한 번 · 다른 값은 줄별 · 빈칸도 값 · **칸은 종류가 정한 것만**(깊이 결정 · Noul · 크기와 무관 — `listed_only` 줄도 같은 칸) · 줄마다 **줄 번호 `n`**(한 질문 안 1 부터 · 쪽을 넘어 이어짐) · `gid` · 코드 · silver 칸 · `evidence_kind` 칸 · `price_mid_raw` 는 **줄에 없다** | `walk/fold.py` · 새 `walk/material.py`(줄 만들기 — 이름 제안) |
| 3 | `verified_lines[]{n, gid, gold_table, silver_table, silver_id, evidence_kind, kind, range, layer, depth}` — 줄 수 = `verified_gids` 수 | `verified.py` · `col_b.py` `b_trace` |
| 4 | 늘 싣는 표지: 층(`layer.role` · holder 이름 · `hier.match` · `attr.column`) · 깊이(`deepen` / `listed_only`) · 「원장 진술(검증 안 됨)」(= `evidence_kind` — 묶음 안 값이 같으면 머리에 한 번 · 다르면 줄마다) · `same_day` 빈칸 · 충돌 짝의 줄 번호(같은 `conflict_id` 를 앱이 묶음) · 「물려받은 값으로 채움」(`met_by` = `inherited` 인 종류의 묶음) · 하위 층 · 물려받음 묶음 머리에 holder 이름(FT7) · TG2 · TG3 `named` · 입구 고르기로 읽은 입구의 표지 · 「더 볼 수 있는 정보」(`offered` 종류 이름 + 행 수) · `scope_gap` · 종료 상태 | `verified.py` `marks` · `material.py` · `col_b.py` `judgement` |
| 5 | gate: **K1** 줄 번호 수 = `verified_gids` 수 · `verified_lines` 빠짐 0 · 읽기로 한 종류의 싣는 칸이 전부 실렸나 · 조회 계획이 빠짐없이 `complete` / **K4** 표지가 다 붙었나 + `price_mid_raw` 가 재료에 **없나** + 물려받은 값으로 채운 종류의 표지 / **K5** 「행의 표 ∈ 읽기로 한 종류가 허용한 표」(판정용 조회의 행이 섞이면 실패) / **G7** = 명시 대상(`target` · `uncertain_kept` · `named` · 입구 고르기 확정)이 재료에 있나 — `dropped` · `overlaps` · `unused` 셋만 예외 / **G12** 결과를 `gates[]` 에 | `walk/gate.py` |
| 6 | 쪽 나눔(FT4) · 「못 실으면 실행 중단」(FT5)은 그대로 — 줄 번호만 쪽을 넘어 잇는다 | `fold.py` `pages` · `col_b.py` `prompt_pages` |
| 7 | Jev state 의 `verified` 는 식별 칸만(대상 · 표 · facet · 층 · 행 수 · `depth`) — 그대로 | `depth.py` |

**NOTE 한 줄씩**
- **N-1**: 「말할 이름 = 시술 이름」 표지는 **값을 싣는다.** `procedure_name` 칸이 없는 표(`g_outcome` · `g_adverse` · `g_adverse_detail` · `g_recovery` · `g_pair` · `g_package`)의 케이스 행은 **그 케이스의 `g_profile.procedure_name`** 을 표지에 적는다 — 값은 그 케이스의 `facets` profile 한 번으로 얻고(`purpose` = `label` 로 기록 · 그 profile 행은 `verified` 에 넣지 않는다 — K5) 이미 읽은 profile 이 있으면 그것을 쓴다. 값을 못 얻으면 표지 없이 넘기지 말고 K4 실패다.
- **N-4**: `g_scope` 의 `path` 는 **층 표지의 일부로**(holder 이름과 함께) 싣고 `link` 는 기록(`verified_lines[].layer`)에만 둔다.

**완료 조건**(모의)
1. 재료 문자열에 `gid` 꼴(`G[A-Z]{2}-\d{5}`) · `silver_` · `_code` 칸 이름 · `price_mid_raw` 가 **0** · 줄 번호가 1 부터 빠짐없이.
2. 읽은 행 수 = 재료 줄 수 = `verified_lines` 수(행을 빼는 길이 없다) · `listed_only` 후보 줄의 칸 = `deepen` 후보 줄의 칸.
3. 표 · 종류마다 재료의 칸 집합 = §3-2a 표의 칸 집합(13 줄 전부 시험 · 헤더에 없는 칸 0).
4. `evidence_kind` 가 섞인 묶음은 줄마다 · 한 값이면 머리에 한 번 표지 · 케이스 행(칸 없는 표)에 시술 이름 **값**이 든 표지.
5. K1 ~ K5 가 각각 실패하는 합성 입력으로 「실행 중단」 이 난다(K5: 읽기로 하지 않은 종류의 행을 섞음).
6. 같은 질문에서 종류 하나만 읽을 때의 `llm_input_bytes` < 14 종류 전부 읽을 때(「B 전체」)의 값.

**검증**: `uv run pytest tests/test_walk_material.py tests/test_walk_core.py -q`.

## 8. WP-5 — 답 프롬프트(초안) · 답 꼬리

**SPEC**: §6-3 P1 ~ P10 · 「B 에만 해당하는 것」 · §7-3 `answer_lines[]` · §7-2 `answer` · `cited[]` · O-9 · O-25 ④ · §10-1 「고정 표지」.

- **문구는 초안이다 — e2e 보고 때 사용자가 확인한다(C-1).** 파일을 고치면 sha 가 바뀌어 「프롬프트 미확정(사용자 확인 전)」 표지가 다시 붙는다(`prompts.py` 그대로 — 풀어 주는 길을 만들지 않는다).

| 파일 | 고칠 것 |
|---|---|
| `prompts/common.md`(세 열 공통) | **P2** 답 본문에 id 를 줄마다 넣지 않는다(0.4.1 의 「문장마다 인용」 지시를 뺀다) · **P9** 모범 답 꼴 — 짧게 · 계열로 묶고 · 시술 이름으로 · 원리 한 줄 · 물은 것만 · 끝은 되묻기 · **P10** 층을 밝힌다(하위의 것 / 윗층의 것 — 물려받은 값으로 채운 정보도) · P1 · P3 ~ P8 은 그대로 |
| `prompts/col_b.md` | 재료 읽는 법: 줄 번호 · 층 표지 · 「원장 진술」 · 「물려받은 값으로 채움」 · `deepen` / `listed_only` · TG2 · `named` · 「더 볼 수 있는 정보」(읽지 않은 정보를 아는 것처럼 말하지 않고 되묻기 재료로) · 종료 상태 · `scope_gap`. **답 꼬리**: 답 본문 뒤에 답 줄 ↔ 재료 줄 번호를 짧게 적게 한다(본문에는 번호 · id 를 넣지 않는다) |
| `prompts/col_a.md` · `col_c.md` | 인용을 줄마다 달라는 문장이 있으면 P2 에 맞춰 뺀다(근거는 trace 의 `paths[]` · `gids[]` 에 남는다) |
| `prompts/judge.md` | 「근거 추적」 의 물음을 id 인용이 아니라 기록 대조로(§8-3 — WP-8 과 함께) |

- 꼬리 처리(`col_b.py`): 앱이 꼬리를 **떼어** `answer_lines[]{answer_line, rows[]}` 로 남기고 `answer`(화면 · 채점 입력)에는 꼬리가 없다. 꼬리가 없거나 깨졌으면 답은 그대로 · `answer_lines` = `null`(오류로 만들지 않는다). 쪽이 여럿이면 쪽마다 떼어 잇는다. 스트리밍 화면에 꼬리가 보이지 않게 — 꼬리의 시작 표식 뒤는 화면으로 흘리지 않는다(표식의 꼴은 구현 때 정하고 보고 — O-25 ④).
- **N-5**: 출력 토큰 지표는 **꼬리를 포함한 값**이다 — 꼬리의 글자 수를 `columns.b` 의 trace 에 따로 적어(`answer_tail_chars` — 이름 제안) 보고서 「답 길이」 행의 주석에 「B 는 꼬리 포함」 을 밝힌다.

**완료 조건**: 모의 CLI 로 — 꼬리가 있는 답 → `answer` 에 꼬리 없음 · `answer_lines` 의 줄 번호 ⊂ `verified_lines` 의 `n` · 꼬리가 깨진 답 → `answer_lines` = `null` · 답 그대로 · `prompts --status` 가 「미확정」 을 낸다 · `JEV_FILES` 가 실제 파일과 같다(없는 파일을 가리키지 않는다).
**검증**: `uv run pytest tests/test_columns.py tests/test_interim.py tests/test_cli.py -q`.

## 9. WP-6 — 열 정리 · 속도 탭 · 화면 · 기록

**SPEC**: §7-1 `settings` · `order` · §7-2 · §7-3 · §10-1 전부 · O-11(이름) · O-26 ① ② ③.

| # | 구현 | 어디 |
|---|---|---|
| 1 | **`b_slim` 을 새 B 로 합친다**(O-26 ②): `columns/col_b_slim.py` · `walk/select.py` · `prompts/jev/bundle.md` · `tests/test_speed.py` 의 선별 시험을 지운다. `runner.ALL_COLS` 에서 `b_slim` 을 빼고 **`b_full`**(화면 이름 「B 전체」 — 정보 종류 14 를 전부 읽은 꼴: 단계 ① 은 같고 읽는 종류만 그 대상의 표에 있는 것 전부 · 이름은 제안)을 넣는다. `b_full` 은 채점 대상이 아니다 | `runner.py` · `columns/col_b.py`(읽는 종류를 덮어쓰는 인자 하나) |
| 2 | 속도 탭의 열 = **`b` · `c`** 가 늘 돌고 고르면 `b_full` · effort 하나를 그 실행의 모든 열에(그대로) · 카드 머리 = 전체 ms · 첫 답 글자 ms · 단계별 ms(Jev · 허브 · LLM — 「선별」 막대는 없어진다) · LLM 입력 KB · 출력 토큰 · 모델 · effort. 「넘긴 묶음 / 뺀 묶음」 표 자리에는 **`front.kinds[]`**(종류 · Noul · 결정)을 그 필드 이름 그대로 보인다 — 새 문구를 짓지 않는다 | `speed.py` `SPEED_COLS` · `web/server.py` `speed_columns` · `web/static/speed.js` · `index.html` |
| 3 | 정확도 탭 기본 열에서 **「B 켬」 을 뺀다**(고르면 켬 — O-26 ①). batch 의 `b_on` 은 그대로 | `web/server.py`(`b_on` 기본 `False`) · `web/static/app.js` · `index.html` |
| 4 | B trace 화면: `front`(대상 · 종류 · `gap` · 범위 · required 의 `met_by`) · `breadth[]` 의 `kind` · `purpose` · `verified_lines` 수 · `answer_lines` 유무를 trace 필드 이름으로 보인다. 옛 줄(`front` 없음 · `range_choice` 있음 · `b_slim` 있음)을 다시 볼 때 깨지지 않는다(없는 필드는 비워 둔다) | `web/static/app.js` · `speed.js` |
| 5 | 기록: `timing.stages[]` 이름 = `resolve` · `coverage` · `jev` · `hub` · `gate` · `llm` · `parts{jev_ms, hub_ms, llm_ms}`(`select_ms` 는 없어진다) · `calls.hub_calls` 에 `coverage` · 판정용 · 표지용 조회 포함 · `settings` 에서 범위 문턱 둘을 뺀다 · trace 에서 `selection` 을 뺀다 | `runs.py` · `timing.py` · `config.py` `walk_settings` · `col_b.py` `b_trace` |
| 6 | 화면 고정 표지(「프롬프트 미확정」 · 「추론 끔 = effort low」 · 「동시 실행」 · gold 해시 앞자리)는 그대로 · 기준 지표 `click_to_first_answer_ms` 그대로 | 손대지 않음 — 시험만 |
| 7 | README 「실행 안내(e2e)」 의 `b_slim` 줄 · 속도 탭 줄을 새 열 이름으로 | `README.md` |

**완료 조건**: `b_slim` · `select_ms` · `selection` 낱말이 `clinic_chat/` · `prompts/` · `README.md` 에 0(옛 줄을 읽는 자리의 「없으면 비움」 처리는 예외 — 그 줄 수를 보고) · `runner --columns b_full` 이 모의로 돈다 · 화면 API 시험(실호출 0)이 새 열 목록 · 옛 줄 다시 보기를 본다 · 화면에 새로 넣은 글자가 전부 SPEC 용어 · trace 필드 이름 · 옛 화면의 말이다(더한 글자 목록을 보고).
**검증**: `uv run pytest tests/test_speed.py tests/test_web.py tests/test_runs.py tests/test_batch.py -q` → 18221 에 띄워 화면을 한 번 본다(모의 또는 WP-9 와 함께).

## 10. WP-7 — 세트 · 답 키 다시 뽑기(37)

**SPEC**: §9-3c(길 찾기 묶음 넷 — 16 문항 · 세트 합 85) · §9-4 · §9-5(입력 · 출력 · 기대 종료 상태 계산 · 확인 절차) · O-27 · O-10 · O-19.

| # | 구현 | 어디 |
|---|---|---|
| 1 | 세트 칸에 **`expected_kinds[]`** 를 더한다 · `expected_entries[]` 는 모든 문항에 · `source` 에 「길 찾기」 · 묶음 수 = 37 · 19 · 4 · 4 · 5 · **16**(= 85) | `evalset/loader.py` `FIELDS` · `BUNDLE_COUNTS` · `validate` |
| 2 | 37 의 `expected_kinds[]` **초안**: `questions.csv` 의 `gold_tables` 칸 → §3-2a 표로 종류에 대응(결정론 · 질문 문장을 해석하지 않는다). `g_pair` 처럼 한 표가 네 종류에 걸치는 것은 그 문항의 범위로 가른다(시술 조합 = `combo` · 동시 가능 = `same_day` · 순서·간격 = `order_interval` · 회피 = `avoid`) — 가를 수 없는 문항은 지어내지 않고 대조 요약에 올린다 | `evalset/key_calls.py` |
| 3 | 호출 명세 = **기대 대상 × 기대 종류의 조회** — WP-3 의 `plan_calls` 를 그대로(roles 에 하위 층 포함) · 부위·고민은 `groups` 를 끝까지 읽어 후보별 profile 호출을 편다(그대로) · `resolve` · `scope` 호출은 명세에 없다(`lineup` 을 기대 종류로 가진 문항의 `g_scope` 행은 키 `rows[]` 에 넣지 않는다 — §9-5) | `evalset/key_calls.py` |
| 4 | 키 `rows[]` — **N-2**: 종류별 행도 RQ1 과 **같은 함수**(WP-3 `required.py`)로 거른다 — `overview` · `mechanism` 은 그 종류의 칸에 값이 있는 profile 행만 키에 든다(원리 칸이 빈칸뿐인 하위 제품 profile 행이 키에 들어 C 가 D7 에서 깎이지 않게). 대조 요약에 「칸 값으로 빠진 profile 행 수」 를 문항마다 낸다 | `evalset/answer_key.py` |
| 5 | 기대 종료 상태: (가) = WP-3 의 같은 판정 함수(판정용 조회 포함 · 그 행은 키에 안 넣음) · 기대 종류마다 `self` · `lower` · `inherited` → `met_by` 를 대조 요약에 · 물려받은 행뿐인 기대 종류 = 「근거 충족」 · `status` 가 「답함」 인데 세 층 모두 0 인 기대 종류 = 「상태 안 맞음」(값을 지어내지 않는다) | `evalset/answer_key.py` `expected_state` · `summary_row` |
| 6 | 대조 요약 「걸린 문항」 에 더함: `expected_kinds[]` 초안이 `gold_tables` 대응과 다른 문항 · RQ1 로 상태가 바뀐 문항 · 키가 0.4.1 키보다 **줄어든** 문항(범위 길 → 대상 × 종류 — 행 수 앞뒤) | `answer_key.py` `write_summary` |
| 7 | **37 다시 뽑기(실물 — 새 허브 18106)**: 명세 37 → 키 37 → `data/eval-set/key-summary.md`. 옛 키 · 옛 명세는 지우지 말고 `data/eval-set/_v041/` 로 옮긴다(gitignore 로컬). 키는 전부 **미확인** 상태다 — `confirmed` 를 워커가 적지 않는다 | 로컬 `data/eval-set/**` |
| 8 | 길 찾기 16 문항 **초안**(C-2 — 0.4.1 의 추가 32 와 같은 길): `pick.py` 가 허브 `coverage` 로 꼴에 맞는 코드 후보를 낸다((i) 자기 0 · 하위에 행인 상위 제품 · 시술 · 계열 (iv) 물려받음만 있는 대상 · 덮인 조각 · 한 글자 이름 · 두 표 겹침 …) → 워커가 문장 초안을 세트 파일에 `status: draft` 로 · `expected_entries[]` · `expected_kinds[]` · 기대 종료 상태와 함께. 「정보 종류 하나만」 다섯은 KD8 질문 셋(`data/experiments/kd8/` — 실험용)을 **복사하지 않고** 새로 적는다(그 셋은 사용자 확정 대상이 아니다). draft 문항은 Jev · LLM 으로 보내지 않는다 | `evalset/pick.py` · 로컬 `set.jsonl` |

**완료 조건**
1. 같은 build · 같은 명세 → 바이트까지 같은 키(그대로) · `sample_check`(표본 ⊂ 키)의 결과를 문항마다 보고 — **키가 「대상 × 종류」 로 좁아져 표본이 안 드는 문항이 생기면 그것은 `expected_kinds[]` 초안이 좁다는 뜻이다. 명세를 손으로 넓히지 말고 걸린 문항으로 올린다.**
2. Q10 = (가) · Q33 = (나) · Q12 = (다)(답 키 쪽 `asked_fields[]`)가 그대로 나오는지 보고(다르면 「상태 안 맞음」 그대로 올린다).
3. `review-spec-v051.md` §2 의 대상(`product:PRD-416`)을 기대 대상으로 둔 합성 명세로: 효과 → `met_by` = `lower` · 원리 → `inherited` 가 대조 요약에 찍힌다.
4. `loader --validate` 가 85 줄(draft 수 포함)을 통과.
5. 보고: 걸린 문항 수와 까닭별 수 · 0.4.1 키 대비 행 수 변화 · draft 16 의 `resolve` 후보 수.

**검증**: `uv run pytest tests/test_answer_key.py -q` → 실물: `HUB_REST_URL=http://127.0.0.1:18106/procedure-hub/gold uv run python -m clinic_chat.evalset.key_calls --from-gold-build <gold-build.py>` → `… answer_key --all`.

## 11. WP-8 — 채점 · 보고서

**SPEC**: §8-2 D1 ~ D10 · 불릿 · §8-3(「근거 추적」) · §10 열별 표 · 「B 전용」 · 「B 낮은 effort / 켬」 · O-17 · O-25 ① ②.

| # | 구현 | 어디 |
|---|---|---|
| 1 | D1 · D2: 답이 글자로 적은 id 가 없으면 「해당 없음」 · **B 의 D2 = `answer_lines[]` 의 줄 번호 ⊂ `verified_lines[]`** | `quality/checks.py` |
| 2 | **D10 「읽지 않은 것」**(B · C · A 는 「해당 없음」): 답의 이름 → 코드(D3) 가운데 그 열이 읽은 행(B `verified_gids` · C `tool_calls[].gids[]`)의 키 코드 칸 · 곁 칸 어디에도 없는 것 → `unread_codes[]`(기록 · 위반 수 아님) | `quality/checks.py` · `quality/grade.py` |
| 3 | D7: 키가 「기대 대상 × 기대 종류」 로 바뀐 것만 받는다(식은 그대로) · B 가 읽은 대상 · 종류가 기대를 품는데 0 이 아니면 대조 요약에 「앱 결함」 으로 | `quality/grade.py` |
| 4 | 보고서 열별 표: 「답 길이 — 출력 토큰 · LLM 입력 KB」 행 · `first_answer_text_ms` · D10 행 | `report.py` `_col_table` |
| 5 | 「B 전용」 에 **맨 앞 판단**: 대상 일치(확정 ⊇ `expected_entries[]` 인 문항 수 · 놓친 · 더 둔 · `dropped` 중 기대였던 수 · `named` 수와 그중 기대가 아니었던 수) · 종류 일치(읽은 ⊇ `expected_kinds[]` · 놓친 · 더 읽은 · `offered` 중 기대였던 수) · 끌어낸 범위에 기대 범위 · `scope_gap` 수 · 대상 · 종류 Noul 분포(yes / 사이 / no) · 후보 수 분포 · `met_by` 분포 · 판정용 조회가 돈 문항 수 · `answer_lines` 가 선 문항 수 · `entry.unused[]` 수 · 입구 고르기 지표. 0.4.1 의 `range_choice` 분포 줄은 뺀다 | `report.py` `_b_only` |
| 6 | ② 채점의 「근거 추적」 물음 · 입력을 P2 에 맞춘다(`prompts/judge.md` — WP-5) | `quality/judge.py` |

**NOTE 한 줄(N-3)**: ② 채점 입력은 이번 판도 **(a) 전체 행 · 전 칸 그대로**다 — 「§3-6 과 같은 꼴」 로 줄일 때 「전 칸」 인지 「싣는 칸」 인지는 1회차 trace 뒤 O-17 을 정할 때 함께 정한다(코드에 TODO 를 남기지 않고 §15 에 적어 둔다).

**완료 조건**: 합성 run 줄로 D2(B · 줄 번호) · D10 · 「B 전용」 의 새 줄이 값으로 찍힌다 · A 의 D10 이 0 이 아니라 「해당 없음」 · 미확인 키로 채점이 거부되는 것이 그대로다(풀어 주는 플래그 없음).
**검증**: `uv run pytest tests/test_quality.py -q`.

## 12. WP-9 — 실물 확인 · 마감

**전제**: 새 허브가 18106 에 떠 있다(WORK-005 WP-4 뒤 — 허브 워커 또는 코디). 앱 화면 확인은 18221. Jev 키 · CLI 구독은 앱 `.env` · 로컬 로그인(워커는 `.env` 를 열지 않는다 — 없으면 「못 돌림」 으로 보고).

| # | 문항(문장은 `$W/work-v05-instructions.md` 「쓸 것」 의 E 목록 · 여기는 꼴만) | 열 | 보고에 적을 것 | 기대 |
|---|---|---|---|---|
| E7 | e2e 3 — 자기 행 0 인 상위 제품 이름 × 효과(`product:PRD-416`) | `b` · `c` | 종료 상태 · `front.targets[]` · `front.kinds[]`(값 · 결정) · `required[].met_by` · 하위 층 행 수 · `llm_input_bytes`(KB) · 첫 답 글자 ms · 전체 ms | 「근거 충족」 · `met_by` = `lower` · 하위 제품의 자기 행 4 가 재료에 |
| E8 | e2e 4 — 같은 제품 이름에 옛 조사 목록 밖의 조사 × 원리 | `b` · `c` | 같음 + `resolve` 후보 수 · 입구 고르기가 **안 돈 것** | 「근거 충족」 · `met_by` = `inherited` · 답이 「윗층의 것」 임을 밝힘 |
| E9 | 고민 하나에 무엇을 하나(큰 폭 — 0.4.1 에서 입력 110 KB) | `b` · `c` · `b_full` | 같음 + 후보(`groups`) 수 = 재료의 후보 수 · `b` 와 `b_full` 의 입력 KB | 「근거 충족」 · 후보 전부가 재료에 · 입력이 0.4.1 값보다 작다 |
| E10 | 종류를 짚지 않은 「…뭐야」 꼴(계열 · 시술 이름) | `b` · `c` | 같음 + 읽은 종류 · `offered` 종류 | 「근거 충족」 · 읽은 종류 = 개요(+ yes 로 난 것) |
| E11 | Q22(동시 가능 · 두 끝) | `b` · `c` | 같음 | 「근거 충족」 · 0.4.1 기준선(첫 글자 2.2 초)과 나란히 |

- 실행: `HUB_REST_URL=… HUB_GOLD_MCP_URL=… uv run python -m clinic_chat.runner --question "<문장>" --columns b,c`(E9 는 `b,c,b_full` · E11 은 `--set-id Q22`). 문항마다 1 회 — 단건이라 편차가 크다는 것을 보고에 밝힌다. effort 는 속도 탭 조건(`low`)으로 맞춘다.
- 기대와 다르면 **코드를 그 문항에 맞춰 고치지 않는다**(규칙은 일반 규칙이어야 한다 — `_RESUME` §1 e2e 피드백 3) — trace 를 붙여 보고한다.
- 실물 값으로 다시 볼 것(WP-0): `kind_{k}` 가 물은 종류를 yes · 1위로 세웠나 · `target_{i}` 가 맞는 후보에 낮은 값을 냈나(냈어도 `named` 로 읽혔나).
- 마감: `uv run ruff check .` · **전체 `uv run pytest -q` 한 번**(기준선 138 과 나란히 — 지운 시험 수 · 더한 시험 수를 함께) · `batch --check` · 18221 화면에서 E7 을 한 번(정확도 탭 · 속도 탭 · 기록 다시 보기 — 옛 줄 하나 포함) · README 갱신 · 커밋 후보 grep(시술 이름 · 질문 문장 · 실제 `gid` · LCK id · 홈 경로 · 키 꼴 0).
- **하지 않는 것**: 전체 batch · 채점(키 미확인) · 18105 · 18220 재시작 · 커밋.

## 13. 순서 · 의존 · 병행

```
허브(WORK-005)   WP-1 ─┐
                 WP-2 ─┼─ WP-3 ─ WP-4 ──────────────┐(18106 에 새 허브)
앱(WORK-006)  WP-0                                   │
              WP-1 ─ WP-2 ─ WP-3 ─ WP-4 ─ WP-5 ─ WP-6 ┼─ WP-7(실물 뽑기) ─ WP-9
                                   └────── WP-8 ──────┘
```

| 무엇 | 근거 |
|---|---|
| 앱 WP-1 ~ WP-6 · WP-8 은 허브를 기다리지 않는다 | 필요한 허브 응답은 둘뿐이고 꼴이 WORK-005 §3(`matched`) · §4(`coverage`)에 고정돼 있다. 「하위 *」 role 의 `facets` 는 0.4.1 허브가 이미 낸다 |
| 앱 WP-2 → WP-3 → WP-4 는 차례로 | 조회 계획 · required · 재료가 앞 WP 의 꼴에 기댄다 |
| WP-5 · WP-6 · WP-8 은 WP-4 뒤 서로 나란히 | 파일이 갈린다(`prompts/` / `web/` · `speed.py` / `quality/` · `report.py`) |
| WP-7 의 코드는 WP-3 뒤 · 실물 뽑기는 허브 WP-4 뒤 | `plan_calls` · `required.py` 를 함께 쓴다 |
| 모의 ↔ 실물 꼴 대조 | WP-9 앞에 `hub_rest --ping` 으로 `coverage` · `resolve` 응답의 키 집합을 모의와 대조한다(다르면 모의를 고치고 그 WP 시험을 다시) |
| 바꿔 끼우기 | 허브 · 앱이 다 끝난 뒤 **코디가** 18105 · 18220 을 함께 새 코드로 다시 띄운다(WORK-005 §7) |

## 14. SPEC-002 변경 절 ↔ WP 대응(미대응 0)

**0.5.0 — A. 길 찾기 재설계**

| 결정 → 옮긴 것 | 절 | WP |
|---|---|---|
| 맨 처음 Jev 가 대상 · 정보 종류를 판단 · 순서를 뒤집음 | §0 · §1 · §3-1 흐름 | WP-2 · WP-3 |
| ① 넓은 후보 · 후보마다 행 수 셈 | §3-1 CD1 ~ CD4 | WP-1 · WP-2 |
| ② Jev 한 요청 — 대상 Noul · 종류 Noul · 범위는 결정론 · instructions 영어 · 후보 설명에 행 수 | TG1 ~ TG6 · KD1 ~ KD7 · RG1 · §3-2a · §3-3 | WP-0 · WP-2 |
| ③ 고른 대상 × 종류만 · 그 안에서는 빠짐없이 · 하위 층 자기 행 + 층 표시 · required | 단계 ② · §3-2 role · RQ1 · G4 · G12 · §5 | WP-3 · WP-4 |
| ④ 애매한 Noul — 대상은 넘김 쪽 · 종류는 기본 묶음과 합집합 | TG2 · KD2 · KD3 · 기본 묶음 · §3-4 | WP-2(WP-0 이 본문 그대로임을 고정) |
| ⑤ 깊이 · 틀린 말 검사 · 종료 상태 유지 · 다시 적음 | §3-1 대응 표 · G4 · G7 · G9 · K1 · K5 | WP-3 · WP-4 |
| ⑥ 답에 id 인용을 줄마다 넣지 않음 · 모범 답 꼴 | §6-3 P2 · P9 · P10 · §8-2 D10 · 「근거 추적」 | WP-5 · WP-8 |

**0.5.0 — B. e2e 실패 넷 + 속도 탭**

| # | 막히는 자리 | WP · 확인 |
|---|---|---|
| e2e 1 | 읽기 전에 종류를 고름 · P2 · P9 | WP-2 · WP-4 · WP-5 · E9 |
| e2e 2 | 화면 기본 열에서 B 켬 | WP-6 |
| e2e 3 | 하위 층을 결정론으로 읽음 · RQ1 · 후보 설명에 셈 · 층 밝힘 | WP-3 · WP-4 · WP-5 · E7 |
| e2e 4 | 부분 일치 · 입구 고르기 안 탐 · 물은 종류만 | 허브 WP-1 · 앱 WP-2 · E8 |
| (속도 탭) | 선별이 읽기 앞으로 | WP-2 · WP-6 · E9 |

**0.5.0 — C. 되적기**

| 되적은 것 | 절 | WP |
|---|---|---|
| F-1 짧은 조각 빼기 없앰 | CD2 | WP-2(0.4.1 구현의 「긴 조각 안의 짧은 조각 후보를 뺀 것」 을 없앤다 — `app-report.md`) |
| W-1 속성 시작 폭 · R2-N2 효과도 읽기로 했을 때만 | §3-2 속성 시작 행 | WP-3 |
| Q10 (가) 펼침 행 제외 · 같은 함수 · (나) 에도 | §5 불릿 · BR3 | WP-3 · WP-7(이미 구현 — 판정용 조회를 더함) |
| Q25 순서·간격은 회피 갈래 안 읽음 | BR3 | WP-3(이미 구현 — `plan_calls` 로 옮길 때 유지) |
| W-2 ~ W-8 — `entry.unused[]` · 상품 이름 길 넓히기만 · `FT5` · D4 · D8 표마다 | TG6 · BR3 · §5 · §8-2 불릿 | WP-2 · WP-3(이미 구현 — 유지 · 시험 그대로) |
| 제품 offer role · `distinct_rows` | §3-2 상품 행 | WP-3(앱의 `ROLES_PRODUCT_OFFER` 에서 `물려받음` 을 뺀다) |
| N1-1 · 되묻기 재료에 이름 · 코드 · 세 상태엔 켬 안 돌림 · W2-1 세 상태에서도 단계 ⑤ · C-1 | §5 · §6-3 머리 · O-9 | WP-3 · WP-5(이미 구현 — 유지) |
| CLI 로 추론 끌 수 없음 → `low` | §6-1 · O-23 | 이미 구현 — 변경 없음 |
| 화면 · 속도 탭 · 조건 맞춤 · 동시 실행 · C 측정 보정 | §10-1 · §7-1 `order` · §7-2 · §7-3 `interim_text[]` | 이미 구현 — WP-6 이 열만 정리 |

**0.5.0 — D. 시험 세트**: §9-3c · §9-4 → WP-7.

**0.5.1**

| 지적 · 결정 | 절 | WP |
|---|---|---|
| 결정 3 ① · F-1 — RQ1 네 줄 · `met_by` · 칸으로 세는 종류 · G12 · 종료 상태 · P10 · §9-3c 기대 | §3-2 RQ1 · §4 G12 · K4 · §5 표 · §6-3 P10 · §7-3 `met_by` · §9-3c · §9-5 · §10 | WP-3 · WP-4 · WP-5 · WP-7 · WP-8 |
| 결정 3 ② · W-1 — 덮이지 않은 일치는 대상 · 빼는 것은 덮인 조각뿐 · 입구 고르기는 후보 0 일 때만 · G7 | TG3 ~ TG5 · RG6 · 입구 고르기 표 · §3-4 · G7 · §5 · §7-3 `front` | WP-2 · WP-4(G7) |
| 결정 3 ③ · W-2 — WORK 첫 WP = 정보 종류 판단 확인 | KD8 · §9-3c · O-24 ④ ⑤ | WP-0(결과 반영) |
| 「LLM 에는 필요한 것만」 · W-6 — 싣는 칸 표 · 기록에만 두는 칸 · gate 표 · 줄 번호 · `verified_lines` · `answer_lines` · D2 · D10 | §3-2a · §3-3 · §3-6 FT2 · FT3 · FT5 · FT6 · G8 · G9 · K1 · K4 · §6-3 · §7-3 · §8-2 · O-18 · O-25 · O-28 | WP-4 · WP-5 · WP-8 |
| W-3 — ① (가) 의 뜻 · 판정용 조회 ② 종류 단위 ③ e2e 보고 때 ④ D7 ⑤ 추가 묶음의 키 길 ⑥ 명세 입력 낱말 | §5 (가) · §8-2 D7 · §9-4 · §9-5 · O-5 | WP-3 · WP-7 · WP-8 |
| W-4 — C 열 · 허브 도구 설명에 하위 role | §2-4 · D7 불릿 | 허브 WORK-005 WP-3 · 앱 WP-1(C 도구 8) |
| W-5 — 적응 세는 식 | §3-2 RQ1 규모 | WP-3(허브 맞춤 그대로 셈) |
| W-7 · W-8 | SPEC-001 | WORK-005 WP-3 |
| N-1 · N-2(0.5.0 검수의 것) — e2e 4 종료 상태 · 후보 0 · 종류 전부 no · `gap` yes | 변경 기록 · O-21 ⑤ | WP-2(입구 고르기 표) · E8 |

**재검수 NOTE 6(`review-spec-v051.md` §7)**

| # | 한 줄 | 어디 |
|---|---|---|
| N-1 | 칸 없는 표의 케이스 행은 표지가 시술 이름 **값**을 싣는다 — 그 케이스의 `g_profile.procedure_name` | WP-4 |
| N-2 | 키 `rows[]` 의 종류별 행도 RQ1 과 같은 함수 — 칸에 값이 있는 행 | WP-7 |
| N-3 | ② 채점 입력은 지금 전 칸 그대로 · 줄일 때 「전 칸 / 싣는 칸」 은 O-17 과 함께 1회차 trace 뒤 | WP-8 · 아래 열린 것 |
| N-4 | `g_scope.path` 는 층 표지의 일부로 · `link` 는 기록에 | WP-4 |
| N-5 | 출력 토큰은 꼬리 포함 · 꼬리 글자 수를 따로 기록 | WP-5 |
| N-6 | (가) 판정은 `coverage` 셈을 먼저 견주고 · Q10 결정과 수가 다르면 조회로 | WP-3 |

**이번 판에 구현 대상이 아닌 절**(바뀌지 않았거나 뒤 단계): §2-3 A 의 원장 도구 · §6-1 · §6-2 · §6-4 · §8-4 · §8-5 · §8-6 · §9-1 ~ §9-3b(문항은 그대로 — 답 키만 WP-7 의 길로 다시) · 추가 32 + 길 찾기 16 의 **확정 · 그 키 뽑기**(사용자 확정 뒤) · 전체 batch · 채점.

## 15. 열린 것 · 이 문서를 쓰며 본 것(SPEC 은 고치지 않았다)

| # | 무엇 | 이 문서의 제안 | 상태 |
|---|---|---|---|
| O-24 ④ ⑤ | KD2 · KD3 | **본문 그대로**(KD8 결과) | 닫힘 — 1회차 trace 로 다시 봄 |
| O-24 ⑦ | instructions 문구 | 종류 · 후보 · 입구 · 깊이 후보의 **이름을 instructions 에 직접**(WP-0). `target` · `entry` · `candidate` 쪽은 미확인 | 1회차 trace 뒤 재확인 |
| O-11 | 이름 | 새 열 `b_full` · 파일 `walk/front.py` · `kinds.py` · `required.py` · `material.py` · trace `answer_tail_chars` · `front.required[].coverage_mismatch` · `breadth[].purpose` 에 `label`(N-1 의 표지용 조회) | 구현 때 정함 — 보고 |
| O-25 ④ | 답 꼬리의 꼴 | 본문 밖 꼬리 · 표식은 구현 때 · 스트리밍 화면에 안 보이게 | 구현 때 정함 |
| O-26 | 열 정리 | ① B 켬을 화면 기본에서 뺌 ② `b_slim` 을 `b` 로 합침 · 「B 전체」 = `b_full` ③ 동시 상한은 지금 값 | 구현 때 정함(SPEC 추천 그대로) |
| O-28 | 싣는 칸 목록 | 표 그대로 | 1회차 trace 뒤 고침 |
| O-5 ③ (iii) | 판정용 조회의 꼴 | `coverage` 먼저 견줌 → 다르면 조회(N-6) | 구현 때 정함 — 보고 |
| O-17 · N-3 | ② 채점 입력 크기 · 꼴 | (a) 전 칸 그대로 | 1회차 trace 뒤 |
| B-1 | **`purpose` = `label` 은 SPEC 에 없는 값이다** — SPEC §7-3 `breadth[].purpose` 는 `read` \| `end_state` 둘. N-1 의 값(케이스의 시술 이름)을 얻는 조회를 기록할 자리가 필요해 더했다 | 받으면 SPEC 되적기 후보 · 안 받으면 「이미 읽은 profile 이 있을 때만 값을 싣고 없으면 케이스의 `layer.holder` 로 대신」 은 **하지 않는다**(다른 필드로 채우는 것이라) — 그때는 `end_state` 처럼 기록 없이 부를 수는 없으니 코디가 정한다 | 코디 확인 필요(구현 전) |
| B-2 | 「B 전체」 를 「단계 ① 은 같고 읽는 종류만 전부」 로 읽었다 — SPEC §10-1 은 「정보 종류 14 를 전부 읽은 꼴 = 0.4.1 의 폭」 까지만 적었다. 싣는 칸도 14 종류의 것이 되어 0.4.1 의 「전 칸」 과는 입력 크기가 다르다 | 그대로 가고 화면 · 보고에 「B 전체 = 종류 전부 · 싣는 칸은 0.5.1」 임을 밝힌다(0.4.1 기준선과 직접 견줄 수 없다) | 구현 때 정함 — 보고 |
| B-3 | 37 의 `expected_kinds[]` 를 `gold_tables` 에서 낼 때 `g_profile` 이 `overview` 인지 `mechanism` 인지 표만으로는 갈리지 않는다 | 둘 다 초안에 넣고 대조 요약에 올린다(사용자가 답 키 확인 때 고름 — 기존 확인 지점) | 뒤 단계에서 사용자 확인 |
| B-4 | 답 키가 「대상 × 종류」 로 좁아지면 0.4.1 키에서 걸렸던 17 문항의 까닭이 바뀐다 | WP-7 대조 요약에 앞뒤를 나란히 | 보고 |

## 변경 기록

### 0.1.0 (2026-11-16)

- 새로 씀 — SPEC-002 0.5.0 · 0.5.1 의 변경 절을 WP 열로. KD8 결과(`kd8-jev-check-report.md`)를 WP-0 으로 받아 KD2 · KD3 을 본문 그대로 두고 「instructions 에 이름 직접」 을 구현 지시로 넣었다(코디 11-16 지시 — `target_{i}` · `entry_{i}` 도 같은 꼴 · 미확인 · 1회차 trace 재확인).
