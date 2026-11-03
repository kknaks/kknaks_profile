---
type: work
id: WORK-002
title: "그래프 v2 구현 — 큐레이션 적재 · 빌드 · 검증 · tool · E2E (오늘 안 · 축소 범위)"
status: todo
product: procedure-hub
feature: phub-recommend
work_type: change
owner: "backend 워커"
roles:
  pm: "코디네이터"
  design: ""
  fe: ""
  be: "backend 워커"
  qa: "reviewer_code 워커 · 코디(E2E)"
  ops: ""
progress: 0
created_at: 2026-10-27
updated_at: 2026-10-27
tags:
  - product/procedure-hub
  - feature/phub-recommend
  - doc/work
  - status/todo
links:
  baselines: []
  decisions:
    - "orchestration/work/phub-recommend/DEC-001.md"
    - "orchestration/work/phub-recommend/DEC-002.md"
    - "orchestration/work/phub-recommend/DEC-003.md"
  specs:
    - "orchestration/work/phub-recommend/SPEC-004.md"
    - "orchestration/work/phub-recommend/SPEC-001.md"
  works:
    - "orchestration/work/phub-recommend/WORK-001.md"
  releases: []
  related:
    - "orchestration/work/phub-recommend/_RESUME.md"
    - "orchestration/work/phub-recommend/review-spec-004-report.md"
---

> **SPEC-005 · WORK-003 으로 대체됨(2026-10-30)**

# 그래프 v2 구현 — 큐레이션 적재 · 빌드 · 검증 · tool · E2E (오늘 안 · 축소 범위)

SPEC-004 0.2.0 의 **오늘 범위**를 WORK-001 이 만든 graph 모듈 위에 구현한다. 순서는 적재 → 노드 → 엣지 → 검증 · 발행 → tool → E2E 이고, 약 5시간을 잡는다.
**비목표**: SPEC-004 §8 「2차」 전부 · 식약처 API · 운영 화면 · 상담 에이전트 · 배포 · commit/push(코드는 로컬 전용 · 미커밋 — `_RESUME` §1).

> 계약은 SPEC-004(달라지는 것)와 SPEC-001(그대로인 것)이 갖는다. 이 문서는 순서 · 파일 · 검증 명령만 갖는다. 둘이 다르면 SPEC 을 따른다.

> **변경 이력**
> - 2026-10-27 검수 반영(`review-spec-004-report.md`) — 실물 입력 계약(F-1 · F-2) · 허가 후보로 제조사(F-3 a) · `include_unconfirmed`(W-1) · 동점 후보 전부(W-2) · Phase 0 축소(W-5) · `graph_support.py` 포함(W-8) · schema 판정 제거(W-9) · 4차 원장 재대조(W-7) · 범위 축소(약 5시간)
> - 2026-10-27 초안

## Meta

- Covers spec: SPEC-004 0.2.0 §1 「오늘」 범위(+ SPEC-001 에서 바뀌지 않은 절)
- Depends on work: WORK-001(v1 코드 — 미커밋 상태로 워크트리에 있다)
- 입력(`$W` = `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend`):
  - `procedure-master-v3.json`
  - `product-master-draft.json`(`version` 4)
  - `source-fix-list.json`
  - `gate-answers/product-match.json` · `gate-answers/source-fix.json` · `gate-answers/classify-v1.json` · `gate-answers/classify-v2.json`
- 코드: `/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-recommend`(브랜치 `kknaksss/phub-recommend`). 명령은 전부 `backend/` 에서 친다
- 로컬: DB `phub-graph-postgres`(55434 — v1 발행본 있음) · 앱 18005
  - **사용자 포트 · 프로세스는 건드리지 않는다**(3700 · 3800 · 8700 · 8800 · 54329 · `procedure-*`)
  - `envs/.env.graph` 는 이미 있다 — `cp envs/graph.env.example …` 를 **치지 않는다**
- 외부 호출 없음(stg · 식약처 · 모델)

## Work Summary

| Field | Value |
|---|---|
| Goal | v1 그래프를 SPEC-004 v2 로 **교체**하고, REST 7 · MCP 6 이 v2 를 서빙한다(기본 = 승인 · 자동만) |
| Non-goal | 새 테이블 · alembic · graph 밖 변경 · SPEC-004 §8 |
| 완료 판정 | Phase 5 E2E 스크립트 PASS(E-1~E-5) + 전체 테스트 · ruff 통과 + 코디가 Swagger · MCP 로 E-2 · E-4 를 한 번씩 확인 |

## Scope · Code Surface

| 파일 | 변경 | SPEC-004 |
|---|---|---|
| `app/modules/graph/domain.py` | 노드 16 · 엣지 16 타입 표와 설명 · 필수 원천 14 · 큐레이션 원천 이름 · 검증 코드 · 타입 순서 · 게이트 순위 | §3.1.1 · §3.2.4 · §3.3.4 · §3.4 |
| `app/modules/graph/curation.py`(새) | 실물 칸 어댑터(§3.1.2 · §3.1.3) · `approval`/`status` → `gate_status` · 이름 치환표 · 노드(계열 · 단위 시술 · 부위 · 기법 · 목적 · 패키지 · 제품 · 품목 · 제조사 · 규격) | §3.1 · §3.2 |
| `app/modules/graph/lowering.py`(새) | 규칙 A · 부위 일치 · `treats` ①~⑤ · 계열 `procedure_relation` 끝 · 그 밖 엣지 D | §3.3.3 |
| `app/modules/graph/resolve.py` | v2 사전 · **모호 = 후보 목록 반환**(동점 선택 코드 제거) | §3.3.2 |
| `app/modules/graph/sources.py` | stg 추출기 재배선(고민 트리 · 어휘 · 부작용 유지, 시술군 · 시술 항목 · v1 제품 · v1 부위 노드 제거) · `build_graph` 조립 | §3.2 · §3.3 |
| `app/modules/graph/validation.py` | v2 코드 · `coverage_gap` 이름 바꾸기 · `counts.schema="v2"` | §3.4 |
| `app/modules/graph/application.py` | 적재 `--curation-dir` · 빌드 필수 원천 14 · 조회(`include_unconfirmed` 거르기 · `Edge.gate_status` · Safety v2 · 검색 synonym 열 · 동점 전부 · `count_by_gate`) | §3.1 · §4 |
| `mcp_server.py` · `router/graph.py` · `schema/graph.py` · `swagger_docs/graph.py` | `include_unconfirmed` · 새 필드 · 타입 허용값 · tool 설명 문장 · 404 문구 | §4 |
| `scripts/graph_ingest.py` | `--curation-dir` | §3.1 |
| `scripts/graph_e2e_check.py` | v2 로 교체(E-1~E-5) | §6 |
| `scripts/graph_v2_expected.py`(새) | 입력만으로 노드 타입별 · 게이트별 수 + E2E id 목록 | §6.1 |
| `tests/graph_support.py` | v1 stg fixture 빌더 → v2(큐레이션 fixture 포함) | §5.1 · W-8 |
| `tests/fixtures/graph_v2/`(새) | 실물에서 잘라 낸 큐레이션 fixture · `expected.json` | — |
| `tests/test_graph_{ingest,domain,sources,build,api,mcp}.py` | v1 단언 → v2(build 59/79/49 · api 59/24/49/15 · `missing_bronze` 10 → 14 · sources `treats` 26 등) | W-8 |
| `tests/test_graph_curation.py` · `tests/test_graph_lowering.py`(새) | 아래 Phase | — |
| `docs/graph-local.md` | v2 순서 · `include_unconfirmed` · 게이트 답 갱신 시 재적재 | — |

손대지 않는 것: alembic · `app/model/graph.py` · `tests/test_graph_boundary.py`(그대로 통과해야 한다) · graph 밖 전부 · `envs/.env.graph`.

## Execution

각 Phase 끝에는 **그 Phase 테스트만** 돌린다. 전체 테스트 · ruff 는 Phase 5 에서 한 번 돌린다.
공통 접두: `cd /Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-recommend/backend`. 테스트 env 는 `DATABASE_URL=sqlite+aiosqlite:///:memory:` 다.

### Phase 0 — 체크포인트 · 입력 대조 · 기대값 (30분)

1. **v1 체크포인트**(커밋하지 않는다):
   ```bash
   CK=/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-v1-checkpoint-2026-10-27; mkdir -p $CK
   git -C .. diff > $CK/tracked.diff
   git -C .. ls-files --others --exclude-standard -z | xargs -0 tar czf $CK/untracked.tgz -C ..
   ```
2. **입력 대조**(레포 밖 스크립트): SPEC-004 §3.1.2 · §3.1.3 의 필수 칸 · 상태값 · 행선지 type · `site_status` 를 실물과 대조해 표로 남긴다. 확인할 값은 실물 수(단위 시술 236 · `approval` 5종 · 행선지 11종 · 제품 게이트 `status` 4종 · `license_keys` 486 의 후보 조인 486/486)와 E2E id(`UP-M2-004` · `UP-M2-011` · `UP-M11-001` · `UP-M1-006` · `UP-M9-018` · `M1-2-1` auto · `M2-2-1` auto · `M11-1-1` pending)다
3. **escalation 기준**: 필수 칸이 없거나 알 수 없는 상태값 · type 이 **새로** 생겼으면 코디에게 `escalation` 을 보낸다. 수만 바뀌었으면 대조표에 적고 진행한다(시술 원장이 아직 고쳐지는 중이다)
4. **기대값**: `scripts/graph_v2_expected.py --work-dir $W --stg-dir /Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-stg-2026-10-26 --out tests/fixtures/graph_v2/expected.json`. 빌드 코드를 import 하지 않는다. **노드 타입별 수 · 게이트별 수 · E-1~E-4 의 있어야 함 / 없어야 함 id** 까지만 쓴다(엣지 · 이슈 수는 2차)

검증: 대조표와 `expected.json` 이 있다. 대조표 경로를 코디에게 메시지로 알리고, 기다리지 않고 Phase 1 로 간다.

### Phase 1 — 큐레이션 브론즈 적재 (20분)

- `domain.py`: 큐레이션 원천 7행(필수 5 + 보관 2) · 파일 이름표 · 필수 원천 14(`products` 는 보관)
- `scripts/graph_ingest.py` · `application.py`: `--curation-dir` — 같은 해시 · 멱등. `input_mode="dir"` · `source_location` = 파일 경로. 없는 파일은 `failed`(`file_not_found`) · 종료 코드 1
- `tests/test_graph_ingest.py`: 7 `inserted` → 다시 7 `unchanged` · 하나 바꾸면 그것만 `inserted` · 없는 파일 `failed`

검증:
```bash
DATABASE_URL=sqlite+aiosqlite:///:memory: uv run pytest tests/test_graph_ingest.py -q
uv run --env-file envs/.env.graph python scripts/graph_ingest.py --curation-dir $W     # inserted 7
uv run --env-file envs/.env.graph python scripts/graph_ingest.py --curation-dir $W     # unchanged 7
```

### Phase 2 — 실버 노드 v2 (1시간 15분)

- `curation.py`:
  - 어댑터 — 필수 칸이 없으면 `curation_shape_error`. 참조가 깨지면 노드 · 엣지를 만들지 않고 warning
  - 상태 매핑표 — `approval` 6종 + 모르는 값, 제품 게이트 `status` 4종 + 모르는 값
  - 노드 — 계열(`modality_codes` = M 이면 `[id]`, X 는 `[]`) · 부위(`site:<원문>` · 「(묶음)」 을 뗀 name) · 기법 · 목적(이름) · 패키지(`components`) · 단위 시술(`site_status` 5갈래) · 제품(브랜드 병합 · `license_status`) · 품목(`groups()` 묶음 규칙 · 의료기기는 모델명) · 제조사(§3.2.6 — 후보 행의 `company` · `manufacturer_original`) · 규격(`specs[]` 만)
  - 이름 치환표 — A1 × `fix` · 문자열 전체 일치 · taxonomy · problem-packages · `problem_tree` 동의어 · 원천 표기는 동의어로 남김
- `sources.py`: 고민 트리 · 어휘 · 부작용 추출기는 유지하고 치환 뒤 값을 쓴다. 시술군 · 시술 항목 · v1 제품 · v1 부위 노드는 없앤다. 계열 `extracted` · `session_phase_order` 는 코드로 끌어온다
- 위험 부위 대응(§3.2.5) → `danger_zone_ids`
- fixture `tests/fixtures/graph_v2/`: 실물 행을 **복사해 줄인다**(지어내지 않는다)
  - 계열 M1 · M2 · M9 · M11 · X1
  - 부위 트리 중 얼굴 · 턱(묶음) 가지 · 볼(묶음) 가지 · 얼굴 전체
  - 단위 시술: `UP-M1-006`(approved) · `UP-M2-004` · `UP-M2-011` · `UP-M11-001` · `UP-M9-018` · 「해당 없음」 1 · `null` 1
  - 원장 행: `M1-2-1` · `M2-2-1` · `M11-1-1` · package 1 · hold 1
  - 제품 게이트 행: auto · not_applicable · unconfirmed · pending 각 1 — 실물에 user · none 은 없으므로 넣지 않는다
  - `source-fix` A1 전부
- `tests/test_graph_curation.py`:
  - 노드 타입별 수 · id 안정
  - 게이트 매핑(`approval` 6 + 모르는 값 · 제품 게이트 4 + 모르는 값)
  - 부위 `site_status` 5갈래의 엣지 · 경고
  - 치환(「바디 쳐짐」 → 「바디 처짐」 · 동의어 「바디 쳐짐」)
  - `license_status`: 실물에 있는 licensed · not_applicable · unconfirmed(+ 취소 허가만 있는 행이 fixture 에 있으면 cancelled)
  - 품목 묶음(보톡스 2 key → 품목 1 · 쥬비덤 → 모델명별 여럿)
  - 제조사(쥬비덤 → 한국애브비(주) · Allergan / 보톡스 → 한국애브비(주)만)
  - `curation_shape_error` · `dangling_reference`(warning) · `ledger_destination_skipped`(hold)

검증:
```bash
DATABASE_URL=sqlite+aiosqlite:///:memory: uv run pytest tests/test_graph_curation.py tests/test_graph_domain.py -q
```

### Phase 3 — 시맨틱 엣지 v2 · 내림 (50분)

- `resolve.py`: v2 사전(단위 시술은 이름 + `ledger_item` · `market` 동의어) · 행선지 해석. **후보가 둘 이상이면 「모호」 를 돌려준다** — 사전순 선택 코드를 지운다
- `lowering.py`: 규칙 A(§3.3.3 A) · 부위 일치 · `treats` ①②③⑤ · ④(단위 시술 하나 · 계열 · 제품 → 계열 하나만, 모호 · 못 풂이면 엣지 없음) · `procedure_relation` **계열 단위만**(synergy 는 원천 시술군 코드) · D(`has_complication` · `site_caution` · `has_product` · `uses_product`)
- `sources.py`: 주장에 `gate_status` · `lowering` · `conditions.*` 를 단다. `has_unit` · `at_site` · `uses_technique` · `includes` · `has_item` · `licensed_to` · `manufactured_by` · `has_spec` · 부위 `has_child` · `synonym`(+ purpose)
- `tests/test_graph_lowering.py`:
  - 규칙 A 실물 예 5개(볼 · 눈꺼풀 · 팔뚝/복부/허벅지 · 턱선무너짐 없음 · 이중턱 없음)
  - 부위 일치 셋(`exact` · `ancestor` · `whole_area`)
  - 부위 없음 → 계열 + `treats_not_lowered`
  - **모호 이름 → 엣지 없음 + `ambiguous_name_ref`**(예: 「울쎄라」 가 여러 단위 시술에 걸림 — 단, 해석 사전에서 device 동의어는 빠지므로 `market` · `ledger_item` 에서 실물로 겹치는 이름을 고른다)
  - 계열 쌍 M1↔M2 엣지 하나 · `conflict` · 주장 `auto`
  - 자기 쌍 제외 · 주장 게이트 = 가장 약한 값
- `tests/test_graph_build.py` · `tests/test_graph_sources.py`: v1 단언을 v2 fixture 기준으로 고친다(`graph_support.py` 와 함께)

검증:
```bash
DATABASE_URL=sqlite+aiosqlite:///:memory: uv run pytest tests/test_graph_lowering.py tests/test_graph_build.py tests/test_graph_sources.py -q
```

### Phase 4 — 검증 v2 · 발행 · 실DB 빌드 (30분)

- `validation.py`: SPEC-004 §3.4 코드 · `coverage_gap` 이름 바꾸기 · `counts.schema="v2"`(판정에는 쓰지 않는다 — W-9)
- `application.py` 빌드: 필수 원천 14
- 실DB 빌드 → `expected.json`(노드 · 게이트 수)과 대조

검증:
```bash
uv run --env-file envs/.env.graph python scripts/graph_build.py     # published · graph_version = v1 마지막 + 1 · error 0
uv run --env-file envs/.env.graph python scripts/graph_build.py     # unchanged
```
수가 다르면 먼저 규칙 구현과 기대값 계산 중 어느 쪽이 SPEC 과 다른지 가린다. 숫자를 맞추려고 한쪽을 고치지 않는다. SPEC 해석이 갈리면 코디에게 `ask` 한다.

### Phase 5 — 조회 tool · E2E · 문서 (1시간 30분)

- `application.py` 조회:
  - `include_unconfirmed` 거르기(노드 · 주장 · 엣지 · 펼치기 · 404 문구 · 안전 주장 예외 · `gate_filter`)
  - `Edge.gate_status` 계산
  - Safety v2(계열 상속 · `site_cautions` 조상까지 · `gaps` 넷)
  - 검색 synonym 열 · **동점 전부**
  - 목록 `gate_status` · 스키마 `count_by_gate`
- `schema` · `router` · `swagger_docs` · `mcp_server`: 파라미터 · 필드 · 타입 허용값 · tool 설명 문장(SPEC-004 §4.2 표)
- `tests/test_graph_api.py` · `tests/test_graph_mcp.py` v2:
  - 기본 응답에 `unconfirmed` 0
  - `include_unconfirmed=true` 에서 전부
  - `unconfirmed` 노드 `get_node` 404
  - 「보톡스」 계열 + 제품 동점 전부
  - `UP-M1-006` safety 상속
  - MCP = REST 같은 JSON
- `scripts/graph_e2e_check.py`: SPEC-004 §6 E-1~E-5 단계를 그대로 부르고 `expected.json` 의 id 목록과 대조한다. E-4 는 MCP(JSON-RPC `tools/call`)로도 한 번 부른다
- `docs/graph-local.md` 갱신

검증(전체 — 이 work 에서 한 번):
```bash
uv run ruff check app tests scripts
DATABASE_URL=sqlite+aiosqlite:///:memory: uv run pytest --ignore=tests/integration -q
uv run --env-file envs/.env.graph uvicorn app.graph_main:app --port 18005 &
uv run python scripts/graph_e2e_check.py --base-url http://127.0.0.1:18005      # E-1~E-5 PASS
# 확인 뒤 18005 프로세스 종료(DB 는 그대로)
```

### 4차 원장 · 게이트 답이 오늘 다시 오면(W-7)

코드는 바꾸지 않는다. 순서: Phase 0 대조 다시 → `graph_ingest --curation-dir $W` → `graph_build` → `graph_e2e_check.py`. 대조에서 새 칸 · 새 값이 나오면 escalation 한다.

## Done Criteria

- [ ] Phase 5 검증 전부 통과(ruff · 전체 테스트 · E2E PASS) — 출력 원문을 report 에 붙인다
- [ ] 실DB 에 v2 발행본(`counts.schema="v2"`)이 있고 v1 발행본 행은 그대로다
- [ ] alembic 0 · graph 밖 변경 0(`git -C .. status --short` 를 report 에)
- [ ] Phase 0 대조표 · escalation 이력
- [ ] SPEC-004 와 다르게 구현한 곳 0 — 있으면 목록과 근거(`ask` 로 합의한 것만)

## Rollback

배포 · 커밋 없음. Phase 0 체크포인트로 코드를 되돌리고 `graph_build --force` 로 v1 을 새 번호로 재발행한다. DB 는 지우지 않는다.

## Open Issues

- SPEC-004 §7 OQ-G01~G16 은 임시값으로 진행한다. 임시값으로 안 되는 경우를 만나면 고치지 말고 `ask` 한다
- OQ-G06(기본 응답 = 승인 · 자동만)은 코디 기본값이고 사용자 확인 대기다. 뒤집혀도 `include_unconfirmed` 의 기본값 하나만 바꾸면 된다

## Related

- SPEC-004 0.2.0 · SPEC-001 · WORK-001 · DEC-001~003 · `review-spec-004-report.md` · `_RESUME.md` §2 2026-10-27 행
