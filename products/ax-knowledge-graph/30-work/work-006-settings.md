---
type: work
id: AXKG-WORK-006
title: "WP5: 설정 — AI Provider·Prompts·Templates"
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
    - "[[decision-003-graph-rag-chat-and-default-claude|AXKG-DEC-003]]"
    - "[[decision-005-ai-execution-assembly-and-link-context|AXKG-DEC-005]]"
  specs:
    - "[[spec-007-ai-provider-settings|AXKG-SPEC-007]]"
    - "[[spec-009-prompt-dynamic-management|AXKG-SPEC-009]]"
    - "[[spec-010-document-template-management|AXKG-SPEC-010]]"
  works:
    - "[[work-001-mvp-pipeline-scaffold|AXKG-WORK-001]]"
  releases: []
  related: []
---

# WP5: 설정 — AI Provider·Prompts·Templates

AI 실행 설정(provider/options/task_overrides)과 프롬프트·템플릿의 편집/버전/롤백 UI·API. WP0이 깐 테이블·seed 위에 관리 표면을 붙인다. WP4와 병렬 가능.

## Meta

- Baseline: AXKG-BL-001
- Covers spec: AXKG-SPEC-007(provider 설정), AXKG-SPEC-009(프롬프트·output_schema), AXKG-SPEC-010(문서 템플릿)
- Depends on work: AXKG-WORK-001(WP0 — 테이블·seed·resolution)
- Parallel work: AXKG-WORK-005(WP4)
- Follow-up work: tool/workflow 설정 노출 (SPEC-009 OQ, 후속 스펙)
- External dependency: 없음

## Scope

포함:

- AI Provider (SPEC-007): `GET/PUT /settings/ai-provider`, `GET /settings/ai-provider/health`, `PUT/DELETE /settings/ai-provider/task-overrides/{task_key}` — 등록된 task definition만 override 허용, 설정 변경 비소급
- Prompts (SPEC-009): 목록/활성 버전 조회, 저장(텍스트+output_schema 한 쌍 → 새 버전+활성), 롤백(포인터 이동), output_schema JSON Schema 검증(`INVALID_OUTPUT_SCHEMA`)
- Templates (SPEC-010): 목록/조회/저장(새 버전+활성)/롤백, key 3종(reference/permanent/project_baseline)
- FE: `/settings` 탭 구성(AI Provider / Prompts / Templates) — 좌측 목록 + 우측 편집기 + 버전 히스토리, 저장/롤백 확인 모달. **기준: `21-html/page-settings.html` — 탭 레이아웃·한국어 카피 모두 시안을 따른다**

제외:

- 프롬프트 A/B·자동 최적화·변수 엔진, project decision/spec 템플릿 확장, 템플릿 개정 마이그레이션(SPEC-010 OQ — 운영 전 결정)

## Code Surface

- Repo / module: ax-graph
- 만질 파일 후보:

| 경로 | 설명 |
|---|---|
| `apps/api/axkg/api/routes/settings.py` · `prompts.py` · `templates.py` | 설정·프롬프트·템플릿 라우터 |
| `apps/api/axkg/services/settings.py` + `repositories/`(settings·prompts·document_templates 확장) | 버전/롤백/override 비즈니스 |
| `apps/web/app/settings/` | 설정 탭 UI |

## Domain / Schema

| Entity | 이 WP에서 |
|---|---|
| `settings` | ai_provider 편집·override 검증 |
| `prompts` / `prompt_versions` | 버전 CRUD·활성 포인터·롤백 |
| `document_templates` / `document_template_versions` | 동일 |

- 상태 / invariant: 저장은 항상 새 버전(기존 불변), 롤백은 포인터 이동(복사 없음). output_schema는 envelope 내부 form만 관장(코드 고정 envelope 불변).
- Migration 필요 여부: 없음.
- SPEC에 환류: 없음 예상.

## Execution

### Phase 1 — AI Provider 설정 API

- **Status**: TODO
- **작업**:
  - [ ] settings 조회/갱신 + task-overrides CRUD(등록 definition 검증) + health
- **검증**: [ ] SPEC-007 Validation·Case Matrix, 비소급 규칙(진행 중 task 영향 없음)

### Phase 2 — Prompts API

- **Status**: TODO
- **작업**:
  - [ ] 목록/버전/저장(쌍 저장+활성)/롤백 + JSON Schema 검증
- **검증**: [ ] SPEC-009 AC (빈 본문/무효 스키마 거부, 롤백 쌍 전환)

### Phase 3 — Templates API

- **Status**: TODO
- **작업**:
  - [ ] 목록/버전/저장/롤백 (key 3종 검증)
- **검증**: [ ] SPEC-010 AC (스탬프 계약은 WP3 초안 생성과 연동 확인)

### Phase 4 — FE 설정 탭

- **Status**: TODO
- **작업**:
  - [ ] 탭 3개 + 목록/편집기/버전 히스토리 + 확인 모달
- **검증**: [ ] page-settings.html 시안 대비 UX AC

## Pre-deploy Check

- [ ] provider credential이 응답/클라이언트에 노출되지 않음
- [ ] output_schema 무효 저장이 파이프라인을 깨지 않음(활성 전환 전 검증)

## Rollback

- 작업 레포 커밋 단위 revert. 설정 데이터는 버전 롤백으로 복구.

## Done Criteria

- [ ] 모든 Phase DONE/SUPERSEDED
- [ ] SPEC-007/009/010 AC 반영
- [ ] product `log.md`·`30-work/README.md` 갱신

## Open Issues

- 템플릿 개정 시 기존 문서 재적용 정책 (SPEC-010 OQ — 운영 전 결정).
