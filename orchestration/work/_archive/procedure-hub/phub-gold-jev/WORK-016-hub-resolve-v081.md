---
type: work
id: WORK-016
title: "허브 resolve 0.8.1 구현 계획 — 맞춤 꼴 = 정확한 이름 → 코드 · 부분 · 줄임 · 덮임 지움 · 입력 abbr 없앰 · 도구 설명 · REST = MCP · 고칠 · 지울 시험"
status: draft
product: procedure-hub
feature: phub-gold-jev
version: 0.1.0
created_at: 2026-11-18
updated_at: 2026-11-18
tags:
  - product/procedure-hub
  - feature/phub-gold-jev
  - doc/work
  - status/draft
links:
  specs:
    - "orchestration/work/phub-gold-jev/SPEC-001-hub-gold-mcp.md (0.8.1 — §4-1 · §5-1 R1 ~ R9 · §5-11 NM 지움 · §3-1 · §9 T15 · T23 · T26 · T27 · T29 · §10 O-32 · 변경 기록 0.8.0 「남길 것 · 지울 것」 · 0.8.1 「고칠 · 지울 허브 시험」) ← 계약"
    - "orchestration/work/phub-gold-jev/SPEC-003-hub-gold-db.md (§5 P1 메서드 수 · §7 DT9 · DT10 — 두 판)"
  decisions:
    - "orchestration/work/phub-gold-jev/_RESUME.md §2 (2026-11-18 — 「상담 입구 결정 표 D-1~D-15 확정」 D-1 · D-2 · 「허브 resolve = 최소 목록 꼴 · 규칙을 더하지 않는다」 · 「SPEC-008 검수 WARN 16 코디 답」(F-1 ⓒ · F-11 · 나머지 리포트대로) · 「SPEC-008 0.2.0 남은 정할 것 코디 답」)"
    - "orchestration/work/phub-gold-jev/work-016-017-brief.md (이 문서의 발주서)"
  related:
    - "orchestration/work/phub-gold-jev/WORK-013-hub-v07.md (앞 허브 WORK — 꼴 · 포트 · 실물 확인 절차)"
    - "orchestration/work/phub-gold-jev/WORK-017-consult-v04.md (앱 상담 0.4 — 같은 때 · 목록 꼴만 쓴다)"
---

# WORK-016 — 허브 `resolve` 0.8.1 구현 계획

> 경로 접두어: `W` = 이 폴더 · `H` = `~/orca/workspaces/PROCEDURE-HUB/phub-gold-jev`(HEAD `d97a9ad` · **이 위에 이어서 짓는다**) · `B` = `$H/backend` · `SM` = `$P/orchestration/work/_archive/procedure-hub/phub-ledger-redesign/silver-model`(gitignore · 로컬 데이터).
> **계약은 SPEC-001 0.8.1 이다**(0.8.0 의 규칙 · 응답 필드 + 0.8.1 의 영향 표 · 고칠 · 지울 시험 표 — 0.8.1 은 계약 변경 0). 이 문서는 「어느 파일을 · 어떤 순서로 · 무엇으로 확인하나」 만 정한다. SPEC 에 없는 동작을 만들지 않는다 — 어긋나는 것을 만나면 코드를 맞춰 고치지 말고 보고한다(§8).
> **다른 도구 8(`scope` · `neighbors` · `facets` · `concern_candidates` · `pair` · `evidence` · `health` · `coverage`)의 계약 · gold 15표 · `gold_hash` · 보조 입력 · `aux_hash` 는 한 글자도 바뀌지 않는다.** 적재를 다시 하지 않는다 · alembic 을 돌리지 않는다.
> 줄 번호는 `$B` `d97a9ad` 에서 이 워커가 읽은 것이다(읽기만).

## 0. 요약

- 만드는 것: `resolve` **맞춤 꼴** = 입력 `text` 전체의 `norm` 이 `g_entry.norm` 과 **같을 때만** 후보(R2). 부분 일치 · 덮임(`covered_by`) · 줄임(NM · `how` · `full`) · `matched.start` 를 지운다. 입력 `abbr` 은 **없앤다** — 주면 `invalid_argument`(O-32 (a)). 목록 꼴은 머리 `request.abbr` 칸이 없어지는 것 하나 말고 그대로다.
- WP 넷: **WP-1** 맞춤 꼴 · 색인 · repository → **WP-2** 입력 `abbr` 처분 · REST · MCP · 도구 설명 · swagger → **WP-3** 고칠 · 지울 시험(SPEC-001 0.8.1 표 8 파일 + 이 워커가 grep 으로 더 찾은 3 파일) → **WP-4** 두 판 · 실물 18107 · 마감. 순서대로(한 워커 · 직렬).
- **시험 규칙**(`_RESUME` §2 11-17 「시험은 구현한 것만 돌림 · 전체 테스트 안 돌림」 — 지금도 유효): WP 마다 **그 WP 의 「돌릴 파일」 만** · 전체 pytest(`uv run pytest --ignore=tests/integration`) 금지 · 돌린 파일 · 통과 · skip · 지운 시험 수를 보고에 적는다.
- 실물은 **18107 만** 워커가 띄웠다 내린다. **18105 재시작은 코디 몫**(앱 0.4 와 같이 — WORK-017). 허브 브랜치 커밋도 코디.

## 1. 지금 코드(`$B` · `d97a9ad` · 읽기만)

| 파일 | 지금(0.7.2) | 이번에 |
|---|---|---|
| `app/modules/gold/resolve.py`(137) | 머리말 R7 · NM 설명(`:6-12`) · `ABBR_MODES`(`:26`) · `__all__` 에 `ABBR_MODES` · `HOW_ABBR` · `HOW_PART`(`:24`) · `resolve(…, abbr)`(`:34-35` · `:39` `ctx.enum(abbr, …)`) · `_positions`(`:52`) · `_covered_by`(`:61-72`) · `_match(ctx, text, rng, abbr)`(`:74-113` — `entry_norms()` 를 돌아 부분 일치 · `abbr_keys()` · `entries_by_abbr()`(`:86-92`) · `matched{span, start, covered_by, how[, full]}`(`:108-110`) · `request.abbr`(`:112`)) · `_listing(…, abbr)`(`:116-118` — `request.abbr`) | WP-1 · WP-2 |
| `app/modules/gold/memory.py` | `abbr_keys_of`(`:35`) · 적재 때 줄임 열쇠 색인 `entry_by_abbr` · `abbr_keys`(`:66-71`) · `entry_by_norm` | WP-1 — 줄임 열쇠 함수 · 색인 지움(`entry_by_norm` 은 그대로 — R2 가 이것 하나로 찾는다) |
| `app/modules/gold/repository.py` | Protocol `abbr_keys()` · `entries_by_abbr(key)`(`:48-49`) · 구현(`:124-130`) | WP-1 — 두 메서드 지움(Protocol 메서드 수 −2 · SPEC-003 §5 P1 되적기 후보 → §8 A-1) |
| `app/modules/gold/headers.py` | `MATCHED_FIELDS = ("span", "start", "covered_by", "how")`(`:112`) · `MATCHED_ABBR_FIELDS`(`:113`) | WP-1 — `MATCHED_FIELDS = ("span",)` · `MATCHED_ABBR_FIELDS` 지움 |
| `app/modules/gold/service.py` | `resolve(…, abbr)`(`:63-64`) | WP-2 — `abbr` 인자 처분(§4) |
| `app/router/gold.py` | `/resolve` 의 쿼리 `abbr`(`:54`) · `svc.resolve(…, abbr=abbr)`(`:58`) | WP-2 |
| `app/modules/gold/mcp_server.py` | `DESCRIPTIONS["resolve"]`(`:34-42` — 부분 · 덮임 · 줄임 · `matched{span, start, covered_by, how, full}` 문장) · 도구 함수 `resolve(…, abbr)`(`:156-158`) | WP-2 — 설명 · 입력 스키마 |
| `app/swagger_docs/gold.py` | `resolve` 불릿 둘(`:14-15` — 부분 일치 · `covered_by` · `abbr`) | WP-2 — 문구만 |
| 그 밖(`concern.py` · `facets.py` · `pairs.py` · `coverage.py` · `core.py` · `cursor.py` · …) | — | **안 고친다** |

grep(이 워커 · `$B` · `rg -n "abbr" app`): `app/` 안 `abbr` 이 나오는 파일 = `resolve.py` · `memory.py` · `repository.py` · `service.py` · `router/gold.py` · `mcp_server.py` · `swagger_docs/gold.py` **7** — 위 표가 전부다. `covered_by` · `"how"` · `"full"` 계산 필드는 `resolve.py` · `headers.py` · `mcp_server.py` · `swagger_docs/gold.py` 에만 있다. 구현 워커는 WP-2 끝에 `rg -n "abbr|covered_by|HOW_ABBR|HOW_PART|entry_by_abbr|abbr_keys" app` 가 **0** 인지 본다(§6 완료 조건 3).

## 2. 공통

| 항목 | 이번 판 |
|---|---|
| allowed_paths(허브 레포) | **고치는 파일**: `backend/app/modules/gold/{resolve,memory,repository,headers,service,mcp_server}.py` · `backend/app/router/gold.py` · `backend/app/swagger_docs/gold.py` · `backend/tests/{gold_fixture,test_gold_contract,test_gold_tools_synthetic,test_gold_mcp,test_gold_v07_compat,test_medallion_repo,test_gold_coverage,test_gold_real}.py` · `backend/README.md`(gold 절의 `resolve` 줄만) / **지우는 파일**: `backend/tests/test_gold_v07_resolve.py` / **새 파일**: 없음(새 시험은 기존 파일의 T15 · T29 자리에 — §5) |
| 손대지 않는 것 | `backend/app/main.py` · `backend/app/core/**`(`test_gold_rest.py` 가 막는다) · `app/model/**` · `alembic/**` · `scripts/**` · `gold_main.py` · `config.py` · `inputs.py` · `db_inputs.py` · `medallion_load.py` · `concern.py` · `descend.py` · `facets.py` · `pairs.py` · `coverage.py` · `core.py` · `cursor.py` · `kinds.py` · `ledger.py` · `ranges.py` · `closure.py` · `pyproject.toml` · `uv.lock`(새 의존 0) · `.github/**` · **다른 도구 8 의 시험 파일**(`test_gold_holes.py` · `test_gold_v07_descend.py` · `test_gold_v07_site.py` · `test_gold_load.py` · `test_gold_rest.py`) |
| 데이터 | 로컬 `$SM/gold` · `$SM/silver` · `$SM/notes/ledger-check-list.csv`. CSV · 응답 dump 를 허브 레포에 넣지 않는다(대조 응답은 세션 임시 폴더) |
| 시험 | ① WP 마다 「돌릴 파일」 표의 파일만 ② 전체 pytest 금지(WP-4 에서도) ③ 명령 꼴 `DATABASE_URL=sqlite+aiosqlite:///:memory: uv run pytest <파일들> -q -rs`(README) — 실물 시험(`@needs_gold`)은 데이터 env 넷을 준 채 돌린다(없으면 skip — skip 수를 보고) ④ `uv run ruff check <고친 파일들>` 만 |
| 포트 | 시험은 포트 없이(ASGI transport). 서버 확인은 **18107 만** — 띄우기 전 `lsof -nP -iTCP:18107 -sTCP:LISTEN`(비어 있지 않으면 **멈추고 보고**). **18105 · 18106 · 18222 · 18224 · 18432 를 내리거나 띄우지 않는다.** 18105 에는 GET 읽기만. 자기가 띄운 PID 만 내린다(`pkill` · 포트로 죽이기 금지) |
| 접속 값 | DB 판 확인(§6 ③)에만 — 코디가 정한 방법 그대로(레포 밖 접속 값 파일을 `set -a; . <파일>; set +a` 로 프로세스 env 에만 · `cat` · `echo` 금지 — `_RESUME` §2 11-17 「WORK-010 B 코디 답」 B-1) |
| 커밋 | **안 한다** — 워크트리에 변경만 남긴다(허브 브랜치 커밋은 코디) |

## 3. WP-1 — 맞춤 꼴 = 정확한 이름 · 색인 · repository

**SPEC**: §4-1 입력 표 · 계산 필드 표 · 「없앤 계산 필드」 · 순서 불릿 · §5-1 R1 · R2 · R5 · R6 · R7(지움) · R8 · R9(지움) · §5-11 「NM — 0.8.0 에서 지움」 · §3-1 「줄임 열쇠 — 0.8.0 에서 없앴다」 · 변경 기록 0.8.0 「남길 것 · 지울 것」 표 · 부록 A.

| 만들 · 고칠 것 | 어디 | 내용 |
|---|---|---|
| 맞춤 | `resolve.py` `_match` | `q = norm(text)`(R1 식 그대로 — `norm` 함수는 안 고친다). 후보 = `ctx.repo` 의 `norm` → 행 색인으로 **`q` 와 같은 `norm` 의 행만**(부분 문자열로 훑지 않는다 · `entry_norms()` 를 도는 반복 지움). 같은 (`entity_table`, `entity_code`) 는 한 번(`gold-build.py:636-641` 과 같은 규칙 — 지금 코드의 중복 제거 식 그대로) |
| `matched` | 같은 곳 · `headers.py` | 맞춤 꼴 후보마다 `matched = {"span": <그 행의 norm>}` **하나**(= `q`). `start` · `covered_by` · `how` · `full` 은 싣지 않는다. `headers.MATCHED_FIELDS = ("span",)` · `MATCHED_ABBR_FIELDS` 지움 |
| 순서 | `_match` 정렬 키 | 표 순서(`_order_key` 의 `gold-build.py:633-634` 순서) → `name_kind` = 「이름」 먼저 → `gid`. `range` 를 줬으면 `in_range` 참이 앞(그대로). 「긴 조각 먼저」 · 「같은 길이에서 `부분` 먼저」 키는 지운다 |
| 머리 `ambiguous` | 같은 곳 | 그 `norm` 의 개념이 2 이상인가(뜻 그대로 — 조각이 하나) |
| 후보 0 | 같은 곳 | `200` · `candidates` = `[]` · `total` 0 (R5 — 문장 · 조사 붙은 이름 · 일부 · 이어 쓴 글 · 오타 → 0) |
| 지울 함수 | `resolve.py` | `_positions` · `_covered_by` · 줄임 맞춤 가지(`:86-92`) · 머리말 R7 · NM 문단(`:6-12` → 0.8.0 한 줄 「R2 정확 일치 — 문장에서 찾지 않는다(SPEC-001 0.8.0)」) · `HOW_ABBR` · `HOW_PART` |
| 색인 | `memory.py` | `abbr_keys_of`(`:35`) · `entry_by_abbr` · `abbr_keys`(`:66-71`) 지움. `entry_by_norm`(맞춤이 쓰는 색인)은 그대로. 두 판(CSV · DB)이 같은 `GoldMemory` 코드로 짓는다 — 한 곳에서 지우면 두 판에서 함께 없어진다(SPEC-001 §5-11 「두 판」) |
| repository | `repository.py` | Protocol `abbr_keys` · `entries_by_abbr`(`:48-49`) · 구현(`:124-130`) 지움. `_match` 가 `norm` 색인을 읽는 메서드가 지금 있으면(`entries_by_norm` 꼴) 그것을 쓴다 — **없으면 새 메서드를 더하지 말고 보고**(§8 A-2) |

**완료 조건**(T15 · T26 의 남는 확인 · T27 의 `resolve` 줄)
1. 합성: 이름 · 별칭 글자 그대로 → 그 개념 · 띄어쓰기 · 대소문자를 바꿔도 같은 후보(R1) · **이름이 든 문장 · 조사가 붙은 이름 · 이름의 앞이나 뒤 일부 · 두 이름을 이어 쓴 글 → 후보 0**(`200` · 빈 목록) · 같은 `norm` 개념 둘(합성 「겹침」 → `PRC-902` · `CON-904`) → 둘 다 + `ambiguous` 참 · `range` 를 주면 `in_range` 가 앞이고 버리지 않는다.
2. 응답 어디에도 `matched.start` · `covered_by` · `how` · `full` · `particle` 이 없다 · `matched` 키 = (`span`,) · `span` = 입력의 `norm`.
3. 낱말 둘 이름의 앞 낱말을 줄인 글(띄어 쓴 꼴 · 붙여 쓴 꼴) → **후보 0**(옛 NM 이 맞추던 꼴 — T26 남는 확인).
4. 적재 뒤 `repo._m` 에 `entry_by_abbr` · `abbr_keys` 가 없다 · repository 에 `abbr_keys` · `entries_by_abbr` 가 없다(두 판).
5. **실물**(데이터 env): 서로 다른 `norm` 마다 직접 센 개념 집합 = `resolve(text=<그 norm 의 한 행 text>)` 의 후보 집합(T15 「`norm` 2,541 마다 직접 센 것과 같다」 — 데이터 판이 바뀌었으면 그 판의 수를 보고) · 겹치는 `norm` 수(0.8.0 문서 99)도 센다.

**돌릴 파일**: §5 의 WP-3 표가 이 WP 의 기대를 바꾸므로 **WP-1 은 시험을 고친 WP-3 뒤에 같이 돈다**(WP-1 · WP-2 만 끝난 상태에서는 아래 셋만 돌려 깨지는 자리를 보고에 적는다 — 고치지 않는다): `tests/test_gold_tools_synthetic.py` · `tests/test_gold_contract.py` · `tests/test_medallion_repo.py`.

## 4. WP-2 — 입력 `abbr` 처분 · REST = MCP · 도구 설명 · swagger

**SPEC**: §4-1 「0.7 의 입력 `abbr` 은 없앴다 — 주면 `invalid_argument`」 · 불릿 「MCP 도구 설명에 문장 하나」 · §4-0(오류 꼴) · §10 O-32 (a) · §9 T29.

| 만들 · 고칠 것 | 어디 | 내용 |
|---|---|---|
| 입력 `abbr` | `resolve.py` `resolve()` | 서명에서 `abbr` 을 빼지 **않고** 「주면 `invalid_argument`」 로 받는다: `abbr` 이 `None` 이 아니면 `invalid_argument: abbr`(오류 글 꼴은 `ctx` 의 다른 입력 오류와 같은 식 — 지금 `ctx.enum` 이 내는 꼴을 따른다). 목록 꼴 · 맞춤 꼴 둘 다. `ABBR_MODES` 지움 |
| `request` | `_match` · `_listing` | `request` 에서 `abbr` 키를 지운다 — 맞춤 꼴 · 목록 꼴 둘 다(O-32 — cursor 는 `request` 로 서명하므로 0.7.2 가 낸 cursor 를 0.8.1 이 받지 않는다 · 그대로 둔다) |
| 서비스 | `service.py:63-64` | `abbr` 인자를 그대로 `_resolve` 에 넘긴다(검사는 `resolve.py` 한 곳) |
| REST | `router/gold.py:54-58` | 쿼리 `abbr` 을 **남기되** 설명을 「0.8.0 에서 없앰 — 주면 `invalid_argument`」 로 · `svc.resolve(…, abbr=abbr)` 그대로. 까닭: 쿼리 자체를 지우면 FastAPI 가 모르는 쿼리를 버려 `abbr=x` 가 200 이 된다 — SPEC 「주면 `invalid_argument`」 와 갈린다(§8 A-3). 상태 코드는 다른 `invalid_argument` 와 같은 값(지금 422 — `test_gold_mcp.py` `ERRORS` 표가 그 값이다) |
| MCP | `mcp_server.py:156-158` | 도구 함수의 `abbr` 인자도 같은 이유로 남긴다(입력 스키마에 `abbr` 이 남는다 — 설명은 「없앰 · 주면 `invalid_argument`」). **REST = MCP**: 같은 입력 → 같은 JSON · 같은 오류 글(T7 · T29) |
| 도구 설명 | `mcp_server.py` `DESCRIPTIONS["resolve"]`(`:34-42`) | **새 문장**(T29 · SPEC §4-1 그대로): 「`text` 는 이름 하나다 — 문장을 넣으면 후보가 0 이다. 문장에서 입구를 찾으려면 목록 꼴로 입구를 받아 고른다」. 지울 것: 부분 문자열 · 덮임(`covered_by`) · 줄임 · `matched{span, start, covered_by, how, full}` · 「조사를 떼지 않는다」 · 「긴 조각 먼저」 문장. 남길 것: 목록 꼴(`range` · `tables` · 쪽 넘김) 설명 · 「고르지 않고 전부」(겹침 — R6) · `matched{span}` 한 마디 |
| swagger | `swagger_docs/gold.py:14-15` | `resolve` 불릿을 0.8.0 뜻으로(정확한 이름 → 코드 · 문장이면 후보 0 · 목록 꼴 · `abbr` 없앰). 문구만 |
| README | `backend/README.md` gold 절 | `resolve` 를 설명하는 줄이 있으면 0.8.0 뜻으로 한 줄(없으면 안 고친다) |

> **A-3 대안**(구현 워커가 정하지 않는다 — 코디): (b) 서명 · 스키마에서 `abbr` 을 지우고 모르는 입력을 받는 쪽에 맡긴다 — MCP 는 스키마 밖 인자를 오류로, REST 는 무시로 받아 **REST ≠ MCP** 가 된다. 본문 = (a) 남기고 오류로.

**완료 조건**
1. `resolve(text="겹침", abbr="on")` · `abbr="off"` · `abbr="x"` · `resolve(range="시술", abbr="off")` → 넷 다 `invalid_argument`(REST · MCP 같은 오류 글 · REST 상태 코드 = 다른 `invalid_argument` 와 같음).
2. 맞춤 꼴 · 목록 꼴 응답의 `request` 에 `abbr` 키가 없다.
3. `tools/list` 의 `resolve` 설명에 새 문장(「이름 하나」 · 「문장을 넣으면 후보가 0」 · 「목록 꼴」 조각)이 있고 「부분 문자열」 · 「조사를 떼지 않는다」 · 「covered_by」 · 「줄임」 · 「how」 조각이 없다.
4. `rg -n "abbr|covered_by|HOW_ABBR|HOW_PART|entry_by_abbr|abbr_keys" app` 의 남는 줄 = **`resolve.py` 의 `abbr` 거절 검사 · `router/gold.py` · `mcp_server.py` 의 `abbr` 인자 · 설명 줄뿐**(그 밖 0).

**돌릴 파일**: WP-3 과 함께(위 WP-1 과 같은 까닭).

## 5. WP-3 — 고칠 · 지울 시험

**SPEC**: 변경 기록 0.8.1 「고칠 · 지울 허브 시험」 표(8 파일) · 그 아래 불릿 「이 표 밖에서 맞춤 꼴에 문장을 넣는 곳이 더 나오면 같은 처분 — `rg -n 'resolve\(' backend/tests` 로 전수를 다시 센다」.

**전수 grep**(이 워커 · `$B` · `d97a9ad`):
- `rg -n "resolve\(" tests` 가 나오는 파일 13 — 그 가운데 `Path(...).resolve()` 만인 6(`legacy_corpus_support` · `test_ai_usage` · `test_medallion_image` · `test_medallion_load` · `test_medallion_model` · `test_gold_rest` 의 76 · 82 행) · 다른 모듈 `EntityResolver().resolve`(`test_retrieval_domain.py` — `app/modules/retrieval` · gold 아님) 1 을 빼면 **gold `resolve` 를 부르는 시험 파일 = 7**: `test_gold_contract` · `test_gold_coverage` · `test_gold_real` · `test_gold_rest` · `test_gold_tools_synthetic` · `test_gold_v07_compat` · `test_gold_v07_resolve`.
- `rg -n "abbr" tests` → 5 파일(`test_gold_contract` 1 · `test_gold_mcp` 2 · `test_gold_v07_compat` 9 · `test_gold_v07_resolve` 29 · `test_medallion_repo` 2).
- `rg -n 'covered_by|\["how"\]|"full"|MATCHED_ABBR' tests` → `test_gold_tools_synthetic` · `test_gold_v07_compat` · `test_gold_contract` · `test_medallion_repo` · `test_gold_v07_resolve`.
- 합치면 **9 파일**: SPEC-001 0.8.1 표의 8 줄 = 7 파일(`test_gold_contract` · `test_gold_v07_resolve` · `test_gold_v07_compat` · `test_gold_tools_synthetic` · `test_gold_mcp` · `test_medallion_repo` · `gold_fixture` — 표는 `test_gold_mcp` 를 두 줄로 적었다) **+ 표 밖 파일 2**(`test_gold_coverage` · `test_gold_real`). 표의 파일 안에서도 자리가 빠진 곳이 셋 있다(`test_gold_contract.check_response` · `test_gold_v07_compat.test_T27_tools_list_and_rest_equals_mcp` · `test_medallion_repo.SAME_V07_PATHS`). 표 밖 자리는 모두 아래 ★ 6(H-2 · H-7 · H-12 · H-14 · H-15 · H-16). `test_gold_rest.py:40` 의 `("/resolve", {"text": "시술가"})` 는 합성 이름 하나(`PRC-901` 의 `entity_name`)라 0.8.0 에서도 후보가 그대로 — **안 고친다**.

### 5-1. 고칠 · 지울 시험 표

「고침」 = 기대를 0.8.0 계약으로 바꿔 남김 · 「지움」 = 대상 규칙이 없어져 지움 · ★ = SPEC-001 0.8.1 표에 없던 자리(이 워커 grep — 같은 처분 규칙을 적용).

| # | 파일 | 함수 · 자리(줄 = `d97a9ad`) | 처분 | 새 기대 · 새 시험 |
|---|---|---|---|---|
| H-1 | `test_gold_contract.py` | `test_T3_real_response_fields`(241 ~ 262) — `resolve(text=q["entry_text"] or q["question"])`(245) · `resolve(text=q["question"])`(260) | **고침** | 245 = `entry_text` 가 있으면 그것 · 없으면 그 문항 기대 입구의 **이름**(`entity_name` — 문항 표 · 답 키 명세에서 읽는 칸이 없으면 그 문항은 이 단언에서 빼고 뺀 수를 보고) · 260 줄 = 이름 입력으로 바꾼다 · `seen > 0` 단언은 이름 입력이라 그대로 선다 |
| H-2 ★ | `test_gold_contract.py` | `check_response` 의 `resolve` 가지(93 ~ 96 — `MATCHED_ABBR_FIELDS if how == "줄임" else MATCHED_FIELDS`) · import(31 · 34) | **고침** | `matched` 가 있으면 `tuple(c["matched"]) == MATCHED_FIELDS`(= `("span",)`) · `MATCHED_ABBR_FIELDS` import 지움 |
| H-3 | `test_gold_v07_resolve.py` | 파일 전체 — `test_T26_*` **16 함수**(`keys_equal_independent_build` · `base_fixture_has_no_keys` · `abbr_matches_and_covers_last_word` · `one_word_prefix_no_candidate` · `no_match_shapes` · `abbr_inside_full_name_is_covered` · `short_abbr_inside_long_abbr` · `part_wins_and_not_repeated` · `one_key_two_concepts` · `same_span_part_first` · `matched_shape_and_order` · `abbr_off_is_06` · `abbr_off_base_same_as_on` · `abbr_invalid` · `tool_description_and_schema` · `real_counts_and_37_questions`) | **지움**(파일째) | 남는 확인 셋 → `test_gold_tools_synthetic.py` 에 새로(H-9): 줄인 글 → 후보 0 · `how` · `full` 없음 · 줄임 열쇠 색인 없음. `_abbr_invalid` 의 뜻(`abbr` → `invalid_argument`)은 H-10 으로 옮김 |
| H-4 | `test_gold_v07_compat.py` | `test_T27_resolve_abbr_off_06_shape`(79 ~ 88 — `abbr="off"` · `MATCHED_06` · `request.abbr == "on"`) | **지움** | T27 이 「`resolve` 맞춤 꼴은 0.6 과 같은 응답이 아니다」 로 이미 뺐다. 목록 꼴 `request` 에 `abbr` 없음은 H-11(T29)이 본다 |
| H-5 | `test_gold_v07_compat.py` | `test_T27_real_hash_and_06_shape`(120 ~ ) 의 `resolve(text=q["question"], abbr="off")`(129) | **고침** | `resolve` 줄만 빼고 남긴다(해시 · 다른 도구 0.6 꼴 대조는 그대로) |
| H-6 | `test_gold_v07_compat.py` | `test_T27_descriptions_three_sentences`(90) · `SENTENCES["resolve"]`(35 — 「글자 그대로 맞은 것이 아니라」) · `OLD_FRAGMENTS["resolve"]`(36 — 「고르지 않고」 · 「부분 문자열」 · 「조사를 떼지 않는다」) | **고침** | `SENTENCES["resolve"]` = T29 문장의 조각(「이름 하나」 · 「문장을 넣으면 후보가 0」) · `OLD_FRAGMENTS["resolve"]` 에서 「부분 문자열」 · 「조사를 떼지 않는다」 는 **없어야 하는 조각**으로 뜻을 뒤집거나 지운다(지금 그 표가 「남아 있어야」 인지 「없어야」 인지 읽고 맞춘다 — 「고르지 않고」 는 R6 이라 남는다) · `concern_candidates` 줄은 그대로 |
| H-7 ★ | `test_gold_v07_compat.py` | `test_T27_tools_list_and_rest_equals_mcp`(97 ~ 118) — `"abbr" in input_schema`(106) · `call_tool("resolve", {"text": "가나 마바사", "abbr": "on"})` · REST 같은 꼴(113 ~ 115 — `how == "줄임"` 단언) | **고침** | 106 = §4 (a) 에서 `abbr` 이 스키마에 남으므로 그 단언은 지우지 말고 둔다(A-3 이 (b) 로 바뀌면 뒤집는다) · 113 ~ 115 = 이름 하나 입력(`v07` 판의 합성 이름)으로 REST = MCP 를 보고 `how` 단언을 지운다 |
| H-8 | `test_gold_tools_synthetic.py` | `test_resolve_overlap_all_and_order`(36) · `test_resolve_one_per_entity_longest_span`(43) · `test_T15_covered_only_when_every_occurrence_covered`(83) | **지움** 셋 | — (뜻: 겹침 순서 · 긴 조각 · `covered_by` — 0.8.0 에 그 규칙이 없다. 단 36 의 「겹침 → `PRC-902` · `CON-904` · `ambiguous`」 는 H-9 가 0.8.0 꼴로 다시 본다) |
| H-9 | `test_gold_tools_synthetic.py` | `test_T15_resolve_wide_candidates`(64 ~ 80) · 도우미 `_brute`(50 — 부분 문자열 셈) | **고침** | 이름 → `test_T15_resolve_exact_name`(제안). 기대: 이름 · 별칭(`시술 가 별칭` → `PRC-901` · `matched` = `{span: "시술가별칭"}`) · 띄어쓰기 · 대소문자 = 같은 후보 / 문장(`"시술가 그리고 시술 가 별칭"`) · 조사 붙은 이름(`"시술가는"`) · 일부(`"시술"`) · 이어 쓴 글(`"재료가나효과가"`) → 후보 0 · `"겹침"` → 둘 + `ambiguous` · 순서 = 표 순서 → 「이름」 먼저 → `gid` · `matched` 키 = (`span`,) · `_brute` = `r["norm"] == norm(text)` 로 바꿈. **+ T26 남는 확인**(H-3 에서 옮김): 낱말 둘 합성 이름의 앞 낱말 줄인 글(띄어 · 붙여) → 후보 0 · 응답에 `how` · `full` 없음(`_no_key`) · `repo._m` 에 `entry_by_abbr` 없음 · repo 에 `abbr_keys` 없음. 합성 이름 · 글은 `gold_fixture.py` 에 이미 있는 것에서 고른다(새로 지으면 `v07` 판의 낱말 둘 이름) |
| H-9b | `test_gold_tools_synthetic.py` | `test_resolve_range_never_drops`(91) · `test_resolve_zero_is_200`(97) · `test_T13_resolve_listing`(102) · `test_T6_deterministic_paging`(343 — `("resolve", {"range": "시술"})`) | **그대로**(입력이 이름 · 없는 말 · 목록 꼴이다) — 돌려서 확인 | 91 의 순서 기대(`CON-904` → `PRC-902` · `in_range` 앞)는 0.8.0 에서도 같다 |
| H-10 | `test_gold_mcp.py` | `test_tool_list`(38)의 44 ~ 45 행 — 설명에 「고르지 않고」 · 「부분 문자열」 · 「조사를 떼지 않는다」 단언 | **고침** | 「고르지 않고」 는 남김(R6) · 「`text` 는 이름 하나다」 · 「문장을 넣으면 후보가 0」 있음 · 「부분 문자열」 · 「조사를 떼지 않는다」 · 「줄임」 없음(T29) |
| H-11 | `test_gold_mcp.py` | `SAME` 66 행(`{"text": "겹침 시술가", "abbr": "off"}`) · `ERRORS` 104 행(`{"text": "겹침", "abbr": "x"}` → 422) · `SAME_V07` 112 행(`{"text": "가나 마바사 어때"}`) | **고침** | 66 = `{"text": "시술가"}`(이름 하나 · `abbr` 뺌) · 104 = `abbr` 을 주면 0.8.0 `invalid_argument`(값 `x` 대신 `on` 으로 — 「값이 틀려서」 가 아니라 「입력이 없어져서」 오류임을 보인다 · 상태 코드 그대로) + `{"range": "시술", "abbr": "off"}` 한 줄 더함 · 112 = `v07` 판의 합성 **이름 하나**(낱말 둘 이름 그대로)로 바꿈 — H-12 가 이 표본의 자리 0 을 읽는다 |
| H-12 ★ | `test_medallion_repo.py` | `MEMORY_INDEXES` 의 `"entry_by_abbr"`(84) · `test_dt9_same_memory_index_v07`(96 ~ 101 — `len(entry_by_abbr) > 0` · `abbr_keys()` 같음) · `SAME_V07_PATHS[0] = ("how", "줄임")`(112) · `_path_ok` 의 `how` 가지(116 ~ 117) | **고침** | 84 = `entry_by_abbr` 뺌 · 100 = 「`entry_by_abbr` 속성이 두 판 모두 없다」 로 · 112 = 자리 0 의 표지를 `("total", 1)` 꼴(이름 하나 → 후보 하나 — H-11 의 112 행 표본)로 바꾸거나 자리 0 을 `SAME_V07_PATHS` 에서 뺀다(`_path_ok` 의 `how` 가지 지움) · `test_dt10_tool_responses_equal` · `_v07` 는 0.8.0 응답으로 그대로 돈다 |
| H-13 | `gold_fixture.py` | 합성 gold(121 ~ 126 — 「겹침」 `norm` 하나에 개념 둘 · 「시술 가 별칭」) · `v07` 판의 줄임 꼴 표본 행 · 머리말 5 행 | **고침(필요한 만큼)** | 「겹침」 · 「시술 가 별칭」 은 **남긴다**(H-9 가 쓴다). `v07` 판 줄임 표본 행은 **남긴다**(H-9 의 「줄인 글 → 후보 0」 재료 · `test_gold_v07_descend` · `_site` 가 같은 판을 쓴다 — 지우면 그쪽이 흔들린다). 머리말의 「부분 문자열만 같은 항목」 설명만 0.8.0 뜻으로 한 줄 |
| H-14 ★ | `test_gold_coverage.py` | `test_e2e_shapes_at_tool_level`(361 ~ 373) — `resolve(text=name + "께서")` → 후보 > 0 단언(372 ~ 373) | **고침** | `resolve(text=name)` → `PRD-416` 이 후보(이름 하나) **+** `resolve(text=name + "께서")` → 후보 0(R5 — 조사 붙은 이름). docstring 의 「옛 조사 목록 밖의 꼬리가 resolve 후보 0 이 아님」 → 0.8.0 뜻으로 · coverage 단언(368)은 그대로 |
| H-15 ★ | `test_gold_coverage.py` | `test_T15_real_concepts_per_question`(376 ~ 393) — 37 질문 문장마다 개념 수 1 ~ 7 · 중앙 3 · 「문장 `norm` 안의 부분 문자열인 행」 = 후보 | **고침** | 0.8.0 T15 실물 = 「서로 다른 `norm` 마다 직접 센 개념 집합 = `resolve(text=<그 norm 의 한 행 text>)`」(WP-1 완료 조건 5) 로 바꾸고 + **37 질문 문장 → 후보 0**(질문 글은 남기지 않는다 — 지금 그대로). 이름 → `test_T15_real_exact_name`(제안) |
| H-16 ★ | `test_gold_real.py` | 도우미 `entries(svc, qq)`(50 ~ 63 — `entry_text` 와 `question` **문장**을 각각 `resolve` 한 `in_range` 합집합) · 그것을 쓰는 시험 6(92 `test_T4_37_questions_pointers_in_tool_paths` 쪽 · 186 · 229 `test_T8_S2_S4_…` · 250 `test_T8_V1_V2_pair_values_unchanged`(Q21) · 277 `test_T9_Q17_package_hier` · 407 `test_W1_product_offer_rows_are_own_or_child_products`) | **고침** | `question` 문장 쪽은 0.8.0 에서 늘 0 이다 → 입구가 `entry_text` 쪽만 남아 **두 끝을 묻는 문항(Q21 — docstring 이 밝힌 꼴)에서 한 끝이 빠진다**. 처분 = 문장 대신 **그 문항이 기대하는 입구의 이름 각각**(`entry_text` 를 `·` 등으로 나눈 이름 · 또는 답 키 명세의 이름 칸)을 `resolve` 해 합집합. 문항 표에서 이름을 얻는 칸이 없으면 **고치지 말고 보고**(§8 A-4 — 시험 앱 답 키 명세 `name_to_entry` 의 자리) — 지금 37 문항에서 `question` 쪽만 내던 입구가 몇 개인지를 먼저 센다(0.7.2 허브 = 18105 읽기 · 또는 이 판 코드로 문장 쪽만 돌린 수) |

**셈**: 지움 = 파일 1(`test_gold_v07_resolve.py` · 함수 16) + 함수 4(H-4 1 · H-8 3) = **함수 20** · 고침 = **H-1 · H-2 · H-5 · H-6 · H-7 · H-9 · H-10 · H-11 · H-12 · H-13 · H-14 · H-15 · H-16 의 13 자리**(H-16 은 도우미 하나 + 부르는 시험 6) · 그대로 확인 = H-9b 4 함수 · 새 시험 = H-9 안(T15 정확 이름 + T26 남는 확인) · H-11 의 `abbr` 오류 두 줄 · H-15 의 실물 정확 이름(옮겨 지은 것 — 새 파일 0).

### 5-2. 돌릴 파일(WP-1 ~ WP-3 묶음 — 이것만)

| 파일 | 왜 |
|---|---|
| `tests/test_gold_tools_synthetic.py` | H-8 · H-9 · H-9b — 두 판(`csv` · `db`) |
| `tests/test_gold_contract.py` | H-1 · H-2 |
| `tests/test_gold_mcp.py` | H-10 · H-11 · REST = MCP(T7) |
| `tests/test_gold_v07_compat.py` | H-4 ~ H-7 |
| `tests/test_medallion_repo.py` | H-12 · DT9 · DT10 |
| `tests/test_gold_coverage.py` | H-14 · H-15(실물 — env 넷) |
| `tests/test_gold_real.py` | H-16(실물 — env 넷) |
| `tests/test_gold_v07_descend.py` · `tests/test_gold_v07_site.py` | **안 고친다** — `gold_fixture` `v07` 판을 같이 쓰므로 H-13 뒤 한 번 돌려 본다 |
| `tests/test_gold_rest.py` | **안 고친다** — `/resolve` `{"text": "시술가"}` 한 줄 · 경계 시험(`main.py` · `core/`)이 이 WORK 의 allowed_paths 를 지키는지 본다 |

`test_gold_v07_resolve.py` 는 지웠으므로 돌지 않는다. 그 밖의 gold 시험 파일(`test_gold_holes` · `test_gold_load`)은 이 WORK 가 고친 모듈의 `resolve` 길을 타지 않는다 — 돌리지 않는다(보고에 「안 돌린 파일」 로 이름만).

## 6. WP-4 — 두 판 · 실물 18107 · 마감

WP-3 뒤 한 번. 응답은 세션 임시 폴더에(레포 밖). `<…>` 는 자리 표시다.

```bash
# backend/ 에서
lsof -nP -iTCP:18107 -sTCP:LISTEN          # 비어 있어야 한다 — 아니면 멈추고 보고

# ① CSV 판을 18107 에 — 데이터 env 넷(+ 기대 해시) — WORK-013 §8-1 과 같은 꼴
GOLD_CSV_DIR=<gold 폴더> GOLD_SOURCE_REF_PATH=<silver 폴더>/source_ref.csv \
GOLD_HIERARCHY_DIR=<silver 폴더> GOLD_LEDGER_CHECK_PATH=<ledger-check-list.csv> GOLD_EXPECTED_HASH=<지금 gold_hash> \
  uv run uvicorn app.gold_main:app --host 127.0.0.1 --port 18107
# ② 요청 묶음(아래 표) → 응답 저장 → 18107 을 내린다(자기 PID 만)

# ③ DB 판을 같은 포트에 — 접속 값은 코디가 정한 방법으로 env 에만(찍지 않는다)
GOLD_REPOSITORY=db GOLD_EXPECTED_HASH=<같은 값> uv run uvicorn app.gold_main:app --host 127.0.0.1 --port 18107
# ④ 같은 묶음 → ② 와 견준다 → 18107 을 내린다 → lsof 로 내려간 것을 본다
```

| # | 확인 | 기대 |
|---|---|---|
| E1 | `health` | `build.gold_hash` · `aux_hash` 가 18105(지금 떠 있는 0.7.2 코드 — **GET 읽기만**)의 `health` 와 같다(새 입력 0) |
| E2 | **정확한 이름 → 코드** | 목록 꼴로 받은 다섯 표(`concern` · `site` · `modality` · `procedure` · `product`)의 행에서 표마다 **이름 행 하나 · 별칭 행 하나**(있으면 — 고른 행의 `gid` 를 보고)를 골라 그 `text` 로 맞춤 꼴 → 그 개념이 후보 · `matched` = `{span: <그 행 norm>}` · 띄어쓰기를 지운 꼴도 같은 후보 · 겹치는 `norm` 하나(같은 `norm` 개념 2 이상인 것 — 목록에서 셈)는 전부 + `ambiguous` 참 |
| E3 | **문장 → 후보 0** | E2 의 이름을 든 문장(「<이름> 받고 싶어요」 꼴 — 글자는 워커가 붙이는 시험 입력이다) · 이름 + 조사(「<이름>는」) · 이름의 앞 절반 → 셋 다 `200` · `total` 0 |
| E4 | **목록 꼴 그대로** | `resolve(tables=concern,site,modality,procedure,product)` 를 `next_cursor: null` 까지 → `counts.entities` 의 다섯 표 합 = **820**(고민 260 · 부위 89 · 계열 18 · 시술 138 · 제품 315 — 데이터 판이 바뀌었으면 그 판의 수와 까닭을 보고) · `candidates[]` 행 · 순서 · `total` 이 18105(0.7.2) 의 같은 요청과 **`request.abbr` 칸만 빼고 글자까지 같다** · 18107 응답 `request` 에 `abbr` 없음 |
| E5 | `abbr` 거절 | `/resolve?text=<E2 이름>&abbr=on` · `&abbr=off` → `invalid_argument`(REST 상태 코드 · MCP 오류 글 같음) |
| E6 | 다른 도구 불변 | 앱 답 키 명세 37 의 호출(앱 워크트리 `data/eval-set/calls/` — **읽기만** · `_RESUME` §2 11-17 「WORK-010 B 코디 답」 B-2) 가운데 **`resolve` 가 아닌 호출 전부**를 18105 와 18107 에 → `build.loaded_at` 빼고 같다. `resolve` 호출은 입력이 이름이면 후보 집합이 0.7.2 의 「`span` = 입력 `norm`」 후보와 같은지만 보고(다르면 호출 · 값을 보고 — O-33 재료) |
| E7 | MCP | `tools/list` 9 도구 · `resolve` 설명이 WP-2 완료 조건 3 · E2 의 한 요청을 MCP 로 → REST JSON 과 같다 |
| E8 | **CSV 판 = DB 판** | ② 와 ④ 의 응답(E2 ~ E7 의 요청 전부)이 `build.loaded_at` 을 빼고 같다 · `health` 는 `load_ms` 도 빼고 |

- **앱 0.4 가 쓰는 꼴은 E4 하나다**(SPEC-001 0.8.1 영향 표 · WORK-017 WP-1). 앱 0.4 실물(WORK-017 WP-12)은 이 WORK 의 18107 을 다시 띄워 쓴다 — 두 WORK 가 한 워커면 18107 을 띄운 채 넘겨도 되고, 다른 워커면 이 WP 끝에 내리고 앱 워커가 같은 명령으로 다시 띄운다(코디가 순서를 정한다 — §8 B-2).
- 18105 · 18106 · 18222 · 18224 를 내리거나 띄우지 않는다. PostgreSQL 에 쓰는 명령(적재 · alembic)을 돌리지 않는다.

### 6-1. 코디 몫

| 순서 | 무엇 | 왜 코디인가 |
|---|---|---|
| WP-4 뒤 | 워커 보고 검증 — 바뀐 시험 파일만(§5-2) · `git diff --stat` · grep(§7) | 사용자 11-17 「시험은 구현한 것만」 |
| 뒤 | 코드 검수 발주 → PASS 뒤 허브 브랜치 커밋 | 커밋은 코디 |
| 앱 0.4 PASS 뒤 | **18105 를 새 코드로 다시 띄운다 — 앱 0.4(18222)와 같이**(SPEC-001 0.8.1 영향 표: 0.3 앱을 0.8.0 허브에 붙이지 않는다 · 앱 0.4 만 먼저는 된다) | 18105 는 앱 · 사용자 e2e 가 보는 포트 |
| 뒤 | 시험 앱 B · C 열 · 답 키를 0.7.2 옛 판에 묶는 방법(O-33) | D-2 · 이 WORK 밖 |
| 뒤 | SPEC 되적기(§8 A) | 코디 |

## 7. 완료 조건 · 검증 명령

| # | 완료 조건 | 누가 | 무엇으로 |
|---|---|---|---|
| 1 | WP-1 완료 조건 1 ~ 5 · WP-2 완료 조건 1 ~ 4 | 워커 | §5-2 의 파일 |
| 2 | §5-1 표 H-1 ~ H-16 이 처분대로 · 지운 함수 20 · 고친 자리 13 · 그 밖에서 깨진 시험 0(있으면 고치지 말고 이름 · 까닭 보고) | 워커 | §5-2 · 보고 |
| 3 | `rg` 잔여 — WP-2 완료 조건 4 | 워커 | 아래 |
| 4 | 실물 E1 ~ E8 · 18107 내려감 | 워커 | §6 |
| 5 | 전체 pytest 를 돌리지 않았다 · 돌린 파일 · 통과 · skip 수가 보고에 있다 | 워커 | 보고 |
| 6 | 다른 도구 8 의 코드 diff 0(`concern.py` · `facets.py` · `pairs.py` · `coverage.py` · `core.py` · `descend.py` …) | 워커 → 코디 | 아래 |

```bash
# backend/ 에서 — 이 묶음만(전체가 아니다)
uv run ruff check app/modules/gold/{resolve,memory,repository,headers,service,mcp_server}.py app/router/gold.py app/swagger_docs/gold.py \
  tests/{gold_fixture,test_gold_contract,test_gold_tools_synthetic,test_gold_mcp,test_gold_v07_compat,test_medallion_repo,test_gold_coverage,test_gold_real}.py
DATABASE_URL=sqlite+aiosqlite:///:memory: uv run pytest tests/test_gold_tools_synthetic.py tests/test_gold_contract.py tests/test_gold_mcp.py \
  tests/test_gold_v07_compat.py tests/test_medallion_repo.py tests/test_gold_coverage.py tests/test_gold_real.py \
  tests/test_gold_v07_descend.py tests/test_gold_v07_site.py tests/test_gold_rest.py -q -rs
rg -n "abbr|covered_by|HOW_ABBR|HOW_PART|entry_by_abbr|abbr_keys" app      # §4 완료 조건 4 의 줄만
rg -n "resolve\(" tests | rg -v "Path\(|EntityResolver"                      # 남은 gold resolve 호출 — 문장 입력 0

# 허브 워크트리 루트에서
lsof -nP -iTCP:18107 -sTCP:LISTEN                                            # 비어 있다
git status --porcelain                                                       # §2 allowed_paths 안뿐 · *.csv · dump · *.db 0
git diff --stat HEAD -- backend/app/modules/gold/{concern,descend,facets,pairs,coverage,core,cursor,kinds,ledger,ranges,closure}.py backend/app/main.py backend/app/core   # 비어 있다
git diff HEAD -U0 | grep -n -i -E "postgresql(\+asyncpg)?://[^<]|passw|secret|token|api[_-]?key"   # 0
```

## 8. 열린 것 · 이 문서를 쓰며 본 것(SPEC 은 고치지 않았다)

### 8-1. A — SPEC 되적기 후보(코디)

| # | 무엇 | 이 문서의 값 |
|---|---|---|
| A-1 | SPEC-003 §5 P1 의 repository 메서드 수 | 0.7.2 까지 줄임 열쇠 메서드 2 를 더한 수 → **−2**(SPEC-001 0.8.0 「따라 고칠 곳」 에 이미 적힘 · 수는 구현 뒤 센다) |
| A-2 | 맞춤이 `norm` 색인을 읽는 repository 메서드 | 있으면 그것 · 없으면 **새 메서드를 더하지 않고 보고**(Protocol 을 넓히면 두 판 DT9 표가 바뀐다) |
| A-3 | REST · MCP 의 `abbr` 입력을 남겨 거절하나(본문 a) · 지우나(b) | (a) — 지우면 REST 가 모르는 쿼리를 무시해 `invalid_argument` 가 서지 않는다(SPEC 「주면 `invalid_argument`」 와 갈림 · REST ≠ MCP). SPEC-001 §4-1 에 「스키마에는 남고 설명은 『없앰』」 한 줄 되적기 |
| A-4 | `test_gold_real.entries` 의 문장 입력(H-16) | 문항이 기대하는 입구의 이름을 얻는 칸이 문항 표에 없으면 보고 — 답 키 명세(`name_to_entry`)와 같은 자리를 쓸지는 O-33 과 함께 코디 |
| A-5 | SPEC-001 0.8.1 「고칠 · 지울 허브 시험」 표 밖 자리 ★ 6(H-2 · H-7 · H-12 · H-14 · H-15 · H-16 — 파일로는 `test_gold_coverage` · `test_gold_real` 둘이 새로) | 표의 「같은 처분」 규칙으로 처분했다 — 표에 줄을 더하는 되적기 |

### 8-2. B — 구현 워커가 추측으로 메우지 않게 이 문서가 정한 값(코디가 바꿀 수 있다)

| # | 무엇 | 이 문서의 값 | 왜 |
|---|---|---|---|
| B-1 | 새 시험을 어느 파일에 | 새 파일 0 — `test_gold_tools_synthetic.py`(T15 · T26 남는 확인) · `test_gold_mcp.py`(T29 설명 · `abbr` 오류) · `test_gold_coverage.py`(T15 실물) | SPEC-001 0.8.1 표 「T15 시험 자리에 새로 쓴다」 · 지운 `test_gold_v07_resolve.py` 를 다른 이름으로 되살리지 않는다 |
| B-2 | 18107 을 앱 0.4 실물에 넘기나 | 워커가 같으면 띄운 채 넘김 · 다르면 내리고 앱 워커가 같은 명령으로 | 18107 은 「띄웠다 내린다」 포트다(WORK-013 §2) — 코디가 순서를 정한다 |
| B-3 | `gold_fixture` `v07` 판의 줄임 표본 | 남긴다 | `test_gold_v07_descend` · `_site` 가 같은 판을 쓴다 · 「줄인 글 → 0」 재료 |
| B-4 | E3 의 문장 · E2 의 행 | 워커가 목록 꼴 응답에서 고른 행 · 그 이름에 붙인 시험 입력 — 보고에 `gid` · 입력을 적는다 | 고정 수 · 고정 이름을 이 문서가 박지 않는다(데이터 판이 바뀐다) |

## 9. SPEC-001 0.8.0 · 0.8.1 절 ↔ WP 대응(미대응 0)

| SPEC-001 | 규칙 · 칸 | WP |
|---|---|---|
| §4-1 입력 표(`text` 이름 하나 · `range` · `tables` · `cursor` · `limit` · `abbr` 없앰) | WP-1 · WP-2 |
| §4-1 계산 필드(`matched.span` · `in_range` · `ambiguous`) · 없앤 필드(`start` · `covered_by` · `how` · `full`) | WP-1 |
| §4-1 순서 · 겹침 · 후보 0 · 쪽 넘김 없음 | WP-1 |
| §4-1 MCP 도구 설명 문장 | WP-2 |
| §4-1 목록 꼴 그대로 · `request.abbr` 없음 | WP-2 · E4 |
| §5-1 R1 · R2 · R3 · R5 · R6 · R8 · R7 지움 · R9 지움 | WP-1 |
| §5-11 NM 지움 · 「두 판」 | WP-1(`memory.py` · `repository.py`) |
| §3-1 줄임 열쇠 색인 없앰 | WP-1 |
| §9 T13 · T15 · T23(`covered_by` 줄 지움) · T26(남는 확인) · T27(T3 뺌) · T29 | WP-3(H-1 ~ H-16) · E2 ~ E8 |
| §10 O-32 (a) | WP-2 · A-3 |
| §10 O-33 | 이 WORK 밖(§6-1 코디) |
| 변경 기록 0.8.0 「남길 것 · 지울 것」 | WP-1 · WP-2 |
| 변경 기록 0.8.0 · 0.8.1 「쓰는 곳별 영향」 | §6 E4 · §6-1(18105 재시작 순서) |
| 변경 기록 0.8.1 「고칠 · 지울 허브 시험」 | WP-3 §5-1 |
| 부록 A(없어진 계산 필드 · 줄임 열쇠 칸) | WP-1 |

## 변경 기록

### 0.1.0 (2026-11-18) — 처음 씀

- SPEC-001 0.8.1 을 WP 넷(WP-1 맞춤 꼴 · 색인 · repository → WP-2 `abbr` · REST · MCP · 설명 → WP-3 시험 → WP-4 두 판 · 실물 18107)으로.
- 고칠 · 지울 시험 = SPEC-001 0.8.1 표 8 파일 + 이 워커 grep(`rg -n "resolve\(|abbr|covered_by|\"how\"|\"full\"|MATCHED_ABBR" tests`)으로 더 찾은 자리 ★(H-2 · H-7 · H-12 · H-14 · H-15 · H-16 — 새 파일 `test_gold_coverage.py` · `test_gold_real.py`) — 지움 함수 20 · 고침 13 자리 · 그대로 확인 4.
- 이 워커가 정한 값 B-1 ~ B-4 · 되적기 후보 A-1 ~ A-5. 이 워커는 허브 · DB · 앱을 부르지 않았다 · 코드를 고치지 않았다(읽기만).
