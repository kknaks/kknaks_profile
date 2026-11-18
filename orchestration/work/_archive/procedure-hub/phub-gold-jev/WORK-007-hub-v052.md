---
type: work
id: WORK-007
title: "허브 0.5.2 구현 계획 — 구멍 셋(HG1 윗고민 물려받음 · HG2 하위 = 자손 전부 · HG3 고민 + 부위) · 보조 입력 ③ · 되적기 · 시험 T20 ~ T23"
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
    - "orchestration/work/phub-gold-jev/SPEC-001-hub-gold-mcp.md (0.5.2 · 검수 FAIL 0 · WARN 3 — review-spec-v052.md) ← 계약"
  decisions:
    - "orchestration/work/phub-gold-jev/_RESUME.md §2 (2026-11-17 「SPEC 0.5.2 사용자 결정(전부 추천)」 — U-3 행 0 고민만 · 가까운 윗고민 하나 / U-4 concern_site = 보조 입력 ③ · 「답 키 검토」)"
  related:
    - "orchestration/work/phub-gold-jev/WORK-008-app-v052.md (앱 쪽 — 답 키 다시 뽑기는 이 문서 뒤)"
    - "orchestration/work/phub-gold-jev/WORK-005-hub-v05.md (0.5.1 구현 계획 — 공통 규칙 §2 를 그대로 잇는다)"
    - "orchestration/work/phub-gold-jev/review-spec-v052.md (§7 WARN 3 · NOTE 6 — 이 문서 §9)"
    - "orchestration/work/phub-gold-jev/app-key-fix1-report.md (키 전용 기준 대상 · 54 고민 · 18 계열)"
---

# WORK-007 — 허브 0.5.2 구현 계획(구멍 셋 + 되적기)

> 경로 접두어: `P` = 프로필 워크트리 · `W` = `$P/orchestration/work/phub-gold-jev` · `SM` = `$P/orchestration/work/_archive/procedure-hub/phub-ledger-redesign/silver-model`(gitignore · 로컬 데이터) · `HUB-WT` = `~/orca/workspaces/PROCEDURE-HUB/phub-gold-jev`(브랜치 `kknaksss/phub-gold-jev` · **0.5.1 구현이 미커밋으로 올라가 있다 — 그 위에 이어서 고친다 · 새로 쓰지 않는다**).
> **계약은 SPEC-001 0.5.2 이다.** 이 문서는 「어느 파일을 · 어떤 순서로 · 무엇으로 확인하나」 만 정한다. SPEC 에 없는 동작을 만들지 않는다 — 어긋나는 것을 찾으면 코드를 맞춰 고치지 말고 보고한다(§10).
> 공개 레포 규칙 · 하지 말 것 · allowed_paths · 데이터 env · 검증 명령의 틀은 **WORK-001 §2 · WORK-005 §2 그대로**다(아래 §2 에 바뀐 것만).
> **사용자 결정은 닫혔다**(_RESUME §2 11-17 — 전부 추천): **U-3 = (a) · (가)** 행이 0 인 고민(13)만 · 가장 가까운(행이 있는) 윗고민 하나 / **U-4 = (a)** `concern_site` 는 보조 입력 ③(허브가 silver 를 읽는다 · gold 불변). 이 문서의 「U-3 을 달리 정하면」 꼴 갈래는 전부 (a) 로 읽는다(§9 N-6).

## 0. 요약

- 바뀌는 것은 넷이다: ① **보조 입력 ③** `concern_site.csv`(같은 `GOLD_HIERARCHY_DIR` · `aux_hash` 6 파일) ② **HG2** 「하위 *」 = `g_scope` 하위 role 을 끝까지 따라간 자손 전부(`scope` · `facets` · `pair` · `coverage` 가 **같은 닫힘 함수 하나**) ③ **HG1** 행 0 인 고민 → 가장 가까운 윗고민의 행(`inherited_from` · `hier.match` = `상위` · `upper` 입력) ④ **HG3** `site` 맞춤 = 글자 일치 ∪ 그 부위에 묶인 고민 · 그 하위 고민의 행(`site_match[]`).
- gold 15표 · gold 해시는 그대로다. 바뀌는 것: `aux_hash`(파일 하나 늘어 값이 달라진다 → 옛 cursor 는 `cursor_invalid`) · 다섯 도구의 응답(전부 **넓어지는 쪽**) · 도구 설명.
- WP 다섯: **WP-1** 보조 입력 ③ 적재 → **WP-2** 하위 닫힘(HG2) → **WP-3** 윗고민 물려받음(HG1) → **WP-4** 고민 + 부위(HG3) → **WP-5** 되적기 확인 · 설명 · 시험 마감 · 다시 센 수 보고.
- **되적기의 허브 몫은 대부분 이미 코드에 있다**(§7 표 — 「이미 있음 · 파일:줄」). 새로 짓는 것은 HG1 ~ HG3 과 그 시험(T20 ~ T22)이다.
- **코디가 18105 에 띄운 허브는 건드리지 않는다.** 서버 확인은 **18106** 만 쓰고(11-17 비어 있음 확인 — `lsof`), 앱 워커가 답 키 다시 뽑기에 이어 쓰므로 **WP-5 뒤 띄워 둔 채 코디에게 알린다**(§8).

## 1. 지금 코드(11-17 확인 — `HUB-WT/backend`)

| 파일 | 지금(0.5.1) | 이번에 |
|---|---|---|
| `app/modules/gold/inputs.py`(181줄) | 보조 ① 계층 3표를 `GOLD_HIERARCHY_DIR` 에서(`:128-141`) · 보조 ② 원장 확인 목록(`:143-160`) · `aux_hash` = `source_ref` + 보조 4 파일(`:163`) | WP-1 — 같은 폴더의 `concern_site.csv` 를 더 읽는다 |
| `app/modules/gold/headers.py`(102줄) | `HIERARCHY_TABLES` · `HIERARCHY_COLUMNS`(`:57-58`) · 계산 필드 목록(`:95-97`) | WP-1 · WP-5 — `concern_site` 칸 상수 · 부록 A 새 다섯 줄 · 0.5.2 계산 필드 |
| `app/modules/gold/memory.py`(118줄) · `repository.py`(206줄) | 계층 색인(`memory.py:81`) · `parent_of` · `ancestors` · `descendants`(`repository.py:177-199`) · `scope_by_subject` | WP-1 — 보조 ③ 색인 · 메서드 둘 / WP-2 — 닫힘을 적재 때 셀지 요청 때 따라갈지(O-23 — §10 A-1) |
| `app/modules/gold/core.py`(138줄) | `layer_of`(`:124-131`) = `role` · `path` · `holder` · `scope_gid` | WP-2 — `depth` · `via[]` |
| `app/modules/gold/service.py`(166줄) | `scope`(`:61-75`) = 대상의 `g_scope` 행 한 단 · 순서 `gid` | WP-2 — 닫힘 · `depth` · `via[]` · `descend` · 순서 `depth` → `gid` |
| `app/modules/gold/facets.py`(284줄) | `_target`(`:233` 부터) = `scope_by_subject` 에서 `role in roles` 인 holder 한 단 · 머리글이 「하위는 한 단」 | WP-2 — 「하위 *」 role 이 왔을 때 닫힘 · 머리글 고침 |
| `app/modules/gold/pairs.py`(113줄) | `_holders`(`:24-29`) 한 단 · `PAIR_ROLES`(`:17`) · `PACKAGE_ROLES`(`:18`) | WP-2 — 두 끝 펼침 · 패키지 맞춤이 같은 닫힘 |
| `app/modules/gold/coverage.py`(132줄) | `lineup` = 대상의 「하위 *」 행 한 단(`:100-103`) · `_layered`(`:83-95`) · 고민 `indication` = `asked_rows` 수를 `self` 로 · 나머지 `null`(`:121-132`) · 제품 offer role(`:112`) | WP-2 — `lower` · `lower_holders` · `lineup` 이 닫힘으로 / WP-3 — 고민 `indication.inherited` |
| `app/modules/gold/concern.py`(69줄) | `site` = 두 칸 글자 일치(`:33`) · `asked_rows`(`:67-69`) · 윗고민 없음 | WP-3 · WP-4 — `upper` · `inherited_from` · `hier` · `site_match[]` · `counts` 둘 |
| `app/modules/gold/mcp_server.py`(165줄) · `app/router/gold.py`(139줄) · `app/swagger_docs/gold.py`(36줄) | 도구 9 설명 — `coverage` 설명에 「하위는 g_scope 한 단」(`mcp_server.py:83`) · `concern_candidates` 설명에 「site 정확 일치」(`:67`) | WP-2 ~ WP-5 — 새 입력 둘(`descend` · `upper`) · 설명 고침 |
| `app/modules/gold/kinds.py`(48줄) | `indication` 의 한국어 이름 = 옛 말(`:12`) | WP-5 — 「어디에 쓰나」(SPEC §5-8 「이름」 칸) |
| `tests/gold_fixture.py`(273줄) | silver 폴더에 계층 3표만 쓴다(`:255`) · 합성 계열 하나에 `하위 시술` 둘 · 그 시술에 `하위 케이스` 하나(`:89-103` — **이미 두 단이다**) | WP-1 — 가짜 `concern_site.csv` / WP-2 ~ WP-4 — 닫힘 · 순환 · 형제 · 윗고민 · 묶임 가짜 행 |
| `tests/test_gold_*.py`(7 파일) | `len(rec.files) == 21`(`test_gold_load.py:85 · 146`) · `test_T16_real_counts_reproduce_spec`(`test_gold_coverage.py:281`) · `test_T16_real_offer_spec_numbers_are_item_based`(`:324`) | WP-1 — 22 로 **고친다**(계약이 바뀐 자리) / WP-5 — 새 `test_gold_holes.py`(이름 제안) |

기준선: 11-16 코디 검증 = 데이터 env 로 README 「검증」 전체 **598 passed**(`_RESUME` §5 「허브 v05 완료」). **WP-1 을 시작하기 전에 같은 명령을 한 번 돌려 통과 · skip 수를 적어 둔다**(WP-5 가 이 수와 견준다).

## 2. 공통 — WORK-005 §2 에서 바뀐 것만

| 항목 | 이번 판 |
|---|---|
| allowed_paths | WORK-005 §2 와 같다 — `backend/app/modules/gold/**`(새 파일 `closure.py` 포함 — 이름 제안) · `backend/app/router/gold.py` · `backend/app/swagger_docs/gold.py` · `backend/tests/gold_fixture.py` · `gold_support.py` · `test_gold_*.py`(새 `test_gold_holes.py` 포함) · `backend/envs/.env.example`(설명 한 줄 — env 이름은 늘지 않는다) · `backend/README.md`(gold 절의 보조 입력 파일 목록 한 줄). `pyproject.toml` · `uv.lock` 은 안 고친다 |
| 데이터 env | **이름 그대로 넷**. `GOLD_HIERARCHY_DIR` 폴더에서 `concern_site.csv` 를 함께 읽는다(SPEC §2-2 — env 를 늘리지 않는다). 로컬 = `$SM/silver/`(11-17 확인: 헤더 `id,concern_code,site_code` · 95 행) |
| 포트 | 시험은 포트 없이(ASGI transport). 서버 확인은 **18106** 만. 18105(허브) · 18220(화면)은 코디 것 — 죽이거나 다시 띄우지 않는다 |
| 검증 명령 | WORK-001 §2-4 그대로(`DATABASE_URL=sqlite+aiosqlite:///:memory:` · 데이터 env 없으면 실물 시험 skip · skip 수와 통과 수를 둘 다 보고). **단계마다 그 WP 의 시험만 · 전체는 WP-5 에 한 번** |
| 커밋 | 안 한다 — 워크트리에 변경만 남긴다(코디 몫) |
| 공개 레포 | 합성 fixture 는 가짜 코드 · 가짜 이름만. 시험 이름 · 주석 · 단언에 시술 · 고민 · 부위 이름 · 질문 문장을 넣지 않는다. 실물 단언의 **코드**(`CON-…` · `SITE-…` · `CSI-…` · `LCK-…` · `M…`)와 수는 SPEC 에 적힌 것까지 쓴다 |
| 「시험이 깨진다」 의 뜻 | 계약이 바뀐 자리의 기존 단언은 **지우지 않고 새 계약으로 고친다** — 고친 시험 이름과 까닭을 보고에 목록으로 낸다(§7 완료 조건 6). 그 밖의 기존 시험은 한 줄도 안 바뀌고 통과해야 한다 |

## 3. WP-1 — 보조 입력 ③ `concern_site` 적재

**목표**: silver `concern_site.csv` 의 세 칸을 메모리에 두고 `aux_hash` 에 넣는다. gold 는 건드리지 않는다.
**SPEC**: §2-1(표의 보조 입력 ③ 행 · X7) · §2-2(`GOLD_HIERARCHY_DIR`) · §2-3 4(보조 5 파일 + `source_ref` = 6 · `aux_hash`) · §3-1(보조 ③ 색인) · §4-8(`files[]` 의 `aux` 줄) · 부록 A 「(보조 ③ · 0.5.2 HG3)」 줄 · §9 T1 · T2 · T22 끝 문장 · U-4 (a).

| 고칠 것 | 어디 | 내용 |
|---|---|---|
| 칸 상수 | `headers.py` | `CONCERN_SITE_COLUMNS = ("id", "concern_code", "site_code")`(이름 제안) — 부록 A 의 그 줄. T3 이 실제 silver 헤더와 대조한다 |
| 읽기 | `inputs.py` `read_inputs`(`:128-141` 뒤) | `hier_dir / "concern_site.csv"` — 파일 없음 = `GoldLoadError`(시작 실패) · 쓸 칸 없음 = `GoldLoadError`(기존 「보조 입력에 쓸 칸 없음」 문구 꼴 그대로) · 세 칸만 남긴다 · `FileRecord(…, "aux")` 로 `aux_files` 에 더한다 → `aux_hash` 가 6 파일로 선다(식은 그대로 — 이름순) |
| 색인 | `memory.py` | `site_code` → `(concern_code, id)[]`(`id` 오름차순) · `concern_code` → `site_code[]` |
| repository | `repository.py` Protocol + `CsvMemoryGoldRepository` | 메서드 둘(이름 제안): `concern_site_by_site(site_code) -> Sequence[tuple[str, str]]` · `sites_of_concern(concern_code) -> Sequence[str]`. service 는 이 메서드만 부른다(`test_service_layer_uses_repository_only` 그대로) |
| 적재 기록 | `repository.py` `LoadRecord` · `service.py` `health` | `files[]` 가 **22 줄**(gold 15 + `questions.csv` + `source_ref` + 보조 5). `health.aux` 에 이 표의 수를 실을지는 SPEC §4-8 에 없다 — §10 A-2 |
| 합성 fixture | `tests/gold_fixture.py`(`:249-258`) | silver 폴더에 가짜 `concern_site.csv`(헤더 세 칸 · 가짜 `CSI-9…` id) |
| 실물 env 확인 | `tests/gold_support.py:27` 근처 | 「실물 경로 있음」 판정에 `concern_site.csv` 를 더한다(없으면 실물 시험 skip — 시작 실패로 시험이 깨지지 않게) |
| 문서 | `envs/.env.example:14` · `README.md:87` 근처 | `GOLD_HIERARCHY_DIR` 설명에 「`concern.csv` · `adverse.csv` · `condition.csv` · `concern_site.csv` 가 있는 폴더」 한 줄 |

**완료 조건**
1. T1 실물: `concern_site.csv` 의 행 수 = 파일 행 수(95) · **gold 해시가 0.5.1 과 같다**(SPEC §2-3 3 의 11-16 값) · `kind` 가 `source_ref` · `aux` 인 **6 줄**로 다시 센 값 = `aux_hash` · `aux_hash` 가 0.5.1 값과 **다르다**.
2. T2 합성: `concern_site.csv` 없음 · 세 칸 중 하나 없음 → 시작 실패.
3. `test_hash_formula_and_record_synthetic` · `test_T1_real_load_counts_and_hash` 의 `21` 을 `22` 로 고친다(계약이 바뀐 자리 — 목록에 적는다). `test_memory_holds_no_aux_text` 는 그대로 통과(이 표에 글 칸이 없다 — X7).
4. 실물 셈(SPEC §5-9 HG3 「규모」): 고민 85 · 부위 51 · 그 51 이 전부 `g_entry` 의 site 입구에 있고 `entity_name` 이 코드마다 하나다 — 시험이 직접 세어 단언한다.
5. 0.5.1 build 의 cursor 를 새 build 에 주면 `cursor_invalid`(기존 `test_cursor_invalid` 가 build 묶임을 본다 — 그대로 통과하는지만 확인).

**검증**: `uv run ruff check app tests scripts` → `DATABASE_URL=sqlite+aiosqlite:///:memory: uv run pytest tests/test_gold_load.py tests/test_gold_contract.py -q` → 데이터 env 로 같은 파일.

## 4. WP-2 — 「하위 *」 = 자손 전부(HG2)

**목표**: 대상의 「하위 *」 `g_scope` 행에서 시작해 그 holder 를 `subject` 로 삼은 「하위 *」 행을 **더 없을 때까지** 따라간 holder 목록을 **함수 하나**가 내고, 네 자리가 그 함수만 쓴다.
**SPEC**: §3-1 「하위 닫힘」 줄 · §4-2(끝 불릿) · §4-4 `roles` 칸(0.5.2 문장) · §4-6 규칙 1 · 3 · §4-9 `lower` · `lower_holders` · §5-3 S6 · §5-8 `lineup` · **§5-9 HG2-1 ~ HG2-7** · 부록 A 「(0.5.2 HG2 — 따라가는 칸)」 줄 · 계산 필드(`layer.depth` · `layer.via` · `scope` 행의 `depth` · `via`) · §9 T21 · Q12 줄 · O-21(결정됨) · O-23 · O-26.

| 만들 · 고칠 것 | 어디 | 내용 |
|---|---|---|
| 닫힘 함수 | 새 `app/modules/gold/closure.py`(이름 제안) | `lower_closure(ctx, node, roles, descend)` → `(g_scope 행, depth, via[])` 목록. ① 시작 = 대상을 `subject` 로 둔 행 가운데 `role` 이 **요청이 준 「하위 *」 role** 인 것(`depth` 1 · `via` = `[]`) ② 그 holder 를 `subject` 로 둔 행 가운데 `role` 이 **같은 요청 role 집합** 인 것을 따라간다(`depth` + 1 · `via` 에 거친 holder `{holder_table, holder_code, scope_gid}` 를 가까운 순으로) ③ **한 holder 는 한 번** — 여러 길이면 가장 얕은 `depth` · 같으면 `scope_gid` 가 작은 길(HG2-3 · 너비 우선 + 단마다 `gid` 순으로 돌면 이 규칙이 구조로 선다) ④ 방문한 holder 는 다시 가지 않는다(순환 · 자기 고리에서 끝난다) ⑤ `descend` = `one` 이면 ① 에서 멈춘다. **`자기` · `물려받음` · `제품 경유` · `상위 제품` · `구성 항목` 으로는 따라가지 않고, `자기` · `물려받음` 으로 닿은 holder 에서 다시 내려가지 않는다**(HG2-2 — 닫힘은 대상의 「하위 *」 행에서만 시작한다) |
| `layer` | `core.py` `layer_of`(`:124-131`) | `depth`(1 부터) · `via[]` 를 받는 인자를 더한다. **대상 쪽 행 전부에 붙는다**(HG2-4) — `자기` · `물려받음` · 그 밖의 role 로 한 단에 닿은 행은 `depth` 1 · `via` `[]`. `role` · `path` · `holder` · `scope_gid` 는 **마지막 단의 `g_scope` 행 값 그대로** |
| ① `scope` | `service.py:61-75` | `roles` 가 없거나(전부) 「하위 *」 를 품으면 닫힘의 행을 더 낸다. 두 단 아래 행은 `g_scope` 행 그대로(그 행의 `subject_*` 는 중간 holder 다) · 모든 행에 계산 `depth` · `via[]` · `total` · `counts_by_role` 은 따라간 행을 품는다 · **순서 = `depth` → `gid`** · 입력 `descend`(`all` 기본 \| `one`) |
| ② `facets` 대상 쪽 | `facets.py` `_target`(`:233` 부터) · `facets()` 입력 | holder 목록 = (요청 role 가운데 「하위 *」 가 아닌 것의 한 단 행) + (「하위 *」 가 왔으면 닫힘). **기본값(`자기` · `물려받음`)과 제품 offer 기본(`자기` · `하위 제품`)은 그대로**(S2 · §4-4) — 제품 offer 의 `하위 제품` 은 닫힘으로 선다(제품 → 제품 → 제품). 입력 `descend`. 머리글의 「하위는 한 단」 문장을 고친다 |
| ③ `pair` | `pairs.py` `_holders`(`:24-29`) · `pair()` 입력 | 두 끝 펼침(`PAIR_ROLES`) · 패키지 맞춤(`PACKAGE_ROLES`)이 같은 닫힘을 쓴다 — 계열 끝은 `하위 시술` 아래의 `하위 케이스` 까지. `a_layer` · `b_layer` 에 `depth` · `via[]`. (subject, holder) 마다 한 길만 남기는 지금 규칙(`setdefault` — `:28`)은 HG2-3 의 「한 holder 한 번」 과 같은 식으로 맞춘다. 입력 `descend` |
| ④ `coverage` | `coverage.py:100-103` · `_layered`(`:83-95`) | `lineup` 의 `lower` · `lower_holders` = 닫힘의 행 수 · holder 수. 다른 종류는 `facet_rows` · `pair_rows` 가 닫힘으로 바뀌면 **따라 바뀐다**(세는 길을 따로 짓지 않는다 — T16 불변식). `coverage` 에는 `descend` 입력이 없다(늘 `all` — SPEC §4-9) |
| 입력 `descend` — **N-1** | `service.py` · `router/gold.py` · `swagger_docs/gold.py` · `mcp_server.py` | **세 도구(`scope` · `facets` · `pair`)의 입력 표에 같은 줄**을 넣는다: `descend` = `all`(기본) \| `one` · 표 밖 값 = `invalid_argument` · `request` 에 되돌린다(안 줘도 기본값 `all` 을 그대로 적는다 — 기본값이 있는 enum 의 기존 꼴 `self_pair` 와 같게). `request` 가 바뀌므로 cursor 는 `descend` 에 묶인다 |
| 도구 설명 — HG2-7 · **N-2** | `mcp_server.py` `DESCRIPTIONS` 의 `scope` · `facets` · `pair` · `coverage` | 「하위 role 은 그 아래의 아래까지 전부 · `layer.depth` 로 몇 단인지 · `layer.via[]` 로 거친 층」 + **「아래의 아래는 거치는 role 도 함께 줘야 닿는다 — 계열의 케이스는 `하위 시술` 과 `하위 케이스` 를 함께」**(N-2: 계열에 `하위 케이스` 만 주면 한 단 행이 0 이라 못 닿는다). `coverage` 설명의 「하위는 g_scope 한 단」(`:83`)을 「자손 전부」 로. 0.5.1 의 W-4 문장(「하위 층의 자기 행은 `roles` 에 그 role 을 줘야 나온다」)은 그대로 둔다(T19 가 본다) |
| 적재 때 셀지 | `memory.py` | §10 A-1 — 제안 = 요청 때 따라간다(색인 `scope_by_subject` 로 충분 · 가장 긴 길 4 단) |

**완료 조건**
1. T21 합성: 가짜 계열 → 가짜 시술 → 가짜 케이스에서 — 계열의 `scope` 에 케이스 행이 `depth` 2 · `via` = 그 시술로 나온다 · 계열의 `facets`(「하위 *」 role) 에 케이스 자기 행이 `layer.role` = `하위 케이스` · `layer.depth` 2 · `layer.via[]` = 그 시술 · 계열 끝 `pair` 에 케이스 끝 관계 행 · `coverage.lower` = 같은 조회를 공개 도구로 끝까지 넘겨 센 수.
2. T21 합성(막는 것): **형제 fixture** — 한 제품의 조회에 `물려받음` holder(그 시술)의 다른 하위 제품 행이 **없다** · 한 holder 가 두 길로 닿으면 **한 번**(얕은 `depth` · 같으면 작은 `scope_gid`) · **순환 fixture**(가짜 A → B → A)에서 끝난다 · `descend` = `one` 이면 0.5.1 과 같은 행 · 순서 · `total` · `counts`(새 계산 필드 `depth` · `via` 는 붙는다 — §10 A-3) · 계열에 `하위 케이스` **만** 주면 케이스에 못 닿는다(N-2 — 설명 문장이 MCP `list_tools` 에 있다).
3. T21 실물: 계열 **18 전부**의 `scope` 에서 `depth` 2 의 케이스 수가 SPEC §5-9 의 계열별 수와 같다(합 268) · 한 단으로 닿는 케이스는 0 · **전 대상 858 에서 닫힘의 holder 가 전부 그 대상의 `g_scope` 자손이다**(자손 아닌 holder 0 — 검수 §3 의 셈) · 가장 긴 길 4 단 · 순환 0 · 자기 고리 0.
4. T21 실물(Q12 줄): 계열 대상 조회만으로(`roles` 에 하위 셋 · 키 전용 하위 기준 없이) Q12 의 표본 4 가 전부 나온다 — `gid` 는 시험이 로컬 `questions.csv` 에서 읽는다.
5. T16 실물 불변식(`test_T16_real_invariant_all_target_nodes`)이 **손대지 않고** 통과한다 — 대상 4표 전 노드 × 14 종류에서 `coverage` = 도구로 센 수.
6. **§4-9 의 `lower` 수를 T16 으로 다시 센다**(SPEC §5-9 끝 불릿 · 변경 기록 「고치지 않은 것」): `test_T16_real_counts_reproduce_spec` 의 「`self` 0 · `lower` 1 이상」 수(적응 시술 33 · 제품 3 · 계열 1 / 효과 30 · 3 · 1 / 부작용 31 · 3 / 회복 4 / 금기 2 / 상품 계열 17 · 시술 0 · 제품 7)와 「`inherited` 만」 수가 **HG2 뒤에도 같은지** 그대로 돌린다 — 검수는 「판정이 뒤집히는 (대상, 종류) 0 · 느는 것은 `lower` 의 행 수와 `lower_holders` 뿐」 으로 세었다(검수 §3). **같으면 그대로 · 다르면 코드를 수에 맞추지 말고 보고한다.** 따로 보고할 것: 종류마다 `lower` 행 합의 앞(`descend` = `one`) · 뒤(`all`).
7. 응답이 커지는 자리의 크기 · 시간을 보고한다(O-26 — 자르지 않는다): 계열의 `facets` adverse_detail 한 건 · 계열 끝 `pair` 한 건의 `total` · 끝까지 넘긴 ms.

**검증**: `uv run pytest tests/test_gold_holes.py tests/test_gold_tools_synthetic.py tests/test_gold_coverage.py tests/test_gold_mcp.py tests/test_gold_rest.py -q`(합성) → 데이터 env 로 같은 파일 + `tests/test_gold_real.py`.

## 5. WP-3 — 고민 → 윗고민 물려받음(HG1)

**목표**: 물은 고민의 행이 0 이면 가장 가까운(행이 있는) 윗고민 하나의 행을 같은 꼴로 내고 층을 밝힌다.
**SPEC**: §4-5(입력 `upper` · 출력 `inherited_from` · `counts.self_rows` · 불릿 셋) · §4-9 `inherited`(고민 노드) · §5-5 H5 · H6 · §5-8 `indication` 줄 · **§5-9 HG1-1 ~ HG1-7** · 부록 A 「(보조 · 0.5.2 HG1 · HG3)」 줄 · §9 T20 · Q10 줄 · U-3 (a) · (가) · O-25(전부).

| 고칠 것 | 어디 | 내용 |
|---|---|---|
| 안쪽 함수 | `concern.py`(`asked_rows` 옆 — `:67`) | `concern_rows(ctx, code, upper)` → `(행 전부, inherited_from)`(이름 제안). ① `asked_rows(code)` 가 1 이상이면 그대로 · `inherited_from` = `None` ② 0 이고 `upper` = `auto` 면 `repo.parent_of("concern", …)` 로 **한 단씩** 올라가 행이 1 이상인 **첫** 윗고민에서 멈춘다 → 그 윗고민의 `asked_rows` 전부 · `inherited_from` = `{concern_code, steps}` ③ 뿌리까지 0 이면 빈 목록 · `None` ④ `upper` = `none` 이면 ① 만. **`site` 거르기 앞**에서 판정한다(HG1-1 — `site` 로 0 이 된 것은 해당 없다) |
| 무엇을 내나 | `concern_candidates()`(`:32-63`) | 윗고민을 직접 물었을 때와 **같은 행 전부**(`groups` · `modality_only[]` · `unreached[]` · 쪽 넘김 · `total` = 묶음) — 「직접」 행만 고르지 않는다(HG1-3 · O-25). 행의 gold 칸(`asked_concern_code` · `concern_code` · `concern_match` …)은 **값 그대로** — 요청 코드로 바꿔 쓰지 않는다 |
| 층 표시 | 같은 함수 | 머리 `inherited_from`(늘 싣는다 — 아니면 `null`) · 물려받은 응답의 **모든 행**(세 목록 다)에 `hier{asked_code: 요청 코드, match: "상위"}`(`out_row` 의 계산 필드 인자로 — `facets` 의 `hier` 와 같은 꼴) |
| `counts` | 같은 함수 | `self_rows` = 물은 고민 자신의 행 수(`site` 거르기 앞 · 물려받은 응답이면 0). `unfiltered_rows` 의 뜻은 §10 A-4 |
| `ledger_check[]` | 같은 함수(`:63`) | **요청 코드만** — 윗고민 코드로 넓히지 않는다(HG1-5 · O-14). `not_found` 기준도 그대로(`:29-30`) |
| 입력 `upper` | `service.py:109-110` · `router/gold.py` · `swagger_docs/gold.py` · `mcp_server.py` | `auto`(기본) \| `none` · 표 밖 값 = `invalid_argument` · `request` 에 되돌린다 |
| `coverage` 고민 노드 | `coverage.py` `_value`(`:121-132`) | 고민의 `indication` = `{self, inherited}` — **`concern_rows` 를 그대로 불러** 센다(같은 함수 — HG1-6): `self` = 자기 행 수 · `inherited` = `self` 가 0 일 때 물려받을 행 수(아니면 `0`) · `lower` · `lower_holders` = `null`. 값 쪽의 다른 (노드, 종류)는 그대로 셋 다 `null` |
| 안 바뀌는 것 | `facets.py` | `facets` indication 값 쪽(`node` = concern — 직접만) · `facets` package 값 쪽(이미 상위 고민 전부)은 손대지 않는다(HG1-7) — 기존 T9 시험이 그대로 통과 |
| 도구 설명 | `mcp_server.py` `DESCRIPTIONS["concern_candidates"]`(`:66-70`) · `["coverage"]` | 「물은 고민의 행이 0 이면 가장 가까운 윗고민의 행 — 머리 `inherited_from` · 행 `hier.match` = 상위 · `upper` = `none` 이면 0 그대로」 / `coverage` 에 「고민 노드의 indication 만 `inherited` 가 수」 |

**완료 조건**
1. T20 합성(가짜 고민 뿌리 → 자식 → 손자 — `gold_fixture.py:42` 의 계층에 행 0 인 고민을 더한다): 행 0 인 고민 → 가장 가까운 윗고민을 직접 물은 것과 **같은 `gid` 집합**(세 목록 다) · `inherited_from{concern_code, steps}` · 전 행 `hier.match` = `상위` · 행의 `asked_concern_code` 가 gold 값 그대로(= 윗고민 코드) · `ledger_check[]` 는 요청 코드의 것 · `counts.self_rows` = 0.
2. T20 합성(막는 것): **자기 행이 1 이상인 고민은 바뀌지 않는다**(`inherited_from: null` · 행에 `hier` 없음) — **묶음만 0 인 고민**(자기 행이 `modality_only[]` · `unreached[]` 뿐)도 그렇다(U-3 (a) · N-6 — 이 줄은 뒤집히지 않는다) · 바로 위도 0 이고 그 위에 행이 있으면 `steps` = 2 에서 멈춘다(**N-4**: 실물 gold 에는 `steps` 2 가 없다 — 합성으로만 시험한다) · 두 단 위까지 다 행이 있으면 가까운 쪽에서 멈춘다 · 뿌리까지 0 이면 `200` · `total: 0` · `inherited_from: null` · `upper` = `none` 이면 `total` 0.
3. T20 실물: 행 0 인 고민이 **13**(SPEC §5-9 의 코드 목록) · 13 전부 `steps` = 1 · 그 행 합 1,033 · `CON-012` → `CON-008` 의 묶음 65 · 행 181 · `ledger_check[]` 에 `LCK-010` 그대로 · 13 고민마다 `coverage` 의 `indication.inherited` = 그 조회의 `counts.rows` · 자기 행 1 이상인 고민 전부에서 `indication.inherited` = 0.
4. 기존 `test_T4_Q10_empty_pointers_is_zero_with_ledger`(`test_gold_real.py:181`)는 **고친다**(계약이 바뀐 자리 — Q10 은 이제 `total` 0 이 아니다): 기본값으로 윗고민 묶음 + `LCK-010` · `upper` = `none` 으로 0.5.1 과 같은 `total` 0. `test_T11_presence_*` 의 「있고 행 0 → `200` · `total: 0`」 은 윗고민도 없는 값으로 맞는지 확인하고, 걸리면 `upper` = `none` 을 명시해 고친다(목록에 적는다).
5. T7: `upper` 를 준 REST 응답 = MCP 응답. T6: 물려받은 응답도 끝까지 넘긴 묶음 합 = `total`.

**검증**: `uv run pytest tests/test_gold_holes.py tests/test_gold_coverage.py tests/test_gold_mcp.py -q` → 데이터 env 로 같은 파일 + `tests/test_gold_real.py`.

## 6. WP-4 — 고민 + 부위 → `concern_site`(HG3)

**목표**: `site` 를 주면 「부위 글자 일치」 **또는** 「행의 `concern_code` 가 그 부위에 묶인 고민 · 그 하위 고민」 인 행을 낸다. 새 행을 만들지 않고 대상을 바꾸지 않는다.
**SPEC**: §4-5(`site` 입력 · `counts.by_site_match` · 불릿) · **§5-9 HG3-1 ~ HG3-6** · 「어디서 합치나」(O-24 (a)) · 부록 A 「(0.5.2 HG3 — 부위 이름 읽기)」 · 「(0.5.2 HG3 — 맞추는 칸)」 줄 · 계산 필드 `site_match`(+ `csi_ids`) · §9 T22 · O-9 · O-17 ① ⑤.

| 고칠 것 | 어디 | 내용 |
|---|---|---|
| 부위 코드 | `concern.py` | `site` 글자 → `g_entry` 의 site 입구 가운데 `entity_name` 이 **글자 그대로 같은** 것의 `entity_code`(§5-7 A1 과 같은 식 — `repo.entries_by_table("site")`). 없으면 (ii) 를 돌지 않는다(HG3-2) |
| 묶인 고민 집합 | 같은 파일 | 그 부위 코드마다 `repo.concern_site_by_site()` 의 고민 + 그 고민의 `repo.descendants("concern", …)`(자손 전부). 집합의 고민마다 「어느 묶임(`id`)으로 들어왔나」 를 함께 든다(하위 고민은 그 윗 묶임의 `id`) |
| 맞춤 | `concern_candidates()`(`:33`) | 행(HG1 이 돌았으면 윗고민의 행) 가운데 (i) `st in (site_name, case_site_name)` **또는** (ii) `concern_code` ∈ 묶인 고민 집합. **합집합이다 — 0.5.1 의 행은 하나도 줄지 않는다** |
| `site_match[]` | 같은 함수 | `site` 를 건 응답의 **모든 행**에 계산 `site_match[]` — (i) 로 맞았으면 `column` 항목 · (ii) 면 `concern_site` 항목 + `csi_ids[]`(오름차순) · 둘 다면 둘 다. 항목의 꼴은 §10 A-5(SPEC 은 낱말 둘과 `csi_ids[]` 까지 정했다) |
| `counts.by_site_match` | 같은 함수 | `site` 를 걸었을 때 `{column, concern_site}` 별 행 수(둘 다 맞은 행은 양쪽에) · 안 걸었으면 `null` |
| 안 넓히는 것 | — | 부위 계층(상위 부위 → 하위 부위)으로는 넓히지 않는다(HG3-5) · `site` 로 0 이면 0 그대로 + `unfiltered_rows`(HG3-6 · O-9) · `resolve` 는 건드리지 않는다(HG3-3) |
| 도구 설명 | `mcp_server.py:67` | 「site = `site_name` · `case_site_name` 글자 일치 ∪ 그 부위에 묶인 고민 · 그 하위 고민의 행 — 행마다 `site_match[]`」 |

**완료 조건**
1. T22 합성: 낸 행 = 「글자 일치 ∪ 묶인 고민 · 그 하위 고민」 을 직접 센 것 · 글자로도 묶임으로도 맞는 행에 항목 둘 · 하위 고민 행의 `csi_ids[]` = 윗 묶임의 id · `counts.by_site_match` · **묶임 없는 (고민, 부위)는 0.5.1 과 같은 행**(0 이면 0 + `unfiltered_rows`) · 부위 입구에 없는 글자는 글자 일치만 · 상위 부위로 걸면 하위 부위에 묶인 고민은 안 맞는다.
2. T22 실물 — **W-1 을 반영한 문장으로 쓴다**(SPEC §9 T22 의 두 기준을 gold 에 맞게 고친 것 · 규칙 HG3-1 은 그대로):
   - (윗고민, 부위) **97 짝** 가운데 글자 일치 0 인 **40 짝 중 37 이 1 행 이상**이 된다. **남는 3 짝은 0 그대로다**(`CON-200` × `SITE-084` · `CON-277` × `SITE-084` · `CON-226` × `SITE-019` — 묶인 고민 `CON-206` · `CON-230` 이 행 0 인 고민이라 넣을 행이 gold 에 없다). 「40 전부」 로 단언하지 않는다.
   - 「묶인 고민 **자신**을 그 부위로 걸어도 0 이 되지 않는다」 는 **자기 행이 1 이상인 묶인 고민 91 짝**에 대해서만 단언한다(95 짝 − 자기 행 0 인 4).
   - **HG1 × HG3 이 겹치는 4 짝**(묶인 고민 자신이 행 0 — `CSI-0007` · `0047` · `0079` · `0083`): HG1 이 먼저 돌아 윗고민의 행을 그 부위로 거른다(HG3-1 「HG1 이 돌았으면 윗고민의 행」 그대로) → **2 짝(`CSI-0079` · `0083`)은 0 행 + `unfiltered_rows`** · 나머지 2 짝은 7 행씩 · 넷 다 `inherited_from` ≠ `null`.
   - 97 짝 전부에서 0.5.1 의 `gid` 집합(`site` 글자 일치만 — 시험이 직접 센다) ⊂ 0.5.2 응답의 집합(준 짝 0) · `CON-001` × `SITE-014` = **73 행 · 묶음 16**(글자 일치 24 · 묶인 `CON-005` 54 · 겹침 5) · 그 54 행의 `csi_ids[]` = `CSI-0001`.
3. T1(다시): 보조 입력 ③ 을 읽어도 gold 해시가 같다(WP-1 의 단언이 덮는다).
4. T7 · T6: `site` 를 건 응답이 REST = MCP · 끝까지 넘긴 묶음 합 = `total` · `modality_only[]` · `unreached[]` 는 첫 쪽에만.

**검증**: `uv run pytest tests/test_gold_holes.py tests/test_gold_tools_synthetic.py tests/test_gold_mcp.py -q` → 데이터 env 로 같은 파일 + `tests/test_gold_real.py`.

## 7. WP-5 — 되적기 확인 · 시험 마감 · 다시 센 수

**SPEC**: §4-1 `matched.covered_by` · §4-8 `integrity` · §4-9 `inherited` 줄 · 「상품 셈 식」 불릿 · 되적기 불릿(WORK-005 A-2 ~ A-5) · §5-8 「이름」 불릿 · 부록 A(새 다섯 줄 · 계산 필드) · §9 T3 · T23 · 문항별 기대 Q33 줄 · O-22 ①.

**되적기의 허브 몫 — 코드 대조**(11-17 확인)

| 되적은 것(SPEC 0.5.2) | 코드 | 할 일 |
|---|---|---|
| `matched.covered_by` — 나온 자리가 **전부** 덮였을 때만 | **이미 있음** · `resolve.py` + `tests/test_gold_tools_synthetic.py:79`(`test_T15_covered_only_when_every_occurrence_covered`) | T23 표지를 시험 이름 · 주석에 덧붙인다 |
| 제품 노드 `coverage` 의 `offer.inherited` = `0`(`null` 아님) | **이미 있음** · `coverage.py:112`(제품 offer 를 `자기` · `하위 제품` 으로 세어 `_layered` 가 0 을 낸다) | **단언이 없다** — 합성 · 실물에 「제품 노드 `offer.inherited == 0` 이고 `None` 이 아니다」 한 줄씩 더한다(T23) |
| `health.integrity.scope_duplicate_subject_holder_rows` | **이미 있음** · `memory.py:110-118` · `tests/test_gold_load.py:131 · 168` | T23 표지만 |
| `coverage` 상품 셈 = §4-4 맞춤 규칙의 수(계열 17 · 시술 0 · 제품 7) | **이미 있음** · `facets.py` `_holder_rows` 의 offer 갈래 · `tests/test_gold_coverage.py:324-354`(두 식을 다 센다) | **HG2 뒤에 다시 센다**(T23 「HG2 뒤는 다시 센다」) — 검수는 HG2 뒤에도 17 · 0 · 7 로 세었다(검수 §3: 케이스의 상품은 그 시술의 `procedure_code` 로 한 단에서 이미 잡힌다). 같으면 그대로 · 다르면 보고. `item_*` 식의 15 · 11 단언은 **HG2 앞(`descend` = `one`)의 수**임을 주석으로 밝히거나 닫힘으로 다시 세어 고친다 |
| `pair` 로 읽는 네 종류의 `lower` 는 `하위 제품` 없음 | **이미 있음** · `pairs.py:17`(`PAIR_ROLES`) | 도구 설명(`pair` · `coverage`)에 한 줄(SPEC §4-9 「도구 설명에 적는다」) |
| `lineup.lower_holders` · 같은 노드 두 번 · `kinds[]` 순서 · 빈 `norm` | **이미 있음** · `coverage.py:8 · 100-103` · `kinds.py` · `resolve.py` | 없음(기존 시험 통과 확인) |
| Q33 — 답 키가 상품을 입구(값 쪽 `node` = offer)로 | **이미 있음** · `facets.py` `VALUE_SIDE["offer"]` · T14 | 「두 길의 행이 같다」(§9 Q33 줄) 실물 단언 한 줄 — `offer_name_contains` 길의 `gid` 집합 = 값 쪽 `node` 길의 집합 |
| 사람이 읽는 말 `indication` = 「어디에 쓰나」 | **없음** · `kinds.py:12` 가 옛 말 | 이름 값을 고친다(응답 필드가 아니라 상수 — 응답에 나가는 자리가 있으면 그 자리를 보고한다) |

**마감 할 일**

1. T3: `headers.py` 에 부록 A 의 0.5.2 다섯 줄(보조 `concern` 두 칸 · 보조 ③ 세 칸 · 부위 이름 읽기 · 맞추는 칸 · 따라가는 칸)과 계산 필드(`inherited_from` · `site_match` · `csi_ids` · `layer.depth` · `layer.via` · `scope` 행의 `depth` · `via` · `counts.self_rows` · `counts.by_site_match`)를 넣고 기계 대조가 통과한다. 「(보조)」 줄이 **일곱**(0.5.1 의 다섯 + 둘)임을 단언한다.
2. `test_tool_list`: 도구 **9** 그대로 · 새 입력(`descend` 셋 · `upper` 하나)이 MCP 입력 스키마에 있다 · 설명 문장(HG2-7 · N-2 · HG1 · HG3 · 0.5.1 W-4)이 `list_tools` 에 그대로 보인다.
3. **다시 센 수 둘 — W-2**: SPEC 의 두 수는 어느 식으로도 다시 나오지 않았다(검수 §2 #13 · #16). **시험 기준에 박지 말고 세는 식과 함께 다시 세어 보고한다**:
   - 「케이스를 한 끝으로 둔 `g_pair` 행」(SPEC §5-9 · SPEC-002 §9-3d 는 129): 식 = **계열 18 의 닫힘으로 닿는 케이스 268 을 `from` 또는 `to` 로 둔 서로 다른 `g_pair` `gid` 수**(검수 셈 100) + 계열마다 세어 더한 값(검수 셈 104). 둘 다 적는다.
   - 「97 짝의 행 합」(SPEC §5-9 는 289 → 1,700): 식 = **97 (윗고민, 부위) 짝마다 `concern_candidates(윗고민, site)` 의 `counts.rows` 합**(HG3-1 (ii) 가 「자손 전부」 이므로 검수 셈 1,722 가 기대값이다 · 자손을 빼면 1,662). 앞 값 289 는 글자 일치만의 합.
   - 시험은 「도구 응답 = 직접 센 값」 을 단언하고, 위 기대값(100 · 104 · 1,722)은 **보고에 수로 적는다**(SPEC 되적기 재료 — §10 A-6).
4. e2e 가 실패했던 꼴을 **도구 수준에서** 한 번씩(실물 · 포트 없이 — 코드만 · 문장 없음): ① e2e 4 꼴 `concern_candidates("CON-001", site = SITE-014 의 `entity_name`)` → 73 행 · 묶음 16 ② Q10 꼴 `concern_candidates("CON-012")` → `inherited_from` = `CON-008` · 묶음 65 ③ Q12 꼴 계열 `M2` 의 `facets` adverse(하위 셋) → 표본 4 가 든다. 부위 이름은 시험이 `g_entry` 에서 읽는다(코드에 글자로 넣지 않는다).
5. 마지막에 **한 번** README 「검증」 전체: `uv run ruff check app tests scripts` · 데이터 env + `DATABASE_URL=sqlite+aiosqlite:///:memory: uv run pytest --ignore=tests/integration`. 통과 · skip 수를 §1 의 기준선과 나란히 보고한다.
6. **고친 기존 시험 목록**을 보고한다(이름 · 까닭 한 줄) — 예상: `len(rec.files)` 둘(WP-1) · Q10 의 `total` 0(WP-3) · 합성 계열의 `lower` · `scope` 단언(WP-2 — fixture 가 이미 두 단이라 걸릴 수 있다) · `coverage` 설명 낱말. 목록 밖의 기존 시험이 바뀌었으면 그것이 지적이다.
7. `backend/README.md` gold 절: 보조 입력 파일 목록에 `concern_site.csv` · 새 입력 둘을 한 줄씩.
8. **18106 에 띄워** `health`(`files[]` 22 줄 · `aux_hash`) · 위 4 의 세 꼴을 REST 로 한 번 · MCP `list_tools`(9 · 설명)를 보고 **띄워 둔다** — `GOLD_EXPECTED_HASH` 를 주고 띄운다(11-16 값). 띄우기 전 `lsof -nP -iTCP:18106 -sTCP:LISTEN` 으로 비었는지 확인한다. 띄운 뒤 코디에게 알린다(앱 워커가 WORK-008 WP-3 에 쓴다 · §8).
9. 커밋 후보 grep: 시술 · 고민 · 부위 이름 · 질문 문장 · 실제 `gid` · 홈 경로 0(SPEC 에 적힌 코드 · 수는 예외 — §2).

**완료 조건**: T20 ~ T23 이 시험 이름 또는 주석으로 찾아진다 · 위 1 ~ 9 · `git status --porcelain` 이 §2 allowed_paths 안의 파일뿐이다.

## 8. 순서 · 병행

| 순서 | 무엇 | 근거 |
|---|---|---|
| WP-1 먼저 | 보조 ③ 색인이 WP-4 의 재료다 · fixture 가 바뀐다 | — |
| WP-2 → WP-3 → WP-4 | 한 워커가 차례로. WP-2(닫힘)와 WP-3 · WP-4(`concern.py`)는 파일이 갈리지만 `mcp_server.py` · `headers.py` · `coverage.py` · fixture 를 함께 건드린다 | 병행의 이득이 작다 |
| WP-5 | 마지막 | 전체 검증은 끝에 한 번 |
| **앱과 나란히** | 앱(WORK-008)의 WP-1(세트 칸) · WP-2(새 응답 받기 — 모의) · WP-4(구멍 묶음 꼴) · WP-5(되적기 확인)는 이 문서를 기다리지 않는다. **앱이 보는 새 응답 꼴은 아래 「응답 꼴」 셋뿐이다.** 앱의 답 키 다시 뽑기(WP-3) · 실물 확인(WP-6)은 **이 문서 WP-5 의 18106 뒤** | 계약이 SPEC 에 고정돼 있다 |
| 허브 바꿔 끼우기 | WP-5 가 끝나면 코디에게 알린다. **18105 를 새 코드로 다시 띄우는 것은 코디가 앱 새 코드와 함께** 한다(새 허브는 넓어진 응답을 낸다 — 옛 앱도 깨지지는 않지만 층 표지가 빠진 채 답한다) | 사용자 e2e 화면(18220)이 중간에 반쯤 바뀌지 않게 |

**응답 꼴 — 앱이 모의로 쓰는 계약**(코드는 가짜다 · 바뀐 필드만)

```json
{
  "concern_candidates(HG1)": {
    "request": {"concern_code": "CON-90003", "site": null, "upper": "auto", "cursor": null, "limit": 100},
    "inherited_from": {"concern_code": "CON-90002", "steps": 1},
    "counts": {"rows": 3, "groups": 2, "procedures": 2, "modality_only": 0, "unreached": 0,
               "unfiltered_rows": 3, "self_rows": 0, "by_site_match": null},
    "groups": [{"candidate_table": "procedure", "candidate_code": "PRC-90001", "rows": [
      {"gold_table": "g_indication", "gid": "GIN-90001", "asked_concern_code": "CON-90002", "concern_code": "CON-90004",
       "concern_match": "하위 고민", "hier": {"asked_code": "CON-90003", "match": "상위"}}]}]
  },
  "concern_candidates(HG3)": {
    "request": {"concern_code": "CON-90001", "site": "<부위 이름>", "upper": "auto"},
    "inherited_from": null,
    "counts": {"rows": 2, "unfiltered_rows": 9, "self_rows": 9, "by_site_match": {"column": 1, "concern_site": 2}},
    "groups": [{"rows": [
      {"gid": "GIN-90002", "site_match": [{"by": "column"}, {"by": "concern_site", "csi_ids": ["CSI-9001"]}]},
      {"gid": "GIN-90003", "site_match": [{"by": "concern_site", "csi_ids": ["CSI-9001"]}]}]}]
  },
  "facets(HG2 — 하위 role 을 준 대상 쪽 행의 layer)": {
    "layer": {"role": "하위 케이스", "path": "<g_scope.path>",
              "holder": {"holder_table": "procedure_case", "holder_code": "CAS-90001", "holder_name": "<이름>"},
              "scope_gid": "GSC-90002", "depth": 2,
              "via": [{"holder_table": "procedure", "holder_code": "PRC-90001", "scope_gid": "GSC-90001"}]}
  }
}
```

(`site_match[]` 항목의 열쇠 `by` 는 이 문서의 제안이다 — §10 A-5. `coverage` 의 고민 노드는 `{"kind": "indication", "self": 0, "lower": null, "lower_holders": null, "inherited": 3}` 꼴이 된다. `via[]` 에는 **이름이 없다**(SPEC §5-9 HG2-4 — 표 · 코드 · `scope_gid` 뿐) — 앱이 이름을 얻는 길은 WORK-008 WP-2.)

## 9. 검수 지적 반영 — WARN 3 · NOTE 6(`review-spec-v052.md` §7)

| # | 지적(한 줄) | 이 문서에서 | 어디 |
|---|---|---|---|
| **W-1** | T22 의 실물 기준 둘이 gold 와 다르다(40 → 37 · 묶인 고민 자신이 행 0 인 4 짝) | T22 를 「40 중 37 · 남는 3 은 묶인 고민 행 0」 · 「자기 행 1 이상인 91 짝은 0 이 되지 않는다」 로 쓰고, HG1 × HG3 이 겹치는 4 짝의 기대(2 짝 0 + `unfiltered_rows` · 2 짝 7 행)를 못 박았다 | §6 완료 조건 2 |
| **W-2** | 다시 세어 안 나오는 수 둘(케이스 끝 `g_pair` 129 · 97 짝 행 합 1,700) | 시험 기준에 박지 않는다 — 세는 식을 정해 다시 세어 보고(기대 100 · 104 / 1,722) | §7 마감 3 · §10 A-6 |
| **W-3** | SPEC-002 §9-3d HG2 (iii) 「두 단 아래에만 상품」 은 허브 맞춤 식으로 0 건 | 허브 시험에는 그 꼴이 없다 — 상품은 HG2 뒤에도 17 · 0 · 7 인지 다시 센다. 문항 꼴을 바꾸는 것은 앱 쪽 | §7 표 「상품 셈」 줄 · WORK-008 WP-4 |
| N-1 | `descend` 가 `facets` · `pair` 입력 표에 없다 | 세 도구 입력에 같은 줄 | §4 표 「입력 `descend`」 |
| N-2 | 계열에 `하위 케이스` 만 주면 케이스에 못 닿는다 | 도구 설명 한 줄 + 합성 시험 | §4 표 「도구 설명」 · 완료 조건 2 |
| N-3 | 「제품의 하위 제품」 을 거치는 13 짝은 한 방향 관계다 | 규칙은 그대로 — `layer.depth` · `via[]` 로 밝힌다. 실물 시험에서 그 13 짝의 행에 `via[]` 가 그 제품을 가리키는지 한 건 본다. 답에서 어떻게 읽히는지는 앱 실물 확인 | §4 완료 조건 3 · WORK-008 WP-6 |
| N-4 | `inherited_from.steps` 2 는 지금 gold 에 없다 | 합성 fixture 로 2 를 시험 · 실물은 「13 전부 1」 | §5 완료 조건 2 · 3 |
| N-5 | U-2 로 Q03 · Q05 의 기대 종류가 는다 | 허브 무관 — 앱 쪽 | WORK-008 WP-1 · WP-3 |
| N-6 | U-3 을 (b) 로 정하면 T20 한 줄 · HG1 묶음 (iii) 이 뒤집힌다 | **U-3 = (a) 로 닫혔다** — T20 의 「묶음만 0 인 고민은 바뀌지 않는다」 줄을 그대로 쓴다 | 머리말 · §5 완료 조건 2 |

## 10. 열린 것 · 이 문서를 쓰며 본 것(SPEC 은 고치지 않았다)

| # | 무엇 | 이 문서의 제안 | 상태 |
|---|---|---|---|
| A-1 | 닫힘을 적재 때 세어 둘지 요청 때 따라갈지(SPEC §3-1 · O-23) | **요청 때 따라간다** — 가장 긴 길 4 단 · `scope_by_subject` 색인 하나면 된다. `coverage` 64 노드 한 번의 ms 를 0.5.1 값과 나란히 보고하고, 눈에 띄게 느리면 적재 때 세는 쪽으로 | 구현 때 정함 |
| A-2 | `health.aux` 에 보조 ③ 의 수를 실을지 — SPEC §4-8 의 `aux` 꼴에는 `hierarchy` · `ledger_check` 뿐이다 | `aux.concern_site{rows, concerns, sites}` 를 더한다(O-12 ③ 의 「적재한 수」 와 같은 꼴 · 계산 필드) — 넣었으면 보고 | 구현 때 정함 — SPEC 되적기 후보 |
| A-3 | T21 「`descend` = `one` 이면 0.5.1 과 같은 응답」 — HG2-4 는 `depth` · `via` 가 **모든 대상 쪽 행에** 붙는다고 적었다 | 「같은 응답」 = 같은 행 · 순서 · `total` · `counts`. 새 계산 필드(`depth` 1 · `via` `[]`)와 `request.descend` 는 붙는다 | 구현 때 정함 |
| A-4 | 물려받은 응답의 `counts.unfiltered_rows` — SPEC §4-5 는 「`site` 를 안 걸었을 때 행 수」, HG1-1 은 걸리는 때를 「`unfiltered_rows` = 0」 으로 적었다(물려받기 **앞**의 값) | 응답에는 **`site` 를 안 걸었을 때 이 응답이 낼 행 수**(물려받았으면 윗고민의 행 수)를 낸다 — HG3-6 「0 이면 0 + `unfiltered_rows`」 가 물려받은 응답에서도 뜻이 서게. 물은 고민 자신의 0 은 `self_rows` 와 `inherited_from` 이 말한다. 검수 W-1 의 「2 짝은 0 + `unfiltered_rows`」 와 같은 읽기다 | 구현 때 정함 — SPEC 되적기 후보 |
| A-5 | `site_match[]` 항목의 꼴 — SPEC 은 `column` · `concern_site`(+ `csi_ids[]`) 까지(O-23) | `[{"by": "column"}, {"by": "concern_site", "csi_ids": […]}]`(§8 응답 꼴). 어느 칸으로 맞았는지는 행의 칸 값으로 보이므로 `column` 항목에 칸 이름을 싣지 않는다(SPEC HG3-4 문장 그대로) | 구현 때 정함 |
| A-6 | W-2 의 두 수 · §4-9 끝 불릿의 「한 단 기준」 수 | 다시 센 값과 식을 **보고에** 적는다 — SPEC 은 이 워커가 고치지 않는다(코디가 되적기 때 쓴다) | 보고 |
| A-7 | 대상 쪽 `facets` 행의 순서 — 지금 holder `g_scope.gid` → 행 `gid`. 닫힘의 holder 가 끼면 | holder 를 (`depth`, `scope_gid`) 순으로 → 행 `gid`. `depth` 1 끼리는 지금 순서와 같다(`descend` = `one` 응답이 0.5.1 과 같은 순서 — A-3) | 구현 때 정함 |
| A-8 | 닫힘이 따라가는 role — HG2-2 는 「요청이 준 하위 role 뿐」. `scope` 를 `roles` 없이(전부) 부르면 | 하위 셋 전부로 따라간다(「전부」 의 뜻 그대로) | 구현 때 정함 |
| O-23 | 0.5.2 의 이름 · 꼴(`upper` · `descend` · `inherited_from` · `counts.self_rows` · `counts.by_site_match` · `site_match[]` · `layer.depth` · `layer.via[]`) | 본문 그대로 | SPEC 제안 그대로 |
| O-25 | HG1 이 내는 행 = 윗고민으로 물은 행 전부 | 본문 그대로(직접만 고르지 않는다) | 1회차 trace 뒤 |
| O-26 | HG2 뒤 커지는 응답 | 자르지 않는다 — 크기 · ms 보고(§4 완료 조건 7) | 1회차 trace 뒤 |

**이번 판에 구현 대상이 아닌 절**: §8 stg · O-3 · O-7 · O-8 · O-11(뒤 단계) · O-15 · O-17(1회차 trace 뒤 — HG3-5 가 「부위 계층으로는 안 넓힌다」 를 다시 적었다) · O-22 ②(stg 올릴 때). 「제품 경유」 는 여전히 하위가 아니다(O-21 의 남은 것 — 따라가지 않는다).

## 11. SPEC-001 0.5.2 변경 절 ↔ WP 대응(미대응 0)

변경 기록 「결정 · 지시 → 문서 자리」 표의 행 순서 그대로.

| 변경(변경 기록의 행) | 절 | WP |
|---|---|---|
| HG1 고민 → 윗고민 물려받음 | §4-5(입력 · 출력 · 불릿) · §4-9 `inherited` · §5-5 H5 · H6 · §5-8 · §5-9 HG1 · §9 T20 · Q10 줄 · U-3 · O-25 | WP-3 · WP-5(설명 · T3) |
| HG2 하위 = 자손 전부 | §3-1 · §4-2 · §4-4 `roles` · §4-6 규칙 1 · 3 · §4-9 `lower` · §5-3 S6 · §5-8 `lineup` · §5-9 HG2 · §9 T21 · Q12 줄 · O-21 · O-26 | WP-2 · WP-5(설명 · T3 · 다시 센 수) |
| HG3 고민 + 부위 → `concern_site` | §2-1(표 · X7) · §2-2 · §2-3 4 · §3-1 · §4-5 · §5-9 HG3 · §9 T22 · 부록 A · U-4 · O-24 | WP-1(적재) · WP-4(맞춤) · WP-5(T3) |
| 상품 셈 식 | §4-9 수 · 「상품 셈 식」 불릿 · §9 T23 | WP-5(이미 있음 — HG2 뒤 다시 셈) |
| 제품 offer `inherited` = 0 | §4-9 `inherited` 줄 · T23 | WP-5(이미 있음 — 단언 더함) |
| A-1 `covered_by` | §4-1 · T23 | WP-5(이미 있음 — 표지) |
| 구현에서 정해진 그 밖(N-5 · N-8 · A-2 ~ A-5) | §4-9 · §4-8 · O-22 ① | WP-5(이미 있음 — `pair` 종류의 `lower` 설명 한 줄만 더함) |
| 화면 말 「적응」 → 「어디에 쓰나」 | §5-8 표 · 불릿 | WP-5(`kinds.py:12`) |
| Q33 답 키 입구 | §9 문항별 기대 Q33 줄 | WP-5(두 길의 행이 같다 — 단언) |
| (끌어낸 것 ⑤) 묶인 고민 자신 + 그 부위 | §5-9 HG3 「같은 구멍의 다른 꼴」 · T22 | WP-4 완료 조건 2 |
| (고치지 않은 것) §4-9 · §5-3 S6 의 `lower` 수 = 한 단 기준 | §4-9 끝 불릿 · §5-9 끝 불릿 | WP-2 완료 조건 6 · WP-5 마감 3 |
| 부록 A 새 다섯 줄 · 0.5.2 계산 필드 | 부록 A | WP-1 · WP-5 마감 1 |
| `aux_hash` · 옛 cursor = `cursor_invalid` | §2-3 4 | WP-1 완료 조건 1 · 5 |

## 변경 기록

### 0.1.0 (2026-11-17)

- 새로 씀 — SPEC-001 0.5.2 의 변경 절을 WP 다섯으로. 사용자 결정 U-3 · U-4 는 추천으로 닫힌 값으로 적었다(_RESUME §2 11-17). `review-spec-v052.md` §7 의 WARN 3 · NOTE 6 을 §9 에 한 줄씩 넣었다 — 허브에 닿는 것은 W-1(T22 문장) · W-2(수 둘) · N-1 ~ N-4 · N-6 이고, W-3 · N-5 는 앱 쪽(WORK-008)이다.
