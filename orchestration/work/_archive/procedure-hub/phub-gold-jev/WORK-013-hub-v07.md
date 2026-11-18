---
type: work
id: WORK-013
title: "허브 0.7.2 구현 계획 — 줄임 일치(NM) · 시술로 내려가기(DP) · 고민 부위(CS) · 고민 + 부위 거름 / 우선 표시(SP) · 시험 T24 ~ T28 · 두 판 응답 같음"
status: draft
product: procedure-hub
feature: phub-gold-jev
version: 0.2.0
created_at: 2026-11-17
updated_at: 2026-11-17
tags:
  - product/procedure-hub
  - feature/phub-gold-jev
  - doc/work
  - status/draft
links:
  specs:
    - "orchestration/work/phub-gold-jev/SPEC-001-hub-gold-mcp.md (0.7.2 — SP1 기준 넓힘 · 0.7.1 은 검수 PASS(FAIL 0 · WARN 0 · NOTE 4 · review-spec-001-v071.md) · 0.7.2 검수는 앞) ← 계약"
    - "orchestration/work/phub-gold-jev/SPEC-003-hub-gold-db.md (0.1.0 — §5 P1 · P2 · §7 DT10 · 두 판 응답 같음)"
  decisions:
    - "orchestration/work/phub-gold-jev/_RESUME.md §2 (2026-11-17 — 「규칙 변경 = 넣음(지금 · SPEC-001 0.7.2 + WORK-013 WP-3): 고민 + 부위 는 물은 부위가 그 고민의 부위(자기 + 하위) 안에 있을 때만 거름(HG3) · 아니면 거르지 않고 우선 표시(SP)」 — 0.2 의 근거)"
    - "orchestration/work/phub-gold-jev/_RESUME.md §2 (2026-11-17 — 「순차 진행 · 결과만 보고 · 시험은 구현한 것만 돌림(전체 테스트 안 돌림)」 · 「0.7.1 코디 확인: O-30 표지 뜻 넓힘 받음 · O-31 그대로 둠」 · 「① 규칙(사용자 결정)」 · 「SPEC-001 0.7 U7-1~3 = (a)」 · 「WORK-010 B 코디 답」 B-1 접속 값 파일 · B-2 답 키 명세 자리 · 「WORK-011 B 코디 답」 B-1 18105 읽기 됨)"
  related:
    - "orchestration/work/phub-gold-jev/review-spec-001-v07.md (0.7.0 검수 — WARN 6 · NOTE 8 · SPEC 0.7.1 이 닫음)"
    - "orchestration/work/phub-gold-jev/review-spec-001-v071.md (0.7.1 검수 — NOTE N-2 · N-3 을 이 문서 §9 가 받는다)"
    - "orchestration/work/phub-gold-jev/WORK-010-hub-db.md (앞 허브 WORK — 꼴 · 두 판 fixture · 포트 규칙)"
---

# WORK-013 — 허브 0.7.2 구현 계획(NM · DP · CS · SP)

> 경로 접두어: `P` = 프로필 워크트리 · `W` = `$P/orchestration/work/phub-gold-jev` · `SM` = `$P/orchestration/work/_archive/procedure-hub/phub-ledger-redesign/silver-model`(gitignore · 로컬 데이터) · `H` = `~/orca/workspaces/PROCEDURE-HUB/phub-gold-jev`(브랜치 `kknaksss/phub-gold-jev` · HEAD `daa54e3` · 작업 트리 깨끗함 · **이 위에 이어서 짓는다**) · `B` = `$H/backend`.
> **계약은 SPEC-001 0.7.2 이다.** 구현된 것은 0.6 이라 이 문서는 0.7.0 + 0.7.1 + 0.7.2 를 한 번에 받는다(SPEC 변경 기록 0.7.1 · 0.7.2 — 0.7.2 는 SP1 의 기준 한 줄만 바꿨다 · 필드 · 입력 · 이름은 0.7.1 그대로). 이 문서는 「어느 파일을 · 어떤 순서로 · 무엇으로 확인하나」 만 정한다 — SPEC 에 없는 동작을 만들지 않는다. 어긋나는 것을 찾으면 코드를 맞춰 고치지 말고 보고한다(§10).
> **사용자 결정은 닫혔다**: U7-1 ~ U7-3 = (a) · 규칙 SP(「① 규칙」) · O-30 표지 뜻 = (a) 글자 일치 ∪ 묶임(코디가 받음) · **O-31 ① 은 0.7.2 로 닫혔다**(_RESUME §2 11-17 「규칙 변경 = 넣음」 — 물은 부위가 그 고민의 부위 안에 있을 때만 거름). WORK 전에 물을 것 0(SPEC §10).
> Procedure Hub 데이터(원장 · silver · gold)는 공개 정보다(11-17). **비밀값 · 접속 문자열 · 내부 URL 금지는 그대로다.**

## 0. 요약

- 만드는 것 넷: ① **NM** `resolve` 줄임 일치(줄임 열쇠 색인 · `matched.how` · `matched.full` · 입력 `abbr`) ② **DP · CS** `concern_candidates` 의 쪽 밖 목록 `descended[]` · `sites[]`(+ `counts.descended` · `counts.sites` · 입력 `to_procedure`) ③ **SP** `site` 는 **물은 부위가 그 고민의 `sites[]` 안에 있을 때만 거름** — 그 밖은 거르지 않고 표지만(0.7.2 · `site_mode` · `site_applied` · `site_prefer` · `n_site_prefer` · `counts.site_prefer`) ④ **기존 필드 불변 · 두 판 · REST = MCP · 도구 설명 문장 셋** + 실물 확인.
- WP 넷: **WP-1 NM** → **WP-2 DP · CS** → **WP-3 SP** → **WP-4 불변 · 두 판 · 실물 확인 · 마감**. 순서대로 한다(WP-3 의 기준이 WP-2 의 `sites[]` 다 · 셋이 `concern.py` · `headers.py` · `mcp_server.py` 를 함께 고친다).
- **시험 규칙(사용자 11-17)**: WP 마다 **그 WP 의 시험 파일만** 돌린다 · **전체 pytest(`--ignore=tests/integration` 66 파일)는 어느 WP 에서도 돌리지 않는다** · **돌린 파일 목록을 보고에 적는다**(§2 「시험」 줄 · WP 마다 「돌릴 파일」 표).
- 새 입력 0 — gold 15표 · gold 해시 · 보조 입력 · `aux_hash` · DB(18432)의 내용은 그대로다. **적재를 다시 하지 않는다 · alembic 을 돌리지 않는다.**
- 워커는 18107 에만 허브를 띄웠다 내린다. **18105(코디 것 — 지금 0.6 코드 · DB 판)에는 읽기 요청만 보낸다.** 18105 를 새 코드로 다시 띄우는 것 · 앱 답 키 다시 뽑기는 코디 몫이다(§8-2).

## 1. 지금 코드(11-17 확인 — `$B` · HEAD `daa54e3` · 읽기만)

| 파일 | 지금 | 이번에 |
|---|---|---|
| `app/modules/gold/resolve.py`(115줄) | `norm`(`:23-24`) · `_positions`(`:46-52`) · `_covered_by`(`:55-65` — 더 긴 맞은 조각만 본다) · `_match`(`:68-91` — `entry_norms()` 를 돌아 부분 일치 · 정렬 키 `:78` · `matched{span, start, covered_by}` `:88`) · `request` 에 `abbr` 없음(`:90`) | WP-1 — 줄임 맞춤 · `how` · `full` · NM4 덮임 · `abbr` |
| `app/modules/gold/memory.py`(131줄) | `entry_by_norm` · `entry_norms`(`:45-46`) · 보조 ③ 색인 둘(`:91-102`) | WP-1 — **줄임 열쇠 색인 하나**(SPEC §3-1 — 적재 때 한 번 · 두 판이 같은 코드로 짓는다). 그 밖은 안 고친다 |
| `app/modules/gold/repository.py`(231줄) | Protocol **29 메서드**(`:42-79`) · `MemoryGoldRepository`(`:82-223`) · `sites_of_concern` 은 `site_code[]` 만(`:217-219`) · `concern_site_by_site` 는 (`concern_code`, `id`)[](`:213-215`) | WP-1 — 줄임 열쇠 메서드 **둘**(29 → 31 · 이름 제안 — §10 A-2). WP-2 는 새 메서드 0(지금 둘로 묶임 `id` 를 읽는다 — SPEC §3-1 「새 색인 없음」) |
| `app/modules/gold/concern.py`(142줄) | 입력 `concern_code` · `site` · `upper`(`:28-36`) · `site` 거르기(`:49-65` — 맞은 행에만 `site_match` 를 붙인다 `:63-64`) · 묶음 · `modality_only` · `unreached` 가르기(`:70-78`) · `counts` 8칸(`:90-94`) · 쪽 밖 목록 셋은 첫 쪽에만(`:98-101`) · `concern_rows`(`:110-128` — `coverage` 도 부른다) · `bound_concerns`(`:131-142`) | WP-2 · WP-3 |
| `app/modules/gold/headers.py`(124줄) | 계산 필드 상수 `MATCHED_FIELDS`(`:98`) · `HG3_*` · `HG2_FOLLOW_COLUMNS`(`:104-106`) · `INHERITED_FROM_FIELDS` · `SITE_MATCH_BY` · `CONCERN_COUNT_FIELDS`(`:116-118`) | WP-1 ~ WP-3 — 부록 A 의 0.7 · 0.7.1 여섯 줄과 계산 필드 이름을 상수로(시험이 읽는다) |
| `app/modules/gold/service.py`(174줄) | `resolve`(`:62-63`) · `concern_candidates`(`:115-117`) 가 입력을 그대로 넘긴다 | 새 입력 인자만(`abbr` · `to_procedure` · `site_mode`) |
| `app/router/gold.py`(144줄) | `/resolve`(`:48-56`) · `/concern-candidates`(`:100-108`) | 새 쿼리 인자 셋 · 설명 |
| `app/modules/gold/mcp_server.py`(183줄) | `DESCRIPTIONS["resolve"]`(`:34-42`) · `DESCRIPTIONS["concern_candidates"]`(`:75-83` — 끝 문장 「site 로 0 이면 0 그대로」) · 도구 함수(`:137-140` · `:158-161`) | 새 입력 셋 · **도구 설명 문장 셋**(§2 「도구 설명」 줄) |
| `app/swagger_docs/gold.py`(38줄) | `GOLD_API_DESCRIPTION` 의 `resolve` · `concern-candidates` 불릿 | WP-4 — 문구만 |
| `app/modules/gold/coverage.py` | `asked_rows` · `concern_rows` 를 부른다(`:19` · `:127-128`) | **안 고친다** — 셈은 그대로다(DP8 · T16). `concern_rows` 의 부르는 꼴 · 돌려주는 것을 바꾸지 않는다 |
| `tests/gold_fixture.py`(322줄) | `write_fixture(root, holes=False)`(`:288`) — 기본 판 · `holes` 판. 기본 판: 묶임 `CON-904` ↔ `SITE-903` 하나(`:52`) · `PKG-901` 「구성 항목」 → `PRC-901`(`:121`) · `M9` 「하위 시술」 → `PRC-901` · `PRC-902`(`:118-119`) · `CON-901` 의 「계열 층만」 · 「패키지 — 항목 코드 없음」 행(`:161-162`) | 새 선택지 `v07`(이름 제안) — 기본 판 · `holes` 판은 **한 줄도 안 바꾼다** |
| `tests/medallion_fixture.py`(184줄) | `write_medallion_fixture(root, holes)`(`:128`) · `build_db(root, holes, db_name)`(`:174`) | `v07` 를 그대로 넘기는 인자만 |
| `tests/test_gold_contract.py`(195줄) | `ROW_COMPUTED`(`:41`) · `check_response`(`:72-112` — `matched` 는 `MATCHED_FIELDS` 와 **꼭 같아야** `:78` · 묶음 열쇠 = 머리 7 + `n_rows` · `rows` `:95` · `counts` = `CONCERN_COUNT_FIELDS` `:100`) | WP 마다 그 WP 가 더한 필드만큼 |
| `tests/test_gold_mcp.py`(126줄) | `SAME`(`:54-69`) — `test_medallion_repo.py:28` 이 가져다 DT10 에 쓴다(`:111`) | WP-4 — 표본 더하기 |
| `tests/test_medallion_repo.py`(290줄) | `test_dt9_same_memory_index`(`:83-90` — `_m` 의 색인 8 을 두 판에서 견준다) · `test_dt10_tool_responses_equal`(`:105-122`) | WP-1(색인 이름 하나) · WP-4(N-3 표본) |

듣는 포트(11-17 `lsof`): 18105 · 18106 · 18210 · 18220 · 18222 · 18432. **18107 은 비어 있다.**

## 2. 공통

| 항목 | 이번 판 |
|---|---|
| allowed_paths(허브 레포) | **새 파일**: `backend/app/modules/gold/descend.py`(DP 따라가기 — `concern.py` 에 둬도 된다 · §10 A-1) · `backend/tests/test_gold_v07_resolve.py` · `test_gold_v07_descend.py` · `test_gold_v07_site.py` · `test_gold_v07_compat.py`(이름은 제안) / **고치는 파일**: `backend/app/modules/gold/{resolve,concern,memory,repository,headers,service,mcp_server}.py` · `backend/app/router/gold.py` · `backend/app/swagger_docs/gold.py` · `backend/tests/{gold_fixture,medallion_fixture}.py` · `backend/tests/{test_gold_contract,test_gold_mcp,test_gold_tools_synthetic,test_gold_holes,test_medallion_repo}.py`(§2 「기존 시험」 줄의 자리만) · `backend/README.md`(gold 절) |
| 손대지 않는 것 | `backend/app/main.py` · `backend/app/core/**`(`test_gold_rest.py:74-85` 가 막는다) · `app/model/**` · `alembic/**` · `scripts/**` · `gold_main.py` · `config.py` · `inputs.py` · `db_inputs.py` · `medallion_load.py` · `silver_contract.py` · `closure.py` · `coverage.py` · `facets.py` · `pairs.py` · `core.py` · `cursor.py` · `kinds.py` · `ledger.py` · `ranges.py` · `pyproject.toml` · `uv.lock`(새 의존 0) · `.github/**` |
| 데이터 | 로컬 `$SM/gold` · `$SM/silver` · `$SM/notes/ledger-check-list.csv`. **CSV · 응답 dump 를 허브 레포에 넣지 않는다**(대조용 응답은 세션 임시 폴더) |
| **시험**(사용자 11-17 「구현한 것만 · 전체 안 돌림」) | ① WP 마다 **「돌릴 파일」 표의 파일만** 돌린다 — 그 WP 의 새 시험 파일 + 그 WP 가 **고친** 기존 시험 파일. ② **전체 pytest(`uv run pytest --ignore=tests/integration`)는 돌리지 않는다** — WP-4 에서도. ③ 보고에 **돌린 파일 목록 · 통과 · skip 수**를 WP 마다 적는다. ④ 명령 꼴: `DATABASE_URL=sqlite+aiosqlite:///:memory: uv run pytest <파일들> -q -rs`(README `:111-115`) — 실물 시험은 데이터 env 넷이 없으면 skip 이므로 **env 넷을 준 채** 돌린다(env 이름은 README gold 절). ⑤ `ruff` 는 고친 파일에만: `uv run ruff check <고친 파일들>` |
| **기존 시험** — 기본값이 바뀌어 기대가 달라지는 자리(grep 으로 센 것 · 이 밖에서 깨지면 고치지 말고 보고) | ⓐ `test_gold_tools_synthetic.py:71-73` · `:87` — `matched` 를 dict 통째로 견준다 → `"how": "부분"` 을 더한다(새 필드) ⓑ `test_gold_tools_synthetic.py:279-282` — 기본 판에서 `CON-901` 은 묶인 부위가 없다(자기 · 하위 0) → 기본값 `auto` 면 `prefer` 가 되어 「2 행」 · 「`total` 0」 이 안 선다 → **두 호출에 `site_mode="filter"` 를 준다**(SP7 — 0.7.0 과 같은 응답을 보는 길 · 0.6 기대를 그대로 지킨다) ⓒ `test_gold_holes.py:320-325` `test_T22_with_inherit` — `holes` 판의 `CON-905` 는 묶인 부위가 없다 → `prefer` 로 바뀐다. 물려받은 `CON-902` 의 행이 전부 묶임으로 맞아 지금 단언은 그대로 설 것으로 **보인다 — 돌려서 확인한다**(안 서면 `site_mode="filter"` 로) ⓓ `test_gold_contract.py:41` · `:78` · `:95` · `:100` — 새 계산 필드 ⓔ `test_medallion_repo.py:87` — 견주는 색인 목록에 줄임 열쇠 색인 ⓕ 합성 fixture 의 낱말 둘 이름 때문에 기존 `resolve` 시험에 `줄임` 후보가 새로 붙거나 `covered_by` 가 달라지면 → 그 시험은 **`abbr="off"`** 로 0.6 기대를 지킨다(NM6) — 줄임 기대는 새 파일에만 쓴다 ⓖ **(0.2 — 0.7.2 로 grep 다시)** `test_gold_holes.py:299-305` `test_T22_unbound_is_051` · `:314-317` `test_T22_other_site_does_not_pick_bound` — `holes` 판에서 `CON-901` · `CON-902` 의 `sites[]` 는 `SITE-902`(「부위나」) 하나다. 「부위가」(`SITE-901` — 그 고민의 부위가 아닌 부위) · 「부위없음」(부위 입구에 없는 글자)으로 건 호출 자리 셋(`:301` 의 두 짝 · `:304` · `:316`)은 0.7.2 에서 `prefer` 가 된다(0.7.1 이었다면 `filter` 그대로였다) → **그 셋에 `site_mode="filter"` 를 준다** — 「글자 일치만」 · 「0 이면 0 + `unfiltered_rows`」 · 「다른 부위로는 묶임으로 안 맞는다」 는 `filter` 길의 성질이라 0.5.2 기대를 그대로 지킨다(`prefer` 기대는 새 파일에만 쓴다). **0.7.2 로도 안 바뀌는 자리**(grep — `site` 를 건 호출 전부): `test_gold_holes.py:285` · `:310` · `:336`(`CON-901` · `CON-902` × 「부위나」 — 안 부위 → `filter`) · `:568` · `:583` · `:600` · `:649`(실물 — 전부 묶인 고민 · 그 윗고민 × 그 부위 → `filter`) · `test_gold_mcp.py:63` · `test_gold_tools_synthetic.py:279` · `:281`(기본 판 `CON-901` 은 `sites[]` = `[]` → `prefer` — ⓑ 그대로) · `test_gold_holes.py:322`(ⓒ 그대로) · `test_gold_tools_synthetic.py:443` · `test_gold_mcp.py:95`(빈 `site` — 오류 길). **고친 시험 이름 · 줄 · 까닭을 보고에 목록으로 낸다** |
| **도구 설명**(MCP — SPEC §4-1 · §4-5 · 검수 W-3) | 뜻이 들어 있어야 하는 문장 셋. 문구는 다듬어도 되지만 시험이 찾는 조각은 그대로 둔다: ① `resolve` — 「`matched.how` = `줄임` 인 후보는 글자 그대로 맞은 것이 아니라 줄여 말한 꼴로 맞은 것이다 — 질문이 그것을 가리키는지 확인하고 쓴다」(T26) ② `concern_candidates` — 「`descended[]` 의 묶음은 계열 단위다(`unit` = `계열`) — 그 안의 시술 하나하나가 그 적응을 자기 것으로 가진 것이 아니라 `from[]` 의 행이 말한 층(계열 · 메뉴 · 제품)의 것이다」(T24) ③ `concern_candidates` — 「`site_applied` = `prefer` 면 부위로 거르지 않은 응답이다 — `site_prefer` = `false` 인 행은 그 부위의 것이라고 말한 행이 아니다」(T28). 지금 끝 문장 「site 로 0 이면 0 그대로」(`mcp_server.py:82`)는 「`site_applied` = `filter` 일 때」 로 고친다. **기존 시험이 찾는 조각**(`test_gold_holes.py:359-360` — `inherited_from` · `hier{asked_code, match: 상위}` · 「그 부위에 묶인 고민 · 그 하위 고민」 / `test_gold_mcp.py:44-45` — 「고르지 않고」 · 「부분 문자열」 · 「조사를 떼지 않는다」)은 지우지 않는다 |
| 새 입력 셋 | `resolve.abbr`(`on` \| `off` · 기본 `on`) · `concern_candidates.to_procedure`(`auto` \| `none` · 기본 `auto`) · `concern_candidates.site_mode`(`auto` \| `filter` · 기본 `auto`). **셋 다 `request` 에 싣는다** — cursor 서명에 들어간다(`cursor.py:21-23`). `resolve` 맞춤 꼴은 쪽 넘김이 없어 `abbr` 은 목록 꼴에서 뜻이 없다 — 목록 꼴에 `abbr` 을 주면 무시할지 `invalid_argument` 일지는 §10 A-3. `site` 가 없으면 `site_mode` 는 무시한다(SPEC §4-5) |
| 포트 | 시험은 포트 없이(ASGI transport). 서버 확인은 **18107 만** — 띄우기 전 `lsof -nP -iTCP:18107 -sTCP:LISTEN` 으로 비었는지 본다(비어 있지 않으면 **멈추고 보고**). 18105 · 18106 · 18210 · 18220 · 18222 · 18005 는 내리거나 띄우지 않는다. PostgreSQL 컨테이너(18432)를 내리거나 다시 만들지 않는다 |
| 접속 값 | DB 판 확인(§8-1 ③)에만 쓴다. 코디가 정한 방법 그대로 — 레포 밖 접속 값 파일을 `set -a; . <파일>; set +a` 로 **프로세스 env 에 올리기만** 한다(_RESUME §2 11-17 「WORK-010 B 코디 답」 B-1). 내용을 화면 · 로그 · 보고에 찍지 않는다(`cat` · `echo` 금지) |
| 커밋 | 안 한다 — 워크트리에 변경만 남긴다(코디 몫) |

## 3. WP-1 — NM · `resolve` 줄임 일치

**SPEC**: §3-1 「줄임 열쇠」 줄 · §4-1(`matched.how` · `matched.full` · `covered_by` · 「줄임 일치」 불릿) · §5-1 R9 · §5-11 NM1 ~ NM6 · 「셈」 · 부록 A 「0.7 NM」 줄 · §9 T26 · O-29(값은 본문 그대로).

| 만들 · 고칠 것 | 어디 | 내용 |
|---|---|---|
| 줄임 열쇠 짓기 | `memory.py`(색인) — 짓는 함수는 `resolve.py` 또는 `memory.py` 한 곳에만(식 두 벌 금지) | NM1: `g_entry.text` 를 공백으로 나눈 낱말이 2 이상인 행마다 — 끝 낱말 통째 · 앞 낱말은 저마다 「앞에서 2 글자 이상 자른 접두(통째 포함)」 · **한 글자 낱말은 통째로** · 순서 그대로 이어 붙여 소문자로(R1 식 — `resolve.norm` 과 같은 식을 쓴다) · 그 행의 `norm` 과 같은 것은 뺀다 · **열쇠 길이 4 글자 이상**(NM3 ⑥ — 상수 하나 · O-29). 색인 = 열쇠 → `g_entry` 행[] |
| repository | `repository.py` | 메서드 둘(이름 제안 `abbr_keys()` · `entries_by_abbr(key)`) — Protocol **29 → 31**. SPEC-003 §5 P1 의 「메서드 29」 는 되적기 후보로 보고한다(SPEC 은 안 고친다 — §10 A-2) |
| 맞춤 | `resolve.py` `_match` | NM2: 질문 `norm` 안에 열쇠가 부분 문자열로 들어 있으면 그 행이 후보. NM5: 같은 (`entity_table`, `entity_code`) 가 `부분` 으로 이미 후보면 `줄임` 으로 다시 내지 않는다 · 한 열쇠가 개념 여럿이면 전부(`ambiguous` 에 함께 센다) |
| `matched` | 같은 곳 · `headers.py` | **모든 후보에 `how`**(`부분` \| `줄임`). `줄임` 이면 `span` = 맞은 **열쇠** · `start` = 그 열쇠의 첫 자리 · **`full` = 그 행의 `norm`**. **`부분` 후보에는 `full` 을 싣지 않는다**(T27 — `abbr` = `off` 응답이 `how` 만 빼면 0.6 과 같은 JSON 이어야 한다). 상수: `부분` 의 열쇠 = (`span`, `start`, `covered_by`, `how`) · `줄임` 은 + `full`(순서 제안 — §10 A-4) |
| 덮임(NM4) | `_covered_by` 를 부르는 자리 | 「더 긴 맞은 조각」 의 집합에 줄임으로 맞은 조각(`span`)도 넣는다 — `부분` 후보도 `줄임` 후보도 같은 식 하나로(「나온 자리가 전부 덮였을 때만」 그대로). `abbr` = `off` 면 줄임 조각이 없으니 0.6 과 같은 값이다 |
| 순서 | `_match` 의 정렬 키(`:78`) | 조각 길이 = `matched.span` 글자 수 내림차순(식 그대로) · **같은 자리에서는 `부분` 이 `줄임` 앞**(SPEC §4-1) · 그 밖의 키는 그대로 |
| 입력 `abbr` | `resolve.py` · `service.py:62-63` · `router/gold.py:48-56` · `mcp_server.py:137-140` | `ctx.enum` 으로 검사(`on` · `off` · 기본 `on`) · `request` 에 싣는다. `off` = NM 이 돌지 않는다(NM6) |
| 도구 설명 | `mcp_server.py` `DESCRIPTIONS["resolve"]` | §2 문장 ① + `matched{span, start, covered_by, how, full}` · `abbr` 한 마디 |
| fixture | `tests/gold_fixture.py` 의 `v07` 판 | 가짜 이름으로: 낱말 둘 이름(앞 낱말 3 글자 이상) · 앞 낱말이 **한 글자**인 이름 · 낱말 셋 이름 · 한 낱말 이름(줄임 없음 확인용) · 끝 낱말이 다른 입구의 `norm` 과 같은 이름(「끝 낱말만 맞던 후보」 가 덮이는 꼴) · **이름 A 안에 이름 B 의 줄임 열쇠가 든 짝** · 긴 줄임 조각 안에 짧은 줄임 열쇠가 든 짝 · 한 열쇠가 개념 둘에 닿는 짝 |

**완료 조건**(T26)
1. 합성: 직접 지은 열쇠 집합 = 색인의 열쇠 집합(시험이 NM1 식을 **따로** 한 번 더 짓는다 — 구현 함수를 다시 부르지 않는다).
2. 낱말 둘 이름의 앞 낱말을 2 글자로 줄인 문장 — 띄어 쓴 꼴 · 붙여 쓴 꼴 · 조사 붙은 꼴 → 그 개념이 `how` = `줄임`(`span` = 열쇠 · `full` = 그 행의 `norm`)으로 나오고, 끝 낱말만 맞던 후보에 `covered_by` = 그 줄임 조각이 붙는다(빠지지 않는다).
3. **한 낱말 이름의 앞 글자만 같은 말 → 후보 0** · 끝 낱말을 줄인 말 → 안 맞음 · 낱말을 뺀 말 · 순서를 바꾼 말 → 안 맞음 · 길이 4 미만 열쇠는 없다.
4. 앞 낱말이 한 글자인 이름 — 그 낱말을 통째로 둔 열쇠가 지어진다.
5. 이름 A 를 그대로 말한 문장 → B 가 `줄임` 후보로 나오되 `covered_by` = A 의 조각 · 긴 `줄임` 조각 안에 든 짧은 `줄임` 후보에도 `covered_by` 가 붙는다.
6. 같은 개념이 `부분` 이면 `줄임` 으로 다시 안 나온다 · 한 열쇠가 개념 둘이면 둘 다 + `ambiguous`.
7. `abbr="off"` → 전 후보 `how` = `부분` · `how` 를 빼면 `abbr` 인자를 안 받던 0.6 의 응답과 같다(합성 — 후보 · 순서 · `covered_by`) · `abbr="x"` → `invalid_argument`.
8. **실물**(데이터 env): 열쇠 수 = **2,881**(하한 없이 지으면 2,885) · 닿는 개념 533 · 37 문항(로컬 `questions.csv` 의 질문 — `gold_support.real_questions`)에서 `abbr` = `on` 과 `off` 의 응답이 `matched.how` 칸만 빼고 같다(새 후보 0).
9. `tools/list` 의 `resolve` 설명에 §2 문장 ① 의 조각(「글자 그대로 맞은 것이 아니라」)이 있다 · 입력 스키마에 `abbr` 이 있다.

**돌릴 파일**

| 파일 | 왜 |
|---|---|
| `tests/test_gold_v07_resolve.py` | 새 시험(위 1 ~ 9) |
| `tests/test_gold_tools_synthetic.py` | 고친다(§2 ⓐ · ⓕ) — 두 판(`csv` · `db`)으로 돈다 |
| `tests/test_gold_contract.py` | 고친다(`matched` 꼴) |
| `tests/test_medallion_repo.py` | 고친다(§2 ⓔ — 줄임 열쇠 색인이 두 판에서 같다) |
| `tests/test_gold_coverage.py` | 안 고친다 — `resolve` 응답을 읽는다(`:391`)라 한 번 돌려 본다 |

## 4. WP-2 — DP · CS · `concern_candidates` 의 `descended[]` · `sites[]`

**SPEC**: §3-1 「시술로 내려가기」 · 「고민 부위」 줄(새 색인 없음) · §4-0 쪽 밖 목록 표의 `concern_candidates` 줄 · §4-5(`to_procedure` · `descended[]` · `sites[]` · `counts.descended` · `counts.sites` · 「`descended[]` 의 꼴」 표 · `from[].lands` 줄 · 「0.7 — 쪽 밖 목록」 불릿) · §5-11 DP1 ~ DP9 · CS1 ~ CS6 · 「셈」 · 부록 A 「0.7 DP」 둘 · 「0.7 CS」 둘 · §9 T24 · T25 · O-27(이름 · 꼴은 본문 그대로) · O-28(한계 — 구현 대상 아님).

| 만들 · 고칠 것 | 어디 | 내용 |
|---|---|---|
| 내려가기 | 새 `descend.py`(또는 `concern.py`) | DP1: 대상 = **이 응답의** `modality_only[]` · `unreached[]` 행 전부(`site` 로 거른 뒤 · HG1 로 물려받았으면 그 행). DP2: 행의 (`target_table`, `target_code`) 에서 `repo.scope_by_subject` 만 따라 — 패키지 → role 「구성 항목」 holder / 제품 → role 「물려받음」 holder 가운데 가장 좁은 층 하나(케이스 → 시술 → 계열) / 케이스 → role 「물려받음」 의 시술 / 계열 → 그대로. 계열에 닿으면 그 계열의 role 「하위 시술」 holder 전부. silver 를 더 읽지 않는다 · 관계를 만들지 않는다 |
| `descended[]` 항목 | 같은 곳 | 한 항목 = 계열 하나: `modality_code` · `modality_name` · `unit`(고정값 `계열`) · `procedures[]{procedure_code, procedure_name, scope_gid, in_groups}` · `from[]{gid, reach, lands, procedure_codes, path[]{table, code, name, role, scope_gid}}`. `in_groups` 는 **쪽과 무관하게** 이 조회의 `groups` 전체와 견준다. `path[]` 첫 항목 = 행의 대상(`role` · `scope_gid` 는 `null`) |
| `lands` = `procedure`(실물 0 · 합성으로만) | 같은 곳 | SPEC §4-5 `from[].lands` 줄 그대로 — ① 닿은 시술의 계열 묶음(그 시술을 `subject` 로 둔 role 「물려받음」 의 계열 holder · 계열 둘이면 묶음 둘) ② `procedures[]` 는 그 계열의 시술 전부 그대로 · 닿은 시술은 `from[].procedure_codes[]` 로만 ③ `unit` 은 `계열` 그대로 · `path[]` 끝 항목 = 닿은 시술(계열은 넣지 않는다). `lands` = `modality` 면 `procedure_codes` 는 `null`. **계열이 없는 시술에 닿으면 못 내린 행이다**(DP9) |
| 못 내린 행(DP9) | 같은 곳 | `unreached[]` 에 그대로 두고 `counts.descended.undescended` 에 센다 |
| 순서(DP7) | 같은 곳 | `descended[]` = 계열의 `g_scope` 「자기」 행 `gid` 글자 순(없으면 `modality_code`) · `procedures[]` = `scope_gid` · `from[]` = `gid` · 같은 행이 한 계열에 여러 길이면 `scope_gid` 열이 작은 길 하나 · 한 행이 계열 둘이면 두 묶음에 다 |
| `counts.descended` | `concern.py` · `headers.py` | `{rows, modalities, procedures, new_procedures, undescended}` |
| 입력 `to_procedure` | `concern.py` · `service.py:115-117` · `router/gold.py:100-108` · `mcp_server.py:158-161` | `auto`(기본) \| `none`. **`none` 이면 `descended` · `counts.descended` 두 필드를 뺀다**(`null` · `[]` 로 싣지 않는다 — DP8). `request` 에 싣는다 |
| `sites[]`(CS) | `concern.py` | CS1: 물은 고민(`match` = `직접`) + 그 자손 고민(`repo.descendants("concern", code)` — `match` = `하위`)의 묶임 행마다 한 항목. 묶임 행 = `repo.sites_of_concern(c)` 의 부위마다 `repo.concern_site_by_site(site)` 에서 `concern_code` 가 `c` 인 (`concern_code`, `id`) — **새 색인 · 새 메서드 0**. CS2: `{site_code, site_name, concern_code, csi_id, match}` · `site_name` = `g_entry` 의 (site, 코드) `entity_name`(`bound_concerns` 가 이름 → 코드를 읽는 것과 같은 표 · 거꾸로). CS3: HG1 로 물려받은 응답에서도 **물은 고민 기준**. CS4: `site` 로 거르지 않는다. CS5: 순서 `match`(`직접` 먼저) → `site_code` → `csi_id` · 접지 않는다. 없으면 `[]`(필드를 빼지 않는다) |
| `counts.sites` | `concern.py` · `headers.py` | `{direct, lower, distinct_sites}` — `direct` · `lower` 는 항목 수 |
| 쪽 밖 목록 | `concern.py:98-101` 꼴 | `descended` · `sites` 는 **첫 쪽에만** 싣는다 · `counts.descended` · `counts.sites` 는 `counts` 안이라 모든 쪽에 |
| 안 바뀌는 것(DP8 · CS6) | — | `groups[]` · `modality_only[]` · `unreached[]` · `total` · 기존 `counts` 8칸 · `inherited_from` · `ledger_check[]` · 행의 칸. 내린 시술을 `groups` 에 섞지 않는다 · 내린 행을 두 목록에서 빼지 않는다. `coverage` 의 셈도 그대로 |
| 도구 설명 | `mcp_server.py` `DESCRIPTIONS["concern_candidates"]` | §2 문장 ② + `to_procedure` · `sites[]` 한 마디 |
| fixture(`v07` 판) | `tests/gold_fixture.py` | 가짜 코드로: 계열을 「구성 항목」 으로 둔 패키지(메뉴 꼴) + 그 패키지에만 닿은 고민(묶음 0 → 내린 뒤 시술 ≥ 1) · 「물려받음」 holder 가 계열뿐인 제품 + 「제품 — 케이스 없음」 행 · **`g_scope` 로 어디에도 안 닿는 대상**(못 내린 행) · **계열이 없는 시술을 「구성 항목」 으로 둔 패키지**(`lands` = `procedure` 인데 못 내림) · 자기 묶임이 있는 고민 · 하위 고민에만 묶임이 있는 윗고민 · 묶임이 없는 고민 · 한 부위가 고민 둘에 묶인 꼴. 기본 판에 이미 있는 것도 쓴다 — `PKG-901` 「구성 항목」 → `PRC-901`(계열 `M9` 가 있는 시술 = `lands` = `procedure` 의 정상 꼴) · `M9` 「계열 층만」 |

**완료 조건**(T24 · T25)
1. 합성 — `descended[]` 의 시술 집합 = 그 응답의 `modality_only[]` · `unreached[]` 행을 **시험이 DP2 로 직접 따라가 센 것**(`lands` = `modality` 행 기준) · `procedure` 행은 `procedure_codes[]` 로 견준다.
2. `procedures[].procedure_code` 는 전부 `g_scope` 의 procedure holder(패키지 · 제품 · 계열 코드 0) · `groups[].candidate_table` ∈ {`procedure`, `procedure_case`} · 메뉴 · 패키지 · 제품 이름은 `from[].path[]` 에만.
3. `path[]` 의 `scope_gid` 가 전부 실재하는 `g_scope` 행이고 그 role 이 DP2 의 role · `from[].gid` ⊂ 그 응답의 `modality_only[]` ∪ `unreached[]` · `in_groups` = `groups` 전체와 대조(쪽을 1 로 넘겨도 같다).
4. `lands` = `procedure` 합성 — 닿은 시술의 계열 묶음에 들어가고 `procedures[]` 는 계열의 시술 전부 · `procedure_codes[]` = 닿은 시술만 · `unit` = `계열` · 계열 없는 시술이면 `undescended` 1 + 그 행이 `unreached[]` 에 그대로.
5. `to_procedure="none"` → `descended` · `counts.descended` **두 열쇠가 없다**(`in` 으로 본다) · 나머지는 `auto` 응답에서 두 열쇠를 뺀 것과 같다 · `to_procedure="x"` → `invalid_argument` · 행이 0 인 응답은 `descended` = `[]`.
6. `sites[]` = 보조 ③ 에서 물은 고민 · 그 자손의 묶임 행을 직접 센 것 · `match` · 순서(CS5) · `site_name` · 묶임 없는 고민은 `[]` · HG1 로 물려받은 응답에서도 물은 고민 기준 · **`site` 를 걸어도 `sites[]` 는 같다** · `counts.sites` = 직접 센 수.
7. 결정론 — 같은 입력 두 번 → `descended[]` · `sites[]` 순서까지 같다 · 둘째 쪽부터는 두 열쇠가 없다 · 0.6 에서 만든 꼴의 cursor(`request` 에 `to_procedure` 없음)는 `cursor_invalid`.
8. **실물**(데이터 env · 고민 260 전부): 완료 조건 1 ~ 3 · 6 이 전 고민에서 선다 · 묶음 0 이던 **41** 고민 전부에 내린 시술 ≥ 1 · `counts.descended.undescended` 합 **0** · 내린 것이 있는 고민 **142** · 고민당 최대 **107**(`CON-226` · 계열 6) · `CON-168` → 계열 1(`M18`) · 시술 6(`PRC-123` ~ `PRC-128`) · `sites[]` 가 있는 고민 **100**(자기 85) · 항목 수 최대 23(서로 다른 부위 18) · `CON-168` 의 `sites[]` = `SITE-072` 1 항목(`CSI-0054`).
9. `tools/list` 의 `concern_candidates` 설명에 §2 문장 ② 의 조각(「계열 단위」 · 「시술 하나하나가」)이 있다 · 입력 스키마에 `to_procedure` 가 있다.

**돌릴 파일**

| 파일 | 왜 |
|---|---|
| `tests/test_gold_v07_descend.py` | 새 시험(위 1 ~ 9) |
| `tests/test_gold_contract.py` | 고친다(묶음 밖 새 열쇠 · `counts` 칸) |
| `tests/test_gold_holes.py` | 안 고친다(이 WP 에서는) — `concern.py` 를 고쳤으므로 T20 · T22 가 그대로 서는지 본다 |
| `tests/test_gold_tools_synthetic.py` | 안 고친다(이 WP 에서는) — `concern_candidates` 기존 시험 |
| `tests/test_gold_coverage.py` | 안 고친다 — `concern_rows` 를 함께 쓴다(T16 그대로) |

## 5. WP-3 — SP · 고민 + 부위: 거름 / 우선 표시

**SPEC**: §4-5(`site` 줄의 0.7.1 문장 · `site_mode` · `site_applied` · `site_prefer` · `n_site_prefer` · `counts.site_prefer` · 「`site` 로 걸러 0」 불릿 · 「`prefer` 일 때의 셈」 불릿) · §5-9 HG3-7 · §5-11 SP1 ~ SP8(**SP1 · SP6 = 0.7.2**) · 「셈」 · 부록 A 「0.7.1 SP」 줄 · §9 T28 · T22(문장) · O-30 = (a) · O-31(① 은 0.7.2 로 닫힘 = SP1 · ② ~ ④ 는 한계 — 구현 대상 아님).

| 만들 · 고칠 것 | 어디 | 내용 |
|---|---|---|
| 기준(SP1 — **0.7.2**) | `concern.py` | `site` 가 있고 `site_mode` = `auto` 일 때: **물은 부위의 코드가 물은 고민의 `sites[]` 의 `site_code` 안에 있으면 `filter` · 없으면 `prefer`.** 「물은 부위의 코드」 = `site` 글자와 `entity_name` 이 글자 그대로 같은 site 입구의 코드 — `bound_concerns`(`concern.py:131-142`)가 읽는 것과 **같은 표 · 같은 식**(`entries_by_table("site")`)이다(새 메서드 0). `sites[]` 가 `[]` 이면 늘 `prefer`(0.7.1 의 기준은 이 한 경우였다) · **부위 입구에 없는 글자는 코드가 없으므로 `prefer`** · `match` 가 `직접` 이든 `하위` 든 「안」 이다 · 부위 계층으로 넓히지 않는다. `site_mode` = `filter` 면 늘 `filter`(SP7). HG1 로 물려받은 응답에서도 기준은 **물은 고민**의 `sites[]`. **`sites[]` 를 세는 함수는 WP-2 의 것 하나만 쓴다**(`to_procedure` 와 무관 · `site` 와 무관) |
| `prefer`(SP2 ~ SP5) | `concern.py:49-65` | 행을 빼지 않는다 — `rows` = `all_rows`. **모든 행**(`groups[].rows[]` · `modality_only[]` · `unreached[]`)에 `site_prefer`(`true` \| `false`) — `true` = 지금 거르기가 남기는 행(글자 일치 ∪ 묶임 — 같은 판정 코드 하나). `true` 인 행에만 `site_match[]`(0.5.2 꼴 그대로). 묶음에 `n_site_prefer` · `counts.site_prefer{rows, groups}` · `counts.by_site_match` 는 표지 행으로 센다 · `counts.rows` = `counts.unfiltered_rows` · `total` · `descended[]` 는 `site` 를 안 건 조회와 같다. **순서를 바꾸지 않는다**(SP4) · 표지 0 이어도 그대로 낸다(SP5) |
| **N-2 — `site_match` 의 꼴 하나** | 같은 곳 | **`site_prefer` = `false` 인 행에는 `site_match` 필드가 없다**(`[]` 로 싣지 않는다). 0.5.2 의 꼴 — 맞은 행에만 붙고 비어 있지 않다(`concern.py:63-64` · `test_gold_contract.py:63-64` 의 `assert r["site_match"]`) — 과 하나로 맞춘다. SPEC §4-5 `site_prefer` 줄 되적기 후보(§10 A-5) |
| `filter`(SP6) | 같은 곳 | 물은 부위가 `sites[]` 안에 있는 짝 · `site_mode` = `filter` — 0.7.0 과 같은 응답(지금 코드의 거르기 그대로) + 머리 `site_applied` = `filter` · `counts.site_prefer` = `null`. **`site_prefer` · `n_site_prefer` 필드는 없다** |
| `site` 없음 | 같은 곳 | `site_applied` = `null` · `counts.site_prefer` = `null` · `site_mode` 는 무시(검사는 한다 — enum 밖이면 `invalid_argument`) |
| 입력 `site_mode` | `concern.py` · `service.py` · `router/gold.py` · `mcp_server.py` | `auto`(기본) \| `filter` · `request` 에 싣는다 |
| 상수 | `headers.py` | `CONCERN_COUNT_FIELDS` 에 `descended`(WP-2) · `sites`(WP-2) · `site_prefer` · `site_applied` 의 어휘 · 부록 A 「0.7.1 SP」 줄의 칸(`site_name` · `case_site_name` · `concern_code` — 지금 `HG3_MATCH_COLUMNS` 와 겹친다) |
| 도구 설명 | `mcp_server.py` | §2 문장 ③ + `site_mode` 한 마디 · 끝 문장을 「`site_applied` = `filter` 일 때 0 이면 0 그대로」 로 |
| fixture(`v07` 판) | `tests/gold_fixture.py` | **묶임 없는 고민에 부위 글자가 적힌 행 둘 · 안 적힌 행 둘**(T28 합성) · 묶임 없는 고민인데 윗고민이 그 부위에 묶인 꼴(묶임으로만 표지 — O-30 (a)) · 행 0 이라 물려받는 묶임 없는 고민 · 묶임 있는 고민 + 자기 부위(회귀 — `filter`) · **(0.2) 묶임 있는 고민 + 그 고민의 부위가 아닌 부위(`prefer` — 부위 글자가 적힌 행 · 안 적힌 행이 함께 있게)** · **하위 고민에만 묶임이 있는 윗고민 + 그 부위(`filter`) · + 다른 부위(`prefer`)** · 행 0 이라 물려받는 **묶임 있는** 고민 + 자기 부위(`filter`). `holes` 판에 이미 있는 것도 쓴다 — `CON-901` · `CON-902` 의 `sites[]` = `SITE-902` · 「부위가」 가 밖 부위다 |

**완료 조건**(T28 · T22)
1. 합성 — 묶임 없는 고민 + 부위: `site_applied` = `prefer` · 행 넷 다 나오고 표지 둘 · 행 · 묶음 · 순서 · `total` · `descended[]` 가 `site` 를 안 건 조회와 같다(새 필드를 빼고 견준다).
2. `site_prefer` = `true` 인 행 집합 = **같은 조회를 `site_mode="filter"` 로 불러 나온 행 집합** · 그 행의 `site_match[]` 도 같다 · `false` 행에는 `site_match` 열쇠가 없다(N-2).
3. `n_site_prefer` · `counts.site_prefer` · `counts.by_site_match` = 직접 센 수 · 표지 0 인 짝도 `200` · 행 전부 · `counts.site_prefer.rows` = 0.
4. 묶임 있는 고민 + **그 고민의 부위(자기 또는 하위 고민의 묶임)**: `site_applied` = `filter` · `site_prefer` · `n_site_prefer` 열쇠가 없다 · 0 이면 0 + `unfiltered_rows` · 새 열쇠(`site_applied` · `counts.site_prefer`)를 빼면 `site_mode="filter"` 응답과 같다. **(0.2 — 0.7.2) 같은 고민 + 그 고민의 부위가 아닌 부위: `site_applied` = `prefer`** · 행 전부 · 완료 조건 1 ~ 3 이 그 짝에서도 선다 · 같은 조회를 `site_mode="filter"` 로 부르면 0.7.0 응답이다(0 이면 0 + `unfiltered_rows`) · **`site_applied` = `filter` ⇔ 물은 부위의 코드 ∈ 그 응답 `sites[]` 의 `site_code`**(시험이 직접 센다) · 부위 입구에 없는 글자 → `prefer`.
5. `site` 없음 → `site_applied` = `null` · `site_mode="filter"` + 묶임 없는 고민 → 걸러진다 · `site_mode="x"` → `invalid_argument` · 물려받은 응답 + 묶임 없는 고민 → `prefer` + `inherited_from` 그대로 · (0.2) 물려받은 응답 + 묶임 있는 고민: 자기 부위로 → `filter` · 다른 부위로 → `prefer`(기준은 물은 고민의 `sites[]`).
6. 쪽 넘김 — `prefer` 응답을 `limit=1` 로 끝까지 넘긴 묶음 합 = `total` · 0.7.0 꼴 cursor(`request` 에 `site_mode` 없음)는 `cursor_invalid`.
7. **실물**(데이터 env · 고민 260 × 부위 이름 89 = **23,140** 짝 · 0.2 — SPEC 0.7.2 재셈): `filter` 짝 **191**(자기 묶임 95 · 하위 묶임만 96 · 고민 100) · `prefer` 짝 **22,949** · 전 짝에서 `site_applied` = `filter` ⇔ 물은 부위의 코드 ∈ `sites[]` · `prefer` 짝 전부에서 완료 조건 1 ~ 3 이 선다 · `sites[]` = `[]` 인 **160** 고민의 **14,240** 짝은 전부 `prefer`(`filter` 로 0 행인 짝 **14,008** → 전부 행이 나온다 · 표지 행 합 **646** · 232 짝) · **`sites[]` 가 있는 100 고민의 밖 부위 8,709 짝도 전부 `prefer`**(`filter` 로 0 행인 짝 **8,444** → 전부 행 · 표지 행 합 **971** · 265 짝) · `prefer` 전체 표지 행 합 **1,617**(497 짝) · `auto` 에서 0 행인 짝 **5**(전부 `filter` — `CON-200` · `CON-206` · `CON-277` × `SITE-084` 이름 · `CON-226` · `CON-230` × `SITE-019` 이름 · 고치지 않는다 — SPEC O-31 ④) · `CON-048` × `SITE-051` 이름 = **105 행 · 묶음 55 · 표지 0** · **`CON-005` × `SITE-051` 이름 = `prefer` · 54 행 · 묶음 15 · 표지 0**(`site_mode="filter"` 로는 0 행 · `unfiltered_rows` 54) · `CON-005` × `SITE-014` 이름 = `filter` · 54 행 · 묶음 15 · `CON-001` × `SITE-014` 이름 = `filter` · **73 행 · 묶음 16**(`by_site_match` = `column` 24 · `concern_site` 54 — `test_gold_holes.py:596-609` 가 이미 본다 · 손대지 않고 통과) · `CON-001` × `SITE-051` 이름 = `filter` · 11 행 · 묶음 3 · 물려받는 고민 13 가운데 묶임 없는 **9** 는 전 짝 `prefer` · 묶임 있는 4(`CON-012` · `CON-136` · `CON-206` · `CON-230`)는 자기 부위로 물을 때만 `filter`.
8. 실물 시험이 도는 시간을 적는다(260 × 89 = 23,140 조회 × 두 번) — 길어도 표본으로 줄이지 않는다. 줄여야 하면 고치지 말고 수와 함께 보고한다(§10 A-6).
9. `tools/list` 의 `concern_candidates` 설명에 §2 문장 ③ 의 조각(「부위로 거르지 않은 응답」)이 있다 · 입력 스키마에 `site_mode` 가 있다.

**돌릴 파일**

| 파일 | 왜 |
|---|---|
| `tests/test_gold_v07_site.py` | 새 시험(위 1 ~ 9) |
| `tests/test_gold_tools_synthetic.py` | 고친다(§2 ⓑ) |
| `tests/test_gold_holes.py` | **고친다(§2 ⓖ — `:301` · `:304` · `:316` 에 `site_mode="filter"`)** · §2 ⓒ 확인(`test_T22_with_inherit` · `test_e2e_shapes_052_real` · `test_T22_real` 이 그대로 서나) — ⓖ 밖에서 안 서는 것은 고치지 말고 보고한다 |
| `tests/test_gold_contract.py` | 고친다(`ROW_COMPUTED` 에 `site_prefer` · 묶음 열쇠 `n_site_prefer` · `counts` 칸 · `site_applied`) |
| `tests/test_gold_v07_descend.py` | WP-2 의 것 — `concern.py` 를 다시 고쳤으므로 한 번 더 |

## 6. WP-4 — 기존 필드 불변 · 두 판 · REST = MCP · 문서

**SPEC**: §9 T27(+ T3 부록 A · T6 · T7 의 0.7 몫) · §5-11 「두 판(CSV · DB)」 문단 · 부록 A 「0.7 의 계산 필드」 · 「0.7.1 의 계산 필드」 문단 · 변경 기록 0.7.0 · 0.7.1 의 cursor 줄 · SPEC-003 §5 P2 · §7 DT10 · 검수 N-3.

| 만들 · 고칠 것 | 어디 | 내용 |
|---|---|---|
| 0.6 꼴 동치(합성) | 새 `tests/test_gold_v07_compat.py` | 기본 판 · `holes` 판 · `v07` 판에서: `concern_candidates(site 없음)` 는 새 열쇠(`descended` · `sites` · `counts.descended` · `counts.sites` · `site_applied` · `counts.site_prefer` · `request.to_procedure` · `request.site_mode`)를 빼면 **`to_procedure="none"` 응답에서 같은 열쇠를 뺀 것**과 같다 · `site` 를 건 조회는 `site_mode="filter"` 로 같다 · `resolve` 는 `abbr="off"` 일 때 `matched.how` · `request.abbr` 을 빼면 열쇠 집합이 0.6 의 것(`span` · `start` · `covered_by`)이다 |
| **두 판 — DT10 표본**(N-3) | `tests/test_gold_mcp.py` `SAME` · `tests/test_medallion_repo.py` | `SAME` 에 더한다: `resolve` 줄임 꼴 하나 · `resolve` `abbr=off` 하나 · `concern_candidates` `to_procedure=none` 하나 · `site_mode=filter` 하나. **`prefer` 짝 하나 · `filter` 짝 하나가 DT10 을 실제로 돈다**: ① `prefer` 짝 = 이미 있는 `CON-901` × 「부위나」(`test_gold_mcp.py:63` — 기본 판에서 `CON-901` 은 묶인 부위가 없다) ② `filter` 짝 = 부위가 묶이고 **행이 있는** 고민 + 그 부위 — 기본 판에는 없다(`CON-904` 는 행 0) → `v07` 판(또는 `holes` 판의 `CON-901` × 「부위나」 · `CON-902` × 「부위나」)으로 DT10 을 한 번 더 돈다. ③ **(0.2) `prefer` 짝 하나 더 — 묶임 있는 고민 + 그 고민의 부위가 아닌 부위**(`holes` 판 `CON-901` × 「부위가」 — 0.7.2 가 새로 연 길). **세 짝의 응답에서 `site_applied` 가 `prefer` · `filter` · `prefer` 임을 단언한 뒤** 두 판 JSON 을 견준다(표본이 실제로 그 길을 탔다는 증거). 쪽 넘김 표본(`PAGED` `:93-96`)에 `concern_candidates` `limit=1` 하나 |
| REST = MCP(T7) | `test_gold_mcp.py` | 위 `SAME` 이 덮는다 · 새 입력의 enum 밖 값 셋(`abbr` · `to_procedure` · `site_mode`)을 `ERRORS`(`:82-96`)에 — 두 입구의 오류 글이 같다 |
| 헤더 계약(T3) | `tests/test_gold_contract.py` | 부록 A 의 0.7 · 0.7.1 여섯 줄(`headers.py` 상수)의 칸 ⊂ 실제 헤더(합성 · 실물) · `descended[]` · `sites[]` 의 열쇠 집합 = 상수 · `v07` 판 응답으로 `check_response` |
| 도구 설명 셋 | `test_gold_v07_compat.py` | `mcp_server.DESCRIPTIONS` 와 `tools/list` 양쪽에 §2 문장 ① ② ③ 의 조각 · 기존 조각이 그대로 |
| 해시 불변 | 같은 파일(실물) | `health.build.gold_hash` · `aux_hash` 가 SPEC-003 §2-5 의 값(= `GOLD_EXPECTED_HASH` 로 주는 값)과 같다 — 새 입력 0. `health` 의 열쇠 집합이 그대로(`test_medallion_repo.py:125-133` 이 이미 본다) |
| 문서 | `swagger_docs/gold.py` · `README.md` gold 절 | `resolve` · `concern-candidates` 불릿에 새 입력 셋 · 새 필드 한 줄씩(README `:87` 의 「새 입력」 줄 꼴) |

**완료 조건**(T27)
1. 위 표의 시험이 통과한다.
2. **gold 시험 묶음이 그대로 통과한다** — `tests/test_gold_*.py`(기존 8 + 새 4) · `tests/test_medallion_repo.py`. T27 의 「0.6 의 응답 기대(T1 ~ T23)가 그대로 통과」 가 이것이다. **이것은 gold 모듈의 시험만이다 — 전체 pytest 가 아니다**(§10 B-1 — 코디가 더 좁히라고 하면 그대로 따른다).
3. 고친 기존 시험 목록(이름 · 줄 · 까닭)이 §2 「기존 시험」 줄의 ⓐ ~ ⓖ 안이다 · 밖이면 까닭과 함께 보고한다.
4. `git diff HEAD --stat -- backend/app/modules/gold/coverage.py backend/app/modules/gold/closure.py backend/app/modules/gold/facets.py backend/app/modules/gold/pairs.py backend/app/modules/gold/inputs.py backend/app/modules/gold/db_inputs.py backend/app/gold_main.py` 가 비어 있다.
5. `uv run ruff check <고친 · 새 파일>` 통과.

**돌릴 파일**

| 파일 | 왜 |
|---|---|
| `tests/test_gold_v07_compat.py` · `tests/test_gold_v07_resolve.py` · `tests/test_gold_v07_descend.py` · `tests/test_gold_v07_site.py` | 새 시험 넷 |
| `tests/test_gold_contract.py` · `tests/test_gold_mcp.py` · `tests/test_medallion_repo.py` · `tests/test_gold_tools_synthetic.py` · `tests/test_gold_holes.py` | 고친 기존 시험 |
| `tests/test_gold_real.py` · `tests/test_gold_coverage.py` · `tests/test_gold_load.py` · `tests/test_gold_rest.py` | 안 고친다 — 완료 조건 2(T27) |
| `tests/test_medallion_load.py` | **`medallion_fixture.py` 를 고쳤을 때만**(`v07` 인자) |

`tests/test_medallion_model.py` 와 gold 밖의 시험은 돌리지 않는다.

## 7. 순서 · 의존

- WP-1 → WP-2 → WP-3 → WP-4 → §8-1 실물 확인. WP-1 은 `resolve` 쪽이라 WP-2 · WP-3 과 코드가 겹치지 않지만 `headers.py` · `mcp_server.py` · `test_gold_contract.py` 를 함께 고치므로 한 워커가 순서대로 한다.
- 앱(WORK-014 — 다른 writer 의 문서)은 이 계약의 필드 이름(SPEC §4-1 · §4-5)만 본다. 허브 구현이 끝나기 전에 앱이 새 필드를 보려면 18107 에 뜬 허브가 있어야 하는데, **18107 은 이 WORK 의 실물 확인 때만 잠깐 뜬다** — 앱 쪽 일정은 코디가 맞춘다(§10 B-3).

## 8. 실물 확인 — 순서 · 누가

### 8-1. 워커 몫(허브 18107 — 띄웠다 내린다)

WP-4 뒤에 한 번. 응답은 세션 임시 폴더에 둔다(레포 밖). `<…>` 는 자리 표시다.

```bash
# backend/ 에서
lsof -nP -iTCP:18107 -sTCP:LISTEN          # 비어 있어야 한다 — 아니면 멈추고 보고

# ① CSV 판을 18107 에 — 데이터 env 넷(+ 기대 해시)
GOLD_CSV_DIR=<gold 폴더> GOLD_SOURCE_REF_PATH=<silver 폴더>/source_ref.csv \
GOLD_HIERARCHY_DIR=<silver 폴더> GOLD_LEDGER_CHECK_PATH=<ledger-check-list.csv> GOLD_EXPECTED_HASH=<SPEC-003 §2-5 의 gold_hash> \
  uv run uvicorn app.gold_main:app --host 127.0.0.1 --port 18107
# ② 요청 묶음(아래 표) → 응답 저장 → 18107 을 내린다(자기가 띄운 프로세스만)

# ③ DB 판을 같은 포트에 — 접속 값은 코디가 정한 방법으로 프로세스 env 에만(찍지 않는다)
GOLD_REPOSITORY=db GOLD_EXPECTED_HASH=<같은 값> \
  uv run uvicorn app.gold_main:app --host 127.0.0.1 --port 18107
# ④ 같은 요청 묶음 → ② 의 응답과 견준다 → 18107 을 내린다 → lsof 로 내려간 것을 본다
```

| # | 확인 | 기대 |
|---|---|---|
| E1 | 18107 `health`(CSV 판) | `build.gold_hash` · `build.aux_hash` 가 18105(0.6 코드 · DB 판 — **읽기만**)의 `health` 와 같다 · 열쇠 집합이 같다 |
| E2 | **기존 필드 불변** — 37 문항 답 키 명세의 호출(앱 워크트리 `data/eval-set/calls/` 37 파일 — **읽기만** · _RESUME §2 11-17 「WORK-010 B 코디 답」 B-2)을 18105 와 18107 에 그대로 · 쪽을 끝까지 | 18107 응답에서 새 열쇠(§6 첫 줄의 목록 + `matched.how` · `matched.full` · `request.abbr`)를 빼면 18105 응답과 같다(`build.loaded_at` 제외). 달라지는 값이 있으면 **NM4 의 `covered_by` 한 자리뿐**이어야 하고 37 문항에서는 0 건이다(SPEC 변경 기록 0.7.0) — 0 이 아니면 문항 · 호출 · 값을 보고한다 |
| E3 | 새 필드 실물 — DP | `concern_candidates(CON-168)` → `total` 0 · `descended` 1 묶음(`M18`) · 시술 6(`PRC-123` ~ `PRC-128`) · `from[].path` = 패키지 → 계열 · `sites` = `SITE-072` 1 항목 |
| E4 | 새 필드 실물 — SP | `concern_candidates(CON-048, site=<SITE-051 의 g_entry 이름>)` → `site_applied` = `prefer` · 105 행 · 묶음 55 · `counts.site_prefer.rows` 0 / `concern_candidates(CON-001, site=<SITE-014 의 이름>)` → `filter` · 73 행 · 묶음 16 / 앞 조회에 `site_mode=filter` → 0 행 · `unfiltered_rows` 105 / **(0.2) `concern_candidates(CON-005, site=<SITE-051 의 이름>)` → `prefer` · 54 행 · 묶음 15 · `counts.site_prefer.rows` 0 · `sites` = `SITE-014` 1 항목 — 같은 조회에 `site_mode=filter` → 0 행 · `unfiltered_rows` 54 / `concern_candidates(CON-005, site=<SITE-014 의 이름>)` → `filter` · 54 행 · 묶음 15** |
| E5 | 새 필드 실물 — NM | `$W/_RESUME.md` §1 「수정 2 목록」 2 의 둘째 꼴(계열 `M18` 이름의 앞 낱말을 줄인 말 — 띄어 쓴 꼴 · 붙여 쓴 꼴) → `M18` 이 `how` = `줄임` · `CON-137` 에 `covered_by` / 같은 문장 `abbr=off` → `M18` 없음 |
| E6 | MCP | `tools/list` 9 도구 · 설명에 문장 셋 · `concern_candidates` 를 MCP 로 한 번 불러 REST JSON 과 같다 |
| E7 | **CSV 판 = DB 판** | ② 와 ④ 의 응답(E2 ~ E5 의 요청 전부)이 `build.loaded_at` 을 빼고 같다 · `health` 는 `load_ms` 도 빼고 |

- 18105 에는 GET 조회만 보낸다. 18105 · 18106 · 18210 · 18220 · 18222 를 내리거나 띄우지 않는다. PostgreSQL 에 쓰는 명령(적재 · alembic)을 돌리지 않는다.
- `pkill` · 포트로 찾아 죽이기를 쓰지 않는다 — 자기가 띄운 프로세스의 PID 만 내린다.

### 8-2. 코디 몫

| 순서 | 무엇 | 왜 코디인가 |
|---|---|---|
| WP-4 뒤 | 워커 보고 검증 — **바뀐 WP 의 시험만**(§3 ~ §6 의 「돌릴 파일」) · grep | 사용자 11-17 「시험은 구현한 것만」 |
| 뒤 | 코드 검수 발주 → PASS 뒤 **18105 를 새 코드로 다시 띄운다**(앱 18220 · 18222 와 함께) | 18105 는 앱 · 사용자 e2e 가 보는 포트다 |
| 뒤 | 앱 답 키 37 다시 뽑기 · 대조(새 허브에서 키가 그대로인가 — `site` 를 건 호출 0 이라 SP 로는 안 바뀐다 · 앱 WORK 의 걸음) | 앱 레포는 이 WORK 밖 |
| 뒤 | 커밋 · SPEC 되적기(§10 A) | 코디 몫 |

## 9. 완료 조건 · 검증 명령(모음)

| # | 완료 조건 | 누가 | 무엇으로 |
|---|---|---|---|
| 1 | T24 ~ T28 이 시험 이름 또는 주석으로 찾아진다 · 통과 | 워커 | §3 ~ §6 의 「돌릴 파일」 |
| 2 | **검수 N-2** — `prefer` 응답의 `site_prefer` = `false` 행에 `site_match` 가 없다(꼴 하나) | 워커 | §5 완료 조건 2 |
| 2-1 | **(0.2) SP1 기준(0.7.2)** — `filter` ⇔ 물은 부위의 코드 ∈ `sites[]` · 묶임 있는 고민 + 밖 부위 = `prefer` · 안 부위 짝은 `site_mode="filter"` 응답과 같다(회귀 0) | 워커 | §5 완료 조건 4 · 7 · E4 |
| 3 | **검수 N-3** — DT10 이 `prefer` 짝 · `filter` 짝을 실제로 돈다(`site_applied` 단언 뒤 두 판 대조) | 워커 | §6 표 「두 판」 |
| 4 | CSV 판 = DB 판 — 합성(DT10) · 실물(E7) | 워커 | §6 · §8-1 |
| 5 | MCP 도구 설명 문장 셋 | 워커 | §3 9 · §4 9 · §5 9 · §6 · E6 |
| 6 | 기존 필드 불변 — 합성(§6) · 실물(E2) · `gold_hash` · `aux_hash` 그대로 | 워커 | §6 · §8-1 |
| 7 | **전체 pytest 를 돌리지 않았다 · WP 마다 돌린 파일 목록이 보고에 있다** | 워커 | 보고 |
| 8 | 18107 이 내려가 있다 · 레포에 CSV · 응답 dump · 접속 값 0 | 워커 → 코디 | 아래 |

```bash
# backend/ 에서 — WP-4 의 묶음(전체가 아니다)
uv run ruff check app/modules/gold app/router/gold.py app/swagger_docs/gold.py tests/test_gold_*.py tests/test_medallion_repo.py tests/gold_fixture.py tests/medallion_fixture.py
DATABASE_URL=sqlite+aiosqlite:///:memory: uv run pytest tests/test_gold_*.py tests/test_medallion_repo.py -q -rs

# 허브 워크트리 루트에서
lsof -nP -iTCP:18107 -sTCP:LISTEN                         # 비어 있다
git status --porcelain                                    # §2 allowed_paths 안뿐 · *.csv · *.json dump · *.db 0
git diff --stat origin/release/v1.2.0 -- backend/app/main.py backend/app/core   # 비어 있다
git diff HEAD -U0 | grep -n -i -E "postgresql(\+asyncpg)?://[^<]|passw|secret|token|api[_-]?key"   # 0
git diff HEAD -U0 | grep -n -E "/(Users|home)/[a-z]"      # 홈 경로 0
```

## 10. 열린 것 · 이 문서를 쓰며 본 것(SPEC 은 고치지 않았다)

**A — 구현 때 정한다(제안값 · 정한 값을 보고에 적는다)**

| # | 무엇 | 제안 | 상태 |
|---|---|---|---|
| A-1 | DP 코드의 자리 | 새 `descend.py`(`closure.py` 꼴 — repository 만 읽는다) · `concern.py` 는 부르기만 | 구현 때 정함 |
| A-2 | 줄임 열쇠 메서드 이름 · 수 | `abbr_keys()` · `entries_by_abbr(key)` — Protocol 31. **SPEC-003 §5 P1 「메서드 29」 → 31** 은 되적기 후보(SPEC-001 §5-11 끝 문단이 「WORK 에서 수를 고친다」 로 넘겼다 — 문서는 코디 몫) | 보고 |
| A-3 | `resolve` 목록 꼴에 `abbr` 을 주면 | 무시한다(`request` 에는 싣는다) — `site` 없는 `site_mode` 와 같은 꼴. SPEC 에 적힌 것이 없다 | 구현 때 정함 — SPEC §4-1 되적기 후보 |
| A-4 | `matched` 의 열쇠 순서 · `부분` 후보에 `full` 을 싣나 | (`span`, `start`, `covered_by`, `how`) · `줄임` 만 + `full`. SPEC §4-1 은 「`줄임` 이면 `full` 이 함께 붙는다」 로만 적었고 T27 의 「`how` 를 빼면 같은 JSON」 이 `부분` 에 `full` 이 없어야 선다 | 구현 때 정함 — 되적기 후보 |
| A-5 | N-2 `site_prefer` = `false` 행의 `site_match` | **필드 없음**(§5) | 이 문서가 닫음 — SPEC §4-5 되적기 후보 |
| A-6 | T24 · T25 · T28 실물 시험의 시간(고민 260 전부 · 260 × 89 짝) | 줄이지 않고 잰다. 눈에 띄게 길면(제안 기준: 새 시험 넷 합 3 분 넘게) 수와 함께 보고 — 표본으로 줄일지는 코디가 정한다 | 재기만 |
| A-7 | fixture 선택지 이름 · `v07` 판을 `holes` 위에 얹을지 따로 둘지 | `write_fixture(root, holes=False, v07=False)` — `v07=True` 는 `holes` 의 개체도 함께 싣는다(회귀 짝을 한 판에서 본다) | 구현 때 정함 |
| A-8 | 이름 · 꼴(O-27 · O-29 · O-30) | SPEC 본문 그대로 — `to_procedure` · `abbr` · `site_mode` · `descended[]` · `sites[]` · `site_applied` · `site_prefer` · `n_site_prefer` · `counts.*` · 접두 하한 2 · 열쇠 하한 4 | 구현 때 정함(본문 = 제안) |

**B — 코디에게 받을 것(발주서에)**

| # | 무엇 | 왜 |
|---|---|---|
| B-1 | WP-4 완료 조건 2 의 「gold 시험 묶음」(`tests/test_gold_*.py` + `test_medallion_repo.py`)을 돌려도 되나 | T27 이 「0.6 의 기대가 그대로 통과」 를 요구한다 — 이 문서는 「gold 모듈의 시험 = 구현한 것」 으로 읽었다. 더 좁히라면 「고친 · 새 파일만」 으로 하고 T27 의 그 줄은 「돌리지 않음」 으로 보고한다 |
| B-2 | DB 판 확인(§8-1 ③)의 접속 값 파일 자리 | _RESUME §2 11-17 「WORK-010 B 코디 답」 B-1 의 방법 그대로면 발주서에 한 줄만 · 이 문서를 쓴 워커는 그 파일을 열지 않았다 |
| B-3 | 앱 구현(WORK-014)이 새 허브를 보려 할 때 | 18107 은 워커가 띄웠다 내린다 — 앱 워커가 쓸 허브를 따로 띄울지 · 18105 를 언제 바꿀지는 코디가 정한다 |

**이 문서를 쓰며 본 것**

- **기본 합성 판의 `CON-901` 은 묶인 부위가 없다**(자기 0 · 하위 `CON-902` · `CON-903` 도 0 — 묶임은 `CON-904` 하나) → 기본값 `auto` 에서 `CON-901` + `site` 는 `prefer` 다. 기존 시험 한 곳(`test_gold_tools_synthetic.py:279-282`)의 기대가 바뀌는 까닭이고, 같은 짝이 DT10 의 `prefer` 표본이 된다(§2 ⓑ · §6).
- `holes` 판의 `CON-905`(물려받는 고민)도 묶인 부위가 없다 → `test_T22_with_inherit` 이 `prefer` 길을 탄다(SPEC §5-11 SP 셈의 `CON-250` 꼴과 같다 — 물려받은 윗고민 행이 묶임으로 맞는다).
- 실물 `test_T22_real`(`test_gold_holes.py:548-592`)의 짝은 전부 「묶인 고민의 윗고민」 · 「묶인 고민 자신」 × **그 묶임의 부위**라 0.7.2 로도 `filter` 그대로다(물은 부위가 `sites[]` 안) — 손대지 않는다. 그 시험이 「그대로 0」 으로 적은 3 짝(`:575`)이 SPEC O-31 ④ 의 5 짝 가운데 셋이다.
- **(0.2) `holes` 판의 `CON-901` · `CON-902` 는 `sites[]` 가 `SITE-902` 하나다** → 「부위가」 · 「부위없음」 으로 건 기존 호출 셋이 0.7.2 에서 `prefer` 로 바뀐다(§2 ⓖ). 0.7.1 기준이었다면 그 셋은 `filter` 그대로였다 — 0.1 이 「이 밖에서 깨지면 보고」 로 둔 자리가 0.7.2 로 생긴 것이다.
- `coverage` 는 `concern_rows` 만 부르고 `site` · 내려가기를 쓰지 않는다 — DP8 의 「`coverage` 셈 그대로」 가 코드로 선다.

**이번 판에 구현 대상이 아닌 절**: SPEC §10 O-28(DP 의 한계) · O-29 의 「1회차 trace 뒤」 · O-31 ② ~ ④(SP 의 한계 · 데이터 보강 · `filter` 로 0 인 5 짝 — ① 은 0.7.2 의 SP1 로 닫혀 WP-3 이 구현한다) · 변경 기록 0.7.1 의 「SPEC-002 되적기 후보」 표 · 「따라 고칠 곳」(SPEC-006 · SPEC-003 · `_RESUME` — 다른 문서 · 다른 사람) · 검수 0.7.1 N-1(괄호 문구) · N-4(앱 SPEC-006 몫).

## 11. SPEC-001 0.7.0 + 0.7.1 + 0.7.2 절 ↔ WP 대응(미대응 0)

| SPEC-001 절 | 무엇 | WP | 시험 · 확인 |
|---|---|---|---|
| §0 요약 0.7.0 · 0.7.1 · 0.7.2 줄 | 무엇을 더했나 | 전부 | — |
| §3-1 「줄임 열쇠」 | 메모리 색인 · 두 판 같은 코드 | WP-1 | §3 1 · 8 · `test_dt9_same_memory_index` |
| §3-1 「시술로 내려가기」 · 「고민 부위」 | 새 색인 없음 | WP-2 | §4 표(새 메서드 0) |
| §4-0 쪽 밖 목록 표의 `concern_candidates` 줄 | `descended[]` · `sites[]` 는 첫 쪽에만 | WP-2 | §4 7 |
| §4-1 `matched.how` · `matched.full` · `covered_by` · 순서 · 「줄임 일치」 불릿 · 입력 `abbr` · 도구 설명 | — | WP-1 | T26 · §3 1 ~ 9 |
| §4-5 입력 `to_procedure` · 출력 `descended[]` · `counts.descended` · 「꼴」 표 · `from[].lands` | — | WP-2 | T24 · §4 1 ~ 5 · 8 |
| §4-5 출력 `sites[]` · `counts.sites` | — | WP-2 | T25 · §4 6 · 8 |
| §4-5 입력 `site`(0.7.1) · `site_mode` · 출력 `site_applied` · `site_prefer` · `n_site_prefer` · `counts.site_prefer` · 「0 이면 0」 불릿 · 「`prefer` 일 때의 셈」 불릿 | — | WP-3 | T28 · §5 1 ~ 7 |
| §4-5 「MCP 도구 설명에 적을 문장」 ① ② | — | WP-2(①) · WP-3(②) | §4 9 · §5 9 · E6 |
| §5-1 R9 | 줄임 일치를 R2 위에 | WP-1 | T26 |
| §5-9 HG3-7 | 거르는 것은 물은 부위가 `sites[]` 안에 있을 때뿐(0.7.2) | WP-3 | T28 · T22 · §5 4 · 7 |
| §5-11 DP1 ~ DP9 | 내려가기 규칙 | WP-2 | T24 |
| §5-11 CS1 ~ CS6 | 고민 부위 규칙 | WP-2 | T25 |
| §5-11 NM1 ~ NM6 | 줄임 규칙 | WP-1 | T26 |
| §5-11 SP1 ~ SP8 | 고민 + 부위: 거름 / 우선 표시(SP1 · SP6 = 0.7.2 기준) | WP-3 | T28 · §5 1 ~ 7 |
| §5-11 셈(DP · CS · NM · SP) | 실물 수 | WP-1 ~ WP-3 | §3 8 · §4 8 · §5 7 |
| §5-11 「두 판(CSV · DB)」 | 새 입력 0 · 같은 `GoldMemory` · DT10 을 0.7 필드까지 · 메서드 수 | WP-1(색인) · WP-4 | §6 「두 판」 · E7 · §10 A-2 |
| §9 T22(0.7.1 · 0.7.2 문장) | 묶임 없는 (고민, 부위) 의 갈림 — 0 그대로는 `site_mode` = `filter` 일 때 | WP-3 | §5 4 · 7 · §2 ⓑ ⓒ ⓖ |
| §9 T24 | 시술로 내려가기 | WP-2 | §4 |
| §9 T25 | 고민 부위 | WP-2 | §4 |
| §9 T26 | 줄임 일치 | WP-1 | §3 |
| §9 T27 | 기존 필드 불변 · 두 판 · REST = MCP · 결정론 · 해시 | WP-4 | §6 · E1 · E2 · E7 |
| §9 T28 | 고민 + 부위: 거름 / 우선 표시(0.7.2 기준 · 191 / 22,949 짝) | WP-3 | §5 |
| §9 T3 · T6 · T7 의 0.7 몫 | 헤더 계약 · 결정론 · 두 입구 | WP-2(T6) · WP-4(T3 · T7) | §4 7 · §6 |
| §10 U7-1 ~ U7-3 | 사용자 결정 | 닫힘 — 전부 (a) | 머리말 |
| §10 O-27 · O-30 | 이름 · 꼴 · 표지의 뜻 | WP-2 · WP-3 — 본문 그대로 · O-30 = (a) | §10 A-8 |
| §10 O-29 | NM 의 값(하한 2 · 4) | WP-1 — 본문 값 · 한계는 구현 대상 아님 | §3 |
| §10 O-28 · O-31 ② ~ ④ | 한계 | **구현 대상 아님** | §10 끝 줄 |
| §10 O-31 ① | 부위 있는 고민을 다른 부위로 물으면 0 — **0.7.2 로 닫힘** | WP-3(SP1) | §5 4 · 7 · E4 |
| 부록 A 「0.7」 다섯 줄 · 「0.7.1 SP」 한 줄 · 계산 필드 두 문단 | 읽는 칸 · 계산 필드 이름 | WP-1 ~ WP-3(`headers.py`) · WP-4(T3) | §6 「헤더 계약」 |
| 변경 기록 0.7.0 · 0.7.1 — cursor 줄 | 옛 cursor = `cursor_invalid` | WP-2 · WP-3 | §4 7 · §5 6 |
| 변경 기록 0.7.1 — 「SPEC-002 되적기 후보」 · 「따라 고칠 곳」 | 다른 문서 | **구현 대상 아님** | §10 끝 줄 |
| 변경 기록 0.7.2 — 규칙 한 줄 · 끌어낸 것 ① ~ ④ | SP1 기준 · 입구에 없는 글자 = `prefer` · 「안」 = `site_code` 글자 그대로 · 물려받은 응답 기준 · 5 짝 그대로 | WP-3 | §5 표 「기준」 · 4 · 5 · 7 |
| 변경 기록 0.7.2 — SPEC-002 되적기 #4 · #2 · 「따라 고칠 곳」 | 다른 문서 | **구현 대상 아님** | — |
| 검수 0.7.1 N-2 | `site_match` 꼴 하나 | WP-3 | §5 · §9 2 |
| 검수 0.7.1 N-3 | DT10 표본에 `prefer` 짝 · `filter` 짝 | WP-4 | §6 · §9 3 |
| 검수 0.7.1 N-1 · N-4 | 문구 · 앱 몫 | **구현 대상 아님** | §10 끝 줄 |
| SPEC-003 §5 P2 · §7 DT10 | 두 판 응답 같음 | WP-4 | §6 · E7 |

## 변경 기록

### 0.2.0 (2026-11-17)

- 계약을 SPEC-001 **0.7.2** 로 올렸다(_RESUME §2 11-17 「규칙 변경 = 넣음」) — **WP-3 의 판정 한 줄**: 「`sites[]` 가 `[]` 인가」 → 「물은 부위의 코드가 `sites[]` 의 `site_code` 안에 있는가」(§5 표 「기준」). 필드 · 입력 · 이름 · 파일 목록 · WP 순서 · 시험 파일 이름은 0.1 그대로다.
- WP-3: fixture 꼴 넷 더함 · 완료 조건 4 · 5 · 7 고침(실물 수 — `filter` 191 · `prefer` 22,949 · 밖 부위 8,709 짝 · 0 행 5 짝 · `CON-005` × `SITE-051` 이름 54 행) · 「돌릴 파일」 의 `test_gold_holes.py` 를 「고친다」 로.
- **기존 시험 기대가 바뀌는 자리를 다시 grep 했다**(§2 ⓖ): `test_gold_holes.py` 의 호출 자리 셋(`:301` · `:304` · `:316`)에 `site_mode="filter"`. 그 밖의 `site` 호출은 안 바뀐다(목록을 ⓖ 에 적었다).
- WP-4 DT10 표본에 「묶임 있는 고민 + 밖 부위」 `prefer` 짝 하나 · §8-1 E4 에 `CON-005` 꼴 · §9 2-1 · §11 대응 줄.
- **「시험은 그 WP 의 파일만 · 전체 pytest 금지」 는 그대로다**(§0 · §2). §10 B-1 ~ B-3 은 손대지 않았다(코디가 답한다).
- 돌려 보지 않은 것: pytest · 서버 · DB(읽기와 `grep` · SPEC 재셈 스크립트만).

### 0.1.0 (2026-11-17)

- 새로 씀 — SPEC-001 0.7.0 + 0.7.1 을 WP 넷(WP-1 NM · WP-2 DP · CS · WP-3 SP · WP-4 불변 · 두 판 · 문서)과 실물 확인(18107 에 CSV 판 → DB 판)으로.
- 사용자 11-17 「시험은 구현한 것만 · 전체 안 돌림」 을 WP 마다 「돌릴 파일」 표로 넣었다 — 전체 pytest 는 어느 WP 에도 없다.
- `review-spec-001-v071.md` 의 N-2(꼴 = `false` 행에 `site_match` 없음) · N-3(DT10 에 `prefer` 짝 · `filter` 짝)을 §5 · §6 · §9 에 받았다.
- 이 문서가 더한 것(SPEC 되적기 후보 — §10 A): Protocol 메서드 29 → 31 · 목록 꼴의 `abbr` · `부분` 후보에 `full` 없음 · N-2 의 꼴.
- 돌려 보지 않은 것: pytest · 서버 · DB(읽기와 `lsof` · `grep` 만). 접속 값 파일 · `.env` 는 열지 않았다.
