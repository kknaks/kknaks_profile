---
type: work
id: KDEV-WORK-007
title: "enforcement ON — L1~L4 ERROR + 부팅 fail-fast + pre-commit (kill-switch)"
status: done
product: kknaks-dev
work_type: enforcement
owner: "profile-be"
roles:
  pm: ""
  design: ""
  fe: ""
  be: "profile-be"
  qa: ""
  ops: ""
progress: 100
created_at: 2026-06-30
updated_at: 2026-06-30
tags:
  - product/kknaks-dev
  - doc/work
  - status/done
links:
  baselines:
    - "[[baseline-001-repo-knowledge-graph|KDEV-BL-001]]"
  decisions: []
  specs:
    - "[[spec-004-graph-validation|KDEV-SPEC-004]]"
  works:
    - "[[work-005-migrate-notes|KDEV-WORK-005]]"
  releases: []
  related: []
---

# enforcement ON — L1~L4 ERROR + 부팅 fail-fast + pre-commit (kill-switch)

report-only 검증기를 **enforcement**로 전환한다(D-016). ERROR(L1~L4) 위반 시 부팅 fail-fast + pre-commit 차단. **단일 enforcement 지점 = `load_persona`** (boot·pre-commit·reload 세 caller 모두 이걸 호출). `GRAPH_ENFORCE` env kill-switch(기본 ON, =0이면 우회). 현재 ERROR 합계 0(L2 해소 완료)이라 켜도 정상 부팅.

> 비목표: 시각화(WORK-008/009), 데이터 정제, /posts 배선. 신규 검증 규칙 추가 안 함(기존 L1~L6 그대로, 차단만 켬).

## Meta

- Baseline: [[baseline-001-repo-knowledge-graph|KDEV-BL-001]]
- Covers spec: [[spec-004-graph-validation|KDEV-SPEC-004]] (§7 enforcement OPEN 해소)
- Depends on work: [[work-005-migrate-notes|KDEV-WORK-005]] + L2 해소(6f823e4, ERROR=0 프리req)
- Follow-up work: WORK-008(/graph 시각화)
- External dependency: 없음

## Work Summary

| Field | Value |
|---|---|
| Type | enforcement |
| Owner | profile-be |
| Status | done |
| Progress | 100% |
| Branch/PR | feat/knowledge-graph · 커밋 `cd4e453` |
| Blocker | - |
| Next | WORK-008 전역 그래프 /graph |

## Role Assignment

| Role | Assignee | Responsibility | Status |
|---|---|---|---|
| BE | profile-be | enforce 함수 + caller 의미(boot raise/reload catch) + 테스트 + pre-commit 확인 | done |
| QA | admin | 메커니즘 게이트 재현(주입→raise, kill-switch, L5-only, pre-commit) + pytest | done |

## 핵심 설계 (advisor 교정 반영)

1. **단일 enforce 지점 = `load_persona`**: boot(main.py:35)·pre-commit 훅·runtime reload(admin/reload.py) 세 caller가 전부 load_persona 호출 → 한 곳에서 enforce.
2. **caller 의미가 다름 (★최중요)**:
   - **boot**(lifespan→load_all): raise **propagate** → fail-fast(서버 안 뜸). 의도된 동작.
   - **runtime reload**(content_enrich webhook 등): raise를 **caller가 catch** → reload 거부, **기존 `_data` 유지하며 계속 서빙**(webhook이 prod 죽이면 안 됨). `_data = load_persona(...)`는 raise 시 _data 미재할당이라 구 데이터 자동 생존 — reload caller가 swallow+로그/500.
3. **`level=="ERROR"`만 차단**: L5=156은 WARN → 절대 boot 막으면 안 됨. `[v for v in violations if v["level"]=="ERROR"]` + `_graph_error`(빌드 예외)만 raise.
4. **`GraphEnforcementError(PersonaError)` 서브클래스**: 기존 pre-commit `except PersonaError`가 공짜로 catch(메시지 깔끔). ⚠ **boot 경로에서 PersonaError를 swallow하고 계속하는 코드 없는지 grep**(있으면 fail-fast 무력화).
5. **kill-switch**: `GRAPH_ENFORCE` env(기본 `"1"`=enforce). `"0"`이면 enforce skip(비상 부팅·테스트). 

## Code Surface

| 경로 | 동작 |
|---|---|
| `app/back/core/graph.py` (또는 persona_loader) | `GraphEnforcementError(PersonaError)` + `_enforce_graph(data)`: `GRAPH_ENFORCE!="0"` && (ERROR-level 위반 or `_graph_error`) → raise |
| `app/back/service/persona_loader.py:160~` | 그래프 try/except 뒤에 `_enforce_graph(data)` 호출(report 산출은 유지, 그 다음 enforce) |
| `app/back/main.py` (lifespan/load_all/reload) | boot=propagate. **runtime reload caller가 GraphEnforcementError catch→reload 거부·구 데이터 유지** |
| `app/back/api/admin/reload.py` | reload 엔드포인트가 enforce 실패를 catch→500/로그, 워커 크래시 금지 |
| `app/back/tests/conftest.py` | `GRAPH_ENFORCE=0` 전역 기본(266 테스트 안정) — 실-persona load 테스트도 enforce off |
| `app/back/tests/test_graph.py`/`test_loader.py` | 메커니즘 테스트(주입→raise / kill-switch / L5-only / 회귀) |
| `.git/hooks/pre-commit` + `app/scripts/install_hooks.sh` | 이미 load_persona 호출 → enforce 자동. 메시지 확인, 필요 시 install_hooks 갱신 |

- **CI**: deploy.yml은 push→docker `up --build back`(PR 게이트 없음, solo 미push). **신규 PR 워크플로 안 만든다**(아무도 트리거 안 함, WORK-006 교훈). **docker up이 곧 deploy 게이트** — 나쁜 데이터→back 부팅 fail-fast→배포 가시적 실패. D-016 3지점 = pre-commit(커밋) + boot-fail-fast(부팅=deploy 게이트). PR merge gate는 PR 플로 생기면 별도.
- 무변경: API 스키마, FE.

## Execution

### Phase 1 — enforce 함수 + 단일 지점 배선
- **Status**: DONE
- `GraphEnforcementError(PersonaError)`(persona_loader.py:83) + `_enforce_graph`(env kill-switch + ERROR-only + _graph_error, L92~). load_persona 그래프 산출 뒤 호출(persona_loader.py:211).

### Phase 2 — caller 의미 (boot propagate / reload catch) ★
- **Status**: DONE
- boot(lifespan→load_all)=propagate(fail-fast), runtime reload 4 caller=`reload_data()` 래퍼로 catch(구 _data 유지·서빙 지속, webhook 503). boot 경로 PersonaError swallow 없음 확인.

### Phase 3 — 테스트 (메커니즘 증명)
- **Status**: DONE
- conftest GRAPH_ENFORCE=0 전역. 메커니즘 테스트 실증(주입 ERROR→raise / kill-switch→로드 / L5-only→로드 / reload 실패→구 데이터 생존). **278 passed**. GraphEnforcementError⊂PersonaError 확인.

### Phase 4 — pre-commit 확인
- **Status**: DONE
- pre-commit 훅이 load_persona로 enforce(PersonaError catch), 트리거 `persona|reference|products` 확장. 주입 ERROR 커밋 차단 실증.

## Pre-deploy Check

- [x] 현재 실 데이터(ERROR=0, nodes 308, L5=156)로 enforce ON 부팅 성공
- [x] kill-switch GRAPH_ENFORCE=0 동작
- [x] runtime reload는 enforce 실패해도 prod 안 죽음(구 데이터 유지·서빙 지속)
- [x] L5=156 WARN은 boot 안 막음

## Rollback

- enforce 함수 호출 제거 or `GRAPH_ENFORCE=0` 환경변수로 즉시 비활성(kill-switch). 단일 커밋 revert.

## Done Criteria (메커니즘 게이트 — 데이터 측정 아님)

- [x] **boot 성공**: 실 데이터(ERROR=0, nodes 308, L5=156) + enforce ON
- [x] **주입 ERROR → load_persona raise** (enforce ON) — fail-fast 실증
- [x] **주입 ERROR + GRAPH_ENFORCE=0 → 로드 성공** — kill-switch 실증
- [x] **L5 orphan만 주입 → 로드 성공** (enforce ON) — WARN은 안 막음 실증
- [x] **runtime reload가 enforce 실패 시 구 데이터 유지·서빙 지속** (워커 크래시 X)
- [x] **pre-commit이 주입 ERROR 커밋 차단**
- [x] pytest 278 green (테스트는 enforce off)
- [x] 30-work/README·log 갱신 + SPEC-004 §7 enforcement OPEN 해소(이 task)

## Open Issues

- PR merge-gate(D-016 CI)는 현재 PR 플로 없어 보류 — boot-fail-fast-at-deploy가 deploy 게이트. PR 플로 생기면 lightweight 워크플로 별도.

## Related

- Spec: [[spec-004-graph-validation|KDEV-SPEC-004]]
- Work: [[work-005-migrate-notes|KDEV-WORK-005]]
