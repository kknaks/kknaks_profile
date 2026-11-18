---
type: work
id: WORK-005
title: "허브 0.5.1 구현 계획 — resolve 넓은 후보 · coverage 도구 · 하위 role 설명 · 시험 T15 ~ T19"
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
    - "orchestration/work/phub-gold-jev/SPEC-001-hub-gold-mcp.md (0.5.1 · 재검수 PASS — review-spec-v051.md) ← 계약"
  decisions:
    - "orchestration/work/phub-gold-jev/_RESUME.md §2 (2026-11-16 「끝까지 진행」 · 「SPEC 0.5.0 검수 뒤 결정 3」 · 「길 찾기 재설계 진행」 · 「허브 검수 뒤」)"
  related:
    - "orchestration/work/phub-gold-jev/WORK-006-app-v05.md (앱 쪽 — 나란히 돈다)"
    - "orchestration/work/phub-gold-jev/WORK-001-hub.md (0.4.1 구현 계획 — 공통 규칙 §2 를 그대로 잇는다)"
    - "orchestration/work/phub-gold-jev/review-spec-v051.md"
---

# WORK-005 — 허브 0.5.1 구현 계획(길 찾기 재설계의 허브 쪽)

> 경로 접두어: `P` = 프로필 워크트리 · `W` = `$P/orchestration/work/phub-gold-jev` · `SM` = `$P/orchestration/work/_archive/procedure-hub/phub-ledger-redesign/silver-model`(gitignore · 로컬 데이터) · `HUB-WT` = `~/orca/workspaces/PROCEDURE-HUB/phub-gold-jev`(브랜치 `kknaksss/phub-gold-jev` · **0.4.1 구현이 미커밋으로 올라가 있다 — 그 위에 이어서 고친다 · 새로 쓰지 않는다**).
> **계약은 SPEC-001 0.5.1 이다.** 이 문서는 「어느 파일을 · 어떤 순서로 · 무엇으로 확인하나」 만 정한다. SPEC 에 없는 동작을 만들지 않는다 — 어긋나는 것을 찾으면 코드를 맞춰 고치지 말고 보고한다(§9).
> 공개 레포 규칙 · 하지 말 것 · allowed_paths · 데이터 env · 검증 명령의 틀은 **WORK-001 §2 그대로**다(아래 §2 에 바뀐 것만 적는다).

## 0. 요약

- 바뀌는 것은 넷이다: ① `resolve` 맞춤 꼴 = 문장 `norm` 안의 입구 이름 **부분 일치 전부**(조사 목록 폐기 · `matched{span, start, covered_by}`) ② 새 도구 `coverage`(도구 9 — 노드 × 정보 종류 14 × 층의 행 수) ③ 「하위 *」 role 을 도구 설명에 적음(계약 · 기본값은 그대로) ④ 시험 T15 ~ T19.
- gold 15표 · gold 해시 · 보조 입력 · 0.4.1 의 여덟 도구 **입력**은 그대로다. 응답에서 바뀌는 것은 `resolve` 의 `matched` 필드뿐이다(`particle` 없어짐 → 앱이 함께 바뀐다 · WORK-006 WP-1).
- WP 넷: **WP-1** resolve 넓은 후보 → **WP-2** coverage(정보 종류 표 + 도구 + REST · MCP) → **WP-3** 하위 role 설명 · 되적기 확인 → **WP-4** 시험 마감 · 실물 셈 재현.
- **코디가 18105 에 띄운 허브는 건드리지 않는다.** 워커가 서버로 확인해야 하면 **18106** 만 쓰고 끝나면 내린다(11-16 비어 있음 확인). 18105 를 새 코드로 다시 띄우는 것은 코디 몫이다 — 앱 새 코드와 **함께** 바뀌어야 한다(§7).

## 1. 지금 코드(11-16 확인 — `HUB-WT/backend`)

| 파일 | 지금 | 이번에 |
|---|---|---|
| `app/modules/gold/resolve.py`(107줄) | `_match` = 공백 낱말 + 이웃 낱말 이어 붙임 → `norm` 완전 일치 → 안 되면 `PARTICLES` 16 중 하나를 뗌(`:20` · `:52-66`) · `matched{span, particle}` | WP-1 — `_match` 를 다시 쓴다 · `PARTICLES` 삭제 · `_listing` 은 그대로 |
| `app/modules/gold/repository.py` · `memory.py` | `entries_by_norm(norm)` 색인(`memory.py:45`) — `norm` 전부를 도는 메서드 없음 | WP-1 — `entry_norms()` 하나 더함(Protocol + CSV 구현) |
| `app/modules/gold/facets.py`(267줄) | `roles` 에 `g_scope.role` 값을 주면 그 holder 행이 나온다(`_target` — `:125-127`) · 제품 offer 기본 role(`PRODUCT_OFFER_ROLES` — `:26-28`) · `counts.distinct_rows` | 동작은 그대로(T19 로 확인) · WP-2 가 쪽 넘김 앞의 「행 전부」 를 내는 안쪽 함수를 `coverage` 와 **함께 쓰게** 가른다 |
| `app/modules/gold/pairs.py`(107줄) | `PAIR_ROLES` = 자기 · 물려받음 · 하위 케이스 · 하위 시술 고정 · `b` 없이 `package_kinds`(N1-1) 구현됨 | WP-2 — 같은 식으로 안쪽 함수를 가른다 · WP-3 T18 시험 확인 |
| `app/modules/gold/service.py`(161줄) | 도구 8 · 머리글 「도구 8」 | WP-2 — 9 번째 `coverage` |
| `app/modules/gold/mcp_server.py`(150줄) | `DESCRIPTIONS` 8 · `resolve` 설명이 0.4.1 맞춤 규칙 | WP-1 · WP-2 · WP-3 — 설명 고침 · 도구 하나 더함 |
| `app/router/gold.py` · `app/swagger_docs/gold.py` | REST 8 | WP-2 — `GET /coverage` |
| `app/modules/gold/headers.py` · `config.py` | 부록 A 계약 · 설정 | WP-2 — 개요 칸 · 원리 칸 상수 · `GOLD_COVERAGE_NODES_MAX` |
| `tests/test_gold_*.py`(6 파일 · 79 시험 함수) | `test_resolve_particle_and_span`(`test_gold_tools_synthetic.py:43`)이 `matched.particle` 을 본다 · `test_tool_list` 가 도구 8 · `resolve` 설명 낱말을 본다(`test_gold_mcp.py:16 · 34`) | WP-1 · WP-4 — 그 둘은 **고친다**(계약이 바뀐 자리) · 나머지 시험은 그대로 통과해야 한다 |

기준선(11-16 코디 검증): 데이터 env 로 README 「검증」 전체 = **568 passed · 2 skipped**. 이 수에서 줄어드는 것은 위 「고친다」 둘의 이름 바뀜뿐이어야 한다.

## 2. 공통 — WORK-001 §2 에서 바뀐 것만

| 항목 | 이번 판 |
|---|---|
| allowed_paths | WORK-001 §2-2 와 같다 — `backend/app/modules/gold/**`(새 파일 `coverage.py` · `kinds.py` 포함) · `backend/app/router/gold.py` · `backend/app/swagger_docs/gold.py` · `backend/tests/gold_fixture.py` · `gold_support.py` · `test_gold_*.py`(새 `test_gold_coverage.py` 포함) · `backend/envs/.env.example`(이름 한 줄) · `backend/README.md`(「gold 로컬 실행 · 검증」 절의 도구 목록 한 줄). **`pyproject.toml` · `uv.lock` 은 이번에 안 고친다**(새 의존 없음) |
| 포트 | 시험은 포트 없이(ASGI transport). 서버 확인은 **18106** 만 · 끝나면 내린다. 18105(허브) · 18220(화면)은 코디 것 — 죽이거나 다시 띄우지 않는다 |
| 데이터 env · 검증 명령 | WORK-001 §2-3 · §2-4 그대로(`DATABASE_URL=sqlite+aiosqlite:///:memory:` · 데이터 env 없으면 실물 시험 skip · skip 수와 통과 수를 둘 다 보고) |
| 커밋 | 안 한다 — 워크트리에 변경만 남긴다(코디 몫) |
| 공개 레포 | 합성 fixture 는 가짜 코드 · 가짜 이름만. 시험 이름 · 주석에 시술 이름 · 질문 문장을 넣지 않는다. T15 의 「조사 16 밖의 조사」 도 가짜 이름에 붙여 만든다 |

## 3. WP-1 — `resolve` 넓은 후보

**목표**: 맞춤 꼴이 질문 문장 `norm` 안에 부분 문자열로 든 `g_entry.norm` 을 **전부** 낸다. 조사 · 띄어쓰기에 기대지 않는다.
**SPEC**: §4-1(출력 표 · 순서 · 불릿) · §5-1 R1 ~ R8 · §4-0 「`total` 단위」 resolve 행 · 부록 A 「(넓은 후보)」 줄 · §9 T15 · O-4(결정됨).

| 고칠 것 | 어디 | 내용 |
|---|---|---|
| 전체 `norm` 돌기 | `repository.py` Protocol + `CsvMemoryGoldRepository` · `memory.py` | `entry_norms() -> Sequence[str]` — `g_entry` 의 서로 다른 `norm`(빈 문자열 제외). 색인은 적재 때 한 번 만든다. service 는 여전히 repository 메서드만 부른다(`test_service_layer_uses_repository_only` 그대로) |
| 맞춤 | `resolve.py` `_match` | ① `q = norm(text)`(R1 — 다른 정규화 없음) ② `entry_norms()` 가운데 `q` 의 부분 문자열인 것 전부 = 맞은 조각 ③ 조각마다 `q` 안의 **나온 자리 전부**를 구한다 ④ 그 조각의 `g_entry` 행을 모은다. 낱말로 자르지 않고 조사를 떼지 않는다(R2 · R3) · 길이 하한 없음(R7) · 점수 · 순위 없음(R8) |
| `matched` | 같은 함수 | `span` = 그 행의 `norm` · `start` = 첫 자리(0 부터) · `covered_by` = 아래 규칙 · **`particle` 필드를 없앤다** |
| `covered_by` | 같은 함수 | 그 조각의 나온 자리가 **전부** 더 긴 맞은 조각의 나온 자리 안에 통째로 들면 → 첫 자리를 덮는 조각 가운데 가장 긴 것(길이가 같으면 앞 자리) · 한 자리라도 덮이지 않았으면 `null`(§9 의 A-1 — SPEC-002 §9-3c 「짧은 이름과 긴 이름을 둘 다 따로 말함 = 둘 다 덮이지 않은 일치」 에서 끌어낸 것). **표지일 뿐 — 덮인 후보도 빼지 않는다** |
| 순서 | 같은 함수 | (`range` 를 줬으면 `in_range` 참 먼저 →) 맞은 조각 `norm` 글자 수 내림차순 → `TABLE_ORDER` → `name_kind` 「이름」 먼저 → `gid`. 같은 (`entity_table`, `entity_code`) 는 이 순서의 첫 행 하나만(가장 긴 조각의 행이 남는다) |
| `ambiguous` | 같은 함수 | 같은 `norm` 에 개념 2 이상인 조각이 있나(뜻 그대로) |
| 삭제 | `resolve.py:20` | `PARTICLES` · 낱말 이어 붙임 루프 · 머리글의 R2 · O-4 (a) 설명 |
| 도구 설명 | `mcp_server.py` `DESCRIPTIONS["resolve"]` · `swagger_docs/gold.py` · `router/gold.py` summary | 「문장 norm 안의 입구 이름 부분 일치 전부 · 조사를 떼지 않는다 · 덮인 짧은 조각도 `matched.covered_by` 와 함께 남는다 · 고르지 않고 전부」 로. `test_tool_list` 가 보는 낱말 「고르지 않고」 는 남긴다 |

**완료 조건**
1. T15 합성: 가짜 입구로 — 입력 `norm` 의 부분 문자열인 `norm` 이 전부 나온다(직접 센 수 = `total`) · 옛 조사 16 밖의 글자가 뒤에 붙은 이름도 맞는다 · 띄어쓰기를 바꾼 입력이 같은 후보 집합을 낸다 · 긴 조각 안에 든 짧은 조각이 `covered_by` 와 함께 **남아 있다** · 같은 짧은 조각이 따로 한 번 더 나오면 `covered_by` = `null` · 순서 = 긴 조각 먼저 · 응답 어디에도 `particle` 키가 없다.
2. 후보 0 = `200` · 빈 목록(`test_resolve_zero_is_200` 그대로) · `range` 가 후보를 버리지 않는다(`test_resolve_range_never_drops` 그대로) · 목록 꼴 시험(`test_T13_*`)은 손대지 않고 통과.
3. `test_resolve_particle_and_span` 은 T15 시험으로 **바꾼다**(지우고 끝내지 않는다).
4. T15 실물(데이터 env): 로컬 `questions.csv` 의 37 질문을 그대로 주어 문항당 서로 다른 개념 수가 **1 ~ 7 · 중앙 3**(SPEC-001 §4-1 셈)으로 나온다 — 질문 문장은 시험이 로컬 파일에서만 읽고 코드 · 출력에 남기지 않는다. T4(37 되짚기)가 그대로 통과한다.

**검증**: `uv run ruff check app tests scripts` → `DATABASE_URL=sqlite+aiosqlite:///:memory: uv run pytest tests/test_gold_tools_synthetic.py tests/test_gold_mcp.py -q` → 데이터 env 를 주고 `tests/test_gold_real.py -q`.

## 4. WP-2 — `coverage`(도구 9) + 정보 종류 표

**목표**: 노드 목록을 받아 노드마다 정보 종류 × 층(`self` · `lower` · `inherited`)의 서로 다른 `gid` 수를 낸다. **행 본문은 없다.**
**SPEC**: §4-0(응답 머리 `request` 의 `null` · 「`total` 단위」 · 「있음」 표의 `coverage.nodes[]` 행 · REST ↔ MCP 표 9) · §4-9 전부 · §5-8 전부 · 부록 A 「(정보 종류 셈)」 네 줄 · 계산 필드 줄 · §9 T16 · O-19(본문 = 새 도구) · O-20(14 · 64) · O-6(상한은 설정).

| 만들 · 고칠 것 | 어디 | 내용 |
|---|---|---|
| 정보 종류 표 | 새 `app/modules/gold/kinds.py` | §5-8 표를 상수 하나로: `kind` 14 의 **순서**(표의 행 순서) · 노드의 표마다 「세는 조회」 또는 없음(「—」). `OVERVIEW_COLUMNS`(§5-8 의 11 칸) · `MECHANISM_COLUMNS`(3 칸)는 `headers.py` 에 두고 T3 이 CSV 헤더와 대조한다. 속성 쪽 조합은 기존 `ATTR_MATCH`(§4-4 「속성 쪽」 표)에 있는 것만 — 표와 어긋나면 멈추고 보고 |
| 「행 전부」 안쪽 함수 | `facets.py` · `pairs.py` · `concern.py` | 쪽 넘김 **앞**의 전체 행(대상 쪽은 `layer` 포함)을 내는 안쪽 함수를 드러내 `facets()` · `pair()` · `concern_candidates()` 와 `coverage()` 가 **같은 함수**를 부르게 한다. 세는 길을 따로 짓지 않는다 — 불변식(T16)을 구조로 지킨다. 기존 응답 · 순서 · `total` 은 바뀌지 않는다(T6 · T7 그대로) |
| 셈 | 새 `app/modules/gold/coverage.py` | 대상 4표 노드: 종류의 조회를 `roles` = `자기` · `물려받음` · `하위 시술` · `하위 케이스` · `하위 제품`(종류 `offer` 의 제품 노드는 `자기` · `하위 제품` — §4-4)으로 한 번 얻어 `layer.role` 로 갈라 **서로 다른 `gid`** 를 센다 → `self` · `lower`(+ `lower_holders` = 그런 행을 가진 서로 다른 holder 수) · `inherited`. `overview` · `mechanism` 은 그 종류의 칸에 값이 하나라도 있는 profile 행만. `indication` 은 `facets` indication 맞춤 그대로(`concern_match` = 직접). `pair` 로 읽는 넷(`avoid` · `combo` · `same_day` · `order_interval`)은 `b` 없이 부른 행을 `a_layer.role` 로 가른다(`same_day` = 갈래 전부). `lineup` = `scope` 의 「하위 *」 행 수 → `self` 0 · `lower` = 그 수 · `inherited` `null`. 값 쪽 · 속성 쪽 노드: `hier` 기본값(`expand`)으로 얻은 행 전부가 `self` · 나머지 셋은 `null`. concern 의 `indication` = `concern_candidates` 의 `counts.rows`(쪽 밖 목록 포함) |
| 입력 검사 | `coverage.py` | `nodes` 필수 · 1 ~ 상한(설정 `GOLD_COVERAGE_NODES_MAX` 기본 64) · 넘으면 `invalid_argument`(잘라 내지 않는다) · `표:코드` 꼴 아님 = `invalid_argument` · 하나라도 gold 에 없으면 `not_found`(어느 항목인지 문구에) — 「있음」 기준은 표에 따라 `g_scope` subject 색인 / `g_entry` 색인(§4-0). `kinds` = §5-8 코드 정확 일치 · 표 밖 값 = `invalid_argument` · 안 주면 전부이고 `request.kinds` = `null` |
| 출력 | `coverage.py` | `items[]` = `nodes` **순서 그대로** · `{node, name, kinds[]{kind, self, lower, lower_holders, inherited}}` · 그 노드의 표에 「—」 인 종류는 싣지 않는다(0 과 구분) · `name` = `g_entry.entity_name`(입구 없으면 `g_scope.subject_name`) · `total` = `items` 수 · `next_cursor` = `null` · `ledger_check[]` **없음** |
| 도구 9 | `service.py` | `coverage(nodes, kinds)` · 머리글 「도구 9」 |
| REST | `router/gold.py` · `swagger_docs/gold.py` | `GET /coverage` — `nodes` · `kinds` 는 기존 목록 입력과 같은 꼴(`split`) |
| MCP | `mcp_server.py` | 도구 `coverage` · 설명 = 「후보 × 정보 종류 × 층의 행 수 — 셈뿐 · 고르지 않는다 · 셈이 전부 0 인 노드도 그대로 낸다 · 하위는 `g_scope` 한 단」 + 종류 14 코드 |
| 설정 | `config.py` · `envs/.env.example` | `GOLD_COVERAGE_NODES_MAX`(선택 · 기본 64 · 빈 값 = 미설정) |

**응답 꼴 — 앱이 모의로 쓰는 계약**(WORK-006 WP-1 은 이 꼴만 보고 먼저 짓는다 · 코드는 가짜다)

```json
{
  "build": {"gold_hash": "<sha>", "aux_hash": "<sha>", "loaded_at": "<ISO 8601>"},
  "request": {"nodes": ["product:PRD-90001", "site:SIT-90001"], "kinds": null},
  "total": 2,
  "next_cursor": null,
  "items": [
    {"node": "product:PRD-90001", "name": "<이름>", "kinds": [
      {"kind": "overview", "self": 1, "lower": 1, "lower_holders": 1, "inherited": 3},
      {"kind": "mechanism", "self": 0, "lower": 0, "lower_holders": 0, "inherited": 3},
      {"kind": "outcome", "self": 0, "lower": 4, "lower_holders": 1, "inherited": 19},
      {"kind": "lineup", "self": 0, "lower": 2, "lower_holders": 2, "inherited": null}
    ]},
    {"node": "site:SIT-90001", "name": "<이름>", "kinds": [
      {"kind": "overview", "self": 4, "lower": null, "lower_holders": null, "inherited": null}
    ]}
  ]
}
```

(대상 4표 노드의 `kinds[]` 는 실제로는 14 줄 전부다 — 위는 줄인 것. `kinds[]` 의 순서 = §5-8 표의 행 순서.)

**완료 조건**
1. T16 합성: 가짜 대상(자기 0 · 하위에 행 · 물려받음에 행 / 원리 칸이 빈 자기 profile 행)으로 — `self` · `lower` · `lower_holders` · `inherited` 가 손으로 센 값 · 「—」 종류가 안 실림 · `nodes` 순서 그대로 · 없는 노드 = `not_found` · 상한 넘김 · 빈 `nodes` · 표 밖 `kinds` = `invalid_argument` · `request.kinds` = `null` · 원리 칸이 빈 자기 행뿐인 제품의 `mechanism.self` = 0 · 값 쪽 노드의 세 칸 = `null`.
2. T16 실물(불변식): **대상 4표 전 노드 × 14 종류**에서 `coverage` 의 수 = 같은 build 에서 그 종류의 조회를 그 role 로 **공개 도구로** 끝까지 넘겨 센 서로 다른 `gid` 수(안쪽 함수를 같이 쓰더라도 시험은 도구 응답으로 센다).
3. T16 실물(셈 재현): SPEC-001 §4-9 끝 두 불릿의 수가 다시 나온다 — `self` 0 · `lower` ≥ 1: 적응 시술 33 · 제품 3 · 계열 1 / 효과 30 · 3 · 1 / 부작용 31 · 3 / 상품 계열 15 · 시술 11 · 제품 7 / 회복 4 / 금기 2 · 그중 `inherited` ≥ 1: 적응 34 · 효과 31 · `inherited` 만: 원리 — 입구 있는 제품 315 가운데 314. 한 수라도 다르면 **코드를 수에 맞추지 말고** 보고한다(식이 다른 것인지 SPEC 의 수가 다른 것인지 가려야 한다).
4. T7: `coverage` 의 REST 응답 = MCP 응답 · 오류 문구도 같다. T6: 같은 입력 두 번 = 같은 응답.
5. 기존 `facets` · `pair` · `concern_candidates` 시험이 **하나도 안 바뀌고** 통과한다(안쪽 함수를 가른 것이 응답을 바꾸지 않았다는 증거).
6. 보고에 적을 것: 노드 7 개 · 64 개 `coverage` 한 번의 ms(실물 · 포트 없이 재도 된다) — 앱이 단계 ①-1 에서 매 질문 부른다.

**검증**: `uv run pytest tests/test_gold_coverage.py tests/test_gold_tools_synthetic.py tests/test_gold_mcp.py tests/test_gold_rest.py tests/test_gold_contract.py -q`(합성) → 데이터 env 로 같은 파일 + `tests/test_gold_real.py`.

## 5. WP-3 — 하위 role 설명 · 되적기 확인

**목표**: 계약 · 기본값을 그대로 두고 **설명만** 더한다. 0.5.0 이 되적은 것(이미 구현됨)이 시험에 걸려 있는지 확인한다.
**SPEC**: §4-4 `roles` 칸(0.5.1 문장) · §5-2 표 · §5-3 S2 · S5 · S6 · §4-6 · §9 T17 · T18 · T19 · O-21 · O-22 ①.

| 할 것 | 어디 | 내용 |
|---|---|---|
| W-4 문장 | `mcp_server.py` `DESCRIPTIONS["facets"]` · `swagger_docs/gold.py` 의 `roles` 설명 | 「하위 층(`하위 시술` · `하위 케이스` · `하위 제품`)의 자기 행은 `roles` 에 그 role 을 줘야 나온다 — 기본값(`자기` · `물려받음`)으로는 나오지 않는다」 를 그대로 넣는다. 모든 부르는 쪽에 같은 설명이다 |
| `pair` 설명 | `DESCRIPTIONS["pair"]` | 펼치는 role(자기 · 물려받음 · 하위 케이스 · 하위 시술)이 이미 적혀 있다 — 그대로인지 확인만(§5-3 S2) |
| semantic-map 을 바꿔 읽는 자리(W-7) · 한 단의 한계(W-8) | `facets.py` 머리글 주석 | 코드 동작은 없다 — 「하위는 `g_scope` 의 하위 role 한 단 · 두 단 아래 · 『제품 경유』 는 나오지 않는다(SPEC-001 §5-3 S6 · O-21)」 한 줄을 주석으로 남긴다 |
| T19 | `test_gold_tools_synthetic.py` · `test_gold_real.py` · `test_gold_mcp.py` | 「하위 *」 role 을 주면 그 holder 의 자기 행이 `layer.role` = 그 role 로 나온다 · 기본값으로는 안 나온다 · 「상위 제품」 은 명시해야만 · **MCP `facets` 설명에 위 문장이 있다** |
| T17 · T18 확인 | 같은 파일 | T17 = 기존 `test_W1_*` 넷이 덮는다(제품 offer 기본 role · `distinct_rows`) — 이름에 T17 을 덧붙이거나 그대로 둔다. T18(`b` 없이 `package_kinds`) = `test_pair_packages` 가 「`a` 쪽과 겹치는 패키지 전부 · `b` 를 주면 양쪽과 다 겹치는 것만」 을 둘 다 보는지 읽고 없으면 더한다 |
| `request` 의 `null` | 같은 파일 | `scope.roles` · `pair.classes` · `coverage.kinds` 를 안 주면 `request` 에 `null` 로 돌아온다(§4-0) — 단언 한 줄씩 |
| O-22 ① | `memory.py` `_integrity` | `health.integrity` 에 (`subject`, `holder`) 짝이 두 번 이상인 `g_scope` 행 수를 하나 더 센다(지금 0 — 계약은 그대로 · SPEC 추천). 이름은 구현 때 정하고 보고한다 |

**완료 조건**: T17 · T18 · T19 가 시험 이름 또는 주석으로 찾아진다 · 기본값(S2) · 제품 offer 기본값이 안 바뀌었다(기존 시험 통과) · 도구 설명 문장이 MCP `list_tools` 에 그대로 보인다.
**검증**: `uv run pytest tests/test_gold_tools_synthetic.py tests/test_gold_mcp.py -q` → 데이터 env 로 `tests/test_gold_real.py -q`.

## 6. WP-4 — 시험 마감 · 실물 확인

**SPEC**: §9 T3(부록 A 대조 — 새 줄 다섯) · T6 · T7 · T15 ~ T19 · 「문항별 기대」 표의 Q04 줄.

1. T3: `headers.py` 에 부록 A 의 새 줄(「(정보 종류 셈)」 넷 · 「(넓은 후보)」 하나)과 계산 필드(`matched.start` · `matched.covered_by` · `coverage` 전 필드)를 넣고 기계 대조가 통과한다. `matched.particle` 이 계산 필드 목록에서 빠졌다.
2. `test_tool_list`: 도구 **9**.
3. Q04 줄: 상위 제품 진술은 하위 제품에 안 붙고(S4 그대로) · 거꾸로 하위 제품의 자기 행은 「하위 제품」 role 을 주면 상위 제품 조회에 `layer` 와 함께 나온다(실물 한 건).
4. e2e 가 실패했던 두 꼴을 **도구 수준에서** 한 번씩(실물 · 포트 없이): ① `product:PRD-416` 의 `coverage` 가 효과 (0, 4, 19) · 적응 (0, 11, 27) · 원리 (0, 0, 3) · 개요 (1, 1, 3) 을 낸다(`review-spec-v051.md` §2 의 셈) ② 그 제품의 이름 뒤에 옛 조사 목록 밖의 조사를 붙인 글을 `resolve` 에 주면 후보가 0 이 아니고 그 제품이 들어 있다(이름은 시험이 `g_entry` 에서 읽는다 — 코드에 글자로 넣지 않는다).
5. 마지막에 **한 번** README 「검증」 전체: `uv run ruff check app tests scripts` · 데이터 env + `DATABASE_URL=sqlite+aiosqlite:///:memory: uv run pytest --ignore=tests/integration`. 통과 · skip 수를 기준선(568 · 2)과 나란히 보고한다.
6. `backend/README.md` 의 gold 절 REST 도구 목록에 `coverage` 를 더한다(한 줄).
7. 18106 에 띄워 `health` · `coverage` 한 건 · MCP `list_tools`(9)를 한 번 보고 내린다 — 앱 워커가 이어서 쓰겠다고 하면 코디에게 알리고 띄워 둔다(§7).
8. 커밋 후보 grep: 시술 이름 · 질문 문장 · 실제 `gid` · 홈 경로 0.

## 7. 순서 · 병행

| 순서 | 무엇 | 근거 |
|---|---|---|
| WP-1 ∥ WP-2 | 서로 다른 파일(`resolve.py` / `coverage.py` · `kinds.py`)이라 한 워커가 차례로 해도 · 나눠도 된다. `mcp_server.py` · `headers.py` 만 둘이 함께 건드린다 | — |
| WP-3 | WP-2 뒤(`request.kinds` 단언 · 설명 문장) | — |
| WP-4 | 마지막 | 전체 검증은 끝에 한 번 |
| **앱과 나란히** | 앱(WORK-006)은 **§4 의 응답 꼴과 §3 의 `matched` 꼴만 보고** 모의 허브로 WP-1 ~ WP-6 을 먼저 짓는다. 실물이 필요한 것은 앱의 답 키 다시 뽑기(WP-7) · 실물 확인(WP-9)뿐이다 | 계약이 SPEC 에 고정돼 있고 두 응답 꼴이 작다 |
| 허브 바꿔 끼우기 | 허브 WP-4 가 끝나면 코디에게 알린다. **18105 를 새 코드로 다시 띄우는 것은 코디가 앱 새 코드와 함께** 한다 — 옛 앱은 `matched.particle` 을 읽고(`APP clinic_chat/walk/entry.py:70`) 새 허브는 그것을 내지 않는다. 그 전까지 새 앱의 실물 확인은 18106 의 새 허브로 한다 | 사용자 e2e 화면(18220)이 중간에 깨지지 않게 |

## 8. SPEC-001 변경 절 ↔ WP 대응(미대응 0)

**0.5.0**

| 변경(변경 기록의 행) | 절 | WP |
|---|---|---|
| 넓은 후보 | §4-1 · §5-1 R2 · R3 · R7 · R8 · §9 T15 · O-4 | WP-1 · WP-4 |
| 정보 종류 셈 | §4-0 · §4-9 · §5-8 · §9 T16 · 부록 A · O-19 · O-20 | WP-2 · WP-4 |
| 하위 층 자기 행 | §4-4 `roles` · §5-2 표 · §5-3 S5 · S6 · §9 T19 · O-21 | WP-3(동작은 이미 있음 — T19 로 확인 · 주석) |
| 되적기 — 제품 상품 role · `distinct_rows` | §4-0 · §4-4 · §5-2 상품 행 · §9 T17 | WP-3(이미 구현 — 시험 확인) |
| 되적기 — N1-1 `b` 없는 `package_kinds` | §4-6 · §9 T18 | WP-3(이미 구현 — 시험 확인 · 없으면 더함) |
| 되적기 — `request` 의 `null` | §4-0 응답 머리 | WP-2(`coverage.kinds`) · WP-3(단언) |
| `matched.particle` 폐기 · `matched.start` | §4-1 · 부록 A 계산 필드 | WP-1 · WP-4 |

**0.5.1**

| 지적 · 결정 | 절 | WP |
|---|---|---|
| 결정 3 ① · F-1 · N-4 — `overview` / `mechanism` 은 칸 값 · RQ1 과 같은 함수 | §4-9 셈 표 · 불릿 · §5-8 · §9 T16 · 부록 A 개요 칸 줄 | WP-2(칸 상수 · 셈) · WP-4(T3) |
| W-4 — 도구 설명에 하위 role | §4-4 `roles` · §5-3 S2 · §9 T19 | WP-3 |
| W-5 — 적응 세는 식 | §4-9 「세는 식」 | WP-2(`facets` indication 맞춤을 그대로 씀 · 완료 조건 3 의 37 / 34) |
| W-7 — semantic-map 을 바꿔 읽는 자리 | §5 머리 · §5-3 S5 | WP-3(주석 — 허브 동작 변화 없음 · 앱 쪽이 WORK-006 WP-3 · WP-4) |
| W-8 — 한 단으로 놓치는 수 | §5-3 S6 · O-21 | WP-3(주석) · WP-2(셈이 한 단뿐임을 시험이 본다) |

**이번 판에 구현 대상이 아닌 절**: §8 stg · O-3 · O-7 · O-8 · O-11(뒤 단계) · O-15 · O-17(1회차 trace 뒤). SPEC-002 O-15(C 에 주는 도구 수 — `coverage` 포함 8)는 앱 쪽이다(WORK-006 WP-1).

## 9. 열린 것 · 이 문서를 쓰며 본 것(SPEC 은 고치지 않았다)

| # | 무엇 | 이 문서의 제안 | 상태 |
|---|---|---|---|
| A-1 | `matched.covered_by` — 같은 조각이 문장에 **두 번** 나오고 한 번만 긴 조각 안에 들 때. SPEC-001 §4-1 은 「더 긴 맞은 조각 안에 통째로 들어 있으면」 · `start` = 첫 자리까지만 적었다 | **나온 자리가 전부 덮였을 때만** 덮인 것으로 본다(§3). SPEC-002 §9-3c 의 「둘 다 따로 말함 = 둘 다 덮이지 않은 일치」 와 맞고, 틀려도 넓히는 쪽이다(덮이지 않은 것은 앱이 대상으로 둔다) | 구현 때 정함 — SPEC 되적기 후보 |
| A-2 | `coverage` 의 `lineup` 에서 `lower_holders` — §5-8 은 `self` 0 · `lower` = 행 수 · `inherited` `null` 만 적었다 | 「하위 *」 행의 서로 다른 holder 수 | 구현 때 정함 |
| A-3 | `coverage.nodes` 에 같은 노드가 두 번 오면 | 준 대로 두 번 낸다(「`nodes` 순서 그대로」) | 구현 때 정함 |
| A-4 | `coverage` 의 `kinds[]` 순서 | §5-8 표의 행 순서(SPEC-002 §3-2a 표는 순서가 다르다 — 앱은 `kind` 코드로 찾고 순서에 기대지 않는다) | 구현 때 정함 |
| A-5 | 빈 `norm` 의 `g_entry` 행 | 지금 gold 에 있는지 확인하고, 있으면 맞춤에서 건너뛰고 수를 보고한다(빈 문자열은 모든 글의 부분 문자열이다) | 구현 때 확인 |
| O-6 | `coverage.nodes` 상한 | 64 · `GOLD_COVERAGE_NODES_MAX` | SPEC 제안 그대로 |
| O-19 · O-20 | 새 도구 · 종류 14 | 본문 그대로 | 구현 때 정함 / 1회차 trace 뒤 |
| O-22 ① | (`subject`, `holder`) 중복 셈 | WP-3 | 구현 때 정함 |

## 변경 기록

### 0.1.0 (2026-11-16)

- 새로 씀 — SPEC-001 0.5.0 · 0.5.1 의 변경 절을 WP 넷으로. `review-spec-v051.md` §7 의 NOTE 6 은 전부 SPEC-002 쪽이라 WORK-006 에 적었다(허브에 닿는 것은 N-6 의 「`coverage` 셈으로 먼저 견줌」 하나 — 허브 계약은 그대로다).
