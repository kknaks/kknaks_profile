# [backend] WORK-003 구현 — 허브 골드 그래프 · 도구 9 · 원장 도구 3 · E2E

너는 맥락이 없다. 역할 `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/roles/procedure-hub/backend/role.md`(rules · workflow · skills · tools 같이). 코드 워크트리 `/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-recommend`(브랜치 `kknaksss/phub-recommend` · **로컬 전용 · push 금지 · PR 금지**).
정본: `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/SPEC-005.md` · `WORK-003.md`(검수 v2 PASS · 보강 raw-mcp · 열린 것 O-1~O-4 결정됨). 입력 `$W` = `/Users/kknaks/orca/workspaces/kknaks_profile/프로시져허브메달리온/orchestration/work/phub-recommend/` · 원장 = `/Users/kknaks/orca/workspaces/PROCEDURE-HUB/phub-stg-2026-10-26/`.

## 하는 일
WORK-003 Phase **0 → 1 → 2 → 3 → 3b → 4** 를 순서대로 · Phase 마다 완료 조건 · 그 Phase 시험만 · 전체 시험 · ruff · 품질 측정 전체는 Phase 4 끝에 한 번.
- Phase 0 기준점 커밋(v1 미커밋 파일 — 로컬 커밋만)
- 입력은 $W 파일을 **읽기만**(실버 · 시맨틱 · 품질 측정 파일 수정 금지 — 측정 스크립트를 골드 도구 위로 돌리는 어댑터는 코드 레포 쪽에)
- Phase 4 완료 조건: 품질 측정 목표 6/6(CC 슬롯 경로) 유지 + Q106 · Q108 · Q109 · Q110 맞음(의료진 5문항 제외) · 로컬 서버 `127.0.0.1:18005` 실물 호출(REST · 골드 MCP · 원장 MCP 각각 tools/list · 호출) · 속도 측정 보고(p50 · p95 — 기준은 사용자가 나중에)

## 지킬 것
- SPEC 과 다르게 해야 하면 **고치기 전에** 코디에게 `ask`(decision_gate) · 막히면 `escalation` · Phase 끝마다 `heartbeat`(phase 이름)
- 사용자 포트 3700 · 3800 · 8700 · 8800 · 54329 · 기존 `procedure-*` 컨테이너 건드리지 말 것 · DB 55434(graph-local compose) 만
- env 는 `envs/.env.gold`(git 제외 · 예시만 커밋 · 비밀값 없음) · 키 · 실명 금지 · LLM 호출 없음
- 서버는 E2E 동안만 띄우고 끝나면 내림(포트 · 프로세스 정리)

## 완료 보고 — 문구 변경 금지
```bash
orca orchestration send --to term_15f07066-c2d1-4037-a5d1-d09830057ddb --from term_5aa0d8e8-74db-4b9f-9be6-467f20566ac3 --type worker_done --task-id <taskId> --dispatch-id <dispatchId> --subject "backend 완료: WORK-003 허브 골드" --body "Phase 0~4 · 품질 N/6 · Q106 · Q108~110 N/4 · 실물 호출 REST · gold-mcp · raw-mcp · p50/p95 N/N ms · 시험 N passed · 커밋 N(로컬)"
orca terminal send --terminal term_15f07066-c2d1-4037-a5d1-d09830057ddb --text "[worker_done] backend 완료 — WORK-003 허브 골드. 상세는 인박스." --enter
```
