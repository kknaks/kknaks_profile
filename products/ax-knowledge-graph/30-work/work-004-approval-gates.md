---
type: work
id: AXKG-WORK-004
title: "WP3: 승인 게이트 — 분류·문서화·Apply Executor"
status: todo
product: ax-knowledge-graph
work_type: new-feature
owner: kknaks
roles:
  pm: kknaks
  design: kknaks
  fe: kknaks
  be: kknaks
  qa: kknaks
  ops: kknaks
progress: 0
created_at: 2026-07-07
updated_at: 2026-07-07
tags:
  - product/ax-knowledge-graph
  - doc/work
  - status/todo
links:
  baselines:
    - "[[baseline-001-ax-knowledge-graph-from-curated-sources|AXKG-BL-001]]"
  decisions:
    - "[[decision-001-para-pipeline-and-approval-gates|AXKG-DEC-001]]"
    - "[[decision-005-ai-execution-assembly-and-link-context|AXKG-DEC-005]]"
  specs:
    - "[[spec-001-curation-pipeline|AXKG-SPEC-001]]"
    - "[[spec-002-approval-gate-feedback-loop|AXKG-SPEC-002]]"
    - "[[spec-004-documentation-approval-gate|AXKG-SPEC-004]]"
    - "[[spec-011-ai-execution-pipeline|AXKG-SPEC-011]]"
  works:
    - "[[work-002-source-intake|AXKG-WORK-002]]"
    - "[[work-003-document-graph-core|AXKG-WORK-003]]"
  releases: []
  related: []
---

# WP3: 승인 게이트 — 분류·문서화·Apply Executor

`summarized` source를 분류 게이트(②)에서 PARA 승인하고, 문서화 게이트(③)에서 초안+연결+파생지식을 통째 승인해 영구 문서를 만드는 제품 핵심 흐름. **WP1(요약된 source)과 WP2(retriever·index·엣지 rebuild)를 전제**한다.

## Meta

- Baseline: AXKG-BL-001
- Covers spec: AXKG-SPEC-001(파이프라인), AXKG-SPEC-002(게이트 공통 규칙), AXKG-SPEC-004(문서화 게이트), AXKG-SPEC-011②③(분류·문서초안 스테이지)
- Depends on work: AXKG-WORK-002(WP1), AXKG-WORK-003(WP2)
- Parallel work: 없음 (양쪽 선행 완료 후)
- Follow-up work: 없음 (MVP 핵심 완성)
- External dependency: 없음

## Scope

포함:

- 게이트 공통 (SPEC-002): approval_gates/revisions/feedback 서비스·레포, `/gates/{gate_id}/feedback·regenerate·retry·approve`, 버전 규칙(v1 read-only, revision 불변, superseded), resume session 사용(`options.resume`)
- 분류 스테이지(②): `classification_gate` context builder(요약 payload + `context/para-classification.md`, **그래프 컨텍스트 없음**), classification.v1 payload 저장, 승인 → destination 확정 + 문서화 게이트 자동 생성(archive는 종료→`archived`)
- 문서화 스테이지(③): `documentation_gate` context builder — **연결 후보 2단 컨텍스트**(retriever top-N + index 스냅샷, WP2) + destination→템플릿 key 매핑 + 활성 템플릿/프롬프트 조립, documentation.v1(draft+derived_suggestions+apply_plan 제안) 저장
- Apply Executor (SPEC-004): apply_plan 검증(pre-validation at revision 생성 + approve 시 재검증) — path allowlist, stale revision, 깨진 wikilink 거부 → file_actions(create/patch/frontmatter) 실행 → db_actions → 증분 엣지 rebuild → `documented`
- 재분류 재오픈 (SPEC-002/004 S-3): 분류 게이트 approved→regenerating, approved revision superseded, destination 리셋, 문서화 게이트 cancelled
- 파이프라인 파생 상태 라벨 (SPEC-001 매핑표) — Inbox 큐 분류
- FE: 승인 화면(`/approval`) — 중앙 세로 스택(①요약·분류 카드 → ②분류 게이트 → ③문서화 게이트 인라인), 피드백 모달, 초안 전문 접기/펴기, 파생지식 읽기 목록, apply plan preview, 버전 badge. **기준: `21-html/page-approval.html` — 레이아웃·한국어 카피 모두 시안을 따른다**

제외:

- Graph Chat (WP4), 설정 UI (WP5)
- 멀티 reviewer

## Code Surface

- Repo / module: ax-graph
- 만질 파일 후보:

| 경로 | 설명 |
|---|---|
| `apps/api/axkg/api/routes/approval_gates.py` · `documentation_gates.py` · `sources.py` | 게이트 액션(공통)·조회 뷰·classification-gates 트리거 |
| `apps/api/axkg/services/gates.py` + `repositories/gates.py` · `revisions` · `feedback` | 게이트 lifecycle·버전·재오픈 |
| `apps/api/axkg/services/ai/` | ②③ context builder 등록, destination→템플릿 매핑, resume 배선 |
| `apps/api/axkg/workers/apply_executor.py` + `services/documents.py` | apply_plan 검증·실행(유일한 Markdown writer) |
| `apps/web/app/approval/` | 승인 화면 |

## Domain / Schema

| Entity | 이 WP에서 |
|---|---|
| `approval_gates` / `approval_gate_revisions` / `gate_feedback` | 전체 구현 |
| `drafts` / `apply_plans` | 전체 구현 |
| `ai_tasks` | ②③ task_type 실사용 |
| `documents` / `document_edges` | 쓰기 경로(executor 경유) 연결 |

- 상태 / invariant: AI는 DB/Markdown을 직접 쓰지 않는다 — executor만. 승인 revision 불변, 재오픈은 컨테이너 상태만.
- Migration 필요 여부: 없음(WP0 완료).
- SPEC에 환류: 없음 예상.

## Execution

### Phase 1 — 게이트 공통 + 분류 게이트

- **Status**: TODO
- **작업**:
  - [ ] gates 서비스/레포 + `/gates/{id}/*` 공통 액션, 버전·feedback 규칙
  - [ ] ② context builder + classification.v1 저장 + 승인 → destination/문서화 게이트 생성(archive 분기)
- **검증**: [ ] SPEC-001 U-3·S-1·S-2, SPEC-002 상태기계·버전 AC

### Phase 2 — 문서화 게이트 (초안+파생지식)

- **Status**: TODO
- **작업**:
  - [ ] ③ context builder: 연결 후보 2단 + destination→템플릿 매핑 + 3자 조립
  - [ ] documentation.v1 payload(draft/derived/apply_plan 제안) + 조회 뷰(`/documentation-gates*`)
- **검증**: [ ] 생성된 wikilink 전부 index 스냅샷 resolve (SPEC-011 AC), 파생지식 한 덩어리 규칙

### Phase 3 — Apply Executor

- **Status**: TODO
- **작업**:
  - [ ] pre-validation(revision 생성 시) + approve 재검증 (path/stale/broken link 거부)
  - [ ] file_actions 실행 + db_actions + 증분 rebuild + documented 전이 (멱등)
- **검증**: [ ] SPEC-004 Case Matrix·Apply Matrix, 거부 케이스 전부

### Phase 4 — 재분류 + FE 승인 화면

- **Status**: TODO
- **작업**:
  - [ ] "이 destination이 아님" 재오픈 흐름 (S-3 5단계)
  - [ ] FE 중앙 스택 + 피드백 모달 + preview/diff + 파생지식 목록
- **검증**: [ ] URL→요약→분류→문서화→documented 전 과정 라이브 e2e

## Pre-deploy Check

- [ ] 생성 문서 preview 없이 자동 저장하지 않음
- [ ] executor가 allowlist 밖 경로를 거부
- [ ] 깨진 wikilink가 확정 문서에 못 들어감

## Rollback

- 작업 레포 커밋 단위 revert. 적용된 Markdown은 git으로 revert.

## Done Criteria

- [ ] 모든 Phase DONE/SUPERSEDED
- [ ] SPEC-001/002/004 AC + SPEC-011 ②③ AC 반영
- [ ] product `log.md`·`30-work/README.md` 갱신

## Open Issues

- 없음 (선행 WP 완료 전 착수 금지만 유의).
