---
type: work
id: WORK-003
title: "허브 골드 구현 — 적재 · 골드 빌드 · 도구 9(REST · MCP) · 골드 E2E"
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
created_at: 2026-10-30
updated_at: 2026-10-30
replaces:
  - "WORK-002"
tags:
  - product/procedure-hub
  - feature/phub-recommend
  - doc/work
  - status/todo
links:
  spec: "orchestration/work/phub-recommend/SPEC-005.md"
  decisions:
    - "orchestration/work/phub-recommend/_RESUME.md §2"
---

# 허브 골드 구현 — 적재 → 골드 빌드 → 도구 → E2E

> 검수 반영 2026-10-30(F-1 ~ F-5 · W-1 ~ W-9) — `review-spec005-report.md`
> 보강 2026-10-30(raw-mcp · O-1~O-4) — SPEC-005 §5-12 · §7

SPEC-005 0.1.0 을 구현한다. 계약은 SPEC-005 가 갖고, 이 문서는 순서 · 파일 · 완료 조건 · 검증 명령만 갖는다. 둘이 다르면 SPEC 을 따른다.

**비목표**: 실버 · 시맨틱 · 브론즈 수정 · 연결 층(병원 상품 · KOS) · 상담 앱 · Jev · Claude · 배포 · push. v1 그래프와 대조하지 않는다(뼈대만 재사용).

## Meta

- Covers spec: SPEC-005 0.1.0 전부
- 입력 `$W` = `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend` — 파일 12(SPEC-005 §2-1)는 **읽기만** — `$W` 에서 고치는 파일은 `quality-eval.py` 하나(골드 모드 추가 · Phase 4)
- 코드: `/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-recommend`(브랜치 `kknaksss/phub-recommend` · 로컬 전용 · **push 금지**). 명령은 전부 `backend/` 에서
- 로컬: DB `phub-graph-postgres`(55434) · 앱 18005
  - **사용자 포트 · 프로세스는 건드리지 않는다**(3700 · 3800 · 8700 · 8800 · 54329 · `procedure-*` 컨테이너)
  - 18005 에 v1 그래프 앱이 떠 있으면 그 프로세스가 이 작업의 것인지 확인하고 내린다 — 아니면 escalation
- 원장 입력(평가용 원장 도구 · Phase 3b) = `/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-stg-2026-10-26/`(파일 21) — **읽기만** · 경로는 env `PHUB_RAW_DIR`
- 외부 호출 없음(stg · 식약처 · 모델 · 인터넷)
- 실명 · 키를 코드 · 문서 · 시험에 넣지 않는다. 시험 기대값은 실물 빌드에서 뽑는다(가상 문장 없음)

## Work Summary

| Field | Value |
|---|---|
| Goal | 실버 · 시맨틱 파일 → 골드 그래프(DB 발행본) → 메모리 그래프 → 도구 9 를 REST · MCP 로 · 품질 측정을 골드 도구 위에서 6/6 + Q106 · Q108 · Q109 · Q110 맞음 |
| Non-goal | 위 비목표 · 실버 빈 곳 고치기(보강 후보 목록만) |
| 완료 판정 | §Done Criteria 전부 |

## Scope · Code Surface

| 파일 | 새/고침 | SPEC-005 |
|---|---|---|
| `app/graph_main.py` | 고침 — 같은 진입점 · 같은 lifespan 꼴로 골드 컨테이너 · 골드 라우터 · 골드 MCP 로 배선(v1 graph 모듈 import 제거) · 시작 때 발행본 메모리 적재 · 원장 MCP 별도 마운트(Phase 3b — lifespan 에서 두 MCP session_manager 를 같이 돌림) | §1-3 · §4-1 · §5-12 |
| `app/modules/raw/`(새) — `config.py` · `manifest.py`(해시 가드) · `store.py`(원장 메모리 적재) · `paths.py`(경로 문법) · `tools.py`(raw_list · raw_get · raw_search 코어) · `mcp_server.py` | 새 — 골드 · 시맨틱 import 금지 | §5-12 |
| `backend/raw-manifest.json` · `scripts/raw_manifest.py` | 새 — 원장 21 파일 이름 · 바이트 · sha16(비밀값 없음) | §5-12 |
| `app/modules/gold/`(새) — `config.py` · `container.py` · `inputs.py`(입력 계약 · 해시 가드) · `ids.py`(G1) · `build.py`(G2~G18 · §3-2 순서) · `pairs.py`(§3-3) · `facts.py`(§4-3) · `guards.py`(§3-5) · `repository.py` · `memory.py`(메모리 그래프 · 사전 색인) · `resolve.py`(resolve_rules) · `tools.py`(도구 코어 9 · 순수 함수) · `mcp_server.py` | 새 | §2~§5 |
| `app/model/gold.py` · `alembic/versions/<새 리비전>_gold_schema.py` | 새 | §4-2 |
| `app/router/gold.py` · `app/schema/gold.py` · `app/swagger_docs/gold.py` | 새 | §5 |
| `envs/gold.env.example` | 새(비밀값 없음 · `.env.gold` 는 git 제외 확인) · `PHUB_RAW_DIR` · `RAW_GET_MAX_BYTES` · `GOLD_NEIGHBORS_MAX_DEPTH=2` · `GOLD_NEIGHBORS_MAX_LIMIT=50` | §4-1 · §5-9 · §5-12 |
| `scripts/gold_ingest.py` · `scripts/gold_build.py` · `scripts/gold_publish.py` · `scripts/gold_export.py` · `scripts/gold_speed.py` | 새 | §4-1 · §6 |
| `tests/test_gold_*.py` · `tests/fixtures/gold/` | 새 | §6-4 |
| `docs/gold-local.md` | 새 — 실행 순서 · 포트 · env | — |
| `$W/quality-eval.py` | 고침 — `--gold <base_url>` 모드만 더함(실버 판 경로 · 문항 · 채점 식 그대로) | §6-1 |

손대지 않는 것: `$W` 의 실버 · 시맨틱 · 결정 파일 · `quality-eval-set.json` · 기존 앱(`app.main`) · v1 graph 모듈 파일(import 만 끊음 · 지우지 않음) · `app/core/*` · 사용자 env 파일.

## Execution

- 각 Phase 끝에는 **그 Phase 시험만** 돌린다. 전체 시험 · ruff · 품질 측정 전체는 Phase 4 끝에 한 번
- 시험 env: `DATABASE_URL=sqlite+aiosqlite:///:memory:`
- Phase 마다 끝나면 코디에게 `heartbeat`(phase 이름) · 막히면 `escalation`. SPEC 과 다르게 해야 하는 곳은 고치기 전에 `ask`

### Phase 0 — 기준점 · 입력 대조

1. 기준점 커밋(로컬 · push 금지): 지금 미커밋 v1 그래프 파일(`git status --short` 의 graph 관련)을 「v1 graph 기준점」 한 커밋으로. 사용자 파일 · env 는 넣지 않음(`git status --ignored` 로 확인 후)
2. 입력 대조 스크립트(레포 밖 · `$W` 에 쓰지 않음 · 출력은 코드 레포 `backend/build-out/input-check.json`): SPEC-005 §2-1 해시 11 가드 · §2-2 칸 경로가 실물에 있는지 · 실물 셈(override 624 · 그중 계열 부작용 gap 계열을 덮은 행 72 · by_direction 118 · 자기 쌍 엣지 4 · conditions.resolved product 7 · ledger 3 · 노드 1,071 · 저장 엣지 3,179 · I4 1,379 · 합병증 펼침 285 · 조합 구성 581 · resolved 230 · resolved_pairs 105 · conditions.resolved 241 · 메뉴 라벨 8)
3. escalation 기준: 칸이 없거나 새 값 종류가 생겼거나 해시 가드 실패 → 코디에게 escalation 하고 멈춤. 셈만 다르면 표에 적고 진행

완료 조건: `input-check.json` 이 있고 해시 11/11 같음 · 칸 경로 누락 0 · 기준점 커밋 sha 를 코디에게 알림

### Phase 1 — 적재

- `app/model/gold.py` · alembic 리비전 · `gold_source_snapshot`(SPEC §4-2) — 다른 골드 테이블도 이 리비전에서 같이 만든다
- `scripts/gold_ingest.py --from-dir $W`: 파일 12 를 원문 그대로 · 같은 sha 면 `unchanged` · 없는 파일 = 실패 종료 코드 1
- 시험 `tests/test_gold_ingest.py`: 12 `inserted` → 다시 12 `unchanged` · 하나 바꾸면 그것만 · 없는 파일 실패

검증:
```bash
DATABASE_URL=sqlite+aiosqlite:///:memory: uv run pytest tests/test_gold_ingest.py -q
docker compose -f graph-local.compose.yml up -d
[ -f envs/.env.gold ] || cp envs/gold.env.example envs/.env.gold   # 없을 때만 · 있으면 건드리지 않음
uv run --env-file envs/.env.gold alembic upgrade head
uv run --env-file envs/.env.gold python scripts/gold_ingest.py --from-dir $W   # inserted 12
uv run --env-file envs/.env.gold python scripts/gold_ingest.py --from-dir $W   # unchanged 12
```

완료 조건: 위 명령 출력 원문 · alembic 리비전 id

### Phase 2 — 골드 빌드 · 발행

- §3-2 순서 그대로: 해시 가드 → G1 → 저장 엣지 21 → 펼침(G2 · G4 · G5 · G7 · G9 · G11 · G16 · G17) → 시술 쌍 · 자기 쌍 · 확인 조건 값(§3-3) → 거르기 표시(G8 · G12) → 안전 묶음(G13) → facts(§4-3) → 사전 적재 + 메뉴 라벨(G18 · 기존 mode 그대로 · menu 는 별도 후보) → 가드 → 빌드 해시 → 한 트랜잭션 저장 → 발행
- 가드는 고정 숫자 대신 입력 파일에서 센 값과 대조(SPEC §3-5)
- 보강 후보 `build-out/gold-hub-gaps.json`(SPEC §3-6 첫 3행 포함)
- `scripts/gold_export.py` → `build-out/gold-export.json`(발행본 노드 · 엣지 · facts — Phase 4 M3 · M4 입력)
- 시험 `tests/test_gold_build.py` · `tests/test_gold_guards.py` · `tests/test_gold_pairs.py`:
  - 실물 입력 빌드 → 가드 전부 통과 · 셈 기록
  - 같은 입력 두 번 → 빌드 해시 같음
  - fixture(실물에서 잘라 낸 것 · 일부러 깬 것) → 가드마다 실패를 내는지: 해시 다름 · 맵에 없는 id · 합병증 펼침 셈 다름 · I4 다름 · 단위 쌍 두 값 · 조건 모름 옵션 2개 · 겉 칸 + 옵션 같이
  - §3-3: resolved_pairs 105 쌍은 그 값 · 엣지 하나만 닿는 쌍 · 가장 구체적 엣지 · 방향 뒤집기(first · by_direction)
  - G9: priority 작을수록 먼저(0 < 1 < 2 < 3 < 계열) · override_of 보존 · 계열 부작용 gap 계열(72행)도 통과 · override_of 가 계열 노드에 없으면 실패 · 합병증 안 덮음
  - G15b: 한쪽 방향 None 인 11건 통과 · None 뺀 값이 둘 이상이면 실패
  - 자기 쌍: self_pair 엣지 4 의 resolved
  - 확인 조건: product 키 행은 제품에만 · ledger 키 3(KR8-0212~0214) → `package:P6-03`(`step6 packages[].ledger_id` · O-4 결정) · ledger 키마다 패키지 정확히 1 가드
  - G10: 162 단위 상태 3값

검증:
```bash
DATABASE_URL=sqlite+aiosqlite:///:memory: uv run pytest tests/test_gold_build.py tests/test_gold_guards.py tests/test_gold_pairs.py -q
uv run --env-file envs/.env.gold python scripts/gold_build.py      # published · build_hash 출력
uv run --env-file envs/.env.gold python scripts/gold_build.py      # unchanged(같은 해시)
uv run --env-file envs/.env.gold python scripts/gold_export.py
```

완료 조건: 발행본 1 · 가드 표(기대 · 실제 · 통과) 원문 · 빌드 해시 두 번 같음 · `gold-hub-gaps.json` · `gold-export.json`

### Phase 3 — 도구 9 · REST · MCP

- `tools.py` 도구 코어 9(SPEC §5-2~§5-10) — 순수 함수 · 메모리 그래프만 읽음
- REST 라우터 · MCP 서버는 코어를 부르기만(입력 이름 · 기본값 · 오류 문구 같음) · 헬스
- `graph_main.py` 배선 · 시작 때 발행본 메모리 적재(적재 시간 로그)
- 시험 `tests/test_gold_tools.py` · `tests/test_gold_api.py` · `tests/test_gold_mcp.py`:
  - 도구마다 실물 빌드 값 기대 — 최소: resolve 「턱선 처짐」(낱말 나눔 → 부위 + 고민 전부) · 「처짐/탄력」(candidates P3 · P4-1 mode 「전부」 그대로 + menu_candidates 1) · 「색소/미백」(candidates P5 mode 「하나」 그대로 + menu_candidates 1) · 「쁘띠시술」(menu_candidates) / recommend 이마 주름 · 턱선 처짐(layer 「상위」 포함 · U-1 ②) · cc 슬롯 하나 · site_free(병변 단위) 통과 / procedure_card slim · sections(overview = 환자 설명 가이드 · aftercare = source_text.aftercare) · 안전 동봉 · gap 상태 / check_conditions `id=package:P6-03`(O-4 3행) / 모든 응답에 `claude_contract`(allowed_fact_ids = facts id 전부 · must_show_flags · rule 고정 문장 — O-3) / neighbors depth 3 · limit 51 → 4xx · 50 넘는 이웃 → truncated(O-1) / pair_check by_sub_condition · by_direction · prior 경과 · 같은 id 두 번(자기 쌍) / check_conditions 전역 + 등급 / compare / combos menu(라벨 8 각각) · concern(③ combos · reference 나눔) / neighbors truncated / vocab
  - 안전 동봉: 시술이 나오는 모든 도구 응답에 안전 칸
  - REST ↔ MCP 같은 입력 → 같은 JSON
  - 기본 응답 거르기 · include_* 옵션 · excluded_counts

검증:
```bash
DATABASE_URL=sqlite+aiosqlite:///:memory: uv run pytest tests/test_gold_tools.py tests/test_gold_api.py tests/test_gold_mcp.py -q
uv run --env-file envs/.env.gold uvicorn app.graph_main:app --host 127.0.0.1 --port 18005
curl -s 127.0.0.1:18005/procedure-hub/gold/health
```

완료 조건: 시험 통과 원문 · 서버 기동 로그(발행 빌드 id · 메모리 적재 셈 · 시간) · 헬스 응답

### Phase 3b — 평가용 원장 도구 3(raw-mcp · 골드 아님)

- `scripts/raw_manifest.py --dir $PHUB_RAW_DIR` → `backend/raw-manifest.json`(21행) — 한 번 만들어 커밋(로컬)
- `app/modules/raw/` · 원장 MCP `/procedure-hub/raw-mcp/mcp` 마운트(SPEC §5-12) — 해시 가드 실패면 마운트 안 함 · 헬스에 사유 · 골드 도구는 그대로 뜸
- 시험 `tests/test_raw_tools.py` · `tests/test_raw_mcp.py` · `tests/test_module_boundary.py`:
  - 경계: `app/modules/raw/**` 소스가 `app.modules.gold` 를 import 하지 않음 · `app/modules/gold/**` 가 `app.modules.raw` 를 import 하지 않음(AST import 검사) · raw 가 `$W` 경로 · `semantic` 문자열 경로를 열지 않음
  - manifest: 실물 21/21 통과 · 파일 하나 빠짐 / 해시 다름 / 파일 더 있음 → 마운트 안 함(임시 폴더 복사본으로)
  - raw_list 21 · structure depth · raw_get `taxonomy.problem[3]`(실물 키 `id · category · category_en · subcategories`) · `["키"]` 문법 · 없는 경로 4xx · 한도 넘으면 `truncated` · `next_offset` 로 이어 읽어 원문과 같음
  - raw_search 정규화 = 공백 · 소문자만(대소문자 · 공백 다른 질의 → 같은 hits · 「쳐짐」 ↔ 「처짐」은 다른 결과) · 순서 결정론 · limit · total

검증:
```bash
DATABASE_URL=sqlite+aiosqlite:///:memory: uv run pytest tests/test_raw_tools.py tests/test_raw_mcp.py tests/test_module_boundary.py -q
uv run --env-file envs/.env.gold uvicorn app.graph_main:app --host 127.0.0.1 --port 18005
curl -s 127.0.0.1:18005/procedure-hub/gold/health     # raw manifest 21/21 · 원장 MCP 마운트 여부
```

완료 조건: 시험 통과 원문 · 헬스 응답(manifest 21/21) · 원장 MCP 3 도구 각 1회 실제 호출 기록

### Phase 4 — 골드 E2E · 품질 · 속도 · 전체 검증

1. 백엔드 마지막 커밋(로컬) 뒤 서버 재시작 — 옛 코드가 떠 있는 상태로 재지 않는다
2. 실물 호출(SPEC §6-2): REST 9 · MCP 9 각 1회 이상 · REST ↔ MCP 응답 같음 · 샘플 흐름 3~10단계 기록 → `build-out/gold-e2e.md`
3. 품질(SPEC §6-1): `quality-eval.py` 에 `--gold http://127.0.0.1:18005` 모드를 더해 실행 → `quality-report-gold.json` · `.md`(실버 판 리포트 덮지 않음 · 출력 폴더는 `--out` 으로 코드 레포 `build-out/`) · 두 번 실행 바이트 같음
   - I-01 은 T1 `candidates` 의 concern · site 만 · I-11 은 라벨이면 `menu_candidates` → T7 `menu` · I-09 확인 조건 노드 없는 문항(Q101)은 T3 overview · ops · I-07 자기 쌍(Q091)은 같은 id 두 번(SPEC §6-1)
   - 목표 6/6 · Q106 · Q108 · Q109 · Q110 맞음 · 실버 판에서 맞던 문항이 골드 판에서 틀린 것 0(문항별 대조표)
   - 못 채우면 원인을 문항별로 적고 escalation(데이터 · 규칙을 임의로 바꾸지 않는다)
4. 속도(SPEC §6-3): `scripts/gold_speed.py` → `gold-speed.json` · `.md`(통과 기준 없음 · 보고만 · SPEC §7 O-2)
5. 전체 검증 한 번: ruff · 전체 시험(`uv run pytest -q`) · 기존 앱 시험 회귀 0

완료 조건: 아래 Done Criteria

## Done Criteria

- [ ] Phase 0~3 · 3b 완료 조건 전부(출력 원문을 report 에)
- [ ] `quality-report-gold` 목표 6/6 · Q106 · Q108 · Q109 · Q110 「맞음」 · 계산 밖 5문항(Q042 · Q075 · Q083 · Q084 · Q102) 표시 · 실버 판 대비 회귀 0
- [ ] 로컬 서버 실물 호출 REST 9 · MCP 9 · REST ↔ MCP 같음 · 샘플 흐름 기록 · 원천에 없는 샘플 값이 응답에 없음 · 모든 골드 응답에 `claude_contract`
- [ ] 원장 MCP 3(raw_list · raw_get · raw_search) 실물 호출 · manifest 21/21 · 모듈 경계 시험 통과
- [ ] 속도 리포트(도구별 p50 · p95 · 최대 · 응답 바이트 · 적재 시간)
- [ ] 빌드 해시 · 입력 해시 11 · 발행 빌드 id 를 report 머리에
- [ ] ruff · 전체 시험 통과 · `git status --short` 원문 · push 0
- [ ] SPEC-005 와 다르게 구현한 곳 0 — 있으면 목록 + `ask` 로 합의한 근거
- [ ] 허브 보강 후보 목록 경로

## Rollback

push · 배포 없음. Phase 0 기준점 커밋으로 코드를 되돌린다. 골드 테이블은 별도 리비전이라 `alembic downgrade` 로 그 리비전만 내린다. DB 볼륨 · v1 발행본 행은 지우지 않는다.

## Open Issues

- SPEC-005 §7 열린 것 없음 — O-1 ~ O-4 는 10-30 사용자 결정(O-1 neighbors depth ≤ 2 · limit 50 · O-2 속도 기준은 실측 보고 뒤 · O-3 claude_contract 블록 · O-4 넥큐레이션 3행 → P6-03)
- 실버에 빈 곳(보강 후보)이 보이면 고치지 않고 목록에만

## Related

- SPEC-005 0.1.0 · `_RESUME.md` §2 · `semantic.json` · `gold-research.md` · `quality-report.md` · SPEC-004 · WORK-002(대체됨)

## SPEC 과 다른 점(구현 · 2026-10-30 · backend 워커)

코디 답 10-30 「A · ② 대로 진행」(ask) — 근거와 함께 기록. 전체 표 · 해석 목록은 코드 레포 `backend/build-out/work003-report.md` §SPEC 과 다른 점.

| # | SPEC | 구현 | 근거 |
|---|---|---|---|
| D-1 | T2 입력 concerns 1+ · cc 범위 「같은 원천 문제(P)」 | 선택 입력 `cc_roots?: [P{n}]` — 고민 노드 없는 대분류일 때만(쁘띠시술 P1 · 기타 P14) · 그 밖은 concerns 의 대분류(기존 concern 경로 그대로) · cc 나 site 가 있으면 concerns 0 허용 | CC 이름이 원천 문제 둘에 걸침(아그네스 · 스킨보톡스 · 프락셔널레이저 · 니들RF · 서브시전 · 브이올렛) — 병합 고민으로 P 를 잡으면 Q005 · Q017 틀림 · Q004 · Q031 은 고민 노드 없음 |
| D-2 | G5 rules.product_link 재계산(technique_compat 포함) | 계열(주 · 보조) · 하위 일치 · guards · extra_stored 재계산 · technique_compat 판정만 실버 `product_links[].technique_excluded` 값 · 제품마다 = inherited_candidates 가드 354/354 유지 | 4단계 장비 속성 판정 로직 재구현 안 함 |
| D-3 | `$W/quality-eval.py` 에 `--gold` 모드 | `$W` 는 읽기만 — 코드 레포 어댑터 `scripts/gold_quality_eval.py` 가 exec 해 채점 식을 빌림 · 리포트는 `backend/build-out/quality-report-gold.*` | 브리프 「측정 스크립트를 골드 도구 위로 돌리는 어댑터는 코드 레포 쪽에」 |
