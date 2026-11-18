---
type: work
id: WORK-008
title: "앱 0.5.2 구현 계획 — 세트 칸(U-1 · U-2) · 허브 0.5.2 응답 받기(윗고민 · 자손 층 · 부위 묶임 표지) · 답 키 다시 뽑기(키 전용 기준 대상 빼고 대조) · 구멍 묶음 꼴 · 실물 확인"
status: draft
product: procedure-hub
feature: phub-gold-jev
version: 0.1.0
created_at: 2026-11-17
updated_at: 2026-11-17
tags:
  - product/procedure-hub
  - feature/phub-gold-jev
  - doc/work
  - status/draft
links:
  specs:
    - "orchestration/work/phub-gold-jev/SPEC-002-chat-eval.md (0.5.2 · 검수 FAIL 0 · WARN 1 — review-spec-v052.md) ← 계약"
    - "orchestration/work/phub-gold-jev/SPEC-001-hub-gold-mcp.md (0.5.2 — 허브 도구 계약 · §5-9 HG1 ~ HG3)"
  decisions:
    - "orchestration/work/phub-gold-jev/_RESUME.md §2 (2026-11-17 「SPEC 0.5.2 사용자 결정(전부 추천)」 — U-1 Q03 · Q05 lineup 뺌 / U-2 Q03 · Q05 에 indication · outcome 더함 · 「답 키 검토」 · 2026-11-16 「v05 앱 검수 뒤(코디)」)"
  related:
    - "orchestration/work/phub-gold-jev/WORK-007-hub-v052.md (허브 쪽 — 먼저 돈다 · §8 이 새 응답 꼴)"
    - "orchestration/work/phub-gold-jev/WORK-006-app-v05.md (0.5.1 구현 계획 — 공통 규칙 §2 를 그대로 잇는다)"
    - "orchestration/work/phub-gold-jev/app-key-fix1-report.md (K1 ~ K7 · 키 전용 기준 대상 · 미결 1 ~ 6)"
    - "orchestration/work/phub-gold-jev/review-spec-v052.md (§7 WARN 3 · NOTE 6 — 이 문서 §10)"
---

# WORK-008 — 앱 0.5.2 구현 계획(되적기 확인 + 허브 구멍 셋의 앱 쪽)

> 경로 접두어: `P` = 프로필 워크트리 · `W` = `$P/orchestration/work/phub-gold-jev` · `SM` = 로컬 데이터 폴더(WORK-007 과 같음) · `APP-WT` = `~/orca/workspaces/clinic_chat/phub-gold-jev`(브랜치 `kknaksss/phub-gold-jev` · **0.5.1 구현 + 수정 1 + 답 키 고치기 1 이 미커밋으로 올라가 있다 — 그 위에 이어서 고친다 · 새로 쓰지 않는다**).
> **계약은 SPEC-002 0.5.2 이다.** 이 문서는 「어느 파일을 · 어떤 순서로 · 무엇으로 확인하나」 만 정한다. SPEC 에 없는 동작 · 화면 문구 · 답 문구를 만들지 않는다 — 어긋나는 것은 코드를 맞춰 고치지 말고 보고한다(§11).
> 하지 말 것 · 로컬 자리 · env · 검증 명령의 틀은 **WORK-002 §2 · WORK-006 §2 그대로**다(§2 에 바뀐 것만).
> **질문 문장 · 시술 · 고민 · 부위 이름은 이 문서에 없다.** 실물 확인 문항 넷은 꼴과 코드로만 적고, 문장은 `$W/work-v052-instructions.md` 「쓸 것」 의 WORK-008 줄 · 로컬 세트 파일에서 읽는다.
> **사용자 결정은 닫혔다**(_RESUME §2 11-17 — 전부 추천): **U-1 = (a)** Q03 · Q05 의 케이스에서 `lineup` 을 뺀다 / **U-2 = (a)** Q03 · Q05 의 기대 종류에 `indication` · `outcome` 을 더한다(윗층만 → 층 밝히면 정답). 허브 쪽 U-3 = 행 0 고민만 · 가까운 윗고민 하나 / U-4 = 보조 입력 ③.

## 0. 요약

- SPEC-002 0.5.2 의 대부분은 **되적기**다 — 구현이 먼저 있었고 SPEC 이 따라 적었다. §7 표가 줄마다 「이미 있음 · 파일:줄」 을 댄다. **새로 짓는 것은 넷**: ① 세트 칸(U-1 · U-2) ② 허브 0.5.2 의 새 응답(윗고민 · 자손 층 · 부위 묶임)을 RQ1 · 답 재료 표지 · gate 로 받는 것 ③ **답 키 다시 뽑기**(키 전용 기준 대상을 빼고 → 행이 같은지 대조) ④ 구멍 묶음 10 문항의 **draft 꼴**.
- WP 여섯: **WP-1** 세트 칸(U-1 · U-2) → **WP-2** 허브 0.5.2 응답 받기(모의로) → **WP-3** 답 키 다시 뽑기 · `key-table.md`(**허브 뒤**) → **WP-4** 구멍 묶음 꼴(§9-3d — draft 까지) → **WP-5** 되적기 확인 → **WP-6** 실물 확인 · 마감(**허브 뒤**).
- 순서: **허브(WORK-007) 먼저.** 앱의 WP-1 · WP-2 · WP-5 · WP-4 의 코드는 허브를 기다리지 않는다(WORK-007 §8 의 응답 꼴 셋만 본다). **WP-3 · WP-4 의 후보 뽑기 · WP-6 은 새 허브(18106) 뒤**다.
- 사용자 확인 지점은 늘지 않는다: 답 키 확인 1회(`key-table.md` — WP-3 뒤 코디가 보인다) · 추가 문항 확정(구멍 묶음 10 — WP-4) · 답 프롬프트 문구(e2e 보고 때 — 이 판에서 답 꼴 · 문구는 정하지 않는다 · O-31).

## 1. 지금 코드(11-17 확인 — `APP-WT`)

| 파일 | 지금(0.5.1 + 수정 1 + 답 키 고치기 1) | 이번에 |
|---|---|---|
| `clinic_chat/clients/hub_rest.py`(301줄) | `concern_candidates(concern_code, site, **kw)`(`:194`) · `read_all` 이 쪽 밖 목록 · 머리 필드를 모은다(`:137-162`) · `OUTSIDE_LISTS`(`:33`) | WP-2 — 머리 `inherited_from` 이 `ReadAll.as_response()`(`:91`)에 남는지 확인(안 남으면 남긴다). 새 입력 `upper` · `descend` 는 **주지 않는다**(허브 기본값 = 넓히는 쪽) |
| `clinic_chat/walk/required.py`(110줄) | `layer_bucket`(`:24-35`) = `layer.role` 로 `self` · `inherited` · `lower` · role 없으면 `self` → **윗고민 행도 `self` 로 센다** | WP-2 — 윗고민으로 물려받은 `concern_candidates` 행 = `inherited` |
| `clinic_chat/walk/material.py`(207줄) | `llm_marks`(`:43-82`) = `layer` · `holder` · `path` · `hier` · `attr` · `depth`(**깊이 결정** — `:60`) · `speak_name` · `inherited_fill`(`layer.role` = 물려받음일 때만 — `:73`) · `time_of` · `about` | WP-2 — 자손 층 표지(`layer.depth` · `via`) · 부위 묶임 표지(`site_match`) · 윗고민 채움 표지 |
| `clinic_chat/walk/verified.py`(181줄) | `group_key`(`:42-46`) = (표, 대상, `layer.role`) · `marks`(`:58-65`) = `layer` · `hier` · `attr` | WP-2 — 묶음 열쇠가 자손 층을 섞지 않는지 · `site_match` 를 기록 표지에 |
| `clinic_chat/walk/gate.py`(166줄) | K4 = 표지가 붙었나(`:98-128`) · G12(`:146`) | WP-2 — 새 표지 셋이 K4 에 |
| `clinic_chat/walk/calls.py`(383줄) | 고민 + 부위 = 부위마다 `concern_candidates(concern_code, site)` 한 조회(`:177-180`) · 부위 필터 부위마다(`:97-108`) · `key_calls`(`:273-278`) | 그대로(§7 「이미 있음」) |
| `clinic_chat/walk/end_state.py`(90줄) | (가) = 읽은 조회 전체 0 + `ledger_check[]` | WP-2 — 윗고민 행이 온 조회는 0 이 아니다(코드 변화 없이 서는지 시험) |
| `clinic_chat/evalset/loader.py`(169줄) | `FIELDS`(`:21-22`)에 `key_upper_entries` · `key_lower_entries` · `key_fix1` 이 없다(세트 파일에는 있다) · `BUNDLE_COUNTS`(`:24`) = 85 | WP-1 · WP-4 |
| `clinic_chat/evalset/key_calls.py`(317줄) | `build_spec` — 세트 확정값이 초안을 이김(`:163-210`) · 키 전용 기준 대상 → `entries[].upper_of` · `lower_of`(`:184-185`) | WP-1 — 대상별 기대 종류(§11 B-1) |
| `clinic_chat/evalset/answer_key.py`(493줄) | `kinds_met`(`:166`) · `fold_extra`(`:197-214`) · 옛 키 대비(`_v041` — `:383`) | WP-3 — 대조 스크립트 · 허브가 낸 `inherited_from` 을 `via` 로 |
| `clinic_chat/evalset/key_table.py`(128줄) | `KIND_KO["indication"]` = 「어디에 쓰나」(`:19`) · `--prev _v051`(`:122`) | WP-3 — 앞 판 폴더 이름만 |
| `clinic_chat/evalset/pick.py`(174줄) | `--paths` = 길 찾기 16 의 코드 후보(`:84-156`) | WP-4 — 구멍 묶음 후보(`--holes` — 이름 제안) |
| `tests/fake_hub.py`(76줄) · `tests/walk_fixture.py`(144줄) | 모의 허브 — 정해 둔 응답을 그대로 | WP-2 — 새 필드를 넣은 가짜 응답 |
| 로컬 `data/eval-set/`(gitignore) | `set.jsonl` 85 줄 · `calls/` 37 · `answer-key/` 37 · `key-summary.md` · `key-table.md` · `_v041/` · `_v051/` | WP-1 · WP-3 · WP-4 |

세트의 지금 값(11-17 확인 — 코드만): Q03 `expected_entries` = `procedure_case:CAS-016` · `modality:M1` · `expected_kinds` = `overview` · `mechanism` · `lineup` · `key_lower_entries` = `procedure:PRC-001`(of `M1`) / Q05 = `procedure_case:CAS-021` · 같은 세 종류 / Q10 = `concern:CON-012` · `indication` · `key_upper_entries` = `concern:CON-008` / Q12 = `modality:M2` · `adverse:ADV-051` · `adverse` · `key_lower_entries` = `procedure:PRC-100` · `101` · `102`(of `M2`).

기준선: 11-17 코디 검증 = `uv run pytest -q` **163 passed · 1 skipped**(`_RESUME` §5 「app-key-fix1 완료」).

## 2. 공통 — WORK-006 §2 에서 바뀐 것만

| 항목 | 이번 판 |
|---|---|
| allowed_paths | WORK-006 §2 와 같다 — `clinic_chat/**` · `prompts/**` · `tests/**` · `README.md`(실행 안내 절). `pyproject.toml` · `uv.lock` · `.gitignore` · `.env.example` 은 안 고친다(새 env 없음). gitignore 로컬 = `.env` · `data/**` · `runs/**` |
| 포트 | **18220(화면) · 18105(허브)는 코디 것** — 죽이거나 다시 띄우지 않는다. 새 허브는 허브 워커가 WORK-007 WP-5 에서 띄워 둔 **18106** 만 쓴다(`HUB_REST_URL=http://127.0.0.1:18106/procedure-hub/gold` · `HUB_GOLD_MCP_URL` 을 그 실행의 프로세스 env 로 — `.env` 를 열거나 고치지 않는다). 화면 확인은 **18221** |
| 외부 호출 | 단위 시험은 전부 모의. 실물은 WP-3 · WP-4 의 허브 호출(Jev · LLM 없음)과 WP-6 뿐 |
| 답 프롬프트 · 화면 문구 | **이 판에서 새 문구를 지어 넣지 않는다.** 표지의 값은 SPEC 이 적은 말(§3-1 BR1 의 「부위 글자로 맞음」 / 「그 부위의 고민으로 묶임」 · G12 의 「물려받은 값으로 채움」)과 gold 칸 값까지다. 하위 고민을 어떻게 묶어 말하나(e2e 피드백 5)는 정하지 않는다(SPEC O-31) |
| 옛 기록 | `runs/runs.jsonl` 의 옛 줄 · `data/eval-set/_v041/` · `_v051/` 은 고치거나 지우지 않는다 |
| 검증 | `uv run ruff check .` · `uv run pytest tests/test_<이 WP 것>.py -q` · 전체 `uv run pytest -q` 는 WP-6 에 한 번 |

## 3. WP-1 — 세트 칸: U-1 · U-2

**목표**: 사용자 결정 둘을 **세트 파일의 칸**으로 넣는다(키 파일을 손으로 고치지 않는다 — KF1 · §9-5 확인 절차 3). 명세 · 키는 WP-3 에서 다시 뽑는다.
**SPEC**: §11 U-1 · U-2 · §9-4 세트 파일 칸 · §9-5 KF1 · KF3 · §8-3 「정답 꼴 둘」 ① · `app-key-fix1-report.md` 미결 3.

| # | 할 것 | 어디 |
|---|---|---|
| 1 | **U-2**: Q03 · Q05 의 `expected_kinds[]` 에 `indication` · `outcome` 을 더한다(순서 = §3-2a 표의 순서) · `key_fix1{at, why}` 를 적는다(`why` = 「SPEC 0.5.2 사용자 결정 U-1 · U-2 — _RESUME §2 2026-11-17」) | 로컬 `data/eval-set/set.jsonl` |
| 2 | **U-1**: 두 케이스(`CAS-016` · `CAS-021`)에서 `lineup` 을 뺀다 — **Q05 는 `lineup` 없음 · Q03 은 계열 `M1` 쪽 `lineup` 만 남는다.** Q05 는 `expected_kinds[]` 에서 `lineup` 을 지우면 된다. **Q03 은 대상이 둘이라 지금 칸(`expected_kinds[]` — 문항에 하나)으로는 「이 대상에서만 뺀다」 를 적을 수 없다** → 대상별로 적는 길 하나가 필요하다(§11 B-1 — 제안: 세트 칸 `expected_kinds_by_entry{표:코드: kinds[]}` · 없으면 `expected_kinds[]` 가 모든 대상에) | 로컬 `set.jsonl` · `evalset/key_calls.py` `build_spec`(`:163-210`) · `evalset/answer_key.py` `kinds_met`(`:166`) · `evalset/key_table.py` |
| 3 | 세트 로더가 0.5.2 의 칸을 안다 — `key_upper_entries` · `key_lower_entries` · `key_fix1`(+ B-1 의 칸)을 `FIELDS` 밖의 **선택 칸**으로 두고 꼴만 검증한다(`{node, of}` 가 `표:코드` 인가 · `of` 가 `expected_entries[]` 에 있나). 필수 칸으로 올리지 않는다(다른 82 줄에 없는 칸이다) | `evalset/loader.py`(`:21-22` · `validate`) |
| 4 | B · C 가 읽는 대상 · 종류에는 **아무것도 바뀌지 않는다** — 세트의 기대 칸은 채점 기준일 뿐이다(B 걷기 · 답 프롬프트를 고치지 않는다) | — |

**완료 조건**
1. 합성 세트 한 줄(가짜 케이스 + 가짜 계열 · 대상별 기대 종류)로: 명세의 조회에 케이스의 `scope`(lineup) 호출이 **없고** 계열의 것은 있다 · `kinds_met` 에 케이스의 `lineup` 줄이 없다 · 대상별 칸이 없는 문항은 지금과 같은 명세가 나온다(기존 `tests/test_key_fix1.py` 8 · `tests/test_answer_key.py` 가 그대로 통과).
2. `loader --validate` 가 85 줄을 통과한다(칸 꼴 오류 0).
3. 보고: 세트에서 바꾼 줄 = Q03 · Q05 둘 · 바꾼 칸 이름.

**검증**: `uv run pytest tests/test_key_fix1.py tests/test_answer_key.py -q` → `uv run python -m clinic_chat.evalset.loader --validate`.

## 4. WP-2 — 허브 0.5.2 응답 받기(윗고민 · 자손 층 · 부위 묶임)

**목표**: 허브가 넓혀 준 행을 **층을 가려** 세고(RQ1), 답 재료에 그 층을 표지로 싣고, gate 가 표지가 붙었는지 본다. 앱이 묶인 고민을 따로 찾거나 대상을 바꾸지 않는다.
**SPEC**: §3-1 BR1(끝 두 문장) · TG6 · §3-2 RQ1 아래 0.5.2 불릿 셋(고민 대상의 RQ1 · 「하위 *」 = 자손 전부 · 상품의 층 셈) · §4 G4 · G10 · G12 · K4 · §5 (가) · §7-3 `front.required[]` · SPEC-001 §5-9 HG1-4 · HG2-4 · HG3-4 · O-25.

**모의부터**: `tests/fake_hub.py` · `tests/walk_fixture.py` 에 WORK-007 §8 「응답 꼴」 셋을 넣은 가짜 응답을 더한다(가짜 코드 · 가짜 이름). 실물 꼴과의 대조는 WP-6 앞에 `hub_rest --ping` 으로(§8).

| # | 할 것 | 어디 | 내용 |
|---|---|---|---|
| 1 | 머리 필드 | `clients/hub_rest.py` `read_all`(`:137-162`) | `concern_candidates` 응답 머리의 `inherited_from` · `counts.self_rows` · `counts.by_site_match` 가 끝까지 읽은 응답(`as_response()`)에 남는다(첫 쪽의 값). 새 입력은 주지 않는다 — `upper` 기본 `auto` · `descend` 기본 `all` |
| 2 | **고민 대상의 RQ1** | `walk/required.py` `layer_bucket`(`:24-35`) · `target_rows`(`:63-83`) · `required_status`(`:86-110`) | **머리 `inherited_from` ≠ `null` 인 `concern_candidates` 조회의 행**은 `inherited` 로 센다 → `met_by` = `inherited`(RQ1 셋째 줄). 행의 `hier.match` = `상위` **만으로 가르지 않는다** — `facets` package 값 쪽의 `상위`(윗고민 패키지)와 섞이면 안 된다. `front.required[]` 의 그 줄에 `inherited_from.concern_code` 를 함께 기록한다(필드 이름 = `inherited_via` 제안 — 답 키 `kinds_met[].via` 와 같은 뜻) |
| 3 | `coverage` 대조 | `walk/required.py:99-104` | 고민 노드의 `coverage` `indication` 이 `{self, inherited}` 수로 온다 — 읽은 행의 셈과 같아야 한다(좁힘 없는 조회에서만 대조 — 그대로). 모의 `coverage` 도 그 꼴로 |
| 4 | 종료 상태 | `walk/end_state.py` | 윗고민 행이 온 조회는 「조회 전체에서 행 0」 이 아니다 → **(가) 가 아니라 「근거 충족」**(SPEC §3-2 · §9-5 KF3 의 Q10) · `ledger_check[]` 는 그대로 기록에 남는다. 코드 변화 없이 서는지 시험으로 확인하고, 안 서면 판정 식이 아니라 2 의 셈을 본다 |
| 5 | 윗고민 표지 | `walk/material.py` `llm_marks`(`:43-82`) | 행의 `hier` = `상위` 는 이미 실린다(`:57-58`). **`inherited_fill` 을 윗고민으로 채운 종류에도 붙인다**(지금은 `layer.role` = 물려받음일 때만 — `:73`) — G12 (ii) 의 「물려받은 값으로 채움」 표지 그대로. 어느 윗고민인지는 행의 `asked_concern_name` 칸(이미 싣는 칸 — `walk/kinds.py:139`)이 말한다 · 형제 고민 행은 `concern_name` · `concern_match` 칸(같은 줄)이 가른다(O-25) — **새 칸을 싣지 않는다** |
| 6 | **자손 층 표지**(HG2) | `walk/material.py` · `walk/verified.py` `marks`(`:58-65`) | `layer.depth` ≥ 2 인 행에 「거친 층」 표지를 붙인다. **이름이 겹친다 — 지금 `depth` 표지는 깊이 결정(`deepen` · `listed_only`)이다(`material.py:60`).** 새 표지는 다른 이름으로 둔다(제안 `layer_depth` · `layer_via` — §11 B-2). `via[]` 에는 **이름이 없다**(표 · 코드 · `scope_gid`) → 사람이 읽는 이름을 얻는 길: (a) 케이스 행은 이미 「말할 이름 = 그 케이스의 시술 이름」(`speak_name` — G10)이 있다 (b) 그 밖(계열 → 시술 → 제품 · 제품 → 제품)은 기존 `purpose` = `label` 조회(`walk/calls.py:44` · B-1)로 그 holder 의 이름을 얻는다. **이름을 못 얻으면 표지를 지어내지 않고 코드를 기록에만 남긴다**(LLM 에는 코드를 보내지 않는다 — §3-2a) |
| 7 | 묶음 열쇠 | `walk/verified.py` `group_key`(`:42-46`) · `walk/fold.py` | 층별 묶음(FT7)에서 **다른 holder 의 행이 한 묶음에 섞여 holder 표지가 하나만 남지 않는지** 확인한다 — 자손 층으로 `하위 케이스` 행이 여러 시술 아래에서 온다. 섞이면 열쇠에 holder 를 넣는다(행은 빼지 않는다) |
| 8 | **부위 묶임 표지**(HG3) | `walk/material.py` · `walk/verified.py` | 행의 `site_match[]` 를 표지 `site_match` 로 싣는다 — 값은 SPEC §3-1 BR1 의 두 말(「부위 글자로 맞음」 / 「그 부위의 고민으로 묶임」) · 둘 다면 둘 다. `csi_ids[]` 는 기록(`verified_lines[]`)에만 |
| 9 | gate K4 | `walk/gate.py`(`:98-128`) | 표지가 붙었나에 셋을 더한다: `layer.depth` ≥ 2 행의 거친 층 표지 · `site_match[]` 가 있는 행의 표지 · 윗고민으로 채운 종류의 `inherited_fill`. 빠지면 K4 실패(G4 · G12 표지와 같은 자리) |
| 10 | 고민 + 부위는 한 조회 | `walk/calls.py:177-180` | **이미 있음** — 부위마다 `concern_candidates(concern_code, site)`. 앱이 묶인 고민을 따로 부르지 않는다(확인만) |
| 11 | 상품의 층 셈 | `walk/material.py` · 모의 | 제품 노드 `offer.inherited` = `0`(모의도 `0` — `null` 아님) · 상품 행에서 「하위에 따로 있는 상품」 이라는 표지를 만들지 않는다 — 행의 `item_name` 등 싣는 칸(`walk/kinds.py:166`)으로 가른다. 지금 코드가 `lower` 를 그렇게 말하는 표지를 붙이는지 확인하고, 없으면 「이미 있음」 으로 적는다 |
| 12 | C 열 | `columns/col_c.py:18` · `prompts/col_c.md` | 도구 8 · 「도구 설명을 따른다」 그대로 — 허브의 새 설명(하위 role = 자손 전부 · 윗고민 · 부위 묶임)이 MCP 로 그대로 간다. **앱 쪽 변경 없음**(확인만) |
| 13 | 화면 · 기록 | `web/static/app.js:89-91` · `runs.py:24` | `front.required[]` 를 그대로 찍는 자리라 새 필드가 보인다 — **문구를 더하지 않는다**. 옛 줄(새 필드 없음)에서 화면이 깨지지 않는지만 확인 |

**완료 조건**
1. 모의 Q10 꼴(행 0 고민 → 윗고민 행): `front.required[]` 의 `indication` = `self` 0 · `inherited` ≥ 1 · `met_by` = `inherited` · 윗고민 코드 기록 · 종료 = 「근거 충족」 · `ledger_check[]` 가 trace 에 남음 · 재료의 그 행들에 `hier` · `inherited_fill` 표지 · 표지를 떼면 K4 실패.
2. 모의(막는 것): 자기 행이 있는 고민의 응답(`inherited_from: null`)은 지금과 같은 셈(`self`) · `facets` package 값 쪽의 `hier.match` = `상위` 행은 `inherited` 로 **세지 않는다**(지금과 같다).
3. 모의 HG2 꼴(계열 → 시술 → 케이스): `lower` 가 `depth` 2 행까지 세어진다 · 그 행에 거친 층 표지 + 케이스의 말할 이름 · 다른 시술 아래 케이스가 한 묶음에서 holder 표지를 잃지 않는다 · 깊이 결정 표지(`depth`)가 그대로 있다(이름이 안 겹친다).
4. 모의 HG3 꼴: `site_match[]` 의 두 값이 표지로 · 둘 다 맞은 행에 둘 다 · 묶임 없는 응답(필드 없음 — 0.5.1 허브)에서도 깨지지 않는다.
5. 답 키와 B 가 **같은 함수**다(`evalset/answer_key.py` 가 `walk/required.py` 를 쓴다 — 그대로): 같은 가짜 응답에서 키 `kinds_met[]` 의 `met_by` = B 의 `met_by`.
6. 기존 시험(`tests/test_walk_*.py` · `test_key_fix1.py` · `test_web.py`)이 그대로 통과한다.

**검증**: `uv run pytest tests/test_walk_core.py tests/test_walk_material.py tests/test_walk_front.py tests/test_key_fix1.py tests/test_web.py -q`(새 시험은 `tests/test_holes.py` — 이름 제안).

## 5. WP-3 — 답 키 다시 뽑기 · 대조 · `key-table.md`(허브 뒤)

**전제**: 새 허브가 **18106** 에 떠 있다(WORK-007 WP-5 · `health.files[]` 22 줄). Jev · LLM 을 부르지 않는다.
**SPEC**: §9-5 KF2(「구멍이 막히면 키 전용 기준 대상을 빼고 행이 같은지 대조 — 다르면 그 차이가 지적이다」) · KF3 · KF5 · §9-4 · SPEC-001 §5-9 「37 문항에서 바뀌는 것」 셋(HG1 = Q10 하나 · HG2 = 6 문항 · HG3 = 0) · `app-key-fix1-report.md` 미결 1 · 2.

**세 걸음으로 뽑는다 — 허브가 바꾼 것과 사용자 결정이 바꾼 것을 섞지 않는다.**

| 걸음 | 세트 | 허브 | 무엇을 얻나 |
|---|---|---|---|
| (가) 기준 | 지금 그대로(키 전용 기준 대상 있음 · U-1 · U-2 **앞**) | 0.5.1(지금 키 — 다시 뽑지 않는다) | 지금의 `data/eval-set/{calls, answer-key, key-summary.md, key-table.md}` 를 **`data/eval-set/_v052a/`** 로 옮겨 둔다(이름 제안 · gitignore 로컬 · `_v041/` · `_v051/` 은 그대로) |
| (나) 허브만 바뀜 | Q10 의 `key_upper_entries` · Q12 · Q03 의 `key_lower_entries` 를 **지운다** · 기대 종류는 (가) 와 같다(WP-1 의 U-1 · U-2 를 아직 넣지 않은 세트 사본으로 — 사본 자리는 `_v052b/` 제안) | **0.5.2(18106)** | 명세 37 → 키 37 → **(가) 와 대조** |
| (다) 최종 | (나) + WP-1 의 U-1 · U-2 | 0.5.2(18106) | 명세 37 → 키 37 → `key-summary.md` · **`key-table.md`**(앞 판 = `_v052a`) — 사용자 확인 1회의 재료 |

**(나) 의 대조 — 무엇이 같아야 하고 무엇이 달라도 되나**

| 문항 | 기대 | 다르면 |
|---|---|---|
| **Q10** | 키 `rows[]` 의 (`gold_table`, `gid`) 집합이 (가) 와 **같다**(윗고민 `CON-008` 을 직접 부른 행 = 허브가 `CON-012` 에 물려준 행 — SPEC-001 HG1-3) · `kinds_met` `indication` = `inherited` · `via` = `CON-008`(이번에는 키 전용 대상이 아니라 허브의 `inherited_from`) · 기대 종료 = 「근거 충족」 · `ledger_check[]` 에 `LCK-010` | **보고**(어느 `gid` 가 한쪽에만 있나 · 표별 수) |
| **Q12** | (`gold_table`, `gid`) 집합이 (가) 와 **같다**(계열 `M2` 하나로 하위 시술 셋 · 그 아래 케이스의 행까지 — SPEC-001 HG2) · 표본 4/4 · 기대 종료 = 「원천 미확정 (다)」 그대로 | 보고 |
| **Q03** | 같다(계열 `M1` 하나로 하위 시술 · 그 아래 케이스까지) | 보고 |
| Q19 · Q20 · Q25 · Q27 | **늘어난다**(SPEC-001 §5-9 셈: 쌍 14 → 18 · 9 → 12 · 5 → 6 · 7 → 9 — 계열 끝이 케이스 끝 관계까지 편다) — (가) ⊂ (나) 이고 는 행이 전부 `a_layer` · `b_layer` 의 `depth` ≥ 2 다 | 수가 다르거나 준 행이 있으면 보고 |
| Q18 · Q21 · Q22 · Q23 · Q28 · Q30 · Q36 | `rows[]` 는 같다(SPEC 셈 — 계열이 대상이지만 안 는다). **쪽 밖 `same_day_packages[]` 는 SPEC 이 세지 않았다 — 여기서 대조해 수를 보고한다** | 보고(지적이 아니라 SPEC 이 미룬 셈) |
| 그 밖의 문항 | 같다(HG3 로 바뀌는 문항 0 — 명세에 부위 입구 0) | **다르면 지적**(문항 · 표 · 수) |

- 대조는 **(`gold_table`, `gid`) 집합**으로 한다. `layer_role` 칸은 달라도 된다 — (가) 는 하위 시술을 직접 불러 그 시술 기준의 층(`자기` 등)이고 (나) 는 계열 기준의 층(`하위 시술` · `하위 케이스`)이다. 그 차이는 수로만 보고한다.
- 대조 스크립트는 코드로 남긴다(제안: `python -m clinic_chat.evalset.answer_key --diff _v052a` — 문항별 `only_prev` · `only_now` 수 · 표별 수 · `kinds_met` · 기대 종료 앞뒤). 결과 파일은 `data/eval-set/key-diff-v052.md`(gitignore 로컬 — 이름 제안).
- **차이가 나도 세트 · 명세를 손으로 넓혀 맞추지 않는다.** 차이 그대로가 보고다(KF2).

**(다) 뒤**

1. `key-summary.md` · `key-table.md` 를 다시 쓴다(`key_table --prev _v052a`). 「바뀜」 칸에 Q03 · Q05(U-1 · U-2) · Q10 · Q12(키 전용 대상 빠짐) · Q19 · Q20 · Q25 · Q27(HG2 로 는 행)이 찍힌다.
2. Q03 · Q05: 「상태 안 맞음(rq1)」 이 풀렸나(U-1) · `indication` · `outcome` 의 `met_by` 가 케이스에서 `inherited`(윗층만)로 서나 · 표본 7 이 키에 다 드나(U-2 — 0.5.1 은 7 중 1). 안 풀리면 그대로 보고한다.
3. **N-5 를 보고에 한 줄로 적는다**: 「U-2 로 Q03 · Q05 의 기대 종류가 늘었다 — B 가 그 종류를 읽지 않으면 빠짐으로 잡힌다」. `key-table.md` 의 두 줄에서 기대 정보 칸이 는 것이 보이는지 확인한다(코디가 사용자에게 표를 보일 때 함께 말할 것 — 표에 새 문구를 지어 넣지 않는다).
4. `--confirm` 을 **하지 않는다**(확인된 키 0 / 37 그대로 — 사용자 확인 뒤 코디가).

**완료 조건**: 같은 build · 같은 명세 → 바이트까지 같은 키(그대로) · (나) 대조표가 위 표의 줄마다 「같음 / 늘어남 n → m / 다름」 으로 채워졌다 · `key-table.md` 가 다시 쓰였다 · 보고에 `gold_hash`(0.5.1 과 같아야 한다) · `aux_hash`(달라야 한다)를 적었다.

**검증**: `uv run pytest tests/test_answer_key.py tests/test_key_fix1.py -q` → 실물: `HUB_REST_URL=http://127.0.0.1:18106/procedure-hub/gold uv run python -m clinic_chat.evalset.key_calls --from-gold-build <gold-build.py>` → `… answer_key --all` → `… answer_key --diff _v052a`.

## 6. WP-4 — 구멍 묶음 셋: draft 꼴(§9-3d)

**목표**: 10 문항(HG1 3 · HG2 3 · HG3 4)의 **꼴** — 대상 코드 후보 · 기대 대상 · 기대 종류 · 기대 종료 — 을 허브 셈으로 뽑아 둔다. **문장은 사용자 확인이다**(SPEC §9-3d · O-30 · _RESUME 「진행 순서」 C-2).
**SPEC**: §9-3d 표 · 끝 불릿 둘 · §9-4 · O-30 · O-31.

| # | 할 것 | 어디 |
|---|---|---|
| 1 | 후보 뽑기 — 허브 `coverage` · `concern_candidates` · `scope` 로(결정론 · Jev · LLM 없음 · 18106): **HG1** (i) 행 0 · 윗고민 한 단(9) (ii) 행 0 · 윗고민 두 단(4) (iii) 자기 행은 있으나 묶음 0(41) / **HG2** (i) 계열 × `indication` · `outcome`(케이스에 자기 행이 있는 계열) (ii) 계열 둘 — 케이스 끝에만 관계 행이 있는 짝 (iii) **아래 W-3** / **HG3** (i) (윗고민, 부위) 글자 일치 0 · 묶임으로 1 이상(37) (ii) 글자 일치도 있고 묶임도 있는 짝 (iii) 묶인 고민 자신 + 그 부위(자기 행 1 이상인 91) (iv) 묶임 없는 (고민, 부위) | `evalset/pick.py` 에 `--holes`(이름 제안) → `data/eval-set/pick-holes.json`(gitignore 로컬) |
| 2 | **W-3 — HG2 (iii) 의 꼴을 바꾼다**: SPEC 의 「자기 · 한 단 하위에 상품이 없고 두 단 아래에만 있는 계열」 은 허브의 상품 맞춤 식으로 **0 건**이다(케이스의 상품은 그 시술의 `procedure_code` 로 한 단에서 이미 잡힌다 — 검수 §3 · `HUB facets.py` offer 갈래). 이 꼴로는 문항이 서지 않는다 → **실제로 있는 꼴 둘을 후보로 뽑아 둘 다 보고하고 고르지 않는다**: (iii-a) 계열을 물어 **케이스의 부작용 · 회복 행**이 오나(케이스 자기 행 — 부작용 415 · 회복 9) (iii-b) 계열 → 시술 → **제품**의 두 단 아래 제품 행(새로 닿는 24 짝 · 계열 7). 어느 쪽으로 둘지는 문항 확정 때 사용자가 정한다(문항 수는 제안이라 SPEC 을 다시 돌리지 않는다 — O-30). 후보가 정말 0 인지도 `pick` 이 세어 보고한다 | 같은 곳 |
| 3 | draft 줄의 꼴 — 문항마다 `id`(제안 `H01` ~ `H10`) · `bundle`(§9-3d 의 묶음 이름 셋) · `source`(「구멍」 — 제안) · `range` · `expected_entries[]` · `expected_kinds[]` · `expected_end_state` · `status: draft`. **`question` 은 비워 둔다**(§11 B-3 — 문장 초안을 워커가 쓸지는 코디 확인. 기본 = 꼴만) | `data/eval-set/pick-holes.json` — **`set.jsonl` 에는 아직 넣지 않는다**(`loader` 가 85 줄 · 필수 칸을 본다 — `evalset/loader.py:69-80`) |
| 4 | 기대 종료(§9-3d 표 그대로): HG1 (i) (ii) = 근거 충족(층을 밝힘 · `met_by` = `inherited`) · **HG1 (iii) = 근거 충족 · 윗고민 행이 섞이지 않는다**(N-6 — U-3 = (a) 로 닫혔으므로 이 기대가 그대로 선다) · HG2 = 근거 충족 · HG3 (i) ~ (iii) = 근거 충족 · (iv) = 후보 소진 또는 근거 충족(후보의 행 수에 따라 — 후보마다 `pick` 이 적는다) | 같은 곳 |
| 5 | 세트 합 95 · `BUNDLE_COUNTS` 의 「구멍」 10 은 **문장이 확정돼 줄이 서는 때** 올린다(지금 올리면 `--validate` · `batch --check` 가 깨진다) — 이 WP 에서는 `loader` 에 묶음 이름을 받는 자리만 준비하고 수는 85 그대로 | `evalset/loader.py:24` |
| 6 | draft 문항은 Jev · LLM 으로 보내지 않는다 · 답 키도 뽑지 않는다(확정 뒤 — 「허브 0.5.2 구현 뒤에 답 키를 뽑는다」 는 이미 선다) | — |

**완료 조건**: `pick --holes` 가 꼴마다 후보 수 · 고른 후보(코드)를 낸다 · HG2 (iii) 은 SPEC 꼴의 후보 수(0 이 기대) + (iii-a) · (iii-b) 후보 수를 함께 낸다 · 후보 수가 SPEC §9-3d 「셈 근거」 · 검수 §2 의 수(13 = 9 + 4 · 41 · 18 계열 · 97 짝 · 37 · 91)와 맞는지 대조해 보고한다(다르면 보고) · `--validate` 85 줄 통과.

**검증**: `uv run pytest tests/test_answer_key.py -q`(pick 의 합성 시험이 거기 있으면 그 파일) → 실물: `HUB_REST_URL=… uv run python -m clinic_chat.evalset.pick --holes`.

## 7. WP-5 — SPEC-002 0.5.2 되적기 확인(코드에 있나)

**목표**: 변경 기록의 되적기 줄마다 코드를 대조한다. **있으면 고치지 않는다.** 아래는 11-17 에 이 문서를 쓰며 읽은 결과다 — 구현 워커는 줄마다 다시 열어 확인하고, 다르면 고친 것을 보고한다.

| 되적은 것(SPEC-002 0.5.2 변경 기록의 행) | 절 | 코드 | 할 일 |
|---|---|---|---|
| W-1 읽을 종류 0 → 기본 묶음(KD6) | §3-1 KD6 | **이미 있음** · `walk/front.py:254-262` · `tests/test_walk_front.py:177-184` | 없음 |
| W-2 부위마다 조회 · 둘째 부위는 `unused` 아님 | §3-1 BR1 · TG6 | **이미 있음** · `walk/calls.py:97-108 · 177-180` · `walk/gate.py:84-87` · `tests/test_walk_core.py:252` | 없음 |
| W-3 37 의 `expected_entries[]` = 명세 `entries` | §9-4 | **이미 있음** · 로컬 `set.jsonl`(37 문항 중 빈 것 0 — 11-17 셈) · `evalset/key_calls.py:171-172 · 208` | 없음 |
| N-2 `entry.by` = `noul` | §3-1 입구 고르기 | **이미 있음** · `walk/entry.py:119` · `walk/front.py:187 · 315`(기록 값 `noul`). `read_as.by` = `entry_pick`(`entry.py:120`)은 답 재료 표지(「이 입구로 읽었다」)이고 `runs.py:24` 의 `entry_pick` 은 trace 칸 이름이다 — `entry.by` 가 아니다 | 확인만 — trace 한 줄에서 `entry.by` 값을 찍어 본다 |
| N-5 gold 표 이름을 LLM 에 안 보냄 | §3-2a 「고르는 식」 | 확인 필요 · `walk/fold.py` · `walk/material.py` 의 묶음 머리 | 모의 답 입력(단계 ⑤ 프롬프트)에 `g_` 로 시작하는 표 이름이 0 인지 단언 한 줄(있으면 「이미 있음」 · 시험만 더함) |
| B-1 `purpose` = `label` | §7-3 `breadth[]` | **이미 있음** · `walk/calls.py:44` | 없음 |
| B-2 「B 전체」 = 단계 ① 같고 종류만 전부 · 채점 밖 | §10-1 | **이미 있음** · `columns/col_b.py:10 · 112` · `speed.py:18` | 없음 |
| 상품 셈 식 · 제품 offer `inherited` = 0 | §3-2 RQ1 아래 불릿 | 모의에 `0` 이 가는지 확인 필요 · `tests/walk_fixture.py:59` | WP-2 표 11 |
| G13 · G14 · 표지 `time_of` · `about` · K4 · 공통 답 지시 | §4 표 · K4 | **이미 있음** · `walk/material.py:77-81` · `walk/gate.py:126-128` · `prompts/common.md` · `tests/test_key_fix1.py:146-162` | 없음 |
| D11 | §8-2 | **이미 있음** · `quality/checks.py:182 · 194` · `report.py:115` | 없음 |
| ② 채점 입력 `kinds_met` · 정답 꼴 둘 | §8-3 | **이미 있음** · `quality/judge.py:59-71` · `quality/grade.py:149`. 「정답 꼴 둘」 의 채점 지시(`prompts/judge.md`)에 윗층만 · 자료 없음 두 꼴이 들어 있는지 확인 | 없으면 SPEC §8-3 의 문장을 그대로 옮긴다(새 문구를 짓지 않는다) |
| `lineup_rows[]` · `kinds_met[]` · `scope` 가 명세에 듦(lineup 한정) · 세트 칸 셋 · 세트 확정값이 초안을 이김 | §9-4 · §9-5 KF1 ~ KF5 | **이미 있음** · `walk/calls.py:273-278` · `evalset/answer_key.py:166 · 194-214 · 285` · `evalset/key_calls.py:163-210` · `evalset/key_table.py` | 세트 칸 셋이 `loader.FIELDS` 에 없다 → WP-1 표 3 |
| 화면 말 「적응」 → 「어디에 쓰나」 | §3-2a 불릿 · §9-5 KF5 | 답 키 표 = **이미 있음** · `evalset/key_table.py:19`. 화면 · 보고서 = 정보 종류의 한국어 이름을 찍는 자리가 없다(코드 · 영어 이름을 그대로 찍는다 — `web/static/app.js:82-91` · `report.py`). 앱 코드에 옛 말이 남은 곳은 주석 한 줄(`evalset/pick.py:9`)뿐 | 화면 · 보고서에 한국어 이름을 **새로 넣지 않는다**(문구를 지어 넣지 않는다) — 한국어 이름이 필요한 자리가 생기면 `key_table.KIND_KO` 를 함께 쓴다. 주석 한 줄만 고친다 |
| 허브 구멍 셋의 앱 쪽 — 고민 RQ1 · 자손 층 표지 · 고민 + 부위 한 조회 · 구멍 묶음 10 | §3-1 BR1 · §3-2 RQ1 아래 불릿 셋 · §9-3d · §9-5 KF2 | **없음**(고민 + 부위 한 조회만 이미 있음 — `walk/calls.py:177-180`) | WP-2 · WP-3 · WP-4 |
| 사용자가 정할 것 U-1 · U-2 | §11 맨 위 표 | 세트 칸 — **없음** | WP-1 |
| (끌어낸 것 ①) G14 의 근거 = G4 | §4 G14 | **이미 있음**(G13 과 같은 자리) | 없음 |
| (O-29 ④) 공통 답 지시가 바뀌어 0.5.1 까지의 runs 와 프롬프트가 다르다 | §11 O-29 | 코드 없음 | WP-6 보고에 한 줄(앞 판 기록과 견줄 때 주의) |

**완료 조건**: 위 표의 「확인 필요」 · 「확인만」 줄이 전부 「이미 있음 · 파일:줄」 또는 「고침 · 파일:줄」 로 채워져 보고에 실린다 · 고친 것이 있으면 그 시험 이름.

**검증**: `uv run pytest tests/test_walk_material.py tests/test_quality.py tests/test_key_fix1.py -q`.

## 8. WP-6 — 실물 확인 · 마감(허브 뒤)

**전제**: 새 허브가 18106 에 떠 있다. 앱 화면 확인은 18221. Jev 키 · CLI 구독은 앱 `.env` · 로컬 로그인(워커는 `.env` 를 열지 않는다 — 없으면 「못 돌림」 으로 보고하고 코디가 돌린다).

**먼저**: `HUB_REST_URL=… uv run python -m clinic_chat.clients.hub_rest --ping` 으로 실물 `concern_candidates`(물려받은 응답 · `site` 를 건 응답) · `facets`(하위 role · 계열) · `coverage`(고민 노드)의 **키 집합을 WP-2 의 모의와 대조**한다 — 다르면 모의를 고치고 WP-2 시험을 다시 돌린다.

| # | 문항(문장은 `$W/work-v052-instructions.md` 「쓸 것」 WORK-008 줄의 순서 그대로 · 여기는 꼴과 코드만) | 열 | 보고에 적을 것 | 기대 |
|---|---|---|---|---|
| F1 | e2e 피드백 4 의 꼴 — 윗고민 `CON-001` + 부위 `SITE-014` | `b` · `c` | **B · C 종료 상태** · **나온 시술 수**(답 재료의 서로 다른 `procedure_code` 수 · 답에 이름이 나온 시술 수 — ① D3 식) · `front.targets[]` · 읽은 조회와 `counts.by_site_match` · 재료의 `site_match` 표지 수(두 값 따로) · 입력 KB · 첫 답 글자 ms | 「근거 충족」 · 재료 **73 행 · 묶음 16**(글자 일치 24 · 묶임 54 · 겹침 5) · 0.5.1 의 run(`53da717fd7a6` — 묶음 2)보다 시술 수가 는다 |
| F2 | Q10 의 꼴을 자유 질문으로 — 행 0 인 고민 `CON-012` + 종류 `indication` | `b` · `c` | 같음 + `required[].met_by` · 윗고민 코드 · `ledger_check[]` · 답이 「윗고민의 것」 으로 밝혔나(눈으로 — 채점하지 않는다) | 「근거 충족」(「원천 미확정 (가)」 **아님**) · `met_by` = `inherited` · 윗고민 = `CON-008` · 묶음 65 · `LCK-010` 이 trace 에 |
| F3 | Q12 의 꼴 — 계열 `M2` + 사건 `ADV-051` × `adverse`(`--set-id Q12`) | `b` · `c` | 같음 + `depth` ≥ 2 인 재료 행 수 · 그 행의 거친 층 표지 · 표본 4 가 재료에 있나 · 물은 시간 칸이 빈칸인 것을 답이 어떻게 말했나 | 「원천 미확정 (다)」 그대로 · 표본 4/4 · 케이스 행이 「어느 시술의 케이스」 표지와 함께 |
| F4 | e2e 피드백 5 의 꼴 — 직접 행이 적고 하위 고민 행이 많은 윗고민(코드는 `resolve` 결과로 보고) | `b` · `c` | **B · C 종료 상태 · 나온 시술 수** · 재료 행의 `concern_match` 값별 수 | 종료 상태 · 시술 수를 **기록만** — 하위 고민을 어떻게 묶어 말하나는 이 판에서 정하지 않는다(O-31). 0.5.1 의 run(`ce5d23661812` — 시술 10)과 나란히 |

- 실행: `HUB_REST_URL=… HUB_GOLD_MCP_URL=… uv run python -m clinic_chat.runner --question "<문장>" --columns b,c`(F3 은 `--set-id Q12`). 문항마다 1 회 — 단건이라 편차가 크다는 것을 보고에 밝힌다. effort 는 속도 탭 조건(`low`).
- 기대와 다르면 **코드를 그 문항에 맞춰 고치지 않는다**(규칙은 일반 규칙이어야 한다 — `_RESUME` §1 e2e 피드백 3) — trace 를 붙여 보고한다.
- **N-3 을 여기서 본다**: F3 또는 따로 한 건(계열 → 시술 → 제품 → 제품 — 「제품의 하위 제품」 을 거치는 길)에서 답이 그 행을 「그 제품 아래 제품의 것」 으로 읽게 하는 표지가 재료에 있는지(G4) 한 줄 보고. 답 문장은 채점하지 않는다.
- 실물을 못 돌린 문항은 「미완료」 로 보고한다 → 코디가 돌린다(WORK-006 때와 같은 길).
- 마감: `uv run ruff check .` · **전체 `uv run pytest -q` 한 번**(기준선 163 · 1 과 나란히 — 더한 시험 수 · 고친 시험 이름) · `batch --check` · `loader --validate`(85) · 18221 화면에서 F2 를 한 번(정확도 탭 · 기록 다시 보기 — 옛 줄 하나 포함) · README 「실행 안내」 의 허브 전제 줄(0.5.2 — `concern_site.csv`)을 고침 · 커밋 후보 grep(시술 · 고민 · 부위 이름 · 질문 문장 · 실제 `gid` · LCK id · 홈 경로 · 키 꼴 0 — 시험의 가짜 코드는 예외).
- **하지 않는 것**: 전체 batch · 채점(키 미확인) · `--confirm` · 18105 · 18220 재시작 · 18106 내리기(코디가 내린다) · 커밋.

## 9. 순서 · 의존 · 병행

```
허브(WORK-007)  WP-1 ─ WP-2 ─ WP-3 ─ WP-4 ─ WP-5 ──┐(18106 에 새 허브)
앱(WORK-008)   WP-1 ─┐                              │
               WP-2 ─┼───────────────────────────── ┼─ WP-3(다시 뽑기 · 대조) ─ WP-6(실물)
               WP-5 ─┘        WP-4(코드) ───────────┴─ WP-4(후보 뽑기)
```

| 무엇 | 근거 |
|---|---|
| **허브 먼저** — 앱의 답 키 다시 뽑기는 허브 뒤 | 지시(`$W/work-v052-instructions.md` 「순서」) · KF2 의 대조는 새 허브의 응답이 있어야 선다 |
| 앱 WP-1 · WP-2 · WP-5 는 허브를 기다리지 않는다 | 필요한 새 응답 꼴은 셋뿐이고 WORK-007 §8 에 고정돼 있다 |
| WP-3 의 (나) 는 WP-1 의 U-1 · U-2 를 **넣지 않은** 세트 사본으로 | 허브가 바꾼 것과 사용자 결정이 바꾼 것을 섞지 않는다(§5) |
| WP-3 는 WP-2 뒤 | 답 키와 B 가 같은 함수(`walk/required.py`) — 윗고민 행을 `inherited` 로 세는 것이 먼저 서야 Q10 의 `kinds_met` 이 선다 |
| 모의 ↔ 실물 꼴 대조 | WP-6 앞 `hub_rest --ping`(§8 「먼저」) |
| 바꿔 끼우기 | 허브 · 앱이 다 끝난 뒤 **코디가** 18105 · 18220 을 함께 새 코드로 다시 띄운다 → 사용자 `key-table.md` 확인 1회 |

## 10. 검수 지적 반영 — WARN 3 · NOTE 6(`review-spec-v052.md` §7)

| # | 지적(한 줄) | 이 문서에서 | 어디 |
|---|---|---|---|
| W-1 | T22 의 실물 기준 둘이 gold 와 다르다 | 허브 시험 쪽(WORK-007 §6). 앱은 구멍 묶음 HG3 후보를 「글자 일치 0 → 1 이상」 **37** · 「묶인 고민 자신」 **91** 로 뽑는다 | §6 표 1 |
| W-2 | 다시 세어 안 나오는 수 둘(케이스 끝 `g_pair` 129 · 97 짝 행 합 1,700) | 허브가 식과 함께 다시 센다(WORK-007 §7 마감 3). 앱은 SPEC §9-3d 「셈 근거」 칸의 129 를 문항 꼴의 근거로 쓰지 않고, HG2 (ii) 후보를 허브 응답으로 직접 센다 | §6 표 1 · 완료 조건 |
| **W-3** | §9-3d HG2 (iii) 「두 단 아래에만 상품」 은 허브 식으로 0 건 — 문항이 서지 않는다 | (iii) 을 실제로 있는 꼴 둘((iii-a) 계열 → 케이스의 부작용 · 회복 · (iii-b) 두 단 아래 제품 행)의 후보로 바꿔 뽑고, 고르는 것은 사용자 문항 확정 때 | §6 표 2 |
| N-1 | `descend` 입력 표 | 허브 쪽. 앱은 `descend` · `upper` 를 주지 않는다(기본값) | §4 표 1 |
| N-2 | 계열에 `하위 케이스` 만 주면 못 닿는다 | 앱 B 는 하위 셋을 다 준다(확인만 — `walk/ranges.py` 의 role 상수). C 는 허브 도구 설명으로 | §4 표 12 |
| N-3 | 「제품의 하위 제품」 을 거치는 13 짝은 한 방향 | 실물 확인에서 층 표지가 재료에 있는지 한 줄(G4) | §8 |
| N-4 | `steps` 2 는 지금 gold 에 없다 | 앱은 `steps` 값을 판정에 쓰지 않는다(기록만) — 모의에 2 를 한 건 넣어 깨지지 않는지만 | §4 완료 조건 1 |
| **N-5** | U-2 로 Q03 · Q05 의 기대 종류가 늘어 B 가 안 읽으면 빠짐으로 잡힌다 | 보고에 한 줄 · `key-table.md` 의 두 줄에서 보이는지 확인(코디가 사용자에게 함께 말한다) | §5 「(다) 뒤」 3 |
| **N-6** | U-3 을 (b) 로 정하면 HG1 묶음 (iii) 의 기대가 뒤집힌다 | **U-3 = (a) 로 닫혔다** — (iii) 의 기대 = 윗고민 행이 섞이지 않고 자기 행(계열 층)으로 답한다 | §6 표 4 |

## 11. 열린 것 · 이 문서를 쓰며 본 것(SPEC 은 고치지 않았다)

| # | 무엇 | 이 문서의 제안 | 상태 |
|---|---|---|---|
| **B-1** | **U-1 을 Q03 에 적을 칸이 없다.** 결정은 「Q03 은 계열 `M1` 쪽 `lineup` 만 남는다」 인데 세트 칸 `expected_kinds[]` 는 문항에 하나라 대상별로 못 가른다(`lineup` 은 대상 4표 전부에 조회가 있는 종류다 — KD4 로도 안 빠진다). SPEC §9-4 의 칸 목록에 대상별 칸이 없다 | 세트 선택 칸 `expected_kinds_by_entry{표:코드: kinds[]}` 를 더한다 — 있으면 그 대상은 그 종류만 · 없으면 `expected_kinds[]`. **채점 기준(키)만 바뀌고 B · C 는 안 바뀐다.** 다른 길: `lineup` 을 문항에서 통째로 빼고(Q03 도) 계열 쪽 하위 목록은 「물은 것」 에서 내린다 — 결정 문장과 다르므로 권하지 않는다 | **코디 확인**(새 세트 칸 — SPEC 되적기 후보). 답이 올 때까지 Q05 만 고치고 Q03 의 `lineup` 은 그대로 둔 채 보고한다 |
| B-2 | 자손 층 표지의 이름 — `depth` 는 이미 깊이 결정 표지다(`walk/material.py:60`) | `layer_depth`(몇 단) · `layer_via`(거친 층의 이름 — 이름을 얻었을 때만) | 구현 때 정함 |
| B-3 | 구멍 묶음 10 의 **문장 초안**을 워커가 쓸지 — 지시는 「draft 꼴만 · 문장은 사용자 확인」, 0.5.1 의 길 찾기 16 은 워커가 문장 초안까지 썼다(C-2) | **기본 = 꼴만**(`question` 비움 · `pick-holes.json`). 문장 초안까지 원하면 코디가 따로 지시 — 그때 `status: draft` 로 `set.jsonl` 에 넣고 `BUNDLE_COUNTS` 를 95 로 | 코디 확인(기본값으로 진행) |
| B-4 | `via[]` 에 이름이 없다(SPEC-001 HG2-4) — 「어느 시술 아래의 케이스 것」 을 말하려면 이름이 있어야 한다 | 케이스는 기존 `speak_name` · 그 밖은 `label` 조회(§4 표 6). 허브가 `via[]` 에 `holder_name` 을 실어 주면 조회가 준다 — 계약 변경이라 이 판에서는 하지 않는다 | 구현 때 정함 — SPEC 되적기 후보(허브 `via[]` 에 이름) |
| B-5 | 윗고민으로 물려받은 행을 가르는 기준 | 응답 머리 `inherited_from`(§4 표 2) — 행의 `hier.match` 만으로 가르지 않는다 | 구현 때 정함 |
| B-6 | WP-3 (가) · (나) 보관 폴더 이름 · 대조 스크립트 꼴 | `_v052a/`(다시 뽑기 앞 키) · `_v052b/`(걸음 (나) 의 세트 사본 · 키) · `answer_key --diff` · `key-diff-v052.md` | 구현 때 정함 |
| B-7 | 구멍 묶음의 `source` · `id` 이름 | `source` = 「구멍」 · `id` = `H01` ~ `H10` | 구현 때 정함(O-11 과 같은 갈래) |
| O-29 | 0.5.2 에서 되적은 이름 · D11 의 한계 · 프롬프트가 0.5.1 runs 와 다름 | 본문 그대로 — ④ 는 WP-6 보고에 한 줄 | 구현 때 정함 · 1회차 trace 뒤 · 프롬프트 확인 때 |
| O-30 | 구멍 묶음 문항 수 3 · 3 · 4 · HG1 (iii) 의 기대 | 본문 그대로(U-3 = (a)) · HG2 (iii) 은 W-3 대로 후보 둘 | 추가 문항 확인 때 |
| O-31 | 넓어진 행을 답이 어떻게 묶어 말하나(e2e 피드백 5) | **이 판에서 정하지 않는다** — F4 는 기록만 | 프롬프트 확인 때 |

**이번 판에 구현 대상이 아닌 것**: 답 프롬프트 문구 · 화면 문구 · 답 꼴(e2e 피드백 1 · 2 · 5) · 전체 batch · 채점 · 상담 설계.

## 12. SPEC-002 0.5.2 변경 절 ↔ WP 대응(미대응 0)

변경 기록 「결정 · 지시 → 문서 자리」 표의 행 순서 그대로.

| 변경(변경 기록의 행) | 절 | WP |
|---|---|---|
| W-1 읽을 종류 0 → 기본 묶음 | §3-1 KD6 | WP-5(이미 있음) |
| W-2 부위마다 조회 | §3-1 BR1 · TG6 | WP-5(이미 있음) |
| W-3 37 의 `expected_entries[]` = 명세 `entries` | §9-4 | WP-5(이미 있음) |
| N-2 `entry.by` = `noul` | §3-1 입구 고르기 | WP-5(이미 있음 — 확인만) |
| N-5 gold 표 이름을 LLM 에 안 보냄 | §3-2a | WP-5(확인 + 단언 한 줄) |
| B-1 `purpose` = `label` | §7-3 | WP-5(이미 있음) · WP-2 표 6(같은 길을 자손 층 이름에 쓴다) |
| B-2 「B 전체」 | §10-1 | WP-5(이미 있음) |
| 상품 셈 식 · 제품 offer `inherited` = 0 | §3-2 RQ1 아래 불릿 · 규모 불릿 | WP-2 표 11 · WP-5 |
| G13 · G14 시간 섞기 | §4 표 · K4 | WP-5(이미 있음) |
| D11 | §8-2 | WP-5(이미 있음) |
| ② 채점 입력 `kinds_met` · 정답 꼴 둘 | §8-3 | WP-5(이미 있음 — `judge.md` 확인) |
| `lineup_rows[]` · `kinds_met[]` · `scope` 가 명세에 듦 · 세트 칸 셋 · 세트 확정값이 초안을 이김 | §9-4 · §9-5 KF1 ~ KF5 | WP-5(이미 있음) · WP-1 표 3(로더가 세트 칸을 앎) |
| 화면 말 「적응」 → 「어디에 쓰나」 | §3-2a 불릿 · §9-5 KF5 | WP-5(답 키 표 이미 있음 · 화면 · 보고서는 한국어 이름 자리 없음) · WP-3(`key-table.md` 다시) |
| 허브 구멍 셋의 앱 쪽 — 고민 대상의 RQ1 | §3-2 RQ1 아래 첫 0.5.2 불릿 | WP-2 표 2 ~ 5 |
| 허브 구멍 셋의 앱 쪽 — 「하위 *」 = 자손 전부의 층 표지 | §3-2 RQ1 아래 둘째 0.5.2 불릿 | WP-2 표 6 · 7 · 9 |
| 허브 구멍 셋의 앱 쪽 — 고민 + 부위는 한 조회 · `site_match[]` 표지 | §3-1 BR1 | WP-2 표 8 ~ 10 |
| 허브 구멍 셋의 앱 쪽 — 구멍 묶음 10 문항 | §9-3d | WP-4 |
| 허브 구멍 셋의 앱 쪽 — 키 전용 기준 대상을 빼고 대조 | §9-5 KF2 | WP-3 |
| 사용자가 정할 것 U-1 · U-2 | §11 맨 위 표 | WP-1 · WP-3 (다) |
| (끌어낸 것 ①) G14 의 근거 | §4 G14 | WP-5(이미 있음) |
| (끌어낸 것 ②) KF2 를 규칙으로 | §9-5 KF2 | WP-3 |
| (끌어낸 것 ③) U-2 를 사용자 결정으로 | §11 U-2 | WP-1 · WP-3 (다) 2 · 3 |
| (고치지 않은 것) 답 프롬프트 · 화면 문구 · e2e 피드백 1 · 2 · 5 의 답 꼴 | O-31 | 구현 대상 아님(§11) — F4 는 기록만 |
| O-29 ④ 프롬프트가 0.5.1 runs 와 다름 | §11 O-29 | WP-6 보고 한 줄 |
| O-30 구멍 묶음 문항 수 | §11 O-30 | WP-4 |

## 변경 기록

### 0.1.0 (2026-11-17)

- 새로 씀 — SPEC-002 0.5.2 의 변경 절을 WP 여섯으로. 사용자 결정 U-1 · U-2 는 추천으로 닫힌 값으로 적었다(_RESUME §2 11-17). 되적기 줄마다 코드를 열어 「이미 있음 · 파일:줄」 을 달았다(§7). `review-spec-v052.md` §7 의 WARN 3 · NOTE 6 을 §10 에 한 줄씩 넣었다 — 앱에 닿는 것은 W-3(구멍 묶음 HG2 (iii) 꼴) · N-5 · N-6 이다. **U-1 을 Q03 에 적을 세트 칸이 없다는 것을 찾았다**(§11 B-1 — 코디 확인).
