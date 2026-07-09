---
type: work
id: AXKG-WORK-004
title: "WP3: 승인 게이트 — 분류·문서화·Apply Executor"
status: done
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
progress: 100
created_at: 2026-07-07
updated_at: 2026-07-08
tags:
  - product/ax-knowledge-graph
  - doc/work
  - status/done
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

- **Status**: DONE (PLAN-006-T-001, 라이브 e2e 통과)
- **작업**:
  - [x] gates 서비스/레포 + `/gates/{id}/*` 공통 액션, 버전·feedback 규칙
  - [x] ② context builder + classification.v1 저장 + 승인 → destination/문서화 게이트 생성(archive 분기)
- **검증**: [x] SPEC-001 U-3·S-1·S-2, SPEC-002 상태기계·버전 AC (`test_classification_gate.py` 21, admin 게이트 155 passed) + 라이브 e2e 전구간(분류 트리거→AI 실행→review_pending→승인→destination 확정, archive/문서화 컨테이너 분기, open-kknaks Session Rule 저장)

### Phase 2 — 문서화 게이트 (초안+파생지식)

- **Status**: DONE (PLAN-006-T-004, 라이브 e2e 통과)
- **작업**:
  - [x] ③ context builder: 연결 후보 2단(WP2 retriever+index 스냅샷) + destination→템플릿 매핑(resource→reference/area→permanent/project→project_baseline) + 3자 조립
  - [x] documentation.v1 payload(draft/derived/apply_plan **제안(validation_status=pending)**) + 조회 뷰(`/documentation-gates`·`/drafts/{v}/markdown`) + regenerate/retry gate_kind 인지 라우팅
- **검증**: [x] SPEC-004 AC(초안 frontmatter+본문 / 파생지식 한 덩어리·개별승인 없음 / 피드백→v2 통째 재생성 / 실패→retry), 연결 후보 2단 컨텍스트 항상 주입 (`test_documentation_gate.py` 12, admin 게이트 206 passed) + 라이브 e2e(분류 승인→문서화 게이트 generating→reference 초안+파생지식 3+apply_plan pending→review_pending, source summarized 유지). wikilink resolve는 확정 문서 유입(Phase 3) 후 재검증

### Phase 3 — Apply Executor

- **Status**: DONE (PLAN-006-T-006, 라이브 e2e 통과 — 전 과정 완결)
- **작업**:
  - [x] approve 시점 검증(단일 게이트): path allowlist/stale/`BROKEN_WIKILINK`/`UP_WITHOUT_BODY_LINK`/`DUPLICATE_STEM` 거부 (plan 내 신규 stem은 유효 target 인정)
  - [x] file_actions 실행(executor=유일 writer, MarkdownRoot write_new/overwrite) + **db_actions executor derive**(main create_document/파생/source documented/gate) + 증분 rebuild(WP2 rebuild_document) + `summarized→documented` 전이 (멱등, 재승인 `GATE_ALREADY_APPROVED`)
- **검증**: [x] SPEC-004 Case/Apply Matrix, 거부 케이스 (`test_apply_executor.py` 9, admin 게이트 215 passed) + 라이브 e2e(PKM 문서화 승인→`/workspace/resources/...md` 확정 write+documents/edges 인덱스+source documented+그래프 노드 1)

> **Phase 3 Open Issue(비차단, Phase 2 프롬프트)**: 라이브에서 문서화 AI가 파생지식 `draft_markdown`을 빈값으로 산출 → executor가 빈 파일 스킵(문서 1개=main만 생성). 메인 reference note는 정상. 파생지식 본문 채우기는 documentation_gate 프롬프트/output_schema 튜닝 소관(후속). executor는 빈 create를 만들지 않음(정상 방어).

### Phase 4 — 재분류 + FE 승인 화면

- **Status**: DONE (BE PLAN-006-T-009 + FE PLAN-006-T-010)
- **작업**:
  - [x] "이 destination이 아님" 재오픈 흐름 (S-3 5단계): **BE done**(T-009 — 공통 `/gates/{id}/feedback` 확장 `not_this_destination`+이유 필수, 원자적 재오픈 5전이: 분류 approved→regenerating+approved_revision 해제·superseded 불변·source destination 리셋·문서화 cancelled·v2 regenerate 큐잉, 재승인→문서화 재생성=Phase2 재사용. `test_reclassification_reopen.py` 8, admin 게이트 223 passed) + **FE done**(T-010 — 문서화 게이트 피드백 모달 "이 destination이 아님" 보조옵션+이유 필수→requestReclassification, 성공→GET gates 재조회, 문서화 "재분류 요청됨"·분류 재검토 복귀, tsc+build 통과).
  - [x] FE 승인 화면: **분류 게이트**(인박스 원페이지 2컬럼 통합 + ② 실배선 + 파생 라벨, PLAN-006-T-003) + **문서화 게이트 ③ 실렌더**(초안 전문 접기/펴기+파생지식 목록+apply plan preview+[피드백]/[승인]→documented) + **완료 탭**(documented 가시화) + 피드백 모달 공통화 (tsc+build 통과, PLAN-006-T-007)
- **검증**: [x] URL→요약→분류→문서화→documented 전 과정 라이브 e2e 완결(브라우저 가시화: 문서함/승인/완료 3탭 + ②③ 게이트 + 그래프 노드) + 재분류 재오픈 FE(tsc+build, `/` 200)

> **Phase 4 노트**: FE 승인 화면 = 분류 게이트 FE(T-003) + 문서화 게이트 FE(T-007) + 재분류 재오픈 FE(T-010) 전부 done. 별도 `/approval` 라우트 은퇴, Source Inbox 원페이지 스택 통합("문서함" 네이밍 + inbox/승인/완료 3탭). 재분류 재오픈 = BE(T-009)+FE(T-010) done.

## Pre-deploy Check

- [x] 생성 문서 preview 없이 자동 저장하지 않음 (문서화 게이트 승인 전 초안 preview, apply는 approve 결과로만)
- [x] executor가 allowlist 밖 경로를 거부 (`PATH_NOT_ALLOWED`, `test_reject_path_escape`)
- [x] 깨진 wikilink가 확정 문서에 못 들어감 (`BROKEN_WIKILINK` 생성 경로 거부, `test_reject_broken_wikilink`)

## Rollback

- 작업 레포 커밋 단위 revert. 적용된 Markdown은 git으로 revert.

## Done Criteria

- [x] 모든 Phase DONE/SUPERSEDED (Phase 1·2·3·4 done — 전 과정 라이브 완결)
- [x] SPEC-001/002/004 AC + SPEC-011 ②③ AC 반영 (분류=SPEC-001/002, 문서화 초안=SPEC-004/011③, apply=SPEC-004 Apply Matrix; 재분류 재오픈 S-3만 Phase 4)
- [x] product `log.md`·`30-work/README.md` 갱신 (PLAN-006-T-005)

## Open Issues

- **FE Phase 4 전부 done**: 분류 게이트 FE(T-003)·문서화 게이트 FE(T-007)·재분류 재오픈 FE(T-010).
- **RECLASSIFICATION_NOT_ALLOWED 에러코드(미해소 OQ)**: 재분류 거부(대상이 문서화 게이트 아님 / 분류 미승인)를 표면화하는 코드가 SPEC-002/004 Case Matrix에 없어 워커가 임의 삭제 않고 `RECLASSIFICATION_NOT_ALLOWED`(409) 도입(BE+FE 코드에 존재). **spec Case Matrix 정식 등재 여부는 사용자/curator 결정 필요**(동작 무관, 문서 정합만). 재분류 응답=문서화 게이트(cancelled) 반환·이유는 분류 게이트 기록 = 워커 판단(FE UX 확정 시 조정 가능).
- **파생 라벨 doc_***: FE는 classify_*/doc_* 6종 한국어 매핑을 넣었으나 BE `derive_inbox_label`은 현재 classify_*만 방출(doc_*는 Phase 2 배선 시 자동 반영) — PLAN-006-T-003.
- **원본 메타 패널**: 기존 source-detail의 원본 URL/Slack/raw text 상세 그리드는 시안 승인 컬럼에 없어 스택에서 제외(URL만 요약·collection_failed 카드에 유지). raw_text/Slack 상세 뷰 복원 필요 시 admin 판단 후 별도 태스크 — PLAN-006-T-003.
